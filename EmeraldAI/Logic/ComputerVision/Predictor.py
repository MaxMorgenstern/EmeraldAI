#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import os
import sys
import numpy as np

import operator
import time

from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Logic.ComputerVision.Detector import *

from EmeraldAI.Logic.External.facerec.model import PredictableModel
from EmeraldAI.Logic.External.facerec.feature import Fisherfaces
from EmeraldAI.Logic.External.facerec.distance import EuclideanDistance
from EmeraldAI.Logic.External.facerec.classifier import NearestNeighbor
from EmeraldAI.Logic.External.facerec.validation import KFoldCrossValidation
from EmeraldAI.Logic.External.facerec.serialization import save_model, load_model
from EmeraldAI.Logic.External.facerec.helper.common import *
from EmeraldAI.Logic.External.facerec.helper.video import *

# TODO - put variables into config - eg __probeTreshhold

class ExtendedPredictableModel(PredictableModel):

    def __init__(self, feature, classifier, image_size, subject_names):
        PredictableModel.__init__(self, feature=feature, classifier=classifier)
        self.image_size = image_size
        self.subject_names = subject_names


class Predictor(object):

    def __getImageSize(self, size=None):
        if(size == None):
            size = "100x100"
        return (int(size.split("x")[0]), int(size.split("x")[1]))

    def __getModel(self, image_size, subject_names):
        feature = Fisherfaces()
        classifier = NearestNeighbor(dist_metric=EuclideanDistance(), k=1)
        return ExtendedPredictableModel(feature=feature, classifier=classifier, image_size=image_size, subject_names=subject_names)

    def __readImages(self, path, size=None):
        c = 0
        X = []
        y = []
        folder_names = []
        for dirname, dirnames, filenames in os.walk(path):
            for subdirname in dirnames:
                folder_names.append(subdirname)
                subject_path = os.path.join(dirname, subdirname)
                for filename in os.listdir(subject_path):
                    if(not filename.startswith('.')):
                        try:
                            im = cv2.imread(os.path.join(
                                subject_path, filename), cv2.IMREAD_GRAYSCALE)
                            if (size is not None):
                                im = cv2.resize(im, size)
                            X.append(np.asarray(im, dtype=np.uint8))
                            y.append(c)
                        except IOError, (errno, strerror):
                            print "I/O error({0}): {1}".format(errno, strerror)
                        except:
                            print "Unexpected error:", sys.exc_info()[0]
                            raise
                c = c + 1
        return [X, y, folder_names]

    def __getModelName(self):
        datasetPath = Global.EmeraldPath + "Data" + os.sep + "ComputerVisionData" + os.sep
        modelName = datasetPath + "myModel.pkl"
        return modelName

    def CreateDataset(self):
        datasetPath = Global.EmeraldPath + "Data" + os.sep + "ComputerVisionData" + os.sep
        imageSize = self.__getImageSize()

        [images, labels, subject_names] = self.__readImages(
            datasetPath, imageSize)
        # Zip us a {label, name} dict from the given data:
        list_of_labels = list(xrange(max(labels) + 1))
        subject_dictionary = dict(zip(list_of_labels, subject_names))
        # Get the model we want to compute:
        model = self.__getModel(image_size=imageSize,
                                subject_names=subject_dictionary)

        print "CreateDataset..."
        # Compute the model:
        model.compute(images, labels)
        # And save the model, which uses Pythons pickle module:
        save_model(self.__getModelName(), model)

    def TestModel(self):
        print "numfolds"

    def LoadDataset(self):
        return load_model(self.__getModelName())

    def PredictPerson(self, camera, detectorFunction=None, model=None):
        predictorApp = self.GetPredictor(camera, detectorFunction, model)
        return predictorApp.run()

    def GetPredictor(self, camera, detectorFunction=None, model=None):
        if(model == None):
            model = self.LoadDataset()
        if not isinstance(model, ExtendedPredictableModel):
            print "[Error] The given model is not of type '%s'." % "ExtendedPredictableModel"
            return

        return PredictorApp(model, camera, detectorFunction)


class PredictorApp(object):

    def __init__(self, model, camera, detectorFunction=None):
        self.__model = model
        self.__detector = Detector()
        if(detectorFunction == None):
            detectorFunction = self.__detector.DetectFaceFrontal
        self.__detectorFunction = detectorFunction
        self.__cam = camera
        self.__maxDistance = 150
        self.__predicted = {}
        self.__timeout = 5
        self.__probeTreshhold = 50  # after 10 detections return

    def AddPrediction(self, key, distance):
        if(self.__predicted.has_key(key)):
            self.__predicted[key] += (self.__maxDistance - distance) / 10
        else:
            self.__predicted[key] = (self.__maxDistance - distance) / 10

    def run(self):
        self.__predicted = {}
        probeCount = 0
        timeout = time.time() + self.__timeout

        while True and time.time() <= timeout:
            ret, img = self.__cam.read()
            # Resize the frame to half the original size for speeding up the detection process:
            #img = cv2.resize(frame, (frame.shape[1]/2, frame.shape[0]/2), interpolation = cv2.INTER_CUBIC)

            profiles = self.__detectorFunction(img)
            for (x, y, w, h) in profiles:
                face = img.copy()
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = self.__detector.CropImage(face, x, y, w, h)

                face = cv2.resize(face, self.__model.image_size,
                                  interpolation=cv2.INTER_CUBIC)

                predInfo = self.__model.predict(face)
                distance = predInfo[1]['distances'][0]
                prediction = predInfo[0]

                if distance > self.__maxDistance:
                    self.AddPrediction(
                        "Unknown", distance - self.__maxDistance)
                else:
                    key = self.__model.subject_names[prediction]
                    self.AddPrediction(key, distance)
                probeCount += 1

            if(probeCount > self.__probeTreshhold):
                break

        return self.__predicted

    def runVisual(self):
        displayTick = 0
        probeCount = 0
        while True:
            ret, img = self.__cam.read()
            # Resize the frame to half the original size for speeding up the detection process:
            #img = cv2.resize(frame, (frame.shape[1]/2, frame.shape[0]/2), interpolation = cv2.INTER_CUBIC)
            imgout = img.copy()

            profiles = self.__detector.DetectFaceFrontal(img)
            for (x, y, w, h) in profiles:
                face = img.copy()
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = self.__detector.CropImage(face, x, y, w, h)

                face = cv2.resize(face, self.__model.image_size,
                                  interpolation=cv2.INTER_CUBIC)

                predInfo = self.__model.predict(face)
                distance = predInfo[1]['distances'][0]
                prediction = predInfo[0]

                if distance > self.__maxDistance:
                    cv2.rectangle(imgout, (x, y),
                                  (x + w, y + h), (0, 0, 255), 1)
                    cv2.putText(imgout, "Unknown - " + str(distance), (x - 10,
                                                                       y - 10), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 255), 1)
                    self.AddPrediction("Unknown", distance)
                else:
                    key = self.__model.subject_names[prediction]
                    cv2.rectangle(imgout, (x, y),
                                  (x + w, y + h), (0, 255, 0), 1)
                    cv2.putText(imgout, key + " - " + str(distance), (x - 10,
                                                                      y - 10), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0), 1)
                    self.AddPrediction(key, distance)
                probeCount += 1

            #imgout = cv2.resize(imgout, (imgout.shape[1]*2, imgout.shape[0]*2), interpolation = cv2.INTER_CUBIC)
            cv2.imshow('videofacerec', imgout)

            # space
            ch = cv2.waitKey(10)
            if ch == 32:
                self.__predicted.clear()
                print "prediction cleared"
                displayTick = 0
                probeCount = 0

            # Show image & exit on escape:
            if ch == 27:
                break

            if(len(self.__predicted) > 0 and probeCount > 5 and displayTick % 30 == 0):
                sortedList = sorted(self.__predicted.items(),
                                    key=operator.itemgetter(1), reverse=True)
                print sortedList
                print "Probe Count " + str(probeCount)
                if(probeCount > 20):
                    print "This is: " + sortedList[0][0]

            displayTick += 1
