import cv2 as cv
import numpy as np
from PIL import ImageGrab
import time

# --------------------------------
# screenshot = np.array(ImageGrab.grab((617, 440, 1320, 890)))  # RGB format

image = cv.imread("image6.jpg")
screenshot = cv.cvtColor(image[440:890, 617:1320], cv.COLOR_BGR2RGB)
# --------------------------------

hsv = cv.cvtColor(screenshot, cv.COLOR_RGB2HSV)

lower_bound = np.array([148, 240, 104], dtype=np.uint8)
upper_bound = np.array([160, 255, 130], dtype=np.uint8)

mask = cv.inRange(hsv, lower_bound, upper_bound)
result = cv.bitwise_and(screenshot, screenshot, mask=mask)

# ------------------------------------------------

kernel = np.ones((5, 5), np.uint8)
mask = cv.dilate(mask, kernel, iterations=1)

contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

for contour in contours:
    M = cv.moments(contour)

    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    cv.circle(screenshot, (cX, cY), 20, (255, 0, 0), 2)

# ------------------------------------------------

cv.imshow('Original Image', cv.cvtColor(screenshot, cv.COLOR_RGB2BGR))
cv.imshow('Mask', mask)
cv.imshow('Result', result)

cv.waitKey(0)
cv.destroyAllWindows()
