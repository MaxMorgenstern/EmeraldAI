#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

import speech_recognition as sr
from shutil import copyfile

from EmeraldAI.Logic.Modules import Global


# Create config file if it does not exist
configFile = os.path.join(Global.EmeraldPath, "Config", "base.config")
if not os.path.exists(configFile):
	exampleConfigFile = os.path.join(Global.EmeraldPath, "Config", "base.config.example")
	copyfile(exampleConfigFile, configFile)

# Bot

# TODO - Set Name



# SpeechToText

# TODO - Set Microphone

microphoneDict = {}
for i, name in enumerate(sr.Microphone().list_microphone_names()):
	print i, name
	microphoneDict[i] = name

print "Enter the ID of your primary microphone"
inputData = int(raw_input("ID: "))

print "You selected:", microphoneDict[inputData]


# ComputerVision

# TODO - Set CameraID


