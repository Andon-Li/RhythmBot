from time import time, sleep
import pyautogui

# game_element format: (lane_number(0-4), element_type(0-2), timestamp)
def read_elements(game_element_list, list_lock):
    for i in range(100):
        sleep(0.1)
        with list_lock:
            game_element_list.append((0, 0, time()))
