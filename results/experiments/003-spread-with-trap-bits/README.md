---
scipact: 1
number: 3
slug: spread-with-trap-bits
title: What is the run-to-run spread of mean_score on the kept code with trap bits?
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
tldr: "PASS: on the kept code the spread over seeds 0-4 is 5.48 around a mean of 75.22, reproducing 002 bit for bit, so the floor is 5.48 and the baseline 75.22."
results: results.json
rule:
  statistic: noise_floor
  branches:
    PASS: noise_floor <= 10
    FAIL: noise_floor > 20
  otherwise: INCONCLUSIVE
predecessor: null
successor: null
calibration: true
---
# Experiment 003: What is the run-to-run spread of mean_score on the kept code with trap bits?

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

**Outcome (TL;DR):** PASS: on the kept code the spread over seeds 0-4 is 5.48 around a mean of 75.22, reproducing 002 bit for bit, so the floor is 5.48 and the baseline 75.22.

**So what?** The floor grew from 1.32 to 5.48 as the level went from 33 to 75, as expected: longer, more variable games. The next iterations need to lift the five-seed mean above 80.70 to count. The reading also showed training is fully deterministic under the seeds (every per-seed value, record and step count matched 002), so a repeat of a command is a check of the code, never a new draw of the noise.

---

## Question

What is the seed-to-seed spread of `mean_score` (the mean score over the
last 100 of 300 games) on the kept code after 002 (trap bits in the state),
trained once on each of seeds 0-4? 002 moved the level from 33 to 75, and
the floor of 1.32 measured at 33 (001) under-reads the noise at 75; this
contract re-measures it so the next iterations are judged at their level.

## Hypothesis / Prior

Diagnostic - no directional prior. The expectation, so it can be wrong:
002's reading of the same command on the same seeds had a per-seed spread
of 5.48 (std 2.48); if training is deterministic under the seeds this
contract reproduces those numbers exactly, and if it is not the spread
should still land near 5, since the sources of run-to-run variation (food
placement, exploration, initial weights) are seeded.

## Pre-registration

- **Specific quantitative outputs:** `train.py --seeds 0-4` writes to
  `results.json`: `mean_score` (the mean over the five seeds), `std`,
  `spread` and `noise_floor` (max - min of the five per-seed values),
  `baseline` (= the mean), `min`, `max`, `n_seeds`, `seeds`, `seconds`, and
  under `runs` each seed's own results.
- **Decision rule:** the statistic is `noise_floor`. PASS if it is at most
  10 points: at a baseline near 75, a floor of 10 lets a change of the size
  worth keeping here (a tenth or more of the level) resolve in one reading.
  FAIL if above 20: then only changes that move the level by more than a
  quarter could resolve, and the instrument needs tightening (a scope edit)
  before looping on. Between 10 and 20, INCONCLUSIVE: a floor nothing
  inherits, and the design is revisited.
- **Instrument check:**
  - `noise_floor` is the range of five single-seed values applied to a
    five-seed mean: it over-reads the mean's noise by roughly a factor of
    five and cannot detect a real improvement smaller than the single-seed
    range (INCONCLUSIVE instead). The approved scope's trade.
  - The same seeds as 002: if training is deterministic, this reading is
    002's reading again and adds no independent draw of the range; it then
    cannot detect that seeds 0-4 are an unusually tight or loose set. What
    it does add is a determinism check (identical per-seed values or not),
    recorded under Results either way.
  - `baseline` is the mean of the same five seeds every step uses, so the
    comparison stays paired; it cannot detect a change that helps only on
    seeds outside 0-4.
  - A crash or a run over the 1500 s cap leaves no `results.json`; the
    close is VOID, and this cannot tell a hang from a slow, sound run.
- **Stopping criterion:** five runs of 300 games each, seeds 0-4, no other
  early stopping; one reading.
- **What would change my mind:** a spread above 20 at level 75 means the
  single-seed range is no longer a usable floor at this budget and the
  campaign needs a sharper instrument (the interval of the mean, or more
  seeds) before the next iteration; per-seed values that differ from 002's
  by more than a point mean the seeding leaves something unseeded, and that
  goes into the decisions log before the next step.
- **Minimum detectable effect:** the floor itself, expected near 5.5 from
  002's per-seed spread: a later change must move the five-seed mean by more
  than that to count, about 7 % of the level.

## Method

- **Script(s):** none beyond the harness; `train.py` computes the statistic.
- **Command:** `uv run train.py --games 300 --last 100 --seeds 0-4 --no-render`
- **Seed(s):** `0, 1, 2, 3, 4`, one 300-game run each, in parallel, headless.
- **Data:** none; the Snake environment is generated, and its food placement
  is seeded by the run seed.
- **Key parameters:** the constants of `agent.py` at this commit:
  `MAX_MEMORY=100000`, `BATCH_SIZE=1000`, `LR=0.001`, `GAMMA=0.9`,
  `HIDDEN_SIZE=256`, `EXPLORE_GAMES=80`, `STATE_SIZE=14` (11 tutorial bits
  plus 3 trap bits); `Linear_QNet(14, 256, 3)`, Adam, MSE loss.
- **Writes:** `results.json` in `$SCIPACT_EXPERIMENT_DIR` with `noise_floor`,
  `baseline`, `mean_score` and the per-seed runs; `runs/` beside it.

---

## Results

| seed | mean_score | record | steps | seconds |
|---|---|---|---|---|
| 0 | 77.12 | 174 | 505568 | 266 |
| 1 | 76.88 | 157 | 543746 | 284 |
| 2 | 76.90 | 169 | 478823 | 250 |
| 3 | 71.64 | 133 | 455723 | 227 |
| 4 | 73.58 | 161 | 477509 | 241 |

Mean over seeds **75.224**, std 2.48 (standard error of the
mean about 1.1), min 71.64, max 77.12, **spread (noise_floor) 5.48**;
wall clock 284 s. Every per-seed `mean_score`, `record` and `steps`
value is identical to 002's.

```
✓ 003-spread-with-trap-bits closed: PASS
    key statistic noise_floor = 5.48
    PASS          fired  noise_floor <= 10
    FAIL          no     noise_floor > 20
```

## Interpretation

The PASS branch fired: `noise_floor` = 5.48 is at most 10. Iterations
inherit floor 5.48 and baseline 75.224 from here.

Training is deterministic under the seeds: this reading is 002's reading to
the last digit. So, as the instrument check said, this contract added no
independent draw of the range; it re-measured the floor at the new level
with the same five seeds, which is what the iterations are paired against.
The spread's growth (1.32 to 5.48, about four times, while the level went
up 2.3 times) is in line with longer games having more room to vary.

## Deviations from pre-registration

none

## Next steps

- Iterations against baseline 75.22 with floor 5.48; KEEP needs > 80.70.
- Because a repeat run reproduces exactly, a future recalibration after a
  KEEP can quote the KEEP's own per-seed spread rather than re-run, if the
  scope is ever edited to allow it; under the current scope it re-runs.

## Caveats / known issues

- The floor is one draw of a five-seed range, and a deterministic re-run
  cannot widen that draw; only different seeds could, and those are out of
  scope.
- The single-seed range over-reads the noise of the five-seed mean (SE
  about 1.1); effects between about 2 and 5.5 points will read
  INCONCLUSIVE.

## Reviewer notes
*For the human reviewer. The agent never writes here. Date each note.*

-

## Related experiments
*Optional. Predecessor and successor links live in the front matter too.*
