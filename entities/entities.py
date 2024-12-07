import pygame

#import images
bg1 = pygame.image.load("images/bg1.jpg")

#tiles
wall_tile_test = pygame.image.load("images/blocks/wall_sell_test.png")
stone_wall_images = []
for n in range(5):
    stone_wall_images.append(pygame.image.load(f"images/blocks/stone_wall_cell_{n}.png"))

#player
player_walking_images = []
for n in range(4):
     player_walking_images.append(pygame.image.load(f"images/player/player_walk_{n}.png"))
player_stay_img = pygame.image.load("images/player/player_stay.png")
cursor_img = pygame.image.load("images/cursor.png")
#guns

#bullets
def get_bullet_img(gun_type):
    return pygame.image.load(f"images/guns/bullets/bullet_{gun_type}_test.png" )

#enemies
plus_enemy_stay_image = pygame.image.load("images/enemies/plus_vrug.png")
minus_enemy_stay_image = pygame.image.load("images/enemies/SU-shi_vrag.png")


def collision(obj, group2):
    for obj2 in group2:
        if obj.rect.colliderect(obj2.rect):
            return True, obj.rect.colliderect(obj2.rect)
    return False

player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
player_bullets_group = pygame.sprite.Group()
enemy_bullets_group = pygame.sprite.Group()