You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #10125
Reported DB version: 1.18.3
Title: `count` `exact=false` on compound filter under-counts 20-60% when conditions touch the same field (independence assumption)
Contract claimed in the report: Issue body: cardinality estimator assumes independence across combined conditions; same-field (red AND must_not blue) under-counts ~20-60% while single-condition is exact.
Probe observations:
  [c1] control: count exact=false kw=red -> status=200, count=130
  [c2] count exact=false compound (kw=red AND NOT kw=blue) -> status=200, count=101 (single kw=red gave 130)
  [c3] count exact=false cross-field (kw=red AND cat=x) -> status=200, count=63
L1 mechanical note: OK
