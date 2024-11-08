import pygame.display

from settings import HALF_WINDOW_WIDTH, HALF_WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from map import map1


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
        self.camera_box_borders = {"left": 600, "right": 600, "top": 300, "bottom": 300}

        self.left = self.camera_box_borders["left"]
        self.top = self.camera_box_borders["top"]
        self.width = WINDOW_WIDTH - (self.camera_box_borders["left"] + self.camera_box_borders["right"])
        self.height = WINDOW_HEIGHT - (self.camera_box_borders["top"]  + self.camera_box_borders["bottom"])
        self.camera_box_rect = pygame.Rect(self.left, self.top, self.width, self.height)

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

        if self.camera_box_rect.right + self.left <= map1.get_map_size()[0] + 2:
            self.offset.x = max(0, self.camera_box_rect.left - self.camera_box_borders["left"])
        if self.camera_box_rect.bottom + self.top <= map1.get_map_size()[1] + 2:
            self.offset.y = max(0, self.camera_box_rect.top - self.camera_box_borders["top"])

camera = Camera()
