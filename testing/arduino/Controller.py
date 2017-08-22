#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import pygame
from pygame.locals import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.Movement.ParallelWheels import ParallelWheels

pygame.init()
pygame.display.set_mode((100,100))

def talker():
    pub = rospy.Publisher('to_arduino', String, queue_size=10)
    rospy.init_node('keypress_sender', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    val = "0|0|0"
    while not rospy.is_shutdown():

        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
            if event.type == KEYDOWN and event.dict['key'] == 27: sys.exit()

            if event.type == KEYUP:
                """
                if event.key == 273: key_up = '0'
                if event.key == 274: key_down = '0'
                if event.key == 275: key_right = '0'
                if event.key == 276: key_left = '0'
                if event.key == 32: key_up = key_down = key_right = key_left = '0'
                """
            if event.type == KEYDOWN:
                print event.key
                if event.key == 273:
                    val = ParallelWheels().Move(0)
                if event.key == 274:
                    val = ParallelWheels().Move(180)

                if event.key == 275:
                    val = ParallelWheels().Rotate()
                if event.key == 276:
                    val = ParallelWheels().Rotate(False)

                # page up
                if event.key == 280:
                    val = ParallelWheels().Move(-45)

                # page down
                if event.key == 281:
                    val = ParallelWheels().Move(45)

                # Q
                if event.key == 113:
                    val = "0|0|0"
                """
                if event.key == 273: key_up = '1'
                if event.key == 274: key_down = '1'
                if event.key == 275: key_right = '1'
                if event.key == 276: key_left = '1'
                if event.key == 32: key_up = key_down = key_right = key_left = '0'
                """

        print "Message:", val
        pub.publish(val)

        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

