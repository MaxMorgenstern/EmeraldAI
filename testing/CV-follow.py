#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import cv2
import re
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

boundaries = [
    # Yellow
    #([17, 100, 100], [50, 200, 200]),
    # RED
    ([17, 15, 100], [50, 56, 200]),
    ([0, 0, 40], [30, 20, 90]),
    ([35, 75, 125], [45, 90, 240]),
    ([60, 50, 120], [100, 75, 145])
]
# yellow - RGB:
# 127 143 71
# 103 114 47
# 107 110 45
# 121 121 64
# 107 113 61
# 112 112 58
# hell
# 239 255 134
# 215 237 100
# 143 169 69

# red - RGB
# 90 15 29
# 70 10 14
# 233 90 117
# 135 82 41
# 227 63 25
#


camera = cv2.VideoCapture(0)

ret = camera.set(3, 320)
ret = camera.set(4, 240)

while True:
    if (camera.isOpened() != 0):
        ret, image = camera.read()
        if image != None:
            height, width = image.shape[:2]

            #image = image[height/2:height, 0:width].copy()
            # Crop from x, y, w, h -> 100, 200, 300, 400
            # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

            globalMask = None
            for (lower, upper) in boundaries:
                # create NumPy arrays from the boundaries
                lower = np.array(lower, dtype = "uint8")
                upper = np.array(upper, dtype = "uint8")

                # find the colors within the specified boundaries and apply
                # the mask
                mask = cv2.inRange(image, lower, upper)
                #output = cv2.bitwise_and(image, image, mask = mask)
                if globalMask == None:
                    globalMask = mask
                else:
                    globalMask += mask


            output = cv2.bitwise_and(image, image, mask = cv2.GaussianBlur(globalMask, (5, 5), 0))
            thresh = cv2.threshold(output, 60, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
            cont = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            contSize = 0
            contObject = None
            for c in cont[0]:
                cS = cv2.contourArea(c)
                M = cv2.moments(c)
                if M["m00"] != 0 and cS > contSize:
                    contSize = cS
                    contObject = c

            contourThreshold = 150

            if contSize >= contourThreshold and contObject != None:
                # compute the center of the contour
                M = cv2.moments(contObject)

                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(image, str(cX) + " - " + str(contSize), (cX - 10, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                pointsToMode = (width/2 - cX)
                cv2.putText(image, str(pointsToMode), (width/2, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv2.imshow("image", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()

