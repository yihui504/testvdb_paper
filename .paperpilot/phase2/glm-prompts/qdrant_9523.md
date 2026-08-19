You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #9523
Reported DB version: 1.18.2
Title: Search offset pagination returns duplicate point IDs across pages (HNSW approximation)
Contract claimed in the report: Issue body: offset pagination with HNSW is non-deterministic; scroll cursor pagination does not have this problem.
Probe observations:
  [c1] page1 offset=0 ids=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] (http_status=200)
  [c2] page2 offset=10 ids=[10, 11, 12, 13, 14, 15, 16, 17, 18, 19] overlap_with_p1=[] (http_status=200)
  [c3] page3 offset=20 ids=[20, 21, 22, 23, 24] unique_union=25 duplicate_sets=[] (http_status=200)
  [c4] scroll control ids=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] (non-overlapping cursor) (http_status=200)
L1 mechanical note: OK
