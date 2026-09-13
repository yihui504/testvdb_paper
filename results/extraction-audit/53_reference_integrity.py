"""Verify every cross-reference in TestVDB.tex is an intact \\ref/\\cite
command -- catches the case where a shell heredoc ate a backslash and left a
bare 'ef{...}' (R3 cycle-2 item 5.4)."""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = "TestVDB.tex"
s = io.open(P, encoding="utf-8").read()

# any {label} that is not preceded by a command backslash
bare = [(m.start(), m.group(0)) for m in
        re.finditer(r"(?<!\\)\b(?:ef|cite|label|eqref)\{[^}]*\}", s)]
print(f"bare (backslash-stripped) reference commands: {len(bare)}")
for pos, txt in bare[:10]:
    line = s[:pos].count("\n") + 1
    print(f"   line {line}: {txt!r}")

# every \ref target must exist as a \label
refs = set(re.findall(r"\\ref\{([^}]*)\}", s))
labels = set(re.findall(r"\\label\{([^}]*)\}", s))
missing = sorted(refs - labels)
print(f"\n\\ref targets: {len(refs)}; labels: {len(labels)}")
print("dangling \\ref targets:", missing if missing else "none")

# every \cite key must be in the bib
keys = set(re.findall(r"@\w+\{([^,]+),", io.open("TestVDB.bib",
                                                 encoding="utf-8").read()))
cited = set()
for m in re.finditer(r"\\cite[a-z]*\{([^}]*)\}", s):
    for k in m.group(1).split(","):
        cited.add(k.strip())
print("cited but not in bib:", sorted(cited - keys) or "none")
