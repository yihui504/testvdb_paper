You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: milvus-io/milvus
Issue number: #52313
Reported DB version: 3.0.0
Title: [Bug]: entities/insert JSON field — plain strings stored in inconsistent formats across REST/gRPC; written values unreadable via gRPC (round-trip failure)
Contract claimed in the report: Issue: REST/gRPC persist different bytes for the same JSON-string input; REST-written rows unreadable via gRPC.
Probe observations:
  [c1] REST insert plain-string into JSON field -> http=200, code=0
  [c2] gRPC insert plain string -> DataNotMatchException code=1, message: Invalid JSON string
  [c_q] query meta -> http=200, code=0, data: id=100 meta=plain_string
  [c_grpc_get] gRPC get -> error: unexpected character (REST-written value unreadable)
L1 mechanical note: OK
