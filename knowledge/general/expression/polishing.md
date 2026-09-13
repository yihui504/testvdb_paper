# Polishing Guidelines

## Core Principle
Polishing ≠ rewriting. Polishing improves expression quality while **preserving the original meaning and structure**.

## Scope Control
1. If user specified a range, only modify that range
2. If no range specified, ask — don't default to full-paper polishing
3. Confirm before large changes — for 3+ paragraphs, use confirm_plan first
4. Report what was changed

## Never Modify
- \cite{}, \ref{}, \label{} — preserve all citations and cross-references
- Math environments ($...$, equation, align) — don't touch formula content
- Experimental data and numerical results — never change any numbers
- Table/figure content — only modify captions when explicitly asked
- Custom LaTeX commands and macro definitions
- Superscripts, subscripts, and special symbol formatting

## Terminology Consistency
- Don't expand abbreviations that have already been defined
- Don't rename terms that the user has established in facts memory
- Use the same expression for the same concept throughout

## Iterative Polishing
From the 3rd polishing iteration onward:
- Don't re-edit content already modified in previous iterations
- Focus on specific issues the user raised this time
- If nothing meaningful can be improved, proactively say so
