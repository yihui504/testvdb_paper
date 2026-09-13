"""Paper-derivative numbers after the cognition-strip re-judge: per-run table
rows, flat closure of the routed confirmations, joint-vs-flat pair, and the
Qwen forced-only pair."""
import glob
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
        "arms/rq2_3run")
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))

# human adjudication of the 17 routed confirmations (final, in worksheet)
ADJ_CONFIRM = {"milvus_005", "milvus_013", "milvus_036", "milvus_038",
               "milvus_043", "qdrant_014", "qdrant_015", "qdrant_016",
               "qdrant_027"}


def load(run, base):
    d = {}
    for f in sorted(glob.glob(f"{ROOT}/{base}/{run}/verdicts_batch*.jsonl")):
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


def tfp(d):
    tp = sum(1 for i in d if is_c(d[i]) and GT[i] == "T")
    fp = sum(1 for i in d if is_c(d[i]) and GT[i] == "F")
    return tp, fp


def mc(b, c):
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, k)
                            for k in range(0, min(b, c) + 1)) / 2 ** n)


print("== per-run table rows (TP FP FN TN) ==")
for r in ("run1", "run2", "run3"):
    tp, fp = tfp(load(r, "rerun_v2"))
    print(f"core {r}: {tp} {fp} {51 - tp} {30 - fp}")
for r in ("run_donly1", "run_donly2", "run_donly3"):
    tp, fp = tfp(load(r, "rerun_v3"))
    print(f"D-only {r}: {tp} {fp} {51 - tp} {30 - fp}")
for r in ("run_flat1", "run_flat2", "run_flat3"):
    tp, fp = tfp(load(r, "rerun_v3"))
    print(f"flat {r}: {tp} {fp} {51 - tp} {30 - fp}")
for r in ("run_donlyq1", "run_donlyq2", "run_donlyq3"):
    tp, fp = tfp(load(r, "rerun_v3"))
    print(f"D-onlyQ {r}: {tp} {fp} {51 - tp} {30 - fp}")

full_runs = [load(f"run_full{i}", "rerun_v3") for i in (1, 2, 3)]
flat_runs = [load(f"run_flat{i}", "rerun_v3") for i in (1, 2, 3)]

routed = [i for i in GT
          if sum(is_c(r.get(i)) for r in full_runs) >= 2
          and any(r.get(i) == "HUMAN_REVIEW" for r in full_runs)]
n_fp = sum(1 for i in routed
           if sum(1 if r.get(i) == "FALSE_POSITIVE" else 0
                  for r in flat_runs) >= 2)
print(f"\nrouted confirmations {len(routed)}; flat closes as FP: {n_fp}")

# joint system: forced-confirmed + adjudicated-confirmed, routed FPs resolved
joint = {}
for i in GT:
    vs = [is_c(r.get(i)) for r in full_runs]
    if sum(vs) >= 2:
        if i in routed:
            joint[i] = "CONFIRMED" if i in ADJ_CONFIRM else "FALSE_POSITIVE"
        else:
            joint[i] = "CONFIRMED"
    else:
        joint[i] = "FALSE_POSITIVE"
jtp, jfp = tfp(joint)
ftp, ffp = tfp(flat := {i: ("CONFIRMED" if sum(is_c(r.get(i))
                                              for r in flat_runs) >= 2
                            else "FALSE_POSITIVE") for i in GT})
b = sum(1 for i in joint if joint[i] == "CONFIRMED" and flat[i] != "CONFIRMED")
c = sum(1 for i in joint if joint[i] != "CONFIRMED"
        and flat[i] == "CONFIRMED")
print(f"joint: TP {jtp} FP {jfp} (recall {jtp/51:.3f}, supp {(30-jfp)/30:.3f})"
      f"  flat: TP {ftp} FP {ffp}")
print(f"joint-vs-flat discordant {b}/{c} p={mc(b, c):.4f}")

qf = load("run_fullq1", "rerun_v3")
qa = load("run_flatq1", "rerun_v3")
qfc = {i: (qf[i] == "CONFIRMED") for i in qf}
qac = {i: (qa[i] == "CONFIRMED") for i in qa}
qtp = sum(1 for i in qfc if qfc[i] and GT[i] == "T")
atp = sum(1 for i in qac if qac[i] and GT[i] == "T")
b = sum(1 for i in qf if qfc[i] and not qac[i])
c = sum(1 for i in qf if not qfc[i] and qac[i])
qhr = sum(1 for v in qa.values() if v == "HUMAN_REVIEW")
print(f"\nQwen forced-only: full {qtp}/51={qtp/51:.3f} "
      f"flat {atp}/51={atp/51:.3f} discordant {b}/{c} p={mc(b, c):.4f}")
print(f"Qwen-flat HR after rejudge: {qhr}/81 = {qhr/81:.3f}")
