"""Round-14 patch 4: upstream number updates (abstract/intro/contribution/
conclusion/backbone/Limitations), the §3.5 HR-contradiction fix, cognition
corpus scope, and the Argus citation."""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = "TestVDB.tex"
txt = open(P, encoding="utf-8").read()
n0 = len(txt)
BS = "\\"


def rep(old, new, tag):
    global txt
    assert old in txt, f"{tag}: anchor missing"
    txt = txt.replace(old, new, 1)
    print(f"  ok: {tag}")


# 1. abstract
rep("while the structured full stage reaches 0.804 recall at 0.800 suppression "
    "under the deployment's counting convention---against 0.588 for a flat "
    "single-prompt judge reading the same packs and sources.",
    "while the structured full stage reaches 0.765 recall at 0.700 suppression "
    "under the deployment's counting convention---against 0.588 for a flat "
    "single-prompt judge reading the same packs and sources.",
    "abstract headline")
rep("the deployment's counting convention, under which routed cases count as "
    "confirmed, yields the 0.804---routing, not forced accuracy, is where the "
    "structure pays.",
    "the deployment's counting convention, under which routed cases count as "
    "confirmed, yields the 0.765---routing, not forced accuracy, is where the "
    "structure pays.",
    "abstract convention yield")

# 2. intro
rep("the full structured stage reaches 0.804 recall at 0.700 suppression"
    .replace("0.700", "0.800") + ", and a flat single-prompt judge reading the "
    "same packs and sources reaches only 0.588---the structured protocol's "
    "advantage survives Holm correction ($p{=}0.029$), and 20.6\\% of its "
    "verdicts route to an explicit human-review channel rather than being "
    "forced.",
    "the full structured stage reaches 0.765 recall at 0.700 suppression, and "
    "a flat single-prompt judge reading the same packs and sources reaches "
    "only 0.588---the structured protocol's advantage survives Holm correction "
    "($p{=}0.0052$), and 19.8\\% of its verdicts route to an explicit "
    "human-review channel rather than being forced.",
    "intro headline")

# 3. contribution 2
rep("reading the same packs and sources it recalls 0.804 where a flat "
    "single-prompt judge reaches 0.588 ($p{=}0.0072$, Holm-corrected $0.029$; "
    "a three-run re-run of this pair on a second family does not separate, "
    "$p{=}1.0$); its verdicts admit three readings, reported side by side "
    "(forced verdicts 0.529, joint judge-plus-human 0.647, counting convention "
    "0.804)",
    "reading the same packs and sources it recalls 0.765 where a flat "
    "single-prompt judge reaches 0.588 ($p{=}0.0013$, Holm-corrected $0.0052$; "
    "a three-run re-run of this pair on a second family does not separate, "
    "$p{=}1.0$); its verdicts admit three readings, reported side by side "
    "(forced verdicts 0.529, joint judge-plus-human 0.647, counting convention "
    "0.765)",
    "contribution 2")

# 4. backbone replication paragraph
rep("(exact McNemar raw $p{=}0.0075$, Holm-corrected $p{=}0.029$ across this "
    "subsection's seven paired tests)",
    "(exact McNemar raw $p{=}0.0075$, Holm-corrected $p{=}0.023$ across this "
    "subsection's seven paired tests)",
    "backbone D-onlyQ corrected p")
rep("under majority voting the two arms separate not at all (discordant pairs "
    "7/7, exact McNemar $p{=}1.0$; forced-only 0.510 vs.\\ 0.451, $p{=}1.0$), "
    "with lower routing rates on both arms (9.5\\% full, 7.8\\% flat pooled "
    "across three runs, against 20.6\\% on the primary family)",
    "under majority voting the two arms separate not at all (discordant pairs "
    "8/5, exact McNemar $p{=}0.58$; forced-only 0.510 vs.\\ 0.451, $p{=}0.45$), "
    "with lower routing rates on both arms (10.3\\% full, 8.6\\% flat pooled "
    "across three runs, against 19.8\\% on the primary family)",
    "backbone second-family numbers")

# 5. Limitations sixth-threat numbers
rep("16 of the full stage's 41 confirmations are driven by it, and excluding "
    "them lowers recall to 0.490",
    "16 of the full stage's 39 confirmations are driven by it, and excluding "
    "them lowers recall to 0.451",
    "limitations co-evolution numbers")

# 6. §3.5 HR contradiction
rep("routed to the review queue rather than silently resolved, and such cases "
    "lie outside every automated rate in Section~" + BS + "ref{sec:eval})",
    "routed to the review queue rather than silently resolved, and such cases "
    "lie outside the forced-verdict rates of Section~" + BS + "ref{sec:eval})",
    "§3.5 HR contradiction")

# 7. cognition corpus scope in the arms paragraph
rep("identical packs, default sampling, no access to adjudication labels or "
    "issue history, and every case judged in every run.",
    "identical packs, default sampling, no access to adjudication labels or "
    "issue history except the maintainer-cognition materials the full stage "
    "reads as perspective D (historical patterns mined in August 2026, before "
    "the re-adjudication and scoped in Section "
    + BS + "ref{sec:limitations}), and every case judged in every run.",
    "arms cognition scope")

# 8. conclusion numbers
rep("the convention-based 0.804, the joint judge-plus-human 0.647, and the "
    "forced-verdict 0.529 measure different layers",
    "the convention-based 0.765, the joint judge-plus-human 0.647, and the "
    "forced-verdict 0.529 measure different layers",
    "conclusion readings")

# 9. Argus in Related Work
rep("It is the closest DBMS-side instance", "SHOULD-NOT-MATCH") if False else None
old = ("the DBMS differential line (NoREC, TLP, DQE, PQS, DDLCheck, BUZZBEE)")
if old not in txt:
    # find the actual DBMS differential sentence
    import re
    m = re.search(r"the DBMS differential line \([^)]*\)", txt)
    old = m.group(0) if m else None
if old:
    txt = txt.replace(old, old.replace("BUZZBEE)", "BUZZBEE), and Argus, whose "
        "LLM-proposed query-equivalence oracles are validated by a formal SQL "
        "equivalence prover (query-equivalence authority where "
        "Section~" + BS + "ref{sec:intro} demands prose-conformance "
        "authority)", 1), 1)
    print("  ok: Argus related-work")
else:
    print("  WARN: DBMS differential line not found; Argus deferred")

open(P, "w", encoding="utf-8").write(txt)
print(f"patch 4 done; delta {len(txt) - n0:+d} chars")
