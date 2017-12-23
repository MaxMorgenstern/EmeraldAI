#!/usr/bin/env python
import time
import math
import rospy
from geometry_msgs.msg import Twist

speed = 255
timeToSleep = 2

def move():
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    channel = "/navigation/twist"
    #channel = "/turtle1/cmd_vel"
    velocity_publisher = rospy.Publisher(channel, Twist, queue_size=10)
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0


    for i in range(4):
        # move forward
        vel_msg.linear.x = speed
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)
        time.sleep(timeToSleep)

        #rotate ccw
        vel_msg.linear.x = 0
        vel_msg.angular.z = speed * 2 * math.pi / 360
        velocity_publisher.publish(vel_msg)
        time.sleep(timeToSleep)

    # stop
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    time.sleep(timeToSleep)



if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass
