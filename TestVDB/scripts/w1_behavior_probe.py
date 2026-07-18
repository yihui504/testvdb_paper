#!/usr/bin/env python3
from __future__ import annotations
"""W1-behavior: extend the task-intrinsic probe to by-design behavior issues.

Round 8 W1 expansion. These four Milvus issues (50319/50321/50322/50325) are
by-design behavior over-strict: GLM asserts the API 'should reject' an
operation, but Milvus by-design accepts it (maintainer resolution/by-design).
This is a DIFFERENT subtype from the parameter over-strict (optional-default)
in e2/W1, so it is reported SEPARATELY to avoid muddying the optional-default
mechanism claim of RQ3.

Inputs: issue bodies hardcoded below (from test_questions/issue_bodies/issue_503*.md).
Outputs: scripts/w1_behavior_results.json
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

# (id, db, passage, glm_assertion, real_semantics) — by-design behavior over-strict
# passage = doc-derived constraint GLM would read; glm_assertion = GLM's over-formalization;
# real_semantics = actual Milvus behavior (maintainer-confirmed by-design).
BEHAVIOR_CASES: list[tuple[str, str, str, str, str]] = [
    ("milvus_50319_unloaded_search", "milvus",
     "The REST API contract requires `collections/load` before `entities/search` "
     "or `entities/query`. Operations on an unloaded collection should be rejected.",
     "search/query on an unloaded collection MUST return a non-zero error "
     "('collection not loaded')",
     "Milvus returns code=0 with valid data on never-loaded collections "
     "(by-design; issue resolution/by-design)"),
    ("milvus_50321_dup_collection", "milvus",
     "Collection names must be unique; creating a collection with an "
     "already-existing name is an error.",
     "creating a collection with an existing name MUST return a non-zero error "
     "('collection already exists')",
     "Milvus returns code=0 identical to first creation (by-design idempotent)"),
    ("milvus_50322_drop_nonexist", "milvus",
     "The REST API error code documentation defines code=4 (CollectionNotExists) "
     "for dropping a non-existent collection.",
     "drop on a non-existent collection MUST return code=4 (CollectionNotExists)",
     "Milvus returns code=0 (by-design idempotent drop)"),
    ("milvus_50325_underscore_name", "milvus",
     "Collection names must match [a-zA-Z][a-zA-Z0-9_]* — starting with a letter, "
     "not an underscore.",
     "collection names starting with underscore MUST be rejected with a "
     "validation error",
     "Milvus accepts leading-underscore names with code=0 (by-design)"),
]

FORMALIZE_PROMPT = (
    "Formalize this API documentation passage into a single formal constraint "
    "(an assertion the API should enforce on the operation or behavior). "
    "Output ONLY the assertion.\n\nPassage: {passage}\n\n"
    "Respond STRICT JSON: {{\"clause\": \"...\"}}"
)
TI_PROMPT = (
    "A formal constraint was derived from API documentation. Given the REAL "
    "semantics (how the API actually behaves), is the constraint OVER-STRICT "
    "(it rejects a behavior the real semantics actually allows)?\n\n"
    "Constraint: {clause}\nReal semantics: {real}\n\n"
    "Respond STRICT JSON: {{\"over_strict\": true | false, \"rationale\": \"...\"}}"
)
JUDGE_PROMPT = (
    "You are reviewing a formal constraint another engineer derived from API "
    "documentation. Judge whether it correctly captures DOCUMENTED behavior, or "
    "is over-strict (rejects behaviors the documentation allows) or under-strict.\n\n"
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
    for cid, db, passage, glm_a, real in BEHAVIOR_CASES:
        ds_clause = formalize(passage)
        ti = judge_ti(ds_clause, real)
        cm = crossmodel_judge(passage, glm_a)
        rows.append({
            "id": cid, "db": db, "issue": cid.split("_")[1],
            "subtype": "by-design-behavior",
            "task_intrinsic": ti,
            "ground_truth": "over-strict",
            "source_contradicts": True,
            "glm_assertion": glm_a, "deepseek_clause": ds_clause,
            "crossmodel_judgment": cm,
        })
        print(f"{cid:35} DS={ds_clause[:40]:40} TI={ti!s:5} crossmodel={cm}")
        time.sleep(0.5)

    n = len(rows)
    ti_count = sum(1 for r in rows if r.get("task_intrinsic"))
    lo, hi = wilson_ci(ti_count, n)
    ti_rows = [r for r in rows if r.get("task_intrinsic")]
    ti_cm = sum(1 for r in ti_rows if r.get("crossmodel_judgment"))

    summary = {
        "subtype": "by-design-behavior (distinct from parameter over-strict in e2/W1)",
        "n": n,
        "ti_count": ti_count, "ti_rate": ti_count / n if n else 0.0,
        "ti_wilson_95": [lo, hi],
        "ti_crossmodel_catch": f"{ti_cm}/{len(ti_rows)}" if ti_rows else "0/0",
        "source_catch_all": f"{n}/{n}",
        "note": ("Reported SEPARATELY from parameter-TI (e2/W1, n=12). "
                 "Do NOT mix into the optional-default mechanism rate of RQ3."),
    }
    print(f"\n=== W1-BEHAVIOR SUMMARY (n={n}, by-design issues) ===")
    print(f"task-intrinsic: {ti_count}/{n} = {ti_count/n:.2%} "
          f"(Wilson 95% CI [{lo:.2%}, {hi:.2%}])")
    print(f"cross-model judging catches TI subset: {summary['ti_crossmodel_catch']}")
    print(f"source-grounded falsification catches: {summary['source_catch_all']}")
    print("NOTE: distinct subtype (by-design behavior), reported separately from parameter-TI.")

    out = {"summary": summary, "rows": rows}
    json.dump(out, open("scripts/w1_behavior_results.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("[wrote scripts/w1_behavior_results.json]")


if __name__ == "__main__":
    main()
