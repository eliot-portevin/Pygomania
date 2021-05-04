import pygame, time
from player import Player
from platforms import Platform

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

        # Platforms
        self.platforms = pygame.sprite.Group()
        surface = pygame.surface.Surface((200, 50), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 150))
        self.platform_1 = Platform(surface, pygame.rect.Rect(300, 500, 200, 50))
        self.platform_2 = Platform(surface,pygame.rect.Rect(900,500,200,50))
        surface = pygame.surface.Surface((W,round(H*0.0602)),pygame.SRCALPHA)
        surface.set_colorkey((0,0,0))
        self.ground = Platform(surface,pygame.rect.Rect(0,round(H*0.9398),W,H*0.0602))
        self.platforms.add(self.platform_1,self.platform_2,self.ground)

        # Players
        self.players = ['Mage', 'Boxer', 'Dwarf', 'Soldier', 'Gorgone', 'Tenniswoman']
        self.character = 0
        self.descriptions = open('media/descriptions.txt','r').readlines()
        self.stats = [['70', '5', '15', '25'],['85', '8', '15', '30'],['10', '1', '1', '2'],['70', '5', '15', '25'],
                      ['70', '5', '15', '25'],['70', '5', '15', '25']]
        self.stats_max = [100,10,20,35]
        self.stats_names = [['Health', 'Punch', 'Fireball', 'Lightning'],['Health','Punch','Spring Punch', 'Air KO'],
                            ['Health','Punch','Axe', 'Rage'],['Health','Punch','Words', 'Bear'],
                            ['Health','Punch','Snake', 'Stone'],['Health','Punch','Racket', 'Smash']]

        self.info_font = pygame.font.SysFont('toonaround', 18)
        self.menu_characters_dict = {}
        for i in range(6):
            self.menu_characters_dict[self.players[i]] = [self.descriptions[i][:-1],self.stats[i],self.stats_names[i]]
        # Number, Folder
        self.attacks_dict = ['media/Mage_animation/', 'media/Boxer_animation/',
                             'media/Dwarf_animation/', 'media/Soldier_animation/',
                             'media/Gorgone_animation/', 'media/Tenniswoman_animation/']

        self.player = Player(W, H, round(W / 2), round(23 / 216 * H), self.attacks_dict[self.character],self.platforms)
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
        self.prev_time = time.time()


        # Colours
        self.white = (255, 255, 255)
        self.button_colour = (217, 215, 126, 140)
        self.black = (0, 0, 0)
        self.black_transparent = (0, 0, 0, 150)
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
        self.WINDOW.blit(text_black, (round(position[0] - text_white.get_width() / 2 - round(fontsize / 20)),
                                      position[1] + round(fontsize / 25)))
        self.WINDOW.blit(text_white, (round(position[0] - text_white.get_width() / 2), position[1]))
        n = text_white.get_width()
        return n

    def box_text(self, surface, font, x_start, x_end, y_start, text, colour):
        x = x_start
        y = y_start
        words = text.split(' ')

        for word in words:
            word_t = font.render(word, True, colour)
            if word_t.get_width() + x <= x_end:
                surface.blit(word_t, (x, y))
                x += word_t.get_width() + 4
            else:
                y += word_t.get_height() + 5
                x = x_start
                surface.blit(word_t, (x, y))
                x += word_t.get_width() + 4

    def stats_text(self):
        x_name = self.W / 2 - 200
        x_stat = self.W / 2 + 180
        y = self.H / 3 + 20
        for i in range(4):
            stat_name = self.info_font.render(str(self.stats_names[self.character][i]), True, self.white)
            stat = self.info_font.render(str(self.stats[self.character][i]), True, self.white)
            self.WINDOW.blit(stat, (x_stat, y))
            self.WINDOW.blit(stat_name, (x_name, y))
            pygame.draw.rect(self.WINDOW, self.white, (self.W / 2 - 100, y + 5, int(self.stats[self.character][i])*300/self.stats_max[i], 10))
            y += 40

    def main_menu_func(self):
        self.WINDOW.blit(self.BG, (0, 0))
        self.text('toonaround', 90, 'Pygomania', (self.WINDOW.get_width() / 2, 70))
        self.mouse_rect.x, self.mouse_rect.y = pygame.mouse.get_pos()
        # First player line
        for i in range(3):
            s = pygame.Surface((200, 130), pygame.SRCALPHA)
            s.fill(self.button_colour)
            x = 150
            y = round(self.H / 5 * (i + 1.5))
            self.WINDOW.blit(s, (x, y))
            rect = pygame.Rect(x, y, 200, 130)
            if self.mouse_rect.colliderect(rect):
                self.WINDOW.blit(s, (x, y))
                self.character = i
            self.text('toonaround', 30, self.players[i], (150 + s.get_width() / 2, y + s.get_height() + 5))
            x = self.W - (150 + s.get_width())

        # Second line
        for i in range(3):
            s = pygame.Surface((200, 130), pygame.SRCALPHA)
            s.fill(self.button_colour)
            y = round(self.H / 5 * (i + 1.5))
            self.WINDOW.blit(s, (x, y))
            rect = pygame.Rect(x, y, 200, 130)
            if self.mouse_rect.colliderect(rect):
                self.character = i +3
                self.WINDOW.blit(s, (x, y))
            self.text('toonaround', 30, self.players[i + 3], (self.W - (150 + s.get_width() / 2), y +
                                                              s.get_height() + 5))

        # Start button
        self.WINDOW.blit(self.start_button, (self.W / 2 - self.start_button.get_width() / 2, self.H - 180))

        if self.mouse_rect.colliderect(self.start_rect):
            self.WINDOW.blit(self.start_button_hovering, (self.W / 2 - self.start_button.get_width() / 2, self.H - 180))

        # Information box
        info_box = pygame.Surface((450, 350), pygame.SRCALPHA)
        info_box.fill(self.black_transparent)
        self.WINDOW.blit(info_box, (self.W / 2 - info_box.get_width() / 2, self.H / 3))

        x_start = self.W / 2 - info_box.get_width() / 2 + 10
        self.box_text(self.WINDOW, self.info_font, x_start, x_start + 430, self.H / 1.7 -5, self.descriptions[self.character][:-1], self.white)

        self.stats_text()
    def connect(self):
        self.connected = True

    def update(self, dt):

        if self.keys.get(pygame.K_a):
            self.player.move_left(dt)
        if self.keys.get(pygame.K_d):
            self.player.move_right(dt)
        if self.keys.get(pygame.K_s):
            self.player.fall_down()

        self.player.gravity(dt)
        self.player.check_collision_y(self.platforms)
        self.player.animate()
        self.player_sprites.draw(self.WINDOW)
        self.platforms.draw(self.WINDOW)
        self.player.fireballs.draw(self.WINDOW)
        for fireball in self.player.fireballs:
            fireball.move(dt)
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
