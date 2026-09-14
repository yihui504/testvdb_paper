"""Check whether the anchor's nine dispatches all use the same protocol, and
whether that protocol matches what the paper says (full-stage / four
perspectives) or something narrower."""
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

A = r"C:\Users\11428\Desktop\TestVDB_artifact\rq2\analyses\unsubmitted-anchor"

MARKERS = {
    "claims four perspectives": "四视角",
    "no C perspective": "无 C 视角",
    "binary verdict in output": '"verdict":"CONFIRMED|FALSE_POSITIVE"',
    "insufficient -> FP": "证据不足一律",
    "human review mentioned": "HUMAN_REVIEW",
    "cognition mentioned": "COG",
    "source clone path": ".sourcedeps/qdrant/v1.18.0",
}

for f in sorted(glob.glob(os.path.join(A, "dispatch_run*.txt"))):
    txt = open(f, encoding="utf-8", errors="replace").read()
    found = {k: (v in txt) for k, v in MARKERS.items()}
    name = os.path.basename(f)
    print(f"{name}: " + ", ".join(k for k, ok in found.items() if ok))
