# Snake AI as an experiment harness

A fork of [patrickloeber/snake-ai-pytorch](https://github.com/patrickloeber/snake-ai-pytorch),
the *Teach AI To Play Snake* tutorial (Deep Q-learning with PyTorch and Pygame,
[playlist](https://www.youtube.com/playlist?list=PLqnslRFeH2UrDh7vUmJ60YrmWd64mTTKV)),
turned into something you can run experiments on: fixed budgets, seeds, headless
runs, and a results file. The learning algorithm is the tutorial's.

## What changed

- **One window.** The score chart (score per game, running mean) is drawn in the
  game window next to the board; the separate matplotlib window and `helper.py`
  are gone.
- **`train.py`**, a harness: a fixed number of games, a seed, `--no-render` for
  fast headless runs, identical runs over several seeds in parallel, A/B runs,
  and a `results.json`.
- **Seeding.** `random`, NumPy, torch and the game's food placement are seeded.
- **Constants** at the top of `agent.py` (hidden size, learning rate, gamma,
  batch size, memory, exploration length) that a run can override.
- **Headless speed.** Without rendering there is no frame clock, so a run is
  bound by training, not by drawing.

`agent.py`, `model.py` and `game.py` keep the tutorial's structure and numerics;
`snake_game_human.py` (play it yourself) is untouched.

## Setup

```
uv sync
```

Python 3.11 or newer; `uv` picks 3.14 from `.python-version`.

## Run

```
uv run agent.py                                      # the tutorial: train forever, watch it play
uv run train.py --games 300 --seed 0 --no-render     # one run, ~minutes
uv run train.py --games 300 --seed 0                 # the same, rendered
uv run train.py --games 300 --seeds 0-4 --no-render  # five seeds in parallel: their mean and spread
uv run train.py --games 300 --seeds 0-4 --replicates 5 --no-render   # calibration: the same 5-seed reading on 5 disjoint seed sets
uv run train.py --games 300 --seeds 0-2 --ab HIDDEN_SIZE=512 --no-render   # A/B over the same seeds
uv run train.py --smoke                              # 10 headless games, writes nothing
uv run train.py --help
```

`--set NAME=VALUE` overrides a constant of `agent.py` for a run (repeatable);
`--ab NAME=VALUE` runs a baseline arm without the override and a treatment arm
with it over the same seeds. `--fps 0` renders unthrottled.

## What a run writes

`results.json` goes to `$SCIPACT_EXPERIMENT_DIR` when that variable is set,
otherwise to the current directory; `--out` overrides. The statistic is
**`mean_score`**: the mean score over the last `--last` games (default 100) of a
run, so the number is about the trained agent, not the learning curve; with
`--seeds` it is the mean of that over the seeds.

A **noise floor** for a statistic is the spread of repeated readings of it with
nothing changed. Training is deterministic under a seed, so repeating the same
seeds gives spread 0 and the readings must use fresh seeds: `--replicates R`
repeats the `--seeds` reading on R disjoint seed sets (the given seeds, then
the next ones: `--seeds 0-4 --replicates 5` uses 0–4, 5–9, …, 20–24) and writes
`noise_floor` as the spread of the R reading means. The spread between single
seeds of one reading (`seed_spread`) is not the floor of their mean; it is
about √N larger.

| Mode | Keys |
|---|---|
| one run | `mean_score`, `mean_score_all`, `record`, `games`, `last`, `seed`, `steps`, `seconds`, `config`, `scores` |
| `--seeds` | `mean_score` (mean over seeds), `std`, `seed_spread` (max − min of the seeds), `min`, `max`, `n_seeds`, `seeds`, `seconds`, `config`, `runs` (one entry per seed) |
| `--seeds --replicates R` | `noise_floor` (spread of the R reading means), `baseline` (their mean, = `mean_score`), `readings` (R), `instrument` (one line), `reading_means`, `reading_std`, `seed_sets`, `seconds`, `config`, `readings_detail` (one `--seeds` block per reading) |
| `--ab` | `delta` (treatment − baseline), `deltas` (per seed), `ci_low`, `ci_high` (95 % paired t-interval), `n_seeds`, `seeds`, `seconds`, `treatment_config`, `arms.baseline`, `arms.treatment` (the `--seeds` shape) |

With `--seeds`, `--replicates` and `--ab`, every run is a separate headless
process; its log and its own `results.json` are kept under `runs/` next to the
results file.

## Files

| File | Role |
|---|---|
| `train.py` | the harness: budgets, seeds, headless runs, results |
| `agent.py` | the agent, its constants, the training loop; `python agent.py` is the tutorial |
| `model.py` | the Q-network and the trainer |
| `game.py` | the Snake environment, rendering and the in-window chart |
| `snake_game_human.py` | the game, keyboard-controlled |

## License

MIT, as upstream.
