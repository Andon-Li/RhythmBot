import threading
from ElementReader import read_elements
from InputManager import send_inputs

game_element_list = []
list_lock = threading.Lock()

bindings = ['a', 's', 'd', 'm_l', 'm_r']

element_reader_thread = threading.Thread(target=read_elements, args=(game_element_list, list_lock), daemon=True)
input_manager_thread = threading.Thread(target=send_inputs, args=(game_element_list, list_lock, bindings), daemon=True)

input_manager_thread.start()
element_reader_thread.start()

input_manager_thread.join()
element_reader_thread.join()
