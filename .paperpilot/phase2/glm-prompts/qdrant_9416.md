You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #9416
Reported DB version: 1.18.2
Title: `vectors={}` silently accepted during collection creation — produces unusable collection
Contract claimed in the report: Issue body: API doc marks vectors required=false; vectors={} accepted 200 then any point op fails 'Default vector config is not found in collection'.
Probe observations:
  [c1] vectors={} create -> status=200, collection_exists=True (http_status=200)
  [c2] upsert into vectorless collection -> status=400 body='{"status":{"error":"Wrong input: Not existing vector name error: "},"time":0.005177777}' (no default vector config -> unusable) (http_status=400)
L1 mechanical note: OK
