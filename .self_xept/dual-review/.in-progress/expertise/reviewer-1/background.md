# Background Literature for Domain Expert Review of TestVDB

## Core Competitors (Full Read)

### MASTOR (mastor26)
**Stem:** `mastor a multi agent approach to semantic test oracle generation for restful apis (2026)`
**Cached:** `mastor a multi agent approach to semantic test oracle generation for restful apis (2026).txt`
**Summary File:** Not yet written

### SATORI (satori25)  
**Stem:** `satori static test oracle generation for rest apis (40th ieee acm international conference on automated software engineering ase 2025)`
**Cached:** `satori static test oracle generation for rest apis (40th ieee acm international conference on automated software engineering ase 2025).txt`
**Summary File:** Not yet written

### AugmenTest (augmentest25)
**Stem:** `augmentest enhancing tests with llm-driven oracles`
**Metadata:** arXiv:2501.17461, 2025, ICST conference
**Fetched:** Yes (available as arXiv PDF)
**Summary File:** Not yet written

### VDBFuzz (vdbfuzz26)
**Stem:** Not found via literature search scripts
**Status:** Provisional - mentioned in TestVDB paper but no full-text retrieved

### Metamap/AGORA+ (agoraplus25, metmap24)
**Stem:** Not fully searched yet
**Status:** Provisional - mentioned in TestVDB paper

## Cached Self-Preference Bias Literature

### Panickssery et al. (panickssery24)
**Stem:** `llm evaluators recognize and favor their own generations (2024)`
**Cached:** Full text available
**Key Finding:** Establishes self-preference bias in LLM evaluators and shows correlation with self-recognition capability

### Wataoka et al. (wataoka24)
**Stem:** `self preference bias in llm as a judge (2024)`  
**Cached:** Full text available
**Key Finding:** Quantifies self-preference bias metric; identifies perplexity as underlying cause (LLMs prefer lower-perplexity texts)

## Two-Column Relational Findings

### TestVDB vs. MASTOR
**TestVDB Claim:** MASTOR extracts from source code and cannot detect documentation-implementation gaps (Table 1 exclusion row)
**Verification Needed:** Read MASTOR's actual source extraction methodology and oracle types to confirm it targets implemented behavior vs. documented contracts

### TestVDB vs. SATORI
**TestVDB Claim:** SATORI extracts from OpenAPI schema fields and stays in explicit constraint regime (Table 1 exclusion row)
**Verification Needed:** Confirm SATORI's extraction assumes schema fields carry constraints (type, format, min, max) and does not enter ambiguous prose regime

### TestVDB vs. AugmenTest
**TestVDB Claim:** AugmenTest infers from documentation but treats LLM as final arbiter, verified through runtime behavior only (Related Work)
**Verification Needed:** Confirm AugmenTest does not use implementation source as independent verification signal

### Self-Preference Bias Foundation
**TestVDB Claim:** Self-preference bias occurs when same LLM family extracts claim and judges conformance (Section 4)
**Verification Needed:** Panickssery/Wataoka establish this for LLM-as-judge; TestVDB correctly applies it to test-oracle pipeline

## Missing Related Work Search

Search scope to identify uncited highly-related work:
1. REST-API oracle derivation from natural-language documentation (non-LLM: NLP, pattern matching)
2. LLM-as-oracle for API testing beyond AugmenTest (ChatAssert, Testora, Doc2OracLLM)
3. VDBMS testing beyond VDBFuzz (empirical bug studies, roadmaps)

## Next Steps
1. Write structured summaries for MASTOR, SATORI, AugmenTest (problem/method/contribution/numbers/venue/limitations)
2. Attempt VDBFuzz search with alternative keywords (vector database fuzzing, search-based DBMS testing)
3. Conduct scoped coverage searches for missing REST-API LLM-oracle work
4. Verify TestVDB's characterization claims against full competitor texts
