#!/usr/bin/env python
from __future__ import division

import serial
import rospy
import os
import sys
import math

import tf2_ros as tf

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


    #wheelDiameter = 64 # mm
    wheelDiameter = 318 # mm - tank
    wheelBaseline = 180 # distance between wheels in mm - tank
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

        distanceLeft = clicksLeft * wheelDistancePerTickLeft
        distanceRight = clicksRight * wheelDistancePerTickRight

        estimatedDistance = (distanceRight + distanceLeft) / 2  / 1000 # mm to m
        estimatedRotation = (distanceRight - distanceLeft) / wheelBaseline


        dt = (currentTime - lastTime).to_sec()

        if (estimatedDistance != 0):
            # calculate distance traveled in x and y
            xTmp = math.cos(estimatedRotation) * estimatedDistance
            yTmp = -math.sin(estimatedRotation) * estimatedDistance
            # calculate the final position of the robot
            x += (math.cos(th) * xTmp - math.sin(th) * yTmp) * dt
            y += (math.sin(th) * xTmp + math.cos(th) * yTmp) * dt

        if (estimatedRotation != 0):
            th += estimatedRotation * dt

        # create the quaternion
        quaternion = Quaternion()
        quaternion.x = 0.0
        quaternion.y = 0.0
        quaternion.z = math.sin(th / 2)
        quaternion.w = math.cos(th / 2)

        SendTF2Transform(transformBroadcaster,
            (x, y, 0.),
            (quaternion.x, quaternion.y, quaternion.z, quaternion.w),
            currentTime,
            odomFrameID,
            odomParentFrameID)

        # next, we'll publish the odometry message over ROS
        odomMsg.header.stamp = currentTime

        # set the position
        odomMsg.pose.pose = Pose(Point(x, y, 0.), quaternion)

        # set the velocity
        odomMsg.twist.twist = Twist(Vector3(estimatedDistance, 0, 0), Vector3(0, 0, estimatedRotation))

        # publish the message
        #rospy.loginfo(odomMsg)
        odomPub.publish(odomMsg)

        lastTime = currentTime


print "Bye!"
