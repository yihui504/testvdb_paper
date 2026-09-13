"""Generate Qwen-backbone dispatch files for the full and flat arms (single
run each): copy the v3 protocol dispatches of run_full1 / run_flat1, pointing
the output paths at run_fullq1 / run_flatq1."""
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

V3 = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
      "arms/rq2_3run/rerun_v3")

n = 0
for src_run, dst_run in (("run_full1", "run_fullq1"),
                         ("run_flat1", "run_flatq1")):
    dst_dir = os.path.join(V3, dst_run)
    os.makedirs(dst_dir, exist_ok=True)
    for f in sorted(glob.glob(f"{V3}/{src_run}/batch*_dispatch.txt")):
        t = open(f, encoding="utf-8").read()
        t = t.replace(f"rerun_v3\\{src_run}", f"rerun_v3\\{dst_run}")
        t = t.replace(f"rerun_v3/{src_run}", f"rerun_v3/{dst_run}")
        open(os.path.join(dst_dir, os.path.basename(f)), "w",
             encoding="utf-8").write(t)
        n += 1
print("dispatch files written:", n)

bad = 0
for r in ("run_fullq1", "run_flatq1"):
    for f in glob.glob(f"{V3}/{r}/batch*_dispatch.txt"):
        t = open(f, encoding="utf-8").read()
        ok = (r in t
              and "rerun_v3\\run_full1" not in t
              and "rerun_v3\\run_flat1" not in t
              and "rerun_v3/run_full1" not in t
              and "rerun_v3/run_flat1" not in t)
        if r == "run_fullq1":
            ok = ok and "客观约束" in t
        if not ok:
            bad += 1
            print("BAD:", f)
print("check:", "OK" if bad == 0 else f"{bad} BAD")
