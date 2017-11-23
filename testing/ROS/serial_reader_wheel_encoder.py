#!/usr/bin/env python
from __future__ import division

import serial
import rospy
import os
import sys
import math

import tf2_ros as tf
import tf_conversions as tf_conv

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, TransformStamped


def RadianToDegree(rad):
    return (rad * 4068) / 71.0

def DegreeToRadian(deg):
    return (deg * 71) / 4068.0

def SendTF2Transform(transformBroadcaster, translation, rotation, time, child_frame_id, frame_id):
    t = TransformStamped()
 
    t.header.stamp = time
    t.header.frame_id = frame_id
    t.child_frame_id = child_frame_id
    t.transform.translation.x = translation[0]
    t.transform.translation.y = translation[1]
    t.transform.translation.z = translation[2]
    #t.transform.rotation = rotation

    t.transform.rotation.x = rotation[0]
    t.transform.rotation.y = rotation[1]
    t.transform.rotation.z = rotation[2]
    t.transform.rotation.w = rotation[3]

    transformBroadcaster.sendTransform(t)



if __name__=="__main__":

    uid = str(os.getpid())
    rospy.init_node("serial_reader_{0}".format(uid))
    rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

    odomPub = rospy.Publisher('/odom', Odometry, queue_size=25)
    transformBroadcaster = tf.TransformBroadcaster()

    port_name = "/dev/ttyUSB0"
    #baud = 57600 # 230400
    baud = 230400

    if len(sys.argv) >= 2 :
        port_name  = sys.argv[1]

    if len(sys.argv) >= 3 :
        baud  = int(sys.argv[2])

    ser = serial.Serial(port_name, baud)

    odomParentFrameID = "/odom"
    odomFrameID = "/base_link"
    odomMsg = Odometry()
    odomMsg.header.frame_id = odomParentFrameID
    odomMsg.child_frame_id = odomFrameID


    wheelDiameter = 70 # mm
    wheelBaseline = 100 # distance between wheels in mm
    encoderTicksPerRevelation = 20

    wheelDistancePerTickLeft = math.pi * wheelDiameter / encoderTicksPerRevelation
    wheelDistancePerTickRight = math.pi * wheelDiameter / encoderTicksPerRevelation


    # start position
    x = 0.0
    y = 0.0
    th = 0.0

    currentTime = rospy.Time.now()
    lastTime = rospy.Time.now()

    while True:
        line = ser.readline().rstrip()
        if(len(line) <= 1):
            continue

        data = line.split("|")
        if(len(data) <= 1):
            continue
        #print data

        # we expect 10 values from the ultrasonic node
        if(len(data) > 10):
            continue


        currentTime = rospy.Time.now()
        
        messageType = data[0]
        timestamp = int(data[1])

        moduleID1 = int(data[2])
        timestampDelta1 = int(data[3])
        clickCount1 = int(data[4])
        clickCount1Delata = int(data[5])

        moduleID2 = int(data[6])
        timestampDelta2 = int(data[7])
        clickCount2 = int(data[8])
        clickCount2Delata = int(data[9])

        #####

        clicksLeft = clickCount1Delata
        clicksRight = clickCount2Delata

        distanceLeft = clicksLeft * wheelDistancePerTickLeft / 1000 # mm to m
        distanceRight = clicksRight * wheelDistancePerTickRight / 1000 # mm to m

        estimatedDistance = (distanceRight + distanceLeft) / 2
        estimatedRotation = (distanceLeft - distanceRight) / wheelBaseline

        print distanceLeft, distanceRight
        print estimatedDistance, estimatedRotation


        # compute odometry in a typical way given the velocities of the robot
        dt = (currentTime - lastTime).to_sec()
        delta_x = (estimatedDistance * math.cos(estimatedRotation)) * dt
        delta_y = (estimatedDistance * math.sin(estimatedRotation)) * dt
        delta_th = estimatedRotation * dt

        x += delta_x
        y += delta_y
        th += delta_th


        # since all odometry is 6DOF we'll need a quaternion created from yaw
        odomQuaternion = tf_conv.transformations.quaternion_from_euler(0, 0, th)

        SendTF2Transform(transformBroadcaster,
            (x, y, 0.),
            odomQuaternion,
            currentTime,
            odomFrameID,
            odomParentFrameID)

        # next, we'll publish the odometry message over ROS
        odomMsg.header.stamp = currentTime

        # set the position
        odomMsg.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odomQuaternion))

        # set the velocity
        odomMsg.twist.twist = Twist(Vector3(estimatedDistance, 0, 0), Vector3(0, 0, estimatedRotation))

        # publish the message
        #rospy.loginfo(odomMsg)
        odomPub.publish(odomMsg)

        lastTime = currentTime
        

print "Bye!"
