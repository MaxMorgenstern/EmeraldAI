import cv2
import numpy as np

# disparity settings
window_size = 5
min_disp = 32
num_disp = 112-min_disp
stereo = cv2.StereoSGBM(
    minDisparity = min_disp,
    numDisparities = num_disp,
    SADWindowSize = window_size,
    uniquenessRatio = 10,
    speckleWindowSize = 100,
    speckleRange = 32,
    disp12MaxDiff = 1,
    P1 = 8*3*window_size**2,
    P2 = 32*3*window_size**2,
    fullDP = False
)

# morphology settings
kernel = np.ones((12,12),np.uint8)

counter = 450

#while counter < 650:

# increment counter
#counter += 1

# only process every third image (so as to speed up video)
#if counter % 3 != 0: continue

# load stereo image
#filename = str(counter).zfill(4)

image_left = cv2.imread('example1_1.png')
image_right = cv2.imread('example1_2.png')

# compute disparity
disparity = stereo.compute(image_left, image_right).astype(np.float32) / 16.0
disparity = (disparity-min_disp)/num_disp

# apply threshold
threshold = cv2.threshold(disparity, 0.6, 1.0, cv2.THRESH_BINARY)[1]
# apply morphological transformation
morphology = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)


# show images
cv2.imshow('left eye', image_left)
cv2.imshow('right eye', image_right)
cv2.imshow('disparity', disparity)
cv2.imshow('threshold', threshold)
cv2.imshow('morphology', morphology)
cv2.waitKey(1)
