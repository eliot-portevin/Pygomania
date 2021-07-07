import pygame

from spritesheet import Spritesheet


class Player(pygame.sprite.Sprite):
    def __init__(self, W, H, x, y, character, platforms):
        super().__init__()
        self.dir = character

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

        self.spelling = False
        self.jumping = False
        self.double_jumping = False
        self.moving = False
        self.moving_right = False
        self.jump_animation = False

        self.create_animations("idle")

        self.W = W
        self.H = H
        self.velocity = 0
        self.acceleration = 0.6
        self.key = 0
        self.time = pygame.time.get_ticks()
        self.platforms = platforms

        self.ground = round(self.H * 0.942)
        self.fall_platform = False
        self.image = self.idle_right_sprites[0][0]
        self.player_left = self.image
        self.player_right = pygame.transform.flip(self.player_left, True, False)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = x, y + 40
        self.life = 100
        self.life_max = self.life
        self.life_image = pygame.image.load('media/life.png')
        self.life_image = pygame.transform.scale(self.life_image, (57, 57))
        self.tmp = 500

    def create_animations(self, sheet_name, agrandissement=192 / 19, w_normal=True):
        setattr(self, sheet_name + "_sheet", Spritesheet(self.dir + sheet_name + "-sheet.png"))
        setattr(self, sheet_name + "_right_sprites", [])
        setattr(self, sheet_name + "_left_sprites", [])
        for i in range(getattr(self, sheet_name + "_sheet").get_nb_sprites()):
            sprite, duration = getattr(self, sheet_name + "_sheet").parse_sprites(f"{sheet_name}{i}.png")
            w, h = sprite.get_width(), sprite.get_height()
            if w_normal:
                size = round(sprite.get_width() * agrandissement)
                size2 = round(h * size / w)
            else:
                size2 = round(sprite.get_height() * agrandissement)
                size = round(w * size2 / h)
            sprite = pygame.transform.scale(sprite, (size, size2))
            getattr(self, sheet_name + "_right_sprites").append([sprite, duration])
            getattr(self, sheet_name + "_left_sprites").append([pygame.transform.flip(sprite, True, False), duration])

    def move(self, dt, platforms, window):
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

    def timer(self, pos, font, surface, color, variable, temp_variable):
        if pygame.time.get_ticks() - getattr(self, temp_variable) > 1000:
            setattr(self, variable, getattr(self, variable) - 1)
            setattr(self, temp_variable, pygame.time.get_ticks())
        text = font.render(str(getattr(self, variable)), True, color)
        rect = text.get_rect(topleft=pos)
        surface.blit(text, (rect.centerx, pos[1]))

    def move_right(self, dt):
        if self.rect.x < self.W - self.image.get_width():
            self.rect.x += round(5 * dt)

    def move_left(self, dt):
        if self.rect.x > 0:
            self.rect.x -= round(5 * dt)

    def jump(self):
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
            self.rect.y += self.velocity * 0.5

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
        if self.rect.bottom > self.ground:
            self.rect.bottom = self.ground

    def get_hits(self, sprite_group):
        hits = []
        for sprite in sprite_group:
            if pygame.sprite.collide_mask(self, sprite):
                hits.append(sprite)
        return hits
    def damage(self,amount):
        if self.life < amount:
            # Il est mort
            self.life = 0
            pass
        else:
            self.life -= amount
