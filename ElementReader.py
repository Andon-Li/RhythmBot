from multiprocessing import Process, Queue
from time import time, sleep
import win32gui
import pygetwindow

# game_element format: (lane_number(0-4), element_type(0-1), timestamp)
# Element types:
# Down note
# Release


def read_elements(element_queue):
    window = pygetwindow.getWindowsWithTitle("Fortnite")[0]

    print(window)
    print(window.topleft)
    print(window.bottomright)



