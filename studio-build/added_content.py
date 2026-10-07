"""Manifest of content that is NOT from the teacher's Hebrew course (run inside build_verbal.py; read by studio_added.py).

Teacher request (2026-10-07): "What are the lessons, slides and techniques you added? Mark them for me in the studio so
I know to look at the script more carefully."

How an item is found (topics 1-38, the math that exists in base-v18.html = the English course before any additions):
- Added video: the built video id is not in the base, and its slides do not mostly match one base video (a rebuilt /
  renamed copy of a base video is compared slide by slide instead, like a base video).
- Added slide: a slide of a video whose text has no counterpart in the base. Counterpart = a base slide of the same video,
  or (content that moved) any base slide of the same or a neighbouring topic, whose words cover most of this slide's
  words after normalising: lower case, every number (digits, decimals, fractions, number words) -> '#', TeX commands
  and one-letter names dropped. So renumbered slides (new numbers, other letters, a tweaked story) and cut / shortened
  slides are not additions.
Topics 39-52 are built from modules (the teacher's Hebrew verbal / psychometric-thinking / writing / charts material;
the base holds an older version under other ids), so there is no base to compare with. There only the explicit list
below counts (topic 51, "Picking values that fit", added 2026-10-06 in modulesV51.py).

Each added item gets a label (source + method):
- "New exam method · <name>" - from METHODS: the videos / slides that add_methods (math_patches/tNN.py, 2026-10-06,
  logged under "2026-10-06 new exam methods" in tNN_CHANGES.md) created or appended to, plus topic 51 Case 4.
- "Added in the September review" - an r26 video / question, or a slide inserted into an existing lesson by the
  course review (math_patches; the review ran 2026-09 to 2026-10).
- "Added (not in your Hebrew course)" - anything else found by the comparison.
METHODS entries with kind 'lines' mark slides that already existed but got new-method lines (no new slide); they get a
milder "lines added" banner, since the teacher still has to read them.

Line level (2026-10-07, "point out WHAT you added"): in a slide that matches its base slide (the teacher's own), every
spoken / drawn line and board item is compared with the lines and items of the base video (new_lines): numbers -> '#',
names dropped, and a line counts as the teacher's when most of its words are in one base line, in the base slide, or it
is the same sentence with a few words swapped. The rest are "new lines on your slide" (rec['lines']).
attach_notes() adds what each added video / slide / line set teaches, from added_notes.json.

Output: manifest(D, base) -> {videoId: {topic, title, added, label, method, slides: {beatIndex: {title, label, kind}}}}
and markdown(...) for ~/Downloads/Added-Content-List.md.
"""
import re, difflib, json, os

SEPT = 'Added in the September review'
OTHER = 'Added (not in your Hebrew course)'
GUIDE = 'studio-build/real_exam/method_search/TEACHER_GUIDE.md'

# (video id, slide title or '*' for the whole video, method name, kind) - from the "2026-10-06 new exam methods"
# sections of math_patches/tNN_CHANGES.md and modulesV51.py.  kind: 'new' = new video / new slide, 'lines' = an older
# slide that got new-method lines.
METHODS = [
    # 5 · power count
    ('r26-t05-power-count', '*', 'Power count', 'new'),
    ('solve-q-r26-t05-17', '*', 'Power count', 'new'),
    ('solve-q-r26-t05-18', '*', 'Power count', 'new'),
    ('r26-t05-summary', 'Count the powers', 'Power count', 'new'),
    # 11 · given power -> asked power
    ('solve-q-r26-t11-13', '*', 'Given power → asked power', 'new'),
    # 12 · ranges in two moves
    ('inequalities', 'Ranges in two moves', 'Ranges in two moves', 'new'),
    ('solve-q-322', 'Method 2 · Two moves', 'Ranges in two moves', 'lines'),
    ('solve-q-r26-t12-13', '*', 'Ranges in two moves', 'new'),
    # 13 · mirror test
    ('r26-t13-mirror', '*', 'Mirror test', 'new'),
    ('solve-q-r26-t13-15', '*', 'Mirror test', 'new'),
    ('solve-q-368', 'Method 3 · Plug in', 'Mirror test', 'lines'),
    # 15 · tag it
    ('r26-t15-remainder-tools', 'Tag it', 'Tag it', 'new'),
    ('solve-q-r26-t15-15', '*', 'Tag it', 'new'),
    # 18 · digit word equations (digit ratio)
    ('digit-puzzles', 'The 4 steps', 'Digit ratio (10A + B equations)', 'lines'),
    ('r26-t18-summary', 'The 4 steps', 'Digit ratio (10A + B equations)', 'lines'),
    ('solve-q-520', 'Method 1 · Algebraic form', 'Digit ratio (10A + B equations)', 'lines'),
    # 23 · flip rule, arrow map
    ('wp-052', 'Same part: flip', 'Flip rule', 'new'),
    ('wp-052', 'Same whole: keep', 'Flip rule', 'new'),
    ('solve-q-r26-t23-16', '*', 'Flip rule', 'new'),
    ('wp-053', 'The arrow map', 'Arrow map', 'new'),
    ('wp-053', 'Walk the path', 'Arrow map', 'new'),
    # 25 · percent shares as weights
    ('solve-wp25-g089', 'Shares as weights', 'Percent shares as weights', 'new'),
    # 26 · compare by factors, catching up
    ('r26-t26-factors', '*', 'Compare by factors', 'new'),
    ('solve-q-r26-t26-21', '*', 'Compare by factors', 'new'),
    ('solve-wp26-g102', 'Same idea: catching up', 'Catching up', 'new'),
    # 27 · the V in motion
    ('wp-110', 'Two things change? The V', 'The V in motion', 'new'),
    ('solve-q-r26-t27-31', '*', 'The V in motion', 'new'),
    ('wp-106', 'The table', 'The V in motion (Speed · Distance · Time table)', 'lines'),
    # 28 · counting pointer
    ('wp-123', 'At most? At least?', 'Counting pointer (at most / at least → Topic 21)', 'new'),
    # 29 · which door?
    ('r26-t29-summary', 'Which door?', 'Which door?', 'new'),
    # 51 · pick values that fit (modulesV51.py, 2026-10-06)
    ('pt51-plug-numbers', 'Case 4: pick values', 'Pick values that fit', 'new'),
    ('pt51-plug-numbers', 'Pick values: watch out', 'Pick values that fit', 'new'),
    ('pt51-plug-numbers', 'Nothing-changes value', 'Pick values that fit', 'new'),
    ('solve-pt-q24', '*', 'Pick values that fit', 'new'),
]

MATH_TOPICS = range(1, 39)
LINES = 'New lines in your slides'


# ---------- line level: spoken lines / board items added into a slide of the teacher's ----------
LINE_MIN = 3         # a line with fewer content words ("Choice two.") is never counted as added
LINE_COVER = 0.5     # a line whose words are >= 50% in one line of the base video is the teacher's (maybe reworded)
LINE_SLIDE = 0.7     # ... or >= 70% in the whole base slide (lines merged / split)
ITEM_COVER = 0.6


def _line_text(l):
    return l.get('say') if l.get('say') is not None else l.get('draw')


def _item_text(it):
    out = []; _strings(it, out); return ' '.join(out)


SHAPE = 0.7          # ... or >= 70% the same characters as one base line, after numbers -> '#' and names -> 'N'


def _shape(t):
    t = re.sub(r"\b[A-Z][a-z]+(?:'s)?\b", 'N', t).lower()
    t = re.sub(r'\d+(?:[.,]\d+)*', '#', t)
    t = re.sub(r'\b(?:%s)\b' % '|'.join(sorted(_NUMW, key=len, reverse=True)), '#', t)
    t = re.sub(r'#(?:[\s-]*#)+', '#', t)
    return re.sub(r'\s+', ' ', t).strip()


def ltokens(t):
    """tokens of a spoken line, without names (capitalised words): a renamed story ("Maya" for "Dana") is not new."""
    return tokens(re.sub(r"\b[A-Z][a-z]+(?:'s)?\b", ' ', t))


def new_lines(b, bb, BV, Q=None, QB=None):
    """Lines of slide b (built) that are not in its base counterpart bb (base video BV).  Numbers are normalised, so a
    renumbered line is not new; a line counts as the teacher's when most of its words are in one base line of the
    video (it may have moved) or in the base slide.  Returns {'say': [i...], 'draw': [i...], 'items': [k...]} with
    indexes into b['lines'] / b['items'], or None."""
    base_lines, base_texts = [], []
    for x in BV.get('beats') or []:
        for l in x.get('lines') or []:
            t = _line_text(l)
            if t: base_lines.append(ltokens(t)); base_texts.append(t)
        if isinstance(x.get('script'), str):
            for t in re.split(r'(?<=[.!?])\s+|\n+', x['script']):
                if t.strip(): base_lines.append(ltokens(t))
        for it in x.get('items') or []: base_lines.append(tokens(_item_text(it)))
        _b = []; _strings(x.get('board') or [], _b)
        for t in _b: base_lines.append(ltokens(t))
    whole = tokens(slide_raw(bb, QB)) | ltokens(slide_raw(bb, QB))
    base_items = [ltokens(_item_text(it)) for x in BV.get('beats') or [] for it in x.get('items') or [] if it.get('k') != 'q']

    shapes = [_shape(t) for t in base_texts]

    def is_new(n, pool, thr, text=None):
        if len(n) < LINE_MIN: return False
        if cover(n, whole) >= LINE_SLIDE: return False
        if any(cover(n, x) >= thr for x in pool): return False
        if text is not None:                               # the same sentence with a few words swapped (a tweaked story)
            sh = _shape(text)
            for x in shapes:
                sm = difflib.SequenceMatcher(None, sh, x, autojunk=False)
                if sm.real_quick_ratio() >= SHAPE and sm.quick_ratio() >= SHAPE and sm.ratio() >= SHAPE: return False
        return True

    out = {'say': [], 'draw': [], 'items': []}
    for i, l in enumerate(b.get('lines') or []):
        t = _line_text(l)
        if t and is_new(ltokens(t), base_lines, LINE_COVER, t): out['say' if l.get('say') is not None else 'draw'].append(i)
    for k, it in enumerate(b.get('items') or []):
        if it.get('k') == 'q': continue
        if is_new(ltokens(_item_text(it)), base_items + base_lines, ITEM_COVER): out['items'].append(k)
    return out if (out['say'] or out['draw'] or out['items']) else None

# ---------- text of a slide ----------
_NUMW = set('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen '
            'seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million '
            'half halves third thirds quarter quarters fifth fifths sixth sixths eighth eighths tenth tenths twice '
            'double triple first second third fourth fifth sixth seventh eighth ninth tenth once'.split())
_STOP = set('the a an and or of to in is it on at as be by for so we you i that this then than with what are was were '
            'its it\'s our your my me us he she they them his her their there here not no yes do does did can will '
            'just now one all each every if from into out up down more less which who how why when where'.split())
_SKIP_KEYS = {'k', 'id', 'qid', 'pid', 'color', 'col', 'size', 'w', 'h', 'x', 'y', 'band', 'hideok', 'src', 'paras',
              'font', 'align', 'fig', 'svg', 'img', 'style'}


def _strings(x, out):
    if isinstance(x, str): out.append(x)
    elif isinstance(x, list):
        for y in x: _strings(y, out)
    elif isinstance(x, dict):
        for k, y in x.items():
            if k not in _SKIP_KEYS: _strings(y, out)


def slide_raw(b, Q=None):
    out = [b.get('title') or '', b.get('bigTitle') or '']
    for l in b.get('lines') or []:
        for k in ('say', 'label', 'draw'):
            if isinstance(l.get(k), str): out.append(l[k])
    for it in b.get('items') or []:
        _strings(it, out)
        if Q is not None and it.get('k') == 'q' and it.get('qid') in Q:
            q = Q[it['qid']]; out.append(q.get('stemRich') or q.get('stem') or '')
    if isinstance(b.get('script'), str): out.append(b['script'])
    _strings(b.get('board') or [], out)
    return ' '.join(out)


def tokens(t):
    t = t.lower()
    t = re.sub(r'\\[a-z]+', ' ', t)                       # TeX commands
    t = re.sub(r'\d+(?:[.,]\d+)*', ' # ', t)               # numbers
    t = re.sub(r'[’\']s\b', '', t)
    ws = re.findall(r'[a-z#]+', t)
    return {('#' if w in _NUMW else w) for w in ws if (len(w) > 1 or w == '#') and w not in _STOP}


def cover(n, b):
    """share of the new slide's words that the base slide has (1 = all)."""
    return len(n & b) / len(n) if n else 1.0


def _norm_title(t):
    return re.sub(r'[\d#]+', '#', re.sub(r'[^a-z0-9#]+', ' ', (t or '').lower())).strip()


MATCH = 0.6          # same video: a slide whose words are >= 60% in one base slide of that video is not new
MATCH_FAR = 0.7      # content that moved (other video, same / neighbouring topic): stricter
WEAK = 0.3           # a rewrite in the place of a base slide (see counterparts)


def counterparts(N, L, nt, bt):
    """For each new slide: does it have a counterpart in the base video?  1) strong matches (cover >= MATCH) aligned in
    order (a slide may move a little, so any strong match counts);  2) between two aligned slides, a new slide that takes
    the place of an unmatched base slide in the same gap is a rewrite of it (cover >= WEAK, or the same title) - not an
    addition.  A new slide in a gap where the base had nothing left over is an insertion."""
    n, m = len(N), len(L)
    S = [[cover(N[i], L[j]) for j in range(m)] for i in range(n)]
    # longest chain of strong matches (DP, maximise total score)
    best = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            best[i][j] = max(best[i + 1][j], best[i][j + 1], (S[i][j] + best[i + 1][j + 1]) if S[i][j] >= MATCH else 0)
    pair, i, j = {}, 0, 0
    while i < n and j < m:
        if S[i][j] >= MATCH and abs(best[i][j] - (S[i][j] + best[i + 1][j + 1])) < 1e-9: pair[i] = j; i += 1; j += 1
        elif best[i][j] == best[i + 1][j]: i += 1
        else: j += 1
    used = set(pair.values())
    have = [i in pair or any(S[i][j] >= MATCH for j in range(m)) for i in range(n)]
    match = dict(pair)
    for i in range(n):
        if have[i] and i not in match: match[i] = max(range(m), key=lambda j: S[i][j])
    # gaps
    anchors = [(-1, -1)] + sorted(pair.items()) + [(n, m)]
    for (a0, b0), (a1, b1) in zip(anchors, anchors[1:]):
        free = [j for j in range(b0 + 1, b1) if j not in used]
        for i in range(a0 + 1, a1):
            if have[i] or not free: continue
            j = max(free, key=lambda j: S[i][j] + (1 if nt[i] and nt[i] == bt[j] else 0))
            if S[i][j] >= WEAK or (nt[i] and nt[i] == bt[j]):
                have[i] = True; free.remove(j); used.add(j); match[i] = j
    # a slide that moved (e.g. Method 3 became Method 1): same title (without "Method N ·") as an unused base slide
    core = lambda t: re.sub(r'^method # ', '', t or '')
    for i in range(n):
        if have[i] or not core(nt[i]): continue
        js = [j for j in range(m) if j not in used and core(bt[j]) == core(nt[i]) and S[i][j] >= WEAK]
        if js: have[i] = True; used.add(js[0]); match[i] = js[0]
    return have, match


def plain_title(v):
    t = v.get('title') or ''
    if v.get('questionId') or '\\' in t or '$' in t:
        t = re.sub(r'\\(?:text|mathrm|textbf)\{([^}]*)\}', r'\1', t)
        t = re.sub(r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}', r'(\1)/(\2)', t)
        t = re.sub(r'\\(?:left|right|begin\{[a-z]*\}(?:\{[^}]*\})?|end\{[a-z]*\}|quad|qquad|,|;|!)', ' ', t)
        t = re.sub(r'\\\\(?:\[[^]]*\])?', '; ', t)
        t = t.replace('\\cdot', '·').replace('\\ne', '≠').replace('\\le', '≤').replace('\\ge', '≥').replace('\\pi', 'π')
        t = re.sub(r'\\[a-zA-Z]+', ' ', t).replace('$', '').replace('&', ' ')
        t = re.sub(r'[{}]', '', t)
        t = re.sub(r'\s+', ' ', t).strip()
        if len(t) > 90: t = t[:88].rstrip() + '…'
        if v.get('questionId'): t = 'Solution · ' + t
    return t


def manifest(D, B, review_ids=()):
    """D = built course, B = base-v18 course, review_ids = videos the course review (math_patches) touched."""
    review_ids = set(review_ids)
    Q, QB = D.get('questions', {}), B.get('questions', {})
    base_slides = {}                                       # topic -> [(videoId, beatIdx, tokens, normTitle)]
    btok = {}
    for vid, v in B['videos'].items():
        if v.get('topic') not in MATH_TOPICS: continue
        L = btok[vid] = []
        for k, b in enumerate(v.get('beats') or []):
            tk = tokens(slide_raw(b, QB)); L.append(tk)
            base_slides.setdefault(v['topic'], []).append((vid, k, tk))

    meth = {}
    for vid, sl, name, kind in METHODS: meth.setdefault(vid, []).append((sl, name, kind))
    warn = []
    for vid, ents in meth.items():
        v = D['videos'].get(vid)
        if not v: warn.append('METHODS: video %s not in the course' % vid); continue
        titles = [b.get('title') for b in v['beats']]
        for sl, name, kind in ents:
            if sl != '*' and sl not in titles: warn.append('METHODS: slide "%s" not in %s' % (sl, vid))

    flow_vids = [f['ref'] for f in D['flow'] if f['type'] == 'video']
    in_course = set(flow_vids)
    seen, M = set(), {}
    for vid in flow_vids:
        if vid in seen: continue
        seen.add(vid)
        v = D['videos'].get(vid)
        if not v: continue
        t = v.get('topic'); beats = v.get('beats') or []
        ents = meth.get(vid, [])
        whole = next((e for e in ents if e[0] == '*'), None)
        rec = dict(topic=t, title=plain_title(v), group=v.get('navLabel'), added=False, label=None, method=None, slides={}, rebuilt=None, lines={})

        def lab_for(title, default):
            e = next((e for e in ents if e[0] == title), None) or whole
            if e: return 'New exam method · ' + e[1], e[1], e[2]
            return default, None, 'new'

        if t in MATH_TOPICS:
            toks = [tokens(slide_raw(b, Q)) for b in beats]
            ref = vid if vid in btok else None
            if ref is None:                                # renamed / rebuilt copy of a base video?
                best, bs = None, 0
                for bvid, L in btok.items():
                    if B['videos'][bvid]['topic'] not in (t - 1, t, t + 1) or bvid in in_course: continue   # only a base video that is gone
                    hit = sum(1 for n in toks if any(cover(n, x) >= MATCH for x in L))
                    if hit > bs: best, bs = bvid, hit
                if beats and bs >= max(2, 0.6 * len(beats)): ref = best; rec['rebuilt'] = best
            src = SEPT if ('r26' in vid or 'r26' in (v.get('questionId') or '') or vid in review_ids) else OTHER
            if ref is None:
                rec['added'] = True
                rec['label'], rec['method'], _ = lab_for('*', src)
                for k, b in enumerate(beats):
                    l, m, kind = lab_for(b.get('title'), src)
                    rec['slides'][k] = dict(title=b.get('title') or b.get('bigTitle'), label=l, method=m, kind='new')
            else:
                L = btok[ref]
                far = [x for tt in (t - 1, t, t + 1) for x in base_slides.get(tt, [])]
                have, match = counterparts(toks, L, [_norm_title(b.get('title')) for b in beats],
                                    [_norm_title(b.get('title')) for b in B['videos'][ref]['beats']])
                for k, b in enumerate(beats):
                    n = toks[k]
                    e = next((e for e in ents if e[0] == b.get('title')), None)
                    if have[k] or any(cover(n, x[2]) >= MATCH_FAR for x in far if x[0] != ref):
                        if have[k] and k in match:         # the teacher's slide: spoken lines / board items added into it
                            nl = new_lines(b, B['videos'][ref]['beats'][match[k]], B['videos'][ref], Q, QB)
                            if nl: rec['lines'][k] = nl
                        if e and e[2] == 'lines':
                            rec['slides'][k] = dict(title=b.get('title'), label='New exam method · ' + e[1],
                                                    method=e[1], kind='lines')
                        elif e:                            # listed as a new slide but its words exist in the base
                            warn.append('METHODS: %s / "%s" matches base text - kept as added (listed)' % (vid, b.get('title')))
                            rec['slides'][k] = dict(title=b.get('title'), label='New exam method · ' + e[1], method=e[1], kind='new')
                        continue
                    l, m, kind = lab_for(b.get('title'), SEPT)
                    if kind == 'lines': l = 'New exam method · ' + m      # whole slide new after all
                    rec['slides'][k] = dict(title=b.get('title') or b.get('bigTitle'), label=l, method=m, kind='new')
        else:                                              # module topics: explicit list only
            if whole:
                rec['added'] = True; rec['label'] = 'New exam method · ' + whole[1]; rec['method'] = whole[1]
            for k, b in enumerate(beats):
                e = next((e for e in ents if e[0] == b.get('title')), None) or whole
                if e: rec['slides'][k] = dict(title=b.get('title') or b.get('bigTitle'), label='New exam method · ' + e[1], method=e[1], kind=e[2] if e is not whole else 'new')
        for k in list(rec['lines']):                       # a slide that is new as a whole is not "lines added"
            if rec['slides'].get(k, {}).get('kind') == 'new': del rec['lines'][k]
        if rec['added'] or rec['slides'] or rec['lines']:
            if not rec['added'] and not rec['slides']:
                rec['label'] = LINES
            elif not rec['added']:
                ms = sorted({s['method'] for s in rec['slides'].values() if s['method']})
                other = sorted({s['label'] for s in rec['slides'].values() if not s['method']})
                rec['label'] = (('New exam method · ' + ', '.join(ms)) + ((' — plus: ' + ', '.join(other)) if other else '')) if ms else (other[0] if len(other) == 1 else ', '.join(other) or SEPT)
            M[vid] = rec
    return M, warn


# ---------- what each added item teaches (added_notes.json, written once from the slides' board items + spoken lines) ----------
NOTES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'added_notes.json')

# teacher guide section for each new exam method (studio-build/real_exam/method_search/TEACHER_GUIDE.md,
# also ~/Downloads/New-Exam-Methods-Teacher-Guide.md)
GUIDE_SECTIONS = {
    'Power count': 'Topic 5 — Count the Powers',
    'Given power → asked power': 'Topics 10–11 — Given power → asked power',
    'Ranges in two moves': 'Topic 12 — 1. Ranges in two moves',
    'Mirror test': 'Topic 13 — The Mirror Test',
    'Tag it': 'Topic 15 — Tag it (guaranteed factors)',
    'Digit ratio (10A + B equations)': 'Topic 18 — Digit word equations',
    'Flip rule': 'Topic 23 — 1. The flip rule',
    'Arrow map': 'Topic 23 — 2. The arrow map',
    'Percent shares as weights': 'Topic 25 — 1. Percent shares as weights',
    'Compare by factors': 'Topics 26–29 — 1. Compare by factors',
    'Catching up': 'Topics 26–29 — 2. Catching up = gap ÷ difference in rates',
    'The V in motion': 'Topics 26–29 — 1. Compare by factors (the V made general)',
    'The V in motion (Speed · Distance · Time table)': 'Topics 26–29 — 1. Compare by factors (the V made general)',
    'Counting pointer (at most / at least → Topic 21)': 'Topics 26–29 — 3. "At most / at least" in counting → Topic 21',
    'Which door?': 'Topics 26–29 — 5. Which door? COUNT / PATH / SYMMETRY',
    'Pick values that fit': 'Topic 51 — Picking values that fit',
}


def guide_pointer(method):
    sec = GUIDE_SECTIONS.get(method)
    return ('Teacher guide → "%s" (New-Exam-Methods-Teacher-Guide.md in Downloads)' % sec) if sec else None


def load_notes(path=NOTES_FILE):
    try: return json.load(open(path, encoding='utf-8'))
    except FileNotFoundError: return {}


def attach_notes(M, D, N=None):
    """Put the notes on the manifest: rec['note'] (added video), slide['note'] (added slide), rec['lines'][k]['note']
    (new lines in a slide of the teacher's), plus rec/slide['guide'] for new exam methods.  Notes are keyed
    'videoId' and 'videoId#slideIndex' and carry the slide title: when the index no longer fits, the title finds it.
    Returns warnings for added items without a note."""
    N = load_notes() if N is None else N
    warn = []
    NV, NS, NL = N.get('videos', {}), N.get('slides', {}), N.get('lines', {})

    core = lambda t: re.sub(r'^(?:method|approach|shortcut|way)\s*\d*\s*·\s*', '', (t or '').strip().lower())

    def find(tab, vid, k, title):
        e = tab.get('%s#%d' % (vid, k))
        if e and (e.get('t') or '') == (title or ''): return e
        for key, x in tab.items():                         # slides moved: same video, same title
            if key.rsplit('#', 1)[0] == vid and (x.get('t') or '') == (title or '') and title: return x
        if e and (not e.get('t') or core(e['t']) == core(title)): return e    # renamed "X" -> "Method 2 · X"
        return None

    for vid, r in M.items():
        v = D['videos'][vid]
        if r['added']:
            e = NV.get(vid)
            if e: r['note'] = e['d'] if isinstance(e, dict) else e
            else: warn.append('no note for added video %s (%s)' % (vid, r['title']))
            if r['method']: r['guide'] = guide_pointer(r['method'])
        for k, sl in r['slides'].items():
            if sl['method']: sl['guide'] = guide_pointer(sl['method'])
            if r['added'] or sl['kind'] != 'new': continue
            e = find(NS, vid, k, sl['title'])
            if e: sl['note'] = e['d']
            else: warn.append('no note for added slide %s#%d "%s"' % (vid, k, sl['title']))
        for k, x in r['lines'].items():
            t = v['beats'][k].get('title')
            e = find(NL, vid, k, t)
            if e: x['note'] = e['d']
            else: warn.append('no note for new lines in %s#%d "%s"' % (vid, k, t))
    return warn


def line_slides(r):
    """indexes of the teacher's slides in r that got new lines (found by the comparison or listed in METHODS)."""
    return sorted(set(r['lines']) | {k for k, x in r['slides'].items() if x['kind'] == 'lines'})


def counts(M, D):
    C = {}
    for vid, r in M.items():
        c = C.setdefault(r['topic'], dict(videos=0, slides=0, lines=0, nlines=0, method_items=0))
        if r['added']: c['videos'] += 1
        else: c['slides'] += sum(1 for s in r['slides'].values() if s['kind'] == 'new')
        c['lines'] += len(line_slides(r))
        c['nlines'] += sum(len(x['say']) + len(x['draw']) + len(x['items']) for x in r['lines'].values())
        c['method_items'] += (1 if r['added'] and r['method'] else 0) + (0 if r['added'] else sum(1 for s in r['slides'].values() if s['method']))
    return C


def report(M, D):
    C = counts(M, D)
    tt = {x['id']: x['title'] for x in D['topics']}
    rows = ['  topic %2d %-40s added videos %2d · added slides %2d · your slides with new lines %2d (%3d lines) · new-method items %d'
            % (t, tt.get(t, '')[:40], c['videos'], c['slides'], c['lines'], c['nlines'], c['method_items']) for t, c in sorted(C.items())]
    tot = [sum(c[k] for c in C.values()) for k in ('videos', 'slides', 'lines', 'nlines', 'method_items')]
    rows.append('  TOTAL: %d added videos, %d added slides in older videos, %d older slides with new lines (%d lines / board items), %d new-method items' % tuple(tot))
    return '\n'.join(rows)


def _plain(t, n=170):
    t = re.sub(r'\\(?:text|mathrm|textbf)\{([^}]*)\}', r'\1', t or '')
    t = re.sub(r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}', r'\1/\2', t)
    t = t.replace('\\cdot', '·').replace('\\times', '×').replace('\\to', '→').replace('\\ne', '≠').replace('\\le', '≤').replace('\\ge', '≥')
    t = re.sub(r'\\[a-zA-Z]+', ' ', t).replace('$', '').replace('{', '').replace('}', '')
    t = re.sub(r'\s+', ' ', t).strip()
    return t if len(t) <= n else t[:n - 1].rstrip() + '…'


def line_texts(b, x):
    """the added lines of slide b as (kind, text): 'say', 'draw' or 'board'."""
    L = b.get('lines') or []
    out = [('say' if L[i].get('say') is not None else 'draw', _line_text(L[i])) for i in sorted(x['say'] + x['draw'])]
    return out + [('board', _item_text(b['items'][k])) for k in x['items']]


def markdown(M, D, recorded=()):
    tt = {x['id']: x['title'] for x in D['topics']}
    rec = set(recorded)
    md = ['# Added content — not from your Hebrew course', '',
          'Everything in the studio that was added after your Hebrew course was translated — and WHAT each added thing teaches. '
          'In the studio these videos have an orange **NEW** tag (or **+ new slides** / **+ new lines**). On the first slide of an '
          'added video a box at the top of the script says what the lesson adds; every added slide has an orange banner with '
          'what it teaches; and on your own slides the added lines have an orange left border and a small "new line" tag, with a '
          'banner "New lines on this slide". Please read these scripts more carefully before recording.', '',
          '- **New exam method · <name>** — a method added on 2026-10-06 from the real-exam method search. The teacher guide '
          'explains each one: `%s` (also `~/Downloads/New-Exam-Methods-Teacher-Guide.md`).' % GUIDE,
          '- **Added in the September review** — added during the course review (September–October 2026): new lessons, '
          'summaries, guided questions and slides.',
          '- **New lines on your slide** — a slide of yours (it matches your Hebrew-course slide) with a few spoken lines or '
          'board items added. Found by comparing every line with your original video; renumbered lines, renamed people and '
          'small wording edits are not counted. The added lines are quoted under the slide.',
          '- Renumbered questions (new numbers, letters or story) and shortened slides are NOT listed: they are still your material.',
          '- Topics 39–52 (verbal, writing, Psychometric Thinking, charts) were built from your Hebrew material; only the new '
          'Topic 51 method is listed there.', '']
    C = counts(M, D)
    md += ['## Counts', '', '| Topic | Added videos | Added slides (in your videos) | Your slides with new lines | New lines / board items |', '|---|---|---|---|---|']
    for t, c in sorted(C.items()):
        md.append('| %d · %s | %d | %d | %d | %d |' % (t, tt.get(t, ''), c['videos'], c['slides'], c['lines'], c['nlines']))
    md.append('| **Total** | **%d** | **%d** | **%d** | **%d** |' % tuple(sum(c[k] for c in C.values()) for k in ('videos', 'slides', 'lines', 'nlines')))
    md.append('')
    order = []
    for f in D['flow']:
        if f['type'] == 'video' and f['ref'] in M and f['ref'] not in order: order.append(f['ref'])
    cur = None
    for vid in order:
        r = M[vid]; v = D['videos'][vid]
        if r['topic'] != cur:
            cur = r['topic']; md += ['## Topic %d · %s' % (cur, tt.get(cur, '')), '']
        tag = 'NEW video' if r['added'] else ('+ new slides' if any(s['kind'] == 'new' for s in r['slides'].values()) else 'new lines in your slides')
        md.append('### %s — `%s`  (%s)%s' % (r['title'], vid, tag, ' ✓ recorded' if vid in rec else ''))
        md.append('*%s*' % r['label'])
        md.append('')
        if r['added']:
            md.append('**What it adds:** %s' % (r.get('note') or '(no note yet)'))
            if r.get('guide'): md.append('· %s' % r['guide'])
            md.append('')
            ex = [s for s in r['slides'].values() if s['label'] != r['label']]
            md.append(('All %d slides are new.' % len(r['slides']) if len(r['slides']) > 1 else 'Its one slide is new.') + (' Within it:' if ex else ''))
            for k, s in sorted(r['slides'].items()):
                if s['label'] != r['label']: md.append('- Slide %d · %s — **%s**' % (k + 1, s['title'], s['label']))
        else:
            for k in sorted(set(r['slides']) | set(r['lines'])):
                s = r['slides'].get(k)
                if s and s['kind'] == 'new':
                    md.append('- Slide %d · %s — **Added slide** (%s): %s' % (k + 1, s['title'], s['label'], s.get('note') or '(no note yet)'))
                    if s.get('guide'): md.append('  - %s' % s['guide'])
                    continue
                x = r['lines'].get(k)
                head = '- Slide %d · %s — **New lines on your slide**' % (k + 1, v['beats'][k].get('title'))
                if s: head += ' (%s)' % s['label']
                md.append(head + (': ' + x['note'] if x and x.get('note') else ''))
                if s and s.get('guide'): md.append('  - %s' % s['guide'])
                if x:
                    for kind, t in line_texts(v['beats'][k], x):
                        md.append('  - %s“%s”' % ({'say': '', 'draw': '✎ ', 'board': 'board: '}[kind], _plain(t)))
        md.append('')
    return '\n'.join(md)
