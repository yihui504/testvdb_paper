## Reviewer 1: Domain Expert

**Overall Recommendation:** Accept

### Summary

The paper asks how an LLM-based confirmation stage decides whether a candidate defect in a vector
database management system is real, and what its errors are made of. Its material is a mining
campaign against Milvus, Qdrant and Weaviate: 81 adjudicated submissions, of which maintainers
confirmed 51 and merged fixes for 23, drawn from 16 of the 19 versions the ledger covers. Two
measurement studies are built around that pool. The first audits what the confirmation stage reads:
each of the 134 (constraint, cited-page) pairs the case packages carry, as the pipeline produced
them, is checked against the page it cites, splitting into 18 supported as cited, 58 mis-anchored
(source-file or landing-page citations, re-anchored to version-pinned documentation) and 58 with no
support on the cited page. The same audit found two channels through which material the stage was
forbidden to read had reached it, both repaired, with the affected cases re-judged and all reported
rates recomputed on the cleaned pool.

The second study classifies the deployed stage's 243 judgments
on the primary backbone by the clause that closes each judgment. Contract refutation, which carries
no evidence requirement, closes 50 and is wrong on 24 of them; the verbatim-guarded by-design clause
closes 19 and is right 17 times; 24 of the stage's 30 incorrect closures to False-Positive come from
the unguarded clause. A replay that routes contract refutation rather than closing on it recovers
seven true bugs for nine false-positive interceptions under the deployment's counting convention and
changes nothing under a forced-verdict reading. The paper also prices the deployed stage against a
flat judge under both readings across twelve configurations, reports a second model backbone on
which the clause pattern does not reproduce, runs the released crash-oriented VDBMS fuzzer against
the same instance for 0 oracle anomalies, and reports four defects in its own dispatches, the
voiding of its detection-ability experiment, and the limits of its own counting convention.

### Core Strengths

- **S1:** The audit of the oracle's *input* is the paper's most transferable contribution: a
  three-way census of 134 cited pairs (18 / 58 / 58), the two mechanisms behind it, the
  expectation-framing check on the rebuilt set, and the two leak repairs the audit forced — see 2.1,
  4.1.
- **S2:** The clause census's cross-tab is what turns its headline number from a correlation into an
  argument: the 24 wrong contract-refutation closures fall on cases the audit judged *supported*
  (20), or weak-evidence (4), and on none of the 18 cases the audit left without documented evidence
  — see 2.2.
- **S3:** The twelve-configuration study is statistically correct and prices its own convention
  everywhere: nineteen printed exact-McNemar pairs recompute exactly, the derived rates and the
  net/F1 arithmetic reproduce from the printed counts, and the Holm family accounting is right — see
  2.3, 4.1.
- **S4:** Section 5 hands over four practices with measured backing — audit what the oracle reads;
  put the guard where the error mass is; price the deferral channel and the contrast, not just the
  level; check the dispatch before re-architecting the judge — see 3.1, 3.2.
- **S5:** Scope discipline is unusual: the paper names the one unjudgeable case and prices the point
  eleven configurations get for it, states where its own dispatch defines the perspectives twice,
  and reports the second backbone's non-replication in the abstract rather than in a footnote — see
  1.2, 2.4.

### Core Weaknesses

- **W1:** The signature four-perspective contrast changes five things at once, and under forced
  verdicts the two arms are equal *in count* while their decided sets overlap only 22/27 and 23/26;
  with an interval that excludes only effects above roughly eleven points, the paper cannot say
  whether the perspectives help, hurt or do nothing on the primary backbone — see 2.5.
- **W2:** The census — the paper's title-bearing result — is a single-backbone observation that does
  not reproduce on the second backbone (there the unguarded clause supplies 50% of incorrect
  False-Positive closures, and the *guarded* clause is the inaccurate one), so the prescription is
  bounded advice rather than a property of the protocol — see 2.6.
- **W3:** Missing related work: the paper's central conclusion is a statement about abstention, and
  it cites none of the selective-prediction / learning-to-defer line that formalises exactly this
  coverage-versus-risk accounting — see 3.3.
- **W4:** The paper's most novel measurement rests on a single-reader classification whose row-level
  accounting "does not fully reconcile", and the judge's behaviour on the as-produced versus the
  rebuilt material — the comparison Section 5's advice implies is knowable — is never measured — see
  2.8, 2.9.

### Detailed Assessment

1. **Importance & Scope** — Excellent
   - **1.1** The problem is established with quantitative context rather than assertion: Section 2
     grounds the "silent majority" in the VDBMS bug study's symptom split (functional failures
     dominant, crashes a minority class) and in VDBFuzz's own crash-only oracle, then Table 1
     positions six oracle families by *where each anchors its expectation* and isolates the
     residual — untagged, system-level behavioural prose. I checked the two load-bearing citations
     against the cached competitors: the bug study does report functional failure as the dominant
     symptom with crash second, and VDBFuzz self-describes as crash-only. The effect is that the
     paper's target is not a gap the authors assert but one a reader can see the edges of.
   - **1.2** Scope is stated with unusual precision, which is what makes the paper's several
     refusals legible: 81 adjudicated submissions (51 maintainer-confirmed, 30 adjudicated by the
     authors), a 132-row ledger that also holds 49 unadjudicated and 2 withdrawn submissions, 16
     versions for the 81 against the ledger's 19, one unjudgeable case named individually, two
     backbones with serving aliases and no pinned weights, and a census scoped to the primary
     backbone only. I could not find a headline number whose scope, pool or counting convention is
     left for the reader to guess; the "under what assumptions" half of this criterion is met.
   - **1.3 [minor, fixable]** The title and opening promise more than the body measures: the title
     says "Detecting Documentation–Implementation Bugs" and the abstract opens on what detectors
     miss, but the paper's own position is that the runs which would have measured detection were
     voided and that what remains is a record of submissions and adjudication plus two audits. A
     title and first paragraph pitched at the actual deliverable (a record, an audit, a census)
     would remove a reader's first wrong expectation.

2. **Insights & Evidence** — Adequate
   - **2.1** The pair audit (Section 4.3) is a genuinely new measurement of a step every pipeline in
     this line performs and none reports: the three-way split of 134 cited pairs, the two dominant
     mechanisms (version drift from a fixed-version augmentation contract; constraints that exist as
     prose but not as documented values), the case-level companion object (12 headline assertions,
     all acted on: 5 supported, 3 dropped, 2 over-strong, 2 weak-evidence), and the
     expectation-framing check on the rebuilt set (zero of 81 packages carry a sentence framed as an
     expectation; all 19 apparent hits inspected and all are quoted server responses). The
     arithmetic closes (18+58+58=134; each 43.3% share is of 134). This is the result a reader will
     cite.
   - **2.2** The census's cross-tab (Section 4.5) is the strongest analytic move in the paper. The
     audit and the census admit a single alternative explanation — the 24 bad closures are just the
     58 unsupported pairs failing a mechanical containment check — and the cross-tab kills it: the
     wrong closures fall on cases whose rebuilt packages *do* carry documented evidence (20 of them,
     at a rate I make out to be 20 of 180 judgments on those cases), on 4 of the weak-evidence
     cases, and on none of the 18 cases the audit left without documented evidence. Nothing in my
     own reading of the numbers reopens that reading.
   - **2.3** The statistical reporting is correct at a level I could verify independently. I
     recomputed every exact-McNemar value the paper prints beside a discordant pair (nineteen pairs)
     and all are right, including the asymmetric ones (2/6 → 0.2891; 9/6 → 0.6072; 4/4 → 1.0;
     11/2 → 0.0225; 2/14 → 0.0042). The derived quantities reproduce from printed counts: the
     conclusion's rate pairs are 30/51, 39/51, 27/51 and 41/51; the two source-only configurations'
     0.706 and 0.725 are 36 and 37 of 51; the "net is 30 either way" check is 39−9 and 48−18; and
     the F1 figures (0.788 with source, 0.821 without) follow from the stated TP/FP counts to three
     decimals. The Holm accounting is also right: the four surviving p-values do fall below
     α/10…α/7 and the fifth (0.0225) above α/6. For a paper this number-dense, that is worth saying.
   - **2.4** The disclosures are load-bearing rather than decorative, and the paper puts them where
     they bite: the second backbone's non-replication is in the abstract, Section 1 and the threats
     section; the four dispatch defects are reported rather than quietly repaired, with the honest
     observation that none was found by the authors' own audit; the two leak repairs are quantified
     in the direction that costs the authors (the controls' leaked false positives rise, and the
     deployed configuration would have read 41/51 without the repair); and the counting convention is
     priced at the arms and at the headline contrast. This is the behaviour that makes the rest of
     the evidence usable.
   - **2.5 [major, fixable]** The design cannot answer the causal question the paper poses. Section
     4.4 states that the four-perspective contrast "changes five things", and the flat-to-deployed
     contrast bundles the verdict space with the routing rule; the result is that the paper's
     organizational conclusion — the organization changes *which* cases are decided, not how many —
     rests on two arms differing in five respects, and on an equality of counts (27 vs 27, 26 vs 26
     under forced verdicts) whose interval on the primary backbone excludes only effects larger than
     about eleven points, so equivalence is asserted rather than demonstrated. The set-overlap
     figures (22/27, 23/26) are a real finding; the claim that the perspectives are worth nothing on
     this backbone is not established by them. The fix is constructible with the study's own
     machinery (perspectives without cognition access; cognition without perspectives), and the
     paper should either run at least one de-confounded arm or narrow the claim to what the bundled
     comparison licenses.
   - **2.6 [major, fixable]** The census is one backbone deep, and the paper is explicit that the
     pattern does not reproduce: on the second backbone the unguarded clause supplies 24 of 48
     incorrect closures (50% rather than 80%), the guarded clause closes 50 and is wrong 22 times,
     and — because the deployed dispatch prints two perspective definitions with C and D exchanged,
     and 217 of 243 recorded D cells there use the source vocabulary against 98 of 243 on the
     primary — the letters may not denote the same perspective on the two backbones. The mitigating
     evidence is good (on the primary, each lettered perspective's cells carry its own vocabulary
     and no other across all 243 judgments; the 24 is invariant across the two printed aggregation
     rules; the count rests on maintainer labels, not on the authors' 30 negatives). But the honest
     reading is that "the guard protects the clause that was already clean" is a primary-backbone
     observation, and the paper says so; a corrected dispatch re-run on the second backbone would
     settle whether the reversal is real or a vocabulary artefact, and without it the prescription
     stays advice.
   - **2.7 [minor, fixable]** The counting convention is author-chosen and one of its consequences is
     not stripped out: under the convention a routed case is credited, and `milvus_001` — never
     captured, documentation segment retired — is routed by eleven of the twelve configurations, so
     the deployed stage's 39/51 includes a point for a case nobody could judge. The paper discloses
     this precisely, and reports the forced reading throughout, but it never prints the deployed
     numbers with that case removed, which is a one-line sensitivity and the first thing a skeptical
     reader will compute.
   - **2.8 [minor, fixable]** The pair audit — the novel measurement — is a single-reader
     classification with no second coder and, by the paper's own threats section, its row-level
     accounting "does not fully reconcile in our own report". The pair-level rates that are printed
     do reconcile and ship as verdicts, so this is not a threat to the number; but for a contribution
     whose selling point is measurement discipline, the unreconciled ledger should be explained in
     the body (or reconciled) rather than flagged only as an open item.
   - **2.9 [minor, fixable]** Section 5's advice outruns the design in one direction: "a sample of
     pairs against their cited pages suffices to know whether your confirmation rate is a property
     of your judge or of your materials." In this study the audited material was replaced *before*
     any judge read it, so there is no as-produced-versus-rebuilt comparison anywhere in the paper —
     a reader cannot tell how much of the judges' behaviour the 43.3% would have explained. The
     cross-tab in 2.2 partially does this job for the clause, and the honest version of the claim
     ("this is cheap to measure") is defensible; as phrased it promises a variance decomposition the
     study does not contain.
   - **2.10 [minor, fixable]** The yield claim's provenance stops one step short. The paper states
     that the detection-ability runs were voided for dispatch-discipline violations and that "a
     substantial share of the 81 adjudicated submissions sits on versions that experiment covered",
     but not what share of the 81 was *produced* by the voided dispatches. The adjudication logic
     ("maintainers are external to the violated protocol") is sound — a maintainer-confirmed bug is
     real however it was found — but a reader weighing the campaign contribution needs the share,
     not only the version overlap.

3. **Perspective** — Excellent
   - **3.1** The four practices in Section 5 are the paper's most portable output, and each is tied
     to a measured finding rather than offered as advice: audit the oracle's input (with a base rate,
     43.3%, and the observation that the two leak channels came out of the same audit); instrument
     the judge by the clause that closes each judgment (which located the error mass in one place);
     price deferral and the contrast rather than the level (where the paper shows its own headline
     gain falling by two thirds under hand-pricing); and check the dispatch before re-architecting
     the judge (where a one-line schema repair moved five of the headline nine bugs, and none of the
     four defects was found by the authors' own audit). Practitioners building LLM-judged pipelines
     in any domain can act on all four.
   - **3.2** The paper's sharpest lesson is framed as a result rather than a caveat: under a
     convention that counts routed cases as confirmed, a routing rule's effect and the routing rate
     are the same quantity, so the "improvement" is the convention, not the judge. Stating this and
     then reporting both readings is the kind of evaluation discipline that transfers to any
     pipeline that escalates cases to humans.
   - **3.3 [minor, fixable]** Related-work coverage: the conclusion — that what a judge confirms is
     decided less by how it is organised than by how it accounts for the cases it refuses to decide —
     is the coverage-versus-risk statement of selective prediction and learning-to-defer, and the
     paper cites none of that line. What I could verify this session (abstract-level, via web search,
     so I mark the pointer provisional): "Trust or Escalate: LLM Judges with Provable Guarantees for
     Human Agreement" (Jung et al., ICLR 2025) gives judge-confidence-based selective evaluation with
     human-agreement guarantees and escalation, and the same search surfaced conformal abstention
     work and the classical deferral line (Madras et al. 2018; Mozannar & Sontag 2020). A positioning
     paragraph would cost little and would convert the paper's strongest lesson from an apparent
     discovery into a measured instance — which is the contribution it actually is. If the authors
     intend the deferral result as a general finding, this becomes load-bearing rather than
     cosmetic; as presented (an audit of one deployment's accounting) it is a gap, not a flaw.
   - **3.4 [minor, fixable]** One competitor characterisation is overstated. Table 1's
     structured-source row asserts that these oracles "cannot report a documentation–code gap as a
     defect"; that holds for MASTOR, which takes the implementation as its authority (its own
     self-stated limitation is that it cannot detect violations of requirements not reflected in
     code), but not for the row's other members: SATORI's own reported bug categories include
     specification–response mismatches, i.e. documentation–implementation inconsistency on the
     response side, detected from natural-language OpenAPI field descriptions. The paper's actual
     and correct distinction — anchor type and granularity (per-field structured metadata, no
     cross-request state coupling) rather than "no documentation gap" — is stated in the paragraph
     below the table; the table's reason column should be aligned with it.

4. **Verifiability** — Excellent
   - **4.1** The declared package is specific and complete enough to follow the work: the pool, the
     frozen per-run verdicts of all twelve configurations, the packages the study read, the dispatch
     texts, English renderings of the two judging prompts under `rq2/prompts/`, the pair-audit
     verdicts, the adjudication worksheet and the blind passes, and five named analysis scripts with
     a statement of what each recomputes (including `clause_tally.py second` for the second
     backbone's census). Re-judged cells ship beside the pre-repair state, so either pool can be
     reconstructed. I judged the link from the text rather than by fetching it: the URL is declared
     but my environment refused the anonymous-host fetch, so I could not confirm reachability, and I
     record that as the basis of this rating rather than implying I opened it.
   - **4.2 [minor, fixable]** Four supporting analyses are explicitly not scripted (the catch-all
     composition, the expectation-framing check, the C row's evidence classification, and the
     per-perspective cell vocabularies), the fix-PR characterisation is outside the shipped artifact,
     and the rebuild's row-level accounting does not reconcile. Each is flagged, which is the right
     behaviour, but it means a reader cannot independently recompute those numbers, and one of them
     (the catch-all composition) carries a paragraph of the census's interpretation.
   - **4.3 [minor, fixable]** The models are the least verifiable part of the method: both backbones
     are "serving aliases without pinned weights", and the second "varies with the dispatching
     session rather than being randomized". The frozen re-analysis is verifiable; the pipeline run is
     not attributable to a defined model. If the aliases' identities and dates can be recovered, put
     them in the artifact and say so, since that is what makes the two-backbone comparison
     interpretable.

5. **Presentation** — Adequate
   - **5.1** Structure is sound: the approach section names what each stage is *for* in the
     measurement, the evaluation carries its own methodology subsection before any result, and the
     threats section is unusually complete and mirrors the criteria a skeptical reader would apply.
     Tables are built to defend themselves — Table 3's caption pre-empts the misreading that the two
     43.3% shares combine, and Table 4's rows sum to the 243 judgments with the right/wrong columns
     reconciling against the 51/30 pool. LaTeX hygiene is clean (the source I read contains no
     comment markers or disabled blocks).
   - **5.2 [minor, fixable]** Within a single contrast the prose subject and the printed order do
     not agree, so the direction has to be re-derived sentence by sentence. Section 4.1 defines a/b
     by "the arm whose count is printed first", and Section 4.4 introduces the four-perspective
     contrast with the four-perspective arm as its subject, but prints the other arm first — 51 vs.
     48 (9/6) on the primary, where 51 belongs to the rule-bearing flat judge, and 41 vs. 30 (12/1)
     on the second. The order is at least consistent between the two backbones, so nothing is
     misreported; the trip hazard is that a reader who takes the numbers in the subject's order
     reverses the direction, and the primary recall row ("39 vs. 39") carries no recoverable order at
     all. Name the arms in the parentheses.
   - **5.3 [minor, fixable]** Two load-bearing rates are printed without their base: "20 fall on
     cases whose rebuilt packages carry documented evidence (rate 0.11)" is a per-judgment rate (20
     of 180), not the per-case rate the sentence structure suggests (20 of 60), and Section 4.6's
     "three anomalies apiece" over "152 lines" does not parse cleanly (152 lines × 3 apiece = 456
     reported entries, which is not what the surrounding audit of the zero describes). State the
     denominator, or drop the appositional number.
   - **5.4 [minor, fixable]** One sentence is unparseable without the author's memory: "The re-judged
     cells were merged into those runs and the pool reduced as before" (Section 4.1) — "the pool
     reduced" has no antecedent, and this is the paragraph that has to convince a reader that every
     rate is computed on the cleaned pool.
   - **5.5 [minor, fixable]** Arm naming multiplies across sections: the full stage is also "the
     deployed stage", the rule-bearing flat judge is also "the rule-bearing control" (and one
     sentence warns that this control "is not the deployed stage"), and the flat-plus-schema arm
     appears as "the schema-corrected control" and "the schema-repaired control". Table 2 gives the
     numbered configurations but no legend for its bullet columns. A one-line glossary mapping
     shorthand to table row would remove an entire class of misreads.
   - **5.6 [minor, fixable]** The four perspectives are presented in three orderings and two
     vocabularies: Section 3.5 introduces A/B/C/D (contract, objective, elegance, cognition), Section
     4.5's legend gives the firing order A, B, D, C, Table 4 is grouped by outcome, and the
     vocabulary question (source-derived versus cognition values) is discussed at length without a
     printed value list. The paper is admirably transparent about why the vocabularies matter; a
     single canonical naming table would make that transparency pay off.
   - **5.7 [minor, fixable]** The abstract is a dense block in which each of the three bolded results
     carries its own scope caveat, so the paper's strongest concrete findings (the cross-tab, the
     exact statistics, the schema-repair result) are invisible at the abstract level while the
     hedges are not. Trading one hedge for one number would make the abstract do more work.

### Questions for Authors

- **Q1:** Were the schema-fix, `flat + aggregation`, and second-backbone `flat + aggregation` arms
  (configurations 3, 4 and 10) dispatched before or after the embedded-cognition strip? Section 4.1
  names only the second backbone's flat judge as partially post-strip, but those three are flat-family
  arms whose dispatches also forbid the cognition section. If they read the leaky packages, the claim
  that every reported rate is computed on the cleaned pool needs a qualification; if they did not, one
  sentence closes the gap — this would move **4.2** up.
- **Q2:** How sensitive is the census to the 98 source-vocabulary D cells on the primary backbone?
  They fall through to the catch-all by classification rather than by the judge's reasoning. If any of
  them are refutations that the mis-declared schema forced into the wrong vocabulary, the paper's 80%
  understates the unguarded error mass; if they are largely inert, the census is robust to its own
  instrument defect. Either answer sharpens **2.6**.
- **Q3:** Can the authors report the judge's behaviour on the as-produced packages against the rebuilt
  ones — at least for the 12 case-level main assertions the audit acted on and the 58 re-anchored
  pairs? That is the comparison that converts Section 5's advice into a measurement, and it would move
  **2.9** up (or let the advice be weakened with evidence).
- **Q4:** Can at least one de-confounded four-perspective comparison be supplied on the primary
  backbone — perspectives without cognition access, or cognition without perspectives? Two arms would
  decide whether "the organization changes which cases, not how many" survives, and would move
  **2.5** up; as printed, that claim is the paper's most quotable and its least isolated.
- **Q5:** What share of the 81 adjudicated submissions was produced by the voided detection-ability
  dispatches, and does the yield claim change if that share is excluded? The adjudication argument is
  sound, but a reader weighing the campaign contribution cannot currently separate submissions found
  under the violated discipline from those found without it — this would settle **2.10**.


---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Accept

### Summary

The paper reports an experience study of documentation--implementation bugs in vector database management systems (VDBMSs): cases where a system silently accepts an input or behaves in a way its API documentation does not describe, and therefore emits no crash signal. It describes a four-stage LLM-agent pipeline---specification extraction from vendor documentation, strategy-bound probe generation, sandboxed execution against a pinned instance, and a confirmation stage that splits evidence assembly from cross-examination---and then reports three bodies of measurement. First, a mining campaign across Milvus, Qdrant and Weaviate whose ledger holds 132 rows for these systems, 81 of them adjudicated by maintainers (51 confirmed, 23 with merged fixes); the runs that would have measured per-version detection ability were voided for dispatch-discipline violations, so no detection rate is claimed. Second, an audit of the 134 (constraint, cited-page) pairs the confirmation stage's packages carry: 18 supported as cited, 58 citing a source file or landing page and re-anchored, and 58 unsupported by the page they cite. Third, a clause-level census of the 243 judgments the deployed confirmation stage produced (81 cases, three runs each, primary backbone): the unguarded contract-refutation clause closes 50 judgments and 24 of them fall on maintainer-confirmed bugs, while the verbatim-guarded by-design clause closes 19 and is right 17 times; routing the former to human review rather than closing on it would recover seven true bugs for nine additional leaked false positives under the deployment's counting convention, and nothing under a forced reading.

The paper additionally re-adjudicates the 81 cases under twelve judge configurations on two model backbones, prices the counting convention (a routed case counts as confirmed) at every contrast by reporting forced and, where ruled, hand-adjudicated readings beside it, reports four defects in its own dispatches rather than repairing them quietly, runs the released VDBFuzz template set against Qdrant as a crash-oracle baseline (zero oracle anomalies), and states its own limits---including that the clause census does not reproduce on the second backbone and that two exchanged perspective definitions in the dispatch mean the two censuses may not be comparable.

### Core Strengths

- **S1:** A first-of-its-kind, pair-level measurement of the distillation step every documentation-derived-oracle pipeline performs and none reports, with the two dominant mechanisms (version drift; conceptual-only documentation) named and the rebuilt set checked for expectation framing. --- see 2.1
- **S2:** The clause census is the paper's best evidential work: its load-bearing count (24 of 50 contract refutations fall on true bugs) is computed on maintainer labels alone, shown invariant across the two aggregation rules the dispatch prints, and separated from the pair audit by a cross-tab. --- see 2.2
- **S3:** The pricing discipline keeps every headline honest: contrasts are reported under the deployment convention, the forced reading and (where ruled) the hand-adjudicated reading, with floors, intervals, and an explicit "suggested, not established"; the counts and statistics I recomputed are internally consistent. --- see 2.3
- **S4:** Transferable lessons tied to the measurements, including the candid reporting of four defects in the authors' own dispatches and the observation that none was found by their own audit. --- see 3.1

### Core Weaknesses

- **W1:** The census---the paper's claim---is single-backbone: it does not reproduce on the second backbone (50% rather than 80%), and the dispatch's exchanged perspective definitions bound even the comparison, so the generality of "the protocol guards the clean clause" is limited. --- see 2.4, 3.3
- **W2:** Verifiability trails the paper's own standard at exactly the claim-carrying analyses: the census's sub-analyses (C-row evidence classification, catch-all composition, per-perspective cell vocabularies) are printed but not scripted, and the row-level rebuild accounting is disclosed as not reconciling. --- see 4.3, 4.4
- **W3:** Bookkeeping slips around the statistics: "Sixteen paired tests appear below" against the twenty p-values printed in Section 4.4 (by my count), and a Holm family choice that is never justified and that decides which of the recall-level contrasts count as significant. --- see 2.5, 2.6
- **W4:** The highest-value passages are the hardest to read: direction words reused with opposite polarity, rates printed without denominators, and arm identities that must be tracked across five near-identically named configurations. --- see 5.2, 5.3, 5.4

### Detailed Assessment

1. **Importance & Scope** --- Excellent
   - **1.1** The problem is important and its context is well established. Section 2 grounds the target in the empirical record: the VDBMS bug study finds functional failure the dominant symptom class (the cached study: 57.3% functional failure against 15.1% crash), the one dedicated fuzzer reaches only the crash class by its own stated limitation, and the community roadmap names oracle definition as the open problem. The paper's residue---silent violations of documented contracts---is exactly that residual, which makes the target worth the effort, and the running examples (Milvus \#49823's `nprobe` bound, Qdrant \#10369's `lookup_from` size coupling) make the class concrete in one endpoint-level and one stateful shape.
   - **1.2** The scope statement is unusually disciplined and is maintained wherever a claim appears---abstract, introduction, Section 4.5, Threats: the ledger is a record of submissions and adjudication and not a per-run rate (the detection-ability runs were voided); recall levels are contrasts on a common pool, not operating performance; vector-search correctness is explicitly excluded in Section 2; the census is scoped to the primary backbone. For an experience report, pairing each claim with its scope of claim is the property I weigh most, and it is done here.

2. **Insights & Evidence** --- Excellent
   - **2.1** The pair-level audit (Section 4.3, Table 3) is the most transferable measurement in the paper. The authors audited the 134 deduplicated (constraint, cited-page) pairs the packages carried as produced---before the rebuild---against the page each cites at the version each claims, split them into supported-as-cited (18), re-anchored (58), and unsupported (58), and named the two mechanisms: version drift from a single fixed-version contract, and constraints that exist in prose but not as documented values. This measures the step that the oracle-authority survey shows the field reports qualitatively if at all ("58 studies flag it as a risk while 44 report observing it empirically"), and the rates are correctly hedged as this distiller on these three vendors' documentation.
   - **2.2** The clause census (Section 4.5, Table 4) is carefully constructed, and its robustness arguments are the evidence I trust most. The load-bearing count---24 of the 50 judgments closed by contract refutation fall on maintainer-confirmed bugs---rests only on the 51 maintainer labels, not on the authors' own negatives; it is invariant across the two aggregation rules the dispatch prints because contract refutation assigns False-Positive under both; it is preserved by the two leak repairs, which were applied before these judgments were recorded; and the cross-tab separates the census from the pair audit (20 of the 24 fall on cases whose rebuilt packages carry documented evidence, 4 on the three weak-evidence cases, none on the 18 without evidence), which is exactly the isolation needed to argue the clause is closing wrong rather than the material being defective. Identifying the lettered perspectives by their cell vocabulary (A/B/C clean; D split 145 cognition / 98 source) is the right response to the C/D exchange defect, and the paper draws the boundary honestly, including the two cases where C=Refuted rested on code structure its own red line does not admit.
   - **2.3** The pricing discipline is what keeps the headline honest. Every contrast is given under the deployment convention (a routed case counts as confirmed), the forced reading, and, where hand-ruled, a joint reading; the routing change is priced at nine under the convention and at three---a floor---under hand-adjudication of the routed queue; the four-perspective contrast is reported as equal forced counts with different case sets (intersecting in 22 of 27 and 23 of 26), and the source-withheld arm is reported as a tie on net true positives minus leaked false positives (30 either way, bootstrap CI $[-8,+8]$) and on $F_1$ rather than as a win. I recomputed what the text allows and everything agreed: every printed discordant-pair p-value reproduces as an exact McNemar value for its pair ($0/9\to0.0039$, $12/1\to0.0034$, $16/2\to0.0013$, and the $p<0.0001$ entries as bounds), the $\pm0.11$ interval matches a matched-pairs Wald computation for 4/4 at $n{=}51$, Table 4's rows sum to 243 with the correct 153/90 true-bug/negative split, and the $F_1$ and precision figures implied by the printed counts (0.788/0.821; 0.917) reproduce. I found no arithmetic error in the numbers the text states.
   - **2.4 [minor, unfixable]** The census does not generalize, and the paper knows it. On the second backbone, contract refutation closes 56 judgments with 24 of 48 incorrect false-positive closures (50% rather than 80%), and by-design---the guarded clause---closes 50 and is wrong 22 times, so the finding "the protocol guards the clause that is already clean" holds only on the backbone where it was measured. The paper states the non-reproduction in the abstract, Section 4.5, the Discussion, and Threats, and gives the reason the comparison is itself bounded (the dispatch defines the perspectives twice with C and D exchanged, and the D cells' vocabulary split differs sharply between backbones: 217 of 243 source-vocabulary judgments against 98 of 243). Because the scope is disclosed wherever the claim appears, the residual defect is generality rather than correctness, and it inheres in recorded data---no revision removes it.
   - **2.5 [minor, fixable]** Section 4.1 states "Sixteen paired tests appear below, ten of them at the recall level"; by my count Section 4.4 prints twenty p-values---ten recall-level and ten confirmed-set-level comparisons (schema-line repair, routing-rule step, the bundled contrast on each backbone, the deployed-versus-flat reference, the two four-perspective contrasts, the two secondary four-perspective contrasts, and evidence access, each at both levels). The Holm family of ten is unaffected, but in a paper whose credibility rests on counting discipline the count should be reconciled.
   - **2.6 [minor, fixable]** The Holm correction is run over the ten recall-level tests, and the paper does not say why that family is the right one. I checked the obvious alternative---a family of all twenty printed paired tests. There the second backbone's perspective contrast ($p{=}0.0034$) is the seventh smallest and still clears ($\alpha/14 = 0.00357$); the two recall-level $p{=}0.0039$ contrasts (the bundled contrast on the primary backbone and the evidence-access contrast) would not (they meet $\alpha/13 = 0.00385$). The family restriction is therefore defensible but consequential---it decides which recall-level results count as significant---so the paper should state the rationale, letting a reader reproduce the reasoning instead of taking the family on trust.
   - **2.7 [minor, fixable]** The pool's provenance is described qualitatively where a number matters. Section 4.2 says "a substantial share of the 81 adjudicated submissions sits on versions that experiment covered" by the runs voided for dispatch-discipline violations, and defends the ledger on the ground that maintainers are external to the violated protocol. The census's catch-all discussion leans on the pool base rate (63.0% true bugs) and the arms' levels are contrasts on this non-random pool, so the share---how many of the 81, and the version overlap---should be given.

3. **Perspective** --- Excellent
   - **3.1** The lessons (Section 5) are specific, tied to measurements, and transferable to anyone operating an LLM-judgment pipeline: audit the oracle's input and not only its verdicts (with the observation that a pair sample is cheap); put the evidence guard where the error mass is; price the deferral channel and the contrast, not just the level, because a counting convention that credits abstention pays for exactly the effects under study; check the dispatch before re-architecting the judge; and self-audit the stage against its printed rules---"that is a five-line script". The last lesson comes with the paper's most valuable admission: all four dispatch defects were found by outside readers, not by the authors' audit, which is stated as the limit of self-audit rather than as an excuse.
   - **3.2** Within the two lines I specialize in---documentation-derived oracles and LLM-judge organization---the positioning holds up against the competitors as fetched. Metamon is accurately described as the closest operational line: its consistency signal is an LLM judgment stabilized by metamorphic queries, and its own stated limitation is that no independent (non-LLM) evidence source is consulted---the self-reference the paper says its source grounding exists to break; its quoted profile (precision 0.722 / recall 0.480) is verbatim from that paper. Ma et al. is accurately described as measuring bias rather than accuracy, with debate amplifying bias after the first round and a meta-judge resisting it, so the paper's "adding perspectives is not a uniform correction" is a fair gloss rather than a stretch. VDBFuzz's crash-oracle-by-construction premise is the fuzzer's own stated limitation. The oracle-authority survey is fairly paraphrased. Scoped coverage searches in both lines surfaced no uncited work that changes the delta. The contribution the paper claims---not a new oracle but an audit of the oracle's input, plus a clause-level error census---is real, and the paper does not claim more.
   - **3.3 [minor, fixable]** The lesson "put the evidence guard where the error mass is" is stated more strongly than two backbones support. On the second backbone the pattern reverses: the unguarded clause supplies 50% of the incorrect false-positive closures rather than 80%, and the guarded by-design clause is wrong 22 of 50 times, so the prescription is a property of one deployment, not of the protocol. The Discussion does bound it ("advice about where to look rather than a property of the protocol"), but the one-line lesson as written generalizes a single-backbone pattern and should carry the second backbone's result inline.
   - **3.4 [minor, fixable]** Because the paper's lesson is that others should run the same audit, the audit itself should be stated as a procedure: what the single reader checked on each page (which asserted semantics, at which version), how "supported" was decided, and how much of the 134-pair pass was mechanical. As written, the three verdicts in Table 3 are one-line definitions, which is thin for a protocol the paper wants reused.

4. **Verifiability** --- Excellent
   - **4.1** The text is self-contained enough to follow and check the claims I tested. Discordant-pair counts and p-values are printed for every contrast; the counting convention and both alternative readings are defined before use; both leak repairs are specified with their re-judged configurations and the affected figures before and after (including the awkward ones, such as the deployed stage reading 41/51 pre-repair); and the census's scope and letter-identification argument are given in full. I could reconstruct the provenance of essentially every number in Section 4 from the text alone, and the recomputations I did agreed.
   - **4.2** The artifact is declared with its contents enumerated---pool, the frozen per-run verdicts of all twelve configurations, the packages the study read, the dispatch texts and judging prompts under `rq2/prompts/`, the pair-audit verdicts, the adjudication worksheet and blind passes, and five named analysis scripts under `rq2/analyses/`. I checked the link: it resolves to the service's repository endpoint and requires the service's sign-in (HTTP 401 to an unauthenticated client), so I could not verify the contents independently; the enumeration, the named scripts, and the statement that re-judged cases ship beside the untouched batches make the recomputation story concrete.
   - **4.3 [minor, fixable]** The census is the paper's claim, yet three of its constituent computations are "printed but not yet scripted": the C row's evidence classification (the fifteen/two/two split), the catch-all composition, and the per-perspective cell vocabularies on which the letter identification rests. The raw material---the recorded cells---ships, so this is convenience rather than substance; but for the section a reader will most want to re-check by hand, scripting these closes the gap between "recomputable from the artifact" and "recomputable for the census too".
   - **4.4 [minor, fixable]** Threats discloses that "the row-level accounting of the rebuild does not fully reconcile in our own report", and the paper prints the pair-level rates that do reconcile. The disclosure is right, but the unresolved accounting is exactly what would bound the audit's downstream effect (which rows the rebuilt packages actually changed for the judges); either ship the reconciliation or state which row-level claims the paper does not rely on.
   - **4.5 [minor, unfixable]** Both backbones are serving aliases without pinned weights, so the twelve configurations cannot be re-executed exactly. The paper's decision to ship the frozen verdicts and make claims about them mitigates this for checking but not for replication; it is disclosed in Section 4.1 and Threats, and no revision can remove it.

5. **Presentation** --- Adequate
   - **5.1** The structure is sound and the supporting apparatus does real work: the four-stage narrative with claim-first paragraph leads, one pipeline figure, and four tables whose captions preempt the reader's mistake (Table 3's warning that the two 43.3% shares are each of 134 is exactly what is needed). The section order---approach, evaluation, discussion, threats, related work---is the right one for an experience paper, and I found no language errors, no missing sections, and no broken references.
   - **5.2 [minor, fixable]** Direction words are reused with opposite polarity in load-bearing sentences. Section 4.4 says the stage "intercepts 21 of 30 false positives" (a good outcome) and then that withholding source "buys nine true bugs for nine false-positive interceptions" (a cost); the abstract and Section 4.5 use "nine false-positive interceptions" and "seven true bugs for nine interceptions" the same way. A reader has to stop and derive that "interceptions" here means false positives *lost* to routing. Write the cost direction as "nine additional leaked false positives".
   - **5.3 [minor, fixable]** Several rates are printed without a stated denominator or unit: Section 4.5's cross-tab gives "(rate 0.11)" and "(rate 0.00)" for wrong closures against evidence class---0.11 is consistent with judgment cells over the documented-evidence cases (20/180) and 0.00 with 0/54, but the reader must reconstruct that---and Section 4.1's suppression figures (0.467$\to$0.400) are only interpretable after finding the definition one paragraph earlier. State the unit each rate is over at first use.
   - **5.4 [minor, fixable]** Arm identities carry too much implicit state for prose. Five configurations whose names differ by one word ("flat judge", "flat $+$ schema fix", "flat $+$ aggregation", "full, no aggregation", "full stage") are contrasted across one paragraph series in Section 4.4, each with materials, red lines, and verdict space that differ; and the four-perspective contrast's five co-varying items are listed once and then referred to as "that label". A compact contrast table (arm pair, what changes, convention/forced readings) would let a reader check each comparison without re-deriving which arm is which.

### Questions for Authors

- **Q1:** How should a reader reconcile "Sixteen paired tests appear below" (Section 4.1) with the twenty printed p-values in Section 4.4? --- [intended effect: reconciling the count, or narrowing the sentence to the sixteen the authors actually count, would remove the bookkeeping discrepancy I flag in item 2.5; if instead some printed comparisons are not counted as tests, naming them would settle it.]
- **Q2:** What is the rationale for the Holm family being the ten recall-level tests rather than all paired tests printed? --- [intended effect: I checked the broader family in item 2.6; the second backbone's perspective contrast still clears it, but the two recall-level $p{=}0.0039$ contrasts would not, so the answer decides whether 2.6 stays a presentational gap or becomes a concern about which recall-level contrasts the paper calls significant.]
- **Q3:** Are the four perspectives intended as four independent signals about a case, or as a deliberately heterogeneous bundle (a containment check, an objective-rule list, a refutation guard, a retrieval corpus)? --- [intended effect: the answer bears on item 3.2's delta claim---if the bundle is deliberate, the difference from Ma et al.'s homogeneous judge ensembles should be stated as a difference in kind, not only in "currency".]
- **Q4:** Under the recommended guard the convention-level outcome is $+7$ true bugs and nine additional leaked false positives (precision falls from about 0.81 to about 0.72); would the authors report the counterfactual's precision or $F_1$ beside its recall? --- [intended effect: adding it would let a practitioner weigh item 2.2's prescription rather than only its recall gain.]
- **Q5:** What share of the 81 adjudicated submissions came from the campaigns whose detection runs were voided? --- [intended effect: the number would settle item 2.7 and let a reader judge whether the pool's 63.0% base rate---on which the census's catch-all reading depends---is a property of the systems or of the voided campaigns' materials.]


---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Accept

### Summary

The paper studies documentation--implementation bugs in three production vector database management systems (Milvus, Qdrant, Weaviate): cases where the system silently accepts an input, or produces a behaviour, that its own API documentation does not permit. It reports a four-stage pipeline in which a knowledge extractor crawls vendor documentation, a specification extractor emits constraint records with citations, attack agents turn those records into executable probes with inline oracle lines, a sandboxed executor runs the probes against pinned instances of the target, and a confirmation stage decides per candidate whether the observation is a defect. That last stage is the paper's object of study: an evidence builder assembles a five-section chain (document verification, execution evidence, contract grounding, chain trace, source grounding) and a chain auditor cross-examines it under four mechanical checks and, in the deployed form, four perspectives (A contract, B objective constraints, C behavioural elegance, D maintainer cognition), with a fixed aggregation order producing a three-valued verdict (Confirmed, False-Positive, Human-Review).

The paper reports three results. The campaign: 51 of 81 adjudicated submissions were maintainer-confirmed, of which 23 were fixed through merged PRs, against a ledger of 132 rows over 19 versions; the paper states repeatedly that this is a record of submissions and adjudication and not a per-run detection rate, because the runs that would have measured detection were voided for dispatch-discipline violations. The audit: of the 134 (constraint, cited-page) pairs the confirmation stage's packages carry, 18 were supported as cited, 58 cited a source file or an API landing page rather than the page documenting the constraint and were re-anchored, and 58 had no support on their cited page; the same audit exposed two channels through which forbidden material had reached the stage, both repaired with the affected cases re-judged, and every rate in the paper is computed on the cleaned pool. The census: classifying the deployed stage's 243 judgments (81 cases, three runs each) by the aggregation clause that closes them, contract refutation (no evidence requirement) closes 50 judgments and 24 of those are maintainer-confirmed bugs, while the verbatim-guarded by-design clause closes 19 and is right 17 times; the unguarded clause supplies 24 of the stage's 30 incorrect closures to False-Positive, and a replay that routes instead of closing on it recovers seven true bugs for nine released false positives under the deployment's counting convention and changes nothing under forced verdicts. The study is run as twelve judge configurations over a common frozen pool on two model backbones; on the four-perspective contrast the forced-verdict recall is identical on both backbones (27 vs 27 and 26 vs 26) while the decided sets overlap in only 22 of 27 and 23 of 26, and the large convention-level effect of the aggregation rule (0.588 to 0.765, and 0.529 to 0.804) is attributed by the authors to deferral rather than to better deciding. The census pattern does not reproduce on the second backbone, where by-design refutation is the error-dense clause.

### Core Strengths

- **S1:** A maintainer-validated campaign with auditable ground truth: 51 bugs confirmed and 23 fixed by merged PRs across three production systems, reported with unusually explicit limits on what the record does and does not measure — see 1.2, 2.4, 4.1
- **S2:** The census is separated from its most obvious confound by a cross-tabulation showing the wrong closures rest on material the audit judged *supported* (20 of 24 on documented-evidence cases, none on the 18 cases the audit left unsupported), which converts a correlation into a finding — see 2.1
- **S3:** The two evidence leaks are handled as a reported experiment rather than a quiet repair, including the disclosure that the repair moves the two full-family controls *against* the paper's own headline and the numbers for what the unrepaired pool would have shown — see 2.3
- **S4:** Transferable practical lessons, one of them — the deferral lesson — supported on both backbones: price the deferral channel rather than the accuracy level; audit the oracle's input, not only its output; check the dispatch before re-architecting the judge — see 3.1, 3.2, 3.3
- **S5:** Verifiability discipline: a complete artifact inventory with named scripts, and explicit marking of every number that is printed-but-not-scripted and every claim that sits outside the shipped artifact — see 4.1, 4.2, 4.3

### Core Weaknesses

- **W1:** The clause census — which the paper itself designates as its claim — is a single-backbone measurement whose second-backbone attempt produced the opposite pattern, and the non-reproduction cannot be interpreted because of a defect in the authors' own dispatch — see 2.5
- **W2:** The paper's practical prescription rests on a replay over frozen verdicts rather than on a re-judgment, so the measured payoff disappears entirely under the forced reading and no direct evidence is offered that a guarded judge would keep the seven bugs — see 2.6
- **W3:** The bundled contrast is reported in the Conclusion as the effect of "adding an aggregation rule" while the paper's own decomposition gives five of the nine bugs to a one-line schema repair, and on the second backbone no decomposition exists at all — see 2.7
- **W4:** The evidence base carries provenance limits that are disclosed but never quantified (author-adjudicated negatives, unquantified pre-submission screen, unquantified duplicate share, printed-but-unscripted supporting classifications) — see 2.8, 2.9, 2.10, 1.4

### Detailed Assessment

1. **Importance & Scope** — Excellent

   - **1.1** Section 2 and Table 1 do the contextual work well: the paper establishes that VDBMS failures are predominantly silent functional failures rather than crashes, that the one dedicated VDBMS fuzzer's oracle fires on a 5xx response or a failed request, and that the remaining oracle families anchor their expectations somewhere other than system-level API prose — intra-system differential variants compare an engine with itself, schemas bound fields without carrying cross-request behaviour, and the prose-reading tools (@tComment, JDoctor, DocTer, RBCTest, RESTInfer) work at field, method or parameter granularity. Each table row names a concrete representative and a structural reason. This is an unusually crisp statement of why a residual exists.

   - **1.2** The scope is stated at the granularity at which each claim is actually supported, and restated where a reader might over-read: the campaign is "a record of submissions and adjudication, not a per-run detection rate" with the void record shipped (Sections 1, 4.2, 6); the census is explicitly scoped to the primary backbone (the abstract, the third introduction bullet, Sections 4.5, 6 and 8); and the audit refuses to generalise its rates beyond "this distiller on these three vendors' documentation" (Sections 4.3, 6). A reader can therefore tell, for every headline number, what population it is a statement about. For an experience paper this is the property that most determines whether the findings can be used.

   - **1.3 [minor, fixable]** The load-bearing context claim — that *no* oracle family takes its expectation from "untagged, system-level behavioural prose" (Section 2, last paragraph of Table 1's discussion) — is asserted from a table the authors construct; the rows are their summaries of other systems' designs rather than measurements taken here, and the claim is what makes the residual a gap rather than a preference. Section 7 is more careful ("to our knowledge no prior work measures the reliability of a documentation-derived oracle on an adjudicated pool of VDBMS cases"), and the paper would be better if Section 2's framing were written at Section 7's scope. I flag this part of the rating as **provisional**: I surveyed no related work for this review, I take the characterisations of the named tools in Table 1 and Section 7 as the paper states them rather than from the works themselves, and I take no position on whether any competitor is missing.

   - **1.4 [minor, fixable]** The pool's scope boundary is named but not quantified. Section 6 describes the pool as a "submission-filtered subset of one pipeline's output", and Section 4.1 gives the pool as 81 cases without the number of candidates the pipeline produced before the authors' screening step. Because the paper's headline is a ratio ("51 of 81 adjudicated submissions"), a reader cannot tell how much of it reflects the detector and how much reflects the screen. The paper's caveat that it is "not a per-run detection rate" addresses the per-version runs that were voided, not the screen. Report the screened-out count and the screening criteria.

2. **Insights & Evidence** — Adequate

   - **2.1** Section 4.5 anticipates and tests the objection that would otherwise wreck the census: since contract refutation is a mechanical containment check and the pair audit found 58 of 134 cited pairs unsupported, the 24 wrong closures could simply be defective rows failing that check rather than a protocol closing wrong. The cross-tab separates the two — of the 24, 20 fall on cases whose rebuilt packages carry documented evidence, 4 on the three weak-evidence cases, and none on the eighteen cases the audit left without documented evidence. That is the right experiment to run on your own finding and it is run.

   - **2.2** The evidence base for the campaign is of the kind an experience paper should want: 51 bugs confirmed by maintainers external to the protocol, with labels, closures and merged fix PRs, over three systems and 15 versions, in a ledger whose row accounting reconciles (81 adjudicated + 49 unadjudicated + 2 withdrawn = 132; 43 + 28 + 10 = 81 cases; 29 + 14 + 8 = 51 confirmed; 11 + 9 + 3 = 23 fixed; 14 + 14 + 2 = 30 negatives; 23 + 18 + 7 + 3 = 51 dispositions). I checked these and the census arithmetic (61 + 21 + 7 + 50 + 19 + 16 + 69 = 243; the three False-Positive-assigning clauses close 85 judgments containing 30 wrong, of which contract refutation supplies 24, i.e. 80%); they reconcile, which is not something I can say of most experience reports with this many derived counts.

   - **2.3** The two leak repairs are treated as a measurement event rather than housekeeping (Section 4.1): the paper names both channels, the five configurations affected on the first repair, the six runs missed on the second, and the re-judge protocol, and then reports that the repair moves the two full-family controls *against* its own interest — suppression falls 0.467 to 0.400 and 0.933 to 0.900, false positives leak by two and one — and gives the counterfactual number a reader would otherwise have to compute (41/51 with a confirmed set of 41 + 6 rather than 39/51 and 39 + 9). It also states plainly that the second repair was applied to the deployed stage but not to two controls, and that raw generations ship so either pool can be reconstructed.

   - **2.4** The result the Conclusion actually rests on is supported on both backbones: the four-perspective organization leaves forced-verdict recall unchanged (27 vs 27 and 26 vs 26) while the decided cases overlap in only 22 of 27 and 23 of 26, whereas the aggregation-and-routing change moves the convention-level counts on both backbones. The paper also refuses to present the deferral gain as better deciding ("we say so rather than presenting the difference as the rule getting better at deciding", Section 8). The 2x2-style design (flat judge vs rule-bearing judge, with and without perspectives) is a genuinely informative piece of study construction, and the sources of the residual asymmetry are disclosed in Section 4.1.

   - **2.5 [major, fixable]** The clause census — designated by Section 4.4 as "the paper's claim" — is a single-backbone result, and the second-backbone attempt produced the opposite pattern: there contract refutation closes 56 judgments and by-design refutation closes 50 of which 22 are wrong, and the unguarded clause supplies 24 of 48 incorrect False-Positive closures, "50% rather than 80%" (Section 4.5). The paper cannot interpret that non-reproduction because of its own defect: the deployed dispatch defines the four perspectives twice with C and D exchanged, and the recorded D cells use the source vocabulary in 217 of 243 second-backbone judgments against 98 of 243 on the primary, so the letters may not denote the same perspective across backbones. The paper scopes the claim correctly and applies the scope in the abstract, the introduction, the census, the threats section and the conclusion — this is not overreach — but the consequence is that the paper's central empirical measurement rests on one serving alias of one model family with no clean replication signal in either direction. A revision can address this without re-running the target: a second census taken under a dispatch whose perspective definitions are unambiguous would say whether the pattern is backbone-dependent or letter-confounded.

   - **2.6 [major, fixable]** The practical prescription is priced by replay rather than by re-judgment. Section 4.5 routes contract refutation to human review "everything else held at the recorded perspective values" and reports seven true bugs for nine released false positives under the convention, explicitly noting that "what cannot be computed from frozen data is whether a judge re-adjudicating those refutations under a verbatim-evidence guard would reach the same place", and that forced, the same replay changes nothing. So the paper's actionable claim — put the evidence guard where the error mass is (Section 5) — currently rests on arithmetic over recorded cells; its only empirical support is that the guarded clause is accurate where it fires (17 of 19) and that the unguarded clause's closures fall on supported material. The diagnosis (24 wrong closures, and where they land) is solid and convention-independent; the prescription is not yet directly evidenced. Re-judging the 15 cases the clause closes, under the guard, on the shipped materials would convert it into a measurement and would also settle whether the seven survive.

   - **2.7 [major, fixable]** The bundled contrast is attributed to the rule in the paper's headline sentence while its own decomposition gives most of the credit elsewhere. Section 4.4 decomposes the primary bundle as flat 30 → schema-repaired 35 → rule-bearing 39, so a one-line output-schema repair carries five of the nine bugs; Section 5 says so explicitly ("A one-line schema repair moved five of the headline nine bugs"). Yet the Conclusion states that "adding an aggregation rule that lets it route a case to human review rather than close it raises recall on both backbones (0.588 to 0.765 ...; 0.529 to 0.804 ...)", where the second figure is the same two-edit bundle and — unlike the primary — has no schema-repaired control on that backbone at all (Section 4.4 notes the split is unmeasured there). The second-backbone "replication" therefore replicates a bundle whose primary decomposition assigns the majority of its effect to the schema edit, not to the rule. Either restate the conclusion at the bundle's scope, or add the missing second-backbone schema-only arm so the rule's own effect is measured twice.

   - **2.8 [minor, fixable]** How much of the yield is rediscovery is not quantified. Section 4.2 records that 3 of the 51 confirmed bugs are "tracked as duplicates"; the paper does not say whether those duplicate the authors' own earlier submissions or pre-existing upstream reports, and the confirmation stage's perspective D reads a corpus distilled from the target's own historical issues and merged PRs (Section 3.5), so a reader will reasonably ask about the overlap. A count of the confirmed bugs that were already open upstream before submission would settle it.

   - **2.9 [minor, fixable]** The 30 negatives are the denominator of every suppression figure and the entire cost side of the "seven for nine" price, and their provenance is thinner than the benefit side's. Section 4.1 says they were "adjudicated by us against the maintainers' disposition where available"; Section 6 says only that they were "adjudicated by us". The paper is careful to note that the load-bearing census count (24) is computed on maintainer-confirmed labels and so does not rest on these — but the nine released false positives in the counterfactual do. State how many of the 30 carry a maintainer disposition and how many are pure author calls.

   - **2.10 [minor, fixable]** Section 4.5's claim that the judge applies the verbatim-intent requirement non-uniformly — the observation that `milvus_011`'s and `milvus_012`'s other runs recorded weak refutations *with* reasons, and that "the verbatim-evidence requirement is therefore not applied uniformly by the judge" — rests on a hand classification of the 19 C=Refuted cells that Section 4.1 lists among the analyses "printed but not yet scripted". The interpretive claim is interesting and specific; it would be stronger if the classification behind it were scripted like the four analyses that are.

3. **Perspective** — Excellent

   - **3.1** Section 5's lessons are each tied to a named measurement and stated at a level that transfers to any pipeline that distils an artifact and then judges against the distillation: audit the oracle's *input* (from the 134-pair audit); put the evidence guard where the error mass is (from the census); price the deferral channel and price the contrast rather than the level (from the +9 convention figure falling to +3 under hand-pricing); check the dispatch before re-architecting the judge (from the four self-reported dispatch defects); and self-audit the stage against its own rules. A practitioner can act on these the same week, and two are cheap by the paper's own account — the audit ("a sample of pairs against their cited pages suffices") and the self-audit replay ("a five-line script").

   - **3.2** The deferral lesson is the most transferable thing here and it is the one supported on both backbones: when a judge has an abstention channel and the reporting convention credits it, the accuracy figure is a joint property of the judge and the convention. The paper demonstrates the mechanism rather than asserting it — the same contrast worth nine under the convention prices at three under hand-adjudication and at zero under forced verdicts, and the paper says "at nothing under the forced reading, which is the cleanest demonstration that it is the convention, not the judge, that pays for abstention" (Section 5). Anyone reporting an LLM judge over a pool with a human-review channel faces this and most do not price it.

   - **3.3** The paper practises the audit it preaches and turns it on itself: it reports four defects in its own dispatches found by external readers rather than by its own audit, states that this "is the limit of self-audit and it is why the paper reports them rather than repairing them quietly" (Section 5), and volunteers the artifact of the released baseline tool that "meets a reader who opens the logs to audit the zero" — 152 lines of a three-key dictionary being read as a failure count — rather than leaving it to be discovered (Section 4.6). As a model for how to report an instrument's own failures in an experience paper, this is directly useful. My rating on this criterion is **provisional** to the extent it depends on whether these lessons are already standard practice in the field's evaluation literature, which I did not survey.

   - **3.4 [minor, fixable]** One lesson the paper's own data supports is left implicit: the author-executed non-blind adjudication of the routed queue agrees with an independent pass on 4, 5 and 6 of 20 commonly ruled cases (kappa = -0.01, 0.08, 0.11) and two of the three independent statements land at the forced floor (Section 4.1). The paper uses this correctly to report the joint reading as a bound, but does not state the lesson that follows for anyone repeating this line of work — that the "is this a bug" judgment over an uncertain candidate may itself be near-unreproducible, so the counting convention has to be built to bound it rather than to be confirmed by it. Stating it would make the perspective set stronger without new data.

4. **Verifiability** — Excellent

   - **4.1** The Data Availability section's inventory is specified at the level a replicator needs: the pool, the frozen per-run verdicts of all twelve configurations, the packages the study read (the post-rebuild, cognition-stripped generation the dispatches name), the dispatch texts and the judging prompts they instantiate with English renderings under `rq2/prompts/`, the pair-audit verdicts, the adjudication worksheet and the blind passes, and five named analysis scripts under `rq2/analyses/` (`recompute_paper_numbers.py`, `clause_tally.py`, `convention_pricing.py`, `bootstrap_net_f1.py`, `audit/pair_audit.py`), with `clause_tally.py second` for the second-backbone census. Per the review protocol I did not access the artifact, so I judge the link as declared from the text; the paper states its location (an anonymised, review-time URL) and gives no indication the link is not reachable.

   - **4.2** The paper marks exactly which numbers are *not* scripted or shipped, which is what makes the rest usable: the catch-all composition, the expectation-framing check, the C-row evidence classification and the per-perspective cell vocabularies "are printed but not yet scripted, and the artifact's script-coverage note says so" (Section 4.1); the fix-PR characterisation is "not part of the shipped artifact and we mark the claim accordingly" (Section 4.2); the hand-guided baseline probe shipped but "its output was not retained, so no execution result is claimed" (Section 4.6). A reader knows which claims to take on trust and which to recompute.

   - **4.3** Repairs are reconstructible in both directions. The Data Availability section states that where a run was re-judged, "the re-judged cases and the pre-repair state both ship beside the untouched batches, so either pool can be reconstructed from the package alone"; Section 4.1 makes the same commitment in its own words for the leak repairs ("Both raw generations ship alongside the cleaned one, so a reader can reconstruct either"); and the paper supplies the unrepaired counterfactual itself (41/51 with a confirmed set of 41 + 6), so a reader can check the direction and size of the repair without re-doing it. The void record for the RQ1 detection experiment ships too.

   - **4.4** The evidence-collection conventions are disclosed at the level that makes the numbers interpretable: the verdict space, the majority-of-three confirmation rule and what a stricter rule would give (37/51 rather than 39/51), the counting convention and its admitted price, the *a/b* discordant-pair notation and the note that *a* is the arm printed first, paired exact McNemar at both the confirmed-set and recall levels with both reported for every contrast, and an explicit Holm family of ten naming which four survive and where it stops. Statistically this is more than an experience paper usually supplies.

   - **4.5 [minor, fixable]** The judgments themselves are documented rather than reproducible: both backbones are "serving aliases without pinned weights" (Sections 4.1, 6), and Table 2 names them at a granularity (GLM-5.3-Flash, Qwen3.8-Flash) that does not pin a snapshot. This does not impair checking the paper's claims — the per-run verdicts ship, so every number is recomputable from the artifact — but it means a future reader cannot test whether a different snapshot reproduces the census, and it is the boundary of what the artifact supports. Disclosed; I record it because a reader should know where the check stops.

   - **4.6 [minor, fixable]** The artifact's inventory (the Data Availability section) covers the confirmation stage's materials and the analyses, but not the earlier stages: the knowledge extractor, specification extractor, attack agents, strategy registry and executor described in Section 3 are prose, and their properties — strategy binding as a deterministic function of the constraint record, the five pre-execution gates, the version-alignment precondition — are therefore not checkable against shipped code. Since those stages are not what the paper measures this is minor, but the paper's contribution 2 ("an audit-and-rebuild discipline") would be more portable with the discipline's scripts alongside the pair-audit verdicts.

   - **4.7 [minor, fixable]** Section 6 records that "the row-level accounting of the rebuild does not fully reconcile in our own report and we flag it as an open item; the rates we print are the pair-level ones, which do reconcile". Flagging it is the right move, but a reader who tries to follow the 134 pairs back to the 81 packages will hit the same wall. A short reconciliation table (pairs per package, duplicate instances removed, rows dropped) would close it.

5. **Presentation** — Adequate

   - **5.1** The structure is sound and the section order does real work: pipeline description (Section 3), then methodology and conventions (4.1), then the campaign and the audit (4.2, 4.3), then the instrument (4.4), then the claim (4.5), then the baseline (4.6), with Discussion, Threats, Related Work and Conclusion following. Section 4.4's pointer — "This section supplies the instrument; Section 4.5 carries the paper's claim" — is exactly the kind of signpost a dense paper needs, and Section 6 (Threats) is organised by axis so a skeptical reader can go straight to the relevant caveat.

   - **5.2** The abstract and introduction are organised around the three results with numbers that match the body, and each states its own scope (the third introduction bullet ends with the second-backbone non-reproduction and the C/D ambiguity). I checked the headline arithmetic against the tables and text — 243 judgments, 80% from 24 of 30, 81/51/23/30 case counts, 132 ledger rows, 134 pairs — and it reconciles. My assessment of Figure 1 is from its caption only, since the review copy contains the `.tex` alone.

   - **5.3 [minor, fixable]** The cross-tabulation in Section 4.5 gives rates without denominators: "20 fall on cases whose rebuilt packages carry documented evidence (rate 0.11), 4 on the three weak-evidence cases, and none on the eighteen cases the audit left without documented evidence (rate 0.00)". That sentence names two of the three strata ("the three weak-evidence cases", "the eighteen cases") but not the documented-evidence stratum behind the 0.11, and neither rate's denominator is stated. From the surrounding counts they appear to be wrong closures divided by judgments in each case stratum (20/180, 4/9, 0/54, with strata of 60 + 3 + 18 = 81 cases yielding 180 + 9 + 54 = 243 judgments), but the reader has to reconstruct the missing stratum and both denominators.

   - **5.4 [minor, fixable]** "Interceptions" is used for false positives that are *released* rather than blocked: "recovers seven true bugs for nine interceptions" (Section 1 and the abstract) and "it buys nine true bugs for nine false-positive interceptions" (Section 4.4), against a suppression figure that falls, so the new cases must be leaked false positives. Since "intercept" ordinarily means catching, the sign of the trade is invertible on a first read. Something like "nine false positives released" or "nine interceptions forgone" would remove the ambiguity.

   - **5.5 [minor, fixable]** Table 2 has no column for the schema-line edit, so the relation among its rows 2, 3 and 4 is invisible: Section 4.1 says the aggregation arm "changes that same line, the sentence declaring that no aggregation rule applies, and appends the routing clause", i.e. row 4 is row 3 plus the rule, and Section 4.4's decomposition (30 → 35 → 39) depends on exactly that. As printed, a reader comparing rows 2 and 4 would take the contrast to be the rule alone.

   - **5.6 [minor, fixable]** There is no results table. Twelve configurations across two backbones under two counting readings are reported entirely in running prose; checking, say, what the second backbone's source-only arm scored means reconstructing it from a parenthesis in Section 4.4 ("the two source-only configurations (0.706 and 0.725 recall) are shipped but outside this section's contrasts"). One table giving recall, suppression and confirmed-set count per configuration under both readings would make the paper's instrument checkable at a glance, and would have made 5.5 self-evident.

   - **5.7 [minor, fixable]** Section 4.3 reports that two of the twelve case-level main assertions "were recorded as weak-evidence rows", while Section 4.5 refers to "the three weak-evidence cases". Either the two objects differ (case-level assertions versus packages — in which case say so) or one count is wrong. I found no other internal count that fails to reconcile, which makes this one stand out.

   - **5.8 [minor, fixable]** Section 4.6's account of the baseline logs is hard to parse: "152 lines, across 119 of the 205 per-template logs, report three anomalies apiece". It is unclear how 152 lines relate to 119 logs, and whether 152 is a single-copy figure given the immediately preceding sentence about the master log being "a verbatim echo" that doubles any total taken over the directory.

   - **5.9 [minor, fixable]** "The primary backbone" and "the second backbone" are used throughout the narrative without ever being named there; the mapping (primary = GLM-5.3-Flash, second = Qwen3.8-Flash) exists only in Table 2, and the reader must combine that with Section 4.5's "the second backbone records three" to fix which is which. Name them once in Section 4.1.

   - **5.10 [minor, fixable]** The prose carries a high decode cost. Several sentences bundle four or more measurements with a scope qualifier — the evidence-access paragraph of Section 4.4 ("39→48 ... discordant 0/9 ... p=0.0039; forced 27→31 ... cuts suppression from 21/30 to 12/30 ..."), the leak-repair paragraph of Section 4.1 with its nested parenthetical about the second backbone's flat arm, and the census's fifteen/two/two evidence split in Section 4.5. I did not find a sentence I could not eventually decode, and the two reporting units (per judgment, n = 243, in the census table; per case, n = 81, in the recall figures) are stated where they appear, but the decode cost is high enough that a skimming reader will mis-take a number.

### Questions for Authors

- **Q1:** Of the 51 maintainer-confirmed bugs, 3 are "tracked as duplicates" (Section 4.2). Are those duplicates of pre-existing upstream reports or of your own earlier submissions, and how many of the 51 were already open upstream before you filed? — background 2.8; the intended effect: if a material share of the yield is rediscovery, 2.8's weight rises and my Insights & Evidence rating would move down, since the campaign's value to readers is its validated new findings rather than its filing throughput.

- **Q2:** What fraction of the 30 negatives carries a maintainer disposition, and how many were adjudicated solely by you? — background 2.9; the intended effect: if most negatives are pure author calls, the cost side of the abstract's "seven true bugs for nine" price is materially less anchored than its benefit side, and 2.9's rating would move down.

- **Q3:** Section 4.5's counterfactual is a replay over recorded cells. Would the authors run the direct version — re-judging the 15 cases contract refutation closes, under the verbatim-intent guard, on the shipped materials — and report how many of the seven true bugs survive? — background 2.6; the intended effect: a positive result would move 2.6 up by turning the paper's prescription into an empirical claim, and a null result would move it down by showing the gain was an artifact of the convention.

- **Q4:** Can the second backbone's census be re-taken under a dispatch whose four perspective definitions are unambiguous? — background 2.5; the intended effect: this is the single measurement that decides whether the census pattern is backbone-dependent or letter-confounded, and a clean reproduction would move 2.5 up to the point where the paper's central claim would be a two-backbone result.

- **Q5:** How do the authors read the independent adjudicator's near-chance agreement with their own pass (4, 5 and 6 of 20 common cases; kappa = -0.01, 0.08, 0.11) as a statement about the reproducibility of the bug/not-bug judgment itself, as distinct from a bound on this paper's joint reading? — background 3.4 and 4.5; the intended effect: an explicit lesson here would move Perspective further up, and the underlying datum is a limit on what any successor study in this line can expect from its own adjudication step.


---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Importance & Scope | Excellent | Excellent | Excellent | **Excellent** |
| Insights & Evidence | Adequate | Excellent | Adequate | **Adequate** |
| Perspective | Excellent | Excellent | Excellent | **Excellent** |
| Verifiability | Excellent | Excellent | Excellent | **Excellent** |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Accept** | **Accept** | **Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three recommendations land on Accept, so the unanimous shortcut decides outright; the consensus-tier count would return the same verdict, there being no consensus Poor and no consensus Weak. This round moves two criteria to **consensus Excellent that were not there last round**: Verifiability, which all three now rate Excellent, and Perspective, which R1 joins to make unanimous. The Verifiability move has a mechanical cause worth recording — the anonymous snapshot the Data Availability section names was five commits behind the repository last round, and every script and prompt directory the paper declares now resolves. Verifiability has been the only lever criterion in this project for four rounds, and it moved for the same reason every previous time: whether a reader can run what the paper prints.

Insights & Evidence remains the single criterion at consensus Adequate, and the two reviewers who hold it there name the same bound: the census is a primary-backbone measurement whose second-backbone attempt produced the opposite pattern and cannot be interpreted, because the deployed dispatch defines the four perspectives twice with C and D exchanged. R2 dissents upward and says why — it weights the cross-tab, the invariance of the load-bearing 24 across both printed aggregation rules, and the fact that the count rests on maintainer labels rather than the authors' own negatives, which it calls "exactly the isolation needed to argue the clause is closing wrong rather than the material being defective". That is a genuine divergence of weighting, not of fact, and it is the one place where the three reviews disagree.

The round's remaining `[major, fixable]` items all reduce to two questions the paper cannot answer from its current data: whether the four-perspective organization helps, hurts or does nothing, and whether a guarded judge would reach the same closures. Both would need new arms. The paper discloses the first ("changes five things at once"; the interval excludes only effects above about eleven points) and states the second's limit in its own words ("what cannot be computed from frozen data"). No reviewer made the verdict conditional on either.

### Priority Revisions
Ranked by impact on the verdict. Every item below is `[minor]` or `[major, fixable]`; there is no `[major, unfixable]` that the verdict fails to reflect, and the two items the verdict is *not* allowed to be held hostage by — the single-backbone census and the replay-vs-measurement prescription — are already scoped in the paper at every place the affected number appears.

1. **De-confound the four-perspective contrast, or narrow the claim to what the bundle licenses.** R1 rates this `[major, fixable]` at 2.5 and R3 at 2.7; R2 reaches the same asymmetry from its own side at 5.4. The paper's most quotable sentence — "the organization changes *which* cases are decided, not how many" — rests on two arms differing in five respects, with an equality of forced counts (27 vs. 27, 26 vs. 26) whose primary-backbone interval excludes only effects above about eleven points. R1's fix is constructible from the study's own machinery (perspectives without cognition access; cognition without perspectives); R3's narrower one is to restate the Conclusion, which currently credits "adding an aggregation rule" with an effect its own decomposition gives five of nine bugs to a one-line schema repair, and whose second-backbone "replication" is the same two-edit bundle with no schema-only control there at all. The restatement half of this costs text, not runs.

2. **Say which stratum and which base each rate is over.** R1 rates this `[minor]` at 5.3 and R2 at 5.3 — independently, and both on numbers this paper leans on. R1 reads "20 fall on cases whose rebuilt packages carry documented evidence (rate 0.11)" as a per-case rate (20 of 60) when it is per-judgment (20 of 177 or 180), and R2 reconstructs the same strata differently; the sentence prints two of the four stratum sizes but not the third, so a careful reader cannot settle it. R1 also flags §4.6's "152 lines … three anomalies apiece", which does not parse. Note this is a defect the author introduced this round in response to the previous round's objection, which is the cleanest argument for the reviewers' other presentation asks.

3. **Put a second reader on the pair audit.** All three reviewers reach it — R1 at 2.8, R2 at 2.5, R3 at 2.7 — and all three rate it `[minor, fixable]`. The audit is the paper's most transferable contribution and its second most quoted number, it is a single-reader classification with no agreement figure, and the paper's own threats section records that its row-level accounting "does not fully reconcile". R1's sharper version: for a contribution whose selling point is measurement discipline, the unreconciled ledger should be reconciled or explained in the body rather than flagged as an open item.

4. **Name the arms and the backbones where the numbers are.** R1 rates `[minor]` at 5.5 and 5.2, R2 at 5.4, R3 at 5.6 — the third round in a row that arm-identity and labelling drift has been reported. Five configurations whose names differ by one word are contrasted in one prose series; "the deployed stage", "the full stage" and "the deployed configuration" are the same arm; the two backbones are never named in the narrative, only in Table 2. A one-line glossary would remove a class of misreads at almost no page cost.

5. **Position the abstention result against selective prediction.** R1 rates `[minor, fixable]` at 3.3 and it is the round's only *new* related-work gap: the paper's conclusion is a coverage-versus-risk statement, and it cites none of the selective-prediction or learning-to-defer line that formalises exactly this accounting. R1's pointer (Jung et al., ICLR 2025) is verified in this round's revision and cited; the remaining half is the classical deferral line (Madras et al.; Mozannar & Sontag), which R1 marks provisional and which should be verified before citing.

6. **Take the results table, or justify not taking it.** R1 at 5.6, R2 at 5.4 and R3 at 5.6 all ask for one table giving recall, suppression and confirmed-set counts per configuration under both readings. The author's reason for declining is arithmetic and should be stated in the artifact rather than left implicit: the counted text+figures standing is 17.76 of 18 pages, so a twelve-row table must displace equivalent prose rather than be added.

7. **Reconcile the count, not just the numbers.** R2's item 2.5 is resolved this round — the paper's "Sixteen paired tests" was wrong, and it now reads twenty, with the recall-level ten unchanged and the family's rationale stated. Record it as the class it belongs to: the paper prints several derived counts (the paired tests, the eighteen/nineteen pairs, the 43.3% shares, the 152 lines), and each has been caught by a different reviewer in a different round. The remaining unverified ones are §4.6's line accounting and §4.1's "substantial share" of the 81 that sits on versions the voided runs covered, which R1 (2.10) and R2 (2.7) both ask to be quantified.
