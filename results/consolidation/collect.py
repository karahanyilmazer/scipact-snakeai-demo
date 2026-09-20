#!/usr/bin/env python3
"""One table for the three campaigns, read straight from their branches.

    python3 results/consolidation/collect.py            # writes experiments.csv and prints a Markdown table

Each row is one experiment: which branch, its number, the change, the
instrument the number was read on (seeds, comparison, floor or interval),
the reading, the verdict and the per-seed values. Nothing is run; every
number comes from the results.json and README front matter committed on the
branch, via `git show`.
"""

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BRANCHES = ["supervised", "autonomous", "autonomous-2"]


def show(branch, path):
    r = subprocess.run(
        ["git", "show", f"{branch}:{path}"], cwd=ROOT, capture_output=True, text=True
    )
    return r.stdout if r.returncode == 0 else None


def listdir(branch, path):
    out = show(branch, path)
    return [] if out is None else [ln.rstrip("/") for ln in out.splitlines()[2:] if ln]


def front_matter(readme):
    m = re.match(r"---\n(.*?)\n---", readme, re.S)
    fm = {}
    for ln in m.group(1).splitlines():
        k, _, v = ln.partition(":")
        if _ and not ln.startswith(" "):
            fm[k.strip()] = v.strip().strip('"')
    return fm


def rows():
    for b in BRANCHES:
        for d in sorted(listdir(b, "results/experiments")):
            if not re.match(r"\d{3}-", d):
                continue
            base = f"results/experiments/{d}"
            fm = front_matter(show(b, f"{base}/README.md"))
            res = show(b, f"{base}/results.json")
            verdict = show(b, f"{base}/verdict.json")
            r = json.loads(res) if res else {}
            v = json.loads(verdict) if verdict else {}
            row = {
                "campaign": b,
                "number": d[:3],
                "slug": d[4:],
                "weight": fm.get("weight"),
                "verdict": fm.get("verdict"),
                "title": fm.get("title"),
            }
            if "delta" in r:  # supervised: paired A/B
                bl, tr = r["arms"]["baseline"], r["arms"]["treatment"]
                row.update(
                    instrument=f"paired A/B, seeds {r['seeds'][0]}-{r['seeds'][-1]}, 95 % t-interval",
                    seeds=f"{r['seeds'][0]}-{r['seeds'][-1]}",
                    baseline=bl["mean_score"],
                    reading=tr["mean_score"],
                    delta=r["delta"],
                    resolution=f"[{r['ci_low']:+.2f}, {r['ci_high']:+.2f}]",
                    per_seed=" ".join(f"{x['mean_score']:.2f}" for x in tr["runs"]),
                )
            elif "block_means" in r:  # autonomous: calibration by disjoint 3-seed blocks
                row.update(
                    instrument="calibration: range of five 3-seed block means, seeds 0-14",
                    seeds="0-14",
                    baseline=r["baseline"],
                    reading=r["baseline"],
                    delta="",
                    resolution=f"floor {r['noise_floor']} (block std {r['block_std']}, per-seed std {r['per_seed_std']})",
                    per_seed=" ".join(f"{x:.2f}" for x in r["per_seed"]),
                )
            elif "runs" in r:
                seeds = f"{r['seeds'][0]}-{r['seeds'][-1]}"
                n = r["n_seeds"]
                if "improvement" in v:  # an iteration judged against the floor in force
                    row.update(
                        instrument=f"{n}-seed mean vs best kept, floor from calibration",
                        baseline=v["baseline"],
                        delta=round(v["improvement"], 2),
                        resolution=f"floor {v['noise_floor']} ({v['calibration'][:3]})",
                    )
                else:  # a calibration read as the single-seed range on fixed seeds
                    row.update(
                        instrument=f"calibration: single-seed range over seeds {seeds} (fixed)",
                        baseline=r["mean_score"],
                        delta="",
                        resolution=f"single-seed range {r.get('noise_floor', r.get('seed_spread'))} (std {r['std']})",
                    )
                row.update(
                    seeds=seeds,
                    reading=r["mean_score"],
                    per_seed=" ".join(f"{x['mean_score']:.2f}" for x in r["runs"]),
                )
            else:
                row.update(instrument="never run", seeds="", baseline="", reading="", delta="", resolution="", per_seed="")
            yield row


def main():
    data = list(rows())
    fields = ["campaign", "number", "slug", "weight", "verdict", "instrument", "seeds",
              "baseline", "reading", "delta", "resolution", "per_seed", "title"]  # fmt: skip
    with (HERE / "experiments.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(data)
    print("| campaign | # | change | verdict | reading | Δ vs baseline | resolution | seeds | per seed |")
    print("|---|---|---|---|---|---|---|---|---|")
    for r in data:
        d = f"{r['delta']:+.2f}" if isinstance(r["delta"], float) else ""
        print(f"| {r['campaign']} | {r['number']} | {r['slug']} | {r['verdict']} | {r['reading']} | {d} | {r['resolution']} | {r['seeds']} | {r['per_seed']} |")
    print(f"\n{len(data)} experiments -> {HERE / 'experiments.csv'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
