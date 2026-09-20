---
scipact: 1
number: 6
slug: huber-loss
title: Huber (SmoothL1) loss instead of MSE
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
hypothesis: The +10/-10 terminal rewards give the TD error a heavy tail; a loss linear beyond error 1 caps the gradient those rare targets inject into Q-values that otherwise sit near zero, so late training is steadier and the last-100 mean rises
change: 2d674d8
parent: null
rule: inherit
---
# Experiment 006: Huber (SmoothL1) loss instead of MSE

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
- **Change:** Huber (SmoothL1) loss instead of MSE
- **Why:** The +10/-10 terminal rewards give the TD error a heavy tail; a loss linear beyond error 1 caps the gradient those rare targets inject into Q-values that otherwise sit near zero, so late training is steadier and the last-100 mean rises
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
