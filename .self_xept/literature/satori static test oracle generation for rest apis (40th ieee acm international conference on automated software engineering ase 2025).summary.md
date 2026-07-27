# SATORI — Summary (context-independent)

**Citation:** Alonso, Martin-Lopez, Segura, Bavota, Ruiz-Cortés. "SATORI: Static Test Oracle Generation for REST APIs." ASE 2025 (40th IEEE/ACM Int'l Conf. on Automated Software Engineering), pp. 1364–1376. arXiv:2508.16318.

## Problem
REST API test-case generators produce valid requests but are constrained by the oracles they support: crashes (5XX), spec disconformities, regressions, best-practice violations. They miss semantic faults in response fields (e.g., `country` should be 2 chars; `latitude` ∈ [-90, 90]) encoded only implicitly in the OpenAPI Specification (OAS) prose. AGORA+ (the only prior REST oracle generator) addresses this dynamically by detecting likely invariants from execution, but its accuracy depends on a diverse exercising test suite and may inherit faulty responses.

## Method
**Static, black-box, OAS-only.** No API execution required. SATORI prompts an LLM to infer 17 types of test oracles (format, length, numerical range, enum membership, etc.) over the **response fields** documented in the OAS, by reading each field's name, description, and schema. Output is normalized into executable Chai/Postman assertions via PostmanAssertify. Assessed 21 LLM backbones.

## Key Quantitative Results
- **Benchmark:** 17 operations from 12 industrial APIs; ground-truth dataset OKAMI (10.5k oracles over 1.8k response fields) released on Hugging Face.
- **Oracle F1: 74.3%** (vs. AGORA+ 69.3% on comparable oracle types). Together SATORI + AGORA+ find 90% of ground-truth oracles (complementary).
- **Bugs found: 18** across 7 APIs (Amadeus Hotel, Deutschebahn, FDIC, GitLab, Marvel, OMDb, Vimeo), vs. AGORA+ 13 across 7. Led to documentation updates in Vimeo.

## Dataset & Venue
12 industrial REST APIs (OAS-documented); ASE 2025.

## Limitations (as stated)
- Source of truth is the OAS (a structured, low-ambiguity specification). SATORI does not address natural-language documentation outside a spec.
- Oracles are over **response fields** (output correctness), not over input accept/reject decisions.
- Evaluated on operations with manually annotated ground truth (17 operations); scale of the manually-validated subset is modest.
- LLM may hallucinate oracles; no independent verification step beyond F1 against annotation.
