# Translation Guidelines

## Core Principle
The primary goal of translation is **completeness and accuracy**. Losing content is worse than awkward phrasing.

## Completeness Check (Most Important)
After translation, verify ALL of the following are preserved:
1. **Floats**: every \begin{table} and \begin{figure} has a counterpart
2. **Equations**: every equation, align, and inline $...$ is preserved
3. **Algorithms**: algorithm, lstlisting, and similar environments are intact
4. **Sections**: every \section/\subsection has a counterpart
5. **Bibliography entries**: bib file untouched; \cite{} count matches source

## Never Translate
- \cite{key} — keep citation keys as-is
- \ref{label}, \label{name} — keep cross-references as-is
- Math symbols inside equations
- BibTeX keys and field names
- Custom LaTeX command names
- Code block content (unless user explicitly asks)

## Must Translate
- Section titles (text inside \section{})
- Body text / Abstract / Figure/table captions / Author affiliations (if requested)

## Terminology Consistency
1. Build glossary before translating — get user confirmation
2. Use the same translation throughout — one term, one translation
3. Preserve proper nouns in original language
4. Follow domain conventions

## Academic Register
- Chinese → English: use formal academic English; mix passive and active voice
- English → Chinese: use formal written Chinese; avoid translationese
- Preserve original hedging level
