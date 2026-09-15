# Reviewer 3 — General Reviewer

## What I am, and am not, qualified to assess

I am a software-engineering reviewer without specialism in LLM judging, documentation-based testing,
or vector databases. I can assess: the paper's argument and its internal consistency; whether its
numbers are checkable and whether they check out; experimental hygiene; and whether a non-specialist
can follow it. I cannot assess: whether the characterisation of the VDBMS bug landscape in §1–§2 is
fair to that literature; whether the characterisations in §7 of AGORA+, SATORI, MASTOR, MASTEST,
Metamon, LogicHunter, Argus and the rest are accurate (I did not read those papers); whether the
134 citation-level classifications in §4.3 are individually right (I checked only their aggregate);
and whether Milvus/Qdrant/Weaviate document the constraints the paper says they document.

This round the object is the LaTeX submission. I read `TestVDB-v10.tex` in full (997 lines; the
compiled PDF is 20 pages, which I confirmed from `TestVDB-v10.log` and by paging the PDF). I also
re-ran five of the artifact's analysis scripts from the local replication tree
(`C:\Users\11428\Desktop\TestVDB_artifact`) — `clause_tally.py` (both backbones), `audit/pair_audit.py`,
`convention_pricing.py`, `bootstrap_net_f1.py` and `recompute_paper_numbers.py` — and every number of
the paper's that I checked printed exactly as the paper states it. I did **not** attempt to reach the
anonymized URL, and where a statement is about the shipped snapshot rather than the local tree I say
so. I measured sentence lengths myself with a small script; where a count below is mine I give the
method, because my own counts are as prone to error as anyone's.

---

## Overall Recommendation

**Weak Accept** — chair's verdict **CONDITIONAL**.

Every fixable objection I raised last round has been addressed, and one of them (the level-mixed
statistics in §8) was the one I said stood "exactly where the paper is asking to be trusted most".
The round's conversion also cost the paper its appendix, and the six questions asked of me this
round are mostly about what that cost. My answer is that the paper still stands on its own for
*what was measured* and *what was held constant* — better than before, because §4.1 now says what
each control edits — but that the verbatim instructions are now only in the package, and one control
claim (the discipline every judge ran under) has left the paper entirely. What keeps the score at
Weak Accept rather than Accept is unchanged from last round and is not a correctness problem: the
paper's central prescription is a replay whose measured value under the authors' own honest reading
is zero, on one backbone, and the ~15-case re-adjudication that would convert it from "a replay" to
"a measured prescription" has not been run.

---

## Summary

The paper reports three artefacts. A mining campaign that produced 51 maintainer-confirmed
documentation–implementation bugs across Milvus, Qdrant and Weaviate with 23 merged fixes (§4.2);
an audit of the evidence packages the confirmation stage reads, finding 18 of 134 (constraint,
cited-page) pairs supported as cited, 58 re-anchored and 58 unsupported by the page they cite
(§4.3); and a census of the deployed confirmation stage's 243 judgments by the clause that closes
them, locating most of the stage's false-positive closures in the one refuting clause its protocol
does not guard (§4.5). §4.4 supplies the instrument: twelve frozen judge configurations over the
same 81-case pool, contrasted under two counting conventions, with the four-perspective null result
(organisation changes *which* cases are decided, not how many) and the deferral result (the routing
rule moves recall only because a routed case counts as confirmed).

This round I re-verified the instrument's numbers, the census table on both backbones, the two
replays, the net/F1 intervals and the adjudication agreement statistics against the local artifact
tree; all reproduced. The claims are now assembled in one findable place (the abstract's three
labelled paragraphs, echoed by §1's itemised list and contributions) and the levels of every printed
contrast are labelled where they are printed.

---

## Core Strengths

**S1. The numbers verify, and the ones that mattered most last round now verify too.** Running the
five scripts named in §4.1 from the artifact root reproduced, cell for cell: §4.5's census table on
the primary backbone (61/56/5 at 0.92, 21/17/4 at 0.81, 7/5/2 at 0.71, 50/26/24 at 0.52, 19/17/2 at
0.89, 16/12/4 at 0.75, catch-all 69, total 243); the same table's second-backbone version (A=Refuted
56, C=Refuted 50 of which 22 wrong, 24 of 48 incorrect closures = 50% rather than 80%, D-cells
carrying the source vocabulary 217 of 243, and three A=Refuted-with-B=Confirmed cells where the
primary has none); the compliance paragraph (17 judgments forced to False-Positive against the rule
and the red lines mark them, 5 to Confirmed, 10 of the 17 on true bugs); both §4.5 replays (39/51 →
43/51 with suppression 21/30 → 19/30; 39/51 → 46/51 with 21/30 → 12/30; both no-ops forced); §4.3's
pair audit (134 = 18 supported 13.4% / 58 re-anchored 43.3% / 58 unsupported 43.3%, and the case
level 5 supported, 3 unsupported, 2 weak-evidence, 2 over-strong = 12); §4.4's levels (39/51 at
suppression 21/30 convention, 27/51 at 27/30 forced, flat judge 30/51, flat+schema 35/51,
rule-bearing 39/51, no-source 48/51, the second backbone's 27→41, the equal forced figures 27/27 and
26/26, the spans [23,31] forced and [27,48] convention); the net/F1 comparison (net +0, 95% CI
[−8,+8]; F1 0.788 with source against 0.821 without, difference +0.033, CI [−0.044,+0.115]); and the
independent-pass agreement (4/20, 5/20, 6/20 with κ = −0.01, 0.08, 0.11, two of three statements
landing at the forced floor). §4.1's "sixteen paired tests appear below, ten of them at the recall
level" also checks: I count exactly sixteen printed p-value expressions in §4, ten of them on a
recall-level test.

**S2. The appendix cut was done the right way round.** The material that had to survive did: §4.1 now
carries a paragraph naming what each control edits ("The schema-fix arm changes only the flat
dispatch's output-schema line ... The source-withheld arm drops the `source=` path from every
per-case material line of the full-stage dispatch"), placed immediately beside Table 2, where a
reader meets the configurations. Four navigational sentences were added in the same commit
("Figure 1 shows the four stages", "Table 2 lists the twelve", "Table 3 gives the three-way split",
"Table 4 is grouped by the outcome each clause assigns") and the abstract was trimmed in two places
rather than in the sections that carry the claims. Reading the paper end to end, I never wanted to
flip to an appendix for the *design*; I only wanted it twice, for the prompt texts (Q1 below).

**S3. The claim set is now in one place, and it is the abstract.** This is the thing I asked for two
rounds ago and last round said I could not find. The abstract's three bold-labelled paragraphs
("The campaign", "The audit", "The census") state the surviving claims one by one, and each carries
its scope in the same breath: "It is a record of submissions and adjudication, *not* a per-run
detection rate: the runs that would have measured detection ability were voided for
dispatch-discipline violations, and nothing here depends on them"; "measured on the primary
backbone, where the perspectives are identified by their content, and not reproduced on the second";
"Routing contract refutation instead of closing on it recovers seven true bugs for nine
false-positive interceptions under the deployment's convention, and nothing under the forced
reading". §1's itemised list and contribution list restate the same three, and §8 repeats the
caveats. A reader can now answer "what does this paper claim?" from page 1.

**S4. §4.5's robustness arguments are the right ones, and they hold up.** The load-bearing count (24
of 50 contract-refutation closures falling on maintainer-confirmed bugs) rests on maintainer labels
only, so it does not depend on the 30 negatives the authors adjudicated themselves; it is invariant
across the two aggregation rules the dispatch prints because contract refutation assigns
False-Positive under both; and the paper discloses the pre-repair alternative (47 and 20) rather than
quietly reporting the cleaned numbers. The C row is identified by content rather than assumption —
the paper reads all nineteen of its cells and reports what each rests on, including the two that rest
on code structure alone and therefore do not meet the clause's own red line. That last disclosure is
against interest and it is new; a weaker paper would have reported the row's accuracy (17 of 19) and
stopped.

**S5. The honesty is still load-bearing rather than decorative.** The four dispatch defects are
reported in §1, §5 and §6 ("**None of the four was found by our own audit**; all were found by
reviewers reading the shipped texts"); §4.2 states the fix-PR characterisation sits outside the
shipped artifact and marks the claim accordingly; §4.1 states which values are printed but not
scripted; §4.6 discloses the 152 lines that look like anomaly reports before a reader finds them. In
each case the admission is quantified and attached to its consequence. This remains, for me, the
paper's most distinctive quality.

---

## Core Weaknesses

**W1. [major, fixable] The census's prescription is worth nothing under the reading the paper calls
honest, and the pattern it rests on reverses on the second backbone.** §4.5: "**Forced, the same
replay changes nothing** (27/51, 27/30, and the confirmed sets are identical), because an abstention
and a closure score the same there." §4.5's opening: "the same census on the second backbone does not
reproduce the pattern ... **50% rather than 80%**." So the third leg of the title is a one-backbone
descriptive count whose remedy is priced in the currency the paper simultaneously says is not a
measurement of the judge. The paper says all of this itself, in the abstract, §4.5, §5, §6 and §8, so
this is not an undisclosed problem — but it is the reason I cannot yet call the paper Accept: the
thing a reader would take away ("guard the clause that closes wrong") is, by the authors' own
account, a change to how cases are *counted* rather than to how many bugs the stage finds. Fixable
only by running the ~15-case re-adjudication under a verbatim guard, which §4.5 itself names as what
frozen data cannot compute.

**W2. [minor, fixable] §8 prints the discordant pairs of the headline contrast in the opposite order
to §4.4, for the same tests.** §4.1 fixes the convention: "Discordant pairs are written *a/b*, where
*a* is the arm whose count is printed first in the comparison being reported." §4.4 prints the
bundled contrast as "30→39 at the recall level (0/9, p=0.0039)" — rates flat-first, pairs
flat-first, consistent. §8 prints the same test as "(0.588 to 0.765, 9/0 at the recall level,
$p{=}0.0039$)" and the second backbone as "14/0" where §4.4 has "0/14". The p-values match, so this
is labelling rather than arithmetic; but the conclusion is where a reader is asked to take numbers on
trust, and this is the second consecutive round in which the conclusion is the one place where the
levels and the order of a contrast go wrong (last round it was the level, which is now fixed).

**W3. [minor, fixable] "Suppression" is used five times and never defined, and the one sentence that
prices the leak repair uses "false-positive count" in the direction opposite to it.** §4.1: "the
arms' true-positive sets are unchanged (48 and 33) while their false-positive counts rise by two and
one---suppression $0.467\to0.400$ and $0.933\to0.900$". I checked the arithmetic: the intercepted
counts are 14/30 → 12/30 and 28/30 → 27/30, i.e. the arms' *confirmed* false positives rise (16→18
leaked, 2→3 leaked) and their interception falls. The sentence is coherent once decoded, but
"suppression" and "false-positive count" point in opposite directions in the same clause, and
"suppression" is never glossed, though it carries five printed values (21/30 and 27/30 in §4.4, 12/30
in §4.5, and the two ranges in §4.1). One clause at first use ("suppression: the share of the 30
negatives the arm does not confirm") fixes it.

**W4. [minor, fixable] The sentence that promises the prompts is now the only place they are
mentioned, and it is imprecise twice.** §4.1: "All dispatch texts, and English renderings of the two
judging prompts, ship verbatim in the artifact." First, "the two judging prompts" has no antecedent
in the paper any more — the removed appendix named them (the full-stage protocol and the flat
judge); a reader now has to infer which two. Second, in the local artifact tree I inspected, the
per-arm dispatch files that instantiate those prompts are in Chinese (I measured one: `run_flat1/
batch1_dispatch.txt`, 3,321 characters, 506 CJK; `run1/batch1_dispatch.txt`, 1,925 characters, 276
CJK), and I could not find an English rendering of either prompt anywhere in the tree (a search for
the flat prompt's own phrases found only the README's arm table). If the anonymized snapshot carries
files this tree does not, the sentence is fine and this paragraph is withdrawn; if it does not, the
sentence over-promises and — worse for the project — the English renderings of the prompts existed
only in the appendix the page limit forced out. Given this project's history of package/paper drift,
this one is worth a ten-minute check before submitting.

**W5. [minor, fixable] The abstract has stopped mentioning the paper's own answer.** §8 states the
paper's finding twice in the first person: "the answer on this pool is not the judge's internal
organization", and "what an LLM judge confirms is decided less by how it is organized than by how it
accounts for the cases it refuses to decide." Neither sentence has a counterpart in the abstract,
whose three paragraphs cover the campaign, the audit and the census. The abstract is not wrong; it is
missing the one result §8 leads with, and the four dispatch defects the abstract carried last round
were also cut (they survive in §1, §5 and §6). A reader of the abstract alone would not know that the
paper's headline is about *deferral*, even though §8 says it twice and §4.4 carries the numbers it
rests on (forced-verdict recall 25→27 on the primary, 23→26 on the second).

**W6. [minor, fixable] Density: §4.4 and §4.5 are the same wall of qualified quantities as last
round, and longer than the appendix that was cut to make room.** I measured the sentences I quote in
this review: §7's Ma et al. sentence runs **90 words**; §4.1's leak-repair sentence **80**; §4.4's
"Across the nine judging arms …" **76**; §3.5's aggregation-rule sentence **75**; §4.5's "The
nineteen judgments this census closes by C=Refuted …" and "But the last two are the weaker kind …"
**74 each**. Across the body prose (tables excluded, abbreviations and decimals protected, my own
crude splitter), I count 340 sentences of five words or more with a median of 27 and **17 sentences
of 70 words or more**. The new §4.1 paragraph is itself seven sentences in ten lines, one of them
46 words. This is my own count on my own splitter, so treat it as an order of magnitude rather than a
specification; the point is that the passages a reader must read most carefully — the two sections
that carry the paper's claim — are the passages with the longest sentences, and neither gained a
single short sentence this round.

**W7. [minor, fixable] Two small residuals from last round's list.** §7 still says "the twelve frozen
configurations below" when they are two sections above (§4.1) — flagged last round and unchanged.
And §4.5's breakdown of the nineteen C=Refuted cells (fifteen comment-or-docstring, two server rule,
two code structure) is a hand reading that no script prints — `clause_tally.py` prints the C row's
accuracy but not this classification — while §4.1's list of "printed but not yet scripted" values
does not name it. It is the census's most self-critical number; either script it or add it to that
list.

---

## Detailed Assessment

### 1. Importance & Scope — **Good**

The problem is real and correctly framed for a general reader: §1–§2 explain why a class of bugs that
does not crash is out of reach of the one dedicated fuzzer, and the two worked examples (Milvus
#49823 as a single-response boundary violation; Qdrant #10369, which needs a delete-and-recreate
transition to become observable) make the class concrete without domain training. The empirical asset
is substantial: 51 maintainer-confirmed bugs with 23 merged fixes across three production systems,
recorded with its provenance ("It is **not** a per-run detection rate, and we cannot supply one").
The scope limits are stated rather than hidden: submission-filtered pool, no inter-annotator study,
one case unjudgeable and credited to eleven of twelve configurations under the convention (§4.1, §6).

What keeps this from Excellent is the same thing as last round: the *measurement* scope is narrower
than the framing. One domain, one task, one pool, and the experiment that would have made detection
ability measurable was voided by the authors' own review. What remains are contrasts on a frozen
pool, which §6 correctly calls "contrasts on a common pool, not operating performance". That is a
legitimate thing to publish; it is a smaller thing than the title's "mining campaign" phrasing
suggests to a reader who does not reach §6.

### 2. Insights & Evidence — **Good**

The transferable insight is §4.3's: every pipeline in this line distils documentation and then
judges against the distillation, and nobody measures the distillation. The measurement is concrete
and reproduced for me by the shipped script; §4.3 also exhibits the right self-scepticism ("we are
not claiming these rates as properties of LLM distillation in general") and names the two mechanisms
behind the unsupported pairs (version drift, conceptual-only documentation). The second insight —
§4.5's "The protocol guards the clause that is already clean" — is the paper's most quotable finding
and the paper does the hard part of defending it: the load-bearing count is computed on maintainer
labels, is invariant across the two printed aggregation rules, and survives the two leak repairs.

Why not Excellent, unchanged from last round: the census is a single-backbone result by the paper's
own admission, its counterfactual is a replay rather than a re-adjudication (the paper names this as
what frozen data cannot compute), and under forced verdicts it is a no-op. Meanwhile §4.3's audit
finding stands on its own and would survive the census being dropped — which is a healthy sign about
which leg is load-bearing, and also the reason I would not elevate the criterion on the census's
strength alone. The evidence packaging is, as last round, unusually good, and the fixes to §8's
statistics and §4.2's uncheckable number removed the two places where the packaging had holes.

### 3. Perspective — **Good**

The paper has a point of view and it is not self-serving: an LLM judge is expected to over-report,
the protocol keeps the over-reporting visible in a review queue rather than suppressing it at the
cost of discarding defects, and the paper then measures what that design position costs and buys
(§3.5, §4.4, §4.5). The Discussion's four lessons are prescriptive without overselling — "audit what
your oracle reads, not only what it concludes", "put the evidence guard where the error mass is",
"price the deferral channel, and price the contrast, not just the level", "check the dispatch before
you re-architect the judge" — and the last is backed by four defects the authors found in their own
dispatches, one of which moved five of the headline nine bugs. That is the strongest possible
illustration of the paper's own methodological claim, and §7's closing position ("what this paper adds
to the line is not a new oracle but an audit of the oracle's *input*") is the right claim for this
paper.

Two things keep this from Excellent. First, the paper's stance of "we privilege neither reading" is
maintained so carefully that the reader must infer which reading the authors would defend; §4.4's
"At the reading this paper considers honest, the deployed change is suggested, not established"
finally says it, but only in the third of that section's six blocks (I measure §4.4 at 883 words with
tables excluded). Second, §8's register loosens where
§4.5's is precise: §4.5 says by-design refutation is "the middle of the three clauses that assign
False-Positive" (19, against cognition's 16 and contract refutation's 50), while §8 generalises to
"the clause that closes the most judgments" — which is not true of the census table as printed, where
B=Confirmed assigns 61 closures. The same loose formula appears in §5. This was in my last round's
list and is still there.

### 4. Verifiability — **Excellent**

This remains the criterion the paper earns outright, and I verified it rather than taking the
declaration on trust: five scripts, run from the artifact root with no edits, reproduced every number
I list in S1 — the census on both backbones, both replays, the compliance counts, the pair audit, the
levels and contrasts with their discordant pairs and intervals, the κ statistics, and the per-arm
majority matrices. The declared package contents match the local tree: `rq2/materials` holds the 81
frozen packages, `rq2/pool` the pool, `rq2/verdicts/run_*` the per-run outputs for all twelve arms
plus their `_pre_cogstrip_merge` backups for the re-judged runs, and `rq2/analyses/pricing` the
adjudication worksheet and the three blind passes. The paper is also now explicit about what is
*not* scripted (the joint prices, the catch-all composition, the expectation-framing check), which is
the right way to declare a boundary; my only addition to that list is §4.5's C-cell classification
(W7).

Two residual qualifications, neither of which changes the score. First, the one artifact-content
claim I could not confirm (W4: the English renderings of the two prompts), which is precisely the
class of drift that has bitten this project before — and which matters more now that the appendix is
gone. Second, I cannot see the anonymized snapshot; if it lags the tree I inspected, the numbers I
reproduced are the tree's, not the snapshot's. The paper could make that failure mode visible the way
§4.1 makes the other ones visible, by naming the artifact revision the package corresponds to.

### 5. Presentation — **Good**

The organisation is defensible and the tables carry the load: the oracle-family table in §2, the
twelve-configuration table in §4.1, the pair-audit table in §4.3 and the census table in §4.5 each
answer their section's question in one screen, and this round added the cross-references that tell a
reader so. Section numbering is coherent and the paper repeatedly tells the reader which of two
readings it is reporting as it goes.

What costs it the higher band is density and level-discipline, both measured in W6 and W2. On Q3 of
this round — better or worse to read than last round? — **better, modestly**. The appendix's removal
did not leave a hole in the design description (§4.1's new paragraph is in the right place and its
seven sentences are traceable to the arm table beside them), the four added cross-references are
genuine navigational help, and the abstract's two trims made page 1 easier. What is worse is
localised and real: the reader who wants to know exactly what instructions the judges received now
has to open the package and read Chinese, and the paper's own list of what each judge was *given*
(identical pack and clone, no network, cases judged independently) has left the paper with the
appendix — I could not find that statement anywhere in the body. Density in §4.4–§4.5 is unchanged;
those two sections still read as a ledger rather than as prose.

---

## Questions for Authors

**Q1.** §8 prints the headline contrast as "(0.588 to 0.765, 9/0 at the recall level, $p{=}0.0039$)"
and §4.4 prints the same test as "30→39 at the recall level (0/9, $p{=}0.0039$)". Given §4.1's
definition of the pair order, which is intended? *Intended effect:* make the conclusion's numbers
readable under the same convention as the body, so that a reader who checks one against the other
does not have to decide which of the two is mislabelled.

**Q2.** Will the paper define "suppression" at first use, and re-word §4.1's sentence so that the
direction of "false-positive counts rise" cannot be read as the direction of "suppression falls"? My
recomputation says the arms' *confirmed* false positives rise (16→18 and 2→3) while their
interception falls (14/30→12/30 and 28/30→27/30), which is what the sentence means, but the two terms
sit three words apart pointing opposite ways. *Intended effect:* remove a trap that a reviewer who
checks the arithmetic will otherwise mark as an error, and give the suppression numbers a definition
a reader can carry.

**Q3.** Which two prompts does §4.1 mean by "the two judging prompts", and do English renderings of
both ship in the artifact? The removed appendix named them and carried their text; the body of the
paper no longer does either. In the local artifact tree I inspected, the per-arm dispatch files are
Chinese and I could not find an English rendering. *Intended effect:* fix a dangling reference on the
one page that promises what a reader will find in the package, and confirm that the promise is true
of the snapshot you will ship — this project has been bitten twice by exactly this class of drift.

**Q4.** Will §4.5's classification of the nineteen C=Refuted cells (fifteen comment-or-docstring, two
server rule, two code structure) ship as output, or be added to §4.1's list of printed-but-not-scripted
values? It is the number that shows the paper's own guarded clause was not applied uniformly, so it is
the one a sceptical reader will want to check. *Intended effect:* keep the census's most
self-critical claim verifiable by the same route as the rest of the census.

**Q5.** Does the paper want the abstract to carry §8's answer — that what moves the outcome is how
often the judge declines to decide, not how it is organised? The abstract's three paragraphs cover
the campaign, the audit and the census, and a reader who stops there never learns the finding the
conclusion leads with. *Intended effect:* make the abstract and the conclusion point at the same
headline, and stop a reviewer from having to infer which of the paper's three legs the authors
consider the finding.

**Q6.** Is the ~15-case re-adjudication of contract refutations under a verbatim-evidence guard
planned, or is the replay the final form of the prescription? §4.5 names it as what frozen data
cannot compute, which is exactly the one thing a decider will ask for. *Intended effect:* let the
committee know whether the prescription is measured or replayed — and, if it is to be run, get the
one experiment that would convert the census from a description of the accounting into a change to
the judge.

---

## Answers to the round's six questions

### Q1 — Does the paper still stand without its appendix?

**Short answer: yes for what was measured and what was held constant, no for what the judges were
handed — and I would name two things rather than one.**

*What was measured*, from the paper alone: the object is stage (iv), the bug-confirmation stage
(§3.1, Figure 1); §4.4 varies its evidence access and its internal organisation across twelve frozen
configurations; §4.5 counts where its 243 recorded judgments close and prices one counterfactual. I
can say all of that without the appendix.

*What was held constant*: the 81-case pool; the per-case packages, "frozen per case ... the judge
configurations in Section 4 read the same packages. Whatever a configuration concludes, it concluded
from the same material as the others" (§3.1); three runs per configuration with a stated majority rule and
a stated tie consequence (§4.1: "under a rule that demanded two identical verdicts the deployed
stage's recall would be 37/51 rather than the 39/51 we report"); and — thanks to this round's addition
— the exact edit each control arm makes to its parent dispatch (§4.1). That last paragraph is what
makes the experiment describable in the paper rather than in an appendix, and it is a real gain.

*What the judges were given*: at protocol level, yes — §3.5 gives the four perspectives (A contract
run mechanically, B the seven objective-constraint classes named, C behavioural elegance refuting
only on verbatim intent evidence, D maintainer cognition), the verdict space, and the aggregation
order clause by clause; §4.1 adds the red lines the flat judge keeps and the four of seven classes it
carries as examples. At wording level, no. The verbatim instructions, and the aggregation clause as
restated for a judge without perspective labels, are no longer in the paper at all.

**What is now only in the package, and whether it changes what I can conclude:**

1. *The two prompt texts themselves (English renderings, with the Chinese originals authoritative).*
   Their absence does not change what I can conclude about the census or the audit; the next item
   does.
2. *The re-stated aggregation clause handed to the rule-bearing control.* This one matters. The
   paper's title contrast is "flat judge → rule-bearing judge" (30→39 recall, 9/0, $p{=}0.0039$
   primary; 27→41, 14/0, $p{=}0.0001$ second), and §4.4 tells us that the *test of the perspective
   contrast* has to treat "the aggregation rule text" as one of the five things that differ, "since a
   perspective-free judge cannot carry an A/B/C/D clause table". So the paper itself says a
   perspective-free judge gets a differently-worded rule. Whether that differently-worded rule is
   *content-equivalent* to the deployment's is a claim the reader can no longer check in the paper,
   and the appendix used to state it ("the same three outcomes and the same default"). I can accept
   the contrast without it — the arm is a traceable edit and the paper says so — but I cannot verify
   that the control's rule is the deployment's rule, which is the whole point of the contrast.
3. *The discipline every judge ran under.* The appendix said it in one sentence: "Each judge
   receives the same per-case materials---the frozen evidence pack and the case's version-pinned
   source clone---under identical discipline clauses (own pack and clone only, no network access,
   cases judged independently)." I grepped the body: nothing states it (no occurrence of "network",
   "isolation", or an independent-judging clause anywhere in the .tex). For a study whose claim is
   that contrasts are on a common pool, "how were the judges kept comparable" is a design fact, not a
   detail; one sentence in §3.5 or §4.1 restores it.

Nothing else that I wanted was missing. The seven objective-constraint classes are named in §3.5, the
verdict vocabulary is defined, the cognition corpus's role is stated, and the counting conventions are
defined in §4.1 where they are first used.

### Q2 — The claim set

**It is now assembled, and the place is the abstract.** The sentences that decide it:

- "**The campaign.** Across Milvus, Qdrant, and Weaviate, maintainers confirmed 51 of 81 adjudicated
  submissions as real bugs and fixed 23 through merged PRs. The ledger records 132 rows ... It is a
  record of submissions and adjudication, *not* a per-run detection rate: the runs that would have
  measured detection ability were voided for dispatch-discipline violations, and nothing here depends
  on them."
- "**The audit.** ... 18 are supported as cited, 58 cite a source file or a landing page rather than
  the page that documents the constraint and were re-anchored, and 58 have no support on their cited
  page---43.3%. Two leak repairs followed from the same audit and are load-bearing ... and **every
  rate below is computed on the cleaned pool**."
- "**The census.** ... Contract refutation, which carries no evidence requirement, closes 50
  judgments and 24 of them are maintainer-confirmed bugs; by-design refutation ... closes 19 and is
  right 17 times. **80% of the stage's incorrect closures to False-Positive come from the unguarded
  clause.**"
- and the scope sentence inside the same paragraph: "measured on the primary backbone, where the
  perspectives are identified by their content, and not reproduced on the second."

§1's itemised list restates the same three with the same scoping, and contribution 3 scopes the
census again. A reader no longer has to combine sections to find the claims, which is what I asked
for two rounds ago and what I said was missing last round. The *surrendered* claims (no detection
rate; no four-perspective advantage; the deployed change "suggested, not established"; no
generalisation beyond the primary backbone) are still spread across §4.4, §4.5, §6 and §8 rather than
sitting beside the claims — one sentence in §1 naming them would close that gap, but the positive set
is now findable, which was the question.

### Q3 — Density

**Better to read than the version I reviewed last round, modestly and for identifiable reasons — but
the two sections that carry the claim are as dense as before.**

What improved: (i) §4.1 now names what each control edits, in seven sentences, next to Table 2, so a
reader no longer has to reconstruct the arm design from the contrasts; (ii) four cross-references were
added ("Figure 1 shows the four stages", "Table 2 lists the twelve", "Table 3 gives the three-way
split", "Table 4 is grouped by the outcome each clause assigns"); (iii) the abstract lost two clauses
(the twelve case-level assertions, the four dispatch defects) that were carried in the body anyway;
(iv) the appendix is gone, so there is no second place to look. What got worse: the reader who wants
the judges' instructions now has only the package, and the sentence that promises them ("English
renderings of the two judging prompts") is itself one of the harder ones to parse, because "the two
judging prompts" is never explained.

The density I measured, all of these from the body prose with tables excluded and em-dashes not
counted as words:

- §7, the Ma et al. sentence: **90 words** — "The closest work to ours is Ma et al. ... on a second
  backbone it costs recall rather than buying it." It carries a comparison, a premise, a reproduction
  and a backbone caveat in one sentence; it is the longest I found anywhere in the paper.
- §4.1, the leak-repair accounting: **80 words** — "It does not move the two controls in our favour
  either: of the nineteen verdicts the six re-judge files rewrite, fifteen move a case toward
  confirmation ... and on the forced reading the no-source arm's recall rises by one, to 31." This is
  a sentence with four clauses of numbers, and it is the paragraph that asks to be trusted about the
  authors' own repair.
- §4.4, "Across the nine judging arms ...": **76 words**, listing six arms and two ranges and two
  baselines.
- §3.5, the aggregation rule: **75 words**, seven ordered clauses in one sentence. Here I think the
  density is *earned*: the rule is ordered, and the sentence mirrors the order.
- §4.5, "The nineteen judgments this census closes by C=Refuted ..." and "But the last two are the
  weaker kind ...": **74 words each**.

Across the whole body (tables excluded, abbreviations and decimals protected, split on sentence-final
punctuation; my own splitter, so an order of magnitude rather than a specification) I count 340
sentences of ≥5 words, median 27 words, with 17 sentences of ≥70 words. Note what those numbers say:
the *median* is comfortable. The problem is not that every sentence is long; it is that the longest
ones cluster where the paper is most careful and most qualified — the leak repair, the arm summary,
the C-cell reading — so a reader who slows down only where the paper is being honest ends up slowing
down constantly. Splitting four or five of those into two sentences each, with the number in a second
sentence, would cost a few lines and buy a lot.

### Q4 — Over-claimed or under-claimed

**The abstract does not over-promise: I checked every number in it against the body and the artifact
and all of them are delivered.** The campaign paragraph's 51/81, 23 fixes, 132 rows (81 + 49 + 2) and
19 versions are §4.2's; §4.2's per-system split also reconciles (Milvus 43 = 29 + 14, Qdrant 28 = 14
+ 14, Weaviate 10 = 8 + 2; 43 + 28 + 10 = 81, 29 + 14 + 8 = 51, 11 + 9 + 3 = 23). The audit
paragraph's 134 = 18 + 58 + 58 with 43.3% is §4.3's table and the script's output. The census
paragraph's 50 and 24, 19 and 17, 80% (24 of the 30 incorrect closures to False-Positive: 24 + 2 + 4)
and the seven-for-nine counterfactual are §4.5's, and the scope qualifier is attached in the same
paragraph.

**What the abstract has stopped mentioning, and whether a reader would want it:**

1. §8's answer. The conclusion's first person ("the answer on this pool is not the judge's internal
   organization"; "what an LLM judge confirms is decided less by how it is organized than by how it
   accounts for the cases it refuses to decide") has no abstract counterpart. A reader who reads only
   the abstract learns that the paper has a census leg, not that the census leg's headline is about
   deferral. This is the one mismatch I would fix.
2. The four dispatch defects. The abstract carried "Four defects in our own dispatches were found by
   reviewers reading what we shipped" until this round, and that clause was cut. The body keeps the
   full account (§1, §5, §6). Cutting it is defensible on space grounds; I note it because it was,
   for me, one of the paper's distinguishing features, and because the sentence that remains in §5
   ("A one-line schema repair moved five of the headline nine bugs") is doing self-critical work that
   the abstract now never signals.
3. §4.6's baseline result (0 oracle anomalies from the released VDBFuzz configuration, bounded to
   that configuration) was never in the abstract and is not there now. It is a supporting study, so
   this is a note rather than a complaint.

No sentence in the body, as far as I could check, has been left claiming more than the abstract
promises or less than the artifact supports.

### Q5 — Compliance, as a reader

Reading the compiled PDF as a submission rather than as a draft, it looks compliant:

- **Double-anonymous.** `\documentclass[acmsmall,screen,review,anonymous]{acmart}`; the log records
  "Using anonymous mode"; page 1 of the PDF prints "ANONYMOUS AUTHOR(S)" with no names, affiliations
  or email addresses; the `.tex` contains no `\author`, `\affiliation` or ORCID anywhere. There is
  exactly **one** URL in the whole paper — the `anonymous.4open.science` artifact link — so there are
  no author-revealing repository or personal URLs. No acknowledgments section, and no
  funding/acknowledgment block that could deanonymise.
- **Data Availability.** A `\section*{Data Availability}` sits immediately after the Conclusion (it
  begins on page 18, immediately before the References heading on the same page) and describes the
  package's contents in two short paragraphs, including the two-generations-of-re-judged-cases
  convention. That is the section the call asks for, in the position it asks for.
- **References.** 39 entries in the `.bbl`, all 39 cited in the text, none uncited, none obviously
  padded. Spot-checking the first eight: TOSEM with a DOI (10.1145/3726524), ASE with an arXiv id,
  ISSTA 2018 with a DOI, AIware 2025 with page numbers, EACL 2024 demo with a DOI, ISSTA 2016 with a
  DOI. Venues, volumes, page ranges and DOIs are present where they would be expected, and the
  bibliography is not a list of self-citations — it is dominated by LLM-oracle and DBMS-testing work
  by other groups. I cannot check individual entries for accuracy without reading each paper, but
  nothing looks synthetic.
- **Length.** The PDF is 20 pages: text and figures run through page 18; the references occupy pages
  18–20. If the call's allowance is 18 pages of text plus references beyond, this fits; I could not
  reach the call itself, so I am reporting the measurement, not the verdict.
- **Housekeeping.** No Chinese working notes remain in the compiled source (I measured 0 CJK
  characters in the `.tex`); the appendix is gone; the review line numbers that ACM's `review` mode
  prints are present, as expected for a submission.

### Q6 — What sinks it now

If I were the reviewer deciding this paper's fate, the first objection I would write is:

> *The paper's third leg is a census of one configuration's judgments on one backbone. Its
> prescription — guard contract refutation — is worth seven true bugs only because a routed case is
> counted as confirmed, and it is worth exactly nothing under the paper's own forced reading; on the
> second backbone the pattern does not reproduce at all — there the guarded clause closes 50 and is
> wrong 22 times (accuracy 0.56, against contract refutation's 0.57). Strip the convention and what
> survives is a descriptive count: 24 of 50 refutations fall on
> real bugs. Is that a finding, or an accounting observation?*

**Not fatal, and mostly already answered — by the paper, in the right places.** The load-bearing
count is computed on maintainer labels, so it does not rest on the authors' own negatives; it is
invariant across the two aggregation rules the dispatch prints because contract refutation assigns
False-Positive under both; and the primary backbone's C cells are identified by their content rather
than assumed. The scope is stated in the abstract, §4.5's first sentence ("We state the scope because
it is narrower than the claim sounds and because we can check it"), §5 and §6. What is *not* answered
is the part §4.5 names itself: whether a judge re-adjudicating those refutations under a
verbatim-evidence guard would reach the same place. That experiment is ~15 cases on material the
authors already hold. Without it, the honest description of the contribution is "we measured where
this stage's errors land, and the fix is unpriced" — which is a real contribution and, I think,
publishable; but it is smaller than "the protocol guards the wrong clause", and the paper's title and
abstract still lean slightly towards the larger phrasing.

The second objection I would write is bookkeeping, and the paper is now clean on it: §4.2's
uncheckable "twenty-six of the 81" is gone (replaced by the qualitative statement), §3.1's "holding
everything else fixed" is gone, the majority tie rule is now stated with its 37/51 sensitivity, and
§8's levels are re-paired. What remains on that list is small and mechanical: the §8 discordant-pair
order (W2), the undefined "suppression" (W3), and the artifact sentence about the prompts (W4).

---

## Final scored judgement

| Criterion | Score |
|---|---|
| Importance & Scope | Good |
| Insights & Evidence | Good |
| Perspective | Good |
| Verifiability | **Excellent** |
| Presentation | Good |

**Overall recommendation: Weak Accept.** **Chair's verdict: CONDITIONAL.**

One line: this is a complete, honest, auditable measurement paper whose instrument I re-verified end
to end this round; every fixable objection from last round is fixed, and the paper now states its
claims and their scope on page 1. It is not Accept because the census's prescription is unpriced
under the authors' own honest reading and reverses on the second backbone, so the paper's third leg
remains a description of where errors land rather than a demonstrated improvement — and because the
page-limit cut moved the judges' own instructions out of the paper while leaving behind a sentence
that promises them in the package, which I could not confirm.

**Conditions I would attach (all cheap, none requiring new experiments):**

1. Re-order §8's discordant pairs to match §4.1's convention, or restate the convention (W2).
2. Define "suppression" at first use and clean up §4.1's counter-directional wording (W3).
3. Name the two judging prompts where §4.1 promises them, and verify that the English renderings ship
   in the snapshot; restore the judges' discipline clauses in one sentence (W4, Q1).
4. Add §8's answer — deferral, not organisation — to the abstract, and close §5/§8's "closes the most
   judgments" formula to "the refuting clause that closes the most" (W5).
5. Add the C-cell classification to §4.1's list of printed-but-not-scripted values, and fix "below"
   in §7 (W7).
6. Split the four or five longest sentences in §4.1, §4.4 and §4.5 — the ones that carry the authors'
   own leak-repair accounting, the arm listing and the C-cell reading (W6).

**What would move me to Accept:** the ~15-case re-adjudication under a verbatim-evidence guard
(Q6/W1), or — if that experiment is not run — a title, abstract and §8 that describe the census as
the single-backbone, convention-priced measurement it is, so that the paper claims exactly what it
measured.


