#!/usr/bin/env python3
"""Verify readability metrics after presentation overhaul."""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

tex = open('paper/paper-draft-vldb-final.tex', encoding='utf-8').read()


def clean(s):
    s = re.sub(r'\\texttt\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[{}$%\\]', ' ', s)
    return s


def wc(s):
    return len(clean(s).split())


# abstract
i = tex.find('\\begin{abstract}') + len('\\begin{abstract}')
j = tex.find('\\end{abstract}')
ab = tex[i:j]
nums = len(re.findall(r'\d+\.?\d*', clean(ab)))
print("ABSTRACT: %d words, %d numbers (was 219 words / 10 numbers)" % (wc(ab), nums))

# 5.3
i = tex.find('\\subsection{RQ3')
j = tex.find('\\subsection{RQ4')
s53 = tex[i:j] if i >= 0 and j > i else ''
subs = s53.count('\\subsubsection{')
paras = s53.count('\\paragraph{')
print("SECTION 5.3: %d words, %d subsubsection, %d paragraph (was 2252 words / 12 paragraph)" % (wc(s53), subs, paras))

# threats
i = tex.find('\\subsection{Threats to Validity}')
j = tex.find('\\section{Related Work}')
st = tex[i:j] if i >= 0 and j > i else ''
items = st.count('\\item')
has_itemize = '\\begin{itemize' in st
print("THREATS: %d words, itemize=%s, %d items (was 466 words / undivided block)" % (wc(st), has_itemize, items))

# contributions
ci = tex.find('paragraph{Contributions}')
ce = tex.find('end{enumerate}', ci)
print("CONTRIBUTIONS: %d items (was 5)" % tex[ci:ce].count('\\item'))
