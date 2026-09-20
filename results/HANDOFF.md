# Handoff: current position

For an agent taking over. A current snapshot, not a history; git keeps the
old versions. Rewrite it in full at every handoff and keep it under a screen.

## Where we are

- Campaign: hill-climb `mean_score` (last 100 of 300 games, mean over seeds
  0-4) of the Snake DQN agent; 10 iterations, then hand off. 0 of 10 run.
- Baseline 33.17, noise floor 1.32, both from calibration 001 (PASS). A
  reading takes about 50 s; `[run].max_seconds` is 600.
- Best kept: the unchanged tutorial code (HEAD), 33.17.

## Next

1. Does a dead-end (trap) detector in the state lift the plateau? Self-
   trapping is the visible death cause at this level.
2. Does a lower learning rate (2.5e-4) lift the plateau, given noisy
   single-step updates on top of the batch replay?
3. Then: Huber loss, a target network, longer exploration, a deeper net.

## Blocked on a person

- Nothing.

## Do not rediscover

- The floor is tight (1.32 at level 33) because the plateau is stable, not
  because the seeds fail to vary (001).
