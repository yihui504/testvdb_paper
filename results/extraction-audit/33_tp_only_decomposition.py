"""Round-13 sensitivity: decompose the flagship full-vs-flat confirmed-set net
into its ground-truth components (true-positive flips vs false-positive leak
flips) and run component-wise exact McNemar tests on both backbones."""
import glob
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
        "arms/rq2_3run")
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


def majority(runs):
    ids = sorted(set.intersection(*(set(r) for r in runs)))
    return {i: sum(is_c(r[i]) for r in runs) >= 2 for i in ids}


Ts = sorted(i for i in GT if GT[i] == "T")
Fs = sorted(i for i in GT if GT[i] == "F")

for label, fb, ab in (("primary (GLM)", "rerun_v3", "rerun_v3"),):
    full = majority([load(fb, f"run_full{k}") for k in (1, 2, 3)])
    flat = majority([load(ab, f"run_flat{k}") for k in (1, 2, 3)])
    b = sum(1 for i in Ts if full[i] and not flat[i])
    c = sum(1 for i in Ts if flat[i] and not full[i])
    bf = sum(1 for i in Fs if full[i] and not flat[i])
    cf = sum(1 for i in Fs if flat[i] and not full[i])
    print(f"{label}")
    print(f"  true-positive flips: {b}/{c}  exact McNemar p={mc(b, c):.4f}")
    print(f"  leak flips:          {bf}/{cf}  exact McNemar p={mc(bf, cf):.4f}")
    print(f"  net {b-c}+{bf-cf} = {(b-c)+(bf-cf)} "
          f"(flagship confirmed-set net 47-34 = 13)")

qf = majority([load("rerun_v3", f"run_fullq{k}") for k in (1, 2, 3)])
qa = majority([load("rerun_v3", f"run_flatq{k}") for k in (1, 2, 3)])
qb = sum(1 for i in Ts if qf[i] and not qa[i])
qc = sum(1 for i in Ts if qa[i] and not qf[i])
print(f"second family (Qwen)")
print(f"  true-positive flips: {qb}/{qc}  exact McNemar p={mc(qb, qc):.4f}")
