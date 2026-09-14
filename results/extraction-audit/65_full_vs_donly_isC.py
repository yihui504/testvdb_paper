"""Recompute the full-vs-source-only comparison under the is-C unit (the unit
the paper's numbers actually use) and decompose the discordant cases."""
import glob
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))


def load(base, run):
    d = {}
    for f in sorted(glob.glob(f"{ROOT}/{base}/{run}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            o = json.loads(l)
            if o.get("defect_id"):
                d[o["defect_id"]] = o["verdict"]
    return d


def is_c(v):
    return v in ("CONFIRMED", "HUMAN_REVIEW")


def mc(b, c):
    n = b + c
    return 1.0 if n == 0 else min(
        1.0, 2 * sum(math.comb(n, k)
                     for k in range(0, min(b, c) + 1)) / 2 ** n)


full = [load("rerun_v3", f"run_full{k}") for k in (1, 2, 3)]
donly = [load("rerun_v3", f"run_donly{k}") for k in (1, 2, 3)]
for r in range(3):
    p = f"{ROOT}/rerun_v3/run_full{r + 1}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES_FULL:
            full[r][o["defect_id"]] = o["verdict"]

full_m = {i: sum(is_c(full[r][i]) for r in range(3)) >= 2 for i in GT}
donly_m = {i: sum(is_c(donly[r][i]) for r in range(3)) >= 2 for i in GT}

b = [i for i in sorted(GT) if full_m[i] and not donly_m[i]]
c = [i for i in sorted(GT) if donly_m[i] and not full_m[i]]
print(f"full {sum(full_m.values())} vs source-only {sum(donly_m.values())}")
print(f"discordant {len(b)}/{len(c)}  p={mc(len(b), len(c)):.4f}")

print("\n== full-only (is-C unit): is the full confirmation HR-carried? ==")
for i in b:
    fv = [full[r][i] for r in range(3)]
    dv = [donly[r][i] for r in range(3)]
    n_hr = sum(1 for v in fv if v == "HUMAN_REVIEW")
    n_c = sum(1 for v in fv if v == "CONFIRMED")
    # does source-only confirm on a forced majority at all?
    d_c = sum(1 for v in dv if v == "CONFIRMED")
    kind = ("HR-majority (routing-carried)"
            if n_hr >= 2 else f"forced majority {n_c}/3 + HR minority")
    print(f"  {i:14s} GT={GT[i]} full={fv} donly={dv}")
    print(f"      {kind}; source-only forced CONFIRMED count {d_c}/3")

print("\n== source-only-only ==")
for i in c:
    fv = [full[r][i] for r in range(3)]
    dv = [donly[r][i] for r in range(3)]
    print(f"  {i:14s} GT={GT[i]} full={fv} donly={dv}")

hr_kind = sum(1 for i in b
              if sum(1 for r in range(3)
                     if full[r][i] == "HUMAN_REVIEW") >= 2)
print(f"\nfull-only {len(b)} = HR-majority {hr_kind} + "
      f"forced-majority {len(b) - hr_kind}")
