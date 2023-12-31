import cv2 as cv
import numpy as np
from PIL import ImageGrab

# screenshot = np.array(ImageGrab.grab((617, 480, 1320, 876)))  # RGB format

image = cv.imread("image5.jpg")
screenshot = cv.cvtColor(image[480:876, 617:1320], cv.COLOR_BGR2RGB)

hsv = cv.cvtColor(screenshot, cv.COLOR_RGB2HSV)

lower_bound = np.array([148, 240, 104], dtype=np.uint8)
upper_bound = np.array([160, 252, 130], dtype=np.uint8)

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

    cv.circle(mask, (cX, cY), 20, (255, 255, 255), 2)

# ------------------------------------------------

cv.imshow('Original Image', cv.cvtColor(screenshot, cv.COLOR_RGB2BGR))
cv.imshow('Mask', mask)
cv.imshow('Result', result)

cv.waitKey(0)
cv.destroyAllWindows()
