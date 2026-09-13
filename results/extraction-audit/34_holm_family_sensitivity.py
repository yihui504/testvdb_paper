"""Round-14 sensitivity: Holm-adjusted p for the flagship full-vs-flat test as
a function of the correction family's composition.

Family members (raw exact McNemar p, all on the same 81-candidate pool unless
noted): core-vs-flat, core-vs-D-only, core-vs-full (all <1e-4); full-vs-flat
0.0072; D-only-Qwen-vs-flat 0.0075; D-only-vs-flat 0.041; full-vs-D-only 0.549.
Sensitivity analyses: forced-verdict pair 0.51, joint-vs-flat 1.0, and the
second-family full-vs-flat pair 1.0 (different data)."""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CORE = [("<0.0001", 1e-7)] * 3
FAMILY7 = ([("core-vs-flat", 6e-8), ("core-vs-D-only", 3e-9),
            ("core-vs-full", 7e-11), ("full-vs-flat", 0.0072),
            ("D-only-Qwen-vs-flat", 0.0075), ("D-only-vs-flat", 0.0414),
            ("full-vs-D-only", 0.549)])
EXTRA = [("forced-verdict pair", 0.51), ("joint-vs-flat", 1.0),
         ("second-family full-vs-flat", 1.0)]


def holm_flagship(tests):
    """Return the flagship's (rank, multiplier, adjusted p) under Holm."""
    s = sorted(tests, key=lambda t: t[1])
    n = len(s)
    prev = 0.0
    for k, (name, p) in enumerate(s):
        mult = n - k
        adj = min(1.0, max(prev, p * mult))
        prev = adj
        if name == "full-vs-flat":
            return k + 1, mult, adj
    return None


for extra_n in (0, 2, 3):
    tests = FAMILY7 + EXTRA[:extra_n]
    rank, mult, adj = holm_flagship(tests)
    label = {0: "declared family (7 confirmatory tests)",
             2: "+ forced & joint sensitivity pairs (9)",
             3: "+ second-family replication (10, maximal)"}[extra_n]
    print(f"{label:44s} n={len(tests):2d}  flagship rank {rank}, "
          f"multiplier {mult}, adjusted p = {adj:.4f}")
