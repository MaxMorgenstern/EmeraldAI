#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Pipelines.SpeechToText.STT import STT
from EmeraldAI.Pipelines.InputProcessing.ProcessInput import ProcessInput
from EmeraldAI.Pipelines.ScopeAnalyzer.AnalyzeScope import AnalyzeScope
from EmeraldAI.Pipelines.ResponseProcessing.ProcessResponse import ProcessResponse
from EmeraldAI.Pipelines.TextToSpeech.TTS import TTS
from EmeraldAI.Pipelines.Trainer.Trainer import Trainer
from EmeraldAI.Entities.User import User

from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager

import SubApplication.DetectFace as DF

BaseManager.register('User', User)
manager = BaseManager()
manager.start()
CVUserInstance = manager.User()

def RunBrain():
    loopTerminator = False

    while not loopTerminator:
        pipelineArgs = STT().Process()
        if(pipelineArgs == None):
            continue

        print "We got:", pipelineArgs.Input

        # Get References from Processes
        User().SetUserByCVTag(CVUserInstance.GetCVTag())

        pipelineArgs = ProcessInput().ProcessAsync(pipelineArgs)

        pipelineArgs = AnalyzeScope().Process(pipelineArgs)

        pipelineArgs = ProcessResponse().Process(pipelineArgs)

        pipelineArgs = TTS().Process(pipelineArgs)

        trainerResult = Trainer().Process(pipelineArgs)

        print "Pipeline Args", pipelineArgs.toJSON()
        print "Main User", User().toJSON()
        print "CV User", CVUserInstance.toJSON()
        print "Trainer Result: ", trainerResult




if __name__ == "__main__":
    faceThread = Process(target=DF.RunFaceDetection, args=[CVUserInstance])
    faceThread.start()

    try:
        RunBrain()
    except KeyboardInterrupt:
        print "End"
