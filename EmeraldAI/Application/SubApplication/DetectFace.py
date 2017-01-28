#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.ComputerVision.Predictor import *
from EmeraldAI.Logic.ComputerVision.Detector import *
from EmeraldAI.Entities.User import User


from collections import Counter

def GetHighestResult(resultList):
    sortedList = sorted(resultList.items(),
                        key=operator.itemgetter(1), reverse=True)
    return sortedList[0]


def RunFaceDetection():
    # TODO - dynamic via config
    camera = cv2.VideoCapture(0)
    ret = camera.set(3, 640)
    ret = camera.set(4, 360)

    p = Predictor()
    # TODO - if not created create - or on regular base
    #p.CreateDataset()
    predictor = p.GetPredictor(camera, Detector().DetectFaceFrontal)

    previousResult = None

    while True:
        detectionResult = predictor.run()
        #detectionResult = predictor.runVisual()
        if(detectionResult != None and len(detectionResult)):
            # ToDo - check if this is a plausible way of doing it
            if previousResult != None:
                combinedResult = (Counter(previousResult) + Counter(detectionResult))
                print "Combined Result", combinedResult
                print "Combined Best Guess", GetHighestResult(combinedResult)

            print ""
            print "Current Result", detectionResult
            print "Current Best Guess",  GetHighestResult(detectionResult)
            print ""
            print "---"

            # TODO - get details of user + write to user class
            User().SetUserByCVTag(GetHighestResult(detectionResult)[0])


            previousResult = detectionResult.copy()


if __name__ == "__main__":
    RunFaceDetection()
