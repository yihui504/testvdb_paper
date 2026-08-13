import os, collections
paths = []
for root, _, files in os.walk('run/results'):
    if 'dev_review.json' in files:
        p = os.path.join(root, 'dev_review.json').replace(os.sep, '/')
        paths.append(p)
print('total dev_review.json:', len(paths))
cnt = collections.Counter()
for p in paths:
    parts = p.split('/')
    vendor = parts[-5]
    num = parts[-3]
    cnt[(vendor, num)] += 1
dups = [(k, v) for k, v in cnt.items() if v > 1]
print('dups:', dups)
for k, n in dups:
    print(k, ':')
    for p in paths:
        pr = p.split('/')
        if pr[-5] == k[0] and pr[-3] == k[1]:
            print('   ', p)
