#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import os
import sys
import numpy as np

from EmeraldAI.Logic.Modules import Global

from EmeraldAI.Logic.External.facerec.model import PredictableModel
from EmeraldAI.Logic.External.facerec.feature import Fisherfaces
from EmeraldAI.Logic.External.facerec.distance import EuclideanDistance
from EmeraldAI.Logic.External.facerec.classifier import NearestNeighbor
from EmeraldAI.Logic.External.facerec.validation import KFoldCrossValidation
from EmeraldAI.Logic.External.facerec.serialization import save_model, load_model

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

  def __readImages(self, path):
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
                        print os.path.join(subject_path, filename)
                        X.append(np.asarray(im, dtype=np.uint8))
                        y.append(c)
                    except IOError, (errno, strerror):
                        print "I/O error({0}): {1}".format(errno, strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise
            c = c+1
    return [X,y,folder_names]


  def CreateDataset(self):
    datasetPath = Global.EmeraldPath + "Data/ComputerVisionData/"
    modelName = datasetPath + "myModel.pkl"

    [images, labels, subject_names] = self.__readImages(datasetPath)
    # Zip us a {label, name} dict from the given data:
    list_of_labels = list(xrange(max(labels)+1))
    subject_dictionary = dict(zip(list_of_labels, subject_names))
    # Get the model we want to compute:
    model = self.__getModel(image_size=self.__getImageSize(), subject_names=subject_dictionary)

    # Compute the model:
    model.compute(images, labels)
    # And save the model, which uses Pythons pickle module:
    save_model(modelName, model)

  """
Traceback (most recent call last):
  File "testing/testCV-detection.py", line 14, in <module>
    p.CreateDataset()
  File "/Users/maximilianporzelt/Google Drive/EmeraldAI/EmeraldAI/Logic/ComputerVision/Predictor.py", line 72, in CreateDataset
    model.compute(images, labels)
  File "/Users/maximilianporzelt/Google Drive/EmeraldAI/EmeraldAI/Logic/External/facerec/model.py", line 21, in compute
    features = self.feature.compute(X,y)
  File "/Users/maximilianporzelt/Google Drive/EmeraldAI/EmeraldAI/Logic/External/facerec/feature.py", line 193, in compute
    model.compute(X,y)
  File "/Users/maximilianporzelt/Google Drive/EmeraldAI/EmeraldAI/Logic/External/facerec/operators.py", line 41, in compute
    X = self.model1.compute(X,y)
  File "/Users/maximilianporzelt/Google Drive/EmeraldAI/EmeraldAI/Logic/External/facerec/feature.py", line 54, in compute
    XC = asColumnMatrix(X)
  File "/Users/maximilianporzelt/Google Drive/EmeraldAI/EmeraldAI/Logic/External/facerec/util.py", line 52, in asColumnMatrix
    mat = np.append(mat, col.reshape(-1,1), axis=1) # same as hstack
  File "/usr/local/lib/python2.7/site-packages/numpy/lib/function_base.py", line 4586, in append
    return concatenate((arr, values), axis=axis)
ValueError: all the input array dimensions except for the concatenation axis must match exactly
  """

  def TestModel():
    print "numfolds"

  def LoadDataset():
    print ""

  def PredictPerson():
    print ""
