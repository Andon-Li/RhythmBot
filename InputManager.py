import time
from multiprocessing import Queue
from time import sleep, perf_counter
import pydirectinput as pdi


# game_element format: (lane number(0-4), element type(0-2), 'perf_counter' time of action)
def send_inputs(element_queue: Queue, bindings, print_queue):
    while True:
        element_type, lane, time = element_queue.get()

        while perf_counter() < time:
            continue

        if element_type == 0 or element_type == 1:
            pdi.keyDown('d')
            pdi.keyUp('d')
