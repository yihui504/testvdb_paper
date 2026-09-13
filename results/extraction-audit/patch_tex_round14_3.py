"""Round-14 patch 3: full-stage paragraph, strata paragraph rewrite, stale
joint-tail removal, and the fourth leak channel disclosure in Limitations."""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = "TestVDB.tex"
txt = open(P, encoding="utf-8").read()
n0 = len(txt)
BS = "\\"
SC = BS + "textsc{"

# ---- A: full-stage paragraph ----------------------------------------------
old = ("The structured stage recalls 41/51 (0.804, Wilson [0.675, 0.890]) at "
       "suppression 0.800 (Wilson [0.627, 0.905]) and precision 0.872. Of its 41 "
       "confirmations, 24 are " + SC + "Confirmed} in all-component form and 17 "
       "carry at least one " + SC + "Human-Review} component---twelve routed by "
       "the majority of their three runs, two more losing their majority under "
       "forced scoring only because a single " + SC + "Human-Review} vote splits "
       "the other two, and the remaining three confirmed two-to-one on ordinary "
       "votes with a single " + SC + "Human-Review} component alongside. The "
       "three-run case agreement is 70.4\\% (57 of 81 cases), and 20.6\\% of all "
       "full-stage verdicts---50 of the 243 case judgments pooled across the "
       "three runs---route to review.")
new = ("The structured stage recalls 39/51 (0.765, Wilson [0.632, 0.860]) at "
       "suppression 0.700 (Wilson [0.521, 0.833]) and precision 0.812. Of its 39 "
       "confirmations, 23 are " + SC + "Confirmed} in all-component form and 16 "
       "carry at least one " + SC + "Human-Review} component---ten routed by the "
       "majority of their three runs and six confirmed two-to-one on ordinary "
       "votes with a single minority " + SC + "Human-Review} component alongside. "
       "The three-run case agreement is 67.9\\% (55 of 81 cases), and 19.8\\% of "
       "all full-stage verdicts---48 of the 243 case judgments pooled across the "
       "three runs---route to review.")
assert old in txt, "A anchor missing"
txt = txt.replace(old, new, 1)

# ---- B: suppression-cost sentence -----------------------------------------
old = ("The suppression cost relative to the core is five cases: four are "
       + SC + "Human-Review}-majority false positives the protocol routes to a "
       "human rather than closes (in earlier protocol runs these were forced to "
       + SC + "False-Positive}), and one is a forced-verdict disagreement---a "
       "batch-delete case confirmed through a near-version clone whose Go "
       "sources are absent from the archive; the verdict has not been "
       "re-examined against a same-version clone.")
new = ("The suppression cost relative to the core is eight cases: six are "
       + SC + "Human-Review}-majority false positives the protocol routes to a "
       "human rather than closes, and two are forced-verdict "
       "disagreements---an enum-closure confirmation on a parameter the "
       "implementation silently defaults, and a batch-delete case whose probe "
       "value a later source reading suggests may never have bound (the "
       "binding-artifact note in Section " + BS + "ref{sec:limitations}).")
assert old in txt, "B anchor missing"
txt = txt.replace(old, new, 1)

# ---- C: enum-closure sentence ---------------------------------------------
old = ("A sixth full-stage false positive, an enum-closure confirmation on a "
       "parameter the implementation silently defaults, is already confirmed by "
       "the contract core---it is the core's single leak---and so adds no "
       + BS + "emph{relative} cost. All are recorded as protocol-vs-adjudication "
       "conflicts, not measurement errors.")
new = ("One of the eight, an enum-closure confirmation on a parameter the "
       "implementation silently defaults, is already confirmed by the contract "
       "core---it is the core's single leak---and so adds no " + BS + "emph{relative} "
       "cost. All are recorded as protocol-vs-adjudication conflicts, not "
       "measurement errors.")
assert old in txt, "C anchor missing"
txt = txt.replace(old, new, 1)

# ---- D: strata paragraph rewrite ------------------------------------------
old = ("The 37 evidence-present packs (a verifiable contract row) yield "
       "convention-scoring recall of 0.784 for the full stage; the 3 "
       "weak-evidence packs 0.667; and the 11 evidence-absent packs (no "
       "verifiable contract entry; documentation simply does not constrain the "
       "behavior) 0.909---the highest cell under this convention, and its "
       "quantitative form of the paper's motivating asymmetry. The scoring "
       "decomposition, however, shows what carries that cell: of its 10 "
       "convention confirmations, only 3 are confirmed outright on "
       + SC + "Confirmed} majorities---one of the three carrying a "
       + SC + "Human-Review} component in a minority run---while the other 7 "
       "route to " + SC + "Human-Review}, and only 4 of the 8 routed cases "
       "survive hand adjudication, so the same stratum recalls 0.273 (3/11) "
       "under forced verdicts and 0.545 (6/11) in the joint reading---below the "
       "evidence-present stratum under both (0.649 and 0.703) and above the "
       "weak-evidence cell under both (0.000 and 0.333, 1/3 of its three "
       "packs). Without documented semantics the stage can still force-confirm "
       "the objective-constraint violations of perspective B---numeric lower "
       "bounds, enum closures, and interface asymmetry are violations whether "
       "or not any prose states them---but the remaining cases only a "
       "maintainer can decide, and the convention credits the escalation. The "
       "evidence-absent stratum is therefore where routing contributes most, "
       "not where forced confirmation is strongest, and the asymmetry claim "
       "inherits the layer of the scoring it is read under. The contract core "
       "scores 0.216/0.000/0.000 across the same strata (8/37, 0/3, 0/11): "
       "without documented semantics it has nothing to say about the "
       "evidence-absent stratum, by construction.")
new = ("The 37 evidence-present packs (a verifiable contract row) yield "
       "convention-scoring recall of 0.784 for the full stage; the 3 "
       "weak-evidence packs 0.667; and the 11 evidence-absent packs (no "
       "verifiable contract entry; documentation simply does not constrain the "
       "behavior) 0.727. The scoring decomposition shows what carries each "
       "cell: under forced verdicts the strata read 0.649 / 0.000 / 0.273, and "
       "under the joint reading 0.703 / 0.333 / 0.545---under every scoring, "
       "the evidence-absent stratum does " + BS + "emph{not} lead. The contract "
       "core scores 0.216/0.000/0.000 across the same strata (8/37, 0/3, 0/11). "
       "The motivating asymmetry therefore survives in its architectural form, "
       "not a per-stratum form: without documented semantics the stage has "
       "nothing contractual to say (the core is silent on 11 of 11), whatever "
       "it recovers there comes from the objective-constraint classes of "
       "perspective B or from routing to a human, and the human-review channel "
       "is what keeps the evidence-absent packs from scoring zero. The "
       "documentation still constrains a minority of the defect surface---but "
       "where it constrains nothing, no scoring of this stage is strong.")
assert old in txt, "D anchor missing"
txt = txt.replace(old, new, 1)

# ---- E: remove the stale joint-tail sentence ------------------------------
old = ("The joint reading exists for the full stage alone: only its routed "
       "cases were hand-adjudicated, so the flat arm has no equal-treatment "
       "joint counterpart (Table~" + BS + "ref{tab:scorings} reports it under "
       "forced and convention scorings), and the reading's human cost is the 21 "
       "hand-adjudicated cases---17 routed confirmations plus 4 routed false "
       "positives, a quarter of the pool.")
assert old in txt, "E anchor missing"
txt = txt.replace(old, " ", 1)

# ---- F: fourth leak channel in Limitations --------------------------------
old = "A fourth, irreducible threat is \\emph{adjudication disagreement}:"
new = ("A fourth channel surfaced at the cognition materials themselves: a "
       "candidate-anchoring audit found that the runtime cognition files "
       "contained entries referencing seven of the 81 candidates' own issue "
       "numbers (four false-positive-side by-design patterns with maintainer "
       "quotes and two true-positive-side blindspot examples in Milvus; one "
       "by-design pattern in Qdrant), although a cleaned variant of the Milvus "
       "file had existed since before the re-adjudication. Because the full "
       "stage is the only arm that reads these materials, we removed the "
       "candidate-anchored entries, re-adjudicated the seven cases in every "
       "affected arm and run on both backbones, and replaced the affected "
       "verdicts; every number in Section 4 is computed on the cleaned pool, "
       "and the pre-cleanup verdict files ship in the artifact. A fifth, "
       "irreducible threat is \\emph{adjudication disagreement}:")
assert old in txt, "F anchor missing"
txt = txt.replace(old, new, 1)

open(P, "w", encoding="utf-8").write(txt)
print(f"patch 3 applied; delta {len(txt) - n0:+d} chars")
