---
scipact: 1
number: 5
slug: spread-with-lr-2p5e-4
title: What is the run-to-run spread of mean_score on the kept code with trap bits and LR 2.5e-4?
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
    PASS: noise_floor <= 12
    FAIL: noise_floor > 20
  otherwise: INCONCLUSIVE
predecessor: null
successor: null
calibration: true
---
# Experiment 005: What is the run-to-run spread of mean_score on the kept code with trap bits and LR 2.5e-4?

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
last 100 of 300 games) on the kept code after 004 (trap bits, LR 2.5e-4),
trained once on each of seeds 0-4? The floor in force (5.48, from 003) was
measured at level 75; 004 moved the level to 82 with a per-seed spread of
9.15, so the floor under-reads the noise and is re-measured here.

## Hypothesis / Prior

Diagnostic - no directional prior. Training was shown deterministic under
the seeds (003 reproduced 002 exactly), so this contract is expected to
reproduce 004's per-seed values: spread 9.15, mean 82.18. It is run rather
than copied because the scope inherits a floor only from a calibration
contract's own results, and a re-run is also a second determinism check.

## Pre-registration

- **Specific quantitative outputs:** `train.py --seeds 0-4` writes to
  `results.json`: `mean_score` (the mean over the five seeds), `std`,
  `spread` and `noise_floor` (max - min of the five per-seed values),
  `baseline` (= the mean), `min`, `max`, `n_seeds`, `seeds`, `seconds`, and
  under `runs` each seed's own results.
- **Decision rule:** the statistic is `noise_floor`. PASS if it is at most
  12 points: at a level near 82, a floor of 12 still resolves a change worth
  keeping (about a seventh of the level) in one reading. FAIL if above 20:
  only changes of a quarter of the level could then resolve, and the
  instrument needs tightening (a scope edit) first. Between 12 and 20,
  INCONCLUSIVE: a floor nothing inherits, and the design is revisited.
- **Instrument check:**
  - `noise_floor` is the range of five single-seed values applied to a
    five-seed mean: it over-reads the mean's noise by roughly a factor of
    five and cannot detect a real improvement smaller than the single-seed
    range (INCONCLUSIVE instead). The approved scope's trade.
  - The same seeds as 004 under deterministic training: this is 004's
    reading again, so it cannot detect that seeds 0-4 are an unusually
    tight or loose set; it only re-states the floor at the level the next
    iterations are judged at, and checks determinism once more.
  - `baseline` is the mean of the five seeds every step uses, so the
    comparison is paired; it cannot detect a change that helps only on
    other seeds.
  - A crash or a run over the 1500 s cap leaves no `results.json`; the
    close is VOID, and this cannot tell a hang from a slow, sound run.
- **Stopping criterion:** five runs of 300 games each, seeds 0-4, no other
  early stopping; one reading.
- **What would change my mind:** a spread above 20 at level 82 means the
  single-seed range is not a usable floor at this budget and the campaign
  needs a sharper instrument before the next iteration; per-seed values
  that differ from 004's mean the seeding leaves something unseeded, and
  that goes into the decisions log before the next step.
- **Minimum detectable effect:** the floor itself, expected 9.15 from 004's
  per-seed spread: a later change must move the five-seed mean by more than
  that, about 11 % of the level.

## Method

- **Script(s):** none beyond the harness; `train.py` computes the statistic.
- **Command:** `uv run train.py --games 300 --last 100 --seeds 0-4 --no-render`
- **Seed(s):** `0, 1, 2, 3, 4`, one 300-game run each, in parallel, headless.
- **Data:** none; the Snake environment is generated, and its food placement
  is seeded by the run seed.
- **Key parameters:** the constants of `agent.py` at this commit:
  `MAX_MEMORY=100000`, `BATCH_SIZE=1000`, `LR=0.00025`, `GAMMA=0.9`,
  `HIDDEN_SIZE=256`, `EXPLORE_GAMES=80`, `STATE_SIZE=14`;
  `Linear_QNet(14, 256, 3)`, Adam, MSE loss.
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
