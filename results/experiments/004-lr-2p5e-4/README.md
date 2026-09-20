---
scipact: 1
number: 4
slug: lr-2p5e-4
title: LR 2.5e-4 instead of 1e-3
status: done
weight: iteration
needs_approval: false
involves:
  held_out_data: false
  external_submission: false
  deletes_data: false
date_started: 2026-09-20
date_completed: 2026-09-20
verdict: KEEP
tldr: "KEEP: LR 2.5e-4 lifts mean_score from 75.22 to 82.18 (+6.96, floor 5.48), all five seeds up."
results: results.json
hypothesis: Every step trains on one transition at LR 1e-3 before the batch replay, which is a noisy update on a small MSE target; a quarter of the rate should let the Q-values settle rather than oscillate late in training, raising the last-100 mean
change: c3e9321
parent: null
rule: inherit
---
# Experiment 004: LR 2.5e-4 instead of 1e-3

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
- **Change:** LR 2.5e-4 instead of 1e-3
- **Why:** Every step trains on one transition at LR 1e-3 before the batch replay, which is a noisy update on a small MSE target; a quarter of the rate should let the Q-values settle rather than oscillate late in training, raising the last-100 mean
- **Command:** `uv run train.py --games 300 --last 100 --seeds 0-4 --no-render`
- **Writes:** `results.json` with `mean_score` (the mean over seeds 0-4 of the last-100 mean), plus the per-seed runs under `runs`

## Results

| seed | mean_score | record | steps | seconds |
|---|---|---|---|---|
| 0 | 80.23 | 146 | 441069 | 215 |
| 1 | 86.70 | 169 | 446075 | 220 |
| 2 | 77.55 | 146 | 311238 | 144 |
| 3 | 83.60 | 147 | 356296 | 172 |
| 4 | 82.82 | 154 | 514840 | 253 |

Mean over seeds **82.18**, std 3.47, per-seed spread 9.15; wall clock 255 s.

```
✓ 004-lr-2p5e-4 closed: KEEP
    key statistic mean_score = 82.18
    KEEP          fired
    DISCARD       no
    improvement +6.956 vs baseline 75.224 (002-trap-bits-in-state), noise floor 5.48
```

## Reading
All five seeds rose (per-seed deltas +3.1, +9.8, +0.7, +12.0, +9.2), consistent with the late-training Q-values settling at the lower rate rather than a faster climb (records did not rise: 146-169 vs 133-174); the kept code's own per-seed spread is 9.15, above the floor of 5.48, so the floor is re-measured before the next step.

## Deviations from pre-registration

none

## Reviewer notes

-
