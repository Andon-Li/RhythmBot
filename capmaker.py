import cv2
import dxcam
from ElementReader3 import line_algo
from time import perf_counter_ns

camera = dxcam.create(region=(728, 482, 1202, 582))
camera.start()

image = camera.get_latest_frame()
for y, x in line_algo(97, 68):
    image[y, x] = (255, 255, 0)
for y, x in line_algo(139, 122):
    image[y, x] = (255, 255, 0)
for y, x in line_algo(218, 216):
    image[y, x] = (255, 255, 0)
for y, x in line_algo(296, 310):
    image[y, x] = (255, 255, 0)
for y, x in line_algo(375, 406):
    image[y, x] = (255, 255, 0)


image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
cv2.imwrite(f"caps\\capmaker_{perf_counter_ns()}.png", image)
