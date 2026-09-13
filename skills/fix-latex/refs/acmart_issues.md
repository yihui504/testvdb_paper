# ACM acmart Document Class Troubleshooting

## Package Conflicts

### Conflict with amssymb

**Error:**
```
LaTeX Error: Command `\Bbbk' already defined.
```

**Cause:** acmart loads newtxmath which defines `\Bbbk`. Loading amssymb creates conflict.

**Solution:**
```latex
% Option 1: Remove amssymb entirely (recommended)
% DELETE: \usepackage{amssymb}

% Option 2: Clear the symbol before loading
\let\Bbbk\relax
\usepackage{amssymb}
```

### Conflict with amsmath/amsfonts

**Error:** Various math symbol redefinition errors

**Cause:** acmart automatically loads amsmath and amsfonts

**Solution:** Remove manual loading:
```latex
% DELETE these lines:
% \usepackage{amsmath}
% \usepackage{amsfonts}
```

### Hyperref Already Loaded

**Error:**
```
Package hyperref Error: hyperref package is already loaded
```

**Cause:** acmart loads hyperref automatically

**Solution:** Remove `\usepackage{hyperref}` from your preamble

## Format Options

acmart requires explicit format specification:

```latex
% Required format options:
\documentclass[acmsmall]{acmart}        % Small format
\documentclass[acmlarge]{acmart}        % Large format  
\documentclass[acmtog]{acmart}          % TOG format
\documentclass[sigconf]{acmart}         % Conference format
\documentclass[sigplan]{acmart}         % SIGPLAN format
\documentclass[sigchi]{acmart}          % SIGCHI format
```

## Bibliography Issues

### natbib vs biblatex

**Error:** Citation commands not working

**Cause:** acmart uses natbib by default

**Solution:**
```latex
% Use natbib commands:
\citep{key}   % Parenthetical citation
\citet{key}   % Textual citation
\cite{key}    % Basic citation

% NOT biblatex commands like \parencite, \textcite
```

### BibTeX Compilation

**Required multiple passes:**
- First pass: generates .aux file
- BibTeX pass: processes bibliography
- Second/third pass: resolves citations
- 用 `latexmk` 自动跑多遍 + bibtex（见 `local_compile.md`），无需手动逐遍

## Version Requirements

acmart requires:
- TeX Live 2020 or newer
- Recent version of acmart.cls (v1.60+)

**Check version:**
```latex
% In log file, look for:
% Document Class: acmart YYYY/MM/DD vX.XX
```

## Common Warnings

### "Some images may lack descriptions"

**Warning:**
```
Class acmart Warning: Some images may lack descriptions.
```

**Cause:** Accessibility requirement - images should have alt text

**Solution:** Add descriptions to figures:
```latex
\begin{figure}
  \Description{Detailed description of the image for screen readers}
  \includegraphics{image.pdf}
  \caption{Short caption}
\end{figure}
```

### "Reference 'TotPages' undefined"

**Warning:**
```
LaTeX Warning: Reference `TotPages' on page 1 undefined
```

**Cause:** First compilation hasn't created .aux files

**Solution:** Run pdflatex twice (this is normal, not an error)

## Font Issues

### Missing Libertine Fonts

**Error:**
```
Font shape 'T1/LinuxLibertineT-TLF/m/n' undefined
```

**Solution:**
- Report missing libertine package to user
- User needs to install libertine fonts in their TeX distribution

### newtxmath Conflicts

acmart loads newtxmath automatically. Don't load:
- txfonts
- Other math font packages

## ACM Metadata

### Required Metadata

acmart expects certain metadata:

```latex
\acmYear{2024}
\acmConference[CONF '24]{Conference Name}{Month Date}{City, Country}
\copyrightyear{2024}
\acmPrice{15.00}
\acmDOI{10.1145/1234567.1234567}
\acmISBN{978-1-4503-XXXX-X/XX/XX}
```

**Note:** Missing metadata causes warnings, not errors

## Column Balance Issues

### Two-column Layout

**Problem:** Content not balancing across columns

**Solution:**
```latex
% Use \newpage sparingly
% Let acmart handle column breaks
% For manual control:
\begin{figure*}[t]  % Spans both columns
  ...
\end{figure*}
```

## CCS Concepts

### Missing CCS Categories

**Warning:** No CCS concepts defined

**Solution:**
```latex
\begin{CCSXML}
<ccs2012>
<concept>
<concept_id>10003752.10003790</concept_id>
<concept_desc>Theory of computation~Logic</concept_desc>
<concept_significance>500</concept_significance>
</concept>
</ccs2012>
\end{CCSXML}

\ccsdesc[500]{Theory of computation~Logic}
```

## Package Load Order

**Safe load order:**

1. acmart document class
2. Encoding packages (fontenc, inputenc)
3. Graphics packages (graphicx)
4. Math packages (only if needed and not conflicting)
5. Other packages
6. Never load: hyperref, amsmath, amsfonts (already included)

## Quick Fixes Summary

| Problem | Solution |
|---------|----------|
| `\Bbbk already defined` | Remove `\usepackage{amssymb}` |
| Hyperref error | Remove `\usepackage{hyperref}` |
| Missing format | Add `[acmsmall]` or other format option |
| Bibliography not appearing | Run BibTeX, compile twice |
| Font errors | User needs to install libertine and newtx fonts |
| Undefined references | Compile twice |
| CCS warnings | Add CCS concepts (optional) |
