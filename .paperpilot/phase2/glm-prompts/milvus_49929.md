You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: milvus-io/milvus
Issue number: #49929
Reported DB version: 2.6.16
Title: [Bug]: REST API and PyMilvus SDK have inconsistent default index creation behavior
Contract claimed in the report: Issue: same logical operation (create -> create_index) yields different outcomes across REST and SDK.
Probe observations:
  [c1] REST create_index on bare collection -> http=200, code=100
  [c2] SDK create_index after quick-create -> MilvusException code=65535 (message: CreateIndex failed: creating multiple indexes on same field is not supported)
L1 mechanical note: OK
