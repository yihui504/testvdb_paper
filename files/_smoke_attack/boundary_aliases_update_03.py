#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
TestVDB Boundary Attack Script
Target: qdrant v1.18.0
Attack: type x constraints::qdrant_state_aliases_update_001 (chunk chunk_aliases+update, unit 1/2;
        this script = S2-type-boundary matrix on the required actions container: {omitted, null,
        string, object}; round coverage = S1 x unit1 (01 pos, 02 neg empty-array) + S2 x unit1
        (03 type matrix) + state-principle x behavioral_contracts::qdrant_bc_alias_switch_atomic_001
        (04 atomic switch) + S7 x unit1 (05 malformed alias_name); S3/S4/S6 have no applicable target
        in this chunk)
Oracle: each of the four legs - actions omitted, actions=null, actions="not-an-array",
        actions={} - must be rejected with a 4xx whose error text names the violated parameter
        ('actions'); any 2xx on any leg is Type1_IllegalSuccess (required-field/type validation
        unenforced), a 5xx is Type3_RuntimeFailure, a 404/405 route miss is SCRIPT_ERROR (path
        mismatch, not a defect), and any transport failure is re-verified against /healthz before any
        verdict
Constraint: multiple alias actions applied atomically; assertion: actions[] applied atomically: no
        concurrent request sees intermediate state
Endpoint: POST /collections/aliases (contract path aliases+update, category=admin; parameters:
        actions, type array<AliasOperations>, required=true; request_required_paths: actions,
        actions[].create_alias{alias_name, collection_name} | actions[].delete_alias{alias_name} |
        actions[].rename_alias{old_alias_name, new_alias_name})
Assertion: constraints::qdrant_state_aliases_update_001
source_url: https://api.qdrant.tech/v-1-18-x/api-reference/collections/update-aliases.md
doc_version: v1.18.x
Rationale: S2 type-boundary matrix per the strategy table (null / missing field / type confusion) aimed
           at the required container that carries the atomicity promise: whatever the container type
           violation, the server must refuse the request rather than improvise an empty/default batch
           (an improvised empty batch would silently no-op the very operation the constraint says is
           applied atomically). Level=system + empty bound_strategies -> D2 principle-based
           construction; the positive face of the same promise is covered by boundary_aliases_update_01
           (G4 pairing across the round, legs share the setup). S5 folded: a correct 4xx must name the
           violated parameter, else Type2_PoorDiagnostics.
"""

import requests
import json
import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TESTVDB_DB_URL = os.environ.get("TESTVDB_DB_URL")  # contract-driven: NO default port


def _resolve_target():
    """X1 three-layer bootstrap: env TESTVDB_TARGET -> upward-walk for structured_contract.json ->
    contract.target. Only when all three layers fail is the run a SCRIPT_ERROR."""
    t = os.environ.get("TESTVDB_TARGET")
    if t:
        return t, "env:TESTVDB_TARGET"
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        cand = os.path.join(d, "structured_contract.json")
        if os.path.isfile(cand):
            try:
                with open(cand, encoding="utf-8") as fh:
                    return (json.load(fh).get("target") or ""), "contract:" + cand
            except Exception:
                pass
        p = os.path.dirname(d)
        if p == d:
            break
        d = p
    return "", "unresolved"


TARGET, TARGET_SRC = _resolve_target()
if not TESTVDB_DB_URL:
    print("VERDICT: SCRIPT_ERROR - TESTVDB_DB_URL not set (see agents/_target_api_reference.md)")
    sys.exit(2)
if TARGET != "qdrant":
    print(f"VERDICT: SCRIPT_ERROR - target unresolved/mismatched (got {TARGET!r} via {TARGET_SRC}; "
          f"this script was generated for the qdrant v1.18.0 contract)")
    sys.exit(2)

# Fallback declaration contract: this round's dispatch mandates the safe_request three-tuple pattern
print("FALLBACK_TRIGGERED: safe_request used instead of the rt.request runtime (dispatch-mandated "
      "three-tuple pattern for this round; alias path_keys are absent from the abridged PATHS list in "
      "agents/_target_api_reference.md)")
print("[FALLBACK_JUSTIFIED: REST translations cross-checked against scripts/runtime/qdrant.py PATHS "
      "(update_aliases -> /collections/aliases, list_aliases -> /aliases, healthz -> /healthz; "
      "live-verified against qdrant v1.18.x per the runtime source comments)]")


def safe_request(method, path, json_body=None, data=None, headers=None, timeout=30):
    """Resilient HTTP wrapper. Returns (status_code, body_or_None, raw_text).
    Transport failure -> (-1, None, str(e)); non-JSON body -> (status, None, text)."""
    try:
        r = requests.request(method, TESTVDB_DB_URL + path, json=json_body, data=data,
                             headers=headers or {"Content-Type": "application/json"}, timeout=timeout)
        try:
            body = r.json() if r.text else {}
        except (json.JSONDecodeError, ValueError):
            print(f"JSON_DECODE_ERROR: {r.text[:200]}")
            return r.status_code, None, r.text
        return r.status_code, body, r.text
    except requests.exceptions.RequestException as e:
        print(f"REQUEST_ERROR: {e}")
        return -1, None, str(e)


def db_alive():
    status, _b, _raw = safe_request("GET", "/healthz", timeout=5)
    return 200 <= status < 300


def classify_transport(tag):
    """G8/D3b-3: a transport failure must be re-checked for liveness via a lightweight health endpoint
    before any verdict; a business endpoint's response must never prove liveness."""
    if not db_alive():
        print(f"[{tag}] transport failed AND /healthz dead -> server-side death")
        print(f"VERDICT: DEFECT_FOUND (Type3_RuntimeFailure) - {tag} killed the instance")
        sys.exit(1)
    print(f"VERDICT: SCRIPT_ERROR - {tag}: transport failure but service alive")
    sys.exit(2)


def err_text(body):
    """Extract the human error text from the qdrant envelope without assuming a fixed structure."""
    if isinstance(body, dict):
        st = body.get("status")
        if isinstance(st, dict) and isinstance(st.get("error"), str):
            return st["error"]
        if isinstance(st, str):
            return st
    return ""


# Contract-derived endpoint constant (chunk endpoint aliases+update; REST translation per
# scripts/runtime/qdrant.py PATHS: update_aliases -> /collections/aliases)
ALIASES_UPDATE = "/collections/aliases"

C1 = "tvdb_bnd_alu03_c1"
DIM = 4  # minimal legal collection scaffold; no vector legs exist in this chunk

# S2 matrix on the required actions container (per-leg expectations declared before execution, D3a)
LEGS = [
    ("missing_actions", {}),                        # required field absent entirely
    ("null_actions", {"actions": None}),            # null instead of array
    ("string_actions", {"actions": "not-an-array"}),  # type confusion: array -> string
    ("object_actions", {"actions": {}}),            # type confusion: array -> object
]


def make_coll(name):
    status, _b, raw = safe_request("PUT", f"/collections/{name}",
                                   json_body={"vectors": {"size": DIM, "distance": "Cosine"}})
    return status, raw


def drop_coll(name):
    try:
        status, _b, raw = safe_request("DELETE", f"/collections/{name}")
        if status not in (200, 404):
            print(f"Cleanup warning: DELETE {name} returned {status}: {raw[:200]}")
    except Exception as e:
        print(f"Cleanup warning: {e}")


def cleanup():
    """Mandatory script-cleanup spec: best-effort, existence-tolerant, never a nonzero exit."""
    drop_coll(C1)


def main():
    cleanup()  # pre-clean leftovers (best-effort)
    try:
        # --- setup (G8: a setup failure must never produce a defect conclusion) ---
        status, _b, raw = make_coll(C1)
        if status == -1:
            classify_transport("setup create_collection")
        if not (200 <= status < 300):
            print(f"VERDICT: SCRIPT_ERROR - setup create_collection {C1} -> {status}: {raw[:200]}")
            sys.exit(2)

        # --- Act + Assert: one matrix leg at a time, expectation declared per leg ---
        defects = []
        for tag, payload in LEGS:
            status, body, raw = safe_request("POST", ALIASES_UPDATE, json_body=payload)
            print(f"[{tag}] Status: {status}")
            print(f"[{tag}] Body: {raw[:300]}")
            if status == -1:
                classify_transport(f"leg {tag}")
            if status in (404, 405):
                print(f"VERDICT: SCRIPT_ERROR - update_aliases route missing ({status}); path mismatch")
                sys.exit(2)
            if 200 <= status < 300:
                got = body.get("result") if isinstance(body, dict) else "?"
                defects.append(f"{tag}: Type1_IllegalSuccess (2xx on type-invalid container, "
                               f"result={got})")
                continue
            if 500 <= status:
                defects.append(f"{tag}: Type3_RuntimeFailure (5xx {status} on type-invalid container)")
                continue
            if not (400 <= status < 500):
                print(f"VERDICT: SCRIPT_ERROR - leg {tag}: unexpected status {status}")
                sys.exit(2)
            # 4xx: correct rejection; S5 folded message-quality check
            msg = err_text(body) or raw
            if "action" not in msg.lower():
                defects.append(f"{tag}: Type2_PoorDiagnostics (4xx does not name 'actions': "
                               f"{msg[:120]})")

        if defects:
            print("VERDICT: DEFECT_FOUND (" + "; ".join(defects) + ")")
            sys.exit(1)
        print(f"VERDICT: NO_DEFECT (all {len(LEGS)} type-boundary legs rejected 4xx naming 'actions')")
        sys.exit(0)
    finally:
        cleanup()


if __name__ == "__main__":
    main()
