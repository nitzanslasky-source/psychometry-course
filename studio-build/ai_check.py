"""ai_check.py [videoId ...] : check that ai_scripts/<videoId>.json lines up with the video in the built studio —
same number of slides, and on every slide the same number of spoken lines as the video has (one AI line per original
spoken line, same order). Also flags style slips the teacher rejected (exclamation marks, 'So yeah')."""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('SRC', os.path.expanduser('~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html'))
s = open(SRC, encoding='utf-8').read(); k = s.find('window.COURSE=') + len('window.COURSE=')
D = json.JSONDecoder().raw_decode(s[k:])[0]
ids = sys.argv[1:] or [os.path.basename(p)[:-5] for p in sorted(glob.glob(os.path.join(HERE, 'ai_scripts', 'vr*.json')))]
bad = 0
for vid in ids:
    p = os.path.join(HERE, 'ai_scripts', vid + '.json')
    if not os.path.exists(p): print('MISSING', vid); bad += 1; continue
    a = json.load(open(p, encoding='utf-8'))['slides']; v = D['videos'].get(vid)
    if not v: print('NO VIDEO', vid); bad += 1; continue
    want = [sum(1 for l in b['lines'] if l.get('say')) for b in v['beats']]
    got = [len(x) for x in a]
    probs = []
    if want != got: probs.append('lines per slide: video %s, script %s' % (want, got))
    for i, sl in enumerate(a):
        for t in sl:
            if '!' in t: probs.append('slide %d has "!": %s' % (i + 1, t[:60]))
            if re.search(r'\bso yeah\b', t, re.I): probs.append('slide %d "So yeah"' % (i + 1))
            if not t.strip(): probs.append('slide %d empty line' % (i + 1))
    print(('OK   ' if not probs else 'FAIL ') + vid + ('' if not probs else '\n   ' + '\n   '.join(probs)))
    bad += bool(probs)
sys.exit(1 if bad else 0)
