import pygame
from player import Player


class Game:
    def __init__(self, win, W, H, BG):
        self.WINDOW = win
        self.W = W
        self.H = H
        self.BG = BG

        # Menu variables
        self.menu_open = True
        self.pause = False
        self.show_prompt = False
        self.main_menu = False
        self.keys = {}

        # Variables related to the characters
        self.character = 1
        # Mage:1, Boxer:2, Dwarf:3, Soldier:4, Gorgone:5, Tenniswoman:6
        # Number, Folder
        self.attacks_dict = {1: [1, 'media/Mage_animation/'], 2: [2, 'media/Boxer_animation/'],
                             3: [3, 'media/Dwarf_animation/'],
                             4: [4, 'media/Soldier_animation/'], 5: [5, 'media/Gorgone_animation/'],
                             6: [6, 'media/Tenniswoman_animation/']}

        self.player = Player(W, H, round(W / 2), round(203 / 216 * H),self.attacks_dict[self.character])
        self.player_sprites = pygame.sprite.Group()
        self.player_sprites.add(self.player)

        self.title_font = pygame.font.SysFont('toonaround', 180)
        self.title_text1 = self.title_font.render('Pygomania', True, (255, 255, 255))
        self.title_text2 = self.title_font.render('Pygomania', True, (0, 0, 0))

        self.prompt_font = pygame.font.SysFont('toonaround', 50)
        self.prompt1 = self.prompt_font.render('Press Space to Continue', 1, (255, 255, 255))
        self.prompt2 = self.prompt_font.render('Press Space to Continue', 1, (0, 0, 0))
        self.time = 0

        # Colours
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0, 180)
        # Temporary values
        self.tmp = 1

        # Server values
        self.connected = False

    def text(self, font, fontsize, text, position):
        font = pygame.font.SysFont(font, fontsize)
        text_white = font.render(text, 1, (255, 255, 255))
        text_black = font.render(text, 1, (0, 0, 0))
        self.WINDOW.blit(text_black, (
        round(position[0] - text_white.get_width() / 2 - round(fontsize / 20)), position[1] + round(fontsize / 25)))
        self.WINDOW.blit(text_white, (round(position[0] - text_white.get_width() / 2), position[1]))

    def main_menu_func(self):
        self.WINDOW.blit(self.BG, (0, 0))
        self.text('toonaround', 70, 'Pygomania', (self.WINDOW.get_width() / 2, 70))

    def connect(self):
        self.connected = True
        pass

    def update(self):
        if self.keys.get(pygame.K_a):
            self.player.move_left()
        if self.keys.get(pygame.K_d):
            self.player.move_right()
        if self.keys.get(pygame.K_s):
            self.player.fall_down()

        self.player.gravity()
        self.player.animate()
        self.player.check_height()
        self.player_sprites.draw(self.WINDOW)
        self.player.fireballs.draw(self.WINDOW)
        for fireball in self.player.fireballs:
            fireball.move()
        # Life Bar
        self.BG.blit(self.player.life_image, (40, 60))
        if self.tmp == 1:
            shape_surf = pygame.Surface(pygame.Rect((120, 66, 4 * self.player.life, 40)).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, self.red, shape_surf.get_rect())
            self.BG.blit(shape_surf, (120, 66, 4 * self.player.life, 40))
            self.tmp += 1
        pygame.draw.rect(self.BG, self.white, (120, 66, 400, 40), 4)

    def menu_update(self):
        self.WINDOW.blit(self.title_text2,
                         (round(self.W / 2 - self.title_text2.get_width() / 2 - 7), round(self.H / 2.6 + 7)))
        self.WINDOW.blit(self.title_text1, (round(self.W / 2 - self.title_text1.get_width() / 2), round(self.H / 2.6)))
        if self.show_prompt:
            self.WINDOW.blit(self.prompt2,
                             (round(self.W / 2 - self.prompt2.get_width() / 2 - 3), round(self.H / 1.55 + 3)))
            self.WINDOW.blit(self.prompt1, (round(self.W / 2 - self.prompt1.get_width() / 2), round(self.H / 1.55)))

        if pygame.time.get_ticks() - self.time > 500:
            self.show_prompt = not self.show_prompt
            self.time = pygame.time.get_ticks()

    def pause_screen(self):
        if self.pause:
            self.WINDOW.blit(self.title_text2,
                             (round(self.W / 2 - self.title_text2.get_width() / 2 - 7), round(self.H / 2.6 + 7)))
            self.WINDOW.blit(self.title_text2,
                             (round(self.W / 2 - self.title_text2.get_width() / 2 - 7), round(self.H / 2.6 + 7)))
