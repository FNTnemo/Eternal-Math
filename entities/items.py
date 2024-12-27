import pygame.sprite

from entities.images import item_group, heal_item_image, win_cup_image

#название, каринка, свойства
item_types = {"heal": ["heal", heal_item_image, 1],
              "cup": ["cup", win_cup_image]}

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, type, scale):
        super().__init__(item_group)
        self.type = type[0]
        self.original_image = type[1]
        self.image = pygame.transform.scale(self.original_image, (self.original_image.get_size()[0] * scale,
                                                                  self.original_image.get_size()[1] * scale))
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))

        #свойства
        if self.type == "heal":
            self.heal = type[2]

    def update(self):
        from player.player import player
        if self.is_collide(player):
            if self.type == "heal":
                if player.hp < player.max_hp:
                    player.hp += self.heal
                    item_group.remove(self)
            if self.type == "cup":
                player.win()

    def is_collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        return False
