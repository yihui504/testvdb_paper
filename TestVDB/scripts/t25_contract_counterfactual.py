#!/usr/bin/env python3
"""T2.5 — Contract over-formalization counterfactual (Round 13).

Tests whether the over-strict constraints that caused the 12 by-design FPs are
GLM-5.2-specific or task-intrinsic, by feeding the SAME raw doc passage to
DeepSeek (different family) and checking if it reproduces the over-strict version.

Reframe (retroactive contract attribution): no new pipeline run needed; we test
whether a different LLM, given the same doc passage GLM saw, produces the same
over-strict constraint that the maintainer later called by-design.
"""
import json, os, sys, requests, time
sys.stdout.reconfigure(encoding="utf-8")

API_KEY = open("deepseek_apikey.txt").read().strip()
URL = "https://api.deepseek.com/chat/completions"
# Windows: requests reads system proxy from registry; force no-proxy
SESSION = requests.Session()
SESSION.trust_env = False

def deepseek_formalize(passage):
    """Ask DeepSeek to formalize a doc passage into constraint assertions."""
    prompt = (
        "You are a contract formalizer for a vector database REST API. "
        "Given the API documentation passage below, extract the formal constraint(s) "
        "as assertion(s) — code/math expressions a validator could check. "
        "Output ONLY the assertions, one per line (no prose, no preamble).\n\n"
        f"Passage: {passage}"
    )
    r = SESSION.post(URL, headers={"Authorization": f"Bearer {API_KEY}",
                                    "Content-Type": "application/json"}, timeout=40,
        json={"model": "deepseek-chat",
              "messages": [{"role": "user", "content": prompt}],
              "max_tokens": 200, "temperature": 0.0})
    return r.json()["choices"][0]["message"]["content"].strip()

# 4 test cases: (id, raw doc passage, GLM's over-strict assertion, what counts as "reproduced over-strict")
cases = [
    {
        "id": "q3_shardsNum",
        "raw": "`shardsNum` (integer, optional): Number of shards (default: 1)",
        "glm_assertion": "shardsNum >= 1",
        "over_strict_marker": ">= 1",  # over-strict: misses 0=default
        "note": "GLM inferred '>=1' from 'default:1'; real semantics: 0=DefaultShardNumber (use default)"
    },
    {
        "id": "q37_metricType",
        "raw": "`metricType` (string, optional): Supports L2, IP, COSINE. `consistencyLevel` (string, optional): Strong, Session, Bounded, Eventually",
        "glm_assertion": "metricType in ['L2','IP','COSINE']",
        "over_strict_marker": "in [",  # over-strict: empty/None should fall to default
        "note": "GLM inferred strict enum; real: empty=unspecified→default COSINE, invalid→Bounded fallback"
    },
    {
        "id": "q46_dimension",
        "raw": "dimension must be between 1 and 32768 for FloatVector",
        "glm_assertion": "dimension >= 1 && dimension <= 32768",
        "over_strict_marker": "32768",  # control: this matches doc (both GLM & DeepSeek should reproduce)
        "note": "CONTROL — bound matches doc; FP was 'too permissive' not 'wrong constraint'"
    },
    {
        "id": "q52_search_data",
        "raw": "`data` (array[array[float]], required): Query vector embeddings",
        "glm_assertion": "Array.isArray(data) && data.every(non-empty float array)",
        "over_strict_marker": "every",  # over-strict: empty array edge
        "note": "GLM inferred non-empty requirement; real: empty data=[] accepted (returns empty)"
    },
]

print("=" * 70)
print("T2.5 CONTRACT OVER-FORMALIZATION COUNTERFACTUAL")
print("GLM-5.2 (baseline) vs DeepSeek (different family), same doc passages")
print("=" * 70)

results = []
for c in cases:
    print(f"\n--- {c['id']} ---")
    print(f"raw passage: {c['raw']}")
    print(f"GLM assertion: {c['glm_assertion']}")
    try:
        ds = deepseek_formalize(c["raw"])
    except Exception as e:
        ds = f"ERROR: {e}"
    print(f"DeepSeek assertion:\n{ds}")
    # score: did DeepSeek reproduce the over-strict marker?
    reproduced = c["over_strict_marker"] in ds.replace(" ", " ").lower() or \
                 any(m in ds.lower() for m in [c["over_strict_marker"].lower()])
    # looser check for the marker
    reproduced = c["over_strict_marker"].lower() in ds.lower()
    verdict = "REPRODUCED over-strict" if reproduced else "DID NOT reproduce (less strict)"
    print(f"→ {verdict}")
    results.append({**c, "deepseek_assertion": ds, "reproduced_over_strict": reproduced})

# summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
reproduced_count = sum(1 for r in results if r["reproduced_over_strict"])
# q46 is a control (both should reproduce the factual bound)
clean_cases = [r for r in results if r["id"] != "q46_dimension"]
clean_reproduced = sum(1 for r in clean_cases if r["reproduced_over_strict"])
print(f"Total cases: {len(results)} (3 over-strict + 1 control)")
print(f"DeepSeek reproduced over-strict: {clean_reproduced}/3 over-strict cases")
print(f"Control (q46 dimension bound): {'reproduced (expected)' if results[2]['reproduced_over_strict'] else 'NOT reproduced'}")
print()
if clean_reproduced >= 2:
    print(f"→ {clean_reproduced}/3 reproduced → over-formalization is TASK-INTRINSIC (DeepSeek also over-formalizes)")
elif clean_reproduced <= 1:
    print(f"→ {clean_reproduced}/3 reproduced → over-formalization is GLM-SPECIFIC (DeepSeek does not over-formalize)")
else:
    print(f"→ ambiguous split")

with open("TestVDB/scripts/t25_counterfactual_results.json", "w", encoding="utf-8") as f:
    json.dump({"glm_baseline": "GLM-5.2", "counterfactual": "DeepSeek (deepseek-chat/v4-flash)",
               "temperature": 0.0, "results": results,
               "reproduced_over_strict_count": clean_reproduced,
               "clean_n": len(clean_cases)}, f, indent=2, ensure_ascii=False)
print("\nSaved TestVDB/scripts/t25_counterfactual_results.json")
