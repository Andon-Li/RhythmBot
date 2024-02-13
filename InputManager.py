import time
from multiprocessing import Queue
from time import sleep, perf_counter
import pydirectinput as pdi


# game_element format: (lane number(0-4), element type(0-2), 'perf_counter' time of action)
def send_inputs(element_queue: Queue, bindings, print_queue):
    note_number = 0
    lift_number = 0
    while True:
        element_type, lane, time = element_queue.get()

        while perf_counter() < time:
            continue

        if element_type == 0 or element_type == 1:
            note_number += 1
        else:
            lift_number += 1

        print_queue.put("note " + str(note_number))
        print_queue.put("lift " + str(lift_number))
