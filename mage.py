import pygame
from player import Player
from fireball import Fireball
from laser_beam import Laser_Beam


class Mage(Player):
    def __init__(self, W, H, x, y, dir, platform):
        super().__init__(W, H, x, y, "media/Mage_animation/", platform)

        self.fireballs = pygame.sprite.Group()
        self.laser_beam = pygame.sprite.GroupSingle()

        self.create_animations('move')
        self.create_animations('spell')
        self.create_animations('jump')
        self.create_animations('ultimate')

        self.planning_ulti = False
        self.ulti = False
        self.ulti_prev_surf = pygame.surface.Surface((150, (round(self.H * 0.03))), pygame.SRCALPHA)
        self.ulti_prev_surf_alpha = 0
        self.ulti_pos = 0
        self.ulti_max_time = 5
        self.ulti_time_seconds = 0
        self.ulti_temp_time = 0

    def change_animation(self):
        if self.jump_animation:
            if self.moving_right:
                self.image = self.jump_right_sprites[0][0]
            else:
                self.image = self.jump_left_sprites[0][0]
            self.tmp = self.jump_right_sprites[0][1]
        elif self.ulti:
            if self.moving_right:
                self.image = self.ultimate_right_sprites[0][0]
            else:
                self.image = self.ultimate_left_sprites[0][0]
            self.tmp = self.ultimate_right_sprites[0][1]
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
        x, bottom = self.rect.x, self.rect.bottom
        self.rect = self.image.get_rect(x=x, bottom=bottom)
        self.key = 0
        self.time = pygame.time.get_ticks()

    def animate(self, dt):
        if pygame.time.get_ticks() - self.time >= self.tmp:
            if self.jump_animation:
                if self.key == self.jump_sheet.get_nb_sprites() - 1:
                    self.jump(dt)
                elif self.moving_right:
                    self.key += 1
                    self.image = self.jump_right_sprites[self.key][0]
                else:
                    self.key += 1
                    self.image = self.jump_left_sprites[self.key][0]
                self.tmp = self.jump_left_sprites[self.key][1]
            elif self.ulti:
                if self.key == self.ultimate_sheet.get_nb_sprites() - 1:
                    self.ulti = False
                    self.change_animation()
                elif self.key == self.ultimate_sheet.get_nb_sprites() - 2:
                    laser = Laser_Beam(self.W, self.H, self.ulti_pos)
                    self.laser_beam.add(laser)
                    self.key += 1
                    self.ulti_prev_surf_alpha = 5
                    self.ulti_prev_surf.fill((0, 0, 0, self.ulti_prev_surf_alpha))
                    self.ulti_temp_time = pygame.time.get_ticks()
                    self.ulti_time_seconds = 5
                else:
                    self.ulti_prev_surf_alpha += 15
                    self.ulti_prev_surf.fill((0, 0, 0, self.ulti_prev_surf_alpha))
                    if self.moving_right:
                        self.key += 1
                        self.image = self.ultimate_right_sprites[self.key][0]
                    else:
                        self.key += 1
                        self.image = self.ultimate_left_sprites[self.key][0]
                self.tmp = self.ultimate_left_sprites[self.key][1]
            elif self.spelling:
                if self.key == self.spell_sheet.get_nb_sprites() - 1:
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
            x, bottom = self.rect.x, self.rect.bottom
            self.rect = self.image.get_rect(x=x, bottom=bottom)
            self.time = pygame.time.get_ticks()

    def ulti_prevision(self, surf, pos, blit):
        if self.planning_ulti:
            x = pos
            self.ulti_pos = x
            if self.rect.x - x > 0 and self.moving_right:
                self.moving_right = False
                self.change_animation()
            elif self.rect.x - x < 0 and not self.moving_right:
                self.moving_right = True
                self.change_animation()
            w = round(self.W * 0.15)
            if blit:
                surface = pygame.surface.Surface((150, self.ground), pygame.SRCALPHA)
                surface.fill((0, 0, 0, 100))
                surf.blit(surface, (x - w / 2, 0))
        if self.ulti:
            surf.blit(self.ulti_prev_surf, (self.ulti_pos - round(self.W * 0.075), self.ground))
