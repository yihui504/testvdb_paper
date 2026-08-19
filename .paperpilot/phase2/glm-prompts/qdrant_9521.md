You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #9521
Reported DB version: 1.18.2
Title: Silent data loss: named vector upsert in single-vector collection returns 200 OK but point is discarded
Contract claimed in the report: Issue body: collection has unnamed vectors; named-vector format is accepted 200/acknowledged but point discarded (count=0); wrong-dimension is correctly rejected 400.
Probe observations:
  [c1] named-vector upsert into single-vec coll -> status=400, count=0 (stored/rejected, OK) (http_status=400)
  [c2] wrong-dim(6) upsert -> status=400 body='{"status":{"error":"Wrong input: Vector dimension error: expected dim: 4, got 6"},"time":0.000158351}' (http_status=400)
L1 mechanical note: OK
