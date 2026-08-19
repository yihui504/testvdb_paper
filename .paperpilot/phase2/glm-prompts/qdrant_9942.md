You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #9942
Reported DB version: 1.18.2
Title: OpenAPI schema for `VectorParams.size` is missing the enforced `maximum: 65536` constraint
Contract claimed in the report: Issue body: server rejects size=70000 with 422 'must be from 1 to 65536' but VectorParams.size schema only declares minimum:1; DenseVectorConfig.size already has maximum:65536.
Probe observations:
  [c1] GET VectorParams.size schema -> status=404 (schema=None)
  [c2] create with size=70000 -> status=422, body: vectors.size: value 70000 invalid, must be from 1 to 65536
L1 mechanical note: CONTRADICT
