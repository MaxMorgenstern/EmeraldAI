#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import cv2
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')
from EmeraldAI.Logic.ComputerVision.Trainer import *
from EmeraldAI.Logic.ComputerVision.Detector import *

myCV = Trainer()
myDect = Detector()

camera = cv2.VideoCapture(0)
ret = camera.set(3, 640)
ret = camera.set(4, 360)
#ret = camera.set(3,640)
#ret = camera.set(4,480)
print('This app will capture several images to learn your face.')
name = raw_input('Please enter your name: ')
print('Press Ctrl-C to quit.')

max_img_num = 0

# Create the directory for positive training images if it doesn't exist.
img_dir = myCV.GetTrainingImageDir() + name
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
else:
    for root, dirs, filenames in os.walk(img_dir):
        for f in filenames:
            tmp_num = re.findall('\d+|$', f)[0]
            if(tmp_num > max_img_num):
                max_img_num = tmp_num


def img_message(img_num):
    switcher = {
        0: "normal face",
        1: "smile",
        2: "sad face",
        3: "suprised",
        4: "look slightly to the right",
        5: "look slightly to the left",
        6: "look slightly up",
        7: "look slightly down",
        8: "lighting from the left",
        9: "lighting from the right",
        10: "eyes closed"
    }
    return switcher.get(img_num, "nothing")


def img_name(img_num):
    switcher = {
        0: "normal",
        1: "happy",
        2: "sad",
        3: "suprised",
        4: "looking_right",
        5: "looking_left",
        6: "looking_up",
        7: "looking_down",
        8: "left_light",
        9: "right_light",
        10: "eyes_closed"
    }
    return switcher.get(img_num, "nothing")

img_num = max_img_num

"""
while img_num < 11:
  # Show the capture window
  image = myCV.CapturePerson(camera, img_message(img_num))

  # Get coordinates of single face in captured image.
  result = myCV.DetectFaceInImage(image)

  if result is None:
    print ('Could not detect single face!')
    continue

  x, y, w, h = result
  # Crop image as close as possible to desired face aspect ratio.
  # Might be smaller if face is near edge of image.
  img_crop = myCV.CropImage(image, x, y, w, h)
  # Save image to file.
  filename = os.path.join(img_dir, '%02d_%s_%s.pgm' % (img_num, name, img_name(img_num)))
  cv2.imwrite(filename, img_crop)
  print ('Found face and wrote training image' + filename)
  img_num += 1

# No Enter 2 Eyes
while img_num < 25:
  image = myCV.CapturePerson(camera, '', False, True, True)

  # Get coordinates of single face in captured image.
  result = myCV.DetectFaceInImage(image)
  if result is None:
    continue

  x, y, w, h = result
  # Crop image as close as possible to desired face aspect ratio.
  # Might be smaller if face is near edge of image.
  img_crop = myCV.CropImage(image, x, y, w, h)
  # Save image to file.
  filename = os.path.join(img_dir, '%02d_%s_auto.pgm' % (img_num, name))
  cv2.imwrite(filename, img_crop)
  print ('Found face and wrote training image' + filename)
  img_num += 1
"""
# No Enter No Eyes
# while img_num < 50:

while True:
    image = myCV.CaptureFace(camera, '', False, True, False)
    if(image != None):
        cv2.imshow('Output', image)

    # Get coordinates of single face in captured image.
    #result = myDect.DetectSingleFace(image)
    # if result is None:
    #  continue
    # print "okay"
    #x, y, w, h = result
    # Crop image as close as possible to desired face aspect ratio.
    # Might be smaller if face is near edge of image.
    #img_crop = myCV.CropImage(image, x, y, w, h)
    # Save image to file.
    if(image != None):
        filename = os.path.join(img_dir, '%02d_%s_auto.pgm' % (img_num, name))
        cv2.imwrite(filename, image)
        print('Found face and wrote training image' + filename)
        img_num += 1

cv2.destroyAllWindows()
