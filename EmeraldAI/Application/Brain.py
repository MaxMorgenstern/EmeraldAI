#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
import re
import time
from math import floor
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Pipelines.InputProcessing.ProcessInput import ProcessInput
from EmeraldAI.Pipelines.ScopeAnalyzer.AnalyzeScope import AnalyzeScope
from EmeraldAI.Pipelines.ResponseProcessing.ProcessResponse import ProcessResponse
from EmeraldAI.Pipelines.TextToSpeech.TTS import TTS
from EmeraldAI.Pipelines.Trainer.Trainer import Trainer
from EmeraldAI.Entities.User import User
from EmeraldAI.Entities.Context import Context
from EmeraldAI.Entities.PipelineArgs import PipelineArgs
from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Audio.SoundMixer import *
from EmeraldAI.Logic.Memory.Brain import Brain as BrainMemory

GLOBAL_FaceappPublisher = None

# TODO lisen and mute to timestamps to set intervals
def InitSettings():
    BrainMemory().Set("PersonDetectionTimestamp", time.time())
    BrainMemory().Set("DarknessTimestamp", time.time())

    if(not BrainMemory().Has("Listen")):
        BrainMemory().Set("Listen", True)

    if(not BrainMemory().Has("Mute")):
        BrainMemory().Set("Mute", False)


def RunBrain():
    global GLOBAL_FaceappPublisher

    rospy.init_node('brain_node', anonymous=True)

    rospy.Subscriber("to_brain", String, callback)

    GLOBAL_FaceappPublisher = rospy.Publisher('to_faceapp', String, queue_size=10)

    rospy.spin()


def callback(data):
    dataParts = data.data.split("|")

    if dataParts[0] == "CLOCK":
        ProcessClock(dataParts[1])

    print "Just got", dataParts

    if dataParts[0] == "CVSURV":
        ProcessSurveilenceData(dataParts)

    if dataParts[0] == "CV":
        ProcessCVData(dataParts)

    if dataParts[0] == "STT":
        ProcessSpeech(dataParts[1])

    if dataParts[0] == "FACEAPP":
        ProcessFaceApp(dataParts[1])

    if dataParts[0] == "PING":
        ProcessPing(dataParts[1])



##### CV #####

def ProcessCVData(dataParts):
    if dataParts[1] == "PERSON":
        ProcessPerson(dataParts[2], dataParts[3], dataParts[4], dataParts[5], (dataParts[6]=="True"), (dataParts[7]=="True"), (dataParts[8]=="True"))

    if dataParts[1] == "POSITION":
        ProcessPosition(dataParts[2], dataParts[3], dataParts[4], dataParts[5])

    if dataParts[1] == "MOOD":
        ProcessMood(dataParts[2], dataParts[3], dataParts[4])

    if dataParts[1] == "GENDER":
        ProcessGender(dataParts[2], dataParts[3], dataParts[4])

    if dataParts[1] == "DARKNESS":
        ProcessDarkness(dataParts[2], dataParts[3])


def ProcessPerson(cameraName, id, bestResult, secondBestResult, thresholdReached, timeoutReached, luckyShot):
    if(not Config().GetBoolean("Application.Brain", "RecognizePeople")):
        return
    if(__cancelCameraProcess(cameraName, BrainMemory().GetFloat("DarknessTimestamp"))):
        return

    currentUser = User().GetCVTag()
    unknownUserTag = Config().Get("Application.Brain", "UnknownUserTag")

    bestResultTag, bestResultValue = __getResult(bestResult)
    secondBestResultTag, secondBestResultValue = __getResult(secondBestResult)

    minSetPersonThreshold = Config().GetInt("Application.Brain", "MinSetPersonThreshold")
    setPersonThreshold = Config().GetInt("Application.Brain", "SetPersonThreshold")

    # skip if best is unknown
    if(bestResultTag == unknownUserTag):
        # expect if 2nd best is about 10% off and no other user is set
        if(secondBestResultTag != None and
            (secondBestResultValue*0.9) >= bestResultValue and
            secondBestResultValue > minSetPersonThreshold and
            (currentUser == unknownUserTag or currentUser == secondBestResultTag)):
            __updateUser(secondBestResultTag, secondBestResultValue)
        return

    # if threshold is reched, set user
    # or if we have at least 1/3 of the person threshold
    if(thresholdReached or bestResultValue >= (setPersonThreshold/3)):
        # if 2nd user is current user and by 10% off the first - update second
        if(secondBestResultTag != None and
            secondBestResultTag != unknownUserTag and
            secondBestResultTag == currentUser and
            (secondBestResultValue*0.6) >= bestResultValue):
            __updateUser(secondBestResultTag, secondBestResultValue)
            return
        __updateUser(bestResultTag, bestResultValue)
        return

    # on lucky shot
    if(luckyShot):
        # if another user is set
        if (currentUser != unknownUserTag and currentUser != bestResultTag):
            return
        if(secondBestResultTag != None and
            secondBestResultTag != unknownUserTag and
            (secondBestResultValue*0.9) >= bestResultValue):
            return
        __updateUser(bestResultTag, bestResultValue, True)
        return


def ProcessPosition(cameraName, cameraId, xPos, yPos):
    if(int(cameraId) > 0 or __cancelCameraProcess(cameraName, BrainMemory().GetFloat("DarknessTimestamp"))):
        return
    lookAt = "center"
    if(yPos != "center"):
        lookAt = yPos
    if(xPos != "center"):
        lookAt = xPos
    ProcessAnimation(lookAt)


def ProcessAnimation(animation):
    global GLOBAL_FaceappPublisher
    if(animation is None):
        return
    animationData = "FACEMASTER|{0}".format(animation)
    rospy.loginfo(animationData)
    GLOBAL_FaceappPublisher.publish(animationData)


def ProcessMood(cameraName, id, mood):
    print int(id), mood
    # TODO

def ProcessGender(cameraName, id, gender):
    print int(id), gender
    # TODO

def ProcessDarkness(cameraName, value):
    # TODO - new parameter value added
    if(cameraName == "IR"):
        return
    BrainMemory().Set("DarknessTimestamp", time.time())


def __getResult(data):
    resultTag = None
    resultValue = 0
    if (len(data) > 2):
        resultData = re.sub("[()'\"]", "", data).split(",")
        resultTag = resultData[0]
        resultValue = int(resultData[1])

    return resultTag, resultValue


def __updateUser(cvTag, predictionValue=0, reducedTimeout=False):
    print "set/update user", cvTag
    personDetectionTimestamp = BrainMemory().GetFloat("PersonDetectionTimestamp")
    if(User().GetCVTag() != cvTag and personDetectionTimestamp > time.time()):
        return

    elif personDetectionTimestamp <= time.time():
        tmpBasePersonTimeout = Config().GetInt("Application.Brain", "PersonTimeout") # 3
        basePersonTimeout = round(tmpBasePersonTimeout/2) if reducedTimeout else tmpBasePersonTimeout
        personDetectionTimestamp = time.time() + basePersonTimeout

    User().SetUserByCVTag(cvTag)

    predictionWeightLowValue = Config().GetInt("Application.Brain", "PredictionWeightLowValue") # 10
    predictionWeightHighValue = Config().GetInt("Application.Brain", "PredictionWeightHighValue") # 20
    predictionWeightHighValueBonus = Config().GetInt("Application.Brain", "PredictionWeightHighValueBonus") # 3
    predictionWeightBorder = Config().GetInt("Application.Brain", "PredictionWeightBorder") # 55

    predictionValue = int(floor(predictionValue/predictionWeightLowValue
        if (predictionValue < predictionWeightBorder) else predictionValue/predictionWeightHighValue+predictionWeightHighValueBonus))

    BrainMemory().Set("PersonDetectionTimestamp", personDetectionTimestamp+predictionValue)


def __cancelCameraProcess(cameraName, darknessTimestamp):
    if(cameraName == "IR"):
        darknessTimeout = Config().GetInt("Application.Brain", "DarknessTimeout") # 10 seconds
        if(not Config().GetBoolean("Application.Brain", "RecognizeWithIRCam")):
            return True
        if(Config().GetBoolean("Application.Brain", "RecognizeWithIRCamOnlyOnDarkness") and darknessTimestamp <= (time.time() - darknessTimeout)):
            return True
    return False


##### CV Surveilence #####

def ProcessSurveilenceData(dataParts):
    print "TODO"



##### STT #####

def ProcessSpeech(data):
    if(not BrainMemory().GetBoolean("Listen")):
        return

    cancelSpeech = False
    stopwordList = Config().GetList("Bot", "StoppwordList")
    if(data in stopwordList):
        cancelSpeech = True
        SoundMixer().Stop()

    pipelineArgs = PipelineArgs(data)

    pipelineArgs = ProcessInput().ProcessAsync(pipelineArgs)

    pipelineArgs = AnalyzeScope().Process(pipelineArgs)

    pipelineArgs = ProcessResponse().Process(pipelineArgs)

    if(not cancelSpeech and not BrainMemory().GetBoolean("Mute")):
        if(pipelineArgs.Animation != None):
            ProcessAnimation(pipelineArgs.Animation)

        pipelineArgs = TTS().Process(pipelineArgs)

    trainerResult = Trainer().Process(pipelineArgs)

    Context().History.append(pipelineArgs)

    print "Pipeline Args", pipelineArgs.toJSON()
    print "Main User", User().toJSON()
    print "Trainer Result: ", trainerResult
    print "Response", pipelineArgs.Response



##### FACEAPP #####

def ProcessFaceApp(state):
    # TODO remove print
    print state
    # state == ON / OFF
    ProcessSpeech("TRIGGER_FACEAPP_{0}".format(state))



##### PING #####

def ProcessPing(state):
    print state
    # TODO - state = DEAD / ALIVE
    # TODO - a device we need does not ping anymore or a new device has been found



##### CLOCK #####

def ProcessClock(timestamp):
    # only check every 5 seconds
    if (int(timestamp)%5 != 0):
        return

    if (BrainMemory().GetFloat("PersonDetectionTimestamp") > time.time()):
        return;

    User().Reset()



##### MAIN #####

if __name__ == "__main__":
    if(Pid.HasPid("Brain")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Brain")
    try:
        InitSettings()
        RunBrain()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Brain")
