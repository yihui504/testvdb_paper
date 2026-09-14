"""Sweep pool variants / bases for the paper's 4.3 sentence

  "Of its 39 confirmations, 24 are Confirmed in all three runs and 15 carry at
   least one Human-Review component---12 routed by the majority of their three
   runs and 3 confirmed two-to-one on ordinary votes with a minority
   Human-Review vote alongside."

R3 (round-16) flagged a parity non-closure around these aggregates; the
aggregates themselves close, but this 4-way sub-split does not obviously
reproduce. Find the basis that does, or prove none does.
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = r".paperpilot/phase2-rerun/arms/rq2_3run"
V3 = os.path.join(BASE, "rerun_v3")
GT = json.load(open(os.path.join(BASE, "gt_81.json"), encoding="utf-8"))
COGANCHOR = ["milvus_004", "milvus_006", "milvus_018", "milvus_019",
             "milvus_021", "milvus_027", "qdrant_017"]
IS_C = lambda v: v in ("CONFIRMED", "HUMAN_REVIEW")


def load(paths):
    v = {}
    for f in paths:
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                j = json.loads(line)
                v[j["defect_id"]] = j["verdict"]
    return v


pools = {}
for r in (1, 2, 3):
    b = load(sorted(glob.glob(os.path.join(V3, f"run_full{r}",
                                           "verdicts_batch*.jsonl"))))
    rj = load([os.path.join(V3, f"run_full{r}",
                            "verdicts_coganchor_rejudge.jsonl")])
    pools.setdefault("B_nocoganchor_override", {})[r] = dict(b)
    c = dict(b)
    c.update(rj)
    pools.setdefault("A_final_clean", {})[r] = c

# optional archived pre-cogstrip originals
arch = glob.glob(os.path.join(V3, "run_full1", "_pre_cogstrip_merge*"))
print(f"archived pre-cogstrip dirs: {arch}")

for name, pool in pools.items():
    print(f"\n############ {name} ############")
    for restrict, label in ((None, "all 48 majority-confirmed"),
                            ("T", "39 TP majority-confirmed"),
                            ("F", "9 FP-leak majority-confirmed")):
        cases = [c for c in sorted(GT)
                 if sum(IS_C(pool[r][c]) for r in (1, 2, 3)) >= 2
                 and (restrict is None or GT[c] == restrict)]
        vecs = {}
        for c in cases:
            vecs[c] = "".join("C" if pool[r][c] == "CONFIRMED"
                              else ("H" if pool[r][c] == "HUMAN_REVIEW" else "F")
                              for r in (1, 2, 3))
        all3c = sum(1 for v in vecs.values() if v == "CCC")
        anyhr = sum(1 for v in vecs.values() if "H" in v)
        hrmaj = sum(1 for v in vecs.values() if v.count("H") >= 2)
        hr1 = sum(1 for v in vecs.values() if v.count("H") == 1)
        hr1_c2 = sum(1 for v in vecs.values() if v.count("H") == 1
                     and v.count("C") == 2)
        neither = len(cases) - all3c - anyhr
        print(f"  {label}: n={len(cases)}  all3_CONFIRMED={all3c}  "
              f"anyHR={anyhr}  [HRmaj={hrmaj}  HRx1={hr1} (of which C2={hr1_c2})]  "
              f"neither={neither}")
        print(f"      all3+anyHR = {all3c + anyhr}")

print("\n=== final pool, TP vectors ===")
pool = pools["A_final_clean"]
for c in sorted(GT):
    if GT[c] == "T" and sum(IS_C(pool[r][c]) for r in (1, 2, 3)) >= 2:
        v = "".join("C" if pool[r][c] == "CONFIRMED"
                    else ("H" if pool[r][c] == "HUMAN_REVIEW" else "F")
                    for r in (1, 2, 3))
        print(f"  {c:14s} {v}")
