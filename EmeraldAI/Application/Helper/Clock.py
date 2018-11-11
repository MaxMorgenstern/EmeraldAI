import time
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.Modules import Pid

import rospy
from std_msgs.msg import String
from rosgraph_msgs.msg import Clock


def RunClock():
    time.sleep(5)

    rospy.init_node('emerald_clock_node', anonymous=False)

    systemTime = rospy.Publisher('/emerald_ai/helper/clock/system', String, queue_size=2)
    rosTime = rospy.Publisher('/emerald_ai/helper/clock/ros', Clock, queue_size=2)

    rate = rospy.Rate(10) # Herz

    clockMessage = Clock()

    while True:
        clockData = "CLOCK|{0}".format(int(round(time.time())))
        systemTime.publish(clockData)

        clockMessage.clock = rospy.Time.now()
        rosTime.publish(clockMessage)

        rate.sleep()



##### MAIN #####

if __name__ == "__main__":
    if(Pid.HasPid("Clock")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Clock")
    try:
        RunClock()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Clock")
