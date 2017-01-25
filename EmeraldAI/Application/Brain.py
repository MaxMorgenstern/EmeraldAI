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

loopTerminator = False

while not loopTerminator:
	pipelineArgs = STT().Process()
	if(pipelineArgs == None):
		continue

	print "We got: ", pipelineArgs.Input

	pipelineArgs = ProcessInput().ProcessAsync(pipelineArgs)

	pipelineArgs = AnalyzeScope().Process(pipelineArgs)

	pipelineArgs = ProcessResponse().Process(pipelineArgs)

	pipelineArgs = TTS().Process(pipelineArgs)

	trainerResult = Trainer().Process(pipelineArgs)

	print "Trainer Result: ", trainerResult
	print "#####"
