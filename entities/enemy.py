import math

import pygame.sprite

import guns
from entities.images import enemies_group, plus_enemy_stay_image, \
    minus_enemy_stay_image, player_projectile_group
from entities.tile import collide_tiles
from guns import gun_types, all_guns
from player.camera import camera
from player.player import player

# тип, скорость, хп, пушка
enemy_types = {"plus": ["plus", plus_enemy_stay_image, 2, 10],
               "minus": ["minus", minus_enemy_stay_image, 4.7, 6]}

scale = 0.15

def spawn_enemy(type_str, pos):
    enemy = Enemy(enemy_types[type_str], pos)
    for wall_block in collide_tiles:
        if enemy.rect.colliderect(wall_block.rect):
            enemy.death()
            return None
    return enemy

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, pos):
        super().__init__(enemies_group)
        source_image = enemy_type[1].convert_alpha()
        w, h = source_image.get_size()
        self.image = pygame.transform.scale(source_image, (w * scale, h * scale))
        self.rect = self.image.get_rect(midbottom=(pos[0], pos[1]))

        self.type = enemy_type[0]
        self.velocity_length = enemy_type[2]
        self.hp = enemy_type[3]

        self.velocity = pygame.math.Vector2()
        if self.type == "plus":
            self.add_gun("standard")
            self.damage = 1
        else:
            self.gun = "empty"
            self.damage = 2

        #booleans
        self.is_flip = False
        self.in_attack_radius = False

    def add_gun(self, gun_type_str): #выдать игроку пушку
        for gun_type in gun_types:
            if gun_type == gun_type_str:
                new_gun = guns.Gun(gun_types[gun_type], self)
                all_guns.append(new_gun)
                self.gun = new_gun

    def update(self):
        if player.alive:
            if self.gun != "empty":
                if self.in_attack_radius:
                    self.gun.fire()
                if self.gun.ammo <= 0 or self.gun.reload_delay > 0:
                    self.gun.reload()
            if player.rect.colliderect(self.rect):
                player.get_damage(self.damage)
            self.movement()
            self.animation()
            if self.hp <= 0:
                self.death()
            for projectile in player_projectile_group:
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
        if self.type == "plus" and r <= 250:
            self.in_attack_radius = True
            return
        else:
            self.in_attack_radius = False
        if r <= 600:
            if not self.is_collide(collide_tiles):
                self.rect.x += self.velocity.x
                self.rect.y += self.velocity.y

    def get_damage(self, damage):
        self.hp -= damage
    def death(self):
        enemies_group.remove(self)
        if self.gun != "empty":
            all_guns.remove(self.gun)

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

def find_path(start_pos, end_pos):
    pass
