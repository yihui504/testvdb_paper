"""Problem 1A, step 1: inventory the ledger's columns for anything that can
separate the 81 adjudicated candidates by mining round / pipeline generation
(needed to replace 'whose per-generation configuration we do not itemize')."""
import sys
from collections import Counter

import openpyxl

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

wb = openpyxl.load_workbook("data/phase1_issue_classification.xlsx",
                            data_only=True)
ws = wb["issues"]
rows = list(ws.iter_rows(values_only=True))
hdr = [str(h) for h in rows[0]]
idx = {h: k for k, h in enumerate(hdr)}

scored = [r for r in rows[1:]
          if r and r[idx["gt_label"]] in ("CONFIRMED", "FALSE_POSITIVE")]
print(f"scored rows (81-pool): {len(scored)}")

for col in ("vendor", "reported_version", "group", "gt_category",
            "classification_basis", "version_source"):
    vals = Counter(str(r[idx[col]]) for r in scored)
    print(f"\n== {col}: {len(vals)} distinct ==")
    for v, n in vals.most_common(25):
        print(f"   {n:3d}  {v[:90]}")

# created_at distribution by month (submission time segments the rounds)
months = Counter(str(r[idx["created_at"]])[:7] for r in scored)
print("\n== created_at by month ==")
for m, n in sorted(months.items()):
    print(f"   {m}: {n}")
