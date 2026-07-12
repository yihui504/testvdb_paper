#!/usr/bin/env python3
"""Fact-check xept Round-16 Independent Mock Review density/marginal claims."""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

tex = open('.paperpilot/review/.in-progress/paper/paper-draft-vldb-final.tex', encoding='utf-8').read()


def clean(s):
    s = re.sub(r'\\texttt\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[{}$%\\]', ' ', s)
    return s


def wcount(s):
    return len(clean(s).split())


# Abstract
i = tex.find('\\begin{abstract}') + len('\\begin{abstract}')
j = tex.find('\\end{abstract}')
ab = tex[i:j]
nums = len(re.findall(r'\d+\.?\d*', clean(ab)))
print("=== ABSTRACT ===")
print("  xept claim: ~200 words, 15+ numbers")
print("  actual: %d words, %d numbers" % (wcount(ab), nums))

# 5.3 RQ3
i = tex.find('\\subsection{RQ3')
j = tex.find('\\subsection{RQ4')
s53 = tex[i:j] if i >= 0 and j > i else ''
paras53 = s53.count('\\paragraph{')
print("\n=== SECTION 5.3 (RQ3) ===")
print("  xept claim: ~1500 words, 9 paragraph blocks")
print("  actual: %d words, %d paragraph blocks" % (wcount(s53), paras53))

# Threats
i = tex.find('\\subsection{Threats to Validity}')
j = tex.find('\\section{Related Work}')
st = tex[i:j] if i >= 0 and j > i else ''
cats = re.findall(r'\\emph\{([^}]+)\}', st)
cat_names = [c[:18] for c in cats]
has_itemize = '\\begin{itemize' in st
print("\n=== THREATS ===")
print("  xept claim: ~450 words, 9 categories in one UNDIVIDED block")
print("  actual: %d words, %d emph-labels" % (wcount(st), len(cats)))
print("  uses itemize/item structure? ", has_itemize)
print("  categories: ", cat_names)

# Contributions
ci = tex.find('paragraph{Contributions}')
ce = tex.find('end{enumerate}', ci)
nitem = tex[ci:ce].count('\\item')
print("\n=== CONTRIBUTIONS ===")
print("  xept claim: 5 (overloaded)")
print("  actual: %d item contributions" % nitem)

# Marginal value arithmetic
print("\n=== MARGINAL VALUE (xept: only ~6 TPs exclusive to LLM pipeline) ===")
print("  36 TPs - 27 boundary/validation - 3 result-correctness(model-free invariant) = %d" % (36 - 27 - 3))
print("  xept arithmetic (36-27-3==6): ", 36 - 27 - 3 == 6)
print("  paper line 224: result-correctness cases = COSINE>1.0 + incomplete index + payload filter = 3")

# Cost
has_cost = bool(re.search(r'USD|dollar|cost.effectiveness|cost per bug', tex, re.I))
has_token = bool(re.search(r'10\^?\{?7|10\^7|per.token|wall.clock', tex))
print("\n=== COST-EFFECTIVENESS ===")
print("  xept claim: not discussed (no $ translation)")
print("  paper has $/dollar/cost-per-bug? ", has_cost)
print("  paper has token/wall-clock budget? ", has_token)

# GLM monoculture
glm_mentions = len(re.findall(r'GLM-5\.2', tex))
print("\n=== GLM MONOCULTURE ===")
print("  xept claim: all 20 agents use GLM-5.2")
print("  GLM-5.2 mentions in paper: ", glm_mentions)

# Template
print("\n=== TEMPLATE ===")
dc = re.search(r'\\documentclass\[?([a-z]*)\]?\{([a-z]+)\}', tex)
print("  xept claim: ACM sigconf but filename VLDB")
print("  documentclass: ", dc.group(0) if dc else "?")
