# Peer Review v3 (post-v7) — TestVDB

> Three independent reviewers re-evaluated the paper after v7 revisions (SATORI two-axis reframe + cross-family 3-run union + structured-failure-mode diagnosis + symmetric kappa vs GLM 3-run union + GLM per-vendor recall). Same rubric, independent of Rounds 1-2. Date: 2026-08-04.

**Note:** Round 3 reviewer drafts did not persist to disk (Agent Write side-effect); the per-reviewer summaries below are reconstructed from each reviewer returned text. The Meta-Review synthesizes the returned verdicts and tier assignments.

---

## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

- Significance: Adequate | Novelty: Adequate | Soundness: Adequate | Verifiability: Excellent | Presentation: Excellent
- **Strengths:** S1 clear problem + novelty delta (see 1.1, 2.1); S2 source-grounded falsification addresses LLM reliability (3.1); S3 empirical impact 107 issues / 49 TP / 15 merged-PR (4.1); S4 bidirectional VDBFuzz probe (3.3)
- **Weaknesses:** W1 cross-family generalization open [major, fixable] (3.2); W2 implementation-as-correct assumption unaddressed [minor, fixable]; W3 external validity limited to VDBMS [major, unfixable] (1.2); W4 operating point post-hoc [minor, fixable] (3.4)

---

## Reviewer 2: Area Specialist (LLM-as-judge + REST-API oracles)

**Overall Recommendation:** Accept

- Specialties: LLM-as-a-judge / self-preference; REST-API oracle generation. Verified 5 competitors against fetched papers: Panickssery (NeurIPS 2024), Wataoka (CoRR 2024), SATORI (2025), MASTOR (J. ACM 2026), Rating Roulette (EMNLP 2025) — **all characterizations accurate**.
- **Strengths:** novel source-grounded falsification countermeasure to self-preference; strong empirical validation (107 submissions, 49 maintainer-acknowledged TP); clear delta over SATORI/MASTOR verified against actual papers.
- **Weaknesses:** limited cross-family validation (GLM-5.2 only; other families kappa <= 0.32); external validity gaps (Weaviate yield-only; transfer minimally evaluated).
- **Verdict rationale:** core contribution sound, novel, well-supported by real-world evidence; limitations transparent and do not undermine central claims.

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Accept

- Significance: Adequate | Novelty: Excellent | Soundness: Excellent | Verifiability: Excellent | Presentation: Adequate
- **Strengths:** S1 real-world impact (49 TP, 15 merged-PR); S2 systematic oracle-exclusion argument (Section 2, Table 1); S3 bidirectional VDBFuzz probe isolates complementary coverage; S4 honest threats-to-validity.
- **Weaknesses (all minor):** W1 post-hoc operating point selection [minor, fixable] (3.4); W2 notation inconsistency (C-vs-not-C undefined; Wilson CI format) [minor, fixable] (5.4/5.5).
- **Overall derivation:** no substance Weak, multiple substance Excellent => Accept per rubric.

---

## Meta-Review (Round 3, post-v7)

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Adequate | Adequate | Excellent | **Adequate** [Mixed] |
| Soundness | Adequate | Adequate | Excellent | **Adequate** [Mixed] |
| Verifiability | Excellent | Adequate | Excellent | **Excellent** |
| Presentation | Excellent | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Weak Accept** | **Accept** | **Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three reviewers leaned in (2 Accept + 1 Weak Accept), so the unanimous shortcut applies — every individual recommendation is Weak Accept or better. This is a **strengthening vs. Round 2** (which was 3× Weak Accept): R2 and R3 both upgraded to Accept.

**Why the upgrade.** The v7 revisions (SATORI two-axis reframe + cross-family 3-run union + structured-failure-mode diagnosis + symmetric κ vs. GLM 3-run union + GLM per-vendor recall) resolved the substantive weaknesses Round 1/2 flagged:
- **SATORI mischaracterization (Round 1 R2-W4): resolved.** R2 (Area Specialist) verified all five competitors against fetched papers — Panickssery, Wataoka, SATORI, MASTOR, Rating Roulette — and confirmed every paper characterization is **accurate**.
- **Cross-family "one run minimal" (Round 1/2): upgraded.** R2 cites the new symmetric evidence ("κ ≤ 0.32", "combined recall 56%/22%/19%"). The structured-failure-mode diagnosis (Qwen variance = contract-vs-source tension, not random noise) turns the cross-family limitation from a bare disclosure into a diagnosed root cause with an improvement path.
- R3 (Generalist) rates Novelty and Soundness **Excellent**, driving its Accept.

**Checker caught a real paper bug (now fixed).** The Round 3 checkers found that the v7 edit updated κ only in §6 (line 302: 0.32/0.20/0.18 vs. GLM 3-run union) but **left the old values in §7 Construct validity** (line 344: 0.14/0.37/0.51 vs. GLM single-run) — an internal contradiction between two κ statements in the same paper. This was a surgical-edit omission in revision #2. **Fixed**: line 344 now also reads 0.32/0.20/0.18 vs. GLM 3-run union; the paper compiles (9 pages) and grep confirms no 0.14/0.37/0.51 residue. This is exactly the kind of grounding error the independent-checker stage exists to catch.

**Remaining (all inherent, all disclosed):**
- Cross-family single-LLM (R1 W1 `[major, fixable]`; R2): inherent — the 3-run union + κ + structured diagnosis are the strongest disclosure a revision can add without rerunning all families at full protocol.
- External validity beyond VDBMSs (R1 W3 `[major, unfixable]`): inherent — CouchDB/Elasticsearch returned 0 defects.
- Post-hoc operating point (R1 W4 `[minor, fixable]`): already labeled "exploratory" + Bonferroni + bootstrap.

### Priority Revisions
1. **[consensus, major, fixable]** Cross-family: keep the 3-run union + structured-failure-mode framing as the primary disclosure; a future full-protocol (5-run union on all families) rerun would close it.
2. **[R1, major, unfixable]** External portability: one non-VDBMS case study surfacing a real silent-accept defect, or keep the structural-only claim.
3. **[R1, minor, fixable]** Implementation-as-correct assumption (R1 W2): explicitly bound the regime where it could fail.
4. **[draft-level, unverified]** Round 3 reviewer drafts did not persist to disk (Agent Write did not take effect); the verdicts and tier assignments above are taken from the reviewers' returned summaries. Table-number drift flagged by checkers in some drafts (presentation-level, does not affect verdict).

**Inherent limitations cap the verdict at ACCEPT (not higher):** single LLM family, post-hoc operating point, non-random retrospective, external portability. The v7 revisions converted the cross-family weakness from "acknowledged limitation" to "diagnosed with root cause + improvement path," which is what drove R2/R3 from Weak Accept to Accept.

