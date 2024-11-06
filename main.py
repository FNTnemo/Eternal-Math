import pygame

from player.HUD import *

pygame.init() #инициализация

from player.player import player
import guns
from settings import *

scr = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption(TITLE)
#pygame.display.set_icon()


stop = False
player.add_gun("standard")
player.add_gun("laser")

while not stop: #main game loop
    scr.fill((0, 0, 0))  # заливка экрана
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            stop = True  # заершение программы

    fps = clock.get_fps()

    #player
    player.movement()
    player.player_draw(scr)
    player.switch_gun()
    player.get_selected_gun().fire()
    player.get_selected_gun().reload()

    #bullets
    guns.draw_bullets(scr)
    guns.bullets_movement()

    #HUD
    x0 = 5
    y0 = WINDOW_HEIGHT - 18
    update_hud_el()
    if fps >= 60:
        HUD_elements.append(debug_font.render("FPS: " + str(fps), True, green))
    elif fps >= 30:
        HUD_elements.append(debug_font.render("FPS: " + str(fps), True, yellow))
    else:
        HUD_elements.append(debug_font.render("FPS: " + str(fps), True, red))
    for i in range(len(HUD_elements)):
        scr.blit(HUD_elements[i], (x0, y0 - i * 14))
    HUD_elements.clear()

    clock.tick(TPS)  #ticks per second
    pygame.display.flip()