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
    element_height_in_previous_frame = 500  # need to make dynamic
    next_element_type = 0
    lift_element_counter = 0
    offset = 0.93

    with mss.mss() as sct:
        lane_2_px_dimensions = dec_to_px(sct, 1, 0.447, 0.493, 0.0, 0.1)

        highway_activity_left_dimensions = dec_to_px(sct, 1, 0.985, 0.277, 0.0, 0.008)
        highway_activity_right_dimensions = dec_to_px(sct, 1, 0.985, 0.731, 0.0, 0.008)

        while True:  # GAME LOOP
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

                # Purple Note, top end of h can be reduced to 0.851
                if 0.84 < h < 0.855 and \
                        0.94 < s and \
                        220 < v < 245:
                    if next_element_type:
                        if element_height_in_previous_frame < height:
                            element_queue.put((next_element_type, 2, perf_counter()+offset))
                            next_element_type = 1
                        element_height_in_previous_frame = height
                    else:
                        next_element_type = 1
                    break

                # Orange Note
                elif 0.1 < h < 0.12 and \
                        0.9 < s and \
                        240 < v:
                    if next_element_type:
                        if element_height_in_previous_frame < height:
                            element_queue.put((next_element_type, 2, perf_counter()+offset))
                            next_element_type = 2
                        element_height_in_previous_frame = height
                    else:
                        next_element_type = 2
                    break

                # Purple Lift Element
                elif 0.82 < h < 0.87 and \
                        0.03 < s < 0.22 and \
                        200 < v:
                    if lift_element_counter == 9:
                        if next_element_type:
                            if element_height_in_previous_frame < height:
                                element_queue.put((next_element_type, 2, perf_counter() + offset))
                                next_element_type = 3
                            element_height_in_previous_frame = height
                        else:
                            next_element_type = 3
                        break
                    else:
                        lift_element_counter += 1

                # Orange Lift Element
                elif (h < 0.03 or h > 0.97) and \
                        0.06 < s < 0.2 and \
                        170 < v:
                    if lift_element_counter == 9:
                        if next_element_type:
                            if element_height_in_previous_frame < height:
                                element_queue.put((next_element_type, 2, perf_counter() + offset))
                                next_element_type = 4
                            element_height_in_previous_frame = height
                        else:
                            next_element_type = 4
                        break
                    else:
                        lift_element_counter += 1

                # Background
                else:
                    lift_element_counter = 0

            # For loop has not found an element
            else:
                if next_element_type:
                    element_queue.put((next_element_type, 2, perf_counter() + offset))
                    element_height_in_previous_frame = 500
                    next_element_type = 0
