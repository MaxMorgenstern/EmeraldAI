#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import select
import cv2
from EmeraldAI.Logic.Modules import Global

class Detector(object):

  __haarFaceFrontal = 'haarcascade_frontalface_alt2.xml'
  __haarFaceProfile = 'haarcascade_profileface.xml'

  __haarBodyUpper = 'haarcascade_upperbody.xml'
  __haarBodyLower = 'haarcascade_lowerbody.xml'
  __haarBodyFull = 'haarcascade_fullbody.xml'

  __haarEyes = 'haarcascade_eye.xml'
  __haarEyesGlasses = 'haarcascade_eye_tree_eyeglasses.xml'

  __haarScale = 1.1
  __haarMinNeighbors = 4
  __haarMinSize = (30, 30)

  def __init__(self):
    self.__haarDir = Global.EmeraldPath + "Data/HaarCascades/"
    self.__cascadeFaceFrontal = cv2.CascadeClassifier(self.__haarDir + self.__haarFaceFrontal)
    self.__cascadeFaceProfile = cv2.CascadeClassifier(self.__haarDir + self.__haarFaceProfile)

    self.__cascadeBodyUpper = cv2.CascadeClassifier(self.__haarDir + self.__haarBodyUpper)
    self.__cascadeBodyLower = cv2.CascadeClassifier(self.__haarDir + self.__haarBodyLower)
    self.__cascadeBodyFull = cv2.CascadeClassifier(self.__haarDir + self.__haarBodyFull)

    self.__cascadeEyes = cv2.CascadeClassifier(self.__haarDir + self.__haarEyes)
    self.__cascadeEyesGlasses = cv2.CascadeClassifier(self.__haarDir + self.__haarEyesGlasses)


  def DetectSingleFace(self, image):
    faces = self.DetectFaceFrontal(image)
    if len(faces) == 1:
      return faces[0]

    profiles = self.DetectFaceProfile(image)
    if len(profiles) == 1:
      return profiles[0]

    return None

  def DetectFaceFrontal(self, image, haarScale=None):
    if(haarScale==None):
      haarScale = self.__haarScale
    return self.__detect(image, haarScale, self.__cascadeFaceFrontal)

  def DetectFaceProfile(self, image, haarScale=None):
    if(haarScale==None):
      haarScale = self.__haarScale
    return self.__detect(image, haarScale, self.__cascadeFaceProfile)

  def DetectBodyUpper(self, image, haarScale=None):
    if(haarScale==None):
      haarScale = self.__haarScale
    return self.__detect(image, haarScale, self.__cascadeBodyUpper)

  def DetectBodyLower(self, image, haarScale=None):
    if(haarScale==None):
      haarScale = self.__haarScale
    return self.__detect(image, haarScale, self.__cascadeBodyLower)

  def DetectBodyFull(self, image, haarScale=None):
    if(haarScale==None):
      haarScale = self.__haarScale
    return self.__detect(image, haarScale, self.__cascadeBodyFull)

  def DetectEyes(self, image):
    return self.__cascadeEyes.detectMultiScale(image)

  def DetectEyesGlasses(self, image):
    return self.__cascadeEyesGlasses.detectMultiScale(image)


  def __detect(self, image, haarScale, cascade):
    return cascade.detectMultiScale(image,
      scaleFactor=haarScale,
      minNeighbors=self.__haarMinNeighbors,
      minSize=self.__haarMinSize,
      flags=cv2.CASCADE_SCALE_IMAGE)
