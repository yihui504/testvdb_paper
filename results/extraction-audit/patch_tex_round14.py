"""Round-14 patch 1: replace the flagship-comparison paragraph in §4.3 with
the cognition-anchor-cleaned numbers (16/2, p=0.0013, flagship adjusted 0.0052
in the declared family and 0.0092 in the maximal ten-test family)."""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = "TestVDB.tex"
txt = open(P, encoding="utf-8").read()

start_marker = "The paper's central comparison is the full stage"
end_marker = "backbone replication below)."
i = txt.find(start_marker)
assert i != -1, "start not found"
j = txt.find(end_marker, i)
assert j != -1, "end not found"
j += len(end_marker)

BS = "\\"
new_seg = (
    "The paper's central comparison is the full stage against a flat single-prompt judge "
    "reading the same packs and sources, with no perspective vocabulary, evidence-chain "
    "sections, or aggregation rule (Table~" + BS + "ref{tab:rq2-single}): the flat judge reaches "
    "majority recall 0.588 (Wilson [0.452, 0.712]) at suppression 0.867---solidly between "
    "the core and the full stage, but statistically below the full stage. Over the 81 "
    "paired cases the full stage beats the flat judge on 16 and loses on 2---each test "
    "pairs the two arms' " + BS + "emph{confirmed sets} (" + BS + "textsc{Confirmed} or "
    + BS + "textsc{Human-Review} under the convention above, so a ``leak'' counts as "
    "confirmed on both sides), the discordant net therefore matches the confirmed-set "
    "difference, and here it is 48 vs.\\ 34, net $+14$ (exact McNemar $p{=}0.0013$, "
    "Holm-corrected $p{=}0.0052$ across the seven paired tests in this subsection"
    + BS + "footnote{The family is defined by construction: the seven confirmation-arm "
    "pairs on the primary pool. The seven paired tests, with raw exact $p$ and discordant "
    "nets: core-vs-flat $<0.0001$ (discordant 0/25); core-vs-D-only $<0.0001$ (2/37); "
    "core-vs-full $<0.0001$ (1/40); full-vs-flat $p{=}0.0013$ (16/2; fourth-smallest, "
    "Holm multiplier 4); D-only-Qwen-vs-flat $p{=}0.0075$ (15/3; fifth-smallest, "
    "multiplier 3, adjusted 0.023; backbone replication below); D-only-vs-flat "
    "$p{=}0.041$ (15/5); full-vs-D-only $p{=}0.39$ (8/4). Adding the three sensitivity "
    "analyses below to the family as a maximal ten-test set raises the flagship's "
    "adjusted value only to 0.0092.}); the flat judge in turn beats the contract core "
    "($p{<}0.0001$), as do source-only ($p{<}0.0001$) and the full stage ($p{<}0.0001$). "
    "The ordering resolves cleanly: core $<$ flat $<$ D-only $\\approx$ full, of which "
    "the full-vs-flat separation survives correction under every family size we test, "
    "full-vs-D-only is indistinguishable ($p{=}0.39$; the two confirmed sets differ by "
    "four cases, so that test is underpowered at this pool size), and the flat-vs-D-only "
    "step does not survive correction ($p{=}0.083$); the second-backbone source-only arm "
    "separates from the flat judge at a corrected $p$ of 0.023 (backbone replication "
    "below)."
)
txt = txt[:i] + new_seg + txt[j:]
open(P, "w", encoding="utf-8").write(txt)
print("patched flagship paragraph, len", len(new_seg))
