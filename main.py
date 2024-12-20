import pygame
from settings import *

pygame.init() #инициализация
scr = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)
pygame.display.set_icon(pygame.image.load("images/UI/LOGO.ico"))

pygame.mouse.set_visible(False)

from guns import all_projectiles, all_guns
from entities.enemy import spawn_enemy
from player.player import player
from player.camera import camera
from map import Background, load_map, loaded_map, m0_0, m0_1, get_map_size
from player.HUD import cursor, debug_font, debug_elements, update_debug_el, HUD_elements, \
    update_HUD_elements
from entities.entities import bg1, enemy_projectile_group, player_projectile_group, enemies_group, player_group, \
    item_group
from entities.tile import collide_tiles, tiles

stop = False
load_map(m0_1)
#loaded_map.draw_map()

for element in range(-(int(-get_map_size(loaded_map)[1] // bg1.get_size()[1]))): #background draw
    tiles.add(Background(0, element * 1080, (1920, 1080), bg1))

player.add_gun("standard") #player guns
player.add_gun("laser")

spawn_enemy("plus", (100, 400)) #enemy spawn
spawn_enemy("minus", (700, 200))


while not stop: #main game loop
    scr.fill((0, 0, 0))  # screen fill
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True  # game ending

    fps = clock.get_fps()
    #player
    player.update()
    camera.center_box_camera(player)
    #player.player_angle_debug_draw(scr)
    #camera.camera_shake(10, 10)

    if player.alive:
        #enemy
        for enemy in enemies_group:
            enemy.update()

        #guns
        for gun in all_guns:
            gun.update()
        player.get_selected_gun().update()

        #bullets movement
        for projectile in all_projectiles:
            projectile.movement()

        #item
        for item in item_group:
            item.update()
    cursor.update_pos()

    #draw
    print(len(all_guns))
    draw_queue = [tiles, collide_tiles, item_group, enemy_projectile_group, player_projectile_group, enemies_group, player_group, all_guns, [player.get_selected_gun()]]
    for group in draw_queue:
        for obj in group:
            scr.blit(obj.image, (obj.rect.x - camera.offset.x, obj.rect.y - camera.offset.y))
            #pygame.draw.rect(scr, "red", obj.rect)
    scr.blit(cursor.image, (cursor.rect.x, cursor.rect.y))

    #HUD
    x0 = 5
    y0 = WINDOW_HEIGHT - 18
    update_HUD_elements()
    update_debug_el()
    if fps >= 60:
        debug_elements.append(debug_font.render("FPS: " + str(fps), True, green))
    elif fps >= 30:
        debug_elements.append(debug_font.render("FPS: " + str(fps), True, yellow))
    else:
        debug_elements.append(debug_font.render("FPS: " + str(fps), True, red))

    for element in range(len(debug_elements)):
        scr.blit(debug_elements[element], (x0, y0 - element * 14))
    for element in HUD_elements:
        scr.blit(element.image, (element.rect.x, element.rect.y))
    debug_elements.clear()
    HUD_elements.clear()

    clock.tick(TPS)  #ticks per second
    pygame.display.flip()