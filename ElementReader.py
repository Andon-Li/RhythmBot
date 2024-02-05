import multiprocessing
import timeit
from multiprocessing import Process, Queue
from time import time, sleep
import win32gui
import pygetwindow as pgw
import mss.tools
import PIL.Image
import colorsys
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
    pixels = sct.grab(left_dimensions)[0] + sct.grab(right_dimensions)[0]
    for pixel in pixels:
        h, s, v = colorsys.rgb_to_hsv(*pixel)
        if (h > 0.73 or h < 0.78) and \
                (s > 0.9) and \
                (v > 0.22 or v < 0.26):
            return False

    return True


def new_read_func(element_queue: Queue):
    with mss.mss() as sct:
        lane_2_px_dimensions = dec_to_px(sct, 1, 0.447, 0.493, 0.0, 0.05)

        highway_activity_left_dimensions = dec_to_px(sct, 1, 0.985, 0.276, 0.0, 0.008)
        highway_activity_right_dimensions = dec_to_px(sct, 1, 0.985, 0.731, 0.0, 0.008)

        while not is_highway_active(sct, highway_activity_left_dimensions, highway_activity_right_dimensions):
            sleep(0.1)




def read_elements(element_queue: Queue):
    with mss.mss() as sct:
        monitor_dimensions = dec_to_px(sct, 1, 0.447, 0.493, 0.0, 0.05)
        while True:
            sct_img = sct.grab(monitor_dimensions)
            release_note_counter = 0
            note_found = False

            for idx, row in enumerate(sct_img.pixels):
                h, s, v = colorsys.rgb_to_hsv(*row[0])

                # Purple Note
                if 0.9 < h < 0.92 and \
                        0.95 < s and \
                        104 < v < 111:
                    note_found = True

                # Orange Note
                elif 0.045 < h < 0.055 and \
                        0.97 < s and \
                        224 < v < 235:
                    note_found = True

                # Release Note
                elif 0.82 < h < 0.87 and \
                        0.05 < s < 0.22 and \
                        210 < v:
                    if release_note_counter == 10:
                        element_queue.put((1, 2, idx/monitor_dimensions["height"]))
                    else:
                        release_note_counter += 1

                # Background
                else:
                    release_note_counter = 0
                    if note_found:
                        element_queue.put((0, 2, idx/monitor_dimensions["height"]))
                        note_found = False

