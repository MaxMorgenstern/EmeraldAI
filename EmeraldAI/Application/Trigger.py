#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
import time
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

#import rospy
#from std_msgs.msg import String

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.GPIO.GPIOProxy import GPIOProxy

GLOBAL_Publisher = None

def RunTrigger():
    global GLOBAL_Publisher

    # TODO: Config
    GPIOInputChannel = 3 # Board Pin #3

    GLOBAL_Publisher = rospy.Publisher('to_brain', String, queue_size=10)
    rospy.init_node('STT_node', anonymous=True)
    ospy.Rate(10) # 10hz

    # TODO: Config, which trigger

    # GPIO Trigger
    GPIO = GPIOProxy(None, (GPIOInputChannel))
    GPIO.add_event_detect(GPIOInputChannel, GPIO.RISING, Trigger, 100)

    # TODO: Keyboard Trigger
    # TODO: STT Keyword Trigger

    while True:
        time.sleep(1)

def Trigger(callback):
    global GLOBAL_Publisher

    triggerData = "TRIGGER|{0}".format(time.time())
    rospy.loginfo(triggerData)
    GLOBAL_FaceappPublisher.publish(triggerData)


if __name__ == "__main__":
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
