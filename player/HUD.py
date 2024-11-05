import pygame

from player.player import player
from settings import *

pygame.font.init()
HUD_elements = []

debug_font = pygame.font.Font(None, 18)

def update_hud_el():
    HUD_elements.append(debug_font.render("selected_gun_index: " + str(player.selected_gun_index),True, green))
    HUD_elements.append(debug_font.render("ammo: " + str(player.get_selected_gun().ammo),True, green))
    HUD_elements.append(debug_font.render("reload_delay: " + str(player.get_selected_gun().reload_delay),True, green))
    HUD_elements.append(debug_font.render("ammo_delay: " + str(player.get_selected_gun().ammo_delay),True, green))
    from main import fps
    HUD_elements.append(debug_font.render("FPS: " + str(fps),True, green))