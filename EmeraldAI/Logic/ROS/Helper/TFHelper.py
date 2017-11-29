#!/usr/bin/python
# -*- coding: utf-8 -*-
from geometry_msgs.msg import TransformStamped

def SendTF2Transform(transformBroadcaster, translation, rotation, time, childFrameID, frameID):
    t = TransformStamped()
 
    t.header.stamp = time
    t.header.frame_id = frameID
    t.child_frame_id = childFrameID
    t.transform.translation.x = translation[0]
    t.transform.translation.y = translation[1]
    t.transform.translation.z = translation[2]

    t.transform.rotation.x = rotation[0]
    t.transform.rotation.y = rotation[1]
    t.transform.rotation.z = rotation[2]
    t.transform.rotation.w = rotation[3]

    transformBroadcaster.sendTransform(t)
