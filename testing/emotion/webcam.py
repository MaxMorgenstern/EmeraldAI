import cv2
import glob
import os
import re
import numpy as np

class ComputerVision(object):

    def __init__(self):

        self.__ModelFile = "myModel.mdl"
        self.__DictionaryFile = "myDict.npy"

        self._DatasetBasePath = os.path.dirname(os.path.abspath(__file__)) +  os.sep + "ComputerVisionData"
        self.__TempCVFolder = "Temp"

        self.__resizeWidth = 350
        self.__resizeHeight = 350

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
            self.__ensureDirectoryExists(self._DatasetBasePath + os.sep + datasetName)
            self.__ensureDirectoryExists(self._DatasetBasePath + os.sep + datasetName + os.sep + imageType)

            out = cv2.resize(img, (self.__resizeWidth, self.__resizeHeight)) #Resize face so all images have same size

            # TODO
            cv2.imwrite("%s/%s/%s/%s.jpg" %(self._DatasetBasePath, datasetName, imageType, fileName), out) #Write image
        except:
           pass #If error, pass file

    def __loadImages(self, modelType):
        trainingData = []
        trainingLabels = []
        trainingLabelsDict = {}

        for dirname, dirnames, filenames in os.walk(self._DatasetBasePath + os.sep + modelType):
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
        for root, dirs, filenames in os.walk(self._DatasetBasePath + os.sep + datasetName + os.sep + imageType):
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

    def TrainModel(self, modelType):
        images, labels, labelDict = self.__loadImages(modelType)
        self.__RecognizerModel.train(images, labels)
        self.__RecognizerDictionary = labelDict

        path = self._DatasetBasePath + os.sep + modelType + os.sep
        self.__RecognizerModel.save(path + self.__ModelFile)
        np.save(path + self.__DictionaryFile, labelDict)

    def LoadModel(self, modelType):
        path = self._DatasetBasePath + os.sep + modelType + os.sep
        self.__RecognizerModel.load(path + self.__ModelFile)
        self.__RecognizerDictionary = np.load(path + self.__DictionaryFile).item()

        return self.__RecognizerModel, self.__RecognizerDictionary


    #todo
    def Predict(self, image, model, dictionary):
        faces = self.DetectFaceBest(image)
        result = []
        if len(faces) > 0:
            croppedFaceImages = self.__cropFaces(image, faces)
            for croppedImage in croppedFaceImages:

                resized = cv2.resize(self.__toGrayscale(croppedImage), (self.__resizeWidth, self.__resizeHeight))

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

    def TakeFaceImage(self, image, imageType):
        faces = self.DetectFaceFast(image)
        if len(faces) > 0:
            croppedFaceImages = self.__cropFaces(image, faces)
            for croppedImage in croppedFaceImages:
                resizedImage = cv2.resize(self.__toGrayscale(croppedImage), (self.__resizeWidth, self.__resizeHeight))

                fileName = str(self.__getHighestImageID(self.__TempCVFolder, imageType) + 1)
                self.__saveImg(resizedImage, self.__TempCVFolder, imageType, fileName)

    def LimitImagesInFolder(self, amount):
        return "TODO"

cv = ComputerVision()

#cv.TrainModel("mood")
#exit()


model, dictionary = cv.LoadModel("mood")


camera = cv2.VideoCapture(0)
ret = camera.set(3, 640)
ret = camera.set(4, 480)

count = 0

while True:
    ret, image = camera.read()

    #cv.TakeFaceImage(image, "normal")

    result = cv.Predict(image, model, dictionary)
    print result
    print ""
    print ""

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
