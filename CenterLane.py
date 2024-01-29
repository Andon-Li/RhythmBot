# import cv2 as cv
# import numpy as np
#
# video = cv.VideoCapture("Video2_5fps_WithInput.mp4")
#
# while True:
#     _, image = video.read()
#     wide = image[480:870, 900:1030]
#     cropped_image = image[480:870, 960:970]
#     hsv_cropped_image = cv.cvtColor(cropped_image, cv.COLOR_BGR2HSV)
#
#     average_per_row = np.average(hsv_cropped_image, axis=1)
#
#     # 670060 6B0065 75006F 6B0062 purple note
#     # (152, 255, 103), (151, 255, 107.1), (151, 255, 117.3), (154, 255, 100)
#
#     # D53E0C CE370B DA4703 D33C09 orange note
#     # (7, 240, 212), (7, 241, 206.1), (9.5, 251.4, 218.1), (7.5, 244.1, 210.9)
#
#     # E0ADED E1ABF0 E0ACEE CF9EE0 unactivated purple sustain
#     # (144, 68.8, 236.9), (143.5, 73.44, 239.9), (143.5, 70.6, 237.9), (142.5, 75.2, 223.8)
#
#     # EFC7D1 DCB8BA EACACD DBB7B5 unactivated orange sustain
#     # (172.5, 42.5, 238.9), (178.5, 41.8, 220.1), (177, 34.9, 234.1), (1.5, 44.37, 219.1)
#
#     # FBEEFD FBF5FD FCF4FE activated purple sustain
#     # (146, 15.1, 253), (142.5, 8.2, 253), (144, 10, 254)
#
#     # FCF7F7 FDFCF9 FEFCFD activated orange sustain
#     # (0, 5.1, 251.9), (45, 4.08, 232.9), (330, 2.1, 253.9)
#
#     for index, color in enumerate(average_per_row):
#         if (151 <= color[0] <= 155 and
#                 254 <= color[1] <= 255 and
#                 99 <= color[2] <= 118):  # purple note
#             average_per_row[index] = np.array([0, 255, 255])
#         elif (7 <= color[0] <= 10 and
#               240 <= color[1] <= 252 and
#               206 <= color[2] <= 219):  # orange note
#             average_per_row[index] = np.array([60, 255, 255])
#         elif (142 <= color[0] <= 146 and
#               50 <= color[1] <= 94 and
#               215 <= color[2] <= 239):  # unacc purple sustain
#             average_per_row[index] = np.array([120, 255, 255])
#         elif ((172 <= color[0] or color[0] <= 2) and
#               34 <= color[1] <= 45 and
#               219 <= color[2] <= 239):  # unacc orange sustain
#             average_per_row[index] = np.array([180, 255, 255])
#         elif (142 <= color[0] <= 151 and
#               8-2 <= color[1] <= 16 and
#               253-2 <= color[2] <= 254):  # acc purple sustain
#             average_per_row[index] = np.array([240, 255, 255])
#         elif (0 <= color[0] <= 360 and
#               2 <= color[1] <= 6 and
#               232 <= color[2] <= 254):  # acc orange sustain
#             average_per_row[index] = np.array([300, 255, 255])
#
#     category = np.zeros((len(average_per_row), 1, 3), dtype=np.uint8)
#     category[:, 0, :] = average_per_row
#     category = np.tile(category, (1, 1, 1))
#
#     category = cv.cvtColor(category, cv.COLOR_HSV2BGR)
#
#     cv.imshow("wide", wide)
#     cv.imshow("cropped_image", cropped_image)
#     cv.imshow("category", category)
#
#     if cv.waitKey() == ord('q'):
#         cv.destroyAllWindows()
#         quit()

import cv2 as cv
import numpy
import numpy as np

video = cv.VideoCapture("2024-01-23 16-57-32.avi")

while True:
    _, image = video.read()

    mask = np.zeros_like(image)
    vertices = np.array([[961, 800],
                         [960, 479],
                         [968, 479],
                         [972, 800]])
    cv.fillPoly(mask, [vertices], color=(255, 255, 255))

    cropped_lane = cv.bitwise_and(image, mask)

    cv.imshow("image", image)
    cv.imshow("crop", cropped_lane[479:801, 960:973])

    for row in cropped_lane[479:801, 960:973]:
        count = 0
        b_total = 0
        g_total = 0
        r_total = 0
        for pixel in row:
            if numpy.array_equal(pixel, np.array([0, 0, 0])):
                count += 1
                b_total += pixel[0]
                g_total += pixel[1]
                r_total += pixel[2]
        print(f"({b_total/count}, {g_total/count}, {r_total/count})")


    def mouse_callback(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            print(f"x={x},  y={y}")
    cv.setMouseCallback("image", mouse_callback)

    if cv.waitKey() == ord('q'):
        quit()
