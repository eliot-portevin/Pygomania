import pygame
from player import Player

class Boxer(Player):
    def __init__(self,*args):
        super().__init__(*args)
        self.create_animations("punch",w_normal=False)
        self.image = self.idle_right_sprites[0][0]
        self.rect = self.image.get_rect()
        self.punching = False
        self.moving_right = True
        self.key = 0
    def animate(self,dt):
        self.jump_animation = True
        if pygame.time.get_ticks() - self.time >= self.tmp:
            if not self.punching:
                if self.moving_right:
                    self.image = self.idle_right_sprites[self.key][0]
                else:
                    self.image = self.idle_left_sprites[self.key][0]
                self.tmp = self.idle_right_sprites[self.key][1]
                self.key = (self.key + 1) % self.idle_sheet.get_nb_sprites()
            else:
                if self.moving_right:
                    self.image = self.punch_right_sprites[self.key][0]
                else:
                    self.image = self.punch_left_sprites[self.key][0]
                self.tmp = self.punch_right_sprites[self.key][1]
                self.key += 1
                if self.key == self.punch_sheet.get_nb_sprites():
                    self.punching = False
                    self.change_animation()
            self.time = pygame.time.get_ticks()
            if not self.moving_right:
                self.rect = self.image.get_rect(topright=self.rect.topright)
    def change_animation(self):
        self.key = 0
        if self.punching:
            if self.moving_right:
                self.image = self.punch_right_sprites[self.key][0]
            else:
                self.image = self.punch_left_sprites[self.key][0]
            self.tmp = self.punch_right_sprites[self.key][1]
        else:
            if self.moving_right:
                self.image = self.idle_right_sprites[self.key][0]
            else:
                self.image = self.idle_left_sprites[self.key][0]
            self.tmp = self.idle_right_sprites[self.key][1]
        self.time = pygame.time.get_ticks()
        if not self.moving_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
