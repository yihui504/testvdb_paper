You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: weaviate/weaviate
Issue number: #11745
Reported DB version: 1.38.0
Title: Text property accepts strings containing ASCII control characters (SOH, STX, ETX)
Contract claimed in the report: RFC 8259 section 7 requires C0 control chars in JSON strings to be escaped; raw control bytes are non-printable and pollute indexes.
Probe observations:
  [c1] POST schema TestText -> http=200
  [c2] POST object with raw 0x01 0x02 0x03 control bytes in text_field -> http=400
L1 mechanical note: OK
