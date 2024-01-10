import cv2 as cv
import numpy as np


def row_averages(image:np.array, placeholder: tuple = (0, 0, 0)):
    height, width, channels = image.shape
    average_colors = np.zeros((height, 3))

    for row_index in range(height):
        row = image[row_index, :]
        non_zero_pixels = row[row.sum(axis=1) != 0]

        if non_zero_pixels:
            average_colors[row_index] = np.mean(non_zero_pixels)
        else:
            average_colors[row_index] = np.array(placeholder)

    return average_colors


def crop_by_decimal(image: np.array, left: float, right: float, top: float, bottom: float):
    if left >= right or top >= bottom:
        raise Exception("Negative range")

    height, width, channels = image.shape

    left_px = int(width*left)
    right_px = int(width*right)
    top_px = int(height*top)
    bottom_px = int(height*bottom)

    return image[top_px:bottom_px, left_px:right_px]


def fillPoly_by_decimal(image, top_left, top_right, bottom_right, bottom_left):





if __name__ == '__main__':

    video = cv.VideoCapture("Video2_5fps_WithInput.mp4")

    while True:
        _, image = video.read()
        cropped_image = crop_by_decimal(image, 0.5, 0.51, 0.44, 0.80)

        mask = np.zeros_like(cropped_image)

        # static points!
        points = np.array([[[0, 0], [0, 10], [10, 10], [10, 0]]])
        cv.fillPoly(mask, points, color=(255, 255, 255))
        masked_cropped_image = cv.bitwise_and(cropped_image, mask)

        cv.imshow("image", image)
        cv.imshow("cropped image", cropped_image)
        cv.imshow("masked cropped image", masked_cropped_image)

        if cv.waitKey() == ord('q'):
            quit()
