from multiprocessing import Process, Queue
from time import time, sleep
import pyautogui

# game_element format: (lane_number(0-4), element_type(0-2), timestamp)
# Element types:
#      0 Full note
#      1 Sustain note
#      2 Release element
#      3


def read_elements(element_queue):
    for _ in range(200):
        sleep(0.1)
        element_queue.put((0, 0, 0))

