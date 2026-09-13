"""Generate cognition-strip re-judge dispatches for the affected runs.

v3 runs list cases as `- milvus_XXX: pack=... | source=...` lines; the v2
core dispatch lists bare pack paths. Both are handled. For each run, the
re-judge dispatch is that run's batch1 dispatch with the case/material list
reduced to the 10 cognition-stripped packs and the output path pointed at
verdicts_rejudge_cog.jsonl; protocol text stays verbatim.
"""
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R3 = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
      r"arms/rq2_3run/rerun_v3")
V2 = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
      r"arms/rq2_3run/rerun_v2")
MAT = (r"c:\Users\11428\Desktop\testvdb_paper\.paperpilot\phase2-rerun"
       r"\arms\materials_complete")

TARGETS = ["milvus_010", "milvus_014", "milvus_018", "milvus_019",
           "milvus_022", "milvus_026", "milvus_027", "milvus_028",
           "milvus_032", "milvus_033"]

RUNS = ([f"{V2}/run{i}" for i in (1, 2, 3)] +
        [f"{R3}/{r}" for r in ("run_flat1", "run_flat2", "run_flat3",
                               "run_donly1", "run_donly2", "run_donly3",
                               "run_donlyq1", "run_donlyq2", "run_donlyq3",
                               "run_flatq1")])

V3_LINE = re.compile(r"^- (milvus_\d{3}): .*$")
V2_LINE = re.compile(r"^c:.*materials_complete[\\\\/](milvus_\d{3})\.md$")


def case_id(ln: str):
    m = V3_LINE.match(ln)
    if m:
        return m.group(1), "v3"
    m = V2_LINE.match(ln)
    if m:
        return m.group(1), "v2"
    return None, None


def main():
    for run_dir in RUNS:
        batches = sorted(glob.glob(run_dir + "/batch*_dispatch.txt"))
        assert batches, run_dir
        want = set(TARGETS)
        lines_by_case, fmt = {}, None
        for b in batches:
            for ln in open(b, encoding="utf-8"):
                cid, f = case_id(ln.rstrip("\n"))
                if cid in want:
                    lines_by_case[cid] = ln.rstrip("\n")
                    fmt = f
        missing = want - set(lines_by_case)
        assert not missing, f"{run_dir}: missing {missing}"

        base = open(batches[0], encoding="utf-8").read()
        lines = base.split("\n")
        idx = [i for i, ln in enumerate(lines) if case_id(ln)[0]]
        new_lines = (lines[:idx[0]]
                     + [lines_by_case[c] for c in TARGETS]
                     + lines[idx[-1] + 1:])
        out = "\n".join(new_lines)
        out = re.sub(r"verdicts_batch\d+\.jsonl",
                     "verdicts_rejudge_cog.jsonl", out)
        n = sum(1 for ln in out.split("\n") if case_id(ln)[0])
        assert n == 10 and "rejudge_cog" in out, (run_dir, n)
        open(os.path.join(run_dir, "rejudge_cog_dispatch.txt"), "w",
             encoding="utf-8").write(out)
        print(f"{os.path.basename(run_dir)} [{fmt}]: 10 cases, ok")


if __name__ == "__main__":
    main()
