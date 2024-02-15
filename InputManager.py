import time
from multiprocessing import Queue
from time import sleep, perf_counter
import pydirectinput as pdi


# game_element format: (element type(0-2), lane number(0-4), 'perf_counter' time of action)
def send_inputs(element_queue: Queue, bindings, print_queue):
    while True:
        element_type, lane, time = element_queue.get()

        while perf_counter() < time:
            continue

        match element_type:
            case 1:
                print_queue.put("Purple Note")
            case 2:
                print_queue.put("Orange Note")
            case 3:
                print_queue.put("Purple Lift Element")
            case 4:
                print_queue.put("Orange Lift Element")