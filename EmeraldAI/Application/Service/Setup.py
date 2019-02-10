#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
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

print "Start config setup..."
cp = ConfigParser.ConfigParser()

# Create log config file if it does not exist
print "Check Database"
dbFile = os.path.join(Global.EmeraldPath, "Data", "SqliteDB", "brain.sqlite")
if not os.path.exists(dbFile):
    emptyDB = os.path.join(Global.EmeraldPath, "Data", "SqliteDB", "brain.sqlite.empty")
    print "Create database"
    copyfile(emptyDB, dbFile)


# Create log config file if it does not exist
print "Check logging.config"
logConfigFile = os.path.join(Global.EmeraldPath, "Config", "logging.config")
if not os.path.exists(logConfigFile):
    logdir = os.path.join(Global.EmeraldPath, "Data", "Log")
    print "Copy example logging.config and set log path to '{0}'".format(logdir)

    exampleLogConfigFile = os.path.join(Global.EmeraldPath, "Config", "logging.config.default")
    copyfile(exampleLogConfigFile, logConfigFile)

    cp.read(logConfigFile)
    cp.set("DEFAULT", "my_log_dir", logdir+"/")
    with open(logConfigFile, 'wb') as filePointer:
        cp.write(filePointer)


# Check logfile and create if it does not exist
cp.read(logConfigFile)
logfile = cp.get("DEFAULT", "my_log_dir") + "logfile.log"
if not os.path.exists(logfile):
    print "Create logfile.log"
    f = open(logfile, "w+")
    f.close()


# Create hardware config file if it does not exist
print "Check hardware.config"
configFileHardware = os.path.join(Global.EmeraldPath, "Config", "hardware.config")
if not os.path.exists(configFileHardware):
    print "Copy example hardware.config"
    exampleConfigFileHardware = os.path.join(Global.EmeraldPath, "Config", "hardware.config.default")
    copyfile(exampleConfigFileHardware, configFileHardware)

# Create config file if it does not exist
print "Check base.config"
updateConfig = False
configFile = os.path.join(Global.EmeraldPath, "Config", "base.config")
if not os.path.exists(configFile):
    print "Copy example base.config"
    exampleConfigFile = os.path.join(Global.EmeraldPath, "Config", "base.config.default")
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
    print "Please set your camera. Keep the Cam-window selected on pressing the key"
    print "y: Set camera"
    print "n: Next camera"
    print "q: quit process"
    dump = raw_input("Press enter to confirm")

    camID = 0
    updateCam = True

    timestamp = time.time()
    runCamDetection = True
    selectedID = 0
    print "Searching for camera... (we stop this process if we can't find any within 20 seconds)"
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
    cv2.destroyWindow("Camera {0}".format(camID))
    cv2.destroyAllWindows()
    print "Set camera #{0} as primary.".format(camID)
    cp.set("ComputerVision", "CameraID", camID)


    # Set Performance
    print "Set the processing power."
    print "P) 'Precise' detection will be slower but more accurate. (Best for computer with more processing power - 350px)"
    print "M) 'Medium' detection will be an avarage of both. (100px)"
    print "F) 'Fast' detection will be faster but less accurate. (Best for small computer - 50px)"

    print "Please select:"
    inputData = raw_input("P/M/F: ")
    if(inputData.lower() == "p"):
        imageSize = 350
        detectonSetting = "precise"
    elif(inputData.lower() == "m"):
        imageSize = 100
        detectonSetting = "medium"
    else:
        imageSize = 50
        detectonSetting = "fast"

    cp.set("ComputerVision", "ImageSizeWidth", imageSize)
    cp.set("ComputerVision", "ImageSizeHeight", imageSize)
    cp.set("ComputerVision", "DetectionSettings", detectonSetting)


with open(configFile, 'wb') as filePointer:
    cp.write(filePointer)


print "Config setup complete"
print "Opening the config files. Please update API Keys and additional settings."
print "Path: ", configFile
print "Path: ", configFileHardware
print "Path: ", logConfigFile

dump = raw_input("Press enter to confirm")

if sys.platform.startswith('darwin'):
    subprocess.call(('open', configFile))
    subprocess.call(('open', configFileHardware))
elif os.name == 'nt': # For Windows
    os.startfile(configFile)
    os.startfile(configFileHardware)
elif os.name == 'posix': # For Linux, Mac, etc.
    subprocess.call(('xdg-open', configFile))
    subprocess.call(('xdg-open', configFileHardware))


print "Setup complete"

time.sleep(2) 
