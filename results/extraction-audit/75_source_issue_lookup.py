"""Trace the 6 cases the blind pass flagged as 'probe never exercised the
claimed path' back to their source issues."""
import sys

import openpyxl

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CASES = ["milvus_010", "milvus_027", "milvus_033", "milvus_036",
         "milvus_038", "milvus_043"]

wb = openpyxl.load_workbook("data/phase1_issue_classification.xlsx",
                            data_only=True)
ws = wb["issues"]
rows = list(ws.iter_rows(values_only=True))
hdr = [str(h) for h in rows[0]]
idx = {h: k for k, h in enumerate(hdr)}

# defect_id -> issue number mapping: check the index files
import json
try:
    m = json.load(open(".paperpilot/phase2-rerun/defect_id_map.json",
                       encoding="utf-8"))
    print("defect_id_map.json entries:", len(m))
    for c in CASES:
        print(f"  {c} -> {m.get(c, 'NOT FOUND')}")
except FileNotFoundError:
    print("(no defect_id_map.json)")

print("\n--- by title keyword search in ledger ---")
for c in CASES:
    print(f"{c}: ", end="")
    for r in rows[1:]:
        if not r:
            continue
        blob = " ".join(str(v) for v in r if v is not None)
        if c in blob:
            print(f"found in ledger row: {r[idx['vendor']]} "
                  f"#{r[idx['number']]} | {str(r[idx['title']])[:60]}")
            break
    else:
        print("(not in ledger by id)")
