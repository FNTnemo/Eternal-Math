import math
import pygame

import guns
from entities.tile import collide_tiles
from guns import gun_types
from player.camera import camera
from settings import *
from entities.entities import player_stay_img, player_walking_images, collision
from entities.entities import player_group

class Player(pygame.sprite.Sprite):
    def __init__(self, hp, pos0, scale, velocity, group):
        super().__init__(group)
        self.image = player_stay_img.convert_alpha()
        self.image_size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (self.image_size[0] * scale, self.image_size[1] * scale))

        self.rect = self.image.get_rect(midbottom=(pos0[0],pos0[1]))
        self.size = (self.image.get_size()[0], self.image.get_size()[1])
        self.scale = scale

        #walking
        self.direction = pygame.math.Vector2()
        self.last_direction = pygame.math.Vector2()
        self.velocity = velocity #скорость игока
        self.max_velocity = pygame.math.Vector2(5, 5)
        #dash
        self.start_dash_delay = 60
        self.dash_delay = 0
        self.dash_count = 3
        self.can_dash = True

        #gun
        self.guns = []
        self.selected_gun_index = -1

        self.hp = 10

        #anim
        #sprites
        self.walking_images = player_walking_images
        self.stay_images = pygame.transform.scale(player_stay_img, (player_stay_img.get_size()[0] * scale, player_stay_img.get_size()[1] * scale))

        self.frame_rate = 64
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

        self.is_flip = False

    def update(self):
        self.animation()
        self.movement()
        self.switch_gun()
        self.get_selected_gun().fire()
        self.get_selected_gun().reload()

    #movement
    def movement(self): #перемещение игрока
        keys = pygame.key.get_pressed()
        self.direction.x, self.direction.y = 0, 0

        if keys[pygame.K_w] and keys[pygame.K_s]: self.direction.y = 0 #y
        elif keys[pygame.K_w]:
            self.direction.y = -1
            self.rect.y -= self.velocity
            if self.is_collide(collide_tiles):
                self.rect.y += self.velocity
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.rect.y += self.velocity
            if self.is_collide(collide_tiles):
                self.rect.y -= self.velocity
        if keys[pygame.K_a] and keys[pygame.K_d]: self.direction.y = 0 #x
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.rect.x -= self.velocity
            if self.is_collide(collide_tiles):
                self.rect.x += self.velocity
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.rect.x += self.velocity
            if self.is_collide(collide_tiles):
                self.rect.x -= self.velocity

        if self.direction.x != 0: self.last_direction.x = self.direction.x
        if self.direction.y != 0: self.last_direction.y = self.direction.y

        if self.dash_delay <= 0:
            if keys[pygame.K_LSHIFT]: self.dash()
        else: self.dash_delay -= 1

    def dash(self):
        self.rect.x += self.velocity * self.direction.x * 10
        self.rect.y += self.velocity * self.direction.y * 10

        self.dash_delay = self.start_dash_delay
        if self.dash_count >= 3: self.dash_count = 3

    def is_collide(self, group):
        for sprite in group:
            if self.rect.colliderect(sprite):
                return True

    #anim
    def animation(self):
        #walking
        if self.direction.x != 0 or self.direction.y != 0:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(self.walking_images): self.frame = 0
                self.image = pygame.transform.scale(self.walking_images[self.frame],
                                                    (self.walking_images[self.frame].get_size()[0] * self.scale,
                                                     self.walking_images[self.frame].get_size()[1] * self.scale))
                if self.direction.x < 0: self.flip()
        else:
            self.image = self.stay_images
            if self.last_direction.x < 0: self.flip()

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    #guns
    def switch_gun(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1] and self.selected_gun_index - 1 >= 0: self.selected_gun_index -= 1
        if keys[pygame.K_3] and self.selected_gun_index + 1 < len(self.guns): self.selected_gun_index += 1

    def add_gun(self, gun_type_str): #выдать игроку пушку
        for gun_type in gun_types:
            if gun_type == gun_type_str:
                new_gun = guns.Gun(gun_types[gun_type], "player")
                self.guns.append(new_gun)
                self.selected_gun_index += 1
                break

    def get_damage(self, damage):
        self.hp -= damage

    def player_angle_debug_draw(self, screen): #отрисовка игрока
        pygame.draw.line(screen, green, (self.rect.center[0] - camera.offset.x, self.rect.center[1] - camera.offset.y), (pygame.mouse.get_pos()), 1) #линия от игрока до мышки

    def get_selected_gun(self): #функция, которая возвращает пушку, которая в руках
        if self.selected_gun_index > -1:
            return self.guns[self.selected_gun_index]

    def calc_player_angle(self): #угол между направлением взгляда и прямой y = player_x (сложная формула из интернета)
        from player.HUD import cursor
        mouse_pos_x, mouse_pos_y = cursor.rect.center
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

player = Player(10,(200 * scale_x, 300 * scale_y), 0.38 * scale_x, 5 * scale_x, player_group) #create player