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
from EmeraldAI.Logic.Memory.Brain import Brain as BrainMemory

GLOBAL_FaceappPublisher = None

# TODO lisen and mute to timestamps to set intervals
def InitSettings():
    BrainMemory().Set("PersonDetectionTimestamp", time.time())
    BrainMemory().Set("DarknessTimestamp", time.time())

    if(not BrainMemory().Has("Listen")):
        BrainMemory().Set("Listen", True)

    if(not BrainMemory().Has("Mute")):
        BrainMemory().Set("Mute", False)


def RunBrain():
    global GLOBAL_FaceappPublisher

    rospy.init_node('brain_node', anonymous=True)

    rospy.Subscriber("to_brain", String, callback)

    GLOBAL_FaceappPublisher = rospy.Publisher('to_faceapp', String, queue_size=10)

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

# TODO - we are getting flooded - timeouts after set
# + checking if still user or most likely another one

def ProcessCVData(dataParts):
    if dataParts[1] == "PERSON":
        ProcessPerson(dataParts[2], dataParts[3], dataParts[4], dataParts[5], (dataParts[6]=="True"), (dataParts[7]=="True"))

    if dataParts[1] == "POSITION":
        ProcessPosition(dataParts[2], dataParts[3], dataParts[4], dataParts[5])

    if dataParts[1] == "MOOD":
        ProcessMood(dataParts[2], dataParts[3], dataParts[4])

    if dataParts[1] == "GENDER":
        ProcessGender(dataParts[2], dataParts[3], dataParts[4])

    if dataParts[1] == "DARKNESS":
        ProcessDarkness(dataParts[2], dataParts[3])


def ProcessPerson(cameraName, id, bestResult, bestResultPerson, thresholdReached, timeoutReached):
    if(not Config().GetBoolean("Application.Brain", "RecognizePeople")):
        return
    if(__cancelCameraProcess(cameraName, BrainMemory().GetFloat("DarknessTimestamp"))):
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
    if(BrainMemory().GetFloat("PersonDetectionTimestamp") <= (time.time()-personTimeout)):
        timeout = True

    unknownUserTag = Config().Get("Application.Brain", "UnknownUserTag")
    if(not timeout and not thresholdReached and (not timeoutReached or bestResultTag == unknownUserTag)):
        return

    if(User().GetCVTag() is not bestResultTag):
        print "set user", bestResultTag
        User().SetUserByCVTag(bestResultTag)
        BrainMemory().Set("PersonDetectionTimestamp", time.time())


def __cancelCameraProcess(cameraName, darknessTimestamp):
    if(cameraName == "IR"):
        darknessTimeout = Config().GetInt("Application.Brain", "DarknessTimeout") # 10 seconds
        if(not Config().GetBoolean("Application.Brain", "RecognizeWithIRCam")):
            return True
        if(Config().GetBoolean("Application.Brain", "RecognizeWithIRCamOnlyOnDarkness") and darknessTimestamp <= (time.time() - darknessTimeout)):
            return True
    return False


def ProcessPosition(cameraName, id, xPos, yPos):
    if(id > 0 or cameraName == "IR" and BrainMemory().GetFloat("DarknessTimestamp") <= (time.time() - darknessTimeout)):
            return

    lookAt = "center"
    if(yPos != "center"):
        lookAt = yPos
    if(xPos != "center"):
        lookAt = xPos

    ProcessAnimation(lookAt)


def ProcessAnimation(animation):
    global GLOBAL_FaceappPublisher

    if(animation == None):
        return

    animationData = "FACEMASTER|{0}".format(animation)
    rospy.loginfo(animationData)
    GLOBAL_FaceappPublisher.publish(animationData)


def ProcessMood(cameraName, id, mood):
    print id, mood
    # TODO

def ProcessGender(cameraName, id, gender):
    print id, gender
    # TODO

def ProcessDarkness(cameraName, value):
    # TODO - new parameter value added
    if(cameraName == "IR"):
        return
    BrainMemory().Set("DarknessTimestamp", time.time())



##### CV Surveilence #####

def ProcessSurveilenceData(dataParts):
    print "TODO"



##### STT #####

def ProcessSpeech(data):
    if(not BrainMemory().GetBoolean("Listen")):
        return

    cancelSpeech = False
    stopwordList = Config().GetList("Bot", "StoppwordList")
    if(data in stopwordList):
        cancelSpeech = True
        SoundMixer().Stop()

    pipelineArgs = PipelineArgs(data)

    pipelineArgs = ProcessInput().ProcessAsync(pipelineArgs)

    pipelineArgs = AnalyzeScope().Process(pipelineArgs)

    pipelineArgs = ProcessResponse().Process(pipelineArgs)

    if(not cancelSpeech and not BrainMemory().GetBoolean("Mute")):
        if(pipelineArgs.Animation != None):
            ProcessAnimation(pipelineArgs.Animation)

        pipelineArgs = TTS().Process(pipelineArgs)

    trainerResult = Trainer().Process(pipelineArgs)

    Context().History.append(pipelineArgs)

    print "Pipeline Args", pipelineArgs.toJSON()
    print "Main User", User().toJSON()
    print "Trainer Result: ", trainerResult
    print "Response", pipelineArgs.Response



##### FACEAPP #####

def ProcessFaceApp(state):
    # TODO remove print
    print state
    # state == ON / OFF
    ProcessSpeech("TRIGGER_FACEAPP_{0}".format(state))



##### PING #####

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
        InitSettings()
        RunBrain()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Brain")
