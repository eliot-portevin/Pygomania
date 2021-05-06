import pygame

from fireball import Fireball
from spritesheet import Spritesheet


class Player(pygame.sprite.Sprite):
    def __init__(self, W, H, x, y, character, platforms):
        super().__init__()
        self.idle_sheet = Spritesheet(f'{character}idle-sheet.png')
        self.move_sheet = Spritesheet(f'{character}move-sheet.png')
        self.crouched_sheet = None
        self.jump_sheet = None
        self.slight_hit_sheet = None
        self.big_hit_sheet = None
        self.jumping_attack_sheet = None
        self.falling_attack_sheet = None
        self.crouched_attack = None
        self.spell_sheet = Spritesheet(f"{character}q_spell-sheet.png")
        self.ultimate_sheet = None

        self.idle_right_sprites = []
        self.idle_left_sprites = []
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.crouched_right_sprites = []
        self.crouched_left_sprites = []
        self.jump_right_sprites = []
        self.jump_left_sprites = []
        self.slight_hit_right_sprites = []
        self.slight_hit_left_sprites = []
        self.big_hit_right_sprites = []
        self.big_hit_left_sprites = []
        self.jumping_attack_right_sprites = []
        self.jumping_attack_left_sprites = []
        self.falling_attack_right_sprites = []
        self.falling_attack_left_sprites = []
        self.spell_right_sprites = []
        self.spell_left_sprites = []
        self.ultimate_right_sprites = []
        self.ultimate_left_sprites = []

        for row in range( self.idle_sheet.get_nb_sprites()):
            sprite, duration = self.idle_sheet.parse_sprites(f"idle{row}.png")
            sprite = pygame.transform.scale(sprite, (192,192))
            self.idle_right_sprites.append([sprite, duration])
            self.idle_left_sprites.append([pygame.transform.flip(sprite, True, False), duration])
        for row in range(self.move_sheet.get_nb_sprites()):
            sprite, duration = self.move_sheet.parse_sprites(f"move{row}.png")
            sprite = pygame.transform.scale(sprite, (192,192))
            self.move_right_sprites.append([sprite, duration])
            self.move_left_sprites.append([pygame.transform.flip(sprite, True, False), duration])
        for row in range(self.spell_sheet.get_nb_sprites()):
            sprite, duration = self.spell_sheet.parse_sprites(f"q_spell{row}.png")
            sprite = pygame.transform.scale(sprite, (256, 256))
            self.spell_right_sprites.append([sprite, duration])
            self.spell_left_sprites.append([pygame.transform.flip(sprite, True, False), duration])

        self.spelling = False
        self.jumping = False
        self.double_jumping = False
        self.moving = False
        self.moving_right = False

        self.W = W
        self.H = H
        self.velocity = 0
        self.acceleration = 0.3
        self.key = 0
        self.time = pygame.time.get_ticks()
        self.platforms = platforms
        self.fireballs = pygame.sprite.Group()

        self.image = self.idle_right_sprites[0][0]
        self.image = pygame.transform.scale(self.image, (192,192))
        self.player_left = self.image
        self.player_right = pygame.transform.flip(self.player_left, True, False)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = x, y + 40
        self.life = 100
        self.life_image = pygame.image.load('media/life.png')
        self.life_image = pygame.transform.scale(self.life_image, (57, 57))
        self.tmp = 500

    def change_animation(self):
        if self.spelling:
            if self.moving_right:
                self.image = self.spell_right_sprites[0][0]
            else:
                self.image = self.spell_left_sprites[0][0]
            self.tmp = self.spell_right_sprites[0][1]
        elif not self.moving:
            self.tmp = self.idle_right_sprites[0][1]
            if self.moving_right:
                self.image = self.idle_right_sprites[0][0]
            else:
                self.image = self.idle_left_sprites[0][0]
        else:
            self.tmp = self.move_right_sprites[0][1]
            if not self.moving_right:
                self.image = self.move_left_sprites[0][0]
            else:
                self.image = self.move_right_sprites[0][0]
        self.key = 0
        self.time = pygame.time.get_ticks()

    def animate(self):
        if pygame.time.get_ticks()-self.time >= self.tmp:
            if self.spelling:
                if self.key == self.spell_sheet.get_nb_sprites():
                    self.spelling = False
                    if self.moving_right:
                        fireball = Fireball((self.rect.right, self.rect.centery), 1)
                    else:
                        fireball = Fireball((self.rect.left, self.rect.centery), -1)
                    fireball.add(self.fireballs)
                    self.change_animation()
                elif self.moving_right:
                    self.image = self.spell_right_sprites[self.key][0]
                else:
                    self.image = self.spell_left_sprites[self.key][0]
                self.tmp = self.spell_left_sprites[self.key][1]
                self.key += 1


            elif not self.moving:
                self.tmp = self.idle_right_sprites[self.key][1]
                if self.moving_right:
                    self.image = self.idle_right_sprites[self.key][0]
                else:
                    self.image = self.idle_left_sprites[self.key][0]
                self.key = (self.key + 1) % self.idle_sheet.get_nb_sprites()
            else:
                self.tmp = self.move_right_sprites[self.key][1]
                if not self.moving_right:
                    self.image = self.move_left_sprites[self.key][0]

                else:
                    self.image = self.move_right_sprites[self.key][0]
                self.key = (self.key+1) % self.move_sheet.get_nb_sprites()
            self.time = pygame.time.get_ticks()


    def move_right(self, dt):
        if self.rect.x < self.W - self.image.get_width():
            self.rect.x += round(5 * dt)

    def move_left(self, dt):
        if self.rect.x > 0:
            self.rect.x -= round(5 * dt)

    def jump(self, dt):
        if not self.jumping:
            self.jumping = True
        elif not self.double_jumping:
            self.double_jumping = True

        self.velocity = -12
        self.rect.y += self.velocity * dt

    def fall_down(self):
        if self.jumping or self.double_jumping:
            self.velocity += 5

    def gravity(self, dt):
        self.velocity += self.acceleration * dt
        self.rect.y += self.velocity * dt

    def check_collision_y(self, platforms):
        self.jumping = True
        self.rect.y += 1
        collisions = self.get_hits(platforms)
        for tile in collisions:
            if self.velocity > 0 and 0 <= (self.rect.bottom - tile.rect.y) < 70:
                self.jumping = False
                self.double_jumping = False
                self.velocity = 0
                self.rect.bottom = tile.rect.top
    def get_hits(self, sprite_group):
        hits = []
        for sprite in sprite_group:
            if pygame.sprite.collide_mask(self,sprite):
                hits.append(sprite)
        return hits
