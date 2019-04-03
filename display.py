import sys
import pygame
from pygame.locals import *


class PlayerObject:
    surface = pygame.Surface((20, 20))
    surface.fill(color.THECOLORS["red"])
    rect = Rect(surface.get_rect())


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    player = PlayerObject
    player.rect = player.rect.move(1 / 5 * 640, 4 / 5 * 480)
    speed = 10
    clock = pygame.time.Clock()
    while 1:
        tick = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        player.rect = player.rect.move(speed / tick, 0)
        screen.fill(color.THECOLORS["black"])
        screen.blit(player.surface, player.rect)
        pygame.display.flip()
        speed += 1
        print(player.rect.x, end="\r")


if __name__ == '__main__':
    main()
