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


def RunCV(camID, camType, surveillanceMode):
    pub = rospy.Publisher('to_brain', String, queue_size=10)
    rospy.init_node('CV_node', anonymous=True)
    rospy.Rate(10) # 10hz

    if(camID  < 0):
        camID = Config().GetInt("ComputerVision", "CameraID")
    if(camType == "STD"):
        camType = Config().Get("ComputerVision", "CameraType")
    if(not surveillanceMode):
        surveillanceMode = Config().GetBoolean("ComputerVision", "SurveillanceMode")

    cvInstanceType = "CV"
    if(surveillanceMode):
        cvInstanceType = "CVSURV"


    camera = cv2.VideoCapture(camID)
    camera.set(3, Config().GetInt("ComputerVision", "CameraWidth"))
    camera.set(4, Config().GetInt("ComputerVision", "CameraHeight"))

    cropBodyImage = Config().GetBoolean("ComputerVision", "CropBodyImage")
    intervalBetweenImages = Config().GetInt("ComputerVision", "IntervalBetweenImages")

    bodyDetectionInterval = Config().GetInt("ComputerVision", "BodyDetectionInterval")

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

    while not camera.isOpened():
        print "Waiting for camera"
        time.sleep(1)

    ret, image = camera.read()
    imageHeight, imageWidth = image.shape[:2]

    BodyDetectionTimestamp = time.time()

    while True:
        #rate.sleep()
        ret, image = camera.read()

        if(image == None):
            print "Can't read image"
            continue

        lumaThreshold = 50 # TODO to config
        if (cv.GetLuma(image) < lumaThreshold):
            bodyData = "{0}|DARKNESS|{1}".format(cvInstanceType, camType)
            #print bodyData
            rospy.loginfo(bodyData)
            pub.publish(bodyData)
            continue

        cv2.imshow("image", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        bodyDetectionTimeout = False
        if(BodyDetectionTimestamp <= (time.time()-bodyDetectionInterval)):
            bodyDetectionTimeout = True

        if(surveillanceMode or bodyDetectionTimeout):
            rawBodyData = cv.DetectBody(image)
            if (len(rawBodyData) > 0):
                bodyID = 1
                bodyDetectionTimeout = False
                BodyDetectionTimestamp = time.time()

                for (x, y, w, h) in rawBodyData:
                    centerX = (x + w/2)
                    centerY = (y + h/2)

                    if (centerX < imageWidth/3):
                        posX = "left"
                    elif (centerX > imageWidth/3*2):
                        posX = "right"
                    else:
                        posX = "center"

                    if (centerY < imageHeight/5):
                        posY = "top"
                    elif (centerY > imageHeight/5*4):
                        posY = "bottom"
                    else:
                        posY = "center"

                    bodyData = "{0}|BODY|{1}|{2}|{3}|{4}".format(cvInstanceType, camType, bodyID, posX, posY)
                    #print bodyData
                    rospy.loginfo(bodyData)
                    pub.publish(bodyData)

                    bodyID += 1

                cv.TakeImage(image, "Body", (rawBodyData if cropBodyImage else None))


        if(surveillanceMode or not bodyDetectionTimeout):
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

                            predictionData = "{0}|PERSON|{1}|{2}|{3}|{4}|{5}|{6}".format(cvInstanceType, camType, key, bestResult, bestResultPerson, thresholdReached, timeoutReached)


                        if (predictorObject.Name == "Mood"):
                            predictionData = "{0}|MOOD|{1}|{2}|{3}".format(cvInstanceType, camType, key, bestResult)


                        if (predictorObject.Name == "Gender"):
                            predictionData = "{0}|GENDER|{1}|{2}|{3}".format(cvInstanceType, camType, key, bestResult)

                        #print predictionData
                        rospy.loginfo(predictionData)
                        pub.publish(predictionData)

            if(takeImage and clockFace <= (time.time()-intervalBetweenImages) and cv.TakeImage(image, "Person", rawFaceData, grayscale=True)):
                clockFace = time.time()


if __name__ == "__main__":
    camID = -1
    camType = "STD"
    surveillanceMode = False
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if (arg.lower().startswith("-cam")):
                camID = int(arg.lower().replace("-cam", ""))
            if (arg.lower().startswith("-type")):
                camType = int(arg.lower().replace("-type", ""))
            if (arg.lower().startswith("-surveillance")):
                surveillanceMode = True

    if(Pid.HasPid("CV{0}".format(camID))):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("CV{0}".format(camID))

    try:
        EnsureModelUpdate()
        RunCV(camID, camType, surveillanceMode)
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("CV{0}".format(camID))
