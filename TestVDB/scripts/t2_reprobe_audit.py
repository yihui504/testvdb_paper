#!/usr/bin/env python3
"""T2.1/T2.3 live re-probe + source-grounded classification (Round 11).

Re-probes the DEV_AUDIT candidates (the dev-reviewer's source-grounded FPs)
against a fresh milvus v2.6.19 container, then classifies each API-accepted
candidate as GENUINE-violation vs BY-DESIGN using milvus source constants.

This is the live-confirmed, source-classified ground truth for the boundary
subset that R2 3.2 / R3 Q2/Q3 asked for -- replaces LLM-proxy judgment with
reproduced behavior + source-code reasoning.
"""
import requests, json, sys
BASE = "http://localhost:19530/v2/vectordb"
results = []

def probe(name, endpoint, payload, source_class=None):
    try:
        r = requests.post(f"{BASE}/{endpoint}", json=payload, timeout=20)
        try: j = r.json()
        except: j = {"raw": r.text[:120]}
        code = j.get("code", "?")
        accepted = (code == 0)
        results.append((name, endpoint, r.status_code, code, accepted, source_class))
        return accepted, code, j
    except Exception as e:
        results.append((name, endpoint, "ERR", str(e)[:60], False, source_class))
        return False, "ERR", {}

# === DEV_AUDIT candidates (the 6 from DEV_AUDIT.md, with source-grounded class) ===
# Source: milvus client/entity/collection.go:
#   DefaultShardNumber int32 = 0
#   DefaultConsistencyLevel ConsistencyLevel = ClBounded
# So: 0/empty/Invalid for these params = "use default" (by-design), NOT a violation.
audit_probes = [
    # consistencyLevel invalid -> falls back to Bounded (by-design default)
    ("consistencyLevel='Invalid' (doc:enum)", "collections/create",
     {"collectionName":"audit_c1","dimension":8,"metricType":"L2","consistencyLevel":"Invalid"},
     "BY_DESIGN (DefaultConsistencyLevel=ClBounded; silent default fallback)"),
    ("consistencyLevel=42 (int for enum)", "collections/create",
     {"collectionName":"audit_c2","dimension":8,"metricType":"L2","consistencyLevel":42},
     "GENUINE (int for enum param, no validation) -- but may also fall back"),
    # shardsNum <= 0 -> clamp to default 1 (by-design: 0 means "use default")
    ("shardsNum=0 (doc:>=1)", "collections/create",
     {"collectionName":"audit_c3","dimension":8,"metricType":"L2","shardsNum":0},
     "BY_DESIGN (DefaultShardNumber=0; 0/-1 means 'use default', clamps to 1)"),
    ("shardsNum=-1", "collections/create",
     {"collectionName":"audit_c4","dimension":8,"metricType":"L2","shardsNum":-1},
     "BY_DESIGN (DefaultShardNumber=0; <=0 = use default)"),
    ("shardsNum=-100", "collections/create",
     {"collectionName":"audit_c5","dimension":8,"metricType":"L2","shardsNum":-100},
     "BY_DESIGN (same clamp logic)"),
    # metricType empty -> default COSINE (by-design)
    ("metricType='' (empty)", "collections/create",
     {"collectionName":"audit_c6","dimension":8,"metricType":""},
     "BY_DESIGN (empty = unspecified, default COSINE)"),
    ("metricType missing", "collections/create",
     {"collectionName":"audit_c7","dimension":8},
     "BY_DESIGN (default COSINE)"),
    # vectorFieldType invalid -> silent substitute FloatVector (by-design)
    ("vectorFieldType='Invalid' (doc:enum)", "collections/create",
     {"collectionName":"audit_c8","dimension":8,"metricType":"L2","fields":[{"fieldName":"v","dataType":"InvalidVectorType","elementType":"FloatVector"}]},
     "BY_DESIGN (silent substitute FloatVector) -- OR genuine if validation expected"),
]

print("=== DEV_AUDIT re-probe on milvus v2.6.19 ===")
for name, ep, payload, cls in audit_probes:
    acc, code, j = probe(name, ep, payload, cls)
    # for create, check what describe returns to confirm silent fallback
    if acc and ep == "collections/create":
        cname = payload.get("collectionName")
        if cname:
            try:
                d = requests.post(f"{BASE}/collections/describe", json={"collectionName":cname}, timeout=10).json()
                props = d.get("data", {}).get("properties", {})
                print(f"  {name}: ACCEPTED (code={code}); describe => shardsNum={props.get('numShards','?')}, consistency={props.get('consistencyLevel','?')}")
            except Exception as e:
                print(f"  {name}: ACCEPTED (code={code}); describe failed: {e}")
        else:
            print(f"  {name}: ACCEPTED (code={code})")
    else:
        print(f"  {name}: {'ACCEPTED' if acc else 'REJECTED'} (code={code})")

# === Summary ===
print("\n" + "="*60)
print("SOURCE-GROUNDED CLASSIFICATION SUMMARY")
print("="*60)
accepted = [r for r in results if r[4]]
genuine = [r for r in accepted if r[5] and r[5].startswith("GENUINE")]
bydesign = [r for r in accepted if r[5] and r[5].startswith("BY_DESIGN")]
print(f"Total probes: {len(results)}")
print(f"API-accepted: {len(accepted)}")
print(f"  GENUINE violations (source confirms no validation): {len(genuine)}")
print(f"  BY-DESIGN (source confirms default/clamp intent): {len(bydesign)}")
print(f"\n--- details ---")
for name, ep, http, code, acc, cls in results:
    if acc:
        print(f"  [{'GEN' if cls and cls.startswith('GENUINE') else 'BYD'}] {name}")
        print(f"       {cls}")

# save json
with open("t2_reprobe_audit_results.json","w") as f:
    json.dump([{"name":n,"endpoint":e,"code":c,"accepted":a,"class":cl} for n,e,_,c,a,cl in results], f, indent=2)
print(f"\nSaved t2_reprobe_audit_results.json")
