## Reviewer 1: Domain Expert

**Overall Recommendation:** Accept

### Summary

This experience paper reports three linked studies produced by one defect-mining pipeline for
documentation–implementation bugs in vector DBMSs (Milvus, Qdrant, Weaviate). The first is a
submission ledger: 132 rows across 19 versions, of which 81 candidates were adjudicated — 51
maintainer-confirmed bugs (23 with merged fixes) and 30 negatives labelled by the authors. The
runs that would have measured per-version detection ability were voided by the authors for
dispatch-discipline violations, so the campaign is reported as a record of submissions and
adjudication, not as a detection rate. The second study audits the evidence packages the
confirmation stage reads: of 134 (constraint, cited-page) pairs, 18 are supported as cited, 58
were mis-anchored (source file or landing page) and re-anchored, and 58 have no support on their
cited page; the same audit exposed two channels through which forbidden material reached the
stage, which were repaired and the affected cases re-judged. The third study classifies the
deployed stage's 243 judgments (81 cases × three runs, primary backbone) by the aggregation clause
that closes each one: contract refutation, which has no evidence requirement, closes 50 judgments
and 24 of the 30 incorrect closures to False-Positive; the verbatim-guarded by-design clause
closes 19 and is right 17 times. A replay that routes contract refutation to human review instead
of closing on it moves recall 39/51 → 46/51 and suppression 21/30 → 12/30 under the deployment's
convention and changes nothing under forced verdicts. The paper additionally runs the released
configuration of the one dedicated VDBMS fuzzer against Qdrant (205 templates; zero oracle
anomalies), prices every contrast under a convention, a forced and a hand-adjudicated reading, and
reports four defects found in its own dispatches.

### Core Strengths

- **S1:** The audit of the confirmation stage's *input* is a first-of-kind, pair-level measurement
  with an independent second reader and a check for the failure mode the method invites — see 2.1,
  1.2
- **S2:** The census is designed to falsify its own most obvious alternative explanation, and it
  does: the clause finding is separated from the pair-audit finding by a package-strata cross-tab,
  and its load-bearing count rests on maintainer labels only — see 2.2
- **S3:** The organization-versus-deferral result is clean and usefully negative: forced-verdict
  recall is equal across the perspective contrast on both backbones even though the two
  configurations do not decide the same cases (their forced true-bug sets intersect in 22 of 27
  and 23 of 26), and the two levels of testing are both reported — see 2.3
- **S4:** Withholding the implementation source raises recall and worsens the false-positive side,
  with net and F₁ intervals that span zero — a counterintuitive result that reframes source
  grounding as a suppression mechanism — see 2.4
- **S5:** Verifiability is unusually strong for this kind of paper: a declared replication package
  with frozen per-run verdicts, dispatch texts, judging prompts, audit verdicts and five named
  analysis scripts, plus an explicit statement of what is *not* scripted — see 4.1, 4.2

### Core Weaknesses

- **W1:** The clause census — the paper's headline insight — is measured on one deployment on one
  (unpinned) backbone and reverses on the second, where by-design refutation is the inaccurate
  clause and the unguarded clause supplies 50% rather than 80%; the non-replication sits in a
  subordinate clause of contribution 3, while the bullet's opening line and the Discussion heading
  still name the misplaced guard as the finding — see 2.5
- **W2:** The prescription is priced by a replay over frozen recorded values, not by an
  intervention, and its gain is zero under the forced reading; both facts are stated (Section 4.5;
  the null also in the abstract), but the contribution bullet that carries the number says only
  that the counterfactual is "priced at both readings" — which tells a reader the reporting, not
  that one reading nulls the effect — see 2.6
- **W3:** The deployed protocol that every number is computed against is malformed by the paper's
  own account (two printed aggregation rules with opposite defaults, four perspectives defined
  twice with C and D exchanged, a schema that mixes vocabularies), and the identification of the
  load-bearing column A against B is argued from distributional shape rather than content — see
  2.7, 2.8, Q1
- **W4:** Related work: DocPrism sits in the paper's own bibliography but is never cited, although
  it belongs squarely to the family the paper positions itself against, and the routing/escalation
  mechanism the paper measures is supported by a single citation from the abstention literature —
  see 3.2

### Detailed Assessment

1. **Importance & Scope** — Excellent
   - **1.1** Section 2 separates *consistency* (does observable behaviour match what the API
     documentation prescribes) from *correctness* (is the returned result mathematically right),
     and Section 3.2 makes the endpoint-level/system-level split observational: a constraint
     violated by one request/response pair is endpoint-level even when elaborate setup is needed,
     and one violated only by relating observations across requests or against evolved state is
     system-level. This is the kind of definitional work that makes the later numbers falsifiable,
     and it correctly excludes approximate-nearest-neighbour correctness from scope.
   - **1.2** The paper establishes the problem's importance from the field's own artifacts rather
     than from assertion: the VDBMS bug study's non-crashing majority, VDBFuzz's oracle reaching
     only crashes/5xx, and the community roadmap naming oracle definition as the open problem
     (Section 2). It then argues structurally — via the oracle-family table (Table 1) — that no
     deterministic-oracle family anchors its expectation in untagged, system-level behavioural
     prose, which is precisely where the residual lives. I checked the table's factual claims
     against fetched copies of AGORA+ (trace-anchored), SATORI (OpenAPI-field-anchored) and
     VDBFuzz (crash-only by its own statement), and the shared cache for MASTOR (source-anchored):
     all accurate.
   - **1.3** Scope is stated with its limits rather than around them: the 81 candidates are a
     submission-filtered subset of one pipeline's output (Section 6); the detection-ability
     experiment was voided and no per-run rate is supplied (Sections 4.1, 4.2); recall levels are
     contrasts on a common pool, not operating performance; one case (milvus\_001) is unjudgeable
     yet credited under the deployment's convention to eleven of twelve configurations (Sections
     4.1, 6). A reader cannot mistake the yield number for a benchmark score.

2. **Insights & Evidence** — Adequate
   - **2.1** The pair audit (Section 4.3) is the paper's most novel measurement: all 134
     (constraint, cited-page) pairs on the packages *as produced*, adjudicated against the page
     each cites at the claimed version, split 18 supported / 58 mis-anchored / 58 unsupported, with
     two named mechanisms (version drift from a single-version contract; constraints that exist as
     prose but not as documented values). Two design choices make it credible: the rebuild is
     followed by a check for the failure mode the method invites ("zero of 81 packages contain a
     sentence framed as an expectation" — the 19 hits for such phrasing are verbatim server
     responses), and a blind second reader re-coded a stratified sample of 36 of the 122 reachable
     pairs, agreeing on 31 (κ = 0.78) with all 15 SWAP pairs called SWAP again. The authors
     correctly decline to generalise the rates beyond this distiller on these three vendors.
   - **2.2** The census (Section 4.5) does something reviewers rarely get: it separates its own
     most plausible alternative explanation. Since 58 of 134 cited pairs are unsupported, the
     "unguarded clause is wrong half the time" result could have been the audit finding resurfacing
     — defective rows failing a mechanical containment check. The cross-tab over the packages' four
     strata shows 20 of the 24 bad closures fall on the 59 cases whose *rebuilt* packages carry
     documented evidence (rate 0.11 among their 177 judgments) and none on the 18 the audit left
     without documented evidence; the paper also states that the load-bearing 24 rests on
     maintainer-confirmed labels only, so it does not depend on the self-adjudicated negatives, and
     that it is invariant across the two aggregation rules the dispatch prints.
   - **2.3** The level design produces a genuinely useful negative result (Section 4.4): the
     perspective contrast yields identical forced-verdict recall on both backbones (27 vs 27,
     26 vs 26) while the forced true-bug sets intersect in 22 of 27 and 23 of 26, and the
     paper refuses to privilege either the confirmed-set or the recall level where they disagree.
     The statistics are handled better than is typical: paired exact McNemar at both levels, an
     explicit ten-test recall family, and a Holm correction that is stated together with its
     consequence (the deployed stage's own recall-level advantage over the flat judge is not
     significant after correction and should be read descriptively). I re-derived the Holm step
     from the printed p-values; it is correct.
   - **2.4** The evidence-access contrast is the paper's most counterintuitive measured result:
     withholding the implementation source raises recall 39 → 48 and cuts suppression 21/30 →
     12/30, while net true positives minus leaked false positives is 30 either way (paired
     bootstrap 95% CI [−8, +8]) and F₁ differs by +0.033 with an interval spanning zero. The paper
     states this as a tie rather than a victory and names the arm's two other changes (Section 4.4)
     — the honest framing of a result that cuts against the pipeline's own design premise.
   - **2.5 [major, fixable]** The census's scope sentence is present but subordinated. It is
     measured on one deployed configuration on the primary backbone, and on the second backbone
     the pattern reverses: there, contract refutation closes 56 judgments and by-design refutation
     closes 50 of which 22 are wrong, so the unguarded clause supplies 24 of 48 incorrect closures
     to False-Positive — 50%, not 80% (Section 4.5). Contribution 3 does carry the scope ("measured
     on the primary backbone and does not reproduce on the second"), but the same bullet opens by
     naming the contribution as "locating the evidence guard on the wrong clause", and the
     Discussion heading with the same finding ("Put the evidence guard where the error mass is")
     carries no such qualifier — so the non-replication, which is the strongest evidence the
     pattern is deployment-specific, does the work of a caveat the headlines do not. Fix: fold the
     scope into those headlines (e.g. "on this deployment"), or promote the reversal itself to a
     stated finding about deployment-dependence.
   - **2.6 [major, fixable]** The counterfactual that prices the fix is a replay rather than an
     intervention, and the paper says so plainly: "what cannot be computed from frozen data is
     whether a judge re-adjudicating those refutations under a verbatim-evidence guard would reach
     the same place" (Section 4.5). Its seven-true-bug gain exists only under the deployment's
     convention — under the forced reading the replay changes nothing — so it is a property of the
     counting convention rather than of the judge's decisions. Both facts are disclosed, and the
     disclosure is exemplary; what survives is placement: the contribution bullet that carries the
     number says only that the counterfactual is "priced at both readings", and the whole change's
     "suggested, not established" reading sits in the hand-priced paragraph of Section 4.4 rather
     than where the finding is named. Fix: run the guarded re-adjudication on the frozen fifty, or
     state the replay status and the forced-reading null beside the number in the contribution and
     the Discussion.
   - **2.7 [major, fixable]** The object quantified is not a single well-defined protocol. The
     deployed dispatch prints two aggregation rules whose last steps disagree about the
     insufficient-evidence default, defines the four perspectives twice with C and D exchanged, and
     its output schema follows different definitions for C and D (Sections 1, 4.1, 4.5). The paper
     bounds this carefully (the appended rule is treated as operative, the 22 forward departures
     are replayed, the reversal is shown to lie in the content-identified C), but the census's
     central quantities depend on which printed rule a reader takes as the protocol, and the paper
     acknowledges the consequence: the second backbone's D field carries two incompatible
     vocabularies, so D's meaning is unsettled there. Fix: show how a reader recovers the
     operative-rule choice from the shipped package — which recorded field the tally keys on, and
     where the appended rule is pinned among the two printed — so the census's semantics do not
     rest on the reader's assumption.
   - **2.8 [major, fixable]** The identification of the load-bearing clause is weaker than the
     paper's phrasing suggests. The content tests cover two of the four perspectives — no cell
     outside C records a *weak* refutation, no cell outside D carries the source vocabulary — which
     is what the letters C and D rest on. A and B share all three values (Neutral, Confirmed,
     Refuted), and the paper argues them apart by *shape* ("A is Neutral 172, Refuted 50, Confirmed
     21; B is Neutral 146, Confirmed 80, Refuted 17"). Since the aggregation closes to
     False-Positive on A = Refuted, the entire 50-closure/24-wrong result — and therefore the 80%
     — attaches to whichever column is A. The abstract's "the perspectives are identified by their
     content" does not hold for that column. Fix: state the identification mechanism for A and B
     explicitly (field name or declared column order in the schema), and, if available, add a
     content test that separates them.
   - **2.9 [minor, fixable]** The false-positive side of every level rests on labels with thinner
     provenance than the recall side: the 30 negatives are "adjudicated by us against the
     maintainers' disposition where available" (Section 4.1), with no inter-annotator study and no
     count of how many carried a maintainer disposition. Suppression (21/30), precision (0.917),
     the intercept counts and the catch-all composition all move with those labels; the census's
     own 24 is unaffected (the paper says so), and one of the 81 is unjudgeable yet credited to
     eleven of twelve configurations under the convention. Fix: report the disposition split and a
     sensitivity bound for the FP-side quantities.
   - **2.10 [minor, fixable]** The evidence-access arm is not source-access-only: it also redirects
     the by-design clause to the cognition materials and drops the objective-constraint
     perspective's negative-sentinel exemption (Section 4.4). One sentence discloses this, but the
     headline phrasing ("withholding the implementation source raises recall 39 → 48") invites the
     single-variable reading. Fix: either report the claim as a bundled contrast, as the
     four-perspective contrast is, or add the arm that isolates the source channel.

3. **Perspective** — Adequate
   - **3.1** The lessons are concrete and mostly transferable, each tied to a measured finding:
     audit what your oracle reads, not only what it concludes (Section 4.3 gives the method and the
     numbers); price the deferral channel and the contrast, not just the level; check the dispatch
     before re-architecting the judge (the four defects found by outside readers, not by the
     authors' own audit); self-auditing a stage against its own printed rule is a five-line script
     that revealed 22 forward departures. The generalization of the second lesson is bounded by the
     paper's own non-replication — the Discussion concedes it is "advice about where to look rather
     than a property of the protocol" — which is exactly what caps this criterion at Adequate (the
     bounded evidence is itemized at 2.5).
   - **3.2 [minor, fixable]** Related-Work coverage is careful but has one clear gap. DocPrism
     (`docprism25` in the paper's own `TestVDB.bib`; "Multi-lingual Detection of Incorrectness
     Inconsistencies between Code and Documentation") is never cited, although the Section 7
     sentence that names the "LLM-era successors" of the comment–code inconsistency literature
     cites only DocChecker and C4R-LLaMA, and DocPrism belongs to that same family with an explicit
     focus on incorrectness-level inconsistency. Separately, the routing/escalation mechanism that
     Section 4.5 measures is grounded in a single citation from the abstention literature
     (`trustorescalate25`); the paper's own framing ("selective prediction prices the same
     accounting from the other side") invites positioning against the learning-to-defer /
     selective-classification line. [The latter is provisional: I did not survey that literature
     this session, so I do not name a specific omitted work.] Fix: cite and position DocPrism;
     strengthen the deferral positioning or drop the appeal to it.
   - **3.3** I verified the paper's characterizations of the competitors it actually rests on,
     against fetched copies or the project's shared cache: Metamon (the quoted profile, precision
     0.722 / recall 0.480, matches its abstract verbatim at the chosen threshold; the mechanism —
     LLM adjudication stabilised by metamorphic queries — is as described); VDBFuzz (crash-oracle
     by its own statement; the 205-template figure matches the released repository's
     `templates/qdrant/` inventory, which I inspected); Ma et al. (debate amplifies bias after the
     initial round, meta-judge resists — verbatim consistent); TRACE (detection falls 21–43 pp when
     only the implementation drifts — accurate, and "adjacent in spirit" is the right label);
     Mughal et al. (83 studies coded; "hallucination named far more often than measured" is the
     review's own phrasing); MASTOR (implementation-as-authority, with the review's stated limit);
     LogicHunter (documentation as the statement of intent, implementation consulted freely);
     AGORA+ (trace-anchored) and SATORI (OpenAPI-field-anchored). No mischaracterization found.
     The one claim I could not verify is Bodicoat et al. ("prompting technique and supplied context
     dominate model choice in oracle accuracy"): I confirmed the citation's identity (AIware 2025)
     but could obtain no text or abstract, so I record it as unverified rather than disputed.
   - **3.4 [minor, fixable]** The Metamon contrast compresses one step. Metamon captures behaviour
     by *executing* EvoSuite-generated regression tests (assertions recording actual outputs) and
     deliberately does not show code to the LLM; the final arbiter is the LLM, which is why the
     paper's "self-reference" framing is defensible for authority. But "its falsifier is another
     LLM question" elides the execution-derived behaviour evidence, and a reader of Section 7 alone
     would not know Metamon runs anything. Fix: state the delta as authority and granularity (no
     source grounding, method-level prose) rather than as "no execution evidence".

4. **Verifiability** — Excellent
   - **4.1** The Data Availability section declares a replication package at an anonymous URL and
     enumerates what it contains: the pool, the frozen per-run verdicts of all twelve
     configurations, the packages the study read (post-rebuild, cognition-stripped), the dispatch
     texts and the judging prompts they instantiate, the pair-audit verdicts, the adjudication
     worksheet and the blind passes, and the five analysis scripts that Section 4.1 names
     (`recompute_paper_numbers.py`, `clause_tally.py`, `convention_pricing.py`,
     `bootstrap_net_f1.py`, `audit/pair_audit.py`). It also states that where a run was re-judged,
     the re-judged cases and the pre-repair state ship beside the untouched batches, so either pool
     is reconstructible from the package alone — which is what makes the leak repairs auditable
     rather than merely disclosed.
   - **4.2 [minor, fixable]** Four reports are expressly outside the shipped artifact, and the
     paper marks them: the fix-PR characterisation ("all 23 merged fixes modify implementation
     code, 15 also add a regression test, none documentation-only") is "not part of the shipped
     artifact" (Sections 1, 4.2, 6), and three printed analyses — the catch-all composition, the
     expectation-framing check and the C row's evidence classification — are "printed but not yet
     scripted", with the artifact's script-coverage note saying so. The honesty is exemplary; the
     fix is mechanical — ship the fix-PR table and script the three printed analyses — and would
     remove the only non-recomputable numbers in the paper.
   - **4.3 [minor, fixable]** The artifact link is declared. I could not establish that it resolves
     from a non-interactive client (the platform returns `not_connected` for the declared
     repository id and for a control id alike), so I record it as declared-but-unchecked rather
     than as dead. Please confirm the anonymous link is live and browsable for reviewers.

5. **Presentation** — Adequate
   - **5.1** The structure is sound and the four tables each carry load (oracle families and their
     anchors; the twelve configurations; the pair-level audit; the clause census grouped by
     assigned outcome). The census table's columns (n / right / wrong / accuracy) with the
     catch-all row marked as differing in kind in the caption and body is the kind of detail that
     prevents misreading.
   - **5.2 [minor, fixable]** Section 4.4's contrast ordering is ambiguous where it matters most.
     The four-perspective paragraph prints the rule-bearing *baseline* first ("−11 true bugs on the
     second (41 vs. 30, 12/1, p = 0.0034)"; "51 vs. 48"), whereas three sentences earlier the same
     subsection prints the *evaluated* arm first ("the deployed stage against the flat judge is 48
     vs 34"). The −11 sign and the confirmed-set pairs are the only cues that the first number is
     the control, and a reader who assumes the paragraph's own framing (the perspective contrast)
     will read the second-backbone row as a gain rather than a loss. Fix: name the arms in these
     parentheticals, or fix one X-vs-Y order for the paper.
   - **5.3 [minor, fixable]** The statements about which perspective letters are identified vary
     across the paper: Section 1 says "the two refuting clauses are identified by the evidence
     their cells cite", the abstract says "the perspectives are identified by their content", and
     Section 4.5 says "two of the four are identified uniquely" (C by the weak-refutation value, D
     by the source vocabulary). Align the three with Section 4.5's more precise claim, which is the
     one the census actually establishes.
   - **5.4 [minor, fixable]** One sentence in Section 4.5 is self-undermining as written: "None
     rests on observed behaviour alone, which is the property the legend requires of this clause."
     The legend requires affirmative verbatim intent evidence (a comment, docstring, or maintainer
     quote), which is stronger than "not observed behaviour alone" — and the next two sentences
     turn on exactly that gap when they argue that the two structural-inference closures are
     inadmissible. Rewrite so the necessary and sufficient conditions are not conflated.
   - **5.5 [minor, fixable]** "Generation" is overloaded. Section 4.1's "Both raw generations ship
     alongside the cleaned one" sits next to Data Availability's "the earlier rebuilt generations
     are archived separately and do not ship", where the first plainly concerns verdict
     generations and the second package generations. Disambiguate the term in both places.
   - **5.6 [minor, fixable]** Minor wording, for a cleanup pass: the abstract's "58 cite a source
     file or a landing page rather than the page that documents the constraint and were re-anchored"
     reads better with a comma or a split; Section 4.5's "which is the property the legend
     requires" (see 5.4) and "the split that puts the latter in the catch-all below" are dense
     enough to need a second reading; and the contribution list's "with the counterfactual priced
     at both readings" would be clearer as "priced under both counting readings".

### Questions for Authors

- **Q1:** How are the A and B cells distinguished from one another (they share all three values)?
  Is it the schema's field names, the declared column order, or an inference from the value
  distributions? — [intended effect: this is the identification of the column the entire 50/24/80%
  result attaches to. If the mechanism is textual and stated, item 2.8's concern is discharged and
  criterion 2's evidence base is firmer; if it is only the distributions, the census's headline
  attribute is unverifiable as printed and 2.8 stands as a major gap.]
- **Q2:** Would you run the guard as an intervention rather than a replay — re-adjudicate the
  cases the contract clause closed under a verbatim-evidence requirement, on the same frozen
  packages — and report what a guarded judge actually reaches? — [intended effect: this is the
  computation Section 4.5 names as impossible from frozen data. If it reproduces the replay's
  seven-bug recovery, item 2.6's objection is discharged and the prescription becomes a measured
  effect; if it does not, the paper's own framing (a property of the convention) is confirmed and
  the contribution should be reworded accordingly.]
- **Q3:** Under the forced reading the routing step makes the schema-repaired control *worse*
  (29 → 27, Section 4.4). What does the deployment's convention buy, stated without the
  routed-counts-as-confirmed credit — is there any reading under which the added rule improves the
  judge's decisions rather than its accounting? — [intended effect: this bears directly on item
  2.3's positive result and 2.6's prescription. A concrete answer (e.g. the hand-priced queues at
  +3/+4 already given) would let the paper state the rule's value as a routing/queue artifact
  rather than an accuracy effect, tightening both items.]
- **Q4:** Of the 30 negatives, how many carried a maintainer disposition, and how do the
  FP-side quantities (suppression 21/30, precision 0.917, the catch-all composition) move if the
  self-adjudicated ones are excluded? — [intended effect: item 2.9's severity. A sensitivity bound
  computed on the maintainer-disposed subset would move the FP-side evidence from Adequate to a
  documented bound; absent one, 2.9 stays as a standing caveat on a quarter of the census's
  denominator.]
- **Q5:** By what screening rule were the 132 ledger rows selected from the pipeline's raw output,
  and how many candidates did the runs on those 16 versions produce before screening? — [intended
  effect: item 1.3. The paper is candid that no detection rate exists, but a candidate denominator
  (even from the voided runs, as raw counts) would let a reader see the submission funnel's shape;
  without it, the campaign's yield remains a numerator with no denominator.]


---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Accept

### Summary

The paper reports three things about detecting documentation--implementation bugs in vector database
management systems (VDBMSs). First, a mining campaign: 81 adjudicated submissions across Milvus,
Qdrant and Weaviate, of which maintainers confirmed 51 as real bugs and fixed 23 through merged PRs,
recorded in a 132-row ledger spanning 19 versions. Second, an audit of the material the pipeline's
confirmation stage reads: the per-case packages distil vendor documentation into constraint records
with a citation each, and the authors audited all 134 (constraint, cited-page) pairs as the pipeline
produced them, finding 18 supported as cited, 58 anchored to a source file or landing page and
re-anchored, and 58 with no support on the cited page; the same audit exposed two channels through
which material the stage was forbidden to read had reached it, both repaired, with the affected cases
re-judged. Third, a census of the deployed confirmation stage's 243 judgments (81 cases times three
runs), classified by the clause of its fixed aggregation sequence that closes each one: contract
refutation closes 50 and is wrong 24 times, by-design refutation closes 19 and is wrong twice, and
the catch-all routes 69 to human review. Replaying the protocol with contract refutation routed
instead of closing moves recall from 39/51 to 46/51 and suppression from 21/30 to 12/30 under the
authors' counting convention, and changes nothing under the forced reading.

Around these, the paper supplies a twelve-configuration re-adjudication study over two model
backbones with paired exact McNemar tests at both the confirmed-set and recall levels, a Holm
correction over a stated family, bootstrap intervals for its net and F1 claims, a forced-verdict
reading reported beside every contrast with the convention priced at the two places the paper prices
it, an independent adjudicator's blind pass, a blind second reader for the pair audit, a run of the
released VDBFuzz template set against Qdrant (0 oracle anomalies), and four defects that readers of
the shipped dispatches, not the authors, found in the tooling.

### Core Strengths

- **S1:** The evidence-package audit measures the distillation step that every "distil a specification
  from documentation, then judge against it" pipeline performs and that, to our knowledge, none
  reports, and it is itself independently checked (blind second reader, 31/36, $\kappa=0.78$) and
  falsification-oriented (a zero-expectation-framing check over all 81 rebuilt packages). — see 2.1,
  4.1, 4.2
- **S2:** The clause census is constructed so that its headline survives the authors' own attempts to
  falsify it: the letters are identified from the evidence their cells cite rather than assumed, the
  load-bearing count is invariant across the two aggregation rules the dispatch prints, and it is
  computed only on maintainer-confirmed labels, so it does not rest on the 30 negatives the authors
  adjudicated themselves. — see 2.2, 2.3
- **S3:** Every contrast is reported at both the confirmed-set and recall levels, the counting
  convention is priced rather than hidden (including an independent adjudicator who agrees with the
  authors' joint reading at essentially chance and is reported as a bound), and the paper's own
  instrument defects are reported rather than quietly repaired. — see 2.4, 3.3
- **S4:** The novelty deltas the paper draws are narrow and hold when checked against the papers
  themselves: Metamon, CASCADE and MASTOR are characterized as their own texts describe them, and
  Table 1's exclusion claim (no oracle family takes its expectation from untagged, system-level
  behavioural prose) holds against AGORA+, SATORI and MASTEST as well. — see 3.1, 3.2

### Core Weaknesses

- **W1:** The census's diagnosis — "the protocol guards the clause that is already clean" — compares
  two clauses that fire at different points of the aggregation sequence on different case sets
  (contract refutation is tried before the by-design perspective and closes 50 judgments; by-design
  closes only the 19 that contract, objective-constraint and cognition clauses all left open). The
  paper separates the census from the pair audit's defective-rows rival, but not from a selection
  rival, and the paper's own account already restricts the headline to one backbone. — see 2.5
- **W2:** Bundled contrasts are priced carefully in the body and then re-bundled in the Conclusion:
  §4.4 divides the headline gain into a schema-line repair (30$\to$35) and the routing rule (35$\to$39),
  while the Conclusion credits "adding an aggregation rule" with the whole 30$\to$39 movement, and
  §4.1's enumeration of contrasts that change more than one thing omits the evidence-access arm even
  though §4.4 discloses that it changes three. — see 2.6, 2.8
- **W3:** Three statements do not match the material shipped with the paper: the first leak repair's
  re-judged arms (as §4.1 lists them versus the artifact README), the second reader's 15 SWAP pairs
  (versus a sample the README describes as 12 per verdict), and the released baseline's oracle (the
  one claim in §4.6 contradicts the README's description of that oracle as a liveness check). The
  paper's central promise — every rate computed on the cleaned pool, everything checkable — rests on
  exactly these disclosures. — see 2.7, 4.3, 4.4, 4.5

### Detailed Assessment

1. **Importance & Scope** — Excellent
   - **1.1** The problem's importance is established by external evidence rather than asserted: the
     yield section (§4.2) reports 51 of 81 adjudicated submissions confirmed by maintainers and 23
     fixed by merged PRs, per system (Milvus 29/43, Qdrant 14/28, Weaviate 8/10), which is validation
     the pipeline cannot manufacture. The preliminaries (§2) anchor the target class in the field's own
     numbers: the empirical bug study the paper cites attributes the dominant share of VDBMS bugs to
     functional failures (the service stays up and returns wrong results) against a crash minority, and
     VDBFuzz's oracle is crash-only by construction — I verified both against the cached papers. The
     practical stakes are stated concretely in §1 (a disabled filter returns all matches, an
     out-of-range `nprobe` returns results, and no error code is logged).
   - **1.2** Scope is stated where each claim is made rather than quarantined in a limitations
     section: §2 separates documentation consistency from vector-search correctness and says the latter
     is not measured; §4.2, §1 and the Threats section repeat that the ledger is not a detection rate
     and that the detection-ability runs were voided; §4.3 says the audit rates are this distiller on
     these three vendors' documentation; §4.5 states that the census covers the primary backbone only
     and that it does not reproduce on the second. For a paper whose headline number could easily be
     read as a performance figure, that discipline is the reason it cannot be.
   - **1.3 [minor, fixable]** The studied units are the 81 submissions that survived the pipeline's own
     screening, and the paper's Threats correctly names this ("submission-filtered subset of one
     pipeline's output") and says recall levels are contrasts rather than operating performance. The
     artifact ships a 32-case anchor experiment on candidates that never entered the pool, which is the
     one measurement that speaks directly to how much that screening shapes the yield and the census,
     and the paper does not report it. Reporting it, or saying why it is not reported, would close the
     largest remaining gap in the scope argument.

2. **Insights & Evidence** — Excellent
   - **2.1** The audit (§4.3) is the paper's most transferable result and it is done at the right
     object: the 134 pairs as the pipeline produced them, before the rebuild, and the paper is explicit
     that this describes the material as found rather than the improved material the judges went on to
     read. It gives both totals and mechanisms (version drift from a single fixed contract version;
     constraints that exist only as
     prose, such as a `nprobe` bound tied to `nlist`), it audits a second, different object at case
     level (12 headline assertions, of which five supported, three dropped, two over-strong, two
     recorded as weak-evidence, all acted on), and it closes with a falsification test of its own
     rebuild (zero of 81 packages contain an expectation-framed sentence; the 19 phrasing hits are all
     verbatim server responses). The counts reconcile (18+58+58=134; 5+3+2+2=12), and the second
     reader's support is genuine: the artifact ships the stratified sample, the blind classifications,
     and the withheld key.
   - **2.2** The census (§4.5) is built to survive contact with a hostile reader, which is unusual for
     an error-attribution result. The letters are not assumed: C uniquely records weak refutations (59
     cells) and D uniquely carries the source vocabulary, so the clause mapping is read off cell
     contents and the same content test is run on the second backbone before that backbone's count is
     used. The 24-count is invariant across the two aggregation rules the dispatch prints, and the
     paper notes that the one pair the alternative rule would route does not occur on this backbone
     (three times on the other). The materials cross-tab is the sharpest move: it takes the rival the
     paper itself names ("the two results could be one phenomenon---defective rows failing a containment
     check rather than a protocol closing wrong") and shows 20 of the 24 wrong closures fall on the 59
     packages the audit judged supported and none on the 18 it left without documented
     evidence, which also explains why a mechanical containment check does not simply mirror the pair
     audit's 43.3%. I recomputed the table's sums (61+21+7+50+19+16+69=243; 24+2+4=30 incorrect
     closures to False-Positive; 45=28+17 catch-all judgments resting on bugs; 59+3+18+1=81) and they
     hold.
   - **2.3** The scope disclosure is not a formality: the pre-repair contrast (contract refutation 47,
     by-design 20) and the second backbone's reversal (by-design wrong 22 of 50, unguarded clause 24 of
     48 = 50% rather than 80%) are printed inside the census section, next to the headline, not
     deferred; and the abstract and contribution list carry the same scope. A reader who only reads the
     abstract of this paper is told the same bounded claim the body supports.
   - **2.4** The statistics are appropriate and correctly computed. Paired exact McNemar is reported at
     both the confirmed-set and recall levels for every contrast, the two levels are allowed to
     disagree and neither is privileged, the ten-test family behind the Holm correction is named by
     membership rather than size, and the interval methods (matched-pairs Wald for recall differences,
     paired case-level bootstrap for net and F1) match the claims they support. I re-derived five of
     the printed exact p-values from the printed discordant cells (0/9$\to$0.0039, 0/14$\to$0.0001,
     12/1$\to$0.0034, 2/14$\to$0.0042, 16/2$\to$0.0013) and the Holm step-down ($\alpha/10$,
     $\alpha/9$, $\alpha/8$, $\alpha/7$ all clear their four smallest p-values; $\alpha/6=0.00833$
     stops at 0.0225): all correct.
   - **2.5 [minor, fixable]** The census's interpretation rests on a comparison the paper does not
     fully bank. Contract refutation is tried before the by-design perspective in the printed sequence
     (§3.5, §4.5), so A=Refuted fires on the largest and most heterogeneous set (50 closures, including
     any candidate whose cited contract text contradicts the observation) while C=Refuted closes only
     the 19 judgments that A, B and D all left open. The observed accuracy gap (26/50 = 0.52 versus
     17/19 = 0.89) is therefore consistent with two stories: the verbatim-evidence guard is doing the
     work, or C's small residual set is easier. The paper names and kills one rival (defective rows,
     §4.5) but not this one, and the sentence "the protocol guards the clause that is already clean"
     asserts the second story without evidence. The prescription survives either way, because it rests
     on error mass — 50 closures at 48% wrong is 24 errors against 19 at 11% is 2 — which is a
     volume-dominated argument. The fix is to say so and to name the selection rival explicitly; the
     numbers, the replay and the cross-tab all stand.
   - **2.6 [minor, fixable]** The evidence-access result (§4.4) is presented as "withholding the
     implementation source raises recall 39$\to$48 (...; forced 27$\to$31) and cuts suppression from
     21/30 to 12/30", but the §4.1 account of the control as "a traceable edit" lists only the drop of
     the `source=` path, while
     §4.4 itself discloses two further changes in the same arm (the by-design clause redirected to the
     cognition materials, and the objective-constraint perspective's negative-sentinel exemption
     dropped). §4.1 also enumerates three contrasts that "change more than one thing"; on its own
     disclosure this arm is a fourth. The ablation-isolation caveat is present, so the finding is
     usable, but the paper's accounting promise should cover this arm too.
   - **2.7 [minor, fixable]** The baseline's measurement instrument is described inconsistently with
     the material shipped with the paper. §4.6 says "the per-template oracle fires on 5xx rather than
     on service death", while the artifact's README describes the released per-template oracle as a
     `GET /`-returns-200 liveness check that records an anomaly "once it stops holding" — which does
     fire on service death. §2's earlier gloss for the tool as a whole ("fires on a 5xx response or a
     failed request") also merges VDBFuzz's own definition of its oracle (crash: process termination,
     segmentation faults, runtime exceptions — I checked the cached paper, which never mentions 5xx)
     with what the released templates do. The bound argument survives and is in fact helped by the
     correction: a liveness check fires on a crash, so a zero under it is a stronger statement about
     the released configuration than the paper claims, and the second half of the sentence (the
     mutation vocabulary topping out below the values some crash classes need, 65,536 and 10,000) is
     corroborated by the shipped baseline sources.
   - **2.8 [minor, fixable]** The Conclusion attributes the bundled contrast to one of its parts:
     "Adding an aggregation rule that lets it route a case to human review rather than close it raises
     recall on both backbones (0.588 to 0.765 ...)", where 0.588$\to$0.765 is the flat judge to the
     rule-bearing judge, a pair that differs by both the schema-line repair and the rule. §4.4 splits
     it 30$\to$35$\to$39 and §5 says plainly that "a one-line schema repair moved five of the headline
     nine bugs", so the body is right; the summary sentence re-bundles what the paper took care to
     separate, and it is the sentence a reader is most likely to quote.

3. **Perspective** — Excellent
   - **3.1** I checked the deltas the paper draws against the competitors themselves, and they hold.
     Metamon is described as asking an LLM whether a generated regression oracle agrees with the
     method's documented specification and stabilising that judge, with a published profile of
     precision 0.722 at recall 0.480 — the surviving numbers match its paper verbatim, and the
     "falsifier is another LLM question" gloss is right (its metamorphic variant negation is a check on
     the judge, not an external authority). CASCADE is described as inverting the roles at method
     granularity with a regenerated implementation as falsifier — correct, and its own residual
     false-positive analysis (both residual FPs came from generated code and tests sharing an
     assumption the prose left under-specified) sharpens the authors' case for an external falsifier
     rather than weakening it. MASTOR is described as taking the implementation as its authority —
     correct, and MASTOR's own limitations state that it cannot detect violations of intended
     requirements not reflected in code. Ma et al. (Many Minds) are described as measuring multi-agent
     judging for bias rather than accuracy and finding debate amplifies biases after the first round
     while a meta-judge resists — correct, and the paper carries the caveat that its own "changes
     which cases are decided, not how many" reproduction reverses on the second backbone. Table 1's
     exclusion claim also holds for the structured-source row: AGORA+'s oracles are response-property
     invariants learned from observed traffic with no natural-language documentation prose as their
     source, SATORI's are per-response-field oracles from OpenAPI metadata with a fixed unary oracle
     catalogue, and MASTEST's are spec-anchored status and type checks. The claim that none of these
     anchors at untagged system-level behavioural prose is exactly right, and the paper does not
     overclaim beyond it.
   - **3.2** The paper's framing of its own contribution is narrow and correctly drawn ("not a new
     oracle but an audit of the oracle's *input*"), and the gap it claims is corroborated by the
     literature it cites: the systematic review of 83 oracle papers reports hallucination named far
     more often than measured, which is the measurement the audit supplies. Scoped coverage searches
     in both of my specialty areas (NL-documentation-derived oracles; LLM-judge organization,
     abstention and escalation) surfaced no genuinely related uncited work that would compete with
     either the audit or the census; the closest judge-side works the census rests on are all cited.
   - **3.3** The lessons are concrete, priced where possible and applicable beyond this case: measure
     the support of what your oracle reads (a sample of pairs against their cited pages is cheap);
     price the deferral channel and the contrast, not only the level; check the dispatch before
     re-architecting the judge ("a one-line schema repair moved five of the headline nine bugs");
     self-auditing a stage against its own printed rule is a five-line script. The disclosure that none
     of the four dispatch defects was found by the authors' own audit is the kind of negative lesson
     that is rarely published and is the most reusable thing here for anyone building agentic
     pipelines.
   - **3.4 [minor, fixable]** One uncited adjacent work is worth one sentence, marked provisional
     because I could retrieve only its title, venue and partial abstract: an FSE 2025 empirical study
     of LLM-as-a-judge against human evaluators in software engineering (DOI 10.1145/3728963). It is
     not a competitor to the census claim, but it is the natural place to position the paper's
     independent-adjudicator result (κ = −0.01/0.08/0.11), which currently sits alone.

4. **Verifiability** — Excellent
   - **4.1** The artifact is declared and reachable. On 2026-09-15 I resolved the declared URL and
     fetched its README (HTTP 200) with content matching this paper; a control artifact on the same
     host behaves identically at the `/r/` route, so reachability is not in question. The README's
     layout matches the Data Availability manifest item for item: the pool and ledger, the frozen
     per-run verdicts for every arm and run, the packages the study read, the dispatch texts and the
     two judging prompts under `rq2/prompts/`, the pair-audit verdict records with the second reader's
     sample, verdicts and withheld key, and the analysis scripts. Where a run was re-judged after
     either leak repair, the re-judged cases and the pre-repair state both ship, as the paper says, so
     either pool is reconstructible.
   - **4.2** The paper names the five scripts and what each recomputes, and it is honest about the
     three quantities that are printed but not scripted (the catch-all composition, the
     expectation-framing check, and the C row's evidence classification) — the shipped README repeats
     the same three and adds that two of them are reconstructible from the verdicts and that the routed
     queue is defined in code. The paper's counting-convention definition and the artifact's routed-queue
     definition are the same sentence. For a paper whose headline is a count, that is the right
     verifiability posture.
   - **4.3 [minor, fixable]** The audit's object does not ship: the packages the audit measured are the
     as-produced (pre-rebuild) ones; the paper's Data Availability says the earlier generations "are
     archived separately and do not ship", and the artifact README adds that the pre-rebuild originals
     sit in the development tree. The audit's verdict records do ship, so whether the 43.3%
     can be re-derived, as opposed to inspected, depends on whether those records carry the as-produced
     constraint text and cited anchor for each pair. Saying which it is (or shipping the pre-rebuild
     pairs) is the last step in making the paper's most transferable number independently checkable.
   - **4.4 [minor, fixable]** The paper's account of the first leak repair's reach does not match the
     artifact's. §4.1 says the stripped cognition sections were re-judged across five configurations —
     "contract core, flat judge and source-only on the primary at three runs each, the second backbone's
     source-only at three and its flat judge at one"; the README lists the re-judged runs for that
     repair as `run_fullc*`, `run_donly*`, `run_flat*`, `run_donlyq*`, `run_flatq1`. The two lists
     agree on the flat, source-only and second-backbone families and disagree on whether the contract
     core or the full stage's re-adjudication carries that repair. Since "every number this paper
     reports is computed on the cleaned pool" is a disclosure claim resting on this list, the two
     documents should agree; the second repair's list matches between them exactly.
   - **4.5 [minor, fixable]** The second reader's paragraph reports "the 15 SWAP pairs" as all
     re-called SWAP, while the artifact describes the sample as "12 per verdict" (36 = 12+12+12), which
     would put 12 re-anchored pairs in it. One of the two is wrong, and the number is inside the
     sentence that carries the audit's independent verification.

5. **Presentation** — Adequate
   The paper is complete and understandable and its structure is sound, but the presentation of the
   results is where it costs the reader most: the numbers live in prose, and several load-bearing
   sentences carry more ambiguity than a claim this precise can afford. Each item below is individually
   a blemish rather than a defect; together they are why this criterion sits below the others.
   - **5.1** The structure is complete and conventional (Preliminaries, Approach, Evaluation,
     Discussion, Threats, Related Work, Conclusion), the aggregation machinery is legible because the
     clause legend is fixed once (§3.5) and the census table is grouped by the outcome each clause
     assigns, Table 2 makes the twelve configurations comparable, and the prose reads as carefully
     edited. The stripped source carries no comment, `\iffalse` or `\begin{comment}` markers, so
     nothing was hidden by the strip.
   - **5.2 [minor, fixable]** The results exist only in prose. The per-arm outcomes (recall under the
     convention, forced recall, suppression, leaked false positives) are scattered across §4.4 and
     compressed in the "readings reorder the arms" paragraph into ranges over nine arms, and the
     contrast grid (which pair, which reading, which interval) has to be reconstructed sentence by
     sentence. One table — arm rows against convention recall, forced recall and suppression, with the
     contrasts listed beneath it — would let a reader check the paper's claims at a glance and would
     also make the two-level disagreements visible instead of narrated.
   - **5.3 [minor, fixable]** Several load-bearing sentences need a second reading. "No recorded cell on
     this backbone carries the A=Refuted-with-B=Confirmed pair that the other rule would route" leaves
     "the other rule" unresolved, and the surrounding argument (which rule is operative) is exactly
     what the paper needs the reader to hold. "Two of the three independent passes land at the forced
     floor" does not say which two or what a pass landing at the floor means for the joint reading it
     bounds. The five-configuration list in §4.1 mixes arms and run counts inside one sentence, and the
     two-level p-value reporting is correct but reads as a wall of numbers without the table of 5.2.
   - **5.4 [minor, fixable]** Terminology drift that matters for a reader checking the artifact:
     SWAP, DROP and SUPPORTED appear only in the second-reader sentence and are never mapped to the
     table's own three verdict names; "the operator's page" (§4.3) reads as a slip for the endpoint's
     page; and the artifact is organized as RQ1/RQ2/RQ3 while the paper introduces the same paths
     without ever naming that numbering.

### Questions for Authors

- **Q1:** Can you say what a verbatim-evidence guard on contract refutation would do to the accuracy of
  the clause that fires before the by-design perspective, or bound that reading in words? If the
  selection rival is named and the census's claim rests on error mass (50 closures at 48% wrong against
  19 at 11%), item 2.5's caveat becomes a wording note rather than a gap in the reading of your
  headline.
- **Q2:** Which account of the first leak repair's re-judged arms is correct — §4.1's (contract core,
  flat judge and source-only on the primary; second-backbone source-only and one flat run) or the
  artifact README's (`run_fullc*`, `run_donly*`, `run_flat*`, `run_donlyq*`, `run_flatq1`)? If the
  README is right, does any reported contract-core figure rest on a generation that was not re-judged?
  Item 4.4 would then stop being a documentation nit and the cleaned-pool sentence would need a
  qualifier.
- **Q3:** The artifact lists five baseline runs (the 205-template full-coverage run plus four
  head-to-head runs up to 161,046 logged requests). Does any of them record a non-zero oracle anomaly,
  and why does §4.6 report only one? If any did, the zero would need to be scoped to the reported run;
  if none did, reporting them strengthens a bound you currently state more narrowly than necessary.
- **Q4:** Do the pair-audit verdict records carry the as-produced constraint text and cited anchor for
  each pair, and is the second-reader sample 15 re-anchored pairs (as §4.3 says) or 12 per verdict (as
  the artifact README says)? If the records carry the row text, the 43.3% is independently re-checkable
  and item 4.3 disappears; if not, shipping the pre-rebuild pairs is the last step. Either answer also
  settles item 4.5, whose count sits inside the audit's own verification sentence.
- **Q5:** Should the Conclusion name the contrast it is pricing (flat judge to the schema-repaired
  rule-bearing judge) instead of "adding an aggregation rule"? As written it credits the rule alone
  with a movement §4.4 divides 30$\to$35$\to$39 and §5 attributes five of the nine bugs to the schema
  line, so a one-clause change would remove the only place where the summary outruns the section it
  summarizes (item 2.8).


---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Accept

### Summary

The paper reports an experience study of a defect-mining pipeline aimed at documentation--implementation inconsistencies in three production vector database systems (Milvus, Qdrant, Weaviate). The pipeline has four stages; the object of study is the last one, a bug-confirmation stage in which an evidence builder assembles a per-case evidence chain and an LLM-based chain auditor cross-examines it under a fixed aggregation rule, four perspectives (contract, objective constraints, behavioural elegance, maintainer cognition), and a three-valued verdict space (Confirmed, False-Positive, Human-Review).

Three results are reported. First, a campaign: maintainers confirmed 51 of 81 adjudicated submissions and fixed 23 through merged PRs; the ledger holds 132 rows across 19 versions; the experiment that would have measured per-version detection was voided and no detection rate is supplied. Second, an audit of the 134 (constraint, cited-page) pairs the confirmation stage reads: 18 supported as cited, 58 mis-anchored and re-anchored, 58 unsupported by their cited page; two leakage repairs followed the same audit, and every reported number is recomputed on the cleaned pool. Third, a clause-level census of the deployed configuration's 243 judgments on the primary backbone: contract refutation -- a mechanical containment check carrying no evidence requirement -- closes 50 judgments, 24 of them on maintainer-confirmed bugs, and supplies 80% of the stage's incorrect closures to False-Positive, while the guarded by-design clause closes 19 and is right 17 times; a replay that routes the unguarded clause instead of closing on it recovers seven true bugs for nine interceptions under the deployment's counting convention and nothing under the forced reading. The paper also reports four defects in its own dispatches, found by reviewers reading the shipped texts rather than by its own audit.

### Core Strengths

- **S1:** The paired audit of the oracle's *input* -- 18/58/58 of 134 cited pairs, with a blind second reader (31/36, kappa = 0.78) and an explicit refusal to generalize -- is a cheap, transferable measurement that no pipeline in this line reports. -- see 2.2, 1.1
- **S2:** The measurement design is disciplined and its limits are declared up front: twelve frozen configurations, three runs each, control arms that are traceable one-line edits of their parents, both counting readings reported for every contrast, and an explicit list of the three contrasts that change more than one thing. -- see 2.1
- **S3:** The clause census is constructed to resist its own obvious confound: the perspectives are identified by their recorded vocabularies rather than assumed, the pair-audit explanation is separated by a cross-tab (20 of the 24 wrong closures fall on packages the audit judged supported; none on those it left unsupported), and the load-bearing count is checked for invariance across both printed aggregation rules and restricted to maintainer-confirmed labels. -- see 2.3
- **S4:** The paper reports its own instrument's defects and its own nulls: four dispatch defects found by reviewers, two leak repairs with before/after numbers, a voided detection experiment, and a misleading log artifact in the baseline tool. That is what makes the "auditable pipeline" claim credible rather than aspirational. -- see 3.1, 4.1, 5.1

### Core Weaknesses

- **W1:** The census -- the paper's headline lesson -- is a one-backbone finding that reverses on the second backbone, and the reason for the reversal is left undiagnosed even though the second backbone carries a known, fixable instrument defect (the doubled perspective definition leaves the D field with two incompatible vocabularies). -- see 2.4
- **W2:** The priced counterfactual does not reconcile internally: "+7 true bugs for nine interceptions" implies sixteen flipped cases, while the supporting sentence reports fifteen cases closed by the clause in at least two of three runs with seven of them true bugs; the "case-level maximum" argument also omits single-run flips. The figure appears in the abstract, the introduction, §4.5 and §5. -- see 2.5
- **W3:** Every suppression, interception, net and F1 statement rests on the 30 negatives the authors adjudicated themselves, and the hand-priced reading that carries §4.4's "worth three, and that is a floor" is a single non-blind pass that an independent adjudicator reproduces at near-chance. The paper bounds both, but the conclusions inherit them. -- see 2.6, 2.7
- **W4:** The results are carried almost entirely in dense prose with no per-arm outcome table, and the four-perspective contrast never names its two arms, printing the rule-bearing arm first where the rest of §4.4 prints the deployed stage first. -- see 5.2, 5.3
- **W5:** Three gaps between what the paper says a reader can check and what it ships or carries: the Related Work says §6 carries the training-data contamination threat and it does not; the audit's input generation does not ship; three printed analyses are unscripted. -- see 2.9, 4.2, 4.4

### Detailed Assessment

1. **Importance & Scope** — Excellent
   - **1.1** The residual this paper works in is defined by a structural argument rather than a gap-in-the-market claim: §2 establishes that the dominant VDBMS defect shape is non-crashing (the bug study's functional-failure share; the roadmap's oracle-definition problem), that the one dedicated VDBMS fuzzer's oracle fires on process death or 5xx, and hence that the documentation--implementation residual is out of that oracle's reach by construction; Table 1 then positions six oracle families by where each anchors its expectation and why each misses. That is an effective, compact context for a problem that matters to anyone deploying a VDBMS under a retrieval-augmented application. (I did not survey the field for this review; the positioning against the cited works is taken from the paper and is provisional.)
   - **1.2** Scope statements are explicit, load-bearing and repeated where it counts: the pool composition and label provenance (§4.1); the ledger's nature as "a record of submissions and adjudication, not a per-run detection rate" with the voided experiment named (§4.2); the census's scope to the primary backbone (§4.5); the unjudgeable case and its convention credit (§4.1, §6). A reader never has to guess which population a number describes.
   - **1.3 [minor, unfixable]** The campaign contribution carries less evidential weight than its position suggests, and no revision can change that: because the 15-version experiment was voided in full, "51 of 81" is a yield over screened submissions rather than a detection ability, and the missing rate cannot be supplied. The paper discloses this twice and is right to; I record it only because contribution 1 is listed first while carrying the least evidential force of the three.

2. **Insights & Evidence** — Adequate
   - **2.1** The instrument is fit to the question and mostly isolates one variable at a time: twelve configurations (Table 2) each re-adjudicate the same 81 frozen packages three times; the controls are traceable edits (the schema-fix arm changes one output-schema line; the aggregation arm changes that line plus one sentence plus an appended clause; the source-withheld arm drops the source path from every per-case material line); and the three contrasts that change more than one thing are named rather than hidden (§4.1). This is the strongest part of the study.
   - **2.2** The package audit (§4.3) is the paper's most distinctive new measurement, and it is done carefully: every one of the 134 pairs is checked against the page it cites at the version the row claims, the three-way split is reported with an explicit "each of 134, not combined" caption (Table 3), the two dominant mechanisms (version drift; conceptual-only documentation) are named, the rebuild is checked for the failure this class of work invites (zero of 81 packages contain an expectation-framed sentence), and a blind second reader on a stratified sample of 36 reachable pairs agrees on 31 (kappa = 0.78). The paper also explicitly declines to generalize these rates to LLM distillation at large.
   - **2.3** The census (§4.5) is built so that its most plausible alternative explanation is testable: the perspectives are identified by their recorded value vocabularies rather than assumed (no cell outside C records a weak refutation; no cell outside D carries the source vocabulary); the pair-audit confound is separated by a cross-tab showing that 20 of the 24 wrong contract-refutation closures fall on packages the audit classified as carrying documented evidence (rate 0.11) and none on the packages it left without; and the load-bearing 24 is checked for invariance across both printed aggregation rules and computed only on maintainer-confirmed labels. That is the right construction for a claim of this shape.
   - **2.4 [major, fixable]** The census does not reproduce on the second backbone (§4.5): there, contract refutation closes 56 judgments and by-design closes 50, of which 22 are wrong, so the guarded clause is no longer the accurate one, and the unguarded clause supplies 50% rather than 80% of incorrect closures. The paper states the scope clearly, but it leaves the cause open -- on that backbone the dispatch's doubled perspective definition leaves D's cells carrying two incompatible vocabularies, and the paper can only say it "cannot rule out the letters meaning different things there." The instrument fix is known and cheap on the face of the paper's own design (one schema line, as the primary's flat+schema arm demonstrates), so a re-dispatch could settle whether the reversal is substantive or an artifact. Until then, §5's prescription rests on a single backbone with an undiagnosed alternative explanation on the other.
   - **2.5 [major, fixable]** The priced counterfactual in §4.5 does not reconcile. "moves recall 39/51 to 46/51 and suppression 21/30 to 12/30 ... seven true bugs for nine interceptions" implies 7 + 9 = 16 flipped cases; the supporting sentence says "Fifteen cases are closed by this clause in at least two of three runs, seven of them true bugs" (7 + 8 = 15). The gap is not cosmetic, because the accompanying inference ("so seven is the case-level maximum") also omits that a case can flip when the clause fires in only one of three runs -- routing lifts a case's confirmed-run count from one to two. The number is printed in the abstract, the introduction, §4.5 and §5, so it should be recomputed (convention_pricing.py ships) or the counts reconciled in one place.
   - **2.6 [minor, unfixable]** The 30 negatives that anchor every suppression, interception, net and F1 statement are adjudicated by the authors, with no inter-annotator study (§4.1, §6). The census insulates its load-bearing count by using maintainer labels only, but the counterfactual's interceptions and the net/F1 comparisons of §4.4 are conditioned on labels the paper itself supplies.
   - **2.7 [minor, fixable]** The hand-priced reading that carries §4.4's conclusion ("at the reading this paper considers honest, the deployed change is suggested, not established"; +3 for the rule-bearing control, +4 for the deployed stage) rests on one author-executed non-blind pass, and the independent adjudicator agrees with it on 4, 5 and 6 of 20 commonly ruled cases (kappa = -0.01, 0.08, 0.11), i.e., near chance. The paper bounds this correctly, but the +3/+4 numbers are still printed as findings; they should be quoted only with the agreeing-rates attached.
   - **2.8 [minor, fixable]** The Holm family is defined as the ten recall-level tests, and the sensitivity of that choice is not reported. If the twenty paired tests the paper prints are treated as one family (alpha/20 = 0.0025), only the smallest p (0.0001) survives, so the bundled contrast on the primary (0.0039) and the evidence-access contrast (0.0039) would fall to descriptive as well. A one-line sensitivity statement would bound the significance claims better than the current framing.
   - **2.9 [minor, fixable]** The Related Work says that Molinelli et al.'s contamination threat is carried "here" by §6. §6 consists of Yield, Pool, Materials, Design, Backbone, Counting and Instrument -- and contains no contamination paragraph. For an LLM pipeline whose inputs are the public documentation and issue trackers of widely used systems, dropping the one threat the paper itself calls first-order is a coherence gap between §6 and §7, not merely a missing citation.
   - **2.10 [minor, fixable]** The abstract's "locates the error budget in the one refuting clause its protocol does not guard" is broader than the measurement. The census counts incorrect closures to False-Positive (30, of which the unguarded clause supplies 24) and does not evaluate the confirmation side, where Table 4 records 11 incorrect closures to Confirmed (B 5, A 4, D 2), or the 69 catch-all judgments' correctness (45 bugs / 24 FPs, unscored). Either narrow the phrase or report the confirmation-side error mass.

3. **Perspective** — Adequate
   - **3.1** The lessons are explicit, quantified and mostly transferable (§5): audit what the oracle reads, not only what it concludes (43.3% of cited pairs unsupported); put the evidence guard where the error mass is (24 of 50 closures wrong); price the deferral channel and the contrast, not just the level (nine under the convention, three under hand-pricing); check the dispatch before re-architecting the judge (a one-line schema repair moved five of the headline nine bugs); and self-audit the stage against its own printed rules (22 forward departures, 17 in the forbidden direction, 10 of them on real bugs). For practitioners building LLM-judge pipelines these are concrete and worth having.
   - **3.2 [minor, unfixable]** The central prescriptive lesson does not extend beyond the case, and no revision of this data can change that: because the pattern reverses on the second backbone, the paper's own conclusion is that the rule is "advice about where to look rather than a property of the protocol." The paper's most quotable lesson is therefore also its least portable.
   - **3.3 [minor, fixable]** The paper measures the distillation failure and repairs it in-house (version-pinned rebuild, full re-anchoring, the version-drift and conceptual-only mechanisms) but does not convert the repair into guidance: the prescription to readers is "measure your own numbers", not "pin the version, re-anchor, and check for expectation-framed sentences". A short paragraph on what the rebuild actually changed beyond the expectation-framing check would make the first lesson actionable rather than diagnostic.

4. **Verifiability** — Excellent
   - **4.1** The artifact is declared with a specific anonymous URL and an inventory that maps to the paper's claims: the pool, the frozen per-run verdicts of all twelve configurations, the packages the study read, the dispatch texts and the two judging prompts, the pair-audit verdicts, the adjudication worksheet and blind passes, and the five named analysis scripts under rq2/analyses/ (§4.1, Data Availability). Re-judged cases ship beside the pre-repair state so either pool can be reconstructed from the package alone. I judged this from the text and did not fetch the URL, per review protocol; if the link is live, this is about as checkable as an experience paper of this kind gets.
   - **4.2 [minor, fixable]** The audit's own input does not ship: the packages "as the pipeline produced them" -- the material the 18/58/58 split is *about* -- are archived separately and excluded from the package (Data Availability). A reader can inspect the shipped per-pair verdicts but cannot re-derive the split, and the same is true of the twelve case-level assertions. The exclusion is disclosed; shipping the pre-rebuild generation would close it.
   - **4.3 [minor, unfixable]** Both backbones are unpinned serving aliases (§4.1), so the judgments cannot be regenerated and verification must rest entirely on the frozen artifacts. This inheres in the setting and is disclosed, but it means "replicate" in the strict sense is unavailable here; "recheck" is.
   - **4.4 [minor, fixable]** Two procedural gaps in otherwise complete reporting: the case-level audit covers "12 main assertions" of 81 cases with no stated selection rule, so a reader cannot tell whether those twelve are all objects of that kind or a subset; and three printed analyses (the catch-all composition, the expectation-framing check, and the C row's evidence classification) are not scripted (§4.1, §6). The underlying cells ship, so both remain derivable in principle.

5. **Presentation** — Adequate
   - **5.1** The structure works: each results section opens with its question in italics ("How much of what the confirmation stage reads is actually in the documentation?"), the abstract is tri-partite and mirrors the contributions, the a/b discordance convention is declared before it is used, and each headline is scoped where it is made. Figure 1 and the four tables are referenced and load-bearing rather than decorative.
   - **5.2 [minor, fixable]** The results live almost entirely in prose. §4.4 in particular compresses a dozen paired contrasts into long sentences ("the schema-line repair alone moves recall 30 to 35 ... adding the routing rule on top moves recall 35 to 39 ... and, forced, the other way (29 to 27, 3/1)"). A per-arm table (arm x backbone, convention/forced/joint, suppression, net) would carry most of that section and let a reader check the "readings reorder the arms" claim directly.
   - **5.3 [minor, fixable]** The four-perspective contrast never names its arms in the results sentence: "the same two are 51 vs. 48 ... and 51 vs. 35", and "41 vs. 30" with "-11 true bugs". The printed order there (rule-bearing flat judge first) differs from the deployed-first order used elsewhere in §4.4 (e.g., "the deployed stage against the flat judge is 48 vs 34"), so the direction of the second-backbone result is recoverable only from the sign in the prose. Name both arms in each contrast.
   - **5.4 [minor, fixable]** Spelling is inconsistent in a way that touches a technical term: "behavioural elegance" in §3.5 versus "behavioral elegance" in §4.5's legend, alongside mixed -our/-or forms elsewhere ("behaviour" and "generalise" against "behavior"). Pick one convention.
   - **5.5 [minor, fixable]** "the middle of the three clauses that assign False-Positive (19 judgments, against cognition's 16 and contract refutation's 50)" reads first as firing order, but the legend's firing order is A, B, D, C; the intended sense is median by count. Say "the median-closing clause" or reorder the comparison.

### Questions for Authors

- **Q1:** Do the counterfactual's two printed counts come from different objects -- i.e., does a sixteenth case flip when the clause fires in only one of its three runs? -- [background: 2.5; if the counts reconcile, or if the abstract's "nine interceptions" changes, 2.5 resolves either way; as printed, the abstract carries a number the paper's own arithmetic does not support.]
- **Q2:** Would re-dispatching the second backbone's deployed stage with the corrected perspective vocabulary (one schema line, as the primary's flat+schema arm shows) settle whether the non-replication in the census is substantive or an artifact of the doubled definition? -- [background: 2.4; a diagnosis either way would raise the item -- if the reversal is real, the lesson is backbone-dependent and should be stated as such; if it is an instrument effect, the census's bound lifts. The item stays major only while the cause is open.]
- **Q3:** What happens to the four surviving contrasts if the Holm family is defined over all twenty paired tests printed (alpha/20 = 0.0025)? -- [background: 2.8; if only the smallest survives, §4.1 and §6 should say so and the reading of "the four smallest significant" changes; reporting the sensitivity either way improves the item.]
- **Q4:** How much error mass lies outside the census's view -- the 11 incorrect closures to Confirmed in Table 4 and the 69 catch-all judgments -- and is the unguarded clause also the dominant source there? -- [background: 2.10; if the clause also dominates false confirmations, the abstract's "error budget" phrasing becomes exact; if not, it needs narrowing.]
- **Q5:** Priced by the deployment's own net metric, which the paper uses for the evidence-access contrast, routing contract refutation moves 39 - 9 = 30 to 46 - 18 = 28 under the convention. Should that number be disclosed beside "seven true bugs for nine interceptions"? -- [background: 2.5; if the authors show the net metric is unchanged or inapplicable here, the census's prescription is less qualified; if it drops, the prescription's framing should carry it.]


---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Importance & Scope | Excellent | Excellent | Excellent | **Excellent** |
| Insights & Evidence | Adequate | Excellent | Adequate | **Adequate** |
| Perspective | Adequate | Excellent | Adequate | **Adequate** |
| Verifiability | Excellent | Excellent | Excellent | **Excellent** |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Accept** | **Accept** | **Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three recommendations land on Accept, so the unanimous shortcut decides outright. Importance & Scope and Verifiability are consensus Excellent for the third consecutive round. Perspective falls from consensus Excellent to Adequate — R2 still rates it Excellent, R1 and R3 move to Adequate — and this is the round's one regression in the instrument's reading; both of the reviewers who moved say why in the same terms: the census's central prescription is a replay over frozen values whose gain exists only under one counting convention, so the paper's most quotable lesson is also its least portable, and the paper's own non-replication on the second backbone bounds it further. That is not a new finding — it is the item the previous two rounds also carried — but two reviewers have now decided it belongs in the tier rather than in the prose.

The round's most consequential item belongs to the author, not to the paper. R2 checked the artifact against the text and found that the second reader's agreement figure did not match the shipped sample; the cause was a join on a non-unique key (six pair records carry the placeholder `<noid>`), which collapsed those rows and had published **31/36 with κ = 0.78**. Joined by row order the true figures are **30/36 and κ = 0.75**, with all twelve sampled SWAP pairs — not fifteen — called SWAP again. The paper, the artifact README and the shipped script are corrected, and the script now asserts the join order rather than trusting it. This is the fourth round in which a number published by the author rather than by a reviewer was found unusable on inspection, and it is the second in which the defect was inside material added to *answer* a reviewer.

Insights & Evidence stays at Adequate on a 2–1 split for the same reason as last round, with one item sharpened: R3 showed that the counterfactual's two counts do not reconcile as printed (seven bugs plus nine released negatives implies sixteen flipped cases against a stated fifteen), and the author's recount confirms the diagnosis with a detail the reviewer could not reach — the fifteen contain seven bugs and eight negatives, so the ninth released case is one the clause closes in a single run. The reconciliation is in the paper now. R2's dissent upward rests on the cross-tab, the invariance checks and the second reader, which it weighed as sufficient for the claim the paper actually makes.

### Priority Revisions
Ranked by impact. Every `[major, fixable]` item this round is one the author can close with text or with a recount; none requires a new experiment.

1. **Re-verify every published number that a reviewer did not independently recompute.** R2's item 4.5 caught the second reader's figure; the recount found 30/36 and κ = 0.75 against a published 31/36 and 0.78, and a SWAP count of 12 where the paper printed 15. The same class of defect produced the counterfactual's irreconcilable counts (R3's 2.5), the "Sixteen paired tests" of the previous round, and the page over-run that the corrected page meter exposed. The pattern is consistent across four rounds: **the numbers this paper gets wrong are the ones it derives itself and no reviewer recomputes.** The remedy that has worked each time is mechanical — recompute the claim from the shipped data before printing it — and the second reader's case shows it must also be applied to numbers added in response to a review.

2. **Name the selection rival in the census, and rest it on error mass.** R2 rates this `[minor, fixable]` at 2.5 and it is the sharpest new methodological point in the round: contract refutation is tried before the by-design perspective in the printed sequence, so it fires on the largest and most heterogeneous set (50 closures) while C = Refuted closes only the 19 that A, B and D all left open, and the observed accuracy gap (0.52 against 0.89) is consistent both with the guard doing the work and with C's small residual set being easier. The paper kills the pair-audit rival and not this one. R2 also supplies the fix: the prescription survives either way because it rests on error mass — 50 closures at 48% wrong is 24 errors against 19 at 11% is 2 — so naming the rival and resting the claim there costs a sentence and removes the alternative reading.

3. **Say how the load-bearing column is identified.** R1 rates this `[major, fixable]` at 2.8: A and B share all three values, so the "identified by their content" claim does not hold for the column the entire 50-closure/24-wrong/80% result attaches to. The author's answer, now in the paper, is that the dispatch names A and B the same way in both of its definitions and names only C and D twice with the definitions exchanged, so A and B are what their field names say and the content test is needed only for the pair that is defined twice. The abstract and §1 have been narrowed to match; R1's Q1 asked exactly this question and it is now answered in the text.

4. **Reconcile the counterfactual's counts in one place.** R3 rates this `[major, fixable]` at 2.5; the recount above resolves it, and the paper now states that the seven come from the fifteen, that eight of the fifteen are negatives, and that the ninth released case is closed by the clause in a single run. The word "interceptions" — which the paper used in two opposite senses, meaning "blocked" at one site and "released" at four — is replaced by "released" throughout, which is also what R2 asked for in the previous round.

5. **Take the per-arm table, or state the page arithmetic that forbids it.** R2 at 5.2 and R3 at 5.2 independently ask for one table carrying each arm's convention recall, forced recall and suppression. The author's reason for declining is a measurement and should be recorded rather than left implicit: the paper stands at 17.81 of the 18 counted pages, so a twelve-row table must displace equivalent prose. This is the third consecutive round in which all three reviewers have asked for it.

6. **Bring the artifact's account of the paper's own material into line.** R2's 4.4 found the README attributing the first leak repair to `run_fullc*` where the paper's §4.1 lists the contract core; the artifact settles it in the paper's favour — `verdicts_rejudge_cog.jsonl` ships in `run1-3` and not in `run_fullc*` — and the README is corrected. Two further artifact-vs-text items R2 raised are fixed the same way: the README's join instruction, and its list of what the paper does and does not script.
