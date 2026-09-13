#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
TestVDB Boundary Attack Script
Target: qdrant v1.18.0
Attack: state_atomicity x behavioral_contracts::qdrant_bc_alias_switch_atomic_001 (chunk
        chunk_aliases+update, unit 2/2; principle-based construction per D2 - the contract is
        level=system with bound_strategies=[], so both directions are built from G1-G10; round coverage
        = S1 x unit1 (01 pos, 02 neg empty-array) + S2 x unit1 (03 type matrix) + state-principle x
        behavioral_contracts::qdrant_bc_alias_switch_atomic_001 (04 atomic switch) + S7 x unit1
        (05 malformed alias_name); S3/S4/S6 have no applicable target in this chunk)
Oracle: across 5 rename-style switch rounds performed as ONE aliases+update batch each
        ([delete_alias B, create_alias B->target], target alternating c2/c1), every concurrent GET
        /aliases read must always show exactly one entry B->{c1|c2} (never zero = 'neither' visible,
        never two = 'both' visible, never a third mapping); each switch round must answer 2xx with
        body result==true (contract response_shape result:boolean), the final state must be
        B->c2 (rounds 1/3/5 target c2), a 4xx on any spec-legal switch round is
        Type4_StateLogicViolation, a 5xx is Type3_RuntimeFailure, observer transport failures are
        excluded unless /healthz is also dead (G8), and any main-thread transport failure is
        re-verified against /healthz before any verdict
Constraint: alias switch via multiple actions is atomic; expected_behavior: no concurrent request
        observes intermediate state (both/neither visible); scenario: actions create_alias B->c2 +
        delete_alias B (rename-style switch)
Endpoint: POST /collections/aliases (contract path aliases+update, category=admin; observation read:
        GET /aliases, contract path aliases+list, response_shape result.aliases[].alias_name/
        collection_name)
Assertion: behavioral_contracts::qdrant_bc_alias_switch_atomic_001
source_url: https://api.qdrant.tech/v-1-18-x/api-reference/collections/update-aliases.md
doc_version: v1.18.x
Rationale: G6 mutation justification - the contract scenario 'create_alias B->c2, delete_alias B' is a
           rename-style switch of one globally-unique alias name; realized as [delete_alias B,
           create_alias B->target] inside ONE batch because actions apply in array order and
           create-before-delete is self-colliding (B still exists), whereas delete-then-create in a
           single batch is exactly the atomic switch whose safety the contract promises - without
           atomicity a reader window exists where B does not exist. The observer uses GET /aliases (a
           lightweight alias-resolution read, no vectors needed) so every intermediate state the
           contract forbids ('both/neither visible') is directly observable; 5 alternating rounds
           widen the race window without changing the mechanism. Setup uses the same single-action
           batch form so the probe never depends on an out-of-chunk endpoint.
"""

import requests
import json
import sys
import os
import time
import threading

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


def ok_result(status, body):
    """Success per the contract response_shape for aliases+update: 2xx AND result == True."""
    return 200 <= status < 300 and isinstance(body, dict) and body.get("result") is True


# Contract-derived endpoint constants (chunk endpoint aliases+update; observation aliases+list;
# REST translation per scripts/runtime/qdrant.py PATHS)
ALIASES_UPDATE = "/collections/aliases"
ALIASES_LIST = "/aliases"

C1 = "tvdb_bnd_alu04_c1"
C2 = "tvdb_bnd_alu04_c2"
ALIAS = "tvdb_bnd_alu04_alias"
ROUNDS = 5
DIM = 4  # minimal legal collection scaffold; no vector legs exist in this chunk

_stop = threading.Event()
_obs_lock = threading.Lock()
_observations = []  # (t_rel, kind, detail); kind in transport/intermediate_state/server_error/client_error/inconclusive_parse


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
    drop_coll(C2)


def update_aliases(actions):
    return safe_request("POST", ALIASES_UPDATE, json_body={"actions": actions})


def list_aliases():
    return safe_request("GET", ALIASES_LIST)


def alias_hits(body):
    """Return (hits, mode) where hits = [(alias_name, collection_name)] for the probe alias,
    parsed per this contract's aliases+list response_shape (result.aliases[].alias_name/collection_name)."""
    if isinstance(body, dict):
        result = body.get("result")
        if isinstance(result, dict) and isinstance(result.get("aliases"), list):
            hits = [(e.get("alias_name"), e.get("collection_name"))
                    for e in result["aliases"] if isinstance(e, dict) and e.get("alias_name") == ALIAS]
            return hits, "structured"
    return [], "raw_only"


def observe():
    """Concurrent reader: the contract's expected_behavior is that no concurrent request observes an
    intermediate state (both/neither visible). Every /aliases read must show exactly one
    ALIAS -> {C1|C2} entry throughout the switch window."""
    t0 = time.time()
    while not _stop.is_set():
        status, body, _raw = list_aliases()
        dt = time.time() - t0
        if status == -1:
            with _obs_lock:
                _observations.append((dt, "transport", ""))
        elif 200 <= status < 300:
            hits, mode = alias_hits(body)
            if mode != "structured":
                with _obs_lock:
                    _observations.append((dt, "inconclusive_parse", ""))
            elif len(hits) != 1 or hits[0][1] not in (C1, C2):
                with _obs_lock:
                    _observations.append((dt, "intermediate_state", f"hits={hits}"))
        elif 500 <= status:
            with _obs_lock:
                _observations.append((dt, "server_error", f"{status}"))
        elif 400 <= status < 500:
            with _obs_lock:
                _observations.append((dt, "client_error", f"{status}"))
        time.sleep(0.005)


def main():
    cleanup()  # pre-clean leftovers (best-effort)
    try:
        # --- setup: c1, c2, and alias B->c1 established via single-action batches (G8: setup failures
        #     must never produce a defect conclusion) ---
        for name in (C1, C2):
            status, _b, raw = make_coll(name)
            if status == -1:
                classify_transport(f"setup create_collection {name}")
            if not (200 <= status < 300):
                print(f"VERDICT: SCRIPT_ERROR - setup create_collection {name} -> {status}: {raw[:200]}")
                sys.exit(2)
        status, body, raw = update_aliases(
            [{"create_alias": {"collection_name": C1, "alias_name": ALIAS}}])
        if status == -1:
            classify_transport("setup create_alias")
        if not ok_result(status, body):
            print(f"VERDICT: SCRIPT_ERROR - setup create_alias failed: {status}: {raw[:200]}")
            sys.exit(2)

        # --- Act: observer up, then 5 atomic rename-style switch rounds ---
        obs = threading.Thread(target=observe, daemon=True)
        obs.start()
        time.sleep(0.05)  # let the observer reach steady state before the first switch

        switch_fail = None
        expected_final = None
        for i in range(1, ROUNDS + 1):
            target = C2 if i % 2 == 1 else C1
            expected_final = target
            status, body, raw = update_aliases([
                {"delete_alias": {"alias_name": ALIAS}},
                {"create_alias": {"collection_name": target, "alias_name": ALIAS}},
            ])
            print(f"[switch round {i} -> {target}] Status: {status}")
            print(f"[switch round {i} -> {target}] Body: {raw[:300]}")
            if status == -1:
                _stop.set()
                obs.join()
                classify_transport(f"switch round {i}")
            if not ok_result(status, body):
                switch_fail = (f"round {i} -> {target}: status {status}: "
                               f"{err_text(body) or raw[:200]}")
                break
            time.sleep(0.05)

        _stop.set()
        obs.join()

        if switch_fail:
            print(f"VERDICT: DEFECT_FOUND (Type4_StateLogicViolation) - spec-legal atomic switch "
                  f"rejected/unapplied: {switch_fail}")
            sys.exit(1)

        # --- final reconciliation: exactly one ALIAS -> expected_final after the committed switches ---
        status, body, raw = list_aliases()
        if status == -1:
            classify_transport("final list_aliases")
        if not (200 <= status < 300):
            print(f"VERDICT: SCRIPT_ERROR - final list_aliases read failed: {status}")
            sys.exit(2)
        hits, mode = alias_hits(body)
        final_ok = (mode == "structured" and len(hits) == 1 and hits[0][1] == expected_final)

        with _obs_lock:
            bad = [o for o in _observations if o[1] in ("intermediate_state", "server_error", "client_error")]
            transports = [o for o in _observations if o[1] == "transport"]
            inconclusive = [o for o in _observations if o[1] == "inconclusive_parse"]
        for o in bad[:10]:
            print(f"OBSERVATION {o[1]} @+{o[0]:.3f}s: {o[2]}")
        if inconclusive:
            print(f"NOTE: {len(inconclusive)} observer reads were non-JSON/exotic (excluded from "
                  f"intermediate-state evidence, reported for the judge)")

        if not final_ok:
            print(f"VERDICT: DEFECT_FOUND (Type4_StateLogicViolation) - post-switch state unreconciled: "
                  f"hits={hits} expected={ALIAS}->{expected_final} (parse mode {mode})")
            sys.exit(1)
        if bad:
            kinds = sorted({o[1] for o in bad})
            print(f"VERDICT: DEFECT_FOUND (Type4_StateLogicViolation) - concurrent reader observed "
                  f"intermediate state ({kinds} x {len(bad)} reads) during the atomic alias switch")
            sys.exit(1)
        if transports:
            if not db_alive():
                print("VERDICT: DEFECT_FOUND (Type3_RuntimeFailure) - observer transport failures and "
                      "/healthz dead -> instance died under the concurrent switch load")
                sys.exit(1)
            print(f"NOTE: {len(transports)} observer transport failures but /healthz alive "
                  f"(excluded from evidence per G8 three-outcome isolation)")

        print(f"VERDICT: NO_DEFECT ({ROUNDS} atomic switch rounds; concurrent observer clean; "
              f"final state {ALIAS}->{expected_final})")
        sys.exit(0)
    finally:
        cleanup()


if __name__ == "__main__":
    main()
