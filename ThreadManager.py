from multiprocessing import Process, Queue
from ElementReader import read_elements
from InputManager import send_inputs

if __name__ == '__main__':
    element_queue = Queue(maxsize=100)

    bindings = ['a', 's', 'd', 'm_l', 'm_r']

    element_reader_process = Process(target=read_elements, args=(element_queue,))
    input_manager_thread = Process(target=send_inputs, args=(element_queue, bindings))

    element_reader_process.start()
    input_manager_thread.start()

    element_reader_process.join()
    input_manager_thread.join()
