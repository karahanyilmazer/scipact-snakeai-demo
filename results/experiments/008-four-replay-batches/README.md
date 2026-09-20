---
scipact: 1
number: 8
slug: four-replay-batches
title: Four replay batches per game instead of one
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
tldr: "INCONCLUSIVE: four replay batches per game read 87.13 vs 82.18 (+4.95, floor 9.15); four seeds up 8-10, one down 9.6 from a late sag."
results: results.json
hypothesis: One 1000-sample batch per game is a thin use of a 100k-transition buffer; four batches quadruple the off-policy gradient steps at the same LR, so the Q-function fits the buffer sooner and the take-off that now comes at game 100-250 comes earlier, leaving more of the last 100 games at the plateau and a better-fitted plateau
change: 48a594a
parent: null
rule: inherit
---
# Experiment 008: Four replay batches per game instead of one

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
- **Change:** Four replay batches per game instead of one
- **Why:** One 1000-sample batch per game is a thin use of a 100k-transition buffer; four batches quadruple the off-policy gradient steps at the same LR, so the Q-function fits the buffer sooner and the take-off that now comes at game 100-250 comes earlier, leaving more of the last 100 games at the plateau and a better-fitted plateau
- **Command:** `uv run train.py --games 300 --last 100 --seeds 0-4 --no-render`
- **Writes:** `results.json` with `mean_score` (the mean over seeds 0-4 of the last-100 mean), plus the per-seed runs under `runs`

## Results

| seed | mean_score | record | steps | seconds |
|---|---|---|---|---|
| 0 | 87.87 | 170 | 570888 | 346 |
| 1 | 94.78 | 166 | 573326 | 350 |
| 2 | 85.90 | 165 | 504420 | 308 |
| 3 | 73.96 | 169 | 403421 | 248 |
| 4 | 93.15 | 169 | 523414 | 322 |

Mean over seeds **87.13**, std 8.22, per-seed spread 20.82; wall clock 351 s.

```
    key statistic mean_score = 87.132
    KEEP          no
    DISCARD       no
    improvement +4.952 vs baseline 82.18 (004-lr-2p5e-4), noise floor 9.15
    written to results/experiments/008-four-replay-batches/verdict.json; index regenerated
```

## Reading
The mechanism held (take-off moved from games 150-250 to 100-150 on every seed, and three seeds plateaued at 93-95, above anything seen before) but seed 3 sagged from 83 to 73 over the last 100 games, so per-seed deltas were +7.6, +8.1, +8.4, -9.6, +10.3 and the mean gain (+4.95) sat inside the floor; more gradient steps raise the plateau and also its late instability, which points at stabilising the target (a target network) before spending more steps.

## Deviations from pre-registration

none

## Reviewer notes

-
