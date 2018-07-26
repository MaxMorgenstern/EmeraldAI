#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Memory.Brain import Brain as BrainMemory

GLOBAL_FaceappPublisher = None


def InitSettings():
    BrainMemory().Set("Brain.CV.Start", time.time())


def RunBrainCV():
    global GLOBAL_FaceappPublisher

    rospy.init_node('emerald_brain_cv_node', anonymous=True)

    rospy.Subscriber("/emerald_ai/io/computer_vision", String, callback)

    GLOBAL_FaceappPublisher = rospy.Publisher('/emerald_ai/app/face', String, queue_size=10)

    rospy.spin()


def callback(data):
    dataParts = data.data.split("|")
    
    if dataParts[0] == "CVSURV":
        ProcessSurveilenceData(dataParts)
        return

    if dataParts[0] == "CV":
        ProcessCVData(dataParts)
        return


##### CV Surveilence #####

def ProcessSurveilenceData(dataParts):
    print "TODO"



##### CV #####

def ProcessCVData(dataParts):
    if dataParts[1] == "PERSON":
        # (cameraName, id, bestResult, secondBestResult, thresholdReached, timeoutReached, luckyShot)
        ProcessPerson(dataParts[2], dataParts[3], dataParts[4], dataParts[5], (dataParts[6]=="True"), (dataParts[7]=="True"), (dataParts[8]=="True"))

    if dataParts[1] == "POSITION":
        # (cameraName, cameraId, xPos, yPos)
        ProcessPosition(dataParts[2], dataParts[3], dataParts[4], dataParts[5])

    if dataParts[1] == "MOOD":
        # (cameraName, id, mood)
        ProcessMood(dataParts[2], dataParts[3], dataParts[4])

    if dataParts[1] == "GENDER":
        # (cameraName, id, gender)
        ProcessGender(dataParts[2], dataParts[3], dataParts[4])

    if dataParts[1] == "DARKNESS":
        # (cameraName, value)
        ProcessDarkness(dataParts[2], dataParts[3])




if __name__ == "__main__":
    if(Pid.HasPid("Brain.CV")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Brain.CV")
    try:
        InitSettings()
        RunBrainCV()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Brain.CV")
