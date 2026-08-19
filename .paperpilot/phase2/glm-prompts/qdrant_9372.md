You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #9372
Reported DB version: 1.18.2
Title: Strict mode inconsistently validates zero values — allows creation of unusable collections
Contract claimed in the report: Issue body: consistency matrix shows 3 fields reject 0 (422) while filter_max_conditions and upsert_max_batchsize accept 0 (200) producing a poisoned collection.
Probe observations:
  [c1] create with max_query_limit=0 -> status=422
  [c2] create with filter_max_conditions=0 -> status=200; filtered scroll -> status=400, body: Filter condition limit reached (1 > 0)
  [c3] create with upsert_max_batchsize=0 -> status=200; upsert -> status=400, body: Limit exceeded 1 > 0 for upsert limit
L1 mechanical note: OK
