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
from EmeraldAI.Logic.ComputerVision.ModelMonitor import ModelMonitor


def EnsureModelUpdate():
    monitor = ModelMonitor()
    predictionModules = Config().GetList("ComputerVision", "Modules")

    for moduleName in predictionModules:
        if(monitor.CompareHash(moduleName, monitor.GetStoredHash(moduleName))):
            print "Model '{0}' up to date".format(moduleName)
            continue
        print "Rebuild Model '{0}'...".format(moduleName)
        monitor.Rebuild(moduleName)


def RunCV(camID):
    #pub = rospy.Publisher('to_brain', String, queue_size=10)
    #rospy.init_node('CV_node', anonymous=True)
    #rospy.Rate(10) # 10hz

    if(camID  < 0):
        camID = Config().GetInt("ComputerVision", "CameraID")

    camera = cv2.VideoCapture(camID)
    camera.set(3, Config().GetInt("ComputerVision", "CameraWidth"))
    camera.set(4, Config().GetInt("ComputerVision", "CameraHeight"))

    cv = ComputerVision()

    predictionObjectList = []

    predictionModules = Config().GetList("ComputerVision", "Modules")
    for moduleName in predictionModules:
        model, dictionary = cv.LoadModel(moduleName)
        if (model == None or dictionary == None):
            continue
        print "load", moduleName
        predictionObjectList.append(PredictionObject(moduleName, model, dictionary, 1500)) # last one distance

    clockFace = time.time()
    clockBody = time.time()

    while True:
        ret, image = camera.read()

        cv2.imshow("image", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        rawBodyData = cv.DetectBody(image)
        if (len(rawBodyData) > 0):
            #rospy.loginfo("CV|BODY|{0}".format(len(rawBodyData)))
            #pub.publish("CV|BODY|{0}".format(len(rawBodyData)))

            # TODO - move to config  so we can detect all the time or this way
            predictionResult, thresholdReached, timeoutReached, rawFaceData = cv.PredictMultipleStream(image, predictionObjectList, threshold=7500)

            takeImage = True
            for predictorObject in predictionResult:
                if len(predictorObject.PredictionResult) > 0 and (thresholdReached or timeoutReached):

                    if (predictorObject.Name == "Person"):
                        for key, face in predictorObject.PredictionResult.iteritems():
                            bestResult = predictorObject.GetBestPredictionResult(key, False)
                            bestResultPerson = predictorObject.GetBestPredictionResult(key, True)

                            if(bestResult[0] != "Unknown"):
                                takeImage = False

                            print "Face Detection", bestResult, bestResultPerson, thresholdReached, timeoutReached
                            #rospy.loginfo("CV|PERSON|{0}|{1}|{2}|{3}|{4}".format(key, bestResult[0], bestResult[1], thresholdReached, timeoutReached))
                            #pub.publish("CV|PERSON|{0}|{1}|{2}|{3}|{4}".format(key, bestResult[0], bestResult[1], thresholdReached, timeoutReached))

                    if (predictorObject.Name == "Mood"):
                        print "Mood: ", predictorObject.PredictionResult
                        #rospy.loginfo("CV|Mood|{0}|{1}|{2}|{3}|{4}".format("TODO"))
                        #pub.publish("CV|Mood|{0}|{1}|{2}|{3}|{4}".format("TODO"))


            if(takeImage and clockFace <= (time.time()-1) and cv.TakeImage(image, "Person", rawFaceData, grayscale=True)):
                clockFace = time.time()

            if(clockBody <= (time.time()-1) and cv.TakeImage(image, "Body", rawBodyData)):
                clockBody = time.time()



if __name__ == "__main__":
    camID = -1
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if (arg.lower().startswith("-cam")):
                camID = int(arg.lower().replace("-cam", ""))

    try:
        EnsureModelUpdate()
        RunCV(camID)
    except KeyboardInterrupt:
        print "End"
