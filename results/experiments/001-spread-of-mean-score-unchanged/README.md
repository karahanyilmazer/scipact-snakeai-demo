---
scipact: 1
number: 1
slug: spread-of-mean-score-unchanged
title: What is the run-to-run spread of mean_score on the unchanged code?
status: planned
weight: full
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

**Outcome (TL;DR):** *one sentence, filled in after running, leading with the verdict. The single most important field.*

**So what?** *Two or three plain-language sentences, filled in after running. Why does this matter for the next decision? Write for a reader who has not seen the details below.*

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
*Fill in after running.*

The actual numbers, with intervals. A bare point estimate is not a result.
Embed figures from `./figures/`. Quote the verdict block that `scipact close`
printed.

## Interpretation
*Fill in after running. The agent's reading of the results, applying the
pre-registered rule. Name which branch fired. Be honest about ambiguity; if
the experiment did not cleanly answer the question, say so.*

## Deviations from pre-registration
*Fill in after running. Leave as "none" if there were none. The lock detects
edits to the sections above; a documented deviation is a finding, an
undocumented one is noise in the archive.*

none

## Next steps
*Fill in after running.*

## Caveats / known issues
*Fill in after running.*

## Reviewer notes
*For the human reviewer. The agent never writes here. Date each note.*

-

## Related experiments
*Optional. Predecessor and successor links live in the front matter too.*
