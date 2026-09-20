---
scipact: 1
number: 11
slug: gamma-0p95
title: GAMMA 0.95 instead of 0.9
status: done
weight: iteration
needs_approval: false
involves:
  held_out_data: false
  external_submission: false
  deletes_data: false
date_started: 2026-09-20
date_completed: 2026-09-20
verdict: INCONCLUSIVE
tldr: "INCONCLUSIVE: GAMMA 0.95 reads 82.84 vs 82.18 (+0.66, floor 9.15); same plateau, same late sag."
results: results.json
hypothesis: At 0.9 a reward 20 steps away is worth 12 % of one adjacent, so a long snake values only the nearest food and walks into corridors it cannot leave; at 0.95 that horizon doubles, so the Q-values of moves that keep the board open rise relative to greedy ones, and fewer late-game deaths lift the plateau
change: 50a4dbc
parent: null
rule: inherit
---
# Experiment 011: GAMMA 0.95 instead of 0.9

<!-- An iteration-weight contract: one change, one metric, one commit. The
     decision rule is inherited from the [iteration] table (the metric and
     its direction) and the latest closed calibration (the measured noise
     floor and baseline), so this contract needs four things: the change
     (the title), why it should move the metric (the front-matter
     `hypothesis`, also the Why line below; the checker refuses one that
     repeats the title), the exact command, and the commit. `change` is the
     commit holding the change under test: commit it first, then open the
     contract with `--change HEAD`; unless the verdict is KEEP it is
     reverted, so the next iteration starts from the best kept state. After
     the close, one line under Reading says what the number taught. This is
     the autoresearch loop with a record. -->

**Outcome (TL;DR):** *one sentence, filled in after running: KEEP, DISCARD or INCONCLUSIVE and the number.*

## Method
- **Change:** GAMMA 0.95 instead of 0.9
- **Why:** At 0.9 a reward 20 steps away is worth 12 % of one adjacent, so a long snake values only the nearest food and walks into corridors it cannot leave; at 0.95 that horizon doubles, so the Q-values of moves that keep the board open rise relative to greedy ones, and fewer late-game deaths lift the plateau
- **Command:** `uv run train.py --games 300 --last 100 --seeds 0-4 --no-render`
- **Writes:** `results.json` with `mean_score` (the mean over seeds 0-4 of the last-100 mean), plus the per-seed runs under `runs`

## Results

| seed | mean_score | record | steps | seconds |
|---|---|---|---|---|
| 0 | 84.00 | 163 | 516009 | 278 |
| 1 | 85.28 | 179 | 513798 | 268 |
| 2 | 90.89 | 161 | 521630 | 278 |
| 3 | 78.76 | 149 | 455884 | 231 |
| 4 | 75.25 | 173 | 474249 | 243 |

Mean over seeds **82.84**, std 6.05, per-seed spread 15.64; wall clock 279 s.

```
    key statistic mean_score = 82.836
    KEEP          no
    DISCARD       no
    improvement +0.656 vs baseline 82.18 (004-lr-2p5e-4), noise floor 9.15
    written to results/experiments/011-gamma-0p95/verdict.json; index regenerated
```

## Reading
Per-seed deltas +3.8, -1.4, +13.3, -4.8, -7.6, no shared sign, and the same shape as before (peaks of 86-91 in games 150-250, then a sag on three seeds), so a longer horizon neither raises the plateau nor removes the sag; it took off a little earlier (all seeds past 40 by game 150) without that reaching the last 100 games, which rules out horizon length as the plateau's limiter at this state representation.

## Deviations from pre-registration

none

## Reviewer notes

-
