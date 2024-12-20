import pygame

import guns
from player.player import player
from settings import *
from entities.entities import player_group, player_projectile_group, enemy_projectile_group, enemies_group, cursor_img, \
    half_heat, full_heat, math_menu_image
from entities.tile import tiles, collide_tiles, Tile

pygame.font.init()
debug_elements = []
HUD_elements = []

debug_font = pygame.font.Font(None, 20)

def update_debug_el():
    debug_elements.append(debug_font.render("selected_gun_index: " + str(player.selected_gun_index), True, black))
    debug_elements.append(debug_font.render("ammo: " + str(player.get_selected_gun().ammo), True, black))
    debug_elements.append(debug_font.render("reload_delay: " + str(player.get_selected_gun().reload_delay), True, black))
    debug_elements.append(debug_font.render("ammo_delay: " + str(player.get_selected_gun().ammo_delay), True, black))
    debug_elements.append(debug_font.render("selected_gun: " + str(player.get_selected_gun().type), True, black))
    debug_elements.append(debug_font.render(f"number_of_existing_bullets: {len(guns.all_projectiles)}", True, black))
    debug_elements.append(debug_font.render(f"number_of_existing_objects: "
                                          f"{len(enemy_projectile_group) + len(player_projectile_group) + len(enemies_group) + len(player_group) +
                                             len(tiles) + len(collide_tiles)}", True, black))
    debug_elements.append(debug_font.render("player_hp: " + str(player.hp), True, black))

class HUD_element(pygame.sprite.Sprite):
    def __init__(self, image, pos, scale, visible):
        super().__init__()
        self.original_image = image
        self.image = pygame.transform.scale(image, (self.original_image.get_size()[0] * scale, self.original_image.get_size()[1] * scale))
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        self.visible = visible

    def update(self):
        pass

def update_HUD_elements():
    #hp
    if player.hp % 2 == 0:
        for i in range(player.hp//2):
            HUD_elements.append(HUD_element(full_heat, (10 + i * 55, 10), 0.15, True))
    else:
        for i in range(player.hp//2):
            HUD_elements.append(HUD_element(full_heat, (10 + i * 55, 10), 0.15, True))
        HUD_elements.append(HUD_element(half_heat, (10 + (player.hp//2) * 55, 10), 0.15, True))

    #math menu
    if player.math_menu:
        math_img_size = math_menu_image.get_size()
        menu_img = pygame.transform.scale(math_menu_image, (math_img_size[0] * scale_x, math_img_size[1] * scale_y ))
        HUD_elements.append(HUD_element(menu_img, (140, 72), 0.4, True))

    #bullet indicator


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