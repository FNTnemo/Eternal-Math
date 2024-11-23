from ctypes import PyDLL

import pygame
from pygame.examples.cursors import image

import guns
from player.player import player
from settings import *
from entities.entities import player_group, player_bullets_group, enemy_bullets_group, enemies_group, cursor_img
from entities.tile import tiles, collide_tiles, Tile

pygame.font.init()
debug_elements = []
HUD_elements = []

debug_font = pygame.font.Font(None, 20)

def update_debug_el():
    debug_elements.append(debug_font.render("selected_gun_index: " + str(player.selected_gun_index), True, green))
    debug_elements.append(debug_font.render("ammo: " + str(player.get_selected_gun().ammo), True, green))
    debug_elements.append(debug_font.render("reload_delay: " + str(player.get_selected_gun().reload_delay), True, green))
    debug_elements.append(debug_font.render("ammo_delay: " + str(player.get_selected_gun().ammo_delay), True, green))
    debug_elements.append(debug_font.render("selected_gun: " + str(player.get_selected_gun().type), True, green))
    debug_elements.append(debug_font.render(f"number_of_existing_bullets: {len(guns.all_projectiles)}", True, green))
    debug_elements.append(debug_font.render(f"number_of_existing_objects: "
                                          f"{len(enemy_bullets_group) + len(player_bullets_group) + len(enemies_group) + len(player_group) +
                                             len(tiles) + len(collide_tiles)}", True, green))

class HUD_element(pygame.sprite.Sprite):
    def __init__(self, rect, images, visible):
        super().__init__()
        self.image = pygame.image
        self.rect = rect
        self.visible = visible

    def draw(self, scr):
        scr.blit(self.image, self.rect)

def update_HUD_element(element):
    HUD_elements.append(HUD_element(element.image, pygame.Rect(500, 500, WINDOW_WIDTH - 500 * 2, WINDOW_HEIGHT - 500 * 3), )) #math window

class Cursor(pygame.sprite.Sprite):
    def __init__(self, scale):
        super().__init__()
        self.img_size = cursor_img.get_size()
        self.image = pygame.transform.scale(cursor_img, (self.img_size[0] * scale, self.img_size[1] * scale))
        w = self.img_size[0] * scale
        h = self.img_size[1] * scale

        self.rect = pygame.Rect(0, 0, w, h)
        self.scale = scale



    def update_pos(self):
        self.rect.center = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

cursor = Cursor(0.2)