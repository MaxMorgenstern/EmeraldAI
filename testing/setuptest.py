#!/usr/bin/python
# -*- coding: utf-8 -*-
import speech_recognition as sr

microphoneDict = {}
for i, name in enumerate(sr.Microphone().list_microphone_names()):
	print i, name
	microphoneDict[i] = name

print "Enter the ID of your primary microphone"
inputData = int(raw_input("ID: "))

print "You selected:", microphoneDict[inputData]

# set config
# write config
