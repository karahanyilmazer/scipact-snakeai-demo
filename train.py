#!/usr/bin/env python3
"""Fixed-budget, seeded, optionally headless training runs that write results.json.

    uv run train.py --games 300 --seed 0 --no-render               one run
    uv run train.py --games 300 --seeds 0-4 --no-render            identical runs: spread and mean
    uv run train.py --games 300 --seeds 0-2 --ab HIDDEN_SIZE=512   A/B over the same seeds
    uv run train.py --smoke                                        does the code run? (10 games)

The algorithm lives in agent.py and model.py; this file only runs it and
measures. The statistic is mean_score: the mean score over the last --last
games of a run. results.json goes to $SCIPACT_EXPERIMENT_DIR when that is
set, else to the current directory; --out overrides.
"""

import argparse
import json
import math
import os
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_GAMES = 300
DEFAULT_LAST = 100
SMOKE_GAMES = 10
# Two-sided 95 % Student t quantiles by degrees of freedom, for the paired A/B interval.
T_95 = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
    16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
}  # fmt: skip


def parse_seeds(spec):
    """'0-4' -> [0, 1, 2, 3, 4]; '0,1,2' -> [0, 1, 2]; '5' -> [0, 1, 2, 3, 4]."""
    spec = spec.strip()
    if "," in spec:
        return [int(s) for s in spec.split(",") if s.strip()]
    if "-" in spec:
        lo, hi = spec.split("-", 1)
        return list(range(int(lo), int(hi) + 1))
    return list(range(int(spec)))


def parse_overrides(items):
    out = {}
    for item in items:
        name, sep, value = item.partition("=")
        if not sep or not name.isupper():
            raise SystemExit(
                f"train.py: expected NAME=VALUE with an uppercase NAME, got {item!r}"
            )
        out[name] = value
    return out


def constants(module):
    """The uppercase numeric constants of agent.py: the run's configuration."""
    return {
        k: v
        for k, v in vars(module).items()
        if k.isupper() and not k.startswith("_") and isinstance(v, (int, float))
    }


def apply_overrides(module, overrides):
    """Set constants on the agent module, each coerced to the type of its current value."""
    known = constants(module)
    for name, raw in overrides.items():
        if name not in known:
            raise SystemExit(
                f"train.py: agent.py has no constant {name}; it has {', '.join(known)}"
            )
        current = known[name]
        try:
            if isinstance(current, bool):
                value = raw.lower() in ("1", "true", "yes")
            elif isinstance(current, int):
                value = int(raw) if raw.lstrip("-").isdigit() else int(float(raw))
            else:
                value = float(raw)
        except ValueError:
            raise SystemExit(
                f"train.py: {name}={raw!r} is not a {type(current).__name__}"
            ) from None
        setattr(module, name, value)
    return constants(module)


def mean(values):
    return sum(values) / len(values)


def run_one(args, overrides):
    """One training run in this process; returns the results dict."""
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    if args.no_render:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    import torch

    torch.set_num_threads(1)  # the net is tiny; threads only add overhead
    import agent as agent_module

    config = apply_overrides(agent_module, overrides)
    games = SMOKE_GAMES if args.smoke else args.games

    def on_game(n, score, record):
        print(f"game {n} score {score} record {record}", flush=True)

    started = time.monotonic()
    scores, steps = agent_module.train(
        games=games,
        seed=args.seed,
        render=not args.no_render,
        fps=args.fps,
        on_game=on_game,
    )
    seconds = time.monotonic() - started
    last = min(args.last, len(scores))
    return {
        "mean_score": round(mean(scores[-last:]), 4),
        "mean_score_all": round(mean(scores), 4),
        "record": max(scores),
        "games": len(scores),
        "last": last,
        "seed": args.seed,
        "steps": steps,
        "seconds": round(seconds, 1),
        "config": config,
        "scores": scores,
    }


def run_many(args, jobs, out_dir):
    """Run (label, seed, overrides) jobs as headless subprocesses, in parallel.

    Each job writes runs/<label>-seed<seed>.{log,json} next to results.json.
    Returns {label: [result per seed, in order]}.
    """
    runs_dir = out_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    workers = args.jobs or min(len(jobs), os.cpu_count() or 1)

    def one(job):
        label, seed, overrides = job
        stem = runs_dir / f"{label}-seed{seed}"
        cmd = [
            sys.executable, str(HERE / "train.py"),
            "--games", str(args.games), "--last", str(args.last), "--seed", str(seed),
            "--no-render", "--out", str(stem.with_suffix(".json")),
        ]  # fmt: skip
        for name, value in overrides.items():
            cmd += ["--set", f"{name}={value}"]
        with stem.with_suffix(".log").open("w") as log:
            code = subprocess.call(cmd, stdout=log, stderr=subprocess.STDOUT, cwd=HERE)
        if code != 0:
            raise RuntimeError(
                f"{label} seed {seed} exited {code}; see {stem.with_suffix('.log')}"
            )
        result = json.loads(stem.with_suffix(".json").read_text())
        print(
            f"{label} seed {seed}: mean_score {result['mean_score']:.2f} "
            f"record {result['record']} ({result['seconds']:.0f} s)",
            flush=True,
        )
        return result

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(one, jobs))
    grouped = {}
    for (label, _, _), result in zip(jobs, results, strict=True):
        grouped.setdefault(label, []).append(result)
    return grouped


def aggregate(runs, args):
    """Identical runs summarised: mean_score is their mean, noise_floor their spread."""
    values = [r["mean_score"] for r in runs]
    m = mean(values)
    return {
        "mean_score": round(m, 4),
        "std": round(statistics.stdev(values), 4) if len(values) > 1 else 0.0,
        "spread": round(max(values) - min(values), 4),
        "noise_floor": round(max(values) - min(values), 4),
        "baseline": round(m, 4),
        "min": min(values),
        "max": max(values),
        "n_seeds": len(runs),
        "seeds": [r["seed"] for r in runs],
        "games": args.games,
        "last": args.last,
        "config": runs[0]["config"],
        "runs": runs,
    }


def run_seeds(args, seeds, overrides, out_dir):
    grouped = run_many(args, [("run", s, overrides) for s in seeds], out_dir)
    return aggregate(grouped["run"], args)


def run_ab(args, seeds, base, treatment, out_dir):
    """Baseline and treatment arms over the same seeds; a paired 95 % interval on the delta."""
    if len(seeds) < 2:
        raise SystemExit(
            "train.py: --ab needs --seeds with at least 2 seeds for a paired interval"
        )
    jobs = [("baseline", s, base) for s in seeds]
    jobs += [("treatment", s, {**base, **treatment}) for s in seeds]
    grouped = run_many(args, jobs, out_dir)
    arms = {label: aggregate(runs, args) for label, runs in grouped.items()}
    deltas = [
        t["mean_score"] - b["mean_score"]
        for b, t in zip(grouped["baseline"], grouped["treatment"], strict=True)
    ]
    n = len(deltas)
    d = mean(deltas)
    half = T_95.get(n - 1, 1.96) * statistics.stdev(deltas) / math.sqrt(n)
    return {
        "delta": round(d, 4),
        "ci_low": round(d - half, 4),
        "ci_high": round(d + half, 4),
        "deltas": [round(x, 4) for x in deltas],
        "n_seeds": n,
        "seeds": seeds,
        "games": args.games,
        "last": args.last,
        "treatment_config": {k: arms["treatment"]["config"][k] for k in treatment},
        "arms": arms,
    }


def summary(result):
    if "delta" in result:
        t, b = result["arms"]["treatment"], result["arms"]["baseline"]
        return (
            f"delta {result['delta']:+.2f} [{result['ci_low']:+.2f}, {result['ci_high']:+.2f}] "
            f"over {result['n_seeds']} seeds: treatment {t['mean_score']:.2f} vs baseline "
            f"{b['mean_score']:.2f} ({result['treatment_config']})"
        )
    if "noise_floor" in result:
        return (
            f"mean_score {result['mean_score']:.2f} over {result['n_seeds']} seeds "
            f"(std {result['std']:.2f}, spread {result['spread']:.2f}); "
            f"noise_floor {result['noise_floor']:.2f}, baseline {result['baseline']:.2f}"
        )
    return (
        f"mean_score {result['mean_score']:.2f} over the last {result['last']} of "
        f"{result['games']} games; record {result['record']}; seed {result['seed']}; "
        f"{result['steps']} steps in {result['seconds']:.0f} s"
    )


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    os.replace(tmp, path)


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument(
        "--games",
        type=int,
        default=DEFAULT_GAMES,
        help="games per run (default %(default)s)",
    )
    p.add_argument(
        "--last",
        type=int,
        default=DEFAULT_LAST,
        help="mean_score averages the last LAST games (default %(default)s)",
    )
    which = p.add_mutually_exclusive_group()
    which.add_argument(
        "--seed",
        type=int,
        default=0,
        help="the seed of a single run (default %(default)s)",
    )
    which.add_argument(
        "--seeds",
        type=parse_seeds,
        metavar="SPEC",
        help="identical runs over these seeds, in parallel and headless: '0-4', '0,1,2' or '5' (= 0-4)",
    )
    p.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="override a constant of agent.py for this run, e.g. HIDDEN_SIZE=512; repeatable",
    )
    p.add_argument(
        "--ab",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="A/B: run a baseline arm (without these overrides) and a treatment arm (with them) over the same --seeds and report the paired delta; repeatable",
    )
    p.add_argument(
        "--no-render",
        action="store_true",
        help="no window: skip drawing and the frame clock (much faster)",
    )
    p.add_argument(
        "--fps",
        type=int,
        default=40,
        help="frames per second when rendering; 0 for unthrottled (default %(default)s)",
    )
    p.add_argument(
        "--jobs",
        type=int,
        help="parallel processes for --seeds (default: one per seed, at most the CPU count)",
    )
    p.add_argument(
        "--out",
        type=Path,
        help="results file (default: $SCIPACT_EXPERIMENT_DIR/results.json, else ./results.json)",
    )
    p.add_argument(
        "--smoke",
        action="store_true",
        help=f"a {SMOKE_GAMES}-game headless run that writes nothing: does the code run?",
    )
    return p.parse_args(argv)  # fmt: skip


def main(argv=None):
    args = parse_args(argv)
    overrides = parse_overrides(args.set)
    treatment = parse_overrides(args.ab)
    if args.smoke:
        args.no_render, args.seeds = True, None
    if treatment and not args.seeds:
        raise SystemExit(
            "train.py: --ab needs --seeds (2 or more) so the arms share seeds"
        )
    out = args.out
    if out is None:
        exp_dir = os.environ.get("SCIPACT_EXPERIMENT_DIR")
        out = Path(exp_dir) / "results.json" if exp_dir else Path("results.json")

    started = time.monotonic()
    if args.seeds:
        args.no_render = True
        if treatment:
            result = run_ab(args, args.seeds, overrides, treatment, out.parent)
        else:
            result = run_seeds(args, args.seeds, overrides, out.parent)
        result["seconds"] = round(time.monotonic() - started, 1)
    else:
        result = run_one(args, overrides)

    print(summary(result))
    if args.smoke:
        return 0
    write_json(out, result)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
