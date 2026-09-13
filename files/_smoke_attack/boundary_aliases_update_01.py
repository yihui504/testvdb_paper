#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
TestVDB Boundary Attack Script
Target: qdrant v1.18.0
Attack: boundary x constraints::qdrant_state_aliases_update_001 (chunk chunk_aliases+update, unit 1/2;
        this script = S1-boundary POSITIVE leg: actions[] min-legal cardinality = exactly one create_alias;
        round coverage = S1 x unit1 (01 pos, 02 neg empty-array) + S2 x unit1 (03 type matrix) +
        state-principle x behavioral_contracts::qdrant_bc_alias_switch_atomic_001 (04 atomic switch) +
        S7 x unit1 (05 malformed alias_name); S3/S4/S6 have no applicable target in this chunk)
Oracle: POST /collections/aliases with a single legal create_alias action must answer 2xx with body
        result==true (contract response_shape result:boolean), and an independent GET /aliases must then
        show exactly one entry mapping the alias to the target collection; any transport failure must be
        re-verified against /healthz before any verdict
Constraint: multiple alias actions applied atomically; assertion: actions[] applied atomically: no
        concurrent request sees intermediate state
Endpoint: POST /collections/aliases (contract path aliases+update, category=admin; required paths:
        actions[], actions[].create_alias.alias_name, actions[].create_alias.collection_name)
Assertion: constraints::qdrant_state_aliases_update_001
source_url: https://api.qdrant.tech/v-1-18-x/api-reference/collections/update-aliases.md
doc_version: v1.18.x
Rationale: G4 positive/negative pairing - the atomicity constraint also has a promise side: the smallest
           legal batch (one create_alias action, the min-legal cardinality of the required actions[]
           array) must be accepted AND actually applied; with only negative legs the constraint itself
           could be false and the attack groundless. Application is verified through the independent
           GET /aliases read (keys taken from this contract's aliases+list response_shape:
           result.aliases[].alias_name / result.aliases[].collection_name), never from the mutating
           call's own body alone. Level=system + empty bound_strategies -> D2 principle-based
           construction (G1-G10).
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
    """Extract the human error text from the qdrant envelope without assuming a fixed structure
    (status may be the string 'ok' on success or an object {error: ...} on failure)."""
    if isinstance(body, dict):
        st = body.get("status")
        if isinstance(st, dict) and isinstance(st.get("error"), str):
            return st["error"]
        if isinstance(st, str):
            return st
    return ""


def ok_result(status, body):
    """Success per the contract response_shape for aliases+update: 2xx AND result == True
    (response_shape: result: boolean)."""
    return 200 <= status < 300 and isinstance(body, dict) and body.get("result") is True


# Contract-derived endpoint constants (chunk endpoint aliases+update; REST translation per
# scripts/runtime/qdrant.py PATHS: update_aliases -> /collections/aliases, list_aliases -> /aliases)
ALIASES_UPDATE = "/collections/aliases"
ALIASES_LIST = "/aliases"

C1 = "tvdb_bnd_alu01_c1"
ALIAS = "tvdb_bnd_alu01_alias"
DIM = 4  # minimal legal collection scaffold; no vector legs exist in this chunk


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
    try:
        safe_request("POST", ALIASES_UPDATE,
                     json_body={"actions": [{"delete_alias": {"alias_name": ALIAS}}]})
    except Exception as e:
        print(f"Cleanup warning: {e}")
    drop_coll(C1)


def update_aliases(actions):
    """POST /collections/aliases (contract aliases+update). Body per contract parameters:
    {actions: [create_alias{collection_name, alias_name} | delete_alias{alias_name} | ...]}"""
    return safe_request("POST", ALIASES_UPDATE, json_body={"actions": actions})


def list_aliases():
    return safe_request("GET", ALIASES_LIST)


def alias_entries(body):
    """Parse GET /aliases per this contract's aliases+list response_shape
    (result.aliases[].alias_name / .collection_name). Returns (entries, mode)."""
    if isinstance(body, dict):
        result = body.get("result")
        if isinstance(result, dict) and isinstance(result.get("aliases"), list):
            entries = []
            for e in result["aliases"]:
                if isinstance(e, dict) and "alias_name" in e:
                    entries.append((e.get("alias_name"), e.get("collection_name")))
            return entries, "structured"
    return [], "raw_only"


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

        # --- Act: min-legal cardinality actions[] (exactly one create_alias) ---
        status, body, raw = update_aliases(
            [{"create_alias": {"collection_name": C1, "alias_name": ALIAS}}])
        print(f"Status: {status}")
        print(f"Body: {raw}")
        if status == -1:
            classify_transport("update_aliases single create_alias")
        if status in (404, 405):
            print(f"VERDICT: SCRIPT_ERROR - update_aliases route missing ({status}); path mismatch")
            sys.exit(2)
        if not (200 <= status < 300):
            print(f"VERDICT: DEFECT_FOUND (Type4_StateLogicViolation) - legal min-cardinality batch "
                  f"rejected/unapplied: {status}: {err_text(body) or raw[:200]}")
            sys.exit(1)
        if not ok_result(status, body):
            print(f"VERDICT: DEFECT_FOUND (Type4_StateLogicViolation) - 2xx but contract response_shape "
                  f"result:boolean is not True: {raw[:200]}")
            sys.exit(1)

        # --- Assert application via the independent GET /aliases read ---
        lst_status, lst_body, lst_raw = list_aliases()
        if lst_status == -1:
            classify_transport("list_aliases verification")
        if not (200 <= lst_status < 300):
            print(f"VERDICT: SCRIPT_ERROR - list_aliases verification read failed: {lst_status}")
            sys.exit(2)
        entries, mode = alias_entries(lst_body)
        hits = [e for e in entries if e[0] == ALIAS]
        print(f"alias entries for {ALIAS}: {hits} (parse mode: {mode})")
        if len(hits) == 1 and hits[0][1] == C1:
            print("VERDICT: NO_DEFECT")
            sys.exit(0)
        if len(hits) == 0:
            print("VERDICT: DEFECT_FOUND (Type4_StateLogicViolation) - update_aliases reported "
                  "result=true but the alias is not visible via /aliases")
            sys.exit(1)
        print(f"VERDICT: DEFECT_FOUND (Type4_StateLogicViolation) - alias mapping unexpected: {hits}")
        sys.exit(1)
    finally:
        cleanup()


if __name__ == "__main__":
    main()
