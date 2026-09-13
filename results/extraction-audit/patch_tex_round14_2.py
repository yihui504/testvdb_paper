"""Round-14 patch 2: §4.3 decomposition / joint paragraphs rewritten on the
cognition-anchor-cleaned numbers (symmetrized adjudication)."""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = "TestVDB.tex"
txt = open(P, encoding="utf-8").read()
n0 = len(txt)

BS = "\\"
SC = BS + "textsc{"

# ---- patch A: the forced-verdict decomposition sentence -------------------
old = ("The decomposition, however, locates the mechanism precisely. Under "
       "forced-verdict-only scoring (" + SC + "Human-Review} not counted as "
       "confirmation), the full stage recalls 0.529 (27/51) and the flat judge "
       "0.490 (25/51)---indistinguishable ($p{=}0.51$). The full-vs-flat "
       "separation is therefore carried by the routing channel, not by "
       "forced-verdict accuracy: the structured protocol converts the cases both "
       "judges find unresolvable into explicit human-review decisions (17 of the "
       "full stage's 41 confirmations) instead of forced closures, and the flat "
       "judge---which shares the three-valued verdict space but has no aggregation "
       "rule that mandates routing, and in the primary family routes only 8.6"
       "\\% of its verdicts (21 of 243 pooled across its three runs)---closes 10 "
       "of those 17 routed confirmations as " + SC + "False-Positive}.")
new = ("The decomposition, however, locates the mechanism precisely. Under "
       "forced-verdict-only scoring (" + SC + "Human-Review} not counted as "
       "confirmation), the full stage recalls 0.529 (27/51) and the flat judge "
       "0.490 (25/51)---indistinguishable ($p{=}0.34$). The full-vs-flat "
       "separation is therefore carried by the routing channel, not by "
       "forced-verdict accuracy: the structured protocol converts the cases both "
       "judges find unresolvable into explicit human-review decisions (15 of the "
       "full stage's 39 confirmations) instead of forced closures, and the flat "
       "judge---which shares the three-valued verdict space but has no aggregation "
       "rule that mandates routing, and in the primary family routes only 8.6"
       "\\% of its verdicts (21 of 243 pooled across its three runs)---closes 8 "
       "of those 15 routed confirmations as " + SC + "False-Positive}.")
assert old in txt, "patch A anchor missing"
txt = txt.replace(old, new, 1)

# ---- patch B: the asymmetry sentence (none / exactly one) -----------------
old = ("The one evidence-access asymmetry the comparison carries---the full stage "
       "legitimately reads the maintainer-cognition materials the flat judge is "
       "forbidden---contributes to none of the separation beyond one "
       "already-disclosed case: across the cases where the two arms disagree, the "
       "cognition materials deliver a defect-side signal only in the batch-delete "
       "leak.")
new = ("The one evidence-access asymmetry the comparison carries---the full stage "
       "legitimately reads the maintainer-cognition materials the flat judge is "
       "forbidden---contributes to none of the separation beyond one "
       "already-disclosed case: across the cases where the two arms disagree, the "
       "cognition materials delivered a defect-side signal only in the "
       "batch-delete leak before the candidate-anchored entries were removed (the "
       "leak channel disclosed in Section~" + BS + "ref{sec:limitations}).")
assert old in txt, "patch B anchor missing"
txt = txt.replace(old, new, 1)

# ---- patch C: per-perspective decomposition -------------------------------
old = ("The per-perspective verdicts recorded for every run locate the "
       "confirmations precisely: of the full stage's 41 majority confirmations, 7 "
       "are driven by the contract perspective, 16 by the objective-constraint "
       "perspective (the contract chain neutral or refuted on the same case), 2 "
       "by the maintainer-cognition perspective, and 16 carry no forced-driving "
       "perspective at all---they confirm only because the protocol routes them "
       "to " + SC + "Human-Review}.")
new = ("The per-perspective verdicts recorded for every run locate the "
       "confirmations precisely: of the full stage's 39 majority confirmations, 7 "
       "are driven by the contract perspective, 16 by the objective-constraint "
       "perspective (the contract chain neutral or refuted on the same case), 2 "
       "by the maintainer-cognition perspective, and 14 carry no forced-driving "
       "perspective at all---12 of the 14 confirm only because the protocol "
       "routes them to " + SC + "Human-Review}, and 2 are confirmed on ordinary "
       "majorities despite carrying a minority " + SC + "Human-Review} component.")
assert old in txt, "patch C anchor missing"
txt = txt.replace(old, new, 1)

# ---- patch D: joint adjudication paragraph (symmetrized) -------------------
i = txt.find("To test what the routing resolves when a human actually reviews")
j = txt.find("The joint reading exists for the full stage alone:")
assert i != -1 and j > i, "patch D anchors missing"
new = (
    "To test what the routing resolves when a human actually reviews, the "
    "authors then adjudicated the routed cases of \\emph{both} arms against "
    "their pack materials only, without consulting the issue trackers, playing "
    "the channel's designated human role (non-blind; disclosed). For the full "
    "stage's routed confirmations, 9 were confirmed on their pack evidence, 2 "
    "were returned as material-insufficient, and 6 were rejected on the "
    "materials alone---a self-consistent behavior record, a distorted premise, "
    "a descriptive-only assertion, a missing documentation anchor, or an "
    "explicit in-source by-design comment; all are maintainer-confirmed "
    "upstream, so the rejections mark cases where the frozen pack undersells a "
    "real bug rather than routing failures. Replacing the convention with these "
    "adjudications yields a joint judge-plus-human recall of 33/51 (0.647): six "
    "true positives above forced-only scoring (0.529) and six below the "
    "convention's 0.765---the convention overstates the joint system, forced "
    "scoring understates it, and the measured truth sits in between "
    "(Table~" + BS + "ref{tab:scorings}). The channel routes both ways, and the "
    "human pass adjudicates its false-positive side as well: of the six routed "
    "false positives, five are rejected on their pack materials and one is "
    "returned for a cleaner reproduction; a returned case is never adjudicated "
    "a false positive, so it still counts as intercepted in the joint system "
    "and the joint suppression closes at 27/30 (0.900) with precision 0.917. "
    "Crucially, the flat judge's own 11 routed confirmations were adjudicated "
    "under the same pack-materials rule (four upholding their earlier "
    "hand-outcomes, two confirmed on enumeration-class evidence, three "
    "rejected for missing documentation anchors), giving the joint reading an "
    "equal-treatment counterpart for both arms: the joint full stage recalls "
    "0.647 at precision 0.917 against a joint flat judge at 0.549 and 0.966, "
    "and the separation survives---discordant 8/1, exact McNemar $p{=}0.039$---"
    "so the routing advantage is not an artifact of adjudicating only one "
    "arm's routed cases. "
)
txt = txt[:i] + new + txt[j:]

open(P, "w", encoding="utf-8").write(txt)
print(f"patched decomposition + joint paragraphs; delta {len(txt) - n0:+d} chars")
