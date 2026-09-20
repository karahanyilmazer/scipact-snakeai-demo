---
scipact: 1
number: 6
slug: huber-loss
title: Huber (SmoothL1) loss instead of MSE
status: done
weight: iteration
needs_approval: false
involves:
  held_out_data: false
  external_submission: false
  deletes_data: false
date_started: 2026-09-20
date_completed: 2026-09-20
verdict: DISCARD
tldr: "DISCARD: Huber loss drops mean_score from 82.18 to 65.04 (-17.14, floor 9.15), with seeds split 46-84."
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

| seed | mean_score | record | steps | seconds |
|---|---|---|---|---|
| 0 | 67.30 | 160 | 439791 | 216 |
| 1 | 45.94 | 141 | 353575 | 168 |
| 2 | 69.98 | 160 | 455141 | 223 |
| 3 | 58.10 | 170 | 335332 | 159 |
| 4 | 83.86 | 179 | 577299 | 298 |

Mean over seeds **65.04**, std 14.11, per-seed spread 37.92; wall clock 299 s.

```
✓ 006-huber-loss closed: DISCARD
    key statistic mean_score = 65.04
    KEEP          no
    DISCARD       fired
    improvement -17.14 vs baseline 82.18 (004-lr-2p5e-4), noise floor 9.15
```

## Reading
The seeds split wide (45.9 to 83.9, spread 37.9 against the baseline's 9.2) while records held (141-179): capping the gradient of the rare terminal targets did not steady late training, it slowed how fast the -10 death signal propagates, so some seeds were still learning at game 300; this rules out the loss's tail as the source of late-training noise at this LR.

## Deviations from pre-registration

none

## Reviewer notes

-
