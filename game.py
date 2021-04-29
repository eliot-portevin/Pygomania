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

        # Players
        self.players = ['Mage', 'Boxer', 'Dwarf', 'Soldier', 'Gorgone', 'Tenniswoman']
        self.character = 1
        # Number, Folder
        self.attacks_dict = {1: [1, 'media/Mage_animation/'], 2: [2, 'media/Boxer_animation/'],
                             3: [3, 'media/Dwarf_animation/'],
                             4: [4, 'media/Soldier_animation/'], 5: [5, 'media/Gorgone_animation/'],
                             6: [6, 'media/Tenniswoman_animation/']}

        self.player = Player(W, H, round(W / 2), round(203 / 216 * H), self.attacks_dict[self.character])
        self.player_sprites = pygame.sprite.Group()
        self.player_sprites.add(self.player)

        self.title_font = pygame.font.SysFont('toonaround', 180)
        self.title_text1 = self.title_font.render('Pygomania', True, (255, 255, 255))
        self.title_text2 = self.title_font.render('Pygomania', True, (0, 0, 0))

        self.prompt_font = pygame.font.SysFont('toonaround', 50)
        self.prompt1 = self.prompt_font.render('Press Space to Continue', True, (255, 255, 255))
        self.prompt2 = self.prompt_font.render('Press Space to Continue', True, (0, 0, 0))
        self.time = 0

        self.start_button = pygame.image.load('media/start_button.png')
        self.start_button = pygame.transform.scale(self.start_button, (230, 85))
        self.start_button_hovering = pygame.image.load('media/start_button_hovering.png')
        self.start_button_hovering = pygame.transform.scale(self.start_button_hovering, (230, 85))

        self.start_rect = pygame.Rect(self.W / 2 - self.start_button.get_width() / 2, self.H - 180, 230, 85)

        self.mouse_rect = pygame.Rect(0, 0, 1, 1)

        # Colours
        self.white = (255, 255, 255)
        self.button_colour = (217, 215, 126, 140)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0, 180)
        # Temporary values
        self.tmp = 1

        # Server values
        self.connected = False

    def text(self, font, fontsize, text, position):
        font = pygame.font.SysFont(font, fontsize)
        text_white = font.render(text, True, (255, 255, 255))
        text_black = font.render(text, True, (0, 0, 0))
        self.WINDOW.blit(text_black, (round(position[0] - text_white.get_width() / 2 - round(fontsize / 20)), position[1] + round(fontsize / 25)))
        self.WINDOW.blit(text_white, (round(position[0] - text_white.get_width() / 2), position[1]))

    def main_menu_func(self):
        self.WINDOW.blit(self.BG, (0, 0))
        self.text('toonaround', 90, 'Pygomania', (self.WINDOW.get_width() / 2, 70))
        self.mouse_rect.x, self.mouse_rect.y = pygame.mouse.get_pos()
        #First player line
        for i in range(3):
            s = pygame.Surface((200, 130), pygame.SRCALPHA)
            s.fill(self.button_colour)
            x = 150
            y = round(self.H / 5 * (i + 1.5))
            self.WINDOW.blit(s, (x, y))
            rect = pygame.Rect(x, y, 200, 130)
            if self.mouse_rect.colliderect(rect):
                self.WINDOW.blit(s, (x, y))

        #Second line
        for i in range(3):
            s = pygame.Surface((200, 130), pygame.SRCALPHA)
            s.fill(self.button_colour)
            x = self.W - (150 + s.get_width())
            y = round(self.H / 5 * (i + 1.5))
            self.WINDOW.blit(s, (x, y))
            rect = pygame.Rect(x, y, 200, 130)
            if self.mouse_rect.colliderect(rect):
                self.WINDOW.blit(s, (x, y))

        #Start button
        self.WINDOW.blit(self.start_button, (self.W / 2 - self.start_button.get_width() / 2, self.H - 180))

        if self.mouse_rect.colliderect(self.start_rect):
            self.WINDOW.blit(self.start_button_hovering, (self.W / 2 - self.start_button.get_width() / 2, self.H - 180))

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
