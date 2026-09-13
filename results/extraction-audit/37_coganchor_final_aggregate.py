"""Coganchor-rejudge FINAL aggregation: both backbones' full arms merge the
7-case rejudge verdicts; every downstream number recomputed (five arms, three
readings, all paired tests, seven-test Holm family + family-size sensitivity,
strata, cross-family pair, routing rates)."""
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
# author adjudication 2026-09-13: the two newly routed cases are REJECTED
NEW_ROUTED_REJECTED = {"milvus_019", "milvus_021"}


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


def merged(base, run):
    d = load(base, run)
    p = f"{ROOT}/{base}/{run}/verdicts_coganchor_rejudge.jsonl"
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


core_runs = [load("rerun_v2", f"run{k}") for k in (1, 2, 3)]
full_runs = [merged("rerun_v3", f"run_full{k}") for k in (1, 2, 3)]
flat_runs = [load("rerun_v3", f"run_flat{k}") for k in (1, 2, 3)]
don_runs = [load("rerun_v3", f"run_donly{k}") for k in (1, 2, 3)]
donq_runs = [load("rerun_v3", f"run_donlyq{k}") for k in (1, 2, 3)]
fullq_runs = [merged("rerun_v3", f"run_fullq{k}") for k in (1, 2, 3)]
flatq_runs = [load("rerun_v3", f"run_flatq{k}") for k in (1, 2, 3)]


def majority(runs, forced=False):
    ids = sorted(set.intersection(*(set(r) for r in runs)))
    return {i: (sum((r[i] == "CONFIRMED") if forced else is_c(r[i])
                    for r in runs) >= 2) for i in ids}


def arm(name, runs, forced=False):
    m = majority(runs, forced)
    tp = sum(1 for i in m if m[i] and GT[i] == "T")
    fp = sum(1 for i in m if m[i] and GT[i] == "F")
    rlo, rhi = wilson(tp, 51)
    print(f"{name:22s} TP {tp:2d} FP {fp}  recall {tp / 51:.3f} "
          f"[{rlo:.3f},{rhi:.3f}]  supp {(30 - fp) / 30:.3f}  "
          f"prec {tp / (tp + fp):.3f}")
    return m


print("== five arms, convention scoring (cognition-anchor cleaned) ==")
core_m = arm("contract core", core_runs)
full_m = arm("full stage", full_runs)
flat_m = arm("flat judge", flat_runs)
don_m = arm("source-only (D-only)", don_runs)
donq_m = arm("D-only-Qwen", donq_runs)
print()
fullq_m = arm("full-Qwen (2nd family)", fullq_runs)
flatq_m = arm("flat-Qwen (2nd family)", flatq_runs)

print("\n== three readings, full stage ==")
full_f = arm("full, forced verdicts", full_runs, forced=True)
routed = {i for i in GT if full_m[i]
          and any(r[i] == "HUMAN_REVIEW" for r in full_runs)}
joint_m = {}
for i in GT:
    if not full_m[i]:
        joint_m[i] = False
    elif i in routed:
        joint_m[i] = i in ADJ_CONFIRM or i in routed and False
    else:
        joint_m[i] = True
# corrected: newly routed 019/021 are author-REJECTED; original routed keep
# their worksheet outcome (in ADJ_CONFIRM iff upheld)
joint_m = {}
for i in GT:
    if not full_m[i]:
        joint_m[i] = False
    elif i in routed:
        joint_m[i] = i in ADJ_CONFIRM
    else:
        joint_m[i] = True
jtp = sum(1 for i in GT if joint_m[i] and GT[i] == "T")
jfp = sum(1 for i in GT if joint_m[i] and GT[i] == "F")
print(f"{'full, joint':22s} TP {jtp:2d} FP {jfp}  recall {jtp}/51="
      f"{jtp / 51:.3f}  supp {(30 - jfp) / 30:.3f}  "
      f"prec {jtp / (jtp + jfp):.3f}")

print("\n== paired tests (confirmed-set basis) ==")


def pair(n1, d1, n2, d2):
    b = sum(1 for i in d1 if d1[i] and not d2[i])
    c = sum(1 for i in d2 if d2[i] and not d1[i])
    return b, c, mc(b, c)


def pairb(d1, d2):
    b = sum(1 for i in d1 if d1[i] and not d2[i])
    c = sum(1 for i in d2 if d2[i] and not d1[i])
    return b, c, mc(b, c)


tests = {
    "core-vs-flat": pairb(core_m, flat_m),
    "core-vs-D-only": pairb(core_m, don_m),
    "core-vs-full": pairb(core_m, full_m),
    "full-vs-flat": pairb(full_m, flat_m),
    "D-only-Qwen-vs-flat": pairb(donq_m, flat_m),
    "D-only-vs-flat": pairb(don_m, flat_m),
    "full-vs-D-only": pairb(full_m, don_m),
}
order = sorted(tests.items(), key=lambda t: t[1][2])
n = len(order)
prev = 0.0
print(f"{'test':22s} {'disc':>6s} {'raw p':>8s} {'mult':>4s} {'adj p':>7s}")
for k, (nm_, (b, c, p)) in enumerate(order):
    mult = n - k
    adj = min(1.0, max(prev, p * mult))
    prev = adj
    print(f"{nm_:22s} {b:2d}/{c:2d} {p:8.4f} {mult:4d} {adj:7.4f}")

print("\n== family-size sensitivity for the flagship ==")
p_flag = tests["full-vs-flat"][2]
for extra, label in ((0, "declared 7"), (2, "+forced & joint (9)"),
                     (3, "+second-family (10)")):
    size = 7 + extra
    rank = 1 + sum(1 for _, (b, c, p) in tests.items() if p < p_flag)
    # the excluded tests are all larger than 0.0072, so rank stays 4
    print(f"  {label:26s} n={size:2d}  rank {rank}, multiplier "
          f"{size - rank + 1}, adjusted p = {p_flag * (size - rank + 1):.4f}")

print("\n== ground-truth decomposition of the flagship net ==")
Ts = [i for i in GT if GT[i] == "T"]
b = sum(1 for i in Ts if full_m[i] and not flat_m[i])
c = sum(1 for i in Ts if flat_m[i] and not full_m[i])
print(f"  TP-only: {b}/{c} p={mc(b, c):.4f}")
bf = sum(1 for i in GT if GT[i] == 'F' and full_m[i] and not flat_m[i])
cf = sum(1 for i in GT if GT[i] == 'F' and flat_m[i] and not full_m[i])
print(f"  leak-only: {bf}/{cf} p={mc(bf, cf):.4f}")

print("\n== second family (both sides cleaned) ==")
b, c, p = pairb(fullq_m, flatq_m)
print(f"fullq-vs-flatq: discordant {b}/{c} p={p:.4f}")
fq_f = majority(fullq_runs, True)
aq_f = majority(flatq_runs, True)
qft = sum(1 for i in fq_f if fq_f[i] and GT[i] == "T")
qat = sum(1 for i in aq_f if aq_f[i] and GT[i] == "T")
qb = sum(1 for i in Ts if fq_f[i] and not aq_f[i])
qc = sum(1 for i in Ts if aq_f[i] and not fq_f[i])
print(f"  forced-only: fullq {qft}/51={qft / 51:.3f} flatq {qat}/51="
      f"{qat / 51:.3f} TP-flips {qb}/{qc} p={mc(qb, qc):.4f}")

print("\n== routing rates ==")
for nm_, runs in (("full", full_runs), ("flat", flat_runs)):
    hr = sum(1 for r in runs for i in r if r[i] == "HUMAN_REVIEW")
    print(f"  {nm_:4s} HR {hr}/243 = {hr / 243:.3f}")

print("\n== strata (full stage) ==")
mainv = [json.loads(l) for l in open(
    r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit/"
    "rebuild_v1/verify_verdicts_main.jsonl", encoding="utf-8")]
LAYER = {x["case"]: x["layer"] for x in mainv if x.get("layer")}
AUD = json.load(open(r"c:/Users/11428/Desktop/testvdb_paper/results/"
                     "extraction-audit/rebuild_final/assembly_audit.json",
                     encoding="utf-8"))
for r in AUD:
    if r["case"] not in LAYER:
        LAYER[r["case"]] = ("evidence_absent" if r["rows_kept"] == 0
                            and r["arch"] == 0 else "evidence_present")
LAYER["milvus_038"] = "weak_evidence"
for scoring, conf in (("convention", full_m), ("forced", full_f),
                      ("joint", joint_m)):
    cells = []
    for lay in ("evidence_present", "weak_evidence", "evidence_absent"):
        t = [i for i in GT if GT[i] == "T" and LAYER.get(i) == lay]
        k = sum(1 for i in t if conf[i])
        cells.append(f"{lay} {k}/{len(t)}={k / len(t):.3f}"
                     if t else f"{lay} -")
    tot = sum(1 for i in GT if GT[i] == "T" and conf[i])
    print(f"  {scoring:10s} {'; '.join(cells)}  (sum {tot})")
