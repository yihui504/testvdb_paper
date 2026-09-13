#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
TestVDB Boundary Attack Script
Target: qdrant v1.18.0
Attack: malformed_input x constraints::qdrant_state_aliases_update_001 (chunk chunk_aliases+update,
        unit 1/2; S7 character-fuzzing on the user-input string field alias_name inside a multi-action
        batch, which additionally exercises the atomicity face of behavioral_contracts::
        qdrant_bc_alias_switch_atomic_001 - a malformed action must poison the WHOLE batch, not be
        skipped; round coverage = S1 x unit1 (01 pos, 02 neg empty-array) + S2 x unit1 (03 type
        matrix) + state-principle x behavioral_contracts::qdrant_bc_alias_switch_atomic_001 (04 atomic
        switch) + S7 x unit1 (05 malformed alias_name); S3/S4/S6 have no applicable target in this
        chunk)
Oracle: a batch mixing a malformed alias_name with a trailing legal create_alias must be rejected 4xx
        with NOTHING applied (neither a malformed-named alias nor the trailing legal alias may persist);
        5xx / parser-or-encoding signal ('panic'/'internal'/'serde'/'utf'/'decode' in the body) =
        Type3_RuntimeFailure; 2xx with a malformed-named alias persisted = Type1_IllegalSuccess (silent
        accept, judge to weigh doc semantics); 2xx with only the trailing legal alias persisted = Type4
        (malformed action silently dropped); 2xx with nothing persisted = Type4 (success reported,
        nothing applied); 4xx with any alias persisted = Type4 (rejection yet partial application - the
        atomicity promise broken); a correct 4xx must name the violated parameter family, else
        Type2_PoorDiagnostics; a 404/405 route miss is SCRIPT_ERROR; transport failures are
        re-verified against /healthz before any verdict. A trailing single-action legal create_alias
        positive control must succeed, else the run is SCRIPT_ERROR (harness invalidation, not a defect
        conclusion)
Constraint: multiple alias actions applied atomically; assertion: actions[] applied atomically: no
        concurrent request sees intermediate state
Endpoint: POST /collections/aliases (contract path aliases+update, category=admin; attacked field:
        actions[].create_alias.alias_name, a user-input string; observation read: GET /aliases)
Assertion: constraints::qdrant_state_aliases_update_001
source_url: https://api.qdrant.tech/v-1-18-x/api-reference/collections/update-aliases.md
doc_version: v1.18.x
Rationale: S7 fills the malformed-input/character-boundary blindspot that strategies 1-2 do not cover
           (they test value/type boundaries, not input-stream malformation). Legs: (A) the JSON escape
           sequence backslash-u0000 (legal JSON, decodes to U+0000) with a trailing legal create_alias;
           (A2) a BARE NUL byte injected into the raw bytes (illegal JSON control character),
           single-action batch; (B) the backslash-uD800 lone-surrogate escape (legal JSON syntax, illegal
           Unicode scalar on decode). All legs are sent via data=<bytes> because json= would be rejected
           client-side by serialization first and the DB's own behavior would never be measured. G6
           mutation justification: the malformed action is placed FIRST in the batch with a trailing
           legal create_alias so all outcomes are separable - whole-batch rejection (atomic, no defect),
           silent drop + rest applied (partial application), silent accept (malformed name persisted).
           Windows-stdout safety: malformed names exist only inside raw byte bodies and are never printed
           as Python str.
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


def ok_result(status, body):
    """Success per the contract response_shape for aliases+update: 2xx AND result == True."""
    return 200 <= status < 300 and isinstance(body, dict) and body.get("result") is True


# Contract-derived endpoint constants (chunk endpoint aliases+update; observation aliases+list;
# REST translation per scripts/runtime/qdrant.py PATHS)
ALIASES_UPDATE = "/collections/aliases"
ALIASES_LIST = "/aliases"

C1 = "tvdb_bnd_alu05_c1"
C2 = "tvdb_bnd_alu05_c2"
GOOD_A = "tvdb_bnd_alu05_good_a"
GOOD_B = "tvdb_bnd_alu05_good_b"
GOOD_C = "tvdb_bnd_alu05_good_c"
MAL_PREFIX = "tvdb_bnd_alu05_bad"  # malformed names share this prefix so persistence is detectable
DIM = 4  # minimal legal collection scaffold; no vector legs exist in this chunk

CRASH_SIGNALS = ("panic", "internal", "serde", "utf", "decode", "out of memory", "capacity overflow")


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


def delete_alias(name):
    try:
        safe_request("POST", ALIASES_UPDATE,
                     json_body={"actions": [{"delete_alias": {"alias_name": name}}]})
    except Exception as e:
        print(f"Cleanup warning: {e}")


def cleanup():
    """Mandatory script-cleanup spec: best-effort, existence-tolerant, never a nonzero exit."""
    for name in (GOOD_A, GOOD_B, GOOD_C):
        delete_alias(name)
    drop_coll(C1)
    drop_coll(C2)  # dropping the backing collections cascades any surviving alias


def update_aliases(actions):
    return safe_request("POST", ALIASES_UPDATE, json_body={"actions": actions})


def list_aliases():
    return safe_request("GET", ALIASES_LIST)


def persisted_names():
    """Return (set_of_alias_names, mode) via GET /aliases, parsed per this contract's aliases+list
    response_shape (result.aliases[].alias_name / .collection_name)."""
    status, body, _raw = list_aliases()
    if status == -1:
        classify_transport("list_aliases state read")
    if not (200 <= status < 300):
        return set(), "read_failed"
    if isinstance(body, dict):
        result = body.get("result")
        if isinstance(result, dict) and isinstance(result.get("aliases"), list):
            names = {e.get("alias_name") for e in result["aliases"] if isinstance(e, dict)}
            return names, "structured"
    return set(), "raw_only"


def run_leg(tag, raw_body, trailing_good):
    """Execute one malformed-input leg and return a defect string or None (clean rejection).
    Adjudication is declared in the Oracle line before execution (D3a). trailing_good = the legal
    alias name expected from the batch's trailing action, or None for a single-action batch."""
    status, body, raw = safe_request("POST", ALIASES_UPDATE, data=raw_body)
    print(f"[{tag}] Status: {status}")
    print(f"[{tag}] Body: {raw[:400]}")
    if status == -1:
        classify_transport(f"leg {tag}")
    if status in (404, 405):
        print(f"VERDICT: SCRIPT_ERROR - update_aliases route missing ({status}); path mismatch")
        sys.exit(2)
    if 500 <= status:
        return f"{tag}: Type3_RuntimeFailure (server error {status} on malformed input)"
    low = raw.lower()
    if any(k in low for k in CRASH_SIGNALS):
        return f"{tag}: Type3_RuntimeFailure (parser/encoding crash signal in body: {raw[:160]})"

    names, mode = persisted_names()
    mal_survivors = sorted(n for n in names if isinstance(n, str) and n.startswith(MAL_PREFIX))
    good_in = sorted(names & {trailing_good}) if trailing_good else []
    if 200 <= status < 300:
        # 2xx is not automatically a defect: inspect what actually persisted (silent-accept face)
        if mal_survivors:
            return (f"{tag}: Type1_IllegalSuccess (malformed alias_name persisted: {mal_survivors}; "
                    f"judge to weigh doc semantics)")
        if good_in:
            return (f"{tag}: Type4_StateLogicViolation (malformed action silently dropped but trailing "
                    f"legal action applied: {good_in})")
        return f"{tag}: Type4_StateLogicViolation (2xx reported but nothing from the batch persisted)"
    if 400 <= status < 500:
        # correct rejection face - the atomicity promise adds: NOTHING may have been applied
        if mal_survivors:
            return (f"{tag}: Type4_StateLogicViolation (4xx rejection yet malformed alias persisted: "
                    f"{mal_survivors})")
        if good_in:
            return (f"{tag}: Type4_StateLogicViolation (4xx rejection yet trailing legal action "
                    f"partially applied: {good_in} - atomicity broken)")
        msg = err_text(body) or raw
        if not any(k in msg.lower() for k in ("alias", "action", "name", "invalid")):
            return (f"{tag}: Type2_PoorDiagnostics (4xx error names neither alias nor action nor "
                    f"validity: {msg[:120]})")
        return None
    return f"{tag}: unexpected status {status}"


def main():
    cleanup()  # pre-clean leftovers (best-effort)
    try:
        # --- setup (G8: a setup failure must never produce a defect conclusion) ---
        for name in (C1, C2):
            status, _b, raw = make_coll(name)
            if status == -1:
                classify_transport(f"setup create_collection {name}")
            if not (200 <= status < 300):
                print(f"VERDICT: SCRIPT_ERROR - setup create_collection {name} -> {status}: {raw[:200]}")
                sys.exit(2)

        defects = []

        # --- Leg A: JSON escape backslash-u0000 (legal JSON, decodes to U+0000) as the FIRST action,
        #     with a trailing legal create_alias so partial application is detectable. ---
        body_a = (
            '{"actions": ['
            '{"create_alias": {"collection_name": "' + C2 + '", "alias_name": "' + MAL_PREFIX + '\\u0000name_a"}},'
            '{"create_alias": {"collection_name": "' + C1 + '", "alias_name": "' + GOOD_A + '"}}'
            ']}'
        ).encode("utf-8")
        defect = run_leg("A_nul_escaped", body_a, GOOD_A)
        if defect:
            defects.append(defect)

        # --- Leg A2: BARE NUL byte inside the JSON string (illegal control character), built
        #     byte-by-byte so no client layer escapes it; single-action batch. ---
        prefix_b = ('{"actions": [{"create_alias": {"collection_name": "' + C2 + '", "alias_name": "'
                    + MAL_PREFIX).encode("utf-8")
        suffix_b = 'name_a2"}}]}'.encode("utf-8")
        body_a2 = prefix_b + b"\x00" + suffix_b
        defect = run_leg("A2_nul_bare", body_a2, None)
        if defect:
            defects.append(defect)

        # --- Leg B: lone surrogate escape backslash-uD800 (legal JSON syntax, illegal Unicode scalar
        #     on decode), same batch shape as leg A. ---
        body_b = (
            '{"actions": ['
            '{"create_alias": {"collection_name": "' + C2 + '", "alias_name": "' + MAL_PREFIX + '\\ud800name_b"}},'
            '{"create_alias": {"collection_name": "' + C1 + '", "alias_name": "' + GOOD_B + '"}}'
            ']}'
        ).encode("utf-8")
        defect = run_leg("B_lone_surrogate", body_b, GOOD_B)
        if defect:
            defects.append(defect)

        # --- Positive control (G4): a plain single-action legal batch must succeed, proving the
        #     harness face is healthy; failure here invalidates the run, it is not a defect. ---
        status, body, raw = update_aliases(
            [{"create_alias": {"collection_name": C1, "alias_name": GOOD_C}}])
        print(f"[control] Status: {status}")
        print(f"[control] Body: {raw[:300]}")
        if status == -1:
            classify_transport("control create_alias")
        if not ok_result(status, body):
            print(f"VERDICT: SCRIPT_ERROR - positive control failed ({status}): "
                  f"{err_text(body) or raw[:200]} - malformed-input legs are not interpretable")
            sys.exit(2)
        names, mode = persisted_names()
        if GOOD_C not in names:
            print(f"VERDICT: SCRIPT_ERROR - control reported success but alias invisible via /aliases "
                  f"(mode {mode})")
            sys.exit(2)

        if defects:
            print("VERDICT: DEFECT_FOUND (" + "; ".join(defects) + ")")
            sys.exit(1)
        print("VERDICT: NO_DEFECT (NUL-escape / bare-NUL / lone-surrogate legs all rejected with "
              "nothing applied; positive control healthy)")
        sys.exit(0)
    finally:
        cleanup()


if __name__ == "__main__":
    main()
