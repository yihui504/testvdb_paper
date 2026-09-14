## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary

The paper targets *documentation-implementation bugs* in vector database management systems:
cases where the system silently accepts an input or behaves in a way that contradicts its
own API prose — a documented `nprobe` range of `[1, 16384]` while `nprobe=0` returns
HTTP 200 — with no crash and no error code. It argues that this residual is out of reach of
every deterministic oracle family, because each anchors its expectation somewhere other than
system-level untagged prose (crash signals, another implementation, output relations,
machine-checkable properties, structured specs), and that an LLM reading the prose is
therefore the practical oracle — which imports the LLM's false-positive problem. The
proposed system, TestVDB, is a four-stage pipeline: prose→constraint extraction with source
verification, strategy-bound probe generation, sandboxed execution against a Docker-pinned
version, and a confirmation stage that splits evidence assembly from cross-examination,
where an evidence builder assembles a five-section chain and a chain auditor applies four
mechanical checks and four perspectives (contract, physical constraints, behavioral
elegance, maintainer cognition). Verdicts are three-valued — Confirmed, False-Positive, or
Human-Review — and a fixed aggregation rule routes anything unsettled to the human channel
rather than closing it.

The evaluation has three parts. RQ1 reports a maintainer-adjudicated ledger accumulated over
sixteen per-version mining campaigns: 81 adjudicated submissions across Milvus, Qdrant and
Weaviate, 51 confirmed as real bugs and 23 fixed via merged PRs. RQ2 audits the frozen
evidence packages that fed the confirmation stage, finds 43.3% of their cited (constraint,
page) pairs unsupported by the pages they cite, rebuilds all 81 packs from version-pinned
documentation, and re-adjudicates the pool three times per configuration across nine judge
arms. It reports the results under three scoring conventions side by side: forced verdicts
(0.529 for the full stage vs 0.490 for a flat single-prompt judge), a hand-adjudicated
joint judge-plus-human reading (0.647, with an independent adjudicator reaching 0.588), and
a deployment counting convention that treats routed cases as confirmed (0.765 at 0.700
suppression vs 0.588). Decomposing the protocol shows adding the aggregation rule to the
flat judge reproduces the full stage's recall exactly, while the four perspectives without
the aggregation are indistinguishable from a flat judge; withholding the implementation
source raises recall to 0.941 and lowers suppression to 0.467. RQ3 runs VDBFuzz's released
Qdrant template set to completion against the same instance and reports that it reaches none
of the confirmed defects, plus a hand-guided reverse probe that reaches VDBFuzz's own
integer-overflow crash on an older release.

### Core Strengths

- **S1:** A verified, third-party-adjudicated defect yield on live production systems: 51
  maintainer-confirmed bugs and 23 merged fixes across three VDBMSs, with a fix-nature
  classifier showing every merged fix touches implementation code and none is
  documentation-only — see 1.1, 4.1.
- **S2:** The paper audits its own measurement instrument, finds it 43.3% unsupported,
  rebuilds it, and ships the audit verdicts — with the row arithmetic given. Self-found
  instrument failure, fully disclosed, is the strongest methodological move in the paper —
  see 3.1.
- **S3:** A completed 2×2 over {four perspectives} × {aggregation rule}, plus source-withheld
  and second-backbone arms, converts the mechanism claim from an inference into a
  measurement — and the authors report it against their own design, concluding that the
  routing rule rather than the cross-examination organization carries the separation — see
  2.2, 2.3.
- **S4:** The novelty deltas against the closest prior work are real and independently
  checkable: MASTOR's own stated limitation confirms the claimed anchor inversion, and every
  checkable characterization of VDBFuzz is exact — see 2.1, 2.4.
- **S5:** Statistical reporting that includes the tests that fail: recall-only Holm-adjusted
  0.090, flagship against the repaired flat dispatch adjusted 0.098, second-backbone
  p=0.58, and a full family-definition arithmetic with robustness to larger families — see
  3.2.

### Core Weaknesses

- **W1:** Stages (i)–(iii) of the pipeline are held constant across all nine judge arms and
  are never ablated, so the evaluation cannot say what the prose→constraint extraction,
  source verification, strategy binding and sandbox buy over handing a judge the raw
  documentation and raw HTTP logs — even though the paper's headline conclusion is that the
  last stage's structure is inert — see 1.3.
- **W2:** The headline separation is measured against a flat dispatch the authors themselves
  show was mis-specified; against the repaired baseline the flagship does not survive
  correction, yet the abstract and contribution list still quote the unrepaired 0.588 — see
  3.5.
- **W3:** The two cells that carry the central causal claim are built by editing dispatches
  that are neither quoted nor inside the declared artifact inventory — see 3.4, 4.3.
- **W4:** The RQ1 ledger and the RQ2 pool both predate the configuration the paper describes,
  which contributed none of the 81 and has no maintainer-adjudicated output of its own — see
  1.4.
- **W5:** Missing related work: the multi-agent LLM-as-judge literature (nearest hit
  "Judging with Many Minds", EMNLP Findings 2025) is uncited, although the Introduction's
  shared-ambiguity argument and the measured negative on the four-perspective panel are
  instances of that line's findings — see 2.5.

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The strongest single asset is the ledger in §4.2 and Table 2. Of 81 adjudicated
     submissions across Milvus (43), Qdrant (28) and Weaviate (10), maintainers confirmed 51
     and merged fixing PRs for 23; the paper then validates the fix count rather than
     asserting it — every merged fix PR is classified by changed files, all 23 modify
     implementation code, 15 also add regression tests, none is documentation-only, and
     applying the same classifier to the disproved #9149 correctly identifies that PR as
     test-only, matching the authors' own seven-version re-probe. It also reports the
     acceptance signals the projects actually attach (50/51 carry an official `bug` label;
     25/29 Milvus `triage/accepted`; 5/14 Qdrant `accepted`) instead of inventing a severity
     scale. This is real impact on a real problem, established by maintainers rather than by
     the authors.
   - **1.2** The problem framing in §1 and §2.2 is well drawn. Separating *consistency* from
     *correctness* — "what it accepts, what it errors on, what it returns, and how its state
     evolves" versus ANN recall or ranking — gives the paper a claim it can defend and
     explicitly disclaims the one it cannot. Table 1 then organizes the oracle families by a
     single criterion, *where each family anchors its expectation*, which is a more useful
     axis than the usual taxonomy of techniques, and the paper labels rows 2–7 as argued
     rather than exercised ("argued from each family's anchoring mechanism rather than
     exercised"), and explains why its own objective-constraint catalogue appears as row 7
     even though it is a component rather than a competitor. Domain readers will recognize
     the residue this describes.
   - **1.3 [major, fixable]** The evaluation ablates one stage of a four-stage pipeline. All
     nine arms of tables 4–5 read the same rebuilt structured packs; seven of the nine also
     read the same pinned source clones (the two exceptions are the contract core, which is
     described as having "no source access" at all, and "full, no source," whose clone is
     removed and whose source channel is closed); the extraction stage, the source-verification step,
     the strategy-trigger registry and the sandbox are held constant throughout, and no arm
     varies pack *quality*. The nearest thing is the contract-core arm, which reads only the
     pack's contract assertions and reaches 0.157 recall / 0.967 suppression — but the core
     also reads the pack, so it isolates the *evidence chain*, not the pack. This matters
     more now than it would have before revision: because the paper's own decomposition
     concludes that the confirmation stage's structure is inert and the aggregation rule does
     the work, a reader is entitled to ask what the specification extraction, source
     verification and pre-bound strategies contribute — and the paper has no measurement to
     offer. The comparison the community will want (flat judge over raw vendor documentation
     plus raw HTTP logs) is missing.
   - **1.4 [major, unfixable]** The system that produced the ledger is not the system the
     paper specifies. §4.3 and §5 state that all 81 adjudicated submissions originate from
     GLM-5.2 mining rounds (February–August 2026), that the pipeline as described runs on
     GLM-5.3-Flash (September 2026), and that "the reported GLM-5.3-Flash run postdates the
     pool and contributes to the ledger additively" — contributing none of the 81. The
     51-bug yield is therefore the cumulative output of sixteen differently-configured
     campaigns, which the paper says plainly ("the ledger is the sum of sixteen per-version
     campaigns rather than one configuration's output"), and the described configuration's
     only end-to-end ledger (§4.2, "Process ledger of one complete run": 119 chain verdicts →
     96 candidates → 60 defects → 5 registrations) has no maintainer adjudication at all. No
     revision can produce new maintainer verdicts on the new run's submissions within a
     review cycle, so the gap between "the system specified" and "the system that found the
     bugs" is structural. It is disclosed repeatedly and honestly — including in the abstract
     — which is why this is a ceiling on the significance claim rather than a soundness
     failure, but the ceiling is real: the paper cannot state that the artifact it describes
     achieves the yield it reports.
   - **1.5 [minor, fixable]** RQ3 carries less than its share of the paper's weight. The
     systematic direction is an absence whose *reason* the paper concedes is close to
     definitional — "a crash oracle cannot fire on a non-crashing accept by construction" —
     and the reverse direction is explicitly not an automated run: the v1.4.0 confirmation is
     "a hand-executed probe of that boundary-value class," whose "probe value was chosen with
     knowledge of the overflow mechanism from VDBFuzz's own published case study," and the
     authors "did not measure whether TestVDB's automated boundary strategy would generate a
     value in the failing range unaided." Strip those away and the remainder is a genuine but
     narrow finding about VDBFuzz's released configuration (its mutation space tops out at
     65,536 and its dimension candidates at 10,000, so the class its own paper crashed on is
     not constructible from the released templates). The structural complementarity claim is
     sound; the empirical head-to-head adds little beyond it, and §5 should say so where it
     currently reports RQ3 as a contribution.

2. **Novelty** — Adequate
   - **2.1** I checked the delta against **MASTOR** (fetched; cache stem
     `mastor a multi agent approach to semantic test oracle generation for restful apis (corr 2026)`,
     arXiv preprint), which the paper calls the closest work. The paper's characterization is
     accurate on every point I could verify: MASTOR's two-phase design grounds oracles in a
     transitive source closure; a ChallengerAgent does review each path and trigger one
     targeted regeneration; it does generate behavioural-consistency oracles over
     cross-operation association types; and — the load-bearing claim — OAS-declared items not
     substantiated in source are placed in `pending` fields and "oracle-generation agents
     read only the source-verified fields," so the doc-versus-source discrepancy signal it
     records is never turned into an oracle. The paper is also *more* generous than it needs
     to be in crediting that signal at all. Decisively, MASTOR's own §7.4.2 states the
     limitation the paper claims: "MASTOR infers semantics from implementation behavior. It
     cannot detect violations of intended requirements that are not reflected in code." The
     anchor inversion — prose as ground, implementation admissible only as falsifier — is a
     real, non-obvious delta over the closest prior work.
   - **2.2** The evaluation resource is a contribution the paper does not claim. An
     81-case pool (51 maintainer-confirmed bugs, 30 maintainer-adjudicated false positives)
     drawn from production systems, with an audited and rebuilt evidence pack per case, and a
     nine-arm × three-run blind judge benchmark over it, is the artifact most likely to
     outlive this paper, and the completed 2×2 makes it reusable for exactly the question
     ("does judge structure help?") that the paper answers negatively. I did not find this
     claimed anywhere in the contribution list; §Data Availability describes it as
     replication material rather than as a benchmark. I confine my claim to what I verified
     in the paper and its artifact declaration — I did not run a field-wide census of
     comparable adjudicated judge benchmarks — so I state this as an under-claim by the
     authors rather than as a verified first.
   - **2.3** The mechanism finding is new and, to my reading, unclaimed elsewhere: three
     structurally very different configurations — the full stage, the aggregation-only
     control, and the perspective-only arm — reach *exactly* 27/51 under forced-verdict
     scoring (Table 6), and differ only in how often they decline to decide (routing 19.8%,
     28.4%, and less, §4.3). The companion result is equally unusual: withholding the
     implementation source from the full stage *raises* recall from 0.765 to 0.941 and cuts
     suppression from 0.700 to 0.467, so the source channel costs nine adjudicated true bugs
     and refuses seven adjudicated false positives, and the authors state plainly that "the
     aggregate credit for the benchmark belongs to the cheaper configuration, not to the one
     this paper contributes." Papers rarely report that removing their own headline mechanism
     improves the summary metrics, and the structural explanation is convincing: in the fixed
     aggregation the source-anchored perspective can only refute, so it appears in no clause
     that confirms.
   - **2.4** The other three verified deltas hold. **VDBFuzz** (fetched; cache stem
     `vdbfuzz understanding and detecting crash bugs in vector database management systems (ieee acm international conference on software engineering icse 2026)`)
     is characterized accurately in every checkable particular: "13 crash vulnerabilities plus
     six runtime exceptions" matches its abstract; it is three-stage with template-based input
     mutation and API sequence mutation, and the fragment the paper quotes from it — that its
     sequence stage aims at "logical inconsistencies or invalid state transitions" — is exact;
     the fuller sentence that fragment comes from, which the paper does *not* quote ("mutating
     API call sequences to uncover defects caused by logical inconsistencies or invalid state
     transitions," in VDBFuzz's §1 Introduction), also matches the competitor, and I verified it
     in the cached full text rather than taking the paper's word for the paraphrase; the
     120-minutes-per-tool-per-VDBMS protocol is its own; the released
     Qdrant template set is 205 templates per its `generation_summary.json`; the head-to-head
     revision `7a41449` matches the clone I inspected; exactly three released Qdrant templates
     issue `wait=false` upserts, as claimed; and the mutation bounds the paper cites by
     file:line (`vdbfuzz/keywords/__init__.py:292` tops out at 65,536; `vdbfuzz/mutator.py`
     dimension candidates top out at 10,000) are exact — I read both. **Metamon** (fetched)
     is correctly used: precision 0.722 at recall 0.480 on 9,482 pairs, verbatim, and
     correctly disqualified as a head-to-head baseline because its ground truth is
     mutant-injected incorrect oracles at method level in Java, not maintainer adjudication.
     **CASCADE** (fetched) is characterized accurately, and the quoted explanation of its two
     residual false positives — "the generated code and tests made the same false assumption
     over something underspecified in the documentation" — is verbatim.
   - **2.5 [minor, fixable]** Missing related work. **Ma et al., "Judging with Many Minds: Do
     More Perspectives Mean Less Prejudice? On Bias Amplification and Resistance in
     Multi-Agent Based LLM-as-Judge"** (Findings of EMNLP 2025, pp. 17356–17392, DOI
     10.18653/V1/2025.FINDINGS-EMNLP.941) studies position, verbosity, chain-of-thought and
     bandwagon bias across multi-agent debate and LLM-as-meta-judge frameworks and finds that
     debate *amplifies* bias after the initial round and that the amplification persists,
     while meta-judge resists it. That is the nearest empirical precedent for two of this
     paper's load-bearing assertions: the Introduction's claim that "a multi-perspective
     panel does not fix this: every judge reads the same ambiguous documentation, so the
     ambiguity is shared, not broken," and §4.3's measured negative on the four-perspective
     organization. §6's judge-reliability paragraph cites Zheng, Panickssery, Wataoka,
     Haldar, Bodicoat and Molinelli but no multi-agent-judge work at all — the one literature
     whose whole subject is whether adding perspectives to an LLM judge helps. Citing it
     costs the paper no novelty (it *supports* the premise) and materially strengthens it;
     the same paragraph is the natural home for one or two more of that line. I resolved this
     at abstract level rather than by a full read, and I state its findings as the source
     reports them.
   - **2.6 [minor, fixable]** One competitor characterization overreaches. §6 ends the
     LogicHunter discussion (cache stem
     `logichunter testing llm agent frameworks with an agentic oracle (acm sigsoft international symposium on software testing and analysis issta 2026)`,
     fetched: ISSTA 2026; "40 previously unknown bugs, 30 confirmed and 26 fixed"; ReAct
     oracle with `code_search`, `doc_search` and sandboxed `run_code`) with "ours does not let
     the implementation arbitrate at all, admitting it only to falsify the claim already read
     from the prose." The first clause contradicts its own qualifier — admitting the
     implementation *to falsify* is one-directional arbitration — and it contradicts the
     paper's own §4.3, where the source channel "casts 41 explicit by-design refutations and
     59 weak ones" and "is the mechanism that refuses them," and §3.5, where
     `by_design_in_source` drives verdicts. The paper states the accurate version elsewhere
     ("in the fixed aggregation the source-anchored perspective can only refute"), so this is
     a wording fix in a novelty-bearing sentence, not a conceptual error. The rest of the
     LogicHunter characterization is accurate, including the report counts.

3. **Soundness** — Adequate
   - **3.1** The measurement design in §4.3 is exemplary in a way that is rare. Layer 0
     reports that an audit of the originally assembled 81 packs — the instrument that
     produced the paper's own prior reported numbers — found 43.3% of their 134 distinct
     (constraint, cited-page) pairs unsupported by the page, a further two over-strong, 32% of
     constraint rows addressing an unrelated endpoint, and four packs whose assembler
     provenance notes leaked adjudication-adjacent annotations. Layer 1 rebuilds all 81 packs
     from version-pinned documentation and the tested version's own OpenAPI artifact and gives
     the row arithmetic: 674 rows survived out of 2,106 assembled (674 endpoint-filtered, 463
     removed by evidence verification, 969 survivors, 667 kept as rebuilt contract rows plus
     the 7 single assertion rows the archaeology packs retained = 674), typed as 22 `explicit`
     and 652 inferred-from-behavior. Layer 2 aligns the judging protocol with the deployed
     rules after finding that the first re-adjudication protocol still carried two
     pre-deployment rules that suppressed recall by construction. Finding and disclosing that
     your own instrument was 43% unsupported is the opposite of the usual failure mode, and
     the pack-audit verdict records are declared as shipped.
   - **3.2** The statistics are reported with the tests that fail, which is where most papers
     stop. Wilson intervals accompany every rate; the paired comparisons are exact McNemar on
     confirmed sets; the Holm family is defined explicitly, enumerated with raw p-values and
     discordant nets, and stress-tested at family sizes 7, 10 and 13 with the resulting
     adjusted values given (0.0052, 0.0066, 0.0105); and the paper states which results do not
     survive — recall-only Holm-adjusted 0.090, the flagship against the schema-repaired flat
     dispatch raw 0.049 → adjusted 0.098, and the second-backbone pair p=0.58. I re-derived
     the counts in tables 4–6 and in §4.3 and they reconcile: full-vs-flat confirmed sets
     48 vs 34, net +14, decomposed into +9 TP and +5 leakage, matching the discordant 16/2
     (true-positive-only 11/2, leakage-only 5/0 → p=0.0625); the per-perspective attribution
     closes exactly (7+16+2+14 = 39 true positives and 1+2+1+5 = 9 leaks = 48); the forced
     sets are 27+3 = 30 versus 25+1 = 26, giving the 7/3 discordance and the net of 4 the text
     reports. I also checked the multiplicity treatment independently of the paper's own
     three extensions: at rank 7 of a family of *m*, the flagship's adjusted value is
     0.0013·(m−6), which stays below α=0.05 for any *m* up to about 38 — so the flagship's Holm
     survival is robust to a substantially larger family than the authors test, and the
     post-hoc family definition is not carrying the result.
   - **3.3** Threats to validity are measured rather than merely disclosed. The paper's first
     two channels sit on the judgment side — expectation framing and observation leakage — and
     both are handled by measurement rather than by sanitization: a mechanical scan of all 81
     rebuilt packs found 19 expectation-flavoured phrases, all inside verbatim server
     responses, and zero framing added by assembly, so nothing needed removing; and the four
     provenance notes were removed *before* any re-adjudication, so no run had to be redone.
     Two further channels then surfaced *after* the re-adjudication — the paper's third and
     fourth — and these are the ones that cost re-runs: ten packs carried an embedded
     maintainer-cognition section that the core, flat and source-only dispatches forbid
     reading, which forced thirteen affected runs across both backbones to be re-adjudicated
     and replaced; and a candidate-anchoring audit found cognition entries referencing seven
     of the 81 candidates' own issue numbers, which forced every affected arm and run on both
     backbones to be redone the same way. Every number in §4 is recomputed on the cleaned
     pool, and the pre-cleanup verdict files ship for comparison. Finding two further leak
     channels *after* the re-adjudication, and repairing both by re-running the affected arms
     rather than by argument, is a standard of hygiene I rarely see.
   - **3.4 [major, fixable]** The two control cells that carry the paper's central causal
     claim are constructed by editing dispatches whose edited text a reader cannot
     reconstruct. §4.3 and the Table 5 caption say that "full, no aggregation" is the full
     stage "with both aggregation blocks excised" and "every other rule sentence intact," and that
     "flat judge + aggregation" binds the judge to "the full stage's fixed aggregation
     rule — expressed in the flat judge's own vocabulary, since it carries no A/B/C/D
     perspective labels." Appendix A renders the deployed protocol with a *single*
     "Aggregation (fixed)" paragraph, so "both aggregation blocks" is not recoverable from the
     text; and the label-free re-expression of the aggregation for the flat judge is never
     shown at all. That omission is consequential rather than cosmetic, because the two
     readings differ materially: if the transplanted rule is the ordered precedence of
     Appendix A.1, the finding is "the aggregation rule is the mechanism"; if what was added
     is mostly the "everything else ⇒ Human-Review" clause, the finding narrows to "a
     route-always policy inflates a convention that counts routing as confirmation" — which
     the paper's own framing half-concedes but does not settle. The artifact declaration
     compounds this: Appendix A states "all four dispatch files ship verbatim in the
     artifact," which is four files for nine arms, so the two edited dispatches appear to be
     outside the declared inventory. One paragraph quoting the two edited dispatches, with the
     excised blocks identified, resolves the whole item.
   - **3.5 [major, fixable]** The flagship comparison is measured against a flat dispatch the
     authors show was mis-specified. §4.3 states that the flat dispatch's output-schema line
     "declared a binary verdict field while its v3 supplement mandates three-valued
     verdicts," that both control arms first correct this, and that the schema-only arm
     therefore reaches 0.686 — "the baseline the flagship should be read against, since it is
     the flat judge with its dispatch repaired." Against that baseline the flagship's
     confirmed-set separation is raw p=0.049 and Holm-adjusted 0.098, i.e. it does not
     survive; the flagship's Holm-surviving 0.0052 is measured against the shipped, defective
     dispatch. The paper says this in one dense sentence in the middle of §4.3 and then does
     not carry it forward: the abstract still reports "against 0.588 for a flat single-prompt
     judge reading the same packs and sources," and contribution bullet 2 repeats the same
     pairing. Given how scrupulously the rest of the paper surfaces its own weak points, the
     asymmetry here is conspicuous — the single place it hedges least is the headline number.
     The fix is presentational and cheap: state 0.686 as the headline baseline, report the
     shipped-dispatch comparison as the secondary (favourable) reading, and say in the
     abstract that against the repaired baseline the difference is marginal and does not
     survive correction.
   - **3.6 [minor, fixable]** The full stage's per-run true-positive counts decline
     monotonically across its three runs in Table 4 (40 → 38 → 35), while no other multi-run
     arm does: the flat judge goes 30 → 31 → 27, source-only 35 → 38 → 37, and the
     source-withheld arm 47 → 43 → 49. Majority-vote reduction over three runs presumes the
     runs are exchangeable draws from a single process; a monotone within-arm trend is what
     an order, time or substrate-drift effect looks like instead, and it would inflate the
     variance of the majority estimate in one direction. The paper reports case-agreement
     rates and per-run rows, so a reader can see the pattern, but it does not say whether run
     order was randomised or arms interleaved, and does not address the trend.
   - **3.7 [minor, fixable]** Two claims are stated more strongly than the design supports,
     both in the direction of self-criticism. (a) §4.3 says the counting convention "is also
     the only fully mechanical reading, with no human judgment and therefore no adjudicator
     dependence"; the forced reading that the very next sentence calls "the conservative
     floor" is equally mechanical — both are recodings of the same verdict files — so what
     distinguishes the convention is that it matches deployment policy, not that it alone is
     mechanical. (b) The Conclusion says the perspectives' increment is "measurably absent on
     this pool," while the abstract correctly says "not established here." On the
     with-aggregation row the point estimate actually *favours* the perspectives (9 vs 6
     discordant, p=0.61; nine leaks against the control's twelve, routed-queue precision 0.714
     vs 0.600), and §4.3 says so; "measurably absent" is accurate only for the no-rule row
     (+3, p=1.0), which in any case is underpowered at n=81 with 6/5 discordance. The
     Conclusion should match the abstract's hedge.
   - **3.8 [minor, fixable]** One arithmetic statement does not reconcile. §4.3, "What the
     implementation source is for," reports the source-withheld arm's effect as "a swing of 18
     cases in the withheld arm's favour (discordant 2/18, p=0.0004)." The discordant 2/18
     gives a net of 16, and the confirmed-set difference is 64 − 48 = 16 (48 TP + 16 leaked FP
     against 39 + 9); the recall gain (9) plus the suppression gain (7) also gives 16. The 18
     appears to be a slip for 16, or a mislabel of the one-sided discordant count. Every other
     figure in that paragraph reconciles exactly, as does the rest of §4.3.
   - **3.9 [minor, fixable]** One leak channel is closed at the entry level but not the
     pattern level. The maintainer-cognition materials that perspective D reads are distilled
     from the targets' historical issues and merged PRs — the same threads in which the
     authors' own submissions live. The paper found and removed seven candidate-anchored
     *entries* by auditing for the candidates' own issue numbers, which is the right first
     move, but an issue-number grep cannot detect a *pattern* derived from those issues. The
     exposure is small and quantified (D drives 2 of the 39 confirmations at precision 0.667,
     and the paper finds that cognition "delivered a defect-side signal only in the
     batch-delete leak"), and I do not think it changes a rate materially; a sentence stating
     that the derived patterns were (or were not) re-audited at pattern level would close it.

4. **Verifiability** — Excellent
   - **4.1** The artifact declaration is specific and, for this kind of claim, unusually
     complete: agent role definitions and the strategy-trigger registry, per-version knowledge
     bases and specifications, all generated test scripts with their raw HTTP logs, one
     evidence chain per candidate, the submission ledger, the *original and rebuilt* RQ2 packs
     together with the pack-audit verdict records and per-case judge outputs for every arm and
     run, the RQ3 baseline reports with per-template logs, and the analysis scripts that
     recompute every rate, interval and paired test reported. That is the correct inventory
     for this paper's claims — it includes the negative evidence (the original defective
     packs, the pre-cleanup verdict files) and not just the favourable numbers.
   - **4.2** The method is described well enough to follow or replicate without the artifact.
     The five generation gates are enumerated (§3.3); the four mechanical checks and four
     perspectives carry their exact verdict semantics (§3.5), including the three-valued space
     and what each verdict means; the ordered aggregation clauses and the red lines are given
     in full (Appendix A.1); the flat prompt is quoted in full (Appendix A.2); and the scoring
     vocabulary is defined operationally rather than left implicit — pack, case, case judgment,
     case-agreement rate, "routed", suppression versus precision. The pack-rebuild arithmetic
     is stated in full, and the VDBFuzz comparisons cite file and line. My own spot-checks
     against the released VDBFuzz revision (`7a41449`) found every cited constant exactly where
     the paper says it is.
   - **4.3 [minor, fixable]** Two gaps inside an otherwise excellent package. First, the
     dispatch inventory — Appendix A declares "all four dispatch files," and the arms number
     nine, so the edited dispatches for the two control cells are not covered by the
     declaration (see 3.4). Second, the authoritative dispatch files are Chinese and the
     appendix states that the English prompts are "renderings prepared by the authors": a
     reader checking the paper's protocol description is checking it against a translation,
     and the translator is the author. Neither is fatal — the deployed full-stage and flat
     prompts are quoted in full — but both are places where the paper's strongest evidence
     class is one paraphrase removed from the reader.
   - **4.4 [minor, fixable]** I could not verify the artifact link's reachability: outbound
     fetches to `anonymous.4open.science` were blocked in my environment, so this is an
     unverified item and explicitly *not* a dead-link finding. I record it only so the authors
     know a reviewer may ask for a mirror or for a DOI-archived copy at camera-ready, since
     anonymised 4open.science repositories are not guaranteed to persist.

5. **Presentation** — Adequate
   - **5.1** The structure is complete and conventional (Introduction, Background, Approach,
     Evaluation with three RQs, Limitations, Related Work, Conclusion, Appendix), and the
     running example works: Qdrant #10369 is threaded through all four stages with a concrete
     instance at each — the extracted constraint with its assertion, tier and verified source
     (§3.2); the scenario the state agent constructs after matching no pre-bound strategy, with
     both oracle directions (§3.3); the executed pair of requests and responses (§3.4); and
     the completed chain with its five sections and the source asymmetry that falsifies the
     by-design reading (§3.5). It is the clearest passage in the paper and it makes the
     mechanism legible without the figure.
   - **5.2** Table 5 is well constructed for the argument it has to carry: nine arms, per-run
     rows plus majority rows, the two reference rows below a rule, and a caption that states
     precisely what each arm changes relative to the others — including the two ``flat
     judge +'' arms, the source-withheld arm, and the no-aggregation arm. Given that the paper
     lives or dies on readers accepting that the cells are single-variable, the caption is
     doing load-bearing work and mostly succeeds (the exceptions are in 3.4).
   - **5.3 [minor, fixable]** The most-read passages are the hardest to read. The abstract's
     evaluation paragraph is 241 words across five sentences — a 91-word opener followed by
     four more, several carrying nested em-dash qualifications; the abstract's opening
     paragraph is 128 words across three; and contribution bullet 2 in §1 is a run-in label
     plus two sentences — a 30-word lead and then a single sentence of 185 words that alone
     carries the pooled McNemar result, the recall-only non-survival, the second-family
     non-separation, the three readings, and an internal cross-reference.
     The care taken in hedging has been paid for out of the paper's most-read prose. Splitting
     each into three or four declarative sentences, moving the qualifications to a follow-on
     sentence, would cost nothing and materially change how the paper is first read.
   - **5.4 [minor, fixable]** Limitations (§5) is organized by validity type but delivered as
     a handful of very long paragraphs — the "Internal validity" paragraph alone carries six
     distinct threats (expectation framing, observation leakage, the embedded cognition
     sections, the candidate-anchored cognition entries, adjudication disagreement, and
     protocol–pool co-evolution) plus the design-position rationale. The content is
     outstanding; sub-headings per threat would make it usable and would let a reader cite
     individual bounds rather than "the big paragraph."
   - **5.5 [minor, fixable]** Two numbers are overloaded at the points where the claims are
     most delicate. `0.588` denotes both the flat judge's convention recall and the independent
     adjudicator's substituted joint recall in the same subsection; `0.765` denotes both the
     full stage and the aggregation-only control. Both are textually resolvable, but a reader
     tracking the three-reading structure has to hold the distinction in their head at exactly
     the moment the paper is asking for the most charity.
   - **5.6 [minor, fixable]** A typo: §1's closing paragraph reads "a hand-guided probebuilt
     on \system{}'s boundary reasoning" — missing space (the only spelling-type error I found
     in the manuscript).
   - **5.7 [minor, fixable]** Appendix A says the full-stage prompt "instantiates the deployed
     confirmation protocol" without mapping it to an arm name in Table 5, and the appendix's
     four dispatch files are not tied to the nine arm labels. Naming the arm alongside each
     quoted prompt would remove a mapping ambiguity that currently has to be reconstructed
     from the captions.

### Questions for Authors

- **Q1:** Can you quote the two edited dispatches verbatim — the no-aggregation variant with
  the "both aggregation blocks" identified, and the flat-judge-plus-aggregation variant
  showing the label-free re-expression — and state what share of that arm's gain is
  attributable to the "everything else ⇒ Human-Review" clause versus the ordered precedence
  clauses? — Intended effect: if the transplants are shown to be faithful single-variable
  edits, item 3.4's [major, fixable] resolves and the causal claim behind 2.3 moves from
  supported-by-construction to checkable-by-reader; if the re-expression turns out to be
  largely a route-always instruction, the finding legitimately narrows to a claim about the
  counting convention and 3.4 stands as written.
- **Q2:** What does a flat judge given the raw vendor documentation and the raw HTTP logs
  score on the same 81 cases — no structured pack, no rebuilt contract rows, no
  source-verified specifications? — Intended effect: this is the missing ablation behind
  1.3. If it lands near the flat judge's 0.588, the pack-construction stages are the real
  contribution and Significance should move up on the strength of stages (i)–(iii); if it
  collapses, the four-stage pipeline's value is established rather than assumed, and 1.3
  closes.
- **Q3:** Why is the flagship reported against the shipped flat dispatch (0.588) rather than
  the schema-repaired one (0.686), given that against the repaired baseline the confirmed-set
  separation is raw p=0.049 and adjusted 0.098? — Intended effect: if you adopt the repaired
  baseline as the headline and keep the shipped-dispatch comparison as a secondary reading,
  3.5's [major, fixable] resolves and Soundness can move toward Excellent; leaving the current
  ordering in place keeps the strongest form of the comparison in the text and the weakest
  form in the abstract.
- **Q4:** Were the three runs per arm ordered and interleaved, or run arm-by-arm in sequence?
  The full stage's per-run true-positive count declines monotonically (40/38/35) while no
  other multi-run arm does. — Intended effect: if the runs were interleaved and the drift is
  sampling, 3.6 closes as a non-issue and the majority-vote estimates stand unqualified; if
  they were sequential, the drift is a time effect and 3.6 should be upgraded, since
  exchangeability is what the majority-vote reduction assumes.
- **Q5:** Since all 81 adjudicated submissions come from the GLM-5.2 rounds and the
  configuration you describe contributed none of them, can you report any precision or recall
  figure for the described configuration *on an independently adjudicated sample* — or, if
  not, say so explicitly where the RQ2 rates are first reported? — Intended effect:
  the clarification decides whether 1.4 reads as a bounded transfer caveat, which is how it is
  currently framed, or as an unstated gap between the system specified and the system
  measured, which would also bear on the Soundness tier.

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary

The paper targets documentation–implementation bugs in vector database management systems (VDBMSs): cases where the system silently accepts an input or behaves in a way its natural-language API documentation forbids, producing no crash and therefore no oracle signal. It argues structurally (Table 1) that crash signals, differential testing, metamorphic relations, property-based testing, structured-spec oracles and prose-derived method-level oracles all anchor their expectations somewhere other than system-level behavioral prose, leaving an LLM as the practical oracle, and then builds one: a four-stage pipeline (prose → specification → probe → evidence chain) whose confirmation stage splits an evidence builder from a chain auditor that cross-examines a five-section chain from four perspectives (contract, physical constraints, behavioral elegance, maintainer cognition), with the implementation source as falsification anchor.

The evaluation has two layers. RQ1 reports an operational ledger: 51 maintainer-confirmed bugs and 23 merged fixes out of 81 adjudicated submissions across Milvus, Qdrant and Weaviate, accumulated over sixteen per-version mining campaigns. RQ2 audits the frozen evidence packs that fed the confirmation stage (finding 43.3% of cited (constraint, page) pairs unsupported), rebuilds them against version-pinned documentation, and re-adjudicates the full 81-case pool three times per configuration across nine judge arms — contract core, full stage, source-only, flat judge, flat plus schema fix, flat plus aggregation, full with the source withheld, full with the aggregation removed, and source-only on a second backbone. Reported results are three-valued verdicts with Human-Review counted as confirmed under the deployment convention: contract core 0.157 recall at 0.967 suppression; full stage 0.765 at 0.700; flat judge 0.588 at 0.867; forced-verdict scoring collapsing the last pair to 0.529 vs 0.490; and a decomposition attributing the separation to the routing aggregation rather than to the four perspectives. RQ3 probes the crash-oracle baseline VDBFuzz bidirectionally on Qdrant.

### Core Strengths

- **S1:** The RQ2 measurement is rebuilt in three explicitly separated layers (pack audit, pack rebuild, protocol alignment over a leaked-materials cleanup) with every layer's effect traced, and the ablation design is filled in rather than asserted: the 2×2 of {perspectives} × {aggregation rule} is completed by a fresh arm mid-paper, and two further controls price the schema correction and the source channel. — see 3.1, 3.4
- **S2:** Statistical execution is careful and checkable: exact McNemar with discordant pair counts reported alongside all but three paired tests, Wilson intervals, and Holm correction with the family definition stated explicitly plus a sensitivity analysis over three alternative family sizes. I recomputed every p-value, Holm multiplier, F1, Youden's J and net from the reported counts; all reproduce. — see 3.6
- **S3:** Results that cut against the paper's own thesis are reported rather than buried: the source-withheld arm dominates on the paper's own summary metrics; two of the 41 explicit by-design refutations violate the protocol's own verbatim-intent red line and one of them closed a true bug; and the authors' hand-adjudicated routed queue is not reproducible by an independent adjudicator (κ ≈ 0), which the paper prints with the substituted recall. — see 3.7, 3.8
- **S4:** The RQ3 baseline is audited, not just run: the authors show the released runner's success counters are uninformative (a template counts as success whenever its process exits zero; pointed at a dead port it reports 100% success), substitute a per-template liveness oracle, and bound the claim to the released configuration instead of to crash oracles as a class. — see 3.9
- **S5:** I verified the paper's characterizations of its named competitors against their own texts. MASTOR's `pending`-field mechanism, its source-grounded authority, and its own "cannot detect violations of intended requirements that are not reflected in code" limitation match the paper's Table 1 row 5 exactly; VDBFuzz's three-stage design, the verbatim "logical inconsistencies or invalid state transitions" quotation, and its reported 13 crash + 6 runtime-exception yield all check out. — see 2.1, 2.2

### Core Weaknesses

- **W1:** The flagship separation is measured against a flat-judge baseline whose dispatch the authors themselves found defective; against the repaired baseline the paired test is raw p=0.049 and Holm-adjusted 0.098, i.e. it does not survive correction. The abstract's unqualified "That separation survives Holm correction on the confirmed-set unit" is true only against the shipped, mis-dispatched flat judge. — see 3.2, 5.1
- **W2:** The headline unit (confirmed set under the deployment convention) is monotone in permissiveness — an arm that confirms everything maximises it — and five of the fourteen net cases are additional false-positive confirmations. On the metrics that are not permissiveness-monotone (net true-positive count, F1) the margin narrows sharply, J is effectively tied, and no significance test is reported at all. — see 3.3
- **W3:** The paper's central claimed mechanism — source-grounded falsification — is measured to make things worse: withholding the source raises convention recall from 0.765 to 0.941, raises net from 30 to 32, and raises F1 from 0.788 to 0.835, at a suppression cost of 0.700 → 0.467. This is disclosed only in the body; the abstract presents the source anchor without its price, and the contribution list mentions the control without its direction. — see 3.8, 5.2
- **W4:** Provenance bounds every headline. The 81-case pool and the 51-bug ledger come from sixteen earlier campaigns on a different serving identifier whose per-session strategy and rule configuration the authors say they cannot reconstruct; the pipeline described in Section 3 produced none of the 51; the pool is a submission-filtered subset, and both the packs and the ground-truth-adjacent cleanup were executed by the authors. The RQ1 and RQ2 numbers are therefore within-pool rates on a self-built pool, not pipeline precision or recall. — see 3.10, 1.2
- **W5:** The ablation's own arm definitions are ambiguous exactly where the conclusion needs them to be crisp: the text says the schema correction and the aggregation rule "were bundled in a single arm" while the table reports them as two separate arms, and the flat judge and full stage are described both as receiving "the same per-case evidence bundle" and as differing by "the assembled evidence chain the auditor reads". Since the paper's conclusion is that the difference between the arms is protocol structure and not inputs, this needs to be unambiguous. — see 3.11, 5.3

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The paper's durable contribution is empirical and it is real: 51 maintainer-confirmed bugs with 23 merged fixes across three production VDBMSs, with the fix PRs classified by changed files and every one of the 23 shown to modify implementation code (Section 4.2, "Fix nature"). For a domain whose only dedicated tool is a crash fuzzer, that ledger is a concrete step forward, and the duplicate-tracked handling and the re-verification of every submission as of September 2026 are the kind of bookkeeping most bug-finding papers omit.
   - **1.2 [major, unfixable]** The significance of the *system* is bounded by two structural facts the paper states but does not fully price. First, the evaluation never measures the pipeline end to end: RQ1's yields come from a different pipeline generation than Section 3 describes (no per-session configuration survives), and RQ2 measures a judge protocol over packs assembled from that earlier output. Second, on the paper's own primary comparison the sophisticated confirmation stage is statistically indistinguishable from a flat single prompt once verdicts are forced (0.529 vs 0.490, p=0.34, Section 4.3), and the author-executed hand reading that separates them (0.647 vs 0.569) is not significant (p=0.11) and is not reproducible by an independent adjudicator. The paper's honest conclusion — that the gain lies in routing, not judgment — is a useful negative result, but it also means the artifact's measured value over its cheapest baseline is not established at the sample size available. A revision cannot add adjudicated bugs that no longer exist; this inheres in the data.
   - **1.3** To the paper's credit, the bounded claims are stated as such: Section 5's internal-validity discussion closes with “it measures the human--machine pipeline, not the automated stage's end-to-end precision or recall", and Section 4.2 anchors the direction of the submission filter with the 32-case never-submitted sample (19/32 under the stricter A/B/D rule, 31/32 under the deployed one) while explicitly refusing to read the pair as a significant difference. That is the right treatment of a self-selected pool, and it is what keeps this criterion at Adequate rather than lower.

2. **Novelty** — Adequate
   - **2.1** I checked the delta against the competitor the paper itself calls closest. MASTOR (cached stem `mastor a multi agent approach to semantic test oracle generation for restful apis (corr 2026)`) is source-grounded, multi-agent, generates per-field status oracles *and* cross-operation behavioural-consistency oracles over five association types, and has a ChallengerAgent that reviews each generated oracle and drives one targeted regeneration. Its `pending` fields hold precisely the OAS-declared items the source does not substantiate — i.e. it already computes the documentation-versus-source discrepancy signal — but its "precision-biased design" reads only source-verified fields and never converts that signal into an oracle; its own limitation section concedes it "cannot detect violations of intended requirements that are not reflected in code". The paper's characterization is accurate in both directions, and the paper concedes the sub-components explicitly ("A generated oracle reviewed by a second LLM agent is therefore not new here, and cross-request behavioural oracles are not unique to \system{}"). The residual novelty is the anchor inversion — prose as ground, source admissible only as falsifier — and the paper states that delta honestly rather than overclaiming. That is a real but incremental delta, which is what Adequate describes.
   - **2.2** The competitor checks in the structured-spec line also hold up and the boundary is drawn precisely rather than conveniently. SATORI is per-response-field and OAS-anchored, and the paper does not hide that SATORI's reported bugs include specification–response mismatches — it names that subset explicitly as "the subset of our residual whose prose lives in schema descriptions, while the input-acceptance and state-conformance faces remain unreached" (Section 6). AGORA+ is invariant induction from observed traffic, which is bounded by that traffic and output-side only, matching the paper's row-5 characterization. The use of Metamon's precision 0.722 / recall 0.480 as a reference rather than a baseline is correctly labelled as non-head-to-head. One loose attribution inside this set: Section 4.4 calls the 120-minute per-tool per-VDBMS budget "[VDBFuzz's] own published protocol", but VDBFuzz's text places that budget in its baseline-comparison setup against RESTler and Schemathesis, not in its own bug-finding protocol. The number is right and the point (the sweep finished in 50.8 minutes) is unaffected, but the attribution should be corrected.
   - **2.3 [minor, fixable]** Missing related work, within my specialty: the multi-agent / multi-perspective LLM-as-judge literature is not cited at all, yet the paper's most striking result is that decomposing one judge into four perspectives is measurably absent on this pool. Ma et al., "Judging with Many Minds: Do More Perspectives Mean Less Prejudice? On Bias Amplification and Resistance in Multi-Agent Based LLM-as-Judge" (Findings of EMNLP 2025, pp. 17356–17392) studies exactly whether added perspectives help or hurt LLM judging and finds framework-dependent amplification (debate amplifies bias; meta-judge resists). The paper's related-work paragraph on judge reliability cites self-preference and self-inconsistency work but nothing on multi-agent judging, so the negative result is positioned against the paper's own prior rather than against the literature that has asked the same question. Reserved as provisional — I resolved it at abstract level after the ACL Anthology fetch was blocked — and it is a positioning gap rather than a novelty threat.

3. **Soundness** — Adequate
   - **3.1** The ablation is built, not narrated, and this is the strongest part of the paper. Section 4.3 states plainly that the full-versus-flat comparison "differs from the full stage in two things at once" and therefore cannot attribute the gap; it then adds the two `flat judge +` arms to isolate the schema correction from the aggregation rule, and later fills the missing cell of the design with `full, no aggregation` so that the 2×2 of {perspectives} × {aggregation rule} is complete. Read across the four cells the pattern is coherent: adding the rule moves recall in both rows (0.588→0.765 without perspectives; 0.647→0.765 with them), adding the perspectives moves it in neither (+3, p=1.0 without the rule; exactly 0 with it). The paper also prices the source channel by removing it and prices the baseline's harness by auditing its counters. That is a better-controlled ablation than most LLM-pipeline papers offer.
   - **3.2 [major, fixable]** The flagship contrast is run against a baseline the authors themselves found broken, and the abstract reports only the surviving version. Table 5's caption discloses that the shipped flat dispatch "declared a binary verdict field while its v3 supplement mandates three-valued verdicts"; the schema-fix arm repairs that one line and lifts the flat judge from 0.588 to 0.686 (35/51). Section 4.3 then reports the honest consequence in full — against the repaired baseline the confirmed-set contrast is 48 vs 39, discordant 13/4, net +9, raw p=0.049, entering the family seventh of eight for a Holm-adjusted 0.098 — and says outright that "the flagship's Holm-surviving separation is measured against the shipped flat dispatch". But the abstract states "That separation survives Holm correction on the confirmed-set unit" with no mention of the repaired baseline or the 0.098, and the contribution list gives the 48-vs-34 pairing and its 0.0052 without noting that a fairer baseline exists at 0.686. A reader who stops at the abstract gets a claim the body retracts in the direction of weakness. The fix is presentational, not experimental: lead with the repaired baseline.
   - **3.3 [major, fixable]** The unit that carries the headline is monotone in permissiveness, and the paper's ablation contains the demonstration. The confirmed set counts confirmed true positives plus leaked false positives, so a judge that confirms everything scores 81/81; on this metric the *best* arm on the pool is not the full stage (48) but the source-withheld arm (48 TPs + 16 leaks = 64), and the flat + aggregation control (51) also edges it. The paper discloses that "five of its fourteen net cases are additional false-positive confirmations" and defends the unit as "the unit the deployment resolves", which is defensible as an operational accounting choice. What it does not do is carry the conclusion on a metric that is not inflated by liberality: the net count (30 vs 26) and F1 (0.788 vs 0.706) are reported as point estimates with no test, Youden's J is an admitted tie (0.465 vs 0.455), and the only tested alternative to the confirmed-set unit is the recall-only McNemar, which does not survive correction (0.0225 → 0.090). So the significant result is on the permissive metric and the non-permissive metrics are untested. Reporting a paired test for net or F1 (a bootstrap over the 81 paired cases would do) is the fix.
   - **3.4** The forced-verdict decomposition is the paper's most interesting design finding and it is properly staged: with Human-Review re-scored as False-Positive and the runs re-majoritised, the full stage reaches 27/51 and the flat judge 25/51 (discordant 7/3, p=0.34), and the paper concludes that "the structured protocol escalates to explicit human-review decisions […] the cases the flat judge closes by fiat". It then supports that with a routed-queue analysis (the full stage routes 19.8% of pooled verdicts, the flat judge 8.6%; the two routed queues are of similar precision, 15/21 vs 8/11) and states the conclusion in the right register: "On this pool, what the routing rule buys is not better forced guessing but honest escalation." Reporting forced, joint and convention readings side by side in Table 6, with the caption noting that the forced rows collapse the separation and the convention rows carry it, is exactly the right presentation.
   - **3.5 [major, unfixable]** The primary result is single-backbone and the paper's own second-family re-run of the same pair fails to separate (0.588 vs 0.529, discordant 8/5, p=0.58; forced-only 0.510 vs 0.451, p=0.75), with routing rates dropping on both arms (19.8%→10.3% full, 8.6%→7.8% flat). The paper draws the correct narrow conclusion — "a property of that backbone under this protocol, not a law of the protocol itself" — and reads the non-detection as a non-detection rather than as evidence of absence, noting the paired test is underpowered for a gap of that size. I accept the handling, but the practical consequence stands: the only significant version of the headline is one backbone, one pool, one protocol, and the correction family was defined post hoc by the authors. A revision could re-run the pair on a third family, which would help; it cannot make the primary claim multi-backbone.
   - **3.6** Statistical hygiene here is above the norm and I verified it rather than taking it on trust. All but one paired test report their discordant counts, so the exact McNemar values are checkable: full-vs-flat 16/2 → 0.0013 ✓, source-only-Qwen-vs-flat 15/3 → 0.0075 ✓, source-only-vs-flat 15/5 → 0.041 ✓, full-vs-source-only 8/4 → 0.39 ✓, aggregation-vs-schema-only 2/14 → 0.0042 ✓, aggregation-vs-full 9/6 → 0.61 ✓, no-aggregation-vs-flat 6/5 → 1.0 ✓, no-aggregation-vs-full 1/14 → 0.0010 ✓, no-source-vs-full 2/18 → 0.0004 ✓, forced full-vs-flat 7/3 → 0.34 ✓, leakage-only 5/0 → 0.0625 ✓. The Holm adjusted values follow from the stated ranks and family sizes, including the deliberately adversarial family extensions (0.0092 at ten tests; 0.0066 at ten with the control pairs; 0.0105 at thirteen with both groups). The stratified recalls reconcile exactly to the headline (29+2+8 = 39 convention; 24+0+3 = 27 forced; 26+1+6 = 33 joint), and the F1 / J / net figures I recomputed match to three decimals on both backbones. The single exception is the aggregation-vs-flat pair: it appears only in the footnote's control-pair list, by raw p-value (`aggregation-vs-flat, raw p<0.0001`), with no discordant counts anywhere in the paper — the other two control pairs named in that same footnote do have their counts in the body (no-source-vs-full 2/18, aggregation-vs-full 9/6). That one is the contrast the mechanism attribution rests on most directly and it is the one a reader cannot check — see 3.12(b). In a literature where paired tests are routinely asserted without their contingency tables, this is nevertheless a real strength.
   - **3.7 [minor, fixable]** The protocol-fidelity audit is selective. The paper reports that two of the 41 explicit by-design refutations in the deployed full stage rested on bare structural inference — an absent binding tag and an uncommented fallback chain read as intent — "where the red line requires the case to route instead, and both closed their case as False-Positive, one of them an adjudicated true bug, which is the precise failure the rule exists to prevent" (Section 4.3). That is a ~5% violation rate on the one rule the whole design rests on, and it is measured in only one direction: the confirmations that the aggregation "never consults" (72 of them, by the author's own count) and the 59 weak refutations are counted but not audited for whether they too misapplied the red line. Since the paper's argument is that the source channel is trustworthy *because* it can only refuse on verbatim evidence, an audit of both directions, or of a random sample of confirmations, would close the gap.
   - **3.8 [major, fixable]** The source-withheld control is reported accurately and then not integrated into the paper's claims. Withholding the clone from the full stage — every rule sentence, the four perspectives, the aggregation and the cognition materials intact — rises to 0.941 convention recall at 0.467 suppression, discordant 2/18, p=0.0004; on the paper's own summary metrics that arm is the best configuration measured (net 32 vs 30, F1 0.835 vs 0.788), a point the authors state and then decline to read as a defect ("We do not read that as a defect in the full stage but as the price of the falsification anchor"). Structurally the result is explained: in the fixed aggregation the source-anchored perspective appears only in the by-design clause and no confirming clause, so its votes can only refuse, and here they cost nine adjudicated true bugs against seven adjudicated false positives avoided — the wrong trade under the paper's own stated asymmetry, which the authors themselves note ("this is the one channel not priced that way"). The problem is placement: the abstract presents the source as "the falsification anchor" that "breaks the self-referential loop" with no indication that the anchor is measured to cost more than it saves on the evaluated pool; the third contribution bullet names the source-withheld control without its direction or magnitude. Given that the anchor is the paper's headline design claim, this belongs in the abstract with the numbers.
   - **3.9** The RQ3 baseline treatment is stronger than the usual "we ran the tool" comparison and should be recognized as such. Section 4.4 shows that VDBFuzz's released runner marks a template successful whenever its process exits zero, that neither failure marker can fire (one is an interpreter message never compared against; the other does not match the templates' own message), and that pointing the runner at a port with no server yields exit 0 and a reported 100% success rate — so the paper discards the triple and substitutes a per-template liveness oracle, then reports 22,540 mutations across 205 templates, zero anomalies, with 23,258 HTTP responses over 96 distinct paths as evidence the templates reached a live server. The bound is measured from two directions and only the narrower conclusion is drawn ("on that configuration the crash class is not constructible"), with the scoping of the omitted API-sequence-mutation stage stated explicitly. I confirmed against VDBFuzz's own text that the stage description and the verbatim "logical inconsistencies or invalid state transitions" quotation are accurate, and that the cached artefact facts (205 Qdrant templates, `generation_summary.json`) hold.
   - **3.10 [major, unfixable]** Two provenance facts bound what any of the above can mean, and while both are disclosed, their combination is not assessed anywhere. (a) The 81-case pool and the 51-bug ledger originate from sixteen per-version campaigns on GLM-5.2 whose "per-session strategy and rule configuration inside each target" the authors state they cannot reconstruct, and the reported GLM-5.3-Flash run "contributed none of the 81". So the pipeline of Section 3 and the population being judged are disjoint. (b) The pool is a submission-filtered subset — "the 81-candidate pool is a submission-filtered subset of the pipeline's confirmed output rather than a random sample of it" — with the authors noting the induced bias is conservative for suppression but that "the recall direction is anchored below" only by the 32-case anchor sample, which itself "was also measured on the original packs before the audit, so its absolute value is not comparable to the rebuilt-package numbers below". Every headline recall in the paper is therefore a within-pool rate on a pool the authors assembled, screened and re-packed, with the one external anchor explicitly declared non-comparable to it. That is a limitation a revision cannot remove, and it is the main reason the paper's claims should be read as an existence demonstration (this class of bug is real, findable and confirmable) rather than as a performance measurement of the described system.
   - **3.11 [major, fixable]** The arm definitions are ambiguous in the two places the conclusion depends on them being exact. First, the bundling: the caption of Table 5 describes `flat judge + schema fix` as stopping at the schema correction and `flat judge + aggregation` as *additionally* binding the judge to the aggregation rule, which makes the rule's increment identifiable (0.686→0.765); but Section 4.3's "The completed two-by-two" paragraph states that "The two additions were bundled in a single arm, so the partition of the flat-to-control gain between the schema correction and the aggregation rule is not identified; the schema-only arm accounts for at most +5 of it and the remainder is the rule's." Both readings cannot be right. Second, the input difference: Section 4.3 defines the flat judge as "a single prompt over the same packs and sources but without the assembled evidence chain the auditor reads", while Appendix A states that "Each judge receives the same per-case evidence bundle and may read the case's version-pinned source clone". If the flat judge sees the same bundle, "without the assembled evidence chain" is a statement about protocol, not inputs; if it does not, the comparison carries a third difference beyond the two the paper enumerates ("the four-perspective organization and the aggregation rule"), and the conclusion that the arms differ in structure rather than inputs weakens. The fix is one clear paragraph stating, per arm, the exact files handed to the dispatch and the exact lines edited — the paper clearly has this information (it names the edited schema line and the excised aggregation blocks elsewhere).
   - **3.12 [minor, fixable]** Two smaller threats to the convergence of the design's controls. (a) The three-way exact tie in forced-verdict recall — 27/51 in the full stage, in the aggregation-only control, and in the perspective-only arm alike — is doing a great deal of work in the argument that structure affects escalation rather than decision, and the paper reports only the totals. Whether the three arms confirm *the same* 27 cases is not stated; if the sets differ materially, "the same forced reading" is a coincidence of counts rather than a common decision core. A per-case overlap (a 3×3 agreement table for the 51 bugs) would settle it. (b) The one paired test whose discordant counts are not reported is the one inside the central attributional sentence: "adding the aggregation rule moves recall in both rows (0.588 → 0.765 without perspectives, p<0.0001; 0.647 → 0.765 with them)". Every other test in the subsection ships its contingency table; this one does not, and the first clause of it is also the contrast that bundles the schema correction with the rule.

4. **Verifiability** — Excellent
   - **4.1** The Data Availability section enumerates a replication package that covers every claim in the paper: agent role definitions and the strategy-trigger registry, per-version knowledge bases and specifications, all generated test scripts with raw HTTP logs, one evidence chain per candidate, the submission ledger, both the original and the rebuilt RQ2 packs with the pack-audit verdict records and per-case judge outputs for every arm and run, the RQ3 baseline reports with per-template logs, and the analysis scripts. The text is unusually forthcoming about the artefacts that normally stay hidden: the pre-cleanup verdict files ship alongside the cleaned ones, the per-judgment audit of the 41 by-design refutations ships, and the per-run affected flags for the cognition-anchor cleanup ship. Combined with Appendix A reproducing both judge prompts and naming the deliberate difference between them, the work is followable to a level of detail most papers in this area do not reach. I judged the link as declared and specific; per the rubric I did not attempt to resolve or clone it.
   - **4.2** Within the text, the checkable constants are given at the granularity that lets a reader reproduce the baseline comparison rather than take it on faith: the RQ3 footnote cites `vdbfuzz/keywords/__init__.py:292` and `vdbfuzz/mutator.py:247` for the 65,536 integer-boundary ceiling and the 10,000 dimension candidates, and names the hardcoded 2^63 proof-of-concept script as distinct from the 205 swept templates, so a reader can verify both the bound and the exclusion. I could not check those two constants from the cached VDBFuzz text (they are artefact-level, not paper-level), so I record them as specific-but-unverified rather than as errors.
   - **4.3 [minor, fixable]** Three gaps in what the text alone supports. (a) The two de-leaking corrections (the ten packs carrying embedded cognition sections; the seven candidate-anchored cognition entries) are reported only as "the affected verdicts were replaced" — the pre-cleanup numbers are not given in the text, only pointed to in the artefact. Since the de-leaked class cost at least two confirmed bugs on the recall side, and since the paper's headline margin over the flat judge is nine cases, the magnitude of these corrections should be in the text, not only in the package. (b) The independent-adjudicator substitution is stated as producing "0.529, 0.529, and 0.588" from "2, 0, and 4 confirmations where the authors confirm 11", which requires an unstated reconciliation (4 independent confirmations cannot yield +3 over the forced 27 unless one of them coincides with an already-forced case); one sentence would close it. (c) The appendix notes that the Chinese dispatch files are authoritative and the English prompts are renderings, so the actual operational content is only in the package. Acceptable, but it means the paper's Appendix A cannot be checked against itself.

5. **Presentation** — Adequate
   - **5.1 [minor, fixable]** The abstract carries a claim the body qualifies away: "That separation survives Holm correction on the confirmed-set unit" appears without the condition that the baseline is the shipped flat dispatch; the repaired baseline gives raw 0.049 / adjusted 0.098 (Section 4.3). The abstract also reports "0.588 for a flat single-prompt judge" without noting that the same judge reaches 0.686 with its schema line corrected. Since the abstract is where most readers stop, the conditional needs to appear there or the headline needs restating against the repaired baseline.
   - **5.2 [minor, fixable]** The abstract and the contribution list present the implementation source as the design's answer — "the only channel that may refute---to break the extraction-judgment self-reference" — without the measured price (source withheld: 0.941 recall, net 32, F1 0.835 vs the full stage's 0.765 / 30 / 0.788). The third contribution bullet names "the source-withheld control that prices the falsification anchor" but withholds the direction. Given that suppression is the other headline axis and the withheld arm's suppression is 0.467, a reader can reasonably reach the abstract's end without learning that the anchor is the paper's most expensive component.
   - **5.3 [minor, fixable]** Table 5 is hard to read and is the paper's central exhibit. Its 24 data rows mix nine arms with two reference rows in one undifferentiated block — `contract core, majority (ref.)` sits mid-block, between `source-only-Qwen` and the `full, no source` group, and `full, majority (ref.)` closes the table — with no separator convention, so a reader scanning for one arm has to hold the whole block in mind. Per-run granularity is uneven in a second way: most arms show three runs plus a majority, but `flat judge + schema fix` and `source-only-Qwen` appear as majority rows only (the caption states the latter's three runs "are collapsed to its majority row"), so those two rows read as a different kind of object from their neighbours. An arm-per-block layout, grouping each arm's runs with its majority and adding a column naming the dispatch edit that arm carries — the information is already in the caption — would let a reader reconstruct the 2×2 from the table alone.
   - **5.4 [minor, fixable]** The prose is dense to the point of opacity in the subsection carrying the main result. Section 4.3's paragraphs run to twenty-line sentences with several parenthetical qualifications each, and the load-bearing distinctions (confirmed set vs recall-only vs forced vs joint; leak vs routed vs forced-confirmed) are introduced across four hundred words of a single paragraph. The paper has an unusually clean conceptual structure underneath — three scoring conventions, four cells, nine arms — and it would survive being presented as one numbered list of arms, one 2×2, one table of scoring conventions.
   - **5.5 [minor, fixable]** Smaller items, all mechanical: "probebuilt" is missing a space (Introduction); "a swing of 18 cases in the withheld arm's favour" reports the discordant-pair count where the net is 16 (Section 4.3); the claim about the abstract's scope — Section 4.3 says the four perspectives' contribution is "measurably absent" and the Conclusion repeats "measurably absent", while the abstract says only "not established here"; the flat judge's absent evidence-chain sections are a third arm difference in one sentence and not in another (see 3.11); the flat judge's routed-queue precision appears as 8/11 in one paragraph and 15/25 in another without the arms being distinguished in place (the second is the aggregation control).

### Questions for Authors

- **Q1:** Under the repaired flat dispatch — the schema-fix arm, confirmed set 39 — the flagship contrast is raw p=0.049 and Holm-adjusted 0.098, and Section 4.3 says so plainly. Would you restate the abstract's headline claim against the repaired baseline rather than the shipped one? — [intended effect: if so, item 5.1 moves up and 3.2's rating moves to a resolved presentation issue; if you can also report a net/F1 paired test, item 3.3's rating moves up because the conclusion would then rest on a metric that permissiveness does not inflate.]
- **Q2:** In the three arms where forced-verdict recall is exactly 27/51 (full stage, aggregation-only, perspective-only), do the three arms confirm the same 27 cases? — [intended effect: if the sets overlap heavily, item 3.12(a) disappears and the "structure affects escalation, not decision" reading strengthens; if they diverge, the coincidence-of-counts reading weakens the mechanism attribution in 3.4.]
- **Q3:** For each of the nine arms, which exact files does the dispatch receive, and which exact lines were edited? Specifically: does the flat judge receive the same per-case evidence bundle as the full stage, and does `flat judge + aggregation` include the schema correction? — [intended effect: a precise answer resolves 3.11 and moves that item off the weakness list; an answer that the flat judge receives less material would move 2.1 and 3.1 down, since the comparison would no longer isolate protocol structure.]
- **Q4:** The source-withheld arm beats the full stage on net true positives (32 vs 30) and F1 (0.835 vs 0.788). You justify keeping the source channel on an a priori error-cost position. Is there a variant — for example, allowing source evidence to support as well as refuse, or requiring only that refutations meet the verbatim bar — that would test whether the channel's *form* rather than its *existence* is what costs nine true bugs? — [intended effect: a positive answer would raise item 3.8's rating by converting a priced loss into a design space you explored; a negative answer leaves 3.8 as a `[major, fixable]` placement problem and confirms that the anchor's cost is inherent.]
- **Q5:** The reverse RQ3 direction rests on a hand-executed probe whose value "was chosen with knowledge of the overflow mechanism from VDBFuzz's own published case study", and the paper states you "did not measure whether \system{}'s automated boundary strategy would generate a value in the failing range unaided". Given that the forward direction is a full 205-template sweep, is a measured (not hand-guided) reverse direction feasible — running the boundary agent on v1.4.0 with the case study withheld? — [intended effect: a yes moves the RQ3 complementarity claim from an existence proof to a measurement and would raise the corresponding item under 4.2; a no should be stated in the abstract, which currently places the two directions in the same sentence without the asymmetry.]

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary

The paper targets *documentation-implementation bugs* in vector database management systems: inputs the system silently accepts, or behaviors it exhibits, that contradict the vendor's natural-language API documentation (a canonical instance of the class is Milvus accepting `nprobe=0` where the docs declare a range of [1, 16384]; the bug threaded through all four stages as the paper's running example is Qdrant issue #10369, where the `recommend` API bypasses vector-dimension validation for examples taken from `lookup_from`). It argues that this class is invisible to every deterministic oracle family the authors analyze, because each family anchors its expectation in a crash signal, another implementation, an output-output relation, a machine-checkable property, or a structured spec rather than in system-level prose, and that an LLM-derived oracle is therefore the practical option — which imports the LLM's false-positive problem. TestVDB answers with a four-stage agent pipeline: behavioral-specification extraction from crawled documentation, strategy-bound probe generation by three attack agents, Docker-pinned sandboxed execution, and a confirmation stage that splits evidence assembly from cross-examination over a five-section evidence chain judged from four perspectives (contract, physical/objective constraints, behavioral elegance, maintainer cognition), with the implementation source as the falsification anchor.

Empirically the paper reports two layers. First, an operational submission ledger across Milvus, Qdrant and Weaviate: 51 of 81 adjudicated upstream submissions were maintainer-confirmed as real bugs, 23 of them fixed by merged PRs, 30 adjudicated as false positives, 49 still unadjudicated. Second, after an audit found 43.3% of the cited (constraint, page) pairs in the frozen evidence packages unsupported by the pages they cite, the authors rebuilt all 81 packages against version-pinned documentation and re-adjudicated the full pool three runs per configuration under nine judge configurations. The contract-only core recalls 0.157 at 0.967 suppression; the full structured stage reaches 0.765 recall at 0.700 suppression; a flat single-prompt judge reading the same packs and sources reaches 0.588 at 0.867. The paper attributes that separation to the routing/aggregation rule rather than to the four perspectives — adding the aggregation rule to the flat judge reproduces the full stage's recall exactly (39/51), while the four perspectives without the aggregation are statistically indistinguishable from the flat judge — and it reports three readings of the same stage side by side: forced verdicts 0.529, hand-adjudicated joint judge-plus-human 0.647, and the deployment's counting convention 0.765. A bidirectional probe against the VDBFuzz crash-oracle fuzzer on Qdrant v1.18.0/v1.4.0 shows complementary reach in both directions.

### Core Strengths

- **S1:** The measurement rebuild is itself the contribution's strongest evidence: a three-layer audit (shipped packs → rebuilt packs → protocol alignment) with quantitative pack accounting, and an explicit statement of what the audit did *not* verify — see 3.1, 4.2.
- **S2:** Numeric integrity: every row of both confirmation tables partitions the 81-candidate pool correctly, and every rate, Wilson interval, exact McNemar p-value and Holm multiplier I recomputed regenerates — see 3.2, 4.1.
- **S3:** The paper reports results that run against its own design — the four-perspective organization's increment is null, the source-withheld control dominates on the paper's own summary metrics, two by-design refutations violated the paper's own red line — and states that "the aggregate credit for the benchmark belongs to the cheaper configuration, not to the one this paper contributes" — see 3.3, 1.2.
- **S4:** The novelty claim is delimited honestly: the paper names what is *not* new in the closest prior work, organizes the claim around where each oracle family anchors its expectation, and lists its own objective-constraint component as a row of the exclusion table precisely so the residual is not overstated — see 2.1.

### Core Weaknesses

- **W1:** The one control that carries the paper's headline attribution — the flat judge bound to the full stage's aggregation rule — is not shown well enough to check, and the aggregation rule is defined over the four perspectives it is supposed to leave out — see 3.4, 4.3.
- **W2:** The same finding about the four perspectives is stated at two different strengths, "not established" in the abstract and introduction versus "measurably absent … not merely unestablished" in the body and conclusion, and the stronger form rests on a non-significant test (net +1, p = 1.0) of exactly the kind the paper elsewhere refuses to read as evidence of absence — see 3.5.
- **W3:** The abstract and conclusion do not carry two qualifications the body attaches to the headline: that the source-withheld arm beats the full stage on the paper's own summary metrics (net TP−FP 32 vs. 30, F1 0.835 vs. 0.788), and that both the 0.765 recall and the 63.0% precision inherit a submission-filtered, pool-internal measurement — see 1.3, 1.4.
- **W4:** The central comparison is carried by very long single paragraphs with a ten-term definition run-on, one figure for the whole paper, and no visual for the nine-arm design or the recall/suppression tradeoff; a capable reader outside this niche will not follow it in one pass — see 5.2, 5.3, 5.4, 5.5.

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The submission ledger (Table `tab:yield`, §4.2/RQ1) is a concrete, checkable impact claim: 51 maintainer-confirmed bugs out of 81 adjudicated across three production systems, 23 fixed by merged PRs. The authors go beyond the headline by validating the fix column: a classifier over changed files shows all 23 fixes modify implementation code, 15 also add regression tests, none is documentation-only, and the classifier is sanity-checked against the fix PR of the candidate the authors themselves later disproved (Qdrant #9149, identified as test-only, matching the seven-version re-probe that reclassified it). The table partitions exactly: 29+14 = 43, 14+14 = 28, 8+2 = 10, 51+30 = 81, and the status partition 23 fixed + 18 open + 7 closed-without-fix + 3 duplicate-tracked = 51. Bug reports a maintainer merged a fix for are the strongest form of practical impact this kind of work can show.
   - **1.2** The paper's second-order contribution is a transferable design lesson for anyone building LLM-based triage or verification stages: on this pool, what separates a structured protocol from a flat judge is not the analytical framework but the rule that turns unresolvable cases into routed ones plus a fixed aggregation order (§4.3, "Structure is a measured mechanism", "The completed two-by-two"). Reporting that a designed-in component "is measurably absent" is rare and useful, and it is supported by a completed 2×2 rather than by a single ablation.
   - **1.3 [minor, fixable]** The abstract's framing attributes impact to the confirmation stage's "five-section evidence chain … from four perspectives … with the implementation source as the falsification anchor", but §4.3 measures both of those components as not helping: the perspectives add nothing measurable (3.5 below), and withholding the source clone *improves* the configuration on the paper's own aggregate metrics (net TP−FP 32 vs. 30; F1 0.835 vs. 0.788; recall 0.941 vs. 0.765). The body states this plainly and says the aggregate credit "belongs to the cheaper configuration"; the abstract and the conclusion do not carry it. A reader who reads only the abstract will over-attribute value to source grounding.
   - **1.4 [minor, fixable]** The abstract reports "51 of 81 adjudicated submissions" and later "0.765 recall" without the two scope bounds the body is careful about: the pool is a submission-filtered subset of the pipeline's confirmed output chosen by authors with no deterministic submission rule (§4.2), and RQ2's recall is explicitly pool-internal. Neither bound invalidates the numbers, but both bound what "significance" means, and the abstract should say so.

2. **Novelty** — Adequate (provisional: I have not surveyed the field; this is assessed from the paper's own claims and its account of prior work)
   - **2.1** The claim is organized around a single crisp criterion — where each oracle family gets its expectation — and the exclusion table (Table `tab:exclusion`) states, for each family, the structural reason it anchors elsewhere, marking rows 1 and 8 as directly exercised and rows 2–7 as argued from mechanism. The Related Work section names the closest systems and concedes what is not new ("A generated oracle reviewed by a second LLM agent is therefore not new here, and cross-request behavioural oracles are not unique to TestVDB; what is new is the anchor inversion"). Including the authors' own objective-constraint catalogue as row 7, with the argument that omitting it would overstate the residual, is exactly the honest move.
   - **2.2 [minor, fixable]** The demonstrated increment is thinner than the framing. On the paper's own measurements, the effective ingredients are a fixed aggregation order and a three-valued verdict with a routing default — process design, not new capability — while the distinctive structural element (four-perspective cross-examination) is measurably inert and the falsification anchor is net-negative on the summary metrics. What remains as the originality claim is the anchor inversion: the documentation is the ground and the implementation may only falsify. Judged on the paper's own account of MASTOR (source-anchored with a ChallengerAgent), METAMON (LLM judge over generated oracles) and LogicHunter (agentic oracle that consults and executes the implementation before returning a verdict), that delta is real but reads as a re-articulation of who arbitrates. I flag this as provisional: a domain expert who knows these systems' internals may rate this Weak, and the paper would be more convincing if it showed an outcome difference attributable specifically to anchor inversion rather than to the aggregation rule.
   - **2.3 [minor, fixable]** Three framings of the contribution disagree within the paper: the title sells "LLM-Derived Behavioral Specifications", the abstract's central paragraph sells the four-perspective evidence-chain cross-examination, and contribution 2 (Section 1) sells the routing aggregation as "the measured mechanism on the primary backbone". The paper does not tell the reader which one it wants credit for.

3. **Soundness** — Adequate
   - **3.1** The measurement design is unusually well controlled for an LLM-based study. The three layers (§4.3, "Measurement design: audit, rebuild, protocol alignment") each isolate one variable, and the audit's own arithmetic is printed and closes: 2,106 assembled constraint rows → 674 endpoint-filtered out → 463 removed by evidence verification → 969 survivors → 667 kept + 302 archaeology rows dropped, 667+7 = 674 survivors, typed 22 `explicit` versus 652 inferred-from-behavior. The authors then state the audit's boundary — citations were verified, observation payloads were not — and enumerate the four cases where the recorded observation reproduces the filed report's parameter shape rather than the shape the API consumes, noting that three of those are nevertheless true positives because the maintainers reproduced them with corrected payloads and fixed them together. Fine-grained, and the right thing to write down.
   - **3.2** I attempted to regenerate every number the paper prints from the other numbers it prints. All 32 data rows of Tables `tab:rq2-matrix` and `tab:rq2-single` satisfy TP + FP leaked + FN missed + TN intercepted = 81, with TP + FN = 51 and FP + TN = 30 in every row. Derived values check: 8/51 = 0.157 with Wilson [0.082, 0.280]; 29/30 = 0.967 [0.833, 0.994]; 39/51 = 0.765 [0.632, 0.860]; 21/30 = 0.700 [0.521, 0.833]; 19/32 = 0.594 [0.423, 0.745]; 37/51 = 0.725 [0.591, 0.829]; and the second-family Wilson [0.452, 0.712]. Fourteen exact McNemar p-values regenerate from the discordant pairs (16/2 → 0.0013; 11/2 → 0.0225; 5/0 → 0.0625; 6/1 → 0.125; 13/4 → 0.049; 2/14 → 0.0042; 1/14 → 0.0010; 3/19 → 0.0009; 9/6 → 0.61; 6/5 → 1.0; 15/3 → 0.0075; 15/5 → 0.041; 8/4 → 0.39; 2/18 → 0.0004), as do the footnote's Holm multipliers under all three family sizes (4 → 0.0052; 7-member extensions → 0.0092 and ×5 = 0.0066; 13-member extension ×8 = 0.0105), the recall-only multiplier 4 → 0.090, the F1 and Youden values on both backbones, and the three-way stratum decomposition (convention 29+2+8 = 39, forced 24+0+3 = 27, joint 26+1+6 = 33 over 37+3+11 = 51 bugs; the core's 8+0+0 = 8). The RQ3 response tally also closes: 14,022 + 7,520 + 1,512 + 204 = 23,258. Numbers that cannot be regenerated from the printed text are missing inputs, not arithmetic failures, and I list them in item 4.3.
   - **3.3** The paper reports adverse results rather than burying them: the four-perspective organization's null increment with the completed 2×2 (§4.3, "The completed two-by-two"); the source-withheld arm's superiority on net TP−FP and F1; the disclosure that two of the 41 "explicit" by-design refutations were bare structural inference that closed a case as False-Positive, "one of them an adjudicated true bug, which is the precise failure the rule exists to prevent"; the near-chance agreement (κ = −0.01, 0.08, 0.11) between the authors' hand pass and an independent adjudicator; and the statement that the measured deployment is "in this respect more conservative than its own stated position". This is the paper's most distinctive quality.
   - **3.4 [major, fixable]** The arm that carries the paper's headline attribution is not auditable from the text. §4.3 ("What in the protocol carries the gap") says the second "flat judge +" arm binds the judge "to the full stage's fixed aggregation rule — expressed in the flat judge's own vocabulary, since it carries no A/B/C/D perspective labels". But the aggregation rule, as printed in Appendix A, is defined entirely over perspective verdicts: A = Confirmed ⇒ Confirmed; A = Refuted ⇒ False-Positive unless B = Confirmed; B = Confirmed ⇒ Confirmed; D signals decide; C = Refuted ⇒ False-Positive; everything else ⇒ Human-Review. To apply that rule without perspective labels, a judge must still evaluate something equivalent to "does the observation contradict an explicit contract assertion" (A), "is it an objectively invalid value" (B), "is there verbatim by-design intent" (C), and "does maintainer cognition speak to it" (D) — i.e., the perspectives' content. If so, the arm removes the *labels* rather than the *organization*, and the claim that recall is "reproduced *without* the four-perspective organization" is not established by this control. The damage is bounded, because the converse arm (perspectives without aggregation, 0.647) also sits near the flat judge, so the overall direction survives; but the specific attribution to "the rule, not the organization" rests on a manipulation a reader cannot inspect. Printing the two dispatches would resolve it.
   - **3.5 [minor, fixable]** Claim strength for the perspectives result varies by section. §4.3 says the contribution "is therefore not merely unestablished: on this pool it is measurably absent", and the conclusion repeats "measurably absent on this pool, not merely unestablished"; the abstract, the introduction's narrative and contribution 2 all say "not established". A net difference of +1 with p = 1.0 is a failure to reject, not a demonstration of equivalence, and the paper shows it knows the distinction in the backbone-replication paragraph ("we state this as a non-detection rather than as evidence that the effect is absent there: at this pool size the paired test is underpowered"). The same standard should apply to the perspectives' null, ideally with a confidence interval on the difference.
   - **3.6 [minor, fixable]** §4.2's anchor paragraph first says the submitted pool's forced (27/51 = 0.529) and joint (33/51 = 0.647) strict readings "bracket" the never-submitted anchor's 0.594, then concludes "Neither pairing places the submitted pool above the never-submitted stream". One of those two readings, 0.647, *is* above 0.594. Bracketing implies the direction is undetermined — a weaker and different statement from the one printed. Only the deployed-protocol pairing (0.593 vs. 0.969) supports the sentence as written.
   - **3.7 [minor, fixable]** The flagship difference is reported as a discordant net (16/2, net +14) with a p-value and no confidence interval, and the claim that "the advantage is not an artifact of that unit" rests on point estimates of F1 and Youden's J across two backbones, with no interval for either and no correction for that derived-metric family. Given how disciplined the rest of the statistics are, these are conspicuous gaps.

4. **Verifiability** — Adequate
   - **4.1** The artifact is declared with an enumerated inventory mapped onto the reported claims (Data Availability): agent role definitions and the strategy-trigger registry, per-version knowledge bases and specifications, all generated scripts with raw HTTP logs, one evidence chain per candidate, the ledger, the original and rebuilt RQ2 packs with pack-audit verdict records and per-case judge outputs for every arm and run, the RQ3 baseline reports with per-template logs, and "the analysis scripts that recompute every rate, interval, and paired test reported here". The text is also largely self-sufficient for the method: five generation gates, seven objective-constraint classes with the ef/nprobe carve-out, the aggregation clauses in order, the evidence-chain sections, and the strategy registry's pre-binding as a pure function of `specifications.json`. I did not check that the URL resolves (no network access in this review); the rubric asks only that the link be declared, and it is.
   - **4.2** The paper states its non-reproducibility boundaries instead of leaving the reader to find them: serving identifiers and run dates rather than an immutable weights snapshot, the verbatim Chinese dispatch files as authoritative with English renderings in the appendix, the frozen-package protocol's inability to exclude training-data contamination, and the requirement that the deployment's absolute rates not be compared to the pre-audit anchor. That is the right way to bound a measurement made on a moving LLM target.
   - **4.3 [major, fixable]** A few inputs needed to check the central claims are absent from the text: (a) the two "flat judge +" dispatches, above all the aggregation-only prompt (3.4); (b) the run count behind the "flat judge + schema fix, majority" row, which is the arm the flagship is compared against for the "does not survive correction" statement (§4.3, "What in the protocol carries the gap"), while the arms paragraph says every configuration re-adjudicates the pool in three independent runs; (c) several percentages printed without their counts — routing at 28.4%, 10.3% and 7.8%, and the prose statement that the aggregation-only control and the perspective-only arm both show forced-verdict recall 27/51, which appears in no table. The artifact presumably closes all of these, but a reader without network access cannot.
   - **4.4 [minor, fixable]** Appendix A says "all four dispatch files ship verbatim in the artifact" and identifies those four as the full-stage, contract-core, flat-judge and source-only dispatches. The evaluation nevertheless reports nine configurations whose protocols differ (source withheld; aggregation excised; schema fixed; aggregation added), so five dispatch texts are neither printed nor accounted for. A one-line inventory of every dispatch file would close this.

5. **Presentation** — Adequate
   - **5.1** Structure and referencing are clean. I extracted every `\ref` and `\label`: all 19 distinct reference targets resolve to labels that exist (no dangling references), each of the six tables and the single figure is cited from the text at the point it is used, there is no `%`-comment, `\iffalse` or comment-environment residue in the stripped source, and claims are cross-referenced by section rather than restated. The prose language itself is clean, precise and idiomatic.
   - **5.2 [minor, fixable]** One figure for a paper whose central result is a nine-arm, three-scoring comparison. There is no visual for the completion of the 2×2 (perspectives × aggregation) and none for the recall/suppression tradeoff across arms, even though the paper's whole argument is a two-dimensional tradeoff that Table `tab:scorings` only partially shows. Two figures — the 2×2 and a recall-vs-suppression scatter of the nine configurations — would let a reader see the paper's actual finding in seconds rather than reconstructing it from six tables and several thousand words.
   - **5.3 [minor, fixable]** Concrete passages a capable non-specialist will not get through. (i) Contribution 2 in Section 1 is a single sentence of roughly 200 words carrying every hedge of §4.3 at once (48 vs. 34, Holm 0.0052, five of fourteen net cases, recall-only 0.090, p = 0.58, three readings) — it is unparseable on first read and it is the sentence a reviewer is most likely to quote. (ii) §4.3's "Arms and adjudication" paragraph defines all nine judge configurations inside one sentence with parenthetical one-line descriptions and never tabulates what each judge sees; the arms are the paper's experimental design and deserve a table. (iii) §4.3's opening paragraph introduces "false-positive candidate" versus the small-caps `False-Positive` verdict, "suppression", "leak", "pack", "case", "case judgment", "case-agreement rate" and "routed" in one run-on; every table depends on these, so they need to be separated and, ideally, repeated in the table captions. (iv) The Limitations paragraph "Internal validity: judgment-side threats" is a single paragraph of well over a thousand words covering six distinct threats; it should be split. (v) RQ3 states the same "a later operation produces the panic … a surface we have not measured" bound at the end of two consecutive paragraphs.
   - **5.4 [minor, fixable]** "Leak" carries two unrelated senses within a few pages: a candidate the stage wrongly confirms (defined in §4.3), and provenance annotations leaking into judge materials ("the four leak cases", Layer 0 and the paragraph "The four leak cases, re-measured on clean packs"). "The nine leaks" and "four leak cases" therefore read as inconsistent. Similarly "confirmed" denotes maintainer confirmation (RQ1), a stage verdict label (RQ2) and a majority-vote outcome — usually disambiguated by context, occasionally not.
   - **5.5 [minor, fixable]** Text-level fixes: the typo "probebuilt" (Introduction, final sentence of the VDBFuzz passage, where "probe built" is meant); the self-reference "the two thinner conditions were ours, not the authors'" (§4.3, the independent-adjudicator passage), which is confusing in a paper whose "ours" and "the authors'" are the same people; and the abstract's fourth paragraph, which compresses five statistics and two hedge clauses into two sentences and would benefit from being split into "what was measured" and "what it does not establish".

### Questions for Authors

- **Q1:** What is the exact text of the two "flat judge +" dispatches, and specifically how is the fixed aggregation rule stated to a judge that carries no A/B/C/D labels — does the judge evaluate one test per clause equivalent to a perspective, or is the rule restated as a single decision procedure? — [intended effect: this is the whole of 3.4 and 4.3; if the prompt shows the rule was applied without re-introducing the perspectives' tests, 3.4 and 4.3 move up, and if it shows the perspective content was restated, the attribution claim narrows to labels versus content and 3.4 stands as written.]
- **Q2:** How many independent runs does the "flat judge + schema fix" arm have, and was its confirmed set (39) compared run-for-run against the full stage's, or as a majority against a majority? — [intended effect: resolves the comparability of the p = 0.049 result in 4.3 and 3.7; a single run compared against a three-run majority would not be like-for-like and the paper should say so, which would slightly weaken the "does not survive correction" framing it currently uses against itself.]
- **Q3:** In §4.2's anchor paragraph, given that the joint strict reading is 33/51 = 0.647 and the anchor is 0.594, what exactly does "Neither pairing places the submitted pool above the never-submitted stream" assert? — [intended effect: if the intended claim is only that bracketing leaves the direction undetermined, 3.6 becomes a one-sentence rewording; if a directional bound is intended, it is supported only by the deployed-protocol pairing and the sentence should be scoped to it.]
- **Q4:** The source-withheld control is stronger on the paper's own summary metrics (net TP−FP 32 vs. 30; F1 0.835 vs. 0.788). Is there any measurement that isolates the falsification anchor's value at matched accuracy — for example, false positives per confirmed true bug at equal recall — or is the case for it the stated cost asymmetry alone (a maintainer triage pass is cheaper than a shipped defect)? — [intended effect: determines whether 1.3 is a framing problem the abstract can fix, or a limitation of what the paper can claim for its contributed mechanism.]
- **Q5:** A net difference of +1 with p = 1.0 is reported as the perspectives' contribution being "measurably absent" (§4.3, Conclusion) but "not established" (abstract, Section 1). What is the confidence interval on that difference, and would the authors accept the same standard of evidence they apply to the second backbone's non-replication? — [intended effect: if the interval is tight around zero, Soundness 3.5 moves up and the stronger wording is defensible; if not, the abstract's weaker wording should govern and the conclusion should be softened.]

### Self-Check

- Every Detailed-Assessment item points to a specific section, table, paragraph or claim, described in my own words: yes (Sections 1, 4.2, 4.3, 4.4 and 5, plus the named paragraphs inside §4.3; Tables `tab:yield`, `tab:exclusion`, `tab:bug-patterns`, `tab:rq2-matrix`, `tab:rq2-single`, `tab:scorings`; Appendix A).
- Each criterion's tier follows from the evidence listed: Significance — real but bounded impact with two framing gaps → Adequate. Novelty — real but incremental delta, provisional → Adequate. Soundness — core claims defensible, one notable unevaluated control and several minor overreach/consistency gaps → Adequate. Verifiability — main flow followable, key procedural inputs absent from the text but declared in the artifact → Adequate. Presentation — complete and understandable, several passages genuinely awkward, one figure → Adequate.
- Overall Recommendation is the matching line: no criterion below Adequate and no substance criterion Excellent, with no substance Weak and no fixable Weak → **Weak Accept** (rule 2, second bullet).
- Every problem item carries a `[severity, fixability]` tag: 1.3, 1.4, 2.2, 2.3, 3.5, 3.6, 3.7, 4.4, 5.2, 5.3, 5.4, 5.5 are `[minor, fixable]`; 3.4 and 4.3 are `[major, fixable]`. No criterion is rated Poor, so no `[major, unfixable]` item is required or present.
- External-fact claims: I make none about other systems or the field beyond what the paper reports; the Novelty rating is explicitly flagged provisional because I did not survey the field, and every characterization of prior work (MASTOR, METAMON, CASCADE, LogicHunter, VDBFuzz) is drawn from the paper's own related-work text and labelled as such.
- Core Strengths / Weaknesses / Questions are the decision-driving points, each linked to its backing `N.M` items.
- LaTeX stripping: no `%` line comments, `\iffalse`, or `\begin{comment}` markers appear in the stripped `.tex`; notation and macro usage are consistent and no unexpanded macro residue is visible.

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Adequate | Adequate | Adequate | **Adequate** |
| Soundness | Adequate | Adequate | Adequate | **Adequate** |
| Verifiability | Excellent | Excellent | Adequate | **Excellent** |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Weak Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three recommendations again land on Weak Accept, so the unanimous shortcut decides; the consensus-tier count reaches the same verdict, there being no consensus Poor and no consensus Weak. The tier profile is identical to the previous round except in one place, and that place is the point: **Verifiability has moved from Adequate to Excellent by consensus**. Both reviewers who examined the artifact found the declared package complete, specific, and — in Reviewer 1's words — the correct inventory for this paper's claims because it ships the negative evidence (the original defective packs, the pre-cleanup verdict files) rather than only the favourable numbers. That is the round's one measurable advance, and it came from the replication package rather than from the manuscript. It is also the criterion the previous round's reviewers had unanimously rated Adequate while recording that the central comparison could not be checked from the artifact. Everything else held at Adequate. The substance criteria stay where they were for a reason all three reviewers state independently: the paper's own controls have removed the strongest version of its claim, and what remains — a maintainer-adjudicated yield, a measured mechanism finding, and an audited measurement instrument — is publishable on its own terms but is not yet presented as the contribution it is. Reviewer 1 puts the same thing from the reader's side: the paper "should claim the adjudicated 81-case benchmark as a contribution and cite the multi-agent-judge precedent rather than continuing to hedge only." That is a writing problem and a positioning problem, not an evidence problem, and the ranked list below is where they sit. One reviewer's item is deliberately excluded from the revision list as optional: a third backbone, which no reviewer asked for and which the paper already scopes honestly.

### Priority Revisions
Ranked by impact on the verdict. The first two are the only items more than one reviewer rated `[major, fixable]`; the third is a single reviewer's major but is the one path any of them names to a higher Significance tier.

1. **Lead the flagship comparison with the repaired baseline, or restate it.** R1 rates this `[major, fixable]` at 3.5, R2 at 3.2 and 5.1. Both reviewers locate the same asymmetry: the paper's most careful section says the schema-corrected flat arm is "the baseline the flagship should be read against", and that against it the confirmed-set separation is 48 vs. 39, raw $p{=}0.049$, Holm-adjusted 0.098 — it does not survive correction — while the abstract and contribution list still quote the shipped, mis-dispatched flat judge at 0.588 and its surviving 0.0052. R1's phrasing is exact: "the single place it hedges least is the headline number", and the fix is presentational and cheap rather than experimental. Report 0.686 as the headline baseline, keep the shipped-dispatch comparison as the secondary (favourable) reading, and carry the marginal result into the abstract.

2. **Make the two edited dispatches checkable.** R1 rates this `[major, fixable]` at 3.4 and 4.3, R2 at 3.11, R3 at 3.4 and 4.3 — **all three reviewers reached it independently**, which makes it the round's most convergent finding. The two cells that carry the causal claim are built by editing dispatch files: Appendix A prints a single aggregation block, so "both aggregation blocks excised" is not reconstructible from the text, and the label-free re-expression of the aggregation handed to the flat judge is shown nowhere. R3 sharpens why that matters rather than being cosmetic: the deployed rule is defined over the four perspectives, so a judge applying it without labels must still evaluate something equivalent to each perspective's test — and if so, the arm removes the labels rather than the organization, and the attribution to "the rule, not the organization" rests on a manipulation no reader can inspect. R2's version is the complementary one: state, per arm, the exact files handed to the dispatch and the exact lines edited, since the paper clearly has the information. The manuscript now prints the restated aggregation clause in Appendix A and says explicitly that what the arm removes is the separate labelled evaluation and the ordered clause table, not the substantive tests the aggregation refers to; naming the excised blocks and adding the dispatch inventory closes the rest.

3. **Add the missing ablation: a judge given the raw documentation and the raw HTTP logs.** R1 rates this `[major, fixable]` at 1.3, and it is the only item any reviewer connects to a higher tier. All nine arms read the same rebuilt structured packs; stages (i)–(iii) — prose→constraint extraction, source verification, strategy binding, the sandbox — are held constant and never ablated, so the evaluation cannot say what they buy over handing a judge the raw materials. R1 notes why this matters more now than before the revision: the paper's own decomposition concludes the confirmation stage's structure is inert, which leaves the earlier stages carrying the contribution without a measurement to support it. R1's question is the experiment: what does a flat judge over the raw vendor documentation and the raw HTTP logs score on the same 81 cases? Either outcome is useful — near 0.588 and stages (i)–(iii) are the contribution; collapsing and the pipeline's value is established rather than assumed.

4. **Claim the adjudicated benchmark as a contribution.** R1 raises this at 2.2 as an under-claim rather than a defect, and no other reviewer contradicts it. An 81-case pool with 51 maintainer-confirmed bugs and 30 maintainer-adjudicated false positives, an audited and rebuilt evidence pack per case, and a nine-arm × three-run blind judge benchmark over it is, in R1's assessment, the artifact most likely to outlive the paper — and the completed 2×2 makes it reusable for exactly the question the paper answers negatively. It currently appears only under Data Availability as replication material. R1 explicitly confines the claim to what it verified and does not assert a first, so this is a positioning fix the author can make without new evidence.

5. **Test the metrics that permissiveness does not inflate.** R2 rates this `[major, fixable]` at 3.3. The confirmed set counts confirmed true positives plus leaked false positives, so a judge that confirms everything maximises it; on that unit the source-withheld arm (64) outranks the full stage (48) and the aggregation control (51) edges it. The paper discloses that five of the fourteen net cases are added false-positive confirmations and defends the unit as the one the deployment resolves — defensible as accounting — but the only tested alternative is the recall-only McNemar, which does not survive correction. R2's fix is a paired test (a bootstrap over the 81 paired cases suffices) for net or $F_1$, both of which are currently point estimates with no test. The author-side answer, now computed: the net difference between the full stage and the flat judge is $+4$ with a 95\% bootstrap CI of $[-4, +12]$, which spans zero.

6. **Position the negative result against the multi-agent-judge literature.** R1 rates this `[minor, fixable]` at 2.5, R2 at 2.3 — **both reviewers, working separately, name the same uncited work**: Ma et al., "Judging with Many Minds" (Findings of EMNLP 2025), which studies exactly whether adding perspectives to an LLM judge helps and finds framework-dependent amplification. The paper's introduction asserts that a multi-perspective panel does not break shared ambiguity, and its §4.3 measures the four-perspective organization as inert; R1 notes the citation costs no novelty because it supports the premise, and R2 notes the related-work paragraph cites self-preference and self-inconsistency work but nothing on multi-agent judging. One or two sentences in the judge-reliability paragraph closes it.

7. **Address the within-arm run drift, or state that it was not controlled.** R1 rates this `[minor, fixable]` at 3.6. The full stage's per-run true positives decline monotonically (40 → 38 → 35) while no other multi-run arm does, and majority-vote reduction presumes the runs are exchangeable draws — a monotone trend is what an order, time, or substrate-drift effect looks like instead. The paper never states whether run order was randomised or arms interleaved. Either state it, if it was controlled, or record the drift as a bound on the majority-vote estimates.

8. **Presentation and local-consistency cluster (all `[minor, fixable]`, listed so they can be fixed at a glance).** All three reviewers again converge on density, and give measurements this time: R1 measures the abstract's evaluation paragraph at 241 words across five sentences with a 91-word opener, and contribution bullet 2's long sentence at 185 words; R3 measures the Limitations "Internal validity" paragraph at well over a thousand words covering six distinct threats and asks for sub-headings per threat; R2 and R3 both ask for a table of what each of the nine arms sees, and R3 asks for two figures (the completed 2×2 and a recall-vs-suppression scatter of the nine configurations). Localised items: "leak" carrying two unrelated senses within a few pages (R3 5.4); `0.588` and `0.765` each denoting two different things at the point where the three-reading structure is most delicately explained (R1 5.5); and the RQ3 bound about the later panic restated at the end of two consecutive paragraphs (R3 5.3).

*Process note.* Each review was checked by an independent checker against the same stripped source. All three drafts came back with grounded violations on the first pass — eight items in total, every one of them a self-reported count, quotation, locator or attribution rather than a finding: a wrong source-clone count, a fabricated channel tally, a quotation attributed to the paper that belongs to the competitor, and several word counts. Each reviewer patched its own draft, and the second pass found three more of the same kind in one draft, which that reviewer also patched. This is the third consecutive round in which the reviewers' *judgments* survived checking intact while their *self-reported measurements* did not, which is worth recording because it is the same failure mode the paper documents in its own judges. Two drafts also reached the three-round cap, and in both the checker had already prescribed the correction, so the orchestrator applied those rather than leave the drafts unresolved — recorded here because they are edits to a review made outside the reviewer's own hand. Reviewer 2's final pass left three: a count ("all but one paired test" for what is all but three), an unmarked elision inside a quotation, and a paragraph locator within §5. Reviewer 1's left two: the full stage's per-run rows cited to the independent-arms table when they are in the ablation table, and a quoted fragment ("every rule sentence intact") attached to the arm whose wording is "every other rule sentence intact". Reviewer 3's third pass returned clean. In every case the checker saw only its own single draft.
