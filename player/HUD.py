import pygame

import guns
from map import get_map_index
from player.player import player
from settings import *
from entities.images import player_group, player_projectile_group, enemy_projectile_group, enemies_group, cursor_img, half_heat, full_heat, math_menu_image, bullet_indicator_image
from entities.tile import back_tiles, collide_tiles

#hints boolean
W_pressed = False
A_pressed = False
S_pressed = False
D_pressed = False
mouse_button_0_pressed = False
R_pressed = False

pygame.font.init()
debug_elements = []
HUD_elements = []

debug_font = pygame.font.Font(None, 20)
bullet_indicator_font = pygame.font.Font(None, 40)
hints_font = pygame.font.Font(None, 40)

def update_debug_el():
    debug_elements.append(debug_font.render("selected_gun_index: " + str(player.selected_gun_index), True, black))
    debug_elements.append(debug_font.render("ammo: " + str(player.get_selected_gun().ammo), True, black))
    debug_elements.append(debug_font.render("reload_delay: " + str(player.get_selected_gun().reload_delay), True, black))
    debug_elements.append(debug_font.render("ammo_delay: " + str(player.get_selected_gun().ammo_delay), True, black))
    debug_elements.append(debug_font.render("selected_gun: " + str(player.get_selected_gun().type), True, black))
    debug_elements.append(debug_font.render(f"number_of_existing_bullets: {len(guns.all_projectiles)}", True, black))
    debug_elements.append(debug_font.render(f"number_of_existing_objects: "
                                          f"{len(enemy_projectile_group) + len(player_projectile_group) + len(enemies_group) + len(player_group) +
                                             len(back_tiles) + len(collide_tiles)}", True, black))
    debug_elements.append(debug_font.render("player_hp: " + str(player.hp), True, black))

class HUD_element(pygame.sprite.Sprite):
    # для картинок: тип, картинка, позиция, скейл, отображение
    # для текста: тип, текст, позиция
    def __init__(self, typei, *parameters):
        super().__init__()
        self.type = typei
        if self.type == "image":
            self.original_image = parameters[0]
            self.image = pygame.transform.scale(parameters[0], (self.original_image.get_size()[0] * parameters[2], self.original_image.get_size()[1] * parameters[2]))
            self.rect = self.image.get_rect(topleft=(parameters[1][0], parameters[1][1]))
            self.visible = parameters[3]
        if self.type == "text":
            self.text = parameters[0]
            self.position = parameters[1]

    def update(self):
        pass

def update_HUD_elements():
    #hp
    global A_pressed, W_pressed, S_pressed, D_pressed, mouse_button_0_pressed, R_pressed
    if player.hp % 2 == 0:
        for i in range(player.hp//2):
            HUD_elements.append(HUD_element("image", full_heat, (10 + i * 55, 10), 0.15, True))
    else:
        for i in range(player.hp//2):
            HUD_elements.append(HUD_element("image", full_heat, (10 + i * 55, 10), 0.15, True))
        HUD_elements.append(HUD_element("image", half_heat, (10 + (player.hp//2) * 55, 10), 0.15, True))

    #bullet indicator
    HUD_elements.append(HUD_element("image" ,pygame.transform.rotate(bullet_indicator_image, 90), (30, WINDOW_HEIGHT - 70), 0.15, True))
    HUD_elements.append(HUD_element("text", bullet_indicator_font.render(str(player.get_selected_gun().ammo), True, black), (70, WINDOW_HEIGHT - 50)))

    #math menu
    if player.math_menu:
        math_img_size = math_menu_image.get_size()
        menu_img = pygame.transform.scale(math_menu_image, (math_img_size[0] * scale_x, math_img_size[1] * scale_y ))
        HUD_elements.append(HUD_element("image", menu_img, (140, 72), 0.4, True))

    #hints
    hints_pos = (150, WINDOW_HEIGHT - 50)
    if get_map_index() == 0:
        keys = pygame.key.get_pressed()
        m_keys = pygame.mouse.get_pressed()
        if keys[pygame.K_a]: A_pressed = True
        if keys[pygame.K_d]: D_pressed = True
        if keys[pygame.K_w]: W_pressed = True
        if keys[pygame.K_s]: S_pressed = True
        if keys[pygame.K_r]: R_pressed = True
        if m_keys[0]: mouse_button_0_pressed = True
        if not (A_pressed and W_pressed and S_pressed and D_pressed):
            HUD_elements.append(HUD_element("text", hints_font.render("Используйте клавиши W/A/S/D для перемещения", True, black), hints_pos))
        elif not mouse_button_0_pressed:
            HUD_elements.append(HUD_element("text", hints_font.render("Используйте правую кнопку мыши для выстрела", True, black), hints_pos))
        elif not R_pressed and player.get_selected_gun().ammo <= 0:
            HUD_elements.append(HUD_element("text", hints_font.render("Используйте клавишу R для перезарядки оружия", True, black), hints_pos))
        elif R_pressed:
            HUD_elements.append(HUD_element("text", hints_font.render("Найдите портал, для перехода на следующий уровень", True, black), hints_pos))
    elif get_map_index() == 1:
        if len(enemies_group) > 0:
            HUD_elements.append(HUD_element("text", hints_font.render("Убейте всех врагов для активации портала!", True, black), hints_pos))

    if player.is_win:
        HUD_elements.append(HUD_element("text", hints_font.render("Поздравляем, Вы прошли игру!", True, black), (150, WINDOW_HEIGHT//2.5)))
        HUD_elements.append(HUD_element("text", hints_font.render("Главный герой проснулся после крепкого сна, пошёл на урок математики и,", True, black), (150, WINDOW_HEIGHT // 2.5 + 30)))
        HUD_elements.append(HUD_element("text", hints_font.render("используя полученные знания, получил 5.", True, black), (150, WINDOW_HEIGHT // 2.5 + 60)))



hints = pygame.sprite.Sprite()
class Hints(pygame.sprite.Sprite):
    def __init__(self, image, pos, time_bool, time):
        super().__init__()
        self.original_image = image
        self.image = self.original_image
        self.rect = image.get_rect(topleft=pos)
        self.disappearance_time = time
        self.disappearance_bool = time_bool

        self.opacity = 1000

    def update(self):
        if self.disappearance_bool:
            if self.disappearance_time <= 0 < self.opacity:
                self.opacity -= 1
            else:
                self.disappearance_time -= 1
            self.image.putalpha(self.opacity//10)
            self.image.show()


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