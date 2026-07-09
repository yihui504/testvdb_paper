#!/usr/bin/env python3
"""生成 4 个 TP 试题的 output_*.log，并更新 ground_truth.json + stage2_aggregation.json"""
import requests, json, time, os

BASE = "http://localhost:19530"
HEADERS = {"Authorization": "Bearer root:Milvus", "Content-Type": "application/json"}
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def log_req(log_file, label, method, url, body, resp, headers=None):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"=== {label} ===\n")
        f.write(f"REQUEST: {method} {url}\n")
        if headers:
            f.write(f"EXTRA_HEADERS: {json.dumps(headers)}\n")
        f.write(f"BODY: {json.dumps(body, ensure_ascii=False)}\n")
        f.write(f"RESPONSE: {resp.status_code} {resp.text}\n\n")

def clean(coll_name):
    try:
        requests.post(f"{BASE}/v2/vectordb/collections/drop", headers=HEADERS,
                      json={"collectionName": coll_name}, timeout=10)
    except: pass

def reproduce_49823(log_file):
    """#49823: search accepts nprobe=0 (TRUE_BUG, ACCEPTED_OPEN)"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #49823: search accepts nprobe=0\n# Ground truth: TRUE_BUG (triage/accepted, ACCEPTED_OPEN)\n\n")
    c = "test_49823"
    clean(c)
    r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS,
                      json={"collectionName": c, "schema": {"autoID": False, "enableDynamicField": True,
                          "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True},
                                     {"fieldName":"vector","dataType":"FloatVector","elementTypeParams":{"dim":4}}]}})
    log_req(log_file, "STEP1_CREATE", "POST", "/v2/vectordb/collections/create", {"collectionName": c}, r)
    time.sleep(1)
    r = requests.post(f"{BASE}/v2/vectordb/entities/insert", headers=HEADERS,
                      json={"collectionName": c, "data": [{"id":1,"vector":[0.1,0.2,0.3,0.4]}]})
    log_req(log_file, "STEP2_INSERT", "POST", "/v2/vectordb/entities/insert", {"collectionName": c}, r)
    time.sleep(1)
    r = requests.post(f"{BASE}/v2/vectordb/indexes/create", headers=HEADERS,
                      json={"collectionName": c, "indexParams": [{"fieldName":"vector","metricType":"COSINE","indexType":"AUTOINDEX"}]})
    log_req(log_file, "STEP3_CREATE_INDEX", "POST", "/v2/vectordb/indexes/create", {"collectionName": c}, r)
    time.sleep(2)
    r = requests.post(f"{BASE}/v2/vectordb/collections/load", headers=HEADERS, json={"collectionName": c})
    log_req(log_file, "STEP4_LOAD", "POST", "/v2/vectordb/collections/load", {"collectionName": c}, r)
    time.sleep(3)
    body = {"collectionName": c, "data": [[0.1,0.2,0.3,0.4]], "limit": 1, "searchParams": {"params": {"nprobe": 0}}}
    r = requests.post(f"{BASE}/v2/vectordb/entities/search", headers=HEADERS, json=body)
    log_req(log_file, "STEP5_SEARCH_nprobe=0_BUG", "POST", "/v2/vectordb/entities/search", body, r)
    bug_present = r.json().get("code") == 0
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug_present else 'NOT_REPRODUCED'}: search with nprobe=0 returned code={r.json().get('code')}\n")
        f.write(f"bug_present_in_v2.6.17: {bug_present}\n")
    clean(c)
    return bug_present

def reproduce_49890(log_file):
    """#49890: Request-Timeout header accepts non-integer (TRUE_BUG, FIXED - may be fixed in v2.6.17)"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #49890: Request-Timeout header accepts non-integer types\n# Ground truth: TRUE_BUG (FIXED - may be fixed in v2.6.17)\n\n")
    bug_present = False
    for val in ["3.5", "abc"]:
        h = dict(HEADERS)
        h["Request-Timeout"] = val
        r = requests.post(f"{BASE}/v2/vectordb/collections/list", headers=h, json={})
        log_req(log_file, f"LIST_Request-Timeout={val}", "POST", "/v2/vectordb/collections/list", {}, r, {"Request-Timeout": val})
        if r.json().get("code") == 0:
            bug_present = True
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug_present else 'NOT_REPRODUCED'}: non-integer Request-Timeout {'accepted' if bug_present else 'rejected'}\n")
        f.write(f"bug_present_in_v2.6.17: {bug_present}\n")
    return bug_present

def reproduce_50018(log_file):
    """#50018: aliases/list accepts empty collectionName (TRUE_BUG, FIXED - may be fixed)"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #50018: aliases/list accepts empty collectionName\n# Ground truth: TRUE_BUG (FIXED - may be fixed in v2.6.17)\n\n")
    body = {"collectionName": "", "dbName": "default"}
    r = requests.post(f"{BASE}/v2/vectordb/aliases/list", headers=HEADERS, json=body)
    log_req(log_file, "ALIASES_LIST_empty_collectionName_BUG", "POST", "/v2/vectordb/aliases/list", body, r)
    bug_present = r.json().get("code") == 0
    # 对比：collections/describe 应该拒绝空
    r2 = requests.post(f"{BASE}/v2/vectordb/collections/describe", headers=HEADERS, json={"collectionName": ""})
    log_req(log_file, "DESCRIBE_empty_contrast", "POST", "/v2/vectordb/collections/describe", {"collectionName": ""}, r2)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug_present else 'NOT_REPRODUCED'}: aliases/list empty collectionName returned code={r.json().get('code')}\n")
        f.write(f"bug_present_in_v2.6.17: {bug_present}\n")
    return bug_present

def reproduce_49930(log_file):
    """#49930: negative/zero values accepted (TRUE_BUG, ACCEPTED_OPEN)"""
    open(log_file, 'w', encoding='utf-8').write("# Issue #49930: negative/zero values for index/collection params accepted\n# Ground truth: TRUE_BUG (triage/accepted, ACCEPTED_OPEN)\n\n")
    bug_present = False
    # efConstruction=0 via index create
    c = "test_49930"
    clean(c)
    r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS,
                      json={"collectionName": c, "schema": {"autoID": False, "enableDynamicField": True,
                          "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True},
                                     {"fieldName":"vector","dataType":"FloatVector","elementTypeParams":{"dim":4}}]}})
    log_req(log_file, "STEP1_CREATE", "POST", "/v2/vectordb/collections/create", {"collectionName": c}, r)
    time.sleep(1)
    body = {"collectionName": c, "indexParams": [{"fieldName":"vector","metricType":"COSINE","indexType":"HNSW","params":{"M":16,"efConstruction":0}}]}
    r = requests.post(f"{BASE}/v2/vectordb/indexes/create", headers=HEADERS, json=body)
    log_req(log_file, "INDEX_efConstruction=0_BUG", "POST", "/v2/vectordb/indexes/create", body, r)
    if r.json().get("code") == 0:
        bug_present = True
    # efConstruction=-1
    body2 = {"collectionName": c, "indexParams": [{"fieldName":"vector","metricType":"COSINE","indexType":"HNSW","params":{"M":16,"efConstruction":-1}}]}
    r = requests.post(f"{BASE}/v2/vectordb/indexes/create", headers=HEADERS, json=body2)
    log_req(log_file, "INDEX_efConstruction=-1_BUG", "POST", "/v2/vectordb/indexes/create", body2, r)
    if r.json().get("code") == 0:
        bug_present = True
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug_present else 'NOT_REPRODUCED'}: negative/zero efConstruction {'accepted' if bug_present else 'rejected'}\n")
        f.write(f"bug_present_in_v2.6.17: {bug_present}\n")
    clean(c)
    return bug_present

def main():
    print("Generating TP questions...")
    results = {}
    results['49823'] = reproduce_49823(os.path.join(OUT_DIR, "output_49823.log"))
    print(f"  #49823 done (bug_present={results['49823']})")
    results['49890'] = reproduce_49890(os.path.join(OUT_DIR, "output_49890.log"))
    print(f"  #49890 done (bug_present={results['49890']})")
    results['50018'] = reproduce_50018(os.path.join(OUT_DIR, "output_50018.log"))
    print(f"  #50018 done (bug_present={results['50018']})")
    results['49930'] = reproduce_49930(os.path.join(OUT_DIR, "output_49930.log"))
    print(f"  #49930 done (bug_present={results['49930']})")

    # 更新 ground_truth.json（读现有 FP，追加 TP）
    gt_path = os.path.join(OUT_DIR, "ground_truth.json")
    with open(gt_path, encoding='utf-8') as f:
        gt = json.load(f)
    tp_info = {
        "49823": ("search accepts nprobe=0", "TRUE_BUG", "ACCEPTED_OPEN (triage/accepted). nprobe=0 accepted, returns empty results.", "Type1_IllegalSuccess"),
        "49890": ("Request-Timeout non-integer", "TRUE_BUG", "FIXED (triage/accepted). Non-integer Request-Timeout accepted.", "Type1_IllegalSuccess"),
        "50018": ("aliases/list empty collectionName", "TRUE_BUG", "FIXED (triage/accepted). Empty collectionName accepted in aliases/list.", "Type1_IllegalSuccess"),
        "49930": ("negative/zero values accepted", "TRUE_BUG", "ACCEPTED_OPEN (triage/accepted). efConstruction=0/-1 accepted.", "Type1_IllegalSuccess"),
    }
    for num, (title, label, evidence, dtype) in tp_info.items():
        gt[num] = {"issue": int(num), "title": title, "true_label": label,
                   "evidence": evidence, "type": dtype,
                   "bug_present_in_v2.6.17": results[num]}
    with open(gt_path, 'w', encoding='utf-8') as f:
        json.dump(gt, f, ensure_ascii=False, indent=2)
    print("  ground_truth.json updated (8 questions)")

    # 更新 stage2_aggregation.json
    stage2_path = os.path.join(OUT_DIR, "stage2_aggregation.json")
    with open(stage2_path, encoding='utf-8') as f:
        stage2 = json.load(f)
    for num in tp_info:
        stage2["candidates"].append({
            "defect_id": f"issue_{num}",
            "endpoint": tp_info[num][0],
            "defect_type": tp_info[num][3],
            "trigger_script": f"output_{num}.log",
            "vote": "is_defect",
            "severity": "High"
        })
    stage2["total"] = len(stage2["candidates"])
    with open(stage2_path, 'w', encoding='utf-8') as f:
        json.dump(stage2, f, ensure_ascii=False, indent=2)
    print(f"  stage2_aggregation.json updated ({stage2['total']} candidates)")
    print(f"\nSummary (bug_present in v2.6.17):")
    for num, present in results.items():
        print(f"  #{num}: {'BUG EXISTS' if present else 'FIXED/not reproducible'}")

if __name__ == "__main__":
    main()
