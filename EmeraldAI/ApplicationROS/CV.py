#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import cv2
import time

#import rospy
#from std_msgs.msg import String

from EmeraldAI.Entities.PredictionObject import PredictionObject
from EmeraldAI.Logic.ComputerVision.ComputerVision import ComputerVision
from EmeraldAI.Config.Config import *


def RunCV():
    #pub = rospy.Publisher('to_brain', String, queue_size=10)
    #rospy.init_node('CV_node', anonymous=True)
    #rospy.Rate(10) # 10hz

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
    predictionObjectList.append(PredictionObject("Person", personModel, personDictionary, 1500)) # last one distance

    clock = time.time()

    while True:
        ret, image = camera.read()

        clockTimeout = False
        if(clock <= (time.time()-1)):
            clockTimeout = True
            clock = time.time()

        cv2.imshow("image", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        bodyDetectionResult = cv.DetectBody(image)
        if (len(bodyDetectionResult) > 0):
            #print "Body Detection", len(bodyDetectionResult), bodyDetectionResult

            if(clockTimeout):
                cv.TakeImage(image, "Body", bodyDetectionResult)
            #rospy.loginfo("CV|BODY|{0}".format(len(bodyDetectionResult)))
            #pub.publish("CV|BODY|{0}".format(len(bodyDetectionResult)))


            # TODO - Test: only predict face if we have found an body, upper body or head and shoulders
            # TODO - move to config  so we can detect all the time or this way
            predictionResult, thresholdReached, timeoutReached = cv.PredictMultipleStream(image, predictionObjectList)

            takeImage = True
            for predictorObject in predictionResult:
                if len(predictorObject.PredictionResult) > 0 and (thresholdReached or timeoutReached):

                    if (predictorObject.Name is "Person"):
                        for key, face in predictorObject.PredictionResult.iteritems():
                            bestResult = predictorObject.GetBestPredictionResult(key, False)
                            bestResultPerson = predictorObject.GetBestPredictionResult(key, True)

                            if(bestResult[0] != "Unknown"):
                                takeImage = False

                            print ""
                            print "Face Detection", predictionResult, bestResult, bestResultPerson
                            print "Face Detection", bestResult, thresholdReached, timeoutReached
                            #rospy.loginfo("CV|PERSON|{0}|{1}|{2}|{3}|{4}".format(key, bestResult[0], bestResult[1], thresholdReached, timeoutReached))
                            #pub.publish("CV|PERSON|{0}|{1}|{2}|{3}|{4}".format(key, bestResult[0], bestResult[1], thresholdReached, timeoutReached))

                    if (predictorObject.Name is "Mood"):
                        print "TODO"

            if(takeImage and clockTimeout):
                cv.TakeFaceImage(image, "Person")





if __name__ == "__main__":
    try:
        RunCV()
    except KeyboardInterrupt:
        print "End"
