import pygame, math


class Fireball(pygame.sprite.Sprite):
    def __init__(self, pos, dir):
        super().__init__()
        self.velocity = 8
        self.image = pygame.transform.scale(pygame.image.load('media/Mage_animation/fireball.png'), (64, 64))
        # Position in x and y and direction in x (-1 for left and 1 for right)
        self.position = pos
        self.direction = dir
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position

    def move(self,dt):
        self.rect.x += self.velocity * self.direction * dt
        if (math.fabs(self.rect.x - self.position[0]) > 1000) or (self.rect.x > 1920 or self.rect.right < 0):
            self.remove()

    def remove(self):
        self.kill()
