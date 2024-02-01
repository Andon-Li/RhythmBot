from multiprocessing import Queue
from time import time, sleep
import pydirectinput as pdi


# game_element format: (lane number(0-4), element type(0-2), decimal_for_height_location)
def send_inputs(element_queue: Queue, bindings):
    element = element_queue.get()
    print(element)





