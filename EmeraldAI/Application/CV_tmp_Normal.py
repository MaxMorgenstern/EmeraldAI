#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
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
from EmeraldAI.Logic.Modules import Pid

class FPS:
    def __init__(self):
        self._start = None
        self._numFrames = 0

    def start(self):
        self._start = time.time()
        return self

    def update(self):
        self._numFrames += 1
        if self._numFrames > 200:
            self._start = time.time()
            self._numFrames = 0


    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / (time.time()-self._start)


from threading import Thread

class WebcamVideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, Config().GetInt("ComputerVision", "CameraWidth"))
        self.stream.set(4, Config().GetInt("ComputerVision", "CameraHeight"))
        (self.grabbed, self.frame) = self.stream.read()

        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        returnValue = self.frame
        self.frame = None
        return returnValue

    def stop(self):
        self.stopped = True



def EnsureModelUpdate():
    predictionModules = Config().GetList("ComputerVision", "Modules")
    ModelMonitor().EnsureModelUpdate(predictionModules)


def RunCV(camID, camType, surveillanceMode):
    #pub = rospy.Publisher('to_brain', String, queue_size=10)
    #rospy.init_node('CV_node', anonymous=True)
    #rospy.Rate(10) # 10hz

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
    predictionThreshold = Config().GetInt("ComputerVision.Prediction", "PredictionThreshold")

    showCameraImage = Config().GetBoolean("ComputerVision", "ShowCameraImage")
    unknownUserTag = Config().Get("ComputerVision", "UnknownUserTag")

    cv = ComputerVision()

    predictionObjectList = []

    predictionModules = Config().GetList("ComputerVision", "Modules")
    for moduleName in predictionModules:
        model, dictionary = cv.LoadModel(moduleName)
        if (model is None or dictionary is None):
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

    fps = FPS().start()

    while True:
        #rate.sleep()
        ret, image = camera.read()

        fps.update()
        print"[INFO] FPS:", fps.fps()

        if(image is None):
            print "Skip image"
            continue

        if (showCameraImage):
            cv2.imshow("image", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        lumaThreshold = Config().GetInt("ComputerVision", "DarknessThreshold") #
        lumaValue = cv.GetLuma(image)
        if (lumaValue < lumaThreshold):
            lumaData = "{0}|DARKNESS|{1}|{2}".format(cvInstanceType, camType, lumaValue)
            print lumaData
            #rospy.loginfo(lumaData)
            #pub.publish(lumaData)
            time.sleep(1)
            continue


        # Body Detection
        if((surveillanceMode or bodyDetectionInterval < 999) and bodyDetectionTimestamp <= (time.time()-bodyDetectionInterval)):
            rawBodyData = cv.DetectBody(image)
            if (len(rawBodyData) > 0):
                bodyDetectionTimestamp = time.time()

                cv.TakeImage(image, "Body", (rawBodyData if cropBodyImage else None))


        # Face Detection
        predictionResult, timeoutReached, luckyShot, rawFaceData = cv.PredictStream(image, predictionObjectList)

        takeImage = False
        bestResultName = None
        for predictionObject in predictionResult:
            thresholdReached = predictionObject.ThresholdReached(predictionThreshold)
            if len(predictionObject.PredictionResult) > 0 and (thresholdReached or timeoutReached or luckyShot):

                 for key, face in predictionObject.PredictionResult.iteritems():
                    bestResult = predictionObject.GetBestPredictionResult(key, 0)

                    if (predictionObject.Name == "Person"):
                        secondBestResult = predictionObject.GetBestPredictionResult(key, 1)
                        if(bestResult[0] == unknownUserTag):
                            takeImage = True
                            bestResultName = bestResult[0] if (len(secondBestResult) == 0) else secondBestResult[0]

                        predictionData = "{0}|PERSON|{1}|{2}|{3}|{4}|{5}|{6}|{7}".format(cvInstanceType, camType, key, bestResult, secondBestResult, thresholdReached, timeoutReached, luckyShot)


                    if (predictionObject.Name == "Mood"):
                        predictionData = "{0}|MOOD|{1}|{2}|{3}".format(cvInstanceType, camType, key, bestResult)


                    if (predictionObject.Name == "Gender"):
                        predictionData = "{0}|GENDER|{1}|{2}|{3}".format(cvInstanceType, camType, key, bestResult)

                    print predictionData
                    #rospy.loginfo(predictionData)
                    #pub.publish(predictionData)


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

            positionData = "{0}|POSITION|{1}|{2}|{3}|{4}".format(cvInstanceType, camType, faceID, posX, posY)
            print positionData
            #rospy.loginfo(positionData)
            #pub.publish(positionData)
            faceID += 1


        # Take Images
        if(takeImage and clockFace <= (time.time()-intervalBetweenImages) and cv.TakeImage(image, "Person", rawFaceData, grayscale=True, prefix=bestResultName)):
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

    tmpCamID = "" if camID == -1 else camID
    if(Pid.HasPid("CV{0}".format(tmpCamID))):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("CV{0}".format(tmpCamID))

    try:
        EnsureModelUpdate()
        RunCV(camID, camType, surveillanceMode)
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("CV{0}".format(tmpCamID))
