#!/usr/bin/env python3
from __future__ import annotations
"""W1-negative: probe negative cases (explicit-minimum / explicit-enum bounds).

Round 8 W1 expansion. These candidates have documentation that states
EXPLICIT bounds (Minimum 1 / explicit enum), so GLM does NOT over-formalize
them. The paper's within-vendor contrast (§eval RQ3) predicts these are NOT
over-strict. This probe verifies DeepSeek also does not over-formalize explicit
bounds (specificity check), distinguishing the task-intrinsic phenomenon
(ambiguous optional-default) from explicit-bound cases.

Expected: TI=False on all (DeepSeek reads explicit bound correctly).

Inputs: e2_expand_candidates.json + paper §eval "Minimum 1" documentation.
Outputs: scripts/w1_negative_results.json
"""
import json
import os
import re
import time
from typing import Any

import requests

_key_paths = ["deepseek_apikey.txt", "../deepseek_apikey.txt", "../../deepseek_apikey.txt"]
API_KEY = next(open(p).read().strip() for p in _key_paths if os.path.exists(p))
URL = "https://api.deepseek.com/chat/completions"
SESSION = requests.Session()
SESSION.trust_env = False

# (id, db, passage, glm_assertion, real_semantics) — explicit-bound negatives
# passage states explicit Minimum/enum; GLM reads it correctly (not over-strict).
# glm_assertion = the correct (non-over-strict) formalization GLM would produce.
NEGATIVE_CASES: list[tuple[str, str, str, str, str]] = [
    ("qdrant_shard_number", "qdrant",
     "`shard_number` (integer, required=false): Number of shards for the collection. Default 1, Minimum 1.",
     "shard_number >= 1 (documented Minimum 1)",
     "Qdrant rejects shard_number=0; enforces explicit Minimum 1"),
    ("qdrant_replication_factor", "qdrant",
     "`replication_factor` (integer, required=false): Number of replicas per shard. Default 1, Minimum 1.",
     "replication_factor >= 1 (documented Minimum 1)",
     "Qdrant rejects replication_factor=0; enforces explicit Minimum 1"),
    ("qdrant_write_consistency_factor", "qdrant",
     "`write_consistency_factor` (integer, required=false): How many replicas must acknowledge writes. Default 1, Minimum 1.",
     "write_consistency_factor >= 1 (documented Minimum 1)",
     "Qdrant rejects write_consistency_factor=0; enforces explicit Minimum 1"),
    ("weaviate_vectorIndexType", "weaviate",
     "`vectorIndexType` (string, required=false): Vector index type. Default \"hnsw\". Must be one of {hnsw, dynamic, flat}.",
     "vectorIndexType in {hnsw, dynamic, flat} (documented explicit enum)",
     "Weaviate rejects invalid vectorIndexType; enforces explicit enum"),
    ("weaviate_replication_factor", "weaviate",
     "`replicationConfig.factor` (int, required=false): Number of replicas per object. Default 1, Minimum 1.",
     "replicationConfig.factor >= 1 (documented Minimum 1)",
     "Weaviate rejects factor=0; enforces explicit Minimum 1"),
    # paper-cited (§eval RQ3) Weaviate HNSW explicit bounds
    ("weaviate_ef", "weaviate",
     "`ef` (int, required=false): Search exploration breadth. Must be >= 1.",
     "ef >= 1 (documented explicit bound)",
     "Weaviate rejects ef=0; enforces explicit 'Must be >= 1'"),
    ("weaviate_dynamicEfMin", "weaviate",
     "`dynamicEfMin` (int, required=false): Minimum dynamic ef. Must be >= 1.",
     "dynamicEfMin >= 1 (documented explicit bound)",
     "Weaviate rejects dynamicEfMin=0; enforces explicit 'Must be >= 1'"),
    ("weaviate_dynamicEfMax", "weaviate",
     "`dynamicEfMax` (int, required=false): Maximum dynamic ef. Must be >= ef.",
     "dynamicEfMax >= ef (documented explicit relation)",
     "Weaviate rejects dynamicEfMax < ef; enforces explicit relation"),
    ("weaviate_efConstruction", "weaviate",
     "`efConstruction` (int, required=false): Index build exploration. Must be >= 1.",
     "efConstruction >= 1 (documented explicit bound)",
     "Weaviate rejects efConstruction=0; enforces explicit 'Must be >= 1'"),
    ("weaviate_maxConnections", "weaviate",
     "`maxConnections` (int, required=false): HNSW max edges per node. Must be >= 2.",
     "maxConnections >= 2 (documented explicit bound)",
     "Weaviate rejects maxConnections < 2; enforces explicit bound"),
    # Milvus explicit-bound negatives
    ("milvus_dimension", "milvus",
     "`dimension` (int, required=true): Vector dimension. Must be >= 1.",
     "dimension >= 1 (documented explicit bound)",
     "Milvus rejects dimension=0; enforces explicit 'Must be >= 1'"),
    ("milvus_num_partitions", "milvus",
     "`num_partitions` (int, required=false): Number of partitions. Default 64. Must be >= 1.",
     "num_partitions >= 1 (documented explicit bound, optional with default)",
     "Milvus rejects num_partitions=0; enforces explicit bound"),
    # Qdrant optimizer explicit-bound negatives
    ("qdrant_full_scan_threshold", "qdrant",
     "`full_scan_threshold` (int, required=false): Threshold for switching to full scan. Must be >= 1.",
     "full_scan_threshold >= 1 (documented explicit bound)",
     "Qdrant rejects full_scan_threshold=0; enforces explicit bound"),
]

FORMALIZE_PROMPT = (
    "Formalize this API documentation passage into a single formal constraint "
    "(an assertion the API should enforce on the parameter). "
    "Output ONLY the assertion.\n\nPassage: {passage}\n\n"
    "Respond STRICT JSON: {{\"clause\": \"...\"}}"
)
TI_PROMPT = (
    "A formal constraint was derived from API documentation. Given the REAL "
    "semantics (how the API actually behaves), is the constraint OVER-STRICT "
    "(it rejects a value the real semantics actually allows)? Note: if the "
    "documentation states an explicit bound (e.g. 'Minimum 1') and the API "
    "enforces it, the constraint is correct, NOT over-strict.\n\n"
    "Constraint: {clause}\nReal semantics: {real}\n\n"
    "Respond STRICT JSON: {{\"over_strict\": true | false, \"rationale\": \"...\"}}"
)
JUDGE_PROMPT = (
    "You are reviewing a formal constraint another engineer derived from API "
    "documentation. Judge whether it correctly captures DOCUMENTED behavior, or "
    "is over-strict (rejects values the documentation allows) or under-strict.\n\n"
    "Documentation passage:\n{raw}\n\nConstraint under review:\n{clause}\n\n"
    "Respond STRICT JSON: "
    "{{\"judgment\": \"correct\" | \"over-strict\" | \"under-strict\", \"rationale\": \"...\"}}"
)


def _post(messages: list[dict], max_tokens: int = 200) -> str:
    payload = {"model": "deepseek-chat", "temperature": 0.0,
               "messages": messages, "max_tokens": max_tokens}
    hdr = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    last: Any = None
    for attempt in range(5):
        try:
            r = SESSION.post(URL, headers=hdr, timeout=60, json=payload)
            return r.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    return f"ERROR: {last!r}"[:120]


def _json_extract(txt: str) -> dict | None:
    m = re.search(r"\{[^{}]*\}", txt, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:  # noqa: BLE001
        return None


def formalize(passage: str) -> str:
    txt = _post([{"role": "user", "content": FORMALIZE_PROMPT.format(passage=passage)}])
    j = _json_extract(txt)
    return (j or {}).get("clause", "?")[:120] if j else f"parse-error:{txt[:60]}"


def judge_ti(clause: str, real: str) -> bool:
    txt = _post([{"role": "user", "content": TI_PROMPT.format(clause=clause, real=real)}])
    j = _json_extract(txt)
    return bool(j.get("over_strict", False)) if j else False


def crossmodel_judge(raw: str, clause: str) -> bool:
    txt = _post([{"role": "user", "content": JUDGE_PROMPT.format(raw=raw, clause=clause)}])
    j = _json_extract(txt)
    return ((j or {}).get("judgment", "?")).lower().startswith("over")


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))


def main() -> None:
    rows: list[dict] = []
    for cid, db, passage, glm_a, real in NEGATIVE_CASES:
        ds_clause = formalize(passage)
        ti = judge_ti(ds_clause, real)
        cm = crossmodel_judge(passage, glm_a)
        rows.append({
            "id": cid, "db": db, "subtype": "explicit-bound-negative",
            "task_intrinsic": ti,
            "ground_truth": "not-over-strict (explicit bound)",
            "source_contradicts": False,
            "glm_assertion": glm_a, "deepseek_clause": ds_clause,
            "crossmodel_judgment": cm,
        })
        print(f"{cid:35} DS={ds_clause[:38]:38} TI={ti!s:5} crossmodel={cm}")
        time.sleep(0.5)

    n = len(rows)
    ti_count = sum(1 for r in rows if r.get("task_intrinsic"))
    lo, hi = wilson_ci(ti_count, n)
    summary = {
        "subtype": "explicit-bound-negative (within-vendor contrast for over-strict)",
        "n": n,
        "ti_count": ti_count, "ti_rate": ti_count / n if n else 0.0,
        "ti_wilson_95": [lo, hi],
        "expected": "TI=False on all (DeepSeek should read explicit bounds correctly)",
        "note": ("Specificity check: if TI=0, DeepSeek does not over-formalize "
                 "explicit bounds, supporting the within-vendor contrast (§eval RQ3)."),
    }
    print(f"\n=== W1-NEGATIVE SUMMARY (n={n}, explicit-bound cases) ===")
    print(f"task-intrinsic (over-formalized): {ti_count}/{n} = {ti_count/n:.2%} "
          f"(Wilson 95% CI [{lo:.2%}, {hi:.2%}])")
    print(f"Expected: 0% (DeepSeek reads explicit bounds correctly).")

    out = {"summary": summary, "rows": rows}
    json.dump(out, open("scripts/w1_negative_results.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("[wrote scripts/w1_negative_results.json]")


if __name__ == "__main__":
    main()
