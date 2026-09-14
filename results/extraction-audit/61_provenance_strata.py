"""Problem 1A, step 2: the per-generation provenance table. Strata = mining
target (vendor + reported version, the same key the paper's tested-versions
list uses), with submission month as the time axis. Output is the itemized
breakdown that replaces 'whose per-generation configuration we do not
itemize'."""
import sys
from collections import Counter, defaultdict

import openpyxl

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

wb = openpyxl.load_workbook("data/phase1_issue_classification.xlsx",
                            data_only=True)
ws = wb["issues"]
rows = list(ws.iter_rows(values_only=True))
hdr = [str(h) for h in rows[0]]
idx = {h: k for k, h in enumerate(hdr)}

pool = []
for r in rows[1:]:
    if not r or r[idx["gt_label"]] not in ("CONFIRMED", "FALSE_POSITIVE"):
        continue
    if str(r[idx["vendor"]]) == "meilisearch":
        continue
    pool.append(r)
print(f"81-pool: {len(pool)}")

targets = defaultdict(lambda: {"n": 0, "conf": 0, "fp": 0, "months": []})
for r in pool:
    v = str(r[idx["vendor"]])
    ver = str(r[idx["reported_version"]])
    conf = r[idx["gt_label"]] == "CONFIRMED"
    month = str(r[idx["created_at"]])[:7]
    t = targets[(v, ver)]
    t["n"] += 1
    t["conf" if conf else "fp"] += 1
    t["months"].append(month)

print(f"\nmining targets (vendor x reported version): {len(targets)}")
print(f"{'target':22s} {'n':>3s} {'conf':>5s} {'fp':>3s}  months")
for (v, ver), t in sorted(targets.items(),
                          key=lambda kv: (-kv[1]["n"], kv[0])):
    ms = sorted(set(t["months"]))
    print(f"{v + ' ' + ver:22s} {t['n']:3d} {t['conf']:5d} {t['fp']:3d}  "
          f"{ms[0]}..{ms[-1]} ({len(t['months'])})")

# per-vendor version span and totals
print("\nper-vendor:")
for v in ("milvus", "qdrant", "weaviate"):
    vs = {k[1]: t for k, t in targets.items() if k[0] == v}
    n = sum(t["n"] for t in vs.values())
    c = sum(t["conf"] for t in vs.values())
    print(f"  {v:10s} {len(vs)} versions, {n} submissions, {c} confirmed; "
          f"versions: {', '.join(sorted(vs))}")

# monthly totals
months = Counter(str(r[idx["created_at"]])[:7] for r in pool)
print("\nmonthly:", dict(sorted(months.items())))

# how many confirmed bugs sit in targets mined on only one version each
singles = [k for k, t in targets.items() if t["n"] <= 2]
print(f"\ntargets with <=2 submissions: {len(singles)} "
      f"(long tail of one-off mining sessions)")
