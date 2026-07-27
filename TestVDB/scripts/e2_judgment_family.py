#!/usr/bin/env python3
"""E2-judgment with a configurable LLM family — task-intrinsic probe.

Generalizes e2_judgment_longcat.py to any OpenAI-compatible chat API. Tests
whether a third/fourth family reproduces GLM's over-strict clauses (TI) and/or
judges them as over-strict.

Config (env):
  FAMILY    : label for output file + interpretation (e.g. r1, llama33)
  URL       : chat completions endpoint
  MODEL     : model name
  KEY_FILE  : path to file containing API key (one line)
  MAX_TOKENS: override (default 2000; reasoning models need room)

Usage:
  FAMILY=r1 URL=https://api.deepseek.com/chat/completions MODEL=deepseek-reasoner \
    KEY_FILE=deepseek_apikey.txt python e2_judgment_family.py
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

FAMILY = os.environ.get("FAMILY", "unknown")
URL = os.environ.get("URL", "")
MODEL = os.environ.get("MODEL", "")
KEY_FILE = os.environ.get("KEY_FILE", "")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "2000"))

if not (URL and MODEL and KEY_FILE):
    sys.exit("[FAIL] set URL= MODEL= KEY_FILE= FAMILY= env vars")

try:
    API_KEY = open(KEY_FILE).read().strip()
except FileNotFoundError:
    sys.exit(f"[FAIL] key file not found: {KEY_FILE}")

S = requests.Session()
S.trust_env = False

# 6 confirmed TI clauses (Milvus 2 + Qdrant 4) — identical to e2_judgment_longcat.py
CASES: list[tuple[str, str, str, str, str, str]] = [
    ("shardsNum", "milvus", "shardsNum",
     "`shardsNum` (integer, optional): Number of shards (default: 1).",
     "shardsNum >= 1", "0 means use the default shard number"),
    ("data_search", "milvus", "data",
     "`data` (array[array[float]], required): Query vector embeddings.",
     "data must be a non-empty array of non-empty float arrays",
     "an empty data array is tolerated (returns empty)"),
    ("timeout", "qdrant", "timeout",
     "`timeout` (integer, optional): Wait timeout in seconds for the operation "
     "to be applied. Default: 0 (no wait).",
     "timeout >= 1", "0 means no wait (async)"),
    ("group_size", "qdrant", "group_size",
     "`group_size` (integer, optional): Maximum number of points in a single "
     "group returned by grouped search. Default: 1000.",
     "group_size >= 1", "0 is accepted (returns empty groups)"),
    ("score_threshold", "qdrant", "score_threshold",
     "`score_threshold` (float, optional): Define a minimal score threshold for "
     "the search result. Default: null (no threshold).",
     "score_threshold in [0, 1]", "values like 2.0/-0.5 accepted"),
    ("bits", "qdrant", "bits",
     "`bits` (integer, optional): Compression bit-width for product/scalar "
     "quantization. Default: 8.",
     "bits >= 1", "0 is accepted"),
]

PROMPT_F = ("You translate API documentation into checkable assertions. Output "
            "ONLY the single most specific assertion (or 'no constraint stated') "
            "for the named parameter, based strictly on the passage. Do not "
            "invent bounds the passage does not state.\n\n"
            "Parameter: {param}\nPassage: {passage}\nAssertion:")
PROMPT_J = ("You judge whether a test assertion is supported by API documentation. "
            "Reply with exactly one label then one sentence: 'YES_overstrict' "
            "(the assertion is stricter than the documentation states, i.e. rejects "
            "values the doc allows) or 'NO_supported' (the documentation supports "
            "it).\n\nAssertion under review: {clause}\nParameter: {param}\n"
            "Documentation passage: {passage}\nLabel:")


def ask(system: str, user: str) -> str:
    is_ollama = "ollama.com" in URL
    hdr = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload: dict[str, Any] = {
        "model": MODEL,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "temperature": 0,
    }
    if is_ollama:
        payload["stream"] = False
        payload["options"] = {"num_predict": MAX_TOKENS}
    else:
        payload["max_tokens"] = MAX_TOKENS
    last: Any = None
    for attempt in range(5):
        try:
            r = S.post(URL, headers=hdr, json=payload, timeout=180)
            j = r.json()
            if is_ollama:
                content = (j.get("message") or {}).get("content") or ""
                if not content.strip():
                    return f"[ollama empty: {str(j)[:120]}]"
                return content.strip()
            content = (j["choices"][0]["message"].get("content") or "").strip()
            if content:
                return content
            rc = j["choices"][0]["message"].get("reasoning_content") or ""
            fr = j["choices"][0].get("finish_reason")
            return f"[content_empty finish={fr} reasoning_head={rc[:80]!r}]"
        except Exception as e:
            last = e
            time.sleep(2 * (attempt + 1))
    return f"[call-error: {repr(last)[:120]}]"


def formalize(c: tuple[str, str, str, str, str, str]) -> str:
    sys_p = ("You translate API documentation into checkable assertions. Output "
             "ONLY the single most specific assertion (or 'no constraint stated') "
             "for the named parameter, based strictly on the passage. Do not "
             "invent bounds the passage does not state.")
    return ask(sys_p, PROMPT_F.format(param=c[2], passage=c[3]))


def judge(c: tuple[str, str, str, str, str, str]) -> str:
    sys_p = ("You judge whether a test assertion is supported by API documentation. "
             "Reply with exactly one label then one sentence: 'YES_overstrict' "
             "(the assertion is stricter than the documentation states) or "
             "'NO_supported' (the documentation supports it).")
    return ask(sys_p, PROMPT_J.format(clause=c[4], param=c[2], passage=c[3]))


def is_over_strict(f: str) -> bool:
    """Numeric/categorical bound the passage does not state (type-only doesn't count)."""
    f = f.lower()
    if any(k in f for k in ("no constraint", "unstated", "no minimum", "no bound", "not stated")):
        return False
    return bool(re.search(
        r"(\b>=\s*\d|>\s*0\b|\bat least\s+\d|\bminimum\s+\d|"
        r"\bin\s*\[\s*-?\d|\bbetween\s+\d|\bmust be (one of|in)\b|\b∈\s*\[)", f))


def main() -> None:
    print(f"=== family={FAMILY} model={MODEL} url={URL} max_tokens={MAX_TOKENS} ===\n")
    results: list[dict[str, Any]] = []
    for c in CASES:
        cid, db, param, passage, glm_clause, real = c
        t0 = time.time()
        fam_clause = formalize(c)
        t1 = time.time()
        ti = is_over_strict(fam_clause)
        verdict = judge(c)
        t2 = time.time()
        caught = "YES_overstrict" in verdict
        row = {"id": cid, "db": db, "param": param, "glm_clause": glm_clause,
               "family_clause": fam_clause, "real_semantics": real,
               "ti_hold": bool(ti),
               "crossmodel_judgment": "caught" if caught else "missed",
               "verdict_raw": verdict,
               "time_formalize_s": round(t1 - t0, 1),
               "time_judge_s": round(t2 - t1, 1)}
        results.append(row)
        print(f"[{cid:16}] {db:6} fam={fam_clause[:38]:38} TI={ti}  judge={verdict[:30]}")

    out = f"e2_judgment_{FAMILY}_results.json"
    json.dump({"family": FAMILY, "model": MODEL, "url": URL, "cases": results},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    ti_n = sum(1 for r in results if r["ti_hold"])
    caught_n = sum(1 for r in results if r["crossmodel_judgment"] == "caught")
    print(f"\n=== {FAMILY} on 6 TI clauses: TI_hold={ti_n}/6, judge_caught={caught_n}/6 ===")
    print(f"[wrote {out}]")


if __name__ == "__main__":
    main()
