from multiprocessing import Process, Queue
from time import time, sleep
import win32gui
import pygetwindow as pgw
import mss.tools

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
        sct_img = grab_image_by_decimal(sct, 2, 0.46, 0.4, 0.205, 0.0)

        mss.tools.to_png(sct_img.rgb, sct_img.size, output="output.png")
        print("-------------------")


read_elements(None)
