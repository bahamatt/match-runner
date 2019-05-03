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
            self.max_jump_height = 4 / 5 * HEIGHT - 150
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

    def update(self, screen, tick, speed):
        self.speed = speed
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

    def update(self, screen, tick, speed):
        self.speed = speed
        self.rect = self.rect.move(-self.speed / tick, 0)
        screen.blit(self.surface, self.rect)


class Tunnel:

    def __init__(self, game_speed):
        self.x = WIDTH
        self.tunnel_length = 250
        self.upper_length = HEIGHT / 2 - 100 - randrange(10) * 15
        self.lower_length = 4 / 5 * HEIGHT - self.upper_length - self.tunnel_length
        self.speed = game_speed
        self.upper_surface = pygame.Surface((25, self.upper_length))
        self.upper_surface.fill(color.THECOLORS["green"])
        self.lower_surface = pygame.Surface((25, self.lower_length))
        self.lower_surface.fill(color.THECOLORS["green"])
        self.upper_rect = Rect(self.upper_surface.get_rect())
        self.lower_rect = Rect(self.lower_surface.get_rect())

    def update(self, screen, tick, speed):
        self.speed = speed
        self.upper_rect = self.upper_rect.move(-self.speed / tick, 0)
        self.lower_rect = self.lower_rect.move(-self.speed / tick, 0)
        screen.blit(self.upper_surface, self.upper_rect)
        screen.blit(self.lower_surface, self.lower_rect)


class Stone:

    def __init__(self, game_speed):
        self.x = WIDTH
        self.y = 0
        self.dy = 0
        self.delta = 3 + randrange(4)
        self.speed = game_speed
        self.surface = pygame.Surface((30, 30))
        self.surface.fill(color.THECOLORS["yellow"])
        self.rect = Rect(self.surface.get_rect())

    def on_the_ground(self):
        if self.y >= 4 / 5 * HEIGHT - 30:
            return True
        else:
            return False

    def on_the_top(self):
        if self.y <= 0:
            return True
        else:
            return False

    def update(self, screen, tick, speed):
        self.speed = speed
        if self.on_the_top():
            self.dy = self.delta
        if self.on_the_ground():
            self.y = 4 / 5 * HEIGHT - 30
            self.dy = -self.delta
        self.y += self.dy
        self.rect = self.rect.move(-self.speed / tick, self.dy)
        screen.blit(self.surface, self.rect)


class GroundStone:

    def __init__(self, game_speed):
        self.x = WIDTH + 100
        self.y = 4 / 5 * HEIGHT - 60
        self.speed = 2.25 * game_speed
        self.surface = pygame.Surface((60, 60))
        self.surface.fill(color.THECOLORS["purple"])
        self.rect = Rect(self.surface.get_rect())

    def update(self, screen, tick, speed):
        self.speed = 2.25 * speed
        self.rect = self.rect = self.rect.move(-self.speed / tick, 0)
        screen.blit(self.surface, self.rect)


class Game:

    def __init__(self):
        pygame.init()
        self._running = True
        self.speed = 50
        self.maxspeed = 150
        self.final_score = 0
        self.player = PlayerObject()
        self.player.rect = self.player.rect.move(self.player.x, self.player.y)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.scores = []
        self.scores_init()
        self.rectangle_obstacles = []
        self.stones = []
        self.ground_stones = []
        self.tunnels = []
        self.deltaspeed = 0.01
        self.is_displaying_obstacles = False

    def scores_init(self):
        for i in range(0, 9):
            new_score = ScoreObject(i * 100, self.speed)
            new_score.rect = new_score.rect.move(1 / 5 * WIDTH + i * 100, 4 / 5 * HEIGHT)
            self.scores.append(new_score)

    def scores_update(self):
        if self.scores[-1].rect.x < WIDTH - 100:
            new_score = ScoreObject(self.scores[-1].score + 100, self.speed)
            new_score.rect = new_score.rect.move(self.scores[-1].rect.x + 100, 4 / 5 * HEIGHT)
            self.scores.append(new_score)
            self.scores.remove(self.scores[0])

    def obstacles_display(self):
        if not self.is_displaying_obstacles:
            rand = randrange(4)
            if rand == 0:
                self.rectangle_obstacles_init()
                self.is_displaying_obstacles = True
            elif rand == 1:
                self.stones_init()
                self.is_displaying_obstacles = True
            elif rand == 2:
                self.ground_stone_init()
                self.is_displaying_obstacles = True
            elif rand == 3:
                self.tunnels_init()
                self.is_displaying_obstacles = True

    def obstacles_handler(self, tick):
        if self.rectangle_obstacles:
            for obstacle in self.rectangle_obstacles:
                obstacle.update(self.screen, tick, self.speed)
                if obstacle.rect.colliderect(self.player.rect):
                    self._running = False
            self.rectangle_obstacles_update()
        if self.stones:
            for stone in self.stones:
                stone.update(self.screen, tick, self.speed)
                if stone.rect.colliderect(self.player.rect):
                    self._running = False
            self.stones_update()
        if self.ground_stones:
            for stone in self.ground_stones:
                stone.update(self.screen, tick, self.speed)
                if stone.rect.colliderect(self.player.rect):
                    self._running = False
            self.ground_stone_update()
        if self.tunnels:
            for tunnel in self.tunnels:
                tunnel.update(self.screen, tick, self.speed)
                if tunnel.upper_rect.colliderect(self.player.rect) or tunnel.lower_rect.colliderect(self.player.rect):
                    self._running = False
            self.tunnels_update()

    def rectangle_obstacles_init(self):
        for i in range(0, 6):
            if i % 2 == 0:
                new_obstacle = RectangleObstacle(self.speed)
                new_obstacle.rect = new_obstacle.rect.move(new_obstacle.x + i * 300,
                                                           4 / 5 * HEIGHT - new_obstacle.height)
                self.rectangle_obstacles.append(new_obstacle)
            else:
                new_obstacle = RectangleObstacle(self.speed)
                new_obstacle.rect = new_obstacle.rect.move(new_obstacle.x + i * 300, 0)
                self.rectangle_obstacles.append(new_obstacle)

    def rectangle_obstacles_update(self):
        if len(self.rectangle_obstacles) == 1:
            self.is_displaying_obstacles = False
        if self.rectangle_obstacles[-1].rect.x <= -50:
            self.rectangle_obstacles.remove(self.rectangle_obstacles[0])

    def tunnels_init(self):
        for i in range(0, 3):
            new_tunnel = Tunnel(self.speed)
            new_tunnel.upper_rect = new_tunnel.upper_rect.move(new_tunnel.x + i * 375, 0)
            new_tunnel.lower_rect = new_tunnel.lower_rect.move(new_tunnel.x + i * 375,
                                                               4 / 5 * HEIGHT - new_tunnel.lower_length)
            self.tunnels.append(new_tunnel)

    def tunnels_update(self):
        if len(self.tunnels) == 1:
            self.is_displaying_obstacles = False
        if self.tunnels[-1].upper_rect.x <= -50:
            self.tunnels.remove(self.tunnels[0])

    def stones_init(self):
        for i in range(0, 5):
            new_stone = Stone(self.speed)
            new_stone.rect = new_stone.rect.move(new_stone.x + i * 250, new_stone.y)
            self.stones.append(new_stone)

    def stones_update(self):
        if len(self.stones) == 1:
            self.is_displaying_obstacles = False
        if self.stones[-1].rect.x <= -30:
            self.stones.remove(self.stones[0])

    def ground_stone_init(self):
        new_circle = GroundStone(self.speed)
        new_circle.rect = new_circle.rect.move(new_circle.x, new_circle.y)
        self.ground_stones.append(new_circle)

    def ground_stone_update(self):
        if self.ground_stones[0].rect.x <= -50:
            self.ground_stones.remove(self.ground_stones[0])
            self.is_displaying_obstacles = False

    def execute(self):
        while self._running:
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
                score.update(self.screen, tick, self.speed)

            self.player.update(tick / 1000.0, self.screen, self.speed)

            self.obstacles_display()
            self.obstacles_handler(tick)

            self.scores_update()
            pygame.display.flip()
        for score in self.scores:
            if score.rect.left < self.player.rect.left:
                self.final_score = score.score
        print(self.final_score)


def main():
    run_game = Game()
    run_game.execute()


if __name__ == '__main__':
    main()
