#!/usr/bin/env python3
"""Are the two branches' trap bits the same function? Random states, no training.

    uv run python results/consolidation/trap_bits_equivalent.py

`autonomous` (007) puts three trap bits at positions 3-5 of the state;
`autonomous-2` (002) appends them at 11-13. Both say: the free cells reachable
from the cell a move lands on are fewer than the snake is long. This loads
both `agent.py` files from their branches, builds 20 000 random self-avoiding
snakes on the real board and compares the bits. If they always agree, the
different numbers the two campaigns read for "the same" change are a
permutation of the input features meeting the seeded initial weights, not a
different feature.
"""

import importlib.util
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from game import BLOCK_SIZE, Direction, Point, SnakeGameAI  # noqa: E402  game.py is identical on every branch


def load(branch):
    src = subprocess.run(
        ["git", "show", f"{branch}:agent.py"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    path = Path(tempfile.mkdtemp()) / f"agent_{branch.replace('-', '_')}.py"
    path.write_text(src)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Agent()


def main():
    for branch in ("autonomous", "autonomous-2"):
        diff = subprocess.run(["git", "diff", "--quiet", "8578331", branch, "--", "game.py", "model.py"], cwd=ROOT)
        assert diff.returncode == 0, f"{branch} changed game.py or model.py; this check assumes it did not"
    a, b = load("autonomous"), load("autonomous-2")
    rng = random.Random(0)
    game = SnakeGameAI(render=False, seed=0)
    moves = ((BLOCK_SIZE, 0), (-BLOCK_SIZE, 0), (0, BLOCK_SIZE), (0, -BLOCK_SIZE))

    def random_snake(n):
        while True:
            body = [Point(rng.randrange(0, game.w, BLOCK_SIZE), rng.randrange(0, game.h, BLOCK_SIZE))]
            for _ in range(n - 1):
                options = [
                    p
                    for p in (Point(body[-1].x + dx, body[-1].y + dy) for dx, dy in moves)
                    if 0 <= p.x <= game.w - BLOCK_SIZE and 0 <= p.y <= game.h - BLOCK_SIZE and p not in body
                ]
                if not options:
                    break
                body.append(rng.choice(options))
            if len(body) == n:
                return body

    agree = disagree = set_bits = 0
    for _ in range(20_000):
        game.snake = random_snake(rng.choice([3, 5, 10, 20, 40, 80, 150]))
        game.head = game.snake[0]
        game.direction = rng.choice(list(Direction))
        sa, sb = list(a.get_state(game)), list(b.get_state(game))
        trap_a, trap_b = sa[3:6], sb[11:14]
        assert sa[:3] + sa[6:] == sb[:11], "the eleven tutorial features differ"
        if trap_a == trap_b:
            agree += 1
        else:
            disagree += 1
            print("disagree:", len(game.snake), game.direction, trap_a, trap_b)
        set_bits += sum(trap_a)
    print(f"states {agree + disagree}, agree {agree}, disagree {disagree}, trap bits set {set_bits}")
    return 0 if disagree == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
