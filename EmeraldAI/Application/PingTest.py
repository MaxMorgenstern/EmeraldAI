#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import rospy
from std_msgs.msg import String
from EmeraldAI.Logic.Modules import Pid

dictionary = {}
publisher = None

def RunPingTest():
    rospy.init_node('ping_test_node', anonymous=True)

    rospy.Subscriber("ping", String, pingCallback)

    publisher = rospy.Publisher('to_brain', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz

    while True:
        rate.sleep()

        if(len(dictionary) > 0):
            now = datetime.datetime.now()
            for key, value in dictionary:
                if((now - value) > datetime.timedelta(minutes=1)):
                    print key, value, "Not available for 60 seconds"
                    rospy.loginfo("PING|DEAD|{0}".format(key))
                    publisher.publish("PING|DEAD|{0}".format(key))

                    # remove key from dict
                    dictionary.pop(key, None)

def pingCallback(data):
    dataParts = data.data.split("|")
    if (dataParts[0] not in dictionary):
        rospy.loginfo("PING|ALIVE|{0}".format(dataParts[0]))
        publisher.publish("PING|ALIVE|{0}".format(dataParts[0]))
    dictionary[dataParts[0]] = datetime.datetime.strptime(dataParts[1], '%H:%M:%S')


if __name__ == "__main__":
    if(Pid.HasPid("PingTest")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("PingTest")

    try:
        RunPingTest()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("PingTest")

