#!/usr/bin/env python3
"""Schema-aware boundary fuzzer baseline (P0-4, Round 8).

Generates boundary probes from Milvus's DOCUMENTED parameter constraints
(not LLM-derived), runs them against milvus 2.6.19, and reports which the API
accepts (potential spec violations). This is the "hand-written boundary-value
fuzzer" baseline R1/R2 asked for: no LLM in the loop, pure spec-driven.
"""
import requests, json, sys
BASE = "http://localhost:19530/v2/vectordb"
results = []

def probe(name, endpoint, payload):
    try:
        r = requests.post(f"{BASE}/{endpoint}", json=payload, timeout=15)
        try: j = r.json()
        except: j = {"raw": r.text[:80]}
        code = j.get("code", "?")
        accepted = (code == 0)
        results.append((name, endpoint, r.status_code, code, accepted))
        return accepted, code
    except Exception as e:
        results.append((name, endpoint, "ERR", str(e)[:60], False))
        return False, "ERR"

# === collection create boundary (documented: dim 1-32768, metricType L2/IP/COSINE,
#     consistencyLevel Strong/Session/Bounded/Eventually, collectionName non-empty) ===
creates = [
  ("dim=0 (doc:1-32768)", {"collectionName":"fz_t1","dimension":0,"metricType":"L2"}),
  ("dim=-1", {"collectionName":"fz_t2","dimension":-1,"metricType":"L2"}),
  ("dim=32769", {"collectionName":"fz_t3","dimension":32769,"metricType":"L2"}),
  ("dim='128' string (doc:int)", {"collectionName":"fz_t4","dimension":"128","metricType":"L2"}),
  ("metricType=INVALID (doc:L2/IP/COSINE)", {"collectionName":"fz_t5","dimension":128,"metricType":"INVALID"}),
  ("metricType missing", {"collectionName":"fz_t6","dimension":128}),
  ("consistencyLevel=INVALID (doc:enum)", {"collectionName":"fz_t7","dimension":128,"metricType":"L2","consistencyLevel":"INVALID"}),
  ("consistencyLevel=42 (int,doc:enum)", {"collectionName":"fz_t8","dimension":128,"metricType":"L2","consistencyLevel":42}),
  ("collectionName empty (doc:non-empty)", {"collectionName":"","dimension":128,"metricType":"L2"}),
  ("collectionName missing", {"dimension":128,"metricType":"L2"}),
]
for name, p in creates:
    probe(name, "collections/create", p)

# === setup for search/query ===
probe("setup fz_s", "collections/create", {"collectionName":"fz_s","dimension":4,"metricType":"L2"})
probe("setup insert", "entities/insert", {"collectionName":"fz_s","data":[{"id":1,"vector":[0.1,0.2,0.3,0.4]}]})

# === search boundary (documented: limit+offset<16384, limit>=0) ===
searches = [
  ("nprobe=0 (doc:>=1?)", {"collectionName":"fz_s","data":[[0.1,0.2,0.3,0.4]],"annsField":"vector","limit":1,"searchParams":{"params":{"nprobe":0}}}),
  ("nprobe=-1", {"collectionName":"fz_s","data":[[0.1,0.2,0.3,0.4]],"annsField":"vector","limit":1,"searchParams":{"params":{"nprobe":-1}}}),
  ("limit=-1 (doc:>=0)", {"collectionName":"fz_s","data":[[0.1,0.2,0.3,0.4]],"annsField":"vector","limit":-1}),
  ("limit=0", {"collectionName":"fz_s","data":[[0.1,0.2,0.3,0.4]],"annsField":"vector","limit":0}),
  ("limit=16385 (doc:<16384)", {"collectionName":"fz_s","data":[[0.1,0.2,0.3,0.4]],"annsField":"vector","limit":16385}),
  ("wrong-dim query (doc:dim=4)", {"collectionName":"fz_s","data":[[0.1,0.2,0.3]],"annsField":"vector","limit":1}),
]
for name, p in searches:
    probe(name, "entities/search", p)

# === query boundary ===
queries = [
  ("query limit=-1", {"collectionName":"fz_s","filter":"id > 0","limit":-1}),
  ("query limit=0", {"collectionName":"fz_s","filter":"id > 0","limit":0}),
  ("query limit=16385", {"collectionName":"fz_s","filter":"id > 0","limit":16385}),
]
for name, p in queries:
    probe(name, "entities/query", p)

# === report ===
print("\n" + "="*60)
print("SCHEMA-AWARE BOUNDARY FUZZER (P0-4 baseline)")
print("="*60)
fuzzer_probes = [r for r in results if not r[0].startswith("setup")]
violations = [r for r in fuzzer_probes if r[4]]
rejected = [r for r in fuzzer_probes if not r[4]]
print(f"Total probes (excl setup): {len(fuzzer_probes)}")
print(f"API-ACCEPTED (potential spec violations): {len(violations)}")
print(f"API-rejected (spec-conformant): {len(rejected)}")
print("\n--- POTENTIAL VIOLATIONS (API accepts documented-illegal input) ---")
for name, ep, http, code, acc in violations:
    print(f"  * {name}  [{ep}]  http={http} code={code}")
print("\n--- API-REJECTED (spec-conformant, not violations) ---")
for name, ep, http, code, acc in rejected:
    print(f"  ok {name}  [{ep}]  code={code}")
