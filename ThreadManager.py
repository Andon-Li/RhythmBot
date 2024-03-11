from multiprocessing import Process, Queue
from ElementReader3 import read_screen
from InputManager import send_inputs

if __name__ == '__main__':
    element_queue = Queue(maxsize=500)

    element_reader_process = Process(target=read_screen, args=(element_queue,), daemon=True)
    element_reader_process.start()



