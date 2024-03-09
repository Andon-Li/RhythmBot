from multiprocessing import Process, Queue
from ElementReader3 import read_screen
from InputManager import send_inputs

if __name__ == '__main__':
    element_queue = Queue(maxsize=500)
    print_queue = Queue(maxsize=500)

    bindings = ['a', 's', 'd', 'm_l', 'm_r']

    element_reader_process = Process(target=read_screen, args=(element_queue,), daemon=True)
    input_manager_process = Process(target=send_inputs)

    element_reader_process.start()
    input_manager_process.start()

    input_manager_process.join()
    element_reader_process.join()
