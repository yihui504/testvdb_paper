"""Control arm, part 2: where (if anywhere) does the four-perspective
organisation still earn its keep?

Primary result (script 89): a flat judge bound by the same fixed aggregation
rule matches the full stage exactly on convention recall (0.765 = 0.765,
McNemar p=0.61) and on forced-verdict recall (0.529 = 0.529). So the recall the
paper attributes to "structure" is the aggregation rule's.

This script prices the remaining contrasts: the false-positive side, and the
precision of the routed queue (does the full stage, when it declines to decide,
decline better?).
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
FULL_OVR = ["milvus_004", "milvus_006", "milvus_018", "milvus_019",
            "milvus_021", "milvus_027", "qdrant_017"]
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
        v = load(sorted(glob.glob(os.path.join(V3, f"{prefix}{r}",
                                               "verdicts_batch*.jsonl"))))
        if override:
            q = os.path.join(V3, f"{prefix}{r}", override)
            if os.path.exists(q):
                v.update(load([q]))
        out.append(v)
    return out


def mc(b, c):
    n = b + c
    return 1.0 if n == 0 else min(
        1.0, 2 * sum(math.comb(n, k) for k in range(0, min(b, c) + 1)) / 2 ** n)


def fisher(a, b, c, d):
    """two-sided Fisher exact on [[a,b],[c,d]]"""
    n = a + b + c + d
    r1, c1 = a + b, a + c

    def p(x):
        return (math.comb(r1, x) * math.comb(n - r1, c1 - x)
                / math.comb(n, c1))
    obs = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, c1 - (n - r1)),
                                             min(r1, c1) + 1)
                        if p(x) <= obs + 1e-12))


full = arm("run_full", "verdicts_coganchor_rejudge.jsonl")
flat = arm("run_flat", "verdicts_rejudge_cog.jsonl")
agg = arm("run_flatagg")


def maj(runs):
    return {c: sum(IS_C(runs[r][c]) for r in range(3)) >= 2 for c in CASES}


M = {"full": maj(full), "flat": maj(flat), "flat+agg": maj(agg)}

print("=== per-run rows for the new arm (convention) ===")
for r in range(3):
    tp = sum(IS_C(agg[r][c]) and GT[c] == "T" for c in CASES)
    fp = sum(IS_C(agg[r][c]) and GT[c] == "F" for c in CASES)
    fn = sum((not IS_C(agg[r][c])) and GT[c] == "T" for c in CASES)
    tn = sum((not IS_C(agg[r][c])) and GT[c] == "F" for c in CASES)
    print(f"  flat+agg, run {r+1} & {tp} & {fp} & {fn} & {tn} \\\\")

print("\n=== false-positive side, majority (candidates: 30 FP) ===")
for a, b in (("full", "flat"), ("full", "flat+agg"), ("flat+agg", "flat")):
    x = sum(1 for c in CASES if GT[c] == "F" and M[a][c] and not M[b][c])
    y = sum(1 for c in CASES if GT[c] == "F" and M[b][c] and not M[a][c])
    print(f"  {a} vs {b}: leaks discordant {x}/{y}  net {x-y:+d}  "
          f"exact McNemar p={mc(x, y):.4f}")

print("\n=== routed queue: does the structured arm decline better? ===")
q = {}
for name, runs in (("full", full), ("flat", flat), ("flat+agg", agg)):
    sel = [c for c in CASES if M[name][c]
           and any(runs[r][c] == "HUMAN_REVIEW" for r in range(3))]
    tp = sum(1 for c in sel if GT[c] == "T")
    q[name] = (tp, len(sel) - tp)
    print(f"  {name:9s}: queue={len(sel)}  TP={tp}  FP={len(sel)-tp}  "
          f"precision={tp/len(sel):.3f}")

a, b = q["full"]
c, d = q["flat+agg"]
print(f"\n  full vs flat+agg queue precision, Fisher exact: "
      f"[[{a},{b}],[{c},{d}]] p={fisher(a, b, c, d):.4f}")
a, b = q["full"]
c, d = q["flat"]
print(f"  full vs flat      queue precision, Fisher exact: "
      f"[[{a},{b}],[{c},{d}]] p={fisher(a, b, c, d):.4f}")

print("\n=== suppression, majority ===")
for name in ("full", "flat", "flat+agg"):
    tn = sum(1 for c in CASES if GT[c] == "F" and not M[name][c])
    tp = sum(1 for c in CASES if GT[c] == "T" and M[name][c])
    fp = sum(1 for c in CASES if GT[c] == "F" and M[name][c])
    print(f"  {name:9s}: recall {tp/51:.3f} ({tp}/51)  "
          f"suppression {tn/30:.3f} ({tn}/30)  precision {tp/(tp+fp):.3f}")
