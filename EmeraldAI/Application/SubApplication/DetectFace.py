#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.ComputerVision.Predictor import *
from EmeraldAI.Logic.ComputerVision.Detector import *

def RunFaceDetection():
    # TODO - dynamic via config
    camera = cv2.VideoCapture(0)
    ret = camera.set(3, 640)
    ret = camera.set(4, 360)

    p = Predictor()
    predictor = p.GetPredictor(camera, Detector().DetectFaceFrontal)
    while True:
        detectionResult = predictor.run()
        if(detectionResult != None and len(detectionResult)):
            print detectionResult
            print "Best guess" + detectionResult[0][0]
            # TODO - get details of user + write to user class


if __name__ == "__main__":
    RunFaceDetection()
