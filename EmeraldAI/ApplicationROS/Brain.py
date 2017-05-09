#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
            ProcessUser(dataParts[1], dataParts[2], data.data)

        if dataParts[1] == "BODY":
            print "TODO"

        if dataParts[1] == "MOOD":
            print "TODO"

        if dataParts[1] == "GENDER":
            print "TODO"

        # ... TODO - initial greeting on person seen

    if dataParts[0] == "STT":
        ProcessSpeech(dataParts[1])

    if dataParts[0] == "FACEAPP":
        print "TODO"
        # TODO - tablet turned off / on - trigger action
        # dataParts[1] == ON / OFF

    if dataParts[0] == "PING":

        if dataParts[1] == "DEAD":
            print "TODO"

        if dataParts[1] == "ALIVE":
            print "TODO"
        # TODO - a device we need does not ping anymore or a new device has been found




def ProcessUser(type, cvTag, data):
    User().SetUserByCVTag(cvTag)

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




if __name__ == "__main__":
    try:
        RunBrain()
    except KeyboardInterrupt:
        print "End"
