import random

import pygame
from pygame.locals import *

WIDTH = 800
HEIGHT = 640


class Gem:
    def __init__(self, image):
        self.image = image


class Game:
    def __init__(self):
        pygame.init()
        self.score = 0
        self._running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.score = 0
        self._selected = (-1, -1)
        shapes = ["red", "blue", "green", "purple", "yellow", "orange", "white"]
        self.shapes = [pygame.image.load("img/{}.bmp".format(shape)) for shape in shapes]
        self.board = [[Gem(self.shapes[random.randrange(7)]) for _ in range(8)] for _ in range(8)]

    def draw(self):
        for i in range(8):
            for j in range(8):
                self.screen.blit(self.board[i][j].image, (150 + 64 * i, 100 + 64 * j))


    def execute(self):
        while self._running:
            tick = self.clock.tick(60)
            self.events_handler()
            self.check_movement()
            self.screen.fill(color.THECOLORS["black"])
            self.draw()
            pygame.display.flip()

    def events_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == MOUSEBUTTONDOWN:
                self._selected = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONUP:
                self._selected = (-1, -1)

    def check_movement(self):
        if self._selected != (-1, -1):
            current_pos = pygame.mouse.get_pos()
            gem_1_x = (self._selected[0] - 150) // 64
            gem_1_y = (self._selected[1] - 100) // 64
            gem_2_x = (current_pos[0] - 150) // 64
            gem_2_y = (current_pos[1] - 100) // 64
            if gem_2_x > 7 or gem_2_y > 7:
                return
            if (gem_1_x == gem_2_x + 1 and gem_1_y == gem_2_y) or \
                    (gem_1_x + 1 == gem_2_x and gem_1_y == gem_2_y) or \
                    (gem_1_x == gem_2_x and gem_1_y == gem_2_y + 1) or \
                    (gem_1_x == gem_2_x and gem_1_y + 1 == gem_2_y):
                self.board[gem_1_x][gem_1_y], self.board[gem_2_x][gem_2_y] = \
                    self.board[gem_2_x][gem_2_y], self.board[gem_1_x][gem_1_y]
                self._selected = (-1, -1)


def main():
    run_game = Game()
    run_game.execute()


if __name__ == '__main__':
    main()
