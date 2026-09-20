---
scipact: 1
number: 9
slug: target-network
title: Target network synced every 1000 train steps
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
tldr: "INCONCLUSIVE: a target network reads 83.20 vs 82.18 (+1.02, floor 9.15); the late-plateau sag it was meant to cure is unchanged."
results: results.json
hypothesis: Bootstrapping max Q(s') from the live network lets every update chase a moving target, which is the late-plateau sag seen in 005 and 008; a copy refreshed every 1000 steps holds the target still between refreshes, so the plateau stops decaying over the last 100 games and the mean rises
change: f1c49c2
parent: null
rule: inherit
---
# Experiment 009: Target network synced every 1000 train steps

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
- **Change:** Target network synced every 1000 train steps
- **Why:** Bootstrapping max Q(s') from the live network lets every update chase a moving target, which is the late-plateau sag seen in 005 and 008; a copy refreshed every 1000 steps holds the target still between refreshes, so the plateau stops decaying over the last 100 games and the mean rises
- **Command:** `uv run train.py --games 300 --last 100 --seeds 0-4 --no-render`
- **Writes:** `results.json` with `mean_score` (the mean over seeds 0-4 of the last-100 mean), plus the per-seed runs under `runs`

## Results

| seed | mean_score | record | steps | seconds |
|---|---|---|---|---|
| 0 | 79.04 | 159 | 493657 | 275 |
| 1 | 81.14 | 139 | 487465 | 264 |
| 2 | 86.07 | 161 | 437707 | 240 |
| 3 | 89.48 | 153 | 394142 | 210 |
| 4 | 80.26 | 175 | 489624 | 275 |

Mean over seeds **83.20**, std 4.41, per-seed spread 10.44; wall clock 276 s.

```
    key statistic mean_score = 83.198
    KEEP          no
    DISCARD       no
    improvement +1.018 vs baseline 82.18 (004-lr-2p5e-4), noise floor 9.15
    written to results/experiments/009-target-network/verdict.json; index regenerated
```

## Reading
Per-seed deltas -1.2, -5.6, +8.5, +5.9, -2.6 with no shared sign, and the late sag is untouched (seeds 0, 3, 4 peak at 92-97 in games 150-200 and end at 78-82), so a moving bootstrap target is not what erodes the plateau; whatever does (buffer turnover at about 1000 steps a game, or step size at the plateau) is still open, and the sync interval of 1000 is the one value tried.

## Deviations from pre-registration

none

## Reviewer notes

-
