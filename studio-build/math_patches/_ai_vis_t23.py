"""Topic 23 (Percentages) - the scripts for the teacher's own-voice reading (2026-10-20), written from the first draft to
the Codex review standard, the clarity style, W1-W21, the method vocabulary and the method visuals, built exactly like
topics 21-22 (math_patches/_ai_vis_t22.py: the DSL, the TBL / UNITS / ZL builders, the real-row-height layout, the
pen-safe rules and the visual passes are copied here, so the topics stay independent).

The camera lesson 'wp-052' (Calculating Percentages) gets a full reading script with more examples, split into four
parts of about 3-4 minutes (math_patches/_camera_parts.py). Every other topic-23 video gets a script that SHE reads aloud
in the Reading Studio; reading_to_video.py then times the handwriting and the visuals to her words. The summary video
r26-t23-summary is not read: summary_pages/t23.json (python3 summary_pages.py 23) replaces it.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t23.py [vid ...] writes it);
  - the visual plan VIS[vid] in the _ai_visual.py format;
  - the studio video: t23.py ai_redo_t23() (runs LAST) rebuilds the slides from studio_slides(vid) and then
                    _ai_visual.apply() adds the cues and click items around them.

Figures (V1): TBL (the ratio table: percent | amount, the triangle value's diagonal), PTREE (the percent tree), AMAP
(the arrow map). The concept map (NEW / REMINDER per video) is in ~/Downloads/Topic-23-AI-scripts-review.md.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(HERE) != 'math_patches':      # a test copy elsewhere still reads and writes the real studio files
    HERE = '/Users/nitzanslasky/psychometry-course/studio-build/math_patches'
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t23ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-23 flow order of the scripts
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
QBOT = {}   # measured below (QBOT23)


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
CAM_BASE = 'wp-052'
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
            'style': "the teacher reads it herself (Reading Studio), topic-23 scripts (2026-10-20): math_patches/_ai_vis_t23.py is "
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
    VB = '0 0 640 186'
    def txt(x, y, t, c, size=24, style=''):
        return ('<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="%d" font-weight="bold"%s>%s</text>'
                % (x, y, c, FONT, size, (' font-style="%s"' % style) if style else '', t))
    body = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.5"/>' % (L_ - 6, Y_, R_ + 6, Y_, INK) +
            '<path d="M %d %d l 12 -7 l 0 14 Z" fill="%s"/>' % (L_ - 10, Y_, INK) + '<path d="M %d %d l -12 -7 l 0 14 Z" fill="%s"/>' % (R_ + 10, Y_, INK))
    for t in ticks:
        v, lab = t if isinstance(t, tuple) else (t, ('−%s' % -t) if t < 0 else str(t))
        body += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2"/>' % (X(v), Y_ - 10, X(v), Y_ + 10, INK) + txt(X(v), Y_ + 40, lab, INK, 30)
    out = [('line', _svg(VB, body, title))]
    for key, marks in layers:
        b = ''
        for m in marks:
            if m[0] in ('pt', 'ink'):
                c = TEAL if m[0] == 'pt' else INK
                b += '<circle cx="%.1f" cy="%d" r="7" fill="%s"/>' % (X(m[1]), Y_, c) + txt(X(m[1]), Y_ - 18, m[2], c, 30, 'italic')
            elif m[0] == 'arrow':
                a, e = X(m[1]), X(m[2]); d = 1 if e > a else -1
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3"/>' % (a, Y_ - 58, e - 10 * d, Y_ - 58, TEAL) +
                      '<path d="M %.1f %d l %d -7 l 0 14 Z" fill="%s"/>' % (e, Y_ - 58, -14 * d, TEAL))
                if m[3]: b += txt((a + e) / 2, Y_ - 70, m[3], TEAL, 28)
            elif m[0] == 'shade':
                b += '<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (X(m[1]), Y_ - 7, X(m[2]) - X(m[1]), BAND, TEAL)
            elif m[0] == 'cross':
                x0 = X(m[1]); y0 = Y_ - 58
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (x0 - 14, y0 - 14, x0 + 14, y0 + 14, RED) +
                      '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (x0 + 14, y0 - 14, x0 - 14, y0 + 14, RED))
            elif m[0] == 'below':
                b += txt(X(m[1]), Y_ + 68, m[2], TEAL, 28)
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


# ------------------------------------------------------------------------------------------- word-problem figures (V1, copied from topic 22)
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
    body += ''.join(_tx(cx(k), y0 + headh * .68, h, 27) for k, h in enumerate(head))
    left = x0 if haslab else xs[0]
    body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4"/>' % (xs[0], y0, xs[-1], y0, _INK)
    for r in range(nr + 1):
        y = top(r)
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s"/>' % (left if r else xs[0], y, xs[-1], y, _INK, 2.4 if r == 0 else 1.6)
    for x in xs:
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>' % (x, y0, x, top(nr), _INK)
    if haslab:
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>' % (x0, top(0), x0, top(nr), _INK)
        body += ''.join(_tx(x0 + lw / 2.0, cy(r), lab, 26) for r, lab in enumerate(rowlab))
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
                f = '#fbe3cf' if len(m) > 4 and m[4] == 'orange' else MV.BAND
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




# ------------------------------------------------------------------------------------------- topic-23 figures (V1)
#   PTREE  the percent tree (wp 3338-3392: the root is the whole, 100%; a split adds up to 100%; going down a branch
#          makes that group the new 100%; a leaf = the product along its path). Bigger labels than MV.PCTTREE.
#   AMAP   the arrow map (English addition, ~13 real questions): one arrow per "is p% more than / of" sentence, from the
#          whole (the word after "than" / "of") to the other one, the multiplier written on it.
def PTREE(name, root, first, second, col=0, w=None, title='Percent tree'):
    """root = (label, pct); first = [(label, pct), (label, pct)]; second = (index of the node that splits, [(l, p), (l, p)])
    -> layers 'line' (the root), 'b1' (the first split), 'b2' (the second split). Drawn at 1:1 (620 wide), labels ~30."""
    W, H = 640, 300; ry = 132
    out = [('line', MV._svg(W, H, _tx(8, ry - 4, root[0], 30, _INK, 'start') + _tx(8, ry + 30, root[1], 28, _TEAL, 'start'), title))]
    ys = [48, 216]
    b = ''
    for (lab, p), y in zip(first, ys):
        b += '<line x1="104" y1="%d" x2="218" y2="%d" stroke="%s" stroke-width="3"/>' % (ry, y, _INK)
        b += _tx(228, y + 10, lab, 30, _INK, 'start') + _tx(150, (ry + y) / 2.0 + (-12 if y < ry else 34), p, 28, _TEAL)
    out.append(('b1', MV._svg(W, H, b, title + ': first split')))
    k, kids = second; y0 = ys[k]; x0 = 228 + 17 * len(first[k][0]) + 14; b = ''
    for j, (l2, p2) in enumerate(kids):
        y2 = y0 + (-1 if j == 0 else 1) * 52
        b += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.8"/>' % (x0, y0, x0 + 96, y2, _INK)
        b += _tx(x0 + 106, y2 + 10, l2, 30, _INK, 'start') + _tx(x0 + 40, (y0 + y2) / 2.0 + (-10 if j == 0 else 32), p2, 27, _TEAL)
    out.append(('b2', MV._svg(W, H, b, title + ': second split')))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def AMAP(name, nodes, arrows, gap=250, col=0, w=None, title='Arrow map'):
    """nodes = labels left to right; arrows = [(key, i, j, label)] between neighbours, drawn in layers (base = the names)"""
    n = len(nodes); x0 = 80; W = 2 * x0 + (n - 1) * gap; H = 150; yn = 120
    X = lambda i: x0 + i * gap
    base = ''.join(_tx(X(i), yn, t, 34, _INK) for i, t in enumerate(nodes))
    out = [('line', MV._svg(W, H, base, title + ': ' + ', '.join(nodes)))]
    for key, i, j, lab in arrows:
        hw = lambda k: 13 * len(nodes[k]) + 16
        d = 1 if j > i else -1
        xa, xb = X(i) + d * hw(i), X(j) - d * hw(j)
        b = MV._arrow(xa, yn - 11, xb, yn - 11, _TEAL, 3) + _tx((X(i) + X(j)) / 2.0, yn - 34, lab, 30, _TEAL)
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


# =================================================================================================================
# THE SCRIPTS (topic-23 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-23-AI-scripts-review.md.
# Study plan before topic 23: 1, 30, 2, 4, 31, 6, 8, 32, 9, 10, 33, 51, 21, 3, 22, 5, 7. So fractions (2, 3), decimals,
# equations (6, 7), expressions (5), plugging in numbers / the answers and estimation (51), the ratio table and the
# triangle value, "of" = times, "is" = equals (22) are REMINDERS. Percent itself is NEW here (t33-03 used a little).
# Inequalities (12), averages (25) come LATER. 2026-10-21 rule R37: the CORE methods (used in several questions or
# common on the real exam) are taught in the LESSON wp-053 (now in 4 parts): the change rule, multipliers, working back
# from what is left, the arrow map (83 1/3%, not 80%), the flip rule and "same whole, keep". The first question that uses
# each one applies it step by step ("like in the lesson"): g059, g060, g065, g061, q-r26-t23-16. One-off tricks stay in
# their question: the two-changes formula (q-r26-t23-01), the swap x% of y = y% of x (g062). Numbers differ from the
# Hebrew course.
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ wp-052 (camera lesson)
# Hebrew (wp 2685-3080): a percent is a part, like a fraction; 50% off = half price; 100% = the whole, 1% = a hundredth;
# the % sign is a fraction sign; percent -> fraction (over 100, reduce), fraction -> percent (expand to 100); the
# fractions to know (1/2, 1/4, 1/8 by halving; 1/10, 1/5, 1/20; 1/3, 1/6 "sixteen and a bit"); families (3/8, 5/8,
# 3/5, 7/20); three ways: the percent equation (a known percent, an unknown percent, the letter inside), equal ratios /
# the triangle value (and "no whole needed"), the 10% method (chunks, 5% = half of 10%; decimals are rare). NEW (all).
# English additions (teacher: 2-3 examples per concept on camera): 64% = 16/25, 3/20 = 15%, 4/5 = 80%, the check of
# the unknown percent, "the whole is missing" (30% is 63 -> 210). Numbers differ from the Hebrew.
k_1 = IH('k_1', '$100\\%$ $=$ the whole', size=34)
k_2 = IH('k_2', '$1\\%=\\frac{1}{100}$', size=34)
k_3 = IH('k_3', '$29\\%=\\frac{29}{100}$', size=34)
k_4 = IH('k_4', 'A percent of what?', size=32)
k_5 = IH('k_5', '$29\\%$ of $100=29$ tickets', size=30)
k_6 = IH('k_6', '$29\\%$ of $200$', size=30)
k_6b = IH('k_6b', '$2\\cdot29=58$ tickets', size=30)
k_7 = IH('k_7', '$50\\%=\\frac{50}{100}$', size=32)
k_7b = IH('k_7b', '$=\\frac{1}{2}$', size=32, col=1)
k_8 = IH('k_8', '$30\\%=\\frac{30}{100}$', size=32)
k_8b = IH('k_8b', '$=\\frac{3}{10}$', size=32, col=1)
k_9 = IH('k_9', '$64\\%=\\frac{64}{100}$', size=32)
k_10 = IH('k_10', '$64\\div4=16,\\ \\ 100\\div4=25$', size=30)
k_11 = IH('k_11', '$\\frac{64}{100}=\\frac{16}{25}$', size=32)
k_12 = IH('k_12', '$\\frac{11}{25}$: $\\ 25\\cdot4=100$', size=32)
k_13 = IH('k_13', '$11\\cdot4=44$', size=30)
k_14 = IH('k_14', '$\\frac{44}{100}=44\\%$', size=32)
k_15 = IH('k_15', '$\\frac{7}{50}$: $\\ 50\\cdot2=100$', size=30, col=1)
k_16 = IH('k_16', '$7\\cdot2=14$: $\\ 14\\%$', size=30, col=1)
k_17 = IH('k_17', '$\\frac{3}{20}$: $\\ 20\\cdot5=100$', size=30, col=1)
k_18 = IH('k_18', '$3\\cdot5=15$: $\\ 15\\%$', size=30, col=1)
k_20 = IH('k_20', '$\\frac{1}{2}=50\\%$', size=32)
k_21 = IH('k_21', '$\\frac{1}{4}=25\\%$', size=32)
k_22 = IH('k_22', '$\\frac{1}{8}=12.5\\%$', size=32)
k_23 = IH('k_23', '$50\\to25\\to12.5$: $\\ $half each time', size=30)
k_24 = IH('k_24', '$12.5=12\\frac{1}{2}$', size=30, col=1)
k_25 = IH('k_25', '$0.5,\\ \\ 0.25,\\ \\ 0.125$', size=30, col=1)
k_26 = IH('k_26', '$\\frac{1}{10}=10\\%$', size=32)
k_27 = IH('k_27', '$\\frac{1}{5}=\\frac{2}{10}=20\\%$', size=32)
k_28 = IH('k_28', '$\\frac{1}{20}=5\\%$', size=32)
k_29 = IH('k_29', 'check: $\\ \\frac{1}{20}=\\frac{5}{100}=5\\%$', size=30)
k_30 = IH('k_30', '$\\frac{1}{3}=33\\frac{1}{3}\\%$', size=32)
k_31 = IH('k_31', '$\\frac{1}{6}$ $=$ half of $\\frac{1}{3}$', size=32)
k_32 = IH('k_32', 'half of $32=16$: $\\ $a bit more than $16$', size=30)
k_33 = IH('k_33', '$16\\frac{1}{2}+\\frac{1}{6}=16\\frac{2}{3}$', size=30)
k_34 = IH('k_34', '$\\frac{1}{6}=16\\frac{2}{3}\\%$', size=32)
k_35 = IH('k_35', '$\\frac{3}{8}=3\\cdot12.5\\%$', size=30)
k_36 = IH('k_36', '$3\\cdot12=36$', size=30)
k_36b = IH('k_36b', '$36+1.5=37.5\\%$', size=30)
k_37 = IH('k_37', '$\\frac{5}{8}=5\\cdot12.5\\%$', size=30)
k_37b = IH('k_37b', '$60+2.5=62.5\\%$', size=30)
k_38 = IH('k_38', '$\\frac{3}{5}=3\\cdot20\\%=60\\%$', size=30, col=1)
k_39 = IH('k_39', '$\\frac{4}{5}=80\\%$', size=30, col=1)
k_40 = IH('k_40', '$\\frac{7}{20}=7\\cdot5\\%=35\\%$', size=30, col=1)
k_41 = IH('k_41', 'percent $=$ over $100$ $\\qquad$ of $=\\times$', size=32)
k_42 = IH('k_42', '$45\\%$ of $80=\\ ?$', size=32)
k_43 = IH('k_43', '$\\frac{45}{100}\\cdot80$', size=32)
k_44 = IH('k_44', '$=\\frac{45\\cdot4}{5}$', size=32)
k_44a = IH('k_44a', '$80\\div20=4,\\ \\ 100\\div20=5$', size=30)
k_45 = IH('k_45', '$45\\div5=9$', size=30, col=1)
k_45b = IH('k_45b', '$9\\cdot4=36$', size=30, col=1)
k_46 = IH('k_46', '$x\\%$ of $75$ is $21$. $\\ x=\\ ?$', size=32)
k_47 = IH('k_47', '$\\frac{x}{100}\\cdot75=21$', size=32)
k_48 = IH('k_48', '$\\frac{75}{100}=\\frac{3}{4}$', size=30)
k_49 = IH('k_49', '$\\frac{3}{4}x=21$', size=32)
k_50 = IH('k_50', '$\\frac{1}{4}x=21\\div3=7$', size=30, col=1)
k_51 = IH('k_51', '$x=4\\cdot7=28$', size=32, col=1)
k_52 = IH('k_52', 'check: $\\ \\frac{3}{4}\\cdot28=21$', size=30, col=1)
k_53 = IH('k_53', '$(5+x)\\%$ of $60=(70-x)\\%$ of $40$', size=32)
k_54 = IH('k_54', '$\\frac{5+x}{100}\\cdot60=\\frac{70-x}{100}\\cdot40$', size=32)
k_55 = IH('k_55', '$(5+x)\\cdot60=(70-x)\\cdot40$', size=30)
k_56 = IH('k_56', '$3(5+x)=2(70-x)$', size=30, col=1)
k_57 = IH('k_57', '$15+3x=140-2x$', size=30, col=1)
k_58 = IH('k_58', '$5x=125$', size=30, col=1)
k_59 = IH('k_59', '$x=25$', size=30, col=1)
k_t1 = TBL('k_t1', ['Percent', 'Amount'], ['', ''], [
    ('r1', [('c', 0, 0, '100%'), ('c', 0, 1, '80')]), ('r2', [('c', 1, 0, '45%'), ('q', 1, 1)]),
    ('dg', [('diag', (1, 0), (0, 1))]), ('ans', [('cover', 1, 1, '36')])], col=0, colw=180, w=480)
k_60 = IH('k_60', '$?=\\frac{45\\cdot80}{100}$', size=30, col=1)
k_60b = IH('k_60b', '$=36$', size=30, col=1)
k_61 = IH('k_61', '$15\\%$ is $54$. $\\quad 25\\%=\\ ?$', size=30)
k_t2 = TBL('k_t2', ['Percent', 'Amount'], ['', '', ''], [
    ('r1', [('c', 0, 0, '15%'), ('c', 0, 1, '54')]), ('r2', [('c', 1, 0, '5%'), ('c', 1, 1, '18')]),
    ('q', [('c', 2, 0, '25%'), ('q', 2, 1)]), ('ans', [('cover', 2, 1, '90')])], col=0, colw=180, w=480)
k_62 = IH('k_62', '$15\\div3=5,\\ \\ 54\\div3=18$', size=30, col=1)
k_63 = IH('k_63', '$25\\%=5\\cdot5\\%$', size=30, col=1)
k_64 = IH('k_64', '$5\\cdot18=90$', size=30, col=1)
k_65 = IH('k_65', '$10\\%$ of $240=24$', size=32)
k_66 = IH('k_66', '$10\\%$ of $48=4.8$', size=32)
k_66q = IH('k_66q', '$30\\%$ of $240=\\ ?$', size=30)
k_67 = IH('k_67', '$30\\%=3\\cdot10\\%$', size=30)
k_67b = IH('k_67b', '$3\\cdot24=72$', size=30)
k_68 = IH('k_68', '$35\\%=30\\%+5\\%$', size=30)
k_69 = IH('k_69', '$5\\%=24\\div2=12$', size=30)
k_70 = IH('k_70', '$35\\%=72+12=84$', size=30)
k_71 = IH('k_71', '$30\\%$ of a number is $63$. $\\ $The number?', size=30)
k_72 = IH('k_72', '$10\\%=63\\div3=21$', size=30)
k_73 = IH('k_73', '$100\\%=10\\cdot21=210$', size=30)
k_74 = IH('k_74', 'check: $\\ 3\\cdot21=63$', size=30)
k_s1 = IH('k_s1', 'percent $=$ over $100$ $\\qquad$ of $=\\times$', size=30)
k_s2 = I('k_s2', 'The percent equation: $\\ $works every time', size=30)
k_s3 = I('k_s3', 'The ratio table: $\\ $quick, no whole needed', size=30)
k_s4 = I('k_s4', '$10\\%$ chunks: $\\ $round percents, in your head', size=30)
k_s5 = I('k_s5', 'Know the fraction table by heart', size=30)
video('wp-052', 'lesson', slides=[
    S('Calculating Percentages',
      L("Welcome back, and now we're starting a new topic, percentages. Percent questions come up in almost every exam. "
        "They also come up inside chart questions and other word problems."),
      L("And honestly, you already know more than you think. Everybody knows that fifty percent off means half price. "
        "Today we'll make that feeling exact, and fast.")),
    S('What a percent is',
      L("So what is a percent? A percent is a way to describe a part of something. It's just like a fraction."),
      L("One hundred percent is the whole. The whole class, the whole price, the whole bottle.",
        show(k_1, 'One hundred percent is the whole')),
      L("So one percent is one hundredth of the whole. If we cut the whole into a hundred equal parts, one percent is one "
        "of those parts.", show(k_2, 'So one percent is one hundredth')),
      L("Look at the percent sign itself. It has a small circle, a slash, and another small circle. It looks like a "
        "fraction, a number over a number. And that's exactly what it means, something over a hundred."),
      L("So twenty-nine percent is twenty-nine over a hundred. Twenty-nine parts out of a hundred.",
        show(k_3, 'So twenty-nine percent is')),
      L("Careful here. A percent alone is not an amount. It's always a percent of something. So we always ask, a percent "
        "of what?", show(k_4, 'a percent of what')),
      L("Twenty-nine percent of a hundred tickets is twenty-nine tickets. But twenty-nine percent of two hundred tickets "
        "is twice that. Two times twenty-nine is fifty-eight tickets.", show(k_5, 'Twenty-nine percent of a hundred tickets'),
        show(k_6, 'But twenty-nine percent of two hundred'), show(k_6b, 'Two times twenty-nine'))),
    S('Percent to fraction',
      L("Now let's go from a percent to a fraction. It's simple. We write the percent over a hundred, and then we reduce."),
      L("Fifty percent is fifty over a hundred. Fifty and a hundred both divide by fifty. So it's one over two, one half. "
        "Half price, just as we said.", show(k_7, 'Fifty percent is fifty over'), show(k_7b, "So it's one over two")),
      L("Thirty percent is thirty over a hundred. Both divide by ten, so it's three over ten, three tenths.",
        show(k_8, 'Thirty percent is thirty over'), show(k_8b, "so it's three over ten")),
      L("One more. Sixty-four percent is sixty-four over a hundred. Both divide by four.", show(k_9, 'Sixty-four percent is')),
      L("Sixty-four divided by four is sixteen. A hundred divided by four is twenty-five. So sixty-four percent is "
        "sixteen over twenty-five.", show(k_10, 'Sixty-four divided by four'), show(k_11, 'So sixty-four percent is sixteen'))),
    S('Fraction to percent',
      L("Now the other way, from a fraction to a percent. We expand the fraction until the bottom is a hundred. Then the "
        "top is the percent."),
      L("Let's take eleven over twenty-five. How do we get from twenty-five to a hundred? Twenty-five times four is a "
        "hundred.", show(k_12, 'Twenty-five times four is')),
      L("So we multiply the top by four too. Eleven times four is forty-four. That's forty-four over a hundred, forty-four "
        "percent.", show(k_13, 'Eleven times four'), show(k_14, "That's forty-four over a hundred")),
      L("Why can we multiply the top and the bottom by the same number? Because the fraction stays the same. We just cut "
        "it into smaller pieces."),
      L("Another one, seven over fifty. Fifty times two is a hundred. So the top is also times two. Seven times two is "
        "fourteen, so it's fourteen percent.", show(k_15, 'Fifty times two'), show(k_16, 'Seven times two')),
      L("And three over twenty. Twenty times five is a hundred. Three times five is fifteen. So three over twenty is "
        "fifteen percent.", show(k_17, 'Twenty times five'), show(k_18, 'Three times five'))),
    S('Fractions to know',
      L("Some fractions come up again and again on the exam. It's worth knowing their percents by heart, because then we "
        "don't need to calculate."),
      L("A half is fifty percent. A quarter is twenty-five percent. Almost everyone knows these two.",
        show(k_20, 'A half is fifty percent'), show(k_21, 'A quarter is twenty-five')),
      L("What people forget is an eighth. An eighth is twelve and a half percent.", show(k_22, 'An eighth is twelve')),
      L("How do we remember it? A quarter is half of a half, and twenty-five is half of fifty. An eighth is half of a "
        "quarter. So we halve twenty-five too, and half of twenty-five is twelve and a half.",
        show(k_23, 'An eighth is half of a quarter')),
      L("On the exam you'll see twelve point five, and also twelve and a half. It's the same number, so get used to both.",
        show(k_24, 'twelve and a half. It')),
      L("As decimals it's the same idea. Zero point five, zero point two five, and zero point one two five.",
        show(k_25, 'Zero point five'))),
    S('Tenths and fifths',
      L("Now a second family. A tenth is ten percent. Most of us know this one for sure.", show(k_26, 'A tenth is ten percent')),
      L("A fifth is two tenths. So it's twice ten percent, twenty percent.", show(k_27, 'A fifth is two tenths')),
      L("And a twentieth is half of a tenth. Half of ten percent is five percent.", show(k_28, 'a twentieth is half')),
      L("Let's check it with the rule from before. One over twenty. Twenty times five is a hundred, so the top is one "
        "times five, five. Five over a hundred is five percent. It fits.", show(k_29, 'Five over a hundred is five'))),
    S('Thirds and sixths',
      L("A third is thirty-three and a third percent. Sometimes you'll see it as thirty-three point three three, and so "
        "on.", show(k_30, 'A third is thirty-three')),
      L("A sixth is less known. A sixth is half of a third. So we halve thirty-three and a third.",
        show(k_31, 'A sixth is half of a third')),
      L("That's not easy to halve in your head. Here's a quick way. Half of thirty-two is sixteen. So a sixth is sixteen "
        "and a bit.", show(k_32, 'Half of thirty-two is sixteen')),
      L("Exactly, it's sixteen and two thirds percent. Half of thirty-three is sixteen and a half. Half of a third is a "
        "sixth. And sixteen and a half plus a sixth is sixteen and two thirds.",
        show(k_33, 'And sixteen and a half plus a sixth'), show(k_34, 'is sixteen and two thirds.')),
      L("On the exam, sixteen and a bit is usually enough, because only one choice will be close to it.")),
    S('Families',
      L("Now let's build the families. Once we know the basic fraction, we can build the rest by multiplying."),
      L("An eighth is twelve and a half percent. So three eighths is three times twelve and a half.",
        show(k_35, 'So three eighths is three times')),
      L("Three times twelve is thirty-six. And three halves are one and a half. So it's thirty-seven and a half percent.",
        show(k_36, 'Three times twelve is thirty-six'), show(k_36b, "So it's thirty-seven")),
      L("Five eighths is five times twelve and a half. Five times twelve is sixty, and five halves are two and a half. So "
        "it's sixty-two and a half percent.", show(k_37, 'Five eighths is five times'), show(k_37b, "So it's sixty-two")),
      L("A fifth is twenty percent. So three fifths is three times twenty, sixty percent. And four fifths is eighty "
        "percent.", show(k_38, 'So three fifths is'), show(k_39, 'And four fifths is')),
      L("A twentieth is five percent. So seven twentieths is seven times five, thirty-five percent.",
        show(k_40, 'So seven twentieths is')),
      L("So don't try to memorize every fraction. Know the basic ones, and then multiply.")),
    S('The percent equation',
      L("There are three ways to calculate percents. The first is the percent equation. We translate the words into math, "
        "just like in word problems."),
      L("Remember from word problems, of means times. And percent means over a hundred.", show(k_41, 'of means times')),
      L("Let's see it on an example. What is forty-five percent of eighty?", show(k_42, 'What is forty-five percent')),
      L("Forty-five percent is forty-five over a hundred. Of means times, so it's times eighty.",
        show(k_43, "so it's times eighty")),
      L("Before we multiply, let's make the numbers smaller. Eighty and a hundred both divide by twenty. Eighty divided by "
        "twenty is four. A hundred divided by twenty is five. So we have forty-five times four, over five.",
        show(k_44a, 'Eighty divided by twenty'), show(k_44, 'So we have forty-five times four')),
      L("Forty-five divided by five is nine. And nine times four is thirty-six. So forty-five percent of eighty is "
        "thirty-six.", show(k_45, 'Forty-five divided by five'), show(k_45b, 'and nine times four'))),
    S('An unknown percent',
      L("The same translation works when the percent is the unknown. x percent of seventy-five is twenty-one. What is x?",
        show(k_46, 'x percent of seventy-five')),
      L("x percent is x over a hundred. Of means times, so it's times seventy-five. And is means equals, so it's equal "
        "to twenty-one.", show(k_47, "so it's equal to twenty-one")),
      L("Now seventy-five over a hundred is three quarters, from our table. So three quarters of x is twenty-one.",
        show(k_48, 'Now seventy-five over a hundred'), show(k_49, 'So three quarters of x')),
      L("Three quarters are twenty-one, so one quarter is twenty-one divided by three, seven. The whole x is four "
        "quarters, four times seven, twenty-eight.", show(k_50, 'so one quarter is'), show(k_51, 'four times seven')),
      L("Let's check. Twenty-eight percent of seventy-five is three quarters of twenty-eight. A quarter of twenty-eight "
        "is seven, and three quarters is twenty-one. It works.", show(k_52, 'three quarters is twenty-one'))),
    S('A letter inside the percent',
      L("And here's the exam version. The letter sits inside the percent. Five plus x percent of sixty is equal to seventy "
        "minus x percent of forty.", show(k_53, 'Five plus x percent of sixty')),
      L("It looks scary, but it's the same translation. Five plus x percent is five plus x, over a hundred, times sixty. "
        "And on the other side, seventy minus x, over a hundred, times forty.",
        show(k_54, 'And on the other side')),
      L("Both sides are over a hundred. So we multiply both sides by a hundred, and the hundreds are gone. We keep the "
        "brackets, because the sixty multiplies all of five plus x.", show(k_55, 'and the hundreds are gone')),
      L("Sixty and forty both divide by twenty, so we divide both sides by twenty. That gives three times five plus x, "
        "on the left, and two times seventy minus x, on the right.", show(k_56, 'That gives three times')),
      L("Now we open the brackets. Fifteen plus three x is equal to a hundred forty minus two x.",
        show(k_57, 'Fifteen plus three x')),
      L("We add two x to both sides, and take fifteen away from both sides. Five x is equal to a hundred twenty-five. We "
        "divide both sides by five, and x is twenty-five.", show(k_58, 'Five x is equal'), show(k_59, 'and x is twenty-five')),
      L("So the hard part is building the equation. After that, it's algebra we already know.")),
    S('Equal ratios',
      L("The second way is equal ratios, the ratio table from the ratios lesson. It's often quicker for simple "
        "calculations."),
      L("Let's find forty-five percent of eighty again. One column for the percents, one column for the amounts.",
        show(k_t1['line'], 'One column for the percents')),
      L("In the first row, what we know. The whole is a hundred percent, and the whole here is eighty.",
        show(k_t1['r1'], 'In the first row')),
      L("In the second row, forty-five percent, and a question mark for the amount.", show(k_t1['r2'], 'In the second row')),
      L("Across and down, there's no easy whole number. So we use the triangle value. We multiply along the diagonal, "
        "forty-five times eighty. And we divide by what's left, a hundred.", show(k_t1['dg'], 'We multiply along the diagonal'),
        show(k_60, 'And we divide by what')),
      L("That's the same calculation as before, so it's thirty-six again.", show(k_60b, "so it's thirty-six again"), show(k_t1['ans'], 'thirty-six again'))),
    S('No whole needed',
      L("Fifteen percent of a number is fifty-four. What is twenty-five percent of the "
        "same number?", show(k_61, 'Fifteen percent of a number')),
      L("Fifteen percent and fifty-four go in the first row. Twenty-five percent and a question mark go in the last row.",
        show(k_t2['line'], 'Fifteen percent and fifty-four'), show(k_t2['r1'], 'go in the first row'),
        show(k_t2['q'], 'Twenty-five percent and a question mark')),
      L("With an equation, we'd first find the whole number, and then take twenty-five percent of it. With the table, we "
        "don't need the whole."),
      L("Fifteen percent is fifty-four. Let's divide both by three. Fifteen divided by three is five. Fifty-four "
        "divided by three is eighteen. So five percent is eighteen.", show(k_62, "Let's divide both by three"),
        show(k_t2['r2'], 'So five percent is eighteen')),
      L("Twenty-five percent is five times five percent. So it's five times eighteen, ninety.",
        show(k_63, 'Twenty-five percent is five times'), show(k_64, 'five times eighteen'), show(k_t2['ans'], 'eighteen, ninety')),
      L("So we went straight to what they asked. We never found the whole.")),
    S('The ten percent method',
      L("The third way is ten percent. Ten percent is always easy to find, because it's just dividing by ten."),
      L("Ten percent of two hundred forty is twenty-four. We just take off the zero.", show(k_65, 'Ten percent of two hundred')),
      L("Ten percent of forty-eight is four point eight. The decimal point moves one place to the left.",
        show(k_66, 'Ten percent of forty-eight')),
      L("By the way, decimals like four point eight are rare on the exam. Most of the time, the numbers come out round.")),
    S('Building from ten percent',
      L("Now we build other percents from ten percent. What is thirty percent of two hundred forty?", show(k_66q, 'What is thirty percent')),
      L("Thirty percent is three times ten percent. Ten percent is twenty-four, so thirty percent is three times "
        "twenty-four, seventy-two.", show(k_67, 'Thirty percent is three times'), show(k_67b, 'so thirty percent is three times')),
      L("What about thirty-five percent? We split it into thirty percent and five percent.", show(k_68, 'We split it into')),
      L("Thirty percent is seventy-two, as we just saw. Five percent is half of ten percent. Half of twenty-four is "
        "twelve.", show(k_69, 'Half of twenty-four')),
      L("Together, seventy-two plus twelve is eighty-four. So thirty-five percent of two hundred forty is eighty-four.",
        show(k_70, 'seventy-two plus twelve'))),
    S('When the whole is missing',
      L("Ten percent also helps when the whole is missing. Thirty percent of a number is sixty-three. What is the number?",
        show(k_71, 'Thirty percent of a number is sixty-three')),
      L("Thirty percent is three times ten percent. So ten percent is sixty-three divided by three, twenty-one.",
        show(k_72, 'So ten percent is sixty-three')),
      L("The whole is a hundred percent, ten times ten percent. Ten times twenty-one is two hundred ten.",
        show(k_73, 'Ten times twenty-one')),
      L("Let's check. Ten percent of two hundred ten is twenty-one, and three times twenty-one is sixty-three. It works.",
        show(k_74, 'three times twenty-one is sixty-three'))),
    S('Summary',
      L("Let's sum up. Percent means over a hundred, and of means times.", show(k_s1, 'Percent means over')),
      L("We saw three ways to calculate. The percent equation works every time. The ratio table is quick, and we don't "
        "always need the whole. And ten-percent chunks are the fastest in your head, when the percents are round.",
        show(k_s2, 'The percent equation works'), show(k_s3, 'The ratio table is quick'), show(k_s4, 'And ten-percent chunks')),
      L("And know the fraction table by heart. A half, a quarter, an eighth, a tenth, a fifth, a twentieth, a third and a "
        "sixth. [pause] Take a moment to memorize the table on the memory card. In the next lesson we'll see a percent of "
        "a percent, and I'll see you in the next video.", show(k_s5, 'And know the fraction table'))),
])
CAMERA_SPLIT = ('wp-052', 'Calculating Percentages', [
    (1, None),
    (4, "Let's continue with percentages, and learn the fractions to know by heart."),
    (8, "Let's continue with percentages. Now let's calculate a percent of a number."),
    (12, "Let's continue with percentages, and see one more strength of the ratio table.")])


# ------------------------------------------------------------------------------------------------ wp-053 (lesson, in parts)
# Hebrew (wp 3082-3402): two types of percent questions; no whole given -> we'd call it x, but percent of a percent gets
# messy, so plug in 100 (any number works, 100 is the fastest; the number we get IS the percent); each new percent is of
# the NEW amount (the 100 is history); "after 'of' comes the whole", and with several, the "of" of the QUESTION decides.
# Kept from the English course: up and down by the same percent never comes back (p squared over 100), and when 100
# fails (a fixed amount). REMINDER: plugging in numbers (topic 51), the fraction table and 10% chunks (wp-052).
# 2026-10-21 rule R37 (teacher: "every method is taught properly, explained perfectly with extra examples"): the CORE
# methods of the topic are taught HERE, each with what / why / 2-3 worked examples from an easy one / the trap / "when
# you see ...": the change rule (first used in g059; also q-r26-t23-03), multipliers (g060, q-r26-t23-01, g061, g065),
# working back from what is left (g065, practice p13, 2026_spring_q2_07), the arrow map with the 83 1/3%-not-80% trap
# (g061, q-r26-t23-03, 2023_spring_q2_12), the flip rule and "the same whole: keep" (q-r26-t23-16, practice p14,
# 2020_autumn_q1_06, 2024_autumn_q2_08, 2019_spring_q2_12). Those questions now APPLY them ("like in the lesson").
# One-off tricks stay in their question: p + q + pq/100 (q-r26-t23-01), x% of y = y% of x (g062). New numbers here
# (none of a question's). The lesson is split into parts at idea boundaries (SPLIT053 below, _camera_parts.split).
p_1 = I('p_1', 'A price rises by $80\\%$, then falls by $25\\%$ of the new price. What is the change overall?', size=30)
p_2 = IH('p_2', 'price: $\\ 100$', size=30)
p_3 = IH('p_3', '$100+80=180$', size=30)
p_4 = IH('p_4', '$25\\%$ of $180=180\\div4=45$', size=30, col=1)
p_5 = IH('p_5', '$180-45=135$', size=30, col=1)
p_6 = IH('p_6', '$100\\to135$: $\\ +35\\%$', size=30, col=1)
p_7 = IH('p_7', 'not $80-25=55$', size=30, col=1)
p_8 = I('p_8', 'Wood loses $30\\%$, then $20\\%$ of what is left. What percent was lost in total?', size=30)
p_9 = IH('p_9', '$100-30=70$ left', size=30)
p_10 = IH('p_10', '$20\\%$ of $70=2\\cdot7=14$', size=30)
p_11 = IH('p_11', '$70-14=56$ left', size=30)
p_12 = IH('p_12', '$100-56=44$: $\\ $lost $44\\%$', size=30, col=1)
p_13 = IH('p_13', 'what stays: $\\ 80\\%$ of $70=8\\cdot7=56$', size=30, col=1)
p_14 = I('p_14', "Tal earns $60\\%$ more than Ben. Eli earns $45\\%$ less than Tal. By what percent is Eli's pay lower than Ben's?", size=30)
p_15 = I('p_15', 'The whole comes right after "of" / "than"', size=30)
p_16 = IH('p_16', 'Ben: $\\ 100$', size=30)
p_16b = IH('p_16b', 'Ben: $\\ 100$', size=30)
p_17 = IH('p_17', 'Tal: $\\ 100+60=160$', size=30)
p_18 = IH('p_18', 'Eli: $\\ 55\\%$ of $160$', size=30, col=1)
p_19a = IH('p_19a', '$10\\%$ of $160=16$', size=30, col=1)
p_19 = IH('p_19', '$50\\%$: $\\ 80,\\ \\ 5\\%$: $\\ 8$', size=30, col=1)
p_14c = I('p_14c', "Tal: $\\ 60\\%$ more than Ben. $\\ $Eli: $\\ 45\\%$ less than Tal. $\\ $Eli vs Ben?", size=28)
p_14b = I('p_14b', "Tal: $\\ 60\\%$ more than Ben. $\\ $Eli: $\\ 45\\%$ less than Tal. $\\ $Eli vs Ben?", size=28)
p_20 = IH('p_20', '$80+8=88$', size=30, col=1)
p_21 = IH('p_21', 'Ben $100$, Eli $88$: $\\ 12\\%$ lower', size=30, col=1)
p_22 = IH('p_22', '$100+20=120$', size=30)
p_23 = IH('p_23', '$20\\%$ of $120=24$', size=30)
p_24 = IH('p_24', '$120-24=96$: $\\ 4\\%$ lower', size=30)
p_25 = IH('p_25', '$100-20=80$', size=30, col=1)
p_26 = IH('p_26', '$20\\%$ of $80=16$', size=30, col=1)
p_27 = IH('p_27', '$80+16=96$ again', size=30, col=1)
p_27b = IH('p_27b', '$1.2\\cdot0.8=0.96$', size=30)
p_28 = I('p_28', 'Up $p\\%$, then down $p\\%$: $\\ $a loss of $\\dfrac{p^2}{100}\\%$', size=34, hand='Up p%, then down p%:  a loss of {p^2/100}%')
p_29 = IH('p_29', '$20^2=400$, $\\ 400\\div100=4$', size=30)
p_30 = IH('p_30', '$30^2=900$, $\\ 900\\div100=9$', size=30)
p_31 = IH('p_31', '$100\\to130\\to91$: $\\ 9\\%$ lower', size=30)
p_32 = I('p_32', 'Rise $10\\%$, then add a fixed $20$ credits', size=30)
p_33 = IH('p_33', '$100\\to110\\to130$: $\\ +30\\%$', size=30)
p_34 = IH('p_34', '$200\\to220\\to240$: $\\ +20\\%$', size=30)
p_35 = I('p_35', 'A fixed amount? $\\ $Use the real number, or a letter.', size=30)
# the change rule (R37: moved back from g059)
pc_1 = I('pc_1', 'change in $\\%=\\dfrac{\\text{change}}{\\text{original}}\\times100$', size=34, hand='change in % = {change/original}×100')
pc_2 = IH('pc_2', '$20\\to25$: $\\ $change $5$', size=30)
pc_3 = IH('pc_3', '$\\frac{5}{20}=\\frac{1}{4}=25\\%$ higher', size=30)
pc_4 = IH('pc_4', 'not $\\frac{5}{25}$: $\\ $the new price', size=30)
pc_5 = IH('pc_5', '$25\\to20$: $\\ $change $5$', size=30, col=1)
pc_6 = IH('pc_6', '$\\frac{5}{25}=\\frac{1}{5}=20\\%$ lower', size=30, col=1)
pc_7 = IH('pc_7', 'up $25\\%$, $\\ $down $20\\%$', size=30, col=1)
pc_8 = IH('pc_8', '$80\\to60$: $\\ \\frac{20}{80}=\\frac{1}{4}=25\\%$ lower', size=30, col=1)
# multipliers (R37: moved back from g060)
pm_1 = IH('pm_1', 'down $30\\%$: $\\ 70\\%$ stays, $\\ \\times0.7$', size=30)
pm_2 = IH('pm_2', '$200\\cdot0.7=140$', size=30)
pm_3 = IH('pm_3', 'up $40\\%$: $\\ 140\\%$, $\\ \\times1.4$', size=30, col=1)
pm_4 = IH('pm_4', '$50\\cdot1.4=70$', size=30, col=1)
pm_5 = IH('pm_5', 'up $15\\%$: $\\ \\times1.15$', size=30)
pm_6 = IH('pm_6', 'down $5\\%$: $\\ \\times0.95$', size=30, col=1)
pm_7 = IH('pm_7', 'wood: $\\ 0.7\\cdot0.8=0.56$', size=30)
pm_8 = IH('pm_8', '$56\\%$ stays, $\\ 44\\%$ lost', size=30)
pm_9 = IH('pm_9', 'up $50\\%$, then down $20\\%$', size=30, col=1)
pm_10 = IH('pm_10', '$1.5\\cdot0.8=1.2$', size=30, col=1)
pm_11 = IH('pm_11', '$120\\%$: $\\ 20\\%$ higher', size=30, col=1)
pm_12 = IH('pm_12', 'not $50-20=30$', size=30, col=1)
# working back from what is left (R37: moved back from g065)
pw_1 = I('pw_1', 'After a $20\\%$ discount, a shirt costs $96$ credits. What was the price before?', size=30)
pw_3 = IH('pw_3', '$80\\%$ of the start $=96$', size=30)
pw_4 = IH('pw_4', '$10\\%=96\\div8=12$', size=30, col=1)
pw_5 = IH('pw_5', '$100\\%=10\\cdot12=120$', size=30, col=1)
pw_6 = IH('pw_6', 'check: $\\ 120-24=96$', size=30, col=1)
pw_7 = IH('pw_7', 'not $96+20\\%$ of $96$', size=30)
pw_8 = I('pw_8', 'A pond loses $20\\%$ of its fish, then half of the rest. $40$ fish are left. How many were there at the start?', size=30)
pw_9 = IH('pw_9', '$0.8\\cdot0.5=0.4$', size=30)
pw_10 = IH('pw_10', '$40\\%$ of the start $=40$', size=30)
pw_11 = IH('pw_11', '$1\\%=1$, $\\ 100\\%=100$', size=30, col=1)
pw_12 = IH('pw_12', 'check: $\\ 100\\to80\\to40$', size=30, col=1)
# the arrow map (R37: moved back from g061)
pa_1 = AMAP('pa_1', ['Ben', 'Tal', 'Eli'], [('a', 0, 1, '×1.6'), ('b', 1, 2, '×0.55')], gap=250)
pa_2 = IH('pa_2', '$1.6\\cdot0.55$', size=30, col=1)
pa_3 = IH('pa_3', '$16\\cdot55=800+80=880$', size=30, col=1)
pa_4 = IH('pa_4', '$0.88$: $\\ 12\\%$ lower', size=30, col=1)
pa_5 = IH('pa_5', '$x$ is $25\\%$ more than $y$', size=30)
pa_6 = AMAP('pa_6', ['y', 'x'], [('a', 0, 1, '×1.25')], gap=260)
pa_7 = IH('pa_7', 'along the arrow: $\\ \\times$', size=30)
pa_7b = IH('pa_7b', 'against it: $\\ \\div$', size=30)
pa_8 = IH('pa_8', '$1.25=\\frac{5}{4}$', size=30, col=1)
pa_8b = IH('pa_8b', '$\\div\\frac{5}{4}=\\times\\frac{4}{5}=80\\%$', size=30, col=1)
pa_9 = IH('pa_9', '$20\\%$ less, $\\ $not $25\\%$', size=30, col=1)
pa_10 = IH('pa_10', '$20\\%$ more: $\\ \\times\\frac{5}{6}=83\\frac{1}{3}\\%$', size=30, col=1)
# the flip rule and "the same whole: keep" (R37: moved back from q-r26-t23-16)
pf_1 = IH('pf_1', '$50\\%$ of $10=5$', size=30)
pf_2 = IH('pf_2', '$10\\%$ of $50=5$', size=30)
pf_3 = IH('pf_3', '$20\\%$ of Dan $=30\\%$ of Gil', size=30)
pf_4 = IH('pf_4', 'Dan : Gil $=30:20=3:2$', size=30, col=1)
pf_5 = IH('pf_5', '$0.2D=0.3G$', size=30, col=1)
pf_6 = IH('pf_6', '$\\frac{D}{G}=\\frac{0.3}{0.2}=\\frac{3}{2}$', size=30, col=1)
pf_7 = IH('pf_7', '$D=150,\\ G=100$: $\\ 30=30$', size=30, col=1)
pf_8 = IH('pf_8', 'shirt $=40\\%$ of the coat', size=30)
pf_9 = IH('pf_9', 'shoes $=120\\%$ of the coat', size=30)
pf_10 = IH('pf_10', 'coat $100$: $\\ 40$ and $120$', size=30)
pf_11 = IH('pf_11', 'shoes : shirt $=120:40=3:1$', size=30, col=1)
pf_12 = IH('pf_12', 'the same part: $\\ $flip', size=30, col=1)
pf_13 = IH('pf_13', 'the same whole: $\\ $keep', size=30, col=1)
p_s1 = I('p_s1', 'Whole not given? $\\ $Plug in $100$.', size=30)
p_sc = I('p_sc', 'A change: $\\ $divide by the original', size=30)
p_s2 = I('p_s2', 'Changes in a row: $\\ $multiply the multipliers', size=30)
p_sw = I('p_sw', 'Know the end? $\\ $Go back to $100\\%$.', size=30)
p_s3 = I('p_s3', 'The whole comes after "of" / "than"', size=30)
p_sa = I('p_sa', 'Arrow map: $\\ $along $\\times$, $\\ $against $\\div$', size=30)
p_sf = I('p_sf', 'The same part: $\\ $flip. $\\ $The same whole: $\\ $keep.', size=30)
video('wp-053', 'lesson', slides=[
    S('Percent of a Percent',
      L("Welcome back. Percent questions on the exam come in two main types."),
      L("Type one is a straight calculation, like in the last lesson. Type two is a percent of a percent, changes one "
        "after the other, and comparisons. And in type two, the whole often isn't even given.")),
    # ---- part 1: the change rule, plug in a hundred
    S('The change in percent',
      L("But first, one rule we'll use all the time. By what percent did something go up, or down?"),
      L("Here's the rule. A change in percent is the change, divided by the original amount, times a hundred. The "
        "original is where we started, before the change.", show(pc_1, 'A change in percent is')),
      L("Let's see it in numbers. A ticket costs twenty credits, and then it costs twenty-five credits. The change is "
        "twenty-five minus twenty, five credits.", show(pc_2, 'The change is')),
      L("The original is twenty, so we divide by twenty. Five over twenty is a quarter, and a quarter is twenty-five "
        "percent. So the price went up by twenty-five percent.", show(pc_3, 'Five over twenty is a quarter')),
      L("Why the original? Because a percent is always a percent of something. Here we ask, five credits is what "
        "percent of the price we started with?"),
      L("And here's the trap. A lot of students divide by the new price, twenty-five, because it's the last number they "
        "see. Five over twenty-five is only twenty percent. That's the wrong whole.",
        show(pc_4, 'Five over twenty-five is only'))),
    S('Down is not the same',
      L("Now let's go the other way. The price falls from twenty-five credits back to twenty. The change is five "
        "credits again.", show(pc_5, 'The change is five credits again')),
      L("But now the original is twenty-five, the price before this change. Five over twenty-five is a fifth, so the "
        "price fell by twenty percent.", show(pc_6, 'Five over twenty-five is a fifth')),
      L("So the same five credits are twenty-five percent up, but only twenty percent down. Up, the whole is twenty. "
        "Down, the whole is twenty-five, a bigger whole.", show(pc_7, 'are twenty-five percent up')),
      L("One more, a class shrinks from eighty students to sixty. The change is twenty, and the original is eighty. "
        "Twenty over eighty is a quarter, so the class is twenty-five percent smaller.", show(pc_8, 'Twenty over eighty')),
      L("So when you see, by what percent did it rise, or fall, take the change, and divide by the amount before the "
        "change.")),
    S('Plug in a hundred',
      L("Now a percent of a percent. A price rises by eighty percent. Then it falls by twenty-five percent of the new "
        "price. What is the change in the price overall?", show(p_1, 'A price rises by eighty')),
      L("We don't know the price. From school, we'd call it x. But with a percent of a percent, x gets messy very fast."),
      L("Remember plugging in numbers from psychometric thinking? Here we plug in a hundred. Any number would work, but a "
        "hundred is the easiest to calculate with."),
      L("So the price is a hundred credits. It rises by eighty percent. Eighty percent of a hundred is eighty, so the "
        "price is a hundred eighty.", show(p_2, 'So the price is a hundred'), show(p_3, 'so the price is a hundred eighty')),
      L("Now careful. The twenty-five percent is of the new price, a hundred eighty. The hundred is not our whole anymore."),
      L("Twenty-five percent is a quarter. A quarter of a hundred eighty is forty-five. So the price falls to a hundred "
        "eighty minus forty-five, a hundred thirty-five.", show(p_4, 'A quarter of a hundred eighty'),
        show(p_5, 'So the price falls')),
      L("We started at a hundred and ended at a hundred thirty-five. The change is thirty-five, and the original is a "
        "hundred. Thirty-five over a hundred is thirty-five percent, so the price rose by thirty-five percent.",
        show(p_6, 'Thirty-five over a hundred')),
      L("Not eighty minus twenty-five, fifty-five. Why? Because the second percent is taken from a bigger amount.",
        show(p_7, 'Not eighty minus')),
      L("And here's why a hundred is so nice. The original is a hundred, so the change at the end is already the answer "
        "in percent.")),
    S('Two losses',
      L("Here's another example. A pile of wood loses thirty percent. Then it loses twenty percent of what is left. What percent "
        "was lost in total?", show(p_8, 'A pile of wood loses')),
      L("Again we plug in a hundred. So we start with a hundred units of wood. It loses thirty percent, thirty units, so "
        "seventy units are left.", show(p_9, 'so seventy units are left')),
      L("Now twenty percent of what is left. That's twenty percent of seventy, not of a hundred. Ten percent of seventy is "
        "seven, so twenty percent is fourteen.", show(p_10, 'Ten percent of seventy')),
      L("Seventy minus fourteen is fifty-six. So fifty-six units are left.", show(p_11, 'Seventy minus fourteen')),
      L("From a hundred down to fifty-six, we lost forty-four. So forty-four percent was lost in total, not fifty.",
        show(p_12, 'From a hundred down to fifty-six')),
      L("There's a quicker way. Think about what stays. Lose thirty percent, and seventy percent stays. Lose twenty "
        "percent of that, and eighty percent of it stays. Eighty percent of seventy is eight times seven, fifty-six.",
        show(p_13, 'Eighty percent of seventy is'))),
    S('When a hundred fails',
      L("One warning. Plugging in a hundred works when everything in the story is a percent."),
      L("Here's an example where it doesn't. A price rises by ten percent, and then a fixed twenty credits are added. By "
        "what percent did it rise?", show(p_32, 'a fixed twenty credits')),
      L("Start from a hundred. Ten percent more is a hundred ten, and plus twenty is a hundred thirty. That's thirty "
        "percent.", show(p_33, 'Start from a hundred')),
      L("Now start from two hundred. Ten percent more is two hundred twenty, and plus twenty is two hundred forty. The "
        "change is forty, and forty out of two hundred is twenty percent.", show(p_34, 'Now start from two hundred')),
      L("Different starting prices give different answers. So when the story adds a fixed amount, don't plug in a "
        "hundred. Use the number they gave you, or a letter.", show(p_35, 'when the story adds a fixed amount'))),
    # ---- part 2: multipliers, working back
    S('Multipliers',
      L("In the wood question, we looked at what stays. That idea has a name, multipliers. A multiplier is the number we multiply by to make a change in "
        "one step."),
      L("Let's start with a drop. A price goes down thirty percent. What stays? A hundred minus thirty, seventy percent. "
        "Seventy percent is zero point seven. So going down thirty percent is multiplying by zero point seven.",
        show(pm_1, 'So going down thirty percent')),
      L("Let's check it on a price of two hundred. Two hundred times zero point seven is a hundred forty. The long way, "
        "thirty percent of two hundred is sixty, and two hundred minus sixty is a hundred forty. It's the same.",
        show(pm_2, 'Two hundred times zero point seven')),
      L("Now let's take a rise. A price goes up forty percent. We keep the whole price, a hundred percent, and add forty percent. "
        "That's a hundred forty percent, so we multiply by one point four.", show(pm_3, "That's a hundred forty percent")),
      L("On fifty credits, fifty times one point four is seventy. Let's check. Forty percent of fifty is twenty, and "
        "fifty plus twenty is seventy.", show(pm_4, 'fifty times one point four')),
      L("So going up p percent means times the bracket, a hundred plus p, percent. Going down p percent means times the "
        "bracket, a hundred minus p, percent. Up "
        "fifteen percent is times one point one five. Down five percent is times zero point nine five.",
        show(pm_5, 'Up fifteen percent is'), show(pm_6, 'Down five percent is'))),
    S('Two changes: multiply',
      L("And here's the strength of multipliers. When there are two changes in a row, we multiply the two multipliers."),
      L("Think back to the wood. It lost thirty percent, so times zero point seven. Then it lost twenty percent of what "
        "was left, so times zero point eight. Seven times eight is fifty-six, so it's zero point five six.",
        show(pm_7, 'Seven times eight is fifty-six')),
      L("Zero point five six is fifty-six percent. So fifty-six percent stays, and forty-four percent is lost. The same "
        "answer as before, in one line.", show(pm_8, 'So fifty-six percent stays')),
      L("One more. A price goes up fifty percent, and then down twenty percent. Up fifty percent is times one point "
        "five. Down twenty percent is times zero point eight.", show(pm_9, 'A price goes up fifty')),
      L("One point five times zero point eight. Fifteen times eight is a hundred twenty, so it's one point two.",
        show(pm_10, 'Fifteen times eight')),
      L("Times one point two is a hundred twenty percent of the start. So the price is twenty percent higher. Not fifty "
        "minus twenty, thirty percent.", show(pm_11, 'So the price is twenty percent higher'), show(pm_12, 'Not fifty')),
      L("So when you see changes one after the other, write a multiplier for each change, and multiply them.")),
    S('Up and down',
      L("Here's a trap the exam loves. A price goes up twenty percent, and then down twenty percent. Is it back where it "
        "started?"),
      L("Let's plug in a hundred. Up twenty percent is a hundred twenty.", show(p_22, 'Up twenty percent is')),
      L("Now down twenty percent of a hundred twenty. Ten percent of a hundred twenty is twelve, so twenty percent is "
        "twenty-four.", show(p_23, 'so twenty percent is twenty-four')),
      L("A hundred twenty minus twenty-four is ninety-six. So we end four percent lower than the start. We're not back "
        "where we started.", show(p_24, 'A hundred twenty minus twenty-four')),
      L("With multipliers, it's one point two times zero point eight. Twelve times eight is ninety-six, so it's zero "
        "point nine six, four percent lower again.", show(p_27b, 'Twelve times eight')),
      L("Why? Because the twenty percent down is taken from a bigger amount, a hundred twenty. So it takes away more than "
        "it added."),
      L("And if it goes down first, and then up? A hundred down twenty percent is eighty. Twenty percent of eighty is "
        "sixteen, and eighty plus sixteen is ninety-six again. The same result, in any order.",
        show(p_25, 'A hundred down twenty percent'), show(p_26, 'Twenty percent of eighty'), show(p_27, 'and eighty plus sixteen'))),
    S('Up and down: the rule',
      L("There's even a rule for it. Up p percent, and then down p percent, always loses p squared over a hundred percent.",
        show(p_28, 'always loses p squared')),
      L("Twenty squared is four hundred. Four hundred over a hundred is four. That's our four percent.",
        show(p_29, 'Twenty squared is four hundred')),
      L("Let's check the rule once more, with thirty percent. Thirty squared is nine hundred. Over a hundred, that's "
        "nine. So up thirty and down thirty should lose nine percent.", show(p_30, 'Thirty squared is nine hundred')),
      L("With a hundred, up thirty percent is a hundred thirty. Thirty percent of a hundred thirty is thirty-nine. A "
        "hundred thirty minus thirty-nine is ninety-one, nine percent lower. It works.",
        show(p_31, 'A hundred thirty minus thirty-nine'))),
    S('Working back',
      L("Sometimes we know the end, and they ask about the start. After a twenty percent discount, a shirt costs "
        "ninety-six credits. What was the price before?", show(pw_1, 'After a twenty percent discount')),
      L("The start is our whole, a hundred percent. A twenty percent discount leaves eighty percent. So eighty percent of "
        "the start is ninety-six credits.", show(pw_3, 'So eighty percent of')),
      L("Now we go back to a hundred percent, through ten percent. Eighty percent is eight times ten percent. So ten "
        "percent is ninety-six divided by eight, twelve.", show(pw_4, 'So ten percent is')),
      L("A hundred percent is ten times ten percent. Ten times twelve is a hundred twenty credits.",
        show(pw_5, 'Ten times twelve')),
      L("Let's check. Twenty percent of a hundred twenty is twenty-four. A hundred twenty minus twenty-four is "
        "ninety-six. It works.", show(pw_6, 'A hundred twenty minus twenty-four')),
      L("Here's the trap. A lot of students take ninety-six and add twenty percent of ninety-six. But the twenty percent "
        "was taken from the old price, a hundred twenty, not from ninety-six. So that adds back too little.",
        show(pw_7, 'add twenty percent of ninety-six'))),
    S('Working back: two changes',
      L("It works the same with two changes. A pond loses twenty percent of its fish. Then it loses half of the fish "
        "that are left. Forty fish are left. How many fish were there at the start?", show(pw_8, 'A pond loses')),
      L("Losing twenty percent is times zero point eight. Losing half is times zero point five. Eight times five is "
        "forty, so it's zero point four.", show(pw_9, 'Eight times five is forty')),
      L("Zero point four is forty percent. So forty percent of the start is left, and that's forty fish.",
        show(pw_10, 'So forty percent of the start')),
      L("Forty percent is forty fish, so one percent is one fish. A hundred percent is a hundred fish.",
        show(pw_11, 'so one percent is one fish')),
      L("Let's check. A hundred fish lose twenty percent, so eighty are left. Half of eighty is forty. It works.",
        show(pw_12, 'Half of eighty is forty')),
      L("So when you know what is left, and they ask about the start, write what percent of the start is left. Then go "
        "back to a hundred percent.")),
    # ---- part 3: who is the hundred, the arrow map
    S('Who is the hundred?',
      L("Now, where do we put the hundred? Here's a question with three people.", show(p_14, 'three people')),
      L("Here's the rule. The words of and than point at the whole. The whole is whatever comes right after them.",
        show(p_15, 'The whole is whatever')),
      L("For example, thirty percent of the students. The students come after of, so the students are the whole. Or, Tal "
        "earns sixty percent more than Ben. Ben comes after than, so Ben is the whole in that sentence."),
      L("But this question has three thans. Tal than Ben, Eli than Tal, and Eli than Ben. So who gets the hundred?"),
      L("The one that decides is the than in the question itself, lower than Ben's. So Ben gets the hundred.",
        pt('p_14', 'lower than Ben'), show(p_16, 'So Ben gets the hundred'))),
    S('Who is the hundred?',
      L("Ben earns a hundred. Tal earns sixty percent more than Ben, so Tal earns a hundred sixty.",
        show(p_14b, 'Ben earns a hundred'), show(p_16b, 'Ben earns a hundred'), show(p_17, 'so Tal earns')),
      L("Eli earns forty-five percent less than Tal. A hundred minus forty-five is fifty-five. So fifty-five percent of Tal's pay stays.", show(p_18, 'So fifty-five percent')),
      L("Ten percent of a hundred sixty is sixteen. So fifty percent is eighty, and five percent is eight. Eighty plus "
        "eight is eighty-eight.", show(p_19a, 'Ten percent of a hundred sixty'), show(p_19, 'So fifty percent is eighty'), show(p_20, 'Eighty plus eight')),
      L("Eli earns eighty-eight, and Ben earns a hundred. So Eli's pay is twelve percent lower than Ben's. Not fifteen "
        "percent, which is sixty minus forty-five.", show(p_21, "So Eli's pay is twelve"))),
    S('The arrow map',
      L("For chains like this there's also a picture, the arrow map. Each sentence becomes one arrow. The arrow starts "
        "at the whole, and the multiplier is written on it.", show(p_14c, 'For chains like this'),
        show(pa_1['line'], 'the arrow map')),
      L("Tal earns sixty percent more than Ben. Ben comes after than, so the arrow starts at Ben and goes to Tal. Sixty "
        "percent more is a hundred sixty percent, so we write times one point six.", show(pa_1['a'], 'so the arrow starts at Ben')),
      L("Eli earns forty-five percent less than Tal. So the next arrow goes from Tal to Eli. Forty-five percent less "
        "leaves fifty-five percent, so it's times zero point five five.", show(pa_1['b'], 'So the next arrow goes')),
      L("The question compares Eli with Ben, so we walk from Ben to Eli. Both arrows point our way, so we multiply, one "
        "point six times zero point five five.", show(pa_2, 'so we multiply')),
      L("Sixteen times fifty is eight hundred, and sixteen times five is eighty. So sixteen times fifty-five is eight "
        "hundred eighty, and the product is zero point eight eight.", show(pa_3, 'Sixteen times fifty is'),
        show(pa_4, 'and the product is')),
      L("Zero point eight eight is eighty-eight percent of Ben's pay. So it's twelve percent lower, the same answer as "
        "before.")),
    S('Against the arrow',
      L("Now the most common trap with these chains. x is twenty-five percent more than y. What percent of x is y?",
        show(pa_5, 'x is twenty-five percent more')),
      L("The whole is y, the word after than. So the arrow goes from y to x, times one point two five.",
        show(pa_6['line'], 'The whole is y'), show(pa_6['a'], 'So the arrow goes from y')),
      L("Along the arrow, we multiply. Against the arrow, we divide. We want y, so we go from x back to y, against the "
        "arrow. So we divide by one point two five.", show(pa_7, 'Along the arrow, we multiply'),
        show(pa_7b, 'Against the arrow, we divide')),
      L("One point two five is five quarters. Dividing by five quarters is multiplying by four fifths. And four fifths "
        "is eighty percent.", show(pa_8, 'One point two five is five quarters'), show(pa_8b, 'Dividing by five quarters')),
      L("So y is eighty percent of x. That's twenty percent less, not twenty-five percent. Why? Because the twenty-five "
        "percent was of y. Now the whole is x, a bigger whole.", show(pa_9, "That's twenty percent less")),
      L("Let's check with numbers. y is a hundred, so x is a hundred twenty-five. A hundred over a hundred twenty-five is "
        "four fifths, eighty percent. It works."),
      L("With twenty percent more, it's the same idea. One point two is six fifths, so against the arrow we multiply by "
        "five sixths. Five sixths is eighty-three and a third percent. Many students say eighty percent, but that's the "
        "trap.", show(pa_10, 'With twenty percent more'))),
    # ---- part 4: the same part or the same whole
    S('The same part: flip',
      L("Now two different wholes with the same part. Fifty percent of ten is five. And ten percent of fifty is also "
        "five.", show(pf_1, 'Fifty percent of ten is five'), show(pf_2, 'ten percent of fifty is also')),
      L("To give the same amount, the bigger percent needs a smaller whole, and the smaller percent needs a bigger "
        "whole. Fifty percent goes with ten, and ten percent goes with fifty."),
      L("Here's an exam case. Twenty percent of Dan's savings is equal to thirty percent of Gil's savings. Who has more, "
        "and what is the ratio?", show(pf_3, "Twenty percent of Dan's savings")),
      L("Here's the rule. When the same part is a percent of two different wholes, the ratio of the wholes is the "
        "percents, flipped. So Dan to Gil is thirty to twenty, three to two. Dan has more.", show(pf_4, 'So Dan to Gil is')),
      L("Why does it flip? Let's write it as an equation. Call Dan's savings D, and Gil's savings G. So zero point two D "
        "is equal to zero point three G.", show(pf_5, 'So zero point two D')),
      L("We divide both sides by G, and by zero point two, so that D over G is alone. D over G is zero point three over "
        "zero point two, three halves. That's the percents, flipped.", show(pf_6, 'D over G is zero point three')),
      L("Let's check with numbers. Dan has a hundred fifty, and Gil has a hundred. Twenty percent of a hundred fifty is "
        "thirty, and thirty percent of a hundred is thirty. They're equal.", show(pf_7, 'Dan has a hundred fifty')),
      L("The trap is to keep the order, twenty to thirty. That gives Gil more, but the bigger percent goes with the "
        "smaller whole. And one warning. The flip works only when the two amounts are equal. If one amount is ten more "
        "than the other, we write the equation.")),
    S('The same whole: keep',
      L("Now let's see the opposite case. A shirt costs forty percent of the price of a coat. Shoes cost a hundred twenty percent "
        "of the price of the coat. How do the shoes compare with the shirt?", show(pf_8, 'A shirt costs forty'),
        show(pf_9, 'Shoes cost a hundred twenty')),
      L("Here the shared thing is the whole, the coat. So there's no flip. The bigger percent gives the bigger amount."),
      L("Let's plug in a hundred for the coat. Then the shirt costs forty, and the shoes cost a hundred twenty.",
        show(pf_10, "Let's plug in a hundred for the coat")),
      L("So shoes to shirt is a hundred twenty to forty, three to one. The shoes cost three times as much as the shirt.",
        show(pf_11, 'So shoes to shirt is')),
      L("So when you see two percents, ask what is shared. The same part, flip the percents. The same whole, keep them.",
        show(pf_12, 'The same part, flip'), show(pf_13, 'The same whole, keep'))),
    S('Summary',
      L("Let's sum up. When the whole isn't given, plug in a hundred. A change in percent is divided by the original.",
        show(p_s1, 'When the whole'), show(p_sc, 'A change in percent')),
      L("Each new percent is taken from the new amount, so for changes in a row, we multiply the multipliers. And when "
        "we know the end, we go back to a hundred percent.", show(p_s2, 'Each new percent'), show(p_sw, 'And when')),
      L("The whole comes after of or than. On the arrow map, along the arrow we multiply, against it we divide.",
        show(p_s3, 'The whole comes after'), show(p_sa, 'On the arrow map')),
      L("And ask what is shared. The same part, flip. The same whole, keep. [pause] Next we'll see a survey question and "
        "the percent tree, and I'll see you in the next video.", show(p_sf, 'And ask what is shared'))),
])
SPLIT053 = ('wp-053', 'Percent of a Percent', [
    (1, None),
    (6, "Let's continue with percent of a percent, and learn a fast tool, multipliers."),
    (10, "Let's continue with percent of a percent. Now we go back from the end to the start, and compare people."),
    (16, "Let's continue with percent of a percent. Now two percents that share something.")])

# ------------------------------------------------------------------------------------------------ wp23-g054 (Hebrew: the smokers' survey)
# Hebrew (wp 3266-3402): who is the 100? the survey; 60 don't smoke, the rest 40, 30% of THEM (of 40), 12, the rest 28
# (or 70% of 40); write the numbers on the question itself in the exam; then the percent tree (more visual, longer):
# each branch down is the new 100% (the common mistake 10%; the branches always add up to 100%); a leaf = the product
# along the path (70% of 40% = 28%). REMINDER: plug in 100 (wp-053). NEW: the percent tree, writing on the question.
s_1 = IH('s_1', 'all students: $\\ 100$', size=30)
s_2 = IH('s_2', '$35\\%$ of $100=35$ do not play', size=30)
s_3 = IH('s_3', '$100-35=65$ play', size=30)
s_4 = IH('s_4', '$10\\%$ of $65=6.5$', size=30, col=1)
s_5 = IH('s_5', '$8\\cdot6=48,\\ \\ 8\\cdot0.5=4$', size=30, col=1)
s_6 = IH('s_6', '$48+4=52$ piano', size=30, col=1)
s_7 = IH('s_7', '$65-52=13$ guitar only', size=30)
s_8 = IH('s_8', '$13$ out of $100=13\\%$', size=30)
s_9 = IH('s_9', 'or: $\\ 20\\%$ of $65=65\\div5=13$', size=30, col=1)
s_tr = PTREE('s_tr', ('all', '100%'), [('do not play', '35%'), ('play', '65%')], (1, [('piano', '80%'), ('guitar only', '20%')]), w=640)
s_10 = IH('s_10', '$20\\%$ of the players, $\\ $not of all', size=30, col=1)
s_11 = IH('s_11', '$20\\%$ of $65\\%=13\\%$', size=32, col=1)
video('solve-wp23-g054', 'solution', qid='wp23-g054', slides=[
    S('Method 1 · Plugging in numbers',
      L("In a survey, thirty-five percent of the students do not play a musical instrument. Of the students who play an "
        "instrument, eighty percent play the piano and the rest play only the guitar. What percentage of all the surveyed "
        "students play only the guitar?", pt('stem', 'In a survey', 'hl', 12.0), voice='calm', pause=0.5),
      L("So they ask about all the surveyed students, not only the players. It's a percent of a percent, and no number of "
        "students is given. We'll solve it in two different ways, by plugging in numbers, and then with a percent tree.",
        pt('stem', 'all the surveyed students')),
      L("Let's start by plugging in numbers. The whole here is all the students in the survey. So let's say a hundred "
        "students took part.", show(s_1, 'So let\'s say a hundred')),
      L("Thirty-five percent don't play an instrument. Thirty-five percent of a hundred is thirty-five students. So a "
        "hundred minus thirty-five, sixty-five students play.", show(s_2, 'Thirty-five percent of a hundred'),
        show(s_3, 'So a hundred minus thirty-five')),
      L("Now, eighty percent of whom? The question says, of the students who play an instrument. So it's eighty percent "
        "of the sixty-five players, not of the hundred.", pt('stem', 'The question says')),
      L("Ten percent of sixty-five is six and a half. Eighty percent is eight times that. Eight times six is forty-eight, "
        "and eight halves are four. So forty-eight plus four, fifty-two players play the piano.",
        show(s_4, 'Ten percent of sixty-five'), show(s_5, 'Eight times six'), show(s_6, 'So forty-eight plus four'))),
    S('Method 1 · Plugging in numbers',
      L("The rest play only the guitar. Sixty-five minus fifty-two is thirteen students.", show(s_7, 'Sixty-five minus fifty-two')),
      L("We started with a hundred students. So thirteen students are thirteen percent. Choice number three is our "
        "answer.", show(s_8, 'So thirteen students are'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Here's a quicker way to the same thirteen. Eighty percent play the piano, so twenty percent play only the "
        "guitar. Twenty percent is a fifth, and a fifth of sixty-five is thirteen.", show(s_9, 'and a fifth of sixty-five')),
      L("And here's a habit for the exam. Write these numbers right next to the words of the question. A hundred, "
        "thirty-five, sixty-five. Then you see the whole story at once.", pt('stem', 'Write these numbers'))),
    S('Method 2 · The math way: the percent tree',
      L("[pause] Now the same question with a percent tree. We start again from the givens. At the root of the tree, all "
        "the students, a hundred percent.", show(s_tr['line'], 'At the root of the tree')),
      L("The survey splits in two. Thirty-five percent don't play, and the rest, sixty-five percent, play. The two "
        "branches add up to a hundred percent.", show(s_tr['b1'], 'The survey splits in two')),
      L("Now the players split again, into piano and guitar only. And here's the classic mistake. When we go down a "
        "branch, that group becomes the new hundred percent."),
      L("So now the players are a hundred percent. Eighty percent play the piano, and twenty percent play only the "
        "guitar. Again the branches add up to a hundred.", show(s_tr['b2'], 'So now the players are')),
      L("Many students see twenty percent and stop there. That's choice number one. But it's twenty percent of the "
        "players, not of everyone. Eighty percent on the piano wouldn't even fit inside the sixty-five percent who play.",
        show(s_10, "But it's twenty percent of the players"), mk('cross', 'choice 1', "That's choice number one")),
      L("To get a branch at the bottom, we multiply the percents along its path. Twenty percent of sixty-five percent. A "
        "fifth of sixty-five is thirteen, so it's thirteen percent.", show(s_11, 'A fifth of sixty-five')),
      L("We get the same thirteen percent. Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp23-g058 (Hebrew: a share drops 85%)
# Hebrew (wp 3511-3575): the calculation (10% chunks: 85% of 820 = 656 + 41 = 697, then subtract), then the complement:
# 15% is left, "often easier to find the complementary percent". NEW: the complement (what is left).
c_1 = IH('c_1', '$10\\%$ of $680=68$', size=30)
c_2 = IH('c_2', '$75\\%=70\\%+5\\%$', size=30)
c_3 = IH('c_3', '$7\\cdot60=420,\\ \\ 7\\cdot8=56$', size=30)
c_4 = IH('c_4', '$70\\%$: $\\ 420+56=476$', size=30)
c_5 = IH('c_5', '$5\\%$: $\\ 68\\div2=34$', size=30, col=1)
c_6 = IH('c_6', 'drop: $\\ 476+34=510$', size=30, col=1)
c_7 = IH('c_7', '$680-510=170$', size=30, col=1)
c_8 = IH('c_8', '$100\\%-75\\%=25\\%$ left', size=30)
c_9 = IH('c_9', '$25\\%=\\frac{1}{4}$', size=30)
c_10 = IH('c_10', '$680\\div2=340$', size=30)
c_11 = IH('c_11', '$340\\div2=170$', size=30)
video('solve-wp23-g058', 'solution', qid='wp23-g058', slides=[
    S('Method 1 · The math way: the drop first',
      L("A winter coat originally costs six hundred eighty credits. In a clearance sale, its price is reduced by "
        "seventy-five percent. What is the new price?", pt('stem', 'A winter coat', 'hl', 7.0), voice='calm', pause=0.5),
      L("So they ask for the new price, the price after the sale. We'll solve it in two different ways. First we'll find "
        "the drop, and then we'll use what's left.", pt('stem', 'the new price')),
      L("Let's start with the math way. The price drops by seventy-five percent of six hundred eighty. Let's use ten "
        "percent chunks. Ten percent of six hundred eighty is sixty-eight.", show(c_1, 'Ten percent of six hundred eighty')),
      L("Seventy-five percent is seventy percent plus five percent. Seventy percent is seven times sixty-eight. Seven "
        "times sixty is four hundred twenty. Seven times eight is fifty-six. So that's four hundred seventy-six.",
        show(c_2, 'Seventy-five percent is seventy'), show(c_3, 'Seven times sixty'), show(c_4, "So that's four hundred")),
      L("Five percent is half of ten percent. Half of sixty-eight is thirty-four.", show(c_5, 'Half of sixty-eight')),
      L("So the drop is four hundred seventy-six plus thirty-four, five hundred ten credits.", show(c_6, 'So the drop is')),
      L("Careful here. Five hundred ten is choice number one, but it's the drop, not the new price. They ask for the "
        "price after the drop.", mk('cross', 'choice 1', 'but it\'s the drop')),
      L("So the new price is six hundred eighty minus five hundred ten, a hundred seventy. Choice number two is our "
        "answer.", show(c_7, 'So the new price is'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S("Method 2 · The math way: what's left",
      L("[pause] Now a shorter way. We start again from the givens. The whole price is a hundred percent. It drops by "
        "seventy-five percent, so twenty-five percent is left.", show(c_8, 'so twenty-five percent is left')),
      L("Twenty-five percent is a quarter. So the new price is a quarter of six hundred eighty.",
        show(c_9, 'Twenty-five percent is a quarter')),
      L("To find a quarter, we halve twice. Half of six hundred eighty is three hundred forty. Half of three hundred forty "
        "is a hundred seventy.", show(c_10, 'Half of six hundred eighty'), show(c_11, 'Half of three hundred forty')),
      L("The same hundred seventy, with much less work. So when a price drops, think about what stays. Choice number two "
        "is our answer, and I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp23-g057 (Hebrew: a diver used 82.5% of his oxygen)
# Hebrew (wp 3415-3509): what is left (17.5%), the choices are fractions: over 100, expand by 2, reduce by 5; then the
# insight from the choices (1/20 = 5%, so 7/20 = 35%, and 7/40 is half of it). REMINDER: percent <-> fraction, the
# fraction table (camera lesson). NEW here: the choices built in a family; the "used" trap.
f_1 = IH('f_1', '$100-57.5=42.5\\%$ left', size=30)
f_2 = IH('f_2', '$\\frac{42.5}{100}$', size=32)
f_3 = IH('f_3', '$=\\frac{85}{200}$', size=32)
f_4 = IH('f_4', '$85\\div5=17,\\ \\ 200\\div5=40$', size=30, col=1)
f_5 = IH('f_5', '$=\\frac{17}{40}$', size=32, col=1)
f_6 = IH('f_6', '(3) $\\frac{17}{20}=17\\cdot5\\%=85\\%$', size=30)
f_7 = IH('f_7', '(2) $\\frac{17}{40}$ $=$ half of $85\\%=42.5\\%$', size=30)
f_8 = IH('f_8', '(1) $\\frac{23}{40}=1-\\frac{17}{40}$: $\\ $the used ink', size=30)
video('solve-wp23-g057', 'solution', qid='wp23-g057', slides=[
    S('Method 1 · The math way',
      L("A printer cartridge has used fifty-seven point five percent of its ink. What fraction of the ink remains?",
        pt('stem', 'A printer cartridge', 'hl', 5.0), voice='calm', pause=0.5),
      L("So they ask what's left, and the choices are fractions, not percents. We'll solve it in two different ways, the "
        "math way, and then with an insight from the choices.", pt('stem', "So they ask what's left")),
      L("Let's start with the math way. The whole cartridge is a hundred percent. Fifty-seven point five percent was used. "
        "So a hundred minus fifty-seven point five, forty-two point five percent is left.", show(f_1, 'So a hundred minus')),
      L("A lot of students turn the fifty-seven point five itself into a fraction. But that's the ink that was used. We "
        "want what's left."),
      L("Now we turn the percent into a fraction. We write it over a hundred, forty-two point five over a hundred.",
        show(f_2, 'forty-two point five over a hundred')),
      L("A decimal point inside a fraction isn't nice. So we multiply the top and the bottom by two. Forty-two point five "
        "times two is eighty-five. A hundred times two is two hundred.", show(f_3, 'Forty-two point five times two')),
      L("Now we reduce. Eighty-five and two hundred both divide by five. Eighty-five divided by five is seventeen. Two "
        "hundred divided by five is forty.", show(f_4, 'Eighty-five divided by five')),
      L("So it's seventeen over forty. Choice number two is our answer.", show(f_5, "So it's seventeen over forty"),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Insight: the choices',
      L("[pause] Now the insight. These choices are not random. We start again from the givens. Fifty-seven point five "
        "percent was used, so forty-two point five percent is left."),
      L("Look at choice number three, seventeen over twenty. Many students know that a twentieth is five percent. So "
        "seventeen twentieths is seventeen times five, eighty-five percent. That's not forty-two point five, so it's out.",
        show(f_6, 'seventeen times five'), mk('cross', 'choice 3', "so it's out")),
      L("But look at choice number two, seventeen over forty. Its bottom is twice as big, so it's exactly half of "
        "seventeen over twenty. Half of eighty-five percent is forty-two point five percent. That's exactly what's left.",
        show(f_7, 'Half of eighty-five percent'), mk('tick', 'choice 2', "That's exactly what's left")),
      L("And choice number one, twenty-three over forty? Twenty-three is forty minus seventeen. So it's the rest of the "
        "cartridge, the fifty-seven point five percent that was used. That's the trap.",
        show(f_8, 'Twenty-three is forty minus seventeen'), mk('cross', 'choice 1', "That's the trap")),
      L("The exam often builds the choices like this, so a student who looks at them carefully gets there fast. Choice "
        "number two is our answer, and I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ wp23-g059 (Hebrew: 40 -> 44 -> 48)
# Hebrew (wp 3577-3630): 4 of 40 is a tenth; 4 of 44 is 1/11; the cake for 10 or 11 children; or: 10% more than 44 is
# 48.4, so less than 10%; the same jump in money, but the whole grew. REMINDER: the change rule (R37: taught in wp-053
# part 1 with its examples and the "divide by the new price" trap); this is its first question, applied step by step.
g_1 = I('g_1', 'change in $\\%=\\dfrac{\\text{change}}{\\text{original}}\\times100$', size=34, hand='change in % = {change/original}×100')
g_4 = IH('g_4', '$40\\to50$: $\\ \\frac{10}{40}=\\frac{1}{4}=25\\%$', size=30)
g_5 = IH('g_5', '$50\\to60$: $\\ \\frac{10}{50}=\\frac{1}{5}=20\\%$', size=30)
g_6 = IH('g_6', '$\\frac{1}{5}<\\frac{1}{4}$', size=32, col=1)
g_7 = IH('g_7', '$25\\%$ of $50=12.5$', size=30)
g_8 = IH('g_8', '$50+12.5=62.5$', size=30)
g_9 = IH('g_9', '$60<62.5$: $\\ $less than $25\\%$', size=30)
video('solve-wp23-g059', 'solution', qid='wp23-g059', slides=[
    S('Method 1 · The math way: the change rule',
      L("The price of a cinema ticket rises from forty credits to fifty credits, and later to sixty credits. How do the "
        "two percentage increases compare?", pt('stem', 'The price of a cinema ticket', 'hl', 7.0), voice='calm', pause=0.5),
      L("Both rises are ten credits. So many students think the percents are equal too. We'll solve it in two different "
        "ways, the math way with the change rule, and then by understanding.", pt('stem', 'Both rises are ten')),
      L("Let's start with the math way. Like in the lesson, a change in percent is the change, divided by the original "
        "amount, times a hundred. The original is the price before the change.", show(g_1, 'a change in percent is')),
      L("The first rise is from forty to fifty. The change is fifty minus forty, ten credits. The original is forty, the "
        "price before this rise. So we divide by forty, not by the new price, fifty.", pt('stem', 'The first rise is from forty')),
      L("Ten over forty is a quarter, twenty-five percent. So the first rise is twenty-five percent.",
        show(g_4, 'Ten over forty is a quarter'))),
    S('Method 1 · The math way: the change rule',
      L("The second rise is from fifty to sixty. The change is ten again. But now the original is fifty, the price before "
        "this rise. Ten over fifty is a fifth, twenty percent.", show(g_5, 'Ten over fifty is a fifth')),
      L("Which is bigger, a quarter or a fifth? Think of one cake. Shared by four children, or by five children? With five "
        "children, each one gets less. The same top with a bigger bottom gives a smaller fraction.",
        show(g_6, 'The same top with a bigger bottom')),
      L("So the first percentage increase is larger. Choice number three is our answer.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Understanding',
      L("[pause] Now by understanding. We start again from the givens. The first rise, from forty to fifty, is "
        "twenty-five percent, because ten is a quarter of forty."),
      L("What if the second rise were also twenty-five percent? Twenty-five percent of fifty is twelve and a half. So the "
        "price would reach fifty plus twelve and a half, sixty-two and a half.", show(g_7, 'Twenty-five percent of fifty'),
        show(g_8, 'fifty plus twelve and a half')),
      L("But the price only reached sixty. That's less than sixty-two and a half. So the second rise is less than "
        "twenty-five percent.", show(g_9, 'But the price only reached sixty')),
      L("So the same amount of money is a smaller percent when the whole is bigger. Choice number three is our answer, "
        "and I'll see you in the next question.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp23-g060 (Hebrew: Delilah and Samson)
# Hebrew (wp 3632-3797): the calculation with x ("a percent can't stand alone, it always needs a whole"; x minus 30% of
# x is the complement 70% of x; plus 40% OF THAT = 140% of what was left; 98% of x, 2% less); then plug in 100 into the
# whole (after "of"), 70, 40% of 70 = 28, 98; with 200 too (196, 4 of 200 = 2%); why 100: two reasons. NEW: a percent
# never stands alone. REMINDER: plug in 100, multipliers (R37: taught in wp-053 part 2; this is their first question,
# applied step by step with "like in the lesson").
n_1 = IH('n_1', 'start: $\\ x$', size=30)
n_2 = IH('n_2', '$x-30\\%$ of $x$', size=30)
n_3 = IH('n_3', '$100\\%-30\\%=70\\%$', size=30, col=1)
n_4 = IH('n_4', '$70\\%$ of $x=0.7x$', size=30, col=1)
n_5 = IH('n_5', '$100\\%+40\\%=140\\%$: $\\ \\times1.4$', size=30)
n_6 = IH('n_6', '$1.4\\cdot0.7x$', size=30)
n_7 = IH('n_7', '$14\\cdot7=98$: $\\ 0.98x$', size=30)
n_8 = IH('n_8', '$98\\%$ of $x$: $\\ 2\\%$ fewer', size=30, col=1)
n_9 = IH('n_9', 'down $30\\%$: $\\ \\times0.7$', size=30, col=1)
n_9b = IH('n_9b', 'up $40\\%$: $\\ \\times1.4$', size=30, col=1)
n_10 = IH('n_10', 'start: $\\ 100$', size=30)
n_11 = IH('n_11', '$100-30=70$', size=30)
n_12 = IH('n_12', '$40\\%$ of $70=4\\cdot7=28$', size=30)
n_13 = IH('n_13', '$70+28=98$: $\\ 2\\%$ fewer', size=30)
n_14 = IH('n_14', '$200-60=140$', size=30)
n_15 = IH('n_15', '$40\\%$ of $140=56$', size=30)
n_16 = IH('n_16', '$140+56=196$', size=30)
n_17 = IH('n_17', '$\\frac{4}{200}=\\frac{2}{100}=2\\%$', size=30, col=1)
video('solve-wp23-g060', 'solution', qid='wp23-g060', slides=[
    S('Method 1 · The math way: multipliers',
      L("In a computer game, Noa loses thirty percent of her coins. She then wins a prize equal to forty percent of the "
        "coins she has left. Compared with the number of coins she had at the start, how many coins does she have now?",
        pt('stem', 'In a computer game', 'hl', 11.0), voice='calm', pause=0.5),
      L("She loses some coins, and then wins some back. So does she end up with more or fewer? We'll solve it in two "
        "different ways, the math way with algebra, and then by plugging in numbers.", pt('stem', 'She loses some coins')),
      L("Let's start with the math way. We don't know how many coins she had, so let's call it x.",
        show(n_1, "so let's call it x")),
      L("She loses thirty percent of her coins. Careful here. A lot of students write x minus thirty over a hundred. But "
        "a percent can't stand alone. It's always a percent of something, and here it's thirty percent of x.",
        show(n_2, "here it's thirty percent of x")),
      L("So she has x minus thirty percent of x. The whole x is a hundred percent of x. A hundred percent minus thirty "
        "percent leaves seventy percent.", show(n_3, 'A hundred percent minus thirty')),
      L("Seventy percent is zero point seven. Like in the lesson, that's the multiplier for going down thirty percent. So "
        "she has zero point seven x.", show(n_4, 'So she has zero point seven'))),
    S('Method 1 · The math way: multipliers',
      L("Now she wins forty percent of the coins she has left. Forty percent of what? Of zero point seven x, not of x.",
        pt('stem', 'of the coins she has left')),
      L("She keeps all the coins she has, a hundred percent, and gets forty percent more. A hundred plus forty is a "
        "hundred forty percent of what she had. So we multiply by one point four.", show(n_5, 'A hundred plus forty is')),
      L("One point four times zero point seven x. Fourteen times seven is ninety-eight, so it's zero point nine eight x.",
        show(n_6, 'One point four times zero point seven'), show(n_7, 'Fourteen times seven')),
      L("Zero point nine eight x is ninety-eight percent of x. She started with a hundred percent of x, so now she has two "
        "percent fewer. Choice number two is our answer.", show(n_8, 'ninety-eight percent of x'),
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("So, just like in the lesson, each change is one multiplier. To go down thirty percent, we multiply by zero point "
        "seven, what stays. To go up forty percent, we multiply by one point four. And for two changes in a row, we "
        "multiply the multipliers.", show(n_9, 'To go down thirty percent'), show(n_9b, 'To go up forty percent'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. No number of coins is given, so we plug in a "
        "hundred. Where? Into the whole, the coins she had at the start.", show(n_10, 'Into the whole')),
      L("She loses thirty percent of a hundred, thirty coins. So seventy coins are left.", show(n_11, 'So seventy coins')),
      L("The prize is forty percent of the coins she has left, of seventy. It's not forty coins. Ten percent of seventy is "
        "seven, so forty percent is four times seven, twenty-eight.", show(n_12, 'so forty percent is four times')),
      L("Seventy plus twenty-eight is ninety-eight coins. That's two fewer than a hundred, so two percent fewer.",
        show(n_13, 'Seventy plus twenty-eight')),
      L("The trap is choice number three, ten percent more. That's forty minus thirty. But the forty percent is taken "
        "from a smaller amount, seventy.", mk('cross', 'choice 3', 'The trap is choice number three'))),
    S('Method 2 · Plugging in numbers',
      L("Would another number work? Let's try two hundred coins. Thirty percent of two hundred is sixty, so a hundred "
        "forty are left.", show(n_14, 'so a hundred forty are left')),
      L("Forty percent of a hundred forty is fifty-six. Ten percent is fourteen, and four times fourteen is fifty-six. A "
        "hundred forty plus fifty-six is a hundred ninety-six.", show(n_15, 'Forty percent of a hundred forty'),
        show(n_16, 'A hundred forty plus fifty-six')),
      L("That's four fewer, out of two hundred. Four over two hundred is two over a hundred, two percent again.",
        show(n_17, 'Four over two hundred')),
      L("So any number works. We pick a hundred for two reasons. The number we get is already the percent. And percents "
        "of a hundred are the easiest to find. Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t23-01 (added: +25% then -12%)
# English addition (real exam: 2021_spring_q1_13, 2024_autumn_q1_03, 2026_spring_q2_07). REMINDER: multipliers (wp-053
# part 2, g060), plug in 100 (wp-053). NEW here (a one-off trick, R37: stays in this question): the two-changes formula
# p + q + pq/100 (checked on +20 / -20 from the lesson).
a_1 = IH('a_1', '$+25\\%$: $\\ 125\\%=\\times1.25$', size=30)
a_2 = IH('a_2', '$-12\\%$: $\\ 88\\%=\\times0.88$', size=30)
a_3 = IH('a_3', '$1.25\\cdot0.88$', size=30)
a_4 = IH('a_4', '$1\\cdot0.88=0.88$', size=30, col=1)
a_5 = IH('a_5', '$0.88\\div4=0.22$', size=30, col=1)
a_6 = IH('a_6', '$0.88+0.22=1.1$', size=30, col=1)
a_7 = IH('a_7', '$\\times1.1=110\\%$: $\\ 10\\%$ higher', size=30, col=1)
a_8 = IH('a_8', 'start: $\\ 100$', size=30)
a_9 = IH('a_9', '$100+25=125$', size=30)
a_10 = IH('a_10', '$10\\%$ of $125=12.5$', size=30)
a_11 = IH('a_11', '$2\\%$ of $125=2.5$', size=30, col=1)
a_12 = IH('a_12', '$12\\%$: $\\ 12.5+2.5=15$', size=30, col=1)
a_13 = IH('a_13', '$125-15=110$', size=30, col=1)
a_14 = IH('a_14', 'two changes $p\\%$, $q\\%$: $\\quad p+q+\\frac{pq}{100}$', size=30)
a_15 = IH('a_15', '$20+(-20)=0$', size=30)
a_16 = IH('a_16', '$20\\cdot(-20)\\div100=-4$', size=30)
a_17 = IH('a_17', '$25-12=13$', size=30, col=1)
a_18 = IH('a_18', '$25\\cdot(-12)\\div100=-3$', size=30, col=1)
a_19 = IH('a_19', '$13-3=10$', size=30, col=1)
video('solve-q-r26-t23-01', 'solution', qid='q-r26-t23-01', slides=[
    S('Method 1 · The math way: multipliers',
      L("A price rises by twenty-five percent. Later, the new price falls by twelve percent. By what percent is the final "
        "price higher than the original price?", pt('stem', 'A price rises by', 'hl', 7.0), voice='calm', pause=0.5),
      L("Two changes, one after the other. A lot of students just do twenty-five minus twelve, and get thirteen percent. "
        "That's choice number one. But the twelve percent is taken from the new, bigger price.",
        pt('stem', 'taken from the new'), mk('cross', 'choice 1', "That's choice number one")),
      L("We'll solve it in three different ways, with multipliers, by plugging in numbers, and with a short formula."),
      L("Let's start with the math way, with multipliers. Going up twenty-five percent means we keep a hundred percent "
        "and add twenty-five percent. That's a hundred twenty-five percent, so times one point two five.",
        show(a_1, "That's a hundred twenty-five percent")),
      L("Going down twelve percent means eighty-eight percent stays. So it's times zero point eight eight.",
        show(a_2, 'eighty-eight percent stays')),
      L("Two changes in a row, so we multiply the two multipliers. One point two five times zero point eight eight.",
        show(a_3, 'One point two five times'))),
    S('Method 1 · The math way: multipliers',
      L("Here's an easy way to do it. One point two five is one plus a quarter. One times zero point eight eight is zero "
        "point eight eight. And a quarter of zero point eight eight is zero point two two.",
        show(a_4, 'One times zero point eight eight'), show(a_5, 'And a quarter of zero point')),
      L("Zero point eight eight plus zero point two two is one point one.", show(a_6, 'plus zero point two two')),
      L("Times one point one means a hundred ten percent of the original price. So the final price is ten percent higher. "
        "Choice number four is our answer.", show(a_7, 'Times one point one means'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. No price is given, so the original price is a "
        "hundred.", show(a_8, 'so the original price is')),
      L("It rises by twenty-five percent, so it's a hundred twenty-five.", show(a_9, "so it's a hundred twenty-five")),
      L("Now it falls by twelve percent of a hundred twenty-five. Ten percent of a hundred twenty-five is twelve and a "
        "half.", show(a_10, 'Ten percent of a hundred twenty-five')),
      L("One percent is a tenth of that, one and a quarter. So two percent is two and a half. Twelve and a half plus two "
        "and a half is fifteen.", show(a_11, 'So two percent is'), show(a_12, 'Twelve and a half plus')),
      L("A hundred twenty-five minus fifteen is a hundred ten. That's ten percent higher than a hundred. That's choice number "
        "four again.", show(a_13, 'A hundred twenty-five minus fifteen'), mk('tick', 'choice 4', 'choice number four again'))),
    S('Method 3 · The math way: the shortcut formula',
      L("[pause] And there's a short formula for two changes in a row. Call the two changes p and q, in percent. A fall "
        "is a minus number."),
      L("The total change is p plus q, plus p times q over a hundred.", show(a_14, 'The total change is')),
      L("Let's check it on numbers we know. Up twenty, then down twenty. Twenty plus minus twenty is zero. Twenty times "
        "minus twenty is minus four hundred. Over a hundred, that's minus four. So it's four percent lower, just like "
        "in the lesson.", show(a_15, 'Twenty plus minus twenty'), show(a_16, 'Twenty times minus twenty')),
      L("Now our question. p is twenty-five and q is minus twelve. Twenty-five minus twelve is thirteen.",
        show(a_17, 'Twenty-five minus twelve')),
      L("Twenty-five times twelve is three hundred, so p times q is minus three hundred. Over a hundred, that's minus "
        "three. Thirteen minus three is ten.", show(a_18, 'so p times q is'), show(a_19, 'Thirteen minus three')),
      L("Ten percent higher, the same answer. The extra part, p times q over a hundred, is exactly what students forget "
        "when they just add the percents. Choice number four is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])


# ------------------------------------------------------------------------------------------------ wp23-g061 (Hebrew: Maya, Asaf, Yehonatan)
# Hebrew (wp 3799-3890): plug in 100 into the whole (after "than": Asaf), +25% -> 125, -20% of Maya -> 100, ratio 1;
# then the insight: +1/4 then -1/5 are "consecutive" unit fractions (+1/2 -1/3: three halves, take one away; +1/3 -1/4:
# four thirds, take one away), always back to the whole. REMINDER: plug in 100, who is the hundred, the arrow map (R37:
# all taught in wp-053, the arrow map with "against the arrow" and the 83 1/3%-not-80% trap; this is its first question,
# applied step by step). NEW here: the consecutive-fractions insight (two warm-ups, then ours).
d_1 = IH('d_1', 'Omer: $\\ 100$', size=30)
d_2 = IH('d_2', 'Dana: $\\ 100+50=150$', size=30)
d_3 = IH('d_3', '$33\\frac{1}{3}\\%=\\frac{1}{3}$', size=30)
d_4 = IH('d_4', '$\\frac{1}{3}$ of $150=50$', size=30, col=1)
d_5 = IH('d_5', 'Lior: $\\ 150-50=100$', size=30, col=1)
d_6 = IH('d_6', '$100\\div100=1$', size=30, col=1)
d_7 = IH('d_7', '$+\\frac{1}{2}$, then $-\\frac{1}{3}$', size=30)
d_8 = IH('d_8', '$6$ sixths $+1$ sixth $=7$ sixths', size=30)
d_9 = IH('d_9', '$\\frac{1}{7}$ of $7$ sixths $=1$ sixth', size=30)
d_10 = IH('d_10', '$7-1=6$ sixths: $\\ $back', size=30)
d_11 = IH('d_11', '$5$ fifths $+1=6$ fifths, $\\ -1=5$ fifths', size=30, col=1)
d_12 = IH('d_12', '$2$ halves $+1=3$ halves, $\\ -1=2$ halves', size=30, col=1)
d_13 = IH('d_13', 'add $\\frac{1}{n}$, then take away $\\frac{1}{n+1}$: $\\ $back', size=30, col=1)
d_14 = IH('d_14', 'along the arrows: $\\ \\times$', size=30, col=1)
d_m2 = AMAP('d_m2', ['Omer', 'Dana', 'Lior'], [('a', 0, 1, '×1.5'), ('b', 1, 2, '×2/3')], gap=250)
d_18a = IH('d_18a', '$1.5=\\frac{3}{2}$', size=30)
d_18 = IH('d_18', '$\\frac{3}{2}\\cdot\\frac{2}{3}=1$', size=30)
video('solve-wp23-g061', 'solution', qid='wp23-g061', slides=[
    S('Method 1 · Plugging in numbers',
      L("Dana earns fifty percent more than Omer. Lior earns thirty-three and a third percent less than Dana. What is "
        "Lior's wage divided by Omer's wage?", pt('stem', 'Dana earns fifty percent', 'hl', 7.0), voice='calm', pause=0.5),
      L("So they ask for Lior's wage divided by Omer's wage, and no wages are given. We'll solve it in three different "
        "ways, by plugging in numbers, with an insight, and with an arrow map.", pt('stem', "So they ask for Lior's wage")),
      L("Let's start by plugging in numbers, with a hundred. But into whom? Remember, the whole comes after than. Dana "
        "earns more than Omer, so Omer is the whole. Omer gets the hundred.", show(d_1, 'Omer gets the hundred')),
      L("Dana earns fifty percent more than Omer. Fifty percent of a hundred is fifty, so Dana earns a hundred fifty.",
        show(d_2, 'so Dana earns a hundred fifty')),
      L("Lior earns thirty-three and a third percent less than Dana. From our fraction table, thirty-three and a third "
        "percent is a third. A third of a hundred fifty is fifty.", show(d_3, 'From our fraction table'),
        show(d_4, 'A third of a hundred fifty')),
      L("So Lior earns a hundred fifty minus fifty, a hundred. Lior divided by Omer is a hundred divided by a hundred, "
        "one. Choice number one is our answer.", show(d_5, 'So Lior earns'), show(d_6, 'Lior divided by Omer'),
        mk('tick', 'choice 1', 'Choice number one is our answer')),
      L("The trap is choice number three, seven sixths. It comes from fifty percent minus thirty-three and a third "
        "percent, sixteen and two thirds percent more. But the third is taken from Dana's wage, which is bigger.",
        mk('cross', 'choice 3', 'The trap is choice number three'))),
    S('Method 2 · Insight',
      L("[pause] Now the insight. We added fifty percent, took away thirty-three and a third percent, and came back to "
        "the start. Is that luck? No. Fifty percent is a half, and thirty-three and a third percent is a third.",
        show(d_7, 'Fifty percent is a half')),
      L("Let's see it on other fractions first. A whole is six sixths. Add a sixth, and we have seven sixths.",
        show(d_8, 'Add a sixth, and we have')),
      L("Now take away a seventh. A seventh of seven sixths is one sixth. Seven sixths minus one sixth is six sixths, the "
        "whole again.", show(d_9, 'A seventh of seven sixths'), show(d_10, 'Seven sixths minus one sixth')),
      L("Here's another one. A whole is five fifths. Add a fifth, and we have six fifths. Take away a sixth, one of the six "
        "fifths, and we're back to five fifths.", show(d_11, 'A whole is five fifths')),
      L("Now our question. A whole is two halves. Add a half, and we have three halves. Take away a third, one of the "
        "three halves, and we're back to two halves.", show(d_12, 'A whole is two halves')),
      L("So adding one over n, and then taking away one over n plus one, always brings us back. Lior earns exactly what "
        "Omer earns. Choice number one is our answer.", show(d_13, 'So adding one over n'),
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
    S('Method 3 · The math way: the arrow map',
      L("[pause] Now a third way, the arrow map, like in the lesson. Each sentence becomes one arrow. The arrow starts at "
        "the whole, the word after than, and its multiplier is written on it."),
      L("We start again from the givens. Dana earns fifty percent more than Omer. The whole is Omer, so the arrow goes "
        "from Omer to Dana. Fifty percent more is a hundred fifty percent, so it's times one point five.",
        show(d_m2['line'], 'Dana earns fifty percent more'), show(d_m2['a'], 'so the arrow goes from Omer')),
      L("Lior earns thirty-three and a third percent less than Dana. So the arrow goes from Dana to Lior. A third less "
        "leaves two thirds, so it's times two thirds.", show(d_m2['b'], 'So the arrow goes from Dana')),
      L("We want Lior divided by Omer, so we walk from Omer to Lior. Along an arrow we multiply, and both arrows point "
        "our way. So we multiply both multipliers.", show(d_14, 'Along an arrow we multiply')),
      L("One point five is three halves, and three halves times two thirds is one.", show(d_18a, 'One point five is three halves'),
        show(d_18, 'and three halves times two thirds')),
      L("So Lior's wage is one times Omer's wage. Choice number one is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])


# ------------------------------------------------------------------------------------------------ wp23-g062 (Hebrew: 25% of 50% of x is 6)
# Hebrew (wp 3892-4007): "of" is times, so it's all one multiplication: 1/4 * 1/2 * x = 6, x = 48, 3/8 of 48 = 18;
# then the insight: 73% of 84 = 84% of 73 (one multiplication, the order doesn't matter), so 25% of 50% = half of 25%
# = 12.5%; 37.5 is 3 times 12.5, so 3 * 6. REMINDER: of = times, the fraction table. NEW here (a one-off trick, R37:
# stays in this question): a% of b = b% of a (two examples, new numbers), a percent of a percent is one multiplication.
e_1 = IH('e_1', '$25\\%=\\frac{1}{4}$', size=30)
e_2 = IH('e_2', '$18\\%=\\frac{18}{100}=\\frac{9}{50}$', size=30)
e_3 = IH('e_3', '$\\frac{1}{4}\\cdot\\frac{9}{50}\\cdot y=9$', size=30)
e_4 = IH('e_4', '$\\frac{9}{200}y=9$', size=30, col=1)
e_5 = IH('e_5', '$y=200$', size=30, col=1)
e_6 = IH('e_6', '$10\\%$ of $200=20$', size=30, col=1)
e_7 = IH('e_7', '$3\\%=6,\\ \\ 0.5\\%=1$', size=30, col=1)
e_8 = IH('e_8', '$20+6+1=27$', size=30, col=1)
e_9 = IH('e_9', '$32\\%$ of $50=\\frac{32\\cdot50}{100}$', size=30)
e_10 = IH('e_10', '$50\\%$ of $32=\\frac{50\\cdot32}{100}$', size=30)
e_11 = IH('e_11', 'half of $32=16$', size=30)
e_12 = IH('e_12', '$x\\%$ of $y=y\\%$ of $x$', size=32)
e_13 = IH('e_13', '$4\\%$ of $75=75\\%$ of $4=3$', size=30)
e_14 = IH('e_14', '$\\frac{1}{4}$ of $18\\%=4.5\\%$', size=30, col=1)
e_15 = IH('e_15', '$4.5\\%$ of $y=9$', size=30, col=1)
e_16 = IH('e_16', '$13.5=3\\cdot4.5$', size=30, col=1)
e_17 = IH('e_17', '$3\\cdot9=27$', size=30, col=1)
video('solve-wp23-g062', 'solution', qid='wp23-g062', slides=[
    S('Method 1 · The math way',
      L("Twenty-five percent of eighteen percent of y is equal to nine. What is thirteen point five percent of y?",
        pt('stem', 'of eighteen percent', 'hl', 6.0), voice='calm', pause=0.5),
      L("The wording is a bit heavy. But of means times, so the whole left side is one multiplication. We'll solve it in "
        "two different ways, the math way, and then with an insight.", pt('stem', 'The wording is a bit heavy')),
      L("Let's start with the math way. Twenty-five percent is a quarter. Eighteen percent is eighteen over a hundred, "
        "which reduces to nine over fifty.", show(e_1, 'Twenty-five percent is a quarter'), show(e_2, 'Eighteen percent is')),
      L("So a quarter, times nine over fifty, times y, is equal to nine.", show(e_3, 'So a quarter, times nine')),
      L("A quarter times nine over fifty is nine over two hundred. So nine two hundredths of y is nine.",
        show(e_4, 'So nine two hundredths')),
      L("Nine two hundredths of y is nine, so one two hundredth of y is one. So y is two hundred.", show(e_5, 'So y is two hundred')),
      L("Now what they ask, thirteen point five percent of two hundred. Ten percent of two hundred is twenty. Three "
        "percent is six. And half a percent is one.", show(e_6, 'Ten percent of two hundred'), show(e_7, 'Three percent is six')),
      L("Twenty plus six plus one is twenty-seven. Choice number two is our answer.", show(e_8, 'Twenty plus six plus one'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Insight: swap the order',
      L("[pause] Now the insight. Let's start with a question. Which is bigger, thirty-two percent of fifty, or fifty percent of "
        "thirty-two?"),
      L("Thirty-two percent of fifty is thirty-two times fifty, over a hundred. Fifty percent of thirty-two is fifty "
        "times thirty-two, over a hundred.", show(e_9, 'Thirty-two percent of fifty is'), show(e_10, 'Fifty percent of thirty-two is')),
      L("In a multiplication the order doesn't matter, so they're equal. And fifty percent of thirty-two is easy. It's "
        "half of thirty-two, sixteen.", show(e_11, "It's half of thirty-two")),
      L("So x percent of y is equal to y percent of x. We can swap them when it makes the calculation easier.",
        show(e_12, 'So x percent of y')),
      L("Here's another one. Four percent of seventy-five looks hard. But seventy-five percent of four is three quarters of four, "
        "three.", show(e_13, 'three quarters of four'))),
    S('Method 2 · Insight: swap the order',
      L("Now our question. We start again from the givens. Twenty-five percent of eighteen percent is one multiplication, "
        "so we can read it in the easy order. A quarter of eighteen percent is four point five percent.",
        show(e_14, 'A quarter of eighteen percent')),
      L("So four point five percent of y is nine.", show(e_15, 'So four point five percent of y')),
      L("They ask for thirteen point five percent. Thirteen point five is three times four point five. So it's three "
        "times nine, twenty-seven.", show(e_16, 'Thirteen point five is three times'), show(e_17, 'So it\'s three times nine')),
      L("We never even found y. Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp23-g063 (Hebrew: not equal to 20% of 2x)
# Hebrew (wp 4009-4146): the calculation; all choices are over 100, so don't reduce, compare the tops; then the ratios
# insight: 20% of 100 = 10% of 200 (double the whole, halve the percent) -> balanced choices, and the one where both
# grow. REMINDER: percent = over 100. NEW here: "the whole times k, the percent divided by k" (an inverse ratio).
h_1 = IH('h_1', '$16\\%$ of $5y=\\frac{16\\cdot5y}{100}=\\frac{80y}{100}$', size=30)
h_2 = IH('h_2', '(1) $\\ 40\\cdot2y=80y$', size=30)
h_3 = IH('h_3', '(2) $\\ 8\\cdot10y=80y$', size=30)
h_4 = IH('h_4', '(3) $\\ 32\\cdot5y=160y$', size=30, col=1)
h_5 = IH('h_5', '(4) $\\ 20\\cdot4y=80y$', size=30, col=1)
h_6 = IH('h_6', '$y>0$: $\\ 160y\\ne80y$', size=30, col=1)
h_7 = IH('h_7', '$30\\%$ of $100=30$', size=30)
h_8 = IH('h_8', '$15\\%$ of $200=30$', size=30)
h_9 = IH('h_9', 'whole $\\times k$, $\\ $percent $\\div k$', size=30)
h_9b = IH('h_9b', 'the same amount', size=30)
h_10 = IH('h_10', '(1) $\\ 16\\cdot2.5=40$', size=30, col=1)
h_10b = IH('h_10b', '$5y\\div2.5=2y$', size=30, col=1)
h_11 = IH('h_11', '(2) $\\ $percent $\\div2$, $\\ $whole $\\times2$', size=30, col=1)
h_12 = IH('h_12', '(3) $\\ $percent $\\times2$, $\\ $whole the same', size=30, col=1)
h_13 = IH('h_13', '(4) $\\ 20\\cdot4=80=16\\cdot5$', size=30, col=1)
video('solve-wp23-g063', 'solution', qid='wp23-g063', slides=[
    S('Method 1 · The math way: compare the tops',
      L("For y bigger than zero, which expression is not equal to sixteen percent of five y?",
        pt('stem', 'For y bigger than zero', 'hl', 5.0), voice='calm', pause=0.5),
      L("So three of the choices are equal to sixteen percent of five y, and one isn't. We'll solve it in two different "
        "ways, the math way, and then by understanding.", pt('stem', 'and one isn')),
      L("Let's start with the math way. Sixteen percent of five y is sixteen over a hundred, times five y. Sixteen times "
        "five is eighty, so it's eighty y over a hundred.", show(h_1, 'Sixteen times five is eighty')),
      L("Every choice is also some number over a hundred. So we don't need to reduce. We just compare the tops."),
      L("Choice number one says, forty percent of two y. Forty times two y is eighty y. That's equal, so it's out.",
        show(h_2, 'Forty times two y'), mk('cross', 'choice 1', "so it's out")),
      L("Choice number two says, eight percent of ten y. Eight times ten y is eighty y. Equal again, so it's out.",
        show(h_3, 'Eight times ten y'), mk('cross', 'choice 2', 'Equal again')),
      L("Choice number three says, thirty-two percent of five y. Thirty-two times five y is a hundred sixty y. That's not "
        "eighty y.", show(h_4, 'Thirty-two times five y')),
      L("In the exam you'd circle it and move on. Here, let's check the last one too. Choice number four says, twenty "
        "percent of four y. Twenty times four y is eighty y. Equal, so it's out.", show(h_5, 'Twenty times four y'),
        mk('cross', 'choice 4', 'Equal, so it')),
      L("y is positive, so a hundred sixty y can't be equal to eighty y. Choice number three is our answer.",
        show(h_6, 'y is positive'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Understanding: percent and whole',
      L("[pause] Now by understanding. Let's see the idea on easy numbers first. Thirty percent of a hundred is thirty.",
        show(h_7, 'Thirty percent of a hundred')),
      L("Now let's double the whole to two hundred, and still get thirty. Which percent do we need? Fifteen percent of two "
        "hundred is thirty. So we doubled the whole, and we halved the percent.", show(h_8, 'Fifteen percent of two hundred')),
      L("That makes sense. A bigger whole needs a smaller percent to give the same amount. So when the whole is "
        "multiplied by some number, the percent must be divided by the same number.", show(h_9, 'So when the whole is'), show(h_9b, 'divided by the same number')),
      L("Now let's check the choices. We start again from the givens, sixteen percent of five y. Choice number one says forty "
        "percent of two y. Forty is sixteen times two and a half. And two y is five y divided by two and a half. So it's "
        "balanced, and it's equal. Out.", show(h_10, 'Forty is sixteen times'), show(h_10b, 'And two y is five y'), mk('cross', 'choice 1', "balanced, and it's equal")),
      L("Choice number two says eight percent of ten y. The percent is halved, and the whole is doubled. Balanced, out.",
        show(h_11, 'The percent is halved'), mk('cross', 'choice 2', 'Balanced, out')),
      L("Choice number three says thirty-two percent of five y. The percent is doubled, but the whole stays five y. "
        "Nothing balances it, so the amount doubles. It's not equal.", show(h_12, 'The percent is doubled')),
      L("And in choice number four, twenty times four is eighty, the same as sixteen times five. So that one is balanced "
        "too. Choice number three is our answer, and I'll see you in the next question.",
        show(h_13, 'twenty times four is eighty'), mk('cross', 'choice 4', 'balanced'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t23-16 (added: the flip rule)
# English addition (real exam: 2020_autumn_q1_06, 2024_autumn_q2_08, 2019_winter_q2_18; same whole: 2019_spring_q2_12).
# REMINDER (R37: taught in wp-053 part 4 with the warm-up, the why, the limit and "the same whole: keep"): the flip rule,
# here its first question, applied step by step. Methods: the math way (the flip rule), plugging in the answers (300
# first, then 240). REMINDER: ratio parts (22).
l_3 = IH('l_3', 'the same part: $\\ $flip the percents', size=30, col=1)
l_4 = IH('l_4', 'novels : textbooks $=30:45$', size=30, col=1)
l_7 = IH('l_7', '$30:45=2:3$', size=30)
l_8 = IH('l_8', '$2+3=5$ parts, $\\ 600\\div5=120$', size=30)
l_9 = IH('l_9', 'novels: $\\ 2\\cdot120=240$', size=30)
l_10 = IH('l_10', '$45:30$, no flip: $\\ 360$', size=30, col=1)
l_11 = IH('l_11', '(3) $\\ N=300,\\ T=300$', size=30)
l_12 = IH('l_12', '$45\\%$ of $300=135$', size=30)
l_13 = IH('l_13', '$30\\%$ of $300=90$', size=30)
l_14 = IH('l_14', 'fewer novels: $\\ 240$ or $180$', size=30, col=1)
l_15 = IH('l_15', '(2) $\\ N=240,\\ T=600-240=360$', size=30, col=1)
l_16 = IH('l_16', '$45\\%$ of $240=96+12=108$', size=30, col=1)
l_17 = IH('l_17', '$30\\%$ of $360=3\\cdot36=108$', size=30, col=1)
video('solve-q-r26-t23-16', 'solution', qid='q-r26-t23-16', slides=[
    S('Method 1 · The math way: the flip rule',
      L("A library has only novels and textbooks, six hundred books in all. Forty-five percent of the novels is the same "
        "number of books as thirty percent of the textbooks. How many novels does the library have?",
        pt('stem', 'A library has only novels', 'hl', 10.0), voice='calm', pause=0.5),
      L("So one amount of books is forty-five percent of one pile, and thirty percent of the other pile. One part, two "
        "different wholes. We'll solve it in two different ways, with the flip rule, and then by plugging in the answers.",
        pt('stem', 'One part, two')),
      L("Let's start with the math way. Like in the lesson, the same part is a percent of two different wholes. So the "
        "ratio of the wholes is the percents, flipped.", show(l_3, 'So the ratio of the wholes')),
      L("The bigger percent goes with the smaller pile. Thirty percent is the smaller percent, so the textbooks are the "
        "bigger pile. Novels to textbooks is thirty to forty-five.", show(l_4, 'Novels to textbooks is')),
      L("Thirty and forty-five both divide by fifteen. So the ratio is two to three.", show(l_7, 'So the ratio is two to three')),
      L("Two plus three is five parts, and the five parts are six hundred books. So one part is six hundred divided by "
        "five, a hundred twenty.", show(l_8, 'Two plus three is five parts')),
      L("The novels are two parts. Two times a hundred twenty is two hundred forty. Choice number two is our answer.",
        show(l_9, 'Two times a hundred twenty'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Choice number one, three hundred sixty, is the trap. It's the ratio forty-five to thirty, with no flip. That "
        "gives the novels the bigger pile. But the bigger percent belongs to the smaller pile.",
        show(l_10, 'with no flip'), mk('cross', 'choice 1', 'is the trap'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. We start again from the givens. Six hundred books in all, and the two "
        "amounts must be equal."),
      L("Which choice first? Let's take three hundred, choice number three, because percents of three hundred are easy. "
        "N, the novels, is three hundred. So T, the textbooks, is six hundred minus three hundred, three hundred.",
        show(l_11, 'So T, the textbooks')),
      L("Forty-five percent of three hundred is a hundred thirty-five. Thirty percent of three hundred is ninety. Not "
        "equal, so choice number three is out.", show(l_12, 'Forty-five percent of three hundred'),
        show(l_13, 'Thirty percent of three hundred'), mk('cross', 'choice 3', 'so choice number three is out')),
      L("Forty-five percent of the novels gave more books. To make them equal, we need fewer novels and more textbooks. So the answer is less "
        "than three hundred, two hundred forty or a hundred eighty. Choice number one is out too.",
        show(l_14, 'So the answer is less'), mk('cross', 'choice 1', 'Choice number one is out too')),
      L("Let's try two hundred forty. Then the textbooks are six hundred minus two hundred forty, three hundred sixty.",
        show(l_15, "Let's try two hundred forty")),
      L("Forty-five percent of two hundred forty. Ten percent is twenty-four, so forty percent is ninety-six. Five percent "
        "is twelve. Ninety-six plus twelve is a hundred eight.", show(l_16, 'Ninety-six plus twelve')),
      L("Thirty percent of three hundred sixty is three times thirty-six, a hundred eight. Equal, so it works.",
        show(l_17, 'three times thirty-six')),
      L("So, like in the lesson, ask what is shared. Here it's the same part, so we flip the percents. Choice number two "
        "is our answer, and I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp23-g064 (Hebrew: Dudi's oranges, 85% / 15%)
# Hebrew (wp 4148-4228): the difference is the key (85 - 15 = 70% is 14), the ratio table / triangle value (15 * 14 /
# 70 = 3); shortcuts: drop a zero, or a middle step through 10% (70% -> 10% is / 7, then x 1.5). REMINDER: the ratio
# table and the triangle value (22, camera lesson). NEW here: the difference as a percent; a middle step through 10%.
b_1 = IH('b_1', 'factory: $\\ 100\\%-70\\%=30\\%$', size=30)
b_2 = IH('b_2', 'difference: $\\ 70\\%-30\\%=40\\%$', size=30)
b_3 = IH('b_3', '$40\\%=48$ kg', size=30)
b_t = TBL('b_t', ['Percent', 'Kilograms'], ['', ''], [
    ('r1', [('c', 0, 0, '40%'), ('c', 0, 1, '48')]), ('r2', [('c', 1, 0, '30%'), ('q', 1, 1)]),
    ('dg', [('diag', (1, 0), (0, 1))]), ('ans', [('cover', 1, 1, '36')])], col=0, colw=200, w=460)
b_4 = IH('b_4', '$?=\\frac{30\\cdot48}{40}$', size=30, col=1)
b_5 = IH('b_5', '$=\\frac{3\\cdot48}{4}$', size=30, col=1)
b_6 = IH('b_6', '$48\\div4=12,\\ \\ 3\\cdot12=36$', size=30, col=1)
b_7 = IH('b_7', '$40\\%=48$', size=30)
b_8 = IH('b_8', '$10\\%=48\\div4=12$', size=30)
b_9 = IH('b_9', '$30\\%=3\\cdot12=36$', size=30)
video('solve-wp23-g064', 'solution', qid='wp23-g064', slides=[
    S('Method 1 · The math way: the triangle value',
      L("A farmer sells seventy percent of his apples at a market and all the rest to a juice factory. The market gets "
        "forty-eight kilograms more apples than the factory. How many kilograms of apples does the factory get?",
        pt('stem', 'A farmer sells seventy', 'hl', 10.0), voice='calm', pause=0.5),
      L("The key here is the difference. They don't give us the factory's amount. They give the difference between the "
        "two. We'll solve it in two different ways, with the ratio table, and then with ten percent.",
        pt('stem', 'They give the difference')),
      L("Let's start with the math way. All the apples are a hundred percent. The market gets seventy percent, so the "
        "factory gets the rest, a hundred minus seventy, thirty percent.", show(b_1, 'so the factory gets the rest')),
      L("So the difference is seventy minus thirty, forty percent.", show(b_2, 'So the difference is')),
      L("And the question says this difference is forty-eight kilograms. So forty percent is forty-eight kilograms. "
        "Careful, forty-eight is the difference, not the factory's apples. That's choice number three, a trap.",
        show(b_3, 'So forty percent is'), mk('cross', 'choice 3', "That's choice number three"))),
    S('Method 1 · The math way: the triangle value',
      L("Now the ratio table. Percents in one column, kilograms in the other. In the first row, forty percent and "
        "forty-eight. In the second row, the factory's thirty percent, and a question mark.",
        show(b_t['line'], 'Percents in one column'), show(b_t['r1'], 'In the first row'), show(b_t['r2'], 'In the second row')),
      L("Across or down, there's no easy whole number. So we use the triangle value. We multiply along the diagonal, "
        "thirty times forty-eight, and divide by what's left, forty.", show(b_t['dg'], 'We multiply along the diagonal'),
        show(b_4, 'and divide by what')),
      L("Let's make it smaller first. Thirty and forty both divide by ten, so it's three times forty-eight, over four. "
        "Forty-eight divided by four is twelve. Three times twelve is thirty-six.", show(b_5, 'so it\'s three times'),
        show(b_6, 'Forty-eight divided by four'), show(b_t['ans'], 'three times twelve is thirty-six')),
      L("So the factory gets thirty-six kilograms. Choice number two is our answer.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · The math way: through ten percent',
      L("[pause] Now a shorter way. We start again from the givens. The factory gets the rest, thirty percent. The "
        "difference is seventy minus thirty, forty percent, and that's forty-eight kilograms.", show(b_7, 'forty-eight kilograms')),
      L("From forty percent to thirty percent isn't one easy step. So let's take a middle step, ten percent. Forty "
        "percent divided by four is ten percent. So we divide the kilograms by four too. Forty-eight divided by four is "
        "twelve.", show(b_8, 'Forty-eight divided by four is')),
      L("Thirty percent is three times ten percent. Three times twelve is thirty-six kilograms.", show(b_9, 'Three times twelve')),
      L("So when the step isn't easy to see, go through ten percent first. Choice number two is our answer, and I'll see "
        "you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp23-g065 (Hebrew: a pool loses 30% an hour)
# Hebrew (wp 4230-4326): plug in 100 - but a real amount is given, so we plug in 100 PERCENT, not 100 cubic meters;
# 100 -> 70 -> 49 (30% of what is in it now: the complement, 70% of 70); 49% = 98 -> x 2 -> 200; then plugging in the
# answers: the round ones first (200), 140, 98 - the round answer is often right, part of the exam's design.
# REMINDER: plug in 100, what stays, a percent of a percent, working back from what is left (R37: taught in wp-053 part
# 3, the discount and the two-changes pond; this is its first question). NEW here: plug in 100 percent when a real
# amount is given.
w_1 = IH('w_1', 'start: $\\ 100\\%$', size=30)
w_2 = IH('w_2', 'day 1: $\\ 100\\%-10\\%=90\\%$', size=30)
w_3 = IH('w_3', 'day 2: $\\ 90\\%$ of $90\\%=81\\%$', size=30)
w_4 = IH('w_4', 'not $100\\%-10\\%-10\\%$', size=30, col=1)
w_5 = IH('w_5', '$81\\%=243$ L', size=30)
w_6 = IH('w_6', '$80\\cdot3=240$, $\\ 81\\cdot3=243$', size=30)
w_7 = IH('w_7', '$1\\%=3$ L', size=30)
w_8 = IH('w_8', '$100\\%=300$ L', size=30)
w_9 = IH('w_9', '(3) $\\ 300-30=270$', size=30)
w_10 = IH('w_10', '$270-27=243$', size=30)
video('solve-wp23-g065', 'solution', qid='wp23-g065', slides=[
    S('Method 1 · Plugging in numbers',
      L("At the end of each day, ten percent of the water then in a rain barrel is used to water the garden. After two "
        "days, two hundred forty-three liters remain. How many liters were in the barrel at the start?",
        pt('stem', 'At the end of each day', 'hl', 10.0), voice='calm', pause=0.5),
      L("So we know the end, and they ask about the start. We'll solve it in two different ways, by plugging in numbers, "
        "and then by plugging in the answers.", pt('stem', 'they ask about the start')),
      L("Let's start by plugging in numbers. Careful here. We already have a real amount, two hundred forty-three liters. "
        "So we can't just say there were a hundred liters at the start. Instead we plug in a hundred percent. The start "
        "is a hundred percent of the water.", show(w_1, 'Instead we plug in a hundred percent')),
      L("On day one, ten percent is used. So ninety percent of the water is left.", show(w_2, 'So ninety percent')),
      L("On day two, ten percent of the water then in the barrel is used. That's ten percent of what's left, not of the "
        "start. So ninety percent of the ninety percent stays.", pt('stem', 'of the water then in')),
      L("Ninety percent of ninety percent. Nine times nine is eighty-one, so it's eighty-one percent.",
        show(w_3, 'Nine times nine')),
      L("Careful, it's not eighty percent. We don't take away ten percent of the start twice, because the second ten "
        "percent is of a smaller amount.", show(w_4, "Careful, it's not eighty"))),
    S('Method 1 · Plugging in numbers',
      L("So eighty-one percent of the start is two hundred forty-three liters. Like in the lesson, we know what is left, "
        "so now we go back to a hundred percent.", show(w_5, 'So eighty-one percent')),
      L("How many times does eighty-one go into two hundred forty-three? Eighty times three is two hundred forty. So "
        "eighty-one times three is two hundred forty-three. So one percent is three liters.", show(w_6, 'Eighty times three'),
        show(w_7, 'So one percent is three')),
      L("The start is a hundred percent, a hundred times three, three hundred liters. Choice number three is our answer.",
        show(w_8, 'a hundred times three'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Choice number one, two hundred seventy, is the water after one day. It goes back only one day.",
        mk('cross', 'choice 1', 'It goes back only one day'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. We start again from the givens. Which choice first? The roundest one, "
        "three hundred, because ten percent of it is easy."),
      L("On day one, ten percent of three hundred is thirty. Three hundred minus thirty is two hundred seventy.",
        show(w_9, 'Three hundred minus thirty')),
      L("On day two, ten percent of the water now, of two hundred seventy, is twenty-seven. Two hundred seventy minus "
        "twenty-seven is two hundred forty-three.", show(w_10, 'Two hundred seventy minus twenty-seven')),
      L("That's exactly what's left, so three hundred works.", mk('tick', 'choice 3', 'so three hundred works')),
      L("The round answer isn't always right. But it's usually the smartest one to try first, because it's quick to "
        "check. Choice number three is our answer, and I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ r26-t23-traps (lesson)
# English addition (real exam: 2026_spring_q2_07, 2023_spring_q2_12, 2025_winter_q1_20). The other traps are taught in
# the three questions after it. REMINDER: estimation (topic 51). NEW here: estimating a percent between two benchmarks.
x_1 = IH('x_1', 'What percent of $320$ is $90$?', size=32)
x_2 = IH('x_2', '(1) $22\\%$ $\\quad$ (2) $28.125\\%$ $\\quad$ (3) $32\\%$ $\\quad$ (4) $36\\%$', size=30)
x_3 = IH('x_3', '$25\\%$ of $320$: $\\ 160,\\ 80$', size=30)
x_4 = IH('x_4', '$10\\%=32$, $\\ 30\\%=3\\cdot32=96$', size=30)
x_5 = IH('x_5', '$80<90<96$', size=30)
x_6 = IH('x_6', '$25\\%<\\ ?\\ <30\\%$: $\\ $choice (2)', size=30)
video('r26-t23-traps', 'lesson', slides=[
    S('Percent Traps and Shortcuts',
      L("Welcome back. The next three questions show some traps the exam loves. But first, one shortcut that saves a lot "
        "of time, estimating.")),
    S('Estimate',
      L("Here's a question. What percent of three hundred twenty is ninety?", show(x_1, 'What percent of three hundred'),
        show(x_2, 'is ninety')),
      L("We could calculate exactly, ninety over three hundred twenty, times a hundred. That's a long division. But look "
        "at the choices. They're far apart, so an estimate is enough."),
      L("Remember estimation from psychometric thinking. We look for easy percents close to our number."),
      L("Twenty-five percent is a quarter. To find a quarter of three hundred twenty, we halve twice. Half of it is a "
        "hundred sixty, and half again is eighty.", show(x_3, 'and half again is eighty')),
      L("Thirty percent of three hundred twenty. Ten percent is thirty-two, so thirty percent is three times thirty-two, "
        "ninety-six.", show(x_4, 'so thirty percent is three times')),
      L("Ninety is between eighty and ninety-six. So the percent is between twenty-five and thirty.",
        show(x_5, 'Ninety is between'), show(x_6, 'So the percent is between')),
      L("Only choice number two, twenty-eight point one two five percent, is in that range. So that's the answer, with "
        "no long division. [pause] Now three questions. Try each one first, and then watch the solution. I'll see you in "
        "the next video.")),
])

# ------------------------------------------------------------------------------------------------ q-r26-t23-03 (added: "of" or "more than")
# English addition (real exam: 2023_spring_q2_12, 2019_spring_q2_12, 2020_winter_q1_17). REMINDER: plug in 100, who is
# the hundred, the change rule, the arrow map (all wp-053; first applied in g059 / g061). NEW here: p% more than =
# (100 + p)% of.
r_1 = IH('r_1', 'chair: $\\ 100$', size=30)
r_2 = IH('r_2', 'desk: $\\ 150\\%$ of $100=150$', size=30)
r_3 = IH('r_3', 'table: $\\ 100+150=250$', size=30)
r_4 = IH('r_4', '$p\\%$ more than $=(100+p)\\%$ of', size=30, col=1)
r_5 = IH('r_5', '$20\\%$ more $=120\\%$ of', size=30, col=1)
r_6 = IH('r_6', '$150\\%$ more $=250\\%$ of', size=30, col=1)
r_7 = IH('r_7', 'change: $\\ 250-150=100$', size=30)
r_8 = IH('r_8', '$\\frac{100}{150}=\\frac{2}{3}=66\\frac{2}{3}\\%$', size=30)
r_9 = IH('r_9', '(3) $\\ 100$ credits $\\ne100\\%$', size=30, col=1)
r_10 = IH('r_10', '(1) $\\ \\frac{100}{250}=40\\%$: $\\ $wrong whole', size=30, col=1)
r_11 = IH('r_11', '(4) $\\ 50\\%$: $\\ $forgets "more"', size=30, col=1)
r_m = AMAP('r_m', ['desk', 'chair', 'table'], [('a', 1, 0, '×1.5'), ('b', 1, 2, '×2.5')], gap=250)
r_12 = IH('r_12', '$2.5\\div1.5=\\frac{25}{15}=\\frac{5}{3}$', size=30)
r_13 = IH('r_13', '$\\frac{5}{3}=166\\frac{2}{3}\\%$: $\\ 66\\frac{2}{3}\\%$ higher', size=30)
video('solve-q-r26-t23-03', 'solution', qid='q-r26-t23-03', slides=[
    S('Method 1 · Plugging in numbers',
      L("The price of a desk is a hundred fifty percent of the price of a chair. The price of a table is a hundred fifty "
        "percent more than the price of the chair. By what percent is the price of the table higher than the price of the "
        "desk?", pt('stem', 'The price of a desk', 'hl', 11.0), voice='calm', pause=0.5),
      L("Read it carefully. The desk is a hundred fifty percent of the chair. The table is a hundred fifty percent more "
        "than the chair. Of, or more than? That's the whole question.", pt('stem', 'Read it carefully')),
      L("We'll solve it in two different ways, by plugging in numbers, and then with the arrow map."),
      L("Let's start by plugging in numbers. No prices are given, so we plug in a hundred. Into whom? Both sentences "
        "compare with the chair. The chair comes after of, and after than. So the chair is the whole, a hundred.",
        show(r_1, 'So the chair is the whole')),
      L("The desk is a hundred fifty percent of the chair. A hundred fifty percent of a hundred is a hundred fifty.",
        show(r_2, 'A hundred fifty percent of a hundred')),
      L("The table is a hundred fifty percent more than the chair. More than means we keep the chair's price, and add a "
        "hundred fifty percent. A hundred plus a hundred fifty is two hundred fifty.", show(r_3, 'A hundred plus a hundred fifty')),
      L("So here's the rule. p percent more than a number is a hundred plus p percent of it. Twenty percent more is a "
        "hundred twenty percent of it. A hundred fifty percent more is two hundred fifty percent of it.",
        show(r_4, "So here's the rule"), show(r_5, 'Twenty percent more is'), show(r_6, 'A hundred fifty percent more is'))),
    S('Method 1 · Plugging in numbers',
      L("Now the question. By what percent is the table higher than the desk? Than the desk, so now the desk is the "
        "original, the whole.", pt('stem', 'By what percent is the table')),
      L("The change from the desk to the table is two hundred fifty minus a hundred fifty, a hundred.",
        show(r_7, 'The change from the desk')),
      L("We divide the change by the original. A hundred over a hundred fifty is two thirds. And two thirds is sixty-six "
        "and two thirds percent. Choice number two is our answer.", show(r_8, 'A hundred over a hundred fifty'),
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Choice number three, a hundred percent, is a trap. The difference is a hundred credits, but that's not a "
        "hundred percent. We divide it by the desk's price.", show(r_9, 'is a trap'), mk('cross', 'choice 3', 'is a trap')),
      L("Choice number one divides by the table's price. A hundred over two hundred fifty is forty percent, the wrong "
        "whole. And choice number four, fifty percent, reads both sentences as of. It forgets the word more.",
        show(r_10, 'A hundred over two hundred fifty'), mk('cross', 'choice 1', 'the wrong'),
        show(r_11, 'It forgets the word more'), mk('cross', 'choice 4', 'It forgets the word more'))),
    S('Method 2 · The math way: the arrow map',
      L("[pause] Now the arrow map, like in Lior's question. We start again from the givens. Both sentences start at the "
        "chair, the whole.", show(r_m['line'], 'Both sentences start at the')),
      L("The desk is a hundred fifty percent of the chair. So the arrow from the chair to the desk is times one point "
        "five.", show(r_m['a'], 'So the arrow from the chair to the desk')),
      L("The table is a hundred fifty percent more, two hundred fifty percent. So the arrow from the chair to the table "
        "is times two point five.", show(r_m['b'], 'So the arrow from the chair to the table')),
      L("We go from the desk to the table. First back to the chair, against the arrow, so we divide by one point five. "
        "Then on to the table, along the arrow, so we multiply by two point five."),
      L("Two point five divided by one point five is twenty-five over fifteen, five thirds.", show(r_12, 'twenty-five over fifteen')),
      L("Five thirds is a hundred sixty-six and two thirds percent of the desk. So it's sixty-six and two thirds percent "
        "higher. Choice number two is our answer, and I'll see you in the next question.",
        show(r_13, 'Five thirds is a hundred'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t23-04 (added: a mixture)
# English addition (the original course's practice p23 is a mixture; real exam: 2025_autumn_q2_03, the cubes, the same
# structure). NEW here: in a mixture, find what stays the same (add water: the salt stays; add sugar: the water stays).
# REMINDER: what is left (g058), from a percent to the whole (camera lesson), plugging in the answers (51).
m_1 = IH('m_1', 'add water: $\\ $the salt stays', size=30)
m_2 = IH('m_2', 'add sugar: $\\ $the water stays', size=30)
m_3 = IH('m_3', 'water: $\\ 100\\%-20\\%=80\\%$', size=30)
m_4 = IH('m_4', '$80\\%$ of $300=8\\cdot30=240$ g', size=30, col=1)
m_5 = IH('m_5', 'after: $\\ 100\\%-40\\%=60\\%$ water', size=30, col=1)
m_6 = IH('m_6', '$60\\%=240$ g', size=30, col=1)
m_7 = IH('m_7', '$20\\%=240\\div3=80$ g', size=30)
m_8 = IH('m_8', '$100\\%=5\\cdot80=400$ g', size=30)
m_9 = IH('m_9', 'sugar added: $\\ 400-300=100$ g', size=30)
m_10 = IH('m_10', '(2) $\\ 60=20\\%$ of $300$', size=30, col=1)
m_11 = IH('m_11', 'sugar: $\\ 20\\%$ of $300=60$ g', size=30)
m_12 = IH('m_12', '(1) $\\ 60+100=160$ g sugar', size=30)
m_13 = IH('m_13', 'all: $\\ 300+100=400$ g', size=30)
m_14 = IH('m_14', '$\\frac{160}{400}=\\frac{40}{100}=40\\%$', size=30)
video('solve-q-r26-t23-04', 'solution', qid='q-r26-t23-04', slides=[
    S('Method 1 · The math way: what stays the same',
      L("A three hundred gram mixture of sugar and water is twenty percent sugar. How many grams of sugar must be added to "
        "make the mixture forty percent sugar?", pt('stem', 'mixture of sugar and water', 'hl', 7.0), voice='calm', pause=0.5),
      L("This is a mixture question. When we add something to a mixture, the total changes, and so do the percents. The trick is "
        "to find what stays the same. We'll solve it in two different ways, the math way, and then by plugging in the "
        "answers.", pt('stem', 'This is a mixture question')),
      L("Let's start with the math way, and the rule first. Think of a cup of salty water. If we add water, the salt is "
        "still the same salt. If we add salt, the water is still the same water.", show(m_1, 'If we add water'),
        show(m_2, 'If we add salt')),
      L("Here we add sugar. So the sugar changes, and the total changes. What stays the same? The water."),
      L("So let's find the water before. The mixture is twenty percent sugar, so it's a hundred minus twenty, eighty "
        "percent water.", show(m_3, 'eighty percent water')),
      L("Eighty percent of three hundred is eight times thirty, two hundred forty grams of water.",
        show(m_4, 'Eighty percent of three hundred')),
      L("After we add sugar, the mixture is forty percent sugar. So it's a hundred minus forty, sixty percent water. And "
        "the water is still two hundred forty grams.", show(m_5, 'sixty percent water'), show(m_6, 'And the water is still'))),
    S('Method 1 · The math way: what stays the same',
      L("Sixty percent is two hundred forty grams. Let's go down to twenty percent. Sixty divided by three is twenty, so "
        "we divide the grams by three too. Two hundred forty divided by three is eighty grams.",
        show(m_7, 'Two hundred forty divided by three')),
      L("The whole new mixture is a hundred percent, five times twenty percent. Five times eighty is four hundred grams.",
        show(m_8, 'Five times eighty')),
      L("The mixture was three hundred grams, and now it's four hundred. The only thing we added is sugar. So we added "
        "four hundred minus three hundred, a hundred grams of sugar. Choice number one is our answer.",
        show(m_9, 'So we added four hundred minus'), mk('tick', 'choice 1', 'Choice number one is our answer')),
      L("The trap is choice number two, sixty grams. That's twenty percent of three hundred, as if the total doesn't "
        "grow. But when we add sugar, the total grows too.", show(m_10, "That's twenty percent of three hundred"),
        mk('cross', 'choice 2', 'The trap is choice number two'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. We start again from the givens. The mixture has three hundred grams, and "
        "twenty percent of it is sugar. Twenty percent of three hundred is sixty grams of sugar.",
        show(m_11, 'Twenty percent of three hundred is sixty')),
      L("Which choice first? The round one, a hundred grams, choice number one. With a hundred grams added, the sugar is "
        "sixty plus a hundred, a hundred sixty grams.", show(m_12, 'the sugar is sixty plus')),
      L("And the whole mixture is three hundred plus a hundred, four hundred grams.", show(m_13, 'And the whole mixture is')),
      L("A hundred sixty out of four hundred. We divide both by four, and get forty out of a hundred, forty percent. "
        "That's what we want.", show(m_14, 'We divide both by four'), mk('tick', 'choice 1', "That's what we want")),
      L("So when you see a mixture, ask what stays the same. Choice number one is our answer, and I'll see you in the "
        "next question.")),
])

# ------------------------------------------------------------------------------------------------ q-r26-t23-05 (added: letters in the choices)
# English addition (real exam: 2024_spring_q1_16, 2024_winter_q1_15, 2021_spring_q1_13). REMINDER: plugging in numbers
# and its rules (topic 51: easy numbers, a different number for each letter, usually not 0 or 1; two choices left ->
# new numbers), the percent = part / whole x 100. NEW here: why these numbers (a quarter of g is whole, g < N).
q_1 = IH('q_1', '$N=200,\\ \\ g=80$', size=30)
q_2 = IH('q_2', '$25\\%$ of $80=20$ girls', size=30)
q_3 = IH('q_3', '$\\frac{20}{200}=\\frac{10}{100}=10\\%$', size=30)
q_4 = IH('q_4', 'target: $\\ 10$', size=30)
q_5 = IH('q_5', '(1) $\\ \\frac{80}{800}=\\frac{1}{10}$', size=30, col=1)
q_6 = IH('q_6', '(2) $\\ \\frac{8000}{200}=40$', size=30, col=1)
q_7 = IH('q_7', '(3) $\\ \\frac{25\\cdot80}{200}=\\frac{2000}{200}=10$', size=30, col=1)
q_8 = IH('q_8', '(4) $\\ \\frac{5000}{80}>60$', size=30, col=1)
q_9 = IH('q_9', 'chess girls: $\\ \\frac{g}{4}$', size=30)
q_10 = I('q_10', 'percent $=\\frac{\\text{part}}{\\text{whole}}\\times100$', size=30, hand='percent = {part/whole}×100')
q_11 = IH('q_11', '$\\frac{g}{4}\\div N=\\frac{g}{4N}$', size=30, col=1)
q_12 = IH('q_12', '$\\frac{g}{4N}\\cdot100=\\frac{100g}{4N}$', size=30, col=1)
q_12b = IH('q_12b', '$=\\frac{25g}{N}$', size=30, col=1)
video('solve-q-r26-t23-05', 'solution', qid='q-r26-t23-05', slides=[
    S('Method 1 · Plugging in numbers',
      L("A school has N students, and g of them are girls. Twenty-five percent of the girls play chess. What percent of "
        "all the students are girls who play chess?", pt('stem', 'A school has N students', 'hl', 8.0), voice='calm', pause=0.5),
      L("There are letters in the question and in the choices. That's a hint that we can plug in numbers. We'll solve it "
        "in two different ways, by plugging in numbers, and then the math way.", pt('stem', 'There are letters')),
      L("Let's start by plugging in numbers. Remember the rules from psychometric thinking. Easy numbers, a different "
        "number for each letter, and usually not zero or one."),
      L("Let's say there are two hundred students, so N is two hundred. And eighty of them are girls, so g is eighty. Why "
        "eighty? Because a quarter of eighty is a whole number, and eighty is less than two hundred.", show(q_1, 'so g is eighty')),
      L("Twenty-five percent of the girls play chess. A quarter of eighty is twenty girls.", show(q_2, 'A quarter of eighty is')),
      L("Now, what percent of all the students is that? Twenty out of two hundred is ten out of a hundred, ten percent. "
        "So our target is ten.", show(q_3, 'Twenty out of two hundred'), show(q_4, 'So our target is ten'))),
    S('Method 1 · Plugging in numbers',
      L("Now we put N is two hundred and g is eighty into every choice. Choice number one says g over four N. Four times two "
        "hundred is eight hundred, so it's eighty over eight hundred. That's a tenth, not ten. Out.", show(q_5, 'Eighty over eight hundred'), mk('cross', 'choice 1', 'not ten. Out')),
      L("Choice number two says a hundred g over N. A hundred times eighty is eight thousand, and eight thousand over two hundred is forty. That's the percent of girls, "
        "not of chess players. Out.", show(q_6, 'Eight thousand over two hundred'), mk('cross', 'choice 2', 'not of chess players')),
      L("Choice number three says twenty-five g over N. Twenty-five times eighty is two thousand, and two thousand over two "
        "hundred is ten. That's our target.", show(q_7, 'Twenty-five times eighty')),
      L("In the exam you'd circle it and move on. Here, let's check the last one too. Choice number four says twenty-five "
        "N over g. Twenty-five times two hundred is five thousand. Five thousand over eighty is more than sixty, because eighty times sixty is only four thousand eight hundred. Out.",
        show(q_8, 'Five thousand over eighty'), mk('cross', 'choice 4', 'more than sixty')),
      L("Only choice number three gives ten. If two choices had given ten, we'd pick new numbers and test only those "
        "two. Choice number three is our answer.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · The math way',
      L("[pause] Now the math way, with the letters. We start again from the givens. Twenty-five percent of the girls is "
        "a quarter of g, so g over four girls play chess.", show(q_9, 'so g over four girls')),
      L("To get a percent, we take the part over the whole, times a hundred. The part is g over four, and the whole is "
        "all the students, N.", show(q_10, 'we take the part over the whole')),
      L("g over four, divided by N, is g over four N.", show(q_11, 'divided by N')),
      L("Times a hundred, it's a hundred g over four N. A hundred over four is twenty-five, so it's twenty-five g over N.",
        show(q_12, 'Times a hundred'), show(q_12b, 'A hundred over four is twenty-five')),
      L("Choice number one, g over four N, is only the fraction of the students. We still need to multiply by a hundred "
        "to get a percent. Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# =================================================================================================================
QBOT23 = {'solve-q-r26-t23-01': 181, 'solve-q-r26-t23-03': 239, 'solve-q-r26-t23-04': 242, 'solve-q-r26-t23-05': 242,
          'solve-q-r26-t23-16': 242, 'solve-wp23-g054': 286, 'solve-wp23-g057': 181, 'solve-wp23-g058': 181,
          'solve-wp23-g059': 242, 'solve-wp23-g060': 286, 'solve-wp23-g061': 192, 'solve-wp23-g062': 150,
          'solve-wp23-g063': 150, 'solve-wp23-g064': 242, 'solve-wp23-g065': 242}   # measured on the step frames
QBOT.update(QBOT23)
CARRY23 = {
    'solve-wp23-g054': {1: ['$100$ students: $\\ 65$ play']},
    'solve-wp23-g059': {1: ['$40\\to50$: $\\ +25\\%$']},
    'solve-wp23-g060': {1: ['$0.7x$ left'], 3: ['start $100$: $\\ 98$, $\\ 2\\%$ fewer']},
    'solve-q-r26-t23-01': {1: ['$1.25\\cdot0.88$']},
    'solve-wp23-g062': {2: ['$x\\%$ of $y=y\\%$ of $x$']},
    'solve-wp23-g065': {1: ['$81\\%$ of the start is left']},
    'solve-q-r26-t23-03': {1: ['chair $100$, desk $150$, table $250$']},
    'solve-q-r26-t23-04': {1: ['water $240$ g $=60\\%$']},
    'solve-wp23-g064': {1: ['factory $30\\%$, $\\ 40\\%=48$ kg']},
    'solve-q-r26-t23-05': {1: ['$N=200$, $g=80$: $\\ $target $10$']},
}
STEMS23 = {
 "wp23-g054": "In a survey, 35% of the students do not play a musical instrument. Of the students who play an instrument, 80% play the piano and the rest play only the guitar. What percentage of all the surveyed students play only the guitar?",
 "wp23-g058": "A winter coat originally costs 680 credits. In a clearance sale, its price is reduced by 75%. What is the new price?",
 "wp23-g057": "A printer cartridge has used 57.5% of its ink. What fraction of the ink remains?",
 "wp23-g059": "The price of a cinema ticket rises from 40 credits to 50 credits, and later to 60 credits. How do the two percentage increases compare?",
 "wp23-g060": "In a computer game, Noa loses 30% of her coins. She then wins a prize equal to 40% of the coins she has left. Compared with the number of coins she had at the start, how many coins does she have now?",
 "q-r26-t23-01": "A price rises by 25%. Later, the new price falls by 12%. By what percent is the final price higher than the original price?",
 "wp23-g061": "Dana earns 50% more than Omer. Lior earns 33 1/3% less than Dana. What is Lior’s wage divided by Omer’s wage?",
 "wp23-g062": "25% of 18% of y equals 9. What is 13.5% of y?",
 "wp23-g063": "For y>0, which expression is not equal to 16% of 5y?",
 "q-r26-t23-16": "A library has only novels and textbooks, 600 books in all. 45% of the novels is the same number of books as 30% of the textbooks. How many novels does the library have?",
 "wp23-g064": "A farmer sells 70% of his apples at a market and all the rest to a juice factory. The market gets 48 kg more apples than the factory. How many kilograms of apples does the factory get?",
 "wp23-g065": "At the end of each day, 10% of the water then in a rain barrel is used to water the garden. After two days, 243 liters remain. How many liters were in the barrel at the start?",
 "q-r26-t23-03": "The price of a desk is 150% of the price of a chair. The price of a table is 150% more than the price of the chair. By what percent is the price of the table higher than the price of the desk?",
 "q-r26-t23-04": "A 300-gram mixture of sugar and water is 20% sugar. How many grams of sugar must be added to make the mixture 40% sugar?",
 "q-r26-t23-05": "A school has N students, and g of them are girls. 25% of the girls play chess. What percent of all the students are girls who play chess?",
}   # word stems: "given" = the story, "ask" = the question sentence
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
STEMS = STEMS23

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
CP.split(globals(), *SPLIT053)       # 2026-10-21 R37: wp-053 grew (the core methods are taught there), in parts

for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _stem_parts(_v); _write_gap(_v)



# 2026-10-13 carry-over boxes (V2) and the layer-order check (V1): after the visual passes, like topics 13-18
import types as _types
MV.carry(_types.SimpleNamespace(**globals()), CARRY23)
for _v in CARRY23:                                      # 2026-10-18 visual check: the So-far box at a readable size
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
