#!/usr/bin/env python3
"""Reproduction anchor experiment (C3) — independent live re-probe, NO source code.

Re-probes the 27 dev-reviewer-killed candidates using ONLY live behavior (no
milvus source / internal constants), N=5 stability, to quantify:
  - reproduction kill rate on tooling-artifact FPs  (target >= 10/15)
  - reproduction misjudgment rate on by-design FPs  (expected high = honest boundary)

Difference from t2_full_27_reprobe.py: t2's confirms_fp USED source knowledge
("upsert by design", "DefaultShardNumber=0"). Here, violation_observed is judged
purely from the live response (code / shape), simulating what a reproduction-only
anchor could decide WITHOUT source access. Reproduction follows dev-reviewer.md
step-1: rebuild a minimal request, fill necessary params, check whether the
claimed violation actually materializes in the live response.

reproduction_kills_fp = violation NOT observed stably (0/N runs).
"""
import json
import requests
import time
from collections import Counter

BASE = "http://localhost:19530/v2/vectordb"
S = requests.Session()
S.headers.update({"Content-Type": "application/json"})
N_RUNS = 5


def post(ep, payload, timeout=20):
    try:
        r = S.post(f"{BASE}/{ep}", json=payload, timeout=timeout)
        try:
            j = r.json()
        except Exception:
            j = {"raw": r.text[:160]}
        return j.get("code", "?"), j
    except Exception as e:
        return "ERR", {"error": str(e)[:80]}


def mkc(name, **kw):
    b = {"collectionName": name, "dimension": 8, "metricType": "L2"}
    b.update(kw)
    return b


def ins(name, vecs, ids=None):
    data = []
    for i, v in enumerate(vecs):
        row = {"vector": v}
        if ids is not None:
            row["id"] = ids[i]
        data.append(row)
    return post("entities/insert", {"collectionName": name, "data": data})


def setup_base():
    """Create the 3 base collections used by stateless probes (setup verified live)."""
    for fn in ("fp_insert", "fp_search", "fp_upsert"):
        post("collections/drop", {"collectionName": fn})  # clean slate
        time.sleep(1)
    for fn in ("fp_insert", "fp_search"):
        post("collections/create", mkc(fn))
        post("collections/load", {"collectionName": fn})
        time.sleep(4)
    ins("fp_insert", [[float(i)] * 8 for i in range(3)], ids=[1, 2, 3]); time.sleep(2)
    ins("fp_search", [[float(i)] * 8 for i in range(5)], ids=list(range(5))); time.sleep(2)
    # fp_upsert: simple enableDynamicField (complex schema.fields form is rejected by v2.6.19)
    post("collections/create", mkc("fp_upsert", enableDynamicField=True))
    post("collections/load", {"collectionName": "fp_upsert"})
    time.sleep(4)
    ins("fp_upsert", [[float(i)] * 8 for i in range(3)], ids=[10, 11, 12]); time.sleep(2)
    # verify searchable data landed (get_stats rowCount is async-lagged, must probe via search)
    c, j = post("entities/search", {"collectionName": "fp_search", "data": [[1.] * 8], "limit": 3})
    print(f"  [setup verify] fp_search search code={c} has_data={bool(j.get('data'))}")


results = []


def record(did, cat, fp_class, violation_runs, detail):
    kill = (violation_runs == 0)
    unstable = not (violation_runs == 0 or violation_runs == N_RUNS)
    results.append({"defect_id": did, "category": cat, "fp_class": fp_class,
                    "violation_runs": violation_runs, "detail": detail,
                    "reproduction_kills_fp": kill, "unstable": unstable})
    tag = "KILL" if kill else ("MISS" if violation_runs == N_RUNS else "UNSTABLE")
    print(f"[{tag}] {did} ({fp_class}): viol {violation_runs}/{N_RUNS} - {detail}")


def probe(did, cat, fp_class, ep, payload, setup_each=None):
    """Stateless/stateful probe: violation = (code==0) i.e. claimed-bad accept materialized."""
    nv = 0
    detail = ""
    for _ in range(N_RUNS):
        if setup_each:
            setup_each()
        c, _ = post(ep, payload)
        if c == 0:
            nv += 1
        detail = f"code={c}"
    record(did, cat, fp_class, nv, detail)


_uid = [0]


def _fresh(prefix, load=True, n_data=0):
    """Create a fresh uniquely-named collection (optional load + data). Returns name."""
    _uid[0] += 1
    n = f"{prefix}_r{_uid[0]}"
    post("collections/create", mkc(n))
    if load:
        post("collections/load", {"collectionName": n})
        time.sleep(2)
    if n_data:
        ins(n, [[float(i)] * 8 for i in range(n_data)])
        time.sleep(1)
    return n


# ============================================================
print("=== setup base collections ===")
setup_base()

# ---------- A: INPUT_VALIDATED_REJECT (tooling_artifact) ----------
# claim: "invalid input was accepted" -> violation = code==0; live rejects (1804) => KILL
print("\n--- A: input-validation (claim: invalid input accepted) ---")
probe("A1_dim_mismatch", "tooling_artifact", "INPUT_VALIDATED_REJECT", "entities/insert",
      {"collectionName": "fp_insert", "data": [{"id": 100, "vector": [1., 2., 3., 4.]}]})
probe("A2_empty_array", "tooling_artifact", "INPUT_VALIDATED_REJECT", "entities/insert",
      {"collectionName": "fp_insert", "data": [{"id": 101, "vector": []}]})
probe("A3_missing_vector", "tooling_artifact", "INPUT_VALIDATED_REJECT", "entities/insert",
      {"collectionName": "fp_insert", "data": [{"id": 102}]})
probe("A4_null_vector", "tooling_artifact", "INPUT_VALIDATED_REJECT", "entities/insert",
      {"collectionName": "fp_insert", "data": [{"id": 103, "vector": None}]})
probe("A5_type_mismatch", "tooling_artifact", "INPUT_VALIDATED_REJECT", "entities/insert",
      {"collectionName": "fp_insert", "data": [{"id": 104, "vector": "x"}]})

# ---------- B: by-design (reproduction expected to MISJUDGE as TP) ----------
print("\n--- B: by-design (claim: sth accepted that is by-design) ---")
probe("B6_dup_pk", "by_design", "BY_DESIGN_UPSERT_SEMANTICS", "entities/insert",
      {"collectionName": "fp_upsert", "data": [{"id": 1, "vector": [1.] * 8},
                                               {"id": 1, "vector": [2.] * 8}]})
probe("B7_upsert_new", "by_design", "BY_DESIGN_UPSERT_SEMANTICS", "entities/upsert",
      {"collectionName": "fp_upsert", "data": [{"id": 999, "vector": [9.] * 8}]})
probe("B13_big_batch", "by_design", "BY_DESIGN_UPSERT_SEMANTICS", "entities/insert",
      {"collectionName": "fp_upsert",
       "data": [{"id": i % 10, "vector": [float(i)] * 8} for i in range(200)]})
probe("B24_overwrite", "by_design", "BY_DESIGN_UPSERT_SEMANTICS", "entities/upsert",
      {"collectionName": "fp_upsert", "data": [{"id": 1, "vector": [7.] * 8}]})
probe("B10_drop_alias_nonexist", "by_design", "BY_DESIGN_IDEMPOTENT", "aliases/drop",
      {"alias": "nope_xyz"})
probe("B11_drop_index_nonexist", "by_design", "BY_DESIGN_IDEMPOTENT", "indexes/drop",
      {"collectionName": "fp_search", "indexName": "nope_xyz"})
probe("B12_undefined_field", "by_design", "BY_DESIGN_DYNAMIC_FIELD", "entities/insert",
      {"collectionName": "fp_upsert", "data": [{"id": 500, "vector": [5.] * 8, "extra": "x"}]})
probe("B25_deep_filter", "by_design", "BY_DESIGN_ACCEPTED", "entities/query",
      {"collectionName": "fp_search", "filter": " and ".join(["id > 0"] * 100), "limit": 3})

# stateful by-design probes (fresh state each run)


def probe_b8():
    nv, detail = 0, ""
    for _ in range(N_RUNS):
        n = _fresh("dc", load=False)  # create fresh
        c, _ = post("collections/create", mkc(n))  # duplicate create of same name
        if c == 0:
            nv += 1
        detail = f"dup_create_code={c}"
    record("B8_dup_collection", "by_design", "BY_DESIGN_IDEMPOTENT", nv, detail)


probe_b8()


def _drop_then_search():
    n = _fresh("ds")
    post("collections/drop", {"collectionName": n})
    time.sleep(1)
    return n


def probe_b18():
    nv, detail = 0, ""
    for _ in range(N_RUNS):
        n = _drop_then_search()
        c, _ = post("entities/search", {"collectionName": n, "data": [[1.] * 8], "limit": 3})
        if c == 0:
            nv += 1
        detail = f"code={c}"
    record("B18_drop_then_search", "by_design", "STATE_SEMANTICS_CORRECT", nv, detail)


probe_b18()


def probe_b19():
    nv, detail = 0, ""
    for _ in range(N_RUNS):
        n = _fresh("rc")  # fresh empty loaded collection
        c, _ = post("entities/search", {"collectionName": n, "data": [[1.] * 8], "limit": 3})
        if c == 0:
            nv += 1
        detail = f"code={c}"
    record("B19_search_empty", "by_design", "STATE_SEMANTICS_CORRECT", nv, detail)


probe_b19()

# ---------- C: CORRECT_REJECT_CONVENTION (tooling_artifact) ----------
# claim: "bad input accepted" -> live returns business error (1100) => KILL
print("\n--- C: correct-rejection (claim: bad input accepted) ---")
probe("C14_filter_syntax", "tooling_artifact", "CORRECT_REJECT_CONVENTION", "entities/search",
      {"collectionName": "fp_search", "data": [[1.] * 8], "filter": "INVALID (((", "limit": 3})
probe("C15_metric_invalid", "tooling_artifact", "CORRECT_REJECT_CONVENTION", "entities/search",
      {"collectionName": "fp_search", "data": [[1.] * 8], "metricType": "BAD", "limit": 3})
probe("C17_drop_default_db", "tooling_artifact", "CORRECT_REJECT_CONVENTION", "databases/drop",
      {"dbName": "default"})
def probe_c27():
    nv, detail = 0, ""
    for _ in range(N_RUNS):
        n = _fresh("nl", load=False)  # created but NOT loaded
        c, _ = post("entities/search", {"collectionName": n, "data": [[1.] * 8], "limit": 3})
        if c == 0:
            nv += 1
        detail = f"search_notloaded_code={c}"
    record("C27_search_not_loaded", "tooling_artifact", "CORRECT_REJECT_CONVENTION", nv, detail)


probe_c27()

# ---------- D: ORACLE_SCRIPT_BUG (tooling_artifact) ----------
# claim: "search returned missing fields". Reproduction FILLS outputFields (dev-reviewer
# step-1 "fill necessary params"); if the filled request succeeds with data, the candidate's
# "missing field" is an oracle-script artifact => violation = NOT (code==0 with data).
print("\n--- D: oracle-script-bug (reproduction fills outputFields) ---")


def probe_of(did):
    nv, detail = 0, ""
    for _ in range(N_RUNS):
        c, j = post("entities/search", {"collectionName": "fp_search", "data": [[1.] * 8],
                                        "outputFields": ["id"], "limit": 3})
        has_data = bool(j.get("data"))
        if not (c == 0 and has_data):  # filled request did NOT succeed => violation stands
            nv += 1
        detail = f"code={c} has_data={has_data}"
    record(did, "tooling_artifact", "ORACLE_SCRIPT_BUG", nv, detail)


for did in ["D20_outputFields", "D21_outputFields", "D22_outputFields", "D23_outputFields"]:
    probe_of(did)


def probe_d26():
    """rowCount=0 after autoID-violating insert: reproduction checks if insert itself failed."""
    nv, detail = 0, ""
    for _ in range(N_RUNS):
        n = _fresh("ai", load=True)
        # re-create with autoID=True to mirror t2 #26
        post("collections/drop", {"collectionName": n})
        time.sleep(1)
        post("collections/create", {"collectionName": n, "dimension": 8, "metricType": "L2",
            "schema": {"autoId": True, "enableDynamicField": False,
                       "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": True,
                                   "autoID": True},
                                  {"fieldName": "vector", "dataType": "FloatVector",
                                   "elementType": "FloatVector"}]}})
        post("collections/load", {"collectionName": n})
        time.sleep(2)
        c_ins, _ = post("entities/insert", {"collectionName": n,
                        "data": [{"id": 1, "vector": [1.] * 8}]})  # violates autoID
        # violation (candidate claim "rowCount=0 after insert") stands only if insert succeeded
        if c_ins == 0:
            nv += 1
        detail = f"insert_code={c_ins}"
    record("D26_rowCount_autoID", "tooling_artifact", "ORACLE_SCRIPT_BUG", nv, detail)


probe_d26()

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 64)
print("REPRODUCTION ANCHOR SUMMARY (live-only, N=%d, milvus v2.6.19)" % N_RUNS)
print("=" * 64)


def rate(cat, killed=True):
    sub = [r for r in results if r["category"] == cat]
    if not sub:
        return 0, 0
    hit = [r for r in sub if r["reproduction_kills_fp"] == killed]
    return len(hit), len(sub)


tk, tn = rate("tooling_artifact", killed=True)
mk, mn = rate("by_design", killed=False)  # misjudge = did NOT kill a by-design FP
unstable = [r["defect_id"] for r in results if r["unstable"]]
print(f"tooling_artifact: reproduction KILL {tk}/{tn}")
print(f"by_design:        reproduction MISJUDGE (not killed) {mk}/{mn}")
print(f"unstable:         {len(unstable)} {unstable}")
print(f"\nthreshold (>=10/15 tooling): {'MET' if tk >= 10 else 'NOT MET'} ({tk}/15)")

with open("reproduction_anchor_results.json", "w", encoding="utf-8") as f:
    json.dump({"target": "milvus v2.6.19", "n_runs": N_RUNS,
               "tooling_kill": f"{tk}/{tn}", "by_design_misjudge": f"{mk}/{mn}",
               "unstable": unstable, "results": results}, f, indent=2, ensure_ascii=False)
print("\nSaved reproduction_anchor_results.json")
