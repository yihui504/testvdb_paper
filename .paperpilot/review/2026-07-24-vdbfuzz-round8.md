## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs): cases where an API silently accepts an input that violates its natural-language documentation, such as `nprobe=0` or out-of-range HNSW parameters. Because classical oracles (crash, differential, metamorphic, property-based) cannot reach these accept/reject decisions, the paper adopts an LLM to extract behavioral claims from documentation and judge consistency, then introduces source-grounded falsification to address the resulting interpretation errors. Across five VDBMSs, TestVDB surfaced 111 candidate issues; 50 are true-positive defects (36 confirmed, 14 with open fix-PRs). On a controlled retrospective over 48 adjudicated candidates, the source-grounded dev-reviewer with a 3-run union ensemble reaches 67% precision and 74% recall, versus 37% recall without source grounding.

The core contribution is identifying and resolving the two-layer reliability problem: family-specific LLM self-preference (mitigated by cross-model validation) and task-intrinsic documentation-interpretation errors (mitigated by source-grounded falsification). A probe on 18 over-strict clauses shows that cross-model judging misses 3 of 6 task-intrinsic clauses while source falsification catches all 18, and that over-strict concentrates in optional-default APIs (Milvus, Qdrant search parameters) rather than explicit-bound parameters (Weaviate). The paper also quantifies the documentation-implementation residual: about 85% of submitted issues are unreachable by classical oracles.

### Core Strengths

- **S1:** Clear problem formulation and rigorous positioning against the oracle taxonomy (Barr et al. 2015) — see §2, Table 1
- **S2:** Well-executed empirical evaluation with controlled head-to-head against VDBFuzz establishing complementary coverage — see §7, Table 2
- **S3:** Threats to validity section that explicitly scopes claims and acknowledges limitations — see §7, Table 3
- **S4:** Reusable artifact: the model-free invariant oracle subclass (COSINE bounds, index completeness) is classical-addressable and independent of the LLM pipeline — see §7, RQ4

### Core Weaknesses

- **W1:** RQ2 ensemble choice is data-backed (union 67%/74% vs majority 64%/26% — both operating points reported, showing majority sacrifices recall without a precision gain) but would benefit from a fuller operating-characteristic analysis (precision-recall curve, or error analysis of which true positives majority voting kills) — see §7, RQ2 paragraph
- **W2:** MASTOR framing gap: paper correctly identifies source-as-falsifier novelty but omits that MASTOR already demonstrated source-grounded oracle generation — see §5, Related Work
- **W3:** RQ3 statistical ambiguity: pooled task-intrinsic rate (17/29 = 59%) blends parameter (6/18 = 33%) and behavior (11/11 = 100%) subtypes, obscuring the finding — see §7, RQ3 paragraph

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** The problem is well-motivated and practical. VDBMSs are critical infrastructure for LLM applications, and the 111 issues submitted (50 TP) demonstrate that documentation-implementation defects are a real, prevalent class. The roadmap~\cite{roadmap25} and bug study~\cite{bugstudy25} establish this as a recognized research direction. The 85% residual quantification (Table 1, RQ1) provides a compelling structural reason why existing oracles fail: accept/reject decisions diverge by design across VDBMSs and cannot be mechanically checked when boundaries are natural-language. The bidirectional head-to-head with VDBFuzz (Table 2, §7) sharpens this beyond the disjoint-classes observation: crash oracles miss silent accepts; documentation-implementation oracles can reach crash-class defects where the crash-triggering input violates a documented bound. — **This is strong evidence of practical impact.**

- **1.2 [major, fixable]** The generalization claim is under-scoped. §9 claims "Any system whose documentation is natural-language prose rather than a structured specification enters this setting," yet the evaluation is entirely on VDBMS APIs. The evidence for transferability to REST APIs without OpenAPI, configuration validation, or policy-as-code is absent. This weakens the claimed broad applicability. The limitation should be scoped to VDBMSs and structurally similar systems until empirical transfer evidence exists. — **See §9, first paragraph.**

- **1.3** The 85% documentation-implementation residual composition is well-validated. Table 1 explicitly maps each oracle family to the defect class it reaches and why it misses the documentation-implementation residual. The RQ1 fault model classification (classical-addressable vs documentation-implementation vs concurrency) covers all 111 submissions, and the per-issue mapping is in the artifact, making the 85% figure auditable rather than asserted. The controlled VDBFuzz head-to-head (Table 2) strengthens this beyond theoretical classification. — **See Table 1, §7, RQ1.**

#### 2. Novelty — Adequate

- **2.1** The two-layer reliability problem framing is novel and well-differentiated from prior LLM-as-judge work. Family-specific self-preference (Panickssery et al. 2024; Wataoka & Takahashi 2024) is established; task-intrinsic errors, where different families converge on the same wrong clause because the ambiguity is in the shared documentation, is a new contribution. The RQ3 probe on 18 over-strict clauses (DeepSeek reproduces GLM's over-strict claim on 6/18 parameters) provides concrete evidence. The distinction from Haldar et al.'s (2025) intra-judge self-inconsistency (run-to-run variation) is precisely scoped: task-intrinsic stability is an extraction-level property across families, not a sampling-noise phenomenon in judgment. — **See §4, RQ3 probe.**

- **2.2 [major, fixable]** MASTOR framing gap obscures the actual novelty delta. The paper correctly states that MASTOR tests implemented behavior (source encodes what the impl does) while TestVDB tests documentation-prescribed behavior (source falsifies what docs say), but omits that MASTOR already demonstrated source-grounded oracle generation. The novelty is the *asymmetric usage direction* (source as falsifier of LLM-derived claims), not source-grounding per se. Acknowledging that MASTOR is also source-grounded would sharpen the positioning: TestVDB contributes source-as-independent-verification-source for documentation-derived claims, where MASTOR uses source as the oracle itself. — **See §5, paragraph 3; §8.**

- **2.3** The optional-default vs explicit-bound predictor is a strong, falsifiable contribution. RQ3 shows that over-strict concentrates in APIs with optional defaults and no explicit bound (Milvus `ef`, `nprobe`, `level`, `replicaNumber`; Qdrant `timeout`, `group_size`, `score_threshold`, `m`, `bits`) and is absent where documentation states explicit minimums (Weaviate `ef` "Must be >= 1"; Qdrant `shard_number`, `replication_factor` "Minimum 1"). The within-vendor contrast (Qdrant: search params with optional defaults are over-strict; collection params with explicit minimums are not; same pattern on Milvus) isolates documentation style rather than vendor as the driver. This is a mechanistic finding with predictive power. — **See §7, RQ3 paragraph; Table 3.**

- **2.4 [minor, fixable]** The pooled task-intrinsic rate (17/29 = 59%) obscures the subtype finding. Parameters are 6/18 (33%); behaviors are 11/11 (100%). Pooling them dilutes the core result: the behavior phenomenon (11/11) is far stronger than the parameter phenomenon (6/18). The separate reporting is buried mid-paragraph; elevating it to the headline would strengthen the contribution. — **See §7, RQ3 paragraph 2.**

- **2.5** Related Work coverage is adequate for the core competitors. The paper correctly characterizes VDBFuzz (crash-only, complementary), AGORA+ (trace-inferred invariants, structured), SATORI (OpenAPI spec, structured), Toradocu (NLP pattern-based, limited to simple patterns), and the doc-derived oracle line (Doc2OracLL, AugmenTest, ChatAssert, Testora, Konstantinou et al.). No high-impact uncited work was found in scoped searches. The MASTOR framing gap (2.2) is the only omission. — **See §8.**

#### 3. Soundness — Adequate

- **3.1** The RQ1 yield quantification is rigorous. 111 candidates across 5 VDBMSs (Milvus 51, Weaviate 30, Qdrant 26, MeiliSearch 3, Chroma 1); 50 TP (36 confirmed: 32 maintainer-acknowledged + 4 fixed via merged PR; 14 with open fix-PRs). The yield precision on maintainer-adjudicated submissions (72 total: 50 TP + 22 by-design/rejected) is 69.4% (Wilson 95% CI [58.0%, 78.9%]). Treating the 15 pending as FP gives a worst-case bound of [47%, 67%]. The per-issue fault model classification (all 111 mapped to classical-addressable/documentation-implementation/concurrency) is in the artifact, making the 85% documentation-implementation residual auditable. — **See §7, RQ1; Table 3.**

- **3.2** The RQ2 retrospective design is sound but has a single-control limitation. The 48-candidate set (27 TP, 21 FP; Milvus 32, Qdrant 16) is maintainer-adjudicated, which is strong ground truth. The 3-run union ensemble (67% precision, 74% recall) is a clear improvement over the single-LLM baseline (48%/56%/37%). The single-run variance (recall 15-78%; precision 50-73%; accuracy 44-65%) is reported, and the 5-run any-confirmed ensemble (62% precision, 85% recall) is provided. However, the earlier 81%/69.2%/96.7% single-run, single-vendor figures were based on a 16-candidate control whose data is no longer recoverable and are superseded by this cross-vendor ensemble; the paper correctly flags this. — **See §7, RQ2 paragraph.**

- **3.3 [minor, fixable]** RQ2 ensemble justification is data-backed but could go further. The paper reports both operating points (union 3-run 67%/74%, 5-run 62%/85%; majority 64%/26%) and the data already shows that majority voting sacrifices recall (26%) without a precision gain (64% sits within the single-run precision band 50-73%), which supports the union choice. A fuller operating-characteristic analysis (precision-recall curve, or an error analysis of which true positives majority voting specifically kills) would further strengthen the claim. — **See §7, RQ2 paragraph.**

- **3.4** The RQ3 probe design is methodologically careful. The 18-clause probe (13 Milvus + 5 Qdrant) is live-probe-confirmed (each over-strict clause is verified by API testing). The scaling from the original 12-clause pilot to 18 via two passes (Milvus `ef`, `nprobe`, `level`, `replicaNumber`; Qdrant `m`, `bits`) is transparent. The two verification directions—DeepSeek independent formalization (reproduces 6/18) and DeepSeek judging GLM's clauses (catches 8/18, misses 3 of 6 task-intrinsic)—are well-controlled. The behavior-level probe (11/11 TI) and explicit-bound negative control (0/21 TI) establish the phenomenon's boundaries. The only limitation is that all 18 clauses are from GLM's collection; independent sampling from other families would rule out extractor-specific bias. — **See §7, RQ3; Table 3.**

- **3.5** The cross-model dev-reviewer verification (DeepSeek re-runs 20 candidates, Cohen's κ = 1.0) is strong evidence that source-grounded verdicts are not family-specific when source evidence is explicit. The 20-candidate sample spans input-validation, upsert-semantics, idempotent-drop, correct-reject, and dynamic-field subtypes and is non-random but diversity-stratified, which is acceptable given the perfect agreement. — **See §7, RQ2 paragraph.**

- **3.6** Threats to validity (§7) are well-structured and honest. Internal validity: RQ3 covers 50 clauses (18 over-strict + 11 behavior + 21 explicit-bound); the retrospective and yield are the broader evidence base. External: generalization to Weaviate/MeiliSearch/Chroma is breadth-only; statistical claims rest on Milvus/Qdrant; ANN correctness is out-of-scope. Construct: source-anchor results use single family (GLM-5.2); cross-model check (κ = 1.0) suggests verdicts are not family-specific, but recall cannot be estimated without a public ground-truth defect catalog. These are appropriately scoped. — **See §7, "Threats to validity."**

#### 4. Verifiability — Adequate

- **4.1** The paper commits to artifact release: "full prompts, target versions, and per-token accounting are in the artifact, which we will release at a persistent URL upon acceptance" (§6). The 111-submission mapping (all 111 assigned to fault models with one-line rationale), the 48 adjudicated candidates, all five dev-reviewer runs, and the corrected ground truth (27 TP + 21 FP after Qdrant reclassification) are promised in the artifact. This satisfies the bar for reproducibility. — **See §6, paragraph 1; §7, RQ2 footnote.**

- **4.2** The method description is complete enough to follow the pipeline flow. The five stages (extraction → attack generation → LLM judgment → dev-reviewer falsification → novelty gate) and the three anchors (clean reproduction, source-grounded, threat-model cross-check) are clearly described. The falsification rule is concrete: for a clause `parameter ≥ 1`, if source shows `parameter = 0` selects the default, the clause is over-strict and falsified. — **See §5, paragraphs 2-4.**

- **4.3 [minor, fixable]** The runtime cost quantification could be more precise. "On the order of $10^4$ LLM calls and roughly $10 per target" is vague. A table with per-stage LLM call counts and costs would strengthen verifiability. — **See §6, paragraph 1.**

- **4.4** The stability analysis (5-run ensemble, single-run variance) is promised in the artifact but not fully visualized in the paper. A variance plot (recall distribution across runs) would be more informative than the text-only range (15-78%). — **See §7, RQ2 paragraph; footnote 13.**

#### 5. Presentation — Adequate

- **5.1 [minor, fixable]** The structure is sound but some pacing is uneven. Table 1 (oracle exclusion) is excellent and clearly motivates the problem. The RQ2 ensemble justification (3.3) is dense and could benefit from a precision-recall curve. The RQ3 pooled vs subtype reporting (2.4) obscures the behavior finding. — **See Table 1; §7, RQ2/RQ3.**

- **5.2 [minor, fixable]** Notation consistency: "COSINE" distance is all-caps in RQ4 but "cosine" appears in RQ1. Standardize on one. — **See §7, RQ1 vs RQ4.**

- **5.3** Figures and tables are clear. Table 1's structure is excellent. Table 2 (bidirectional reachability) is simple but effective. Table 3 (RQ3 probe) is dense but legible. No broken figures or formatting issues detected. — **See Tables 1-3.**

- **5.4** Language is generally clear with minor awkwardness. "Large class of their defects lacks a practical oracle" (abstract) could be "a large class... lacks." "The test oracle problem~\cite{barr15} is acute here" (§2) is informal but acceptable. No pervasive issues. — **See abstract, §2.**

### Questions for Authors

- **Q1:** Can you provide a precision-recall curve or operating-point analysis for the union vs majority ensemble rule? Item 3.3's rating would move from Adequate toward Excellent if the union choice is empirically grounded rather than pragmatically justified. — **Intended effect:** clarify the data-driven rationale for union over majority; if analysis shows union does not inflate precision beyond per-run variance, 3.3 → Excellent.

- **Q2:** Can you acknowledge MASTOR as prior source-grounded oracle generation work and sharpen the novelty delta to source-as-falsifier (asymmetric usage) rather than source-grounding itself? Item 2.2's rating would move to Excellent if this framing gap is addressed. — **Intended effect:** correct the Related Work omission; 2.2 → Excellent.

- **Q3:** Can you elevate the behavior-TI finding (11/11 = 100%) to the headline and pool only for aggregate statistics, rather than leading with the pooled rate (17/29 = 59%)? Item 2.4's rating would move to Excellent if this clarification is made. — **Intended effect:** surface the stronger behavioral result; 2.4 → Excellent.

- **Q4:** Can you scope the generalization claim (§9) to VDBMSs and structurally similar systems until empirical transfer evidence exists? Item 1.2's rating would move to Excellent if the claim is conservatively scoped. — **Intended effect:** tighten the over-broad applicability claim; 1.2 → Excellent.


## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs), where APIs silently accept inputs that violate their natural-language API documentation. The paper argues that existing oracle families (crash, differential, metamorphic, property-based) cannot reach about 85% of these defects because the documented boundary is ambiguous prose rather than formal specifications, forcing adoption of an LLM as both extractor and semantic judge. The authors decompose LLM reliability errors into two layers: family-specific self-preference (mitigated by cross-model validation) and task-intrinsic documentation-interpretation errors where different families converge on the same wrong claim (resolved by source-grounded falsification). TestVDB instantiates this as a multi-agent pipeline that falsifies LLM-derived behavioral claims against source code. Across five VDBMSs, TestVDB surfaced 111 candidate issues; 50 are true-positive defects (36 confirmed, 14 with open fix-PRs). A controlled retrospective on Milvus and Qdrant shows the source-grounded dev-reviewer reaches 67% precision and 74% recall (3-run ensemble) versus 37% recall without source grounding.

### Core Strengths

- **S1:** Two-layer LLM-error decomposition (family-specific vs task-intrinsic) is well-motivated and empirically validated — see 5.2, RQ3.

- **S2:** Source-grounded falsification mechanism provides a principled counter to task-intrinsic interpretation errors that cross-model validation cannot reach — see 5, 6, Table 3.

- **S3:** Head-to-head VDBFuzz bidirectional reachability probe sharpens the documentation-implementation residual beyond disjoint-class observation — see 5.1, Table 2.

- **S4:** Explicit documentation-style finding (over-strict concentrates in optional-default APIs, absent in explicit-bound APIs) is a strong, falsifiable prediction — see 5.3.

### Core Weaknesses

- **W1:** RQ2 reports both operating points (majority-vote 64%/26%; union 67%/74%) and designates the 3-run union as the headline, explicitly dismissing majority voting as too low-recall. The presentation could foreground that designation more (the majority-vote numbers appear in the same paragraph, skimmable). — see 5.2.

- **W2:** Single-run variance (recall 15-78%) reported but not mechanistically explained or mitigated beyond ensemble aggregation — see 5.2. The source-grounded anchor's stability is unclear.

- **W3:** κ=1.0 on a 20-case non-random sample is insufficient to establish that source-grounded verdicts are family-independent — see 5.2. This is a strong claim needing broader validation.

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** The problem is significant: VDBMSs are critical infrastructure for RAG systems, and documentation-implementation defects corrupt query semantics. The 85% residual claim (about 89% on the 50-TP subset) that classical oracles cannot reach these defects is compelling and well-supported by the structural argument (Table 1) plus the VDBFuzz head-to-head (5.1). The bug study and roadmap citations ground this in recognized VDBMS challenges.

- **1.2 [minor, fixable]** The significance claim is bounded to VDBMSs. The discussion (8) acknowledges generalizability to other natural-language documentation settings (REST APIs without OpenAPI, configuration validation, policy-as-code) but provides no evidence. This does not undermine the VDBMS contribution but limits the claimed broader impact.

#### 2. Novelty — Adequate

- **2.1** The two-layer LLM-error decomposition is a clear contribution. Family-specific self-preference is established (Panickssery, Wataoka), but task-intrinsic documentation-interpretation errors where different families converge on the same wrong claim is a novel phenomenon. The probe on eighteen over-strict clauses (6 task-intrinsic) and the behavior probe (11/11 task-intrinsic) strongly validate this distinction (5.3, Table 3). The separation of extraction-level stability (task-intrinsic) from judgment-level inconsistency (Haldar) is correctly scoped.

- **2.2** Source-grounded falsification as a mechanism to resolve task-intrinsic errors is novel. MASTOR (mastor26), the closest prior work, extracts oracles from source to test implementation behavior (source as reference for expected behavior). TestVDB inverts this: it tests documentation-prescribed behavior against source (source as reference for actual behavior). The paper's characterization (5, Section 6) accurately positions this delta. The other REST-oracle works (AGORA+, SATORI, Toradocu, Doc2OracLL, ChatAssert, Testora) operate in low-ambiguity regimes or trust LLM output without falsification — TestVDB's high-ambiguity documentation regime plus source falsification is the clear novelty.

- **2.3 [minor, fixable]** The ensemble rule and the source-grounded contribution should be decoupled more clearly for novelty presentation. RQ2 presents the union operating point (67%/74%, designated the headline) and the majority-vote alternative (64%/26%, dismissed as too low-recall) in the same paragraph; leading with the union headline and presenting majority-vote only as a sensitivity comparison would sharpen the core claim. [retracted on check: an earlier draft claimed the union was "buried" and that 26% reads as the best achievable point — the paper in fact presents union first and explicitly labels majority voting as unusable.]

#### 3. Soundness — Adequate

- **3.1** The 85% residual classification is methodologically sound. Each of the 111 submissions is assigned to one fault model (classical-addressable, documentation-implementation, concurrency) with a one-line rationale, and the paper states this mapping is in the artifact for auditability. The structural argument (Table 1) mapping why each classical oracle fails is convincing, and the VDBFuzz bidirectional probe (5.1, Table 2) sharpens this beyond theoretical classification.

- **3.2** The RQ3 probe design is methodologically strong. The eighteen-clause parameter probe (6 task-intrinsic), the eleven-clause behavior probe (11/11 task-intrinsic), and the twenty-one-clause explicit-bound negative control (0/21 over-strict) form a complete, falsifiable test. The within-vendor contrast (Qdrant's optional-default parameters over-strict vs explicit-bound parameters not; same pattern on Milvus) is compelling evidence that documentation style drives over-formalization, not vendor. The prediction that "optional-default + no explicit bound → over-strict candidate" is a direct, testable hypothesis.

- **3.3 [minor, fixable]** The RQ2 retrospective (48 candidates) is a small sample, and the paper already scopes the statistical claims to Milvus and Qdrant (Threats to Validity) and reports wide single-run variance (recall 15-78%). The residual concern is presentational: the 67%/74% headline should be framed clearly as a point estimate on this scoped retrospective rather than reading as a stable population property — a framing fix, not a new experiment. [retracted on check: an earlier draft marked this "major, unfixable" and implied the paper overclaims generalizability; the paper in fact scopes to Milvus/Qdrant and discloses the variance.]

- **3.4 [minor, fixable]** The κ=1.0 inter-rater reliability claim between GLM-5.2 and DeepSeek on 20 candidates is based on a non-random, diversity-stratified sample. The paper describes it as "chosen to span input-validation, upsert-semantics, idempotent-drop, correct-reject, and dynamic-field subtypes" — this is purposeful, not random. κ=1.0 on a purposive 20-case sample does not establish that source-grounded verdicts are family-independent in general; it only shows no disagreement on these specific cases. A random sample or larger set would be needed to substantiate the claim that "the source-grounded verdict does not appear family-specific."

- **3.5 [minor, fixable]** The single-run variance (recall 15-78%) is reported but not explained. The paper states that "some runs are conservative and confirm few candidates rather than admitting many false positives" as the cause, but provides no evidence or mechanism. Is the variance due to LLM sampling stochasticity? Attack agent diversity? Dev-reviewer source interpretation differences? Without a mechanistic explanation or mitigation strategy beyond ensemble aggregation, it is unclear whether the source-grounded anchor itself is stable or only the ensemble union across runs is stable.

#### 4. Verifiability — Adequate

- **4.1** The paper provides sufficient information to understand the method and results. The five-stage pipeline (Section 5), the dev-reviewer's three anchors (Section 5), and the per-RQ experimental design are described in enough detail to follow the logic. The artifact promise (prompts, target versions, per-token accounting, 48 candidates, all five runs) is comprehensive.

- **4.2** The links are declared but not verified. The paper states that the artifact will be released "at a persistent URL upon acceptance," which is standard practice. The GitHub issue links in Section 5 (Qdrant #9045, #7967) are specific and verifiable.

#### 5. Presentation — Adequate

- **5.1** The structure is logical and complete. Problem setup → LLM reliability regime → TestVDB design → Evaluation → Related Work → Discussion follows a clear narrative arc. The two-layer error decomposition (Section 5) is well-explained.

- **5.2 [minor, fixable]** RQ2 (Section 5.2) is structurally confusing. It first presents the 3-run ensemble results (65% accuracy, 67% precision, 74% recall) as the headline. Then it introduces single-run variance (15-78% recall). Then it introduces majority voting (64% precision, 26% recall) as an alternative operating point but dismisses it as "recall too low to be useful." Then it returns to the union ensemble as "the operating point" without clearly flagging which operating point readers should take away. The sentence "The union rule, by surfacing candidates that any run confirms, captures signals from high-recall runs without inflating false positives beyond the per-run precision band" attempts justification, but this should be upfront: state early that the paper reports union and majority-vote operating points, recommend union, and explain why. As written, the key performance claim is buried.

- **5.3 [minor, fixable]** Table 3 (cross-model judging vs source-grounded falsification) lists 18 clauses but the total row shows "8/18" for cross-model judging caught. Column 3 is labeled "Cross-model judging" but should be "Caught by cross-model judging" for clarity. The "TI" column marking task-intrinsic status is useful but would benefit from a footnote explaining how TI is determined (second family's independent formalization also over-strict on the same parameter).

- **5.4 [minor, fixable]** Minor typos and inconsistencies: "punctuated by" (used multiple times) is stylistically repetitive. "The two reachability directions are not symmetric" (Section 8) could be clearer as "The two reachability directions exhibit asymmetry."

### Questions for Authors

- **Q1:** The RQ2 section designates the 3-run union ensemble (67% precision, 74% recall) as the headline and dismisses the majority-vote alternative (64% precision, 26% recall) as too low-recall. Could the presentation foreground the union headline earlier and present majority-vote as a sensitivity comparison? This would address W1.

- **Q2:** What mechanism explains the wide single-run variance (recall 15-78%)? Is it LLM sampling stochasticity, attack agent diversity, dev-reviewer source interpretation differences, or something else? Understanding this would address W2 and strengthen confidence in the source-grounded anchor's stability.

- **Q3:** Can you substantiate the family-independent claim with a random sample or larger set beyond the 20-case diversity-stratified sample? κ=1.0 on a purposive sample is suggestive but not sufficient to establish general independence (addresses 3.4).

- **Q4:** The 48-candidate retrospective is the primary evidence for the 67%/74% performance claim, but this is a small subset of the 111 submissions. Do you have interim results from the "ongoing" larger head-to-head study that would provide a more stable estimate? If not, should the headline claim be qualified as "on a 48-candidate retrospective" rather than presented as a general property?


## Reviewer 3: General Reviewer

**Overall Recommendation:** Accept

### Summary
TestVDB addresses documentation-implementation consistency defects in Vector Database Management Systems (VDBMSs), where APIs silently accept inputs that violate their documentation. The authors argue that classical oracles (crash, differential, metamorphic, property-based) cannot reach this defect class because accept/reject decisions are based on natural-language documentation rather than formal specifications. Their solution is source-grounded falsification: an LLM extracts behavioral claims from documentation, which are then falsified against the actual implementation source code. The authors evaluate TestVDB on five VDBMSs, reporting 111 submitted issues with 50 true-positive defects (36 confirmed, 14 with open fix-PRs), and provide controlled experiments showing their source-grounded dev-reviewer achieves 67% precision and 74% recall versus 37% recall without source anchoring. They further distinguish family-specific from task-intrinsic LLM errors and show that cross-model validation cannot resolve task-intrinsic errors where documentation ambiguity causes multiple LLM families to converge on the same wrong claim.

### Core Strengths
- **S1:** Clear problem framing and contribution structure — see §§1–2, where the authors distinguish documentation-implementation consistency from correctness, map the residual against classical oracles (Table 1), and explicitly scope what LLMs contribute and where they fail.
- **S2:** Grounded empirical evaluation with disclosed limitations — see §6, particularly the RQ2 retrospective on 48 adjudicated candidates, the RQ3 cross-model validation probe (Table 4), and the threats-to-validity subsection that honestly flags what the evidence does not cover.
- **S3:** Well-motivated use of source as a falsification anchor — see §5, where the authors contrast their source-grounded approach with REST-API oracle work (AGORA+, SATORI, MASTOR) and explain why MASTOR's use of source cannot detect documentation-implementation gaps, whereas TestVDB's approach explicitly targets them.

### Core Weaknesses
- **W1:** Statistical claims rest on a narrow subsample — see §6, RQ2, where the 67% precision and 74% recall figures derive from a controlled retrospective on only 48 adjudicated candidates (27 TP, 21 FP) across Milvus and Qdrant, with no grounding beyond these two vendors.
- **W2:** Documentation-style correlation is observational, not causal — see §6, RQ3, where the authors observe that over-strict clauses concentrate in optional-default APIs (Milvus, Qdrant) and are absent where documentation states explicit bounds (Weaviate), but acknowledge this is a correlative finding and that ruling out alternative explanations (team structure, implementation complexity) is future work.

### Detailed Assessment

#### 1. Significance — Adequate
- **1.1** The problem addressed is real and practically motivated — see Introduction §1, where the authors cite an empirical VDBMS bug study attributing ~43% of bugs to incorrect behavior and identify oracle definition as a key challenge. Documentation-implementation defects corrupt query semantics and the large majority produce no crash, making them invisible to fuzzers like VDBFuzz. This is a meaningful, scoped problem.
- **1.2** The solution approach is targeted to the problem's structure — see §4, where the authors argue that because documented boundaries are natural-language prose rather than formal, an LLM must both extract behavioral claims and, where extraction fails, judge documentation consistency directly. This dual role introduces reliability problems that source-grounded falsification addresses by treating implementation source as an independent reference. The design logically follows from the problem diagnosis.
- **1.3** Impact is bounded by the problem domain — see §8, where the authors acknowledge that source-grounded falsification requires source and does not transfer to closed-source VDBMSs, and that the 85% documentation-implementation residual is the composition of TestVDB's findings (biased toward this class by design) rather than an estimate of the true defect distribution. The contribution is useful within its scope but is not a broad new testing methodology applicable beyond settings where natural-language documentation creates an LLM interpretation gap.

#### 2. Novelty — Adequate
- **2.1** The authors clearly separate their contribution from prior REST-API oracle work — see §4, where they contrast TestVDB's setting (ambiguous natural-language documentation forcing LLM interpretation) with AGORA+, SATORI, and MASTOR (low-ambiguity structured sources where LLMs transcribe explicit constraints). They articulate that their source-ambiguity gap is what distinguishes VDBMS documentation-implementation consistency testing from this prior line.
- **2.2** The distinction between family-specific and task-intrinsic LLM interpretation errors is non-obvious — see §4, where the authors define task-intrinsic stability as an extraction-level property across model families and demonstrate, on an eighteen-clause probe, that DeepSeek independently reproduces GLM's over-strict claim on 6 of 18 parameters, with cross-model judging missing 3 of these 6. This two-layer reliability decomposition (family-specific vs. task-intrinsic) and the finding that cross-model validation cannot resolve the task-intrinsic layer are incremental but meaningful contributions.
- **2.3** The use of source as a falsification anchor is not conceptually novel but is applied to a new problem — see §5, where the authors contrast their approach with MASTOR's use of source to generate oracles encoding implemented behavior. TestVDB uses source to falsify documentation-derived claims rather than to generate them, which is a real delta but a narrow one. The novelty lies in the specific instantiation (source-grounded falsification of LLM-derived behavioral claims for documentation-implementation consistency) rather than in the broad idea of using source as a reference.

#### 3. Soundness — Adequate
- **3.1** Main claims are supported by appropriate evidence — see §6, where the authors report 111 submitted issues across five VDBMSs with 50 true-positive defects (36 confirmed, 14 with open fix-PRs), and a controlled retrospective on 48 adjudicated candidates showing the source-grounded dev-reviewer achieves 67% precision and 74% recall versus 37% recall without source anchoring. The RQ3 probe on eighteen over-strict clauses shows cross-model judging misses 3 of 6 task-intrinsic clauses while source-grounded falsification contradicts all 18. The main claims (yield, recall gain, task-intrinsic errors) are defensible.
- **3.2 [major, fixable]** Statistical rigor is limited for the headline precision/recall figures — see §6, RQ2, where the 67% precision and 74% recall derive from a controlled retrospective on only 48 adjudicated candidates (27 TP, 21 FP) across Milvus and Qdrant. The authors report Wilson 95% CIs and acknowledge they do not estimate recall because there is no public ground-truth defect catalog. However, the narrow subsample (two vendors, 48 candidates) limits the strength of the quantitative claim. A revision could clarify that these figures are provisional estimates from a small adjudicated set rather than population-level statistics.
- **3.3** The documentation-style correlation is presented as correlative, not causal — see §6, RQ3, where the authors observe that over-strict clauses concentrate in APIs with optional-default parameters (Milvus, Qdrant) and are absent where documentation states explicit bounds (Weaviate). They validate this with within-vendor contrasts (on Qdrant, three search parameters with optional defaults are over-strict, while collection parameters stating explicit minimums are not) and acknowledge in §8 that ruling out alternative explanations is future work. This is honest reporting of a correlative finding, but the presentation in the RQ3 paragraph could be clearer that this is an observation rather than a causal claim.
- **3.4** The VDBFuzz head-to-head is appropriately framed as hypothesis-generating — see §6, RQ1, where the authors run a bidirectional reachability probe on specific Qdrant versions (v1.4.0 reproduces VDBFuzz's integer-overflow crash; v1.18.0 predates the fix for TestVDB's #9045). They explicitly state "each direction is n=1" and treat these as controlled cases rather than a generalized result, which is appropriate given the single-case-per-direction limitation.

#### 4. Verifiability — Excellent
- **4.1** The paper provides enough detail to follow how results were produced — see §5 (Implementation), which describes the multi-agent pipeline on the Claude Code runtime, the 20 agents dispatched to a GLM-5.2 backbone, pinned Docker versions for target VDBMSs, and the rough cost (~$10 per target, 10^4 LLM calls). The per-vendor breakdowns in Table 3, the 18-clause probe in Table 4, and the threat-model cross-check description in RQ2 are all sufficient to understand the experimental setup.
- **4.2** Key procedural details are disclosed — see §6, where the authors describe the adjudication process (72 maintainer-adjudicated submissions: 50 TP, 22 by-design/rejected), the single-run variance across five independent runs (recall 15–78%), the rationale for using the any-confirmed ensemble operating point, and the per-anchor ablation on a 12-FP/4-TP control. The cross-model validation methodology (DeepSeek formalizing documentation independently, then judging GLM's clauses) is also clearly specified.
- **4.3** The authors commit to artifact availability — see §5, where the authors state "the full prompts, target versions, and per-token accounting are in the artifact, which we will release at a persistent URL upon acceptance." This commitment supports verification, and the text alone describes the methodology well enough to follow the work.

#### 5. Presentation — Excellent
- **5.1** Structure is clear and logical — the paper follows a standard and well-motivated progression: problem setup (§2), the LLM role and its reliability problem (§4), TestVDB design (§5), implementation details (§5), evaluation (§6), related work (§7), discussion and limitations (§8), conclusion. The five research questions (RQ1–RQ4) in §6 map cleanly to the contribution claims.
- **5.2** Tables and figures are effective — Table 1 (oracle candidates and the residual) clearly maps why each classical oracle fails to reach documentation-implementation defects. Table 2 (Qdrant version reachability) is simple but communicates the bidirectional probe design. Table 3 (yield per VDBMS) is straightforward. Table 4 (cross-model judging vs. source-grounded on 18 clauses) is the densest but still readable, with TI markers and clear totals.
- **5.3 [minor, fixable]** Minor language issues — see §6, RQ2, where the sentence "On a controlled retrospective over 48 maintainer-adjudicated candidates (27 true-positive, 21 by-design/rejected; Milvus 32, Qdrant 16), the contract-grounded dev-reviewer with a 3-run any-confirmed ensemble reaches 65% accuracy, 67% precision... against a single-LLM baseline (no source-grounded anchor) of 48%/56%/37%" is information-dense and could be split for readability. This is a presentational nit, not a substantive problem.

### Questions for Authors
- **Q1:** Could the RQ2 precision/recall figures be more clearly qualified as estimates from a small adjudicated subsample? — see 3.2; clarifying that 67% precision and 74% recall are from 48 candidates (Milvus 32, Qdrant 16) and may not generalize beyond these two vendors would address the concern that these are population-level statistics.
- **Q2:** Is the RQ3 documentation-style correlation presented as a falsifiable prediction or an observed pattern? — see 3.3; the paper currently presents the optional-default vs. explicit-bound contrast as a "falsifiable prediction" in the RQ3 paragraph but hedges it as correlative in §8. Clarifying whether this is positioned as a prediction to be tested in future work or as an empirical observation from the current data would help readers understand the intended status of this claim.


---

## Meta-Review (Round 8)

**Paper:** TestVDB — Source-grounded falsification for VDBMS documentation-implementation consistency.
**Paper type:** Technical. **Reviewers:** 3 independent (Domain Expert / Area Specialist / Generalist), each verified by an independent checker (1 round; R3 CLEAN, R1/R2 patched). Key change since Round 7: RQ2 now reports a full majority-vote operating point (precision 64%, recall 26%) alongside the union, with explicit justification for choosing union.

### Criterion Consensus

| Criterion | R1 (Domain) | R2 (Area) | R3 (General) | Consensus |
|---|---|---|---|---|
| 1. Significance | Adequate | Adequate | Adequate | Adequate |
| 2. Soundness | Adequate | Adequate | Adequate | Adequate |
| 3. Novelty | Adequate | Adequate | Adequate | Adequate |
| 4. Verifiability | Adequate | Adequate | Excellent | Adequate |
| 5. Presentation | Adequate | Adequate | Excellent | Adequate |
| **Recommendation** | **Weak Accept** | **Weak Accept** | **Accept** | **Accept** |

### Meta Recommendation

**ACCEPT**

Per the rubric gate: no consensus substance criterion sits at Weak or Poor (Significance/Soundness/Novelty all consensus Adequate). Two reviewers individually vote Weak Accept and one Accept; the gate-level verdict is Accept because no consensus criterion drops below Adequate. Confidence is comparable to Round 7 (which was also gate-Accept with two Weak-Accept votes) — R3 moved from Weak Accept (R7) to Accept (R8), while R1/R2 held at Weak Accept.

**Round 7 → Round 8 shift.** The Round 7 top priority — report the full majority-vote operating point and justify the union choice — **landed**. R1's Soundness item on the ensemble (R7 3.1, then [major, fixable]) is now rated [minor, fixable] in R8: the data (union 67%/74% vs majority 64%/26%) does support the union choice; the residual ask is an optional fuller operating-characteristic analysis (precision-recall curve), not a missing justification. R2's sample-size concern (originally flagged [major, unfixable]) was re-grounded on check to [minor, fixable] — the paper already scopes statistical claims to Milvus/Qdrant. So the ensemble thread is effectively closed at "minor / optional."

**Convergence.** All three agree the two-layer error decomposition and source-grounded-falsification delta over MASTOR are the paper's real contributions, and that the RQ3 within-vendor contrast (optional-default over-strict vs explicit-bound not) is a strong falsifiable finding.

**Divergence / new items.** R1 raises a MASTOR-framing gap (acknowledge MASTOR as prior source-grounded oracle generation; sharpen the delta to source-as-falsifier direction) and wants the behavior-TI (11/11) elevated over the pooled rate (17/29) as the RQ3 headline. R2 wants a mechanistic explanation of the 15–78% single-run variance and a random-sample κ supplement. R3 (Accept) raises no blocking items.

### Priority Revisions (non-blocking, camera-ready)

**Framing (highest leverage — would lift Novelty toward Excellent):**
1. **[R1 2.2, Q2]** Acknowledge MASTOR as prior source-grounded oracle generation and sharpen the novelty delta to the *asymmetric direction* (source as falsifier of doc-derived claims, not source-grounding per se). One-sentence Related Work fix.
2. **[R1 2.4, Q3]** In RQ3, lead with the behavior-TI finding (11/11) and the parameter-TI finding (6/18) separately; present the pooled 17/29 only as an aggregate. Currently the pooled rate reads as the headline.
3. **[R1 1.2, Q4]** Scope the §9 generalization claim ("any system with natural-language documentation") to VDBMSs and structurally similar systems until empirical transfer evidence exists.

**Optional deeper analysis (would lift Soundness toward Excellent — now minor since data already supports the union):**
4. **[R1 3.3, Q1]** Add a precision-recall curve or an error analysis of which true positives majority voting specifically kills. The reported operating points already justify union over majority; this would make the operating characteristic fully transparent.
5. **[R2 3.5, Q2]** Add a mechanistic note on the single-run variance source (LLM sampling stochasticity vs attack-agent diversity vs source-interpretation differences).
6. **[R2 3.4, Q3]** Bound the κ=1.0 claim to the purposive 20-candidate sample explicitly, or add a small random-sample supplement.

**Presentation (cosmetic):**
7. [R1 4.3] Replace "on the order of $10^4$ calls, ~$10 per target" with a per-stage cost table.
8. [R1 5.2] Standardize "COSINE" vs "cosine" notation.
9. [R2 5.2] Restructure the dense RQ2 paragraph (union headline first, majority-vote as sensitivity comparison).

**Suppressed since Round 7 (resolved):** the ensemble-rule justification is now data-backed (both operating points reported); the sample-size concern is re-scoped (paper already limits claims to Milvus/Qdrant). The residual items above are framing and optional-analysis polish.
