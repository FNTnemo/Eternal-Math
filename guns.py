import math
import pygame

from settings import *

#gun types кортеж(картинка, тип, скоростельность, задержка, обойма, задержка перезарядки)
gun_types = [("path", "standard", True, 10, 15, 50), ("path", "laser", False, 20, 5, 70)]

#bullet types кортеж(картинка, тип, урон, скорсть)
bullet_types = [("path", "standard", 15, 10), ("path", "laser", 30, 20)]

class Gun:
    def __init__(self, type):
        self.img = type[0] #картинка пушки
        self.type = type[1] #тип оружия = тип пули
        self.rate_of_fire = type[2] #True/False скорострельность (возможность стрелять неотпуская кнопку)
        self.start_ammo_delay = type[3] #задержка между пулями
        self.ammo = type[4] #максимальный боезапас
        self.start_reload_delay = type[5] #задержка перезарядки

        self.max_ammo = self.ammo
        self.reload_delay = 0
        self.ammo_delay = 0

    def reload(self):
        keys = pygame.key.get_pressed()
        if self.reload_delay <= 0:
            if keys[pygame.K_r]:
                self.ammo = self.max_ammo
                self.reload_delay = self.start_reload_delay
        else:
            self.reload_delay -= 1
            print(self.reload_delay)

    def fire(self): #функция выстрела
        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()
        bullet_type = ("none", "none", 0, 0)
        if self.ammo_delay <= 0:
            if (keys[pygame.K_SPACE] or buttons[0]) and self.reload_delay <= 0 and self.ammo > 0:
                from player.player import player

                for bullet in bullet_types:
                    if bullet[1] == self.type:
                        bullet_type = bullet

                angle = player.calc_player_angle()
                new_bullet = Bullet(bullet_type, (player.player_x, player.player_y),
                                    (bullet_type[3] * math.cos(angle), bullet_type[3] * math.sin(angle)))
                all_bullets.append(new_bullet)
                self.ammo -= 1
                self.ammo_delay = self.start_ammo_delay
        else:
            self.ammo_delay -= 1

all_bullets = [] #список со всеми пулями на карте
class Bullet:
    def __init__(self, type, pos, velocity):
        self.img = type[0] #путть до картинки
        self.type = type[1] #урон от пули
        self.damage = type[2] #тип пули = тип оружия
        self.velocity_vec = type[3] #длинна вектора скорости
        self.velocity_x = velocity[0] #скорость пули по х (высчитывается автоматичеки)
        self.velocity_y = velocity[1]# скорость пули по у (высчитывается автоматичеки)

        self.x = pos[0] #координаты
        self.y = pos[1]

    def get_type(self):
        return type

def draw_bullets(screen): #отррисовка пуль
    for bullet in all_bullets:
        if bullet.type == "laser":
            pygame.draw.circle(screen, red, (bullet.x, bullet.y), 10)
        else:
            pygame.draw.circle(screen, blue, (bullet.x, bullet.y), 10)

def bullets_movement(): #перемещение пуль
    for bullet in all_bullets:
        bullet.x += bullet.velocity_x
        bullet.y += bullet.velocity_y