import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('example1_1.png',0)
imgR = cv2.imread('example1_1.png',0)

stereo = cv2.StereoBM(1, 16, 15)

disparity = stereo.compute(imgL,imgR)

plt.imshow(disparity,'gray')
plt.show()
