---
scipact: 1
number: 10
slug: lr-1e-4
title: LR 1e-4 instead of 2.5e-4
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
hypothesis: Lowering the rate from 1e-3 to 2.5e-4 lifted every seed (004) and the plateau still erodes over the last 100 games (005, 009); a smaller step should slow that drift once the policy is good, and if 300 games still suffice to take off, the last 100 sit nearer the peak
change: 09cb083
parent: null
rule: inherit
---
# Experiment 010: LR 1e-4 instead of 2.5e-4

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
- **Change:** LR 1e-4 instead of 2.5e-4
- **Why:** Lowering the rate from 1e-3 to 2.5e-4 lifted every seed (004) and the plateau still erodes over the last 100 games (005, 009); a smaller step should slow that drift once the policy is good, and if 300 games still suffice to take off, the last 100 sit nearer the peak
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
