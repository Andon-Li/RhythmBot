from multiprocessing import Queue
from time import time, sleep
import pydirectinput as pdi


# game_element format: (lane number(0-4), element type(0-2), UTC for input)
def send_inputs(element_queue: Queue, bindings):
    while True:
        pass
