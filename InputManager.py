from multiprocessing import Queue
from time import time, sleep
import pydirectinput as pdi


# game_element format: (lane number(0-4), element type(0-2), UTC for input)
def send_inputs(element_queue: Queue, bindings):
    #         pdi.press('a')
    #         pdi.press('s')
    #         pdi.press('d')
    #         pdi.click(button='left')
    #         pdi.click(button='right')
    #         counter += 1
    #         print(counter)
    counter = 0
    while True:
        lane, el_type, time1 = element_queue.get(block=True)
        counter += 1
        print(counter)

