import pygame
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
    FPS = 60
    clock = pygame.time.Clock()

    while playing:
        win.fill((0,0,0))
        clock.tick(FPS)
        win.blit(BG, (0, 0))

        if game.menu_open:
            game.menu_update()
        elif game.pause:
            game.pause_screen()
        else:
            game.update()

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                game.keys[event.key] = True
                if event.key == pygame.K_w and not (game.player.jumping and game.player.double_jumping):
                    game.player.jump()
                if event.key == pygame.K_q:
                    if not game.player.punching:
                        game.player.punching = True
                        game.player.key = 0
                if event.key == pygame.K_a:
                    game.player.moving_right = False
                    game.player.moving = True
                    game.player.key = 0
                if event.key == pygame.K_d:
                    game.player.moving_right = True
                    game.player.moving = True
                    game.player.key = 0
                if event.key == pygame.K_SPACE and game.menu_open:
                    game.menu_open = False
                if event.key == pygame.K_ESCAPE and game.pause and not game.menu_open:
                    game.pause = False
                if event.key == pygame.K_ESCAPE and not game.menu_open:
                    game.pause = True
            elif event.type == pygame.KEYUP:
                game.keys[event.key] = False
                if event.key in {pygame.K_a,pygame.K_d}:
                    if not (game.keys.get(pygame.K_a) and game.keys.get(pygame.K_d)):
                        game.player.moving = False
                        game.player.key = 0
                    elif game.keys.get(pygame.K_a):
                        game.player.moving_right = False
                        game.player.key = 0
                    elif game.keys.get(pygame.K_d):
                        game.player.moving_right = True
                        game.player.key = 0
            elif event.type == pygame.QUIT:
                playing = False
                pygame.quit()


if __name__ == '__main__':
    main()