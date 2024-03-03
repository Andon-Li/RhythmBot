from colorsys import rgb_to_hsv
from time import perf_counter, time_ns
import dxcam
import csv
import os

def note_thinker(image, pixel_locs: tuple[int, int, int]) -> str:
    def color_match(rgb_val: tuple[int, int, int]) -> int:
        h, s, v = rgb_to_hsv(*rgb_val)

        if s < .12 and 250 < v:
            return 1  # white
        if 0.846<h<0.863 and 0.97<s and 110<v<135:
            return 2  # purple
        if 0.04<h<0.07 and 0.92<s and 215<v:
            return 3  # orange
        if <h< and <s< and <v<:
        return 0  # no match

    match color_match(image[pixel_locs[0]]):
        case 1:
            if (not color_match(image[pixel_locs[1]])) and (color_match(image[pixel_locs[2]])):
                    return 'lift'
            else:
                return 'sustain'
        case 2:
            return 'purple'
        case 3:
            return 'orange'
        case 0:
            return 'background'


def main():
    song_map = []
    #            cent, edge, lift
    lanes_pois = ((53, 74, 69),
                  (140, 169, 162),
                  (234, 265, 257),
                  (327 , 304, 308),
                  (420, 451, 399))

    camera = dxcam.create(region=(728, 579, 1201, 580))
    camera.start()

    while True:
        image = camera.get_latest_frame()
        shot_time = perf_counter()

        if len(song_map) > 500:
            break

        for lane_num, lane_poi in enumerate(lanes_pois):
            note_type = note_thinker(image, lane_poi)
            song_map.append([note_type, lane_num, shot_time])

    if not os.path.exists('song_maps'):
        os.makedirs('song_maps')

    with open(f'song_maps\\{time_ns()}', 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(song_map)


main()
