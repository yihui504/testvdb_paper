"""Qwen full/flat three-run final aggregation: majorities, same-family McNemar,
forced-only sensitivity, agreement."""
import glob
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
        "arms/rq2_3run")
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
                d[o["defect_id"]] = o.get("verdict")
    return d


def is_c(v):
    return v in ("CONFIRMED", "HUMAN_REVIEW")


def mc(b, c):
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, k)
                            for k in range(0, min(b, c) + 1)) / 2 ** n)


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0, c - h), min(1, c + h))


def majority(runs, forced=False):
    ids = sorted(set.intersection(*(set(r) for r in runs)))
    return {i: ("CONFIRMED" if sum((r[i] == "CONFIRMED") if forced
                                   else is_c(r[i]) for r in runs) >= 2
                else "FALSE_POSITIVE") for i in ids}


def arm_line(name, d):
    tp = sum(1 for i in d if d[i] == "CONFIRMED" and GT[i] == "T")
    fp = sum(1 for i in d if d[i] == "CONFIRMED" and GT[i] == "F")
    rlo, rhi = wilson(tp, 51)
    print(f"{name}: TP {tp} FP {fp} recall {tp/51:.3f} [{rlo:.3f},{rhi:.3f}]"
          f" supp {(30-fp)/30:.3f} prec {tp/(tp+fp):.3f} conf-total {tp+fp}")
    return d


full_runs = [load(f"run_fullq{i}") for i in (1, 2, 3)]
flat_runs = [load(f"run_flatq{i}") for i in (1, 2, 3)]
for i, r in enumerate(full_runs, 1):
    n_c = sum(1 for v in r.values() if is_c(v))
    n_hr = sum(1 for v in r.values() if v == "HUMAN_REVIEW")
    print(f"fullq{i}: confirmed {n_c}/81 (HR {n_hr})")
for i, r in enumerate(flat_runs, 1):
    n_c = sum(1 for v in r.values() if is_c(v))
    n_hr = sum(1 for v in r.values() if v == "HUMAN_REVIEW")
    print(f"flatq{i}: confirmed {n_c}/81 (HR {n_hr})")

fm = arm_line("fullq majority", majority(full_runs))
am = arm_line("flatq majority", majority(flat_runs))
b = sum(1 for i in fm if fm[i] == "CONFIRMED" and am[i] != "CONFIRMED")
c = sum(1 for i in fm if fm[i] != "CONFIRMED" and am[i] == "CONFIRMED")
print(f"fullq-vs-flatq (HR-counted): discordant {b}/{c} p={mc(b,c):.4f}")

fmf = majority(full_runs, True)
amf = majority(flat_runs, True)
ftp = sum(1 for i in fmf if fmf[i] == "CONFIRMED" and GT[i] == "T")
atp = sum(1 for i in amf if amf[i] == "CONFIRMED" and GT[i] == "T")
bf = sum(1 for i in fmf if fmf[i] == "CONFIRMED" and amf[i] != "CONFIRMED")
cf = sum(1 for i in fmf if fmf[i] != "CONFIRMED" and amf[i] == "CONFIRMED")
print(f"forced-only: fullq {ftp}/51={ftp/51:.3f} flatq {atp}/51={atp/51:.3f}"
      f" discordant {bf}/{cf} p={mc(bf,cf):.4f}")

for nm, rs in (("fullq", full_runs), ("flatq", flat_runs)):
    ids = sorted(set.intersection(*(set(r) for r in rs)))
    same = sum(1 for i in ids if len({r[i] for r in rs}) == 1)
    print(f"{nm} 3-run agreement {same}/{len(ids)} = {same/len(ids):.3f}")

# GLM flat-vs-Qwen arms for the cross-family reference the paper cites
glm_flat = majority([load(f"run_flat{i}") for i in (1, 2, 3)])
b2 = sum(1 for i in fm if fm[i] == "CONFIRMED" and glm_flat[i] != "CONFIRMED")
c2 = sum(1 for i in fm if fm[i] != "CONFIRMED" and glm_flat[i] == "CONFIRMED")
print(f"fullq(GLM-majority-cross)-vs-flat: {b2}/{c2} p={mc(b2,c2):.4f}")
