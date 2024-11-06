import math
import pygame

from settings import *

#gun types кортеж(картинка, тип пушки, тип пули, скоростельность, задержка, обойма, задержка перезарядки)
gun_types = [("path", "standard", ("path", "standard", 15, 10), True, 10, 15, 50),
             ("path", "laser", ("path", "laser", 30, 20), False, 0, 5, 70)]
#bullet types кортеж(картинка, тип, урон, скорсть)

class Gun:
    def __init__(self, type):
        self.img = type[0] #картинка пушки
        self.type = type[1] #тип оружия = тип пули
        self.bullet_type = type[2]
        self.rate_of_fire = type[3] #True/False скорострельность (возможность стрелять неотпуская кнопку)
        self.start_ammo_delay = type[4] #задержка между пулями
        self.ammo = type[5] #максимальный боезапас
        self.start_reload_delay = type[6] #задержка перезарядки

        self.max_ammo = self.ammo
        self.reload_delay = 0
        self.ammo_delay = 0
        self.can_shot = True

    def reload(self): #перезарядка
        keys = pygame.key.get_pressed()
        if self.reload_delay <= 0:
            if keys[pygame.K_r]:
                self.ammo = self.max_ammo
                self.reload_delay = self.start_reload_delay
        else:
            self.reload_delay -= 1

    def fire(self): #функция выстрела (пипец я её долго говнокодил)
        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()
        if self.ammo_delay <= 0:
            if (keys[pygame.K_SPACE] or buttons[0]) and self.reload_delay <= 0 < self.ammo and (self.can_shot or self.rate_of_fire):
                from player.player import player
                angle = player.calc_player_angle()
                new_bullet = Bullet(self.bullet_type, (player.x, player.y),
                                    (self.bullet_type[3] * math.cos(angle), self.bullet_type[3] * math.sin(angle)))
                all_bullets.append(new_bullet)
                self.ammo -= 1
                self.ammo_delay = self.start_ammo_delay
                self.can_shot = False
            elif self.can_shot == False and not (keys[pygame.K_SPACE] or buttons[0]):
                self.can_shot = True
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

    def remove(self):
        all_bullets.remove(self)

    def get_type(self):
        return type

def draw_bullets(screen): #отрисовка пуль
    for bullet in all_bullets:
        if bullet.type == "laser":
            pygame.draw.circle(screen, red, (bullet.x, bullet.y), 10)
        else:
            pygame.draw.circle(screen, blue, (bullet.x, bullet.y), 10)

def bullets_movement(): #перемещение пуль
    for bullet in all_bullets:
        bullet.x += bullet.velocity_x
        bullet.y += bullet.velocity_y
        #удаление пуль, улетевших за край экрана
        if bullet.x < 0 or bullet.x > WINDOW_WIDTH:
            bullet.remove()
        if bullet.y < 0 or bullet.y > WINDOW_HEIGHT:
            bullet.remove()
