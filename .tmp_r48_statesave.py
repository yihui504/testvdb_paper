# -*- coding: utf-8 -*-
"""R48 STATE_SAVE: mine_state + pipeline_state + coverage + snapshots."""
import json
import shutil
from datetime import datetime, timezone

SD = r"C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.5.0/results/qdrant/v1.18.0/2026-09-04T12-14-11Z"
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

NOTE = (
    "11/13 NO_DEFECT + 2 real DEFECT (boundary_up_spB_03 = defect-61 untagged-enum FAMILY INSTANCE "
    "x5 legs; semantic_up_batch_02 = NEW DEFECT CANDIDATE Type4: identical mixed batch leaves "
    "NONDETERMINISTIC partial application — script 2-run survivors [9 pts] vs [102,107], main-process "
    "6-run replay produced SIX different survivor sets under wait=true with a trailing dim-mismatch "
    "poison; client state unreconstructable from the 400). First pass: 5 DEFECT + 1 SE + 1 crash-no-"
    "verdict -> 4 artifacts + 1 SE fix + 1 family/new pair survived. Artifact repairs (5 waves, 7 "
    "mechanical fixes, all forensics-pinned): (a) ident_01 point+get path_params KeyError crash; "
    "(b) ident_01 get legs sent STRING ids from the live map (server correctly 400'd the strid form "
    "-> get_vecs now canonicalizes to int; R42/R43 pin script-side recurrence); (c) ordB_05 bare "
    "quote() NameError; (d) waitf_03 W3 off-by-one (BASE_N+2 should be +3: the wait=true W2 write "
    "already bumped the count — the correct count 5 was flagged as double-apply); (e) idsA_01 Ibrace "
    "braced-uuid: uuid crate parses braced form as an ALIAS of the same uuid (forensics: bare-form "
    "GET resolves the point, id normalized to bare lowercase) -> 2xx+resolvable = COMPLIANT alias "
    "NOTE, moved out of the illegal set; (f) bkill_04 Type3 OVERRIDDEN by forensics: the container "
    "NEVER died (healthz 200 throughout) — the observed bare disconnect at stage S2 (59.4MB) is a "
    "client-side streaming artifact; server-side replay with BOTH direct and streamed bodies returns "
    "HTTP 400 documented 'Payload error: JSON payload ... larger than allowed (limit: 33554432 "
    "bytes)' 6/6 = the resource_bound contract's legal 'documented client error' disposition (32MB "
    "payload cap PINNED); spB_03's five 400s are the REAL defect-61 family signature (serde untagged "
    "enum generic message without field naming) contrasted by the SAME script's 422s which DO name "
    "fields (validation-layer vs serde-layer split evidence). Positive evidence: id domain closure "
    "(0/1/2**63/2**64-1 exact round-trips; 2**64/-1/digit-string/non-uuid all 400 naming the value); "
    "float 1.0 rejected; uppercase uuid accepted gettable-as-submitted; dup-id-in-batch last-write-"
    "wins characterized; vector-shape closure on named collections (bare array 400 R45 pin, wrong "
    "name 400, multivector-on-dense 400, []/null/str-element all rejected); sparse literal closure "
    "(dup 422 'must be unique' + len-mismatch 422 'same length' BOTH naming fields with '?' "
    "placeholder NOTE); index value domain: float/negative/2**64 rejected (2**32-1 boundary pinned "
    "in spmaxA with 1000-entry construction 200 + SKIPPED note for the resource-infeasible 4.29e9 "
    "count); update_mode/ordering unknown values 400 enumerating ALL variants (defect-61 positive "
    "contrast); identity semantics exact (re-upsert replaces; insert_only refuses update; update_only "
    "refuses insert incl. 404-on-get of the refused id; no wedging after refused modes); "
    "update_filter gate semantics verified three-way (matching updated / non-matching KEPT incl. "
    "payload smuggle attempt / brand-new inserted regardless; no-match filter and absent-key filter "
    "both gate-hold + insert-bypass); wait=false acknowledged + bounded landing + immediate-"
    "visibility both legal; empty batch 400 'Empty update request'; batch escalation POSITIVE "
    "resource envelope: 20k/0.1s, 100k dim-8/0.41s, 1e6 dim-8 rejected by the 32MB payload cap, "
    "container never crashed. D-segment addenda: 32MB payload cap + documented 400 (new pin); "
    "mixed-batch partial-apply nondeterminism -> evidence-builder P0 for Step 9 (defect-63 "
    "candidate); defect-61 family roster += sparse-literal instance. Script-side lessons banked: "
    "live-map STRING keys must be canonicalized before reuse in verification bodies (strid family "
    "recurrence); off-by-one count chains across wait-mixed legs need a fresh count BEFORE each "
    "expectation (lesson 19 applies to expectations, not just baselines); braced-uuid = uuid-crate "
    "alias (never an illegal-domain fixture)."
)

ms = json.load(open(f"{SD}/mine_state.json", encoding="utf-8"))
ms["current_round"] = 49
ms["last_round"] = {
    "round": 48,
    "chunk": "chunk_points+upsert-1of2",
    "verdicts": {"DEFECT": 2, "NOT_DEFECT": 11, "NME": 0},
    "note": NOTE,
}
ms["paused"] = False
ms["updated_at"] = now
json.dump(ms, open(f"{SD}/mine_state.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

ps = json.load(open(f"{SD}/pipeline_state.json", encoding="utf-8"))
ps["current_round"] = 49
ps["phase"] = "ROUND_START"
ps["phase_step_index"] = 0
ps["phases_completed"] = ["ROUND_START"]
ps.setdefault("phase_data", {})["ATTACK_GEN"] = {
    "ROUND_START": {"round": 49, "prev_round": 48, "prev_chunk": "chunk_points+upsert-1of2",
                    "prev_zero_candidate": False},
}
ps["phase_data"]["REPORT"] = {
    "round": 48,
    "chunk": "chunk_points+upsert-1of2",
    "scripts": 13,
    "path_accounting": {"A": 2, "B": 11},
    "first_pass": "6N + 5 DEFECT-candidates + 1 SE + 1 crash-no-verdict",
    "artifact_cycles": ("5 rerun waves / 7 mechanical fixes: ident_01 path_params KeyError + "
                        "string-id get legs (canonical-int); ordB_05 quote import; waitf_03 W3 "
                        "off-by-one (+2->+3); idsA_01 Ibrace alias (uuid-crate braced form); "
                        "bkill_04 Type3 OVERRIDDEN — 32MB payload cap returns documented 400 "
                        "(forensics 6/6, container never died)"),
    "final": ("11/13 NO_DEFECT; spB_03 = defect-61 family instance (serde-layer unnamed 400s vs "
              "validation-layer named 422s); batch_02 = NEW defect candidate Type4 nondeterministic "
              "partial application (6-run replay, six different survivor sets)"),
}
ps["updated_at"] = now
json.dump(ps, open(f"{SD}/pipeline_state.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

cv = json.load(open(f"{SD}/coverage.json", encoding="utf-8"))
cv["round"] = 48
cv["covered_chunks"] = 49
cv["chunks_done"] = 43
cv["overall_coverage_pct"] = round(49 / 66 * 100, 1)
cv["updated_at"] = now
cv.setdefault("endpoints", {})["points+upsert"] = (
    "R48 (1of2, constraints chunk): 13 scripts (boundary 6 [pathA ids + sparse-count], state 3, "
    "semantic 4 [incl. kill-risk batch escalation]). 11 NO_DEFECT + 2 real: spB_03 = defect-61 "
    "untagged-enum family instance (sparse literal serde-layer 400s name nothing; same-script 422s "
    "name fields — layer-split evidence); batch_02 = NEW Type4 candidate — identical mixed batch "
    "(9 valid + trailing dim-mismatch poison) under wait=true leaves NONDETERMINISTIC survivor sets "
    "(six runs, six different sets), client state unreconstructable from the 400. Positive pins: "
    "u64/UUID id domain incl. u64max canary exact round-trip and braced-uuid = uuid-crate alias; "
    "update_mode/ordering unknown values 400 enumerate all variants; sparse literal dup/len 422 "
    "name fields ('?' placeholder NOTE); identity semantics (re-upsert replaces, insert_only "
    "refuses update, update_only refuses insert) exact; update_filter three-way gate verified; "
    "wait=false acknowledged + bounded landing; 32MB payload cap with documented 400 (bkill_04 "
    "Type3 overridden); 100k dim-8 upsert 0.41s; container never crashed. Evidence-builder P0 at "
    "Step 9: batch partial-apply nondeterminism (defect-63 candidate) needs mechanism attribution."
)

json.dump(cv, open(f"{SD}/coverage.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

for name in ("mine_state.json", "pipeline_state.json", "coverage.json"):
    shutil.copyfile(f"{SD}/{name}", f"{SD}/{name}.r48")

print("STATE_SAVE done: round 49 | coverage 49/66 =", cv["overall_coverage_pct"], "%")
