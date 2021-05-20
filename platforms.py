import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.transform.scale(image, (self.rect.w, self.rect.h))
