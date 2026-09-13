# -*- coding: utf-8 -*-
"""Rewrite section 4.3 (RQ2) of TestVDB.tex with the v3 numbers and narrative."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PATH = r"c:/Users/11428/Desktop/testvdb_paper/TestVDB.tex"
START = "\\subsection{RQ2: Effectiveness of False-Positive Interception}"
END = "\\subsection{RQ3: Comparison with VDBFuzz}"

NEW = r"""\subsection{RQ2: Effectiveness of False-Positive Interception}
\label{subsec:rq2}

The two headline results are earned under different configurations. The RQ1 ledger is the operational pipeline's cumulative output: it ran unblinded with the judgment-side threats of Section~\ref{sec:limitations} live, and author-side novelty screening and the submission decision sat in the loop. Everything in this subsection instead re-adjudicates the pool that ledger produced, under blinding and with no human in the loop. The two measure different layers, and neither is the complement of the other. To anchor the direction of the submission filter, we re-adjudicated a seeded sample of 32 candidates registered by the reported Qdrant run that never entered the 81-pool (excluding 4 tracked to a ledger issue), under the same frozen-package blinding and full-stage protocol, three independent runs: the blinded stage re-confirms 19/32 (0.594, Wilson [0.423, 0.745]; unanimous on 26)---higher than its 0.804 on the curated pool under the final protocol would suggest is typical, and measured before the package audit below, so we read it as a directional anchor only, not a paired comparison. Throughout, we keep two senses of ``false positive'' apart: a \emph{false-positive candidate} is one of the 30 maintainer-adjudicated non-bugs, whereas \textsc{False-Positive} (small caps throughout) is the verdict the stage returns; suppression rates are computed over candidates, and a \emph{leak} is a candidate the stage confirms; a \emph{pack} is one candidate's frozen evidence bundle, and a \emph{case} is one candidate as judged in one run.

\textbf{Measurement design: audit, rebuild, protocol alignment.}
The measurement went through two corrections, and we report all three layers because each isolates one variable. \emph{Layer 0, the shipped packages}: an audit of the originally assembled 81 packages against the documentation pages they cite found that 43.3\% of their 134 distinct (constraint, cited-page) pairs had no support on the page (58 constraint rows), a further two were over-strong relative to their page, and 32\% of all constraint rows addressed an endpoint unrelated to the candidate's own; the four packages carrying assembler provenance notes leaked adjudication-adjacent annotations into judge materials. Every defect traced to the assembler (a per-vendor fixed-version contract substitution, parameter-name rather than endpoint matching, and undocumented implementation-private constants read as contract), not to the confirmation stage. \emph{Layer 1, rebuilt packages}: we rebuilt all 81 packages from version-pinned documentation and the tested version's own OpenAPI artifact---each surviving constraint row carries its page citation, a source-type label (\emph{documentation} vs.\ \emph{structured spec}), an evidence tier, and a gate record; the four leaked provenance notes were removed before any re-adjudication. The rebuilt packages contain 674 constraint rows (from 2{,}106 originally; endpoint filtering removed 674 rows and evidence verification 463), typed as 22 \texttt{explicit} and 652 \emph{inferred-from-behavior}; 15 packages correctly declare no verifiable contract entry for their endpoint, including two of the four leak cases whose only pack-level ``support'' had been the leaked annotation. \emph{Layer 2, protocol alignment}: the judging protocol was aligned with the deployed chain-auditor rules after we found our first re-adjudication protocol still carried two pre-deployment rules that the audit had not touched but that suppressed recall by construction---by-design refutation accepted bare structural inference (``no validation is present'') rather than requiring verbatim intent evidence, and ``validation present'' counting as non-defect evidence even when no contract row covered the observed face. The deployed protocol requires intent evidence to be quoted verbatim, treats seven objective constraint classes (numeric lower bounds, closed enum sets, mutually exclusive parameters, type tautologies, same-family inconsistency, interface asymmetry, qualified HTTP semantics) as violations that need no contract endorsement, and routes unresolvable cases to an explicit \textsc{Human-Review} verdict instead of forcing \textsc{False-Positive}. On the observation side, a mechanical scan of all 81 rebuilt packages found 19 expectation-flavored phrases in observed sections, all inside verbatim server responses (``it should be in range [1, 16384]''); zero expectation framing was added by assembly, so no sanitization was applied and none was needed.

\textbf{Arms and adjudication.}
Five judge configurations follow, distinguished only by what the judge sees (Tables~\ref{tab:rq2-matrix},~\ref{tab:rq2-single}): contract core (pack only), full stage (pack plus the four-perspective protocol and its aggregation), source-only (pack and source clone), flat judge (single prompt), and source-only on a second backbone. Every configuration re-adjudicates the full pool of 81 candidates (51 real bugs + 30 false positives) in three independent runs: identical packages, default sampling, no access to adjudication labels or issue history, and every case judged in every run. The verdict is three-valued (\textsc{Confirmed}/\textsc{False-Positive}/\textsc{Human-Review}, Section~\ref{subsec:confirmation}); \textsc{Human-Review} cases count toward \textsc{Confirmed} in every rate below---the deployment routes them to human adjudication rather than closing them, and the study counts a case the way the deployment resolves it. We report both components where the distinction matters.

\begin{table}[t]
\caption{Confirmation-stage ablation over the 81-candidate pool (51 real bugs, 30 false positives) on rebuilt packages: the contract core (pack only) and the full stage (pack plus the structured four-perspective protocol), each in three independent runs with majority vote ($\geq$2/3). \textsc{Human-Review} verdicts count as confirmed (Section~\ref{subsec:confirmation}).}
\label{tab:rq2-matrix}
\small
\begin{tabular}{@{}lrrrr@{}}
\toprule
Run & TP & FP leaked & FN missed & TN intercepted \\
\midrule
core, run 1 & 9 & 1 & 42 & 29 \\
core, run 2 & 6 & 0 & 45 & 30 \\
core, run 3 & 8 & 1 & 43 & 29 \\
core, majority & 7 & 1 & 44 & 29 \\
\midrule
full, run 1 & 42 & 6 & 9 & 24 \\
full, run 2 & 40 & 7 & 11 & 23 \\
full, run 3 & 36 & 8 & 15 & 22 \\
full, majority & 41 & 6 & 10 & 24 \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[t]
\caption{Independent arms over the same 81 rebuilt packages: the source-only judge sees each pack and the pinned source clone; the flat judge is a single prompt with the same inputs and no perspectives, chain sections, or aggregation rule; D-only-Qwen re-runs the source-only arm on a second backbone. Majority vote ($\geq$2/3); core and full majorities repeated for reference.}
\label{tab:rq2-single}
\small
\begin{tabular}{@{}lrrrr@{}}
\toprule
Run & TP & FP leaked & FN missed & TN intercepted \\
\midrule
D-only, run 1 & 36 & 7 & 15 & 23 \\
D-only, run 2 & 40 & 11 & 11 & 19 \\
D-only, run 3 & 39 & 7 & 12 & 23 \\
D-only, majority & 39 & 9 & 12 & 21 \\
flat judge, majority & 30 & 2 & 21 & 28 \\
D-only-Qwen, majority & 36 & 6 & 15 & 24 \\
\midrule
contract core, majority (ref.) & 7 & 1 & 44 & 29 \\
full, majority (ref.) & 41 & 6 & 10 & 24 \\
\bottomrule
\end{tabular}
\end{table}

\textbf{The contract core: suppression without semantics.}
Under majority voting the core recalls 7/51 (0.137, Wilson [0.068, 0.257]) while suppressing 29/30 false positives (0.967, Wilson [0.833, 0.994]); case-level agreement across its three runs is 93.8\%. Its five run-to-run flips sit on decision boundaries, and its single leak is a case whose rebuilt pack carries an explicit closed-set assertion the observation violates but two runs declined to confirm. This is the assertion-framework floor: a judge that sees only documented prose and the observation can intercept what the documentation forbids, and can do so almost perfectly stably---but 37 of the 51 true bugs violate semantics the packages record only as behavioral inference, not checkable assertions, and the core has no other ground to stand on.

\textbf{The full stage: recall recovered, suppression traded.}
The structured stage recalls 41/51 (0.804, Wilson [0.675, 0.890]) at suppression 0.800 (Wilson [0.627, 0.905]) and precision 0.872. Of its 41 confirmations, 24 are \textsc{Confirmed} in all-component form and 17 carry at least one \textsc{Human-Review} component (10.4\% of full-stage verdicts route to review; the three-run case agreement is 75.3\%). The suppression cost relative to the core is exactly six cases: four are \textsc{Human-Review}-majority false positives the protocol routes to a human rather than closes (in earlier protocol runs these were forced to \textsc{False-Positive}), and two are genuine disagreements between the stage and maintainer adjudication---an enum-closure confirmation on a parameter the implementation silently defaults, and a batch-delete case confirmed through a near-version clone whose Go sources are absent from the archive. Both are recorded as protocol-vs-adjudication conflicts, not measurement errors.

\textbf{Structure is a measured mechanism, not scaffolding.}
The paper's central comparison is the full stage against a flat single-prompt judge with the same evidence access and no perspective vocabulary, evidence-chain sections, or aggregation rule (Table~\ref{tab:rq2-single}): the flat judge reaches majority recall 0.588 (Wilson [0.452, 0.712]) at suppression 0.933---solidly between the core and the full stage, but statistically below the full stage. Over the 81 paired cases the full stage beats the flat judge on 18 and loses on 3 (exact McNemar $p{=}0.0013$, Holm-corrected $p{=}0.0030$ across the seven paired tests in this subsection); the flat judge in turn beats the contract core ($p{<}0.0001$), as do source-only ($p{<}0.0001$) and the full stage ($p{<}0.0001$). The ordering that survived the earlier, pre-audit protocol as ``no ordering step survives Holm correction'' now resolves cleanly: core $<$ flat $<$ D-only $\approx$ full, with the full-vs-flat and D-only-vs-flat separations surviving correction and full-vs-D-only indistinguishable ($p{=}0.42$). The mechanism is visible in the confirmations the flat judge misses: 17 of its 21 misses are cases where the structured stage's objective-constraint classes (numeric lower bounds, enum closures, interface asymmetry) or its fixed aggregation confirm without a contract row the flat judge could act on. We therefore claim the structured confirmation protocol as a measured accuracy mechanism---revising the earlier draft's discipline-and-auditability-only framing---while noting what the claim costs: the stage's suppression is the lowest of the three structured arms, bought by exactly the human-review routing that defines its deployment posture.

\textbf{Where recall lives: the evidence-absent stratum.}
Stratifying the 51 true bugs by what their rebuilt package contains shows where each arm's recall comes from. The 37 evidence-present packs (a verifiable contract row) yield recall 0.784 for the full stage; the 3 weak-evidence packs 0.667; and---the decisive cell---the 11 evidence-absent packs (no verifiable contract entry; documentation simply does not constrain the behavior) yield 0.909. The contract core scores 0.137/0.000/0.000 across the same strata: without documented semantics it has nothing, by construction. The bridge is the objective-constraint layer of perspective B---numeric lower bounds, enum closures, and interface asymmetry are violations whether or not any prose states them---plus the human-review channel for cases only a maintainer can decide. This is the quantitative form of the paper's motivating asymmetry: the documentation constrains a minority of the defect surface, and a judge chained to the documentation is chained to that minority.

\textbf{The four leak cases, re-measured on clean packages.}
Under the original packages the four provenance-leaking candidates were confirmed with their leaked annotations in view; the audit showed two of their four main assertions had no page support at all, one rested on descriptive rather than normative prose, and one contradicted its page. On the rebuilt packages with annotations removed, the two unsupported assertions (a Request-Timeout type constraint and a \texttt{lookup\_from} existence constraint) are rejected by the contract core as before---but the full stage now re-confirms them through legitimate routes: the Request-Timeout case as a type-tautology violation (a string header silently swallowed), the lookup case through source forensics showing the existence check fires only on the id-reference path. The leak's original effect was to substitute for missing documentation; once the documentation gap is bridged by objective constraints or source evidence, the confirmations stand without it.

\textbf{The ten misses.}
The full stage's 10 false negatives decompose into three mechanisms. Four are the approximate-count family, whose packs quote the documentation's own disclaimer (``approximate count might be unreliable during the indexing process'') and whose observations fall inside the documented allowance---the contract, read literally, refutes the candidate, and we treat these as ground-truth-adjudication disagreements rather than judge errors. Two are validation-present cases (a limit bound and a strict-mode cap enforced exactly as the source declares). Four are the unconsumed-top-level-field family (TTL via \texttt{properties}, alias-list scoping, filter-id precedence, \texttt{vectorFieldType}), where the implementation silently ignores a field the maintainer later treated as defect-adjacent but no contract row covers and no verbatim by-design comment exists---under the protocol these route to human review, and their \textsc{Human-Review} votes did not reach the confirmation majority. Each mechanism is a named boundary of Section~\ref{sec:limitations} rather than an unexplained loss.

\textbf{Backbone replication.}
Re-running the source-only arm end-to-end on a second model family (Qwen; same packages, same rule) reaches majority recall 0.706 (Wilson [0.570, 0.813]) at suppression 0.800 and precision 0.857, with 61/81 three-run case agreement; it does not separate from the flat judge after Holm correction ($p{=}0.10$). The direction---source forensics recovering far above the contract core---holds on both backbones; the replication was orchestrated from the second family's own session, so backbone and agent runtime co-vary, and the other arms remain single-family.
"""

def main() -> None:
    t = io.open(PATH, encoding="utf-8").read()
    i = t.index(START)
    j = t.index(END)
    t2 = t[:i] + NEW + "\n" + t[j:]
    io.open(PATH, "w", encoding="utf-8").write(t2)
    print("replaced", j - i, "chars with", len(NEW))


if __name__ == "__main__":
    main()
