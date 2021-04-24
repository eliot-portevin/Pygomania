import pygame, os, sys
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, W, H, x, y):
        super().__init__()
        self.idle_sheet = Spritesheet('media/spritesheet_idle.png')
        self.move_sheet = Spritesheet('media/spritesheet_move.png')
        self.punch_sheet = Spritesheet("media/spritesheet_punch.png")
        self.idle_sprites = []
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.punch_sprites = []
        for row in range(8):
            sprite = self.idle_sheet.get_sprites(row*40,0,40,54)
            self.idle_sprites.append(pygame.transform.scale(sprite,(100,135)))
        for row in range(8):
            sprite = self.move_sheet.get_sprites(row*47,0,47,53)
            self.move_right_sprites.append(pygame.transform.scale(sprite, (120, 135)))
        for row in range(8):
            sprite = self.move_sheet.get_sprites(row*47,0,47,53)
            sprite = pygame.transform.flip(sprite,True,False)
            self.move_left_sprites.append(pygame.transform.scale(sprite, (120, 135)))
        self.punch_sprites.append(pygame.transform.scale(self.punch_sheet.get_sprites(0,0,53,48),(140,130)))
        self.punch_sprites.append(pygame.transform.scale(self.punch_sheet.get_sprites(70, 0, 45, 48), (120, 130)))
        self.punch_sprites.append(pygame.transform.scale(self.punch_sheet.get_sprites(118, 0, 62, 48), (163, 130)))
        self.punch_sprites.append(pygame.transform.scale(self.punch_sheet.get_sprites(187, 0, 58, 46), (150, 125)))
        self.punch_sprites.append(pygame.transform.scale(self.punch_sheet.get_sprites(250, 0, 45, 48), (120, 130)))
        self.punch_sprites.append(pygame.transform.scale(self.punch_sheet.get_sprites(312, 0, 58, 46), (150, 125)))
        self.punching = False
        self.jumping = False
        self.double_jumping = False
        self.time = pygame.time.get_ticks()
        self.key = 0
        self.W = W
        self.H = H
        self.velocity = 0
        self.acceleration = 0.6
        self.moving = False
        self.moving_right = False
        prop = round(W/8)
        self.image = pygame.image.load('media/player.png')
        self.image = pygame.transform.scale(self.image,(prop,round(prop*11/16)))
        self.player_left = self.image
        self.player_right = pygame.transform.flip(self.player_left, True, False)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = x,y
        self.life = 100
        self.life_image = pygame.image.load('media/life.png')
        self.life_image = pygame.transform.scale(self.life_image, (57, 57))
        self.tmp = 90

    def animate(self):
        if self.moving:
            self.tmp = 90
        else:
            self.tmp = 150
        
        if pygame.time.get_ticks() - self.time > self.tmp:
            self.key = (self.key+1) % 8
            if self.punching:
                self.image = self.punch_sprites[self.key]
                if self.key == 5:
                    self.punching = False
            elif not self.moving:
                self.image = self.idle_sprites[self.key]
            elif not self.moving_right:
                self.image = self.move_left_sprites[self.key]
            else:
                self.image  = self.move_right_sprites[self.key]
            self.time = pygame.time.get_ticks()
        
    def move_right(self):
        self.moving_right = True
        if self.rect.x < self.W - self.image.get_width():
            self.rect.x += 5

    def move_left(self):
        self.moving_right = False
        if self.rect.x > 0:
            self.rect.x -= 5

    def gravity(self):
        if self.jumping and (self.velocity < 0 or self.rect.bottom < round(203/216*self.H)):
            self.velocity += self.acceleration
            self.rect.y += self.velocity
        else:
            self.velocity = 0
            self.jumping = False
            self.double_jumping = False

    def jump(self):
        if not self.jumping:
            self.jumping = True
        elif not self.double_jumping:
            self.double_jumping = True

        self.velocity = -12
        self.rect.y += self.velocity
    
    def fall_down(self):
        if self.jumping or self.double_jumping:
            self.velocity += 7
    
    def check_height(self):
        if self.rect.bottom >= round(203/216*self.H):
            self.rect.bottom = round(203/216*self.H)