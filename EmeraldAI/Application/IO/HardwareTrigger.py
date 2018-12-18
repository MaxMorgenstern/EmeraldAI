#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pygame
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.GPIO.GPIOProxy import GPIOProxy


class HardwareTrigger:
    def __init__(self, gpioTiggerName="GPIO"):
        rospy.init_node('emerald_trigger_node', anonymous=True)
        rospy.Rate(10) # 10hz

        pygame.init()
        pygame.display.set_mode((200,200))

        
        self.__GPIOInputChannel = Config().GetInt("Trigger", "GPIOPin")
        self.__GPIOTriggerName = gpioTiggerName

        self.__Publisher = rospy.Publisher('/emerald_ai/io/hardware_trigger', String, queue_size=5)

        GPIO = GPIOProxy(None, (self.__GPIOInputChannel))
        GPIO.add_event_detect(self.__GPIOInputChannel, GPIO.RISING, self.GPIOTrigger, 100)


        while 1:
            for event in pygame.event.get():
                #if event.type == pygame.QUIT: sys.exit()
                #if event.type == pygame.KEYDOWN and event.dict['key'] == 27: sys.exit()
                
                if event.type == pygame.KEYDOWN:

                    # Enter
                    if event.key == 13:
                        self.SendTrigger("KEY", "ENTER")
                        continue

                    # Space
                    if event.key == 32:
                        self.SendTrigger("KEY", "SPACE")
                        continue

                    # Esc
                    if event.key == 27:
                        self.SendTrigger("KEY", "ESC")
                        continue

                    self.SendTrigger("KEY", event.key)


    def SendTrigger(self, name, pressId):
        triggerData = "TRIGGER|{0}|{1}|{2}".format(name, pressId, rospy.Time.now().to_sec())
        rospy.loginfo(triggerData)
        self.__Publisher.publish(triggerData)


    def GPIOTrigger(callback):
        self.SendTrigger(self.__GPIOTriggerName, self.__GPIOInputChannel)



if __name__ == "__main__":
    if(Pid.HasPid("Trigger")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Trigger")
    try:

        tmpTriggername = None
        if len(sys.argv) > 1:
            for arg in sys.argv:
                if (arg.lower().startswith("-name")):
                    tmpTriggername = int(arg.lower().replace("-name", ""))

        if tmpTriggername is None:
            HardwareTrigger()
        else:
            HardwareTrigger(tmpTriggername)
    
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Trigger")
