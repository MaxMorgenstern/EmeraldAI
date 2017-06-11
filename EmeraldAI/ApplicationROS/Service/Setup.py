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
import time

from EmeraldAI.Logic.Modules import Global

print "Start setup..."
cp = ConfigParser.ConfigParser()

# Create log config file if it does not exist
print "Check Database"
dbFile = os.path.join(Global.EmeraldPath, "Data", "SqliteDB", "brain.sqlite")
if not os.path.exists(dbFile):
    emptyDB = os.path.join(Global.EmeraldPath, "Data", "SqliteDB", "brain.sqlite.example")
    print "Create database"
    copyfile(emptyDB, dbFile)


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

# TODO - which system are we on Brain? CV? TTS? - setup for specific system

if(updateConfig):
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
    print "Please set your camera"
    print "y: Set camera"
    print "n: Next camera"
    print "q: quit process"
    dump = raw_input("Press enter to confirm")

    camID = 0
    updateCam = True

    timestamp = time.time()
    runCamDetection = True
    selectedID = 0
    while runCamDetection:
        if(updateCam):
            camera = cv2.VideoCapture(camID)
            updateCam = False

        if (camera.isOpened() != 0):
            ret, image = camera.read()

            cv2.imshow("Camera {0}".format(camID), image)

            if cv2.waitKey(1) & 0xFF == ord('y'):
                print "Cam set", camID
                selectedID = camID
                runCamDetection = False

            if cv2.waitKey(1) & 0xFF == ord('n'):
                print "Next camera"
                camID += 1
                updateCam = True

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print "Cancel camera selection"
                camID = 0
                runCamDetection = False

        else:
            if(timestamp + 20 < time.time()):
                print "Camera detection Timeout"
                runCamDetection = False
    print "Set camera #{0} as primary.".format(camID)
    cp.set("ComputerVision", "CameraID", camID)


    # Set Performance
    print "Set the processing power."
    print "'Precise' detection will be slower but more accurate. (Best for computer with more processing power)"
    print "'Fast' detection will be faster but less accurate. (Best for small computer)"

    print "Do you want to set 'Precise' processing?"
    inputData = raw_input("Y/N: ")
    if(inputData.lower() == "y"):
        imageSize = 350
        detectonSetting = "precise"
    else:
        imageSize = 100
        detectonSetting = "fast"

    cp.set("ComputerVision", "ImageSizeWidth", imageSize)
    cp.set("ComputerVision", "ImageSizeHeight", imageSize)
    cp.set("ComputerVision", "DetectionSettings", detectonSetting)


with open(configFile, 'wb') as filePointer:
    cp.write(filePointer)


print "Setup complete"
print "Please open the config file to update API Keys and additional settings"
print "Path: ", configFile

