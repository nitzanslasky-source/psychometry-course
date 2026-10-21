"""Topic 34 (Polygons) - the scripts for the teacher's own-voice reading (2026-10-21), written from the first draft to
the guide (R1-R37, W1-W21), the clarity style, the Codex review standard and Rule V3/V4 geometry visuals, built exactly like
topic 33 (math_patches/_ai_vis_t33.py: the DSL, the GEO colour builders, the geometry handwriting hook and the visual
passes are copied here, so the topics stay independent).

The camera lesson 'geo-104' gets its own reading script, in parts of about 3-4 minutes (CAMERA_SPLIT at the end). Every
other topic-34 video gets a script that SHE reads aloud in the Reading Studio; reading_to_video.py times the handwriting
and the visuals to her words. The summary video r26-t34-summary is replaced by the printable page summary_pages/t34.json.

ONE spec per video drives the script (ai_scripts/<vid>.json), the visual plan (VIS[vid], _ai_visual.py format) and the
studio video (t34.py ai_redo_t34() rebuilds the slides from studio_slides(vid), then _ai_visual.apply()).

R37 (2026-10-21): the core methods of polygons are taught in the LESSONS (the camera lesson geo-104: angle sum, +180 per
side, regular, one angle, central and exterior angles, diagonals split the angle, radii triangles; geo-105: areas by
splitting, the hexagon and the octagon splits; geo-109: the triangles inside regular polygons and the hexagon's
diagonals; geo-112-after: the two hexagon partitions; r26-t34-meet: polygons meeting at a point); the first question
that uses a method applies it slowly with a one-sentence link to the lesson; one-off tricks are taught in their question.

Spec DSL (as in topic 33): video / S / SM / L / I / IH / show / pt / mk / GEO / PIN / _R / LEFT / ROWS / FLOW.
"""
import importlib.util, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _geo_hand as _GH

HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t34ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-34 flow order of the scripts
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
        out = []; ycol = 100 if V['kind'] == 'solution' else 78
        for it in items:
            d = {k: v for k, v in it.items() if not k.startswith('_')}
            if it['_col'] == 1 and not solo:
                if d['k'] == 'vis':
                    d['w'] = min(d.get('w', 540), 540); d['h'] = int(round(d['h'] * d['w'] / it['w']))
                y_here = ycol
                if not d.get('over'): ycol += (d['h'] if d['k'] == 'vis' else int(d.get('size', 36) * 1.55)) + 16
                d.update(x=1010, w=d['w'] if d['k'] == 'vis' else 540, y=y_here)
            elif right and d['k'] == 't':
                d['w'] = 560
            if it.get('_y'): d['y'] = it['_y']          # topic 17: a question with its own figure - place below it
            if it.get('_x'): d['x'] = it['_x']
            if it.get('_w'): d['w'] = it['_w']          # batch C: a narrower row box (two columns of rows)
            out.append((it, d))
        per.append(out)
    return names, per


# 2026-10-14 Rule V4.8 (camera lessons: the face bubble never covers math). Her bubble is composited top right (board
# x >= 1344, y <= 256). In the camera lesson and its parts: a right-column stack that would start above y 262 moves down
# as a whole (its own order and spacing kept), and a left-column item is at most 920 wide (ends left of x 1330; a figure
# and its layers are scaled down together, text wraps). Other videos are unchanged.
CAM_BASE = 'geo-104'
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
                    _h = None if (vid, si + 1) in _GH.NOHAND else (it['_hand'] or _GH.auto(vid, it, si))      # 2026-10-18: geometry worked lines hand-written (_geo_hand.py)
                    if _h and not it['_hand']: d = dict(d, _hwsize=d.get('size', 36))
                    if _h and vid not in _GH.FROZEN: _h = _GH.no_cross(_h)
                    cs.append(('write', d, c[2], _h) if _h else ('show', d, c[2]))
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
            'style': "the teacher reads it herself (Reading Studio), topic-34 scripts (2026-10-21): math_patches/_ai_vis_t34.py is "
                     "the source - edit there and re-run it. Rules: real_exam/TEACHING_STYLE_GUIDE.md R1-R37 (no 'which way is "
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


_studio_slides_plain = studio_slides


def studio_slides(vid):
    out, sb = _studio_slides_plain(vid)
    if vid in FIG_LEFT:
        for b in out:
            for it in b['pre']: it.update(figw=0.56, figalign='left')
    for k, b in enumerate(out):
        if (vid, k) in NOFIG34:
            for it in b['pre']: it.update(nofig=1)
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
    L_, R_, Y_ = 40, 600, 92
    X = lambda v: L_ + 16 + (v - lo) / float(hi - lo) * (R_ - L_ - 32)
    INK, TEAL, BAND, FONT = SNL.INK, SNL.TEAL, SNL.BAND, SNL.FONT
    VB = '0 0 640 160'
    def txt(x, y, t, c, size=24, style=''):
        return ('<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="%d" font-weight="bold"%s>%s</text>'
                % (x, y, c, FONT, size, (' font-style="%s"' % style) if style else '', t))
    body = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.5"/>' % (L_ - 6, Y_, R_ + 6, Y_, INK) +
            '<path d="M %d %d l 12 -7 l 0 14 Z" fill="%s"/>' % (L_ - 10, Y_, INK) + '<path d="M %d %d l -12 -7 l 0 14 Z" fill="%s"/>' % (R_ + 10, Y_, INK))
    for t in ticks:
        v, lab = t if isinstance(t, tuple) else (t, ('−%s' % -t) if t < 0 else str(t))
        body += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2"/>' % (X(v), Y_ - 10, X(v), Y_ + 10, INK) + txt(X(v), Y_ + 38, lab, INK, 25)
    out = [('line', _svg(VB, body, title))]
    for key, marks in layers:
        b = ''
        for m in marks:
            if m[0] in ('pt', 'ink'):
                c = TEAL if m[0] == 'pt' else INK
                b += '<circle cx="%.1f" cy="%d" r="7" fill="%s"/>' % (X(m[1]), Y_, c) + txt(X(m[1]), Y_ - 20, m[2], c, 26, 'italic')
            elif m[0] == 'arrow':
                a, e = X(m[1]), X(m[2]); d = 1 if e > a else -1
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3"/>' % (a, Y_ - 50, e - 10 * d, Y_ - 50, TEAL) +
                      '<path d="M %.1f %d l %d -7 l 0 14 Z" fill="%s"/>' % (e, Y_ - 50, -14 * d, TEAL))
                if m[3]: b += txt((a + e) / 2, Y_ - 62, m[3], TEAL, 22)
            elif m[0] == 'shade':
                b += '<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (X(m[1]), Y_ - 7, X(m[2]) - X(m[1]), BAND, TEAL)
            elif m[0] == 'cross':
                x0 = X(m[1]); y0 = Y_ - 50
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (x0 - 14, y0 - 14, x0 + 14, y0 + 14, RED) +
                      '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (x0 + 14, y0 - 14, x0 - 14, y0 + 14, RED))
            elif m[0] == 'below':
                b += txt(X(m[1]), Y_ + 62, m[2], TEAL, 22)
        out.append((key, _svg(VB, b, key)))
    return _layers(name, out, w, col)

# ------------------------------------------------------------------------------------------- method visuals (V1)
# 2026-10-13 rewrite in the clarity style (TEACHING_STYLE_GUIDE "Clarity style") with the method-visual rule V1: the
# Hebrew topic-19 pictures are built step by step - THE SAME TEMPLATE with the input in every slot (alg 18853-18868,
# SLOT) and the inner operation coloured and replaced by its value, inside out (alg 18910-18925, CHAIN; the circular rule
# goes down and climbs back up, alg 19048-19114, CHAIN up=). Layers are shown right after their base (no item between).
_mv_spec = importlib.util.spec_from_file_location('_method_visuals', os.path.join(HERE, '_method_visuals.py'))
MV = importlib.util.module_from_spec(_mv_spec); _mv_spec.loader.exec_module(MV)


# ------------------------------------------------------------------------------------------- topic-33 geometry figures (V1)
# 2026-10-14 the teaching figures of lines and angles, in colour, BUILT in layers at the spoken words (the lines first, then
# each angle / mark as she talks about it). Coordinates are SVG units in a 640 x 360 box (y grows downwards); angles are in
# degrees, counter-clockwise from the right (math convention, y up). The question figures themselves are the course's (black
# and white, another agent's pipeline); these are our own board copies.
GINK, GTEAL, GRED, GORANGE, GBAND = '#203344', '#087f83', '#d62d48', '#c76a00', '#d5f1ed'
GCOL = {'ink': GINK, 'teal': GTEAL, 'red': GRED, 'orange': GORANGE, 'small': GTEAL, 'large': GORANGE}
GFONT = 'font-family="DejaVu Sans,Arial,sans-serif"'


def gpt(cx, cy, r, deg):
    import math
    return cx + r * math.cos(math.radians(deg)), cy - r * math.sin(math.radians(deg))


def gdir(x1, y1, x2, y2):
    """the direction (degrees, math convention) from (x1, y1) to (x2, y2)"""
    import math
    return math.degrees(math.atan2(-(y2 - y1), x2 - x1)) % 360


def gcross(p1, p2, p3, p4):
    """the intersection of line p1-p2 with line p3-p4"""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
    return x1 + t * (x2 - x1), y1 + t * (y2 - y1)


def _gtxt(x, y, t, c=GINK, size=26, italic=False):
    return ('<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="middle" fill="%s" %s font-size="%d" '
            'font-weight="bold"%s>%s</text>' % (x, y, c, GFONT, size, ' font-style="italic"' if italic else '',
                                                 str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')))


def _gel(e):
    k = e[0]
    if k == 'seg':          # ('seg', x1, y1, x2, y2[, colour[, width[, dashed]]])
        x1, y1, x2, y2 = e[1:5]; c = GCOL.get(e[5] if len(e) > 5 else 'ink'); w = e[6] if len(e) > 6 else 3
        dash = ' stroke-dasharray="9 7"' if len(e) > 7 and e[7] else ''
        return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" stroke-linecap="round"%s/>' % (x1, y1, x2, y2, c, w, dash)
    if k == 'path':         # ('path', [(x, y), ...], colour[, width])  an open polyline (the Z, the U)
        pts = e[1]; c = GCOL.get(e[2]); w = e[3] if len(e) > 3 else 6
        d = 'M ' + ' L '.join('%.1f %.1f' % tuple(p) for p in pts)
        return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round" opacity="0.55"/>' % (d, c, w)
    if k == 'dot':          # ('dot', x, y[, label, dx, dy])
        s = '<circle cx="%.1f" cy="%.1f" r="5.5" fill="%s"/>' % (e[1], e[2], GINK)
        if len(e) > 3: s += _gtxt(e[1] + (e[4] if len(e) > 4 else 0), e[2] + (e[5] if len(e) > 5 else -22), e[3], GINK, 26, True)
        return s
    if k == 'txt':          # ('txt', x, y, text[, colour[, size[, italic]]])
        return _gtxt(e[1], e[2], e[3], GCOL.get(e[4] if len(e) > 4 else 'ink'), e[5] if len(e) > 5 else 26, e[6] if len(e) > 6 else False)
    if k in ('arc', 'wedge'):   # ('arc', cx, cy, r, a1, a2, colour[, label[, label radius]])  a1 -> a2 counter-clockwise
        cx, cy, r, a1, a2, col = e[1:7]; c = GCOL.get(col)
        a2 = a2 if a2 > a1 else a2 + 360
        (x1, y1), (x2, y2) = gpt(cx, cy, r, a1), gpt(cx, cy, r, a2); big = 1 if a2 - a1 > 180 else 0
        if k == 'wedge':
            s = ('<path d="M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 %d 0 %.1f %.1f Z" fill="%s" opacity="0.28" stroke="none"/>'
                 % (cx, cy, x1, y1, r, r, big, x2, y2, c))
        else:
            s = '<path d="M %.1f %.1f A %.1f %.1f 0 %d 0 %.1f %.1f" fill="none" stroke="%s" stroke-width="3.2"/>' % (x1, y1, r, r, big, x2, y2, c)
        if len(e) > 7 and e[7]:
            lx, ly = gpt(cx, cy, e[8] if len(e) > 8 else r + 24, (a1 + a2) / 2.0)
            s += _gtxt(lx, ly, e[7], c, 24)
        return s
    if k == 'right':        # ('right', cx, cy, a1, a2[, size[, colour]])  the right-angle square, with its dot
        cx, cy, a1, a2 = e[1:5]; sz = e[5] if len(e) > 5 else 16; c = GCOL.get(e[6] if len(e) > 6 else 'teal')
        p1 = gpt(cx, cy, sz, a1); p2 = gpt(cx, cy, sz, a2); p3 = (p1[0] + p2[0] - cx, p1[1] + p2[1] - cy)
        dx, dy = (p3[0] + cx) / 2.0, (p3[1] + cy) / 2.0
        return ('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="%s" stroke-width="2.4"/>'
                '<circle cx="%.1f" cy="%.1f" r="2.4" fill="%s"/>' % (p1[0], p1[1], p3[0], p3[1], p2[0], p2[1], c, dx, dy, c))
    if k == 'tick':         # ('tick', x1, y1, x2, y2[, n[, colour]])  n tick marks across the middle of a segment (equal sides)
        import math
        x1, y1, x2, y2 = e[1:5]; n = e[5] if len(e) > 5 else 1; c = GCOL.get(e[6] if len(e) > 6 else 'teal')
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; nx, ny = -uy, ux
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0; s = ''
        for i in range(n):
            o = (i - (n - 1) / 2.0) * 7
            cx, cy = mx + ux * o, my + uy * o
            s += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"/>' % (cx - nx * 10, cy - ny * 10, cx + nx * 10, cy + ny * 10, c)
        return s
    if k == 'par':          # ('par', x1, y1, x2, y2[, n[, colour]])  parallel arrow(s) in the middle of a segment, pointing to (x2, y2)
        import math
        x1, y1, x2, y2 = e[1:5]; n = e[5] if len(e) > 5 else 1; c = GCOL.get(e[6] if len(e) > 6 else 'teal')
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; nx, ny = -uy, ux
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0; s = ''
        for i in range(n):
            o = (i - (n - 1) / 2.0) * 11 + 6
            tx, ty = mx + ux * o, my + uy * o
            s += ('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/>'
                  % (tx - ux * 11 + nx * 8, ty - uy * 11 + ny * 8, tx, ty, tx - ux * 11 - nx * 8, ty - uy * 11 - ny * 8, c))
        return s
    if k == 'tint':         # ('tint', [(x, y), ...], colour)  a steady tint on a region (a polygon)
        return '<path d="M %s Z" fill="%s" opacity="0.22" stroke="none"/>' % (' L '.join('%.1f %.1f' % tuple(p) for p in e[1]), GCOL.get(e[2]))
    if k == 'dim':          # ('dim', x, y, w, h)  fades everything drawn so far (focus: the part redrawn after it stands out)
        return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#ffffff" opacity="0.72"/>' % tuple(e[1:5])
    # ---- topic 33 (circles) elements
    if k == 'circ':         # ('circ', cx, cy, r[, colour[, width[, dashed[, fill colour]]]])  a circle (fill = a steady tint)
        cx, cy, r = e[1:4]; c = GCOL.get(e[4] if len(e) > 4 else 'ink'); w = e[5] if len(e) > 5 else 3
        dash = ' stroke-dasharray="9 7"' if len(e) > 6 and e[6] else ''
        f = ('fill="%s" fill-opacity="0.22"' % GCOL.get(e[7])) if len(e) > 7 and e[7] else 'fill="none"'
        return '<circle cx="%.1f" cy="%.1f" r="%.1f" %s stroke="%s" stroke-width="%s"%s/>' % (cx, cy, r, f, c, w, dash)
    if k == 'arcw':         # ('arcw', cx, cy, r, a1, a2, colour[, width])  a thick highlighted arc of a circle, a1 -> a2 counter-clockwise
        cx, cy, r, a1, a2, col = e[1:7]; c = GCOL.get(col); w = e[7] if len(e) > 7 else 7
        a2 = a2 if a2 > a1 else a2 + 360
        (x1, y1), (x2, y2) = gpt(cx, cy, r, a1), gpt(cx, cy, r, a2); big = 1 if a2 - a1 > 180 else 0
        return ('<path d="M %.1f %.1f A %.1f %.1f 0 %d 0 %.1f %.1f" fill="none" stroke="%s" stroke-width="%s" '
                'stroke-linecap="round" opacity="0.8"/>' % (x1, y1, r, r, big, x2, y2, c, w))
    if k == 'cseg':         # ('cseg', cx, cy, r, a1, a2, colour)  a circular segment (between the chord and the arc a1 -> a2), tinted
        cx, cy, r, a1, a2, col = e[1:7]; c = GCOL.get(col)
        a2 = a2 if a2 > a1 else a2 + 360
        (x1, y1), (x2, y2) = gpt(cx, cy, r, a1), gpt(cx, cy, r, a2); big = 1 if a2 - a1 > 180 else 0
        return '<path d="M %.1f %.1f A %.1f %.1f 0 %d 0 %.1f %.1f Z" fill="%s" opacity="0.28" stroke="none"/>' % (x1, y1, r, r, big, x2, y2, c)
    if k == 'region':       # ('region', svg path d, colour[, opacity])  any tinted region (even-odd: a ring, a circle minus a square ...)
        return '<path d="%s" fill="%s" fill-rule="evenodd" opacity="%s" stroke="none"/>' % (e[1], GCOL.get(e[2]), e[3] if len(e) > 3 else 0.28)
    raise ValueError(k)


def GEO(name, layers, vb='0 0 640 360', w=540, col=1, title='Figure'):
    """a geometry figure built in layers: layers = [('line', [element, ...]), (key, [element, ...]), ...]; the 'line' layer
    is the base (the lines of the figure), every later layer is drawn over it at the spoken words, shown in order right
    after the base (no other item in between). Elements: see _gel. -> {key: item}"""
    out = []
    for key, els in layers:
        body = ''.join(_gel(e) for e in els)
        t = title if key == 'line' else '%s: %s' % (title, key)
        out.append((key, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
                    % (vb, t, t, body)))
    return _layers(name, out, w, col)



CARRY34 = {}       # carry-over boxes (V2): {vid: {slide index: [tex, ...]}}, filled by the scripts


# ------------------------------------------------------------------------------------------- question-video placement
# (from topic 30) The question figure sits on the left (figw 0.56, as in the course's geometry videos); our colour board
# copies and typed steps go in the right column with explicit y (_R). SM = a slide titled without "Method N ·" (no header
# drawn over a tall question figure); the sidebar still names the method.
def _R(it, y, x=1040):
    """place an item (or every layer of a GEO figure) in the right column at board y"""
    for t in (it.values() if '_name' not in it else [it]):
        t['_col'] = 1; t['_x'] = x; t['_y'] = y
    return it


def SM(sb, title, *lines):
    return S(title, *lines, sb=sb)


FIG_LEFT = set()      # question videos whose question figure goes on the left (figw 0.56); filled by the scripts
NOFIG34 = set()       # 2026-10-18 (batch C, as NOFIG31 in topic 31): (video, slide index) that show our enlarged copy
                      # instead of the question figure; the working is written in readable rows on the right (ROWS)


def LEFT(g, y=300, x=410, w=None):
    """(batch C) place a GEO figure (every layer) in the left work area of a NOFIG34 slide, optionally at a new width"""
    for t in (g.values() if '_name' not in g else [g]):
        t['_col'] = 0; t['_x'] = x; t['_y'] = y
        if w and t['k'] == 'vis':
            vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', t['v']['svg']).group(1).split()]
            t['w'] = w; t['h'] = int(round(w * vb[3] / vb[2]))
    return g


def ROWS(y0, dy, *items, x=1040, w=None):
    """(batch C) readable working rows in the right column, one under the other, each shown at its own clause;
    w = the rows' box width (for two columns of rows side by side: the studio pushes a box down when it overlaps)"""
    for i, it in enumerate(items):
        _R(it, y0 + i * dy, x)
        if w: it['_w'] = w
    return items


def SLOT(name, rule, rows, col=0, size=34):
    return MV.items(_layers, name, MV.SLOT(rule, rows, size=size), col=col)


def CHAIN(name, rows, up=None, col=0, size=34, links=None):
    return MV.items(_layers, name, MV.CHAIN(rows, up=up, size=size, links=links), col=col)


def _hand(tex):
    """the hand-written twin of a typed line (studio_handwrite syntax), or None if it has a glyph the pen lacks"""
    t = tex
    for a, b in [('\\blacklozenge', '◆'), ('\\cdot', '·'), ('\\ne', '≠'), ('\\le', '≤'), ('\\ge', '≥'), ('\\to', '→'),
                 ('\\quad', '    '), ('\\qquad', '      '), ('\\ ', ' '), ('\\,', ''), ('\\star', '⋆'), ('\\div', '÷'),
                 ('\\left', ''), ('\\right', '')]:
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




def PIN(g):
    """(topic-31/32 lesson) every layer of a GEO figure is drawn at its base figure's box (fig / of), so a base that the
    renderer moves or shrinks to fit keeps its layers exactly on top of it. Use it on every GEO figure: PIN(GEO(...))."""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g
# ------------------------------------------------------------------------------------------------ geo-074 (camera lesson, in parts)
# 2026-10-14 her camera first lesson of circles as a reading script (camera on), with more examples, split into parts of
# about 3-4 minutes (CAMERA_SPLIT at the end). Hebrew: geo 3446-3512 (circle vocabulary): "before the rules, get to know
# the lines and the angles in a circle"; circle vs disk (the round line vs everything inside, the wooden disk); radius
# (center to the circle; all radii of one circle are equal - spin the radius; marked r); chord (two points on the circle;
# infinitely many, not equal: long, short, very short); the longest chord goes through the middle = the diameter (two
# halves, 2r because it is two radii); inscribed angle (between two chords, vertex ON the circle; two lines stopping inside
# or outside are not); central angle (from the name: vertex at the center, between two radii); arc (a part of the circle,
# short or very long, almost the whole circle; a chord splits the circle into two arcs; "an arc is not only something
# short"); an arc closed off by two radii (central angle) or by two chords (inscribed angle) - the angle "intercepts" the
# arc (her "leans on"): stand inside the angle, the arms are tall walls, the part of the circle you can see; close: next
# lesson the rules. Kept from the English lesson: on the exam "circle" is used for both ("area of the circle" = the
# inside), diameter 14 -> radius 7, minor / major arc (exam wording), "intercepts". Added (the teacher's list for this
# lesson): all radii equal -> two radii make an isosceles triangle (topic 31); tangent, sector and segment as words only
# (their rules come in their own lessons: geo-077 tangents, geo-081 sectors; a segment appears in shaded-area questions).
# Study plan: day 5, after 1, 30, 2, 4, 31, 6, 8, 32, 9, 10 - the isosceles triangle (topic 31) is a short reminder.
# Visuals (V3): every term built on a clean circle at her words: the circle ink, the term being taught teal (a radius, a
# chord, an arc, a small angle), a large angle / the other arc orange, a non-example red; regions tinted (the disk, a
# half, a sector, a segment); each general property shown on 2-3 circles (variations).

# ------------------------------------------------------------------------------------------------ topic-34 polygon helpers
# 2026-10-21 regular and general polygons for the GEO builder (coordinates: SVG units, y down; angles in degrees, counter-
# clockwise from the right). Two new element kinds: 'raw' (ready SVG markup, e.g. the question's own black-and-white figure,
# so our colour copy sits exactly on it) and 'poly' (a closed outline).
import math as _pm
_gel_t33 = _gel


def _gel(e):
    if e[0] == 'raw':       # ('raw', svg markup)
        return e[1]
    if e[0] == 'poly':      # ('poly', [(x, y), ...][, colour[, width[, dashed]]])  a closed outline
        c = GCOL.get(e[2] if len(e) > 2 else 'ink'); w = e[3] if len(e) > 3 else 3
        dash = ' stroke-dasharray="9 7"' if len(e) > 4 and e[4] else ''
        return ('<path d="M %s Z" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round"%s/>'
                % (' L '.join('%.1f %.1f' % tuple(p) for p in e[1]), c, w, dash))
    return _gel_t33(e)


def rp(cx, cy, R, n, start=90):
    """the vertices of a regular n-gon around (cx, cy), circumradius R, the first one at `start` degrees, counter-clockwise"""
    return [gpt(cx, cy, R, start + 360.0 * k / n) for k in range(n)]


def sg(P, Q, col='ink', w=3, dash=False):
    return ('seg', P[0], P[1], Q[0], Q[1], col, w, dash)


def pdot(P):
    return ('dot', P[0], P[1])


def nm(P, t, c=None, d=26, col='ink', size=26):
    """a vertex name, pushed d units away from the point c (the shape's middle) - or at an offset (dx, dy) when c is a tuple of 2 numbers given as 'dxdy'"""
    if c is None: return ('txt', P[0], P[1] - d, t, col, size, True)
    dx, dy = P[0] - c[0], P[1] - c[1]; L = _pm.hypot(dx, dy) or 1
    return ('txt', P[0] + dx / L * d, P[1] + dy / L * d, t, col, size, True)


def at(P, t, dx=0, dy=0, col='ink', size=26, italic=False):
    return ('txt', P[0] + dx, P[1] + dy, t, col, size, italic)


def mid(P, Q, d=0, side=1):
    """the midpoint of P-Q, pushed d units sideways"""
    mx, my = (P[0] + Q[0]) / 2.0, (P[1] + Q[1]) / 2.0
    L = _pm.hypot(Q[0] - P[0], Q[1] - P[1]) or 1
    return mx - (Q[1] - P[1]) / L * d * side, my + (Q[0] - P[0]) / L * d * side


def side_lab(P, Q, t, c, d=20, col='ink', size=24):
    """a label for side P-Q, pushed away from the point c"""
    m = mid(P, Q); dx, dy = m[0] - c[0], m[1] - c[1]; L = _pm.hypot(dx, dy) or 1
    return ('txt', m[0] + dx / L * d, m[1] + dy / L * d, t, col, size, False)


def ang(V, P, Q, r, col, lab=None, lr=None, size=None):
    """the angle arc at V between the rays to P and Q (the smaller angle), with an optional label"""
    d1, d2 = gdir(V[0], V[1], P[0], P[1]), gdir(V[0], V[1], Q[0], Q[1])
    if (d2 - d1) % 360 > 180: d1, d2 = d2, d1
    e = ('arc', V[0], V[1], r, d1, d2, col)
    if lab: e = e + (lab, lr if lr else r + 22)
    return e


def angw(V, P, Q, r, col):
    """the angle at V as a tinted wedge (the smaller angle)"""
    d1, d2 = gdir(V[0], V[1], P[0], P[1]), gdir(V[0], V[1], Q[0], Q[1])
    if (d2 - d1) % 360 > 180: d1, d2 = d2, d1
    return ('wedge', V[0], V[1], r, d1, d2, col)


def alab(V, P, Q, d, t, col='teal', size=22):
    """a label inside the angle at V (on its bisector, d units from V)"""
    d1, d2 = gdir(V[0], V[1], P[0], P[1]), gdir(V[0], V[1], Q[0], Q[1])
    if (d2 - d1) % 360 > 180: d1, d2 = d2, d1
    a = d1 + ((d2 - d1) % 360) / 2.0
    x, y = gpt(V[0], V[1], d, a)
    return ('txt', x, y, t, col, size, False)


def rt(V, P, Q, sz=14, col='teal'):
    """the right-angle square at V between the rays to P and Q"""
    return ('right', V[0], V[1], gdir(V[0], V[1], P[0], P[1]), gdir(V[0], V[1], Q[0], Q[1]), sz, col)


def tk(P, Q, n=1, col='teal'):
    return ('tick', P[0], P[1], Q[0], Q[1], n, col)


def cen(pts):
    return (sum(p[0] for p in pts) / float(len(pts)), sum(p[1] for p in pts) / float(len(pts)))


def foot(P, A, B):
    """the foot of the perpendicular from P to the line A-B"""
    ax, ay = A; bx, by = B; dx, dy = bx - ax, by - ay
    t = ((P[0] - ax) * dx + (P[1] - ay) * dy) / float(dx * dx + dy * dy)
    return ax + t * dx, ay + t * dy


def lerp(P, Q, t):
    return P[0] + (Q[0] - P[0]) * t, P[1] + (Q[1] - P[1]) * t




# 2026-10-18 batch C layout pass: rows that would run into the choices in the course renderer (math_check layout) are
# flowed into columns by their real height (the renderer pushes an overlapping box down, so each row needs its full box).
def _rowh(it):
    sz = it.get('size', 36); t = it.get('t', '')
    h = sz * 1.55 * (1.25 if it.get('_hand') else 1) + 22
    if '\\dfrac' in t: h += sz * 1.2
    elif '\\frac' in t: h += sz * 0.85
    return h


def FLOW(items, cols):
    """place rows in order down the columns cols = [(x, w, y_top, y_bottom), ...], each row at its full height"""
    k = 0; x, w, y, y1 = cols[0]
    for it in items:
        h = _rowh(it)
        while y + h > y1 and k + 1 < len(cols):
            k += 1; x, w, y, y1 = cols[k]
        _R(it, int(y), x); it['_w'] = w; y += h
    return items




def irr(cx, cy, R, n, start=90, f=None, turn=None):
    """a NOT regular n-gon: the regular one with each corner's radius times f[k] and its direction moved by turn[k] degrees"""
    f = f or [1] * n; turn = turn or [0] * n
    return [gpt(cx, cy, R * f[k], start + 360.0 * k / n + turn[k]) for k in range(n)]


def corners(pts, r, col, skip=()):
    """an angle arc at every corner of a convex polygon"""
    n = len(pts)
    return [ang(pts[k], pts[k - 1], pts[(k + 1) % n], r, col) for k in range(n) if k not in skip]


def angbig(V, P, Q, r, col):
    """the BIG angle (over 180) at V between the rays to P and Q"""
    d1, d2 = gdir(V[0], V[1], P[0], P[1]), gdir(V[0], V[1], Q[0], Q[1])
    if (d2 - d1) % 360 > 180: d1, d2 = d2, d1
    return ('arc', V[0], V[1], r, d2, d1, col)


def ticks(pts, n=1, col='teal'):
    return [tk(pts[k], pts[(k + 1) % len(pts)], n, col) for k in range(len(pts))]


def fan(pts, k, col='teal', w=3, dash=True):
    """the diagonals from corner k"""
    n = len(pts)
    return [sg(pts[k], pts[j], col, w, dash) for j in range(n) if j not in (k, (k + 1) % n, (k - 1) % n)]


def fan_tris(pts, k):
    """the triangles of the split from corner k, in order"""
    n = len(pts); out = []
    for j in range(1, n - 1):
        a, b = (k + j) % n, (k + j + 1) % n
        out.append([pts[k], pts[a], pts[b]])
    return out


# =================================================================================================================
# geo-104 (camera lesson, in parts) - Polygons
# 2026-10-21 her camera first lesson of polygons as a reading script (camera on), with more examples, split into parts of
# about 3-4 minutes (CAMERA_SPLIT at the end). Hebrew: geo 5098-5181 (polygons theory): a polygon is a closed shape with 3
# or more sides; we know the triangle and the quadrilateral; pentagon, hexagon, heptagon, octagon; the angle sum depends on
# the number of sides, 180(n - 2), checked on the quadrilateral; or split into triangles (as in the quadrilateral); +1 side
# = +180 (one more triangle); regular = all sides AND all angles equal (the folded hexagon); every regular polygon can be
# inscribed in a circle, not the other way (move a corner along the circle); one angle = the sum / n; the formula-sheet
# form 180 - 360/n (open the brackets, split the fraction); the table pentagon / hexagon / octagon: sums 540, 720, 1080,
# central angles 72, 60, 45, "complete to 180"; the diagonals split the angle equally (inscribed angles on equal arcs);
# radii -> n congruent isosceles triangles; the hexagon: 6 equilateral triangles; recap. Kept from the English lesson: the
# exterior angles (sum 360, the walk around; why "complete to 180" works). R37 additions (core methods, every rule on
# numbers): the sums of the hexagon and heptagon, the "+3 sides = +540" comparison (the real exam 2025 autumn q2_06), the
# sum back to n (900 -> 5 triangles -> 7 sides; the trap: 5), the rectangle as a non-example of regular, the octagon angle
# by halving, the exterior angles of the equilateral triangle and the square, the hexagon's 4 equal angles of 30, the
# pentagon's radii triangles 72 / 54 / 54 (a radius halves the corner's angle), radius = side in the hexagon.
# Study plan: after 30-33 (lines and angles, triangles, quadrilaterals, circles): the triangle's 180, the quadrilateral's
# 360, the isosceles and equilateral triangles, inscribed angles on equal arcs and the central angle are short reminders.
# Visuals (V3): each idea on clean shapes built at her words (the shape ink, the part under study teal, a non-example red,
# a second / third shape for every general rule), triangles tinted one by one as she counts them, values written as found.
# =================================================================================================================
# ---- names: six shapes, built as she names them
def _f1shape(cx, cy, n, name, f, turn, R=58):
    p = irr(cx, cy, R, n, 90, f, turn)
    return [('poly', p, 'ink', 3)] + [pdot(q) for q in p] + [('txt', cx, cy + R + 36, name, 'teal', 28)]
p104names = PIN(GEO('p104names', [
    ('line', _f1shape(100, 90, 3, '3: triangle', [1, 1.05, 0.9], [0, 8, -12])),
    ('q', _f1shape(320, 90, 4, '4: quadrilateral', [1, 0.85, 1.1, 0.9], [10, 0, -15, 5])),
    ('p5', _f1shape(540, 90, 5, '5: pentagon', [1, 0.9, 1.1, 0.95, 0.85], [0, 10, -8, 6, 0])),
    ('p6', _f1shape(100, 270, 6, '6: hexagon', [1, 0.85, 1.05, 0.9, 1.1, 0.95], [0, 8, -6, 0, 10, -5])),
    ('p7', _f1shape(320, 270, 7, '7: heptagon', [1, 0.9, 1.05, 0.85, 1.0, 1.1, 0.9], [0, 6, -5, 8, 0, -6, 4])),
    ('p8', _f1shape(540, 270, 8, '8: octagon', [1, 0.9, 1.08, 0.88, 1.0, 1.1, 0.92, 1.0], [0, 5, -4, 6, 0, -5, 4, 0])),
], vb='0 10 640 370', w=640, col=0, title='Polygons and their names'))
p104nm1 = I('p104nm1', 'The name = the number of sides', size=34, col=1)
p104nm2 = I('p104nm2', 'Not equal sides, not equal angles', size=34, col=1)

# ---- the angle sum: the rule, checked on the quadrilateral
_q4 = irr(170, 160, 120, 4, 100, [1, 0.85, 1.05, 0.9], [0, 5, -10, 8])
p104sum = PIN(GEO('p104sum', [
    ('line', [('poly', _q4, 'ink', 3)] + [pdot(q) for q in _q4]),
    ('ang', corners(_q4, 26, 'teal')),
    ('s', [('txt', 170, 330, '360°', 'teal', 30)]),
], vb='20 20 300 330', w=520, col=0, title='The angles of a quadrilateral'))
p104s0 = IH('p104s0', 'triangle: $180°$ · quadrilateral: $360°$', size=34, col=1)
p104s1 = I('p104s1', 'Sum of the angles $= 180° \\cdot (n-2)$', size=36, col=1)
p104s2 = I('p104s2', '$n$ = the number of sides', size=34, col=1)
p104s3 = IH('p104s3', '$n=4$:  $180° \\cdot (4-2)$', size=36, col=1)
p104s4 = IH('p104s4', '$= 180° \\cdot 2 = 360°$', size=36, col=1)

# ---- more sums: the pentagon and the hexagon
_p5 = irr(150, 150, 110, 5, 90, [1, 0.9, 1.05, 0.95, 0.9], [0, 6, -4, 5, 0])
_p6 = irr(420, 150, 110, 6, 90, [1, 0.88, 1.04, 0.92, 1.06, 0.95], [0, 6, -5, 0, 7, -4])
p104more = PIN(GEO('p104more', [
    ('line', [('poly', _p5, 'ink', 3)] + [pdot(q) for q in _p5]),
    ('a5', corners(_p5, 22, 'teal') + [('txt', 150, 300, '540°', 'teal', 30)]),
    ('h', [('poly', _p6, 'ink', 3)] + [pdot(q) for q in _p6]),
    ('a6', corners(_p6, 22, 'orange') + [('txt', 420, 300, '720°', 'orange', 30)]),
], vb='20 20 530 300', w=590, col=0, title='A pentagon and a hexagon'))
p104m1 = IH('p104m1', '$n=5$:  $180° \\cdot (5-2)$', size=36, col=1)
p104m2 = IH('p104m2', '$= 180° \\cdot 3 = 540°$', size=36, col=1)
p104m3 = IH('p104m3', '$n=6$:  $180° \\cdot (6-2)$', size=36, col=1)
p104m4 = IH('p104m4', '$= 180° \\cdot 4 = 720°$', size=36, col=1)

# ---- why: split into triangles from one corner (the pentagon, then the heptagon)
_P5 = irr(160, 165, 125, 5, 90, [1, 0.92, 1.03, 0.97, 0.9], [0, 4, -3, 3, 0])
_t5 = fan_tris(_P5, 0)
_TC = ['teal', 'orange', 'teal', 'orange', 'teal']
p104tri = PIN(GEO('p104tri', [
    ('line', [('poly', _P5, 'ink', 3)] + [pdot(q) for q in _P5]),
    ('k', [('circ', _P5[0][0], _P5[0][1], 12, 'red', 3)]),
    ('d', fan(_P5, 0)),
    ('t1', [('tint', _t5[0], 'teal'), ('txt', *cen(_t5[0]), '1', 'teal', 30)]),
    ('t2', [('tint', _t5[1], 'orange'), ('txt', *cen(_t5[1]), '2', 'orange', 30)]),
    ('t3', [('tint', _t5[2], 'teal'), ('txt', *cen(_t5[2]), '3', 'teal', 30)]),
], vb='20 20 290 300', w=520, col=0, title='A pentagon split into triangles'))
_P7 = irr(160, 165, 125, 7, 90, [1, 0.94, 1.02, 0.95, 1.0, 1.04, 0.93], [0, 3, -3, 4, 0, -3, 2])
_t7 = fan_tris(_P7, 0)
p104tri7 = PIN(GEO('p104tri7', [
    ('line', [('poly', _P7, 'ink', 3)] + [pdot(q) for q in _P7] + [('circ', _P7[0][0], _P7[0][1], 12, 'red', 3)] + fan(_P7, 0)),
    ('t', [x for k, t in enumerate(_t7) for x in (('tint', t, _TC[k]), ('txt',) + tuple(cen(t)) + (str(k + 1), _TC[k], 28))]),
    ('two', [sg(_P7[0], _P7[1], 'red', 6), sg(_P7[0], _P7[-1], 'red', 6)]),
], vb='20 20 290 300', w=520, col=0, title='A heptagon split into triangles'))
p104t1 = IH('p104t1', '$3 \\cdot 180° = 540°$', size=36, col=1)
p104t2 = IH('p104t2', '$5 \\cdot 180° = 900°$', size=36, col=1)
p104t3 = I('p104t3', '$n$ sides $\\rightarrow$ $n-2$ triangles', size=36, col=1)

# ---- +1 side = +180: a pentagon becomes a hexagon
_A5 = rp(160, 170, 120, 5, 90)
_X = gpt(160, 170, 175, 90 + 72 * 3 + 36)          # the new corner, outside the side _A5[3]-_A5[4]
p104plus = PIN(GEO('p104plus', [
    ('line', [('poly', _A5, 'ink', 3)] + [pdot(q) for q in _A5]),
    ('cut', [sg(_A5[3], _A5[4], 'red', 4, True)]),
    ('new', [sg(_A5[3], _X, 'teal', 4), sg(_X, _A5[4], 'teal', 4), pdot(_X)]),
    ('tri', [('tint', [_A5[3], _X, _A5[4]], 'teal'), ('txt', *cen([_A5[3], _X, _A5[4]]), '+180°', 'teal', 22)]),
], vb='20 30 340 330', w=520, col=0, title='One more side'))
p104p1 = I('p104p1', '1 more side $\\rightarrow$ $+180°$', size=36, col=1)
p104p2 = I('p104p2', '5 sides: $540°$', size=34, col=1)
p104p3 = I('p104p3', '6 sides: $720°$', size=34, col=1)
p104p4 = I('p104p4', '7 sides: $900°$', size=34, col=1)
p104p5 = I('p104p5', '8 sides: $1080°$', size=34, col=1)
p104c1 = IH('p104c1', '$12 - 9 = 3$ more sides', size=36, col=1)
p104c2 = IH('p104c2', '$3 \\cdot 180° = 540°$', size=36, col=1)

# ---- from the sum back to n
p104back = PIN(GEO('p104back', [
    ('line', [('poly', _P7, 'ink', 3)] + [pdot(q) for q in _P7] + fan(_P7, 0)
             + [x for k, t in enumerate(_t7) for x in (('tint', t, _TC[k]), ('txt',) + tuple(cen(t)) + (str(k + 1), _TC[k], 28))]),
    ('sides', [sg(_P7[k], _P7[(k + 1) % 7], 'orange', 6) for k in range(7)]),
], vb='20 20 290 300', w=520, col=0, title='Five triangles, seven sides'))
p104b1 = IH('p104b1', 'sum $= 900°$', size=36, col=1)
p104b2 = IH('p104b2', '$900° \\div 180° = 5$ triangles', size=36, col=1)
p104b3 = IH('p104b3', '$n = 5 + 2 = 7$ sides', size=36, col=1)

# ---- regular: the hexagon; the folded hexagon; the rectangle and the square
_H = rp(120, 150, 92, 6, 0)
# the folded hexagon: corners 4 and 5 of a hexagon, with corner 5 reflected inward across the line 4-0
def _refl(P, A, B):
    F = foot(P, A, B); return 2 * F[0] - P[0], 2 * F[1] - P[1]
_G = rp(370, 150, 92, 6, 0)
_G5 = _refl(_G[5], _G[4], _G[0])
_GF = [_G[0], _G[1], _G[2], _G[3], _G[4], _G5]
_rect = [(530, 100), (690, 100), (690, 200), (530, 200)]
_sq = [(560, 230), (650, 230), (650, 320), (560, 320)]
p104reg = PIN(GEO('p104reg', [
    ('line', [('poly', _H, 'ink', 3)] + [pdot(q) for q in _H]),
    ('tk', ticks(_H)),
    ('an', corners(_H, 20, 'orange') + [('txt', 120, 280, 'regular', 'teal', 26)]),
    ('fold', [('poly', _GF, 'ink', 3)] + [pdot(q) for q in _GF] + ticks(_GF) + [sg(_G[4], _G[5], 'ink', 2, True), sg(_G[5], _G[0], 'ink', 2, True)]),
    ('notreg', [('txt', 370, 280, 'not regular', 'red', 26)]),
    ('big', [angbig(_G5, _G[4], _G[0], 16, 'red'), ('txt', _G5[0] - 10, _G5[1] - 34, '> 180°', 'red', 20)]),
    ('rect', [('poly', _rect, 'ink', 3)] + [rt(_rect[k], _rect[k - 1], _rect[(k + 1) % 4], 12, 'orange') for k in range(4)]
             + [('txt', 610, 85, 'rectangle: not regular', 'red', 20)]),
    ('sq', [('poly', _sq, 'ink', 3)] + ticks(_sq) + [('txt', 605, 345, 'square: regular', 'teal', 20)]),
], vb='0 40 720 320', w=900, col=0, title='Regular and not regular'))

# ---- in a circle: around and inside; a polygon in a circle that is not regular
_C = (150, 175); _Rc = 120
_P5c = rp(_C[0], _C[1], _Rc, 5, 90)
_Q5 = [gpt(_C[0], _C[1], _Rc, d) for d in (90, 150, 200, 300, 340)]
_ri = _Rc * _pm.cos(_pm.radians(36))
p104circ = PIN(GEO('p104circ', [
    ('line', [('poly', _P5c, 'ink', 3)] + [pdot(q) for q in _P5c]),
    ('out', [('circ', _C[0], _C[1], _Rc, 'teal', 3), ('dot', _C[0], _C[1]), ('txt', _C[0] + 16, _C[1] + 18, 'O', 'ink', 24, True)]
            + [('circ', q[0], q[1], 8, 'teal', 3) for q in _P5c]),
    ('in', [('circ', _C[0], _C[1], _ri, 'orange', 2.5, True)]),
    ('q', [('circ', 450, _C[1], _Rc, 'teal', 3)] + [('poly', [(q[0] + 300, q[1]) for q in _Q5], 'ink', 3)]
          + [pdot((q[0] + 300, q[1])) for q in _Q5] + [('txt', 450, 330, 'in a circle, not regular', 'red', 22)]),
], vb='10 40 600 300', w=580, col=0, title='Regular polygons fit in a circle'))
p104c_1 = I('p104c_1', 'Regular $\\Rightarrow$ fits in a circle', size=34, col=1)
p104c_2 = I('p104c_2', 'Fits in a circle: not necessarily regular', size=32, col=1)

# ---- one angle: pentagon 108, hexagon 120, octagon 135
_r5 = rp(110, 150, 85, 5, 90); _r6 = rp(330, 150, 85, 6, 0); _r8 = rp(550, 150, 85, 8, 22.5)
p104one = PIN(GEO('p104one', [
    ('line', [('poly', _r5, 'ink', 3)] + corners(_r5, 16, 'teal')),
    ('v5', [ang(_r5[0], _r5[4], _r5[1], 24, 'teal'), ('txt', 110, 275, '108°', 'teal', 30)]),
    ('h', [('poly', _r6, 'ink', 3)] + corners(_r6, 16, 'orange')),
    ('v6', [('txt', 330, 275, '120°', 'orange', 30)]),
    ('o', [('poly', _r8, 'ink', 3)] + corners(_r8, 14, 'teal')),
    ('v8', [('txt', 550, 275, '135°', 'teal', 30)]),
], vb='10 50 640 250', w=580, col=0, title='One angle of a regular polygon'))
p104o1 = I('p104o1', 'One angle $= \\dfrac{180° \\cdot (n-2)}{n}$', size=36, col=1)
p104o2 = IH('p104o2', '$540° \\div 5 = 108°$', size=36, col=1)
p104o3 = IH('p104o3', '$720° \\div 6 = 120°$', size=36, col=1)
p104o4 = IH('p104o4', '$1080°\\div2=540°$', size=32, col=1)
p104o4b = IH('p104o4b', '$540°\\div2=270°$', size=32, col=1)
p104o4c = IH('p104o4c', '$270°\\div2=135°$', size=32, col=1)
p104o5 = I('p104o5', 'Only when the polygon is regular', size=32, col=1)

# ---- the formula sheet
p104fs1 = I('p104fs1', '$\\dfrac{180° \\cdot (n-2)}{n}$', size=36)
p104fs2 = I('p104fs2', '$= \\dfrac{180n - 360}{n}$', size=36)
p104fs3 = I('p104fs3', '$= \\dfrac{180n}{n} - \\dfrac{360}{n}$', size=36)
p104fs4 = I('p104fs4', '$= 180° - \\dfrac{360°}{n}$', size=36)
p104fs5 = IH('p104fs5', 'hexagon: $360° \\div 6 = 60°$', size=36, col=1)
p104fs6 = IH('p104fs6', '$180° - 60° = 120°$', size=36, col=1)

# ---- the central angle (the hexagon), the trick "complete to 180"
_O6 = (170, 170); _h6 = rp(_O6[0], _O6[1], 125, 6, 0)
p104cen = PIN(GEO('p104cen', [
    ('line', [('poly', _h6, 'ink', 3)] + [pdot(q) for q in _h6] + [('dot', *_O6), ('txt', _O6[0] - 4, _O6[1] + 24, 'O', 'ink', 24, True)]),
    ('r', [sg(_O6, q, 'teal', 3, True) for q in _h6]),
    ('c', [angw(_O6, _h6[0], _h6[1], 34, 'orange'), ang(_O6, _h6[0], _h6[1], 34, 'orange', '60°', 56)]),
    ('v', [ang(_h6[1], _h6[0], _h6[2], 24, 'teal'), at(_h6[1], '120°', 30, 56, 'teal', 24)]),
], vb='30 30 290 280', w=520, col=0, title='The central angle of a regular hexagon'))
p104ce1 = IH('p104ce1', 'hexagon: $360° \\div 6 = 60°$', size=34, col=1)
p104ce2 = IH('p104ce2', 'octagon: $360° \\div 8 = 45°$', size=34, col=1)
p104ce3 = IH('p104ce3', 'pentagon: $360° \\div 5 = 72°$', size=34, col=1)
p104ce4 = I('p104ce4', 'central angle $+$ angle $= 180°$', size=34, col=1)
p104ce5 = IH('p104ce5', '$60° + 120° = 180°$', size=34, col=1)
p104ce6 = IH('p104ce6', '$45° + 135° = 180°$', size=34, col=1)
p104ce7 = IH('p104ce7', '$72° + 108° = 180°$', size=34, col=1)

# ---- exterior angles
_E5 = irr(170, 175, 115, 5, 90, [1, 0.92, 1.05, 0.95, 0.9], [0, 6, -4, 5, 0])
def _ext(k, L=70):
    P, Q = _E5[k], _E5[(k + 1) % 5]                      # extend side k -> k+1 past Q
    d = gdir(P[0], P[1], Q[0], Q[1]); E = gpt(Q[0], Q[1], L, d)
    return E
_ex = [_ext(k) for k in range(5)]
p104ext = PIN(GEO('p104ext', [
    ('line', [('poly', _E5, 'ink', 3)] + [pdot(q) for q in _E5]),
    ('e1', [sg(_E5[1], _ex[0], 'teal', 3, True)]),
    ('a1', [angw(_E5[1], _ex[0], _E5[2], 30, 'orange'), ang(_E5[1], _ex[0], _E5[2], 30, 'orange')]),
    ('i1', [ang(_E5[1], _E5[0], _E5[2], 22, 'teal')]),
    ('all', [x for k in range(5) for x in (sg(_E5[(k + 1) % 5], _ex[k], 'teal', 3, True), angw(_E5[(k + 1) % 5], _ex[k], _E5[(k + 2) % 5], 30, 'orange'))]),
], vb='0 10 340 320', w=520, col=0, title='Exterior angles'))
p104x1 = I('p104x1', 'exterior angle $= 180° -$ angle', size=34, col=1)
p104x2 = I('p104x2', 'All the exterior angles: $360°$', size=34, col=1)
p104x3 = IH('p104x3', 'triangle: $180° - 60° = 120°$', size=34, col=1)
p104x4 = IH('p104x4', '$3 \\cdot 120° = 360°$', size=34, col=1)
p104x5 = IH('p104x5', 'square: $4 \\cdot 90° = 360°$', size=34, col=1)
p104x6 = I('p104x6', 'Regular: each one $= \\dfrac{360°}{n}$', size=34, col=1)

# ---- the diagonals split the angle equally (pentagon 3 x 36, hexagon 4 x 30)
_Od = (160, 175); _Rd = 125
_D5 = rp(_Od[0], _Od[1], _Rd, 5, 270)        # corner 0 at the bottom
p104dia = PIN(GEO('p104dia', [
    ('line', [('poly', _D5, 'ink', 3)] + [pdot(q) for q in _D5]),
    ('d', fan(_D5, 0, 'teal', 3, False)),
    ('three', [ang(_D5[0], _D5[1], _D5[2], 46, 'orange'), ang(_D5[0], _D5[2], _D5[3], 54, 'teal'), ang(_D5[0], _D5[3], _D5[4], 46, 'orange')]),
    ('circ', [('circ', _Od[0], _Od[1], _Rd, 'teal', 2.5, True)]),
    ('arcs', [('arcw', _Od[0], _Od[1], _Rd, 270 + 72 + 0.5, 270 + 144 - 0.5, 'orange', 8), ('arcw', _Od[0], _Od[1], _Rd, 270 + 144 + 0.5, 270 + 216 - 0.5, 'teal', 8),
              ('arcw', _Od[0], _Od[1], _Rd, 270 + 216 + 0.5, 270 + 288 - 0.5, 'orange', 8)]),
    ('v', [alab(_D5[0], _D5[1], _D5[2], 82, '36°', 'orange', 20), alab(_D5[0], _D5[2], _D5[3], 92, '36°', 'teal', 20), alab(_D5[0], _D5[3], _D5[4], 82, '36°', 'orange', 20)]),
], vb='20 30 290 300', w=480, col=0, title='The diagonals of a regular pentagon'))
_D6 = rp(450, 175, 120, 6, 270 - 30)
p104dia6 = PIN(GEO('p104dia6', [
    ('line', [('poly', _D6, 'ink', 3)] + [pdot(q) for q in _D6] + fan(_D6, 0, 'teal', 3, False)),
    ('four', [ang(_D6[0], _D6[k], _D6[k + 1], 44 + 6 * (k % 2), 'orange' if k % 2 else 'teal') for k in range(1, 5)]
             + [at(_D6[0], '30° each', 70, 30, 'teal', 22)]),
], vb='310 30 290 300', w=380, col=1, title='The diagonals of a regular hexagon'))
p104dg1 = IH('p104dg1', '$108° \\div 3 = 36°$', size=36, col=1)
p104dg2 = IH('p104dg2', '$120° \\div 4 = 30°$', size=36, col=1)

# ---- 2026-10-21 external-course fix: "count the sides" (an angle at a corner = the sides between its arms x 180 / n).
# Prerequisites: the diagonals split the angle (just above), the central angle 360 / n (part 3), the inscribed angle is
# half the central angle on the same arc (topic 33). Conditions said and shown: regular; the angle's corner is a corner;
# both arms go through corners. The pentagon (why + the whole-angle check), a regular decagon (a 2026_spring_q2_19-type
# angle between two diagonals, new numbers: 3 x 18 = 54, check 8 x 18 = 144) and a regular hexagon with crossing
# diagonals (a 2023_spring_q2_03-type angle at a crossing, new shape: 30 + 30 -> 120 = the hexagon's angle; the pentagon
# 108 as the second run).
_Ok = (160, 175); _Rk = 125
_K5 = rp(_Ok[0], _Ok[1], _Rk, 5, 270)        # corner 0 at the bottom
p104cnt = PIN(GEO('p104cnt', [
    ('line', [('poly', _K5, 'ink', 3)] + [pdot(q) for q in _K5] + fan(_K5, 0, 'teal', 3, False)
             + [('circ', _Ok[0], _Ok[1], _Rk, 'teal', 2.5, True)]),
    ('one', [ang(_K5[0], _K5[2], _K5[3], 60, 'teal'), ('arcw', _Ok[0], _Ok[1], _Rk, 270 + 144 + 1, 270 + 216 - 1, 'teal', 8),
             alab(_K5[0], _K5[2], _K5[3], 84, '36°', 'teal', 22)]),
    ('cen', [('dot', *_Ok), sg(_Ok, _K5[2], 'orange', 3, True), sg(_Ok, _K5[3], 'orange', 3, True),
             angw(_Ok, _K5[2], _K5[3], 30, 'orange'), ('txt', _Ok[0] + 22, _Ok[1] + 14, 'O', 'ink', 22, True)]),
    ('c72', [('txt', _Ok[0], _Ok[1] - 48, '72°', 'orange', 22)]),
    ('whole', [ang(_K5[0], _K5[4], _K5[1], 28, 'orange')]
              + [sg(_K5[k], _K5[k + 1], 'teal', 7) for k in (1, 2, 3)]
              + [side_lab(_K5[k], _K5[k + 1], str(k), _Ok, 20, 'teal', 24) for k in (1, 2, 3)]),
    ('w108', [('txt', _K5[0][0], _K5[0][1] + 30, '108°', 'orange', 24)]),
], vb='20 30 290 320', w=480, col=0, title='One side adds 180 over n'))
p104k1 = IH('p104k1', 'pentagon: $180° \\div 5 = 36°$', size=30, col=1)
p104k2 = IH('p104k2', 'hexagon: $180° \\div 6 = 30°$', size=30, col=1)
p104k3 = I('p104k3', 'central angle of one side $= \\dfrac{360°}{n}$', size=30, col=1)
p104k3b = I('p104k3b', 'inscribed angle $=$ half $= \\dfrac{180°}{n}$', size=30, col=1)
p104k4 = I('p104k4', 'each side between the arms: $\\dfrac{180°}{n}$', size=30, col=1)
p104k5 = IH('p104k5', '$3 \\cdot 36° = 108°$', size=30, col=1)
p104k6 = I('p104k6', 'Only: regular, corner on a corner, arms through corners', size=26, col=1)

# a regular decagon A ... J, A at the bottom; the diagonals A D and A G; alpha = 3 sides
_Oe = (200, 190); _Re = 140
_E10 = rp(_Oe[0], _Oe[1], _Re, 10, 270)
_EN = 'ABCDEFGHIJ'
p104dec = PIN(GEO('p104dec', [
    ('line', [('poly', _E10, 'ink', 3)] + [pdot(q) for q in _E10] + [nm(_E10[k], _EN[k], _Oe, 22, 'ink', 24) for k in range(10)]
             + [sg(_E10[0], _E10[3], 'ink', 3), sg(_E10[0], _E10[6], 'ink', 3), ang(_E10[0], _E10[3], _E10[6], 46, 'teal'),
                alab(_E10[0], _E10[3], _E10[6], 66, 'α', 'teal', 24)]),
    ('sides', [sg(_E10[k], _E10[k + 1], 'teal', 7) for k in (3, 4, 5)]
              + [side_lab(_E10[k], _E10[k + 1], str(k - 2), _Oe, 18, 'teal', 22) for k in (3, 4, 5)]),
    ('val', [alab(_E10[0], _E10[3], _E10[6], 100, '54°', 'teal', 24)]),
    ('whole', [ang(_E10[0], _E10[9], _E10[1], 24, 'orange')] + [sg(_E10[k], _E10[k + 1], 'orange', 4) for k in range(1, 9)]),
    ('w144', [('txt', _E10[0][0], _E10[0][1] + 52, '144°', 'orange', 24)]),
], vb='40 0 320 400', w=500, col=0, title='A regular polygon with ten sides'))
p104e1 = IH('p104e1', 'one side: $180° \\div 10 = 18°$', size=34, col=1)
p104e2 = IH('p104e2', '$3 \\cdot 18° = 54°$', size=34, col=1)
p104e3 = IH('p104e3', 'whole angle: $8 \\cdot 18° = 144°$', size=34, col=1)
p104e3b = IH('p104e3b', '$360° \\div 10=36°$', size=34, col=1)
p104e4 = IH('p104e4', '$180° - 36° = 144°$', size=34, col=1)

# a regular hexagon A ... F with B C at the bottom; the diagonals A C and B D cross at P
_Oc6 = (200, 190); _Rc6 = 160
_C6 = rp(_Oc6[0], _Oc6[1], _Rc6, 6, 180)      # A left, B bottom left, C bottom right, D right, E, F
_CP = (_Oc6[0], _C6[0][1] + (_C6[2][1] - _C6[0][1]) * 2.0 / 3.0)
p104hxc = PIN(GEO('p104hxc', [
    ('line', [('poly', _C6, 'ink', 3)] + [pdot(q) for q in _C6] + [nm(_C6[k], 'ABCDEF'[k], _Oc6, 24, 'ink', 26) for k in range(6)]
             + [sg(_C6[0], _C6[2], 'ink', 3), sg(_C6[1], _C6[3], 'ink', 3), pdot(_CP), ('txt', _CP[0], _CP[1] - 24, 'P', 'ink', 24, True)]),
    ('tri', [('tint', [_C6[1], _CP, _C6[2]], 'teal')]),
    ('b', [ang(_C6[1], _C6[2], _C6[3], 30, 'teal'), sg(_C6[2], _C6[3], 'teal', 7)]),
    ('b30', [alab(_C6[1], _C6[2], _C6[3], 54, '30°', 'teal', 18)]),
    ('c', [ang(_C6[2], _C6[1], _C6[0], 30, 'orange'), sg(_C6[0], _C6[1], 'orange', 7)]),
    ('c30', [alab(_C6[2], _C6[1], _C6[0], 54, '30°', 'orange', 18)]),
    ('p', [ang(_CP, _C6[1], _C6[2], 16, 'ink')]),
], vb='10 20 380 340', w=520, col=0, title='Two diagonals of a regular hexagon cross'))
# The same highlighted triangle, enlarged without changing its orientation or point names.
_cutB, _cutP, _cutC = (40, 185), (200, 185 - 160 / (3 ** .5)), (360, 185)
p104cut = PIN(GEO('p104cut', [
    ('line', [('poly', [_cutB, _cutP, _cutC], 'teal', 3), ('tint', [_cutB, _cutP, _cutC], 'teal'),
              ('txt', 26, 215, 'B', 'ink', 24, True), ('txt', 200, 70, 'P', 'ink', 24, True),
              ('txt', 374, 215, 'C', 'ink', 24, True)]),
    ('b30', [ang(_cutB, _cutC, _cutP, 32, 'teal'), alab(_cutB, _cutC, _cutP, 58, '30°', 'teal', 24)]),
    ('c30', [ang(_cutC, _cutB, _cutP, 32, 'orange'), alab(_cutC, _cutB, _cutP, 58, '30°', 'orange', 24)]),
    ('p120', [ang(_cutP, _cutB, _cutC, 28, 'ink'), ('txt', 200, 140, '120°', 'ink', 24)]),
], vb='0 45 400 190', w=520, col=0, title='Triangle BPC enlarged, same orientation'))
LEFT(p104cut, y=570, x=410, w=520)
p104h1 = IH('p104h1', 'one side: $180° \\div 6 = 30°$', size=34, col=1)
p104h2 = IH('p104h2', '$\\angle PBC = 30°$', size=34, col=1)
p104h3 = IH('p104h3', '$\\angle PCB = 30°$', size=34, col=1)
p104h4 = IH('p104h4', '$\\angle BPC = 180° - 30° - 30° = 120°$', size=32, col=1)
p104h5 = IH('p104h5', 'pentagon: $180° - 36° - 36° = 108°$', size=32, col=1)
p104h6 = I('p104h6', 'AC and BD: angle BPC equals the polygon\'s angle', size=28, col=1)

# ---- radii: n isosceles triangles (the pentagon 72 / 54 / 54); the hexagon: six equilateral triangles
_Or = (170, 170); _R5 = rp(_Or[0], _Or[1], 130, 5, 90)
p104rad = PIN(GEO('p104rad', [
    ('line', [('poly', _R5, 'ink', 3)] + [pdot(q) for q in _R5] + [('dot', *_Or), ('txt', _Or[0] - 22, _Or[1] + 4, 'O', 'ink', 24, True)]),
    ('r', [sg(_Or, q, 'teal', 3, True) for q in _R5]),
    ('t', [('tint', [_Or, _R5[3], _R5[4]], 'teal'), tk(_Or, _R5[3]), tk(_Or, _R5[4])]),
    ('c', [ang(_Or, _R5[3], _R5[4], 26, 'orange', '72°', 46)]),
    ('b', [ang(_R5[3], _Or, _R5[4], 26, 'teal'), ang(_R5[4], _R5[3], _Or, 26, 'teal'),
           alab(_R5[3], _Or, _R5[4], 46, '54°'), alab(_R5[4], _R5[3], _Or, 46, '54°')]),
    ('h', [('tint', [_Or, _R5[4], _R5[0]], 'orange'), ang(_R5[4], _Or, _R5[0], 34, 'orange'), alab(_R5[4], _Or, _R5[0], 50, '54°', 'orange')]),
], vb='20 20 300 300', w=520, col=0, title='The radii of a regular pentagon'))
p104r1 = IH('p104r1', '$360° \\div 5 = 72°$', size=36, col=1)
p104r2 = IH('p104r2', '$180° - 72° = 108°$', size=36, col=1)
p104r3 = IH('p104r3', '$108° \\div 2 = 54°$', size=36, col=1)
p104r4 = IH('p104r4', '$54° + 54° = 108°$', size=36, col=1)

_Oh = (170, 170); _Hh = rp(_Oh[0], _Oh[1], 130, 6, 0)
p104hex = PIN(GEO('p104hex', [
    ('line', [('poly', _Hh, 'ink', 3)] + [pdot(q) for q in _Hh] + [('dot', *_Oh)] + [sg(_Oh, q, 'teal', 3, True) for q in _Hh]),
    ('t', [('tint', [_Oh, _Hh[0], _Hh[1]], 'teal'), ang(_Oh, _Hh[0], _Hh[1], 26, 'orange', '60°', 46),
           ang(_Hh[0], _Oh, _Hh[1], 22, 'teal', '60°', 44), ang(_Hh[1], _Hh[0], _Oh, 22, 'teal', '60°', 44)]),
    ('all', [('tint', [_Oh, _Hh[k], _Hh[(k + 1) % 6]], 'teal' if k % 2 else 'orange') for k in range(1, 6)]),
    ('rs', [side_lab(_Hh[0], _Hh[1], '5', _Oh, 18, 'ink', 24), ('txt', *mid(_Oh, _Hh[0], 14, 1), '5', 'teal', 24)]),
], vb='20 20 300 300', w=520, col=0, title='A regular hexagon: six equilateral triangles'))
p104hx1 = IH('p104hx1', '$360° \\div 6 = 60°$', size=36, col=1)
p104hx2 = IH('p104hx2', '$(180° - 60°) \\div 2 = 60°$', size=36, col=1)
p104hx3 = I('p104hx3', 'radius $=$ side', size=36, col=1)

# ---- summary
p104z1 = I('p104z1', 'Sum $= 180°(n-2)$ $\\cdot$ $n-2$ triangles $\\cdot$ $+180°$ a side', size=34)
p104z2 = I('p104z2', 'Regular: one angle $=$ sum $\\div n$: $108°, 120°, 135°$', size=34)
p104z3 = I('p104z3', 'Central angle $=$ exterior angle $= 360° \\div n$', size=34)
p104z4 = I('p104z4', 'Angle at a corner $=$ sides between the arms $\\cdot \\dfrac{180°}{n}$', size=34)
p104z5 = I('p104z5', 'Radii: $n$ isosceles triangles $\\cdot$ hexagon: 6 equilateral', size=34)


video('geo-104', 'lesson', slides=[
    S('Polygons',
      L("Welcome back. Today we're learning about polygons. A polygon question shows up in most exams. Most of these "
        "questions use the same few rules, and we'll learn all of them today.")),
    # ------------------------------------------------------------------ part 1: names, the angle sum
    S('What is a polygon?',
      L("A polygon is a closed shape with straight sides. It has three sides or more. We already know two polygons. A "
        "triangle is a polygon with three sides. A quadrilateral is a polygon with four sides.",
        show(p104names['line'], 'A triangle is a polygon'), show(p104names['q'], 'A quadrilateral is a polygon')),
      L("Five sides is a pentagon. Six sides is a hexagon. Seven sides is a heptagon. And eight sides is an octagon.",
        show(p104names['p5'], 'Five sides is a pentagon'), show(p104names['p6'], 'Six sides is a hexagon'),
        show(p104names['p7'], 'Seven sides is a heptagon'), show(p104names['p8'], 'eight sides is an octagon')),
      L("Look at these shapes. Their sides are not equal, and their angles are not equal. They're still a pentagon, a "
        "hexagon, a heptagon and an octagon. The name only tells us how many sides there are.",
        show(p104nm2, 'Their sides are not equal'), show(p104nm1, 'The name only tells us'))),
    S('The angle sum',
      L("Now the angles. In a triangle, the angles add up to one hundred eighty. In a quadrilateral, they add up to "
        "three hundred sixty. So the sum of the angles depends on the number of sides. The more sides, the bigger the sum.",
        show(p104s0, 'In a triangle'), show(p104sum['line'], 'In a quadrilateral'), show(p104sum['ang'], 'they add up to'),
        show(p104sum['s'], 'three hundred sixty. So')),
      L("Here's the rule. The sum of the angles is one hundred eighty, times the bracket, n minus two. n is the number of sides.",
        show(p104s1, "Here's the rule"), show(p104s2, 'n is the number of sides')),
      L("Let's check it on a quadrilateral first, because we know its sum. n is four. Four minus two is two. Two times "
        "one hundred eighty is three hundred sixty. That's exactly the sum we know.",
        show(p104s3, 'n is four'), show(p104s4, 'Two times one hundred eighty'))),
    S('More sums',
      L("Now a pentagon. n is five. Five minus two is three. Three times one hundred eighty is five hundred forty. So the "
        "five angles of any pentagon add up to five hundred forty.",
        show(p104more['line'], 'Now a pentagon'), show(p104m1, 'Five minus two is three'),
        show(p104m2, 'Three times one hundred eighty'), show(p104more['a5'], 'the five angles of any pentagon')),
      L("And a hexagon. n is six. Six minus two is four. Four times one hundred eighty is seven hundred twenty.",
        show(p104more['h'], 'And a hexagon'), show(p104m3, 'Six minus two is four'),
        show(p104m4, 'Four times one hundred eighty'), show(p104more['a6'], 'seven hundred twenty'))),
    S('Why: triangles',
      L("Where does this rule come from? Let's take a pentagon and pick one corner. From that corner, we draw lines to "
        "the other corners. A line that joins two corners that are not next to each other is called a diagonal.",
        show(p104tri['line'], "Let's take a pentagon"), show(p104tri['k'], 'pick one corner'),
        show(p104tri['d'], 'we draw lines to')),
      L("The diagonals cut the pentagon into triangles. One, two, three triangles. Each triangle has one hundred eighty "
        "degrees inside it. So the pentagon has three times one hundred eighty, which is five hundred forty. That's the "
        "same as the rule.",
        show(p104tri['t1'], 'One, two'), show(p104tri['t2'], 'two, three'), show(p104tri['t3'], 'three triangles'),
        show(p104t1, 'three times one hundred eighty'))),
    S('Seven sides',
      L("Now a heptagon, with seven sides. From one corner we get one, two, three, four, five triangles. Five times one "
        "hundred is five hundred, and five times eighty is four hundred. Together, nine hundred. So the angles of a "
        "heptagon add up to nine hundred.",
        show(p104tri7['line'], 'Now a heptagon'), show(p104tri7['t'], 'one, two, three, four, five'),
        show(p104t2, 'Together, nine hundred')),
      L("Why n minus two? Every triangle sits on one side of the polygon. But the two sides that touch our corner don't "
        "get a triangle of their own. So n sides give n minus two triangles.",
        show(p104tri7['two'], 'the two sides that touch our corner'), show(p104t3, 'So n sides give')),
      L("So if you forget the rule in the exam, that's fine. Split the polygon into triangles from one corner, and count them.")),
    S('Every side adds 180',
      L("Now let's see what happens when we add a side. Here's a pentagon. I erase this side, and I draw two new sides "
        "instead. Now there are six sides.",
        show(p104plus['line'], "Here's a pentagon"), show(p104plus['cut'], 'I erase this side'),
        show(p104plus['new'], 'I draw two new sides')),
      L("What really changed? We added one more triangle. One more triangle is one more one hundred eighty. So every "
        "extra side adds one hundred eighty to the sum.",
        show(p104plus['tri'], 'We added one more triangle'), show(p104p1, 'So every extra side')),
      L("So the sums go up in steps of one hundred eighty. A pentagon, five hundred forty. A hexagon, seven hundred "
        "twenty. A heptagon, nine hundred. And an octagon, one thousand eighty.",
        show(p104p2, 'A pentagon, five hundred forty'), show(p104p3, 'A hexagon, seven hundred'),
        show(p104p4, 'A heptagon, nine hundred'), show(p104p5, 'an octagon, one thousand eighty')),
      L("This helps a lot when a question compares two polygons. Say one polygon has twelve sides, and another has nine. "
        "What's the difference between their angle sums? The first one has three more sides. Each side adds one hundred "
        "eighty. So the difference is three times one hundred eighty, which is five hundred forty.",
        show(p104c1, 'The first one has three more sides'), show(p104c2, 'So the difference is'))),
    S('From the sum to the sides',
      L("Sometimes we know the sum, and we need the number of sides. Say the angles add up to nine hundred. How many "
        "sides are there?", show(p104b1, 'Say the angles add up to nine hundred')),
      L("Every triangle is one hundred eighty. Nine hundred divided by one hundred eighty is five, because five times one "
        "hundred eighty is nine hundred. So there are five triangles.",
        show(p104back['line'], 'Every triangle is one hundred eighty'), show(p104b2, 'Nine hundred divided by')),
      L("Careful here. Five is the number of triangles, not the number of sides. There are always two more sides than "
        "triangles. So there are five plus two, seven sides. It's a heptagon, like before.",
        show(p104back['sides'], 'not the number of sides'), show(p104b3, 'So there are five plus two'))),
    # ------------------------------------------------------------------ part 2: regular, in a circle, one angle
    S('Regular polygons',
      L("Now a very important word, regular. A regular polygon has all its sides equal, and all its angles equal. Both "
        "things together.", show(p104reg['line'], 'A regular polygon')),
      L("Here's a regular hexagon. It has six sides, all equal. And it has six angles, all equal. So it looks the same "
        "from every direction.", show(p104reg['tk'], 'six sides, all equal'), show(p104reg['an'], 'six angles, all equal')),
      L("Why do we need both? Look at this. I take two sides of the hexagon and fold them inward. All six sides are still "
        "equal. But the angles are not equal any more. So this is not a regular hexagon.",
        show(p104reg['fold'], 'fold them inward'), show(p104reg['notreg'], 'the angles are not equal any more')),
      L("It still has six sides, so it's still a hexagon. Its angles still add up to seven hundred twenty. One angle now "
        "points inward, and it's bigger than one hundred eighty.", show(p104reg['big'], "it's bigger than one hundred eighty")),
      L("And the other way around. This rectangle has four equal angles, but its sides are not all equal. So this rectangle is "
        "not regular. The regular quadrilateral is the square. And the regular triangle is the equilateral triangle.",
        show(p104reg['rect'], 'This rectangle has four equal angles'), show(p104reg['sq'], 'The regular quadrilateral is the square'))),
    S('In a circle',
      L("Every regular polygon fits in a circle. We can draw a circle around it, so all its corners are on the circle. "
        "The center of that circle, O, is also the center of the polygon.",
        show(p104circ['line'], 'Every regular polygon'), show(p104circ['out'], 'We can draw a circle around it'),
        show(p104c_1, 'all its corners are on the circle')),
      L("We can also draw a circle inside it, touching every side. It has the same center, O. But in questions we "
        "mostly use the circle around it.", show(p104circ['in'], 'a circle inside it')),
      L("But careful, this works only one way. If a polygon fits in a circle, it's not necessarily regular. Here all the "
        "corners are on the circle, but the sides are clearly not equal. So it's not regular.",
        show(p104circ['q'], 'Here all the corners are on the circle'), show(p104c_2, "it's not necessarily regular"))),
    S('One angle',
      L("Now let's find one angle of a regular polygon. We already know how to find the sum of the angles. In a regular "
        "polygon all the angles are equal. So we just divide the sum by the number of angles. And n sides means n angles.",
        show(p104o1, 'we just divide the sum')),
      L("A regular pentagon. The sum is five hundred forty. Five hundred divided by five is one hundred, and forty "
        "divided by five is eight. So one angle is one hundred eight.",
        show(p104one['line'], 'A regular pentagon'), show(p104o2, 'Five hundred divided by five'),
        show(p104one['v5'], 'So one angle is one hundred eight')),
      L("A regular hexagon. The sum is seven hundred twenty, divided by six. Six times one hundred twenty is seven hundred "
        "twenty. So one angle is one hundred twenty.",
        show(p104one['h'], 'A regular hexagon'), show(p104o3, 'divided by six'), show(p104one['v6'], 'So one angle is one hundred twenty')),
      L("A regular octagon. The sum is one thousand eighty, divided by eight. Let's halve it three times, because "
        "eight is two times two times two. Half is five hundred forty. Half again is two hundred seventy. And half again "
        "is one hundred thirty-five.",
        show(p104one['o'], 'A regular octagon'), show(p104o4, 'Half is five hundred forty'),
        show(p104o4b, 'Half again is two hundred seventy'), show(p104o4c, 'And half again is one hundred thirty-five'),
        show(p104one['v8'], 'And half again is one hundred thirty-five')),
      L("Remember these three angles, one hundred eight, one hundred twenty and one hundred thirty-five. The exam uses "
        "them all the time. And we divide only when the polygon is regular. If it's not regular, the angles are not equal.",
        show(p104o5, 'we divide only when the polygon is regular'))),
    # ------------------------------------------------------------------ part 3: the formula sheet, central, exterior
    S('The formula sheet',
      L("On the exam's formula sheet, this rule looks a bit different. Let's see that it's the same rule. We start "
        "from one hundred eighty times the bracket, n minus two, over n.", show(p104fs1, 'We start')),
      L("Let's open the brackets. One hundred eighty times n, minus one hundred eighty times two. That's one hundred "
        "eighty n minus three hundred sixty, all over n.", show(p104fs2, "That's one hundred eighty n minus")),
      L("Now let's split it into two fractions. One hundred eighty n over n is just one hundred eighty, because the n "
        "cancels. So we get one hundred eighty, minus three hundred sixty over n.",
        show(p104fs3, 'split it into two fractions'), show(p104fs4, 'So we get one hundred eighty')),
      L("Let's check it on the hexagon. Three hundred sixty divided by six is sixty. One hundred eighty minus sixty is "
        "one hundred twenty. That's the same as before. Use the form you remember better.",
        show(p104fs5, 'Three hundred sixty divided by six'), show(p104fs6, 'One hundred eighty minus sixty'))),
    S('The central angle',
      L("Now let's draw a line from O to every corner of a regular hexagon. These are radii. They make six angles at the "
        "center. They're called central angles, and they're all equal.",
        show(p104cen['line'], 'every corner of a regular hexagon'), show(p104cen['r'], 'These are radii')),
      L("Together they make a full turn, three hundred sixty. So each one is three hundred sixty divided by six, which is "
        "sixty.", show(p104cen['c'], 'Together they make a full turn'), show(p104ce1, 'divided by six')),
      L("In an octagon, three hundred sixty divided by eight is forty-five. In a pentagon, three hundred sixty divided by "
        "five is seventy-two.", show(p104ce2, 'divided by eight'), show(p104ce3, 'divided by five')),
      L("Now here's a useful trick. The central angle and the polygon's angle always add up to one hundred eighty. In "
        "the hexagon, sixty plus one hundred twenty is one hundred eighty. In the octagon, forty-five plus one hundred "
        "thirty-five. In the pentagon, seventy-two plus one hundred eight.",
        show(p104ce4, 'always add up to one hundred eighty'), show(p104cen['v'], 'In the hexagon'),
        show(p104ce5, 'sixty plus one hundred twenty'), show(p104ce6, 'forty-five plus'), show(p104ce7, 'seventy-two plus')),
      L("So if you forget the angle of the octagon, find its central angle first. Three hundred sixty divided by eight is "
        "forty-five. Then complete it to one hundred eighty. One hundred eighty minus forty-five is one hundred "
        "thirty-five.", pt('p104ce6', 'complete it to one hundred eighty'))),
    S('Exterior angles',
      L("Why does this trick work? Let's meet the exterior angle. Take a polygon, and extend one side past its corner. The "
        "angle between this extension and the next side is called the exterior angle.",
        show(p104ext['line'], 'Take a polygon'), show(p104ext['e1'], 'extend one side past its corner'),
        show(p104ext['a1'], 'The angle between this extension')),
      L("The polygon's angle and the exterior angle sit together on one straight line. So together they make one hundred "
        "eighty. The exterior angle is one hundred eighty minus the polygon's angle.",
        show(p104ext['i1'], "The polygon's angle and the exterior angle"), show(p104x1, 'The exterior angle is')),
      L("Now the big fact. Take one exterior angle at every corner, and add them up. You always get three hundred sixty. "
        "Why? Walk around the polygon along its sides. At every corner, you turn by the exterior angle. After one full "
        "walk you face the same way again. So you turned one full turn, three hundred sixty.",
        show(p104ext['all'], 'Take one exterior angle at every corner'), show(p104x2, 'You always get three hundred sixty')),
      L("Let's check it in numbers. An equilateral triangle has angles of sixty. So each exterior angle is one hundred "
        "eighty minus sixty, one hundred twenty. And three times one hundred twenty is three hundred sixty. A square has "
        "angles of ninety, so each exterior angle is ninety too. Four times ninety is three hundred sixty again.",
        show(p104x3, 'one hundred eighty minus sixty'), show(p104x4, 'three times one hundred twenty'),
        show(p104x5, 'Four times ninety')),
      L("In a regular polygon, all the exterior angles are equal. So each one is three hundred sixty divided by n. That's "
        "exactly the central angle. And that's why the central angle and the polygon's angle add up to one hundred eighty.",
        show(p104x6, 'So each one is three hundred sixty divided by n'))),
    # ------------------------------------------------------------------ part 4: diagonals, radii, the hexagon
    S('The diagonals',
      L("Now the diagonals of a regular polygon. Here's a regular pentagon. Let's take one corner and draw both "
        "diagonals from it. From one corner of a pentagon, that's all we can draw.",
        show(p104dia['line'], "Here's a regular pentagon"), show(p104dia['d'], 'draw both diagonals')),
      L("The diagonals cut the corner's angle into three angles. And these three angles are equal. Why? Remember, "
        "every regular polygon fits in a circle. So each small angle has its corner on the circle. It's an inscribed angle.",
        show(p104dia['three'], 'into three angles'), show(p104dia['circ'], 'every regular polygon fits in a circle')),
      L("Each small angle intercepts the arc under one side of the pentagon. All the sides are equal, so these arcs are "
        "equal too. And inscribed angles on equal arcs are equal. So the three angles are equal.",
        show(p104dia['arcs'], 'the arc under one side')),
      L("The whole angle is one hundred eight, so each one is one hundred eight divided by three. Ninety divided by three "
        "is thirty, and eighteen divided by three is six. So each angle is thirty-six.",
        show(p104dg1, 'one hundred eight divided by three'), show(p104dia['v'], 'So each angle is thirty-six')),
      L("It's the same in a regular hexagon. From one corner we can draw three diagonals. They cut the angle of one "
        "hundred twenty into four equal angles. One hundred twenty divided by four is thirty.",
        show(p104dia6['line'], 'the same in a regular hexagon'), show(p104dia6['four'], 'into four equal angles'),
        show(p104dg2, 'One hundred twenty divided by four'))),
    S('Count the sides',
      L("Let's look at those small angles again. In the regular pentagon, each one was thirty-six. In the regular hexagon, "
        "each one was thirty. And there's a pattern here. Thirty-six is one hundred eighty divided by five. And thirty is "
        "one hundred eighty divided by six.",
        show(p104cnt['line'], 'In the regular pentagon'), show(p104cnt['one'], 'each one was thirty-six'),
        show(p104k1, 'Thirty-six is one hundred eighty divided by five'), show(p104k2, 'thirty is one hundred eighty divided by six')),
      L("Why one hundred eighty divided by n? Because each small angle is an inscribed angle, and it intercepts the arc "
        "under one side. The central angle on that same arc is three hundred sixty divided by n. In the pentagon, that's "
        "seventy-two. And an inscribed angle is half of the central angle on the same arc. So each small angle is half of "
        "three hundred sixty over n. That's one hundred eighty over n, and in the pentagon, half of seventy-two is thirty-six.",
        show(p104cnt['cen'], 'The central angle on that same arc'), show(p104k3, 'is three hundred sixty divided by n'),
        show(p104cnt['c72'], "In the pentagon, that's seventy-two"), show(p104k3b, "That's one hundred eighty over n")),
      L("Use this rule in a regular polygon. The angle's corner must be on the polygon. Both arms must pass through "
        "other corners. Count the sides along the arc between those corners. Use the arc that doesn't pass through "
        "the angle's corner. Each counted side gives one hundred eighty over n. So multiply that by the number of "
        "sides you counted.", show(p104k4, 'Each counted side gives')),
      L("Let's check it on the whole angle of the pentagon. Its arms are the two sides at the corner. Between them, on the "
        "far side, there are three sides. Three times thirty-six is one hundred eight. That's exactly the pentagon's angle, "
        "like we found before.",
        show(p104cnt['whole'], 'Between them, on the far side'), show(p104k5, 'Three times thirty-six'),
        show(p104cnt['w108'], "That's exactly the pentagon's angle")),
      L("Use this rule for a regular polygon. Its equal sides give equal arcs on the circle. "
        "And the angle's corner must be a corner of the polygon, and both arms must go through corners too. Only then is "
        "it an inscribed angle on those arcs.",
        show(p104k6, 'Use this rule for a regular polygon'))),
    S('Ten sides',
      L("Let's use it. Here's a regular polygon with ten sides, A to J. From corner A, we draw two diagonals, to D and to "
        "G. What is the angle alpha between them?",
        show(p104dec['line'], "Here's a regular polygon with ten sides")),
      L("First, what one side adds. One hundred eighty divided by ten is eighteen. So every side between the arms adds "
        "eighteen degrees.", show(p104e1, 'One hundred eighty divided by ten')),
      L("Now we count the sides between the arms, from D to G. They are D E, E F and F G. That's three sides. So alpha is three "
        "times eighteen, which is fifty-four.",
        show(p104dec['sides'], 'D E, E F and F G'), show(p104e2, 'So alpha is three'), show(p104dec['val'], 'which is fifty-four')),
      L("Let's check the rule on the whole angle at A. Its arms are the sides A B and A J. From B to J there are eight "
        "sides. Eight times eighteen is one hundred forty-four. Let's also check it with the formula sheet. Three hundred "
        "sixty divided by ten is thirty-six. One hundred eighty minus thirty-six is one hundred forty-four. That's the same angle.",
        show(p104dec['whole'], 'From B to J there are eight'), show(p104e3, 'Eight times eighteen'),
        show(p104dec['w144'], "is one hundred forty-four. Let's"), show(p104e3b, 'Three hundred sixty divided by ten'),
        show(p104e4, 'eighty minus thirty-six is one hundred forty-four'))),
    S('Crossing diagonals',
      L("Now an angle where two diagonals cross. A B C D E F is a regular hexagon. The diagonals A C and B D cross at the "
        "point P. What is angle B P C?", show(p104hxc['line'], 'A B C D E F is a regular hexagon')),
      L("P isn't a corner of the hexagon, so we can't count sides at P. But look at triangle B P C. Its other two angles "
        "are at B and at C, and those are corners. Here's the same triangle enlarged below. "
        "We'll find its two base angles first. Then subtract their sum from one hundred eighty to find angle B P C.",
        show(p104hxc['tri'], 'look at triangle B P C'), show(p104cut['line'], "Here's the same triangle enlarged below")),
      L("In a hexagon, one side adds one hundred eighty divided by six, thirty. The angle at B is between B C and B D. Its "
        "arms go through C and D, and between them there's one side, C D. So angle P B C is thirty.",
        show(p104h1, 'one hundred eighty divided by six'), show(p104hxc['b'], 'The angle at B is between'),
        show(p104h2, 'So angle P B C is thirty'), show(p104hxc['b30'], 'So angle P B C is thirty'),
        show(p104cut['b30'], 'So angle P B C is thirty')),
      L("The angle at C is between C B and C A. Its arms go through B and A, and between them there's one side, A B. So "
        "angle P C B is thirty too.",
        show(p104hxc['c'], 'The angle at C is between'), show(p104h3, 'So angle P C B is thirty too'),
        show(p104hxc['c30'], 'So angle P C B is thirty too'), show(p104cut['c30'], 'So angle P C B is thirty too')),
      L("The angles of triangle B P C add up to one hundred eighty. So angle B P C is one hundred eighty minus thirty "
        "minus thirty. That's one hundred twenty.",
        show(p104h4, 'one hundred eighty minus thirty'), show(p104hxc['p'], "That's one hundred twenty"),
        show(p104cut['p120'], "That's one hundred twenty")),
      L("One hundred twenty is exactly the hexagon's angle. In a regular pentagon, the same two diagonals cross at one "
        "hundred eighty minus thirty-six minus thirty-six. That's one hundred eight, the pentagon's angle. So "
        "when two diagonals start at two neighboring corners, and each one skips just one corner, look at the angle "
        "facing the side between the two middle corners. Here that's angle B P C, facing B C. "
        "That angle equals the polygon's interior angle, not the angle next to it.",
        show(p104h5, 'hundred eighty minus thirty-six minus thirty-six'), show(p104h6, 'So when two diagonals start'))),
    S('Triangles from the center',
      L("Now let's draw the radii again, from O to every corner. A regular polygon splits into n triangles. Two sides of "
        "each triangle are radii, so every triangle is isosceles. And all the triangles are the same, because all the "
        "sides of the polygon are equal.",
        show(p104rad['line'], 'from O to every corner'), show(p104rad['r'], 'splits into n triangles'),
        show(p104rad['t'], 'so every triangle is isosceles')),
      L("Let's see it in a regular pentagon. There are five triangles. The angle at the center is three hundred sixty "
        "divided by five, seventy-two.", show(p104rad['c'], 'The angle at the center'), show(p104r1, 'divided by five, seventy-two')),
      L("The two base angles share what's left. One hundred eighty minus seventy-two is one hundred eight. The two base "
        "angles are equal, so each one is half of one hundred eight, fifty-four.",
        show(p104r2, 'One hundred eighty minus seventy-two'), show(p104r3, 'each one is half'), show(p104rad['b'], 'fifty-four')),
      L("Now look at one corner of the pentagon. Two base angles meet there, one from each triangle. Fifty-four plus "
        "fifty-four is one hundred eight. That's exactly the pentagon's angle. So the radius cuts the corner's angle into "
        "two equal halves.", show(p104rad['h'], 'Two base angles meet there'), show(p104r4, 'Fifty-four plus'))),
    S('The hexagon',
      L("The regular hexagon is special. Its central angle is sixty. So each triangle has sixty at the top. The two base "
        "angles share one hundred twenty, so each one is sixty too.",
        show(p104hex['line'], 'The regular hexagon is special'), show(p104hx1, 'Its central angle is sixty'),
        show(p104hx2, 'The two base angles share'), show(p104hex['t'], 'so each one is sixty too')),
      L("All three angles are sixty, so the triangle is equilateral. A regular hexagon is made of six equilateral "
        "triangles. And that means the radius is equal to the side. If the side is five, the radius is five too.",
        show(p104hex['all'], 'six equilateral triangles'), show(p104hx3, 'the radius is equal to the side'),
        show(p104hex['rs'], 'If the side is five')),
      L("This split of the hexagon is very important. We'll use it for areas and for angles in the next lessons.")),
    S('Summary',
      L("Let's sum up. The angle sum is one hundred eighty times the bracket, n minus two. Or split from one corner into n minus two "
        "triangles. And every extra side adds one hundred eighty.", show(p104z1, "Let's sum up")),
      L("Regular means all the sides and all the angles are equal. Then one angle is the sum divided by n. The pentagon "
        "is one hundred eight, the hexagon is one hundred twenty, and the octagon is one hundred thirty-five.",
        show(p104z2, 'Regular means')),
      L("The central angle and the exterior angle are both three hundred sixty divided by n. Each one completes the "
        "polygon's angle to one hundred eighty.", show(p104z3, 'The central angle and the exterior angle')),
      L("The diagonals from one corner cut its angle into equal parts, one hundred eighty over n each. So an angle at a "
        "corner, with its arms through two other corners, is the sides between its arms, times one hundred eighty over n. "
        "The radii cut the polygon into n isosceles "
        "triangles, and in the hexagon, six equilateral triangles. Take a moment to memorize these, and I'll see you in "
        "the next video.", show(p104z4, 'The diagonals from one corner'), show(p104z5, 'The radii cut'))),
])

CAMERA_SPLIT = ('geo-104', 'Polygons', [
    (1, None),
    (8, "Let's continue with polygons."),
    (11, "Let's continue with the angles of regular polygons."),
    (14, "Let's continue with the lines inside a regular polygon."),
    (17, "Let's continue with the diagonals of a regular polygon."),
])


# =================================================================================================================
# geo-105 (lesson) - Polygon Areas
# Hebrew geo 5182-5192 + 5327-5362: no area formula for a polygon (only the triangle; not even a general quadrilateral);
# split it into shapes we know; the end of the lesson: "the hexagon: always six equilateral triangles; the octagon: always
# this split (a square, four rectangles, four corner triangles); other polygons: split by what the question gives".
# Kept from the English lesson: "or a bigger shape minus the missing pieces". R37 (core methods: g106, g107, g108, g113,
# g114, g115 and the real exam's hexagon questions): every way on concrete numbers - a "house" pentagon (square 6 + roof of
# height 4: 36 + 12 = 48), an L-shaped hexagon both ways (30 + 12 = 42; 60 - 18 = 42), the hexagon with side 4 (one
# triangle 4 root 3, six: 24 root 3; the trap: one triangle), the octagon split with side 2 (why the corner triangles are
# 45-45-90: 135 - 90 = 45; square 4, triangles 1 each = the square, rectangles 2 root 2; 8 + 8 root 2).
# Numbers differ from the Hebrew (3-4-5 pentagon 28, hexagon 6, octagon 6 / 4 / 1) and from the questions (g106 15/8,
# g107 12, g108 10). Visuals: each shape built at her words, the cut lines dashed teal, the pieces tinted one by one with
# their areas, the missing corner red.
# =================================================================================================================
_hs = [(70, 150), (230, 150), (230, 310), (70, 310)]; _hA = (150, 43)
p105house = PIN(GEO('p105house', [
    ('line', [('poly', [_hs[0], _hA, _hs[1], _hs[2], _hs[3]], 'ink', 3), side_lab(_hs[2], _hs[3], '6', (150, 230), 18),
              side_lab(_hs[1], _hs[2], '6', (150, 230), 18)]),
    ('cut', [sg(_hs[0], _hs[1], 'teal', 3, True)]),
    ('sq', [('tint', _hs, 'teal'), ('txt', 150, 240, '36', 'teal', 30)]),
    ('h', [sg(_hA, (150, 150), 'orange', 2.5, True), rt((150, 150), _hA, _hs[1], 10, 'orange'), ('txt', 162, 100, '4', 'orange', 24)]),
    ('tr', [('tint', [_hs[0], _hA, _hs[1]], 'orange'), ('txt', 120, 128, '12', 'orange', 26)]),
], vb='30 25 250 320', w=520, col=0, title='A pentagon like a house'))
p105h1 = IH('p105h1', 'square: $6 \\cdot 6 = 36$', size=36, col=1)
p105h2 = IH('p105h2', 'triangle: $\\dfrac{6 \\cdot 4}{2} = 12$', size=36, col=1)
p105h3 = IH('p105h3', '$36 + 12 = 48$', size=36, col=1)

_L = [(40, 300), (320, 300), (320, 216), (152, 216), (152, 132), (40, 132)]
p105L = PIN(GEO('p105L', [
    ('line', [('poly', _L, 'ink', 3), ('txt', 180, 324, '10', 'ink', 24), ('txt', 20, 216, '6', 'ink', 24),
              ('txt', 96, 114, '4', 'ink', 24), ('txt', 340, 258, '3', 'ink', 24)]),
    ('cut', [sg((40, 216), (152, 216), 'teal', 3, True)]),
    ('b', [('tint', [(40, 300), (320, 300), (320, 216), (40, 216)], 'teal'), ('txt', 180, 262, '30', 'teal', 28)]),
    ('t', [('tint', [(40, 216), (152, 216), (152, 132), (40, 132)], 'orange'), ('txt', 96, 178, '12', 'orange', 28),
           ('txt', 166, 176, '3', 'orange', 22)]),
], vb='0 95 370 245', w=480, col=0, title='An L-shaped hexagon: two rectangles'))
p105L2 = PIN(GEO('p105L2', [
    ('line', [('poly', _L, 'ink', 3), ('txt', 180, 324, '10', 'ink', 24), ('txt', 20, 216, '6', 'ink', 24),
              ('txt', 96, 114, '4', 'ink', 24), ('txt', 340, 258, '3', 'ink', 24)]),
    ('big', [sg((152, 132), (320, 132), 'teal', 3, True), sg((320, 132), (320, 216), 'teal', 3, True),
             ('tint', [(40, 300), (320, 300), (320, 132), (40, 132)], 'teal')]),
    ('miss', [('tint', [(152, 132), (320, 132), (320, 216), (152, 216)], 'red'), ('txt', 236, 112, '6', 'red', 24),
              ('txt', 236, 178, '18', 'red', 28)]),
], vb='0 95 370 245', w=480, col=0, title='The big rectangle minus the missing corner'))
p105L_1 = IH('p105L_1', '$6 - 3 = 3$', size=34, col=1)
p105L_2 = IH('p105L_2', '$10 \\cdot 3 = 30$', size=34, col=1)
p105L_3 = IH('p105L_3', '$4 \\cdot 3 = 12$', size=34, col=1)
p105L_4 = IH('p105L_4', '$30 + 12 = 42$', size=34, col=1)
p105L_5 = IH('p105L_5', '$10 \\cdot 6 = 60$', size=34, col=1)
p105L_6 = IH('p105L_6', '$10 - 4 = 6$', size=34, col=1)
p105L_7 = IH('p105L_7', '$6 \\cdot 3 = 18$', size=34, col=1)
p105L_8 = IH('p105L_8', '$60 - 18 = 42$', size=34, col=1)

_Oz = (170, 170); _Hz = rp(_Oz[0], _Oz[1], 125, 6, 0)
p105hex = PIN(GEO('p105hex', [
    ('line', [('poly', _Hz, 'ink', 3)] + [pdot(q) for q in _Hz] + [side_lab(_Hz[0], _Hz[1], '4', _Oz, 18)]),
    ('cut', [sg(_Hz[k], _Hz[k + 3], 'teal', 3, True) for k in range(3)]),
    ('one', [('tint', [_Oz, _Hz[0], _Hz[1]], 'teal'), ('txt', *cen([_Oz, _Hz[0], _Hz[1]]), '4√3', 'teal', 22)]),
    ('six', [('tint', [_Oz, _Hz[k], _Hz[(k + 1) % 6]], 'orange' if k % 2 else 'teal') for k in range(1, 6)]),
], vb='30 45 290 250', w=520, col=0, title='A regular hexagon with side 4'))
p105x1 = I('p105x1', 'equilateral triangle: $\\dfrac{a^2\\sqrt3}{4}$', size=34, col=1)
p105x2 = IH('p105x2', '$\\dfrac{4^2\\sqrt3}{4} = \\dfrac{16\\sqrt3}{4} = 4\\sqrt3$', size=34, col=1)
p105x3 = IH('p105x3', '$6 \\cdot 4\\sqrt3 = 24\\sqrt3$', size=34, col=1)

_u = 72.0; _lg = _u * 2 ** 0.5; _ox, _oy = 200, 190
_Oc = [(_ox - _u, _oy - _u - _lg), (_ox + _u, _oy - _u - _lg), (_ox + _u + _lg, _oy - _u), (_ox + _u + _lg, _oy + _u),
       (_ox + _u, _oy + _u + _lg), (_ox - _u, _oy + _u + _lg), (_ox - _u - _lg, _oy + _u), (_ox - _u - _lg, _oy - _u)]
_sqm = [(_ox - _u, _oy - _u), (_ox + _u, _oy - _u), (_ox + _u, _oy + _u), (_ox - _u, _oy + _u)]
_ctri = [[_Oc[7], _Oc[0], _sqm[0]], [_Oc[1], _Oc[2], _sqm[1]], [_Oc[3], _Oc[4], _sqm[2]], [_Oc[5], _Oc[6], _sqm[3]]]
_rects = [[_Oc[0], _Oc[1], _sqm[1], _sqm[0]], [_sqm[1], _Oc[2], _Oc[3], _sqm[2]], [_sqm[3], _sqm[2], _Oc[4], _Oc[5]],
          [_Oc[7], _sqm[0], _sqm[3], _Oc[6]]]
_s2 = (520, 190)
_sq2 = [(_s2[0] - _u, _s2[1] - _u), (_s2[0] + _u, _s2[1] - _u), (_s2[0] + _u, _s2[1] + _u), (_s2[0] - _u, _s2[1] + _u)]
def OCTCUT():
    return ([sg((_ox - _u, _Oc[0][1]), (_ox - _u, _Oc[5][1]), 'teal', 3, True), sg((_ox + _u, _Oc[0][1]), (_ox + _u, _Oc[5][1]), 'teal', 3, True),
             sg((_Oc[7][0], _oy - _u), (_Oc[2][0], _oy - _u), 'teal', 3, True), sg((_Oc[7][0], _oy + _u), (_Oc[2][0], _oy + _u), 'teal', 3, True)])
p105oct = PIN(GEO('p105oct', [
    ('line', [('poly', _Oc, 'ink', 3)] + [pdot(q) for q in _Oc] + [side_lab(_Oc[0], _Oc[1], '2', (_ox, _oy), 16)]),
    ('cut', OCTCUT()),
    ('ang', [ang(_Oc[0], _Oc[7], _Oc[1], 30, 'orange'), at(_Oc[0], '135°', -62, -4, 'orange', 22), rt(_sqm[0], _Oc[7], _Oc[0], 12, 'teal')]),
    ('sq', [('tint', _sqm, 'teal'), ('txt', _ox, _oy, '4', 'teal', 30)]),
    ('tri', [x for t in _ctri for x in (('tint', t, 'orange'), ('txt',) + tuple(cen(t)) + ('1', 'orange', 22))]
            + [('txt', _ox - _u - _lg / 2 - 10, _oy - _u - 4, '√2', 'orange', 20)]),
    ('four', [('poly', _sq2, 'ink', 3), sg(_sq2[0], _sq2[2], 'orange', 2.5, True), sg(_sq2[1], _sq2[3], 'orange', 2.5, True)]
             + [('tint', [_sq2[k], _sq2[(k + 1) % 4], _s2], 'orange') for k in range(4)] + [('txt', _s2[0], _s2[1] + _u + 30, '4 triangles = the square', 'orange', 20)]),
    ('rect', [('tint', r, 'teal') for r in _rects] + [('txt',) + tuple(cen(r)) + ('2√2', 'teal', 20) for r in _rects]),
], vb='10 0 610 380', w=600, col=0, title='A regular octagon with side 2'))
p105o1 = I('p105o1', '1 square $+$ 4 rectangles $+$ 4 triangles', size=32, col=1)
p105o2 = IH('p105o2', '$135° - 90° = 45°$', size=34, col=1)
p105o3 = IH('p105o3', 'square: $2 \\cdot 2 = 4$', size=34, col=1)
p105o4 = IH('p105o4', 'leg: $\\dfrac{2}{\\sqrt2} = \\sqrt2$', size=34, col=1)
p105o5 = IH('p105o5', 'triangle: $\\dfrac{\\sqrt2 \\cdot \\sqrt2}{2} = 1$', size=34, col=1)
p105o6 = IH('p105o6', 'rectangle: $2 \\cdot \\sqrt2 = 2\\sqrt2$', size=34, col=1)
p105o7 = IH('p105o7', '$4 + 4 + 4 \\cdot 2\\sqrt2 = 8 + 8\\sqrt2$', size=34, col=1)

video('geo-105', 'lesson', slides=[
    S('Polygon Areas',
      L("Now let's find the area of a polygon. We don't have one simple formula to use for every shape here. But we "
        "know how to find a triangle's area: a side, times the height to that side, divided by two.")),
    S('Cut it into shapes',
      L("We also know the special quadrilaterals, like the square, the rectangle and the trapezoid. For a general "
        "quadrilateral, we don't have one of those ready-made formulas. So there are two ways. We cut the polygon into "
        "shapes we know. Or we see it as a bigger shape, minus the pieces that are missing."),
      L("Let's start with an easy one. This pentagon looks like a house. Its bottom part is a square with side six. On "
        "top there's a triangle, and its height is four.",
        show(p105house['line'], 'This pentagon looks like a house'), show(p105house['h'], 'its height is four')),
      L("We draw one line, and we get two shapes we know. The square is six times six, thirty-six. The triangle is its "
        "base, six, times its height, four, divided by two. Six times four is twenty-four, and half of that is twelve.",
        show(p105house['cut'], 'We draw one line'), show(p105house['sq'], 'The square is six times six'), show(p105h1, 'thirty-six. The'),
        show(p105house['tr'], 'The triangle is its base'), show(p105h2, 'Six times four is twenty-four')),
      L("So the area of the pentagon is thirty-six plus twelve, forty-eight.", show(p105h3, 'thirty-six plus twelve'))),
    S('Two ways',
      L("Here's a hexagon shaped like the letter L. Its sides are horizontal or vertical. The bottom is ten long, and the left "
        "side is six high. The top is four long, and the short side on the right is three.",
        show(p105L['line'], "Here's a hexagon shaped like the letter L")),
      L("The first way is to cut it. One line across gives two rectangles. The bottom one is ten long and three high. "
        "Ten times three is thirty.", show(p105L['cut'], 'One line across'), show(p105L['b'], 'The bottom one'),
        show(p105L_2, 'Ten times three is thirty')),
      L("The top one is four long. Its height is the left side, six, minus the three we used. Six minus three is three. "
        "So it's four times three, twelve. Together, thirty plus twelve is forty-two.",
        show(p105L_1, 'Six minus three is three'), show(p105L['t'], "So it's four times three"), show(p105L_3, 'four times three, twelve'),
        show(p105L_4, 'thirty plus twelve')),
      L("The second way is a big shape minus the missing piece. Let's complete the hexagon to a rectangle, ten by six. "
        "Ten times six is sixty.", show(p105L2['line'], 'The second way'), show(p105L2['big'], 'complete the hexagon to a rectangle'),
        show(p105L_5, 'Ten times six is sixty')),
      L("The missing corner is ten minus four, six long, and it's three high. Six times three is eighteen. So the area "
        "is sixty minus eighteen, forty-two. The same answer.",
        show(p105L_6, 'ten minus four'), show(p105L2['miss'], 'and it\'s three high'), show(p105L_7, 'Six times three is eighteen'),
        show(p105L_8, 'sixty minus eighteen')),
      L("So when a polygon has no formula, look for lines that cut it into shapes you know. Or close it into a big "
        "shape, and take away what's missing.")),
    S('The regular hexagon',
      L("For two regular polygons, there's one cut we always use. The first one is the regular hexagon. Like in the "
        "first lesson, we cut it into six equilateral triangles.",
        show(p105hex['line'], 'The first one is the regular hexagon'), show(p105hex['cut'], 'six equilateral triangles')),
      L("Remember the area of an equilateral triangle with side a. It's a squared, times root three, divided by four.",
        show(p105x1, 'Remember the area')),
      L("Let's take a hexagon with side four. One triangle is four squared, sixteen, times root three, divided by four. "
        "Sixteen divided by four is four. So one triangle is four root three.",
        show(p105hex['one'], 'One triangle is four squared'), show(p105x2, 'Sixteen divided by four')),
      L("The hexagon has six triangles. Six times four root three is twenty-four root three. Careful here. Many students "
        "stop at one triangle. But four root three is only one sixth of the hexagon.",
        show(p105hex['six'], 'The hexagon has six triangles'), show(p105x3, 'Six times four root three'))),
    S('The regular octagon',
      L("The second one is the regular octagon. We cut a rectangle off the top and the bottom, and off the two sides. "
        "So we get a square in the middle, four rectangles, and four small triangles in the corners.",
        show(p105oct['line'], 'The second one is the regular octagon'), show(p105oct['cut'], 'We cut a rectangle'),
        show(p105o1, 'So we get a square')),
      L("Why is each corner triangle a right triangle? The octagon's angle is one hundred thirty-five. The rectangle takes "
        "ninety of it. One hundred thirty-five minus ninety is forty-five. So the triangle has two angles of forty-five, "
        "and the third one is ninety. It's a silver triangle, forty-five, forty-five, ninety.",
        show(p105oct['ang'], "The octagon's angle is one hundred thirty-five"), show(p105o2, 'One hundred thirty-five minus ninety')),
      L("Let's take an octagon with side two. The square in the middle has side two, so its area is two times two, four.",
        show(p105oct['sq'], 'The square in the middle'), show(p105o3, 'two times two, four')),
      L("The hypotenuse of each corner triangle is a side of the octagon, two. In a silver triangle, we go from the "
        "hypotenuse to a leg by dividing by root two. Two divided by root two is root two.",
        show(p105o4, 'Two divided by root two')),
      L("So the area of one triangle is root two times root two, divided by two. Root two times root two is two, and "
        "half of that is one. Four triangles make four.",
        show(p105o5, 'Root two times root two is two'), show(p105oct['tri'], 'Four triangles make four')),
      L("That's exactly the square. Put the four triangles together and they fill the square, like a square cut by its "
        "two diagonals. This is true in every regular octagon.", show(p105oct['four'], 'they fill the square')),
      L("Each rectangle is two long, and its width is the leg of a triangle, root two. So it's two root two. Four "
        "rectangles make eight root two.", show(p105oct['rect'], 'Each rectangle is two long'), show(p105o6, "So it's two root two")),
      L("So the octagon is four, plus four, plus eight root two. That's eight plus eight root two. Always cut the octagon "
        "like this, even when they ask for only a part of it. And I'll see you in the next video.",
        show(p105o7, 'So the octagon is four'))),
])


# =================================================================================================================
# Question videos (topic 34). Layout (batch C, as NOFIG33): on every slide our enlarged colour copy of the question's
# figure sits on the left (LEFT; its base layer is the question's black-and-white figure, redrawn) and the working is
# written in readable rows on the right (FLOW), each at its own clause. A new slide redraws the figure with the values
# found so far (V2 / V3).
# =================================================================================================================
def QY(vid, y):
    """(topic 34) the work area of a question video starts at y (below the question's text)"""
    return y


def NOFIG(vid, *slides):
    NOFIG34.update((vid, k) for k in slides)


# =================================================================================================================
# solve-geo34-g106 - an irregular pentagon: cut into shapes we know
# Hebrew geo 5193-5221 (3-4-5 there, 8-15-17 here): not regular, a few right angles; split into shapes I know; draw AD:
# a right triangle, legs over 2; what's left is a trapezoid, no bottom base; work with what we have: the triple -> AD;
# drop another height: a square (angles 90), another right triangle, the triple again -> the leg; add: triangle,
# triangle, square. R37: "cut it into shapes we know" is taught in geo-105; here the first use, slowly, with a link.
# Kept from the English video: the trap 285 (only the trapezoid) - said at the step.
# V3: the copy built at her words: AD dashed teal, AED tinted teal with 60, the trapezoid ABCD outlined orange; slide 2:
# AD = 17 written, the height AH dashed with its right angle, the square tinted, AHD tinted with 8; slide 3: the three
# pieces with their areas.
# =================================================================================================================
_A6, _B6, _C6, _D6, _E6 = (300.5, 70.0), (530.0, 70.0), (530.0, 299.5), (178.1, 299.5), (109.9, 197.9)
_H6 = (300.5, 299.5)
def _g106_base(extra=()):
    e = [('poly', [_A6, _B6, _C6, _D6, _E6], 'ink', 3), rt(_B6, _A6, _C6, 11, 'ink'), rt(_C6, _B6, _D6, 11, 'ink'),
         rt(_E6, _A6, _D6, 11, 'ink'),
         ('txt', 415, 48, '15', 'ink', 30), ('txt', 552, 185, '15', 'ink', 30), ('txt', 192, 115, '15', 'ink', 30),
         ('txt', 128, 258, '8', 'ink', 30),
         ('txt', 300, 46, 'A', 'ink', 32, True), ('txt', 548, 52, 'B', 'ink', 32, True), ('txt', 548, 318, 'C', 'ink', 32, True),
         ('txt', 168, 322, 'D', 'ink', 32, True), ('txt', 88, 192, 'E', 'ink', 32, True)]
    return e + list(extra)
_vb106 = '60 22 530 320'
f106a = PIN(GEO('f106a', [
    ('line', _g106_base()),
    ('ad', [sg(_A6, _D6, 'teal', 3, True)]),
    ('aed', [('tint', [_A6, _E6, _D6], 'teal')]),
    ('aedarea', [('txt', 196, 205, '60', 'teal', 34)]),
    ('trap', [('poly', [_A6, _B6, _C6, _D6], 'orange', 5), ('txt', 420, 250, '?', 'orange', 30), ('txt', 345, 322, 'C D = ?', 'orange', 30)]),
], vb=_vb106, w=520, title='The pentagon'))
f106b = PIN(GEO('f106b', [
    ('line', _g106_base([sg(_A6, _D6, 'teal', 3, True), ('tint', [_A6, _E6, _D6], 'teal')])),
    ('ad', [('txt', 252, 175, '17', 'teal', 34)]),
    ('ah', [sg(_A6, _H6, 'orange', 3, True), rt(_H6, _A6, _C6, 11, 'orange'), ('txt', 300, 322, 'H', 'orange', 32, True)]),
    ('sq', [('tint', [_A6, _B6, _C6, _H6], 'orange'), ('txt', 318, 185, '15', 'orange', 30), ('txt', 415, 318, '15', 'orange', 30)]),
    ('ahd', [('tint', [_A6, _H6, _D6], 'teal'), ('txt', 240, 318, '8', 'teal', 34)]),
], vb=_vb106, w=520, title='Two more right triangles'))
f106c = PIN(GEO('f106c', [
    ('line', _g106_base([sg(_A6, _D6, 'ink', 2.5, True), sg(_A6, _H6, 'ink', 2.5, True), ('txt', 300, 322, 'H', 'ink', 30, True)])),
    ('sq', [('tint', [_A6, _B6, _C6, _H6], 'orange'), ('txt', 415, 185, '225', 'orange', 30)]),
    ('ahd', [('tint', [_A6, _H6, _D6], 'teal'), ('txt', 262, 240, '60', 'teal', 32)]),
    ('aed', [('tint', [_A6, _E6, _D6], 'orange'), ('txt', 180, 210, '60', 'orange', 32)]),
], vb=_vb106, w=520, title='Three pieces'))
for _g in (f106a, f106b, f106c): LEFT(_g, y=QY('g106', 330), x=410, w=520)
f106r1 = IH('f106r1', '$15 \\cdot 8 = 120$', size=34)
f106r2 = IH('f106r2', '$120 \\div 2 = 60$', size=34)
f106s1 = IH('f106s1', '$8, 15 \\to AD = 17$', size=34)
f106s2 = IH('f106s2', '$AH = HC = 15$', size=34)
f106s3 = IH('f106s3', '$15, 17 \\to HD = 8$', size=34)
f106t1 = IH('f106t1', 'square: $15 \\cdot 15 = 225$', size=34)
f106t2 = IH('f106t2', '$AHD$: $\\dfrac{15 \\cdot 8}{2} = 60$', size=34)
f106t3 = IH('f106t3', '$225 + 60 = 285$: only $ABCD$', size=34)
f106t4 = IH('f106t4', '$225 + 60 + 60 = 345$', size=34)
FLOW([f106r1, f106r2], [(960, 620, 340, 700)])
FLOW([f106s1, f106s2, f106s3], [(960, 620, 340, 700)])
FLOW([f106t1, f106t2, f106t3, f106t4], [(960, 620, 340, 700)])
NOFIG('solve-geo34-g106', 0, 1, 2)

video('solve-geo34-g106', 'solution', qid='geo34-g106', slides=[
    S('Cut it into shapes we know',
      L("In pentagon A B C D E, angles B, C and E are right angles, and A B is parallel to C D. A B, B C and A E are each "
        "fifteen, and D E is eight. What is the area of the pentagon?",
        pt('stem', 'In pentagon A B C D E', 'hl', 9.0), show(f106a['line'], 'A B, B C and A E'), voice='calm', pause=0.5),
      L("This pentagon is not regular. It has a few right angles, but its sides are not all equal. We don't have a "
        "ready-made formula for this shape. So like in the lesson, we cut it into shapes we know."),
      L("Let's draw a line from A to D. Now look at triangle A E D. The angle at E is a right angle, so it's a right "
        "triangle. Its legs are A E, fifteen, and E D, eight.",
        show(f106a['ad'], 'draw a line from A to D'), show(f106a['aed'], 'Now look at triangle A E D')),
      L("The area of a right triangle is one leg times the other, divided by two. Fifteen times eight is one hundred "
        "twenty. Half of that is sixty.", show(f106r1, 'Fifteen times eight'), show(f106r2, 'Half of that is sixty'),
        show(f106a['aedarea'], 'Half of that is sixty')),
      L("What's left is A B C D. A B is parallel to C D, so it's a trapezoid. For its area we need both bases and the "
        "height. We have the top base, fifteen, and the height, B C, fifteen. But we don't have the bottom base, C D.",
        show(f106a['trap'], "What's left is A B C D"))),
    S('Find the missing pieces',
      L("So let's work with what we have. Triangle A E D has legs eight and fifteen. Remember the triple eight, fifteen, "
        "seventeen. So the hypotenuse, A D, is seventeen.",
        show(f106b['line'], "So let's work with what we have"), show(f106s1, 'Remember the triple'), show(f106b['ad'], 'is seventeen')),
      L("Now let's drop a height from A down to C D. Call its foot H. A B C H has right angles at B, at C and at H. So "
        "the fourth angle, at A, is a right angle too. And A B is equal to B C. So A B C H is a square with side fifteen. "
        "A H is fifteen, and H C is fifteen.",
        show(f106b['ah'], 'drop a height from A'), show(f106b['sq'], 'So A B C H is a square'), show(f106s2, 'A H is fifteen')),
      L("Now look at triangle A H D. It's a right triangle, because A H is a height. Its hypotenuse is A D, seventeen, "
        "and one leg is A H, fifteen. That's eight, fifteen, seventeen again. So the other leg, H D, is eight.",
        show(f106b['ahd'], 'Now look at triangle A H D'), show(f106s3, 'So the other leg'))),
    S('Add the pieces',
      L("Now the pentagon is made of three shapes we know. The square A B C H is fifteen times fifteen, two hundred "
        "twenty-five.", show(f106c['line'], 'three shapes we know'), show(f106c['sq'], 'The square A B C H'),
        show(f106t1, 'fifteen times fifteen')),
      L("Triangle A H D has legs fifteen and eight. So its area is fifteen times eight, divided by two, sixty.",
        show(f106c['ahd'], 'Triangle A H D'), show(f106t2, 'divided by two, sixty')),
      L("Careful here. Two hundred twenty-five plus sixty is two hundred eighty-five, and that's choice number four. But "
        "that's only the trapezoid A B C D. Triangle A E D is outside it, and we still need to add it.",
        show(f106t3, 'Two hundred twenty-five plus sixty'), show(f106c['aed'], 'Triangle A E D is outside it')),
      L("Triangle A E D is sixty too, as we found. So the area is two hundred twenty-five, plus sixty, plus sixty. Two "
        "hundred twenty-five plus one hundred twenty is three hundred forty-five. Choice number two is our answer, and "
        "I'll see you in the next question.", show(f106t4, 'So the area is two hundred twenty-five'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# solve-geo34-g107 - a regular hexagon with side 12: six equilateral triangles
# Hebrew geo 5222-5236 (side 6 there): I can't find a hexagon's area, but I can split it into equilateral triangles; the
# formula a, 2, 3, 4; "don't make the mistake": one triangle is not in the choices / is the trap; times 6; "always, for a
# regular hexagon: diagonals, six equilateral triangles, one, times 6". R37: taught in geo-105 (side 4); here applied
# slowly with a link. Traps at the step: 36 root 3 (one triangle), 144 root 3 (no division by 4).
# V3: the copy, the three long diagonals dashed, one triangle tinted with 12 on its sides, then all six tinted.
# =================================================================================================================
_O107 = (320.0, 180.0); _H107 = rp(_O107[0], _O107[1], 107.353, 6, 0)
def _g107_base(extra=()):
    e = [('poly', _H107, 'ink', 3)] + [nm(p, t, _O107, 24) for p, t in zip(_H107, 'ABCDEF')]
    return e + list(extra)
f107 = PIN(GEO('f107', [
    ('line', _g107_base()),
    ('cut', [sg(_H107[k], _H107[k + 3], 'teal', 3, True) for k in range(3)]),
    ('one', [('tint', [_O107, _H107[0], _H107[1]], 'teal'), side_lab(_H107[0], _H107[1], '12', _O107, 20, 'teal', 28),
             at(mid(_O107, _H107[0]), '12', 0, 20, 'teal', 26), at(mid(_O107, _H107[1]), '12', -22, 4, 'teal', 26)]),
    ('six', [('tint', [_O107, _H107[k], _H107[(k + 1) % 6]], 'orange' if k % 2 else 'teal') for k in range(1, 6)]),
], vb='175 40 290 285', w=480, title='The regular hexagon'))
LEFT(f107, y=QY('g107', 230), x=410, w=480)
f107r1 = I('f107r1', 'one triangle: $\\dfrac{a^2\\sqrt3}{4}$', size=30)
f107r2 = IH('f107r2', '$12^2 = 144$', size=34)
f107r3 = IH('f107r3', '$\\dfrac{144\\sqrt3}{4} = 36\\sqrt3$', size=34)
f107r4 = IH('f107r4', '$6 \\cdot 36 = 180 + 36 = 216$', size=34)
f107r5 = IH('f107r5', 'area $= 216\\sqrt3$', size=34)
FLOW([f107r1, f107r2, f107r3, f107r4, f107r5], [(920, 660, 240, 700)])
NOFIG('solve-geo34-g107', 0)

video('solve-geo34-g107', 'solution', qid='geo34-g107', slides=[
    S('Six equilateral triangles',
      L("A regular hexagon has side length twelve. What is its area?", pt('stem', 'A regular hexagon', 'hl', 4.0),
        show(f107['line'], 'A regular hexagon'), voice='calm', pause=0.5),
      L("Like in the lesson, a regular hexagon is made of six equilateral "
        "triangles. So we find the area of one triangle, and then we multiply by six."),
      L("Let's draw the three long diagonals, through the center. We get six equilateral triangles. The side of each one "
        "is the side of the hexagon, twelve.", show(f107['cut'], 'draw the three long diagonals'),
        show(f107['one'], 'The side of each one')),
      L("The area of an equilateral triangle with side a is a squared, times root three, divided by four. Here a is "
        "twelve, and twelve squared is one hundred forty-four.", show(f107r1, 'The area of an equilateral triangle'),
        show(f107r2, 'twelve squared')),
      L("So one triangle is one hundred forty-four root three, divided by four. One hundred forty-four divided by four is "
        "thirty-six. So one triangle is thirty-six root three. If we forget to divide by four, we get one hundred "
        "forty-four root three. That's choice number two, and it's a trap.",
        show(f107r3, 'One hundred forty-four divided by four'), mk('cross', 'choice 2', "That's choice number two")),
      L("Careful here too. Thirty-six root three is choice number one. But that's only one triangle, one sixth of the "
        "hexagon.", mk('cross', 'choice 1', 'Thirty-six root three is choice number one')),
      L("The hexagon has six triangles, so we need six times thirty-six. Six times thirty is one hundred eighty. Six "
        "times six is thirty-six. Together, two hundred sixteen. So the area is two hundred sixteen root three. Choice number four is our "
        "answer, and I'll see you in the next question.",
        show(f107['six'], 'The hexagon has six triangles'), show(f107r4, 'Six times thirty is'),
        show(f107r5, 'So the area is two hundred sixteen'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
])


# =================================================================================================================
# solve-geo34-g108 - a regular octagon with side 10: the octagon split
# Hebrew geo 5237-5361 (side 6 there; the pattern with 4 and 1; the cross): every time, split it the same way (a
# rectangle off the top, one off the side): a square, 4 triangles, 4 rectangles; symmetric; silver triangles; the four
# triangles together = the square (true in every regular octagon); rectangle = side x leg (hypotenuse / root 2); total;
# the pattern 2a^2 + 2a^2 root 2 (take the square twice, then the same number with root 2); a part: the cross. R37: the
# split is taught in geo-105 (side 2); here applied slowly with a link. Kept from the English video: sides 3 and 7, the
# trap 200 + 100 root 2 (two rectangles). W20: the pattern, with the reason (the triangles = a second square; the
# rectangles = 2 a^2 root 2).
# V3: the copy cut with dashed teal lines, the square tinted with 100, the triangles orange with 25, the rectangles teal
# with 50 root 2; slide 3: the cross tinted.
# =================================================================================================================
_O8 = [(268.12, 54.752), (371.88, 54.752), (445.248, 128.12), (445.248, 231.88), (371.88, 305.248), (268.12, 305.248),
       (194.752, 231.88), (194.752, 128.12)]
_m8 = [(268.12, 128.12), (371.88, 128.12), (371.88, 231.88), (268.12, 231.88)]
_t8 = [[_O8[7], _O8[0], _m8[0]], [_O8[1], _O8[2], _m8[1]], [_O8[3], _O8[4], _m8[2]], [_O8[5], _O8[6], _m8[3]]]
_r8 = [[_O8[0], _O8[1], _m8[1], _m8[0]], [_m8[1], _O8[2], _O8[3], _m8[2]], [_m8[3], _m8[2], _O8[4], _O8[5]], [_O8[7], _m8[0], _m8[3], _O8[6]]]
def _oct_cut(P, M):
    return [sg((M[0][0], P[0][1]), (M[0][0], P[5][1]), 'teal', 3, True), sg((M[1][0], P[0][1]), (M[1][0], P[5][1]), 'teal', 3, True),
            sg((P[7][0], M[0][1]), (P[2][0], M[0][1]), 'teal', 3, True), sg((P[7][0], M[2][1]), (P[2][0], M[2][1]), 'teal', 3, True)]
def _g108_base(cut=False, extra=()):
    e = [('poly', _O8, 'ink', 3), side_lab(_O8[0], _O8[1], '10', (320, 180), 18)]
    if cut: e += [s[:5] + ('ink', 2, True) for s in _oct_cut(_O8, _m8)]
    return e + list(extra)
f108a = PIN(GEO('f108a', [
    ('line', _g108_base()),
    ('cut', _oct_cut(_O8, _m8)),
    ('sq', [('tint', _m8, 'teal'), ('txt', 320, 180, '100', 'teal', 30), side_lab(_m8[0], _m8[1], '10', (320, 180), -16, 'teal', 26)]),
], vb='165 15 310 320', w=480, title='The regular octagon'))
f108b = PIN(GEO('f108b', [
    ('line', _g108_base(True, [('tint', _m8, 'teal'), ('txt', 320, 180, '100', 'teal', 30)])),
    ('tri', [x for t in _t8 for x in (('tint', t, 'orange'),)]),
    ('leg', [('txt', 231, 145, '5√2', 'orange', 22)]),
    ('t25', [('txt',) + tuple(cen(t)) + ('25', 'orange', 26) for t in _t8]),
    ('rect', [('tint', r, 'teal') for r in _r8]),
    ('r50', [('txt', 320, 96, '50√2', 'teal', 24), ('txt', 408, 182, '50√2', 'teal', 22), ('txt', 320, 270, '50√2', 'teal', 24),
             ('txt', 232, 182, '50√2', 'teal', 22)]),
], vb='165 15 310 320', w=480, title='The pieces of the octagon'))
f108c = PIN(GEO('f108c', [
    ('line', _g108_base(True)),
    ('cross', [('tint', _m8, 'teal')] + [('tint', r, 'teal') for r in _r8]),
    ('out', [('tint', t, 'red') for t in _t8]),
], vb='165 15 310 320', w=480, title='The cross in the middle'))
for _g in (f108a, f108b, f108c): LEFT(_g, y=QY('g108', 230), x=410, w=480)
f108r1 = I('f108r1', '1 square $+$ 4 rectangles $+$ 4 triangles', size=28)
f108r2 = IH('f108r2', 'square: $10 \\cdot 10 = 100$', size=34)
f108s1 = I('f108s1', '4 triangles $= 100$', size=30)
f108s2 = IH('f108s2', 'leg: $\\dfrac{10}{\\sqrt2} = \\dfrac{10\\sqrt2}{2} = 5\\sqrt2$', size=34)
f108s3 = IH('f108s3', '$\\dfrac{5\\sqrt2 \\cdot 5\\sqrt2}{2} = \\dfrac{50}{2} = 25$', size=34)
f108s4 = IH('f108s4', 'rectangle: $10 \\cdot 5\\sqrt2 = 50\\sqrt2$', size=34)
f108s5 = IH('f108s5', '$4 \\cdot 50\\sqrt2 = 200\\sqrt2$', size=34)
f108s6 = IH('f108s6', '$100 + 100 + 200\\sqrt2$', size=34)
f108s7 = IH('f108s7', '$= 200 + 200\\sqrt2$', size=34)
f108p1 = I('f108p1', 'side $a$: $\\ 2a^2 + 2a^2\\sqrt2$', size=32)
f108p2 = IH('f108p2', '$3$: $\\ 9 \\cdot 2 = 18$: $\\ 18 + 18\\sqrt2$', size=34)
f108p3 = IH('f108p3', '$7$: $\\ 49 \\cdot 2 = 98$: $\\ 98 + 98\\sqrt2$', size=34)
f108p4 = IH('f108p4', 'cross: $200 + 200\\sqrt2 - 100$', size=34)
f108p5 = IH('f108p5', '$= 100 + 200\\sqrt2$', size=34)
FLOW([f108r1, f108r2], [(920, 660, 240, 700)])
FLOW([f108s1, f108s2, f108s3, f108s4], [(920, 340, 240, 700)])
FLOW([f108s5, f108s6, f108s7], [(1300, 280, 240, 700)])
FLOW([f108p1, f108p2, f108p3, f108p4, f108p5], [(920, 660, 240, 700)])
NOFIG('solve-geo34-g108', 0, 1, 2)

video('solve-geo34-g108', 'solution', qid='geo34-g108', slides=[
    S('The octagon split',
      L("A regular octagon has side length ten. What is its area?", pt('stem', 'A regular octagon', 'hl', 4.0),
        show(f108a['line'], 'A regular octagon'), voice='calm', pause=0.5),
      L("Like in the lesson, we find the area by cutting the regular octagon into shapes we know. We get a square in "
        "the middle, four rectangles, and four silver triangles in the corners.",
        show(f108a['cut'], 'cutting the regular octagon'), show(f108r1, 'We get a square in the middle')),
      L("Let's start with the square. Its side is a side of the octagon, ten. So its area is ten times ten, one hundred.",
        show(f108a['sq'], "Let's start with the square"), show(f108r2, 'ten times ten'))),
    S('Triangles and rectangles',
      L("Now the four corner triangles. Remember from the lesson, together they fill exactly one square like the middle "
        "one. So together they're one hundred too.",
        show(f108b['line'], 'Now the four corner triangles'), show(f108b['tri'], 'together they fill'), show(f108s1, "they're one hundred too")),
      L("Let's check it. The hypotenuse of a corner triangle is a side of the octagon, ten. In a silver triangle, we go "
        "from the hypotenuse to a leg by dividing by root two. Ten over root two, times root two over root two, is ten "
        "root two over two. That's five root two.",
        show(f108s2, 'Ten over root two'), show(f108b['leg'], "That's five root two")),
      L("So one triangle is five root two times five root two, divided by two. Five root two times five root two is "
        "twenty-five times two, fifty. Half of that is twenty-five. And four triangles are one hundred, just like the "
        "square.", show(f108s3, 'Five root two times five root two is'), show(f108b['t25'], 'Half of that is twenty-five')),
      L("Now a rectangle. One side is a side of the octagon, ten. The other side is a leg of a corner triangle, five "
        "root two. So one rectangle is ten times five root two, fifty root two.",
        show(f108b['rect'], 'Now a rectangle'), show(f108s4, 'So one rectangle is'), show(f108b['r50'], 'fifty root two.')),
      L("There are four rectangles, so they make two hundred root two. Careful, four, not two. With only two "
        "rectangles we'd get one hundred root two, and that's the trap in choice number two.",
        show(f108s5, 'so they make two hundred root two'), mk('cross', 'choice 2', "the trap in choice number two")),
      L("So the octagon is one hundred, plus one hundred, plus two hundred root two. That's two hundred plus two hundred "
        "root two. Choice number one is our answer.",
        show(f108s6, 'So the octagon is one hundred'), show(f108s7, "That's two hundred plus"),
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
    S('A pattern',
      L("This question hides a pattern that's true in every regular octagon. The square in the middle is the side "
        "squared, here one hundred. Double it, and you get the plain number, two hundred. Then write the same number "
        "again, with root two. So it's two hundred plus two hundred root two.",
        show(f108c['line'], 'This question hides a pattern'), show(f108p1, 'Then write the same number')),
      L("Why? The four triangles make a second square, so the plain part is two squares. And the four rectangles always "
        "come out as the same number, times root two."),
      L("Let's try it with side three. Three squared is nine. Double it, eighteen. So the area is eighteen plus eighteen "
        "root two. With side seven, seven squared is forty-nine. Double it, ninety-eight. So the area is ninety-eight plus "
        "ninety-eight root two.", show(f108p2, 'Let\'s try it with side three'), show(f108p3, 'With side seven')),
      L("The same cut helps when a question asks for only a part of the octagon. Take the cross in the middle, the "
        "square and the four rectangles. That's the whole octagon without the four triangles. Two hundred plus two "
        "hundred root two, minus the one hundred of the triangles. That leaves one hundred plus two hundred root two. "
        "And I'll see you in the next question.", show(f108c['cross'], 'Take the cross in the middle'), show(f108c['out'], 'without the four triangles'),
        show(f108p4, 'minus the one hundred'), show(f108p5, 'That leaves one hundred plus'))),
])


# =================================================================================================================
# geo-109 (lesson) - Advanced Polygons: the triangles inside regular polygons
# Hebrew geo 5374-5377 ("last lesson the rules; now harder questions and nuances that come back") - the Hebrew lesson
# itself is only this overview, the tools are taught inside its questions. R37 (2026-10-21): two core methods used by
# g110, g112, g112-area, q-r26-t34-03 and the real exam (2023 spring q2_03, 2020 winter q2_04, 2023 autumn q2_02,
# 2025 spring q1_18, 2023 winter q2_05, 2025 winter q2_15) are taught here, each on numbers:
#   - the corner triangle (two sides at a corner + the diagonal): isosceles, the top angle = the polygon's angle;
#     square 45 / 45, pentagon 36 / 36, hexagon 30 / 30; the trap: only in a regular polygon;
#   - the hexagon's diagonals: long = 2a (two radii, radius = side), short = a root 3 (the 30-30-120 triangle as two golden
#     halves); sides 2 and 5; backwards: 9 -> 3 root 3.
# Study plan: the golden triangle (30-60-90: x, x root 3, 2x) and the isosceles triangle are topic 31 (reminders).
# Visuals: three clean polygons with the corner triangle tinted (sides ticked, the diagonal dashed); the hexagon with both
# diagonals; the corner triangle tinted inside the hexagon, then an enlarged cut-out with the dashed height and the values.
# =================================================================================================================
def _corner(cx, cy, R, n, start, top, base, name):
    p = rp(cx, cy, R, n, start); B, A, C = p[0], p[1], p[-1]
    return ([('poly', p, 'ink', 3), ('txt', cx, cy + R + 30, name, 'ink', 22)],
            [('tint', [A, B, C], 'teal'), sg(B, A, 'teal', 5), sg(B, C, 'teal', 5), tk(B, A, 1), tk(B, C, 1), sg(A, C, 'teal', 3, True)],
            [ang(B, A, C, 20, 'orange'), at(B, top, 0, -22, 'orange', 24)],
            [ang(A, B, C, 26, 'teal'), ang(C, A, B, 26, 'teal'), alab(A, B, C, 46, base, 'teal', 18), alab(C, A, B, 46, base, 'teal', 18)])
_c4 = _corner(105, 160, 95, 4, 90, '90°', '45°', 'square')
_c5 = _corner(320, 160, 95, 5, 90, '108°', '36°', 'pentagon')
_c6 = _corner(535, 160, 95, 6, 90, '120°', '30°', 'hexagon')
p109c = PIN(GEO('p109c', [
    ('line', _c4[0]), ('t4', _c4[1]), ('a4', _c4[2] + _c4[3]),
    ('p5', _c5[0]), ('t5', _c5[1]), ('a5', _c5[2] + _c5[3]),
    ('p6', _c6[0]), ('t6', _c6[1]), ('a6', _c6[2] + _c6[3]),
], vb='0 25 640 320', w=580, col=0, title='The corner triangle'))
p109c1 = I('p109c1', 'two equal sides: isosceles', size=34, col=1)
p109c2 = IH('p109c2', '$(180° - 90°) \\div 2 = 45°$', size=34, col=1)
p109c3 = IH('p109c3', '$(180° - 108°) \\div 2 = 36°$', size=34, col=1)
p109c4 = IH('p109c4', '$(180° - 120°) \\div 2 = 30°$', size=34, col=1)

_Ox = (170, 170); _Hx = rp(_Ox[0], _Ox[1], 120, 6, 90)       # A top, B, C, D, E, F counter-clockwise
_nm6 = [nm(p, t, _Ox, 22) for p, t in zip(_Hx, 'ABCDEF')]
p109h = PIN(GEO('p109h', [
    ('line', [('poly', _Hx, 'ink', 3)] + _nm6 + [side_lab(_Hx[0], _Hx[1], 'a', _Ox, 18, 'ink', 24)]),
    ('long', [sg(_Hx[0], _Hx[3], 'orange', 4), ('dot', *_Ox), ('txt', _Ox[0] + 18, _Ox[1] + 4, 'O', 'ink', 22, True)]),
    ('rr', [('txt', _Ox[0] + 16, 110, 'a', 'orange', 24, True), ('txt', _Ox[0] + 16, 232, 'a', 'orange', 24, True)]),
    ('short', [sg(_Hx[0], _Hx[2], 'teal', 4)]),
    ('tri', [('tint', [_Hx[0], _Hx[1], _Hx[2]], 'teal'), ang(_Hx[1], _Hx[0], _Hx[2], 18, 'orange'), at(_Hx[1], '120°', 44, 4, 'orange', 18),
             ang(_Hx[0], _Hx[1], _Hx[2], 34, 'teal'), ang(_Hx[2], _Hx[0], _Hx[1], 34, 'teal')]),
], vb='10 15 320 320', w=520, col=0, title='The diagonals of a regular hexagon'))
p109h1 = I('p109h1', 'long diagonal $= a + a = 2a$', size=34, col=1)

# the cut-out: the corner triangle A B C enlarged, base A C across, B on top
_cA, _cC = (320.0, 260.0), (680.0, 260.0); _ca = 360 / 3 ** 0.5; _cB = (500.0, 260.0 - _ca / 2); _cM = (500.0, 260.0)
_hs6 = rp(130, 170, 80, 6, 90)
p109cut = PIN(GEO('p109cut', [
    ('line', [('poly', _hs6, 'ink', 3), ('tint', [_hs6[0], _hs6[1], _hs6[2]], 'teal'), sg(_hs6[0], _hs6[2], 'teal', 3)]
             + [nm(p, t, (130, 170), 20, 'ink', 24) for p, t in zip(_hs6[:3], 'ABC')]),
    ('big', [('tint', [_cA, _cB, _cC], 'teal'), ('poly', [_cA, _cB, _cC], 'teal', 3), at(_cA, 'A', -18, 4, 'ink', 24, True),
             at(_cC, 'C', 18, 4, 'ink', 24, True), at(_cB, 'B', 0, -22, 'ink', 24, True),
             at(_cA, '30°', 46, -12, 'teal', 18), at(_cC, '30°', -46, -12, 'teal', 18)]),
    ('h', [sg(_cB, _cM, 'orange', 3, True), rt(_cM, _cB, _cC, 11, 'orange'), at(_cB, '60°', -20, 38, 'orange', 18), at(_cB, '60°', 20, 38, 'orange', 18)]),
    ('half', [('tint', [_cA, _cB, _cM], 'orange')]),
    ('sides', [side_lab(_cA, _cB, 'a', _cM, 16, 'ink', 24), at(lerp(_cB, _cM, 0.8), 'a/2', 30, 0, 'orange', 22), at(_cA, '(a/2)√3', 66, 24, 'orange', 22)]),
    ('ac', [at(_cM, 'A C = a√3', 0, 58, 'teal', 26)]),
], vb='30 40 690 320', w=760, col=0, title='The short diagonal of a regular hexagon'))
p109g1 = I('p109g1', 'golden triangle: $x$, $\\ x\\sqrt3$, $\\ 2x$', size=34, col=1)
p109g2 = IH('p109g2', '$AC = 2 \\cdot \\dfrac{a}{2}\\sqrt3 = a\\sqrt3$', size=34, col=1)
p109n1 = IH('p109n1', '$a = 2$: $\\ $long $4$, short $2\\sqrt3$', size=30)
p109n2 = IH('p109n2', '$a = 5$: $\\ $long $10$, short $5\\sqrt3$', size=30)
p109n3 = IH('p109n3', 'short $= 9$: $\\ a = \\dfrac{9}{\\sqrt3} = \\dfrac{9\\sqrt3}{3} = 3\\sqrt3$', size=30)
p109n4 = I('p109n4', 'Regular hexagon: short diagonal $a\\sqrt3$, long diagonal $2a$', size=28)

video('geo-109', 'lesson', slides=[
    S('Advanced Polygons',
      L("Now polygons at a higher level. Most exam questions use the regular pentagon, hexagon and octagon. Inside them "
        "hide a few triangles that come back again and again. Let's get to know them.")),
    S('The corner triangle',
      L("Take a regular polygon, and two sides that meet at one corner. Now join their two far ends. This line is a "
        "diagonal, and it cuts off a triangle at the corner. Let's call it the corner triangle.",
        show(p109c['line'], 'Take a regular polygon'), show(p109c['t4'], 'join their two far ends')),
      L("The two sides are sides of a regular polygon, so they're equal. So the corner triangle is isosceles. Its top "
        "angle is the polygon's angle. And its two base angles are equal, so they share what's left of one hundred eighty.",
        show(p109c1, 'So the corner triangle is isosceles')),
      L("Let's start with a square. The top angle is ninety. One hundred eighty minus ninety is ninety, so each base angle "
        "is forty-five. We know this one. The diagonal of a square makes angles of forty-five.",
        show(p109c['a4'], 'The top angle is ninety'), show(p109c2, 'One hundred eighty minus ninety')),
      L("Now a regular pentagon. The top angle is one hundred eight. One hundred eighty minus one hundred eight is "
        "seventy-two. Half of seventy-two is thirty-six. So each base angle is thirty-six.",
        show(p109c['p5'], 'Now a regular pentagon'), show(p109c['t5'], 'The top angle is one hundred eight'),
        show(p109c['a5'], 'One hundred eighty minus one hundred eight'), show(p109c3, 'Half of seventy-two')),
      L("And a regular hexagon. The top angle is one hundred twenty. One hundred eighty minus one hundred twenty is "
        "sixty. So each base angle is thirty.",
        show(p109c['p6'], 'And a regular hexagon'), show(p109c['t6'], 'The top angle is one hundred twenty'),
        show(p109c['a6'], 'One hundred eighty minus one hundred twenty'), show(p109c4, 'So each base angle is thirty')),
      L("Careful, this works because the two sides are equal. In a polygon that's not regular, the two sides can be "
        "different. So when a diagonal cuts off a corner of a regular polygon, think of an isosceles triangle, and find "
        "its base angles.")),
    S("The hexagon's diagonals",
      L("Now let's look closely at a regular hexagon with side a. It has two kinds of diagonals. A long diagonal goes "
        "through the center. A short diagonal skips just one corner.",
        show(p109h['line'], 'a regular hexagon with side a'), show(p109h['long'], 'A long diagonal'),
        show(p109h['short'], 'A short diagonal')),
      L("The long diagonal is easy. The hexagon is made of six equilateral triangles, so the radius is equal to the side, "
        "a. The long diagonal is two radii. So it's two a.",
        show(p109h['rr'], 'so the radius is equal to the side'), show(p109h1, "So it's two a")),
      L("The short diagonal, A C, closes the corner triangle A B C. Like we just saw, its angles are thirty, thirty and "
        "one hundred twenty.", show(p109h['tri'], 'closes the corner triangle'))),
    S('The short diagonal',
      L("Let's take this triangle out and make it bigger. Now let's drop a height from B to A C. The triangle is "
        "isosceles, so the height cuts it into two equal halves. It cuts the angle of one hundred twenty into sixty and "
        "sixty. And it cuts A C into two equal parts.",
        show(p109cut['line'], "Let's take this triangle out"), show(p109cut['big'], 'make it bigger'),
        show(p109cut['h'], 'drop a height from B')),
      L("Look at one of the two halves. Its angles are thirty, sixty and ninety. So it's a golden triangle. Remember its sides. The "
        "side across from thirty is x, the side across from sixty is x root three, and the hypotenuse is two x.",
        show(p109cut["half"], "Look at one of the two halves"), show(p109g1, 'Remember its sides')),
      L("Here the hypotenuse is A B, the side of the hexagon, a. So the short leg, the height, is a over two. And the "
        "long leg is a over two, times root three. That's half of A C.", show(p109cut['sides'], 'Here the hypotenuse is A B')),
      L("A C is two of these halves. Two times a over two is a, so A C is a root three. The short diagonal is the side "
        "times root three.", show(p109g2, 'A C is two of these halves'), show(p109cut['ac'], 'so A C is a root three'))),
    S('In numbers',
      L("Let's see it in numbers. If the side is two, the long diagonal is two times two, four. And the short diagonal "
        "is two root three.", show(p109n1, 'If the side is two')),
      L("If the side is five, the long diagonal is ten, and the short diagonal is five root three.",
        show(p109n2, 'If the side is five')),
      L("And backwards. If the short diagonal is nine, the side is nine divided by root three. Let's multiply the top "
        "and the bottom by root three. That's nine root three over three, which is three root three.",
        show(p109n3, 'If the short diagonal is nine')),
      L("So when you see a regular hexagon with a diagonal, think of these two. The short diagonal is a root three, and "
        "the long one is two a. Take a moment to memorize this, and I'll see you in the next video.",
        show(p109n4, 'think of these two'))),
])


# =================================================================================================================
# solve-geo34-g110 - a regular pentagon: the angle between two diagonals
# Hebrew geo 5379-5444 (angle alpha = two parts there, the middle part x here): several ways because we can cut a polygon
# into shapes we know; way 1 the triangle (isosceles, 540 / 5 = 108 "know it by heart", base angles 36); way 2 the
# trapezoid ("if you didn't know, now you do": a diagonal of a regular pentagon makes an isosceles trapezoid and a
# triangle; angles on one leg add up to 180); way 3 the diagonals (inscribed angles on equal chords, 3x = 108, 90 + 18).
# R37: the corner triangle is taught in geo-109, the diagonals rule in geo-104 (links). Way 2 here uses BOTH trapezoids
# (R30: it stands alone, it doesn't borrow the 36 from way 1): 72 + 72 = 108 + x.
# V3: the copy; way 1: triangle QRS tinted (RQ, RS ticked), 108 at R, 36 at S, then STP orange with its 36, x = 36
# written; way 2: the trapezoid PQRS tinted with the parallel arrows, 72 at S, then QSTP with its 72, the overlap x;
# way 3: the circle dashed, the three equal arcs, x x x.
# =================================================================================================================
_P0, _Q0, _R0, _S0, _T0 = (320.0, 72.647), (217.901, 146.826), (256.9, 266.85), (383.1, 266.85), (422.099, 146.826)
_c110 = (320.0, 180.0)
def _g110_base(extra=()):
    e = [('poly', [_P0, _Q0, _R0, _S0, _T0], 'ink', 3), sg(_S0, _P0, 'ink', 3), sg(_S0, _Q0, 'ink', 3)]
    e += [nm(p, t, _c110, 26) for p, t in zip([_P0, _Q0, _R0, _S0, _T0], 'PQRST')]
    e += [ang(_S0, _P0, _Q0, 34, 'ink'), alab(_S0, _P0, _Q0, 56, 'x', 'ink', 28)]
    return e + list(extra)
_vb110 = '165 25 310 285'
f110q = PIN(GEO('f110q', [
    ('line', _g110_base()),
    ('x', [ang(_S0, _P0, _Q0, 34, 'red'), alab(_S0, _P0, _Q0, 56, 'x', 'red', 30)]),
], vb=_vb110, w=480, title='The regular pentagon'))
f110a = PIN(GEO('f110a', [
    ('line', _g110_base()),
    ('qrs', [('tint', [_Q0, _R0, _S0], 'teal'), tk(_R0, _Q0), tk(_R0, _S0)]),
    ('r', [ang(_R0, _Q0, _S0, 20, 'orange'), at(_R0, '108°', -46, -16, 'orange', 22)]),
    ('s1', [ang(_S0, _Q0, _R0, 52, 'teal'), alab(_S0, _Q0, _R0, 74, '36°', 'teal', 22)]),
    ('stp', [('tint', [_S0, _T0, _P0], 'orange'), tk(_T0, _S0), tk(_T0, _P0), at(_T0, '108°', -30, 2, 'orange', 22),
             ang(_S0, _T0, _P0, 52, 'orange'), alab(_S0, _T0, _P0, 74, '36°', 'orange', 22)]),
    ('xs', [alab(_S0, _P0, _Q0, 112, 'x = 36°', 'red', 24)]),
], vb=_vb110, w=480, title='Two corner triangles'))
f110b = PIN(GEO('f110b', [
    ('line', _g110_base()),
    ('tz1', [('tint', [_P0, _Q0, _R0, _S0], 'teal'), ('poly', [_P0, _Q0, _R0, _S0], 'teal', 5), ('par', _Q0[0], _Q0[1], _R0[0], _R0[1], 1, 'teal'), ('par', _P0[0], _P0[1], _S0[0], _S0[1], 1, 'teal')]),
    ('a1', [at(_R0, '108°', -46, -16, 'orange', 22), ang(_S0, _R0, _P0, 44, 'teal'), alab(_S0, _R0, _P0, 112, '72°', 'teal', 24)]),
    ('tz2', [('poly', [_Q0, _S0, _T0, _P0], 'orange', 5), ('par', _P0[0], _P0[1], _T0[0], _T0[1], 2, 'orange'), ('par', _Q0[0], _Q0[1], _S0[0], _S0[1], 2, 'orange')]),
    ('a2', [at(_T0, '108°', -30, 2, 'orange', 22), ang(_S0, _Q0, _T0, 58, 'orange'), alab(_S0, _Q0, _T0, 140, '72°', 'orange', 24)]),
], vb=_vb110, w=480, title='Two trapezoids'))
_rc = 107.353
f110c = PIN(GEO('f110c', [
    ('line', _g110_base()),
    ('circ', [('circ', _c110[0], _c110[1], _rc, 'teal', 2.5, True)]),
    ('arcs', [('arcw', _c110[0], _c110[1], _rc, 90 + 0.5, 162 - 0.5, 'orange', 7), ('arcw', _c110[0], _c110[1], _rc, 162 + 0.5, 234 - 0.5, 'teal', 7),
              ('arcw', _c110[0], _c110[1], _rc, 18 + 0.5, 90 - 0.5, 'orange', 7)]),
    ('xxx', [ang(_S0, _R0, _Q0, 40, 'teal'), alab(_S0, _R0, _Q0, 60, 'x', 'teal', 24), ang(_S0, _P0, _T0, 40, 'orange'),
             alab(_S0, _P0, _T0, 60, 'x', 'orange', 24)]),
], vb='180 25 280 300', w=480, title='The pentagon in a circle'))
for _g in (f110q, f110a, f110b, f110c): LEFT(_g, y=QY('g110', 230), x=410, w=480)
f110r1 = IH('f110r1', '$540° \\div 5 = 108°$', size=34)
f110r2 = IH('f110r2', '$180° - 108° = 72°$', size=34)
f110r3 = IH('f110r3', '$72° \\div 2 = 36°$', size=34)
f110r4 = IH('f110r4', '$x = 108° - 36° - 36° = 36°$', size=34)
f110s1 = IH('f110s1', '$\\angle RSP = 180° - 108° = 72°$', size=34)
f110s2 = IH('f110s2', '$\\angle TSQ = 180° - 108° = 72°$', size=34)
f110s3 = IH('f110s3', '$72° + 72° = 144°$', size=34)
f110s4 = IH('f110s4', '$x = 144° - 108° = 36°$', size=34)
f110t1 = IH('f110t1', '$3x = 108°$', size=34)
f110t2 = IH('f110t2', '$90 \\div 3 = 30$, $\\ 18 \\div 3 = 6$', size=34)
f110t3 = IH('f110t3', '$x = 36°$', size=34)
FLOW([f110r1, f110r2, f110r3, f110r4], [(920, 660, 240, 700)])
FLOW([f110s1, f110s2, f110s3, f110s4], [(920, 660, 240, 700)])
FLOW([f110t1, f110t2, f110t3], [(920, 660, 240, 700)])
NOFIG('solve-geo34-g110', 0, 1, 2, 3)

video('solve-geo34-g110', 'solution', qid='geo34-g110', slides=[
    S('The angle between two diagonals',
      L("P Q R S T is a regular pentagon. What is the size of angle P S Q, marked x in the figure?",
        pt('stem', 'P Q R S T is a regular pentagon', 'hl', 6.0), show(f110q['line'], 'P Q R S T'), voice='calm', pause=0.5),
      L("So we want the middle angle at S, between the two diagonals. All we know is that the pentagon is regular. But "
        "inside a regular polygon there are shapes we know, like triangles and trapezoids. So there are several ways in. "
        "We'll solve it in three different ways, all of them the math way.", show(f110q['x'], 'So we want the middle angle'))),
    SM('Method 1 · The math way: corner triangles', 'Two corner triangles',
      L("Let's start with the math way, with corner triangles, like in the lesson. Look at triangle Q R S. R Q and R S "
        "are sides of the regular pentagon, so they're equal. So it's an isosceles triangle.",
        show(f110a['line'], "Let's start with the math way"), show(f110a['qrs'], 'Look at triangle Q R S')),
      L("Its top angle is R, an angle of the regular pentagon. The angles of a pentagon add up to five hundred forty. So "
        "each angle is five hundred forty divided by five, one hundred eight.",
        show(f110r1, 'five hundred forty divided by five'), show(f110a['r'], 'one hundred eight.')),
      L("So the two base angles share one hundred eighty minus one hundred eight, seventy-two. Each one is half of "
        "seventy-two, thirty-six. So angle Q S R is thirty-six.",
        show(f110r2, 'one hundred eighty minus one hundred eight'), show(f110r3, 'Each one is half'),
        show(f110a['s1'], 'So angle Q S R is thirty-six')),
      L("The same happens on the other side, in triangle S T P. T S and T P are equal sides, and the angle at T is one "
        "hundred eight. So angle T S P is thirty-six too.", show(f110a['stp'], 'in triangle S T P')),
      L("The whole angle at S is also one hundred eight. It's made of three parts, thirty-six, x, and thirty-six. So x is "
        "one hundred eight, minus thirty-six, minus thirty-six. That's one hundred eight minus seventy-two, thirty-six. "
        "Choice number three is our answer.",
        show(f110r4, 'So x is'), show(f110a['xs'], 'minus seventy-two, thirty-six'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · The math way: trapezoids', 'Two trapezoids',
      L("Now a second way, the math way with trapezoids. The diagonal S P cuts the pentagon into a triangle and a "
        "quadrilateral, P Q R S. In a regular pentagon, a diagonal is parallel to the side across from it. Here S P is "
        "parallel to Q R. So P Q R S is a trapezoid.",
        show(f110b['line'], 'Now a second way'), show(f110b['tz1'], 'So P Q R S is a trapezoid')),
      L("In a trapezoid, two angles on the same leg add up to one hundred eighty. Look at the leg R S. Angle R is one "
        "hundred eight, because the pentagon is regular. So angle R S P is one hundred eighty minus one hundred eight, "
        "seventy-two.", show(f110b['a1'], 'Look at the leg R S'), show(f110s1, 'So angle R S P is')),
      L("The other diagonal, S Q, does the same on the other side. It's parallel to T P, so Q S T P is a trapezoid too. "
        "Angle T is one hundred eight, so angle T S Q is seventy-two.",
        show(f110b['tz2'], 'The other diagonal, S Q'), show(f110b['a2'], 'Angle T is one hundred eight'), show(f110s2, 'so angle T S Q')),
      L("Now look at the angle at S. Both of these angles of seventy-two include x. Seventy-two plus seventy-two is one "
        "hundred forty-four. That's the whole angle at S, plus x one more time. So x is one hundred forty-four minus one "
        "hundred eight, thirty-six. Choice number three again.",
        show(f110s3, 'Seventy-two plus seventy-two'), show(f110s4, 'So x is one hundred forty-four minus'),
        mk('tick', 'choice 3', 'Choice number three again'))),
    SM('Method 3 · The math way: the diagonals', 'Equal parts',
      L("And a third way, the math way with the diagonals. Remember from the first lesson, the diagonals from one corner "
        "of a regular polygon cut its angle into equal parts. Why? The pentagon fits in a circle. So the small angles at "
        "S are inscribed angles, and they stand on equal arcs, one under each side.",
        show(f110c['line'], 'And a third way'), show(f110c['circ'], 'The pentagon fits in a circle'),
        show(f110c['arcs'], 'they stand on equal arcs')),
      L("From S there are only two diagonals, to Q and to P. S R and S T are sides. So the angle at S is cut into three "
        "equal angles, and each one is x. So three x is one hundred eight.",
        show(f110c['xxx'], 'cut into three equal angles'), show(f110t1, 'So three x is one hundred eight')),
      L("To divide one hundred eight by three, let's split it. Ninety divided by three is thirty, and eighteen divided by "
        "three is six. So x is thirty-six. Choice number three is our answer, and I'll see you in the next question.",
        show(f110t2, 'Ninety divided by three'), show(f110t3, 'So x is thirty-six'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-geo34-g111 - a regular 9-sided polygon in a circle: which statement is not true?
# Hebrew geo 5445-5513 (a pentagon there, a 9-sided polygon here): statement by statement, cross out what is surely true;
# central angles 360 / n; the circle vs the perimeter: the side is the shortest way, the arc a detour ("true for every
# regular polygon in a circle"); BCO = OCD: radius, radius, radius, equal bases -> the same triangles; "symmetry: a radius
# to a corner halves its angle"; in the exam mark it and move on, in a lesson check it: the triangle OCD, the bigger angle
# faces the longer side -> side < r -> P < 9r; "I want to use this question to teach a principle": the hexagon is the
# balance point (6 radii = 6 sides), more sides -> n radii win (2 pi r), fewer sides -> it flips (the pentagon 72 / 54).
# R37 / R29: central angles and radius = side in the hexagon are geo-104 (reminders); "the longer side faces the bigger
# angle" is topic 31 (reminder); the balance principle is a one-off taught here (W20). Pi: "less than three and a half".
# V3: the copy; the two central angles orange with 40; the arc A B thick teal against the side A B orange; triangles OBC,
# OCD tinted with ticks; triangle OCD with 40, 70, 70 and its sides; the hexagon (radius = side) on the last slide.
# =================================================================================================================
_O111 = (320.0, 180.0); _r111 = 107.353
_N9 = [gpt(_O111[0], _O111[1], _r111, 90 + 40 * k) for k in range(9)]    # A, B, C, ... I counter-clockwise
_L9 = 'ABCDEFGHI'
def _g111_base(extra=()):
    e = [('circ', _O111[0], _O111[1], _r111, 'ink', 2.5), ('poly', _N9, 'ink', 3)] + [sg(_O111, p, 'ink', 2) for p in _N9]
    e += [nm(p, t, _O111, 20, 'ink', 26) for p, t in zip(_N9, _L9)] + [('dot', *_O111), ('txt', 338, 194, 'O', 'ink', 26, True)]
    return e + list(extra)
_vb111 = '180 30 280 300'
_A, _B, _C, _D = _N9[0], _N9[1], _N9[2], _N9[3]
_G, _Hh9 = _N9[6], _N9[7]
f111a = PIN(GEO('f111a', [
    ('line', _g111_base()),
    ('cent', [angw(_O111, _A, _B, 40, 'orange'), angw(_O111, _G, _Hh9, 40, 'orange'), alab(_O111, _A, _B, 58, '40°', 'orange', 22),
              alab(_O111, _G, _Hh9, 58, '40°', 'orange', 22)]),
    ('arc', [('arcw', _O111[0], _O111[1], _r111, 90, 130, 'teal', 8), sg(_A, _B, 'orange', 5)]),
], vb=_vb111, w=480, title='The regular 9-sided polygon'))
f111b = PIN(GEO('f111b', [
    ('line', _g111_base()),
    ('two', [('tint', [_O111, _B, _C], 'teal'), ('tint', [_O111, _C, _D], 'orange'), tk(_O111, _B, 1), tk(_O111, _C, 1), tk(_O111, _D, 1),
             tk(_B, _C, 2, 'orange'), tk(_C, _D, 2, 'orange')]),
    ('half', [ang(_C, _B, _O111, 26, 'teal'), ang(_C, _O111, _D, 30, 'orange')]),
], vb=_vb111, w=480, title='Triangles O B C and O C D'))
f111c = PIN(GEO('f111c', [
    ('line', _g111_base()),
    ('ocd', [('tint', [_O111, _C, _D], 'teal'), sg(_C, _D, 'orange', 5)]),
    ('angs', [ang(_O111, _C, _D, 30, 'orange'), alab(_O111, _C, _D, 50, '40°', 'orange', 20),
              ang(_C, _O111, _D, 22, 'teal'), ang(_D, _C, _O111, 22, 'teal'), at(_C, '70°', 44, 6, 'teal', 20), at(_D, '70°', 30, -28, 'teal', 20)]),
], vb=_vb111, w=480, title='Triangle O C D'))
_Oh2 = (170, 160); _Hh2 = rp(_Oh2[0], _Oh2[1], 110, 6, 0)
f111d = PIN(GEO('f111d', [
    ('line', [('poly', _Hh2, 'ink', 3), ('dot', *_Oh2)] + [sg(_Oh2, p, 'teal', 3, True) for p in _Hh2]),
    ('eq', [('tint', [_Oh2, _Hh2[0], _Hh2[1]], 'teal'), side_lab(_Hh2[0], _Hh2[1], 'r', _Oh2, 18, 'teal', 30),
            ('txt', *mid(_Oh2, _Hh2[0], 14, -1), 'r', 'teal', 28, True), ('txt', 170, 300, 'side = radius', 'teal', 28)]),
], vb='40 30 260 290', w=330, title='The regular hexagon'))
for _g in (f111a, f111b, f111c): LEFT(_g, y=QY('g111', 250), x=410, w=320)
LEFT(f111d, y=QY('g111', 240), x=410, w=330)
f111r1 = IH('f111r1', '$360° \\div 9 = 40°$', size=34)
f111r2 = I('f111r2', 'arc $>$ side, for every side', size=30)
f111s1 = I('f111s1', 'matching side lengths: congruent triangles', size=30)
f111t1 = IH('f111t1', '$180° - 40° = 140°$', size=34)
f111t2 = IH('f111t2', '$140° \\div 2 = 70°$', size=34)
f111t3 = I('f111t3', 'side (across $40°$) $<$ radius (across $70°$)', size=28)
f111t4 = IH('f111t4', '$P < 9r$', size=34)
f111u1 = I('f111u1', 'hexagon: $P = 6r$', size=32)
f111u2 = I('f111u2', '7 sides: $P < 2\\pi r < 7r$', size=32)
f111u3 = I('f111u3', 'pentagon: side $>$ $r$, so $P > 5r$', size=30)
f111u4 = I('f111u4', 'more than 6 sides: $P < nr$', size=30)
FLOW([f111r1, f111r2], [(760, 800, 250, 700)])
FLOW([f111s1], [(760, 800, 250, 700)])
FLOW([f111t1, f111t2, f111t3, f111t4], [(760, 800, 250, 700)])
FLOW([f111u1, f111u2, f111u3, f111u4], [(800, 780, 250, 700)])
NOFIG('solve-geo34-g111', 0, 1, 2, 3)

video('solve-geo34-g111', 'solution', qid='geo34-g111', slides=[
    S('Statement by statement',
      L("A regular polygon with nine sides, A B C D E F G H I, is inscribed in a circle with center O and radius r. Which "
        "of the following statements is not true?", pt('stem', 'A regular polygon with nine sides', 'hl', 8.0),
        show(f111a['line'], 'A regular polygon with nine sides'), voice='calm', pause=0.5),
      L("So three of the statements are true, and one is not. We'll go statement by statement. Every statement that is "
        "surely true, we cross out. When three are out, the one that's left is our answer."),
      L("Choice number two says: angle A O B is equal to angle G O H. Both are central angles of the regular polygon. "
        "Like in the lesson, each central angle is three hundred sixty divided by n. Three hundred sixty divided by nine "
        "is forty. So both angles are forty. It's true, so choice number two is out.",
        pt('choice 2', 'Choice number two says'), show(f111a['cent'], 'Both are central angles'),
        show(f111r1, 'Three hundred sixty divided by nine'), mk('cross', 'choice 2', 'so choice number two is out')),
      L("Choice number one says: the circumference of the circle is bigger than the perimeter of the polygon. Here we "
        "don't need to calculate anything. We only need to decide which one is bigger.", pt('choice 1', 'Choice number one says')),
      L("Look at the side A B and the arc A B. The side is a straight line, the shortest way from A to B. The arc goes "
        "around, so it's longer. The same is true for every side and its arc. So the whole circle is longer than all nine "
        "sides together. It's true, so choice number one is out.",
        show(f111a['arc'], 'Look at the side A B'), show(f111r2, 'The same is true for every side'),
        mk('cross', 'choice 1', 'so choice number one is out'))),
    S('Two triangles',
      L("Choice number four says: angle B C O is equal to angle O C D. Look at triangles O B C and O C D. O B, O C and O D "
        "are all radii, so they're equal. And B C and C D are sides of the regular polygon, so they're equal too.",
        pt('choice 4', 'Choice number four says'), show(f111b['line'], 'Look at triangles O B C and O C D'),
        show(f111b['two'], 'are all radii')),
      L("So the two triangles have matching side lengths. They're congruent: the same shape and size. Their matching "
        "angles are equal. Angle B C O "
        "is equal to angle O C D. It's true, so choice number four is out.",
        show(f111s1, 'matching side lengths'), show(f111b['half'], 'Angle B C O'), mk('cross', 'choice 4', 'so choice number four is out')),
      L("So a radius to a corner cuts the corner's angle into two equal halves. It's like the pentagon in the lesson, "
        "where the radius cut one hundred eight into fifty-four and fifty-four."),
      L("Three statements are out. On the exam, you'd mark choice number three and move on. Here, let's see why it's not "
        "true.", pt('choice 3', 'mark choice number three'))),
    S('Why not nine r',
      L("Choice number three says: the perimeter of the polygon is nine r. So we compare nine sides with nine radii. Let's "
        "compare one side with one radius, in triangle O C D.",
        pt('choice 3', 'Choice number three says'), show(f111c['line'], 'So we compare nine sides'), show(f111c['ocd'], 'in triangle O C D')),
      L("The angle at O is a central angle, forty. The two base angles share one hundred eighty minus forty, one hundred "
        "forty. So each one is half of one hundred forty, seventy.",
        show(f111t1, 'one hundred eighty minus forty'), show(f111t2, 'So each one is half'), show(f111c['angs'], 'seventy.')),
      L("Remember from triangles: the longer side is across from the bigger angle. The side C D is across from forty. A "
        "radius, like O C, is across from seventy. So the side is shorter than the radius.",
        show(f111t3, 'The side C D is across from forty')),
      L("One side is shorter than one radius. So nine sides are shorter than nine radii. The perimeter is less than nine "
        "r, not equal to it. So this statement is not true. Choice number three is our answer.",
        show(f111t4, 'The perimeter is less than nine r'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('The hexagon is the balance',
      L("Let's use this question to learn a principle that comes back on the exam. When is the perimeter of a regular "
        "polygon exactly n radii? In the regular hexagon. It's made of six equilateral triangles, so the side is equal to "
        "the radius. Six sides are six radii.",
        show(f111d['line'], 'In the regular hexagon'), show(f111d['eq'], 'so the side is equal to'), show(f111u1, 'Six sides are six radii')),
      L("With more sides, each side gets shorter than the radius. Take seven sides. The whole circle is two pi r. Pi is "
        "less than three and a half, so the circle is less than seven r. And the polygon is shorter than the circle. So "
        "its perimeter is less than seven r.", show(f111u2, 'The whole circle is two pi r')),
      L("With fewer sides, it's the other way around. In a pentagon, the side is across from seventy-two, and the radius "
        "is across from fifty-four. So the side is longer than the radius, and the perimeter is more than five r.",
        show(f111u3, 'In a pentagon')),
      L("So the hexagon is the balance point. With more than six sides, the perimeter is less than n radii. That's our "
        "question, with nine sides. Choice number three is our answer, and I'll see you in the next question.",
        show(f111u4, 'With more than six sides'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-geo34-g112 - a regular hexagon: from the perimeter of triangle ACE to the perimeter of the hexagon
# Hebrew geo 5551-5627 (ACE = 18 there, 42 here): two ways, the math solution and the psychometric one; prove once that
# ACE is equilateral (120, the corner triangles 30 + 30, 120 - 30 - 30 = 60; or by symmetry); the side 6 (14 here); the
# height in the isosceles triangle ABC is also a median and a bisector: 60 / 60, 3 / 3 (7 / 7): a golden triangle, from
# the long leg to the short leg divide by root 3, to the hypotenuse double; times 6. The estimate: the hexagon's perimeter
# > the triangle's (two sides of a triangle > the third); compare each choice with 18 (42) - with whole-number benchmarks
# here (teacher 2026-10-07: no decimal estimates): divide both sides, put the factor into the root (root 48 < root 49,
# root 8 < root 9); the guess: root 3 = golden / equilateral, root 2 = silver / squares; a hexagon -> root 3.
# R37: the corner triangle and the short diagonal a root 3 are taught in geo-109 (links); here applied slowly.
# V3: the copy (ACE bold); method 1: ABC tinted, 120 at B, 30 / 30, then the other corners, 60 at A, C, E, 14 on the sides;
# then ABC as an enlarged cut-out next to the copy, the dashed height, 7 | 7, 60 / 60, the golden half tinted; method 2:
# the corner triangle AFE with AF + FE traced against AE.
# =================================================================================================================
_O112 = (320.0, 180.0); _H12 = rp(_O112[0], _O112[1], 107.353, 6, 90)        # A, B, C, D, E, F
_A2, _B2, _C2, _D2, _E2, _F2 = _H12
def _g112_base(extra=()):
    e = [('poly', _H12, 'ink', 3), ('poly', [_A2, _C2, _E2], 'ink', 4)] + [nm(p, t, _O112, 24, 'ink', 28) for p, t in zip(_H12, 'ABCDEF')]
    return e + list(extra)
_vb112 = '150 25 340 300'
f112q = PIN(GEO('f112q', [('line', _g112_base()), ('ace', [('poly', [_A2, _C2, _E2], 'teal', 6)])], vb=_vb112, w=480, title='The regular hexagon'))
f112a = PIN(GEO('f112a', [
    ('line', _g112_base()),
    ('abc', [('tint', [_A2, _B2, _C2], 'teal'), tk(_B2, _A2), tk(_B2, _C2), ang(_B2, _A2, _C2, 18, 'orange'), at(_B2, '120°', -52, 26, 'orange', 22)]),
    ('b30', [ang(_A2, _B2, _C2, 40, 'teal'), ang(_C2, _A2, _B2, 40, 'teal'), alab(_A2, _B2, _C2, 60, '30°', 'teal', 20), alab(_C2, _A2, _B2, 60, '30°', 'teal', 20)]),
    ('others', [('tint', [_C2, _D2, _E2], 'teal'), ('tint', [_E2, _F2, _A2], 'teal')]),
    ('sixty', [alab(_A2, _C2, _E2, 46, '60°', 'orange', 22), alab(_C2, _E2, _A2, 46, '60°', 'orange', 22), alab(_E2, _A2, _C2, 46, '60°', 'orange', 22)]),
    ('fourteen', [side_lab(_A2, _C2, '14', _O112, -26, 'orange', 26), side_lab(_C2, _E2, '14', _O112, -24, 'orange', 26),
                  side_lab(_E2, _A2, '14', _O112, -26, 'orange', 26)]),
], vb=_vb112, w=480, title='Triangle A C E'))
# the cut-out of A B C, to the right of a small copy
_kA, _kC = (480.0, 270.0), (820.0, 270.0); _ka = 340 / 3 ** 0.5; _kB = (650.0, 270.0 - _ka / 2); _kM = (650.0, 270.0)
f112b = PIN(GEO('f112b', [
    ('line', _g112_base([('tint', [_A2, _B2, _C2], 'teal'), side_lab(_A2, _C2, '14', _O112, -26, 'orange', 26)])),
    ('cut', [('tint', [_kA, _kB, _kC], 'teal'), ('poly', [_kA, _kB, _kC], 'teal', 3), at(_kA, 'A', -20, 6, 'ink', 28, True),
             at(_kC, 'C', 20, 6, 'ink', 28, True), at(_kB, 'B', 0, -24, 'ink', 28, True), at(_kM, '14', 0, 52, 'orange', 26)]),
    ('h', [sg(_kB, _kM, 'orange', 3, True), rt(_kM, _kB, _kC, 11, 'orange'), at(_kM, '7', -85, 24, 'orange', 30), at(_kM, '7', 85, 24, 'orange', 30),
           at(_kB, '60°', -20, 40, 'orange', 18), at(_kB, '60°', 20, 40, 'orange', 18), at(_kA, '30°', 48, -12, 'teal', 20)]),
    ('half', [('tint', [_kA, _kB, _kM], 'orange')]),
    ('vals', [at(lerp(_kB, _kM, 0.8), '7/√3', 42, 0, 'orange', 22), side_lab(_kA, _kB, '14/√3', _kM, 22, 'teal', 24)]),
], vb='150 25 720 310', w=700, title='Triangle A B C, bigger'))
f112c = PIN(GEO('f112c', [
    ('line', _g112_base()),
    ('afe', [('tint', [_E2, _F2, _A2], 'teal'), sg(_A2, _F2, 'orange', 6), sg(_F2, _E2, 'orange', 6), sg(_E2, _A2, 'teal', 6)]),
    ('all', [sg(_A2, _B2, 'orange', 6), sg(_B2, _C2, 'orange', 6), sg(_C2, _D2, 'orange', 6), sg(_D2, _E2, 'orange', 6)]),
], vb=_vb112, w=480, title='The hexagon against the triangle'))
for _g in (f112q, f112a, f112c): LEFT(_g, y=QY('g112', 220), x=410, w=480)
LEFT(f112b, y=QY('g112', 220), x=410, w=520)
f112r1 = IH('f112r1', '$(180° - 120°) \\div 2 = 30°$', size=34)
f112r2 = IH('f112r2', '$120° - 30° - 30° = 60°$', size=34)
f112r3 = IH('f112r3', '$42 \\div 3 = 14$', size=34)
f112s1 = IH('f112s1', '$a\\sqrt3 = 14$', size=34)
f112s2 = IH('f112s2', 'short leg: $\\dfrac{7}{\\sqrt3}$', size=34)
f112s3 = IH('f112s3', '$AB = 2 \\cdot \\dfrac{7}{\\sqrt3} = \\dfrac{14}{\\sqrt3}$', size=34)
f112s4 = IH('f112s4', '$6 \\cdot \\dfrac{14}{\\sqrt3} = \\dfrac{84}{\\sqrt3}$', size=34)
f112s5 = IH('f112s5', '$= \\dfrac{84\\sqrt3}{3} = 28\\sqrt3$', size=34)
f112t1 = IH('f112t1', '$AF + FE > AE$', size=34)
f112t2 = IH('f112t2', 'perimeter $> 42$', size=34)
f112t3 = IH('f112t3', '$24\\sqrt3 \\div 6 = 4\\sqrt3$', size=34)
f112t3b = IH('f112t3b', '$42 \\div 6 = 7$', size=34)
f112t4 = IH('f112t4', '$4\\sqrt3 = \\sqrt{48} < \\sqrt{49} = 7$', size=34)
f112t5 = IH('f112t5', '$24\\sqrt2 < 24\\sqrt3$', size=34)
f112t6 = IH('f112t6', '$28\\sqrt2 \\div 14 = 2\\sqrt2$', size=34)
f112t6b = IH('f112t6b', '$42 \\div 14 = 3$', size=34)
f112t7 = IH('f112t7', '$2\\sqrt2 = \\sqrt8 < \\sqrt9 = 3$', size=34)
f112u1 = I('f112u1', '$\\sqrt3$: golden and equilateral triangles', size=30)
f112u2 = I('f112u2', '$\\sqrt2$: silver triangles and squares', size=30)
FLOW([f112r1, f112r2, f112r3], [(920, 660, 230, 700)])
FLOW([f112s1, f112s2, f112s3], [(950, 310, 230, 700)])
FLOW([f112s4, f112s5], [(1270, 310, 230, 700)])
FLOW([f112t1, f112t2, f112t3, f112t3b, f112t4], [(920, 340, 230, 700)])
FLOW([f112t5, f112t6, f112t6b, f112t7], [(1270, 310, 230, 700)])
FLOW([f112u1, f112u2], [(920, 660, 230, 700)])
NOFIG('solve-geo34-g112', 0, 1, 2, 3, 4)

video('solve-geo34-g112', 'solution', qid='geo34-g112', slides=[
    S('From triangle A C E to the hexagon',
      L("A B C D E F is a regular hexagon. The perimeter of triangle A C E is forty-two. What is the perimeter of the "
        "hexagon?", pt('stem', 'A B C D E F is a regular hexagon', 'hl', 6.0), show(f112q['line'], 'A B C D E F'),
        voice='calm', pause=0.5),
      L("So we know the triangle made of three short diagonals, and we need the hexagon. We'll solve it in two different "
        "ways, the math way, and then with an estimate.", show(f112q['ace'], 'the triangle made of three short diagonals'))),
    SM('Method 1 · The math way: the short diagonal', 'A C E is equilateral',
      L("Let's start with the math way. First, let's see that triangle A C E is equilateral. Look at triangle A B C. Like "
        "in the lesson, it's a corner triangle. B A and B C are sides of the hexagon, so they're equal. And the angle at "
        "B is one hundred twenty. So the base angles are thirty each.",
        show(f112a['line'], "Let's start with the math way"), show(f112a['abc'], 'Look at triangle A B C'),
        show(f112r1, 'So the base angles are thirty'), show(f112a['b30'], 'thirty each.')),
      L("The same is true at the other two corners, in triangles C D E and E F A. So at A, the angle of one hundred twenty "
        "loses thirty and thirty. One hundred twenty minus thirty minus thirty is sixty. The same at C and at E. A "
        "triangle with three angles of sixty is equilateral.",
        show(f112a['others'], 'The same is true at the other two corners'), show(f112r2, 'One hundred twenty minus thirty'),
        show(f112a['sixty'], 'The same at C and at E')),
      L("So its three sides are equal. The perimeter is forty-two, so each side is forty-two divided by three, fourteen. "
        "So A C is fourteen.", show(f112r3, 'forty-two divided by three'), show(f112a['fourteen'], 'So A C is fourteen'))),
    SM('Method 1 · The math way: the short diagonal', 'From the diagonal to the side',
      L("Now from the diagonal to the side. Like in the lesson, the short diagonal is the side times root three. So the "
        "side a, times root three, is fourteen.", show(f112b['line'], 'Now from the diagonal to the side'),
        show(f112s1, 'So the side a, times root three')),
      L("Let's see it again in triangle A B C, bigger. The height from B cuts A C into seven and seven. It also cuts the "
        "angle of one hundred twenty into sixty and sixty. So each half is a golden triangle, thirty, sixty, ninety.",
        show(f112b['cut'], "Let's see it again in triangle A B C"), show(f112b['h'], 'The height from B'),
        show(f112b['half'], 'So each half is a golden triangle')),
      L("Seven is across from sixty, so it's the long leg. To get the short leg, we divide by root three. So the short leg "
        "is seven over root three. The hypotenuse is twice the short leg, fourteen over root three. That's A B, the side "
        "of the hexagon.", show(f112s2, 'we divide by root three'), show(f112s3, 'The hypotenuse is twice'),
        show(f112b['vals'], "That's A B, the side")),
      L("The hexagon has six sides. Six times fourteen over root three is eighty-four over root three. Let's multiply the "
        "top and the bottom by root three. That's eighty-four root three over three. Eighty-four divided by three is "
        "twenty-eight. So the perimeter is twenty-eight root three. Choice number two is our answer.",
        show(f112s4, 'Six times fourteen over root three'), show(f112s5, "That's eighty-four root three over three"),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · Estimation', 'An estimate',
      L("Now let's estimate. The perimeter of the hexagon must be bigger than forty-two. Why? Look at triangle A F E. Two "
        "sides of a triangle together are longer than the third side. So A F plus F E is longer than A E.",
        show(f112c['line'], "Now let's estimate"), show(f112c['afe'], 'Look at triangle A F E'), show(f112t1, 'So A F plus F E')),
      L("The same is true in the other two corner triangles. So the six sides of the hexagon are longer than the three "
        "sides of A C E. The perimeter is more than forty-two.", show(f112c['all'], 'The same is true in the other two'),
        show(f112t2, 'The perimeter is more than forty-two')),
      L("Now let's compare each choice with forty-two, with whole numbers. Choice number three says twenty-four root three. "
        "Let's divide both by six. Twenty-four root three becomes four root three, and forty-two becomes seven.",
        pt('choice 3', 'Choice number three says'), show(f112t3, 'Let\'s divide both by six'), show(f112t3b, 'and forty-two becomes seven')),
      L("Four root three is the root of sixteen times three, the root of forty-eight. Seven is the root of forty-nine. "
        "Forty-eight is less than forty-nine, so twenty-four root three is less than forty-two. Choice number three is out.",
        show(f112t4, 'Four root three is the root'), mk('cross', 'choice 3', 'Choice number three is out')),
      L("Choice number one says twenty-four root two. That's even smaller, because root two is less than root three. So "
        "it's out too.", show(f112t5, "That's even smaller"), mk('cross', 'choice 1', "So it's out too")),
      L("Choice number four says twenty-eight root two. Let's divide both by fourteen. That's two root two against three. "
        "Two root two is the root of eight, and three is the root of nine. So it's less than forty-two, and it's out. Only "
        "choice number two is left. Choice number two is our answer.",
        show(f112t6, "Let's divide both by fourteen"), show(f112t6b, "That's two root two against three"), show(f112t7, 'Two root two is the root of eight'),
        mk('cross', 'choice 4', "and it's out"), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Out of time? Guess smart',
      L("One more idea, for when you have no time and must guess. Two choices have root three, and two have root two. "
        "Root three usually comes from golden triangles and equilateral triangles. Root two usually comes from silver "
        "triangles and squares.", show(f112u1, 'Root three usually comes from'), show(f112u2, 'Root two usually comes from')),
      L("A regular hexagon is built from equilateral triangles. So if you must guess, guess a choice with root three. "
        "Here the full solution gave choice number two, and I'll see you in the next question.",
        pt('choice 2', 'gave choice number two'))),
])


# =================================================================================================================
# geo-112-after (lesson) - Two Hexagon Partitions
# Hebrew geo 5628-5684: "I want to use this question to talk about this partition": the standard partition (6 equilateral
# triangles, each 1/6); three rhombi (congruent; the short diagonal -> two equilateral triangles); the long diagonals -> the
# "Haman's ear" partition (an equilateral triangle in the middle and three outside), all the outside triangles congruent;
# the link: the corner triangle is not equilateral but is ALSO 1/6 (each diagonal halves the rhombus); so its area is
# a^2 root 3 / 4. Kept from the English lesson: "the star partition", the cookie with three corners (the teacher restored
# the hamantasch line, 2026-09-27). R37 additions on numbers: side 4: an equilateral triangle 4 root 3 = a corner triangle
# found with the golden halves (base 4 root 3, height 2); the hexagon 24 root 3, ACE half of it, 12 root 3.
# Visuals: the hexagon three times, built at her words: the six triangles; the three rhombi (one tinted, its short
# diagonal); the long diagonals with the star; one rhombus enlarged with both diagonals, the two halves tinted.
# =================================================================================================================
_Oa = (150, 160); _Ha = rp(_Oa[0], _Oa[1], 115, 6, 90)              # A top, B, C, D, E, F
_Ob = (450, 160); _Hb = rp(_Ob[0], _Ob[1], 115, 6, 90)
p112std = PIN(GEO('p112std', [
    ('line', [('poly', _Ha, 'ink', 3)] + [sg(_Ha[k], _Ha[k + 3], 'teal', 3, True) for k in range(3)]),
    ('t', [('tint', [_Oa, _Ha[k], _Ha[(k + 1) % 6]], 'teal' if k % 2 else 'orange') for k in range(6)]
          + [('txt',) + tuple(cen([_Oa, _Ha[k], _Ha[(k + 1) % 6]])) + ('1/6', 'ink', 18) for k in range(6)]),
    ('rh', [('poly', _Hb, 'ink', 3), sg(_Ob, _Hb[0], 'ink', 3), sg(_Ob, _Hb[2], 'ink', 3), sg(_Ob, _Hb[4], 'ink', 3),
            ('tint', [_Ob, _Hb[0], _Hb[1], _Hb[2]], 'teal'), ('tint', [_Ob, _Hb[4], _Hb[5], _Hb[0]], 'orange')]),
    ('short', [sg(_Ob, _Hb[1], 'teal', 3, True), sg(_Ob, _Hb[5], 'orange', 3, True), sg(_Ob, _Hb[3], 'ink', 3, True)]),
], vb='20 30 560 260', w=900, col=0, title='Six triangles and three rhombi'))

p112star = PIN(GEO('p112star', [
    ('line', [('poly', _Ha, 'ink', 3), sg(_Oa, _Ha[0], 'ink', 3), sg(_Oa, _Ha[2], 'ink', 3), sg(_Oa, _Ha[4], 'ink', 3)]
             + [nm(p, t, _Oa, 22, 'ink', 24) for p, t in zip(_Ha, 'ABCDEF')]),
    ('long', [sg(_Ha[0], _Ha[2], 'teal', 4), sg(_Ha[2], _Ha[4], 'teal', 4), sg(_Ha[4], _Ha[0], 'teal', 4)]),
    ('star', [('tint', [_Ha[0], _Ha[1], _Ha[2]], 'orange'), ('tint', [_Ha[2], _Ha[3], _Ha[4]], 'orange'), ('tint', [_Ha[4], _Ha[5], _Ha[0]], 'orange'),
              ('tint', [_Ha[0], _Ha[2], _Ha[4]], 'teal')]),
    ('ang', [at(_Ha[1], '120°', 40, 2, 'orange', 20), at(_Ha[0], '30°', -14, 44, 'orange', 18), at(_Ha[2], '30°', 26, -26, 'orange', 18)]),
], vb='0 10 300 300', w=520, col=0, title='The star partition'))

# one rhombus, enlarged, with both diagonals
_rO, _rP, _rQ, _rR = (120.0, 200.0), (220.0, 200.0 - 100 * 3 ** 0.5), (320.0, 200.0), (220.0, 200.0 + 0.0)
_rB = (120.0 + 200.0, 200.0)
_Rh = [(80, 230), (230, 230), (305, 100), (155, 100)]      # side 150, angles 60 / 120
_Rh = [(80, 230), (230, 230), (230 + 75, 230 - 75 * 3 ** 0.5), (80 + 75, 230 - 75 * 3 ** 0.5)]
_Rh2 = [(p[0] + 300, p[1]) for p in _Rh]
p112rh = PIN(GEO('p112rh', [
    ('line', [('poly', _Rh, 'ink', 3), ('poly', _Rh2, 'ink', 3)]),
    ('sh', [sg(_Rh[1], _Rh[3], 'teal', 3, True), ('tint', [_Rh[0], _Rh[1], _Rh[3]], 'teal'), ('txt', 190, 268, 'two equilateral', 'teal', 20)]),
    ('lg', [sg(_Rh2[0], _Rh2[2], 'orange', 3, True), ('tint', [_Rh2[0], _Rh2[1], _Rh2[2]], 'orange'), ('txt', 490, 268, 'two corner triangles', 'orange', 20)]),
], vb='60 70 560 220', w=900, col=0, title='One rhombus, two ways'))
p112r1 = I('p112r1', 'each half of the rhombus $= \\dfrac16$ of the hexagon', size=34)

p112n1 = I('p112n1', 'corner triangle $= \\dfrac{a^2\\sqrt3}{4}$', size=34, col=1)
p112n2 = IH('p112n2', '$a = 4$: $\\ \\dfrac{16\\sqrt3}{4} = 4\\sqrt3$', size=34, col=1)
p112n3 = IH('p112n3', 'check: $\\dfrac{4\\sqrt3 \\cdot 2}{2} = 4\\sqrt3$', size=34, col=1)
p112n4 = I('p112n4', '3 corner triangles $= \\dfrac36 = \\dfrac12$', size=34, col=1)
p112n5 = I('p112n5', 'triangle $ACE$ $= \\dfrac12$ of the hexagon', size=34, col=1)

video('geo-112-after', 'lesson', slides=[
    S('Two Hexagon Partitions',
      L("Let's use the last question to look at another way to cut a regular hexagon. We know one way already. The "
        "question showed us a different one. Let's explore it.")),
    S('Six triangles, three rhombi',
      L("Here's the way we know. A regular hexagon is cut into six equilateral triangles. All six are equal, so each one "
        "is exactly one sixth of the hexagon.", show(p112std['line'], "Here's the way we know"), show(p112std['t'], 'All six are equal')),
      L("Now another way to cut it, into three rhombi. A rhombus has four equal sides. The three rhombi are the same.",
        show(p112std['rh'], 'into three rhombi')),
      L("If we draw the short diagonal in each rhombus, we get two equilateral triangles in each one. That's the way we "
        "know again.", show(p112std['short'], 'the short diagonal'))),
    S('The star partition',
      L("But now let's draw the long diagonals of the rhombi. We get the cut from the question. An equilateral triangle "
        "in the middle, A C E, and three triangles around it.",
        show(p112star['line'], 'the long diagonals'), show(p112star['long'], 'An equilateral triangle in the middle')),
      L("We call it the star partition. Fold the three corners in, and you get a cookie with three corners, called a "
        "hamantasch, or Haman's ear. The three outside triangles are all the same.", show(p112star['star'], 'We call it the star partition')),
      L("But each outside triangle is not equilateral. Its angles are thirty, thirty and one hundred twenty. So how big "
        "is it, compared with one triangle of the first cut?", show(p112star['ang'], 'Its angles are thirty'))),
    S('Each one is a sixth',
      L("Let's look at one rhombus. The short diagonal cuts it into two equilateral triangles. Each one is half of the "
        "rhombus.", show(p112rh['line'], "Let's look at one rhombus"), show(p112rh['sh'], 'The short diagonal')),
      L("The long diagonal cuts the same rhombus into two corner triangles. Each one is also half of the rhombus. So a "
        "corner triangle has the same area as an equilateral triangle. It's one sixth of the hexagon too.",
        show(p112rh['lg'], 'The long diagonal'), show(p112r1, "It's one sixth of the hexagon too"))),
    S('Use the formula',
      L("So we can find the area of a corner triangle with the formula of an equilateral triangle, a squared root three "
        "over four. a is the side of the hexagon. And this works even though the corner triangle is not equilateral.",
        show(p112n1, 'with the formula of an equilateral triangle')),
      L("Let's check it in numbers. Take a hexagon with side four. The formula gives sixteen root three over four, which "
        "is four root three.", show(p112n2, 'Take a hexagon with side four')),
      L("Now let's find it the long way. The corner triangle's base is the short diagonal, four root three. Its height is "
        "half the side, two, from the golden triangle. So the area is four root three times two, divided by two. That's "
        "four root three again.", show(p112n3, 'Now let\'s find it the long way')),
      L("And three corner triangles are three sixths, which is half of the hexagon. So triangle A C E in the middle is "
        "the other half. When a question shows this star, think in sixths and halves. Take a moment to memorize this, "
        "and I'll see you in the next video.", show(p112n4, 'three sixths'), show(p112n5, 'triangle A C E in the middle'))),
])


# =================================================================================================================
# solve-geo34-g112-area - the three corner triangles of a hexagon with side 10
# Hebrew geo 5685-5699 (side 2 there, 10 here): the full way (a height, 30 / 60 / 90, the base, the height from the golden
# triangle, base x height / 2, times 3) vs the understanding way (each is 1/6 = an equilateral triangle with the same side;
# 3 x a^2 root 3 / 4). R37: the 1/6 fact is taught in geo-112-after (link). Traps: 25 root 3 (one triangle), 150 root 3
# (the whole hexagon).
# V3: the copy (the three shaded triangles); method 1: ABC with the dashed height, the golden half tinted, 5 and 5 root 3;
# method 2: each shaded triangle tinted orange with 1/6, the middle teal with 1/2.
# =================================================================================================================
def _g112a_base(extra=()):
    e = [('tint', [_A2, _B2, _C2], 'ink'), ('tint', [_C2, _D2, _E2], 'ink'), ('tint', [_E2, _F2, _A2], 'ink'),
         ('poly', _H12, 'ink', 3), ('poly', [_A2, _C2, _E2], 'ink', 3)] + [nm(p, t, _O112, 24, 'ink', 28) for p, t in zip(_H12, 'ABCDEF')]
    return e + list(extra)
_M12 = mid(_A2, _C2)
f112ar = PIN(GEO('f112ar', [
    ('line', _g112a_base([side_lab(_A2, _B2, '10', _O112, 20, 'ink', 26)])),
    ('h', [sg(_B2, _M12, 'orange', 3, True), rt(_M12, _B2, _C2, 10, 'orange'), at(_B2, '120°', -52, 26, 'orange', 22)]),
    ('half', [('tint', [_A2, _B2, _M12], 'orange')]),
    ('heightvalue', [at(mid(_B2, _M12), '5', 20, 6, 'orange', 26)]),
    ('base', [side_lab(_A2, _C2, '10√3', _O112, -32, 'teal', 24)]),
], vb='150 25 340 300', w=480, title='The hexagon with side 10'))
f112as = PIN(GEO('f112as', [
    ('line', _g112a_base()),
    ('six', [('tint', [_A2, _B2, _C2], 'orange'), ('tint', [_C2, _D2, _E2], 'orange'), ('tint', [_E2, _F2, _A2], 'orange')]
            + [('txt',) + tuple(cen(t)) + ('1/6', 'orange', 22) for t in ([_A2, _B2, _C2], [_C2, _D2, _E2], [_E2, _F2, _A2])]),
    ('half', [('tint', [_A2, _C2, _E2], 'teal'), ('txt', *_O112, '1/2', 'teal', 28)]),
], vb='150 25 340 300', w=480, title='Each shaded triangle is one sixth'))
for _g in (f112ar, f112as): LEFT(_g, y=QY('g112-area', 220), x=410, w=480)
f112a1 = IH('f112a1', 'height: $10 \\div 2 = 5$', size=34)
f112a2 = IH('f112a2', 'half base: $5\\sqrt3$, $\\ $ base: $10\\sqrt3$', size=34)
f112a3 = IH('f112a3', '$\\dfrac{10\\sqrt3 \\cdot 5}{2} = 25\\sqrt3$', size=34)
f112a4 = IH('f112a4', '$3 \\cdot 25\\sqrt3 = 75\\sqrt3$', size=34)
f112b1 = IH('f112b1', '$3 \\cdot \\dfrac{10^2\\sqrt3}{4}$', size=34)
f112b2 = IH('f112b2', '$= 3 \\cdot 25\\sqrt3 = 75\\sqrt3$', size=34)
FLOW([f112a1, f112a2, f112a3, f112a4], [(920, 660, 230, 700)])
FLOW([f112b1, f112b2], [(920, 660, 230, 700)])
NOFIG('solve-geo34-g112-area', 0, 1)

video('solve-geo34-g112-area', 'solution', qid='geo34-g112-area', slides=[
    SM('Method 1 · The math way: a golden triangle', 'The long way',
      L("A B C D E F is a regular hexagon with side ten. What is the sum of the areas of triangles A B C, C D E and E F A?",
        pt('stem', 'A B C D E F is a regular hexagon', 'hl', 6.0), show(f112ar['line'], 'A B C D E F'), voice='calm', pause=0.5),
      L("So we need the three shaded corner triangles together. We'll solve it in two different ways, the long math way, "
        "and then by understanding."),
      L("Let's start with the math way. Look at triangle A B C. Its sides B A and B C are ten, and its top angle is one "
        "hundred twenty. Let's drop the height from B. It cuts the triangle into two golden triangles, thirty, sixty, "
        "ninety, with hypotenuse ten.",
        show(f112ar['h'], 'Let\'s drop the height from B'), show(f112ar['half'], 'two golden triangles')),
      L("The short leg, across from thirty, is half the hypotenuse. Ten divided by two is five. That's the height. The "
        "long leg is five root three. That's half of the base, so the base A C is ten root three.",
        show(f112a1, 'Ten divided by two is five'), show(f112ar['heightvalue'], 'Ten divided by two is five'),
        show(f112a2, 'The long leg is five root three'), show(f112ar['base'], 'so the base A C')),
      L("So the area of A B C is the base, ten root three, times the height, five, divided by two. Ten times five is "
        "fifty, and half of that is twenty-five. So it's twenty-five root three. Careful, that's choice number one, but "
        "it's only one triangle.", show(f112a3, 'Ten times five is fifty'), mk('cross', 'choice 1', "that's choice number one")),
      L("There are three triangles. Three times twenty-five root three is seventy-five root three. Choice number three is "
        "our answer. It works, but it's long.", show(f112a4, 'Three times twenty-five'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Understanding', 'Each one is a sixth',
      L("Now by understanding. Like in the lesson, this is the star partition. Each shaded corner triangle is one sixth "
        "of the hexagon. So its area is the same as an equilateral triangle with side ten.",
        show(f112as['line'], 'Now by understanding'), show(f112as['six'], 'Each shaded corner triangle')),
      L("So the shaded area is three times ten squared root three over four. Ten squared is one hundred, and one hundred "
        "divided by four is twenty-five. Three times twenty-five root three is seventy-five root three.",
        show(f112b1, 'three times ten squared'), show(f112b2, 'Three times twenty-five root three')),
      L("And it makes sense. Three sixths is half of the hexagon, and A C E is the other half. The whole hexagon would be "
        "one hundred fifty root three, choice number two, so that's a trap. No heights, no golden triangles. Choice "
        "number three is our answer, and I'll see you in the next question.",
        show(f112as['half'], 'Three sixths is half of the hexagon'), mk('cross', 'choice 2', 'choice number two, so'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-geo34-g113 - five squares on a regular hexagon: perimeters and areas
# Hebrew geo 5701-5761 (3 squares and "twice" there; 5 squares and "3 times" here): two ways, plugging in numbers (a
# number instead of x: the side 2 there, 1 here) and geometric understanding; Ella first, cross out two choices ("if we're
# out of time, at least we doubled our chances"); the hexagon = six equilateral triangles; compare without calculating
# (root 3 < 2); understanding: count the sides; Adam: cut the hexagon into three rhombi, a rhombus vs a square with the
# same sides (squeeze the angle, the opening shrinks; the square uses its sides best). R15: the number 1 with its reason.
# The "why" of square > rhombus is said with base x height (the leaning side makes a shorter height).
# V3: the copy (squares grey); method 1: one square with 1 on its sides, the hexagon's six triangles; method 2: the three
# rhombi tinted, then a square and a rhombus with the same side, the dashed height shorter than the side.
# =================================================================================================================
_O113 = (320.0, 180.0); _V = rp(_O113[0], _O113[1], 60.8, 6, 0)
def _sq_on(P, Q):
    """the square built outside the hexagon on side P-Q"""
    dx, dy = Q[0] - P[0], Q[1] - P[1]; L = _pm.hypot(dx, dy); nx, ny = dy / L, -dx / L
    m = mid(P, Q)
    if (m[0] + nx - _O113[0]) ** 2 + (m[1] + ny - _O113[1]) ** 2 < (m[0] - _O113[0]) ** 2 + (m[1] - _O113[1]) ** 2: nx, ny = -nx, -ny
    return [P, Q, (Q[0] + nx * L, Q[1] + ny * L), (P[0] + nx * L, P[1] + ny * L)]
_SQ = [_sq_on(_V[k], _V[k + 1]) for k in range(5)]
def _g113_base(extra=()):
    e = [x for s in _SQ for x in (('tint', s, 'ink'), ('poly', s, 'ink', 3))] + [('poly', _V, 'ink', 3)]
    return e + list(extra)
_vb113 = '180 45 280 270'
f113a = PIN(GEO('f113a', [
    ('line', _g113_base()),
    ('one', [('tint', _SQ[1], 'teal'), ('poly', _SQ[1], 'teal', 4), side_lab(_SQ[1][2], _SQ[1][3], '1', _O113, 14, 'teal', 26)]),
    ('hex', [('tint', [_O113, _V[k], _V[(k + 1) % 6]], 'orange' if k % 2 else 'teal') for k in range(6)]
            + [sg(_V[k], _V[k + 3], 'teal', 2.5, True) for k in range(3)]),
], vb=_vb113, w=480, title='Five squares on a regular hexagon'))
f113q = PIN(GEO('f113q', [('line', _g113_base())], vb=_vb113, w=480, title='Five squares on a regular hexagon'))
f113b = PIN(GEO('f113b', [
    ('line', _g113_base()),
    ('rh', [sg(_O113, _V[0], 'ink', 3), sg(_O113, _V[2], 'ink', 3), sg(_O113, _V[4], 'ink', 3),
            ('tint', [_O113, _V[0], _V[1], _V[2]], 'teal'), ('tint', [_O113, _V[2], _V[3], _V[4]], 'orange'), ('tint', [_O113, _V[4], _V[5], _V[0]], 'teal')]),
], vb=_vb113, w=480, title='Three rhombi'))
_S1 = [(60, 260), (200, 260), (200, 120), (60, 120)]
_R1 = [(280, 260), (420, 260), (420 + 140 * 0.5, 260 - 140 * 0.866), (280 + 140 * 0.5, 260 - 140 * 0.866)]
f113c = PIN(GEO('f113c', [
    ('line', [('tint', _S1, 'ink'), ('poly', _S1, 'ink', 3), rt(_S1[0], _S1[1], _S1[3], 12, 'ink'), ('txt', 130, 290, 'square', 'ink', 24),
              ('poly', _R1, 'ink', 3), ('txt', 385, 290, 'rhombus', 'ink', 24)] + ticks(_S1) + ticks(_R1)),
    ('h', [sg(_S1[1], _S1[2], 'teal', 6), ('txt', 222, 190, 'height', 'teal', 20),
           sg(_R1[3], (_R1[3][0], 260), 'orange', 3, True), rt((_R1[3][0], 260), _R1[3], _R1[1], 10, 'orange'),
           ('txt', _R1[3][0] - 34, 200, 'height', 'orange', 20)]),
], vb='30 80 520 230', w=520, title='The same side: a square and a rhombus'))
LEFT(f113a, y=QY('g113', 330), x=410, w=430)
LEFT(f113q, y=QY('g113', 330), x=410, w=430)
LEFT(f113b, y=QY('g113', 330), x=410, w=330)
LEFT(f113c, y=QY('g113', 340), x=760, w=400)
f113r1 = IH('f113r1', 'squares: $5 \\cdot 4 = 20$', size=34)
f113r2 = IH('f113r2', 'hexagon: $6 \\cdot 1 = 6$', size=34)
f113r3 = IH('f113r3', '$3 \\cdot 6 = 18$, not $20$', size=34)
f113r4 = IH('f113r4', 'squares: $5 \\cdot 1 = 5$', size=34)
f113r5 = IH('f113r5', 'hexagon: $6 \\cdot \\dfrac{\\sqrt3}{4} = \\dfrac{3\\sqrt3}{2}$', size=34)
f113r6 = IH('f113r6', '$\\dfrac{3\\sqrt3}{2} < \\dfrac{3 \\cdot 2}{2} = 3 < 5$', size=34)
f113s1 = IH('f113s1', '$5 \\cdot 4 = 20$, $\\ 3 \\cdot 6 = 18$', size=32)
f113s2 = I('f113s2', 'same side: square $>$ rhombus', size=30)
f113s3 = I('f113s3', '3 squares $>$ 3 rhombi $=$ the hexagon', size=28)
FLOW([f113r1, f113r2, f113r3], [(860, 360, 330, 700)])
FLOW([f113r4, f113r5, f113r6], [(1250, 330, 330, 700)])
FLOW([f113s1, f113s2, f113s3], [(1180, 400, 330, 700)])
NOFIG('solve-geo34-g113', 0, 1, 2)

video('solve-geo34-g113', 'solution', qid='geo34-g113', slides=[
    S('Ella and Adam',
      L("Five squares are built outside a regular hexagon, on five of its sides. Ella says that the five squares together "
        "have a perimeter three times the hexagon's perimeter. Adam says that the five squares together have a bigger "
        "area than the hexagon. Which of the following is true?", pt('stem', 'Five squares are built', 'hl', 12.0),
        show(f113q['line'], 'Five squares are built'), voice='calm', pause=0.5),
      L("So we check each person on their own. We'll solve it in two different ways, by plugging in numbers, and then "
        "by understanding.")),
    SM('Method 1 · Plugging in numbers', 'A side of one',
      L("Let's plug in numbers. Each square is built on a side of the hexagon, so the square's side is the hexagon's "
        "side. The claims only compare the shapes with each other, so any side works. Let's take the easiest one, a "
        "side of one.", show(f113a['line'], "Let's plug in numbers"), show(f113a['one'], 'a side of one')),
      L("Ella first. One square has four sides of one, so its perimeter is four. Five squares are five times four, "
        "twenty. The hexagon has six sides of one, so its perimeter is six.",
        show(f113r1, 'Five squares are five times four'), show(f113r2, 'The hexagon has six sides')),
      L("Ella says the squares are three times the hexagon. Three times six is eighteen, not twenty. So Ella is wrong. "
        "Choice number one, only Ella, is out. And choice number two, both, is out too. If we run out of time now, we "
        "already have only two choices left.", show(f113r3, 'Three times six is eighteen'),
        mk('cross', 'choice 1', 'Choice number one, only Ella'), mk('cross', 'choice 2', 'choice number two, both')),
      L("Now Adam. One square has area one times one, one. So five squares make five.", show(f113r4, 'five squares make five')),
      L("The hexagon is six equilateral triangles with side one. One triangle is one squared, times root three, over "
        "four. That's root three over four. Six of them are six root three over four, which is three root three over two.",
        show(f113a['hex'], 'six equilateral triangles'), show(f113r5, 'Six of them')),
      L("Is that more or less than five? We don't need the exact number. Root three is less than two. So three root three "
        "over two is less than three times two over two, which is three. And three is less than five. So the squares "
        "have the bigger area, and Adam is right. Only Adam is right. Choice number four is our answer.",
        show(f113r6, 'Root three is less than two'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    SM('Method 2 · Understanding', 'Count, then compare',
      L("Now by understanding. Ella first. We don't need numbers. We just count sides, because all the sides here have "
        "the same length. Five squares have five times four, twenty sides. The hexagon has six. Three times six is "
        "eighteen, not twenty. So Ella is wrong.", show(f113b['line'], 'Now by understanding'), show(f113s1, 'Five squares have')),
      L("Adam is the harder part. Let's cut the hexagon into three rhombi, like in the lesson about the two partitions. Now let's compare one "
        "rhombus with one square.", show(f113b['rh'], 'into three rhombi')),
      L("They have the same side. In the square, every angle is ninety. In the rhombus, the angles are not ninety, so "
        "the rhombus leans.", show(f113c['line'], 'They have the same side')),
      L("The area of each one is a base times a height. In the square, the height is the whole side. In the rhombus, the "
        "side leans, so the height is shorter than the side. So with the same side, the square always has more area.",
        show(f113c['h'], 'In the square, the height'), show(f113s2, 'the square always has more area')),
      L("So three squares are already bigger than the three rhombi, the whole hexagon. And we have five squares. So Adam "
        "is right, and Ella is wrong. Choice number four is our answer, and I'll see you in the next question.",
        show(f113s3, 'So three squares are already bigger'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
])


# =================================================================================================================
# solve-geo34-g114 - a regular octagon: Sara and Ben compare segments
# Hebrew geo 5763-5822 (Hillel / Naomi there; Sara / Ben, K L M N T here): two ways, the math way with numbers instead of x
# and the psychometric way (estimation + knowing the octagon); first always the octagon cut (a square, four silver
# triangles = the square, four rectangles; "draw it when it's not drawn"); plug in AE = 1 (KT here), not the side (we'd
# divide by root 2; we prefer to multiply); the hypotenuse root 2 = every side; Hillel wrong (1 + root 2 vs 2; here Sara is
# RIGHT); cross out; Naomi: 2 + root 2 both. Understanding: one leg cancels; the rest: the square's side against a leg
# (her "measure with your fingers" replaced in 2026-09 by the reason: the hypotenuse is the longest side); Ben: which piece
# cancels which. R37: the octagon cut is taught in geo-105 (link). R15: the number 1 with its reason (multiply, not divide).
# V3: the copy; the two missing cut lines dashed teal, the corner triangle KMT tinted; method 1: values 1, 1, root 2 written,
# LT traced teal with root 2 + 1, MN traced orange; method 2: matching pieces in the same colours, the cancelled ones red.
# =================================================================================================================
_Q8 = [(277.238, 76.762), (362.762, 76.762), (423.238, 137.238), (423.238, 222.762), (362.762, 283.238), (277.238, 283.238),
       (216.762, 222.762), (216.762, 137.238)]
_K, _L, _M, _N = _Q8[0], _Q8[5], _Q8[7], _Q8[2]
_T = (277.238, 137.238); _U = (277.238, 222.762); _W = (362.762, 137.238); _X8 = (362.762, 222.762)
_c114 = (320.0, 180.0)
def _g114_base(extra=()):
    e = [('poly', _Q8, 'ink', 3), sg(_K, _L, 'ink', 3), sg(_M, _N, 'ink', 3), rt(_T, _K, _N, 9, 'ink'),
         at(_K, 'K', -6, -22, 'ink', 28, True), at(_L, 'L', -6, 24, 'ink', 28, True), at(_M, 'M', -24, 0, 'ink', 28, True),
         at(_N, 'N', 24, 0, 'ink', 28, True), at(_T, 'T', 18, 18, 'ink', 26, True)]
    return e + list(extra)
_cut2 = [sg(_W, (362.762, 283.238), 'teal', 3, True), sg((362.762, 76.762), _W, 'teal', 3, True), sg(_Q8[6], _Q8[3], 'teal', 3, True)]
_vb114 = '175 30 290 300'
f114q = PIN(GEO('f114q', [
    ('line', _g114_base()),
    ('cut', _cut2),
    ('kmt', [('tint', [_K, _M, _T], 'teal')]),
], vb=_vb114, w=480, title='The regular octagon'))
f114a = PIN(GEO('f114a', [
    ('line', _g114_base([s[:5] + ('ink', 2, True) for s in _cut2])),
    ('kmt', [('tint', [_K, _M, _T], 'teal'), at(mid(_K, _T), '1', 16, 0, 'teal', 26), at(mid(_M, _T), '1', 0, 22, 'teal', 26)]),
    ('km', [at(mid(_K, _M), '√2', -22, -14, 'teal', 26)]),
    ('all', [at(mid(_T, _U), '√2', 22, 0, 'orange', 24), at(mid(_U, _L), '1', 18, 0, 'orange', 24), at(mid(_W, _N), '1', 0, 22, 'orange', 24)]),
    ('lt', [sg(_T, _L, 'teal', 7)]),
    ('mn', [sg(_M, _N, 'orange', 7)]),
], vb=_vb114, w=480, title='K T is one'))
f114b = PIN(GEO('f114b', [
    ('line', _g114_base([s[:5] + ('ink', 2, True) for s in _cut2])),
    ('legs', [sg(_K, _T, 'teal', 7), sg(_U, _L, 'teal', 7)]),
    ('cancel', [sg(_U, _L, 'red', 9)]),
    ('rest', [sg(_T, _U, 'orange', 7), sg(_K, _M, 'orange', 7)]),
    ('ben', [sg(_M, _T, 'red', 9), sg(_W, _N, 'teal', 7), sg(_T, _W, 'orange', 7)]),
], vb=_vb114, w=480, title='Matching the pieces'))
for _g in (f114q, f114a, f114b): LEFT(_g, y=QY('g114', 330), x=410, w=430)
f114r1 = IH('f114r1', '$KT = MT = 1$, $\\ KM = \\sqrt2$', size=34)
f114r2 = IH('f114r2', '$LT = \\sqrt2 + 1$, $\\ 2KT = 2$', size=34)
f114r3 = IH('f114r3', '$\\sqrt2 > 1$: Sara is right', size=34)
f114r4 = IH('f114r4', '$KMT$: $1 + 1 + \\sqrt2 = 2 + \\sqrt2$', size=34)
f114r5 = IH('f114r5', '$MN = 1 + \\sqrt2 + 1 = 2 + \\sqrt2$', size=34)
f114s1 = I('f114s1', 'Sara: $KT + KT$ against side $+ KT$', size=28)
f114s2 = I('f114s2', '$KT$ (a leg) $<$ side (the hypotenuse)', size=28)
f114s3 = I('f114s3', 'Ben: $KT + MT + KM$ against $MT +$ side $+$ leg', size=28)
FLOW([f114r1, f114r2, f114r3, f114r4, f114r5], [(870, 710, 330, 700)])
FLOW([f114s1, f114s2, f114s3], [(870, 710, 330, 700)])
NOFIG('solve-geo34-g114', 0, 1, 2)

video('solve-geo34-g114', 'solution', qid='geo34-g114', slides=[
    S('Sara and Ben',
      L("The figure shows a regular octagon. K L and M N are perpendicular, and they meet at T. K, L, M and N are "
        "corners of the octagon. Sara says that L T is bigger than two times K T. Ben says that the perimeter of triangle "
        "K M T is equal to M N. Which of the following is true?", pt('stem', 'The figure shows a regular octagon', 'hl', 12.0),
        show(f114q['line'], 'The figure shows a regular octagon'), voice='calm', pause=0.5),
      L("Whatever way we choose, the first step is the octagon cut from the lesson. K L and M N are already two of its "
        "lines. Let's draw the other two. Now we have a square in the middle, four rectangles, and four silver triangles "
        "in the corners. K M T is one of the corner triangles.",
        show(f114q['cut'], "Let's draw the other two"), show(f114q['kmt'], 'K M T is one of the corner triangles')),
      L("We'll solve it in two different ways, by plugging in numbers, and then by understanding.")),
    SM('Method 1 · Plugging in numbers', 'K T is one',
      L("Let's plug in numbers. We could choose the octagon's side. But then, to get K T, we'd have to divide by root "
        "two. It's easier to multiply. So let's choose K T, a leg of the corner triangle. The easiest number is one.",
        show(f114a['line'], "Let's plug in numbers"), show(f114a['kmt'], 'The easiest number is one')),
      L("Triangle K M T is a silver triangle, so its legs are equal, and M T is one too. The hypotenuse K M is the leg "
        "times root two, so it's root two.", show(f114a['km'], 'so it\'s root two'), show(f114r1, 'The hypotenuse K M')),
      L("K M is a side of the octagon. So every side of the octagon is root two, and so is the side of the square. And "
        "every corner triangle has legs of one.", show(f114a['all'], 'So every side of the octagon')),
      L("Now Sara. L T goes from T down to L. It's the side of the square, root two, plus the leg of the bottom triangle, "
        "one. So L T is root two plus one. And two times K T is two times one, two.",
        show(f114a['lt'], 'L T goes from T down to L'), show(f114r2, 'So L T is root two plus one')),
      L("Which is bigger, root two plus one, or two? Let's take one away from both. That's root two against one. Root two "
        "is more than one, because two is more than one. So L T is bigger, and Sara is right. Choice number one, only "
        "Ben, is out. And choice number four, neither, is out too.",
        show(f114r3, 'Root two is more than one'), mk('cross', 'choice 1', 'Choice number one, only Ben'),
        mk('cross', 'choice 4', 'choice number four, neither')),
      L("Now Ben. The perimeter of triangle K M T is one, plus one, plus root two. That's two plus root two.",
        show(f114r4, 'one, plus one, plus root two')),
      L("M N goes from M to N. First the leg M T, one. Then the side of the square, root two. Then the leg on the right, "
        "one. So M N is two plus root two too. They're equal, so Ben is right. Both are right. Choice number two is our "
        "answer.", show(f114a['mn'], 'M N goes from M to N'), show(f114r5, 'So M N is two plus root two'),
        mk('tick', 'choice 2', 'Choice number two is our'))),
    SM('Method 2 · Understanding', 'Match the pieces',
      L("Now by understanding, with no numbers at all. We just match equal pieces. Sara compares two times K T with L T. "
        "L T is the side of the square, plus the leg at the bottom. And that leg is equal to K T, because all the corner "
        "triangles are the same.", show(f114b['line'], 'Now by understanding'), show(f114b['legs'], 'that leg is equal to K T'),
        show(f114s1, 'Sara compares')),
      L("So let's take one K T away from both sides. What's left? One K T for Sara's two times K T, and the side of the "
        "square for L T.", show(f114b['cancel'], "take one K T away")),
      L("The side of the square is a side of the octagon, like the hypotenuse K M. And K T is only a leg. In a right "
        "triangle, the hypotenuse is the longest side. So L T is more than two times K T, and Sara is right.",
        show(f114b['rest'], 'The side of the square is a side'), show(f114s2, 'the hypotenuse is the longest side')),
      L("Now Ben. The perimeter of K M T is K T plus M T plus K M. And M N is M T, plus the side of the square, plus the "
        "leg on the right.", show(f114s3, 'The perimeter of K M T')),
      L("M T is on both sides, so it cancels. K M is a side of the octagon, the same as the side of the square. And K T "
        "is a leg, the same as the leg on the right. So the two are equal, and Ben is right too. Choice number two is our "
        "answer, and I'll see you in the next question.",
        show(f114b['ben'], 'M T is on both sides'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# solve-geo34-g115 - a regular octagon: the shaded parts equal the white rectangle
# Hebrew geo 5823-5847 (2 + 2 root 2 there, 12 + 12 root 2 here): "it's really wrong to solve this with algebra"; the
# first step always: the octagon cut; the four triangles = the white square, the two grey rectangles = the two white
# ones; nothing to calculate; "an edge question solved in seconds if we control this shape". R37: the cut and "four
# triangles = the square" are taught in geo-105 (links). One method (her Hebrew has one).
# V3: the copy (grey sides); the two horizontal cut lines dashed; the white parts outlined teal; the grey parts orange;
# matching pairs tinted in turn (rectangles, then triangles with the square).
# =================================================================================================================
_g15sq = [_T, _W, _X8, _U]
_g15top = [_K, _Q8[1], _W, _T]; _g15bot = [_U, _X8, _Q8[4], _L]
_g15lr = [_M, _T, _U, _Q8[6]]; _g15rr = [_W, _N, _Q8[3], _X8]
_g15tri = [[_K, _M, _T], [_Q8[1], _W, _N], [_X8, _Q8[3], _Q8[4]], [_U, _L, _Q8[6]]]
def _g115_base(extra=()):
    e = [('tint', [_K, _Q8[7], _Q8[6], _L], 'ink'), ('tint', [_Q8[1], _Q8[2], _Q8[3], _Q8[4]], 'ink'),
         ('poly', _Q8, 'ink', 3), sg(_K, _L, 'ink', 3), sg(_Q8[1], _Q8[4], 'ink', 3)]
    return e + list(extra)
f115 = PIN(GEO('f115', [
    ('line', _g115_base()),
    ('cut', [sg(_M, _N, 'teal', 3, True), sg(_Q8[6], _Q8[3], 'teal', 3, True)]),
    ('white', [('poly', _g15sq, 'teal', 5), ('poly', _g15top, 'teal', 5), ('poly', _g15bot, 'teal', 5)]),
    ('grey', [('poly', _g15lr, 'orange', 5), ('poly', _g15rr, 'orange', 5)] + [('poly', t, 'orange', 4) for t in _g15tri]),
    ('rects', [('tint', r, 'teal') for r in (_g15top, _g15bot, _g15lr, _g15rr)] + [('txt',) + tuple(cen(r)) + ('=', 'teal', 30) for r in (_g15top, _g15bot, _g15lr, _g15rr)]),
    ('tris', [('tint', t, 'orange') for t in _g15tri] + [('tint', _g15sq, 'orange')]),
], vb='175 30 290 300', w=480, title='The regular octagon'))
LEFT(f115, y=QY('g115', 270), x=410, w=430)
f115r1 = I('f115r1', 'white: square $+$ 2 rectangles', size=30)
f115r2 = I('f115r2', 'grey: 2 rectangles $+$ 4 triangles', size=30)
f115r3 = I('f115r3', '4 triangles $=$ the square', size=30)
f115r4 = I('f115r4', 'grey $=$ white $= 12 + 12\\sqrt2$', size=32)
FLOW([f115r1, f115r2, f115r3, f115r4], [(870, 710, 280, 700)])
NOFIG('solve-geo34-g115', 0)

video('solve-geo34-g115', 'solution', qid='geo34-g115', slides=[
    S('Match white and grey',
      L("The figure shows a regular octagon cut by two vertical lines. The white rectangle in the middle has an area of "
        "twelve plus twelve root two. What is the sum of the shaded areas?", pt('stem', 'The figure shows a regular octagon', 'hl', 8.0),
        show(f115['line'], 'The figure shows a regular octagon'), voice='calm', pause=0.5),
      L("So we know the white part, and we need the grey part. We could write the side as a letter and do a lot of "
        "algebra. But that takes a long time. We'll solve it by understanding, in a few seconds."),
      L("The first step is always the same, the octagon cut from the lesson. The two vertical lines are already there. "
        "Let's add the two horizontal lines. Now we have a square in the middle, four rectangles, and four silver triangles "
        "in the corners.", show(f115['cut'], "Let's add the two horizontal lines")),
      L("The white rectangle is the square, plus the rectangle above it, plus the rectangle below it.",
        show(f115['white'], 'The white rectangle is the square'), show(f115r1, 'plus the rectangle above it')),
      L("The grey part is the two rectangles on the sides, plus the four corner triangles.",
        show(f115['grey'], 'The grey part'), show(f115r2, 'plus the four corner triangles')),
      L("Now let's match them. All four rectangles are the same, because the octagon is regular. So the two grey "
        "rectangles match the two white rectangles.", show(f115['rects'], 'All four rectangles are the same')),
      L("And like in the lesson, the four corner triangles together make exactly one square like the middle one. So the "
        "four grey triangles match the white square.", show(f115['tris'], 'the four corner triangles together'),
        show(f115r3, 'match the white square')),
      L("So the grey area is equal to the white area, and we didn't calculate anything. The shaded area is twelve plus "
        "twelve root two. So when parts of a regular octagon are shaded, cut it first and match the pieces. Choice number "
        "one is our answer, and I'll see you in the next question.",
        show(f115r4, 'So the grey area is equal'), mk('tick', 'choice 1', 'Choice number one is our answer'))),
])


# =================================================================================================================
# solve-geo34-g116 - the angle sum is 1,440: how many sides?
# Hebrew geo 5849-5900 (1,260 -> 9 there; 1,440 -> 10 here): "most polygon questions are pentagons, hexagons and octagons,
# but there are general ones too"; two ways: the formula (divide first: by 10, by 2, by 9; "we want small numbers") and an
# anchor (the sums we know by heart, the octagon 1,080 is close, 7 and 8 out; +180 per side: add 200, take away 20).
# R37: "from the sum back to n" and "+180 per side" are taught in geo-104 (links). Trap at its step: 8 (n - 2).
# Board: the equation rows, one per clause; the anchor ladder.
# =================================================================================================================
f116r1 = IH('f116r1', '$180(n-2) = 1440$', size=36)
f116r2 = IH('f116r2', '$18(n-2) = 144$', size=36)
f116r3 = IH('f116r3', '$9(n-2) = 72$', size=36)
f116r4 = IH('f116r4', '$n - 2 = 8$', size=36)
f116r5 = IH('f116r5', '$n = 8 + 2 = 10$', size=36)
f116s1 = I('f116s1', 'pentagon $540°$ · hexagon $720°$ · octagon $1080°$', size=32)
f116s2 = IH('f116s2', '$1440 > 1080$: more than 8 sides', size=34)
f116s3 = IH('f116s3', '9 sides: $1080 + 200 - 20 = 1260$', size=34)
f116s4 = IH('f116s4', '10 sides: $1260 + 200 - 20 = 1440$', size=34)

video('solve-geo34-g116', 'solution', qid='geo34-g116', slides=[
    SM('Method 1 · The math way', 'The formula',
      L("The sum of the interior angles of a polygon is one thousand four hundred forty. How many sides does it have?",
        pt('stem', 'The sum of the interior angles', 'hl', 6.0), voice='calm', pause=0.5),
      L("So we go from the sum back to the number of sides, like in the lesson. We'll solve it in two different ways, the "
        "math way, and then by understanding, with an anchor."),
      L("Let's start with the math way. The sum of the angles is one hundred eighty times the bracket, n minus two. Here the sum is one "
        "thousand four hundred forty. So one hundred eighty times the bracket, n minus two is equal to one thousand four hundred forty.",
        show(f116r1, 'So one hundred eighty times the bracket, n minus two')),
      L("We could open the brackets, but we want the smallest numbers possible. So let's divide first. Both sides end in "
        "zero, so let's divide both by ten. Eighteen times the bracket, n minus two is equal to one hundred forty-four.",
        show(f116r2, 'Eighteen times the bracket, n minus two')),
      L("Does one hundred forty-four divide by eighteen? It's hard to see. But both numbers are even, so let's divide both "
        "by two. Nine times the bracket, n minus two is equal to seventy-two.", show(f116r3, 'Nine times the bracket, n minus two')),
      L("Seventy-two divides by nine, from the times table. Nine times eight is seventy-two. So n minus two is eight.",
        show(f116r4, 'So n minus two is eight')),
      L("Careful here. Eight is n minus two, the number of triangles. It's not the number of sides, and it's choice number "
        "four, a trap. n is eight plus two, ten. Choice number three is our answer.",
        mk('cross', 'choice 4', "it's choice number four"), show(f116r5, 'n is eight plus two'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Understanding: an anchor', 'An anchor',
      L("Now by understanding, with an anchor. Which sums do we know by heart? A triangle is one hundred eighty, and a "
        "quadrilateral is three hundred sixty. Like in the lesson, a pentagon is five hundred forty, a hexagon is seven "
        "hundred twenty, and an octagon is one thousand eighty.", show(f116s1, 'a pentagon is five hundred forty')),
      L("One thousand four hundred forty isn't one we know. But the octagon is close. And one thousand four hundred forty "
        "is bigger, so the polygon has more than eight sides. So choice number four, eight, is out.",
        show(f116s2, 'so the polygon has more than eight sides'), mk('cross', 'choice 4', 'So choice number four, eight, is out')),
      L("Remember, every extra side adds one hundred eighty. Let's start from the octagon and add one hundred eighty. An "
        "easy way is to add two hundred and take away twenty. One thousand eighty plus two hundred is one thousand two "
        "hundred eighty. Minus twenty is one thousand two hundred sixty. That's nine sides.",
        show(f116s3, 'One thousand eighty plus two hundred')),
      L("Let's add one hundred eighty again. One thousand two hundred sixty plus two hundred is one thousand four hundred "
        "sixty. Minus twenty is one thousand four hundred forty. That's our sum, with ten sides. Choice number three is "
        "our answer, and I'll see you in the next question.",
        show(f116s4, "Let's add one hundred eighty again"), mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-geo34-g117 - B - A: the sums of 20 and 14 sides
# Hebrew geo 5901-5925 (10 and 13 sides -> pentagon there; 14 and 20 -> octagon here): the math way (express both with
# the formula, don't calculate each and subtract: a common factor 180) and the understanding way (+3 sides, 3 x 180).
# R37: "+180 per side" and "comparing two polygons" are taught in geo-104 (the 12 / 9 example). Trap at its step: the
# hexagon (6 = the extra sides).
# =================================================================================================================
f117r1 = IH('f117r1', '$B = 180(20-2) = 180 \\cdot 18$', size=34)
f117r2 = IH('f117r2', '$A = 180(14-2) = 180 \\cdot 12$', size=34)
f117r3 = IH('f117r3', '$B - A = 180(18 - 12)$', size=34)
f117r4 = IH('f117r4', '$= 180 \\cdot 6 = 1080$', size=34)
f117r5 = IH('f117r5', '$6 + 2 = 8$ sides: octagon', size=34)
FLOW([f117r1, f117r2, f117r3], [(410, 580, 260, 700)])
FLOW([f117r4, f117r5], [(1000, 580, 260, 700)])
f117s1 = IH('f117s1', '$20 - 14 = 6$ more sides', size=34)
f117s2 = IH('f117s2', '$6 \\cdot 180 = 600 + 480 = 1080$', size=34)
f117s3 = I('f117s3', 'hexagon: $720°$, not $1080°$', size=32)

video('solve-geo34-g117', 'solution', qid='geo34-g117', slides=[
    SM('Method 1 · The math way: a common factor', 'A common factor',
      L("A is the sum of the interior angles of a polygon with fourteen sides. B is the sum of the interior angles of a "
        "polygon with twenty sides. The difference, B minus A, is equal to the sum of the interior angles of which "
        "polygon?", pt('stem', 'A is the sum of the interior angles', 'hl', 10.0), voice='calm', pause=0.5),
      L("So we don't need A or B themselves, only the difference between them. We'll solve it in two different ways, the "
        "math way, and then by understanding."),
      L("Let's start with the math way. B has twenty sides. So B is one hundred eighty times the bracket, twenty minus two, which is "
        "one hundred eighty times eighteen.", show(f117r1, 'So B is one hundred eighty')),
      L("A has fourteen sides. So A is one hundred eighty times the bracket, fourteen minus two, which is one hundred eighty times "
        "twelve.", show(f117r2, 'So A is one hundred eighty')),
      L("We won't calculate each one and subtract. Both have one hundred eighty in them, so let's take it out as a common "
        "factor. That means we keep the shared multiplier, one hundred eighty, and subtract eighteen minus twelve. "
        "B minus A is one hundred eighty times the bracket, eighteen minus twelve. Eighteen minus twelve is six. So it's six "
        "times one hundred eighty. Six times one hundred is six hundred, and six times eighty is four hundred eighty. "
        "Together, one thousand eighty.",
        show(f117r3, 'B minus A is one hundred eighty times'), show(f117r4, 'Eighteen minus twelve is six')),
      L("Which polygon has a sum of one thousand eighty? Six times one hundred eighty means six triangles. And there are "
        "always two more sides than triangles. Six plus two is eight sides, an octagon. Choice number two is our answer.",
        show(f117r5, 'Six plus two is eight sides'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · Understanding', 'Count the extra sides',
      L("Now by understanding. Like in the lesson, every extra side adds one hundred eighty. How many more sides does B "
        "have? Twenty minus fourteen is six. So B is six times one hundred eighty more than A.",
        show(f117s1, 'Twenty minus fourteen is six')),
      L("Six times one hundred eighty is one thousand eighty, and like before, that's the sum of an octagon.",
        show(f117s2, 'Six times one hundred eighty is one thousand eighty')),
      L("Careful with choice number one, a hexagon. Six is the number of extra sides, not the answer. A hexagon has a sum "
        "of only seven hundred twenty. Choice number two is our answer, and I'll see you in the next question.",
        mk('cross', 'choice 1', 'Careful with choice number one'), show(f117s3, 'A hexagon has a sum'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# solve-q-r26-t34-01 - one angle is 160: how many sides? (English-made, 2026-09)
# Two ways: the formula-sheet form 180 - 360 / n (geo-104, link) and the exterior angle (geo-104: all of them 360, each
# 360 / n in a regular polygon). The trap 9 (180 / 20) at its step. W20: "one angle given -> the exterior angle first".
# V3: a regular 18-gon with one side extended, the angle 160 and the exterior angle 20 marked.
# =================================================================================================================
_O01 = (170, 165); _P18 = rp(_O01[0], _O01[1], 125, 18, 90)
_e0 = gpt(_P18[1][0], _P18[1][1], 70, gdir(_P18[0][0], _P18[0][1], _P18[1][0], _P18[1][1]))
f01 = PIN(GEO('f01', [
    ('line', [('poly', _P18, 'ink', 3)]),
    ('ang', [ang(_P18[1], _P18[0], _P18[2], 22, 'teal'), at(_P18[1], '160°', 26, 36, 'teal', 24)]),
    ('ext', [sg(_P18[1], _e0, 'orange', 3, True), angw(_P18[1], _e0, _P18[2], 34, 'orange'), at(_P18[1], '20°', -54, 6, 'orange', 24)]),
], vb='10 10 320 310', w=440, col=1, title='A regular polygon with angles of 160'))
_R(f01, 250, 1120)
f01r1 = IH('f01r1', '$180° - \\dfrac{360°}{n} = 160°$', size=34)
f01r2 = IH('f01r2', '$\\dfrac{360°}{n} = 20°$', size=34)
f01r3 = IH('f01r3', '$n = 360 \\div 20 = 36 \\div 2 = 18$', size=34)
f01s1 = IH('f01s1', 'exterior: $180° - 160° = 20°$', size=34)
f01s2 = IH('f01s2', '$n = 360° \\div 20° = 18$', size=34)
f01s3 = IH('f01s3', '$180 \\div 20 = 9$: the trap', size=34)

video('solve-q-r26-t34-01', 'solution', qid='q-r26-t34-01', slides=[
    SM('Method 1 · The math way: the formula', 'The formula',
      L("Each interior angle of a regular polygon is one hundred sixty. How many sides does the polygon have?",
        pt('stem', 'Each interior angle', 'hl', 6.0), voice='calm', pause=0.5),
      L("So we know one angle, and we need the number of sides. We'll solve it in two different ways, both the math way. "
        "First with the formula from the formula sheet, and then with the exterior angle."),
      L("Like in the lesson, one angle of a regular polygon is one hundred eighty, minus three hundred sixty over n. Here "
        "the angle is one hundred sixty. So one hundred eighty minus three hundred sixty over n is equal to one hundred "
        "sixty.", show(f01r1, 'So one hundred eighty minus')),
      L("One hundred eighty minus what is one hundred sixty? Minus twenty. So three hundred sixty over n is twenty.",
        show(f01r2, 'So three hundred sixty over n is twenty')),
      L("So n is three hundred sixty divided by twenty. Let's take a zero off both. Thirty-six divided by two is eighteen. "
        "So n is eighteen. Choice number three is our answer.",
        show(f01r3, 'Thirty-six divided by two'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · The math way: the exterior angle', 'The exterior angle',
      L("Now with the exterior angle. The polygon's angle and its exterior angle add up to one hundred eighty. So the "
        "exterior angle is one hundred eighty minus one hundred sixty, twenty.",
        show(f01['line'], 'Now with the exterior angle'), show(f01['ang'], "The polygon's angle"),
        show(f01['ext'], 'So the exterior angle'), show(f01s1, 'one hundred eighty minus one hundred sixty')),
      L("Like in the lesson, all the exterior angles together make three hundred sixty. The polygon is regular, so they're "
        "all equal, twenty each. How many twenties make three hundred sixty? Three hundred sixty divided by twenty is "
        "eighteen.", show(f01s2, 'Three hundred sixty divided by twenty')),
      L("Careful with choice number one, nine. That's one hundred eighty divided by twenty. It uses one hundred eighty "
        "instead of the full turn, three hundred sixty.", mk('cross', 'choice 1', 'Careful with choice number one'),
        show(f01s3, "That's one hundred eighty divided by twenty")),
      L("So when a question gives one angle of a regular polygon, find the exterior angle first. Then divide three "
        "hundred sixty by it. Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-q-r26-t34-02 - seven diagonals from one corner: how many diagonals in all? (English-made, 2026-09)
# A one-off (R37: one question, ~2 min): n - 3 from one corner (not to itself, not to its two neighbours), shown first on
# the pentagon (2) and the hexagon (3) (W10: an easier example first); n = 10; 10 x 7 counts each diagonal twice (two
# ends) -> 35; checked on the pentagon (5 x 2 / 2 = 5, the star); the traps 70 and 45 (the sides counted) at their steps.
# V3: the pentagon and the hexagon, one corner ringed, its two neighbours red, the diagonals teal; the pentagon's star.
# =================================================================================================================
_p5d = rp(120, 160, 95, 5, 90); _p6d = rp(380, 160, 95, 6, 90)
f02 = PIN(GEO('f02', [
    ('line', [('poly', _p5d, 'ink', 3)] + [pdot(p) for p in _p5d] + [('circ', _p5d[0][0], _p5d[0][1], 11, 'orange', 3)]),
    ('nb', [sg(_p5d[0], _p5d[1], 'red', 6), sg(_p5d[0], _p5d[4], 'red', 6)]),
    ('d5', fan(_p5d, 0, 'teal', 4, False) + [('txt', 120, 290, '5 - 3 = 2', 'teal', 24)]),
    ('hex', [('poly', _p6d, 'ink', 3)] + [pdot(p) for p in _p6d] + [('circ', _p6d[0][0], _p6d[0][1], 11, 'orange', 3)]
            + fan(_p6d, 0, 'teal', 4, False) + [('txt', 380, 290, '6 - 3 = 3', 'teal', 24)]),
], vb='0 40 500 270', w=640, title='Diagonals from one corner'))
_p5s = rp(150, 160, 110, 5, 90)
f02b = PIN(GEO('f02b', [
    ('line', [('poly', _p5s, 'ink', 3)] + [pdot(p) for p in _p5s]),
    ('star', [sg(_p5s[k], _p5s[(k + 2) % 5], 'teal', 4) for k in range(5)] + [('txt', 150, 305, '5 diagonals', 'teal', 24)]),
], vb='20 30 260 300', w=360, title="The pentagon's diagonals"))
_R(f02, 240, 940)
_R(f02b, 240, 1150)
f02r1 = I('f02r1', 'from one corner: $n - 3$', size=34)
f02r2 = IH('f02r2', '$n - 3 = 7$, $\\ n = 10$', size=34)
f02s1 = IH('f02s1', '$10 \\cdot 7 = 70$', size=34)
f02s2 = IH('f02s2', '$70 \\div 2 = 35$', size=34)
f02s3 = IH('f02s3', 'pentagon: $5 \\cdot 2 \\div 2 = 5$', size=34)
f02s4 = IH('f02s4', '$10 \\cdot 9 \\div 2 = 45$: with the sides', size=34)
f02s5 = IH('f02s5', '$45 - 10 = 35$', size=34)

video('solve-q-r26-t34-02', 'solution', qid='q-r26-t34-02', slides=[
    S('Diagonals from one corner',
      L("From one corner of a polygon, exactly seven diagonals can be drawn. How many diagonals does the polygon have in "
        "all?", pt('stem', 'From one corner of a polygon', 'hl', 6.0), voice='calm', pause=0.5),
      L("This is a new kind of question, so let's learn how to count diagonals. We'll do it in two steps. First we find "
        "the number of sides. Then we count all the diagonals."),
      L("Let's start with an easy polygon, a pentagon. A diagonal joins our corner to another corner. But not to itself, "
        "and not to its two neighbors, because those lines are sides. So from one corner of a pentagon there are five "
        "minus three, two diagonals.",
        show(f02['line'], 'a pentagon'), show(f02['nb'], 'not to its two neighbors'), show(f02['d5'], 'five minus three, two')),
      L("In a hexagon, six minus three is three diagonals from one corner. So from one corner of a polygon with n sides, "
        "there are n minus three diagonals.", show(f02['hex'], 'In a hexagon'), show(f02r1, 'So from one corner')),
      L("In our question there are seven. So n minus three is seven, and n is seven plus three, ten. It's a polygon with "
        "ten sides.", show(f02r2, 'So n minus three is seven'))),
    S('All the diagonals',
      L("Now all the diagonals. Each of the ten corners sends seven diagonals. Ten times seven is seventy.",
        show(f02s1, 'Ten times seven is seventy')),
      L("But careful, seventy is a trap, and it's choice number four. Every diagonal has two ends. So we counted each "
        "diagonal twice, once from each end. So we divide by two. Seventy divided by two is thirty-five.",
        mk('cross', 'choice 4', "it's choice number four"), show(f02s2, 'Seventy divided by two')),
      L("Let's check this way of counting on the pentagon. Five corners, two diagonals from each. Five times two is ten, "
        "and half of that is five. And a pentagon really has five diagonals. They make the star inside it.",
        show(f02s3, 'Five times two is ten'), show(f02b['line'], 'a pentagon really has'), show(f02b['star'], 'They make the star')),
      L("And choice number three, forty-five? That's ten times nine, divided by two. It joins every corner to every other "
        "corner, so it counts the ten sides too. But sides are not diagonals. Forty-five minus ten is thirty-five again. "
        "Choice number two is our answer, and I'll see you in the next question.",
        show(f02s4, "That's ten times nine"), mk('cross', 'choice 3', 'And choice number three'), show(f02s5, 'Forty-five minus ten'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# r26-t34-meet (lesson) - Polygons Meeting at a Point (English-made, 2026-09; back in the flow by R37, see t34.py)
# Core method (real exam 2024 winter q1_18: a regular hexagon and a square on a common side; 2020 spring q1_17: pentagons
# around a point): 360 around the shared corner, then the isosceles triangle (both sides = the common side). On numbers:
# the hexagon + square (150, base angles 15; the trap 30); the pentagon + hexagon (132, base angles 24); filling a point
# (3 hexagons, 4 squares, 6 equilateral triangles; 3 pentagons leave 36). Study plan: angles around a point (topic 30),
# the isosceles triangle (topic 31) are reminders; the polygon angles 90 / 108 / 120 are geo-104.
# Visuals: each shape built at her words: the two polygons, the shared corner ringed, the three angles (each colour),
# the gap closed into a triangle (tinted, its two sides ticked), the base angles.
# =================================================================================================================
def ngon_on(P, Q, n, sgn=1):
    """a regular n-gon with side P-Q; sgn picks the side (1: the corners turn counter-clockwise on the screen)"""
    pts = [P, Q]; d = gdir(P[0], P[1], Q[0], Q[1]); L = _pm.hypot(Q[0] - P[0], Q[1] - P[1])
    for k in range(n - 2):
        d += sgn * 360.0 / n; pts.append(gpt(pts[-1][0], pts[-1][1], L, d))
    return pts
# hexagon + square on a vertical common side; the shared corner S at the top of that side
_S = (260.0, 120.0); _Sb = (260.0, 220.0)
_hx = ngon_on(_Sb, _S, 6, 1)          # to the left of the side
_sq = ngon_on(_S, _Sb, 4, 1)          # to the right
_hn = _hx[2]                          # the hexagon's next corner after S
_sn = _sq[3]                          # the square's corner next to S
p_meet = PIN(GEO('p_meet', [
    ('line', [('poly', _hx, 'ink', 3), ('poly', _sq, 'ink', 3)]),
    ('s', [('circ', _S[0], _S[1], 10, 'red', 3)]),
    ('h', [angw(_S, _hn, _Sb, 34, 'teal'), at(_S, '120°', -50, 34, 'teal', 24)]),
    ('q', [rt(_S, _Sb, _sn, 16, 'orange'), at(_S, '90°', 34, 32, 'orange', 24)]),
    ('x', [ang(_S, _hn, _sn, 26, 'red'), at(_S, 'x = 150°', 4, -54, 'red', 26)]),
], vb='60 20 360 270', w=580, col=0, title='A regular hexagon and a square'))
p_meet1 = IH('p_meet1', '$x = 360° - 120° - 90° = 150°$', size=34, col=1)
p_tri = PIN(GEO('p_tri', [
    ('line', [('poly', _hx, 'ink', 3), ('poly', _sq, 'ink', 3), ang(_S, _hn, _sn, 26, 'red'), at(_S, '150°', 4, -50, 'red', 24)]),
    ('close', [sg(_hn, _sn, 'teal', 3, True), ('tint', [_S, _hn, _sn], 'teal')]),
    ('eq', [sg(_S, _hn, 'teal', 5), sg(_S, _sn, 'teal', 5), tk(_S, _hn, 1), tk(_S, _sn, 1), tk(_S, _Sb, 1, 'ink')]),
    ('b', [ang(_hn, _S, _sn, 40, 'orange'), ang(_sn, _hn, _S, 40, 'orange'), at(_hn, '15°', 20, -12, 'orange', 20), at(_sn, '15°', -20, -12, 'orange', 20)]),
], vb='60 20 360 270', w=580, col=0, title='Close the gap'))
p_tri1 = I('p_tri1', 'both sides $=$ the common side: isosceles', size=30, col=1)
p_tri2 = IH('p_tri2', '$180° - 150° = 30°$', size=34, col=1)
p_tri3 = IH('p_tri3', '$30° \\div 2 = 15°$', size=34, col=1)
# pentagon + hexagon
_S2 = (260.0, 120.0); _S2b = (260.0, 220.0)
_px = ngon_on(_S2b, _S2, 5, 1); _hy = ngon_on(_S2, _S2b, 6, 1)
p_two = PIN(GEO('p_two', [
    ('line', [('poly', _px, 'ink', 3), ('poly', _hy, 'ink', 3), ('circ', _S2[0], _S2[1], 10, 'red', 3)]),
    ('a', [at(_S2, '108°', -50, 30, 'teal', 22), at(_S2, '120°', 50, 30, 'orange', 22), ang(_S2, _px[2], _hy[-1], 24, 'red'),
           at(_S2, '132°', 0, -46, 'red', 24)]),
    ('t', [sg(_px[2], _hy[-1], 'teal', 3, True), ('tint', [_S2, _px[2], _hy[-1]], 'teal'), tk(_S2, _px[2]), tk(_S2, _hy[-1])]),
    ('basevalues', [at(_px[2], '24°', 20, -12, 'orange', 20), at(_hy[-1], '24°', -20, -12, 'orange', 20)]),
], vb='60 0 400 300', w=580, col=0, title='A regular pentagon and a regular hexagon'))
p_two1 = IH('p_two1', '$360° - 120° - 108° = 132°$', size=34, col=1)
p_two2 = IH('p_two2', '$180° - 132° = 48°$', size=34, col=1)
p_two3 = IH('p_two3', '$48° \\div 2 = 24°$', size=34, col=1)
# filling a point
_c0 = (190.0, 160.0)
_h1 = ngon_on(_c0, (_c0[0] + 80, _c0[1]), 6, -1); _h2 = ngon_on(_c0, gpt(_c0[0], _c0[1], 80, 120), 6, -1)
_h3 = ngon_on(_c0, gpt(_c0[0], _c0[1], 80, 240), 6, -1)
_c1 = (470.0, 170.0)
_f1 = ngon_on(_c1, gpt(_c1[0], _c1[1], 80, 90), 5, -1); _f2 = ngon_on(_c1, gpt(_c1[0], _c1[1], 80, 90 - 108), 5, -1)
_f3 = ngon_on(_c1, gpt(_c1[0], _c1[1], 80, 90 - 216), 5, -1)
p_fill = PIN(GEO('p_fill', [
    ('line', [('poly', _h1, 'ink', 3), ('tint', _h1, 'teal'), ('poly', _h2, 'ink', 3), ('tint', _h2, 'orange'), ('poly', _h3, 'ink', 3),
              ('tint', _h3, 'teal'), ('txt', _c0[0], 315, '3 · 120° = 360°', 'teal', 24)]),
    ('pent', [('poly', _f1, 'ink', 3), ('tint', _f1, 'teal'), ('poly', _f2, 'ink', 3), ('tint', _f2, 'orange'), ('poly', _f3, 'ink', 3),
              ('tint', _f3, 'teal'), ang(_c1, _f1[1], _f3[-1], 30, 'red'), ('txt', _c1[0], 315, '3 · 108° = 324°', 'red', 24)]),
], vb='20 0 620 330', w=900, col=0, title='Filling a point'))
p_fill1 = I('p_fill1', 'Filling a point: the angles add up to $360°$', size=30)

video('r26-t34-meet', 'lesson', slides=[
    S('Polygons Meeting at a Point',
      L("Now let's look at polygons that meet at one point. On the exam, two regular polygons often sit on a common side. "
        "These questions have two steps, and they come back every time.")),
    S('Around a point',
      L("Here's a regular hexagon, and a square built on one of its sides, outside the hexagon. Look at the corner they "
        "share. Three angles sit around it. The hexagon's angle, the square's angle, and the gap between them, x.",
        show(p_meet['line'], "Here's a regular hexagon"), show(p_meet['s'], 'Look at the corner they share')),
      L("All the angles around one point add up to three hundred sixty. The hexagon's angle is one hundred twenty. The "
        "square's angle is ninety. So x is three hundred sixty, minus one hundred twenty, minus ninety. That's one hundred "
        "fifty.", show(p_meet['h'], "The hexagon's angle is one hundred twenty"), show(p_meet['q'], "square's angle is ninety"),
        show(p_meet1, 'So x is three hundred sixty'), show(p_meet['x'], "That's one hundred fifty"))),
    S('Find the isosceles triangle',
      L("The exam usually goes one step further. Let's close the gap into a triangle, with a line across it.",
        show(p_tri['line'], 'The exam usually goes one step further'), show(p_tri['close'], 'close the gap')),
      L("The two sides of angle x are a side of the square and a side of the hexagon. Both are equal to the common side, "
        "because each polygon is regular. So the two sides are equal, and the triangle is isosceles.",
        show(p_tri['eq'], 'The two sides of angle x'), show(p_tri1, 'and the triangle is isosceles')),
      L("Its top angle is one hundred fifty. The two base angles share one hundred eighty minus one hundred fifty, thirty. "
        "So each base angle is half of thirty, fifteen. Careful, thirty is both base angles together. Don't forget to "
        "divide by two.", show(p_tri2, 'one hundred eighty minus one hundred fifty'), show(p_tri3, 'So each base angle'),
        show(p_tri['b'], 'fifteen. Careful'))),
    S('One more pair',
      L("Let's see it again with a regular pentagon and a regular hexagon on a common side. Around the shared corner, "
        "three hundred sixty minus one hundred twenty is two hundred forty. Minus one hundred eight is one hundred "
        "thirty-two.", show(p_two['line'], 'a regular pentagon and a regular hexagon'), show(p_two['a'], 'Around the shared corner'),
        show(p_two1, 'Minus one hundred eight')),
      L("Again, the two sides of the gap are equal to the common side, so the triangle is isosceles. One hundred eighty "
        "minus one hundred thirty-two is forty-eight. Half of that is twenty-four. So each base angle is twenty-four.",
        show(p_two['t'], 'the two sides of the gap'), show(p_two2, 'minus one hundred thirty-two'), show(p_two3, 'Half of that'),
        show(p_two['basevalues'], 'So each base angle is twenty-four'))),
    S('Filling a point',
      L("And when regular polygons fill the space around a point with no gaps, their angles add up to exactly three "
        "hundred sixty. Three regular hexagons fit, because three times one hundred twenty is three hundred sixty. That's "
        "how a honeycomb is built.", show(p_fill['line'], 'Three regular hexagons fit'), show(p_fill1, 'their angles add up to exactly')),
      L("Four squares fit too, four times ninety. And six equilateral triangles, six times sixty. But three regular "
        "pentagons don't fit. Three times one hundred eight is three hundred twenty-four, so a gap of thirty-six is left.",
        show(p_fill['pent'], 'But three regular pentagons')),
      L("So when two regular polygons share a side, first use the three hundred sixty around the point. Then look for the "
        "isosceles triangle. Take a moment to memorize this, and I'll see you in the next video.")),
])


# =================================================================================================================
# solve-q-r26-t34-03 - a square and a regular pentagon on a common side (English-made, 2026-09)
# R37: the method is taught in r26-t34-meet (link): 360 around A (90, 108 -> 162), then the isosceles triangle ADG
# (AD = AB = AG) -> (180 - 162) / 2 = 9; the trap 18 (both base angles) at its step.
# V3: the copy; A ringed; the square's 90 and the pentagon's 108; the gap 162; triangle ADG tinted, AD and AG ticked with
# AB; the base angles 9.
# =================================================================================================================
_qA, _qB, _qC, _qD = (300.0, 110.0), (300.0, 210.0), (200.0, 210.0), (200.0, 110.0)
_qE, _qF, _qG = (395.1, 240.9), (453.9, 160.0), (395.1, 79.1)
def _q03_base(extra=()):
    e = [('poly', [_qA, _qB, _qC, _qD], 'ink', 3), ('poly', [_qA, _qB, _qE, _qF, _qG], 'ink', 3), sg(_qD, _qG, 'ink', 3),
         at(_qA, 'A', -14, 18, 'ink', 26, True), at(_qB, 'B', 0, 22, 'ink', 26, True), at(_qC, 'C', -16, 16, 'ink', 26, True),
         at(_qD, 'D', -16, -14, 'ink', 26, True), at(_qE, 'E', 8, 20, 'ink', 26, True), at(_qF, 'F', 20, 0, 'ink', 26, True),
         at(_qG, 'G', 6, -18, 'ink', 26, True)]
    return e + list(extra)
f03a = PIN(GEO('f03a', [
    ('line', _q03_base()),
    ('a', [('circ', _qA[0], _qA[1], 10, 'red', 3)]),
    ('sq', [rt(_qA, _qB, _qD, 13, 'orange'), at(_qA, '90°', -36, 40, 'orange', 22)]),
    ('pe', [ang(_qA, _qB, _qG, 22, 'teal'), at(_qA, '108°', 46, 30, 'teal', 22)]),
    ('gap', [ang(_qA, _qD, _qG, 30, 'red'), at(_qA, '162°', -40, -34, 'red', 22)]),
], vb='150 40 340 220', w=520, title='A square and a regular pentagon'))
f03b = PIN(GEO('f03b', [
    ('line', _q03_base([ang(_qA, _qD, _qG, 30, 'red'), at(_qA, '162°', 0, -40, 'red', 22)])),
    ('t', [('tint', [_qA, _qD, _qG], 'teal'), tk(_qA, _qD, 1), tk(_qA, _qB, 1), tk(_qA, _qG, 1)]),
    ('b', [ang(_qD, _qA, _qG, 60, 'orange'), at(_qD, '9°', 74, -10, 'orange', 22), ang(_qG, _qD, _qA, 60, 'orange'), at(_qG, '9°', -50, 16, 'orange', 22)]),
], vb='150 40 340 220', w=520, title='Triangle A D G'))
for _g in (f03a, f03b): LEFT(_g, y=QY('q03', 330), x=410, w=560)
f03r1 = IH('f03r1', '$360° - 90° = 270°$', size=34)
f03r2 = IH('f03r2', '$270° - 108° = 162°$', size=34)
f03s1 = IH('f03s1', '$AD = AB = AG$', size=34)
f03s2 = IH('f03s2', '$180° - 162° = 18°$', size=34)
f03s3 = IH('f03s3', '$18° \\div 2 = 9°$', size=34)
FLOW([f03r1, f03r2], [(1000, 580, 330, 700)])
FLOW([f03s1, f03s2, f03s3], [(1000, 580, 330, 700)])
NOFIG('solve-q-r26-t34-03', 0, 1)

video('solve-q-r26-t34-03', 'solution', qid='q-r26-t34-03', slides=[
    S('Around point A',
      L("Square A B C D and regular pentagon A B E F G share the side A B. They are on opposite sides of A B, as in the "
        "figure. What is the size of angle A D G?", pt('stem', 'Square A B C D and regular pentagon', 'hl', 8.0),
        show(f03a['line'], 'Square A B C D'), voice='calm', pause=0.5),
      L("Like in the lesson, two regular polygons sit on a common side. So first we look at the angles around the shared "
        "corner. Then we look for an isosceles triangle."),
      L("Let's start at the shared corner, A. Three angles sit around it. The square's angle, the pentagon's angle, and "
        "the gap between them, angle D A G.", show(f03a['a'], 'the shared corner, A')),
      L("The square's angle is ninety. The pentagon's angle is one hundred eight, like in the lesson. All the angles "
        "around a point add up to three hundred sixty.",
        show(f03a['sq'], "The square's angle is ninety"), show(f03a['pe'], "The pentagon's angle")),
      L("So angle D A G is three hundred sixty, minus ninety, minus one hundred eight. Three hundred sixty minus ninety is "
        "two hundred seventy. Two hundred seventy minus one hundred eight is one hundred sixty-two.",
        show(f03r1, 'Three hundred sixty minus ninety'), show(f03r2, 'Two hundred seventy minus'), show(f03a['gap'], 'one hundred sixty-two.'))),
    S('The isosceles triangle',
      L("Now look at triangle A D G. A D is a side of the square, so it's equal to A B. A G is a side of the pentagon, so "
        "it's also equal to A B. So A D is equal to A G, and the triangle is isosceles.",
        show(f03b['line'], 'Now look at triangle A D G'), show(f03b['t'], 'A D is a side of the square'), show(f03s1, 'So A D is equal to A G')),
      L("Its top angle, at A, is one hundred sixty-two. The two base angles share one hundred eighty minus one hundred "
        "sixty-two, eighteen.", show(f03s2, 'one hundred eighty minus one hundred')),
      L("Careful, eighteen is choice number one, but it's both base angles together. Each one is half of eighteen, nine. "
        "So angle A D G is nine. Choice number two is our answer, and I'll see you in the next question.",
        mk('cross', 'choice 1', 'eighteen is choice number one'), show(f03s3, 'Each one is half of eighteen'),
        show(f03b['b'], 'So angle A D G is nine'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])
# 21 Oct clarity review: preserve the board and methods; derived figure values wait for their spoken conclusions.
def _cue_pos(say,c):
    ph=c[2] if c[0] in ('show','point') else c[3]
    return -1 if ph.startswith('<') else say.lower().find(ph.lower())

def _later(vid,name,anchor):
    found=0
    for sl in VIDEOS[vid]['slides']:
        for ln in sl['lines']:
            for j,c in enumerate(ln['cues']):
                if c[0]=='show' and c[1]['_name']==name:
                    assert anchor.lower() in ln['say'].lower(),(vid,name,anchor)
                    ln['cues'][j]=show(c[1],anchor);found+=1
            ln['cues'].sort(key=lambda c:_cue_pos(ln['say'],c))
    assert found==1,(vid,name,found)

def _move(vid,name,contains,anchor):
    lines=[ln for sl in VIDEOS[vid]['slides'] for ln in sl['lines']]
    cue=[c for ln in lines for c in ln['cues'] if c[0]=='show' and c[1]['_name']==name]
    target=[ln for ln in lines if contains.lower() in ln['say'].lower()]
    assert len(cue)==len(target)==1,(vid,name,len(cue),len(target))
    assert anchor.lower() in target[0]['say'].lower(),(vid,name,anchor)
    for ln in lines:ln['cues']=[c for c in ln['cues'] if c is not cue[0]]
    target[0]['cues'].append(show(cue[0][1],anchor))
    target[0]['cues'].sort(key=lambda c:_cue_pos(target[0]['say'],c))

for _v,_nm,_ph in [
 ('geo-105','p105house_tr','half of that is twelve'),
 ('geo-105','p105h2','half of that is twelve'),
 ('geo-105','p105L_b','Ten times three is thirty'),
 ('geo-105','p105L2_miss','Six times three is eighteen'),
 ('geo-105','p105hex_one','So one triangle is four root three'),
 ('geo-105','p105x2','So one triangle is four root three'),
 ('geo-105','p105oct_sq','two times two, four'),
 ('geo-105','p105o5','half of that is one'),
 ('geo-105','p105oct_rect',"So it's two root two"),
 ('geo-105','p105o7',"That's eight plus eight root two"),
 ('solve-geo34-g106','f106b_ahd','H D, is eight'),
 ('solve-geo34-g106','f106c_sq','two hundred twenty-five'),
 ('solve-geo34-g106','f106c_ahd','divided by two, sixty'),
 ('solve-geo34-g106','f106t4','is three hundred forty-five'),
 ('solve-geo34-g108','f108a_sq','ten times ten, one hundred'),
 ('solve-geo34-g108','f108p2','So the area is eighteen plus eighteen'),
 ('solve-geo34-g108','f108p3','So the area is ninety-eight plus'),
 ('geo-109','p109c_a4','each base angle is forty-five'),
 ('geo-109','p109c_a5','Half of seventy-two is thirty-six'),
 ('geo-109','p109c_a6','So each base angle is thirty'),
 ('geo-109','p109cut_sides','long leg is a over two, times root three'),
 ('geo-109','p109n1','And the short diagonal is two root three'),
 ('geo-109','p109n2','short diagonal is five root three'),
 ('geo-109','p109n3','which is three root three'),
 ('solve-geo34-g110','f110a_stp','So angle T S P is thirty-six too'),
 ('solve-geo34-g110','f110b_a1','seventy-two'),
 ('solve-geo34-g110','f110b_a2','so angle T S Q is seventy-two'),
 ('solve-geo34-g111','f111a_cent','So both angles are forty'),
 ('solve-geo34-g111','f111u2','its perimeter is less than seven r'),
 ('solve-geo34-g111','f111u3','perimeter is more than five r'),
 ('solve-geo34-g112','f112s5','So the perimeter is twenty-eight root three'),
 ('geo-112-after','p112std_t','is exactly one sixth'),
 ('geo-112-after','p112n2','is four root three'),
 ('geo-112-after','p112n3',"That's four root three again"),
 ('solve-geo34-g112-area','f112a2','so the base A C is ten root three'),
 ('solve-geo34-g113','f113r6','And three is less than five'),
 ('solve-geo34-g113','f113s1','eighteen, not twenty'),
 ('solve-geo34-g114','f114r2','two times one, two'),
 ('solve-geo34-g115','f115r4','The shaded area is twelve plus'),
 ('solve-geo34-g116','f116s1','an octagon is one thousand eighty'),
 ('solve-geo34-g116','f116s3',"That's nine sides"),
 ('solve-geo34-g116','f116s4',"That's our sum, with ten sides"),
 ('solve-geo34-g117','f117r4','Together, one thousand eighty'),
 ('solve-q-r26-t34-02','f02r2','n is seven plus three, ten'),
 ('solve-q-r26-t34-02','f02s3','and half of that is five'),
 ('r26-t34-meet','p_two_a','Minus one hundred eight is one hundred thirty-two'),
]: _later(_v,_nm,_ph)

# carry-over boxes on the continuation slides (V2): the next step uses these results
CARRY34 = globals().get('CARRY34', {})

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
STEMS = {
 "geo34-g106": "In pentagon ABCDE, angles B, C and E are right angles, and AB is parallel to CD. Given:\n$\\begin{cases} AB=BC=AE=15 \\text{ cm} \\\\ DE=8 \\text{ cm} \\end{cases}$\nWhat is the area of the pentagon (in cm²)?",
 "geo34-g107": "A regular hexagon has side length 12 cm. What is its area (in cm²)?",
 "geo34-g108": "A regular octagon has side length 10 cm. What is its area (in cm²)?",
 "geo34-g110": "PQRST is a regular pentagon. What is the size of angle PSQ (marked $x$ in the figure)?",
 "geo34-g111": "A regular 9-sided polygon ABCDEFGHI is inscribed in a circle with center O and radius r. Which of the following statements is not true?",
 "geo34-g112": "ABCDEF is a regular hexagon. The perimeter of triangle ACE is 42 cm. What is the perimeter of the hexagon (in cm)?",
 "geo34-g112-area": "ABCDEF is a regular hexagon of side 10 cm. What is the sum of the areas of triangles ABC, CDE and EFA (in cm²)?",
 "geo34-g113": "Five squares are constructed externally on five sides of a regular hexagon. Ella claims that the sum of the five square perimeters is 3 times the hexagon perimeter. Adam claims that the sum of the five square areas is greater than the hexagon area. Which of the following is true?",
 "geo34-g114": "The accompanying figure shows a regular octagon. KL and MN are perpendicular and intersect at T. K, L, M and N are vertices of the octagon, as shown in the figure. Sara claims that $LT>2KT$. Ben claims that the perimeter of triangle KMT equals MN. Which of the following is true?",
 "geo34-g115": "The accompanying figure shows a regular octagon divided by two vertical segments. The central white rectangle has area $12+12\\sqrt2$ cm². What is the sum of the shaded areas (in cm²)?",
 "geo34-g116": "The sum of the interior angles of a polygon is 1,440°. How many sides does it have?",
 "geo34-g117": "A is the sum of the interior angles of a 14-sided polygon, and B is the sum of the interior angles of a 20-sided polygon. The difference $B-A$ equals the sum of the interior angles of which polygon?",
 "q-r26-t34-01": "Each interior angle of a regular polygon is $160°$. How many sides does the polygon have?",
 "q-r26-t34-02": "From one vertex of a polygon, exactly 7 diagonals can be drawn. How many diagonals does the polygon have in all?",
 "q-r26-t34-03": "Square ABCD and regular pentagon ABEFG share the side AB. They lie on opposite sides of AB, as shown in the figure. What is the size of angle ADG?"
}   # "=?" stems and stems with no "Given:": the whole stem only
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



# (topic 34) the row placements are made next to each video


# the camera lesson in parts of about 3-4 minutes (math_patches/_camera_parts.py), before the visual passes
_cp_spec = importlib.util.spec_from_file_location('_camera_parts', os.path.join(HERE, '_camera_parts.py'))
CP = importlib.util.module_from_spec(_cp_spec); _cp_spec.loader.exec_module(CP)
if 'CAMERA_SPLIT' in globals(): CP.split(globals(), *CAMERA_SPLIT)
for _sp in globals().get('MORE_SPLITS', []): CP.split(globals(), *_sp)     # (topic 34) a long lesson in parts, not on camera

for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _stem_parts(_v); _write_gap(_v)



# 2026-10-13 carry-over boxes (V2) and the layer-order check (V1): after the visual passes, like topics 13-18
import types as _types
MV.carry(_types.SimpleNamespace(**globals()), CARRY34)
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
