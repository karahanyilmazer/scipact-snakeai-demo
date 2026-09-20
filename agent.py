import random
from collections import deque

import numpy as np
import torch

from game import BLOCK_SIZE, Direction, Point, SnakeGameAI
from model import Linear_QNet, QTrainer

# Hyperparameters. Agent() reads them when it is constructed, so
# `train.py --set NAME=VALUE` can override any of them for one run.
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
GAMMA = 0.9  # discount rate
HIDDEN_SIZE = 256
EXPLORE_GAMES = 80  # epsilon = EXPLORE_GAMES - n_games, out of 200
STATE_SIZE = 14  # 3 danger, 4 direction, 4 food, 3 trap

CLOCKWISE = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]


def step(pt, direction):
    """The cell one block from `pt` in `direction`."""
    if direction == Direction.RIGHT:
        return Point(pt.x + BLOCK_SIZE, pt.y)
    if direction == Direction.LEFT:
        return Point(pt.x - BLOCK_SIZE, pt.y)
    if direction == Direction.DOWN:
        return Point(pt.x, pt.y + BLOCK_SIZE)
    return Point(pt.x, pt.y - BLOCK_SIZE)


def reachable(game, start, cap):
    """Free cells reachable from `start` without crossing a wall or the body,
    counted up to `cap`; 0 when `start` itself is a wall or the body."""
    if game.is_collision(start):
        return 0
    body = set(game.snake)
    seen = {start}
    stack = [start]
    n = 0
    while stack:
        pt = stack.pop()
        n += 1
        if n >= cap:
            return n
        for q in (
            Point(pt.x + BLOCK_SIZE, pt.y),
            Point(pt.x - BLOCK_SIZE, pt.y),
            Point(pt.x, pt.y + BLOCK_SIZE),
            Point(pt.x, pt.y - BLOCK_SIZE),
        ):
            if (
                q not in seen
                and q not in body
                and 0 <= q.x <= game.w - BLOCK_SIZE
                and 0 <= q.y <= game.h - BLOCK_SIZE
            ):
                seen.add(q)
                stack.append(q)
    return n


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = GAMMA
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(STATE_SIZE, HIDDEN_SIZE, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r))
            or (dir_l and game.is_collision(point_l))
            or (dir_u and game.is_collision(point_u))
            or (dir_d and game.is_collision(point_d)),
            # Danger right
            (dir_u and game.is_collision(point_r))
            or (dir_d and game.is_collision(point_l))
            or (dir_l and game.is_collision(point_u))
            or (dir_r and game.is_collision(point_d)),
            # Danger left
            (dir_d and game.is_collision(point_r))
            or (dir_u and game.is_collision(point_l))
            or (dir_r and game.is_collision(point_u))
            or (dir_l and game.is_collision(point_d)),
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            # Food location
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y,  # food down
        ]

        # Trap straight / right / left: the move leads into a pocket smaller
        # than the snake, so the head cannot get out before the body fills it.
        i = CLOCKWISE.index(game.direction)
        need = len(game.snake)
        for d in (CLOCKWISE[i], CLOCKWISE[(i + 1) % 4], CLOCKWISE[(i - 1) % 4]):
            state.append(reachable(game, step(head, d), need) < need)

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append(
            (state, action, reward, next_state, done)
        )  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample, strict=True)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = EXPLORE_GAMES - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train(games=None, seed=None, render=True, fps=None, on_game=None):
    """Train a fresh agent for `games` games (forever when None).

    Returns the per-game scores and the number of steps played. `seed` makes
    the run reproducible; `on_game(n_games, score, record)` is called after
    each game. Without a budget the best model so far is saved to
    model/model.pth, as in the tutorial.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
    scores = []
    steps = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI(render=render, seed=seed, fps=fps)
    while games is None or agent.n_games < games:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        steps += 1

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.record_game(score)
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                if games is None:
                    agent.model.save()

            scores.append(score)
            if on_game is not None:
                on_game(agent.n_games, score, record)
    game.close()
    return scores, steps


if __name__ == "__main__":
    train(
        on_game=lambda n, score, record: print(
            "Game", n, "Score", score, "Record:", record
        )
    )
