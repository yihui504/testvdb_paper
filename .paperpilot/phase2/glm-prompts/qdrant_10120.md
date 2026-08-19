You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #10120
Reported DB version: 1.18.3
Title: `count` `exact=false` on `is_empty` under-counts ~35% consistently; `is_null` on the same field is correct
Contract claimed in the report: Issue body: OpenAPI declares exact=false 'approximate count might be unreliable during indexing'; is_empty under-counts ~35% at steady state while is_null is exact-correct, isolating the estimator path.
Probe observations:
  [c1] count exact=true is_empty -> status=200, count=40
  [c2] count exact=false is_empty -> status=200, count=25 (exact=true gave 40)
  [c3] control: count exact=false is_null -> status=200, count=0
L1 mechanical note: OK
