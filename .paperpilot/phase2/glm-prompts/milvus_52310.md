You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: milvus-io/milvus
Issue number: #52310
Reported DB version: 3.0.0
Title: [Bug]: REST API v2 `entities/insert` silently coerces scalar types (string→Int64, int→VarChar, string→Bool); gRPC rejects all
Contract claimed in the report: Number Field docs define distinct INT64/BOOL/FLOAT types; REST still coerces (gRPC fixed in 2.6.14).
Probe observations:
  [c1] REST insert string '123' into INT64 field -> http=200, code=0
  [c1_q] query int64_f -> http=200, code=101, message: collection not loaded
  [c2] REST insert int 123 into VarChar field -> http=200, code=0
  [c2_q] query varchar_f -> http=200, code=101, message: collection not loaded
  [c3] REST insert string 'true' into BOOL field -> http=200, code=0
  [c3_q] query bool_f -> http=200, code=101, message: collection not loaded
L1 mechanical note: OK
