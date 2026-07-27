#!/usr/bin/env python3
"""E2 Vein B DeepSeek: classify 6 new behavior gaps (idempotency/permissiveness).
Reuse w1_behavior_probe prompts. TI = DeepSeek's formalization is over-strict
given the real (idempotent) semantics.
"""
from __future__ import annotations
import json
import os
import re
import time
from typing import Any
import requests

_key_paths = ["deepseek_apikey.txt", "../deepseek_apikey.txt", "../../deepseek_apikey.txt"]
API_KEY = next(open(p).read().strip() for p in _key_paths if os.path.exists(p))
URL = "https://api.deepseek.com/chat/completions"
S = requests.Session()
S.trust_env = False

# (id, db, passage, glm_assertion, real_semantics)
CASES: list[tuple[str, str, str, str, str]] = [
    ("milvus_drop_nonexist_partition", "milvus",
     "Dropping a partition that does not exist should report an error (the partition is not found).",
     "drop on a non-existent partition MUST return a non-zero error ('partition not found')",
     "Milvus returns success (code=0) on dropping a non-existent partition (idempotent, by-design)."),
    ("milvus_create_exist_partition", "milvus",
     "Creating a partition with a name that already exists is an error.",
     "creating a partition with an existing name MUST return a non-zero error ('partition already exists')",
     "Milvus returns success on creating an already-existing partition (idempotent, by-design)."),
    ("milvus_release_not_loaded", "milvus",
     "Releasing a collection that is not currently loaded should report an error.",
     "release on a not-loaded collection MUST return a non-zero error ('collection not loaded')",
     "Milvus returns success on releasing a not-loaded collection (idempotent, by-design)."),
    ("milvus_create_exist_index", "milvus",
     "Creating an index that already exists on a field is an error.",
     "creating an already-existing index MUST return a non-zero error ('index already exists')",
     "Milvus returns success on creating an already-existing index (idempotent, by-design)."),
    ("milvus_load_already_loaded", "milvus",
     "Loading a collection that is already loaded should report an error.",
     "loading an already-loaded collection MUST return a non-zero error ('collection already loaded')",
     "Milvus returns success on loading an already-loaded collection (idempotent, by-design)."),
    ("qdrant_delete_nonexist_collection", "qdrant",
     "Deleting a collection that does not exist returns a 'not found' error.",
     "delete on a non-existent collection MUST return a not-found error",
     "Qdrant returns HTTP 200 success on deleting a non-existent collection (idempotent, by-design)."),
]

FORMALIZE = "Formalize this API documentation passage into a single formal constraint (an assertion the API should enforce on the operation). Output ONLY the assertion.\n\nPassage: {p}\n\nRespond STRICT JSON: {{\"clause\": \"...\"}}"
TI = "A formal constraint was derived from API documentation. Given the REAL semantics (how the API actually behaves), is the constraint OVER-STRICT (it rejects a behavior the real semantics actually allows)?\n\nConstraint: {c}\nReal semantics: {r}\n\nRespond STRICT JSON: {{\"over_strict\": true|false, \"rationale\": \"...\"}}"
JUDGE = "You are reviewing a formal constraint another engineer derived from API documentation. Judge whether it correctly captures DOCUMENTED behavior, or is over-strict (rejects behaviors the documentation allows).\n\nDocumentation passage:\n{raw}\n\nConstraint under review:\n{c}\n\nRespond STRICT JSON: {{\"judgment\": \"correct\"|\"over-strict\"|\"under-strict\", \"rationale\": \"...\"}}"


def post(msg: str) -> str:
    r = S.post(URL, headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
               json={"model": "deepseek-chat", "temperature": 0.0, "messages": [{"role": "user", "content": msg}], "max_tokens": 200},
               timeout=60)
    return r.json()["choices"][0]["message"]["content"].strip()


def jxtract(t: str) -> dict | None:
    m = re.search(r"\{[^{}]*\}", t, re.S)
    return json.loads(m.group(0)) if m else None


def main() -> None:
    rows = []
    for cid, db, passage, glm_a, real in CASES:
        ds = (jxtract(post(FORMALIZE.format(p=passage))) or {}).get("clause", "?")
        ti = bool((jxtract(post(TI.format(c=ds, r=real))) or {}).get("over_strict", False))
        cm = (jxtract(post(JUDGE.format(raw=passage, c=glm_a))) or {}).get("judgment", "?").lower().startswith("over")
        rows.append({"id": cid, "db": db, "subtype": "by-design-behavior", "ground_truth": "over-strict",
                     "task_intrinsic": ti, "glm_assertion": glm_a, "deepseek_clause": ds[:80],
                     "crossmodel_judgment": "caught" if cm else "missed", "source_contradicts": True})
        print(f"{cid:38} DS={ds[:38]:38} TI={ti!s:5} cm={'caught' if cm else 'missed'}")
        time.sleep(0.4)
    ti_n = sum(1 for r in rows if r["task_intrinsic"])
    cm_n = sum(1 for r in rows if r["crossmodel_judgment"] == "caught")
    print(f"\n=== Vein B: {len(rows)} behaviors, TI={ti_n}/{len(rows)}, cross-model caught={cm_n}/{len(rows)} ===")
    json.dump({"rows": rows, "ti": ti_n, "n": len(rows)}, open("scripts/e2_scale_behavior_results.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("[wrote scripts/e2_scale_behavior_results.json]")


if __name__ == "__main__":
    main()
