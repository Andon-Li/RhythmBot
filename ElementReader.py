from multiprocessing import Queue
import time
from time import sleep, perf_counter
import mss.tools
from colorsys import rgb_to_hsv
import cv2 as cv
import numpy as np


def dec_to_px(sct, monitor_number, top_dec, left_dec, width_dec, height_dec) -> dict:
    monitor = sct.monitors[monitor_number]
    top_px = int(monitor["height"]*top_dec + monitor["top"])
    left_px = int(monitor["width"]*left_dec + monitor["left"])
    if width_dec:
        width_px = int(monitor["width"] * width_dec)
    else:
        width_px = 1
    if height_dec:
        height_px = int(monitor["height"] * height_dec)
    else:
        height_px = 1
    return {"top": top_px,
            "left": left_px,
            "width": width_px,
            "height": height_px,
            "mon": monitor_number}


def is_highway_active(sct, left_dimensions, right_dimensions) -> bool:
    rows = sct.grab(left_dimensions).pixels + sct.grab(right_dimensions).pixels
    for row in rows:
        h, s, v = rgb_to_hsv(*row[0])
        if h > 0.73 or h < 0.78 or \
                s > 0.9 or \
                v > 55 or v < 67:
            return True
    return True


# game_element format: (element type(0-2), lane number(0-4), 'perf_counter' time of action)
def read_elements(element_queue):
    element_height_in_previous_frame = 300  # need to make dynamic
    lift_element_counter = 0
    offset = 0.93

    with mss.mss() as sct:
        lane_2_px_dimensions = dec_to_px(sct, 1, 0.447, 0.493, 0.0, 0.1)

        highway_activity_left_dimensions = dec_to_px(sct, 1, 0.985, 0.277, 0.0, 0.008)
        highway_activity_right_dimensions = dec_to_px(sct, 1, 0.985, 0.731, 0.0, 0.008)

        while True:
            while not is_highway_active(sct, highway_activity_left_dimensions, highway_activity_right_dimensions):
                sleep(0.1)

            lane_2_capture = sct.grab(lane_2_px_dimensions)

            for height, row in enumerate(reversed(lane_2_capture.pixels)):
                h, s, v = rgb_to_hsv(*row[0])

                """
                Color samples for top of purple note
                0.85 0.983 240.98
                0.847 0.996 223.13
                0.847 0.983 233.07
                0.853 0.98 240.98
                0.85 0.991 230.01
                """

                # Purple Note
                if 0.845 < h < 0.855 and \
                        0.975 < s and \
                        220 < v < 245:
                    if element_height_in_previous_frame < height:
                        element_queue.put((0, 2, time.perf_counter() + offset))
                    element_height_in_previous_frame = height
                    break

                # Old Purple Note
                # if 0.85 < h < 0.92 and \
                #         0.95 < s and \
                #         104 < v < 111:
                #     if element_height_in_previous_frame < height:
                #         element_queue.put((0, 2, time.perf_counter() + offset))
                #     element_height_in_previous_frame = height
                #     break

                # Orange Note
                elif 0.045 < h < 0.055 and \
                        0.97 < s and \
                        224 < v < 235:
                    if element_height_in_previous_frame < height:
                        element_queue.put((1, 2, time.perf_counter() + offset))
                    element_height_in_previous_frame = height
                    break

                # Lift Element
                elif 0.82 < h < 0.87 and \
                        0.03 < s < 0.22 and \
                        210 < v:
                    if lift_element_counter == 9:
                        if element_height_in_previous_frame < height:
                            element_queue.put((2, 2, time.perf_counter() + offset))
                        element_height_in_previous_frame = height
                        break
                    else:
                        lift_element_counter += 1

                # Background
                else:
                    lift_element_counter = 0
