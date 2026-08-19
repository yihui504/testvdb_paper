You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: milvus-io/milvus
Issue number: #52307
Reported DB version: 3.0.0
Title: [Bug]: entities/upsert JSON field — plain string overwrites valid JSON; written value unreadable via gRPC; REST/gRPC store inconsistent formats
Contract claimed in the report: JSON Field docs describe type as structured key-value data; server must not accept a write it cannot serve back.
Probe observations:
  [c1] REST upsert bare string into JSON field -> http=200, code=0
  [c1_q] query meta after REST upsert -> http=200, code=101, message: collection not loaded
  [c1_grpc_get] gRPC get id=0 -> code=101, message: collection not loaded
  [c1b] gRPC upsert plain string -> DataNotMatchException code=1, message: Invalid JSON string
L1 mechanical note: OK
