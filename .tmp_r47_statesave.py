# -*- coding: utf-8 -*-
"""R47 STATE_SAVE: mine_state + pipeline_state + coverage + snapshot."""
import json
import shutil
from datetime import datetime, timezone

SD = r"C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.5.0/results/qdrant/v1.18.0/2026-09-04T12-14-11Z"
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

NOTE = (
    "12/12 NO_DEFECT (boundary_mp_ 5 [boundsA pathA + 4 pathB] / semantic_mp_ 4 / state_mp_ 3). "
    "Zero-candidate round #8. ORPHAN RECOVERY: state lane inherited a draft-only script from the "
    "user-stopped agent (state_mp_wspec_01.py: helper library complete, NO main/entrypoint -> ran "
    "exit-0 with a 0-byte log) -> repair agent appended main per the draft's own docstring (14 "
    "legs W0/L1/L2/L3); xface_02.meta.json was missing (repair agent died at ECONNRESET one file "
    "before finishing) -> main process wrote the conformant meta from the script docstring; "
    "usingB_05 lacked the G3 'path: B' marker -> one-sed append. Artifact repair cycle, 3 rerun "
    "waves, 6 mechanical fixes, ALL forensics-verified as script-side: (a) det_03 asserted "
    "exhaustive-only per-pair orientation multiplicity==2 on DEFAULT random legs (a pair may "
    "appear once when the reverse row is not sampled) -> gated to row_of None; (b) using_04 sig() "
    "unpack bug 'a, b = <single value if/else single value>' -> 'a =' (ValueError exit 2); "
    "(c) boundsA_01 N1 null==absent strict multiset assertion flaked on a TIE-RICH linear fixture "
    "[i,0,0,0] (|5-3|==|5-7|==2: tied-neighbour emission is by-design random; replay showed "
    "absent/null/explicit pairwise-differing multisets ALL explained by tie swaps, heads equal) -> "
    "(id,score)-key tie-tolerant comparison; (d) samp_03 norm() float round-trip corrupted the "
    "legal u64-max canary itself: float(2**64-1) rounds UP to 2**64 -> 'sampling leak' phantom "
    "ids + 'canary absent'; server-side replay (fresh + full 23-request state sequence) showed "
    "corruption_seen=0 with exact ids and exact scores -> exact-integers-bypass-float fix; "
    "(e) wspec_01 delete used DELETE /collections/{c}/points = nonexistent route (404) -> POST "
    "/points/delete with wait=true in body (xface_02 form); (f) wspec_01 then required result "
    "status=='completed' but wait=true DELETE returns 'acknowledged' (legal UpdateStatus enum "
    "value alongside completed/wait_timeout; forensics: GET of deleted id -> 404, delete "
    "EFFECTIVE; upsert wait=true returns completed — stable asymmetry) -> accept both enum "
    "values. Positive evidence: exhaustive closure X1 56 cells exact; min closures sample=2 / "
    "limit=1 accepted; sample=1/sample=0/limit=0 -> 422 naming search_request.sample/limit "
    "(validator prefix structural, R46 pin); sample=100 above-count clamp COMPLIANT both faces; "
    "u64 canary round-trips EXACT on pairs face (storage GET exact; matrix cells exact both "
    "orientations; f64-corruption hypothesis DISPROVEN server-side); determinism: exhaustive "
    "two-run multiset identical; cross-face pairs-vs-offsets parity NO_DEFECT at 4 write states "
    "(S0 baseline / wait=true move / wait=true delete / clamp) incl. stale-cache probe; "
    "wait=true delete-gone verified 404-on-GET. Chunk closes the matrix family (offsets R46 + "
    "pairs R47): contract assertion text {pairs_a,pairs_b,scores,ids} vs measured "
    "{pairs:[{a,b,score}]} confirmed doc artifact (ticket 28), never claimed. D-segment "
    "addendum: matrix_pairs contract key-shape fix item stands; norm()-style float round-trip "
    "added to reviewer checklist for id canaries."
)

ms = json.load(open(f"{SD}/mine_state.json", encoding="utf-8"))
ms["current_round"] = 48
ms["last_round"] = {
    "round": 47,
    "chunk": "chunk_points+search+matrix+pairs",
    "verdicts": {"DEFECT": 0, "NOT_DEFECT": 0, "NME": 0},
    "note": NOTE,
}
ms["paused"] = False
ms["updated_at"] = now
json.dump(ms, open(f"{SD}/mine_state.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

ps = json.load(open(f"{SD}/pipeline_state.json", encoding="utf-8"))
ps["current_round"] = 48
ps["phase"] = "ROUND_START"
ps["phase_step_index"] = 0
ps["phases_completed"] = ["ROUND_START"]
ps.setdefault("phase_data", {})["ATTACK_GEN"] = {
    "ROUND_START": {"round": 48, "prev_round": 47, "prev_chunk": "chunk_points+search+matrix+pairs",
                    "prev_zero_candidate": True},
}
ps["phase_data"]["REPORT"] = {
    "round": 47,
    "chunk": "chunk_points+search+matrix+pairs",
    "scripts": 12,
    "path_accounting": {"A": 1, "B": 11},
    "first_pass": "7N + 3 DEFECT-candidates + 1 SE + 1 orphan draft (wspec_01 no-main)",
    "artifact_cycles": ("3 rerun waves / 6 mechanical fixes, all script-side forensics-verified: "
                        "det_03 exhaustive-only criterion on random legs; using_04 sig() unpack; "
                        "boundsA_01 tie-rich-fixture multiset flake (tie-tolerant (id,score) keys); "
                        "samp_03 norm() float(2**64-1)->2**64 self-corruption (exact-int bypass; "
                        "server replay corruption_seen=0); wspec_01 DELETE-route 404 -> POST "
                        "/points/delete; acknowledged legal UpdateStatus enum for wait=true delete "
                        "(GET 404 = effect verified)"),
    "final": "12/12 NO_DEFECT, gate 12/12 (after path-marker append), extract candidates = 0",
}
ps["updated_at"] = now
json.dump(ps, open(f"{SD}/pipeline_state.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

cv = json.load(open(f"{SD}/coverage.json", encoding="utf-8"))
cv["round"] = 47
cv["covered_chunks"] = 48
cv["chunks_done"] = 42
cv["overall_coverage_pct"] = round(48 / 66 * 100, 1)
cv["updated_at"] = now
cv.setdefault("endpoints", {})["points+search+matrix+pairs"] = (
    "R47 zero-candidate round #8: 12 scripts (boundary 5 [pathA bounds closure], semantic 4, state 3), "
    "all NO_DEFECT after a 3-wave artifact repair cycle. Positive evidence: u64-max canary round-trips "
    "EXACT on the pairs face (storage GET exact, exhaustive cells exact both orientations, full "
    "23-request state replay corruption_seen=0 — f64-corruption hypothesis disproven server-side); "
    "null/absent/explicit-default equivalence HOLDS (apparent divergence = tie-rich fixture's "
    "by-design tied-neighbour randomness); sample=1/sample=0/limit=0 -> 422 naming search_request.*; "
    "min closures sample=2/limit=1 accepted; above-count clamp COMPLIANT; exhaustive determinism "
    "two-run identical; cross-face pairs-vs-offsets parity NO_DEFECT across 4 write states incl. "
    "wait=true move/delete and stale-cache probe; wait=true delete returns acknowledged (legal enum) "
    "with verified effect. Contract {pairs_a,...} text = doc artifact (ticket 28), no claim. "
    "Script-side lessons banked: exhaustive-only criteria must be gated off random legs; id canaries "
    "must bypass float in normalize steps (float(2**64-1)->2**64 self-corruption); tie-rich linear "
    "fixtures require (id,score)-key comparisons; qdrant has NO DELETE /collections/{c}/points route."
)

json.dump(cv, open(f"{SD}/coverage.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# snapshot
for name in ("mine_state.json", "pipeline_state.json", "coverage.json"):
    shutil.copyfile(f"{SD}/{name}", f"{SD}/{name}.r47")

print("STATE_SAVE done: round 48 | coverage 48/66 =", cv["overall_coverage_pct"], "%")
