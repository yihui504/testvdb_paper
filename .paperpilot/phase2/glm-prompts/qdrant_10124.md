You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
Repo: qdrant/qdrant
Issue number: #10124
Reported DB version: 1.18.3
Title: `count` `exact=false` on numeric/datetime `range` filter returns bidirectionally-wrong counts (histogram estimator)
Contract claimed in the report: Issue body: FieldCondition.range 'check if points value lies in a given range'; exact=false uses a histogram estimator with stable +/-5-10% error at steady state; exact=true always correct.
Probe observations:
  [c1] count exact=true range 100..200 -> status=200, count=48
  [c2] count exact=false range 100..200 -> status=200, count=65 (exact=true gave 48)
  [c3] count exact=false gte=500 -> status=200, count=242
  [c4] count exact=false lte=300 -> status=200, count=166
L1 mechanical note: OK
