"""Control arm (doc 3-#1): the flat judge bound by the full stage's fixed
aggregation rule. One variable changed vs the flat arm -- the discretionary
"judge however you see fit" becomes a fixed aggregation whose default is
HUMAN_REVIEW. Everything else (packs, source clones, red lines, verdict space)
is byte-identical.

Question it settles: is the full stage's advantage over the flat judge carried
by the four-perspective organisation, or by the aggregation rule alone?
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


def matrix(runs, conv=True):
    f = IS_C if conv else (lambda v: v == "CONFIRMED")
    maj = {c: sum(f(runs[r][c]) for r in range(3)) >= 2 for c in CASES}
    tp = sum(maj[c] and GT[c] == "T" for c in CASES)
    fp = sum(maj[c] and GT[c] == "F" for c in CASES)
    fn = sum((not maj[c]) and GT[c] == "T" for c in CASES)
    tn = sum((not maj[c]) and GT[c] == "F" for c in CASES)
    return maj, tp, fp, fn, tn


agg = arm("run_flatagg")
if agg is None or any(len(r) != 81 for r in agg):
    have = [len(r) for r in agg] if agg else None
    raise SystemExit(f"control arm incomplete: {have}")

full = arm("run_full", "verdicts_coganchor_rejudge.jsonl")
flat = arm("run_flat", "verdicts_rejudge_cog.jsonl")

print("=== control arm (flat + fixed aggregation) ===")
for r in range(3):
    conf = sum(IS_C(agg[r][c]) for c in CASES)
    hr = sum(agg[r][c] == "HUMAN_REVIEW" for c in CASES)
    print(f"  run{r+1}: confirmed={conf}  HR={hr} ({hr/81:.1%})  "
          f"C={sum(agg[r][c]=='CONFIRMED' for c in CASES)}")

maj_a, tp, fp, fn, tn = matrix(agg)
print(f"\n  majority: TP={tp} FPleak={fp} FN={fn} TN={tn}")
print(f"    recall      {tp/51:.3f} {wilson(tp, 51)}")
print(f"    suppression {tn/30:.3f} {wilson(tn, 30)}")
print(f"    precision   {tp/(tp+fp):.3f}")

maj_f, ftp, ffp, ffn, ftn = matrix(full)
maj_l, ltp, lfp, lfn, ltn = matrix(flat)


def routed(runs, maj):
    return sum(1 for c in CASES if maj[c]
               and any(runs[r][c] == "HUMAN_REVIEW" for r in range(3)))


for name, runs, maj, t in (("full", full, maj_f, ftp),
                           ("flat", flat, maj_l, ltp),
                           ("flat+agg", agg, maj_a, tp)):
    n = routed(runs, maj)
    tp_r = sum(1 for c in CASES if maj[c] and GT[c] == "T"
               and any(runs[r][c] == "HUMAN_REVIEW" for r in range(3)))
    tot = sum(sum(runs[r][c] == "HUMAN_REVIEW" for r in range(3))
              for c in CASES)
    print(f"\n  [{name}] majority-confirmed={sum(maj.values())}  "
          f"routed queue={n} (TP={tp_r}, FP={n-tp_r})  "
          f"queue precision={tp_r/n:.3f}  pooled HR={tot}/243={tot/243:.1%}")

print("\n=== paired exact McNemar on the confirmed set (majority, convention) ===")
for a, b, na, nb in ((maj_a, maj_l, "flat+agg", "flat"),
                     (maj_a, maj_f, "flat+agg", "full"),
                     (maj_f, maj_l, "full", "flat")):
    x = sum(1 for c in CASES if a[c] and not b[c])
    y = sum(1 for c in CASES if b[c] and not a[c])
    print(f"  {na} vs {nb}: discordant {x}/{y}  net {x-y:+d}  "
          f"exact McNemar p={mc(x, y):.4f}")

print("\n=== forced-verdict only (Human-Review NOT counted) ===")
for name, runs in (("full", full), ("flat", flat), ("flat+agg", agg)):
    _, t, _, _, _ = matrix(runs, conv=False)
    print(f"  {name}: recall {t/51:.3f} ({t}/51)")
