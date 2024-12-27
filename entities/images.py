import pygame

#import images
bg1 = pygame.image.load("images/bg1.jpg").convert_alpha()

#tiles
wall_tile_test = pygame.image.load("images/blocks/wall_sell_test.png").convert_alpha()
stone_wall_images = []
breack_stone_wall_images = []
for n in range(5):
    stone_wall_images.append(pygame.image.load(f"images/blocks/stone_wall_cell_{n}.png").convert_alpha())
for n in range(6):
    breack_stone_wall_images.append(pygame.image.load(f"images/blocks/breack_stone_wall_{n}.png").convert_alpha())
activated_portal_image = pygame.image.load("images/blocks/white_portal.png").convert_alpha()
portal_image = pygame.image.load("images/blocks/portal.png").convert_alpha()
win_cup_image = pygame.image.load("images/items/win_cup.png").convert_alpha()

#player
player_walking_images = []
for n in range(4):
     player_walking_images.append(pygame.image.load(f"images/player/player_walk_{n}.png").convert_alpha())
player_stay_img = pygame.image.load("images/player/player_stay.png").convert_alpha()
cursor_img = pygame.image.load("images/cursor.png").convert_alpha()
#guns

#bullets
#standard_bullet_image = pygame.image.load("images/guns/bullets/bullet.png")
def get_bullet_img(gun_type):
    return pygame.image.load(f"images/guns/bullets/bullet_{gun_type}.png" ).convert_alpha()

#guns
gun_images = {"standard": pygame.image.load("images/guns/standard_gun.png").convert_alpha(),
              "laser": pygame.image.load("images/guns/laser_gun.png").convert_alpha()}

#enemies
plus_enemy_stay_image = pygame.image.load("images/enemies/plus_vrug.png").convert_alpha()
minus_enemy_stay_image = pygame.image.load("images/enemies/SU-shi_vrag.png").convert_alpha()

#hud
half_heat = pygame.image.load("images/UI/half_heart.png").convert_alpha()
full_heat = pygame.image.load("images/UI/full_heart.png").convert_alpha()
bullet_indicator_image = pygame.image.load("images/UI/bullet_indicator.png").convert_alpha()
math_menu_image = pygame.image.load("images/UI/math_menu.png").convert_alpha()

#items
heal_item_image = pygame.image.load("images/items/heal.png").convert_alpha()

#scenes
intro_images = [pygame.image.load("images/intro0.png").convert_alpha(),
                pygame.image.load("images/intro1.png").convert_alpha()]

player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
player_projectile_group = pygame.sprite.Group()
enemy_projectile_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()