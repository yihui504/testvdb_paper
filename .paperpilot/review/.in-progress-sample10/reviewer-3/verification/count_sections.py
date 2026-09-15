import re

PATH = r"c:\Users\11428\Desktop\testvdb_paper\TestVDB-v10.tex"
raw = open(PATH, encoding="utf-8").read()
body = raw.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("%"))

# split at subsection / section headings
marks = [(m.start(), m.group(0)) for m in re.finditer(r"\\(sub)?section\{[^}]*\}", body)]
bounds = []
for i, (pos, name) in enumerate(marks):
    end = marks[i + 1][0] if i + 1 < len(marks) else len(body)
    bounds.append((name, body[pos:end]))

TABLE = re.compile(r"\\begin\{table\}.*?\\end\{table\}", flags=re.S)


def wc(txt):
    t = TABLE.sub(" ", txt)
    t = re.sub(r"\\caption\{[\s\S]*?\n\n", " ", t)
    t = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?", " ", t)
    t = re.sub(r"[{}$]", " ", t)
    return len(t.split())


for name, chunk in bounds:
    if name.startswith("\\subsection"):
        print(f"{name:60s} {wc(chunk):6d} words (tables excluded)")
