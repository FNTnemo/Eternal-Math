import math
import pygame

from entities.tile import collide_tiles
from entities.images import get_bullet_img, enemy_projectile_group, gun_images
from entities.images import player_projectile_group

#gun types кортеж(тип пушки, тип пули, скоростельность, задержка, обойма, задержка перезарядки)
gun_types = {"standard": ("standard", ("standard", 1, 15), True, 10, 15, 50),
             "laser": ("laser", ("laser", 3, 25), False, 0, 5, 70)}
#bullet types кортеж(тип, урон, скорсть)

all_guns = []
class Gun():
    def __init__(self, type, user):
        scale = 0.1
        self.type = type # тип оружия = тип пули
        gun_image = gun_images[self.type[0].split("_")[0]]
        self.original_image = pygame.transform.scale(gun_image.convert_alpha(), (gun_image.get_size()[0] * scale, gun_image.get_size()[1] * scale))
        self.image = self.original_image#картинка пушки
        self.rect = self.image.get_rect(center=user.rect.center)

        self.bullet_type = type[1] #кортеж(картинка, тип, урон, скорсть)
        self.rate_of_fire = type[2] #True/False скорострельность (возможность стрелять неотпуская кнопку)
        self.start_ammo_delay = type[3] #задержка между пулями
        self.ammo = type[4] #максимальный боезапас
        self.start_reload_delay = type[5] #задержка перезарядки

        self.max_ammo = self.ammo
        self.reload_delay = 0
        self.ammo_delay = 0
        self.can_shot = True

        self.flipped = False

        self.user = user

    def update(self):
        self.rect.center = self.user.rect.center
        gun_angle = math.degrees(self.user.calc_angle())
        if gun_angle >= 0 or abs(gun_angle) <= 90:
            self.image = pygame.transform.rotate(self.original_image, 360 - gun_angle)
        elif gun_angle < 0:
            self.image = pygame.transform.flip(pygame.transform.rotate(self.original_image, gun_angle - 360), False, True)

    def reload(self): #перезарядка
        keys = pygame.key.get_pressed()
        if self.reload_delay <= 0:
            from player.player import player
            if self.user != player or keys[pygame.K_r]:
                self.ammo = self.max_ammo

                self.reload_delay = self.start_reload_delay
        else:
            self.reload_delay -= 1

    def fire(self): #функция выстрела (пипец я её долго говнокодил)
        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()
        if self.ammo_delay <= 0:
            from player.player import player
            if (keys[pygame.K_SPACE] or buttons[0] or self.user != player) and self.reload_delay <= 0 < self.ammo and (self.can_shot or self.rate_of_fire):
                angle = self.user.calc_angle()
                new_bullet = Projectile(self.bullet_type, (self.user.rect.center[0], self.user.rect.center[1]),
                                        (self.bullet_type[2] * math.cos(angle), self.bullet_type[2] * math.sin(angle)), self.user)
                all_projectiles.append(new_bullet)
                if self.user == player:
                    player_projectile_group.add(new_bullet)
                else:
                    enemy_projectile_group.add(new_bullet)
                self.ammo -= 1
                self.ammo_delay = self.start_ammo_delay
                self.can_shot = False
            elif self.can_shot == False and not (keys[pygame.K_SPACE] or buttons[0]):
                self.can_shot = True
        else:
            self.ammo_delay -= 1

    def efire(self):
        angle = self.user.calc_angle()
        new_bullet = Projectile(self.bullet_type, (self.user.rect.center[0], self.user.rect.center[1]),
                                (self.bullet_type[2] * math.cos(angle), self.bullet_type[2] * math.sin(angle)),
                                self.user)
        all_projectiles.append(new_bullet)
        enemy_projectile_group.add(new_bullet)

all_projectiles = [] #список со всеми пулями на карте
class Projectile(pygame.sprite.Sprite):
    def __init__(self, type, pos, velocity, sender):
        pygame.sprite.Sprite.__init__(self)
        self.type = type[0]  # тип оружия = тип пули
        img = get_bullet_img(self.type).convert_alpha() #стандартная картинка
        self.image = pygame.transform.rotate(pygame.transform.scale(img, (img.get_size()[0] * 0.25, img.get_size()[1] * 0.25)), 180 - math.degrees(sender.calc_angle()))    # увеличеная картинка пули
        self.rect = self.image.get_rect(center=(pos[0], pos[1])) #поверхность для картинки

        self.damage = type[1] #тип пули = тип оружия
        self.velocity_vec = type[2] #длинна вектора скорости
        self.velocity_x = velocity[0] #скорость пули по х (высчитывается автоматичеки)
        self.velocity_y = velocity[1]# скорость пули по у (высчитывается автоматичеки)

        self.sender = sender

    def remove(self):
        all_projectiles.remove(self)
        player_projectile_group.remove(self)
        enemy_projectile_group.remove(self)

    def is_collide(self, group):
        for sprite in group:
            if self.rect.colliderect(sprite):
                return True

    def get_collide_rect(self, group):
        collide_rects = []
        for sprite in group:
            if self.rect.colliderect(sprite):
                collide_rects += sprite
        return collide_rects

    def movement(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        if self.is_collide(collide_tiles):
            self.remove()

    def get_type(self):
        return self.type

def draw_bullets(screen): #отрисовка пуль
    from player.camera import camera
    for bullet in all_projectiles:
        pygame.draw.circle(screen, "red", (bullet.rect.x - camera.offset.x, bullet.rect.y - camera.offset.y), 10)
