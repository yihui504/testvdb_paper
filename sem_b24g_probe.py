"""sem_b24g throwaway probe: (1) Cosine vs Euclid readback of vec4(0) BEFORE any clear;
(2) phantom-mix clear {0,9999} disposition + live-id payload effect. Live 127.0.0.1:6333."""
import json
import requests

B = "http://127.0.0.1:6333"
SEED = [-0.3, -0.2, -0.1, -0.25]  # vec4(0); norm = 0.45


def req(method, path, body=None):
    r = requests.request(method, B + path, json=body,
                         headers={"Content-Type": "application/json"}, timeout=30)
    try:
        return r.status_code, r.json()
    except Exception:
        return r.status_code, r.text


for coll, dist in [("sem_b24g_cos", "Cosine"), ("sem_b24g_euc", "Euclid")]:
    req("DELETE", f"/collections/{coll}")
    s, b = req("PUT", f"/collections/{coll}", {"vectors": {"size": 4, "distance": dist}})
    print(f"[{coll} create {dist}] {s}")
    s, b = req("PUT", f"/collections/{coll}/points?wait=true",
               {"points": [{"id": 0, "vector": SEED, "payload": {"k1": "a0"}}]})
    print(f"[{coll} upsert seed] {s} {json.dumps(b)[:110]}")
    # readback BEFORE any clear ever happens
    s, b = req("POST", f"/collections/{coll}/points",
               {"ids": [0], "with_payload": True, "with_vector": True})
    print(f"[{coll} readback pre-clear] {s} {json.dumps(b.get('result') if isinstance(b, dict) else b)}")

# phantom-mix replay on the Cosine collection
s, b = req("POST", "/collections/sem_b24g_cos/points/payload?wait=true",
           {"payload": {"kd": "live"}, "points": [0]})
print(f"[mix set kd=live on 0] {s} {json.dumps(b)[:110]}")
s, b = req("POST", "/collections/sem_b24g_cos/points/payload/clear?wait=true",
           {"points": [0, 9999]})
print(f"[mix clear {{0,9999}}] {s} {json.dumps(b)[:200]}")
s, b = req("POST", "/collections/sem_b24g_cos/points",
           {"ids": [0], "with_payload": True, "with_vector": True})
res = b.get("result") if isinstance(b, dict) else b
print(f"[mix post read id0] {s} payload={(res[0].get('payload') if res else None)} vector={(res[0].get('vector') if res else None)}")
s, b = req("POST", "/collections/sem_b24g_cos/points/count", {"exact": True})
print(f"[mix count] {s} {json.dumps(b.get('result') if isinstance(b, dict) else b)}")
s, b = req("POST", "/collections/sem_b24g_cos/points",
           {"ids": [9999], "with_payload": True, "with_vector": True})
print(f"[mix phantom read 9999] {s} result={json.dumps(b.get('result') if isinstance(b, dict) else b)}")

for coll in ("sem_b24g_cos", "sem_b24g_euc"):
    print(f"[cleanup {coll}] {req('DELETE', f'/collections/{coll}')[0]}")
