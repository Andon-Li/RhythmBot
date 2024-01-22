from time import sleep
import pydirectinput as pdi


# game_element format: (lane_number(0-4), element_type(0-2), timestamp)
def send_inputs(game_element_list, list_lock, bindings):
    counter = 0
    while True:
        if not game_element_list:
            continue
        with list_lock:
            latest_element = game_element_list.pop(0)
            pdi.press('a')
            pdi.press('s')
            pdi.press('d')
            pdi.click(button='left')
            pdi.click(button='right')
            counter += 1
            print(counter)
