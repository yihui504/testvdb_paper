"""Problem 2 (second pass), step 1: extract the unique set of routed cases
across both arms — the cases a blind second-pass adjudicator must judge."""
import glob
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}
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

uniq = sorted(full_routed | flat_routed)
both = sorted(full_routed & flat_routed)
print(f"full routed {len(full_routed)}, flat routed {len(flat_routed)}, "
      f"unique {len(uniq)} (both arms: {len(both)} -> {both})")
print(f"\nGT split of unique set: "
      f"T={sum(1 for i in uniq if GT[i] == 'T')} "
      f"F={sum(1 for i in uniq if GT[i] == 'F')}")
print("\nunique routed cases:")
for i in uniq:
    arms = ("both" if i in full_routed and i in flat_routed
            else "full" if i in full_routed else "flat")
    print(f"  {i:14s} GT={GT[i]}  arm={arms}")

# materials availability
import os
missing = [i for i in uniq
           if not os.path.exists(f"{ROOT}/materials_complete/{i}.md")]
print(f"\npack materials missing: {missing or 'none'}")

json.dump({"full_routed": sorted(full_routed),
           "flat_routed": sorted(flat_routed),
           "unique": uniq},
          open("results/extraction-audit/routed_unique.json", "w"),
          indent=1)
print("written: results/extraction-audit/routed_unique.json")
