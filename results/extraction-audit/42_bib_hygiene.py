"""Round-15 bibliography hygiene: list uncited entries, fix the DocPrism
placeholder author, drop the duplicate LlamaRestTest entry, add Zheng et al."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BIB = "TestVDB.bib"
TEX = "TestVDB.tex"

bib = open(BIB, encoding="utf-8").read()
tex = open(TEX, encoding="utf-8").read()

keys = re.findall(r"@\w+\{([^,]+),", bib)
cited = set()
for m in re.finditer(r"\\cite[a-z]*\{([^}]*)\}", tex):
    for k in m.group(1).split(","):
        cited.add(k.strip())
uncited = [k for k in keys if k not in cited]
print(f"bib entries {len(keys)}; cited {len(cited)}; uncited {len(uncited)}")
print("uncited:", " ".join(uncited))
print("cited-but-missing-from-bib:", " ".join(sorted(cited - set(keys))))

# 1. DocPrism author placeholder -> verified authors (arXiv:2511.00215)
old_author = "  author    = {{DocPrism authors}},"
new_author = ("  author    = {Xu, Xiaomeng and Wahab, Zahin and "
              "Holmes, Reid and Lemieux, Caroline},")
assert old_author in bib, "DocPrism placeholder not found"
bib = bib.replace(old_author, new_author)

# 2. drop the duplicate, uncited LlamaRestTest entry
m = re.search(r"@inproceedings\{kim2025llamaresttest,.*?\n\}\n", bib, re.S)
assert m, "kim2025llamaresttest entry not found"
bib = bib.replace(m.group(0), "")
bib = re.sub(r"\n{3,}", "\n\n", bib)

# 3. add Zheng et al. (NeurIPS 36, 2023; verified via search)
zheng = """
@inproceedings{zheng23judge,
  author    = {Zheng, Lianmin and Chiang, Wei-Lin and Sheng, Ying and
               Zhuang, Siyuan and Wu, Zhanghao and Zhuang, Yonghao and
               Lin, Zi and Li, Zhuohan and Li, Dacheng and Xing, Eric P. and
               Zhang, Hao and Gonzalez, Joseph E. and Stoica, Ion},
  title     = {Judging {LLM}-as-a-Judge with {MT-Bench} and {Chatbot Arena}},
  booktitle = {Advances in Neural Information Processing Systems 36 ({NeurIPS})},
  pages     = {46595--46623},
  year      = {2023}
}
"""
if "zheng23judge" not in bib:
    with open(BIB, "a", encoding="utf-8") as f:
        f.write(zheng)
open(BIB, "w", encoding="utf-8").write(bib)
print("bib updated: DocPrism author fixed; duplicate removed; zheng23judge added")
