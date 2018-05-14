#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist


def move():
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    
    rateInHz = 10 # in Hz
    rate = rospy.Rate(rateInHz)

    minVel = 0
    maxVel = 1
    
    currentVelocity = minVel

    #Checking if the movement is forward or backwards
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    while currentVelocity < maxVel:
        vel_msg.linear.x = currentVelocity
        velocity_publisher.publish(vel_msg)
        rate.sleep()

        currentVelocity += 0.001


    vel_msg.linear.x = 0
    #Force the robot to stop
    velocity_publisher.publish(vel_msg)


if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException: pass
