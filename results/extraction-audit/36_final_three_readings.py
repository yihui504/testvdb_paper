"""Final three-reading aggregation on the cognition-anchor-cleaned GLM pool
(7 rejudged cases merged; Qwen side pending its own session)."""
import glob
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
         "milvus_021", "milvus_027", "qdrant_017"}
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))
ADJ_CONFIRM = {"milvus_005", "milvus_013", "milvus_036", "milvus_038",
               "milvus_043", "qdrant_014", "qdrant_015", "qdrant_016",
               "qdrant_027"}


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


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    ctr = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return max(0.0, ctr - h), min(1.0, ctr + h)


full = [load("rerun_v3", f"run_full{k}") for k in (1, 2, 3)]
flat = [load("rerun_v3", f"run_flat{k}") for k in (1, 2, 3)]
for r in range(3):
    p = f"{ROOT}/rerun_v3/run_full{r + 1}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES:
            full[r][o["defect_id"]] = o["verdict"]

nm = {i: sum(is_c(full[r][i]) for r in range(3)) >= 2 for i in GT}
fm = {i: sum(is_c(flat[r][i]) for r in range(3)) >= 2 for i in GT}
forced = {i: sum(full[r][i] == "CONFIRMED" for r in range(3)) >= 2
          for i in GT}
routed = {i for i in GT if nm[i]
          and any(full[r][i] == "HUMAN_REVIEW" for r in range(3))}
joint = {}
for i in GT:
    if not nm[i]:
        joint[i] = "FP"
    elif i in routed:
        joint[i] = "C" if i in ADJ_CONFIRM else "FP"
    else:
        joint[i] = "C"


def line(name, conf):
    def yes(i):
        v = conf[i]
        return v is True or v == "C"
    tp = sum(1 for i in GT if yes(i) and GT[i] == "T")
    fp = sum(1 for i in GT if yes(i) and GT[i] == "F")
    rlo, rhi = wilson(tp, 51)
    slo, shi = wilson(30 - fp, 30)
    print(f"{name:14s} TP {tp:2d} FP {fp}  recall {tp}/51={tp / 51:.3f} "
          f"[{rlo:.3f},{rhi:.3f}]  supp {30 - fp}/30={(30 - fp) / 30:.3f} "
          f"[{slo:.3f},{shi:.3f}]  prec {tp}/{tp + fp}={tp / (tp + fp):.3f}")


line("NEW convention", nm)
line("NEW forced", forced)
line("NEW joint", joint)

b = sum(1 for i in GT if joint[i] == "C" and not fm[i])
c = sum(1 for i in GT if fm[i] and joint[i] != "C")
print(f"joint-vs-flat: discordant {b}/{c} p={mc(b, c):.4f}")
b = sum(1 for i in GT if nm[i] and not fm[i])
c = sum(1 for i in GT if fm[i] and not nm[i])
print(f"convention-vs-flat: discordant {b}/{c} p={mc(b, c):.4f}")
ft = {i: full[r][i] == "CONFIRMED" for i in GT}
ff = {i: sum(flat[r][i] == "CONFIRMED" for r in range(3)) >= 2 for i in GT}
tpo_b = sum(1 for i in GT if ft[i] and not ff[i] and GT[i] == "T")
tpo_c = sum(1 for i in GT if ff[i] and not ft[i] and GT[i] == "T")
print(f"TP-only: {tpo_b}/{tpo_c} p={mc(tpo_b, tpo_c):.4f}")
fpo_b = sum(1 for i in GT if ft[i] and not ff[i] and GT[i] == "F")
fpo_c = sum(1 for i in GT if ff[i] and not ft[i] and GT[i] == "F")
print(f"leak-only: {fpo_b}/{fpo_c} p={mc(fpo_b, fpo_c):.4f}")
hr = sum(1 for r in range(3) for i in GT if full[r][i] == "HUMAN_REVIEW")
print(f"full HR routed verdicts: {hr}/243 = {hr / 243:.3f}")
