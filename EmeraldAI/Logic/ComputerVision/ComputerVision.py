#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import os
import re
import numpy as np
import platform
import time
import operator
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.Logger import *

class DetectionSettings(object):
    def __init__(self, scale, minNeighbors, minSize):
        self.Scale = scale
        self.MinNeighbors = minNeighbors
        self.MinSize = minSize

class ComputerVision(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__ModelFile = "myCVModel{0}.mdl"
        self.__DictionaryFile = "myCVDict{0}.npy"

        if(Config().Get("ComputerVision", "DetectionSettings") == "precise"):
            self.__DetectionSettings = DetectionSettings(1.2, 4, (80, 80))
            self.__FaceDetectionSettings = DetectionSettings(1.1, 4, (30, 30))
            self.__FastDetection = False
            self.__SkipUnlikelyClassifier = False
        else:
            self.__DetectionSettings = DetectionSettings(1.3, 4, (100, 100))
            self.__FaceDetectionSettings = DetectionSettings(1.2, 4, (50, 50))

            self.__SkipUnlikelyClassifier = True
            if(Config().Get("ComputerVision", "DetectionSettings") == "medium"):
                self.__FastDetection = False
            else:
                self.__FastDetection = True


        self.__DatasetBasePath = os.path.join(Global.EmeraldPath, "Data", "ComputerVisionData")
        self.__TempCVFolder = "Temp"
        self.__DisabledFileFolder = "Disabled"

        self.__UnknownUserTag = Config().Get("ComputerVision", "UnknownUserTag") # Unknown
        self.__NotKnownDataTag = Config().Get("ComputerVision", "NotKnownDataTag") # NotKnown

        self.__ImageLimit = Config().GetInt("ComputerVision", "ImageLimit") # 100

        self.__ResizeWidth = Config().GetInt("ComputerVision", "ImageSizeWidth") # 350
        self.__ResizeHeight = Config().GetInt("ComputerVision", "ImageSizeHeight") # 350

        self.__PredictionTimeout = Config().GetInt("ComputerVision.Prediction", "PredictionTimeout") # 5
        self.__PredictStreamTimeoutDate = 0
        self.__PredictStreamTimeoutBool = False
        self.__PredictStreamMaxDistance = Config().GetInt("ComputerVision.Prediction", "MaxPredictionDistance") # 500
        self.__PredictStreamResult = {}

        self.__haarDir = os.path.join(Global.EmeraldPath, "Data", "HaarCascades")

        self.__frontalFace = cv2.CascadeClassifier(os.path.join(self.__haarDir, "haarcascade_frontalface_default.xml"))
        self.__frontalFace2 = cv2.CascadeClassifier(os.path.join(self.__haarDir, "haarcascade_frontalface_alt.xml"))
        self.__frontalFace3 = cv2.CascadeClassifier(os.path.join(self.__haarDir, "haarcascade_frontalface_alt2.xml"))
        self.__frontalFace4 = cv2.CascadeClassifier(os.path.join(self.__haarDir, "haarcascade_frontalface_alt_tree.xml"))
        self.__frontalFace5 = cv2.CascadeClassifier(os.path.join(self.__haarDir, "haarcascade_profileface.xml"))

        self.__fullBody = cv2.CascadeClassifier(os.path.join(self.__haarDir, "haarcascade_fullbody.xml"))
        self.__upperBody = cv2.CascadeClassifier(os.path.join(self.__haarDir, "haarcascade_upperbody.xml"))
        self.__headShoulders = cv2.CascadeClassifier(os.path.join(self.__haarDir, "haarcascade_head_shoulders.xml"))


        if(Config().Get("ComputerVision", "Recognizer") == "FisherFace"):
            try:
                self.__RecognizerModel = cv2.createFisherFaceRecognizer()
            except:
                self.__RecognizerModel = cv2.face.createFisherFaceRecognizer()
        else:
            try:
                self.__RecognizerModel = cv2.createLBPHFaceRecognizer()
            except:
                self.__RecognizerModel = cv2.face.createLBPHFaceRecognizer()

        self.__RecognizerDictionary = {}


    def __toGrayscale(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.equalizeHist(gray)
        return gray

    # TODO - check if this should be x, y, w, h
    def __cropImage(self, img, face):
        x, y, h, w = [result for result in face]
        return img[y:y+h,x:x+w]

    def __saveImg(self, img, datasetName, imageType, fileName):
        try:
            Global.EnsureDirectoryExists(os.path.join(self.__DatasetBasePath, datasetName))
            Global.EnsureDirectoryExists(os.path.join(self.__DatasetBasePath, datasetName, imageType))

            cv2.imwrite(os.path.join(self.__DatasetBasePath, datasetName, imageType, fileName), img) #Write image
        except:
           pass #If error, pass file

    def __loadImages(self, datasetName, imageSize=None):
        trainingData = []
        trainingLabels = []
        trainingLabelsDict = {}

        for dirname, dirnames, filenames in os.walk(os.path.join(self.__DatasetBasePath, datasetName)):
            for subdirname in dirnames:
                if imageSize != None and not subdirname.startswith(imageSize):
                    continue

                if subdirname == self.__DisabledFileFolder:
                    continue

                subjectPath = os.path.join(dirname, subdirname)
                for filename in os.listdir(subjectPath):
                    if(not filename.startswith('.') and filename != self.__DisabledFileFolder):
                        try:
                            image = cv2.imread(os.path.join(subjectPath, filename), cv2.IMREAD_GRAYSCALE)
                            trainingData.append(image)

                            trimmedSubdirname = subdirname.replace(imageSize, "")

                            if (trimmedSubdirname not in trainingLabelsDict):
                                trainingLabelsDict[trimmedSubdirname] = len(trainingLabelsDict)
                            labelID = trainingLabelsDict[trimmedSubdirname]

                            trainingLabels.append(labelID)
                        except IOError, (errno, strerror):
                            FileLogger().Error("ComputerVision: IO Exception: {0}".format(strerror))
                        except Exception as e:
                            FileLogger().Error("ComputerVision: Exception: {0}".format(e))
        return trainingData, np.asarray(trainingLabels), trainingLabelsDict

    def __getHighestImageID(self, datasetName, imageType):
        maxImgNum = 0
        for root, dirs, filenames in os.walk(os.path.join(self.__DatasetBasePath, datasetName, imageType)):
            for f in filenames:
                tmpNum = re.findall('\d+|$', f)[0]
                if(len(tmpNum) > 0 and int(tmpNum) > maxImgNum):
                    maxImgNum = int(tmpNum)
        return int(maxImgNum)

    def __thresholdReached(self, threshold):
        if len(self.__PredictStreamResult) > 0:
            for key, resultSet in self.__PredictStreamResult.iteritems():
                maxKey = max(resultSet.iteritems(), key=operator.itemgetter(1))[0]
                if maxKey != self.__UnknownUserTag and threshold < resultSet[maxKey]:
                    return True
        return False

    def __addPrediction(self, id, key, distance):
        if(self.__PredictStreamResult.has_key(id)):
            if(self.__PredictStreamResult[id].has_key(key)):
                self.__PredictStreamResult[id][key] += (self.__PredictStreamMaxDistance - distance) / 10
            else:
                self.__PredictStreamResult[id][key] = (self.__PredictStreamMaxDistance - distance) / 10
        else:
            self.__PredictStreamResult[id] = {}
            self.__PredictStreamResult[id][key] = (self.__PredictStreamMaxDistance - distance) / 10

    def __getSortedListDir(self, path):
        if platform.system() == 'Windows':
            mtime = lambda f: os.stat(os.path.join(path, f)).st_ctime
        else:
            mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        return list(sorted(os.listdir(path), key=mtime))

    def __disableFile(self, filePath, fileName):
        Global.EnsureDirectoryExists(os.path.join(filePath, self.__DisabledFileFolder))
        os.rename(os.path.join(filePath, fileName), os.path.join(filePath, self.__DisabledFileFolder, fileName))


    def LimitImagesInFolder(self, datasetName, amount=None):
        if amount is None:
            amount = self.__ImageLimit
        amount += 2 # add one for 'Disabled' folder and one for eventual hidden file

        for dirname, dirnames, filenames in os.walk(os.path.join(self.__DatasetBasePath, datasetName)):
            for subdirname in dirnames:
                if subdirname == self.__DisabledFileFolder:
                    continue

                subjectPath = os.path.join(dirname, subdirname)
                dirContent = self.__getSortedListDir(subjectPath)
                if len(dirContent) > amount:
                    filesToDeactivate = len(dirContent) - amount
                    for filename in dirContent:
                        if(not filename.startswith('.')):
                            if filesToDeactivate > 0:
                                self.__disableFile(subjectPath, filename)
                                filesToDeactivate -= 1
                            else:
                                continue

    def GetLuma(self, img):
        averageColor = np.average(np.average(img, axis=0), axis=0) # averageColor: BGR!!!
        return (0.299 * averageColor[2] + 0.587 * averageColor[1] + 0.114 * averageColor[0])

    def DetectBody(self, img):
        bodies = self.__headShoulders.detectMultiScale(img, scaleFactor=self.__DetectionSettings.Scale, minNeighbors=self.__DetectionSettings.MinNeighbors, minSize=self.__DetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)
        if len(bodies) > 0:
            return bodies

        if not self.__SkipUnlikelyClassifier:
            bodies = self.__fullBody.detectMultiScale(img, scaleFactor=self.__DetectionSettings.Scale, minNeighbors=self.__DetectionSettings.MinNeighbors, minSize=self.__DetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)
            if len(bodies) > 0:
                return bodies

            bodies = self.__upperBody.detectMultiScale(img, scaleFactor=self.__DetectionSettings.Scale, minNeighbors=self.__DetectionSettings.MinNeighbors, minSize=self.__DetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)
            if len(bodies) > 0:
                return bodies
        return []

    def DetectFaceFast(self, img):
        face = self.__frontalFace.detectMultiScale(img, scaleFactor=self.__FaceDetectionSettings.Scale, minNeighbors=self.__FaceDetectionSettings.MinNeighbors, minSize=self.__FaceDetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face) > 0:
            return face

        face5 = self.__frontalFace5.detectMultiScale(img, scaleFactor=self.__FaceDetectionSettings.Scale, minNeighbors=self.__FaceDetectionSettings.MinNeighbors, minSize=self.__FaceDetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face5) > 0:
            return face

        if not self.__SkipUnlikelyClassifier:
            face2 = self.__frontalFace2.detectMultiScale(img, scaleFactor=self.__FaceDetectionSettings.Scale, minNeighbors=self.__FaceDetectionSettings.MinNeighbors, minSize=self.__FaceDetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)
            if len(face2) > 0:
                return face2

            face3 = self.__frontalFace3.detectMultiScale(img, scaleFactor=self.__FaceDetectionSettings.Scale, minNeighbors=self.__FaceDetectionSettings.MinNeighbors, minSize=self.__FaceDetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)
            if len(face3) > 0:
                return face3

            face4 = self.__frontalFace4.detectMultiScale(img, scaleFactor=self.__FaceDetectionSettings.Scale, minNeighbors=self.__FaceDetectionSettings.MinNeighbors, minSize=self.__FaceDetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)
            if len(face4) > 0:
                return face4
        return []

    def DetectFaceBest(self, img):
        face = self.__frontalFace.detectMultiScale(img, scaleFactor=self.__FaceDetectionSettings.Scale, minNeighbors=self.__FaceDetectionSettings.MinNeighbors, minSize=self.__FaceDetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)
        face5 = self.__frontalFace5.detectMultiScale(img, scaleFactor=self.__FaceDetectionSettings.Scale, minNeighbors=self.__FaceDetectionSettings.MinNeighbors, minSize=self.__FaceDetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)

        if not self.__SkipUnlikelyClassifier:
            face2 = self.__frontalFace2.detectMultiScale(img, scaleFactor=self.__FaceDetectionSettings.Scale, minNeighbors=self.__FaceDetectionSettings.MinNeighbors, minSize=self.__FaceDetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)
            face3 = self.__frontalFace3.detectMultiScale(img, scaleFactor=self.__FaceDetectionSettings.Scale, minNeighbors=self.__FaceDetectionSettings.MinNeighbors, minSize=self.__FaceDetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)
            face4 = self.__frontalFace4.detectMultiScale(img, scaleFactor=self.__FaceDetectionSettings.Scale, minNeighbors=self.__FaceDetectionSettings.MinNeighbors, minSize=self.__FaceDetectionSettings.MinSize, flags=cv2.CASCADE_SCALE_IMAGE)

        bestResult = face
        if (len(bestResult) < len(face5)):
            bestResult = face5

        if not self.__SkipUnlikelyClassifier:
            if (len(bestResult) < len(face2)):
                bestResult = face2
            if (len(bestResult) < len(face3)):
                bestResult = face3
            if (len(bestResult) < len(face4)):
                bestResult = face4
        return bestResult


    def TrainModel(self, datasetName, imageSize=None):
        if imageSize is None:
            imageSize = "{0}x{1}".format(self.__ResizeWidth, self.__ResizeHeight)
        images, labels, labelDict = self.__loadImages(datasetName, imageSize)
        if len(images) == 0 or len(labels) == 0:
            FileLogger().Error("ComputerVision: No Data given")
            return
        self.__RecognizerModel.train(images, labels)
        self.__RecognizerDictionary = labelDict

        path = os.path.join(self.__DatasetBasePath, datasetName)
        self.__RecognizerModel.save(os.path.join(path, self.__ModelFile.format(imageSize)))
        np.save(os.path.join(path, self.__DictionaryFile.format(imageSize)), labelDict)


    def LoadModel(self, datasetName, imageSize=None):
        if imageSize is None:
            imageSize = "{0}x{1}".format(self.__ResizeWidth, self.__ResizeHeight)
        path = os.path.join(self.__DatasetBasePath, datasetName)
        try:
            self.__RecognizerModel.load(os.path.join(path, self.__ModelFile.format(imageSize)))
            self.__RecognizerDictionary = np.load(os.path.join(path, self.__DictionaryFile.format(imageSize))).item()
            return self.__RecognizerModel, self.__RecognizerDictionary
        except Exception as e:
            FileLogger().Error("ComputerVision: Exception: Error while opening File {0}".format(e))
            return None, None


    def TakeImage(self, image, imageType, dataArray=None, datasetName=None, grayscale=False):
        if datasetName is None:
            datasetName = self.__TempCVFolder

        if(dataArray is None):
            if grayscale:
                image = self.__toGrayscale(image)
            fileName = str(self.__getHighestImageID(datasetName, imageType) + 1) + ".jpg"
            self.__saveImg(image, datasetName, imageType, fileName)
            return True

        if len(dataArray) > 0:
            for imageData in dataArray:
                croppedImage = self.__cropImage(image, imageData)
                if grayscale:
                    croppedImage = self.__toGrayscale(croppedImage)
                resizedImage = cv2.resize(croppedImage, (self.__ResizeWidth, self.__ResizeHeight))

                fileName = str(self.__getHighestImageID(datasetName, imageType) + 1) + ".jpg"
                self.__saveImg(resizedImage, datasetName, imageType, fileName)
                return True
        return False


    def Predict(self, image, predictionObjectList):
        if(self.__FastDetection):
            faces = self.DetectFaceFast(image)
        else:
            faces = self.DetectFaceBest(image)
        result = []
        if len(faces) > 0:
            faceId = 1
            for face in faces:
                croppedImage = self.__cropImage(image, face)
                resizedImage = cv2.resize(self.__toGrayscale(croppedImage), (self.__ResizeWidth, self.__ResizeHeight))

                predictionResult = []
                for predictionObject in predictionObjectList:

                    prediction = None
                    if predictionObject.Model != None:
                        prediction = predictionObject.Model.predict(resizedImage)

                    try:
                        if prediction != None:
                            predictionResult.append({
                                'model': predictionObject.Name,
                                'value': predictionObject.Dictionary.keys()[predictionObject.Dictionary.values().index(prediction[0])],
                                'rawvalue': prediction[0],
                                'distance': prediction[1]
                            })
                    except Exception as e:
                        FileLogger().Error("ComputerVision: Value Error {0}".format(e))

                result.append({
                    'face': {
                        'id': faceId,
                        'data': predictionResult,
                        'coords': {
                            'x': str(face[0]),
                            'y': str(face[1]),
                            'width': str(face[2]),
                            'height': str(face[3])
                        }
                    }
                })

                faceId += 1
        return result, faces


    def PredictStream(self, image, predictionObjectList, timeout=None):
        if timeout is None:
            timeout = self.__PredictionTimeout

        # reset is timeout happened on last call
        if self.__PredictStreamTimeoutBool:
            self.__PredictStreamTimeoutDate = time.time() + timeout
            self.__PredictStreamTimeoutBool = False
            for predictionObject in predictionObjectList:
                predictionObject.ResetResult()

        #check if current call times out
        reachedTimeout = False
        if time.time() > self.__PredictStreamTimeoutDate:
            reachedTimeout = True
            self.__PredictStreamTimeoutBool = True

        prediction, rawFaceData = self.Predict(image, predictionObjectList)

        for key, value in enumerate(prediction):
            dataArray = value['face']['data']
            for data in dataArray:
                for predictionObject in predictionObjectList:
                    if data['model'] == predictionObject.Name:
                        if int(data['distance']) > predictionObject.MaxPredictionDistance or self.__NotKnownDataTag in data['value']:
                            predictionObject.AddPrediction(key, self.__UnknownUserTag, int(data['distance']))
                        else:
                            predictionObject.AddPrediction(key, data['value'], int(data['distance']))

        return predictionObjectList, reachedTimeout, rawFaceData
