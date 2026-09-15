## Reviewer 1: Domain Expert

**Overall Recommendation:** Accept

### Summary

The paper studies how an LLM-based confirmation stage behaves when it decides whether a candidate
defect in a vector database management system (VDBMS) is real. It reports three things. First, a
mining campaign: 81 submissions across Milvus, Qdrant and Weaviate adjudicated by maintainers, of
which 51 were confirmed and 23 fixed by merged PRs, recorded in a 132-row ledger spanning 19
versions, with the ledger explicitly not usable as a per-version detection rate because the runs
that would have measured detection were voided. Second, an audit of the evidence packages that the
confirmation stage reads: every one of the 134 (constraint, cited-page) pairs the packages carried
was checked against the page it cites (18 supported as cited, 58 mis-anchored, 58 unsupported), the
packages were rebuilt, and two leakage channels found by the same audit were stripped and the
affected cases re-judged, so every rate in the paper is computed on the cleaned pool. Third, a
clause-level census: the deployed judge's 243 judgments (81 cases, three runs each) on the primary
backbone classified by the first aggregation clause that decides each judgment, cross-tabulated
against the audit strata, with a counterfactual that routes the unguarded refuting clause instead
of closing on it.

The study is conducted on frozen per-case materials across twelve judge configurations (eight on a
primary backbone, four on a second), three runs each, with paired exact McNemar tests at both a
case-set level and a recall level, both Holm families reported, and the deferral channel priced
under three readings (the deployment's convention that a routed case counts as confirmed, forced
verdicts, and a hand-adjudicated joint reading). A separate section runs the released crash-oracle
fuzzer against one target and records zero oracle anomalies.

### Core Strengths

- **S1:** An audit of the confirmation judge's *input* — a step the paper argues nobody measures —
  with a three-way pair-level split (13.4% supported as cited, 43.3% mis-anchored, 43.3%
  unsupported), a blind second reader at κ = 0.75, an expectation-framing check over all 81
  rebuilt packages, and the two leakage repairs the audit forced; all rates in the paper are then
  recomputed on the cleaned pool. — see 2.5, 4.2.
- **S2:** The clause census is identified rather than assumed: the perspective letters are pinned by
  their cell content, the load-bearing count is computed only on maintainer-confirmed labels, the
  count is invariant across both aggregation rules the dispatch prints, and the rival explanation
  that the census is the pair audit resurfacing is ruled out by a cross-tabulation. — see 2.2, 2.3,
  2.4.
- **S3:** The counting convention is priced rather than hidden: the forced-verdict reading is
  reported beside the convention for every contrast, the convention itself is priced at the arms'
  levels and again at the headline contrast, the headline routing change is re-priced by hand and
  falls from nine to three, and the paper closes that pricing in its own voice with the verdict
  that the deployed change is "suggested, not established". — see 2.6.
- **S4:** Provenance and limits are stated at the load-bearing claims (no detection rate; the
  fix-PR table is not shipped; three analyses are printed but unscripted; the census is
  primary-backbone only), and the artifact is live and matches what the Data Availability
  statement promises. — see 1.2, 4.1, 4.2.

### Core Weaknesses

- **W1:** The census — the paper's own headline claim ("the protocol guards the clause that is
  already clean") — is one backbone deep and reverses on the only other backbone measured, where
  the guarded clause closes 50 judgments and is wrong 22 times and the unguarded clause supplies
  50% rather than 80% of the incorrect False-Positive closures. The paper discloses this throughout
  and scopes the claim accordingly, so it is a ceiling on reach rather than a false statement; but
  a reader cannot yet take the prescription as a property of the protocol. — see 2.7.
- **W2:** The negative half of the ground truth is weak: 19 of the 30 false positives are the
  authors' own calls and there is no inter-annotator study, so the suppression, leaked-false-
  positive, net and F1 figures — including the "nine more false positives released" half of the
  counterfactual — rest on labels the paper itself cannot defend as strongly as the maintainer
  labels. The paper isolates the error counts to maintainer-confirmed labels, which is the right
  move, but not the FP-side cost estimates. — see 2.8.
- **W3:** The counterfactual prices the wrong intervention: the paper prescribes a verbatim-
  evidence guard on contract refutation, but the replay routes *every* judgment the clause closes,
  so the "+7 true bugs / −9 false positives" figure is an upper bound for a cruder intervention
  than the one the Discussion recommends. — see 2.9.
- **W4:** Related-work coverage has one visible hole: Testora (ICSE 2026, "Using Natural Language
  Intent to Detect Behavioral Regressions") is the closest published premise to this paper's own —
  an expectation read from informal prose, judged against an implementation — and it is never
  cited or positioned, although it sits in the project bibliography. — see 3.4.

### Detailed Assessment

1. **Importance & Scope** — Excellent
   - **1.1** The paper locates its problem precisely rather than gesturing at "VDBMS bugs". Section 2
     separates *consistency* (does behaviour match the documentation) from *correctness* (is the
     top-k right), states that only the former is measured, and Table 1 places every oracle family
     at its anchoring site — crash signal, differential testing, metamorphic relations,
     property-based/schema oracles, structured-source oracles, documentation-derived oracles — with
     the structural reason each misses untagged system-level behavioural prose. I checked the named
     works: VDBFuzz's oracle is crash-only by its own statement and its future work names
     correctness oracles as the gap; Metamon's falsifier is another LLM question; CASCADE's
     falsifier is a regenerated implementation; LogicHunter consults and executes the
     implementation freely; TRACE measures the implementation-drift blind spot; the oracle-authority
     survey does report hallucination named far more often than measured. The positioning holds at
     the level of the individual works, not just at the level of families.
   - **1.2** Scope is drawn at every load-bearing claim, which is what makes the rest of the paper
     usable. Section 4.1 gives the pool's provenance in full (51 maintainer-confirmed positives and
     30 negatives of which 11 carry a maintainer disposition, one unjudgeable case, the 132-row
     ledger of which 49 await a maintainer and 2 are withdrawn); Section 4.2 refuses to convert the
     ledger into a detection rate ("we cannot supply one") and explains why the adjudication
     survives the voided measurement; Section 4.5 scopes the census to the primary backbone; and
     the Threats section restates the limits. For a paper whose subject is its own pipeline, this
     is the right discipline and it is sustained rather than perfunctory.
   - **1.3 [minor, fixable]** One motivation step is asserted rather than evidenced: Section 1's
     "We target a prevalent subset: documentation–implementation bugs". The silent-majority premise
     is supported by the VDBMS bug study (functional failure 57.3%, crash 15.1%), but that symptom
     class includes the query-correctness bugs Section 2 explicitly excludes, so it does not
     establish the prevalence of the documentation–implementation sub-class. One sentence bounding
     the claim (e.g. "the sub-class's prevalence is not separately measured; the 51 confirmations
     show it exists at reportable scale") would remove the only context gap I found in the paper's
     framing.

2. **Insights & Evidence** — Excellent
   - **2.1** The method is fitted to the question: the confirmation stage's evidence is frozen per
     case, so the twelve configurations read from the same frozen packages and any difference is
     the dispatch, and the statistics are paired exact McNemar at two levels with the discordant-pair
     convention (a/b) defined once and the family choice reported both ways. I recomputed the
     printed p-values from the discordant pairs — 0/9 → 0.0039, 0/14 → 0.0001, 16/2 → 0.0013,
     2/14 → 0.0042, 12/1 → 0.0034, 18/2 → 0.0004, 0/5 → 0.0625, 1/6 → 0.1250 — and every one is
     exact; the net identity (39 − 9 = 48 − 18 = 30) and the F1 values (0.821 and 0.788) also
     follow from the printed counts. The numbers I re-derived all check out, which is not something
     one can say often.
   - **2.2** The census is identified, not assumed (Section 4.5). Every recorded cell carries a value
     from its perspective's legend, and the ambiguity introduced by the dispatch's doubled
     definition of the perspectives is handled by content: no cell outside C records a *weak*
     refutation (C = Confirmed 72, Neutral 71, Weak-Refuted 59, Refuted 41) and no cell outside D
     carries the source vocabulary. The nineteen judgments the census closes by C = Refuted are then
     read individually and split by the evidence they rest on (15 comment/docstring, 2 a server-side
     name-validation rule, 2 code structure), which is how the paper shows the verbatim requirement
     was not applied uniformly — a compliance hole the aggregation-replay recount cannot see.
   - **2.3** The load-bearing count is made robust in three ways that each close a different escape
     route: it is computed on maintainer-confirmed labels, so the 30 self-adjudicated negatives
     cannot move it; it is invariant across the two aggregation rules the dispatch prints, because
     contract refutation assigns False-Positive under both; and it survives the leak repairs, which
     were applied before these judgments were recorded. The pre-repair counts (47 and 20 rather than
     50 and 19) are disclosed alongside.
   - **2.4** The strongest analytical move in the paper is the cross-tabulation that separates the
     census from the audit (Section 4.5): if the 24 wrong closures were simply defective citation
     rows failing a containment check, the prescription would be to fix the material, not the
     clause. The stratum breakdown answers it — 20 of the 24 fall on the 59 cases whose rebuilt
     packages carry documented evidence, none on the eighteen the audit left without any — and the
     paper explicitly notes that the strata are a different object from the twelve assertion-level
     rows of Section 4.3. The rival selection explanation is raised by the authors themselves and
     answered on error mass.
   - **2.5** The pair audit (Section 4.3) measures a step that the paper argues every pipeline in
     this line performs and none reports (to its knowledge), and it is done with the checks the
     claim needs: the version the row claims, the packages as produced before the rebuild, a blind
     second reader on a stratified sample (30 of 36 agree; κ = 0.75; all 12 SWAP pairs re-called as
     SWAP; the six disagreements sit at the two boundary types), and a verification that the rebuilt
     set contains no expectation-framed sentence (19 hits, all verbatim server responses quoted as
     observations). The interpretation is correctly restrained — "this distiller on these three
     vendors' documentation", not LLM distillation in general.
   - **2.6** The paper treats its counting convention as a first-class object of measurement rather
     than a reporting choice. Section 4.1 states the convention and its price (a configuration that
     routes more scores higher on recall) and says where the convention is priced: "the forced-verdict
     reading beside it for every contrast", and the convention itself at two places, the arms'
     levels and the headline contrast. Section 4.4 does exactly that — the arms' levels include the
     hand-adjudicated joint reading (33/51), while the four-perspective and evidence-access contrasts
     print convention and forced readings — and then re-prices the headline by hand (nine → three
     for the rule-bearing control, four for the deployed stage), calling that a floor. Section 4.4
     and the Discussion both close on the same verdict, that the deployed change is "suggested, not
     established". The independent adjudicator's agreement (4, 5 and 6 of 20 under three protocol
     statements, κ = −0.01, 0.08, 0.11) is used to bound the joint reading rather than to support
     it. This is an unusually candid treatment of a favourable convention.
   - **2.7 [minor, fixable]** The census's reach is the paper's biggest exposure. Section 4.5's own
     cross-backbone paragraph reports that on the second backbone contract refutation closes 56
     judgments and by-design closes 50 of which 22 are wrong (so the guarded clause is *not* the
     accurate one there), and that the unguarded clause supplies 24 of 48 incorrect False-Positive
     closures — 50% rather than 80%. Worse for interpretation, the second backbone's D field cannot
     be identified at all, because the dispatch defines the perspectives twice with C and D
     exchanged and the schema follows different definitions for D and for C, leaving D carrying two
     incompatible vocabularies (217 of 243 cells there against 98 here) and the aggregation's D
     clauses firing twice against 23. The paper discloses this in the abstract, in contribution 3,
     in Section 4.5, in the Discussion and in the Threats section, and states that it "cannot rule
     out the letters meaning different things there" — so the claim it actually makes is scoped and
     supported. Tagged minor because what is exposed is a reader who over-generalizes, not the
     claims as made: the census is correct as a single-backbone result and the fix is more
     backbones (the authors have the pipeline and the frozen packages, so a guard-armed arm and one
     or two further backbones are within a revision's reach), or failing that, labelling the census
     a case study of one backbone in the title-level framing and not only in scope clauses.
   - **2.8 [minor, fixable]** The FP-side ground truth is materially weaker than the bug-side and the
     paper's own disclosure does not fully isolate it. Section 4.1 states that 19 of the 30 negatives
     are "our own calls" with no inter-annotator study and only 11 carry a maintainer disposition.
     Every load-bearing error count is then correctly restricted to maintainer labels (the 24 and
     the 80% share are closures that fell on confirmed bugs), which is the right design. But the
     suppression rates (21/30, 12/30, 0.467 → 0.400, 0.933 → 0.900), the "nine more false positives
     released" half of the counterfactual, and the net and F1 comparisons that the paper uses to
     declare source-withholding a tie all rest on those 19 self-adjudicated negatives. Tagged minor
     for the same reason as 2.7 — the counts the paper's argument leans on are isolated to
     maintainer labels, so what rests on the self-adjudicated negatives are the FP-side figures
     rather than the error counts. A second reader on the 30 negatives, of the kind the paper
     already ran on the pair audit, would settle whether the FP-side conclusions move; without it,
     the FP claims are the least verifiable quantitative content in the paper.
   - **2.9 [minor, fixable]** The counterfactual prices a different intervention from the one the
     paper prescribes. Section 4.5's prescription is an evidence guard on contract refutation, but
     the replay routes to human review *every* judgment the clause closes ("everything else held at
     the recorded perspective values"), including the 26 correct closures, and reports +7 true bugs
     / −9 false positives. The paper is candid that this is a replay and not a re-adjudication
     ("what cannot be computed from frozen data is whether a judge re-adjudicating those refutations
     under a verbatim-evidence guard would reach the same place") and calls seven the case-level
     maximum on the bug side — but the reader is never shown the cheaper measurement that *is*
     available: the rationales for the 50 A = Refuted closures are in the frozen record, and
     classifying them by evidence kind, as Section 4.5 already does for the 19 C = Refuted
     judgments, would price the guard itself.
   - **2.10 [minor, fixable]** The design is a decomposition assembled during the study rather than a
     pre-registered set, and the paper says so. Three contrasts change more than one thing, and the
     four-perspective contrast changes five (perspectives, aggregation-rule text, red-line set,
     declared verdict field, cognition-corpus access), so "the organization does not change how
     many" is a bundle-level null on the primary and, on the second backbone, an undivided −11
     whose carrier is unknown. The paper states the bundle honestly ("With that label"), which is
     what makes this a weakness of attribution rather than of reporting.
   - **2.11 [minor, fixable]** One comparison in Section 4.1 should be labelled. The screening
     measurement reads "the stage confirms 19 of 32 (0.594) against 48 of the 81 (0.593) on the
     pool", where the 32 were re-adjudicated under the full-stage protocol minus the cognition
     perspective. The number 48 is also the deployed stage's confirmed-set size (39 true bugs + 9
     leaked false positives, Section 4.4), which is a *cognition-bearing* configuration. If the
     48/81 baseline is not produced by the same cognition-free protocol as the 19/32 figure, the
     two rates are not from the same instrument and the "does not separate the streams" reading is
     confounded; one clause naming the configuration would settle it.

3. **Perspective** — Adequate
   - **3.1** The Discussion's (§5) five lessons are concrete and each traces to a measured finding:
     audit what the oracle reads, not only what it concludes (from the Section 4.3 audit); put the
     evidence guard where the error mass is (from Section 4.5); price the deferral channel and price
     the contrast, not just the level (from Sections 4.1 and 4.4); check the dispatch before
     re-architecting the judge ("Check the dispatch before you re-architect the judge.", from the
     four dispatch defects reported in Section 1 and Section 5); and self-audit the stage against
     its own printed rules ("Self-auditing a stage against its own rules is cheap and informative.",
     on the Section 4.5 replay the lesson closes with "That is a five-line script."). The pricing,
     dispatch and self-audit lessons transfer to any LLM-judge pipeline with an escalation channel,
     and the audit lesson is cheap to apply (a sample of pairs against their cited pages); the guard
     lesson is the one item 3.2 qualifies.
   - **3.2 [major, fixable]** The signature lesson cannot be transferred as stated. The paper's own
     cross-backbone check moves the error mass to the *guarded* clause on the second backbone, and
     the Discussion concedes the point ("the rule is advice about where to look rather than a
     property of the protocol"). A practitioner cannot act on "put the guard on the clause with the
     error mass" without re-measuring on their own backbone — which is a legitimate lesson, but a
     weaker one than the Discussion's imperative phrasing suggests, and it is the lesson the
     contribution list leads with.
   - **3.3 [minor, fixable]** No lesson is validated by application. The paper rebuilds the packages
     and recomputes all rates on the cleaned pool, which is a real improvement to its own data, but
     it never runs the audited-and-rebuilt discipline on a fresh target (or with the guard in place)
     to show that following the discipline changes an outcome. For an experience paper this is not
     fatal — the measurements are the contribution — but it leaves the prescription at the level of
     "do measure this" rather than "this design works".
   - **3.4 [minor, fixable]** Related-work coverage: Testora (ICSE 2026, "Using Natural Language
     Intent to Detect Behavioral Regressions") is the nearest published relative of this paper's
     premise — an expectation derived from informal prose that an implementation is then judged
     against — and it appears nowhere in Section 7 or anywhere else in the text, although it is in
     the project bibliography (uncited entries do not render, so a reader cannot tell). It is at a
     different granularity (change descriptions rather than API documentation) and a comparison
     need not be quantitative, but the delta should be stated in one sentence, exactly as the paper
     does for Metamon and CASCADE.

4. **Verifiability** — Excellent
   - **4.1** The artifact is declared and live. I resolved the anonymous URL and read the package's
     README: it ships the submission ledger, the 81 frozen packages (post-rebuild,
     cognition-stripped), the per-case verdicts for every arm and run with the re-judged files and
     the pre-repair states beside the untouched batches (so either pool can be reconstructed),
     both dispatch generations, the English prompt renderings under `rq2/prompts/`, the pair-audit
     verdict records with the blind second reader's own classification file beside them, and the
     five analysis scripts under `rq2/analyses/` that Section 4.1 names one by one with what each
     recomputes.
   - **4.2** The paper states in-text what is *not* shipped or scripted: the fix-PR characterisation
     is outside the artifact and is flagged as such; the catch-all composition, the
     expectation-framing check and the C row's evidence classification are printed but not scripted,
     with the artifact's script-coverage note saying so. For a paper whose methodological claim is
     that the pipeline is auditable, a verifiability claim that lists its own gaps is worth more
     than one that does not.
   - **4.3 [minor, fixable]** Two limits a replicator should be told at the Data Availability
     statement rather than mid-method. Both backbones are serving aliases without pinned weights, so
     what is reproducible is the *recomputation* from frozen verdicts, not the experiment; and the
     adjudication basis for the 30 negatives lives in the ledger and the worksheet the Data
     Availability statement names, not in a script, so the weakest ground truth is also the least
     automated part of the package.

5. **Presentation** — Adequate
   - **5.1** The structure is sound and the tables carry the load: the oracle-family table, the
     twelve-configuration table (with perspectives, rule, source and backbone as separate columns),
     the pair-audit split with its caption guarding against summing the two 43.3% shares, and the
     clause census grouped by the outcome each clause assigns, with the catch-all's composition
     shown as bugs/FPs rather than a rate. Quantities are named consistently across the paper
     (39/51, 48 vs 66, the routed queue of 25 vs 11), and the discordant-pair convention — the arm
     whose count is printed first is the *a* of *a/b* — is stated once and holds in the contrasts I
     checked.
   - **5.2 [minor, fixable]** Several sentences need a second pass because their subject is missing
     or displaced, and they cluster where the paper is most compressed. The abstract's "The census
     is measured on the primary backbone, where the two letters the dispatch defines twice are
     settled by their content, and not reproduced on the second" has no subject for "not
     reproduced"; Section 4.1's "ten rebuilt packages carried an embedded maintainer-cognition
     section their dispatches forbid" reads as though the packages own the dispatches; Section 4.4's
     "the two source-only configurations 20 and 19 forced (36 and 37 convention, the two recall
     figures quoted below)" is a parenthetical that requires the reader to hold four numbers and
     then hunt forward for 0.706 and 0.725.
   - **5.3 [minor, fixable]** The oracle-family table and Section 7 disagree on the membership of
     one row: Table 1 lists documentation-derived oracles as @tComment, JDoctor, DocTer, RBCTest,
     RESTInfer, while Section 7 puts Toradocu in the tagged-Javadoc group and ICON in the
     REST-side group. Toradocu and ICON each appear in one list and not the other.
   - **5.4 [minor, fixable]** Section 4.3's "replaying the observation against the operator's page"
     uses "operator" without definition; every other occurrence in the paper is "vendor" or "the
     system", so the reader cannot tell whether a different actor is meant.
   - **5.5 [minor, fixable]** One figure (the pipeline) is thin for a paper whose central object is
     a decision procedure. The census — the paper's claim — is a table of clauses; a small
     firing-order diagram (A → B → D → C → catch-all with the recorded cell counts) would let a
     reader see the selection structure that Sections 4.5 and 5 argue about, and would have made
     the "middle of the three clauses that assign False-Positive" claim checkable at a glance.

### Questions for Authors

- **Q1:** The 50 A = Refuted closures have recorded rationales in the frozen packages: can you
  classify them by evidence kind as you already do for the 19 C = Refuted judgments, and price the
  verbatim-evidence guard itself rather than a routing replay? — [drawn from 2.9; if most closures
  carry no evidence, the +7/−9 figure stands as priced and 2.9 stays minor; if most carry verbatim
  evidence, the prescription's cost is overstated and 2.9 becomes a genuine correction.]
- **Q2:** What would have to hold for the census pattern to be a property of the protocol rather
  than of a backbone — a model family, a documentation style, a routing rate? — [drawn from 2.7;
  naming the conditions would let a reader judge whether their setting is in scope and would move
  2.7's assessment up, because the claim could then be read as conditional rather than anecdotal.]
- **Q3:** Would a second reader on the 30 negatives, as you ran for the pair audit, move the
  suppression rates and the net/F1 tie that the source-withholding conclusion depends on? — [drawn
  from 2.8; a robustness check of the same kind the paper already trusts elsewhere would move 2.8
  up; failure to move it would confirm the tie as the paper states it.]
- **Q4:** The four-perspective contrast bundles five changes and costs 11 true bugs on the second
  backbone: which of the five carries that loss — the perspectives, the aggregation clause table,
  the red-line set, the verdict field, or the cognition corpus? — [drawn from 2.10; isolating even
  one component would change the contrast from a bundle-level null to an attributable one, moving
  2.7 and 2.10 up.]
- **Q5:** Within the bug study's functional-failure class, how much is documentation–implementation
  inconsistency of the kind you target, as opposed to query-correctness failure? — [drawn from 1.3;
  an answer from your own pool (51 confirmations of a documented violation) would upgrade the
  prevalence claim, though it would not change criterion 1's tier.]


---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Accept

### Summary

The paper reports three artifacts from one LLM pipeline that mines documentation–implementation bugs in three vector database systems. First, a campaign ledger: of 81 adjudicated submissions, maintainers confirmed 51 and merged fixes for 23, across 16 of the ledger's 19 covered versions; the per-version detection-ability experiment was voided in full for dispatch-discipline violations, so the ledger is presented as a record of submissions and adjudication rather than a detection rate. Second, an audit of the material the pipeline's confirmation stage reads: all 134 (constraint, cited-page) pairs were checked against the page each cites, splitting 18 supported / 58 mis-anchored to a source file or landing page / 58 unsupported by the cited page, with a case-level pass over 12 headline assertions; the same audit exposed two leakage channels (embedded maintainer-cognition sections in ten packages; runtime cognition files citing candidates' own issue numbers), both repaired, after which every reported rate is recomputed. Third, a clause-level census of the deployed confirmation stage's 243 judgments (81 cases × three runs, primary backbone), which finds contract refutation — the clause carrying no evidence requirement — closing 50 judgments and being wrong on 24 of them, against the verbatim-guarded by-design clause's 19 closures and 17 correct; a replay that routes contract refutation moves recall 39/51 → 46/51 and suppression 21/30 → 12/30 under a counting convention that credits a routed case, and changes nothing under forced verdicts.

Twelve judge configurations over two model backbones supply the contrasts: a rule-bearing judge beats the flat judge on both backbones at the confirmed-set level and at recall, most of the gain being deferral; the four-perspective organization shows no advantage on the primary backbone (39 vs 39 at recall, p = 1.0) and costs 11 true bugs on the second (p = 0.0034), while forced-verdict counts are equal on both with different decision sets. Withholding the implementation source raises recall 39 → 48 and releases nine more false positives, leaving net true positives minus leaked false positives identical and the F1 interval spanning zero.

### Core Strengths

- **S1:** The clause census is a real instrument, and its central number is defended against the two rival explanations a specialist would raise first — that the errors are the pair-audit's material finding resurfacing, and that the clause merely sees the hardest cases — using a stratified cross-tab over the package strata and an explicit error-mass argument. — see 2.1, 2.4
- **S2:** The reporting discipline is exceptional and it survives checking: every prevalence rate is recomputed on the cleaned pool after two self-found leaks, every contrast is given under both counting readings, an independent adjudicator's disagreement (κ = −0.01 / 0.08 / 0.11) is reported and used to demote the authors' own hand reading to a bound, and the printed exact-McNemar p-values and the two Holm families reproduce on the counts printed. — see 2.2, 4.2
- **S3:** The pair audit measures the input to an LLM oracle — a step this literature names but has not quantified — with a blind second reader on a stratified sample (30 of 36, κ = 0.75), a separate case-level pass over the 12 headline assertions all of which were acted on, and a sweep of the rebuilt set for expectation-framed sentences (0 of 81). — see 2.3, 3.1
- **S4:** The positioning against the closest competitors holds up under verification: Metamon's quoted profile (precision 0.722 at recall 0.480) is exact and its falsifier is indeed another LLM question; MASTOR's oracles are indeed source-authoritative, and its authors' own stated limitation ("cannot detect violations of intended requirements that are not reflected in code") is exactly the gap this paper targets; ManyMinds measures bias rather than accuracy; TRACE's implementation-drift asymmetry is reported correctly. — see 3.4
- **S5:** The four-perspective conclusion is argued from invariances that the bundled contrast cannot explain — equal forced-verdict counts on both backbones (27/27, 26/26) with decision sets differing on 5 and 3 cases, a primary-backbone interval that excludes an effect larger than about eleven points, and a second backbone where the same arm loses 11 true bugs. — see 2.5

### Core Weaknesses

- **W1:** The paper's most actionable claim — "put the evidence guard where the error mass is" — is priced by a different intervention. The replay routes *all* 50 contract refutations (§4.5), while the prescription asks for an evidence guard; the paper classifies the 19 by-design closures by what they rest on but never classifies the 50, so how much of the guard's cost is already paid, and whether a guard releases fewer than nine false positives, is unmeasured. — see 2.6
- **W2:** The audit's headline rate is measured on the generation that the repair replaced, so no configuration studied read the material the 43.3% describes, and the rebuilt generation is never re-measured at pair level; the audit-and-rebuild discipline is therefore demonstrated on the way in but not on the way out. — see 2.7, 4.3
- **W3:** The census is a one-backbone result that reverses on the second (contract refutation supplies 50% of incorrect False-Positive closures there and the guarded clause is the inaccurate one), which the paper states but which bounds the transferable rule to "measure your own clause-level error mass". — see 2.8
- **W4:** Related-work positioning has a mechanical gap: the shipped `.bib` contains 22 entries that no `\cite` in the text reaches, among them two whose titles name this paper's own axis, so in an ACM build they never render and the delta against them is never drawn. — see 3.5

### Detailed Assessment

1. **Importance & Scope** — Adequate
   - **1.1** The residual is located precisely and the reason it is unattacked is structural rather than rhetorical: Section 2 walks the oracle families and Table 1 anchors each somewhere other than untagged, system-level behavioural prose, with the one exception (documentation-derived oracles) sitting below system-level granularity and keeping the derived oracle as final arbiter. The observation that no cross-vendor reference adjudicates which of two behaviours is the bug is correct for this domain and is what makes the expectation provenance question load-bearing.
   - **1.2** Boundaries are stated repeatedly and not buried: §4.1 fixes the pool's composition (51 maintainer-confirmed bugs; 30 negatives, 11 with a maintainer disposition and 19 the authors' own), §4.2 states that the detection-ability experiment was voided and that the ledger is not a rate, §4.5 scopes the census to the primary backbone, and the Introduction's third result bullet says the census does not reproduce on the second. A reader is never left to discover a scope limit.
   - **1.3 [minor, fixable]** The scope is narrower than the problem statement in one direction the paper does not fully price: the pool is one pipeline's *submission-filtered* output, so "51 of 81" describes that pipeline's admission behaviour and nothing about the class's detectability, and with the detection runs voided no bound on what the pipeline misses exists. The 19/32 screening check is the nearest thing offered, and §4.1 says explicitly that it "does not separate the streams"; comparing it against 48 of the 81 also sets a cognition-free re-adjudication beside the deployed stage's own confirmed-set count, which is a different configuration. Stating the comparator and what the screening check can and cannot move would close this.

2. **Insights & Evidence** — Adequate
   - **2.1** The census is well-defined operationally before it is used: §3.5 fixes the aggregation order, names the clause that decides as the first in that order, and the census table of §4.5 then reports per-clause closures with right/wrong counts. The arithmetic reconciles: the three False-Positive-assigning clauses supply 24 + 2 + 4 = 30 incorrect closures, so "24 of the 30, 80%" is exactly the share of that denominator, and the case-level version (15 cases closed by the clause in ≥2 of 3 runs, 7 true bugs, 8 negatives, plus one negative released from a single-run closure) accounts for the seven and nine of the counterfactual.
   - **2.2** The statistics are checkable and check out. The exact McNemar p-values printed throughout reproduce from the printed discordant pairs (e.g. 0/5 → 0.0625; 2/6 → 0.2891; 12/1 → 0.0034; 16/2 → 0.0013; 0/9 → 0.0039), the stated test family matches the paper (20 paired tests, exactly 10 at the recall level), and both Holm readings are arithmetically right — the four smallest recall-level p-values clear α/10, α/9, α/8, α/7 and the sequence stops at 0.0225; read as 20 tests, exactly seven clear and the stop lands on the first 0.0039. Statistical claims of this density usually contain an error; this set does not.
   - **2.3** The audit's construction is stronger than a rate report: the three-way split is defined by what the anchor *is* rather than by a similarity judgement ("a `constant.go` path or an API landing page carrying no endpoint documentation"), the case-level object is explicitly separated from the pair-level object, the two dominant mechanisms are named (version drift from one fixed-version contract; conceptual-only documentation where constraints exist as prose but not as values), and the failure mode this class of work invites is swept for (19 expectation-phrased hits, all inspected and all verbatim server responses).
   - **2.4** The census anticipates the causal objection: if the 50 refutations were driven by defective rows, the prescription would be to fix the material. §4.5's cross-tab answers with the package strata — 20 of the 24 wrong closures fall on the 59 cases whose rebuilt packages carry documented evidence (20 of their 177 judgments, rate 0.11), four on the three weak-evidence packages, and none on the eighteen the audit left without documented evidence — so the clause fires on material the audit passed. It also checks invariance across the two printed aggregation rules, and anchors the load-bearing count on maintainer-confirmed labels so that it does not rest on the authors' own negatives.
   - **2.5** The four-perspective result is the paper's cleanest piece of argumentation because it does not lean on the significance of a bundled contrast: forced-verdict recall is identical on both backbones (27/27, 26/26) while the confirmed sets intersect in 22 of 27 and 23 of 26, and on the primary backbone the recall-level interval excludes an effect larger than about eleven points without the paper claiming equivalence. The second backbone then supplies the negative direction at the recall level (−11, p = 0.0034), so the finding is a two-backbone statement rather than a null.
   - **2.6 [major, fixable]** The prescription and its price are different interventions. §4.5 prices *routing contract refutation to human review, everything else held at the recorded perspective values*, which is a whole-clause relabel; §5 (Discussion) then attaches that price ("seven true bugs gained and nine false positives released") to "put the evidence guard where the error mass is". A guard would leave A = Refuted closures that already clear a verbatim-intent bar in place, so the replay bounds the guard's effect from one side only, and the direction of the bound is not stated: the guard recovers at most the seven bugs and releases at most the nine false positives. The material needed is in the artifact and the authors have already applied the method once — §4.5 classifies the 19 by-design closures into fifteen comment/docstring, two name-validation-rule and two code-structure closures and shows the last two do not clear the legend's bar — but the 50 contract refutations are never classified the same way. Either classify them, or restate the recommendation as the routed clause (which is what was measured).
   - **2.7 [minor, fixable]** The audit's object and the judges' object are not the same generation, and only the first is measured. §4.3 is candid ("the split describes the material as found rather than the material the judges went on to read"), yet the rebuilt packages are characterised only at case level (59 documented / 3 weak / 18 without) and by one negative sweep; a post-rebuild pair-level support rate is the natural closure of an audit-and-rebuild *discipline*. Relatedly, §4.3 says the unsupported bucket means "the cited page does not support the constraint, and for many no page does", while §5 (Discussion) renders it "43% had no support at all" — the two are not the same claim, and the universe-level count is the one that would let this paper claim the hallucination measurement its own related work (mughal26) says the field names but does not measure.
   - **2.8 [minor, unfixable]** The census does not reproduce on the second backbone (there contract refutation closes 56 and supplies 24 of 48 incorrect False-Positive closures, 50% rather than 80%, and by-design refutation closes 50 with 22 wrong), and the reason given — the dispatch's doubled perspective definitions leave D carrying two incompatible vocabularies there, with the aggregation's D clauses firing twice against 23 — is honest but means no revision can extend the finding. The paper's handling is correct (the scope is stated in the abstract, the intro, §4.5, §6 and §8), and I record it as a bound on the rule rather than a defect; it is the reason the transferable lesson is "measure where the error mass is" and not "guard clause A".
   - **2.9 [minor, fixable]** Several load-bearing comparisons rest on configurations that differ in more than the named variable, and the paper says so without fully compensating. The deployed-change decomposition (schema-line repair vs routing rule) exists only on the primary backbone, so on the second the "routing raises recall" result is the bundled contrast alone; the four-perspective contrast changes five things, of which two (the aggregation text and the red-line set) are the same ones the rule-bearing flat judge carries, which makes the label "four perspectives" do work the design does not isolate. Reporting each arm's routing rate would let a reader see how much of the −11 on the second backbone is extra abstention versus extra wrong decisions.

3. **Perspective** — Excellent
   - **3.1** The first lesson is genuinely new to this line and cheaply actionable: audit what your oracle reads, not only what it concludes. The paper makes it operational ("a sample of pairs against their cited pages tells you how much of your judge's input is unsupported"), supports it with a blind-reproduced measurement (30 of 36 agreement, κ = 0.75, all 12 SWAP pairs re-called), and — critically — crosses it against where the errors land, which is what turns a rate into a diagnosis. Doc2OracLL (fetched) establishes that documentation quality drives oracle quality at the level of Javadoc prose; it does not audit citation support of a distilled constraint, so the delta is real, though the phrase "the step nobody measures" should be read as "the pair-level citation audit", not as "documentation quality is unstudied".
   - **3.2** The second lesson — price the deferral channel and price the contrast, not just the level — is the one I would expect other groups to adopt. The paper shows the same change worth nine under the deployment's convention and three under hand-adjudication of the routed queue (§4.4), repeatedly swaps in the forced reading, and reports the identical net and overlapping F1 intervals for the source contrast rather than a win. Trust-or-Escalate (fetched) frames exactly this coverage-versus-risk accounting and, notably, reports that an uncalibrated hand rule achieves a 0% guarantee success rate against 90.8% for a calibrated one — which is the context a reader needs to judge the paper's own hand rule, and which the paper cites without drawing out.
   - **3.3** The third lesson — check the dispatch before you re-architect the judge — is supported by a memorable and checkable fact: a one-line schema repair moved five of the headline nine bugs (§5, Discussion), and none of the four dispatch defects was found by the authors' own audit. That the paper reports its own instrument's defects rather than repairing them quietly is the kind of practice that benefits the field, and the self-audit lesson (22 forward departures from the printed rule, 17 in the forbidden direction, ten on real bugs, from a five-line script) generalises beyond this deployment.
   - **3.4** The originality delta is drawn against named works I verified rather than a survey: Metamon (fetched — precision 0.722/recall 0.480 at threshold ≤ −0.1, judge is an LLM over a metamorphically transformed prompt, no non-LLM falsifier, matching the paper's characterization exactly), MASTOR (fetched — oracles grounded in implementation source, OAS claims unsubstantiated in source demoted to `pending`, and the authors' own limitation statement names the gap this paper targets), ManyMinds (fetched — measures bias, not accuracy; debate amplifies bias after round 0→1 and a meta-judge resists; the paper's gloss is fair and the currency difference is flagged), Doc2OracLL (fetched), and TRACE / Mughal's SLR (cached summaries — both characterizations accurate, including the "hallucination named far more often than measured" citation). No mischaracterization found in the paper's treatment of its competitors.
   - **3.5 [minor, fixable]** The `.bib` ships 22 entries that no `\cite` in the text reaches. Two of them name this paper's own axis: `testora26` ("Using Natural Language Intent to Detect Behavioral Regressions", ICSE 2026) and `exoracle26` ("Documentation vs. Code Patterns: What Drives LLM-Based Exception Oracle Generation?"). Under ACM's reference format uncited entries do not print, so a reader of the compiled paper never sees either, and the delta against the closest work on documentation-versus-code oracle authority is never drawn. I assert only their titles and venue (from the `.bib`, verified against the search APIs); positioning each in one sentence, as the paper already does for MASTOR and CASCADE, would close it.
   - **3.6 [minor, fixable]** The perspective the paper actually delivers is one notch weaker than the one it advertises in the Discussion heading. "Put the evidence guard where the error mass is" is bounded by the authors' own second-backbone result and by an unpriced guard; what travels is the weaker, still useful form: locate your clause-level error mass, and price the guard you place there. The Conclusion already says this ("the second backbone reverses it"); the Discussion's heading could too.

4. **Verifiability** — Excellent
   - **4.1** The artifact is declared and itemised in a Data Availability section that names each object a reader would need to re-derive a number: the pool, the frozen per-run verdicts of all twelve configurations, the packages the study read, the dispatch texts and the two judging prompts (in English, under `rq2/prompts/`), the pair-audit verdicts, the adjudication worksheet and the blind passes, plus five named analysis scripts under `rq2/analyses/` mapping to the claims they recompute (`recompute_paper_numbers.py`, `clause_tally.py`, `convention_pricing.py`, `bootstrap_net_f1.py`, `audit/pair_audit.py`, with `clause_tally.py second` for the second backbone). The method text is unusual in the same way: each control is described as a traceable edit of the arm it extends, down to the schema line and the per-case material line.
   - **4.2** Reconstructibility is designed in rather than asserted: "where a run was re-judged after either leak repair, the re-judged cases and the pre-repair state both ship beside the untouched batches, so either pool can be reconstructed from the package alone", and §4.1 says both raw generations ship alongside the cleaned one. The paper also states where it falls short instead of leaving it to be discovered — the catch-all composition, the expectation-framing check and the by-design row's evidence classification are "printed but not yet scripted" with an artifact-side coverage note.
   - **4.3 [minor, fixable]** One object is missing from an otherwise complete set: the Data Availability text says "the earlier rebuilt generations are archived separately and do not ship", and those are exactly the packages the pair audit was performed on. A reader can re-read the audit's verdicts but cannot re-audit the 134 pairs themselves, which is the one claim in the paper whose raw material is not in the package. Shipping the audited generation (or a pair-level file with each constraint, its citation and its verdict) would close it. Two further verifiability limits are disclosed and inherent — both backbones are serving aliases without pinned weights, so exact re-execution of the judge is not possible, and the rebuild's row-level accounting "does not fully reconcile in our own report", with the pair-level rates offered as the ones that do.
   - **4.4** On the declared link itself: I did not clone or run anything. I attempted to confirm reachability and must report the probe as inconclusive rather than as evidence either way — the anonymous host answered a non-browser request with HTTP 401 (`{"error":"not_connected"}`) and a control URL behaved identically, so the response reflects the host's handling of the client, not the repository's state. I therefore judge the artifact on its declared, itemised contents only.

5. **Presentation** — Adequate
   - **5.1** The structure is sound for what the paper does (Preliminaries → Approach → Evaluation with four sub-results → Discussion → Threats → Related Work → Conclusion), the three middle evaluation subsections state their question in italics before answering it, and the Threats section is unusually well matched to the paper's own weak points rather than a formality. Tables are few, correctly labelled, and the census table is a model of legibility; the one figure carries the pipeline.
   - **5.2 [minor, fixable]** The prose is at the density limit and several load-bearing sentences pack three claims into a relative clause, e.g. the abstract's "measured on the primary backbone, where the two letters the dispatch defines twice are settled by their content, and not reproduced on the second". Since the qualifiers here are the paper's own protection, burying them subordinates them to the number they qualify. The abstract is also long enough that its third paragraph (the census) reads as a second abstract.
   - **5.3 [minor, fixable]** The blind second reader's vocabulary is never introduced: §4.3 reports "all 12 SWAP pairs were called SWAP again, and the six disagreements are three at the DROP/SWAP boundary and three at SUPPORTED/DROP", but SWAP, DROP and SUPPORTED appear nowhere else in the paper and are not mapped to the three categories of Table 3 (supported as cited / re-anchored / no support). A reader checking the κ against the table has to guess the correspondence.
   - **5.4 [minor, fixable]** Mechanical nits, collected for convenience: spelling is mixed between British and American forms — "behaviour/behavioural" 16 times against "behavior" 5 times in the same sense (e.g. §3.5 "behavioural elegance" vs §4.5 "observed behaviour alone" alongside "observed behavior"); "distil" vs "distilled" is consistent within each form and needs no change. "favour" (§4.1) is the only British spelling of that word. Numerals and section cross-references are otherwise consistent, and no undefined references remain.

### Questions for Authors

- **Q1:** How many of the 50 contract-refutation closures rest on verbatim intent evidence of the kind the by-design legend demands (an in-source comment or docstring, or a maintainer quote)? §4.5 classifies the 19 by-design closures on exactly this axis but never the 50. — intended effect: if most of the 50 already clear a verbatim bar, item 2.6's rating would move up, because the guard would be nearly free and the replay would approximate its price; if few do, the +7/−9 replay is an upper bound on both sides and 2.6 stands as a must-fix.
- **Q2:** What is the pair-level support rate on the rebuilt packages, and how many of the 58 "no support on the cited page" pairs are unsupported by *any* page at the version claimed? — intended effect: item 2.7's rating would move up if the rebuilt set is re-measured (it would turn the audit from a one-way measurement into a demonstrated discipline), and the universe-level count would let the paper claim the hallucination measurement rather than only the citation-support measurement.
- **Q3:** The screening check in §4.1 compares "19 of 32 (0.594)" — re-adjudicated under the same protocol minus the cognition perspective — against "48 of the 81 (0.593)", which is the deployed stage's confirmed-set count with cognition. What is the 32-candidate number under the deployed configuration, and what exactly does the comparison establish about the filter? — intended effect: item 1.3's rating would move up if the comparator is stated and the inference it supports is bounded explicitly.
- **Q4:** Can the second backbone's perspective arm, which loses 11 true bugs at the recall level while forced counts are equal, be decomposed into the five bundled changes — or at least its routing rate reported alongside? — intended effect: item 2.9's rating would move up, since the loss would be attributable to extra abstention or to extra wrong decisions rather than to "perspectives" as a bundle.
- **Q5:** Does the pair-audit file in the artifact contain the 134 pairs with their citations, or only the verdicts — and if only the verdicts, can the audited generation ship, given that the Data Availability text says the earlier rebuilt generations are archived separately and do not ship? — intended effect: item 4.3's rating would move up if the audited material is reachable, since it is the only claim whose raw material is currently outside the package.


---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Accept

### Summary

The paper reports an experience study of an LLM-based pipeline that mines documentation--implementation
inconsistencies in three production vector database systems (Milvus, Qdrant, Weaviate). The pipeline
extracts constraint records from vendor prose, turns them into executable probes, runs them in a Docker
sandbox, and has an LLM "confirmation stage" decide whether each observed behaviour is a defect. The
paper reports three things: a submission ledger in which maintainers confirmed 51 of 81 adjudicated
submissions and merged fixes for 23; an audit, on the packages as the pipeline produced them, of every
(constraint, cited-page) pair the confirmation stage reads (18 of 134 supported as cited, 58 re-anchored,
58 unsupported), which also exposed two information-leak channels that were repaired and the affected
cases re-judged; and a clause-level census of the confirmation stage's 243 judgments on its primary model
backbone, finding that the unguarded contract-refutation clause closes 50 judgments of which 24 are true
bugs, and supplies 24 of the 30 incorrect closures to False-Positive.

The judgments come from twelve judge configurations on two model backbones, three runs over all 81 cases,
evaluated with paired exact McNemar tests at both the confirmed-set and recall levels. For every contrast
the paper prints a deployment convention (a routed case counts as confirmed) and a forced-verdict reading
side by side, prices a hand-adjudicated joint reading against them, and runs the released VDBFuzz
configuration on the instance where its silent-accept defects are live as a crash-oracle baseline (0
oracle anomalies over 205 templates). The census's counterfactual---routing contract refutation instead of
closing on it---recovers seven true bugs and releases nine more false positives under the convention, and
changes nothing under the forced reading; the paper reports that the census pattern does not reproduce on
the second backbone.

### Core Strengths

- **S1:** An exhaustive, blind-second-reader-checked audit of what the judge *reads* rather than what it
  concludes, with a cross-tab that separates the audit's unsupported rows from the closures they might
  otherwise explain.  --- see 2.1, 4.1
- **S2:** The counting convention is priced at two places and both readings are printed for every
  contrast; the paper shows that the routing rule's headline gain is deferral, not the judge deciding
  better.  --- see 2.2
- **S3:** A replicated null, on both backbones under forced verdicts, for the four-perspective
  organization, with the five bundled changes of that contrast disclosed rather than folded into the
  claim.  --- see 2.2, 3.2
- **S4:** The instrument is audited and reported in public: voided runs owned rather than reused, two leak
  repairs with re-judging, four defects in the authors' own dispatches reported rather than quietly fixed,
  and an explicit statement of what is and is not recomputable from the artifact.  --- see 3.3, 4.1, 4.2

### Core Weaknesses

- **W1:** The census---the paper's lead finding---is a single-deployment observation that the second
  backbone reverses (there, by-design refutation closes 50 and is wrong 22, and the unguarded clause
  supplies 50% rather than 80% of incorrect closures), and the rival mechanism the paper itself names
  (firing-order selection, since contract refutation is tried first on the largest residual) is left
  unresolved.  --- see 2.3
- **W2:** The paper's most honest reading (the hand-adjudicated joint reading, 33/51) is bounded, not
  measured---an independent pass agrees with it at $\kappa\approx0$, and two of three protocol statements
  land at the forced floor---and the pool's 30 negatives have no inter-annotator study while the campaign
  has no per-run detection rate and no candidate funnel.  --- see 2.4, 2.5
- **W3:** Twelve configurations and three readings are reported only in running prose, with no results
  table, and some arm-level numbers do not say which reading they carry, so a reader cannot verify the
  arm relations from the paper.  --- see 5.2, 2.6
- **W4:** The abstract and the evaluation sections are dense to the point of obscuring the claims:
  "the two letters the dispatch defines twice" is used before the letters are introduced, several terms
  are used before definition, and the census numbers are repeated verbatim five times.  --- see 5.3, 5.4,
  5.7

### Detailed Assessment

1. **Importance & Scope** — Excellent
   - **1.1** The Introduction and Section 2 establish the problem with a checkable instance---Milvus issue
     \#49823, where \texttt{nprobe} is documented as an integer in $[1,16384]$ and the REST search API
     accepts \texttt{nprobe=0} with HTTP 200, and Qdrant \#10369 on a cross-collection vector-size
     coupling---and separate the target class (behaviour that contradicts API prose) from vector-search
     correctness, which is exactly the distinction a reader needs before the later claims make sense.
     Table~\ref{tab:oracles} then positions six oracle families by where each anchors its expectation and
     says what each misses; for an experience paper this is the right kind of scoping, because it tells
     the reader which residual is being worked rather than claiming the whole field.
   - **1.2** Scope is stated more precisely than in most papers I review: the pool (81 candidates, 51
     maintainer-confirmed and 30 negatives, of which 11 carry a maintainer disposition and 19 are the
     authors' own calls, Section 4.1); the ledger (132 rows: 81 adjudicated, 49 without a maintainer
     verdict, 2 withdrawn); the census ("the deployed stage on the primary backbone", Section 4.5); and
     what the paper refuses to claim ("not a per-run detection rate, and we cannot supply one",
     Section 4.2). The scope statement is repeated at each place a claim could be over-read, which is
     what makes the paper's honesty legible instead of defensive.
   - **1.3 [minor, unfixable]** The measured reach is narrow in a way that bounds what the *results* can
     be said to establish, even though it does not bound the importance of the *problem*: one pipeline,
     one domain, three vendors, two serving aliases, one census site, and a voided detection experiment.
     The paper says all of this itself; the item is recorded so that this tier is read as a judgement
     about the problem and the clarity of its boundary, not about how far the measurements travel.

2. **Insights & Evidence** — Adequate
   - **2.1** The pair-level audit (Section 4.3) is the paper's most solid measurement and the one I would
     keep if only one could survive: all 134 (constraint, cited-page) pairs were checked against the page
     each cites at the version the row claims, giving 18 supported, 58 mis-anchored (a source file or a
     landing page) and 58 unsupported---43.3% each of the last two, each share of 134. It is corroborated
     by a blind second reader on a stratified sample of 36 of the 122 reachable pairs ($\kappa=0.75$),
     with the 12 unreachable pairs excluded and disclosed, and it is reinforced by a negative control
     after the rebuild: zero of 81 packages contain an expectation-framed sentence, and the 19 phrasing
     hits were inspected and are all verbatim server responses.
   - **2.2** The twelve-configuration study (Table~\ref{tab:configs}) is a fitting design for the question
     "what changes what the judge confirms": frozen per-case materials, three runs per case, paired exact
     McNemar at both the confirmed-set and recall levels, Wald intervals, and a bootstrap CI for net and
     $F_1$. I recomputed the census table's margins (61+21+7+50+19+16+69 = 243, with the confirmed/negative
     judgment split at 153/90), the A/B/C/D legend totals (243 each) and the printed McNemar p-values
     (0.0039, 0.0001, 0.0013, 0.0225, 0.0042, 0.0034, 0.0004, 0.6072, 0.7539, 0.4531, 0.0625, 0.2891,
     0.6250, 1.0) by hand; they all agree with the text, including the Holm step-down under both the
     ten-test and twenty-test families. The forced-verdict equality (27 vs.\ 27 and 26 vs.\ 26, with the
     true-bug sets intersecting in only 22 of 27 and 23 of 26) replicates across backbones and is the
     paper's most robust finding.
   - **2.3 [major, unfixable]** The census (Section 4.5) is the paper's lead result and it rests on one
     deployment. On the second backbone the pattern inverts (contract refutation closes 56, by-design
     closes 50 and is wrong 22; the unguarded clause supplies 24 of 48 incorrect closures, 50% rather than
     80%), and on that backbone the D field's meaning is unsettled, so the paper cannot say whether the
     letters mean the same thing there. The paper reports all of this in the abstract and repeats it in
     the threats---which is exemplary---but the net effect is that "the guard protects the clause that is
     already clean" is a one-site observation whose mechanism is not isolated: the paper itself names the
     selection rival (contract refutation is tried first and on the largest, most heterogeneous set) and
     concedes it does not resolve it. A revision cannot fix this; only a third deployment or a designed
     isolation could.
   - **2.4 [major, unfixable]** The reading that the paper calls honest---the hand-adjudicated joint
     reading, 33/51 and +4 on the headline contrast---is not independent evidence. An independent
     adjudicator on the same materials agrees with the author-executed pass on 4, 5 and 6 of the 20
     commonly ruled cases ($\kappa=-0.01$, 0.08, 0.11), and two of the three independent statements land
     at the forced floor. The paper's response (report the joint reading as a bound, not a measurement) is
     the right one, and it means the strongest statement the paper can make about its own change is
     "suggested, not established". The same weakness reaches the pool: the 30 negatives are adjudicated
     without an inter-annotator study, 19 of them by the authors alone. The census's load-bearing 24 is on
     maintainer labels, which is a real defensive choice, but the closure-accuracy side of Table 4 rests
     partly on self-adjudicated labels.
   - **2.5 [major, unfixable]** The campaign (Sections 1 and 4.2, and the Yield entry of the Threats to
     Validity section) is a ledger, not a measurement of detection: the detection-ability runs were voided
     in full, the pool is submission-filtered, and the screening step is unvalidated---the 32 screened-out
     candidates were re-adjudicated only by the same stage (19/32 confirmed), with no maintainer ground
     truth, so the filter's correctness is unknown. The paper states each of these limits plainly and
     forbids the over-reading itself ("It is not a per-run detection rate, and we cannot supply one").
     That honesty is why this is Adequate evidence for a record and not a soundness failure; it is still
     the reason the reader cannot interpret 51 of 81 as a property of the method.
   - **2.6 [minor, fixable]** Two supports sit outside the shipped artifact and are disclosed as such: the
     fix-PR characterisation (all 23 merged fixes modify implementation code, 15 also add a regression
     test, none is documentation-only, Section 4.2) and the rebuild's row-level accounting, which the
     threats section says "does not fully reconcile in our own report". Both are cheap to repair by
     shipping the table and stating the reconciliation gap's size.
   - **2.7 [minor, fixable]** Three contrasts change more than one variable and the four-perspective
     contrast changes five (Section 4.4), all disclosed. The summary sentences that inherit the bundle
     ("what determines which candidate defects an LLM confirmation judge confirms", the Conclusion's
     "how it is organized") would be safer if they named the bundle each time; as written they invite a
     reading broader than the design supports.

3. **Perspective** — Excellent (provisional: I assessed the lessons from the paper's own reasoning and my
   general knowledge; I did not survey the LLM-testing or oracle literature, so judgements about how novel
   each lesson is for the field are not mine to make)
   - **3.1** "Audit what your oracle reads, not only what it concludes" (the bold-titled lesson in
     Section 5, Discussion) is the most transferable lesson here, and the paper gives it a procedure
     rather than a slogan: sample pairs against their cited pages to estimate how much of the judge's
     input is unsupported, then cross that against where the judge's errors land---which is precisely
     what Section 4.5 does, and what rules out the "the bad rows caused the closures" explanation. Anyone
     running a distil-then-judge pipeline can copy this in a day.
   - **3.2** "Price the deferral channel, and price the contrast, not just the level" (the bold-titled
     lesson in Section 5, Discussion, together with Section 4.4) is a genuinely reusable measurement idea
     for any system with an abstention or escalation channel: the paper shows the bundled effect falling
     from nine bugs to three (to four, deployed) when the routed queue is hand-adjudicated, and identifies
     the convention---not the judge---as what pays for abstention. This is the insight I expect other
     groups to reuse first.
   - **3.3** "Check the dispatch before you re-architect the judge" (the bold-titled lesson in Section 5,
     Discussion) is backed by the paper's own embarrassment, reported rather than hidden: eight of twelve
     dispatches declare a binary verdict field while mandating three values, the deployed dispatch prints
     two aggregation rules with opposite defaults and defines the perspectives twice with C and D
     exchanged, and a one-line schema repair moved five of the headline nine bugs. The companion
     practice---replaying the printed aggregation rule over the judge's own recorded values to count
     departures (22 forward, 17 in the forbidden direction, 10 on real bugs)---is offered as "a five-line
     script" in the same section. Lessons that come with their cost stated are the ones that transfer.
   - **3.4 [minor, fixable]** The most portable form of the census lesson is deployment-independent
     ("measure, per deployment, which clause carries the error mass; do not assume the guard is where the
     errors are"), since the site-specific form is reversed on the second backbone. The "Put the evidence
     guard where the error mass is" lesson in Section 5 carries the bound at its end, but the abstract's
     "locates the error budget in the one refuting clause its protocol does not guard" reads as the
     finding rather than as its scoping. Stating the portable form beside the site-specific one would make
     the lesson harder to misuse.

4. **Verifiability** — Excellent
   - **4.1** The Data Availability statement is unusually specific about objects and generations: the
     pool; the frozen per-run verdicts of all twelve configurations; the packages the study read; the
     dispatch texts and the judging prompts they instantiate (with English renderings of the two judging
     prompts under \texttt{rq2/prompts/}); the pair-audit verdicts, the adjudication worksheet and the
     blind passes; and, for every re-judged run, the re-judged cases *and* the pre-repair state beside the
     untouched batches, so either pool can be reconstructed from the package alone. That last clause is
     the difference between a declared artifact and a checkable one.
   - **4.2** The paper states its own script coverage rather than letting a reader discover it: five named
     analysis scripts recompute all rates, both censuses, both replays, the net and $F_1$ intervals and
     the pair audit; the catch-all composition, the expectation-framing check and the C row's evidence
     classification are "printed but not yet scripted", and the artifact's coverage note says so. Naming
     the unscripted analyses is the behaviour I would want standardized.
   - **4.3 [minor, fixable]** The pair audit's *input*---"the packages as the pipeline produced them"
     (Section 4.3)---is not clearly covered by the shipped objects: the Data Availability sentence says
     the packages that ship are "the post-rebuild, cognition-stripped generation the dispatches name; the
     earlier rebuilt generations are archived separately and do not ship", which leaves it ambiguous
     whether the pre-rebuild generation that the audit scored is in the package. Since that generation is
     the object of the paper's strongest measurement, and 12 of its cited pages are already unreachable,
     shipping it (or a snapshot) would let the 134-pair split be re-derived rather than trusted.
   - **4.4 [minor, unfixable]** The judgments themselves cannot be replayed: both backbones are serving
     aliases without pinned weights, and the dispatched inputs ship while model behaviour does not, so a
     reader can re-run the analyses but not the judging. This inheres in the study and is disclosed. For
     the record, the artifact link in Data Availability is declared at
     \url{https://anonymous.4open.science/r/TestVDB_artifact-EC36/}; I could not confirm reachability from
     my review environment, so I have not treated reachability as evidence either way.

5. **Presentation** — Adequate
   - **5.1** The structure is complete and appropriate to an experience paper (Introduction,
     Preliminaries, Approach, Evaluation, Discussion, Threats to Validity, Related Work, Conclusion, Data
     Availability), the contribution list in Section 1 carries each contribution's scope in the same
     sentence, and the two tables that carry the paper's apparatus---Table~\ref{tab:oracles} on oracle
     families and Table~\ref{tab:pairaudit} on the three-way split---are clear and well captioned,
     including the caption that pre-empts the double-counting misreading of the two 43.3\% shares.
   - **5.2 [minor, fixable]** There is no results table. The twelve configurations' levels, their
     convention/forced/joint readings, recall, suppression, precision and the confirmed-set counts are
     reported only in running prose across Sections 4.1--4.5, and at least one arm's entry does not carry
     its reading: "the no-aggregation arm confirms 33 with 3 leaked false positives (suppression 0.900,
     precision 0.917)" (Section 4.4) follows a sentence that gives the deployed stage's three readings,
     and the paragraph's spans ("forced recall spans $[23,31]$ of 51 against a convention span of
     $[27,48]$") can only be checked if each arm's reading is known. One table, one row per
     configuration, would remove a whole class of reader doubt.
   - **5.3 [minor, fixable]** The abstract is overloaded: it carries three results, two leak repairs, the
     convention caveat, a backbone caveat and a definition-by-implication ("the two letters the dispatch
     defines twice are settled by their content") before the reader knows what the letters, the dispatch
     or the backbone are. Section 1 inherits some of this. The claims are all correct; they are simply
     packed at a density that costs a first-time reader a re-read of the abstract alone.
   - **5.4 [minor, fixable]** Terminology is used before definition in several places: "the deployment's
     convention" appears in the abstract and Section 1 and "the forced reading" in the abstract, but the
     two are only defined in Section 4.1, where "the joint reading" first appears as well; "suppression"
     is defined once, in Section 4.1, and then used as a bare quantity; "precision" appears once (0.917)
     with no definition of its denominator; and the perspective labels are called "letters" throughout
     without ever saying they are A/B/C/D column labels of the dispatch's perspective table.
   - **5.5 [minor, fixable]** The title's first verb, "Detecting", promises a detection result the paper
     explicitly denies ("It is not a per-run detection rate, and we cannot supply one", Section 4.2). The
     subtitle's three nouns are accurate; the title would be safe without the verb.
   - **5.6 [minor, fixable]** The pipeline is named (\system{} = TestVDB) only in the Figure~\ref{fig:pipeline}
     caption; the prose says "the pipeline" and "the stage" throughout, so the system the paper is about
     is never introduced in text. (I reviewed the figure's caption only; the figure file itself is not in
     the review copy.)
   - **5.7 [minor, fixable]** The census's signature numbers (50 closures, 24 wrong, 19, 17, 80\%) recur
     verbatim in the abstract, Section 1, Section 4.5 and the Conclusion (the Discussion restates the same
     phenomenon, but the numerals it prints there---"closes 50 and is wrong 22"---are the second
     backbone's). The repetition inflates length and makes the small contextual differences between
     restatements---which reading, which backbone---easy to miss.

### Questions for Authors

- **Q1:** Which side of the pool is \texttt{milvus\_001}---one of the 51 maintainer-confirmed bugs, or one
  of the 30 negatives---given that its observation was never captured and its version's documentation
  segment is retired, and that the convention credits eleven configurations with a point for it
  (Section 4.1)? — [intended effect: if it is a credited positive, item 2.5's recall denominators become
  readable and I would say so explicitly; if it is a negative, the "credited a point" phrasing needs
  correcting, which would move 2.5 down.]
- **Q2:** What is the candidate funnel for the runs represented in the ledger---how many candidates were
  generated and screened before the 81 were submitted (Section 4.2 gives only the 32 screened candidates
  from "the reported run")? — [intended effect: a small funnel would let the reader interpret 51 of 81 as a
  pipeline property and move 2.5 up; a large one would confirm that the submission filter is the dominant
  unmeasured step and move 2.5 down.]
- **Q3:** Does the pre-rebuild package generation---the object the 134-pair audit scored---ship in the
  replication package, or only its post-rebuild successor and the pair-audit verdicts? — [intended effect:
  shipping it would move 4.3 up, because the paper's strongest measurement would become re-derivable
  rather than trusted.]
- **Q4:** Would re-dispatching the second backbone with a dispatch that defines the perspectives once
  settle whether the census's non-replication (Section 4.5) is a real difference in error distribution or
  a consequence of the doubled definition and the two D vocabularies? — [intended effect: if the
  non-replication is attributable to the dispatch defect, item 2.3's rating would move toward Adequate on a
  future version; as it stands the item stands because the evidence cannot distinguish the two.]
- **Q5:** Which reading do the arm-level numbers in Section 4.4 carry---for example, is the
  no-aggregation arm's "33 with 3 leaked false positives" a convention or a forced figure---and could the
  twelve configurations be tabulated with their readings labelled? — [intended effect: labelling would move
  5.2 up and let a reader check the arm spans without opening the artifact.]


---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Importance & Scope | Excellent | Adequate | Excellent | **Excellent** |
| Insights & Evidence | Excellent | Adequate | Adequate | **Adequate** |
| Perspective | Adequate | Excellent | Excellent | **Excellent** |
| Verifiability | Excellent | Excellent | Excellent | **Excellent** |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Accept** | **Accept** | **Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three reviewers leaned in, so the unanimous shortcut decides the verdict outright: all three
Weak Accept or better → ACCEPT. The consensus-tier count does not disturb it — no criterion sits at
consensus Poor, and no criterion sits at consensus Weak, so the "two or more substance Weak" and
"three or more total Weak" gates are never reached and the "no substance Weak, at most one fixable
Weak" line applies. Verifiability is consensus Excellent for the second consecutive round, and this
time for a stronger reason than artifact synchronization: two reviewers independently re-derived the
printed statistics from the paper's own counts — R1 recomputed eight exact McNemar p-values, the net
identity and both F1 values; R3 recomputed the census margins, the legend totals and both Holm
step-down sequences; R2 did both families — and all three report that every number checks out. R2
states the point plainly: statistical claims of this density usually contain an error, and this set
does not. The three reviewers also agree on the shape of the paper's remaining weakness: Insights &
Evidence is the sole consensus Adequate, and it is Adequate on a single shared ground — the census's
reach — restated by each reviewer in their own terms (the second backbone reverses it; the audited
generation is not the generation the judges read; the campaign is a record rather than a detection
measurement). No reviewer treats that as a defect in the claim as written, because the paper scopes
it in the abstract, in contribution 3, in the evaluation, in the Discussion and in the threats; it is
a ceiling on how far the finding travels. The one genuine divergence is over how to price that
ceiling, and it is recorded under Priority Revisions rather than folded into the verdict, because
R3's `[major, unfixable]` items and R1/R2's `[minor, *]` items describe the same disclosed limits
from different sides of the same convention, not two different defects.

### Priority Revisions
1. **Price the guard the paper actually prescribes.** R1 (2.9, W3) and R2 (2.6, W1) independently
   found the same gap and independently proposed the same measurement: the replay routes *every* one
   of the 50 contract refutations to human review, while the Discussion prescribes a *verbatim-evidence
   guard*, so "+7 true bugs / −9 false positives" bounds a cruder intervention than the one
   recommended, from one side only. Both point out that the rationales for those 50 closures are in
   the frozen record and that §4.5 already performs exactly this classification for the 19 by-design
   closures (15 comment/docstring, 2 name-validation-rule, 2 code-structure). Classify the 50 on the
   same axis — or restate the recommendation as the routed clause, which is what was measured. This
   is the round's most actionable item and its cheapest: no new dispatch, no new arm, no new model.
2. **Decide what the census is — a property of the protocol, or a case study of one backbone.** All
   three reviewers raise the census's reach; they diverge on its severity, and that divergence is
   itself the finding. R3 rates it `[major, unfixable]` (2.3), arguing the fix is more backbones and
   that until then the claim should be labelled a case study at the title-level framing, not only in
   scope clauses. R1 rates it `[minor, fixable]` (2.7, W1) and R2 `[minor, unfixable]` (2.8, W3),
   both holding that the disclosure is complete and the claim is scoped as written, so what remains is
   a ceiling rather than a defect. The council of the three: R3's 2.3 is one reviewer's severity call,
   not a consensus, and does not by itself move the verdict — but it marks the boundary the paper
   should step back from, and R1's and R2's proposed relabelling (name the conditions under which the
   pattern would be a protocol property: a model family, a documentation style, a routing rate) is
   cheap and satisfies R3's objection without a new deployment.
3. **Ship the generation the pair audit scored.** R2 (2.7, 4.3, W2) and R3 (4.3, Q3) both found that
   the audit's headline 43.3%/43.3% split was measured on the generation the repair replaced, that the
   Data Availability statement says those earlier generations "are archived separately and do not
   ship", and that the rebuilt generation is never re-measured at pair level. The audit-and-rebuild
   discipline is therefore demonstrated on the way in but not on the way out. Shipping the audited
   generation, or a pair-level file carrying each constraint, its citation and its verdict, would let
   the split be re-derived rather than trusted — R2 notes this is the one claim in the paper whose raw
   material is not in the package.
4. **Close the related-work hole the shipped bibliography already contains.** R1 (3.4, W4) and R2
   (3.5, W4) independently name the same entry: Testora (ICSE 2026, "Using Natural Language Intent to
   Detect Behavioral Regressions") sits in the project `.bib` and no `\cite` reaches it, so under
   ACM's reference format it never renders and the delta is never drawn — and it is the closest
   published premise to this paper's own. R2 adds the mechanical count: 22 shipped entries are
   unreachable by any `\cite`, among them two that name this paper's axis. One sentence positioning
   Testora, as the paper already does for Metamon and CASCADE, closes the substantive half.
5. **Give the FP-side labels the second reader the pair audit got.** R1 (2.8, W2) and R3 (2.4, W2)
   both observe that 19 of the 30 negatives are the authors' own calls with no inter-annotator study,
   and that the suppression rates, the "nine false positives released" half of the counterfactual, and
   the net/F1 tie all rest on them, while the paper correctly isolates its error counts to maintainer
   labels. Both note the paper already trusts a second-reader design elsewhere (30 of 36, κ = 0.75 on
   the pair audit); running the same design on the 30 negatives would settle whether the FP-side
   conclusions move.
6. **Label the screening comparator.** R1 (2.11) and R2 (1.3, Q3) both flag that §4.1 reads "the stage
   confirms 19 of 32 (0.594) against 48 of the 81 (0.593) on the pool", where the 32 were re-adjudicated
   under the full-stage protocol *minus* the cognition perspective while 48 is the deployed stage's
   cognition-bearing confirmed-set count. If the two rates do not come from the same instrument, the
   "does not separate the streams" reading is confounded. One clause naming the configuration settles it.
7. **Presentation battery**, ranked within the tier: R3 (5.2, W3) and R2 (5.2) ask for a results table
   for the twelve configurations — their levels, readings, recall, suppression, precision and
   confirmed-set counts are reported only in running prose, and at least one arm's figure does not say
   which reading it carries, so the arm spans cannot be checked from the paper; R3 (5.3, 5.4, 5.7) and
   R2 (5.3) ask that the abstract's density come down and that "the convention", "the forced reading",
   "suppression", "precision" and the "letters" be defined before use, and that SWAP/DROP/SUPPORTED be
   mapped to Table 3's three categories; R1 (5.3) found Table 1 and Section 7 disagreeing on the
   membership of one oracle-family row (Toradocu and ICON each appear in one list and not the other);
   R1 (5.4) found "operator" used once without definition in §4.3; R3 (5.5, 5.6) notes the title's
   "Detecting" promises a detection result the paper explicitly denies, and that the pipeline is named
   only in a figure caption and never in prose.
