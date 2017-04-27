#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import cv2

#import rospy
#from std_msgs.msg import String

from EmeraldAI.Entities.PredictionObject import PredictionObject
from EmeraldAI.Logic.ComputerVision.ComputerVision import ComputerVision
from EmeraldAI.Config.Config import *


def RunCV():
    #pub = rospy.Publisher('to_brain', String, queue_size=10)
    #rospy.init_node('CV_node', anonymous=True)
    #rate = rospy.Rate(10) # 10hz

    camera = cv2.VideoCapture(Config().GetInt("ComputerVision", "CameraID"))
    camera.set(3, Config().GetInt("ComputerVision", "CameraWidth"))
    camera.set(4, Config().GetInt("ComputerVision", "CameraHeight"))

    cv = ComputerVision()

    #cv.TrainModel("Person")
    #exit()

    predictionObjectList = []
    # moodModel, moodDictionary = cv.LoadModel("Mood")
    # predictionObjectList.append(PredictionObject("mood", moodModel, moodDictionary, 500))
    personModel, personDictionary = cv.LoadModel("Person")
    predictionObjectList.append(PredictionObject("Person", personModel, personDictionary, 500))

    while True:
        ret, image = camera.read()

        predictionResult, thresholdReached, timeoutReached = cv.PredictMultipleStream(image, predictionObjectList)

        takeImage = True
        for predictorObject in predictionResult:
            if len(predictorObject.PredictionResult) > 0 and (thresholdReached or timeoutReached):
                if (predictorObject.Name is "Person"):
                    for key, face in predictorObject.PredictionResult.iteritems():
                        for name, distance in face.iteritems():
                            if (name != "Unknown"):
                                takeImage = False


                if (predictorObject.Name is "Mood"):
                    print "TODO"

        # todo
        if(takeImage):
            print "Take Image"
            cv.TakeFaceImage(image, "random")

        #if(thresholdReached or timeoutReached):
        #    print "Result: ", predictionResult
        # TODO - get best result and name
        # rospy.loginfo("CV|PERSON|{0}".format(data))
        # pub.publish("CV|PERSON|{0}".format(data))





if __name__ == "__main__":
    try:
        RunCV()
    except KeyboardInterrupt:
        print "End"

"""

visual = False
if len(sys.argv) > 1 and str(sys.argv[1]) == "visual":
    visual = True

def RunCV():
    pub = rospy.Publisher('to_brain', String, queue_size=10)
    rospy.init_node('CV_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    camera = cv2.VideoCapture(Config().GetInt("ComputerVision", "CameraID"))
    camera.set(3, Config().GetInt("ComputerVision", "CameraWidth"))
    camera.set(4, Config().GetInt("ComputerVision", "CameraHeight"))

    pred = Predictor()

    predictorObject = pred.GetPredictor(camera, Detector().DetectFaceFrontal)
    if predictorObject == None:
        print "Create Dataset"
        pred.CreateDataset()
        predictorObject = pred.GetPredictor(camera, Detector().DetectFaceFrontal)

    previousResult = None
    while True:
        rate.sleep()
        if visual:
            detectionResult = predictorObject.RunVisual()
        else:
            detectionResult = predictorObject.Run()
        detectionResult = pred.RemoveUnknownPredictions(detectionResult)

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

            bestCVMatch = pred.GetHighestResult(detectionResult)
            if bestCVMatch[0] != None and bestCVMatch[0] != "Unknown" and bestCVMatch[0] != "NotKnown":
                rospy.loginfo("CV|{0}".format(data))
                pub.publish("CV|{0}".format(data))
                print bestCVMatch[0]


            #previousResult = detectionResult.copy()


if __name__ == "__main__":
    try:
        RunCV()
    except KeyboardInterrupt:
        print "End"

"""
