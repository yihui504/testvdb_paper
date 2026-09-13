"""Second-family numbers after the cognition-anchor rejudge: arm rates,
discordant pairs, and exact McNemar for fullq-vs-flatq (convention and
forced-only)."""
import glob
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
         "milvus_021", "milvus_027", "qdrant_017"}
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))


def load(run):
    """Load the frozen batch verdicts for a run (skip any non-JSON lines)."""
    d = {}
    for f in sorted(glob.glob(f"{ROOT}/rerun_v3/{run}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            try:
                o = json.loads(l)
            except json.JSONDecodeError:
                continue
            if o.get("defect_id"):
                d[o["defect_id"]] = o["verdict"]
    return d


def load_rej(run):
    d = load(run)
    p = f"{ROOT}/rerun_v3/{run}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES:
            d[o["defect_id"]] = o["verdict"]
    return d


def is_c(v):
    return v in ("CONFIRMED", "HUMAN_REVIEW")


def mc(b, c):
    n = b + c
    return 1.0 if n == 0 else min(
        1.0, 2 * sum(math.comb(n, k)
                     for k in range(0, min(b, c) + 1)) / 2 ** n)


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    ctr = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return max(0.0, ctr - h), min(1.0, ctr + h)


fq = [load_rej(f"run_fullq{k}") for k in (1, 2, 3)]
aq = [load(f"run_flatq{k}") for k in (1, 2, 3)]


def arm(name, runs, forced=False):
    ids = sorted(set.intersection(*(set(r) for r in runs)))
    conf = {i: sum((r[i] == "CONFIRMED") if forced else is_c(r[i])
                   for r in runs) >= 2 for i in ids}
    tp = sum(1 for i in ids if conf[i] and GT[i] == "T")
    fp = sum(1 for i in ids if conf[i] and GT[i] == "F")
    rlo, rhi = wilson(tp, 51)
    print(f"{name:22s} TP {tp:2d} FP {fp}  recall {tp}/51={tp / 51:.3f} "
          f"[{rlo:.3f},{rhi:.3f}]  supp {30 - fp}/30={(30 - fp) / 30:.3f}  "
          f"prec {tp}/{tp + fp}={tp / (tp + fp):.3f}")
    return conf


print("== second family, post-rejudge ==")
fc = arm("fullq convention", fq)
ac = arm("flatq convention", aq)
ff = arm("fullq forced", fq, forced=True)
af = arm("flatq forced", aq, forced=True)
b = sum(1 for i in GT if fc[i] and not ac[i])
c = sum(1 for i in GT if ac[i] and not fc[i])
print(f"discordant {b}/{c}  p={mc(b, c):.4f}")
b2 = sum(1 for i in GT if ff[i] and not af[i])
c2 = sum(1 for i in GT if af[i] and not ff[i])
print(f"forced-only discordant {b2}/{c2}  p={mc(b2, c2):.4f}")
# round-13 style cross-check: primary full vs flatq
full = [load(f"run_full{k}") for k in (1, 2, 3)]
for r in range(3):
    p = f"{ROOT}/rerun_v3/run_full{r + 1}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES:
            full[r][o["defect_id"]] = o["verdict"]
fm = {i: sum(is_c(full[r][i]) for r in range(3)) >= 2 for i in GT}
b3 = sum(1 for i in GT if fm[i] and not ac[i])
c3 = sum(1 for i in GT if ac[i] and not fm[i])
print(f"[cross] primary-full vs flatq: discordant {b3}/{c3} "
      f"p={mc(b3, c3):.4f}")
# agreement
ids = sorted(set.intersection(*(set(r) for r in fq)))
same = sum(1 for i in ids if len({fq[k][i] for k in range(3)}) == 1)
print(f"fullq 3-run agreement {same}/{len(ids)} = {same / len(ids):.3f}")


print("== routing and agreement ==")
for nm, runs in (("fullq", fq), ("flatq", aq)):
    hr = sum(1 for r in runs for v in r.values() if v == "HUMAN_REVIEW")
    ids = sorted(set.intersection(*(set(r) for r in runs)))
    same = sum(1 for i in ids if len({runs[k][i] for k in range(3)}) == 1)
    print(f"{nm}: HR {hr}/243 = {hr / 243:.3f}; agreement {same}/{len(ids)}"
          f" = {same / len(ids):.3f}")
