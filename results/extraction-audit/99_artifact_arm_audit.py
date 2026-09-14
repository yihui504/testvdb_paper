"""Audit the replication package against the paper, arm by arm.

For every arm the paper reports, compare the artifact's per-case verdicts with
the ones the paper's own numbers are computed from, and report the generation
each artifact copy came from. A stale copy is worse than a missing one: it lets
a reviewer recompute a number the paper does not report.
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ART = r"C:/Users/11428/Desktop/TestVDB_artifact/rq2/verdicts"
PAPER = r".paperpilot/phase2-rerun/arms/rq2_3run"
GT = json.load(open(f"{PAPER}/gt_81.json", encoding="utf-8"))
CASES = sorted(GT)


def load(d, ovr=None):
    v = {}
    for f in sorted(glob.glob(os.path.join(d, "verdicts_batch*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                o = json.loads(line)
                v[o["defect_id"]] = o["verdict"]
    if ovr:
        p = os.path.join(d, ovr)
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                line = line.strip()
                if line:
                    o = json.loads(line)
                    v[o["defect_id"]] = o["verdict"]
    return v


def majority(v):
    return {c: ("CONFIRMED"
                if sum(1 for r in v if r.get(c) == "CONFIRMED") * 2 >= 3
                else "FALSE_POSITIVE") for c in CASES}


def triple(dirs, ovr):
    return [{c: load(d, ovr).get(c, "MISSING") for c in CASES} for d in dirs]


# arm -> (artifact dirs, paper dirs, override)
ARMS = [
    ("contract core", "run", f"{PAPER}/rerun_v2/run",
     "verdicts_rejudge_cog.jsonl"),
    ("full stage", "run_full", f"{PAPER}/rerun_v3/run_full",
     "verdicts_coganchor_rejudge.jsonl"),
    ("source-only", "run_donly", f"{PAPER}/rerun_v3/run_donly",
     "verdicts_rejudge_cog.jsonl"),
    ("flat judge", "run_flat", f"{PAPER}/rerun_v3/run_flat",
     "verdicts_rejudge_cog.jsonl"),
    ("source-only-Qwen", "run_donlyq", f"{PAPER}/rerun_v3/run_donlyq",
     "verdicts_rejudge_cog.jsonl"),
]

print(f"{'arm':20s} {'artifact vs paper':>20s}   generation match")
print("-" * 70)
for name, art_pat, paper_pat, ovr in ARMS:
    adirs = [f"{ART}/{art_pat}{i}" for i in (1, 2, 3)]
    pdirs = [f"{paper_pat}{i}" for i in (1, 2, 3)]
    if not all(os.path.isdir(d) for d in adirs):
        print(f"{name:20s} {'[absent]':>20s}")
        continue
    a, p = triple(adirs, ovr), triple(pdirs, ovr)
    diff = sum(1 for r in range(3) for c in CASES if a[r][c] != p[r][c])
    # where does the artifact copy actually come from?
    src = "?"
    for cand in sorted(glob.glob(
            ".paperpilot/phase2-rerun/**/verdicts_batch*.jsonl", recursive=True)):
        d = os.path.dirname(cand)
        if len(load(d)) != 81:
            continue
        if all(a[0][c] == load(d).get(c) for c in CASES):
            src = d.replace(".paperpilot/phase2-rerun/", "")
            break
    tar, tpa = majority(a), majority(p)
    tpa_ = sum(tar[c] and GT[c] == "T" for c in CASES)
    tpb = sum(tar[c] and GT[c] == "F" for c in CASES)
    ppa = sum(tpa[c] and GT[c] == "T" for c in CASES)
    ppb = sum(tpa[c] and GT[c] == "F" for c in CASES)
    verdict = "SAME" if diff == 0 else f"DIFFER ({diff} judgments)"
    print(f"{name:20s} {verdict:>20s}   run1 came from: {src}")
    print(f"{'':20s} {'':>20s}   artifact majority TP={tpa_} FP={tpb} | "
          f"paper TP={ppa} FP={ppb}")
