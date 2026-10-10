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
NOTES = []
_V = json.load(open(os.path.join(HERE, 'ai_scripts', '_voice.json'), encoding='utf-8')); PRESETS = list((_V.get('presets') or {'base': 0}))
MODEL = json.load(open(os.path.join(HERE, 'ai_scripts', '_voice.json'), encoding='utf-8')).get('model_id')   # tags matter only for eleven_v3 / v4
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
    bangs = []      # one '!' per video is allowed, at the real aha moment (teacher 2026-10-09); more reads as over-acting
    for i, sl in enumerate(a):
        for t in sl:
            t = t['say'] if isinstance(t, dict) else t
            # a short interjection ("No!") is fine (teacher 2026-10-09: "Is it adding five? No! It's dividing by two");
            # an exclamation mark ending a normal sentence: at most one per video (the aha moment)
            if '!' in re.sub(r'\b(No|Yes|Exactly|Wow|Careful)!', '', t): bangs.append('slide %d: %s' % (i + 1, t[:60]))
            if re.search(r'\bso yeah\b', t, re.I): probs.append('slide %d "So yeah"' % (i + 1))
            if not t.strip(): probs.append('slide %d empty line' % (i + 1))
            sym = re.findall(r'[πα-ωΑ-Ω°%×÷²³√≤≥≠⇒→∠◆]', t)
            if sym: probs.append('slide %d has symbol(s) %s - write them as words: %s' % (i + 1, ''.join(sym), t[:60]))
    # voice presets (segmented mode, teacher 2026-10-09 "mix 3"): "voice" names a preset in _voice.json (or a list, one per
    # part of the line between [pause] tags). Humanizers ("the— the", "um", "uh", "okay so", "sorry, ...") are fine in the
    # explanation, never in the question reading (the first line) - the student follows that word for word.
    for k, l in enumerate(flat):
        pv = l.get('voice') if isinstance(l, dict) else None
        for x in (pv if isinstance(pv, list) else [pv] if pv else []):
            if x not in PRESETS: probs.append('line %d: voice %r is not a preset in _voice.json (%s)' % (k + 1, x, ', '.join(PRESETS)))
    q0 = flat[0]['say'] if flat and isinstance(flat[0], dict) else (flat[0] if flat else '')
    if re.search(r'\b(um|uh|sorry)\b|— |\bokay so\b', q0, re.I): probs.append('line 1 (the question reading) has a humanizer - keep it clean')
    # stutters (teacher 2026-10-09): one repeated short word ("the— the", "a— a") sounds like a computer glitch - a restart
    # repeats a short phrase ("of the— of the circle", "the other— the other choices"); no fake hesitation about writing
    allt0 = ' '.join(t['say'] if isinstance(t, dict) else t for sl in a for t in sl)
    for m in re.finditer(r"((?:[A-Za-z']+\s+)?)([A-Za-z']+)\s*[—–]\s+([A-Za-z']+)(\s+[A-Za-z']+)?", allt0):
        w1, w2, n1, n2 = m.group(1).strip().lower(), m.group(2).lower(), m.group(3).lower(), (m.group(4) or '').strip().lower()
        if n1 == w2 and not (w1 and n1 == w1 and n2 == w2):      # "the— the" (one word), not "of the— of the" (a phrase)
            probs.append('single-word stutter "%s— %s" - repeat a short phrase ("of the— of the circle") or drop it' % (m.group(2), m.group(3)))
    # no humanizer self-correction about the math (teacher 2026-10-10: "slower— sorry, faster" was "bad, weird and confusing")
    for m in re.finditer(r"[A-Za-z']+\s*[—–-]+\s*sorry\b[^.?!]*", allt0, re.I):
        probs.append('self-correction "%s" - no "X— sorry, Y" humanizers (only short phrase repeats and um/uh)' % m.group(0)[:50])
    if re.search(r"let me write (that|it) down", allt0, re.I): probs.append('"let me write that down" - no fake hesitation about writing (teacher 2026-10-09)')
    if len(bangs) > 1: probs.append('%d sentences end with "!" - keep one, at the aha moment: %s' % (len(bangs), ' | '.join(bangs)))
    # delivery tags (only eleven_v3/v4 read them; voice 6 = multilingual_v2 since 2026-10-09 reads none, ai_narrate drops
    # them and turns [pause]/[short pause] into <break>): never [excited] (teacher 2026-10-09: "a bit too exaggerated");
    # on v3/v4 mild tags ([calmly], [matter-of-fact]) at most 3 per video. Words with US/UK variants: use plain words.
    allt = ' '.join(t['say'] if isinstance(t, dict) else t for sl in a for t in sl)
    # numbers like 360 / 180 are said the teacher's way: "three sixty", "one eighty" (teacher 2026-10-09)
    if re.search(r'\b(one|two|three) hundred (and )?(twenty|forty|sixty|eighty)\b', allt, re.I): NOTES.append('%s says e.g. "three hundred sixty" (teacher: "three sixty")' % vid)
    tags = re.findall(r'\[([a-z][a-z -]*)\]', allt)
    tags = [x for x in tags if x not in ('pause', 'short pause', 'long pause')]
    if 'excited' in tags: probs.append('[excited] tag - the teacher found it too exaggerated; use wording instead')
    if not re.match(r'eleven_v[34]', MODEL or ''):
        if tags: NOTES.append('%s %s ignored by %s (dropped before sending)' % (vid, tags, MODEL))
    elif len(tags) > 3: probs.append('%d delivery tags %s - at most 3 per video' % (len(tags), tags))
    risky = re.findall(r'\b(vases?|tomato(?:es)?|routes?|either|neither|schedules?|herbs?|aluminum|aluminium|leisure|garage|privacy|vitamins?|yogurt|controversy|niche|tuna)\b', allt, re.I)
    if risky: NOTES.append('%s %s' % (vid, sorted(set(w.lower() for w in risky))))     # a note, not a failure: swap when the line is next rewritten
    print(('OK   ' if not probs else 'FAIL ') + vid + ('' if not probs else '\n   ' + '\n   '.join(probs)))
    bad += bool(probs)
if NOTES: print('notes (not failures): ' + '; '.join(NOTES))
sys.exit(1 if bad else 0)
