import math
import pygame

import guns
from guns import gun_types
from player.camera import camera
from settings import *
from entities.entities import player_img
from entities.entities import player_group

class Player(pygame.sprite.Sprite):
    selected_gun_index = -1
    guns = []

    def __init__(self, pos, size, velocity, group):
        super().__init__(player_group)
        self.image = pygame.transform.scale(player_img.convert_alpha(),(player_img.get_size()[0] * size, player_img.get_size()[1] * size))
        self.rect = self.image.get_rect(midbottom=(pos[0],pos[1]))

        self.velocity = velocity #скорость игока
        self.size = (self.image.get_size()[0], self.image.get_size()[1])

        self.gun_delta = (self.size[0]/2, self.size[1]/2)

    def movement(self): #перемещение игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.rect.y -= self.velocity
        if keys[pygame.K_s]: self.rect.y += self.velocity
        if keys[pygame.K_a]: self.rect.x -= self.velocity
        if keys[pygame.K_d]: self.rect.x += self.velocity

    def switch_gun(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1] and self.selected_gun_index - 1 >= 0: self.selected_gun_index -= 1
        if keys[pygame.K_3] and self.selected_gun_index + 1 < len(self.guns): self.selected_gun_index += 1

    def player_angle_debug_draw(self, screen): #отрисовка игрока
        pygame.draw.line(screen, green, (self.rect.center[0] - camera.offset.x, self.rect.center[1] - camera.offset.y), (pygame.mouse.get_pos()), 1) #линия от игрока до мышки

    def add_gun(self, gun_type_str): #выдать игроку пушку
        for gun_type in gun_types:
            if gun_type[0] == gun_type_str:
                new_gun = guns.Gun(gun_type)
                self.guns.append(new_gun)
                self.selected_gun_index += 1
                break

    def get_selected_gun(self): #функция, которая возвращает пушку, которая в руках
        if self.selected_gun_index > -1:
            return self.guns[self.selected_gun_index]

    def calc_player_angle(self): #угол между направлением взгляда и прямой y = player_x (сложная формула из интернета)
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        dx1, dy1 = mouse_pos_x - (self.rect.center[0] - camera.offset.x), 0
        dx2, dy2 = mouse_pos_x - (self.rect.center[0] - camera.offset.x), mouse_pos_y - (self.rect.center[1] - camera.offset.y)
        if dx1 == 0: dx1 = 0.0000001
        if dx2 == 0: dx2 = 0.0000001
        k1, k2 = dy1/dx1, dy2/dx2
        rad = (k2 - k1) / (1 + k1 * k2)
        if mouse_pos_x >= self.rect.center[0] - camera.offset.x:
            return math.atan(rad)
        else:
            return -(math.pi - math.atan(rad))

player = Player((200, 200), 5, 5, player_group) #create player