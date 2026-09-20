# Experiment index

One row per experiment, newest at the bottom. The **Outcome** column is the
experiment's TL;DR; this table should be readable without opening a folder.

> **This file is generated** by `scipact index --write`. Edit an experiment's
> front matter, never this table.

Conventions: numbers are never reused; an abandoned experiment becomes
`superseded` with a forward link; verdicts are three-valued and INCONCLUSIVE is
a real answer. **Approval** says who had to say yes: a person, or the approved
scope.

| # | Title | Weight | Approval | Status | Verdict | Date | Outcome (TL;DR) |
|---|-------|--------|----------|--------|---------|------|-----------------|
| [001](001-spread-of-mean-score-unchanged/) | What is the run-to-run spread of mean_score on the unchanged code? | full | scope | done | PASS | 2026-09-20 | PASS: the unchanged agent scores 33.17 +/- 0.61 over seeds 0-4 with a seed-to-seed spread of 1.32, so the noise floor is 1.32 and the baseline 33.17. |
| [002](002-trap-bits-in-state/) | Trap bits in the state: one per move, set when the reachable area is smaller than the snake | iteration | scope | done | KEEP | 2026-09-20 | KEEP: trap bits lift mean_score from 33.17 to 75.22 (+42.05, floor 1.32), every seed more than doubling. |
| [003](003-spread-with-trap-bits/) | What is the run-to-run spread of mean_score on the kept code with trap bits? | full | scope | done | PASS | 2026-09-20 | PASS: on the kept code the spread over seeds 0-4 is 5.48 around a mean of 75.22, reproducing 002 bit for bit, so the floor is 5.48 and the baseline 75.22. |
| [004](004-lr-2p5e-4/) | LR 2.5e-4 instead of 1e-3 | iteration | scope | done | KEEP | 2026-09-20 | KEEP: LR 2.5e-4 lifts mean_score from 75.22 to 82.18 (+6.96, floor 5.48), all five seeds up. |
| [005](005-spread-with-lr-2p5e-4/) | What is the run-to-run spread of mean_score on the kept code with trap bits and LR 2.5e-4? | full | scope | done | PASS | 2026-09-20 | PASS: on the kept code (trap bits, LR 2.5e-4) the spread over seeds 0-4 is 9.15 around a mean of 82.18, reproducing 004 exactly, so the floor is 9.15 and the baseline 82.18. |
| [006](006-huber-loss/) | Huber (SmoothL1) loss instead of MSE | iteration | scope | done | DISCARD | 2026-09-20 | DISCARD: Huber loss drops mean_score from 82.18 to 65.04 (-17.14, floor 9.15), with seeds split 46-84. |
| [007](007-free-run-features/) | Free-run length per move as three state features | iteration | scope | done | DISCARD | 2026-09-20 | DISCARD: free-run features drop mean_score from 82.18 to 72.02 (-10.16, floor 9.15), every seed down. |
| [008](008-four-replay-batches/) | Four replay batches per game instead of one | iteration | scope | done | INCONCLUSIVE | 2026-09-20 | INCONCLUSIVE: four replay batches per game read 87.13 vs 82.18 (+4.95, floor 9.15); four seeds up 8-10, one down 9.6 from a late sag. |
| [009](009-target-network/) | Target network synced every 1000 train steps | iteration | scope | planned |  |  |  |
