import pygame
from random import randrange
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

    def jump(self, deltaspeed):
        if not self.falling:
            self.dy -= 400 + deltaspeed
            self.jumping = True
            self.falling = False

    def update(self, deltatime, screen, deltaspeed):
        if self.on_jump_max_height():
            self.dy += 50 + deltaspeed
            self.jumping = False
            self.falling = True

        if self.on_the_ground() and not self.jumping:
            self.dy = 0
            self.y = 4 / 5 * HEIGHT - 20
            self.max_jump_height = 4/5*HEIGHT - 150
            self.falling = False

        self.y += self.dy * deltatime
        self.rect = pygame.draw.rect(screen, color.THECOLORS["red"], [self.x, self.y, 20, 20], 0)


class ScoreObject:

    def __init__(self, score, speed):
        self.surface = pygame.Surface((100, 1 / 5 * HEIGHT))
        self.surface.fill(color.THECOLORS["gray"])
        self.score = score
        self.speed = speed
        self.rect = Rect(self.surface.get_rect())
        self.rect = pygame.draw.line(self.surface, color.THECOLORS["black"], (0, 0), (0, 1 / 10 * HEIGHT), 5)
        font = pygame.font.Font(None, 20)
        font_surface = font.render(str(score), True, color.THECOLORS["black"], color.THECOLORS["gray"])
        self.surface.blit(font_surface, (5, 1 / 10 * HEIGHT))

    def update(self, screen, tick):
        self.rect = self.rect.move(-self.speed / tick, 0)
        screen.blit(self.surface, self.rect)


class RectangleObstacle:

    def __init__(self, game_speed):
        self.max_height = HEIGHT / 2 - 100
        self.height = self.max_height - randrange(10) * 15
        self.x = WIDTH
        self.y = self.height
        self.speed = game_speed
        self.surface = pygame.Surface((50, self.y))
        self.surface.fill(color.THECOLORS["blue"])
        self.rect = Rect(self.surface.get_rect())

    def update(self, screen, tick):
        self.rect = self.rect.move(-self.speed / tick, 0)
        screen.blit(self.surface, self.rect)


class Game:

    def __init__(self):
        pygame.init()
        self._running = True
        self.speed = 50
        self.maxspeed = 150
        self.player = PlayerObject()
        self.player.rect = self.player.rect.move(self.player.x, self.player.y)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.scores = []
        self.scores_init()
        #self.obstacles = []
        self.rectangle_obstacles = []
        self.deltaspeed = 0.01
        self.is_displaying_obstacles = False

    def scores_init(self):
        for i in range(0, 9):
            new_score = ScoreObject(i * 100, self.speed)
            new_score.rect = new_score.rect.move(1 / 5 * WIDTH + i * 100, 4 / 5 * HEIGHT)
            self.scores.append(new_score)

    def scores_update(self):
        for i in range(0, 9):
            self.scores[i].speed = self.speed
        if self.scores[-1].rect.x < WIDTH - 100:
            new_score = ScoreObject(self.scores[-1].score + 100, self.speed)
            new_score.rect = new_score.rect.move(self.scores[-1].rect.x + 100, 4 / 5 * HEIGHT)
            new_score.speed = self.scores[0].speed
            self.scores.append(new_score)
            self.scores.remove(self.scores[0])

    def rectangle_obstacles_init(self):
        for i in range(0, 6):
            if i % 2 == 0:
                new_obstacle = RectangleObstacle(self.speed)
                new_obstacle.rect = new_obstacle.rect.move(new_obstacle.x + i * 300, 4/5*HEIGHT - new_obstacle.height)
                self.rectangle_obstacles.append(new_obstacle)
            else:
                new_obstacle = RectangleObstacle(self.speed)
                new_obstacle.rect = new_obstacle.rect.move(new_obstacle.x + i * 300, 0)
                self.rectangle_obstacles.append(new_obstacle)

    def rectangle_obstacles_update(self):
        if len(self.rectangle_obstacles) == 1:
            self.is_displaying_obstacles = False
        for i in range(0, len(self.rectangle_obstacles)):
            self.rectangle_obstacles[i].speed = self.speed
        if self.rectangle_obstacles[-1].rect.x <= -50:
            self.rectangle_obstacles.remove(self.rectangle_obstacles[0])

    def execute(self):
        while self._running:
            print(self.speed)
            if self.speed < self.maxspeed:
                self.speed += self.deltaspeed
            tick = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == KEYDOWN and event.key == K_SPACE:
                    if self.player.jumping:
                        self.player.max_jump_height = self.player.y - 150
                        self.player.max_jump_height = max(20.0, self.player.max_jump_height)
                    else:
                        self.player.jump(self.speed)
            self.screen.fill(color.THECOLORS["black"])
            for score in self.scores:
                score.update(self.screen, tick)

            if not self.is_displaying_obstacles:
                rand = randrange(5)
                if rand == 0:
                    self.rectangle_obstacles_init()
                    self.is_displaying_obstacles = True
            if self.rectangle_obstacles:
                for obstacle in self.rectangle_obstacles:
                    if self.player.rect.colliderect(obstacle.rect):
                        self._running = False
                    obstacle.update(self.screen, tick)
                self.rectangle_obstacles_update()
            self.scores_update()
            self.player.update(tick / 1000.0, self.screen, self.speed)
            pygame.display.flip()


def main():
    run_game = Game()
    run_game.execute()


if __name__ == '__main__':
    main()
