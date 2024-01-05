import numpy as np
import cv2 as cv

video = cv.VideoCapture("Video2_5fps_WithInput.mp4")

success = True
while success:
    success, image = video.read()

    image = image[480:770, 617:1312]
    image_3ch = image.copy()
    cv.imshow("roi", image)
    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    # # Read Image as gray scale
    # image = cv.imread("image7.jpg", cv.IMREAD_GRAYSCALE)[480:870, 617:1312]

    # Create mask that can isolate the highway
    mask = np.zeros_like(image)
    roi_corners = np.array([[
        (0, 404),
        (163, 0),
        (532, 0),
        (694, 404)
    ]])
    cv.fillPoly(mask, roi_corners, (255,))

    # Use mask onto Image to isolate the highway
    roi = cv.bitwise_and(image, mask)

    # Find all edges of the ROI
    edges = cv.Canny(roi, 120, 120)

    # Mask ROI again to trim the extra edge along the edge of the original mask
    # mask = np.zeros_like(edges)
    # roi_corners = np.array([[
    #     (3, 404),
    #     (166, 0),
    #     (529, 0),
    #     (691, 404)
    # ]])
    # cv.fillPoly(mask, roi_corners, (255,))
    # edges = cv.bitwise_and(edges, mask)

    # Use Hough Line Probabilistic Transform to detect line segments
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=10, minLineLength=100, maxLineGap=40)
    slope_threshold = 2

    # Draw the lines and endpoints on a blank image for visualization
    line_img_with_endpoints = np.zeros_like(edges)

    for line in lines:
        x1, y1, x2, y2 = line[0]

        # Calculate slope (avoid division by zero)
        if x2 - x1 != 0:
            slope = (y2 - y1) / (x2 - x1)
            # Filter lines based on slope threshold
            if abs(slope) > slope_threshold:
                cv.line(line_img_with_endpoints, (x1, y1), (x2, y2), (255, 255, 255), 1)

    image_hsv = cv.cvtColor(image_3ch, cv.COLOR_RGB2HSV)
    bright_mask = cv.inRange(image_hsv, np.array([140, 0, 95]), np.array([148, 8, 99]))
    masked_hsv = cv.bitwise_and(image_hsv, image_hsv, mask=mask)
    masked_hsv = cv.cvtColor(masked_hsv, cv.COLOR_HSV2RGB)

    cv.imshow("bright mask", masked_hsv)
    cv.imshow("gray_roi", roi)
    cv.imshow("edges", edges)
    cv.imshow("lines", line_img_with_endpoints)

    if cv.waitKey() == ord('q'):
        quit()
