import cv2
from numpy import *
import math
import time
 
camera = cv2.VideoCapture(1)

imageWidth = 640
imageHeight = 480
colorThreshold = 220


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

ret = camera.set(3, imageWidth)
ret = camera.set(4, imageHeight)

FPSstartTime = time.time()
FPSx = 1
counter = 0

while True:
    if (camera.isOpened() != 0):

        rval, frame = camera.read()
        
        if frame is None:
            continue

        
        frame = frame[(imageHeight/2-20):(imageHeight/2+25), 0:imageWidth]

        num = (frame[...,...,2] > colorThreshold)
        xy_val =  num.nonzero()

        x_val = median(xy_val[1])

        if(math.isnan(x_val)):
            continue

        distInPixel = abs(x_val - imageWidth/2) # distance of dot from center x_axis

        print "Dist from center pixel is:", str(distInPixel)
        print "Estimated distance: ", GetDistanceByPixel(distInPixel)
        
        counter += 1
        if((time.time() - FPSstartTime) > FPSx):
            counter = 0
            FPSstartTime = time.time()

        print "FPS:", (counter / (time.time() - FPSstartTime))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

