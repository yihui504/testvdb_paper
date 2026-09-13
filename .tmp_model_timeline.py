import json, sys, collections
for path in sys.argv[1:]:
    per = collections.Counter()
    sc = collections.Counter()
    first = last = None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if '"model"' not in line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            m = r.get("message") or {}
            mod = m.get("model") if isinstance(m, dict) else None
            if not mod:
                continue
            ts = (r.get("timestamp") or "")[:13]
            side = bool(r.get("isSidechain"))
            per[(ts, mod, side)] += 1
            sc[(ts, side)] += 1
            if first is None or ts < first: first = ts
            if last is None or ts > last: last = ts
    print(f"### {path}  span {first} .. {last}")
    for (ts, mod, side), c in sorted(per.items()):
        print(f"  {ts}  sidechain={int(side)}  {mod:<28} {c}")
