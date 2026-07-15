import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import openpyxl
from collections import Counter

CLS = {
 ("chroma-core/chroma", 7375): "X",
 ("meilisearch/meilisearch", 6479): "V", ("meilisearch/meilisearch", 6480): "V", ("meilisearch/meilisearch", 6481): "V",
 ("milvus-io/milvus", 47635): "V", ("milvus-io/milvus", 47636): "V", ("milvus-io/milvus", 47729): "V",
 ("milvus-io/milvus", 47752): "V", ("milvus-io/milvus", 47755): "V", ("milvus-io/milvus", 47763): "V",
 ("milvus-io/milvus", 47766): "V", ("milvus-io/milvus", 47767): "V", ("milvus-io/milvus", 49059): "M",
 ("milvus-io/milvus", 49823): "V", ("milvus-io/milvus", 49824): "V", ("milvus-io/milvus", 49843): "V",
 ("milvus-io/milvus", 49844): "V", ("milvus-io/milvus", 49849): "V", ("milvus-io/milvus", 49850): "V",
 ("milvus-io/milvus", 49889): "V", ("milvus-io/milvus", 49890): "V", ("milvus-io/milvus", 49928): "V",
 ("milvus-io/milvus", 49929): "V", ("milvus-io/milvus", 49930): "V", ("milvus-io/milvus", 50018): "V",
 ("milvus-io/milvus", 50192): "X", ("milvus-io/milvus", 50193): "M", ("milvus-io/milvus", 50194): "X",
 ("milvus-io/milvus", 50305): "V", ("milvus-io/milvus", 50306): "V", ("milvus-io/milvus", 50307): "V",
 ("milvus-io/milvus", 50308): "V", ("milvus-io/milvus", 50309): "V", ("milvus-io/milvus", 50310): "V",
 ("milvus-io/milvus", 50311): "V", ("milvus-io/milvus", 50312): "V", ("milvus-io/milvus", 50313): "V",
 ("milvus-io/milvus", 50314): "V", ("milvus-io/milvus", 50315): "V", ("milvus-io/milvus", 50316): "V",
 ("milvus-io/milvus", 50317): "V", ("milvus-io/milvus", 50318): "V", ("milvus-io/milvus", 50319): "V",
 ("milvus-io/milvus", 50321): "V", ("milvus-io/milvus", 50322): "V", ("milvus-io/milvus", 50323): "V",
 ("milvus-io/milvus", 50324): "V", ("milvus-io/milvus", 50325): "V", ("milvus-io/milvus", 50351): "V",
 ("milvus-io/milvus", 50352): "V", ("milvus-io/milvus", 50353): "V", ("milvus-io/milvus", 50354): "V",
 ("milvus-io/milvus", 50355): "V", ("milvus-io/milvus", 51084): "V", ("milvus-io/milvus", 51085): "V",
 ("qdrant", 8688): "M", ("qdrant", 9017): "V", ("qdrant", 9027): "V", ("qdrant", 9039): "V",
 ("qdrant", 9044): "V", ("qdrant", 9045): "C", ("qdrant", 9149): "V", ("qdrant", 9255): "M",
 ("qdrant", 9364): "X", ("qdrant", 9365): "M", ("qdrant", 9366): "X", ("qdrant", 9371): "X",
 ("qdrant", 9372): "V", ("qdrant", 9373): "M", ("qdrant", 9416): "V", ("qdrant", 9417): "V",
 ("qdrant", 9418): "V", ("qdrant", 9419): "V", ("qdrant", 9420): "V", ("qdrant", 9421): "V",
 ("qdrant", 9520): "C", ("qdrant", 9521): "M", ("qdrant", 9522): "V", ("qdrant", 9523): "M",
 ("qdrant", 9524): "V", ("qdrant", 9525): "V",
 ("weaviate", 11395): "V", ("weaviate", 11396): "V", ("weaviate", 11397): "V", ("weaviate", 11398): "V",
 ("weaviate", 11399): "V", ("weaviate", 11400): "V", ("weaviate", 11401): "V", ("weaviate", 11402): "V",
 ("weaviate", 11433): "V", ("weaviate", 11436): "V", ("weaviate", 11660): "V", ("weaviate", 11661): "V",
 ("weaviate", 11729): "V", ("weaviate", 11730): "Vs", ("weaviate", 11731): "Vs", ("weaviate", 11732): "V",
 ("weaviate", 11734): "V", ("weaviate", 11735): "M", ("weaviate", 11736): "V", ("weaviate", 11737): "Vs",
 ("weaviate", 11738): "Vs", ("weaviate", 11739): "V", ("weaviate", 11740): "V", ("weaviate", 11741): "V",
 ("weaviate", 11742): "V", ("weaviate", 11743): "V", ("weaviate", 11744): "V", ("weaviate", 11745): "V",
 ("weaviate", 11981): "V", ("weaviate", 12041): "V",
}
NAME = {
    "M": "math/correctness (classical-findable)",
    "C": "crash (fuzz)",
    "X": "concurrency/atomicity/consistency (semantic)",
    "V": "pure validation & status-code compliance (LLM-only)",
    "Vs": "schema/enum/format (checkable IF OpenAPI existed)",
    "?": "ambiguous",
}

def cls_of(repo, n):
    if (repo, n) in CLS:
        return CLS[(repo, n)]
    return CLS.get((repo.split("/")[-1], n), "?")


wb = openpyxl.load_workbook("data/yihui504-issues.xlsx", read_only=True, data_only=True)
rows = list(wb["Issues"].iter_rows(values_only=True))[1:]
recs = [(r[0].split("/")[0], r[1], r[5], cls_of(r[0], r[1]), r[2], r[10]) for r in rows]
ACK = {"FIXED", "ACCEPTED_OPEN"}


def tall(rs):
    return Counter(x[3] for x in rs)


tot = tall(recs)
classical = tot["M"] + tot["C"]
resid = tot["V"] + tot["Vs"] + tot["X"]
print("=== ALL 111 ===")
for k in ["M", "C", "X", "Vs", "V", "?"]:
    print("  %-3s %-52s %d" % (k, NAME[k], tot[k]))
print("  >> classical-findable (M+C)   = %d  (%.0f%%)" % (classical, classical / 111 * 100))
print("  >> residual (V+Vs+X)          = %d  (%.0f%%)" % (resid, resid / 111 * 100))
print("  >> ambiguous (?)              = %d" % tot["?"])
print("     of residual: V=%d  Vs=%d  X=%d" % (tot["V"], tot["Vs"], tot["X"]))

ack = [x for x in recs if x[2] in ACK]
at = tall(ack)
acl = at["M"] + at["C"]
ars = at["V"] + at["Vs"] + at["X"]
print("\n=== ACKNOWLEDGED %d ===" % len(ack))
for k in ["M", "C", "X", "Vs", "V", "?"]:
    if at[k]:
        print("  %-3s %-52s %d" % (k, NAME[k], at[k]))
print("  >> classical-findable = %d/%d (%.0f%%) | residual = %d/%d (%.0f%%)" % (acl, len(ack), acl / len(ack) * 100, ars, len(ack), ars / len(ack) * 100))

print("\n=== BORDERLINES (M/X/Vs/?) to spot-check ===")
for x in recs:
    if x[3] in ("M", "X", "Vs", "?"):
        print("  [%s] %s #%s (%s): %s" % (x[3], x[0], x[1], x[2], x[4][:88]))

# artifact
L = [
    "# E1 - 111 bug fault-model first pass (title-based, 2026-07-15)", "",
    "> source = data/yihui504-issues.xlsx. M/X/Vs/? need per-issue verification.", "",
    "| class | meaning | classical-findable? |", "|---|---|---|",
    "| M | math/correctness invariant | YES (differential/metamorphic/PBT) |",
    "| C | crash | YES (fuzz) |",
    "| X | concurrency/atomicity/consistency (semantic) | PARTIAL (needs concurrent harness + semantic oracle) |",
    "| V | pure input-validation & status-code compliance | NO (LLM-as-checker only) |",
    "| Vs | schema/enum/format | ONLY IF OpenAPI exists; VDB has none -> practically LLM-only |",
    "| ? | ambiguous | needs issue look |", "",
    "| repo | issue | category | class | title | url |", "|---|---|---|---|---|---|",
]
for x in recs:
    L.append("| %s | %s | %s | %s | %s | %s |" % (x[0], x[1], x[2], x[3], x[4].replace("|", "/"), x[5]))
L += [
    "",
    "**Tally (111):** classical-findable(M+C)=%d (%.0f%%); residual(V+Vs+X)=%d (%.0f%%); ambiguous=%d" % (classical, classical / 111 * 100, resid, resid / 111 * 100, tot["?"]),
    "**Acknowledged %d:** classical-findable=%d (%.0f%%); residual=%d (%.0f%%)" % (len(ack), acl, acl / len(ack) * 100, ars, ars / len(ack) * 100),
]
open("data/e1-bug-classification.md", "w", encoding="utf-8").write("\n".join(L))
print("\n[wrote data/e1-bug-classification.md]")
