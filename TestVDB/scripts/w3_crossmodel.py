#!/usr/bin/env python3
from __future__ import annotations
"""W3: cross-model consistency of the dev-reviewer (Round 8 Must-Fix).

Re-runs the dev-reviewer's source-grounded falsification with a second LLM
family (DeepSeek) on the same candidates GLM-5.2 adjudicated, BLIND to GLM's
rationale, and reports Cohen's kappa between the two families.

Pilot: n=6 (the candidates in dev_review.json that carry full source-grounding
artifacts: probe / observed / evidence_cmd / contract_refs). A larger
cross-model ablation is ongoing.

Inputs: TestVDB/results/milvus/v2.6.19/2026-07-04T16-43-43Z/debate_logs/dev_review.json
Outputs: TestVDB/scripts/w3_crossmodel_kappa_results.json
"""
import json
import os
import re
import sys
import time
from typing import Any

import requests

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

_key_paths = ["deepseek_apikey.txt", "../deepseek_apikey.txt", "../../deepseek_apikey.txt"]
API_KEY = next(open(p).read().strip() for p in _key_paths if os.path.exists(p))
URL = "https://api.deepseek.com/chat/completions"
SESSION = requests.Session()
SESSION.trust_env = False

DEV_REVIEW = (
    "results/milvus/v2.6.19/2026-07-04T16-43-43Z/"
    "debate_logs/dev_review.json"
)

PROMPT = """You are a dev-reviewer performing source-grounded falsification on a candidate API defect.
Decide whether the candidate is a REAL defect (CONFIRMED) or a FALSE_POSITIVE
(the observed behavior is correct, by-design, or caused by a test-script bug).

Base your judgment ONLY on the probe, the observed behavior, the evidence
command, and the contract below. Do NOT assume anything beyond this evidence.

Probe: {probe}
Observed behavior: {observed}
Evidence: {evidence}
Contract references: {contract}

Respond with STRICT JSON only, no prose:
{{"verdict": "CONFIRMED" | "FALSE_POSITIVE", "rationale": "one sentence"}}"""


def _normalize(v: str) -> str:
    v = (v or "").upper().strip()
    if v.startswith("FALSE"):
        return "FALSE_POSITIVE"
    if v.startswith("CONFIRM"):
        return "CONFIRMED"
    return v


def judge(probe: str, observed: str, evidence: str, contract: str) -> tuple[str, str]:
    payload = {
        "model": "deepseek-chat",
        "temperature": 0.0,
        "messages": [{
            "role": "user",
            "content": PROMPT.format(
                probe=probe, observed=observed,
                evidence=evidence, contract=contract),
        }],
        "max_tokens": 200,
    }
    hdr = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    last: Any = None
    for attempt in range(5):
        try:
            r = SESSION.post(URL, headers=hdr, timeout=60, json=payload)
            txt = r.json()["choices"][0]["message"]["content"].strip()
            break
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    else:
        return ("call-error", repr(last)[:120])
    m = re.search(r"\{[^{}]*\}", txt, re.S)
    if not m:
        return ("parse-error", txt[:120])
    try:
        j = json.loads(m.group(0))
    except Exception:  # noqa: BLE001
        return ("parse-error", txt[:120])
    return (_normalize(j.get("verdict", "?")), j.get("rationale", "")[:120])


def cohen_kappa(a: list[str], b: list[str]) -> tuple[float, dict[str, Any]]:
    labels = sorted(set(a) | set(b))
    n = len(a)
    matrix = {x: {y: 0 for y in labels} for x in labels}
    for x, y in zip(a, b):
        matrix[x][y] += 1
    po = sum(matrix[x][x] for x in labels) / n if n else 0.0
    pe = sum(
        (sum(matrix[x].values()) / n) * (sum(matrix[y][x] for y in labels) / n)
        for x in labels
    ) if n else 0.0
    kappa = (po - pe) / (1 - pe) if (1 - pe) > 0 else 1.0
    return kappa, {"po": po, "pe": pe, "matrix": matrix, "labels": labels}


def main() -> None:
    data = json.load(open(DEV_REVIEW, encoding="utf-8"))
    verdicts = data["verdicts"]
    rows: list[dict[str, Any]] = []
    for v in verdicts:
        steps = v.get("steps", {})
        cr = steps.get("clean_repro", {})
        cg = steps.get("contract_grounding", {})
        contract = "; ".join(cg.get("contract_refs", []) or [])
        glm_v = _normalize(v.get("verdict", ""))
        ds_v, rat = judge(
            cr.get("probe", ""), cr.get("observed", ""),
            cr.get("evidence_cmd", ""), contract,
        )
        rows.append({
            "defect_id": v.get("defect_id"),
            "endpoint": v.get("endpoint"),
            "glm_verdict": glm_v,
            "deepseek_verdict": ds_v,
            "agree": glm_v == ds_v,
            "deepseek_rationale": rat,
        })
        print(f"{v.get('defect_id'):35} GLM={glm_v:16} DS={ds_v:16} "
              f"agree={glm_v == ds_v}")
        time.sleep(0.5)

    valid = [r for r in rows if not r["deepseek_verdict"].endswith("error")]
    glm = [r["glm_verdict"] for r in valid]
    ds = [r["deepseek_verdict"] for r in valid]
    kappa, stats = cohen_kappa(glm, ds)
    interp = ("high agreement (kappa>=0.6)" if kappa >= 0.6 else
              "moderate (0.4<=kappa<0.6)" if kappa >= 0.4 else
              "low / family-specific (kappa<0.4)")
    summary = {
        "n": len(rows),
        "n_valid": len(valid),
        "agreement": sum(r["agree"] for r in valid) / len(valid) if valid else 0.0,
        "cohen_kappa": kappa,
        "interpretation": interp,
        "kappa_stats": stats,
    }
    print("\n=== W3 SUMMARY ===")
    print(f"n={summary['n']} valid={summary['n_valid']} "
          f"agreement={summary['agreement']:.2f} kappa={kappa:.3f} ({interp})")

    out = {"summary": summary, "rows": rows}
    json.dump(out, open("scripts/w3_crossmodel_kappa_results.json", "w",
                        encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[wrote scripts/w3_crossmodel_kappa_results.json]")


if __name__ == "__main__":
    main()
