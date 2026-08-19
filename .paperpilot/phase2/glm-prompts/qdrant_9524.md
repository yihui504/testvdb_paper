You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #9524
Reported DB version: 1.18.2
Title: Invalid filter conditions silently accepted (200 OK) with poor error diagnostics across search/query/scroll endpoints
Contract claimed in the report: Issue body: 5 classes of invalid filters silently accepted (empty must, nonexistent field, type mismatch, contradictory range, wrong structure); rejected cases lack parameter names in serde messages.
Probe observations:
  [c1] search with empty must [] -> status=None (read timeout, no response)
  [c2] search with non-existent field -> status=None (read timeout, no response)
  [c3] search with contradictory range (gt>lt) -> status=None (read timeout, no response)
  [c4] search with null key -> status=None (read timeout)
L1 mechanical note: OK
