---
scipact: 1
number: 1
slug: spread-of-mean-score-unchanged
title: What is the run-to-run spread of mean_score on the unchanged code?
status: done
weight: full
needs_approval: false
involves:
  held_out_data: false
  external_submission: false
  deletes_data: false
date_started: 2026-09-20
date_completed: 2026-09-20
verdict: PASS
tldr: "PASS: the unchanged agent scores 33.17 +/- 0.61 over seeds 0-4 with a seed-to-seed spread of 1.32, so the noise floor is 1.32 and the baseline 33.17."
results: results.json
rule:
  statistic: noise_floor
  branches:
    PASS: noise_floor <= 20
    FAIL: noise_floor > 30
  otherwise: INCONCLUSIVE
predecessor: null
successor: null
calibration: true
---
# Experiment 001: What is the run-to-run spread of mean_score on the unchanged code?

<!-- The front matter is read by machines: `scipact check`, `lock` and `close`.
     Everything below the line is for people.
     needs_approval: true means a person approves this contract before it runs;
     false means it runs under the approved scope. Marking anything under
     `involves:` true makes approval mandatory.
     The `rule` block is the decision rule as code: `statistic` names a key in
     results.json, each branch is an expression over that file's values, and
     `otherwise` fires when none does. Exactly one branch may fire. The rule
     above is a PLACEHOLDER in the usual shape (the checker refuses it as is):
     the statistic is a difference with an interval [ci_low, ci_high]; ADOPT
     needs the difference past the bar with the interval clear of zero; REJECT
     needs the whole interval under the bar; the rest is INCONCLUSIVE. Replace
     every line with this question's statistic and bars. -->

**Outcome (TL;DR):** PASS: the unchanged agent scores 33.17 +/- 0.61 (mean over seeds 0-4 of the last-100 mean) with a seed-to-seed spread of 1.32, so the noise floor is 1.32 and the baseline 33.17.

**So what?** The instrument is far tighter than assumed: five seeds land within 1.3 points of each other at game 300, because the tutorial agent settles on a stable plateau and the last-100 mean averages it out. An iteration therefore counts as KEEP once it lifts the five-seed mean above 34.49, and the campaign can resolve small effects, not only algorithmic leaps. The floor will need re-measuring after a KEEP, since a better agent plays longer, more variable games.

---

## Question

What is the seed-to-seed spread of `mean_score` (the mean score over the
last 100 of 300 games) when the unchanged tutorial agent (`agent.py`,
`model.py` at this commit) is trained once on each of seeds 0-4? The spread
(max - min over the five seeds) becomes the noise floor every iteration in
this campaign is judged against, and the mean over the five seeds their
first baseline.

## Hypothesis / Prior

Diagnostic - no directional prior. An informal expectation, stated so it can
be wrong: the tutorial agent's last-100 mean lands somewhere around 20-40 at
300 games, and seeds differ by 10-20 points, since the agent's level at game
300 depends on how early it learns not to trap itself.

## Pre-registration

- **Specific quantitative outputs:** `train.py --seeds 0-4` writes to
  `results.json`: `mean_score` (the mean over the five seeds), `std`,
  `spread` and `noise_floor` (both max - min of the five per-seed values),
  `baseline` (= the mean), `min`, `max`, `n_seeds`, `seeds`, `seconds`, and
  under `runs` each seed's own results (its `mean_score`, `record`, `steps`,
  `seconds`, `scores`). The per-seed logs and JSON go to `runs/`.
- **Decision rule:** the statistic is `noise_floor`. PASS if it is at most
  20 points: a floor of 20 at an expected baseline of 20-40 lets an
  algorithmic change of the size this campaign is after (tens of points)
  resolve in one reading. FAIL if it is above 30: then nothing a single
  change is likely to do would clear the floor in one reading, and the
  instrument must be tightened (a scope edit) before looping. Between 20 and
  30, INCONCLUSIVE: a floor nothing inherits, and the design is revisited.
- **Instrument check:**
  - `noise_floor` is the range of five single-seed values, used as the
    floor for a five-seed *mean*. The range of single seeds over-reads the
    noise of their mean (by roughly a factor of two to three), so a KEEP is
    conservative; what this cannot detect is a real improvement smaller than
    the single-seed range, which will read INCONCLUSIVE. That is the
    approved scope's trade, and it is the same for every step.
  - Five seeds give a range estimate with a wide interval of its own; the
    floor is one draw of that range, so it cannot detect that seeds 0-4
    happen to be an unusually tight or loose set. A KEEP later recalibrates.
  - `baseline` is the mean of the same five seeds; every iteration reads
    the same seeds, so the comparison is paired. This cannot detect a
    change that helps only on seeds outside 0-4.
  - `steps` and `seconds` per run are recorded only to set
    `[run].max_seconds`; they judge nothing.
  - A run that crashes or exceeds the cap leaves no `results.json`, and the
    close is VOID; this cannot tell a hang from a slow but sound run.
- **Stopping criterion:** five runs of 300 games each, seeds 0-4, no other
  early stopping; one reading.
- **What would change my mind:** a spread above 30 means single-seed ranges
  are not a usable floor at this budget, and the campaign needs a different
  instrument (more seeds per reading, or the interval of the mean) before
  any iteration. A spread under 5 would suggest the seeding is not reaching
  everything that should vary, and would be checked before being trusted.
- **Minimum detectable effect:** the floor itself: a later change must move
  the five-seed mean by more than the spread measured here to count. Against
  the assumed 10-20 point spread (this is the first contract in the project,
  so the number is assumed, not measured), that is a 10-20 point gain on a
  20-40 baseline.

## Method

- **Script(s):** none beyond the harness; `train.py` computes the statistic.
- **Command:** `uv run train.py --games 300 --last 100 --seeds 0-4 --no-render`
- **Seed(s):** `0, 1, 2, 3, 4`, one 300-game run each, in parallel, headless.
- **Data:** none; the Snake environment is generated, and its food placement
  is seeded by the run seed.
- **Key parameters:** the constants of `agent.py` at this commit:
  `MAX_MEMORY=100000`, `BATCH_SIZE=1000`, `LR=0.001`, `GAMMA=0.9`,
  `HIDDEN_SIZE=256`, `EXPLORE_GAMES=80`; `Linear_QNet(11, 256, 3)`, Adam,
  MSE loss.
- **Writes:** `results.json` in `$SCIPACT_EXPERIMENT_DIR` with `noise_floor`,
  `baseline`, `mean_score` and the per-seed runs; `runs/` beside it.

---

## Results

`mean_score` over the last 100 of 300 games, one run per seed, 300 games each:

| seed | mean_score | record | steps | seconds | mean of first 100 games |
|---|---|---|---|---|---|
| 0 | 33.75 | 76 | 166658 | 47.1 | 4.62 |
| 1 | 32.76 | 68 | 163206 | 46.8 | 1.49 |
| 2 | 32.60 | 66 | 159076 | 44.4 | 6.60 |
| 3 | 32.84 | 81 | 159303 | 44.6 | 0.39 |
| 4 | 33.92 | 71 | 172125 | 48.1 | 3.21 |

Mean over seeds **33.174**, std 0.61 (so the mean's standard error is about
0.27), min 32.60, max 33.92, **spread (noise_floor) 1.32**. The whole
reading took 49 s wall clock with the five runs in parallel.

```
✓ 001-spread-of-mean-score-unchanged closed: PASS
    key statistic noise_floor = 1.32
    PASS          fired  noise_floor <= 20
    FAIL          no     noise_floor > 30
```

## Interpretation

The PASS branch fired: `noise_floor` = 1.32 is at most 20. Iterations
inherit floor 1.32 and baseline 33.174.

The pre-registration said a spread under 5 would be checked before being
trusted, since it could mean the seeding was not reaching everything. It is
reaching everything: the five runs differ in their records (66-81), their
step counts (159k-172k) and, most visibly, their learning curves (the mean
of the first 100 games ranges from 0.39 to 6.60). What is tight is the
level at game 300, not the runs: every seed converges to the same plateau
near 33, and the last-100 mean averages 100 games of it, so its per-seed
standard error is about 1.3 for a per-game score std of about 13. A spread
of 1.32 over five such values is what that arithmetic gives. The prior
(10-20 points) was wrong about the plateau's stability, not about the
seeding.

## Deviations from pre-registration

none

## Next steps

- Set `[run].max_seconds` from the measured 49 s reading, with room for
  changes that lengthen games (a better agent plays longer games): 600 s.
- Open the first iteration against baseline 33.174 with floor 1.32.
- Recalibrate after the first KEEP: the spread grows with the level, and a
  floor measured at 33 will under-read the noise at 60 or 90.

## Caveats / known issues

- The floor is the range of five single-seed values applied to a five-seed
  mean, so it over-reads the mean's noise (SE about 0.27) by about five
  times; KEEP is conservative. That is the approved scope's rule.
- Five seeds give one draw of the range; a different five could read
  somewhat tighter or looser. The same five are used for every step, so the
  comparison is paired, but a change that helps only on other seeds is
  invisible here.

## Reviewer notes
*For the human reviewer. The agent never writes here. Date each note.*

-

## Related experiments
*Optional. Predecessor and successor links live in the front matter too.*
