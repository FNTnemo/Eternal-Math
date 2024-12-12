import math

import pygame.sprite

from entities.entities import enemies_group, player_stay_img, player_group, plus_enemy_stay_image, \
    minus_enemy_stay_image
from entities.tile import collide_tiles
from guns import all_projectiles
from player.camera import camera
from player.player import player

# тип, скорость, хп, пушка
enemy_types = {"plus": ["plus", plus_enemy_stay_image, 2, 10],
               "minus": ["minus", minus_enemy_stay_image, 4, 6]}

scale = 0.15

def spawn_enemy(type_str, pos):
    return Enemy(enemy_types[type_str], pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, pos):
        super().__init__(enemies_group)
        source_image = enemy_type[1].convert_alpha()
        w, h = source_image.get_size()
        self.image = pygame.transform.scale(source_image, (w * scale, h * scale))
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))

        self.type = enemy_type[0]
        self.velocity_length = enemy_type[2]
        self.hp = enemy_type[3]
        self.damage = 1

        self.velocity = pygame.math.Vector2()

        #booleans
        self.is_flip = False

    def update(self):
        if player.alive:
            if player.rect.colliderect(self.rect):
                player.get_damage(self.damage)
            self.movement()
            self.animation()
            if self.hp <= 0:
                self.death()
            for projectile in all_projectiles:
                if self.rect.colliderect(projectile.rect):
                    self.get_damage(projectile.damage)
                    projectile.remove()

            #if self.type == "minus":


    def is_collide(self, group):
        for sprite in group:
            new_rect = pygame.Rect(self.rect.x + self.velocity.x, self.rect.y + self.velocity.y,
                                   self.image.get_size()[0], self.image.get_size()[1])
            if new_rect.colliderect(sprite):
                return True
        if player.rect.colliderect(self.rect): return True
        return False

    def movement(self):
        angle = self.calc_angle()
        self.velocity.x = self.velocity_length * math.cos(angle)
        self.velocity.y = self.velocity_length * math.sin(angle)
        r = ((self.rect.x - player.rect.x)**2 + (self.rect.y - player.rect.y)**2) ** 0.5
        print(r)
        if self.type == "plus" and r <= 250:
            return
        if not self.is_collide(collide_tiles):
            self.rect.x += self.velocity.x
            self.rect.y += self.velocity.y

    def get_damage(self, damage):
        self.hp -= damage
    def death(self):
        enemies_group.remove(self)

    #animation
    def animation(self):
        if self.velocity.x < 0 and not self.is_flip:
            self.flip()
            self.is_flip = True
        elif self.velocity.x >= 0 and self.is_flip:
            self.flip()
            self.is_flip = False

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def calc_angle(self):
        from player.HUD import cursor
        player_pos_x, player_pos_y = player.rect.center
        player_pos_x -= camera.offset.x
        player_pos_y -= camera.offset.y
        dx1, dy1 = player_pos_x - (self.rect.center[0] - camera.offset.x), 0
        dx2, dy2 = player_pos_x - (self.rect.center[0] - camera.offset.x), player_pos_y - (self.rect.center[1] - camera.offset.y)
        if dx1 == 0: dx1 = 0.0000001
        if dx2 == 0: dx2 = 0.0000001
        k1, k2 = dy1/dx1, dy2/dx2
        rad = (k2 - k1) / (1 + k1 * k2)
        if player_pos_x >= self.rect.center[0] - camera.offset.x:
            return math.atan(rad)
        else:
            return -(math.pi - math.atan(rad))