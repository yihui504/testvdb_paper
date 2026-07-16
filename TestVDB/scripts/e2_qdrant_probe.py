#!/usr/bin/env python3
"""E2 expansion: live-probe Qdrant v1.18.2 for special-value acceptance.

For each candidate param where a strict bound could be over-strict, probe the
special value (0 / out-of-range) and record whether Qdrant accepts it.
Accept => a strict-bound clause would be over-strict.
"""
import requests, json, time, sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
S = requests.Session(); S.trust_env = False
B = "http://localhost:6333"
C = "e2_test"

def show(label, r):
    try:
        body = r.json()
        st = str(body.get("status", "?"))
        # for search, result presence; for writes, status ok
        acc = (r.status_code == 200 and st == "ok")
    except Exception:
        body = r.text[:80]; st = "?"; acc = (r.status_code == 200)
    print(f"  {label:32} HTTP={r.status_code} status={st:8} ACCEPTED={acc}")
    return acc

# setup
S.put(f"{B}/collections/{C}", json={"vectors":{"size":4,"distance":"Cosine"}}, timeout=20)
time.sleep(0.5)
S.put(f"{B}/collections/{C}/points", json={"points":[{"id":1,"vector":[0.1,0.2,0.3,0.4],"payload":{"g":"a"}}]}, timeout=20)
time.sleep(0.3)
print("=== Qdrant v1.18.2 special-value probes ===\n")

print("[limit]")
show("limit=0 (search)", S.post(f"{B}/collections/{C}/points/search", json={"vector":[0.1,0.2,0.3,0.4],"limit":0}, timeout=15))
show("limit=1 (control)", S.post(f"{B}/collections/{C}/points/search", json={"vector":[0.1,0.2,0.3,0.4],"limit":1}, timeout=15))

print("\n[score_threshold]  (semantic range [0,1] for Cosine)")
show("score_threshold=2.0", S.post(f"{B}/collections/{C}/points/search", json={"vector":[0.1,0.2,0.3,0.4],"limit":5,"score_threshold":2.0}, timeout=15))
show("score_threshold=-0.5", S.post(f"{B}/collections/{C}/points/search", json={"vector":[0.1,0.2,0.3,0.4],"limit":5,"score_threshold":-0.5}, timeout=15))

print("\n[timeout]  (GLM asserted timeout >= 1)")
show("timeout=0 (set payload)", S.post(f"{B}/collections/{C}/points/payload?timeout=0", json={"payload":{"x":1},"points":[1]}, timeout=15))
show("timeout=1 (control)", S.post(f"{B}/collections/{C}/points/payload?timeout=1", json={"payload":{"y":1},"points":[1]}, timeout=15))

print("\n[offset]")
show("offset=0 (control)", S.post(f"{B}/collections/{C}/points/search", json={"vector":[0.1,0.2,0.3,0.4],"limit":1,"offset":0}, timeout=15))

print("\n[group_size]")
show("group_size=0 (grouped search)", S.post(f"{B}/collections/{C}/points/search", json={"vector":[0.1,0.2,0.3,0.4],"limit":3,"group_by":"g","group_size":0}, timeout=15))
show("group_size=1 (control)", S.post(f"{B}/collections/{C}/points/search", json={"vector":[0.1,0.2,0.3,0.4],"limit":3,"group_by":"g","group_size":1}, timeout=15))
