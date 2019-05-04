import sys
import pygame
from pygame.locals import *

WIDTH = 800
HEIGHT = 640


class PlayerObject:
    surface = pygame.Surface((20, 20))
    surface.fill(color.THECOLORS["red"])
    rect = Rect(surface.get_rect())

    def jump(self):
        pass


class ScoreObject:
    def __init__(self, score):
        print(score)
        self.surface = pygame.Surface((100, 1 / 5 * HEIGHT))
        self.surface.fill(color.THECOLORS["gray"])
        self.score = score
        self.rect = Rect(self.surface.get_rect())
        self.rect = pygame.draw.line(self.surface, color.THECOLORS["black"], (0, 0), (0, 1 / 10 * HEIGHT), 5)
        # self.rect = self.rect.move(1 / 5 * WIDTH + score, 4 / 5 * HEIGHT)
        font = pygame.font.Font(None, 20)
        font_surface = font.render(str(score), True, color.THECOLORS["black"], color.THECOLORS["gray"])
        self.surface.blit(font_surface, (5, 1 / 10 * HEIGHT))



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player = PlayerObject()
    player.rect = player.rect.move(1 / 5 * WIDTH, 4 / 5 * HEIGHT - 20)
    position = 0
    speed = 30
    scores = []
    clock = pygame.time.Clock()
    for i in range(0, 9):
        new_score = ScoreObject(i * 100)
        new_score.rect = new_score.rect.move(1 / 5 * WIDTH + i * 100, 4 / 5 * HEIGHT)
        scores.append(new_score)
    while 1:
        tick = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                player.jump()
        screen.fill(color.THECOLORS["black"])
        for score in scores:
            score.rect = score.rect.move(-speed/tick, 0)
            screen.blit(score.surface, score.rect)
        if scores[-1].rect.x < WIDTH - 100:
            new_score = ScoreObject(scores[-1].score + 100)
            new_score.rect = new_score.rect.move(scores[-1].rect.x + 100, 4 / 5 * HEIGHT)
            scores.append(new_score)
        screen.blit(player.surface, player.rect)
        pygame.display.flip()
        position += speed
        print(player.rect.x, end="\r")


if __name__ == '__main__':
    main()
