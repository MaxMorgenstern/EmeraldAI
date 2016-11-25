#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import select
import cv2
from EmeraldAI.Logic.Modules import Global

class ComputerVision(object):

  __faceWidth  = 92
  __faceHeight = 112

  __haarFrontalFace = 'haarcascade_frontalface_alt2.xml'
  __haarProfileFace = 'haarcascade_profileface.xml'
  __haarEyes = 'haarcascade_eye.xml'
  __haarEyesGlasses = 'haarcascade_eye_tree_eyeglasses.xml'

  __haarScale = 1.3
  __haarMinNeighbors = 4
  __haarMinSize = (30, 30)

  def __init__(self):
    self.__imageDir = Global.EmeraldPath + "Data/ComputerVisionData/"
    self.__haarDir = Global.EmeraldPath + "Data/HaarCascades/"
    self.__cascadeFrontalFace = cv2.CascadeClassifier(self.__haarDir + self.__haarFrontalFace)
    self.__cascadeProfileFace = cv2.CascadeClassifier(self.__haarDir + self.__haarProfileFace)
    self.__cascadeEyes = cv2.CascadeClassifier(self.__haarDir + self.__haarEyes)
    self.__cascadeEyesGlasses = cv2.CascadeClassifier(self.__haarDir + self.__haarEyesGlasses)


  def GetTrainingImageDir(self):
    return self.__imageDir


  def DetectFaceInImage(self, image):
    faces = self.__cascadeFrontalFace.detectMultiScale(image,
          scaleFactor=self.__haarScale,
          minNeighbors=self.__haarMinNeighbors,
          minSize=self.__haarMinSize,
          flags=cv2.CASCADE_SCALE_IMAGE)
    if len(faces) == 1:
      return faces[0]

    profiles = self.__cascadeProfileFace.detectMultiScale(image,
          scaleFactor=self.__haarScale,
          minNeighbors=self.__haarMinNeighbors,
          minSize=self.__haarMinSize,
          flags=cv2.CASCADE_SCALE_IMAGE)
    if len(profiles) == 1:
      return profiles[0]

    return None


  def CropImage(self, image, x, y, w, h):
    cropHeight = int((self.__faceHeight / float(self.__faceWidth)) * w)
    midy = y + h/2
    y1 = max(0, midy-cropHeight/2)
    y2 = min(image.shape[0]-1, midy+cropHeight/2)
    return image[y1:y2, x:x+w]


  # TODO - sems not to work on windows
  def __checkEnterPressed(self):
    if select.select([sys.stdin,],[],[],0.0)[0]:
      input_char = sys.stdin.read(1)
      print(input_char)
      return input_char.lower() == "\n"
    return False


  def CapturePerson(self, camera, message='', onEnter=True, showCam=True, twoEyes=True):
    imageCaptured = False
    returnImage = None
    faces = []
    eyes = []
    glasses = []

    if (camera.isOpened() == 0):
      return None

    if(onEnter):
      print (message)
      print ("press 'enter' to capture image")

    while not imageCaptured:
      ret, image = camera.read()
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

      profiles = self.__cascadeProfileFace.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        )

      for (x, y, w, h) in profiles:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)

      faces = self.__cascadeFrontalFace.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        )

      for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]

        eyes = self.__cascadeEyes.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
          cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

        glasses = self.__cascadeEyesGlasses.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in glasses:
          cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,255),2)

      font = None
      if(self.is_cv2()):
        font = cv2.CV_AA
      if(self.is_cv3()):
      	font = cv2.LINE_AA

      if(len(message) > 0):
        cv2.putText(image, message,(25,25), cv2.FONT_HERSHEY_PLAIN, 0.5, (255,0,0), 2, font)

      if(showCam):
        cv2.imshow('Video', image)
        #cv2.moveWindow('Video',100,100)
        cv2.waitKey(10)

      if(onEnter):
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
        if self.__checkEnterPressed():
          if twoEyes and (len(eyes) == 2 or len(glasses) == 2) or not twoEyes and (len(eyes) <= 2 or len(glasses) <= 2):
            ret, image = camera.read()
            returnImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            imageCaptured = True
          else:
            print ("Unable to detect a proper face or too many faces detected: try again")

      else:
        if twoEyes and (len(eyes) == 2 or len(glasses) == 2) or not twoEyes and (len(eyes) <= 2 or len(glasses) <= 2):
          ret, image = camera.read()
          returnImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
          imageCaptured = True

    return returnImage


  def is_cv2(self):
    return self.check_opencv_version("2.")

  def is_cv3(self):
    return self.check_opencv_version("3.")

  def check_opencv_version(self, major):
    return cv2.__version__.startswith(major)
