import cv2 as cv
import numpy as np
from PIL import ImageGrab
import time


video = cv.VideoCapture("Video2_5fps_WithInput.mp4")

while True:
    # screenshot in BGR format
    success, screenshot = video.read()
    screenshot = screenshot[470:890, 617:1320]

    # --------------------------------

    hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)

    lower_bound_purple = np.array([148, 240, 104])
    upper_bound_purple = np.array([160, 255, 130])

    mask_purple = cv.inRange(hsv, lower_bound_purple, upper_bound_purple)

    lower_bound_orange = np.array([2, 193, 216])
    upper_bound_orange = np.array([22, 255, 240])

    mask_orange = cv.inRange(hsv, lower_bound_orange, upper_bound_orange)

    combined_mask = cv.bitwise_or(mask_purple, mask_orange)

    result = cv.bitwise_and(screenshot, screenshot, mask=combined_mask)

    # ------------------------------------------------

    kernel = np.ones((5, 5), np.uint8)
    combined_mask = cv.dilate(combined_mask, kernel, iterations=1)
    combined_mask = cv.erode(combined_mask, kernel, iterations=1)

    contours, _ = cv.findContours(combined_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        M = cv.moments(contour)

        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        cv.circle(screenshot, (cX, cY), 20, (255, 0, 0), 2)

    # ------------------------------------------------

    cv.imshow('Original Image', screenshot)
    cv.imshow('Mask', combined_mask)
    cv.imshow('Result', result)

    if cv.waitKey() == ord('q'):
        quit()
