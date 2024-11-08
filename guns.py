import math
import pygame

from player.camera import camera
from settings import *
from entities.entities import get_bullet_img
from entities.entities import player_bullets, enemy_bullets

#gun types кортеж(картинка, тип пушки, тип пули, скоростельность, задержка, обойма, задержка перезарядки)
gun_types = [("standard", ("standard", 15, 10), True, 10, 15, 50),
             ("laser", ("laser", 30, 20), False, 0, 5, 70)]
#bullet types кортеж(картинка, тип, урон, скорсть)



class Gun():
    def __init__(self, type):
        self.type = type[0]  # тип оружия = тип пули
        #self.image = get_bullet_img(self.type) #картинка пушки
        #self.rect = self.image.get_rect(topleft=())

        self.bullet_type = type[1] #кортеж(картинка, тип, урон, скорсть)
        self.rate_of_fire = type[2] #True/False скорострельность (возможность стрелять неотпуская кнопку)
        self.start_ammo_delay = type[3] #задержка между пулями
        self.ammo = type[4] #максимальный боезапас
        self.start_reload_delay = type[5] #задержка перезарядки

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
                new_bullet = Bullet(self.bullet_type, (player.rect.center[0], player.rect.center[1]),
                                    (self.bullet_type[2] * math.cos(angle), self.bullet_type[2] * math.sin(angle)))
                all_bullets.append(new_bullet)
                player_bullets.add(new_bullet)
                self.ammo -= 1
                self.ammo_delay = self.start_ammo_delay
                self.can_shot = False
            elif self.can_shot == False and not (keys[pygame.K_SPACE] or buttons[0]):
                self.can_shot = True
        else:
            self.ammo_delay -= 1

all_bullets = [] #список со всеми пулями на карте
class Bullet(pygame.sprite.Sprite):
    def __init__(self, type, pos, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.type = type[0]  # тип оружия = тип пули
        img = get_bullet_img(self.type).convert_alpha() #стандартная картинка
        self.image = pygame.transform.scale(img, (img.get_size()[0] * 8, img.get_size()[1] * 8))   # увеличеная картинка пули
        self.rect = self.image.get_rect(center=(pos[0], pos[1])) #поверхность для картинки

        self.damage = type[1] #тип пули = тип оружия
        self.velocity_vec = type[2] #длинна вектора скорости
        self.velocity_x = velocity[0] #скорость пули по х (высчитывается автоматичеки)
        self.velocity_y = velocity[1]# скорость пули по у (высчитывается автоматичеки)

    def remove(self):
        all_bullets.remove(self)
        player_bullets.remove(self)

    def get_type(self):
        return type

def draw_bullets(screen): #отрисовка пуль
    for bullet in all_bullets:
        pygame.draw.circle(screen, "red", (bullet.rect.x - camera.offset.x, bullet.rect.y - camera.offset.y), 10)

def bullets_movement(): #перемещение пуль
    for bullet in all_bullets:
        bullet.rect.x += bullet.velocity_x
        bullet.rect.y += bullet.velocity_y
        #удаление пуль, улетевших за край экрана
        if bullet.rect.x - camera.offset.x < 0 or bullet.rect.x - camera.offset.x > WINDOW_WIDTH:
            bullet.remove()
        elif bullet.rect.y - camera.offset.y < 0 or bullet.rect.y - camera.offset.y > WINDOW_HEIGHT:
            bullet.remove()
