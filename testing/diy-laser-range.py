import cv2
from numpy import *
import math


#variables
loop = 1
dot_dist = 0
obj_dist = 0
 
cv2.namedWindow("preview")
vc = cv2.VideoCapture(1)

imageWidth = 640
imageHeight = 480


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

pixel = [0, 2, 6.5, 9.5, 12.5, 16, 27.5, 45.5, 98, 106, 160]
distance = [663, 440, 286, 222, 173, 136, 90, 57, 30, 22, 16]

def GetDistanceByPixel(x):
    numpy.interp(x, pixel, distance)


ret = vc.set(3, imageWidth)
ret = vc.set(4, imageHeight)
 
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
 
else:
    rval = False
    #print "failed to open webcam"
 
if rval == 1 :
 
    while loop == 1:
        if (vc.isOpened() != 0):
            rval, frame = vc.read()

            frame = frame[(imageHeight/2-40):(imageHeight/2+40), 0:imageWidth]

            num = (frame[...,...,2] > 230)
            xy_val =  num.nonzero()
 
            y_val = median(xy_val[0])
            x_val = median(xy_val[1])

            cv2.line(frame, (0,imageHeight/2), (imageWidth,imageHeight/2), (255,0,0), 2)
            cv2.line(frame, (imageWidth/2,0),  (imageWidth/2,imageHeight), (255,0,0), 2)

            if(math.isnan(x_val) or math.isnan(y_val)):
                cv2.imshow("preview", frame)
                continue

            cv2.circle(frame, (int(x_val), int(y_val)), 7, (255, 255, 0), -1)

            #distInPixel = ((x_val - imageWidth/2)**2 + (y_val - imageHeight/2)**2 )**0.5 # distance of dot from center pixel
            distInPixel = abs(x_val - imageWidth/2) # distance of dot from center x_axis only

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


elif rval == 0:
        print " webcam error "