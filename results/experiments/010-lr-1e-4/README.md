---
scipact: 1
number: 10
slug: lr-1e-4
title: LR 1e-4 instead of 2.5e-4
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
tldr: "DISCARD: LR 1e-4 drops mean_score from 82.18 to 40.90 (-41.28, floor 9.15); one seed never takes off and the rest are still climbing at game 300."
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

| seed | mean_score | record | steps | seconds |
|---|---|---|---|---|
| 0 | 52.58 | 129 | 269324 | 109 |
| 1 | 54.88 | 130 | 255063 | 106 |
| 2 | 31.84 | 67 | 209072 | 80 |
| 3 | 0.28 | 11 | 107131 | 39 |
| 4 | 64.91 | 153 | 323632 | 138 |

Mean over seeds **40.90**, std 25.69, per-seed spread 64.63; wall clock 139 s.

```
    key statistic mean_score = 40.898
    KEEP          no
    DISCARD       fired
    improvement -41.282 vs baseline 82.18 (004-lr-2p5e-4), noise floor 9.15
    written to results/experiments/010-lr-1e-4/verdict.json; index regenerated
```

## Reading
At 1e-4 the budget is no longer enough to take off: seed 3 never learned (0.3 throughout) and the other four were still climbing in games 250-300 (36-78, no plateau reached), so the drift the change was meant to slow was never reached; this brackets the rate for a 300-game budget between 1e-4 (too slow) and 1e-3 (worse than 2.5e-4 at the plateau), and the late sag needs a different lever than a globally smaller step.

## Deviations from pre-registration

none

## Reviewer notes

-
