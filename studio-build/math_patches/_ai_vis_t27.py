"""Topic 27 (Motion) - the scripts for the teacher's own-voice reading (2026-10-23), written from the first draft to the
Codex review standard, the clarity style, W1-W25 (W24: Codex's lessons, W25: the acceptance standard), R37 (core methods
taught in the lessons), the method vocabulary and the method visuals, built exactly like topics 22-26
(math_patches/_ai_vis_t26.py: the DSL and the visual passes are copied here, so the topics stay independent).

The camera lesson 'wp-106' (Distance, Speed and Time) gets a full reading script with more examples, split into three
parts of about 3-4 minutes (math_patches/_camera_parts.py). The lessons that carry the topic's core methods (R37) are split
into parts too (not on camera): wp-110 (speed ratios), wp-113 (relative speed) and r26-t27-special (trains and circular
tracks, now a real lesson). Every other topic-27 video gets a script that SHE reads aloud in the Reading Studio. The
summary video r26-t27-summary is not read: summary_pages/t27.json (python3 summary_pages.py 27) replaces it.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t27.py [vid ...] writes it);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t27.py ai_redo_t27() (runs LAST) rebuilds the slides from studio_slides(vid) and then
                    _ai_visual.apply() adds the click items, POINT highlights and pen marks around it.

Spec DSL (as in topic 26): video / S / L / I / IH (a hand-written board line) / show / pt / mk; the topic-27 pictures of
her Hebrew course, built in layers at the spoken words: TRI27 (the motion triangle), ROAD (the sketch: ends, movers with
their start times, arrows with speeds, the gap, the meeting point, the road in ratio parts, a train with its length),
TRACK (the circular track), RTRI (the climb's right triangle), TBL (the speed | distance | time table) and VT27 (the V
with distance in the middle). The concept map (NEW / REMINDER per video) is in ~/Downloads/Topic-27-AI-scripts-review.md.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(HERE) != 'math_patches':      # a test copy elsewhere still reads and writes the real studio files
    HERE = '/Users/nitzanslasky/psychometry-course/studio-build/math_patches'
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t27ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-27 flow order of the scripts
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
CAM_BASE = 'wp-106'
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
            'style': "the teacher reads it herself (Reading Studio), topic-27 scripts (2026-10-23): math_patches/_ai_vis_t27.py is "
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



CARRY27 = {}      # vid -> carry-over ("So far") boxes, _method_visuals.carry format
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



# ------------------------------------------------------------------------------------------- topic-26 figures (V1)
# TRI26  the formula triangle (wp 5945-5962: «משולש ההספק... אני מסתיר אותו ומבצע כפל או חילוק בהתאם למה שנשאר»): the
#        triangle, the three names (work on top, rate and time at the bottom), then "cover" one name at a time (a teal
#        card over it; the card of the previous cover is lifted again in the same layer).
# VT     the V method (wp 6285-6341), _method_visuals.VTABLE: the empty team | work | time table, row 1, row 2, the V (or
#        the upside-down V when the work is asked), the rule "multiply the V, divide by the other two".
def TRI26(name, top='Work', left='Rate', right='Time', col=0, w=None, title='The formula triangle'):
    W, H = 360, 250
    pos = {'top': (180, 112, top, 30), 'left': (120, 200, left, 28), 'right': (240, 200, right, 28)}
    body = ('<path d="M 180 14 L 340 230 L 20 230 Z" fill="%s" stroke="%s" stroke-width="2.6"/>' % (_LIGHT, _INK) +
            '<line x1="80" y1="140" x2="280" y2="140" stroke="%s" stroke-width="2.4"/>' % _INK +
            '<line x1="180" y1="140" x2="180" y2="230" stroke="%s" stroke-width="2.4"/>' % _INK)
    out = [('line', MV._svg(W, H, body, title))]
    word = lambda k: _tx(pos[k][0], pos[k][1], pos[k][2], pos[k][3], _INK)
    out.append(('vals', MV._svg(W, H, ''.join(word(k) for k in ('top', 'left', 'right')), '%s = %s × %s' % (top, left, right))))
    def card(k):
        x, y, t, s = pos[k]
        return ('<rect x="%.1f" y="%.1f" width="96" height="44" rx="8" fill="%s" stroke="%s" stroke-width="2.4"/>'
                % (x - 48, y - 32, _TEAL, _TEAL) + _tx(x, y, '?', 32, '#ffffff'))
    def lift(k):
        x, y, t, s = pos[k]
        return ('<rect x="%.1f" y="%.1f" width="104" height="52" fill="%s"/>' % (x - 52, y - 36, _LIGHT)) + word(k)
    prev = None
    for k in ('top', 'right', 'left'):
        b = (lift(prev) if prev else '') + card(k)
        out.append(('cover_' + k, MV._svg(W, H, b, 'cover the %s' % pos[k][2].lower())))
        prev = k
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def VT(name, given, asked, unknown='time', col=0, w=None):
    """the V method table (own=True: the written calculation lines can come between its layers)"""
    return MV.items(_layers, name, MV.VTABLE(given, asked, unknown), w=w, col=col, own=True)



# ------------------------------------------------------------------------------------------- topic-27 figures (V1)
# The pictures of her Hebrew motion lessons, built in layers at the spoken words (own=True: a layer finds its own base,
# so written lines can come in between):
#   TRI27  the motion triangle (wp 6999-7014: «משולש התנועה... אני פשוט מסתיר אותו ומבצע את התרגיל שמולי»): distance on
#          top, speed and time at the bottom; one teal card over the name we cover.
#   ROAD   the motion sketch (wp 7096 «בכלל בעיות תנועה מומלץ לשרטט», 7560-7567 the truck: the cities, the first stage,
#          the gap left, the two speeds toward each other; 7590-7610 Miki: the head start, the gap, the chase; 7244-7419
#          the road cut into 2 + 3 parts): a road with its ends, each mover as a dot with its start time, an arrow per
#          direction with its speed, the gap bracketed, the meeting point, equal parts and each mover's share.
#   TRACK  the circular track (wp 8061-8130 the karts and the lap counter): the track, the start, the two runners, an arrow
#          for each direction, the lap in the middle.
#   RTRI   the right triangle of a climb (wp 7097-7106 the plane: the sloping path, the ground, the height).
#   VT27   the V method with distance in the middle (speed | distance | time), as in the work topic (wp 6285-6341).
#   TBL    (above) the speed | distance | time table (wp 7175, 7550-7599, 7879): a row per mover or part.
_RED27 = '#d62d48'


def TRI27(name, col=0, w=None, title='The motion triangle'):
    W, H = 460, 270
    pos = {'top': (230, 124, 'Distance', 30), 'left': (160, 218, 'Speed', 30), 'right': (300, 218, 'Time', 30)}
    tri = ('<path d="M 230 14 L 440 254 L 20 254 Z" fill="%s" stroke="%s" stroke-width="2.6"/>' % (_LIGHT, _INK) +
           '<line x1="107" y1="155" x2="353" y2="155" stroke="%s" stroke-width="2.4"/>' % _INK +
           '<line x1="230" y1="155" x2="230" y2="254" stroke="%s" stroke-width="2.4"/>' % _INK)
    out = [('line', MV._svg(W, H, tri, title))]
    word = lambda k: _tx(pos[k][0], pos[k][1], pos[k][2], pos[k][3], _INK)
    out.append(('vals', MV._svg(W, H, ''.join(word(k) for k in ('top', 'left', 'right')), 'distance = speed × time')))
    def card(k):
        x, y, t, s = pos[k]
        return ('<rect x="%.1f" y="%.1f" width="120" height="46" rx="8" fill="%s" stroke="%s" stroke-width="2.4"/>'
                % (x - 60, y - 33, _TEAL, _TEAL) + _tx(x, y, '?', 32, '#ffffff'))
    for k in ('top', 'right', 'left'):         # each cover redraws the whole triangle, so the card before it is gone
        b = tri + ''.join(word(j) for j in ('top', 'left', 'right') if j != k) + card(k)
        out.append(('cover_' + k, MV._svg(W, H, b, 'cover the %s' % pos[k][2].lower())))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def VT27(name, given, asked, unknown='time', col=0, w=None, title='The V method'):
    """the V table with distance in the middle: columns speed | distance | time, row 1 given, row 2 asked ('?')."""
    colw = [190, 190, 190]; W, H, body, cell, xs = MV._table(('Speed', 'Distance', 'Time'), 2, colw, 74, y0=10)
    H += 60
    out = [('line', MV._svg(W, H, body, title + ': speed, distance, time'))]
    for r, row in enumerate((given, asked)):
        b = ''.join(MV._text(*cell(r, c), v, 30, _TEAL if v == '?' else _INK) for c, v in enumerate(row) if v != '')
        out.append(('r%d' % (r + 1), MV._svg(W, H, b, 'row %d: speed %s, distance %s, time %s' % ((r + 1,) + tuple(row)))))
    (xt1, yt1), (xw1, yw1), (xm1, ym1) = cell(0, 0), cell(0, 1), cell(0, 2)
    (xt2, yt2), (xw2, yw2), (xm2, ym2) = cell(1, 0), cell(1, 1), cell(1, 2)
    if unknown != 'distance':
        b = ('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="%s" stroke-width="3.4" stroke-linejoin="round"/>'
             % (xt1 + 26, yt1 - 6, xw2, yw2 + 12, xm1 - 26, ym1 - 6, _TEAL))
    else:
        b = ('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="%s" stroke-width="3.4" stroke-linejoin="round"/>'
             % (xt2 + 26, yt2 - 14, xw1, yw1 - 30, xm2 - 26, ym2 - 14, _TEAL))
    out.append(('v', MV._svg(W, H, b, 'the V')))
    out.append(('calc', MV._svg(W, H, MV._text(W / 2, H - 22, 'multiply the V, divide by the other two', 24, _TEAL),
                                'multiply the V, divide by the other two')))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def ROAD(name, layers, col=0, w=None, title='The sketch', H=None, Y=None):
    """a straight road from L to R; positions p in 0..1. layers = [(key, [mark, ...])]:
      ('end', p, text)               a tick and a name under the road (a town, home, the gate)
      ('dot', p, text[, colour])     a mover on the road, its name (and start time) above it
      ('arrow', a, b, text[, row[, colour]])  a direction arrow above the road from a to b, its speed above it
      ('gap', a, b, text)            a bracket under the road from a to b and its length (teal)
      ('meet', p, text)              the meeting point: a teal star, its text under the road
      ('parts', a, b, n)             the road from a to b cut into n equal parts (ticks)
      ('seg', a, b[, colour])        a tinted part of the road (a share; 'orange' for the second mover)
      ('block', a, b, text)          a box on the road (a train with its length)
      ('post', p, text)              a post standing at p, its name above
      ('below', p, text[, colour])   a text under the road
      ('above', p, text[, row])      a text above the road"""
    W = 1000; L_, R_ = 70, 930
    if Y is None:                       # the room above / under the road that the marks really need
        top, bot = 30, 26
        for _k, ms in layers:
            for m in ms:
                if m[0] in ('dot', 'above'): top = max(top, 54 + 52 * (m[3] if m[0] == 'above' and len(m) > 3 else 0))
                if m[0] == 'arrow': top = max(top, 112 + 52 * (m[4] if len(m) > 4 else 0))
                if m[0] == 'post': top = max(top, 124)
                if m[0] == 'block': top = max(top, 68)
                if m[0] in ('end', 'meet', 'below'): bot = max(bot, 68)
                if m[0] == 'gap': bot = max(bot, 116)
        Y = top
    if H is None: H = Y + bot
    X = lambda p: L_ + p * (R_ - L_)
    def _tx(x, y, t, size=28, col=None, anchor='middle'):      # a label near an edge stays inside the picture
        w2 = len(t) * size * 0.3
        if x - w2 < 6: return MV._text(6, y, t, size, col or _INK, 'start')
        if x + w2 > W - 6: return MV._text(W - 6, y, t, size, col or _INK, 'end')
        return MV._text(x, y, t, size, col or _INK, anchor)
    body = ('<rect x="%d" y="%d" width="%d" height="14" rx="7" fill="%s" stroke="%s" stroke-width="2.4"/>'
            % (L_, Y - 7, R_ - L_, _LIGHT, _INK))
    out = [('line', MV._svg(W, H, body, title))]
    col_ = lambda c: {'orange': ORANGE, 'red': _RED27, 'ink': _INK}.get(c, _TEAL)
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'end':
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3"/>' % (X(m[1]), Y - 20, X(m[1]), Y + 20, _INK)
                      + _tx(X(m[1]), Y + 56, m[2], 32, _INK))
            elif k == 'dot':
                c = col_(m[3] if len(m) > 3 else '')
                b += '<circle cx="%.1f" cy="%d" r="12" fill="%s" stroke="#ffffff" stroke-width="2"/>' % (X(m[1]), Y, c)
                b += _tx(X(m[1]), Y - 24, m[2], 32, c)
            elif k == 'arrow':
                row = m[4] if len(m) > 4 else 0; c = col_(m[5] if len(m) > 5 else '')
                y = Y - 70 - row * 52
                b += MV._arrow(X(m[1]), y, X(m[2]), y, c, 3.2) + _tx((X(m[1]) + X(m[2])) / 2, y - 12, m[3], 32, c)
            elif k == 'gap':
                xa, xb = X(m[1]) + 2, X(m[2]) - 2; y = Y + 72
                b += ('<path d="M %.1f %d L %.1f %d L %.1f %d L %.1f %d" fill="none" stroke="%s" stroke-width="2.8"/>'
                      % (xa, y - 12, xa, y, xb, y, xb, y - 12, _TEAL)) + _tx((xa + xb) / 2, y + 36, m[3], 32, _TEAL)
            elif k == 'meet':
                x = X(m[1])
                pts = ' '.join('%.1f,%.1f' % (x + (17 if i % 2 == 0 else 7) * __import__('math').cos(__import__('math').pi * (i / 5.0 - .5)),
                                              Y + (17 if i % 2 == 0 else 7) * __import__('math').sin(__import__('math').pi * (i / 5.0 - .5))) for i in range(10))
                b += '<polygon points="%s" fill="%s" stroke="#ffffff" stroke-width="1.5"/>' % (pts, _RED27)
                b += _tx(x, Y + 56, m[2], 30, _RED27)
            elif k == 'parts':
                a, e, n = m[1], m[2], m[3]
                b += ''.join('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.6"/>'
                             % (X(a + (e - a) * j / float(n)), Y - 14, X(a + (e - a) * j / float(n)), Y + 14, _INK) for j in range(1, n))
            elif k == 'seg':
                f = {'orange': '#fbd9b9'}.get(m[3] if len(m) > 3 else '', MV.BAND)
                b += ('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2.4"/>'
                      % (X(m[1]), Y - 7, X(m[2]) - X(m[1]), f, _INK))
            elif k == 'block':
                b += ('<rect x="%.1f" y="%d" width="%.1f" height="48" rx="8" fill="#dde6f3" stroke="%s" stroke-width="2.6"/>'
                      % (X(m[1]), Y - 58, X(m[2]) - X(m[1]), _INK)) + _tx((X(m[1]) + X(m[2])) / 2, Y - 24, m[3], 30, _INK)
            elif k == 'post':
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="5"/>' % (X(m[1]), Y - 8, X(m[1]), Y - 84, _INK)
                      + _tx(X(m[1]), Y - 96, m[2], 28, _INK))
            elif k == 'below':
                b += _tx(X(m[1]), Y + 54, m[2], 28, col_(m[3] if len(m) > 3 else ''))
            elif k == 'above':
                b += _tx(X(m[1]), Y - 24 - 52 * (m[3] if len(m) > 3 else 0), m[2], 28, _INK)
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def TRACK(name, layers, col=0, w=None, title='The circular track', label_size=26):
    """a circular track; angles in degrees, 0 = the start at the bottom, growing counter-clockwise. layers:
      ('start', text)                     the start line at the bottom, its text under it
      ('runner', a, text[, colour])       a runner at angle a, its name outside the track
      ('dir', a0, a1, text[, colour])     an arrow along the outside of the track from a0 to a1, its text near its middle
      ('center', text[, line])            a text in the middle of the track (line 0 or 1)
      ('meet', a, text)                   a red star at angle a, its text outside"""
    import math
    W, H = 720, 540; cx, cy, r = 360, 255, 180
    P = lambda a, rr=r: (cx + rr * math.sin(math.radians(a)), cy + rr * math.cos(math.radians(a)))
    body = ('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="16"/>' % (cx, cy, r, _LIGHT) +
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="2.4"/>' % (cx, cy, r + 8, _INK) +
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="2.4"/>' % (cx, cy, r - 8, _INK))
    out = [('line', MV._svg(W, H, body, title))]
    col_ = lambda c: {'orange': ORANGE, 'red': _RED27, 'ink': _INK}.get(c, _TEAL)
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'start':
                b += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="5"/>' % (cx, cy + r - 16, cx, cy + r + 16, _INK)
                b += _tx(cx, cy + r + 52, m[1], 28, _INK)
            elif k == 'runner':
                c = col_(m[3] if len(m) > 3 else ''); x, y = P(m[1]); xo, yo = P(m[1], r - 46)
                b += '<circle cx="%.1f" cy="%.1f" r="12" fill="%s" stroke="#ffffff" stroke-width="2"/>' % (x, y, c)
                b += _tx(xo, yo + 9, m[2], label_size, c)
            elif k == 'dir':
                a0, a1 = m[1], m[2]; c = col_(m[4] if len(m) > 4 else ''); rr = r + 26 if len(m) <= 5 else m[5]
                n = 24; pts = [P(a0 + (a1 - a0) * j / float(n), rr) for j in range(n + 1)]
                b += '<polyline points="%s" fill="none" stroke="%s" stroke-width="3.2"/>' % (' '.join('%.1f,%.1f' % p for p in pts[:-1]), c)
                (x1, y1), (x2, y2) = pts[-3], pts[-1]
                b += MV._arrow(x1, y1, x2, y2, c, 3.2)
                xm, ym = P((a0 + a1) / 2.0, rr + 40)
                b += _tx(xm, ym + 9, m[3], label_size, c)
            elif k == 'center':
                b += _tx(cx, cy - 6 + 40 * (m[2] if len(m) > 2 else 0), m[1], max(28,label_size), _TEAL)
            elif k == 'meet':
                x, y = P(m[1]); xo, yo = P(m[1], r + 44)
                pts = ' '.join('%.1f,%.1f' % (x + (17 if i % 2 == 0 else 7) * math.cos(math.pi * (i / 5.0 - .5)),
                                              y + (17 if i % 2 == 0 else 7) * math.sin(math.pi * (i / 5.0 - .5))) for i in range(10))
                b += '<polygon points="%s" fill="%s" stroke="#ffffff" stroke-width="1.5"/>' % (pts, _RED27) + _tx(xo, yo + 9, m[2], label_size, _RED27)
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def RTRI(name, layers, col=0, w=None, title='The right triangle'):
    """a climb: bottom-left start, the ground to the right, the height up at the right end, the sloping path.
    layers: ('path', text) the slope and its length, ('ground', text), ('height', text), ('right',) the square."""
    W, H = 720, 330; A, B, C = (70, 270), (520, 270), (520, 60)
    body = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (A + B + (_INK,)) +
            '<circle cx="%d" cy="%d" r="7" fill="%s"/>' % (A + (_INK,)) + _tx(A[0], A[1] + 40, 'start', 26, _INK))
    out = [('line', MV._svg(W, H, body, title))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'path':
                b += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>' % (A + C + (_TEAL,))
                b += _tx((A[0] + C[0]) / 2 - 40, (A[1] + C[1]) / 2 - 14, m[1], 38, _TEAL)
            elif k == 'ground':
                b += _tx((A[0] + B[0]) / 2, B[1] + 44, m[1], 38, _INK)
            elif k == 'height':
                b += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3" stroke-dasharray="9 6"/>' % (B + C + (ORANGE,))
                b += _tx(B[0] + 16, (B[1] + C[1]) / 2 + 12, m[1], 38, ORANGE, 'start')
            elif k == 'right':
                b += '<path d="M %d %d L %d %d L %d %d" fill="none" stroke="%s" stroke-width="2.4"/>' % (B[0] - 26, B[1], B[0] - 26, B[1] - 26, B[0], B[1] - 26, _INK)
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


# =================================================================================================================
# THE SCRIPTS (topic-27 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-27-AI-scripts-review.md.
# Study plan before topic 27 (src/lib/planData.ts ORDER): 1, 30, 2, 4, 31, 6, 8, 32, 9, 10, 33, 51, 39, 42, 21, 3, 43,
# 22, 41, 5, 7, 44, 23, 11, 24, 49, 12, 45, 25, 40, 34, 13, 52, 26, 14, 46, 35, 15, 52, 47. So fractions (2, 3),
# equations (6, 7), Pythagoras (31), circles and the circumference (33), the method names and plugging in (51), the ratio
# table, identical ratios and the triangle value (22), percent multipliers (23), the weighted average (25) and the whole
# work topic (26: rate x time = work, the triangle, direct and inverse, the flip, the V, adding rates) are REMINDERS.
# New here: distance = speed x time and its triangle, the units (minutes as fractions of an hour, converting a speed by
# identical ratios), the speed | distance | time table, the sketch; average speed; speed ratios (what is fixed, a meeting
# in ratio parts, the V with distance in the middle); relative speed (toward / apart add, a chase subtracts, the starting
# gap, the head start, "how much faster", from whose start the time is counted); trains with a length; circular tracks;
# the current; a percent change of the speed; letters in the choices.
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ wp-106 (camera lesson)
# Hebrew (wp 6985-7116): motion is a work problem ("instead of cracking seeds I cover distance"); d = t x v and the
# triangle ("whoever knows it, fine; whoever needs the triangle, here it is"); 30 kph x 4 h; always the same units; 1 km =
# 1000 m, 1 h = 60 min, 1 min = 60 s; kph = km in ONE hour, m/s = m in ONE second; x3.6: forget it (almost never on the
# exam, nobody remembers multiply or divide) -> identical ratios; Pythagoras: the plane, north and west, "when the
# directions differ, draw", "in motion questions always draw". English (camera lesson, 2-3 examples per idea, numbers
# differ from the Hebrew and from the questions): 15 x 3 = 45; the triangle with its three covers; 120 / 40 = 3 h,
# 150 / 2 = 75 kph; minutes as fractions of an hour (and the 1.25 h trap); 60 kph for 40 min = 40 km; converting with
# identical ratios on its OWN examples (90 kph -> 30 km in 20 minutes; 10 m/s -> 36 kph), so g107 applies the method to
# new numbers instead of repeating the lesson's example (Hebrew-vs-English report, section 2); the speed | distance | time
# table (two parts, the total row, never add speeds, the link); the sketch (ends, dots with start times, arrows with
# speeds, the gap, the meeting point); a right triangle when the directions differ (Pythagoras: REMINDER, topic 31).
# Real exam: 2025_winter_q1_16 (1 km in 72 s), 2021_autumn_q2_01, 2022_autumn_q2_09 (d = vt with letters).
m_w1 = I('m_w1', 'Work: $\\ $rate $\\times$ time $=$ work', size=36)
m_w2 = I('m_w2', '$25$ boxes an hour', size=36)
m_w3 = I('m_w3', '$25$ kilometers an hour', size=36)
m_f = I('m_f', 'Distance $=$ speed $\\times$ time', size=46)
m_k1 = I('m_k1', 'kph: $\\ $kilometers in ONE hour', size=34)
m_e1 = I('m_e1', '$15$ kph, $\\ $for $3$ hours', size=36)
m_e2 = IH('m_e2', '$15\\times3=45$ km', size=36)
m_tr = TRI27('m_tr', w=520)
m_t1 = IH('m_t1', 'distance $=$ speed $\\times$ time', size=34, col=1)
m_t2 = IH('m_t2', 'time $=$ distance $\\div$ speed', size=34, col=1)
m_t3 = IH('m_t3', 'speed $=$ distance $\\div$ time', size=34, col=1)
m_g1 = I('m_g1', 'A train: $\\ 120$ km at $40$ kph. $\\ $Time?', size=36)
m_g2 = IH('m_g2', 'time $=$ distance $\\div$ speed', size=34)
m_g3 = IH('m_g3', '$120\\div40=3$ hours', size=36)
m_g4 = I('m_g4', 'A bus: $\\ 150$ km in $2$ hours. $\\ $Speed?', size=36)
m_g5 = IH('m_g5', 'speed $=$ distance $\\div$ time', size=34)
m_g6 = IH('m_g6', '$150\\div2=75$ kph', size=36)
m_g7 = IH('m_g7', '$75\\times2=150$', size=34)
_wp106 = [
    S('Distance, Speed and Time',
      L("Welcome back, and now a new topic, motion."),
      L("Motion questions come up in almost every exam. Cars, trains, runners and boats all cover some distance in "
        "some time."),
      L("And the good news is that you already know the idea, from work and rate.")),
    S('Motion is work',
      L("Remember the work formula? Rate times time is equal to work.", show(m_w1, 'Rate times time is equal to work')),
      L("In motion, the work is the distance we cover. And the rate is our speed."),
      L("In work, a machine packs twenty-five boxes an hour.", show(m_w2, 'packs twenty-five boxes an hour')),
      L("In motion, a car covers twenty-five kilometers an hour. It's the same idea, with new names.",
        show(m_w3, 'a car covers twenty-five kilometers an hour')),
      L("So the motion formula is this. Distance is equal to speed times time.",
        show(m_f, 'Distance is equal to speed times time')),
      L("The speed is the distance we cover in one unit of time. Kilometers per hour means how many kilometers we "
        "cover in one hour.", show(m_k1, 'Kilometers per hour means'))),
    S('The formula',
      L("Let's see it in numbers. A cyclist rides at fifteen kilometers per hour, for three hours. How far does she "
        "ride?", show(m_e1, 'A cyclist rides at fifteen kilometers per hour')),
      L("Fifteen kilometers per hour means fifteen kilometers in each hour. So every hour adds fifteen more "
        "kilometers."),
      L("For three hours, we multiply fifteen by three. Fifteen times three is forty-five. So she rides forty-five kilometers.",
        show(m_e2, 'Fifteen times three is forty-five')),
      L("So to find the distance, we multiply the speed by the time.")),
    S('The triangle',
      L("If you're not sure when to multiply and when to divide, use the motion triangle.",
        show(m_tr['line'], 'use the motion triangle')),
      L("The distance goes on top. The speed and the time go at the bottom, side by side.",
        show(m_tr['vals'], 'The distance goes on top')),
      L("Now we cover the one we want. What's left tells us what to do."),
      L("Cover the distance. The speed and the time are left, side by side. So the distance is the speed times the "
        "time.", show(m_tr['cover_top'], 'Cover the distance'), show(m_t1, 'So the distance is the speed times')),
      L("Cover the time. The distance is left, over the speed. So the time is the distance divided by the speed.",
        show(m_tr['cover_right'], 'Cover the time'), show(m_t2, 'So the time is the distance divided')),
      L("And cover the speed. The distance is left, over the time. So the speed is the distance divided by the time.",
        show(m_tr['cover_left'], 'And cover the speed'), show(m_t3, 'So the speed is the distance divided')),
      L("If you know the formula by heart, that's enough. If you need the triangle, here it is.")),
    S('Find the time, find the speed',
      L("Now a new example. A train travels a hundred twenty kilometers at forty kilometers per hour. How long does "
        "the trip take?", show(m_g1, 'A train travels a hundred twenty kilometers')),
      L("They ask for the time. So we cover the time, and the time is the distance divided by the speed.",
        show(m_g2, 'the time is the distance divided by the speed')),
      L("A hundred twenty divided by forty is three, because forty times three is a hundred twenty. So the trip takes "
        "three hours.", show(m_g3, 'A hundred twenty divided by forty')),
      L("Now the other way. A bus travels a hundred fifty kilometers in two hours. What is its speed?",
        show(m_g4, 'A bus travels a hundred fifty kilometers')),
      L("We cover the speed. The speed is the distance divided by the time.", show(m_g5, 'The speed is the distance divided')),
      L("A hundred fifty divided by two is seventy-five. So the bus travels at seventy-five kilometers per hour.",
        show(m_g6, 'A hundred fifty divided by two')),
      L("Let's check it. Seventy-five kilometers in each hour, for two hours, is a hundred fifty. That's the distance "
        "they gave us.", show(m_g7, 'for two hours, is a hundred fifty'))),
]
m_u1 = IH('m_u1', '$1$ km $=1000$ m', size=36)
m_u2 = IH('m_u2', '$1$ hour $=60$ minutes, $\\ 1$ minute $=60$ seconds', size=34)
m_u3 = IH('m_u3', '$30$ minutes $=\\frac{30}{60}=\\frac{1}{2}$ hour', size=34)
m_u4 = IH('m_u4', '$20$ minutes $=\\frac{20}{60}=\\frac{1}{3}$ hour', size=34)
m_ut = TBL('m_ut', ['12 min', '15 min', '20 min', '30 min', '40 min', '45 min'], ['hour'], [
    ('ra', [('c', 0, 2, '1/3'), ('c', 0, 3, '1/2')]),
    ('rb', [('c', 0, 0, '1/5')]), ('rc', [('c', 0, 1, '1/4')]),
    ('rd', [('c', 0, 4, '2/3')]), ('re', [('c', 0, 5, '3/4')])],
    colw=130, labw=110, rowh=64, headh=56, w=920, size=34, title='Minutes as parts of an hour')
m_m1 = I('m_m1', '$60$ kph, $\\ $for $40$ minutes', size=36)
m_m2 = IH('m_m2', '$40$ minutes $=\\frac{2}{3}$ hour', size=34)
m_m3 = IH('m_m3', '$60\\div3=20$', size=34, col=1)
m_m4 = IH('m_m4', '$20\\times2=40$ km', size=34, col=1)
m_m5 = IH('m_m5', '$60\\times40$: $\\ $the trap', size=34, col=1)
m_m6 = IH('m_m6', '$1.25$ hours $=1$ hour $+\\frac{1}{4}$ hour', size=34)
m_m7 = IH('m_m7', '$=1$ hour $15$ minutes, $\\ $not $25$', size=34)
m_c0 = I('m_c0', 'Forget $\\times3.6$. $\\ $Use identical ratios.', size=36)
m_c1 = I('m_c1', '$90$ kph. $\\ $How far in $20$ minutes?', size=36)
m_ct = TBL('m_ct', ['Time', 'Distance'], ['', ''], [
    ('r1', [('c', 0, 0, '60 min'), ('c', 0, 1, '90 km')]),
    ('r2', [('c', 1, 0, '20 min'), ('q', 1, 1)]),
    ('a3', [('down', 0, 0, 1, '÷3')]),
    ('ans', [('cover', 1, 1, '30 km'), ('down', 1, 0, 1, '÷3')])], colw=210, labw=0, rowh=70, side=90, w=640, size=36)
m_c2 = IH('m_c2', '$90\\div3=30$ km', size=34, col=1)
m_r1 = I('m_r1', '$10$ meters a second. $\\ $In kph?', size=36)
m_rt = TBL('m_rt', ['Time', 'Distance'], ['', '', ''], [
    ('r1', [('c', 0, 0, '1 s'), ('c', 0, 1, '10 m')]),
    ('r2', [('c', 1, 0, '60 s'), ('down', 0, 0, 1, '×60')]),
    ('r2b', [('c', 1, 1, '600 m'), ('down', 1, 0, 1, '×60')]),
    ('r3', [('c', 2, 0, '60 min'), ('down', 0, 1, 2, '×60')]),
    ('r3b', [('c', 2, 1, '36000 m'), ('down', 1, 1, 2, '×60')])], colw=220, labw=0, rowh=66, side=100, w=660, size=36)
m_r2 = IH('m_r2', '$10\\times60=600$ m', size=34, col=1)
m_r3 = IH('m_r3', '$600\\times6=3600$', size=34, col=1)
m_r4 = IH('m_r4', '$600\\times60=36000$ m', size=34, col=1)
m_r5 = IH('m_r5', '$36000$ m $=36$ km', size=34, col=1)
m_r6 = I('m_r6', '$36$ kph', size=40, col=1)
_wp106 += [
    S('The same units',
      L("Motion questions love to mix units. So before we calculate, the units must match."),
      L("If the speed is in kilometers per hour, the distance must be in kilometers, and the time in hours."),
      L("One kilometer is a thousand meters.", show(m_u1, 'One kilometer is a thousand meters')),
      L("One hour is sixty minutes, and one minute is sixty seconds. So meters per second means how many meters we "
        "cover in one second.", show(m_u2, 'One hour is sixty minutes')),
      L("Now the most common case. The speed is per hour, but the time is in minutes. So we turn the minutes into "
        "part of an hour."),
      L("Thirty minutes is thirty out of sixty. That's half an hour.", show(m_u3, 'Thirty minutes is thirty out of sixty')),
      L("Twenty minutes is twenty out of sixty. We divide both by twenty, and that's one third of an hour.",
        show(m_u4, 'Twenty minutes is twenty out of sixty')),
      L("In the same way, twelve minutes is a fifth of an hour, and fifteen minutes is a quarter. Forty minutes is two "
        "thirds, and forty-five minutes is three quarters.", show(m_ut['line'], 'In the same way'),
        show(m_ut['ra'], 'In the same way'), show(m_ut['rb'], 'twelve minutes is a fifth'),
        show(m_ut['rc'], 'fifteen minutes is a quarter'), show(m_ut['rd'], 'Forty minutes is two thirds'),
        show(m_ut['re'], 'forty-five minutes is three quarters')),
      L("Take a moment to learn this row by heart. It comes up in almost every motion question.")),
    S('Minutes in a question',
      L("Now a new example. A car drives at sixty kilometers per hour, for forty minutes. How far does it go?",
        show(m_m1, 'A car drives at sixty kilometers per hour')),
      L("The speed is per hour, so the time must be in hours too. Forty minutes is two thirds of an hour.",
        show(m_m2, 'Forty minutes is two thirds of an hour')),
      L("The distance is the speed times the time, so sixty times two thirds. Sixty divided by three is twenty.",
        show(m_m3, 'Sixty divided by three is twenty')),
      L("Then twenty times two is forty. So the car goes forty kilometers.", show(m_m4, 'twenty times two is forty')),
      L("A lot of students write sixty times forty. That mixes hours with minutes, so the answer is far too big.",
        show(m_m5, 'sixty times forty')),
      L("Careful with decimals of an hour too. One point two five hours is one hour and a quarter of an hour.",
        show(m_m6, 'One point two five hours is one hour and a quarter')),
      L("A quarter of an hour is fifteen minutes. So one point two five hours is one hour and fifteen minutes, not one "
        "hour and twenty-five.", show(m_m7, 'So one point two five hours is one hour and fifteen'))),
    S('Changing the units of a speed',
      L("Sometimes we need to change the units of a speed. Some books teach a rule. To go from meters per second to "
        "kilometers per hour, multiply by three point six."),
      L("You can forget that rule. It almost never comes up on the exam, and almost nobody remembers whether to "
        "multiply or to divide.", show(m_c0, 'You can forget that rule')),
      L("Instead, we use identical ratios, like in topic twenty-two. If we multiply the time by some number, the "
        "distance is multiplied by the same number."),
      L("Now a new example. A car drives at ninety kilometers per hour. How far does it go in twenty minutes?",
        show(m_c1, 'A car drives at ninety kilometers per hour')),
      L("One hour is sixty minutes. So the car goes ninety kilometers in sixty minutes.",
        show(m_ct['line'], 'So the car goes ninety kilometers'), show(m_ct['r1'], 'So the car goes ninety kilometers')),
      L("We want twenty minutes. From sixty minutes to twenty minutes, we divide by three.",
        show(m_ct['r2'], 'We want twenty minutes'), show(m_ct['a3'], 'we divide by three')),
      L("So we divide the distance by three too. Ninety divided by three is thirty. So in twenty minutes the car goes "
        "thirty kilometers.", show(m_c2, 'Ninety divided by three is thirty'), show(m_ct['ans'], 'the car goes thirty kilometers'))),
    S('A speed in meters per second',
      L("Now the other way. A runner runs ten meters every second. What is his speed in kilometers per hour?",
        show(m_r1, 'A runner runs ten meters every second')),
      L("We write ten meters in one second. Then we grow the time, one step at a time.",
        show(m_rt['line'], 'We write ten meters in one second'), show(m_rt['r1'], 'We write ten meters in one second')),
      L("From one second to one minute, the time is times sixty, because a minute is sixty seconds.",
        show(m_rt['r2'], 'From one second to one minute')),
      L("So the distance is times sixty too. Ten times sixty is six hundred meters in one minute.",
        show(m_r2, 'Ten times sixty is six hundred'), show(m_rt['r2b'], 'six hundred meters in one minute')),
      L("From one minute to one hour, the time is times sixty again.", show(m_rt['r3'], 'From one minute to one hour')),
      L("So six hundred times sixty. Six hundred times six is three thousand six hundred. So six hundred times sixty is "
        "thirty-six thousand meters in one hour.", show(m_r3, 'Six hundred times six is three thousand'),
        show(m_r4, 'So six hundred times sixty is thirty-six thousand'), show(m_rt['r3b'], 'thirty-six thousand meters in one hour')),
      L("A thousand meters is one kilometer, so thirty-six thousand meters is thirty-six kilometers.",
        show(m_r5, 'thirty-six thousand meters is thirty-six kilometers')),
      L("So his speed is thirty-six kilometers per hour.", show(m_r6, 'So his speed is thirty-six')),
      L("So when a speed comes in other units, don't look for a rule. Change the time step by step, and change the "
        "distance in the same way.")),
]
m_tb = TBL('m_tb', ['Speed', 'Distance', 'Time'], ['part 1', 'part 2', 'total'], [
    ('r1a', [('c', 0, 0, '15'), ('c', 0, 2, '2')]), ('r1b', [('c', 0, 1, '30')]),
    ('r2a', [('c', 1, 0, '10'), ('c', 1, 1, '20')]), ('r2b', [('c', 1, 2, '2')]),
    ('t1', [('c', 2, 1, '50')]), ('t2', [('c', 2, 2, '4')]), ('t3', [('c', 2, 0, 'no sum', _RED27)])],
    colw=160, labw=140, rowh=64, headh=56, w=700, size=36)
m_b1 = IH('m_b1', '$15\\times2=30$ km', size=32, col=1)
m_b2 = IH('m_b2', '$20\\div10=2$ hours', size=32, col=1)
m_b3 = IH('m_b3', '$30+20=50$ km', size=32, col=1)
m_b4 = IH('m_b4', '$2+2=4$ hours', size=32, col=1)
m_b5 = IH('m_b5', '$15+10$: $\\ $not a speed', size=32, col=1)
m_b6 = I('m_b6', 'The link: $\\ $equal times, equal distances, or a total', size=34)
m_sk = ROAD('m_sk', [
    ('ends', [('end', 0, 'town A'), ('end', 1, 'town B')]),
    ('dots', [('dot', 0, 'Dan 8:00'), ('dot', 1, 'Eli 9:00', 'orange')]),
    ('arr', [('arrow', 0, .3, '40 kph'), ('arrow', 1, .7, '60 kph', 0, 'orange')]),
    ('gap', [('gap', 0, 1, 'initial gap: 100 km')]),
    ('meet', [('meet', .64, 'they meet')])], w=900)
m_p0 = RTRI('m_p0', [('height', [('height', 'height'), ('right',)]), ('path', [('path', 'the path')]), ('ground', [('ground', 'the ground')])], w=600)
m_p1 = IH('m_p1', '$a^2+b^2=c^2$', size=38)
m_p2 = IH('m_p2', '$3^2+4^2=9+16=25=5^2$', size=34)
m_s1 = I('m_s1', 'Distance $=$ speed $\\times$ time: $\\ $cover the one you want', size=34)
m_s2 = I('m_s2', 'The units match. $\\ $Minutes are parts of an hour.', size=34)
m_s3 = I('m_s3', 'A speed in other units: $\\ $identical ratios', size=34)
m_s4 = I('m_s4', 'The table: $\\ $add distances and times, never speeds', size=34)
m_s5 = I('m_s5', 'Always draw a sketch.', size=34)
_wp106 += [
    S('The table',
      L("Many motion questions have two travelers, or one trip in two parts. We organize them in a table."),
      L("The table has three columns, speed, distance and time. The distance goes in the middle, because the distance "
        "is the speed times the time.", show(m_tb['line'], 'The table has three columns')),
      L("It's like the work table, team, work and time. Each traveler, or each part of the trip, gets its own row."),
      L("Now a new example. A cyclist rides two hours at fifteen kilometers per hour."),
      L("That's part one. The speed is fifteen, and the time is two hours.", show(m_tb['r1a'], 'The speed is fifteen')),
      L("The distance is the speed times the time. Fifteen times two is thirty kilometers.",
        show(m_b1, 'Fifteen times two is thirty'), show(m_tb['r1b'], 'is thirty kilometers')),
      L("Then she rides twenty kilometers at ten kilometers per hour. That's part two.",
        show(m_tb['r2a'], 'Then she rides twenty kilometers')),
      L("The time is the distance divided by the speed. Twenty divided by ten is two hours.",
        show(m_b2, 'Twenty divided by ten'), show(m_tb['r2b'], 'is two hours')),
      L("So in every row, the distance is the speed times the time. When we know two boxes, the row gives us the "
        "third."),
      L("Now the whole trip. We add a total row."),
      L("The distances add up. Thirty plus twenty is fifty kilometers.", show(m_b3, 'Thirty plus twenty is fifty'),
        show(m_tb['t1'], 'is fifty kilometers')),
      L("The times add up too. Two plus two is four hours.", show(m_b4, 'Two plus two is four'),
        show(m_tb['t2'], 'is four hours')),
      L("But the speeds don't add up. Fifteen plus ten is not her speed on the whole trip. We'll see why in the "
        "average-speed lesson.", show(m_b5, 'Fifteen plus ten is not'), show(m_tb['t3'], 'is not her speed')),
      L("Then we look for the link the question gives us. Equal times, equal distances, or a total.",
        show(m_b6, 'Equal times, equal distances, or a total')),
      L("For example, if two travelers ride for the same time, we write their two times as equal. That gives us the equation.")),
    S('Draw a sketch',
      L("And in every motion question, draw a sketch. It takes a few seconds, and it shows what really happens."),
      L("Let's build an example sketch without solving it yet. Dan leaves town A at eight, at forty kilometers per hour. Eli leaves town B at nine, at sixty. The towns are a hundred kilometers apart."),
      L("Draw the road, and mark where it starts and ends.", show(m_sk['line'], 'Draw the road'),
        show(m_sk['ends'], 'mark where it starts and ends')),
      L("Put a dot for each traveler, and write the time each one starts.", show(m_sk['dots'], 'Put a dot for each traveler')),
      L("Draw an arrow for each direction, and write the speed on it.", show(m_sk['arr'], 'Draw an arrow for each direction')),
      L("Mark the initial distance between the towns, a hundred kilometers. That's the gap before anyone moves.",
        show(m_sk['gap'], 'Mark the initial distance between the towns')),
      L("And when they meet, mark the meeting point. We'll solve questions like this one in the relative speed "
        "lesson.", show(m_sk['meet'], 'mark the meeting point'))),
    S('Directions at an angle',
      L("Sometimes the directions are not on one line. A plane climbs at an angle. Or one person walks north, and "
        "another walks west."),
      L("For the plane climbing above level ground, the sketch is a right triangle.", show(m_p0['line'], 'the sketch is a right triangle')),
      L("The vertical height and the horizontal ground meet at a right angle. They are the two legs. The sloping path is the hypotenuse, the longest side.",
        show(m_p0['height'], 'The vertical height'), show(m_p0['ground'], 'and the horizontal ground'),
        show(m_p0['path'], 'The sloping path')),
      L("Remember Pythagoras, from topic thirty-one. We call the two short sides a and b, and the long side c. Then a "
        "squared plus b squared is equal to c squared.", show(m_p1, 'Then a squared plus b squared')),
      L("For example, short sides three and four. Three squared is nine, and four squared is sixteen. Nine plus sixteen is "
        "twenty-five, and twenty-five is five squared. "
        "So the long side is five.", show(m_p2, 'Nine plus sixteen is twenty-five')),
      L("So when the directions are different, draw a sketch. Use Pythagoras only if the triangle has a right angle. Here, speed times time gives the path along the slope, not the height.")),
    S('Recap',
      L("So let's sum it up. Distance is equal to speed times time. In the triangle, cover the one you want.",
        show(m_s1, 'Distance is equal to speed times time')),
      L("The units must match, and minutes become parts of an hour.", show(m_s2, 'The units must match')),
      L("To change the units of a speed, use identical ratios. Change the time, and the distance in the same way.",
        show(m_s3, 'To change the units of a speed')),
      L("Two travelers, or two parts? Make a table. Add the distances and the times, but never the speeds.",
        show(m_s4, 'Make a table')),
      L("And always draw a sketch.", show(m_s5, 'And always draw a sketch')),
      L("Take a moment to memorize this. Now try the first question, and I'll see you in the next video.")),
]
video('wp-106', 'lesson', slides=_wp106)
CAMERA_SPLIT = ('wp-106', 'Distance, Speed and Time', [
    (1, None),
    (5, "Let's continue with motion, and look at the units."),
    (9, "Let's continue, with two tools that help in every motion question.")])

# ------------------------------------------------------------------------------------------------ g107 (the e-scooter)
# Hebrew (wp 7041-7076, the walker 5 m/s, km in half an hour): identical ratios, 1 s -> 1 min (x60) -> 30 min (x30),
# "better than memorising 3.6". English: 6 m/s, 50 minutes, km. First question of the topic: identical ratios (camera
# lesson part 2) applied slowly, "like in the lesson", on new numbers (the lesson used 90 kph -> 20 min and 10 m/s ->
# kph). x50 said as x100, then half (R36). Trap at its step: 0.3 = 6 x 50 m (seconds mixed with minutes).
g7t = TBL('g7t', ['Time', 'Distance'], ['', '', ''], [
    ('r1', [('c', 0, 0, '1 s'), ('c', 0, 1, '6 m')]),
    ('r2', [('c', 1, 0, '1 min'), ('down', 0, 0, 1, '×60')]),
    ('r2b', [('c', 1, 1, '360 m'), ('down', 1, 0, 1, '×60')]),
    ('r3', [('c', 2, 0, '50 min'), ('down', 0, 1, 2, '×50')]),
    ('r3b', [('c', 2, 1, '18000 m'), ('down', 1, 1, 2, '×50')])], colw=200, labw=0, rowh=58, headh=50, side=90, w=520, size=30)
g7a = IH('g7a', '$6\\times50=300$ m: $\\ $the trap', size=30, col=1)
g7b = IH('g7b', '$6\\times60=360$ m', size=30, col=1)
g7c = IH('g7c', '$360\\times100=36000$', size=30, col=1)
g7d = IH('g7d', '$36000\\div2=18000$ m', size=30, col=1)
g7e = IH('g7e', '$18000$ m $=18$ km', size=30, col=1)
video('solve-wp27-g107', 'solution', qid='wp27-g107', slides=[
    S('Method 1 · The math way: identical ratios',
      L("An electric scooter moves at six meters per second. How many kilometers does it travel in fifty minutes?",
        pt('stem', 'An electric scooter moves', 'hl', 5.0), voice='calm', pause=0.5),
      L("So the speed is in meters per second, but they ask for kilometers, after fifty minutes. The units don't "
        "match.", pt('stem: ask', 'but they ask for kilometers')),
      L("Let's solve it the math way, with identical ratios, like in the lesson. We change the time step by step, and "
        "the distance in the same way.", show(g7t['line'], 'with identical ratios')),
      L("We start from the given. The scooter goes six meters in one second.", show(g7t['r1'], 'The scooter goes six meters')),
      L("Careful here. A lot of students multiply six by fifty right away. But six meters is for one second, and fifty "
        "is minutes.", show(g7a, 'multiply six by fifty')),
      L("That gives three hundred meters, which is zero point three kilometers, choice number one. It mixes seconds "
        "with minutes.", mk('cross', 'choice 1', 'It mixes seconds')),
      L("So first, from one second to one minute. The time is times sixty, because a minute is sixty seconds.",
        show(g7t['r2'], 'from one second to one minute')),
      L("So the distance is times sixty too. Six times sixty is three hundred sixty meters in one minute.",
        show(g7b, 'Six times sixty'), show(g7t['r2b'], 'three hundred sixty meters in one minute')),
      L("Now from one minute to fifty minutes. The time is times fifty, so the distance is times fifty too.",
        show(g7t['r3'], 'from one minute to fifty minutes')),
      L("Times fifty is times a hundred, and then half. Three hundred sixty times a hundred is thirty-six thousand.",
        show(g7c, 'Three hundred sixty times a hundred')),
      L("Half of thirty-six thousand is eighteen thousand. So in fifty minutes the scooter goes eighteen thousand "
        "meters.", show(g7d, 'Half of thirty-six thousand'), show(g7t['r3b'], 'eighteen thousand meters')),
      L("They ask for kilometers. A thousand meters is one kilometer. So eighteen thousand meters is eighteen "
        "kilometers.", show(g7e, 'eighteen thousand meters is eighteen')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g108 (the gondola lift)
# Hebrew (wp 7077-7116, the plane 300 kph, 1 minute, ground 4 km): the distance in the time first (÷60), the sketch,
# drop a perpendicular, 3-4-5 -> 3; "when the directions differ, draw". English: 17 kph, 6 minutes, ground 1.5 km.
# Two methods: Pythagoras with the shortcut a² - b² = (a - b)(a + b) (topic 4; R36: no 17² by heart), and her move, a
# known triple (8, 15, 17, said honestly as "if you know it"). Pythagoras and the triple are REMINDERS (topic 31). The
# path first, at the step: "1.7 is not our final answer yet" (choice 1 is the path).
g8r = RTRI('g8r', [('height', [('height', '?'), ('right',)]), ('path', [('path', '1.7 km')]), ('ground', [('ground', '1.5 km')])], w=540, col=1)
g8a = IH('g8a', '$6$ minutes $=\\frac{6}{60}=\\frac{1}{10}$ hour', size=30)
g8b = IH('g8b', '$17\\times\\frac{1}{10}=1.7$ km', size=30)
g8c = IH('g8c', '$1.7$ km: $\\ $the path, $\\ $not the height', size=30)
g8d = IH('g8d', 'in tenths: $\\ 17$ and $15$', size=30)
g8e = IH('g8e', '$h^2+15^2=17^2$', size=30)
g8f = IH('g8f', '$h^2=17^2-15^2$', size=30)
g8g = IH('g8g', '$=(17-15)(17+15)$', size=30)
g8h = IH('g8h', '$=2\\times32=64$', size=30, col=1)
g8i = IH('g8i', '$h=8$ tenths $=0.8$ km', size=30, col=1)
g8j = IH('g8j', '$1.7$ km $=17$ tenths', size=30)
g8k = IH('g8k', '$8,\\ 15,\\ 17$', size=32)
g8l = IH('g8l', '$64+225=289=17^2$', size=30)
video('solve-wp27-g108', 'solution', qid='wp27-g108', slides=[
    S('Method 1 · The math way: Pythagoras',
      L("A gondola lift climbs along a straight cable at seventeen kilometers per hour. After six minutes, its "
        "horizontal distance from the bottom station is one point five kilometers. How high above the bottom station "
        "is it, in kilometers?", pt('stem', 'A gondola lift climbs', 'hl', 12.0), voice='calm', pause=0.5),
      L("So the gondola climbs at an angle, and they ask for its height. The directions are not on one line, so we "
        "draw a right triangle, like in the lesson.", pt('stem: ask', 'they ask for its height')),
      L("We'll solve it in two different ways. Let's start with the math way. First we find how far the gondola really "
        "moves, along the cable."),
      L("The speed is per hour, but the time is in minutes. Six minutes is six out of sixty, a tenth of an hour.",
        show(g8a, 'Six minutes is six out of sixty')),
      L("The distance is the speed times the time. Seventeen times a tenth is one point seven kilometers.",
        show(g8b, 'Seventeen times a tenth')),
      L("Careful, one point seven is choice number one, but it's not our final answer. It's the path along the cable, "
        "not the height.", show(g8c, "It's the path along the cable"), mk('cross', 'choice 1', 'not the height'))),
    S('Method 1 · The math way: Pythagoras',
      L("Now the sketch, the right triangle.", show(g8r['line'], 'Now the sketch')),
      L("The path along the cable is the long side, one point seven.", show(g8r['path'], 'The path along the cable is the long side')),
      L("The ground is one point five. And the height is the side we need.", show(g8r['ground'], 'The ground is one point five'),
        show(g8r['height'], 'And the height is the side')),
      L("Let's count in tenths of a kilometer, so the numbers are whole. One point seven is seventeen tenths, and one "
        "point five is fifteen tenths.", show(g8d, 'Let\'s count in tenths')),
      L("Pythagoras says the height squared plus fifteen squared is equal to seventeen squared.", show(g8e, 'Pythagoras says')),
      L("So the height squared is seventeen squared minus fifteen squared.", show(g8f, 'So the height squared is seventeen')),
      L("Remember the shortcut from topic four. A difference of two squares is the difference of the numbers, times "
        "their sum.", show(g8g, 'A difference of two squares')),
      L("Seventeen minus fifteen is two, and seventeen plus fifteen is thirty-two. Two times thirty-two is sixty-four.",
        show(g8h, 'Two times thirty-two')),
      L("So the height squared is sixty-four, and the height is eight tenths of a kilometer. That's zero point eight.",
        show(g8i, 'the height is eight tenths'))),
    S('Method 2 · Understanding: a known triple',
      L("[pause] Now by understanding, with a known triple. It's the same first step. The path along the cable is "
        "one point seven kilometers, seventeen tenths.", show(g8j, 'seventeen tenths')),
      L("The ground is fifteen tenths. And fifteen and seventeen belong to the triple eight, fifteen, seventeen, just "
        "like three, four, five.", show(g8k, 'the triple eight, fifteen, seventeen')),
      L("Why is it a triple? Eight squared is sixty-four, and fifteen squared is two hundred twenty-five. Together "
        "that's two hundred eighty-nine, and that's seventeen squared.", show(g8l, 'Together that')),
      L("You don't have to know this triple by heart. But if you know it, the height is eight tenths right away."),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-108-after (lesson: average speed)
# Hebrew (wp 7117-7147, 7149-7204): the hand across the notebook (slow, fast, slow, stop); average speed = the ONE constant
# speed for the whole trip; total distance / total time, "I don't care what the speed was at the start, the middle or
# the end"; NOT the average of the speeds; rare on the exam (teacher decision: the line stays), but it hides in "if it had
# moved at a constant speed"; the slow part takes more time, so the answer is nearer the slow speed (the weighted-average
# reminder); no distance given -> a friendly one (her 120 for 60 and 40); only total / total (teacher decision
# 2026-10-08: no 2ab/(a+b), no weighted-average method). English: total / total in the table (24 km in 2 h + 6 km in
# 1 h -> 10, not 9); a stop counts as time (120 + 60 km, a 1-hour stop -> 45, not 60); there at 120, back at 60 with a
# friendly 120 km -> 80, not 90; equal TIMES -> the plain average (1 h at 40 + 1 h at 80 -> 60; real-exam audit A7);
# "equal distances or equal times?". Numbers differ from g109 (105 / 70), q-r26-t27-21 / -22 and the Hebrew (60 / 40).
v8f = I('v8f', 'Average speed $=\\dfrac{\\text{total distance}}{\\text{total time}}$', size=42)
v8meaning = I('v8meaning', 'Average speed: $\\ $one constant speed for the same distance in the same total time', size=36)
v8t = TBL('v8t', ['Speed', 'Distance', 'Time'], ['part 1', 'part 2', 'total'], [
    ('r1', [('c', 0, 0, '12'), ('c', 0, 1, '24'), ('c', 0, 2, '2')]),
    ('r2', [('c', 1, 0, '6'), ('c', 1, 1, '6'), ('c', 1, 2, '1')]),
    ('t1', [('c', 2, 1, '30')]), ('t2', [('c', 2, 2, '3')]), ('t3', [('c', 2, 0, '10', _TEAL)])],
    colw=160, labw=140, rowh=62, headh=54, w=700, size=36)
v8a = IH('v8a', '$24+6=30$ km', size=32, col=1)
v8b = IH('v8b', '$2+1=3$ hours', size=32, col=1)
v8c = IH('v8c', '$30\\div3=10$ kph', size=32, col=1)
v8d = IH('v8d', '$\\frac{12+6}{2}=9$: $\\ $not the answer', size=32, col=1)
v8s0 = I('v8s0', '$120$ km in $2$ h, $\\ $a stop of $1$ h, $\\ 60$ km in $1$ h', size=34)
v8s1 = IH('v8s1', '$120+60=180$ km', size=32)
v8s2 = IH('v8s2', '$2+1+1=4$ hours', size=32)
v8s3 = IH('v8s3', '$180\\div4=45$ kph', size=32)
v8s4 = IH('v8s4', 'no stop: $\\ 180\\div3=60$', size=32)
v8n0 = I('v8n0', 'There at $120$ kph, $\\ $back at $60$ kph', size=34)
v8n1 = IH('v8n1', '$\\frac{120+60}{2}=90$?', size=32)
v8n2 = IH('v8n2', 'pick $120$ km each way', size=32)
v8n3 = IH('v8n3', 'there: $\\ 120\\div120=1$ hour', size=32, col=1)
v8n4 = IH('v8n4', 'back: $\\ 120\\div60=2$ hours', size=32, col=1)
v8n5 = IH('v8n5', '$240$ km in $3$ hours', size=32, col=1)
v8n6 = IH('v8n6', '$240\\div3=80$ kph, $\\ $not $90$', size=32, col=1)
v8q0 = I('v8q0', '$1$ hour at $40$, $\\ 1$ hour at $80$', size=34)
v8q1 = IH('v8q1', '$40+80=120$ km', size=32)
v8q2 = IH('v8q2', '$120\\div2=60$ kph', size=32)
v8q3 = IH('v8q3', '$\\frac{40+80}{2}=60$: $\\ $the same', size=32)
v8q4 = I('v8q4', 'Equal times: $\\ $the plain average works', size=34)
v8q5 = I('v8q5', 'Equal distances: $\\ $closer to the slower speed', size=34)
v8r1 = I('v8r1', 'Total distance $\\div$ total time. $\\ $Stops count as time.', size=34)
v8r2 = I('v8r2', 'Ordinary average of speeds: $\\ $only for equal times', size=34)
v8r3 = I('v8r3', 'First ask: $\\ $equal distances, or equal times?', size=34)
v8r4 = I('v8r4', 'No distance given? $\\ $Pick a friendly one.', size=34)
video('wp-108-after', 'lesson', slides=[
    S('Average Speed',
      L("Welcome back. Now average speed."),
      L("Honestly, it's rare on the exam. But the idea behind it shows up in other words, and it hides a classic trap. "
        "So let's understand it properly.")),
    S('What it means',
      L("Imagine moving your hand across a page. Move slowly, then quickly, then slowly again, and stop."),
      L("The hand's speed kept changing. So what is its average speed?"),
      L("The average speed is the one constant speed that covers the same distance in the same time.",
        show(v8meaning, 'The average speed is the one constant speed')),
      L("The exam may not say average speed. It may say, if it had moved at a constant speed. That's the same thing.")),
    S('Total distance over total time',
      L("Here is how we find it. The average speed is the total distance divided by the total time.",
        show(v8f, 'The average speed is the total distance divided')),
      L("We don't care how fast we went in each part. We only ask, how far in total, and how long in total."),
      L("Now a new example. A runner runs twenty-four kilometers in two hours, at twelve kilometers per hour. Then she "
        "runs six more kilometers in one hour, at six kilometers per hour.", show(v8t['line'], 'Now a new example'),
        show(v8t['r1'], 'A runner runs twenty-four kilometers'), show(v8t['r2'], 'Then she runs six more kilometers')),
      L("The total distance is twenty-four plus six, thirty kilometers.", show(v8a, 'twenty-four plus six'),
        show(v8t['t1'], 'thirty kilometers')),
      L("The total time is two plus one, three hours.", show(v8b, 'two plus one'), show(v8t['t2'], 'three hours')),
      L("So the average speed is thirty divided by three, ten kilometers per hour.", show(v8c, 'thirty divided by three'),
        show(v8t['t3'], 'ten kilometers per hour')),
      L("And the middle of twelve and six is nine, not ten. So here, adding the two speeds and halving them gives a wrong answer.",
        show(v8d, 'the middle of twelve and six is nine'))),
    S('A stop counts as time',
      L("Now a new example, with a stop. A bus drives a hundred twenty kilometers in two hours. Then it stops for one "
        "hour. Then it drives sixty more kilometers in one hour.", show(v8s0, 'A bus drives a hundred twenty kilometers')),
      L("The total distance is a hundred twenty plus sixty, a hundred eighty kilometers.",
        show(v8s1, 'a hundred twenty plus sixty')),
      L("The total time includes the stop, because the trip includes it. Two plus one plus one is four hours.",
        show(v8s2, 'Two plus one plus one')),
      L("A hundred eighty divided by four is forty-five. So the average speed is forty-five kilometers per hour.",
        show(v8s3, 'A hundred eighty divided by four')),
      L("Without the stop, it would be a hundred eighty divided by three, sixty. So the stop matters.",
        show(v8s4, 'it would be a hundred eighty divided by three'))),
    S('Not the average of the speeds',
      L("And here's the big trap. The average speed is not the average of the two speeds. At least, not necessarily."),
      L("Now a new example. A car drives to a town at a hundred twenty kilometers per hour. It comes back on the same "
        "road at sixty.", show(v8n0, 'A car drives to a town')),
      L("Most students say ninety, the middle of a hundred twenty and sixty. Let's check it.",
        show(v8n1, 'Most students say ninety')),
      L("The distance isn't given, so we pick a friendly one, a number that both speeds divide. Let's say a hundred "
        "twenty kilometers each way.", show(v8n2, 'a hundred twenty kilometers each way')),
      L("There, a hundred twenty kilometers at a hundred twenty kilometers per hour takes one hour.",
        show(v8n3, 'There, a hundred twenty kilometers')),
      L("Back, a hundred twenty kilometers at sixty takes two hours.", show(v8n4, 'Back, a hundred twenty kilometers')),
      L("So the car drives two hundred forty kilometers in three hours.", show(v8n5, 'two hundred forty kilometers in three')),
      L("Two hundred forty divided by three is eighty. So the average speed is eighty, not ninety.",
        show(v8n6, 'Two hundred forty divided by three')),
      L("Why is it lower? The two distances are equal, but the slow part takes more time. So the car spends more time "
        "at sixty, and that pulls the average toward sixty."),
      L("Remember weighted averages, from topic twenty-five? The bigger group pulls the average toward it. Here, the "
        "longer time does the pulling.")),
    S('Equal times',
      L("Now a different case. A car drives one hour at forty kilometers per hour, and then one more hour at eighty.",
        show(v8q0, 'A car drives one hour at forty')),
      L("The total distance is forty plus eighty, a hundred twenty kilometers.", show(v8q1, 'forty plus eighty')),
      L("The total time is two hours. So the average speed is a hundred twenty divided by two, sixty.",
        show(v8q2, 'a hundred twenty divided by two')),
      L("And sixty is exactly the middle of forty and eighty.", show(v8q3, 'exactly the middle of forty and eighty')),
      L("Why? Each speed lasts one hour. So we add forty and eighty kilometers, then divide by two hours. That is exactly the ordinary average of the speeds."),
      L("So before we calculate, we ask, equal distances or equal times? With equal times, the plain average works.",
        show(v8q4, 'With equal times')),
      L("With equal distances, the answer is closer to the slower speed.", show(v8q5, 'With equal distances'))),
    S('Recap',
      L("So let's sum it up. The average speed is the total distance divided by the total time. And a stop counts as "
        "time.", show(v8r1, 'The average speed is the total distance')),
      L("Don't simply average the speeds unless the two travel times are equal.", show(v8r2, "Don't simply average the speeds")),
      L("First ask, equal distances, or equal times?", show(v8r3, 'First ask')),
      L("And if the distance is missing, pick a friendly number.", show(v8r4, 'if the distance is missing')),
      L("Now try the next question, and I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ g109 (city and coast)
# Hebrew (wp 7149-7204, Dimona - Be'er Sheva 60 / 40): not 50 - logic first (less time at 60, so closer to 40; the
# weighted-average reminder); no formula; the distance missing -> plug in 120 (divides by both) rather than x; 240 / 5
# = 48. English: 105 / 70; the logic rules out 90 and 87.5 (her first step), a friendly 210 km -> 84. Method 2 (the
# algebra with d, an English addition the teacher kept 2026-10-08) shows why any distance works. First question after
# the lesson: total / total and the friendly distance applied with "like in the lesson".
g9a = IH('g9a', 'more time at $70$: $\\ $closer to $70$', size=30)
g9b = IH('g9b', 'below $87.5$', size=30)
g9c = IH('g9c', 'pick $210$ km', size=30)
g9c2 = IH('g9c2', '$105\\times2=210$, $\\ 70\\times3=210$', size=30)
g9d = IH('g9d', 'there: $\\ 210\\div105=2$ hours', size=30, col=1)
g9e = IH('g9e', 'back: $\\ 210\\div70=3$ hours', size=30, col=1)
g9f = IH('g9f', '$420$ km in $5$ hours', size=30, col=1)
g9g = IH('g9g', '$420\\div5=84$ kph', size=30, col=1)
g9h = IH('g9h', 'each way $d$: $\\ $total distance $2d$', size=30)
g9i = IH('g9i', 'time: $\\ \\frac{d}{105}+\\frac{d}{70}$', size=30)
g9j = IH('g9j', '$=\\frac{2d}{210}+\\frac{3d}{210}=\\frac{5d}{210}=\\frac{d}{42}$', size=30)
g9k = IH('g9k', '$2d\\div\\frac{d}{42}=2d\\times\\frac{42}{d}$', size=30, col=1)
g9l = IH('g9l', '$=2\\times42=84$', size=30, col=1)
video('solve-wp27-g109', 'solution', qid='wp27-g109', slides=[
    S('Method 1 · Plugging in numbers: a friendly distance',
      L("A car drives from a city to the coast at a hundred five kilometers per hour. It returns along the same road at "
        "seventy, without stopping. What is its average speed for the whole round trip?",
        pt('stem', 'A car drives from a city', 'hl', 10.0), voice='calm', pause=0.5),
      L("So the two ways have the same distance, and they ask for the average speed. That's the trap the lesson warned "
        "us about.", pt('stem: ask', 'they ask for the average speed')),
      L("We'll solve it in two different ways. First, plugging in numbers. But before we calculate, let's think, like "
        "in the lesson."),
      L("It's not eighty-seven and a half, the plain average of a hundred five and seventy. The distances are equal, so "
        "the slow way takes more time.", mk('cross', 'choice 3', "It's not eighty-seven and a half")),
      L("More time at seventy pulls the average toward seventy. So the answer is closer to seventy.",
        show(g9a, 'More time at seventy')),
      L("So the answer is below eighty-seven and a half. Ninety is out too.", show(g9b, 'below eighty-seven and a half'),
        mk('cross', 'choice 1', 'Ninety is out too'))),
    S('Method 1 · Plugging in numbers: a friendly distance',
      L("Now we calculate. The distance isn't given, so we pick a friendly one. Two hundred ten kilometers works, because "
        "a hundred five times two is two hundred ten, and seventy times three is two hundred ten.",
        show(g9c, 'Two hundred ten kilometers works'), show(g9c2, 'a hundred five times two')),
      L("There, two hundred ten kilometers at a hundred five takes two hours.", show(g9d, 'There, two hundred ten')),
      L("Back, two hundred ten kilometers at seventy takes three hours.", show(g9e, 'Back, two hundred ten')),
      L("So the total is four hundred twenty kilometers in five hours.", show(g9f, 'four hundred twenty kilometers in five')),
      L("The total distance divided by the total time is four hundred twenty divided by five, eighty-four. So the average "
        "speed is eighty-four kilometers per hour.", show(g9g, 'four hundred twenty divided by five'))),
    S('Method 2 · The math way: a letter for the distance',
      L("[pause] Now the math way, with a letter instead of a number. We start again from the givens. Let's call the "
        "distance each way d. So the total distance is two d.", show(g9h, 'So the total distance is two d')),
      L("The time there is d divided by a hundred five. The time back is d divided by seventy.", show(g9i, 'The time there')),
      L("To add these fractions, we need a common denominator. A hundred five times two is two hundred ten, and seventy "
        "times three is two hundred ten."),
      L("So we have two d over two hundred ten, plus three d over two hundred ten. That's five d over two hundred ten, "
        "and that's d over forty-two.", show(g9j, 'So we have two d over two hundred ten')),
      L("Now the total distance divided by the total time. Two d divided by d over forty-two is two d times forty-two "
        "over d.", show(g9k, 'Two d divided by d over forty-two')),
      L("The d on top and the d at the bottom cancel. Two times forty-two is eighty-four. The same answer.",
        show(g9l, 'Two times forty-two is eighty-four')),
      L("The d cancels, and that's why plugging in works. Any distance we pick gives the same average speed."),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-110 (lesson: speed ratios)
# Hebrew (wp 7206-7242): some motion questions need no calculation; ratios run through the whole quantitative section;
# the same direct / inverse rules as in work; time fixed -> speed and distance direct ("I have one hour to run"); speed
# fixed -> time and distance direct; distance fixed -> time and speed inverse ("from my house to a friend's"); "the
# skill is spotting when to use them". Her two sample questions (Dani / Dina, Yaron / Moti) carry the meeting in ratio
# parts. R37 (the core of g111, g112, q-r26-t27-31, g118, g120, q-r26-t27-05): each rule on numbers (8 / 12 kph for one
# hour; 10 kph for 1, 2, 3 hours; 12 km at 4 and at 6 kph -> 3 and 2 hours, why: speed x time stays 12); what is
# fixed (four quick situations); part 2: a meeting in ratio parts (10 and 20 kph on a 90 km road -> 1 : 2 -> a third;
# checked), and the V with distance in the middle (the V itself: REMINDER from topic 26; A 3x as fast for half as long,
# 90 km -> 60). The "not a meeting" contrast (the whole is the fast one's parts) is g112's own idea, taught there.
r0a = I('r0a', 'Time fixed: $\\ $speed and distance, $\\ $the same way', size=34)
r0b = IH('r0b', '$1$ hour at $8$ kph: $\\ 8$ km', size=32)
r0c = IH('r0c', '$1$ hour at $12$ kph: $\\ 12$ km', size=32)
r0d = IH('r0d', 'speeds $2:3$ $\\ \\to\\ $ distances $2:3$', size=32)
r1a = I('r1a', 'Speed fixed: $\\ $time and distance, $\\ $the same way', size=34)
r1b = IH('r1b', '$10$ kph: $\\ 1$ hour $10$ km, $\\ 2$ hours $20$ km', size=32)
r1c = IH('r1c', '$3$ hours $30$ km', size=32)
r2a = I('r2a', 'Distance fixed: $\\ $speed and time, $\\ $opposite ways', size=34)
r2b = IH('r2b', '$12$ km at $4$ kph: $\\ 12\\div4=3$ hours', size=32)
r2c = IH('r2c', '$12$ km at $6$ kph: $\\ 12\\div6=2$ hours', size=32)
r2d = IH('r2d', 'speeds $4:6=2:3$, $\\ $times $3:2$', size=32, col=1)
r2e = IH('r2e', '$4\\times3=12$, $\\ 6\\times2=12$', size=32, col=1)
r3a = I('r3a', 'What is fixed?', size=40)
r3b = I('r3b', 'The same three hours for both: $\\ $time', size=32)
r3c = I('r3c', 'The same road there and back: $\\ $distance', size=32)
r3d = I('r3d', 'They start together and stop together: $\\ $time', size=32)
r3e = I('r3e', 'The same speed all day: $\\ $speed', size=32)
_wp110 = [
    S('Speed Ratios',
      L("Welcome back. Now speed ratios."),
      L("Some motion questions need almost no calculation. We only need ratios, the same way and opposite ways."),
      L("Ratios run through the whole quantitative section. And in motion, they save a lot of work.")),
    S('The same time',
      L("These rules are just like the ones in work and rate. First, when the time is fixed, the speed and the distance "
        "go the same way.", show(r0a, 'when the time is fixed')),
      L("Say I have one hour to run. At eight kilometers per hour, I cover eight kilometers.", show(r0b, 'At eight kilometers per hour')),
      L("At twelve kilometers per hour, I cover twelve kilometers. The faster I run, the farther I get.",
        show(r0c, 'At twelve kilometers per hour')),
      L("Eight to twelve is two to three. So if the speeds are two to three, the distances are two to three too.",
        show(r0d, 'if the speeds are two to three'))),
    S('The same speed',
      L("Second, when the speed is fixed, the time and the distance go the same way too.", show(r1a, 'when the speed is fixed')),
      L("I run at ten kilometers per hour. In one hour I cover ten kilometers. In two hours, twenty.",
        show(r1b, 'I run at ten kilometers per hour')),
      L("In three hours, thirty. The more time I have, the farther I get.", show(r1c, 'In three hours, thirty'))),
    S('The same distance',
      L("Third, when the distance is fixed, the speed and the time go opposite ways. This is where students slip.",
        show(r2a, 'when the distance is fixed')),
      L("From my house to a friend's house is twelve kilometers. At four kilometers per hour, twelve divided by four is "
        "three hours.", show(r2b, 'At four kilometers per hour')),
      L("At six kilometers per hour, twelve divided by six is two hours. The faster I go, the less time it takes.",
        show(r2c, 'At six kilometers per hour')),
      L("The speeds are four to six, that's two to three. And the times are three to two. The ratio flips.",
        show(r2d, 'The ratio flips')),
      L("Why does it flip? Because the speed times the time must stay twelve. Four times three is twelve, and six times "
        "two is twelve.", show(r2e, 'Four times three is twelve'))),
    S('What is fixed?',
      L("So the real skill is to spot when to use these rules. Before we use a rule, we ask, what is fixed here? The "
        "time, the speed, or the distance?", show(r3a, 'what is fixed here')),
      L("Let's try four quick situations. Two cars drive the same three hours. The time is fixed, so the distances "
        "follow the speeds.", show(r3b, 'Two cars drive the same three hours')),
      L("Someone drives to a town and back on the same road. The distance is fixed, so the times flip.",
        show(r3c, 'on the same road')),
      L("Two people start together and stop together, when they meet. The time is fixed, so the distances follow the "
        "speeds.", show(r3d, 'Two people start together')),
      L("A train keeps the same speed all day. The speed is fixed, so more time means more distance.",
        show(r3e, 'A train keeps the same speed'))),
]
r4s = ROAD('r4s', [
    ('ends', [('end', 0, 'A'), ('end', 1, 'B')]),
    ('dots', [('dot', 0, 'slow: 10 kph'), ('dot', 1, 'fast: 20 kph', 'orange')]),
    ('arr', [('arrow', 0, .25, ''), ('arrow', 1, .75, '', 0, 'orange')]),
    ('gap', [('gap', 0, 1, '90 km')]),
    ('parts', [('parts', 0, 1, 3)]),
    ('shares', [('seg', 0, 1 / 3.), ('seg', 1 / 3., 1, 'orange'), ('meet', 1 / 3., 'they meet')])], w=900)
r4a = IH('r4a', 'the same time: $\\ $distances $10:20=1:2$', size=32)
r4b = IH('r4b', '$1+2=3$ parts: $\\ $the slow one covers $\\frac{1}{3}$', size=32)
r4c = IH('r4c', '$3$ hours: $\\ 30$ km and $60$ km, $\\ 30+60=90$', size=32)
r5s = I('r5s', 'A: $\\ 3$ times as fast, $\\ $half as long, $\\ 90$ km. $\\ $B: $\\ $how far?', size=32)
r5v = VT27('r5v', ('3', '90', '1'), ('1', '?', '2'), unknown='distance', w=560)
r5a = IH('r5a', '$1\\times90\\times2=180$', size=32, col=1)
r5a2 = IH('r5a2', '$180\\div(3\\times1)=60$ km', size=32, col=1)
r5b = IH('r5b', '$90\\times\\frac{1}{3}=30$', size=32, col=1)
r5c = IH('r5c', '$30\\times2=60$ km', size=32, col=1)
r6a = I('r6a', 'Time fixed or speed fixed: $\\ $the same way', size=34)
r6b = I('r6b', 'Distance fixed: $\\ $the ratio flips', size=34)
r6c = I('r6c', 'A meeting: $\\ $the road in ratio parts', size=34)
r6d = I('r6d', 'Two things change: $\\ $the V, $\\ $distance in the middle', size=34)
_wp110 += [
    S('A meeting in ratio parts',
      L("Now a new example. Two cyclists start at the same time from the two ends of a ninety-kilometer road, and ride "
        "toward each other.", show(r4s['line'], 'Two cyclists start at the same time'), show(r4s['ends'], 'from the two ends'),
        show(r4s['gap'], 'ninety-kilometer road')),
      L("The slow one rides at ten kilometers per hour, and the fast one at twenty. What part of the road does the slow "
        "one cover until they meet?", show(r4s['dots'], 'The slow one rides at ten'), show(r4s['arr'], 'and the fast one at twenty')),
      L("They start together, and they stop together when they meet. So the time is fixed, and the distances follow the "
        "speeds. Ten to twenty is one to two.", show(r4a, 'Ten to twenty is one to two')),
      L("So we cut the road into one plus two, three equal parts.", show(r4s['parts'], 'three equal parts')),
      L("The slow cyclist covers one part, and the fast one covers two parts. So the slow one covers one third of the "
        "road.", show(r4s['shares'], 'The slow cyclist covers one part'), show(r4b, 'So the slow one covers one third')),
      L("Let's check it. They meet after three hours. The slow cyclist rides thirty kilometers. The fast cyclist rides sixty kilometers. "
        "Thirty plus sixty is ninety, the whole road.", show(r4c, 'They meet after three hours')),
      L("So in a meeting, the road is cut into the sum of the ratio parts.")),
    S('Two things change: the V',
      L("One more tool. What if two things change at once, the speed and the time? Then we use the V, like in the work "
        "topic."),
      L("Now a new example. Car A drives three times as fast as car B, but for half as long. Car A covers ninety "
        "kilometers. How far does car B go?", show(r5s, 'Car A drives three times as fast')),
      L("We make the table speed, distance and time, with the distance in the middle. The distance is the speed times "
        "the time, just like work is the team times the time.", show(r5v['line'], 'We make the table speed, distance and time')),
      L("We use ratio parts for the speed and time, not real units. Car A gets speed three, and time one. Its real distance is "
        "ninety kilometers.", show(r5v['r1'], 'Car A gets speed three')),
      L("Car B gets speed one. Its time is two, because car A drives half as long as car B. Its distance is the "
        "question.", show(r5v['r2'], 'Car B gets speed one')),
      L("The unknown is in the middle column. So the V is upside down. It joins car B's speed, car A's distance, and "
        "car B's time.", show(r5v['v'], 'So the V is upside down')),
      L("We multiply the V, and divide by the other two. One times ninety times two is a hundred eighty. Divided by "
        "three times one, that's sixty kilometers.", show(r5v['calc'], 'We multiply the V'), show(r5a, 'One times ninety times two'),
        show(r5a2, 'Divided by three times one')),
      L("Why does it work? Car B has a third of car A's speed, so in the same time it covers a third of the distance. Ninety times a third is "
        "thirty.", show(r5b, 'Ninety times a third')),
      L("But car B drives twice as long, so it covers twice that. Thirty times two is sixty kilometers.",
        show(r5c, 'Thirty times two is sixty'))),
    S('Recap',
      L("So let's sum it up. When the time or the speed is fixed, the other two go the same way.", show(r6a, 'When the time or the speed is fixed')),
      L("When the distance is fixed, the speed and the time go opposite ways, so the ratio flips.", show(r6b, 'When the distance is fixed')),
      L("In a meeting, the distances follow the speeds, and the road is cut into the sum of the parts.",
        show(r6c, 'In a meeting')),
      L("And when two things change at once, use the V, with the distance in the middle.", show(r6d, 'when two things change')),
      L("Take a moment to memorize this. Now try the next questions, and I'll see you in the next video.")),
]
video('wp-110', 'lesson', slides=_wp110)
SPLITS.append(('wp-110', 'Speed Ratios', [
    (1, None),
    (5, "Let's continue with speed ratios, and see them in a meeting.")]))

# ------------------------------------------------------------------------------------------------ g111 (Maya and Theo)
# Hebrew (wp 7244-7365, Dani and Dina, she is 1.5 times as fast): (1) ratios 1 : 1.5 = 2 : 3, the same time, the whole
# road is 5 parts -> 2/5; (2) plugging in 10 and 15 (x10 to drop the decimal), they meet after one hour ("the simplest");
# (3) "what if" elimination: he covers less than half (out); if she were 2x -> a third; she is slower than that, so he
# covers more than a third (out 1/3, 1/4). English: Theo 1.25 x Maya -> 4 : 5 -> 4/9; plug in 16 and 20; "imagine Theo
# were exactly twice as fast". First use of the meeting in ratio parts (wp-110 part 2), "like in the lesson".
g11s = ROAD('g11s', [
    ('ends', [('end', 0, 'Maya'), ('end', 1, 'Theo')]),
    ('parts', [('parts', 0, 1, 9)]),
    ('shares', [('seg', 0, 4 / 9.), ('seg', 4 / 9., 1, 'orange'), ('meet', 4 / 9., 'they meet')]),
    ('lab', [('above', 2 / 9., 'Maya: 4 parts'), ('above', 13 / 18., 'Theo: 5 parts')])], w=900)
g11a = IH('g11a', 'speeds $1:1.25$', size=30)
g11b = IH('g11b', '$\\times4$: $\\ 4:5$', size=30)
g11c = IH('g11c', '$4+5=9$ parts: $\\ $Maya $\\frac{4}{9}$', size=30)
g11d = IH('g11d', 'Maya $16$ kph, $\\ $Theo $16+4=20$ kph', size=30)
g11e = IH('g11e', '$1$ hour: $\\ 16$ km and $20$ km', size=30)
g11f = IH('g11f', 'trail: $\\ 16+20=36$ km', size=30)
g11g = IH('g11g', '$\\frac{16}{36}=\\frac{4}{9}$', size=32)
g11h = IH('g11h', 'Theo faster: $\\ $Maya less than $\\frac{1}{2}$', size=30)
g11i = IH('g11i', 'if Theo were $\\times2$: $\\ $Maya $\\frac{1}{3}$', size=30)
g11j = IH('g11j', 'Theo slower than that: $\\ $Maya more than $\\frac{1}{3}$', size=30)
g11k = IH('g11k', '$\\frac{1}{3}=\\frac{3}{9}<\\frac{4}{9}$', size=30, col=1)
video('solve-wp27-g111', 'solution', qid='wp27-g111', slides=[
    S('Method 1 · Understanding: ratio parts',
      L("Maya and Theo start at the same time from opposite ends of a bike trail, and ride toward each other. Theo "
        "rides at one point two five times Maya's speed. What fraction of the trail does Maya cover before they meet?",
        pt('stem', 'Maya and Theo start', 'hl', 11.0), voice='calm', pause=0.5),
      L("So there's no distance, no time, and no real speed. They only tell us that Theo is one and a quarter times as "
        "fast.", pt('stem: given', 'Theo is one and a quarter times')),
      L("We'll solve it in three different ways. First by understanding, with ratio parts, like in the lesson."),
      L("They start together, and they stop together when they meet. So the time is fixed, and the distances follow the "
        "speeds. The speeds are one to one point two five.", show(g11a, 'The speeds are one to one point two five')),
      L("One point two five is one and a quarter. So we multiply both by four, to make them whole. That's four to five.",
        show(g11b, 'That\'s four to five')),
      L("So we cut the trail into four plus five, nine equal parts.", show(g11s['line'], 'So we cut the trail'),
        show(g11s['ends'], 'So we cut the trail'), show(g11s['parts'], 'nine equal parts')),
      L("Maya rides four parts, and Theo rides five. So Maya covers four out of nine, four ninths of the trail.",
        show(g11s['shares'], 'Maya rides four parts'), show(g11s['lab'], 'and Theo rides five'),
        show(g11c, 'four out of nine'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. Data is missing, so we choose friendly "
        "numbers."),
      L("Let's say Maya rides at sixteen kilometers per hour. We pick sixteen, because a quarter of sixteen is four. So "
        "Theo rides at sixteen plus four, twenty.", show(g11d, 'Let\'s say Maya rides at sixteen')),
      L("Let's say they meet after one hour, the simplest time. The time is the same for both, so any time works.",
        show(g11e, 'they meet after one hour')),
      L("In that hour, Maya rides sixteen kilometers, and Theo rides twenty. So the trail is sixteen plus twenty, "
        "thirty-six kilometers.", show(g11f, 'sixteen plus twenty')),
      L("Maya covers sixteen out of thirty-six. We divide both by four, and that's four ninths again.",
        show(g11g, 'We divide both by four'))),
    S('Method 3 · Understanding: what if',
      L("[pause] Now by understanding, with no calculation at all. We start again from the givens. Theo is faster, so "
        "Maya covers less than half of the trail.", show(g11h, 'so Maya covers less than half')),
      L("So one half is out. And five ninths is more than half, so it's out too.", mk('cross', 'choice 2', 'So one half is out'),
        mk('cross', 'choice 3', "so it's out too")),
      L("Now imagine Theo were exactly twice as fast. Then Maya would cover one part out of three, a third.",
        show(g11i, 'imagine Theo were exactly twice as fast')),
      L("But Theo is only one and a quarter times as fast. That's slower than twice. So Maya covers more than a third.",
        show(g11j, 'So Maya covers more than a third')),
      L("One quarter is less than a third, so it's out.", mk('cross', 'choice 4', "so it's out")),
      L("Four ninths is left. And it fits, because a third is three ninths, and four ninths is more.", show(g11k, 'a third is three ninths')),
      L("Choice number one is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g112 (rowboat and motorboat)
# Hebrew (wp 7368-7440, Yaron and Moti, 2.5 x): NOT a meeting - Moti flies the whole way; 1 : 2.5 = 2 : 5, the whole
# route is 5 parts, not 7; plug in 10 and 25, one hour -> the route is 25 -> 10/25; her summary: meeting vs one covers
# everything. English: 4.5 x -> 2 : 9 -> 2/9; the trap 2/11 (the meeting answer) at its step. The contrast with a
# meeting is this question's own idea (taught here, about 2 minutes, with the picture).
g12s = ROAD('g12s', [
    ('ends', [('end', 0, 'motorboat'), ('end', 1, 'rowboat')]),
    ('parts', [('parts', 0, 1, 9)]),
    ('motor', [('seg', 0, 1, 'orange'), ('arrow', 0, 1, 'motorboat: all 9 parts', 0, 'orange')]),
    ('row', [('seg', 7 / 9., 1), ('arrow', 1, 7 / 9., 'rowboat: 2 parts', 1)])], w=900)
g12a = IH('g12a', 'speeds $1:4.5$', size=30)
g12b = IH('g12b', '$\\times2$: $\\ 2:9$', size=30)
g12c = IH('g12c', 'the whole lake $=9$ parts, $\\ $not $2+9=11$', size=30)
g12d = IH('g12d', 'rowboat: $\\ \\frac{2}{9}$', size=32, col=1)
g12f = IH('g12f', 'rowboat $4$ kph, $\\ $motorboat $4\\times4.5=18$ kph', size=30)
g12g = IH('g12g', 'motorboat: $\\ 1$ hour, $\\ $so the lake is $18$ km', size=30)
g12h = IH('g12h', 'rowboat: $\\ 4$ km in that hour', size=30)
g12i = IH('g12i', '$\\frac{4}{18}=\\frac{2}{9}$', size=32, col=1)
video('solve-wp27-g112', 'solution', qid='wp27-g112', slides=[
    S('Method 1 · Understanding: ratio parts',
      L("A rowboat and a motorboat leave opposite ends of a lake at the same time, each heading for the other end. The "
        "motorboat is four point five times as fast as the rowboat. By the time the motorboat reaches the far end, what "
        "fraction of the length of the lake has the rowboat traveled?", pt('stem', 'A rowboat and a motorboat', 'hl', 14.0),
        voice='calm', pause=0.5),
      L("It looks like the last question, but it isn't. They don't stop when they meet. They stop when the motorboat "
        "reaches the far end.", pt('stem: ask', 'They stop when the motorboat')),
      L("We'll solve it in two different ways. First by understanding, with ratio parts. Both boats move for the same "
        "time, so the distances follow the speeds."),
      L("The speeds are one to four point five. We multiply both by two, to make them whole. That's two to nine.",
        show(g12a, 'The speeds are one to four point five'), show(g12b, "That's two to nine")),
      L("So while the rowboat covers two parts, the motorboat covers nine parts.")),
    S('Method 1 · Understanding: ratio parts',
      L("Now the sketch. The motorboat goes all the way across the lake. So the whole lake is the motorboat's nine "
        "parts.", show(g12s['line'], 'Now the sketch'), show(g12s['ends'], 'Now the sketch'), show(g12s['parts'], 'nine parts.'),
        show(g12s['motor'], 'The motorboat goes all the way')),
      L("The rowboat started at the other end, and it covered only two of those parts.", show(g12s['row'], 'it covered only two')),
      L("So the whole lake is nine parts, not two plus nine.", show(g12c, 'not two plus nine')),
      L("So the rowboat traveled two ninths of the lake.", show(g12d, 'two ninths of the lake')),
      L("Two elevenths, choice number one, would be right in a meeting question, where the road is the sum of both "
        "parts. Here, the motorboat covers the whole length alone.", mk('cross', 'choice 1', 'covers the whole length alone'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. Let's say the rowboat moves at four "
        "kilometers per hour. Four times four point five is eighteen, so the motorboat moves at eighteen.",
        show(g12f, 'the rowboat moves at four')),
      L("Let's say the motorboat reaches the far end after one hour, the simplest time. So the lake is eighteen "
        "kilometers long.", show(g12g, 'the motorboat reaches the far end after one hour')),
      L("In that same hour, the rowboat covers four kilometers.", show(g12h, 'the rowboat covers four kilometers')),
      L("That's four out of eighteen. We divide both by two, and that's two ninths again.", show(g12i, 'We divide both by two')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t27-31 (van and scooter)
# No Hebrew (an English question, the V of topic 26 with distance in the middle, real exams 2023_spring_q2_05,
# 2025_spring_q1_16). First use after wp-110 part 2: the V applied slowly, "like in the lesson". Method 2: factors (the
# same way as is, the opposite way flipped: topic 26 camera lesson part 3). Traps at their steps: 180 (the speed not
# flipped), 120 (the speed ignored).
q31v = VT27('q31v', ('1', '1', '40'), ('1.5', '3', '?'), unknown='time', w=560)
q31a = IH('q31a', '$1\\times3\\times40=120$', size=30, col=1)
q31b = IH('q31b', '$120\\div1.5=80$', size=30, col=1)
q31c = IH('q31c', '$1.5\\times80=120$', size=30, col=1)
q31d = IH('q31d', 'time $=$ distance $\\div$ speed', size=30)
q31e = IH('q31e', 'distance $\\times3$: $\\ $time $\\times3$', size=30)
q31f = IH('q31f', 'speed $\\times\\frac{3}{2}$: $\\ $time $\\times\\frac{2}{3}$', size=30)
q31g = IH('q31g', '$40\\times3=120$', size=30, col=1)
q31h = IH('q31h', '$120\\times\\frac{2}{3}=80$', size=30, col=1)
q31i = IH('q31i', '$120\\times\\frac{3}{2}=180$: $\\ $the trap', size=30, col=1)
video('solve-q-r26-t27-31', 'solution', qid='q-r26-t27-31', slides=[
    S('Method 1 · The math way: the V method',
      L("A delivery van travels three times as far as a scooter, at one point five times the scooter's speed. The "
        "scooter's trip takes forty minutes. How many minutes does the van's trip take?",
        pt('stem', 'A delivery van travels', 'hl', 9.0), voice='calm', pause=0.5),
      L("So two things change at once, the distance and the speed. And they ask for the van's time.",
        pt('stem: ask', "they ask for the van's time")),
      L("We'll solve it in two different ways. Let's start with the math way, with the V, like in the lesson. The table "
        "is speed, distance and time, with the distance in the middle.", show(q31v['line'], 'with the V, like in the lesson')),
      L("We use ratio parts for the speeds and distances, not real units. So the scooter gets speed one and distance one. Its real time "
        "is forty minutes.", show(q31v['r1'], 'the scooter gets speed one')),
      L("The van goes one and a half times as fast, so its speed is one point five. It goes three times as far, so its "
        "distance is three. Its time is the question.", show(q31v['r2'], 'so its speed is one point five')),
      L("The unknown is in the time column. So it's a normal V. It joins the scooter's speed, the van's distance, and the "
        "scooter's time.", show(q31v['v'], "So it's a normal V")),
      L("We multiply the V. One times three times forty is a hundred twenty.", show(q31v['calc'], 'We multiply the V'),
        show(q31a, 'One times three times forty')),
      L("Then we divide by the other two, one times one and a half. A hundred twenty divided by one and a half is "
        "eighty.", show(q31b, 'A hundred twenty divided by one and a half')),
      L("Why eighty? Because one and a half times eighty is eighty plus forty, a hundred twenty.", show(q31c, 'one and a half times eighty')),
      L("So the van's trip takes eighty minutes.")),
    S('Method 2 · Understanding: factors',
      L("[pause] Now by understanding, with factors, one change at a time. We start again from the givens. The time is "
        "the distance divided by the speed.", show(q31d, 'The time is the distance divided by the speed')),
      L("The van goes three times as far. More distance means more time, so the time goes the same way, times three.",
        show(q31e, 'More distance means more time')),
      L("Forty times three is a hundred twenty.", show(q31g, 'Forty times three')),
      L("The van is one and a half times as fast. More speed means less time, so the time goes the opposite way. We flip "
        "three halves to two thirds.", show(q31f, 'We flip three halves to two thirds')),
      L("A hundred twenty times two thirds. A third of a hundred twenty is forty, so two thirds of it is eighty. The same "
        "answer.", show(q31h, 'A hundred twenty times two thirds')),
      L("Careful with a hundred eighty, choice number four. It multiplies by three halves, so it didn't flip the speed.",
        show(q31i, 'It multiplies by three halves'), mk('cross', 'choice 4', "so it didn't flip the speed")),
      L("And a hundred twenty, choice number three, forgets the speed completely.", mk('cross', 'choice 3', 'forgets the speed completely')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-113 (lesson: relative speed)
# REWRITTEN 25 Oct at the teacher's request ("show where runner A is after an hour and where B is after an hour, and then
# after 2 hours and after 3 hours, and show that the gap just expands or closes every hour by the same, so I don't have
# to calculate each person ... explaining that the meeting point is where they cover together the whole thing ... make it
# visually well"). Two parts (teacher, 25 Oct: exactly 2, longer parts are fine).
# Hebrew (wp 7442-7498, 7639-7643): the rate the gap closes or opens; opposite directions (toward: the truck and the car
# crash "at 70"; apart: the gap grows) -> add; the same direction (a chase) -> subtract, the car covers the truck's way
# plus the gap between them; "only the gap between them matters, not the whole way"; her closing recap: chases are where
# students slip; "Miki could be 100 and the father 102, only the gap matters".
# Part 1: the definition; TOWARD hour by hour (Mia 3 kph, Leo 5 kph, 24 km: the gap 24 -> 16 -> 8 -> 0, the same 8 every
# hour = 3 + 5); the meeting = together they cover the whole gap (9 + 15 = 24); the quick way 24 / 8 = 3, time = the gap
# divided by the relative speed; her truck 20 + car 50 = a crash at 70; a second example (Sara 12, Tom 8, 50 km: 50 -> 30
# -> 10 -> 0, 2 1/2 h, checked 30 + 20 = 50); APART hour by hour (0 -> 8 -> 16 -> 24), after 5 h -> 40 km, 20 km apart ->
# 2 1/2 h; cars 40 + 60, 150 km -> 1 1/2 h.
# Part 2: the CHASE hour by hour (cyclist 9 kph, runner 6 kph 9 km ahead: 9 -> 6 -> 3 -> 0, the same 3 every hour);
# "imagine the slow one stands still"; catching up = he covers her head start plus her way (27 - 18 = 9); time = the
# starting gap / the difference (9 / 3 = 3); a second chase (car 70, bus 50, 10 km -> 1/2 h = 30 min) and the faster one
# in front (the gap grows by the difference); the classic mistake (only the starting gap, 100 and 102); a head start first,
# in two stages (Dan 4 kph, half an hour, sister 12 kph -> 2 km -> 8 -> 15 min); from whose start the time is counted
# (external findings, real exam 2026_spring_q2_17: Ava and Ben, 30 s from Ava's start -> 3/2; from Ben's start -> 4/3),
# every start time on the sketch; the recap. The later questions lean on these words: "with relative speed, like in the
# lesson", "in two stages", "toward each other, so we add", "in a chase we subtract", "the head start", "from whose start",
# "imagine the slow one stands still", "the time is the gap divided by the speed", "together they cover the whole lap".
_RS_TEAL_BAND = MV.BAND


def HOURS(name, lo, hi, rows, layers, w=1150, gapcol=True, title='Hour by hour', guides=(), y0=136, bottom=56):
    """the hour-by-hour picture (wp-113, 2026-10-25): the same road drawn once per row (start, after 1 hour, after 2 hours
    ...), positions in km from lo to hi, and the gap in a column at the right. The base: the column title, row 0's road
    and its label, the faint start guides. layers = [(key, [mark, ...])]:
      ('road', r)                          row r's road and its label (rows[r])
      ('dot', r, km, text, colour[, side]) a mover and its name above it (side -1: name to the left, 1: to the right)
      ('spd', r, km, d, text, colour)      a speed arrow above the mover, direction d (1 right, -1 left), its text
      ('trail', r, a, b, text, colour, lvl) the way covered from a to b and the mover at b; lvl 0: a band on the road, its
                                           text under the road; lvl 1: a thick line just above the road, its text above
      ('note', r, km, text, colour)        a text under the road
      ('above', r, km, text, colour[, lift]) a text above the road (lift: px higher)
      ('gap', r, text)                     the gap in the column
      ('chg', r, text)                     the change from the row above: an arrow down the column and its text
      ('star', r, km)                      the meeting point (a red star)
      ('brace', r, a, b, text, colour, lvl) a bracket under the road (lvl 1, 2: lower) and its text
      ('colbox',)                          a frame around the gap column"""
    import math
    W = 1000; X0, X1 = 170, (770 if gapcol else 960); GX = 885
    RH = 106; n = len(rows)
    ys = [y0 + RH * r for r in range(n)]
    H = ys[-1] + bottom
    X = lambda km: X0 + (km - lo) * (X1 - X0) / float(hi - lo)
    col_ = lambda c: {'orange': ORANGE, 'red': _RED27, 'ink': _INK}.get(c, _TEAL)
    def _T(x, y, t, size=28, col=None, anchor='middle'):     # a centred label near an edge stays inside the picture
        w2 = len(t) * size * 0.3
        if anchor == 'middle' and x + w2 > W - 6: return _tx(W - 6, y, t, size, col, 'end')
        if anchor == 'middle' and x - w2 < 6: return _tx(6, y, t, size, col, 'start')
        return _tx(x, y, t, size, col, anchor)
    def road(r):
        y = ys[r]
        return (_T(6, y + 11, rows[r], 30, _INK, 'start') +
                '<rect x="%d" y="%d" width="%d" height="14" rx="7" fill="%s" stroke="%s" stroke-width="2.4"/>' % (X0, y - 7, X1 - X0, _LIGHT, _INK))
    body = ''
    for g in guides:
        body += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#9aa7b0" stroke-width="2" stroke-dasharray="6 6"/>'
                 % (X(g), ys[0] + 10, X(g), H - 8))
    if gapcol:
        body += _T(GX, 36, 'the gap', 30, _TEAL)
        body += '<line x1="800" y1="%d" x2="800" y2="%d" stroke="#c9d3d9" stroke-width="2"/>' % (14, H - 6)
    body += road(0)
    out = [('line', MV._svg(W, H, body, title))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'road':
                b += road(m[1])
            elif k == 'dot':
                y = ys[m[1]]; c = col_(m[4]); x = X(m[2]); side = m[5] if len(m) > 5 else 0
                b += '<circle cx="%.1f" cy="%d" r="12" fill="%s" stroke="#ffffff" stroke-width="2"/>' % (x, y, c)
                b += _T(x + 14 * side, y - 22, m[3], 32, c, {-1: 'end', 0: 'middle', 1: 'start'}[side])
            elif k == 'spd':
                y = ys[m[1]] - 66; d = m[3]; x = X(m[2]) + 14 * d; c = col_(m[5])
                b += MV._arrow(x, y, x + 96 * d, y, c, 3.2) + _T(x + 48 * d, y - 12, m[4], 30, c)
            elif k == 'trail':
                r, a, e, t, c, lvl = m[1:7]; y = ys[r]; cc = col_(c)
                xa, xe = sorted((X(a), X(e)))
                if lvl == 0:
                    f = '#fbd9b9' if c == 'orange' else _RS_TEAL_BAND
                    b += ('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2.4"/>'
                          % (xa, y - 7, xe - xa, f, cc)) + _T((xa + xe) / 2, y + 42, t, 30, cc)
                else:
                    b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="7" stroke-linecap="round"/>'
                          % (xa, y - 18, xe, y - 18, cc)) + _T((xa + xe) / 2, y - 30, t, 30, cc)
                b += '<circle cx="%.1f" cy="%d" r="12" fill="%s" stroke="#ffffff" stroke-width="2"/>' % (X(e), y, cc)
            elif k == 'note':
                b += _T(X(m[2]), ys[m[1]] + 42, m[3], 30, col_(m[4]))
            elif k == 'above':
                b += _T(X(m[2]), ys[m[1]] - 26 - (m[5] if len(m) > 5 else 0), m[3], 30, col_(m[4]))
            elif k == 'gap':
                b += _T(GX, ys[m[1]] + 15, m[2], 42, _TEAL)
            elif k == 'chg':
                r = m[1]
                b += MV._arrow(GX, ys[r - 1] + 24, GX, ys[r] - 24, _TEAL, 3) + _T(GX + 20, (ys[r - 1] + ys[r]) / 2.0 + 10, m[2], 30, _TEAL, 'start')
            elif k == 'star':
                x = X(m[2]); y = ys[m[1]]
                pts = ' '.join('%.1f,%.1f' % (x + (21 if i % 2 == 0 else 9) * math.cos(math.pi * (i / 5.0 - .5)),
                                              y + (21 if i % 2 == 0 else 9) * math.sin(math.pi * (i / 5.0 - .5))) for i in range(10))
                b += '<polygon points="%s" fill="%s" stroke="#ffffff" stroke-width="1.5"/>' % (pts, _RED27)
            elif k == 'brace':
                r, a, e, t, c, lvl = m[1:7]; cc = col_(c); y = ys[r] + 22 + 58 * lvl
                xa, xe = X(a) + 2, X(e) - 2
                b += ('<path d="M %.1f %d L %.1f %d L %.1f %d L %.1f %d" fill="none" stroke="%s" stroke-width="2.8"/>'
                      % (xa, y - 12, xa, y, xe, y, xe, y - 12, cc)) + _T((xa + xe) / 2, y + 34, t, 30, cc)
            elif k == 'colbox':
                b += '<rect x="806" y="6" width="188" height="%d" rx="12" fill="none" stroke="%s" stroke-width="4"/>' % (H - 12, _TEAL)
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=0, own=True)


def STRIP(name, cells, w=1000, title='The gap, hour by hour'):
    """the gap hour by hour as a strip of boxes (wp-113): cells = [(time, gap, change)] (change '' for the first);
    layers 'line' (box 0), 'c1', 'c2', ... (an arrow with the change, then the next box)."""
    cw, ag = 180, 84; n = len(cells); W = 20 + n * cw + (n - 1) * ag; H = 136
    xs = [10 + i * (cw + ag) for i in range(n)]
    def box(i):
        t, g, _ = cells[i]; x = xs[i]
        return (_tx(x + cw / 2.0, 30, t, 28, _INK) +
                '<rect x="%d" y="44" width="%d" height="84" rx="10" fill="%s" stroke="%s" stroke-width="2.6"/>' % (x, cw, _LIGHT, _TEAL) +
                _tx(x + cw / 2.0, 100, g, 40, _TEAL))
    out = [('line', MV._svg(W, H, box(0), title + ': ' + cells[0][1]))]
    for i in range(1, n):
        b = MV._arrow(xs[i - 1] + cw + 8, 92, xs[i] - 8, 92, _TEAL, 3) + _tx((xs[i - 1] + cw + xs[i]) / 2.0, 76, cells[i][2], 28, _TEAL)
        out.append(('c%d' % i, MV._svg(W, H, b + box(i), '%s: %s' % (title, cells[i][1]))))
    return MV.items(_layers, name, out, w=w, col=0, own=True)


s3meaning = I('s3meaning', 'Relative speed: $\\ $how fast the gap between them changes', size=36)
# ---- part 1: toward each other, hour by hour (Mia 3 kph from km 0, Leo 5 kph from km 24)
rsH = HOURS('rsH', 0, 24, ['start', '1 hour', '2 hours', '3 hours'], [
    ('d0', [('dot', 0, 0, 'Mia', 'teal'), ('dot', 0, 24, 'Leo', 'orange')]),
    ('g0', [('gap', 0, '24')]),
    ('vA', [('spd', 0, 0, 1, '3 kph', 'teal')]),
    ('vB', [('spd', 0, 24, -1, '5 kph', 'orange')]),
    ('r1', [('road', 1)]),
    ('a1', [('trail', 1, 0, 3, '3 km', 'teal', 0)]),
    ('b1', [('trail', 1, 24, 19, '5 km', 'orange', 0)]),
    ('c1', [('chg', 1, '−8')]),
    ('g1', [('gap', 1, '16')]),
    ('r2', [('road', 2)]),
    ('a2', [('trail', 2, 0, 6, '6 km', 'teal', 0)]),
    ('b2', [('trail', 2, 24, 14, '10 km', 'orange', 0)]),
    ('c2', [('chg', 2, '−8')]),
    ('g2', [('gap', 2, '8')]),
    ('r3', [('road', 3)]),
    ('a3', [('trail', 3, 0, 9, '9 km', 'teal', 0)]),
    ('b3', [('trail', 3, 24, 9, '15 km', 'orange', 0)]),
    ('c3', [('chg', 3, '−8')]),
    ('g3', [('gap', 3, '0')]),
    ('m3', [('star', 3, 9)]),
    ('box', [('colbox',)])], guides=(0, 24), title='Toward each other, hour by hour')
rsHk = IH('rsHk', 'every hour: $\\ 3+5=8$ km closer', size=32)
rsT = HOURS('rsT', 0, 24, ['3 hours'], [
    ('ends', [('above', 0, 0, "Mia's start", 'teal'), ('above', 0, 24, "Leo's start", 'orange')]),
    ('a', [('trail', 0, 0, 9, 'Mia: 9 km', 'teal', 0)]),
    ('b', [('trail', 0, 24, 9, 'Leo: 15 km', 'orange', 0), ('star', 0, 9)]),
    ('all', [('brace', 0, 0, 24, 'the whole gap: 24 km', 'red', 1)])],
    gapcol=False, y0=60, bottom=120, title='They meet')
rsTa = IH('rsTa', '$9+15=24$', size=32)
rsTk = I('rsTk', 'They meet when together they cover the whole gap.', size=34)
rsTb = IH('rsTb', '$24\\div8=3$ hours', size=32)
rsTf = I('rsTf', 'time $=$ the gap $\\div$ the relative speed', size=34)
rsC = ROAD('rsC', [
    ('dots', [('dot', .06, 'truck'), ('dot', .94, 'car', 'orange')]),
    ('arrT', [('arrow', .06, .36, '20 kph')]),
    ('arrC', [('arrow', .94, .64, '50 kph', 0, 'orange')])], w=1100, title='A truck and a car')
rsCa = IH('rsCa', '$20+50=70$ km closer every hour', size=32)
rsCk = I('rsCk', 'Toward each other: $\\ $add the speeds.', size=34)
rsE = ROAD('rsE', [
    ('dots', [('dot', 0, 'Sara'), ('dot', 1, 'Tom', 'orange')]),
    ('gap', [('gap', 0, 1, 'the gap: 50 km')]),
    ('arrS', [('arrow', 0, .3, '12 kph')]),
    ('arrT', [('arrow', 1, .7, '8 kph', 0, 'orange')])], w=1100, title='Sara and Tom')
rsEa = IH('rsEa', '$12+8=20$ km closer every hour', size=32)
rsEs = STRIP('rsEs', [('start', '50', ''), ('1 hour', '30', '−20'), ('2 hours', '10', '−20'), ('2½ hours', '0', '−10')])
rsEb = IH('rsEb', '$50\\div20=2\\frac{1}{2}$ hours', size=32)
rsEc = IH('rsEc', '$2\\frac{1}{2}$ hours $=2$ hours $30$ minutes', size=32)
rsK = HOURS('rsK', 0, 50, ['2½ hours'], [
    ('ends', [('above', 0, 0, "Sara's start", 'teal'), ('above', 0, 50, "Tom's start", 'orange')]),
    ('a', [('trail', 0, 0, 30, 'Sara: 30 km', 'teal', 0)]),
    ('b', [('trail', 0, 50, 30, 'Tom: 20 km', 'orange', 0), ('star', 0, 30)]),
    ('all', [('brace', 0, 0, 50, 'the whole gap: 50 km', 'red', 1)])],
    gapcol=False, y0=60, bottom=120, title='Check: they meet')
rsKa = IH('rsKa', 'Sara: $\\ 12\\times2\\frac{1}{2}=30$ km', size=32)
rsKb = IH('rsKb', 'Tom: $\\ 8\\times2\\frac{1}{2}=20$ km', size=32)
rsKc = IH('rsKc', '$30+20=50$', size=32)
# apart, hour by hour (both from km 0; Mia to the left at 3 kph, Leo to the right at 5 kph)
rsA = HOURS('rsA', -9, 15, ['start', '1 hour', '2 hours', '3 hours'], [
    ('d0', [('dot', 0, 0, 'Mia', 'teal', -1), ('dot', 0, 0, 'Leo', 'orange', 1)]),
    ('g0', [('gap', 0, '0')]),
    ('vA', [('spd', 0, 0, -1, '3 kph', 'teal')]),
    ('vB', [('spd', 0, 0, 1, '5 kph', 'orange')]),
    ('r1', [('road', 1)]),
    ('a1', [('trail', 1, 0, -3, '3 km', 'teal', 0)]),
    ('b1', [('trail', 1, 0, 5, '5 km', 'orange', 0)]),
    ('c1', [('chg', 1, '+8')]),
    ('g1', [('gap', 1, '8')]),
    ('r2', [('road', 2)]),
    ('a2', [('trail', 2, 0, -6, '6 km', 'teal', 0)]),
    ('b2', [('trail', 2, 0, 10, '10 km', 'orange', 0)]),
    ('c2', [('chg', 2, '+8')]),
    ('g2', [('gap', 2, '16')]),
    ('r3', [('road', 3)]),
    ('a3', [('trail', 3, 0, -9, '9 km', 'teal', 0)]),
    ('b3', [('trail', 3, 0, 15, '15 km', 'orange', 0)]),
    ('c3', [('chg', 3, '+8')]),
    ('g3', [('gap', 3, '24')]),
    ('box', [('colbox',)])], guides=(0,), title='Apart, hour by hour')
rsAk = IH('rsAk', 'every hour: $\\ 3+5=8$ km farther', size=32)
rsQa = IH('rsQa', 'after $5$ hours: $\\ 5\\times8=40$ km', size=32)
rsQb = IH('rsQb', '$20$ km apart: $\\ 20\\div8=2\\frac{1}{2}$ hours', size=32)
rsQ = ROAD('rsQ', [
    ('town', [('end', .5, 'the town')]),
    ('dots', [('dot', .5, '', 'ink')]),
    ('arr1', [('arrow', .47, .17, '40 kph')]),
    ('arr2', [('arrow', .53, .83, '60 kph', 0, 'orange')])], w=1100, title='Two cars from one town')
rsQc = IH('rsQc', '$40+60=100$ km farther every hour', size=32)
rsQd = IH('rsQd', '$150\\div100=1\\frac{1}{2}$ hours', size=32)
rsQk = I('rsQk', 'Toward each other or apart: $\\ $add.', size=34)
# ---- part 2: a chase, hour by hour (the cyclist 9 kph from km 0, the runner 6 kph from km 9)
rsS = HOURS('rsS', 0, 27, ['start', '1 hour', '2 hours', '3 hours'], [
    ('dR', [('dot', 0, 9, 'runner', 'orange')]),
    ('vR', [('spd', 0, 9, 1, '6 kph', 'orange')]),
    ('dC', [('dot', 0, 0, 'cyclist', 'teal')]),
    ('vC', [('spd', 0, 0, 1, '9 kph', 'teal')]),
    ('h0', [('note', 0, 4.5, '9 km ahead', 'ink')]),
    ('g0', [('gap', 0, '9')]),
    ('r1', [('road', 1)]),
    ('a1', [('trail', 1, 0, 9, '9 km', 'teal', 0)]),
    ('b1', [('trail', 1, 9, 15, '6 km', 'orange', 1)]),
    ('c1', [('chg', 1, '−3')]),
    ('g1', [('gap', 1, '6')]),
    ('r2', [('road', 2)]),
    ('a2', [('trail', 2, 0, 18, '18 km', 'teal', 0)]),
    ('b2', [('trail', 2, 9, 21, '12 km', 'orange', 1)]),
    ('c2', [('chg', 2, '−3')]),
    ('g2', [('gap', 2, '3')]),
    ('r3', [('road', 3)]),
    ('a3', [('trail', 3, 0, 27, '27 km', 'teal', 0)]),
    ('b3', [('trail', 3, 9, 27, '18 km', 'orange', 1)]),
    ('c3', [('chg', 3, '−3')]),
    ('g3', [('gap', 3, '0')]),
    ('m3', [('star', 3, 27)]),
    ('box', [('colbox',)])], guides=(0, 9), title='A chase, hour by hour')
rsSk = IH('rsSk', 'every hour: $\\ 9-6=3$ km closer', size=32)
rsU = HOURS('rsU', 0, 27, ['3 hours'], [
    ('ends', [('above', 0, 0, "his start", 'teal'), ('above', 0, 9, "her start", 'orange', 36)]),
    ('r', [('trail', 0, 9, 27, 'runner: 18 km', 'orange', 1)]),
    ('c', [('trail', 0, 0, 27, 'cyclist: 27 km', 'teal', 0), ('star', 0, 27)]),
    ('h', [('brace', 0, 0, 9, 'head start: 9 km', 'red', 1)])],
    gapcol=False, y0=120, bottom=120, title='He catches her')
rsUa = IH('rsUa', '$27-18=9$', size=32)
rsUk = I('rsUk', 'He catches her when he gains the whole starting gap.', size=34)
rsUb = IH('rsUb', '$9\\div3=3$ hours', size=32)
rsUf = I('rsUf', 'A chase: $\\ $time $=$ the starting gap $\\div$ the difference', size=34)
rsV = ROAD('rsV', [
    ('bus', [('dot', .4, 'bus', 'orange')]),
    ('arrB', [('arrow', .4, .62, '50 kph', 1, 'orange')]),
    ('car', [('dot', 0, 'car')]),
    ('arrC', [('arrow', 0, .3, '70 kph')]),
    ('gap', [('gap', 0, .4, 'the gap: 10 km')])], w=1100, title='A car chases a bus')
rsVa = IH('rsVa', '$70-50=20$ km closer every hour', size=32)
rsVb = IH('rsVb', '$10\\div20=\\frac{1}{2}$ hour', size=32)
rsVc = IH('rsVc', '$\\frac{1}{2}$ hour $=30$ minutes', size=32)
rsVd = IH('rsVd', 'the car in front: $\\ $the gap grows by $20$ km an hour', size=32)
_wp113 = [
    S('Relative Speed',
      L("Welcome back. Now relative speed."),
      L("This is about two travelers at once. How fast do they get closer, or farther apart?")),
    S('What it is',
      L("Relative speed is the rate at which the gap between two travelers changes.",
        show(s3meaning, 'Relative speed is the rate')),
      L("We don't follow each one on its own. We follow the gap between them."),
      L("How many kilometers does the gap change in one hour? That's the relative speed.")),
    S('Toward each other, hour by hour',
      L("Now a new example. Mia and Leo stand twenty-four kilometers apart, on the same road.",
        show(rsH['line'], 'Mia and Leo stand'), show(rsH['d0'], 'Mia and Leo stand'), show(rsH['g0'], 'twenty-four kilometers apart')),
      L("They walk toward each other. Mia walks three kilometers per hour, and Leo walks five.",
        show(rsH['vA'], 'Mia walks three'), show(rsH['vB'], 'Leo walks five')),
      L("Let's see where they are after one hour.", show(rsH['r1'], 'after one hour')),
      L("In one hour, Mia walks three kilometers. So she's three kilometers from her start.",
        show(rsH['a1'], 'Mia walks three kilometers')),
      L("Leo walks five kilometers toward her. So he's five kilometers from his start.",
        show(rsH['b1'], 'Leo walks five kilometers')),
      L("Together, they closed three plus five, eight kilometers. So the gap is twenty-four minus eight, sixteen.",
        show(rsH['c1'], 'three plus five, eight'), show(rsH['g1'], 'twenty-four minus eight, sixteen')),
      L("Now after two hours. Each of them walks for one more hour.", show(rsH['r2'], 'after two hours')),
      L("Mia walks three more kilometers. So she's six kilometers from her start.", show(rsH['a2'], 'six kilometers from her start')),
      L("Leo walks five more. So he's ten kilometers from his start.", show(rsH['b2'], 'ten kilometers from his start')),
      L("The gap shrinks by eight again. Sixteen minus eight is eight kilometers.",
        show(rsH['c2'], 'shrinks by eight again'), show(rsH['g2'], 'Sixteen minus eight')),
      L("And after three hours? Mia is nine kilometers from her start. Leo is fifteen kilometers from his.",
        show(rsH['r3'], 'after three hours'), show(rsH['a3'], 'Mia is nine kilometers'), show(rsH['b3'], 'Leo is fifteen kilometers')),
      L("The gap shrinks by eight once more. Eight minus eight is zero. They meet.",
        show(rsH['c3'], 'by eight once more'), show(rsH['g3'], 'Eight minus eight is zero'), show(rsH['m3'], 'They meet')),
      L("Now look only at the gap column. Twenty-four, sixteen, eight, zero.", show(rsH['box'], 'look only at the gap column')),
      L("Every hour, the gap shrinks by the same eight kilometers."),
      L("Why eight? Because every hour, Mia closes three kilometers, and Leo closes five."),
      L("Three plus five is eight. So the gap shrinks by eight every hour.", show(rsHk, 'Three plus five is eight')),
      L("So we don't need to find where each of them is. We only follow the gap.")),
    S('They meet: together, the whole gap',
      L("Now look at the moment they meet, after three hours.", show(rsT['line'], 'the moment they meet'),
        show(rsT['ends'], 'the moment they meet')),
      L("Mia walked nine kilometers, from her start to the meeting point.", show(rsT['a'], 'Mia walked nine kilometers')),
      L("Leo walked fifteen kilometers, from his start to the same point.", show(rsT['b'], 'Leo walked fifteen kilometers')),
      L("Together, their two pieces make the whole road between them. Nine plus fifteen is twenty-four.",
        show(rsT['all'], 'make the whole road'), show(rsTa, 'Nine plus fifteen')),
      L("So they meet when together they have covered the whole gap.", show(rsTk, 'they meet when together')),
      L("Every hour, together they cover eight kilometers. They need to cover twenty-four."),
      L("How many hours is that? Twenty-four divided by eight is three hours.", show(rsTb, 'Twenty-four divided by eight')),
      L("That's the quick way. The time is the gap divided by the relative speed.",
        show(rsTf, 'The time is the gap divided'))),
    S('Toward each other: add',
      L("Here's an easy way to remember that we add."),
      L("Imagine a truck that drives at twenty kilometers per hour. A car drives toward it at fifty.",
        show(rsC['line'], 'Imagine a truck'), show(rsC['dots'], 'Imagine a truck'), show(rsC['arrT'], 'twenty kilometers per hour'),
        show(rsC['arrC'], 'A car drives toward it')),
      L("In one hour, the truck covers twenty kilometers, and the car covers fifty."),
      L("So together, they close twenty plus fifty, seventy kilometers every hour.", show(rsCa, 'twenty plus fifty, seventy')),
      L("If they crash, it's like a crash at seventy. Toward each other, we add the speeds.",
        show(rsCk, 'Toward each other, we add'))),
    S('Another example',
      L("Now a new example, with different numbers."),
      L("Sara and Tom start fifty kilometers apart, and ride toward each other.",
        show(rsE['line'], 'Sara and Tom start'), show(rsE['dots'], 'Sara and Tom start'), show(rsE['gap'], 'fifty kilometers apart')),
      L("Sara rides at twelve kilometers per hour, and Tom rides at eight.",
        show(rsE['arrS'], 'Sara rides at twelve'), show(rsE['arrT'], 'Tom rides at eight')),
      L("They ride toward each other, so we add the speeds. Twelve plus eight is twenty.", show(rsEa, 'Twelve plus eight')),
      L("So the gap shrinks by twenty kilometers every hour. Let's follow the gap."),
      L("At the start, the gap is fifty kilometers.", show(rsEs['line'], 'At the start, the gap')),
      L("After one hour, it's fifty minus twenty, thirty.", show(rsEs['c1'], 'fifty minus twenty, thirty')),
      L("After two hours, it's thirty minus twenty, ten.", show(rsEs['c2'], 'thirty minus twenty, ten')),
      L("Now only ten kilometers are left. That's less than one hour of riding."),
      L("Ten is half of twenty. So they need half an hour more. They meet after two and a half hours.",
        show(rsEs['c3'], 'They meet after two and a half')),
      L("The quick way gives the same answer. Fifty divided by twenty is two and a half hours.",
        show(rsEb, 'Fifty divided by twenty')),
      L("Two and a half hours is two hours and thirty minutes.", show(rsEc, 'two hours and thirty minutes'))),
    S('Check: together, the whole gap',
      L("Let's check that they really meet after two and a half hours.", show(rsK['line'], "Let's check"),
        show(rsK['ends'], "Let's check")),
      L("In two and a half hours, Sara rides twelve times two and a half. That's thirty kilometers.",
        show(rsKa, 'Sara rides twelve times'), show(rsK['a'], "That's thirty kilometers")),
      L("Tom rides eight times two and a half. That's twenty kilometers.",
        show(rsKb, 'Tom rides eight times'), show(rsK['b'], "That's twenty kilometers")),
      L("Thirty plus twenty is fifty. Together they covered the whole gap, so they meet.",
        show(rsKc, 'Thirty plus twenty'), show(rsK['all'], 'covered the whole gap'))),
    S('Moving apart, hour by hour',
      L("Now a new example, with the same Mia and Leo. This time, they start from the same point.",
        show(rsA['line'], 'start from the same point'), show(rsA['d0'], 'start from the same point')),
      L("They walk in opposite directions, away from each other."),
      L("At the start, the gap between them is zero.", show(rsA['g0'], 'the gap between them is zero')),
      L("Mia walks three kilometers per hour, and Leo walks five.", show(rsA['vA'], 'Mia walks three'),
        show(rsA['vB'], 'Leo walks five')),
      L("After one hour, Mia is three kilometers from the start, on one side.", show(rsA['r1'], 'After one hour'),
        show(rsA['a1'], 'Mia is three kilometers')),
      L("Leo is five kilometers from the start, on the other side.", show(rsA['b1'], 'Leo is five kilometers')),
      L("So the gap is three plus five, eight kilometers.", show(rsA['c1'], 'three plus five'), show(rsA['g1'], 'eight kilometers')),
      L("After two hours, Mia is six kilometers from the start, and Leo is ten.", show(rsA['r2'], 'After two hours'),
        show(rsA['a2'], 'Mia is six kilometers'), show(rsA['b2'], 'Leo is ten')),
      L("The gap grows by eight again. Eight plus eight is sixteen.", show(rsA['c2'], 'grows by eight again'),
        show(rsA['g2'], 'Eight plus eight')),
      L("After three hours, Mia is nine kilometers from the start, and Leo is fifteen.", show(rsA['r3'], 'After three hours'),
        show(rsA['a3'], 'Mia is nine kilometers'), show(rsA['b3'], 'Leo is fifteen')),
      L("The gap grows by eight once more. Sixteen plus eight is twenty-four.", show(rsA['c3'], 'by eight once more'),
        show(rsA['g3'], 'Sixteen plus eight')),
      L("Look at the gap column again. Zero, eight, sixteen, twenty-four.", show(rsA['box'], 'Look at the gap column')),
      L("Every hour, the gap grows by the same eight kilometers."),
      L("They walk in opposite directions, so again we add. Three plus five is eight.", show(rsAk, 'Three plus five is eight'))),
    S('Moving apart: two questions',
      L("Now two quick questions about Mia and Leo."),
      L("How far apart are they after five hours? The gap grows by eight every hour."),
      L("So after five hours, the gap is five times eight, forty kilometers.", show(rsQa, 'five times eight')),
      L("And when are they twenty kilometers apart? We need a gap of twenty."),
      L("The gap grows by eight every hour. Twenty divided by eight is two and a half hours.",
        show(rsQb, 'Twenty divided by eight')),
      L("Now a new example. Two cars leave the same town at the same time, in opposite directions.",
        show(rsQ['line'], 'Two cars leave'), show(rsQ['town'], 'Two cars leave'), show(rsQ['dots'], 'the same town')),
      L("One drives at forty kilometers per hour, and the other at sixty.", show(rsQ['arr1'], 'One drives at forty'),
        show(rsQ['arr2'], 'the other at sixty')),
      L("Opposite directions, so we add. Forty plus sixty is a hundred kilometers every hour.",
        show(rsQc, 'Forty plus sixty')),
      L("When are they a hundred fifty kilometers apart? The gap grows by a hundred every hour. So a hundred fifty "
        "divided by a hundred is one and a half hours.",
        show(rsQd, 'A hundred fifty divided by a hundred')),
      L("So toward each other or apart, we add the speeds.", show(rsQk, 'toward each other or apart'))),
    # ---- part 2
    S('A chase, hour by hour',
      L("In a chase, both of them move the same way, and one tries to catch the other."),
      L("Now a new example. A runner runs at six kilometers per hour.", show(rsS['line'], 'A runner runs'),
        show(rsS['dR'], 'A runner runs'), show(rsS['vR'], 'six kilometers per hour')),
      L("A cyclist rides behind her on the same road, at nine kilometers per hour.",
        show(rsS['dC'], 'A cyclist rides behind her'), show(rsS['vC'], 'at nine kilometers')),
      L("At the start, the runner is nine kilometers ahead of him.", show(rsS['h0'], 'nine kilometers ahead'),
        show(rsS['g0'], 'nine kilometers ahead')),
      L("After one hour, the cyclist rode nine kilometers.", show(rsS['r1'], 'After one hour'),
        show(rsS['a1'], 'the cyclist rode nine')),
      L("But the runner didn't wait. She ran six kilometers further.", show(rsS['b1'], 'She ran six kilometers')),
      L("So he gained only nine minus six, three kilometers. The gap is nine minus three, six.",
        show(rsS['c1'], 'nine minus six, three'), show(rsS['g1'], 'The gap is nine minus three')),
      L("After two hours, he rode eighteen kilometers, and she ran twelve.", show(rsS['r2'], 'After two hours'),
        show(rsS['a2'], 'he rode eighteen'), show(rsS['b2'], 'she ran twelve')),
      L("He gained three kilometers again. Six minus three is three.", show(rsS['c2'], 'He gained three kilometers again'),
        show(rsS['g2'], 'Six minus three')),
      L("After three hours, he rode twenty-seven kilometers, and she ran eighteen.", show(rsS['r3'], 'After three hours'),
        show(rsS['a3'], 'he rode twenty-seven'), show(rsS['b3'], 'she ran eighteen')),
      L("He gained three once more. Three minus three is zero. He catches her.",
        show(rsS['c3'], 'He gained three once more'), show(rsS['g3'], 'Three minus three'), show(rsS['m3'], 'He catches her')),
      L("Look at the gap column. Nine, six, three, zero.", show(rsS['box'], 'Look at the gap column')),
      L("Every hour, the gap closes by the same three kilometers."),
      L("Why three? Because he rides nine, but she runs away six. Nine minus six is three.",
        show(rsSk, 'Nine minus six is three')),
      L("Imagine the slow one stands still. Then the cyclist comes closer at only three kilometers per hour."),
      L("So in a chase, we subtract the speeds.")),
    S('He catches her: the whole head start',
      L("Now look at the moment he catches her, after three hours.", show(rsU['line'], 'the moment he catches her'),
        show(rsU['ends'], 'the moment he catches her')),
      L("The runner ran eighteen kilometers, from her start to the meeting point.", show(rsU['r'], 'The runner ran eighteen')),
      L("The cyclist rode twenty-seven kilometers. He rode her nine-kilometer head start, and then her eighteen kilometers too.",
        show(rsU['c'], 'The cyclist rode twenty-seven'), show(rsU['h'], 'her nine-kilometer head start')),
      L("So his distance minus her distance is the head start. Twenty-seven minus eighteen is nine.",
        show(rsUa, 'Twenty-seven minus eighteen')),
      L("He catches her when he has gained the whole starting gap.", show(rsUk, 'He catches her when')),
      L("He gains three kilometers every hour, and he needs nine. Nine divided by three is three hours.",
        show(rsUb, 'Nine divided by three')),
      L("So in a chase, the time is the starting gap divided by the difference of the speeds.",
        show(rsUf, 'the time is the starting gap'))),
    S('Another chase',
      L("Now a new example. A bus drives at fifty kilometers per hour. A car drives behind it, at seventy.",
        show(rsV['line'], 'A bus drives'), show(rsV['bus'], 'A bus drives'), show(rsV['arrB'], 'fifty kilometers per hour'),
        show(rsV['car'], 'A car drives behind it'), show(rsV['arrC'], 'at seventy')),
      L("At the start, the bus is ten kilometers ahead of the car.", show(rsV['gap'], 'ten kilometers ahead')),
      L("It's a chase, so we subtract. The car gains seventy minus fifty, twenty kilometers every hour.",
        show(rsVa, 'seventy minus fifty')),
      L("It needs to gain ten kilometers. Ten divided by twenty is half an hour.", show(rsVb, 'Ten divided by twenty')),
      L("So the car catches the bus after thirty minutes.", show(rsVc, 'after thirty minutes')),
      L("And what if the faster one is in front? Then the gap doesn't close. It grows."),
      L("Say the car is in front and drives away from the bus. The gap grows by seventy minus fifty, twenty kilometers every hour.",
        show(rsVd, 'The gap grows by seventy minus fifty')),
      L("The same direction, so we still subtract the speeds.")),
]
s4a = IH('s4a', 'only the starting gap counts', size=32)
s4b = IH('s4b', '$102-100=2$ km an hour', size=32)
s4s = ROAD('s4s', [
    ('ends', [('end', 0, ''), ('above', 0, 'home')]),
    ('dan', [('dot', 0, ''), ('arrow', 0, .3, 'Dan: 4 kph, from 0 min')]),
    ('dan2', [('dot', .4, 'Dan at 30 min')]),
    ('sis', [('dot', 0, '', 'orange'), ('arrow', 0, .3, 'sister: 12 kph, from 30 min', 1, 'orange')]),
    ('gap', [('gap', 0, .4, 'gap: 2 km')])], w=1100)
s4c = IH('s4c', 'half an hour: $\\ 4\\times\\frac{1}{2}=2$ km', size=32)
s4d = IH('s4d', 'she gains $12-4=8$ km an hour', size=32)
s4e = IH('s4e', '$2\\div8=\\frac{1}{4}$ hour $=15$ minutes', size=32)
s5s = ROAD('s5s', [
    ('ends', [('end', 0, 'start')]),
    ('ava', [('dot', 0, ''), ('arrow', 0, .35, 'Ava starts at 0 s')]),
    ('ben', [('dot', 0, '', 'orange'), ('arrow', 0, .35, 'Ben starts at 10 s', 1, 'orange')]),
    ('meet', [('meet', .8, 'meet: 30 s after Ava starts')])], w=1100)
s5a = IH('s5a', 'Ava runs $30$ s, $\\ $Ben runs $30-10=20$ s', size=32)
s5b = IH('s5b', 'the same distance: $\\ $the times flip', size=32)
s5c = IH('s5c', 'times $30:20=3:2$', size=32)
s5d = IH('s5d', 'Ben is $\\frac{3}{2}$ times as fast', size=32)
s5e = IH('s5e', 'from Ben\'s start: $\\ $Ben $30$ s, $\\ $Ava $40$ s', size=32)
s5f = IH('s5f', 'Ben is $\\frac{40}{30}=\\frac{4}{3}$ times as fast', size=32)
s5g = I('s5g', 'From whose start is the time counted?', size=34)
s6a = I('s6a', 'Toward each other or apart: $\\ $add the speeds', size=34)
s6b = I('s6b', 'A chase: $\\ $subtract the speeds', size=34)
s6e = I('s6e', 'Meet: $\\ $together they cover the whole gap', size=34)
s6f = I('s6f', 'time $=$ the gap $\\div$ the relative speed', size=34)
s6c = I('s6c', 'Only the starting gap counts. $\\ $A head start: $\\ $find it first.', size=34)
s6d = I('s6d', 'Mark every start time. $\\ $From whose start?', size=34)
_wp113 += [
    S('Only the starting gap',
      L("Here's the classic mistake, and it's almost always in a chase."),
      L("The only distance that matters is the gap between them when the chase starts. Not the whole way they ride, and "
        "not where they end up.", show(s4a, 'The only distance that matters')),
      L("Imagine the runner at a hundred kilometers per hour, and the cyclist at a hundred and two. They travel very far, "
        "but the gap still closes by only two kilometers every hour.", show(s4b, 'the gap still closes by only two')),
      L("So in a chase, we only look at the starting gap, and at the difference between the speeds.")),
    S('A head start',
      L("And when one of them leaves earlier, we first find the head start. That head start is the gap."),
      L("Now a new example. Dan walks from home at four kilometers per hour. Half an hour later, his sister rides after "
        "him at twelve kilometers per hour. When does she catch him?", show(s4s['line'], 'Dan walks from home'),
        show(s4s['ends'], 'Dan walks from home'), show(s4s['dan'], 'at four kilometers per hour')),
      L("We solve it in two stages. In the first stage, only Dan walks. In the second stage, both of them move."),
      L("So first, the head start. In half an hour, Dan walks four times a half, two kilometers.",
        show(s4c, 'Dan walks four times a half'), show(s4s['dan2'], 'two kilometers.')),
      L("Now the second stage. His sister starts, so we mark her start time on the sketch. The gap between them is two kilometers.",
        show(s4s['sis'], 'His sister starts'), show(s4s['gap'], 'The gap between them is two kilometers')),
      L("It's a chase, so we subtract. She gains twelve minus four, eight kilometers every hour.",
        show(s4d, 'She gains twelve minus four')),
      L("Two divided by eight is a quarter of an hour. So she catches him fifteen minutes after she starts.",
        show(s4e, 'Two divided by eight'))),
    S('From whose start?',
      L("Now careful with the time in a chase. Is it counted from the chaser's start, or from the first one's start? We "
        "read the question, and we mark both start times on the sketch.", show(s5g, 'Is it counted from the chaser')),
      L("Now a new example. Ava starts running. Ben waits ten seconds, and then chases her on the same route. He "
        "catches her thirty seconds after Ava started. How many times as fast as Ava is Ben?",
        show(s5s['line'], 'Ava starts running'), show(s5s['ends'], 'Ava starts running'), show(s5s['ava'], 'Ava starts running'),
        show(s5s['ben'], 'Ben waits ten seconds'), show(s5s['meet'], 'thirty seconds after Ava started')),
      L("The thirty seconds are counted from Ava's start. So Ava runs thirty seconds, and Ben runs only thirty minus ten, "
        "twenty seconds.", show(s5a, 'Ben runs only thirty minus ten')),
      L("They both run the same distance, from the start to the meeting point. The distance is fixed, so the times flip, "
        "like in speed ratios.", show(s5b, 'The distance is fixed, so the times flip')),
      L("Ava's time to Ben's time is thirty to twenty, three to two. So Ben's speed is three halves of Ava's. He is one "
        "and a half times as fast.", show(s5c, 'thirty to twenty, three to two'), show(s5d, 'one and a half times as fast'))),
    S('Change whose start we count from',
      L("Now change just the last part of the question. Ben still starts ten seconds after Ava. But suppose Ben catches Ava thirty seconds after Ben starts. Ben runs thirty seconds, and Ava runs "
        "ten more, forty.", show(s5e, 'Ben runs thirty seconds')),
      L("Then Ben is forty over thirty, four thirds times as fast.", show(s5f, 'forty over thirty')),
      L("Two readings, two different answers. So always ask, from whose start is the time counted?")),
    S('Recap',
      L("So let's sum it up. Toward each other, or apart, we add the speeds.", show(s6a, 'Toward each other, or apart')),
      L("In a chase, we subtract them.", show(s6b, 'In a chase, we subtract them')),
      L("They meet when together they cover the whole gap. And the time is the gap divided by the relative speed.",
        show(s6e, 'They meet when together'), show(s6f, 'the time is the gap divided')),
      L("Only the starting gap counts. And if one leaves earlier, we find the head start first.", show(s6c, 'Only the starting gap counts')),
      L("And we mark every start time on the sketch, and ask from whose start the time is counted.", show(s6d, 'we mark every start time')),
      L("Chases are where students slip, so take a moment to memorize this. I'll see you in the next video.")),
]
video('wp-113', 'lesson', slides=_wp113)
SPLITS.append(('wp-113', 'Relative Speed', [
    (1, None),
    (9, "Let's continue with relative speed, and look at chases.")]))

# ------------------------------------------------------------------------------------------------ g114 (runners moving apart)
# Hebrew (wp 7501-7528, Shimon and Roi, 6 and 4 kph apart, 500 m): apart -> add (10); 500 m = half a km (same units);
# 1/2 / 10 = 1/20 h -> 3 min. English: 8 + 10 = 18, 1.8 km -> 1/10 h -> 6 min. First use of "apart -> add" (wp-113),
# "like in the lesson". Trap at its step: 10 (a tenth of an hour is not ten minutes). Method 2 (English): identical
# ratios (18 km in 60 minutes -> 1.8 km in 6 minutes).
g14s = ROAD('g14s', [
    ('dots', [('dot', .5, 'the gate', 'ink')]),
    ('arr', [('arrow', .47, .1, '8 kph'), ('arrow', .53, .9, '10 kph', 0, 'orange')]),
    ('gap', [('gap', .1, .9, '1800 m apart')])], w=760)
g14a = IH('g14a', 'apart: $\\ 8+10=18$ km an hour', size=30)
g14b = IH('g14b', '$1800$ m $=1.8$ km', size=30)
g14c = IH('g14c', 'time $=1.8\\div18=\\frac{1}{10}$ hour', size=30, col=1)
g14d = IH('g14d', '$\\frac{1}{10}$ of $60$ minutes $=6$ minutes', size=30, col=1)
g14e = IH('g14e', '$\\frac{1}{10}$ hour $\\ne10$ minutes', size=30, col=1)
g14t = TBL('g14t', ['Time', 'Gap'], ['', ''], [
    ('r1', [('c', 0, 0, '60 min'), ('c', 0, 1, '18 km')]),
    ('r2', [('c', 1, 1, '1.8 km'), ('down', 1, 0, 1, '÷10')]),
    ('ans', [('cover', 1, 0, '6 min'), ('down', 0, 0, 1, '÷10')])], colw=190, labw=0, rowh=62, side=90, w=540)
video('solve-wp27-g114', 'solution', qid='wp27-g114', slides=[
    S('Method 1 · The math way: relative speed',
      L("Two runners leave the same gate at the same time, and run in opposite directions along a straight path. Their "
        "speeds are eight and ten kilometers per hour. After how many minutes are they one thousand eight hundred meters "
        "apart?", pt('stem', 'Two runners leave the same gate', 'hl', 11.0), voice='calm', pause=0.5),
      L("So they move apart, and they ask when the gap is one thousand eight hundred meters. They ask for minutes.",
        pt('stem: ask', 'They ask for minutes'), show(g14s['line'], 'So they move apart'), show(g14s['dots'], 'So they move apart'),
        show(g14s['arr'], 'So they move apart')),
      L("We'll solve it in two different ways. Let's start with the math way, with relative speed, like in the lesson. "
        "They move in opposite directions, so we add the speeds.", show(g14s['gap'], 'with relative speed')),
      L("Eight plus ten is eighteen. So the gap grows by eighteen kilometers every hour.", show(g14a, 'Eight plus ten is eighteen')),
      L("The gap is in meters, but the speed is in kilometers per hour. The units must match. One thousand eight hundred "
        "meters is one point eight kilometers.", show(g14b, 'One thousand eight hundred meters is one point eight')),
      L("The time is the gap divided by the speed. One point eight divided by eighteen is one tenth. So it takes a tenth "
        "of an hour.", show(g14c, 'One point eight divided by eighteen')),
      L("Careful, a tenth of an hour is not ten minutes. Ten, choice number two, is the trap.", show(g14e, 'a tenth of an hour is not ten minutes'),
        mk('cross', 'choice 2', 'is the trap')),
      L("They ask for minutes. A tenth of sixty minutes is six minutes.", show(g14d, 'A tenth of sixty minutes'))),
    S('Method 2 · Understanding: identical ratios',
      L("[pause] Now by understanding, with identical ratios. We start again from the givens. Moving apart, the gap grows "
        "by eight plus ten, eighteen kilometers in sixty minutes.", show(g14t['line'], 'Moving apart'), show(g14t['r1'], 'eighteen kilometers in sixty minutes')),
      L("We need a gap of one point eight kilometers. From eighteen to one point eight, we divide by ten.",
        show(g14t['r2'], 'We need a gap of one point eight')),
      L("So we divide the time by ten too. Sixty divided by ten is six minutes.", show(g14t['ans'], 'Sixty divided by ten')),
      L("Choice number one is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g115 (the bus and the car)
# Hebrew (wp 7531-7575, the truck 6:00 at 80, the car 6:30 at 100, 130 km): stage 1, the truck alone for half an hour
# -> 40 km, 90 left; stage 2, toward each other -> 180; "the distance in the table is always the gap between them";
# 90 / 180 = 1/2 -> 7:00; "always draw, even calculate on the sketch". English: 09:00 bus at 72, 09:20 car at 108,
# 204 km -> 10:20. Method 2 (English): plugging in the answers (10:20: the bus 1 h 20 min = 96 km, the car 108 km,
# 96 + 108 = 204). Trap at its step: 10:08 (both from 9:00, the head start ignored).
g15s = ROAD('g15s', [
    ('ends', [('end', 0, 'Oakton'), ('end', 1, 'Bayside')]),
    ('bus', [('dot', 0, ''), ('arrow', 0, .35, 'bus 72 kph, from 9:00')]),
    ('stage1', [('seg', 0, 24 / 204.), ('dot', 24 / 204., '9:20')]),
    ('car', [('dot', 1, '', 'orange'), ('arrow', 1, .65, 'car 108 kph, from 9:20', 0, 'orange')]),
    ('gap', [('gap', 24 / 204., 1, '180 km left')]),
], w=900)
g15t = ROAD('g15t', [
    ('ends', [('end', 0, 'Oakton'), ('end', 1, 'Bayside')]),
    ('bus', [('dot', 0, ''), ('arrow', 0, .35, 'bus 72 kph, from 9:00'), ('seg', 0, 24 / 204.), ('dot', 24 / 204., '9:20'),
             ('gap', 24 / 204., 1, '180 km left')]),
    ('car', [('dot', 1, '', 'orange'), ('arrow', 1, .65, 'car 108 kph, from 9:20', 0, 'orange')]),
    ('meet', [('meet', (24 + 72) / 204., 'they meet')])], w=900)
g15a = IH('g15a', '$20$ minutes $=\\frac{1}{3}$ hour', size=30)
g15b = IH('g15b', '$72\\times\\frac{1}{3}=24$ km', size=30)
g15c = IH('g15c', '$204-24=180$ km left', size=30, col=1)
g15d = IH('g15d', 'toward each other: $\\ 72+108=180$ kph', size=30, col=1)
g15e = IH('g15e', '$180\\div180=1$ hour', size=30, col=1)
g15f = IH('g15f', '$9:20+1$ hour $=10:20$', size=30, col=1)
g15g = IH('g15g', 'try $10:20$: $\\ $the bus drives $1\\frac{1}{3}$ hours', size=30)
g15h = IH('g15h', '$72\\times\\frac{4}{3}=24\\times4=96$ km', size=30)
g15i = IH('g15i', 'the car drives $1$ hour: $\\ 108$ km', size=30, col=1)
g15j = IH('g15j', '$96+108=204$ km', size=30, col=1)
video('solve-wp27-g115', 'solution', qid='wp27-g115', slides=[
    S('Method 1 · The math way: a head start, then together',
      L("At nine o'clock a bus leaves Oakton for Bayside at seventy-two kilometers per hour. At nine twenty a car leaves "
        "Bayside for Oakton at a hundred eight kilometers per hour. The towns are two hundred four kilometers apart. When "
        "do they meet?", pt('stem', 'a bus leaves Oakton', 'hl', 13.0), voice='calm', pause=0.5),
      L("So they drive toward each other, but the bus leaves twenty minutes earlier. They ask for the clock time of the "
        "meeting.", pt('stem: ask', 'They ask for the clock time')),
      L("We'll solve it in two different ways. Let's start with the math way, in two stages, like in the lesson. First we "
        "draw the sketch.", show(g15s['line'], 'First we draw the sketch'), show(g15s['ends'], 'First we draw the sketch')),
      L("Let's start with stage one. From nine to nine twenty, only the bus drives.", show(g15s['bus'], 'only the bus drives')),
      L("Twenty minutes is a third of an hour. The bus drives seventy-two times a third, twenty-four kilometers.",
        show(g15a, 'Twenty minutes is a third'), show(g15b, 'seventy-two times a third'), show(g15s['stage1'], 'twenty-four kilometers.')),
      L("The whole road is two hundred four kilometers. So at nine twenty, two hundred four minus twenty-four, a hundred "
        "eighty kilometers are left between them.", show(g15c, 'two hundred four minus twenty-four'), show(g15s['gap'], 'a hundred eighty kilometers are left'))),
    S('Method 1 · The math way: a head start, then together',
      L("Now stage two. At nine twenty the car starts, toward the bus.", show(g15t['line'], 'Now stage two'), show(g15t['ends'], 'Now stage two'),
        show(g15t['bus'], 'Now stage two'), show(g15t['car'], 'At nine twenty the car starts')),
      L("They drive toward each other, so we add the speeds. Seventy-two plus a hundred eight is a hundred eighty "
        "kilometers per hour.", show(g15d, 'Seventy-two plus a hundred eight')),
      L("The distance that matters is the gap between them, a hundred eighty kilometers. A hundred eighty divided by a "
        "hundred eighty is one hour.", show(g15e, 'A hundred eighty divided by a hundred eighty')),
      L("Careful, that's one hour after nine twenty, when the gap started. It's not one hour after nine.",
        show(g15t['meet'], 'one hour after nine twenty')),
      L("Nine twenty plus one hour is ten twenty.", show(g15f, 'Nine twenty plus one hour')),
      L("Ten oh eight, choice number one, starts both at nine and forgets the head start.", mk('cross', 'choice 1', 'forgets the head start'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. We'll check ten twenty first. That gives the car exactly one hour, so the calculation is easy."),
      L("Until ten twenty, the bus drives from nine, so one hour and twenty minutes. That's one and a third hours.",
        show(g15g, 'the bus drives from nine')),
      L("Seventy-two times four thirds. A third of seventy-two is twenty-four, and times four is ninety-six kilometers.",
        show(g15h, 'A third of seventy-two')),
      L("The car drives from nine twenty, so exactly one hour. That's a hundred eight kilometers.",
        show(g15i, 'The car drives from nine twenty')),
      L("When they meet, together they have covered the whole road. Ninety-six plus a hundred eight is two hundred four. "
        "That's exactly the road.", show(g15j, 'Ninety-six plus a hundred eight')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g116 (Zoe and Sam)
# Hebrew (wp 7578-7643, Miki 4 kph, his father leaves a quarter of an hour later and catches him half an hour later):
# the head start (1 km), "the common mistake: only the starting gap counts", 1 / (1/2) = 2 = how much FASTER the father
# is, not his speed ("at 2 he'd never catch him") -> 6. English: Zoe 15 kph, Sam 12 minutes later, catches her 20
# minutes after he starts -> 3 km, 9 faster, 24. "Twenty minutes after HE starts": the from-whose-start check of wp-113,
# said at its step. Method 2 (English): both cover the same 8 km.
g16s = ROAD('g16s', [
    ('ends', [('end', 0, 'home')]),
    ('zoe', [('dot', 0, ''), ('arrow', 0, .3, 'Zoe: 15 kph, from 0 min')]),
    ('zoe2', [('dot', .375, 'Zoe at 12 min')]),
    ('sam', [('dot', 0, '', 'orange'), ('arrow', 0, .3, 'Sam: ?, from 12 min', 1, 'orange')]),
    ('gap', [('gap', 0, .375, 'gap: 3 km')]),
    ('meet', [('meet', 1, 'caught: 12 + 20 min')])], w=900)
g16a = IH('g16a', '$12$ minutes $=\\frac{1}{5}$ hour', size=30)
g16b = IH('g16b', '$15\\times\\frac{1}{5}=3$ km ahead', size=30, col=1)
g16c = IH('g16c', '$20$ minutes $=\\frac{1}{3}$ hour', size=30)
g16d = IH('g16d', '$3\\div\\frac{1}{3}=3\\times3=9$', size=30)
g16e = IH('g16e', '$9$: $\\ $how much FASTER, $\\ $not his speed', size=30, col=1)
g16f = IH('g16f', '$15+9=24$ kph', size=30, col=1)
g16g = IH('g16g', 'Zoe: $\\ 12+20=32$ minutes', size=30)
g16h = IH('g16h', '$15$ km in $60$ minutes: $\\ \\frac{1}{4}$ km a minute', size=30)
g16i = IH('g16i', '$32\\times\\frac{1}{4}=8$ km', size=30)
g16j = IH('g16j', 'Sam: $\\ 8$ km in $\\frac{1}{3}$ hour', size=30, col=1)
g16k = IH('g16k', '$8\\div\\frac{1}{3}=8\\times3=24$ kph', size=30, col=1)
video('solve-wp27-g116', 'solution', qid='wp27-g116', slides=[
    S('Method 1 · The math way: relative speed',
      L("Zoe rides her bike from home at fifteen kilometers per hour. Twelve minutes later, her brother Sam leaves home "
        "along the same route, and catches up with Zoe twenty minutes after he starts. What is Sam's speed?",
        pt('stem', 'Zoe rides her bike from home', 'hl', 11.0), voice='calm', pause=0.5),
      L("So it's a chase, with a head start. And the twenty minutes are counted from Sam's start, because they say after "
        "he starts.", pt('stem: given', 'twenty minutes are counted from Sam')),
      L("We'll solve it in two different ways. Let's start with the math way, with relative speed, like in the lesson. "
        "First, the sketch.", show(g16s['line'], 'First, the sketch'), show(g16s['ends'], 'First, the sketch'),
        show(g16s['zoe'], 'First, the sketch')),
      L("How far ahead is Zoe when Sam leaves? Twelve minutes is a fifth of an hour.", show(g16a, 'Twelve minutes is a fifth')),
      L("Fifteen times a fifth is three. So Zoe is three kilometers ahead.", show(g16b, 'Fifteen times a fifth'),
        show(g16s['zoe2'], 'So Zoe is three kilometers ahead')),
      L("Now Sam starts. The only distance that matters is that three-kilometer gap. Not the whole way they ride.",
        show(g16s['sam'], 'Now Sam starts'), show(g16s['gap'], 'that three-kilometer gap')),
      L("So Sam has a gap of three kilometers to close.")),
    S('Method 1 · The math way: relative speed',
      L("Sam closes the three-kilometer gap in twenty minutes, a third of an hour.", show(g16c, 'twenty minutes, a third of an hour')),
      L("The gap divided by the time is three divided by a third. That's three times three, nine.",
        show(g16d, 'three divided by a third')),
      L("Now careful, because nine is not Sam's speed. In a chase we subtract, so nine is how much faster Sam is than Zoe.",
        show(g16e, 'nine is not Sam')),
      L("At nine kilometers per hour he would never catch her, because she rides at fifteen. Nine, choice number one, is "
        "the trap.", mk('cross', 'choice 1', 'is the trap')),
      L("So Sam's speed is Zoe's fifteen plus nine, twenty-four kilometers per hour.", show(g16f, "Zoe's fifteen plus nine"))),
    S('Method 2 · The math way: the same distance',
      L("[pause] Now the math way, with the distances. We start again from the givens. When Sam catches Zoe, they are at "
        "the same place. So they both rode the same distance from home."),
      L("Zoe rode twelve minutes before Sam, and twenty minutes with him. Twelve plus twenty is thirty-two minutes.",
        show(g16g, 'Twelve plus twenty is thirty-two')),
      L("Fifteen kilometers per hour is fifteen kilometers in sixty minutes. That's a quarter of a kilometer every "
        "minute.", show(g16h, 'a quarter of a kilometer every minute')),
      L("Thirty-two times a quarter is eight. So Zoe rode eight kilometers.", show(g16i, 'Thirty-two times a quarter')),
      L("Sam rode the same eight kilometers in twenty minutes, a third of an hour.", show(g16j, 'Sam rode the same eight')),
      L("Eight divided by a third is eight times three, twenty-four kilometers per hour. The same answer.",
        show(g16k, 'Eight divided by a third')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g117 (motorbike and train)
# Hebrew (wp 7648-7764, car A 8 km in 10 min, car B 10 km in 8 min): (1) the calculation, minutes -> hours (÷60),
# 8 ÷ 1/6 = 48, 10 ÷ 8/60 = 75, and two mental-subtraction tips for 75 - 48 (add 2 to both; walk via a round anchor);
# (2) identical ratios, "the way I recommend": 10 -> 60 minutes is x6; for B, her paths to x7.5, and "if you don't see
# it, the triangle value" (Hebrew-vs-English #2: restored). English: 9 km / 15 min (36) and 15 km / 9 min (100) -> 64;
# the same two tips (add 4: 104 - 40; walk 36 -> 40 -> 100); the ratio step ÷3 then x20, and the triangle value
# (REMINDER, topic 22) for whoever doesn't see it. Trap: 136 adds the speeds.
g17a = IH('g17a', '$15$ minutes $=\\frac{1}{4}$ hour', size=30)
g17b = IH('g17b', '$9\\div\\frac{1}{4}=9\\times4=36$ kph', size=30)
g17c = IH('g17c', '$9$ minutes $=\\frac{9}{60}$ hour', size=30)
g17d = IH('g17d', '$15\\div\\frac{9}{60}=\\frac{15\\times60}{9}$', size=30, col=1)
g17e = IH('g17e', '$=\\frac{900}{9}=100$ kph', size=30, col=1)
g17sf = I('g17sf', 'So far: $\\ $motorbike $36$ kph, $\\ $train $100$ kph', size=30)
g17f = IH('g17f', '$100-36$', size=32)
g17g = IH('g17g', '$104-40=64$', size=30)
g17h = IH('g17h', '$36\\to40$: $\\ 4$, $\\ 40\\to100$: $\\ 60$', size=30)
g17i = IH('g17i', '$4+60=64$', size=30)
g17t = TBL('g17t', ['Time', 'Distance'], ['', ''], [
    ('r1', [('c', 0, 0, '15 min'), ('c', 0, 1, '9 km')]),
    ('r2', [('c', 1, 0, '60 min'), ('down', 0, 0, 1, '×4')]),
    ('ans', [('cover', 1, 1, '36 km'), ('down', 1, 0, 1, '×4')])], colw=180, labw=0, rowh=60, side=80, w=480)
g17u = TBL('g17u', ['Time', 'Distance'], ['', '', ''], [
    ('r1', [('c', 0, 0, '9 min'), ('c', 0, 1, '15 km')]),
    ('r2', [('c', 1, 0, '3 min'), ('c', 1, 1, '5 km'), ('down', 0, 0, 1, '÷3'), ('down', 1, 0, 1, '÷3')]),
    ('r3', [('c', 2, 0, '60 min'), ('down', 0, 1, 2, '×20')]),
    ('ans', [('cover', 2, 1, '100 km'), ('down', 1, 1, 2, '×20')])], colw=180, labw=0, rowh=58, side=80, w=480, col=1)
g17v = IH('g17v', '$\\frac{15\\times60}{9}=100$', size=30)
g17w = IH('g17w', '$100-36=64$', size=30)
video('solve-wp27-g117', 'solution', qid='wp27-g117', slides=[
    S('Method 1 · The math way: hours',
      L("A motorbike travels nine kilometers in fifteen minutes. A train travels fifteen kilometers in nine minutes. What "
        "is the difference between their speeds, in kilometers per hour?", pt('stem', 'A motorbike travels', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("So they ask for speeds in kilometers per hour, but the times are in minutes. The units don't match.",
        pt('stem: ask', 'they ask for speeds')),
      L("We'll solve it in two different ways. Let's start with the math way. We turn the minutes into hours."),
      L("Let's start with the motorbike. Fifteen minutes is fifteen out of sixty, a quarter of an hour.", show(g17a, 'Fifteen minutes is fifteen out of sixty')),
      L("The speed is the distance divided by the time. Nine divided by a quarter is nine times four, thirty-six "
        "kilometers per hour.", show(g17b, 'Nine divided by a quarter')),
      L("Now the train. Nine minutes is nine sixtieths of an hour.", show(g17c, 'Nine minutes is nine sixtieths')),
      L("Fifteen divided by nine sixtieths is fifteen times sixty, over nine.", show(g17d, 'Fifteen divided by nine sixtieths')),
      L("Fifteen times sixty is nine hundred, and nine hundred divided by nine is a hundred. So the train goes a hundred "
        "kilometers per hour.", show(g17e, 'nine hundred divided by nine'))),
    S('Method 1 · The math way: hours',
      L("They ask for the difference, so a hundred minus thirty-six. Before a long subtraction, here are two quick ways.",
        show(g17sf, 'They ask for the difference'), show(g17f, 'a hundred minus thirty-six')),
      L("Here's the first way. We add four to both numbers, so the second one is a round forty. A hundred four minus forty is "
        "sixty-four.", show(g17g, 'A hundred four minus forty')),
      L("Here's another way. We walk from thirty-six to a round forty, that's four. Then from forty to a hundred, that's sixty.",
        show(g17h, 'We walk from thirty-six')),
      L("Four plus sixty is sixty-four. So the difference is sixty-four kilometers per hour.", show(g17i, 'Four plus sixty')),
      L("A hundred thirty-six, choice number four, adds the speeds instead.", mk('cross', 'choice 4', 'adds the speeds instead'))),
    S('Method 2 · Understanding: identical ratios',
      L("[pause] Now by understanding, with identical ratios. This way saves most of the work. We start again from the "
        "givens."),
      L("The motorbike goes nine kilometers in fifteen minutes. We want one hour, sixty minutes.",
        show(g17t['line'], 'The motorbike goes nine kilometers'), show(g17t['r1'], 'The motorbike goes nine kilometers'),
        show(g17t['r2'], 'We want one hour')),
      L("From fifteen to sixty is times four. So the distance is times four too. Nine times four is thirty-six "
        "kilometers in one hour.", show(g17t['ans'], 'Nine times four is thirty-six')),
      L("The train goes fifteen kilometers in nine minutes. From nine to sixty isn't a whole step. So first we divide "
        "both by three. That's five kilometers every three minutes.", show(g17u['line'], 'The train goes fifteen kilometers'),
        show(g17u['r1'], 'The train goes fifteen kilometers'), show(g17u['r2'], 'five kilometers every three minutes')),
      L("An hour is twenty times three minutes. So five times twenty, a hundred kilometers in one hour.",
        show(g17u['r3'], 'An hour is twenty times three'), show(g17u['ans'], 'a hundred kilometers in one hour')),
      L("If you don't see that step, use the triangle value from topic twenty-two. Multiply along the diagonal, fifteen "
        "times sixty, and divide by what's left, nine. That's a hundred too.", show(g17v, 'Multiply along the diagonal')),
      L("A hundred minus thirty-six is sixty-four. The same answer.", show(g17w, 'A hundred minus thirty-six is sixty-four')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g118 (the elevator)
# Hebrew (wp 7766-7861, the zip line 120 m in 10 s, double speed to the middle, then half speed): instinct says 10,
# wrong; (1) the calculation (12 m/s; 60/24 = 2.5; 60/6 = 10 -> 12.5); (2) ratios (normally 5 + 5; double speed -> half
# the time; half speed -> double); (3) the insight: the slow half alone = the whole normal trip, plus something -> rule
# out 10, 7.5, 5. Her recommendation (kept as one plain line, no verdict paragraph, R16): ratios; the insight is quick
# when you see it. English: 60 m in 20 s -> 25 s. R36: 30 / 1.5 said as "one and a half times twenty is thirty".
g18a = IH('g18a', 'normal: $\\ 60\\div20=3$ m a second', size=30)
g18b = IH('g18b', 'each half: $\\ 60\\div2=30$ m', size=30)
g18c = IH('g18c', 'first half: $\\ 3\\times2=6$ m a second', size=30, col=1)
g18d = IH('g18d', '$30\\div6=5$ s', size=30, col=1)
g18e = IH('g18e', 'second half: $\\ 3\\div2=1.5$ m a second', size=30, col=1)
g18f = IH('g18f', '$30\\div1.5=20$ s', size=30, col=1)
g18g = IH('g18g', '$5+20=25$ s', size=30)
g18h = IH('g18h', 'normal: $\\ 10$ s and $10$ s', size=30)
g18i = IH('g18i', 'twice as fast: $\\ 10\\div2=5$ s', size=30)
g18j = IH('g18j', 'half as fast: $\\ 10\\times2=20$ s', size=30)
g18k = IH('g18k', '$5+20=25$ s', size=30, col=1)
g18l = IH('g18l', 'the slow half alone: $\\ 20$ s', size=30)
g18m = IH('g18m', 'plus the fast half: $\\ $more than $20$', size=30)
video('solve-wp27-g118', 'solution', qid='wp27-g118', slides=[
    S('Method 1 · The math way: the speeds',
      L("An elevator normally rises sixty meters in twenty seconds, at a constant speed. On one trip, it rises the first "
        "half of the way at twice its normal speed, and the second half at half its normal speed. How many seconds does "
        "this trip take?", pt('stem', 'An elevator normally rises', 'hl', 13.0), voice='calm', pause=0.5),
      L("Your instinct may say twenty, because twice the speed and half the speed seem to cancel. They don't. Let's see "
        "why.", pt('stem: given', 'twice the speed and half the speed')),
      L("We'll solve it in three different ways. Let's start with the math way, with the speeds. The normal speed is "
        "sixty divided by twenty, three meters a second.", show(g18a, 'sixty divided by twenty')),
      L("Each half of the way is sixty divided by two, thirty meters.", show(g18b, 'sixty divided by two')),
      L("The first half is at twice the normal speed, three times two, six meters a second.", show(g18c, 'three times two, six')),
      L("Thirty meters at six meters a second takes thirty divided by six, five seconds.", show(g18d, 'thirty divided by six')),
      L("The second half is at half the normal speed. Three divided by two is one and a half meters a second.", show(g18e, 'Three divided by two')),
      L("Thirty divided by one and a half is twenty, because one and a half times twenty is thirty. That's twenty seconds for the second half.",
        show(g18f, 'Thirty divided by one and a half')),
      L("Five plus twenty is twenty-five seconds.", show(g18g, 'Five plus twenty'))),
    S('Method 2 · Understanding: ratios',
      L("[pause] Now by understanding, with ratios and no speeds at all. We start again from the givens. The distance of "
        "each half is fixed, so the speed and the time go opposite ways."),
      L("On a normal trip, each half takes half of twenty seconds, ten seconds.", show(g18h, 'each half takes half of twenty')),
      L("The first half is twice as fast, so it takes half the time. Ten divided by two is five seconds.",
        show(g18i, 'Ten divided by two')),
      L("The second half is half as fast, so it takes twice the time. Ten times two is twenty seconds.",
        show(g18j, 'Ten times two')),
      L("Five plus twenty is twenty-five seconds again.", show(g18k, 'Five plus twenty is twenty-five seconds again'))),
    S('Method 3 · Insight',
      L("[pause] And now the insight. It's quick, but only if you happen to see it. If you don't, the ratios always work."),
      L("At half the speed, the second half alone takes twenty seconds. That's as long as the whole normal trip.",
        show(g18l, 'the second half alone takes twenty')),
      L("And the fast half still takes some time on top of that. So the answer is more than twenty seconds.",
        show(g18m, 'more than twenty seconds')),
      L("So twenty, ten and fifteen are all out. Only twenty-five is left.", mk('cross', 'choice 1', 'So twenty'),
        mk('cross', 'choice 3', 'ten and fifteen'), mk('cross', 'choice 4', 'are all out')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g120 (the new ferry)
# Hebrew (wp 7965-8059, Pretoria - Cape Town 1,600 km in 6 h, 50% faster): (1) the calculation (+50% = x1.5); (2) ratios
# ("twice as fast, half the time; three times, a third; so 1.5 times, divide by 1.5"); (3) the insight / estimate: if it
# were twice as fast -> 3 h, so 3 and anything under 3 are out; 9 is slower than the old train; "I ruled out three
# answers with one round number". English: 360 km in 12 h, 60% faster -> 7.5 h. Hebrew-vs-English #3 RESTORED by the
# choices (t27.py: 8 -> 4.8, the 60%-less-time trap): twice as fast -> 6 h rules out 6, 4.8 and 19.2 at once. A percent
# multiplier (topic 23) and "the time goes the opposite way" (topic 26, wp-110) are REMINDERS. R36: 360 / 48 checked as
# 48 x 7 + 24.
g20a = IH('g20a', 'old speed: $\\ 360\\div12=30$ kph', size=30)
g20b = IH('g20b', '$60\\%$ faster: $\\ \\times1.6$', size=30)
g20c = IH('g20c', '$30\\times1.6=48$ kph', size=30)
g20d = IH('g20d', 'time $=360\\div48$ hours', size=30, col=1)
g20e = IH('g20e', '$360\\div12=30$, $\\ 48\\div12=4$', size=30, col=1)
g20e2 = IH('g20e2', '$30\\div4=7.5$ hours', size=30, col=1)
g20f = IH('g20f', '$12-60\\%$ of $12=4.8$: $\\ $the trap', size=30, col=1)
g20g = IH('g20g', 'twice as fast: $\\ $half the time', size=30)
g20h = IH('g20h', '$1.6$ times as fast: $\\ $time $\\div1.6$', size=30)
g20i = IH('g20i', '$\\frac{12}{1.6}=\\frac{120}{16}=7.5$', size=30)
g20j = IH('g20j', 'twice as fast: $\\ 12\\div2=6$ hours', size=30)
g20k = IH('g20k', 'less than twice: $\\ $more than $6$', size=30)
g20l = IH('g20l', 'faster: $\\ $less than $12$', size=30)
video('solve-wp27-g120', 'solution', qid='wp27-g120', slides=[
    S('Method 1 · The math way: the speeds',
      L("A ferry covers a route of three hundred sixty kilometers in twelve hours. A new ferry travels sixty percent "
        "faster. How many hours does the new ferry take on the same route?", pt('stem', 'A ferry covers a route', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("So the route is the same, and only the speed changes. They ask for the new time.", pt('stem: ask', 'They ask for the new time')),
      L("We'll solve it in three different ways. Let's start with the math way. The old speed is the distance divided by "
        "the time. Three hundred sixty divided by twelve is thirty kilometers per hour.", show(g20a, 'Three hundred sixty divided by twelve')),
      L("Sixty percent faster means a hundred sixty percent of the old speed. So we multiply by one point six.",
        show(g20b, 'So we multiply by one point six')),
      L("Thirty times one point six is forty-eight kilometers per hour.", show(g20c, 'Thirty times one point six')),
      L("The new time is the route's distance divided by the new speed. So we need three hundred sixty divided by forty-eight.",
        show(g20d, 'three hundred sixty divided by forty-eight')),
      L("Divide both numbers by twelve to make the division easier. Three hundred sixty divided by twelve is thirty. Forty-eight divided by twelve is four. So thirty divided by four is seven and a half hours.",
        show(g20e, 'Three hundred sixty divided by twelve'), show(g20e2, 'thirty divided by four')),
      L("Careful, sixty percent faster doesn't mean sixty percent less time. Twelve minus sixty percent of twelve is four "
        "point eight, choice number two. That's the trap.", show(g20f, 'Twelve minus sixty percent'),
        mk('cross', 'choice 2', "That's the trap"))),
    S('Method 2 · Understanding: ratios',
      L("[pause] Now by understanding, with ratios. We start again from the givens. The route is the same, so the speed "
        "and the time go opposite ways."),
      L("Twice as fast takes half the time. Three times as fast takes a third of the time.", show(g20g, 'Twice as fast takes half')),
      L("So one point six times as fast takes the time divided by one point six.", show(g20h, 'one point six times as fast')),
      L("Twelve divided by one point six. We multiply both by ten, so it's a hundred twenty divided by sixteen. That's "
        "seven and a half again.", show(g20i, 'a hundred twenty divided by sixteen'))),
    S('Method 3 · Estimation',
      L("[pause] Now let's estimate, with one easy number. We start again from the givens. If the new ferry were twice "
        "as fast, it would take half the time, twelve divided by two, six hours.", show(g20j, 'twelve divided by two')),
      L("But it's less than twice as fast. So it takes more than six hours. Six and four point eight are out.",
        show(g20k, 'So it takes more than six hours'), mk('cross', 'choice 1', 'Six and four point eight'),
        mk('cross', 'choice 2', 'are out')),
      L("And it's faster than the old ferry, so it takes less than twelve hours. Nineteen point two is out too.",
        show(g20l, 'so it takes less than twelve'), mk('cross', 'choice 3', 'Nineteen point two is out')),
      L("One easy number ruled out three choices. Only seven and a half is left."),
      L("Choice number four is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g119 (B is the midpoint)
# Hebrew (wp 7863-7963, Gabriel 30 kph A -> C; Alexander 30 min A -> B, then 20 kph): (1) algebra with a d-t-v table:
# call each HALF x ("not x/2"); stay in hours ("half, not 30"); his first speed isn't needed; 2x/30 = 1/2 + x/20 -> x =
# 30 -> 60; (2) plugging in the answers: the round ones first, 60 before 90 because the halves are 30, not 45 -> 2 h =
# 1/2 + 1 1/2; "not by chance: NITE checks whether you know what to plug in first". English: 48 kph; 20 minutes, then
# 36 kph -> 48. Trap at its step: 24 = x, only half the road.
g19t = TBL('g19t', ['Speed', 'Distance', 'Time'], ['rider 1', 'rider 2, A to B', 'rider 2, B to C'], [
    ('r1', [('c', 0, 0, '48'), ('c', 0, 1, '2x'), ('c', 0, 2, '2x/48')]),
    ('r2', [('c', 1, 1, 'x'), ('c', 1, 2, '1/3')]),
    ('r3', [('c', 2, 0, '36'), ('c', 2, 1, 'x'), ('c', 2, 2, 'x/36')])], colw=130, labw=210, rowh=56, headh=50, w=560, size=30)
g19a = IH('g19a', '$\\frac{2x}{48}=\\frac{1}{3}+\\frac{x}{36}$', size=32, col=1)
g19a2 = IH('g19a2', '$\\frac{2x}{48}=\\frac{1}{3}+\\frac{x}{36}$', size=32)
g19b = IH('g19b', '$\\frac{x}{24}=\\frac{1}{3}+\\frac{x}{36}$', size=32)
g19c = IH('g19c', '$\\times72$: $\\ 3x=24+2x$', size=30)
g19d = IH('g19d', '$x=24$', size=30, col=1)
g19e = IH('g19e', 'AC $=2x=48$ km', size=30, col=1)
g19f = IH('g19f', '$24$: $\\ $only half the road', size=30, col=1)
g19g = IH('g19g', 'try $48$: $\\ $each half $24$ km', size=30)
g19h = IH('g19h', 'rider 1: $\\ 48\\div48=1$ hour', size=30)
g19i = IH('g19i', 'rider 2: $\\ \\frac{1}{3}$ hour, $\\ $then $24\\div36=\\frac{2}{3}$ hour', size=30)
g19j = IH('g19j', '$\\frac{1}{3}+\\frac{2}{3}=1$ hour: $\\ $equal', size=30, col=1)
video('solve-wp27-g119', 'solution', qid='wp27-g119', slides=[
    S('Method 1 · The math way: the table',
      L("B is the midpoint of a straight road from A to C. One motorcyclist rides from A to C at forty-eight kilometers "
        "per hour. Another takes twenty minutes from A to B, then rides from B to C at thirty-six kilometers per hour. "
        "Their total travel times are equal. How many kilometers long is A C?", pt('stem', 'B is the midpoint', 'hl', 15.0),
        voice='calm', pause=0.5),
      L("So we have two riders, and the link is equal times. They ask for the whole road, A to C.", pt('stem: ask', 'They ask for the whole road')),
      L("We'll solve it in two different ways. Let's start with the math way, with the table from the lesson. B is the "
        "midpoint, so let's call each half x. Then we don't need x over two.", show(g19t['line'], 'with the table from the lesson')),
      L("The first rider covers the whole road, two x, at forty-eight. His time is two x over forty-eight.",
        show(g19t['r1'], 'The first rider covers the whole road')),
      L("The second rider covers the first half, x, in twenty minutes. The speed is per hour, so we stay in hours. Twenty "
        "minutes is a third of an hour.", show(g19t['r2'], 'The second rider covers the first half')),
      L("We don't even need his speed on that half. We only need the time, and it's given."),
      L("Then he covers the other half, x, at thirty-six. That time is x over thirty-six.", show(g19t['r3'], 'Then he covers the other half')),
      L("The times are equal. So two x over forty-eight is equal to a third, plus x over thirty-six.", show(g19a, 'The times are equal')),
      L("Now we solve this equation. Both sides are times in hours, so x will come out in kilometers.")),
    S('Method 1 · The math way: the table',
      L("Here is our equation again.", show(g19a2, 'Here is our equation again')),
      L("Two x over forty-eight is x over twenty-four.", show(g19b, 'Two x over forty-eight is x over twenty-four')),
      L("We multiply every term by seventy-two to remove the denominators. Twenty-four, three and thirty-six all divide seventy-two. "
        "That gives three x is equal to twenty-four plus two x.", show(g19c, 'That gives three x')),
      L("We take two x off both sides, and x is twenty-four.", show(g19d, 'and x is twenty-four')),
      L("Careful, twenty-four is choice number one, but it's only x, half of the road.", show(g19f, "it's only x, half of the road"),
        mk('cross', 'choice 1', 'half of the road')),
      L("The whole road is two x, two times twenty-four, forty-eight kilometers.", show(g19e, 'two times twenty-four'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. We start again from the givens, and with the friendliest choice. Let's try "
        "forty-eight. Then each half is twenty-four kilometers.", show(g19g, "Let's try")),
      L("Forty-eight is friendly, because the first rider rides forty-eight kilometers at forty-eight. That's exactly one "
        "hour.", show(g19h, "That's exactly one")),
      L("The second rider takes twenty minutes, a third of an hour, to B. Then twenty-four kilometers at thirty-six. "
        "Twenty-four over thirty-six is two thirds of an hour.", show(g19i, 'Twenty-four over thirty-six')),
      L("A third plus two thirds is one hour. Both times are one hour, so they are equal, just like the given says.",
        show(g19j, 'A third plus two thirds')),
      L("It worked on the first try, and that's not luck. The exam checks whether you know which answer to plug in first. "
        "Start with the round, friendly one."),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ r26-t27-special (lesson: trains and circular tracks)
# No Hebrew lesson (her karts question g121 carries the circular track; trains are not in her course). Real-exam gaps
# (reviews/exam-coverage-wordproblems.md §6 M4 and gap 4; ~/Downloads/Exam-coverage-audit.md): the special cases are
# CORE (R37) and are taught here, before their first question (t27.py moves this lesson before g121), each with two
# worked examples. Part 1, a train with a length: a post (its own length: 200 m at 25 m/s -> 8 s; 2024_winter_q1_14:
# a man on a platform, 120 kph for half a minute -> 1 km) and a bridge or a platform (the bridge plus the train:
# 300 + 200 = 500 m -> 20 s); the trap: the bridge alone. Part 2, a circular track: the same direction -> they meet once
# every lap the fast one gains (subtract: 600 m, 10 and 7 kph -> 12 min; 2024_autumn_q2_10: speeds v and 2v -> the
# first meeting is back at the start), opposite directions -> once every lap they cover together (add: 600 m, 10 and 8
# -> 2 min; 1 km, 7 and 5 -> 5 min). Relative speed is a REMINDER (wp-113); "any two meetings in a row" and "laps it"
# are her karts lines (g121, Hebrew-vs-English #1), said again there.
x1s = ROAD('x1s', [
    ('post', [('post', .7, 'post')]),
    ('front', [('block', .4, .7, 'start: 200 m')]),
    ('back', [('block', .7, 1, 'finish: 200 m'), ('gap', .7, 1, 'the front moves 200 m')])], w=860)
x1a = IH('x1a', 'past a post: $\\ $the train\'s own length', size=32)
x1b = IH('x1b', '$200\\div25=8$ seconds', size=32)
x1c = IH('x1c', '$120$ kph $=2$ km a minute', size=32, col=1)
x1d = IH('x1d', 'half a minute: $\\ 1$ km', size=32, col=1)
x1e = IH('x1e', 'the train is $1$ km long', size=32, col=1)
x2s = ROAD('x2s', [
    ('bridge', [('seg', .28, .70, 'orange'), ('below', .49, 'bridge 300 m', 'orange')]),
    ('front', [('block', 0, .28, 'start')]),
    ('back', [('block', .70, .98, 'finish'), ('gap', .28, .98, 'the front moves: bridge + train')])], w=860)
x2a = IH('x2a', 'a bridge: $\\ $the bridge $+$ the train', size=32)
x2b = IH('x2b', '$300+200=500$ m', size=32)
x2c = IH('x2c', '$500\\div25=20$ seconds', size=32)
x2d = IH('x2d', '$300\\div25=12$: $\\ $the trap', size=32)
_x27 = [
    S('Special Motion Cases',
      L("Welcome back. Now three special cases from the exam. Trains that have a length, boats on a river, and circular "
        "tracks."),
      L("The formula stays the same. Distance is equal to speed times time. Only the distance, or the speed, is "
        "different."),
      L("In this lesson we learn the trains and the circular tracks. The river comes in its own question.")),
    S('A train passes a post',
      L("Until now, every traveler was a dot. But a train is not a dot. It has a length."),
      L("Now a new example. A train two hundred meters long passes a post, at twenty-five meters a second. How long does "
        "that take?", show(x1s['line'], 'A train two hundred meters long'), show(x1s['post'], 'passes a post'),
        show(x1s['front'], 'A train two hundred meters long')),
      L("The train starts passing when its front reaches the post. It finishes when its back passes the post. These are two positions of the same train.",
        show(x1s['back'], 'It finishes when its back passes')),
      L("So the front moves exactly one train length, two hundred meters. Past a post, the train covers its own length.",
        show(x1a, 'Past a post, the train covers its own length')),
      L("The time is the distance divided by the speed. Two hundred divided by twenty-five is eight seconds.",
        show(x1b, 'Two hundred divided by twenty-five')),
      L("Now a second example, from a real exam. A train passes a man on a platform at a hundred twenty kilometers per "
        "hour. It takes half a minute. How long is the train?"),
      L("A hundred twenty kilometers in sixty minutes is two kilometers every minute.", show(x1c, 'two kilometers every minute')),
      L("In half a minute, the train moves one kilometer.", show(x1d, 'In half a minute')),
      L("Passing a man is like passing a post. So the distance it moves is its own length. The train is one kilometer "
        "long.", show(x1e, 'The train is one kilometer long'))),
    S('A train crosses a bridge',
      L("Now a bridge. The same train, two hundred meters long, at twenty-five meters a second, crosses a bridge three "
        "hundred meters long completely.", show(x2s['line'], 'Now a bridge'), show(x2s['bridge'], 'crosses a bridge')),
      L("It starts when the front gets on the bridge.", show(x2s['front'], 'It starts when the front gets on')),
      L("And it ends when the back gets off the bridge.", show(x2s['back'], 'it ends when the back gets off')),
      L("So the front moves across the whole bridge, and then one more train length. A bridge means the bridge plus the "
        "train.", show(x2a, 'A bridge means the bridge plus the train')),
      L("Three hundred plus two hundred is five hundred meters.", show(x2b, 'Three hundred plus two hundred')),
      L("Five hundred divided by twenty-five is twenty seconds.", show(x2c, 'Five hundred divided by twenty-five')),
      L("A lot of students divide only the bridge, three hundred divided by twenty-five, twelve seconds. That forgets "
        "the train's own length.", show(x2d, 'three hundred divided by twenty-five')),
      L("A platform or a tunnel works the same way as a bridge. Its length, plus the train.")),
]
x3s = TRACK('x3s', [
    ('start', [('start', 'start')]),
    ('run', [('runner', 0, 'fast', 'ink'), ('runner', 0, '', 'orange')]),
    ('dir', [('dir', 8, 120, 'same direction'), ('dir', 8, 70, '', 'orange', 232)]),
    ('lap', [('center', 'the fast one gains'), ('center', 'one full lap', 1)])], w=540, col=1)
x3a = IH('x3a', 'the same direction: $\\ $subtract', size=32)
x3b = IH('x3b', '$10-7=3$ kph', size=32)
x3c = IH('x3c', '$600$ m $=0.6$ km', size=32)
x3d = IH('x3d', '$3$ km in $60$ min $\\ \\to\\ 0.6$ km in $12$ min', size=32)
x3e = IH('x3e', 'B is twice as fast: $\\ $B gains one lap', size=32)
x3f = IH('x3f', 'when A has done $1$ lap, $\\ $B has done $2$', size=32)
x3g = IH('x3g', 'they meet at the start', size=32)
x4s = TRACK('x4s', [
    ('start', [('start', 'start')]),
    ('dir', [('dir', 8, 110, 'runner 1'), ('dir', -8, -110, 'runner 2', 'orange')]),
    ('meet', [('meet', 200, 'they meet')]),
    ('lap', [('center', 'together:'), ('center', 'one full lap', 1)])], w=640, col=1)
x4a = IH('x4a', 'opposite directions: $\\ $add', size=32)
x4b = IH('x4b', '$10+8=18$ kph', size=32)
x4c = IH('x4c', '$18$ km in $60$ min $\\ \\to\\ 0.6$ km in $2$ min', size=32)
x4d = IH('x4d', '$7+5=12$ kph', size=32)
x4e = IH('x4e', '$12$ km in $60$ min $\\ \\to\\ 1$ km in $5$ min', size=32)
x5a = I('x5a', 'A post: $\\ $the train. $\\ $A bridge: $\\ $the bridge $+$ the train.', size=34)
x5b = I('x5b', 'A track, the same direction: $\\ $subtract, $\\ $one lap gained', size=34)
x5c = I('x5c', 'A track, opposite directions: $\\ $add, $\\ $one lap together', size=34)
_x27 += [
    S('A circular track, the same direction',
      L("Now circular tracks. Two runners start together from the same point, and run in the same direction.",
        show(x3s['line'], 'Now circular tracks'), show(x3s['start'], 'from the same point'), show(x3s['run'], 'Two runners start together')),
      L("The fast one pulls away. Then it chases the slow one from behind, all the way around.", show(x3s['dir'], 'The fast one pulls away')),
      L("They meet again when the fast one has gained one full lap.", show(x3s['lap'], 'gained one full lap')),
      L("That's a chase, so we subtract the speeds. Imagine the slow one stands still. Then the fast one moves at the "
        "difference, and it needs one lap.", show(x3a, "That's a chase, so we subtract")),
      L("Now a new example. The track is six hundred meters, and the speeds are ten and seven kilometers per hour. Ten "
        "minus seven is three.", show(x3b, 'Ten minus seven is three')),
      L("Six hundred meters is zero point six kilometers.", show(x3c, 'Six hundred meters is zero point six')),
      L("Three kilometers take sixty minutes. Zero point six is a fifth of three, so it takes a fifth of sixty minutes, "
        "twelve minutes.", show(x3d, 'Three kilometers take sixty minutes')),
      L("So they meet every twelve minutes."),
      L("Now a second example, from a real exam. Two cars start together from the same point on a circular track. Car B is twice as fast as car A, in the same direction. Where do they "
        "meet first?", show(x3e, 'Car B is twice as fast')),
      L("They meet when B has gained one lap. B covers twice what A covers. So when A has done one lap, B has done two.",
        show(x3f, 'So when A has done one lap')),
      L("A is back at the start after one lap. So they meet at the start.", show(x3g, 'So they meet at the start'))),
    S('A circular track, opposite directions',
      L("Now the runners start together, but run in opposite directions. They run toward each other around the track.",
        show(x4s['line'], 'run in opposite directions'), show(x4s['start'], 'run in opposite directions'), show(x4s['dir'], 'They run toward each other')),
      L("They meet when together they have covered one full lap.", show(x4s['meet'], 'They meet when together'),
        show(x4s['lap'], 'one full lap')),
      L("They move toward each other, so we add the speeds.", show(x4a, 'so we add the speeds')),
      L("Now a new example. The track is six hundred meters, and the speeds are ten and eight kilometers per hour. Ten "
        "plus eight is eighteen.", show(x4b, 'Ten plus eight is eighteen')),
      L("Eighteen kilometers take sixty minutes. Zero point six is eighteen divided by thirty. So the time is sixty "
        "divided by thirty, two minutes.", show(x4c, 'Eighteen kilometers take sixty minutes')),
      L("Another example. A one-kilometer track, with speeds seven and five. Seven plus five is twelve.",
        show(x4d, 'Seven plus five is twelve')),
      L("Twelve kilometers take sixty minutes. So one kilometer takes sixty divided by twelve, five minutes.",
        show(x4e, 'one kilometer takes sixty divided by twelve'))),
    S('Recap',
      L("So let's sum it up. A train passing a post covers its own length. A bridge, a platform or a tunnel means its "
        "length plus the train.", show(x5a, 'A train passing a post')),
      L("On a circular track in the same direction, we subtract the speeds. They meet once every lap the fast one gains.",
        show(x5b, 'in the same direction')),
      L("In opposite directions, we add the speeds. They meet once every lap they cover together.",
        show(x5c, 'In opposite directions')),
      L("Take a moment to memorize this. Now try the next question, and I'll see you in the next video.")),
]
video('r26-t27-special', 'lesson', slides=_x27)
SPLITS.append(('r26-t27-special', 'Special Motion Cases', [
    (1, None),
    (3, "Let's continue with the special cases, and look at circular tracks.")]))

# ------------------------------------------------------------------------------------------------ g121 (the circular track)
# Hebrew (wp 8061-8283, karts on a 500 m track, 60 and 50 kph, the time between consecutive meetings): first the meaning
# with the animation (the fast one gains a full lap); "it doesn't have to be counted from the start: any two meetings in
# a row"; "or 'when it laps it', depends on the wording, the same meaning" (Hebrew-vs-English #1: both RESTORED here);
# (1) the equation 60t = 50t + 1/2 ("give it to the poor one": the lap goes to the slower side), "not how we solve it on
# the exam"; (2) relative speed: "you stand still", the fast one at the difference, 10 km in 60 min -> 1/2 km x6 -> 3 min.
# English: 400 m, 12 and 9 kph -> 8 min; relative speed first (her "the way we solve it"), the equation as a check (the
# teacher kept this order, t27_CHANGES Q13). First question after the special lesson: "like in the lesson".
g21s = TRACK('g21s', [
    ('start', [('start', 'start')]),
    ('dir', [('dir', 8, 120, '12 kph'), ('dir', 8, 50, '9 kph', 'orange', 236)]),
    ('lap', [('center', '1 lap = 400 m')])], w=540, col=1)
g21a = IH('g21a', 'any two meetings in a row: $\\ $one lap gained', size=30)
g21b = IH('g21b', '$12-9=3$ kph', size=30)
g21c = IH('g21c', '$400$ m $=0.4$ km', size=30)
g21d = IH('g21d', '$3$ km: $\\ 60$ min $\\ \\to\\ 1$ km: $\\ 20$ min', size=30, col=1)
g21e = IH('g21e', '$0.4\\times20=8$ minutes', size=30, col=1)
g21f = IH('g21f', '$12t=9t+0.4$', size=32)
g21g = IH('g21g', '$3t=0.4$', size=30)
g21h = IH('g21h', '$t=\\frac{0.4}{3}=\\frac{4}{30}=\\frac{2}{15}$ hour', size=30)
g21i = IH('g21i', '$60\\times\\frac{2}{15}=4\\times2=8$ minutes', size=30, col=1)
video('solve-wp27-g121', 'solution', qid='wp27-g121', slides=[
    S('Method 1 · The math way: relative speed',
      L("Two runners start together from the same point of a circular track, running in the same direction. The track is "
        "four hundred meters long. Their speeds are twelve and nine kilometers per hour. How many minutes pass between "
        "consecutive meetings?", pt('stem', 'Two runners start together', 'hl', 12.0), voice='calm', pause=0.5),
      L("First, what do consecutive meetings mean? They are two meetings that come one right after the other.",
        pt('stem: ask', 'consecutive meetings mean'), show(g21s['line'], 'consecutive meetings mean'), show(g21s['start'], 'consecutive meetings mean')),
      L("We'll solve it in two different ways. Let's start with the math way, with relative speed, like in the lesson. "
        "They run the same way, so the fast one meets the slow one again when it has gained one full lap.",
        show(g21s['dir'], 'They run the same way'), show(g21s['lap'], 'one full lap')),
      L("We can count from any meeting, wherever it happens on the track. Before the next meeting, the fast runner gains one more full lap on the slow runner.",
        show(g21a, 'the fast runner gains one more full lap')),
      L("Some questions ask instead, when does the fast one lap the slow one? It's the same question, in other words."),
      L("So we need the time it takes the fast one to gain one lap.")),
    S('Method 1 · The math way: relative speed',
      L("It's a chase, so we subtract the speeds. Twelve minus nine is three. Imagine the slow one stands still, and the "
        "fast one runs at three kilometers per hour.", show(g21b, 'Twelve minus nine is three')),
      L("The fast one needs one lap, four hundred meters. That's zero point four kilometers.",
        show(g21c, "That's zero point four kilometers")),
      L("Three kilometers take sixty minutes. So one kilometer takes sixty divided by three, twenty minutes.",
        show(g21d, 'Three kilometers take sixty minutes')),
      L("Zero point four of a kilometer takes zero point four times twenty, eight minutes.", show(g21e, 'zero point four times twenty'))),
    S('Method 2 · The math way: an equation',
      L("[pause] Now the math way, with an equation, as a check. We start again from the givens. Both runners run for "
        "the same time. Let's call it t, in hours."),
      L("The fast one covers twelve t, and the slow one covers nine t. The fast one covers one more lap, zero point four "
        "kilometers. So twelve t is equal to nine t plus zero point four.", show(g21f, 'So twelve t is equal to nine t')),
      L("We take nine t off both sides. Three t is zero point four.", show(g21g, 'Three t is zero point four')),
      L("So t is zero point four divided by three. That's four thirtieths, two fifteenths of an hour.",
        show(g21h, 'zero point four divided by three')),
      L("Two fifteenths of sixty minutes. Sixty divided by fifteen is four, and four times two is eight minutes. The same "
        "answer.", show(g21i, 'Sixty divided by fifteen is four')),
      L("Choice number one is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t27-01 (the train and the bridge)
# No Hebrew (real exam 2024_winter_q1_14). First use after the special lesson (part 1), "like in the lesson": the post
# gives the speed (its own length), the bridge plus the train. Method 2 (English): ratios (the same speed, the distance
# x8/3, so the time x8/3). Trap at its step: 25 (the bridge alone).
q1s = ROAD('q1s', [
    ('bridge', [('seg', .27, .72, 'orange'), ('below', .495, 'bridge 500 m', 'orange')]),
    ('front', [('block', 0, .27, 'start: 300 m')]),
    ('back', [('block', .72, .99, 'finish: 300 m'), ('gap', .27, .99, 'the front moves: bridge + train')])], w=860)
q1a = IH('q1a', 'post: $\\ 300$ m in $15$ s', size=30)
q1b = IH('q1b', '$300\\div15=20$ m a second', size=30)
q1c = IH('q1c', '$500+300=800$ m', size=30)
q1d = IH('q1d', '$800\\div20=40$ seconds', size=30)
q1e = IH('q1e', '$500\\div20=25$: $\\ $the trap', size=30)
q1f = IH('q1f', '$300$ m: $\\ 15$ s, $\\ $so $100$ m: $\\ 5$ s', size=30)
q1g = IH('q1g', '$800$ m: $\\ 8\\times5=40$ s', size=30)
video('solve-q-r26-t27-01', 'solution', qid='q-r26-t27-01', slides=[
    S('Method 1 · The math way: the train\'s length',
      L("A train three hundred meters long travels at a constant speed. It passes a signal post in fifteen seconds. How "
        "many seconds does it take to cross a bridge five hundred meters long completely?", pt('stem', 'A train three hundred meters long', 'hl', 10.0),
        voice='calm', pause=0.5),
      L("So the train has a length, and they ask for the time on the bridge. The speed isn't given, so the post gives it "
        "to us.", pt('stem: ask', 'they ask for the time on the bridge')),
      L("We'll solve it in two different ways. Let's start with the math way, like in the lesson. Passing a post, the "
        "train moves its own length, three hundred meters, in fifteen seconds.", show(q1a, 'three hundred meters, in fifteen seconds')),
      L("The speed is three hundred divided by fifteen, twenty meters a second.", show(q1b, 'three hundred divided by fifteen')),
      L("Next, we use the speed of twenty meters a second on the bridge.")),
    S('Method 1 · The math way: the train\'s length',
      L("Now the bridge. It starts when the front gets on the bridge, and ends when the back gets off.",
        show(q1s['line'], 'Now the bridge'), show(q1s['bridge'], 'Now the bridge'), show(q1s['front'], 'when the front gets on'),
        show(q1s['back'], 'when the back gets off')),
      L("So the front moves the bridge plus one train length. Five hundred plus three hundred is eight hundred meters.",
        show(q1c, 'Five hundred plus three hundred')),
      L("Eight hundred divided by twenty is forty seconds.", show(q1d, 'Eight hundred divided by twenty')),
      L("Twenty-five, choice number one, divides only the bridge. It forgets the train's own length.",
        show(q1e, 'divides only the bridge'), mk('cross', 'choice 1', "forgets the train's own length"))),
    S('Method 2 · Understanding: ratios',
      L("[pause] Now by understanding, with ratios. We start again from the givens. The speed is the same the whole time, "
        "so the time and the distance go the same way."),
      L("Three hundred meters take fifteen seconds. So a hundred meters take a third of that, five seconds.",
        show(q1f, 'So a hundred meters take a third')),
      L("Crossing the bridge completely, the front moves the bridge plus the train, eight hundred meters. That's eight "
        "hundreds, so eight times five, forty seconds.", show(q1g, 'eight times five')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t27-02 (the current)
# No Hebrew (an English question; plane and wind in the practice). A one-off idea, taught here (R37, about 2 minutes):
# downstream = boat + current, upstream = boat - current (a 10 kph boat in a 2 kph current: 12 and 8), so the current is
# half the difference and the boat the average; a tailwind / headwind works the same. Two methods: the two equations
# (subtract them), plugging in the answers (4 -> the boat 20 -> 24 and 16). Traps at their steps: 8 (not halved),
# 20 (the boat).
q2a = IH('q2a', 'with the current: $\\ $boat $+$ current', size=30)
q2b = IH('q2b', 'against it: $\\ $boat $-$ current', size=30)
q2c = IH('q2c', 'boat $10$, $\\ $current $2$: $\\ 10+2=12$, $\\ 10-2=8$', size=30)
q2d = IH('q2d', 'down: $\\ 48\\div2=24$ kph', size=30)
q2e = IH('q2e', 'up: $\\ 48\\div3=16$ kph', size=30)
q2f = IH('q2f', '$b+c=24$, $\\ b-c=16$', size=30)
q2g = IH('q2g', 'subtract: $\\ 2c=24-16=8$', size=30, col=1)
q2h = IH('q2h', '$c=4$ kph', size=30, col=1)
q2i = IH('q2i', '$8$: $\\ $not halved, $\\ 20$: $\\ $the boat', size=30, col=1)
q2j = IH('q2j', 'try $c=4$: $\\ $down $24$, $\\ $so the boat $24-4=20$', size=30)
q2k = IH('q2k', 'up: $\\ 20-4=16$', size=30)
q2l = IH('q2l', '$48\\div16=3$ hours: $\\ $it fits', size=30)
video('solve-q-r26-t27-02', 'solution', qid='q-r26-t27-02', slides=[
    S('How a current works',
      L("A boat travels forty-eight kilometers downstream in two hours. The return trip upstream, along the same route, "
        "takes three hours. The boat's speed in still water does not change. What is the speed of the current, in "
        "kilometers per hour?", pt('stem', 'A boat travels forty-eight kilometers', 'hl', 12.0), voice='calm', pause=0.5),
      L("So they ask for the speed of the river's current. I want to use this question to show you how a current works.",
        pt('stem: ask', "they ask for the speed of the river's current")),
      L("Downstream means with the current. The water carries the boat, so we add the current to the boat's speed.",
        show(q2a, 'we add the current')),
      L("Upstream means against the current. The water pushes back, so we subtract it.", show(q2b, 'so we subtract it')),
      L("Let's see it in numbers. A boat goes ten kilometers per hour in still water, and the current is two. Downstream "
        "it goes ten plus two, twelve. Upstream, ten minus two, eight.", show(q2c, 'A boat goes ten kilometers per hour')),
      L("A plane works the same way. A wind from behind adds to its speed, and a wind against it subtracts.")),
    S('Method 1 · The math way: two equations',
      L("We'll solve it in two different ways. Let's start with the math way. First the two real speeds. Downstream, "
        "forty-eight kilometers in two hours is twenty-four kilometers per hour.", show(q2d, 'Downstream, forty-eight kilometers')),
      L("Upstream, forty-eight kilometers in three hours is sixteen kilometers per hour.", show(q2e, 'Upstream, forty-eight kilometers'))),
    S('Method 1 · The math way: two equations',
      L("Let's call the boat's speed in still water b. Call the current's speed c. Then b plus c is twenty-four, and b minus c is "
        "sixteen.", show(q2f, 'Then b plus c is twenty-four')),
      L("We subtract the second equation from the first. The b's cancel. Twenty-four minus sixteen is eight, so two c is "
        "eight.", show(q2g, 'We subtract the second equation')),
      L("So c is half of eight, four kilometers per hour. The current is half the difference of the two speeds.",
        show(q2h, 'So c is half of eight')),
      L("Careful with eight, choice number one. It forgets to halve. And twenty, choice number three, is the boat, not the "
        "current.", show(q2i, 'It forgets to halve'), mk('cross', 'choice 1', 'It forgets to halve'),
        mk('cross', 'choice 3', 'is the boat, not the current'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. We start again from the givens. Let's try a current of four. Downstream "
        "the speed is twenty-four, so the boat is twenty-four minus four, twenty.", show(q2j, "Let's try a current of four")),
      L("Upstream, the boat goes twenty minus four, sixteen kilometers per hour.", show(q2k, 'twenty minus four, sixteen')),
      L("At sixteen, the forty-eight kilometers take forty-eight divided by sixteen, three hours. That's exactly the "
        "given.", show(q2l, 'forty-eight divided by sixteen')),
      L("Choice number four is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t27-03 (opposite directions on a circle)
# No Hebrew (the opposite-direction case of the special lesson, part 2). First use, "like in the lesson": add the
# speeds, one lap together. Method 2: identical ratios (36 km in 60 min -> 1.2 km in 2 min). Trap at its step: 18 (the
# same-direction answer, the difference of the speeds).
q3s = TRACK('q3s', [
    ('start', [('start', 'start')]),
    ('dir', [('dir', 8, 110, '20 kph'), ('dir', -8, -110, '16 kph', 'orange')]),
    ('lap', [('dir', 0, 200, '', 'ink', 180), ('dir', 0, -160, '', 'orange', 180),
             ('meet', 200, 'meet'), ('center', 'together:'), ('center', '1 lap = 1.2 km', 1)])], w=540, col=1, label_size=34)
q3a = IH('q3a', 'opposite directions: $\\ 20+16=36$ kph', size=30)
q3b = IH('q3b', 'time $=1.2\\div36=\\frac{12}{360}=\\frac{1}{30}$ hour', size=30)
q3c = IH('q3c', '$\\frac{1}{30}$ of $60$ minutes $=2$ minutes', size=30, col=1)
q3d = IH('q3d', '$18$: $\\ 20-16$, $\\ $no', size=30, col=1)
q3t = TBL('q3t', ['Time', 'Distance'], ['', ''], [
    ('r1', [('c', 0, 0, '60 min'), ('c', 0, 1, '36 km')]),
    ('r2', [('c', 1, 1, '1.2 km'), ('down', 1, 0, 1, '÷30')]),
    ('ans', [('cover', 1, 0, '2 min'), ('down', 0, 0, 1, '÷30')])], colw=190, labw=0, rowh=62, side=90, w=540)
video('solve-q-r26-t27-03', 'solution', qid='q-r26-t27-03', slides=[
    S('Method 1 · The math way: relative speed',
      L("Two cyclists start together from the same point of a circular track one point two kilometers long, and ride in "
        "opposite directions. Their speeds are twenty and sixteen kilometers per hour. After how many minutes do they "
        "meet for the first time?", pt('stem', 'Two cyclists start together', 'hl', 12.0), voice='calm', pause=0.5),
      L("So they ride toward each other around the track. They ask when they first meet, in minutes.",
        pt('stem: ask', 'They ask when they first meet'), show(q3s['line'], 'they ride toward each other'),
        show(q3s['start'], 'they ride toward each other'), show(q3s['dir'], 'around the track')),
      L("We'll solve it in two different ways. Let's start with the math way, like in the lesson. In opposite "
        "directions, they meet when together they have covered one full lap, one point two kilometers.",
        show(q3s['lap'], 'together they have covered one full lap')),
      L("They move toward each other, so we add the speeds. Twenty plus sixteen is thirty-six kilometers per hour.",
        show(q3a, 'Twenty plus sixteen')),
      L("So we need the time for one lap at thirty-six kilometers per hour.")),
    S('Method 1 · The math way: relative speed',
      L("The time is one point two divided by thirty-six. We multiply both by ten, so it's twelve over three hundred "
        "sixty. That's one thirtieth of an hour.", show(q3b, 'one point two divided by thirty-six')),
      L("A thirtieth of sixty minutes is two minutes.", show(q3c, 'A thirtieth of sixty minutes')),
      L("Eighteen, choice number one, is the same-direction answer. It subtracts the speeds, but here they ride toward "
        "each other.", show(q3d, 'It subtracts the speeds'), mk('cross', 'choice 1', 'here they ride toward each other'))),
    S('Method 2 · Understanding: identical ratios',
      L("[pause] Now by understanding, with identical ratios. We start again from the givens. Together they cover twenty "
        "plus sixteen, thirty-six kilometers in sixty minutes.", show(q3t['line'], 'Together they cover'), show(q3t['r1'], 'thirty-six kilometers in sixty minutes')),
      L("We need one lap, one point two kilometers. Thirty-six divided by thirty is one point two. So we divide by "
        "thirty.", show(q3t['r2'], 'We need one lap')),
      L("So the time is divided by thirty too. Sixty divided by thirty is two minutes.", show(q3t['ans'], 'Sixty divided by thirty')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ r26-t27-graphs (lesson: percents and letters)
# No Hebrew lesson (her Pretoria question g120 touches "% faster"). R37 (the core of q-r26-t27-05, q-r26-t27-06 and the
# practice p02, p03, p06, p17): a percent change of the speed on a fixed route -> write the speed factor as a fraction
# and flip it for the time (+25%: x5/4 -> x4/5, 20% less time; +50%: x3/2 -> x2/3; -20%: x4/5 -> x5/4, 25% MORE time);
# the trap: the same percent off the time. The flip and the percent multiplier are REMINDERS (topic 26 camera lesson
# part 3, topic 23), so each gets one short worked example. Letters in the choices: plugging in numbers (REMINDER,
# topic 51) - easy allowed numbers, the target, test every choice, two hits -> new numbers - and counting the units.
p0a = I('p0a', 'The same route: $\\ $speed $\\times$ a fraction, $\\ $so time $\\times$ the flipped fraction', size=32)
p0b = IH('p0b', '$25\\%$ faster: $\\ $speed $\\times\\frac{5}{4}$', size=32)
p0c = IH('p0c', 'time $\\times\\frac{4}{5}$: $\\ \\frac{1}{5}$ less, $\\ 20\\%$ less', size=32)
p0d = IH('p0d', '$60$ minutes $\\times\\frac{4}{5}=48$ minutes', size=32)
p0e = IH('p0e', '$50\\%$ faster: $\\ \\times\\frac{3}{2}$, $\\ $time $\\times\\frac{2}{3}$', size=32, col=1)
p0f = IH('p0f', '$20\\%$ slower: $\\ \\times\\frac{4}{5}$, $\\ $time $\\times\\frac{5}{4}$', size=32, col=1)
p0g = IH('p0g', '$\\frac{5}{4}$: $\\ 25\\%$ more time', size=32, col=1)
p1a = I('p1a', 'Letters in the choices: $\\ $plug in easy numbers', size=34)
p1b = IH('p1b', 'find the target, $\\ $then test every choice', size=32)
p1c = IH('p1c', 'two choices hit? $\\ $Try new numbers on those two.', size=32)
p1d = IH('p1d', 'or count the units: $\\ $the answer must be a time', size=32)
video('r26-t27-graphs', 'lesson', slides=[
    S('Percents and Letters',
      L("Welcome back. Now two exam favorites in motion. The speed changes by a percent, and answers written with "
        "letters.")),
    S('A percent change of the speed',
      L("Remember from work and rate. When the job is the same, the rate and the time go opposite ways. In motion, the "
        "route is the job. So on the same route, the speed and the time go opposite ways."),
      L("So we write the change of the speed as a fraction, and we flip it for the time.", show(p0a, 'and we flip it for the time')),
      L("Now a new example. On the same route, the speed is twenty-five percent faster. Twenty-five percent more is "
        "times one and a quarter, five quarters.", show(p0b, 'times one and a quarter')),
      L("We flip five quarters to four fifths. So the time is times four fifths. That's one fifth less, twenty percent "
        "less time.", show(p0c, 'We flip five quarters to four fifths')),
      L("So a trip of sixty minutes takes sixty times four fifths, forty-eight minutes.", show(p0d, 'sixty times four fifths')),
      L("Careful, twenty-five percent faster does not mean twenty-five percent less time. It's only twenty percent "
        "less."),
      L("Another example. Fifty percent faster is times three halves. So the time is times two thirds.",
        show(p0e, 'Fifty percent faster is times three halves')),
      L("And slower works the same way. Twenty percent slower is times four fifths. So the time is times five quarters.",
        show(p0f, 'Twenty percent slower is times four fifths')),
      L("Five quarters means a quarter more, so twenty-five percent more time.", show(p0g, 'Five quarters means a quarter more'))),
    S('Letters in the choices',
      L("Now let's look at letters. When the choices have letters, plugging in numbers is our safety net, like in topic fifty-one.",
        show(p1a, 'plugging in numbers is our safety net')),
      L("We pick easy numbers that the question allows. We find the answer with those numbers. That's our target. Then "
        "we put the same numbers into every choice.", show(p1b, "That's our target")),
      L("If two choices give the target, we try new numbers, but only on those two.", show(p1c, 'If two choices give the target')),
      L("And there's a quick check with no numbers. We look at the units. If they ask for a time, the right choice must "
        "come out as a time.", show(p1d, 'We look at the units')),
      L("We'll see one question of each kind now. I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ q-r26-t27-05 (25% faster, 12 minutes less)
# No Hebrew (an English question; real exams 2023_winter_q1_16, 2020_spring_q1_20 on rates). First use after the lesson:
# the flip ("like in the lesson"). Two methods: the fraction (1/5 of the trip = 12 min -> 60), plugging in the answers
# (60 minutes: a 60 km trip at 60 kph; 25% faster = 75 kph -> 48 minutes -> 12 less). Trap at its step: 48 (the new
# time; also "25% less time").
q5a = IH('q5a', 'speed $\\times\\frac{5}{4}$ $\\ \\to\\ $ time $\\times\\frac{4}{5}$', size=30)
q5b = IH('q5b', 'saved: $\\ \\frac{1}{5}$ of the usual time $=12$ minutes', size=30)
q5c = IH('q5c', 'usual time: $\\ 5\\times12=60$ minutes', size=30)
q5d = IH('q5d', '$48$: $\\ $the new time', size=30, col=1)
q5e = IH('q5e', 'try $60$: $\\ 60$ km at $60$ kph', size=30)
q5f = IH('q5f', '$25\\%$ faster: $\\ 60+15=75$ kph', size=30)
q5g = IH('q5g', '$\\frac{60}{75}=\\frac{4}{5}$ hour $=48$ minutes', size=30, col=1)
q5h = IH('q5h', '$60-48=12$: $\\ $it fits', size=30, col=1)
video('solve-q-r26-t27-05', 'solution', qid='q-r26-t27-05', slides=[
    S('Method 1 · Understanding: flip the fraction',
      L("A cyclist rides from home to work at a constant speed. If she rode twenty-five percent faster, the trip would "
        "take twelve minutes less. How many minutes does the trip take at her usual speed?",
        pt('stem', 'A cyclist rides from home to work', 'hl', 10.0), voice='calm', pause=0.5),
      L("So the route is the same, and the speed changes by a percent. They ask for the usual time, not the new one.",
        pt('stem: ask', 'They ask for the usual time')),
      L("We'll solve it in two different ways. First by understanding, like in the lesson. Twenty-five percent faster is "
        "times five quarters. On the same route we flip it, so the time is times four fifths.", show(q5a, 'so the time is times four fifths')),
      L("The new time is four fifths of the usual time. So we save the remaining one fifth. The question says that saving is twelve minutes.",
        show(q5b, 'that saving is twelve minutes')),
      L("So one fifth of the usual time is twelve minutes. The usual time is five times twelve, sixty minutes.",
        show(q5c, 'five times twelve')),
      L("Careful with forty-eight, choice number two. It's sixty minus twelve, the new time. And it's also what you get "
        "if you wrongly treat twelve as a quarter of the usual time. They ask for the usual time.", show(q5d, "It's sixty minus twelve"),
        mk('cross', 'choice 2', 'They ask for the usual time'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. We start again from the givens. Let's try sixty minutes. To make it easy, "
        "say the trip is sixty kilometers at sixty kilometers per hour. That takes one hour, sixty minutes.",
        show(q5e, "Let's try sixty minutes")),
      L("Now she rides twenty-five percent faster. A quarter of sixty is fifteen, so sixty plus fifteen, seventy-five kilometers per "
        "hour.", show(q5f, 'sixty plus fifteen')),
      L("Sixty kilometers at seventy-five is sixty over seventy-five, four fifths of an hour. That's forty-eight minutes.",
        show(q5g, 'sixty over seventy-five')),
      L("Sixty minus forty-eight is twelve minutes less. That's exactly the given.", show(q5h, 'Sixty minus forty-eight')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t27-06 (letters: d, t, k)
# No Hebrew (real exam 2022_autumn_q2_09). First use after the lesson: letters in the choices. Three methods: plugging
# in numbers (d = 40, t = 2, k = 10 -> 30 minutes; why not a speed of 60: choices 3 and 4 would both hit), the math way
# (speed d/t, time kt/d hours, x60), counting the units (km and hours; a time; minutes = hours x 60).
q6a = IH('q6a', '$d=40$, $\\ t=2$: $\\ $speed $40\\div2=20$ kph', size=30)
q6b = IH('q6b', '$k=10$: $\\ 10\\div20=\\frac{1}{2}$ hour $=30$ minutes', size=30)
q6c = IH('q6c', '(1) $\\ \\frac{10\\cdot2}{60\\cdot40}$: $\\ $tiny, no', size=30, col=1)
q6d = IH('q6d', '(2) $\\ \\frac{60\\cdot40}{10\\cdot2}=120$, no', size=30, col=1)
q6e = IH('q6e', '(3) $\\ \\frac{60\\cdot10\\cdot2}{40}=\\frac{1200}{40}=30$', size=30, col=1)
q6f = IH('q6f', '(4) $\\ \\frac{10\\cdot40}{60\\cdot2}=\\frac{400}{120}$, no', size=30)
q6g = IH('q6g', 'A tie is possible: $\\ $test the survivors with new numbers', size=30)
q6h = IH('q6h', 'speed $=\\frac{d}{t}$', size=30)
q6i = IH('q6i', 'time $=k\\div\\frac{d}{t}=\\frac{kt}{d}$ hours', size=30)
q6j = IH('q6j', 'minutes: $\\ \\frac{kt}{d}\\times60=\\frac{60kt}{d}$', size=30)
q6k = IH('q6k', '$k,\\ d$: $\\ $km. $\\ t$: $\\ $hours', size=30)
q6l = IH('q6l', '(2) $\\ \\frac{1}{\\text{hours}}$, $\\ $(4) $\\ \\frac{\\text{km}^2}{\\text{hours}}$: $\\ $out', size=30)
q6m = IH('q6m', 'minutes $=$ hours $\\times60$: $\\ 60$ on top', size=30)
q6ratio = IH('q6ratio', 'time $=\\frac{k}{d}\\times t=\\frac{kt}{d}$ hours', size=30)
video('solve-q-r26-t27-06', 'solution', qid='q-r26-t27-06', slides=[
    S('Method 1 · Plugging in numbers',
      L("A car travels d kilometers in t hours. At the same speed, how many minutes does it take to travel k kilometers?",
        pt('stem', 'A car travels d kilometers', 'hl', 7.0), voice='calm', pause=0.5),
      L("So there are letters in the question and letters in the choices. And they ask for minutes, while t is in hours.",
        pt('stem: ask', 'they ask for minutes')),
      L("We'll solve it in three different ways. First, let's plug in numbers, like in the lesson. We pick easy numbers "
        "that divide well. Let's say d is forty kilometers and t is two hours. The speed is forty divided by two, twenty "
        "kilometers per hour.", show(q6a, "Let's say d is forty")),
      L("Let's say k is ten kilometers. Ten kilometers at twenty takes half an hour. They ask for minutes, so thirty "
        "minutes. That's our target.", show(q6b, "Let's say k is ten")),
      L("Now every choice, with the same numbers. Choice number one says k t over sixty d. That's twenty over two "
        "thousand four hundred, tiny. Out.", show(q6c, "That's twenty over two"), mk('cross', 'choice 1', 'tiny. Out')),
      L("Choice number two says sixty d over k t. That's two thousand four hundred over twenty, a hundred twenty. Out.",
        show(q6d, "That's two thousand four hundred over twenty"), mk('cross', 'choice 2', 'a hundred twenty. Out')),
      L("Choice number three says sixty k t over d. Sixty times ten times two is twelve hundred, and twelve hundred over "
        "forty is thirty. That's our target.", show(q6e, 'Choice number three says')),
      L("Choice number four says k d over sixty t. That's four hundred over a hundred twenty, a bit more than three. Out.",
        show(q6f, "That's four hundred over"), mk('cross', 'choice 4', 'a bit more than three. Out')),
      L("A speed of sixty is allowed too. But it makes two choices match here. That doesn't make both correct. If two choices match, try new easy numbers on those two.",
        show(q6g, 'If two choices match'))),
    S('Method 2 · The math way',
      L("[pause] Now the math way, with the letters. We start again from the givens. The speed is the distance divided by "
        "the time, d over t.", show(q6h, 'd over t')),
      L("The time for k kilometers is k divided by d over t. Dividing by a fraction is multiplying by its flip. So it's k t "
        "over d hours.", show(q6i, 'Dividing by a fraction')),
      L("They ask for minutes, so we multiply the hours by sixty. That's sixty k t over d, choice number three.",
        show(q6j, 'we multiply the hours by sixty'))),
    S('Method 3 · Understanding: the units',
      L("[pause] Now by understanding, starting with the units. We start again from the givens. k and d are kilometers, and t "
        "is hours.", show(q6k, 'k and d are kilometers')),
      L("The answer is a time. So the kilometers must cancel."),
      L("Choice number two is sixty d over k t. The kilometers cancel, leaving one over hours. Choice number four is k d over sixty t. It has kilometers squared over hours. Neither one "
        "is a time, so both are out.", show(q6l, 'Neither one is a time'), mk('cross', 'choice 2', 'so both are out'),
        mk('cross', 'choice 4', 'so both are out')),
      L("The units alone leave two choices. Choice number one is k t over sixty d. Choice number three is sixty k t over d."),
      L("We still need the distance ratio. k over d tells us how many copies of the original distance we travel. At the same speed, the time is that many copies of t hours."),
      L("So k t over d is the time in hours. To convert hours to minutes, we multiply by sixty, not divide. So the sixty must be on top. That's choice number three.",
        show(q6ratio, 'k t over d is the time in hours'), show(q6m, 'so the sixty must be on top'), mk('cross', 'choice 1', 'must be on top')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])
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
STEMS_T27 = {
 "wp27-g107": "An electric scooter moves at 6 meters per second. How many kilometers does it travel in 50 minutes?",
 "wp27-g108": "A gondola lift climbs along a straight cable at 17 kph. After 6 minutes, its horizontal distance from the bottom station is 1.5 kilometers. How high above the bottom station is it, in kilometers?",
 "wp27-g109": "A car drives from a city to the coast at 105 kph and returns along the same road at 70 kph, without stopping. What is its average speed for the whole round trip?",
 "wp27-g111": "Maya and Theo start at the same time from opposite ends of a bike trail and ride toward each other. Theo rides at 1.25 times Maya’s speed. What fraction of the trail does Maya cover before they meet?",
 "wp27-g112": "A rowboat and a motorboat leave opposite ends of a lake at the same time, each heading for the other end. The motorboat is 4.5 times as fast as the rowboat. By the time the motorboat reaches the far end, what fraction of the length of the lake has the rowboat traveled?",
 "q-r26-t27-31": "A delivery van travels 3 times as far as a scooter, at 1.5 times the scooter's speed. The scooter's trip takes 40 minutes. How many minutes does the van's trip take?",
 "wp27-g114": "Two runners leave the same gate at the same time and run in opposite directions along a straight path. Their speeds are 8 and 10 kph. After how many minutes are they 1,800 meters apart?",
 "wp27-g115": "At 09:00 a bus leaves Oakton for Bayside at 72 kph. At 09:20 a car leaves Bayside for Oakton at 108 kph. The towns are 204 kilometers apart. When do they meet?",
 "wp27-g116": "Zoe rides her bike from home at 15 kph. Twelve minutes later, her brother Sam leaves home along the same route and catches up with Zoe 20 minutes after he starts. What is Sam’s speed?",
 "wp27-g117": "A motorbike travels 9 kilometers in 15 minutes. A train travels 15 kilometers in 9 minutes. What is the difference between their speeds, in kph?",
 "wp27-g118": "An elevator normally rises 60 meters in 20 seconds, at a constant speed. On one trip, it rises the first half of the way at twice its normal speed and the second half at half its normal speed. How many seconds does this trip take?",
 "wp27-g120": "A ferry covers a route of 360 kilometers in 12 hours. A new ferry travels 60% faster. How many hours does the new ferry take on the same route?",
 "wp27-g119": "B is the midpoint of a straight road from A to C. One motorcyclist rides from A to C at 48 kph. Another takes 20 minutes from A to B, then rides from B to C at 36 kph. Their total travel times are equal. How many kilometers long is AC?",
 "wp27-g121": "Two runners start together from the same point of a circular track, running in the same direction. The track is 400 meters long. Their speeds are 12 and 9 kph. How many minutes pass between consecutive meetings?",
 "q-r26-t27-01": "A train 300 meters long travels at a constant speed. It passes a signal post in 15 seconds. How many seconds does it take to cross a bridge 500 meters long completely?",
 "q-r26-t27-02": "A boat travels 48 km downstream in 2 hours. The return trip upstream, along the same route, takes 3 hours. The boat’s speed in still water does not change. What is the speed of the current, in kph?",
 "q-r26-t27-03": "Two cyclists start together from the same point of a circular track 1.2 km long and ride in opposite directions. Their speeds are 20 kph and 16 kph. After how many minutes do they meet for the first time?",
 "q-r26-t27-05": "A cyclist rides from home to work at a constant speed. If she rode 25% faster, the trip would take 12 minutes less. How many minutes does the trip take at her usual speed?",
 "q-r26-t27-06": "A car travels $d$ kilometers in $t$ hours. At the same speed, how many minutes does it take to travel $k$ kilometers?",
}


# 2026-10-23: the last baseline of each question's stem on the board (estimated from the stem length, about 64 characters
# a line, then checked on the rendered step frames).
def _qbot_est(stem):
    import textwrap
    n = len(textwrap.wrap(re.sub(r'\$', '', stem), 64))
    return {1: 137, 2: 181, 3: 232, 4: 286, 5: 330}.get(n, 330)
for _v, _V in VIDEOS.items():
    if _V['kind'] == 'solution' and _V.get('qid') in STEMS_T27 and _v not in QBOT:
        QBOT[_v] = _qbot_est(STEMS_T27[_V['qid']])


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
WIDE = {'g14s', 'g15s', 'g15t', 'g16s', 'q1s', 'g12s'}
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


# 2026-10-23 visual check (V4): each result at its own clause
_clause_rows('wp-106', 'm_u2', ('$1$ hour $=60$ minutes', 'One hour is sixty minutes'),
             ('$1$ minute $=60$ seconds', 'one minute is sixty seconds'))
_clause_rows('wp-106', 'm_p2', ('$3^2=9$', 'Three squared is nine'),
             ('$4^2=16$', 'four squared is sixteen'), ('$9+16=25$', 'Nine plus sixteen is twenty-five'),
             ('$25=5^2$', 'twenty-five is five squared'))
_clause_rows('r26-t27-special', 'x3d', ('$3$ km: $\\ 60$ min', 'Three kilometers take sixty minutes'),
             ('$0.6=\\frac{1}{5}$ of $3$: $\\ 60\\div5=12$ min', 'a fifth of sixty minutes'))
_clause_rows('r26-t27-special', 'x4c', ('$18$ km: $\\ 60$ min', 'Eighteen kilometers take sixty minutes'),
             ('$0.6=18\\div30$: $\\ 60\\div30=2$ min', 'So the time is sixty'))
_clause_rows('r26-t27-special', 'x4e', ('$12$ km: $\\ 60$ min', 'Twelve kilometers take sixty minutes'),
             ('$1$ km: $\\ 60\\div12=5$ min', 'one kilometer takes sixty divided by twelve'))
_clause_rows('solve-wp27-g121', 'g21d', ('$3$ km: $\\ 60$ min', 'Three kilometers take sixty minutes'),
             ('$1$ km: $\\ 60\\div3=20$ min', 'one kilometer takes sixty divided by three'))
_clause_rows('solve-wp27-g109', 'g9c2', ('$105\\times2=210$', 'a hundred five times two'),
             ('$70\\times3=210$', 'seventy times three is two hundred ten'))
_clause_rows('solve-wp27-g115', 'g15h', ('$72\\times\\frac{4}{3}$', 'Seventy-two times four thirds'),
             ('$72\\div3=24$', 'A third of seventy-two'), ('$24\\times4=96$ km', 'times four is ninety-six'))
_clause_rows('solve-wp27-g120', 'g20e', ('$360\\div12=30$', 'Three hundred sixty divided by twelve'),
             ('$48\\div12=4$', 'Forty-eight divided by twelve'))
_clause_rows('solve-q-r26-t27-02', 'q2c', ('boat $10$, $\\ $current $2$', 'A boat goes ten kilometers per hour'),
             ('down: $\\ 10+2=12$', 'Downstream it goes ten plus two'), ('up: $\\ 10-2=8$', 'Upstream, ten minus two'))
_clause_rows('solve-q-r26-t27-03', 'q3b', ('time $=1.2\\div36$', 'The time is one point two divided by thirty-six'),
             ('$=\\frac{12}{360}$', 'so it\'s twelve over three hundred'), ('$=\\frac{1}{30}$ hour', 'one thirtieth of an hour'))
_clause_rows('solve-q-r26-t27-06', 'q6e', ('(3) $\\ \\frac{60\\cdot10\\cdot2}{40}$', 'Choice number three says'),
             ('$=\\frac{1200}{40}=30$', 'twelve hundred over forty is thirty'))
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
 "wp27-g107": "An electric scooter moves at 6 meters per second. How many kilometers does it travel in 50 minutes?",
 "wp27-g108": "A gondola lift climbs along a straight cable at 17 kph. After 6 minutes, its horizontal distance from the bottom station is 1.5 kilometers. How high above the bottom station is it, in kilometers?",
 "wp27-g109": "A car drives from a city to the coast at 105 kph and returns along the same road at 70 kph, without stopping. What is its average speed for the whole round trip?",
 "wp27-g111": "Maya and Theo start at the same time from opposite ends of a bike trail and ride toward each other. Theo rides at 1.25 times Maya’s speed. What fraction of the trail does Maya cover before they meet?",
 "wp27-g112": "A rowboat and a motorboat leave opposite ends of a lake at the same time, each heading for the other end. The motorboat is 4.5 times as fast as the rowboat. By the time the motorboat reaches the far end, what fraction of the length of the lake has the rowboat traveled?",
 "q-r26-t27-31": "A delivery van travels 3 times as far as a scooter, at 1.5 times the scooter's speed. The scooter's trip takes 40 minutes. How many minutes does the van's trip take?",
 "wp27-g114": "Two runners leave the same gate at the same time and run in opposite directions along a straight path. Their speeds are 8 and 10 kph. After how many minutes are they 1,800 meters apart?",
 "wp27-g115": "At 09:00 a bus leaves Oakton for Bayside at 72 kph. At 09:20 a car leaves Bayside for Oakton at 108 kph. The towns are 204 kilometers apart. When do they meet?",
 "wp27-g116": "Zoe rides her bike from home at 15 kph. Twelve minutes later, her brother Sam leaves home along the same route and catches up with Zoe 20 minutes after he starts. What is Sam’s speed?",
 "wp27-g117": "A motorbike travels 9 kilometers in 15 minutes. A train travels 15 kilometers in 9 minutes. What is the difference between their speeds, in kph?",
 "wp27-g118": "An elevator normally rises 60 meters in 20 seconds, at a constant speed. On one trip, it rises the first half of the way at twice its normal speed and the second half at half its normal speed. How many seconds does this trip take?",
 "wp27-g120": "A ferry covers a route of 360 kilometers in 12 hours. A new ferry travels 60% faster. How many hours does the new ferry take on the same route?",
 "wp27-g119": "B is the midpoint of a straight road from A to C. One motorcyclist rides from A to C at 48 kph. Another takes 20 minutes from A to B, then rides from B to C at 36 kph. Their total travel times are equal. How many kilometers long is AC?",
 "wp27-g121": "Two runners start together from the same point of a circular track, running in the same direction. The track is 400 meters long. Their speeds are 12 and 9 kph. How many minutes pass between consecutive meetings?",
 "q-r26-t27-01": "A train 300 meters long travels at a constant speed. It passes a signal post in 15 seconds. How many seconds does it take to cross a bridge 500 meters long completely?",
 "q-r26-t27-02": "A boat travels 48 km downstream in 2 hours. The return trip upstream, along the same route, takes 3 hours. The boat’s speed in still water does not change. What is the speed of the current, in kph?",
 "q-r26-t27-03": "Two cyclists start together from the same point of a circular track 1.2 km long and ride in opposite directions. Their speeds are 20 kph and 16 kph. After how many minutes do they meet for the first time?",
 "q-r26-t27-05": "A cyclist rides from home to work at a constant speed. If she rode 25% faster, the trip would take 12 minutes less. How many minutes does the trip take at her usual speed?",
 "q-r26-t27-06": "A car travels $d$ kilometers in $t$ hours. At the same speed, how many minutes does it take to travel $k$ kilometers?",
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
MV.carry(_types.SimpleNamespace(**globals()), CARRY27)
for _v in CARRY27:                                      # 2026-10-18 visual check: the So-far box at a readable size
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
