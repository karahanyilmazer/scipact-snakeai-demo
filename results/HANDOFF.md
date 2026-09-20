# Handoff: current position

For an agent taking over. A current snapshot, not a history; git keeps the
old versions. Rewrite it in full at every handoff and keep it under a screen.

## Where we are

- Campaign: hill-climb `mean_score` (last 100 of 300 games, mean over seeds
  0-4) of the Snake DQN agent; 10 iterations, then hand off. 2 of 10 run.
- Best kept: **82.18** with trap bits (002, +42.05) and LR 2.5e-4 (004,
  +6.96) on the tutorial's 33.17. HEAD holds both.
- Floor in force 9.15, baseline 82.18 (005, PASS); KEEP needs > 91.33. A
  reading now
  takes about 280 s; `[run].max_seconds` is 1500.

## Next

1. Does a Huber loss lift the plateau (the -10/+10 rewards make MSE
   targets spiky)?
2. Then: a target network, longer exploration, a deeper net, a
   food-distance feature, a bigger batch, GAMMA 0.95.

## Blocked on a person

- Nothing.

## Do not rediscover

- The floor is tight (1.32 at level 33) because the plateau is stable, not
  because the seeds fail to vary (001).
- Self-trapping was the tutorial agent's plateau: three trap bits (capped
  flood fill per move) more than double every seed (002).
- LR 2.5e-4 beats 1e-3 on every seed at level 75 (004); a lower LR still
  is untested.
- Training is deterministic under the seeds: 003 reproduced 002 exactly, so
  a re-run is a code check, not a new noise draw.
