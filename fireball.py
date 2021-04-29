import pygame, time, math


class Fireball(pygame.sprite.Sprite):
    def __init__(self, pos, dir):
        super().__init__()
        self.velocity = 300
        self.image = pygame.transform.scale(pygame.image.load('media/Mage_animation/fireball.png'), (64, 64))
        # Position in x and y and direction in x (-1 for left and 1 for right)
        self.position = pos
        self.direction = dir
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.time = time.time()
        self.begin_time = self.time
        self.frames = 0

    def move(self):
        self.frames += 1
        now = time.time()
        dt = now - self.time
        self.time = now
        self.rect.x += self.velocity * self.direction * dt
        if (math.fabs(self.rect.x - self.position[0]) > 1000) or (self.rect.x > 1920 or self.rect.right < 0):
            self.remove()

    def remove(self):
        # print(self.groups)             #Je les ai enlevés parce que ils servaient à rien
        # print(self.groups())           #Mais en même temps je me disais que tu pourrais en avoir besoin
        self.kill()
