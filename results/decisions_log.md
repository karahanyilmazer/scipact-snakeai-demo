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

## 2026-09-20: run cap raised to 1500 s after 002

The trap-bit KEEP (002) made games about five times longer: a five-seed
reading went from 49 s to 279 s. A cap of 600 leaves no room for a kept
change that lengthens games again, so it is raised to 1500 (about five times
the new reading). The floor of 1.32 was measured at level 33 and the kept
code's own per-seed spread is 5.48, so a calibration on the kept code comes
before the next iteration, as the loop skill requires after a large KEEP.

*What would change my mind:* a sound reading killed at 1500 s means raising
it again; a reading that takes under 100 s again means a change that
shortens games, which the metric would also show.
