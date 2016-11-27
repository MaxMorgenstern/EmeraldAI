#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import select
import cv2
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Logic.ComputerVision.Detector import *

class Trainer(object):

  __faceWidth  = 92
  __faceHeight = 112

  def __init__(self):
    self.__imageDir = Global.EmeraldPath + "Data/ComputerVisionData/"
    self.__detector = Detector()


  def GetTrainingImageDir(self):
    return self.__imageDir


  def CropImage(self, image, x, y, w, h):
    cropHeight = int((self.__faceHeight / float(self.__faceWidth)) * w)
    midy = y + h/2
    y1 = max(0, midy-cropHeight/2)
    y2 = min(image.shape[0]-1, midy+cropHeight/2)
    return image[y1:y2, x:x+w]


  def __checkEnterPressed(self):
    if(Global.OS == 'windows'):
      return self.__checkEnterPressedWindows()
    else:
      return self.__checkEnterPressedOSXLinux()

  def __checkEnterPressedOSXLinux(self):
    if select.select([sys.stdin,],[],[],0.0)[0]:
      input_char = sys.stdin.read(1)
      print(input_char)
      return input_char.lower() == "\n"
    return False

  def __checkEnterPressedWindows(self):
    import msvcrt
    if msvcrt.kbhit():
      key = msvcrt.getch()
      print key
      return (key == "\r")
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
      grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

      profiles = self.__detector.DetectFaceProfile(grayImage)
      for (x, y, w, h) in profiles:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)

      faces = self.__detector.DetectFaceFrontal(grayImage)
      for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        roiGray = grayImage[y:y+h, x:x+w]
        roiColor = image[y:y+h, x:x+w]

        eyes = self.__detector.DetectEyes(roiGray)
        for (ex,ey,ew,eh) in eyes:
          cv2.rectangle(roiColor,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

        glasses = self.__detector.DetectEyesGlasses(roiGray)
        for (ex,ey,ew,eh) in glasses:
          cv2.rectangle(roiColor,(ex,ey),(ex+ew,ey+eh),(255,0,255),2)

      if(len(message) > 0):
        font = None
        if(self.is_cv2()):
          font = cv2.CV_AA
        if(self.is_cv3()):
          font = cv2.LINE_AA
        cv2.putText(image, message,(25,25), cv2.FONT_HERSHEY_PLAIN, 0.5, (255,0,0), 2, font)

      if(showCam):
        cv2.imshow('Video', image)
        cv2.waitKey(10)

      if(onEnter):
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
        if (self.__checkEnterPressed()):
          if (twoEyes and (len(eyes) == 2 or len(glasses) == 2)):
            imageCaptured = True

          elif (not twoEyes and (len(eyes) <= 2 or len(glasses) <= 2)):
          	imageCaptured = True

      elif (twoEyes and (len(eyes) == 2 or len(glasses) == 2)):
          imageCaptured = True

      else:
      	imageCaptured = True

    ret, image = camera.read()
    returnImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return returnImage


  def is_cv2(self):
    return self.check_opencv_version("2.")

  def is_cv3(self):
    return self.check_opencv_version("3.")

  def check_opencv_version(self, major):
    return cv2.__version__.startswith(major)


# TODO
# return Cropped image
