import pygame

from settings import *

pygame.init() #инициализация
scr = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

from player.camera import camera
from map import map1, Background
from player.HUD import *
from entities.entities import bg1
from entities.tile import collide_tiles, tiles

clock = pygame.time.Clock()

map1.draw_map()
tiles.add(Background(0, 0, (1920, 1080), bg1))
tiles.add(Background(0, 1080, (1920, 1080), bg1))

pygame.display.set_caption(TITLE)
#pygame.display.set_icon()

#custom cursor
pygame.mouse.set_visible(False)
cursor = Cursor(3)

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
    player.switch_gun()
    player.get_selected_gun().fire()
    player.get_selected_gun().reload()
    camera.center_box_camera(player)

    #bullets
    guns.bullets_movement()

    cursor.update_pos()

    #draw
    draw_queue = [tiles, collide_tiles, enemy_bullets, player_bullets, enemies, player_group]
    for group in draw_queue:
        for obj in group:
            scr.blit(obj.image, (obj.rect.x - camera.offset.x, obj.rect.y - camera.offset.y))
    scr.blit(cursor.image, (cursor.rect.x - cursor.img_size[0]*1.5, cursor.rect.y - cursor.img_size[1]*1.5))

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