# -*- coding: utf-8 -*-
"""R42 STATE_SAVE: mine_state + pipeline_state + coverage + snapshots."""
import json
from datetime import datetime, timezone

SD = r"C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.5.0/results/qdrant/v1.18.0/2026-09-04T12-14-11Z"
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

ms = json.load(open(f"{SD}/mine_state.json", encoding="utf-8"))
ms["current_round"] = 43
ms["last_round"] = {
    "round": 42,
    "chunk": "chunk_points+scroll",
    "verdicts": {"DEFECT": 0, "NOT_DEFECT": 0, "NME": 0},
    "note": "16/16 NO_DEFECT (boundary 6 [limitA pathA + 5 pathB] / state 5 / semantic 5). First run 7N + 5 DEFECT-candidates + 4 SCRIPT_ERROR -> forensics ALL artifacts: (a) index create ghost-route PUT /collections/{c}/index/{field} (DELETE-only, R35 fact) -> correct PUT /collections/{c}/index body {field_name, field_schema} — killed 3 SEs + orderby_03 fake-Type1 (indexes never existed, no-range-index 400 was correct); (b) string-id fixture used 'a'..'h' (illegal point id; must be UUID/u64); (c) fullwalk comparator type bug ([1..8] equal printed, judged unequal — R26/R39 family); (d) pagB_03 ghost leg self-polluted by its own u64 canary point (id-order >= offset semantics => canary correctly returned); (e) pagconB_04 D1 ignored its own wait=true id=0 upsert (read-your-write correct); (f) envelope_01 with_payload={} -> 400 spec-legal (WithPayloadInterface oneOf[bool, array, PayloadSelector{include|exclude}] — {} matches none; contrast MaybeOneOrMany); agent-side extra: strid ghost-offset >= semantics two-sided re-pin; orderby_03 desc-monotonicity assert bug fixed; residual 409 -> idempotent pre-drop. Capability matrix POSITIVE evidence: integer/float/datetime -> 200 asc (datetime micro-integers); keyword/bool/geo -> 400 named despite index-create 200 (range-capability line held); limit=0 -> 422 names scroll_request.limit (validator present, defect-59 contrast); offset INCLUSIVE characterized both faces. Kill-risk legs (INT_MAX/u32max/u64max) zero container kills. Zero-candidate round #3.",
}
ms["paused"] = False
json.dump(ms, open(f"{SD}/mine_state.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

ps = json.load(open(f"{SD}/pipeline_state.json", encoding="utf-8"))
ps["current_round"] = 43
ps["phase"] = "ROUND_START"
ps["phase_step_index"] = 0
ps["phases_completed"] = ["ROUND_START"]
ps.setdefault("phase_data", {})["ATTACK_GEN"] = {
    "ROUND_START": {"round": 43, "prev_round": 42, "prev_chunk": "chunk_points+scroll", "prev_zero_candidate": True},
}
ps["phase_data"]["REPORT"] = {
    "round": 42,
    "chunk": "chunk_points+scroll",
    "scripts": 16,
    "path_accounting": {"A": 1, "B": 15},
    "first_pass": "7N/5D-candidates/4 SE (3 ghost-route index + 1 illegal string-id)",
    "artifact_cycles": "1 cycle: 5 candidates + 4 SE all artifacts (ghost-route PUT index; UUID point ids; comparator type bug; canary-vs-ghost fixture pollution; read-your-write miss; with_payload={} spec-legal)",
    "final": "16/16 NO_DEFECT, gate 16/16, extract sc candidates = 0",
    "kill_leg": "3 kill-risk scripts (INT_MAX/u32max/u64max) completed, zero container kills",
}
json.dump(ps, open(f"{SD}/pipeline_state.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

cv = json.load(open(f"{SD}/coverage.json", encoding="utf-8"))
cv["round"] = 42
cv["covered_chunks"] = 42
cv["chunks_done"] = 37
cv["overall_coverage_pct"] = round(42 / 66 * 100, 1)
cv["updated_at"] = now
cv.setdefault("endpoints", {})["points+scroll"] = (
    "R42 zero-candidate round #3: 16 scripts (boundary 6 [pathA limit closure], state 5, semantic 5), all NO_DEFECT "
    "after 1 artifact cycle. Positive evidence: limit minimum:1 validator fires 422 naming scroll_request.limit "
    "(defect-59 contrast: hnsw_ef had no validator); pagination npo-chain = exact partition; offset INCLUSIVE "
    ">= semantics (spec text) characterized on int/str-uuid/u64 ids; ghost offset exhausted; u64 canary round-trip "
    "digit-exact; order_by range-capability matrix = integer/float/datetime 200 asc vs keyword/text/bool/geo 400 "
    "named (doc line held); delete-index revokes capability; order_by tracks current state under writes; "
    "with_payload default TRUE echo + false strip + {} 400 spec-legal; cursor stability under upsert/delete writes. "
    "Ops lessons: ghost-route PUT /index/{field} (DELETE-only) vs body-form PUT /index; point ids must be u64/UUID; "
    "ghost-offset legs mutually exclusive with u64 canary points in same fixture."
)
json.dump(cv, open(f"{SD}/coverage.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

for f in ("mine_state", "pipeline_state", "coverage"):
    open(f"{SD}/{f}.json.r42", "w", encoding="utf-8").write(open(f"{SD}/{f}.json", encoding="utf-8").read())

print("STATE_SAVE done: round 43, coverage 42/66 = 63.6%, snapshots .r42")
