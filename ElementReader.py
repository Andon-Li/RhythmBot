from multiprocessing import Process, Queue
from time import time, sleep
import pyautogui

# game_element format: (lane_number(0-4), element_type(0-1), timestamp)
# Element types:
# Down note
# Release


def read_elements(element_queue):
    while True:

