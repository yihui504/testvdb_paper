"""The completed 2x2, plus the source-withheld arm.

                        no aggregation          fixed aggregation
  flat (no perspectives)   flat judge            flat + aggregation
  four perspectives        full, no aggregation  full stage

`full, no aggregation` is the cell the paper was missing, which is why
"the advantage belongs to the routing rule rather than to the four
perspectives" outranks what the three-arm design could support. With the cell
filled, the perspectives' own contribution is readable as the within-row
difference under each aggregation condition.
"""
import glob
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
V3 = os.path.join(ROOT, "rerun_v3")
GT = json.load(open(os.path.join(ROOT, "gt_81.json"), encoding="utf-8"))
CASES = sorted(GT)
IS_C = lambda v: v in ("CONFIRMED", "HUMAN_REVIEW")

ARMS = [
    ("flat judge", "run_flat", "verdicts_rejudge_cog.jsonl"),
    ("flat + aggregation", "run_flatagg", None),
    ("full, no aggregation", "run_noscopic",
     "verdicts_coganchor_rejudge.jsonl"),
    ("full stage", "run_full", "verdicts_coganchor_rejudge.jsonl"),
    ("full, no source", "run_fullnosrc",
     "verdicts_coganchor_rejudge.jsonl"),
]


def load(paths):
    v = {}
    for f in paths:
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                o = json.loads(line)
                v[o["defect_id"]] = o["verdict"]
    return v


def arm(prefix, override):
    out = []
    for r in (1, 2, 3):
        p = sorted(glob.glob(os.path.join(V3, f"{prefix}{r}",
                                          "verdicts_batch*.jsonl")))
        if not p:
            return None
        v = load(p)
        if override:
            q = os.path.join(V3, f"{prefix}{r}", override)
            if os.path.exists(q):
                v.update(load([q]))
        if len(v) != 81:
            return None
        out.append(v)
    return out


def wilson(k, n, z=1.959964):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 3), round(min(1.0, c + h), 3))


def mcnemar(b, c):
    n = b + c
    return 1.0 if n == 0 else min(
        1.0, 2 * sum(math.comb(n, k) for k in range(0, min(b, c) + 1)) / 2 ** n)


loaded, M = {}, {}
print("=== per-run (convention) ===")
for name, prefix, ovr in ARMS:
    runs = arm(prefix, ovr)
    if runs is None:
        print(f"  {name:22s} [incomplete]")
        continue
    loaded[name] = runs
    cells, hrs = [], []
    for r in range(3):
        tp = sum(IS_C(runs[r][c]) and GT[c] == "T" for c in CASES)
        fp = sum(IS_C(runs[r][c]) and GT[c] == "F" for c in CASES)
        cells.append(f"{tp}+{fp}")
        hrs.append(sum(runs[r][c] == "HUMAN_REVIEW" for c in CASES))
    print(f"  {name:22s} {cells[0]:>9s} {cells[1]:>9s} {cells[2]:>9s}   "
          f"HR {sum(hrs) / 243:.1%}")

print("\n=== majority ===")
for name in loaded:
    runs = loaded[name]
    maj = {c: sum(IS_C(runs[r][c]) for r in range(3)) >= 2 for c in CASES}
    M[name] = maj
    tp = sum(maj[c] and GT[c] == "T" for c in CASES)
    fp = sum(maj[c] and GT[c] == "F" for c in CASES)
    tn = sum((not maj[c]) and GT[c] == "F" for c in CASES)
    forced = sum(GT[c] == "T" and sum(runs[r][c] == "CONFIRMED"
                                      for r in range(3)) >= 2 for c in CASES)
    print(f"  {name:22s} recall {tp}/51 {tp / 51:.3f} {wilson(tp, 51)}  "
          f"supp {tn}/30 {tn / 30:.3f}  prec {tp / (tp + fp):.3f}  "
          f"forced {forced}/51")

print("\n=== paired exact McNemar (confirmed set, convention) ===")
for a, b in (("full, no aggregation", "full stage"),
             ("full, no aggregation", "flat + aggregation"),
             ("full, no aggregation", "flat judge"),
             ("full stage", "flat + aggregation"),
             ("flat + aggregation", "flat judge"),
             ("full, no source", "full stage")):
    if a not in M or b not in M:
        continue
    x = sum(1 for c in CASES if M[a][c] and not M[b][c])
    y = sum(1 for c in CASES if M[b][c] and not M[a][c])
    print(f"  {a:22s} vs {b:22s}: discordant {x}/{y}  net {x - y:+d}  "
          f"p={mcnemar(x, y):.4f}")
