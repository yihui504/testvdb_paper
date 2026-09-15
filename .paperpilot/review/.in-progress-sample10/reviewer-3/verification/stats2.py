import re

PATH = r"c:\Users\11428\Desktop\testvdb_paper\TestVDB-v10.tex"
raw = open(PATH, encoding="utf-8").read()
body = raw.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("%"))
body = re.sub(r"\\begin\{table\}.*?\\end\{table\}", " ", body, flags=re.S)
body = body.split(r"\bibliographystyle", 1)[0]
for cmd in ["textbf", "emph", "texttt", "textit", "textsc", "url", "system", "caption", "subsection", "section"]:
    for _ in range(6):
        body = re.sub(r"\\%s\{([^{}]*)\}" % cmd, r" \1 ", body)
body = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?", " ", body)
body = body.replace("~", " ").replace("---", " - ").replace("--", "-")
body = re.sub(r"\$([^$]*)\$", r" \1 ", body)
body = re.sub(r"[{}]", " ", body)
for k in ["e.g.", "i.e.", "et al.", "vs.", "cf.", "No.", "Proc.", "Sect.", "Fig.", "Sec.", "Milvus\n"]:
    body = body.replace(k, k.replace(".", "<D>"))
body = re.sub(r"(\d)\.(\d)", r"\1<D>\2", body)
body = re.sub(r"\s+", " ", body)
sents = []
for p in re.split(r"(?<=[.!?])\s+(?=[A-Z(\u201c\"'])", body):
    s = p.strip()
    s = s.replace("<D>", ".")
    s = re.sub(r"^[-*\s]+", "", s)
    if len(s.split()) >= 5:
        sents.append(s)
lens = sorted(len(s.split()) for s in sents)
n = len(lens)
print("sentences(>=5w):", n)
print("mean:", round(sum(lens) / n, 1), "median:", lens[n // 2])
print("p75:", lens[int(n * .75)], "p90:", lens[int(n * .90)], "p95:", lens[int(n * .95)], "max:", lens[-1])
print(">=50w:", sum(1 for x in lens if x >= 50), "| >=60w:", sum(1 for x in lens if x >= 60), "| >=70w:", sum(1 for x in lens if x >= 70))
print("share >=60w: %.1f%%" % (100 * sum(1 for x in lens if x >= 60) / n))
# raw token count of file
print("raw tokens in .tex:", len(raw.split()))
