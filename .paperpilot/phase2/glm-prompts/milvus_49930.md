You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: milvus-io/milvus
Issue number: #49930
Reported DB version: 2.6.16
Title: [Bug]: REST API v2 accepts invalid searchParams (ef=0/-1 for HNSW, nprobe=0/-1 for IVF_FLAT) without validation
Contract claimed in the report: Issue: limit/offset validated, searchParams not; ef should be >=1, nprobe in [1,nlist].
Probe observations:
  [c1] HNSW search with ef=-1 -> http=200, code=0
  [c2] HNSW search with ef=0 -> http=200, code=0
  [c3] IVF_FLAT search with nprobe=0 -> http=200, code=0
L1 mechanical note: OK
