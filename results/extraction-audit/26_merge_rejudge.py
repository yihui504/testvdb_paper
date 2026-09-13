"""Merge the cognition-strip re-judge verdicts into the run verdict files.

For each run that has verdicts_rejudge_cog.jsonl, replace the verdict lines
of the 10 re-judged cases inside the original verdicts_batch*.jsonl files.
The pre-merge originals are archived to _pre_cogstrip_merge/ under the run
directory first, so the merge is reversible and auditable.
"""
import glob
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R3 = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
      r"arms/rq2_3run/rerun_v3")
V2 = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
      r"arms/rq2_3run/rerun_v2")

RUNS = ([f"{V2}/run{i}" for i in (1, 2, 3)] +
        [f"{R3}/{r}" for r in ("run_flat1", "run_flat2", "run_flat3",
                               "run_donly1", "run_donly2", "run_donly3",
                               "run_donlyq1", "run_donlyq2", "run_donlyq3",
                               "run_flatq1")])


def main():
    for run_dir in RUNS:
        rj = os.path.join(run_dir, "verdicts_rejudge_cog.jsonl")
        if not os.path.exists(rj):
            continue
        new = {}
        for l in open(rj, encoding="utf-8"):
            l = l.strip()
            if l:
                o = json.loads(l)
                new[o["defect_id"]] = o
        assert len(new) == 10, (rj, len(new))
        batches = sorted(glob.glob(run_dir + "/verdicts_batch*.jsonl"))
        arch = os.path.join(run_dir, "_pre_cogstrip_merge")
        os.makedirs(arch, exist_ok=True)
        replaced = 0
        for b in batches:
            dst = os.path.join(arch, os.path.basename(b))
            if not os.path.exists(dst):
                shutil.copy2(b, dst)
            lines_out = []
            for l in open(b, encoding="utf-8"):
                s = l.strip()
                if not s:
                    continue
                o = json.loads(s)
                if o.get("defect_id") in new:
                    lines_out.append(json.dumps(
                        new[o["defect_id"]], ensure_ascii=False))
                    replaced += 1
                else:
                    lines_out.append(s)
            open(b, "w", encoding="utf-8").write("\n".join(lines_out) + "\n")
        print(f"{os.path.basename(run_dir)}: replaced {replaced}/10")


if __name__ == "__main__":
    main()
