You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: milvus-io/milvus
Issue number: #52308
Reported DB version: 3.0.0
Title: [Bug]: REST API v2 `entities/insert` accepts string numbers for Int64 primary key (type coercion gap; gRPC rejects)
Contract claimed in the report: Primary Field docs define Int64/VarChar PK; REST silently coerces strings instead of rejecting.
Probe observations:
  [c1] REST insert string PK '123' -> http=200, code=0
  [c1_q] query id=123 -> http=200, code=101, message: collection not loaded
  [c1_grpc] gRPC insert string PK -> DataNotMatchException code=1, message: id field should be int64, got str
  [c2] REST insert non-numeric string PK 'abc' -> http=200, code=1804
  [c2_q] query id=0 -> http=200, code=101, message: collection not loaded
L1 mechanical note: OK
