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

    minVel = 0.12 
    maxVel = 0.20
    
    currentVelocity = minVel

    #Checking if the movement is forward or backwards
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    
    print "Start Test"

    while currentVelocity < maxVel:
        vel_msg.linear.x = currentVelocity
        velocity_publisher.publish(vel_msg)
        print "Velocity", currentVelocity
        rate.sleep()

        currentVelocity += 0.0005

    vel_msg.linear.x = 0
    #Force the robot to stop
    velocity_publisher.publish(vel_msg)
    
    return


    minVel = 0.12
    maxVel = 0.20
    currentVelocity = maxVel

    print "Start Test"

    while currentVelocity > minVel:
        vel_msg.linear.x = currentVelocity
        velocity_publisher.publish(vel_msg)
        print "Velocity", currentVelocity
        rate.sleep()

        currentVelocity -= 0.001



if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException: pass
