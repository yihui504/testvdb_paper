"""Locate the 32-candidate anchor re-adjudication: hunt for verdict files with
~32 entries whose case ids are NOT in the 81-pool."""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

POOL = set(json.load(open(
    ".paperpilot/phase2-rerun/arms/rq2_3run/gt_81.json",
    encoding="utf-8")).keys())
print(f"81-pool ids: {len(POOL)}")

ROOTS = [
    r".paperpilot/phase2-rerun",
    r"C:\Users\11428\.claude\plugins\cache\testvdb\testvdb",
    r"C:\Users\11428\Desktop\mftui\TestVDB",
    r"C:\Users\11428\Desktop\tvdb_sessions",
]

hits = []
for root in ROOTS:
    if not os.path.isdir(root):
        continue
    for path in glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True):
        if "site-packages" in path or ".git" in path:
            continue
        try:
            if os.path.getsize(path) > 30_000_000:
                continue
            ids = set()
            for line in open(path, encoding="utf-8", errors="replace"):
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    ids = set()
                    break
                for k in ("defect_id", "case", "candidate", "id"):
                    if isinstance(o, dict) and o.get(k):
                        ids.add(o[k])
                        break
            if 25 <= len(ids) <= 40:
                outside = ids - POOL
                hits.append((path, len(ids), len(outside)))
        except OSError:
            continue

hits.sort(key=lambda t: -t[2])
print(f"\nfiles with 25-40 ids: {len(hits)}")
for path, n, outside in hits[:25]:
    print(f"  ids={n:3d}  outside-pool={outside:3d}  {path}")
