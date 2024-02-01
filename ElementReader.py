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


def dec_to_px(sct, monitor_number, top_dec, left_dec, width_dec=0.0, height_dec=0.0):
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
    with (mss.mss() as sct):
        monitor_dimensions = dec_to_px(sct, 1, 0.447, 0.493, 0.0, 0.15)
        while True:
            sct_img = sct.grab(monitor_dimensions)

            cv.imshow("window", np.array(sct_img))

            release_note_counter = 0
            note_found = False

            for row in sct_img.pixels:

                # row is a tuple, containing pixel elements
                pixel_hsv = colorsys.rgb_to_hsv(*row[0])

                # Purple Note
                if 0.9 < pixel_hsv[0] < 0.92 and \
                        0.95 < pixel_hsv[1] and \
                        104 < pixel_hsv[2] < 111:
                    note_found = True

                # Orange Note ***not done****
                elif 0.9 < pixel_hsv[0] < 0.92 and \
                        0.95 < pixel_hsv[1] and \
                        104 < pixel_hsv[2] < 111:
                    note_found = True

                # Release Note
                elif 0.82 < pixel_hsv[0] < 0.87 and \
                        0.05 < pixel_hsv[1] < 0.22 and \
                        210 < pixel_hsv[2]:
                    if release_note_counter == 10:
                        print("release note")
                        element_queue.put(())
                    else:
                        release_note_counter += 1
                else:
                    release_note_counter = 0
                    if note_found:
                        print("NOTE")
                        element_queue.put((0, 2, ))
                        note_found = False

            cv.waitKey()
            quit()


read_elements(None)
