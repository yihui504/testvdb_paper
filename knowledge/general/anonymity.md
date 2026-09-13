# Anonymity Check

Loaded on-demand for double-blind venues. Check on **compiled PDF**, not LaTeX source.

## 1. Author Information
Check PDF for visible author names, affiliations, emails in title/header area.

## 2. Self-Citation Risk Levels
**High risk (FAIL)**: "In our previous work [X]", "We previously showed in [X]", GitHub/website URLs with identifiable usernames
**Medium risk (WARNING)**: "In previous work [X]" (no "our" but citing suspiciously related paper), multiple citations to same author group
**Safe (PASS)**: "Previous work [X] showed..." (neutral third-person), "Smith et al. [X] demonstrated..."

## 3. Acknowledgments
- FAIL: Named funding with PI names / Named collaborators or institutions
- WARNING: Acknowledgments section exists (review content)
- PASS: No acknowledgments, or explicitly anonymized

## 4. External Links
- FAIL: github.com/realname/... — use Anonymous GitHub (anonymous.4open.science)
- FAIL: Personal/institutional websites, identifiable cloud storage links

## 5. PDF Metadata
Check PDF properties (Author, Creator fields). Use \hypersetup{pdfauthor={}} to clear.
