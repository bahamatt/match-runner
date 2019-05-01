import pygame
from pygame.locals import *

WIDTH = 800
HEIGHT = 640


class PlayerObject:

    def __init__(self):
        self.x = 1 / 5 * WIDTH
        self.y = 4 / 5 * HEIGHT - 20
        self.dy = 0
        self.jumping = False
        self.falling = False
        self.surface = pygame.Surface((20, 20))
        self.surface.fill(color.THECOLORS["red"])
        self.rect = Rect(self.surface.get_rect())
        self.max_jump_height = 3 / 5 * HEIGHT

    def on_the_ground(self):
        if self.y >= 4 / 5 * HEIGHT - 20:
            return True
        else:
            return False

    def on_jump_max_height(self):
        if self.y <= self.max_jump_height:
            return True
        else:
            return False

    def jump(self):
        if not self.falling:
            self.dy -= 400
            self.jumping = True
            self.falling = False

    def update(self, deltatime, screen):

        if self.on_jump_max_height():
            self.dy += 50
            self.jumping = False
            self.falling = True

        if self.on_the_ground() and not self.jumping:
            self.dy = 0
            self.y = 4 / 5 * HEIGHT - 20
            self.max_jump_height = 3 / 5 * HEIGHT
            self.falling = False

        self.y += self.dy * deltatime
        self.rect.move_ip(self.x, self.y)
        pygame.draw.rect(screen, color.THECOLORS["red"], [self.x, self.y, 20, 20], 0)


class ScoreObject:
    def __init__(self, score):
        print(score)
        self.surface = pygame.Surface((100, 1 / 5 * HEIGHT))
        self.surface.fill(color.THECOLORS["gray"])
        self.score = score
        self.position = 0
        self.speed = 50
        self.rect = Rect(self.surface.get_rect())
        self.rect = pygame.draw.line(self.surface, color.THECOLORS["black"], (0, 0), (0, 1 / 10 * HEIGHT), 5)
        # self.rect = self.rect.move(1 / 5 * WIDTH + score, 4 / 5 * HEIGHT)
        font = pygame.font.Font(None, 20)
        font_surface = font.render(str(score), True, color.THECOLORS["black"], color.THECOLORS["gray"])
        self.surface.blit(font_surface, (5, 1 / 10 * HEIGHT))

    def update(self, screen, tick):
        self.rect = self.rect.move(-self.speed / tick, 0)
        screen.blit(self.surface, self.rect)
        self.position += self.speed


class Game:
    def __init__(self):
        pygame.init()
        self._running = True
        self.player = PlayerObject()
        self.player.rect = self.player.rect.move(self.player.x, self.player.y)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.scores = []
        self.scores_init()

    def scores_init(self):
        for i in range(0, 9):
            new_score = ScoreObject(i * 100)
            new_score.rect = new_score.rect.move(1 / 5 * WIDTH + i * 100, 4 / 5 * HEIGHT)
            self.scores.append(new_score)

    def scores_update(self):
        if self.scores[-1].rect.x < WIDTH - 100:
            new_score = ScoreObject(self.scores[-1].score + 100)
            new_score.rect = new_score.rect.move(self.scores[-1].rect.x + 100, 4 / 5 * HEIGHT)
            self.scores.append(new_score)

    def execute(self):
        while self._running:
            tick = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # sys.exit()
                    self._running = False
                if event.type == KEYDOWN and event.key == K_SPACE:
                    if self.player.jumping:
                        self.player.max_jump_height = self.player.y - 108
                        self.player.max_jump_height = max(20.0, self.player.max_jump_height)
                    else:
                        self.player.jump()
            self.screen.fill(color.THECOLORS["black"])
            for score in self.scores:
                score.update(self.screen, tick)
            self.scores_update()
            self.player.update(tick / 1000.0, self.screen)
            pygame.display.flip()


def main():
    run_game = Game()
    run_game.execute()


if __name__ == '__main__':
    main()
