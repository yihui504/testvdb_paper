# -*- coding: utf-8 -*-
"""R41 STATE_SAVE: mine_state + pipeline_state + coverage + snapshots."""
import json
from datetime import datetime, timezone

SD = r"C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.5.0/results/qdrant/v1.18.0/2026-09-04T12-14-11Z"
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---- mine_state ----
ms = json.load(open(f"{SD}/mine_state.json", encoding="utf-8"))
ms["current_round"] = 42
ms["last_round"] = {
    "round": 41,
    "chunk": "chunk_points+recommend+groups",
    "verdicts": {"DEFECT": 0, "NOT_DEFECT": 0, "NME": 0},
    "note": "16/16 NO_DEFECT (16 scripts: boundary 6 [1 pathA+5 pathB] / state 5 / semantic 5). First run 8 DEFECT candidates + 2 SCRIPT_ERROR (payload_04 tuple-arity R17-blindspot, envB_05 NoneType.get) -> main-process forensics adjudicated ALL artifacts: (a) committed openapi RecommendGroupsRequest group_size/limit = uint NO minimum -> 0->200 {groups:[]} spec-legal (synthetic-rubric artifact, R15 precedent); (b) serde value-type error messages unnamed -> defect-61 family cross-ref (R38 numbered), while M1-M3 missing-field legs DO name = diagnostics layering positive evidence; (c) offset silent flatten-ignore = R38 adjudicated characterization; (d) id-form positives SELF-EXCLUDE on groups face = R39 exclusion-chain pinned (geoB_06 AVG1 split AVG1a raw + AVG1b self-exclusion cross-pin); (e) stratmath_02 symmetric fixture [1,9] tied id4/id6 best at sfs(-9)=0.05 -> asymmetric re-pin [1,7]; (f) vecless_41 strategy=average script bug -> average_vector (groups enum has no alias); (g) offsetB_04 helper rebuilt body with default gs=3 (L5 fake-diverge) -> helper fixed; (h) D5b/D7 legs extended defect-61 family waiver per general ruling. Kill-leg 2^62 rejected 400 u32, no OOM, container healthy throughout. Zero-candidate round #2.",
}
ms["paused"] = False
json.dump(ms, open(f"{SD}/mine_state.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---- pipeline_state ----
ps = json.load(open(f"{SD}/pipeline_state.json", encoding="utf-8"))
ps["current_round"] = 42
ps["phase"] = "ROUND_START"
ps["phase_step_index"] = 0
ps["phases_completed"] = ["ROUND_START"]
ps.setdefault("phase_data", {})["ATTACK_GEN"] = {
    "ROUND_START": {"round": 42, "prev_round": 41, "prev_chunk": "chunk_points+recommend+groups", "prev_zero_candidate": True},
}
ps["phase_data"]["REPORT"] = {
    "round": 41,
    "chunk": "chunk_points+recommend+groups",
    "scripts": 16,
    "path_accounting": {"A": 2, "B": 14},
    "first_pass": "7N/8D-candidates/1 crash(payload_04 tuple-arity, no verdict) + envB_05 SCRIPT_ERROR",
    "artifact_cycles": "1 cycle: 8 DEFECT candidates + 2 SE all adjudicated artifacts (9 fixes across 3 agents: 6 boundary [incl geoB_06 forensic] + 2 semantic + 1 state repair [new agent, original stopped])",
    "final": "16/16 NO_DEFECT, gate 16/16 PASS, extract rg candidates = 0",
    "kill_leg": "diag_03 group_size=2^62 -> 400 u32 deserializer (no OOM, container healthy)",
}
json.dump(ps, open(f"{SD}/pipeline_state.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---- coverage ----
cv = json.load(open(f"{SD}/coverage.json", encoding="utf-8"))
cv["round"] = 41
cv["covered_chunks"] = 41
cv["chunks_done"] = 36
cv["overall_coverage_pct"] = round(41 / 66 * 100, 1)
cv["updated_at"] = now
cv.setdefault("endpoints", {})["points+recommend+groups"] = (
    "R41 zero-candidate round #2: 16 scripts (boundary 6 [slotA/typeA pathA + 4 pathB], state 5, semantic 5), "
    "all NO_DEFECT after 1 artifact cycle. Key characterizations: group_size REQUIRED on this face (missing -> 400 named, "
    "unlike query-groups default-3); group_size/limit 0 -> 200 empty groups spec-legal (uint no minimum in committed "
    "openapi); offset silent flatten-ignore (R38 cross-ref); id-form positives self-exclude (defect-62 exclusion-chain "
    "groups-face extension); strategy math re-pinned (avg plain distance, best_score sfs(-d2) strict>, sum d2-sums); "
    "group_by grp-less exclusion + dual membership + u64 canary clean; with_lookup both forms + ghost 404 clean; "
    "envelope GroupsResult conformant; serde unnamed-message legs = defect-61 family cross-ref; 2^62 kill-leg 400 u32."
)
json.dump(cv, open(f"{SD}/coverage.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---- snapshots ----
for f in ("mine_state", "pipeline_state", "coverage"):
    open(f"{SD}/{f}.json.r41", "w", encoding="utf-8").write(open(f"{SD}/{f}.json", encoding="utf-8").read())

print("STATE_SAVE done: round 42, coverage 41/66 = 62.1%, snapshots .r41 written")
