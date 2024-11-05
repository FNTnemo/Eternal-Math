import math

import pygame

pygame.init() #инициализация

from player import player
import guns
from settings import *

scr = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption(TITLE)
#pygame.display.set_icon()

stop = False

#player = Player(10, 10, 0, 5) #create player
player.add_gun(guns.standard_pistol)


while not stop: #main game loop
    scr.fill((0, 0, 0))  # заливка экрана
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            stop = True  # заершение программы

    #player
    player.movement()
    player.player_draw(scr)
    player.get_selected_gun().fire()

    print(math.degrees(player.calc_player_angle()))

    #bullets
    guns.draw_bullets(scr)
    guns.bullets_movement()

    clock.tick(TPS)  #ticks per second
    pygame.display.flip()