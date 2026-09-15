# Reviewer 1 (Domain Expert) — FSE 2027 review of `TestVDB-v10.tex` / `TestVDB-v10.pdf`

**Object under review:** the LaTeX submission and its compiled PDF (20 pages), not a markdown draft.
**Evidence used:** the frozen verdicts and the replication package at `c:\Users\11428\Desktop\TestVDB_artifact`
(git HEAD `432459e`), plus targeted web verification of the bibliography.
**Method:** every number below that I state as a fact was recomputed by running shipped scripts in
place or by writing throwaway probes against the shipped raw files; the full list is in the Method
Note at the end. Items I could not reproduce are marked as such.

---

## Overall Recommendation

**Weak Accept.** Chair's verdict: **CONDITIONAL**.

The submission is the same measurement/experience paper that has been converging over the last
several rounds, now in LaTeX and with the appendix removed to meet the page limit. I reproduced
essentially every printed number from the shipped artifact, including the four quantities the paper
itself says are *not* scripted (I recomputed the joint pricing of the headline contrast from the
shipped worksheet and it lands on 32-vs-29 / 33-vs-29 exactly). The protocol claims that moved into
§4.1 after the appendix was cut verify verbatim against the shipped dispatch texts. The reference
list contains no fabrication that I could find in a sample of 18 entries; one author-name error and
two minor bibliographic slips are the extent of it.

The conditions are small and mechanical (see W1–W3): a LaTeX-conversion corruption that prints the
literal string "ootnotesize" inside two tables in the shipped PDF, one wrong author given name, and
two bibliographic details to re-check. None of the science is at risk. What keeps this from a clean
Accept is unchanged from the previous round and is not a defect the authors can fix by editing: the
paper's own claim is now the null-ish result — organization changes *which* cases a judge decides,
not how many — and its one positive effect (the routing rule) is worth +3 under the paper's own
honest reading, priced by the authors themselves as "suggested, not established" (§4.4). That is a
coherent, well-evidenced measurement paper, and it is scoped honestly, but it does not deliver a
positive result a reviewer can take home.

---

## Summary

The paper is a measurement study of the confirmation stage of an LLM-based bug-finding pipeline for
vector DBMSs. Three objects are measured: (i) a mining campaign's ledger — 81 adjudicated
submissions, 51 maintainer-confirmed, 23 merged fixes, across Milvus/Qdrant/Weaviate and 19
versions; (ii) an audit of the oracle's *input* — every one of the 134 (constraint, cited-page)
pairs that the confirmation stage reads, of which 18 are supported as cited and 58 have no support
on the cited page (two 43.3% shares of 134); and (iii) a clause-level census of the stage's own 243
judgments on the primary backbone, locating the error mass in the one refuting clause the protocol
does not guard (contract refutation: 50 closures, 24 of them real bugs; 24 of the stage's 30
incorrect closures to False-Positive = 80%), while the verbatim-guarded by-design clause is the
most accurate refuter measured (17 of 19). A counterfactual replay prices the guard move at seven
true bugs for nine false-positive interceptions under the deployment's counting convention and at
nothing under forced verdicts — the paper says so itself, and that is the paper's most interesting
single sentence.

---

## Core Strengths

**S1 — The verification story is real, and it survived my attempt to break it.**
I ran `rq2/analyses/recompute_paper_numbers.py`, `clause_tally.py` (both backbones),
`convention_pricing.py`, `bootstrap_net_f1.py` and `audit/pair_audit.py` from the artifact root, and
every rate, discordant pair and p-value I checked matches the paper: the arm matrix (deployed stage
39+9, forced 27; flat 30+4, forced 25; flat+schema 35+4, forced 29; flat+aggregation 39+12, forced
27; no-source 48+18, suppression 0.400, forced 31; no-aggregation 33+3, precision 0.917; contract
core 8/51 at suppression 29/30; the Qwen arms 27/41/30 all matching §4.4 and §8). The 16 paired tests
(10 at recall level) that §4.1 says are printed all appear with the printed values, the Holm
family of ten is non-circular and reproduces (0.0001/0.0034/0.0039/0.0039 against α/10…α/7, stopping
at the fifth, 0.0225), and the census sums to 243 exactly (61+21+7+50+19+16+69). Four previous rounds
paid a reviewer to catch a number error; this round I caught none.

**S2 — The two "printed but not scripted" quantities are nevertheless fully reconstructible from the
shipped raw material.** The README says the joint prices, the catch-all composition and the
expectation-framing check are not scripted. I rebuilt the first two from the worksheet and the
verdicts: the catch-all (the 69 rule-mandated judgments) splits 37 with the source vocabulary in the
D cell — 53.6%, printed as 54%, resting on 28 true bugs — against 32 with a rule-defined D cell, 17
of which rest on true bugs (53.1% against a 63.0% base rate, ≈1.1 SE below); and the joint pricing
reproduces to the case: rule-bearing control 32/51 vs flat 29 (+3), deployed 33 vs 29 (+4), 22
decisive routed cases in the control with 9 never ruled (one of them a true bug), 8 in the flat
judge with 2 never ruled (none a true bug), symmetric crediting +4, asymmetric +5. A reader who
wants to check the paper's most contestable numbers can do it without asking the authors anything.

**S3 — The audit of the oracle's input is the generalizable contribution, and it is measured, not
asserted.** 134 pairs, three-way split, with the class boundaries defined so that the two 43.3%
shares cannot be misread as a combined 86.6% (Table 3 and its caption make this explicit). The case
level is measured on a *different* object and reported as such (12 assertions: 5 supported, 3
dropped, 2 over-strong, 2 weak-evidence). The two mechanisms behind it (version drift from the
augmentation script; conceptual-only documentation) are named. To my knowledge this is the first
pair-level measurement of this step in this line of work, and §5 draws the transferable lesson
without over-claiming it (the paper explicitly refuses to generalize the rates).

**S4 — Disclosure discipline that most papers in this register do not have.** The counting convention
is priced in *two* places, both readings are printed for every contrast, the independent adjudicator
is reported as a bound (κ = −0.01/0.08/0.11 on 20 commonly ruled cases; two of three passes at the
forced floor), the pre-repair state of every leak repair ships alongside the cleaned one, and four
defects in the authors' own dispatches are reported rather than repaired quietly — including the one
that costs them: the deployed dispatch defines the four perspectives twice with C and D exchanged and
declares the source vocabulary in the D slot, which is why §4.5 must identify the letters by content
on the primary backbone and cannot on the second.

**S5 — The §4.5 identification repair is now accurate to the cell.** The previous round's mis-stated
distribution is fixed: I read all 19 C=Refuted-closing judgments. Fifteen rest on an in-source
comment or docstring; two (milvus_026, in two of its three runs) on the server's own name-validation
rule; two (milvus_011 and milvus_012, each in its third run) on code structure — a default
expression and a fallback chain, exactly as printed. I also checked the two cases' *other* runs: both
do record WEAK_REFUTED with the reasons the paper quotes ("no comment behind a silent behaviour";
the fallback chain "shows design but carries no comment or quote"). The paper's claim that the
verbatim-evidence requirement is not applied uniformly by the judge that recorded these cells is
therefore not a rhetorical hedge — it is literally what the cells say.

**S6 — The apparatus around the claims is internally consistent at a level I rarely see.** The
nine-arm forced span [23, 31] and convention span [27, 48] reproduce; the source-only arms' 0.706
and 0.725 match 36/51 and 37/51; "one of the 51 is a crash-or-panic defect" is exactly one ledger row
(qdrant #9045, empty-vector upsert panic); "eleven of the twelve configurations route milvus_001"
reproduces per-arm; the three three-way-split cases are milvus_021/milvus_038/qdrant_027 and the
strict-two-identical-verdicts rule gives 37/51 exactly as §4.1 says; the "22 departures forward and
one in reverse" is literally 17 forced-to-False-Positive + 5 to Confirmed (10 of the 17 on true
bugs) and exactly one reverse cell (milvus_019 run 1); and the RQ3 counts are exact — 205
per-template logs + 1 master, 11,629 response-status lines and 1,127 stage completions in the
per-template logs with the directory total exactly doubled by the echo, 0 anomalies, 152
false-anomaly lines reading "3 apiece" across 119 logs, wall time 50.75 minutes.

---

## Core Weaknesses

**W1 — The LaTeX conversion corrupted two `\footnotesize` commands; the literal string
"ootnotesize" is typeset in the shipping PDF. `[minor, fixable]`**
The source file contains two FORM FEED bytes (0x0c) where the two characters `\f` belonged, at
lines 166 and 466 — the only two control characters in the file. LaTeX treats the form feed as
whitespace, so it typesets the remaining letters. In `TestVDB-v10.pdf`, `pdftotext` recovers
`ootnotesize` as a standalone line directly under the caption of Table 1 (the oracle table, p.4) and
again *inside* the body of Table 2 (the twelve configurations), immediately before the row for
configuration 6 ("… ootnotesize 6 source-only -- -- ✓ GLM-5.3-Flash"), where it displaces that row's
layout. Two consequences: a reader of the PDF sees garbled text in two tables, and both tables are
set at body size rather than footnote size. The fix is to retype `\footnotesize` at those two lines.
Note for the authors: the memory of this project already records this class of bug for bash heredocs
(an unquoted heredoc turns `\f` into 0x0c); this is a fresh instance that survived the compile
because a form feed is legal input. It is worth an automated scan for control bytes in the `.tex`
before submission, because this one is invisible in the log (0 errors, 20 pages).

**W2 — One bibliography entry has the wrong author. `[minor, fixable]`**
`haldar25` reads `author = {Haldar, Reshma and others}`. The paper is "Rating Roulette:
Self-Inconsistency in LLM-As-A-Judge Frameworks", Findings of EMNLP 2025 (2025.findings-emnlp.1361),
by **Rajarshi Haldar and Julia Hockenmaier** — the given name in the bib is wrong ("Reshma" for
"Rajarshi") and the second author is hidden behind "and others". Under the CFP's reference-integrity
check this is not a fabrication (title, venue, year and first-author surname are correct) but it is
exactly the class of error that check is built to surface, and it is trivially fixable.

**W3 — Two bibliographic details to re-verify against the publisher record. `[minor, fixable]`**
(a) `ddlcheck25`: the bib prints pages 2281--2293; the PVLDB record I located gives PVLDB 18(7):
2281–2294. (b) `agoraplus25`: the bib gives year 2026; every source I found (including the authors'
own page, `rest-oracle-tosem2025`) places the TOSEM article's publication in 2025, with the
companion RCR report in TOSEM 35(7), July 2026 — so the year is at best the issue year and at worst
off by one. Neither is a reason to doubt the entry; both are one-line corrections. I also could not
confirm the third decimal of the Metamon figures the paper quotes ("precision 0.722 at recall
0.480"): every source I can reach states 0.72 / 0.48, so the paper may be quoting the results table
while the abstract rounds — the authors should confirm they are quoting the table, and if they are
not, round to 0.72/0.48.

**W4 — The census's central count, and its scope, are the paper's own hostage. `[major, unfixable
by editing]`**
Nothing in this round weakened it — the numbers are, if anything, more airtight than before — but
the first hostile question will be whether a single-backbone census that does not reproduce on the
second backbone, on a dispatch that (by the authors' own defect report) defines the perspectives
inconsistently, can carry a contribution. The paper's answers are on the page: the letters are
identified by their content on the primary backbone (§4.5, S5 above), the counterfactual is
explicitly "a replay rather than a re-adjudication" whose gain exists only under the convention, and
§5 moves from "the guard is misplaced" to "look at your own clause census, not at ours". A hostile
reviewer can still call the residual claim thin. The only fix is new evidence (a re-adjudication of
the routed refutations under a verbatim guard, on both backbones), which is beyond a revision cycle.
I record it as a weakness of the *result*, not of the *reporting*: the reporting is honest about it,
and that honesty is precisely why the paper reads as a measurement paper rather than an overclaimed
one.

**W5 — The headline positive is a convention artifact, and the paper's own pricing says so.
`[major, unfixable by editing]`**
"Adding an aggregation rule that lets it route a case to human review rather than close it raises
recall on both backbones (0.588 to 0.765 … 0.529 to 0.804)" (§8) is, mechanically, the routing rate
— under the convention a routed case counts as confirmed, so a judge that abstains more scores
higher. The paper says this in as many words and prices it at the honest reading (+3 for the control,
floor). Reviewers who read only §8's first paragraph will still come away with the wrong impression:
the sentence is true, but its most natural reading overstates what was achieved. This is a framing
risk the authors have largely handled (the sentence continues "and we say so"), and I did not find a
place where the paper claims more than it priced. But it will be the first thing a hostile reviewer
writes down, so I put it here rather than in the questions.

**W6 — Minor prose damage from the conversion, no meaning loss. `[minor, fixable]`**
The abstract and §1 bullet 2 now say only that "the audit acted on all 12" case-level assertions,
where the markdown source's abstract carried the 5/3/2/2 breakdown. The breakdown is still in §4.3
and matches the shipped audit verdicts (5 SUPPORTED, 3 UNSUPPORTED, 2 WEAK_EVIDENCE, 1
OVER_STRONG_REWRITE + 1 OVER_STRONG_WEAKEN). This is compression, not error, and the abstract is
better for it; I flag it only because Q1 asks me to check whether anything changed meaning, and this
is the one place where content, not just form, moved.

---

## Detailed Assessment

### 1. Importance & Scope — **Good**

The paper studies a real and under-measured question: what a confirmation-stage LLM judge actually
buys, and where inside it the errors live. The three-system campaign (Milvus/Qdrant/Weaviate), the
81-case adjudicated pool, the 12 configurations and the audit of every cited pair the judge reads
give the paper more empirical surface than most measurement papers in this register. The scope
statement is unusually disciplined: the ledger is "a record of submissions and adjudication, not a
per-run detection rate" (§1), the voided detection experiment is disclosed (§4.2), the census is
scoped to one backbone (§4.5, §6), and the rates from the pair audit are explicitly refused as
general properties of LLM distillation (§4.3). I checked the ledger in the shipped xlsx and the
campaign's claims are exactly right: 132 rows over three systems, 81 adjudicated (A∪B∪C) + 49
unadjudicated + 2 self-submitted PRs excluded, 19 distinct versions with the 81 spanning 16 and the
51 spanning 15, and the per-system and outcome splits (23 fixed / 18 acknowledged-open / 7
closed-no-fix / 3 duplicates; Milvus 43 (29/11/14), Qdrant 28 (14/9/14), Weaviate 10 (8/3/2)) all
reproduce. Why not higher: the domain is narrow by design (one task, one pipeline, three systems),
and the campaign contributes a record rather than ability, which the paper states. The transferable
part — the *audit* and the *census* — is what carries the scope, and it is genuinely scope-worthy.
The one scope claim I could not verify is the fix-PR characterisation (all 23 modify implementation
code, 15 add a regression test); the paper correctly marks it as outside the shipped artifact.

### 2. Insights & Evidence — **Good**

Two insights are earned rather than asserted. (1) *The distillation is the unmeasured step*: 18 of
134 cited pairs supported, 58 mis-anchored, 58 unsupported, with the two mechanisms named, and the
follow-on check that no rebuilt package contains a pipeline-authored expectation sentence
(spot-checked: the "should"-phrased hits I sampled are quoted server responses, consistent with the
§4.3 account; the check itself is not scripted, and the paper says so). (2) *The guard sits on the
already-clean clause*: contract refutation closes 50 judgments and is wrong 24 times while the
verbatim-guarded by-design clause closes 19 and is right 17 times, and the "24 of 30 incorrect
closures = 80%" is exact — and, importantly, computed on maintainer-confirmed labels only. The
supporting arithmetic is invariant in the right way: the load-bearing 24 holds in both the pre-repair
(47/20) and post-repair (50/19) census, no cell on the primary backbone carries the
A=Refuted-with-B=Confirmed pair that the other printed rule would route (I confirm zero; the second
backbone has three), and the catch-all composition is reported as composition rather than as a rate.
The evidence is also honestly bounded in three directions at once: cross-backbone non-reproduction,
the C/D letter ambiguity, and the convention pricing. What keeps this at Good rather than Excellent:
the second insight does not survive its own cross-backbone check (by-design closes 50 and is wrong
22 on the second backbone), so the general claim reduces to "audit your own census", and the
counterfactual is a replay, not a re-adjudication — a limit the authors state in the same paragraph.
The quantitative story is strong; the generalizable claim is a rule of thumb, and the paper says so.

### 3. Perspective — **Good**

The paper's stance is the most distinctive thing about it and the reason it has been converging
rather than oscillating: it reports defects in its own instrument (four, with consequences), prices
the counting convention at two places, prints both readings of every contrast, and treats the
deferral channel as the finding rather than as a nuisance ("on this pool, what an LLM judge confirms
is decided less by how it is organized than by how it accounts for the cases it refuses to decide").
The related-work positioning is accurate where I checked: Metamon's self-referential falsifier and
its precision/recall profile, Ma et al.'s bias-not-accuracy framing, Molinelli et al.'s leakage-free
benchmark, LogicHunter's documentation-as-intent-but-consults-implementation oracle, TRACE's
implementation-drift blind spot — all verified true of the works they name. The self-audit lesson in
§5 ("check the dispatch before you re-architect the judge"; "a one-line schema repair moved five of
the headline nine bugs") is earned. Why not Excellent: the perspective is now almost entirely
first-person or negative — the paper's message to the field is "measure your materials, price your
convention, audit your census" — and it has no positive methodological artifact a reader can adopt
wholesale (the audit discipline is described but not packaged, e.g. as a checklist or script beyond
`pair_audit.py`). As a domain expert I find the negative results credible and useful; I would not
call the perspective field-shifting.

### 4. Verifiability — **Excellent**

This is the criterion on which this round's object improved most, and it now holds end to end. I ran
the five named scripts in place from the artifact root with no edits; they print the paper's numbers,
including both readings of every contrast, both censuses (`clause_tally.py second` reproduces 56
contract-refutation closures, 50 by-design closures with 22 wrong, 24-of-48 incorrect closures =
50%, D-cell source vocabulary 217/243), both replays, and the net/F1 bootstrap intervals. The two
quantities the README declares unscripted are reconstructible from shipped raw material (S2), and I
did reconstruct them. The dispatch texts ship per run, and the §4.1 arm-edit paragraph — the
material moved out of the deleted appendix — verifies *verbatim*: the schema-fix arm differs from the
flat judge only in the output-schema line and path; the aggregation arm differs additionally in the
sentence that declares no aggregation rule applies and the appended routing clause; the
source-withheld arm has 0 `source=` lines against the full stage's 14; the no-aggregation arm has 0
aggregation blocks against the full stage's 2. The leak-repair bookkeeping also checks out at the
file level: 13 `_pre_cogstrip_merge/` directories = the nine primary-backbone runs + the second
backbone's source-only three + its flat judge one, exactly as §4.1 says, and 12 `_pre_coganchor`
files; the re-judge files rewrite 19 verdicts, 15 toward confirmation under the convention, 4
between Confirmed and Human-Review, 0 away, with the two control arms' TP sets unchanged (48, 33),
their FP counts +2 and +1, suppression 0.467→0.400 and 0.933→0.900, and the no-source arm's forced
recall 30→31; the pre-repair deployed stage reads 41+6 against the reported 39+9. The paper's
statements about what ships are true, including the negative ones ("the earlier rebuilt generations
are archived separately and do not ship"). The only things I could not check were the ones the
artifact legitimately excludes (the fix-PR characterisation; the expectation-framing census; the
per-run weights of the two backbones, which are aliases without pinned weights — a limit the paper
states). Scoring a submission Excellent here means I would accept its numbers without re-running
them; on this evidence I would.

### 5. Presentation — **Good**

The prose is dense but disciplined, the structure is legible (campaign → audit → census, then the
instrument section that supplies the census), and the tables carry their own warnings where a reader
would misread them (the pair-audit caption's "each of 134, not a combined 86.6%"; Table 2's
per-column meaning). Section cross-references all resolve — the compiled PDF has zero "??" and the
log has zero undefined references — and I checked that each `\ref` points at the section the prose
means (the census, the audit, the instrument section, the threats). The LaTeX reads as the markdown
did: I compared the Introduction's bullet list, the oracle table, the twelve-configuration table and
the census table against the markdown source of truth and found no meaning change beyond the
abstract compression noted in W6. Why not Excellent: the "ootnotesize" corruption (W1) is visible in
the shipped PDF in two tables; §4.4 and §4.5 are the densest passages in the paper and a reader who
does not already know the experimental design will need two passes to disentangle levels,
conventions and arms (the `a/b` convention is defined but used at speed, and the nine-arm span
sentence in §4.4 requires the reader to reconstruct which nine arms are meant); and the missing
appendix means the judging prompts themselves — relevant when judging whether the four-perspective
stage was fairly compared — are only in the artifact (Q2).

---

## Questions for Authors

**Q1.** Two `\f` characters in your source were replaced by form-feed bytes (0x0c) during the LaTeX
conversion, so `\footnotesize` is typeset as "ootnotesize" in Table 1 and inside Table 2 of the
shipped PDF. Please restore both commands, recompile, and confirm that (a) no other control byte
remains anywhere in the `.tex`, and (b) the recompiled page count still satisfies the CFP once those
two tables actually shrink.
*Intended effect:* remove the only visible production defect in the submission, and confirm the
compliance claim after the layout change rather than before it.

**Q2.** `haldar25` gives the first author as "Haldar, Reshma" — the author is Rajarshi Haldar — and
hides Julia Hockenmaier behind "and others". Please supply the corrected entry, and while you are in
the bibliography confirm `ddlcheck25`'s page range against the PVLDB record (you print 2281--2293;
the record I found reads 2281–2294) and `agoraplus25`'s year (you print 2026; the TOSEM article
appears to be 2025, with only the companion RCR report in 2026).
*Intended effect:* close the CFP-required reference-integrity check with a list that survives it.

**Q3.** §4.4's joint pricing (32-vs-29, 33-vs-29, the 22/9/1 and 8/2/0 case counts, the symmetric
and asymmetric crediting rules) is described in §4.1 and the README as "printed but not scripted".
It is nevertheless fully reconstructible from the shipped worksheet. Would you either script it —
the worksheet parser is already in `convention_pricing.py` and would take a few lines to generalise
— or state in §4.4 that the material to reproduce those four numbers ships under
`rq2/analyses/pricing/`?
*Intended effect:* make the paper's most contestable numbers as cheap to check as its most
favourable ones, so a skeptical reviewer's cheapest path is verification rather than suspicion.

**Q4.** §4.1 discloses that under the convention eleven of twelve configurations are "credited a
point for a case nobody could judge" (milvus_001). Please state what excluding that case, or
reporting it separately, does to the headline contrast (one case is ≈2 recall points on 51) — the
disclosure is complete but the reader cannot see whether the headline depends on it.
*Intended effect:* pre-empt the "free point" objection by pricing it, as you already do for the
convention and the leak repairs.

**Q5.** The four-perspective contrast against the rule-bearing flat judge changes five things (§4.4).
You have already shown that the schema-line repair alone moves five bugs. Is there a sixth
configuration — or a re-analysis of existing runs — that isolates the remaining four (perspectives,
rule text, red lines, cognition access) even partially? If not, say explicitly which of the five the
paper's conclusion does *not* attribute to the perspective decomposition, so that "the organization
changes which cases are decided, not how many" is not read as a claim about perspectives alone.
*Intended effect:* convert a five-variable contrast into a bounded claim, without new dispatch runs.

**Q6.** On the second backbone by-design refutation closes 50 judgments and is wrong 22 times
(§4.5), i.e. that backbone's error mass sits on the *guarded* clause. Does that mean the guard
itself (verbatim-intent requirement) is the problem rather than its placement — or that the second
backbone's C/D letter confusion makes the clause attribution untrustworthy there? Both readings are
weaker for the paper's advice than "put the guard where the error mass is", and the paper currently
leaves the reader to choose. Please say which reading you intend.
*Intended effect:* close the one place where §5's advice and §4.5's second-backbone result can be
read as contradicting each other.

---

## Answers to Q1–Q6

### Q1 · The LaTeX conversion

I read the `.tex` in full and compared it against `docs/paper-sample-lqm-path.md` at the three places
the question names, and ran two mechanical checks over the compiled PDF.

*Markdown list → `itemize`.* The Introduction's three results (yield / audit / census) and §3.5's
four perspectives are faithful, including the qualifiers that matter: "It carries our own screening
and submission decisions, and the runs that would have measured per-version detection ability were
voided"; "the census is measured on the primary backbone, where the two refuting clauses are
identified by the evidence their cells cite; on the second backbone the pattern does not reproduce
and, because our own dispatch defines the four perspectives twice with C and D exchanged, we cannot
rule out the letters meaning different things there". No claim migrated between bullets. The one
content change I found anywhere in the conversion is the abstract's compression of the case-level
audit result (5/3/2/2 → "acted on all 12"), which is repeated correctly in §1's second bullet and
fully stated in §4.3; the detail was not lost, it was moved (W6).

*Markdown table → `tabular`.* All four tables survive with their numbers and their load-bearing
qualifiers intact. I checked each cell of Table 3 against the shipped `pair_audit.py` output (18
supported, 58 re-anchored, 58 unsupported, 134) and each row of Table 4 against `clause_tally.py`
(61/56/5, 21/17/4, 7/5/2, 50/26/24, 19/17/2, 16/12/4, catch-all 69 = 45 bugs + 24 FPs, total 243).
Table 2's twelve rows match the shipped arm directories one for one. Table 1 (oracles) is a literature
table and its entries are correct for the works named (Q3). The one conversion defect is formal, not
semantic, and it is real: the two mangled `\footnotesize` commands, which print "ootnotesize" under
Table 1's caption and inside Table 2's body in the shipped PDF (W1).

*Cross-reference → `Section~\ref{}`.* The compiled PDF contains no "??" and the LaTeX log contains no
undefined-reference warning; I verified that the labels resolve to the sections the prose means
(`sec:census`→§4.5, `sec:audit`→§4.3, `sec:buys`→§4.4, `sec:method`→§4.1, `sec:threats`→§6,
`sec:baseline`→§4.6). No claim is now attached to the wrong evidence by a mis-pointed reference.

**Verdict on Q1:** the conversion changed no meaning that I can find; it introduced one visible
formatting corruption that must be fixed before submission.

### Q2 · The appendix was removed — is the protocol still assessable from the paper alone?

*What the paper gives you.* §3.5 states the verdict space, the aggregation clause order (contract
confirmation decides; contract refutation with the objective-constraint perspective confirmed routes
rather than closing; otherwise a contract refutation closes to False-Positive; then objective-
constraint confirmation; then cognition; then explicit by-design; then the catch-all), the red lines
(only explicit intent evidence may refute; unsettled cases route), and the four perspectives with
their content. §4.1 states what each control arm's dispatch edits — the exact paragraph that lived
in the deleted appendix — and I verified every clause of it against the shipped dispatch texts (the
schema-fix arm's single-line change; the aggregation arm's three changes; the source-withheld arm's
14→0 `source=` lines; the no-aggregation arm's 2→0 aggregation blocks). So the *protocol* is
assessable from the paper; what is not in the paper is the *prompt text itself*.

*What I would have to open the artifact to check.* Three things, and I did open it to check all
three: (i) whether the flat judge was actually given the same materials minus the organization —
answer: yes, the flat dispatch names the same `materials_complete/*.md` packs and the same source
clones per case, and additionally *forbids* the cognition corpus, so "access to the cognition corpus"
is a real fifth difference; (ii) whether "keeps the protocol's red lines" is accurate for the flat
judge — answer: yes, its terminal rule carries the verbatim-intent requirement and names four of the
seven objective-constraint classes as examples (数值下界 / 枚举闭集 / 互斥 / 类型套套逻辑), which is
exactly what §4.1 claims; (iii) whether the four perspectives are the ones the census attributes
letters to — answer: this is where the deployed dispatch is broken in exactly the way §1 and §4.5
disclose (two perspective blocks with C/D exchanged; two aggregation rules with opposite defaults;
the output schema declaring the source vocabulary in the D slot).

*Is that acceptable?* Yes, with one condition. For a paper whose verification strategy *is* the
replication package, the standard is not "no claim requires the artifact" but "the artifact settles
what the paper asserts, and the paper asserts nothing the artifact contradicts". That standard is met
here, and met unusually well: I checked all three of the above in a single sitting with no
instructions beyond the paper's own pointers, and §4.1's arm-edit paragraph read as a truthful
description of the files. The residual is the *fairness* question the prompt asks about: whether the
four-perspective stage is fairly compared against the flat judge. The paper's own list of the five
differences is the honest answer — it is not a clean comparison, it is a five-variable contrast,
and the paper says so and refuses to attribute the effect to the perspectives alone. A reader who
wants to judge fairness must read the two dispatch texts; both ship per run, so that is one `ls` and
two reads away. The one thing that is *not* fully assessable from the paper is the identification of
the C and D letters, which the paper handles by reading the cells' content (§4.5) — and that
hand-reading is itself only checkable against the frozen verdict files in the package. Given the
artifact ships, I would not hold the appendix's removal against the paper; had the package not been
shipped, this would be a serious problem rather than a note.

### Q3 · The reference list

I verified 18 entries against the real literature (searches, not the `.bib`), chosen to cover every
entry the paper attaches a specific claim to plus a spread of venues and years. In the numbered
reference list (39 entries, `\begin{thebibliography}{39}`):

*Verified correct as to authors, title, venue and year:* `vdbfuzz26` (ICSE 2026; the paper's
"crash-oracle by construction" and "first dedicated VDBMS fuzzer" are both true of VDBFuzz);
`metamon25` (Lee, An, Yoo; LLM4Code 2025, pp. 120–127; the paper's "falsifier is another LLM
question" describes metamorphic prompting correctly); `manyminds25` (Ma et al.; EMNLP 2025 Findings,
pp. 17356–17392; "debate amplifies biases after an initial round while a meta-judge resists them" is
their finding); `molinelli25` (Molinelli, Di Grazia, Martin-Lopez, Ernst, Pezzè; ASE 2025; the
leakage-free benchmark and the near-human-average / unreliable-per-subject contrast are theirs);
`logichunter26` (Long, Zhao, Wang; ISSTA 2026; "treats retrieved documentation as the statement of
intent but consults and executes the implementation freely" is exactly its Agentic Oracle);
`acme26` (Jiang et al.; PACMSE 3(FSE), Art. FSE039; clause mappings via LLMs — correct);
`argus25` (Mang et al.; PACMMOD 4(3), Art. 140; "validating them with a formal prover" = SQLSolver —
correct); `mastor26` (Deng et al.; arXiv 2606.10465; "takes the implementation as its authority" —
correct); `mastest26` (Han, Zhu; AITest 2026, pp. 235–248; correct); `satori25` (Alonso et al.; ASE
2025; OpenAPI-derived oracles — correct); `agoraplus25` (Alonso, Ernst, Segura, Ruiz-Cortés; TOSEM,
doi 10.1145/3726524; traces/execution-derived invariants — correct, but see the year note in W3);
`trace26` (Ulfat, Sabit, Hossain; arXiv 2604.03447; "systematic blind spot when the implementation
drifts while the documentation stays plausible" is their headline finding); `konstantinou24`
(Konstantinou, Degiovanni, Papadakis; arXiv 2410.21136; "oracles capture actual rather than expected
behaviour" is their conclusion); `bodicoat25` (Bodicoat, Jahangirova, Terragni; AIware 2025, pp.
29–39; "prompting technique and supplied context dominate model choice in oracle accuracy" matches
their results); `restinfer22` (Yi Liu; ESEC/FSE 2022, pp. 1816–1818); `ddlcheck25` (Song et al.;
PVLDB 18(7); equivalent-database construction — correct, page-end noted in W3); `norec20`/`tlp20`/
`pqs20`/`buzzbee24`/`dqe23` and the classic oracle line (`peters98`, `zhong09`, `icomment07`,
`docref13`, `tcomment12`, `jdoctor18`, `docter22`, `toradocu16`) are the standard, correctly
attributed entries of this literature — I recognise them from domain knowledge rather than
re-searching each one, and none carries a claim in the paper that is false of the work.

*Problems found:* one wrong author given name and one hidden co-author (`haldar25`:
"Haldar, Reshma and others" should be Rajarshi Haldar and Julia Hockenmaier) — W2; and the two minor
bibliographic details in W3. I found **no fabricated, hallucinated or unlocatable entry** in the
sample, and no case where a claim the paper attaches to a work is false of that work. The specific
attribution claims the question names — Metamon's profile, TRACE's blind spot, Ma et al.'s bias
finding, Molinelli et al.'s per-subject unreliability, LogicHunter's oracle — are each accurate.
(The one caveat: I could not confirm the third decimal of Metamon's 0.722/0.480 against a
publicly visible source; see W3.)

### Q4 · Did last round's repairs land?

All five, verified by recomputation:

**(a) The §4.5 evidence distribution.** Fixed and now exactly right. Of the 19 judgments the census
closes by C=Refuted: 15 cite an in-source comment or docstring; 2 (milvus_026, in two of its three
runs) cite the server's own name-validation rule; 2 (milvus_011 and milvus_012, each in its third
run) rest on code structure — a default expression (`isEmptyExpression → trueLiteral`) and a fallback
chain (the three-level dbName fallback). I read all 19 cells and both cases' other runs; the paper's
account, including the quoted weak-refutation reasons on the other two runs, is verbatim accurate.

**(b) Level-mixing in §8.** Fixed. The recall-level figures are now paired with recall-level
statistics (0.588→0.765 with 9/0, p=0.0039; 0.529→0.804 with 14/0, p=0.0001) and the confirmed-set
contrasts are stated separately (17/0 and 19/0, both p<0.0001).

**(c) The circular Holm family.** Fixed. The family is now defined before the correction as the ten
recall-level tests printed in the paper (16 paired tests appear in total, 10 of them at the recall
level). I recomputed: the ten sorted p-values are 0.0001, 0.0034, 0.0039, 0.0039, 0.0225, 0.0625,
0.2891, 0.4531, 0.6250, 1.0; the first four clear α/10, α/9, α/8, α/7 and the fifth (0.0225) does
not clear α/6. The four named survivors are the four smallest, in order, and the descriptive reading
of the deployed stage's own advantage is stated.

**(d) The unreproducible §4.2 version-overlap count.** Fixed by removing the number. §4.2 now reads
"A substantial share of the 81 adjudicated submissions sits on versions that experiment covered";
the 26/20 version-overlap count no longer appears anywhere in the paper. (Separately verified: the
version counts that *are* printed — 19 ledger versions, 16 for the 81, 15 for the 51 — reproduce
exactly from the shipped ledger.)

**(e) The §4.4 arm ordering.** Fixed. Both halves of the deployed-vs-flat sentence now print the
deployed stage first ("48 vs 34 on the confirmed set (16/2, p=0.0013) and 39 vs 30 at recall (11/2,
p=0.0225)"), which matches the `a/b` convention defined in §4.1 ("a is the arm whose count is
printed first") and matches the script's discordant pairs (16/2 and 11/2, both in the deployed
stage's favour).

### Q5 · Compliance

Measured on the shipped `TestVDB-v10.pdf` (LaTeX log: "Output written … (20 pages)"):

- **Total: 20 pages.**
- **Text + figures: 18 pages** — the body runs pages 1–18, with the last line of the Conclusion at
  content-line 18 of 54 on page 18 (a full page carries 64 content lines). So the text itself ends
  comfortably inside page 18; at most 18 pages are used for text and figures. **Compliant** with
  "at most 18 pages excluding references and the Data Availability statement."
- **Data Availability: page 18, immediately after the Conclusion, before the References. Compliant**
  with "after the Conclusion."
- **References: pages 18–20** — entry [1]–[9] on page 18 (from content-line 29 of 54), [10]–[30] on
  page 19, [31]–[39] on page 20, i.e. roughly 2.2 pages of a 4-page allowance. 39 numbered entries.
  **Compliant.**
- **Double-anonymous: yes.** The title page reads "ANONYMOUS AUTHOR(S)" (acmart `anonymous` option);
  the running heads read "Anon."; the `.tex` contains no `\author`, `\affiliation`, `\email` or
  `\thanks` command; the only URL in the document is the anonymized artifact
  (`https://anonymous.4open.science/r/TestVDB_artifact-EC36/`). No author-revealing URLs or
  acknowledgements. **Compliant.**

One caveat the authors should note: the page-18 margin is thin enough that the W1 fix (restoring
`\footnotesize`, which shrinks two tables) will only help, but any *addition* to §4 or §5 would push
the text onto page 19 and put the claim at risk. The compliance statement should be re-measured after
the fix and treated as binding.

### Q6 · What sinks it now?

**The first objection a hostile reviewer writes** is the convention objection, in this form: *"Your
headline quantitative result — the routing rule raises recall from 0.588 to 0.765 — is definitionally
the routing rate, because your convention counts an abstention as a confirmation. You say so. Under
forced verdicts your replay is a no-op, so the judge's decisions are unchanged and only the
accounting moved. What has been learned beyond how you chose to count?"*

That objection is **not fatal and is largely already answered** — the paper's response is that the
counting convention *is* the finding ("on this pool, what an LLM judge confirms is decided less by
how it is organized than by how it accounts for the cases it refuses to decide"), that the
deployment's ledger does count routed cases (so the convention is the deployment's, not the paper's
convenience), and that both readings are printed for every contrast with the joint hand-priced
reading as a floor (+3, "suggested, not established"). It remains fixable-by-framing only; the
authors have already done most of that framing. The residual risk is that the abstract's first
quantitative sentence will be quoted without its second half.

**The second objection, which is harder**, attacks the census: *"Your own dispatch defines the four
perspectives twice with C and D exchanged and prints two aggregation rules with opposite defaults;
you then ask me to accept a clause census computed with one of those two rules, on one backbone,
where the second backbone does not reproduce — and the only reason the primary census survives is a
post-hoc human reading of 19 cells, two of which show the judge violating its own red line. So the
deployed system, as deployed, cannot actually tell you which clause closed a case."* The paper's
answers are all present (§4.5's content-based identification; the invariance of the load-bearing 24
across both printed rules, both repairs and maintainer-confirmed labels only; the scoping of the
claim to the primary backbone; the replay-not-re-adjudication caveat) — but the answer converts the
contribution from "the protocol guards the wrong clause" to "an auditable pipeline lets you find out
that it does"; that is the paper's own thesis, so the objection lands as a reframing rather than a
refutation. **Fixable only by new data** (a re-adjudication under a verbatim guard, on both
backbones), and the paper says exactly that.

---

## Final Scored Judgement

| Criterion | Score | One-line basis |
|---|---|---|
| Importance & Scope | **Good** | Three production systems, 81 adjudicated cases, 12 configurations, and an audit of every cited pair the judge reads; scope stated with unusual discipline, but the domain is narrow and the campaign yields a record, not a rate. |
| Insights & Evidence | **Good** | Two earned insights (the distillation is the unmeasured step; the guard sits on the already-clean clause), both bounded by the authors in the same paragraphs; the second does not reproduce on the second backbone and the paper says so. |
| Perspective | **Good** | Self-audit, convention pricing and both-readings reporting are exemplary; the message is entirely negative/first-person, and the generalizable advice is a rule of thumb. |
| Verifiability | **Excellent** | I re-ran all five shipped scripts in place and reproduced every printed rate, test and census on both backbones; the two "not scripted" quantities are reconstructible from shipped raw material and I reconstructed them; the §4.1 arm-edit paragraph verifies verbatim against the dispatch files. |
| Presentation | **Good** | Clean structure, tables that warn against their own misreading, all cross-references resolve; the "ootnotesize" corruption in two tables of the shipped PDF and the density of §4.4–§4.5 keep it from Excellent. |

**Overall: Weak Accept.** **Chair's verdict: CONDITIONAL.**

The conditions are mechanical: (1) fix the two form-feed-corrupted `\footnotesize` commands and
re-measure the page split; (2) correct the `haldar25` author entry and re-check the two bibliographic
details in W3. No condition touches a number, a claim or a section of the argument. If the authors
also adopt the Q3/Q4 suggestions (script or point at the joint pricing; price the milvus_001 credit),
the paper's most attackable surfaces are pre-answered at the point of attack.

I would raise this to an unconditional Accept if the artifact's joint-pricing worksheet were wired
into one of the shipped scripts — not because I doubt the numbers (I reproduced them) but because a
paper whose thesis is "audit your oracle, price your convention" is at its most convincing when its
own most contestable number is one command away from a reader.

---

## Method Note — what I recomputed, and how

All artifact work was done in place from the artifact root (`c:\Users\11428\Desktop\TestVDB_artifact`,
HEAD `432459e`) with the shipped Python 3.8.6, no edits to any shipped file, plus throwaway probe
scripts written outside the repository.

**Ran the five shipped analysis scripts.** `rq2/analyses/recompute_paper_numbers.py` (12-arm matrices,
majority/first-run readings, Wilson CIs, confirmed-set and recall-level McNemar, routed queues,
perspective votes), `clause_tally.py` and `clause_tally.py second` (both censuses, rule compliance,
both replays), `convention_pricing.py` (convention/forced/joint bounds, the three blind passes and
κ), `bootstrap_net_f1.py` (net and F1 with 95% CIs), `audit/pair_audit.py` (the 134/18/58/58 pair
split and the 12 case-level assertions). Every figure compared against the paper matched.

**Recomputed the two quantities the README declares unscripted.** Catch-all composition over the 69
rule-mandated catch-all judgments (37 source-vocabulary D cells = 53.6%, 28 on true bugs; 32
rule-defined D cells, 17 on true bugs = 53.1% against a 63.0% base rate) using `clause_tally.py`'s
clause function; joint pricing of the headline contrast from `analyses/pricing/HR17_adjudication_worksheet.md`
plus the frozen verdicts (control 32 vs flat 29, deployed 33 vs 29, decisive-routed counts 22/9/1 and
8/2/0, symmetric +4, asymmetric +5).

**Probes over the raw shipped material.** The ledger xlsx (132 rows for three systems; 81 = A∪B∪C;
49 D + 2 excluded self-PRs; 19/16/15 versions; per-system and per-outcome splits; the single
crash-or-panic row, qdrant #9045). Per-arm `milvus_001` routing (11 of 12 arms credit it; contract
core never does). Three-way-split cases and the strict-majority variant (37/51). The 19 C=Refuted
closing cells classified by their recorded evidence, plus milvus_011/012 across all three runs. The
rule-departure count (22 forward = 17 forced-False-Positive + 5 Confirmed, 10 of the 17 on true
bugs; exactly one reverse, milvus_019 run 1). Pre-repair states: deployed 41+6, contract refutation
47 / by-design 20, control arms' TP-set invariance and FP +2/+1, suppression 0.467→0.400 and
0.933→0.900, forced 30→31; the six re-judge files' 19 rewritten verdicts (15 toward, 4 no-op, 0
away). The first repair's pre-state directories (13 `_pre_cogstrip_merge/`, matching §4.1's
nine-plus-three-plus-one) and the 12 `_pre_coganchor` files. Arm dispatch facts by diff: the eight
binary-schema arms with three-valued prose vs the three three-valued arms and the truly binary
contract core; the flat judge's four-of-seven objective-constraint classes; the two aggregation
blocks and two perspective blocks in the deployed dispatch, and the output schema's source
vocabulary in the D slot. RQ3 log counts over the shipped directory (205 per-template logs + master;
11,629 response-status lines and 1,127 stage completions per-template, exactly doubled directory-wide
by the echo; 152 "3 anomalies" lines across 119 logs; 50.75 minutes wall time from first/last
timestamps).

**LaTeX/PDF checks.** Full read of `TestVDB-v10.tex`; byte-level scan for control characters (two
0x0c); `pdftotext` extraction and string search for the corrupted command (2 hits);
`grep` of the LaTeX log for undefined references (0) and "??" in the PDF text (0); page-by-page
extraction for section placement and page-split measurement; bibliography check of 39 numbered
entries and web verification of 18 of them (including every work the paper attaches a claim to).

**Not verified, and why.** The fix-PR characterisation in §4.2 (explicitly marked as outside the
shipped artifact); the expectation-framing census in §4.3 (single-reader, not scripted — my
independent phrase scan is consistent with the paper's account but cannot reproduce its 19-hit count);
the fidelity of the two model backbones and their sampling (aliases without pinned weights, stated as
a limitation); the third decimal of Metamon's precision/recall figures (W3).


