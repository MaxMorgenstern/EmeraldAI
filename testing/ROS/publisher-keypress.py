#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import pygame
from pygame.locals import *
import sys

pygame.init()
pygame.display.set_mode((100,100))


def talker():
    pub = rospy.Publisher('to_arduino', String, queue_size=10)
    rospy.init_node('keypress_sender', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    data_string = ""
    while not rospy.is_shutdown():

        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
            if event.type == KEYDOWN and event.dict['key'] == 27: sys.exit()

            if event.type == KEYUP:
                data_string = "U|%s" % event.key
                pub.publish(data_string)
                print data_string

            if event.type == KEYDOWN:
                data_string = "D|%s" % event.key
                pub.publish(data_string)
                print data_string

        #print data_string
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
 