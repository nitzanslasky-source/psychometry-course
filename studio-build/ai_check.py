"""ai_check.py [videoId ...] : check that ai_scripts/<videoId>.json lines up with the video in the built studio —
same number of slides, and on every slide the same number of spoken lines as the video has (one AI line per original
spoken line, same order). Also flags style slips the teacher rejected (exclamation marks other than a short 'No!', 'So yeah', symbols the
TTS spells out: π α β ° % × ÷ ² √ - write them as words)."""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('SRC', os.path.expanduser('~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html'))
s = open(SRC, encoding='utf-8').read(); k = s.find('window.COURSE=') + len('window.COURSE=')
D = json.JSONDecoder().raw_decode(s[k:])[0]
ids = sys.argv[1:] or [os.path.basename(p)[:-5] for p in sorted(glob.glob(os.path.join(HERE, 'ai_scripts', '*.json'))) if not os.path.basename(p).startswith('_')]
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
    # cues (APPEAR / POINT / DRAW) right before each spoken line: an AI line's `at` list times them (ai_narrate.py)
    cues = []
    for b in v['beats']:
        n = 0
        for l in b['lines']:
            if l.get('say'): cues.append(n); n = 0
            else: n += 1
    flat = [l for sl in a for l in sl]
    for k, l in enumerate(flat):
        if isinstance(l, dict):
            if not isinstance(l.get('say'), str): probs.append('line %d: an object line needs "say"' % (k + 1))
            at = l.get('at') or []
            if k < len(cues) and len(at) > cues[k]:
                probs.append('line %d: %d "at" phrases but only %d cues before it' % (k + 1, len(at), cues[k]))
            for ph in at:
                prev = flat[k - 1] if k else ''
                prev = prev['say'] if isinstance(prev, dict) else prev
                if ph is not None and ph.startswith('<'):
                    if ph[1:].lower() not in prev.lower(): probs.append('line %d: "at" phrase %r is not in the previous line' % (k + 1, ph))
                elif ph is not None and ph.lower() not in (l.get('say') or '').lower():
                    probs.append('line %d: "at" phrase %r is not in the line' % (k + 1, ph))
    for i, sl in enumerate(a):
        for t in sl:
            t = t['say'] if isinstance(t, dict) else t
            # a short interjection ("No!") is fine (teacher 2026-10-09: "Is it adding five? No! It's dividing by two");
            # an exclamation mark ending a normal sentence is not
            if '!' in re.sub(r'\b(No|Yes|Exactly|Wow|Careful)!', '', t): probs.append('slide %d has "!": %s' % (i + 1, t[:60]))
            if re.search(r'\bso yeah\b', t, re.I): probs.append('slide %d "So yeah"' % (i + 1))
            if not t.strip(): probs.append('slide %d empty line' % (i + 1))
            sym = re.findall(r'[πα-ωΑ-Ω°%×÷²³√≤≥≠⇒→∠◆]', t)
            if sym: probs.append('slide %d has symbol(s) %s - write them as words: %s' % (i + 1, ''.join(sym), t[:60]))
    print(('OK   ' if not probs else 'FAIL ') + vid + ('' if not probs else '\n   ' + '\n   '.join(probs)))
    bad += bool(probs)
sys.exit(1 if bad else 0)
