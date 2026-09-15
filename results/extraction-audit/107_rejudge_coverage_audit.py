"""Coverage audit: for every re-judged run in the development tree, does the
artifact ship the re-judged cases AND the pre-repair state?

The lesson from the candidate-anchor backfill is that a repair reaching the
development tree but not the shipped package produces two sets of numbers and
no error. This checks the class, not one instance.
"""
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEV = r".paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3"
ART = r"C:/Users/11428/Desktop/TestVDB_artifact/rq2/verdicts"
REJUDGE = ("verdicts_coganchor_rejudge.jsonl", "verdicts_rejudge_cog.jsonl")
PRE = ("_pre_coganchor.jsonl", "_pre_cogstrip_merge")

print(f"{'run':18s} {'rejudge':22s} {'pre-state':20s} {'in artifact?':12s}")
print("-" * 78)
bad = 0
for d in sorted(os.listdir(DEV)):
    p = os.path.join(DEV, d)
    if not os.path.isdir(p) or not d.startswith("run_"):
        continue
    rj = [f for f in REJUDGE if os.path.exists(os.path.join(p, f))]
    pre = [f for f in PRE if os.path.exists(os.path.join(p, f))]
    if not rj:
        continue
    ok_rj = all(os.path.exists(os.path.join(ART, d, f)) for f in rj)
    # An empty `pre` is a gap, not a pass: all() over nothing is vacuously true,
    # and "the run was re-judged but kept no pre-repair state" is exactly the
    # defect this audit exists to catch.
    ok_pre = bool(pre) and all(os.path.exists(os.path.join(ART, d, f))
                               for f in pre)
    status = "OK" if (ok_rj and ok_pre) else "GAP"
    if status == "GAP":
        bad += 1
    print(f"{d:18s} {','.join(rj) or '-':22s} {','.join(pre) or '[none]':20s} "
          f"{status:12s}")
    if status == "GAP":
        if not pre:
            print(f"    no pre-repair state in the development tree either")
        for f in rj + pre:
            if not os.path.exists(os.path.join(ART, d, f)):
                print(f"    missing from artifact: {d}/{f}")
print(f"\n  {bad} runs with a coverage gap")
