from multiprocessing import Queue
import os
from time import perf_counter_ns
import csv
from colorsys import rgb_to_hsv
import dxcam
import numpy as np


class Lane:
    def __init__(self):
        self.latest_note_type = 0
        self.latest_note_height = 0
        self.pois = None

    def set_pois(self, pois):
        self.pois = pois
        return self

    def note_search(self, image):
        output_type = 0
        white_px_counter = 0
        for y, x in self.pois:
            match color_match(*rgb_to_hsv(*image[y, x])):
                case 1:
                    if y < self.latest_note_height - 2:
                        output_type = self.latest_note_type
                    self.latest_note_type = 1
                    self.latest_note_height = y
                    break

                case 2:
                    if y < self.latest_note_height - 2:
                        output_type = self.latest_note_type
                    self.latest_note_type = 2
                    self.latest_note_height = y
                    break

                case 3:
                    if white_px_counter == 9:
                        if y < self.latest_note_height - 2:
                            output_type = self.latest_note_type
                        self.latest_note_type = 3
                        self.latest_note_height = y
                        break
                    else:
                        white_px_counter += 1

                case 0:
                    white_px_counter = 0

        if output_type:
            self.latest_note_height = 0
            return output_type
        return 0


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


def color_match(h, s, v):
    # Purple Note
    if 0.825 < h < 0.877 and 0.93 < s and 109 < v < 130:
        return 1

    # Orange Note
    if 0.11 < h < 0.12 and 0.88 < s and 242 < v:
        return 2

    #  Lift Note
    if 0.09 < h and s < 0.07 and 230 < v:
        return 3

    return 0


def read_screen():
    lane1 = Lane().set_pois(line_algo(61, 29))
    lane2 = Lane().set_pois(line_algo(139, 122))
    lane3 = Lane().set_pois(line_algo(218, 216))
    lane4 = Lane().set_pois(line_algo(296, 310))
    lane5 = Lane().set_pois(line_algo(375, 406))
    lanes = [lane1, lane2, lane3, lane4, lane5]

    camera = dxcam.create(region=(728, 482, 1202, 582))
    camera.start()
    while True:
        image = camera.get_latest_frame()
        shot_time = perf_counter_ns()

        for number, lane in enumerate(lanes):
            if note_type := lane.note_search(image):
                # note_queue.put((note_type, number, shot_time))
                print(note_type, number, shot_time)

read_screen()
