import pickle

import pygame
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, K_RETURN, K_BACKSPACE
from pygame.locals import Rect
from pygame.locals import color

WIDTH = 800
HEIGHT = 640


def add_high_score(self, final_score):
    i = 0
    while self._high_scores[i][0] >= final_score:
        i += 1
        if i > 10:
            print("error")
            break
    self._high_scores.insert(i, (final_score, self.player_name))
    self._high_scores.pop()
    with open('scores.pickle', 'wb') as file:
        pickle.dump(self._high_scores, file)


def gameover_screen(self):
    self._running = False
    self.player_name = ""
    self.new_high_score = self.final_score > self._high_scores[9][0]
    while self._gameover:
        self.screen.fill(color.THECOLORS["black"])
        font = pygame.font.Font('dat/Century Gothic.ttf', 60)
        (w, h) = pygame.font.Font.size(font, "Game Over")
        title_surface = font.render("Game Over", True, color.THECOLORS["blue"])
        self.screen.blit(title_surface, ((WIDTH - w) / 2, (HEIGHT - h) / 3))
        (w, h) = pygame.font.Font.size(font, "Score: " + str(self.final_score))
        score_surface = font.render("Score: " + str(self.final_score), True, color.THECOLORS["blue"])
        self.screen.blit(score_surface, ((WIDTH - w) / 2, (HEIGHT - h) / 2))
        if self.new_high_score:
            (w, h) = pygame.font.Font.size(font, "Enter your name: {:s}".format(self.player_name))
            score_surface = font.render("Enter your name: {:s}".format(self.player_name), True, color.THECOLORS["blue"])
            self.screen.blit(score_surface, ((WIDTH - w) / 2, (HEIGHT - h) / 2 + 2 * h))
        font = pygame.font.Font('dat/Century Gothic.ttf', 30)
        (w, h) = pygame.font.Font.size(font, "  Back to menu  ")
        back_to_menu_surface = font.render("  Back to menu  ", True, color.THECOLORS["white"],
                                           color.THECOLORS["black"])
        back_to_menu_bg = pygame.Surface((w + 4, h + 4))
        back_to_menu_bg.fill(color.THECOLORS["gray"])
        self.screen.blit(back_to_menu_bg, (28, HEIGHT - h - 22))
        self.screen.blit(back_to_menu_surface, (30, HEIGHT - h - 20))
        pygame.display.update()
        events_handler(self, w, h)


def events_handler(self, w, h):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (3, 3))
            if Rect(30, HEIGHT - h - 20, w + 4, h + 4).colliderect(mouse_rect):
                self._gameover = False
                self._start_window = True
        elif event.type == KEYDOWN and self.new_high_score:
            if event.key == K_RETURN:
                add_high_score(self, self.final_score)
                self.new_high_score = False
            elif event.key == K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                self.player_name += event.unicode
