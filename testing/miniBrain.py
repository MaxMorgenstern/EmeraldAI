#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Pipelines.InputProcessing.ProcessInput import ProcessInput
from EmeraldAI.Pipelines.ScopeAnalyzer.AnalyzeScope import AnalyzeScope
from EmeraldAI.Pipelines.ResponseProcessing.ProcessResponse import ProcessResponse
from EmeraldAI.Pipelines.TextToSpeech.TTS import TTS
from EmeraldAI.Pipelines.Trainer.Trainer import Trainer
from EmeraldAI.Entities.User import User
from EmeraldAI.Entities.Context import Context
from EmeraldAI.Entities.PipelineArgs import PipelineArgs
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Audio.SoundMixer import *

def ProcessSpeech(data):
    print "ProcessSpeech - Go"
    cancelSpeech = False
    stopwordList = Config().GetList("Bot", "StoppwordList")
    if(data in stopwordList):
        cancelSpeech = True
        SoundMixer().Stop()

    print "ProcessSpeech - No Stopword"

    pipelineArgs = PipelineArgs(data)

    print "ProcessSpeech - Pipeline Args Created"

    pipelineArgs = ProcessInput().ProcessAsync(pipelineArgs)

    print "ProcessSpeech - Process Async completed"

    pipelineArgs = AnalyzeScope().Process(pipelineArgs)

    print "ProcessSpeech - Scope analyzed"

    pipelineArgs = ProcessResponse().Process(pipelineArgs)

    print "ProcessSpeech - Response processed"

    if(not cancelSpeech):
        if(pipelineArgs.Animation != None):
            print "There should have been an animation", pipelineArgs.Animation

        pipelineArgs = TTS().Process(pipelineArgs)
        print "ProcessSpeech - TTS Triggered"

    trainerResult = Trainer().Process(pipelineArgs)

    print "ProcessSpeech - Trainer Done"

    Context().History.append(pipelineArgs)

    print "Pipeline Args", pipelineArgs.toJSON()
    print "Main User", User().toJSON()
    print "Trainer Result: ", trainerResult
    print "Input: ", data
    print "Response: ", pipelineArgs.Response

    while SoundMixer().IsPlaying():
        time.sleep(1)


print "Set user..."
User().SetUserByCVTag("Max")
print User().toJSON()
time.sleep(2)
print "Start Speech processing"
ProcessSpeech("Warmup")

#ProcessSpeech("Guten Abend")

#ProcessSpeech("Wer ist Angela Merkel")

ProcessSpeech("Wieviel ist 432 plus 68")

ProcessSpeech("Wieviel ist 4 + 32 / 6")

#ProcessSpeech("Bist du ein Mensch")

#ProcessSpeech("TRIGGER_FACEAPP_OFF")

#ProcessSpeech("Was ist eine Süßkartoffel")

ProcessSpeech("Welcher Tag ist heute?")

exit()

ProcessSpeech("xxx")

ProcessSpeech("xxx")
