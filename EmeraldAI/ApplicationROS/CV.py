#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

# TODO update

from EmeraldAI.Logic.ComputerVision.Predictor import *
from EmeraldAI.Logic.ComputerVision.Detector import *
from EmeraldAI.Config.Config import *

visual = False
if len(sys.argv) > 1 and str(sys.argv[1]) == "visual":
    visual = True

def RunCV():
    pub = rospy.Publisher('to_brain', String, queue_size=10)
    rospy.init_node('CV_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    camera = cv2.VideoCapture(Config().GetInt("ComputerVision", "CameraID"))
    camera.set(3, Config().GetInt("ComputerVision", "CameraWidth"))
    camera.set(4, Config().GetInt("ComputerVision", "CameraHeight"))

    pred = Predictor()

    predictorObject = pred.GetPredictor(camera, Detector().DetectFaceFrontal)
    if predictorObject == None:
        print "Create Dataset"
        pred.CreateDataset()
        predictorObject = pred.GetPredictor(camera, Detector().DetectFaceFrontal)

    previousResult = None
    while True:
        rate.sleep()
        if visual:
            detectionResult = predictorObject.RunVisual()
        else:
            detectionResult = predictorObject.Run()
        detectionResult = pred.RemoveUnknownPredictions(detectionResult)

        if(detectionResult != None and len(detectionResult)):

            """
            # ToDo - check if this is a plausible way of doing it
            if previousResult != None:
                combinedResult = (Counter(previousResult) + Counter(detectionResult))
                print "Combined Result", combinedResult
                print "Combined Best Guess", GetHighestResult(combinedResult)

            print ""
            print "Current Result", detectionResult
            print "Current Best Guess",  GetHighestResult(detectionResult)
            print ""
            print "---"
            """


            bestCVMatch = pred.GetHighestResult(detectionResult)
            if bestCVMatch[0] != None and bestCVMatch[0] != "Unknown" and bestCVMatch[0] != "NotKnown":
                rospy.loginfo("CV|{0}".format(data))
                pub.publish("CV|{0}".format(data))
                print bestCVMatch[0]


            #previousResult = detectionResult.copy()


if __name__ == "__main__":
    try:
        RunCV()
    except KeyboardInterrupt:
        print "End"
