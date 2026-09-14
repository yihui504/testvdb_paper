"""1B-light aggregate: the 32 unsubmitted-anchor cases re-judged under the
actual full-stage protocol (three-valued, routing aggregation), compared
against the original A/B/D binary anchor (19/32 = 0.594)."""
import glob
import json
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = (r".paperpilot/phase2-rerun/arms/rq2_3run/anchor_fullstage")
OLD = r"C:\Users\11428\Desktop\TestVDB_artifact\rq2\analyses\unsubmitted-anchor"
CASES = json.load(open(f"{OLD}/.tmp_task2_packs_list.json", encoding="utf-8"))

is_c = lambda v: v in ("CONFIRMED", "HUMAN_REVIEW")

# --- old anchor (binary, A/B/D, force-close) --------------------------------
old = {}
for r in (1, 2, 3):
    d = {}
    for f in sorted(glob.glob(f"{OLD}/verdicts_run{r}_batch*.jsonl")):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                o = json.loads(line)
                d[o["defect_id"]] = o["verdict"]
    old[r] = d
old_maj = {c: sum(is_c(old[r].get(c)) for r in (1, 2, 3)) >= 2 for c in CASES}
old_conf = sum(old_maj.values())
print(f"OLD anchor (A/B/D binary): {old_conf}/{len(CASES)} = "
      f"{old_conf / len(CASES):.3f}   per-run "
      f"{[sum(is_c(v) for v in old[r].values()) for r in (1, 2, 3)]}")

# --- new run (full-stage v3, three-valued) ----------------------------------
new = {}
for r in (1, 2, 3):
    p = f"{OUT}/verdicts_run{r}.jsonl"
    d = {}
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            d[o["defect_id"]] = o["verdict"]
    new[r] = d
    print(f"  run{r}: {len(d)} cases  {dict(Counter(d.values()))}")

if all(len(new[r]) == len(CASES) for r in (1, 2, 3)):
    new_maj = {c: sum(is_c(new[r][c]) for r in (1, 2, 3)) >= 2 for c in CASES}
    unan = sum(1 for c in CASES
               if len({new[r][c] for r in (1, 2, 3)}) == 1)
    conf = sum(new_maj.values())
    print(f"\nNEW anchor (full-stage v3): {conf}/{len(CASES)} = "
          f"{conf / len(CASES):.3f}")
    print(f"  per-run confirmed: "
          f"{[sum(is_c(v) for v in new[r].values()) for r in (1, 2, 3)]}")
    print(f"  unanimous across runs: {unan}/{len(CASES)}")
    flips = [c for c in CASES if new_maj[c] != old_maj[c]]
    print(f"\nflips vs old anchor: {len(flips)}")
    for c in flips:
        print(f"  {c}: old={'C' if old_maj[c] else 'FP'} -> "
              f"new={[new[r][c] for r in (1, 2, 3)]}")
else:
    print("\n(incomplete: waiting for all three runs)")
