"""Coverage audit: for every re-judged run in the development tree, does the
artifact ship the re-judged cases AND the pre-repair state?

The lesson from the candidate-anchor backfill is that a repair reaching the
development tree but not the shipped package produces two sets of numbers and
no error. This checks the class, not one instance.

Both tree layouts are scanned. The contract core lives in `rerun_v2/run{1,2,3}`
and is shipped as `rq2/verdicts/run{1,2,3}`; everything else lives in
`rerun_v3/`. A first version of this script scanned only `rerun_v3`, which is
how the core's three missing pre-strip archives went unnoticed.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ARMS = r".paperpilot/phase2-rerun/arms/rq2_3run"
ART = r"C:/Users/11428/Desktop/TestVDB_artifact/rq2/verdicts"
# (development directory, name the artifact ships it under)
TREES = ([(f"{ARMS}/rerun_v3/{d}", d) for d in
          ("run_full1", "run_full2", "run_full3",
           "run_fullq1", "run_fullq2", "run_fullq3",
           "run_fullnosrc1", "run_fullnosrc2", "run_fullnosrc3",
           "run_noscopic1", "run_noscopic2", "run_noscopic3",
           "run_donly1", "run_donly2", "run_donly3",
           "run_donlyq1", "run_donlyq2", "run_donlyq3",
           "run_flat1", "run_flat2", "run_flat3", "run_flatq1")]
         + [(f"{ARMS}/rerun_v2/run{i}", f"run{i}") for i in (1, 2, 3)])
REJUDGE = ("verdicts_coganchor_rejudge.jsonl", "verdicts_rejudge_cog.jsonl",
           "verdicts_clean.jsonl")
PRE = ("_pre_coganchor.jsonl", "_pre_cogstrip_merge")

print(f"{'run':18s} {'rejudge':22s} {'pre-state':20s} {'in artifact?':12s}")
print("-" * 78)
bad = 0
for dev_dir, d in TREES:
    p = dev_dir
    if not os.path.isdir(p):
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
