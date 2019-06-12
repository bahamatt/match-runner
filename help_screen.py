import pygame
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import Rect
from pygame.locals import color

WIDTH = 800
HEIGHT = 640


def help_screen(self):
    self._running = False
    self.screen.fill(color.THECOLORS["black"])
    font = pygame.font.Font('dat/Century Gothic.ttf', 26)
    with open("dat/helptext.txt", "r") as file:
        i = 0
        for line in file:
            surface = font.render(line.strip(), True, color.THECOLORS["blue"])
            self.screen.blit(surface, ((WIDTH / 16), (HEIGHT / 16) * i + 16))
            i += 1
    (w, h) = pygame.font.Font.size(font, "  Back to menu  ")
    back_to_menu_surface = font.render("  Back to menu  ", True, color.THECOLORS["white"], color.THECOLORS["black"])
    back_to_menu_bg = pygame.Surface((w + 4, h + 4))
    back_to_menu_bg.fill(color.THECOLORS["gray"])
    self.screen.blit(back_to_menu_bg, (28, HEIGHT - h - 22))
    self.screen.blit(back_to_menu_surface, (30, HEIGHT - h - 20))
    pygame.display.update()
    events_handler(self, h, w)


def events_handler(self, h, w):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (3, 3))
            if Rect(30, HEIGHT - h - 20, w + 4, h + 4).colliderect(mouse_rect):
                self._help_window = False
                self._start_window = True