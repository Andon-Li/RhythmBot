from time import perf_counter
import mss.tools
from colorsys import rgb_to_hsv
import cv2 as cv
import numpy as np
import pyautogui as pag
import dxcam


def initialization():
    def bresenham_line(x0, x1, dy):
        x0 = int(x0)
        x1 = int(x1)
        output = []
        dx = x1-x0
        xi = 1

        if dx < 0:
            xi -= 1
            dx *= -1

        D = (2*dx)-dy
        x = x0

        for y in range(dy):
            output.append((x, dy-y-1))
            if D > 0:
                x = x + xi
                D += 2*(dx-dy)
            else:
                D += 2*dx

        return output

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        monitor_height = monitor['height']
        monitor_width = monitor['width']
    cap_left = int(monitor_width * 0.3771)
    cap_top = int(monitor_height * 0.4445)
    cap_right = int(monitor_width * 0.6277)
    cap_bottom = int(monitor_height * 0.5445)
    cap_width = cap_right-cap_left
    cap_height = cap_bottom-cap_top

    activity = bresenham_line(0, cap_width*0.0894, cap_height)

    lane_0 = bresenham_line(cap_width * 0.0583, cap_width * 0.1352, cap_height)
    lane_1 = bresenham_line(cap_width * 0.2578, cap_width * 0.2973, cap_height)
    lane_2 = bresenham_line(cap_width * 0.4574, cap_width * 0.4616, cap_height)
    lane_3 = bresenham_line(cap_width * 0.6549, cap_width * 0.6217, cap_height)
    lane_4 = bresenham_line(cap_width * 0.8545, cap_width * 0.7880, cap_height)

    return ((cap_left, cap_top, cap_right, cap_bottom),
            (lane_0, lane_1, lane_2, lane_3, lane_4),
            activity)


def is_highway_inactive(image, indices) -> bool:
    for x, y in indices:
        h, s, v = rgb_to_hsv(*image[y, x])
        if h < 0.7 or h > 0.81 or \
                s < 0.67 or \
                v < 114 or v > 190:
            return True
    return False


def matches_purple_note(h, s, v):
    if 0.84 < h < 0.865 and \
            0.94 < s and \
            105 < v < 140:
        return True
    return False


def matches_orange_note(h, s, v):
    if 0.1 < h < 0.12 and \
            0.9 < s and \
            240 < v:
        return True
    return False


def matches_purple_lift_note(h, s, v):
    if 0.82 < h < 0.88 and \
            0.03 < s < 0.22 and \
            200 < v:
        return True
    return False


def matches_orange_lift_note(h, s, v):
    if (h < 0.03 or h > 0.97) and \
            0.06 < s < 0.2 and \
            170 < v:
        return True
    return False


def read_elements(element_queue):
    current_note_type = 0
    current_note_height = 99999

    offset = 0.5

    lift_note_counter = 0

    cap_region, lane_indices, activity_indices = initialization()

    camera = dxcam.create(region=cap_region)
    camera.start()
    while True:
        image = camera.get_latest_frame()

        if is_highway_inactive(image, activity_indices):
            continue

        for lane_num, indexes in enumerate(lane_indices):
            for x, y in indexes:
                h, s, v = rgb_to_hsv(*image[y, x])

                if matches_purple_note(h, s, v):
                    if y > current_note_height:
                        element_queue.put((current_note_type, lane_num, perf_counter()+offset))
                        current_note_type = 1
                    current_note_height = y
                    break

                elif matches_orange_note(h, s, v):
                    if y > current_note_height:
                        element_queue.put((current_note_type, lane_num, perf_counter()+offset))
                        current_note_type = 2
                    current_note_height = y
                    break

                elif matches_orange_lift_note(h, s, v):
                    if lift_note_counter == 9:
                        if y > current_note_height:
                            element_queue.put((current_note_type, lane_num, perf_counter()+offset))
                            current_note_type = 3
                        current_note_height = y
                    else:
                        lift_note_counter += 1
                    break

                elif matches_purple_lift_note(h, s, v):
                    if lift_note_counter == 9:
                        if y > current_note_height:
                            element_queue.put((current_note_type, lane_num, perf_counter()+offset))
                            current_note_type = 4
                        current_note_height = y
                    else:
                        lift_note_counter += 1
                    break

                else:
                    lift_note_counter = 0
            else:
                if current_note_type:
                    element_queue.put((current_note_type, lane_num, perf_counter()+offset))
                    current_note_height = 99999

    # with mss.mss() as sct:
    #     lane_capture_dimensions = dec_to_px(sct, 1, 0.447, 0.3927, 0.201, 0.1)
    #
    #     highway_activity_left_dimensions = dec_to_px(sct, 1, 0.985, 0.277, 0.0, 0.008)
    #     highway_activity_right_dimensions = dec_to_px(sct, 1, 0.985, 0.731, 0.0, 0.008)
    #
    #     while True:  # GAME LOOP
    #         while not is_highway_active(sct, highway_activity_left_dimensions, highway_activity_right_dimensions):
    #             sleep(0.1)
    #
    #         lane_capture = np.array(sct.grab(lane_capture_dimensions))
    #
    #         for height, row in enumerate(reversed(lane_capture)):
    #             h, s, v = rgb_to_hsv(*row[0])
    #
    #             # Purple Note
    #             if 0.84 < h < 0.855 and \
    #                     0.94 < s and \
    #                     220 < v < 245:
    #                 if next_element_type:
    #                     if element_height_in_previous_frame < height:
    #                         element_queue.put((next_element_type, 2, perf_counter()+offset))
    #                         next_element_type = 1
    #                     element_height_in_previous_frame = height
    #                 else:
    #                     next_element_type = 1
    #                 break
    #
    #             # Orange Note
    #             elif 0.1 < h < 0.12 and \
    #                     0.9 < s and \
    #                     240 < v:
    #                 if next_element_type:
    #                     if element_height_in_previous_frame < height:
    #                         element_queue.put((next_element_type, 2, perf_counter()+offset))
    #                         next_element_type = 2
    #                     element_height_in_previous_frame = height
    #                 else:
    #                     next_element_type = 2
    #                 break
    #
    #             # Purple Lift Element
    #             elif 0.82 < h < 0.87 and \
    #                     0.03 < s < 0.22 and \
    #                     200 < v:
    #                 if lift_element_counter == 9:
    #                     if next_element_type:
    #                         if element_height_in_previous_frame < height:
    #                             element_queue.put((next_element_type, 2, perf_counter() + offset))
    #                             next_element_type = 3
    #                         element_height_in_previous_frame = height
    #                     else:
    #                         next_element_type = 3
    #                     break
    #                 else:
    #                     lift_element_counter += 1
    #
    #             # Orange Lift Element
    #             elif (h < 0.03 or h > 0.97) and \
    #                     0.06 < s < 0.2 and \
    #                     170 < v:
    #                 if lift_element_counter == 9:
    #                     if next_element_type:
    #                         if element_height_in_previous_frame < height:
    #                             element_queue.put((next_element_type, 2, perf_counter() + offset))
    #                             next_element_type = 4
    #                         element_height_in_previous_frame = height
    #                     else:
    #                         next_element_type = 4
    #                     break
    #                 else:
    #                     lift_element_counter += 1
    #
    #             # Background
    #             else:
    #                 lift_element_counter = 0
    #
    #         # For loop has not found an element
    #         else:
    #             if next_element_type:
    #                 element_queue.put((next_element_type, 2, perf_counter() + offset))
    #                 element_height_in_previous_frame = 500
    #                 next_element_type = 0
