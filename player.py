import pygame

from fireball import Fireball
from spritesheet import Spritesheet


class Player(pygame.sprite.Sprite):
    def __init__(self, W, H, x, y, character, platforms):
        super().__init__()
        self.crouched_sheet = None
        self.slight_hit_sheet = None
        self.big_hit_sheet = None
        self.jumping_attack_sheet = None
        self.falling_attack_sheet = None
        self.crouched_attack = None
        self.ultimate_sheet = None

        self.crouched_right_sprites = []
        self.crouched_left_sprites = []
        self.slight_hit_right_sprites = []
        self.slight_hit_left_sprites = []
        self.big_hit_right_sprites = []
        self.big_hit_left_sprites = []
        self.jumping_attack_right_sprites = []
        self.jumping_attack_left_sprites = []
        self.falling_attack_right_sprites = []
        self.falling_attack_left_sprites = []
        self.ultimate_right_sprites = []
        self.ultimate_left_sprites = []

        self.create_animations('idle',character)
        self.create_animations('move',character)
        self.create_animations('spell',character)
        self.create_animations('jump',character)

        self.spelling = False
        self.jumping = False
        self.double_jumping = False
        self.moving = False
        self.moving_right = False
        self.jump_animation = False

        self.W = W
        self.H = H
        self.velocity = 0
        self.acceleration = 0.6
        self.key = 0
        self.time = pygame.time.get_ticks()
        self.platforms = platforms
        self.fireballs = pygame.sprite.Group()

        self.image = self.idle_right_sprites[0][0]
        self.ground = round(self.H*0.942)
        self.fall_platform = False
        self.player_left = self.image
        self.player_right = pygame.transform.flip(self.player_left, True, False)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = x, y + 40
        self.life = 100
        self.life_image = pygame.image.load('media/life.png')
        self.life_image = pygame.transform.scale(self.life_image, (57, 57))
        self.tmp = 500

    def create_animations(self,sheet_name,directory):
        setattr(self,sheet_name+"_sheet",Spritesheet(directory+sheet_name+"-sheet.png"))
        setattr(self, sheet_name + "_right_sprites", [])
        setattr(self, sheet_name + "_left_sprites", [])
        for i in range(getattr(self,sheet_name+"_sheet").get_nb_sprites()):
            sprite, duration = getattr(self, sheet_name+"_sheet").parse_sprites(f"{sheet_name}{i}.png")
            sprite = pygame.transform.scale(sprite,(192,192))
            getattr(self, sheet_name + "_right_sprites").append([sprite,duration])
            getattr(self,sheet_name+"_left_sprites").append([pygame.transform.flip(sprite, True, False), duration])

    def move(self,dt,platforms):
        self.gravity(dt)
        copy = platforms.copy()
        if self.fall_platform:
            self.rect.y += 1
            platform_list = self.get_hits(copy)
            if platform_list:
                for tile in platform_list:
                    copy.remove(tile)
            else:
                self.fall_platform = False
        self.check_collision_y(copy)
        self.animate(dt)
        copy.empty()

    def change_animation(self):
        if self.jump_animation:
            if self.moving_right:
                self.image = self.jump_right_sprites[0][0]
            else:
                self.image = self.jump_left_sprites[0][0]
            self.tmp = self.jump_right_sprites[0][1]
        elif self.spelling:
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

    def animate(self,dt):
        if pygame.time.get_ticks()-self.time >= self.tmp:
            if self.jump_animation:
                if self.key == self.jump_sheet.get_nb_sprites()-1:
                    self.jump(dt)
                elif self.moving_right:
                    self.key += 1
                    self.image = self.jump_right_sprites[self.key][0]
                else:
                    self.key += 1
                    self.image = self.jump_left_sprites[self.key][0]
                self.tmp = self.jump_left_sprites[self.key][1]
            elif self.spelling:
                if self.key == self.spell_sheet.get_nb_sprites()-1:
                    self.spelling = False
                    if self.moving_right:
                        fireball = Fireball((self.rect.right, self.rect.centery), 1)
                    else:
                        fireball = Fireball((self.rect.left, self.rect.centery), -1)
                    fireball.add(self.fireballs)
                    self.change_animation()
                elif self.moving_right:
                    self.key += 1
                    self.image = self.spell_right_sprites[self.key][0]
                else:
                    self.key += 1
                    self.image = self.spell_left_sprites[self.key][0]
                self.tmp = self.spell_left_sprites[self.key][1]

            elif not self.moving:
                self.key = (self.key + 1) % self.idle_sheet.get_nb_sprites()
                self.tmp = self.idle_right_sprites[self.key][1]
                if self.moving_right:
                    self.image = self.idle_right_sprites[self.key][0]
                else:
                    self.image = self.idle_left_sprites[self.key][0]
            else:
                self.key = (self.key + 1) % self.move_sheet.get_nb_sprites()
                self.tmp = self.move_right_sprites[self.key][1]
                if not self.moving_right:
                    self.image = self.move_left_sprites[self.key][0]

                else:
                    self.image = self.move_right_sprites[self.key][0]

            self.time = pygame.time.get_ticks()

    def move_right(self, dt):
        if self.rect.x < self.W - self.image.get_width():
            self.rect.x += round(5 * dt)

    def move_left(self, dt):
        if self.rect.x > 0:
            self.rect.x -= round(5 * dt)

    def jump(self, dt):
        if not self.jump_animation and not self.jumping:
            self.jump_animation = True
            self.spelling = False
            self.change_animation()
        else:
            self.jump_animation = False
            if not self.jumping:
                self.jumping = True
            elif not self.double_jumping:
                self.double_jumping = True
            self.velocity = -15
            self.rect.y += self.velocity * dt

    def fall_down(self):
        if self.jumping or self.double_jumping:
            self.velocity += 20
        elif self.rect.bottom < self.ground - 10:
            self.fall_platform = True
            self.velocity += 15

    def gravity(self, dt):
        self.velocity += self.acceleration * dt
        self.rect.y += self.velocity * dt

    def check_collision_y(self, platforms):
        self.jumping = True
        self.rect.y += 1
        collisions = self.get_hits(platforms)
        for tile in collisions:
            if self.velocity > 0 and 0 <= (self.rect.bottom - tile.rect.y) < 40:
                self.jumping = False
                self.double_jumping = False
                self.velocity = 0
                self.rect.bottom = tile.rect.top
        if self.rect.bottom > self.ground :
            self.rect.bottom = self.ground

    def get_hits(self, sprite_group):
        hits = []
        for sprite in sprite_group:
            if pygame.sprite.collide_mask(self,sprite):
                hits.append(sprite)
        return hits
