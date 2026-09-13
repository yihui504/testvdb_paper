import json, glob
for pat in ("icon-inferring*", "restinfer-inferring*"):
    for f in sorted(glob.glob(".paperpilot/literature/bib-cache/%s*.candidates.json" % pat)):
        d = json.load(open(f, encoding="utf-8"))
        for r in d["records"][:2]:
            print({k: r.get(k) for k in ("title", "authors", "year", "venue", "doi")})
        print("---", f.split("/")[-1][:40])
