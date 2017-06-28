#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
import re
import time
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Pipelines.InputProcessing.ProcessInput import ProcessInput
from EmeraldAI.Pipelines.ScopeAnalyzer.AnalyzeScope import AnalyzeScope
from EmeraldAI.Pipelines.ResponseProcessing.ProcessResponse import ProcessResponse
from EmeraldAI.Pipelines.TextToSpeech.TTS import TTS
from EmeraldAI.Pipelines.Trainer.Trainer import Trainer
from EmeraldAI.Entities.User import User
from EmeraldAI.Entities.Context import Context
from EmeraldAI.Entities.PipelineArgs import PipelineArgs
from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Audio.SoundMixer import *

STT_CancelSpeech = False

CV_PersonDetectionTimestamp = time.time()
CV_DarknessTimestamp = time.time()

GLOBAL_FaceappPub = None

def RunBrain():
    global GLOBAL_FaceappPub

    rospy.init_node('brain_node', anonymous=True)

    rospy.Subscriber("to_brain", String, callback)

    GLOBAL_FaceappPub = rospy.Publisher('to_faceapp', String, queue_size=10)

    rospy.spin()

def callback(data):
    dataParts = data.data.split("|")
    print "Just got", dataParts

    if dataParts[0] == "CVSURV":
        ProcessSurveilenceData(dataParts)

    if dataParts[0] == "CV":
        ProcessCVData(dataParts)

    if dataParts[0] == "STT":
        ProcessSpeech(dataParts[1])

    if dataParts[0] == "FACEAPP":
        ProcessFaceApp(dataParts[1])

    if dataParts[0] == "PING":
        ProcessPing(dataParts[1])


##### CV #####
def ProcessCVData(dataParts):
    if dataParts[1] == "PERSON":
        ProcessPerson(dataParts[2], dataParts[3], dataParts[4], dataParts[5], (dataParts[6]=="True"), (dataParts[7]=="True"))

    if dataParts[1] == "BODY":
        ProcessBody(dataParts[2], dataParts[3], dataParts[4], dataParts[5])

    if dataParts[1] == "MOOD":
        ProcessMood(dataParts[2], dataParts[3], dataParts[4])

    if dataParts[1] == "GENDER":
        ProcessGender(dataParts[2], dataParts[3], dataParts[4])

    if dataParts[1] == "DARKNESS":
        ProcessDarkness(dataParts[2])


def ProcessPerson(cameraName, id, bestResult, bestResultPerson, thresholdReached, timeoutReached):
    global CV_PersonDetectionTimestamp, CV_DarknessTimestamp

    if(not Config().GetBoolean("Application.Brain", "RecognizePeople")):
        return
    if(__cancelCameraProcess(cameraName, CV_DarknessTimestamp)):
        return

    personToUnknownFactor = Config().GetInt("Application.Brain", "PersonToUnknownFactor") # 1 : 5
    personTimeout = Config().GetInt("Application.Brain", "PersonTimeout") # 10 seconds

    bestResultTag = None
    if (len(bestResult) > 2):
        resultData = re.sub("[()'\"]", "", bestResult).split(",")
        bestResultTag = resultData[0]
        bestResultValue = int(resultData[1])

        if (len(bestResultPerson) > 2):
            resultData = re.sub("[()'\"]", "", bestResultPerson).split(",")
            if(bestResultValue / personToUnknownFactor <= int(resultData[1])):
                bestResultTag = resultData[0]

    timeout = False
    if(CV_PersonDetectionTimestamp <= (time.time()-personTimeout)):
        timeout = True

    unknownUserTag = Config().Get("Application.Brain", "UnknownUserTag")
    if(not timeout and not thresholdReached and (not timeoutReached or bestResultTag == unknownUserTag)):
        return

    if(User().GetCVTag() is not bestResultTag):
        print "set user", bestResultTag
        User().SetUserByCVTag(bestResultTag)
        CV_PersonDetectionTimestamp = time.time()


def __cancelCameraProcess(cameraName, darknessTimestamp):
    if(cameraName == "IR"):
        darknessTimeout = Config().GetInt("Application.Brain", "DarknessTimeout") # 10 seconds
        if(not Config().GetBoolean("Application.Brain", "RecognizeWithIRCam")):
            return True
        if(Config().GetBoolean("Application.Brain", "RecognizeWithIRCamOnlyOnDarkness") and darknessTimestamp <= (time.time() - darknessTimeout)):
            return True
    return False


def ProcessBody(cameraName, id, xPos, yPos):
    global CV_DarknessTimestamp

    if(cameraName == "IR"):
        if(CV_DarknessTimestamp <= (time.time() - darknessTimeout)):
            return

    lookAt = "center"
    if(yPos != "center"):
        lookAt = yPos
    if(xPos != "center"):
        lookAt = xPos

    ProcessAnimation(lookAt)


def ProcessAnimation(animation):
    global GLOBAL_FaceappPub

    if(animation == None):
        return

    animationData = "FACEMASTER|{0}".format(animation)
    rospy.loginfo(animationData)
    GLOBAL_FaceappPub.publish(animationData)


def ProcessMood(cameraName, id, mood):
    print id, mood
    # TODO

def ProcessGender(cameraName, id, gender):
    print id, gender
    # TODO

def ProcessDarkness(cameraName):
    global CV_DarknessTimestamp
    if(cameraName == "IR"):
        return
    CV_DarknessTimestamp = time.time()


##### CV Surveilence #####
def ProcessSurveilenceData(dataParts):
    print "TODO"


##### STT #####

def ProcessSpeech(data):
    if(not Config().GetBoolean("Application.Brain", "Listen")):
        return

    STT_CancelSpeech = False
    stopwordList = Config().GetList("Bot", "StoppwordList")
    if(data in stopwordList):
        STT_CancelSpeech = True
        SoundMixer().Stop()

    pipelineArgs = PipelineArgs(data)

    pipelineArgs = ProcessInput().ProcessAsync(pipelineArgs)

    pipelineArgs = AnalyzeScope().Process(pipelineArgs)

    pipelineArgs = ProcessResponse().Process(pipelineArgs)

    if STT_CancelSpeech:
        print "speech canceled"
        return

    if(not Config().GetBoolean("Application.Brain", "Mute")):
        if(pipelineArgs.Animation != None):
            ProcessAnimation(pipelineArgs.Animation)

        pipelineArgs = TTS().Process(pipelineArgs)

    trainerResult = Trainer().Process(pipelineArgs)

    Context().History.append(pipelineArgs)

    print "Pipeline Args", pipelineArgs.toJSON()
    print "Main User", User().toJSON()
    print "Trainer Result: ", trainerResult


##### FACEAPP #####

def ProcessFaceApp(state):
    # TODO remove print
    print state
    # state == ON / OFF
    ProcessSpeech("TRIGGER_FACEAPP_{0}".format(state))


##### FACEAPP #####

def ProcessPing(state):
    print state
    # TODO - state = DEAD / ALIVE
    # TODO - a device we need does not ping anymore or a new device has been found



##### MAIN #####

if __name__ == "__main__":
    if(Pid.HasPid("Brain")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Brain")
    try:
        RunBrain()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Brain")
