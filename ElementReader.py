from time import sleep, perf_counter
import mss.tools
from colorsys import rgb_to_hsv
import cv2 as cv
import numpy as np
import pyautogui as pag
import dxcam


class AppState:
    def __init__(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            self.monitor_height = monitor['height']
            self.monitor_width = monitor['width']
        self.cap_left = int(self.monitor_width * 0.375)
        self.cap_top = int(self.monitor_height * 0.4463)
        self.cap_height = int(self.monitor_height * 0.1)
        self.cap_width = int(self.monitor_width * 0.255)
        self.cap_right = self.cap_left + self.cap_width
        self.cap_bottom = self.cap_top + self.cap_height

        self.highway_edge_idx = 0.0961, 0.0082, 0.8998, 0.9898

        self.lane_0_idx = None
        self.lane_1_idx = None
        self.lane_2_idx = None
        self.lane_3_idx = None
        self.lane_4_idx = None

        self.element_height_in_previous_frame = 500  # need to make dynamic
        self.next_element_type = 0
        self.lift_element_counter = 0
        self.offset = 0.52

    def get_cap_region(self):
        return self.cap_left, self.cap_top, self.cap_right, self.cap_bottom


# Bresenham's Line Algorithm
def compute_line_idx(cap_width, cap_height, dec_x0, dec_x1):
    x0 = int(dec_x0 * (cap_width-1))
    y0 = 0
    x1 = int(dec_x1 * (cap_width-1))
    y1 = cap_height-1

    indices = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while x0 != x1 or y0 != y1:
        indices.append((x0, y0))

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    indices.append((x1, y1))
    return indices


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


def find_color_range(image, idx):
    maxh = 0
    minh = 1
    maxs = 0
    mins = 1
    maxv = 0
    minv = 255
    for index in idx:
        x, y = index
        r, g, b = image[y, x]
        h, s, v = rgb_to_hsv(r, g, b)
        if h > maxh:
            maxh = h
        if h < minh:
            minh = h
        if s > maxs:
            maxs = s
        if s < mins:
            mins = s
        if v > maxv:
            maxv = v
        if v < minv:
            minv = v
        print(f"{r}, {g}, {b}")
    print(f"""
    maxh{maxh}
    minh{minh}
    maxs{maxs}
    mins{mins}
    maxv{maxv}
    minv{minv}
    """)


def highway_is_inactive(image, idx):
    for index in idx:
        x, y = index
        h, s, v = rgb_to_hsv(*image[y, x])
        if h < 0.7 or \
            s < 0.4 or \
            v < 58 or v > 110:
            return True
    return False


def initialization():
    def bresenham_line(x0, x1, dy):
        output = []
        dx = x1-x0
        xi = 1

        if dx < 0:
            xi -= 1
            dx *= -1

        D = (2*dx)-dy
        x = x0

        for y in range(dy):
            output.append((x, y))
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

    lane_1 = bresenham_line(cap_width*0.1, cap_width*0.1, cap_height)
    lane_2 = bresenham_line(cap_width * 0.1, cap_width * 0.1, cap_height)
    lane_3 = bresenham_line(cap_width * 0.1, cap_width * 0.1, cap_height)
    lane_4 = bresenham_line(cap_width * 0.1, cap_width * 0.1, cap_height)
    lane_5 = bresenham_line(cap_width * 0.1, cap_width * 0.1, cap_height)

    return ((cap_left, cap_top, cap_right, cap_bottom),
            (lane_1, lane_2, lane_3, lane_4, lane_5),
            activity)

# game_element format: (element type(0-2), lane number(0-4), 'perf_counter' time of action)
def read_elements(element_queue):
    cap_region, lane_indices, activity_indices = initialization()

    highway_idx = np.concatenate((compute_line_idx(cap_width, cap_height, 0.0913, 0),
                                  compute_line_idx(cap_width, cap_height, 0.9066, 1)))

    # lane0_idx = compute_line_idx(cap_width, cap_height, )
    # lane1_idx = compute_line_idx(cap_width, cap_height, )
    # lane2_idx = compute_line_idx(cap_width, cap_height, )
    # lane3_idx = compute_line_idx(cap_width, cap_height, )
    # lane4_idx = compute_line_idx(cap_width, cap_height, )

    camera = dxcam.create(region=(cap_left, cap_top, cap_right, cap_bottom))
    camera.start()
    while True:
        image = camera.get_latest_frame()

        while highway_is_inactive(image, highway_idx):
            print("hello")
            sleep(0.3)


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
