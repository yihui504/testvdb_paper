"""Exact routed sets for both arms, so the joint-reading prose can be
reconciled with the 12/39 routing attribution."""
import glob
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))
ADJ_CONFIRM_FULL = {"milvus_005", "milvus_013", "milvus_036", "milvus_038",
                    "milvus_043", "qdrant_014", "qdrant_015", "qdrant_016",
                    "qdrant_027"}
UPHELD_FLAT = {"milvus_010", "milvus_033", "weaviate_003", "milvus_036",
               "milvus_038", "milvus_043", "qdrant_014"}


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

for name, runs, maj in (("full", full, full_m), ("flat", flat, flat_m)):
    conf = [i for i in GT if maj[i]]
    routed = [i for i in conf
              if any(runs[r][i] == "HUMAN_REVIEW" for r in range(3))]
    print(f"{name}: confirmations {len(conf)}  routed {len(routed)}")
    print(f"   routed T/F: "
          f"{sum(1 for i in routed if GT[i] == 'T')}/"
          f"{sum(1 for i in routed if GT[i] == 'F')}")
    for i in sorted(routed):
        vs = [runs[r][i] for r in range(3)]
        tag = "adj-confirmed" if (name == "full" and i in ADJ_CONFIRM_FULL) \
            or (name == "flat" and i in UPHELD_FLAT) else "REJECTED/other"
        print(f"     {i:14s} GT={GT[i]} {vs}  -> {tag}")
    print()

print("=== cross-arm: what the flat judge does to the full arm's routed TPs ===")
full_routed_tp = [i for i in GT if GT[i] == "T" and full_m[i]
                  and any(full[r][i] == "HUMAN_REVIEW" for r in range(3))]
closed = [i for i in full_routed_tp if not flat_m[i]]
print(f"full routed TPs {len(full_routed_tp)}; flat closes as non-confirmation: "
      f"{len(closed)} -> {sorted(closed)}")
print("=== table 6 caption ===")
import re
tex = open("TestVDB.tex", encoding="utf-8").read()
m = re.search(r"\caption\{Table 6 caption placeholder\}", tex)
m = re.search(r"(?s)tab:scorings.*?\n\end\{table\}", tex)
print(m.group(0)[:1400] if m else "not found")
