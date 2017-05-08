import cv2
import glob
import os
import re
import numpy as np
import platform
import time
import operator

"""
TODO: check why we get lot of:
Value Error 1701013047 is not in list
Value Error 32718 is not in list
"""

class ComputerVision(object):

    def __init__(self):
        self.__ModelFile = "myModel.mdl"
        self.__DictionaryFile = "myDict.npy"

        self.__DatasetBasePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ComputerVisionData")
        self.__TempCVFolder = "Temp"
        self.__DisabledFileFolder = "Disabled"

        self.__UnknownUserTag = "Unknown"

        self.__ImageLimit = 100

        self.__ResizeWidth = 350
        self.__ResizeHeight = 350

        self.__PredictionTimeout = 5
        self.__PredictStreamThreshold = 300
        self.__PredictStreamTimeoutDate = 0
        self.__PredictStreamTimeoutBool = False
        self.__PredictStreamMaxDistance = 500
        self.__PredictStreamResult = {}

        self.__frontalFace = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.__frontalFace2 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
        self.__frontalFace3 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        self.__frontalFace4 = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")
        self.__frontalFace5 = cv2.CascadeClassifier("haarcascade_profileface.xml")

        self.__RecognizerModel = cv2.createFisherFaceRecognizer()
        self.__RecognizerDictionary = {}


    def __toGrayscale(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
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

    def __loadImages(self, datasetName):
        trainingData = []
        trainingLabels = []
        trainingLabelsDict = {}

        for dirname, dirnames, filenames in os.walk(os.path.join(self.__DatasetBasePath, datasetName)):
            for subdirname in dirnames:
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


    def TrainModel(self, datasetName):
        images, labels, labelDict = self.__loadImages(datasetName)
        self.__RecognizerModel.train(images, labels)
        self.__RecognizerDictionary = labelDict

        path = os.path.join(self.__DatasetBasePath, datasetName)
        self.__RecognizerModel.save(os.path.join(path, self.__ModelFile))
        np.save(os.path.join(path, self.__DictionaryFile), labelDict)


    def LoadModel(self, datasetName):
        path = os.path.join(self.__DatasetBasePath, datasetName)
        self.__RecognizerModel.load(os.path.join(path, self.__ModelFile))
        self.__RecognizerDictionary = np.load(os.path.join(path, self.__DictionaryFile)).item()

        return self.__RecognizerModel, self.__RecognizerDictionary

    def TakeFaceImage(self, image, imageType, datasetName=None):
        if datasetName == None:
            datasetName = self.__TempCVFolder
        faces = self.DetectFaceFast(image)
        if len(faces) > 0:
            for face in faces:
                croppedImage = self.__cropFace(image, face)
                resizedImage = cv2.resize(self.__toGrayscale(croppedImage), (self.__ResizeWidth, self.__ResizeHeight))

                fileName = str(self.__getHighestImageID(datasetName, imageType) + 1)
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

            if int(data['distance']) > self.__PredictStreamMaxDistance:
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
                    print "--", predictionObject.Name, predictionObject.Dictionary

                    prediction = predictionObject.Model.predict(resizedImage)

                    try:
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
        print prediction
        for key, value in enumerate(prediction):
            dataArray = value['face']['data']
            for data in dataArray:
                for predictionObject in predictionObjectList:
                    if data['model'] == predictionObject.Name:
                        if int(data['distance']) > predictionObject.MaxPredictionDistance:
                            predictionObject.AddPrediction(key, self.__UnknownUserTag, (int(data['distance']) - predictionObject.MaxPredictionDistance))
                        else:
                            predictionObject.AddPrediction(key, data['value'], int(data['distance']))

        for predictionObject in predictionObjectList:
            if predictionObject.ThresholdReached(threshold):
                reachedThreshold = True

        return predictionObjectList, reachedThreshold, reachedTimeout


class PredictionObject(object):
    def __init__(self, name, model, dictionary, maxDistance):
        self.Name = name
        self.Model = model
        self.Dictionary = dictionary
        self.PredictionResult = {}

        self.MaxPredictionDistance = maxDistance
        self.__UnknownUserTag = "Unknown"

    def AddPrediction(self, id, key, distance):
        if(self.PredictionResult.has_key(id)):
            if(self.PredictionResult[id].has_key(key)):
                self.PredictionResult[id][key] += (self.MaxPredictionDistance - distance) / 10
            else:
                self.PredictionResult[id][key] = (self.MaxPredictionDistance - distance) / 10
        else:
            self.PredictionResult[id] = {}
            self.PredictionResult[id][key] = (self.MaxPredictionDistance - distance) / 10

    def ThresholdReached(self, threshold):
        if len(self.PredictionResult) > 0:
            for key, resultSet in self.PredictionResult.iteritems():
                maxKey = max(resultSet.iteritems(), key=operator.itemgetter(1))[0]
                if maxKey != self.__UnknownUserTag and threshold < resultSet[maxKey]:
                    return True
        return False

    def ResetResult(self):
        self.PredictionResult = {}

    def __repr__(self):
         return "Result:{0}".format(self.PredictionResult)

    def __str__(self):
         return "Result:{0}".format(self.PredictionResult)






cv = ComputerVision()

#cv.TrainModel("person")
#exit()


#cv.LimitImagesInFolder("mood", 5)
#exit()

model, dictionary = cv.LoadModel("mood")


moodModel, moodDictionary = cv.LoadModel("mood")
personModel, personDictionary = cv.LoadModel("person")

print moodDictionary
print personDictionary

print type(cv) is ComputerVision
print type(model), type(dictionary)
#exit()


camera = cv2.VideoCapture(0)
ret = camera.set(3, 640)
ret = camera.set(4, 480)

count = 0


predictionObjectList = []
predictionObjectList.append(PredictionObject("mood", moodModel, moodDictionary, 500))
predictionObjectList.append(PredictionObject("person", personModel, personDictionary, 500))


while True:
    ret, image = camera.read()

    #cv.TakeFaceImage(image, "normal")

    #result = cv.PredictMultiple(image, predictionObjectList)
    result, thresholdReached, timeoutReached = cv.PredictStream(image, predictionObjectList)

    #result = cv.Predict(image, model, dictionary)
    #result, thresholdReached, timeoutReached = cv.PredictStream(image, model, dictionary)
    if(len(result) > 0):
        print thresholdReached, timeoutReached, result
        #print ""
        #print result
        #print result[0]['face']['value'], " - ", result[0]['face']['distance']


"""
    if len(faces) > 0:

        cropped = to_grayscale(crop_faces(image, faces))
        resized = cv2.resize(cropped, (350,350))
        save_img(resized, "neutral", count)
        count +=1

    #if (image != None):
    #    cv2.rectangle(image, (int(coords['x']), int(coords['y'])), (int(coords['x']) + int(coords['width']), int(coords['y']) + int(coords['height'])), (0, 0, 255), 1)
    #    cv2.putText(image, textStr, (int(coords['x']) - 10, int(coords['y']) - 10), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 255), 1)

    cv2.imshow("image", image)
"""
