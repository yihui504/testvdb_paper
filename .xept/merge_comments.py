#!/usr/bin/env python3
"""Git merge driver for .self_xept/comments/** — union anchors by id.

Called by git as:  merge_comments.py %O %A %B
  %O = base (ancestor), %A = ours (current branch, the file to write), %B = theirs.
Comments are append-mostly; the union is: anchors keyed by anchor_id, and within a
shared anchor its comments/replies keyed by comment id. Ours wins on shared scalar
fields (offsets, resolved state); a comment deleted on one side may resurrect on a
union — an accepted limitation (deletions are rare and low-stakes).

Exit 0 on success (merged result written to %A), non-zero on failure (git then
leaves the conflict for a manual resolve).
"""

import json
import sys


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("anchors", [])
        return []
    except Exception:
        return []


def key_of(anchor):
    if not isinstance(anchor, dict):
        return None
    return anchor.get("anchor_id") or anchor.get("id")


def union_comments(a, b):
    """Union two comment/reply lists by comment id; ours wins on shared ids."""
    merged = {}
    for c in list(b or []) + list(a or []):
        if not isinstance(c, dict):
            continue
        cid = c.get("id")
        if not cid:
            continue
        merged[cid] = c  # a (ours) appended last -> wins
    return list(merged.values())


def main():
    if len(sys.argv) != 4:
        print("usage: merge_comments.py %O %A %B", file=sys.stderr)
        return 1
    base, ours, theirs = sys.argv[1], sys.argv[2], sys.argv[3]
    a = load(ours)
    b = load(theirs)
    a_by_id = {key_of(x): x for x in a if key_of(x)}
    b_by_id = {key_of(x): x for x in b if key_of(x)}
    out = []
    for kid, anchor in a_by_id.items():
        other = b_by_id.get(kid)
        if other is not None:
            anchor["comments"] = union_comments(anchor.get("comments"), other.get("comments"))
            anchor["replies"] = union_comments(anchor.get("replies"), other.get("replies"))
            del b_by_id[kid]
        out.append(anchor)
    # anchors only in theirs (b)
    for kid, anchor in b_by_id.items():
        out.append(anchor)
    # keep anchors without a stable id (shouldn't happen) — append a's then b's
    for x in a:
        if not key_of(x):
            out.append(x)
    for x in b:
        if not key_of(x):
            out.append(x)
    with open(ours, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
