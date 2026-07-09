#!/usr/bin/env python3
"""回合 B: v2.6.17 新 4 个（#50324 TP, #50321/50322/50325 FP）"""
import requests, json, time, os
BASE = "http://localhost:19530"
HEADERS = {"Authorization": "Bearer root:Milvus", "Content-Type": "application/json"}
OUT = os.path.dirname(os.path.abspath(__file__))

def log_req(lf, label, body, resp):
    with open(lf, 'a', encoding='utf-8') as f:
        f.write(f"=== {label} ===\nBODY: {json.dumps(body, ensure_ascii=False)[:200]}\nRESPONSE: {resp.status_code} {resp.text}\n\n")

def clean(c):
    try: requests.post(f"{BASE}/v2/vectordb/collections/drop", headers=HEADERS, json={"collectionName": c}, timeout=10)
    except: pass

def setup(c):
    r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json={"collectionName": c, "schema": {"autoID": False, "enableDynamicField": True, "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True},{"fieldName":"vector","dataType":"FloatVector","elementTypeParams":{"dim":"4"}}]}})
    time.sleep(1); return r

def reproduce_50324(lf):
    """#50324 TP: insert accepts 101 entities (exceeds documented REST max 100?)"""
    open(lf,'w',encoding='utf-8').write("# Issue #50324: insert accepts 101 entities\n# Ground truth: TRUE_BUG (FIXED, triage/accepted)\n# Test version: v2.6.17\n\n")
    c="t50324"; clean(c); setup(c)
    data=[{"id":i,"vector":[float(i)*0.01]*4} for i in range(1,102)]  # 101 entities
    body={"collectionName": c, "data": data}
    r=requests.post(f"{BASE}/v2/vectordb/entities/insert", headers=HEADERS, json=body)
    log_req(lf, "INSERT_101_entities", body, r)
    bug=r.json().get("code")==0
    with open(lf,'a',encoding='utf-8') as f: f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: insert 101 code={r.json().get('code')}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_50321(lf):
    """#50321 FP: duplicate collection creation returns code=0 (idempotent by-design)"""
    open(lf,'w',encoding='utf-8').write("# Issue #50321: duplicate collection creation returns code=0\n# Ground truth: FALSE_POSITIVE (by-design, idempotent)\n# Labels: kind/bug, resolution/by-design\n# Test version: v2.6.17\n\n")
    c="t50321"; clean(c); setup(c)
    # create again (duplicate)
    body={"collectionName": c, "dimension": 4}
    r=requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json=body)
    log_req(lf, "CREATE_duplicate", body, r)
    bug=r.json().get("code")==0
    with open(lf,'a',encoding='utf-8') as f: f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: duplicate create code={r.json().get('code')} (by-design idempotent)\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_50322(lf):
    """#50322 FP: drop non-existent collection returns code=0 (idempotent by-design)"""
    open(lf,'w',encoding='utf-8').write("# Issue #50322: drop non-existent collection returns code=0\n# Ground truth: FALSE_POSITIVE (by-design, idempotent)\n# Labels: kind/bug, resolution/by-design\n# Test version: v2.6.17\n\n")
    c="t50322_nonexistent"
    clean(c)  # ensure not exist
    body={"collectionName": c}
    r=requests.post(f"{BASE}/v2/vectordb/collections/drop", headers=HEADERS, json=body)
    log_req(lf, "DROP_nonexistent", body, r)
    bug=r.json().get("code")==0
    with open(lf,'a',encoding='utf-8') as f: f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: drop nonexistent code={r.json().get('code')} (by-design idempotent)\nbug_present: {bug}\n")
    return bug

def reproduce_50325(lf):
    """#50325 FP: collection names with leading underscore accepted (by-design)"""
    open(lf,'w',encoding='utf-8').write("# Issue #50325: collection names with leading underscore accepted\n# Ground truth: FALSE_POSITIVE (by-design)\n# Labels: kind/bug, resolution/by-design\n# Test version: v2.6.17\n\n")
    c="_t50325_underscore"
    clean(c)
    body={"collectionName": c, "dimension": 4}
    r=requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json=body)
    log_req(lf, "CREATE_leading_underscore", body, r)
    bug=r.json().get("code")==0
    clean(c)
    with open(lf,'a',encoding='utf-8') as f: f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: underscore name code={r.json().get('code')} (by-design allowed)\nbug_present: {bug}\n")
    return bug

def main():
    print("Round B: v2.6.17 new 4 candidates")
    for num, fn in [('50324', reproduce_50324), ('50321', reproduce_50321), ('50322', reproduce_50322), ('50325', reproduce_50325)]:
        try:
            bug = fn(os.path.join(OUT, f"output_{num}.log"))
            print(f"  #{num}: bug_present={bug}")
        except Exception as e:
            print(f"  #{num}: ERROR {e}")

if __name__ == "__main__":
    main()
