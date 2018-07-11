#!/usr/bin/env python
import rospy
import os, sys

from nav_msgs.msg import Odometry
#from geometry_msgs.msg import Pose#, Quaternion, Twist, Vector3

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.LocationProcessing.PoseGrabber import *


"""
def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + " I heard %s", data.data)
    pos = data.pose.pose.position
    ori = data.pose.pose.orientation
    #p = Pose(pos, ori)
    #print p
    print pos.x, pos.y, pos.z, " - ", ori.x, ori.y, ori.z, ori.w

    # DID NOT WORK: subscriberObject.unregister()
"""
""" 
def subscriber():
    rospy.init_node('subscriber_node_name_without_slash', anonymous=True)

    msg = rospy.wait_for_message("/odometry/filtered", Odometry)
    print msg.pose.pose

    #subscriberObject = rospy.Subscriber("/odometry/filtered", Odometry, callback)

    rospy.spin()
"""
if __name__ == '__main__':
    print "PID:", str(os.getpid())
    #subscriber()

    pg = PoseGrabber()
    print pg.GetPose()

# http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber(python)
