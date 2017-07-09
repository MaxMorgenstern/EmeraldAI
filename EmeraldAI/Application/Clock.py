import time
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.Modules import Pid

import rospy
from std_msgs.msg import String


def RunClock():
    rospy.init_node('clock_node', anonymous=True)

    pub = rospy.Publisher('to_brain', String, queue_size=10)

    rospy.Rate(10) # 10hz

    while True:
        clockData = "CLOCK|{0}".format(int(round(time.time())))
        #print clockData
        #rospy.loginfo(clockData)
        pub.publish(clockData)
        time.sleep(1)



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
