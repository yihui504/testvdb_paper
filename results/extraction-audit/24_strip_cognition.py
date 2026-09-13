"""Strip the embedded maintainer-cognition section from the 10 affected packs.

The section (inherited from the v9 originals) leaks D-perspective material
into arms whose dispatches forbid reading cognition files. We archive the
originals, remove the section, and verify the diff is exactly that block.
"""
import glob
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MAT = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
       r"arms/materials_complete")
ARCH = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
        r"arms/rq2_3run/_v9_archive/packs_pre_cogstrip")

TARGETS = ["milvus_010", "milvus_014", "milvus_018", "milvus_019",
           "milvus_022", "milvus_026", "milvus_027", "milvus_028",
           "milvus_032", "milvus_033"]

HDR = "--- 维护者态度参考（developer_cognition"
NEXT = re.compile(r"^(VERDICT:|--- )")


def strip(text: str) -> tuple[str, int]:
    lines = text.split("\n")
    out, cutting, removed = [], False, 0
    for ln in lines:
        if not cutting and ln.startswith(HDR):
            cutting = True
            removed += 1
            continue
        if cutting:
            if NEXT.match(ln):
                cutting = False
                out.append(ln)
            else:
                removed += 1
            continue
        out.append(ln)
    return "\n".join(out), removed


def main():
    os.makedirs(ARCH, exist_ok=True)
    for case in TARGETS:
        f = os.path.join(MAT, case + ".md")
        orig = open(f, encoding="utf-8").read()
        assert HDR in orig, f"{case}: header not found"
        shutil.copy2(f, os.path.join(ARCH, case + ".md"))
        new, removed = strip(orig)
        assert HDR not in new, f"{case}: header survived"
        # sanity: contract rows and observed section untouched
        assert new.count("evidence_tier") == orig.count("evidence_tier"), case
        assert new.count("constraint_id") == orig.count("constraint_id"), case
        open(f, "w", encoding="utf-8").write(new)
        print(f"{case}: removed {removed} lines")
    # confirm no other pack carries the section
    stray = [f for f in glob.glob(MAT + "/*.md")
             if HDR in open(f, encoding="utf-8").read()]
    print("stray packs still carrying section:", stray or "none")


if __name__ == "__main__":
    main()
