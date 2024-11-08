import pygame
from pygame.examples.cursors import image, image_cursor

import guns
from player.player import player
from settings import *
from entities.entities import player_group, player_bullets, enemy_bullets, enemies, cursor_img
from entities.tile import tiles, collide_tiles, Tile

pygame.font.init()
HUD_elements = []

debug_font = pygame.font.Font(None, 20)

def update_hud_el():
    HUD_elements.append(debug_font.render("selected_gun_index: " + str(player.selected_gun_index),True, green))
    HUD_elements.append(debug_font.render("ammo: " + str(player.get_selected_gun().ammo),True, green))
    HUD_elements.append(debug_font.render("reload_delay: " + str(player.get_selected_gun().reload_delay),True, green))
    HUD_elements.append(debug_font.render("ammo_delay: " + str(player.get_selected_gun().ammo_delay),True, green))
    HUD_elements.append(debug_font.render("selected_gun: " + str(player.get_selected_gun().type), True, green))
    HUD_elements.append(debug_font.render(f"number_of_existing_bullets: {len(guns.all_bullets)}", True, green))
    HUD_elements.append(debug_font.render(f"number_of_existing_objects: "
                                          f"{len(enemy_bullets) + len(player_bullets) + len(enemies) + len(player_group) + 
                                             len(tiles) + len(collide_tiles)}", True, green))

class Cursor(pygame.sprite.Sprite):
    def __init__(self, scale):
        super().__init__()
        self.img_size = cursor_img.get_size()
        self.image = pygame.transform.scale(cursor_img, (self.img_size[0] * scale, self.img_size[1] * scale))
        self.rect = image.get_rect(center=(pygame.mouse.get_pos()))
    def update_pos(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()