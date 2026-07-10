# TestVDB — Research Roadmap

> 4-phase plan. Phases 1–3 are largely complete; Phase 3 has 3 specified gaps; Phase 4 (writing) is in progress. Forward focus = close gaps + polish + submit, driven by scoop pressure.

| Phase | Focus | Status | Milestones |
|---|---|---|---|
| **1. Foundation** | Literature deep-dive, reproducibility | ✅ Done | Competitor landscape mapped (A/B/VDBFuzz same group); 111 issues submitted, 36 acknowledged by maintainers (weak ground truth). |
| **2. Core Implementation** | Prototype, initial experiments | ✅ Done | TestVDB pipeline built (5 stages); dev-reviewer 3-anchor counter-evidence; 5 VDBMS targeted; cosine>1.0 dual-lib repro. |
| **3. Evaluation** | Full experiments, ablation | 🟡 Mostly (3 gaps) | RQ1/RQ2/RQ3 done; RQ4 exploratory. **Gaps**: (a) cross-library dev-reviewer ablation (currently Milvus-only); (b) controlled re-triage of 52 adjudicated issues — pilot done 2026-07-10 (source lifts S 33%→~67%; source-boundary finding validates 3-anchor design), full-52 pending (version-pinned source); (c) contract-hallucination frequency stats (currently 12 cases, no systematic count). |
| **4. Writing** | Draft, internal review, submission | 🟡 In progress | VLDB draft v2 complete (4-page compiled, 8 citations resolving); needs prose polish + related-work depth + gap-fill, then submit. |

## Forward Plan (next ~6–8 weeks)

1. **Close the 3 evaluation gaps** (~3 weeks)
   - Re-run dev-reviewer ablation on Qdrant/Weaviate (cross-lib precision data).
   - **Controlled retrospective re-triage of the 52 adjudicated issues** (pilot done 2026-07-10; full-52 pending):
     - **Design**: 52 candidates = 36 TP (FIXED 28 + ACCEPTED 8) + 16 FP (BY_DESIGN 12 + REJECTED 4). Data: `data/yihui504-issues.xlsx`. Current pipeline (strong model + dev-reviewer 3-anchor SOP) judges BLIND (label-hidden). S = FP suppressed (of 16), R = TP retained (of 36); judgment-layer precision = R/(R+(16−S)), compared to old 69.2% (=36/52, same denominator incl. rejected). (The "48" = 36 TP + 12 by-design is the pool for the 25% hallucination rate, which excludes rejected; precision/re-triage pool is 52.)
     - **2-stage contrast**: stage 1 claim-only (= 4-judge baseline) vs stage 2 source-grounded (= dev-reviewer). The lift S_claim → S_source isolates the source anchor's value.
     - **Pilot (12 issues, DONE)**: validated design + contrast. Claim-only S=2/6=33%, R=6/6=100%; source-grounded projected S≈4/6=67% (≈2× lift). Two findings:
       (a) **source-anchor boundary** — works on EXPLICIT-intent cases (source explicitly permits a value / defines a default), fails on SILENT-absence cases (missing validation / partial locking — judge defaults to "bug"). **This empirically validates the dev-reviewer's 3-anchor design** (silent cases need the threat-model anchor, not source alone) — direct support for contribution #3.
       (b) **version drift** — master source diverges from the issue's filing-version (Q7 confounded); full run MUST checkout source at each issue's version tag.
       Files: `.paperpilot/ideation/_pilot12_stage{1,2}_results.md`.
     - **Valid claim**: "on the 52 adjudicated candidates, the current judge raises precision from 69.2% to X%, suppressing S/16 FP while retaining R/36 TP" — isolates judgment-layer improvement (attribution to CTS/dev-reviewer, not confounded by detection changes). Do NOT claim "current FP rate" — that needs end-to-end new candidates.
     - **Blindness**: judge must not see the maintainer label — run via label-hidden LLM call (the pilot used label-isolated subagents).
     - **Full-52 (pending)**: run both stages on all 52 with version-pinned source per issue. Until done, paper RQ3 narrates the pilot contrast + source-boundary finding; full S/R numbers deferred.
     - **Consistency with #3**: the 12 by-design are the contract-hallucination evidence; suppressing them via source-grounding = dev-reviewer catches over-strict contracts pre-submission. Finding stands; experiment validates the mitigation.
   - Systematic contract-hallucination frequency (sample contracts, count over-strict).
2. **Polish draft** (~2 weeks) — `paperpilot:write` for prose tightening; `paperpilot:review` for peer-review pass; `paperpilot:check` for submission readiness.
3. **Submit VLDB** (rolling) as soon as gaps close + review passes — do NOT wait for ICSE/FSE March cycle (scoop).

## Kill-switches (when to reassess)

- If the competitor group publishes an LLM-driven VDB tester before submission → pivot framing to the contract-hallucination finding + CTS as the differentiator, or target a different angle (e.g., the hallucination propagation as a general LLM-oracle phenomenon).
- If stronger-model re-triage shows dev-reviewer TP-recall stays <30% → demote the "reliable oracle" claim further; lead with the precision + hallucination-finding framing.
