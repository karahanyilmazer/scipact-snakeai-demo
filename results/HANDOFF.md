# Handoff: current position

For the agent who runs the next campaign. A current snapshot, not a history;
`results/CONSOLIDATION.md` has the reasoning and every number, and git keeps
the old versions. Rewrite this file in full at every handoff and keep it
under a screen.

## Where we are

- 2026-09-21: three campaigns consolidated on this branch (`supervised`,
  `autonomous`, `autonomous-2`; 41 experiments, all archives `scipact check`
  clean). No experiment has run under this branch's scope yet.
- **Code:** `e2af12e` = `main` at `e7db21e` (the harness with `--replicates`)
  + the kept `agent.py` from `autonomous-2` (trap bits, LR 2.5e-4). This is
  the base every A/B's baseline arm runs from. `uv run train.py --smoke`
  passes.
- **Settled:** the tutorial agent is 33.2 ± 1.1 per seed and state-bound;
  trap bits are +42 (73.3 over 15 fresh seeds at LR 1e-3); LR 2.5e-4 on top
  is up on all 8 fixed seeds tried. Everything else tried is null or
  harmful at 300 games (`CONSOLIDATION.md` §2, §5 for the closed list).
- **Not settled:** what the kept code scores on fresh seeds (82.18 and
  90.49 are fixed-seed readings on two feature orderings of the same
  function; seeds 0-4 sat +3.7 above the 15-seed mean one level down); and
  four leads inside their old floors: four replay batches (+5.0), the tail
  cell free in the trap count (+3.5), tail-reachable bits instead of trap
  bits (+7.6), LR 5e-4 (+4.2).
- **Instrument for this campaign:** paired A/B over seeds 0-19 (the
  archived paired per-seed sd of 5-6 gives ±2.7 at 20 seeds; 5 seeds gave
  ±7, which is why the leads are still leads). Rule: ADOPT `delta >= 3 and
  ci_low > 0`; REJECT `ci_high < 3`. About 25 min per A/B, 40 min for the
  calibration, on this 12-core machine.

## Next

1. Read `results/SCOPE.md` (draft) with the person; `scipact approve scope`.
   The `[run].max_seconds` of 5400 and the bars (ADOPT ≥ 3, calibration
   PASS ≤ 5 / FAIL > 10) are proposals; change them before approval if you
   disagree, not after.
2. Calibration contract on the unchanged code:
   `uv run train.py --games 300 --seeds 0-19 --replicates 3 --no-render`.
   Report `baseline` as the kept code's number. From `runs/`, count seeds
   with first score ≥ 20 after game 150 and seeds ending ≤ 2: that is the
   take-off confound and the collapse rate, both open.
3. Wave 1, four contracts, each one commit that adds a constant with the
   kept behaviour as default, then `--ab CONST=value`:
   `REPLAY_BATCHES=4` (`autonomous-2` 48a594a has the code),
   `TAIL_FREE=1` (1439df6), `TAIL_BITS=1` (`autonomous` 1c84028's
   `_tail_region`, appended at 11-13 in place of the trap bits), `LR=0.0005`.
   Independent; dispatch concurrently if the machine is free, they contend
   for the same 12 cores otherwise.
4. Wave 2 from the ADOPTs: pairwise combinations; an LR schedule as one
   change. Then hand off.

## Blocked on a person

- Scope approval (step 1).
- The budget diagnostic (500 games, kept code, seeds 0-19, games 401-500 vs
  201-300): withdrawn by the reviewer in `supervised` 005, so ask, do not
  open. It is the run that separates plateau lifts from take-off effects.
- Optional harness change: `--ab` re-runs the deterministic baseline arm
  every time; an option to reuse a recorded arm halves each A/B. `train.py`
  is out of scope for the agent.

## Do not rediscover

- The two trap-bit implementations are the same function
  (`results/consolidation/trap_bits_equivalent.py`); do not A/B one against
  the other. Feature order alone moved a 3-seed reading by 9 points at LR
  2.5e-4, through take-off timing.
- `autonomous-2`'s floors 1.32 / 5.48 / 9.15 were single-seed ranges on
  fixed seeds (`noise_floor` of the old harness = today's `seed_spread`);
  `autonomous`'s 1.51 / 13.17 were ranges of disjoint 3-seed block means.
  Neither is a paired resolution. Do not inherit either.
- LR below 2.5e-4 collapses seeds inside 300 games (0.3-2.0 on one seed in
  three or five); LR is not a knob to lower further at this budget.
- The `supervised` "do not ask about LR" closure is for the 11-bit agent
  only.
- The gate hook matches `train.py` invocations anywhere in a Bash command;
  run experiments through `scipact run NNN -- <command>`; `--smoke` is
  exempt.
- `python3 results/consolidation/collect.py` regenerates the cross-campaign
  table from the branches; nothing in `results/consolidation/` needs a
  training run.
