#!/usr/bin/env python

import rospy
import tf
import math
import numpy
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan, Range

rospy.init_node('sonar_to_laser_node')

# buffer
b1 = 0.0
b2 = 0.0

pub_back = rospy.Publisher('/laser/radar/back', LaserScan, queue_size=10)
pub_front = rospy.Publisher('/laser/radar/front', LaserScan, queue_size=10)

Scan_msg = LaserScan()
Scan_msg.angle_min = math.pi/4 - 0.05
Scan_msg.angle_max = math.pi/4 + 0.05
Scan_msg.angle_increment = 0.1
Scan_msg.time_increment = 0.0
Scan_msg.range_min = 0.05
Scan_msg.range_max = 0.5


def callback_buffer(msg):
    global b1, b2
    b1 = b2
    b2 = msg.range

    if b1 > 0.0 and b2 > 0.0:
        Scan_msg.ranges = [msg.range]
    else:
        Scan_msg.ranges = [0.0]

    Scan_msg.header.stamp = rospy.Time.now()
    pub_back.publish(Scan_msg)

def callback_raw_back(msg):
    callback_raw(msg, "back")

def callback_raw_front(msg):
    callback_raw(msg, "front")

def callback_raw(msg, name):
    Scan_msg.ranges = [msg.range]
    Scan_msg.header.stamp = rospy.Time.now()
    Scan_msg.header.frame_id = "/radar_ultrasonic_{0}".format(name)
    
    if name == "back":
        pub_back.publish(Scan_msg)
    
    if name == "front":
        pub_front.publish(Scan_msg)


sub = rospy.Subscriber('/range/radar/back', Range, callback_raw_back)
sub = rospy.Subscriber('/range/radar/front', Range, callback_raw_front)

rospy.spin()
