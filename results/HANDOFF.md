# Handoff: current position

For an agent taking over. A current snapshot, not a history; git keeps the
old versions. Rewrite it in full at every handoff and keep it under a screen.

## Where we are

- Campaign: hill-climb `mean_score` (last 100 of 300 games, mean over seeds
  0-4) of the Snake DQN agent; 10 iterations, then hand off. 1 of 10 run.
- Best kept: **75.22** with trap bits in the state (002, KEEP, +42.05 over
  the tutorial's 33.17). HEAD holds it.
- Floor in force 1.32 (001), measured at level 33; stale. A reading now
  takes about 280 s; `[run].max_seconds` is 1500.

## Next

1. Recalibrate on the kept code: what is the spread at level 75?
2. Does a lower learning rate (2.5e-4) lift the plateau, given noisy
   single-step updates on top of the batch replay?
3. Then: Huber loss, a target network, longer exploration, a deeper net,
   a food-distance feature.

## Blocked on a person

- Nothing.

## Do not rediscover

- The floor is tight (1.32 at level 33) because the plateau is stable, not
  because the seeds fail to vary (001).
- Self-trapping was the tutorial agent's plateau: three trap bits (capped
  flood fill per move) more than double every seed (002).
