# Writing a Good ML Introduction

## Core Principle
ML reviewers are experts. Get to the point fast and be precise about your contribution.

## How ML Introductions Differ
ML intros are **task-centric**: open with task/benchmark, state current SOTA, then identify limitation. ML intros rarely start with societal motivation.

**Typical flow**: Task importance → SOTA results → SOTA limitation → Our key insight → What we propose → Headline numbers → Contribution list

## Contribution List Conventions
ML papers almost always list 3-4 contributions:
1. A novel formulation, insight, or perspective
2. The proposed method/architecture (named, with brief description)
3. Theoretical analysis or guarantee (if applicable)
4. Empirical results: "We evaluate on [benchmarks] and achieve [metric], outperforming [SOTA] by [margin]"

**Including numbers in intro**: ML convention is to announce key results if they are strong. Vague claims read as hiding weak numbers.
**Naming your method**: introduce in boldface on first mention.

## Language Patterns
**Task framing**: "X is a fundamental problem in [area] with applications in [A, B, C]."
**Limitation of SOTA**: "However, existing methods rely on [assumption], which limits..."
**Key insight**: "Our key observation is that [insight], which enables [consequence]."
**Contribution**: "We propose **MethodName**, a [type] for [task] that [key property]."
**Results preview**: "Our method reduces [cost] by [X]× while maintaining comparable [quality]."

## Hook variants (first sentence)
- Benchmark hook: "Large language models have achieved near-human performance on [benchmark], yet struggle with [harder task]."
- Application hook: "[Application] relies on [capability], which remains a bottleneck."
- Scale hook: "The success of [approach] has been driven by scale, but [cost] demands more efficient alternatives."

## Common Pitfalls
- Explaining basics reviewers already know
- Vague contributions: "We study X" instead of "We show X achieves Y"
- Missing recent arXiv papers
- Overselling incremental improvements
- No numbers in introduction when results are available
- Claiming "first" without hedging
