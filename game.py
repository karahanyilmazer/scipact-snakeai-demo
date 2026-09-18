import random
from collections import namedtuple
from enum import Enum
from pathlib import Path

import numpy as np
import pygame

FONT_PATH = Path(__file__).resolve().parent / "arial.ttf"


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREY = (90, 90, 90)
DIM = (40, 40, 40)
LIGHT = (180, 180, 180)
ORANGE = (255, 140, 0)

BLOCK_SIZE = 20
SPEED = 40
CHART_WIDTH = 400  # the score chart drawn to the right of the board


class SnakeGameAI:
    def __init__(
        self, w=640, h=480, render=True, seed=None, fps=SPEED, chart_width=CHART_WIDTH
    ):
        self.w = w
        self.h = h
        self.render = render
        self.fps = SPEED if fps is None else fps
        self.rng = random.Random(seed)  # food placement; seeded per game instance
        # score history across games, shown in the chart
        self.scores = []
        self.mean_scores = []
        self.record = 0
        self._total = 0
        if render:
            pygame.init()
            self.font = pygame.font.Font(str(FONT_PATH), 25)
            self.small_font = pygame.font.Font(str(FONT_PATH), 14)
            self.chart_width = chart_width
            self.display = pygame.display.set_mode((self.w + self.chart_width, self.h))
            pygame.display.set_caption("Snake")
            self.clock = pygame.time.Clock()
            self.chart = pygame.Surface((self.chart_width, self.h))
            self._draw_chart()
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y),
        ]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = self.rng.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = self.rng.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        if self.render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit(0)

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock (headless runs skip both)
        if self.render:
            self._update_ui()
            if self.fps:
                self.clock.tick(self.fps)
        # 6. return game over and score
        return reward, game_over, self.score

    def record_game(self, score):
        """Add a finished game's score to the history the chart shows."""
        self.scores.append(score)
        self._total += score
        self.mean_scores.append(self._total / len(self.scores))
        self.record = max(self.record, score)
        if self.render:
            self._draw_chart()

    def close(self):
        if self.render:
            pygame.quit()

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if (
            pt.x > self.w - BLOCK_SIZE
            or pt.x < 0
            or pt.y > self.h - BLOCK_SIZE
            or pt.y < 0
        ):
            return True
        # hits itself
        return pt in self.snake[1:]

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(
                self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12)
            )

        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
        )

        header = (
            f"Game {len(self.scores) + 1}   Score {self.score}   Record {self.record}"
        )
        self.display.blit(self.font.render(header, True, WHITE), [0, 0])
        self.display.blit(self.chart, (self.w, 0))
        pygame.display.flip()

    def _draw_chart(self):
        """Redraw the score chart (score per game, running mean) onto its surface."""
        s = self.chart
        s.fill(BLACK)
        pygame.draw.line(s, GREY, (0, 0), (0, self.h))

        left, top = 44, 36
        right, bottom = self.chart_width - 16, self.h - 40
        pw, ph = right - left, bottom - top
        n = len(self.scores)
        ymax = max(max(self.scores, default=0), 1)

        title = self.small_font.render("score per game", True, BLUE2)
        s.blit(title, (left, 10))
        title2 = self.small_font.render("running mean", True, ORANGE)
        s.blit(title2, (left + title.get_width() + 16, 10))

        for frac in (0, 0.25, 0.5, 0.75, 1):
            y = bottom - frac * ph
            pygame.draw.line(s, DIM, (left, y), (right, y))
            label = self.small_font.render(f"{ymax * frac:g}", True, LIGHT)
            s.blit(label, (left - label.get_width() - 6, y - label.get_height() / 2))
        pygame.draw.rect(s, GREY, pygame.Rect(left, top, pw, ph), 1)
        xlabel = self.small_font.render(f"games: {n}", True, LIGHT)
        s.blit(xlabel, (left + (pw - xlabel.get_width()) / 2, bottom + 10))

        if n == 0:
            return

        def points(series):
            step = pw / max(n - 1, 1)
            return [
                (left + i * step, bottom - v / ymax * ph) for i, v in enumerate(series)
            ]

        for series, colour in ((self.scores, BLUE2), (self.mean_scores, ORANGE)):
            pts = points(series)
            if n > 1:
                pygame.draw.aalines(s, colour, False, pts)
            else:
                pygame.draw.circle(s, colour, pts[0], 3)
            value = series[-1]
            text = f"{value:.1f}" if isinstance(value, float) else str(value)
            label = self.small_font.render(text, True, colour)
            x, y = pts[-1]
            s.blit(
                label,
                (min(x + 4, right - label.get_width()), y - label.get_height() / 2),
            )

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
