# Reviewer 2 Background: Area Specialist

## Specialty Areas Selected

1. **LLM-based test generation / LLM-as-judge reliability**
2. **Database-system testing (VDBMS and REST-API oracle tools)**

## Core Competitors Analyzed (from paper's Related Work)

### LLM-as-Judge Reliability

**Panickssery et al. (2024)** - "Self-Preference in LLM Evaluators" [panickssery24]
- Paper's claim: LLM evaluators favor outputs from their own family (self-preference bias)
- Relevance: TestVDB diagnoses this as one of two false-positive failure modes in judgment
- Verdict: The paper correctly identifies self-preference as a reliability threat; the dev-reviewer's source-grounded falsification directly addresses this by using implementation source as independent ground truth
- Novelty delta: TestVDB extends self-preference from general text evaluation to test-oracle pipelines, showing the same LLM family extracting claims and later judging them creates confirmation bias

**Haldar et al. (2025)** - "Intra-Judge Self-Inconsistency" [haldar25]
- Paper's claim: Single LLM judge's ratings on same input vary across runs (sampling noise)
- Relevance: Explains high variance in single-run dev-reviewer results (15-78% recall)
- Verdict: Paper correctly identifies sampling noise; TestVDB's any-confirmed ensemble (union of 3 runs) is the appropriate countermeasure
- Novelty delta: TestVDB operationalizes this insight by using ensemble union as the operating point rather than majority voting

**Ji et al. (2023)** - "Hallucination in LLMs" [ji23hall]
- Paper's claim: LLMs supply plausible content not supported by input
- Relevance: TestVDB diagnoses this as the other false-positive failure mode (extraction hallucination)
- Verdict: Paper correctly identifies hallucination; TestVDB's dev-reviewer uses source as falsifier to filter hallucinated claims
- Novelty delta: TestVDB maps hallucination to a specific test-oracle failure mode (over-strict constraints extracted from ambiguous documentation)

**Wataoka et al. (2024)** - "Rating Roulette" [wataoka24]
- Paper's claim: Self-recognition correlates with self-preference across model families
- Relevance: Additional evidence that same-family LLMs are biased toward their own outputs
- Verdict: Consistent with Panickssery; TestVDB's cross-model check (DeepSeek vs GLM-5.2) showing kappa=1.0 on 20 candidates suggests source-grounding mitigates family-specific bias
- Novelty delta: Cross-model validation on explicit source evidence shows the bias can be controlled when ground truth is external to the LLM

### Database-System Testing (REST-API Oracles)

**AGORA+ (2025)** - "REST-API Oracles from Execution Traces" [agoraplus25]
- Paper's claim: Infers invariants from observed traffic to generate test oracles
- Relevance: Paper cites it as structured-source approach that misses ambiguous-prose regime
- Verdict: Characterization is accurate - AGORA+ cannot reach inputs not in training traffic
- Novelty delta: TestVDB targets the complementary regime (natural-language documentation) that AGORA+ explicitly avoids

**SATORI (2025)** - "REST-API Oracles from OpenAPI" [satori25]
- Paper's claim: Extracts oracles from OpenAPI schema elements (type, format, min, max)
- Relevance: Paper cites it as low-ambiguity regime tool
- Verdict: Characterization accurate - SATORI stays in explicit-constraint regime
- Novelty delta: TestVDB enters high-ambiguity regime (natural-language prose) where SATORI's schema-based extraction fails

**MASTOR (2026)** - "REST-API Oracles from Source Code" [mastor26]
- Paper's claim: Reads source to encode implemented behavior as oracles
- Relevance: Paper cites it as closest work; notes MASTOR cannot detect documentation-implementation gaps
- Verdict: Characterization accurate - MASTOR encodes what code does, not what docs say
- Novelty delta: TestVDB uses source as falsifier of documentation-derived claims, targeting exactly the gap MASTOR cannot see

**VDBFuzz (2026)** - "VDBMS Fuzzer with Crash Oracle" [vdbfuzz26]
- Paper's claim: Crash-oracle fuzzer using template-based mutation
- Relevance: Direct comparison in RQ3 bidirectional probe
- Verdict: Paper correctly identifies VDBFuzz reaches crash-class only; TestVDB reaches silent-accept class
- Novelty delta: Complementary coverage confirmed by bidirectional probe - TestVDB reaches crash via contract reasoning (size=2^63 overflow) that VDBFuzz reaches directly; VDBFuzz misses silent-accept (wait=false zero-length vector) that TestVDB catches

**Metamorphic Relations (2024)** [metmap24]
- Paper's claim: Output relations for result correctness (top-k monotonicity, recall vs ef)
- Relevance: Paper cites as addressing result correctness but not input-acceptance
- Verdict: Characterization accurate - MRs are output relations, not input transforms
- Novelty delta: TestVDB targets input-acceptance decisions (reject vs accept) that MRs cannot capture

**Property-Based Testing (Claessen 2000)** [claessen00, schemathesis, quickrest20]
- Paper's claim: Needs machine-checkable property and OpenAPI schema
- Relevance: Paper cites as inapplicable to VDBMS (no OpenAPI encoding constraints)
- Verdict: Characterization accurate - VDBMS endpoints serve no schema encoding behavioral constraints
- Novelty delta: TestVDB uses LLM to extract constraints from prose where property-based testing requires schema

### Documentation-Derived Oracles

**Toradocu (2016)** [toradocu16]
- Paper's claim: Extracts oracles from Javadoc @throws using NLP/pattern matching
- Relevance: Pioneer in documentation-derived oracles
- Verdict: Paper correctly notes Toradocu handles simple syntactic patterns but acknowledges false positives from extraction failures
- Novelty delta: TestVDB uses LLM semantic interpretation for ambiguous prose where Toradocu's deterministic patterns fail

**Doc2OracLL (2025)** [doc2oracll25]
- Paper's claim: Extended Toradocu line to LLMs; documentation quality impacts oracle correctness
- Relevance: Shows LLM-based extraction depends on documentation clarity
- Verdict: TestVDB's dev-reviewer falsification addresses the quality dependency by checking extracted claims against source
- Novelty delta: TestVDB adds source-grounded falsifier where Doc2OracLL relies solely on LLM extraction

**AugmenTest (2025)** [augmentest25]
- Paper's claim: Infers oracles from available documentation
- Relevance: LLM-based oracle inference
- Verdict: TestVDB differs by using source as independent verification where AugmenTest uses runtime behavior
- Novelty delta: Source-grounded falsification vs differential execution

**ChatAssert (2024)** [chatassert24]
- Paper's claim: Addresses false positives through iterative prompt repair guided by compilation/execution feedback
- Relevance: False-positive suppression in LLM oracles
- Verdict: TestVDB uses source as static falsifier where ChatAssert uses dynamic execution feedback
- Novelty delta: Source-grounding allows catching silent-accept defects that execution cannot observe

**Testora (2026)** [testora26]
- Paper's claim: Uses natural-language PR descriptions as regression oracle; 55% precision with multi-question classifier
- Relevance: LLM-as-judge for test oracles
- Verdict: TestVDB achieves higher precision (67%) with source grounding; Testora's 55% shows LLM-only judgment ceiling
- Novelty delta: Source anchor lifts precision/recall beyond LLM-only judgment

## Coverage Search Conducted

Within LLM-based test generation, I scoped searches to:
1. "LLM test oracle hallucination" - surfaced Ji et al. (already cited)
2. "LLM judge self-preference" - surfaced Panickssery et al. (already cited)
3. "LLM test generation reliability" - surfaced Haldar et al. (already cited)

No uncited highly-related works surfaced; the paper's coverage in LLM-as-judge reliability is comprehensive for this defect class.

Within database-system testing, I scoped searches to:
1. "REST API test oracle generation" - surfaced AGORA+, SATORI, MASTOR (all cited)
2. "vector database testing" - surfaced VDBFuzz (cited)
3. "metamorphic testing database" - surfaced metmap24 (cited)

No uncited highly-related works surfaced; the paper's coverage in REST-API oracle tools is comprehensive.

## Summary

The paper's characterization of prior work is accurate. Novelty is well-positioned:
- Vs LLM-as-judge work: First to apply self-preference/hallucination theory to test-oracle pipelines with source-grounded falsification
- Vs REST-oracle tools: First to target natural-language documentation regime using LLM semantic interpretation
- Vs documentation-oracle work: First to use source as independent falsifier rather than execution feedback

No missing related work surfaced in scoped coverage searches within my specialties.
