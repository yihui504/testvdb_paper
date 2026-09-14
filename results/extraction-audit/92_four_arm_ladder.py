"""Four-arm ladder on the same 81 rebuilt packs, same materials, same source
clones, same discipline. The only deltas are the prompt-level rules:

  flat        : plain prompt, discretionary routing wording, no aggregation
  flatschema : flat + the output-schema enum corrected to three-valued
                (confound control: did fixing the field alone move anything?)
  flat+agg    : flat + a fixed aggregation whose default is HUMAN_REVIEW
  full        : four perspectives + chain sections + cognition + aggregation

Decision rule, fixed before the data landed: if flatschema lands near flat
(~0.588, TP ~30) the field fix is inert and the flat+agg attribution is clean;
if it lands near 0.765 (TP ~39) the flat+agg result is a confound and is
withdrawn.
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


def load(paths):
    v = {}
    for f in paths:
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                j = json.loads(line)
                v[j["defect_id"]] = j["verdict"]
    return v


def arm(prefix, override=None):
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
        out.append(v)
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0, c - h), 3), round(min(1, c + h), 3))


def mc(b, c):
    n = b + c
    return 1.0 if n == 0 else min(
        1.0, 2 * sum(math.comb(n, k) for k in range(0, min(b, c) + 1)) / 2 ** n)


ARMS = [("full", arm("run_full", "verdicts_coganchor_rejudge.jsonl")),
        ("flat", arm("run_flat", "verdicts_rejudge_cog.jsonl")),
        ("flatschema", arm("run_flatschema")),
        ("flat+agg", arm("run_flatagg"))]

M = {}
print("=== per-run, convention (CONFIRMED + HUMAN_REVIEW) ===")
print(f"  {'arm':11s} {'run1':>12s} {'run2':>12s} {'run3':>12s}   HR rate")
for name, runs in ARMS:
    if runs is None or any(len(r) != 81 for r in runs):
        print(f"  {name:11s} [incomplete: "
              f"{[len(r) for r in runs] if runs else 'no files'}]")
        continue
    cells, hrs = [], []
    for r in range(3):
        tp = sum(IS_C(runs[r][c]) and GT[c] == "T" for c in CASES)
        fp = sum(IS_C(runs[r][c]) and GT[c] == "F" for c in CASES)
        cells.append(f"{tp}+{fp}")
        hrs.append(sum(runs[r][c] == "HUMAN_REVIEW" for c in CASES))
    print(f"  {name:11s} {cells[0]:>12s} {cells[1]:>12s} {cells[2]:>12s}   "
          f"{sum(hrs)/243:.1%}")

print("\n=== majority (>=2/3) ===")
for name, runs in ARMS:
    if runs is None or any(len(r) != 81 for r in runs):
        continue
    maj = {c: sum(IS_C(runs[r][c]) for r in range(3)) >= 2 for c in CASES}
    M[name] = maj
    tp = sum(maj[c] and GT[c] == "T" for c in CASES)
    fp = sum(maj[c] and GT[c] == "F" for c in CASES)
    tn = sum((not maj[c]) and GT[c] == "F" for c in CASES)
    forced = sum(GT[c] == "T"
                 and sum(runs[r][c] == "CONFIRMED" for r in range(3)) >= 2
                 for c in CASES)
    print(f"  {name:11s}: recall {tp/51:.3f} {wilson(tp,51)}  "
          f"supp {tn/30:.3f}  prec {tp/(tp+fp):.3f}  "
          f"confirmed={tp+fp}  forced-recall {forced}/51")

print("\n=== the confound test ===")
if "flatschema" in M and "flat" in M and "flat+agg" in M:
    for a, b in (("flatschema", "flat"), ("flatschema", "flat+agg")):
        x = sum(1 for c in CASES if M[a][c] and not M[b][c])
        y = sum(1 for c in CASES if M[b][c] and not M[a][c])
        print(f"  {a} vs {b}: discordant {x}/{y}  net {x-y:+d}  "
              f"exact McNemar p={mc(x, y):.4f}")
    for a, b in (("flat+agg", "flat"), ("flat+agg", "full")):
        if a in M and b in M:
            x = sum(1 for c in CASES if M[a][c] and not M[b][c])
            y = sum(1 for c in CASES if M[b][c] and not M[a][c])
            print(f"  {a} vs {b}: discordant {x}/{y}  net {x-y:+d}  "
                  f"exact McNemar p={mc(x, y):.4f}")
