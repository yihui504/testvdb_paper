#!/usr/bin/env python3
"""回合 2: 9 个 v2.6.16 候选（#47767 FP, #49059 TP, #49844 TP, #49889 TP, #50192 FP, #49890 TP, #50018 TP, #49930 TP, #49928 FP）"""
import requests, json, time, os, threading

BASE = "http://localhost:19530"
HEADERS = {"Authorization": "Bearer root:Milvus", "Content-Type": "application/json"}
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def log_req(log_file, label, method, url, body, resp, headers=None):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"=== {label} ===\nREQUEST: {method} {url}\n")
        if headers: f.write(f"EXTRA_HEADERS: {json.dumps(headers)}\n")
        f.write(f"BODY: {json.dumps(body, ensure_ascii=False)}\nRESPONSE: {resp.status_code} {resp.text}\n\n")

def clean(c):
    try: requests.post(f"{BASE}/v2/vectordb/collections/drop", headers=HEADERS, json={"collectionName": c}, timeout=10)
    except: pass

def setup_coll(c, schema=None, dim=4):
    if schema is None:
        schema = {"autoID": False, "enableDynamicField": True,
                  "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True},
                             {"fieldName":"vector","dataType":"FloatVector","elementTypeParams":{"dim":str(dim)}}]}
    r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json={"collectionName": c, "schema": schema})
    time.sleep(1); return r

def insert_data(c, n=3, dim=4):
    data = [{"id": i, "vector": [float(i)*0.1]*dim} for i in range(1, n+1)]
    r = requests.post(f"{BASE}/v2/vectordb/entities/insert", headers=HEADERS, json={"collectionName": c, "data": data})
    time.sleep(1); return r, data

def create_index_load(c, metric="COSINE"):
    r = requests.post(f"{BASE}/v2/vectordb/indexes/create", headers=HEADERS,
                      json={"collectionName": c, "indexParams": [{"fieldName":"vector","metricType":metric,"indexType":"AUTOINDEX"}]})
    time.sleep(2)
    r2 = requests.post(f"{BASE}/v2/vectordb/collections/load", headers=HEADERS, json={"collectionName": c})
    time.sleep(3); return r, r2

# === 5 个新候选 ===
def reproduce_47767(log_file):
    """#47767 FP by-design: empty query vector [] accepted"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #47767: empty query vector accepted\n# Ground truth: FALSE_POSITIVE (by-design)\n# Labels: resolution/by-design\n\n")
    c = "test_47767"; clean(c)
    setup_coll(c); insert_data(c); create_index_load(c)
    body = {"collectionName": c, "data": [[]], "limit": 1}  # empty vector
    r = requests.post(f"{BASE}/v2/vectordb/entities/search", headers=HEADERS, json=body)
    log_req(log_file, "SEARCH_empty_vector_BUG", "POST", "/v2/vectordb/entities/search", body, r)
    bug = r.json().get("code") == 0
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: empty vector code={r.json().get('code')}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_49059(log_file):
    """#49059 TP FIXED: cosine distance > 1.0 for identical vectors"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #49059: COSINE distance > 1.0 for identical vectors\n# Ground truth: TRUE_BUG (FIXED - may still exist in v2.6.16)\n\n")
    c = "test_49059"; clean(c)
    setup_coll(c);
    # insert 2 identical vectors
    data = [{"id":1,"vector":[1.0,2.0,3.0,4.0]},{"id":2,"vector":[1.0,2.0,3.0,4.0]}]
    requests.post(f"{BASE}/v2/vectordb/entities/insert", headers=HEADERS, json={"collectionName": c, "data": data})
    time.sleep(1); create_index_load(c, metric="COSINE")
    body = {"collectionName": c, "data": [[1.0,2.0,3.0,4.0]], "limit": 2}
    r = requests.post(f"{BASE}/v2/vectordb/entities/search", headers=HEADERS, json=body)
    log_req(log_file, "SEARCH_check_distance_BUG", "POST", "/v2/vectordb/entities/search", body, r)
    # check if any distance > 1.0
    try:
        results = r.json().get("data", {}).get("scores", []) or r.json().get("data", [])
        distances = [x.get("distance", x.get("score",0)) if isinstance(x, dict) else x for x in (results if isinstance(results, list) else [])]
        bug = any(d > 1.0 for d in distances if d is not None)
    except: bug = False
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: cosine distance > 1.0 detected\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_49844(log_file):
    """#49844 TP: query accepts null filter, returns all"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #49844: query accepts null filter, silently returns all\n# Ground truth: TRUE_BUG (triage/accepted)\n\n")
    c = "test_49844"; clean(c)
    setup_coll(c); insert_data(c); create_index_load(c)
    body = {"collectionName": c, "filter": None, "outputFields": ["id"], "limit": 10}
    r = requests.post(f"{BASE}/v2/vectordb/entities/query", headers=HEADERS, json=body)
    log_req(log_file, "QUERY_null_filter_BUG", "POST", "/v2/vectordb/entities/query", body, r)
    bug = r.json().get("code") == 0
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: null filter code={r.json().get('code')}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_49889(log_file):
    """#49889 TP: empty dbName accepted"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #49889: empty dbName accepted\n# Ground truth: TRUE_BUG (triage/accepted)\n\n")
    body = {"dbName": ""}
    r = requests.post(f"{BASE}/v2/vectordb/collections/list", headers=HEADERS, json=body)
    log_req(log_file, "LIST_empty_dbName_BUG", "POST", "/v2/vectordb/collections/list", body, r)
    bug = r.json().get("code") == 0
    # contrast: describe with empty should reject (in v2.6.16?)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: empty dbName code={r.json().get('code')}\nbug_present: {bug}\n")
    return bug

def reproduce_50192(log_file):
    """#50192 FP by-design: concurrent rename + create same name both succeed"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #50192: concurrent rename + create with same target both succeed\n# Ground truth: FALSE_POSITIVE (by-design)\n# Labels: resolution/by-design\n\n")
    c1, c2 = "test_50192_a", "test_50192_target"
    clean(c1); clean(c2)
    setup_coll(c1)
    results = {}
    def do_rename():
        r = requests.post(f"{BASE}/v2/vectordb/collections/rename", headers=HEADERS, json={"oldCollectionName": c1, "newCollectionName": c2})
        results['rename'] = r
    def do_create():
        r = setup_coll(c2)
        results['create'] = r
    t1 = threading.Thread(target=do_rename); t2 = threading.Thread(target=do_create)
    t1.start(); t2.start(); t1.join(); t2.join()
    log_req(log_file, "CONCURRENT_RENAME", "POST", "/v2/vectordb/collections/rename", {"oldCollectionName": c1, "newCollectionName": c2}, results.get('rename'))
    log_req(log_file, "CONCURRENT_CREATE", "POST", "/v2/vectordb/collections/create", {"collectionName": c2}, results.get('create'))
    rename_ok = results.get('rename').json().get("code") == 0
    create_ok = results.get('create').json().get("code") == 0
    bug = rename_ok and create_ok
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: both succeeded (rename={rename_ok}, create={create_ok})\nbug_present: {bug}\n")
    clean(c1); clean(c2); return bug

# === 4 个现有逻辑移植 ===
def reproduce_49890(log_file):
    """#49890 TP: Request-Timeout non-integer"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #49890: Request-Timeout non-integer\n# Ground truth: TRUE_BUG (FIXED)\n\n")
    bug = False
    for val in ["3.5", "abc"]:
        h = dict(HEADERS); h["Request-Timeout"] = val
        r = requests.post(f"{BASE}/v2/vectordb/collections/list", headers=h, json={})
        log_req(log_file, f"LIST_Request-Timeout={val}", "POST", "/v2/vectordb/collections/list", {}, r, {"Request-Timeout": val})
        if r.json().get("code") == 0: bug = True
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}\nbug_present: {bug}\n")
    return bug

def reproduce_50018(log_file):
    """#50018 TP: aliases/list empty collectionName"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #50018: aliases/list empty collectionName\n# Ground truth: TRUE_BUG (FIXED)\n\n")
    body = {"collectionName": "", "dbName": "default"}
    r = requests.post(f"{BASE}/v2/vectordb/aliases/list", headers=HEADERS, json=body)
    log_req(log_file, "ALIASES_LIST_empty_BUG", "POST", "/v2/vectordb/aliases/list", body, r)
    bug = r.json().get("code") == 0
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: code={r.json().get('code')}\nbug_present: {bug}\n")
    return bug

def reproduce_49930(log_file):
    """#49930 TP (in v2.6.16): efConstruction=0/-1"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #49930: negative/zero efConstruction accepted (v2.6.16 should be bug)\n# Ground truth: TRUE_BUG (in v2.6.16; fixed in v2.6.17)\n\n")
    c = "test_49930"; clean(c); setup_coll(c)
    bug = False
    for ef in [0, -1]:
        body = {"collectionName": c, "indexParams": [{"fieldName":"vector","metricType":"COSINE","indexType":"HNSW","params":{"M":16,"efConstruction":ef}}]}
        r = requests.post(f"{BASE}/v2/vectordb/indexes/create", headers=HEADERS, json=body)
        log_req(log_file, f"INDEX_efConstruction={ef}_BUG", "POST", "/v2/vectordb/indexes/create", body, r)
        if r.json().get("code") == 0: bug = True
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_49928(log_file):
    """#49928 FP by-design: 32768-dim"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #49928: 32768-dim collection without warning\n# Ground truth: FALSE_POSITIVE (by-design)\n# Labels: resolution/by-design\n\n")
    c = "test_49928"; clean(c)
    body = {"collectionName": c, "dimension": 32768}
    r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json=body)
    log_req(log_file, "CREATE_dim=32768_BUG", "POST", "/v2/vectordb/collections/create", body, r)
    bug = r.json().get("code") == 0
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: code={r.json().get('code')}\nbug_present: {bug}\n")
    clean(c); return bug

def main():
    print("Round 2: 9 v2.6.16 candidates")
    fns = [('47767', reproduce_47767), ('49059', reproduce_49059), ('49844', reproduce_49844),
           ('49889', reproduce_49889), ('50192', reproduce_50192), ('49890', reproduce_49890),
           ('50018', reproduce_50018), ('49930', reproduce_49930), ('49928', reproduce_49928)]
    results = {}
    for num, fn in fns:
        try:
            results[num] = fn(os.path.join(OUT_DIR, f"output_{num}.log"))
            print(f"  #{num}: bug_present={results[num]}")
        except Exception as e:
            results[num] = f"ERROR: {e}"
            print(f"  #{num}: {results[num]}")
    print("\nSummary:")
    for num, v in results.items():
        print(f"  #{num}: {'BUG EXISTS' if v is True else 'NOT REPRODUCED' if v is False else v}")

if __name__ == "__main__":
    main()
