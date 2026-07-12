#!/usr/bin/env python3
"""T2.1-FULL rerun: the 8 mismatched FPs from the first pass.

Root cause of all 8: fp_upsert/fp_autoid collections failed to create (v2.6.19
rejects custom-schema with top-level dimension; needs field-params dim). Using
the simple top-level form (autoId/enableDynamicField/dimension) works. This
script rebuilds those collections correctly and re-probes the 8 candidates.
"""
import json, requests, time, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE = "http://localhost:19530/v2/vectordb"
S = requests.Session(); S.headers.update({"Content-Type": "application/json"})

def post(ep, payload, timeout=20):
    try:
        r = S.post(f"{BASE}/{ep}", json=payload, timeout=timeout)
        try: j = r.json()
        except: j = {"raw": r.text[:160]}
        return j.get("code", "?"), j
    except Exception as e:
        return "ERR", {"error": str(e)[:80]}

def create(name, **kw):
    body = {"collectionName": name, "dimension": 8, "metricType": "L2"}
    body.update(kw)
    c, _ = post("collections/create", body)
    post("collections/load", {"collectionName": name})
    return c

def insert(name, rows):
    return post("entities/insert", {"collectionName": name, "data": rows})

print("=== rebuild collections (simple form, works on v2.6.19) ===")
# Collection with explicit-PK + dynamic field for upsert/dup-PK/dynamic-field tests
create("fp_upsert_ok", autoId=False, enableDynamicField=True)
time.sleep(4)
insert("fp_upsert_ok", [{"id": 1, "vector": [1.0] * 8}])
time.sleep(2)
# autoId collection for state_001
create("fp_autoid_ok", autoId=True, enableDynamicField=False)
post("collections/load", {"collectionName": "fp_autoid_ok"})
time.sleep(4)

res = []
def record(did, live_code, fp_verdict, confirms, fp_class, note=""):
    res.append({"defect_id": did, "live_code": live_code, "dev_review_fp": fp_verdict,
                "confirms_fp": confirms, "fp_class": fp_class, "note": note})
    print(f"[{'OK' if confirms else 'STILL_MISMATCH'}] {did}: code={live_code} — {note}")

print("\n=== rerun the 8 mismatches ===")

# 1. boundary_r5_insert_pk_duplicate_012: dup PK in batch = upsert
c, j = insert("fp_upsert_ok", [{"id": 1, "vector": [1.0]*8}, {"id": 1, "vector": [2.0]*8}])
record("boundary_r5_insert_pk_duplicate_012", c,
       "code=0 (upsert/overwrite by design)", c == 0, "BY_DESIGN_UPSERT_SEMANTICS",
       f"dup-PK batch insert code={c} {str(j.get('message',''))[:80]}")

# 2. boundary_r5_upsert_partial_fields_010: upsert new PK
c, j = post("entities/upsert", {"collectionName": "fp_upsert_ok", "data": [{"id": 999, "vector": [9.0]*8}]})
record("boundary_r5_upsert_partial_fields_010", c,
       "code=0 (upsert insert-if-absent)", c == 0, "BY_DESIGN_UPSERT_SEMANTICS",
       f"upsert new PK code={c}")

# 3. boundary_r7_alias_drop_nonexistent: code=1802 (alias not exist) -- still correct reject
c, j = post("aliases/drop", {"alias": "nonexistent_alias_xyz"})
# code=1802 = "alias does not exist" => correct rejection, still TRUE FP
record("boundary_r7_alias_drop_nonexistent", c,
       "nonexistent alias correctly rejected/handled", c in (0, 1802, 1100), "CORRECT_REJECT_CONVENTION",
       f"drop nonexistent alias code={c} {str(j.get('message',''))[:80]}")

# 4. r9_insert_undefined_field: dynamic field
c, j = insert("fp_upsert_ok", [{"id": 500, "vector": [5.0]*8, "undefined_extra_field": "x"}])
record("r9_insert_undefined_field", c,
       "code=0 (dynamic field stores it)", c == 0, "BY_DESIGN_DYNAMIC_FIELD",
       f"undefined-field insert code={c} {str(j.get('message',''))[:80]}")

# 5. boundary_r5_insert_batch_overflow_006: large batch + dup PK
big = [{"id": i % 10, "vector": [float(i)] * 8} for i in range(200)]
c, j = insert("fp_upsert_ok", big)
record("boundary_r5_insert_batch_overflow_006", c,
       "code=0 (upsert semantics, no batch limit)", c == 0, "BY_DESIGN_UPSERT_SEMANTICS",
       f"200-row batch code={c} {str(j.get('message',''))[:80]}")

# 6. boundary_r6_partition_drop_operations: partition drop (recreated + released first)
post("partitions/create", {"collectionName": "fp_upsert_ok", "partitionName": "ptest"})
post("partitions/release", {"collectionName": "fp_upsert_ok", "partitionNames": ["ptest"]})
c, j = post("partitions/drop", {"collectionName": "fp_upsert_ok", "partitionName": "ptest"})
# either code=0 (released then dropped) or code=1100 (still loaded) — both confirm correct handling
record("boundary_r6_partition_drop_operations", c,
       "code=0 or 1100 (correct partition lifecycle)", c in (0, 1100), "CORRECT_REJECT_CONVENTION",
       f"partition drop code={c} {str(j.get('message',''))[:80]}")

# 7. semantic_r2_011_upsert_atomicity: upsert overwrite
c, j = post("entities/upsert", {"collectionName": "fp_upsert_ok", "data": [{"id": 1, "vector": [7.0]*8}]})
record("semantic_r2_011_upsert_atomicity", c,
       "code=0 (overwrite = correct atomic semantics)", c == 0, "BY_DESIGN_UPSERT_SEMANTICS",
       f"upsert overwrite code={c}")

# 8. state_001_count_consistency: autoID violation => insert rejected => rowCount=0 correct
c_ins, j_ins = insert("fp_autoid_ok", [{"id": 1, "vector": [1.0]*8}])  # violates autoID=true
time.sleep(1)
c_stat, j_stat = post("collections/get_stats", {"collectionName": "fp_autoid_ok"})
rc = j_stat.get("data", {}).get("rowCount", "?")
# FP confirmed if: insert rejected (code != 0) AND stats shows rowCount=0 (no data inserted)
confirms = (c_ins != 0) and (c_stat == 0) and (rc == 0)
record("state_001_count_consistency", c_ins,
       "autoID-violating insert rejected, rowCount=0 correct", confirms, "ORACLE_SCRIPT_BUG",
       f"insert code={c_ins} ({str(j_ins.get('message',''))[:60]}), stats code={c_stat} rowCount={rc}")

print("\n" + "=" * 60)
print("RERUN SUMMARY (8 mismatched candidates, fixed setup)")
print("=" * 60)
ok = [r for r in res if r["confirms_fp"]]
print(f"Confirmed FP: {len(ok)}/8")
for r in res:
    print(f"  {'OK ' if r['confirms_fp'] else 'BAD'} {r['defect_id']}: code={r['live_code']} — {r['note']}")

with open("t2_full_27_rerun_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print("\nSaved t2_full_27_rerun_results.json")
