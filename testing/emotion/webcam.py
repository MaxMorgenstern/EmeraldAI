import cv2
import glob
import os
import numpy as np

class ComputerVision(object):

    def __init__(self):

        self.__ModelFile = "myModel.mdl"
        self.__DictionaryFile = "myDict.npy"

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
        #gray = cv2.equalizeHist(gray)
        return gray

    # todo - this only crops one face
    def __cropFaces(self, img, faces):
        for face in faces:
            x, y, h, w = [result for result in face]
            return img[y:y+h,x:x+w]

    def __saveImg(self, img, directory, imagetype, filenumber):
        try:
            out = cv2.resize(img, (self.__resizeWidth, self.__resizeHeight)) #Resize face so all images have same size
            cv2.imwrite("%s/%s/%s.jpg" %(directory, imagetype, filenumber), out) #Write image
        except:
           pass #If error, pass file

    def __loadImages(self, directory):
        training_data = []
        training_labels = []
        training_labels_dict = {}

        for dirname, dirnames, filenames in os.walk(directory):
            for subdirname in dirnames:
                subject_path = os.path.join(dirname, subdirname)
                for filename in os.listdir(subject_path):
                    if(not filename.startswith('.')):
                        try:
                            image = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                            training_data.append(image)

                            if (subdirname not in training_labels_dict):
                                training_labels_dict[subdirname] = len(training_labels_dict)
                            labelID = training_labels_dict[subdirname]

                            training_labels.append(labelID)
                        except IOError, (errno, strerror):
                            print "IOError"
                        except:
                            print "Error"
        return training_data, np.asarray(training_labels), training_labels_dict

    def __ensureDirectoryExists(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def DetectSingleFace(self, img):
        face = self.__frontalFace.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face) > 0:
            return face[0]

        face2 = self.__frontalFace2.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face2) > 0:
            return face2[0]

        face3 = self.__frontalFace3.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face3) > 0:
            return face3[0]

        face4 = self.__frontalFace4.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face4) > 0:
            return face4[0]

        face5 = self.__frontalFace5.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face5) > 0:
            return face[0]
        return []

    def DetectAllFace(self, img):
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

    def TrainModel(self, directory):
        images, labels, labelDict = self.__loadImages(directory)
        self.__RecognizerModel.train(images, labels)
        self.__RecognizerDictionary = labelDict

        # TODO... place in "directory"
        self.__RecognizerModel.save(self.__ModelFile)
        np.save(self.__DictionaryFile, labelDict)

    def LoadModel(self, directory):
        # TODO ...load from "directory"
        self.__RecognizerModel.load(self.__ModelFile)
        self.__RecognizerDictionary = np.load(self.__DictionaryFile).item()


    #todo
    def Predict(self, cv_image, model, dictionary):
        faces = self.DetectSingleFace(cv_image)
        result = None
        if len(faces) > 0:
            cropped = self.__toGrayscale(self.__cropFaces(cv_image, faces))
            resized = cv2.resize(cropped, (self.__resizeWidth, self.__resizeHeight))

            prediction = model.predict(resized)

            result = {
                'face': {
                    'name': dictionary[prediction[0]],
                    'id': prediction[0],
                    'distance': prediction[1],
                    'coords': {
                        'x': str(faces[0][0]),
                        'y': str(faces[0][1]),
                        'width': str(faces[0][2]),
                        'height': str(faces[0][3])
                    }
                }
            }
        return result



ComputerVision().TrainModel("webcam")

"""

camera = cv2.VideoCapture(0)
ret = camera.set(3, 640)
ret = camera.set(4, 480)

count = 0

while True:
    ret, image = camera.read()

    faces = detect_faces(image)

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
