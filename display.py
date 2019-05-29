import os
import pickle
import pygame
from random import randrange
from pygame.locals import *
import match3 as match

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
        self.rect = self.rect.move(-self.speed/tick, 0)
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


class ObstaclesInitializer:
    @staticmethod
    def rectangle_obstacles_init(rectangle_obstacles, speed):
        for i in range(0, 6):
            if i % 2 == 0:
                new_obstacle = RectangleObstacle(speed)
                new_obstacle.rect = new_obstacle.rect.move(new_obstacle.x + i * 300,
                                                           4 / 5 * HEIGHT - new_obstacle.height)
                rectangle_obstacles.append(new_obstacle)
            else:
                new_obstacle = RectangleObstacle(speed)
                new_obstacle.rect = new_obstacle.rect.move(new_obstacle.x + i * 300, 0)
                rectangle_obstacles.append(new_obstacle)


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

    def obstacles_handler(self, tick):
        if self.rectangle_obstacles:
            for obstacle in self.rectangle_obstacles:
                obstacle.update(self.screen, tick, self.speed)
                self.check_for_collision(obstacle.rect)
            self.rectangle_obstacles_update()
        if self.stones:
            for stone in self.stones:
                stone.update(self.screen, tick, self.speed)
                self.check_for_collision(stone.rect)
            self.stones_update()
        if self.ground_stones:
            for stone in self.ground_stones:
                stone.update(self.screen, tick, self.speed)
                self.check_for_collision(stone.rect)
            self.ground_stone_update()
        if self.tunnels:
            for tunnel in self.tunnels:
                tunnel.update(self.screen, tick, self.speed)
                self.check_for_collision(tunnel.upper_rect)
                self.check_for_collision(tunnel.lower_rect)
            self.tunnels_update()

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
        self.is_displaying_obstacles = True

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
        self.is_displaying_obstacles = True

    def stones_update(self):
        if len(self.stones) == 1:
            self.is_displaying_obstacles = False
        if self.stones[-1].rect.x <= -30:
            self.stones.remove(self.stones[0])

    def ground_stone_init(self):
        new_circle = GroundStone(self.speed)
        new_circle.rect = new_circle.rect.move(new_circle.x, new_circle.y)
        self.ground_stones.append(new_circle)
        self.is_displaying_obstacles = True

    def ground_stone_update(self):
        if self.ground_stones[0].rect.x <= -50:
            self.ground_stones.remove(self.ground_stones[0])
            self.is_displaying_obstacles = False

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
            self.no_collision_time = 5500
            self.bonus_speed_time = 4000
            self.speed = self.speed * 3
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
            self.bonus_score = 0
        if self.speed > self.maxspeed and self.bonus_speed_time == 0:
            self.speed = self.speed / 3

    def start_menu(self):
        self.screen.fill(color.THECOLORS["black"])
        font = pygame.font.SysFont('centurygothic', 80)
        (w, h) = pygame.font.Font.size(font, "Match Runner")
        title_surface = font.render("Match Runner", True, color.THECOLORS["blue"])
        self.screen.blit(title_surface, ((WIDTH - w) / 2, h / 3))
        menu_surface = pygame.Surface((400, 430))
        menu_surface.fill(color.THECOLORS["gray"])
        self.screen.blit(menu_surface, (200, 170))
        menu_black_surf = pygame.Surface((360, 82.5))
        menu_black_surf.fill(color.THECOLORS["black"])
        font = pygame.font.SysFont('centurygothic', 45)
        start_surface = font.render("New Game", True, color.THECOLORS["white"], color.THECOLORS["black"])
        (w, h) = pygame.font.Font.size(font, "New Game")
        self.screen.blit(menu_black_surf, (220, 190))
        self.screen.blit(start_surface, ((WIDTH - w)/2, 200))
        scores_surface = font.render("High Scores", True, color.THECOLORS["white"], color.THECOLORS["black"])
        (w, h) = pygame.font.Font.size(font, "High Scores")
        self.screen.blit(menu_black_surf, (220, 292.5))
        self.screen.blit(scores_surface, ((WIDTH - w) / 2, 302.5))
        help_surface = font.render("Help", True, color.THECOLORS["white"], color.THECOLORS["black"])
        (w, h) = pygame.font.Font.size(font, "Help")
        self.screen.blit(menu_black_surf, (220, 395))
        self.screen.blit(help_surface, ((WIDTH-w)/2, 405))
        quit_surface = font.render("Quit", True, color.THECOLORS["white"], color.THECOLORS["black"])
        (w, h) = pygame.font.Font.size(font, "Quit")
        self.screen.blit(menu_black_surf, (220, 497.5))
        self.screen.blit(quit_surface, ((WIDTH-w)/2, 507.5))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (3, 3))
                if Rect(220, 190, 360, 110).colliderect(mouse_rect):
                    self.new_game_init()
                    self._start_window = False
                elif Rect(220, 292.5, 360, 110).colliderect(mouse_rect):
                    self._start_window = False
                    self._scores_window = True
                elif Rect(220, 450, 360, 110).colliderect(mouse_rect):
                    pygame.quit()
                    quit()

    def score_screen(self):
        self.screen.fill(color.THECOLORS["black"])
        font = pygame.font.SysFont('centurygothic', 32)
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
                if Rect(30, HEIGHT - h - 20, w+4, h+4).colliderect(mouse_rect):
                    self._scores_window = False
                    self._start_window = True

    def gameover(self):
        name = ""
        new_high_score = self.final_score > self._high_scores[9][0]
        while self._gameover:
            self.screen.fill(color.THECOLORS["black"])
            font = pygame.font.SysFont('centurygothic', 60)
            (w, h) = pygame.font.Font.size(font, "Game Over")
            title_surface = font.render("Game Over", True, color.THECOLORS["blue"])
            self.screen.blit(title_surface, ((WIDTH - w) / 2, (HEIGHT - h) / 3))
            (w, h) = pygame.font.Font.size(font, "Score: " + str(self.final_score))
            score_surface = font.render("Score: " + str(self.final_score), True, color.THECOLORS["blue"])
            self.screen.blit(score_surface, ((WIDTH - w) / 2, (HEIGHT - h) / 2))
            if new_high_score:
                (w, h) = pygame.font.Font.size(font, "Enter your name: {:s}".format(name))
                score_surface = font.render("Enter your name: {:s}".format(name), True, color.THECOLORS["blue"])
                self.screen.blit(score_surface, ((WIDTH - w) / 2, (HEIGHT - h) / 2 + 2 * h))
            font = pygame.font.SysFont('centurygothic', 30)
            (w, h) = pygame.font.Font.size(font, "  Back to menu  ")
            back_to_menu_surface = font.render("  Back to menu  ", True, color.THECOLORS["white"], color.THECOLORS["black"])
            back_to_menu_bg = pygame.Surface((w+4, h+4))
            back_to_menu_bg.fill(color.THECOLORS["gray"])
            self.screen.blit(back_to_menu_bg, (28, HEIGHT-h-22))
            self.screen.blit(back_to_menu_surface, (30, HEIGHT - h - 20))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (3, 3))
                    if Rect(30, HEIGHT - h - 20, w+4, h+4).colliderect(mouse_rect):
                        self._gameover = False
                        self._start_window = True
                elif event.type == KEYDOWN and new_high_score:
                    if event.key == K_RETURN:
                        self.add_high_score(self.final_score, name)
                        new_high_score = False
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

    def execute(self):
        while self._running:
            while self._start_window:
                self.start_menu()
            while self._scores_window:
                self.score_screen()
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
                self.player.update(self.screen, self.tick/1000.0, self.speed, self.no_collision)
            self.match_updater(self.tick)
            self.obstacles_display()
            self.scores_update()
            if self.bonus_speed_time > 0:
                font = pygame.font.SysFont('centurygothic', 120)
                (w, h) = pygame.font.Font.size(font, "BONUS!")
                title_surface = font.render("BONUS!", True, color.THECOLORS["orange"])
                self.screen.blit(title_surface, ((WIDTH - w) / 2, h / 3))
            pygame.display.flip()
            for score in self.scores:
                if score.rect.left < self.player.rect.left:
                    self.final_score = score.score
            while self._gameover:
                self.gameover()

    def add_high_score(self, final_score, name):
        i = 0
        while self._high_scores[i][0] >= final_score:
            i += 1
            if i > 10:
                print("error")
                break
        self._high_scores.insert(i, (final_score, name))
        self._high_scores.pop()
        with open('scores.pickle', 'wb') as file:
            pickle.dump(self._high_scores, file)


def main():
    run_game = Game()
    run_game.execute()


if __name__ == '__main__':
    main()
