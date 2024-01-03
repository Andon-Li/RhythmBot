import numpy as np
import cv2 as cv

# Read Image
image = cv.imread("image5.jpg")[480:870, 617:1312]

# Create mask that can isolate the highway
mask_3ch = np.zeros_like(image)
roi_corners = np.array([[
    (0, 404),
    (163, 0),
    (532, 0),
    (694, 404)
]])
cv.fillPoly(mask_3ch, roi_corners, (255, 255, 255))

# Use mask onto Image to isolate the highway
roi = cv.bitwise_and(image, mask_3ch)

# Find all edges of the ROI
edges = cv.Canny(roi, 100, 200)

# Mask ROI again to trim the extra edge along the edge of the original mask
mask_1ch = np.zeros_like(edges)
roi_corners = np.array([[
    (3, 404),
    (166, 0),
    (529, 0),
    (691, 404)
]])
cv.fillPoly(mask_1ch, roi_corners, (255, 255, 255))
edges = cv.bitwise_and(edges, mask_1ch)

# Use Hough Line Probabilistic Transform to detect line segments
lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=40, maxLineGap=4)
slope_threshold = 1

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
            cv.line(roi, (x1, y1), (x2, y2), (0, 0, 255), 3)


cv.imshow("edges", edges)
cv.imshow("roi", roi)
cv.imshow("lines", line_img_with_endpoints)

cv.waitKey()
