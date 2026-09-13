## Reviewer 1: Domain Expert

**Overall Recommendation:** Accept

### Summary

The paper targets documentation-implementation inconsistencies in vector database management
systems: cases where a VDBMS silently accepts an input or exhibits behavior that contradicts its
natural-language API documentation, a subset of the non-crashing bugs that a crash oracle cannot
reach by construction. The authors argue through a seven-row exclusion table that every
deterministic-oracle candidate anchors its expectation somewhere other than system-level,
untagged behavioral prose, and answer with TestVDB, a four-stage agentic pipeline: documentation
distillation into source-verified constraints, test generation by attack agents bound to
pre-registered strategies, sandboxed execution against a Docker-pinned instance with raw HTTP
logging, and a confirmation stage that splits evidence assembly (an evidence builder producing a
five-section evidence chain) from cross-examination (a chain auditor applying four mechanical
checks and four perspectives — contract, physical constraints, behavioral elegance, maintainer
cognition — with the implementation source as the falsification anchor). The confirmation
verdict is three-valued, with an explicit Human-Review channel.

The evidence comes in two layers. In an operational human–machine deployment across Milvus,
Qdrant and Weaviate, maintainers confirmed 51 of 81 adjudicated submissions as real bugs and
fixed 23 via merged PRs (Section 4.2); the paper discloses that this ledger is cumulative over
earlier mining rounds with author-side screening and submission in the loop. In a controlled
re-adjudication of that pool on rebuilt, audited evidence packs (Section 4.3), the contract-only
core suppresses 96.7% of the 30 adjudicated false positives at 0.157 recall of the 51 bugs; the
full stage reaches 0.765 recall at 0.700 suppression under a counting convention that treats
routed Human-Review cases as confirmed, against 0.588 at 0.867 for a flat single-prompt judge
reading the same materials; under forced verdicts the two judges are indistinguishable
(0.529 vs. 0.490), a hand-adjudicated joint judge-plus-human reading gives 0.647 recall at 0.917
precision, and a three-run re-run of the full-vs-flat pair on a second model family does not
separate (p=0.58). RQ3 runs VDBFuzz's complete released Qdrant template set against the version
on which the paper's Qdrant defects are live and reports that it reaches none of them, while a
hand-guided probe built on the paper's boundary reasoning reproduces VDBFuzz's integer-overflow
crash on v1.4.0.

### Core Strengths

- **S1:** A verified real-world yield — 51 maintainer-confirmed bugs and 23 merged fixes across
  three production VDBMSs — with the fixed set validated by classifying every fix PR's changed
  files rather than by assertion. — see 1.1, 1.2.
- **S2:** The oracle-exclusion analysis and the "anchor inversion" are a real delta: I checked the
  five closest works through the shared literature cache (summaries distilled from their full
  texts, plus the cached full text where a specific claim needed it) and none takes the
  documentation prose as ground with a non-LLM falsifier. — see 2.1, 2.2.
- **S3:** An unusually thorough self-audit and remediation of the paper's own evidence pipeline
  (pack audit → rebuild → protocol alignment → four named contamination channels, with the two
  that reached the judged materials remediated by re-adjudicating the affected cases), which is
  the reason the RQ2 numbers can be read at all. — see 3.1, 4.1.
- **S4:** RQ3 is a methodological contribution in its own right: the released baseline runner's
  counters are shown to be broken, a per-template liveness oracle is substituted, and the zero is
  bounded from two directions with file:line evidence. — see 1.3.
- **S5:** Statistical reporting hygiene, including explicit anti-claims (the recall-only
  comparison does not survive correction; the second backbone does not replicate the separation).
  — see 3.1.

### Core Weaknesses

- **W1:** The headline full-vs-flat separation is carried by the counting convention and by five
  additional false-positive confirmations; under recall-only scoring it does not survive
  correction, so the accuracy claim — as opposed to the escalation claim — is not established.
  — see 3.2, 3.6.
- **W2:** The joint judge-plus-human reading (0.647/0.917), one of the three readings quoted in
  the abstract, was produced by the authors themselves adjudicating their own system's routed
  cases, non-blind. — see 3.3.
- **W3:** The flat-judge baseline is a deliberately minimal single prompt; a "thorough flat"
  control that shares the full stage's material but not its perspective vocabulary is not run, so
  part of the measured structure effect could be prompt richness. — see 3.4.
- **W4:** Five of the 51 "true bugs" are outside the paper's stated target class by construction
  (the Result-Incorrectness family), yet they enter the RQ1 ledger, the RQ2 recall denominator,
  and the full stage's largest miss block, without a stratified in-class recall. — see 3.5.
- **W5:** Density: the abstract's third paragraph and Section 4.3 compress the entire evidential
  posture — three scoring conventions, five arms, two backbones — into a few very long passages,
  making it hard to see which number is the claim. — see 5.2.

### Detailed Assessment

1. **Significance** — Excellent
   - **1.1** The target class is well chosen and concretely motivated. Section 1 instantiates it
     with Milvus accepting `nprobe=0` with HTTP 200 against a documented `[1, 16384]` range
     (issue #49823), and Section 2.2 draws the consistency/correctness line explicitly (what the
     system accepts, errors on, returns, and how its state evolves, versus whether a returned
     result is right). This is the residual that the paper's cited testing roadmap names as the
     key open challenge, and the class matters in practice because these systems feed retrieval
     context into LLM applications where a silent wrong result is worse than a crash. The framing
     work here — separating the class from result correctness and showing why the standard oracle
     families structurally miss it — is a genuine contribution in its own right.
   - **1.2** The yield is externally validated rather than self-reported. Section 4.2 reports 51
     of 81 adjudicated submissions confirmed by maintainers and 23 fixed via merged PRs, and then
     validates actionability by classifying every merged fix PR by its changed files: all 23
     modify implementation code, 15 also add regression tests, none is documentation-only, and
     the classifier is sanity-checked against the reclassified candidate Qdrant #9149 (correctly
     identified as test-only). The acceptance-label tabulation (50 of 51 carry an official bug
     label) is a further independent signal. The disclosure that the ledger measures the
     human–machine pipeline (author screening and submission in the loop) bounds this item but
     does not erase it: the fixes are merged in production systems regardless of how candidates
     were filtered.
   - **1.3** RQ3 is the strongest single piece of comparative work in the paper. Section 4.4 runs
     VDBFuzz's complete released Qdrant template set — 205 templates, 50.8 minutes, 22,540
     mutations, 23,258 HTTP responses over 96 endpoint paths — against the same v1.18.0 instance
     where the paper's Qdrant defects are live, and reports zero anomalies. Before drawing
     anything from that zero, the authors show the released runner's own success/failure counters
     are uninformative (pointed at a dead port, it reports 100% success), substitute a
     per-template liveness oracle, and bound the zero from both directions. The conclusion is
     narrow and correctly drawn: on that configuration the crash class is not constructible. The
     reverse direction is honestly presented as a hand-guided probe that knew the overflow
     mechanism, not as an automated result.
   - **1.4 [minor, fixable]** The motivating claim that only 2 of the 51 maintainer-confirmed bugs
     produce a crash or panic (Section 1) is not accompanied by which two they are. Table 3's
     `Other` row shows Qdrant #9045 as "zero-length vector accepted, then panic on later search",
     which makes the reader work to reconcile the "silent majority" framing with the ledger.
     Naming the two (or pointing to the ledger field) would make the paper's central motivation
     checkable at a glance.

2. **Novelty** — Adequate
   - **2.1** The exclusion analysis and the anchor inversion are real, and they survive
     verification against the closest prior work. I read the five works the argument most rests
     on: SATORI (ASE 2025) derives unary oracles per response field from OpenAPI field metadata
     and its natural-language descriptions — response-side properties from schema-anchored prose;
     AGORA+ (TOSEM 2026) learns response invariants from observed traffic and cannot reach
     inputs the traffic did not exercise; MASTOR (arXiv 2026) grounds oracles in implementation
     source, and its own limitations state that it "cannot detect violations of intended
     requirements that are not reflected in code"; Metamon (LLM4Code 2025) captures behavior as
     generated test oracles and asks the same LLM family whether they agree with the documented
     specification, with no independent evidence source; CASCADE (FSE 2026) uses code regenerated
     from the same documentation as its falsifier, and its own residual false positives came from
     cases where the generated code and tests shared the documentation's underspecification.
     None of the five takes the prose as ground and uses the implementation only as falsifier.
     The paper's characterizations of all five matched their sources in every claim I checked,
     and the substantive claims of its Table 1 rows are accurate as written (the row-5 label is
     addressed separately at 5.4).
   - **2.2** The measured finding that the structured protocol's separation comes from the
     routing channel rather than forced-verdict accuracy (Section 4.3) is new to me as a
     quantified result in this literature: the confirmation-stage line (Metamon, CASCADE,
     MASTOR's ChallengerAgent) reports accuracy tradeoffs, not escalation behaviour. Reporting it
     against a flat judge on the same packs is a contribution even though it partially deflates
     the pipeline's own accuracy story — which the authors accept explicitly.
   - **2.3 [minor, fixable]** The delta is concentrated in one conceptual move. Every component —
     LLM prose-to-constraint extraction (RESTInfer, Doc2OracLL, nl2postcond), second-agent oracle
     review (MASTOR's ChallengerAgent), source grounding as a check (CASCADE, MASTOR) — has a
     close antecedent, which the paper itself concedes ("A generated oracle reviewed by a second
     LLM agent is therefore not new here"). Contribution 2 in Section 1 should therefore be
     positioned as *the anchor inversion plus the routing finding*, not as a new pipeline
     architecture; as written it opens with "A four-stage, multi-agent pipeline…", which invites
     a novelty judgment the paper would lose.
   - **2.4 [minor, fixable]** The abstract says "the constraint-inference line that does read
     prose stops at parameter-level declarations". The body is more careful — it names RESTInfer
     for parameter constraints *and* ICON for temporal call-sequence constraints, and states the
     granularity as "parameter/method" (Related Work) — but the abstract's compression understates
     the nearest miss on the claim that no prose-reading line goes above parameter level.
     Reword the abstract to match the body (e.g., "parameter- and method-level, including call-
     sequence, declarations"). Otherwise, Related-Work coverage is complete: I ran scoped
     coverage searches over the paper's area, deduplicated against its 60-entry bibliography, and
     found no genuinely related uncited work — the two closest uncited hits (Pandita et al. 2012
     on method-specification inference from NL, and DAInfer on aliasing specifications) sit inside
     the already-cited constraint-inference family and target a different constraint class
     (title-level check; provisional). All 60 bibliography entries are cited and all citations
     resolve.

3. **Soundness** — Adequate
   - **3.1** The measurement-integrity program is the paper's best methodological asset, and it is
     what makes the RQ2 numbers readable at all. The authors audited their own 81 shipped packs
     and found 43.3% of the 134 distinct (constraint, cited-page) pairs unsupported by the cited
     page, 32% of constraint rows addressing an unrelated endpoint, and four packs leaking
     assembler provenance notes; rebuilt the packs from version-pinned documentation (with all
     the arithmetic reconciling: 2,106 assembled rows → 674 surviving, 22 explicit / 652
     inferred-from-behavior, 21 packs with no surviving contract row); aligned the judging
     protocol with the deployed rules; and then audited the judgment side, finding four separate
     contamination channels: expectation-framing (measured and found absent from the rebuilt
     packs — zero expectation-framed sentences outside verbatim server responses, so no
     sanitization was applied and none was needed), observation leakage (the four assembler
     provenance notes, removed before re-adjudication), ten packs carrying embedded
     maintainer-cognition sections into arms forbidden to read them, and seven candidate-anchored
     entries in the cognition materials — the latter two remediated by removing the material and
     re-adjudicating the affected cases in every affected arm and run on both backbones. (The
     paragraph's fifth item, adjudication disagreement, is a different category: an irreducible
     divergence between two fallible arbiters, not a remediated contamination channel.) The
     statistical reporting is also disciplined:
     Wilson intervals for every rate, exact McNemar with a stated Holm family, a maximal-ten-test
     sensitivity for the flagship value, and anti-claims that most papers would not print (the
     recall-only comparison does not survive correction, Holm-adjusted 0.090; the second-family
     re-run of the full-vs-flat pair does not separate, p=0.58). I re-derived the Wilson
     intervals, the exact McNemar p-values and the Holm multipliers from the reported counts and
     found them internally consistent throughout.
   - **3.2 [major, fixable]** The paper's flagship separation is carried by the counting
     convention, and the metric it is measured on credits additional false-positive confirmations
     as successes. Section 4.3 reports the significant test on the *confirmed set* — "so a 'leak'
     counts as confirmed on both sides" — where the full stage's 48 vs. the flat judge's 34 is
     +9 true positives and +5 additional leakage; the true-positive-only exact McNemar on the 51
     bugs (11/2, raw p=0.0225) does not survive correction, and under forced verdicts the two
     judges are indistinguishable (0.529 vs. 0.490, p=0.34). The authors state this plainly, so
     the flaw is not concealment — it is that the automatable part of the contribution (does the
     structured protocol find more real bugs than a flat judge?) is not statistically
     established, while what is established is that the aggregation rule escalates more cases
     (19.8% vs. 8.6% routing). Repositioning is possible at revision cost: lead the abstract with
     the forced and joint readings, present the convention number as deployment-conditioned, and
     add the one missing statistic the reader wants (a correct-decisions or precision-constrained
     recall comparison). As written, the abstract's first result sentence still leads with the
     convention number, and a reader who stops there will over-read it.
   - **3.3 [major, fixable]** The joint reading — 0.647 recall / 0.917 precision, quoted in the
     abstract — rests on the authors playing the human-review role themselves: "the authors then
     adjudicated the routed cases of *both* arms against their pack materials only … playing the
     channel's designated human role (non-blind; disclosed)". They did the right things around it
     (the same rule for both arms, outcome distributions reported: 9 confirmed, 2
     material-insufficient, 4 rejected for the full stage; 7 upheld of 11 for the flat arm), but a
     headline number produced by an interested, non-blind party judging its own system's outputs
     is soft evidence. This is fixable by construction: an independent adjudicator, blind to arm
     identity, would either reproduce the split or move it — and either outcome would be
     informative.
   - **3.4 [minor, fixable]** The flat-judge baseline is a deliberately minimal prompt (Appendix
     B: "There is no prescribed analytical framework — no perspectives, no chain sections, no
     aggregation rule"). The paper's mitigation is real and partly convincing — both arms share
     the recall-driving red lines, the flat judge is told to use Human-Review when a case cannot
     be settled, and it reaches majority confirmation on 13 of the 16 objective-constraint-driven
     confirmations — but the two arms still differ in *prompt length and analytical instruction*,
     not only in "structure". A thorough flat control (same materials, a long prompt that walks
     the four checks as a checklist but produces a single verdict without the aggregation rule)
     would isolate the structural contribution the paper wants to claim.
   - **3.5 [minor, fixable]** Five of the 51 confirmed bugs are Result-Incorrectness
     (approximate `count` under-counting), which Section 4.2 explicitly places outside the
     assertion framework "by construction — no documented accuracy contract bounds approximate
     behavior", and which entered the ledger on maintainer adjudication alone. They are all in
     the RQ2 pool, where four of them form the full stage's largest miss block. Including the
     deployed pipeline's real outputs in the pool is defensible, but it means the measured recall
     mixes the target class with an out-of-class family that no arm can address through the
     framework; a stratified recall over the 46 in-class bugs would let the reader see what the
     stage achieves on what it targets. Relatedly, the reader is not told what route detected
     those five bugs at all.
   - **3.6 [minor, fixable]** Under the convention, convention-recall is mechanically
     forced-confirms plus routed cases: 12 of the full stage's 39 confirmations exist only
     because the aggregation rule routes them (they are majority-Human-Review cases that forced
     scoring excludes). So "routing is where the structure pays" is partly definitional: the
     protocol's routing branches raise the convention number by construction, and the paper's
     real defence is that the escalations are mostly justified once a human looks (9 of 15
     upheld). That defence is currently buried in a long paragraph; reporting routing propensity
     and conditional routing precision as first-class mechanism statistics would make the claim
     sharper and less vulnerable to the "you defined your way to a separation" reading.

4. **Verifiability** — Excellent
   - **4.1** The text is unusually complete for an agentic-pipeline paper: the four stages, the
     five generation gates, the pre-bound strategy registry semantics, the evidence-chain
     sections, the confirmation verdicts, the aggregation rule in full (Appendix A), both judging
     prompts (English renderings; the verbatim Chinese dispatch files are declared authoritative
     in the artifact), the collection protocol, the two senses of "false positive", and all three
     scoring conventions. Every rate in the paper is backed by a stated numerator and denominator
     in the tables, and the arithmetic I checked (rates, Wilson bounds, exact McNemar values,
     Holm multipliers, strata sums, the pack-rebuild counts) is internally consistent. The Data
     Availability section declares a replication package whose inventory covers everything the
     claims need: agent roles and the strategy-trigger registry, per-version knowledge bases and
     specifications, generated scripts with raw HTTP logs, one evidence chain per candidate, the
     submission ledger for all 130 submissions, the original and rebuilt packs with audit
     verdicts and per-case judge outputs for every arm and run, RQ3 per-template logs, and the
     analysis scripts. The link is declared with a specific project identifier; I could not
     confirm reachability from this review environment, which I do not hold against the paper.
   - **4.2 [minor, fixable]** One run accounting does not reconcile. Section 5 (Limitations) states that after
     removing the embedded cognition sections, the authors "re-adjudicated the ten cases in every
     affected arm and run — the three contract-core runs, the six source-only runs, and the four
     flat-judge runs, thirteen in total across both backbones". Under the accounting stated in
     Section 4.3 — "every configuration … in three independent runs", plus the second-family
     re-runs of "the full and flat arms … three runs each" and the second-family source-only arm,
     three runs — the cognition-forbidden arms alone have 3 (core) + 6 (source-only) + 6 (flat)
     = 15 runs, not 13, and "four flat-judge runs" has no identifiable referent. Either the
     enumeration is wrong or some runs were out of scope for a stated reason; the paper should
     reconcile the two counts, since this paragraph is precisely where it asks the reader to
     trust that contamination was fully remediated.

5. **Presentation** — Adequate
   - **5.1** The structure is sound and the paper is complete: Introduction, Background,
     Approach, Evaluation, Limitations, Related Work, Conclusion, plus the prompt appendix. Two
     choices deserve praise. First, one real bug (Qdrant #10369) is threaded through all four
     stages (Sections 3.2–3.5), which makes an abstract pipeline concrete. Second, the
     terminology is explicitly disambiguated where it matters — "false-positive candidate" versus
     the `False-Positive` verdict, "pack" versus "case" (Section 4.3) — which prevents most of
     the misreadings this kind of evaluation invites. Tables 4–6 carry explicit counting-
     convention notes in their captions, which is the right place for them.
   - **5.2 [minor, fixable]** The abstract is three paragraphs, with the deployment yield in the
     second and the full evidential stack compressed into the third: the 43.3% audit, three
     scoring readings of the same comparison, a Holm qualification, a second-backbone
     non-replication, and the RQ3 probe. The paper's actual claim is subtle enough that most
     readers will take away either "0.765 recall" or "indistinguishable", depending on where they
     stop. This is a comprehension problem, not a formatting nit — that third paragraph, Section
     4.3's flagship paragraph, and the joint-analysis paragraph each carry between five and ten
     distinct quantitative claims, and no one of them can be read without cross-referencing the
     others. Restructure the closing paragraph into claim-then-evidence sentences with the three
     readings named in one place, and let Section 4.3 carry the convention detail and the
     seven-test family footnote.
   - **5.3 [minor, fixable]** In the source I reviewed, the cross-reference in Section 5
     (Internal validity paragraph) reads "Section~ef{sec:eval}" — if this is not an artifact of
     the review pipeline's source stripping, it renders as a visible typo in the PDF and should
     be checked.
   - **5.4 [minor, fixable]** Table 1's row-5 label, "REST doc/spec-derived oracles (AGORA+,
     SATORI, MASTOR, MASTEST)", files MASTOR — a source-derived oracle, as the row's own text and
     the Related Work both say — under "doc/spec-derived". Relabel the row by mechanism
     ("structured-source oracles") so the row heading does not contradict its content.
   - **5.5 [minor, fixable]** Section 4.3's phrase "the structured protocol converts the cases
     both judges find unresolvable into explicit human-review decisions" is not accurate for the
     seven routed confirmations the flat judge force-closed as `False-Positive`: those were not
     cases the flat judge found unresolvable. Reword to "cases the flat judge closes rather than
     escalates".

### Questions for Authors

- **Q1:** Would the full-vs-flat separation survive on a metric that prices false-positive
  confirmations — e.g., confirmed true positives minus confirmed false positives, or recall at a
  precision floor? — [intended effect: if it survives, item 3.2's rating moves toward the stronger
  end because the separation would no longer depend on the convention's treatment of leaks; if it
  does not, 3.2 stands as written and the abstract's first result sentence should lead with the
  forced/joint readings.]
- **Q2:** Can the joint judge-plus-human reading (0.647/0.917) be reproduced by an adjudicator
  blind to arm identity — and ideally not one of the authors — working under the same
  pack-materials rule? — [intended effect: a reproduced split would move 3.3 up; a materially
  different split would tell the reader how much of the joint number is the adjudicator.]
- **Q3:** Was a "thorough flat" control considered — the same packs and source access, a long
  prompt that names the checks as a checklist (contract, objective constraints, intent evidence,
  cognition) but produces one verdict with no aggregation rule? — [intended effect: if the gap
  persists under that control, 3.4 becomes a non-issue and the structure claim strengthens; if
  not run, 3.4 remains and bounds the size of the claimed structure effect.]
- **Q4:** What is the full stage's recall on the 46 in-class bugs (excluding the five
  Result-Incorrectness bugs), and through which route were those five detected at all, given that
  no contract assertion covers them? — [intended effect: an in-class recall figure would move 3.5
  up; a route description would also clarify whether the ledger's 51 and the framework's target
  class are being deliberately conflated or merely pooled.]
- **Q5:** Which runs were affected by the third contamination channel, and how does "four
  flat-judge runs" reconcile with three runs per configuration per backbone? — [intended effect:
  resolving the count would move 4.2 off the list; leaving it unexplained keeps a
  remediation-accounting doubt in the one paragraph that asks the reader to trust the cleanup.]

---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Accept

### Summary

The paper targets documentation-implementation bugs in vector database management systems (VDBMSs): cases where the system silently accepts an input or returns a result that contradicts its prose API documentation, a subclass of the non-crashing logic bugs that crash-oracle fuzzers cannot reach. It argues structurally (Table 1, Section 2.3) that every deterministic-oracle family anchors its expectation somewhere other than system-level, untagged prose, leaving an LLM-derived oracle as the practical option, and instantiates TestVDB as a four-stage pipeline: documentation is distilled into source-verified constraints with pre-bound attack strategies (Sections 3.2–3.3), probes run against Docker-pinned targets (Section 3.4), and a bug-confirmation stage splits an evidence builder from a chain auditor that cross-examines a five-section evidence chain from four perspectives with the implementation source as the falsification anchor (Section 3.5).

Empirically, the paper reports a cumulative submission ledger across Milvus, Qdrant, and Weaviate (51 of 81 adjudicated submissions maintainer-confirmed, 23 fixed via merged PRs; Sections 4.1–4.2), then re-adjudicates that 81-candidate pool under an audited, rebuilt, version-pinned pack protocol with five judge configurations run three times each (Section 4.3). The contract core reaches 0.157 recall at 0.967 suppression; the structured full stage reaches 0.765 recall at 0.700 suppression versus 0.588 for a flat single-prompt judge, a difference that survives Holm correction only on the confirmed-set unit and is attributed by the paper's own decomposition to the human-review routing channel rather than forced-verdict accuracy; a second model family fails to replicate the full-vs-flat separation. Section 4.4 probes VDBFuzz bidirectionally on Qdrant, finding its released template set reaches none of the silent-accept defects on one instance, and reporting a hand-guided probe that reaches VDBFuzz's crash-class integer overflow on another.

### Core Strengths

- **S1:** An unusually self-critical measurement program for the confirmation stage: the paper audits its own evidence packs (43.3% of cited pairs unsupported), rebuilds them, aligns the judging protocol with the deployed rules, removes each further contamination channel it finds (provenance notes, embedded cognition sections, candidate-anchored cognition entries) with re-adjudication of every affected run, and reports three scoring conventions plus a second backbone, including negative results. — see 3.1, 3.4
- **S2:** Novelty positioning within the LLM-oracle / documentation-consistency literature is accurate and verifiable: I read the four closest named competitors (SATORI, MASTOR, Metamon, CASCADE) in their cached full texts and AGORA+ via its cached summary, and every characterization the paper makes survives, including the "anchor inversion" delta over MASTOR. — see 2.1, 2.2, 2.4
- **S3:** A real-world yield with actionability evidence: 51 maintainer-confirmed bugs, 23 merged fixes, a fix-nature classifier validated against the one disproved candidate, and an eight-pattern taxonomy whose acceptance family covers 72.5% of the corpus. — see 1.1, 1.2
- **S4:** The RQ3 comparison is bounded honestly: after showing the released runner's success/failure counters are uninformative (a dead-port run reports 100% success), the paper substitutes a per-template liveness oracle, measures what its own run actually did, and states only the narrower conclusion its configuration supports. — see 3.2
- **S5:** Strong verifiability ammunition: a declared replication package with per-case judge outputs for every arm and run, both judging prompts rendered in Appendix A, and an internal arithmetic that coheres across the abstract, prose, and all five tables. — see 4.1, 3.3

### Core Weaknesses

- **W1:** The headline yield is not attributable to the pipeline configuration the rest of the paper describes and evaluates: the 81-candidate ledger "predates the run reported here, which contributed none of the 81" and spans "earlier pipeline generations whose per-generation configuration we do not itemize," so no experiment in the paper shows the Section 3 configuration (or its confirmation stage) producing any of the 51 bugs. — see 3.5, 1.3
- **W2:** The flagship full-vs-flat separation is carried by the counting convention that treats Human-Review (and leaked false positives) as confirmations; the recall-only comparison does not survive correction, forced verdicts are indistinguishable, and the second-family re-run does not separate. The paper discloses each of these, but the "structure pays" claim needs a net-benefit statistic and sharper positioning. — see 3.4, 1.4
- **W3:** Ground-truth construction details are left partly implicit: the reclassified Qdrant #9149 is never placed in a current ledger column, the 81-pool is an author-screened subset with no deterministic submission rule, and the joint judge-plus-human reading relies on a non-blind human pass played by the authors. — see 3.6
- **W4:** Perspective B's seven "objective" violation classes were codified from the same mining experience that produced the pool, drive 16 of the full stage's 39 confirmations, and have no measured false-positive behavior outside this pool; the flat judge admits no symmetric exclusion. — see 3.7
- **W5:** Presentation: the source contains one broken cross-reference ("Section~ ef{sec:eval}" in Limitations), and the paper's density — an abstract whose third paragraph packs the pack audit, the three scoring conventions, the Holm-corrected statistics, and the second-family result into roughly 260 words, alongside several statistics-stacked body paragraphs — makes the decisive numbers hard to locate on first reading. — see 5.2, 5.3, 5.4

### Detailed Assessment

1. **Significance** — Excellent
   - **1.1** The paper establishes the target class concretely in Sections 1 and 2.1: silent, wrong-result failures that keep the service up, illustrated by Milvus accepting `nprobe=0` with HTTP 200 against documentation declaring `[1, 16384]` (issue #49823), and quantified against its own ledger ("only 2 of the 51 maintainer-confirmed bugs produce a crash or panic"). This is exactly the failure shape the cited VDBMS bug study reports as dominant, and the paper shows the one dedicated VDBMS fuzzer is crash-oracle by construction — so the problem is real, unsolved by the existing tool, and worth solving.
   - **1.2** The empirical yield is clear practical impact: 51 maintainer-confirmed real bugs across three production systems with 23 merged fixes, plus an acceptance-signal breakdown (50/51 carry an official bug label; 25/29 Milvus `triage/accepted`). The fix-nature classification (all 23 fixed bugs modify implementation code, 15 add regression tests, none documentation-only) and its validation against the disproved #9149 (the classifier flags that PR as test-only, matching the seven-version re-probe) make report inflation an unlikely explanation. The eight-pattern taxonomy in Section 4.2 gives the field a citable corpus description.
   - **1.3 [minor, fixable]** The impact is real but its attribution is looser than the framing suggests (see also 3.5): the ledger is cumulative across mining rounds and versions, the 81-pool is a submission-filtered subset of the pipeline's own confirmed output with author-side screening and no deterministic submission rule, and 49 further submissions are excluded from every rate. The paper states each of these, but a reader cannot connect any of the 51 bugs to the Section 3 configuration. A per-generation provenance table would let the significance claim land on the described system.
   - **1.4 [minor, fixable]** The significance of the paper's own methodological innovation is narrower than its contribution list foregrounds: by the paper's own decomposition, the structured confirmation protocol's advantage over a flat prompt with the same materials and red lines is the routing channel (forced verdicts 0.529 vs. 0.490, $p{=}0.34$), and the measured gain does not replicate on a second family. The paper says this explicitly; the residual task is to state the system-level takeaway (escalation rather than accuracy, with its human cost) as the contribution, not as a caveat.

2. **Novelty** — Adequate
   - **2.1** The paper's core novelty claim — that the constraint-inference and REST-oracle literature anchors expectations in signals, structured sources, or method-/parameter-level prose, leaving system-level untagged behavioral prose unoccupied (Table 1) — holds against the works I verified. Within my specialty (LLM-derived oracles from documentation and documentation-implementation consistency), I checked the five closest named competitors — four in their cached full texts (SATORI, MASTOR, Metamon, CASCADE) and AGORA+ via its cached summary — each with a verdict. SATORI [verified]: per-response-field oracles from OpenAPI field name/type/description/examples, unary and response-side only, with real bugs that are documentation-vs-response mismatches — does not touch input acceptance or state, as the paper says. AGORA+ [verified via its cached summary]: response-field invariants induced from observed request/response traffic — cannot reach inputs the traffic did not exercise, as the paper says. MASTOR [verified]: oracles grounded in source-verified fields, OAS claims absent from source demoted to `pending` — its authority is the implementation. Metamon [verified]: method-level Javadoc checked against EvoSuite-captured behavior, with the LLM itself as judge and no non-LLM evidence source. CASCADE [verified]: method-level documentation checked with tests and a regenerated implementation both derived from the same documentation — an LLM artifact as falsifier. None occupies the system-level-prose position.
   - **2.2** The specific delta claims survive relational verification. "MASTOR's authority is the implementation, whereas TestVDB takes the prose as ground and uses the implementation only as the falsifier" is accurate and is in fact MASTOR's own stated limitation ("It cannot detect violations of intended requirements that are not reflected in code"). The concession that "a generated oracle reviewed by a second LLM agent is therefore not new here, and cross-request behavioural oracles are not unique to TestVDB" matches MASTOR's ChallengerAgent and multi-operation oracle paths exactly, and the paper's citations of Metamon (precision 0.722 at recall 0.480 on 9,482 pairs) and CASCADE (both residual false positives arose from "the generated code and tests made the same false assumption over something underspecified in the documentation") are verbatim-accurate against those texts.
   - **2.3 [minor, unfixable]** The originality is real but incremental at the mechanism level: every component — LLM extraction from prose, source grounding, second-agent review, cross-operation oracles — is present in a named prior system, and no named competitor performs the same task, so the delta is argued structurally (Table 1) rather than measured against a comparable baseline. The contribution is a deliberately chosen design inversion (prose as expectation ground, implementation as falsifier) applied to a domain no prior logic-bug work targets. The paper is honest about this; the tier reflects the size of the delta, not a misstatement.
   - **2.4** Related-Work coverage within my specialty is dense and accurate, and no missing citing opportunity surfaced. Scoped searches for LLM-oracle generation from documentation, doc-implementation inconsistency detection, API constraint inference, DBMS/VDBMS fuzzing, and VDBMS bug studies returned no genuinely related uncited work; the one plausible hit (multi-agent REST-API testing with semantic graphs, ICSE 2025) turned out to be GentaREST, already cited as `\cite{gentarest25}`.

3. **Soundness** — Adequate
   - **3.1** The RQ2 measurement program is, in places, better than the standard of the field: the Layer-0 audit found 43.3% of 134 distinct (constraint, page) pairs unsupported and attributed every defect to the assembler; the rebuilt packs (674 surviving rows of 2,106, typed 22 explicit vs. 652 inferred) and protocol alignment are documented step by step; three contamination channels (four provenance notes, ten packs with embedded cognition sections, seven candidate-anchored cognition entries) were removed with re-adjudication of every affected arm and run (13 core/source-only/flat runs for the cognition sections; all affected runs on both backbones for the candidate-anchored entries); and a mechanical scan confirmed zero expectation framing outside verbatim server responses. The one complete-run funnel (Section 4.2) and the stratification of recall by evidence availability (0.784 / 0.667 / 0.727 under the convention; 0.649 / 0.000 / 0.273 forced) let a reader see where each arm's recall comes from.
   - **3.2** The RQ3 comparison is executed and bounded with unusual care. The paper first shows that VDBFuzz's released runner's success/failure counters cannot be trusted (one failure marker is emitted by no code path; the other mismatches the templates' actual messages; a dead-port run reports exit 0 and 100% success), then substitutes a per-template liveness oracle, runs the full 205-template Qdrant set with the time limit removed (22,540 mutations; 23,258 HTTP responses over 96 paths; zero anomalies), and draws only the conclusion its released configuration supports — locating the bounds it can measure (per the paper's inspection of the released code: integer boundary set topping at 65,536; dimension candidates at 10,000; the 2^62 overflow threshold) and disclosing that the reverse direction is a hand-guided probe chosen with knowledge of VDBFuzz's published case study. RQ3's claims are stated no more strongly than the evidence.
   - **3.3** Internal numerical consistency is high, which materially supports the paper's claims. I cross-checked the abstract against the body and the tables: 48 vs. 34 confirmed sets = 16−2 discordant = +9 true positives (11/2) +5 leakage (5/0); the stratification products (0.784×37 + 0.667×3 + 0.727×11 = 39; 0.649×37 + 0 + 0.273×11 = 27; joint 26+1+6 = 33) reproduce the arm totals exactly; the RQ3 response ledger sums correctly (14,022+7,520+1,512+204 = 23,258); the Holm multipliers implied by the footnote (flagship fourth-smallest ×4 → 0.0052; raw 0.041 sixth-smallest ×2 → 0.083) match the reported adjusted values; and the largest-family sensitivity (0.0092) is consistent with a ×7 multiplier. This coherence is a strong verifiability signal (see 4.3).
   - **3.4 [minor, fixable]** The paper's central comparison survives correction only on a statistic that mixes precision and recall: the McNemar unit is the "confirmed set," under which the full stage's 9 leaked false positives and the flat judge's 4 count as successes, and the paper itself decomposes the net +14 into +9 true positives and +5 additional false-positive confirmations, notes that the recall-only comparison does not survive correction (Holm-adjusted 0.090), that forced verdicts are indistinguishable, and that the second-family re-run does not separate ($p{=}0.58$). All disclosed — but the headline "structure is a measured mechanism" needs a net-benefit statistic (TP−FP, $F_1$, or Youden) reported alongside, so the reader can see whether the structure is beneficial once leakage is priced; and the contribution wording should lead with routing-not-accuracy.
   - **3.5 [major, fixable]** The paper's two halves do not meet: RQ1's 51-bug yield comes from ledger entries that "predate the run reported here, which contributed none of the 81" and span "earlier pipeline generations whose per-generation configuration we do not itemize," while the Section 3 pipeline description (pre-bound strategies, five generation gates, the Human-Review channel) is what RQ2 re-adjudicates on frozen packs. The one complete end-to-end funnel the paper reports (Qdrant v1.18.0; 96 candidates, 60 defect-confirming, five registrations) was "recorded under that run's pre-review protocol, whose verdict vocabulary predates the Human-Review channel." As written, no reader or reviewer can identify which configuration produced any particular one of the 51 bugs, or reproduce the run that found them. This is disclosed, not hidden, but for a system paper it leaves the core system claim unanchored; a per-generation provenance mapping (or an explicit rescoping of RQ1 to "the operational pipeline across its generations") is needed.
   - **3.6 [minor, fixable]** Ground-truth construction is described at a high level but not fully: Qdrant #9149 is "disproved by our own seven-version re-probe" and "reclassified," yet the paper never states which column it now occupies (the ledger's Qdrant row is 28 adjudicated = 14 confirmed + 14 false positives, so it must be somewhere); the 81-pool is an author-screened subset with no deterministic submission rule (disclosed); and the joint judge-plus-human reading (0.647/0.917) rests on the authors adjudicating both arms' routed cases "non-blind; disclosed." The third point is inherent to the setting, but the first is a one-line fix that would let a reader reconstruct the pool exactly.
   - **3.7 [minor, fixable]** Perspective B's seven objective constraint classes are the largest single driver of the measured recall (16 of 39 confirmations; excluding them drops recall to 0.451), and the paper discloses that they were "codified from the same mining experience that produced the evaluated pool" and admits no symmetric exclusion for the flat judge. The ef/nprobe carve-out analysis (no verdict flips; four true bugs confirmed on the absence of sentinel semantics) is a good self-check but covers one class only. Without any measurement of the classes' behavior on candidates outside this pool (e.g., the 49 unadjudicated submissions or the 32-candidate anchor set), the external validity of the objective-constraint principle — the claim that "a limit parameter accepting zero is an objective violation even if no contract row states a bound" — rests on this pool alone.

4. **Verifiability** — Adequate
   - **4.1** The Data Availability statement declares a replication package whose inventory covers every claim: agent role definitions and the strategy-trigger registry, per-version knowledge bases and specifications, all scripts with raw HTTP logs, one evidence chain per candidate, the submission ledger, original and rebuilt RQ2 packs with pack-audit verdict records and per-case judge outputs for every arm and run, RQ3 baseline reports with per-template logs, and analysis scripts to recompute every rate and test. Appendix A reproduces both judging prompts and discloses the deliberate asymmetry (the full stage legitimately reads cognition materials). For RQ2 and RQ3 this is enough to follow and check the work.
   - **4.2 [minor, fixable]** I could not confirm the declared link resolves publicly: my headless probe of `https://anonymous.4open.science/r/TestVDB_artifact-EC36/` redirects to the service's API endpoint and returns HTTP 401 — but calibration shows the same 401 for a nonexistent slug, so the probe is uninformative rather than evidence of a dead link. The authors should verify the link in a browser before submission. Separately, text-only replication of stages (i)–(iii) is limited: the extraction/generation prompts live only in the artifact ("agent role definitions"), and the paper describes the JSON schemas but not the prompts themselves, so the text alone cannot reproduce the extraction or generation stages.
   - **4.3** The text is fully self-limited in its definitions: "false-positive candidate" vs. the `False-Positive` verdict, "candidate/case/pack/leak," and the three scoring conventions (forced, joint judge-plus-human, convention) are defined before use and used consistently; the scoring tables and prose agree throughout (see 3.3). This is exactly what a reader needs to check the paper's own claims, and it is done well.

5. **Presentation** — Adequate
   - **5.1** The structure is sound and the heavy tables are well captioned: Table 1's oracle-exclusion analysis is the clearest statement of the paper's intellectual core, the ablation and arm tables are self-describing, and the running example (#10369) threads the pipeline legibly through all four stages.
   - **5.2 [minor, fixable]** The source contains a broken cross-reference in the Limitations section: the text reads "every number in Section~" and then, on the next source line, "ef{sec:eval}" where `\ref{sec:eval}` was intended (Section 5, internal-validity paragraph). Every other `\ref` in the file I read is intact and no comment/`\iffalse` residue is present, so this is a single corrupted reference in the source; it will render as literal "efsec:eval" text. The authors should repair it.
   - **5.3 [minor, fixable]** Density is the main readability cost. The abstract runs about 490 words across three paragraphs, and its third paragraph (roughly 260 words) alone carries the pack audit, the three scoring conventions, the Holm-corrected statistics, the second-family result, and the VDBFuzz probe; several body paragraphs stack eight or more statistics (the decomposition paragraph and the backbone-replication paragraph in Section 4.3 are the worst). Leading the dense paragraph with a one-sentence result shape, leaving the convention detail to Section 4.3, would let a reader locate the decisive numbers on first pass.
   - **5.4 [minor, fixable]** Naming could be unified: the arms are "core/full/source-only/flat/source-only-Qwen" while the text also speaks of "Layer 0/1/2" for the measurement layers and "convention/forced/joint" for scorings; the second-family model is called "Qwen3.8-Flash" in prose but "source-only-Qwen" in the tables. Small unifying edits (one naming table, or consistent arm labels) would remove the recurring re-orientation.

### Questions for Authors

- **Q1:** Can you map each of the 51 confirmed bugs to the pipeline generation/configuration that produced it — or state explicitly that the records are insufficient? — [from 3.5; if itemized or if RQ1 is rescoped to "the operational pipeline across generations," item 3.5's [major] tag would drop to minor and Soundness would rise.]
- **Q2:** What is the full-vs-flat comparison on a net-benefit statistic (TP−FP, $F_1$, or Youden) on both backbones? — [from 3.4; if the net-benefit also favors the full stage, my convention-dependence concern would shrink; if it is null, the contribution statement in Section 1 should be amended accordingly.]
- **Q3:** Where does Qdrant #9149 sit in the current 81-case ledger (false positive, or excluded), and does the RQ2 ground truth therefore include author-side overrides of maintainer adjudication? — [from 3.6; a one-sentence clarification plus a line in the ledger description would let a reader reconstruct the pool and would raise 3.6.]
- **Q4:** Has perspective B's objective-constraint principle been applied to candidates outside this pool (the 49 unadjudicated submissions or the 32-candidate anchor set), and what is its false-positive rate there? — [from 3.7; an out-of-pool estimate would answer the co-evolution concern directly; its absence keeps 3.7 at minor.]
- **Q5:** Does the artifact pin the stage (i)–(iii) prompts and the per-generation configuration of the reported Qdrant run, and does the declared anonymous link resolve for external readers? — [from 4.2; a positive answer would move Verifiability from Adequate toward Excellent.]

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Accept

### Summary

The paper targets *documentation-implementation bugs* in vector database management systems (VDBMSs): cases where a system silently accepts an input or behaves in a way that violates its natural-language API documentation (a canonical instance is Milvus accepting `nprobe=0` although the docs state $[1,16384]$; the running example carried through the four pipeline stages is Qdrant `#10369`). The paper first argues structurally, in Table 1 (`tab:exclusion`), that each standard oracle family anchors its expectation in something other than system-level prose---crash signals, other implementations, output relations, machine-checkable properties, or structured specs---so an LLM-derived oracle is the practical option for this residual, which imports the LLM's false-positive problem. It then presents TestVDB, a four-stage pipeline: documentation distilled into source-verified specifications; attack agents bound to a pre-registered strategy registry that emit executable probes; sandboxed execution against a Docker-pinned version with raw HTTP logging; and a confirmation stage that splits evidence assembly from cross-examination, grounding verdicts in a five-section evidence chain (document, behavior, source) audited from four perspectives, with a three-valued verdict that includes explicit human review.

The evaluation has two layers. On the operational side (Section 4.2, Table 2), a cumulative submission ledger across Milvus, Qdrant, and Weaviate reports 51 maintainer-confirmed bugs and 23 merged fixes out of 81 adjudicated submissions (30 false positives), with a taxonomy of eight bug patterns. On the measurement side (Section 4.3), all 81 candidates' frozen evidence packages were audited, found to contain substantial unsupported citations (43.3% of distinct constraint/page pairs), rebuilt against version-pinned documentation, and re-adjudicated three times per configuration by five judge arms; the paper reports the confirmation stage under three scoring readings (forced verdicts, a hand-adjudicated joint judge-plus-human reading, and a deployment counting convention), a Holm-corrected full-versus-flat-judge comparison on the primary backbone, a second-backbone replication that does not separate the pair, and a bidirectional reach comparison with the VDBFuzz crash oracle.

### Core Strengths

- **S1:** A concrete, auditable real-world yield: 51 maintainer-confirmed bugs and 23 merged fixes across three production VDBMSs, with the per-case ledger, taxonomy, and fix classification shipped in the artifact (Table 2, Table 3, Section 4.2). — see 1.2
- **S2:** An unusually rigorous and self-auditing measurement design for RQ2: audit, rebuild, protocol alignment; five arms in three runs each; Wilson intervals; exact McNemar with a pre-declared test family and Holm correction; three scoring readings; a second backbone; and a named, remediated contamination audit (Section 4.3, Section 5). — see 3.1, 3.3
- **S3:** Strong claim discipline: every headline number carries its qualifier, and the paper reports its own negative results (forced-verdict collapse, second-family non-replication, failure of the recall-only correction, the hand-guided nature of the RQ3 reverse probe) rather than burying them (Sections 4.3, 5). — see 3.2
- **S4:** Verifiability in the strong sense: the artifact's contents are enumerated, both judging prompts are reproduced in Appendix A, and the reported statistics close arithmetically from the text---I re-derived the paired-test $p$-values, the Wilson intervals I spot-checked, the Holm multipliers, the stratified recalls, the pack-row arithmetic, and the RQ3 response counts. — see 4.1, 4.2
- **S5:** The oracle-exclusion analysis (Table 1) is a legible, transferable account of *where* an LLM oracle is forced for prose-defined behavior---useful well beyond the three systems studied. — see 1.4, 2.1

### Core Weaknesses

- **W1:** The paper's flagship comparison is thinner than its framing suggests: the full-versus-flat separation is carried by the human-routing channel (forced verdicts 0.529 vs. 0.490, $p{=}0.34$), five of the fourteen net cases are additional false-positive confirmations, the recall-only test does not survive correction, the full stage does not separate from its own source-only component ($p{=}0.39$), and the pair does not separate on a second model family ($p{=}0.58$). All of this is disclosed, but the reader must assemble it across several passages in Sections 1, 4.3, and 5. — see 3.4, 3.5
- **W2:** Density and legibility: the abstract compresses three scoring readings, two Holm corrections, and a non-replication into one paragraph, and several body sentences are parse-broken on first read, so a non-specialist cannot easily locate the headline claim. — see 5.2, 5.3
- **W3:** Small internal accounting snags a reproducing reader will hit: the printed Holm-adjusted 0.090 does not follow from the stated test family; "four flat-judge runs" is hard to reconcile with the flat arm's six runs across two backbones; and two enumerations do not close on their counts. — see 4.3, 4.4, 5.6
- **W4:** Novelty is incremental relative to the paper's own named closest works, and the paper's new *mechanism* (the four-perspective evidence chain) is not shown to add over its own single-step source-forensics arm. — see 2.2, 3.5
- **W5:** The 51/23 impact figure cannot be attributed to the reported configuration: the reported run postdates the pool and contributed none of the 81, and the pool spans un-itemized earlier generations. — see 1.3

### Detailed Assessment

1. **Significance** — Excellent
   - **1.1** The problem is established concretely and early: Section 1 ties silent VDBMS misbehavior to retrieval-augmented applications (a disabled filter returns all matches; a dropped partition hides data), and Section 2.1 grounds the "non-crashing majority" claim in cited empirical studies. The `nprobe=0` example is a clean, checkable instance, and the running `#10369` example is carried through all four pipeline stages (Sections 3.2--3.5). For a reader outside the field, the paper makes the stakes legible.
   - **1.2** The yield is the strongest evidence of impact: Table 2 reports 51 confirmed of 81 adjudicated submissions, 23 fixed via merged PRs, with fix-nature validation (all 23 modify implementation code, none documentation-only, Section 4.2) and a pattern taxonomy (Table 3) whose dominant family---Silent-Accept, Type-Coercion, Silent-Ignore at 37/51---is exactly the class the paper set out to reach. Real bugs fixed in production systems are the clearest form of practical impact this kind of work can show.
   - **1.3 [minor, fixable]** The ledger's attribution is limited: Table 2's caption and Section 4.3 state that "the reported GLM-5.3-Flash run postdates the pool and contributed none of the 81", and Section 5 concedes the yield "measures the human--machine pipeline, not the automated stage's end-to-end precision or recall". The paper could report the reported configuration's *own* adjudicated yield as a separate number---the 32-candidate anchor in Section 4.3 comes close, but it was measured on original packs under the pre-audit protocol, so it does not answer the question. This bounds how the 51/23 figure can be cited.
   - **1.4** The exclusion analysis (Table 1) is a contribution in its own right: it classifies each oracle family by where its expectation comes from and locates the residual precisely ("system-level, untagged behavioral prose"). Even a non-specialist can follow and reuse the argument, and it frames the whole paper.

2. **Novelty** — Adequate (provisional: I did not fetch the cited competitors; this assessment rests on the paper's own characterizations)
   - **2.1** The paper states its delta against named close works with specific differences (Section 6): Metamon keeps an LLM question as its falsifier---the self-reference TestVDB breaks; CASCADE cross-checks tests against code generated from the same documentation, sharing its ambiguity; MASTOR grounds oracles in source (implementation as authority), whereas TestVDB "inverts the roles"---prose as ground, implementation as falsifier. The paper is candid that generated oracles reviewed by second agents and cross-request behavioral oracles are not new; the anchor inversion is a real, articulable difference.
   - **2.2 [minor, fixable]** The originality is a stance (anchor inversion) plus engineering (evidence chain, three-valued routing, strategy registry) rather than a new mechanism class: each component has precedent in the works the paper itself cites, and the paper's own source-only arm---which contains the inversion's core, source forensics---does not separate from the full protocol ($p{=}0.39$, Section 4.3). A source-access ablation on the full stage (or an explicit demonstration that removing source grounding re-introduces the self-reference problem the paper describes) would make the delta measurable rather than positional. This is a reformulation task, not a new experiment necessarily.

3. **Soundness** — Excellent
   - **3.1** The RQ2 measurement design is the most rigorous part of the paper (Section 4.3): a three-layer correction (audit of shipped packs; rebuild from version-pinned documentation; protocol alignment with deployed auditor rules), five judge arms over the full 81-candidate pool in three independent runs each, majority reduction, Wilson intervals, exact McNemar tests with a pre-declared seven-pair family and Holm correction, three scoring readings reported side by side, and a maximal ten-test sensitivity bound (0.0092). The RQ3 baseline receives the same care: the released runner's success/failure counters are shown to be uninformative (100% reported success against a dead port), and a liveness-based per-template oracle is substituted with the substitution argued and bounded.
   - **3.2** Claim discipline is exemplary for the genre: the second-family full-versus-flat pair "separate[s] not at all" ($p{=}0.58$); the forced-verdict reading collapses the comparison to 0.529 vs. 0.490; the recall-only correction does not survive (Holm-adjusted 0.090); the RQ3 reverse direction is explicitly "a hand-executed probe", with the probe value chosen knowing the overflow mechanism and the measured bound that the released integer set tops out at 65,536. The paper's scoping sentences ("a measured mechanism on the primary backbone, not a law of the protocol") match what the evidence supports.
   - **3.3** Ground-truth and contamination handling is honest and specific (Section 5): the `#9149` reclassification, expectation-framing scan (19 hits, all inside verbatim server responses), four provenance notes removed, ten embedded cognition sections re-adjudicated, and seven candidate-anchored cognition entries removed with affected cells re-run---each with counts and with the pre-cleanup verdict files shipped. A reader can see exactly which threats were measured and which remain irreducible (adjudication disagreement, protocol--pool co-evolution).
   - **3.4 [minor, fixable]** The counting-convention language overstates at one point: Section 4.3 justifies it as "the study counts a case the way the deployment resolves it", but the deployment resolves routed cases by human adjudication, and the paper's own joint pass confirms only 9 of 15 routed confirmations (4 rejected, 2 returned); the paper later says the convention "overstates the joint system". Calling the convention an upper model of the routing channel would remove the tension between the definition and the paper's own three-reading result.
   - **3.5 [minor, fixable]** Section 4.3 reports that full-versus-source-only is indistinguishable ($p{=}0.39$; discordant 8/4), noting the test is underpowered at this pool size. This bound belongs next to contribution 2: it says the four-perspective apparatus is not shown to add recall over its own single-step source-forensics component on this pool, only over the flat judge. As written, this important null sits in the middle of a long paragraph.
   - **3.6 [minor, fixable]** Table 1's rows 2--6 are "argued from each family's anchoring mechanism" rather than exercised, as the caption states, yet the Introduction and abstract make universal claims ("every deterministic-oracle candidate falls structurally short"; "no deterministic-oracle family derives its expectation from that behavioral prose"). The argument is plausible and well-constructed, but the quantifier outruns the evidence shown. Either exercise one non-crash family (e.g., a metamorphic or property-based tool on the same instance) or soften to "the families we analyzed".
   - **3.7 [minor, fixable]** The "returned" (material-insufficient) cases are counted asymmetrically: on the false-positive side, a returned case "is never adjudicated a false positive, so it still counts as intercepted" (Section 4.3, giving joint suppression 27/30), while on the true-positive side returned cases do not count toward the joint recall of 33/51 (Table 6). Both choices are disclosed, but stating the alternative (e.g., a returned case as unresolved under both metrics, or counting it as intercepted on both) would let a reader see how sensitive 0.900/0.647 are to this convention.
   - **3.8 [minor, fixable]** The cognition-access asymmetry sentence in Section 4.3 is self-tensioned: it says the asymmetry "contributes to none of the separation beyond one already-disclosed case", then locates its signal "before the candidate-anchored entries were removed". State one way or the other, post-cleanup, whether any of the 16-versus-2 discordant cases in the flagship pair depends on the full stage's privileged cognition access.
   - **3.9 [minor, fixable]** Appendix A's aggregation is written as a cascade ("Otherwise (A=Neutral): B=Confirmed $\Rightarrow$ Confirmed; D=Supports-Defect $\Rightarrow$ Confirmed; ...; C=Refuted (explicit by-design) $\Rightarrow$ False-Positive"), but nothing declares the list to be priority-ordered. Read as a cascade, a maintainer-cognition support hit would confirm a case even where the source carries verbatim by-design intent evidence---which the body's summary ("an explicit by-design refutes", Section 3.5) and the C-perspective clause ("only an \emph{explicit} by-design may refute") read the other way. Since 2 of the 39 confirmations are cognition-driven, the tie-breaking rule should be stated explicitly.

4. **Verifiability** — Excellent
   - **4.1** The Data Availability section enumerates the artifact (agent role definitions and the strategy-trigger registry, per-version knowledge bases and specifications, generated scripts with raw HTTP logs, one evidence chain per candidate, the submission ledger, original and rebuilt packs with audit records, per-case judge outputs for every arm and run, RQ3 per-template logs, and analysis scripts that "recompute every rate, interval, and paired test reported here"). Appendix A reproduces both judging prompts, with the caveat that the Chinese originals in the artifact are authoritative. Even without the artifact, the text alone is enough to follow how the evidence was produced.
   - **4.2** The internal accounting closes. I re-derived, from the text alone: every per-row and total sum in Tables 2, 4, 5, and 6 against the 51 true bugs / 30 false positives / 81 candidates; the exact McNemar $p$-values from the stated discordant splits (16/2$\to$0.0013, 11/2$\to$0.0225, 8/2$\to$0.11, 7/3$\to$0.34, 8/5$\to$0.58, 5/0$\to$0.0625, 15/3$\to$0.0075, 15/5$\to$0.041, 8/4$\to$0.39); the Holm multipliers 4 and 3 for the fourth- and fifth-smallest of the seven paired tests, including the maximal-ten-test bound of 0.0092; the Wilson intervals I spot-checked (39/51, 8/51, 29/30, 19/32, 37/51, 30/51); the stratified recalls, which reconstruct the marginal totals exactly (29+2+8 $=$ 39 convention; 24+0+3 $=$ 27 forced; 26+1+6 $=$ 33 joint); the pack-rebuild arithmetic (2,106$-$674$-$463 $=$ 969; 969$-$302 $=$ 667; 667$+$7 $=$ 674; 22$+$652 $=$ 674); and the RQ3 status counts (14,022$+$7,520$+$1,512$+$204 $=$ 23,258). This level of internal closure is rare and materially raises confidence in the numbers I cannot check.
   - **4.3 [minor, fixable]** The one statistic that does not reproduce from its stated method is the recall-only correction: the printed "Holm-adjusted 0.090" for raw $p{=}0.0225$ implies multiplier 4, which is the rank the flagship pair occupies in the seven-test family, whereas inserting the recall-only test into that family gives rank 6 of 8 (multiplier 3, adjusted 0.0675; larger still under the maximal ten-test set). The qualitative conclusion---does not survive---is unchanged under every multiplier. Please state the rank convention used.
   - **4.4 [minor, fixable]** Section 5 says the embedded-cognition channel was re-adjudicated across "the three contract-core runs, the six source-only runs, and the four flat-judge runs, thirteen in total", but Section 4.3 describes the flat arm running three times on each of two backbones (six runs), which would make fifteen. One of the two counts is wrong, or "affected" is narrowed by a rule that is not stated; either way the clean-pool claim is worth reconciling.

5. **Presentation** — Adequate
   - **5.1** The structure is conventional and complete (Introduction, Background, Approach, Evaluation, Limitations, Related Work, Conclusion, Appendix), all cross-referenced tables and sections exist, and the running example threaded through stages i--iv is the paper's best comprehension aid. The limitations section is unusually well organized by validity type.
   - **5.2 [minor, fixable]** The abstract is overloaded: it carries all three scoring readings, two Holm-corrected comparisons, a non-replication, and a complementarity result in one block, so the headline number is not findable. Leading with one reading (and moving the rest to Section 1 or 4.3) would make the contribution legible to the "capable reader who is not pre-loaded with this niche".
   - **5.3 [minor, fixable]** Several sentences are parse-broken on first read and should be split: the "That separation survives Holm correction on the confirmed-set unit---the statistic the deployment resolves, though five of its fourteen net cases are additional false-positive confirmations, and the recall-only comparison does not survive (Holm-adjusted 0.090)" construction (Section 1), and the single sentence running from "Over the 81 paired cases..." through the discordant/tie accounting (Section 4.3).
   - **5.4 [minor, fixable]** The cross-reference in the Limitations paragraph is broken in the source as given: line 367 ends "every number in Section~" and line 368 begins "ef{sec:eval}", so it would typeset as "Section ef{sec:eval}". If the comment-stripping pass ate the `\ref`, disregard this item; otherwise it is a broken reference to fix. (No other stripping artifacts are present: no line comments or `\iffalse`/`comment` markers survive.)
   - **5.5 [minor, fixable]** Naming and phrasing nits: Table 6's caption says "the flat stage" where the arm is called the "flat judge" everywhere else, and the relationship between the reported run and the ledger is phrased three different ways ("contributing to it additively rather than being contained in it", Section 4.2; "contributes to the ledger additively", Section 4.3; "contributed none of the 81", Table 2 caption and Introduction). One canonical sentence would prevent a reader from thinking the 81 came from the reported run.
   - **5.6 [minor, fixable]** Two enumerations do not close on their counts: Section 4.3 lists five rejection reasons ("a self-consistent behavior record, a distorted premise, a descriptive-only assertion, a missing documentation anchor, or an explicit in-source by-design comment") for "4 were rejected on the materials alone"; and the same paragraph says "21 packs carry no surviving contract row ... 14 of the 51 true bugs sit in these packs", while the strata below describe the 3 weak-evidence packs as retaining "a single surviving row". One clause each would reconcile both.

### Questions for Authors

- **Q1:** Can you report the reported configuration's own adjudicated submission yield as a separate number (the reported run's registrations are tracked; four were excluded from the 32-candidate anchor, Section 4.3)? — [intended effect: answered, item 1.3 could be dropped and the significance claim (criterion 1) sharpened from "a pipeline family across generations" to "the reported configuration".]
- **Q2:** What family and ranking convention produced the recall-only Holm-adjusted value of 0.090? — [intended effect: resolving it would turn item 4.3 from a reproducibility snag into a stated convention; the qualitative conclusion is unchanged either way.]
- **Q3:** Please reconcile the "four flat-judge runs" re-adjudicated for the embedded-cognition channel with the flat arm's three-runs-per-backbone description (six runs across two backbones, Section 4.3). — [intended effect: removes the only place where the clean-pool claim cannot be reproduced from the text; item 4.4.]
- **Q4:** After the cognition-anchor cleanup, does the full stage's privileged cognition access affect any of the 16-versus-2 discordant cases in the flagship pair? The current sentence ("contributes to none of the separation beyond one already-disclosed case ... before the candidate-anchored entries were removed") reads both ways. — [intended effect: if yes, the flagship paragraph needs that disclosure; if no, deleting the clause settles item 3.8.]
- **Q5:** In Appendix A's fixed aggregation, is the listed order a priority order? If so, a `D=Supports-Defect` hit would confirm a case even where `C=Refuted` carries verbatim by-design intent evidence, which the body's summary ("an explicit by-design refutes", Section 3.5) reads the other way. — [intended effect: pins protocol determinism where 2 of the 39 confirmations originate; item 3.9.]

---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Excellent | Excellent | Excellent | **Excellent** |
| Novelty | Adequate | Adequate | Adequate | **Adequate** |
| Soundness | Adequate | Adequate | Excellent | **Adequate** |
| Verifiability | Excellent | Adequate | Excellent | **Excellent** |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Accept** | **Accept** | **Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three reviewers recommended Accept, so the unanimous shortcut decides
outright. No criterion sits at consensus Poor or at consensus Weak; Significance
reaches consensus Excellent (all three), and Verifiability reaches consensus
Excellent on the strength of a declared artifact manifest plus a text whose
arithmetic closes: all three reviewers independently re-derived the exact
McNemar values, Wilson intervals, Holm multipliers, stratified-recall sums,
pack-rebuild arithmetic and RQ3 response counts from the text alone and
reproduced them, and R2 additionally cross-checked the abstract against the body
and every table.

The three reviews converge on the same residual concern, and it is a framing
concern rather than an evidential one. All three independently judge that the
automatable part of contribution 2 is not yet statistically established: the
significant full-vs-flat test runs on the confirmed-set unit, under which five
of the fourteen net cases are additional false-positive confirmations (R1 3.2,
R2 3.4, R3 W1); the recall-only comparison does not survive correction
(Holm-adjusted 0.090); forced verdicts are indistinguishable (0.529 vs. 0.490,
p=0.34); and the pair does not separate on the second family (p=0.58). What the
evidence does establish — that the aggregation rule escalates rather than
force-closes, and that the escalations are mostly justified once a human looks —
is the escalation claim, not an accuracy claim. R1 and R2 also both observe that
the flat comparator is a deliberately minimal single prompt, so part of the
measured structure effect could be prompt richness rather than structure
(R1 3.4), and R2 asks for the one statistic that would settle it: a net-benefit
metric on which leakage is priced (R2 Q2, R1 Q1).

Two further [major, fixable] items sit on attribution rather than on
measurement. R2 3.5 and R1 1.2 both find that the 51-bug yield cannot be
connected to the configuration the paper describes and evaluates — the ledger
predates the reported run, which contributed none of the 81, and spans
generations whose per-generation configuration is not itemized. R1 3.3 notes
that the joint judge-plus-human reading, one of the three headline numbers, was
produced by the authors adjudicating their own system's routed cases non-blind.
Neither is concealed; both are disclosed in the body, and the reviewers say so.
They are the items that keep Soundness at consensus Adequate rather than
Excellent.

Presentation remains the weakest consensus tier, and for the second round
running the reason is the same: the decisive numbers are hard to locate. Both R1
and R2 rate the abstract's density as a comprehension problem rather than a
formatting nit — three reviewers across two rounds have now independently had to
assemble the paper's actual claim from three separate passages. Notably, all
three reviewers in this round independently flagged the same broken
cross-reference in the Limitations paragraph (`Section~ef{sec:eval}`), which
confirms the value of shipping a source whose references resolve.

### Priority Revisions
1. **Add a net-benefit statistic to the flagship comparison (R2 3.4, R2 Q2,
   R1 Q1).** TP−FP, F
   $1$, or Youden's $J$ alongside the confirmed-set test would let the reader see
   whether the structure still pays once leakage is priced. This is the single
   highest-value addition: it either converts the convention-dependence objection
   into a supporting result or bounds the claim honestly.
2. **Reposition the contribution as escalation, not accuracy (R1 3.2, R2 1.4,
   R3 W1).** The paper already states "routing, not forced accuracy, is where the
   structure pays"; the abstract and contribution 2 should lead with that, with
   the convention number presented as deployment-conditioned rather than as the
   first result sentence.
3. **Anchor RQ1 to the evaluated configuration or rescope it (R2 3.5, R1 1.2).**
   Either a per-generation provenance mapping or an explicit rescoping of RQ1 to
   "the operational pipeline across its generations" would close the gap between
   the paper's two halves.
4. **State the joint reading's provenance limit where the number appears
   (R1 3.3).** The non-blind, author-played adjudication is disclosed in the
   paragraph but not attached to the 0.647/0.917 figure itself, which is quoted
   in the abstract.
5. **Fix the two labeling defects (R1 5.4, R1 5.5).** Table 1's row-5 heading
   files MASTOR under "doc/spec-derived" while the row's own cell calls it a
   "source-derived oracle"; and §4.3 says the protocol "converts the cases both
   judges find unresolvable", which is not true of the seven routed confirmations
   the flat judge force-closed.
6. **Reconcile the run accounting the reviewers could not follow (R1 4.2,
   R2 4.2, R3 Q3).** Both R1 and R2 flagged the "four flat-judge runs" in the
   thirteen-run cleanup as having no identifiable referent. The paper's count is
   correct (the affected runs are the three contract-core, six source-only, and
   four flat runs), but the paragraph should say why the flat arm's other two
   runs are not in it.
7. **Presentation and precision** (all `[minor, fixable]`): name the two
   crash-producing bugs behind the "silent majority" framing (R1 1.4); state
   which ledger column the reclassified Qdrant #9149 occupies (R2 3.6); pin
   Appendix A's aggregation as priority-ordered or not, since 2 of the 39
   confirmations are cognition-driven (R3 3.9); state one rule for returned cases
   on both sides of the joint reading (R3 3.7); narrow the universal quantifiers
   on Table 1 rows 2--6 or exercise one non-crash family (R3 3.6); reconcile the
   two enumerations that do not close on their counts (R3 5.6); unify the arm
   naming so "Qwen3.8-Flash" and "source-only-Qwen" read as one arm (R2 5.4); and
   split the abstract's third paragraph (R1 5.2, R2 5.3, R3 5.2).

Divergences worth noting. R3 rates Soundness Excellent where R1 and R2 rate it
Adequate, and the difference is the unit of judgment: R3 credits the measurement
program and the internal closure of the numbers, while R1 and R2 judge the
criterion against the claim the framing makes. R1 and R2 also both propose new
controls (a thorough-flat prompt; an independent blind adjudicator) that R3 does
not request — a difference of what each treats as fixable within a revision.
These are emphases, not contradictions: all three agree on what the evidence
shows and on the direction the framing should move.
