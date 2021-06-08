import pygame
from player import Player

class Boxer(Player):
    def __init__(self,*args):
        super().__init__(*args)
        self.image = self.idle_right_sprites[0][0]
        self.rect = self.image.get_rect()
    def animate(self,dt):
        self.image = self.idle_right_sprites[0][0]
    def change_animation(self):
        pass