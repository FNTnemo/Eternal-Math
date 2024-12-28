import pygame
from pygame import K_ESCAPE

from settings import *

pygame.init() #инициализация
scr = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)
pygame.display.set_icon(pygame.image.load("images/UI/LOGO.ico"))

pygame.mouse.set_visible(False)

from guns import all_projectiles, all_guns
from player.player import player
from player.camera import camera
from map import Background, load_map, loaded_map, get_map_size, map_queue, map_index
from player.HUD import cursor, debug_elements, HUD_elements, update_HUD_elements
from entities.images import bg1, enemy_projectile_group, player_projectile_group, enemies_group, player_group, \
    item_group
from entities.tile import collide_tiles, back_tiles, tiles

stop = False
intro = True

load_map(map_queue[map_index])

for element in range(-(int(-get_map_size(loaded_map)[1] // bg1.get_size()[1]))): #background draw
    back_tiles.add(Background(0, element * 1080, (1920, 1080), bg1))

player.add_gun("standard") #player guns
player.add_gun("laser")

def rander():
    #draw
    draw_queue = [back_tiles, collide_tiles, tiles, item_group, enemy_projectile_group, player_projectile_group, enemies_group, player_group, all_guns, [player.get_selected_gun()]]
    for group in draw_queue:
        for obj in group:
            scr.blit(obj.image, (obj.rect.x - camera.offset.x, obj.rect.y - camera.offset.y))
            #pygame.draw.rect(scr, "red", obj.rect)
    scr.blit(cursor.image, (cursor.rect.x, cursor.rect.y))

    #HUD
    x0 = 5
    y0 = WINDOW_HEIGHT - 18
    update_HUD_elements()

    for element in range(len(debug_elements)):
        scr.blit(debug_elements[element], (x0, y0 - element * 14))
    for element in HUD_elements:
        if element.type == "image":
            scr.blit(element.image, (element.rect.x, element.rect.y))
        if element.type == "text":
            scr.blit(element.text, element.position)

    HUD_elements.clear()

    #update_debug_el()
    #if fps >= 60:
    #    debug_elements.append(debug_font.render("FPS: " + str(fps), True, green))
    #elif fps >= 30:
    #    debug_elements.append(debug_font.render("FPS: " + str(fps), True, yellow))
    #else:
    #    debug_elements.append(debug_font.render("FPS: " + str(fps), True, red))
    # debug_elements.clear()

def update():
    player.update() #player
    camera.center_box_camera(player)
    cursor.update_pos()

    for tile in tiles:
        tile.update()

    if player.alive:
        for enemy in enemies_group:
            enemy.update() #enemy

        for gun in all_guns:
            gun.update() #guns
        player.get_selected_gun().update()

        for projectile in all_projectiles:
            projectile.movement() #bullets

        for item in item_group:
            item.update() #item

def restart_game():
    pass

while not stop: #main game loop
    scr.fill((0, 0, 0))  # screen fill
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (keys[K_ESCAPE] and player.is_win):
            stop = True  # game ending
    fps = clock.get_fps()
    ##

    ##
    update()
    rander()

    clock.tick(TPS)  #ticks per second
    pygame.display.flip()