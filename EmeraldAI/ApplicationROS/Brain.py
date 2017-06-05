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

cancelSpeech = False
clockPerson = time.time()
faceappPub = None

def RunBrain():
    global faceappPub

    rospy.init_node('brain_node', anonymous=True)

    rospy.Subscriber("to_brain", String, callback)

    faceappPub = rospy.Publisher('to_faceapp', String, queue_size=10)

    rospy.spin()

def callback(data):
    dataParts = data.data.split("|")
    print "Just got", dataParts

    if dataParts[0] == "CV":
        if dataParts[1] == "PERSON":
            ProcessPerson(dataParts[2], dataParts[3], dataParts[4], dataParts[5], (dataParts[6]=="True"), (dataParts[7]=="True"))

        if dataParts[1] == "BODY":
            ProcessBody(dataParts[2], dataParts[3], dataParts[4], dataParts[5])

        if dataParts[1] == "MOOD":
            ProcessMood(dataParts[2], dataParts[3], dataParts[4])

        if dataParts[1] == "GENDER":
            ProcessGender(dataParts[2], dataParts[3], dataParts[4])

        if dataParts[1] == "DARKNESS":
            print "TODO" # TODO

    if dataParts[0] == "STT":
        ProcessSpeech(dataParts[1])

    if dataParts[0] == "FACEAPP":
        ProcessFaceApp(dataParts[1])

    if dataParts[0] == "PING":
        ProcessPing(dataParts[1])


# TODO cameraName == IR or STD

##### CV #####

def ProcessPerson(cameraName, id, bestResult, bestResultPerson, thresholdReached, timeoutReached):
    global clockPerson

    if(not Config().GetBoolean("Application.Brain", "RecognizePeople")):
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
    if(clockPerson <= (time.time()-personTimeout)):
        timeout = True

    unknownUserTag = Config().Get("Application.Brain", "UnknownUserTag")
    if(not timeout and not thresholdReached and (not timeoutReached or bestResultTag == unknownUserTag)):
        return

    if(User().GetCVTag() is not bestResultTag):
        print "set user", bestResultTag
        User().SetUserByCVTag(bestResultTag)
        clockPerson = time.time()


def ProcessBody(cameraName, id, xPos, yPos):
    global faceappPub

    # TODO - remove
    print id, xPos, yPos # center, left right, top bottom

    lookAt = "center"
    if(yPos != "center"):
        lookAt = yPos
    if(xPos != "center"):
        lookAt = xPos

    lookAtData = "FACEMASTER|{0}".format(lookAt)
    rospy.loginfo(lookAtData)
    faceappPub.publish(lookAtData)


def ProcessMood(cameraName, id, mood):
    print id, mood
    # TODO

def ProcessGender(cameraName, id, gender):
    print id, gender
    # TODO


##### STT #####

def ProcessSpeech(data):
    if(not Config().GetBoolean("Application.Brain", "Listen")):
        return

    cancelSpeech = False
    stopwordList = Config().GetList("Bot", "StoppwordList")
    if(data in stopwordList):
        cancelSpeech = True

    pipelineArgs = PipelineArgs(data)

    pipelineArgs = ProcessInput().ProcessAsync(pipelineArgs)

    pipelineArgs = AnalyzeScope().Process(pipelineArgs)

    pipelineArgs = ProcessResponse().Process(pipelineArgs)

    if cancelSpeech:
        print "speech canceled"
        return

    if(not Config().GetBoolean("Application.Brain", "Mute")):
        pipelineArgs = TTS().Process(pipelineArgs)

    trainerResult = Trainer().Process(pipelineArgs)

    Context().History.append(pipelineArgs)

    print "Pipeline Args", pipelineArgs.toJSON()
    print "Main User", User().toJSON()
    print "Trainer Result: ", trainerResult


##### FACEAPP #####

def ProcessFaceApp(state):
    print state
    # TODO - tablet turned off / on - trigger action
    # state == ON / OFF


##### FACEAPP #####

def ProcessPing(state):
    print state
    # TODO - state = DEAD / ALIVE
    # TODO - a device we need does not ping anymore or a new device has been found



##### MAIN #####

if __name__ == "__main__":
    if(Pid.HasPid("Brain")):
        sys.exit()
    Pid.Create("Brain")
    try:
        RunBrain()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Brain")
