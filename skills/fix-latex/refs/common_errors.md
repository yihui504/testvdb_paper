# Common LaTeX Errors Catalog

## Compilation Errors (Stop Compilation)

### Undefined Control Sequence

**Error:**
```
! Undefined control sequence.
l.42 \somecommand
```

**Causes:**
1. Typo in command name
2. Missing package that defines the command
3. Command doesn't exist

**Solutions:**
```latex
% Check spelling
\textbf{text}  % NOT \testbf

% Load required package
\usepackage{amsmath}  % For \align, \equation*, etc.
\usepackage{graphicx} % For \includegraphics
\usepackage{hyperref} % For \url, \href

% Common missing packages:
% - amsmath: advanced math
% - graphicx: images
% - xcolor: colors
% - listings: code listings
% - hyperref: hyperlinks
```

### Missing $ Inserted

**Error:**
```
! Missing $ inserted.
```

**Cause:** Math mode needed but not active

**Solutions:**
```latex
% Wrong: Using math symbols in text mode
The value of x_2 is...

% Right: Use math mode
The value of $x_2$ is...
The value of $x^2$ is...

% For display math:
\[ x = y + z \]
% or
\begin{equation}
  x = y + z
\end{equation}
```

### File Not Found

**Error:**
```
! LaTeX Error: File 'package.sty' not found.
```

**Solutions:**
- Report missing package name to user
- User needs to install package in their TeX distribution
- For custom files: verify file exists in project directory

### Environment Undefined

**Error:**
```
! LaTeX Error: Environment foo undefined.
```

**Solutions:**
```latex
% Check environment name spelling
\begin{itemize} ... \end{itemize}  % NOT \begin{items}

% Load package that defines environment
\usepackage{algorithm}  % For algorithm environment
\usepackage{listings}   % For lstlisting environment
\usepackage{theorem}    % For theorem-like environments
```

### Missing \begin{document}

**Error:**
```
! LaTeX Error: Missing \begin{document}.
```

**Causes:**
1. Content before `\begin{document}`
2. Typo in preamble causing text to appear
3. Missing `\begin{document}`

**Solution:**
```latex
\documentclass{article}
% Preamble - only commands, no text
\usepackage{...}
\title{...}
\begin{document}  % Required!
% Content goes here
\end{document}
```

### Mismatched Braces

**Error:**
```
! Too many }'s.
```

**Cause:** Unbalanced { and }

**Solution:**
```latex
% Wrong:
\textbf{bold text

% Right:
\textbf{bold text}

% Use editor features:
% - Bracket matching
% - Auto-completion
% - Syntax highlighting
```

### Paragraph Ended Before Command Was Complete

**Error:**
```
! Paragraph ended before \command was complete.
```

**Cause:** Missing } or ] in command argument

**Solution:**
```latex
% Wrong:
\section{My Section

% Right:
\section{My Section}

% Wrong:
\includegraphics[width=0.5\textwidth{image.pdf}

% Right:
\includegraphics[width=0.5\textwidth]{image.pdf}
```

## Warnings (Compilation Succeeds)

### Undefined References

**Warning:**
```
LaTeX Warning: Reference `sec:intro' undefined on input line 42.
```

**Causes:**
1. Missing `\label{sec:intro}`
2. Typo in label name
3. First compilation (normal)

**Solutions:**
```latex
% Define label:
\section{Introduction}
\label{sec:intro}

% Reference it:
See Section~\ref{sec:intro}.

% Always compile TWICE for references to resolve
```

### Citation Undefined

**Warning:**
```
LaTeX Warning: Citation 'smith2020' undefined on input line 42.
```

**Solutions:**
1. Check .bib file for entry with key `smith2020`
2. Run BibTeX: `bibtex document`
3. Compile sequence: latex -> bibtex -> latex -> latex
4. Check citation key spelling

### Overfull/Underfull Hbox

**Warning:**
```
Overfull \hbox (10.5pt too wide) in paragraph at lines 42--45
```

**Cause:** LaTeX can't break line properly

**Solutions:**
```latex
% Allow hyphenation:
\usepackage[english]{babel}

% Manual hyphenation:
su\-per\-cal\-i\-frag\-i\-lis\-tic

% Allow more stretching:
\sloppy
... text ...
\fussy

% Break long URLs:
\usepackage{url}
\url{http://example.com/very/long/url}
```

### Float Too Large

**Warning:**
```
LaTeX Warning: Float too large for page
```

**Solutions:**
```latex
% Reduce figure size:
\includegraphics[width=0.8\textwidth]{image.pdf}

% Allow float on separate page:
\begin{figure}[p]  % p = separate page
  ...
\end{figure}

% Scale down table:
\resizebox{\textwidth}{!}{
  \begin{tabular}{...}
  ...
  \end{tabular}
}
```

## Package-Specific Errors

### babel/polyglossia Conflicts

**Error:** Language option conflicts

**Solution:**
```latex
% Choose one:
\usepackage[english]{babel}
% OR
\usepackage{polyglossia}
\setdefaultlanguage{english}
```

### Graphics Driver Not Found

**Error:**
```
! Package graphics Error: No driver specified.
```

**Solution:**
```latex
% Specify driver:
\usepackage[pdftex]{graphicx}  % For pdflatex
\usepackage[xetex]{graphicx}   % For xelatex
\usepackage[luatex]{graphicx}  % For lualatex

% Or let LaTeX auto-detect:
\usepackage{graphicx}
```

### Encoding Errors

**Error:** Strange characters or encoding warnings

**Solutions:**
```latex
% For UTF-8 documents (modern):
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% For XeLaTeX/LuaLaTeX (handles UTF-8 natively):
\usepackage{fontspec}
```

## Math Errors

### Bad Math Environment Delimiter

**Error:**
```
! Missing $ inserted.
```

**Solutions:**
```latex
% Wrong:
$$x = y$$  % Don't use $$ in LaTeX

% Right:
\[ x = y \]  % Display math
\begin{equation} x = y \end{equation}  % Numbered equation
$x = y$  % Inline math
```

### Double Subscript

**Error:**
```
! Double subscript.
```

**Cause:** Two subscripts without grouping

**Solutions:**
```latex
% Wrong:
x_i_j

% Right:
x_{i_j}  % Nested subscript
x_i,_j   % Two separate subscripts
```

## File System Errors

### Permission Denied

**Error:** Can't write to output directory

**Solutions:**
```bash
# Check permissions:
ls -la

# Fix permissions:
chmod 755 directory
chmod 644 file.tex
```

### File Name with Spaces

**Problem:** `\includegraphics{my image.pdf}` fails

**Solutions:**
```latex
% Option 1: Rename file (no spaces)
\includegraphics{my_image.pdf}

% Option 2: Use grffile package
\usepackage{grffile}
\includegraphics{my image.pdf}
```

## Exit Codes Reference

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 0    | Success | - |
| 1    | Error   | Undefined commands, missing files |
| 12   | Error   | Package conflicts, symbol redefinition |

## Log Analysis Tips

- Search for "error" (case-insensitive) in log files
- Look for lines starting with "!" for TeX primitive errors
- Check "warning" messages for potential issues
- File and line numbers help locate problems quickly
