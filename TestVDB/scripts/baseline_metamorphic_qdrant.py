#!/usr/bin/env python3
"""Classical-oracle baseline: metamorphic relations on Qdrant v1.18.2.

A small MR suite (distance symmetry, top-k monotonicity, COSINE bound,
self-similarity) that a metamorphic/differential tester would check. These test
RESULT CORRECTNESS. They structurally cannot test accept/reject CONFORMANCE
(no MR relates input-acceptance decisions), which is the residual TestVDB targets.
"""
import requests, time, sys, math
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
S = requests.Session(); S.trust_env = False
B = "http://localhost:6333"; C = "bl_mrp"
EPS = 1e-6

S.put(f"{B}/collections/{C}", json={"vectors":{"size":4,"distance":"Cosine"}}, timeout=20)
time.sleep(0.4)
PTS = [
 (1,[0.10,0.20,0.30,0.40]),(2,[0.9,0.8,0.7,0.6]),(3,[0.1,0.0,0.1,0.0]),
 (4,[0.5,0.5,0.5,0.5]),(5,[0.2,0.3,0.4,0.5]),(6,[1.0,0.9,0.8,0.7]),
 (7,[0.0,0.1,0.0,0.1]),(8,[0.33,0.33,0.33,0.34]),(9,[0.8,0.6,0.4,0.2]),
 (10,[0.12,0.34,0.56,0.78]),
]
S.put(f"{B}/collections/{C}/points?wait=true",
      json={"points":[{"id":i,"vector":v} for i,v in PTS]}, timeout=20)
time.sleep(0.3)
V = {i:v for i,v in PTS}

def search(vec, limit, with_payload=False, with_vector=False):
    r = S.post(f"{B}/collections/{C}/points/search",
        json={"vector":vec,"limit":limit,"with_payload":with_payload,"with_vector":with_vector}, timeout=15)
    return r.json().get("result",[])

print("=== Classical-oracle baseline: metamorphic relations on Qdrant v1.18.2 ===\n")

# MR1: distance symmetry  d(a,b)==d(b,a)  -> score(a->b)==score(b->a)
viol = 0; checked = 0
for a in [1,2,4,9]:
    for b in [x for x in [2,3,5,8] if x!=a]:
        ra = search(V[a], 10); rb = search(V[b], 10)
        sab = next((p["score"] for p in ra if p["id"]==b), None)
        sba = next((p["score"] for p in rb if p["id"]==a), None)
        if sab is not None and sba is not None:
            checked += 1
            if abs(sab - sba) > 1e-5: viol += 1; print(f"  MR1 VIOLATION a={a},b={b}: {sab} vs {sba}")
print(f"MR1 distance symmetry: {checked} pairs, {viol} violations")

# MR2: top-k monotonicity  top-k IDs subset of top-(k+1) IDs
viol = 0
for q in [1,4,9]:
    ids3 = {p["id"] for p in search(V[q],3)}
    ids4 = {p["id"] for p in search(V[q],4)}
    if not ids3.issubset(ids4): viol += 1; print(f"  MR2 VIOLATION q={q}: top3 {ids3} not subset of top4 {ids4}")
print(f"MR2 top-k monotonicity: 3 queries, {viol} violations")

# MR3: COSINE bound  score in [-1, 1]
viol = 0; n = 0
for q in [1,2,4,9]:
    for p in search(V[q],10):
        n += 1
        if p["score"] < -1 - EPS or p["score"] > 1 + EPS:
            viol += 1; print(f"  MR3 VIOLATION q={q} id={p['id']}: score={p['score']} out of [-1,1]")
print(f"MR3 COSINE bound [-1,1]: {n} scores, {viol} violations")

# MR4: self-similarity  search(v)->top is v, score ~= 1.0
viol = 0
for i in [1,4,8]:
    top = search(V[i],1)
    if not top or top[0]["id"] != i or abs(top[0]["score"] - 1.0) > 1e-5:
        viol += 1; print(f"  MR4 VIOLATION id={i}: top={top}")
print(f"MR4 self-similarity (top is self, score~1.0): 3 points, {viol} violations")

print("\n=== conformance defects found by these MRs: 0 (MRs relate OUTPUT correctness,")
print("    not INPUT accept/reject decisions -- the conformance residual is out of reach by construction) ===")
