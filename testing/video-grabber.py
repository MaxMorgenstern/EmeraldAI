#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
#sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
sys.path.append(dirname(dirname(abspath(__file__))))

reload(sys)
sys.setdefaultencoding('utf-8')

from threading import Thread

import cv2
import time
import numpy as np

import rospy
from sensor_msgs.msg import CompressedImage

from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Modules import Pid


class WebcamVideoStream:
    def __init__(self, camID):
        self.stream = cv2.VideoCapture(camID)
        self.stream.set(3, Config().GetInt("ComputerVision", "CameraWidth"))
        self.stream.set(4, Config().GetInt("ComputerVision", "CameraHeight"))
        (self.grabbed, self.frame) = self.stream.read()

        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        returnValue = self.frame
        self.frame = None
        return returnValue

    def stop(self):
        self.stopped = True


def RunCV(videoStream, camID):
    pub = rospy.Publisher('/camera/{0}'.format(camID), CompressedImage, queue_size=10)
    rospy.init_node('camera_node_{0}'.format(camID), anonymous=True)
    rospy.Rate(10) # 10hz

    if videoStream is not None:
        stream = videoStream.start()
    else:
        camera = cv2.VideoCapture(camID)
        camera.set(3, Config().GetInt("ComputerVision", "CameraWidth"))
        camera.set(4, Config().GetInt("ComputerVision", "CameraHeight"))

    if videoStream is not None:
        image = stream.read()
        while image is None:
            print "Waiting for stream"
            time.sleep(1)
            image = stream.read()
    else:
        while not camera.isOpened():
            print "Waiting for camera"
            time.sleep(1)
        ret, image = camera.read()

    msg = CompressedImage()
    msg.format = "jpeg"

    while True:
        if videoStream is not None:
            image = stream.read()
        else:
            ret, image = camera.read()

        if(image is None):
            continue

        msg.header.stamp = rospy.Time.now()
        msg.data = np.array(cv2.imencode('.jpg', image)[1]).tostring()
        # Publish new image
        pub.publish(msg)




if __name__ == "__main__":
    camID = -1
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if (arg.lower().startswith("-cam")):
                camID = int(arg.lower().replace("-cam", ""))

    if(camID  < 0):
        camID = Config().GetInt("ComputerVision", "CameraID")

    tmpCamID = "" if camID == -1 else camID
    if(Pid.HasPid("Camera_{0}".format(tmpCamID))):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Camera_{0}".format(tmpCamID))

    videoStream = None
    if Config().GetBoolean("ComputerVision", "UseThreadedVideo"):
        videoStream = WebcamVideoStream(camID)

    try:
        RunCV(videoStream, camID)
    except KeyboardInterrupt:
        print "End"
    finally:
        videoStream.stop()
        Pid.Remove("Camera_{0}".format(tmpCamID))
