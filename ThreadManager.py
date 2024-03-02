from multiprocessing import Process, Queue
from ElementReader import main
from InputManager import send_inputs

if __name__ == '__main__':
    element_queue = Queue(maxsize=500)
    print_queue = Queue(maxsize=500)

    bindings = ['a', 's', 'd', 'm_l', 'm_r']

    element_reader_process = Process(target=main, args=(element_queue,), daemon=True)
    input_manager_thread = Process(target=send_inputs, args=(element_queue, bindings), daemon=True)

    element_reader_process.start()
    input_manager_thread.start()

    element_reader_process.join()
    input_manager_thread.join()
