---
scipact: 1
number: 7
slug: free-run-features
title: Free-run length per move as three state features
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
tldr: "DISCARD: free-run features drop mean_score from 82.18 to 72.02 (-10.16, floor 9.15), every seed down."
results: results.json
hypothesis: The danger bits see one cell; a count of free cells in each of the three directions lets the policy prefer open lanes before it is adjacent to the body, cutting the deaths that the trap bits catch only at the last step
change: 6b6847d
parent: null
rule: inherit
---
# Experiment 007: Free-run length per move as three state features

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
- **Change:** Free-run length per move as three state features
- **Why:** The danger bits see one cell; a count of free cells in each of the three directions lets the policy prefer open lanes before it is adjacent to the body, cutting the deaths that the trap bits catch only at the last step
- **Command:** `uv run train.py --games 300 --last 100 --seeds 0-4 --no-render`
- **Writes:** `results.json` with `mean_score` (the mean over seeds 0-4 of the last-100 mean), plus the per-seed runs under `runs`

## Results

| seed | mean_score | record | steps | seconds |
|---|---|---|---|---|
| 0 | 72.51 | 158 | 460737 | 259 |
| 1 | 78.10 | 144 | 467390 | 262 |
| 2 | 73.50 | 135 | 379084 | 204 |
| 3 | 66.23 | 151 | 418011 | 227 |
| 4 | 69.77 | 139 | 430800 | 239 |

Mean over seeds **72.02**, std 4.42, per-seed spread 11.87; wall clock 263 s.

```
    key statistic mean_score = 72.022
    KEEP          no
    DISCARD       fired
    improvement -10.158 vs baseline 82.18 (004-lr-2p5e-4), noise floor 9.15
    written to results/experiments/007-free-run-features/verdict.json; index regenerated
```

## Reading
Every seed fell (66.2-78.1 vs 80.2-86.7) and the spread widened to 11.9: three continuous inputs on a network trained by single-transition steps did not add usable lookahead, they made the fit noisier, and the binary trap bits already carry the part of that information the policy can act on; this rules out straight-line free-run length as the missing signal at this level.

## Deviations from pre-registration

none

## Reviewer notes

-
