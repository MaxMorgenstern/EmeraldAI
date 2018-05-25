#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
#sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
sys.path.append(dirname(dirname(abspath(__file__))))

reload(sys)
sys.setdefaultencoding('utf-8')

import numpy as np
import cv2

import rospy
from sensor_msgs.msg import CompressedImage

from EmeraldAI.Logic.Modules import Pid



def RunCV():
    rospy.init_node('camera_reciever_node', anonymous=True)

    subscriber = rospy.Subscriber("/camera/1", CompressedImage, callback, queue_size = 1)

    rospy.spin()


def callback(data):
    print data.header.stamp

    np_arr = np.fromstring(data.data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)

    cv2.imshow("image", image)
    cv2.waitKey(2)



if __name__ == "__main__":
    if(Pid.HasPid("Reciever_1")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Reciever_1")

    try:
        RunCV()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Reciever_1")
