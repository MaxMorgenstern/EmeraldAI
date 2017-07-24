#!/usr/bin/env python

import rospy
from msg_cv.msg import CV

def talker():
    pub = rospy.Publisher('chat_channel', CV)
    rospy.init_node('talker', anonymous=True)
    r = rospy.Rate(10) #10hz
    msg = CV()
    msg.Name = "Test"
    msg.ID = 0
    msg.BestResult = "(Max, 100)"
    msg.SecondndResult = "()"
    msg.ThresholdReached = True
    msg.timeoutReached = True
    msg.LuckyShot = False

    while not rospy.is_shutdown():
        rospy.loginfo(msg)
        pub.publish(msg)
        r.sleep()

def callback(data):
    rospy.loginfo("%s is age: %d" % (data))

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chat_channel", CV, callback)
    rospy.spin()



if __name__ == '__main__':
    try:
        talker()
        #listener()
    except rospy.ROSInterruptException: pass





