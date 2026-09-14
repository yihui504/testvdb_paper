"""Debug: why does run_donly* load to only 20 confirmations when the paper's
source-only majority is 44 (36 TP + 8 leak)?"""
import glob
import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))

for run in ("run_donly1", "run_donly2", "run_donly3"):
    files = sorted(glob.glob(f"{ROOT}/rerun_v3/{run}/verdicts_batch*.jsonl"))
    print(f"== {run}: {len(files)} file(s) ==")
    d = {}
    for f in files:
        n_lines = 0
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            n_lines += 1
            try:
                o = json.loads(l)
            except json.JSONDecodeError:
                continue
            if o.get("defect_id"):
                d[o["defect_id"]] = o["verdict"]
        print(f"   {f.split('/')[-1]}: {n_lines} lines")
    print(f"   cases: {len(d)}; verdict histogram: "
          f"{dict(Counter(d.values()))}")
    conf = sum(1 for i in d if d[i] == "CONFIRMED" and GT.get(i) == "T")
    print(f"   CONFIRMED majority on true bugs: {conf}")

# cross-check: the majority_fullstage_cleaned.json / majority_verdicts.json
for f in ("majority_verdicts.json", "majority_fullstage.json",
          "majority_fullstage_cleaned.json"):
    try:
        o = json.load(open(f"{ROOT}/{f}", encoding="utf-8"))
        if isinstance(o, dict):
            keys = list(o)[:3]
            print(f"\n{f}: {len(o)} entries, sample keys {keys}")
    except Exception as e:
        print(f"\n{f}: {e}")
