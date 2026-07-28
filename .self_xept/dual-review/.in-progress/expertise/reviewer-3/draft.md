## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
This paper presents TestVDB, a system for detecting documentation-implementation defects in Vector Database Management Systems (VDBMSs). The authors identify a gap where existing crash-oracle fuzzers like VDBFuzz miss logical bugs that manifest as silent acceptance of invalid inputs rather than crashes. TestVDB uses LLMs to extract behavioral claims from natural-language documentation, generate tests, and adjudicate whether responses violate documented expectations. A key contribution is a "dev-reviewer" agent that grounds verdicts in implementation source code to counter two LLM failure modes: hallucination in claim extraction and self-preference bias in judgment. The authors report 107 submitted issues across three VDBMSs with 49 maintainer-acknowledged true positives (15 fixed via merged PR), and on a 48-candidate retrospective, the dev-reviewer achieves 67% precision and 74% recall versus 37% recall without source grounding.

### Core Strengths
- **S1:** Well-motivated problem space — see 1.1, the distinction between crash-oracle and documentation-implementation defects is clearly articulated with a concrete example (nprobe=0).
- **S2:** Oracle-exclusion argument is systematic — see 2.1, Table 1 provides a clear walkthrough of why each existing oracle candidate misses the documentation-implementation residual.
- **S3:** Source-grounded falsification contribution is sound — see 3.1, the dev-reviewer's three-check falsification mechanism is well-specified with appropriate justification for moving ground truth from LLM to implementation source.
- **S4:** Empirical evaluation demonstrates real-world impact — see 4.1, the 49 maintainer-acknowledged defects including 15 merged PR fixes show practical utility beyond a theoretical contribution.

### Core Weaknesses
- **W1:** Novelty is incremental rather than transformative — see 2.2, the core LLM-as-judge reliability problem and source-grounded falsification solution are not new ideas; the contribution is primarily in applying known techniques to a new domain (VDBMSs).
- **W2:** Post-hoc operating point selection weakens RQ2 claims — see 4.2 [major, fixable], the 3-run union ensemble is selected after examining multiple operating points without pre-registration, and the Wilson CIs do not account for this selection, risking overfitting to the retrospective dataset.
- **W3:** External validity is limited — see 4.3 [major, fixable], generalization claims beyond VDBMSs rest on a single CouchDB pilot (n=5 probes) with no defects found; this is insufficient evidence for the broader transferability claim to "REST APIs without OpenAPI, configuration validation, and policy-as-code."

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** The problem is well-motivated. Section 1 clearly articulates why documentation-implementation defects matter: they corrupt query semantics in retrieval-augmented LLM applications where wrong context silently reaches the model. The Milvus #49823 example (nprobe=0 accepted despite documented range [1, 16384]) is a concrete instance that shows real impact. The 15 merged-PR fixes across three production VDBMSs demonstrate that maintainers recognize and prioritize these defects, supporting practical significance.

- **1.2 [minor, fixable]** Scope is narrower than framing suggests. The title and introduction position this as a general solution to "documentation-implementation defects," but the evaluation is VDBMS-only. Section 6 (Discussion) acknowledges this but claims transferability to "REST APIs without OpenAPI, configuration validation, and policy-as-code" on structural grounds alone. The CouchDB pilot (n=5 probes, zero defects found) is insufficient evidence for this broader claim, which overstates the scope relative to what's empirically demonstrated.

#### 2. Novelty — Adequate (provisional)

- **2.1** The oracle-exclusion argument is the strongest novelty contribution. Table 1 provides a systematic walkthrough of why each existing oracle candidate (crash, differential, metamorphic, property-based, REST doc/spec-derived) misses the documentation-implementation residual, with specific citations to each tool and a clear structural reason. This framing clarifies why LLMs are the practical oracle for this residual and is a useful conceptual contribution for researchers in oracle design.

- **2.2 [major, unfixable]** Core reliability techniques are not new. Section 5 identifies two LLM failure modes (hallucination at extraction, self-preference in judgment) and cites established work on both [ji23hall, panickssery24]. Source-grounded falsification as a mitigation is conceptually similar to prior work on using independent signals to correct LLM biases, though the specific application to test oracles and the three-check mechanism (reproducibility, evidence sufficiency, falsifiability) is a reasonable instantiation. The contribution is primarily domain-specific (VDBMSs) rather than methodologically novel.

- **2.3** Related work coverage is adequate for a VDBMS-focused contribution. Section 7 cites REST-API oracle tools (AGORA+, SATORI, MASTOR) and explains the boundary: those tools assume low-ambiguity structured sources, while TestVDB targets the ambiguous-prose regime. The distinction is clear. I have not surveyed the broader LLM-as-judge or documentation-derived oracle literature, so my Novelty assessment is provisional pending a reviewer with field expertise.

#### 3. Soundness — Adequate

- **3.1** The core claim is supported. Section 4.1 (RQ1) reports 107 submitted issues with 49 maintainer-acknowledged true positives. Table 2 breaks this down by vendor (Milvus 22/51, Qdrant 14/26, Weaviate 13/30). The 68.1% precision (Wilson 95% CI [56.6%, 77.7%]) on adjudicated submissions and 15 merged-PR fixes across three production VDBMSs are concrete evidence that TestVDB surfaces real defects worth fixing.

- **3.2 [major, fixable]** Operating point selection in RQ2 is post-hoc and not accounted for in uncertainty. Section 4.2 evaluates four operating points (single-run, 3-run union, 5-run union, 5-run majority) and selects the 3-run union as the headline because "it sits at the knee of the precision-recall trade-off." This selection is hypothesis-generating rather than hypothesis-testing, and the Wilson CIs in Table 4 do not account for selection across four operating points. A Bonferroni correction (α=0.05/4) would widen the 3-run precision CI to roughly [44%, 84%] and recall to [51%, 89%], which the authors acknowledge but do not incorporate into their headline claims. The 37% → 74% recall gain comparison is against a single-LLM baseline, but Table 5 shows that multi-perspective judging achieves 80% precision at 15% recall—substantially different precision-recall trade-offs that make the "without source grounding" comparison potentially cherry-picked.

- **3.3** Method ablation is well-designed. Section 4.2 reports a three-condition ablation on a 12-FP/4-TP control (Table 6): clean-reproduction only (17% FP suppression), source-grounded alone (75%), threat-model alone (50%), union (91%). The source-grounded anchor is clearly the dominant contributor, and the isolation of source grounding's contribution on the full 48-candidate retrospective (recall drops from 74% to 19% without it) provides strong evidence that source access drives the recall gain.

- **3.4** Threats to validity are appropriately disclosed. Section 4.4 clearly states limitations: single-run variance (15–78% recall), the 48-candidate retrospective is maintainer-adjudicated but non-random and not pre-registered, no public ground-truth defect catalog exists for VDBMSs (so recall cannot be estimated), the implementation-as-correct assumption bounds the approach, and cross-family generalization is an open question (κ=0.14 DeepSeek, κ=0.51 LongCat vs. GLM). This transparency is adequate.

#### 4. Verifiability — Adequate

- **4.1** Paper is self-contained for the core pipeline. Section 3 provides a clear four-stage description (behavioral-claim extraction, test-script generation, sandboxed execution, defect confirmation) with a diagram (Figure 1). The dev-reviewer's three-check falsification mechanism (Figure 2, Section 5) is specified with sufficient detail to understand the logic: independently reproducible, evidence sufficient, falsifiable. The Milvus #49823 example walk-through (Section 3) anchors the abstract description.

- **4.2 [minor, fixable]** Artifact availability is claimed but not verifiable from text. Section 3 states "The full prompts, target versions, and per-token accounting are in the artifact, which we will release at a persistent URL upon acceptance." This is standard practice, but the URL is not provided, so I cannot verify the artifact exists or assess its completeness. Section 3 also mentions cost (roughly $10 per target at current API pricing) and LLM-call distribution (Table 3), which is useful but does not substitute for inspecting the actual prompts and implementation.

- **4.3** Critical parameters are reported. Section 4.2 specifies the retrospective size (48 candidates: 27 TP, 21 FP), the VDBMS versions under test (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2), the LLM backbone (GLM-5.2), and the operating points evaluated. This is sufficient to understand the experimental setup.

#### 5. Presentation — Adequate

- **5.1** Structure is logical and follows a clear narrative arc. Introduction → Problem Setup (oracle-exclusion) → Approach (TestVDB pipeline) → False-Positive Problem (diagnosing LLM failure modes) → Dev-Reviewer (solution) → Evaluation (three RQs) → Related Work → Discussion/Limitations → Conclusion. Sectioning is appropriate and the flow is coherent.

- **5.2** Writing is clear with minor issues. The prose is generally understandable, but some sentences are dense and could be simplified for clarity. For example, the second sentence in the abstract ("Because the boundary is natural-language prose, current instantiations...") packs three oracle types and a structural reason into one clause. The technical description is adequate but could be more accessible.

- **5.3 [minor, fixable]** Some notation inconsistency. Table 1 uses bullet symbols for row separators that appear as rendered characters; this is a minor formatting issue. Figure 1 and Figure 2 use TikZ diagrams that are clear but could benefit from more explicit labels (e.g., "NL docs" and "impl source" in Figure 1 are somewhat terse).

- **5.4** Citations are adequate for a domain-focused paper. I have not verified whether critical works are missing, but the cited works (VDBFuzz, AGORA+, SATORI, MASTOR, LLM-as-judge reliability studies) are relevant and properly contextualized.
