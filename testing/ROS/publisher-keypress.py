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
    
    key_up = '0'
    key_down = '0'
    key_right = '0'
    key_left = '0'
    while not rospy.is_shutdown():

        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
            if event.type == KEYDOWN and event.dict['key'] == 27: sys.exit()

            if event.type == KEYUP:
                if event.key == 273: key_up = '0'
                if event.key == 274: key_down = '0'
                if event.key == 275: key_right = '0'
                if event.key == 276: key_left = '0'
                if event.key == 32: key_up = key_down = key_right = key_left = '0'

            if event.type == KEYDOWN:
                if event.key == 273: key_up = '1'
                if event.key == 274: key_down = '1'
                if event.key == 275: key_right = '1'
                if event.key == 276: key_left = '1'
                if event.key == 32: key_up = key_down = key_right = key_left = '0'


        val = int('{}{}{}{}'.format(key_up, key_down, key_left, key_right), 2)
        print "Value:", val
        pub.publish(val)

        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
 