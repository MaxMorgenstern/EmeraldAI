#!/usr/bin/env python
import rospy

from nav_msgs.msg import Odometry
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import *
if(Config().Get("Database", "WiFiFingerprintDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "WiFiFingerprintDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

class PositionGrabber(object):
    __metaclass__ = Singleton

    __timeout = 3

    def __init__(self):
        rospy.init_node("Position_grabber", anonymous=True)


    def GetLivePosition(self): 
        try:
            msg = rospy.wait_for_message("/odometry/filtered", Odometry, self.__timeout)
        except Exception:
            return None
        return msg.pose.pose

    def GetDatabasePosition(self, pose, range=0.01):
        p = pose.position
        query = """SELECT * 
            FROM Location_Map_Position
            Where PointX BETWEEN {0} and {1}
            AND PointY BETWEEN {2} and {3}
            AND PointZ BETWEEN {4} and {5}"""

        position = db().Fetchall(query.format((p.x-range), (p.x+range), (p.y-range), (p.y+range), (p.z-range), (p.z+range)))
        if len(position) > 0:
            return position
        return None


    def CreatePosition(self, pose, ignoreOrientation=False):
        p = pose.position
        o = pose.orientation
        if(ignoreOrientation):
            query = "INSERT INTO Location_Map_Position ('PointX', 'PointY', 'PointZ') Values ('{0}', '{1}', '{2}')".format(p.x, p.y, p.z)
        else:
            query = "INSERT INTO Location_Map_Position ('PointX', 'PointY', 'PointZ', 'OrientationX', 'OrientationY', 'OrientationZ', 'OrientationW') Values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(p.x, p.y, p.z, o.x, o.y, o.z, o.w)
        return db().Execute(query)

