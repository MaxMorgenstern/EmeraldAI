#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import Config
from EmeraldAI.Logic.Logger import FileLogger
from EmeraldAI.Logic.Memory.Brain import Brain as BrainMemory
from EmeraldAI.Pipelines.TriggerProcessing.ProcessTrigger import ProcessTrigger
from EmeraldAI.Logic.Helper import TimeTable
from EmeraldAI.Entities.User import User
from EmeraldAI.Logic.IFTTT import WebhookTrigger


class BrainActionTrigger:
    def __init__(self):    	
        self.__UnknownUserTag = Config().Get("Application.Brain", "UnknownUserTag")

        self.__CheckActive = Config().GetBoolean("ComputerVision.Intruder", "CheckActive")
        self.__CVSURVOnly = Config().GetBoolean("ComputerVision.Intruder", "CVSURVOnly")
        self.__Delay = Config().GetInt("ComputerVision.Intruder", "Delay")

        self.__IFTTTGreeting = Config().Get("IFTTT.Event", "IFTTTGreeting")
        self.__IFTTTIntruder = Config().Get("IFTTT.Event", "IFTTTIntruder")
        self.__IFTTTWebhook = WebhookTrigger.WebhookTrigger()

        self.__TimeTable = TimeTable.TimeTable("ComputerVision.Intruder")

        rospy.init_node('emerald_brain_actiontrigger_node', anonymous=True)

    	self.__SpeechTriggerPublisher = rospy.Publisher('/emerald_ai/io/speech_to_text', String, queue_size=10)

        self.__ResponsePublisher = rospy.Publisher('/emerald_ai/io/text_to_speech', String, queue_size=10)

        self.__TriggerPublisher = rospy.Publisher('/emerald_ai/alert/trigger', String, queue_size=10)

    	# in order to check if someone we know is present
        rospy.Subscriber("/emerald_ai/io/person", String, self.knownPersonCallback)

    	# in order to check if a intruder
        rospy.Subscriber("/emerald_ai/io/computer_vision", String, self.unknownPersonCallback)

        # checks the app status - it sends the status change if turned on/off
        rospy.Subscriber("/emerald_ai/app/status", String, self.appCallback)

        rospy.spin()


    def knownPersonCallback(self, data):
        dataParts = data.data.split("|")
        if (dataParts[0] == "PERSON" and dataParts[1] != self.__UnknownUserTag):

            User().SetUserByCVTag(dataParts[1])

            # Greeting
            if (User().LastSpokenTo is None or 
                datetime.strptime(User().LastSpokenTo, "%Y-%m-%d %H:%M:%S").date() < datetime.today().date()):

                response = ProcessTrigger().ProcessCategory("Greeting")
                lastAudioTimestamp = BrainMemory().GetString("Brain.AudioTimestamp", 20)
                if(lastAudioTimestamp is None and len(response) > 1):
                    FileLogger().Info("ActionTrigger, knownPersonCallback(): {0}".format(response))
                    self.__ResponsePublisher.publish("TTS|{0}".format(response))
                    self.__IFTTTWebhook.TriggerWebhook(self.__IFTTTGreeting, User().FullName, response)

                    self.__TriggerPublisher.publish("TRIGGER|Info|Greeting")


    def unknownPersonCallback(self, data):
        if(not self.__CheckActive or not self.__TimeTable.IsActive()):
            return
        
        dataParts = data.data.split("|")

        if (dataParts[0] == "CV" and self.__CVSURVOnly):
            return

        # No valid user within 5 Minutes
        user = User().LoadObject(300)
        if(user.GetName() is not None and user.GetName().lower() != "unknown"):
            return

        timestamp = BrainMemory().GetInt("Brain.Trigger.UnknownPerson.Timestamp", self.__Delay * 3)
        if (timestamp is None):
            BrainMemory().Set("Brain.Trigger.UnknownPerson.Timestamp", rospy.Time.now().to_sec())
            return

        if(rospy.Time.now().to_sec() - timestamp > self.__Delay):
            
            response = ProcessTrigger().ProcessCategory("Intruder")
            if(len(response) > 1):
                FileLogger().Info("ActionTrigger, unknownPersonCallback(): {0}".format(response))
                self.__ResponsePublisher.publish("TTS|{0}".format(response))
                self.__IFTTTWebhook.TriggerWebhook(self.__IFTTTIntruder)

                self.__TriggerPublisher.publish("TRIGGER|Warning|Intruder")


    def appCallback(self, data):
        dataParts = data.data.split("|")
        if dataParts[0] == "FACEAPP":
            response = "TRIGGER_FACEAPP_{0}".format(dataParts[1]) # == ON / OFF
            FileLogger().Info("ActionTrigger, appCallback(): {0}".format(response))
            self.__SpeechTriggerPublisher.publish("STT|{0}".format(response))


if __name__ == "__main__":
    if(Pid.HasPid("Brain.Trigger")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Brain.Trigger")
    try:
        BrainActionTrigger()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Brain.Trigger")
