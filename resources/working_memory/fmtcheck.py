# -*- coding: utf-8 -*-
"""Formatting check for citations in TestVDB.tex (xept:check-references step 4)."""
import io, re

with io.open(r'C:\Users\11428\Desktop\testvdb_paper\files\TestVDB.tex', encoding='utf-8') as f:
    tex = f.read()

# 1. citation after period (period directly followed by \cite on same line)
after_period = []
for m in re.finditer(r'\.\s*\\cite\{([^}]*)\}', tex):
    after_period.append((m.start(), m.group(1)))
print('A) \\cite directly after a period:', len(after_period))

# 2. \cite not preceded by ~ or whitespace (need ~ before cite)
no_tilde = []
for m in re.finditer(r'\\cite\{([^}]*)\}', tex):
    start = m.start()
    if start == 0:
        continue
    prev = tex[start-1]
    if prev not in '~ ' and not prev.isalpha():
        no_tilde.append((start, prev, m.group(1)))
print('B) \\cite with unusual previous char (not ~ or space):', len(no_tilde))
for start, prev, k in no_tilde[:30]:
    ctx = tex[max(0,start-40):start+len(k)+10].replace('\n', ' ')
    print('   ...%s[%r]... key=%s' % (ctx[:40], prev, k))

# 3. cite as sentence subject (line starts with ~\cite or \cite)
subject = []
for line in tex.split('\n'):
    if re.match(r'^\s*[~\\]*\\cite\{', line):
        subject.append(line.strip()[:80])
print('C) lines starting with \\cite (sentence-subject smell):', len(subject))
for s in subject:
    print('   ', s)

# 4. citation commands used
cmds = set(re.findall(r'\\(cite|citep|citet|citealp|citeauthor|Citet|Citep)\b', tex))
print('D) citation commands used:', sorted(cmds))

# 5. multiple cites in one \cite (ok) — check for spaces after commas inside \cite
spaced = []
for m in re.finditer(r'\\cite\{([^}]*)\}', tex):
    if re.search(r',\s+', m.group(1)):
        spaced.append(m.group(1))
print('E) \\cite with space after comma:', len(spaced), spaced[:10])

# 6. citation followed by punctuation other than period
for m in re.finditer(r'\\cite\{([^}]*)\}([.,;:!?)\]])', tex):
    pass  # normal

# 7. bibliography style
m = re.search(r'\\bibliographystyle\{([^}]*)\}', tex)
print('F) bibliographystyle:', m.group(1) if m else 'NONE')

# 8. \nocite usage
noc = re.findall(r'\\nocite\{([^}]*)\}', tex)
print('G) \\nocite:', noc if noc else 'none')
