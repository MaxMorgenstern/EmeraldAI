import cv2
import glob
import os
import re
import numpy as np
import platform
import time

class ComputerVision(object):

    def __init__(self):

        self.__ModelFile = "myModel.mdl"
        self.__DictionaryFile = "myDict.npy"

        self.__DatasetBasePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ComputerVisionData")
        self.__TempCVFolder = "Temp"
        self.__DisabledFileFolder = "Disabled"

        self.__ImageLimit = 100

        self.__ResizeWidth = 350
        self.__ResizeHeight = 350

        self.__PredictionTimeout = 5
        self.__PredictStreamTimeout = 0


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

    def __cropFaces(self, img, faces):
        faceImages = []
        for face in faces:
            x, y, h, w = [result for result in face]
            faceImages.append(img[y:y+h,x:x+w])
        return faceImages

    def __saveImg(self, img, datasetName, imageType, fileName):
        try:
            self.__ensureDirectoryExists(os.path.join(self.__DatasetBasePath, datasetName))
            self.__ensureDirectoryExists(os.path.join(self.__DatasetBasePath, datasetName, imageType))

            out = cv2.resize(img, (self.__ResizeWidth, self.__ResizeHeight)) #Resize face so all images have same size

            # TODO
            cv2.imwrite("%s/%s/%s/%s.jpg" %(self.__DatasetBasePath, datasetName, imageType, fileName), out) #Write image
        except:
           pass #If error, pass file

    def __loadImages(self, datasetName):
        trainingData = []
        trainingLabels = []
        trainingLabelsDict = {}

        for dirname, dirnames, filenames in os.walk(os.path.join(self.__DatasetBasePath, datasetName)):
            for subdirname in dirnames:
                subjectPath = os.path.join(dirname, subdirname)
                for filename in os.listdir(subjectPath):
                    if(not filename.startswith('.')):
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

    def Predict(self, image, model, dictionary):
        faces = self.DetectFaceBest(image)
        result = []
        if len(faces) > 0:
            croppedFaceImages = self.__cropFaces(image, faces)
            for croppedImage in croppedFaceImages:

                resized = cv2.resize(self.__toGrayscale(croppedImage), (self.__ResizeWidth, self.__ResizeHeight))

                prediction = model.predict(resized)

                result.append({
                    'face': {
                        'id': len(result)+1,
                        'value': dictionary.keys()[dictionary.values().index(prediction[0])],
                        'rawvalue': prediction[0],
                        'distance': prediction[1],
                        'coords': {
                            'x': str(faces[0][0]),
                            'y': str(faces[0][1]),
                            'width': str(faces[0][2]),
                            'height': str(faces[0][3])
                        }
                    }
                })
        return result

    def TakeFaceImage(self, image, imageType, datasetName=None):
        if datasetName == None:
            datasetName = self.__TempCVFolder
        faces = self.DetectFaceFast(image)
        if len(faces) > 0:
            croppedFaceImages = self.__cropFaces(image, faces)
            for croppedImage in croppedFaceImages:
                resizedImage = cv2.resize(self.__toGrayscale(croppedImage), (self.__ResizeWidth, self.__ResizeHeight))

                fileName = str(self.__getHighestImageID(datasetName, imageType) + 1)
                self.__saveImg(resizedImage, datasetName, imageType, fileName)



    # TODO
    def PredictStream(self, image, model, dictionary, threshold, timeout=None):
        if timeout == None:
            timeout = self.__PredictionTimeout

        if time.time() > self.__PredictStreamTimeout:
            self.__PredictStreamTimeout = time.time() + timeout
            # TODO: whipe data

        # IF distance > maxDistance --> unknown

        prediction = self.Predict(image, model, dictionary)
        for p in prediction:
            print p['face']['value'], p['face']['distance']
            # TODO - more than one --> notify or prediction array

        return prediction



    # TODO
    def LimitImagesInFolder(self, datasetName, amount=None):
        if amount == None:
            amount = self.__ImageLimit

        for dirname, dirnames, filenames in os.walk(os.path.join(self.__DatasetBasePath, datasetName)):
            for subdirname in dirnames:
                subjectPath = os.path.join(dirname, subdirname)
                dirContent = os.listdir(subjectPath)
                if len(dirContent) > amount:
                    filesToDeactivate = len(dirContent) - amount
                    for filename in dirContent:
                        print time.ctime(self.__getCreationDate(os.path.join(subjectPath, filename)))


    def __disableFile(self, filePath, fileName):
        os.rename(os.path.join(filePath, fileName), os.path.join(filePath, self.__DisabledFileFolder, fileName))

    def __getCreationDate(self, filePath):
        if platform.system() == 'Windows':
            return os.path.getctime(filePath)
        else:
            stat = os.stat(filePath)
            try:
                return stat.st_birthtime
            except AttributeError:
                return stat.st_mtime


cv = ComputerVision()


#cv.TrainModel("mood")
#exit()


#cv.LimitImagesInFolder("mood", 10)
#exit()

model, dictionary = cv.LoadModel("mood")


camera = cv2.VideoCapture(0)
ret = camera.set(3, 640)
ret = camera.set(4, 480)

count = 0

while True:
    ret, image = camera.read()

    #cv.TakeFaceImage(image, "normal")

    #result = cv.Predict(image, model, dictionary)
    result = cv.PredictStream(image, model, dictionary, 100)
    if(len(result) > 0):
        #print result
        print ""
        print ""
        print result[0]['face']['value'], " - ", result[0]['face']['distance']


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
