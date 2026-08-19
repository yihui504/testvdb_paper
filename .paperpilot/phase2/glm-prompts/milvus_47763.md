You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: milvus-io/milvus
Issue number: #47763
Reported DB version: 2.6.10
Title: [Bug]:  Field name validation missing - accepts invalid field names causing data inaccessibility
Contract claimed in the report: Milvus Limitations doc: 'A resource name must start with a letter or an underscore'.
Probe observations:
  [c1] insert dynamic field names '123field'/'@field' -> http=200, code=0
  [c1_q] query field '123field' -> http=200, code=65535, message: parse output field name failed: 123field
  [c2] control: insert valid field name -> http=200, code=0
  [c2_q] control: query valid field -> http=200, code=101, message: collection not loaded
L1 mechanical note: OK
