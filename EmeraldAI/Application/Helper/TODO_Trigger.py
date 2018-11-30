#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
import time
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.GPIO.GPIOProxy import GPIOProxy

GLOBAL_Publisher = None
GLOBAL_TriggerName = "default"

def RunTrigger():
    global GLOBAL_Publisher

    GPIOInputChannel = Config().GetInt("Trigger", "GPIOPin")

    GLOBAL_Publisher = rospy.Publisher('/emerald_ai/helper/hardware_trigger', String, queue_size=5)
    rospy.init_node('emerald_trigger_node', anonymous=True)
    rospy.Rate(10) # 10hz

    # TODO: Config, which trigger

    # GPIO Trigger
    GPIO = GPIOProxy(None, (GPIOInputChannel))
    GPIO.add_event_detect(GPIOInputChannel, GPIO.RISING, Trigger, 100)

    # TODO: Keyboard Trigger
    # TODO: STT Keyword Trigger - snowboy

    while True:
        time.sleep(1)

def Trigger(callback):
    global GLOBAL_Publisher, GLOBAL_TriggerName

    triggerData = "TRIGGER|{0}|{1}".format(GLOBAL_TriggerName, rospy.Time.now().to_sec())
    rospy.loginfo(triggerData)
    GLOBAL_Publisher.publish(triggerData)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if (arg.lower().startswith("-name")):
                GLOBAL_TriggerName = int(arg.lower().replace("-name", ""))

    if(Pid.HasPid("Trigger")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Trigger")
    try:
        RunTrigger()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Trigger")
