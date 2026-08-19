You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #9039
Reported DB version: 1.18.0
Title: Bug: Async upsert silently discards dimension-mismatched vectors (Poor Diagnostics)
Contract claimed in the report: Issue body: wait=true returns 400 with 'Vector dimension error', wait=false returns 200 'acknowledged' while discarding the point; acknowledged means received by WAL, not validated/stored.
Probe observations:
  [c1] async 3-dim upsert -> status=200 body={"result":{"operation_id":1,"status":"acknowledged"},"status":"ok","time":0.000208958} count_after=0 (http_status=200)
  [c2] sync(wait=true) 3-dim upsert -> status=400 body='{"status":{"error":"Wrong input: Vector dimension error: expected dim: 4, got 3"},"time":0.006035594}' (http_status=400)
L1 mechanical note: OK
