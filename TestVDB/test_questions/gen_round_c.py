#!/usr/bin/env python3
"""回合 C: #51084/#51085 (v2.6.19 FIXED, test in v2.6.17 which is < v2.6.19, should still exist)"""
import requests, json, time, os
BASE = "http://localhost:19530"
HEADERS = {"Authorization": "Bearer root:Milvus", "Content-Type": "application/json"}
OUT = os.path.dirname(os.path.abspath(__file__))

def clean(c):
    try: requests.post(f"{BASE}/v2/vectordb/collections/drop", headers=HEADERS, json={"collectionName": c}, timeout=10)
    except: pass

def reproduce_51084(lf):
    """#51084 TP: invalid consistencyLevel silently substituted"""
    open(lf,'w',encoding='utf-8').write("# Issue #51084: invalid consistencyLevel silently substituted\n# Ground truth: TRUE_BUG (FIXED in v2.6.19, should exist in v2.6.17)\n# Test version: v2.6.17\n\n")
    c="t51084"; clean(c)
    body={"collectionName": c, "dimension": 4, "consistencyLevel": "Invalid"}
    r=requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json=body)
    with open(lf,'a',encoding='utf-8') as f:
        f.write(f"=== CREATE_consistencyLevel=Invalid ===\nBODY: {json.dumps(body)}\nRESPONSE: {r.status_code} {r.text}\n\n")
    bug=r.json().get("code")==0
    # describe to verify substitution
    r2=requests.post(f"{BASE}/v2/vectordb/collections/describe", headers=HEADERS, json={"collectionName": c})
    with open(lf,'a',encoding='utf-8') as f:
        f.write(f"=== DESCRIBE_verify ===\nRESPONSE: {r2.status_code} {r2.text[:300]}\n\n")
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: invalid consistency code={r.json().get('code')} (silent substitution)\nbug_present: {bug}\n")
    clean(c); return bug

def reproduce_51085(lf):
    """#51085 TP: invalid vectorFieldType silently substituted"""
    open(lf,'w',encoding='utf-8').write("# Issue #51085: invalid vectorFieldType silently substituted\n# Ground truth: TRUE_BUG (FIXED in v2.6.19, should exist in v2.6.17)\n# Test version: v2.6.17\n\n")
    c="t51085"; clean(c)
    schema={"autoID": False, "enableDynamicField": True,
            "fields": [{"fieldName":"id","dataType":"Int64","isPrimary":True},
                       {"fieldName":"vector","dataType":"InvalidVectorType","elementTypeParams":{"dim":"4"}}]}
    body={"collectionName": c, "schema": schema}
    r=requests.post(f"{BASE}/v2/vectordb/collections/create", headers=HEADERS, json=body)
    with open(lf,'a',encoding='utf-8') as f:
        f.write(f"=== CREATE_vectorFieldType=Invalid ===\nBODY: {json.dumps(body)[:200]}\nRESPONSE: {r.status_code} {r.text}\n\n")
    bug=r.json().get("code")==0
    with open(lf,'a',encoding='utf-8') as f:
        f.write(f"\n=== VERDICT ===\n{'DEFECT_FOUND' if bug else 'NOT_REPRODUCED'}: invalid vectorFieldType code={r.json().get('code')} (silent substitution)\nbug_present: {bug}\n")
    clean(c); return bug

def main():
    print("Round C: #51084/#51085 in v2.6.17")
    for num, fn in [('51084', reproduce_51084), ('51085', reproduce_51085)]:
        bug = fn(os.path.join(OUT, f"output_{num}.log"))
        print(f"  #{num}: bug_present={bug}")

if __name__ == "__main__":
    main()
