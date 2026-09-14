"""Inventory the 32-candidate unsubmitted anchor: case list, batch layout,
and the per-run/majority verdicts that produced 19/32 = 0.594."""
import glob
import json
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

A = r"C:\Users\11428\Desktop\TestVDB_artifact\rq2\analyses\unsubmitted-anchor"
POOL = set(json.load(open(
    ".paperpilot/phase2-rerun/arms/rq2_3run/gt_81.json",
    encoding="utf-8")).keys())

print("=== map / packs list ===")
for f in (".tmp_task2_map.json", ".tmp_task2_packs_list.json"):
    p = os.path.join(A, f)
    if os.path.exists(p):
        o = json.load(open(p, encoding="utf-8"))
        print(f"{f}: {type(o).__name__}, "
              f"{len(o) if hasattr(o, '__len__') else ''}")
        print("   ", str(o)[:400])

print("\n=== packs ===")
packs = sorted(os.listdir(os.path.join(A, "packs")))
print(f"{len(packs)} files; first 5: {packs[:5]}")

print("\n=== verdicts, per run ===")
runs = {}
for r in (1, 2, 3):
    d = {}
    for f in sorted(glob.glob(os.path.join(A, f"verdicts_run{r}_batch*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            key = o.get("defect_id") or o.get("case") or o.get("id")
            if key:
                d[key] = o.get("verdict") or o.get("ruling")
    runs[r] = d
    print(f"  run{r}: {len(d)} cases, "
          f"{dict(Counter(d.values()))}")

ids = sorted(set().union(*[set(d) for d in runs.values()]))
print(f"\nunion of case ids: {len(ids)}")
print("ids:", ids)
outside = [i for i in ids if i not in POOL]
print(f"\noutside the 81-pool: {len(outside)} -> {outside}")
inside = [i for i in ids if i in POOL]
print(f"inside the 81-pool: {len(inside)} -> {inside}")

is_c = lambda v: v in ("CONFIRMED", "HUMAN_REVIEW")
maj = {i: sum(is_c(runs[r].get(i, "")) for r in (1, 2, 3)) >= 2 for i in ids}
conf = [i for i in ids if maj[i]]
print(f"\nmajority-confirmed: {len(conf)}/{len(ids)} = "
      f"{len(conf) / len(ids):.3f}")
unan = [i for i in ids
        if len({runs[r].get(i) for r in (1, 2, 3)}) == 1]
print(f"unanimous across runs: {len(unan)}")
