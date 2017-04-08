#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import glob
import os
import re
import numpy as np
import platform
import time
import operator
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Logic.Singleton import Singleton

# TODO: replace print with log
# TODO: add logging
# TODO: body detection
# TODO: test line 60 --> #gray = cv2.equalizeHist(gray)

class ComputerVision(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__ModelFile = "myCVModel.mdl"
        self.__DictionaryFile = "myCVDict.npy"

        self.__DatasetBasePath = os.path.join(Global.EmeraldPath, "Data", "ComputerVisionData")
        self.__TempCVFolder = "Temp"
        self.__DisabledFileFolder = "Disabled"

        self.__UnknownUserTag = Config().Get("ComputerVision", "UnknownUserTag") # Unknown
        self.__NotKnownDataPrefix = Config().Get("ComputerVision", "NotKnownDataPrefix") # NotKnown

        self.__ImageLimit = Config().GetInt("ComputerVision", "ImageLimit") # 100

        self.__ResizeWidth = Config().GetInt("ComputerVision", "ImageSizeWidth") # 350
        self.__ResizeHeight = Config().GetInt("ComputerVision", "ImageSizeHeight") # 350

        self.__PredictionTimeout = Config().GetInt("ComputerVision.Prediction", "PredictionTimeout") # 5
        self.__PredictStreamThreshold = Config().GetInt("ComputerVision.Prediction", "PredictionThreshold") # 300
        self.__PredictStreamTimeoutDate = 0
        self.__PredictStreamTimeoutBool = False
        self.__PredictStreamMaxDistance = Config().GetInt("ComputerVision.Prediction", "MaxPredictionDistance") # 500
        self.__PredictStreamResult = {}

        self.__haarDir = os.path.join(Global.EmeraldPath, "Data", "HaarCascades")

        self.__frontalFace = cv2.CascadeClassifier(os.path.join(self.__haarDir, Config().Get("ComputerVision", "HaarcascadeFaceFrontalDefault")))
        self.__frontalFace2 = cv2.CascadeClassifier(os.path.join(self.__haarDir, Config().Get("ComputerVision", "HaarcascadeFaceFrontalAlt")))
        self.__frontalFace3 = cv2.CascadeClassifier(os.path.join(self.__haarDir, Config().Get("ComputerVision", "HaarcascadeFaceFrontalAlt2")))
        self.__frontalFace4 = cv2.CascadeClassifier(os.path.join(self.__haarDir, Config().Get("ComputerVision", "HaarcascadeFaceFrontalAltTree")))
        self.__frontalFace5 = cv2.CascadeClassifier(os.path.join(self.__haarDir, Config().Get("ComputerVision", "HaarcascadeFaceProfile")))

        self.__RecognizerModel = cv2.createFisherFaceRecognizer()
        self.__RecognizerDictionary = {}


    def __toGrayscale(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        #gray = cv2.equalizeHist(gray)
        return gray

    def __cropFace(self, img, face):
        x, y, h, w = [result for result in face]
        return img[y:y+h,x:x+w]

    def __saveImg(self, img, datasetName, imageType, fileName):
        try:
            self.__ensureDirectoryExists(os.path.join(self.__DatasetBasePath, datasetName))
            self.__ensureDirectoryExists(os.path.join(self.__DatasetBasePath, datasetName, imageType))

            out = cv2.resize(img, (self.__ResizeWidth, self.__ResizeHeight)) #Resize face so all images have same size

            cv2.imwrite(os.path.join(self.__DatasetBasePath, datasetName, imageType, fileName), out) #Write image
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

                            if (subdirname not in trainingLabelsDict):
                                trainingLabelsDict[subdirname] = len(trainingLabelsDict)
                            labelID = trainingLabelsDict[subdirname]

                            trainingLabels.append(labelID)
                        except IOError, (errno, strerror):
                            print "IOError"
                        except:
                            print "Error"
        return trainingData, np.asarray(trainingLabels), trainingLabelsDict

    def __ensureDirectoryExists(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

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
        self.__ensureDirectoryExists(os.path.join(filePath, self.__DisabledFileFolder))
        os.rename(os.path.join(filePath, fileName), os.path.join(filePath, self.__DisabledFileFolder, fileName))


    def LimitImagesInFolder(self, datasetName, amount=None):
        if amount == None:
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

    def DetectFaceFast(self, img):
        face = self.__frontalFace.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face) > 0:
            return face

        face2 = self.__frontalFace2.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face2) > 0:
            return face2

        face3 = self.__frontalFace3.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face3) > 0:
            return face3

        face4 = self.__frontalFace4.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face4) > 0:
            return face4

        face5 = self.__frontalFace5.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face5) > 0:
            return face
        return []

    def DetectFaceBest(self, img):
        face = self.__frontalFace.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        face2 = self.__frontalFace2.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        face3 = self.__frontalFace3.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        face4 = self.__frontalFace4.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        face5 = self.__frontalFace5.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

        bestResult = face
        if (len(bestResult) < len(face2)):
            bestResult = face2
        if (len(bestResult) < len(face3)):
            bestResult = face3
        if (len(bestResult) < len(face4)):
            bestResult = face4
        if (len(bestResult) < len(face5)):
            bestResult = face5
        return bestResult


    def TrainModel(self, datasetName, imageSize=None):
        if imageType == None:
            imageSize = "{0}x{1}".format(self.__ResizeWidth, self.__ResizeHeight)
        images, labels, labelDict = self.__loadImages(datasetName, imageSize)
        if len(images) == 0 or len(labels) == 0:
        	print "Error, no data given"
        	return
        self.__RecognizerModel.train(images, labels)
        self.__RecognizerDictionary = labelDict

        path = os.path.join(self.__DatasetBasePath, datasetName)
        self.__RecognizerModel.save(os.path.join(path, self.__ModelFile))
        np.save(os.path.join(path, self.__DictionaryFile), labelDict)


    def LoadModel(self, datasetName):
        path = os.path.join(self.__DatasetBasePath, datasetName)
        try:
            self.__RecognizerModel.load(os.path.join(path, self.__ModelFile))
            self.__RecognizerDictionary = np.load(os.path.join(path, self.__DictionaryFile)).item()
            return self.__RecognizerModel, self.__RecognizerDictionary
        except Exception as e:
            print "Error while opening File", e
            return None, None

    def TakeFaceImage(self, image, imageType, datasetName=None):
        if datasetName == None:
            datasetName = self.__TempCVFolder
        faces = self.DetectFaceBest(image)
        if len(faces) > 0:
            for face in faces:
                croppedImage = self.__cropFace(image, face)
                resizedImage = cv2.resize(self.__toGrayscale(croppedImage), (self.__ResizeWidth, self.__ResizeHeight))

                fileName = str(self.__getHighestImageID(datasetName, imageType) + 1) + ".jpg"
                self.__saveImg(resizedImage, datasetName, imageType, fileName)

    def Predict(self, image, model, dictionary):
        faces = self.DetectFaceBest(image)
        result = []
        if len(faces) > 0:
            for face in faces:
                croppedImage = self.__cropFace(image, face)
                resizedImage = cv2.resize(self.__toGrayscale(croppedImage), (self.__ResizeWidth, self.__ResizeHeight))
                prediction = model.predict(resizedImage)

                try:
                    result.append({
                        'face': {
                            'id': len(result)+1,
                            'data': [{
                                'model': '',
                                'value': dictionary.keys()[dictionary.values().index(prediction[0])],
                                'rawvalue': prediction[0],
                                'distance': prediction[1]
                                }],
                            'coords': {
                                'x': str(face[0]),
                                'y': str(face[1]),
                                'width': str(face[2]),
                                'height': str(face[3])
                            }
                        }
                    })
                except Exception as e:
                    print "Value Error", e
        return result

    def PredictStream(self, image, model, dictionary, threshold=None, timeout=None):
        if threshold == None:
            threshold = self.__PredictStreamThreshold

        if timeout == None:
            timeout = self.__PredictionTimeout

        # reset is timeout happened on last call
        if self.__PredictStreamTimeoutBool:
            self.__PredictStreamResult = {}
            self.__PredictStreamTimeoutDate = time.time() + timeout
            self.__PredictStreamTimeoutBool = False

        #check if current call times out
        reachedTimeout = False
        if time.time() > self.__PredictStreamTimeoutDate:
            reachedTimeout = True
            self.__PredictStreamTimeoutBool = True

        prediction = self.Predict(image, model, dictionary)
        for key, value in enumerate(prediction):
            data = value['face']['data'][0]

            if int(data['distance']) > self.__PredictStreamMaxDistance or data['value'].startswith(self.__NotKnownDataPrefix):
                self.__addPrediction(key, self.__UnknownUserTag, (int(data['distance']) - self.__PredictStreamMaxDistance))
            else:
                self.__addPrediction(key, data['value'], int(data['distance']))

        return self.__PredictStreamResult, self.__thresholdReached(threshold), reachedTimeout

    def PredictMultiple(self, image, predictionObjectList):
        faces = self.DetectFaceBest(image)
        result = []
        if len(faces) > 0:
            faceId = 1
            for face in faces:
                croppedImage = self.__cropFace(image, face)
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
                        print "Value Error", e

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
        return result

    def PredictMultipleStream(self, image, predictionObjectList, threshold=None, timeout=None):
        if threshold == None:
            threshold = self.__PredictStreamThreshold

        if timeout == None:
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

        reachedThreshold = False

        prediction = self.PredictMultiple(image, predictionObjectList)

        for key, value in enumerate(prediction):
            dataArray = value['face']['data']
            for data in dataArray:
                for predictionObject in predictionObjectList:
                    if data['model'] == predictionObject.Name:
                        if int(data['distance']) > predictionObject.MaxPredictionDistance or data['value'].startswith(self.__NotKnownDataPrefix):
                            predictionObject.AddPrediction(key, self.__UnknownUserTag, (int(data['distance']) - predictionObject.MaxPredictionDistance))
                        else:
                            predictionObject.AddPrediction(key, data['value'], int(data['distance']))

        for predictionObject in predictionObjectList:
            if predictionObject.ThresholdReached(threshold):
                reachedThreshold = True

        return predictionObjectList, reachedThreshold, reachedTimeout
