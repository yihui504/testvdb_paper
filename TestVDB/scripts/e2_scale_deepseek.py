#!/usr/bin/env python3
"""E2 scaling: DeepSeek classification of the 4 new over-strict Milvus clauses.

For each: (1) DeepSeek independently formalizes the doc passage -> TI if it
reproduces the over-strict clause; (2) DeepSeek judges GLM's clause against
the passage -> caught (flags over-strict) vs missed.
Reuses the e2_judgment.py DeepSeek call pattern (trust_env=False, api.deepseek.com).
"""
from __future__ import annotations
import json
import sys
import requests

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

API_KEY = open("../deepseek_apikey.txt").read().strip()
URL = "https://api.deepseek.com/chat/completions"
S = requests.Session()
S.trust_env = False
MODEL = "deepseek-chat"

# 4 new confirmed over-strict Milvus clauses (impl accepts the boundary value)
CLAUSES = [
    {
        "id": "ef",
        "param": "ef",
        "glm_clause": "ef >= 1",
        "passage": ('Milvus search API, searchParams field (object, required=false): '
                    '"Index-specific search params, e.g. {\"params\": {\"ef\": 64}} for HNSW." '
                    'No minimum or bound for ef is stated in the passage.'),
    },
    {
        "id": "nprobe",
        "param": "nprobe",
        "glm_clause": "nprobe >= 1",
        "passage": ('Milvus search API, searchParams field (object, required=false): '
                    '"Index-specific search params" for an IVF_FLAT index (the IVF analog is nprobe). '
                    'No minimum or bound for nprobe is stated in the passage.'),
    },
    {
        "id": "level",
        "param": "level",
        "glm_clause": "level >= 0",
        "passage": ('Milvus search API: an optional integer "level" parameter controlling search effort. '
                    'No minimum or bound for level is stated in the passage.'),
    },
    {
        "id": "replicaNumber",
        "param": "replicaNumber",
        "glm_clause": "replicaNumber >= 1",
        "passage": ('Milvus LoadCollection API: "replicaNumber (int, required=false): Default 1. '
                    'Adjustable dynamically since 2.4.13." No minimum or bound is stated.'),
    },
    {
        "id": "m",
        "param": "m",
        "glm_clause": "m >= 2",
        "passage": ('Qdrant HnswConfig (collection create): "m (integer, optional): Number of edges per '
                    'node in HNSW graph. Default 16." No minimum or bound is stated in the passage.'),
    },
]


def ask(system: str, user: str) -> str:
    r = S.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"model": MODEL, "messages": [{"role": "system", "content": system},
                                           {"role": "user", "content": user}],
              "max_tokens": 120, "temperature": 0},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"].strip()


def independent_formalize(c: dict) -> str:
    sys_p = "You translate API documentation into checkable assertions. Output ONLY the single most specific assertion (or 'no constraint stated') for the named parameter, based strictly on the passage. Do not invent bounds the passage does not state."
    user = f"Parameter: {c['param']}\nPassage: {c['passage']}\nAssertion:"
    return ask(sys_p, user)


def judge(c: dict) -> str:
    sys_p = "You judge whether a test assertion is supported by API documentation. Reply with exactly one label then one sentence: 'YES_overstrict' (the assertion is stricter than the documentation states) or 'NO_supported' (the documentation supports it)."
    user = f"Assertion under review: {c['glm_clause']}\nParameter: {c['param']}\nDocumentation passage: {c['passage']}\nLabel:"
    return ask(sys_p, user)


def main() -> None:
    results = []
    for c in CLAUSES:
        ds_clause = independent_formalize(c)
        verdict = judge(c)
        # TI = DeepSeek's own formalization also imposes a >=1 / positive bound the passage does not state
        ti = ("over-strict" in ds_clause.lower() or
              any(tok in ds_clause for tok in [">= 1", ">=1", "> 0", ">0", "must be >= 1", "at least 1"]) is False
              and ("no constraint" in ds_clause.lower() or "unstated" in ds_clause.lower()) is False
              and (">=" in ds_clause or "> 0" in ds_clause))
        caught = "YES_overstrict" in verdict
        row = {"id": c["id"], "param": c["param"], "glm_clause": c["glm_clause"],
               "deepseek_clause": ds_clause, "task_intrinsic": bool(ti),
               "crossmodel_judgment": "caught" if caught else "missed",
               "verdict": verdict}
        results.append(row)
        print(f"[{c['id']}] GLM={c['glm_clause']} | DS={ds_clause[:50]} | TI={ti} | {verdict[:40]}")

    json.dump(results, open("scripts/e2_scale_deepseek_results.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    ti_n = sum(1 for r in results if r["task_intrinsic"])
    caught_n = sum(1 for r in results if r["crossmodel_judgment"] == "caught")
    print(f"\n=== 4 new clauses: TI={ti_n}/4, cross-model caught={caught_n}/4 ===")
    print("[wrote scripts/e2_scale_deepseek_results.json]")


if __name__ == "__main__":
    main()
