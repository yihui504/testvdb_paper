"""Round-15 PR: the single authoritative routed-case accounting, computed from
the frozen verdict files (cognition-anchor-cleaned pool).

Definitions fixed here:
  convention-confirmed  = CONFIRMED or HUMAN_REVIEW in >= 2 of 3 runs
  forced-confirmed      = CONFIRMED in >= 2 of 3 runs
  routed-only           = convention-confirmed but not forced-confirmed
  HR-carrying           = convention-confirmed with >= 1 HUMAN_REVIEW vote
  routed false positive = FP candidate that is convention-confirmed with >= 1
                          HUMAN_REVIEW vote
"""
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


def report(name, runs):
    conv = {i for i in GT if sum(is_c(runs[k][i]) for k in range(3)) >= 2}
    forc = {i for i in GT if sum(runs[k][i] == "CONFIRMED"
                                 for k in range(3)) >= 2}
    routed_only = conv - forc
    hr_carry = {i for i in conv
                if any(runs[k][i] == "HUMAN_REVIEW" for k in range(3))}
    hr_fp = {i for i in hr_carry if GT[i] == "F"}
    hr_tp = {i for i in hr_carry if GT[i] == "T"}
    pooled_hr = sum(1 for k in range(3) for i in GT
                    if runs[k][i] == "HUMAN_REVIEW")
    print(f"== {name} ==")
    print(f"  convention-confirmed {len(conv)}  (TP "
          f"{sum(1 for i in conv if GT[i] == 'T')}, FP "
          f"{sum(1 for i in conv if GT[i] == 'F')})")
    print(f"  forced-confirmed     {len(forc)}")
    print(f"  routed-only          {len(routed_only)}  (TP "
          f"{sum(1 for i in routed_only if GT[i] == 'T')}, FP "
          f"{sum(1 for i in routed_only if GT[i] == 'F')})")
    print(f"  HR-carrying          {len(hr_carry)}  (TP {len(hr_tp)}, "
          f"FP {len(hr_fp)})")
    print(f"  pooled HR verdicts   {pooled_hr}/243 = {pooled_hr / 243:.3f}")
    print(f"  routed FPs (HR,GT=F) {sorted(hr_fp)}")
    print(f"  routed-only cases:   {sorted(routed_only)}")
    print(f"  HR-carrying TPs:     {sorted(hr_tp)}")
    return conv, forc, routed_only, hr_carry


print("### GLM side")
report("full (cleaned)", full)
report("flat", flat)
