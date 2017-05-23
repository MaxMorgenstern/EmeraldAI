#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import time

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

# TODO - global config - mute - detecting people off/on - listen to commands - sleep mode
cancelSpeech = False
clockPerson = time.time()

def RunBrain():
    rospy.init_node('brain_node', anonymous=True)

    rospy.Subscriber("to_brain", String, callback)

    rospy.spin()

def callback(data):
    dataParts = data.data.split("|")
    print dataParts

    if dataParts[0] == "CV":
        if dataParts[1] == "PERSON":
            ProcessPerson(dataParts[2], dataParts[3], dataParts[4], dataParts[5], (dataParts[6]=="True"), (dataParts[7]=="True"))

        if dataParts[1] == "BODY":
            ProcessBody(dataParts[2], dataParts[3], dataParts[4], dataParts[5])

        if dataParts[1] == "MOOD":
            ProcessMood(dataParts[2], dataParts[3], dataParts[4])

        if dataParts[1] == "GENDER":
            ProcessGender(dataParts[2], dataParts[3], dataParts[4])

    if dataParts[0] == "STT":
        ProcessSpeech(dataParts[1])

    if dataParts[0] == "FACEAPP":
        ProcessFaceApp(dataParts[1])

    if dataParts[0] == "PING":
        ProcessPing(dataParts[1])



##### CV #####

def ProcessPerson(camId, id, bestResult, bestResultPerson, thresholdReached, timeoutReached):
    global clockPerson

    # TODO - to confic
    personToUnknownFactor = 5
    personTimeout = 10 # seconds

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

    # TODO - unknown user tag from config
    if(not timeout and not thresholdReached and (not timeoutReached or bestResultTag == "Unknown")):
        return

    if(User().GetCVTag() is not bestResultTag):
        User().SetUserByCVTag(bestResultTag)
        clockPerson = time.time()


def ProcessBody(camId, id, xPos, yPos):
    print id, xPos, yPos # center, left right, top bottom
    # TODO
    # TODO - trigger eyes to move

def ProcessMood(camId, id, mood):
    print id, mood
    # TODO

def ProcessGender(camId, id, gender):
    print id, gender
    # TODO


##### STT #####

def ProcessSpeech(data):
    # TODO - check if stop command
    # cancelSpeech = True

    pipelineArgs = PipelineArgs(data)

    pipelineArgs = ProcessInput().ProcessAsync(pipelineArgs)

    pipelineArgs = AnalyzeScope().Process(pipelineArgs)

    pipelineArgs = ProcessResponse().Process(pipelineArgs)

    if cancelSpeech:
        return

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
