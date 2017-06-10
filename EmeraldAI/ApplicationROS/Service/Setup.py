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
import cv2

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
updateConfig = False
configFile = os.path.join(Global.EmeraldPath, "Config", "base.config")
if not os.path.exists(configFile):
    print "Copy example base.config"
    exampleConfigFile = os.path.join(Global.EmeraldPath, "Config", "base.config.example")
    copyfile(exampleConfigFile, configFile)
    updateConfig = True
else:
    print "Do you want to update the data in base.config"
    inputData = raw_input("Y/N: ")
    if(inputData.lower() == "y"):
        updateConfig = True

# TODO - which system are we on Brain? CV? TTS?

if(False):
    cp.read(configFile)

    # Speech To Text
    # Set Microphone
    microphoneDict = {}
    for i, name in enumerate(sr.Microphone().list_microphone_names()):
        print i, name
        microphoneDict[i] = name

    if(len(microphoneDict) > 0):
        print "Enter the ID of your primary microphone"
        inputData = int(raw_input("ID: "))
        print "You selected:", microphoneDict[inputData]

        cp.set("SpeechToText", "Microphone", microphoneDict[inputData])
    else:
        print "No microphone detected"


# ComputerVision

# Set CameraID
camID = 100
camera = cv2.VideoCapture(camID)

while True:
    # TODO timeout
    if (camera.isOpened() != 0):
        print "ok"
        ret, image = camera.read()

        cv2.imshow("Camera {0}".format(camID), image)

        if cv2.waitKey(1) & 0xFF == ord('y'):
            print "Cam set"
        if cv2.waitKey(1) & 0xFF == ord('n'):
            print "Next camera"
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print "Cancel camera selection"
    else:
        print "..."



#with open(configFile, 'wb') as filePointer:
#    cp.write(filePointer)



"""
cp.read(configFile)
cp.set("Bot", "Name", "Helga")
with open(configFile, 'wb') as cfpointer:
    cp.write(cfpointer)
"""
# Bot






