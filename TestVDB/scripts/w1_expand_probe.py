#!/usr/bin/env python3
from __future__ import annotations
"""W1: expand the task-intrinsic probe (Round 8 Must-Fix).

Adds Qdrant v1.18.2 over-strict clauses (live-probe-confirmed: 0 / special
value accepted) to the original Milvus-9 set, re-runs DeepSeek formalization
(judge TI: does the second family ALSO over-formalize?) and cross-model
judging, and reports the task-intrinsic rate with a Wilson 95% CI.

Confirmed over-strict on Qdrant v1.18.2 (this run): timeout=0, group_size=0,
score_threshold out-of-range. Rejected (NOT over-strict): limit, shard_number,
replication_factor, write_consistency_factor.

Inputs: scripts/e2_judgment_results.json (Milvus-9), live qdrant probe.
Outputs: scripts/w1_full_results.json
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

# (id, db, passage, glm_assertion, real_semantics) — qdrant live-probe-confirmed
QDRANT_CASES = [
    ("qdrant_timeout", "qdrant",
     "`timeout` (integer, required=false): Operation timeout.",
     "timeout >= 1",
     "0 means no timeout; Qdrant accepts timeout=0"),
    ("qdrant_group_size", "qdrant",
     "`group_size` (integer, required=true): Max points per group in grouped search.",
     "group_size >= 1 AND limit >= 1",
     "0 accepted; Qdrant accepts group_size=0"),
    ("qdrant_score_threshold", "qdrant",
     "`score_threshold` (float, optional): Relevance score filter for Cosine search.",
     "score_threshold in [0, 1]",
     "any float accepted, no [0,1] enforcement; Qdrant accepts 2.0 and -0.5"),
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
    "(it rejects a value the real semantics actually allows)?\n\n"
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
    milvus9 = json.load(open("scripts/e2_judgment_results.json", encoding="utf-8"))
    rows: list[dict] = list(milvus9)
    qrows: list[dict] = []
    for cid, db, passage, glm_a, real in QDRANT_CASES:
        ds_clause = formalize(passage)
        ti = judge_ti(ds_clause, real)
        cm = crossmodel_judge(passage, glm_a)
        qrows.append({
            "id": cid, "db": db, "task_intrinsic": ti,
            "ground_truth": "over-strict", "source_contradicts": True,
            "glm_assertion": glm_a, "deepseek_clause": ds_clause,
            "crossmodel_judgment": cm,
        })
        print(f"{cid:28} DS={ds_clause[:38]:38} TI={ti!s:5} crossmodel={cm}")
        time.sleep(0.5)

    all_rows = rows + qrows
    n = len(all_rows)
    ti_count = sum(1 for r in all_rows if r.get("task_intrinsic"))
    ti_rate = ti_count / n
    lo, hi = wilson_ci(ti_count, n)
    ti_rows = [r for r in all_rows if r.get("task_intrinsic")]
    ti_cm = sum(1 for r in ti_rows
                if r.get("crossmodel_flagged") or r.get("crossmodel_judgment"))

    summary = {
        "n": n, "milvus_n": len(rows), "qdrant_n": len(qrows),
        "ti_count": ti_count, "ti_rate": ti_rate,
        "ti_wilson_95": [lo, hi],
        "ti_crossmodel_catch": f"{ti_cm}/{len(ti_rows)}",
        "source_catch_all": f"{n}/{n}",
    }
    print(f"\n=== W1 SUMMARY (n={n}, milvus={len(rows)} + qdrant={len(qrows)}) ===")
    print(f"task-intrinsic: {ti_count}/{n} = {ti_rate:.2%} "
          f"(Wilson 95% CI [{lo:.2%}, {hi:.2%}])")
    print(f"cross-model judging catches TI subset: {summary['ti_crossmodel_catch']}")
    print(f"source-grounded falsification catches: {summary['source_catch_all']}")

    out = {"summary": summary, "rows": all_rows, "qdrant_new": qrows}
    json.dump(out, open("scripts/w1_full_results.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("[wrote scripts/w1_full_results.json]")


if __name__ == "__main__":
    main()
