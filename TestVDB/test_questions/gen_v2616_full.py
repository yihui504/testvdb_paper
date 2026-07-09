#!/usr/bin/env python3
"""回合 A: v2.6.16 组 15 个候选（7 新 + 8 复用 gen_v2616）"""
import requests, json, time, os, threading
BASE = "http://localhost:19530"
HEADERS = {"Authorization": "Bearer root:Milvus", "Content-Type": "application/json"}
OUT = os.path.dirname(os.path.abspath(__file__))

def log_req(lf, label, m, u, body, resp, h=None):
    with open(lf, 'a', encoding='utf-8') as f:
        f.write(f"=== {label} ===\nREQUEST: {m} {u}\n")
        if h: f.write(f"EXTRA_HEADERS: {json.dumps(h)}\n")
        f.write(f"BODY: {json.dumps(body, ensure_ascii=False)}\nRESPONSE: {resp.status_code} {resp.text}\n\n")

def clean(c):
    try: requests.post(f"{BASE}/v2/vectordb/collections/drop", headers=HEADERS, json={"collectionName": c}, timeout=10)
    except: pass

def setup(c, schema=None, dim=4):
    if schema is None:
        schema = {"autoID": False, "enableDynamicField": True,
                  "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True},
                             {"fieldName":"vector","dataType":"FloatVector","elementTypeParams":{"dim":str(dim)}}]}
    r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json={"collectionName": c, "schema": schema})
    time.sleep(1); return r

def insert(c, n=3, dim=4):
    data = [{"id": i, "vector": [float(i)*0.1]*dim} for i in range(1, n+1)]
    r = requests.post(f"{BASE}/v2/vectordb/entities/insert", headers=HEADERS, json={"collectionName": c, "data": data})
    time.sleep(1); return r

def idx_load(c, metric="COSINE"):
    requests.post(f"{BASE}/v2/vectordb/indexes/create", headers=HEADERS, json={"collectionName": c, "indexParams": [{"fieldName":"vector","metricType":metric,"indexType":"AUTOINDEX"}]})
    time.sleep(2); requests.post(f"{BASE}/v2/vectordb/collections/load", headers=HEADERS, json={"collectionName": c}); time.sleep(3)

# === 7 个新函数 ===
def reproduce_47729(lf):
    """#47729 TP: nprobe validation missing (IVF)"""
    open(lf,'w',encoding='utf-8').write("# Issue #47729: nprobe validation missing\n# Ground truth: TRUE_BUG (FIXED, triage/accepted)\n# Test version: v2.6.16 (original v2.6.10)\n\n")
    c="t47729"; clean(c); setup(c); insert(c)
    # create IVF index, then search with invalid nprobe
    requests.post(f"{BASE}/v2/vectordb/indexes/create", headers=HEADERS, json={"collectionName": c, "indexParams": [{"fieldName":"vector","metricType":"L2","indexType":"IVF_FLAT","params":{"nlist":128}}]})
    time.sleep(2); requests.post(f"{BASE}/v2/vectordb/collections/load", headers=HEADERS, json={"collectionName": c}); time.sleep(3)
    bug=False
    for np_val in [-1, 0, 999999]:
        body={"collectionName": c, "data": [[0.1,0.2,0.3,0.4]], "limit": 1, "searchParams": {"params": {"nprobe": np_val}}}
        r=requests.post(f"{BASE}/v2/vectordb/entities/search", headers=HEADERS, json=body)
        log_req(lf, f"SEARCH_nprobe={np_val}", "POST", "/v2/vectordb/entities/search", body, r)
        if r.json().get("code")==0: bug=True
    with open(lf,'a',encoding='utf-8') as f: f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_47752(lf):
    """#47752 TP: ef validation missing (HNSW)"""
    open(lf,'w',encoding='utf-8').write("# Issue #47752: ef validation missing\n# Ground truth: TRUE_BUG (FIXED)\n# Test version: v2.6.16 (original v2.6.10)\n\n")
    c="t47752"; clean(c); setup(c)
    bug=False
    for ef in [-1, 0]:
        body={"collectionName": c, "indexParams": [{"fieldName":"vector","metricType":"COSINE","indexType":"HNSW","params":{"M":16,"efConstruction":ef}}]}
        r=requests.post(f"{BASE}/v2/vectordb/indexes/create", headers=HEADERS, json=body)
        log_req(lf, f"INDEX_efConstruction={ef}", "POST", "/v2/vectordb/indexes/create", body, r)
        if r.json().get("code")==0: bug=True
    with open(lf,'a',encoding='utf-8') as f: f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_47755(lf):
    """#47755 TP: filter expression too lenient"""
    open(lf,'w',encoding='utf-8').write("# Issue #47755: filter expression too lenient\n# Ground truth: TRUE_BUG (FIXED)\n# Test version: v2.6.16 (original v2.6.10)\n\n")
    c="t47755"; clean(c)
    schema={"autoID": False, "enableDynamicField": True, "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True},{"fieldName":"vector","dataType":"FloatVector","elementTypeParams":{"dim":"4"}},{"fieldName":"age","dataType":"Int64"}]}
    setup(c, schema=schema)
    requests.post(f"{BASE}/v2/vectordb/entities/insert", headers=HEADERS, json={"collectionName": c, "data": [{"id":1,"vector":[0.1,0.2,0.3,0.4],"age":25},{"id":2,"vector":[0.2,0.3,0.4,0.5],"age":30}]})
    time.sleep(1); idx_load(c)
    bug=False
    for filt in ["", "1==1", "invalid_syntax!!!"]:
        body={"collectionName": c, "data": [[0.1,0.2,0.3,0.4]], "limit": 10, "filter": filt}
        r=requests.post(f"{BASE}/v2/vectordb/entities/search", headers=HEADERS, json=body)
        log_req(lf, f"SEARCH_filter={filt!r}", "POST", "/v2/vectordb/entities/search", body, r)
        if r.json().get("code")==0: bug=True
    with open(lf,'a',encoding='utf-8') as f: f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_47763(lf):
    """#47763 TP: field name validation missing"""
    open(lf,'w',encoding='utf-8').write("# Issue #47763: field name validation missing\n# Ground truth: TRUE_BUG (FIXED)\n# Test version: v2.6.16 (original v2.6.10)\n\n")
    c="t47763"; clean(c)
    bug=False
    for fname in ["", "123numeric", "field with space"]:
        schema={"autoID": False, "enableDynamicField": True, "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True},{"fieldName":fname,"dataType":"FloatVector","elementTypeParams":{"dim":"4"}}]}
        r=requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json={"collectionName": f"{c}_{fname[:5]}", "schema": schema})
        log_req(lf, f"CREATE_fieldName={fname!r}", "POST", "/v2/vectordb/collections/create", {"fieldName": fname}, r)
        if r.json().get("code")==0: bug=True
        try: requests.post(f"{BASE}/v2/vectordb/collections/drop", headers=HEADERS, json={"collectionName": f"{c}_{fname[:5]}"}, timeout=5)
        except: pass
    with open(lf,'a',encoding='utf-8') as f: f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}\nbug_present: {bug}\n")
    return bug

def reproduce_47766(lf):
    """#47766 TP: data type validation missing"""
    open(lf,'w',encoding='utf-8').write("# Issue #47766: data type validation missing\n# Ground truth: TRUE_BUG (FIXED)\n# Test version: v2.6.16 (original v2.6.10)\n\n")
    c="t47766"; clean(c); setup(c)
    # insert with wrong data type (string instead of float vector)
    body={"collectionName": c, "data": [{"id":1, "vector": "not_an_array"}]}
    r=requests.post(f"{BASE}/v2/vectordb/entities/insert", headers=HEADERS, json=body)
    log_req(lf, "INSERT_wrong_type", "POST", "/v2/vectordb/entities/insert", body, r)
    bug = r.json().get("code")==0
    with open(lf,'a',encoding='utf-8') as f: f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_49843(lf):
    """#49843 TP: negative collection name silently dropped"""
    open(lf,'w',encoding='utf-8').write("# Issue #49843: negative collection name silently dropped\n# Ground truth: TRUE_BUG (FIXED)\n# Test version: v2.6.16\n\n")
    bug=False
    for name in ["-1", "-100", "col-1"]:
        r=requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json={"collectionName": name, "dimension": 4})
        log_req(lf, f"CREATE_name={name!r}", "POST", "/v2/vectordb/collections/create", {"collectionName": name}, r)
        if r.json().get("code")==0: bug=True
        try: requests.post(f"{BASE}/v2/vectordb/collections/drop", headers=HEADERS, json={"collectionName": name}, timeout=5)
        except: pass
    with open(lf,'a',encoding='utf-8') as f: f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}\nbug_present: {bug}\n")
    return bug

def reproduce_49929(lf):
    """#49929 FP: REST API and PyMilvus SDK inconsistent (by-design)"""
    open(lf,'w',encoding='utf-8').write("# Issue #49929: REST API and PyMilvus SDK have inconsistent behavior\n# Ground truth: FALSE_POSITIVE (by-design)\n# Labels: resolution/by-design\n# Test version: v2.6.16\n\n")
    c="t49929"; clean(c); setup(c); insert(c); idx_load(c)
    # REST search (default consistency) - behavior is by-design different from SDK
    body={"collectionName": c, "data": [[0.1,0.2,0.3,0.4]], "limit": 1}
    r=requests.post(f"{BASE}/v2/vectordb/entities/search", headers=HEADERS, json=body)
    log_req(lf, "REST_search_default_consistency", "POST", "/v2/vectordb/entities/search", body, r)
    # by-design: REST uses Bounded consistency by default, SDK uses Strong - difference is intentional
    bug = r.json().get("code")==0  # REST returns results (by-design behavior)
    with open(lf,'a',encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: REST returns code={r.json().get('code')} (by-design Bounded consistency vs SDK Strong)\nbug_present: {bug}\n")
    clean(c); return bug

def main():
    print("Round A: v2.6.16 group, 7 new candidates")
    fns = [('47729', reproduce_47729), ('47752', reproduce_47752), ('47755', reproduce_47755),
           ('47763', reproduce_47763), ('47766', reproduce_47766), ('49843', reproduce_49843), ('49929', reproduce_49929)]
    for num, fn in fns:
        try:
            bug = fn(os.path.join(OUT, f"output_{num}.log"))
            print(f"  #{num}: bug_present={bug}")
        except Exception as e:
            print(f"  #{num}: ERROR {e}")

if __name__ == "__main__":
    main()
