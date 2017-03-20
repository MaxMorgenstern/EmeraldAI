#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import cv2
import re
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')
#from EmeraldAI.Logic.ComputerVision.Trainer import *
#from EmeraldAI.Logic.ComputerVision.Detector import *

#myCV = Trainer()
#myDect = Detector()

boundaries = [
    ([0, 100, 100], [15, 255, 255]),
    ([350, 100, 100], [360, 255, 255]),
    ([0, 100, 50], [15, 255, 255]),
    ([350, 100, 50], [360, 255, 255]),
    ([0, 50, 50], [15, 255, 255]),
    ([350, 50, 50], [360, 255, 255])
]
# yellow - RGB: 
# 127 143 71
# 103 114 47
# 107 110 45
# 121 121 64
# 107 113 61
# 112 112 58
# hell
# 239 255 134
# 215 237 100
# 143 169 69

# red - RGB
# 90 15 29
# 70 10 14
# 233 90 117
# 135 82 41
# 227 63 25
# 


camera = cv2.VideoCapture(1)
#ret = camera.set(3, 640)
#ret = camera.set(4, 360)

while True:
    if (camera.isOpened() != 0):
        ret, image = camera.read()
        if image != None:
            hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            #cv2.imshow('Video', image)
            #cv2.imshow('Gray', grayImage)
            globalMask = None
            for (lower, upper) in boundaries:
                # create NumPy arrays from the boundaries
                lower = np.array(lower, dtype = "uint8")
                upper = np.array(upper, dtype = "uint8")
             
                # find the colors within the specified boundaries and apply
                # the mask
                mask = cv2.inRange(hsvImage, lower, upper)
                #output = cv2.bitwise_and(image, image, mask = mask)
                if globalMask == None:
                    globalMask = mask
                else:
                    globalMask += mask
         

            output = cv2.bitwise_and(image, image, mask = globalMask)
                
            # show the images
            cv2.imshow("output", output)
            #cv2.imshow("mask", mask)
            cv2.imshow("image", image)
            #cv2.imshow("images", np.hstack([image, globalMask]))

            #gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
            #blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            #thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
            #cv2.imshow("thresh", thresh)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()

