import random

import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.locals import color

WIDTH = 800
HEIGHT = 640


class Gem:
    def __init__(self, image):
        self.image = image
        self.matched = False
        self.offset = [0, 0]

    def update_offset(self):
        if self.offset[0] != 0:
            old_offset = self.offset[0]
            if self.offset[0] < 0:
                self.offset[0] += 10
            else:
                self.offset[0] -= 10
            if old_offset * self.offset[0] <= 0:
                self.offset[0] = 0
        if self.offset[1] != 0:
            old_offset = self.offset[1]
            if self.offset[1] < 0:
                self.offset[1] += 10
            else:
                self.offset[1] -= 10
            if old_offset * self.offset[1] <= 0:
                self.offset[1] = 0


class Game:
    def __init__(self):
        pygame.init()
        self.time_left = 15000
        self.board_locked = False
        self.score = 0
        self._running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self._selected = (-1, -1)
        self.shape_names = ["red", "blue", "green", "purple", "yellow", "orange", "white"]
        self.shapes = [pygame.image.load("img/{}.bmp".format(shape)) for shape in self.shape_names]
        self.board = self.generate()

    def draw(self):
        font = pygame.font.SysFont('centurygothic', 40)
        time_surface = font.render("Time left: {:.3f}".format(self.time_left / 1000), True, color.THECOLORS["white"])
        self.screen.blit(time_surface, (10, 10))
        score_surface = font.render("Score: {:d}".format(self.score), True, color.THECOLORS["white"])
        self.screen.blit(score_surface, (10, 50))
        for i in range(8):
            for j in range(8):
                self.screen.blit(self.board[i][j].image, (150 + 64 * i + self.board[i][j].offset[0],
                                                          100 + 64 * j + self.board[i][j].offset[1]))

    def win_window(self):
        font = pygame.font.SysFont('centurygothic', 80)
        win_surface = font.render("Extra speed!", True, color.THECOLORS["white"], color.THECOLORS["black"])
        (w, h) = pygame.font.Font.size(font, "Extra speed!")
        self.screen.blit(win_surface, ((15 + WIDTH - w) / 2, (HEIGHT - h) / 2))

    def execute(self):
        while self._running:
            tick = self.clock.tick(60)
            if self.board_locked:
                animation_complete = True
                for i in range(8):
                    for j in range(8):
                        self.board[i][j].update_offset()
                        if self.board[i][j].offset != [0, 0]:
                            animation_complete = False
                if animation_complete:
                    matches_found = self.find_matches()
                    if matches_found > 0:
                        self.score += 100 * matches_found
                        self.fill_board()
                    else:
                        self.board_locked = False
            else:
                self.events_handler()
                self.check_for_move()
            self.screen.fill(color.THECOLORS["black"])
            self.draw()
            pygame.display.flip()
            self.time_left -= tick
            # if self.score >= 500:
            #     pygame.display.update()
            #     # self.win_window()
            #     self.wait_for(250)
            #     self._running = False
            #     return self.score
            if self.time_left < 0:
                self._running = False
                return self.score

    def wait_for(self, wait_time):
        screen_copy = self.screen.copy()
        wait_count = 0
        while wait_count < wait_time:
            dt = self.clock.tick(60)
            wait_count += dt
            pygame.event.pump()
            self.screen.blit(screen_copy, (0, 0))
            pygame.display.flip()

    def events_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == MOUSEBUTTONDOWN:
                self._selected = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONUP:
                self._selected = (-1, -1)

    def check_for_move(self):
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
                self.board_locked = True
                self.swap((gem_1_x, gem_1_y), (gem_2_x, gem_2_y))
                self._selected = (-1, -1)

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

    def fill_board(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j].matched:
                    for k in range(j, 0, -1):
                        self.swap((i, k), (i, k - 1))
        for i in range(8):
            for j in range(7, -1, -1):
                if self.board[i][j].matched:
                    self.board[i][j].matched = False
                    self.board[i][j].image = self.shapes[random.randrange(7)]
                    self.board[i][j].offset[1] = -320

    def find_matches(self):
        i = 0
        j = 0
        score = 0
        while i <= 7:
            while j <= 7:
                if j <= 5 and not (
                        self.board[i][j].matched is True and
                        self.board[i][j + 1].matched is True and
                        self.board[i][j + 2].matched is True) and \
                        self.board[i][j].image == self.board[i][j + 1].image == self.board[i][j + 2].image:
                    self.board[i][j].matched = True
                    self.board[i][j + 1].matched = True
                    self.board[i][j + 2].matched = True
                    score += 1
                if i <= 5 and not (
                        self.board[i][j].matched is True and
                        self.board[i + 1][j].matched is True and
                        self.board[i + 2][j].matched is True) and \
                        self.board[i][j].image == self.board[i + 1][j].image == self.board[i + 2][j].image:
                    self.board[i][j].matched = True
                    self.board[i + 1][j].matched = True
                    self.board[i + 2][j].matched = True
                    score += 1
                j += 1
            j = 0
            i += 1
        return score

    def swap(self, gem_1, gem_2):
        self.board[gem_1[0]][gem_1[1]], self.board[gem_2[0]][gem_2[1]] = \
            self.board[gem_2[0]][gem_2[1]], self.board[gem_1[0]][gem_1[1]]
        self.board[gem_1[0]][gem_1[1]].offset[0] += (gem_2[0] - gem_1[0]) * 64
        self.board[gem_1[0]][gem_1[1]].offset[1] += (gem_2[1] - gem_1[1]) * 64
        self.board[gem_2[0]][gem_2[1]].offset[0] += (gem_1[0] - gem_2[0]) * 64
        self.board[gem_2[0]][gem_2[1]].offset[1] += (gem_1[1] - gem_2[1]) * 64

    def quick_swap(self, gem_1, gem_2):
        self.board[gem_1[0]][gem_1[1]], self.board[gem_2[0]][gem_2[1]] = \
            self.board[gem_2[0]][gem_2[1]], self.board[gem_1[0]][gem_1[1]]


def main():
    run_game = Game()
    score = run_game.execute()
    return score


if __name__ == '__main__':
    main()
