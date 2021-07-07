import pygame
import socket
import threading
import time

from boxer import Boxer
from mage import Mage
from platforms import Platform
from server_functions import ServerClass


class Game:
    def __init__(self, win, W, H, BG):
        self.WINDOW = win
        self.W = W
        self.H = H
        self.WH = (W + H) / 2
        self.BG = BG

        self.server_funcs = ServerClass()

        # Colours
        self.white = (255, 255, 255)
        self.button_colour = (217, 215, 126, 140)
        self.button_colour_selected = (217, 215, 126, 190)
        self.black = (0, 0, 0)
        self.black_transparent = (0, 0, 0, 150)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0, 180)

        # Menu variables
        self.playing = True
        self.menu_open = True
        self.interface = False
        self.create = False
        self.join = False
        self.pause = False
        self.show_prompt = False
        self.main_menu = False
        self.waiting_for_other = False
        self.keys = {}
        self.key_events = {pygame.KEYDOWN: [], pygame.KEYUP: []}
        self.mouse_events = {pygame.MOUSEBUTTONDOWN: [], pygame.MOUSEBUTTONUP: []}
        self.mouse_buttons = {}

        # Platforms
        self.platforms = pygame.sprite.Group()
        surface = pygame.surface.Surface((round(self.W * 0.139), round(W * 0.056)), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 150))
        self.platform_1 = Platform(surface, pygame.rect.Rect(round(W * 0.174), round(H * 0.611), round(W * 0.139),
                                                             round(H * 0.056)))
        self.platform_2 = Platform(surface, pygame.rect.Rect(round(W * 0.694), round(H * 0.611), round(W * 0.139),
                                                             round(H * 0.056)))
        surface = pygame.surface.Surface((W, round(H * 0.0602)), pygame.SRCALPHA)
        surface.set_colorkey((0, 0, 0))
        self.ground = Platform(surface, pygame.rect.Rect(0, round(H * 0.942), W, H * 0.0602))
        self.platforms.add(self.platform_1, self.platform_2, self.ground)

        # Players
        self.character_class = {0: Mage, 1: Boxer}
        self.player = None
        self.player_2 = None
        self.players = ['Mage', 'Boxer', 'Dwarf', 'Soldier', 'Gorgone', 'Tenniswoman']
        self.character = -7
        self.character_2 = 0
        self.character_selected = -6
        self.descriptions = open('media/descriptions.txt', 'r').readlines()
        self.stats = [['70', '5', '15', '25'], ['85', '8', '15', '30'], ['10', '1', '1', '2'], ['70', '5', '15', '25'],
                      ['70', '5', '15', '25'], ['70', '5', '15', '25']]
        self.stats_max = [100, 10, 20, 35]
        self.stats_names = [['Health', 'Punch', 'Fireball', 'Lightning'], ['Health', 'Punch', 'Spring Punch', 'Air KO'],
                            ['Health', 'Punch', 'Axe', 'Rage'], ['Health', 'Punch', 'Words', 'Bear'],
                            ['Health', 'Punch', 'Snake', 'Stone'], ['Health', 'Punch', 'Racket', 'Smash']]
        self.attacks_dict = ['media/Mage_animation/', 'media/Boxer_animation/',
                             'media/Dwarf_animation/', 'media/Soldier_animation/',
                             'media/Gorgone_animation/', 'media/Tenniswoman_animation/']
        self.player_sprites = pygame.sprite.Group()

        # Menu values
        self.info_font = pygame.font.SysFont('toonaround', round(self.WH * 0.0154))
        self.menu_characters_dict = {}
        for i in range(6):
            self.menu_characters_dict[self.players[i]] = [self.descriptions[i][:-1], self.stats[i], self.stats_names[i]]
        self.title_font = pygame.font.SysFont('toonaround', round(self.WH * 0.154))
        self.title_font1 = self.title_font.render('Pygomania', True, (255, 255, 255))
        self.title_font2 = self.title_font.render('Pygomania', True, (0, 0, 0))

        self.prompt_font = pygame.font.SysFont('toonaround', round(self.WH * 0.043))
        self.prompt1 = self.prompt_font.render('Press Space to Continue', True, (255, 255, 255))
        self.prompt2 = self.prompt_font.render('Press Space to Continue', True, (0, 0, 0))
        self.start_button = pygame.image.load('media/start_button.png')
        self.start_button = pygame.transform.scale(self.start_button, (round(W * 0.16), round(H * 0.094)))
        self.start_button_hovering = pygame.image.load('media/start_button_hovering.png')
        self.start_button_hovering = pygame.transform.scale(self.start_button_hovering,
                                                            (round(W * 0.16), round(H * 0.094)))
        self.start_rect = pygame.Rect(self.W / 2 - self.start_button.get_width() / 2, round(self.H * 0.8),
                                      round(W * 0.16), round(H * 0.094))
        self.start = False

        self.join_text = self.text('toonaround', round(self.WH * 0.128), "Join", (round(W * 0.486), round(H * 0.278)))
        self.join_rect = self.join_text[0].get_rect(topleft=self.join_text[1])
        self.create_text = self.text('toonaround', round(self.WH * 0.128), "Create",
                                     (round(W * 0.486), round(H * 0.556)))
        self.create_rect = self.create_text[0].get_rect(topleft=self.create_text[1])
        self.waiting = self.text("toonaround", round(self.WH * 0.128), "Waiting for another player...",
                                 (round(W / 2), round(H * 0.444)))

        self.title_text = self.text('toonaround', round(self.WH * 0.077), 'Pygomania', (round(W / 2), round(H * 0.078)))
        self.rect_surface = pygame.surface.Surface((round(W * 0.139), round(H * 0.144)), pygame.SRCALPHA)
        self.rect_surface.fill(self.button_colour)
        self.rect_surfaces = []
        for i in range(6):
            self.rect_surfaces.append(self.rect_surface.copy())
        self.name_surfaces = []
        for x in range(2):
            for y in range(3):
                i = 3 * x + y
                self.name_surfaces.append(self.text('toonaround', round(self.WH * 0.0256), self.players[i],
                                                    (round(W * 0.653) * x + round(W * 0.174),
                                                     round(H * 0.2 * y + H * 0.45))))
        self.menu_rects = []
        for x in range(2):
            for y in range(3):
                self.menu_rects.append(
                    pygame.rect.Rect(round(W * 0.653) * x + round(W * 0.104), round(self.H * 0.2 * y + H * 0.3),
                                     self.rect_surface.get_width(),
                                     self.rect_surface.get_height()))
        self.info_box = pygame.Surface((round(W * 0.313), round(H * 0.389)), pygame.SRCALPHA)
        self.info_box.fill(self.black_transparent)
        self.x_start = round(W * 0.344) + round(self.W / 144)
        self.time = 0

        self.prev_time = time.time()

        # Temporary values
        self.tmp = 1

        # Server values
        self.connected = False
        SERVER = socket.gethostbyname(socket.gethostname())
        # SERVER = '192.168.1.126'
        self.HEADER = 16
        PORT = 10632
        self.ADDR = (SERVER, PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MSG = '!DISCONNECT'
        self.receive_object = [{},{},{},{},(0,0)]
        # toutes les touches vraies, les touches event, les boutons de la souris,
        # les boutons event, la position de la souris

    def text(self, font, fontsize, text, pos):
        font = pygame.font.SysFont(font, fontsize)
        text_white = font.render(text, True, (255, 255, 255))
        text_black = font.render(text, True, (0, 0, 1))
        surface = pygame.surface.Surface(
            (text_white.get_width() + round(fontsize / 20), text_white.get_height() + round(fontsize / 25)),
            pygame.SRCALPHA)
        surface.blit(text_black, (0, round(fontsize / 25)))
        surface.blit(text_white, (round(fontsize / 20), 0))
        x = pos[0] - round(surface.get_width() / 2)
        pos = (x, pos[1])
        return [surface, pos]

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
            stat_name = self.info_font.render(str(self.stats_names[self.character_selected][i]), True, self.white)
            stat = self.info_font.render(str(self.stats[self.character_selected][i]), True, self.white)
            self.WINDOW.blit(stat, (x_stat, y))
            self.WINDOW.blit(stat_name, (x_name, y))
            pygame.draw.rect(self.WINDOW, self.white, pygame.rect.Rect(self.W / 2 - 100, y + 5,
                                                                       int(self.stats[self.character_selected][
                                                                               i]) * 300 / self.stats_max[i], 10))
            y += 40

    def main_menu_func(self):
        if not self.waiting_for_other:
            self.WINDOW.blit(self.title_text[0], self.title_text[1])
            for i in range(6):
                rect = self.menu_rects[i]
                self.WINDOW.blit(self.rect_surfaces[i], (rect.x, rect.y))
                self.WINDOW.blit(self.name_surfaces[i][0], self.name_surfaces[i][1])

            # Start button
            if not self.start:
                self.WINDOW.blit(self.start_button, self.start_rect)
            else:
                self.WINDOW.blit(self.start_button_hovering, self.start_rect)
            if self.character >= 0:
                pygame.draw.rect(self.WINDOW, (217, 215, 126), self.menu_rects[self.character], 10)

            # Information box
            self.WINDOW.blit(self.info_box, (self.W / 2 - self.info_box.get_width() / 2, self.H / 3))
            if self.character_selected >= 0:
                self.box_text(self.WINDOW, self.info_font, self.x_start, self.x_start + 430, self.H / 1.7 - 5,
                              self.descriptions[self.character_selected][:-1], self.white)

                self.stats_text()
        else:
            self.WINDOW.blit(self.waiting[0], self.waiting[1])

    def main_menu_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                for rect in self.menu_rects:
                    if rect.collidepoint(e.pos[0], e.pos[1]):
                        self.character = self.menu_rects.index(rect)
                if self.start and self.character >= 0:
                    x = round(4 * self.W / 5)
                    self.server_funcs.send(["Play", self.character], self.client)
                    if self.player_2 is not None:
                        self.main_menu = False
                        threading.Thread(target=self.send_online).start()
                        threading.Thread(target=self.receive_online).start()
                        x = round(self.W / 5)
                    else:
                        self.waiting_for_other = True
                    self.player = self.character_class[self.character](self.W, self.H, x, round(23 / 216 * self.H),
                                                                       self.attacks_dict[self.character],
                                                                       self.platforms)
                    self.player_sprites.add(self.player)

            elif e.type == pygame.MOUSEMOTION:
                for rect in self.menu_rects:
                    index = self.menu_rects.index(rect)
                    if rect.collidepoint(e.pos[0], e.pos[1]):
                        if index == self.character_selected:
                            break
                        surface = self.rect_surfaces[index]
                        surface.fill(self.button_colour_selected)
                        self.character_selected = index
                    elif index != self.character_selected:
                        surface = self.rect_surfaces[index]
                        surface.fill(self.button_colour)
                self.start = False
                if self.start_rect.collidepoint(e.pos[0], e.pos[1]):
                    self.start = True

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.server_funcs.send(socket.gethostname(), self.client)
        self.connected = True

    def move_character(self, keys, player, dt):
        if keys.get(pygame.K_a):
            player.move_left(dt)
        if keys.get(pygame.K_d):
            player.move_right(dt)

    def update(self, dt):
        self.move_character(self.keys, self.player, dt)
        self.move_character(self.receive_object[0], self.player_2, dt)

        for players in self.player_sprites:
            players.move(dt, self.platforms)
        self.BG.blit(self.player.life_image, (40, 60))
        self.player_sprites.draw(self.WINDOW)
        self.platforms.draw(self.WINDOW)
        if self.character == 0:
            self.update_mage(dt, self.player, pygame.mouse.get_pos()[0], True)
        if self.character_2 == 0:
            self.update_mage(dt, self.player_2, self.receive_object[4][0], False)
        # Life Bar

        if self.tmp == 1:
            shape_surf = pygame.Surface(pygame.Rect((120, 66, 4 * self.player.life, 40)).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, self.red, shape_surf.get_rect())
            self.BG.blit(shape_surf, (120, 66, 4 * self.player.life, 40))
            self.tmp += 1
        pygame.draw.rect(self.BG, self.white, (120, 66, 400, 40), 4)

    def update_mage(self, dt, player, mouse_pos, blit):
        if player.ulti_time_seconds != 0 and blit:
            player.timer((round(self.W / 2), 0), self.prompt_font, self.WINDOW, (0, 0, 0), 'ulti_time_seconds',
                         'ulti_temp_time')
        player.fireballs.draw(self.WINDOW)
        player.laser_beam.draw(self.WINDOW)
        player.ulti_prevision(self.WINDOW, mouse_pos, blit)
        other_player = self.player
        if blit:
            other_player = self.player_2
        for fireball in player.fireballs:
            fireball.move(dt)
            if pygame.sprite.collide_mask(fireball,other_player):
                other_player.damage(fireball.damage)
        for laser in player.laser_beam:
            laser.check()

    def events(self,):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.key_events[pygame.KEYDOWN].append(event.key)
                self.keys[event.key] = True
                if event.key == pygame.K_w and not self.player.double_jumping:
                    self.player.jump()
                elif event.key == pygame.K_q:
                    if self.character == 0:
                        if not self.player.spelling and not self.player.ulti:
                            self.player.spelling = True
                    elif self.character == 1:
                        self.player.punching = True
                    self.player.change_animation()
                elif event.key == pygame.K_a:
                    if self.keys.get(pygame.K_d):
                        self.player.moving = False
                    else:
                        self.player.moving_right = False
                        self.player.moving = True
                    self.player.change_animation()
                elif event.key == pygame.K_s:
                    self.player.fall_down()
                elif event.key == pygame.K_e:
                    if self.character == 0:
                        if not self.player.planning_ulti and self.player.ulti_time_seconds == 0:
                            self.player.planning_ulti = True
                elif event.key == pygame.K_d:
                    if self.keys.get(pygame.K_a):
                        self.player.moving = False
                    else:
                        self.player.moving_right = True
                        self.player.moving = True
                    self.player.change_animation()
            elif event.type == pygame.KEYUP:
                self.key_events[pygame.KEYUP].append(event.key)
                self.keys[event.key] = False
                if event.key == pygame.K_e and self.player.planning_ulti and not self.player.ulti and self.player.ulti_time_seconds == 0:
                    self.player.planning_ulti = False
                    self.player.ulti = True
                    self.player.change_animation()
                if event.key in {pygame.K_a, pygame.K_d}:
                    if not (self.keys.get(pygame.K_a) or self.keys.get(pygame.K_d)):
                        self.player.moving = False
                    elif self.keys.get(pygame.K_a):
                        self.player.moving = True
                        self.player.moving_right = False
                    elif self.keys.get(pygame.K_d):
                        self.player.moving_right = True
                        self.player.moving = True
                    self.player.change_animation()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_events[pygame.MOUSEBUTTONDOWN].append(event.button)
                self.mouse_buttons[event.button] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_events[pygame.MOUSEBUTTONUP].append(event.button)
                self.mouse_buttons[event.button] = False
                if event.button == 3 and self.player.planning_ulti:
                    self.player.planning_ulti = False
            elif event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
    def events_2(self):
        for keydown in self.receive_object[1][pygame.KEYDOWN]:
            if keydown == pygame.K_w and not self.player_2.double_jumping:
                self.player_2.jump()
            elif keydown == pygame.K_q:
                if self.character_2 == 0:
                    if not self.player_2.spelling and not self.player_2.ulti:
                        self.player_2.spelling = True
                elif self.character_2 == 1:
                    self.player_2.punching = True
                self.player_2.change_animation()
            elif keydown == pygame.K_a:
                if self.receive_object[0].get(pygame.K_d):
                    self.player_2.moving = False
                else:
                    self.player_2.moving_right = False
                    self.player_2.moving = True
                self.player_2.change_animation()
            elif keydown == pygame.K_s:
                self.player_2.fall_down()
            elif keydown == pygame.K_e:
                if self.character_2 == 0:
                    if not self.player_2.planning_ulti and self.player_2.ulti_time_seconds == 0:
                        self.player_2.planning_ulti = True
            elif keydown == pygame.K_d:
                if self.receive_object[0].get(pygame.K_a):
                    self.player_2.moving = False
                else:
                    self.player_2.moving_right = True
                    self.player_2.moving = True
                self.player_2.change_animation()
        for keyup in self.receive_object[1][pygame.KEYUP]:
            if keyup == pygame.K_e:
                if self.character_2 == 0:
                    if self.player_2.planning_ulti and not self.player_2.ulti and self.player_2.ulti_time_seconds == 0:
                        self.player_2.planning_ulti = False
                        self.player_2.ulti = True
                        self.player_2.change_animation()
            if keyup in {pygame.K_a, pygame.K_d}:
                if not (self.receive_object[0].get(pygame.K_a) or self.receive_object[0].get(pygame.K_d)):
                    self.player_2.moving = False
                elif self.receive_object[0].get(pygame.K_a):
                    self.player_2.moving = True
                    self.player_2.moving_right = False
                elif self.receive_object[0].get(pygame.K_d):
                    self.player_2.moving_right = True
                    self.player_2.moving = True
                self.player_2.change_animation()
        for mouseup in self.receive_object[3][pygame.MOUSEBUTTONUP]:
            if mouseup == 3:
                if self.character_2 == 0:
                    if self.player_2.planning_ulti:
                        self.player_2.planning_ulti = False

    def menu_update(self):
        self.WINDOW.blit(self.title_font2,
                         (round(self.W / 2 - self.title_font2.get_width() / 2 - 7), round(self.H / 2.6 + 7)))
        self.WINDOW.blit(self.title_font1, (round(self.W / 2 - self.title_font1.get_width() / 2), round(self.H / 2.6)))
        if self.show_prompt:
            self.WINDOW.blit(self.prompt2,
                             (round(self.W / 2 - self.prompt2.get_width() / 2 - 3), round(self.H / 1.55 + 3)))
            self.WINDOW.blit(self.prompt1, (round(self.W / 2 - self.prompt1.get_width() / 2), round(self.H / 1.55)))

        if pygame.time.get_ticks() - self.time > 500:
            self.show_prompt = not self.show_prompt
            self.time = pygame.time.get_ticks()

    def menu_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
            elif e.type == pygame.KEYUP:
                if e.key in {pygame.K_SPACE, pygame.K_KP_ENTER}:
                    self.menu_open = False
                    self.interface = True

    def pause_screen(self):
        if self.pause:
            self.WINDOW.blit(self.title_font2,
                             (round(self.W / 2 - self.title_font2.get_width() / 2 - 7), round(self.H / 2.6 + 7)))
            self.WINDOW.blit(self.title_font2,
                             (round(self.W / 2 - self.title_font2.get_width() / 2 - 7), round(self.H / 2.6 + 7)))

    def interface_screen(self):
        if not self.join and not self.create:
            self.WINDOW.blit(self.join_text[0], self.join_text[1])
            self.WINDOW.blit(self.create_text[0], self.create_text[1])
        elif self.create:
            self.WINDOW.blit(self.waiting[0], self.waiting[1])
        elif self.join:
            for i in self.server_funcs.games:
                self.WINDOW.blit(i[1][0], i[1][1])

    def interface_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    if not self.join and not self.create:
                        if self.join_rect.collidepoint(e.pos):
                            self.join = True
                            self.server_funcs.send("Games", self.client)
                            self.server_funcs.games = self.server_funcs.receive(self.client)
                            for i in range(len(self.server_funcs.games)):
                                text = self.text('toonaround', 60, self.server_funcs.games[i],
                                                 (round(self.W / 2), i * 300 + 200))
                                self.server_funcs.games[i] = [self.server_funcs.games[i], text]
                        elif self.create_rect.collidepoint(e.pos):
                            self.server_funcs.send(["Create", socket.gethostname()], self.client)
                            self.create = True
                            thread = threading.Thread(target=self.waiting_receive)
                            thread.start()
                    elif self.join:
                        for i in self.server_funcs.games:
                            if i[1][0].get_rect(topleft=i[1][1]).collidepoint(e.pos):
                                self.server_funcs.send(["join", i[0]], self.client)
                                self.create = True
                                thread = threading.Thread(target=self.waiting_receive)
                                thread.start()
                                break
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.join = False

    def waiting_receive(self):
        message = self.server_funcs.receive(self.client)
        if message is not None:
            if self.interface:
                self.interface = False
                self.main_menu = True
                thread = threading.Thread(target=self.waiting_receive)
                thread.start()
            elif self.main_menu:
                x = round(4 * self.W / 5)
                if self.player:
                    x = round(self.W / 5)
                self.character_2 = message
                print(message)
                self.player_2 = self.character_class[message](self.W, self.H, x, round(23 / 216 * self.H),
                                                              self.attacks_dict[message], self.platforms)
                self.player_sprites.add(self.player_2)
                if self.player is not None:
                    self.main_menu = False
                    threading.Thread(target=self.send_online).start()
                    threading.Thread(target=self.receive_online).start()

    def send_online(self):
        while not self.player_2 and not self.player:
            time.sleep(0.5)
        while self.playing:
            time.sleep(0.05)
            send_object = [self.keys, self.key_events, self.mouse_buttons, self.mouse_events,
                           pygame.mouse.get_pos()]
            self.server_funcs.send(["Play", send_object], self.client)
            self.key_events = {pygame.KEYDOWN: [], pygame.KEYUP: []}
            self.mouse_events = {pygame.MOUSEBUTTONDOWN: [], pygame.MOUSEBUTTONUP: []}

    def receive_online(self):
        while not self.player_2 and not self.player:
            time.sleep(0.5)
        while self.playing:
            self.receive_object = self.server_funcs.receive(self.client)
            self.events_2()



