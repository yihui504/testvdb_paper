You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #9525
Reported DB version: 1.18.2
Title: Systemic: serde deserialization errors across 7 endpoints expose Rust internal types (usize/u32/f32) and lack parameter names
Contract claimed in the report: Issue body: serde echoes Rust types (usize/u32/f32) and column offsets without parameter names; application-level validation (e.g. limit=0 -> 422 names param) proves Qdrant can produce good messages.
Probe observations:
  [c1] search with limit=-1 -> status=400, body: invalid value: integer `-1`, expected usize
  [c2] search with score_threshold=string -> status=400, body: invalid type: string, expected f32
  [c3] recommend with strategy=123 -> status=400, body: invalid type: integer `123`, expected string or map
  [c4] scroll with limit=-1 -> status=400, body: invalid value: integer `-1`, expected usize
  [c5] query with limit=-1 -> status=400, body: invalid value: integer `-1`, expected usize
L1 mechanical note: OK
