import pygame.sprite

collide_tiles = pygame.sprite.Group()
tiles = pygame.sprite.Group()

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size, img):
        super().__init__()
        sell_size_k_x = size[0] / img.get_size()[0]
        sell_size_k_y = size[1] / img.get_size()[1]
        self.image = pygame.transform.scale(img.convert_alpha(), (img.get_size()[0] * sell_size_k_x, img.get_size()[1] * sell_size_k_y))
        self.rect = self.image.get_rect(topleft=(x, y))

def clear_tiles():
    for i in collide_tiles:
        i.remove()
    for i in tiles:
        i.remove()