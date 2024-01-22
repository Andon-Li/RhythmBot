import cv2 as cv
import numpy as np


def row_averages(image: np.array, placeholder: tuple = (0, 0, 0)):
    height, width, _ = image.shape
    average_colors = np.zeros((height, 3))

    for row_index in range(height):
        row = image[row_index, :]
        non_zero_pixels = row[row.sum(axis=1) != 0]

        if non_zero_pixels.size > 0:
            average_colors[row_index] = np.mean(non_zero_pixels, 0)
        else:
            average_colors[row_index] = np.array(placeholder)

    return average_colors.astype(np.uint8)


def crop_by_decimal(image: np.array, left: float, right: float, top: float, bottom: float):
    if left >= right or top >= bottom:
        raise Exception("Negative range")

    height, width, _ = image.shape

    left_px = int(width*left)
    right_px = int(width*right)
    top_px = int(height*top)
    bottom_px = int(height*bottom)

    return image[top_px:bottom_px, left_px:right_px]


def fillPoly_by_decimal(image: np.array, points_d: np.array, color: tuple = (255, 255, 255)):
    height, width, _ = image.shape
    points_px = np.apply_along_axis(lambda a: (int(a[0]*width), int(a[1]*height)), 2, points_d)
    cv.fillPoly(image, points_px, color)


def imshow_tiled(window_name, oned_image):
    reshaped_averages = np.reshape(oned_image, (281, 1, 3))
    tiled_reshaped_averages = np.tile(reshaped_averages, (1, 200, 1))
    cv.imshow(window_name, tiled_reshaped_averages)


if __name__ == '__main__':

    video = cv.VideoCapture("Video4_8fps_WithInput.avi")

    while True:
        _, image = video.read()
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        cropped_image = crop_by_decimal(image, 0.501, 0.503, 0.44, 0.70)

        mask = np.zeros_like(cropped_image)
        points = np.array([[[0, 0], [0.5, 0], [1, 1], [0, 1]]])
        fillPoly_by_decimal(mask, points)
        masked_cropped_image = cv.bitwise_and(cropped_image, mask)

        averages = row_averages(masked_cropped_image)

        cv.imshow("image", cv.cvtColor(image[450:900, 800:1100], cv.COLOR_HSV2BGR))
        cv.imshow("masked cropped image", cv.cvtColor(masked_cropped_image, cv.COLOR_HSV2BGR))
        imshow_tiled("averages", averages)

        ranging = np.zeros_like(averages)
        for index in range(len(averages)):
            if 152 <= averages[index][0] < 157 and 253 <= averages[index][1] < 256 and 95 <= averages[index][2] < 128:  # Purple Note
                ranging[index] = np.array([0, 0, 255])
            elif 6 <= averages[index][0] < 10 and 236 <= averages[index][1] < 256 and 198 <= averages[index][2] < 239:  # Orange Note
                ranging[index] = np.array([0, 255, 0])
            elif 142 <= averages[index][0] < 148 and 48 <= averages[index][1] < 67 and 238 <= averages[index][2] < 256:  # Purple Sustain Off
                ranging[index] = np.array([0, 255, 255])
            else:
                ranging[index] = np.array([40, 40, 40])

        # 147 50 243
        # 147 50 246
        # 145 65 240
        # 145 48 255
        # 145 49 254
        # 144 59 248
        # 145 63 244


        imshow_tiled("ranged", ranging)

        if cv.waitKey() == ord('q'):
            quit()
