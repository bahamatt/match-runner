import os
import pickle
from random import randrange

import pygame
from pygame.locals import KEYDOWN, K_SPACE
from pygame.locals import Rect
from pygame.locals import color

import match3 as match
from gameover_screen import gameover_screen
from help_screen import help_screen
from menu_screen import menu_screen
from scores import score_screen

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

    def update(self, screen, tick, deltaspeed, no_collision):
        if self.on_jump_max_height():
            self.dy += 50 + deltaspeed
            self.jumping = False
            self.falling = True

        if self.on_the_ground() and not self.jumping:
            self.dy = 0
            self.y = 4 / 5 * HEIGHT - 20
            self.max_jump_height = 4 / 5 * HEIGHT - 150
            self.falling = False

        self.y += self.dy * tick
        if no_collision:
            self.rect = pygame.draw.rect(screen, color.THECOLORS["orange"], [self.x, self.y, 20, 20], 0)
        else:
            self.rect = pygame.draw.rect(screen, color.THECOLORS["red"], [self.x, self.y, 20, 20], 0)


class ScoreObject:
    def __init__(self, score, speed):
        self.x = 0
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
        self.rect = Rect(self.upper_surface.get_rect())
        self.lower_rect = Rect(self.lower_surface.get_rect())

    def update(self, screen, tick, speed):
        self.speed = speed
        self.rect = self.rect.move(-self.speed / tick, 0)
        self.lower_rect = self.lower_rect.move(-self.speed / tick, 0)
        screen.blit(self.upper_surface, self.rect)
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


class MatchRectangle:
    def __init__(self, game_speed):
        self.x = randrange(350, WIDTH)
        self.y = randrange(4 / 5 * HEIGHT - 80)
        self.speed = game_speed
        self.surface = pygame.Surface((35, 35))
        self.surface.fill(color.THECOLORS["orange"])
        self.rect = Rect(self.surface.get_rect())

    def update(self, screen, tick, speed):
        self.speed = speed
        self.rect = self.rect = self.rect.move(-self.speed / tick, 0)
        screen.blit(self.surface, self.rect)


def default_scores():
    score_list = [(16000, "Alice"), (8000, "Bob"), (4000, "Craig"), (2000, "Dave"), (1000, "Erin"), (500, "Frank"),
                  (400, "Grace"), (300, "Heidi"), (200, "Ivan"), (100, "Judy")]
    return score_list


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Match Runner")
        self._high_scores = []
        if os.path.isfile('scores.pickle'):
            with open('scores.pickle', 'rb') as file:
                self._high_scores = pickle.load(file)
        else:
            with open('scores.pickle', 'wb') as file:
                pickle.dump(default_scores(), file)
                self._high_scores = default_scores()
        self._start_window = True
        self._scores_window = False
        self._help_window = False
        self._running = True
        self._paused = False
        self._gameover = False
        self.display_match = False
        self.start_bonus_speed = False
        self.no_collision = False
        self.bonus_speed_time = 0
        self.no_collision_time = 0
        self.speed = 50
        self.maxspeed = 150
        self.bonus_score = 0
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
        self.match_rectangles = []
        self.deltaspeed = 0.01
        self.is_displaying_obstacles = False
        self.tick = 0

    def new_game_init(self):
        self._running = True
        self._paused = False
        self._gameover = False
        self.display_match = False
        self.start_bonus_speed = False
        self.no_collision = False
        self.bonus_speed_time = 0
        self.no_collision_time = 0
        self.speed = 50
        self.bonus_score = 0
        self.final_score = 0
        self.player = PlayerObject()
        self.player.rect = self.player.rect.move(self.player.x, self.player.y)
        self.scores = []
        self.scores_init()
        self.rectangle_obstacles = []
        self.stones = []
        self.ground_stones = []
        self.tunnels = []
        self.match_rectangles = []
        self.is_displaying_obstacles = False
        self.tick = 0

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
            rand = randrange(5)
            if rand == 0:
                self.rectangle_obstacles_init()
            elif rand == 1:
                self.stones_init()
            elif rand == 2:
                self.ground_stone_init()
            elif rand == 3:
                self.tunnels_init()
            elif rand == 4 and not self.start_bonus_speed and self.bonus_speed_time == 0:
                if randrange(3) != 0:
                    self.match_rectangle_init()

    def check_for_collision(self, obstacle_rect):
        if self.no_collision_time == 0:
            if obstacle_rect.colliderect(self.player.rect):
                self._gameover = True
                self._running = False

    def obstacles_handler(self, tick):
        for obstacle_list in [self.rectangle_obstacles, self.stones, self.ground_stones, self.tunnels]:
            if obstacle_list:
                for obstacle in obstacle_list:
                    obstacle.update(self.screen, tick, self.speed)
                    self.check_for_collision(obstacle.rect)
                    if obstacle_list == self.tunnels:
                        self.check_for_collision(obstacle.lower_rect)
                self.obstacles_update(obstacle_list)

    def match_updater(self, tick):
        if self.match_rectangles:
            if self._paused:
                self._paused = False
            for rect in self.match_rectangles:
                rect.update(self.screen, tick, self.speed)
                if not self.display_match and rect.rect.colliderect(self.player.rect):
                    self._paused = True
                    self.display_match = True
                    self.match_init()
            self.match_rectangle_update()

    def events_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                pygame.quit()
                quit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                if self.player.jumping:
                    self.player.max_jump_height = self.player.y - 150
                    self.player.max_jump_height = max(20.0, self.player.max_jump_height)
                else:
                    self.player.jump(self.speed)

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
        self.is_displaying_obstacles = True

    def tunnels_init(self):
        for i in range(0, 3):
            new_tunnel = Tunnel(self.speed)
            new_tunnel.rect = new_tunnel.rect.move(new_tunnel.x + i * 375, 0)
            new_tunnel.lower_rect = new_tunnel.lower_rect.move(new_tunnel.x + i * 375,
                                                               4 / 5 * HEIGHT - new_tunnel.lower_length)
            self.tunnels.append(new_tunnel)
        self.is_displaying_obstacles = True

    def stones_init(self):
        for i in range(0, 5):
            new_stone = Stone(self.speed)
            new_stone.rect = new_stone.rect.move(new_stone.x + i * 250, new_stone.y)
            self.stones.append(new_stone)
        self.is_displaying_obstacles = True

    def ground_stone_init(self):
        new_circle = GroundStone(self.speed)
        new_circle.rect = new_circle.rect.move(new_circle.x, new_circle.y)
        self.ground_stones.append(new_circle)
        self.is_displaying_obstacles = True

    def obstacles_update(self, obstacles):
        if obstacles == self.ground_stones:
            if obstacles[0].rect.x <= -50:
                obstacles.remove(obstacles[0])
                self.is_displaying_obstacles = False
            return
        if len(obstacles) == 1:
            self.is_displaying_obstacles = False
        if obstacles[-1].rect.x <= -50:
            obstacles.remove(obstacles[0])

    def match_rectangle_init(self):
        new_match_rect = MatchRectangle(self.speed)
        new_match_rect.rect = new_match_rect.rect.move(new_match_rect.x, new_match_rect.y)
        self.match_rectangles.append(new_match_rect)
        self.is_displaying_obstacles = True

    def match_init(self):
        bonus_score = match.main()
        self.bonus_score = bonus_score

    def match_rectangle_update(self):
        if self.match_rectangles[0].rect.x <= 80:
            self.match_rectangles.remove(self.match_rectangles[0])
            self.display_match = False
            self.is_displaying_obstacles = False

    def bonus_speed_handler(self):
        if self.start_bonus_speed and self.player.on_the_ground():
            self.bonus_speed_time = self.bonus_score * 5
            self.no_collision_time = self.bonus_speed_time + 1500
            self.speed = self.speed * 3
            self.bonus_score = 0
            self.start_bonus_speed = False
        if self.bonus_speed_time > 0:
            self.bonus_speed_time -= self.tick
        if self.no_collision_time > 0:
            self.no_collision_time -= self.tick
        if self.bonus_speed_time < 0:
            self.bonus_speed_time = 0
            self.speed = self.speed / 3
        if self.no_collision_time < 0:
            self.no_collision_time = 0
            self.no_collision = False
        if self.bonus_score >= 500:
            self.start_bonus_speed = True
            self.no_collision = True
        if self.speed > self.maxspeed and self.bonus_speed_time == 0:
            self.speed = self.speed / 3

    def execute(self):
        while True:
            while self._start_window:
                menu_screen(self)
            while self._scores_window:
                score_screen(self)
            while self._help_window:
                help_screen(self)
            while self._running:
                if self.speed < self.maxspeed:
                    self.speed += self.deltaspeed
                self.bonus_speed_handler()
                self.tick = self.clock.tick(60)
                self.events_handler()
                self.screen.fill(color.THECOLORS["black"])
                for score in self.scores:
                    score.update(self.screen, self.tick, self.speed)
                self.obstacles_handler(self.tick)
                if not self._paused:
                    self.player.update(self.screen, self.tick / 1000.0, self.speed, self.no_collision)
                self.match_updater(self.tick)
                self.obstacles_display()
                self.scores_update()
                if self.bonus_speed_time > 0:
                    font = pygame.font.Font('dat/Century Gothic.ttf', 120)
                    (w, h) = pygame.font.Font.size(font, "BONUS!")
                    title_surface = font.render("BONUS!", True, color.THECOLORS["orange"])
                    self.screen.blit(title_surface, ((WIDTH - w) / 2, h / 3))
                pygame.display.flip()
                for score in self.scores:
                    if score.rect.left < self.player.rect.left:
                        self.final_score = score.score
            while self._gameover:
                gameover_screen(self)
