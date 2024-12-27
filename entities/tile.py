import random

import pygame.sprite

from entities.images import stone_wall_images, enemies_group, portal_image, breack_stone_wall_images

from entities.images import activated_portal_image

collide_tiles = pygame.sprite.Group()
back_tiles = pygame.sprite.Group()
tiles = pygame.sprite.Group()

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, type_sting, size):
        super().__init__()
        self.type = type_sting
        img = None

        if self.type == "wall":
            m = random.randint(0, 10)
            if m == 0:
                n = random.randint(0, 5)
                img = breack_stone_wall_images[n].convert_alpha()
            else:
                n = random.randint(0, 4)
                img = stone_wall_images[n].convert_alpha()
        if self.type == "portal":
            img = portal_image
            self.activated = False

        self.sell_size_k_x = size[0] / img.get_size()[0]
        self.sell_size_k_y = size[1] / img.get_size()[1]
        self.original_image = pygame.transform.scale(img.convert_alpha(), (img.get_size()[0] * self.sell_size_k_x, img.get_size()[1] * self.sell_size_k_y))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))

        self.rotation_degrees = 0

    def update(self):
        if self.type == "portal":
            if self.rotation_degrees <= 360:
                self.rotation_degrees += 1
            else: self.rotation_degrees = 0
            self.image = pygame.transform.rotate(self.original_image, self.rotation_degrees)
            if len(enemies_group) <= 0:
                self.activated = True
                self.original_image = pygame.transform.scale(activated_portal_image, (activated_portal_image.get_size()[0] * self.sell_size_k_x, activated_portal_image.get_size()[1] * self.sell_size_k_y))


def clear_tiles():
    for i in collide_tiles:
        i.remove()
    for i in back_tiles:
        i.remove()