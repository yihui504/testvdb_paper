"""Phase A: symmetric joint reading for the flat arm.

Dispositions (pack-materials-only, same protocol as the full arm's worksheet):
  new adjudications (this session):
    milvus_001  T  REJECTED  no execution record + no verifiable contract
    milvus_010  T  UPHELD    same-family inconsistency: alter_properties rejects
                             the same -100 TTL with an explicit range message
                             ("expect [-1, 3155760000]"), create silently accepts
    milvus_033  T  UPHELD    behavioral row promises 400 on invalid parameters;
                             create returned 200 and substituted FloatVector
    weaviate_003 T UPHELD    pack assertion replicationConfig.factor >= 1
                             violated; response shows silent substitution to 1
    milvus_020  F  REJECTED  no contract row; stale read not in objective classes
  reused (identical protocol, already adjudicated):
    milvus_036 / milvus_038 / milvus_043 / qdrant_014  T  UPHELD (round-13)
    milvus_019 / milvus_027                            F  REJECTED (this session)
"""
import glob
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}
UPHELD_FLAT = {"milvus_010", "milvus_033", "weaviate_003",
               "milvus_036", "milvus_038", "milvus_043", "qdrant_014"}
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))
ADJ_CONFIRM_FULL = {"milvus_005", "milvus_013", "milvus_036", "milvus_038",
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
        if o.get("defect_id") in CASES_FULL:
            full[r][o["defect_id"]] = o["verdict"]

full_m = {i: sum(is_c(full[r][i]) for r in range(3)) >= 2 for i in GT}
flat_m = {i: sum(is_c(flat[r][i]) for r in range(3)) >= 2 for i in GT}
full_routed = {i for i in GT if full_m[i]
               and any(full[r][i] == "HUMAN_REVIEW" for r in range(3))}
flat_routed = {i for i in GT if flat_m[i]
               and any(flat[r][i] == "HUMAN_REVIEW" for r in range(3))}

full_joint = {}
for i in GT:
    if not full_m[i]:
        full_joint[i] = False
    elif i in full_routed:
        full_joint[i] = i in ADJ_CONFIRM_FULL
    else:
        full_joint[i] = True
flat_joint = {}
for i in GT:
    if not flat_m[i]:
        flat_joint[i] = False
    elif i in flat_routed:
        flat_joint[i] = i in UPHELD_FLAT
    else:
        flat_joint[i] = True


def line(name, conf):
    tp = sum(1 for i in GT if conf[i] and GT[i] == "T")
    fp = sum(1 for i in GT if conf[i] and GT[i] == "F")
    rlo, rhi = wilson(tp, 51)
    print(f"{name:22s} TP {tp:2d} FP {fp}  recall {tp}/51={tp / 51:.3f} "
          f"[{rlo:.3f},{rhi:.3f}]  supp {30 - fp}/30={(30 - fp) / 30:.3f}  "
          f"prec {tp}/{tp + fp}={tp / (tp + fp):.3f}")


print(f"flat routed confirmations: {len(flat_routed)} "
      f"(upheld {len(flat_routed & UPHELD_FLAT)})")
line("flat convention", flat_m)
line("flat joint (SYMMETRIC)", flat_joint)
line("full joint", full_joint)
line("full convention", full_m)

b = sum(1 for i in GT if full_joint[i] and not flat_joint[i])
c = sum(1 for i in GT if flat_joint[i] and not full_joint[i])
print(f"\njoint-vs-joint: confirmed sets "
      f"{sum(full_joint.values())} vs {sum(flat_joint.values())} = "
      f"discordant {b}/{c} p={mc(b, c):.4f}")
b2 = sum(1 for i in GT if full_m[i] and not flat_m[i])
c2 = sum(1 for i in GT if flat_m[i] and not full_m[i])
print(f"convention-vs-convention: discordant {b2}/{c2} p={mc(b2, c2):.4f}")
