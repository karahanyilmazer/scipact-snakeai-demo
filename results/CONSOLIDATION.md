# Consolidation of the three campaigns

Written 2026-09-21 on the `consolidation` branch, from the SciPact archives on
`supervised`, `autonomous` and `autonomous-2` (all forked from `8578331`) and
from `main` at `e7db21e`. Every number below is read from a committed
`results.json`; `consolidation/collect.py` regenerates the full table
(`consolidation/experiments.csv`, 41 experiments) from the branches, and
`consolidation/trap_bits_equivalent.py` reproduces the one code check this
document relies on. Nothing was trained for this document.

The question all three campaigns asked: what raises `mean_score`, the mean
score over the last 100 of 300 games of the tutorial's Snake DQN agent, and by
how much. The short answer: one change (three "trap bits" in the state) more
than doubles it; one hyperparameter (the learning rate, once the state has
those bits) adds something the instruments could not size; nothing else
tried moves it; and the numbers the campaigns headline (33.2, 76.6, 82.2,
90.5) are on different instruments and only the first is a population mean.

## 1. The instruments

Same machine throughout (Apple M4 Pro, 12 cores; Python 3.14.6, torch 2.14.0,
numpy 2.5.3), same budget (300 games, statistic over the last 100), headless.
Training is deterministic under a seed: the five defaults runs on seeds 0-4
read `33.75, 32.76, 32.60, 32.84, 33.92` on all three branches, on two days,
under different parallel loads. Timings vary with load; scores do not.

| Campaign | Command | Reading | Compared against | Resolution used | Code level |
|---|---|---|---|---|---|
| `supervised` 001-004 | `train.py --games 300 --seeds 0-4 --ab NAME=VALUE` | mean over seeds 0-4, both arms | the baseline arm, paired by seed | 95 % paired t-interval; bar 3 (001) then 2 points | tutorial, 11-bit state |
| `supervised` 006 | `train.py --games 300 --seeds 0-19` | 20 single-seed readings | — | single-seed range 3.87, std 1.09; **not inherited** (statistic was one run) | tutorial |
| `autonomous` | `train.py --games 300 --seeds 0-2` | mean over seeds 0-2 | best kept value (same seeds) | floor = range of five **disjoint** 3-seed block means (seeds 0-14, `scripts/calibrate.py`): 1.51 at 33.2, 13.17 at 73.3 | tutorial → trap bits (007) → + LR 2.5e-4 (021) |
| `autonomous-2` | `train.py --games 300 --seeds 0-4` | mean over seeds 0-4 | best kept value (same seeds) | floor = the harness's `noise_floor` key at `8578331`, which was the **single-seed range on the same five seeds**: 1.32, 5.48, 9.15 | tutorial → trap bits (002) → + LR 2.5e-4 (004) |

Three facts about these instruments, all measured:

- **The floors are different quantities.** `autonomous`'s floors are what
  `train.py --replicates` (added in `e7db21e`) now writes: the spread of the
  reading's mean across fresh seed sets. `autonomous-2`'s "calibrations" 003
  and 005 re-ran the seeds of 002 and 004 and reproduced them bit for bit,
  so they measured nothing about repeatability; the range of five single
  seeds is about √5 wider than the spread of their mean would be, and it is
  the quantity `e7db21e` renamed `seed_spread` for exactly this reason. (The
  message of `e7db21e` says two of three campaigns inherited it as the floor;
  reading the archives, one did. `supervised` measured the single-seed range
  for a single-seed statistic and declined to inherit it.)
- **Both loop floors were unpaired, applied to paired comparisons.** Every
  iteration ran on the same fixed seeds as its baseline, so the comparison
  was paired and the archives contain the paired data. The per-seed paired
  difference has a standard deviation of about **5-6 points at the 76-82
  level** (median over 18 archived comparisons: 4.7 on `autonomous`, 5.9 on
  `autonomous-2`; 1.5-9 depending on the change). So a paired 5-seed design
  resolves about ±7, ten seeds ±4, twenty seeds ±2.7 (95 % half-widths). The
  `autonomous-2` handoff's "SE of the mean about 1.6" was optimistic by about
  two.
- **Seeds 0-4 are a quiet, and at the higher level a favourable, subset.**
  At the 11-bit level their std is 0.61 against 1.23 for seeds 5-19 (means
  equal). At the trap-bit level (`autonomous` 008, LR 1e-3) they read 76.95
  against 71.48 for seeds 5-14 and 73.30 for all fifteen. Every headline
  number of the two autonomous campaigns is on seeds 0-4 or 0-2 and should
  be read as sitting a few points above the configuration's mean.

Per-seed noise by level: std 1.09 at 33 (20 seeds), 6.05 at 73 (15 seeds).
The noise grows faster than the score, mostly because of take-off timing
(§3).

## 2. Settled

Settled means: measured on an instrument that can carry the claim, and not
contradicted anywhere in the three archives.

1. **The tutorial agent plateaus at 33.2 ± 1.1 per seed** (20 seeds, `supervised`
   006; 15 seeds, `autonomous` 001, same values). It is at the plateau by
   game ~120 and flat to 300 in every seed (games 101-150 through 251-300
   all read 30-36), so **the plateau is the state's, not the budget's**. The
   1000-game question (`supervised` 005) was withdrawn unrun, but this
   answers what it asked for the 11-bit agent.
2. **Nothing cheap moves the 11-bit agent.** Paired 5-seed intervals: hidden
   512 −0.36 [−1.42, +0.70]; EXPLORE_GAMES 160 +0.64 [−0.29, +1.57]; LR 3e-3
   −2.60 [−5.37, +0.17] (every seed down); LR 3e-4 −0.06 [−2.14, +2.02] (same
   plateau, reached later). 3-seed readings inside a 1.51 floor: danger two
   ahead +1.26, second hidden layer −1.15, GAMMA 0.95 +0.93, 4 replay steps
   +0.15; detaching the TD target −2.92 (DISCARD).
3. **Trap bits are the one large effect.** Three bits, one per move, set when
   the free cells reachable from the landing cell are fewer than the snake is
   long. Written independently twice (`autonomous` 007 as `_is_trap`, bits at
   positions 3-5; `autonomous-2` 002 as `reachable()`, bits at 11-13), the two
   compute the identical function on 20 000 random states
   (`consolidation/trap_bits_equivalent.py`). +43.4 on seeds 0-2, +42.05 on
   seeds 0-4, every seed more than doubled; **73.30 over 15 fresh seeds** at
   LR 1e-3 (`autonomous` 008), which is the only many-seed number above the
   tutorial level in the project. Records (best single game) go from 64-81 to 132-184.
4. **With trap bits, LR 1e-3 → 2.5e-4 raises the 300-game metric on all eight
   fixed seeds** it was tried on (+13.9 on seeds 0-2; +6.96 on seeds 0-4,
   all five up); both campaigns kept it. Its size is not settled (§3, §4).
   Below it, **LR 1e-4 and 1.25e-4 fail**: one seed in three or five never
   takes off inside 300 games (reads 0.3-2.0) and the rest are still
   climbing at game 300 (−41, −52; DISCARD twice).
5. **Harmful at the trap-bit level:** Huber loss (−31.9 at LR 1e-3 on 3 seeds;
   −17.1 at LR 2.5e-4 on 5 seeds, seeds split 46-84); free-run-length
   features (−10.2, every seed down); adding tail-reachable bits *on top of*
   the trap bits as a 17-feature state (−16.2: one seed collapsed to 0.57).
6. **Null at the trap-bit level, within instruments that resolve ~10:** hidden
   512 (−5.3), BATCH 2000 (−3.6), food-relative bits (−1.9), MAX_MEMORY 20k
   (−1.1) and 1e6 (−0.5), GAMMA 0.95 (−1.3 at LR 1e-3, +0.7 at 2.5e-4),
   EXPLORE 40 (+0.4), danger two ahead (+0.9), target network (+1.0). None of
   these has a per-seed pattern worth a second look; GAMMA and the network
   size are now null at both levels and should stay closed at 300 games.

## 3. What contradicts, and why

**90.49 (`autonomous` 021) vs 82.18 (`autonomous-2` 004) for "trap bits + LR
2.5e-4".** Same feature function (§2.3), different position in the state
vector, so under seeded init each feature meets different initial weights
and the trajectories diverge. On the three seeds the two share, the
readings are 90.49 and 81.49, and the gap is take-off timing: the first game
scoring ≥ 20 comes at games 100, 91, 101 on `autonomous` and 111, 113, 173
on `autonomous-2`. A seed that takes off at game 173 spends most of the
last-100 window still climbing (games 201-250 read 70.2, games 251-300 read
84.9). Both readings are inside their own floors of each other; neither is
the configuration's mean; the only calibrated number for trap bits (73.30
over 15 seeds) is at LR 1e-3. **At LR 2.5e-4 the 300-game metric is a
mixture of plateau height and take-off time**, which is why its per-seed
noise is 3-6 and why lowering LR further collapses seeds outright.

**"Do not ask about LR again" (`supervised`) vs KEEP on LR in both autonomous
campaigns.** Different code levels, not a contradiction. At 11 bits the
plateau is set by self-trapping and no LR moves it (§2.2); `supervised` 004's
own diagnostic already saw the mechanism (LR 3e-4 "still rising at game
300"). At 14 bits the plateau is higher and a lower LR reaches a higher one,
at the cost of a later take-off. The `supervised` closure holds for the
11-bit agent only.

**Floors 1.32 / 5.48 / 9.15 vs 1.51 / 13.17.** Different quantities (§1).
`autonomous-2`'s are single-seed ranges on fixed seeds and would read the
same on a perfectly repeatable instrument; `autonomous`'s are ranges of
five disjoint block means. Neither is wrong as a conservative KEEP bar; only
the second describes repeatability. The verdicts do not change under either
reading, but "the floor grew 1.32 → 5.48 → 9.15" (`autonomous-2` handoff)
describes the single-seed spread, not the instrument.

**Four readings of "the tail".** `autonomous` 010, tail-reachable bits
*instead of* trap bits: +7.6 at LR 1e-3, 3 of 3 seeds up, records to 219.
`autonomous` 016, trap bit off when the region reaches the tail: −1.0.
`autonomous-2` 013, the tail cell counts as free in the trap count: +3.5 at
LR 2.5e-4, 4 of 5 seeds up, sag gone. `autonomous` 009, tail bits *added*:
−16.2 with one collapsed seed. These are four different functions on
instruments resolving ±7 to ±15 per reading; nothing contradicts, nothing is
resolved. The two positive ones (010, 013) are the same idea at different
strengths.

**Four replay steps: +0.15 (`autonomous` 005) vs +4.95 (`autonomous-2` 008).**
The first is at 11 bits and LR 1e-3, where the plateau is state-bound; the
second at 14 bits and LR 2.5e-4, where more gradient steps per game bring
take-off forward (first game ≥ 20 at 88-104 instead of 83-173) and four of
five seeds read +7.6 to +10.3 while the fifth sagged −9.6. Consistent with
§3's mechanism, unresolved (paired half-width ±10 on five seeds).

**Provenance notes.** `scipact check` passes on all three archives except a
regenerated-index format difference from a newer CLI. It flags that the
`autonomous` scope approval was recorded without an `asked_at` (the hook was
not running); the quoted approval is the person's, the record is weaker than
`autonomous-2`'s. `supervised` 004 is a REJECT by the 2 % tolerance
(`ci_high` 2.02 against 2.04); read it as INCONCLUSIVE-leaning-null.

## 4. Open

1. **What the kept code actually scores.** Trap bits + LR 2.5e-4 has never
   been run on seeds beyond 0-4. The fixed-seed readings are 82.2 (5 seeds)
   and 90.5 (3 seeds, other feature order); the population mean is likely
   below 82 (seeds 0-4 sat +3.7 at the previous level).
2. **The take-off / plateau confound at LR 2.5e-4** (§3): 2 of 8 fixed seeds
   took off after game 150. Whether 300 games is at the plateau for this
   configuration is the withdrawn budget question in a sharper form; it
   needs a person (see §5).
3. **Four leads, all inside their instruments:** four replay batches per
   game (+5.0, 4/5 up); the tail cell free in the trap count (+3.5, 4/5 up,
   sag gone); tail-reachable bits in place of trap bits (+7.6, 3/3 up, at LR
   1e-3); LR 5e-4 (+4.2, 3/3 up, at LR 1e-3). Combinations untried. An LR
   schedule (1e-3 until take-off, 2.5e-4 after) is the natural way to keep
   the plateau without the late take-off and has not been tried.
4. **The collapse mode.** A seed that never takes off (score ≤ 2 after 300
   games) appeared three times: LR 1.25e-4, LR 1e-4, and the 17-feature state.
   Never on the kept code in 8 seeds. Its frequency at the kept LR sets how
   heavy-tailed the mean is; a calibration on 20+ fresh seeds measures it.
5. **The late sag.** Both autonomous handoffs describe a sag over the last
   100 games. With trap bits at LR 1e-3, games 251-300 read below games
   201-250 in 6 of 8 seeds across both branches (by 5-12 points where they
   do); at LR 2.5e-4 in 3 of 8. Suggestive, not established (a 6-of-8 sign
   is p ≈ 0.14). What it is not: the moving target (target network, +1.0,
   sag unchanged), the horizon (GAMMA); MAX_MEMORY 1e6 made it milder at the
   same plateau. Low priority at the kept LR; the calibration's 60 curves
   will say whether it exists there.

## 5. Proposal for the next campaign

**Start from the tip of `consolidation`.** The code there is `e2af12e`:
`main` at `e7db21e` (the harness with `--replicates`, `seed_spread` honestly
named) plus the kept `agent.py` from `autonomous-2` (trap bits appended at
11-13, LR 2.5e-4; the two cherry-picked `try:` commits, `--smoke` passes).
Not from either autonomous tip: their `train.py` predates `--replicates`
and still writes the single-seed range under the name `noise_floor`, and
`scipact status` there reports 9.15 or 13.17 as the floor in force. The two
trap-bit orderings are interchangeable; the archived fixed-seed numbers will
not reproduce on the other ordering, and the calibration below replaces
them anyway.

**Design: paired A/B over 20 seeds, autonomous waves, not a hill-climb.** The
open questions are few and specific, and the loop's KEEP-against-a-range
rule is what left them open. Each experiment is one command,

    uv run train.py --games 300 --seeds 0-19 --ab NAME=VALUE --no-render

with the change behind an uppercase constant of `agent.py` whose default is
the kept behaviour (`REPLAY_BATCHES = 1`, `TAIL_FREE = 0`, ...), so both
arms run from one commit and the harness writes `delta`, `ci_low`,
`ci_high`. Rule per experiment, before any run: ADOPT if `delta >= 3` and
`ci_low > 0`; REJECT if `ci_high < 3`; otherwise INCONCLUSIVE. With the
archived paired sd of 5-6 the half-width at 20 seeds is about 2.7, so a
true +5 adopts, a true 0 rejects, and +3 is the edge, which is what the leads
are. A constant's default flips only on ADOPT. Cost: 40 runs of 150-350 s
on 12 cores, about 20-25 min per experiment; the baseline arm is recomputed
each time (deterministic, so it is the same 20 numbers; a `train.py` option
to reuse them would halve the cost and is a harness change for a person).

**First contract, a calibration:**

    uv run train.py --games 300 --seeds 0-19 --replicates 3 --no-render

on the kept code, unchanged: 60 fresh seeds, ~35-45 min. It writes the
population mean of the kept code (open item 1), the noise floor of the
20-seed mean, per-seed std and, from `runs/`, the take-off distribution and
the collapse frequency (items 2 and 4). Proposed bars: PASS if `noise_floor
<= 5`, FAIL if `> 10`; the 20-seed mean's spread over three readings should
be 2-4 if per-seed std is ~6. It also says whether seeds 0-19 sit high, as
0-4 did.

**Wave 1** (four independent A/Bs, ~2 h): `REPLAY_BATCHES=4`; `TAIL_FREE=1`
(the tail cell free in the trap count); `TAIL_BITS=1` (tail-reachable bits
in place of trap bits, `autonomous` 010's function); `LR=0.0005`.
**Wave 2**, from wave 1's ADOPTs: their pairwise combinations, and an LR
schedule as one change. Closed, do not reopen at 300 games: network width and
depth, GAMMA, EXPLORE_GAMES, BATCH_SIZE, MAX_MEMORY, Huber, detached target,
danger two ahead, food-relative bits, free-run features, LR ≤ 1.25e-4, a
target network, tail bits added as a 17-feature state.

**For a person, not the scope:** the budget diagnostic, 500 games on the kept
code over seeds 0-19 with games 401-500 against 201-300, which decides
whether the leads are plateau lifts or take-off effects. `supervised` 005
was withdrawn by the reviewer, so it is not reopened without them; it is
the single most informative run the project has not made.

A draft scope with these rules is at `results/SCOPE.md`; `scipact.toml` is
set to autonomous mode with the harness gate. `results/HANDOFF.md` has the
first steps.
