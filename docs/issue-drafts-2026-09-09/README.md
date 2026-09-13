# Issue drafts for qdrant (2026-09-09)

Three bug reports verified surviving on **v1.19.1** (commit `6ab21cac`) and
originally found on v1.18.0 (commit `db3fca3`). Evidence base:
`.../2026-09-04T12-14-11Z/defects/v1.19.1-survival-report.md` (plugin results
dir), MRE `defect-63-mre.py` (live-verified DEFECT_REPRODUCED on the 1.19.1
container, port 6335).

Each file = one issue. The `# Title` line goes into the GitHub **Add a title\***
field; everything under `# Body` goes into the **Add a description** field
(bug-report template).

## Submission order

1. `issue-1-snapshot-upload-500-path-leak.md` — 500 + internal path disclosure
   (strongest: error-classification + info-leak, deterministic on both versions)
2. `issue-2-snapshot-same-second-collision.md` — same-second snapshot name
   collision, silent loss with 200s on both creates
3. `issue-3-untagged-vectorsparse-unnamed-400.md` — untagged-enum 400 names no
   field (sparse domain)

## Pre-submission checklist

- [ ] Issue 3: search qdrant issues for `untagged enum` first. If an existing
      issue already covers the family (e.g. with_lookup), post issue 3 as a
      **comment** extending it to the sparse domain instead of opening a new one.
- [x] All three: response bodies re-verified byte-exact against the live 1.19.1
      container (6335) on 2026-09-09 15:16 local — issue 1 garbage/empty 500s
      + wrong-field 400 contrast (1.19.1 phrasing `missing "snapshot"` now in
      the draft), issue 2 concurrent double-create → two 200s, identical name,
      listing 1 entry, issue 3 sparse-missing-values 400 unnamed vs
      duplicate-indices 422 `points[0].vector.?.indices`.
- [ ] Do not reference internal artifacts (session dirs, chain files) in the
      public issues — drafts are already self-contained.
