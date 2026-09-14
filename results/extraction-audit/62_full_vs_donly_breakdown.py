"""Problem 3A: case-level decomposition of the full-vs-source-only difference
(discordant 8/4, net +4, p=0.39). Question: is the full stage's edge over its
own source component carried by the routing channel (HR-mediated confirmations
the binary arm force-closes) or by the perspectives?"""
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
                d[o["defect_id"]] = o
    return d


def is_c(v):
    return v in ("CONFIRMED", "HUMAN_REVIEW")


full = [load("rerun_v3", f"run_full{k}") for k in (1, 2, 3)]
donly = [load("rerun_v3", f"run_donly{k}") for k in (1, 2, 3)]
for r in range(3):
    p = f"{ROOT}/rerun_v3/run_full{r + 1}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES_FULL:
            full[r][o["defect_id"]] = o

full_m = {i: sum(is_c(full[r][i]["verdict"]) for r in range(3)) >= 2
          for i in GT}
donly_m = {i: sum(donly[r][i]["verdict"] == "CONFIRMED" for r in range(3)) >= 2
           for i in GT}

full_only = [i for i in sorted(GT) if full_m[i] and not donly_m[i]]
donly_only = [i for i in sorted(GT) if donly_m[i] and not full_m[i]]
print(f"full-only confirmations: {len(full_only)}")
print(f"source-only-only       : {len(donly_only)}\n")

print("== full-only cases: is the confirmation HR-mediated? ==")
for i in full_only:
    fv = [full[r][i]["verdict"] for r in range(3)]
    dv = [donly[r][i]["verdict"] for r in range(3)]
    n_hr = sum(1 for v in fv if v == "HUMAN_REVIEW")
    n_c = sum(1 for v in fv if v == "CONFIRMED")
    # majority-HR => exists only via routing; majority-Confirmed w/ HR
    # minority => forced majority exists but routing carried it over
    kind = ("ROUTED (majority HR)"
            if n_hr >= 2 else
            f"forced majority ({n_c}/3 C) + HR minority")
    persp = []
    for r in range(3):
        o = full[r][i]
        if o.get("perspectives"):
            persp.append({k: str(v)[:4]
                          for k, v in o["perspectives"].items()})
    b_hits = sum(1 for p in persp if p.get("B", "").startswith("CONF"))
    print(f"  {i:14s} GT={GT[i]}  full={fv}  donly={dv}")
    print(f"      -> {kind}; B=CONF in {b_hits}/3 runs; donly never confirms"
          if donly_m[i] is False else "")

print("\n== source-only-only cases ==")
for i in donly_only:
    fv = [full[r][i]["verdict"] for r in range(3)]
    dv = [donly[r][i]["verdict"] for r in range(3)]
    print(f"  {i:14s} GT={GT[i]}  full={fv}  donly={dv}")

# summary counts
hr_carried = sum(1 for i in full_only
                 if sum(1 for r in range(3)
                        if full[r][i]["verdict"] == "HUMAN_REVIEW") >= 2)
forced_carried = len(full_only) - hr_carried
tp = sum(1 for i in full_only if GT[i] == "T")
print(f"\nfull-only {len(full_only)} = routed-only {hr_carried} + "
      f"forced-majority {forced_carried}; of which TP {tp}, "
      f"FP {len(full_only) - tp}")
