#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Pipelines.SpeechToText.STT import STT
from EmeraldAI.Pipelines.TextToSpeech.TTS import TTS
from EmeraldAI.Pipelines.InputProcessing.ProcessInput import ProcessInput
from EmeraldAI.Pipelines.ScopeAnalyzer.AnalyzeScope import AnalyzeScope
from EmeraldAI.Pipelines.ResponseProcessing.ProcessResponse import ProcessResponse

from EmeraldAI.Entities.PipelineArgs import PipelineArgs

"""
TODO: Fix this on ProcessInput call if data comes from STT
EmeraldAI/Logic/Modules/NLP.py:44: UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
"""

loopTerminator = False

while not loopTerminator:
	data = STT().Process()
	if(data == None):
		continue

	data = ProcessInput().Process(data)

	data = AnalyzeScope().Process(data)

	data = ProcessResponse().Process(data)

	data = TTS().Process(data)

	print data.toJSON()
