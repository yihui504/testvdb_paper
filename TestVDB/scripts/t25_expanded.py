#!/usr/bin/env python3
"""T2.5-expanded — Contract over-formalization counterfactual (Round 16).

Extends the Round-13 N=3 DeepSeek counterfactual to N=10 by adding seven
by-design-prone parameter descriptions rooted in the paper's documented
by-design cases (Section 4: lenient defaults, idempotent accepts,
eventual-consistency intermediates, fallback semantics). Tests whether a
different LLM family (DeepSeek) reproduces the over-strict reading that
GLM-5.2 produced, i.e. whether over-formalization is task-intrinsic.

Each case carries (raw passage, over-strict tendency, control flag).
Output is the full DeepSeek assertion so each verdict is human-verifiable,
not just a regex marker.
"""
import json
import os
import sys
import requests

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = open("deepseek_apikey.txt", encoding="utf-8").read().strip()
URL = "https://api.deepseek.com/chat/completions"
SESSION = requests.Session()
SESSION.trust_env = False  # bypass Windows system proxy


def deepseek_formalize(passage: str) -> str:
    prompt = (
        "You are a contract formalizer for a vector database REST API. "
        "Given the API documentation passage below, extract the formal constraint(s) "
        "as assertion(s) --- code/math expressions a validator could check. "
        "Output ONLY the assertions, one per line (no prose, no preamble).\n\n"
        f"Passage: {passage}"
    )
    r = SESSION.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        timeout=40,
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200,
            "temperature": 0.0,
        },
    )
    return r.json()["choices"][0]["message"]["content"].strip()


# 10 cases: 9 over-strict-prone + 1 control. Passages are real Milvus v2.6.x
# REST parameter descriptions; over_strict names the tendency GLM-5.2 showed.
CASES = [
    {
        "id": "c1_shardsNum",
        "raw": "`shardsNum` (integer, optional): Number of shards. Default: 1.",
        "over_strict": "infer '>=1' or 'required', missing that 0 means use-default",
        "marker": [">= 1", ">=1", "> 0", "must be"],
        "control": False,
    },
    {
        "id": "c2_metricType",
        "raw": "`metricType` (string, optional): Distance metric type. Allowed values: L2, IP, COSINE.",
        "over_strict": "infer strict enum membership / reject on missing, missing that omitted or invalid falls back to a default",
        "marker": ["in (", "in [", "must be one of", "must equal"],
        "control": False,
    },
    {
        "id": "c3_dimension",
        "raw": "`dimension` (integer, required): Vector dimension. Must be between 1 and 32768 for FloatVector fields.",
        "over_strict": "CONTROL --- factual bound; both GLM and DeepSeek should reproduce 1..32768",
        "marker": ["32768", "1"],
        "control": True,
    },
    {
        "id": "c4_consistencyLevel",
        "raw": "`consistencyLevel` (string, optional): Read consistency. Allowed: Strong, Session, Bounded, Eventually. Default: Bounded.",
        "over_strict": "infer strict enum + required, missing that missing/invalid falls back to Bounded",
        "marker": ["in (", "in [", "must be one of", "must equal"],
        "control": False,
    },
    {
        "id": "c5_data_search",
        "raw": "`data` (array of float arrays, required): Query vectors for ANN search.",
        "over_strict": "infer every element must be a non-empty valid vector, missing that edge cases (empty) may be tolerated",
        "marker": ["every", "non-empty", "length > 0", "must not be empty"],
        "control": False,
    },
    {
        "id": "c6_outputFields",
        "raw": "`outputFields` (array of strings, optional): Fields to include in results. If omitted, all fields are returned.",
        "over_strict": "infer required or non-empty, missing that omitted means return all",
        "marker": ["required", "non-empty", "must", "length > 0"],
        "control": False,
    },
    {
        "id": "c7_limit",
        "raw": "`limit` (integer, optional): Maximum number of results to return. Default: 0 (returns all matches).",
        "over_strict": "infer '>=1', missing that 0 means no limit",
        "marker": [">= 1", ">=1", "> 0", "must be >"],
        "control": False,
    },
    {
        "id": "c8_roundDecimal",
        "raw": "`roundDecimal` (integer, optional): Decimal places to round distances to. Default: -1 (no rounding).",
        "over_strict": "infer '>=0', missing that -1 means no rounding",
        "marker": [">= 0", ">=0", ">= 1", "must be >"],
        "control": False,
    },
    {
        "id": "c9_offset",
        "raw": "`offset` (integer, optional): Number of results to skip. Default: 0.",
        "over_strict": "infer '>=1', missing that 0 means skip none",
        "marker": [">= 1", ">=1", "> 0", "must be >"],
        "control": False,
    },
    {
        "id": "c10_dbName",
        "raw": "`dbName` (string, optional): Target database name. Default: 'default'.",
        "over_strict": "infer required or non-empty, missing that omitted uses the default database",
        "marker": ["required", "non-empty", "must"],
        "control": False,
    },
]

print("=" * 70)
print("T2.5-EXPANDED CONTRACT OVER-FORMALIZATION COUNTERFACTUAL (N=10)")
print("DeepSeek vs GLM-5.2, same doc passages (by-design-prone Milvus params)")
print("=" * 70)

results = []
for c in CASES:
    print(f"\n--- {c['id']} {'[CONTROL]' if c['control'] else ''} ---")
    print(f"passage: {c['raw']}")
    print(f"GLM over-strict tendency: {c['over_strict']}")
    try:
        ds = deepseek_formalize(c["raw"])
    except Exception as e:
        ds = f"ERROR: {e}"
    print(f"DeepSeek assertion:\n{ds}")
    low = ds.lower()
    hit = any(m.lower() in low for m in c["marker"])
    verdict = ("reproduced over-strict" if hit else "less strict / acknowledges default")
    print(f"marker hit: {hit} -> auto-verdict: {verdict}")
    results.append({**c, "deepseek_assertion": ds, "marker_hit": hit})

clean = [r for r in results if not r["control"]]
reproduced = sum(1 for r in clean if r["marker_hit"])
ctrl = [r for r in results if r["control"]][0]
print("\n" + "=" * 70)
print(f"OVER-STRICT CASES: {reproduced}/{len(clean)} reproduced by DeepSeek")
print(f"CONTROL ({ctrl['id']}): marker hit = {ctrl['marker_hit']} (expected: reproduce factual bound)")

with open("TestVDB/scripts/t25_expanded_results.json", "w", encoding="utf-8") as f:
    json.dump(
        {
            "glm_baseline": "GLM-5.2",
            "counterfactual": "DeepSeek (deepseek-chat)",
            "temperature": 0.0,
            "n_over_strict": len(clean),
            "n_reproduced": reproduced,
            "results": results,
        },
        f,
        indent=2,
        ensure_ascii=False,
    )
print("\nSaved TestVDB/scripts/t25_expanded_results.json")
