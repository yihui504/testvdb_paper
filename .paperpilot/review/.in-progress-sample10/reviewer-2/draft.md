# Reviewer 2 — Area Specialist (empirical evaluation of LLM-based SE tools)

**Object under review:** `c:\Users\11428\Desktop\testvdb_paper\TestVDB-v10.tex` (LaTeX submission;
compiled `TestVDB-v10.pdf`, 20 pages). Rebuilt from source with `pdflatex` (three passes): 0 errors,
0 undefined references, 0 overfull boxes.
**Evidence used:** `.paperpilot/phase2-rerun/arms/rq2_3run/` (frozen verdicts, `gt_81.json`) and the
replication package `c:\Users\11428\Desktop\TestVDB_artifact` at git HEAD `432459e` (working tree clean).
Everything below was obtained by running code; raw outputs are under `reviewer-2/verification/`.

---

## Overall Recommendation

**Weak Accept** — chair's verdict **CONDITIONAL**.

This is the cleanest state this submission has been in across the rounds I have seen. Every
load-bearing number recomputes: I re-derived the per-arm confusion matrices, both readings of every
contrast, both levels of every paired test, the clause census on both backbones, both replays, the
re-set intersections, the pair audit, the submission ledger's row census, and the crash-oracle
baseline's log counts from raw artifacts with my own code, and everything the paper prints matched.
The paper also keeps the two properties that earned it credit in earlier rounds — it reports four
defects in its own dispatches and prices its counting convention against its own interest at two
places (§4.4, §4.5).

What holds it at Weak Accept is not a wrong number. It is that the paper's central claim (§4.5) is
measured on one backbone, reverses on the second (§4.5 itself says so), its prescription is a no-op
under the forced reading, and the one contrast the title-level story rests on is priced by hand at a
floor the authors call "suggested, not established" (§4.4). A measurement paper whose headline
finding lives under a counting convention the paper argues is inflated is a real but conditional
contribution.

The four conditions I would attach to the verdict (W1–W4 below, plus the three wording fixes W5–W7
listed in Core Weaknesses) are all textual, and none touches a result. The first two are, however,
exactly the class of defect that sank earlier rounds — a claim *about the package* that the package
does not support — so they must be fixed rather than noted:

1. §4.1, last sentence of the arm-edit paragraph, claims "English renderings of the two judging
   prompts ... ship verbatim in the artifact". **They do not ship.** No file with "prompt" in its
   name exists anywhere in the package, and an exhaustive case-insensitive search for the English
   protocol vocabulary (`behavioral elegance`, `Weak-Refuted`, `objective constraints`,
   `Supports-Not-Defect`) finds nothing outside `pipeline/agents/chain-auditor.md` (the deployed
   pipeline's agent definition, a different object). The English renderings existed only in the
   removed appendix. Either ship them or delete the clause. (W1)
2. §4.4 prints two routed-count denominators — "The control has 22 decisive routed cases, of which
   9 were never ruled, one of them a true bug; the flat judge has 8, of which 2 were never ruled,
   none a true bug" — that do not reproduce under any reading I tried. The *sub*-claims reproduce
   exactly (the control's 9 never-ruled cases contain exactly one true bug, `milvus_024`; the flat
   judge's 2 never-ruled contain none), but the totals come out at 25 and 11 under the natural
   reading (a case routed in ≥1 of 3 runs and convention-confirmed) and 21 and 4 under a ≥2-of-3
   reading. (W2)
3. `\footnotesize` in the `tab:oracles` and `tab:configs` floats has lost its `\f`: byte 11267
   (line 166) and byte 33598 (line 466) of the `.tex` each hold a form feed (0x0C) followed by
   `ootnotesize`. The compiled PDF consequently typesets the literal string **"ootnotesize"** in
   Table 1 (p. 4) and Table 2 (p. 9), and those two tables render at `\normalsize` rather than
   `\footnotesize`. (W3)
4. §4.5's catch-all sentence describes the 32 non-source-vocabulary catch-all judgments as those
   "whose D cell the rule does define". All 32 are `NO_SIGNAL`, for which the appended aggregation
   contains no clause either — the sentence is defensible only as a claim about *vocabularies*, not
   about clauses, and as written it will read to a checker as the same kind of claim the paper
   makes about the other 37. (W4)

## Summary

The paper reports three artefacts. (i) A mining campaign: 51 of 81 adjudicated submissions across
Milvus, Qdrant and Weaviate confirmed by maintainers, 23 fixed through merged PRs, drawn from a
132-row ledger covering 19 versions; the paper states at every appearance that this is a record of
submissions and adjudication, not a per-run detection rate, and that the detection-ability
experiment was voided in full. (ii) An audit of the (constraint, cited-page) pairs the confirmation
stage's packages carry: 18 of 134 supported as cited, 58 re-anchored from a source file or landing
page, 58 with no support on the cited page; from which two leak repairs followed. (iii) A clause-level
census of the deployed stage's 243 judgments: contract refutation carries no evidence requirement,
closes 50 judgments, and 24 of them are maintainer-confirmed bugs; the verbatim-guarded by-design
clause closes 19 and is right 17 times; 80% of the stage's incorrect closures to False-Positive come
from the unguarded clause; routing that clause instead of closing on it recovers seven true bugs for
nine interceptions under the deployment's convention and nothing under the forced reading.

Sections: §1 Introduction, §2 Preliminaries, §3 Approach (the protocol the census counts over), §4
Evaluation (§4.1 methodology and the twelve configurations, §4.2 mining yield, §4.3 the pair audit,
§4.4 what the confirmation stage buys, §4.5 the clause census, §4.6 the crash-oracle baseline), §5
Discussion, §6 Threats to Validity, §7 Related Work, §8 Conclusion, then Data Availability and
References.

## Core Strengths

**S1 — The load-bearing measurements reproduce, and they reproduce on a package frozen at a single
commit that a reviewer can run in place.** All five scripts named in §4.1 execute from the artifact
root and print the paper's current numbers; I re-derived every one of them independently from
`rq2/verdicts/*/verdicts_batch*.jsonl` plus the re-judge overrides, using only the conventions the
paper states in text, and got identical results (see the method note). This is not a small thing for
this line of work: four earlier rounds found a reviewer-caught numeric error each time, and this
round I could not produce one on any load-bearing figure.

**S2 — The self-audit of the instrument is real, verifiable, and priced against the authors'
interest.** §4.1's four dispatch defects are checkable in the shipped texts and all four check out:
the binary schema line appears in **exactly eight** of the twelve arm dispatches while their own text
mandates three values (the contract core is legitimately binary — "HUMAN_REVIEW" appears zero times
in its dispatch — which is why eight is the right count and my first count of nine was wrong); the
two aggregation blocks with opposite last-step defaults are both printed in the deployed dispatch
(the earlier one ends "证据不足一律 FALSE_POSITIVE", the appended one ends "其余 → HUMAN_REVIEW");
the two complete perspective definitions with C and D exchanged are both printed; and the output
schema declares the source vocabulary for the perspective the second block calls maintainer
cognition. The paper then reports that the second leak repair **does not move the two controls in
its favour** — suppression 0.467→0.400 and 0.933→0.900, forced recall 30→31 with the arm's
true-positive set unchanged — and that without the repair the deployed configuration would read
better (41/51 and 41+6) than the 39/51 and 39+9 it reports. I recomputed that ledger verdict by
verdict: of the nineteen rewritten verdicts, fifteen move toward confirmation, four move between
Confirmed and Human-Review, and none moves away. Reporting your own repair as having made your
headline worse is the behaviour a measurement paper owes its readers.

**S3 — The counting convention is priced rather than asserted, at both places the paper says it
should be.** §4.1 commits to "we report the forced-verdict reading beside it for every contrast, and
we price the convention at two places: the arms' levels, and the headline contrast itself." That
commitment is kept. Every headline contrast is printed at both levels and the paper refuses to
privilege either ("The two levels disagree for the rule step, and we privilege neither"). The census
counterfactual is explicitly a replay, explicitly a no-op under the forced reading, and the paper
draws the right conclusion from that: "the gain it shows is a property of the convention rather than
of the stage's decisions." The independent adjudicator's disagreement (κ = −0.01, 0.08, 0.11) is
reported as a bound rather than as a measurement, and "Two of the three independent passes land at
the forced floor" is stated in §4.1 rather than buried.

**S4 — §4.5's identification of the C=Refuted cells by their content does what the paper claims, and
the departure it exposes is disclosed in the right place.** I listed all nineteen judgments the
census closes by C=Refuted with their `d_evidence` and rationales: fifteen cite an in-source comment
or docstring, two (`milvus_026`, runs 1 and 2) name the server's own name-validation rule and its
error message, and two (`milvus_011` and `milvus_012`, each in run 3) rest on code structure — a
default expression that maps an empty filter to `trueLiteral`, and a three-level `dbName` fallback
chain. The paper's distribution is exactly right. So is the consequence it draws: the requirement the
clause enforces is not applied uniformly, and the compliance recount does not catch it because that
recount checks the *verdict* against the clause the recorded perspective values select, taking those
values as given. I verified that reading of the script: a cell wrongly recorded as `C=REFUTED` is
invisible to it. The paper states this in §4.5 as a departure of the judge that recorded the cells
rather than as a flaw in the census, which is the honest placement.

**S5 — Two contrasts are reported in the direction that hurts, and both are load-bearing for the
Conclusion.** The four-perspective contrast is null on the primary backbone (39 vs. 39, 4/4,
p = 1.0) and **−11 true bugs on the second** (41 vs. 30, 12/1, p = 0.0034), and §4.4 says so in bold.
The evidence-access contrast shows the deployed stage's most trusted evidence channel is not
separable from having no source: net +0 with CI [−8, +8], F₁ +0.033 with CI [−0.044, +0.115]. §4.4
calls that "the price of the falsification anchor, stated as a tie rather than as a defeat", which is
exactly what the intervals support.

## Core Weaknesses

**W1 [minor, fixable] — §4.1 claims the artifact ships English renderings of the two judging prompts;
the artifact does not.** The sentence is the last one of the arm-edit paragraph: "All dispatch texts,
and English renderings of the two judging prompts, ship verbatim in the artifact." The dispatch
texts do ship (`rq2/verdicts/run_*/batch*_dispatch.txt`, plus `rq2/verdicts/dispatch_template.md` and
`rq2/verdicts/dispatch_fullstage_template.md`), and they are verbatim. The English renderings do not:
they lived in the removed appendix (`\section{Judging Prompts}`, removed in commit `0a78d2a`), and
nothing in the package replaces them. This matters more than a typo because of *why* an expert wants
them — see Q2 — and because the paper's own §4.1 is where a reader is told where to look. Fix by
either shipping the two renderings or by narrowing the sentence to "All dispatch texts ship verbatim
in the artifact; the prompts the judges actually read are those dispatch files." The second option
costs nothing: the dispatch files are authoritative and, as implemented, they do contain a full
English-free statement of every rule the paper attributes to each arm.

**W2 [minor, fixable] — the two routed-count denominators in §4.4 do not reproduce.** §4.4 reads:
"The control has 22 decisive routed cases, of which 9 were never ruled, one of them a true bug; the
flat judge has 8, of which 2 were never ruled, none a true bug." Reconstructed from the frozen
verdicts against the shipped worksheet `rq2/analyses/pricing/HR17_adjudication_worksheet.md` (22 ruled
cases: 9 CONFIRM, 2 RETURN, 6 REJECT in the 17-case sheet, plus 5 in the two addenda):
"routed in ≥1 of 3 runs and convention-confirmed" gives the control **25** decisive cases (unruled 9)
and the flat judge **11** (unruled 2); "routed in ≥2 of 3 runs" gives **21** (unruled 9) and **4**
(unruled 1). No reading I tried produces 22 and 8, and both printed totals sit exactly 3 below the
first reading — a coincidence, or a definition I could not recover. The two *load-bearing* claims in
the same sentence are exact: of the control's 9 never-ruled decisive cases exactly one is a true bug
(`milvus_024`), and the flat judge's 2 never-ruled contain none. The paper flags this quantity as one
of the three "printed but not yet scripted" in §4.1 and §6, which is the right disclosure, but a
denominator a reader cannot reconstruct is worse than a price they cannot reconstruct. Either script
the contrast pricing (the material is all shipped; I reproduced the three joint levels 33/32/29 from
the worksheet in about thirty lines) or correct the two totals.

**W3 [minor, fixable] — two tables typeset the literal word "ootnotesize".** `\footnotesize` in the
`tab:oracles` and `tab:configs` floats has been eaten by a form-feed character: the `.tex` holds
`\r\n\x0cootnotesize` at lines 166 and 466, so LaTeX sets the text `ootnotesize` after the caption
and sets the table body at normal size. The PDF renders it on page 4 ("...residual. ootnotesize
Candidate oracle ...") and page 9 ("...differ. ootnotesize# configuration ..."). This is a
submission-visible typographic defect in a paper that is otherwise faultless on the page (0 overfull
boxes, 0 errors, 0 undefined references in my rebuild). It is exactly the kind of thing a
desk-checker sees first.

**W4 [minor, fixable] — §4.5's catch-all wording conflates vocabulary with clause.** §4.5 reports
that the catch-all routes 69 judgments, that 37 (54%) carry the source vocabulary in their D cell —
"a vocabulary the operative rule has no clause for" — and then says: "On the 32 catch-all judgments
whose D cell the rule does define, 17 rest on true bugs (53.1%) against a pool base rate of 63.0%."
The 32 are all `NO_SIGNAL` (composition of the 69: `NO_SIGNAL` 32, `by_design_in_source` 11,
`validation_present` 10, `validation_absent` 9, `not_found` 7). `NO_SIGNAL` *is* a defined value of
the cognition perspective in the dispatch, but the appended aggregation has no clause for it either,
so "the rule does define" is true of the vocabulary and false of the clause. The substantive content
— 17/32 = 53.1% against a 63.0% base rate, about 1.2 standard errors, "we could not detect
enrichment" — is unaffected and I reproduce it exactly. Suggested fix: "on the 32 catch-all
judgments whose D cell uses the cognition vocabulary (all `NO_SIGNAL`, a value the perspective
defines but the aggregation has no clause for)".

**W5 [minor, fixable] — §8 is the one place the census finding travels without its scope.**
The paper is otherwise scrupulous about this, and I want to record that I checked it after being
ready to file it as a major weakness: the abstract carries the qualifier in the same sentence as the
claim ("locates the error budget in the one refuting clause its protocol does not guard---measured on
the primary backbone, where the perspectives are identified by their content, and not reproduced on
the second"), as does §1's third bullet, as does §4.5's opening, as does §5's "the error mass moved
on the second backbone ... the rule is advice about where to look rather than a property of the
protocol", and §6's Backbone paragraph states it a fourth time. The one exception is §8: "the clause
that closes the most judgments is the one the protocol guards least: contract refutation carries no
evidence requirement, closes 50 of 243 judgments and is wrong about half the time, while the guarded
by-design clause closes 19 and is right 17 times." Four words of scope there would close the loop in
the section a reader is most likely to quote. This is the first thing a hostile reviewer will pull
out of context, and it costs one clause to make it impossible.

**W6 [minor, fixable] — §1's contribution list claims more identification than §4.5 performs.** §1
item 3 says §4.5 "identifies the two refuting clauses by the evidence their cells carry." §4.5 does
this for C (the nineteen cells, read one by one) and identifies D by its vocabulary split. It does
not do either for A — the identification of A rests on the fact that all 243 A cells carry the
contract vocabulary (`CONFIRMED` 21 / `REFUTED` 50 / `NEUTRAL` 172), which the paper never reports,
even though the same uniformity holds for B and C (`B`: 80/17/146; `C`: 72 `CONFIRMED`, 71 `NEUTRAL`,
59 `WEAK_REFUTED`, 41 `REFUTED`) and would have made the "identified by content" claim much stronger
than the two examples it gives. Add one sentence reporting the per-perspective cell vocabularies, or
soften §1.

**W7 [minor, fixable] — §4.1 promises both levels "for every contrast"; three contrasts are printed
at the recall level only.** §4.1 states the statistics policy as: "Paired exact McNemar at both the
confirmed-set level (81 cases) and the recall level (51 true bugs); they disagree and **both are
reported for every contrast**, including the isolation steps." Ten of the sixteen printed
confirmed-set/recall pairs do keep that promise. The four-perspective contrast does not: §4.4 prints
39 vs. 39 on the primary backbone (4/4, p = 1.0, ±0.11) and −11 on the second (41 vs. 30, 12/1,
p = 0.0034), both at the recall level, and the confirmed-set counterpart of that same comparison —
which my recompute puts at 51 vs. 51 with discordant 9/6, p = 0.6072, i.e. *not* the 4/4 the paper
prints — appears nowhere; a grep of the `.tex` finds neither `9/6` nor `0.6072`. The same holds for
the two auxiliary perspective readings in the last sentence of that paragraph ("At the recall level
against the rule-free flat judge the perspectives are +3 ... and against the schema-corrected control
−2 ..."), whose confirmed-set counterparts are 33 vs. 30 at 6/4, p = 0.7539 and 33 vs. 35 at 2/5,
p = 0.4531. The omission is defensible on the merits — for the primary four-perspective contrast both
confirmed sets are 51, so the confirmed-set test is uninformative — but it is exactly the asymmetry
§4.1 says it will not have, and it is the sentence a reader will use to decide whether the paper
reports adverse readings symmetrically. Either print the three confirmed-set numbers (they are in the
shipped script) or add "at the recall level" to the policy sentence.

## Detailed Assessment

### 1. Importance & Scope — Good

The residual the paper works in is real and well-argued in §2: the one dedicated VDBMS fuzzer is
crash-oracle by construction, the empirical bug study puts the dominant share of VDBMS defects in
functional failures, and the oracle families that read prose read it at field, parameter or method
granularity from tagged sources. The measurement question — how much of what a documentation-derived
oracle reads is actually in the documentation, and where inside the judge do the errors land — is the
right question for this line, and §4.3's answer (43.3% of cited pairs unsupported) is, to my
knowledge, the first quantitative measurement of it.

Docked for three scope facts the paper states but cannot escape. One pipeline, three vendors, one
domain, 81 cases for the census, one backbone for the claim. Twelve configurations added during the
study rather than pre-registered, three of which change more than one thing and one of which changes
five (§4.1, §6). The census's counterfactual is a replay over frozen values, so §4.5 correctly refuses
to draw the conclusion a design paper would want: "what cannot be computed from frozen data is
whether a judge re-adjudicating those refutations under a verbatim-evidence guard would reach the
same place." And the yield is explicitly not a detection rate — the RQ1 experiment was voided, 2.6%
of the ledger's adjudicated rows sit on versions that experiment covered, and the fix-PR
characterisation table is admittedly outside the shipped artifact (§4.2). A reader who came for a
detector leaves with a very well-measured oracle instead. That is a legitimate deliverable; it is
just narrower than the title suggests.

### 2. Insights & Evidence — Good

The two headline insights both survive recomputation, and both are the kind that change behaviour.

The pair audit (§4.3) is the paper's most transferable result: 18 of 134 supported as cited, 58
re-anchored, 58 unsupported, and the two mechanisms behind it (version drift in the augmentation
script, and constraints that exist as prose descriptions but not as documented values) are the two
failure modes any "distil a spec from docs, then judge against it" pipeline should expect. I
reproduced the three-way split exactly from `rq2/analyses/audit/pair_audit.py` and the raw verdict
records (34 source-file anchors → 19 DROP / 15 SWAP; 57 landing-page anchors → 43 SWAP / 14 DROP; 43
documentation-page anchors → 25 DROP / 18 SUPPORTED), and the case-level object separately (5
SUPPORTED, 3 UNSUPPORTED, 2 WEAK_EVIDENCE, 1 OVER_STRONG_REWRITE, 1 OVER_STRONG_WEAKEN). The paper
keeps the two objects apart and says so twice, including in the table caption ("The two 43.3% shares
are each of 134, not a combined 86.6%").

The census (§4.5) is the paper's claim. I reproduce the whole table: B=Confirmed 61 (56 right / 5
wrong, 0.92), A=Confirmed 21 (17/4, 0.81), D=Supports-Defect 7 (5/2, 0.71), A=Refuted 50 (26/24,
0.52), C=Refuted 19 (17/2, 0.89), D=Supports-Not-Defect 16 (12/4, 0.75), catch-all 69. The 24-of-50
is a strong, checkable fact, and the paper shows it is constructed to survive three objections: it
is the same under both printed aggregation rules because contract refutation assigns False-Positive
under both, no recorded primary-backbone cell carries the `A=Refuted` with `B=Confirmed` pair the
other rule would route (the second backbone records three, and I confirm both counts), and it is
computed on maintainer-confirmed labels rather than on the 30 negatives the authors adjudicated. All
three checks are correct. The counterfactual replay (39/51→46/51, 21/30→12/30) is a no-op forced,
which the paper says in the same paragraph.

What keeps this at Good rather than Excellent is that the two most decision-relevant facts about the
census cut its reach: the pattern reverses on the second backbone, and the prescription pays only
under a convention the paper itself prices at −11 points of recall on that backbone's four-perspective
arm. The paper is honest to a fault about both; a finding whose generalisation is bounded by the
authors is still bounded.

### 3. Perspective — Excellent

This is the dimension on which this submission has no peer among the papers I have reviewed this
year. The register is correct for what it measures: §4.3 explicitly refuses to generalise its rates
("we are not claiming these rates as properties of LLM distillation in general — they are this
distiller on these three vendors' documentation, classified by a single reader without a second
coder"), and §4.1 pre-empts the generalisation a hostile reader would try ("they are high enough that
the next pipeline in this line should measure its own numbers before attributing a confirmation rate
to its judge").

The self-reporting goes past disclosure into pricing. §4.1 reports the second leak repair's effect on
the controls and states that it does not help them. §4.5 reports that the cleaned pool is what makes
"by-design is the middle of the three" true at all, and that the load-bearing 24 is invariant either
way. §4.5's last paragraph reports that the judge departs from the appended rule in 22 forward
judgments, then immediately supplies the caveat that *removes the sting*: "the dispatch prints an
earlier rule whose last step commands exactly those closures, so they are deviations from the appended
rule and compliance with the earlier one." §4.6 volunteers that 152 lines across 119 of the baseline's
own logs look like anomaly reports and are not. §6 lists the four dispatch defects as an instrument
threat rather than as a discussion point, and notes that none was found by the authors' own audit.

One insight is genuinely new to me and is the paper's best sentence: "the organization changes *which*
cases are decided, not how many" — the forced true-bug sets of the two configurations intersect in 22
of 27 and 23 of 26, which I verified exactly, while the counts are equal. That is a much more useful
statement about multi-perspective LLM judges than a recall delta, and it reproduces Ma et al.'s
bias-amplification finding in a different currency.

### 4. Verifiability — Good (high end; one fix away from Excellent)

I ran all five scripts named in §4.1 in place from the artifact root. They execute, they read only
`rq2/`, and they print the paper's current numbers. I then re-derived every one of those numbers from
the raw JSONL with independent code, and separately verified: the submission ledger's row census
(132 three-system rows = 81 adjudicated + 51 unadjudicated, of which exactly 2 are the authors' own
withdrawn PRs, `milvus_47785` and `milvus_51809`; 19 distinct versions, 16 among the 81, 15 among the
51; per-vendor 43/28/10 split as printed); the two leak repairs (the 81 shipped packs contain zero
occurrences of `developer_cognition`, `by_design_patterns`, `blindspot_indicators`,
`developer_quote`, `recurring_patterns`; the pre-repair verdicts ship beside the re-judged ones); the
re-judge ledger (19 rewritten verdicts, 15 toward / 4 between / 0 away; controls' true-positive sets
unchanged at 48 and 33, false-positive counts +2 and +1); the crash-oracle baseline from its own logs
(205 per-template logs, 1,127 completed mutation stages, 11,629 response-status lines, zero 5xx, 152
anomaly lines in 119 logs all reporting exactly three, 50.75 minutes wall time, and the master log a
verbatim 2× echo); the pre-repair census (47 and 20) and the deployed configuration's counterfactual
(41/51 with 41+6); `milvus_001`'s routing (credited by eleven of twelve configurations, only the
contract core never); the three-way verdict splits (3 of 81) and the 37/51 alternative-reduction
figure; and the two forced true-bug set intersections. All matched.

What earns the tier is one thing beyond that: the three quantities the paper says are "printed but not
scripted" are, for two of them, still recomputable from shipped material. I reconstructed the
hand-adjudicated joint prices for all three arms from `rq2/analyses/pricing/HR17_adjudication_worksheet.md`
plus the frozen verdicts — forced true positives (27 / 27 / 25) plus the routed true bugs the
worksheet's CONFIRM rulings add that were not already forced-confirmed (6 / 5 / 4) — and got **33,
32, 29**, exactly the printed values, hence the printed +3 and +4. The catch-all composition
(37 source-vocabulary / 28 true bugs; 32 cognition-vocabulary / 17 true bugs against a 63.0% base
rate) I reproduced too.

It is not Excellent because two checkable statements about the package do not hold as shipped — the
English renderings that §4.1 says travel with the dispatch texts do not exist anywhere in the package,
and the two routed-count denominators in §4.4 do not come out of the shipped worksheet on any reading
I could construct — and because the third unscripted quantity (the expectation-framing check: "zero of
81 packages contain a sentence framed as an expectation") ships with no intermediate list, so the "19
hits for such phrasing" cannot be inspected. My own independent scan of the 81 packs finds no
expectation-framed sentence in either English or Chinese, which is consistent with the claim, but
consistency is not verification. Correcting W1 and W2, and shipping the expectation-framing hit list,
would move this to Excellent with no change to any result.

### 5. Presentation — Good

The paper is dense and disciplined about its readings: every rate is labelled convention or forced,
the interval is attached to the level it belongs to, discordant pairs are printed as `a/b` with the
convention for *which* arm is `a` stated once and used consistently (§4.1), and the tables are each
referenced from the text. The clause legend and the census table are grouped by outcome. The
five-thing decomposition of the four-perspective contrast is listed before the label is used. I
checked the `a/b` convention on six contrasts in both directions — the printed order is consistent
throughout.

Docked for W3 (a literal `ootnotesize` and two tables at the wrong size in the compiled PDF), W4 (a
sentence whose wording will be checked and found wanting), W6 (an §1 claim stronger than what §4.5
shows), and for one structural cost of the 18-page limit: §4.5 in particular now asks the reader to
hold four things at once (the primary census, the second backbone's non-reproduction, the C/D
ambiguity, and the vocabulary split) before it states the claim, and the claim arrives in the last
third of the paragraph. The material is all necessary; a two-sentence "what we claim / what we do not"
box before the clause legend would pay for itself.


## Questions for Authors

(The five questions below are numbered Q1-Q5 *to the authors*; they are separate from the
Q1-Q6 the round asks me to answer, which follow in the next section.)


**Q1 (to the authors). The expectation-framing check has no material in the package.** §4.3 reports "zero of 81
packages contain a sentence framed as an expectation---the 19 hits for such phrasing were each
inspected and are all verbatim server responses, quoted as observations", and §4.1/§6 list this as
one of the three quantities printed but not scripted. My own scan of the 81 packs finds no
expectation-framed sentence in English or Chinese, so I have no reason to doubt the zero; but the
"19 hits" cannot be inspected, and a reader who wants to know what phrasing produced them cannot
find out. *Intended effect:* shipping either the pattern list or the 19 hits (they are cheap) would
let a reader check the one leak-adjacent negative result in §4.3 that has no other support, and would
retire one of the three "printed but not scripted" items.

**Q2 (to the authors). How is a "decisive routed case" defined in §4.4?** The sentence "The control has 22 decisive
routed cases, of which 9 were never ruled ... the flat judge has 8, of which 2 were never ruled"
does not reproduce: ≥1-of-3-run routing plus convention confirmation gives 25 and 11; ≥2-of-3 gives
21 and 4. The never-ruled sub-counts are exact under the first reading (9 with one true bug; 2 with
none). *Intended effect:* telling a reader the definition would make the pricing of the routing
change auditable end to end; as it stands the last step of §4.4 is the only place in the paper where
I could not close the loop from shipped material. *(I did close the loop on the prices themselves —
33/32/29 reproduce from the worksheet — so this is about the denominators, not the result.)*

**Q3 (to the authors). §4.6's zero is a bound on the released configuration; is the released configuration's
mutation vocabulary the right target?** The paper already protects itself here ("the zero is a bound
on the released configuration's reach into the silent majority rather than on the crash-oracle
family"), and I reproduced 205 templates, 1,127 completed mutation stages, 11,629 status lines, zero
5xx, and 152 anomaly-looking lines in 119 logs that all report exactly three. *Intended effect:* a
sentence saying whether the baseline was re-run with a widened vocabulary, or why not, would make the
"hand-guided probe submits a value that vocabulary cannot reach" claim in §4.6 concretely checkable
(that probe ships but its output was not retained, so it is currently an assertion with no evidence
at all).

**Q4 (to the authors). Does the flat-judge arm really isolate organization, given the shared rules do most of the
work?** §4.1 says the flat judge "keeps the protocol's red lines ... and the objective-constraint
principle stated with four of its seven classes as examples rather than the full enumeration". I
verified the four-vs-seven split in the shipped dispatches. *Intended effect:* stating in the body
(not only in the artifact) that the shared rules are the ones that most affect recall would prepare
the reader for the null on the primary backbone instead of leaving it to look like a failed
manipulation.

**Q5 (to the authors). What is the intended reading of the `A=Refuted` cell's evidence?** §1 says §4.5 "identifies
the two refuting clauses by the evidence their cells carry", but §4.5 performs the content reading
only for C (all nineteen cells) and the vocabulary reading for D. A cheap strengthening: report that
all 243 A cells carry the contract vocabulary (21 CONFIRMED / 50 REFUTED / 172 NEUTRAL), and likewise
for B and C, which I verified is the case. *Intended effect:* it converts "the letters are identified
by content on the primary backbone" from a claim illustrated by two examples into a claim established
for all four perspectives, which is what the census's scope argument needs.

## Answers to Q1–Q6

### Q1 · The package, again, and on the submission

**Do the five analysis scripts run in place and print the paper's current numbers?** Yes, all five,
unchanged, from the artifact root at HEAD `432459e`, reading only `rq2/`. Full transcripts in
`verification/artifact_scripts_raw.txt`.

- `recompute_paper_numbers.py` — twelve per-arm matrices, both readings, Wilson intervals, 15
  confirmed-set and 14 recall-level McNemar tests, routed queues, per-perspective votes. Prints
  full stage 39/51 convention / 27/51 forced / suppression 21/30, flat judge 30/51, flat+schema
  35/51, flat+aggregation 39/51, full-no-source 48/51 suppression 12/30, full-no-aggregation 33/51
  suppression 27/30; second backbone flat 27/51, flat+agg 41/51, full 30/51 — every one of which
  appears in §4.4, §4.5 or §8.
- `clause_tally.py` / `clause_tally.py second` — the two censuses, the rule-compliance split, both
  replays.
- `convention_pricing.py` — convention 39/51, forced floor 27/51, joint 33/51, and the three
  independent passes with raw agreement and κ.
- `bootstrap_net_f1.py` — net +0 [−8, +8], F₁ +0.033 [−0.044, +0.115], 20,000 resamples, seed
  `20260914`.
- `audit/pair_audit.py` — 18 SUPPORTED / 58 SWAP / 58 DROP of 134, and the case-level 5/3/2/1/1.

**Claim about the package (i): "All rates, the census on both backbones, both replays, the net and
F₁ intervals and the pair audit are recomputable from the artifact's five analysis scripts."**
**True.** I executed each script and then re-derived all of it from the raw JSONL with independent
code; nothing disagreed. I also verified the Holm arithmetic §4.1 performs by hand: the ten
recall-level p-values sorted are 0.0001, 0.0034, 0.0039, 0.0039, 0.0225, …, tested against
α/10 = 0.005, α/9 = 0.00556, α/8 = 0.00625, α/7 = 0.00714, α/6 = 0.00833 — the four smallest pass,
the fifth stops the procedure. Exactly as printed.

**Claim about the package (ii): "The joint prices, the catch-all composition and the expectation-
framing check are printed but not yet scripted, and the artifact's script-coverage note says so."**
**True as stated, with two shades of nuance.** The README's "Script coverage" paragraph names
precisely those three and adds the Holm-family correction, which the paper also computes by hand. The
nuance: `convention_pricing.py` *does* script the deployed stage's own joint price (33/51) and its
κs — what is unscripted is the pricing *of the contrast* (the control's 32 and the flat judge's 29,
hence +3). And the joint prices are nevertheless recomputable from shipped material: I reproduced
33/32/29 exactly from `analyses/pricing/HR17_adjudication_worksheet.md` plus the frozen verdicts
(forced true positives 27/27/25 plus the routed true bugs the worksheet's CONFIRM rulings add that
were not already forced-confirmed, 6/5/4). The catch-all composition I also reproduced (37
source-vocabulary of which 28 are true bugs; 32 cognition-vocabulary of which 17 are true bugs, 53.1%
against a 63.0% base rate). Only the expectation-framing check has no shipped material at all, so of
the three "printed but not scripted" items, two are in fact recomputable and one is not.

**So: is each claim true as shipped?** The recomputability claim is fully true. The
printed-but-not-scripted claim is true but under-describes what is in fact recoverable, and the one
item that is genuinely unverifiable is the smallest one.

### Q2 · The appendix was removed to meet the page limit

**Does the paper still let an expert judge the central comparison?** Largely yes, and better than I
expected — with one exception inside the paper and one about the package.

*What the paper tells you about the two arms.* §3.5 gives the full-stage protocol in prose: the five
evidence-chain sections, the four mechanical checks, the four perspectives (A contract; B objective
constraints with its seven classes and the `ef`/`nprobe` sentinel carve-out; C behavioural elegance
with the verbatim-intent requirement; D maintainer cognition), the three-valued verdict space, and
the aggregation order clause by clause, with the remark that "the clause that closes a judgment is
the first in this sequence that decides it". §4.1 then states what the flat judge is: "the full
stage's materials without the perspective vocabulary and the aggregation rule, and it keeps the
protocol's red lines---the verbatim-intent requirement for by-design refutation, and the objective-
constraint principle stated with four of its seven classes as examples rather than the full
enumeration". And the arm-edit paragraph (folded into §4.1 when the appendix was cut) states the
exact edit for each of the four control arms. So an expert can determine **what each arm was given
and which parts of the protocol each applies**, which is what the central comparison needs.

*I verified the arm-edit paragraph against the shipped dispatches by diffing them.* It is exactly
right, line for line: `run_flat1` → `run_flatschema1` changes only the material-list output path (a
consequence of where the run wrote) and the schema line `"CONFIRMED|FALSE_POSITIVE"` →
`"CONFIRMED|FALSE_POSITIVE|HUMAN_REVIEW"`; `run_flat1` → `run_flatagg1` changes that same schema line,
the one sentence declaring that no aggregation rule applies, and appends the routing clause;
`run_full1` → `run_fullnosrc1` drops `source=` from all 14 per-case material lines and adds a nine-
line configuration note (`source=` occurrences: 14 → 0); `run_full1` → `run_noscopic1` excises both
aggregation blocks and adds a "no fixed aggregation rule" note. This is the strongest verification of
a paper-vs-package claim I have been able to do on this submission.

*What the paper no longer tells you.* The literal prompt text: the exact enumeration of B's seven
classes as dispatched, the exact wording of the red-line clauses, and — most relevantly to §4.1's
disclosure — the two aggregation blocks and the two C/D-exchanged perspective definitions whose
coexistence is the paper's defects 2 and 3. A reader who wants to see the contradiction the paper
reports must open the dispatches.

*Where to open it, and whether that is acceptable.* `rq2/verdicts/run_flat1/batch1_dispatch.txt` and
`rq2/verdicts/run_full1/batch1_dispatch.txt` (or the placeholder templates
`rq2/verdicts/dispatch_template.md` and `rq2/verdicts/dispatch_fullstage_template.md`) hold the
prompts verbatim, in Chinese, with the four defects plainly visible — I confirmed all four by reading
them. That is acceptable: the prompts the judges actually read ship, they are authoritative, and a
reader needs no interpretation to check the paper's descriptions against them. What is **not**
acceptable is §4.1's sentence claiming English renderings also ship: there is no such file in the
package, and an expert who wants the comparison in English is left with `pipeline/agents/chain-auditor.md`
— the deployed pipeline's agent definition, which is English and describes the same four perspectives
but is a *different object* from the RQ2 dispatch (it is the plugin spec, and it is where the letters
are not exchanged). That file is a partial substitute, not the promised rendering. See W1.

### Q3 · The measurements

Everything below was recomputed from `.paperpilot/phase2-rerun/arms/rq2_3run/…` and the artifact's
`rq2/verdicts/…` with independent code (`verification/indep_recompute.py`, `indep_claims.py`,
`indep_claims3.py`), using only the conventions the paper states in text (majority over three runs; a
routed case counted confirmed by convention, re-scored False-Positive under the forced reading;
further details in the method note).

*The rule's effect on both backbones, at both levels.* **Reproduces.** Primary: flat →
flat+aggregation 0.588 → 0.765 at the recall level, 9/0, p = 0.0039, and 34 → 51 on the confirmed set,
17/0, p < 0.0001. Second: 0.529 → 0.804, 14/0, p = 0.0001; 32 → 51, 19/0, p < 0.0001. The forced
reading moves 25 → 27 and 23 → 26, as §8 says. The two isolation steps also reproduce: schema-line
repair alone 30 → 35 recall (0/5, p = 0.0625) and 34 → 39 confirmed (1/6, p = 0.1250), forced 25 → 29;
the routing rule on top 35 → 39 recall (2/6, p = 0.2891) and 39 → 51 confirmed (2/14, p = 0.0042),
and forced the other way (29 → 27, 3/1).

*The four-perspective contrast.* **Reproduces at the levels printed.** Primary 39 vs. 39, 4/4,
p = 1.0, matched-pairs half-width ±0.11 (I recompute ±0.109, so "the data exclude an effect larger
than about eleven points" is correct); second backbone 41 vs. 30, 12/1, p = 0.0034; forced 27 vs. 27
and 26 vs. 26 with intersections 22 of 27 and 23 of 26, both exact. — But see the level question
below.

*The evidence-access contrast, including the net and F₁ intervals.* **Reproduces.** 39 → 48 at the
recall level (0/9, p = 0.0039), forced 27 → 31, suppression 21/30 → 12/30; confirmed set 48 vs. 66
(0/18, p < 0.0001). Net +30 either way, difference 0, bootstrap 95% CI [−8, +8]; F₁ 0.821 without
source against 0.788 with it, +0.033, CI [−0.044, +0.115]. Both intervals span zero.

*The two forced spans.* **Reproduces.** Across the nine arms §4.4 contrasts: forced [23, 31] of 51
against convention [27, 48] — forced values 25, 29, 27, 27, 27, 31, 23, 26, 26 and convention values
30, 35, 39, 33, 39, 48, 27, 41, 30. The contract core at 8 forced / 8 convention and the two
source-only configurations at 20/36 and 19/37 also check out.

*The set intersections.* **Reproduces.** 22 of 27 and 23 of 26, as above.

*The clause census on both backbones.* **Reproduces exactly.** Primary: B=Confirmed 61 (56/5, 0.92),
A=Confirmed 21 (17/4, 0.81), D=Supports-Defect 7 (5/2, 0.71), A=Refuted 50 (26/24, 0.52), C=Refuted
19 (17/2, 0.89), D=Supports-Not-Defect 16 (12/4, 0.75), catch-all 69; total 243 with 153 judgments on
true bugs and 90 on false positives; 98 of 243 D cells in source vocabulary. Second backbone:
A=Refuted 56, C=Refuted 50 with 22 wrong, D=Supports-Not-Defect 2, `A=Refuted with B=Confirmed` 3,
catch-all 57; D-cell source vocabulary 217 of 243; incorrect False-Positive closures 48 of which
A=Refuted supplies 24 — 50% rather than 80%. Every figure in §4.5's cross-backbone paragraph is
exact. The compliance split also reproduces: the rule mandates Human-Review on 69 judgments, the
judge recorded it on 48, 17 forward departures to False-Positive (10 of them on true bugs) and 5 to
Confirmed, 1 reverse departure; both replays reproduce at both readings (strict compliance 43/51 and
19/30 convention, 27/51 and 27/30 forced; contract refutation routed 46/51 and 12/30 convention,
no-op forced).

*Any printed figure that does not reproduce.* Two, both reported in full above and as weaknesses.
(a) §4.4's "22 decisive routed cases ... the flat judge has 8" — see W2. (b) Nothing else. I went
looking specifically where earlier rounds bled, and all of it is exact: §4.1's pre-repair
counterfactuals ("41/51 with a confirmed set of 41+6", "39/51 and 39+9"); §4.5's pre-repair census
("47 closures and 20"); the re-judge ledger's 19 rewritten verdicts with 15 toward / 4 between / 0
away and the controls' unchanged true-positive sets at 48 and 33; `milvus_001`'s eleven-of-twelve
routing; the three-way splits (3 of 81) and the 37/51 alternative reduction; and the case-level span
of the A=Refuted errors (15 cases closed by that clause in ≥2 of 3 runs, 7 of them true bugs, all 7
unconfirmed).

*Any contrast reported at only one level or at mixed levels.* **Yes, three, all in §4.4's
four-perspective paragraph**, against §4.1's commitment that both levels are reported for every
contrast including the isolation steps. The primary four-perspective contrast (39 vs. 39, 4/4,
p = 1.0) and the second-backbone one (41 vs. 30, 12/1, p = 0.0034) are recall-level only; their
confirmed-set counterpart would be 51 vs. 51 with discordant 9/6, p = 0.6072, which appears nowhere
in the `.tex`. Likewise the two auxiliary readings at the end of the same paragraph (+3 at 5/2,
p = 0.4531 and −2 at 1/3, p = 0.6250) are labelled recall-level and their confirmed-set counterparts
(6/4, p = 0.7539 and 2/5, p = 0.4531) are omitted. See W7. I found no contrast reported at *mixed*
levels — every rate carries its reading and its level, and the `a/b` discordant-pair convention ("a is
the arm whose count is printed first") is used consistently in both directions, which I checked on
six contrasts.

### Q4 · The clause census's own consistency

**The distribution reproduces exactly.** The primary backbone has 19 judgments whose closing clause is
C=Refuted, and I read all nineteen with their recorded `perspectives.C`, `d_evidence` and `rationale`:

| kind | judgments | cases |
|---|---|---|
| in-source comment or docstring | **15** | milvus_015 r1; milvus_023 r1–r3; qdrant_003 r1; qdrant_011 r1; qdrant_012 r1; qdrant_013 r1, r3; qdrant_025 r1, r2; weaviate_004 r1–r3; weaviate_007 r1 |
| the server's own name-validation rule, code and error message named | **2** | milvus_026 r1, r2 |
| code structure only — a default expression; a fallback chain | **2** | milvus_011 r3; milvus_012 r3 |

That is 15 + 2 + 2 = 19, and the run indices match the paper's ("`milvus_026`, in two of its three
runs"; "`milvus_011` and `milvus_012`, each in its third run"). The two structure cases cite
`plan_parser_v2.go:113-115` (an empty filter mapping to `trueLiteral`, the parameter "deliberately
declared optional") and `handler_v2.go:362-367` (an explicit three-level `dbName` fallback chain).
Neither cites a comment. The paper's claim that "None rests on observed behaviour alone" also holds —
but note that the protocol requires more than "not observed behaviour alone": §3.5 says "Bare
structural inference ('no validation is present') is recorded as a weak refutation and routed to
human review rather than closing the case", and both of these two closed the case on exactly bare
structural inference.

**The weak-refutation claim about the same cases' other runs is exact.** `milvus_011` run 2 reads
"C 仅 WEAK_REFUTED（无注释静默行为）" — a silent behaviour with no comment behind it — and
`milvus_012` run 2 reads "兜底链结构示设计但无注释/quote 明文(红线3 不构成 REFUTED)" — the
fallback-chain structure shows design but carries no comment or quote, so red line 3 does not admit
it. Both are the case's second run, as the paper says.

**Is the consequence stated honestly?** Yes, and in a way I want to credit explicitly. §4.5 says:
"The verbatim-evidence requirement is therefore not applied uniformly by the judge that recorded
these cells---a departure the compliance recount below does not catch, because that recount measures
compliance with the *aggregation* rule, and this is a requirement of the perspective itself." I
checked that this is exactly why the recount misses it: `clause_tally.py` derives the closing clause
*from the judge's own recorded perspective values* and then asks only whether the recorded verdict
matches what that clause assigns. A judge that wrongly writes `C=REFUTED` is therefore counted as
compliant, and the two independence cases are counted as C-clause successes/failures rather than as
protocol departures. The paper names the mechanism correctly and puts the disclosure in §4.5 rather
than in a limitations footnote.

Two observations the paper could make and does not, both of which *strengthen* its position, which is
why I raise them as questions rather than objections. First, the departure cuts in both directions:
of the two misapplied C-closures, one is on a false positive (`milvus_011`) and one on a true bug
(`milvus_012`), so the unguarded discipline is not a one-way bias. Second, compliance with the C
requirement does not guarantee accuracy — the clause's two errors are `weaviate_007` run 1, which
cites a genuine comment verbatim ("Set these defaults if the user leaves them blank") and is wrong
anyway, and `milvus_012` run 3. The paper reports C at 17/19 without noting that one of the two
misses came through the guard rather than around it, which is arguably the more interesting fact for
its thesis: a verbatim-evidence guard certifies the *form* of the evidence, not its relevance.

### Q5 · Compliance

Measured on the rebuilt `TestVDB-v10.pdf` (three `pdflatex` passes from `TestVDB-v10.tex`; byte
identical to the PDF shipped beside it, 940,109 bytes, so the build is deterministic).

**Page split.** 20 pages total. Body text and figures run from p. 1 to p. 18; the Conclusion ends
part-way down p. 18 and the Data Availability statement begins at the same point (p. 18, ≈35% down
the page). References begin on p. 18 and run through p. 20.

- Text + figures: **≈17.4 pages** (p. 1 through p. 18 to the start of Data Availability) ≤ 18. ✓
- References: **≈2.4 pages** (39 entries, `[1]`–`[39]`) ≤ 4. ✓
- Data Availability **after the Conclusion**: ✓ (Conclusion → Data Availability → References, the
  order the CFP requires).
- Double-anonymous: ✓ `\documentclass[acmsmall,screen,review,anonymous]{acmart}`; running heads read
  "Anon."; no author block, no acknowledgements, no affiliation; the artifact URL is
  `https://anonymous.4open.science/r/TestVDB_artifact-EC36/`; a grep for self-identifying patterns
  (acknowledgements, "our previous work", named repositories, author names) returns nothing
  substantive.
- LaTeX hygiene: 0 errors, 0 undefined references, 0 overfull boxes. 24 underfull boxes remain, all
  in table cells and vertical glue — cosmetic.

Two remarks. First, this is a genuine fix of the previous round's problem: the appendix that was
carrying the paper past the limit is gone and the body now has ~0.6 pages of headroom, which is thin
but compliant. Second, the two floats affected by W3 set at the wrong size, so fixing the form feed
will *shrink* Tables 1 and 2 and buy back a little of that headroom rather than cost it.

### Q6 · What sinks it now?

**First hostile objection, verbatim as I would expect to read it:** *"The paper's headline is that the
error mass sits in the unguarded clause, and it prices the fix at seven true bugs for nine
interceptions — but its own §4.5 shows the pattern reverses on the second backbone (by-design closes
50 and is wrong 22 times; the unguarded clause supplies 50% of the bad False-Positive closures rather
than 80%), and §4.4 shows the prescription is a no-op under the forced reading. The census is
therefore a one-backbone observation about a counting convention, not a property of the protocol; and
the one contrast the paper's account rests on — flat judge to rule-bearing judge — differs in three
edits, with the four-perspective arm differing in five, so 'it is the routing, not the organization'
is a claim about a bundle."*

**Fatal, fixable, or already answered?** Mostly already answered, and the residue is fixable by
wording. The reversal is in the abstract, §1, §4.5, §5 and §6 — the paper does not hide it, and §5
draws the right inference from it ("the rule is advice about where to look rather than a property of
the protocol"). The forced-reading no-op is stated in the same sentence as the counterfactual every
time it appears, and §8 turns it into the paper's actual thesis. The bundle criticism is answered by
the isolation steps §4.4 supplies (schema-line repair alone; routing rule on top) and by the
hand-priced floor, which the paper states is a floor and calls "suggested, not established". What is
*not* answered is that the paper's own promised symmetry — both levels for every contrast — is broken
exactly in the paragraph where the four-perspective contrast is discussed (W7), and that a
reader cannot reconstruct two of the denominators in the pricing sentence (W2). Those two are the
handholds an unsympathetic reviewer will use to argue that the paper reports the readings that
survive and omits the ones that do not; both are repaired by printing numbers the shipped script
already computes.

So: **not fatal; fixable; the substantive objections are already answered in the text.** The paper's
survival depends on the authors being willing to make three small, purely presentational changes
(W1, W2, W7) that remove the appearance of selective reporting without altering a single result.


## Scored Judgement

| Criterion | Tier | One-line justification |
|---|---|---|
| Importance & Scope | **Good** | The question — how much of what a documentation-derived oracle reads is actually in the documentation, and where inside the judge do the errors land — is the right one for this line and is measured for the first time; scope is one pipeline, three vendors, 81 cases, one backbone for the census. |
| Insights & Evidence | **Good** | Both headline results (43.3% of cited pairs unsupported; 24 of 50 unguarded closures on true bugs, 80% of bad False-Positive closures) recompute exactly and survive the construction checks the paper runs on them; the census reverses on the second backbone and its prescription is convention-only, both self-disclosed. |
| Perspective | **Excellent** | Four self-reported instrument defects, two leak repairs priced against the authors' own interest, both readings printed for every headline rate, an adverse second-backbone result in bold, and one genuinely new finding ("the organization changes which cases are decided, not how many"). |
| Verifiability | **Good** | All five scripts run in place and every load-bearing number reproduces from raw verdicts, including the two prices the paper calls unscripted; held back by one false claim about the package (English renderings, W1), two unreproducible denominators (W2), and one unshippable check. |
| Presentation | **Good** | Dense but disciplined; every rate carries its reading and level and the `a/b` convention is consistent; docked for the literal `ootnotesize` in two tables (W3), a sentence in §4.5 that conflates vocabulary with clause (W4), and three contrasts printed at one level after §4.1 promised both (W7). |

**Overall: Weak Accept** — **CONDITIONAL**.

**Conditions (all textual; none requires new measurements):**
1. Delete or substantiate §4.1's clause claiming the artifact ships English renderings of the two
   judging prompts (W1).
2. Either script the contrast pricing or correct the two routed-count denominators in §4.4 (W2).
3. Fix the two `\footnotesize` macros that have lost their `\f` (W3).
4. Reword §4.5's "the 32 catch-all judgments whose D cell the rule does define" (W4), add the census's
   scope to §8 (W5), print or explicitly decline the three missing confirmed-set tests in §4.4 (W7),
   and either report the per-perspective cell vocabularies or soften §1's identification claim (W6).

**What would move me to Accept in a later round:** the conditions above, plus one substantive
addition — a re-adjudication, on even a subsample of the fifteen cases the census's clause closes in
at least two of three runs, of whether a judge given a verbatim-evidence guard on contract refutation
reaches the same place. §4.5 currently says this "cannot be computed from frozen data", which is
true; but it is the one experiment that would convert the paper's prescription from a property of the
counting convention into a statement about the stage. Everything else is already there.

---

## Method Note: What I Recomputed, and How

**Environment.** Artifact `c:\Users\11428\Desktop\TestVDB_artifact`, git HEAD `432459e`, working tree
clean; frozen verdicts also available at
`.paperpilot/phase2-rerun/arms/rq2_3run/`. Python 3.13 (stdlib only) and PyPDF2 for PDF inspection;
MiKTeX-pdfTeX 4.23 for the LaTeX rebuild. All scripts and raw outputs are under
`reviewer-2/verification/`.

**Step 1 — ran the artifact's five scripts in place, unmodified, from the artifact root.**
`recompute_paper_numbers.py`, `clause_tally.py`, `clause_tally.py second`, `convention_pricing.py`,
`bootstrap_net_f1.py`, `audit/pair_audit.py`. Transcript: `artifact_scripts_raw.txt` (242 lines).
Each script's `ROOT` is `rq2/verdicts`, so the run is self-contained.

**Step 2 — independent re-derivation from raw JSONL only (`indep_recompute.py`,
`indep_claims.py`, `indep_claims3.py`).** These do not import the artifact's analyses. Arm→directory
→override-file mapping taken from the README's table and the paper's §4.1 text; a run is a dict
`case -> record` assembled from `verdicts_batch{1..6}.jsonl` with the re-judge file applied as an
override; majority over three runs with `HUMAN_REVIEW` counted confirmed under the convention and
re-scored `FALSE_POSITIVE` under the forced reading; exact McNemar as
`2 * sum_{k<=min(b,c)} C(n,k) / 2^n`; matched-pairs Wald half-width
`1.96 * sqrt(a+b - (a-b)^2/n)/n`; Wilson intervals for the arms. Outputs:
`indep_recompute_output.txt`, `indep_claims_output.txt`, `indep_claims3_output.txt`.

**Step 3 — the clause census, reimplemented from the paper's §3.5 clause order** (A=Confirmed →
A=Refuted with B=Confirmed → A=Refuted → B=Confirmed → D=Supports-Defect → D=Supports-Not-Defect →
C=Refuted → catch-all), applied to the recorded perspective cells of `run_full{1,2,3}` (primary) and
`run_fullq{1,2,3}` (second). Reproduced both censuses, the compliance split, both replays at both
readings, the D-cell vocabulary split (98/243 and 217/243), the catch-all composition
(`NO_SIGNAL` 32, `by_design_in_source` 11, `validation_present` 10, `validation_absent` 9,
`not_found` 7), and the base rate 153/243 = 63.0%.

**Step 4 — the C=Refuted cell audit.** Printed all nineteen judgments with `perspectives.C`,
`d_evidence` and `rationale`, classified each citation by hand into comment/docstring, server
validation rule, or code structure, and cross-checked the same cases' other runs for the recorded
`WEAK_REFUTED` rationales. Also printed every `WEAK_REFUTED` run of `milvus_011`, `milvus_012` and
`milvus_026` in full.

**Step 5 — package-property checks.** (a) Read `README.md`'s "Script coverage" paragraph and compared
it to §4.1's sentence about the five scripts; (b) searched the whole package (case-insensitive,
all text extensions) for the English protocol vocabulary and for any file with `prompt` in its name,
to test §4.1's "English renderings" claim; (c) diffed the four control dispatches against their
parents with `difflib` to test the arm-edit paragraph line by line; (d) read the two aggregation
blocks and both perspective definitions in `run_full1/batch1_dispatch.txt` to test the four
self-reported dispatch defects; (e) counted the binary-vs-three-valued `verdict` schema line across
all twelve arms; (f) opened `pipeline/agents/chain-auditor.md` to see what English material a reader
can and cannot substitute for the removed prompt appendix.

**Step 6 — the ledger.** Loaded `rq1/ledger/phase1_issue_classification.xlsx` with `openpyxl`,
enumerated all 136 data rows, filtered the three systems (132 rows), and reproduced the adjudicated /
unadjudicated / withdrawn split, the 19/16/15 version counts, the per-vendor 43-28-10 and 29-14-8 and
11-9-3 and 14-14-2 tables, and the four category counts behind §4.2's "23 fixed, 18 acknowledged-open,
7 closed without a fix, 3 tracked as duplicates".

**Step 7 — the crash-oracle baseline.** Walked `rq3/runs/full-coverage-v3/logs/` (206 files),
decoded the literal `\uXXXX` escapes that the logger writes, and counted response-status lines,
completed mutation stages, anomaly-report lines and status-code frequencies, with and without the
11.5 MB master log. The master log is a verbatim echo, and the arithmetic confirms it exactly:
counting all 206 files doubles the per-template figures (23,258 = 2 × 11,629 status lines;
2,254 = 2 × 1,127 stages; 304 = 2 × 152 anomaly lines), which is why the single-copy numbers the paper
reports are the right ones. Also checked that all 152 anomaly-report lines carry the value 3, and read
the surrounding log lines to confirm the no-mutable-fields mechanism the paper describes ("No mutable
fields found" immediately followed by "found 3 mutation sequences causing anomalies").

**Step 8 — compliance.** Rebuilt the PDF (`pdflatex` ×3) and measured the split with PyPDF2 by
stripping the line-number column and locating the "Data Availability" and "References" markers on
each page; counted the reference list (`[1]`–`[39]`); grepped for anonymity tells; counted LaTeX
errors, undefined references and over/underfull boxes from the `.log`; and scanned the `.tex` at byte
level for control characters, which is how W3 was found (form feeds at bytes 11267 and 33598).

**Step 9 — the unscripted quantities.** Reconstructed the hand-adjudicated joint prices from
`rq2/analyses/pricing/HR17_adjudication_worksheet.md` (parsed the 22 `裁决:` checkboxes: 9 CONFIRM,
2 RETURN, 6 REJECT in the 17-case sheet plus 5 in the two addenda) crossed with the forced true-positive
sets, giving 33 / 32 / 29 for the full stage, the rule-bearing control and the flat judge — the paper's
printed values. Tried six operationalizations of "decisive routed case" against the same worksheet to
test §4.4's 22/9 and 8/2; the never-ruled sub-counts reproduce under
≥1-of-3-routing-plus-convention, the totals do not (`decisive.py`, `decisive_output.txt`,
`joint_spot_output.txt`).

**Verification inventory** (`reviewer-2/verification/`): `artifact_scripts_raw.txt` (all five
scripts' output); `indep_recompute.py` + `_output.txt`; `indep_claims.py` + `_output.txt`;
`indep_claims3.py` + `_output.txt`; `baseline_count.py` + `_output.txt`; `anom_vals.py`;
`pagesplit.py`, `pagesplit2.py` + `_output.txt`; `pricing_check.py` + `_output.txt`;
`decisive.py` + `_output.txt`; `joint_spot.py` + `_output.txt`; `ws_outline.py`.

**What I could not verify, and why.** (i) The expectation-framing check's 19 hits — no script, no
intermediate list, no pattern in the package (my own scan of all 81 packs finds zero
expectation-framed sentences in English or Chinese, which is consistent with the claim but is not the
same test). (ii) §4.2's "One of the 51 is a crash-or-panic defect" and the fix-PR characterisation
("all 23 merged fixes modify implementation code, 15 also add a regression test, and none is
documentation-only") — the paper states the second is not part of the shipped artifact, and the first
has no supporting table in the ledger; both are correctly flagged by the paper itself. (iii) The
independent adjudicator's raw passes: the three `blind_pass_*_verdicts.jsonl` files and
`convention_pricing.py` reproduce the agreement counts (4, 5, 6 of 20) and κ (−0.01, 0.08, 0.11), but
whether those passes were run under the protocol statements the paper describes is not checkable from
the package beyond the file names.
