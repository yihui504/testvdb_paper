"""How many upheld hand-adjudications were already counted under forced
scoring? Cycle-3 R1 4.3 / R3 4.4 both flagged that Table 6's joint rows are not
recomputable from the stated counts without this overlap."""
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
full_forced = {i: sum(full[r][i] == "CONFIRMED"
                      for r in range(3)) >= 2 for i in GT}
flat_forced = {i: sum(flat[r][i] == "CONFIRMED"
                      for r in range(3)) >= 2 for i in GT}


def report(name, upheld, forced, conv, gt_filter="T"):
    tp_for = sum(1 for i in GT if GT[i] == gt_filter and forced[i])
    tp_conv = sum(1 for i in GT if GT[i] == gt_filter and conv[i])
    overlap = [i for i in sorted(upheld) if forced[i]]
    fresh = [i for i in sorted(upheld) if not forced[i]]
    print(f"== {name} ==")
    print(f"  forced-confirmed ({gt_filter}): {tp_for}")
    print(f"  convention-confirmed ({gt_filter}): {tp_conv}")
    print(f"  upheld hand-adjudications: {len(upheld)}")
    print(f"    already forced-confirmed: {len(overlap)} -> {overlap}")
    print(f"    newly added by the pass : {len(fresh)} -> {fresh}")
    print(f"  joint = {tp_for} + {len(fresh)} = {tp_for + len(fresh)}")


report("full", ADJ_CONFIRM_FULL, full_forced, full_m)
print()
report("flat", UPHELD_FLAT, flat_forced, flat_m)
