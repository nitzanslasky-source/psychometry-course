"""Topic 25 (Averages) - the scripts for the teacher's own-voice reading (2026-10-21), written from the first draft to
the Codex review standard, the clarity style, W1-W21, R37 (core methods taught in the lessons), the method vocabulary
and the method visuals, built exactly like topics 22-24 (math_patches/_ai_vis_t24.py: the DSL and the visual passes are
copied here, so the topics stay independent; the stem-part highlighting as in topic 22).

The camera lesson 'wp-080' (Averages) gets a full reading script with more examples, split into three parts of about
3-4 minutes (math_patches/_camera_parts.py). The other two lessons grew under R37 and are split into parts too (not on
camera): 'wp-081' (sum from the average) and 'wp-086' (weighted averages). Every other topic-25 video gets a script that
SHE reads aloud in the Reading Studio; reading_to_video.py then times the handwriting and the visuals to her words. The
summary video r26-t25-summary is not read: summary_pages/t25.json (python3 summary_pages.py 25) replaces it.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t25.py [vid ...] writes it);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t25.py ai_redo_t25() (runs LAST) rebuilds the slides from studio_slides(vid) and then
                    _ai_visual.apply() adds the cues and click items around them.

Spec DSL (as in topic 24): video / S / L / I / IH (a hand-written board line) / show / pt / mk; the topic-25 pictures of
her Hebrew course, built in layers at the spoken words: TOWERS (the cube towers, wp 5211-5235: the towers, the limits
smallest / biggest, the extra blocks moved, the level), ZL (the balance point of two values, wp 5363-5382: the average
in the middle, one value, the mirror value), SAW (the seesaw in its exam form, wp 5750-5782: the axis, the values above,
the weights below, the gap cut into units, the pivot nearer the heavy side), TBL (the differences from the average; the
"count x average = sum" box; the then-and-now table). The concept map (NEW / REMINDER per video) is in
~/Downloads/Topic-25-AI-scripts-review.md.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(HERE) != 'math_patches':      # a test copy elsewhere still reads and writes the real studio files
    HERE = '/Users/nitzanslasky/psychometry-course/studio-build/math_patches'
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t25ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-25 flow order of the scripts
TAG = re.compile(r'\[(short pause|pause|long pause)\]')
CHOICE_N = re.compile(r'(?<![Cc]hoice )(?<![Tt]he )\b[Nn]umbers? (one|two|three|four)\b')   # = ai_check.py (R34)
VERDICT = re.compile(r'which (way|method|one of them) is (better|best|faster)|\bso which way\b', re.I)


# ------------------------------------------------------------------------------------------------------------- DSL
def I(name, tex, size=36, col=0, hand=None):
    return {'_name': name, '_col': col, '_hand': hand, 'k': 't', 't': tex, 'size': size, 'gap': 16}


def NL(name, svg, w=560, col=0):
    vb = [float(t) for t in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    return {'_name': name, '_col': col, '_hand': None, 'k': 'vis', 'v': {'type': 'geometry', 'svg': svg}, 'w': w,
            'h': int(round(w * vb[3] / vb[2])), 'gap': 16}


def DIST(name, lo, hi, c, r, base=(0,), band=None, w=1060, col=0):
    """a |x - c| number line BUILT in layers (2026-10-11, teacher: "build the number line at the spoken words"):
    -> {'line': the line with c (and the `base` ticks), 'right': the arrow r steps right + its end, 'left': the arrow r
    steps left + its end, 'band': the shaded band between the ends (band='open' / 'closed'; None = no band)}.
    Each is a figure item of the same size drawn at the same place (over=1: the layer above the previous item), so they
    must be shown in this order: line, then right/left (either order), then band. Labels are big (~ the handwriting)."""
    L_, R_, Y_ = SNL.L, SNL.R, SNL.Y
    X = lambda v: L_ + 30 + (v - lo) / float(hi - lo) * (R_ - L_ - 60)
    INK, TEAL, BAND, FONT = SNL.INK, SNL.TEAL, SNL.BAND, SNL.FONT
    top, bot = 74, 56
    fmt = lambda v: ('−%d' % -v) if v < 0 else '%d' % v
    def svg(body, title):
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 %d 640 %d" role="img" aria-label="%s"><title>%s</title>%s</svg>'
                % (Y_ - top, top + bot, title, title, body))
    def tick(v, bold=False):
        return ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2"/>' % (X(v), Y_ - 11, X(v), Y_ + 11, INK) +
                '<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="27" font-weight="bold">%s</text>' % (X(v), Y_ + 42, INK, FONT, fmt(v)))
    def dot(v):
        closed = band not in ('open', 'rays')
        return '<circle cx="%.1f" cy="%d" r="7" fill="%s" stroke="%s" stroke-width="2.5"/>' % (X(v), Y_, TEAL if closed else '#ffffff', TEAL)
    def arrow(e):
        d = -1 if e > c else 1
        return ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.5"/>' % (X(c), Y_ - 36, X(e) + 4 * d, Y_ - 36, TEAL) +
                '<path d="M %.1f %d l %d -6 l 0 12 Z" fill="%s"/>' % (X(e), Y_ - 36, 12 * d, TEAL) +
                '<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="27" font-weight="bold">%d</text>' % ((X(c) + X(e)) / 2, Y_ - 45, TEAL, FONT, r))
    line = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.5"/>' % (L_ - 10, Y_, R_ + 10, Y_, INK) +
            '<path d="M %d %d l 12 -7 l 0 14 Z" fill="%s"/>' % (L_ - 14, Y_, INK) + '<path d="M %d %d l -12 -7 l 0 14 Z" fill="%s"/>' % (R_ + 14, Y_, INK) +
            ''.join(tick(v) for v in base if v != c) + tick(c) + '<circle cx="%.1f" cy="%d" r="6" fill="%s"/>' % (X(c), Y_, INK) +
            '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.5" stroke-dasharray="4 4"/>' % (X(c), Y_ - 36, X(c), Y_ - 7, INK))
    out = {'line': svg(line, 'Number line: %s marked' % fmt(c)),
           'right': svg(arrow(c + r) + tick(c + r) + dot(c + r), '%d steps right of %s: %s' % (r, fmt(c), fmt(c + r))),
           'left': svg(arrow(c - r) + tick(c - r) + dot(c - r), '%d steps left of %s: %s' % (r, fmt(c), fmt(c - r)))}
    if band == 'rays':                         # |x - c| > r: two rays going outward from the open ends, a gap between
        a, b = X(c - r), X(c + r)
        out['band'] = svg('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (L_ - 2, Y_ - 7, a - L_ + 2, BAND, TEAL)
                          + '<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (b, Y_ - 7, R_ + 2 - b, BAND, TEAL)
                          + '<path d="M %d %d l 12 -7 l 0 14 Z" fill="%s"/>' % (L_ - 14, Y_, TEAL) + '<path d="M %d %d l -12 -7 l 0 14 Z" fill="%s"/>' % (R_ + 14, Y_, TEAL)
                          + dot(c - r) + dot(c + r), 'below %s or above %s' % (fmt(c - r), fmt(c + r)))
    elif band:
        a, b = X(c - r), X(c + r)
        out['band'] = svg('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (a, Y_ - 7, b - a, BAND, TEAL)
                          + dot(c - r) + dot(c + r) + '<circle cx="%.1f" cy="%d" r="6" fill="%s"/>' % (X(c), Y_, INK),
                          'between %s and %s' % (fmt(c - r), fmt(c + r)))
    items = {}
    for k, sv in out.items():
        it = NL('%s_%s' % (name, k), sv, w=w, col=col)
        if k != 'line': it['over'] = 1; it['gap'] = 0
        items[k] = it
    return items


def show(item, phrase): return ('show', item, phrase)
def pt(target, phrase, style=None, dur=None): return ('point', target, phrase, style, dur)
def mk(kind, target, phrase): return ('mark', kind, target, phrase)


def L(say, *cues, voice=None, pause=None):
    return {'say': say, 'cues': list(cues), 'voice': voice, 'pause': pause}


def S(title, *lines, sb=None):
    return {'title': title, 'sb': sb or title, 'lines': list(lines)}


def video(vid, kind, slides, qid=None, title=None):
    VIDEOS[vid] = {'kind': kind, 'slides': slides, 'qid': qid, 'title': title}
    ORDER.append(vid)


def fig(*a, **k): return SNL.fig(*a, **k)


# ------------------------------------------------------------------------------------------------------- resolving
def _plain(say): return re.sub(r'\s+', ' ', TAG.sub(' ', say)).strip()


# 2026-10-18 visual check: the last baseline of each question's stem on the board (measured on the rendered step
# frames). The right column starts just below it, so its rows keep their own spacing; otherwise the renderer pushes
# every row under the one above with a 14 px gap (cramped rows).
QBOT = {'solve-q-r26-t25-01': 230, 'solve-q-r26-t25-02': 242, 'solve-q-r26-t25-03': 181, 'solve-q-r26-t25-04': 181, 'solve-q-r26-t25-05': 181, 'solve-wp25-g082': 181, 'solve-wp25-g083': 181, 'solve-wp25-g084': 242, 'solve-wp25-g085': 286, 'solve-wp25-g087': 242, 'solve-wp25-g088': 242, 'solve-wp25-g089': 242, 'solve-wp25-g090': 242, 'solve-wp25-p18': 181}   # measured on the frames (2026-10-21)


def _layout(vid):
    """item dicts per slide (placed), name -> (slide index, item index); raises on a bad spec."""
    V = VIDEOS[vid]; names = {}; per = []
    for si, sl in enumerate(V['slides']):
        lesson_title = V['kind'] == 'lesson' and si == 0
        pre = 1 if V['kind'] == 'solution' else 0
        items = []
        for ln in sl['lines']:
            for c in ln['cues']:
                if c[0] == 'show':
                    it = c[1]
                    assert not lesson_title, (vid, 'no board items on the title slide')
                    assert it['_name'] not in names, (vid, 'item name used twice', it['_name'])
                    names[it['_name']] = (si, pre + len(items)); items.append(it)
        right = any(it['_col'] == 1 for it in items)
        solo = right and not any(it['_col'] == 0 for it in items)   # only right-column items: use the left column
        out = []; ycol = max(100, QBOT.get(vid, 0) + 50) if V['kind'] == 'solution' else 78
        for it in items:
            d = {k: v for k, v in it.items() if not k.startswith('_')}
            if it['_col'] == 1 and not solo:
                if d['k'] == 'vis':
                    d['w'] = min(d.get('w', 540), 540); d['h'] = int(round(d['h'] * d['w'] / it['w']))
                y_here = ycol
                if not d.get('over'): ycol += (d['h'] if d['k'] == 'vis' else int(d.get('size', 36) * 1.55 * ((1.9 if '/' in it['_hand'] else 1.45) if it['_hand'] else 1))) + 16
                d.update(x=1010, w=d['w'] if d['k'] == 'vis' else 540, y=y_here)
            elif right and d['k'] == 't':
                d['w'] = 560
            if it.get('_y'): d['y'] = it['_y']          # topic 17: a question with its own figure - place below it
            if it.get('_x'): d['x'] = it['_x']
            out.append((it, d))
        per.append(out)
    return names, per


# 2026-10-14 Rule V4.8 (camera lessons: the face bubble never covers math). Her bubble is composited top right (board
# x >= 1344, y <= 256). In the camera lesson and its parts: a right-column stack that would start above y 262 moves down
# as a whole (its own order and spacing kept), and a left-column item is at most 920 wide (ends left of x 1330; a figure
# and its layers are scaled down together, text wraps). Other videos are unchanged.
CAM_BASE = 'wp-080'
CAM_W, CAM_Y = 920, 280


def _cam_width(d, hand=None):
    """the drawn width of a board item, roughly (a figure: its box; a hand-written line: its pen strokes at the
    hand-written size, 1.2x; text: ~half the size per visible character)"""
    if d['k'] == 'vis': return d.get('w') or 540
    if hand:
        import studio_handwrite as _HW
        return min(d.get('w') or 1130, _HW.write(hand)['w'] * round(d.get('size', 36) * 1.2) / 100.0)
    t = re.sub(r'\\(quad|qquad)', '    ', d.get('t') or ''); t = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'\1', t)
    t = re.sub(r'\\[a-zA-Z]+', 'x', t)
    for ch in '${}\\': t = t.replace(ch, '')
    return min(d.get('w') or 1130, len(t) * d.get('size', 36) * (0.6 if d['k'] == 'hw' else 0.5))
_layout_plain = _layout


def _layout(vid):
    names, per = _layout_plain(vid)
    if not re.fullmatch(re.escape(CAM_BASE) + r'(-\d+)?', vid) or VIDEOS[vid]['kind'] != 'lesson': return names, per
    for sl in per:
        right = [d for it, d in sl if d.get('x') == 1010 and d.get('y') is not None]
        if any(d.get('x') == 1010 and d.get('y') is not None and d['y'] < CAM_Y - 18 and not d.get('over')
               and 1010 + _cam_width(d, it.get('_hand')) > 1335 for it, d in sl):
            top, yl = CAM_Y, 78                    # ... and below a left-column figure that reaches under the right column
            for it2, d2 in sl:
                if d2.get('x') is not None or d2.get('y') is not None or d2.get('over'): continue
                h2 = d2['h'] if d2['k'] == 'vis' else d2.get('size', 36) * 1.55 * (1.2 if it2.get('_hand') else 1)
                if d2['k'] == 'vis' and 410 + (d2.get('w') or 0) > 1000: top = max(top, int(yl + h2 + 16))
                yl += h2 + 16
            dy = top - min(d['y'] for d in right)
            for d in right: d['y'] += dy
        for it, d in sl:
            if d.get('x') is not None or d.get('y') is not None: continue
            if d['k'] == 'vis' and d.get('w', 0) > CAM_W:
                d['h'] = int(round(d['h'] * CAM_W / d['w'])); d['w'] = CAM_W
            elif d['k'] in ('t', 'hw') and (d.get('w') or 1130) > CAM_W:
                d['w'] = CAM_W
    return names, per


def _target(vid, names, si, t):
    if t in ('stem',) or re.fullmatch(r'stem: (g\d|given|ask)', t) or re.fullmatch(r'choice \d', t) or t.startswith('fig:'): return t
    nm, _, part = t.partition(':')
    nm = nm.strip()
    assert nm in names, (vid, 'unknown item', nm)
    s, k = names[nm]
    assert s == si, (vid, 'item %s is on another slide' % nm)
    return 'item %d' % k + (': ' + part.strip() if part else '')


def check(vid):
    """the spec's own checks: phrases in their line, in order; no symbols the TTS spells out; one CAPS word, one '!'."""
    V = VIDEOS[vid]; probs = []; flat = [ln for sl in V['slides'] for ln in sl['lines']]
    allt = ' '.join(ln['say'] for ln in flat)
    for n, ln in enumerate(flat, 1):
        say = ln['say']; low = say.lower(); last = -1
        for c in ln['cues']:
            ph = c[2] if c[0] in ('show', 'point') else c[3]
            if ph.startswith('<'):
                prev = flat[n - 2]['say'].lower() if n > 1 else ''
                if ph[1:].lower() not in prev: probs.append('line %d: %r not in the previous line' % (n, ph))
                continue
            k = low.find(ph.lower())
            if k < 0: probs.append('line %d: phrase %r not in the line' % (n, ph)); continue
            if k < last: probs.append('line %d: phrase %r comes before the previous cue' % (n, ph))
            last = k
        if re.search(r'[πα-ωΑ-Ω°%×÷²³√≤≥≠⇒→∠◆]|\.\.\.|…|—', say): probs.append('line %d: symbol / ... / dash: %s' % (n, say[:60]))
        if re.search(r'\b(um|uh|sorry|Good\.|Notice:)', say): probs.append('line %d: filler / label: %s' % (n, say[:60]))
        for part in TAG.split(say)[0::2]:
            pass
        vs = ln['voice']
        if isinstance(vs, list):
            parts = [p for p in TAG.split(say)[0::2]]
            if not parts[0].strip(): parts = parts[1:]
            if len(vs) != len(parts): probs.append('line %d: %d voices for %d parts' % (n, len(vs), len(parts)))
    caps = re.findall(r'\b[A-Z]{2,}\b', allt)
    caps = [c for c in caps if c not in ('I', 'OK', 'GCD', 'LCM')]
    if len(caps) > 1: probs.append('CAPS words: %s (at most one)' % caps)
    bangs = re.findall(r'[A-Za-z][^.?!]*!', re.sub(r'\b(No|Yes|Exactly)!', '', allt))
    if len(bangs) > 1: probs.append('%d "!" sentences (at most one)' % len(bangs))
    if re.search(r'\bchoice (one|two|three|four)\b', allt, re.I): probs.append('says "choice N" - say "choice number N" (R34)')
    if V['kind'] == 'solution':
        for n, ln in enumerate(flat, 1):
            for m in CHOICE_N.finditer(ln['say']): probs.append('line %d: bare "%s" - say "choice number N" (R34)' % (n, m.group(0)))
    if VERDICT.search(allt): probs.append('a "which way is better" verdict - the teacher dropped it (2026-10-11)')
    # exact decimals (0.9, one point two) are fine (teacher, 2026-10-12); only decimal ESTIMATES (of roots, pi) are banned
    if re.search(r'(about|roughly|approximately|almost|≈)\s+\S*\s*(\d\.\d|\b(zero|one|two|three|four|five|six|seven|eight|nine) point\b)', allt, re.I): probs.append('a decimal estimate - use whole-number benchmarks')
    for sl in V['slides']:
        for ln in sl['lines']:
            for c in ln['cues']:
                if c[0] == 'show' and c[1].get('_hand'):
                    try: HWR.write(c[1]['_hand'])
                    except Exception as e: probs.append('item %s: handwriting text %r has an unsupported glyph (%s)' % (c[1]['_name'], c[1]['_hand'], e))
    try:
        names, per = _layout(vid)
        for si, sl in enumerate(V['slides']):
            for ln in sl['lines']:
                for c in ln['cues']:
                    if c[0] == 'point': _target(vid, names, si, c[1])
                    if c[0] == 'mark': _target(vid, names, si, c[2])
    except AssertionError as e:
        probs.append('items: %s' % (e,))
    return probs


# ------------------------------------------------------------------------------------------- the three outputs
def vis(vid):
    """{spoken line N (1-based, whole video): [cue tuples in the _ai_visual.py format]}"""
    V = VIDEOS[vid]; names, per = _layout(vid); out = {}; n = 0
    placed = {id(it): d for sl in per for it, d in sl}
    for si, sl in enumerate(V['slides']):
        for ln in sl['lines']:
            n += 1; cs = []
            for c in ln['cues']:
                if c[0] == 'show':
                    it = c[1]; d = placed[id(it)]
                    cs.append(('write', d, c[2], it['_hand']) if it['_hand'] else ('show', d, c[2]))
                elif c[0] == 'point':
                    x = ('point', _target(vid, names, si, c[1]), c[2])
                    if c[3] or c[4]: x += (c[3] or 'hl',)
                    if c[4]: x += (c[4],)
                    cs.append(x)
                else:
                    cs.append(('mark', c[1], _target(vid, names, si, c[2]), c[3]))
            if cs: out[n] = cs
    return out


def ai_json(vid):
    V = VIDEOS[vid]; slides = []
    for sl in V['slides']:
        row = []
        for ln in sl['lines']:
            d = {'say': ln['say']}
            if ln['voice']: d['voice'] = ln['voice']
            at = [c[2] if c[0] in ('show', 'point') else c[3] for c in ln['cues']]
            if at: d['at'] = at
            if ln['pause']: d['pause'] = ln['pause']
            row.append(d if len(d) > 1 else d['say'])
        slides.append(row)
    return {'videoId': vid,
            'style': "the teacher reads it herself (Reading Studio), topic-25 scripts (2026-10-21): math_patches/_ai_vis_t25.py is "
                     "the source - edit there and re-run it. Rules: real_exam/TEACHING_STYLE_GUIDE.md R1-R35 (no 'which way is "
                     "better' verdict) + NITZAN_RHYTHM_DELIVERY.md P1-P13. Calm preset on the question reading and plain calculations.",
            'slides': slides}


def write_json(vid):
    p = os.path.join(SB, 'ai_scripts', vid + '.json')
    json.dump(ai_json(vid), open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    return p


def studio_slides(vid):
    """beat specs for math_api.MathCourse._beat (spoken lines only; cues + items come from _ai_visual.apply) + sidebar."""
    V = VIDEOS[vid]; lesson = V['kind'] == 'lesson'
    body = V['slides'][1:] if lesson else V['slides']
    sb = list(dict.fromkeys(sl['sb'] for sl in body))
    out = []
    for si, sl in enumerate(V['slides']):
        script = [_plain(ln['say']) for ln in sl['lines']]
        if lesson and si == 0:
            out.append({'title': sl['title'], 'mode': 'title', 'active': -1, 'pre': [], 'script': script})
        else:
            out.append({'title': sl['title'], 'mode': 'concept' if lesson else 'question', 'active': sb.index(sl['sb']),
                        'pre': [] if lesson else [Q(V['qid'])], 'script': script})
    return out, sb


def rebuild(M, vid):
    """replace the studio video's slides by the spec (spoken lines only); _ai_visual.apply adds cues + items."""
    v = M.video(vid); beats, sb = studio_slides(vid)
    v['beats'] = [M._beat(v, b) for b in beats]
    v.setdefault('hybrid', {})['sidebar'] = sb
    M.touched_videos.add(vid)


def stats(vid):
    flat = [ln for sl in VIDEOS[vid]['slides'] for ln in sl['lines']]
    words = sum(len(_plain(ln['say']).split()) for ln in flat)
    chars = sum(len(_plain(ln['say'])) for ln in flat)
    cues = sum(len(ln['cues']) for ln in flat)
    return {'words': words, 'chars': chars, 'minutes': round(words / 165.0, 1), 'cues': cues, 'lines': len(flat)}

# ------------------------------------------------------------------------------------------- topic-17 figures (copied to topic 18; not used yet)
# The number line is BUILT in layers at the spoken words (like DIST in topic 13 / STRIP in topic 14): every layer is a
# figure item of the same size drawn at the same place (over=1), shown in order right after its base (never another
# item in between). Labels are big and bold (about the size of the handwriting).
def _svg(vb, body, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, title, title, body))


LAYER_BASE = {}     # a figure layer's item name -> its base item's name (a POINT on a layer lights nothing visible)


def _layers(name, out, w, col):
    items = {}
    base = '%s_%s' % (name, out[0][0])
    for k, sv in out:
        it = NL('%s_%s' % (name, k), sv, w=w, col=col)
        if k != 'line': it['over'] = 1; it['gap'] = 0; LAYER_BASE[it['_name']] = base
        items[k] = it
    return items


RED = '#d62d48'


def ZL(name, lo, hi, layers, ticks=(-1, 0, 1), w=1060, col=0, title='Number line'):
    """a number line from lo to hi (positions only - NOT to scale, like the exam's figures), ticks with labels at
    `ticks` (a value, or (value, label)). layers = [(key, [mark, ...]), ...] drawn on top, in order. Marks:
      ('pt', v, label)          a teal dot on v and a bold italic label above it
      ('ink', v, label)         an ink dot on v and a label above it (a given point)
      ('arrow', a, b, text)     a teal arrow above the line from a to b, text above its middle ('' = none)
      ('shade', a, b)           a teal band on the line from a to b (open ends)
      ('cross', v)              a red cross above v (a range ruled out)
      ('below', v, text)        a teal label under the line at v
    -> {key: item}; show them in order (the base line is key 'line')."""
    L_, R_, Y_ = 40, 600, 112
    X = lambda v: L_ + 16 + (v - lo) / float(hi - lo) * (R_ - L_ - 32)
    INK, TEAL, BAND, FONT = SNL.INK, SNL.TEAL, SNL.BAND, SNL.FONT
    VB = '0 0 640 194'
    def txt(x, y, t, c, size=24, style=''):
        return ('<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="%d" font-weight="bold"%s>%s</text>'
                % (x, y, c, FONT, size, (' font-style="%s"' % style) if style else '', t))
    body = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.5"/>' % (L_ - 6, Y_, R_ + 6, Y_, INK) +
            '<path d="M %d %d l 12 -7 l 0 14 Z" fill="%s"/>' % (L_ - 10, Y_, INK) + '<path d="M %d %d l -12 -7 l 0 14 Z" fill="%s"/>' % (R_ + 10, Y_, INK))
    for t in ticks:
        v, lab = t if isinstance(t, tuple) else (t, ('−%s' % -t) if t < 0 else str(t))
        body += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2"/>' % (X(v), Y_ - 10, X(v), Y_ + 10, INK) + txt(X(v), Y_ + 44, lab, INK, 36)
    out = [('line', _svg(VB, body, title))]
    for key, marks in layers:
        b = ''
        for m in marks:
            if m[0] in ('pt', 'ink'):
                c = TEAL if m[0] == 'pt' else INK
                b += '<circle cx="%.1f" cy="%d" r="7" fill="%s"/>' % (X(m[1]), Y_, c) + txt(X(m[1]), Y_ - 18, m[2], c, 36, 'italic')
            elif m[0] == 'arrow':
                a, e = X(m[1]), X(m[2]); d = 1 if e > a else -1
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3"/>' % (a, Y_ - 58, e - 10 * d, Y_ - 58, TEAL) +
                      '<path d="M %.1f %d l %d -7 l 0 14 Z" fill="%s"/>' % (e, Y_ - 58, -14 * d, TEAL))
                if m[3]: b += txt((a + e) / 2, Y_ - 70, m[3], TEAL, 34)
            elif m[0] == 'shade':
                b += '<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (X(m[1]), Y_ - 7, X(m[2]) - X(m[1]), BAND, TEAL)
            elif m[0] == 'cross':
                x0 = X(m[1]); y0 = Y_ - 58
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (x0 - 14, y0 - 14, x0 + 14, y0 + 14, RED) +
                      '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (x0 + 14, y0 - 14, x0 - 14, y0 + 14, RED))
            elif m[0] == 'below':
                b += txt(X(m[1]), Y_ + 74, m[2], TEAL, 32)
        out.append((key, _svg(VB, b, key)))
    return _layers(name, out, w, col)

# ------------------------------------------------------------------------------------------- method visuals (V1)
# 2026-10-13 rewrite in the clarity style (TEACHING_STYLE_GUIDE "Clarity style") with the method-visual rule V1: the
# Hebrew topic-19 pictures are built step by step - THE SAME TEMPLATE with the input in every slot (alg 18853-18868,
# SLOT) and the inner operation coloured and replaced by its value, inside out (alg 18910-18925, CHAIN; the circular rule
# goes down and climbs back up, alg 19048-19114, CHAIN up=). Layers are shown right after their base (no item between).
_mv_spec = importlib.util.spec_from_file_location('_method_visuals', os.path.join(HERE, '_method_visuals.py'))
MV = importlib.util.module_from_spec(_mv_spec); _mv_spec.loader.exec_module(MV)


def SLOT(name, rule, rows, col=0, size=34):
    return MV.items(_layers, name, MV.SLOT(rule, rows, size=size), col=col)


def CHAIN(name, rows, up=None, col=0, size=34, links=None):
    return MV.items(_layers, name, MV.CHAIN(rows, up=up, size=size, links=links), col=col)


def _hand(tex):
    """the hand-written twin of a typed line (studio_handwrite syntax), or None if it has a glyph the pen lacks"""
    t = tex
    for a, b in [('\\blacklozenge', '◆'), ('\\times', '×'), ('\\cdot', '·'), ('\\ne', '≠'), ('\\le', '≤'), ('\\ge', '≥'), ('\\to', '→'),
                 ('\\quad', '    '), ('\\qquad', '      '), ('\\ ', ' '), ('\\,', ''), ('\\star', '⋆'), ('\\div', '÷'),
                 ('\\left', ''), ('\\right', ''), ('\\%', '%')]:
        t = t.replace(a, b)
    t = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'{\1/\2}', t)
    t = re.sub(r'\\sqrt\{([^{}]*)\}', r'√{\1}', t)
    t = re.sub(r'\\text\{([^{}]*)\}', r'\1', t)
    t = t.replace('$', '').replace('-', '−')
    if '\\' in t.replace('\\hl', ''): return None
    try:
        HWR.write(t); return t
    except Exception:
        return None


def IH(name, tex, size=34, col=0):
    """a board line that is hand-written when the handwriting style is on (typed otherwise)"""
    return I(name, tex, size=size, col=col, hand=_hand(tex))


# ------------------------------------------------------------------------------------------- figures copied from topic 22 (V1)
# The word-problem pictures of her Hebrew course, built in layers at the spoken words (each layer a figure item drawn
# over its base; own=True: a layer finds its own base, so the written calculation lines can come in between):
#   TBL    the ratio table (wp 1300-1392: a column per quantity, row 1 the known pair, row 2 the new case and "?",
#          the times-k arrow across or down, else the diagonal of the triangle value) and the then-and-now table
#          (wp 1942-1990: "I stop and continue my table": a row for every time in the story)
#   UNITS  ratio units as boxes (3x and 10x as 3 and 10 equal boxes, the extra 7 bracketed) and the fraction bar for a
#          story (wp 2213-2267: "let's draw them as a rectangle", cut into 4, 3 kept)
#   ZL     a number line (the gap that turns around; the range of a price; where a mix must land)
ORANGE = '#c8641e'
_INK, _TEAL, _LIGHT = MV.INK, MV.TEAL, MV.LIGHT


def _tx(x, y, t, size=28, col=None, anchor='middle'):
    return MV._text(x, y, t, size, col or _INK, anchor)


def TBL(name, head, rowlab, layers, colw=200, labw=190, rowh=74, headh=56, col=0, w=None, side=0, size=34,
        title='Table'):
    """a table: head = the column names, rowlab = the row names ('' = no name column); layers = [(key, [mark, ...])]:
      ('c', r, c, text[, colour])      a cell value (r, c from 0; c counts the value columns only)
      ('q', r, c)                      a teal question mark
      ('cover', r, c, text)            the value found, over the question mark (teal)
      ('across', r, label)             an arrow across row r, from column 0 to column 1, with its label (x 7)
      ('down', c, r1, r2, label)       an arrow down beside column c (the first or the last), from row r1 to r2
      ('diag', (r1, c1), (r2, c2))     the diagonal of the triangle value
      ('box', r, c)                    a teal frame around a cell
    side = an empty margin left and right (for the down arrows)"""
    nr = len(rowlab); haslab = any(rowlab); lw = labw if haslab else 0
    x0 = 10 + side; y0 = 10
    xs = [x0 + lw + k * colw for k in range(len(head) + 1)]
    W = xs[-1] + 10 + side; H = y0 + headh + rowh * nr + 12
    top = lambda r: y0 + headh + rowh * r
    cy = lambda r: top(r) + rowh * .64
    cx = lambda c: (xs[c] + xs[c + 1]) / 2.0
    body = '<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (xs[0], y0, xs[-1] - xs[0], headh, _LIGHT)
    body += ''.join(_tx(cx(k), y0 + headh * .68, h, max(27, size - 2)) for k, h in enumerate(head))   # topic 25: the data sit in the head row
    left = x0 if haslab else xs[0]
    body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4"/>' % (xs[0], y0, xs[-1], y0, _INK)
    for r in range(nr + 1):
        y = top(r)
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s"/>' % (left if r else xs[0], y, xs[-1], y, _INK, 2.4 if r == 0 else 1.6)
    for x in xs:
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>' % (x, y0, x, top(nr), _INK)
    if haslab:
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>' % (x0, top(0), x0, top(nr), _INK)
        body += ''.join(_tx(x0 + lw / 2.0, cy(r), lab, max(26, size - 6)) for r, lab in enumerate(rowlab))
    out = [('line', MV._svg(W, H, body, title + ': ' + ', '.join(head)))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'c':
                b += _tx(cx(m[2]), cy(m[1]), m[3], size, m[4] if len(m) > 4 else _INK)
            elif k == 'q':
                b += _tx(cx(m[2]), cy(m[1]), '?', size + 2, _TEAL)
            elif k == 'cover':
                r, c = m[1], m[2]
                b += '<rect x="%.1f" y="%.1f" width="76" height="%.1f" fill="#ffffff"/>' % (cx(c) - 38, top(r) + 6, rowh - 12)
                b += _tx(cx(c), cy(r), m[3], size, _TEAL)
            elif k == 'across':
                r = m[1]; y = top(r) + rowh * .5
                xm = (cx(0) + cx(1)) / 2.0
                b += MV._arrow(cx(0) + 46, y + 6, cx(1) - 46, y + 6)
                b += '<rect x="%.1f" y="%.1f" width="66" height="27" rx="5" fill="#ffffff"/>' % (xm - 33, y - 25)
                b += _tx(xm, y - 3, m[2], 28, _TEAL)
            elif k == 'down':
                c, r1, r2 = m[1], m[2], m[3]
                y1, y2 = top(r1) + rowh * .32, top(r2) + rowh * .68
                if c == 0:
                    x = xs[0] - 20 - (lw if haslab else 0)
                    b += MV._arrow(x, y1, x, y2) + _tx(x - 10, (y1 + y2) / 2.0 + 10, m[4], 30, _TEAL, 'end')
                else:
                    x = xs[-1] + 20
                    b += MV._arrow(x, y1, x, y2) + _tx(x + 10, (y1 + y2) / 2.0 + 10, m[4], 30, _TEAL, 'start')
            elif k == 'diag':
                (r1, c1), (r2, c2) = m[1], m[2]
                x1, ya, x2, yb = cx(c1), top(r1) + rowh * .5, cx(c2), top(r2) + rowh * .5
                b += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3.2" stroke-linecap="round"/>'
                      % (x1 + (x2 - x1) * .22, ya + (yb - ya) * .22, x1 + (x2 - x1) * .78, ya + (yb - ya) * .78, _TEAL))
            elif k == 'box':
                r, c = m[1], m[2]
                b += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="none" stroke="%s" stroke-width="3"/>'
                      % (xs[c] + 5, top(r) + 5, colw - 10, rowh - 10, _TEAL))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def UNITS(name, rows, layers, unit=46, boxh=44, labw=150, gap=58, col=0, w=None, title='Ratio units', extra=0):
    """rows of equal boxes = ratio units: rows = [(label, number of boxes)]; layers = [(key, [mark, ...])]:
      ('fill', r, i0, i1[, colour])    tint boxes i0 .. i1-1 of row r (teal; 'orange')
      ('br', r, i0, i1, text[, 'up'])  a bracket under (or over) boxes i0 .. i1-1, with its text
      ('in', r, i, text)               a value inside box i
      ('right', r, text)               a value after the row"""
    n = max(c for _, c in rows); x0 = 10 + labw; y0 = 46
    W = x0 + n * unit + 20 + extra; H = y0 + len(rows) * (boxh + gap) + 6
    rt = lambda r: y0 + r * (boxh + gap)
    bx = lambda i: x0 + i * unit
    body = ''
    for r, (lab, c) in enumerate(rows):
        body += _tx(x0 - 14, rt(r) + boxh * .7, lab, 30, _INK, 'end')
        body += ''.join('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" stroke-width="2.2"/>'
                        % (bx(i), rt(r), unit, boxh, _INK) for i in range(c))
    out = [('line', MV._svg(W, H, body, title))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'fill':
                r, i0, i1 = m[1], m[2], m[3]
                f = {'orange': '#fbe3cf', 'blue': '#dde6f3', 'grey': '#e2e2e2', 'yellow': '#fbf0c4'}.get(m[4] if len(m) > 4 else '', MV.BAND)
                b += ''.join('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="2.2"/>'
                             % (bx(i), rt(r), unit, boxh, f, _INK) for i in range(i0, i1))
            elif k == 'br':
                r, i0, i1, t = m[1], m[2], m[3], m[4]
                up = len(m) > 5 and m[5] == 'up'
                y = rt(r) - 8 if up else rt(r) + boxh + 8; d = -10 if up else 10
                xa, xb = bx(i0) + 3, bx(i1) - 3
                b += ('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="%s" stroke-width="2.6"/>'
                      % (xa, y, xa, y + d, xb, y + d, xb, y, _TEAL))
                b += _tx((xa + xb) / 2.0, y + d + (-8 if up else 30), t, 29, _TEAL)
            elif k == 'in':
                r, i, t = m[1], m[2], m[3]
                b += _tx(bx(i) + unit / 2.0, rt(r) + boxh * .7, t, 27, _TEAL)
            elif k == 'right':
                r, t = m[1], m[2]
                c = rows[r][1]
                b += _tx(bx(c) + 14, rt(r) + boxh * .7, t, 28, _TEAL, 'start')
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def OWN(d, name):
    """a ZL number line whose layers find their own base (written lines may come in between)"""
    for it in d.values():
        if it.get('over'): it['of'] = name
        else: it['fig'] = name
    return d



CARRY25 = {}      # vid -> carry-over ("So far") boxes, _method_visuals.carry format
SPLITS = []       # lessons split into parts (not on camera)


# ------------------------------------------------------------------------------------------- topic-25 figures (V1)
# The pictures of her Hebrew topic-25 lessons, built in layers at the spoken words (each layer a figure item drawn over
# its base; own=True: a layer finds its own base, so the written calculation lines can come in between):
#   TOWERS  the cube towers (wp 5211-5235: «נבנה מגדלי קוביות בגבהים לפי המספרים... לפני שאנחנו מתחילים בואו נתחום רגע
#           את הממוצע... נעביר קוביות מהמגדלים הגבוהים למגדלים הנמוכים... כל המגדלים באותו גובה»): the towers, the two
#           limits (the tallest and the shortest tower), the blocks above the average (orange) and the empty places below
#           it (dashed), then the blocks moved: every tower at the average.
#   SAW     the seesaw in its exam form (wp 5750-5782: «אנחנו מציירים ציר... מעל הציר... את הציונים... מתחת... את המשקל...
#           נחלק אותו ל-5 יחידות מרחק»): the axis, the values above the ends, the weights below, the gap cut into equal
#           units, the pivot (the average) nearer the heavy side, the two distances.
_ORF2 = '#fbd9b9'
LIGHTH = MV.LIGHT


def TOWERS(name, hs, layers, cube=34, gapx=34, col=0, w=None, title='Towers of blocks'):
    """towers of cubes, heights hs (left to right), the value under each tower. layers = [(key, [mark, ...])]:
      ('lim', level, text)     a red dashed line at this height across the towers, its text at the right
      ('lvl', level, text)     a teal dashed line at this height (the average), its text at the right
      ('extra', level)         the cubes above `level` tinted orange (the blocks that will move)
      ('gap', level)           dashed empty places from each short tower up to `level`
      ('move', level)          the blocks moved: the orange cubes gone, the empty places filled teal"""
    n = len(hs); top = max(hs); x0 = 20; y0 = 26
    W = x0 + n * (cube + gapx) + 190; H = y0 + top * cube + 52
    X = lambda i: x0 + gapx / 2.0 + i * (cube + gapx)
    Y = lambda k: y0 + (top - k) * cube          # the top edge of cube number k (1 = the bottom cube)
    base = Y(0)
    def sq(i, k, fill, stroke=_INK, dash=''):
        return ('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="2"%s/>'
                % (X(i), Y(k), cube, cube, fill, stroke, (' stroke-dasharray="%s"' % dash) if dash else ''))
    body = '<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.6"/>' % (x0, base, X(n - 1) + cube + gapx / 2.0, base, _INK)
    for i, h in enumerate(hs):
        body += ''.join(sq(i, k, LIGHTH) for k in range(1, h + 1))
        body += _tx(X(i) + cube / 2.0, base + 34, str(h), 28, _INK)
    out = [('line', MV._svg(W, H, body, '%s: %s' % (title, ', '.join(str(h) for h in hs))))]
    xr = X(n - 1) + cube + gapx / 2.0
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k in ('lim', 'lvl'):
                y = Y(m[1]); c = RED if k == 'lim' else _TEAL
                b += ('<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3" stroke-dasharray="9 6"/>'
                      % (x0, y, xr, y, c) + _tx(xr + 10, y + 9, m[2], 26, c, 'start'))
            elif k == 'extra':
                for i, h in enumerate(hs):
                    b += ''.join(sq(i, kk, _ORF2) for kk in range(m[1] + 1, h + 1))
            elif k == 'gap':
                for i, h in enumerate(hs):
                    b += ''.join(sq(i, kk, 'none', _TEAL, '6 4') for kk in range(h + 1, m[1] + 1))
            elif k == 'move':
                for i, h in enumerate(hs):
                    b += ''.join('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="#ffffff"/>' % (X(i) - 2, Y(kk) - 2, cube + 4, cube + 4)
                                 for kk in range(m[1] + 1, h + 1))
                    b += ''.join(sq(i, kk, MV.BAND, _TEAL) for kk in range(h + 1, m[1] + 1))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def SAW(name, v1, v2, layers, col=0, w=None, title='The seesaw'):
    """the weighted-average axis (exam form): v1 left, v2 right (labels). layers = [(key, [mark, ...])]:
      ('vals',)                the two values above the ends
      ('wts', t1, t2)          the weights below the ends (teal)
      ('mid', text)            a dashed tick at the middle of the axis with its text above (the plain middle)
      ('units', n)             the gap cut into n equal units (ticks)
      ('pivot', k, n, text)    the pivot k units of n from the left end, its value under it
      ('dl', k, n, text)       the distance from the left end to the pivot, written above the axis
      ('dr', k, n, text)       the distance from the pivot to the right end, written above the axis
      ('heavy', side)          a thick teal ring around the heavy end's weight (0 left, 1 right)"""
    L_, R_, Y_ = 70, 570, 112; W, H = 640, 262
    X = lambda k, n: L_ + (R_ - L_) * k / float(n)
    body = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>' % (L_, Y_, R_, Y_, _INK) +
            ''.join('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (x, Y_ - 13, x, Y_ + 13, _INK) for x in (L_, R_)))
    out = [('line', MV._svg(W, H, body, '%s: %s and %s' % (title, v1, v2)))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'vals':
                b += _tx(L_, Y_ - 54, v1, 46) + _tx(R_, Y_ - 54, v2, 46)
            elif k == 'wts':
                b += _tx(L_, Y_ + 62, m[1], 40, _TEAL) + _tx(R_, Y_ + 62, m[2], 40, _TEAL)
            elif k == 'mid':
                x = (L_ + R_) / 2.0
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.4" stroke-dasharray="6 5"/>' % (x, Y_ - 52, x, Y_ + 14, ORANGE)
                      + _tx(x, Y_ - 60, m[1], 34, ORANGE))
            elif k == 'units':
                b += ''.join('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.4"/>' % (X(j, m[1]), Y_ - 11, X(j, m[1]), Y_ + 11, _TEAL)
                             for j in range(1, m[1]))
            elif k == 'pivot':
                x = X(m[1], m[2])
                b += ('<path d="M %.1f %d L %.1f %d L %.1f %d Z" fill="%s"/>' % (x, Y_ + 4, x - 20, Y_ + 40, x + 20, Y_ + 40, _TEAL)
                      + _tx(x, Y_ + 84, m[3], 44, _TEAL))
            elif k in ('dl', 'dr'):
                a, e = (L_, X(m[1], m[2])) if k == 'dl' else (X(m[1], m[2]), R_)
                b += ('<path d="M %.1f %d L %.1f %d L %.1f %d L %.1f %d" fill="none" stroke="%s" stroke-width="2"/>'
                      % (a + 4, Y_ - 14, a + 4, Y_ - 22, e - 4, Y_ - 22, e - 4, Y_ - 14, _TEAL)
                      + _tx((a + e) / 2.0, Y_ - 30, m[3], 32, _TEAL))
            elif k == 'heavy':
                x = L_ if m[1] == 0 else R_
                b += '<rect x="%d" y="%d" width="%d" height="52" rx="10" fill="none" stroke="%s" stroke-width="3.5"/>' % (x - 48, Y_ + 26, 96, _TEAL)
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


# =================================================================================================================
# THE SCRIPTS (topic-25 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-25-AI-scripts-review.md.
# Study plan before topic 25: 1, 30, 2, 4, 31, 6, 8, 32, 9, 10, 33, 51, (39, 42), 21, 3, (43), 22, (41), 5, 7, (44), 23,
# 11, 24, (49), 12, (45). So fractions (2, 3), equations (6, 7), the method names and plugging in (51), ratios and
# "the bigger the weight" style ratio thinking (22), percents (23: 30% of a number) and inequalities (12) are REMINDERS.
# Numbers in a row and even / odd (topic 16) come LATER, so "consecutive even numbers" is explained where it is used.
# New here (all of it): the average as the middle, symmetric and evenly spaced numbers, adding a number equal to the
# average, between the smallest and the biggest, the formula (the towers), the balance (differences add up to zero; two
# numbers: exactly in the middle), a base number, one value / every value changes, sum = how many x average, a value
# joins or leaves (compare it to the average of the group it is in), the biggest (and the smallest biggest) possible
# value, plugging in equal values, an average equal to a letter, the balance with "more / less than", weighted averages
# (copies, the formula, the seesaw, groups as weights, percent shares), the seesaw backwards (find the group sizes).
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ wp-080 (camera lesson)
# Hebrew (wp 5175-5252): an average = a number that describes the middle; the exam says "average"; symmetric groups (10
# and 20 -> 15; 2, 4, 6, 8 -> 5; 2, 4, 6 -> 4, the average is also one of the numbers); rule 1: adding or removing
# numbers equal to the average doesn't change it; a group that isn't symmetric (12, 5, 4, 8, 5, 3, 6, 5): cube towers,
# "before we start, let's box the average in": never above the tallest, never below the shortest, strictly between them;
# share the blocks -> 6; the sum shared among the towers = the formula (48 / 8). The balance point ("ההגדרה הראשונה -
# ממוצע כנקודת איזון", wp 5362) is used in her next lesson; here it is taught on the towers (the tall towers give what the
# short ones get). English (camera lesson, 2-3 examples per idea, numbers differ from the Hebrew): 16 and 30, 6-10-14-18;
# evenly spaced 3 ... 19, numbers in a row 20 ... 30, an even count 4, 6, 8, 10; 3, 5, 7 plus another 5; towers 4, 9, 3,
# 11, 8 (the limits, the move, the level 7); the formula with a second example; the balance (differences add up to 0,
# a missing score, two numbers: exactly in the middle); a base number; one value changes; every value changes (+3, x2,
# ages, both). Real exam: 2024_winter_q2_07 (evenly spaced), 2024_spring_q1_07 / 2025_autumn_q1_18 (balance),
# 2025_autumn_q2_15 / 2022_winter_q1_08 (every value changes). NEW (all).
a_m0 = I('a_m0', 'An average describes the middle of a group of numbers', size=36)
a_m1 = I('a_m1', '$16$ and $30$', size=38)
a_z1 = OWN(ZL('a_z1', 13, 33, [('ends', [('ink', 16, ''), ('ink', 30, '')]),
                           ('mid', [('arrow', 23, 16, '7'), ('arrow', 23, 30, '7'), ('pt', 23, '23')])],
          ticks=(16, 30), w=560, title='16 and 30 on a number line'), 'a_z1')
a_m2 = IH('a_m2', '$16+7=23$', size=36, col=1)
a_m3 = IH('a_m3', '$23+7=30$', size=36, col=1)
a_m4 = I('a_m4', '$6,\\ 10,\\ 14,\\ 18$', size=38)
a_z2 = OWN(ZL('a_z2', 4, 20, [('mid', [('pt', 12, 'middle 12')])], ticks=(6, 10, 14, 18), w=560,
          title='6, 10, 14 and 18 on a number line'), 'a_z2')
a_m5 = IH('a_m5', '$6$ and $18$: $\\ $middle $12$', size=36, col=1)
a_m6 = IH('a_m6', '$10$ and $14$: $\\ $middle $12$', size=36, col=1)
a_m7 = I('a_m7', 'Symmetric numbers: $\\ $the average is the middle', size=36)
a_e1 = I('a_e1', '$3,\\ 7,\\ 11,\\ 15,\\ 19$', size=40)
a_e2 = IH('a_e2', 'each step: $\\ +4$', size=36)
a_e3 = IH('a_e3', '$3$ and $19$, $\\ 7$ and $15$, $\\ $middle $11$', size=36)
a_e4 = I('a_e4', 'Evenly spaced: $\\ $the average is the middle number', size=36)
a_e5 = IH('a_e5', '$3+19=22$', size=36, col=1)
a_e6 = IH('a_e6', '$22\\div2=11$', size=36, col=1)
a_e7 = I('a_e7', 'Or: $\\ $the first plus the last, divided by $2$', size=36)
a_n1 = I('a_n1', '$20,\\ 21,\\ 22,\\ \\dots,\\ 30$', size=40)
a_n2 = IH('a_n2', '$20+30=50$', size=36)
a_n3 = IH('a_n3', '$50\\div2=25$', size=36)
a_n4 = I('a_n4', '$4,\\ 6,\\ 8,\\ 10$', size=40)
a_n5 = IH('a_n5', 'middle numbers: $\\ 6$ and $8$', size=36)
a_n6 = IH('a_n6', 'halfway: $\\ 7$', size=36)
a_n7 = IH('a_n7', '$4+10=14$', size=36, col=1)
a_n8 = IH('a_n8', '$14\\div2=7$', size=36, col=1)
a_k1 = I('a_k1', '$3,\\ 5,\\ 7$: $\\ $average $5$', size=38)
a_k2 = I('a_k2', '$3,\\ 5,\\ 5,\\ 7$: $\\ $average still $5$', size=38)
a_k3 = I('a_k3', 'Add or remove a number equal to the average: $\\ $the average stays', size=36)
a_k4 = IH('a_k4', 'average $10$, $\\ $add $10$: $\\ $still $10$', size=36)
a_k5 = IH('a_k5', 'add $12$: $\\ $the average goes up', size=36)
# part 2
a_t0 = I('a_t0', '$4,\\ 9,\\ 3,\\ 11,\\ 8$', size=40)
a_tw = TOWERS('a_tw', [4, 9, 3, 11, 8], [
    ('hi', [('lim', 11, 'at most 11')]), ('lo', [('lim', 3, 'at least 3')]),
    ('extra', [('extra', 7)]), ('gap', [('gap', 7)]), ('move', [('move', 7), ('lvl', 7, '7 each')])], w=560)
a_t1 = I('a_t1', 'The average is between the smallest and the biggest number', size=34, col=1)
a_t2 = IH('a_t2', 'give: $\\ 2+4+1=7$', size=36, col=1)
a_t3 = IH('a_t3', 'get: $\\ 3+4=7$', size=36, col=1)
a_f1 = IH('a_f1', '$4+9+3=16$', size=36)
a_f2 = IH('a_f2', '$16+11+8=35$', size=36)
a_f3 = IH('a_f3', '$35\\div5=7$', size=36)
a_f4 = I('a_f4', 'average $=\\dfrac{\\text{the sum}}{\\text{how many numbers}}$', size=40)
a_f5 = I('a_f5', '$2,\\ 5,\\ 11$', size=38, col=1)
a_f6 = IH('a_f6', '$2+5+11=18$', size=36, col=1)
a_f7 = IH('a_f7', '$18\\div3=6$', size=36, col=1)
a_f8 = IH('a_f8', '$6$ is between $2$ and $11$', size=36, col=1)
a_b0 = TBL('a_b0', ['4', '9', '3', '11', '8'], ['vs. 7'], [
    ('d', [('c', 0, 0, '−3'), ('c', 0, 1, '+2'), ('c', 0, 2, '−4'), ('c', 0, 3, '+4'), ('c', 0, 4, '+1')])],
    colw=110, labw=150, rowh=66, w=760)
a_b1 = IH('a_b1', '$+2+4+1=+7$ $\\ $above', size=36)
a_b2 = IH('a_b2', '$-3-4=-7$ $\\ $below', size=36)
a_b3 = I('a_b3', 'The balance: $\\ $the differences from the average add up to $0$', size=36)
a_c0 = I('a_c0', '$86,\\ 93,\\ 95,\\ ?$ $\\quad$ average $90$', size=38)
a_c1 = TBL('a_c1', ['86', '93', '95', '?'], ['vs. 90'], [
    ('d1', [('c', 0, 0, '−4')]), ('d2', [('c', 0, 1, '+3')]), ('d3', [('c', 0, 2, '+5')]), ('d4', [('c', 0, 3, '−4', _TEAL)])],
    colw=110, labw=150, rowh=66, w=560)
a_c2 = IH('a_c2', '$-4+3+5=+4$', size=36, col=1)
a_c3 = IH('a_c3', '$90-4=86$', size=36, col=1)
a_c4 = IH('a_c4', '$-4+3+5-4=0$', size=36, col=1)
a_d0 = I('a_d0', 'Two numbers: $\\ $the average is exactly in the middle', size=36)
a_d1 = I('a_d1', '$40$ and $?$ $\\quad$ average $47$', size=38)
a_z3 = OWN(ZL('a_z3', 37, 57, [('a', [('ink', 40, '40')]), ('m', [('arrow', 47, 40, '7')]), ('b', [('arrow', 47, 54, '7'), ('pt', 54, '54')])],
          ticks=(47,), w=560, title='40, the average 47 and the other number'), 'a_z3')
a_d2 = IH('a_d2', '$47-40=7$', size=36, col=1)
a_d3 = IH('a_d3', '$47+7=54$', size=36, col=1)
# part 3
a_g0 = I('a_g0', '$97,\\ 102,\\ 104,\\ 99$', size=40)
a_g1 = TBL('a_g1', ['97', '102', '104', '99'], ['vs. 100'], [
    ('d', [('c', 0, 0, '−3'), ('c', 0, 1, '+2'), ('c', 0, 2, '+4'), ('c', 0, 3, '−1')])], colw=110, labw=150, rowh=66, w=560)
a_g2 = IH('a_g2', 'minus: $\\ -3-1=-4$', size=36, col=1)
a_g3 = IH('a_g3', 'plus: $\\ 2+4=6$', size=36, col=1)
a_g4 = IH('a_g4', '$6-4=2$', size=36, col=1)
a_g5 = IH('a_g5', '$2\\div4=\\frac{1}{2}$', size=36, col=1)
a_g6 = IH('a_g6', 'average: $\\ 100\\frac{1}{2}$', size=36, col=1)
a_h1 = I('a_h1', '$5$ scores: $\\ $one goes up by $10$', size=38)
a_h2 = IH('a_h2', 'the sum: $\\ +10$', size=36)
a_h3 = IH('a_h3', '$10\\div5=2$: $\\ $the average $+2$', size=36)
a_h4 = I('a_h4', '$4$ numbers: $\\ $one goes down by $12$', size=38)
a_h5 = IH('a_h5', '$12\\div4=3$: $\\ $the average $-3$', size=36)
a_v0 = I('a_v0', '$2,\\ 4,\\ 9$', size=40)
a_v1 = IH('a_v1', '$2+4+9=15$', size=36)
a_v2 = IH('a_v2', '$15\\div3=5$', size=36)
a_v3 = I('a_v3', '$+3$: $\\ 5,\\ 7,\\ 12$', size=38)
a_v4 = IH('a_v4', '$5+7+12=24$', size=36)
a_v5 = IH('a_v5', '$24\\div3=8$', size=36)
a_v5b = IH('a_v5b', '$8=5+3$', size=36)
a_v6 = I('a_v6', '$\\times2$: $\\ 4,\\ 8,\\ 18$', size=38, col=1)
a_v7 = IH('a_v7', '$4+8+18=30$', size=36, col=1)
a_v8 = IH('a_v8', '$30\\div3=10$', size=36, col=1)
a_v8b = IH('a_v8b', '$10=5\\times2$', size=36, col=1)
a_v9 = I('a_v9', 'Every value changes the same way: $\\ $so does the average', size=36)
a_w1 = IH('a_w1', 'ages: $\\ $average $31$, $\\ $in $4$ years: $\\ 35$', size=36)
a_w2 = IH('a_w2', '$\\times2$, then $+1$: $\\ 5\\times2=10$', size=36)
a_w3 = IH('a_w3', '$10+1=11$', size=36)
a_s1 = I('a_s1', 'Symmetric or evenly spaced: $\\ $the middle', size=36)
a_s2 = I('a_s2', 'Between the smallest and the biggest number', size=36)
a_s3 = I('a_s3', 'average $=$ the sum $\\div$ how many numbers', size=36)
a_s4 = I('a_s4', 'The balance: $\\ $the differences add up to $0$', size=36)
a_s5 = I('a_s5', 'Every value changes the same way: $\\ $so does the average', size=36)
video('wp-080', 'lesson', slides=[
    S('Averages',
      L("Welcome back, and now a new topic, averages."),
      L("Average questions come up in almost every exam. They use a few simple ideas. Once you know them, these questions "
        "are quick.")),
    S('What is an average?',
      L("On the exam, it usually just says the average. It's the average you know from school.", show(a_m0, "It's the average you know")),
      L("An average is one number that describes the middle of a group of numbers. So let's see what the middle means."),
      L("Let's start with the easy case, numbers that are symmetric. Take sixteen and thirty. Where's the middle?",
        show(a_m1, 'Take sixteen and thirty'), show(a_z1['line'], "Where's the middle"), show(a_z1['ends'], "Where's the middle")),
      L("Sixteen plus seven is twenty-three. And twenty-three plus seven is thirty.", show(a_m2, 'Sixteen plus seven'),
        show(a_m3, 'twenty-three plus seven')),
      L("So twenty-three is seven above sixteen, and seven below thirty. It's exactly in the middle.",
        show(a_z1['mid'], "It's exactly in the middle")),
      L("So the average of sixteen and thirty is twenty-three.")),
    S('Symmetric numbers',
      L("Now four numbers. Six, ten, fourteen and eighteen.", show(a_m4, 'Six, ten, fourteen'), show(a_z2['line'], 'Six, ten, fourteen')),
      L("Six and eighteen are a pair. Their middle is twelve, because six plus six is twelve, and twelve plus six is eighteen.",
        show(a_m5, 'Six and eighteen are a pair')),
      L("Ten and fourteen are also a pair. Ten plus two is twelve, and twelve plus two is fourteen. So their middle is twelve "
        "too.", show(a_m6, 'Ten and fourteen are also a pair')),
      L("Every pair has the same middle, twelve. So the average of all four numbers is twelve.",
        show(a_z2['mid'], 'Every pair has the same middle')),
      L("So when the numbers are symmetric, the average is the middle. We don't need to calculate.",
        show(a_m7, 'So when the numbers are symmetric'))),
    S('Evenly spaced',
      L("On the exam, symmetric numbers often come as evenly spaced numbers. That means each number is the same step above "
        "the one before."),
      L("For example, three, seven, eleven, fifteen and nineteen.", show(a_e1, 'three, seven, eleven')),
      L("Each one is four more than the one before.", show(a_e2, 'Each one is four more')),
      L("Evenly spaced numbers are symmetric around the middle one. Three and nineteen are a pair. Seven and fifteen are a "
        "pair. And eleven is in the middle.", show(a_e3, 'Three and nineteen are a pair')),
      L("So the average is the middle number, eleven.", show(a_e4, 'So the average is the middle number')),
      L("There's another way. Take the first number and the last number, and find their middle.", show(a_e7, 'There\'s another way')),
      L("Three plus nineteen is twenty-two. And twenty-two divided by two is eleven. The same eleven.",
        show(a_e5, 'Three plus nineteen'), show(a_e6, 'twenty-two divided by two'))),
    S('Numbers in a row',
      L("Numbers in a row are evenly spaced too. For example, twenty, twenty-one, twenty-two, and so on up to thirty. Each "
        "step is one.", show(a_n1, 'For example, twenty, twenty-one')),
      L("So the average is the first plus the last, divided by two. Twenty plus thirty is fifty. Fifty divided by two is "
        "twenty-five.", show(a_n2, 'Twenty plus thirty'), show(a_n3, 'Fifty divided by two')),
      L("And what if there's no single middle number? Take four, six, eight and ten. That's four numbers, so there are two "
        "middle numbers, six and eight.", show(a_n4, 'Take four, six, eight'), show(a_n5, 'two middle numbers')),
      L("Then the average is halfway between them, seven.", show(a_n6, 'halfway between them')),
      L("And the first plus the last works here too. Four plus ten is fourteen, and fourteen divided by two is seven.",
        show(a_n7, 'Four plus ten'), show(a_n8, 'fourteen divided by two'))),
    S('Adding the average',
      L("Now let's add a number to a group. Take three, five and seven. The average is five, the middle.",
        show(a_k1, 'Take three, five and seven')),
      L("And five is also one of the numbers. It sits right on the middle."),
      L("Now let's add another five. What's the average of three, five, five and seven? Three and seven are still a pair "
        "around five. So the average is still five.", show(a_k2, "What's the average of three, five, five")),
      L("Why? A number that is equal to the average sits on the middle. It doesn't pull the middle up, and it doesn't pull "
        "it down."),
      L("So here's our first rule. If we add or remove a number equal to the average, the average doesn't change.",
        show(a_k3, "So here's our first rule")),
      L("For example, four numbers have an average of ten. We add a fifth number, ten. The average stays ten.",
        show(a_k4, 'four numbers have an average of ten')),
      L("But if we add twelve, that's more than the average. So the average goes up.", show(a_k5, 'But if we add twelve'))),
    S('Towers of blocks',
      L("Now the harder case, numbers that aren't symmetric. For example, four, nine, three, eleven and eight.",
        show(a_t0, 'For example, four, nine, three')),
      L("Let's draw each number as a tower of blocks. Four blocks, nine blocks, three, eleven and eight.",
        show(a_tw['line'], "Let's draw each number")),
      L("To find the average, we share the blocks equally, so that all the towers have the same height."),
      L("Before we share, let's find the limits. We'll only move blocks from the tall towers to the short ones."),
      L("So no tower can end up taller than eleven, the tallest tower now. And no tower can end up shorter than three, the "
        "shortest one.", show(a_tw['hi'], 'So no tower can end up taller'), show(a_tw['lo'], 'And no tower can end up shorter')),
      L("So the average is always between the smallest number and the biggest number.", show(a_t1, 'So the average is always between')),
      L("And when the numbers aren't all equal, the average can't be the smallest or the biggest number. It's somewhere in "
        "between."),
      L("Now let's share the blocks. Let's try to make every tower seven blocks high. Above seven, nine has two extra "
        "blocks, eleven has four, and eight has one.", show(a_tw['extra'], 'Above seven, nine has two')),
      L("Two plus four plus one is seven blocks to give.", show(a_t2, 'Two plus four plus one')),
      L("The two short towers get them. Four needs three blocks, and three needs four blocks. Three plus four is seven.",
        show(a_tw['gap'], 'The two short towers get them'), show(a_t3, 'Three plus four is seven')),
      L("It works. The tall towers give exactly what the short towers need. Now every tower is seven blocks high.",
        show(a_tw['move'], 'Now every tower is seven')),
      L("So the average of these five numbers is seven. We didn't add or remove a single block. We just shared them "
        "equally.")),
    S('The formula',
      L("So what did we really do? We took all the blocks, that's the sum. And we shared them among the towers, that's how "
        "many numbers there are."),
      L("Let's count the blocks. Four plus nine plus three is sixteen. Sixteen plus eleven plus eight is thirty-five.",
        show(a_f1, 'Four plus nine plus three'), show(a_f2, 'Sixteen plus eleven plus eight')),
      L("There are five towers. Thirty-five divided by five is seven. The same seven.", show(a_f3, 'Thirty-five divided by five')),
      L("That's the formula from school. The average is equal to the sum, divided by how many numbers there are.",
        show(a_f4, "That's the formula from school")),
      L("Let's try it once more, on two, five and eleven.", show(a_f5, 'on two, five and eleven')),
      L("Two plus five plus eleven is eighteen. There are three numbers. Eighteen divided by three is six.",
        show(a_f6, 'Two plus five plus eleven'), show(a_f7, 'Eighteen divided by three')),
      L("And six is between two and eleven, as it must be.", show(a_f8, 'And six is between'))),
    S('The balance',
      L("Now look at the towers again. The tall towers gave seven blocks, and the short towers got seven blocks."),
      L("Let's write how far each number is from the average, seven. Plus above the average, and minus below it.",
        show(a_b0['line'], "Let's write how far")),
      L("Four is three below, minus three. Nine is plus two. Three is minus four. Eleven is plus four. Eight is plus one.",
        show(a_b0['d'], 'Four is three below')),
      L("Above the average, two plus four plus one is seven. Below it, three plus four is seven.",
        show(a_b1, 'Above the average'), show(a_b2, 'Below it')),
      L("So the amount above the average is equal to the amount below it. And that's always true, for any group."),
      L("In other words, the differences from the average add up to zero. We call this the balance. It's the fastest tool "
        "in average questions.", show(a_b3, 'add up to zero'))),
    S('The balance: a missing number',
      L("Let's use it. Four test scores, eighty-six, ninety-three, ninety-five and one more. The average is ninety. What's "
        "the missing score?", show(a_c0, 'Four test scores')),
      L("Let's compare each score to ninety, the average.", show(a_c1['line'], 'compare each score')),
      L("Eighty-six is four below ninety, so minus four. Ninety-three is three above, plus three. Ninety-five is five "
        "above, plus five.", show(a_c1['d1'], 'so minus four'), show(a_c1['d2'], 'plus three'), show(a_c1['d3'], 'plus five')),
      L("Together, minus four plus three plus five is plus four.", show(a_c2, 'Together, minus four')),
      L("So the three scores we know are four points above the average, together. The missing score must balance them. So "
        "it's four points below ninety."),
      L("Ninety minus four is eighty-six.", show(a_c3, 'Ninety minus four'), show(a_c1['d4'], 'eighty-six')),
      L("Now the differences add up to zero. And we did no big sum and no division, only small differences.",
        show(a_c4, 'Now the differences add up to zero'))),
    S('Two numbers',
      L("With only two numbers, the balance is even simpler. The average of two numbers is exactly in the middle between "
        "them.", show(a_d0, 'The average of two numbers is exactly')),
      L("For example, the average of forty and another number is forty-seven. What's the other number?",
        show(a_d1, 'the average of forty and another'), show(a_z3['line'], "What's the other number")),
      L("Forty is seven below forty-seven, because forty-seven minus forty is seven.", show(a_z3['a'], 'Forty is seven below'),
        show(a_z3['m'], 'Forty is seven below'), show(a_d2, 'forty-seven minus forty')),
      L("So the other number is seven above the average. Forty-seven plus seven is fifty-four.",
        show(a_z3['b'], 'So the other number is seven above'), show(a_d3, 'Forty-seven plus seven')),
      L("So when you see an average and one missing number, think of the balance.")),
    S('A base number',
      L("The balance also helps with calculations. Let's find the average of ninety-seven, a hundred two, a hundred four "
        "and ninety-nine.", show(a_g0, "Let's find the average of")),
      L("We don't add them up. These numbers are all near a hundred. So we pick a hundred as a base, and we write only the "
        "differences.", show(a_g1['line'], 'we write only the differences')),
      L("Ninety-seven is three below, so minus three. A hundred two is two above, so plus two. A hundred four is four "
        "above, so plus four. Ninety-nine is one below, so minus one.", show(a_g1['d'], 'Ninety-seven is three below')),
      L("The minuses are minus three and minus one. Together, that's minus four.", show(a_g2, 'The minuses are')),
      L("The pluses are two and four. Together, that's plus six.", show(a_g3, 'The pluses are')),
      L("Together, six minus four is plus two. So the four numbers have two extra above the base.",
        show(a_g4, 'six minus four')),
      L("Shared among four numbers, two divided by four is one half.", show(a_g5, 'two divided by four')),
      L("So the average is a hundred plus one half, a hundred and a half.", show(a_g6, 'So the average is a hundred plus')),
      L("So when the numbers are close to a round number, use it as a base. The numbers stay small, so we make fewer "
        "mistakes.")),
    S('One value changes',
      L("Now what happens when one value changes? Five students took a test. One score goes up by ten points.",
        show(a_h1, 'One score goes up')),
      L("The sum goes up by ten. There are still five scores, so we share the ten among them.", show(a_h2, 'The sum goes up')),
      L("Ten divided by five is two. So the average goes up by two points.", show(a_h3, 'Ten divided by five')),
      L("And we didn't need any of the scores. The change in the sum is shared among all the values."),
      L("One more. One of four numbers goes down by twelve. Twelve divided by four is three. So the average goes down by "
        "three.", show(a_h4, 'One of four numbers'), show(a_h5, 'Twelve divided by four'))),
    S('Every value changes',
      L("Now every value changes in the same way. Take two, four and nine.", show(a_v0, 'Take two, four and nine')),
      L("Two plus four plus nine is fifteen. Fifteen divided by three is five. So the average is five.",
        show(a_v1, 'Two plus four plus nine'), show(a_v2, 'Fifteen divided by three')),
      L("Let's add three to every value. We get five, seven and twelve.", show(a_v3, "Let's add three")),
      L("Five plus seven plus twelve is twenty-four. Twenty-four divided by three is eight. And eight is five plus three.",
        show(a_v4, 'Five plus seven plus twelve'), show(a_v5, 'Twenty-four divided by three'), show(a_v5b, 'And eight is five plus three')),
      L("Every tower grew by three blocks, so the average grew by three too."),
      L("Now let's multiply every value by two. We get four, eight and eighteen.", show(a_v6, "multiply every value by two")),
      L("Four plus eight plus eighteen is thirty. Thirty divided by three is ten. And ten is five times two.",
        show(a_v7, 'Four plus eight plus eighteen'), show(a_v8, 'Thirty divided by three'), show(a_v8b, 'And ten is five times two')),
      L("Every value doubled, so the sum doubled, and the average doubled too."),
      L("So when every value changes in the same way, the average changes in the same way.",
        show(a_v9, 'So when every value changes'))),
    S('Every value changes: examples',
      L("Here's a classic. The average age in a family is thirty-one. In four years, everyone is four years older. So the "
        "average age will be thirty-one plus four, thirty-five.", show(a_w1, 'The average age in a family')),
      L("And what if every value is multiplied by two, and then one is added? We do the same steps to the average, in the "
        "same order."),
      L("For two, four and nine, the average is five. Five times two is ten, and ten plus one is eleven.",
        show(a_w2, 'Five times two is ten'), show(a_w3, 'ten plus one is eleven')),
      L("Let's check. Two, four and nine become five, nine and nineteen. Their sum is thirty-three. Thirty-three divided "
        "by three is eleven. It works.")),
    S('Summary',
      L("Let's sum up this lesson. When the numbers are symmetric or evenly spaced, the average is the middle.",
        show(a_s1, 'When the numbers are symmetric')),
      L("The average is always between the smallest number and the biggest number.", show(a_s2, 'The average is always between')),
      L("The average is equal to the sum, divided by how many numbers there are.", show(a_s3, 'The average is equal to the sum')),
      L("The balance. The differences from the average add up to zero.", show(a_s4, 'The differences from the average')),
      L("And when every value changes in the same way, the average changes in the same way.",
        show(a_s5, 'And when every value changes')),
      L("Take a moment to memorize this. Next, we'll turn the formula around. I'll see you in the next video.")),
])
CAMERA_SPLIT = ('wp-080', 'Averages', [
    (1, None),
    (6, "Let's continue with averages, and look at numbers that aren't symmetric."),
    (11, "Let's continue, and see three more tools for averages.")])


# ------------------------------------------------------------------------------------------------ wp-081 (lesson: sum)
# Hebrew (wp 5253-5326): 8 / 2 = 4, so 8 = 2 x 4: the sum = how many x the average; "sometimes I don't know the numbers
# ... I treat each one as if it were the average" (3 numbers, average 5 -> 15, "maybe 6, 8, 3, I don't know"); her sample
# question is our g082. English (R37, the core methods of the topic's questions, 2-3 examples each, numbers differ from
# the Hebrew): turn the formula around; each value as the average (4 numbers of average 6; 9 players, 8 points); a value
# joins (20 -> 22 with 30: 4 before) or leaves (50 -> 45 without 80: 6 left): compare the value to the average of the
# group it is in; the biggest possible value (positive / whole / different change the answer) and the smallest possible
# biggest value; plugging in equal values for letters; an average equal to a letter or to the difference; the balance
# with "more / less than". Real exam: 2026_spring_q2_15, 2020_winter_q2_20 (joins / leaves), 2025_spring_q1_05,
# 2024_winter_q1_17 (biggest / smallest possible), 2023_autumn_q1_03, 2024_autumn_q1_08 (equal to a letter / the
# difference), 2026_spring_q1_04 (more / less than 8). NEW (all); the formula and the balance are REMINDERS (wp-080).
b_s0 = I('b_s0', 'average $=\\dfrac{\\text{the sum}}{\\text{how many}}$', size=40)
b_s1 = IH('b_s1', '$12\\div3=4$', size=36, col=1)
b_s2 = IH('b_s2', '$12=3\\times4$', size=36, col=1)
b_s3 = I('b_s3', 'the sum $=$ how many $\\times$ the average', size=40)
b_e0 = I('b_e0', '$4$ numbers, $\\ $average $6$. $\\ $The sum?', size=38)
b_e1 = IH('b_e1', '$6+6+6+6$', size=36)
b_e2 = IH('b_e2', '$4\\times6=24$', size=36)
b_e3 = IH('b_e3', '$2+5+7+10=24$', size=36, col=1)
b_e4 = I('b_e4', '$9$ players, $\\ $average $8$ points', size=38)
b_e5 = IH('b_e5', '$9\\times8=72$', size=36)
b_e6 = I('b_e6', 'Average and how many? $\\ $Write the sum.', size=36)
b_j0 = I('b_j0', 'Average $20$. $\\ 30$ joins. $\\ $Now the average is $22$. $\\ $How many before?', size=36)
b_j1 = IH('b_j1', '$30-22=8$ $\\ $above', size=36)
b_j2 = IH('b_j2', '$22-20=2$ $\\ $below, each', size=36)
b_j3 = IH('b_j3', '$8\\div2=4$ $\\ $numbers before', size=36)
b_j4 = IH('b_j4', '$4\\times20=80$', size=36, col=1)
b_j5 = IH('b_j5', '$80+30=110$', size=36, col=1)
b_j6 = IH('b_j6', '$110\\div5=22$', size=36, col=1)
b_j7 = I('b_j7', 'Before: $\\ 4$. $\\ $After: $\\ 5$. $\\ $Read what they ask.', size=36, col=1)
b_l0 = I('b_l0', 'Average $50$. $\\ 80$ leaves. $\\ $Now the average is $45$. $\\ $How many are left?', size=36)
b_l1 = IH('b_l1', '$80-50=30$ $\\ $above', size=36)
b_l2 = IH('b_l2', '$50-45=5$ $\\ $below, each', size=36)
b_l3 = IH('b_l3', '$30\\div5=6$ $\\ $numbers left', size=36)
b_l4 = IH('b_l4', '$6\\times45=270$', size=36, col=1)
b_l5 = IH('b_l5', '$270+80=350$', size=36, col=1)
b_l6 = IH('b_l6', '$7\\times50=350$', size=36, col=1)
b_l7 = I('b_l7', 'Compare the number to the average of the group it is in', size=36)
b_x0 = I('b_x0', '$5$ positive whole numbers, $\\ $average $10$. $\\ $The biggest one?', size=36)
b_x1 = IH('b_x1', '$5\\times10=50$', size=36)
b_x2 = IH('b_x2', '$1+1+1+1=4$', size=36)
b_x3 = IH('b_x3', '$50-4=46$', size=36)
b_x4 = I('b_x4', 'different: $\\ 1,\\ 2,\\ 3,\\ 4$', size=36, col=1)
b_x5 = IH('b_x5', '$1+2+3+4=10$', size=36, col=1)
b_x6 = IH('b_x6', '$50-10=40$', size=36, col=1)
b_x7 = I('b_x7', 'positive $\\cdot$ whole $\\cdot$ different: $\\ $each one changes the answer', size=36)
b_y0 = I('b_y0', '$5$ days, $\\ 22$ calls. $\\ $One day had more calls than any other day. $\\ $At least?', size=34)
b_y1 = IH('b_y1', '$22\\div5$: $\\ $between $4$ and $5$', size=36)
b_y2 = IH('b_y2', '$5$: $\\ $the others at most $4$', size=36)
b_y3 = IH('b_y3', '$5+4\\times4=21$, $\\ $not $22$', size=36)
b_y4 = IH('b_y4', '$6+4\\times5=26$, $\\ $enough', size=36)
b_y5 = I('b_y5', 'The biggest? $\\ $The others as small as they can be.', size=36, col=1)
b_y6 = I('b_y6', 'The smallest biggest? $\\ $The others as big as they can be.', size=36, col=1)
b_p0 = I('b_p0', 'average of $a,\\ b,\\ c$ $=8$', size=38)
b_p1 = I('b_p1', 'average of $a+5,\\ b+5,\\ c+5$ $=\\ ?$', size=38)
b_p2 = IH('b_p2', '$a=b=c=8$', size=36)
b_p3 = IH('b_p3', '$8+5=13$', size=36)
b_p4 = IH('b_p4', 'average: $\\ 13$', size=36)
b_p5 = I('b_p5', '"different"? $\\ $Don\'t make them equal.', size=36, col=1)
b_p6 = I('b_p6', 'Two choices the same? $\\ $Try other numbers.', size=36, col=1)
b_q0 = I('b_q0', 'average of $x,\\ y,\\ z$ $=x$', size=38)
b_q1 = IH('b_q1', '$x+y+z=3x$', size=36)
b_q2 = IH('b_q2', '$y+z=2x$', size=36)
b_q3 = IH('b_q3', 'average of $y,\\ z$ $=x$', size=36)
b_q4 = I('b_q4', 'average of $m,\\ n$ $=m-n$', size=38, col=1)
b_q5 = IH('b_q5', '$m+n=2(m-n)$', size=36, col=1)
b_q6 = IH('b_q6', '$m+n=2m-2n$', size=36, col=1)
b_q7 = IH('b_q7', '$3n=m$', size=36, col=1)
b_q8 = IH('b_q8', '$n=2,\\ m=6$', size=36, col=1)
b_q9 = IH('b_q9', 'average: $\\ 8\\div2=4$', size=36, col=1)
b_q10 = IH('b_q10', 'difference: $\\ 6-2=4$', size=36, col=1)
b_r0 = I('b_r0', 'average of $a,\\ b,\\ c$ $>6$', size=38)
b_r1 = I('b_r1', 'average of $a,\\ b,\\ c,\\ d$ $<6$', size=38)
b_r2 = IH('b_r2', '$a+b+c>3\\times6=18$', size=36)
b_r3 = IH('b_r3', '$a+b+c+d<4\\times6=24$', size=36)
b_r4 = IH('b_r4', 'so $d<24-18=6$', size=36)
b_r5 = IH('b_r5', '$a=2,\\ b=9,\\ c=10$: $\\ 21\\div3=7$', size=36, col=1)
b_r6 = IH('b_r6', '$a=2$ is below $6$', size=36, col=1)
b_r7 = I('b_r7', 'Must be true? $\\ $Test the others with numbers.', size=36, col=1)
b_z1 = I('b_z1', 'the sum $=$ how many $\\times$ the average', size=36)
b_z2 = I('b_z2', 'A number joins or leaves: $\\ $compare it to the average of the group it is in', size=34)
b_z3 = I('b_z3', 'The biggest one: $\\ $the others as small as they can be', size=36)
b_z4 = I('b_z4', 'Letters: $\\ $plug in equal values, $\\ $or write the sum', size=36)
video('wp-081', 'lesson', slides=[
    S('Sum from the Average',
      L("Welcome back. Now one small step with the formula, and it solves a lot of exam questions.")),
    S('Turn it around',
      L("Remember the formula. The average is equal to the sum, divided by how many numbers there are.",
        show(b_s0, 'Remember the formula')),
      L("Let's see it in numbers. Twelve divided by three is four. So twelve is three times four.",
        show(b_s1, 'Twelve divided by three'), show(b_s2, 'So twelve is three times four')),
      L("The formula works the same way. The sum is equal to how many numbers there are, times the average.",
        show(b_s3, 'The sum is equal to how many')),
      L("Why do we need it? Because often we don't know the numbers. But we know how many there are, and their average.")),
    S('Each value as the average',
      L("For example, four numbers have an average of six. What's their sum?", show(b_e0, 'four numbers have an average of six')),
      L("We don't know the numbers. Maybe they're two, five, seven and ten. Maybe they're all six. It doesn't matter."),
      L("We can treat every number as if it were the average. So we have four numbers of six each.", show(b_e1, 'four numbers of six each')),
      L("Four times six is twenty-four. That's the sum.", show(b_e2, 'Four times six')),
      L("Let's check with two, five, seven and ten. Two plus five is seven, plus seven is fourteen, plus ten is twenty-four. "
        "The same sum.", show(b_e3, "Let's check with two")),
      L("One more. A team of nine players scored an average of eight points each. How many points did they score "
        "together?", show(b_e4, 'A team of nine players')),
      L("Nine players, eight points each on average. Nine times eight is seventy-two.", show(b_e5, 'Nine times eight')),
      L("So when you see the average and how many, write the sum right away.", show(b_e6, 'write the sum right away'))),
    S('A number joins',
      L("Now a new number joins a group. The average of a group of numbers is twenty. A new number, thirty, joins the "
        "group. Now the average is twenty-two. How many numbers were there before?", show(b_j0, 'A new number, thirty')),
      L("Let's use the balance. Now thirty is in the group, so we compare it to the new average. Thirty minus twenty-two is "
        "eight. So thirty is eight above the new average.", show(b_j1, 'Thirty minus twenty-two')),
      L("The old numbers had an average of twenty. So each one counts as twenty, like we just saw. That's two below "
        "the new average.", show(b_j2, "That's two below")),
      L("The eight above must balance the old numbers below. Each old number is two below. Eight divided by two is four. So "
        "there were four numbers before.", show(b_j3, 'Eight divided by two')),
      L("Let's check with sums. Before, four numbers with an average of twenty. Four times twenty is eighty.",
        show(b_j4, 'Four times twenty')),
      L("Thirty joins. Eighty plus thirty is a hundred ten. Now there are five numbers. A hundred ten divided by five is "
        "twenty-two. Correct.", show(b_j5, 'Eighty plus thirty'), show(b_j6, 'A hundred ten divided by five')),
      L("And careful. They asked how many there were before. After the new number joined, there are five. So always read "
        "which one they ask.", show(b_j7, 'They asked how many there were before'))),
    S('A number leaves',
      L("It works the same when a number leaves. The average of a group is fifty. One number, eighty, leaves. Now the "
        "average is forty-five. How many numbers are left?", show(b_l0, 'One number, eighty, leaves')),
      L("This time eighty was in the old group, so we compare it to the old average. Eighty minus fifty is thirty. So "
        "eighty is thirty above.", show(b_l1, 'Eighty minus fifty')),
      L("The numbers that are left have an average of forty-five. Fifty minus forty-five is five. So each one is five "
        "below fifty.", show(b_l2, 'Fifty minus forty-five')),
      L("Thirty divided by five is six. So six numbers are left.", show(b_l3, 'Thirty divided by five')),
      L("Let's check. Six times forty-five is two hundred seventy. Plus eighty is three hundred fifty. And seven numbers "
        "with an average of fifty also give seven times fifty, three hundred fifty.", show(b_l4, 'Six times forty-five'),
        show(b_l5, 'Plus eighty'), show(b_l6, 'seven times fifty')),
      L("So compare the number to the average of the group it is in. Joins, the new average. Leaves, the old average.",
        show(b_l7, 'So compare the number'))),
    S('The biggest possible value',
      L("Now a different kind of question. Five positive whole numbers have an average of ten. What's the biggest possible "
        "value of one of them?", show(b_x0, 'Five positive whole numbers')),
      L("First the sum. Five numbers, average ten. Five times ten is fifty.", show(b_x1, 'Five times ten')),
      L("To make one number as big as it can be, we make the other four as small as they can be."),
      L("The smallest positive whole number is one. So the other four are one each. One plus one plus one plus one is "
        "four.", show(b_x2, 'One plus one plus one')),
      L("So the big one gets the rest. Fifty minus four is forty-six.", show(b_x3, 'Fifty minus four')),
      L("Now careful. If the question says the numbers are different, we can't use four ones. The four smallest different "
        "positive whole numbers are one, two, three and four.", show(b_x4, 'The four smallest different')),
      L("One plus two plus three plus four is ten. So the big one is fifty minus ten, forty.", show(b_x5, 'One plus two plus three'),
        show(b_x6, 'fifty minus ten')),
      L("So watch the words positive, whole and different. Each one changes the answer.", show(b_x7, 'So watch the words'))),
    S('The smallest biggest value',
      L("And the opposite question. In five days, Dan made twenty-two phone calls. On one day he made more calls than on "
        "any other day. At least how many calls did he make on that day?", show(b_y0, 'In five days')),
      L("The average is twenty-two divided by five. That's more than four and less than five. The busiest day is at least "
        "the average, so it's at least five.", show(b_y1, 'twenty-two divided by five')),
      L("Let's try five. Then every other day had fewer calls, so at most four.", show(b_y2, "Let's try five")),
      L("So five calls on the busiest day, and four other days with four calls each. Four times four is sixteen, plus "
        "five is twenty-one. That's less than twenty-two, so five is not enough.", show(b_y3, 'Four times four is sixteen')),
      L("Let's try six. The other days can have up to five each. Four times five is twenty, plus six is twenty-six. That's "
        "enough, and the other days can simply have fewer calls. So the answer is six.", show(b_y4, 'Four times five is twenty')),
      L("So for the biggest possible value, make the others as small as they can be. For the smallest possible biggest "
        "value, make the others as big as they can be.", show(b_y5, 'So for the biggest possible'),
        show(b_y6, 'For the smallest possible biggest'))),
    S('Letters: plug in equal values',
      L("Now letters. The average of a, b and c is eight. What's the average of a plus five, b plus five, and c plus five?",
        show(b_p0, 'The average of a, b and c'), show(b_p1, "What's the average of a plus five")),
      L("There's a quick way to plug in numbers. Nothing says the letters are different. So let's make every letter equal "
        "to the average, eight. Then their average is eight, as given.", show(b_p2, 'make every letter equal')),
      L("Each new value is eight plus five, thirteen. All three are thirteen, so their average is thirteen.",
        show(b_p3, 'eight plus five'), show(b_p4, 'so their average is thirteen')),
      L("It agrees with the last lesson. Every value grew by five, so the average grew by five."),
      L("Two warnings. If the question says the numbers are different, we can't make them equal. And if two choices give "
        "the same result, we try other numbers.", show(b_p5, 'If the question says the numbers are different'),
        show(b_p6, 'if two choices give the same result'))),
    S('An average equal to a letter',
      L("Sometimes the average is equal to one of the letters. We do the same thing, we write the sum."),
      L("The average of x, y and z is x. So the sum is three times x. x plus y plus z is equal to three x.",
        show(b_q0, 'The average of x, y and z is x'), show(b_q1, 'x plus y plus z is equal')),
      L("We take x away from both sides. So y plus z is equal to two x.", show(b_q2, 'So y plus z is equal')),
      L("Two numbers with a sum of two x have an average of x. So y and z also have an average of x.",
        show(b_q3, 'So y and z also')),
      L("One more. The average of m and n is equal to their difference, m minus n. Then the sum is two times the "
        "difference.", show(b_q4, 'The average of m and n'), show(b_q5, 'Then the sum is two times')),
      L("Careful, two times the whole difference. That's two m minus two n.", show(b_q6, "That's two m minus two n")),
      L("We add two n to both sides, and take m away from both sides. So three n is equal to m.", show(b_q7, 'So three n is equal')),
      L("Let's check with numbers. n is two, so m is six. Their sum is eight, and the average is four. The difference is "
        "six minus two, also four.", show(b_q8, 'so m is six'), show(b_q9, 'and the average is four'),
        show(b_q10, 'The difference is six minus two'))),
    S('The balance with more and less',
      L("The balance also works with more than and less than. The average of a, b and c is more than six. The average of "
        "a, b, c and d is less than six. What must be true?", show(b_r0, 'The average of a, b and c is more'),
        show(b_r1, 'The average of a, b, c and d')),
      L("Think of six as a line. a, b and c are above the line on average. So together they have something extra above "
        "six."),
      L("But all four together are below the line. So someone pulls them down, by more than that extra. Only d is left. So "
        "d must be less than six."),
      L("Let's check with sums. a plus b plus c is more than three times six, eighteen.", show(b_r2, 'more than three times six')),
      L("And all four add up to less than four times six, twenty-four.", show(b_r3, 'less than four times six')),
      L("So d is less than twenty-four minus eighteen, six.", show(b_r4, 'So d is less than')),
      L("What about a alone? It can be below six. For example, a is two, b is nine, and c is ten. Their sum is twenty-one, "
        "and twenty-one divided by three is seven. That's more than six, so it fits.", show(b_r6, 'It can be below six'),
        show(b_r5, 'a is two, b is nine')),
      L("So a doesn't have to be above six. Only d is sure. When they ask what must be true, test the other letters with "
        "numbers.", show(b_r7, 'When they ask what must be true'))),
    S('Summary',
      L("Let's sum up. The sum is equal to how many numbers there are, times the average.", show(b_z1, 'The sum is equal to how many')),
      L("When a number joins or leaves, compare it to the average of the group it is in.", show(b_z2, 'When a number joins')),
      L("For the biggest possible value, make the others as small as they can be.", show(b_z3, 'For the biggest possible')),
      L("And with letters, plug in equal values, or write the sum.", show(b_z4, 'And with letters')),
      L("Take a moment to memorize this. Now let's use it in the questions. I'll see you in the next video.")),
])
SPLITS.append(('wp-081', 'Sum from the Average', [
    (1, None),
    (5, "Let's continue, and find the biggest and the smallest possible values."),
    (8, "Let's continue, and work with letters.")]))


# ------------------------------------------------------------------------------------------------ wp25-g082 (Hebrew: the gifted class, 8 x 6)
# Hebrew (wp 5289-5324): 8 students solve 6 puzzles on average -> treat each one as the average: 48 together ("we don't
# know what each one solves, but together surely 48"); one student can't solve 49. One method. English: 12 volunteers x
# 7 bags. REMINDER: sum = how many x the average (wp-081). The Hebrew "one alone can't be more than all" kept as a line.
g82a = I('g82a', '$12$ volunteers, $\\ $average $7$ bags', size=30)
g82b = I('g82b', 'the sum $=$ how many $\\times$ the average', size=30)
g82c = IH('g82c', '$12\\times7$', size=30)
g82d = IH('g82d', '$10\\times7=70$', size=30, col=1)
g82e = IH('g82e', '$2\\times7=14$', size=30, col=1)
g82f = IH('g82f', '$70+14=84$', size=30, col=1)
video('solve-wp25-g082', 'solution', qid='wp25-g082', slides=[
    S('Method 1 · The math way: the sum',
      L("Twelve volunteers clean a beach. On average, each volunteer fills seven bags of litter. How many bags do they fill "
        "altogether?", pt('stem', 'Twelve volunteers clean a beach', 'hl', 6.0), voice='calm', pause=0.5),
      L("So they ask for the total number of bags. We know how many volunteers there are, and their average. That's "
        "exactly the move from the lesson.", pt('stem', 'So they ask for the total')),
      L("Let's do it the math way. We don't know how many bags each volunteer filled. And we don't need to.",
        show(g82a, "Let's do it the math way")),
      L("Like in the lesson, we treat every volunteer as if they filled exactly the average, seven bags."),
      L("The sum is how many, times the average. So it's twelve times seven.", show(g82b, 'The sum is how many'),
        show(g82c, 'twelve times seven')),
      L("Ten times seven is seventy. And two times seven is fourteen. Seventy plus fourteen is eighty-four.",
        show(g82d, 'Ten times seven'), show(g82e, 'two times seven'), show(g82f, 'Seventy plus fourteen')),
      L("Maybe one volunteer filled twenty bags, and another only two. It doesn't matter. Together they still fill "
        "eighty-four bags."),
      L("Choice number one is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp25-g083 (Hebrew: Dani and Sarit, Q4)
# Hebrew (wp 5329-5386): the formula ((Dani + Sarit) / 2 = 168, x2, -171) and then "the first definition, the average as a
# balance point": Dani 3 above, so Sarit 3 below, "faster and easier". Both methods kept, in her order. REMINDERS: the
# formula (wp-080), the two-number balance (wp-080 part 2). Trap at the step: 182 = the average + 18.
g83f = IH('g83f', '$\\frac{169+C}{2}=164$', size=30)
g83a = IH('g83a', '$164\\times2=328$', size=30)
g83b = IH('g83b', '$169+C=328$', size=30)
g83c = IH('g83c', '$328-170=158$', size=30, col=1)
g83d = IH('g83d', '$158+1=159$', size=30, col=1)
g83e = IH('g83e', '$159+20=179$', size=30, col=1)
g83g = IH('g83g', '$179-2=177$', size=30, col=1)
g83h = IH('g83h', '$164+18=182$: $\\ $the trap', size=30, col=1)
g83z = OWN(ZL('g83z', 155, 173, [('e', [('ink', 169, 'Ethan'), ('arrow', 164, 169, '5'), ('below', 169, '169')]),
                                 ('c', [('arrow', 164, 159, '5'), ('pt', 159, 'Chloe'), ('below', 159, '159')])],
              ticks=((164, '164'),), w=560, title='Ethan, Chloe and their average 164'), 'g83z')
g83i = IH('g83i', '$169-164=5$', size=30, col=1)
g83j = IH('g83j', '$164-5=159$', size=30, col=1)
g83k = IH('g83k', '$159+18=177$', size=30, col=1)
video('solve-wp25-g083', 'solution', qid='wp25-g083', slides=[
    S('Method 1 · The math way: the formula',
      L("Ethan is a hundred sixty-nine centimeters tall. The average height of Ethan and Chloe is a hundred sixty-four "
        "centimeters. Ryan is eighteen centimeters taller than Chloe. How tall is Ryan?",
        pt('stem', 'Ethan is a hundred sixty-nine', 'hl', 9.0), voice='calm', pause=0.5),
      L("So they ask for Ryan's height. Ryan is compared to Chloe, so first we need Chloe. We'll solve it in two "
        "different ways, the math way with the formula, and then by understanding, with the balance.",
        pt('stem', "So they ask for Ryan's height")),
      L("Let's start with the math way. Let's call Chloe's height C. The average of Ethan and Chloe is their sum, divided "
        "by two. And it's equal to a hundred sixty-four.", show(g83f, 'divided by two')),
      L("To get rid of the two, we multiply both sides by two. A hundred sixty-four times two is three hundred twenty-eight.",
        show(g83a, 'A hundred sixty-four times two'), show(g83b, 'three hundred twenty-eight')),
      L("Now we take a hundred sixty-nine away from both sides. Three hundred twenty-eight minus a hundred seventy is a "
        "hundred fifty-eight.", show(g83c, 'Three hundred twenty-eight minus')),
      L("But we took away one too many, so we add it back. A hundred fifty-eight plus one is a hundred fifty-nine.",
        show(g83d, 'A hundred fifty-eight plus one')),
      L("So Chloe is a hundred fifty-nine centimeters tall. And Ryan is eighteen centimeters taller than Chloe.",
        pt('stem', 'And Ryan is eighteen')),
      L("A hundred fifty-nine plus twenty is a hundred seventy-nine. Then we take away two, and get a hundred "
        "seventy-seven.", show(g83e, 'A hundred fifty-nine plus twenty'), show(g83g, 'Then we take away two')),
      L("Careful, the eighteen goes on Chloe, not on the average. A hundred sixty-four plus eighteen is a hundred "
        "eighty-two, choice number one. That's the trap.", show(g83h, 'A hundred sixty-four plus eighteen'),
        mk('cross', 'choice 1', "That's the trap")),
      L("So Ryan is a hundred seventy-seven centimeters tall. That's choice number four.")),
    S('Method 2 · Understanding: the balance',
      L("[pause] Now by understanding, with the balance. We start again from the givens. Like in the lesson, the average "
        "of two numbers is exactly in the middle between them.", show(g83z['line'], 'exactly in the middle')),
      L("Ethan is a hundred sixty-nine. A hundred sixty-nine minus a hundred sixty-four is five. So Ethan is five above "
        "the average.", show(g83z['e'], 'Ethan is a hundred sixty-nine'), show(g83i, 'A hundred sixty-nine minus')),
      L("So Chloe must be five below the average, on the other side. A hundred sixty-four minus five is a hundred "
        "fifty-nine.", show(g83z['c'], 'So Chloe must be five below'), show(g83j, 'A hundred sixty-four minus five')),
      L("That's the same Chloe, with almost no calculation. Ryan is eighteen centimeters more. A hundred fifty-nine plus "
        "eighteen is a hundred seventy-seven.", show(g83k, 'A hundred fifty-nine plus eighteen')),
      L("Choice number four is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t25-02 (English: Dana's fifth test)
# No Hebrew (a September addition, real exam 2024_spring_q1_07). The sum (wp-081) and the balance (wp-080, its first use
# in a question: applied slowly, "like in the lesson"). Trap at the step: 87 = 85 + 2.
q2a = IH('q2a', '$5\\times85$', size=30)
q2b = IH('q2b', '$5\\times80=400$', size=30)
q2c = IH('q2c', '$5\\times5=25$', size=30)
q2d = IH('q2d', '$400+25=425$', size=30)
q2e = IH('q2e', '$78+85=163$', size=30, col=1)
q2f = IH('q2f', '$91+88=179$', size=30, col=1)
q2g = IH('q2g', '$163+179=342$', size=30, col=1)
q2h = IH('q2h', '$425-340=85$', size=30, col=1)
q2i = IH('q2i', '$85-2=83$', size=30, col=1)
q2t = TBL('q2t', ['78', '85', '91', '88', '?'], ['vs. 85'], [
    ('d1', [('c', 0, 0, '−7'), ('c', 0, 1, '0')]), ('d2', [('c', 0, 2, '+6'), ('c', 0, 3, '+3')]), ('d3', [('c', 0, 4, '−2', _TEAL)])],
    colw=96, labw=130, rowh=64, w=560)
q2j = IH('q2j', '$-7+6=-1$', size=30, col=1)
q2k = IH('q2k', '$-1+3=2$', size=30, col=1)
q2l = IH('q2l', '$85-2=83$', size=30, col=1)
q2m = IH('q2m', '$85+2=87$: $\\ $the trap', size=30, col=1)
video('solve-q-r26-t25-02', 'solution', qid='q-r26-t25-02', slides=[
    S('Method 1 · The math way: the sum',
      L("Dana took five tests. Her scores on four of them were seventy-eight, eighty-five, ninety-one and eighty-eight. The "
        "average of all five scores is eighty-five. What was her score on the fifth test?",
        pt('stem', 'Dana took five tests', 'hl', 9.0), voice='calm', pause=0.5),
      L("So they ask for the fifth score. We know four scores, and the average of all five. We'll solve it in two "
        "different ways, the math way with the sum, and then by understanding, with the balance.",
        pt('stem', 'So they ask for the fifth score')),
      L("Let's start with the math way. Like in the lesson, the sum is how many times the average. That's five scores "
        "times eighty-five.", show(q2a, 'five scores times eighty-five')),
      L("Five times eighty is four hundred. Five times five is twenty-five. So all five scores add up to four hundred "
        "twenty-five.", show(q2b, 'Five times eighty'), show(q2c, 'Five times five'), show(q2d, 'So all five scores add up')),
      L("Now the four scores we know. Seventy-eight plus eighty-five is a hundred sixty-three.", show(q2e, 'Seventy-eight plus eighty-five')),
      L("Ninety-one plus eighty-eight is a hundred seventy-nine.", show(q2f, 'Ninety-one plus eighty-eight')),
      L("A hundred sixty-three plus a hundred seventy-nine is three hundred forty-two.", show(q2g, 'A hundred sixty-three plus')),
      L("The fifth score is what's left. Four hundred twenty-five minus three hundred forty is eighty-five. Then we take "
        "away two more, and get eighty-three.", show(q2h, 'Four hundred twenty-five minus'), show(q2i, 'Then we take away two more')),
      L("So the fifth score is eighty-three. That's choice number two.")),
    S('Method 2 · Understanding: the balance',
      L("[pause] Now by understanding, with the balance. We start again from the givens. Like in the lesson, the "
        "differences from the average add up to zero. So we compare each score to eighty-five.",
        show(q2t['line'], 'So we compare each score')),
      L("Seventy-eight is seven below, so minus seven. Eighty-five is the average itself, so zero.",
        show(q2t['d1'], 'Seventy-eight is seven below')),
      L("Ninety-one is six above, plus six. Eighty-eight is three above, plus three.", show(q2t['d2'], 'Ninety-one is six above')),
      L("Together, minus seven plus six is minus one. Minus one plus three is plus two.", show(q2j, 'minus seven plus six'),
        show(q2k, 'Minus one plus three')),
      L("So the four scores are two points above the average, together. The fifth score must balance them. So it's two "
        "points below eighty-five."),
      L("Eighty-five minus two is eighty-three. The same answer, with small numbers.", show(q2l, 'Eighty-five minus two'),
        show(q2t['d3'], 'The same answer')),
      L("Careful with eighty-seven, choice number four. That's eighty-five plus two. It adds the two instead of balancing "
        "it.", show(q2m, "That's eighty-five plus two"), mk('cross', 'choice 4', 'It adds the two')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t25-01 (English: a new student joins)
# No Hebrew (a September addition, real exams 2026_spring_q2_15, 2020_winter_q2_20). A number joins (wp-081: compare it to
# the new average) and the before / after table of sums. Trap at the step: 8 = after.
q1a = IH('q1a', '$94-73=21$ $\\ $above', size=30, col=1)
q1b = IH('q1b', '$73-70=3$ $\\ $below, each', size=30, col=1)
q1c = IH('q1c', '$21\\div3=7$', size=30, col=1)
q1d = I('q1d', '$8$ $=$ after the new student: $\\ $the trap', size=28, col=1)
q1t = TBL('q1t', ['students', 'average', 'sum'], ['before', 'after'], [
    ('r1', [('c', 0, 0, 'n'), ('c', 0, 1, '70'), ('c', 0, 2, '70n')]),
    ('r2', [('c', 1, 0, 'n+1'), ('c', 1, 1, '73'), ('c', 1, 2, '73(n+1)')])], colw=170, labw=130, rowh=64, w=560)
q1e = IH('q1e', '$70n+94=73(n+1)$', size=30)
q1f = IH('q1f', '$70n+94=73n+73$', size=30)
q1g = IH('q1g', '$94-73=21$', size=30, col=1)
q1h = IH('q1h', '$21=3n$', size=30, col=1)
q1i = IH('q1i', '$n=7$', size=30, col=1)
video('solve-q-r26-t25-01', 'solution', qid='q-r26-t25-01', slides=[
    S('Method 1 · Understanding: the balance',
      L("The average score of the students in a class was seventy. A new student with a score of ninety-four joined the "
        "class, and the class average rose to seventy-three. How many students were in the class before the new student "
        "joined?", pt('stem', 'The average score of the students', 'hl', 10.0), voice='calm', pause=0.5),
      L("So they give two averages and the new student's score. They ask how many students there were before the new "
        "student came.", pt('stem', 'So they give two averages')),
      L("We'll solve it in two different ways. First by understanding, with the balance from the lesson, and then the "
        "math way, with an equation."),
      L("Like in the lesson, a new score joins, so we compare it to the new average. Ninety-four minus seventy-three is "
        "twenty-one. So the new student is twenty-one points above the new average.", show(q1a, 'Ninety-four minus seventy-three')),
      L("The old students had an average of seventy, so each one counts as seventy. Seventy-three minus seventy is three. "
        "So each old student is three below the new average.", show(q1b, 'Seventy-three minus seventy')),
      L("The twenty-one above must balance the old students below. Each one is three below. Twenty-one divided by three "
        "is seven.", show(q1c, 'Twenty-one divided by three')),
      L("So there were seven students before the new student joined."),
      L("Careful with eight, choice number three. Eight is the number of students after the new student joined. They ask "
        "about before.", show(q1d, 'Eight is the number of students after'), mk('cross', 'choice 3', 'They ask about before')),
      L("So seven students, choice number two.")),
    S('Method 2 · The math way: an equation',
      L("[pause] Now the math way. We start again from the givens. Let's call the number of students before n, and make a "
        "table, before and after.", show(q1t['line'], 'and make a table')),
      L("Before, there were n students with an average of seventy. So the sum is seventy n.", show(q1t['r1'], 'So the sum is seventy n')),
      L("After, there's one more student, so n plus one students, with an average of seventy-three. So the sum is "
        "seventy-three times the bracket, n plus one.", show(q1t['r2'], 'So the sum is seventy-three times')),
      L("The new student changes the sum, and also how many students there are. The old sum plus ninety-four is the new "
        "sum.", show(q1e, 'The old sum plus ninety-four')),
      L("We open the brackets. Seventy-three times the bracket, n plus one is seventy-three n plus seventy-three.",
        show(q1f, 'We open the brackets')),
      L("Now we take seventy n and seventy-three away from both sides. Ninety-four minus seventy-three is twenty-one. And "
        "seventy-three n minus seventy n is three n.", show(q1g, 'Ninety-four minus seventy-three'), show(q1h, 'is three n')),
      L("We divide both sides by three. Twenty-one divided by three is seven, so n is seven.", show(q1i, 'so n is seven')),
      L("Seven students before, the same answer. Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t25-03 (English: the biggest of six)
# No Hebrew (real exams 2025_spring_q1_05, 2024_winter_q1_17). The biggest possible value (wp-081 part 2: the others as
# small as they can be; positive / whole / different). Traps at the step: 49 (five ones), 54 (zeros).
q3a = IH('q3a', '$6\\times9=54$', size=30)
q3b = IH('q3b', 'the others: $\\ 1,\\ 2,\\ 3,\\ 4,\\ 5$', size=30)
q3c = IH('q3c', '$1+2+3+4+5=15$', size=30)
q3d = IH('q3d', '$54-15=39$', size=30)
q3e = IH('q3e', '$1, 2, 3, 4, 5, 39$', size=30, col=1)
q3e2 = IH('q3e2', '$54\\div6=9$', size=30, col=1)
q3f = IH('q3f', '$54-5=49$: $\\ $five ones, no', size=30, col=1)
q3g = IH('q3g', '$54$: $\\ $five zeros, no', size=30, col=1)
video('solve-q-r26-t25-03', 'solution', qid='q-r26-t25-03', slides=[
    S('Method 1 · The math way: the others smallest',
      L("Six different positive integers have an average of nine. What is the largest possible value of one of them?",
        pt('stem', 'Six different positive integers', 'hl', 5.0), voice='calm', pause=0.5),
      L("So they ask for the biggest value that one of the six numbers can have. And look at the words. Different, "
        "positive, and integers, which means whole numbers. Each one matters here.", pt('stem', 'So they ask for the biggest')),
      L("Let's do it the math way, like in the lesson. First the sum. Six numbers with an average of nine. Six times nine "
        "is fifty-four.", show(q3a, 'Six times nine')),
      L("To make one number as big as it can be, we make the other five as small as they can be."),
      L("They must be positive whole numbers, and different. So the five smallest are one, two, three, four and five.",
        show(q3b, 'So the five smallest are')),
      L("One plus two plus three plus four plus five is fifteen.", show(q3c, 'One plus two plus three')),
      L("So the big one gets the rest. Fifty-four minus fifteen is thirty-nine.", show(q3d, 'Fifty-four minus fifteen')),
      L("Let's check. One, two, three, four, five and thirty-nine are six different positive whole numbers. Their sum is "
        "fifty-four, and fifty-four divided by six is nine.", show(q3e, "Let's check"), show(q3e2, 'fifty-four divided by six')),
      L("Careful with forty-nine, choice number three. That's fifty-four minus five, as if the others were five ones. But "
        "the numbers must be different, so we can't use five ones.", show(q3f, "That's fifty-four minus five"),
        mk('cross', 'choice 3', "so we can't use five ones")),
      L("And fifty-four, choice number four, needs the other five to be zero. But zero isn't positive.",
        show(q3g, 'And fifty-four, choice number four'), mk('cross', 'choice 4', "But zero isn't positive")),
      L("Choice number one is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t25-04 (English: nine even numbers in a row)
# No Hebrew (real exam 2024_winter_q2_07). Evenly spaced -> the middle number (wp-080, part 1). "Consecutive even
# numbers" is NEW here (topic 16 comes later): explained with an example. Traps at the step: 34 (steps of one), 39 (odd).
q4a = IH('q4a', 'like $12,\\ 14,\\ 16$: $\\ +2$ each', size=30)
q4t = TBL('q4t', ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th'], [''], [
    ('m', [('c', 0, 4, '30', _TEAL)]), ('u', [('c', 0, 5, '32'), ('c', 0, 6, '34'), ('c', 0, 7, '36'), ('c', 0, 8, '38')]),
    ('b', [('box', 0, 8)])], colw=84, rowh=64, size=30, w=780)
q4b = IH('q4b', '$30+4=34$: $\\ $steps of $1$, no', size=30)
q4c = IH('q4c', '$39$ is odd, no', size=30)
q4d = IH('q4d', 'smallest: $\\ x$', size=30)
q4e = IH('q4e', '$8\\times2=16$', size=30)
q4f = IH('q4f', 'biggest: $\\ x+16$', size=30)
q4g = IH('q4g', '$\\frac{x+x+16}{2}=30$', size=30, col=1)
q4h = IH('q4h', '$2x+16=60$', size=30, col=1)
q4i = IH('q4i', '$2x=44$', size=30, col=1)
q4j = IH('q4j', '$x=22$', size=30, col=1)
q4k = IH('q4k', '$22+16=38$', size=30, col=1)
video('solve-q-r26-t25-04', 'solution', qid='q-r26-t25-04', slides=[
    S('Method 1 · Understanding: the middle number',
      L("The average of nine consecutive even numbers is thirty. What is the largest of them?",
        pt('stem', 'The average of nine consecutive', 'hl', 5.0), voice='calm', pause=0.5),
      L("So they ask for the biggest of the nine numbers. First, what are consecutive even numbers? They're even numbers "
        "in a row, like twelve, fourteen and sixteen. Each one is two more than the one before.",
        pt('stem', 'So they ask for the biggest'), show(q4a, 'like twelve, fourteen')),
      L("We'll solve it in two different ways, by understanding with the middle number, and then the math way."),
      L("Let's start by understanding. Each number is two more than the one before, so the numbers are evenly spaced. "
        "Like in the lesson, the average is the middle number.", show(q4t['line'], 'so the numbers are evenly spaced')),
      L("There are nine numbers. The middle one is the fifth, with four numbers before it and four after it. So the fifth "
        "number is thirty.", show(q4t['m'], 'So the fifth number is thirty')),
      L("Now we go up four numbers, two each time. Thirty-two, thirty-four, thirty-six, thirty-eight.",
        show(q4t['u'], 'Thirty-two, thirty-four')),
      L("So the biggest is thirty-eight.", show(q4t['b'], 'So the biggest is thirty-eight')),
      L("Careful with thirty-four, choice number one. That's thirty plus four, as if each step were one. But each step is "
        "two, because the numbers are even.", show(q4b, "That's thirty plus four"), mk('cross', 'choice 1', 'But each step is two')),
      L("And thirty-nine, choice number three, is odd. So it can't even be one of the numbers.", show(q4c, 'is odd'),
        mk('cross', 'choice 3', "So it can't even be one")),
      L("So the biggest is thirty-eight, choice number two.")),
    S('Method 2 · The math way: the first and the last',
      L("[pause] Now the math way. We start again from the givens. Let's call the smallest number x.", show(q4d, "Let's call the smallest")),
      L("Each step is two, and there are eight steps from the first number to the ninth. Eight times two is sixteen. So "
        "the biggest is x plus sixteen.", show(q4e, 'Eight times two'), show(q4f, 'So the biggest is x plus sixteen')),
      L("Like in the lesson, for evenly spaced numbers the average is the first plus the last, divided by two. So x plus x "
        "plus sixteen, divided by two, is thirty.", show(q4g, 'So x plus x')),
      L("We multiply both sides by two. Thirty times two is sixty. So two x plus sixteen is sixty.", show(q4h, 'So two x plus sixteen')),
      L("We take sixteen away from both sides. Sixty minus sixteen is forty-four. So two x is forty-four, and x is "
        "twenty-two.", show(q4i, 'So two x is forty-four'), show(q4j, 'and x is twenty-two')),
      L("But x is the smallest number, and they ask for the biggest. Twenty-two plus sixteen is thirty-eight.",
        show(q4k, 'Twenty-two plus sixteen')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t25-05 (English: 3a + 2)
# No Hebrew (real exams 2025_autumn_q2_15, 2022_winter_q1_08). Every value changes the same way (wp-080 part 3) and
# plugging in equal values (wp-081 part 2). Traps at the step: 60, 66 (the wrong order), 22.
q5a = IH('q5a', '$20\\times3=60$', size=30, col=1)
q5b = IH('q5b', '$60+2=62$', size=30, col=1)
q5c = IH('q5c', '$(20+2)\\times3=66$: $\\ $wrong order', size=30, col=1)
q5d = IH('q5d', '$a=b=c=20$', size=30, col=1)
q5e = IH('q5e', '$3\\times20=60$', size=30, col=1)
q5f = IH('q5f', '$60+2=62$', size=30, col=1)
video('solve-q-r26-t25-05', 'solution', qid='q-r26-t25-05', slides=[
    S('Method 1 · Understanding: every value changes',
      L("The average of a, b and c is twenty. What is the average of three a plus two, three b plus two, and three c plus "
        "two?", pt('stem', 'The average of a, b and c', 'hl', 6.0), voice='calm', pause=0.5),
      L("So we know the average of a, b and c. They ask for the average of three new values. Each new value is three times "
        "the letter, plus two.", pt('stem', 'They ask for the average of three new')),
      L("We'll solve it in two different ways, by understanding, and then by plugging in numbers."),
      L("Let's start by understanding. Every value changes in the same way. Like in the lesson, the average changes in the "
        "same way, and in the same order."),
      L("First, every value is multiplied by three. So the average is multiplied by three. Twenty times three is sixty.",
        show(q5a, 'Twenty times three')),
      L("Then two is added to every value. So two is added to the average. Sixty plus two is sixty-two.",
        show(q5b, 'Sixty plus two')),
      L("Careful with sixty, choice number one. It forgets the plus two.", mk('cross', 'choice 1', 'It forgets the plus two')),
      L("And sixty-six, choice number three, comes from the wrong order. Twenty plus two is twenty-two, and twenty-two "
        "times three is sixty-six. It adds the two before it multiplies.", show(q5c, 'and twenty-two times three'),
        mk('cross', 'choice 3', 'It adds the two before')),
      L("And twenty-two, choice number four, forgets the times three.", mk('cross', 'choice 4', 'forgets the times three')),
      L("So the new average is sixty-two, choice number two.")),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. Like in the lesson, nothing says the letters "
        "are different. So let's make all three equal to the average, twenty.", show(q5d, 'equal to the average, twenty')),
      L("Then the average of a, b and c is twenty, just as the question says."),
      L("Each new value is three times twenty, plus two. Three times twenty is sixty. And sixty plus two is sixty-two.",
        show(q5e, 'Three times twenty is sixty'), show(q5f, 'sixty plus two is sixty-two')),
      L("All three new values are sixty-two, so their average is sixty-two."),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# ------------------------------------------------------------------------------------------------ wp25-g084 (Hebrew: the pair averages, Q17)
# Hebrew (wp 5389-5493): three numbers x, y, z and their three pairs: the formula (same denominator, collect, take out 2:
# x + y + z = 3 times the average) and then plugging in numbers (all 1: "not written they're different"; rule out three
# choices, "I still don't mark it"; "a hard question turned into a warm-up"). English (September): four numbers, six
# pairs, 6 times the average. Both methods kept, in her order. REMINDERS: the formula, sum = how many x average,
# plugging in equal values (wp-081), rule out three choices (topic 51).
g84a = I('g84a', '$p,\\ q,\\ r,\\ s$', size=32)
g84b = I('g84b', 'pairs: $\\ (p,q),\\ (p,r),\\ (p,s),\\ (q,r),\\ (q,s),\\ (r,s)$', size=28)
g84c = IH('g84c', 'each pair: $\\ \\frac{p+q}{2}$', size=30)
g84d = IH('g84d', '$p$: $\\ $in $3$ pairs', size=30, col=1)
g84e = IH('g84e', 'sum $=\\frac{3(p+q+r+s)}{2}$', size=30, col=1)
g84f = IH('g84f', '$p+q+r+s=4A$', size=32)
g84g = IH('g84g', '$\\frac{3\\times4A}{2}=\\frac{12A}{2}$', size=32)
g84h = IH('g84h', '$=6A$', size=32)
g84i = IH('g84i', '$p=q=r=s=1$', size=30)
g84j = IH('g84j', 'each pair: $\\ 1$', size=30)
g84k = IH('g84k', 'six pairs: $\\ 1\\times6=6$', size=30, col=1)
g84l = IH('g84l', 'the average: $\\ 1$', size=30, col=1)
g84m = IH('g84m', '(1) $4\\times1=4$, $\\ $no', size=30, col=1)
g84n = IH('g84n', '(2) $2\\times1=2$, $\\ $no', size=30, col=1)
g84o = IH('g84o', '(3) $6\\times1=6$', size=30, col=1)
g84p = IH('g84p', '(4) $3\\times1=3$, $\\ $no', size=30, col=1)
video('solve-wp25-g084', 'solution', qid='wp25-g084', slides=[
    S('Method 1 · The math way: the formula',
      L("Four numbers are given. Take the average of each of the six different pairs, then add those six averages. The "
        "result equals which of the following?", pt('stem', 'Four numbers are given', 'hl', 8.0), voice='calm', pause=0.5),
      L("So we take every pair of the four numbers, find its average, and add the six averages. They ask how the result "
        "compares to the average of all four numbers.", pt('stem', 'So we take every pair')),
      L("This is a hard question near the end of the section. We'll solve it in two different ways, the math way, and "
        "then by plugging in numbers, which makes it a quick question."),
      L("Let's start with the math way. Let's call the four numbers p, q, r and s.", show(g84a, "Let's call the four numbers")),
      L("The six pairs are p and q, p and r, p and s, q and r, q and s, and r and s.", show(g84b, 'The six pairs are')),
      L("The average of each pair is the two numbers, divided by two. For example, p plus q, divided by two.",
        show(g84c, 'For example, p plus q')),
      L("All six averages have the same denominator, two. So to add them, we just add the tops."),
      L("How many times does p appear? In three pairs, with q, with r and with s. The same is true for every number.",
        show(g84d, 'In three pairs')),
      L("So the tops add up to three times the bracket, p plus q plus r plus s. And it's all divided by two.", show(g84e, 'So the tops add up'))),
    S('Method 1 · The math way: the formula',
      L("Now the average of the four numbers. Let's call it A. Like in the lesson, the sum is how many times the average. "
        "So p plus q plus r plus s is four A.", show(g84f, 'So p plus q plus r plus s is four A')),
      L("So the six averages add up to three times four A, divided by two. Three times four is twelve. Twelve A divided by "
        "two is six A.", show(g84g, 'Three times four is twelve'), show(g84h, 'Twelve A divided by two')),
      L("So the result is six times the average of the four numbers. That's choice number three.")),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the question. Nothing says the four numbers are "
        "different. So, like in the lesson, let's make all four equal to one.", show(g84i, 'make all four equal to one')),
      L("Every pair is one and one, so the average of every pair is one.", show(g84j, 'so the average of every pair')),
      L("There are six pairs, so the six averages add up to one times six, six.", show(g84k, 'one times six')),
      L("And the average of the four numbers is one too.", show(g84l, 'And the average of the four numbers'))),
    S('Method 2 · Plugging in numbers',
      L("Now let's check the choices. We need to rule out three. Choice number one says four times the average. Four times "
        "one is four, not six. So it's out.", show(g84m, 'Choice number one says'), mk('cross', 'choice 1', "So it's out")),
      L("Choice number two says two times the average. Two times one is two, not six. Out.", show(g84n, 'Choice number two says'),
        mk('cross', 'choice 2', 'not six. Out')),
      L("Choice number three says six times the average. Six times one is six. It fits, but when we plug in numbers, we "
        "don't stop at the first match.", show(g84o, 'Choice number three says')),
      L("Choice number four says three times the average. Three times one is three, not six. Out.",
        show(g84p, 'Choice number four says'), mk('cross', 'choice 4', 'Three times one is three')),
      L("Three choices are out, so choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'so choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp25-g085 (Hebrew: Guy and Ruti, Q19)
# Hebrew (wp 5496-5611): "a question with a lot of words": a table (two people, two tests), G and G + 3, two more
# unknowns, the averages formula, x2, G cancels -> 11; then plugging in numbers (80, and 80 again "the easiest, then the
# average is 80"), Ruti's average 76, and the balance point (83 is 7 above, so 69) -> 11. Both methods kept, in her
# order. English (September): Omar and Lena, 6 and 5 -> 16. REMINDERS: the formula, the two-number balance, plugging in.
# Trap at the step: 11 = 6 + 5.
g85t = TBL('g85t', ['geography', 'music', 'average'], ['Omar', 'Lena'], [
    ('g', [('c', 0, 0, 'g'), ('c', 1, 0, 'g+6')]), ('m', [('c', 0, 1, 'm'), ('c', 1, 1, 'L')]),
    ('a', [('c', 0, 2, '(g+m)÷2', None), ('c', 1, 2, '(g+6+L)÷2')])], colw=170, labw=120, rowh=62, size=28, w=560)
g85a = IH('g85a', '$\\frac{g+m}{2}=\\frac{g+6+L}{2}+5$', size=30, col=1)
g85b = IH('g85b', '$g+m=g+6+L+10$', size=30, col=1)
g85c = IH('g85c', '$m=L+16$', size=30, col=1)
g85d = IH('g85d', '$6+5=11$: $\\ $the trap', size=30, col=1)
g85u = TBL('g85u', ['geography', 'music', 'average'], ['Omar', 'Lena'], [
    ('g', [('c', 0, 0, '70'), ('c', 1, 0, '76')]), ('m', [('c', 0, 1, '70'), ('c', 0, 2, '70')]),
    ('a', [('c', 1, 2, '65')]), ('l', [('c', 1, 1, '54', _TEAL)])], colw=170, labw=120, rowh=62, size=30, w=560)
g85e = IH('g85e', '$70-5=65$', size=30, col=1)
g85f = IH('g85f', '$76-65=11$', size=30, col=1)
g85g = IH('g85g', '$65-11=54$', size=30, col=1)
g85h = IH('g85h', '$70-54=16$', size=30, col=1)
video('solve-wp25-g085', 'solution', qid='wp25-g085', slides=[
    S('Method 1 · The math way: a table',
      L("Omar and Lena take two tests, geography and music. Lena's geography score is six points higher than Omar's. "
        "Omar's two-test average is five points higher than Lena's. How much higher is Omar's music score than Lena's?",
        pt('stem', 'Omar and Lena take two tests', 'hl', 11.0), voice='calm', pause=0.5),
      L("So they compare Omar's music score with Lena's music score. That's a lot of words, so let's put them in order "
        "with a table.", pt('stem', "So they compare Omar's music score")),
      L("We'll solve it in two different ways, the math way with a table, and then by plugging in numbers."),
      L("Let's start with the math way. Two people and two tests. So we make a row for each person, a column for each "
        "test, and a column for the average.", show(g85t['line'], 'So we make a row for each person')),
      L("Omar's geography score isn't given, so let's call it g. Lena's geography score is six points higher, so it's g "
        "plus six.", show(g85t['g'], "so let's call it g")),
      L("The music scores aren't given either. Let's call Omar's m, and Lena's L.", show(g85t['m'], "Let's call Omar's m")),
      L("Each average is the sum of the two tests, divided by two.", show(g85t['a'], 'Each average is the sum')),
      L("Omar's average is five more than Lena's. So g plus m over two is equal to g plus six plus L over two, plus five.",
        show(g85a, 'So g plus m over two')),
      L("We multiply both sides by two, to get rid of the twos. Five times two is ten.", show(g85b, 'Five times two is ten')),
      L("Now g is on both sides, so we take it away. And six plus ten is sixteen. So m is equal to L plus sixteen.",
        show(g85c, 'So m is equal to L plus sixteen')),
      L("So Omar's music score is sixteen points higher than Lena's. That's choice number two."),
      L("Careful with eleven, choice number one. That's six plus five. But a lead of five points in the average is a lead "
        "of ten points in the sum, because there are two tests.", show(g85d, "That's six plus five"),
        mk('cross', 'choice 1', 'because there are two tests'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens, with the same table.",
        show(g85u['line'], 'with the same table')),
      L("Omar's geography score isn't given, so let's pick a round number, seventy. Lena's is six points higher, "
        "seventy-six.", show(g85u['g'], "so let's pick a round number")),
      L("Omar's music score isn't given either. Let's pick seventy again. Why? Because then his average is simply seventy, "
        "with no calculation.", show(g85u['m'], "Let's pick seventy again")),
      L("Omar's average is five points higher than Lena's. So Lena's average is seventy minus five, sixty-five.",
        show(g85e, 'seventy minus five'), show(g85u['a'], 'sixty-five')),
      L("Now Lena's music score. Like in the lesson, the average of two numbers is exactly in the middle between them."),
      L("Her geography score is seventy-six. Seventy-six minus sixty-five is eleven. So it's eleven above her average.",
        show(g85f, 'Seventy-six minus sixty-five')),
      L("So her music score is eleven below her average. Sixty-five minus eleven is fifty-four.",
        show(g85g, 'Sixty-five minus eleven'), show(g85u['l'], 'is fifty-four')),
      L("Now the question. Omar's music score is seventy, and Lena's is fifty-four. Seventy minus fifty-four is sixteen.",
        show(g85h, 'Seventy minus fifty-four')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp25-p18 (English practice video)
# No Hebrew. Two averages of letters: write each as a sum (wp-081), and plugging in numbers (pick y and z, x follows).
# Traps at the step: 4 (the gap of the averages), 6 (17 - 11 only).
p18a = IH('p18a', '$\\frac{x+y+11}{3}=\\frac{y+z+17}{3}+4$', size=30)
p18b = IH('p18b', '$x+y+11=y+z+17+12$', size=30)
p18c = IH('p18c', '$x+11=z+29$', size=30, col=1)
p18d = IH('p18d', '$29-11=18$', size=30, col=1)
p18e = IH('p18e', '$x-z=18$', size=30, col=1)
p18f = IH('p18f', '$4$: $\\ $the gap of the averages', size=30, col=1)
p18g = IH('p18g', '$17-11=6$: $\\ $forgets the $4$', size=30, col=1)
p18h = IH('p18h', '$y=0,\\ z=10$', size=30)
p18i = IH('p18i', '$0+10+17=27$', size=30)
p18j = IH('p18j', '$27\\div3=9$', size=30)
p18k = IH('p18k', '$9+4=13$', size=30, col=1)
p18l = IH('p18l', '$3\\times13=39$', size=30, col=1)
p18m = IH('p18m', '$x=39-11=28$', size=30, col=1)
p18n = IH('p18n', '$28-10=18$', size=30, col=1)
video('solve-wp25-p18', 'solution', qid='wp25-p18', slides=[
    S('Method 1 · The math way: the sums',
      L("The average of x, y and eleven is four greater than the average of y, z and seventeen. What is x minus z?",
        pt('stem', 'The average of x, y and eleven', 'hl', 6.0), voice='calm', pause=0.5),
      L("So we have two averages of three numbers each, and y is in both. They ask for x minus z.",
        pt('stem', 'So we have two averages')),
      L("We'll solve it in two different ways, the math way, and then by plugging in numbers."),
      L("Let's start with the math way. Each average is a sum of three numbers, divided by three. And the first one is four "
        "more than the second.", show(p18a, 'And the first one is four')),
      L("Like in the lesson, we turn the averages into sums. We multiply both sides by three. Four times three is twelve. "
        "So the first sum is twelve more than the second sum.", show(p18b, 'So the first sum is twelve more')),
      L("y is on both sides, so we take it away. And seventeen plus twelve is twenty-nine.", show(p18c, 'seventeen plus twelve')),
      L("Now we take z and eleven away from both sides. Twenty-nine minus eleven is eighteen. So x minus z is eighteen.",
        show(p18d, 'Twenty-nine minus eleven'), show(p18e, 'So x minus z is eighteen')),
      L("That's choice number two. Careful with four, choice number four. Four is the gap between the averages. The gap "
        "between the sums is three times bigger.", show(p18f, 'Four is the gap'), mk('cross', 'choice 4', 'three times bigger')),
      L("And six, choice number three, is only seventeen minus eleven. It forgets the four.", show(p18g, 'is only seventeen minus eleven'),
        mk('cross', 'choice 3', 'It forgets the four'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. There's one condition and three letters. So we "
        "can pick y and z, and then x must fit the condition."),
      L("Let's pick y as zero, so it adds nothing. And z as ten, a round number.", show(p18h, "Let's pick y as zero")),
      L("The second average is of zero, ten and seventeen. Zero plus ten plus seventeen is twenty-seven. Twenty-seven "
        "divided by three is nine.", show(p18i, 'Zero plus ten plus seventeen'), show(p18j, 'Twenty-seven divided by three')),
      L("The first average is four more. Nine plus four is thirteen.", show(p18k, 'Nine plus four')),
      L("Like in the lesson, the sum is how many times the average. Three times thirteen is thirty-nine.",
        show(p18l, 'Three times thirteen')),
      L("The first sum is x plus zero plus eleven. So x is thirty-nine minus eleven, twenty-eight.",
        show(p18m, 'So x is thirty-nine minus eleven')),
      L("So x minus z is twenty-eight minus ten, eighteen.", show(p18n, 'twenty-eight minus ten')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

CARRY25['solve-wp25-g084'] = {1: ['six averages: $\\ \\frac{3(p+q+r+s)}{2}$'], 3: ['six averages $6$, $\\ $average $1$']}


# ------------------------------------------------------------------------------------------------ wp-086 (lesson: weighted averages)
# Hebrew (wp 5626-5640, 5650-5740, 5750-5788, 5808-5826, 5833-5844, 5911-5917): a weighted average = values with
# different weights ("importance"), the heavier value pulls the average; matriculation units; the exam just says
# "average"; the copies (3 units -> "as if there were 3 such grades", divide by 4, not 2) -> the formula (each value x its
# weight, divided by the SUM of the weights); the seesaw (tilted, push the pivot toward the heavy group; closer to the
# bigger group; the distances are the weights flipped, why: weight x distance on both sides); the exam form (an axis,
# values above, weights below, cut into units); reduce the weights; "closer to the bigger group" rules out choices.
# R37: all of it is core (g087-g090 and real exams 2021_spring_q2_09, 2024_autumn_q2_01, 2019_spring_q2_19), so it is
# taught HERE with 2-3 examples (numbers differ from the Hebrew), in three parts; percent shares as weights (was a slide
# of g089) moved here. The seesaw backwards (find a group size) stays in g090 (her own question for it). NEW (all).
c_d0 = I('c_d0', 'A weighted average: $\\ $some values count more', size=36)
c_d1 = I('c_d1', 'The heavier value pulls the average toward it', size=36)
c_e0 = I('c_e0', 'project $\\times3$: $\\ 80$, $\\ $quiz: $\\ 40$', size=38)
c_e1 = IH('c_e1', '$80,\\ 80,\\ 80,\\ 40$', size=38)
c_e2 = IH('c_e2', '$80\\times3=240$', size=36, col=1)
c_e3 = IH('c_e3', '$240+40=280$', size=36, col=1)
c_e4 = IH('c_e4', '$3+1=4$ values', size=36, col=1)
c_e5 = IH('c_e5', '$280\\div4=70$', size=36, col=1)
c_e6 = IH('c_e6', 'the middle, $\\ 60$: $\\ $no', size=36, col=1)
c_f0 = I('c_f0', 'average $=\\dfrac{\\text{value}\\times\\text{weight, added up}}{\\text{the sum of the weights}}$', size=32)
c_f1 = IH('c_f1', '$\\frac{80\\times3+40\\times1}{3+1}=\\frac{280}{4}=70$', size=36)
c_f2 = I('c_f2', 'weights $1,\\ 2,\\ 3$: $\\ 90,\\ 60,\\ 80$', size=36)
c_f3 = IH('c_f3', '$90\\times1=90$', size=36, col=1)
c_f4 = IH('c_f4', '$60\\times2=120$', size=36, col=1)
c_f5 = IH('c_f5', '$80\\times3=240$', size=36, col=1)
c_f6 = IH('c_f6', '$90+120+240=450$', size=36, col=1)
c_f7 = IH('c_f7', '$1+2+3=6$', size=36, col=1)
c_f8 = IH('c_f8', '$450\\div6=75$', size=36, col=1)
c_f9 = I('c_f9', 'Divide by the sum of the weights, $\\ $not by how many values', size=34)
c_w1 = SAW('c_w1', '40', '80', [('vals', [('vals',)]), ('wts', [('wts', '×1', '×3'), ('heavy', 1)]), ('units', [('units', 4)]),
                                ('pivot', [('pivot', 3, 4, '70')]), ('dist', [('dl', 3, 4, '30'), ('dr', 3, 4, '10')])], w=560)
c_w2 = I('c_w2', 'weights $3:1$, $\\ $distances $1:3$', size=30, col=1)
c_w3 = IH('c_w3', '$3\\times10=30$', size=36, col=1)
c_w4 = IH('c_w4', '$1\\times30=30$', size=36, col=1)
c_w5 = I('c_w5', 'The distances are the weights, flipped', size=36)
c_x0 = I('c_x0', 'test $\\times4$: $\\ 80$, $\\ $homework: $\\ 30$', size=38)
c_x1 = SAW('c_x1', '30', '80', [('vals', [('vals',)]), ('wts', [('wts', '×1', '×4'), ('heavy', 1)]), ('units', [('units', 5)]),
                                ('pivot', [('pivot', 4, 5, '70'), ('dr', 4, 5, '10')])], w=560)
c_x2 = IH('c_x2', '$80-30=50$', size=36, col=1)
c_x3 = IH('c_x3', '$50\\div5=10$', size=36, col=1)
c_x4 = IH('c_x4', '$80-10=70$', size=36, col=1)
c_x5 = IH('c_x5', '$80\\times4=320$', size=36, col=1)
c_x5b = IH('c_x5b', '$320+30=350$', size=36, col=1)
c_x6 = IH('c_x6', '$350\\div5=70$', size=36, col=1)
c_x7 = I('c_x7', 'The heavy side gets the small part of the gap', size=36)
c_g0 = I('c_g0', '$6$ numbers at $40$, $\\ 9$ numbers at $50$', size=36)
c_g1 = SAW('c_g1', '40', '50', [('vals', [('vals',)]), ('mid', [('mid', 'middle 45')]), ('wts', [('wts', '6', '9'), ('heavy', 1)]),
                                ('units', [('units', 5)]), ('pivot', [('pivot', 3, 5, '46')])], w=560)
c_g2 = IH('c_g2', '$6:9=2:3$', size=36, col=1)
c_g3 = IH('c_g3', 'distances $3:2$', size=36, col=1)
c_g4 = IH('c_g4', '$50-40=10$', size=36, col=1)
c_g5 = IH('c_g5', '$10\\div5=2$', size=36, col=1)
c_g6 = IH('c_g6', '$3\\times2=6$', size=36, col=1)
c_g7 = IH('c_g7', '$40+6=46$', size=36, col=1)
c_p0 = I('c_p0', '$70\\%$ at $30$ dollars, $\\ 30\\%$ at $50$ dollars', size=34)
c_p1 = IH('c_p1', '$50-30=20$', size=36)
c_p2 = IH('c_p2', '$10\\%$ of $20$ $=2$', size=36)
c_p3 = IH('c_p3', '$30\\%$ of $20$ $=6$', size=36)
c_p4 = IH('c_p4', '$30+6=36$', size=36)
c_p5 = I('c_p5', 'Start at the low value, $\\ $add its share of the gap', size=34, col=1)
c_p6 = IH('c_p6', '$40$: $\\ $only for $50\\%$ and $50\\%$', size=36, col=1)
c_s1 = I('c_s1', 'Each value $\\times$ its weight, $\\ \\div$ the sum of the weights', size=36)
c_s2 = I('c_s2', 'Closer to the heavy side: $\\ $the distances are the weights, flipped', size=36)
c_s3 = I('c_s3', 'Groups: $\\ $the weight is the size. $\\ $Percents are weights too.', size=36)
video('wp-086', 'lesson', slides=[
    S('Weighted Averages',
      L("Welcome back, and now weighted averages. So far, every number counted the same, and the average was the "
        "balance point. Now some numbers count more than others.")),
    S('Different weights',
      L("In a weighted average, some values are more important than others. We say they have a bigger weight.",
        show(c_d0, 'In a weighted average')),
      L("You know it from school. A big final exam counts more than a small quiz."),
      L("The heavier value pulls the average toward itself. So the average isn't in the middle anymore. It's closer to "
        "the heavier value.", show(c_d1, 'The heavier value pulls')),
      L("And on the exam it usually just says average, not weighted average. So it's up to us to notice that the values "
        "have different weights.")),
    S('As if there were copies',
      L("Here's an example. In a course, a project counts three times as much as a quiz. Dan got eighty on the project, "
        "and forty on the quiz. What's his average?", show(c_e0, 'In a course')),
      L("The project counts three times. So let's treat it as if Dan had three projects, each with eighty.",
        show(c_e1, 'as if Dan had three projects')),
      L("Now it's a normal average of four values. Eighty times three is two hundred forty. Plus forty is two hundred "
        "eighty.", show(c_e2, 'Eighty times three'), show(c_e3, 'Plus forty is two hundred')),
      L("We divide by four, not by two. Why four? Because there are three copies of the project and one quiz.",
        show(c_e4, 'Why four')),
      L("Two hundred eighty divided by four is seventy. So Dan's average is seventy.", show(c_e5, 'Two hundred eighty divided')),
      L("And seventy is closer to eighty, the heavier value. The plain middle of forty and eighty, sixty, would be wrong.",
        show(c_e6, 'The plain middle'))),
    S('The formula',
      L("What we did is the formula of the weighted average. Each value is multiplied by its weight, and we add them up. "
        "Then we divide by the sum of the weights.", show(c_f0, 'What we did is the formula')),
      L("For Dan, eighty times three plus forty times one, divided by three plus one. That's two hundred eighty divided by "
        "four, seventy.", show(c_f1, 'For Dan')),
      L("It works with more values too. Homework has weight one, a midterm has weight two, and a final has weight three. "
        "Maya got ninety, sixty and eighty.", show(c_f2, 'Homework has weight one')),
      L("Ninety times one is ninety. Sixty times two is a hundred twenty. Eighty times three is two hundred forty.",
        show(c_f3, 'Ninety times one'), show(c_f4, 'Sixty times two'), show(c_f5, 'Eighty times three')),
      L("Ninety plus a hundred twenty is two hundred ten. Plus two hundred forty is four hundred fifty.",
        show(c_f6, 'Plus two hundred forty is four hundred fifty')),
      L("The weights add up to one plus two plus three, six. Four hundred fifty divided by six is seventy-five.",
        show(c_f7, 'one plus two plus three'), show(c_f8, 'Four hundred fifty divided by six')),
      L("Careful, we divide by six, the sum of the weights. A lot of students divide by three here, because there are "
        "three values. That's the trap.", show(c_f9, 'we divide by six'))),
    S('The seesaw',
      L("Now a faster way, the seesaw. Remember, the average is the balance point."),
      L("With equal weights, the seesaw balances exactly in the middle. But when one side is heavier, the seesaw tips "
        "toward it. To balance it again, we move the pivot, the average, toward the heavy side."),
      L("How far? Let's go back to Dan. Forty with weight one, and eighty with weight three.",
        show(c_w1['line'], "Let's go back to Dan"), show(c_w1['vals'], 'Forty with weight one'), show(c_w1['wts'], 'eighty with weight three')),
      L("The average was seventy. Seventy is thirty from forty, and ten from eighty.", show(c_w1['units'], 'The average was seventy'),
        show(c_w1['pivot'], 'The average was seventy'), show(c_w1['dist'], 'Seventy is thirty from forty')),
      L("So the side of eighty is three times heavier, and it's three times closer. The weights are three to one, and the distances "
        "are one to three.", show(c_w2, 'The weights are three to one')),
      L("Why? Weight times distance is the same on both sides. Three times ten is thirty. And one times thirty is thirty. "
        "That's why the seesaw balances.", show(c_w3, 'Three times ten'), show(c_w4, 'one times thirty')),
      L("So the distances are the weights, flipped.", show(c_w5, 'So the distances are the weights'))),
    S('The seesaw on the exam',
      L("On the exam, we don't draw a real seesaw. We draw a line. The values go above its ends, and the weights go "
        "below."),
      L("For example, a test counts four times as much as homework. Noa got eighty on the test, and thirty on the "
        "homework.", show(c_x0, 'a test counts four times'), show(c_x1['line'], 'Noa got eighty'), show(c_x1['vals'], 'Noa got eighty'),
        show(c_x1['wts'], 'on the homework')),
      L("The weights are four to one. So the distances are one to four. We cut the gap into four plus one, five equal "
        "units.", show(c_x1['units'], 'five equal units')),
      L("The gap is eighty minus thirty, fifty. Fifty divided by five is ten. So each unit is ten.",
        show(c_x2, 'eighty minus thirty'), show(c_x3, 'Fifty divided by five')),
      L("The heavy side gets the small part. So the average is one unit from eighty. Eighty minus ten is seventy.",
        show(c_x1['pivot'], 'So the average is one unit'), show(c_x4, 'Eighty minus ten')),
      L("Let's check with the formula. Eighty times four is three hundred twenty, plus thirty is three hundred fifty. Three "
        "hundred fifty divided by five is seventy. The same.", show(c_x5, 'Eighty times four'), show(c_x5b, 'plus thirty is three hundred fifty'), show(c_x6, 'Three hundred fifty divided')),
      L("So remember. The heavy side gets the small part of the gap.", show(c_x7, 'The heavy side gets the small part of the gap'))),
    S('Groups as weights',
      L("Now two groups of numbers. Six numbers have an average of forty. Nine other numbers have an average of fifty. "
        "What's the average of all fifteen?", show(c_g0, 'Six numbers have an average')),
      L("Each group is like one value with a weight. The value is the group's average, and the weight is how many numbers "
        "are in it.", show(c_g1['line'], 'Each group is like one value'), show(c_g1['vals'], "The value is the group's average")),
      L("A lot of students just take the middle, forty-five. But that's only right when the groups are the same size.",
        show(c_g1['mid'], 'just take the middle')),
      L("Here the group at fifty is bigger. So the average is closer to fifty. It's above forty-five.",
        show(c_g1['wts'], 'Here the group at fifty is bigger')),
      L("How far? The weights are six to nine. We can make them smaller. We divide both by three, and get two to three.",
        show(c_g2, 'two to three')),
      L("So the distances are three to two. That's five units.", show(c_g3, 'So the distances are three to two'),
        show(c_g1['units'], "That's five units")),
      L("The gap is fifty minus forty, ten. Ten divided by five is two. So each unit is two.", show(c_g4, 'fifty minus forty'),
        show(c_g5, 'Ten divided by five')),
      L("The average is three units from forty. Three times two is six. And forty plus six is forty-six.",
        show(c_g6, 'Three times two'), show(c_g7, 'forty plus six'), show(c_g1['pivot'], 'is forty-six'))),
    S('Shares in percent',
      L("Sometimes the group sizes are given in percent. Then the percents are the weights."),
      L("In a shop, seventy percent of the shirts cost thirty dollars, and thirty percent cost fifty dollars. What's the "
        "average price?", show(c_p0, 'In a shop')),
      L("Here's a fast way. We start at the low price, thirty. The average moves toward fifty, by the share of the "
        "expensive shirts, thirty percent of the gap.", show(c_p5, 'We start at the low price')),
      L("The gap is fifty minus thirty, twenty.", show(c_p1, 'fifty minus thirty')),
      L("Thirty percent of twenty. Ten percent of twenty is two, so thirty percent is six.", show(c_p2, 'Ten percent of twenty'),
        show(c_p3, 'so thirty percent is six')),
      L("Thirty plus six is thirty-six. So the average price is thirty-six dollars.", show(c_p4, 'Thirty plus six')),
      L("Why does it work? It's the seesaw again. Seventy percent is the heavy side, so it gets the small part of the gap, "
        "six. The light side gets the big part, fourteen."),
      L("The trap is forty, the plain middle. It's only right when the shares are fifty percent and fifty percent.",
        show(c_p6, 'The trap is forty'))),
    S('Summary',
      L("Let's sum up. In a weighted average, each value is multiplied by its weight. Then we divide by the sum of the "
        "weights.", show(c_s1, 'In a weighted average')),
      L("The average is closer to the heavy side. The distances are the weights, flipped.", show(c_s2, 'The average is closer')),
      L("For groups, the weight is the size of the group. And percent shares are weights too.", show(c_s3, 'For groups')),
      L("Take a moment to memorize this. Now let's use it in the questions. I'll see you in the next video.")),
])
SPLITS.append(('wp-086', 'Weighted Averages', [
    (1, None),
    (4, "Let's continue with weighted averages, and see a faster way, the seesaw."),
    (6, "Let's continue, and use the seesaw for groups.")]))

# ------------------------------------------------------------------------------------------------ wp25-g087 (Hebrew: the biology matriculation, 3 : 1)
# Hebrew (wp 5643-5740): "it says average, we must see it's weighted"; the copies -> the formula (60, 60, 60 and 100,
# divide by 4) and then the seesaw ratios (closer to the heavy group; 3 x 10 = 1 x 30). Both kept, in her order.
# English (September): written x2 = 61, oral 97 -> 73. REMINDERS (wp-086). Traps at the step: 79 (the middle), 85 (the
# small part on the light side).
g87a = IH('g87a', '$61,\\ 61,\\ 97$', size=30)
g87b = IH('g87b', '$61\\times2=122$', size=30)
g87c = IH('g87c', '$122+97=219$', size=30)
g87d = IH('g87d', '$2+1=3$', size=30, col=1)
g87e = IH('g87e', '$210\\div3=70$', size=30, col=1)
g87f = IH('g87f', '$9\\div3=3$', size=30, col=1)
g87g = IH('g87g', '$219\\div3=73$', size=30, col=1)
g87h = IH('g87h', '$(61+97)\\div2=79$: $\\ $no weights', size=30, col=1)
g87s = SAW('g87s', '61', '97', [('vals', [('vals',)]), ('wts', [('wts', '×2', '×1'), ('heavy', 0)]), ('units', [('units', 3)]),
                                ('pivot', [('pivot', 1, 3, '73'), ('dl', 1, 3, '12')]), ('dr', [('dr', 1, 3, '24')])], w=560)
g87i = IH('g87i', '$97-61=36$', size=30, col=1)
g87j = IH('g87j', '$36\\div3=12$', size=30, col=1)
g87k = IH('g87k', '$61+12=73$', size=30, col=1)
g87l = IH('g87l', '$2\\times12=24$', size=30, col=1)
g87m = IH('g87m', '$97-24=73$', size=30, col=1)
g87n = IH('g87n', '$97-12=85$: $\\ $the light side', size=30, col=1)
video('solve-wp25-g087', 'solution', qid='wp25-g087', slides=[
    S('Method 1 · The math way: the formula',
      L("A final grade counts the written exam twice as much as the oral exam. Sara scores sixty-one on the written exam "
        "and ninety-seven on the oral exam. What is her final grade?", pt('stem', 'A final grade counts', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("So the two exams have different weights. It doesn't say weighted, but the written exam counts twice as much. So "
        "it's a weighted average.", pt('stem', 'So the two exams have different weights')),
      L("We'll solve it in two different ways, the math way with the formula, and then by understanding, with the seesaw."),
      L("Let's start with the math way. Like in the lesson, the written exam counts twice, so we treat it as two copies. "
        "Sixty-one, sixty-one and ninety-seven.", show(g87a, 'Sixty-one, sixty-one and ninety-seven')),
      L("Sixty-one times two is a hundred twenty-two. Plus ninety-seven is two hundred nineteen.",
        show(g87b, 'Sixty-one times two'), show(g87c, 'Plus ninety-seven')),
      L("We divide by the sum of the weights, two plus one, three. Not by two.", show(g87d, 'two plus one, three')),
      L("Two hundred nineteen divided by three. Two hundred ten divided by three is seventy. And nine divided by three is "
        "three. So it's seventy-three.", show(g87e, 'Two hundred ten divided by three'), show(g87f, 'nine divided by three'),
        show(g87g, "So it's seventy-three")),
      L("Careful with seventy-nine, choice number one. That's the plain middle of sixty-one and ninety-seven. It forgets "
        "the weights.", show(g87h, "That's the plain middle"), mk('cross', 'choice 1', 'It forgets the weights')),
      L("So her final grade is seventy-three. That's choice number four.")),
    S('Method 2 · Understanding: the seesaw',
      L("[pause] Now by understanding, with the seesaw. We start again from the givens. We draw a line, with sixty-one and "
        "ninety-seven above its ends.", show(g87s['line'], 'We draw a line'), show(g87s['vals'], 'with sixty-one and ninety-seven')),
      L("The weights go below. The written exam, sixty-one, has weight two. The oral exam, ninety-seven, has weight one.",
        show(g87s['wts'], 'The weights go below')),
      L("The weights are two to one, so the distances are one to two. We cut the gap into two plus one, three units.",
        show(g87s['units'], 'three units')),
      L("The gap is ninety-seven minus sixty-one, thirty-six. Thirty-six divided by three is twelve. So each unit is "
        "twelve.", show(g87i, 'ninety-seven minus sixty-one'), show(g87j, 'Thirty-six divided by three')),
      L("The heavy side gets the small part. So the average is one unit from sixty-one. Sixty-one plus twelve is "
        "seventy-three.", show(g87s['pivot'], 'So the average is one unit'), show(g87k, 'Sixty-one plus twelve'))),
    S('Method 2 · Understanding: the seesaw',
      L("Let's check from the other side. That's two units from ninety-seven. Two times twelve is twenty-four. And "
        "ninety-seven minus twenty-four is seventy-three.", show(g87l, 'Two times twelve'), show(g87m, 'ninety-seven minus twenty-four')),
      L("Careful with eighty-five, choice number three. That's one unit from ninety-seven, the light side. The small part "
        "goes to the heavy side.", show(g87n, 'one unit from ninety-seven'), mk('cross', 'choice 3', 'The small part goes')),
      L("Choice number four is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp25-g088 (Hebrew: the same question, 4 : 1)
# Hebrew (wp 5744-5788): "as we would on the exam": the axis, the values above, the weights below, 4 times heavier ->
# 4 times closer, the gap 50 into 5 units of 10 -> 90 (from either end); "it may look strange, we're used to equations,
# but with practice it's much faster". English (September): lab x5 = 91, quiz 55 -> 85; the formula as a second method.
# REMINDERS (wp-086). Trap at the step: 61 (the light side).
g88s = SAW('g88s', '55', '91', [('vals', [('vals',)]), ('wts', [('wts', '×1', '×5'), ('heavy', 1)]), ('units', [('units', 6)]),
                                ('pivot', [('pivot', 5, 6, '85'), ('dr', 5, 6, '6')])], w=560)
g88a = IH('g88a', '$91-55=36$', size=30, col=1)
g88b = IH('g88b', '$36\\div6=6$', size=30, col=1)
g88c = IH('g88c', '$91-6=85$', size=30, col=1)
g88d = IH('g88d', '$55+6=61$: $\\ $the light side', size=30, col=1)
g88e = IH('g88e', '$90\\times5=450$', size=30)
g88f = IH('g88f', '$91\\times5=455$', size=30)
g88g = IH('g88g', '$455+55=510$', size=30)
g88h = IH('g88h', '$5+1=6$', size=30, col=1)
g88i = IH('g88i', '$480\\div6=80$', size=30, col=1)
g88j = IH('g88j', '$30\\div6=5$', size=30, col=1)
g88k = IH('g88k', '$510\\div6=85$', size=30, col=1)
g88f0 = I('g88f0', '$\\dfrac{91\\times5+55\\times1}{5+1}$', size=34)
video('solve-wp25-g088', 'solution', qid='wp25-g088', slides=[
    S('Method 1 · Understanding: the seesaw',
      L("A lab report has weight five and a quiz has weight one. A student scores ninety-one on the lab report and "
        "fifty-five on the quiz. What is the weighted course score?", pt('stem', 'A lab report has weight five', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("So it's a weighted average of two scores, and the lab report is five times heavier.",
        pt('stem', "So it's a weighted average")),
      L("We'll solve it in two different ways. First by understanding with the seesaw, the way we'd do it on the exam. "
        "Then the math way, with the formula."),
      L("Let's start with the seesaw. We draw a line. Fifty-five and ninety-one go above its ends, and the weights go "
        "below, one and five.", show(g88s['line'], 'We draw a line'), show(g88s['vals'], 'Fifty-five and ninety-one go above'),
        show(g88s['wts'], 'and the weights go below')),
      L("The lab report is five times heavier, so the average is five times closer to it. The weights are five to one, so "
        "the distances are one to five."),
      L("We cut the gap into five plus one, six units.", show(g88s['units'], 'six units')),
      L("The gap is ninety-one minus fifty-five, thirty-six. Thirty-six divided by six is six. So each unit is six.",
        show(g88a, 'ninety-one minus fifty-five'), show(g88b, 'Thirty-six divided by six')),
      L("The heavy side gets the small part, one unit. Ninety-one minus six is eighty-five.",
        show(g88s['pivot'], 'The heavy side gets the small part'), show(g88c, 'Ninety-one minus six')),
      L("Careful with sixty-one, choice number three. That's one unit from fifty-five, the light side.",
        show(g88d, "That's one unit from fifty-five"), mk('cross', 'choice 3', 'the light side')),
      L("So the score is eighty-five. That's choice number two.")),
    S('Method 2 · The math way: the formula',
      L("[pause] Now the math way, with the formula. We start again from the givens. Each score times its weight, divided "
        "by the sum of the weights.", show(g88f0, 'Each score times its weight')),
      L("Ninety-one times five. Ninety times five is four hundred fifty, and five more is four hundred fifty-five.",
        show(g88e, 'Ninety times five'), show(g88f, 'and five more')),
      L("Plus fifty-five times one. Four hundred fifty-five plus fifty-five is five hundred ten.",
        show(g88g, 'Four hundred fifty-five plus fifty-five')),
      L("The weights add up to five plus one, six.", show(g88h, 'five plus one, six')),
      L("Five hundred ten divided by six. Four hundred eighty divided by six is eighty. And thirty divided by six is five. "
        "So it's eighty-five.", show(g88i, 'Four hundred eighty divided by six'), show(g88j, 'thirty divided by six'),
        show(g88k, "So it's eighty-five")),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp25-g089 (Hebrew: 5 numbers 70, 10 numbers 85, Q5)
# Hebrew (wp 5791-5859): the formula (the weight = the group's size; reduce by 3 first; "is it chance? No, always": the
# common factor cancels), the middle 77.5 + "closer to the bigger group" rules out two choices, then the ratios 1 : 2
# flipped. All three kept, in her order. English (September): 8 numbers 58, 12 numbers 78 -> 70; the estimate leaves 70
# and 72, so the seesaw finishes it. REMINDERS (wp-086, part 3).
g89a = IH('g89a', '$\\frac{8\\times58+12\\times78}{20}$', size=30)
g89b = IH('g89b', '$8:12=2:3$', size=30)
g89c = IH('g89c', '$2\\times58=116$', size=30, col=1)
g89d = IH('g89d', '$3\\times78=234$', size=30, col=1)
g89e = IH('g89e', '$116+234=350$', size=30, col=1)
g89f = IH('g89f', '$350\\div5=70$', size=30, col=1)
g89s = SAW('g89s', '58', '78', [('vals', [('vals',)]), ('mid', [('mid', 'middle 68')]), ('wts', [('wts', '8', '12'), ('heavy', 1)])], w=560)
g89g = IH('g89g', 'above $68$: $\\ $(2), (4) out', size=30, col=1)
g89t = SAW('g89t', '58', '78', [('vals', [('vals',)]), ('wts', [('wts', '2', '3'), ('heavy', 1)]), ('units', [('units', 5)]),
                                ('pivot', [('pivot', 3, 5, '70'), ('dr', 3, 5, '8')]), ('dl', [('dl', 3, 5, '12')])], w=560)
g89h = IH('g89h', '$78-58=20$', size=30, col=1)
g89i = IH('g89i', '$20\\div5=4$', size=30, col=1)
g89j = IH('g89j', '$2\\times4=8$', size=30, col=1)
g89k = IH('g89k', '$78-8=70$', size=30, col=1)
g89l = IH('g89l', '$58+3\\times4=70$', size=30, col=1)
video('solve-wp25-g089', 'solution', qid='wp25-g089', slides=[
    S('Method 1 · The math way: the formula',
      L("Eight numbers have an average of fifty-eight, and twelve other numbers have an average of seventy-eight. What is "
        "the average of all twenty numbers?", pt('stem', 'Eight numbers have an average', 'hl', 7.0), voice='calm', pause=0.5),
      L("So we have two groups of different sizes. Like in the lesson, each group is a value with a weight. The value is "
        "the group's average, and the weight is its size.", pt('stem', 'So we have two groups')),
      L("We'll solve it in three different ways. The math way, then an estimate, and then the seesaw."),
      L("Let's start with the math way. Eight times fifty-eight, plus twelve times seventy-eight, divided by eight plus "
        "twelve, twenty.", show(g89a, 'Eight times fifty-eight')),
      L("These numbers are big. So let's make the weights smaller first. Eight to twelve is two to three, because we "
        "divide both by four.", show(g89b, 'Eight to twelve is two to three')),
      L("Why can we do that? Eight is four times two. And twelve is four times three. So the four is on the top and on the "
        "bottom, and it cancels."),
      L("Two times fifty-eight is a hundred sixteen. Three times seventy-eight is two hundred thirty-four.",
        show(g89c, 'Two times fifty-eight'), show(g89d, 'Three times seventy-eight')),
      L("A hundred sixteen plus two hundred thirty-four is three hundred fifty. We divide by two plus three, five. Three "
        "hundred fifty divided by five is seventy.", show(g89e, 'A hundred sixteen plus'), show(g89f, 'hundred fifty divided by five')),
      L("So the average is seventy. That's choice number one.")),
    S('Method 2 · Estimation: the bigger group',
      L("[pause] Now let's estimate. We start again from the givens. The middle of fifty-eight and seventy-eight is "
        "sixty-eight.", show(g89s['line'], "Now let's estimate"), show(g89s['vals'], 'The middle of fifty-eight'),
        show(g89s['mid'], 'is sixty-eight')),
      L("The middle would be right only if the groups were the same size. Here the group at seventy-eight is bigger, "
        "twelve numbers. So the average is closer to seventy-eight. It's above sixty-eight.",
        show(g89s['wts'], 'Here the group at seventy-eight is bigger')),
      L("So sixty-eight, choice number two, and sixty-six, choice number four, are out.", mk('cross', 'choice 2', 'choice number two'),
        mk('cross', 'choice 4', 'choice number four'), show(g89g, 'are out')),
      L("Sometimes that alone gives the answer. Here two choices are left, seventy and seventy-two. So we need one more "
        "step, the seesaw.")),
    S('Method 3 · Understanding: the seesaw',
      L("[pause] Now by understanding, with the seesaw. The weights are eight to twelve, so two to three. So the distances "
        "are three to two.", show(g89t['line'], 'Now by understanding'), show(g89t['vals'], 'The weights are eight to twelve'),
        show(g89t['wts'], 'so two to three')),
      L("We cut the gap into three plus two, five units.", show(g89t['units'], 'five units')),
      L("The gap is seventy-eight minus fifty-eight, twenty. Twenty divided by five is four. So each unit is four.",
        show(g89h, 'seventy-eight minus fifty-eight'), show(g89i, 'Twenty divided by five')),
      L("The heavy side, seventy-eight, gets the small part, two units. Two times four is eight. Seventy-eight minus eight "
        "is seventy.", show(g89j, 'Two times four'), show(g89k, 'Seventy-eight minus eight'), show(g89t['pivot'], 'is seventy.')),
      L("Let's check from the other side, three units from fifty-eight. Three times four is twelve. And fifty-eight plus "
        "twelve is seventy.", show(g89t['dl'], 'three units from fifty-eight'), show(g89l, 'fifty-eight plus twelve')),
      L("Choice number one is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp25-g090 (Hebrew: the book, 1,000 lines, Q17)
# Hebrew (wp 5862-5910): "until now they asked for the average; here the average is given and they ask for the size of
# one group": the formula (x lines of 7, 1000 - x of 6, = 6.25 -> 250), then the ratios backwards (1/4 and 3/4: three
# times closer to 6, so 6 has three times more lines; 1000 / 4). Both kept, in her order; the September insight (start
# everyone at the low value) is Method 3. The seesaw BACKWARDS is taught here (one question + real exam 2019_spring_q2_19).
# English (September): 2,000 boxes of 3 or 5 kg, average 3.4 -> 400. Traps at the step: 1,600 and 500 (four parts).
g90a = IH('g90a', '$x$ boxes of $5$', size=30)
g90b = IH('g90b', '$2000-x$ boxes of $3$', size=30)
g90c = IH('g90c', '$\\frac{5x+3(2000-x)}{2000}=3.4$', size=30)
g90d = IH('g90d', '$5x+3(2000-x)=6800$', size=30, col=1)
g90e = IH('g90e', '$5x+6000-3x=6800$', size=30, col=1)
g90f = IH('g90f', '$2x=800$', size=30, col=1)
g90g = IH('g90g', '$x=400$', size=30, col=1)
g90s = SAW('g90s', '3', '5', [('vals', [('vals',)]), ('pivot', [('pivot', 1, 5, '3.4')]), ('dist', [('dl', 1, 5, '0.4'), ('dr', 1, 5, '1.6')]),
                              ('wts', [('wts', '×4', '×1')])], w=560)
g90h = IH('g90h', '$1.6\\div0.4=4$', size=30, col=1)
g90i = IH('g90i', '$4+1=5$ parts', size=30, col=1)
g90j = IH('g90j', '$2000\\div5=400$', size=30, col=1)
g90k = IH('g90k', '$4\\times400=1600$ $\\ $of $3$', size=30, col=1)
g90l = IH('g90l', '$2000\\div4=500$: $\\ $not $4$ parts', size=30, col=1)
g90m = IH('g90m', '$2000\\times3=6000$', size=30)
g90n = IH('g90n', '$2000\\times0.4=800$', size=30)
g90o = IH('g90o', '$6000+800=6800$', size=30)
g90p = IH('g90p', '$5-3=2$ extra each', size=30, col=1)
g90q = IH('g90q', '$800\\div2=400$', size=30, col=1)
video('solve-wp25-g090', 'solution', qid='wp25-g090', slides=[
    S('Method 1 · The math way: the formula',
      L("A delivery company ships two thousand boxes. Every box weighs either three kilograms or five kilograms, and the "
        "average weight is three point four kilograms per box. How many boxes weigh five kilograms?",
        pt('stem', 'A delivery company ships', 'hl', 10.0), voice='calm', pause=0.5),
      L("Until now we found the average. This time the average is given, and they ask for the size of one group.",
        pt('stem', 'This time the average is given')),
      L("We'll solve it in three different ways. The math way, then the seesaw backwards, and then an insight."),
      L("Let's start with the math way. The values are three and five kilograms. The weights are the numbers of boxes."),
      L("The number of five-kilogram boxes isn't given, so let's call it x. The rest, two thousand minus x boxes, weigh "
        "three kilograms.", show(g90a, "so let's call it x"), show(g90b, 'The rest, two thousand minus x')),
      L("Each weight times its number of boxes, divided by all two thousand boxes, is three point four.",
        show(g90c, 'Each weight times its number')),
      L("We multiply both sides by two thousand. Two thousand times three is six thousand. And two thousand times zero "
        "point four is eight hundred. So the right side is six thousand eight hundred.", show(g90d, 'So the right side is')),
      L("We open the brackets. Three times two thousand is six thousand. And three times x is three x.",
        show(g90e, 'We open the brackets')),
      L("Five x minus three x is two x. And six thousand eight hundred minus six thousand is eight hundred. So two x is "
        "eight hundred.", show(g90f, 'So two x is eight hundred')),
      L("We divide both sides by two, and x is four hundred. So four hundred boxes weigh five kilograms, choice number "
        "three.", show(g90g, 'and x is four hundred'))),
    S('Method 2 · Understanding: the seesaw backwards',
      L("[pause] Now by understanding, with the seesaw, but backwards. We start again from the givens. This time we know "
        "where the pivot is, three point four. And we look for the weights.", show(g90s['line'], 'with the seesaw, but backwards'),
        show(g90s['vals'], 'with the seesaw, but backwards'), show(g90s['pivot'], 'where the pivot is')),
      L("Three point four is zero point four from three, and one point six from five.", show(g90s['dist'], 'is zero point four from three')),
      L("One point six divided by zero point four is four. So the average is four times closer to three.",
        show(g90h, 'One point six divided by')),
      L("Like in the lesson, the heavy side is the closer side. So the three-kilogram group is four times bigger. The "
        "weights are four parts to one part.", show(g90s['wts'], 'The weights are four parts')),
      L("So we cut the two thousand boxes into four plus one, five parts. Two thousand divided by five is four hundred.",
        show(g90i, 'four plus one, five parts'), show(g90j, 'Two thousand divided by five')),
      L("The five-kilogram boxes are one part, four hundred. The other four parts, sixteen hundred boxes, weigh three "
        "kilograms.", show(g90k, 'sixteen hundred boxes')),
      L("Careful with sixteen hundred, choice number two. That's the three-kilogram boxes. And five hundred, choice number "
        "one, is two thousand divided by four. But there are five parts, not four.", mk('cross', 'choice 2', "That's the three-kilogram boxes"),
        show(g90l, 'is two thousand divided by four'), mk('cross', 'choice 1', 'But there are five parts')),
      L("So four hundred again, choice number three."),
      L("This works every time the average is given and they ask about the groups. The distances from the average, "
        "flipped, give the sizes of the groups. The closer value has the bigger group.")),
    S('Method 3 · Insight: start at the low value',
      L("[pause] Now an insight. We start again from the givens. Let's pretend every box weighs three kilograms. Two "
        "thousand times three is six thousand kilograms.", show(g90m, 'Two thousand times three')),
      L("But the real total is two thousand times three point four. Two thousand times zero point four is eight hundred. "
        "So the real total is six thousand eight hundred kilograms.", show(g90n, 'Two thousand times zero point four'),
        show(g90o, 'So the real total is six thousand')),
      L("So eight hundred kilograms are extra. Where do they come from? From the five-kilogram boxes. Each one is five "
        "minus three, two kilograms more than three.", show(g90p, 'five minus three')),
      L("Eight hundred divided by two is four hundred. So four hundred boxes weigh five kilograms.",
        show(g90q, 'Eight hundred divided by two')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

CARRY25['solve-wp25-g087'] = {2: ['$1$ unit $=12$', 'average: $\\ 61+12=73$']}
# =================================================================================================================
# Extra-visual pass (about one event every 2-4 s): in a solution video every spoken "number N" that has no cue on that
# choice in the same sentence gets a POINT on choice N; every "the given(s)" / "the question" without a cue points at the
# stem. Inserted by position, so each line's cues stay in speaking order.
# =================================================================================================================
_NUM = {'one': 1, 'two': 2, 'three': 3, 'four': 4}


def _phrase_pos(say, c):
    ph = c[2] if c[0] in ('show', 'point') else c[3]
    return -1 if ph.startswith('<') else say.lower().find(ph.lower())


def _unique(say, k, n=3):
    """a phrase starting at k whose FIRST occurrence in the line is at k (grow it word by word)."""
    words = re.finditer(r'\S+', say[k:])
    ends = [m.end() for m in words]
    for j in range(min(n, len(ends)) - 1, len(ends)):
        ph = say[k:k + ends[j]].rstrip('.,?!')
        if '[' in ph or ']' in ph: return None
        if say.lower().find(ph.lower()) == k: return ph
    return None


def _densify(vid):
    V = VIDEOS[vid]
    if V['kind'] != 'solution': return
    for sl in V['slides']:
        for ln in sl['lines'][1:] if sl is V['slides'][0] else sl['lines']:
            say = ln['say']; have = [(_phrase_pos(say, c), c) for c in ln['cues']]
            sents = [(m.start(), m.end()) for m in re.finditer(r'[^.?!]+[.?!]?', say)]
            add = []
            for m in re.finditer(r'\b[Nn]umbers? (one|two|three|four)\b', say):
                ch = 'choice %d' % _NUM[m.group(1)]
                s0, s1 = next(((a, b) for a, b in sents if a <= m.start() < b), (0, len(say)))
                if any(s0 <= p < s1 and (ch in c) for p, c in have): continue
                ph = _unique(say, m.start())
                if ph: add.append((m.start(), pt(ch, ph)))
            for m in re.finditer(r'\b(the givens?|the question)\b', say, re.I):
                s0, s1 = next(((a, b) for a, b in sents if a <= m.start() < b), (0, len(say)))
                if any(s0 <= p < s1 for p, c in have): continue
                ph = _unique(say, m.start())
                if ph: add.append((m.start(), pt('stem', ph)))
            if add:
                allc = have + add
                allc.sort(key=lambda x: x[0])
                ln['cues'] = [c for p, c in allc]


_SKIP = re.compile(r"^(Our (first|second|third) method|We'll (solve|do)|Two ways|Okay|I'll see you|Which way|So which way|"
                   r"Welcome|Before|Let's see it in numbers|Try it|That's it|Now go)", re.I)


def _follow(vid):
    """a sentence with no cue that talks on about the step just shown: a POINT on that board item (the line being
    explained lights up while it is explained)."""
    V = VIDEOS[vid]
    for si, sl in enumerate(V['slides']):
        last = None
        for ln in sl['lines']:
            say = ln['say']; have = [(_phrase_pos(say, c), c) for c in ln['cues']]
            add = []
            for m in re.finditer(r'[^.?!]+[.?!]?', say):
                k = m.start() + len(m.group()) - len(m.group().lstrip())
                t = TAG.match(say, k)
                while t: k = t.end() + 1 if say[t.end():t.end() + 1] == ' ' else t.end(); t = TAG.match(say, k)
                body = say[k:m.end()]
                prev_shows = [c for p, c in have if p < k and c[0] == 'show']
                if prev_shows: last = prev_shows[-1][1]['_name']
                if any(m.start() <= p < m.end() for p, c in have): 
                    for p, c in have:
                        if m.start() <= p < m.end() and c[0] == 'show': last = c[1]['_name']
                    continue
                if len(body.split()) <= 4 or _SKIP.match(body) or last is None: continue
                ph = _unique(say, k)
                if ph: add.append((k, pt(_base(last), ph)))
            if add:
                allc = sorted(have + add, key=lambda x: x[0])
                ln['cues'] = [c for p, c in allc]
            for p, c in have:
                if c[0] == 'show': last = c[1]['_name']


# Method headers (2026-10-11, teacher: "make it easy to follow" - a method change must be clear on the board): a solution
# slide titled "Method N · X" gets a small header line "Method N: X" at the top of its work area, shown when the voice
# names the method in the slide's first line ("Our second method", "first by understanding", ...).
_ORD = r"(?:first|second|third|fourth)"


HDR_ROOM = 330          # px of left-column steps (estimated) above which a slide has no room for the method header


def _method_headers(vid):
    V = VIDEOS[vid]
    if V['kind'] != 'solution': return
    for si, sl in enumerate(V['slides']):
        m = re.match(r'Method (\d) · (.+)$', sl['title'])
        if not m: continue
        # 2026-10-11 (teacher): no "Our first / second method" lines any more - the header comes with the first words of
        # the method's first line (slide 1: the line after the first reaction); a continuation slide of the same method
        # gets no second header
        if si and V['slides'][si - 1]['sb'] == sl['sb']: continue
        lines = sl['lines'][2:3] if si == 0 else sl['lines'][:1]
        for ln in lines:
            say = ln['say']; h = re.search(r"[A-Za-z]", TAG.sub(lambda q: ' ' * len(q.group(0)), say))
            if not h: continue
            ph = _unique(say, h.start(), 2)
            if not ph: continue
            col0 = [c[1] for l2 in sl['lines'] for c in l2['cues'] if c[0] == 'show' and c[1]['_col'] == 0 and not c[1].get('over')]
            est = sum((it['h'] if it['k'] == 'vis' else it.get('size', 36) * 1.55) + 16 for it in col0)
            if est + 45 > HDR_ROOM: break     # a full left column keeps its room (the sidebar still names the method)
            it = I('hdr%d' % si, 'Method %s: %s' % (m.group(1), m.group(2)), size=28)
            have = [(_phrase_pos(say, c), c) for c in ln['cues']]
            ln['cues'] = [c for p, c in sorted(have + [(h.start() - .5, show(it, ph))], key=lambda x: x[0])]
            break


def _base(name):
    """a number-line layer ('n1_left') -> its base line ('n1_line'): a POINT on a layer lit nothing visible (q-359)"""
    return LAYER_BASE.get(name) or re.sub(r'_(left|right|band)$', '_line', name)


# 2026-10-11 (teacher, her own voice: "no empty screen while I explain"): no stretch of more than FILL_W words without a
# visual. A long stretch gets a POINT every ~7 words on what it talks about - the item shown last on this slide (a figure
# layer -> its base line), else the question. Runs after the passes above, so it only fills what is still empty.
FILL_W, FILL_STEP = 6, 5
_CLOSE = re.compile(r"(Okay\.|I'll see you)", re.I)


def _fill(vid):
    V = VIDEOS[vid]
    for si, sl in enumerate(V['slides']):
        last = None
        for li, ln in enumerate(sl['lines']):
            if si == 0 and li == 0: 
                continue                                     # the question reading: the question is lit already
            say = ln['say']; have = sorted([(_phrase_pos(say, c), c) for c in ln['cues']], key=lambda x: x[0])
            masked = TAG.sub(lambda m: ' ' * len(m.group(0)), say)            # no word inside a [pause] tag
            words = [m.start() for m in re.finditer(r'\S+', masked)]
            cut_at = (_CLOSE.search(say).start() if _CLOSE.search(say) else len(say))
            marks_ = [p for p, c in have if p >= 0] + [cut_at]
            add, prev, idx = [], 0, 0
            ctx = lambda pos: next((c[1]['_name'] for p, c in reversed(have) if p <= pos and c[0] == 'show'), last)
            for b in marks_:
                seg = [w for w in words if prev <= w < b]
                if len(seg) > FILL_W:
                    for k in range(FILL_STEP // 2 + 2, len(seg) - 2, FILL_STEP):
                        ph = _unique(say, seg[k])
                        tg = ctx(seg[k])
                        if ph: add.append((seg[k], pt(_base(tg) if tg else 'stem', ph)))
                prev = b + 1
            if add:
                ln['cues'] = [c for p, c in sorted(have + add, key=lambda x: x[0])]
            for p, c in have:
                if c[0] == 'show': last = c[1]['_name']


# 2026-10-11 (topic 14): a hand-written item is drawn stroke by stroke and only counts as "on the board" when the pen is
# done (studio_autonarrate anWrites: at least glyphs/14 s). A POINT / mark on that item while it is still being written
# stops the auto-narrate run ("item N is not on the board at this moment"). So a cue on an item that is being written
# must come late enough in the same line: points and marks that come too early are dropped (marks are listed).
CPS = 14.0         # her reading pace, characters a second (about 155 words a minute)
WRITE_LATE = []


def _write_gap(vid):
    V = VIDEOS[vid]
    for sl in V['slides']:
        for ln in sl['lines']:
            say = ln['say']; keep = []; writing = {}      # item name -> (word index of its show, words needed)
            chars = lambda p: len(TAG.sub('', say[:p]))
            for c in ln['cues']:
                p = _phrase_pos(say, c)
                if c[0] == 'show' and c[1].get('_hand'):
                    n = HWR.write(c[1]['_hand'])['n']                 # glyphs: the pen needs at least n/14 s
                    writing[c[1]['_name']] = (chars(p) if p >= 0 else 0, (max(.35, n / 14.0) + .45) * CPS)
                tgt = c[1] if c[0] == 'point' else (c[2] if c[0] == 'mark' else None)
                if isinstance(tgt, str):
                    nm = _base(tgt.split(':')[0].strip())
                    if nm in writing and p >= 0 and chars(p) - writing[nm][0] < writing[nm][1]:
                        if c[0] == 'mark': WRITE_LATE.append((vid, c[3], nm))
                        continue
                keep.append(c)
            ln['cues'] = keep




# 2026-10-11 teacher: "when I talk about the second given, highlight only the second given" (from topic 13): a POINT on
# 'stem' becomes the part of the question her sentence is about (studio_autonarrate anStemParts: g1 g2 g3 = each given
# formula, given = all of them, ask = the question sentence), matched on the sentence's words; the whole stem only when
# nothing matches (and on the question reading itself). The stems are copied from the course (stemRich).

# 2026-10-11 teacher: "when I talk about the second given, highlight only the second given" (from topic 13): a POINT on
# 'stem' becomes the part of the question her sentence is about (given = the story, ask = the question sentence). The
# stems are copied from the course (stemRich).
STEMS = {
 "wp25-g082": "Twelve volunteers clean a beach. On average, each volunteer fills 7 bags of litter. How many bags do they fill altogether?",
 "wp25-g083": "Ethan is 169 cm tall. The average height of Ethan and Chloe is 164 cm. Ryan is 18 cm taller than Chloe. How tall is Ryan?",
 "q-r26-t25-02": "Dana took five tests. Her scores on four of them were 78, 85, 91 and 88. The average of all five scores is 85. What was her score on the fifth test?",
 "q-r26-t25-01": "The average score of the students in a class was 70. A new student with a score of 94 joined the class, and the class average rose to 73. How many students were in the class before the new student joined?",
 "q-r26-t25-03": "Six different positive integers have an average of 9. What is the largest possible value of one of them?",
 "q-r26-t25-04": "The average of nine consecutive even numbers is 30. What is the largest of them?",
 "q-r26-t25-05": "The average of $a$, $b$ and $c$ is $20$. What is the average of $3a+2$, $3b+2$ and $3c+2$?",
 "wp25-g084": "Four numbers are given. Take the average of each of the six different pairs, then add those six averages. The result equals which of the following?",
 "wp25-g085": "Omar and Lena take two tests, geography and music. Lena’s geography score is 6 points higher than Omar’s. Omar’s two-test average is 5 points higher than Lena’s. How much higher is Omar’s music score than Lena’s?",
 "wp25-p18": "The average of $x$, $y$ and $11$ is $4$ greater than the average of $y$, $z$ and $17$. What is $x-z$?",
 "wp25-g087": "A final grade counts the written exam twice as much as the oral exam. Sara scores 61 on the written exam and 97 on the oral exam. What is her final grade?",
 "wp25-g088": "A lab report has weight 5 and a quiz has weight 1. A student scores 91 on the lab report and 55 on the quiz. What is the weighted course score?",
 "wp25-g089": "Eight numbers have an average of 58, and twelve other numbers have an average of 78. What is the average of all twenty numbers?",
 "wp25-g090": "A delivery company ships 2,000 boxes. Every box weighs either 3 kg or 5 kg, and the average weight is 3.4 kg per box. How many boxes weigh 5 kg?",
}   # word stems: "given" = the story, "ask" = the question sentence

_NW = {str(i): w for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve thirteen '
       'fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split())}
_SYN = {'negative': 'minus', 'less': 'smaller', 'greater': 'bigger', 'more': 'bigger', 'larger': 'bigger', 'equals': 'is',
        'equal': 'is', 'absolute': 'abs', 'bars': 'abs', 'positive': 'pos', 'negatives': 'minus', 'cdot': 'times'}


def _words(t):
    t = re.sub(r'(\d+)', lambda m: ' ' + _NW.get(m.group(1), m.group(1)) + ' ', t.lower())
    return [_SYN.get(w, w) for w in re.findall(r"[a-z]+", t)]


def _tex_words(tex):
    t = tex.replace('\\left', '').replace('\\right', '').replace('\\cdot', ' times ').replace('\\ne', ' not equal ')
    t = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r' \1 over \2 ', t)
    t = t.replace('|', ' absolute ').replace('<', ' smaller ').replace('>', ' bigger ').replace('=', ' is ')
    t = t.replace('+', ' plus ').replace('-', ' minus ')
    return _words(t)


def _stem_part_words(stem):
    m = re.search(r'(Which|What|How)\b[^$]*?(\$[^$]*\$[^$]*?)*[?]?\s*$', stem)
    ask = stem[m.start():] if m else ''
    head = stem[:m.start()] if m else stem
    g = head.split('Given:', 1)[1] if 'Given:' in head else ''      # topic 15: no "Given:" = no given parts (word stems)
    parts, n = {}, 0
    for f in re.findall(r'\$([^$]*)\$', g):
        rows = re.split(r'\\\\', re.sub(r'\\(begin|end)\{cases\}', '', f)) if 'cases' in f else [f]
        for r in rows:
            n += 1; parts['g%d' % n] = _tex_words(r)
    if ask: parts['ask'] = _words(re.sub(r'\$([^$]*)\$', lambda m: ' '.join(_tex_words(m.group(1))), ask))
    if 'Given:' not in head and head.strip():         # topic 22 word stems: the story (studio anStemParts: given = all before ask)
        parts['given'] = _words(re.sub(r'\$([^$]*)\$', lambda m: ' '.join(_tex_words(m.group(1))), head))
    return parts


_W8 = {'is': 0, 'the': 0, 'of': 0, 'a': 0, 'abs': 1, 'value': 0, 'smaller': 1, 'bigger': 1, 'plus': 1, 'minus': 1,
       'times': 1, 'over': 1, 'not': 1, 'following': 0, 'which': 1, 'true': 1, 'necessarily': 2, 'could': 2,
       'cannot': 2, 'possible': 2, 'values': 1, 'all': 1, 'precise': 2, 'domain': 2, 'what': 1, 'gives': 1}
_ORDN = {'first': 'g1', 'second': 'g2', 'third': 'g3'}


def _stem_target(stem, sent):
    P = _stem_part_words(stem); sw = _words(sent); ss = set(sw)
    m = re.search(r'\b(first|second|third) given', sent, re.I)
    if m and _ORDN[m.group(1).lower()] in P: return _ORDN[m.group(1).lower()]
    if re.search(r'\b(both|the) givens\b|\bgivens\b', sent, re.I) and 'given' not in ss - {'givens'}: return 'given' if any(k.startswith('g') for k in P) else None
    if re.search(r"\b(they ask|they're asking|the question|asking)\b", sent, re.I) and 'ask' in P: return 'ask'
    sc = {}
    for k, ws in P.items():
        sc[k] = sum(_W8.get(w, 2) for w in set(ws) if w in ss)
    best = sorted(sc.items(), key=lambda x: -x[1])
    if best and best[0][1] >= 2 and (len(best) == 1 or best[0][1] > best[1][1]): return best[0][0]
    return None


def _stem_parts(vid):
    V = VIDEOS[vid]; stem = STEMS.get(V.get('qid'))
    if not stem: return
    for si, sl in enumerate(V['slides']):
        for li, ln in enumerate(sl['lines']):
            if si == 0 and li == 0: continue                      # the question reading: the whole question
            say = ln['say']; new = []
            for c in ln['cues']:
                if c[0] == 'point' and c[1] == 'stem':
                    p = say.find(c[2].lstrip('<')); a = max(say.rfind('.', 0, max(p, 0)), say.rfind('?', 0, max(p, 0))) + 1
                    b = min([x for x in (say.find('.', p), say.find('?', p)) if x >= 0] or [len(say)])
                    tg = _stem_target(stem, say[a:b + 1])
                    if tg: c = ('point', 'stem: ' + tg) + tuple(c[2:])
                new.append(c)
            ln['cues'] = new



# the camera lesson in parts of about 3-4 minutes (math_patches/_camera_parts.py), before the visual passes
_cp_spec = importlib.util.spec_from_file_location('_camera_parts', os.path.join(HERE, '_camera_parts.py'))
CP = importlib.util.module_from_spec(_cp_spec); _cp_spec.loader.exec_module(CP)
CP.split(globals(), *CAMERA_SPLIT)
for _sp in SPLITS: CP.split(globals(), *_sp)     # 2026-10-21 R37: the lessons that grew (core methods in them), in parts, not on camera

for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _stem_parts(_v); _write_gap(_v)



# 2026-10-13 carry-over boxes (V2) and the layer-order check (V1): after the visual passes, like topics 13-18
import types as _types
MV.carry(_types.SimpleNamespace(**globals()), CARRY25)
for _v in CARRY25:                                      # 2026-10-18 visual check: the So-far box at a readable size
    for _sl in VIDEOS[_v]['slides']:
        for _ln in _sl['lines']:
            for _c in _ln['cues']:
                if _c[0] == 'show' and _c[1].get('keep'): _c[1]['size'] = 30
MV.calm(_types.SimpleNamespace(**globals()), ORDER)     # 2026-10-13 steady highlights (visual only)
_lp = [(v, p) for v in ORDER for p in MV.check_layers(VIDEOS[v])]
assert not _lp, ('figure layers out of order', _lp)


# 2026-10-15 one vocabulary for method names (math_patches/_method_names.py CORE; guide "Method names"): a "Method N · X"
# title or sidebar outside it stops the run, so a new script uses the vocabulary from its first draft.
_mn_spec = importlib.util.spec_from_file_location('_method_names_vocab', os.path.join(HERE, '_method_names.py'))
_mn = importlib.util.module_from_spec(_mn_spec); _mn_spec.loader.exec_module(_mn)
_mn.check_vocab(VIDEOS)


if __name__ == '__main__':
    _bad = 0
    for _v in sys.argv[1:] or ORDER:
        _p = check(_v)
        if _p: print('PROBLEMS', _v, _p); _bad += 1
        print('script written:', write_json(_v), stats(_v))
    for x in WRITE_LATE: print('mark dropped (its item is still being written):', x)
    sys.exit(1 if _bad else 0)
