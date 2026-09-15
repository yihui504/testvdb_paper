import re

PATH = r"c:\Users\11428\Desktop\testvdb_paper\TestVDB-v10.tex"
raw = open(PATH, encoding="utf-8").read()
body = raw.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("%"))
prose = re.sub(r"\\begin\{table\}.*?\\end\{table\}", " \nTABLE\n ", body, flags=re.S)
prose = prose.split(r"\bibliographystyle", 1)[0]
for cmd in ["textbf", "emph", "texttt", "textit", "textsc", "url"]:
    for _ in range(6):
        prose = re.sub(r"\\%s\{([^{}]*)\}" % cmd, r"\1", prose)
prose = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?", " ", prose)
prose = re.sub(r"[{}]", " ", prose)
prose = re.sub(r"\s+", " ", prose)

pres = [
    "Read as a family of ten",
    "It does not move the two controls",
    "The nineteen judgments this census closes",
    "But the last two are the weaker kind",
    "Aggregation is fixed",
    "The flat judge is the full stage",
    "Each control is a traceable edit",
    "The closest work to ours is Ma",
    "Across the nine judging arms",
]
for pre in pres:
    i = prose.find(pre)
    if i < 0:
        print("MISS", pre)
        continue
    tail = prose[i:i + 1600]
    m = re.search(r"[.!?](?=\s+[A-Z])", tail)
    end = m.end() if m else len(tail)
    s = tail[:end]
    print("=" * 100)
    print(len(s.split()), "words")
    print(s[:1300])
    print()
