"""Exact word counts for the specific sentences Reviewer 3 quotes, plus corpus stats.

Method: read the .tex, take the body prose only (no tables/tabular/captions),
unwrap formatting commands, resolve dashes to a single token, then locate each
quoted sentence by a distinctive prefix and print its exact word count.
"""
import re

PATH = r"c:\Users\11428\Desktop\testvdb_paper\TestVDB-v10.tex"
raw = open(PATH, encoding="utf-8").read()
body = raw.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("%"))
prose = re.sub(r"\\begin\{table\}.*?\\end\{table\}", " \n\nTABLE\n\n ", body, flags=re.S)
prose = prose.split(r"\bibliographystyle", 1)[0]
prose = re.sub(r"\\caption\{[^{}]*\}", " ", prose)
for cmd in ["textbf", "emph", "texttt", "textit", "textsc", "url", "system"]:
    for _ in range(6):
        prose = re.sub(r"\\%s\{([^{}]*)\}" % cmd, r"\1", prose)
prose = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?", " ", prose)
prose = prose.replace("~", " ")
prose = re.sub(r"[{}]", " ", prose)
prose = re.sub(r"\s+", " ", prose)

MARK = "[[["  # sentences to measure, by distinctive prefix


def measure(prefix, label):
    i = prose.find(prefix)
    if i < 0:
        print(f"MISS  {label}: prefix not found -> {prefix[:60]!r}")
        return
    chunk = prose[i:]
    # cut at the sentence end: a period followed by space + capital, ignoring known abbreviations
    end = len(chunk)
    for m in re.finditer(r"[.!?](?=\s+[A-Z(\u201c])", chunk):
        cand = chunk[: m.end()]
        # skip abbreviation false hits
        if re.search(r"(?:et al|e\.g|i\.e|vs|cf|No|Proc|Sect|Fig|Sec)\.$", cand.strip()):
            continue
        end = m.end()
        break
    s = chunk[:end].strip()
    print(f"{len(s.split()):3d} words  {label}")


pairs = [
    ("The closest work to ours is Ma et al", "S-RW: 'The closest work to ours is Ma et al...' (Related Work)"),
    ("Read as a family of ten, a Holm correction", "S-4.1: Holm correction sentence"),
    ("It does not move the two controls in our favour", "S-4.1: 'It does not move the two controls...'"),
    ("Across the nine judging arms this section contrasts", "S-4.4: 'Across the nine judging arms...'"),
    ("The nineteen judgments this census closes by C=Refuted", "S-4.5: 'The nineteen judgments this census closes...'"),
    ("But the last two are the weaker kind", "S-4.5: 'But the last two are the weaker kind...'"),
    ("Aggregation is fixed, and the order in which its clauses", "S-3.5: aggregation rule"),
    ("The flat judge is the full stage's materials without", "S-4.1: flat-judge control-arm description"),
    ("Each control is a traceable edit of the arm it extends", "S-4.1: new control-arm paragraph, opener"),
    ("One artefact of the released tool meets a reader", "S-4.6: VDBFuzz artefact sentence"),
    ("Three facts make this count the census's most robust", "S-4.5: 'Three facts make this count...'"),
    ("The packages that stage reads are distilled from vendor documentation", "S-abstract: audit sentence"),
    ("Classifying the deployed stage's 243 judgments by the clause", "S-abstract: census opener"),
    ("Routing contract refutation instead of closing on it", "S-abstract: counterfactual"),
    ("It is a record of submissions and adjudication", "S-abstract: campaign scope"),
    ("In the design it is not a per-run detection rate", "S-abstract: NOT-A-SENTENCE probe"),
    ("The census covers the deployed stage on the primary backbone", "S-4.5: census scope opener"),
    ("By-design refutation must rest on verbatim intent evidence", "S-4.5: 'The protocol guards the clause...' opener"),
]
for p, lab in pairs:
    measure(p, lab)

# corpus stats over body prose, excluding TABLE blocks
paras = [re.sub(r"\s+", " ", p).strip() for p in prose.split("TABLE") if p.strip()]
sents = []
for p in paras:
    for m in re.finditer(r"[^.!?]*[.!?]", p):
        s = m.group(0).strip()
        s = re.sub(r"^(?:et al|e\.g|i\.e|vs|cf|No|Proc|Sect|Fig|Sec)\.$", "", s)
        if len(s.split()) >= 5:
            sents.append(s)
lens = sorted(len(s.split()) for s in sents)
n = len(lens)
print("\n--- body-prose sentence stats (tables excluded) ---")
print("sentences:", n, "| mean:", round(sum(lens) / n, 1), "| median:", lens[n // 2])
print("p90:", lens[int(n * 0.90)], "| max:", lens[-1])
print(">=60 words:", sum(1 for x in lens if x >= 60), "| >=70:", sum(1 for x in lens if x >= 70),
      "| >=80:", sum(1 for x in lens if x >= 80))
