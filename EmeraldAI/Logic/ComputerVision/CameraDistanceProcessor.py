import cv2
from numpy import abs, median, interp
import math

from EmeraldAI.Logic.Singleton import Singleton

def CameraDistanceProcessor(object):
    __metaclass__ = Singleton

    def __init__(self, camID):
        self.__imageWidth = 640
        self.__imageHeight = 480

        self.__camera = cv2.VideoCapture(camID)
        self.__camera.set(3, self.__imageWidth)
        self.__camera.set(4, self.__imageHeight)

        self.__colorThreshold = 220

        # office
        self.__distanceInPixel = [2, 4, 5, 7, 9, 10, 12, 16, 20, 27, 43, 76, 178]
        self.__distanceInMM = [380, 320, 280,230, 200, 180, 150, 120, 100, 80, 50, 30, 10]

        # home
        # self.__distanceInPixel = [0, 2, 6.5, 9.5, 12.5, 16, 27.5, 45.5, 98, 106, 160]
        # self.__distanceInMM = [663, 440, 286, 222, 173, 136, 90, 57, 30, 22, 16]


        def SetPixelDistance(self, pixel, distance):
            self.__distanceInPixel = pixel
            self.__distanceInMM = distance


        def GetDistanceByPixel(self, pixel):
            return interp(pixel, self.__distanceInPixel, self.__distanceInMM)


        def Process(self, returnPixel=False):
            if (self.__camera.isOpened() != 0):

                rval, frame = self.__camera.read()
                
                if frame is None:
                    return -1

                frame = frame[(self.__imageHeight/2-20):(self.__imageHeight/2+25), 0:self.__imageWidth]

                num = (frame[...,...,2] > self.__colorThreshold)
                xy_val =  num.nonzero()

                x_val = median(xy_val[1])

                if(math.isnan(x_val)):
                    return -1

                distInPixel = abs(x_val - self.__imageWidth/2) # distance of dot from center x_axis

                if returnPixel:
                    return distInPixel
                else:
                    return self.GetDistanceByPixel(distInPixel)

            return -1
