"""Full ledger rows for the three group-by issues, to check whether the
classification basis agrees with the maintainers' comments on the issues."""
import sys

import openpyxl

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NUMS = {52309: "milvus_036", 52311: "milvus_038", 52325: "milvus_043",
        49843: "milvus_010", 51085: "milvus_033", 50351: "milvus_027"}

wb = openpyxl.load_workbook("data/phase1_issue_classification.xlsx",
                            data_only=True)
rows = list(wb["issues"].iter_rows(values_only=True))
hdr = [str(h) for h in rows[0]]
idx = {h: k for k, h in enumerate(hdr)}

for n, case in NUMS.items():
    for r in rows[1:]:
        if not r or r[idx["number"]] != n:
            continue
        print(f"===== {case}  #{n} =====")
        for col in ("title", "state", "state_reason", "gt_category",
                    "group", "gt_label", "classification_basis",
                    "dev_reviewer_verdict", "dev_reviewer_confidence"):
            v = r[idx[col]]
            print(f"  {col}: {str(v)[:300]}")
        print()
        break
