import time
from multiprocessing import Queue
from time import sleep, perf_counter
import pydirectinput as pdi


# game_element format: (lane number(0-4), element type(0-2), 'perf_counter' time of action)
def send_inputs(element_queue: Queue, bindings):
    while True:
        element = element_queue.get()
        while perf_counter() < element[2]:
            sleep(0.01)

        pdi.keyDown('d')