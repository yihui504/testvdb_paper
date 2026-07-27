#!/usr/bin/env python3
"""E2-judgment with a third LLM family (longcat) — task-intrinsic probe.

Replicates e2_judgment.py's cross-model judging paradigm but with longcat as
the second LLM family (instead of DeepSeek) on the 6 confirmed task-intrinsic
(TI) over-strict clauses (Milvus 2 + Qdrant 4).

For each TI clause, two queries:
  (1) independent_formalize: longcat independently formalizes the doc passage;
      TI-hold if it also produces an over-strict bound the passage does not state
  (2) judge: longcat judges whether GLM's over-strict clause is supported by
      the passage -> caught (flags over-strict) vs missed

Goal: test whether the TI convergence observed with DeepSeek (2-family) holds
with a third family. If longcat also over-formalizes the same clauses, the TI
claim strengthens from binary (DeepSeek agrees with GLM) to family-set
convergence. If longcat disagrees on a clause, that clause is downgraded from
TI to family-specific (GLM+DeepSeek shared bias).

Inputs: 6 TI clauses (Milvus shardsNum/data_search + Qdrant timeout/group_size/
score_threshold/bits), passages from Qdrant/Milvus API docs.
Output: scripts/e2_judgment_longcat_results.json
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from typing import Any

import requests

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# === longcat API config (OpenAI-compatible; fill these) =====================
# Place key in scripts/longcat_apikey.txt (one line). Override URL/MODEL via env
# if longcat is hosted elsewhere (DashScope / SiliconFlow / self-hosted).
_key_paths = ["longcat_apikey.txt", "../longcat_apikey.txt", "../../longcat_apikey.txt"]
API_KEY = next((open(p).read().strip() for p in _key_paths if os.path.exists(p)), "")
URL = os.environ.get("LONGCAT_URL", "https://api.longcat.chat/openai/v1/chat/completions")
MODEL = os.environ.get("LONGCAT_MODEL", "LongCat-2.0")
# ===========================================================================

S = requests.Session()
S.trust_env = False

if not API_KEY:
    print("[WARN] longcat_apikey.txt not found — set LONGCAT_URL/LONGCAT_MODEL env")
    print(f"       URL={URL}  MODEL={MODEL}")


# 6 confirmed TI clauses (Milvus 2 + Qdrant 4).
# (id, db, param, passage, glm_clause, real_semantics)
CASES: list[tuple[str, str, str, str, str, str]] = [
    # --- Milvus 2 TI (from scripts/e2_judgment.py) ---
    ("shardsNum", "milvus", "shardsNum",
     "`shardsNum` (integer, optional): Number of shards (default: 1).",
     "shardsNum >= 1",
     "0 means use the default shard number"),
    ("data_search", "milvus", "data",
     "`data` (array[array[float]], required): Query vector embeddings.",
     "data must be a non-empty array of non-empty float arrays",
     "an empty data array is tolerated (returns empty)"),
    # --- Qdrant 4 TI (passages from Qdrant v1.18.2 API docs; GLM clauses per
    #     e2_qdrant_probe.py / e2_scale_probe_veinA.py) ---
    ("timeout", "qdrant", "timeout",
     "`timeout` (integer, optional): Wait timeout in seconds for the operation "
     "to be applied. Default: 0 (no wait).",
     "timeout >= 1",
     "0 means no wait (async); Qdrant accepts the request without enforcing >=1"),
    ("group_size", "qdrant", "group_size",
     "`group_size` (integer, optional): Maximum number of points in a single "
     "group returned by grouped search. Default: 1000.",
     "group_size >= 1",
     "0 is accepted (returns empty groups); no minimum stated"),
    ("score_threshold", "qdrant", "score_threshold",
     "`score_threshold` (float, optional): Define a minimal score threshold for "
     "the search result. Only points with scores above this threshold are "
     "returned. Default: null (no threshold).",
     "score_threshold in [0, 1]",
     "values like 2.0 and -0.5 are accepted (Cosine range is [0,1]); no bound enforced"),
    ("bits", "qdrant", "bits",
     "`bits` (integer, optional): Compression bit-width for product/scalar "
     "quantization. Default: 8.",
     "bits >= 1",
     "0 is accepted (degenerate quantization); no minimum stated"),
]

PROMPT_FORMALIZE = (
    "You translate API documentation into checkable assertions. Output ONLY the "
    "single most specific assertion (or 'no constraint stated') for the named "
    "parameter, based strictly on the passage. Do not invent bounds the passage "
    "does not state.\n\n"
    "Parameter: {param}\nPassage: {passage}\nAssertion:"
)

PROMPT_JUDGE = (
    "You judge whether a test assertion is supported by API documentation. Reply "
    "with exactly one label then one sentence: 'YES_overstrict' (the assertion is "
    "stricter than the documentation states, i.e. rejects values the doc allows) "
    "or 'NO_supported' (the documentation supports it).\n\n"
    "Assertion under review: {clause}\n"
    "Parameter: {param}\n"
    "Documentation passage: {passage}\nLabel:"
)


def ask(system: str, user: str) -> str:
    hdr = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": 1000,  # longcat-2.0 is a reasoning model (~300 reasoning tokens)
        "temperature": 0,
    }
    last: Any = None
    for attempt in range(5):
        try:
            r = S.post(URL, headers=hdr, json=payload, timeout=60)
            return r.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            last = e
            time.sleep(2 * (attempt + 1))
    return f"[call-error: {repr(last)[:120]}]"


def independent_formalize(c: tuple[str, str, str, str, str, str]) -> str:
    sys_p = (
        "You translate API documentation into checkable assertions. Output ONLY "
        "the single most specific assertion (or 'no constraint stated') for the "
        "named parameter, based strictly on the passage. Do not invent bounds the "
        "passage does not state."
    )
    user = f"Parameter: {c[2]}\nPassage: {c[3]}\nAssertion:"
    return ask(sys_p, user)


def judge(c: tuple[str, str, str, str, str, str]) -> str:
    sys_p = (
        "You judge whether a test assertion is supported by API documentation. "
        "Reply with exactly one label then one sentence: 'YES_overstrict' (the "
        "assertion is stricter than the documentation states) or 'NO_supported' "
        "(the documentation supports it)."
    )
    user = (
        f"Assertion under review: {c[4]}\nParameter: {c[2]}\n"
        f"Documentation passage: {c[3]}\nLabel:"
    )
    return ask(sys_p, user)


def is_over_strict(formalization: str) -> bool:
    """longcat's formalization imposes a NUMERIC/CATEGORICAL bound the passage does not state.

    Type-only constraints ("must be an integer", "must be an array of arrays") do
    NOT count as over-strict — the over-strict phenomenon is about value bounds
    (>= N, > 0, at least N, minimum N, in [a,b]) that the passage does not state.
    """
    f = formalization.lower()
    if any(k in f for k in ("no constraint", "unstated", "no minimum", "no bound", "not stated")):
        return False
    # Explicit numeric/categorical bound (must include a number or enumerated set)
    return bool(
        re.search(
            r"(\b>=\s*\d|>\s*0\b|\bat least\s+\d|\bminimum\s+\d|"
            r"\bin\s*\[\s*-?\d|\bbetween\s+\d|\bmust be (one of|in)\b|\b∈\s*\[)",
            f,
        )
    )


def main() -> None:
    if not API_KEY:
        sys.exit("[FAIL] no API key — create scripts/longcat_apikey.txt")

    results: list[dict[str, Any]] = []
    for c in CASES:
        cid, db, param, passage, glm_clause, real = c
        longcat_clause = independent_formalize(c)
        ti_hold = is_over_strict(longcat_clause)
        verdict = judge(c)
        caught = "YES_overstrict" in verdict
        row = {
            "id": cid,
            "db": db,
            "param": param,
            "glm_clause": glm_clause,
            "longcat_clause": longcat_clause,
            "real_semantics": real,
            "ti_hold_longcat": bool(ti_hold),
            "crossmodel_judgment": "caught" if caught else "missed",
            "verdict_raw": verdict,
        }
        results.append(row)
        print(
            f"[{cid:16}] {db:6} longcat={longcat_clause[:40]:40} "
            f"TI_hold={ti_hold}  judge={verdict[:35]}"
        )

    out = "e2_judgment_longcat_results.json"
    json.dump(
        {"model": MODEL, "url": URL, "cases": results},
        open(out, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=2,
    )

    ti_n = sum(1 for r in results if r["ti_hold_longcat"])
    caught_n = sum(1 for r in results if r["crossmodel_judgment"] == "caught")
    print(f"\n=== longcat on 6 TI clauses: TI_hold={ti_n}/6, judge_caught={caught_n}/6 ===")
    print(f"[wrote {out}]")

    # Verdict interpretation
    print("\n--- Interpretation ---")
    if ti_n == 6:
        print("longcat reproduces ALL 6 TI clauses -> 3-family convergence (GLM+DeepSeek+longcat)")
        print("TI claim strengthens from binary to family-set statistic.")
    elif ti_n >= 4:
        print(f"longcat reproduces {ti_n}/6 -> partial convergence; downgrade {6 - ti_n} clause(s)")
        print("to family-specific. TI claim holds on majority with 3-family support.")
    else:
        print(f"longcat reproduces only {ti_n}/6 -> TI claim WEAKENED.")
        print("Most clauses are GLM+DeepSeek shared bias, not documentation-intrinsic.")


if __name__ == "__main__":
    main()
