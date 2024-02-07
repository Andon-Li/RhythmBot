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


# game_element format: (lane number(0-4), element type(0-2), 'perf_counter' time of action)
def read_elements(element_queue):
    element_has_passed = False
    next_element_type = None
    next_element_height = 30000
    lift_element_counter = 0

    with mss.mss() as sct:
        lane_2_px_dimensions = dec_to_px(sct, 1, 0.447, 0.493, 0.0, 0.05)

        highway_activity_left_dimensions = dec_to_px(sct, 1, 0.985, 0.277, 0.0, 0.008)
        highway_activity_right_dimensions = dec_to_px(sct, 1, 0.985, 0.731, 0.0, 0.008)

        while True:
            while not is_highway_active(sct, highway_activity_left_dimensions, highway_activity_right_dimensions):
                sleep(0.1)

            lane_2_capture = sct.grab(lane_2_px_dimensions)

            for idx, row in enumerate(reversed(lane_2_capture.pixels)):
                h, s, v = rgb_to_hsv(*row[0])

                # Purple Note
                if 0.9 < h < 0.92 and \
                        0.95 < s and \
                        104 < v < 111:
                    next_element_type = 0
                    if next_element_height < idx:
                        next_element_height += 30000
                        element_has_passed = True
                    break

                # Orange Note
                elif 0.045 < h < 0.055 and \
                        0.97 < s and \
                        224 < v < 235:
                    next_element_type = 1
                    if next_element_height < idx:
                        next_element_height += 30000
                        element_has_passed = True
                    break

                # Lift Element
                elif 0.82 < h < 0.87 and \
                        0.05 < s < 0.22 and \
                        210 < v:
                    if lift_element_counter == 10:
                        next_element_type = 2
                        if next_element_height < idx:
                            next_element_height += 30000
                            element_has_passed = True
                        break
                    else:
                        lift_element_counter += 1

                # Background
                else:
                    lift_element_counter = 0

            if element_has_passed:
                element_queue.put((next_element_type, perf_counter()))
                element_has_passed = False


def read_elements_headless():
    element_has_passed = False
    next_element_type = None
    next_element_height = 0
    lift_element_counter = 0

    with mss.mss() as sct:
        lane_2_px_dimensions = dec_to_px(sct, 1, 0.447, 0.493, 0.0, 0.05)

        highway_activity_left_dimensions = dec_to_px(sct, 1, 0.985, 0.277, 0.0, 0.008)
        highway_activity_right_dimensions = dec_to_px(sct, 1, 0.985, 0.731, 0.0, 0.008)

        while True:
            while not is_highway_active(sct, highway_activity_left_dimensions, highway_activity_right_dimensions):
                print("@@@@@NOT ACTIVE@@@@@")
                sleep(0.1)

            lane_2_capture = sct.grab(lane_2_px_dimensions)

            for idx, row in enumerate(reversed(lane_2_capture.pixels)):
                h, s, v = rgb_to_hsv(*row[0])

                # Purple Note
                if 0.9 < h < 0.92 and \
                        0.95 < s and \
                        104 < v < 111:
                    if next_element_height < idx:
                        next_element_type = 0
                        next_element_height -= 30000
                        element_has_passed = True
                    next_element_height = idx
                    break

                # Orange Note
                elif 0.045 < h < 0.055 and \
                        0.97 < s and \
                        224 < v < 235:
                    if next_element_height < idx:
                        next_element_type = 1
                        next_element_height -= 30000
                        element_has_passed = True
                    next_element_height = idx
                    break

                # Lift Element
                elif 0.82 < h < 0.87 and \
                        0.03 < s < 0.22 and \
                        210 < v:
                    if lift_element_counter == 9:
                        if next_element_height < idx:
                            next_element_type = 2
                            next_element_height -= 30000
                            element_has_passed = True
                        next_element_height = idx
                        break
                    else:
                        lift_element_counter += 1

                # Background
                else:
                    lift_element_counter = 0

            if element_has_passed:
                match next_element_type:
                    case 0:
                        print("purple", end='')
                    case 1:
                        print("orange", end='')
                    case 2:
                        print("lift", end='')
                print()
                element_has_passed = False


read_elements_headless()
