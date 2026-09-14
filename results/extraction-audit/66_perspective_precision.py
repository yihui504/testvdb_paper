"""Problem 4A: per-perspective precision cross-tabulation (R2 3.8). For the
full stage's 39 majority confirmations, which perspective drove each, and what
is each perspective's precision (TP vs FP)? Also: what did each perspective do
on the 12 misses and the 21 non-confirmations of false positives?"""
import glob
import json
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))


def load(run):
    d = {}
    for f in sorted(glob.glob(f"{ROOT}/rerun_v3/{run}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            o = json.loads(l)
            if o.get("defect_id"):
                d[o["defect_id"]] = o
    return d


def is_c(v):
    return v in ("CONFIRMED", "HUMAN_REVIEW")


runs = [load(f"run_full{k}") for k in (1, 2, 3)]
for r in range(3):
    p = f"{ROOT}/rerun_v3/run_full{r + 1}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES_FULL:
            runs[r][o["defect_id"]] = o

maj = {i: sum(is_c(runs[r][i]["verdict"]) for r in range(3)) >= 2
       for i in GT}


def persp_votes(i, key):
    """How many runs record a defect-side vote for perspective `key`.
    A/B vote by CONFIRMED; the cognition field (COG/D) votes defect-side via
    SUPPORTS_DEFECT."""
    n = 0
    for r in range(3):
        p = runs[r][i].get("perspectives") or {}
        for k, val in p.items():
            u = str(val).upper()
            if k in ("A", "B") and k == key and u.startswith("CONF"):
                n += 1
            if k in ("COG", "D") and key in ("COG", "D") \
                    and "SUPPORTS_DEFECT" in u:
                n += 1
    return n


def driver(i):
    """Driving perspective of a majority confirmation (paper's taxonomy):
    A if contract confirms in >=2 runs; else B if objective confirms >=2;
    else D if cognition supports in >=2; else none."""
    for key in ("A", "B", "COG", "D"):
        if persp_votes(i, key) >= 2:
            return key
    return "none"


# normalize: some verdict files use 'COG' and some 'D' for cognition
def driver_norm(i):
    d = driver(i)
    return "cognition" if d in ("COG", "D") else d


tab = defaultdict(Counter)
for i in sorted(GT):
    if maj[i]:
        tab[driver_norm(i)][GT[i]] += 1

print("== driving perspective x ground truth, 39 majority confirmations ==")
tot = Counter()
for d in ("A", "B", "cognition", "none"):
    tp, fp = tab[d]["T"], tab[d]["F"]
    n = tp + fp
    tot["tp"] += tp
    tot["fp"] += fp
    prec = tp / n if n else float("nan")
    print(f"  {d:10s} n={n:2d}  TP {tp:2d}  FP {fp}  precision {prec:.3f}")
print(f"  {'total':10s} n={tot['tp'] + tot['fp']}  TP {tot['tp']}  "
      f"FP {tot['fp']}")

print("\n== the 12 misses: any perspective voting defect-side? ==")
for i in sorted(i for i in GT if GT[i] == "T" and not maj[i]):
    votes = {k: persp_votes(i, k) for k in ("A", "B", "COG", "D")}
    print(f"  {i:14s} {votes}")

print("\n== the 21 correctly-rejected false positives: any perspective "
      "voting defect-side? ==")
for i in sorted(i for i in GT if GT[i] == "F" and not maj[i]):
    votes = {k: persp_votes(i, k) for k in ("A", "B", "COG", "D")}
    flag = "  <-- B voted defect-side" if votes["B"] else ""
    print(f"  {i:14s} {votes}{flag}")

print("\n== identity of the FP leaks by driving perspective ==")
for i in sorted(i for i in GT if GT[i] == "F" and maj[i]):
    print(f"  {i:14s} driver={driver_norm(i)}")
