## Reviewer 1: Domain Expert

**Overall Recommendation:** Accept

### Summary

The paper studies documentation--implementation bugs in vector DBMSs---cases where Milvus, Qdrant, or
Weaviate silently accepts an input or returns a shape that contradicts its own API documentation---and
reports three things from one pipeline that mines and confirms such cases: a submission-and-adjudication
ledger (81 adjudicated candidates, 51 maintainer-confirmed bugs, 23 merged fixes, spanning 16 of the
ledger's 19 versions); an audit of the material the pipeline's confirmation stage reads, in which every
(constraint, cited-page) pair reaching a judge's package was checked against the page it cites and the
packages were then rebuilt against version-pinned documentation; and a census of the confirmation stage's
243 recorded judgments on its primary model backbone, classified by the clause of its aggregation rule
that closes each judgment.

The census is the analytical core. The two clauses that assign False-Positive are compared: contract
refutation---a mechanical containment check that carries no evidence requirement---closes 50 judgments and
falls on maintainer-confirmed bugs in 24 of them, while by-design refutation, which the protocol requires
be backed by verbatim intent evidence, closes 19 and is wrong twice; 24 of the stage's 30 incorrect
closures to False-Positive come from the unguarded clause. A replay that routes contract refutation to
human review rather than closing on it moves recall from 39/51 to 46/51 under the deployment's counting
convention (a routed case counts as confirmed) and changes nothing under the forced-verdict reading.
Beside the census, a twelve-configuration study runs three times over the same frozen pool while varying
what the judge is given and which rules it applies; it finds the four-perspective decomposition changing
*which* cases are decided rather than how many, and reports the aggregation rule's effect as largely
deferral.

### Core Strengths

- **S1:** The audit of the oracle's *input* is a measurement this line does not otherwise have: 134
  (constraint, cited-page) pairs split 18 supported / 58 mis-anchored / 58 unsupported, plus a case-level
  layer and a rebuild self-check. The paper frames it exactly as the gap the related work leaves open
  (oracle reliability is measured; the support of the oracle's premise is not). — see 2.3, 3.1
- **S2:** The census is constructed so that its headline count cannot be an artifact of the disputed
  letter semantics: the load-bearing perspective is identified by its cells' unique vocabulary, the count
  is invariant across the two aggregation rules the dispatch prints, and it rests only on
  maintainer-confirmed labels. The paper runs its own strongest objection (that the census is the pair
  audit resurfacing) and separates the two at the material stratum where they could be one phenomenon. —
  see 2.1, 2.2
- **S3:** The study's central negative is clean and decision-relevant rather than a null: forced-verdict
  recall is identical across the two perspective configurations on both backbones (27 vs. 27; 26 vs. 26)
  while their true-bug sets intersect in only 22 of 27 and 23 of 26, and the evidence-access contrast
  ends in a stated tie on net and F1 rather than a claimed win. — see 2.4, 3.4
- **S4:** Candor plus reproducibility is carried further here than is usual: four defects in the authors'
  own dispatches are reported rather than repaired, two leaks are priced with before/after numbers and
  both raw generations shipped, and the declared artifact is live with a coverage note that matches the
  paper's own disclosure list. — see 4.1, 4.2, 4.3, 3.2
- **S5:** The practice lessons are portable and each is tied to a measurement: audit the oracle's input;
  price the deferral channel and the contrast, not the level; check the dispatch before re-architecting
  the judge (a one-line schema repair moved five of the headline nine bugs). — see 3.1, 3.2, 3.3

### Core Weaknesses

- **W1:** The census does not reproduce on the second backbone, the instrument's C/D ambiguity makes the
  reversal uninterpretable, and the content-based re-identification the authors perform on the primary is
  not applied to the second---so the paper's headline prescription rests on a single measurement that its
  own second measurement contradicts. — see 2.5
- **W2:** The audit's headline rates (43.3% unsupported, 43.3% mis-anchored) are one reader's
  classification with no second coder and no reported reliability check, in a line whose standard practice
  the authors' own cited bug study follows (three-stage annotation, kappa > 0.95). — see 2.6
- **W3:** Missing related work: Doc2OracLL (FSE 2025) studies the documentation-to-LLM-oracle channel---
  the nearest step to what this paper audits---and is uncited; the documentation-derived-oracle paragraph
  in Section 7 is where it belongs. — see 3.6

### Detailed Assessment

1. **Importance & Scope** — Excellent
   - **1.1** The problem is important and its context is established from sources rather than asserted.
     Section 2 grounds the premise in the empirical bug study (functional failures the dominant class,
     crash defects a minority) and the community roadmap's naming of oracle definition as the open
     problem, and Section 1 makes it concrete with Milvus issue #49823 (\texttt{nprobe} documented as an
     integer in [1, 16384]; the REST search API accepts 0, returns HTTP 200, and answers). I checked the
     two empirical sources against the shared cache: the bug study reports 57.3% functional failure and
     15.1% crash, and VDBFuzz's own text says crashes are "the most direct and observable oracle" with
     vector-search correctness left to future work. The gap the paper targets is the one the field has
     named, and the paper works in it.
   - **1.2** Table 1 (Section 2) does the positioning work a domain expert would ask for: for each oracle
     family it gives the anchor of the expectation and the structural reason that anchor misses
     system-level behavioural prose. The table's claim is deliberately narrow---the prose-reading families
     read at field, parameter or method granularity and none takes its expectation from untagged,
     system-level prose---and it holds against the competitors I read (Javadoc/method-level tools in the
     Metamon and Konstantinou lines; OpenAPI/trace/source-grounded tools in the SATORI, AGORA+ and MASTOR
     lines). Cross-vendor differential testing is correctly excluded for the right reason (each VDBMS
     standardizes its own parameter semantics, so no vendor adjudicates another's behaviour).
   - **1.3** Scope is stated wherever a reader could over-generalize, and at the level where the
     over-generalization would occur: the pool (submission-filtered, maintainer-adjudicated for positives,
     self-adjudicated for the 30 negatives), the census (primary backbone only), the audit (this distiller
     on these three vendors, one reader), and the statistics (unadjusted p-values, an explicit Holm family
     of ten with its stop point named, and both test levels printed when they disagree). This is the
     criterion on which the paper is strongest: the problem matters and no reader can mistake what was
     measured for what was not.

2. **Insights & Evidence** — Adequate
   - **2.1** The census's construction is mechanical and robust in the way that matters (Section 4.5). The
     load-bearing row rests on perspective A, and A is identified by content rather than assumed: its 243
     cells carry {Neutral 172, Refuted 50, Confirmed 21} and no other letter carries that vocabulary, so
     the 24-of-50 count does not depend on the judge's letter semantics---which is exactly the ambiguity
     that troubles D (cognition vocabulary 145 vs. source vocabulary 98). The count is also shown to be
     invariant across the two aggregation rules the dispatch prints and, importantly, to rest only on
     maintainer-confirmed labels, so it does not depend on the 30 negatives the authors adjudicated
     themselves.
   - **2.2** The paper runs its own strongest objection and separates it at the right granularity
     (Section 4.5): if contract refutation fires because the quoted text does not literally contain the
     assertion, the census could be the pair audit resurfacing, "in which case the prescription would be
     to fix the material rather than to guard the clause". The cross-tab answers at the level the data
     supports: of the 24 wrong closures, 20 fall on the 59 packages whose rebuilt evidence is documented
     (20 of their 177 judgments, rate 0.11), 4 on the 3 weak-evidence packages, and none on the 18 the
     audit left without documented evidence (rate 0.00). The claim is then stated at that granularity
     ("The clause fires on material the audit judged supported"), which is what the cross-tab shows.
   - **2.3** The audit itself (Section 4.3, Table 3) is the paper's genuinely new measurement: every cited
     pair checked against the page it names at the version the row claims, on the packages as the pipeline
     produced them, giving 18 supported as cited / 58 re-anchored from a source file or landing page / 58
     with no support on the cited page (43.3%). Two things make it more than a number: the case-level
     layer is a different object (12 main assertions, five supported, three dropped, two over-strong, two
     weak-evidence, all acted on), and the rebuild is checked for the failure mode this class of work
     invites---zero of 81 rebuilt packages contain a sentence framed as an expectation, with the 19
     phrasing hits each inspected and all verbatim server responses. Against the line's closest works
     (Metamon stabilizes an LLM judge whose falsifier is another LLM question; the systematic review
     reports hallucination named far more often than measured), measuring the oracle's *input* is a
     contribution the field has not made.
   - **2.4** The statistics and the reading discipline are handled correctly, and I checked the arithmetic
     rather than taking it. All ten recall-level p-values follow from the discordant pairs as printed
     (0/9 -> 0.0039; 0/14 -> 0.0001; 12/1 -> 0.0034; 2/6 -> 0.2891; 1/6 -> 0.1250; 0/5 -> 0.0625;
     16/2 -> 0.0013; 11/2 -> 0.0225; 2/14 -> 0.0042; 9/6 -> 0.6072), the Holm sequence over them stops
     exactly where the paper says it stops (four at alpha/10 .. alpha/7, the fifth at alpha/6 = 0.00833
     failing against 0.0225), and the net/F1 figures reconcile with the confusion counts (deployed
     39 true positives / 9 leaked, F1 0.788; no-source 48/18, F1 0.821). The paper also reports the ties
     as ties rather than converting them to wins: net difference 0 with interval [-8, +8]; F1 difference
     +0.033 spanning zero; "we privilege neither" on the two test levels.
   - **2.5 [major, fixable]** The census's generality is not established, and the paper's own second
     measurement points the other way (Section 4.5, Section 6 "Backbone"). On the second backbone
     contract refutation closes 56 judgments and by-design refutation closes 50 of which 22 are wrong, so
     "the protocol guards the clause that is already clean" reverses there. The paper states this
     honestly, but the reversal is left uninterpretable because the deployed dispatch defines C and D
     twice with the two exchanged---precisely the ambiguity the paper resolves on the primary by
     identifying the letters through their cells' vocabularies. That identification is available for the
     second backbone from the same shipped verdicts (the paper itself reports the aggregate split, 217 vs.
     98), and the paper does not perform it. Performing it would either restore comparability and make the
     second census a test of the claim, or demonstrate incomparability rather than suspect it. Until then
     the paper's headline prescription ("put the evidence guard where the error mass is") rests on one
     backbone, and the one-line hedge that it is "advice about where to look rather than a property of the
     protocol" is doing more work than the evidence can carry.
   - **2.6 [major, fixable]** The audit's headline rates have no reliability check. Section 4.3 says the
     43.3%/43.3% split is "this distiller on these three vendors' documentation, classified by a single
     reader without a second coder", and no reliability sample is reported. This is one of the paper's
     three headline numbers (contribution 2), and the standard in this line is a second coder: the bug
     study the paper cites as its premise used multi-stage annotation with Cohen's kappa > 0.95. The pair
     verdicts ship with the artifact, so a re-coding of a sample by an independent annotator is a revision
     task, not a new experiment, and it would convert an unquantified uncertainty into a measured one.
   - **2.7 [minor, fixable]** Two priced quantities rest on human readings that the paper itself shows to
     be unstable. The "honest" price of the deployed change (Section 4.4) comes from an author-executed
     non-blind pass whose agreement with an independent adjudicator is 4, 5 and 6 of 20 commonly ruled
     cases at kappa = -0.01, 0.08 and 0.11 (Section 4.1)---that is chance-level agreement, so the
     independent pass bounds the reading in the ordinary sense of a second opinion but not in any
     statistical one; and the Section 4.5 counterfactual is a replay at recorded perspective values rather
     than a re-adjudication, which the paper says. Both are handled conservatively (the conclusion is
     drawn against the authors' own headline), but the derivations should not be quoted without their
     instability attached.

3. **Perspective** — Excellent
   - **3.1** The first lesson of Section 5---audit what your oracle reads, not only what it concludes---is
     the paper's most portable contribution, and it is backed by a measurement that also tells the reader
     how cheap the method is ("a sample of pairs against their cited pages"). It applies to the largest
     authority class in the field's own taxonomy of LLM oracles (specification-derived sources dominate
     the 83-study corpus the paper cites); any pipeline that distils documentation and judges against the
     distillation inherits both the risk and the fix.
   - **3.2** "Check the dispatch before you re-architect the judge" is quantified and memorable: four
     defects in the authors' own dispatches, none found by their own audit, and a one-line schema repair
     that moved five of the headline nine bugs. Self-reporting instrument defects at this level of detail
     is rare and is itself a practice lesson a reader can carry away.
   - **3.3** "Price the deferral channel, and price the contrast, not just the level" (Section 5) links
     this work to the selective-prediction/escalation line it cites and states the honest conclusion---
     at the reading the paper considers honest, the deployed change is suggested, not established. The
     paper's willingness to report its own headline as at most a suggestion, while still reporting the
     convention-level number that a deployment would actually experience, is the right shape for an
     experience report.
   - **3.4** The organization result is a useful negative with a mechanism: the four-perspective
     decomposition changes which cases are decided, not how many (forced 27 vs. 27 and 26 vs. 26, sets
     intersecting in 22/27 and 23/26), which reproduces in a different currency the premise of the closest
     prior work on multi-perspective judging (Ma et al.: debate amplifies bias after the first round,
     meta-judge resists, so adding perspectives is not a uniform correction). I checked that
     characterization against the cached full text and it is faithful.
   - **3.5** The related-work positioning is accurate where it is most load-bearing, which I verified
     against the cached sources rather than from memory: VDBFuzz is crash-oracle (its own text leaves
     vector-search correctness to future work); Metamon's published profile is quoted verbatim (precision
     0.722 at recall 0.480) and correctly labelled a different-pool tradeoff rather than a head-to-head
     baseline; MASTOR's self-stated limitation ("cannot detect violations of intended requirements that
     are not reflected in code") is exactly the delta the paper claims; TRACE's implementation-drift
     blind spot (detection falling 21-43 points when only the implementation changes) is the asymmetry the
     paper's source-anchored falsifier is designed around. No mischaracterization found.
   - **3.6 [minor, fixable]** Missing related work. Doc2OracLL (Hossain, Taylor, Dwyer, "Investigating the
     Impact of Documentation on LLM-Based Test Oracle Generation", FSE 2025, DOI 10.1145/3729354) studies
     the documentation-to-LLM-oracle channel at Javadoc/method level and is not cited; the
     documentation-derived-oracle paragraph in Section 7 is the natural home for it. It does not threaten
     the novelty claim---it measures documentation's effect on the quality of generated oracles, not
     whether a distilled specification is supported by the page it cites---but a paper whose headline
     contribution is "the step nobody measures" should show that it knows the work measuring the nearest
     step.

4. **Verifiability** — Excellent
   - **4.1** The artifact is declared and reachable. The URL in the Data Availability section resolves
     (I fetched the README through the anonymous link; the repository file path returns HTTP 200), and
     its layout matches the Data Availability paragraph item for item: the pool, the frozen per-run
     verdicts for every arm and run, the post-rebuild cognition-stripped packages, the dispatch texts and
     the English renderings of the two judging prompts, the pair-audit verdicts, the adjudication
     worksheet and the blind passes, and the analysis scripts. The README also documents the
     anonymization and states that no verdict, confidence, perspective value or claim text was altered.
   - **4.2** The five scripts under `rq2/analyses/` cover the main quantitative claims---per-arm matrices,
     both readings, both levels of every paired test, the census on either backbone, both replays, the
     pair audit, the materials cross-tab, and the net and F1 bootstrap intervals---so the paper's numbers
     are recomputable rather than merely inspectable.
   - **4.3** The leak repairs are reconstructible from the package alone: re-judged cases ship beside the
     untouched batches and the pre-repair states ship as well, which is what makes Section 4.1's
     before/after numbers (41/51 with a confirmed set of 41+6 vs. the reported 39/51 and 39+9; suppression
     0.467 to 0.400 and 0.933 to 0.900) checkable rather than asserted. The second repair is shown not to
     move the controls in the authors' favour, which is the direction of disclosure a reader should want.
   - **4.4 [minor, fixable]** One stated statistic is outside the artifact's coverage and outside the
     paper's own coverage list. Section 4.1 reports the outcome of a Holm correction over the ten
     recall-level p-values ("leaves the four smallest significant ... and stops at the fifth"), but the
     artifact's note says no Holm-family correction is computed by any script, and the paper's
     script-coverage sentence names four unscripted quantities without mentioning Holm. Since the ten
     p-values are scripted, this is a two-line addition; as printed, the paper's coverage disclosure is
     accurate but incomplete by one item.

5. **Presentation** — Adequate
   - **5.1** The structure is complete and conventional (introduction, preliminaries, approach,
     evaluation with six subsections, discussion, threats to validity, related work, conclusion, data
     availability), and I verified that every table resolves to the content the paper attributes to it:
     Table 1 is the oracle-candidate table in Section 2, Table 2 the twelve configurations in Section
     4.1, Table 3 the pair-level audit in Section 4.3, and Table 4 the clause census in Section 4.5. The
     internal section cross-references I checked resolve correctly, and I found no language errors that
     obstruct reading.
   - **5.2 [minor, fixable]** "The two full-family controls" (Section 4.1, in the second-leak-repair
     paragraph) are never named. The reader must infer from the true-positive counts in the next sentence
     (48 and 33) that they are the no-source and no-aggregation arms of Table 2. Name them once.
   - **5.3 [minor, fixable]** Section 4.1's first-leak-repair sentence---"The re-judged runs span five
     configurations: contract core, flat judge and source-only on the primary backbone at three runs each
     (nine), the second backbone's source-only arm at three, and its flat judge at one"---takes several
     readings to parse. A list keyed to Table 2's configuration numbers would fix it.
   - **5.4 [minor, fixable]** "Defect 3" in Section 4.5 points at an enumeration that exists only in
     Section 5's list, because Section 1 bundles two of the four defects into one sentence. Number the
     four dispatch defects once, in one place, and refer to those numbers everywhere.
   - **5.5 [minor, fixable]** Density is the main readability cost. Several paragraphs pack four to six
     distinct results into one breath---Section 4.4's "The readings reorder the arms" paragraph and
     Section 4.5's catch-all paragraph are the two hardest---and numbers that belong to a named
     configuration are sometimes given bare (the two source-only recall figures 0.706 and 0.725 in
     Section 4.4, with their backbones unattached), so the reader must reconstruct the mapping from
     Table 2. None of this is incorrect; splitting these paragraphs and naming the configuration at each
     number would materially reduce the effort of checking the paper.

### Questions for Authors

- **Q1:** Table 4 sums to 243, and Section 4.5 reports separately that the judge departs from the appended
  rule in 22 judgments, 17 of them closed to False-Positive. Do those 17 sit inside the catch-all row (69,
  "assigns Human-Review"), that is, does the census count them by what the rule assigns rather than by what
  was recorded? — [intended effect: if they are inside, the row mixes routed and closed judgments and the
  "composition, not a rate" reading of the channel needs restating, moving 2.1 down; if they are counted
  elsewhere, the paper should say where.]
- **Q2:** Can the second backbone's C and D cells be identified by their content as the primary's are, and
  if so what does the census look like under that identification? — [intended effect: if it can be done,
  item 2.5's "uninterpretable" becomes a comparability result and the criterion could move up; if it
  cannot be done, incomparability is demonstrated rather than suspected, which strengthens the paper's
  scope statement without changing the tier.]
- **Q3:** What is the human-review burden of the prescribed change---how many cases reach a person per true
  bug recovered? Fifteen cases are closed by contract refutation in at least two of three runs and seven
  of them are true bugs, but the paper prices only recall and suppression. — [intended effect: adding the
  queue cost would strengthen 3.3's pricing lesson, since the deployment's whole design is about keeping
  the over-report visible in a review queue; without it the prescription is incomplete for a practitioner.]
- **Q4:** Of the 24 wrong contract-refutation closures, how many rest on a pair the audit marked "supported
  as cited" rather than on a re-anchored one? The cross-tab is at package granularity; the row-level
  version is the granularity at which the clause actually reads. — [intended effect: it would settle 2.2
  at the finer stratum and could move that item either way, with the direction determined by the answer.]
- **Q5:** Which two configurations are "the two full-family controls" in Section 4.1? — [intended effect:
  naming them would move 5.2 up.]


---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Accept

### Summary

The paper reports three connected studies of one defect-mining pipeline for vector database management systems
(Milvus, Qdrant, Weaviate). The first is a campaign record: maintainers confirmed 51 of 81 adjudicated submissions
and merged fixes for 23, and the shipped ledger holds 132 rows across 19 versions, of which the 81 span 16 and the 51
span 15. The detection-ability experiment that would have measured per-version detection was voided for
dispatch-discipline violations, so the ledger is offered as a record of submissions and maintainer adjudication
rather than a detection rate.

The second and third studies measure the pipeline's own confirmation stage. An audit of the 134 (constraint,
cited-page) pairs the stage's packages carried found 18 supported as cited, 58 that cited a source file or an API
landing page and were re-anchored, and 58 unsupported by the page they cited; two leak channels the same audit
exposed — a maintainer-cognition section embedded in ten rebuilt packages, and runtime cognition files citing seven
candidates' own issue numbers — were repaired, the affected cases re-judged, and every rate is computed on the
cleaned pool. A clause-level census of the deployed judge's 243 judgments (81 cases × 3 runs on the primary
backbone) classifies each judgment by the clause that closes it: contract refutation closes 50 and 24 of those
closures fall on maintainer-confirmed bugs; the verbatim-guarded by-design clause closes 19 and is right 17 times;
24 of the stage's 30 incorrect closures to False-Positive come from the unguarded clause. Routing contract
refutation instead of closing on it moves recall 39/51 → 46/51 and suppression 21/30 → 12/30 under the deployment's
convention, and nothing under the forced reading. Twelve judge configurations, each re-adjudicating all 81 cases
three times on two backbones, support a paired-test analysis in which the four-perspective organisation changes
*which* cases are decided (forced recall equal at 27/27 and 26/26, true-bug sets intersecting in 22/27 and 23/26)
while the aggregation rule that permits routing moves recall. The paper also reports four defects in its own dispatch
texts and runs the released VDBFuzz configuration against the Qdrant instance, obtaining zero oracle anomalies over
1,127 mutation stages.

### Core Strengths

- **S1:** The clause-level error census is the line's first measurement of where an LLM confirmation judge's
  refutations go wrong, and it is built to survive its own objections: the perspectives are identified from cell
  content rather than assumed from letters, the load-bearing count rests on maintainer labels only, and a package
  cross-tab separates it from the pair audit. — see 2.1, 2.2
- **S2:** The input audit measures a step every "distil a specification from documentation, then judge against it"
  pipeline performs and that the line does not report: 43.3% of cited pairs unsupported, a further 43.3%
  mis-anchored, with the pair-level and assertion-level objects kept distinct. — see 2.3, 3.1, 3.4
- **S3:** The organisation-vs-deferral result is a useful negative reported on two backbones with a fitting design:
  paired exact tests at both levels, both counting readings, a stated Holm family, and the null stated as a bounded
  interval rather than as equivalence. — see 2.4, 2.5
- **S4:** Instrument honesty is load-bearing rather than decorative: four self-defects reported instead of repaired,
  both raw generations shipped, the independent adjudication pass that disagrees at chance reported as a bound, and
  the misleading anomaly lines the baseline's own logs contain disclosed. — see 2.6, 2.9, 2.11, 4.1, 4.2
- **S5:** The lessons in §5 are concrete, quantified, and written to transfer, and the paper bounds the ones that do
  not travel. — see 3.1, 3.2

### Core Weaknesses

- **W1:** The census — the paper's headline — is scoped to one backbone, and the paper leaves its non-replication on
  the second backbone uninterpretable even though the content-based letter identification it already uses on the
  primary could be applied to the second backbone's shipped cells. — see 2.7; Q1
- **W2:** The 43.3% audit number is a single-reader classification with no reliability check; the scope statement
  ("this distiller on these three vendors' documentation") bounds the generalisation but does not establish that a
  second reader would classify the same 134 pairs the same way. — see 2.8; Q3
- **W3:** The hand-priced reading the paper calls the honest one rests on one author's non-blind pass, and the
  independent pass agrees with it on 4, 5 and 6 of 20 (κ ≈ 0). The paper bounds rather than claims it, but the
  pricing that keeps "the deployed change is suggested, not established" leans on this instrument. — see 2.9; Q4

### Detailed Assessment

1. **Importance & Scope** — Excellent
   - **1.1** §2 grounds the target in the field's own evidence rather than asserting it: the non-crashing majority
     is anchored in the VDBMS bug study (functional failures 57.3% against crash 15.1%) and in VDBFuzz's crash-only
     oracle, and the roadmap's open problem is quoted as the residual the paper works in. The paper then separates
     *consistency* (behaviour against the API documentation) from *correctness* (ANN search returning the true
     top-k) and says explicitly which one it does not measure. I checked the bug-study figures against the cached
     competitor record and they match; the scope statement is therefore not a rhetorical hedge but a boundary the
     paper respects in the rest of the text.
   - **1.2** Scope is stated with unusual precision at every level and repeated where it matters: the abstract says
     the ledger is "a record of submissions and adjudication, not a per-run detection rate"; §4.1 states the 30
     negatives are adjudicated by the authors, that there is no inter-annotator study, and that one case is
     unjudgeable and is credited under the convention to eleven of twelve configurations; §4.5 scopes the census to
     one backbone and explains why; §6 restates each limit by heading. For an experience paper whose units are
     reachable only through its own pipeline, this is the right posture.
   - **1.3 [minor, fixable]** §4.2 says "a substantial share of the 81 adjudicated submissions sits on versions that
     experiment covered" — the voided detection experiment. The paper's whole attribution argument depends on the
     reader accepting that the adjudication survives the violation, so the size of that overlap is load-bearing and
     could simply be given (how many of the 16 versions, or how many of the 81 cases, sit on versions the voided
     experiment covered). As printed the reader cannot tell whether "substantial" means a third or nearly all.

2. **Insights & Evidence** — Adequate
   - **2.1** The judge study is designed so that a claim about a stage can be traced to the file that grounds it:
     twelve configurations × 3 runs over one frozen pool, all judges reading the same packs and the same
     version-pinned source clone under identical discipline clauses, and each control described as a traceable edit
     of its parent (the schema line, the sentence declaring that no aggregation rule applies, the routing clause,
     the `source=` path). §4.1 also discloses which contrasts change more than one thing (three of them; the
     four-perspective contrast changes five) instead of presenting clean attributions the design does not support.
     That is the right way to report a growing, non-preregistered configuration study.
   - **2.2** The census is constructed to survive the two objections it raises against itself. The clauses are not
     attributed from perspective letters but identified by the vocabulary each letter's cells carry (A: Neutral
     172/Refuted 50/Confirmed 21; B: 146/80/17; C: 72/71/59/41; D: cognition 145 vs source 98 — I checked that each
     sums to 243), the 24-closure count is computed only on maintainer-confirmed labels, and the cross-tab rules out
     the alternative that the finding is the pair audit resurfacing (20 of the 24 fall on the 59 cases whose rebuilt
     packages carry documented evidence, 4 on the 3 weak-evidence packages, none on the 18 without documented
     evidence; 59+3+18+1 = 81, and 20/177 = 0.11 as printed). The paper also shows the count is invariant across
     both aggregation rules its dispatch prints. This is the strongest single piece of analysis in the paper.
   - **2.3** §4.3 audits the judge's input rather than its output, and defines its object precisely: 134
     deduplicated (constraint, cited-page) pairs classified against the page each cites at the version the row
     claims (18 + 58 + 58 = 134; 18/134 = 13.4%, 58/134 = 43.3%, both shares of 134 as the table says), with the
     twelve case-level assertions kept as a separate object and all twelve acted on (5 supported, 3 dropped, 2
     over-strong, 2 weak-evidence). The two dominant mechanisms — version drift and conceptual-only documentation —
     explain the split rather than merely describing it.
   - **2.4** I recomputed the statistics from the printed counts. There are exactly 20 paired tests (ten at the
     recall level, ten at the confirmed-set level) as §4.1 says, and every printed p-value matches exact McNemar on
     its printed discordant pair: 0/5 → 0.0625; 0/9 → 0.0039, twice; 0/14 → 0.0001; 0/17, 0/18, 0/19 → <0.0001;
     1/3 → 0.6250; 1/6 → 0.1250; 2/5 → 0.4531; 2/6 → 0.2891; 2/14 → 0.0042; 4/4 → 1.0; 5/2 → 0.4531; 6/4 → 0.7539;
     9/6 → 0.6072; 11/2 → 0.0225; 12/1 → 0.0034; 16/2 → 0.0013; 18/2 → 0.0004. Every printed margin also equals its
     printed discordant difference (39−30 = 9 = 11−2; 48−34 = 14 = 16−2; 51−34 = 17 = 17−0; 41−27 = 14 = 14−0;
     51−32 = 19 = 19−0; 51−35 = 16 = 18−2; 36−34 = 2 = 6−4; 36−39 = −3 = 2−5), which also confirms the a/b
     direction convention holds for every pair I checked. The Holm family of ten is correctly applied: sorted
     ascending, 0.0001 < α/10, 0.0034 < α/9, 0.0039 < α/8, the second 0.0039 < α/7, and 0.0225 > α/6 stops the
     sequence. Both readings are priced, and the two levels that disagree are printed side by side without
     privileging either.
   - **2.5** The paper's central negative is properly bounded. On the primary backbone the four-perspective contrast
     is 39 vs 39 at recall (4/4, p = 1.0) and the paper states the interval (±0.11) excludes an effect larger than
     about eleven points but does not establish equivalence; on the second backbone the same contrast is −11 true
     bugs (41 vs 30, 12/1, p = 0.0034) and 51 vs 35 on the confirmed set. Under forced verdicts the two are equal on
     both backbones (27/27; 26/26) with true-bug sets intersecting in only 22/27 and 23/26 — the paper's "changes
     which cases are decided, not how many" is exactly what those numbers support, and the conclusion reproduces it
     at the same precision.
   - **2.6** The leak repairs are reported in the direction that does not flatter the authors: the second repair
     was found to have been applied to the deployed stage but not to the two full-family controls, the six control
     runs were re-judged, and §4.1 states that the arms' true-positive sets are unchanged (48 and 33) while the FPs
     they leak rise by two and one, suppression falling 0.467 → 0.400 and 0.933 → 0.900, with the no-source arm's
     forced recall rising by one. It also prices the counterfactual both ways (the deployed configuration would have
     read 41/51 with 41+6 before the repair) and ships both raw generations so either pool can be reconstructed.
   - **2.7 [major, fixable]** The census is the paper's headline, and it is a single-backbone result whose
     non-replication on the second backbone is left as a shrug: §4.5 reports that there contract refutation closes
     56 judgments, by-design closes 50 of which 22 are wrong, and the unguarded clause supplies 24 of 48 incorrect
     closures (50% rather than 80%), then says "we cannot rule out the letters meaning different things there"
     because the dispatch defines the four perspectives twice with C and D exchanged. But the paper's own remedy for
     exactly this ambiguity is already in the paper: on the primary it identifies each perspective by the vocabulary
     its cells carry, and the second backbone's cells ship (217 of 243 D cells use the source vocabulary there
     against 98 on the primary). Re-running `clause_tally.py second` under content-based identification would say
     whether the reversal is a real backbone contrast or an artifact of the paper's own dispatch defect. As printed,
     the paper's flagship lesson has to be downgraded to "advice about where to look" when the answer may already be
     in its data. The fix is a replay, not a new experiment.
   - **2.8 [major, fixable]** §4.3's 43.3% is one reader's classification of all 134 pairs, with no second coder
     and no reliability estimate. The paper discloses this and refuses to generalise ("this distiller on these three
     vendors' documentation"), which is the right hedge, but the number is the paper's most quotable result and the
     one a practitioner is invited to compare against their own. A second read of the 134 pairs (or a stratified
     sample) is cheap, and without it the reader cannot distinguish a property of the distiller from a property of
     the classifier.
   - **2.9 [minor, fixable]** The hand-priced/joint reading — the paper calls it "the reading this paper considers
     honest", and it is what turns the headline change from +9 to +4 and the deployed stage from 39/51 to 33/51 —
     is one author's non-blind pass over the routed queue, bounded by an independent pass that agrees on 4, 5 and 6
     of the 20 commonly ruled cases under the three protocol statements (κ = −0.01, 0.08, 0.11), with two of the
     three independent passes landing at the forced floor. The paper reports this and calls the joint reading a
     bound rather than a measurement, which is the honest handling; the residual issue is only that the *pricing
     paragraph* (§4.4) presents +3/+4/+5 as readings of one measurement when the underlying hand-rulings are
     themselves near-chance-reproducible, so the reader should be told what happens to those three numbers if the
     independent pass's rulings are used instead.
   - **2.10 [minor, fixable]** The counterfactual's arithmetic does not follow from the case counts as printed.
     §4.5 says "Fifteen cases are closed by this clause in at least two of three runs, seven of them true bugs, and
     all seven are unconfirmed — so seven is the case-level maximum", and reports suppression 21/30 → 12/30 (nine
     interceptions). Eight negatives remain among those fifteen, so the ninth interception must come from somewhere
     the sentence does not describe — for instance a negative closed by A = Refuted in exactly one run that has one
     other Confirmed-or-Human-Review run, which flips under the replay even though it is not among the fifteen. That
     is consistent, but it also means the ceiling argument is not valid as stated (a single-closure case flips under
     the same replay) and the replay rule the counterfactual actually applies is nowhere stated. See Q2.
   - **2.11 [minor, fixable]** §4.6 reports zero oracle anomalies from the released VDBFuzz configuration on the
     Qdrant instance "where our silent-accept defects are live", and reads the zero as a bound on the released
     configuration's reach into the silent majority. The reading is appropriately narrow, and the disclosure of the
     152 misleading "three anomalies" lines in the baseline's own logs is exemplary (the cached VDBFuzz record does
     confirm the 205-template release, so the run's inputs are identifiable). What is missing is the other
     explanation: if the tested instance contained no crash-class defect the released mutation vocabulary could have
     reached, the zero is also consistent with there having been nothing to find, and the bound would need that
     caveat. One sentence on what live crash-class defects the tested instance had would close it.
   - **2.12 [minor, fixable]** The stated justification for the Holm family is imprecise: §4.1 says the ten
     recall-level tests form the family "because they share an estimator, which the confirmed-set tests do not", but
     the confirmed-set tests use the same estimator (exact McNemar); what distinguishes the ten is that they share a
     pool (the 51 true bugs). The family choice itself is defensible — say the true reason.

3. **Perspective** — Excellent
   - **3.1** The five lessons in §5 are each tied to a measurement rather than asserted: audit the oracle's input
     (43.3% unsupported, "a sample of pairs against their cited pages tells you how much of your judge's input is
     unsupported"); put the evidence guard where the error mass is (24 of 50 closures wrong, priced at seven bugs
     for nine interceptions and re-priced at zero); price the contrast, not just the level (nine under the
     convention, three under hand-pricing); check the dispatch before re-architecting the judge (a one-line schema
     repair moved five of the headline nine bugs); and self-audit a stage against its own rules (22 forward
     departures, 17 in the forbidden direction, 10 on real bugs — "a five-line script"). A practitioner building
     any documentation-derived-oracle pipeline can adopt these without reproducing the study, which is what makes
     them lessons rather than findings.
   - **3.2** The paper bounds its own lessons where the evidence stops: "the rule is advice about where to look
     rather than a property of the protocol" (§5), and "at the reading this paper considers honest, the deployed
     change is suggested, not established" (§4.4). It also states that the census is measured on the primary
     backbone and does not reproduce. Readers are told which of the five lessons they can carry away unmodified and
     which need their own measurement first.
   - **3.3** Related-Work coverage holds up under the checks I could make. I fetched the cached competitors and
     compared the paper's characterizations against them: Metamon (precision 0.72 / recall 0.48 confirmed in its own
     abstract; its falsifier is a metamorphic LLM query with self-consistency and no non-LLM evidence source — the
     paper's "self-reference this pipeline's source grounding exists to break" is accurate, and the paper correctly
     declines to call it a head-to-head baseline); Ma et al. (multi-agent debate amplifies bias across rounds; the
     meta-judge resists; bias measured as consistency, not accuracy — the paper's "measure multi-agent judging for
     bias rather than for accuracy" and "adding perspectives is not a uniform correction" both hold); TRACE
     (detection falls 21–43 points when only the implementation changes — "the asymmetry a source-anchored
     falsifier is built for" holds); the oracle survey (hallucination named by 58 studies, observed by 44; only 2 of
     83 studies in the REST/API domain — it supports both "named far more often than measured" and the novelty of a
     VDBMS-specific, adjudicated-pool measurement); Molinelli et al. (43% against 45% human mutation score, per-
     project −40% to +30% — "near-human on average, unreliable per-subject" holds); and MASTOR, whose own
     limitations section says it "infers semantics from implementation behavior … cannot detect violations of
     intended requirements that are not reflected in code", which is precisely the delta the paper claims. Two
     scoped coverage searches within my specialty (LLM-judge abstention/organisation, and documentation-derived
     oracle reliability) surfaced no uncited closely-related work, so I have no Missing-Related-Work finding; the
     only bibliography gap I found is the unkeyed CASCADE mention (see 5.2).
   - **3.4** The paper states its delta honestly: "what this paper adds to the line is not a new oracle but an audit
     of the oracle's input". The survey's own gap — trust gaps where hallucination is named more often than measured
     — is what §4.3 measures for this class, and the paper does not claim more than that.
   - **3.5 [minor, fixable]** The flagship lesson is the one that transfers least, and the heading does not say so:
     "Put the evidence guard where the error mass is" is true on the primary backbone, and on the second backbone
     the guarded clause is the inaccurate one (50 closures, 22 wrong). The text of §5 carries the qualifier, but a
     reader who takes the heading plus the 24-of-50 result away will move guards toward contract refutation
     specifically. Leading with the transferable form — "measure where your error mass is before deciding what to
     guard" — would match what the paper can support.

4. **Verifiability** — Excellent
   - **4.1** The artifact is declared and reachable, and its contents are the ones this paper needs: the link in
     Data Availability resolves (I checked it; the anonymous repository answers with a redirect to its file API);
     the pool, the frozen per-run verdicts of all twelve configurations, the packages the study read, the dispatch
     texts, English renderings of the two judging prompts, the pair-audit verdicts, the adjudication worksheet, the
     blind passes and the five named analysis scripts all ship, and where a run was re-judged both the re-judged
     cases and the pre-repair state ship beside the untouched batches so either pool can be reconstructed.
   - **4.2** The text alone is unusually checkable: the counting convention, the ≥2-of-3 majority rule and its
     exception (three cases split three ways; recall would be 37/51 under a two-identical-verdict rule), the clause
     firing order, the exact differences among the twelve configurations, the discordant-pair a/b convention, the
     Holm family, and the analysis scripts by name. I recomputed every printed McNemar p-value and every printed
     margin (see 2.4) from the text alone; the census table's own arithmetic is closed (rows sum to 243; decided
     rows 174; 24 of 30 = 80%; 15+2+2 = 19; 37+32 = 69; 28+17 = 45; 51+49+2 = 132), and the F1/net figures follow
     from the confirmed sets (39 TP / 9 leaked → 0.788; 48 / 18 → 0.821; net 30 both ways).
   - **4.3 [minor, fixable]** Three recomputability gaps remain, all self-declared: four analyses are "printed but
     not yet scripted" (the catch-all composition, the expectation-framing check, the C row's evidence
     classification, the per-perspective cell vocabularies); the rebuild's row-level accounting "does not fully
     reconcile" in the authors' own report; and the fix-PR characterisation (all 23 modify implementation code, 15
     add a regression test, none documentation-only) is not in the shipped artifact. Each is flagged, and none of
     the rates printed depends on them, but scripting the four named analyses would remove the only place where the
     printed numbers run ahead of the artifact.

5. **Presentation** — Excellent
   - **5.1** The structure carries a heavy instrument: §3 describes the pipeline and says what each stage is for in
     the measurement, §4.1 fixes the pool, the counting convention and the statistics before any result, §4.3–§4.6
     are four self-contained measurements each opened by an italicised question, §5 is lessons, §6 threats, and §7
     related work ends by naming what is not claimed. Headings do real work ("The protocol guards the clause that is
     already clean", "We report them rather than repair them") and the tables are readable and correctly captioned
     (the pair-audit table even pre-empts the double-counting reading of its two 43.3% shares).
   - **5.2 [minor, fixable]** §7 names CASCADE and characterises its mechanism — "inverts the roles the same way
     while working at method granularity, taking a regenerated implementation rather than a real one as its
     falsifier" — but gives no inline citation, while every other named system (Metamon, AGORA+, SATORI, MASTOR,
     MASTEST, VDBFuzz, LogicHunter, Toradocu, @tComment, JDoctor, DocTer, RESTInfer, RBCTest) carries one. The
     characterisation is accurate; add the reference key.
   - **5.3 [minor, fixable]** §4.2 refers to "the RQ1 detection-ability experiment". RQ1 is defined nowhere in the
     paper — the label survives from an earlier framing, as do the `rq2/prompts/` and `rq2/analyses/` artifact paths.
     Name the experiment by what it is or define the label once.
   - **5.4 [minor, fixable]** VDBFuzz's oracle is described twice with different thresholds: §2 says it "fires on a
     5xx response or a failed request induced by template-driven input mutation", §4.6 says "the per-template
     oracle fires on 5xx rather than on service death". Both can be true of different parts of the tool, but a
     reader comparing the two passages has to guess which is the operative statement.
   - **5.5 [minor, fixable]** §4.5's disclosure about the pre-repair counts is not checkable as written: it gives
     pre-repair contract refutation = 47 and by-design = 20 and concludes that "by-design is the middle of the
     three" holds "of the cleaned pool", but with those two numbers by-design would also be the middle pre-repair —
     the reader needs the pre-repair cognition count (16 post-repair) to see what the re-judging moved.
   - **5.6 [minor, fixable]** Housekeeping: mixed British/American spelling ("artefact" beside "behaviour" and
     "behavior"); in §4.5 an em-dash is followed by a comma ("--- all `NO_SIGNAL`, a value the perspective defines
     but the aggregation has no clause for either ---, 17 rest on true bugs"); and the abstract's closing "43.3%"
     attaches to the second of two equal shares without the "each of 134" qualifier the table carries, which the
     table's caption then has to repair.

### Questions for Authors

- **Q1:** On the second backbone, can you re-identify the four perspectives by the vocabulary their cells carry (the
  method already used on the primary, where each letter's cells carry its own vocabulary and no other) and re-run
  the census? — If the reversal survives content-based identification, item 2.7's rating would move up because the
  paper would have a real two-backbone contrast instead of an uninterpretable non-replication; if it disappears,
  the paper's non-replication claim becomes correspondingly stronger.
- **Q2:** What exactly does the counterfactual replay change — every A = Refuted cell, or only cases the clause
  closes in at least two of three runs? — Stating the rule and showing how +7 and −9 follow from the printed counts
  would move item 2.10's rating up, because a single-closure case also flips under a per-cell replay, which is the
  reading under which the "seven is the case-level maximum" sentence is not valid as written.
- **Q3:** Would a second coder on the 134 pairs (or a stratified sample) be feasible before publication? — A
  reliability figure would move item 2.8's rating up without changing the claim's scope, since the paper already
  restricts it to this distiller and these vendors.
- **Q4:** If the three pricing figures (+3 / +4 / +5) were recomputed with the independent pass's rulings rather
  than your own, do they move, and by how much? — An answer would move item 2.9's rating up if the pricing is
  stable under the independent rulings, and would change how the paper's "suggested, not established" sentence
  should be read if it is not.
- **Q5:** What live crash-class defects did the tested Qdrant instance contain — in particular any the released
  mutation vocabulary could have reached? — Naming them (or stating that there were none) would move item 2.11's
  rating up, because it decides whether the zero anomalies bound the oracle's reach or merely reflect an instance
  with nothing for a crash oracle to find.


---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Accept

### Summary

The paper reports three linked empirical studies of one multi-agent pipeline that mines documentation–implementation ("silent") defects in three vector database systems — Milvus, Qdrant, and Weaviate. The first is a mining campaign: 81 adjudicated submissions, of which maintainers confirmed 51 as real bugs and merged fixes for 23, drawn from a 132-row ledger covering 19 versions. The paper states plainly that this is a record of submissions and adjudication rather than a per-run detection rate, because the runs that would have measured detection ability were voided for information-boundary violations, and that nothing in the paper depends on them.

The second study audits the material the pipeline's confirmation stage reads. All 134 (constraint, cited-page) pairs that the per-case evidence packages carried at the time of the study were checked against the page each cites: 18 are supported as cited, 58 cited a source file or a landing page and were re-anchored, and 58 have no support on the cited page. The same audit surfaced two channels through which material the judge was forbidden to read had reached it — an embedded maintainer-cognition section in ten rebuilt packages, and the candidates' own issue numbers in the runtime cognition files. Both were stripped, the affected cases were re-judged, and every reported rate is computed on the cleaned pool.

The third study classifies the deployed judge's 243 judgments (81 cases × 3 runs, on the primary backbone) by the aggregation clause that closes each one, and locates the error mass on the one refuting clause the protocol does not guard: contract refutation closes 50 judgments, 24 of them on maintainer-confirmed bugs, and supplies 80% of the stage's incorrect closures to False-Positive, while the guarded by-design clause closes 19 and is right 17 times. A replay that routes contract refutation to human review instead of closing on it is priced at seven true bugs for nine false-positive interceptions under the deployment's counting convention, and at zero under a forced-verdict reading. The paper also reports four defects in its own dispatches, one of which — a one-line output-schema field — moves five of the nine bugs in its headline contrast.

### Core Strengths

- **S1:** A complete, quantitative audit of the oracle's *input* — the step this line of work normally leaves unmeasured — with the two mechanisms that explain the rates, the repair discipline that followed, and a check on the failure the repair class invites — see 2.2, 4.1, 4.2.
- **S2:** The census's load-bearing count is defended against the obvious competing explanation (defective citation material) and against three internal sources of artifact (labels, aggregation rules, leak repairs) — see 2.1.
- **S3:** The paper prices its own accounting convention and shows how much of its flagship effect is deferral rather than better deciding, reporting three readings side by side — see 2.3, 2.4.
- **S4:** Self-audit and disclosure at a level rare in this literature: voided runs, four defects in the authors' own instrument, an accounting item left flagged as unreconciled, and a non-blind pass reported as a bound rather than a measurement — see 3.1, 3.2, 4.3.
- **S5:** Scope discipline: every claim carries its population, in the abstract, in §4.5, and in §6 — including the census's single-backbone scope and the audit's non-generalisability — see 1.2.

### Core Weaknesses

- **W1:** The census, which carries the paper's title claim, is a single-backbone measurement; its pattern does not reproduce on the second backbone, and that second measurement is itself confounded by the authors' own dispatch defect — see 2.5, 3.4.
- **W2:** The four-perspective contrast changes five things at once, so it cannot isolate the perspective decomposition — yet the Conclusion's first sentence generalizes from it to "the judge's internal organization," while the paper's own step ladder shows a one-line schema field does move the outcome — see 2.9.
- **W3:** The hand-priced readings that cut the flagship effect from nine true bugs to three rest on an author-executed, non-blind pass that the authors' own independent adjudicator reproduces on only 4, 5, and 6 of 20 commonly ruled cases (κ = −0.01, 0.08, 0.11) — see 2.8.
- **W4:** For a paper whose second contribution is an audit discipline, two supporting claims sit outside the shipped artifact or do not reconcile, and the pair-level classification is a single reader's — see 2.10, 4.3.
- **W5:** Several load-bearing passages are compressed past easy parsing, and two references misattribute content (a cross-reference that resolves to text the target section does not contain, and a contribution bullet that misstates where the 243 judgments come from) — see 5.2, 5.3, 5.4, 5.6.

### Detailed Assessment

1. **Importance & Scope** — Excellent *[provisional: I did not survey this niche, so my sense of how much the field already knows about judge-input audits is from the paper alone]*
   - **1.1** The problem is established with the right shape. Section 1 opens on the concrete failure mode (a disabled filter returning all matches; a zero-length vector corrupting an index), Section 2 backs "most VDBMS bugs do not crash" with two cited studies and shows that the one dedicated fuzzer's oracle — which Section 4.6 reports as firing on 5xx rather than on service death for the released configuration — cannot reach that class, and Section 4.2 lands it with the practical number: 51 maintainer-confirmed bugs, 23 with merged fixes, across three production systems. The separation the paper draws in Section 2 between *consistency* (behaviour vs. the API documentation) and *correctness* (mathematical quality of results) is stated cleanly and excludes the vector-search-accuracy question that would otherwise blur the target.
   - **1.2** Scope is attached to every claim rather than to a caveat section. Section 4.5 opens the census by narrowing it to the deployed stage on the primary backbone, gives the check that produced the narrowing, and states what can and cannot be said about the second backbone; Section 4.3's "What it means" refuses to generalise the audit rates to LLM distillation; Section 6 lists seven threat categories. This is the discipline that makes the paper's scoped claims usable.
   - **1.3 [minor, fixable]** The pool is submission-filtered and no pre-screening precision is given. Section 1 says the ledger "carries our own screening and submission decisions", and Section 6 calls the pool a "submission-filtered subset of one pipeline's output", but the paper never says what fraction of the pipeline's raw candidate output the 81 represent, and there is no detection rate anywhere (the runs were voided, §4.2). That is honest, but it means the first contribution's "yield" is a confirmation rate *among submitted candidates*; a reader cannot price the campaign against its cost. A revision could state the screening ratio, or state explicitly that it is unavailable.

2. **Insights & Evidence** — Excellent
   - **2.1** The census's construction is unusually well defended for a study of this kind. The classification rule is mechanical (the clause that first decides a judgment, in the fixed firing order given in §3.5 and restated in §4.5), and the load-bearing count — 24 of the 50 contract-refutation closures fall on maintainer-confirmed bugs — is shown to rest only on maintainer labels (§4.5), to be invariant across the two aggregation rules the dispatch prints (§4.5), and to survive the two leak repairs. Most importantly, the paper anticipates the obvious competing explanation — that the pair audit's 58 unsupported pairs *are* the 24 wrong closures — and separates them with a cross-tabulation: 20 of the 24 fall on cases whose packages carry documented evidence, 4 on the 3 weak-evidence packages, and none on the 18 the audit left without documented evidence. That is the argument that turns a correlation into a finding about the protocol rather than about the material.
   - **2.2** The audit in Section 4.3 measures the stage's *input* and then explains its own rates. The three-way split on 134 pairs is reported in Table 3, and the two mechanisms — version drift (the augmentation script drew every vendor's constraints from one fixed version's contract) and conceptual-only documentation (constraints such as `nprobe ∈ [1, nlist]` that exist as prose but not as documented values) — tell the reader *why* the unsupported rate is what it is rather than only that it is 43.3%. The follow-up check ("zero of 81 packages contain a sentence framed as an expectation," with the 19 phrasing hits inspected and attributed to verbatim server responses) is exactly the audit-the-repair discipline this class of work needs.
   - **2.3** Section 4.4 prices the paper's own accounting convention rather than hiding behind it. The three readings (deployment convention, forced verdicts, hand-adjudicated joint) are reported for the same contrasts; the paper states outright that under the convention "the rule's effect and the routing rate are the same quantity" and that it will not present the difference as the rule deciding better; and it reports the net-FP and F₁ bootstrap intervals that make the source-withheld arm a tie rather than a defeat. This is the part of the paper I would most expect other judge papers to copy.
   - **2.4** The substantive negative results are reported and carried into the Conclusion: two configurations that differ in whether they carry the four-perspective decomposition confirm the same number of true bugs under forced verdicts (27 vs. 27 and 26 vs. 26) while their forced true-bug sets intersect in only 22 of 27 and 23 of 26, and on the second backbone the perspective-carrying configuration is *worse* (41 vs. 30, 12/1, p = 0.0034). The step ladder on the primary backbone (flat 30 → +schema-line 35 → +routing 39 at recall, with forced recall going 25 → 29 → 27) is what allows the reader to see that a one-line output-schema repair moves five of the nine bugs.
   - **2.5 [minor, fixable]** The census is a single-backbone measurement whose pattern does not reproduce on the second backbone, and the second measurement cannot settle whether it disagrees: Section 4.5 reports that there contract refutation closes 56 judgments and by-design closes 50 of which 22 are wrong (50% rather than 80% of incorrect FP closures), but the deployed dispatch defines the four perspectives twice with C and D exchanged, and the recorded D cells use the source vocabulary in 217 of 243 judgments on the second backbone against 98 of 243 on the primary. The paper is scrupulous about this — it is in the abstract, in Section 4.5, in Section 6 — and the claim it actually makes ("the rule is advice about where to look rather than a property of the protocol") is exactly as strong as the evidence supports, so leaving this unfixed does not undermine the stated claim. But the contribution list presents the census as a general contribution, and one of its two available replications is a null that the paper itself cannot interpret. A revision that repaired the dispatch and re-read the second backbone would decide whether the finding is about the protocol or about this configuration; short of that, the paper should say in the contribution bullet that the census is one configuration's, not a replicated pattern.
   - **2.6 [minor, fixable]** The paper reads the recorded rationales behind the *guarded* clause but not behind the unguarded one. Section 4.5 reports that the 19 C=Refuted closures were read one by one and separated into 15 comment-or-docstring citations, 2 name-validation citations, and 2 structural inferences — and that the last two violate the red line. The 50 A=Refuted closures are the load-bearing row of Table 4 and are never read that way. Reading them matters because the paper's own compliance recount shows the judge departs from its appended rule in 22 of 243 judgments, i.e. written guards do not necessarily bind; if the recorded rationales behind those 50 closures show evidence-based refutations rather than mechanical containment failures, the counterfactual's assumed behaviour changes. The data ships, so this is a reading exercise, not a new experiment.
   - **2.7 [minor, fixable]** Neither the census (Table 4) nor the pair audit (Table 3) is disaggregated by system, although the pool is heavily unbalanced (Milvus 43 adjudicated, Qdrant 28, Weaviate 10, §4.2). Section 4.3's "conceptual-only documentation" mechanism and Section 4.5's "the clause fires on material the audit judged supported" argument both invite the question of whether the error mass is concentrated in one vendor's documentation; a per-system row would let a reader see whether the fixing recommendation is about clauses or about one vendor's prose.
   - **2.8 [minor, fixable]** The hand-priced reading — the one the paper calls the honest one — is the least verifiable number in the paper. Section 4.1 reports that an independent adjudicator on the same materials agrees with the author-executed non-blind pass on 4, 5, and 6 of the 20 commonly ruled cases under the three protocol statements (κ = −0.01, 0.08, 0.11), and that "two of the three independent passes land at the forced floor". Section 4.4 then builds the +3 floor and the "suggested, not established" conclusion on that pass. The paper's handling (report it as a bound; report every contrast under forced verdicts as well) is correct, but a table of the disputed cases — which side each of the ~14 disagreements falls on — would let a reader see whether the floor or the convention reading is closer to right.
   - **2.9 [minor, fixable]** The four-perspective contrast is bundled and the Conclusion generalizes from it. Section 4.4 is explicit that the contrast changes five things against the rule-bearing flat judge (the perspectives, the aggregation rule text, the red-line set, the declared verdict field, and access to the cognition corpus), and labels the result accordingly. Section 8, however, opens with "the answer on this pool is not the judge's internal organization" and then evidences it with the four-perspective contrast alone — while Section 4.4's own step ladder shows that two *other* organizational choices (the one-line output-schema field and the routing clause) move the outcome a lot. The body is careful; the Conclusion's first sentence should name the bundle ("the four-perspective decomposition") rather than "internal organization."
   - **2.10 [minor, fixable]** The pair-audit classification is a single reader's, without a second coder (Section 4.3's "What it means" and Section 6 both say so), and the row-level accounting of the rebuild "does not fully reconcile in our own report" (Section 6). Both are disclosed, and the printed pair-level rates do reconcile, but for a paper whose second contribution is an audit discipline, a second coder on a sample and a note on what fails to reconcile would close the two gaps that a reader will otherwise have to take on trust.
   - **2.11 [minor, fixable]** One of the 81 cases, `milvus_001`, is unjudgeable, and Section 4.1 reports that eleven of the twelve configurations route it to Human-Review in at least two of three runs and are therefore "credited a point for a case nobody could judge." The paper never says whether that case is one of the 51 true bugs or one of the 30 negatives, and the direction of the credit — recall credit versus a leaked false positive — depends on which it is. Nor is any contrast reported with the case excluded.

3. **Perspective** — Excellent *[provisional: the transferability of the lessons to other pipelines is judged from the paper's own reasoning]*
   - **3.1** Section 5 gives five lessons, each tied to a measurement rather than to a sentiment: audit what your oracle reads (backed by the 134-pair audit and the cross-tab in §4.5); put the evidence guard where the error mass is (backed by Table 4); price the deferral channel and price the contrast, not just the level (backed by the +9 → +3 collapse); check the dispatch before you re-architect the judge (backed by four defects, one of which moves five bugs); and self-audit a stage against its own rules ("that is a five-line script"). The most valuable lesson is the meta-observation attached to the fourth: none of the four dispatch defects was found by the authors' own audit — they were found by reviewers reading the shipped texts — and the paper says so rather than quietly repairing them. For a paper whose methodological claim is that the pipeline is auditable, that is the honest limit case, and it is the kind of lesson experience papers exist to deliver.
   - **3.2** Section 6's threats taxonomy is organised by object — yield, pool, materials, design, backbone, counting, instrument — rather than by generic hedging, which makes it directly reusable as a checklist by anyone reporting a judge study: for each object it says what was not measured and what the reader should therefore not conclude.
   - **3.3 [minor, fixable]** The paper recommends procedures but never reports their cost. The only effort number in the paper is the baseline's (205 templates, 50.8 minutes wall time, §4.6). A practitioner deciding whether to adopt "audit what your oracle reads" needs the price of the audit the authors actually ran: the 134-pair classification, the 12-assertion case audit, the 20 hand-adjudications, and the twelve configurations × 81 cases × 3 runs. Section 5 calls the measurement "cheap" without a number behind it.
   - **3.4 [minor, fixable]** The guard lesson is stated as an imperative with a back-reference rather than with its transfer condition. Section 5's "Put the evidence guard where the error mass is" is followed immediately by the concession that on the second backbone the error mass moved, and the conclusion is that the rule is "advice about where to look rather than a property of the protocol." Stating the condition under which the advice transfers — a refuting clause that carries no evidence requirement while closing a large share of FP assignments — would make the lesson usable without overclaiming, and would remove the impression that it is a rule that failed a replication.

4. **Verifiability** — Excellent
   - **4.1** The artifact declaration is specific and complete for the analyses the paper's claims rest on. The Data Availability section names the replication package URL and enumerates the pool, the frozen per-run verdicts of all twelve configurations, the packages the study read, the dispatch texts and the judging prompts, the pair-audit verdicts, the adjudication worksheet and the blind passes, and the five analysis scripts; Section 4.1 names those five scripts by filename and says which analyses are scripted and which are not. I attempted to resolve the declared URL from my review environment and could not (the fetch was refused by this environment's network policy, not by the site), so I judge the link as declared; I did not attempt to clone or run anything.
   - **4.2** The paper states which numbers a reader can reproduce and which they cannot: "All rates, the census on both backbones, both replays, the net and F₁ intervals and the pair audit are recomputable from the artifact's five analysis scripts", while the catch-all composition, the expectation-framing check, the C-row evidence classification, and the per-perspective cell vocabularies are "printed but not yet scripted", with the artifact's coverage note saying so. Both raw (pre-repair) generations ship beside the cleaned one, so either pool can be reconstructed (§4.1, Data Availability). For a study whose object is the auditability of its own stage, that is the right level of disclosure.
   - **4.3 [minor, fixable]** Two supporting claims are not checkable from the package. The fix-PR characterisation in Section 4.2 (all 23 merged fixes modify implementation code, 15 also add a regression test, none is documentation-only) is explicitly "not part of the shipped artifact" and the paper marks the claim accordingly; the row-level accounting of the rebuild "does not fully reconcile" and is left as an open item (§6). Shipping the fix-PR table and a one-paragraph reconciliation note would remove the two places where the paper asks the reader to take its word.
   - **4.4 [minor, unfixable]** The two backbones are serving aliases without pinned weights (§4.1, §6), and as printed the paper identifies them only by alias (GLM-5.3-Flash, Qwen3.8-Flash). The judge runs therefore cannot be regenerated by a reader; verification is limited to the frozen verdicts and the shipped analyses. This does not move the tier — the paper's claims are about the recorded behaviour of those configurations and every number is checkable from the frozen material — but the paper should state plainly, in one clause, that re-generation (as opposed to re-analysis) is not reproducible.
   - **4.5 [minor, fixable]** The three protocol statements behind the independent adjudication ("pack-only, pack-plus-source and full-protocol", §4.1) are named but never described. Since the paper's most conservative reading rests on how those statements were posed, either the statements or their location in the package should be given in the text.

5. **Presentation** — Adequate *(note: the pipeline figure's image file is not present in the stripped source I reviewed, so my assessment of Figure 1 rests on its caption and its references, both of which are informative and consistent with the surrounding text)*
   - **5.1** The structure is sound: eight numbered sections with the unnumbered Data Availability after the Conclusion, the three results previewed in the abstract and Section 1 and revisited in Section 8, and the load-bearing material placed where a reader will look for it. Individual presentation decisions are actively helpful: Table 3's caption pre-empts the obvious misreading ("the two 43.3% shares are each of 134, not a combined 86.6%"); Table 4 is grouped by the outcome each clause assigns rather than by clause order; the a/b convention for discordant pairs is declared once (§4.1) and used consistently; and Section 4.5's "this is not the pair audit's finding resurfacing" paragraph states the alternative explanation before the reader can raise it.
   - **5.2 [minor, fixable]** Several load-bearing sentences are compressed past easy parsing and have to be reconstructed. Section 4.1's Holm sentence packs the family, the four surviving values, their four thresholds, and the stopping point into one clause-chain; Section 4.1's leak-repair sentence runs five clauses, three re-judgments and a convention across the same breath; Section 4.5's "the eighty-first, whose observation replay is incomplete, closes none" arrives without an antecedent the reader can hold; and "Two of the three independent passes land at the forced floor" (§4.1, repeated in §6) is never expanded in place. None of these is wrong; each costs a re-read in a passage the argument depends on.
   - **5.3 [minor, fixable]** Section 4.1 attributes the leak discovery to the audit: "The audit in Section 4.3 exposed two channels through which material the confirmation stage was forbidden to read had reached it." Section 4.3, as printed, contains the pair audit, the case-level audit, the two mechanisms, the rebuild, and the expectation-framing check — but no account of the leak discovery, which appears only in Section 4.1. A reader who follows the cross-reference finds nothing there.
   - **5.4 [minor, fixable]** Section 4.5's identification argument does not hold as printed for the pair it most needs. The paper argues that on the primary backbone "each lettered perspective's cells carry its own vocabulary and no other", then prints A as {Neutral, Refuted, Confirmed} and B as {Neutral, Confirmed, Refuted} — the same value set. The content check therefore separates C (weak-refuted) and D (cognition vs. source vocabulary) but not A from B, and the census's headline row is an A row. Either give the distinguishing signal for A vs. B or drop the claim and say what does the identifying.
   - **5.5 [minor, fixable]** Terms are used before they are defined and one is directionally confusing. "The deployment's convention" and "the forced reading" appear in the abstract and in Section 1's bullets but are defined only in Section 4.1; "suppression" is defined once as "the share of the 30 negatives an arm does not confirm", so that a larger value is better, which reads backwards in "cuts suppression from 21/30 to 12/30" (§4.4); and "the contract-only core, a blind baseline" (§4.4) never says in what sense the core is blind.
   - **5.6 [minor, fixable]** Contribution 3 in Section 1 says the census is "supported by a twelve-configuration study that supplies the 243 judgments." The 243 judgments are the deployed configuration's alone (§4.5); the twelve-configuration study supplies 2,916. Reword so the count is not attributed to the wrong object.
   - **5.7 [minor, fixable]** Internal project labels leak into the text and into the shipped paths without definition: "the RQ1 detection-ability experiment" (§4.2) and `rq2/prompts/`, `rq2/analyses/` (§4.1, Data Availability). A reader outside the project cannot tell what RQ1 and RQ2 are.
   - **5.8 [minor, fixable]** Section 4.1 says the flat judge "keeps the protocol's red lines," while Section 4.4 lists "the red-line set" as one of the five things the four-perspective contrast changes. Both can be true (the flat judge keeps some red lines; the full stage carries a larger set), but the two statements are left for the reader to reconcile.

### Questions for Authors

- **Q1:** If the second backbone's dispatch were repaired (one definition of the four perspectives) and its 243 judgments re-read, does the error mass return to the unguarded clause? — the background is item 2.5; if the pattern reproduces under a repaired dispatch, that item's severity drops, and if it does not, the abstract's "80%" needs a stronger statement of the conditions under which the census holds.
- **Q2:** Given that A and B print the same value vocabulary, what signal identifies which letter is the contract perspective, and what do the recorded rationale strings behind the 50 A=Refuted closures actually say? — affects 2.6 and 5.4; either answer would let a reader see whether those closures are mechanical containment failures (the paper's characterization) or evidence-based refutations that the census misattributes.
- **Q3:** Is `milvus_001` one of the 51 true bugs or one of the 30 negatives, and what do the headline contrasts look like with it excluded? — affects 2.11; the direction of the "point" the paper says eleven configurations are credited with depends on the answer.
- **Q4:** Is there any evidence separating "C is accurate because the verbatim guard works" from "C is accurate, and the guard is incidental"? No arm in Table 2 drops the by-design guard, so the recommendation is currently to *add* a guard to A; if the guard is what keeps C clean, the correct prescription is different. — affects 2.1 and the Section 5 lesson in 3.4.
- **Q5:** What did the two interventions cost in human effort — the 134-pair classification, the 12-assertion case audit, the 20 hand-adjudications, and the twelve configurations × 3 runs? — affects 3.3; without a figure, the paper's central methodological advice cannot be budgeted by a reader deciding whether to adopt it.


---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Importance & Scope | Excellent | Excellent | Excellent | **Excellent** |
| Insights & Evidence | Adequate | Adequate | Excellent | **Adequate** |
| Perspective | Excellent | Excellent | Excellent | **Excellent** |
| Verifiability | Excellent | Excellent | Excellent | **Excellent** |
| Presentation | Adequate | Excellent | Adequate | **Adequate** |
| **Recommendation** | **Accept** | **Accept** | **Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three recommendations land on Accept, so the unanimous shortcut decides outright. Three of the five criteria are now **consensus Excellent** — Importance & Scope, Perspective and Verifiability — and Verifiability has held there for two consecutive rounds since the anonymous snapshot was brought current, which is the first time in this project that the lever criterion has stayed up across a round boundary rather than oscillating with the shipping state.

Insights & Evidence is the one criterion held at Adequate by consensus, on a 2–1 vote, and the split is now precise enough to name. All three reviewers converge on the same factual bound: the census is a primary-backbone measurement whose second-backbone attempt produced the opposite pattern. R1 and R2 hold the tier there and both go further than the previous round — R2 rates it `[major, fixable]` and observes that the paper's own remedy is already in its data, since the content-based letter identification it performs on the primary could be applied to the second backbone's shipped cells; R3 dissents upward because it weighs the cross-tab and the invariance checks as sufficient for the claim the paper actually states. That is a difference of weighting, not of fact, and it is the round's one substantive disagreement.

The other two `[major, fixable]` items — a second reader for the pair audit (all three reviewers, fourth round running) and the bundled four-perspective contrast (R1 and R3) — are both bounded by things the paper already discloses, and neither reviewer made the verdict conditional on either. Presentation remains at consensus Adequate, and this round's presentation findings are overwhelmingly **defects the author introduced while fixing the previous round's**: the Holm family's stated rationale, a missing citation key on a newly added sentence, an em-dash followed by a comma, a count attributed to the wrong object. That pattern, not any single item, is what the author should take from this round.

### Priority Revisions
Ranked by impact on the verdict. Every item is `[minor]`; the three `[major, fixable]` items are addressed first and each is bounded by a disclosure the paper already carries.

1. **Apply the primary's content-based letter identification to the second backbone.** R2 rates this `[major, fixable]` at 2.7 and R1 at 2.5 — the same remedy, independently reached, and R2's framing is the sharpest: the second backbone's cells ship, the paper already reports the D-cell vocabulary split (217 of 243 against 98 of 243), and `clause_tally.py second` reads them, so re-running the census under content-based identification is a replay rather than a new experiment. Either outcome is worth having — a surviving reversal makes the census a two-backbone result, and a vanishing one converts "uninterpretable" into a measured incomparability. This is the only `[major]` item in the paper's three rounds that is fixable without new runs and would move the one criterion still at consensus Adequate.

2. **Put a second reader on the pair audit.** All three reviewers reach it again — R1 at 2.6, R2 at 2.8, R3 at 2.10 — and R1 sharpens it with a comparison that should sting: the bug study the paper cites as its own premise used multi-stage annotation at κ > 0.95, and the paper's 43.3% is one reader with no reliability estimate. The pair verdicts ship, so a re-coding of a sample is a revision task. It has now been the reviewers' most consistently repeated request across four rounds.

3. **Take the bundling seriously in the Conclusion, which is the cheaper half.** R1 rates it `[major, fixable]` at 2.5 and R3 at 2.9; R3's version is the one to act on: §8 opens with "the answer on this pool is not the judge's internal organization" and evidences it with the four-perspective contrast alone, while §4.4's own step ladder shows a one-line schema field and the routing clause each moving the outcome. The body is careful and the Conclusion is not. Naming the bundle rather than generalizing costs a clause.

4. **Count before asserting — including counts about your own fixes.** R2's item 2.10 is a live arithmetic gap in the counterfactual's ceiling argument (eight of the fifteen cases are negatives, so the ninth interception must come from outside the fifteen, which the sentence does not describe), and the round's presentation findings are dominated by errors introduced in the previous round's repairs: the Holm rationale stated wrong in the sentence that added it, CASCADE characterized without its citation key, an em-dash followed by a comma, and contribution 3 crediting the twelve configurations with the deployed stage's 243 judgments. Four of this round's findings sit in text less than an hour old. The discipline that would have caught all four is the same one that caught "Sixteen paired tests" last round, and it should be applied to repairs as strictly as to original claims.

5. **Give the survivor rates and the remaining disclosures their bases.** R1 at 5.2 and 5.4, R2 at 5.3, R3 at 2.11 and 5.7 converge on the same class: the two full-family controls are never named, "the RQ1 detection-ability experiment" carries a label the paper never defines, `milvus_001`'s ground-truth class is never stated although the direction of the credit it earns depends on it, and §4.2's "substantial share" of the 81 that sits on versions the voided runs covered is left unquantified in a passage whose whole argument is attribution. Each is one clause.
