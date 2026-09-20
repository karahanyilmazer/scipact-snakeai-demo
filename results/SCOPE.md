# Scope

What the agent may do in this project without asking, what it may not, and
what always needs a person. A person approves this file once with
`scipact approve scope`. Editing it afterwards withdraws the approval until
someone approves it again.

**Status: draft**, proposed by the consolidation of 2026-09-21
(`results/CONSOLIDATION.md`, §5). It is the fourth campaign on this problem
and the first on the kept code (trap bits + LR 2.5e-4, `agent.py` at
`e2af12e`).

The campaign: size the effects the three earlier campaigns left inside their
noise floors, on an instrument that can resolve them. Paired A/B over 20
seeds, one change per contract, in autonomous waves; not a hill-climb. The
harness is `train.py`; the code under test is `agent.py` and `model.py`.

## In scope

- **One calibration first**, on the unchanged kept code:
  `uv run train.py --games 300 --seeds 0-19 --replicates 3 --no-render`
  (60 fresh seeds). It records the kept code's population mean, the noise
  floor of the 20-seed mean, and per seed: the take-off game (first score
  ≥ 20) and any collapse (last-100 mean ≤ 2).
- **Major experiments, one change each**, on `agent.py` or `model.py`, each
  behind an uppercase constant whose default is the kept behaviour, run as
  `uv run train.py --games 300 --seeds 0-19 --ab NAME=VALUE --no-render`.
  Wave 1: `REPLAY_BATCHES=4`; `TAIL_FREE=1` (the tail cell counts as free in
  the trap count); `TAIL_BITS=1` (tail-reachable bits in place of the trap
  bits, `autonomous` 010's function); `LR=0.0005`. Wave 2: pairwise
  combinations of wave 1's ADOPTs; a learning-rate schedule (1e-3 until the
  first score ≥ 20, 2.5e-4 after) as one change.
- Flipping a constant's default in `agent.py` after an ADOPT, in its own
  commit, so the next contract's baseline arm is the adopted code.

## Out of scope

- `game.py` (the environment, its rewards, the board, the step cap) and
  `train.py` (the harness, the budget, the statistic): changing them changes
  the question.
- More or fewer games than 300, a statistic other than `mean_score` over the
  last 100, seeds other than 0-19 for the A/Bs. A tighter or longer
  instrument is a scope edit.
- Reopening what is closed at 300 games (`CONSOLIDATION.md` §2, §5): network
  width and depth, `GAMMA`, `EXPLORE_GAMES`, `BATCH_SIZE`, `MAX_MEMORY`, Huber
  loss, a detached target, danger two ahead, food-relative bits,
  free-run-length features, `LR` ≤ 1.25e-4, a target network, tail bits added
  as a 17-feature state.
- Anything that needs the network or writes outside the repository.

## Always ask a person

An experiment that involves any of these is marked `needs_approval: true` and
waits for `scipact approve`, whatever the mode:

- held-out or test data (`held_out_data`): there is none here
- an external submission (`external_submission`)
- deleting or overwriting data (`deletes_data`): the archive under
  `results/experiments/` is never deleted or rewritten
- **the budget diagnostic**: 500 games on the kept code over seeds 0-19,
  games 401-500 against 201-300. The reviewer withdrew the budget question
  in `supervised` 005; it is not reopened without them. It is also the run
  that would say whether the wave-1 leads lift the plateau or move the
  take-off, so it is worth asking for.

## How a result counts

- A major experiment's statistic is `delta` (treatment − baseline, paired by
  seed over seeds 0-19) with its 95 % t-interval `[ci_low, ci_high]`, as
  `train.py --ab` writes them. **ADOPT** if `delta >= 3` and `ci_low > 0`;
  **REJECT** if `ci_high < 3`; otherwise **INCONCLUSIVE**. The bar of 3 is
  the smallest change to the kept code worth carrying; the archived paired
  per-seed sd of 5-6 gives a half-width of about 2.7 at 20 seeds.
- The calibration's statistic is `noise_floor` (the spread of the three
  20-seed reading means). **PASS** if `noise_floor <= 5`, **FAIL** if
  `noise_floor > 10`, otherwise INCONCLUSIVE; its `baseline` is the kept
  code's mean over 60 seeds and is the number to report for the code, not
  the fixed-seed 82.18 or 90.49.
- Both arms of every A/B run from one commit; the baseline arm is the kept
  code by construction. A change enters the code only on ADOPT.
- INCONCLUSIVE is a real answer and is recorded as one; a lead that reads
  INCONCLUSIVE at 20 seeds is not re-run at more seeds under this scope.

```toml
version = "1"                # a label for people; the approval binds to the content
status = "draft"

[results]
min_seeds = 20
threshold_tolerance = 0      # bars as written

[iteration]
# No iteration-weight contracts in this campaign; the table names the
# statistic the calibration measures.
statistic = "mean_score"
direction = "max"
calibration_runs = 3         # 20-seed readings a calibration averages (--replicates 3)
```

## Stop and ask

A result that contradicts an assumption above; a lock that fails to verify
without a documented deviation; a run that times out; a collapsed seed
(last-100 mean ≤ 2) in the baseline arm of any A/B, which means the kept
code is not the stable base this scope assumes. Three unresolved verdicts
in a row are the bar: change approach first, stop at twice the bar. After
wave 2, or at the clock the person set: stop and hand off.
