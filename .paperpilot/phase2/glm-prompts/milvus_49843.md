You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: milvus-io/milvus
Issue number: #49843
Reported DB version: 2.6.16
Title: [Bug]: REST API v2 silently drops negative collection.ttl.seconds on collection create
Contract claimed in the report: alter_properties error message; PR #46717 added TTL validation to createCollectionTask.PreExecute but REST create bypasses it.
Probe observations:
  [c1] create with negative TTL -> http=200, code=0
  [c1_rb] describe collection after negative-TTL create -> http=200
  [c2] control: alter_properties with negative TTL -> http=200, code=1100
L1 mechanical note: OK
