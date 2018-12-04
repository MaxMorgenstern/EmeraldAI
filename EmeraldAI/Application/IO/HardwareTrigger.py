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
        
        self.__GPIOInputChannel = Config().GetInt("Trigger", "GPIOPin")
        self.__GPIOTriggerName = gpioTiggerName

        self.__Publisher = rospy.Publisher('/emerald_ai/io/hardware_trigger', String, queue_size=5)

        GPIO = GPIOProxy(None, (self.__GPIOInputChannel))
        GPIO.add_event_detect(self.__GPIOInputChannel, GPIO.RISING, self.GPIOTrigger, 100)

    
        # TODO: Keyboard Trigger
        # TODO: STT Keyword Trigger - snowboy

        print "Keypress..."
        while 1:
            """
            if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
                print "Up pressed"
            pygame.event.pump()
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print "Quit"

        #rospy.spin()


    def GPIOTrigger(callback):
        triggerData = "TRIGGER|{0}|{1}".format(self.__GPIOTriggerName, rospy.Time.now().to_sec())
        rospy.loginfo(triggerData)
        self.__Publisher.publish(triggerData)



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
