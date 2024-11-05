import math
import pygame.image

import guns
from guns import gun_types
from settings import *

class Player:
    selected_gun_index = -1
    guns = []

    def __init__(self, x0, y0, velocity):
        self.player_x = x0 #координаты
        self.player_y = y0
        self.velocity = velocity #скорость игока

    def movement(self): #перемещение игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.player_y -= self.velocity
        if keys[pygame.K_s]: self.player_y += self.velocity
        if keys[pygame.K_a]: self.player_x -= self.velocity
        if keys[pygame.K_d]: self.player_x += self.velocity

    def switch_gun(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1] and self.selected_gun_index - 1 >= 0: self.selected_gun_index -= 1
        if keys[pygame.K_3] and self.selected_gun_index + 1 < len(self.guns): self.selected_gun_index += 1

    def player_draw(self, screen): #отрисовка игрока
        pygame.draw.rect(screen, white, pygame.Rect(self.player_x, self.player_y, 10, 10))
        pygame.draw.line(screen, green, (self.player_x, self.player_y), (pygame.mouse.get_pos()), 1)

    def add_gun(self, gun_type_str): #выдать игроку пушку
        for gun_type in gun_types:
            if gun_type[1] == gun_type_str:
                self.guns.append(guns.Gun(gun_type))
                self.selected_gun_index += 1
                break

    def get_selected_gun(self): #функция, которая возвращает пушку, которая в руках
        if self.selected_gun_index > -1:
            return self.guns[self.selected_gun_index]

    def calc_player_angle(self): #угол между направлением взгляда и прямой y = player_x
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

player = Player(10, 10, 5) #create player