#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import cv2
import time

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

    showCameraImage = Config().GetBoolean("ComputerVision", "ShowCameraImage")

    predictionThreshold = Config().GetInt("ComputerVision.Prediction", "PredictionThreshold")

    unknownUserTag = Config().Get("ComputerVision", "UnknownUserTag")

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

    bodyDetectionTimestamp = time.time()

    while True:
        #rate.sleep()
        ret, image = camera.read()

        if(image is None):
            print "Can't read image"
            continue

        if (showCameraImage):
            cv2.imshow("image", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        lumaThreshold = Config().GetInt("ComputerVision", "DarknessThreshold") #
        lumaValue = cv.GetLuma(image)
        if (lumaValue < lumaThreshold):
            bodyData = "{0}|DARKNESS|{1}|{2}".format(cvInstanceType, camType, lumaValue)
            print bodyData
            time.sleep(1)
            continue


        # Body Detection
        if(surveillanceMode or bodyDetectionInterval < 999 and bodyDetectionTimestamp <= (time.time()-bodyDetectionInterval)):
            print "waste of time"
            rawBodyData = cv.DetectBody(image)
            if (len(rawBodyData) > 0):
                bodyDetectionTimestamp = time.time()

                cv.TakeImage(image, "Body", (rawBodyData if cropBodyImage else None))


        # Face Detection
        predictionResult, timeoutReached, luckyShot, rawFaceData = cv.PredictStream(image, predictionObjectList)

        takeImage = True
        for predictionObject in predictionResult:
            thresholdReached = predictionObject.ThresholdReached(predictionThreshold)
            if len(predictionObject.PredictionResult) > 0 and (thresholdReached or timeoutReached or luckyShot):

                 for key, face in predictionObject.PredictionResult.iteritems():
                    bestResult = predictionObject.GetBestPredictionResult(key, 0)

                    if (predictionObject.Name == "Person"):
                        if(bestResult[0] != unknownUserTag):
                            takeImage = False

                        secondBestResult = predictionObject.GetBestPredictionResult(key, 1)
                        predictionData = "{0}|PERSON|{1}|{2}|{3}|{4}|{5}|{6}|{7}".format(cvInstanceType, camType, key, bestResult, secondBestResult, thresholdReached, timeoutReached, luckyShot)


                    if (predictionObject.Name == "Mood"):
                        predictionData = "{0}|MOOD|{1}|{2}|{3}".format(cvInstanceType, camType, key, bestResult)


                    if (predictionObject.Name == "Gender"):
                        predictionData = "{0}|GENDER|{1}|{2}|{3}".format(cvInstanceType, camType, key, bestResult)

                    print predictionData


        # Face position detection
        faceID = 0
        for (x, y, w, h) in rawFaceData:
            centerX = (x + w/2)
            centerY = (y + h/2)

            if (centerX < imageWidth/3):
                posX = "right"
            elif (centerX > imageWidth/3*2):
                posX = "left"
            else:
                posX = "center"

            if (centerY < imageHeight/5):
                posY = "top"
            elif (centerY > imageHeight/5*4):
                posY = "bottom"
            else:
                posY = "center"

            faceData = "{0}|POSITION|{1}|{2}|{3}|{4}".format(cvInstanceType, camType, faceID, posX, posY)
            print faceData
            faceID += 1


        # Take Images
        if(takeImage and clockFace <= (time.time()-intervalBetweenImages) and cv.TakeImage(image, "Person", rawFaceData, grayscale=True)):
            clockFace = time.time()
            print "cheese"

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
