"""Mechanical tells check for original Verbal items. Usage: python3 lint_originals.py P41a [P41b ...]
Flags per item: key uniquely longest by >15%; en/em dashes; contractions;
singular generic 'they'; British spellings; one option text repeated verbatim in all 4 options (completion slot).
File level: share of items whose key is the longest option must be <= 0.30 (chance is 0.25)."""
import json, re, sys
C = '/Users/nitzanslasky/psychometry-course/content/verbal_originals_%s.json'
BRIT = r'\b(colour|favour|behaviour|centre|theatre|organis|realis|analys(e|ing)|travell|labour|neighbour|pupils?|shop front|bookshop|whilst|amongst|towards|catalogue)\b'
bad_total = 0
for G in sys.argv[1:]:
    d = json.load(open(C % G)); items = list(d.get('items', []))
    for p in d.get('passages', []):
        items += [dict(q, id='%s-%d' % (p['id'], k + 1)) for k, q in enumerate(p['questions'])]
    longest = 0
    for x in items:
        o = x['options']; k = x['answer'] - 1; L = [len(s) for s in o]; f = []
        others = [L[i] for i in range(4) if i != k]
        if L[k] == max(L):
            longest += 1
            if L[k] > 1.15 * max(others): f.append('key uniquely longest (%d vs %d)' % (L[k], max(others)))
        txt = x['stem'] + ' ' + ' '.join(o)
        if re.search('[–—]', txt): f.append('en/em dash')
        if re.search(r"\b\w+n't\b|\b(I'm|I've|I'll|you're|we're|they're|it's|that's)\b", txt, re.I): f.append('contraction')
        if re.search(BRIT, txt, re.I): f.append('British/avoid form: ' + re.search(BRIT, txt, re.I).group(0))
        if ' / ' in o[0]:
            slots = [s.split(' / ') for s in o]
            if all(len(s) == len(slots[0]) for s in slots):
                for j in range(len(slots[0])):
                    if len({s[j].strip() for s in slots}) == 1: f.append('slot %d identical in all options' % (j + 1))
        if f: bad_total += 1; print(G, x['id'], '; '.join(f))
    r = longest / max(1, len(items))
    print('== %s: key-is-longest share %.2f %s' % (G, r, 'OK' if r <= .30 else 'TOO HIGH (max 0.30)'))
    if r > .30: bad_total += 1
sys.exit(1 if bad_total else 0)
