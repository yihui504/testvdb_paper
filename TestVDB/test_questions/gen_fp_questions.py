#!/usr/bin/env python3
"""生成 4 个 by-design FP 试题的 output_*.log + ground_truth.json + stage2_aggregation.json"""
import requests, json, time, threading, os, sys

BASE = "http://localhost:19530"
HEADERS = {"Authorization": "Bearer root:Milvus", "Content-Type": "application/json"}
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def log_req(log_file, label, method, url, body, resp):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"=== {label} ===\n")
        f.write(f"REQUEST: {method} {url}\n")
        f.write(f"BODY: {json.dumps(body, ensure_ascii=False)}\n")
        f.write(f"RESPONSE: {resp.status_code} {resp.text}\n\n")

def clean(coll_name):
    try:
        requests.post(f"{BASE}/v2/vectordb/collections/drop", headers=HEADERS,
                      json={"collectionName": coll_name}, timeout=10)
    except: pass

def reproduce_50193(log_file):
    """#50193: get_stats returns rowCount=0 (BY_DESIGN - stale count)"""
    open(log_file, 'w').write("# Issue #50193: get_stats returns rowCount=0 after insert+load\n# Ground truth: FALSE_POSITIVE (by-design, stale count)\n# Labels: resolution/by-design\n\n")
    c = "test_50193"
    clean(c)
    r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS,
                      json={"collectionName": c, "schema": {"autoID": False, "enableDynamicField": True,
                          "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True},
                                     {"fieldName":"vector","dataType":"FloatVector","elementTypeParams":{"dim":4}},
                                     {"fieldName":"value","dataType":"Int64"}]}})
    log_req(log_file, "STEP1_CREATE", "POST", "/v2/vectordb/collections/create", {"collectionName": c}, r)
    time.sleep(1)
    data = [{"id": i, "vector": [float(i),float(i+1),float(i+2),float(i+3)], "value": i*10} for i in range(1,6)]
    r = requests.post(f"{BASE}/v2/vectordb/entities/insert", headers=HEADERS, json={"collectionName": c, "data": data})
    log_req(log_file, "STEP2_INSERT_5", "POST", "/v2/vectordb/entities/insert", {"collectionName": c, "data": "[5 entities]"}, r)
    time.sleep(1)
    r = requests.post(f"{BASE}/v2/vectordb/indexes/create", headers=HEADERS,
                      json={"collectionName": c, "indexParams": [{"fieldName":"vector","metricType":"COSINE","indexType":"AUTOINDEX"}]})
    log_req(log_file, "STEP2_5_CREATE_INDEX", "POST", "/v2/vectordb/indexes/create", {"collectionName": c}, r)
    time.sleep(2)
    r = requests.post(f"{BASE}/v2/vectordb/collections/load", headers=HEADERS, json={"collectionName": c})
    log_req(log_file, "STEP3_LOAD", "POST", "/v2/vectordb/collections/load", {"collectionName": c}, r)
    time.sleep(3)
    r = requests.post(f"{BASE}/v2/vectordb/collections/get_stats", headers=HEADERS, json={"collectionName": c})
    log_req(log_file, "STEP4_GET_STATS_BUG", "POST", "/v2/vectordb/collections/get_stats", {"collectionName": c}, r)
    r = requests.post(f"{BASE}/v2/vectordb/entities/query", headers=HEADERS,
                      json={"collectionName": c, "filter": "id > 0", "limit": 10, "outputFields": ["id","value"]})
    log_req(log_file, "STEP5_QUERY_VERIFY", "POST", "/v2/vectordb/entities/query", {"collectionName": c, "filter": "id > 0"}, r)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("\n=== VERDICT ===\nDEFECT_FOUND: get_stats returns rowCount=0 but query returns 5 entities (data exists)\n")
    clean(c)

def reproduce_50194(log_file):
    """#50194: concurrent delete+search returns stale data (BY_DESIGN - concurrency)"""
    open(log_file, 'w').write("# Issue #50194: concurrent delete+search returns stale/deleted data\n# Ground truth: FALSE_POSITIVE (by-design, concurrency semantics)\n# Labels: resolution/by-design\n\n")
    c = "test_50194"
    clean(c)
    r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS,
                      json={"collectionName": c, "schema": {"autoID": False, "enableDynamicField": True,
                          "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True},
                                     {"fieldName":"vector","dataType":"FloatVector","elementTypeParams":{"dim":4}},
                                     {"fieldName":"value","dataType":"Int64"}]}})
    log_req(log_file, "STEP1_CREATE", "POST", "/v2/vectordb/collections/create", {"collectionName": c}, r)
    time.sleep(1)
    data = [{"id": i, "vector": [float(i)*0.1,float(i+1)*0.1,float(i+2)*0.1,float(i+3)*0.1], "value": i*10} for i in range(1,11)]
    r = requests.post(f"{BASE}/v2/vectordb/entities/insert", headers=HEADERS, json={"collectionName": c, "data": data})
    log_req(log_file, "STEP2_INSERT_10", "POST", "/v2/vectordb/entities/insert", {"collectionName": c, "data": "[10 entities]"}, r)
    time.sleep(1)
    r = requests.post(f"{BASE}/v2/vectordb/indexes/create", headers=HEADERS,
                      json={"collectionName": c, "indexParams": [{"fieldName":"vector","metricType":"COSINE","indexType":"HNSW","params":{"M":16,"efConstruction":200}}]})
    log_req(log_file, "STEP3_CREATE_INDEX", "POST", "/v2/vectordb/indexes/create", {"collectionName": c}, r)
    time.sleep(1)
    r = requests.post(f"{BASE}/v2/vectordb/collections/load", headers=HEADERS, json={"collectionName": c})
    log_req(log_file, "STEP4_LOAD", "POST", "/v2/vectordb/collections/load", {"collectionName": c}, r)
    time.sleep(3)
    # 并发 delete + search
    results = {}
    def do_search():
        r = requests.post(f"{BASE}/v2/vectordb/entities/search", headers=HEADERS,
                          json={"collectionName": c, "data": [[0.1,0.2,0.3,0.4]], "limit": 10, "outputFields": ["id","value"]})
        results['search'] = r
    def do_delete():
        r = requests.post(f"{BASE}/v2/vectordb/entities/delete", headers=HEADERS,
                          json={"collectionName": c, "filter": "id in [1,2,3,4,5]"})
        results['delete'] = r
    t1 = threading.Thread(target=do_search); t2 = threading.Thread(target=do_delete)
    t1.start(); t2.start(); t1.join(); t2.join()
    log_req(log_file, "STEP5_CONCURRENT_SEARCH", "POST", "/v2/vectordb/entities/search", {"collectionName": c, "filter": "concurrent with delete"}, results.get('search'))
    log_req(log_file, "STEP6_CONCURRENT_DELETE", "POST", "/v2/vectordb/entities/delete", {"collectionName": c, "filter": "id in [1,2,3,4,5]"}, results.get('delete'))
    time.sleep(2)
    r = requests.post(f"{BASE}/v2/vectordb/entities/search", headers=HEADERS,
                      json={"collectionName": c, "data": [[0.1,0.2,0.3,0.4]], "limit": 10, "outputFields": ["id","value"]})
    log_req(log_file, "STEP7_FINAL_SEARCH_VERIFY", "POST", "/v2/vectordb/entities/search", {"collectionName": c}, r)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("\n=== VERDICT ===\nDEFECT_FOUND: concurrent delete+search may return stale/deleted entities\n")
    clean(c)

def reproduce_50351(log_file):
    """#50351: shardsNum=0/-1/65535 accepted (BY_DESIGN - clamping)"""
    open(log_file, 'w').write("# Issue #50351: shardsNum=0/-1/65535 accepted with code=200\n# Ground truth: FALSE_POSITIVE (by-design, clamping behavior)\n# Labels: kind/bug, resolution/by-design\n\n")
    for shards in [0, -1, 65535]:
        c = f"test_50351_{shards}"
        clean(c)
        body = {"collectionName": c, "dimension": 4, "shardsNum": shards, "metricType": "L2"}
        r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json=body)
        log_req(log_file, f"CREATE_shardsNum={shards}", "POST", "/v2/vectordb/collections/create", body, r)
        clean(c)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("\n=== VERDICT ===\nDEFECT_FOUND: shardsNum=0/-1/65535 all accepted with code=200 (documented min is 1)\n")

def reproduce_49928(log_file):
    """#49928: 32768-dim collection created without warning (BY_DESIGN - documented max)"""
    open(log_file, 'w').write("# Issue #49928: 32768-dimension collection created without warning\n# Ground truth: FALSE_POSITIVE (by-design, 32768 is documented max)\n# Labels: resolution/by-design\n\n")
    c = "test_49928_highdim"
    clean(c)
    body = {"collectionName": c, "dimension": 32768}
    r = requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json=body)
    log_req(log_file, "CREATE_dim=32768", "POST", "/v2/vectordb/collections/create", body, r)
    r = requests.post(f"{BASE}/v2/vectordb/collections/describe", headers=HEADERS, json={"collectionName": c})
    log_req(log_file, "DESCRIBE_verify", "POST", "/v2/vectordb/collections/describe", {"collectionName": c}, r)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("\n=== VERDICT ===\nDEFECT_FOUND: 32768-dim collection created without warning (OOM risk)\n")
    clean(c)

def main():
    print("Generating FP questions...")
    reproduce_50193(os.path.join(OUT_DIR, "output_50193.log"))
    print("  #50193 done")
    reproduce_50194(os.path.join(OUT_DIR, "output_50194.log"))
    print("  #50194 done")
    reproduce_50351(os.path.join(OUT_DIR, "output_50351.log"))
    print("  #50351 done")
    reproduce_49928(os.path.join(OUT_DIR, "output_49928.log"))
    print("  #49928 done")

    # ground_truth.json
    gt = {
        "50193": {"issue": 50193, "title": "get_stats returns rowCount=0", "true_label": "FALSE_POSITIVE", "evidence": "BY_DESIGN (resolution/by-design label). Stale count, query returns correct data.", "type": "Type4_StateLogicViolation"},
        "50194": {"issue": 50194, "title": "concurrent delete+search stale", "true_label": "FALSE_POSITIVE", "evidence": "BY_DESIGN (resolution/by-design label). Concurrency semantics, eventual consistency.", "type": "Type4_StateLogicViolation"},
        "50351": {"issue": 50351, "title": "shardsNum=0/-1/65535 accepted", "true_label": "FALSE_POSITIVE", "evidence": "BY_DESIGN (resolution/by-design label). Clamping behavior, milvus clamps to valid range.", "type": "Type1_IllegalSuccess"},
        "49928": {"issue": 49928, "title": "32768-dim collection without warning", "true_label": "FALSE_POSITIVE", "evidence": "BY_DESIGN (resolution/by-design label). 32768 is documented max dimension.", "type": "Type1_IllegalSuccess"}
    }
    with open(os.path.join(OUT_DIR, "ground_truth.json"), 'w', encoding='utf-8') as f:
        json.dump(gt, f, ensure_ascii=False, indent=2)
    print("  ground_truth.json written")

    # stage2_aggregation.json (候选清单，dev-reviewer 读这个)
    candidates = []
    for issue_num, info in gt.items():
        candidates.append({
            "defect_id": f"issue_{issue_num}",
            "endpoint": info["title"],
            "defect_type": info["type"],
            "trigger_script": f"output_{issue_num}.log",
            "vote": "is_defect",
            "severity": "High"
        })
    stage2 = {"candidates": candidates, "total": len(candidates)}
    with open(os.path.join(OUT_DIR, "stage2_aggregation.json"), 'w', encoding='utf-8') as f:
        json.dump(stage2, f, ensure_ascii=False, indent=2)
    print("  stage2_aggregation.json written")
    print(f"Done. {len(candidates)} FP questions generated in {OUT_DIR}")

if __name__ == "__main__":
    main()
