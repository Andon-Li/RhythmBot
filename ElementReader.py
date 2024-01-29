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


def grab_image_by_decimal(sct, monitor_number, top_dec, left_dec, width_dec=0.0, height_dec=0.0):
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
    return sct.grab({"top": top_px,
                     "left": left_px,
                     "width": width_px,
                     "height": height_px,
                     "mon": monitor_number})


def read_elements(element_queue):
    with mss.mss() as sct:
        for _ in range(1000):
            sct_img = grab_image_by_decimal(sct, 1, 0.46, 0.877, 0.0, 0.0)

            mss.tools.to_png(sct_img.rgb, sct_img.size, output="output.png")
            h, s, v = colorsys.rgb_to_hsv(*sct_img.pixels[0][0])
            # if 0.89 < h < 0.91 and 0.98 < s and 0.42 < v < 0.43:
                # print("NOTE FOUND")
            # elif 0.86 < h < 0.87 and s < 0.09 and 0.98 < v:
                # print("SUSTAIN FOUND")
            # else:
                # print("----------------")

for _ in range(10000):
    read_elements(None)
