#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
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

# TODO - global config - mute - detecting people off/on - listen to commands - sleep mode
cancelSpeech = False

def RunBrain():
    rospy.init_node('brain_node', anonymous=True)

    rospy.Subscriber("to_brain", String, callback)

    rospy.spin()

def callback(data):
    dataParts = data.data.split("|")
    print dataParts

    if dataParts[0] == "CV":
        if dataParts[1] == "PERSON":
            ProcessPerson(dataParts[2], dataParts[3], dataParts[4], dataParts[5], dataParts[6])

        if dataParts[1] == "BODY":
            ProcessBody(dataParts[2], dataParts[3], dataParts[4])

        if dataParts[1] == "MOOD":
            ProcessMood(dataParts[2], dataParts[3])

        if dataParts[1] == "GENDER":
            ProcessGender(dataParts[2], dataParts[3])

    if dataParts[0] == "STT":
        ProcessSpeech(dataParts[1])

    if dataParts[0] == "FACEAPP":
        ProcessFaceApp(dataParts[1])

    if dataParts[0] == "PING":
        ProcessPing(dataParts[1])



##### CV #####

def ProcessPerson(id, bestResult, bestResultPerson, thresholdReached, timeoutReached):
    User().SetUserByCVTag("TODO")
    # TODO - bestResult and bestResultPerson are touples ('username', distance)
    # ... TODO - initial greeting on person seen
    # TODO - ensure we don't overwrite this too often

def ProcessBody(id, xPos, yPos):
    print id, xPos, yPos # center, left right, top bottom
    # TODO
    # TODO - trigger eyes to move

def ProcessMood(id, mood):
    print id, mood
    # TODO

def ProcessGender(id, gender):
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
    try:
        RunBrain()
    except KeyboardInterrupt:
        print "End"
