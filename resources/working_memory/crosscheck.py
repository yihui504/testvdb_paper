# -*- coding: utf-8 -*-
import io, re
from collections import Counter

with io.open(r'C:\Users\11428\Desktop\testvdb_paper\files\TestVDB.tex', encoding='utf-8') as f:
    tex = f.read()
with io.open(r'C:\Users\11428\Desktop\testvdb_paper\files\TestVDB.bib', encoding='utf-8-sig') as f:
    bib = f.read()

cited = set()
for m in re.finditer(r'\\cite\{([^}]*)\}', tex):
    for k in m.group(1).split(','):
        k = k.strip()
        if k:
            cited.add(k)

bib = re.sub(r'(?m)^\s*%.*$', '', bib)
keys = set(re.findall(r'@\w+\s*\{\s*([A-Za-z0-9_.\-]+)\s*,', bib))
allkeys = re.findall(r'@\w+\s*\{\s*([A-Za-z0-9_.\-]+)\s*,', bib)

print('cited keys (%d):' % len(cited))
print(' '.join(sorted(cited)))
print()
print('bib keys (%d):' % len(keys))
print()
missing = cited - keys
print('CITED BUT NOT IN BIB (FAIL):', sorted(missing) if missing else 'none')
uncited = keys - cited
print('IN BIB BUT NEVER CITED (WARNING): %d' % len(uncited))
print(' '.join(sorted(uncited)))
dups = [k for k, c in Counter(allkeys).items() if c > 1]
print()
print('duplicate bib keys:', dups if dups else 'none')

# count \cite occurrences per key (usage frequency)
freq = Counter()
for m in re.finditer(r'\\cite\{([^}]*)\}', tex):
    for k in m.group(1).split(','):
        k = k.strip()
        if k:
            freq[k] += 1
print()
print('cite usage frequency:')
for k in sorted(freq):
    print('  %s: %d' % (k, freq[k]))
