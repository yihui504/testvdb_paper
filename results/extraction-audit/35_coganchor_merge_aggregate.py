"""Merge the 7-case cognition-anchor rejudge verdicts into the full arm and
re-aggregate every downstream number. Qwen runs are NOT re-judged yet (they
run in a Qwen session), so this script reports both worlds for the GLM side
and flags the Qwen-side numbers as stale."""
import glob
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
        "arms/rq2_3run")
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
                d[o["defect_id"]] = o
    return d


def load_rejudge(base, run):
    d = load(base, run)
    p = f"{ROOT}/{base}/{run}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES:
            d[o["defect_id"]] = o
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


def arm(name, runs, forced=False):
    ids = sorted(set.intersection(*(set(r) for r in runs)))
    conf = {i: (sum((r[i]["verdict"] == "CONFIRMED") if forced
                    else is_c(r[i]["verdict"]) for r in runs) >= 2)
            for i in ids}
    tp = sum(1 for i in ids if conf[i] and GT[i] == "T")
    fp = sum(1 for i in ids if conf[i] and GT[i] == "F")
    rlo, rhi = wilson(tp, 51)
    print(f"{name:26s} TP {tp:2d} FP {fp}  recall {tp/51:.3f} "
          f"[{rlo:.3f},{rhi:.3f}]  supp {(30-fp)/30:.3f}  "
          f"prec {tp/(tp+fp):.3f}")
    return conf


full_runs_old = [load("rerun_v3", f"run_full{k}") for k in (1, 2, 3)]
flat_runs = [load("rerun_v3", f"run_flat{k}") for k in (1, 2, 3)]
full_runs_new = [load_rejudge("rerun_v3", f"run_full{k}") for k in (1, 2, 3)]

print("== GLM full arm: old (cognition-anchored) vs new (cleaned) ==")
arm("full OLD majority", full_runs_old)
arm("full NEW majority", full_runs_new)
arm("full NEW forced-only", full_runs_new, forced=True)
arm("flat majority", flat_runs)

old_m = {i: sum(is_c(r[i]["verdict"]) for r in full_runs_old) >= 2
         for i in GT}
new_m = {i: sum(is_c(r[i]["verdict"]) for r in full_runs_new) >= 2 for i in GT}
flat_m = {i: sum(is_c(r[i]["verdict"]) for r in flat_runs) >= 2 for i in GT}


def pair(n1, d1, n2, d2):
    b = sum(1 for i in d1 if d1[i] and not d2[i])
    c = sum(1 for i in d2 if d2[i] and not d1[i])
    return f"{n1}: discordant {b}/{c} p={mc(b, c):.4f}"


print("\n== pairs (confirmed-set basis) ==")
print(pair("full OLD vs flat", old_m, "flat", flat_m))
print(pair("full NEW vs flat", new_m, "flat", flat_m))
Ts = [i for i in GT if GT[i] == "T"]
Fs = [i for i in GT if GT[i] == "F"]
b = sum(1 for i in Ts if new_m[i] and not flat_m[i])
c = sum(1 for i in Ts if flat_m[i] and not new_m[i])
print(f"NEW TP-only: {b}/{c} p={mc(b, c):.4f}")
bf = sum(1 for i in Fs if new_m[i] and not flat_m[i])
cf = sum(1 for i in Fs if flat_m[i] and not new_m[i])
print(f"NEW leak-only: {bf}/{cf} p={mc(bf, cf):.4f}")

print("\n== the 7 cases, per-run verdicts (old -> new) ==")
for i in sorted(CASES):
    o = [full_runs_old[k][i]["verdict"] for k in range(3)]
    n = [full_runs_new[k][i]["verdict"] for k in range(3)]
    print(f"  {i:12s} GT={GT[i]}  {o} -> {n}   flat="
          f"{[flat_runs[k][i]['verdict'] for k in range(3)]}")

print("\n== joint reading (NEW majority; reusing the 9/2/6 adjudication for "
      "the original 17 routed; the NEW routed set needs author adjudication "
      "for any case not in that worksheet) ==")
routed_old = {i for i in GT if old_m[i]
              and any(r[i]["verdict"] == "HUMAN_REVIEW" for r in full_runs_old)}
routed_new = {i for i in GT if new_m[i]
              and any(r[i]["verdict"] == "HUMAN_REVIEW" for r in full_runs_new)}
print("routed OLD:", len(routed_old), " NEW:", len(routed_new))
print("  newly routed (need adjudication):",
      sorted(routed_new - routed_old))
print("  left the routed set:", sorted(routed_old - routed_new))
joint = {}
for i in GT:
    if not new_m[i]:
        joint[i] = False
    elif i in routed_new and i not in ADJ_CONFIRM and i not in routed_old:
        joint[i] = None  # needs author adjudication
    elif i in routed_new:
        joint[i] = i in ADJ_CONFIRM or i in routed_old and old_m[i]
    else:
        joint[i] = True
need = [i for i in GT if joint[i] is None]
jtp_known = sum(1 for i in GT if joint[i] and GT[i] == "T")
print(f"joint TP known: {jtp_known} + {len(need)} pending adjudication "
      f"{sorted(need)}; joint TP ranges {jtp_known}..{jtp_known + len(need)}")
