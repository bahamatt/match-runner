import pygame
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import Rect
from pygame.locals import color

WIDTH = 800
HEIGHT = 640


def score_screen(self):
    self._running = False
    self.screen.fill(color.THECOLORS["black"])
    font = pygame.font.Font('dat/Century Gothic.ttf', 32)
    for i in range(10):
        surface = font.render("{:d}".format(i + 1), True, color.THECOLORS["blue"])
        self.screen.blit(surface, ((WIDTH / 16), (HEIGHT / 12) * i + 16))
        surface = font.render("{:d}".format(self._high_scores[i][0]), True, color.THECOLORS["blue"])
        self.screen.blit(surface, ((WIDTH / 4), (HEIGHT / 12) * i + 16))
        surface = font.render(self._high_scores[i][1], True, color.THECOLORS["blue"])
        self.screen.blit(surface, ((WIDTH / 2), (HEIGHT / 12) * i + 16))
    (w, h) = pygame.font.Font.size(font, "  Back to menu  ")
    back_to_menu_surface = font.render("  Back to menu  ", True, color.THECOLORS["white"], color.THECOLORS["black"])
    back_to_menu_bg = pygame.Surface((w + 4, h + 4))
    back_to_menu_bg.fill(color.THECOLORS["gray"])
    self.screen.blit(back_to_menu_bg, (28, HEIGHT - h - 22))
    self.screen.blit(back_to_menu_surface, (30, HEIGHT - h - 20))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (3, 3))
            if Rect(30, HEIGHT - h - 20, w + 4, h + 4).colliderect(mouse_rect):
                self._scores_window = False
                self._start_window = True