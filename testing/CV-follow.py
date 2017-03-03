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
    ([17, 100, 100], [50, 200, 200]),
    ([17, 15, 100], [50, 56, 200])
]
# ([17, 15, 100], [50, 56, 200])

camera = cv2.VideoCapture(1)
#ret = camera.set(3, 640)
#ret = camera.set(4, 360)

while True:
    if (camera.isOpened() != 0):
        ret, image = camera.read()
        if image != None:
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #cv2.imshow('Video', image)
            #cv2.imshow('Gray', grayImage)
            globalMask = None
            for (lower, upper) in boundaries:
                # create NumPy arrays from the boundaries
                lower = np.array(lower, dtype = "uint8")
                upper = np.array(upper, dtype = "uint8")
             
                # find the colors within the specified boundaries and apply
                # the mask
                mask = cv2.inRange(image, lower, upper)
                #output = cv2.bitwise_and(image, image, mask = mask)
                if globalMask == None:
                    globalMask = mask
                else:
                    globalMask += mask
         
            output = cv2.bitwise_and(image, image, mask = globalMask)
                
            # show the images
            cv2.imshow("output", output)
            #cv2.imshow("mask", mask)
            #cv2.imshow("images", np.hstack([image, globalMask]))

            gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
            cv2.imshow("thresh", thresh)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()

