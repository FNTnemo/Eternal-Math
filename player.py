import math

import pygame.image

import guns
from settings import *

class Player:
    selected_gun_index = 0
    guns = []

    def __init__(self, x0, y0, angle0, velocity):
        self.player_x = x0
        self.player_y = y0
        self.player_angle = angle0
        self.velocity = velocity

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.player_y -= self.velocity
        if keys[pygame.K_s]: self.player_y += self.velocity
        if keys[pygame.K_a]: self.player_x -= self.velocity
        if keys[pygame.K_d]: self.player_x += self.velocity

    def player_draw(self, screen):
        pygame.draw.rect(screen, white, pygame.Rect(self.player_x, self.player_y, 10, 10))
        pygame.draw.line(screen, green, (self.player_x, self.player_y), (pygame.mouse.get_pos()), 1)

    def add_gun(self, gun_type):
        self.guns.append(guns.Gun(gun_type))

    def get_selected_gun(self):
        return self.guns[self.selected_gun_index]

    def calc_player_angle(self):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        dx1, dy1 = mouse_pos_x - self.player_x, self.player_y - self.player_y
        dx2, dy2 = mouse_pos_x - self.player_x, mouse_pos_y - self.player_y
        if dx1 == 0: dx1 = 0.00001
        if dx2 == 0: dx2 = 0.00001
        k1, k2 = dy1/dx1, dy2/dx2
        if mouse_pos_x >= self.player_x:
            return math.atan(k2 - k1) / (1 + k1 * k2)
        else:
            return -(math.pi - math.atan(k2 - k1) / (1 + k1 * k2))

player = Player(10, 10, 0, 5) #create player