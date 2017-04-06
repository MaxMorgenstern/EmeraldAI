#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import cv2
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Config.Config import *
from EmeraldAI.Entities.User import User
from EmeraldAI.Entities.PredictionObject import PredictionObject
from EmeraldAI.Logic.ComputerVision.ComputerVision import ComputerVision

"""
import sys
visual = False
if len(sys.argv) > 1 and str(sys.argv[1]) == "visual":
    visual = True
"""
#from collections import Counter

"""
def GetHighestResult(resultList):
    sortedList = sorted(resultList.items(), key=operator.itemgetter(1), reverse=True)
    return sortedList[0]
"""

def RunFaceDetection():
    camera = cv2.VideoCapture(Config().GetInt("ComputerVision", "CameraID"))

    ret = camera.set(3, Config().GetInt("ComputerVision", "CameraWidth"))
    ret = camera.set(4, Config().GetInt("ComputerVision", "CameraHeight"))


    moodModel, moodDictionary = ComputerVision().LoadModel("mood")
    personModel, personDictionary = ComputerVision().LoadModel("person")

    predictionObjectList = []
    predictionObjectList.append(PredictionObject("mood", moodModel, moodDictionary, 500)) # 500 == max distance
    predictionObjectList.append(PredictionObject("person", personModel, personDictionary, 500))

    while True:
        ret, image = camera.read()

        result, thresholdReached, timeoutReached = ComputerVision().PredictMultipleStream(image, predictionObjectList)

        for predictorObject in result:
            print predictorObject.PredictionResult


    """
    pred = Predictor()

    predictorObject = pred.GetPredictor(camera, Detector().DetectFaceFrontal)
    if predictorObject == None:
        pred.CreateDataset()
        predictorObject = pred.GetPredictor(camera, Detector().DetectFaceFrontal)

    previousResult = None
    while True:
        print "RunFaceDetection() while..."
        if visual:
            detectionResult = predictorObject.RunVisual()
        else:
            detectionResult = predictorObject.Run()
        if(detectionResult != None and len(detectionResult)):

            # ToDo - check if this is a plausible way of doing it
#            if previousResult != None:
#                combinedResult = (Counter(previousResult) + Counter(detectionResult))
#                print "Combined Result", combinedResult
#                print "Combined Best Guess", GetHighestResult(combinedResult)
#
#            print ""
#            print "Current Result", detectionResult
#            print "Current Best Guess",  GetHighestResult(detectionResult)
#            print ""
#            print "---"


            bestCVMatch = GetHighestResult(detectionResult)
            if bestCVMatch[0] != None and bestCVMatch[0] != "Unknown" and bestCVMatch[0] != "NotKnown":
                print "set CV Tag", bestCVMatch
                passedUser.SetUserByCVTag(bestCVMatch[0], False)


            #previousResult = detectionResult.copy()
    """

if __name__ == "__main__":
    try:
        RunFaceDetection()
    except KeyboardInterrupt:
        print "End"
