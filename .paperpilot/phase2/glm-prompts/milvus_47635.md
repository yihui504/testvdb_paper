You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: milvus-io/milvus
Issue number: #47635
Reported DB version: 2.3
Title: [Bug]: Search fails with Code 0 immediately after Collection.load() returns success
Contract claimed in the report: Code 0 is defined as Success in the Milvus API specification; search failing with code=0 violates the contract.
Probe observations:
  [c1] attempt 0 search ok (count=1)
  [c1] attempt 1 search ok (count=1)
  [c1] attempt 2 search ok (count=1)
  [c1] attempt 3 search ok (count=1)
  [c1] attempt 4 search ok (count=1)
  [c1] attempt 5 search ok (count=1)
  [c1] attempt 6 search ok (count=1)
  [c1] attempt 7 search ok (count=1)
  [c1] attempt 8 search ok (count=1)
  [c1] attempt 9 search ok (count=1)
  [c1] attempt 10 search ok (count=1)
  [c1] attempt 11 search ok (count=1)
L1 mechanical note: OK
