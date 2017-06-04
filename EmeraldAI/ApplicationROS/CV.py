#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import cv2
import time

import rospy
from std_msgs.msg import String

from EmeraldAI.Entities.PredictionObject import PredictionObject
from EmeraldAI.Logic.ComputerVision.ComputerVision import ComputerVision
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.ComputerVision.ModelMonitor import ModelMonitor
from EmeraldAI.Logic.Modules import Pid


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
    rospy.init_node('CV_node', anonymous=True)
    rospy.Rate(10) # 10hz

    if(camID  < 0):
        camID = Config().GetInt("ComputerVision", "CameraID")

    camera = cv2.VideoCapture(camID)
    camera.set(3, Config().GetInt("ComputerVision", "CameraWidth"))
    camera.set(4, Config().GetInt("ComputerVision", "CameraHeight"))

    cropBodyImage = Config().GetBoolean("ComputerVision", "CropBodyImage")
    intervalBetweenImages = Config().GetInt("ComputerVision", "IntervalBetweenImages")

    cv = ComputerVision()

    predictionObjectList = []

    predictionModules = Config().GetList("ComputerVision", "Modules")
    for moduleName in predictionModules:
        model, dictionary = cv.LoadModel(moduleName)
        if (model == None or dictionary == None):
            continue
        print "load", moduleName
        predictionObjectList.append(PredictionObject(moduleName, model, dictionary))

    clockFace = time.time()
    clockBody = time.time()

    while not camera.isOpened():
        print "Waiting for camera"
        time.sleep(1)

    ret, image = camera.read()
    imageHeight, imageWidth = image.shape[:2]

    while True:
        #rate.sleep()
        ret, image = camera.read()

        if(image == None):
            print "Can't read image"
            continue

        lumaThreshold = 20 # to config
        if (cv.GetLuma(image) < lumaThreshold):
            bodyData = "CV|DARKNESS|{0}".format(camID)
            #print bodyData
            rospy.loginfo(bodyData)
            pub.publish(bodyData)
            continue

        cv2.imshow("image", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        rawBodyData = cv.DetectBody(image)
        if (len(rawBodyData) > 0):
            bodyID = 1

            for (x, y, w, h) in rawBodyData:
                centerX = (x + w/2)
                centerY = (y + h/2)

                if (centerX < imageWidth/3):
                    posX = "left"
                if (centerX > imageWidth/3*2):
                    posX = "right"
                else:
                    posX = "center"

                if (centerY < imageHeight/5):
                    posY = "top"
                if (centerY > imageHeight/5*4):
                    posY = "bottom"
                else:
                    posY = "center"

                bodyData = "CV|BODY|{0}|{1}|{2}|{3}".format(camID, bodyID, posX, posY)
                #print bodyData
                rospy.loginfo(bodyData)
                pub.publish(bodyData)

                bodyID += 1

            predictionResult, thresholdReached, timeoutReached, rawFaceData = cv.PredictStream(image, predictionObjectList, threshold=7500)

            takeImage = True
            for predictorObject in predictionResult:
                if len(predictorObject.PredictionResult) > 0 and (thresholdReached or timeoutReached):

                     for key, face in predictorObject.PredictionResult.iteritems():
                        bestResult = predictorObject.GetBestPredictionResult(key, False)

                        if (predictorObject.Name == "Person"):
                            bestResultPerson = predictorObject.GetBestPredictionResult(key, True)

                            if(bestResult[0] != "Unknown"):
                                takeImage = False

                            predictionData = "CV|PERSON|{0}|{1}|{2}|{3}|{4}|{5}".format(camID, key, bestResult, bestResultPerson, thresholdReached, timeoutReached)


                        if (predictorObject.Name == "Mood"):
                            predictionData = "CV|MOOD|{0}|{1}|{2}".format(camID, key, bestResult)


                        if (predictorObject.Name == "Gender"):
                            predictionData = "CV|GENDER|{0}|{1}|{2}".format(camID, key, bestResult)

                        #print predictionData
                        rospy.loginfo(predictionData)
                        pub.publish(predictionData)

            if(takeImage and clockFace <= (time.time()-intervalBetweenImages) and cv.TakeImage(image, "Person", rawFaceData, grayscale=True)):
                clockFace = time.time()

            passedBodyData = rawBodyData if cropBodyImage else None
            if(clockBody <= (time.time()-intervalBetweenImages) and cv.TakeImage(image, "Body", passedBodyData)):
                clockBody = time.time()



if __name__ == "__main__":
    camID = -1
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if (arg.lower().startswith("-cam")):
                camID = int(arg.lower().replace("-cam", ""))

    if(Pid.HasPid("CV{0}".format(camID))):
        sys.exit()
    Pid.Create("CV{0}".format(camID))

    try:
        EnsureModelUpdate()
        RunCV(camID)
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("CV{0}".format(camID))
