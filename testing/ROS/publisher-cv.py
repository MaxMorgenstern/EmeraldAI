#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
import cv2
import re
import numpy as np
from enum import Enum
import rospy
from std_msgs.msg import String
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')


class RevertRotateState(Enum):
    Revert = 0
    RotateLeft = 1
    RotateRight = 2
    Done = 3


def GetCenterOffset(camera, crop, boundaries, contourThreshold, visual = False):

    ret, image = camera.read()
    pointsToMove = None

    if image != None:
        height, width = image.shape[:2]

        if crop:
            image = image[height/2:height, 0:width].copy()
        # Crop from x, y, w, h -> 100, 200, 300, 400
        # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

        globalMask = None
        for (lower, upper) in _boundaries:
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

        output = cv2.bitwise_and(image, image, mask = cv2.GaussianBlur(globalMask, (5, 5), 0))
        thresh = cv2.threshold(output, 60, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
        cont = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contSize = 0
        contObject = None
        for c in cont[0]:
            cS = cv2.contourArea(c)
            M = cv2.moments(c)
            if M["m00"] != 0 and cS > contSize:
                contSize = cS
                contObject = c

        if contSize >= contourThreshold and contObject != None:
            # compute the center of the contour
            M = cv2.moments(contObject)

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            pointsToMove = (width/2 - cX)

            if visual:
                cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(image, str(cX) + " - " + str(contSize), (cX - 10, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(image, str(pointsToMove), (int(width/2), 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        if visual:
            cv2.imshow("image", image)

    return pointsToMove

def PublishToArduino(publisher, motor1, motor2, rate):
    val = '{}|{}'.format(motor1, motor2)
    pub.publish(val)
    rate.sleep()

def ResetRevertAndRotate():
    _revertAndRotate = False
    _revertAndRotateState = None
    _revertAndRotateProcess = 0
    _revertAndRotateIteration = 1

def RevertAndRotate():
    stepsPerProcess = 10

    if _revertAndRotateState == None:
        _revertAndRotateState = RevertRotateState.Revert

    if _revertAndRotateState == RevertRotateState.Revert:
        PublishToArduino(_publisher, -50, -50, _rate)
        _revertAndRotateProcess += 1

        if _revertAndRotateProcess * _revertAndRotateIteration > stepsPerProcess:
            _revertAndRotateState = RevertRotateState.RotateLeft
            _revertAndRotateProcess = 0


    if _revertAndRotateState == RevertRotateState.RotateLeft:
        PublishToArduino(_publisher, -50, 50, _rate)
        _revertAndRotateProcess += 1

        if _revertAndRotateProcess * _revertAndRotateIteration > stepsPerProcess:
            _revertAndRotateState = RevertRotateState.RotateRight
            _revertAndRotateProcess = 0

    if _revertAndRotateState == RevertRotateState.RotateRight:
        PublishToArduino(_publisher, 50, -50, _rate)
        _revertAndRotateProcess += 1

        if _revertAndRotateProcess * _revertAndRotateIteration > stepsPerProcess:
            _revertAndRotateState = RevertRotateState.Revert
            _revertAndRotateProcess = 0
            _revertAndRotateIteration += 1


    if _revertAndRotateState == RevertRotateState.Done:
        ResetRevertAndRotate()


##########

_boundaries = [
    ([17, 15, 100], [50, 56, 200]),
    ([0, 0, 40], [30, 20, 90]),
    ([35, 75, 125], [45, 90, 240]),
    ([60, 50, 120], [100, 75, 145])
]

_cameraID = 0
_cameraWidth = 320
_cameraHeigt = 240
_contourThreshold = 150
_camResize = True

_leftThreshold = 10
_rightThreshold = -10

_revertAndRotate = False # revert and rotate triggered
_revertAndRotateState = None # State
_revertAndRotateProcess = 0 # Process in percent
_revertAndRotateIteration = 1 # number of iterations since lost of track


_publisher = rospy.Publisher('to_arduino', String, queue_size=10)
rospy.init_node('cv_sender', anonymous=True)
_rate = rospy.Rate(10) # 10hz

cam = cv2.VideoCapture(_cameraID)

if _camResize:
    ret = cam.set(3, _cameraWidth)
    ret = cam.set(4, _cameraHeigt)



while True:
    if _revertAndRotate:
        RevertAndRotate()

    elif (cam.isOpened() != 0):
        offset = GetCenterOffset(cam, False, _boundaries, _contourThreshold, True)

        if offset == None:
            print "we lost track - drive a bit back + turn around"
            _revertAndRotate = True


        elif offset >= _leftThreshold:
            correction = (100 / abs(_cameraWidth/2) * abs(offset))
            PublishToArduino(_publisher, 100, correction, _rate)
            print "we drive to the left - need to correct to right", correction
            ResetRevertAndRotate()


        elif offset <= _rightThreshold:
            correction = (100 / abs(_cameraWidth/2) * abs(offset))
            PublishToArduino(_publisher, correction, 100, _rate)
            print "we drive to the right - need to correct to left", correction
            ResetRevertAndRotate()


        elif offset > _rightThreshold and offset < _leftThreshold:
            PublishToArduino(_publisher, 100, 100, _rate)
            print "in tollerance drive straight"
            ResetRevertAndRotate()

        else:
            print "ERROR!"
            _revertAndRotate = True


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()


