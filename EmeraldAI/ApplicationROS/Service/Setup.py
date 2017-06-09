#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import speech_recognition as sr
from shutil import copyfile
import ConfigParser

from EmeraldAI.Logic.Modules import Global

print "Start setup..."
cp = ConfigParser.ConfigParser()

# Create log config file if it does not exist
print "Check logging.config"
logConfigFile = os.path.join(Global.EmeraldPath, "Config", "logging.config")
if not os.path.exists(logConfigFile):
	logdir = os.path.join(Global.EmeraldPath, "Data", "Log")
	print "Copy example logging.config and set log path to '{0}'".format(logdir)

	exampleLogConfigFile = os.path.join(Global.EmeraldPath, "Config", "logging.config.example")
	copyfile(exampleLogConfigFile, logConfigFile)

	cp.read(logConfigFile)
	cp.set("DEFAULT", "my_log_dir", logdir+"/")
	with open(logConfigFile, 'wb') as filePointer:
	    cp.write(filePointer)


# Create config file if it does not exist
print "Check base.config"
configFile = os.path.join(Global.EmeraldPath, "Config", "base.config")
if not os.path.exists(configFile):
	print "Copy example base.config"
	exampleConfigFile = os.path.join(Global.EmeraldPath, "Config", "base.config.example")
	copyfile(exampleConfigFile, configFile)





"""
cp.read(configFile)
cp.set("Bot", "Name", "Helga")
with open(configFile, 'wb') as cfpointer:
    cp.write(cfpointer)
"""
# Bot


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


