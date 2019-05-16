import random

import pygame
from pygame.locals import *

WIDTH = 800
HEIGHT = 640


class Gem:
    def __init__(self, image):
        self.image = image
        self.matched = False


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
        self.blank = pygame.image.load("img/blank.bmp")
        self.board = self.generate()

    def draw(self):
        for i in range(8):
            for j in range(8):
                self.screen.blit(self.board[i][j].image, (150 + 64 * i, 100 + 64 * j))

    def execute(self):
        while self._running:
            tick = self.clock.tick(60)
            self.events_handler()
            self.check_move()
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

    def check_move(self):
        if self._selected != (-1, -1):
            current_pos = pygame.mouse.get_pos()
            gem_1_x = (self._selected[0] - 150) // 64
            gem_1_y = (self._selected[1] - 100) // 64
            gem_2_x = (current_pos[0] - 150) // 64
            gem_2_y = (current_pos[1] - 100) // 64
            if gem_1_x > 7 or gem_1_y > 7 or gem_2_x > 7 or gem_2_y > 7:
                return
            if (gem_1_x == gem_2_x + 1 and gem_1_y == gem_2_y) or \
                    (gem_1_x + 1 == gem_2_x and gem_1_y == gem_2_y) or \
                    (gem_1_x == gem_2_x and gem_1_y == gem_2_y + 1) or \
                    (gem_1_x == gem_2_x and gem_1_y + 1 == gem_2_y):
                self.board[gem_1_x][gem_1_y], self.board[gem_2_x][gem_2_y] = \
                    self.board[gem_2_x][gem_2_y], self.board[gem_1_x][gem_1_y]
                self._selected = (-1, -1)
                matches = self.find_matches()
                print(matches)
                for i in range(8):
                    for j in range(8):
                        if self.board[i][j].matched is True:
                            self.board[i][j].image = self.blank
                # if matches == 0:
                #     self.board[gem_1_x][gem_1_y], self.board[gem_2_x][gem_2_y] = \
                #         self.board[gem_2_x][gem_2_y], self.board[gem_1_x][gem_1_y]

    def generate(self):
        board = [[Gem(self.shapes[random.randrange(7)]) for _ in range(8)] for _ in range(8)]
        i = 0
        j = 0
        while i <= 7:
            while j <= 7:
                if j <= 5 and board[i][j].image == board[i][j + 1].image == board[i][j + 2].image:
                    board[i][j] = Gem(self.shapes[random.randrange(7)])
                    board[i][j + 1] = Gem(self.shapes[random.randrange(7)])
                    board[i][j + 2] = Gem(self.shapes[random.randrange(7)])
                    i = 0
                    j = 0
                    continue
                if i <= 5 and board[i][j].image == board[i + 1][j].image == board[i + 2][j].image:
                    board[i][j] = Gem(self.shapes[random.randrange(7)])
                    board[i + 1][j] = Gem(self.shapes[random.randrange(7)])
                    board[i + 2][j] = Gem(self.shapes[random.randrange(7)])
                    i = 0
                    j = 0
                    continue
                j += 1
            j = 0
            i += 1
        return board

    def find_matches(self):
        i = 0
        j = 0
        score = 0
        while i <= 7:
            while j <= 7:
                if j <= 5 and not (self.board[i][j].matched is True and self.board[i][j+1].matched is True and self.board[i][j+2].matched is True) \
                        and self.board[i][j].image == self.board[i][j + 1].image == self.board[i][j + 2].image:
                    self.board[i][j].matched = True
                    self.board[i][j+1].matched = True
                    self.board[i][j+2].matched = True
                    score += 1
                if i <= 5 and not (self.board[i][j].matched is True and self.board[i+1][j].matched is True and self.board[i+2][j].matched is True) \
                        and self.board[i][j].image == self.board[i + 1][j].image == self.board[i + 2][j].image:
                    self.board[i][j].matched = True
                    self.board[i+1][j].matched = True
                    self.board[i+2][j].matched = True
                    score += 1
                j += 1
            j = 0
            i += 1
        return score


def main():
    run_game = Game()
    run_game.execute()


if __name__ == '__main__':
    main()
