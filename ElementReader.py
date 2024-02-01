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


def dec_to_px(sct, monitor_number, top_dec, left_dec, width_dec, height_dec):
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


def read_elements(element_queue: Queue):
    with mss.mss() as sct:
        monitor_dimensions = dec_to_px(sct, 1, 0.447, 0.493, 0.0, 0.15)
        while True:
            sct_img = sct.grab(monitor_dimensions)

            cv.imshow("window", np.array(sct_img))

            release_note_counter = 0
            note_found = False

            for idx, row in enumerate(sct_img.pixels):
                h, s, v = colorsys.rgb_to_hsv(*row[0])

                # Purple Note
                if 0.9 < h < 0.92 and \
                        0.95 < s and \
                        104 < v < 111:
                    note_found = True

                # Orange Note ***not done****
                elif 0.045 < h < 0.055 and \
                        0.97 < s and \
                        224 < v < 235:
                    note_found = True

                # Release Note
                elif 0.82 < h < 0.87 and \
                        0.05 < s < 0.22 and \
                        210 < v:
                    if release_note_counter == 10:
                        print("release note")
                        element_queue.put((1, 2, idx/monitor_dimensions["height"]))
                    else:
                        release_note_counter += 1

                # Background
                else:
                    release_note_counter = 0
                    if note_found:
                        print("NOTE")
                        element_queue.put((0, 2, idx/monitor_dimensions["height"]))
                        note_found = False

            cv.waitKey()
            quit()
