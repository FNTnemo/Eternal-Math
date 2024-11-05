import math

import pygame
from pygame.time import delay

from settings import *

#gun types
standard_pistol = ("path", "standard", True, 10, 15)

#bullet types
standard_bullet = ("path", "standard", 15, 10)

class Gun:
    def __init__(self, type):
        self.img = type[0] #картинка пушки
        self.type = type[1] #максимальный боезапас
        self.rate_of_fire = type[2] #True/False скорострельность (возможность стрелять неотпуская кнопку)
        self.delay = type[3] #задержка между пулями
        self.ammo = type[4] #тип оружия = тип пули

        self.start_delay = self.delay

    def fire(self):
        keys = pygame.key.get_pressed()
        if self.delay <= 0:
            if keys[pygame.K_SPACE] and self.ammo > 0:
                from player import player
                angle = player.calc_player_angle()
                new_bullet = Bullet(standard_bullet, (player.player_x, player.player_y),
                                    (standard_bullet[3] * math.cos(angle), standard_bullet[3] * math.sin(angle)))
                all_bullets.append(new_bullet)
                self.ammo -= 1
                self.delay = self.start_delay
        else:
            self.delay -= 1

    def get_type(self):
        return type

all_bullets = []
class Bullet:
    def __init__(self, type, pos, velocity):
        self.img = type[0]
        self.type = type[1] #урон от пули
        self.damage = type[2] #тип пули = тип оружия
        self.velocity_vec = type[3]
        self.velocity_x = velocity[0]
        self.velocity_y = velocity[1]# скорость пули

        self.x = pos[0]
        self.y = pos[1]

    def get_type(self):
        return type

def draw_bullets(screen):
    for bullet in all_bullets:
        pygame.draw.circle(screen, blue, (bullet.x, bullet.y), 10)

def bullets_movement():
    for bullet in all_bullets:
        bullet.x += bullet.velocity_x
        bullet.y += bullet.velocity_y