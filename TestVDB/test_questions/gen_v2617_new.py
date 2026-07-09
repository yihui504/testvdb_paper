#!/usr/bin/env python3
"""回合 1: 6 个新 v2.6.17 候选复现（#50319 FP, #50323 TP, #50352 FP, #50353 TP, #50354 TP, #50355 TP）"""
import requests, json, time, os

BASE = "http://localhost:19530"
HEADERS = {"Authorization": "Bearer root:Milvus", "Content-Type": "application/json"}
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def log_req(log_file, label, method, url, body, resp):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"=== {label} ===\nREQUEST: {method} {url}\nBODY: {json.dumps(body, ensure_ascii=False)}\nRESPONSE: {resp.status_code} {resp.text}\n\n")

def clean(c):
    try: requests.post(f"{BASE}/v2/vectordb/collections/drop", headers=HEADERS, json={"collectionName": c}, timeout=10)
    except: pass

def setup_coll(c, schema=None, dim=4):
    if schema is None:
        schema = {"autoID": False, "enableDynamicField": True,
                  "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True},
                             {"fieldName":"vector","dataType":"FloatVector","elementTypeParams":{"dim":str(dim)}}]}
    r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json={"collectionName": c, "schema": schema})
    time.sleep(1)
    return r

def insert_data(c, n=3, dim=4):
    data = [{"id": i, "vector": [float(i)]*dim} for i in range(1, n+1)]
    r = requests.post(f"{BASE}/v2/vectordb/entities/insert", headers=HEADERS, json={"collectionName": c, "data": data})
    time.sleep(1)
    return r, data

def create_index_load(c):
    r = requests.post(f"{BASE}/v2/vectordb/indexes/create", headers=HEADERS,
                      json={"collectionName": c, "indexParams": [{"fieldName":"vector","metricType":"COSINE","indexType":"AUTOINDEX"}]})
    time.sleep(2)
    r2 = requests.post(f"{BASE}/v2/vectordb/collections/load", headers=HEADERS, json={"collectionName": c})
    time.sleep(3)
    return r, r2

def reproduce_50319(log_file):
    """#50319 FP by-design: search on unloaded collection returns code=0"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #50319: search on unloaded collection returns valid results\n# Ground truth: FALSE_POSITIVE (by-design)\n# Labels: kind/bug, resolution/by-design\n\n")
    c = "test_50319"; clean(c)
    setup_coll(c); insert_data(c)
    # DON'T load - search directly
    body = {"collectionName": c, "data": [[0.1,0.2,0.3,0.4]], "limit": 1}
    r = requests.post(f"{BASE}/v2/vectordb/entities/search", headers=HEADERS, json=body)
    log_req(log_file, "SEARCH_UNLOADED_BUG", "POST", "/v2/vectordb/entities/search", body, r)
    bug = r.json().get("code") == 0
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: search unloaded returned code={r.json().get('code')}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_50323(log_file):
    """#50323 TP: delete accepts both filter and ids (mutually exclusive)"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #50323: delete accepts both filter and ids (mutually exclusive)\n# Ground truth: TRUE_BUG (triage/accepted)\n\n")
    c = "test_50323"; clean(c)
    setup_coll(c); insert_data(c); create_index_load(c)
    body = {"collectionName": c, "filter": "id > 0", "ids": [1, 2]}
    r = requests.post(f"{BASE}/v2/vectordb/entities/delete", headers=HEADERS, json=body)
    log_req(log_file, "DELETE_filter_AND_ids_BUG", "POST", "/v2/vectordb/entities/delete", body, r)
    bug = r.json().get("code") == 0
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: delete both filter+ids returned code={r.json().get('code')}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_50352(log_file):
    """#50352 FP by-design: metricType='' silently accepted"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #50352: metricType='' silently substituted\n# Ground truth: FALSE_POSITIVE (by-design)\n# Labels: kind/bug, resolution/by-design\n\n")
    c = "test_50352"; clean(c)
    body = {"collectionName": c, "dimension": 4, "metricType": ""}
    r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json=body)
    log_req(log_file, "CREATE_metricType_empty_BUG", "POST", "/v2/vectordb/collections/create", body, r)
    # describe to see actual metricType
    r2 = requests.post(f"{BASE}/v2/vectordb/collections/describe", headers=HEADERS, json={"collectionName": c})
    log_req(log_file, "DESCRIBE_verify", "POST", "/v2/vectordb/collections/describe", {"collectionName": c}, r2)
    bug = r.json().get("code") == 0
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: metricType='' create returned code={r.json().get('code')}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_50353(log_file):
    """#50353 TP: search limit=0/-1 accepted"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #50353: search returns 200 for limit=0/-1\n# Ground truth: TRUE_BUG (triage/accepted)\n\n")
    c = "test_50353"; clean(c)
    setup_coll(c); insert_data(c); create_index_load(c)
    results = {}
    for lim in [0, -1]:
        body = {"collectionName": c, "data": [[0.1,0.2,0.3,0.4]], "limit": lim}
        r = requests.post(f"{BASE}/v2/vectordb/entities/search", headers=HEADERS, json=body)
        log_req(log_file, f"SEARCH_limit={lim}_BUG", "POST", "/v2/vectordb/entities/search", body, r)
        if r.json().get("code") == 0: results[lim] = True
    bug = any(results.values())
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: limit=0/-1 accepted={results}\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_50354(log_file):
    """#50354 TP: weak password 'abcdefgh' accepted"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #50354: password complexity not enforced\n# Ground truth: TRUE_BUG (triage/accepted)\n\n")
    user = "testuser50354"
    try: requests.post(f"{BASE}/v2/vectordb/users/drop", headers=HEADERS, json={"userName": user}, timeout=5)
    except: pass
    body = {"userName": user, "password": "abcdefgh"}
    r = requests.post(f"{BASE}/v2/vectordb/users/create", headers=HEADERS, json=body)
    log_req(log_file, "CREATE_weak_password_BUG", "POST", "/v2/vectordb/users/create", body, r)
    bug = r.json().get("code") == 0
    try: requests.post(f"{BASE}/v2/vectordb/users/drop", headers=HEADERS, json={"userName": user}, timeout=5)
    except: pass
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: weak password returned code={r.json().get('code')}\nbug_present: {bug}\n")
    return bug

def reproduce_50355(log_file):
    """#50355 TP: upsert fails on autoID=true despite docs saying supported"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #50355: upsert fails on autoID=true collections\n# Ground truth: TRUE_BUG (triage/accepted)\n\n")
    c = "test_50355"; clean(c)
    schema = {"autoID": True, "enableDynamicField": True,
              "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True,"autoID":True},
                         {"fieldName":"vector","dataType":"FloatVector","elementTypeParams":{"dim":"4"}}]}
    setup_coll(c, schema=schema); create_index_load(c)
    # upsert with explicit id (autoID=true should auto-generate, but docs say upsert supported)
    body = {"collectionName": c, "data": [{"id": 1, "vector": [0.1,0.2,0.3,0.4]}]}
    r = requests.post(f"{BASE}/v2/vectordb/entities/upsert", headers=HEADERS, json=body)
    log_req(log_file, "UPSERT_autoID_true_BUG", "POST", "/v2/vectordb/entities/upsert", body, r)
    resp_code = r.json().get("code")
    # bug = upsert fails (code != 0) on autoID=true
    bug = resp_code != 0
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: upsert on autoID=true returned code={resp_code} (bug if non-zero)\nbug_present: {bug}\n")
    clean(c); return bug

def main():
    print("Round 1: 6 new v2.6.17 candidates")
    results = {}
    for num, fn in [('50319', reproduce_50319), ('50323', reproduce_50323), ('50352', reproduce_50352),
                    ('50353', reproduce_50353), ('50354', reproduce_50354), ('50355', reproduce_50355)]:
        results[num] = fn(os.path.join(OUT_DIR, f"output_{num}.log"))
        print(f"  #{num}: bug_present={results[num]}")
    print("\nDone. Check output_*.log for details.")
    for num, present in results.items():
        print(f"  #{num}: {'BUG EXISTS' if present else 'NOT REPRODUCED'}")

if __name__ == "__main__":
    main()
