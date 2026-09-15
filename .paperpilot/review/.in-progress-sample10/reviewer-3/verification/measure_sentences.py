"""Measure sentence lengths in TestVDB-v10.tex after stripping LaTeX markup.

Crude but auditable: strip comments/preamble, drop environments we do not want
(tables, figure captions kept), unwrap formatting commands, then split on
sentence-final punctuation followed by whitespace + uppercase/backslash.
Abbreviations are protected by a placeholder pass.
"""
import re
import sys
import json

PATH = r"c:\Users\11428\Desktop\testvdb_paper\TestVDB-v10.tex"
raw = open(PATH, encoding="utf-8").read()

# keep only body
body = raw.split(r"\begin{document}", 1)[1]
body = body.split(r"\end{document}", 1)[0]
# drop comments
body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("%"))
# drop table/tabular bodies (they are data, not prose)
body = re.sub(r"\\begin\{table\}.*?\\end\{table\}", " ", body, flags=re.S)
body = re.sub(r"\\begin\{tabular\}.*?\\end\{tabular\}", " ", body, flags=re.S)
# drop bibliography section
body = body.split(r"\bibliographystyle", 1)[0]

# unwrap formatting commands (keep argument)
for cmd in ["textbf", "emph", "texttt", "textit", "textsc", "url", "system", "subsection",
            "section", "item", "footnote", "textsuperscript", "textsubscript", "caption"]:
    prev = None
    while prev != body:
        prev = body
        body = re.sub(r"\\%s\{([^{}]*)\}" % cmd, r" \1 ", body)

# drop remaining commands (refs, labels, cites, layout)
body = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?", " ", body)
body = body.replace("~", " ").replace("---", " - ").replace("--", "-")
body = re.sub(r"\\\\", " ", body)
body = re.sub(r"\$([^$]*)\$", r" \1 ", body)
body = re.sub(r"[{}]", " ", body)

# protect abbreviations and numeric decimals from splitting
protect = {
    "e.g.": "eg<DOT>", "i.e.": "ie<DOT>", "et al.": "etal<DOT>", "vs.": "vs<DOT>",
    "cf.": "cf<DOT>", "al.": "al<DOT>", "No.": "No<DOT>", "Proc.": "Proc<DOT>",
    "Fig.": "Fig<DOT>", "Sec.": "Sec<DOT>", "Sect.": "Sect<DOT>", "vs.\\": "vs<DOT>\\",
    "e.g.\\": "eg<DOT>\\", "i.e.\\": "ie<DOT>\\",
}
for k, v in protect.items():
    body = body.replace(k, v)
# protect decimals: 0.467 -> 0<DOT>467
body = re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", body)
# protect issue numbers like #49823 and file names
body = re.sub(r"\b([a-z]+_)(\d+)", r"\1<UL>\2", body)

# normalise whitespace
body = re.sub(r"[ \t]+", " ", body)

# split sentences
parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\\\"'])", body)
sents = []
for p in parts:
    s = re.sub(r"<DOT>", ".", p)
    s = re.sub(r"<UL>", "_", s).strip()
    s = re.sub(r"^[-*\s]+", "", s)
    if len(s.split()) < 6:
        continue
    sents.append(s)

sents.sort(key=lambda s: -len(s.split()))
print("total sentences:", len(sents))
for i, s in enumerate(sents[:20], 1):
    w = len(s.split())
    print(f"\n[{i}] {w} words :: {s[:600]}")
