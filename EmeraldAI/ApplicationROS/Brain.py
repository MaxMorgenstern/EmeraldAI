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

def RunBrain():
    rospy.init_node('brain_node', anonymous=True)

    rospy.Subscriber("to_brain", String, callback)

    rospy.spin()

def callback(data):
    dataParts = data.data.split("|")
    print dataParts

    if dataParts[0] == "CV":
        ProcessUser(dataParts[1])
        # ... TODO - initial greeting

    if dataParts[0] == "STT":
        ProcessSpeech(dataParts[1])
        # TODO - stop command

    if dataParts[0] == "FACEAPP":
        print "TODO"
        # TODO - tablet turned off / on

    if dataParts[0] == "PING":
        print "TODO"
        # TODO - a device we need does not ping anymore




def ProcessUser(cvTag):
    User().SetUserByCVTag(cvTag)

def ProcessSpeech(data):
    pipelineArgs = PipelineArgs(data)

    pipelineArgs = ProcessInput().ProcessAsync(pipelineArgs)

    pipelineArgs = AnalyzeScope().Process(pipelineArgs)

    pipelineArgs = ProcessResponse().Process(pipelineArgs)

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
