## Background: Core Competitors (≤5)

### 1. VDBFuzz (vdbfuzz26)
- **Stem:** `vdbfuzz26`
- **Metadata:** See `records/vdbfuzz.json`. VDBFuzz is a crash-oracle fuzzer for VDBMSs.
- **Paper's Characterization:** VDBFuzz uses crash as its oracle and misses silent-accept defects because they don't crash. The bidirectional probe shows TestVDB reaches VDBFuzz's integer-overflow crash via contract reasoning, while VDBFuzz misses TestVDB's #9045 silent-accept defect.
- **Verdict:** Paper's characterization is accurate. VDBFuzz targets crashes, not accept/reject decisions.

### 2. AGORA+ (Alonso et al., TOSEM 2025)
- **Stem:** `agora-plus_2025_tosem`
- **Metadata:** See `records/agora-plus.json`. Dynamic invariant detection from execution traces. 80% precision, 106 invariant types.
- **Paper's Characterization:** AGORA+ infers invariants from observed traffic and cannot reach inputs the traffic did not exercise. It targets output invariants, not input-acceptance decisions.
- **Verdict:** Paper's characterization is accurate. AGORA+ is output-focused and requires observed traffic. Novelty delta: TestVDB targets input-acceptance (consistency) without requiring observed traffic.

### 3. SATORI (Alonso et al., ASE 2025)
- **Stem:** `satori_2025_ase`
- **Metadata:** See `records/satori.json`. Static LLM-based oracle generation from OpenAPI specs. F1 74.3%.
- **Paper's Characterization:** SATORI reads OpenAPI schema elements (type, format, minimum, maximum) and stays in a regime where constraints are explicit. VDBMS documentation carries constraints in prose with no schema field to anchor on, so SATORI's extraction step has no input.
- **Verdict:** Paper's characterization is directionally correct. SATORI relies on structured schema fields; VDBMS documentation is unstructured prose. The delta is valid but not empirically tested on VDBMS endpoints.

### 4. MASTOR (Deng et al., arXiv 2026)
- **Stem:** `mastor_2026_arxiv`
- **Metadata:** See `records/mastor.json`. Multi-agent semantic oracle generation from implementation source. Mutation score 75.4%.
- **Paper's Characterization:** MASTOR reads source to generate oracles that encode implemented behavior and cannot detect a gap between documentation and code. TestVDB reads source as a falsifier of documentation-derived claims.
- **Verdict:** Paper's characterization is accurate. MASTOR encodes implementation; TestVDB checks documentation-implementation gap. Novelty delta is clear.

### 5. Doc2OracLL (Hossain et al., PACM Softw. Eng. 2024)
- **Stem:** `doc2oracll_2024_pacm`
- **Metadata:** See `records/toradocu.json`. Investigates Javadoc impact on LLM-based TOG. Shows description and return tags most valuable.
- **Paper's Characterization:** Not cited. The paper cites Toradocu (Peters & Parnas, ISSTA 1994) but not Doc2OracLL or AugmenTest.
- **Verdict:** Missing related work. Doc2OracLL is directly relevant to documentation-interpretation regimes and LLM-derived oracles. AugmenTest (fetched but not cited) also belongs here.

## Novelty Delta Summary

TestVDB's novelty is strongest relative to:
- **VDBFuzz:** Targets crashes vs. silent-accept defects.
- **MASTOR:** Encodes implementation vs. checks documentation-implementation gap.
- **AGORA+:** Output-focused, requires traffic vs. input-focused, documentation-driven.
- **SATORI:** Structured schema vs. unstructured prose (valid but untested).

Missing comparisons:
- **AugmenTest/Doc2OracLL:** Directly address documentation quality vs. LLM oracle correctness. TestVDB should position itself against these works in the documentation-interpretation regime.
