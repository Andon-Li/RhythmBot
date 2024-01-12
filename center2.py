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

    return average_colors


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


if __name__ == '__main__':

    video = cv.VideoCapture("Video2_5fps_WithInput.mp4")

    while True:
        _, image = video.read()
        # image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        cropped_image = crop_by_decimal(image, 0.5, 0.507, 0.44, 0.70)

        mask = np.zeros_like(cropped_image)

        points = np.array([[[0, 0], [0.55, 0], [1, 1], [0, 1]]])
        fillPoly_by_decimal(mask, points)
        masked_cropped_image = cv.bitwise_and(cropped_image, mask)

        averages = row_averages(masked_cropped_image)

        cv.imshow("image", image[400:900, 800:1100])
        cv.imshow("cropped image", cropped_image)
        cv.imshow("masked cropped image", masked_cropped_image)
        cv.imshow("averages", averages)

        if cv.waitKey() == ord('q'):
            quit()
