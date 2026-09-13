"""Prepare the rerun: archive v9 runs + packs, install rebuilt packs into
materials_complete/ (same filenames), and emit rerun_v2 dispatch files whose
output paths point at fresh verdict directories."""
import glob
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/arms/rq2_3run"
ARCH = ROOT + "/_v9_archive"
REBUILT = (r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit/"
           "rebuild_final/packs")
RUNS = [f"run{i}" for i in (1, 2, 3)] + \
       [f"run_full{i}" for i in (1, 2, 3)] + \
       [f"run_flat{i}" for i in (1, 2, 3)] + \
       [f"run_donly{i}" for i in (1, 2, 3)] + \
       [f"run_donlyq{i}" for i in (1, 2, 3)]


def main() -> None:
    os.makedirs(ARCH, exist_ok=True)
    # 1. archive v9 runs and the v9 packs (move, not copy)
    for run in RUNS:
        src = os.path.join(ROOT, run)
        if os.path.isdir(src):
            shutil.move(src, os.path.join(ARCH, run))
            print("archived run:", run)
    mat = os.path.join(ROOT, "materials_complete")
    if os.path.isdir(mat):
        shutil.move(mat, os.path.join(ARCH, "materials_complete"))
        print("archived materials_complete")

    # 2. install rebuilt packs under the original name
    os.makedirs(mat, exist_ok=True)
    n = 0
    for f in glob.glob(REBUILT + "/*.md"):
        shutil.copy2(f, os.path.join(mat, os.path.basename(f)))
        n += 1
    print("installed rebuilt packs:", n)

    # 3. rewrite dispatch files with rerun_v2 output paths
    out_root = os.path.join(ROOT, "rerun_v2")
    n_dispatch = 0
    for run in RUNS:
        src_dir = os.path.join(ARCH, run)
        if not os.path.isdir(src_dir):
            continue
        dst_dir = os.path.join(out_root, run)
        os.makedirs(dst_dir, exist_ok=True)
        for f in sorted(glob.glob(src_dir + "/batch*_dispatch.txt")):
            t = open(f, encoding="utf-8").read()
            t2 = t.replace("rq2_3run\\" + run, "rq2_3run\\rerun_v2\\" + run)
            t2 = t2.replace("rq2_3run/" + run, "rq2_3run/rerun_v2/" + run)
            base = os.path.basename(f)
            open(os.path.join(dst_dir, base), "w",
                 encoding="utf-8").write(t2)
            n_dispatch += 1
    print("rerun_v2 dispatch files:", n_dispatch)

    # sanity: no dispatch may still point at the archived path
    bad = 0
    for f in glob.glob(out_root + "/*/batch*_dispatch.txt"):
        t = open(f, encoding="utf-8").read()
        if re.search(r"rq2_3run[\\\\/]run", t):
            bad += 1
            print("STILL OLD PATH:", f)
    print("path check:", "OK" if bad == 0 else f"{bad} BAD")


if __name__ == "__main__":
    main()
