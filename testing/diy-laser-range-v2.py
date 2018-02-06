import cv2
from numpy import *
import math
import time

from threading import Thread


#variables
loop = 1
dot_dist = 0
obj_dist = 0
 
cv2.namedWindow("preview")

imageWidth = 640
imageHeight = 480
colorThreshold = 220



class WebcamVideoStream:
    def __init__(self, camID):
        self.stream = cv2.VideoCapture(camID)
        self.stream.set(3, imageWidth)
        self.stream.set(4, imageHeight)
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




"""
pixel   distance
2       380
4       320
5       280
7       230
9       200
10      180
12      150
16      120
20      100
27       80
43       50
76       30
178      10
"""


"""
pixel   distance
0       6.630
2       4.440
6.5     2.860
9.5     2.220
12.5    1.730
16      1.360
27.5    0.900
45.5    0.573
98      0.300
106     0.220
160     0.160
"""

# office
pixel = [2, 4, 5, 7, 9, 10, 12, 16, 20, 27, 43, 76, 178]
distance = [380, 320, 280,230, 200, 180, 150, 120, 100, 80, 50, 30, 10]

# home
#pixel = [0, 2, 6.5, 9.5, 12.5, 16, 27.5, 45.5, 98, 106, 160]
#distance = [663, 440, 286, 222, 173, 136, 90, 57, 30, 22, 16]

def GetDistanceByPixel(x):
    return interp(x, pixel, distance)

videoStream = WebcamVideoStream(1)
stream = videoStream.start()

while True:

    frame = stream.read()
    while frame is None:
        print "Waiting for stream"
        time.sleep(0.1)
        frame = stream.read()

    frame = frame[(imageHeight/2-20):(imageHeight/2+25), 0:imageWidth]

    num = (frame[...,...,2] > colorThreshold)
    xy_val =  num.nonzero()

    #y_val = median(xy_val[0])
    x_val = median(xy_val[1])

    if(math.isnan(x_val)):
        continue

    #if(math.isnan(y_val)):
    #    continue
    
    #cv2.line(frame, (0,imageHeight/2), (imageWidth,imageHeight/2), (255,0,0), 2)
    #cv2.line(frame, (imageWidth/2,0),  (imageWidth/2,imageHeight), (255,0,0), 2)
    #cv2.circle(frame, (int(x_val), int(y_val)), 7, (255, 255, 0), -1)

    distInPixel = abs(x_val - imageWidth/2) # distance of dot from center x_axis

    print "Dist from center pixel is:", str(distInPixel)
    print "Estimated distance: ", GetDistanceByPixel(distInPixel)

    """
    # work out distance using D = h/tan(theta)
    theta =0.0011450*distInPixel + 0.0154
    tan_theta = math.tan(theta)

    if tan_theta > 0: # bit of error checking
        obj_dist =  int(5.33 / tan_theta)
    #print "The dot is " + str(obj_dist) + "cm  away"
    """

    cv2.imshow("preview", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

