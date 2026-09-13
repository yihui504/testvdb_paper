"""Repair the pack-install path bug.

The rerun prep installed the rebuilt packs into arms/rq2_3run/materials_complete
(a fresh, unreferenced directory) while every dispatch file points at
arms/materials_complete - which still held the *original* v9 packs. Every
verdict produced so far was therefore judged on the original packs and is void.

This script:
  1. archives the original arms/materials_complete to _v9_archive/
  2. installs rebuild_final/packs/*.md into arms/materials_complete/
  3. moves every rerun_v2 verdict file to rerun_v2/_voided_wrongpacks/
  4. verifies byte-identity against rebuild_final
"""
import filecmp
import glob
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ARMS = r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/arms"
ROOT = ARMS + "/rq2_3run"
MAT = ARMS + "/materials_complete"                       # what dispatches read
REBUILT = (r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit/"
           "rebuild_final/packs")
ARCH = ROOT + "/_v9_archive"
VOID = ROOT + "/rerun_v2/_voided_wrongpacks"
WRONG_INSTALL = ROOT + "/materials_complete"             # the accidental dir


def main() -> None:
    # 1. archive the originals
    dst = ARCH + "/materials_complete_v9originals"
    if os.path.isdir(MAT):
        if os.path.isdir(dst):
            print("archive target already exists; leaving as-is:", dst)
        else:
            shutil.move(MAT, dst)
            print("archived originals ->", dst)

    # 2. install rebuilt packs at the path the dispatches actually use
    os.makedirs(MAT, exist_ok=True)
    n = 0
    for f in sorted(glob.glob(REBUILT + "/*.md")):
        shutil.copy2(f, os.path.join(MAT, os.path.basename(f)))
        n += 1
    print("installed rebuilt packs into", MAT, ":", n)

    # 3. void every verdict produced against the wrong packs
    os.makedirs(VOID, exist_ok=True)
    moved = 0
    for f in glob.glob(ROOT + "/rerun_v2/*/verdicts_batch*.jsonl"):
        run = os.path.basename(os.path.dirname(f))
        os.makedirs(VOID + "/" + run, exist_ok=True)
        shutil.move(f, VOID + "/" + run + "/" + os.path.basename(f))
        moved += 1
    print("voided verdict files:", moved)

    # 4. verify identity + report the accidental dir
    bad = []
    for f in sorted(glob.glob(MAT + "/*.md")):
        base = os.path.basename(f)
        src = REBUILT + "/" + base
        if not os.path.exists(src) or not filecmp.cmp(f, src, shallow=False):
            bad.append(base)
    print("identity check:", "OK (81/81 match)" if not bad else f"MISMATCH {bad}")
    if os.path.isdir(WRONG_INSTALL):
        print("NOTE: stray dir still present:", WRONG_INSTALL,
              f"({len(os.listdir(WRONG_INSTALL))} files) - harmless, unreferenced")


if __name__ == "__main__":
    main()
