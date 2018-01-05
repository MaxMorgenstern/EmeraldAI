#!/usr/bin/python
# -*- coding: utf-8 -*-
import tf2_ros as tf
import rospy

from geometry_msgs.msg import TransformStamped

from EmeraldAI.Logic.Singleton import Singleton

class TFsLooper():
    __metaclass__ = Singleton

    def __init__(self):
        self.__transformBroadcaster = tf.TransformBroadcaster()
        self.__trandformDict = {}
        self.__trandformTTL = {}


    def add(self, transform, ttl=10):
        key = "{0}_{1}".format(transform.header.frame_id, transform.child_frame_id)
        if(key in self.__trandformDict):
            self.remove(key)
        self.__trandformDict[key] = transform
        self.__trandformTTL[key] = ttl


    def remove(self, key):
        del self.__trandformDict[key]
        del self.__trandformTTL[key]


    def loop():
        tmpTrandformDict = dict(self.__trandformDict)
        tmpTrandformTTL = dict(self.__trandformTTL)

        for key in self.__trandformDict:
            tmpTrandformDict[key].header.stamp = rospy.Time.now()

            self.__transformBroadcaster.sendTransform(tmpTrandformDict[key])

            tmpTrandformTTL[key] -= 1

            if tmpTrandformTTL[key] <= 0:
                self.remove(key)

