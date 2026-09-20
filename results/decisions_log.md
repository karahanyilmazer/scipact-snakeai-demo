# Decisions log

Dated methodological decisions and the reasoning behind them. An experiment
answers one question with numbers; this file records the choices *between*
experiments, including the ones made without running anything.

Newest entries at the bottom. Each entry ends with *What would change my
mind*.

---

## 2026-09-20: the floor is the single-seed range; the run cap is 600 s

The approved scope judges a five-seed mean against the range (max - min) of
the five single-seed values of the calibration, which `train.py --seeds`
writes as `noise_floor`. That over-reads the noise of the mean by roughly
five times (001: range 1.32, standard error of the mean 0.27), so KEEP is
conservative and the per-seed values are kept in every `results.json` for a
later, sharper reading. `[run].max_seconds` is set to 600 from the measured
49 s five-seed reading: a better agent plays longer games, and a change that
widens the state or the network slows every step.

*What would change my mind:* a run of INCONCLUSIVE verdicts on changes whose
per-seed deltas all share a sign would mean the range is hiding real effects
and the instrument should be sharpened (a scope edit, so a person's call); a
reading killed at the cap that was sound would mean raising it.
