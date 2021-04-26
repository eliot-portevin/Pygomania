import pygame, os
from spritesheet import Spritesheet
from fireball import Fireball
class Player(pygame.sprite.Sprite):
    def __init__(self, W, H, x, y):
        super().__init__()
        self.idle_sheet = Spritesheet('media/Mage_animation/idle-sheet.png')
        self.move_sheet = Spritesheet('media/spritesheet_move.png')
        self.punch_sheet = Spritesheet("media/Mage_animation/q_spell-sheet.png")
        self.idle_right_sprites = []
        self.idle_left_sprites = []
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.q_spell_right_sprites = []
        self.q_spell_left_sprites = []
        for row in range(1,9):
            sprite = self.idle_sheet.parse_sprites(f"idle{row}.png")
            sprite = pygame.transform.scale(sprite,(256,256))
            self.idle_right_sprites.append(sprite)
            self.idle_left_sprites.append(pygame.transform.flip(sprite,True,False))
        for row in range(8):
            sprite = self.move_sheet.get_sprites(row*47,0,47,53)
            self.move_right_sprites.append(pygame.transform.scale(sprite, (120, 135)))
        for row in range(8):
            sprite = self.move_sheet.get_sprites(row*47,0,47,53)
            sprite = pygame.transform.flip(sprite,True,False)
            self.move_left_sprites.append(pygame.transform.scale(sprite, (120, 135)))
        for row in range(1,9):
            sprite = self.punch_sheet.parse_sprites(f"q_spell{row}.png")
            sprite = pygame.transform.scale(sprite, (256, 256))
            self.q_spell_right_sprites.append(sprite)
            self.q_spell_left_sprites.append(pygame.transform.flip(sprite,True,False))
        self.punching = False
        self.jumping = False
        self.double_jumping = False
        self.time = pygame.time.get_ticks()
        self.key = 1
        self.W = W
        self.H = H
        self.velocity = 0
        self.acceleration = 0.6
        self.moving = False
        self.moving_right = False
        self.fireballs = pygame.sprite.Group()
        self.image = self.idle_right_sprites[0]
        self.image = pygame.transform.scale(self.image,(256,256))
        self.player_left = self.image
        self.player_right = pygame.transform.flip(self.player_left, True, False)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = x, y + 40
        self.life = 100
        self.life_image = pygame.image.load('media/life.png')
        self.life_image = pygame.transform.scale(self.life_image, (57, 57))
        self.tmp = 90
    def animate(self):
        if self.punching:
            self.tmp = 40
        elif self.moving:
            self.tmp = 150
        else:
            self.tmp = 150
        if pygame.time.get_ticks() - self.time > self.tmp:
            self.key = (self.key+1) % 8
            if self.punching:
                if self.moving_right:
                    self.image = self.q_spell_right_sprites[self.key]
                else:
                    self.image = self.q_spell_left_sprites[self.key]
                if self.key == 7:
                    self.punching = False
                    if self.moving_right:
                        fireball = Fireball((self.rect.right, self.rect.centery), 1)
                    else:
                        fireball = Fireball((self.rect.left, self.rect.centery), -1)
                    fireball.add(self.fireballs)

            elif not self.moving:
                if self.moving_right:
                    self.image = self.idle_right_sprites[self.key]
                else:
                    self.image = self.idle_left_sprites[self.key]
            elif not self.moving_right:
                self.image = self.move_left_sprites[self.key]
            else:
                self.image = self.move_right_sprites[self.key]
            self.time = pygame.time.get_ticks()

    def move_right(self):
        if self.rect.x < self.W - self.image.get_width():
            self.rect.x += 5

    def move_left(self):
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
        if self.rect.bottom >= round(203 / 216 * self.H):
            self.rect.bottom = round(203 / 216 * self.H)
