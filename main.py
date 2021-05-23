import pygame
import time
from game import Game

pygame.init()

win = pygame.display.set_mode((1440, 900))
W, H = win.get_width(), win.get_height()

pygame.display.set_caption('Pygomania')
pygame.display.set_icon(pygame.image.load('media/player.png'))

BG = pygame.image.load('media/background.jpg').convert()
BG = pygame.transform.scale(BG, (W, H))

game = Game(win, W, H, BG)
clock = pygame.time.Clock()


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = game.prompt_font.render(fps + "  FPS", 1, (130,100,70))
    return fps_text


def main():
    fps = 60

    while game.playing:

        clock.tick(fps)
        dt = (time.time() - game.prev_time)*50
        game.prev_time = time.time()
        win.blit(BG, (0, 0))
        if not game.connected:
            game.connect()
        if game.menu_open:
            game.menu_update()
            game.menu_events()
        elif game.pause:
            game.pause_screen()
        elif game.main_menu:
            game.main_menu_func()
            game.main_menu_events()
        else:
            game.update(dt)
            game.events(dt)
        win.blit(update_fps(),(0,0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
