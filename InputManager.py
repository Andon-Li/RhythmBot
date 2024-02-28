import time
from multiprocessing import Queue
from time import sleep, perf_counter
import pydirectinput as pdi


# game_element format: (element type(0-2), lane number(0-4), 'perf_counter' time of action)
def send_inputs(element_queue: Queue, bindings):
    pdi.PAUSE = 0.01
    while True:
        element_type, lane, time = element_queue.get()

        while perf_counter() < time:
            continue

        print(f"{element_type}, {lane}")
