You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #9045
Reported DB version: 1.12.1
Title: Bug: Empty vector `[]` upsert with `wait=false` can trigger server panic (zero-length assertion failure)
Contract claimed in the report: Issue body: try_from_flatten rejects dim==0 ('MultiDenseVector cannot have zero dimension'); validate_vector_parameters only in debug_assert; #7967 documents a 'length must be greater than zero' panic.
Probe observations:
  [c1] sync empty-vector upsert -> status=400, count=0 (http_status=400)
  [c2] async empty-vector upsert -> status=200 count=0 (http_status=200)
  [server_health] GET / after crash attempt -> status=200 (http_status=200)
L1 mechanical note: OK
