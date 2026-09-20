# Scope

What the agent may do in this project without asking, what it may not, and
what always needs a person. A person approves this file once with
`scipact approve scope`. Editing it afterwards withdraws the approval until
someone approves it again.

The campaign: hill-climb `mean_score` (the mean score over the last 100 of
300 games, averaged over seeds 0-4) of the Snake DQN agent, one change per
step, under the autoresearch loop. The harness is `train.py`; the algorithm
under test is `agent.py` and `model.py`.

## In scope

- One calibration of the unchanged code: "what is the run-to-run spread of
  `mean_score` over seeds 0-4?"; a re-calibration after a KEEP if the floor
  looks stale (the spread grows with the score).
- Iterations that change `agent.py` or `model.py` only, one idea each:
  hyperparameters (`LR`, `GAMMA`, `HIDDEN_SIZE`, `BATCH_SIZE`, `MAX_MEMORY`,
  `EXPLORE_GAMES`), the exploration schedule, the state features in
  `get_state`, the network (depth, width, activation), the trainer (loss,
  optimizer, target computation, batching, a target network, double DQN).
- Budget: 300 games per run, `--last 100`, seeds 0-4, headless; at most
  10 iterations in this campaign, then a handoff.

## Out of scope

- `game.py` (the environment, its rewards, the board) and `train.py` (the
  harness, the budget, the statistic): changing them changes the question.
- New metrics, more games per run, other seeds for the readings; a longer
  budget or a tighter instrument is a scope edit.
- Anything that needs the network or writes outside the repository.

## Always ask a person

An experiment that involves any of these is marked `needs_approval: true` and
waits for `scipact approve`, whatever the mode:

- held-out or test data (`held_out_data`) — there is none here
- an external submission (`external_submission`)
- deleting or overwriting data (`deletes_data`)

## How a result counts

- A reading is `mean_score` over seeds 0-4 of one command, all five seeds
  every time; the calibration's spread over those seeds is the noise floor.
- An iteration is KEEP only when its reading beats the best kept baseline by
  more than the floor; otherwise the change is reverted. Inside the floor is
  a plateau, not a signal.
- INCONCLUSIVE is a real answer and is recorded as one.

```toml
version = "1"                # a label for people; the approval binds to the content
status = "draft"

[results]
min_seeds = 5
threshold_tolerance = 0      # bars as written

[iteration]
statistic = "mean_score"
direction = "max"
calibration_runs = 5         # seeds 0-4, one run each
```

## Stop and ask

A result that contradicts an assumption above; a lock that fails to verify
without a documented deviation; a run that times out. Three unresolved
verdicts in a row are the bar (`scipact status` says so): change approach
first, stop at twice the bar. Ten iterations closed: stop and hand off.
