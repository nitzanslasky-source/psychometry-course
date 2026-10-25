"""Topic 28 (Counting possibilities and factorials) - the scripts for the teacher's own-voice reading (2026-10-25),
written from the first draft to the Codex review standard, the clarity style, W1-W26 (W24: Codex's lessons, W25: the
acceptance standard, W26: plugging in the answers does not always hit first), R37 (core methods taught in the lessons),
the method vocabulary and the method visuals, built exactly like topics 22-27 (math_patches/_ai_vis_t27.py: the DSL and
the visual passes are copied here, so the topics stay independent).

The camera lesson 'wp-123' (Counting Possibilities: what we count, listing in order, multiplying the choices) gets a full
reading script with more examples, split into parts of about 3-4 minutes (math_patches/_camera_parts.py). Every other
lesson of the topic is a real R37 lesson now (the old two-slide stubs are gone): wp-124-after (restrictions and forced
choices), wp-127 (the pool: with or without repetition, rows and factorial), wp-131 (mutual action), wp-134 (adding and
subtracting cases), wp-137 (choosing a group), wp-140-after (factorials), wp-141-after (forced digits), r26-t28-cases
("at least one", boxes, the worst case) and r26-t28-arrange (together, apart, repeats, a round table); the long ones are
split into parts (not on camera). Every other topic-28 video gets a script that SHE reads aloud in the Reading Studio.
The summary video r26-t28-summary is not read: summary_pages/t28.json (python3 summary_pages.py 28) replaces it.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t28.py [vid ...] writes it);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t28.py ai_redo_t28() (runs LAST) rebuilds the slides from studio_slides(vid) and then
                    _ai_visual.apply() adds the click items, POINT highlights and pen marks around it.

Spec DSL (as in topic 27): video / S / L / I / IH (a hand-written board line) / show / pt / mk; the topic-28 pictures of
her Hebrew course, built in layers at the spoken words: SLOTS28 (the stage slots: a box per stage, the number of options
written in it, the times signs, the product; a short list under a box), TREE28 (a small tree for a tiny case, before the
rule), LIST28 (a full list for a tiny case: every arrangement in rows, repeats crossed out, the same group bracketed, a
glued block), DOTS28 (points on a circle: towns, vertices, people at a round table, with the lines between them),
POOL28 (the pool of items, picked items crossed out or put back) and TBL (the games table). The concept map (NEW /
REMINDER per video) is in ~/Downloads/Topic-28-AI-scripts-review.md.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(HERE) != 'math_patches':      # a test copy elsewhere still reads and writes the real studio files
    HERE = '/Users/nitzanslasky/psychometry-course/studio-build/math_patches'
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t28ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-28 flow order of the scripts
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
QBOT = {}   # filled below (measured on the frames)


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
CAM_BASE = 'wp-123'
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
            'style': "the teacher reads it herself (Reading Studio), topic-28 scripts (2026-10-25): math_patches/_ai_vis_t28.py is "
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
      ('right', r, text)               a value after the row
      ('tick', r, i, text)             a clock time over the edge before box i (a timeline)"""
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
            elif k == 'tick':                    # 2026-10-21 a clock time above the edge before box i (a timeline)
                r, i, t = m[1], m[2], m[3]
                b += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"/>' % (bx(i), rt(r) - 10, bx(i), rt(r) + boxh, _INK)
                      + _tx(bx(i), rt(r) - 16, t, 26, _INK))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def OWN(d, name):
    """a ZL number line whose layers find their own base (written lines may come in between)"""
    for it in d.values():
        if it.get('over'): it['of'] = name
        else: it['fig'] = name
    return d



CARRY28 = {}      # vid -> carry-over ("So far") boxes, _method_visuals.carry format
SPLITS = []       # lessons split into parts (not on camera)


# ------------------------------------------------------------------------------------------- topic-28 figures (V1)
# The pictures of her Hebrew counting lessons, built in layers at the spoken words (own=True: a layer finds its own
# base, so written lines can come in between):
#   SLOTS28  the stage slots (wp 8340-8352 «אנחנו רושמים את מספר האפשרויות בכל שלב... ובסוף כופלים»; 8541-8572 the
#            books: «ראשון, שני, שלישי... 5, 4, 3, 2, 1»; 9305-9314 «למעלה אני כותב את מספר האופציות ולמטה אני מפרט»):
#            a box per stage with its name above, the number of options written in it at the words, the times signs,
#            the product; the options listed under a box; a forced box gets its 1.
#   TREE28   a small tree for a tiny case (wp 8355-8384: «נניח ובחרתי את הסלט הזה... 5 ועוד 5 ועוד 5»): the first
#            choices in a column, the branches of each one drawn as it is named, the count of each group.
#   LIST28   a full list for a tiny case (wp 8303-8331 123, 124, 134, 234; 8697-8727 the 12 flights, each line twice;
#            9024-9047 the same three children in six orders = one group; 9714-9744 the rows of students): rows of
#            cells written one by one, a repeat crossed out, rows that are the same group bracketed, a glued block.
#   DOTS28   points on a circle (wp 8642 «הנה הגלובוס שלנו»: the countries; 8760-8790 the hexagon's vertices; a round
#            table): the points with their names, the lines between them drawn as they are counted.
#   POOL28   the pool (wp 8471-8540 «האם האיבר שבחרנו יצא מהמאגר... המאגר הלך והצטמצם»): the items in a frame, a
#            picked item marked, an item that left the pool crossed out, or put back.
#   TBL      (above) the games table of g143 (wp 9640-9690: teams | games added | total).
_RED28 = '#d62d48'


def _c28(c):
    return {'teal': _TEAL, 'orange': ORANGE, 'red': _RED28, 'ink': _INK, None: _INK, '': _INK}.get(c, c)


def SLOTS28(name, labels, layers, boxw=150, boxh=100, gap=60, eqw=None, sub=0, col=0, w=None, title='Stages of choice',
            lab_size=28):
    """a row of stage boxes, labels above. layers = [(key, [mark, ...])]:
      ('n', i, text[, colour])   the number of options in box i (big)
      ('x',)                     the times signs between all the boxes
      ('x', i)                   one times sign, between box i and box i + 1
      ('eq', text[, colour])     '= text' after the last box
      ('sub', i, text[, row])    a small text under box i (the options listed; row 0, 1, 2 for more lines)
      ('hl', i[, colour])        a thick frame around box i (the stage we talk about)
      ('cross', i)               a red line through box i's number (a wrong count)"""
    n = len(labels); x0 = 14
    if eqw is None:              # room for '= 24' after the last box (only as wide as the result needs)
        eqs = [m[1] for _k, ms in layers for m in ms if m[0] == 'eq']
        eqw = (40 + 30 * max(len(t) for t in eqs) + 30) if eqs else 14
    W = x0 + n * boxw + (n - 1) * gap + (eqw if eqw else 14); y0 = 48
    H = y0 + boxh + (18 + 34 * sub if sub else 14)
    bx = lambda i: x0 + i * (boxw + gap)
    body = ''
    for i, lab in enumerate(labels):
        body += ('<rect x="%.1f" y="%d" width="%d" height="%d" rx="10" fill="#ffffff" stroke="%s" stroke-width="2.6"/>'
                 % (bx(i), y0, boxw, boxh, _INK)) + MV._text(bx(i) + boxw / 2.0, y0 - 14, lab, lab_size, _INK)
    out = [('line', MV._svg(W, H, body, title + ': ' + ', '.join(labels)))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'n':
                b += MV._text(bx(m[1]) + boxw / 2.0, y0 + boxh * .66, m[2], 50, _c28(m[3] if len(m) > 3 else None))
            elif k == 'x':
                for i in ([m[1]] if len(m) > 1 else range(n - 1)):
                    b += MV._text(bx(i) + boxw + gap / 2.0, y0 + boxh * .64, '×', 44, _INK)
            elif k == 'eq':
                b += MV._text(bx(n - 1) + boxw + 16, y0 + boxh * .66, '= ' + m[1], 46, _c28(m[2] if len(m) > 2 else 'teal'), 'start')
            elif k == 'sub':
                row = m[3] if len(m) > 3 else 0
                b += MV._text(bx(m[1]) + boxw / 2.0, y0 + boxh + 34 + 34 * row, m[2], 25, _TEAL)
            elif k == 'hl':
                b += ('<rect x="%.1f" y="%d" width="%d" height="%d" rx="12" fill="none" stroke="%s" stroke-width="5"/>'
                      % (bx(m[1]) - 5, y0 - 5, boxw + 10, boxh + 10, _c28(m[2] if len(m) > 2 else 'teal')))
            elif k == 'cross':
                x, y = bx(m[1]) + boxw / 2.0, y0 + boxh * .5
                b += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="5"/>' % (x - 38, y + 26, x + 38, y - 26, _RED28)
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def TREE28(name, roots, kids, layers, rowh=50, col=0, w=None, title='A small tree', size=28, kidw=None, right=220):
    """a tree for a tiny case: the first choices (roots) in a column on the left; layers = [(key, [mark, ...])]:
      ('br', i)            the branches of root i to every kid, with the kids' names
      ('cnt', i, text)     a teal text right of root i's group (its count)
      ('sum', text)        a teal text under the tree
      ('leaf', i, j, text) a text after kid j of root i (the full result, e.g. 'soup 1, bread A')
      ('hl', i)            a teal frame around root i"""
    nk = len(kids); nr = len(roots)
    rootw = max(len(r) for r in roots) * size * .62 + 30
    kw = kidw or max(len(k) for k in kids) * size * .62 + 30
    x_r = 10; x_k = x_r + rootw + 90
    gh = nk * rowh + 16
    W = int(x_k + kw + right); H = int(nr * gh + 70)
    ry = lambda i: 20 + i * gh + gh / 2.0
    ky = lambda i, j: 20 + i * gh + 8 + rowh * (j + .5)
    body = ''
    for i, r in enumerate(roots):
        body += ('<rect x="%.1f" y="%.1f" width="%.1f" height="44" rx="10" fill="%s" stroke="%s" stroke-width="2.4"/>'
                 % (x_r, ry(i) - 22, rootw, _LIGHT, _INK) + MV._text(x_r + rootw / 2.0, ry(i) + 10, r, size, _INK))
    out = [('line', MV._svg(W, H, body, title + ': ' + ', '.join(roots)))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'br':
                i = m[1]
                for j, kd in enumerate(kids):
                    b += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4"/>'
                          % (x_r + rootw, ry(i), x_k - 8, ky(i, j) - 8, _TEAL))
                    b += MV._text(x_k, ky(i, j) + 2, kd, size, _INK, 'start')
            elif k == 'cnt':
                i = m[1]
                b += MV._text(x_k + kw + 30, ry(i) + 12, m[2], size + 4, _TEAL, 'start')
            elif k == 'sum':
                b += MV._text(W / 2.0, H - 16, m[1], size + 4, _TEAL)
            elif k == 'leaf':
                b += MV._text(x_k + kw + 10, ky(m[1], m[2]) + 2, m[3], size - 4, _TEAL, 'start')
            elif k == 'hl':
                i = m[1]
                b += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="12" fill="none" stroke="%s" stroke-width="4"/>'
                      % (x_r - 6, 20 + i * gh + 2, x_k + kw - x_r + 12, gh - 4, _TEAL))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def LIST28(name, nrows, ncols, layers, cellw=96, cellh=52, head=None, grid=False, right=220, col=0, w=None,
           title='The full list', size=32, gapc=12):
    """a list for a tiny case: rows of cells (each cell one item, e.g. a letter or a digit). layers = [(key, [mark, ...])]:
      ('c', r, c, text[, colour])     a cell text
      ('r', r, text[, colour])        a whole row at once, one character per cell ('ABC'); or a list of cell texts
      ('strike', r[, colour])         a line through row r (a repeat), red
      ('ring', r0, r1, text)          a bracket right of rows r0..r1 with a text (the same group / the same arrangement)
      ('note', r, text[, colour])     a text right of row r
      ('glue', r, c0, c1[, colour])   a rounded frame around cells c0..c1 of row r (glued together)
      ('hl', r, c[, colour])          a filled tint behind cell (r, c)
      ('xc', r, c)                    a red line through cell (r, c) (not allowed)
      ('foot', text[, colour])        a text under the list
    head = column names written above the first row; grid = draw every cell border (a square of digits)"""
    x0 = 10; yh = 40 if head else 6
    has_foot = any(m[0] == 'foot' for _k, ms in layers for m in ms)
    W = int(x0 + ncols * (cellw + gapc) + right); H = int(yh + nrows * cellh + (54 if has_foot else 12))
    cx = lambda c: x0 + c * (cellw + gapc) + cellw / 2.0
    cy = lambda r: yh + r * cellh + cellh * .5
    body = ''
    if head:
        body += ''.join(MV._text(cx(c), 30, h, 24, _INK) for c, h in enumerate(head))
    if grid:
        for r in range(nrows):
            for c in range(ncols):
                body += ('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="#ffffff" stroke="%s" stroke-width="2.6"/>'
                         % (cx(c) - cellw / 2.0, cy(r) - cellh / 2.0, cellw, cellh, _INK))
    body = '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff" stroke="#ffffff" stroke-width="1"/>' % (W, H) + body   # the full box, so the first layer lands in place
    out = [('line', MV._svg(W, H, body, title))]
    ty = lambda r: cy(r) + size * .36
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'c':
                b += MV._text(cx(m[2]), ty(m[1]), m[3], size, _c28(m[4] if len(m) > 4 else None))
            elif k == 'r':
                cells = list(m[2]) if isinstance(m[2], str) else m[2]
                b += ''.join(MV._text(cx(c), ty(m[1]), t, size, _c28(m[3] if len(m) > 3 else None)) for c, t in enumerate(cells) if t)
            elif k == 'strike':
                r = m[1]
                b += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="4"/>'
                      % (x0 - 2, cy(r), x0 + ncols * (cellw + gapc) - gapc + 2, cy(r), _c28(m[2] if len(m) > 2 else 'red')))
            elif k == 'ring':
                r0, r1 = m[1], m[2]; x = x0 + ncols * (cellw + gapc) + 4
                ya, yb = cy(r0) - cellh * .4, cy(r1) + cellh * .4
                b += ('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="%s" stroke-width="3"/>'
                      % (x, ya, x + 14, ya, x + 14, yb, x, yb, _TEAL))
                b += MV._text(x + 26, (ya + yb) / 2.0 + 10, m[3], 26, _TEAL, 'start')
            elif k == 'note':
                b += MV._text(x0 + ncols * (cellw + gapc) + 10, ty(m[1]) - 2, m[2], 26, _c28(m[3] if len(m) > 3 else 'teal'), 'start')
            elif k == 'glue':
                r, c0, c1 = m[1], m[2], m[3]
                b += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="14" fill="none" stroke="%s" stroke-width="4"/>'
                      % (cx(c0) - cellw / 2.0 - 2, cy(r) - cellh * .46, cx(c1) - cx(c0) + cellw + 4, cellh * .92,
                         _c28(m[4] if len(m) > 4 else 'teal')))
            elif k == 'hl':
                r, c = m[1], m[2]
                hc = m[3] if len(m) > 3 else ''
                b += ('<rect x="%.1f" y="%.1f" width="%d" height="%.1f" rx="8" fill="%s" fill-opacity="0.25" stroke="%s" stroke-width="3"/>'
                      % (cx(c) - cellw / 2.0 + 3, cy(r) - cellh * .44, cellw - 6, cellh * .88,
                         {'orange': '#fbd9b9', 'red': '#f6d0d6'}.get(hc, MV.BAND), {'orange': ORANGE, 'red': _RED28}.get(hc, _TEAL)))
            elif k == 'xc':
                r, c = m[1], m[2]
                b += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="4"/>'
                      % (cx(c) - cellw * .42, cy(r) + cellh * .3, cx(c) + cellw * .42, cy(r) - cellh * .3, _RED28))
            elif k == 'foot':
                b += MV._text(W / 2.0, H - 12, m[1], 28, _c28(m[2] if len(m) > 2 else 'teal'))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def DOTS28(name, labels, layers, R=150, col=0, w=None, title='Points', table=False, size=28, start=-90, pad=70):
    """n points on a circle (clockwise from the top), each with its name outside. layers = [(key, [mark, ...])]:
      ('ln', i, j[, colour[, dashed]])   a line from point i to point j (teal; 'ink' for a side; 'red')
      ('sides',)                         every side of the polygon (ink)
      ('fan', i[, colour])               every line from point i to the points that are not its neighbours (diagonals)
      ('all', i[, colour])               every line from point i to all the other points
      ('mid', text[, colour])            a text in the middle
      ('lab', i, text[, colour])         an extra text by point i
      ('ring', i[, colour])              a ring around point i (the one we start from / fix)
      ('under', text[, colour])          a text under the circle
    table = draw a round table (a light disc) in the base"""
    import math
    n = len(labels); cxx = R + pad + 40; cyy = R + pad; W = int(2 * cxx); H = int(2 * cyy + 40)
    P = [(cxx + R * math.cos(math.radians(start + 360.0 * i / n)), cyy + R * math.sin(math.radians(start + 360.0 * i / n))) for i in range(n)]
    def lab_xy(i, d=40):
        a = math.radians(start + 360.0 * i / n)
        return cxx + (R + d) * math.cos(a), cyy + (R + d) * math.sin(a) + 10
    body = ''
    if table:
        body += '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="2.4"/>' % (cxx, cyy, R * .62, _LIGHT, _INK)
    for i, (x, y) in enumerate(P):
        body += '<circle cx="%.1f" cy="%.1f" r="10" fill="%s"/>' % (x, y, _INK)
        lx, ly = lab_xy(i)
        body += MV._text(lx, ly, labels[i], size, _INK)
    out = [('line', MV._svg(W, H, body, title + ': ' + ', '.join(labels)))]
    def line(i, j, c='teal', dash=False):
        (x1, y1), (x2, y2) = P[i], P[j]
        return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"%s/>'
                % (x1, y1, x2, y2, _c28(c), ' stroke-dasharray="9 7"' if dash else ''))
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'ln':
                b += line(m[1], m[2], m[3] if len(m) > 3 else 'teal', len(m) > 4 and m[4])
            elif k == 'sides':
                b += ''.join(line(i, (i + 1) % n, 'ink') for i in range(n))
            elif k == 'fan':
                b += ''.join(line(m[1], j, m[2] if len(m) > 2 else 'teal') for j in range(n) if j != m[1] and (j - m[1]) % n not in (1, n - 1))
            elif k == 'all':
                b += ''.join(line(m[1], j, m[2] if len(m) > 2 else 'teal') for j in range(n) if j != m[1])
            elif k == 'mid':
                b += MV._text(cxx, cyy + 10, m[1], size + 2, _c28(m[2] if len(m) > 2 else 'teal'))
            elif k == 'lab':
                lx, ly = lab_xy(m[1], 78)
                b += MV._text(lx, ly, m[2], size - 4, _c28(m[3] if len(m) > 3 else 'teal'))
            elif k == 'ring':
                x, y = P[m[1]]
                b += '<circle cx="%.1f" cy="%.1f" r="20" fill="none" stroke="%s" stroke-width="4"/>' % (x, y, _c28(m[2] if len(m) > 2 else 'teal'))
            elif k == 'under':
                b += MV._text(cxx, H - 8, m[1], size, _c28(m[2] if len(m) > 2 else 'teal'))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def POOL28(name, tokens, layers, tok=64, col=0, w=None, title='The pool', size=34):
    """the pool: the items in a rounded frame, in a row. layers = [(key, [mark, ...])]:
      ('pick', i)            a teal disc behind item i (picked now)
      ('gone', i)            item i crossed out (it left the pool)
      ('note', text[, colour])  a text under the pool"""
    n = len(tokens); gap = 14; x0 = 30
    W = int(2 * x0 + n * tok + (n - 1) * gap); H = 150
    cx = lambda i: x0 + i * (tok + gap) + tok / 2.0; cy = 56
    body = ('<rect x="8" y="10" width="%d" height="92" rx="40" fill="%s" stroke="%s" stroke-width="2.6"/>' % (W - 16, _LIGHT, _INK))
    body += ''.join(MV._text(cx(i), cy + size * .36, t, size, _INK) for i, t in enumerate(tokens))
    out = [('line', MV._svg(W, H, body, title + ': ' + ', '.join(tokens)))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'pick':
                b += ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="4"/>' % (cx(m[1]), cy, tok * .46, _TEAL))
            elif k == 'gone':
                x = cx(m[1])
                b += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="5"/>' % (x - 24, cy + 24, x + 24, cy - 24, _RED28) +
                      '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="5"/>' % (x - 24, cy - 24, x + 24, cy + 24, _RED28))
            elif k == 'note':
                b += MV._text(W / 2.0, H - 12, m[1], 26, _c28(m[2] if len(m) > 2 else 'teal'))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)

# lessons whose course title changes with the rewrite (the old stub titles); split lessons get theirs from SPLITS (t28.py hook)
TITLES28 = {}

# ------------------------------------------------------------------------------------------------ wp-123 (camera lesson)
# Hebrew (wp 8290-8392): combinatorics comes from "combination" = a possibility; we count the ways to arrange or to choose,
# by the question's data; type 1 = trial and error, "we counted, we checked" (123, 124, 134, 234); most exam questions
# use a technique, multiplying the possibilities: the options at every stage of choice, then multiply; WHY multiply
# (salad 1 -> 5 drinks, salad 2 -> 5, salad 3 -> 5: 5 + 5 + 5 = 3 x 5); the ORDER of the stages doesn't matter (drink
# first: 3 + 3 + 3 + 3 + 3 = 5 x 3). English (camera lesson, 2-3 examples per idea, numbers differ from the Hebrew and
# from the questions): what counts as a different result (a row, a team, a code); "at most / at least" = topic 21
# (a short reminder); listing in order (24, 27, 47; 8 as a sum of two: 1+7 ... 4+4); the tree of 3 shirts x 2 hats
# BEFORE the rule; the stage boxes; hats first (2 x 3); three stages 4 x 3 x 2 = 24; the adding trap; a locker code
# 4 x 10 = 40 (A0 ... A9, ten codes for each letter). Real exam: 2026_spring_q2_20 (kinds of house: stages),
# 2022_winter_q2_18, 2020_spring_q2_16 (product rule). R37: the product rule is the topic's core method.
c_d1 = LIST28('c_d1', 2, 2, [('r1', [('r', 0, ['Dan', 'Mia'])]), ('r2', [('r', 1, ['Mia', 'Dan']), ('ring', 0, 1, '2 rows')])],
              cellw=110, cellh=50, right=200, w=520, title='A row of two')
c_d2 = I('c_d2', 'A team: $\\ $Dan and Mia $=$ Mia and Dan', size=34)
c_d3 = I('c_d3', 'A code: $\\ 12$ and $21$ are different', size=34)
c_d4 = I('c_d4', 'Does the order matter?', size=36)
c_m1 = I('c_m1', 'At most? $\\ $At least? $\\ $Topic $21$: push to the extreme', size=34)
c_l0 = I('c_l0', 'Two-digit numbers from $2,\\ 4,\\ 7$: $\\ $tens $<$ units', size=34)
c_l1 = LIST28('c_l1', 3, 2, [('a', [('r', 0, '24'), ('note', 0, 'tens 2')]), ('b', [('r', 1, '27'), ('note', 1, 'tens 2')]),
                             ('c', [('r', 2, '47'), ('note', 2, 'tens 4')]),
                             ('e', [('foot', '3 numbers')])], cellw=56, cellh=50, right=170, w=440, title='Listed in order')
c_l2 = IH('c_l2', '$72$: $\\ 7>2$, $\\ $no', size=32, col=1)
c_s0 = I('c_s0', '$8$ as a sum of two whole numbers, $\\ $bigger than $0$', size=34)
c_s1 = LIST28('c_s1', 4, 1, [('a', [('c', 0, 0, '1 + 7')]), ('b', [('c', 1, 0, '2 + 6')]), ('c', [('c', 2, 0, '3 + 5')]),
                             ('d', [('c', 3, 0, '4 + 4')]), ('e', [('foot', '4 ways')])], cellw=150, cellh=50, right=60, w=300,
              title='Smallest first')
c_s2 = IH('c_s2', '$5+3$: $\\ $the same as $3+5$', size=32, col=1)
c_s3 = I('c_s3', 'List in order, $\\ $smallest first.', size=34)
c_t0 = I('c_t0', '$3$ shirts, $\\ 2$ hats. $\\ $How many outfits?', size=34)
c_t1 = TREE28('c_t1', ['shirt 1', 'shirt 2', 'shirt 3'], ['cap', 'sun hat'], [
    ('b0', [('br', 0), ('cnt', 0, '2')]), ('b1', [('br', 1), ('cnt', 1, '2')]), ('b2', [('br', 2), ('cnt', 2, '2')])],
    rowh=46, right=90, w=700, title='3 shirts, 2 hats')
c_t2 = IH('c_t2', '$2+2+2=6$', size=34, col=1)
c_t3 = IH('c_t3', '$3$ groups of $2$: $\\ 3\\times2=6$', size=34, col=1)
c_r0 = I('c_r0', 'A stage of choice: $\\ $a moment where we pick something', size=34)
c_r1 = SLOTS28('c_r1', ['shirt', 'hat'], [('a', [('n', 0, '3')]), ('b', [('n', 1, '2')]), ('x', [('x',)]), ('eq', [('eq', '6')])],
               w=560, title='Two stages')
c_r2 = I('c_r2', 'The options of each stage, $\\ $then multiply.', size=36)
c_h1 = TREE28('c_h1', ['cap', 'sun hat'], ['shirt 1', 'shirt 2', 'shirt 3'], [
    ('b0', [('br', 0), ('cnt', 0, '3')]), ('b1', [('br', 1), ('cnt', 1, '3')])], rowh=42, right=90, w=680, title='Hats first')
c_h2 = IH('c_h2', '$3+3=6$', size=34, col=1)
c_h3 = IH('c_h3', '$2\\times3=3\\times2=6$', size=34, col=1)
c_h4 = I('c_h4', 'The order of the stages does not matter.', size=34)
c_e0 = I('c_e0', '$4$ sandwiches, $\\ 3$ drinks, $\\ 2$ desserts. $\\ $One of each.', size=34)
c_e1 = SLOTS28('c_e1', ['sandwich', 'drink', 'dessert'], [('a', [('n', 0, '4')]), ('b', [('n', 1, '3')]), ('c', [('n', 2, '2')]),
                                                       ('x', [('x',)]), ('eq', [('eq', '24')])], w=800, title='Three stages')
c_e2 = IH('c_e2', '$4\\times3=12$ pairs', size=34)
c_e3 = IH('c_e3', '$12\\times2=24$ meals', size=34)
c_e4 = IH('c_e4', '$4+3+2=9$: $\\ $items on the menu, $\\ $not meals', size=32)
c_e5 = IH('c_e5', '$3$ shirts $+\\ 2$ hats $=5$ items, $\\ $but $6$ outfits', size=32)
c_k0 = I('c_k0', 'A locker code: $\\ $a letter A to D, $\\ $then a digit $0$ to $9$', size=34)
c_k1 = LIST28('c_k1', 1, 10, [('a', [('r', 0, ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'])]),
                              ('b', [('note', 0, '10 codes')])], cellw=68, cellh=56, right=150, gapc=2, w=880, size=36,
              title='The codes that start with A')
c_k2 = IH('c_k2', 'B: $\\ 10$, $\\ $C: $\\ 10$, $\\ $D: $\\ 10$', size=32)
c_k3 = SLOTS28('c_k3', ['letter', 'digit'], [('a', [('n', 0, '4')]), ('b', [('n', 1, '10')]), ('x', [('x',)]), ('eq', [('eq', '40')])],
               w=560, title='Two stages')
c_z1 = I('c_z1', 'A short list: $\\ $list in order, $\\ $and count.', size=34)
c_z2 = I('c_z2', 'Stages: $\\ $the options in each box, $\\ $multiply.', size=34)
c_z3 = I('c_z3', 'Never add the stages.', size=34)
_wp123 = [
    S('Counting Possibilities',
      L("Welcome back, and now a new topic, counting possibilities."),
      L("In these questions we count how many ways there are to arrange something, or to choose something. We always "
        "count according to the data in the question."),
      L("The math name for this is combinatorics. It comes from the word combination, and a combination is simply one "
        "possibility."),
      L("Counting questions come up in almost every exam. So let's learn them step by step.")),
    S('What is a different result?',
      L("Before we count anything, we decide what counts as a different result."),
      L("Two friends, Dan and Mia, stand in a row. Dan, then Mia, is one row.", show(c_d1['line'], 'Two friends, Dan and Mia'),
        show(c_d1['r1'], 'Dan, then Mia, is one row')),
      L("Mia, then Dan, is another row. We swapped them, so the order changed. So here we have two different rows.",
        show(c_d1['r2'], 'Mia, then Dan, is another row')),
      L("Now we pick the same two friends for a team. Dan and Mia is the same team as Mia and Dan. The order doesn't "
        "matter in a team.", show(c_d2, 'Dan and Mia is the same team')),
      L("And in a code, one two and two one are different codes, because the digits are in different places.",
        show(c_d3, 'one two and two one are different codes')),
      L("So in every question, first ask yourself one thing. Does the order matter? We'll come back to this question "
        "all through the topic.", show(c_d4, 'Does the order matter'))),
    S('At most? At least?',
      L("One more thing before we start. Some questions with the same kind of story ask at most how many, or at least "
        "how many."),
      L("Those are not counting questions. They are the extreme questions from topic twenty-one. Remember, we push to "
        "the extreme, and we give the others as little as possible.", show(c_m1, 'They are the extreme questions')),
      L("So when you see at most or at least, use the topic twenty-one way. Everything else in this topic, we count.")),
    S('Listing in order',
      L("The first way to count is the simplest one. We just write the options, check which ones fit, and count them. "
        "This is trial and error."),
      L("Let's see an example. How many two-digit numbers can we make from the digits two, four and seven, if the tens "
        "digit is smaller than the units digit?", show(c_l0, 'How many two-digit numbers can we make')),
      L("We list them in order, with the smallest tens digit first. The tens digit is two. Then the units digit can be "
        "four, so twenty-four.", show(c_l1['line'], 'We list them in order'), show(c_l1['a'], 'so twenty-four')),
      L("Or the units digit can be seven, so twenty-seven. Both units digits are bigger than two, so both numbers fit.",
        show(c_l1['b'], 'so twenty-seven')),
      L("Now the tens digit is four. The units digit must be bigger than four, so only seven. That's forty-seven.",
        show(c_l1['c'], "That's forty-seven")),
      L("And the tens digit seven? No digit here is bigger than seven. So seventy-two, for example, doesn't fit.",
        show(c_l2, 'seventy-two, for example')),
      L("So there are three numbers. What did we do? We counted, and we checked.", show(c_l1['e'], 'So there are three numbers'))),
    S('Listing without repeats',
      L("Now another example. In how many ways can we write eight as a sum of two whole numbers bigger than zero? The "
        "order doesn't matter here.", show(c_s0, 'In how many ways can we write eight')),
      L("Again we list in order. We start with the smallest first number, one. One plus seven.",
        show(c_s1['line'], 'Again we list in order'), show(c_s1['a'], 'One plus seven')),
      L("Then two plus six, and three plus five.", show(c_s1['b'], 'Then two plus six'), show(c_s1['c'], 'three plus five')),
      L("Then four plus four. Four plus four is eight, so it fits too.", show(c_s1['d'], 'Then four plus four')),
      L("What about five plus three? It's the same as three plus five, and the order doesn't matter. So we stop here.",
        show(c_s2, 'What about five plus three')),
      L("So there are four ways.", show(c_s1['e'], 'So there are four ways')),
      L("That's why we list in order, smallest first. Nothing is missed, and nothing is counted twice.",
        show(c_s3, 'smallest first')),
      L("Listing works well when the list is short. When the list is long, we need a faster way.")),
    S('Why we multiply',
      L("Now the main tool of the topic, multiplying the possibilities. Let's see it on a tiny example first."),
      L("Lia has three shirts and two hats, a cap and a sun hat. An outfit is one shirt and one hat. How many outfits can "
        "she make?", show(c_t0, 'Lia has three shirts and two hats')),
      L("Let's draw it. Here are the three shirts.", show(c_t1['line'], 'Here are the three shirts')),
      L("Say she picks shirt one. With it, she can wear the cap, or the sun hat. That's two outfits.",
        show(c_t1['b0'], 'Say she picks shirt one')),
      L("Now shirt two. Again, the cap or the sun hat. Two more outfits.", show(c_t1['b1'], 'Now shirt two')),
      L("And shirt three, the same. Two more.", show(c_t1['b2'], 'And shirt three')),
      L("So we have two, plus two, plus two. That's six outfits.", show(c_t2, 'two, plus two, plus two')),
      L("Two plus two plus two is three groups of two. And three groups of two is three times two. That's why we "
        "multiply.", show(c_t3, 'three groups of two is three times two'))),
    S('Stages of choice',
      L("So here's the rule. A stage of choice is a moment where we pick something.", show(c_r0, 'A stage of choice is')),
      L("Lia has two stages. Stage one is the shirt, with three options. We write three in its box.",
        show(c_r1['line'], 'Lia has two stages'), show(c_r1['a'], 'We write three in its box')),
      L("Stage two is the hat, with two options. We write two in its box.", show(c_r1['b'], 'We write two in its box')),
      L("Then we multiply the options. Three times two is six outfits. It's the same six we counted on the tree.",
        show(c_r1['x'], 'Then we multiply the options'), show(c_r1['eq'], 'Three times two is six')),
      L("So we count the options at each stage, and we multiply them.", show(c_r2, 'we count the options at each stage'))),
    S('Which stage first?',
      L("Does it matter which stage we write first? Let's check. This time Lia picks the hat first.",
        show(c_h1['line'], 'Lia picks the hat first')),
      L("With the cap, she can wear any of the three shirts. That's three outfits.", show(c_h1['b0'], 'With the cap')),
      L("With the sun hat, again three shirts. Three more outfits.", show(c_h1['b1'], 'With the sun hat')),
      L("Three plus three is six. The same six outfits.", show(c_h2, 'Three plus three is six')),
      L("Two times three is the same as three times two. In multiplication, the order doesn't change the result.",
        show(c_h3, 'Two times three is the same')),
      L("So the order of the stages doesn't matter. Write the stages in any order, and you get the same answer.",
        show(c_h4, 'the order of the stages'))),
    S('Three stages',
      L("Now a new example, with three stages. A cafe sells four kinds of sandwich, three drinks and two desserts. A meal "
        "is one of each. How many meals are possible?", show(c_e0, 'A cafe sells four kinds of sandwich')),
      L("Three stages, three boxes. The sandwich has four options, the drink three, and the dessert two.",
        show(c_e1['line'], 'Three stages, three boxes'), show(c_e1['a'], 'The sandwich has four options'),
        show(c_e1['b'], 'the drink three'), show(c_e1['c'], 'and the dessert two')),
      L("Why multiply again? Each of the four sandwiches goes with each of the three drinks. Four times three is twelve "
        "pairs.", show(c_e2, 'Four times three is twelve')),
      L("And each of those twelve pairs goes with each of the two desserts. Twelve times two is twenty-four.",
        show(c_e3, 'Twelve times two is twenty-four')),
      L("So we multiply all three boxes. Four times three times two is twenty-four meals.",
        show(c_e1['x'], 'So we multiply all three boxes'), show(c_e1['eq'], 'is twenty-four meals')),
      L("Careful here. A lot of students add the numbers. Four plus three plus two is nine.",
        show(c_e4, 'Four plus three plus two is nine')),
      L("But nine counts the items on the menu, not the meals. Remember Lia. Three shirts plus two hats is five items, "
        "but she had six outfits.", show(c_e5, 'Three shirts plus two hats is five items'))),
    S('A code in two stages',
      L("One more example. A locker code is one letter from A to D, and then one digit from zero to nine. How many codes "
        "are possible?", show(c_k0, 'A locker code is one letter')),
      L("Let's see the codes that start with A. A zero, A one, and so on up to A nine. That's ten codes.",
        show(c_k1['line'], "Let's see the codes that start with A"), show(c_k1['a'], 'A zero, A one'),
        show(c_k1['b'], "That's ten codes")),
      L("The codes that start with B are ten more, and so are C and D.", show(c_k2, 'The codes that start with B')),
      L("So four letters, and ten digits for each letter. Four times ten is forty codes.",
        show(c_k3['line'], 'So four letters'), show(c_k3['a'], 'So four letters'), show(c_k3['b'], 'and ten digits'),
        show(c_k3['x'], 'Four times ten'), show(c_k3['eq'], 'is forty codes'))),
    S('Recap',
      L("So let's sum it up. If the list is short, we list it in order, and we count.", show(c_z1, 'we list it in order')),
      L("If it's long, we work in stages. We write the number of options in each box, and we multiply.",
        show(c_z2, 'we work in stages')),
      L("And we never add the stages. Adding counts the items, not the results.", show(c_z3, 'we never add the stages')),
      L("Take a moment to memorize this. Now try the first question, and I'll see you in the next video.")),
]
video('wp-123', 'lesson', slides=_wp123)
CAMERA_SPLIT = ('wp-123', 'Counting Possibilities', [
    (1, None),
    (5, "Let's continue with counting.")])

# ------------------------------------------------------------------------------------------------ g124 (digits going up)
# Hebrew (wp 8303-8333, digits 1-4 going up: 123, 124, 134, 234): "what do we do? we just check... we counted, we
# checked". English: digits 3, 5, 6, 9 (the Hebrew-vs-English report keeps the added insight: choose the one digit left
# out). First question of the topic: listing in order, like in the camera lesson (part 1). Trap at its step: 24 counts
# every order of three digits.
g4L = LIST28('g4L', 4, 3, [('a', [('r', 0, '356')]), ('b', [('r', 1, '359')]), ('c', [('r', 2, '369')]), ('d', [('r', 3, '569')]),
                           ('e', [('foot', '4 numbers')])], cellw=46, cellh=48, right=40, gapc=6, w=230, title='Going up, in order')
g4a = IH('g4a', '$3,\\ 9$: $\\ $nothing above $9$', size=30, col=1)
g4b = IH('g4b', '$6$ first: $\\ $only $9$ is bigger, $\\ $no', size=30, col=1)
g4O = LIST28('g4O', 4, 1, [('a', [('c', 0, 0, 'leave out 3:  569')]), ('b', [('c', 1, 0, 'leave out 5:  369')]),
                           ('c', [('c', 2, 0, 'leave out 6:  359')]), ('d', [('c', 3, 0, 'leave out 9:  356')])],
             cellw=330, cellh=48, right=20, w=400, size=30, title='The digit left out')
g4c = IH('g4c', '$356$: $\\ $only one order goes up', size=30, col=1)
g4d = IH('g4d', '$4\\times3\\times2=24$: $\\ $every order', size=30, col=1)
video('solve-wp28-g124', 'solution', qid='wp28-g124', slides=[
    S('Method 1 · The math way: listing',
      L("How many three-digit numbers can be made from the digits three, five, six and nine, if the hundreds digit is "
        "smaller than the tens digit, and the tens digit is smaller than the units digit?",
        pt('stem', 'How many three-digit numbers', 'hl', 9.0), voice='calm', pause=0.5),
      L("So every digit must be bigger than the digit before it. The digits go up, from left to right. We have only four "
        "digits, so the list will be short.", pt('stem: given', 'every digit must be bigger')),
      L("We'll solve it in two different ways. Let's start with the math way, by listing, like in the lesson. We list in "
        "order, with the smallest hundreds digit first.", show(g4L['line'], 'We list in order')),
      L("The hundreds digit is three. Then the tens digit must be bigger than three, so five, six or nine."),
      L("Three and five, and then a units digit bigger than five. That's six or nine. So three hundred fifty-six, and "
        "three hundred fifty-nine.", show(g4L['a'], 'So three hundred fifty-six'), show(g4L['b'], 'three hundred fifty-nine')),
      L("Three and six, and then a units digit bigger than six. That's only nine. So three hundred sixty-nine.",
        show(g4L['c'], 'So three hundred sixty-nine')),
      L("Three and nine? No digit is bigger than nine, so nothing works here.", show(g4a, 'Three and nine')),
      L("Now the hundreds digit is five. The tens digit is six, and the units digit is nine. That's five hundred "
        "sixty-nine.", show(g4L['d'], "That's five hundred sixty-nine")),
      L("Can the hundreds digit be six? Then we need two bigger digits after it. But only nine is bigger than six, so no. "
        "And nine can't start a number here either.", show(g4b, 'Can the hundreds digit be six')),
      L("So there are four numbers. What did we do? We counted, and we checked.", show(g4L['e'], 'So there are four numbers'))),
    S('Method 2 · Insight: the digit left out',
      L("[pause] Now the insight. Every number here uses three of the four digits. And three different digits can go up "
        "in only one order, smallest first.", show(g4c, 'only one order')),
      L("So choosing the number is the same as choosing the three digits. And that's the same as choosing the one digit "
        "we leave out.", show(g4O['line'], 'the one digit')),
      L("We can leave out three, and then the number is five hundred sixty-nine.", show(g4O['a'], 'We can leave out three')),
      L("Or we leave out five, or six, or nine. Each time, one number.", show(g4O['b'], 'Or we leave out five'),
        show(g4O['c'], 'or six'), show(g4O['d'], 'or nine')),
      L("Four digits to leave out, so four numbers again."),
      L("Choice number two, twenty-four, is a trap. Four times three times two counts every order of three digits. But "
        "only one of those orders goes up.", show(g4d, 'Four times three times two'), mk('cross', 'choice 2', 'is a trap')),
      L("Choice number four is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-124-after (lesson: restrictions)
# Hebrew (wp 8393-8469, the employee number: sum 10 -> the first digit can't be 0, "10 is not a digit, it's a number",
# the second digit is forced, 9 x 1, the mistake 9 x 9, "imagine you picked, then ask what completes it"; wp 9325
# "there is no number 076"). The old stub "Multiply the Choices" ("let's see it in two questions") becomes a real R37
# lesson (exam-coverage audit, gap 3): no leading zero (90 two-digit numbers, checked by 99 - 10 + 1), the most
# restricted stage first (450 even three-digit numbers, checked by half of 900), a forced stage gets 1 (sum 11 -> 8,
# listed; units twice the tens -> 4, listed). New numbers (not her sum 10, not g126's sum 14).
r_a0 = I('r_a0', 'Two-digit numbers', size=36)
r_a1 = SLOTS28('r_a1', ['tens', 'units'], [('a', [('n', 0, '9'), ('sub', 0, '1 to 9')]), ('b', [('n', 1, '10'), ('sub', 1, '0 to 9')]),
                                           ('x', [('x',)]), ('eq', [('eq', '90')])], sub=1, w=560, title='Two-digit numbers')
r_a2 = IH('r_a2', '$07$? $\\ $We just write $7$', size=32, col=1)
r_a3 = IH('r_a3', '$9\\times10=90$', size=32, col=1)
r_a4 = IH('r_a4', '$10$ to $99$: $\\ 99-10+1=90$', size=32, col=1)
r_b0 = I('r_b0', 'Three-digit even numbers', size=36)
r_b1 = SLOTS28('r_b1', ['hundreds', 'tens', 'units'], [('u', [('n', 2, '5'), ('sub', 2, '0 2 4 6 8'), ('hl', 2)]),
                                                     ('h', [('n', 0, '9'), ('sub', 0, '1 to 9')]),
                                                     ('t', [('n', 1, '10'), ('sub', 1, '0 to 9')]),
                                                     ('x', [('x',)]), ('eq', [('eq', '450')])], sub=1, w=820, title='Three-digit even numbers')
r_b2 = IH('r_b2', '$9\\times10=90$', size=32, col=1)
r_b3 = IH('r_b3', '$90\\times5=450$', size=32, col=1)
r_b4 = IH('r_b4', '$100$ to $999$: $\\ 900$ numbers, $\\ $half even: $\\ 450$', size=32, col=1)
r_c0 = I('r_c0', 'Two-digit numbers, $\\ $digit sum $11$', size=36)
r_c1 = IH('r_c1', '$0+11$? $\\ 11$ is a number, $\\ $not a digit', size=32)
r_c2 = IH('r_c2', '$1+10$? $\\ $no', size=32)
r_c3 = SLOTS28('r_c3', ['first', 'second'], [('a', [('n', 0, '8'), ('sub', 0, '2 to 9')]), ('b', [('n', 1, '1', 'teal'), ('sub', 1, 'forced')]),
                                             ('x', [('x',)]), ('eq', [('eq', '8')])], sub=1, w=520, title='Digit sum 11')
r_c4 = IH('r_c4', 'first $6$: $\\ $second $11-6=5$', size=32, col=1)
r_c5 = IH('r_c5', 'first $9$: $\\ $second $11-9=2$', size=32, col=1)
r_c6 = LIST28('r_c6', 1, 8, [('a', [('r', 0, ['29', '38', '47', '56', '65', '74', '83', '92'])])], cellw=54, cellh=48, right=10,
              gapc=8, w=520, size=30, title='The list')
r_c7 = IH('r_c7', '$8\\times10=80$? $\\ $No: $\\ $the second stage has $1$', size=32, col=1)
r_d0 = I('r_d0', 'Two-digit numbers: $\\ $units $=2\\times$ tens', size=36)
r_d1 = IH('r_d1', 'tens $5$: $\\ 2\\times5=10$, $\\ $no', size=32, col=1)
r_d2 = SLOTS28('r_d2', ['tens', 'units'], [('a', [('n', 0, '4'), ('sub', 0, '1 to 4')]), ('b', [('n', 1, '1', 'teal'), ('sub', 1, 'forced')]),
                                           ('x', [('x',)]), ('eq', [('eq', '4')])], sub=1, w=520, title='Units twice the tens')
r_d3 = LIST28('r_d3', 1, 4, [('a', [('r', 0, ['12', '24', '36', '48'])])], cellw=58, cellh=48, right=10, gapc=10, w=300, size=30,
              title='The list')
r_z1 = I('r_z1', 'A number never starts with $0$.', size=34)
r_z2 = I('r_z2', 'Start with the most restricted stage.', size=34)
r_z3 = I('r_z3', 'A forced stage gets $1$.', size=34)
TITLES28['wp-124-after'] = 'Restrictions and Forced Choices'
video('wp-124-after', 'lesson', slides=[
    S('Restrictions and Forced Choices',
      L("In the first lesson we counted in stages. Now let's see what happens when a stage has a restriction."),
      L("Restrictions are what make counting questions hard. So we'll go slowly, with three kinds of restriction.")),
    S('No zero in front',
      L("The first restriction is a number can't start with zero. Let's count all the two-digit numbers.", show(r_a0, 'all the two-digit numbers')),
      L("Two stages, the tens digit and the units digit.", show(r_a1['line'], 'Two stages')),
      L("Can the tens digit be zero? No. There is no number zero seven. We just write seven, and that's a one-digit "
        "number.", show(r_a2, 'There is no number zero seven')),
      L("So the tens digit is one to nine. That's nine options.", show(r_a1['a'], "That's nine options")),
      L("The units digit has no restriction. It can be anything from zero to nine. That's ten options.",
        show(r_a1['b'], "That's ten options")),
      L("Nine times ten is ninety. So there are ninety two-digit numbers.", show(r_a1['x'], 'Nine times ten'),
        show(r_a3, 'Nine times ten is ninety'), show(r_a1['eq'], 'So there are ninety')),
      L("Let's check it another way. The two-digit numbers go from ten to ninety-nine. Ninety-nine minus ten, plus one, "
        "is ninety. The same answer.", show(r_a4, 'Ninety-nine minus ten'))),
    S('The hardest stage first',
      L("Now a new example. How many three-digit numbers are even?", show(r_b0, 'How many three-digit numbers are even')),
      L("Three stages, the hundreds, the tens and the units.", show(r_b1['line'], 'Three stages')),
      L("Which stage has the restriction? An even number ends in an even digit. So the units digit is the one with the "
        "restriction. We start with it."),
      L("The units digit can be zero, two, four, six or eight. That's five options.", show(r_b1['u'], "That's five options")),
      L("The hundreds digit can't be zero, so one to nine. Nine options.", show(r_b1['h'], 'so one to nine')),
      L("And the tens digit is free. Ten options.", show(r_b1['t'], 'the tens digit is free')),
      L("Nine times ten is ninety. Then ninety times five is four hundred fifty.", show(r_b1['x'], 'Nine times ten is ninety'),
        show(r_b2, 'Nine times ten is ninety'), show(r_b3, 'ninety times five'), show(r_b1['eq'], 'is four hundred fifty')),
      L("A check. There are nine hundred three-digit numbers, from a hundred to nine hundred ninety-nine. Half of them "
        "are even, and half of nine hundred is four hundred fifty.", show(r_b4, 'There are nine hundred three-digit numbers')),
      L("So always start with the stage that has the restriction. The free stages can wait, because they work with "
        "anything.")),
    S('One choice decides another',
      L("The third restriction is the hardest one. Sometimes one choice decides another choice."),
      L("Let's see it. How many two-digit numbers have a digit sum of eleven? That means the two digits add up to "
        "eleven.", show(r_c0, 'How many two-digit numbers have a digit sum')),
      L("We start with the first digit. Can it be zero? Then the second digit would need to be eleven. But eleven is a "
        "number, not a digit.", show(r_c1, 'Can it be zero')),
      L("Can it be one? Then the second digit would need to be ten, and ten isn't a digit either.", show(r_c2, 'Can it be one')),
      L("Two works, because two plus nine is eleven. So the first digit is two to nine. That's eight options.",
        show(r_c3['line'], 'So the first digit is two to nine'), show(r_c3['a'], "That's eight options")),
      L("Now the second digit. Imagine we already picked the first digit, say six. What completes six to eleven? Only "
        "five.", show(r_c4, 'say six')),
      L("And if we picked nine? Only two completes it. Whatever we pick first, exactly one digit completes it.",
        show(r_c5, 'if we picked nine')),
      L("So the second stage is forced. It has one option. Eight times one is eight.", show(r_c3['b'], 'It has one option'),
        show(r_c3['x'], 'Eight times one'), show(r_c3['eq'], 'Eight times one is eight')),
      L("Let's list them to see it. Twenty-nine, thirty-eight, forty-seven, and so on up to ninety-two. Eight numbers.",
        show(r_c6['line'], "Let's list them"), show(r_c6['a'], 'Twenty-nine, thirty-eight')),
      L("Careful here. A lot of students give the second digit ten options, or eight. But the second digit isn't free. It "
        "depends on the first one, so it gets one.", show(r_c7, 'A lot of students'))),
    S('Another forced stage',
      L("One more example. How many two-digit numbers have a units digit that is twice the tens digit?",
        show(r_d0, 'How many two-digit numbers have a units digit')),
      L("The tens digit first. It can't be zero. Can it be five? Two times five is ten, and ten isn't a digit.",
        show(r_d1, 'Can it be five')),
      L("So the tens digit is one, two, three or four. Four options.", show(r_d2['line'], 'So the tens digit is one'),
        show(r_d2['a'], 'Four options')),
      L("Once we pick the tens digit, the units digit is forced. It must be twice the tens digit. One option.",
        show(r_d2['b'], 'One option')),
      L("Four times one is four. And here they are, twelve, twenty-four, thirty-six and forty-eight.",
        show(r_d2['x'], 'Four times one'), show(r_d2['eq'], 'Four times one is four'), show(r_d3['line'], 'And here they are'),
        show(r_d3['a'], 'twelve, twenty-four'))),
    S('Recap',
      L("So let's sum it up. A number never starts with zero.", show(r_z1, 'A number never starts with zero')),
      L("Start with the stage that has the restriction.", show(r_z2, 'Start with the stage')),
      L("And if one choice decides another, imagine you already picked the first one. Then ask what completes it. The "
        "forced stage gets one.", show(r_z3, 'The forced stage gets one')),
      L("Take a moment to memorize this, and I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ g125 (soups and breads)
# Hebrew (wp 8338-8392, the salad bar 3 x 5 = 15): the options per stage, multiply; why (5 + 5 + 5); the order of the
# stages doesn't matter (5 x 3). English: 7 soups x 3 breads = 21. First question after the camera lesson's product
# rule: applied slowly, "like in the lesson"; the why on a small piece of the tree (soup 1 -> 3 lunches); the trap 10 =
# adding, at its step.
g5S = SLOTS28('g5S', ['soup', 'bread'], [('a', [('n', 0, '7')]), ('b', [('n', 1, '3')]), ('x', [('x',)]), ('eq', [('eq', '21')])],
              w=520, title='Two stages')
g5T = TREE28('g5T', ['soup 1', 'soup 2'], ['bread 1', 'bread 2', 'bread 3'], [('b0', [('br', 0), ('cnt', 0, '3')]),
                                                                            ('b1', [('br', 1), ('cnt', 1, '3')])],
             rowh=40, right=80, w=420, col=1, title='Each soup, three breads')
g5a = IH('g5a', '$3+3+3+...$: $\\ 7$ times', size=30, col=1)
g5b = IH('g5b', '$7\\times3=21$', size=32)
g5c = IH('g5c', '$7+3=10$: $\\ $menu items', size=30)
g5d = IH('g5d', '$3\\times7=21$', size=32)
video('solve-wp28-g125', 'solution', qid='wp28-g125', slides=[
    S('Method 1 · The math way: stages of choice',
      L("A food truck offers seven soups and three kinds of bread. A lunch contains one soup and one kind of bread. How "
        "many different lunches are possible?", pt('stem', 'A food truck offers', 'hl', 8.0), voice='calm', pause=0.5),
      L("So they ask how many lunches, not how many items. A lunch is a pair, one soup and one bread.",
        pt('stem: ask', 'So they ask how many lunches')),
      L("Let's solve it the math way, in stages, like in the lesson. We have two stages of choice, the soup and the bread.",
        show(g5S['line'], 'two stages of choice')),
      L("The soup has seven options. We write seven in its box.", show(g5S['a'], 'We write seven in its box')),
      L("The bread has three options. We write three in its box.", show(g5S['b'], 'We write three in its box')),
      L("Why do we multiply? Take the first soup. With it, we can take any of the three breads. That's three lunches.",
        show(g5T['line'], 'Take the first soup'), show(g5T['b0'], "That's three lunches")),
      L("The second soup also goes with three breads. Three more lunches.", show(g5T['b1'], 'The second soup')),
      L("And so on for all seven soups. Three lunches for each soup, seven times.", show(g5a, 'Three lunches for each soup')),
      L("Three, seven times, is seven times three. That's twenty-one lunches.", show(g5S['x'], 'is seven times three'),
        show(g5b, "That's twenty-one lunches"), show(g5S['eq'], "That's twenty-one lunches")),
      L("Careful here. A lot of students add, seven plus three is ten. That's choice number one. But ten counts the items "
        "on the menu, not the lunches.", show(g5c, 'seven plus three is ten'), mk('cross', 'choice 1', "That's choice number one")),
      L("And if we start with the bread? Each bread goes with seven soups. Three times seven is twenty-one again. The "
        "order of the stages doesn't matter.", show(g5d, 'Three times seven is twenty-one')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g126 (locker number, sum 14)
# Hebrew (wp 8393-8457, the employee number, digit sum 10): the first digit can't be 0, "10 is not a digit, it's a
# number", 9 options; imagine we picked 6: only 4 completes it; the second choice depends on the first: 1 option; 9 x 1;
# the common mistake 9 x 9; "imagine you picked, then think what completes it". English: digit sum 14 -> 5 x 1 = 5 (the
# report keeps "14 is a number, not a digit", the forced second digit, the 5 x 5 mistake, the listing check, 59 and 95
# both counted, 77 once). The forced stage: like in the lesson (wp-124-after).
g6S = SLOTS28('g6S', ['first', 'second'], [('a', [('n', 0, '5'), ('sub', 0, '5 to 9')]), ('b', [('n', 1, '1', 'teal'), ('sub', 1, 'forced')]),
                                           ('x', [('x',)]), ('eq', [('eq', '5')])], sub=1, w=500, title='Digit sum 14')
g6a = IH('g6a', '$0+14$? $\\ 14$ is not a digit', size=30)
g6b = IH('g6b', '$1+13,\\ 2+12,\\ 3+11,\\ 4+10$: $\\ $no', size=30)
g6c = IH('g6c', '$5+9=14$', size=30, col=1)
g6d = IH('g6d', 'first $6$: $\\ $second $14-6=8$', size=30, col=1)
g6e = IH('g6e', 'first $9$: $\\ $second $14-9=5$', size=30, col=1)
g6f = IH('g6f', '$5\\times5=25$: $\\ $the trap', size=30, col=1)
g6L = LIST28('g6L', 1, 5, [('a', [('r', 0, ['59', '68', '77', '86', '95'])]), ('b', [('note', 0, '5 numbers')])],
             cellw=60, cellh=50, right=170, gapc=10, w=560, size=32, title='The list')
g6g = IH('g6g', '$59\\ne95$', size=30)
video('solve-wp28-g126', 'solution', qid='wp28-g126', slides=[
    S('Method 1 · The math way: stages of choice',
      L("A locker number has two digits, each from zero to nine. The sum of the two digits must be fourteen. How many "
        "locker numbers are possible?", pt('stem', 'A locker number has two digits', 'hl', 8.0), voice='calm', pause=0.5),
      L("So the two digits must add up to fourteen. This is the restriction from the lesson, where one choice decides "
        "another.", pt('stem: given', 'the two digits must add up to fourteen')),
      L("We'll solve it in two different ways. Let's start with the math way, in stages. Stage one is the first digit, "
        "and stage two is the second digit.", show(g6S['line'], 'Stage one is the first digit')),
      L("Can the first digit be zero? Then the second digit would need to be fourteen. But fourteen is a number, not a "
        "digit.", show(g6a, 'Can the first digit be zero')),
      L("What about one, two, three or four? They would need thirteen, twelve, eleven or ten. None of those is a digit.",
        show(g6b, 'What about one, two, three or four')),
      L("Five works, because five plus nine is fourteen. So the first digit is five, six, seven, eight or nine. That's "
        "five options.", show(g6c, 'five plus nine is fourteen'), show(g6S['a'], "That's five options")),
      L("Now the second digit. Imagine we picked six first. What completes six to fourteen? Only eight.",
        show(g6d, 'Imagine we picked six first')),
      L("Picked nine? Only five completes it. Whatever we pick first, exactly one digit completes it.",
        show(g6e, 'Picked nine')),
      L("So the second stage is forced, and it gets one option. Five times one is five.", show(g6S['b'], 'it gets one option'),
        show(g6S['x'], 'Five times one'), show(g6S['eq'], 'Five times one is five')),
      L("This is where many students slip. They give the second digit five options too, and five times five is "
        "twenty-five. That's choice number two. But the second digit isn't free. It depends on the first one.",
        show(g6f, 'five times five is twenty-five'), mk('cross', 'choice 2', "That's choice number two"))),
    S('Method 2 · The math way: listing',
      L("[pause] Now a second way, by listing. The list is short, so we can write it all."),
      L("We start with the smallest first digit, five. Fifty-nine. Then sixty-eight, seventy-seven, eighty-six and "
        "ninety-five.", show(g6L['line'], 'We start with the smallest first digit'), show(g6L['a'], 'Fifty-nine')),
      L("Fifty-nine and ninety-five are two different locker numbers, because the digits are in different places. So we "
        "count both.", show(g6g, 'Fifty-nine and ninety-five')),
      L("And seventy-seven is allowed. Nothing says the digits must be different. We count it once. If you skip it, you "
        "get four, choice number four.", mk('cross', 'choice 4', 'you get four')),
      L("So there are five locker numbers again.", show(g6L['b'], 'So there are five locker numbers')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-127 (lesson: the pool)
# Hebrew (wp 8471-8626): we choose from a pool (digits 0-9, or what the question allows); check whether the item picked
# left the pool or can be picked again; with repetition (1-5: 5 x 5 x 5 = 125, "the 3 goes back into the pool");
# without (5 x 4 x 3 = 60, "the 3 didn't come back... the pool shrank"; "if I had to pick another, only 2 options");
# items in a row = without repetition (5 books: 5 x 4 x 3 x 2 x 1 = 120); the ! sign = factorial (5!, 4!, 100!); n
# items in a row = n!; "we'll use it in the formulas of later types"; recap: with = the pool stays, without = it
# shrinks, a row is the special case of without. The old stub becomes a real R37 lesson: the tiny case of codes from
# 1, 2, 3 LISTED both ways (9, then 6 with 11, 22, 33 crossed out) BEFORE the rule; letters A-F (216 / 120); the six
# orders of A, B, C listed before 3 x 2 x 1; four mugs = 4!; 3!, 4!, 5! (new numbers: not her 1-5 digits, not 5 books).
p_p0 = POOL28('p_p0', ['1', '2', '3'], [('pick', [('pick', 0)]), ('note', [('note', 'it goes back')])], w=300, col=1, title='The pool')
p_L1 = LIST28('p_L1', 3, 3, [('a', [('c', 0, 0, '11'), ('c', 0, 1, '12'), ('c', 0, 2, '13')]),
                             ('b', [('c', 1, 0, '21'), ('c', 1, 1, '22'), ('c', 1, 2, '23')]),
                             ('c', [('c', 2, 0, '31'), ('c', 2, 1, '32'), ('c', 2, 2, '33')]), ('d', [('foot', '9 codes')])],
              cellw=80, cellh=50, right=20, w=330, title='Codes from 1, 2, 3, with repeats')
p_s1 = SLOTS28('p_s1', ['1st', '2nd'], [('a', [('n', 0, '3')]), ('b', [('n', 1, '3')]), ('x', [('x',)]), ('eq', [('eq', '9')])],
               w=440, title='With repetition')
p_p1 = POOL28('p_p1', ['1', '2', '3'], [('gone', [('gone', 0)]), ('note', [('note', '2 left')])], w=300, col=1, title='The pool')
p_L2 = LIST28('p_L2', 3, 3, [('a', [('c', 0, 0, '11'), ('c', 0, 1, '12'), ('c', 0, 2, '13'), ('c', 1, 0, '21'), ('c', 1, 1, '22'),
                                    ('c', 1, 2, '23'), ('c', 2, 0, '31'), ('c', 2, 1, '32'), ('c', 2, 2, '33')]),
                             ('x', [('xc', 0, 0), ('xc', 1, 1), ('xc', 2, 2)]),
                             ('d', [('foot', '9 − 3 = 6 codes')])],
              cellw=80, cellh=50, right=20, w=330, title='Codes from 1, 2, 3, no repeats')
p_s2 = SLOTS28('p_s2', ['1st', '2nd'], [('a', [('n', 0, '3')]), ('b', [('n', 1, '2')]), ('x', [('x',)]), ('eq', [('eq', '6')])],
               w=440, title='Without repetition')
p_b0 = I('p_b0', 'Codes of $3$ letters, $\\ $from A, B, C, D, E, F', size=34)
p_b1 = SLOTS28('p_b1', ['1st', '2nd', '3rd'], [('a', [('n', 0, '6'), ('n', 1, '6'), ('n', 2, '6')]), ('x', [('x',)]), ('eq', [('eq', '216')])],
               w=700, title='Letters may repeat')
p_b2 = IH('p_b2', '$6\\times6=36$, $\\ 36\\times6=216$', size=32)
p_b3 = SLOTS28('p_b3', ['1st', '2nd', '3rd'], [('a', [('n', 0, '6')]), ('b', [('n', 1, '5')]), ('c', [('n', 2, '4')]),
                                             ('x', [('x',)]), ('eq', [('eq', '120')])], w=700, title='No letter twice')
p_b4 = IH('p_b4', '$6\\times5=30$, $\\ 30\\times4=120$', size=32)
p_r0 = I('p_r0', 'A, B, C in a row', size=36)
p_rL = LIST28('p_rL', 6, 3, [('a', [('r', 0, 'ABC'), ('r', 1, 'ACB')]), ('b', [('r', 2, 'BAC'), ('r', 3, 'BCA')]),
                             ('c', [('r', 4, 'CAB'), ('r', 5, 'CBA')]), ('d', [('foot', '6 orders')])],
              head=['1st', '2nd', '3rd'], cellw=70, cellh=46, right=20, gapc=8, w=300, col=1, title='Every order of A, B, C')
p_r1 = SLOTS28('p_r1', ['1st', '2nd', '3rd'], [('a', [('n', 0, '3')]), ('b', [('n', 1, '2')]), ('c', [('n', 2, '1', 'teal')]),
                                             ('x', [('x',)]), ('eq', [('eq', '6')])], w=560, title='Three places')
p_f0 = I('p_f0', '$4$ different mugs in a row', size=36)
p_f1 = SLOTS28('p_f1', ['1st', '2nd', '3rd', '4th'], [('a', [('n', 0, '4'), ('n', 1, '3'), ('n', 2, '2'), ('n', 3, '1')]),
                                                    ('x', [('x',)]), ('eq', [('eq', '24')])], boxw=120, gap=50, w=760, title='Four places')
p_f2 = IH('p_f2', '$4\\times3\\times2\\times1=4!$', size=36)
p_f3 = I('p_f3', '$n!=n\\times(n-1)\\times\\dots\\times2\\times1$', size=36)
p_f4 = IH('p_f4', '$3!=3\\times2\\times1=6$', size=32)
p_f5 = IH('p_f5', '$4!=4\\times3!=4\\times6=24$', size=32)
p_f6 = IH('p_f6', '$5!=5\\times4!=5\\times24=120$', size=32)
p_f7 = I('p_f7', '$n$ different items in a row: $\\ n!$ ways', size=36)
p_z1 = I('p_z1', 'Can we pick it again? $\\ $The pool stays full.', size=34)
p_z2 = I('p_z2', 'It left the pool? $\\ $The pool shrinks.', size=34)
p_z3 = I('p_z3', 'A row: $\\ $without repetition, $\\ n!$', size=34)
_wp127 = [
    S('With or Without Repetition',
      L("Many counting questions have us choose from a pool. The pool can be digits, letters, books or people."),
      L("And after every pick, we ask one question. Did the item leave the pool, or can we pick it again?"),
      L("That one question changes the count. Let's see how.")),
    S('With repetition',
      L("Let's start with a tiny case. How many two-digit codes can we make from the digits one, two and three, if digits "
        "may repeat?"),
      L("Here's the pool, one, two and three. For the first digit we have three options. Say we pick one.",
        show(p_p0['line'], "Here's the pool"), show(p_p0['pick'], 'Say we pick one')),
      L("Digits may repeat. So the one goes back into the pool, and we can pick it again.", show(p_p0['note'], 'goes back into the pool')),
      L("Let's list every code. Eleven, twelve, thirteen.", show(p_L1['line'], "Let's list every code"), show(p_L1['a'], 'Eleven, twelve')),
      L("Twenty-one, twenty-two, twenty-three.", show(p_L1['b'], 'Twenty-one, twenty-two')),
      L("Thirty-one, thirty-two, thirty-three. That's nine codes.", show(p_L1['c'], 'Thirty-one, thirty-two'),
        show(p_L1['d'], "That's nine codes")),
      L("In stages, the first digit has three options, and the second digit has three options too, because the pool "
        "stayed full. Three times three is nine.", show(p_s1['line'], 'In stages'), show(p_s1['a'], 'the first digit has three'),
        show(p_s1['b'], 'the second digit has three'), show(p_s1['x'], 'Three times three'), show(p_s1['eq'], 'Three times three is nine'))),
    S('Without repetition',
      L("Now the same digits, but no digit may repeat."),
      L("The first digit again has three options. Say we pick one. This time the one leaves the pool. Only two digits are "
        "left.", show(p_p1['line'], 'The first digit again'), show(p_p1['gone'], 'the one leaves the pool'),
        show(p_p1['note'], 'Only two digits are left')),
      L("Let's look at the same nine codes.", show(p_L2['line'], 'the same nine codes'), show(p_L2['a'], 'the same nine codes')),
      L("Eleven, twenty-two and thirty-three use a digit twice. They are not allowed now.",
        show(p_L2['x'], 'Eleven, twenty-two and thirty-three')),
      L("Nine minus three leaves six codes.", show(p_L2['d'], 'Nine minus three')),
      L("In stages, the first digit has three options, and the second digit only two. Three times two is six. The pool "
        "shrinks after every pick.", show(p_s2['line'], 'In stages'), show(p_s2['a'], 'the first digit has three'),
        show(p_s2['b'], 'the second digit only two'), show(p_s2['x'], 'Three times two'), show(p_s2['eq'], 'Three times two is six'))),
    S('A bigger pool',
      L("Now a bigger example. A code has three letters, from A, B, C, D, E and F. That's a pool of six letters.",
        show(p_b0, 'A code has three letters')),
      L("If letters may repeat, every letter goes back to the pool. Each place has six options.",
        show(p_b1['line'], 'If letters may repeat'), show(p_b1['a'], 'Each place has six options')),
      L("Six times six is thirty-six. Then thirty-six times six is two hundred sixteen codes.", show(p_b1['x'], 'Six times six'),
        show(p_b2, 'Six times six is thirty-six'), show(p_b1['eq'], 'two hundred sixteen codes')),
      L("If no letter may appear twice, the pool shrinks. The first place has six options.",
        show(p_b3['line'], 'If no letter may appear twice'), show(p_b3['a'], 'The first place has six options')),
      L("One letter is used, so the second place has five. Two are used, so the third place has four.",
        show(p_b3['b'], 'the second place has five'), show(p_b3['c'], 'the third place has four')),
      L("Six times five is thirty. Then thirty times four is a hundred twenty codes.", show(p_b3['x'], 'Six times five'),
        show(p_b4, 'Six times five is thirty'), show(p_b3['eq'], 'a hundred twenty codes')),
      L("The same letters, and a different answer. The only difference is whether a letter leaves the pool.")),
    S('Items in a row',
      L("Putting different items in a row is choosing without repetition. Once an item is in its place, it's out of the "
        "pool."),
      L("Let's see it with three letters, A, B and C, in a row. Let's list every order.", show(p_r0, 'three letters, A, B and C'),
        show(p_rL['line'], "Let's list every order")),
      L("A first, then the other two in two orders. A B C, and A C B.", show(p_rL['a'], 'A first')),
      L("B first, B A C, and B C A. C first, C A B, and C B A. That's six orders.", show(p_rL['b'], 'B first'),
        show(p_rL['c'], 'C first'), show(p_rL['d'], "That's six orders")),
      L("Now in stages. The first place has three options. The second place has two, because one letter is already "
        "placed.", show(p_r1['line'], 'Now in stages'), show(p_r1['a'], 'The first place has three'),
        show(p_r1['b'], 'The second place has two')),
      L("And the last place has only one letter left. No choice at all, so it gets one.", show(p_r1['c'], 'the last place has only one')),
      L("Three times two times one is six. The same six orders we listed.", show(p_r1['x'], 'Three times two times one'),
        show(p_r1['eq'], 'Three times two times one is six'))),
    S('Factorial',
      L("Now a new example. Four different mugs stand in a row on a shelf. In how many orders can they stand?",
        show(p_f0, 'Four different mugs')),
      L("The first place has four options, then three, then two, and the last place one.", show(p_f1['line'], 'The first place has four'),
        show(p_f1['a'], 'The first place has four')),
      L("Four times three is twelve. Times two, it's twenty-four. And times one, it's still twenty-four.",
        show(p_f1['x'], 'Four times three is twelve'), show(p_f1['eq'], 'And times one')),
      L("This product has a name. It's called a factorial, and we write it with an exclamation mark. Four times three "
        "times two times one is four factorial.", show(p_f2, 'is four factorial')),
      L("So n factorial is n, times every whole number below it, all the way down to one.", show(p_f3, 'So n factorial is n')),
      L("For example, three factorial is three times two times one, that's six.", show(p_f4, 'three factorial is three')),
      L("Four factorial is four times three factorial. Four times six is twenty-four.", show(p_f5, 'Four factorial is four times')),
      L("Five factorial is five times four factorial. Five times twenty-four is a hundred twenty.",
        show(p_f6, 'Five factorial is five times')),
      L("So n different items in a row can stand in n factorial orders. We'll use factorial again later in this topic, "
        "when we choose groups.", show(p_f7, 'n different items in a row'))),
    S('Recap',
      L("So let's sum it up. After every pick, ask if the item can be picked again. If it can, the pool stays full.",
        show(p_z1, 'If it can, the pool stays full')),
      L("If it left the pool, the pool shrinks by one at every stage.", show(p_z2, 'If it left the pool')),
      L("And different items in a row are a choice without repetition. That's n factorial.", show(p_z3, 'different items in a row')),
      L("Take a moment to memorize this, and I'll see you in the next video.")),
]
video('wp-127', 'lesson', slides=_wp127)

# ------------------------------------------------------------------------------------------------ g128 (lock, repeats)
# Hebrew (wp 8480-8504, digits 1-5, repeats: 5 x 5 x 5 = 125, "the 3 goes back into the pool"). English: digits 1-9 on
# three wheels, 9 x 9 x 9 = 729 (R36: 81 x 9 = 720 + 9). First question with the pool (wp-127). 777 counts.
g8S = SLOTS28('g8S', ['wheel 1', 'wheel 2', 'wheel 3'], [('a', [('n', 0, '9')]), ('b', [('n', 1, '9')]), ('c', [('n', 2, '9')]),
                                                       ('x', [('x',)]), ('eq', [('eq', '729')])], w=700, title='Three wheels')
g8P = POOL28('g8P', ['1', '2', '3', '4', '5', '6', '7', '8', '9'], [('pick', [('pick', 3)]), ('note', [('note', 'it goes back')])],
             tok=52, w=520, col=1, title='The pool: 1 to 9')
g8a = IH('g8a', '$9\\times9=81$', size=32, col=1)
g8b = IH('g8b', '$80\\times9=720$', size=32, col=1)
g8c = IH('g8c', '$720+9=729$', size=32, col=1)
g8d = IH('g8d', '$777$, $\\ 373$: $\\ $allowed', size=32)
video('solve-wp28-g128', 'solution', qid='wp28-g128', slides=[
    S('Method 1 · The math way: stages of choice',
      L("A suitcase lock has three wheels. Each wheel shows one of the digits one to nine, and digits may repeat. How many "
        "codes are possible?", pt('stem', 'A suitcase lock has three wheels', 'hl', 7.0), voice='calm', pause=0.5),
      L("So we choose a digit for each wheel. And the question says digits may repeat.", pt('stem: given', 'digits may repeat')),
      L("Let's solve it the math way, in stages. Remember the lesson. With or without repetition? Here it's with "
        "repetition.", show(g8S['line'], 'in stages')),
      L("The pool is the nine digits, one to nine. The first wheel has nine options. Say we pick four.",
        show(g8P['line'], 'The pool is the nine digits'), show(g8P['pick'], 'Say we pick four'), show(g8S['a'], 'The first wheel has nine')),
      L("Digits may repeat, so the four goes right back into the pool.", show(g8P['note'], 'goes right back into the pool')),
      L("So the second wheel has nine options again, and so does the third wheel.", show(g8S['b'], 'the second wheel has nine'),
        show(g8S['c'], 'so does the third wheel')),
      L("Now we multiply. Nine times nine is eighty-one.", show(g8S['x'], 'Now we multiply'), show(g8a, 'Nine times nine is eighty-one')),
      L("Then eighty-one times nine. Eighty times nine is seven hundred twenty, and one more nine makes seven hundred "
        "twenty-nine.", show(g8b, 'Eighty times nine'), show(g8c, 'one more nine'), show(g8S['eq'], 'seven hundred twenty-nine')),
      L("So codes like seven seven seven, or three seven three, are included. The question allows them.", show(g8d, 'seven seven seven')),
      L("Choice number one, five hundred four, is the count when digits can't repeat. That's the next question, not this "
        "one.", mk('cross', 'choice 1', 'five hundred four')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g129 (lock, no repeats)
# Hebrew (wp 8506-8540, 1-5 with different digits: 5 x 4 x 3 = 60; "the 3 didn't come back"; with vs without compared).
# English: 9 x 8 x 7 = 504 (R36: 72 x 7 = 490 + 14). Trap 84 = 504 / 6 (dividing: but 123 and 213 are different codes).
g9S = SLOTS28('g9S', ['wheel 1', 'wheel 2', 'wheel 3'], [('a', [('n', 0, '9')]), ('b', [('n', 1, '8')]), ('c', [('n', 2, '7')]),
                                                       ('x', [('x',)]), ('eq', [('eq', '504')])], w=700, title='Three wheels')
g9P = POOL28('g9P', ['1', '2', '3', '4', '5', '6', '7', '8', '9'], [('gone', [('gone', 3)]), ('note', [('note', '8 left')])],
             tok=52, w=520, col=1, title='The pool: 1 to 9')
g9a = IH('g9a', '$9\\times8=72$', size=32, col=1)
g9b = IH('g9b', '$70\\times7=490$', size=32, col=1)
g9c = IH('g9c', '$2\\times7=14$', size=32, col=1)
g9d = IH('g9d', '$490+14=504$', size=32, col=1)
g9e = IH('g9e', '$123\\ne213$: $\\ $no dividing', size=32)
video('solve-wp28-g129', 'solution', qid='wp28-g129', slides=[
    S('Method 1 · The math way: stages of choice',
      L("A suitcase lock has three wheels. Each wheel shows one of the digits one to nine, and no digit may appear twice. "
        "How many codes are possible?", pt('stem', 'A suitcase lock has three wheels', 'hl', 7.0), voice='calm', pause=0.5),
      L("It's the same lock as in the last question, with one change. Now no digit may appear twice.",
        pt('stem: given', 'no digit may appear twice')),
      L("Let's solve it the math way, in stages. This time it's without repetition.", show(g9S['line'], 'in stages')),
      L("The first wheel has nine options. Say we pick four.", show(g9S['a'], 'The first wheel has nine'), show(g9P['line'], 'Say we pick four')),
      L("Now the four leaves the pool. It can't come back, because no digit may appear twice.",
        show(g9P['gone'], 'the four leaves the pool')),
      L("So the second wheel has only eight options left.", show(g9P['note'], 'only eight options left'), show(g9S['b'], 'only eight options')),
      L("Two digits are used now, so the third wheel has seven options.", show(g9S['c'], 'the third wheel has seven')),
      L("Nine times eight is seventy-two.", show(g9S['x'], 'Nine times eight'), show(g9a, 'Nine times eight is seventy-two')),
      L("Then seventy-two times seven. Seventy times seven is four hundred ninety. And two times seven is fourteen.",
        show(g9b, 'Seventy times seven'), show(g9c, 'two times seven is fourteen')),
      L("Four hundred ninety plus fourteen is five hundred four.", show(g9d, 'Four hundred ninety plus fourteen'),
        show(g9S['eq'], 'is five hundred four')),
      L("Compare with the last question. The same digits, but the pool shrinks after every pick. Nine, nine, nine became "
        "nine, eight, seven."),
      L("And careful, we don't divide by anything here. One two three and two one three are different codes. Dividing by "
        "six gives eighty-four, choice number two, and that's a trap.", show(g9e, 'One two three and two one three'),
        mk('cross', 'choice 2', 'eighty-four, choice number two')),
      L("Choice number four is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g130 (7 trophies in a row)
# Hebrew (wp 8541-8626, 5 books on a shelf: 5 x 4 x 3 x 2 x 1 = 120; the last place: "no choice, only one option";
# factorial). English: 7 trophies, 7! = 5040 (built up in small steps, R33). Factorial is taught in wp-127; here "like
# in the lesson". Traps: 720 = 6!, 49 = 7 x 7 (the pool doesn't shrink).
g0S = SLOTS28('g0S', ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th'],
              [('a', [('n', 0, '7')]), ('b', [('n', 1, '6')]), ('c', [('n', 2, '5'), ('n', 3, '4'), ('n', 4, '3'), ('n', 5, '2')]),
               ('d', [('n', 6, '1', 'teal')]), ('x', [('x',)])], boxw=88, gap=40, eqw=14, w=1000, title='Seven places', lab_size=26)
g0a = IH('g0a', '$7\\times6=42$', size=30)
g0b = IH('g0b', '$42\\times5=210$', size=30)
g0c = IH('g0c', '$210\\times4=840$', size=30)
g0d = IH('g0d', '$840\\times3=2520$', size=30, col=1)
g0e = IH('g0e', '$2520\\times2=5040$', size=30, col=1)
g0f = IH('g0f', '$7!=5040$', size=34, col=1)
g0g = IH('g0g', '$7\\times7=49$: $\\ $the trap', size=30, col=1)
video('solve-wp28-g130', 'solution', qid='wp28-g130', slides=[
    S('Method 1 · The math way: stages of choice',
      L("In how many different ways can seven different trophies be placed in a row in a glass cabinet?",
        pt('stem', 'In how many different ways', 'hl', 5.0), voice='calm', pause=0.5),
      L("So we put seven different items in a row. Like in the lesson, a row is a choice without repetition.",
        pt('stem', 'So we put seven different items')),
      L("Let's solve it the math way, in stages. Seven trophies and seven places in the row, so seven stages.",
        show(g0S['line'], 'seven stages')),
      L("The first place can take any of the seven trophies. Seven options.", show(g0S['a'], 'Seven options')),
      L("That trophy is placed, so it's out. The second place has six left.", show(g0S['b'], 'The second place has six')),
      L("Then five, four, three and two.", show(g0S['c'], 'Then five, four, three and two')),
      L("And the last place has only one trophy left. No choice at all.", show(g0S['d'], 'the last place has only one')),
      L("Now we multiply, one step at a time. Seven times six is forty-two.", show(g0S['x'], 'Now we multiply'),
        show(g0a, 'Seven times six is forty-two')),
      L("Forty-two times five is two hundred ten.", show(g0b, 'Forty-two times five')),
      L("Two hundred ten times four is eight hundred forty.", show(g0c, 'Two hundred ten times four')),
      L("Eight hundred forty times three is two thousand five hundred twenty.", show(g0d, 'Eight hundred forty times three')),
      L("And times two is five thousand forty. Times one doesn't change it.", show(g0e, 'And times two is five thousand forty')),
      L("That's seven factorial. Seven different items in a row, seven factorial ways.", show(g0f, "That's seven factorial")),
      L("A lot of students write seven times seven, forty-nine. That's choice number four. But a trophy can't stand in two "
        "places, so the pool shrinks.", show(g0g, 'seven times seven, forty-nine'), mk('cross', 'choice 4', "That's choice number four")),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-131 (lesson: mutual action)
# Hebrew (wp 8629-8752): a mutual action = between two items at once, "quite common on the exam"; flights between 4
# countries: take-off 4 x landing 3 = 12, not in the choices, "what am I missing?"; she numbers all 12 and shows each
# line counted twice (Washington-Russia and back); "with 10 countries we won't draw": count as usual, divide by 2; cues:
# handshakes, paths between houses, games between teams, diagonals of a polygon. Her descending series (wp 8790-8800:
# 5 + 4 + 3 + 2 + 1, "each time one fewer, because a line already comes from the vertex before") is used in g132, g133
# and (rising) in g143, so R37 teaches it here too. English (new numbers): 5 friends shaking hands: 5 x 4 = 20 ordered
# pairs LISTED, each handshake twice, 20 / 2 = 10; the picture 4 + 3 + 2 + 1 = 10; 11 teams: 110 / 2 = 55; roles
# (a captain and a vice captain: 20, don't halve). Real exam: 2025_winter_q1_02 (5 people shake hands), 2020_winter_q2_06.
_HS = [['AB', 'AC', 'AD', 'AE'], ['BA', 'BC', 'BD', 'BE'], ['CA', 'CB', 'CD', 'CE'], ['DA', 'DB', 'DC', 'DE'], ['EA', 'EB', 'EC', 'ED']]
m_s0 = I('m_s0', '$5$ friends. $\\ $Every two shake hands once.', size=34)
m_s1 = SLOTS28('m_s1', ['one', 'the other'], [('a', [('n', 0, '5')]), ('b', [('n', 1, '4')]), ('x', [('x',)]), ('eq', [('eq', '20')])],
               boxw=170, w=560, title='Counted as usual')
m_L = LIST28('m_L', 5, 4, [('r%d' % i, [('r', i, _HS[i])]) for i in range(5)] +
             [('ab', [('hl', 0, 0), ('hl', 1, 0)]), ('ab2', [('ring', 0, 1, 'AB = BA')]),
              ('all', [('hl', 0, 1), ('hl', 2, 0), ('hl', 3, 2), ('hl', 2, 2)])],
             cellw=70, cellh=46, right=180, gapc=10, w=520, size=30, col=1, title='Every ordered pair')
m_s2 = IH('m_s2', '$20\\div2=10$ handshakes', size=34)
m_D = DOTS28('m_D', ['A', 'B', 'C', 'D', 'E'], [
    ('a', [('all', 0)]), ('b', [('ln', 1, 2, 'orange'), ('ln', 1, 3, 'orange'), ('ln', 1, 4, 'orange')]),
    ('c', [('ln', 2, 3, '#5a4fcf'), ('ln', 2, 4, '#5a4fcf')]),
    ('d', [('ln', 3, 4, 'red')]), ('u', [('under', '4 + 3 + 2 + 1 = 10')])], R=130, pad=60, w=430, title='Five friends')
m_d1 = IH('m_d1', 'A: $\\ 4$ new lines', size=30, col=1)
m_d2 = IH('m_d2', 'B: $\\ 3$ new lines', size=30, col=1)
m_d3 = IH('m_d3', 'C: $\\ 2$, $\\ $D: $\\ 1$', size=30, col=1)
m_d4 = IH('m_d4', '$4+3+2+1=10$', size=32, col=1)
m_r0 = I('m_r0', 'A mutual action: $\\ $count as usual, $\\ $then divide by $2$.', size=34)
m_r1 = I('m_r1', '$n$ people: $\\ \\dfrac{n\\times(n-1)}{2}$', size=38)
m_r2 = I('m_r2', '$11$ teams. $\\ $Every two teams play once.', size=34)
m_r3 = IH('m_r3', '$11\\times10=110$', size=32, col=1)
m_r4 = IH('m_r4', '$110\\div2=55$ games', size=32, col=1)
m_c1 = I('m_c1', 'Handshakes $\\ \\cdot\\ $ games between two teams', size=34)
m_c2 = I('m_c2', 'Two-way roads or flights between cities', size=34)
m_c3 = I('m_c3', 'Lines between points $\\ \\cdot\\ $ diagonals', size=34)
m_o0 = I('m_o0', '$5$ players: $\\ $a captain and a vice captain', size=34)
m_o1 = IH('m_o1', '$5\\times4=20$', size=32)
m_o2 = IH('m_o2', 'A captain, B vice $\\ne$ B captain, A vice', size=30)
m_o3 = I('m_o3', 'Different roles: $\\ $don\'t divide.', size=34)
m_z1 = I('m_z1', 'The same pair, two ways? $\\ $Divide by $2$.', size=34)
m_z2 = I('m_z2', 'Or add: $\\ 4+3+2+1$, $\\ $one fewer each time', size=34)
video('wp-131', 'lesson', slides=[
    S('Mutual Action',
      L("Now a new kind of counting question. A mutual action is an action between two people, or two things, at the "
        "same time."),
      L("Like a handshake. When Ann shakes Ben's hand, Ben shakes Ann's hand at the same moment. It's one handshake."),
      L("Mutual action is quite common on the exam, so let's understand it well.")),
    S('Count as usual',
      L("Let's start with an example. Five friends, A, B, C, D and E, meet. Every two of them shake hands once. How many "
        "handshakes are there?", show(m_s0, 'Five friends')),
      L("First, let's count as usual, in stages. Stage one is the person who starts the handshake. That's five options.",
        show(m_s1['line'], "let's count as usual"), show(m_s1['a'], "That's five options")),
      L("Stage two is the other person. Nobody shakes their own hand, so that's four options.", show(m_s1['b'], 'so that\'s four options')),
      L("Five times four is twenty. But twenty is not the answer. Let's see why.", show(m_s1['x'], 'Five times four'),
        show(m_s1['eq'], 'Five times four is twenty')),
      L("Here are all twenty pairs. A first, with B, C, D or E.", show(m_L['line'], 'Here are all twenty pairs'),
        show(m_L['r0'], 'A first')),
      L("Then B first, C first, D first and E first.", show(m_L['r1'], 'Then B first'), show(m_L['r2'], 'C first'),
        show(m_L['r3'], 'D first'), show(m_L['r4'], 'and E first')),
      L("Look at A B and B A. A B is A shaking B's hand. B A is B shaking A's hand. But that's the same handshake.",
        show(m_L['ab'], 'Look at A B and B A'), show(m_L['ab2'], "that's the same handshake")),
      L("And it's the same for every handshake. A C is also there as C A, and C D is there as D C. Every handshake "
        "appears twice in our twenty.", show(m_L['all'], 'A C is also there')),
      L("So we divide by two. Twenty divided by two is ten handshakes.", show(m_s2, 'Twenty divided by two'))),
    S('Draw it',
      L("Let's check it with a drawing. Five points, one for each friend.", show(m_D['line'], 'Five points')),
      L("From A, we draw a line to each of the other four. That's four handshakes.", show(m_D['a'], 'From A, we draw a line'),
        show(m_d1, "That's four handshakes")),
      L("From B, the line to A is already there. So B adds only three new lines.", show(m_D['b'], 'From B, the line to A'),
        show(m_d2, 'B adds only three new lines')),
      L("C adds two new lines, and D adds one. E has no new lines left.", show(m_D['c'], 'C adds two new lines'),
        show(m_D['d'], 'D adds one'), show(m_d3, 'C adds two new lines')),
      L("Four plus three plus two plus one is ten. The same ten handshakes.", show(m_D['u'], 'Four plus three plus two plus one'),
        show(m_d4, 'Four plus three plus two plus one is ten')),
      L("So this is another way to count. Each point adds one fewer new line than the point before it, because one of its "
        "lines is already drawn.")),
    S('The rule',
      L("So here's the rule. In a mutual action, we count as usual, and then we divide by two.", show(m_r0, 'we count as usual')),
      L("Why divide by two? Because counting in order counts every pair twice, once from each side."),
      L("With n people, that's n times n minus one, divided by two.", show(m_r1, 'n times n minus one')),
      L("Now a new example. Eleven teams play in a league. Every two teams play each other once. How many games are "
        "played?", show(m_r2, 'Eleven teams play in a league')),
      L("Count as usual. Eleven teams, and each one plays ten others. Eleven times ten is a hundred ten.",
        show(m_r3, 'Eleven times ten')),
      L("A game between two teams is a mutual action. When team A plays team B, team B plays team A. So we divide by two. "
        "A hundred ten divided by two is fifty-five games.", show(m_r4, 'A hundred ten divided by two'))),
    S('Where you will see it',
      L("How do you spot a mutual action on the exam? Here are the usual stories."),
      L("Handshakes, and games between two teams.", show(m_c1, 'Handshakes')),
      L("Two-way roads, bus lines or flights between cities.", show(m_c2, 'Two-way roads')),
      L("And lines between points, like the diagonals of a polygon.", show(m_c3, 'And lines between points')),
      L("In all of them, the pair A and B is the same as the pair B and A.")),
    S('Roles: no halving',
      L("But careful. Sometimes the two people have different roles. Then we don't divide."),
      L("For example, we choose a captain and a vice captain from five players.", show(m_o0, 'a captain and a vice captain')),
      L("The captain has five options, and the vice captain four. Five times four is twenty.", show(m_o1, 'Five times four is twenty')),
      L("Here, A as captain with B as vice is not the same as B as captain with A as vice. The roles are different.",
        show(m_o2, 'A as captain with B as vice')),
      L("So there's no double counting, and the answer is twenty. We divide by two only when the pair is the same from "
        "both sides.", show(m_o3, "So there's no double counting"))),
    S('Recap',
      L("So let's sum it up. If every pair was counted from both sides, divide by two.", show(m_z1, 'divide by two')),
      L("Or count the new lines and add them, four plus three plus two plus one. One fewer each time.", show(m_z2, 'count the new lines')),
      L("And if the two have different roles, don't divide."),
      L("Take a moment to memorize this, and I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ g132 (six towns, bus lines)
# Hebrew (wp 8642-8730, 4 countries: 4 x 3 = 12, "not in the choices, what am I missing?", each line counted twice,
# divide by 2 -> 6). English: 6 towns: 6 x 5 = 30, the trap 30 is a choice, / 2 = 15; Method 2 her descending series
# (5 + 4 + 3 + 2 + 1, the picture). First question with mutual action (wp-131).
g2S = SLOTS28('g2S', ['from', 'to'], [('a', [('n', 0, '6')]), ('b', [('n', 1, '5')]), ('x', [('x',)]), ('eq', [('eq', '30')])],
              w=480, title='Counted as usual')
g2a = IH('g2a', 'A to B $=$ B to A', size=32)
g2b = IH('g2b', '$30\\div2=15$', size=34)
g2D = DOTS28('g2D', ['A', 'B', 'C', 'D', 'E', 'F'], [
    ('a', [('all', 0)]), ('b', [('ln', 1, j, 'orange') for j in (2, 3, 4, 5)]), ('c', [('ln', 2, j, '#5a4fcf') for j in (3, 4, 5)]),
    ('d', [('ln', 3, 4, 'red'), ('ln', 3, 5, 'red')]), ('e', [('ln', 4, 5, 'ink')])], R=120, pad=56, w=440, title='Six towns')
g2c = IH('g2c', 'A: $\\ 5$, $\\ $B: $\\ 4$, $\\ $C: $\\ 3$', size=30, col=1)
g2d = IH('g2d', 'D: $\\ 2$, $\\ $E: $\\ 1$', size=30, col=1)
g2e = IH('g2e', '$5+4+3+2+1=15$', size=32, col=1)
video('solve-wp28-g132', 'solution', qid='wp28-g132', slides=[
    S('Method 1 · The math way: mutual action',
      L("Six towns are connected so that every pair of towns has exactly one direct two-way bus line. How many bus lines "
        "are there?", pt('stem', 'Six towns are connected', 'hl', 7.0), voice='calm', pause=0.5),
      L("So every two towns have one line between them, and the line goes both ways. That's a mutual action, like in the "
        "lesson.", pt('stem: given', 'every two towns have one line')),
      L("We'll solve it in two different ways. Let's start with the math way. We count as usual, in stages. A line leaves "
        "from one of the six towns.", show(g2S['line'], 'We count as usual'), show(g2S['a'], 'one of the six towns')),
      L("It arrives at a different town, so five options.", show(g2S['b'], 'so five options')),
      L("Six times five is thirty. Thirty is one of the choices, choice number two. But careful, something is off.",
        show(g2S['x'], 'Six times five'), show(g2S['eq'], 'Six times five is thirty')),
      L("We counted the line from A to B, and later the line from B to A. But a two-way line from A to B is the same line "
        "as from B to A.", show(g2a, 'the same line')),
      L("So every line was counted twice. That's why thirty is a trap.", mk('cross', 'choice 2', 'thirty is a trap')),
      L("We divide by two. Thirty divided by two is fifteen bus lines.", show(g2b, 'Thirty divided by two'))),
    S('Method 2 · The math way: one fewer each time',
      L("[pause] Now a second way, with a drawing. Six points for the six towns, A to F.", show(g2D['line'], 'Six points')),
      L("From A, a line to each of the other five towns. Five lines.", show(g2D['a'], 'From A'), show(g2c, 'From A')),
      L("From B, the line to A is already there. So B adds four new lines.", show(g2D['b'], 'So B adds four')),
      L("C adds three new lines, because its lines to A and B are already there.", show(g2D['c'], 'C adds three')),
      L("D adds two, and E adds one. F has no new lines left.", show(g2D['d'], 'D adds two'), show(g2D['e'], 'E adds one'),
        show(g2d, 'D adds two')),
      L("Five plus four plus three plus two plus one is fifteen. The same fifteen lines.", show(g2e, 'Five plus four plus three')),
      L("Choice number one is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g133 (octagon diagonals)
# Hebrew (wp 8753-8814, the hexagon, 4 ways): (1) draw and count (9), "they won't give a 20-sided polygon"; (2) mutual
# action 6 x 5 / 2 = 15 lines minus 6 sides; (3) the descending series 5 + 4 + 3 + 2 + 1 = 15 minus 6; (4) the formula
# n(n - 3)/2. English: the octagon -> 20, the same four ways (the report keeps all four). Rare on the exam, said once.
# Traps: 28 = all the lines (sides included), 40 = not halving.
def _oct_new(k):
    return [('ln', k, j) for j in range(k + 2, 8) if not (k == 0 and j == 7)]
g3D = DOTS28('g3D', ['1', '2', '3', '4', '5', '6', '7', '8'], [('s', [('sides',)])] +
             [('d%d' % k, _oct_new(k)) for k in range(6)], R=150, pad=50, w=500, title='An eight-sided polygon')
g3a = IH('g3a', '$5+5+4+3+2+1=20$', size=30, col=1)
g3b = IH('g3b', '$8\\times7=56$', size=30)
g3c = IH('g3c', '$56\\div2=28$ lines', size=30)
g3d = IH('g3d', '$28-8=20$', size=30)
g3e = IH('g3e', '$7+6+5+4+3+2+1=28$', size=30)
g3f = IH('g3f', '$28-8=20$', size=30)
g3g = I('g3g', '$\\dfrac{n\\times(n-3)}{2}$', size=40)
g3h = IH('g3h', '$8\\times5=40$', size=30, col=1)
g3i = IH('g3i', '$40\\div2=20$', size=30, col=1)
video('solve-wp28-g133', 'solution', qid='wp28-g133', slides=[
    S('Method 1 · The math way: draw and count',
      L("How many diagonals does an eight-sided polygon have?", pt('stem', 'How many diagonals', 'hl', 3.0), voice='calm', pause=0.5),
      L("This question type is rare, but it does show up on the exam. A diagonal joins two vertices that are not next to "
        "each other. So a side is not a diagonal.", pt('stem', 'This question type is rare')),
      L("We'll solve it in four different ways. Let's start with the simplest math way. We draw it, and we count. Exam "
        "polygons are small, so drawing and counting is a real option.", show(g3D['line'], 'We draw it')),
      L("Here are the eight vertices and the eight sides.", show(g3D['s'], 'the eight sides')),
      L("From vertex one, we draw a line to every vertex that is not next to it. Vertex one has five diagonals.",
        show(g3D['d0'], 'From vertex one')),
      L("From vertex two, also five new diagonals.", show(g3D['d1'], 'From vertex two')),
      L("From vertex three, four new ones, because the diagonal to vertex one is already drawn.", show(g3D['d2'], 'From vertex three')),
      L("Then three, two and one new diagonals from the next vertices.", show(g3D['d3'], 'Then three'), show(g3D['d4'], 'two and one'),
        show(g3D['d5'], 'two and one')),
      L("Five plus five plus four plus three plus two plus one is twenty diagonals. With eight sides it's already "
        "crowded, so let's see faster ways.", show(g3a, 'Five plus five plus four'))),
    S('Method 2 · The math way: mutual action',
      L("[pause] Now the second way, with mutual action. A line between two vertices is a mutual action. The line from one "
        "to two is the same as the line from two to one."),
      L("We count as usual. Eight vertices to start from, and seven others to go to. Eight times seven is fifty-six.",
        show(g3b, 'Eight times seven is fifty-six')),
      L("Every line was counted from both ends, so we divide by two. Fifty-six divided by two is twenty-eight lines.",
        show(g3c, 'Fifty-six divided by two')),
      L("But twenty-eight is all the lines, and eight of them are the sides of the polygon. Sides are not diagonals. "
        "That's why twenty-eight, choice number one, is a trap.", mk('cross', 'choice 1', 'choice number one, is a trap')),
      L("Twenty-eight minus eight is twenty diagonals.", show(g3d, 'Twenty-eight minus eight'))),
    S('Method 3 · The math way: one fewer each time',
      L("[pause] The third way is like the drawing in the lesson. From the first vertex, seven new lines. From the next "
        "one, six new lines, then five, four, three, two and one."),
      L("Each time it's one fewer, because one line already came from the vertex before. Seven plus six plus five plus "
        "four plus three plus two plus one is twenty-eight lines.", show(g3e, 'Seven plus six plus five')),
      L("Again, eight of those lines are sides. Twenty-eight minus eight is twenty.", show(g3f, 'Twenty-eight minus eight'))),
    S('Method 4 · The math way: the formula',
      L("[pause] And the fourth way, a formula. The number of diagonals is n times n minus three, divided by two.",
        show(g3g, 'n times n minus three')),
      L("Why minus three? From each vertex there's no diagonal to itself, and none to its two neighbours. So each vertex "
        "has n minus three diagonals. And we divide by two, because each diagonal has two ends."),
      L("Here n is eight. Eight times five is forty.", show(g3h, 'Eight times five is forty')),
      L("Careful, forty is choice number four, and it's a trap. Forty counts every diagonal from both of its ends.",
        mk('cross', 'choice 4', "it's a trap")),
      L("Forty divided by two is twenty. Four ways, and one answer.", show(g3i, 'Forty divided by two')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-134 (lesson: add or subtract cases)
# Hebrew (wp 8816-8953): we can't count in one calculation, so we split into cases; "these questions are very rare on the
# exam, considered very hard, once every few years"; usually 2 cases, count each, add (Ravid: cola forces the nut bar:
# 1 + 3 x 5 = 16); subtracting is even rarer: a rule forbids an arrangement -> all minus forbidden (two dice, sum not 4:
# 36 - 3 = 33); listing the allowed ones directly is possible but messier; recap: rare, near the end of the section.
# English (R37, two examples per idea, new numbers): a lunch of two kinds (3 x 2 + 4 = 10); a forcing rule (the thin
# base forces cheese: 1 + 3 x 3 = 10, then the same by subtracting, 12 - 2); codes with different digits (16 - 4 = 12,
# checked by 4 x 3); the real-exam type "not the same colour" (2021_spring_q2_16, new numbers: 30 - (6 + 4) = 20, checked
# by cases 4 + 16); the cue words "not", "different from", "at least one".
k_a0 = I('k_a0', 'A lunch: $\\ $a sandwich and a drink, $\\ $or a soup alone', size=34)
k_a1 = I('k_a1', '$3$ sandwiches, $\\ 2$ drinks, $\\ 4$ soups', size=34)
k_a2 = IH('k_a2', 'case 1, $\\ $sandwich and drink: $\\ 3\\times2=6$', size=32)
k_a3 = IH('k_a3', 'case 2, $\\ $soup: $\\ 4$', size=32)
k_a4 = IH('k_a4', '$6+4=10$ lunches', size=34)
k_b0 = I('k_b0', '$4$ bases, $\\ 3$ toppings. $\\ $Thin base: $\\ $only cheese.', size=34)
k_b1 = SLOTS28('k_b1', ['thin base', 'cheese'], [('a', [('n', 0, '1')]), ('b', [('n', 1, '1')]), ('x', [('x',)]), ('eq', [('eq', '1')])],
               boxw=170, w=480, title='Case 1: the thin base')
k_b2 = SLOTS28('k_b2', ['other base', 'topping'], [('a', [('n', 0, '3')]), ('b', [('n', 1, '3')]), ('x', [('x',)]), ('eq', [('eq', '9')])],
               boxw=170, w=480, title='Case 2: another base')
k_b3 = IH('k_b3', '$1+9=10$ pizzas', size=34)
k_c1 = IH('k_c1', 'all: $\\ 4\\times3=12$', size=32)
k_c2 = IH('k_c2', 'forbidden: $\\ $thin with the $2$ other toppings', size=32)
k_c3 = IH('k_c3', '$12-2=10$', size=34)
k_c4 = I('k_c4', 'All, $\\ $minus the forbidden ones.', size=36)
k_d0 = I('k_d0', 'Two-digit codes from $1,\\ 2,\\ 3,\\ 4$. $\\ $The digits are different.', size=34)
k_d1 = IH('k_d1', 'all: $\\ 4\\times4=16$', size=32)
k_d2 = IH('k_d2', 'forbidden: $\\ 11,\\ 22,\\ 33,\\ 44$', size=32)
k_d3 = IH('k_d3', '$16-4=12$', size=34)
k_d4 = IH('k_d4', 'check: $\\ 4\\times3=12$', size=32)
k_e0 = I('k_e0', 'Shirts: $\\ 2$ blue, $\\ 4$ white', size=34)
k_e1 = I('k_e1', 'Trousers: $\\ 3$ blue, $\\ 1$ white, $\\ 1$ black', size=34)
k_e2 = I('k_e2', 'Not the same colour. $\\ $How many outfits?', size=34)
k_e3 = IH('k_e3', 'all: $\\ 6\\times5=30$', size=32)
k_e4 = IH('k_e4', 'blue and blue: $\\ 2\\times3=6$', size=32)
k_e5 = IH('k_e5', 'white and white: $\\ 4\\times1=4$', size=32)
k_e6 = IH('k_e6', 'forbidden: $\\ 6+4=10$', size=32)
k_e7 = IH('k_e7', '$30-10=20$', size=34)
k_e8 = IH('k_e8', 'blue shirt: $\\ 2\\times2=4$', size=30, col=1)
k_e9 = IH('k_e9', 'white shirt: $\\ 4\\times4=16$', size=30, col=1)
k_e10 = IH('k_e10', '$4+16=20$', size=32, col=1)
k_z1 = I('k_z1', 'Cases that don\'t overlap: $\\ $add them.', size=34)
k_z2 = I('k_z2', '"Not", $\\ $"different from", $\\ $"at least one": $\\ $all minus forbidden', size=32)
_wp134 = [
    S('Add or Subtract Cases',
      L("Sometimes we can't count everything in one multiplication. Then we split the count into cases, or we subtract."),
      L("First, something important to know. These questions are rare on the exam, and they are considered hard. Maybe "
        "one every few years, and then near the end of the section."),
      L("So don't panic. But know the idea, because it also helps a lot in probability, the next topic.")),
    S('Adding cases',
      L("Let's start with adding. Now a new example. A lunch is either a sandwich and a drink, or a soup alone.",
        show(k_a0, 'A lunch is either')),
      L("There are three sandwiches, two drinks and four soups. How many different lunches are possible?", show(k_a1, 'There are three sandwiches')),
      L("We can't do it in one multiplication, because the two kinds of lunch have different stages. So we split it into "
        "two cases."),
      L("Case one, a sandwich and a drink. Three times two is six lunches.", show(k_a2, 'Three times two is six')),
      L("Case two, a soup alone. That's four lunches.", show(k_a3, "That's four lunches")),
      L("Every lunch is in one case or the other, never in both. So we add the cases. Six plus four is ten lunches.",
        show(k_a4, 'Six plus four is ten'))),
    S('A rule that forces a choice',
      L("Now a new example. A pizza place has four kinds of base and three toppings. A pizza has one base and one topping. "
        "But if you take the thin base, the topping must be cheese.", show(k_b0, 'A pizza place has four kinds of base')),
      L("The rule only talks about the thin base. So we split into two cases, the thin base, and any other base."),
      L("Case one, the thin base. The base has one option, and the topping must be cheese, also one option. One times one "
        "is one pizza.", show(k_b1['line'], 'Case one, the thin base'), show(k_b1['a'], 'The base has one option'),
        show(k_b1['b'], 'also one option'), show(k_b1['x'], 'One times one'), show(k_b1['eq'], 'is one pizza')),
      L("Case two, another base. That's three options. And any topping is allowed, cheese too. Three options. Three times "
        "three is nine.", show(k_b2['line'], 'Case two, another base'), show(k_b2['a'], "That's three options"),
        show(k_b2['b'], 'Three options'), show(k_b2['x'], 'Three times three'), show(k_b2['eq'], 'Three times three is nine')),
      L("The cases don't overlap, because a base is thin or it isn't. One plus nine is ten pizzas.", show(k_b3, 'One plus nine is ten'))),
    S('Subtracting',
      L("Now the other way, subtracting. The same pizzas, but this time we count everything as if there were no rule."),
      L("Four bases times three toppings is twelve pizzas.", show(k_c1, 'Four bases times three toppings')),
      L("Which pizzas does the rule forbid? The thin base with the two toppings that aren't cheese. That's two pizzas.",
        show(k_c2, 'The thin base with the two toppings')),
      L("Twelve minus two is ten. The same answer.", show(k_c3, 'Twelve minus two is ten')),
      L("So when a rule forbids something, count all of them, and subtract the forbidden ones. All, minus forbidden, "
        "leaves what's allowed.", show(k_c4, 'count all of them'))),
    S('Different digits',
      L("Now a new example. How many two-digit codes can we make from the digits one, two, three and four, if the two "
        "digits must be different?", show(k_d0, 'How many two-digit codes')),
      L("First, all the codes, as if digits could repeat. Four times four is sixteen.", show(k_d1, 'Four times four is sixteen')),
      L("The forbidden codes use the same digit twice. Eleven, twenty-two, thirty-three and forty-four. That's four.",
        show(k_d2, 'Eleven, twenty-two')),
      L("Sixteen minus four is twelve codes.", show(k_d3, 'Sixteen minus four')),
      L("Let's check it with the pool. The first digit has four options, and then three are left. Four times three is "
        "twelve. The same.", show(k_d4, 'Four times three is twelve'))),
    S('Not the same colour',
      L("And now a type that comes up on the exam. Dan has six shirts, two blue and four white.", show(k_e0, 'six shirts')),
      L("He has five pairs of trousers, three blue, one white and one black.", show(k_e1, 'five pairs of trousers')),
      L("He wears a shirt and trousers that are not the same colour. How many outfits can he wear?", show(k_e2, 'not the same colour')),
      L("Not the same colour, so let's count all, minus the forbidden. All the outfits are six times five, thirty.",
        show(k_e3, 'six times five, thirty')),
      L("The forbidden ones have the same colour. A blue shirt with blue trousers is two times three, six.",
        show(k_e4, 'two times three, six')),
      L("A white shirt with white trousers is four times one, four. No shirt is black, so there's nothing more to forbid.",
        show(k_e5, 'four times one, four')),
      L("Six plus four is ten forbidden outfits. Thirty minus ten is twenty.", show(k_e6, 'Six plus four is ten'),
        show(k_e7, 'Thirty minus ten is twenty')),
      L("Let's check it with cases. A blue shirt goes with trousers that aren't blue, two of them. Two times two is four.",
        show(k_e8, 'Two times two is four')),
      L("A white shirt goes with trousers that aren't white, four of them. Four times four is sixteen. Four plus sixteen "
        "is twenty again.", show(k_e9, 'Four times four is sixteen'), show(k_e10, 'Four plus sixteen'))),
    S('Recap',
      L("So let's sum it up. If you can't count in one go, split into cases that don't overlap, and add them.", show(k_z1, 'split into cases')),
      L("And when you see the words not, different from, or at least one, count all, and subtract the forbidden ones.",
        show(k_z2, 'when you see the words not')),
      L("Subtracting is worth it when the forbidden group is small and easy to count. Take a moment to memorize this, and "
        "I'll see you in the next video.")),
]
video('wp-134', 'lesson', slides=_wp134)

# ------------------------------------------------------------------------------------------------ g135 (espresso forces a croissant)
# Hebrew (wp 8836-8897, Ravid: cola forces the nut bar: case 1, 1 x 1 = 1; case 2, 3 x 5 = 15, the nut bar included;
# 16). English: espresso -> croissant: 1 + 5 x 5 = 26; the rule works one way only (the croissant still goes with other
# drinks); Method 2 all minus forbidden, 30 - 4 = 26 (both from wp-134).
g35a = SLOTS28('g35a', ['espresso', 'croissant'], [('a', [('n', 0, '1')]), ('b', [('n', 1, '1')]), ('x', [('x',)]), ('eq', [('eq', '1')])],
               boxw=170, w=460, title='Case 1: espresso')
g35b = SLOTS28('g35b', ['other drink', 'pastry'], [('a', [('n', 0, '5')]), ('b', [('n', 1, '5')]), ('x', [('x',)]), ('eq', [('eq', '25')])],
               boxw=170, w=460, title='Case 2: another drink')
g35c = IH('g35c', '$1+25=26$', size=34)
g35d = IH('g35d', '$5\\times4=20$, $\\ 20+1=21$: $\\ $the trap', size=30, col=1)
g35e = IH('g35e', 'all: $\\ 6\\times5=30$', size=32)
g35f = IH('g35f', 'forbidden: $\\ $espresso with $4$ pastries', size=32)
g35g = IH('g35g', '$30-4=26$', size=34)
video('solve-wp28-g135', 'solution', qid='wp28-g135', slides=[
    S('Method 1 · The math way: two cases',
      L("A breakfast stand offers six hot drinks and five pastries. A customer chooses one of each. If the drink is "
        "espresso, the pastry must be a croissant. With any other drink, any pastry is allowed. How many choices are "
        "possible?", pt('stem', 'A breakfast stand offers', 'hl', 12.0), voice='calm', pause=0.5),
      L("So a choice is one drink and one pastry. And there's a rule only for espresso.", pt('stem: given', 'there\'s a rule only for espresso')),
      L("We'll solve it in two different ways. Let's start with the math way, with two cases, like in the lesson. Case "
        "one, the drink is espresso.", show(g35a['line'], 'Case one, the drink is espresso')),
      L("The drink has one option, espresso. And then the pastry must be a croissant, also one option.",
        show(g35a['a'], 'The drink has one option'), show(g35a['b'], 'also one option')),
      L("One times one is one choice.", show(g35a['x'], 'One times one'), show(g35a['eq'], 'is one choice')),
      L("Case two, any other drink. Six drinks minus espresso leaves five options.", show(g35b['line'], 'Case two, any other drink'),
        show(g35b['a'], 'leaves five options')),
      L("With these drinks, any pastry is allowed. The croissant too. So five options.", show(g35b['b'], 'So five options')),
      L("Five times five is twenty-five choices.", show(g35b['x'], 'Five times five'), show(g35b['eq'], 'is twenty-five choices')),
      L("A drink is espresso or it isn't, so the cases don't overlap. We add them. One plus twenty-five is twenty-six.",
        show(g35c, 'One plus twenty-five is twenty-six')),
      L("Careful here. The rule works one way only. Espresso needs a croissant, but a croissant still goes with any other "
        "drink. If you take the croissant away from the other drinks, you get five times four plus one, twenty-one. "
        "That's choice number two, a trap.", show(g35d, 'five times four plus one'), mk('cross', 'choice 2', "That's choice number two"))),
    S('Method 2 · The math way: all minus forbidden',
      L("[pause] Now let's count it the other way, all minus forbidden. With no rule at all, six drinks times five pastries "
        "is thirty.", show(g35e, 'six drinks times five pastries')),
      L("Which choices does the rule forbid? Espresso with a pastry that isn't a croissant. There are four such pastries, "
        "so four forbidden choices.", show(g35f, 'Espresso with a pastry')),
      L("Thirty minus four is twenty-six. The same answer.", show(g35g, 'Thirty minus four')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g136 (two dice, sum not 8)
# Hebrew (wp 8865-8953, two fair dice, sum not 4): "much easier to work backwards": all 36 minus the 3 outcomes of sum 4
# = 33; listing the allowed ones directly is possible but messier. English: green and yellow dice, sum not 8: 36 - 5 = 31
# (the colours make 2-6 and 6-2 different; 4-4 is one outcome); Method 2 the direct count, row by row (6 + 5 x 5 = 31).
# "Fair" is taught in topic 29 (the English stem has no "fair"). The grid of sums is the picture.
_G = [[str(g + y) for y in range(1, 7)] for g in range(1, 7)]
g36G = LIST28('g36G', 6, 6, [('rows', [('r', i, _G[i]) for i in range(6)] + [('note', i, 'green %d' % (i + 1), 'ink') for i in range(6)]),
                             ('h8', [('hl', 1, 5), ('hl', 2, 4), ('hl', 3, 3), ('hl', 4, 2), ('hl', 5, 1)]),
                             ('f', [('foot', 'green down, yellow across', 'ink')])],
              head=['1', '2', '3', '4', '5', '6'], cellw=56, cellh=44, right=130, gapc=6, w=520, size=30, col=1,
              title='Green down, yellow across: the sums')
g36a = IH('g36a', 'all: $\\ 6\\times6=36$', size=32)
g36b = IH('g36b', 'sum $8$: $\\ 2+6,\\ 3+5,\\ 4+4,\\ 5+3,\\ 6+2$', size=30)
g36c = IH('g36c', '$36-5=31$', size=34)
g36d = IH('g36d', '$36-3=33$: $\\ $order ignored', size=30)
g36e = IH('g36e', 'green $1$: $\\ $all $6$ allowed', size=30)
g36f = IH('g36f', 'green $2$ to $6$: $\\ 5$ each, $\\ 5\\times5=25$', size=30)
g36g = IH('g36g', '$6+25=31$', size=34)
video('solve-wp28-g136', 'solution', qid='wp28-g136', slides=[
    S('Method 1 · The math way: all minus forbidden',
      L("A green dice and a yellow dice each show a number from one to six. How many ordered outcomes have a sum "
        "different from eight?", pt('stem', 'A green dice and a yellow dice', 'hl', 7.0), voice='calm', pause=0.5),
      L("So they ask for the outcomes whose sum is not eight. The word different is our cue, like in the lesson.",
        pt('stem: ask', 'whose sum is not eight')),
      L("We could list every outcome whose sum isn't eight, but that's long and messy. It's much easier to work "
        "backwards. We'll solve it in two different ways. Let's start with the math way, all minus forbidden."),
      L("All the outcomes first. The green dice has six options, and the yellow dice six. Six times six is thirty-six.",
        show(g36a, 'Six times six is thirty-six'), show(g36G['line'], 'Six times six'), show(g36G['rows'], 'Six times six is thirty-six'), show(g36G['f'], 'Six times six is thirty-six')),
      L("Now the forbidden ones, a sum of eight. Two and six, three and five, four and four, five and three, and six and "
        "two.", show(g36b, 'Two and six'), show(g36G['h8'], 'Two and six')),
      L("Why are two and six, and six and two, both there? Because the dice have colours. A two on the green and a six on "
        "the yellow is a different outcome from a six on the green and a two on the yellow."),
      L("And four and four is just one outcome. So there are five forbidden outcomes."),
      L("Thirty-six minus five is thirty-one.", show(g36c, 'Thirty-six minus five')),
      L("If you ignore the colours, you count only three forbidden pairs, and you get thirty-three. That's choice number "
        "one, a trap.", show(g36d, 'you get thirty-three'), mk('cross', 'choice 1', "That's choice number one"))),
    S('Method 2 · The math way: a direct count',
      L("[pause] Now let's count the allowed outcomes directly, row by row. This way is longer, but it's a good check."),
      L("If the green dice shows one, the yellow would need seven for a sum of eight. That's impossible. So all six yellow "
        "numbers are allowed.", show(g36e, 'all six yellow numbers are allowed')),
      L("If the green dice shows two, three, four, five or six, exactly one yellow number makes eight. So five yellow "
        "numbers are allowed each time. Five times five is twenty-five.", show(g36f, 'Five times five is twenty-five')),
      L("Six plus twenty-five is thirty-one. The same answer.", show(g36g, 'Six plus twenty-five')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-137 (lesson: choosing a group)
# Hebrew (wp 8955-9216): until now the order of picking mattered (a row); choosing a group: "edge questions, very hard and
# very rare"; 10 children, choose 4: Danny-then-Yossi = Yossi-then-Danny -> a doubling; "a rule full of words sounds like
# Chinese to me, let's see an example"; the kindergarten: 6 x 5 x 4, the same 3 children picked in 6 orders = one group,
# the internal arrangements 3! (lining the 3 up), 6 x 5 x 4 / 3! = 20, "a regular calculation, divided by the factorial
# of the number chosen"; the complementary choice n - 1 of n = n ("choose the one who stays aside", 5 of 6 -> 6, also by
# the group formula), "the group type is very rare, the complementary type more common, and simple". English (R37, new
# numbers, the small cases LISTED before the rule): 2 of 4 (12 ordered pairs, each pair twice, 6 pairs listed); 3 of 5
# (60, the group ABC in 6 orders, 60 / 6 = 10); 4 of 6 with step-by-step cancelling (15); who stays out (4 of 5 = 5,
# listed, and by the formula); the smaller side (7 of 9 = 2 of 9 = 36); roles or no roles (210 vs 35, the report's
# "choices differ by a factor"); the checklist on the board. Real exam: 2023_autumn_q2_07 (3 of 4 = 4), 2020_winter_q2_06.
_OP = [['AB', 'AC', 'AD'], ['BA', 'BC', 'BD'], ['CA', 'CB', 'CD'], ['DA', 'DB', 'DC']]
q_a0 = I('q_a0', '$4$ friends: $\\ $choose $2$ for a trip', size=34)
q_a1 = IH('q_a1', 'as usual: $\\ 4\\times3=12$', size=32)
q_aL = LIST28('q_aL', 4, 3, [('r', [('r', i, _OP[i]) for i in range(4)]), ('ab', [('hl', 0, 0), ('hl', 1, 0)]),
                             ('f', [('foot', 'each pair twice')])], cellw=70, cellh=46, right=20, gapc=10, w=300, col=1,
              title='In order')
q_a2 = IH('q_a2', '$12\\div2=6$ pairs', size=34)
q_a3 = IH('q_a3', 'AB, $\\ $AC, $\\ $AD, $\\ $BC, $\\ $BD, $\\ $CD', size=32)
q_b0 = I('q_b0', '$5$ friends, $\\ $A to E: $\\ $choose $3$', size=34)
q_b1 = IH('q_b1', 'as usual: $\\ 5\\times4\\times3=60$', size=32)
q_bL = LIST28('q_bL', 6, 3, [('a', [('r', 0, 'ABC'), ('r', 1, 'ACB'), ('r', 2, 'BAC'), ('r', 3, 'BCA'), ('r', 4, 'CAB'), ('r', 5, 'CBA')]),
                             ('g', [('ring', 0, 5, 'one group')])], cellw=56, cellh=44, right=170, gapc=6, w=380, col=1,
              title='The group A, B, C picked in order')
q_b2 = IH('q_b2', '$3!=3\\times2\\times1=6$ orders', size=32)
q_b3 = IH('q_b3', '$60\\div6=10$ groups', size=34)
q_r0 = I('q_r0', 'A group: $\\ $count as usual, $\\ $then divide by $k!$', size=36)
q_r1 = I('q_r1', '$k$ = how many we choose', size=32)
q_r2 = IH('q_r2', '$2$ chosen: $\\ \\div2$', size=32, col=1)
q_r3 = IH('q_r3', '$3$ chosen: $\\ \\div6$', size=32, col=1)
q_r4 = IH('q_r4', '$4$ chosen: $\\ \\div24$', size=32, col=1)
q_c0 = I('q_c0', '$6$ people: $\\ $choose $4$', size=34)
q_c1 = I('q_c1', '$\\dfrac{6\\times5\\times4\\times3}{4\\times3\\times2\\times1}$', size=42)
q_c2 = IH('q_c2', 'cancel $4$ and $3$: $\\ {6\\times5/2\\times1}$', size=32)
q_c3 = IH('q_c3', '$30\\div2=15$ groups', size=34)
q_d0 = I('q_d0', '$5$ friends: $\\ $choose $4$', size=34)
q_dL = LIST28('q_dL', 5, 1, [('a', [('c', 0, 0, 'A stays out:  B C D E')]), ('b', [('c', 1, 0, 'B stays out:  A C D E')]),
                             ('c', [('c', 2, 0, 'C stays out:  A B D E'), ('c', 3, 0, 'D stays out:  A B C E'),
                                    ('c', 4, 0, 'E stays out:  A B C D')]), ('f', [('foot', '5 groups')])],
              cellw=420, cellh=46, right=10, w=440, size=28, title='Who stays out')
q_d1 = I('q_d1', 'Choose $n-1$ out of $n$: $\\ n$ ways', size=36)
q_d2 = IH('q_d2', '${5\\times4\\times3\\times2/4!}={120/24}=5$', size=32, col=1)
q_e0 = I('q_e0', '$9$ people: $\\ $choose $7$', size=34)
q_e1 = IH('q_e1', '$=$ choose the $2$ who stay out', size=32)
q_e2 = IH('q_e2', '${9\\times8/2}=36$', size=34)
q_e3 = I('q_e3', 'Always count the smaller side.', size=34)
q_f0 = I('q_f0', '$7$ people: $\\ $choose $3$', size=34)
q_f1 = IH('q_f1', 'roles: $\\ 7\\times6\\times5=210$', size=32)
q_f2 = IH('q_f2', 'a group: $\\ 210\\div6=35$', size=32)
q_g1 = I('q_g1', '1. Does the order matter? $\\ $A row or a code: yes. $\\ $A group: no.', size=30)
q_g2 = I('q_g2', '2. Can items repeat? $\\ $The pool stays full, $\\ $or it shrinks.', size=30)
q_g3 = I('q_g3', '3. A restriction? $\\ $Start with it. $\\ $A forced stage gets $1$.', size=30)
q_g4 = I('q_g4', '4. Counted twice? $\\ $Divide by $2$, $\\ $or by $k!$.', size=30)
q_g5 = I('q_g5', '5. One count, or cases? $\\ $"Not": $\\ $all minus forbidden.', size=30)
_wp137 = [
    S('Choosing a Group',
      L("Until now, the order we picked in mattered. A row changes when two people swap places."),
      L("Now we choose a group, where the order doesn't matter. Picking Ann and then Ben gives the same group as picking "
        "Ben and then Ann."),
      L("A general group question is rare on the exam, and hard. But one simple kind of group question comes up more "
        "often. We'll see both.")),
    S('Two of four',
      L("Let's start small. Four friends, A, B, C and D. We choose two of them for a trip. How many pairs can we choose?",
        show(q_a0, 'Four friends, A, B, C and D')),
      L("First, let's count as usual, as if the order mattered. Four options for the first, and three for the second. Four "
        "times three is twelve.", show(q_a1, 'Four times three is twelve')),
      L("Here are the twelve, in order.", show(q_aL['line'], 'Here are the twelve'), show(q_aL['r'], 'Here are the twelve')),
      L("Look at A B and B A. Picking A first and B second, or B first and A second, gives the same pair. It's the same "
        "trip.", show(q_aL['ab'], 'Look at A B and B A')),
      L("And that's true for every pair. Each pair appears twice in our twelve.", show(q_aL['f'], 'Each pair appears twice')),
      L("So twelve divided by two is six pairs.", show(q_a2, 'twelve divided by two')),
      L("Let's write them. A B, A C, A D, B C, B D and C D. Six pairs.", show(q_a3, "Let's write them"))),
    S('Three of five',
      L("Now a new example. Five friends, A to E. We choose three of them. How many groups?", show(q_b0, 'Five friends, A to E')),
      L("As usual first. Five, then four, then three. Five times four is twenty. Then twenty times three is sixty.",
        show(q_b1, 'Five times four is twenty')),
      L("But how many times does each group appear in the sixty? Take the group A, B and C. We could pick it in this "
        "order, A, B, C.", show(q_bL['line'], 'Take the group A, B and C')),
      L("Or A, C, B. Or B first, or C first. Here are all the orders. It's six orders, and it's one group.",
        show(q_bL['a'], 'Here are all the orders'), show(q_bL['g'], "and it's one group")),
      L("Six is three factorial, the number of ways to line up three people in a row.", show(q_b2, 'Six is three factorial')),
      L("So every group was counted six times. Sixty divided by six is ten groups.", show(q_b3, 'Sixty divided by six'))),
    S('The rule',
      L("So here's the rule for a group. Count as usual, as if the order mattered. Then divide by k factorial.",
        show(q_r0, 'Count as usual')),
      L("k is the number of people we choose.", show(q_r1, 'k is the number')),
      L("Why k factorial? The k people we chose can be lined up in k factorial orders. In the usual count, each of those "
        "orders was counted. But all of them are the same group."),
      L("So two chosen, divide by two. Three chosen, divide by six. Four chosen, divide by twenty-four.",
        show(q_r2, 'two chosen'), show(q_r3, 'Three chosen'), show(q_r4, 'Four chosen'))),
    S('Cancel first',
      L("Now a new example. Six people, and we choose four of them.", show(q_c0, 'Six people')),
      L("As usual, six times five times four times three. Then we divide by four factorial, four times three times two "
        "times one.", show(q_c1, 'Then we divide by four factorial')),
      L("Don't multiply it all out. Cancel first. The four on top cancels with the four below, and the three with the "
        "three. What's left is six times five, over two times one.", show(q_c2, 'Cancel first')),
      L("Six times five is thirty. Then thirty divided by two is fifteen groups.", show(q_c3, 'thirty divided by two'))),
    S('Who stays out',
      L("Now the simpler kind of group. We choose all of them except one."),
      L("Five friends, and we choose four of them.", show(q_d0, 'Five friends, and we choose four')),
      L("Instead of choosing the four who go, let's choose the one who stays out.", show(q_dL['line'], 'the one who stays out')),
      L("If A stays out, the group is B, C, D and E.", show(q_dL['a'], 'If A stays out')),
      L("If B stays out, the group is A, C, D and E.", show(q_dL['b'], 'If B stays out')),
      L("And the same for C, D and E. Each friend who stays out gives a different group. So five groups.",
        show(q_dL['c'], 'And the same for C, D and E'), show(q_dL['f'], 'So five groups')),
      L("So choosing n minus one out of n always gives n. This kind comes up on the exam more often than a general group, "
        "and it's easy.", show(q_d1, 'choosing n minus one out of n')),
      L("And the group rule agrees. Five times four times three times two is a hundred twenty. Divided by four factorial, "
        "twenty-four, it's five.", show(q_d2, 'And the group rule agrees'))),
    S('The smaller side',
      L("It works for more than one person too. Now a new example. Nine people, and we choose seven.", show(q_e0, 'Nine people')),
      L("Choosing the seven who go is the same as choosing the two who stay out.", show(q_e1, 'choosing the two who stay out')),
      L("Two of nine is nine times eight, divided by two factorial, two. Nine times eight is seventy-two. Then seventy-two "
        "divided by two is thirty-six.", show(q_e2, 'Nine times eight is seventy-two')),
      L("That's much faster than dividing by seven factorial. So always count the smaller side.", show(q_e3, 'always count the smaller side'))),
    S('Does the order matter?',
      L("So before you divide, ask again. Does the order matter here?"),
      L("Seven people, and we choose three of them.", show(q_f0, 'Seven people, and we choose three')),
      L("If the three get roles, a president, a secretary and a treasurer, the order matters. Seven times six times five "
        "is two hundred ten. We don't divide.", show(q_f1, 'Seven times six times five')),
      L("If it's a group with no roles, we divide by three factorial. Two hundred ten divided by six is thirty-five.",
        show(q_f2, 'Two hundred ten divided by six')),
      L("Both numbers often appear in the choices. So the question tells you which one, by the roles.")),
    S('The checklist',
      L("Now you have the main tools. Here's the order to think in, for every counting question.",
        show(q_g1, 'the order to think in'), show(q_g2, 'the order to think in'), show(q_g3, 'for every counting question'),
        show(q_g4, 'for every counting question'), show(q_g5, 'for every counting question')),
      L("Take a moment to read it. It's on your summary page too."),
      L("So let's sum it up. For a group, count as usual and divide by k factorial. And if you choose almost everyone, "
        "choose who stays out instead."),
      L("I'll see you in the next video.")),
]
video('wp-137', 'lesson', slides=_wp137)
SPLITS.append(('wp-137', 'Choosing a Group', [
    (1, None),
    (5, "Let's continue, with a simpler kind of group.")]))

# ------------------------------------------------------------------------------------------------ g139 (11 of 12 players)
# Hebrew (wp 9095-9216, 5 of 6 children): n - 1 of n = n; why: choose the one left aside (she goes through the 6
# children); also by the group method, 6 x 5 x 4 x 3 x 2 / 5! = 6; "once you spot n - 1 of n, you know the answer is
# n". English: 11 of 12 -> 12; both methods (the report). The lesson (wp-137 part 2) taught it: "like in the lesson".
g39L = LIST28('g39L', 3, 1, [('a', [('c', 0, 0, 'player 1 stays out')]), ('b', [('c', 1, 0, 'player 2 stays out')]),
                             ('c', [('c', 2, 0, '... player 12 stays out')]), ('f', [('foot', '12 teams')])],
              cellw=380, cellh=46, right=10, w=420, size=28, title='Who stays out')
g39a = I('g39a', '$\\dfrac{12\\times11\\times10\\times\\dots\\times2}{11\\times10\\times\\dots\\times2\\times1}$', size=40)
g39b = IH('g39b', 'cancel $11$ down to $2$: $\\ 12$', size=32)
video('solve-wp28-g139', 'solution', qid='wp28-g139', slides=[
    S('Method 1 · Insight: who stays out',
      L("In how many different ways can a team of eleven players be chosen from a squad of twelve players?",
        pt('stem', 'In how many different ways', 'hl', 5.0), voice='calm', pause=0.5),
      L("So we choose a team, a group. The order doesn't matter. And eleven out of twelve is all of them except one.",
        pt('stem', 'eleven out of twelve')),
      L("We'll solve it in two different ways. Let's start with the insight, who stays out, like in the lesson. Instead of "
        "choosing the eleven players who play, we choose the one player who stays out.", show(g39L['line'], 'the one player who stays out')),
      L("If player one stays out, the other eleven are the team. If player two stays out, that's another team.",
        show(g39L['a'], 'If player one stays out'), show(g39L['b'], 'If player two stays out')),
      L("And so on, up to player twelve. Each player who stays out gives a different team. So there are twelve teams.",
        show(g39L['c'], 'And so on, up to player twelve'), show(g39L['f'], 'So there are twelve teams')),
      L("Careful, eleven is choice number three, and it's a trap. It counts the players in the team, not the ways to "
        "choose it.", mk('cross', 'choice 3', "it's a trap"))),
    S('Method 2 · The math way: the group rule',
      L("[pause] Now the math way, with the group rule from the lesson. We count as usual, twelve, then eleven, and so on "
        "down to two, for the eleven players."),
      L("Then we divide by eleven factorial, because the order inside the team doesn't matter.", show(g39a, 'we divide by eleven factorial')),
      L("Everything from eleven down to two cancels. What's left is twelve.", show(g39b, 'Everything from eleven down to two cancels')),
      L("So once you see n minus one out of n, you can skip this calculation. The answer is n."),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g138 (10 hikers, two guides)
# Hebrew (wp 8988-9094, the kindergarten: 6 children into two groups of 3 with different teachers): 6 x 5 x 4 as usual;
# the same 3 children picked in 6 orders = one group; internal arrangements 3!; 6 x 5 x 4 / 3! = 20. English: 10 hikers,
# 5 to Lena, 5 to Omar: 10 x 9 x 8 x 7 x 6 / 5! = 252, cancelled step by step (R36); the second group is decided; Method
# 2 by understanding: the guides have names, so no halving (126 is that trap). Traps: 30,240 (no dividing).
g38n = IH('g38n', '$10\\times9\\times8\\times7\\times6$', size=32)
g38a = I('g38a', '$\\dfrac{10\\times9\\times8\\times7\\times6}{5\\times4\\times3\\times2\\times1}$', size=42)
g38b = IH('g38b', '$5\\times2=10$: $\\ $cancels the $10$', size=30)
g38c = IH('g38c', '$9\\div3=3$', size=30)
g38d = IH('g38d', '$8\\div4=2$', size=30)
g38e = IH('g38e', '$3\\times2\\times7\\times6$', size=30, col=1)
g38f = IH('g38f', '$6\\times7=42$, $\\ 42\\times6=252$', size=30, col=1)
g38g = IH('g38g', 'Omar: $\\ $the other $5$, $\\ 1$ way', size=30, col=1)
g38h = IH('g38h', 'Lena: $1$ to $5$, $\\ $Omar: $6$ to $10$', size=30)
g38i = IH('g38i', 'Lena: $6$ to $10$, $\\ $Omar: $1$ to $5$', size=30)
g38j = IH('g38j', '$252\\div2=126$: $\\ $only with no names', size=30)
video('solve-wp28-g138', 'solution', qid='wp28-g138', slides=[
    S('Method 1 · The math way: the group rule',
      L("Ten hikers are split between two guides, Lena and Omar, with five hikers assigned to each guide. How many "
        "different splits are possible?", pt('stem', 'Ten hikers are split', 'hl', 8.0), voice='calm', pause=0.5),
      L("So each guide gets a group of five. Inside a group, the order doesn't matter.", pt('stem: given', 'each guide gets a group of five')),
      L("We'll solve it the math way, with the group rule from the lesson, and then check one more thing by understanding. "
        "Let's choose Lena's five hikers first, as usual, as if the order mattered."),
      L("The first hiker has ten options, then nine, eight, seven and six.", show(g38n, 'The first hiker has ten options')),
      L("But picking Rita first and Ben second, or Ben first and Rita second, gives the same group. So we divide by the "
        "orders of five hikers, five factorial.", show(g38a, 'So we divide by the orders')),
      ),
    S('Method 1 · The math way: the group rule',
      L("Let's cancel, one step at a time. Five times two is ten, and that cancels the ten on top.", show(g38b, 'Five times two is ten')),
      L("Nine divided by three is three.", show(g38c, 'Nine divided by three')),
      L("Eight divided by four is two.", show(g38d, 'Eight divided by four')),
      L("What's left is three times two times seven times six.", show(g38e, "What's left is three times two")),
      L("Three times two is six. Then six times seven is forty-two. Forty-two times six is two hundred fifty-two.",
        show(g38f, 'six times seven is forty-two')),
      L("And Omar's group? There's no choice left. The other five hikers go to Omar, so that's one way.",
        show(g38g, "And Omar's group")),
      L("If you forget to divide, you get thirty thousand two hundred forty, choice number four. That counts every order "
        "of Lena's group.", mk('cross', 'choice 4', 'choice number four'))),
    S('Method 2 · Understanding: the guides have names',
      L("[pause] Now by understanding. Should we also divide by two, because there are two groups? Let's think."),
      L("Say hikers one to five go with Lena, and six to ten go with Omar.", show(g38h, 'hikers one to five go with Lena')),
      L("Now swap them. Six to ten with Lena, and one to five with Omar. Is it the same split? No, because the guides have "
        "names. Each hiker has a different guide now.", show(g38i, 'Now swap them')),
      L("So we don't divide by two. Only if the two groups had no names would swapping them change nothing. Then we would "
        "get a hundred twenty-six, choice number one. Here that's a trap.", show(g38j, 'a hundred twenty-six'),
        mk('cross', 'choice 1', 'choice number one')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g140 (9! / 7!)
# Hebrew (wp 9219-9271, 6! / 4!, "easy plus"): n items in a row = n!; write both out and cancel -> 6 x 5; the shortcut:
# 6! = 6 x 5!, = 6 x 5 x 4!, cancel the 4!. English: 9! / 7! = 72, both ways (the report). "Stop early" is first used
# here (her Method 2), so it's taught here; the factorial lesson (wp-140-after) comes right after and reminds it.
# Traps: 63 = 9 x 7 (skips the 8), 81 = 9 x 9.
g40a = I('g40a', '$\\dfrac{9!}{7!}$', size=44)
g40b = I('g40b', '$\\dfrac{9\\times8\\times7\\times6\\times5\\times4\\times3\\times2\\times1}{7\\times6\\times5\\times4\\times3\\times2\\times1}$', size=36)
g40c = IH('g40c', 'cancel $7$ down to $1$: $\\ 9\\times8$', size=30)
g40d = IH('g40d', '$9\\times8=72$', size=34)
g40e = IH('g40e', '$9!=9\\times8\\times7!$', size=34)
g40f = I('g40f', '$\\dfrac{9\\times8\\times7!}{7!}=9\\times8=72$', size=40)
g40g = IH('g40g', '$9\\times7=63$: $\\ $the $8$ is missing', size=30, col=1)
video('solve-wp28-g140', 'solution', qid='wp28-g140', slides=[
    S('Method 1 · The math way: write it out',
      L("What is the ratio of the number of row arrangements of nine distinct objects, to the number of row arrangements "
        "of seven distinct objects?", pt('stem', 'What is the ratio', 'hl', 7.0), voice='calm', pause=0.5),
      L("So they ask for the rows of nine, divided by the rows of seven. Distinct means different. This is an easy one, "
        "and a good reminder of factorials.", pt('stem: ask', 'the rows of nine, divided by')),
      L("We'll solve it in two different ways. Let's start with the math way. How many ways can n different objects stand "
        "in a row? n factorial, like in the lesson on the pool. So the ratio is nine factorial over seven factorial.",
        show(g40a, 'So the ratio is nine factorial')),
      L("Let's write both of them out. Nine factorial is nine times eight times seven, and so on down to one. Seven "
        "factorial is seven times six, and so on down to one.", show(g40b, "Let's write both of them out")),
      L("Everything from seven down to one is on top and below, so it cancels.", show(g40c, 'so it cancels')),
      L("What's left is nine times eight. That's seventy-two.", show(g40d, "What's left is nine times eight"))),
    S('Method 2 · The math way: stop early',
      L("[pause] Now a shorter way. Some students don't write all that. They shorten it, because they understand what a "
        "factorial is."),
      L("Look at nine factorial. After nine and eight comes seven times six, and so on down to one. And that tail is "
        "exactly seven factorial."),
      L("So nine factorial is nine times eight times seven factorial. We stop there, because that's what we need.",
        show(g40e, 'So nine factorial is nine times eight')),
      L("Now seven factorial cancels, on top and below, in one move. Nine times eight is seventy-two again. And we never had to calculate "
        "nine factorial, which is a huge number.", show(g40f, 'seven factorial cancels')),
      L("Careful with choice number four, sixty-three. That's nine times seven, and it skips the eight. The run goes nine, "
        "then eight, then the seven factorial.", show(g40g, "That's nine times seven"), mk('cross', 'choice 4', 'choice number four')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-140-after (lesson: factorials)
# Hebrew (wp 9272-9301, inside Q140): factorial questions can be pure expressions (n! x (n+1)!); the psychometric way
# first: plug in a number (3! x 4!); then the math: (n+1)! = (n+1) x n!, so the product is (n!)^2 (n+1). The old
# "quick extension" becomes a real R37 lesson (exam-coverage gap 1: 12 exam items, F1-F5; the audit asks for factorials
# as a real lesson: by sight, stop early, a run of neighbours and backwards, take out the smaller factorial, counting
# primes; external tracker row 28). Three parts. New numbers: a! = 12 x 10 and 8 x 90; 10!/8!, 12!/11!; 7!/4! = 210;
# backwards 30 = 5 x 6 and 90 = 9 x 10; (n+1)!/(n-1)! at n = 3; n! x (n+2)! at n = 2 (48), and not 6! (720); 6! + 5!
# = 840, 7! - 6! = 4320 (each checked by the plain numbers); 6! = 2^4 x 3^2 x 5 (four twos, not three); 3! x 2^3 = 2 x
# 4 x 6. Real exam: 2020_autumn_q1_04, 2025_spring_q1_14 (F1); 2021_autumn_q2_05, 2022_autumn_q1_17, 2026_spring_q2_18,
# 2022_winter_q2_07, 2025_winter_q1_07 (F2); 2020_winter_q1_19, 2024_winter_q2_17 (F3); 2019_winter_q2_16 (F4);
# 2025_autumn_q1_17 (F5).
f_v0 = TBL('f_v0', ['1!', '2!', '3!', '4!', '5!', '6!', '7!'], [''], [
    ('a', [('c', 0, 0, '1'), ('c', 0, 1, '2'), ('c', 0, 2, '6')]), ('b', [('c', 0, 3, '24'), ('c', 0, 4, '120')]),
    ('c', [('c', 0, 5, '720')]), ('d', [('c', 0, 6, '5040')])], colw=118, labw=0, rowh=66, headh=56, w=860, size=34,
    title='Factorials to know')
f_v1 = IH('f_v1', '$5!=5\\times24=120$', size=32, col=1)
f_v2 = IH('f_v2', '$6!=6\\times120=720$', size=32, col=1)
f_v3 = IH('f_v3', '$7!=7\\times720=5040$', size=32, col=1)
f_v4 = I('f_v4', '$a!=12\\times10$, $\\ a=?$', size=36)
f_v5 = IH('f_v5', '$12\\times10=120=5!$, $\\ a=5$', size=32)
f_v6 = I('f_v6', '$b!=8\\times90$, $\\ b=?$', size=36)
f_v7 = IH('f_v7', '$8\\times90=720=6!$, $\\ b=6$', size=32)
f_v8 = IH('f_v8', '$0!=1$', size=32, col=1)
f_s0 = IH('f_s0', '$8!=8\\times7!$', size=34)
f_s1 = IH('f_s1', '$8!=8\\times7\\times6!$', size=34)
f_s2 = I('f_s2', '$\\dfrac{10!}{8!}=\\dfrac{10\\times9\\times8!}{8!}=10\\times9=90$', size=40)
f_s3 = IH('f_s3', '$(n+1)!=(n+1)\\times n!$', size=34)
f_s4 = IH('f_s4', '$4!=4\\times3!$: $\\ 24=4\\times6$', size=32, col=1)
f_s5 = I('f_s5', '$\\dfrac{12!}{11!}=12$', size=40)
f_s6 = I('f_s6', '$\\dfrac{n!}{(n-1)!}=n$', size=40)
f_r0 = I('f_r0', '$\\dfrac{7!}{4!}=\\dfrac{7\\times6\\times5\\times4!}{4!}$', size=40)
f_r1 = IH('f_r1', '$7\\times6\\times5=210$', size=34)
f_r2 = I('f_r2', '$\\dfrac{b!}{a!}$: $\\ $neighbours from $a+1$ to $b$', size=34)
f_r3 = I('f_r3', '$\\dfrac{b!}{a!}=30$, $\\ b>a$', size=38)
f_r4 = IH('f_r4', '$30=5\\times6$', size=34)
f_r5 = IH('f_r5', 'the run ends at $6$: $\\ b=6$', size=32)
f_r6 = IH('f_r6', 'it starts at $5$, $\\ $right after $a$: $\\ a=4$', size=32)
f_r7 = IH('f_r7', 'check: $\\ \\frac{6!}{4!}=6\\times5=30$', size=32, col=1)
f_r8 = I('f_r8', '$\\dfrac{b!}{a!}=90$', size=38)
f_r9 = IH('f_r9', '$90=9\\times10$: $\\ b=10$, $\\ a=8$', size=32)
f_p0 = I('f_p0', '$\\dfrac{(n+1)!}{(n-1)!}=?$', size=40)
f_p1 = IH('f_p1', '$n=3$: $\\ \\frac{4!}{2!}=\\frac{24}{2}=12$', size=32)
f_p2 = IH('f_p2', '$n\\times(n+1)=3\\times4=12$', size=32, col=1)
f_p3 = I('f_p3', '$(n+1)!=(n+1)\\times n\\times(n-1)!$', size=36)
f_p4 = I('f_p4', '$\\dfrac{(n+1)\\times n\\times(n-1)!}{(n-1)!}=n\\times(n+1)$', size=38)
f_q0 = I('f_q0', '$n!\\times(n+2)!=?$', size=40)
f_q1 = IH('f_q1', '$n=2$: $\\ 2!\\times4!=2\\times24=48$', size=32)
f_q2 = IH('f_q2', '$(n+2)!=(n+2)\\times(n+1)\\times n!$', size=32)
f_q3 = I('f_q3', '$n!\\times(n+2)!=(n!)^2\\times(n+1)\\times(n+2)$', size=36)
f_q4 = IH('f_q4', '$n=2$: $\\ 2^2\\times3\\times4=48$', size=32, col=1)
f_q5 = IH('f_q5', '$2!\\times4!=48$, $\\ $but $6!=720$', size=32, col=1)
f_t0 = I('f_t0', '$6!+5!=?$', size=40)
f_t1 = IH('f_t1', '$6!=6\\times5!$', size=32)
f_t2 = IH('f_t2', '$6\\times5!+1\\times5!=5!\\times(6+1)$', size=32)
f_t3 = IH('f_t3', '$=7\\times120=840$', size=32)
f_t4 = IH('f_t4', 'check: $\\ 720+120=840$', size=32, col=1)
f_t5 = I('f_t5', '$7!-6!=?$', size=40)
f_t6 = IH('f_t6', '$7!-6!=6!\\times(7-1)=6\\times720$', size=32)
f_t7 = IH('f_t7', '$6\\times700=4200$, $\\ 6\\times20=120$, $\\ 4320$', size=30)
f_t8 = IH('f_t8', 'check: $\\ 5040-720=4320$', size=32, col=1)
f_t9 = IH('f_t9', '$7!-6!\\ne1!$', size=32, col=1)
f_u0 = I('f_u0', '$6!=6\\times5\\times4\\times3\\times2\\times1$', size=38)
f_u1 = IH('f_u1', '$6=2\\times3$, $\\ 4=2\\times2$', size=32)
f_u2 = IH('f_u2', 'twos: $\\ 1+2+1=4$', size=32)
f_u3 = IH('f_u3', 'threes: $\\ 2$, $\\ $fives: $\\ 1$', size=32)
f_u4 = IH('f_u4', '$6!=2^4\\times3^2\\times5$', size=36)
f_u5 = IH('f_u5', '$16\\times9=144$, $\\ 144\\times5=720$', size=30, col=1)
f_u6 = IH('f_u6', '$32=2^5$: $\\ $only four twos, $\\ $no', size=32)
f_u7 = IH('f_u7', '$45=3^2\\times5$: $\\ $yes', size=32)
f_u8 = IH('f_u8', '$3$ even numbers, $\\ $but $4$ twos', size=32)
f_u9 = IH('f_u9', '$7!=2^4\\times3^2\\times5\\times7$', size=34)
f_w0 = I('f_w0', '$3!\\times2^3=6\\times8=48$', size=38)
f_w1 = IH('f_w1', '$2\\times4\\times6=48$', size=34)
f_w2 = IH('f_w2', '$(1\\times2)\\times(2\\times2)\\times(3\\times2)$', size=32)
f_w3 = I('f_w3', '$k!\\times2^k=2\\times4\\times6\\times\\dots\\times2k$', size=36)
f_z1 = I('f_z1', 'Know $120$, $\\ 720$, $\\ 5040$ by sight.', size=34)
f_z2 = I('f_z2', 'Stop early: $\\ 9!=9\\times8\\times7!$', size=34)
f_z3 = I('f_z3', '$\\dfrac{b!}{a!}$: $\\ $a run of neighbours', size=34)
f_z4 = I('f_z4', 'A sum or a difference: $\\ $take out the smaller one', size=34)
f_z5 = I('f_z5', 'Divisible? $\\ $Count the primes.', size=34)
_wp140 = [
    S('Factorials',
      L("In the last question we used factorials. Factorials come up on the exam quite often, also as pure math, with no "
        "story at all."),
      L("So let's learn the tools, one at a time, with examples.")),
    S('Know them by sight',
      L("First, the factorials to know by heart. One factorial is one, two factorial is two, and three factorial is six.",
        show(f_v0['line'], 'the factorials to know by heart'), show(f_v0['a'], 'three factorial is six')),
      L("Four factorial is twenty-four. Five factorial is five times twenty-four, a hundred twenty.",
        show(f_v0['b'], 'Five factorial is five times'), show(f_v1, 'Five factorial is five times')),
      L("Each one is the one before, times the next number. Six factorial is six times a hundred twenty, seven hundred "
        "twenty.", show(f_v2, 'Six factorial is six times'), show(f_v0['c'], 'seven hundred twenty')),
      L("And seven factorial is seven times seven hundred twenty, five thousand forty.", show(f_v3, 'seven times seven hundred twenty'),
        show(f_v0['d'], 'five thousand forty')),
      L("One more fact. Zero factorial is one, by definition. It comes up rarely, but now you know it.", show(f_v8, 'Zero factorial is one'))),
    S('Spot them in a question',
      L("Why know them by sight? Because the exam hides them. Now a new example. a factorial is twelve times ten. What "
        "is a?", show(f_v4, 'a factorial is twelve times ten')),
      L("Twelve times ten is a hundred twenty, and a hundred twenty is five factorial. So a is five.", show(f_v5, 'Twelve times ten')),
      L("One more. b factorial is eight times ninety. Eight times ninety is seven hundred twenty, and that's six factorial. "
        "So b is six.", show(f_v6, 'b factorial is eight times ninety'), show(f_v7, 'Eight times ninety is seven hundred twenty'))),
    S('Stop early',
      L("The second tool is the one from the last question. We expand a factorial only as far as we need."),
      L("Eight factorial is eight times seven factorial. Or, if we need it, eight times seven times six factorial.",
        show(f_s0, 'Eight factorial is eight times seven factorial'), show(f_s1, 'eight times seven times six factorial')),
      L("For example, ten factorial over eight factorial. Ten factorial is ten times nine times eight factorial. Eight "
        "factorial cancels, on top and below. We get ten times nine, ninety.", show(f_s2, 'ten factorial over eight factorial')),
      L("The same works with letters. n plus one, factorial, is n plus one, times n factorial.", show(f_s3, 'The same works with letters')),
      L("Let's see it in numbers. Four factorial is four times three factorial. Twenty-four is four times six.",
        show(f_s4, 'Four factorial is four times three factorial')),
      L("So a factorial over the factorial just before it is the bigger number. Twelve factorial over eleven factorial is "
        "twelve.", show(f_s5, 'Twelve factorial over eleven factorial')),
      L("And n factorial over n minus one, factorial, is n.", show(f_s6, 'n factorial over n minus one'))),
    S('A run of neighbours',
      L("Now the third tool. A big factorial over a smaller one. For example, seven factorial over four factorial."),
      L("Seven factorial is seven times six times five times four factorial. Four factorial cancels, on top and below.", show(f_r0, 'Seven factorial is seven times six')),
      L("What's left is seven times six times five. Seven times six is forty-two. Then forty-two times five is two hundred "
        "ten.", show(f_r1, 'seven times six times five')),
      L("So b factorial over a factorial is always a run of neighbours. That means whole numbers in a row, from a plus one "
        "up to b.", show(f_r2, 'a run of neighbours'))),
    S('Backwards',
      L("Now backwards, a type the exam likes. b factorial over a factorial is thirty, and b is bigger than a. What are a "
        "and b?", show(f_r3, 'b factorial over a factorial is thirty')),
      L("We need neighbours that multiply to thirty. Five times six is thirty.", show(f_r4, 'Five times six is thirty')),
      L("The run ends at b, so b is six.", show(f_r5, 'The run ends at b')),
      L("The run starts right after a, at five. So a is four, not five. Careful, that's the common slip.", show(f_r6, 'The run starts right after a')),
      L("Let's check. Six factorial over four factorial is six times five, thirty.", show(f_r7, 'Six factorial over four factorial')),
      L("One more. b factorial over a factorial is ninety. Nine times ten is ninety. So b is ten, and a is eight.",
        show(f_r8, 'b factorial over a factorial is ninety'), show(f_r9, 'Nine times ten is ninety')),
      L("The exam usually limits the numbers, for example to below ten. That way only one run of neighbours fits.")),
    S('Letters: plug in first',
      L("Sometimes a factorial question has only letters. What is n plus one, factorial, over n minus one, factorial?",
        show(f_p0, 'What is n plus one, factorial')),
      L("The psychometric way first. We plug in a number. Let's take n is three, a small number that is easy to calculate.",
        ),
      L("Then we get four factorial over two factorial. Twenty-four over two is twelve. Now we look for the choice that "
        "also gives twelve when n is three.", show(f_p1, 'four factorial over two factorial')),
      L("For example, n times n plus one. Three times four is twelve, so it matches.", show(f_p2, 'Three times four is twelve')),
      L("Now the math, so we really understand it. n plus one, factorial, is n plus one, times n, times n minus one, "
        "factorial. We stop there.", show(f_p3, 'Now the math')),
      L("n minus one, factorial, cancels on top and below. What's left is n times n plus one. The same answer.", show(f_p4, 'cancels on top and below'))),
    S('A product of factorials',
      L("Now a new example. What is n factorial times n plus two, factorial?", show(f_q0, 'What is n factorial times')),
      L("Plug in first. n is two. Two factorial times four factorial is two times twenty-four, forty-eight.", show(f_q1, 'n is two')),
      L("Now the math. We expand n plus two, factorial, until we reach n factorial. That's n plus two, times n plus one, "
        "times n factorial.", show(f_q2, 'We expand n plus two')),
      L("Now n factorial appears twice. And n factorial times n factorial is n factorial squared. So we get n factorial "
        "squared, times n plus one, times n plus two.", show(f_q3, 'n factorial squared')),
      L("Check with n is two. Two squared is four, times three, times four. That's forty-eight again.", show(f_q4, 'Check with n is two')),
      L("And a trap. A product of factorials is not one big factorial. Two factorial times four factorial is forty-eight, "
        "but six factorial is seven hundred twenty.", show(f_q5, 'A product of factorials is not'))),
    S('Sums and differences',
      L("The next tool is for a plus or a minus between factorials. We take out the smaller factorial."),
      L("Now a new example. Six factorial plus five factorial.", show(f_t0, 'Six factorial plus five factorial')),
      L("The smaller one is five factorial. And six factorial is six times five factorial.", show(f_t1, 'six factorial is six times')),
      L("So we have six times five factorial, plus one times five factorial. That's five factorial, times six plus one.",
        show(f_t2, 'So we have six times five factorial')),
      L("Don't forget the one. Six plus one is seven. Then seven times a hundred twenty is eight hundred forty.",
        show(f_t3, 'seven times a hundred twenty')),
      L("Let's check. Seven hundred twenty plus a hundred twenty is eight hundred forty.", show(f_t4, 'Seven hundred twenty plus'))),
    S('Differences',
      L("Now with a minus. Seven factorial minus six factorial. The smaller one is six factorial, and seven factorial is "
        "seven times six factorial.", show(f_t5, 'Seven factorial minus six factorial')),
      L("So it's six factorial times seven minus one. That's six times seven hundred twenty.", show(f_t6, 'six factorial times seven minus one')),
      L("Six times seven hundred is four thousand two hundred. And six times twenty is a hundred twenty. Together four "
        "thousand three hundred twenty.", show(f_t7, 'Six times seven hundred')),
      L("Check. Five thousand forty minus seven hundred twenty is four thousand three hundred twenty.", show(f_t8, 'Five thousand forty minus')),
      L("Careful, we never subtract inside the exclamation mark. Seven factorial minus six factorial is not one factorial.",
        show(f_t9, 'is not one factorial'))),
    S('Primes in a factorial',
      L("Now a question about dividing a factorial. For that, we break every factor into primes, like in the primes topic."),
      L("Six factorial is six times five times four times three times two times one.", show(f_u0, 'Six factorial is six times')),
      L("Six is two times three, and four is two times two.", show(f_u1, 'Six is two times three')),
      L("Let's count the twos. One in the six, two in the four, and one in the two. That's four twos.", show(f_u2, "Let's count the twos")),
      L("The threes are in the six and in the three, so two threes. And one five.", show(f_u3, 'The threes')),
      L("So six factorial is two to the power of four, times three squared, times five.", show(f_u4, 'two to the power of four')),
      L("Let's check. Sixteen times nine is a hundred forty-four. Times five, it's seven hundred twenty.", show(f_u5, 'Sixteen times nine'))),
    S('Is it divisible?',
      L("Is six factorial divisible by thirty-two? Thirty-two is two to the power of five. But we have only four twos, so "
        "no.", show(f_u6, 'Is six factorial divisible by thirty-two')),
      L("Is it divisible by forty-five? Forty-five is three squared times five. We have both, so yes.", show(f_u7, 'Is it divisible by forty-five')),
      L("Careful here. A lot of students count the even numbers. There are three even numbers, six, four and two. But "
        "there are four twos, because four hides two of them.", show(f_u8, 'There are three even numbers')),
      L("Seven factorial is the same, times one more prime, seven.", show(f_u9, 'Seven factorial is the same'))),
    S('Factorial times a power of two',
      L("And a last fact, rare on the exam. Three factorial times two to the power of three is six times eight, "
        "forty-eight.", show(f_w0, 'Three factorial times two')),
      L("And two times four times six is also forty-eight.", show(f_w1, 'two times four times six')),
      L("Why? Give each factor of three factorial its own two. One times two, two times two, and three times two. That's "
        "two, four and six.", show(f_w2, 'One times two, two times two')),
      L("So k factorial times two to the power of k is the product of the even numbers from two up to two k.",
        show(f_w3, 'the product of the even numbers'))),
    S('Recap',
      L("So let's sum it up. Know a hundred twenty, seven hundred twenty and five thousand forty by sight.", show(f_z1, 'by sight')),
      L("Expand a factorial only as far as you need.", show(f_z2, 'Expand a factorial only')),
      L("A big factorial over a smaller one is a run of neighbours.", show(f_z3, 'a run of neighbours')),
      L("For a sum or a difference, take out the smaller factorial, and don't forget the one.", show(f_z4, 'take out the smaller')),
      L("And for dividing, count the primes. Take a moment to memorize this, and I'll see you in the next video.",
        show(f_z5, 'count the primes'))),
]
video('wp-140-after', 'lesson', slides=_wp140)
SPLITS.append(('wp-140-after', 'Factorials', [
    (1, None),
    (6, "Let's continue with factorials, now with letters."),
    (10, "Let's continue, with primes in a factorial.")]))

# ------------------------------------------------------------------------------------------------ q-r26-t28-28 ((10! - 9!) / 8!)
# Not in the Hebrew (her course has no sums of factorials; exam 2020_winter_q1_19, 2024_winter_q2_17). Taught in
# wp-140-after part 2 (take out the smaller factorial); here "like in the lesson". Method 2: everything in eight
# factorials. Traps: 90 (forgets the minus 9!), 1/8! (subtracting inside the exclamation mark).
q28a = I('q28a', '$10!=10\\times9!$', size=36)
q28b = IH('q28b', '$10!-9!=9!\\times(10-1)=9\\times9!$', size=32)
q28c = I('q28c', '$\\dfrac{9\\times9!}{8!}=9\\times\\dfrac{9!}{8!}=9\\times9=81$', size=38)
q28d = IH('q28d', '$\\frac{10!}{8!}=90$: $\\ $the minus is forgotten', size=30, col=1)
q28e = IH('q28e', '$10!=10\\times9\\times8!=90\\times8!$', size=32)
q28f = IH('q28f', '$9!=9\\times8!$', size=32)
q28g = IH('q28g', '$90-9=81$', size=34)
video('solve-q-r26-t28-28', 'solution', qid='q-r26-t28-28', slides=[
    S('Method 1 · The math way: take out the smaller one',
      L("Ten factorial minus nine factorial, all divided by eight factorial, is equal to what?",
        pt('stem', 'Ten factorial minus nine factorial', 'hl', 5.0), voice='calm', pause=0.5),
      L("So we have factorials with a minus sign. We don't calculate them, because they are huge numbers."),
      L("We'll solve it in two different ways. Let's start with the math way, like in the lesson. We take out the smaller "
        "factorial. In ten factorial minus nine factorial, the smaller one is nine factorial."),
      L("Ten factorial is ten times nine factorial.", show(q28a, 'Ten factorial is ten times')),
      L("So we have ten times nine factorial, minus one times nine factorial. That's nine factorial, times ten minus one. "
        "So it's nine times nine factorial.", show(q28b, 'So we have ten times nine factorial')),
      L("Now we divide by eight factorial. Nine factorial over eight factorial is just nine. So nine times nine is "
        "eighty-one.", show(q28c, 'Nine factorial over eight factorial')),
      L("Careful, ninety is choice number three, and it's a trap. Ten factorial over eight factorial is ninety, but that "
        "forgets the minus nine factorial.", show(q28d, 'Ten factorial over eight factorial'), mk('cross', 'choice 3', "it's a trap")),
      L("And choice number four, one over eight factorial, comes from subtracting inside the exclamation mark. Ten minus "
        "nine is one, but ten factorial minus nine factorial is not one factorial.", mk('cross', 'choice 4', 'choice number four'))),
    S('Method 2 · The math way: everything with eight factorial',
      L("[pause] Now another way. We write everything with eight factorial, because we divide by eight factorial."),
      L("Ten factorial is ten times nine times eight factorial. That's ninety times eight factorial.", show(q28e, 'Ten factorial is ten times nine')),
      L("Nine factorial is nine times eight factorial.", show(q28f, 'Nine factorial is nine times')),
      L("So we have ninety times eight factorial, minus nine times eight factorial. That's eighty-one times eight factorial. "
        "Divided by eight factorial, it's eighty-one.", show(q28g, 'eighty-one times eight factorial')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g141 (hundreds + units = 8)
# Hebrew (wp 9303-9332, 9392-9410, "medium"; hundreds + units = 5): she starts with the tens digit, "because there is no
# restriction on it", 10 options; "above I write the number of options and below I list them, I recommend it to you";
# hundreds 1-5, not 0, "there is no such number as 076"; the units digit is forced: 1; 5 x 10 x 1 = 50; "these questions
# are not simple, and this understanding is important". English: sum 8 -> 8 x 10 x 1 = 80. The course teaches "the
# restricted stage first" (wp-124-after), so the hundreds come first; her free-tens remark is kept as one sentence (the
# Hebrew-vs-English report, restore #1). Method 2: the listing check; the trap 90 counts 0-8 (a leading zero).
g41S = SLOTS28('g41S', ['hundreds', 'tens', 'units'], [
    ('h', [('n', 0, '8'), ('sub', 0, '1 to 8')]), ('u', [('n', 2, '1', 'teal'), ('sub', 2, 'forced')]),
    ('t', [('n', 1, '10'), ('sub', 1, '0 to 9')]), ('x', [('x',)]), ('eq', [('eq', '80')])], sub=1, w=760, title='Three positions')
g41a = IH('g41a', '$9$: $\\ 9+0=9$, $\\ $too much', size=30, col=1)
g41b = IH('g41b', '$058$? $\\ $No such number', size=30, col=1)
g41c = IH('g41c', 'hundreds $3$: $\\ $units $8-3=5$', size=30, col=1)
g41d = IH('g41d', 'hundreds $8$: $\\ $units $0$', size=30, col=1)
g41e = IH('g41e', '$8\\times10=80$', size=32, col=1)
g41L = LIST28('g41L', 2, 4, [('a', [('r', 0, ['1_7', '2_6', '3_5', '4_4']), ('r', 1, ['5_3', '6_2', '7_1', '8_0'])]),
                             ('f', [('foot', '8 pairs')])], cellw=80, cellh=48, right=20, gapc=12, w=420, size=30, title='The pairs')
g41f = IH('g41f', '$0\\_8$: $\\ $a two-digit number', size=30)
g41g = IH('g41g', '$8\\times10=80$, $\\ $not $9\\times10=90$', size=30)
video('solve-wp28-g141', 'solution', qid='wp28-g141', slides=[
    S('Method 1 · The math way: stages of choice',
      L("How many three-digit numbers have a hundreds digit and a units digit whose sum is eight?",
        pt('stem', 'How many three-digit numbers', 'hl', 5.0), voice='calm', pause=0.5),
      L("So the hundreds digit and the units digit must add up to eight. The tens digit isn't mentioned at all. These "
        "questions are not simple, so let's go slowly.", pt('stem', 'add up to eight')),
      L("We'll solve it in two different ways. Let's start with the math way, in stages. Three-digit numbers, so three "
        "positions, hundreds, tens and units.", show(g41S['line'], 'three positions')),
      L("Here's a tip that keeps us organized. Above each position, we write how many options it has. Below it, we list "
        "what they are."),
      L("Like in the lesson, we start with a position that has a restriction, the hundreds digit. Can it be nine? Nine plus "
        "even zero is already nine, more than eight. So no.", show(g41a, 'Can it be nine')),
      L("Can it be zero? No. A number can't start with zero. There's no such number as zero five eight.", show(g41b, 'Can it be zero')),
      L("So the hundreds digit is one to eight. That's eight options.", show(g41S['h'], "That's eight options")),
      L("Now the units digit. Once the hundreds digit is chosen, the units digit is already decided. It must complete the "
        "sum to eight."),
      L("If the hundreds digit is three, the units digit must be five. If it's eight, the units digit must be zero. One "
        "option every time.", show(g41c, 'If the hundreds digit is three'), show(g41d, "If it's eight"), show(g41S['u'], 'One option every time')),
      L("So choosing the hundreds digit really chooses two digits at once."),
      L("And the tens digit? The condition doesn't mention it, so it's free. Zero to nine, ten options. A free position can "
        "be filled at any point, even first.", show(g41S['t'], 'ten options')),
      L("Eight times ten times one is eighty.", show(g41S['x'], 'Eight times ten times one'), show(g41e, 'Eight times ten times one'),
        show(g41S['eq'], 'is eighty'))),
    S('Method 2 · The math way: listing',
      L("[pause] Now a quick check, by listing the hundreds and units pairs. The tens digit sits in the middle of each pair."),
      L("One and seven, two and six, three and five, four and four.", show(g41L['line'], 'One and seven'), show(g41L['a'], 'One and seven')),
      L("Five and three, six and two, seven and one, and eight and zero. That's eight pairs.", show(g41L['f'], "That's eight pairs")),
      L("What about zero and eight? That would start with zero, so it's only a two-digit number. If you count it, you get "
        "nine pairs, and nine times ten is ninety. That's choice number one, the trap.", show(g41f, 'What about zero and eight'),
        mk('cross', 'choice 1', "That's choice number one")),
      L("Any of the ten digits can go in the middle of each pair. Eight times ten is eighty again.", show(g41g, 'Eight times ten is eighty again')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-141-after (lesson: forced digits)
# Hebrew (wp 9333-9391, inside Q141): all digits identical (111, 222...): 9 x 1 x 1 = 9, NOT 9 x 9 x 9; units = hundreds:
# 9 x 10 x 1 = 90 (101, 111, 121...), "choosing the hundreds digit really chooses two digits". English: four-digit
# numbers (new numbers), three examples: all identical (9, not 9 to the power of 4); first = last (900; 1001 counts);
# the pairs 3377 (90). The old lesson's line "the forced position gets one" is kept.
d_a0 = I('d_a0', 'Four-digit numbers, $\\ $all digits the same', size=34)
d_a1 = SLOTS28('d_a1', ['1st', '2nd', '3rd', '4th'], [('a', [('n', 0, '9'), ('sub', 0, '1 to 9')]),
                                                    ('b', [('n', 1, '1', 'teal'), ('n', 2, '1', 'teal'), ('n', 3, '1', 'teal'), ('sub', 1, 'forced'), ('sub', 2, 'forced'), ('sub', 3, 'forced')]),
                                                    ('x', [('x',)]), ('eq', [('eq', '9')])], boxw=120, gap=50, sub=1, w=820, title='All the same')
d_a2 = IH('d_a2', '$1111,\\ 2222,\\ ...,\\ 9999$', size=32)
d_a3 = IH('d_a3', '$9^4$? $\\ $No: $\\ $only $9$ numbers', size=32)
d_b0 = I('d_b0', 'Four-digit numbers, $\\ $first digit $=$ last digit', size=34)
d_b1 = SLOTS28('d_b1', ['1st', '2nd', '3rd', '4th'], [('a', [('n', 0, '9'), ('sub', 0, '1 to 9')]),
                                                    ('b', [('n', 1, '10'), ('n', 2, '10'), ('sub', 1, '0 to 9'), ('sub', 2, '0 to 9')]),
                                                    ('c', [('n', 3, '1', 'teal'), ('sub', 3, 'copy')]),
                                                    ('x', [('x',)]), ('eq', [('eq', '900')])], boxw=120, gap=50, sub=1, w=820, title='First = last')
d_b2 = IH('d_b2', '$9\\times10\\times10\\times1=900$', size=32, col=1)
d_b3 = IH('d_b3', '$1001$: $\\ $allowed', size=32, col=1)
d_c0 = I('d_c0', 'Like $3377$: $\\ $2nd $=$ 1st, $\\ $4th $=$ 3rd', size=34)
d_c1 = SLOTS28('d_c1', ['1st', '2nd', '3rd', '4th'], [('a', [('n', 0, '9'), ('sub', 0, '1 to 9')]),
                                                    ('b', [('n', 1, '1', 'teal'), ('sub', 1, 'copy')]),
                                                    ('c', [('n', 2, '10'), ('sub', 2, '0 to 9')]),
                                                    ('d', [('n', 3, '1', 'teal'), ('sub', 3, 'copy')]),
                                                    ('x', [('x',)]), ('eq', [('eq', '90')])], boxw=120, gap=50, sub=1, w=820, title='Pairs')
d_c2 = IH('d_c2', '$1100,\\ 1111,\\ ...,\\ 9999$', size=32, col=1)
d_z1 = I('d_z1', 'A forced position gets $1$.', size=34)
d_z2 = I('d_z2', 'Count each free choice once.', size=34)
video('wp-141-after', 'lesson', slides=[
    S('Forced Digits',
      L("In the last question, choosing the hundreds digit also decided the units digit. That idea deserves a closer look."),
      L("When one choice forces another, the forced position gets exactly one option. Let's see it in three examples.")),
    S('All digits the same',
      L("How many four-digit numbers have all their digits the same?", show(d_a0, 'How many four-digit numbers')),
      L("The first digit can't be zero, so it's one to nine. Nine options.", show(d_a1['line'], 'The first digit'),
        show(d_a1['a'], 'Nine options')),
      L("And the second digit? You might think nine options too. It could be one, in one one one one. Or two, in two two "
        "two two."),
      L("But that's not really true. Once the first digit is chosen, the others must be the same digit. If we pick five, "
        "the number is five five five five. So each of the other positions gets one option.",
        show(d_a1['b'], 'So each of the other positions')),
      L("Nine times one times one times one is nine.", show(d_a1['x'], 'Nine times one'), show(d_a1['eq'], 'times one is nine')),
      L("Here they are, one one one one, two two two two, up to nine nine nine nine. Just nine numbers.", show(d_a2, 'Here they are')),
      L("Careful, not nine to the power of four. That would let every digit be anything.", show(d_a3, 'not nine to the power of four'))),
    S('First digit equals last',
      L("Now a new example. How many four-digit numbers have the same first digit and last digit?", show(d_b0, 'the same first digit')),
      L("The first digit, one to nine. Nine options.", show(d_b1['line'], 'The first digit, one to nine'), show(d_b1['a'], 'Nine options')),
      L("The second and third digits have no restriction. Each one has ten options, zero included.", show(d_b1['b'], 'Each one has ten options')),
      L("And the last digit must copy the first. One option. So choosing the first digit really chooses two digits.",
        show(d_b1['c'], 'One option')),
      L("Nine times ten times ten times one is nine hundred.", show(d_b1['x'], 'Nine times ten'), show(d_b2, 'Nine times ten'),
        show(d_b1['eq'], 'is nine hundred')),
      L("And one zero zero one counts too, so don't drop the zero from the middle.", show(d_b3, 'one zero zero one counts'))),
    S('Two pairs',
      L("One more example. Four-digit numbers like three three seven seven, where the second digit copies the first, and the "
        "fourth copies the third.", show(d_c0, 'like three three seven seven')),
      L("The first digit, one to nine, nine options. The second copies it, one option.", show(d_c1['line'], 'The first digit'),
        show(d_c1['a'], 'nine options'), show(d_c1['b'], 'one option')),
      L("The third digit is free, zero to nine, ten options. The fourth copies it, one option.", show(d_c1['c'], 'ten options'),
        show(d_c1['d'], 'The fourth copies it')),
      L("Nine times one times ten times one is ninety. From one one zero zero, up to nine nine nine nine.",
        show(d_c1['x'], 'Nine times one times ten'), show(d_c1['eq'], 'is ninety'), show(d_c2, 'From one one zero zero'))),
    S('Recap',
      L("So let's sum it up. A forced position gets one option.", show(d_z1, 'A forced position gets one')),
      L("Count each free choice once, and the copies get one. Take a moment to memorize this, and I'll see you in the next "
        "video.", show(d_z2, 'Count each free choice once'))),
])

# ------------------------------------------------------------------------------------------------ g143 (66 matches)
# Hebrew (wp 9528-9706, 28 basketball games): (1) mutual action n(n - 1)/2 = 28 -> n(n - 1) = 56 = two consecutive
# numbers, 8 x 7 -> 8; (2) plugging in the answers (10 -> 45, out; 8 -> 28), and the aside: start from the middle
# (5 -> 10, too few, so 4 is out too); (3) the rising series: a table, each new team adds one game per team already
# there, 1 + 2 + ... + 7 = 28, "8 teams, not 7", "write it across the page", "whatever you prefer". English: 66 matches
# -> 12 players. W26: plugging in the answers starts from the middle of the ordered choices (11, a stated reason) and
# FAILS (55, too few, so 9 is out too), then 12. Table: TBL (the games table of the method visuals library).
g43a = I('g43a', '$\\dfrac{n\\times(n-1)}{2}=66$', size=40)
g43b = IH('g43b', '$n\\times(n-1)=132$', size=34)
g43c = IH('g43c', '$12\\times11=132$', size=34)
g43d = IH('g43d', '$n=12$', size=36)
g43e = IH('g43e', 'in order: $\\ 9,\\ 11,\\ 12,\\ 13$', size=32)
g43f = IH('g43f', '$11$: $\\ {11\\times10/2}=55$, $\\ $too few', size=32)
g43g = IH('g43g', '$9$: $\\ $even fewer, $\\ $out', size=32)
g43h = IH('g43h', '$12$: $\\ {12\\times11/2}=66$', size=32)
g43T = TBL('g43T', ['players', 'added', 'total'], [''] * 6, [
    ('r1', [('c', 0, 0, '1'), ('c', 0, 1, '0'), ('c', 0, 2, '0')]), ('r2', [('c', 1, 0, '2'), ('c', 1, 1, '1'), ('c', 1, 2, '1')]),
    ('r3', [('c', 2, 0, '3'), ('c', 2, 1, '2'), ('c', 2, 2, '3')]), ('r4', [('c', 3, 0, '4'), ('c', 3, 1, '3'), ('c', 3, 2, '6')]),
    ('r5', [('c', 4, 0, '…'), ('c', 4, 1, '…'), ('c', 4, 2, '…')]), ('r6', [('c', 5, 0, '12'), ('c', 5, 1, '11'), ('c', 5, 2, '66')])],
    colw=190, labw=0, rowh=54, headh=54, w=600, size=32, title='The games table')
g43i = IH('g43i', '$1+2+3+...+11=66$', size=32, col=1)
g43j = IH('g43j', 'the last $11$: $\\ $added by player $12$', size=30, col=1)
video('solve-wp28-g143', 'solution', qid='wp28-g143', slides=[
    S('Method 1 · The math way: mutual action',
      L("In a table-tennis league, each pair of players plays exactly one match. There are sixty-six matches altogether. "
        "How many players take part?", pt('stem', 'In a table-tennis league', 'hl', 8.0), voice='calm', pause=0.5),
      L("So this time they give the number of matches, and they ask for the players. We go backwards.", pt('stem: ask', 'they ask for the players')),
      L("We'll solve it in three different ways. Let's start with the math way. Each pair plays once. Does that remind "
        "you of something? It's a mutual action, like in the lesson."),
      L("When the red player plays the black player, the black player plays the red one at the same time. So with n "
        "players, it's n times n minus one, divided by two. And that's sixty-six.", show(g43a, "And that's sixty-six")),
      L("We multiply both sides by two. n times n minus one is a hundred thirty-two.", show(g43b, 'n times n minus one is')),
      L("n and n minus one are neighbours, numbers in a row. Which two neighbours multiply to a hundred thirty-two? Twelve "
        "times eleven is a hundred thirty-two.", show(g43c, 'Twelve times eleven')),
      L("So n is twelve. Twelve players.", show(g43d, 'So n is twelve'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers, still with the mutual action rule. Let's put the choices in order. Nine, "
        "eleven, twelve and thirteen.", show(g43e, 'Let\'s put the choices in order')),
      L("Why start from the middle? Because if the middle choice fails, we learn in which direction to go, and we can rule "
        "out more than one choice. Let's try eleven."),
      L("Eleven players. Eleven times ten is a hundred ten. Divided by two, it's fifty-five matches. That's too few, we need "
        "sixty-six.", show(g43f, 'Eleven players'), mk('cross', 'choice 1', "That's too few")),
      L("Fewer players means fewer matches. So nine players gives even fewer, and nine is out too. We need more players.",
        show(g43g, 'So nine players gives even fewer'), mk('cross', 'choice 4', 'nine is out too')),
      L("Let's try twelve. Twelve times eleven is a hundred thirty-two. Divided by two, it's sixty-six. That's exactly it.",
        show(g43h, "Let's try twelve"))),
    S('Method 3 · The math way: the games table',
      L("[pause] And a third way, less known, but it really shows what mutual action means. We build a table, and we add "
        "one player at a time.", show(g43T['line'], 'We build a table')),
      L("One player alone plays no matches. With a second player, there's one match.", show(g43T['r1'], 'One player alone'),
        show(g43T['r2'], 'With a second player')),
      L("A third player joins and plays each of the two already there. So the third player adds two matches. One plus two "
        "is three.", show(g43T['r3'], 'A third player joins')),
      L("A fourth player adds three matches, one against each player already there. Three plus three is six.", show(g43T['r4'], 'A fourth player')),
      L("And so on. Every new player adds one match for every player who was already there.", show(g43T['r5'], 'And so on')),
      L("On the exam, we don't draw the whole table. We write it across the page. One plus two plus three, and so on. We "
        "keep adding until we reach sixty-six.", show(g43i, 'One plus two plus three')),
      L("One plus two and so on, up to eleven, is sixty-six.", show(g43T['r6'], 'up to eleven, is sixty-six')),
      L("Careful here. The last number we added is eleven. But it comes from the twelfth player, who played the eleven "
        "players before. So twelve players, not eleven.", show(g43j, 'The last number we added is eleven')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g144 (7 of 8 children by height)
# Hebrew (wp 9708-9790, 5 of 6 students by height, "medium plus, even hard"): (1) trial and error with heights 1-6,
# change only the right end, 6 rows; a sanity check against the choices (5 is fewer than found, 5! = 120 far too many);
# (2) the insight of the complementary event: choose who stays ("you stay, everyone else come"), 6; "the complementary
# event isn't magic, it's a technique worth knowing". English: 7 of 8 children -> 8 (both methods, her closing line).
_R44 = ['1234567', '1234568', '1234578', '1234678', '1235678', '1245678', '1345678', '2345678']
g44L = LIST28('g44L', 8, 7, [('a', [('r', 0, _R44[0])]), ('b', [('r', 1, _R44[1])]), ('c', [('r', 2, _R44[2])]),
                             ('d', [('r', k, _R44[k]) for k in range(3, 8)]), ('f', [('foot', '8 rows')])],
              cellw=40, cellh=40, right=20, gapc=4, w=330, size=28, col=1, title='Rows of seven, by height')
g44a = IH('g44a', 'heights $1$ to $8$: $\\ 1$ the shortest', size=30)
g44b = IH('g44b', '$7$? $\\ $We already found $8$', size=30)
g44c = IH('g44c', '$5040=7!$: $\\ $far too many', size=30)
g44d = IH('g44d', '$8$ children: $\\ 8$ ways to choose who stays out', size=30)
g44e = IH('g44e', 'the other $7$: $\\ $only $1$ order', size=30)
g44f = IH('g44f', '$8\\times1=8$', size=34)
video('solve-wp28-g144', 'solution', qid='wp28-g144', slides=[
    S('Method 1 · Plugging in numbers: trial and error',
      L("Eight children all have different heights. A photographer chooses seven of them and places them in a row from "
        "shortest to tallest. How many different rows can be formed?", pt('stem', 'Eight children all have different heights', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("So we choose seven of eight, and their order is forced, from shortest to tallest. This one is medium plus, maybe "
        "even hard.", pt('stem', 'from shortest to tallest')),
      L("We'll solve it in two different ways. Let's start by plugging in numbers, with trial and error. We give the "
        "heights the numbers one to eight. One is the shortest, and eight is the tallest.", show(g44a, 'We give the heights the numbers')),
      L("Now we build rows of seven, always from shortest to tallest. The first row is one to seven.", show(g44L['line'], 'The first row'),
        show(g44L['a'], 'The first row is one to seven')),
      L("To stay organized, we change only the right end. We swap the seven for an eight.", show(g44L['b'], 'We swap the seven for an eight')),
      L("Next, we leave out the six instead. One to five, then seven and eight.", show(g44L['c'], 'we leave out the six')),
      L("And we keep moving the missing child one place to the left, until we leave out the one.", show(g44L['d'], 'keep moving the missing child')),
      L("No more options. That's eight rows.", show(g44L['f'], "That's eight rows")),
      L("Let's check against the choices. Seven is too few, because we already found eight different rows.",
        show(g44b, 'Seven is too few'), mk('cross', 'choice 1', 'Seven is too few')),
      L("Five thousand forty is seven factorial. That would let the seven stand in any order, but here the order is "
        "forced. Far too many, and fifty-six is too many as well, because we found every row.", show(g44c, 'Five thousand forty is seven factorial'),
        mk('cross', 'choice 2', 'Far too many'), mk('cross', 'choice 4', 'fifty-six is too many'))),
    S('Method 2 · Insight: who stays out',
      L("[pause] Now the insight. Imagine you are the photographer. Instead of choosing seven children, you choose the one "
        "child who stays out."),
      L("You say to one child, you stay. Everyone else, come here. And they line up from shortest to tallest, in only one "
        "way.", show(g44e, 'in only one way')),
      L("Any of the eight children can be the one who stays out. So that's eight options.", show(g44d, 'Any of the eight children')),
      L("Eight times one is eight.", show(g44f, 'Eight times one is eight')),
      L("This is the complementary event. It isn't magic. It's a technique worth knowing, and it helps in many questions."),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g142 (digits in a square)
# Hebrew (wp 9412-9526, "hard"; 1-4 in a square, B even, C x D not odd): (1) the calculation: B even, 2 options; a
# product is odd only if both are odd; "the easier conclusion: A must be odd", 2 options, then 2 and 1 -> 8; the nuance:
# a square, not a row, doesn't matter, multiply per stage; (2) trial and error, organised: anchor 2 and 1, change as
# little as possible; 4 options with 2 in the corner, by symmetry 4 more with 4 -> 8. English: 2, 5, 6, 9; A even,
# C x D even -> "the easier conclusion: B must be odd"; both of her methods, plus Method 3 all minus forbidden (12 - 4).
g42Q = LIST28('g42Q', 2, 2, [('lab', [('c', 0, 0, 'A'), ('c', 0, 1, 'B'), ('c', 1, 0, 'C'), ('c', 1, 1, 'D')])],
              cellw=90, cellh=70, grid=True, right=10, gapc=0, w=200, size=36, col=1, title='The square')
g42S = SLOTS28('g42S', ['A', 'B', 'C', 'D'], [('a', [('n', 0, '2'), ('sub', 0, '2, 6')]), ('b', [('n', 1, '2'), ('sub', 1, '5, 9')]),
                                            ('c', [('n', 2, '2'), ('n', 3, '1')]), ('x', [('x',)]), ('eq', [('eq', '8')])],
               boxw=100, gap=46, sub=1, w=640, title='Four stages')
g42a = IH('g42a', 'odd $\\times$ odd $=$ odd', size=30, col=1)
g42b = IH('g42b', 'C or D must be even', size=30, col=1)
g42c = IH('g42c', 'so B is odd', size=32, col=1)
g42d = IH('g42d', '$2\\times2\\times2\\times1=8$', size=32)
g42L = LIST28('g42L', 4, 4, [('a', [('r', 0, '2569')]), ('b', [('r', 1, '2596')]), ('c', [('r', 2, '2956'), ('r', 3, '2965')]),
                             ('f', [('foot', '4 with A = 2')])], head=['A', 'B', 'C', 'D'], cellw=56, cellh=46, right=20, gapc=8,
              w=330, size=30, col=1, title='A is 2')
g42e = IH('g42e', 'A $=6$: $\\ $the same $4$ again', size=30)
g42f = IH('g42f', '$4+4=8$', size=32)
g42g = IH('g42g', 'A even: $\\ 2\\times3!=2\\times6=12$', size=30)
g42h = IH('g42h', 'bad: $\\ $the other even in B: $\\ 2\\times1\\times2=4$', size=30)
g42i = IH('g42i', '$12-4=8$', size=32)
video('solve-wp28-g142', 'solution', qid='wp28-g142', slides=[
    S('Method 1 · The math way: stages of choice',
      L("The digits two, five, six and nine go once each into a square. A and B are on top, C and D below. A is even. C "
        "times D is even. How many arrangements are possible?", pt('stem', 'The digits two, five, six and nine', 'hl', 10.0),
        voice='calm', pause=0.5),
      L("So each digit is used once, with two conditions. A is even, and the bottom product is even. This is a hard one.",
        pt('stem: given', 'with two conditions'), show(g42Q['line'], 'each digit is used once'), show(g42Q['lab'], 'each digit is used once')),
      L("We'll solve it in three different ways. Let's start with the math way, in stages. A is even. How many even "
        "digits do we have? Two, the two and the six. So A has two options.", show(g42S['line'], 'in stages'),
        show(g42S['a'], 'So A has two options')),
      L("Now the bottom product. When is a product odd? Only when both numbers are odd.", show(g42a, 'Only when both numbers are odd')),
      L("So for an even product, C or D must be even.", show(g42b, 'C or D must be even')),
      L("Some students get stuck here. Which bottom square gets the even digit? But there's an easier conclusion."),
      L("One even digit is already in A. The other even digit must go to the bottom. So it can't be in B. So B must be "
        "odd.", show(g42c, 'So B must be odd')),
      L("B is odd, five or nine. Two options.", show(g42S['b'], 'Two options')),
      L("Two digits are left, and no more restrictions. C has two options, and D gets the last one.", show(g42S['c'], 'C has two options')),
      L("Two times two times two times one is eight.", show(g42S['x'], 'Two times two times two'), show(g42d, 'Two times two times two'),
        show(g42S['eq'], 'times one is eight')),
      L("And this time it's a square, not a row. But that doesn't matter. We count the options at each stage, and "
        "multiply.")),
    S('Method 2 · Plugging in numbers: trial and error',
      L("[pause] Now let's plug in numbers, with trial and error. Say you're not sure what to do. Let's try, and list, in an "
        "organized way."),
      L("We fix A as two. Then B must be odd, otherwise the bottom gets two odd digits.", show(g42L['line'], 'We fix A as two')),
      L("B is five. Then six and nine go below, six then nine, or nine then six.", show(g42L['a'], 'B is five'),
        show(g42L['b'], 'or nine then six')),
      L("B is nine. Then five and six go below, in two orders. That's four arrangements with A as two.", show(g42L['c'], 'B is nine'),
        show(g42L['f'], "That's four arrangements")),
      L("Now A is six. It's exactly the same pattern, so there are four more. We don't need to draw them.", show(g42e, 'Now A is six')),
      L("Four plus four is eight.", show(g42f, 'Four plus four is eight'))),
    S('Method 3 · The math way: all minus forbidden',
      L("[pause] And a third way, all minus forbidden. First, only the rule for A. A has two options, and the other three "
        "digits can go in any order, three factorial, six. Two times six is twelve.", show(g42g, 'Two times six is twelve')),
      L("Careful, twelve is choice number one. It forgets the bottom rule.", mk('cross', 'choice 1', 'It forgets the bottom rule')),
      L("When does the bottom rule fail? When the other even digit sits in B, because then both bottom digits are odd. A "
        "has two options, B is forced, and the two odd digits go below in two orders. Two times one times two is four.",
        show(g42h, 'Two times one times two is four')),
      L("Twelve minus four is eight. The same answer.", show(g42i, 'Twelve minus four')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ r26-t28-cases (lesson: at least one, boxes, the worst case)
# Not in the Hebrew (added English lesson; the Hebrew-vs-English report section 2). The old two-slide stub becomes a real
# R37 lesson (exam-coverage audit, gap 3; C2 "at least once", objects into boxes; C8 the worst-case keys, real exam
# 2025_autumn_q1_03, 3 + 2 + 1 = 6, here with new numbers: 4 keys, 4 + 3 + 2 + 1 = 10; "worst luck" is topic 21, a short
# reminder). Small cases LISTED before each rule: two coins (HH HT TH TT: 4 - 1 = 3); codes from 1-5 with at least one 5
# (25 - 16 = 9, listed; the direct count 5 + 5 counts 55 twice); two letters into two boxes (the 4 ways listed = 2 x 2);
# 3 children choose from 4 flavours (4 x 4 x 4 = 64, not 3 to the power of 4).
a_a0 = I('a_a0', 'Two coins. $\\ $At least one head?', size=34)
a_aL = LIST28('a_aL', 4, 2, [('a', [('r', 0, ['H', 'H']), ('r', 1, ['H', 'T']), ('r', 2, ['T', 'H']), ('r', 3, ['T', 'T'])]),
                             ('n', [('note', 3, 'no head', 'red')]), ('k', [('note', 0, 'yes'), ('note', 1, 'yes'), ('note', 2, 'yes')])],
              head=['coin 1', 'coin 2'], cellw=90, cellh=46, right=170, gapc=10, w=400, col=1, title='Two coins')
a_a1 = IH('a_a1', 'all: $\\ 2\\times2=4$', size=32)
a_a2 = IH('a_a2', 'none: $\\ $TT, $\\ 1$', size=32)
a_a3 = IH('a_a3', '$4-1=3$', size=34)
a_a4 = I('a_a4', 'At least one $=$ all $-$ none', size=38)
a_b0 = I('a_b0', 'Two-digit codes from $1$ to $5$. $\\ $At least one $5$?', size=34)
a_b1 = IH('a_b1', 'all: $\\ 5\\times5=25$', size=32)
a_b2 = IH('a_b2', 'no $5$: $\\ 4\\times4=16$', size=32)
a_b3 = IH('a_b3', '$25-16=9$', size=34)
a_bL = LIST28('a_bL', 1, 9, [('a', [('r', 0, ['15', '25', '35', '45', '51', '52', '53', '54', '55'])])], cellw=52, cellh=46, right=10,
              gapc=8, w=560, size=28, title='The list')
a_b4 = IH('a_b4', '$5$ first: $\\ 5$, $\\ 5$ second: $\\ 5$, $\\ 5+5=10$?', size=30)
a_b5 = IH('a_b5', '$55$ is counted twice', size=30)
a_c0 = I('a_c0', 'Letters A and B into box $1$ or box $2$', size=34)
a_cL = LIST28('a_cL', 4, 2, [('a', [('r', 0, ['1', '1'])]), ('b', [('r', 1, ['1', '2'])]), ('c', [('r', 2, ['2', '1'])]),
                             ('d', [('r', 3, ['2', '2'])])], head=['A goes to', 'B goes to'], cellw=130, cellh=46, right=20,
              gapc=10, w=330, col=1, title='Two letters, two boxes')
a_c1 = SLOTS28('a_c1', ['letter A', 'letter B'], [('a', [('n', 0, '2')]), ('b', [('n', 1, '2')]), ('x', [('x',)]), ('eq', [('eq', '4')])],
               boxw=160, w=500, title='Each letter chooses')
a_c2 = I('a_c2', 'Each object chooses a box.', size=36)
a_d0 = I('a_d0', '$3$ children, $\\ 4$ flavours. $\\ $Each child chooses one.', size=34)
a_d1 = SLOTS28('a_d1', ['child 1', 'child 2', 'child 3'], [('a', [('n', 0, '4'), ('n', 1, '4'), ('n', 2, '4')]), ('x', [('x',)]),
                                                         ('eq', [('eq', '64')])], boxw=140, w=760, title='Each child chooses')
a_d2 = IH('a_d2', '$4\\times4\\times4=64$', size=32)
a_d3 = IH('a_d3', '$3\\times3\\times3\\times3=81$: $\\ $the flavours don\'t choose', size=30)
a_e0 = I('a_e0', '$4$ keys, $\\ 4$ lockers. $\\ $At most how many tries?', size=34)
a_eL = LIST28('a_eL', 4, 1, [('a', [('c', 0, 0, 'locker 1:  3 wrong, then right: 4 tries')]), ('b', [('c', 1, 0, 'locker 2:  3 tries')]),
                             ('c', [('c', 2, 0, 'locker 3:  2 tries')]), ('d', [('c', 3, 0, 'locker 4:  1 try')]),
                             ('f', [('foot', '4 + 3 + 2 + 1 = 10')])], cellw=560, cellh=48, right=20, w=560, size=30, col=1,
              title='The worst luck')
a_e1 = IH('a_e1', '$3$ wrong keys, $\\ $then the right one', size=30)
a_z1 = I('a_z1', 'At least one: $\\ $all minus none', size=34)
a_z2 = I('a_z2', 'Into boxes: $\\ $each object chooses', size=34)
a_z3 = I('a_z3', 'At most how many tries: $\\ $the worst luck', size=34)
_cases = [
    S('At Least One, Boxes and the Worst Case',
      L("In this lesson, three more kinds of counting question. At least one, objects that go into boxes, and the most tries "
        "we might need."),
      L("Each one has its own trick, so let's see them one at a time.")),
    S('At least one',
      L("Let's start with a tiny case. We toss two coins. In how many outcomes do we get at least one head?", show(a_a0, 'We toss two coins')),
      L("Here are all the outcomes. Head head, head tail, tail head, and tail tail. Two times two is four.",
        show(a_aL['line'], 'Here are all the outcomes'), show(a_aL['a'], 'Head head'), show(a_a1, 'Two times two is four')),
      L("At least one head means one head or two heads. Only tail tail has no head at all.", show(a_aL['n'], 'Only tail tail'),
        show(a_a2, 'Only tail tail')),
      L("So the outcomes we want are all of them, minus the one with no head. Four minus one is three.", show(a_aL['k'], 'Four minus one'),
        show(a_a3, 'Four minus one is three')),
      L("So at least one is all, minus none. Why? Because the opposite of at least one is none, and none is easy to count.",
        show(a_a4, 'So at least one is all, minus none'))),
    S('At least one five',
      L("Now a new example. Two-digit codes from the digits one to five, and digits may repeat. How many codes have at "
        "least one five?", show(a_b0, 'How many codes have at least one five')),
      L("All the codes first. Five times five is twenty-five.", show(a_b1, 'Five times five is twenty-five')),
      L("Now the codes with no five at all. Each digit has only four options, one to four. Four times four is sixteen.",
        show(a_b2, 'Four times four is sixteen')),
      L("All minus none. Twenty-five minus sixteen is nine.", show(a_b3, 'Twenty-five minus sixteen')),
      L("Let's check with a list. Fifteen, twenty-five, thirty-five, forty-five, and fifty-one up to fifty-five. Nine codes.",
        show(a_bL['line'], "Let's check with a list"), show(a_bL['a'], 'Fifteen, twenty-five')),
      L("Why not count directly? Many students say a five first gives five codes, and a five second gives five more. Five "
        "plus five is ten.", show(a_b4, 'Five plus five is ten')),
      L("But fifty-five was counted twice, once in each group. That's why all minus none is safer.", show(a_b5, 'fifty-five was counted twice'))),
    S('Objects into boxes',
      L("Now a new kind of question. Two letters, A and B, go into two boxes. A box may get both letters, or none. In how "
        "many ways can we do it?", show(a_c0, 'Two letters, A and B')),
      L("Let's list them. Both letters in box one. A in box one and B in box two. A in box two and B in box one. And both "
        "in box two. Four ways.", show(a_cL['line'], "Let's list them"), show(a_cL['a'], 'Both letters in box one'),
        show(a_cL['b'], 'A in box one and B in box two'), show(a_cL['c'], 'A in box two and B in box one'),
        show(a_cL['d'], 'both in box two')),
      L("In stages, who chooses? Each letter chooses a box. Letter A has two options, and letter B has two options. Two "
        "times two is four.", show(a_c1['line'], 'Each letter chooses a box'), show(a_c1['a'], 'Letter A has two options'),
        show(a_c1['b'], 'letter B has two options'), show(a_c1['x'], 'Two times two'), show(a_c1['eq'], 'Two times two is four')),
      L("So every object is a stage, and each stage has as many options as there are boxes.", show(a_c2, 'every object is a stage'))),
    S('Who chooses?',
      L("Now a new example. Three children each choose one of four ice cream flavours. Two children may choose the same "
        "flavour. In how many ways can they choose?", show(a_d0, 'Three children each choose')),
      L("Who chooses? Each child chooses a flavour. So each child is a stage, with four options.", show(a_d1['line'], 'Each child chooses'),
        show(a_d1['a'], 'with four options')),
      L("Four times four times four is sixty-four.", show(a_d1['x'], 'Four times four'), show(a_d2, 'Four times four times four'),
        show(a_d1['eq'], 'is sixty-four')),
      L("The trap is to turn it around. Three times three times three times three is eighty-one. That lets every flavour "
        "choose a child, and that's not the story.", show(a_d3, 'Three times three times three')),
      L("If you're not sure which number is the base, try a tiny case you can list, like the two letters and two boxes.")),
    S('The worst case',
      L("And the last kind. A question that asks at most how many tries. Remember worst luck from topic twenty-one? We use "
        "it here."),
      L("Noa has four keys for four lockers. She doesn't know which key opens which locker. She never tries a key that "
        "she already knows doesn't fit. At most how many tries does she need to open all four? A try that opens a locker "
        "counts too.", show(a_e0, 'Noa has four keys')),
      L("The first locker. With the worst luck, the right key is the last one she tries. Three wrong keys, and then the "
        "right one. That's four tries.", show(a_eL['line'], 'The first locker'), show(a_eL['a'], "That's four tries")),
      L("That key is used now, so three keys are left for the second locker. With the worst luck, three tries.",
        show(a_eL['b'], 'three tries')),
      L("Then two tries for the third locker, and one try for the last one.", show(a_eL['c'], 'Then two tries'),
        show(a_eL['d'], 'one try for the last one')),
      L("Four plus three plus two plus one is ten tries.", show(a_eL['f'], 'Four plus three plus two plus one'))),
    S('Recap',
      L("So let's sum it up. At least one is all, minus none.", show(a_z1, 'At least one is all')),
      L("When objects go into boxes, ask who chooses. Each object chooses a box.", show(a_z2, 'ask who chooses')),
      L("And for at most how many tries, imagine the worst luck at every step. Take a moment to memorize this, and I'll "
        "see you in the next video.", show(a_z3, 'imagine the worst luck'))),
]
video('r26-t28-cases', 'lesson', slides=_cases)
TITLES28['r26-t28-cases'] = 'At Least One, Boxes and the Worst Case'

# ------------------------------------------------------------------------------------------------ q-r26-t28-04 (at least one 5)
# Not in the Hebrew. "At least once" = all minus none (r26-t28-cases): 10^4 - 9^4 = 3439 (R36: 9^2 = 81, 81 x 81 =
# 6480 + 81 = 6561). Traps at their steps: 4000 (a five in each place: overlaps), 6561 (the codes with no five), 2916
# (exactly one five: 4 x 9^3).
q4a = IH('q4a', 'all: $\\ 10\\times10\\times10\\times10=10000$', size=30)
q4b = IH('q4b', 'no $5$: $\\ 9\\times9\\times9\\times9=9^4$', size=30)
q4c = IH('q4c', '$9^2=81$', size=30, col=1)
q4d = IH('q4d', '$81\\times80=6480$', size=30, col=1)
q4e = IH('q4e', '$6480+81=6561$', size=30, col=1)
q4f = IH('q4f', '$10000-6561=3439$', size=32)
q4g = IH('q4g', '$5$ in each place: $\\ 4\\times1000=4000$?', size=30)
q4h = IH('q4h', '$5500$: $\\ $counted twice', size=30)
q4i = IH('q4i', '$4\\times9^3=2916$: $\\ $exactly one $5$', size=30, col=1)
video('solve-q-r26-t28-04', 'solution', qid='q-r26-t28-04', slides=[
    S('Method 1 · The math way: all minus none',
      L("A code has four digits. Each digit is from zero to nine, digits may repeat, and the code may start with zero. How "
        "many codes contain the digit five at least once?", pt('stem', 'A code has four digits', 'hl', 9.0), voice='calm', pause=0.5),
      L("So they ask for at least once. Like in the lesson, that's our signal for all minus none.", pt('stem: ask', 'at least once')),
      L("Let's solve it the math way. Why all minus none? The opposite of at least one five is no five at all, and no five "
        "is one easy count."),
      L("All the codes first. Each of the four digits has ten options. Ten times ten times ten times ten is ten thousand.",
        show(q4a, 'Ten times ten times ten times ten')),
      L("Now the codes with no five. Each digit has nine options, every digit except five. That's nine times nine times "
        "nine times nine, nine to the power of four.", show(q4b, 'nine to the power of four')),
      L("Nine squared is eighty-one. And nine to the power of four is eighty-one times eighty-one.", show(q4c, 'Nine squared is eighty-one')),
      L("Eighty-one times eighty is six thousand four hundred eighty. And one more eighty-one is six thousand five hundred "
        "sixty-one.", show(q4d, 'Eighty-one times eighty'), show(q4e, 'And one more eighty-one')),
      L("Careful, six thousand five hundred sixty-one is choice number three. It's the codes with no five, not our answer "
        "yet.", mk('cross', 'choice 3', 'not our answer yet')),
      L("All minus none. Ten thousand minus six thousand five hundred sixty-one is three thousand four hundred thirty-nine.",
        show(q4f, 'Ten thousand minus'))),
    S('Method 1 · The math way: all minus none',
      L("Why not count directly? Put a five in the first place, then ten, ten, ten. That's a thousand codes. Four places, "
        "four thousand. That's choice number one.", show(q4g, 'Four places, four thousand'), mk('cross', 'choice 1', "That's choice number one")),
      L("But the code five five zero zero was counted twice, once for the first place and once for the second.",
        show(q4h, 'was counted twice')),
      L("And two thousand nine hundred sixteen is four times nine to the power of three. That counts exactly one five. But "
        "at least once also includes two, three and four fives.", show(q4i, 'exactly one five'), mk('cross', 'choice 4', 'includes two, three')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t28-05 (letters into mailboxes)
# Not in the Hebrew. Each object chooses a box (r26-t28-cases): 3^5 = 243 (3, 9, 27, 81, 243). The trap 125 = 5^3 (each
# mailbox choosing one letter). Method 2 plugging in numbers: a tiny case (2 letters, 2 boxes = 4 = 2^2) decides the base.
q5S = SLOTS28('q5S', ['1', '2', '3', '4', '5'], [('a', [('n', i, '3') for i in range(5)]), ('x', [('x',)])], boxw=90, gap=40,
              eqw=14, w=700, title='Each letter chooses a mailbox', lab_size=26)
q5a = IH('q5a', '$3,\\ 9,\\ 27,\\ 81,\\ 243$', size=32)
q5b = IH('q5b', '$3^5=243$', size=34)
q5c = IH('q5c', '$5^3=125$: $\\ $each mailbox gets one letter', size=30, col=1)
q5d = IH('q5d', '$2$ letters, $\\ 2$ boxes: $\\ 4$ ways', size=30)
q5f = IH('q5f', '$3^5=243$', size=34)
q5e = IH('q5e', '$4=2^2$: $\\ $boxes to the power of letters', size=30)
video('solve-q-r26-t28-05', 'solution', qid='q-r26-t28-05', slides=[
    S('Method 1 · The math way: each object chooses',
      L("Five different letters are put into three mailboxes. A mailbox may get any number of letters, or none. In how "
        "many different ways can the letters be put into the mailboxes?", pt('stem', 'Five different letters', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("So every letter goes into some mailbox. And one mailbox may get several letters.", pt('stem: given', 'one mailbox may get several')),
      L("We'll solve it in two different ways. Let's start with the math way. Like in the lesson, we ask who chooses. Each "
        "letter must go somewhere, so each letter chooses a mailbox.", show(q5S['line'], 'each letter chooses a mailbox')),
      L("Letter one has three options. Letter two also has three, because a mailbox can take more than one letter. And so "
        "on, five letters with three options each.", show(q5S['a'], 'five letters with three options each')),
      L("Three times three times three times three times three. Three, nine, twenty-seven, eighty-one, two hundred forty-three.",
        show(q5S['x'], 'Three times three'), show(q5a, 'Three, nine, twenty-seven')),
      L("That's three to the power of five.", show(q5b, "That's three to the power of five")),
      L("The trap is five to the power of three, a hundred twenty-five, choice number one. That lets each mailbox choose "
        "one letter. But a mailbox can get two letters, or none.", show(q5c, 'five to the power of three'),
        mk('cross', 'choice 1', 'choice number one'))),
    S('Method 2 · Plugging in numbers: a tiny case',
      L("[pause] Not sure which number is the base? Let's plug in small numbers, two letters and two boxes, and list."),
      L("Both letters in box one, or both in box two. Or one in each box, in two ways. Four ways.", show(q5d, 'Four ways')),
      L("Four is two squared. That's the number of boxes, to the power of the number of letters.", show(q5e, 'Four is two squared')),
      L("So here it's three to the power of five again.", show(q5f, 'three to the power of five again')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ r26-t28-arrange (lesson: together, apart, repeats, round)
# Not in the Hebrew (added English lesson; Hebrew-vs-English report section 2). The old stub ("four questions, one for
# each") becomes a real R37 lesson in two parts. Every rule is SHOWN on a tiny case first (the teacher's rule "show
# change step by step"; external findings tracker row 28: "show the AAAB rows, list all arrangements, see the repeats,
# before BANANA"): A, B, C with A and B together (the 6 rows listed, 4 marked) -> glue 2! x 2; apart = 6 - 4; then 5
# friends together (48), 4 friends apart (24 - 12, and the gaps 2 x 3 x 2); repeats: A, A, A, B listed (4), the As named
# A1, A2, A3 (6 rows of one word) -> 24 / 3! = 4; AABB (6, listed); a round table of 3 (ABC, BCA, CAB are one seating)
# -> (3 - 1)! = 2, then 5 people (24). Real exam: 2024_spring_q1_05 (repeated digits), 2024_autumn_q1_07.
_ABC = ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']
g_a0 = I('g_a0', 'A, B, C in a row. $\\ $A and B together.', size=34)
g_aL = LIST28('g_aL', 6, 3, [('a', [('r', i, _ABC[i]) for i in range(6)]),
                             ('y', [('note', 0, 'together'), ('note', 2, 'together'), ('note', 4, 'together'), ('note', 5, 'together'),
                                    ('glue', 0, 0, 1), ('glue', 2, 0, 1), ('glue', 4, 1, 2), ('glue', 5, 1, 2)]),
                             ('n', [('note', 1, 'apart', 'red'), ('note', 3, 'apart', 'red')])],
              cellw=50, cellh=44, right=170, gapc=6, w=380, col=1, title='Every order of A, B, C')
g_aM = LIST28('g_aM', 6, 3, [('a', [('r', i, _ABC[i]) for i in range(6)]),
                             ('n', [('note', 1, 'apart', 'red'), ('note', 3, 'apart', 'red')])],
              cellw=50, cellh=44, right=170, gapc=6, w=380, col=1, title='Every order of A, B, C')
g_a1 = LIST28('g_a1', 1, 2, [('g', [('c', 0, 0, 'AB'), ('c', 0, 1, 'C'), ('glue', 0, 0, 0)])], cellw=80, cellh=56, right=10, w=200,
              size=34, title='A and B glued')
g_a2 = IH('g_a2', '$2$ items: $\\ 2!=2$', size=32)
g_a3 = IH('g_a3', 'inside: $\\ $AB or BA, $\\ 2$', size=32)
g_a4 = IH('g_a4', '$2\\times2=4$', size=34)
g_b0 = I('g_b0', '$5$ friends in a row. $\\ $Dan and Mia together.', size=34)
g_b1 = IH('g_b1', 'the block $+\\ 3$ friends: $\\ 4$ items, $\\ 4!=24$', size=32)
g_b2 = IH('g_b2', 'inside: $\\ 2$', size=32)
g_b3 = IH('g_b3', '$24\\times2=48$', size=34)
g_c1 = IH('g_c1', 'apart: $\\ 6-4=2$', size=32)
g_c0 = I('g_c0', '$4$ friends in a row. $\\ $Dan and Mia apart.', size=34)
g_c2 = IH('g_c2', 'all: $\\ 4!=24$', size=32)
g_c3 = IH('g_c3', 'together: $\\ 3!\\times2=6\\times2=12$', size=32)
g_c4 = IH('g_c4', '$24-12=12$', size=34)
g_d1 = LIST28('g_d1', 1, 5, [('a', [('c', 0, 1, 'Ann'), ('c', 0, 3, 'Ben')]), ('g', [('c', 0, 0, 'gap', 'teal'), ('c', 0, 2, 'gap', 'teal'), ('c', 0, 4, 'gap', 'teal')])],
              cellw=80, cellh=56, right=10, gapc=6, w=440, size=34, title='The gaps')
g_d2 = IH('g_d2', 'Ann and Ben: $\\ 2!=2$ orders', size=32)
g_d3 = IH('g_d3', 'Dan: $\\ 3$ gaps, $\\ $Mia: $\\ 2$ gaps', size=32)
g_d4 = IH('g_d4', '$2\\times3\\times2=12$', size=34)
g_e0 = I('g_e0', 'A, A, A, B: $\\ $how many arrangements?', size=34)
g_eL = LIST28('g_eL', 4, 4, [('a', [('r', 0, 'AAAB'), ('r', 1, 'AABA'), ('r', 2, 'ABAA'), ('r', 3, 'BAAA')]), ('f', [('foot', '4 arrangements')])],
              cellw=56, cellh=50, right=20, gapc=6, w=330, title='The arrangements of A, A, A, B')
g_e1 = IH('g_e1', 'A, B, C, D: $\\ 4!=24$', size=32)
_A6 = [['A₁', 'A₂', 'A₃', 'B'], ['A₁', 'A₃', 'A₂', 'B'], ['A₂', 'A₁', 'A₃', 'B'], ['A₂', 'A₃', 'A₁', 'B'], ['A₃', 'A₁', 'A₂', 'B'], ['A₃', 'A₂', 'A₁', 'B']]
g_eN = LIST28('g_eN', 6, 4, [('a', [('r', i, _A6[i]) for i in range(6)]), ('g', [('ring', 0, 5, 'all AAAB')])],
              cellw=62, cellh=50, right=150, gapc=6, w=520, col=1, title='The As with names')
g_e2 = IH('g_e2', '$3!=6$ orders of the As', size=32)
g_e3 = IH('g_e3', '$24\\div6=4$', size=34)
g_f0 = I('g_f0', 'A, A, B, B', size=36)
g_f1 = IH('g_f1', '${4!/2!\\times2!}={24/4}=6$', size=34)
g_fL = LIST28('g_fL', 2, 3, [('a', [('c', 0, 0, 'AABB'), ('c', 0, 1, 'ABAB'), ('c', 0, 2, 'ABBA'), ('c', 1, 0, 'BAAB'), ('c', 1, 1, 'BABA'), ('c', 1, 2, 'BBAA')])],
              cellw=110, cellh=46, right=10, gapc=10, w=380, size=32, col=1, title='The list')
g_f2 = I('g_f2', 'Repeats: $\\ $divide by the factorial of each repeat.', size=34)
g_gD = DOTS28('g_gD', ['A', 'B', 'C'], [('r', [('ring', 0)])], table=True, R=110, pad=56, w=320, col=1, title='A round table')
g_gL = LIST28('g_gL', 2, 3, [('a', [('c', 0, 0, 'ABC'), ('c', 0, 1, 'BCA'), ('c', 0, 2, 'CAB')]), ('b', [('c', 1, 0, 'ACB'), ('c', 1, 1, 'CBA'), ('c', 1, 2, 'BAC')]),
                             ('n', [('note', 0, 'one seating'), ('note', 1, 'another')])],
              cellw=80, cellh=48, right=180, gapc=10, w=500, size=32, title='Turning the table')
g_g1 = IH('g_g1', '$3!=6$ rows, $\\ $but $2$ seatings', size=32)
g_g2 = IH('g_g2', 'fix A: $\\ (3-1)!=2!=2$', size=32)
g_g3 = I('g_g3', '$n$ around a table: $\\ (n-1)!$', size=36)
g_g4 = IH('g_g4', '$5$ people: $\\ 4!=24$', size=32)
g_z1 = I('g_z1', 'Together: $\\ $glue, $\\ $then times the order inside', size=32)
g_z2 = I('g_z2', 'Apart: $\\ $all minus together, $\\ $or the gaps', size=32)
g_z3 = I('g_z3', 'Repeats: $\\ $divide by each repeat\'s factorial', size=32)
g_z4 = I('g_z4', 'A round table: $\\ (n-1)!$', size=32)
_arr = [
    S('Together, Apart and Repeats',
      L("Now rows with a rule. Some people must stand together, some must stand apart. Some items repeat. And sometimes "
        "the row is a round table."),
      L("Each rule changes how we count, and each one has its own trick. We'll see each trick on a tiny case first.")),
    S('Together: glue them',
      L("Let's start with a tiny case. A, B and C stand in a row. A and B must stand together. How many orders?",
        show(g_a0, 'A, B and C stand in a row')),
      L("Here are all six orders of A, B and C.", show(g_aL['line'], 'all six orders'), show(g_aL['a'], 'all six orders')),
      L("A and B are next to each other in A B C, B A C, C A B and C B A. That's four orders.", show(g_aL['y'], "That's four orders")),
      L("Now the trick. We glue A and B into one block. Then we have two items, the block and C.", show(g_a1['line'], 'We glue A and B'),
        show(g_a1['g'], 'the block and C')),
      L("Two items in a row, two factorial, two orders.", show(g_a2, 'two factorial, two orders')),
      L("And inside the block, A and B can stand in two orders, A B or B A.", show(g_a3, 'inside the block')),
      L("Two times two is four. The same four orders.", show(g_a4, 'Two times two is four'))),
    S('Together: an example',
      L("Now a new example. Five friends stand in a row. Dan and Mia must stand together.", show(g_b0, 'Five friends stand in a row')),
      L("We glue Dan and Mia into a block. The block and the three other friends are four items. Four factorial is "
        "twenty-four.", show(g_b1, 'Four factorial is twenty-four')),
      L("Inside the block, Dan and Mia can stand in two orders.", show(g_b2, 'in two orders')),
      L("Twenty-four times two is forty-eight. Don't forget the order inside the block.", show(g_b3, 'Twenty-four times two'))),
    S('Apart',
      L("Now the opposite rule, apart. Back to A, B and C. Now A and B may not stand together."),
      L("Apart is everything except together. All six orders, minus the four together. Six minus four is two.", show(g_aM['line'], 'All six orders'),
        show(g_aM['a'], 'All six orders'), show(g_aM['n'], 'Six minus four is two'), show(g_c1, 'Six minus four is two')),
      L("Now a new example. Four friends in a row, and Dan and Mia must stand apart.", show(g_c0, 'Four friends in a row')),
      L("All the orders, four factorial, twenty-four.", show(g_c2, 'four factorial, twenty-four')),
      L("Together, we glue them. Three items, three factorial, six. Times two inside the block, twelve.", show(g_c3, 'Together, we glue them')),
      L("All minus together. Twenty-four minus twelve is twelve.", show(g_c4, 'Twenty-four minus twelve'))),
    S('Apart: the gaps',
      L("There's a second way for apart, the gaps. We place the other two friends first, Ann and Ben. They can stand in two "
        "orders.", show(g_d1['line'], 'We place the other two friends first'), show(g_d1['a'], 'Ann and Ben'), show(g_d2, 'two orders')),
      L("Ann and Ben make three gaps. One before them, one between them, and one after them.", show(g_d1['g'], 'make three gaps')),
      L("Dan goes into one of the three gaps. Mia goes into one of the two other gaps. That way they're never next to each "
        "other.", show(g_d3, 'Dan goes into one of the three gaps')),
      L("Two times three times two is twelve. The same twelve.", show(g_d4, 'Two times three times two'))),
    S('Repeats',
      L("Now items that repeat. Four different letters, A, B, C and D, can stand in four factorial orders, twenty-four.",
        show(g_e1, 'four factorial orders, twenty-four')),
      L("But what about A, A, A and B? Let's list them.", show(g_e0, 'what about A, A, A and B'), show(g_eL['line'], "Let's list them")),
      L("The B can be last, third, second or first. A A A B, A A B A, A B A A, and B A A A. Only four.", show(g_eL['a'], 'The B can be last'),
        show(g_eL['f'], 'Only four')),
      L("Why so few? Let's give the As names for a moment, A one, A two and A three. Now they are four different letters, "
        "with twenty-four orders."),
      L("But look at these six orders. A one, A two, A three, B. Then A one, A three, A two, B, and so on.", show(g_eN['line'], 'look at these six orders'),
        show(g_eN['a'], 'look at these six orders')),
      L("When we take the names off, all six are the same word, A A A B. Swapping the As changes nothing.", show(g_eN['g'], 'all six are the same word')),
      L("Six is three factorial, the orders of the three As.", show(g_e2, 'Six is three factorial')),
      L("So every word was counted six times. Twenty-four divided by six is four.", show(g_e3, 'Twenty-four divided by six'))),
    S('Two repeats',
      L("Now a new example. A, A, B and B.", show(g_f0, 'A, A, B and B')),
      L("Four letters, twenty-four orders, as if all were different. The two As repeat, so we divide by two factorial. The "
        "two Bs repeat, so we divide by two factorial again. Twenty-four divided by four is six.", show(g_f1, 'Twenty-four divided by four')),
      L("Let's list them to check. A A B B, A B A B, A B B A, B A A B, B A B A and B B A A. Six.", show(g_fL['line'], "Let's list them"),
        show(g_fL['a'], 'A A B B')),
      L("So for repeated items, count as if all were different, then divide by the factorial of each repeat.", show(g_f2, 'divide by the factorial'))),
    S('A round table',
      L("And the last rule, a round table. Three people, A, B and C, sit around a round table.", show(g_gD['line'], 'Three people, A, B and C')),
      L("In a row, A B C and B C A are different. But at a round table, B C A is the same seating, just turned. Everyone has "
        "the same neighbours.", show(g_gL['line'], 'at a round table'), show(g_gL['a'], 'B C A is the same seating')),
      L("So A B C, B C A and C A B are one seating. And A C B, C B A and B A C are another.", show(g_gL['b'], 'are another'),
        show(g_gL['n'], 'are another')),
      L("Three factorial is six rows, but only two seatings.", show(g_g1, 'Three factorial is six rows')),
      L("The trick is to fix one person. A sits in a seat. Then the others fill the remaining seats in two factorial ways, "
        "two.", show(g_gD['r'], 'A sits in a seat'), show(g_g2, 'two factorial ways')),
      L("So n people around a table can sit in n minus one, factorial, ways.", show(g_g3, 'n people around a table')),
      L("For example, five people around a table. Four factorial, twenty-four.", show(g_g4, 'Four factorial, twenty-four'))),
    S('Recap',
      L("So let's sum it up. Together, glue them into a block, and then multiply by the order inside.", show(g_z1, 'glue them into a block')),
      L("Apart, take all minus together, or use the gaps.", show(g_z2, 'all minus together')),
      L("Repeats, divide by the factorial of each repeat.", show(g_z3, 'divide by the factorial')),
      L("And a round table is n minus one, factorial. Take a moment to memorize this, and I'll see you in the next video.",
        show(g_z4, 'n minus one, factorial'))),
]
video('r26-t28-arrange', 'lesson', slides=_arr)
SPLITS.append(('r26-t28-arrange', 'Together, Apart and Repeats', [
    (1, None),
    (5, "Let's continue, with items that repeat.")]))

# ------------------------------------------------------------------------------------------------ q-r26-t28-06 (3 math books together)
# Not in the Hebrew. Together = glue (r26-t28-arrange): 4! x 3! = 144. Method 2 where the block stands (4 places x 3! x
# 3!). Traps: 24 (forgets the order inside), 720 (ignores the rule).
q6a = IH('q6a', 'the block $+\\ 3$ books: $\\ 4$ items', size=32)
q6b = IH('q6b', '$4!=24$', size=32)
q6c = IH('q6c', 'inside: $\\ 3!=6$', size=32)
q6d = IH('q6d', '$24\\times6=144$', size=34)
q6L = LIST28('q6L', 4, 6, [('a', [('c', r, k, 'M') for r in range(4) for k in range(r, r + 3)] +
                           [('glue', 0, 0, 2), ('glue', 1, 1, 3), ('glue', 2, 2, 4), ('glue', 3, 3, 5)])],
             head=['1', '2', '3', '4', '5', '6'], grid=True, cellw=46, cellh=46, right=10, gapc=4, w=340, size=28, col=1,
             title='Where the block of math books can stand')
q6e = IH('q6e', '$4$ places for the block', size=30)
q6f = IH('q6f', '$4\\times6\\times6=144$', size=34)
video('solve-q-r26-t28-06', 'solution', qid='q-r26-t28-06', slides=[
    S('Method 1 · The math way: glue them',
      L("Six different books are placed on a shelf in a row. The three math books among them must stand together, in any "
        "order. How many arrangements are possible?", pt('stem', 'Six different books', 'hl', 8.0), voice='calm', pause=0.5),
      L("So the three math books stand next to each other, and inside their group any order is fine.", pt('stem: given', 'stand next to each other')),
      L("We'll solve it in two different ways. Let's start with the math way. Together means glue, like in the lesson. We "
        "tie the three math books into one block."),
      L("The block and the three other books are four items.", show(q6a, 'are four items')),
      L("Four items in a row, four factorial, twenty-four.", show(q6b, 'four factorial, twenty-four')),
      L("Inside the block, the three math books can stand in three factorial orders, six.", show(q6c, 'three factorial orders, six')),
      L("Twenty-four times six is a hundred forty-four.", show(q6d, 'Twenty-four times six')),
      L("Careful, twenty-four is choice number one, and it's a trap. It forgets the order inside the block.",
        mk('cross', 'choice 1', "it's a trap"))),
    S('Method 2 · The math way: where the block stands',
      L("[pause] Now another way. Let's ask where the block of three can stand on a shelf of six places. It can start at "
        "place one, two, three or four.", show(q6L['line'], 'where the block of three can stand'), show(q6L['a'], 'It can start at place one'),
        show(q6e, 'place one, two, three or four')),
      L("For each place, the math books have three factorial orders inside, six. And the three other books fill the three "
        "other places in three factorial orders, six."),
      L("Four times six times six. Four times six is twenty-four. Then twenty-four times six is a hundred forty-four again.",
        show(q6f, 'Four times six times six')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t28-07 (two girls apart)
# Not in the Hebrew. Apart: the gaps (3! x 4 x 3 = 72) and all minus together (120 - 48 = 72), both from
# r26-t28-arrange. Trap: 48 = the "together" count.
q7L = LIST28('q7L', 1, 7, [('b', [('c', 0, 1, 'boy'), ('c', 0, 3, 'boy'), ('c', 0, 5, 'boy')]),
                           ('g', [('c', 0, 0, 'gap', 'teal'), ('c', 0, 2, 'gap', 'teal'), ('c', 0, 4, 'gap', 'teal'), ('c', 0, 6, 'gap', 'teal')])],
             cellw=62, cellh=56, right=10, gapc=6, w=500, size=32, title='Four gaps')
q7a = IH('q7a', 'boys: $\\ 3!=6$', size=32)
q7b = IH('q7b', 'girls: $\\ 4\\times3=12$', size=32)
q7c = IH('q7c', '$6\\times12=72$', size=34)
q7d = IH('q7d', 'all: $\\ 5!=120$', size=32)
q7e = IH('q7e', 'together: $\\ 4!\\times2=48$', size=32)
q7f = IH('q7f', '$120-48=72$', size=34)
video('solve-q-r26-t28-07', 'solution', qid='q-r26-t28-07', slides=[
    S('Method 1 · The math way: the gaps',
      L("Three boys and two girls stand in a row. All five are different people. The two girls may not stand next to each "
        "other. How many orders are possible?", pt('stem', 'Three boys and two girls', 'hl', 8.0), voice='calm', pause=0.5),
      L("So this is the apart rule from the lesson. The girls must have at least one boy between them.", pt('stem: given', 'the apart rule')),
      L("We'll solve it in two different ways. Let's start with the math way, the gaps. We place the boys first. Three "
        "boys in a row, three factorial, six orders.", show(q7L['line'], 'We place the boys first'), show(q7L['b'], 'Three boys in a row'),
        show(q7a, 'three factorial, six orders')),
      L("The three boys make four gaps. Before the first boy, between the boys twice, and after the last boy.", show(q7L['g'], 'make four gaps')),
      L("The first girl picks one of the four gaps. The second girl picks one of the three other gaps. So the girls are "
        "never side by side. Four times three is twelve.", show(q7b, 'Four times three is twelve')),
      L("Six times twelve is seventy-two.", show(q7c, 'Six times twelve'))),
    S('Method 2 · The math way: all minus together',
      L("[pause] Now all minus together. All the orders of five different people is five factorial, a hundred twenty.",
        show(q7d, 'five factorial, a hundred twenty')),
      L("Together, we glue the two girls. Four items, four factorial, twenty-four. Times two inside the block is forty-eight.",
        show(q7e, 'Times two inside the block')),
      L("Careful, forty-eight is choice number one, and it's the trap. That's the together count, not apart.",
        mk('cross', 'choice 1', "it's the trap")),
      L("A hundred twenty minus forty-eight is seventy-two.", show(q7f, 'A hundred twenty minus forty-eight')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t28-08 (BANANA)
# Not in the Hebrew. Repeats (r26-t28-arrange, after the AAAB rows): 6! / (3! x 2!) = 60. Method 2: choose the places
# (the As: 6 x 5 x 4 / 3! = 20, the Ns: 3 of the 3 left, 3 ways, B last) = 60. Traps: 120 (forgets the Ns), 360
# (forgets the As), 720.
q8a = IH('q8a', 'all different: $\\ 6!=720$', size=32)
q8b = IH('q8b', 'A three times: $\\ \\div3!=\\div6$', size=32)
q8c = IH('q8c', 'N twice: $\\ \\div2!=\\div2$', size=32)
q8d = IH('q8d', '${720/6\\times2}={720/12}=60$', size=34, col=1)
q8e = IH('q8e', '$720\\div6=120$: $\\ $the Ns forgotten', size=30, col=1)
q8f = IH('q8f', '$720\\div2=360$: $\\ $the As forgotten', size=30, col=1)
q8g = IH('q8g', 'places for A: $\\ {6\\times5\\times4/3!}=20$', size=32)
q8h = IH('q8h', 'places for N: $\\ 3$', size=32)
q8i = IH('q8i', 'B: $\\ $the last place, $\\ 1$', size=32)
q8j = IH('q8j', '$20\\times3\\times1=60$', size=34)
video('solve-q-r26-t28-08', 'solution', qid='q-r26-t28-08', slides=[
    S('Method 1 · The math way: divide by the repeats',
      L("How many different arrangements of all the letters of the word banana are there? An arrangement does not have to "
        "be a real word.", pt('stem', 'How many different arrangements', 'hl', 6.0), voice='calm', pause=0.5),
      L("So we arrange six letters, B, A, N, A, N, A. Some letters repeat. A appears three times, and N twice.", pt('stem', 'we arrange six letters')),
      L("We'll solve it in two different ways. Let's start with the math way, like the A A A B example in the lesson. First "
        "we count as if all six letters were different. Six factorial is seven hundred twenty.", show(q8a, 'Six factorial is seven hundred twenty')),
      L("But A appears three times. Swapping the As gives nothing new, so we divide by three factorial, six.", show(q8b, 'we divide by three factorial')),
      L("And N appears twice. Swapping the Ns gives nothing new either, so we divide by two factorial, two.", show(q8c, 'divide by two factorial')),
      L("Six times two is twelve. Then seven hundred twenty divided by twelve is sixty.", show(q8d, 'seven hundred twenty divided by twelve')),
      L("The traps forget one of the repeats. Dividing only by six gives a hundred twenty, choice number two. Dividing only "
        "by two gives three hundred sixty, choice number four.", show(q8e, 'Dividing only by six'), show(q8f, 'Dividing only by two'),
        mk('cross', 'choice 2', 'choice number two'), mk('cross', 'choice 4', 'choice number four'))),
    S('Method 2 · The math way: choose the places',
      L("[pause] Now another way. We have six places, and we choose where each letter goes."),
      L("First the three As. We choose three places out of six. That's a group, so six times five times four, divided by "
        "three factorial. A hundred twenty divided by six is twenty.", show(q8g, 'We choose three places out of six')),
      L("Three places are left. The two Ns take two of them. Choosing two of three is the same as choosing the one that "
        "stays out, three ways.", show(q8h, 'three ways')),
      L("And B takes the last place. One way.", show(q8i, 'B takes the last place')),
      L("Twenty times three times one is sixty again.", show(q8j, 'Twenty times three times one')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t28-09 (round table, together)
# Not in the Hebrew. Two rules: together (glue) and a round table ((n - 1)!), both from r26-t28-arrange: (5 - 1)! x 2 =
# 48. Method 2: fix Dana (Eli: 2 seats, the others 4!). Traps: 240 (a row: 5! x 2), 24 (forgets the order inside),
# 120 (5!).
q9D = DOTS28('q9D', ['Dana', '', '', '', '', ''], [('r', [('ring', 0)]), ('e', [('lab', 1, 'Eli?', 'teal'), ('lab', 5, 'Eli?', 'teal')])],
             table=True, R=120, pad=70, w=400, col=1, title='Fix Dana')
q9a = IH('q9a', 'Dana and Eli: $\\ $one block', size=32)
q9b = IH('q9b', '$5$ items around the table', size=32)
q9c = IH('q9c', '$(5-1)!=4!=24$', size=32)
q9d = IH('q9d', 'inside: $\\ 2$', size=32, col=1)
q9e = IH('q9e', '$24\\times2=48$', size=34, col=1)
q9f = IH('q9f', 'a row: $\\ 5!\\times2=240$', size=30, col=1)
q9g = IH('q9g', 'Eli: $\\ 2$ seats', size=32)
q9h = IH('q9h', 'the other $4$: $\\ 4!=24$', size=32)
q9i = IH('q9i', '$2\\times24=48$', size=34)
video('solve-q-r26-t28-09', 'solution', qid='q-r26-t28-09', slides=[
    S('Method 1 · The math way: glue, then a round table',
      L("Six people sit around a round table. Two arrangements are the same if one is a rotation of the other. Dana and Eli "
        "must sit next to each other. How many arrangements are possible?", pt('stem', 'Six people sit around a round table', 'hl', 10.0),
        voice='calm', pause=0.5),
      L("So there are two rules at once. Dana and Eli together, and a round table. Let's do them one at a time.",
        pt('stem: given', 'Dana and Eli together')),
      L("We'll solve it in two different ways. Let's start with the math way. Together means glue. Dana and Eli become one "
        "block.", show(q9a, 'Dana and Eli become one block')),
      L("The block and the four other people are five items around the table.", show(q9b, 'are five items')),
      L("A round table, like in the lesson. Turning the table changes nobody's neighbours. So five items around a table is "
        "five minus one, factorial. Four factorial is twenty-four.", show(q9c, 'Four factorial is twenty-four')),
      L("Inside the block, Dana can sit on Eli's left or on his right. Two orders.", show(q9d, 'Two orders')),
      L("Twenty-four times two is forty-eight.", show(q9e, 'Twenty-four times two')),
      L("The traps. If we treat the table like a row, we get five factorial times two, two hundred forty. That's choice "
        "number one.", show(q9f, 'two hundred forty'), mk('cross', 'choice 1', "That's choice number one")),
      L("And twenty-four, choice number three, forgets the order inside the block.", mk('cross', 'choice 3', 'forgets the order inside'))),
    S('Method 2 · The math way: fix one person',
      L("[pause] Now a check, with the trick from the lesson. We fix Dana in her seat. Turning the table can't change "
        "anything now.", show(q9D['line'], 'We fix Dana'), show(q9D['r'], 'We fix Dana')),
      L("Eli must sit next to her. That's one of two seats, on her left or on her right.", show(q9D['e'], 'one of two seats'),
        show(q9g, 'one of two seats')),
      L("The other four people fill the four other seats in four factorial ways, twenty-four.", show(q9h, 'four factorial ways')),
      L("Two times twenty-four is forty-eight again.", show(q9i, 'Two times twenty-four')),
      L("Choice number four is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ bigger pictures in the lessons
# 2026-10-25 visual check (the teacher's request for topic 28: "show small cases on a BIG picture"): on a lesson slide,
# the figures (lists, trees, stage boxes, the pool, points) are scaled up together, as far as the slide's free height
# allows (the board is about 880 px tall from y 78; the written rows keep their size), at most x1.6 and at most 900 wide.
def _scale_lesson_figures(maxk=1.5, maxw=900, room=780):
    for vid, V in VIDEOS.items():
        if V['kind'] != 'lesson': continue
        for sl in V['slides']:
            its = [c[1] for ln in sl['lines'] for c in ln['cues'] if c[0] == 'show']
            figs = [it for it in its if it['k'] == 'vis']
            if not figs: continue
            text = sum(it.get('size', 36) * 1.55 * ((1.9 if '/' in it['_hand'] else 1.45) if it.get('_hand') else
                                                     (1.6 if 'frac' in it['t'] else 1)) + 16 for it in its if it['k'] != 'vis')
            bases = [it for it in figs if not it.get('over')]
            fh = sum(it['h'] + 16 for it in bases)
            if not fh: continue
            k = min(maxk, (room - text) / float(fh), min(maxw / float(it['w']) for it in figs))
            if k <= 1.05: continue
            for it in figs:
                it['w'] = int(round(it['w'] * k)); it['h'] = int(round(it['h'] * k))
_scale_lesson_figures()
def _clause_rows(vid, name, *pieces):
    found = 0
    for sl in VIDEOS[vid]['slides']:
        for ln in sl['lines']:
            cues = []
            for cue in ln['cues']:
                if cue[0] == 'show' and cue[1]['_name'] == name:
                    old = cue[1]; found += 1
                    for j, (tex, anchor) in enumerate(pieces):
                        assert anchor.lower() in ln['say'].lower(), (vid, name, anchor)
                        make = IH if old.get('_hand') else I
                        it = make(name if not j else name+'_clause'+str(j), tex,
                                  size=old.get('size',30), col=old['_col'])
                        cues.append(show(it, anchor))
                else: cues.append(cue)
            ln['cues'] = sorted(cues, key=lambda c: _phrase_pos(ln['say'],c))
    assert found == 1, (vid, name, found)

def _later(vid, name, anchor):
    found = 0
    for sl in VIDEOS[vid]['slides']:
        for ln in sl['lines']:
            for j,c in enumerate(ln['cues']):
                if c[0]=='show' and c[1]['_name']==name:
                    assert anchor.lower() in ln['say'].lower(), (vid,name,anchor)
                    ln['cues'][j]=(c[0],c[1],anchor); found+=1
            ln['cues'].sort(key=lambda c: _phrase_pos(ln['say'],c))
    assert found==1,(vid,name,found)

# Position helper here because these edits run before the automatic visual passes.
def _phrase_pos(say, c):
    ph = c[2] if c[0] in ('show', 'point') else c[3]
    return -1 if ph.startswith('<') else say.lower().find(ph.lower())
STEMS_T28 = {
 'wp28-g124': 'How many three-digit numbers can be made from the digits 3, 5, 6 and 9 if the hundreds digit is smaller than the tens digit and the tens digit is smaller than the units digit?',
 'wp28-g125': 'A food truck offers 7 soups and 3 kinds of bread. A lunch contains one soup and one kind of bread. How many different lunches are possible?',
 'wp28-g126': 'A locker number has two digits, each from 0 to 9. The sum of the two digits must be 14. How many locker numbers are possible?',
 'wp28-g128': 'A suitcase lock has three wheels. Each wheel shows one of the digits 1 to 9, and digits may repeat. How many codes are possible?',
 'wp28-g129': 'A suitcase lock has three wheels. Each wheel shows one of the digits 1 to 9, and no digit may appear twice. How many codes are possible?',
 'wp28-g130': 'In how many different ways can 7 different trophies be placed in a row in a glass cabinet?',
 'wp28-g132': 'Six towns are connected so that every pair of towns has exactly one direct two-way bus line. How many bus lines are there?',
 'wp28-g133': 'How many diagonals does an eight-sided polygon have?',
 'wp28-g135': 'A breakfast stand offers 6 hot drinks and 5 pastries. A customer chooses one of each. If the drink is espresso, the pastry must be a croissant; with any other drink, any pastry is allowed. How many choices are possible?',
 'wp28-g136': 'A green dice and a yellow dice each show a number from 1 to 6. How many ordered outcomes have a sum different from 8?',
 'wp28-g139': 'In how many different ways can a team of 11 players be chosen from a squad of 12 players?',
 'wp28-g138': 'Ten hikers are split between two guides, Lena and Omar, with five hikers assigned to each guide. How many different splits are possible?',
 'wp28-g140': 'What is the ratio of the number of row arrangements of 9 distinct objects to the number of row arrangements of 7 distinct objects?',
 'q-r26-t28-28': '$\\dfrac{10!-9!}{8!}=?$',
 'wp28-g141': 'How many three-digit numbers have a hundreds digit and a units digit whose sum is 8?',
 'wp28-g143': 'In a table-tennis league, each pair of players plays exactly one match. There are 66 matches altogether. How many players take part?',
 'wp28-g144': 'Eight children all have different heights. A photographer chooses seven of them and places them in a row from shortest to tallest. How many different rows can be formed?',
 'wp28-g142': 'The digits 2, 5, 6 and 9 go once each into a square: A and B on top, C and D below. A is even. $C\\times D$ is even. How many arrangements are possible?',
 'q-r26-t28-04': 'A code has 4 digits. Each digit is from 0 to 9, digits may repeat, and the code may start with 0. How many codes contain the digit 5 at least once?',
 'q-r26-t28-05': 'Five different letters are put into 3 mailboxes. A mailbox may get any number of letters, or none. In how many different ways can the letters be put into the mailboxes?',
 'q-r26-t28-06': 'Six different books are placed on a shelf in a row. The 3 math books among them must stand together, in any order. How many arrangements are possible?',
 'q-r26-t28-07': 'Three boys and two girls stand in a row. All five are different people. The two girls may not stand next to each other. How many orders are possible?',
 'q-r26-t28-08': 'How many different arrangements of all the letters of the word BANANA are there? (An arrangement does not have to be a real word.)',
 'q-r26-t28-09': 'Six people sit around a round table. Two arrangements are the same if one is a rotation of the other. Dana and Eli must sit next to each other. How many arrangements are possible?',
}


# 2026-10-23: the last baseline of each question's stem on the board (estimated from the stem length, about 64 characters
# a line, then checked on the rendered step frames).
def _qbot_est(stem):
    import textwrap
    n = len(textwrap.wrap(re.sub(r'\$', '', stem), 64))
    return {1: 137, 2: 181, 3: 232, 4: 286, 5: 330}.get(n, 330)
for _v, _V in VIDEOS.items():
    if _V['kind'] == 'solution' and _V.get('qid') in STEMS_T28 and _v not in QBOT:
        QBOT[_v] = _qbot_est(STEMS_T28[_V['qid']])


# 2026-10-23 visual check: a lesson board has room for one tall column. A lesson slide whose items all fit in the left
# column (about 880 px from y 78) gets them all there, in speaking order - no lone rows top right, no figure squeezed to
# the half width, no overlap with a wide sketch. A slide that would not fit keeps its two columns.
def _h_est(it):
    if it['k'] == 'vis': return it['h'] * min(1.0, 1060.0 / it['w']) + 16 if not it.get('over') else 0
    f = (1.9 if '/' in it['_hand'] or 'frac' in it['t'] else 1.45) if it.get('_hand') else (1.6 if 'frac' in it['t'] else 1)
    return it.get('size', 36) * 1.55 * f + 16
ONECOL = []
for _v, _V in VIDEOS.items():
    if _V['kind'] != 'lesson': continue
    for _sl in _V['slides']:
        _its = [c[1] for ln in _sl['lines'] for c in ln['cues'] if c[0] == 'show']
        if not any(it['_col'] == 1 for it in _its): continue
        if sum(_h_est(it) for it in _its) <= 880:
            for it in _its: it['_col'] = 0
            ONECOL.append((_v, _sl['title']))


# 2026-10-23 visual check: a question's sketch (ROAD) keeps its full width on the left; the right column then starts
# below the sketch instead of beside it (the sketch's labels stay readable).
WIDE = set()
for _v, _V in VIDEOS.items():
    for _sl in _V['slides']:
        for ln in _sl['lines']:
            for c in ln['cues']:
                if c[0] == 'show' and c[1].get('fig', c[1].get('of')) in WIDE: c[1]['_wide'] = True

# 2026-10-23 visual check: on a slide with a right column, a left-column figure is at most 570 wide (it ends before the
# right column at x 1010); its layers are scaled with it.
for _v, _V in VIDEOS.items():
    for _sl in _V['slides']:
        _its = [c[1] for ln in _sl['lines'] for c in ln['cues'] if c[0] == 'show']
        if not any(it['_col'] == 1 for it in _its): continue
        for it in _its:
            if it['_col'] == 0 and it['k'] == 'vis' and it['w'] > 570 and not it.get('_wide'):
                it['h'] = int(round(it['h'] * 570.0 / it['w'])); it['w'] = 570


_layout_before_wide = _layout


def _layout(vid):
    names, per = _layout_before_wide(vid)
    sol = VIDEOS[vid]['kind'] == 'solution'
    for sl in per:
        if not any(it.get('_wide') for it, d in sl): continue
        y = max(100, QBOT.get(vid, 0) + 50) if sol else 78; bottom = None
        for it, d in sl:
            if d.get('x') == 1010 or d.get('over'): continue
            h = d['h'] if d['k'] == 'vis' else d.get('size', 36) * 1.55 * ((1.9 if '/' in it['_hand'] else 1.45) if it.get('_hand') else 1)
            if it.get('_wide'): bottom = y + h; break
            y += h + 16
        rights = [d for it, d in sl if d.get('x') == 1010 and d.get('y') is not None]
        if rights and bottom:
            dy = bottom + 16 - min(r["y"] for r in rights)
            if dy > 0:
                for r in rights: r['y'] += dy
    return names, per


# post-content fixes (clause rows etc.)
# 2026-10-25 visual check (V4): each result at its own clause
_clause_rows('wp-127', 'p_b2', ('$6\\times6=36$', 'Six times six is thirty-six'), ('$36\\times6=216$', 'Then thirty-six times six'))
_clause_rows('wp-127', 'p_b4', ('$6\\times5=30$', 'Six times five is thirty'), ('$30\\times4=120$', 'Then thirty times four'))
_clause_rows('solve-wp28-g138', 'g38f', ('$3\\times2=6$', 'Three times two is six'), ('$6\\times7=42$', 'Then six times seven'),
             ('$42\\times6=252$', 'Forty-two times six'))
_clause_rows('wp-140-after', 'f_t7', ('$6\\times700=4200$', 'Six times seven hundred'), ('$6\\times20=120$', 'And six times twenty'),
             ('$4200+120=4320$', 'Together four'))
_clause_rows('wp-140-after', 'f_u5', ('$16\\times9=144$', 'Sixteen times nine'), ('$144\\times5=720$', 'Times five'))
_clause_rows('wp-140-after', 'f_u1', ('$6=2\\times3$', 'Six is two times three'), ('$4=2\\times2$', 'four is two times two'))
_clause_rows('solve-wp28-g135', 'g35d', ('$5\\times4+1=21$: $\\ $the trap', 'five times four plus one'))
_clause_rows('wp-137', 'q_c3', ('$6\\times5=30$', 'Six times five is thirty'), ('$30\\div2=15$ groups', 'Then thirty divided by two'))
_clause_rows('wp-137', 'q_b1', ('as usual: $\\ 5\\times4=20$', 'Five times four is twenty'), ('$20\\times3=60$', 'Then twenty times three'))
_clause_rows('solve-wp28-g140', 'g40f', ('$\\dfrac{9\\times8\\times7!}{7!}$', 'seven factorial cancels'), ('$=9\\times8=72$', 'Nine times eight is seventy-two again'))
CARRY28['wp-140-after-3'] = {2: ['$6!=2^4\\times3^2\\times5$']}     # the new slide "Is it divisible?" leans on it
_clause_rows('solve-q-r26-t28-28', 'q28c', ('$\\dfrac{9\\times9!}{8!}=9\\times\\dfrac{9!}{8!}$', 'Now we divide by eight factorial'),
             ('$=9\\times9=81$', 'So nine times nine'))
_later('solve-wp28-g143', 'g43f', 'Eleven times ten is a hundred ten')
_later('solve-wp28-g143', 'g43h', 'Twelve times eleven is a hundred thirty-two')
CARRY28['solve-q-r26-t28-04'] = {1: ['$10000-6561=3439$']}
CARRY28['solve-wp28-g138'] = {1: ['$\\dfrac{10\\times9\\times8\\times7\\times6}{5\\times4\\times3\\times2\\times1}$']}
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
STEMS = dict(STEMS_T28)   # word stems: "given" = the story, "ask" = the question sentence

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
MV.carry(_types.SimpleNamespace(**globals()), CARRY28)
for _v in CARRY28:                                      # 2026-10-18 visual check: the So-far box at a readable size
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
