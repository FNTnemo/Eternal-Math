#window
import os
import sys

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
HALF_WINDOW_WIDTH = WINDOW_WIDTH/2
HALF_WINDOW_HEIGHT = WINDOW_HEIGHT/2

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

scale_x, scale_y = WINDOW_WIDTH/CAMERA_WIDTH, WINDOW_HEIGHT/CAMERA_HEIGHT
TITLE = "Eternal Math"
TPS = 60

#map
sell_size = (64 * scale_x, 64 * scale_y)

#colors
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)