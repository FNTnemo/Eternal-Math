import pygame

from guns import all_bullets
from player.player import player
from settings import *

pygame.font.init()
HUD_elements = []

debug_font = pygame.font.Font(None, 20)

def update_hud_el():
    HUD_elements.append(debug_font.render("selected_gun_index: " + str(player.selected_gun_index),True, green))
    HUD_elements.append(debug_font.render("ammo: " + str(player.get_selected_gun().ammo),True, green))
    HUD_elements.append(debug_font.render("reload_delay: " + str(player.get_selected_gun().reload_delay),True, green))
    HUD_elements.append(debug_font.render("ammo_delay: " + str(player.get_selected_gun().ammo_delay),True, green))
    HUD_elements.append(debug_font.render("selected_gun: " + str(player.get_selected_gun().type), True, green))
    HUD_elements.append(debug_font.render("number_of_existing_bullets: " + str(len(all_bullets)), True, green))