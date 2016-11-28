#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import os
import sys
import numpy as np

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


class ExtendedPredictableModel(PredictableModel):
  def __init__(self, feature, classifier, image_size, subject_names):
    PredictableModel.__init__(self, feature=feature, classifier=classifier)
    self.image_size = image_size
    self.subject_names = subject_names

class Predictor(object):

  def __getImageSize(self, size=None):
    if(size==None):
      size="100x100"
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
                        im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                        if (size is not None):
                          im = cv2.resize(im, size)
                        X.append(np.asarray(im, dtype=np.uint8))
                        y.append(c)
                    except IOError, (errno, strerror):
                        print "I/O error({0}): {1}".format(errno, strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise
            c = c+1
    return [X,y,folder_names]

  def __getModelName(self):
    datasetPath = Global.EmeraldPath + "Data/ComputerVisionData/"
    modelName = datasetPath + "myModel.pkl"
    return modelName

  def CreateDataset(self):
    datasetPath = Global.EmeraldPath + "Data/ComputerVisionData/"
    imageSize = self.__getImageSize()

    [images, labels, subject_names] = self.__readImages(datasetPath, imageSize)
    # Zip us a {label, name} dict from the given data:
    list_of_labels = list(xrange(max(labels)+1))
    subject_dictionary = dict(zip(list_of_labels, subject_names))
    # Get the model we want to compute:
    model = self.__getModel(image_size=imageSize, subject_names=subject_dictionary)

    print "CreateDataset..."
    # Compute the model:
    model.compute(images, labels)
    # And save the model, which uses Pythons pickle module:
    save_model(self.__getModelName(), model)

  def TestModel(self):
    print "numfolds"

  def LoadDataset(self):
    return load_model(self.__getModelName())

  def PredictPerson(self, camera, model=None):
    if(model==None):
        model = self.LoadDataset()
    if not isinstance(model, ExtendedPredictableModel):
        print "[Error] The given model is not of type '%s'." % "ExtendedPredictableModel"
        return
    PredictorApp(model, camera, "").run()





class PredictorApp(object):
  def __init__(self, model, camera, cascade_filename):
    self.model = model
    self.__detector = Detector()
    #self.detector = CascadedDetector(cascade_fn=cascade_filename, minNeighbors=5, scaleFactor=1.1)
    #self.detectorUpperBody = CascadedDetector(cascade_fn="haarcascade_upperbody.xml", minNeighbors=5, scaleFactor=1.1)
    self.cam = camera

  def run(self):
    while True:
      ret, frame = self.cam.read()
      # Resize the frame to half the original size for speeding up the detection process:
      img = cv2.resize(frame, (frame.shape[1]/2, frame.shape[0]/2), interpolation = cv2.INTER_CUBIC)
      imgout = img.copy()

      #for i,r in enumerate(self.detectorUpperBody.detect(img)):
      #  x,y,w,h = r
      #  cv2.rectangle(imgout, (x, y), (x+w, y+h), (0, 255, 255), 2)

      """
      for i,r in enumerate(self.__detector.DetectFaceFrontal(img)):
        #for i,r in enumerate(self.detector.detect(img)):
        x0,y0,x1,y1 = r
        # (1) Get face, (2) Convert to grayscale & (3) resize to image_size:
        face = img[y0:y1, x0:x1]
        face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
        face = cv2.resize(face, self.model.image_size, interpolation = cv2.INTER_CUBIC)
        # Get a prediction from the model:
        predInfo = self.model.predict(face)
        distance = predInfo[1]['distances'][0]
        prediction = predInfo[0]
        # Draw the face area in image:
        cv2.rectangle(imgout, (x0,y0),(x1,y1),(0,255,0),2)
        # Draw the predicted name (folder name...):

        if distance > 200:
          draw_str(imgout, (x0-20,y0-20), "Unknown - " + str(distance))
        else:
          draw_str(imgout, (x0-20,y0-20), self.model.subject_names[prediction] + " - " + str(distance))
      """
      profiles = self.__detector.DetectFaceFrontal(img)
      for (x, y, w, h) in profiles:
        cv2.rectangle(imgout, (x, y), (x+w, y+h), (0, 255, 255), 2)


      cv2.imshow('videofacerec', imgout)

      # Show image & exit on escape:
      ch = cv2.waitKey(10)
      if ch == 27:
        break
