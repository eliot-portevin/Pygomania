import pygame


class Laser_Beam(pygame.sprite.Sprite):
    def __init__(self,W,H,x):
        super().__init__()
        self.W, self.H = W, H
        self.images = []
        self.image = pygame.surface.Surface((150,round(H*0.942)),pygame.SRCALPHA)
        self.image.fill((118,66,138,150))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.time_apparition = pygame.time.get_ticks()

    def check(self):
        if pygame.time.get_ticks()- self.time_apparition > 1000:
            self.kill()