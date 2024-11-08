import pygame

#import images
bg1 = pygame.image.load("images/bg1.jpg")

#tiles
wall_tile_test = pygame.image.load("images/wall_sell_test.png")

#player
player_img = pygame.image.load("images/player_test.png")
cursor_img = pygame.image.load("images/cursor.png").convert_alpha()
#guns

#bullets
def get_bullet_img(gun_type):
    return pygame.image.load(f"images/bullet_{gun_type}_test.png")

player_group = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()