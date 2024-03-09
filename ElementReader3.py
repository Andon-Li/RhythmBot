import os
from time import perf_counter_ns
import csv
from colorsys import rgb_to_hsv
import dxcam
import numpy as np

class Lane:
    def __init__(self, num: int):
        self.id = num
        self.latest_note_type = 0
        self.latest_note_height = 999
        self.pois = None

    def set_pois(self, pois):
        self.pois = pois
        return self

    def note_search(self):



def line_algo(x0: int, x1: int, y0: int = 0, y1: int = 99) -> np.array:
    output = []

    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    diff = (2 * dx) - dy
    x = x0

    for y in range(y1-y0+1):
        output.append([y, x])
        if diff > 0:
            x += xi
            diff += 2 * (dx - dy)
        else:
            diff += 2 * dx

    return np.flipud(np.array(output))


def color_match(h, s, v):  # returns (height of element, type of element)
    # Purple Note
    if < h < and < s < and < v < :
        return 1
    # Orange Note
    if < h < and < s < and < v < :
        return 2
    # Lift Note
    if  and < s < and < v < :
        return 3

    return 0


def read_screen():
    lane1 = Lane(1).set_pois(line_algo(97, 68))
    lane2 = Lane(2).set_pois(line_algo(139, 122))
    lane3 = Lane(3).set_pois(line_algo(218, 216))
    lane4 = Lane(4).set_pois(line_algo(296, 310))
    lane5 = Lane(5).set_pois(line_algo(375, 406))
    lanes = [lane1, lane2, lane3, lane4, lane5]

    camera = dxcam.create(region=(728, 482, 1202, 582))
    camera.start()
    image = camera.get_latest_frame()
    shot_time = perf_counter_ns()

    for lane in lanes:
        for y, x in lane.pois:
            if note_type := color_match(*rgb_to_hsv(*image[y, x])):
                pas


read_screen()
