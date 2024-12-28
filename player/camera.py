import pygame.display

from map import get_map_size, get_loaded_map
from settings import *


#       \_______/
#   `.,-'\_____/`-.,'
#    /`..'\ _ /`.,'\
#   /  /`.,' `.,'\  \
#  /__/__/     \__\__\__
#  \  \  \     /  /  /
#   \  \,'`._,'`./  /
#    \,'`./___\,'`./
#   ,'`-./_____\,-'`.
#       /       \

class Camera:
    def __init__(self):
        self.display_serf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.camera_box_borders = {"left": 500, "right": 500, "top": 200, "bottom": 200}

        self.left = self.camera_box_borders["left"]
        self.top = self.camera_box_borders["top"]
        self.width = WINDOW_WIDTH - (self.camera_box_borders["left"] + self.camera_box_borders["right"])
        self.height = WINDOW_HEIGHT - (self.camera_box_borders["top"]  + self.camera_box_borders["bottom"])
        self.camera_box_rect = pygame.Rect(self.left, self.top, self.width, self.height)

        #camera shake
        self.camera_shake_offset = pygame.math.Vector2

    def center_camera(self, target):
        self.offset.x = target.rect.center[0] - HALF_WINDOW_WIDTH
        self.offset.y = target.rect.center[1] - HALF_WINDOW_HEIGHT

    def center_box_camera(self, target):
        if target.rect.left < self.camera_box_rect.left:
            self.camera_box_rect.left = target.rect.left
        if target.rect.right > self.camera_box_rect.right:
            self.camera_box_rect.right = target.rect.right
        if target.rect.top < self.camera_box_rect.top:
            self.camera_box_rect.top = target.rect.top
        if target.rect.bottom > self.camera_box_rect.bottom:
            self.camera_box_rect.bottom = target.rect.bottom

        if self.camera_box_rect.right + self.left <= get_map_size(get_loaded_map())[0] + 2:
            self.offset.x = max(0, self.camera_box_rect.left - self.camera_box_borders["left"])
        if self.camera_box_rect.bottom + self.top <= get_map_size(get_loaded_map())[1] + 2:
            self.offset.y = max(0, self.camera_box_rect.top - self.camera_box_borders["top"])

    def camera_shake(self, max_offset_x, max_offset_y):
        self.camera_shake_offset.x += 1

camera = Camera()
