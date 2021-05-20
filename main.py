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


def main():
    playing = True
    fps = 60
    clock = pygame.time.Clock()

    while playing:

        clock.tick(fps)
        dt = (time.time() - game.prev_time)*50
        game.prev_time = time.time()
        win.blit(BG, (0, 0))
        if not game.connected:
            game.connect()
        if game.menu_open:
            game.menu_update()
        elif game.pause:
            game.pause_screen()
        elif game.main_menu:
            game.main_menu_func()
        else:
            game.update(dt)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                game.keys[event.key] = True
                if event.key == pygame.K_w and not game.player.double_jumping :
                    game.player.jump(dt)
                elif event.key == pygame.K_q:
                    if not game.player.spelling and not game.player.ulti:
                        game.player.spelling = True
                        game.player.change_animation()
                elif event.key == pygame.K_a:
                    if game.keys.get(pygame.K_d):
                        game.player.moving = False
                    else:
                        game.player.moving_right = False
                        game.player.moving = True
                    game.player.change_animation()
                elif event.key == pygame.K_s:
                    game.player.fall_down()
                elif event.key == pygame.K_e:
                    game.player.planning_ulti = True
                elif event.key == pygame.K_d:
                    if game.keys.get(pygame.K_a):
                        game.player.moving = False
                    else:
                        game.player.moving_right = True
                        game.player.moving = True
                    game.player.change_animation()
                elif event.key == pygame.K_SPACE and game.menu_open:
                    game.menu_open = False
                    game.main_menu = True
            elif event.type == pygame.KEYUP:
                game.keys[event.key] = False
                if event.key == pygame.K_e and game.player.planning_ulti:
                    game.player.planning_ulti = False
                    game.player.ulti = True
                    game.player.change_animation()
                if event.key in {pygame.K_a, pygame.K_d}:
                    if not (game.keys.get(pygame.K_a) or game.keys.get(pygame.K_d)):
                        game.player.moving = False
                    elif game.keys.get(pygame.K_a):
                        game.player.moving = True
                        game.player.moving_right = False
                    elif game.keys.get(pygame.K_d):
                        game.player.moving_right = True
                        game.player.moving = True
                    game.player.change_animation()
            if event.type == pygame.MOUSEBUTTONUP:
                game.mouse_rect.x, game.mouse_rect.y = pygame.mouse.get_pos()
                if game.mouse_rect.colliderect(game.start_rect):
                    game.main_menu = False
                if event.button == 3 and game.player.planning_ulti:
                    game.player.planning_ulti = False
            elif event.type == pygame.QUIT:
                playing = False
                pygame.quit()


if __name__ == '__main__':
    main()
