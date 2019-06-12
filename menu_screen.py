import pygame
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import Rect
from pygame.locals import color

WIDTH = 800
HEIGHT = 640


def menu_screen(self):
    self._running = False
    self.screen.fill(color.THECOLORS["black"])
    font = pygame.font.Font('dat/Century Gothic.ttf', 80)
    (w, h) = pygame.font.Font.size(font, "Match Runner")
    title_surface = font.render("Match Runner", True, color.THECOLORS["blue"])
    self.screen.blit(title_surface, ((WIDTH - w) / 2, h / 3))
    menu_surface = pygame.Surface((400, 430))
    menu_surface.fill(color.THECOLORS["gray"])
    self.screen.blit(menu_surface, (200, 170))
    menu_black_surf = pygame.Surface((360, 82.5))
    menu_black_surf.fill(color.THECOLORS["black"])
    font = pygame.font.Font('dat/Century Gothic.ttf', 45)
    start_surface = font.render("New Game", True, color.THECOLORS["white"], color.THECOLORS["black"])
    (w, h) = pygame.font.Font.size(font, "New Game")
    self.screen.blit(menu_black_surf, (220, 190))
    self.screen.blit(start_surface, ((WIDTH - w) / 2, 200))
    scores_surface = font.render("High Scores", True, color.THECOLORS["white"], color.THECOLORS["black"])
    (w, h) = pygame.font.Font.size(font, "High Scores")
    self.screen.blit(menu_black_surf, (220, 292.5))
    self.screen.blit(scores_surface, ((WIDTH - w) / 2, 302.5))
    help_surface = font.render("Help", True, color.THECOLORS["white"], color.THECOLORS["black"])
    (w, h) = pygame.font.Font.size(font, "Help")
    self.screen.blit(menu_black_surf, (220, 395))
    self.screen.blit(help_surface, ((WIDTH - w) / 2, 405))
    quit_surface = font.render("Quit", True, color.THECOLORS["white"], color.THECOLORS["black"])
    (w, h) = pygame.font.Font.size(font, "Quit")
    self.screen.blit(menu_black_surf, (220, 497.5))
    self.screen.blit(quit_surface, ((WIDTH - w) / 2, 507.5))
    pygame.display.update()
    events_handler(self)


def events_handler(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (3, 3))
            if Rect(220, 190, 360, 82.5).colliderect(mouse_rect):
                self.new_game_init()
                self._start_window = False
            elif Rect(220, 292.5, 360, 82.5).colliderect(mouse_rect):
                self._start_window = False
                self._scores_window = True
            elif Rect(220, 395, 360, 82.5).colliderect(mouse_rect):
                self._start_window = False
                self._help_window = True
            elif Rect(220, 497.5, 360, 82.5).colliderect(mouse_rect):
                pygame.quit()
                quit()
