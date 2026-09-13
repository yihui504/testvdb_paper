# English AI Style Detection Patterns

Four layers: vocabulary -> syntax -> argumentation -> researcher voice.

---

## Layer 1: Vocabulary

### Tier 1 — Always Replace

These words saw massive frequency spikes in academic writing post-ChatGPT (Kobak et al., 2024: analysis of 14M PubMed abstracts). Replace on sight.

| Flagged | Increase post-GPT | Replacement |
|---------|-------------------|-------------|
| delve / delve into | +1500% | examine, study, investigate |
| underscore | +1000% | highlight, show |
| intricate | +700% | complex, detailed |
| meticulous / meticulously | +2800% | careful, thorough |
| realm | massive spike | area, domain, field |
| showcasing | massive spike | showing, presenting |
| pivotal | massive spike | important, key, central |
| leverage | — | use |
| utilize | — | use |
| harness | — | use, apply |
| robust | — | reliable, stable, consistent |
| comprehensive | — | broad, thorough, full |
| novel | — | new, proposed |
| cutting-edge | — | recent, current |
| seamless / seamlessly | — | smooth, integrated |
| multifaceted | — | complex, varied |
| holistic / holistically | — | overall, integrated |
| unprecedented | — | first, unusual, not previously reported |
| paradigm / paradigm shift | — | approach, model, framework |
| state-of-the-art | — | best-performing, current best |
| groundbreaking | — | new, first |
| tapestry | — | (delete or restructure) |
| embark | — | begin, start |
| streamline | — | simplify, reduce |
| game-changer / game-changing | — | significant, important |
| testament to | — | evidence of, shows |
| synergy | — | combination, interaction |
| innovative / innovation | — | new, improved |
| transformative | — | (be specific: "improves X by Y%") |
| elucidate | — | explain, clarify |
| spearhead | — | lead, initiate |
| catalyze | — | trigger, enable |
| augment | — | supplement, add to |
| revolutionize | — | change, improve |
| cornerstone | — | foundation, basis |
| nexus | — | connection, intersection |
| nascent | — | early, emerging |
| burgeoning | — | growing |
| overarching | — | overall, main |
| actionable | — | practical, usable |
| impactful | — | effective, useful |

### Tier 2 — Flag When 2+ in Same Paragraph

| Word | Replacement |
|------|-------------|
| significant / significantly | (replace with number: "by 15%") |
| effective / effectively | (be specific about what works) |
| dynamic / dynamics | interactions, changes |
| compelling | strong, convincing |
| remarkable / remarkably | notable, unusual |
| sophisticated | complex, advanced |
| instrumental | important, useful |
| facilitate / facilitates | enable, allow |
| foster | support, encourage |
| bolster | strengthen, support |
| navigate / navigating | handle, manage |
| encompass | include, cover |
| paramount | essential, critical |
| poised | ready, positioned |
| nuanced | subtle, detailed |
| crucial | important, key |
| myriad | many, numerous |
| plethora | many, excess of |
| quintessential | typical, defining |

### Tier 3 — Flag When Clustered (3+ on one page)

| Word/Phrase | Fix |
|-------------|-----|
| furthermore | (delete or "also") |
| moreover | (delete or "also") |
| notably | (delete) |
| consequently | "so", "as a result" |
| additionally | "also", or just delete |
| it is important to note that | (delete entirely) |
| it is worth noting that | (delete entirely) |
| interestingly | (delete — let the content be interesting) |
| in today's | (delete — don't date your paper) |
| in an era where | (delete) |
| taken together | (often deletable) |
| in summary | (use sparingly, only in actual summary) |

---

## Layer 2: Syntax

### 2.1 Em-Dash / En-Dash Overuse

Target: ≤1 per 1000 words. Flag if >2 per page.

- Bad: "The framework — which integrates multiple approaches — provides a solution — one that addresses key challenges — for researchers."
- Good: "The framework integrates multiple approaches and addresses key challenges for researchers."
- Fix: comma, parentheses, or split into sentences.

### 2.2 Formulaic Paper Openers

| AI-typical | Human |
|-----------|-------|
| This paper proposes... | We introduce... |
| This paper presents... | Our approach... |
| This paper introduces... | The key idea is... |
| In this work, we... | (fine occasionally, flag if repeated) |

### 2.3 Throat-Clearing Openers

Delete entirely — go straight to the claim:

- "In the rapidly evolving landscape/world of..."
- "In today's digital age..."
- "As we continue to evolve..."
- "In a world where..."
- "Has emerged as a leading/key..."
- "In an era where..."

### 2.4 Filler Transitions

Delete or replace:

| Flagged | Fix |
|---------|-----|
| It is worth noting that | delete — state directly |
| It is important to note that | delete |
| It bears mentioning that | delete |
| This is particularly important because | delete — show importance |
| Interestingly, | delete |
| Notably, | delete |
| Moreover, | delete or "Also," |
| Furthermore, | delete |
| In light of the above, | delete |
| In conclusion, | delete — start with substance |

### 2.5 Uniform Paragraph Length

Flag: all paragraphs in a section within ±1 sentence of each other.
Fix: mix 2-3 sentence paragraphs with 5-8 sentence ones.

### 2.6 Uniform Sentence Length (Burstiness)

AI writing has monotonously consistent sentence length. Human writing alternates.

Flag: 5+ consecutive sentences within ±5 words of each other.
Fix: break one long sentence into two short ones; combine two short ones into a compound sentence. Target: mix of 8-word and 25-word sentences.

### 2.7 Repetitive Sentence Structure

Flag: 3+ consecutive Subject-Verb-Object sentences.
Fix: vary with fronted clause, passive (occasionally), compound, or inverted structure.

- Bad: "The model processes input. The algorithm classifies samples. The system outputs results."
- Good: "After processing input, the model classifies each sample before outputting results."

### 2.8 Three-Item Default

AI defaults to exactly three. Use natural count.

- Bad: "three advantages: efficiency, scalability, and robustness."
- Good: "improves efficiency and scalability." (if only two are supported by evidence)

### 2.9 Hedge Stacking

One hedge per claim.

| Bad | Good |
|-----|------|
| may potentially contribute | may contribute |
| could possibly suggest | suggests |
| appears to seemingly indicate | indicates |
| might arguably be considered | can be considered |

### 2.10 Copula Avoidance

Use "is" when "is" works.

| Bad | Good |
|-----|------|
| serves as a framework | is a framework |
| functions as an indicator | is an indicator |
| acts as a bridge between | connects |
| stands as a testament to | shows |

### 2.11 Synonym Cycling

One term per concept, used consistently.

- Bad: "the framework... the paradigm... the model... the architecture" (same thing)
- Good: "the framework" throughout

### 2.12 Negative Parallelism

State directly instead of "not just X, but also Y":

| Bad | Good |
|-----|------|
| not just efficient, but also scalable | efficient and scalable |
| not merely theoretical, but applicable | applicable in practice |

### 2.13 Significance Inflation

| Flagged | Fix |
|---------|-----|
| groundbreaking | (is it actually?) -> new, first |
| pivotal | important, key |
| transformative | improves X by Y% |
| unprecedented | first reported in this context |
| paradigm-shifting | changes how X is done |
| revolutionary | (almost never justified) |

### 2.14 Vague Attribution

"Studies show..." without `\cite{}` is a red flag.

- Bad: "Studies have shown that this method is effective."
- Good: "This method reduced error rates by 15% in three trials (Smith 2022; Lee 2023)."

---

## Layer 3: Argumentation

**This layer matters more than L1-L2 combined.** A paper with zero "delve" can still scream AI if every claim is unconditional.

### 3.1 Missing Trade-offs

The single biggest AI tell.

- Bad: "Our method improves accuracy and efficiency."
- Good: "The gain in accuracy comes at the cost of additional inference overhead."
- Also good: "Although the improvement is modest, it remains consistent across datasets."

**Detection**: any claim asserting improvement without mentioning cost, limitation, or condition.
**Fix**: add ONE — a cost ("at the expense of"), a condition ("when X > Y"), a boundary ("on datasets where"), or a qualifier ("compared to Z, though not to W").

### 3.2 Unconditional Claims

- Bad: "Method A outperforms Method B."
- Good: "Method A achieves higher accuracy on four of five datasets, although the margin narrows when training data are scarce (Figure 3b)."

### 3.3 All-Positive Results

- Bad: "Our approach is effective across all settings."
- Good: "The approach works well on structured data but degrades on free-form text inputs."

### 3.4 Vague Limitations

- Bad: "A limitation of our work is scalability."
- Good: "Trace collection reaches 40 min for 500-step trajectories, scaling linearly with execution length."

### 3.5 Cataloging Related Work

- Bad: "Smith (2023) proposed X. Jones (2024) extended to Y. Our work differs by Z."
- Good: "Smith (2023) addressed X but assumed fixed vocabulary, which breaks in our setting. Jones (2024) relaxed this but added 3x latency."

### 3.6 Symmetric Comparisons

AI gives equal weight to pros and cons in a balanced, fence-sitting way.

- Bad: "On the one hand X, on the other hand Y."
- Good: "X is the primary concern; Y matters less in practice because..."

---

## Layer 4: Researcher Voice

### 4.1 Certainty -> Uncertainty

| AI-certain | Researcher |
|-----------|------------|
| The results demonstrate | The results suggest / indicate |
| This proves | This supports / provides evidence for |
| This confirms | This is consistent with |
| This reveals | This appears to show |
| This establishes | This points toward |

### 4.2 Failure and Surprise

Real papers contain:
- "Surprisingly, X did not improve Y"
- "Counter to our expectation, the simpler baseline outperformed..."
- "We initially tried X but found..."
- "An unexpected drop in performance when..."

### 4.3 Researcher Vocabulary

| Category | Words |
|----------|-------|
| Honest difficulty | surprisingly, unexpectedly, non-trivial, unstable, difficult, tricky, brittle |
| Modest results | modest, marginal, incremental, slight, partial |
| Real uncertainty | we hypothesize, one possible explanation, it remains unclear, we speculate |
| Process | we initially tried, after several iterations, the key insight was, we noticed that |
| Negative | did not improve, failed to, degrades, breaks down, does not hold |

### 4.4 Design Decision Rationale

- Bad: "We use a transformer encoder with 6 layers."
- Good: "We chose 6 layers after finding deeper models overfit on our dataset (Appendix B). A CNN baseline failed to capture long-range dependencies."

### 4.5 Specific Future Work

- Bad: "Future work will focus on scalability and generalization."
- Good: "A remaining challenge is scaling trace collection to long-horizon tasks (>1000 steps). Checkpoint-based sampling is promising but trades completeness for efficiency."

### 4.6 Rebuttal Voice

| AI rebuttal | Strong rebuttal |
|------------|----------------|
| "We thank the reviewer for the valuable comments." | "The reviewer raises an important question regarding trace quality." |
| "We agree that scalability is important." | "To quantify the scalability concern, we measured runtime on three additional workloads..." |
| "We will add more experiments." | "We ran the suggested experiment. On dataset X, performance drops to Y%, confirming Z is the bottleneck." |

**Rules**: 1. Lead with the issue, not thanks. 2. Include numbers. 3. Show you did something, don't promise. 4. Acknowledge when reviewer is right. 5. Disagree with evidence, not rhetoric.
