#!/usr/bin/env python3
"""Phase 2 N-round aggregator (threat-3 mitigation: judge variance).

Takes N independent GLM verdict files (each a full pass over the cleaned
prompt set), computes per-candidate majority verdict, per-round metrics, and
the mean +/- spread across rounds. Also lists candidates whose verdict flipped
between rounds (the judge-variance signal).

GT source: metrics.json rows (vendor/number/gt/group) — only gt/group are read;
verdicts come entirely from the round files so old and new runs are comparable.

Verdict files: each is a list of {"vendor","number","verdict","rationale"},
same shape as glm_verdicts.json. Name them glm_verdicts_round{k}.json.

Usage:
  py aggregate_rounds.py --gt metrics.json \\
     --rounds "glm_verdicts_round*.json" --out rounds_report.json
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent


def load_gt(path: str) -> dict:
    """{(vendor,num): (gt, group)} from metrics.json rows."""
    rows = json.load(open(path, encoding="utf-8"))["rows"]
    return {(r["vendor"], r["number"]): (r["gt"], r["group"]) for r in rows}


def load_round(path: str) -> dict:
    """{(vendor,num): verdict} from one round's verdict list."""
    out = {}
    for e in json.load(open(path, encoding="utf-8")):
        v = e.get("verdict")
        if v:
            out[(e["vendor"], e["number"])] = v
    return out


def metrics_for(verdicts: dict, gt: dict) -> dict:
    """recall (A∪B), precision (scored A∪B∪C), FP-suppression (C)."""
    ab_total = ab_conf = c_total = c_fp = abc_conf = 0
    for key, (gcat, group) in gt.items():
        if group in ("A", "B"):
            ab_total += 1
            if verdicts.get(key) == "CONFIRMED":
                ab_conf += 1
        elif group == "C":
            c_total += 1
            if verdicts.get(key) == "FALSE_POSITIVE":
                c_fp += 1
            if verdicts.get(key) == "CONFIRMED":
                abc_conf += 1
        # A,B CONFIRMED also count toward abc_conf (precision denominator)
    # recount abc_conf including A/B confirmed
    abc_conf = sum(1 for k, (g, grp) in gt.items() if grp in ("A", "B", "C")
                   and verdicts.get(k) == "CONFIRMED")
    ab_confirmed = sum(1 for k, (g, grp) in gt.items() if grp in ("A", "B")
                       and verdicts.get(k) == "CONFIRMED")
    recall = ab_confirmed / ab_total if ab_total else 0.0
    precision = ab_confirmed / abc_conf if abc_conf else 0.0
    fp_supp = c_fp / c_total if c_total else 0.0
    return {"recall": recall, "precision": precision, "fp_supp": fp_supp,
            "ab_confirmed": ab_confirmed, "ab_total": ab_total,
            "abc_confirmed": abc_conf, "c_fp": c_fp, "c_total": c_total}


def majority(verdicts_list):
    """Majority across rounds; tie -> FALSE_POSITIVE (conservative), flagged."""
    c = Counter(v for v in verdicts_list if v)
    if not c:
        return None, False
    top = c.most_common()
    if len(top) > 1 and top[0][1] == top[1][1]:
        return "FALSE_POSITIVE", True  # tie
    return top[0][0], False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gt", default=str(ROOT / "metrics.json"))
    ap.add_argument("--rounds", required=True,
                    help="glob or comma-separated list of round verdict json files")
    ap.add_argument("--out", default=str(ROOT / "rounds_report.json"))
    args = ap.parse_args()

    if "," in args.rounds:
        files = [f.strip() for f in args.rounds.split(",")]
    else:
        files = sorted(glob.glob(args.rounds))
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        print("no round files matched", file=sys.stderr)
        return 1

    gt = load_gt(args.gt)
    rounds = {os.path.basename(f): load_round(f) for f in files}
    N = len(rounds)

    # per-round metrics
    per_round = {name: metrics_for(vd, gt) for name, vd in rounds.items()}

    # majority verdict per candidate
    maj = {}
    ties = []
    per_cand = defaultdict(list)
    for key in gt:
        for name, vd in rounds.items():
            per_cand[key].append(vd.get(key))
        m, tie = majority(per_cand[key])
        maj[key] = m
        if tie:
            ties.append(key)
    maj_metrics = metrics_for(maj, gt)

    # flippers (verdict changed across rounds)
    flippers = []
    for key, vs in per_cand.items():
        distinct = {v for v in vs if v}
        if len(distinct) > 1:
            v, g, grp = key[0], key[1], gt[key][0]
            flippers.append({"vendor": v, "number": g, "gt": grp,
                             "group": gt[key][1], "verdicts": vs})

    # mean +/- std across rounds
    def spread(metric_key):
        vals = [m[metric_key] for m in per_round.values()]
        mean = sum(vals) / len(vals)
        sd = math.sqrt(sum((x - mean) ** 2 for x in vals) / len(vals)) if len(vals) > 1 else 0.0
        return {"mean": mean, "std": sd, "min": min(vals), "max": max(vals), "values": vals}

    report = {
        "n_rounds": N,
        "round_files": list(rounds.keys()),
        "per_round_metrics": per_round,
        "majority_metrics": maj_metrics,
        "recall_spread": spread("recall"),
        "precision_spread": spread("precision"),
        "fp_supp_spread": spread("fp_supp"),
        "ties": [{"vendor": v, "number": n} for (v, n) in ties],
        "flippers": flippers,
        "n_flippers": len(flippers),
    }
    json.dump(report, open(args.out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print(f"N={N} rounds")
    print(f"majority: recall={maj_metrics['recall']:.3f} "
          f"precision={maj_metrics['precision']:.3f} "
          f"fp_supp={maj_metrics['fp_supp']:.3f}")
    for k in ("recall", "precision", "fp_supp"):
        s = report[f"{k}_spread"]
        print(f"  {k}: mean={s['mean']:.3f} std={s['std']:.3f} "
              f"[{s['min']:.3f}, {s['max']:.3f}]")
    print(f"flippers (verdict changed across rounds): {len(flippers)}")
    print(f"ties (split vote -> conservative FP): {len(ties)}")
    print(f"-> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
