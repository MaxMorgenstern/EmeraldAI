#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')
import re

import rospy
from std_msgs.msg import String

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import Config
from EmeraldAI.Entities.User import User
from EmeraldAI.Logic.Memory.Brain import Brain as BrainMemory
from EmeraldAI.Logic.Logger import FileLogger


class BrainCV:
    def __init__(self):
        rospy.init_node('emerald_brain_cv_node', anonymous=True)

        BrainMemory().Set("Brain.CV.Start", rospy.Time.now().to_sec())

        rospy.Subscriber("/emerald_ai/io/computer_vision", String, self.callback)

        self.__FaceappPublisher = rospy.Publisher('/emerald_ai/app/face', String, queue_size=10)

        self.__PersonPublisher = rospy.Publisher('/emerald_ai/io/person', String, queue_size=10)

        self.__RecognizeWithIRCam = Config().GetBoolean("Application.Brain", "RecognizeWithIRCam")
        self.__RecognizeWithIRCamOnlyOnDarkness = Config().GetBoolean("Application.Brain", "RecognizeWithIRCamOnlyOnDarkness")
        self.__RecognizePeople = Config().GetBoolean("Application.Brain", "RecognizePeople")

        self.__DarknessTimeout = Config().GetInt("Application.Brain", "DarknessTimeout") # 10 seconds
        self.__PersonLock = Config().GetInt("Application.Brain", "PersonLock")
        self.__PersonTimeout = Config().GetInt("Application.Brain", "PersonTimeout")

        self.__UnknownUserTag = Config().Get("Application.Brain", "UnknownUserTag")

        self.__MinSetPersonThreshold = Config().GetInt("Application.Brain", "MinSetPersonThreshold")
        self.__SetPersonThreshold = Config().GetInt("Application.Brain", "SetPersonThreshold")

        rospy.spin()


    def callback(self, data):
        dataParts = data.data.split("|")

        if dataParts[0] == "CVSURV":
            self.ProcessSurveilenceData(dataParts)
            return

        if dataParts[0] == "CV":
            self.ProcessCVData(dataParts)
            return

    ##### CV Surveilence #####

    def ProcessSurveilenceData(self, dataParts):
        print "TODO"


    ##### CV #####

    def ProcessCVData(self, dataParts):
        if dataParts[1] == "PERSON":
            # (cameraName, id, bestResult, secondBestResult, thresholdReached, timeoutReached, luckyShot)
            self.ProcessPerson(dataParts[2], dataParts[3], dataParts[4], dataParts[5], (dataParts[6]=="True"), (dataParts[7]=="True"), (dataParts[8]=="True"))

        if dataParts[1] == "POSITION":
            # (cameraName, id, xPos, yPos)
            self.ProcessPosition(dataParts[2], dataParts[3], dataParts[4], dataParts[5])

        if dataParts[1] == "MOOD":
            # (cameraName, id, mood)
            self.ProcessMood(dataParts[2], dataParts[3], dataParts[4])

        if dataParts[1] == "GENDER":
            # (cameraName, id, gender)
            self.ProcessGender(dataParts[2], dataParts[3], dataParts[4])

        if dataParts[1] == "DARKNESS":
            # (cameraName, value)
            self.ProcessDarkness(dataParts[2], dataParts[3])


    def ProcessPerson(self, cameraName, id, bestResult, secondBestResult, thresholdReached, timeoutReached, luckyShot):
        if not self.__RecognizePeople or self.__cancelCameraProcess(cameraName):
            return

        currentPerson = BrainMemory().GetString("CV.Person.CvTag", self.__PersonTimeout)

        bestResultTag, bestResultValue = self.__getResultDetails(bestResult)
        secondBestResultTag, secondBestResultValue = self.__getResultDetails(secondBestResult)

        if(bestResultTag == self.__UnknownUserTag):

            if(secondBestResultTag is not None and
                secondBestResultTag != self.__UnknownUserTag and
                (secondBestResultValue*0.9) >= bestResultValue and
                secondBestResultValue > self.__MinSetPersonThreshold and
                (currentPerson is None or currentPerson == secondBestResultTag or currentPerson == self.__UnknownUserTag)
                ):
                self.__updateUserByCVTag(secondBestResultTag)
            return

        if(thresholdReached or bestResultValue >= (self.__SetPersonThreshold/3)):

            if(secondBestResultTag != None and
                secondBestResultTag != self.__UnknownUserTag and
                secondBestResultTag == currentPerson and
                (secondBestResultValue*0.6) >= bestResultValue):
                self.__updateUserByCVTag(secondBestResultTag)
                return
            self.__updateUserByCVTag(bestResultTag)
            return

        # on lucky shot
        if(luckyShot):
            # if another user is set
            if (currentPerson is not None and currentPerson != self.__UnknownUserTag):
                return
            if(secondBestResultTag != None and
                secondBestResultTag !=  self.__UnknownUserTag and
                (secondBestResultValue*0.9) >= bestResultValue):
                return
            self.__updateUserByCVTag(bestResultTag, True)
            return


    def ProcessPosition(self, cameraName, id, xPos, yPos):
        if(int(id) > 0 or self.__cancelCameraProcess(cameraName)):
            return

        lookAt = "center"
        if(yPos != "center"):
            lookAt = yPos
        if(xPos != "center"):
            lookAt = xPos

        animationData = "FACEMASTER|{0}".format(lookAt)
        FileLogger().Info(animationData)
        self.__FaceappPublisher.publish(animationData)


    def ProcessMood(self, cameraName, id, mood):
        if not self.__RecognizePeople or self.__cancelCameraProcess(cameraName):
            return
        moodName, moodValue = self.__getResultDetails(mood)
        BrainMemory().Set("CV.Person.Mood", moodName)
        BrainMemory().Set("CV.Person.Mood.Value", moodValue)


    def ProcessGender(self, cameraName, id, gender):
        if not self.__RecognizePeople or self.__cancelCameraProcess(cameraName):
            return
        BrainMemory().Set("CV.Person.Gender", gender)


    def ProcessDarkness(self, cameraName, value):
        if(cameraName == "IR"):
            return
        BrainMemory().Set("CV.DarknessTimestamp", rospy.Time.now().to_sec())
        BrainMemory().Set("CV.DarknessValue", value)


    def __getResultDetails(self, data):
        resultTag = None
        resultValue = 0
        if (len(data) > 2):
            resultData = re.sub("[()'\"]", "", data).split(",")
            resultTag = resultData[0]
            resultValue = int(resultData[1])

        return resultTag, resultValue


    def __updateUserByCVTag(self, cvTag, reducedTimeout=False):
        detectedPerson = BrainMemory().GetString("CV.Person.CvTag", self.__PersonTimeout)
        detectionTimestamp = BrainMemory().GetInt("CV.Person.FirstDetectionTimestamp")
        if detectedPerson is None:
            detectionTimestamp = 0

        if (detectedPerson != cvTag and (detectionTimestamp + self.__PersonLock) > rospy.Time.now().to_sec()):
            return

        BrainMemory().Set("CV.Person.CvTag", cvTag)
        User().SetUserByCVTag(cvTag)
        User().SaveObject()

        personData = "PERSON|{0}".format(cvTag)
        FileLogger().Info(personData)
        self.__PersonPublisher.publish(personData)

        if detectedPerson != cvTag:
            timestamp = rospy.Time.now().to_sec()
            if reducedTimeout:
                timestamp = timestamp - self.__PersonLock
            BrainMemory().Set("CV.Person.FirstDetectionTimestamp", timestamp)


    def __cancelCameraProcess(self, cameraName):
        if(cameraName == "IR"):
            if(not self.__RecognizeWithIRCam):
                return True
            darknessTimestamp = BrainMemory().GetFloat("CV.DarknessTimestamp", self.__DarknessTimeout)
            if(self.__RecognizeWithIRCamOnlyOnDarkness and darknessTimestamp is None):
                return True
        return False



if __name__ == "__main__":
    if(Pid.HasPid("Brain.CV")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Brain.CV")
    try:
        BrainCV()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Brain.CV")
