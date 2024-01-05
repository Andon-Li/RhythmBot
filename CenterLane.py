import cv2 as cv
import numpy as np

video = cv.VideoCapture("Video2_5fps_WithInput.mp4")

while True:
    _, image = video.read()
    thin = image[480:870, 960:970]
    cv.imshow("strip", image[480:870, 960:970])
    cv.imshow("wide", image[480:870, 910:1020])

    horizontal_avg = cv.blur(thin, (40, 1))
    cv.imshow("horizontal_avg", horizontal_avg)

    if cv.waitKey() == ord('q'):
        cv.destroyAllWindows()
        quit()
