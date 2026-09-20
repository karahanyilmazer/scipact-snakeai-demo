---
scipact: 1
number: 2
slug: trap-bits-in-state
title: "Trap bits in the state: one per move, set when the reachable area is smaller than the snake"
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
tldr: "KEEP: trap bits lift mean_score from 33.17 to 75.22 (+42.05, floor 1.32), every seed more than doubling."
results: results.json
hypothesis: A dead-end detector lets the policy avoid walking into pockets it cannot leave, the main death cause once the snake is long, so games run longer and the last-100 mean rises
change: a9ab82c
parent: null
rule: inherit
---
# Experiment 002: Trap bits in the state: one per move, set when the reachable area is smaller than the snake

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
- **Change:** Trap bits in the state: one per move, set when the reachable area is smaller than the snake
- **Why:** A dead-end detector lets the policy avoid walking into pockets it cannot leave, the main death cause once the snake is long, so games run longer and the last-100 mean rises
- **Command:** `uv run train.py --games 300 --last 100 --seeds 0-4 --no-render`
- **Writes:** `results.json` with `mean_score` (the mean over seeds 0-4 of the last-100 mean), plus the per-seed runs under `runs`

## Results

| seed | mean_score | record | steps | seconds |
|---|---|---|---|---|
| 0 | 77.12 | 174 | 505568 | 263 |
| 1 | 76.88 | 157 | 543746 | 278 |
| 2 | 76.90 | 169 | 478823 | 244 |
| 3 | 71.64 | 133 | 455723 | 224 |
| 4 | 73.58 | 161 | 477509 | 242 |

Mean over seeds **75.22**, std 2.48, per-seed spread 5.48; wall clock 279 s.

```
✓ 002-trap-bits-in-state closed: KEEP
    key statistic mean_score = 75.224
    KEEP          fired
    DISCARD       no
    improvement +42.05 vs baseline 33.174 (001-spread-of-mean-score-unchanged), noise floor 1.32
```

## Reading
Every seed more than doubled (71.6-77.1 vs 32.6-33.9) and records rose from 66-81 to 133-174, so self-trapping was indeed the plateau's cause and the three bits are enough for the policy to route around it; runs now take about 250 s each (longer games), and the per-seed spread grew to 5.48, so the floor of 1.32 is stale and must be re-measured before the next step.

## Deviations from pre-registration

none

## Reviewer notes

-
