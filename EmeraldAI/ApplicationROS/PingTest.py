#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import rospy
from std_msgs.msg import String

dictionary = {}
# TODO - to config
timeout = 30 # seconds

def RunPingTest():
    rospy.init_node('ping_test_node', anonymous=True)

    rospy.Subscriber("ping", String, pingCallback)

    publisher = rospy.Publisher('to_brain', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz

    # TODO - alive
    while True:
        rate.sleep()
        if(len(dictionary) > 0):
            now = datetime.datetime.now()
            for key, value in dictionary:
                if((now - value) > datetime.timedelta(minutes=1)):
                    print key, value, "Not available for 60 seconds"
                    rospy.loginfo("PING|DEAD|{0}".format(key))
                    publisher.publish("PING|DEAD|{0}".format(key))


def pingCallback(data):
    dataParts = data.data.split("|")
    dictionary[dataParts[0]] = datetime.datetime.strptime(dataParts[1], '%H:%M:%S')

if __name__ == "__main__":
    try:
        RunPingTest()
    except KeyboardInterrupt:
        print "End"

