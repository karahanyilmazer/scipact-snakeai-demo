---
scipact: 1
number: 11
slug: gamma-0p95
title: GAMMA 0.95 instead of 0.9
status: planned
weight: iteration
needs_approval: false
involves:
  held_out_data: false
  external_submission: false
  deletes_data: false
date_started: null
date_completed: null
verdict: null
tldr: null
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
*Fill in after running: the number, the baseline, the noise floor.*

## Reading
*One line after the close: what the number says about the why, and what it rules out.*

## Deviations from pre-registration

none

## Reviewer notes

-
