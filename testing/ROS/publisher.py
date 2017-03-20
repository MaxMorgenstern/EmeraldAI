#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('to_arduino', String, queue_size=10)
    rospy.init_node('chatter_node_name_without_slash', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
        rate.sleep()
        rate.sleep()
        rate.sleep()
        rate.sleep()
        rate.sleep()
        rate.sleep()
        rate.sleep()
        rate.sleep()
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

# http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber(python)
