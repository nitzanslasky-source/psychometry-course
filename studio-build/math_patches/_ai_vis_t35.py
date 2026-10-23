"""Topic 35 (Three-dimensional geometry) - the scripts for the teacher's own-voice reading (2026-10-22), written from the
first draft to the guide (R1-R37, W1-W25), the clarity style, the Codex review standard and Rule V3/V4 geometry visuals,
built exactly like topic 34 (math_patches/_ai_vis_t34.py: the DSL, the GEO colour builders, the geometry handwriting hook
and the visual passes are copied here, so the topics stay independent).

The camera lesson 'geo-119' gets its own reading script, in parts of about 3-4 minutes (CAMERA_SPLIT at the end). Every
other topic-35 video gets a script that SHE reads aloud in the Reading Studio; reading_to_video.py times the handwriting
and the visuals to her words. The summary video r26-t35-summary is replaced by the printable page summary_pages/t35.json.

ONE spec per video drives the script (ai_scripts/<vid>.json), the visual plan (VIS[vid], _ai_visual.py format) and the
studio video (t35.py ai_redo_t35() rebuilds the slides from studio_slides(vid), then _ai_visual.apply()).

R37 (2026-10-21): the core methods of solids are taught in the LESSONS - geo-119 (camera, 5 parts): the words, prisms,
the cylinder, lateral area = base perimeter x height, total surface = lateral + 2 bases, volume = base area x height,
pointed = one third; geo-120 (3 parts, was an overview): volume ratios and ratio units, right triangles inside solids
(the height, the cone, the pyramid, the cube's diagonals), surfaces of solids made of cubes (count by direction, a
contact hides two faces, a cut adds two faces); r26-t35-water: units, water height, pouring, sinking an object;
(r26-t35-cones, solids made by turning, removed 2026-10-23); r26-t35-cubefacts: the longest segment in a box and in a cylinder, counting faces,
edges and vertices, three face areas. The first question that uses a method applies it slowly with a one-sentence link to
the lesson; one-off tricks (the three angles in a cube, the corner / edge / face-centre cube, the painted cube, solids in a
box) are taught in their question.

Spec DSL (as in topic 34): video / S / SM / L / I / IH / show / pt / mk / GEO / PIN / _R / LEFT / ROWS / FLOW, plus the
solid helpers (boxpts, box_el, cyl_el, cone_el, pyr_el, unit_cubes, pj, G, H35).
"""
import importlib.util, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _geo_hand as _GH

HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t35ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-35 flow order of the scripts
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
CAM_BASE = 'geo-119'
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
               for it, d in sl):     # topic 35: every right-column stack of a camera part starts below the bubble
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
            'style': "the teacher reads it herself (Reading Studio), topic-35 scripts (2026-10-22): math_patches/_ai_vis_t35.py is "
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
        if (vid, k) in NOFIG35:
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



CARRY35 = {}       # carry-over boxes (V2): {vid: {slide index: [tex, ...]}}, filled by the scripts


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
NOFIG35 = set()       # 2026-10-18 (batch C, as NOFIG31 in topic 31): (video, slide index) that show our enlarged copy
                      # instead of the question figure; the working is written in readable rows on the right (ROWS)


def LEFT(g, y=300, x=410, w=None):
    """(batch C) place a GEO figure (every layer) in the left work area of a NOFIG35 slide, optionally at a new width"""
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






# ------------------------------------------------------------------------------------------------ topic-35 solid helpers
# 2026-10-22 three-dimensional figures for the GEO builder (coordinates: SVG units, y down). An oblique view: x to the
# right, y up, depth z drawn up and to the right (k = (0.55, 0.36) per unit of depth). The given solid is ink with light
# grey faces and dashed grey hidden edges (black and white, like the exam); everything we add is teal / orange / red.
# Elements are the GEO ones ('raw' for the filled faces and the ellipses).
FACE_F, FACE_T, FACE_R, HID = '#f8fbfd', '#eef2f6', '#e2e8ee', '#71818d'
KX, KY = 0.55, 0.36


def _praw(pts, fill, stroke='none', sw=0, op=None):
    return ('raw', '<path d="M %s Z" fill="%s"%s stroke="%s" stroke-width="%s" stroke-linejoin="round"/>'
            % (' L '.join('%.1f %.1f' % tuple(p) for p in pts), fill, (' opacity="%s"' % op) if op else '', stroke, sw))


def hid(P, Q):
    """a hidden edge: dashed grey"""
    return ('raw', '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2" stroke-dasharray="7 6"/>'
            % (P[0], P[1], Q[0], Q[1], HID))


def boxpts(x0, y0, W, H, D, kx=KX, ky=KY):
    """the 8 corners of a box: A B C D the bottom (A front left, B front right, C back right, D back left), E F G H the
    top above them. (x0, y0) = A; W, H, D in SVG units (D = the depth, drawn up and to the right)."""
    dx, dy = D * kx, -D * ky
    A = (x0, y0); B = (x0 + W, y0); C = (x0 + W + dx, y0 + dy); Dd = (x0 + dx, y0 + dy)
    E = (x0, y0 - H); F = (x0 + W, y0 - H); G = (x0 + W + dx, y0 - H + dy); Hh = (x0 + dx, y0 - H + dy)
    return dict(A=A, B=B, C=C, D=Dd, E=E, F=F, G=G, H=Hh)


def box_el(P, fill=True, w=3):
    """a box (or a cube) from boxpts: three faces filled, visible edges ink, the three hidden edges dashed"""
    e = []
    if fill:
        e += [_praw([P['A'], P['B'], P['F'], P['E']], FACE_F), _praw([P['B'], P['C'], P['G'], P['F']], FACE_R),
              _praw([P['E'], P['F'], P['G'], P['H']], FACE_T)]
    e += [hid(P['A'], P['D']), hid(P['D'], P['C']), hid(P['D'], P['H'])]
    for a, b in ['AB', 'BF', 'FE', 'EA', 'BC', 'CG', 'GF', 'GH', 'HE']:
        e.append(('seg', P[a][0], P[a][1], P[b][0], P[b][1], 'ink', w, False))
    return e


def names(P, keys='ABCDEFGH', off=None, size=26, col='ink'):
    """the corner letters, pushed away from the box's middle"""
    cx = sum(P[k][0] for k in 'ABCDEFGH') / 8.0; cy = sum(P[k][1] for k in 'ABCDEFGH') / 8.0
    out = []
    for k in keys:
        if off and k in off: out.append(('txt', P[k][0] + off[k][0], P[k][1] + off[k][1], k, col, size, True)); continue
        dx, dy = P[k][0] - cx, P[k][1] - cy; L = _pm.hypot(dx, dy) or 1
        out.append(('txt', P[k][0] + dx / L * 24, P[k][1] + dy / L * 24, k, col, size, True))
    return out


def _ell(cx, cy, rx, ry, part='full', col=GINK, w=3, dash=False, fill='none'):
    """an ellipse: part 'full', 'front' (the lower half, seen) or 'back' (the upper half, hidden)"""
    d = ' stroke-dasharray="7 6"' if dash else ''
    if part == 'full':
        return ('raw', '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>'
                % (cx, cy, rx, ry, fill, col, w, d))
    sweep = 0 if part == 'front' else 1
    return ('raw', '<path d="M %.1f %.1f A %.1f %.1f 0 0 %d %.1f %.1f" fill="none" stroke="%s" stroke-width="%s"%s/>'
            % (cx - rx, cy, rx, ry, sweep, cx + rx, cy, col, w, d))


def cyl_el(cx, yb, r, h, ry=None):
    """an upright cylinder: bottom centre (cx, yb), radius r, height h (SVG units)"""
    ry = ry or r * 0.3; yt = yb - h
    side = ('raw', '<path d="M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f L %.1f %.1f Z" fill="%s" stroke="none"/>'
            % (cx - r, yt, cx - r, yb, r, ry, cx + r, yb, cx + r, yt, FACE_R))
    return [side, _ell(cx, yt, r, ry, 'full', fill=FACE_T), _ell(cx, yb, r, ry, 'back', HID, 2, True),
            _ell(cx, yb, r, ry, 'front'), ('seg', cx - r, yt, cx - r, yb, 'ink', 3, False),
            ('seg', cx + r, yt, cx + r, yb, 'ink', 3, False)]


def cone_el(cx, yb, r, h, ry=None):
    """an upright cone: base centre (cx, yb), radius r, height h; apex (cx, yb - h)"""
    ry = ry or r * 0.3; ax, ay = cx, yb - h
    body = ('raw', '<path d="M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f Z" fill="%s" stroke="none"/>'
            % (ax, ay, cx - r, yb, r, ry, cx + r, yb, FACE_R))
    return [body, _ell(cx, yb, r, ry, 'back', HID, 2, True), _ell(cx, yb, r, ry, 'front'),
            ('seg', ax, ay, cx - r, yb, 'ink', 3, False), ('seg', ax, ay, cx + r, yb, 'ink', 3, False)]


def pyr_el(P, apex, w=3):
    """a pyramid on the base A B C D of boxpts P (a square or rectangle), apex = a point above the base's centre"""
    A, B, C, Dd = P['A'], P['B'], P['C'], P['D']
    e = [_praw([A, B, apex], FACE_F), _praw([B, C, apex], FACE_R)]
    e += [hid(A, Dd), hid(Dd, C), hid(Dd, apex)]
    for p, q in [(A, B), (B, C), (A, apex), (B, apex), (C, apex)]:
        e.append(('seg', p[0], p[1], q[0], q[1], 'ink', w, False))
    return e


def unit_cubes(cells, x0, y0, s, kx=KX, ky=KY, fills=None, w=2):
    """solid built of unit cubes: cells = [(i, j, k)] (i right, j up, k depth); front bottom left corner of cell (0,0,0)
    at (x0, y0), edge s. fills = {(i, j, k): (front, top, right) colours} for marked cubes. Drawn back to front."""
    out = []
    dx, dy = s * kx, -s * ky
    for (i, j, k) in sorted(cells, key=lambda c: (-c[2], c[1], c[0])):
        bx, by = x0 + i * s + k * dx, y0 - j * s + k * dy
        f = (fills or {}).get((i, j, k), (FACE_F, FACE_T, FACE_R))
        fr = [(bx, by), (bx + s, by), (bx + s, by - s), (bx, by - s)]
        tp = [(bx, by - s), (bx + s, by - s), (bx + s + dx, by - s + dy), (bx + dx, by - s + dy)]
        rt_ = [(bx + s, by), (bx + s + dx, by + dy), (bx + s + dx, by - s + dy), (bx + s, by - s)]
        for poly, c in ((fr, f[0]), (tp, f[1]), (rt_, f[2])):
            out.append(_praw(poly, c, GINK, w))
    return out


def cube_face(i, j, k, face, x0, y0, s, kx=KX, ky=KY):
    """the screen polygon of one face ('front', 'top', 'right', 'back', 'left', 'bottom') of the unit cell (i, j, k)"""
    dx, dy = s * kx, -s * ky
    bx, by = x0 + i * s + k * dx, y0 - j * s + k * dy
    if face == 'front': return [(bx, by), (bx + s, by), (bx + s, by - s), (bx, by - s)]
    if face == 'top': return [(bx, by - s), (bx + s, by - s), (bx + s + dx, by - s + dy), (bx + dx, by - s + dy)]
    if face == 'right': return [(bx + s, by), (bx + s + dx, by + dy), (bx + s + dx, by - s + dy), (bx + s, by - s)]
    if face == 'back': return [(bx + dx, by + dy), (bx + s + dx, by + dy), (bx + s + dx, by - s + dy), (bx + dx, by - s + dy)]
    if face == 'left': return [(bx, by), (bx + dx, by + dy), (bx + dx, by - s + dy), (bx, by - s)]
    if face == 'bottom': return [(bx, by), (bx + s, by), (bx + s + dx, by + dy), (bx + dx, by + dy)]
    raise ValueError(face)


def qraw(qid):
    """the question's own black-and-white figure (its SVG body), as the base of our colour copy"""
    svg = QSVG[qid]
    return ('raw', re.sub(r'^.*?</title>|</svg>\s*$', '', svg, flags=re.S))


def tri_el(P, Q, R, col='teal', w=4):
    return [('tint', [P, Q, R], col), ('poly', [P, Q, R], col, w)]


def pj(x0, y0, X, Y, Z, kx=KX, ky=KY):
    """project a 3D point (X right, Y up, Z depth) of a solid whose origin is drawn at (x0, y0)"""
    return (x0 + X + Z * kx, y0 - Y - Z * ky)


def edges_el(pairs, w=3):
    """visible edges (ink) and hidden ones (dashed grey): pairs = [(P, Q, visible?)]"""
    return [('seg', p[0], p[1], q[0], q[1], 'ink', w, False) if v else hid(p, q) for p, q, v in pairs]


def G(name, layers, vb, w=520, col=0, title='Figure'):
    """a lesson figure in the left column, built in layers (PIN: the layers stay on their base)"""
    return PIN(GEO(name, layers, vb=vb, w=w, col=col, title=title))


def H35(name, tex, size=34, col=1):
    """a hand-written row in the right column of a lesson"""
    return IH(name, tex, size=size, col=col)


def water_el(P, frac, col='teal'):
    """water filling the box P up to frac of its height: the front and right faces of the water and its surface"""
    lv = lambda a, b: (a[0] + (b[0] - a[0]) * frac, a[1] + (b[1] - a[1]) * frac)
    e1, f1, g1, h1 = lv(P['A'], P['E']), lv(P['B'], P['F']), lv(P['C'], P['G']), lv(P['D'], P['H'])
    return [('tint', [P['A'], P['B'], f1, e1], col), ('tint', [P['B'], P['C'], g1, f1], col),
            ('tint', [e1, f1, g1, h1], col), ('poly', [e1, f1, g1, h1], col, 2.5)]


# the questions' own black-and-white figures (questionVisual of the built course, 22 Oct 2026): the base of our copies
QSVG = {
 'geo35-g121': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Right circular cone"><title>Right circular cone</title><polygon points="271.214,299.455 368.786,299.455 320.000,60.455" fill="#d9d9d9" stroke="none" stroke-width="2.5" stroke-linejoin="round"/><path d="M 271.214 299.455 A 48.786 13.660 0 0 1 368.786 299.455" fill="none" stroke="#000000" stroke-width="2" stroke-dasharray="6 5"/><path d="M 271.214 299.455 A 48.786 13.660 0 0 0 368.786 299.455" fill="none" stroke="#000000" stroke-width="2.5"/><line x1="271.214" y1="299.455" x2="320.000" y2="60.455" stroke="#000000" stroke-width="2.5"/><line x1="320.000" y1="60.455" x2="368.786" y2="299.455" stroke="#000000" stroke-width="2.5"/><line x1="320.000" y1="299.455" x2="320.000" y2="60.455" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="320.000" y1="299.455" x2="368.786" y2="299.455" stroke="#000000" stroke-width="2.5"/><text x="261.607" y="179.955" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">12</text><text x="344.393" y="319.455" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">√6</text></svg>',
 'q-r26-t35-01': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Water in a box with base 10 by 8 reaches height 9; an empty cube with edge 12"><title>Water in a box with base 10 by 8 reaches height 9; an empty cube with edge 12</title><polygon points="60.000,300.000 210.000,300.000 210.000,110.000 60.000,110.000" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="210.000,300.000 282.000,255.000 282.000,65.000 210.000,110.000" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="60.000,110.000 210.000,110.000 282.000,65.000 132.000,65.000" fill="#eeeeee" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="60.000,300.000 210.000,300.000 210.000,180.000 60.000,180.000" fill="#d9d9d9" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="210.000,300.000 282.000,255.000 282.000,135.000 210.000,180.000" fill="#d9d9d9" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="60.000,180.000 210.000,180.000 282.000,135.000 132.000,135.000" fill="#bfbfbf" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><line x1="60.000" y1="300.000" x2="210.000" y2="300.000" stroke="#000000" stroke-width="2.5"/><line x1="210.000" y1="300.000" x2="210.000" y2="110.000" stroke="#000000" stroke-width="2.5"/><line x1="210.000" y1="110.000" x2="60.000" y2="110.000" stroke="#000000" stroke-width="2.5"/><line x1="60.000" y1="110.000" x2="60.000" y2="300.000" stroke="#000000" stroke-width="2.5"/><line x1="210.000" y1="300.000" x2="282.000" y2="255.000" stroke="#000000" stroke-width="2.5"/><line x1="282.000" y1="255.000" x2="282.000" y2="65.000" stroke="#000000" stroke-width="2.5"/><line x1="282.000" y1="65.000" x2="210.000" y2="110.000" stroke="#000000" stroke-width="2.5"/><line x1="282.000" y1="65.000" x2="132.000" y2="65.000" stroke="#000000" stroke-width="2.5"/><line x1="132.000" y1="65.000" x2="60.000" y2="110.000" stroke="#000000" stroke-width="2.5"/><line x1="60.000" y1="300.000" x2="132.000" y2="255.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="132.000" y1="255.000" x2="282.000" y2="255.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="132.000" y1="255.000" x2="132.000" y2="65.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="135.000" y="322.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">10</text><text x="242.000" y="296.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">8</text><text x="40.000" y="240.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">9</text><polygon points="350.000,300.000 540.000,300.000 540.000,110.000 350.000,110.000" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="540.000,300.000 628.000,245.000 628.000,55.000 540.000,110.000" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="350.000,110.000 540.000,110.000 628.000,55.000 438.000,55.000" fill="#eeeeee" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="350.000" y1="300.000" x2="438.000" y2="245.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="438.000" y1="245.000" x2="628.000" y2="245.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="438.000" y1="245.000" x2="438.000" y2="55.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="445.000" y="322.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">12</text></svg>',
 'geo35-g122': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="A cylinder with height h and a cone with height H, side by side, with equal bases"><title>A cylinder with height h and a cone with height H, side by side, with equal bases</title><polygon points="153.000,285.000 277.000,285.000 277.000,165.000 153.000,165.000" fill="#d9d9d9" stroke="none" stroke-width="0" stroke-linejoin="round"/><ellipse cx="215.000" cy="285.000" rx="62.000" ry="17.000" fill="#d9d9d9" stroke="none" stroke-width="0"/><path d="M 153.000 285.000 A 62.000 17.000 0 0 1 277.000 285.000" fill="none" stroke="#000000" stroke-width="2" stroke-dasharray="6 5"/><path d="M 153.000 285.000 A 62.000 17.000 0 0 0 277.000 285.000" fill="none" stroke="#000000" stroke-width="2.5"/><line x1="153.000" y1="285.000" x2="153.000" y2="165.000" stroke="#000000" stroke-width="2.5"/><line x1="277.000" y1="285.000" x2="277.000" y2="165.000" stroke="#000000" stroke-width="2.5"/><ellipse cx="215.000" cy="165.000" rx="62.000" ry="17.000" fill="white" stroke="#000000" stroke-width="2.5"/><line x1="295.000" y1="285.000" x2="295.000" y2="165.000" stroke="#000000" stroke-width="2" stroke-dasharray="7 5"/><text x="311.000" y="225.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">h</text><polygon points="368.000,285.000 492.000,285.000 430.000,95.000" fill="#d9d9d9" stroke="none" stroke-width="0" stroke-linejoin="round"/><ellipse cx="430.000" cy="285.000" rx="62.000" ry="17.000" fill="#d9d9d9" stroke="none" stroke-width="0"/><path d="M 368.000 285.000 A 62.000 17.000 0 0 1 492.000 285.000" fill="none" stroke="#000000" stroke-width="2" stroke-dasharray="6 5"/><path d="M 368.000 285.000 A 62.000 17.000 0 0 0 492.000 285.000" fill="none" stroke="#000000" stroke-width="2.5"/><line x1="368.000" y1="285.000" x2="430.000" y2="95.000" stroke="#000000" stroke-width="2.5"/><line x1="492.000" y1="285.000" x2="430.000" y2="95.000" stroke="#000000" stroke-width="2.5"/><line x1="430.000" y1="95.000" x2="430.000" y2="285.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="446.000" y="190.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">H</text></svg>',
 'geo35-g123': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Box with hidden edges shown dashed"><title>Box with hidden edges shown dashed</title><polygon points="135.388,277.736 424.975,277.736 424.975,132.942 135.388,132.942" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="424.975,277.736 504.612,227.058 504.612,82.264 424.975,132.942" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="135.388,132.942 424.975,132.942 504.612,82.264 215.025,82.264" fill="#eeeeee" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="135.388" y1="277.736" x2="215.025" y2="227.058" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="215.025" y1="227.058" x2="504.612" y2="227.058" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="215.025" y1="227.058" x2="215.025" y2="82.264" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="120.388" y="290.736" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="434.975" y="295.736" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="522.612" y="234.058" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="199.025" y="224.058" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="120.388" y="117.942" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">E</text><text x="434.975" y="117.942" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">F</text><text x="520.612" y="69.264" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">G</text><text x="203.025" y="64.264" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">H</text><polygon points="135.388,277.736 207.785,277.736 215.025,227.058" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="135.388,132.942 207.785,132.942 215.025,82.264" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="207.785" y1="277.736" x2="207.785" y2="132.942" stroke="#000000" stroke-width="2.5"/><line x1="215.025" y1="227.058" x2="215.025" y2="82.264" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="207.785" y="297.736" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">M</text><text x="207.785" y="113.942" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">N</text><text x="171.586" y="314.736" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">x</text><text x="316.380" y="314.736" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">3x</text></svg>',
 'geo35-g124': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="A right triangular prism with congruent triangular bases"><title>A right triangular prism with congruent triangular bases</title><polygon points="411.000,307.000 463.000,274.000 292.000,46.000 240.000,79.000" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="240.000,307.000 411.000,307.000 240.000,79.000" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="240.000" y1="307.000" x2="292.000" y2="274.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="292.000" y1="274.000" x2="463.000" y2="274.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="292.000" y1="274.000" x2="292.000" y2="46.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="240.000" y1="79.000" x2="292.000" y2="46.000" stroke="#000000" stroke-width="2.5"/><line x1="463.000" y1="274.000" x2="292.000" y2="46.000" stroke="#000000" stroke-width="2.5"/><line x1="250.000" y1="307.000" x2="250.000" y2="297.000" stroke="#000000" stroke-width="1.7"/><line x1="250.000" y1="297.000" x2="240.000" y2="297.000" stroke="#000000" stroke-width="1.7"/><text x="225.000" y="319.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="415.000" y="325.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="225.000" y="64.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="279.000" y="267.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="481.000" y="282.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">E</text><text x="300.000" y="27.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">F</text><text x="325.500" y="328.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">9</text><text x="343.700" y="240.600" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">15</text><text x="449.000" y="304.500" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">5</text></svg>',
 'geo35-g126': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Top view: a circle inscribed in a square of side 2a"><title>Top view: a circle inscribed in a square of side 2a</title><polygon points="215.714,284.286 424.286,284.286 424.286,75.714 215.714,75.714" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><circle cx="320.000" cy="180.000" r="104.286" fill="#d9d9d9" stroke="#000000" stroke-width="2.5"/><line x1="320.000" y1="180.000" x2="424.286" y2="180.000" stroke="#000000" stroke-width="2.5"/><circle cx="320.000" cy="180.000" r="3.2" fill="#000000"/><text x="320.000" y="308.286" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">2k</text></svg>',
 'geo35-g127': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Box with hidden edges shown dashed"><title>Box with hidden edges shown dashed</title><polygon points="197.676,286.541 355.514,286.541 355.514,128.703 197.676,128.703" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="355.514,286.541 442.324,231.297 442.324,73.459 355.514,128.703" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="197.676,128.703 355.514,128.703 442.324,73.459 284.486,73.459" fill="#eeeeee" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="197.676" y1="286.541" x2="284.486" y2="231.297" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="284.486" y1="231.297" x2="442.324" y2="231.297" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="284.486" y1="231.297" x2="284.486" y2="73.459" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="182.676" y="299.541" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="365.514" y="304.541" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="460.324" y="238.297" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="268.486" y="228.297" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="182.676" y="113.703" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">E</text><text x="365.514" y="113.703" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">F</text><text x="458.324" y="60.459" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">G</text><text x="272.486" y="55.459" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">H</text><line x1="302.243" y1="87.270" x2="197.676" y2="286.541" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="302.243" y1="87.270" x2="355.514" y2="286.541" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="302.243" y1="87.270" x2="442.324" y2="231.297" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="302.243" y1="87.270" x2="284.486" y2="231.297" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="302.243" y="69.270" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">P</text></svg>',
 'geo35-g128': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Square pyramid and its perpendicular height"><title>Square pyramid and its perpendicular height</title><polygon points="175.326,300.668 362.002,300.668 320.000,78.429" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="362.002,300.668 464.674,235.332 320.000,78.429" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="175.326" y1="300.668" x2="277.998" y2="235.332" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="277.998" y1="235.332" x2="464.674" y2="235.332" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="277.998" y1="235.332" x2="320.000" y2="78.429" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="320.000" y1="78.429" x2="320.000" y2="268.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><circle cx="320.000" cy="268.000" r="3.2" fill="#000000"/><text x="161.326" y="316.668" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="368.002" y="320.668" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="482.674" y="241.332" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="265.998" y="225.332" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="320.000" y="58.429" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">P</text><text x="300.000" y="268.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">O</text><text x="268.664" y="324.668" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">4√2</text><text x="357.001" y="189.549" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">7</text></svg>',
 'q-r26-t35-02': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="A cone with base radius 6 and slant height 10"><title>A cone with base radius 6 and slant height 10</title><polygon points="215.000,280.000 425.000,280.000 320.000,80.000" fill="#d9d9d9" stroke="none" stroke-width="0" stroke-linejoin="round"/><path d="M 215.000 280.000 A 105.000 28.000 0 0 1 425.000 280.000" fill="none" stroke="#000000" stroke-width="2" stroke-dasharray="6 5"/><path d="M 215.000 280.000 A 105.000 28.000 0 0 0 425.000 280.000" fill="none" stroke="#000000" stroke-width="2.5"/><line x1="215.000" y1="280.000" x2="320.000" y2="80.000" stroke="#000000" stroke-width="2.5"/><line x1="320.000" y1="80.000" x2="425.000" y2="280.000" stroke="#000000" stroke-width="3.5"/><line x1="320.000" y1="80.000" x2="320.000" y2="280.000" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="320.000" y1="270.000" x2="330.000" y2="270.000" stroke="#000000" stroke-width="1.7"/><line x1="330.000" y1="270.000" x2="330.000" y2="280.000" stroke="#000000" stroke-width="1.7"/><line x1="320.000" y1="280.000" x2="425.000" y2="280.000" stroke="#000000" stroke-width="2.5"/><text x="372.500" y="322.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">6</text><text x="394.500" y="174.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">10</text></svg>',
 'geo35-g129': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Box with hidden edges shown dashed"><title>Box with hidden edges shown dashed</title><polygon points="207.785,277.736 352.579,277.736 352.579,132.942 207.785,132.942" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="352.579,277.736 432.215,227.058 432.215,82.264 352.579,132.942" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="207.785,132.942 352.579,132.942 432.215,82.264 287.421,82.264" fill="#eeeeee" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="207.785" y1="277.736" x2="287.421" y2="227.058" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="287.421" y1="227.058" x2="432.215" y2="227.058" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="287.421" y1="227.058" x2="287.421" y2="82.264" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="192.785" y="290.736" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="362.579" y="295.736" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="450.215" y="234.058" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="271.421" y="224.058" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="192.785" y="117.942" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">E</text><text x="362.579" y="117.942" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">F</text><text x="448.215" y="69.264" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">G</text><text x="275.421" y="64.264" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">H</text><polygon points="352.579,277.736 287.421,227.058 432.215,82.264" fill="#d9d9d9" stroke="#000000" stroke-width="3" stroke-linejoin="round"/><text x="280.182" y="303.736" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">4√2</text></svg>',
 'geo35-g130': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Box with hidden edges shown dashed"><title>Box with hidden edges shown dashed</title><polygon points="207.785,277.736 352.579,277.736 352.579,132.942 207.785,132.942" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="352.579,277.736 432.215,227.058 432.215,82.264 352.579,132.942" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="207.785,132.942 352.579,132.942 432.215,82.264 287.421,82.264" fill="#eeeeee" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="207.785" y1="277.736" x2="287.421" y2="227.058" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="287.421" y1="227.058" x2="432.215" y2="227.058" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="287.421" y1="227.058" x2="287.421" y2="82.264" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="192.785" y="290.736" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="362.579" y="295.736" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="450.215" y="234.058" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="271.421" y="224.058" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="192.785" y="117.942" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">E</text><text x="362.579" y="117.942" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">F</text><text x="448.215" y="69.264" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">G</text><text x="275.421" y="64.264" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">H</text><polygon points="207.785,277.736 207.785,132.942 432.215,82.264" fill="none" stroke="#000000" stroke-width="3" stroke-linejoin="round"/><text x="280.182" y="301.736" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">3</text></svg>',
 'geo35-g131': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Box with hidden edges shown dashed"><title>Box with hidden edges shown dashed</title><polygon points="130.556,312.000 427.556,312.000 427.556,130.500 130.556,130.500" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="427.556,312.000 509.444,260.820 509.444,79.320 427.556,130.500" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="130.556,130.500 427.556,130.500 509.444,79.320 212.444,79.320" fill="#eeeeee" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="130.556" y1="312.000" x2="212.444" y2="260.820" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="212.444" y1="260.820" x2="509.444" y2="260.820" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><line x1="212.444" y1="260.820" x2="212.444" y2="79.320" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="279.056" y="334.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">18</text><text x="482.500" y="300.410" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">9</text><text x="470.500" y="195.660" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">11</text></svg>',
 'geo35-g132': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="A 3 by 3 by 3 cube with one corner cube highlighted"><title>A 3 by 3 by 3 cube with one corner cube highlighted</title><polygon points="254.367,90.257 307.945,90.257 337.413,71.505 283.835,71.505" fill="#eeeeee" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="415.101,250.991 444.569,232.239 444.569,178.661 415.101,197.413" fill="#d9d9d9" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="307.945,90.257 361.523,90.257 390.991,71.505 337.413,71.505" fill="#eeeeee" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="415.101,197.413 444.569,178.661 444.569,125.083 415.101,143.835" fill="#d9d9d9" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="224.899,109.009 278.477,109.009 307.945,90.257 254.367,90.257" fill="#eeeeee" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="361.523,90.257 415.101,90.257 444.569,71.505 390.991,71.505" fill="#eeeeee" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="415.101,143.835 444.569,125.083 444.569,71.505 415.101,90.257" fill="#d9d9d9" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="385.633,269.743 415.101,250.991 415.101,197.413 385.633,216.165" fill="#d9d9d9" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="278.477,109.009 332.055,109.009 361.523,90.257 307.945,90.257" fill="#eeeeee" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="195.431,288.495 249.009,288.495 249.009,234.917 195.431,234.917" fill="#ffffff" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="385.633,216.165 415.101,197.413 415.101,143.835 385.633,162.587" fill="#d9d9d9" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="195.431,234.917 249.009,234.917 249.009,181.339 195.431,181.339" fill="#ffffff" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="195.431,127.761 249.009,127.761 278.477,109.009 224.899,109.009" fill="#eeeeee" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="332.055,109.009 385.633,109.009 415.101,90.257 361.523,90.257" fill="#eeeeee" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="249.009,288.495 302.587,288.495 302.587,234.917 249.009,234.917" fill="#ffffff" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="385.633,162.587 415.101,143.835 415.101,90.257 385.633,109.009" fill="#d9d9d9" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="195.431,181.339 249.009,181.339 249.009,127.761 195.431,127.761" fill="#ffffff" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="356.165,288.495 385.633,269.743 385.633,216.165 356.165,234.917" fill="#d9d9d9" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="249.009,234.917 302.587,234.917 302.587,181.339 249.009,181.339" fill="#ffffff" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="249.009,127.761 302.587,127.761 332.055,109.009 278.477,109.009" fill="#eeeeee" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="302.587,288.495 356.165,288.495 356.165,234.917 302.587,234.917" fill="#ffffff" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="356.165,234.917 385.633,216.165 385.633,162.587 356.165,181.339" fill="#d9d9d9" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="249.009,181.339 302.587,181.339 302.587,127.761 249.009,127.761" fill="#ffffff" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="302.587,234.917 356.165,234.917 356.165,181.339 302.587,181.339" fill="#ffffff" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="302.587,127.761 356.165,127.761 385.633,109.009 332.055,109.009" fill="#a6a6a6" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="356.165,181.339 385.633,162.587 385.633,109.009 356.165,127.761" fill="#a6a6a6" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/><polygon points="302.587,181.339 356.165,181.339 356.165,127.761 302.587,127.761" fill="#a6a6a6" stroke="#000000" stroke-width="1.7" stroke-linejoin="round"/></svg>',
}

QSTEM = {
 "geo35-g121": "A cone-shaped container with base radius $\\sqrt6$ cm and height 12 cm is full of water. Which of the following empty containers can hold all the water? The dimensions given are internal dimensions.",
 "q-r26-t35-01": "Water in a box-shaped container with a base of 10 cm × 8 cm reaches a height of 9 cm. All the water is poured into an empty cube-shaped container with an internal edge of 12 cm. How high is the water in the cube (in cm)?",
 "geo35-g122": "A cone and a cylinder have equal base areas. The volume of the cone is four times the volume of the cylinder. If the cylinder’s height is h, what is the cone’s height?",
 "geo35-g123": "The volume of box ABCDEFGH is 320 cm³. M lies on AB so that the ratio AM : MB is 1 : 3, and N lies directly above M on EF. What is the volume of triangular prism AMD–ENH (in cm³)?",
 "geo35-g124": "The bases of a right triangular prism are right triangles. Each base has a leg of 9 cm and a hypotenuse of 15 cm. The height of the prism is 5 cm. What is its lateral surface area (in cm²)?",
 "geo35-g125": "Eighteen identical cubes, each with edge 1 cm, are joined face to face to form a rectangular block. Which of the following block dimensions gives the smallest total surface area?",
 "geo35-g126": "A cylinder is inscribed in a box whose square base has side 2k and whose height is 5k. The cylinder has the same height as the box, and its circular bases are inscribed in the square bases. What fraction of the box’s volume lies outside the cylinder?",
 "geo35-g127": "A pyramid is removed from a cube. The pyramid’s base is the entire bottom face of the cube, and its apex lies on the top face. The remaining solid has volume 60 cm³. What was the volume of the pyramid (in cm³)?",
 "geo35-g128": "A pyramid has a square base with side $4\\sqrt2$ cm. Each lateral edge is 7 cm. What is the height of the pyramid (in cm)?",
 "q-r26-t35-02": "A cone has a base radius of 6 cm and a slant height of 10 cm. What is its volume (in cm³)?",
 "geo35-g129": "The edge of cube ABCDEFGH is $4\\sqrt2$ cm. What is the area of triangle BDG (in cm²)?",
 "geo35-g130": "The edge of cube ABCDEFGH is 3 cm. What is the perimeter of triangle AEG (in cm)?",
 "geo35-g131": "Identical cubes with edge 4 cm are placed in a box with internal dimensions 18 cm × 9 cm × 11 cm. The cube edges must be parallel to the box edges. What is the greatest number of cubes that can fit entirely inside the box?",
 "geo35-g132": "Twenty-seven identical cubes, each with edge 4 cm, form a larger cube. One corner cube is removed, as shown in the accompanying figure. How do the volume and total surface area of the remaining solid change?",
 "q-r26-t35-03": "A wooden cube is painted on all six faces. Then it is cut into 125 identical small cubes, 5 along each edge. How many small cubes have paint on exactly one face?"
}


# =================================================================================================================
# geo-119 (camera lesson, in 5 parts) - Solids: Surface and Volume
# Hebrew geo 5996-6224 (her definitions lesson, all of it): don't be afraid of 3D, the questions are simple; edge, face,
# base (the box's walls); a prism = two identical polygons, the bottom one lifted ("hop"); the cylinder (lift a circle,
# any can); the lateral surface = unroll the cylinder (the toilet roll) -> a rectangle h by 2 pi r; the box (2a + 2b)c,
# the cube 4a^2; ONE general rule: the base perimeter x the height; total surface = lateral + the two bases (cube 6a^2,
# box 2(ab + ac + bc) both ways, cylinder 2 pi r h + 2 pi r^2) "understand, don't memorise"; volume = the content (her
# cola can, here a water bottle), a cubic centimetre, stacked rectangles -> base area x height; cube a^3, cylinder
# pi r^2 h, any prism; pointed solids (the cone like a clown's hat, the pyramid): one third of the straight solid "that
# should have been there"; recap. Kept from the English lesson: the prism lying on its side (find the two identical
# faces, the height joins them), 1 ml = 1 cm^3, the height straight down (not the slanted edge), the formula page.
# R37 (every rule on numbers at once): one box 2 x 3 x 4, one cube 5, one cylinder r 3 h 5 carried through lateral,
# total and volume (40, 100, 30 pi; 52, 150, 48 pi; 24, 125, 45 pi), a triangular prism (perimeter 16 x 10), the cone
# 15 pi and the square pyramid 6 x 6 x 5 -> 60 (a third of the box 180). Letters a, b, c are said as length, width,
# height (W18). Study plan: after topics 30-34 (perimeters, areas, the circle 2 pi r and pi r^2 are short reminders).
# Visuals (V3): every solid built at her words on a clean figure - the given solid ink and grey, the part she names
# teal (an edge, a face, a base, the unrolled rectangle), the second part orange, values written as found.
# =================================================================================================================
# ---- edge, face, base: one box
_P1 = boxpts(40, 300, 240, 150, 150)
p119box = G('p119box', [
    ('line', box_el(_P1)),
    ('edge', [sg(_P1['A'], _P1['B'], 'teal', 7), ('txt', 160, 326, 'an edge', 'teal', 24)]),
    ('face', [('tint', [_P1['B'], _P1['C'], _P1['G'], _P1['F']], 'teal'), ('txt', 322, 200, 'a face', 'teal', 22)]),
    ('bases', [('tint', [_P1['A'], _P1['B'], _P1['C'], _P1['D']], 'orange'), ('tint', [_P1['E'], _P1['F'], _P1['G'], _P1['H']], 'orange'),
               ('txt', 200, 122, 'base', 'orange', 24), ('txt', 200, 274, 'base', 'orange', 24)]),
], vb='0 70 400 280', w=480, title='A box: edges, faces, two bases')

# ---- a prism: lift a triangle, lift a rectangle
_t1, _t2, _t3 = pj(40, 300, 0, 0, 0, 0.45, 0.7), pj(40, 300, 190, 0, 0, 0.45, 0.7), pj(40, 300, 70, 0, 170, 0.45, 0.7)
_u1, _u2, _u3 = pj(40, 300, 0, 140, 0, 0.45, 0.7), pj(40, 300, 190, 140, 0, 0.45, 0.7), pj(40, 300, 70, 140, 170, 0.45, 0.7)
_R1 = boxpts(370, 300, 150, 140, 130, 0.45, 0.7)
p119prism = G('p119prism', [
    ('line', [('tint', [_t1, _t2, _t3], 'teal'), sg(_t1, _t2), sg(_t2, _t3), hid(_t1, _t3)]),
    ('lift', [sg((p[0], p[1] - 12), (p[0], p[1] - 128), 'teal', 2.5, True) for p in (_t1, _t2, _t3)]
             + edges_el([(_t1, _u1, True), (_t2, _u2, True), (_t3, _u3, True), (_u1, _u2, True), (_u2, _u3, True), (_u3, _u1, True)])
             + [('tint', [_u1, _u2, _u3], 'teal'), ('txt', 120, 330, 'identical triangles', 'teal', 22)]),
    ('rect', [('tint', [_R1['A'], _R1['B'], _R1['C'], _R1['D']], 'orange'), sg(_R1['A'], _R1['B']), sg(_R1['B'], _R1['C']),
              hid(_R1['C'], _R1['D']), hid(_R1['D'], _R1['A'])]),
    ('box', box_el(_R1, fill=False) + [('tint', [_R1['E'], _R1['F'], _R1['G'], _R1['H']], 'orange'),
                                         ('txt', 470, 330, 'a box is a prism', 'orange', 22)]),
], vb='0 0 640 340', w=600, title='A prism: lift a copy of the base straight up')

# ---- lying down: the bases are the two identical faces
_a, _b, _c = pj(150, 300, 0, 0, 0), pj(150, 300, 180, 0, 0), pj(150, 300, 0, 170, 0)
_d, _e, _f = pj(150, 300, 0, 0, 170), pj(150, 300, 180, 0, 170), pj(150, 300, 0, 170, 170)
p119lie = G('p119lie', [
    ('line', [_praw([_a, _b, _c], FACE_F), _praw([_b, _e, _f, _c], FACE_R)]
             + edges_el([(_a, _b, True), (_b, _c, True), (_c, _a, True), (_b, _e, True), (_c, _f, True), (_e, _f, True),
                         (_a, _d, False), (_d, _e, False), (_d, _f, False)])),
    ('bases', [('tint', [_a, _b, _c], 'teal'), ('poly', [_a, _b, _c], 'teal', 5), ('poly', [_d, _e, _f], 'teal', 4, True),
               ('txt', 196, 268, 'base', 'teal', 22), ('txt', 300, 150, 'base', 'teal', 22)]),
    ('h', [sg(_b, _e, 'orange', 7), ('txt', 400, 300, 'height', 'orange', 24)]),
], vb='100 60 440 270', w=480, title='A prism lying on its side')

# ---- the cylinder: lift a circle
p119cyl = G('p119cyl', [
    ('line', [_ell(200, 290, 110, 32, 'full', fill=GBAND)]),
    ('cyl', cyl_el(200, 290, 110, 190, 32)),
    ('rh', [sg((200, 290), (310, 290), 'teal', 4), ('dot', 200, 290), ('txt', 255, 312, 'r', 'teal', 30, True),
            sg((340, 100), (340, 290), 'orange', 4, True), ('txt', 362, 196, 'h', 'orange', 30, True)]),
], vb='60 60 340 290', w=420, title='A cylinder: two circles, one above the other')

p119r1 = H35('p119r1', 'right prism: two identical bases')
p119r2 = H35('p119r2', 'height: from base to base')

_S119 = [
    S('Solids: Surface and Volume',
      L("Welcome back, and now three-dimensional geometry, solids."),
      L("A lot of students are afraid of this topic. They don't remember it from school, or they never learned it."),
      L("And that's a shame, because the questions here are usually not hard. A simple formula or a simple idea is "
        "enough, and you solve them quite fast."),
      L("It looks much scarier than it really is. So stay with me, and you'll see.")),
    S('Edge, face, base',
      L("First, let's learn some basic words, so we share one language. Here's a box.",
        show(p119box['line'], "Here's a box")),
      L("An edge is a straight line where two flat faces meet. Like this line on our box. We measure its length in "
        "centimeters, like a side of a triangle.", show(p119box['edge'], 'An edge is a straight line')),
      L("A face is a flat wall of the solid, like a wall of a room. Here's the right face. The box also has a left "
        "face, a front face and a back face.", show(p119box['face'], "Here's the right face")),
      L("The bottom face and the top face are called the bases. So a box has six faces, and two of them are the "
        "bases.", show(p119box['bases'], 'are called the bases'))),
    S('Prism',
      L("Here we work with right prisms. Each has two identical polygon bases, one exactly above the other.",
        show(p119r1, 'right prisms')),
      L("Let's take a triangle. That's the bottom base. Now let's lift a copy of it straight up. The copy is the top "
        "base, and we've made a prism.", show(p119prism['line'], "Let's take a triangle"),
        show(p119prism['lift'], 'lift a copy of it straight up')),
      L("The bottom base and the top base are identical triangles. And the side faces are rectangles."),
      L("Now the same with a rectangle. We lift a copy straight up, and we get a box. So a box is a prism too.",
        show(p119prism['rect'], 'the same with a rectangle'), show(p119prism['box'], 'we get a box'))),
    S('Lying down',
      L("Now careful, because sometimes a prism lies on its side. Here's a triangular prism lying down.",
        show(p119lie['line'], "Here's a triangular prism lying down")),
      L("Where are the bases now? Not at the bottom. The bases are the two identical faces, the two triangles, one at "
        "the front and one at the back.", show(p119lie['bases'], 'the two identical faces')),
      L("The height of a prism is the distance between its two bases. Here, the height is this edge, and it lies flat "
        "on the floor.", show(p119r2, 'The height of a prism'), show(p119lie['h'], 'the height is this edge')),
      L("So don't look for a height that goes up. First find the two identical faces. The height is the edge that "
        "joins them.")),
    S('Cylinder',
      L("On the exam we also have the cylinder. Take a circle, and lift a copy of it straight up.",
        show(p119cyl['line'], 'Take a circle'), show(p119cyl['cyl'], 'lift a copy of it straight up')),
      L("Now both bases are circles, one above the other. That's a cylinder, like a can of soda or a roll of paper "
        "towels."),
      L("The radius of the cylinder is the radius of its base, r. Its height is the distance between the two circles, "
        "h.", show(p119cyl['rh'], 'The radius of the cylinder'))),
]

# ---- geo-119 part 2: the lateral area
p119roll = G('p119roll', [
    ('line', cyl_el(110, 290, 70, 180, 22)),
    ('cut', [sg((110, 312), (110, 132), 'teal', 3, True)]),
    ('roll', [('tint', [(250, 110), (600, 110), (600, 290), (250, 290)], 'teal'), ('poly', [(250, 110), (600, 110), (600, 290), (250, 290)], 'teal', 4),
              sg((190, 200), (238, 200), 'teal', 3), ('raw', '<path d="M 240 200 l -12 -7 l 0 14 Z" fill="%s"/>' % GTEAL)]),
    ('h', [('txt', 625, 200, 'h', 'orange', 32, True)]),
    ('w', [('txt', 425, 318, '2πr', 'orange', 32, True)]),
], vb='20 80 640 260', w=600, title='Unroll the side of a cylinder: a rectangle')
p119a1 = H35('p119a1', 'lateral $= 2πr \\cdot h$')
p119a2 = H35('p119a2', '$2π \\cdot 3 = 6π$')
p119a3 = H35('p119a3', '$6π \\cdot 5 = 30π$')

_B2 = boxpts(40, 310, 100, 200, 150)
_C5 = boxpts(310, 310, 150, 150, 150)
p119lat = G('p119lat', [
    ('line', box_el(_B2) + [('txt', 90, 334, '2', 'ink', 26), ('txt', 196, 300, '3', 'ink', 26), ('txt', 22, 210, '4', 'ink', 26)]),
    ('front', [('tint', [_B2['A'], _B2['B'], _B2['F'], _B2['E']], 'teal'), ('txt', 90, 210, '8', 'teal', 32)]),
    ('right', [('tint', [_B2['B'], _B2['C'], _B2['G'], _B2['F']], 'orange'), ('txt', 181, 183, '12', 'orange', 30)]),
    ('cube', box_el(_C5) + [('txt', 385, 334, '5', 'ink', 26)]),
    ('cside', [('tint', [_C5['A'], _C5['B'], _C5['F'], _C5['E']], 'teal'), ('txt', 385, 235, '25', 'teal', 32)]),
], vb='0 40 560 310', w=560, title='The side faces of a box and of a cube')
p119b1 = H35('p119b1', '$2 \\cdot 4 = 8$')
p119b2 = H35('p119b2', '$3 \\cdot 4 = 12$')
p119b3 = H35('p119b3', '$8 + 8 + 12 + 12 = 40$')
p119b4 = H35('p119b4', '$5 \\cdot 5 = 25$')
p119b5 = H35('p119b5', '$4 \\cdot 25 = 100$')

p119rule = G('p119rule', [
    ('line', box_el(_B2) + [('txt', 90, 334, '2', 'ink', 26), ('txt', 196, 300, '3', 'ink', 26), ('txt', 22, 210, '4', 'ink', 26)]),
    ('per', [sg(_B2['A'], _B2['B'], 'teal', 6), sg(_B2['B'], _B2['C'], 'teal', 6), sg(_B2['C'], _B2['D'], 'teal', 4, True),
             sg(_B2['D'], _B2['A'], 'teal', 4, True), ('txt', 265, 330, 'perimeter 10', 'teal', 24)]),
    ('h', [sg(_B2['B'], _B2['F'], 'orange', 6), ('txt', 270, 150, 'height 4', 'orange', 24)]),
], vb='0 40 380 310', w=440, title='The perimeter of the base and the height')
p119c1 = I('p119c1', 'lateral $=$ perimeter $\\times$ height', size=32, col=1)
p119c2 = H35('p119c2', '$2 + 3 + 2 + 3 = 10$')
p119c3 = H35('p119c3', '$10 \\cdot 4 = 40$')
p119c4 = H35('p119c4', '$4 \\cdot 5 = 20$')
p119c5 = H35('p119c5', '$20 \\cdot 5 = 100$')

_u = 36
_q1, _q2, _q3 = pj(60, 300, 0, 0, 0), pj(60, 300, 6 * _u, 0, 0), pj(60, 300, 3 * _u, 4 * _u, 0)
_w1, _w2, _w3 = pj(60, 300, 0, 0, 200), pj(60, 300, 6 * _u, 0, 200), pj(60, 300, 3 * _u, 4 * _u, 200)
p119tri = G('p119tri', [
    ('line', [_praw([_q1, _q2, _q3], FACE_F), _praw([_q2, _w2, _w3, _q3], FACE_R)]
             + edges_el([(_q1, _q2, True), (_q2, _q3, True), (_q3, _q1, True), (_q2, _w2, True), (_q3, _w3, True), (_w2, _w3, True),
                         (_q1, _w1, False), (_w1, _w2, False), (_w1, _w3, False)])
             + [('txt', 168, 326, '6', 'ink', 26), ('txt', 100, 230, '5', 'ink', 26), ('txt', 236, 230, '5', 'ink', 26)]),
    ('per', [('poly', [_q1, _q2, _q3], 'teal', 6), ('tint', [_q1, _q2, _q3], 'teal')]),
    ('h', [sg(_q2, _w2, 'orange', 6), ('txt', 330, 300, '10', 'orange', 28)]),
], vb='30 40 400 310', w=440, title='A triangular prism: base sides 5, 5 and 6, height 10')
p119d1 = H35('p119d1', '$5 + 5 + 6 = 16$')
p119d2 = H35('p119d2', '$16 \\cdot 10 = 160$')

_S119 += [
    S('Lateral area: unroll it',
      L("Now let's talk about areas. The lateral surface is everything that wraps around the solid, without the two "
        "bases."),
      L("Think of a roll of toilet paper. Tear off one full turn, and stretch it out flat. What do we get? A "
        "rectangle.", show(p119roll['line'], 'Think of a roll'), show(p119roll['cut'], 'Tear off one full turn'),
        show(p119roll['roll'], 'A rectangle')),
      L("The height of this rectangle is the height of the cylinder, h.", show(p119roll['h'], 'the height of the cylinder')),
      L("And its width? This side went once around the circle. So it's the circumference of the base, two pi r.",
        show(p119roll['w'], 'two pi r')),
      L("So the lateral area of a cylinder is the area of this rectangle, two pi r, times h.",
        show(p119a1, 'the lateral area of a cylinder')),
      L("Let's see it in numbers. A cylinder with radius three and height five. Two pi times three is six pi. And six "
        "pi times five is thirty pi.", show(p119a2, 'Two pi times three'), show(p119a3, 'six pi times five'))),
    S('Box and cube',
      L("Now a box. Its base is two by three, and its height is four. What wraps around it? The four side faces, "
        "without the top and the bottom.", show(p119lat['line'], 'Now a box')),
      L("The front face is two times four, eight. The back face is the same, eight.",
        show(p119lat['front'], 'The front face'), show(p119b1, 'two times four')),
      L("The right face is three times four, twelve. And the left face is twelve too.",
        show(p119lat['right'], 'The right face'), show(p119b2, 'three times four')),
      L("So the lateral area is eight plus eight, plus twelve plus twelve. That's forty.",
        show(p119b3, 'eight plus eight')),
      L("A cube is a box whose edges are all equal. Let's take a cube with edge five. Each side face is a square, five "
        "times five, twenty-five.", show(p119lat['cube'], 'a cube with edge five'), show(p119lat['cside'], 'Each side face is a square'),
        show(p119b4, 'five times five')),
      L("There are four side faces, so the lateral area is four times twenty-five, one hundred.",
        show(p119b5, 'four times twenty-five'))),
    S('Perimeter times height',
      L("So do we need a different formula for every shape? No. There's one rule for every right prism, and for the "
        "cylinder too."),
      L("The lateral area is the perimeter of the base, times the height.", show(p119c1, 'The lateral area is the perimeter')),
      L("Why? Unroll the side faces, like the toilet paper. We get one long rectangle. Its width is the whole way "
        "around the base, the perimeter. And its height is the height of the solid."),
      L("Let's check it on our box. The base is two by three. Its perimeter is two plus three plus two plus three, "
        "ten.", show(p119rule['line'], "Let's check it on our box"), show(p119rule['per'], 'Its perimeter is'),
        show(p119c2, 'two plus three plus two')),
      L("Ten times the height, four, is forty. That's the same forty we got face by face.",
        show(p119rule['h'], 'Ten times the height'), show(p119c3, 'four, is forty')),
      L("And the cube with edge five. The perimeter of its base is four times five, twenty. Twenty times the height, "
        "five, is one hundred. Again, the same.", show(p119c4, 'four times five, twenty'), show(p119c5, 'Twenty times the height'))),
    S('Any right prism',
      L("And it works for any right prism. Here's a triangular prism lying on its side. Its base is the triangle at the "
        "front, with sides five, five and six. Its height is the edge going back, ten.", show(p119tri['line'], "Here's a triangular prism")),
      L("The perimeter of the base is five plus five plus six, sixteen.", show(p119tri['per'], 'The perimeter of the base'),
        show(p119d1, 'five plus five plus six')),
      L("Sixteen times the height, ten, is one hundred sixty. So the lateral area is one hundred sixty.",
        show(p119tri['h'], 'Sixteen times the height'), show(p119d2, 'one hundred sixty. So')),
      L("Remember this one rule, perimeter times height. Then you can find the lateral area of any right prism they give "
        "you.")),
]

# ---- geo-119 parts 3-5: total surface area, volume, pointed solids
p119tot = G('p119tot', [
    ('line', box_el(_C5) + [('txt', 385, 334, '5', 'ink', 26)]),
    ('side', [('tint', [_C5['A'], _C5['B'], _C5['F'], _C5['E']], 'teal'), ('tint', [_C5['B'], _C5['C'], _C5['G'], _C5['F']], 'teal'),
              ('txt', 385, 245, '4 faces: 100', 'teal', 22)]),
    ('bases', [('tint', [_C5['E'], _C5['F'], _C5['G'], _C5['H']], 'orange'), ('poly', [_C5['A'], _C5['B'], _C5['C'], _C5['D']], 'orange', 4, True),
               ('txt', 590, 120, 'top 25', 'orange', 22), ('txt', 590, 300, 'bottom 25', 'orange', 22)]),
], vb='280 40 380 310', w=440, title='A cube: four side faces and two bases')
p119e1 = H35('p119e1', '$100 + 25 + 25 = 150$')
p119e2 = H35('p119e2', '$6 \\cdot 25 = 150$')

p119bc = G('p119bc', [
    ('line', box_el(_B2) + [('txt', 90, 334, '2', 'ink', 26), ('txt', 196, 300, '3', 'ink', 26), ('txt', 22, 210, '4', 'ink', 26)]),
    ('bases', [('tint', [_B2['E'], _B2['F'], _B2['G'], _B2['H']], 'orange'), ('poly', [_B2['A'], _B2['B'], _B2['C'], _B2['D']], 'orange', 4, True),
               ('txt', 131, 70, '6', 'orange', 26)]),
    ('cyl', cyl_el(420, 300, 90, 150, 26) + [sg((420, 300), (510, 300), 'ink', 2.5), ('txt', 465, 322, '3', 'ink', 26),
                                             ('txt', 534, 225, '5', 'ink', 26)]),
    ('cb', [_ell(420, 150, 90, 26, 'full', GORANGE, 4, False, 'none'), _ell(420, 300, 90, 26, 'front', GORANGE, 4),
            _ell(420, 300, 90, 26, 'back', GORANGE, 3, True)]),
], vb='0 40 560 310', w=560, title='The box and the cylinder: add the two bases')
p119f1 = H35('p119f1', '$2 \\cdot 3 = 6$')
p119f2 = H35('p119f2', '$40 + 6 + 6 = 52$')
p119f3 = H35('p119f3', '$2 \\cdot (8 + 12 + 6) = 52$')
p119f4 = H35('p119f4', '$π \\cdot 3^2 = 9π$')
p119f5 = H35('p119f5', '$30π + 9π + 9π = 48π$')

_U1 = boxpts(120, 260, 130, 130, 130)
p119cm = G('p119cm', [
    ('line', box_el(_U1) + [('txt', 185, 284, '1 cm', 'ink', 24), ('txt', 285, 252, '1 cm', 'ink', 24), ('txt', 82, 195, '1 cm', 'ink', 24)]),
], vb='40 60 340 240', w=380, title='One cubic centimeter: a cube 1 cm by 1 cm by 1 cm')
p119g1 = H35('p119g1', '$1$ ml $= 1$ cm$^3$')
p119g2 = H35('p119g2', '$500$ ml $= 500$ cm$^3$')

_slab = lambda k: boxpts(40, 310 - 50 * k, 100, 50, 150)
p119stack = G('p119stack', [
    ('line', [('tint', [_B2['A'], _B2['B'], _B2['C'], _B2['D']], 'teal'), ('poly', [_B2['A'], _B2['B'], _B2['C'], _B2['D']], 'ink', 3),
              ('txt', 90, 334, '2', 'ink', 26), ('txt', 196, 300, '3', 'ink', 26)]),
    ('stack', [x for k in range(4) for x in box_el(_slab(k), fill=False, w=2)] +
              [('seg', 245, 260, 245, 310, 'teal', 2),
               ('seg', 240, 260, 250, 260, 'teal', 2),
               ('seg', 240, 310, 250, 310, 'teal', 2),
               ('txt', 273, 285, '1 cm', 'teal', 20)]),
    ('box', box_el(_B2, w=3) + [('txt', 22, 210, '4', 'orange', 28)]),
], vb='0 40 300 310', w=360, title='One-centimeter layers stacked into a box')
p119h1 = I('p119h1', 'volume $=$ base area $\\times$ height', size=32, col=1)
p119h2 = H35('p119h2', '$2 \\cdot 3 = 6$')
p119h3 = H35('p119h3', '$6 \\cdot 4 = 24$')
p119h4 = H35('p119h4', '$5 \\cdot 5 \\cdot 5 = 125$')
p119h5 = H35('p119h5', '$9π \\cdot 5 = 45π$')
p119h6 = H35('p119h6', '$12 \\cdot 10 = 120$')

p119cone = G('p119cone', [
    ('line', cone_el(200, 300, 100, 200, 30) + [sg((200, 300), (300, 300), 'ink', 2.5), ('txt', 250, 322, '3', 'ink', 26),
                                                sg((200, 100), (200, 300), 'ink', 2, True), ('txt', 214, 210, '5', 'ink', 26)]),
    ('cyl', [sg((100, 100), (100, 300), 'teal', 3, True), sg((300, 100), (300, 300), 'teal', 3, True),
             _ell(200, 100, 100, 30, 'full', GTEAL, 3, True, 'none')]),
], vb='60 50 290 290', w=380, title='A cone inside the cylinder with the same base and height')
p119k1 = H35('p119k1', 'cone $= \\frac{1}{3}$ cylinder')
p119k2 = H35('p119k2', '$45π \\div 3 = 15π$')

_PB = boxpts(60, 310, 200, 180, 200)
_apx = ((_PB['A'][0] + _PB['C'][0]) / 2.0, (_PB['A'][1] + _PB['C'][1]) / 2.0 - 180)
_ctr = ((_PB['A'][0] + _PB['C'][0]) / 2.0, (_PB['A'][1] + _PB['C'][1]) / 2.0)
p119pyr = G('p119pyr', [
    ('line', pyr_el(_PB, _apx) + [('txt', 160, 334, '6', 'ink', 26), ('txt', 340, 296, '6', 'ink', 26)]),
    ('h', [sg(_apx, _ctr, 'teal', 4, True), rt(_ctr, _apx, _PB['B'], 12, 'teal'), ('txt', _ctr[0] + 16, _ctr[1] - 70, '5', 'teal', 28)]),
    ('box', [sg(p, q, 'teal', 2.5, True) for p, q in [(_PB['E'], _PB['F']), (_PB['F'], _PB['G']), (_PB['G'], _PB['H']), (_PB['H'], _PB['E']),
                                                      (_PB['A'], _PB['E']), (_PB['B'], _PB['F']), (_PB['C'], _PB['G']), (_PB['D'], _PB['H'])]]),
    ('edge', [sg(_apx, _PB['B'], 'red', 6), ('txt', 360, 150, 'not the height', 'red', 24)]),
], vb='30 80 420 270', w=440, title='A square pyramid, its height, and the box around it')
p119m1 = I('p119m1', 'pyramid $= \\dfrac{\\text{base area} \\times \\text{height}}{3}$', size=30, col=1)
p119m2 = H35('p119m2', '$6 \\cdot 6 = 36$')
p119m3 = H35('p119m3', '$36 \\cdot 5 = 180$')
p119m4 = H35('p119m4', '$180 \\div 3 = 60$')

p119n1 = I('p119n1', 'On the formula page:', size=32, col=0)
p119n2 = I('p119n2', 'box and cube: volume, surface area', size=30, col=0)
p119n3 = I('p119n3', 'cylinder: lateral area, total area, volume', size=30, col=0)
p119n4 = I('p119n4', 'cone and pyramid: volume', size=30, col=0)
p119n5 = I('p119n5', 'Not on it: the general rules, units, the next lessons', size=30, col=0)

p119z1 = I('p119z1', 'Prism, cylinder: lateral area $=$ base perimeter $\\times$ height', size=30, col=0)
p119z2 = I('p119z2', 'Prism, cylinder: total area $=$ lateral area $+$ 2 bases', size=30, col=0)
p119z3 = I('p119z3', 'Prism, cylinder: volume $=$ base area $\\times$ height', size=30, col=0)
p119z4 = I('p119z4', 'Cone, pyramid: volume $=$ base area $\\times$ height $\\div 3$', size=30, col=0)

_S119 += [
    S('Total surface area',
      L("Now the total surface area. It's the area of the solid from every direction. So it's the lateral area, plus "
        "the two bases."),
      L("Let's go back to the cube with edge five. Around it, we had four faces, one hundred.",
        show(p119tot['line'], 'the cube with edge five'), show(p119tot['side'], 'we had four faces')),
      L("Now we add the bottom and the top, twenty-five each. One hundred plus twenty-five plus twenty-five is one "
        "hundred fifty.", show(p119tot['bases'], 'we add the bottom and the top'), show(p119e1, 'One hundred plus twenty-five')),
      L("And that makes sense. A cube has six equal faces, and six times twenty-five is one hundred fifty.",
        show(p119e2, 'six times twenty-five'))),
    S('Box and cylinder',
      L("Now our box, two by three by four. Its lateral area was forty. Each base is two times three, six.",
        show(p119bc['line'], 'Now our box'), show(p119bc['bases'], 'Each base is two times three'), show(p119f1, 'two times three, six')),
      L("So the total surface area is forty, plus six, plus six. That's fifty-two.", show(p119f2, 'forty, plus six, plus six')),
      L("We can also count it face by face. Every face has a twin on the other side. Front and back are eight each. "
        "Right and left are twelve each. Bottom and top are six each."),
      L("So we add one of each, eight plus twelve plus six, twenty-six. Then we double it. Two times twenty-six "
        "is fifty-two again.", show(p119f3, 'eight plus twelve plus six, twenty-six')),
      L("Now the cylinder, with radius three and height five. Its lateral area was thirty pi. One base is a circle, pi "
        "times three squared, nine pi.", show(p119bc['cyl'], 'Now the cylinder'), show(p119bc['cb'], 'One base is a circle'),
        show(p119f4, 'pi times three squared')),
      L("So the total is thirty pi, plus nine pi, plus nine pi, forty-eight pi.", show(p119f5, 'So the total is thirty pi')),
      L("So for a prism or a cylinder, the total surface area is the lateral area plus the two bases. If you understand that, "
        "you don't need to memorize a formula for each shape.")),
    S('Volume',
      L("Now volume. The volume is what's inside the solid, how much it can hold."),
      L("Think of a bottle of water. The label says five hundred milliliters. That's the volume of the water."),
      L("A cubic centimeter is a tiny cube, one centimeter by one centimeter by one centimeter.",
        show(p119cm['line'], 'A cubic centimeter is a tiny cube')),
      L("And one milliliter is exactly one cubic centimeter. So the bottle holds five hundred cubic centimeters.",
        show(p119g1, 'one milliliter is exactly'), show(p119g2, 'So the bottle holds'))),
    S('Base area times height',
      L("Now look at a rectangle, two by three. It has an area, but no volume. It's flat.",
        show(p119stack['line'], 'look at a rectangle')),
      L("Now imagine a layer above that rectangle, one centimeter thick. Stack four of these layers. Together they "
        "make a box, four centimeters high.", show(p119stack['stack'], 'Stack four of these layers'),
        show(p119stack['box'], 'Together they make a box')),
      L("So the volume of the box is the area of its base, times its height. Multiplying the base area by one centimeter "
        "gives one layer's volume. Four layers give four times that volume.", show(p119h1, 'So the volume of the box')),
      L("Our box is two by three, with height four. The base area is two times three, six. And six times four is "
        "twenty-four. So for a box, it's length times width times height.",
        show(p119h2, 'two times three, six'), show(p119h3, 'six times four')),
      L("A cube with edge five is five times five times five, one hundred twenty-five. That's five to the power of "
        "three.", show(p119h4, 'five times five times five')),
      L("The cylinder works the same way. Its base is a circle, pi r squared, and we multiply it by the height. With "
        "radius three and height five, the base is nine pi, and nine pi times five is forty-five pi.",
        show(p119h5, 'nine pi times five')),
      L("And the same for any prism. If the base of a triangular prism has area twelve and its height is ten, its "
        "volume is twelve times ten, one hundred twenty.", show(p119h6, 'twelve times ten'))),
    S('Pointed: the cone',
      L("On the exam we also have pointed solids. They're not prisms."),
      L("A cone has a circle at the bottom, and at the top only a point, like a party hat.",
        show(p119cone['line'], 'A cone has a circle')),
      L("Put a cylinder around it, with the same base and the same height. The cone's volume is one third of that "
        "cylinder.", show(p119cone['cyl'], 'Put a cylinder around it'), show(p119k1, "The cone's volume is one third")),
      L("Our cylinder had radius three and height five, and its volume was forty-five pi. So a cone with the same base "
        "and height is forty-five pi divided by three, fifteen pi.", show(p119k2, 'forty-five pi divided by three'))),
    S('Pointed: the pyramid',
      L("A pyramid has a polygon at the bottom, a triangle, a square, a hexagon, it doesn't matter. And at the top, "
        "one point.", show(p119pyr['line'], 'A pyramid has a polygon')),
      L("Its volume is the base area, times the height, divided by three.", show(p119m1, 'Its volume is the base area')),
      L("Let's take a pyramid with a square base, six by six, and height five. The base area is six times six, "
        "thirty-six.", show(p119pyr['h'], 'and height five'), show(p119m2, 'six times six')),
      L("Thirty-six times five is one hundred eighty. Divided by three, that's sixty.",
        show(p119m3, 'Thirty-six times five'), show(p119m4, 'Divided by three')),
      L("And one hundred eighty is the box around the pyramid, six by six by five. So the pyramid is one third of that "
        "box.", show(p119pyr['box'], 'the box around the pyramid')),
      L("So a pointed solid is always one third of the straight solid with the same base and the same height."),
      L("One more thing. The height goes from the top point straight to the base, at a right angle. In this picture, "
        "it reaches the middle of the base. It is not this "
        "slanted edge, which is longer.", show(p119pyr['edge'], 'It is not this slanted edge'))),
    S('On the formula page',
      L("Good news. At the start of every quantitative section, there's a formula page.", show(p119n1, 'there\'s a formula page')),
      L("It has the volume and the surface area of a box and of a cube. It has the cylinder's lateral area, total "
        "area and volume. And it has the volume of a cone and of a pyramid.",
        show(p119n2, 'It has the volume'), show(p119n3, "the cylinder's lateral area"), show(p119n4, 'the volume of a cone')),
      L("It doesn't have the general rules we learned for any prism. And it doesn't have the ideas of the next "
        "lessons. Those you need to know yourself.", show(p119n5, "It doesn't have the general rules"))),
    S('Recap',
      L("So let's sum up. For a prism or cylinder, the lateral area is everything that wraps around, without the bases. "
        "It's the perimeter of the base, times the height.", show(p119z1, 'the lateral area is everything')),
      L("For these prisms and cylinders, the total surface area is the lateral area plus the two bases.", show(p119z2, 'the total surface area')),
      L("Their volume is the base area, times the height.", show(p119z3, 'Their volume is')),
      L("And a pointed solid, a cone or any pyramid, has volume equal to its base area, times its height, divided by three.",
        show(p119z4, 'And a pointed solid')),
      L("Take a moment to memorize these, and I'll see you in the next video.")),
]
video('geo-119', 'lesson', slides=_S119)
CAMERA_SPLIT = ('geo-119', 'Solids: Surface and Volume', [
    (1, None),
    (5, "Let's continue with the areas of solids."),
    (11, "Let's continue with volume."),
])


# =================================================================================================================
# geo-120 (lesson, 3 parts; was a 0.5-minute overview) - Solids in Questions: the three core ideas
# Hebrew geo 6226-6230 (her intro: "the basic rules last time; now higher-level questions and the nuances that come back")
# and the principles she names in her questions: volume ratios (g122 "this principle helps in harder questions", g127
# ratio units "a tool that really helps"), inner triangles (g128 "one of the principles that keeps coming back in 3D:
# triangles inside the solid, or ones we build"; the height is perpendicular to every line on the base; g130 the cube's
# diagonal x root 3, the box's two right triangles), and surfaces of cube solids (g125: count the faces by direction and
# double by symmetry; apart = the most faces, every contact loses two; g132 lost + gained). R37: these are the topic's
# core methods (several questions each + the real exam: 2020 autumn q2_08 radius vs height, 2021 spring q2_12, 2025
# winter q1_19 cones and cylinders; 2022 autumn q1_20, 2020 autumn q1_07, 2025 autumn q2_14 inner right triangles;
# 2019 winter q2_20 stacked cubes, 2019 spring q1_14 and 2023 autumn q2_19 cut solids), so they are taught here with 2-3
# worked examples each, starting easy; the questions apply them ("like in the lesson").
# External finding (Codex final 2.1): a flat cut exposes TWO new faces (the increase = twice the cut area), contrasted
# with joining. Numbers differ from the Hebrew and from the questions (cylinder 90, cone r 5 / slant 13, pyramid 8 / 9,
# cube 4 and 5, box 2 x 3 x 6, a staircase of 6 cubes, a 4 x 3 x 2 box cut in two).
# Visuals (V3): each idea on a clean solid; the triangle inside is tinted in the solid and then pulled out next to it as
# its own flat triangle (same colours, same labels); cube faces tinted by direction; the cut faces teal.
# =================================================================================================================
# ---- part 1: volume ratios
_cy0 = 130
p120ratio = G('p120ratio', [
    ('line', cyl_el(_cy0, 300, 90, 200, 26)),
    ('cone', cone_el(_cy0, 300, 90, 200, 26)[1:] + [('tint', [(_cy0, 100), (_cy0 - 90, 300), (_cy0 + 90, 300)], 'teal')]),
    ('units', [('txt', 380, 140, 'cone: 1 unit', 'teal', 26), ('txt', 380, 190, 'cylinder: 3 units', 'ink', 26),
               ('txt', 380, 240, 'left: 2 units', 'orange', 26)]),
], vb='20 60 520 290', w=520, title='A cone inside a cylinder with the same base and height')
p120a1 = H35('p120a1', 'cylinder: $15 \\cdot 6 = 90$')
p120a2 = H35('p120a2', 'cone: $90 \\div 3 = 30$')
p120a3 = H35('p120a3', 'left: $90 - 30 = 60$')
p120a4 = H35('p120a4', '$2$ units $= 40$')
p120a5 = H35('p120a5', '$1$ unit $= 20$')

_hb = lambda x, h: cyl_el(x, 300, 50, h, 15)
p120h = G('p120h', [
    ('line', _hb(80, 60) + [('txt', 80, 335, '3', 'ink', 26)]),
    ('two', _hb(220, 120) + [('txt', 220, 335, '6', 'ink', 26)]),
    ('three', _hb(360, 180) + [('txt', 360, 335, '9', 'ink', 26)]),
], vb='10 80 420 270', w=440, title='The same base, the height times 2 and times 3')
p120b1 = H35('p120b1', '$10 \\cdot 3 = 30$')
p120b2 = H35('p120b2', '$10 \\cdot 6 = 60$')
p120b3 = H35('p120b3', '$10 \\cdot 9 = 90$')
p120b4 = H35('p120b4', 'cylinder: $10 \\cdot 4 = 40$')
p120b5 = H35('p120b5', 'cone: $\\frac{10 \\cdot 12}{3} = 40$')
p120b6 = H35('p120b6', '$r = 1$: base $π$')
p120b7 = H35('p120b7', '$r = 2$: base $4π$')

# ---- part 2: right triangles inside solids
_fl = [(40, 300), (360, 300), (460, 230), (140, 230)]
_ft = (250, 265)
p120pole = G('p120pole', [
    ('line', [_praw(_fl, FACE_T), ('poly', _fl, 'ink', 3)]),
    ('pole', [sg(_ft, (250, 90), 'orange', 6), ('dot', *_ft)]),
    ('lines', [sg(_ft, (110, 290), 'teal', 4), sg(_ft, (400, 280), 'teal', 4), sg(_ft, (330, 238), 'teal', 4),
               rt(_ft, (250, 90), (110, 290), 14, 'teal'), rt(_ft, (250, 90), (400, 280), 14, 'teal'),
               rt(_ft, (250, 90), (330, 238), 14, 'teal')]),
], vb='20 70 460 250', w=460, title='A pole on the floor: a right angle with every line from its foot')

p120cone = G('p120cone', [
    ('line', cone_el(150, 290, 100, 210, 28) + [('txt', 200, 316, '5', 'ink', 26), ('txt', 222, 170, '13', 'ink', 26)]),
    ('tri', [('tint', [(150, 80), (150, 290), (250, 290)], 'teal'), ('poly', [(150, 80), (150, 290), (250, 290)], 'teal', 4),
             rt((150, 290), (150, 80), (250, 290), 14, 'teal')]),
    ('cut', [('tint', [(380, 80), (380, 290), (480, 290)], 'teal'), ('poly', [(380, 80), (380, 290), (480, 290)], 'teal', 4),
             rt((380, 290), (380, 80), (480, 290), 14, 'teal'), ('txt', 430, 316, '5', 'teal', 28), ('txt', 452, 170, '13', 'teal', 28),
             ('txt', 360, 185, 'h', 'orange', 30, True)]),
    ('h', [('txt', 352, 220, '12', 'orange', 28)]),
], vb='30 60 480 280', w=520, title='A cone: the radius, the height and the slant height')
p120c1 = H35('p120c1', '$h^2 + 5^2 = 13^2$')
p120c2 = H35('p120c2', '$h^2 = 169 - 25 = 144$')
p120c3 = H35('p120c3', '$h = 12$')

_PP = boxpts(40, 300, 220, 0, 220)
_PO = ((_PP['A'][0] + _PP['C'][0]) / 2.0, (_PP['A'][1] + _PP['C'][1]) / 2.0)
_PA = (_PO[0], _PO[1] - 200)
p120pyr = G('p120pyr', [
    ('line', pyr_el(_PP, _PA) + [('txt', 150, 324, '8', 'ink', 26), ('txt', 312, 190, '9', 'ink', 26)]),
    ('diag', [sg(_PP['A'], _PP['C'], 'teal', 3, True), sg(_PP['B'], _PP['D'], 'teal', 3, True), ('dot', *_PO)]),
    ('tri', [('tint', [_PA, _PO, _PP['B']], 'orange'), ('poly', [_PA, _PO, _PP['B']], 'orange', 4), rt(_PO, _PA, _PP['B'], 12, 'orange')]),
    ('cut', [('tint', [(460, 60), (460, 280), (560, 280)], 'orange'), ('poly', [(460, 60), (460, 280), (560, 280)], 'orange', 4),
             rt((460, 280), (460, 60), (560, 280), 14, 'orange'), ('txt', 510, 306, '4√2', 'orange', 26),
             ('txt', 532, 160, '9', 'orange', 28), ('txt', 440, 175, 'h', 'orange', 30, True)]),
], vb='20 40 580 300', w=580, title='A square pyramid: the height, half the diagonal and the edge')
p120d1 = H35('p120d1', 'diagonal: $8\\sqrt2$, half: $4\\sqrt2$')
p120d2 = H35('p120d2', '$(4\\sqrt2)^2 = 16 \\cdot 2 = 32$')
p120d3 = H35('p120d3', '$h^2 = 81 - 32 = 49$')
p120d4 = H35('p120d4', '$h = 7$')

_CU = boxpts(40, 300, 170, 170, 170)
p120cube = G('p120cube', [
    ('line', box_el(_CU) + [('txt', 125, 324, '4', 'ink', 26)]),
    ('face', [sg(_CU['A'], _CU['C'], 'teal', 4, True), ('txt', 200, 268, '4√2', 'teal', 24)]),
    ('tri', [('tint', [_CU['A'], _CU['C'], _CU['G']], 'orange'), sg(_CU['A'], _CU['G'], 'orange', 4), sg(_CU['C'], _CU['G'], 'orange', 5),
             rt(_CU['C'], _CU['A'], _CU['G'], 12, 'orange')]),
    ('cut', [('tint', [(420, 280), (590, 280), (590, 80)], 'orange'), ('poly', [(420, 280), (590, 280), (590, 80)], 'orange', 4),
             rt((590, 280), (420, 280), (590, 80), 14, 'orange'), ('txt', 505, 306, '4√2', 'teal', 26), ('txt', 612, 180, '4', 'orange', 28)]),
    ('ans', [('txt', 480, 160, '4√3', 'orange', 30)]),
], vb='20 40 630 300', w=600, title='A cube: the face diagonal and the body diagonal')
p120e1 = H35('p120e1', 'face: $4\\sqrt2$')
p120e2 = H35('p120e2', '$4^2 + (4\\sqrt2)^2 = 16 + 32 = 48$')
p120e3 = H35('p120e3', 'body: $\\sqrt{48} = 4\\sqrt3$')
p120e4 = I('p120e4', 'face diagonal $=$ edge $\\cdot \\sqrt2$', size=30, col=1)
p120e4b = I('p120e4b', 'body diagonal $=$ edge $\\cdot \\sqrt3$', size=30, col=1)
p120e5 = H35('p120e5', 'edge $5$: $5\\sqrt2$, $5\\sqrt3$')

_BX = boxpts(40, 300, 110, 220, 160)
p120box = G('p120box', [
    ('line', box_el(_BX) + [('txt', 95, 324, '2', 'ink', 26), ('txt', 200, 290, '3', 'ink', 26), ('txt', 22, 190, '6', 'ink', 26)]),
    ('base', [sg(_BX['A'], _BX['C'], 'teal', 4, True), ('tint', [_BX['A'], _BX['B'], _BX['C']], 'teal')]),
    ('body', [('tint', [_BX['A'], _BX['C'], _BX['G']], 'orange'), sg(_BX['A'], _BX['G'], 'orange', 5), rt(_BX['C'], _BX['A'], _BX['G'], 12, 'orange')]),
], vb='0 30 300 310', w=360, title='A box 2 by 3 by 6: two right triangles')
p120f1 = H35('p120f1', '$2^2 + 3^2 = 4 + 9 = 13$')
p120f2 = H35('p120f2', '$13 + 6^2 = 13 + 36 = 49$')
p120f3 = H35('p120f3', '$\\sqrt{49} = 7$')
p120f4 = H35('p120f4', '$\\sqrt{2^2 + 3^2 + 6^2} = \\sqrt{49} = 7$')

# ---- part 3: solids made of cubes
_ST = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 1, 0), (0, 2, 0)]
_sx, _sy, _ss = 80, 300, 70
_tops = [(2, 0, 0), (1, 1, 0), (0, 2, 0)]
p120st = G('p120st', [
    ('line', unit_cubes(_ST, _sx, _sy, _ss)),
    ('front', [('tint', cube_face(i, j, k, 'front', _sx, _sy, _ss), 'teal') for (i, j, k) in _ST] + [('txt', 170, 330, 'front 6', 'teal', 24)]),
    ('top', [('tint', cube_face(i, j, k, 'top', _sx, _sy, _ss), 'orange') for (i, j, k) in _tops] + [('txt', 330, 120, 'top 3', 'orange', 24)]),
    ('right', [('tint', cube_face(i, j, k, 'right', _sx, _sy, _ss), 'ink') for (i, j, k) in _tops] + [('txt', 390, 250, 'right 3', 'ink', 24)]),
], vb='40 50 420 300', w=440, title='A staircase of 6 cubes: count the faces by direction')
p120g1 = H35('p120g1', 'front $6$, back $6$')
p120g2 = H35('p120g2', 'top $3$, bottom $3$')
p120g3 = H35('p120g3', 'right $3$, left $3$')
p120g4 = H35('p120g4', '$2 \\cdot (6 + 3 + 3) = 24$')

_s2 = 64
p120touch = G('p120touch', [
    ('line', unit_cubes([(0, 0, 0)], 40, 150, _s2) + unit_cubes([(0, 0, 0)], 170, 150, _s2) + [('txt', 140, 190, '6 + 6 = 12', 'ink', 24)]),
    ('join', unit_cubes([(0, 0, 0), (1, 0, 0)], 340, 150, _s2) + [sg((404, 150), (404, 86), 'red', 6), ('txt', 404, 190, '12 − 2 = 10', 'red', 24)]),
    ('row', unit_cubes([(0, 0, 0), (1, 0, 0), (2, 0, 0)], 160, 310, _s2) + [sg((224, 310), (224, 246), 'red', 6), sg((288, 310), (288, 246), 'red', 6),
                                                                              ('txt', 260, 345, '18 − 4 = 14', 'red', 24)]),
], vb='20 40 540 320', w=520, title='Two faces hide at every contact')
p120h1 = H35('p120h1', '$6 \\cdot 2 = 12$')
p120h2 = H35('p120h2', '$12 - 2 = 10$')
p120h3 = H35('p120h3', '$6 \\cdot 3 = 18$, $\\ 18 - 4 = 14$')
p120h4 = H35('p120h4', 'staircase: $36 - 12 = 24$')

_K = boxpts(40, 300, 240, 120, 160)
_Km1, _Km2, _Km3, _Km4 = pj(40, 300, 120, 0, 0), pj(40, 300, 120, 120, 0), pj(40, 300, 120, 120, 160), pj(40, 300, 120, 0, 160)
_KL = boxpts(330, 300, 120, 120, 160); _KR = boxpts(480, 300, 120, 120, 160)
p120cut = G('p120cut', [
    ('line', box_el(_K) + [('txt', 160, 324, '4', 'ink', 26), ('txt', 318, 270, '3', 'ink', 26), ('txt', 22, 240, '2', 'ink', 26)]),
    ('cut', [('poly', [_Km1, _Km2, _Km3, _Km4], 'red', 4, True)]),
    ('apart', box_el(_KL) + box_el(_KR) + [('tint', [_KL['B'], _KL['C'], _KL['G'], _KL['F']], 'teal'),
                                           ('tint', [_KR['A'], _KR['D'], _KR['H'], _KR['E']], 'teal'),
                                           ('poly', [_KR['A'], _KR['D'], _KR['H'], _KR['E']], 'teal', 4, True),
                                           ('txt', 470, 330, 'two new faces', 'teal', 24)]),
], vb='0 60 700 290', w=520, title='One cut makes two new faces')
p120k1 = H35('p120k1', '$2 \\cdot (12 + 8 + 6) = 52$')
p120k2 = H35('p120k2', 'piece: $2 \\cdot (6 + 4 + 6) = 32$')
p120k3 = H35('p120k3', '$32 + 32 = 64$')
p120k4 = H35('p120k4', '$64 - 52 = 12 = 2 \\cdot 6$')

video('geo-120', 'lesson', slides=[
    S('Solids in Questions',
      L("In the last lesson we learned the basic rules of solids. Now let's learn the ideas that come back again and "
        "again in the exam questions."),
      L("There are three of them. Volume ratios, right triangles inside solids, and solids made of cubes. Let's start "
        "with volume ratios.")),
    S('Same base, same height',
      L("Here's a cylinder. Its base area is fifteen, and its height is six. So its volume is fifteen times six, "
        "ninety.", show(p120ratio['line'], "Here's a cylinder"), show(p120a1, 'fifteen times six')),
      L("Now let's put a cone inside it, with the same base and the same height. Like in the last lesson, the cone is "
        "one third of the cylinder. Ninety divided by three is thirty.",
        show(p120ratio['cone'], "let's put a cone inside it"), show(p120a2, 'Ninety divided by three')),
      L("If we carve the cone out of the cylinder, what's left? Ninety minus thirty, sixty. That's two thirds of the "
        "cylinder.", show(p120a3, 'Ninety minus thirty')),
      L("So we can think in ratio units, like in word problems. The cone is one unit. The whole cylinder is three "
        "units. And what's left is two units.", show(p120ratio['units'], 'think in ratio units')),
      L("Now let's turn it around. A cone is carved out of a cylinder with the same base and height, and what's left "
        "is forty. How much was the cone?"),
      L("What's left is two units, so two units are forty. One unit is forty divided by two, twenty. So the cone is "
        "twenty, and the whole cylinder is sixty.", show(p120a4, 'two units are forty'), show(p120a5, 'One unit is forty divided by two'))),
    S('Only the height changes',
      L("Now let's keep the base the same, and change only the height. Here's a cylinder with base area ten, and "
        "two more like it.", show(p120h['line'], "Here's a cylinder with base area ten")),
      L("With height three, the volume is ten times three, thirty. With height six, it's sixty. With height nine, it's "
        "ninety.", show(p120b1, 'ten times three'), show(p120h['two'], 'With height six'), show(p120b2, "it's sixty"),
        show(p120h['three'], 'With height nine'), show(p120b3, "it's ninety")),
      L("So when the base stays the same, the volume grows exactly like the height. Twice the height, twice the volume. "
        "Three times the height, three times the volume."),
      L("Now a cone and a cylinder with the same base. The cylinder has base area ten and height four, so its volume is "
        "forty.", show(p120b4, 'so its volume is forty')),
      L("A cone with the same base and height four is only one third of that. How tall must the cone be to hold forty "
        "too? Three times as tall, twelve. Ten times twelve, divided by three, is forty.",
        show(p120b5, 'Ten times twelve, divided by three')),
      L("Careful, this works for the height, not for the radius. The radius is squared in the base. A radius of one "
        "gives a base of pi. A radius of two gives four pi, four times bigger, not two.",
        show(p120b6, 'A radius of one'), show(p120b7, 'A radius of two'))),
    S('A right angle at the foot',
      L("The second idea is right triangles inside solids. Many 3D questions are solved with Pythagoras, once we find "
        "the right triangle."),
      L("Why are there right triangles? The height stands straight on the base, like a pole on a flat floor.",
        show(p120pole['line'], 'The height stands straight'), show(p120pole['pole'], 'like a pole on a flat floor')),
      L("So the height makes a right angle with every line on the floor that starts at its foot. Not only with one of "
        "them, with all of them.", show(p120pole['lines'], 'with every line on the floor')),
      L("Let's see it in a cone. The radius is five, and the slant height, the line along the outside, is thirteen. "
        "What's the height?", show(p120cone['line'], "Let's see it in a cone")),
      L("The height, the radius and the slant height make a triangle. The radius lies on the base, so the angle "
        "between the height and the radius is a right angle.", show(p120cone['tri'], 'make a triangle')),
      L("Let's pull this triangle out. The slant height, thirteen, is the hypotenuse. The radius, five, is a leg.",
        show(p120cone['cut'], "Let's pull this triangle out")),
      L("So h squared plus five squared is thirteen squared. One hundred sixty-nine minus twenty-five is one hundred "
        "forty-four, so h is twelve. That's the triple five, twelve, thirteen.",
        show(p120c1, 'So h squared plus five squared'), show(p120c2, 'One hundred sixty-nine minus twenty-five'),
        show(p120c3, 'so h is twelve'), show(p120cone['h'], 'so h is twelve'))),
    S('In a pyramid',
      L("Now a pyramid with a square base. The side of the base is eight, and each slanted edge is nine. What's the "
        "height?", show(p120pyr['line'], 'Now a pyramid with a square base')),
      L("All four slanted edges are equal. So the top point is directly above the center of the square. "
        "The height meets the base there, where the diagonals meet.", show(p120pyr['diag'], 'where the diagonals meet')),
      L("So we have a triangle. The height, half of a diagonal, and a slanted edge. The angle at the middle is a right "
        "angle, because half the diagonal lies on the base.", show(p120pyr['tri'], 'So we have a triangle')),
      L("Remember the silver triangle. The diagonal of a square is the side times root two. So the diagonal is eight "
        "root two, and half of it is four root two.", show(p120d1, 'the diagonal is eight root two')),
      L("Now let's pull the triangle out. The edge, nine, is the hypotenuse. The square of four root two is sixteen "
        "times two, thirty-two.", show(p120pyr['cut'], "let's pull the triangle out"), show(p120d2, 'sixteen times two')),
      L("So h squared is eighty-one minus thirty-two, forty-nine. And h is seven.",
        show(p120d3, 'eighty-one minus thirty-two'), show(p120d4, 'And h is seven'))),
    S('In a cube',
      L("Now a cube with edge four. A diagonal on a face is like the diagonal of a square, the edge times root two. So "
        "it's four root two.", show(p120cube['line'], 'Now a cube with edge four'), show(p120cube['face'], 'A diagonal on a face'),
        show(p120e1, "So it's four root two")),
      L("Now the diagonal through the inside of the cube, the body diagonal. Look at this triangle. The vertical edge "
        "stands on the bottom face, so it makes a right angle with the face diagonal.",
        show(p120cube['tri'], 'Look at this triangle')),
      L("Let's pull it out. The legs are four and four root two. Four squared is sixteen, and the square of four root "
        "two is thirty-two. Together, forty-eight.", show(p120cube['cut'], "Let's pull it out"), show(p120e2, 'Four squared is sixteen')),
      L("Root forty-eight is root sixteen times root three, four root three. So the body diagonal is four root three.",
        show(p120e3, 'Root forty-eight is'), show(p120cube['ans'], 'So the body diagonal is')),
      L("This is true in every cube. The face diagonal is the edge times root two. The body diagonal is the edge times "
        "root three. Why root three? Edge squared, plus two edges squared, makes three edges squared.",
        show(p120e4, 'The face diagonal is the edge times'), show(p120e4b, 'The body diagonal is the edge times')),
      L("So a cube with edge five has a face diagonal of five root two, and a body diagonal of five root three.",
        show(p120e5, 'a cube with edge five'))),
    S('In a box',
      L("In a box, the edges are not equal, so there's no fixed ratio. We use the same two right triangles. Here's a "
        "box, two by three, with height six.", show(p120box['line'], "Here's a box")),
      L("First the diagonal of the base. Its square is two squared plus three squared, four plus nine, thirteen. We "
        "don't even need its root.", show(p120box['base'], 'First the diagonal of the base'), show(p120f1, 'four plus nine')),
      L("Then the second triangle, with the height. Thirteen plus six squared is thirteen plus thirty-six, forty-nine. "
        "So the body diagonal is root forty-nine, seven.", show(p120box['body'], 'Then the second triangle'),
        show(p120f2, 'Thirteen plus six squared'), show(p120f3, 'root forty-nine, seven')),
      L("Or in one step: square each edge length, then add the three squares. Take the square root of that sum. Two squared plus three squared plus six squared "
        "is forty-nine, and its root is seven.", show(p120f4, 'Or in one step'))),
    S('Count by direction',
      L("The third idea is solids made of cubes. The surface area is all the faces we can touch from the outside. Here "
        "are six cubes with edge one, in a staircase.", show(p120st['line'], 'in a staircase')),
      L("This shape is not a box, so there's no formula for it. We count the faces, one direction at a time. From the "
        "front, there are six faces. And the back is the same, six.", show(p120st['front'], 'From the front'), show(p120g1, 'the back is the same')),
      L("From above, there are three faces, one on each step. Below, three as well.", show(p120st['top'], 'From above'),
        show(p120g2, 'Below, three as well')),
      L("From the right, three faces, and from the left, three.", show(p120st['right'], 'From the right'), show(p120g3, 'from the left, three')),
      L("So we add six plus three plus three, twelve, and we double it. Two times twelve is twenty-four.", show(p120g4, 'Two times twelve')),
      L("Why can we double? Because what we see from one side, we also see from the opposite side.")),
    S('A contact hides two faces',
      L("Here are two cubes apart. Each has six faces, so together they have twelve.",
        show(p120touch['line'], 'Here are two cubes apart'), show(p120h1, 'together they have twelve')),
      L("Now let's push them together. The two faces that touch are hidden now, one from each cube. So twelve minus "
        "two, ten.", show(p120touch['join'], "let's push them together"), show(p120h2, 'So twelve minus two')),
      L("Three cubes in a row have two contacts. So it's eighteen faces minus four faces, fourteen.",
        show(p120touch['row'], 'Three cubes in a row'), show(p120h3, 'minus four')),
      L("Let's check our staircase. Six cubes have thirty-six faces. The cubes touch in six places, so twelve faces "
        "hide. Thirty-six minus twelve is twenty-four, as we counted.", show(p120h4, 'Thirty-six minus twelve')),
      L("So the more the cubes touch, the smaller the surface area. The tightest shape has the smallest surface.")),
    S('A cut adds two faces',
      L("Now the opposite of joining, a cut. Here's a box, four by three, with height two. Its faces are twelve, "
        "eight and six. Twelve plus eight plus six is twenty-six, and twice that is fifty-two.", show(p120cut['line'], "Here's a box"), show(p120k1, 'twice that is fifty-two')),
      L("Let's cut it in the middle, straight down. We get two boxes, each two by three by two.",
        show(p120cut['cut'], "Let's cut it in the middle")),
      L("Each piece has faces of six, four and six. Six plus four plus six is sixteen, and twice that is thirty-two. The two pieces together have "
        "sixty-four.", show(p120cut['apart'], 'Each piece has faces'), show(p120k2, 'twice that is thirty-two'), show(p120k3, 'sixty-four')),
      L("Sixty-four minus fifty-two is twelve. Where did twelve come from? The cut made two new faces, one on each "
        "piece, and each one is three times two, six.", show(p120k4, 'Sixty-four minus fifty-two')),
      L("So a cut adds two new faces, and the volume doesn't change. Joining two pieces does the opposite. Two faces "
        "touch, and they hide."),
      L("So again, three ideas. Volume ratios, right triangles inside solids, and counting faces. Take a moment to "
        "memorize them, and I'll see you in the next video.")),
])
MORE_SPLITS = [('geo-120', 'Solids in Questions', [
    (1, None),
    (3, "Let's continue with right triangles inside solids."),
    (7, "Let's continue with solids made of cubes."),
])]


# =================================================================================================================
# Question videos (topic 35). Layout (as topic 34, batch C NOFIG): on every slide our enlarged colour copy of the
# question's figure sits on the left (LEFT; its base layer is the question's own black-and-white figure) and the working
# is written in readable hand rows on the right (FLOW), each at its own clause.
# =================================================================================================================
def QY(vid, y):
    return y


def NOFIG(vid, *slides):
    NOFIG35.update((vid, k) for k in slides)


COLS = [(920, 660, 240, 860)]
LONGCH = {'geo35-g121', 'geo35-g132'}      # choices written as sentences: one column of four rows, from about y 715


def QTOP(qid):
    """where the work area starts: below the question's lines (measured on the frames: about 72 px a line)"""
    import math
    n = math.ceil(len(re.sub(r'\$[^$]*\$', 'xxxx', QSTEM[qid])) / 80.0)
    return 40 + 72 * n


def QBOT(qid):
    return {'geo35-g132': 520}.get(qid, 590 if qid in LONGCH else 700)


def QLEFT(g, qid, w=460):
    """the colour copy on the left, as big as fits between the question and the choices (at most w wide)"""
    base = g['line'] if 'line' in g else g
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', base['v']['svg']).group(1).split()]
    top, bot = QTOP(qid), QBOT(qid)
    w = int(min(w, (bot - top - 10) * vb[2] / vb[3]))
    return LEFT(g, y=top, x=410, w=w)


def QC(qid):
    """two columns of hand-written rows on the right of the copy"""
    top, bot = QTOP(qid) + 5, QBOT(qid)
    return [(900, 690, top, bot)]


def QW(qid):
    """one wide column, on a slide without a figure"""
    return [(430, 1150, QTOP(qid) + 5, QBOT(qid))]


# =================================================================================================================
# solve-geo35-g121 - which container holds the cone's water?
# Hebrew geo 6232-6321 (cone r root 5, h 6 there -> 10 pi; r root 6, h 12 here -> 24 pi): the volume of the cone = how
# much water; a container that is bigger or equal holds it -> mark; smaller -> out; a cone is pointed, one third of the
# straight solid (the cylinder around it); the cube = edge cubed ("a cube is a square in 3D"); the box = multiply the
# dimensions; the square pyramid = base x height / 3; "straight or pointed - the two most important principles of volume".
# 2026-10-23 (Nitzan's decision: pi as 3.14, like her Hebrew and like solve-geo33-g089): 3.14 < pi < 3.15, each end
# worked in easy mental steps (24 x 3 = 72; 24 x 14 = 240 + 96 = 336 -> 3.36; a tenth of 24 = 2.4, half of it 1.2 -> 3.6)
# -> 75.36 < water < 75.6, so 75 < water < 76, which decides every choice (64 and 72 below, 84 above, 20 pi < 24 pi). Was
# 3 < pi < 3 and a half (72 and 84). The right choice is choice 2, so "in the exam you'd circle it and move on, here
# let's check the others" (R24); the pi = 3 trap (the box is exactly 72) at its step. R37: geo-119 taught the formulas.
# V3: the cone copy, its base tinted, the height teal, 24 pi written; the pyramid with 6, 6, 7; the box and the cylinder.
# =================================================================================================================
f121a = PIN(GEO('f121a', [
    ('line', [qraw('geo35-g121')]),
    ('base', [_ell(320, 299.455, 48.786, 13.66, 'full', GTEAL, 4, False, GBAND)]),
    ('h', [sg((320, 299.455), (320, 60.455), 'orange', 5)]),
    ('v', [('txt', 430, 180, '24π', 'teal', 34)]),
], vb='200 40 300 300', w=420, title='The cone of water'))
_PQ = boxpts(60, 300, 200, 0, 200)
_PQo = ((_PQ['A'][0] + _PQ['C'][0]) / 2.0, (_PQ['A'][1] + _PQ['C'][1]) / 2.0)
f121b = PIN(GEO('f121b', [
    ('line', pyr_el(_PQ, (_PQo[0], _PQo[1] - 210)) + [('txt', 160, 326, '6', 'ink', 28), ('txt', 330, 290, '6', 'ink', 28)]),
    ('h', [sg((_PQo[0], _PQo[1] - 210), _PQo, 'teal', 4, True), ('txt', _PQo[0] + 18, _PQo[1] - 100, '7', 'teal', 30)]),
    ('v', [('txt', 200, 40, '84', 'teal', 34)]),
], vb='30 20 380 320', w=420, title='Choice 2: a square pyramid'))
_BQ = boxpts(40, 300, 180, 120, 110)
f121c = PIN(GEO('f121c', [
    ('line', box_el(_BQ) + [('txt', 130, 326, '6', 'ink', 28), ('txt', 262, 292, '4', 'ink', 28), ('txt', 20, 240, '3', 'ink', 28)]),
    ('v', [('txt', 150, 130, '72', 'red', 34)]),
    ('cyl', cyl_el(440, 300, 70, 170, 20) + [sg((440, 300), (510, 300), 'ink', 2.5), ('txt', 475, 326, '√2', 'ink', 26),
                                             ('txt', 530, 215, '10', 'ink', 26)]),
    ('cv', [('txt', 440, 100, '20π', 'red', 34)]),
], vb='0 60 560 290', w=520, title='Choices 3 and 4: a box and a cylinder'))
for _g in (f121a, f121b, f121c): QLEFT(_g, 'geo35-g121')
f121r1 = IH('f121r1', '$(\\sqrt6)^2 = 6$, base $6π$', size=30)
f121r2 = IH('f121r2', '$12 \\div 3 = 4$', size=30)
f121r3 = IH('f121r3', '$6π \\cdot 4 = 24π$', size=30)
f121r4 = IH('f121r4', '$3.14 < π < 3.15$', size=30)
f121r5 = IH('f121r5', '$24 \\cdot 3 = 72$', size=30)
f121r6 = IH('f121r6', '$24 \\cdot 14 = 240 + 96 = 336$', size=30)
f121r7 = IH('f121r7', '$24 \\cdot 0.14 = 3.36$', size=30)
f121u1 = IH('f121u1', '$24 \\cdot 3.14 = 72 + 3.36 = 75.36$', size=30)
f121u2 = IH('f121u2', '$24 \\cdot 0.15 = 2.4 + 1.2 = 3.6$', size=30)
f121u3 = IH('f121u3', '$24 \\cdot 3.15 = 72 + 3.6 = 75.6$', size=30)
f121u4 = IH('f121u4', '$75 <$ water $< 76$', size=30)
f121s1 = IH('f121s1', '(1) $4 \\cdot 4 \\cdot 4 = 64 < 75$', size=30)
f121s2 = IH('f121s2', '(2) $6 \\cdot 6 = 36$', size=30)
f121s3 = IH('f121s3', '$36 \\div 3 = 12$', size=30)
f121s4 = IH('f121s4', '$12 \\cdot 7 = 84 >$ water', size=30)
f121t1 = IH('f121t1', '(3) $6 \\cdot 4 \\cdot 3 = 72$', size=30)
f121t2 = IH('f121t2', '$π > 3.14$, so water $> 75 > 72$', size=30)
f121t3 = IH('f121t3', '(4) $(\\sqrt2)^2 = 2$, base $2π$', size=30)
f121t4 = IH('f121t4', '$2π \\cdot 10 = 20π < 24π$', size=30)
FLOW([f121r1, f121r2, f121r3], QC('geo35-g121'))
FLOW([f121r4, f121r5, f121r6, f121r7], QC('geo35-g121'))
FLOW([f121u1, f121u2, f121u3, f121u4], QC('geo35-g121'))
FLOW([f121s1, f121s2, f121s3, f121s4], QC('geo35-g121'))
FLOW([f121t1, f121t2, f121t3, f121t4], QC('geo35-g121'))
NOFIG('solve-geo35-g121', 0, 1, 2, 3, 4)
f121a2 = PIN(GEO('f121a2', [('line', [qraw('geo35-g121'), ('txt', 430, 180, '24π', 'teal', 34)])], vb='200 40 300 300', w=420, title='The cone of water'))
QLEFT(f121a2, 'geo35-g121')
f121a3 = PIN(GEO('f121a3', [('line', [qraw('geo35-g121'), ('txt', 430, 180, '24π', 'teal', 34)])], vb='200 40 300 300', w=420, title='The cone of water'))
QLEFT(f121a3, 'geo35-g121')

video('solve-geo35-g121', 'solution', qid='geo35-g121', slides=[
    SM('Method 1 · The math way', 'How much water?',
      L("A cone-shaped container with base radius root six and height twelve is full of water. Which of the following "
        "empty containers can hold all the water?", pt('stem', 'A cone-shaped container', 'hl', 8.0),
        show(f121a['line'], 'A cone-shaped container'), voice='calm', pause=0.5),
      L("So first we need to know how much water there is. That's the volume of the cone. Then we look for a container "
        "whose volume is the same, or bigger."),
      L("Let's start with the math way. A cone is a pointed solid. So, like in the first lesson, its volume is the base "
        "area, times the height, divided by three."),
      L("The base is a circle, so its area is pi r squared. The square of root six is six, so the base area is six pi.",
        show(f121a['base'], 'The base is a circle'), show(f121r1, 'The square of root six')),
      L("Now times the height, twelve, and divided by three. Twelve divided by three is four. And six pi times four is "
        "twenty-four pi. So there's twenty-four pi of water.", show(f121a['h'], 'times the height, twelve'),
        show(f121r2, 'Twelve divided by three'), show(f121r3, 'six pi times four'), show(f121a['v'], "So there's twenty-four pi"))),
    SM('Method 1 · The math way', 'How much is 24 pi?',
      L("How much is twenty-four pi? We don't need pi exactly. Pi is more than three point one four, and less than "
        "three point one five.", show(f121a2['line'], 'How much is twenty-four pi'),
        show(f121r4, 'Pi is more than three point one four')),
      L("First the lower end, twenty-four times three point one four. We take the three first. Twenty-four times three "
        "is seventy-two.", show(f121r5, 'Twenty-four times three is')),
      L("Now twenty-four times point one four. That's fourteen hundredths, so first we calculate twenty-four times "
        "fourteen. Twenty-four times ten is two hundred forty. Twenty-four times four is ninety-six. Together, three "
        "hundred thirty-six.", show(f121r6, 'Together, three hundred thirty-six')),
      L("Make that hundredths, and we get three point three six.", show(f121r7, 'Make that hundredths'))),
    SM('Method 1 · The math way', 'Between which numbers?',
      L("Now we add the two parts. Seventy-two plus three point three six is seventy-five point three six. So the water "
        "is more than seventy-five point three six.", show(f121a3['line'], 'Now we add the two parts'),
        show(f121u1, 'Seventy-two plus three point three six')),
      L("Now the upper end, twenty-four times three point one five. The three gives seventy-two again. Point one five is "
        "a tenth, plus half a tenth. A tenth of twenty-four is two point four, and half of that is one point two. "
        "Together that's three point six.", show(f121u2, "Together that's three point six")),
      L("Seventy-two plus three point six is seventy-five point six. So the water is less than seventy-five point six.",
        show(f121u3, 'Seventy-two plus three point six')),
      L("So the water is between seventy-five point three six and seventy-five point six. That's more than seventy-five, "
        "and less than seventy-six.", show(f121u4, "That's more than seventy-five"))),
    SM('Method 1 · The math way', 'Go through the choices',
      L("Now the choices. If a container's volume is the same as the water, or bigger, all the water fits. If it's "
        "smaller, it's out. And for each container we ask first, is it straight or pointed?"),
      L("Choice number one says, a cube with edge four. A cube is a straight solid, edge times edge times edge. Four "
        "times four times four is sixty-four.", show(f121s1, 'Four times four times four')),
      L("Sixty-four is less than seventy-five, so it's less than the water. Choice number one is out.",
        mk('cross', 'choice 1', 'Choice number one is out')),
      L("Choice number two says, a square pyramid with base edge six and height seven. A pyramid is pointed. So it's "
        "the base area, times the height, divided by three.", show(f121b['line'], 'a square pyramid'),
        show(f121b['h'], 'height seven')),
      L("The base is a square, six times six, thirty-six. Thirty-six divided by three is twelve. And twelve times seven "
        "is eighty-four.", show(f121s2, 'six times six'), show(f121s3, 'Thirty-six divided by three'),
        show(f121s4, 'twelve times seven'), show(f121b['v'], 'is eighty-four')),
      L("So the pyramid holds eighty-four, and the water is less than seventy-six. All the water fits. In the exam you'd "
        "circle it and move on. Here, let's check the others too.", pt('choice 2', 'So the pyramid holds eighty-four'))),
    SM('Method 1 · The math way', 'The other two',
      L("Choice number three says, a box measuring six by four by three. A box is straight, so we multiply its three "
        "edges. Six times four is twenty-four, and twenty-four times three is seventy-two.",
        show(f121c['line'], 'a box measuring six by four by three'), show(f121t1, 'Six times four is twenty-four'),
        show(f121c['v'], 'twenty-four times three is seventy-two')),
      L("Careful here. If you take pi as just three, the water is exactly seventy-two, and this box looks big enough. "
        "But pi is more than three point one four, so the water is more than seventy-five. This box is too small. "
        "Choice number three is out.",
        show(f121t2, 'But pi is more than three point one four'), mk('cross', 'choice 3', 'Choice number three is out')),
      L("Choice number four says, a cylinder with base radius root two and height ten. The square of root two is two, so "
        "the base is two pi. Times ten, that's twenty pi.", show(f121c['cyl'], 'a cylinder with base radius root two'),
        show(f121t3, 'The square of root two'), show(f121t4, 'Times ten'), show(f121c['cv'], "that's twenty pi")),
      L("Twenty pi is less than twenty-four pi, so choice number four is out too.",
        mk('cross', 'choice 4', 'so choice number four is out')),
      L("So again, straight or pointed? Straight, the base area times the height. Pointed, the same, divided by "
        "three. Only the pyramid holds all the water. Choice number two is our answer, and I'll see you in the next "
        "question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# r26-t35-water (lesson) - Water in containers
# No Hebrew lesson (added in the 2026-09 review; her g131 "liquid spreads evenly, no empty space left" is the seed). Kept
# from the English lesson: 1 ml = 1 cm^3, a liter = 1000 cm^3 (10 x 10 x 10), a cubic meter = 1,000,000 cm^3, 2 liters
# into a 20 x 10 base -> 10 cm. R37 (core: q-r26-t35-01, practice p12, p13, q-r26-t35-10, -13; real exam 2022 winter
# q1_14 cups, 2024 autumn q1_04 volumes): the height = volume / base area with its why (volume = base area x height, turned
# around) on two examples, pouring (the volume stays, the height changes; 600 cm^3 from a 10 x 10 base into a 20 x 15
# base -> 2 cm), and sinking a solid (the rise = its volume / the base area; a cube 64 in a 16 x 8 tank -> half a cm),
# which the practice set uses (p13 cube dropped in a tank, the stone).
# Visuals: boxes with the water tinted teal, its height orange, written at her words.
# =================================================================================================================
_W1 = boxpts(40, 300, 260, 150, 170)
p_w1 = G('p_w1', [
    ('line', box_el(_W1) + [('txt', 170, 326, '20', 'ink', 28), ('txt', 360, 290, '10', 'ink', 28)]),
    ('water', water_el(_W1, 0.45)),
    ('h', [sg(_W1['A'], (40, 300 - 150 * 0.45), 'orange', 6), ('txt', 14, 268, '?', 'orange', 30)]),
], vb='0 50 420 300', w=480, title='2 liters of water in a box with base 20 by 10')
p_wa1 = H35('p_wa1', '$1$ ml $= 1$ cm$^3$')
p_wa2 = H35('p_wa2', '$1$ liter $= 10 \\cdot 10 \\cdot 10 = 1000$ cm$^3$')
p_wa3 = H35('p_wa3', '$1$ m$^3 = 100 \\cdot 100 \\cdot 100 = 1000000$ cm$^3$')
p_wb1 = I('p_wb1', 'height $=$ volume $\\div$ base area', size=32, col=1)
p_wb2 = H35('p_wb2', '$2$ liters $= 2000$ cm$^3$')
p_wb3 = H35('p_wb3', 'base: $20 \\cdot 10 = 200$')
p_wb4 = H35('p_wb4', '$2000 \\div 200 = 10$ cm')

_W2 = boxpts(40, 300, 130, 180, 130); _W3 = boxpts(270, 300, 230, 120, 190)
p_w2 = G('p_w2', [
    ('line', box_el(_W2) + water_el(_W2, 0.6) + [('txt', 105, 326, '10', 'ink', 26), ('txt', 205, 296, '10', 'ink', 26),
                                                ('txt', 20, 250, '6', 'orange', 28)]),
    ('new', box_el(_W3) + [('txt', 385, 326, '20', 'ink', 26), ('txt', 560, 290, '15', 'ink', 26)]),
    ('water', water_el(_W3, 0.18) + [('txt', 250, 290, '?', 'orange', 28)]),
], vb='0 40 620 310', w=600, title='Pouring water into a wider box')
p_wc1 = H35('p_wc1', '$10 \\cdot 10 \\cdot 6 = 600$')
p_wc2 = H35('p_wc2', 'base: $20 \\cdot 15 = 300$')
p_wc3 = H35('p_wc3', '$600 \\div 300 = 2$ cm')

_W4 = boxpts(40, 300, 300, 150, 150)
_cb = boxpts(150, 300, 70, 70, 70)
p_w4 = G('p_w4', [
    ('line', box_el(_W4) + water_el(_W4, 0.7) + [('txt', 190, 326, '16', 'ink', 26), ('txt', 400, 290, '8', 'ink', 26)]),
    ('cube', box_el(_cb) + [('txt', 185, 250, '4', 'ink', 24)]),
    ('rise', [('tint', [pj(40, 300, 0, 105, 0), pj(40, 300, 300, 105, 0), pj(40, 300, 300, 125, 0), pj(40, 300, 0, 125, 0)], 'orange'),
              ('txt', 380, 170, 'rise', 'orange', 26)]),
], vb='0 50 460 300', w=480, title='A cube sinks in a tank: the water rises')
p_wd1 = H35('p_wd1', 'cube: $4 \\cdot 4 \\cdot 4 = 64$')
p_wd2 = H35('p_wd2', 'base: $16 \\cdot 8 = 128$')
p_wd3 = H35('p_wd3', 'rise: $64 \\div 128 = \\frac{1}{2}$ cm')

video('r26-t35-water', 'lesson', slides=[
    S('Water Level',
      L("Now let's look at water in containers. These questions use the volume formula, turned around."),
      L("There are three things to know. The units, the height of the water, and what happens when we pour or drop "
        "something in.")),
    S('Liters and cubic centimeters',
      L("Often the water is in liters, and the container is in centimeters. So first, the units."),
      L("Remember, one milliliter is one cubic centimeter.", show(p_wa1, 'one milliliter is one cubic centimeter')),
      L("A liter is a thousand milliliters, so it's a thousand cubic centimeters. That's a cube, ten by ten by ten.",
        show(p_wa2, "it's a thousand cubic centimeters")),
      L("And a cubic meter is a hundred centimeters in each direction. A hundred times a hundred times a hundred is a "
        "million cubic centimeters.", show(p_wa3, 'A hundred times a hundred'))),
    S('The height of the water',
      L("Water takes the shape of its container, and its top is flat. So the water in a box is a box itself.",
        show(p_w1['line'], 'Water takes the shape'), show(p_w1['water'], 'the water in a box is a box itself')),
      L("Its volume is the base area times its height. So its height is the volume divided by the base area. It's the "
        "same formula, turned around.", show(p_w1['h'], 'So its height is the volume'), show(p_wb1, 'divided by the base area')),
      L("Let's pour two liters into a box whose base is twenty by ten. How high is the water?"),
      L("First, the same units. Two liters are two thousand cubic centimeters.", show(p_wb2, 'Two liters are')),
      L("The base area is twenty times ten, two hundred.", show(p_wb3, 'twenty times ten')),
      L("So the height is two thousand divided by two hundred, ten centimeters.", show(p_wb4, 'two thousand divided by two hundred'))),
    S('Pouring',
      L("Now we pour water from one container into another. Here's a box, ten by ten, with water six centimeters high.",
        show(p_w2['line'], "Here's a box, ten by ten")),
      L("So the water is ten times ten times six, six hundred cubic centimeters.", show(p_wc1, 'ten times ten times six')),
      L("We pour all of it into a box whose base is twenty by fifteen. The volume of the water doesn't change. It's the "
        "same six hundred. Only the height changes.", show(p_w2['new'], 'a box whose base is twenty by fifteen')),
      L("The new base area is twenty times fifteen, three hundred. So the new height is six hundred divided by three "
        "hundred, two centimeters.", show(p_wc2, 'twenty times fifteen'), show(p_wc3, 'six hundred divided by three hundred'),
        show(p_w2['water'], 'two centimeters')),
      L("Does it make sense? The new base is bigger, so the water spreads out, and it's lower. Six went down to two. "
        "The trap is to keep the same height. The height doesn't carry over, the volume does.")),
    S('Dropping in a solid',
      L("And one more case. Here's a tank whose base is sixteen by eight, with some water in it.",
        show(p_w4['line'], "Here's a tank whose base")),
      L("We drop in a cube with edge four. It goes all the way under, and no water spills out. What happens to the water?",
        show(p_w4['cube'], 'We drop in a cube')),
      L("The cube pushes the water up. The water rises by a layer whose volume is exactly the volume of the cube.",
        show(p_w4['rise'], 'The water rises by a layer')),
      L("The cube is four times four times four, sixty-four. The base of the tank is sixteen times eight, one hundred "
        "twenty-eight.", show(p_wd1, 'four times four times four'), show(p_wd2, 'sixteen times eight')),
      L("So the water rises by sixty-four divided by one hundred twenty-eight. That's one half of a centimeter.",
        show(p_wd3, 'So the water rises by')),
      L("So again, same units first. The height of the water is its volume divided by the base area. When we pour, "
        "the volume stays the same. And I'll see you in the next video.")),
])


# =================================================================================================================
# solve-q-r26-t35-01 - water poured from a box into a cube
# No Hebrew source (added question). R37: the lesson r26-t35-water just taught height = volume / base area and "the volume
# stays"; here the first use, slowly, with the link. Two ways: the math way (720, 144, 5), and understanding (the base is
# 144 / 80 = 9 / 5 times bigger, so the height is 9 / 5 times smaller: 9 x 5 / 9 = 5), which stands on its own. The trap
# 9 (the height carried over) at its step.
# =================================================================================================================
f01a = PIN(GEO('f01a', [
    ('line', [qraw('q-r26-t35-01')]),
    ('w', [('raw', '<polygon points="60,300 210,300 210,180 60,180" fill="%s" opacity="0.3"/>' % GTEAL), ('txt', 135, 240, '720', 'teal', 34)]),
    ('base', [('tint', [(350, 300), (540, 300), (628, 245), (438, 245)], 'orange'), ('txt', 470, 275, '144', 'orange', 30)]),
    ('new', [('tint', [(350, 300), (540, 300), (540, 250), (350, 250)], 'teal'), ('txt', 330, 275, '5', 'teal', 32)]),
], vb='20 40 620 300', w=560, title='The water and the cube'))
QLEFT(f01a, 'q-r26-t35-01')
f01r1 = IH('f01r1', '$10 \\cdot 8 = 80$', size=30)
f01r2 = IH('f01r2', '$80 \\cdot 9 = 720$', size=30)
f01r3 = IH('f01r3', 'base: $12 \\cdot 12 = 144$', size=30)
f01r4 = IH('f01r4', '$720 \\div 144 = 5$', size=30)
f01r5 = IH('f01r5', '$144 \\cdot 5 = 720$', size=30)
f01s1 = IH('f01s1', '$\\frac{144}{80} = \\frac{9}{5}$', size=30)
f01s2 = IH('f01s2', '$9 \\cdot \\frac{5}{9} = 5$', size=30)
FLOW([f01r1, f01r2, f01r3, f01r4, f01r5], QC('q-r26-t35-01'))
FLOW([f01s1, f01s2], QC('q-r26-t35-01'))
NOFIG('solve-q-r26-t35-01', 0, 1)
f01b = PIN(GEO('f01b', [
    ('line', [qraw('q-r26-t35-01')]),
    ('bases', [('tint', [(60, 300), (210, 300), (282, 255), (132, 255)], 'teal'), ('txt', 135, 345, 'base 80', 'teal', 26),
               ('tint', [(350, 300), (540, 300), (628, 245), (438, 245)], 'orange'), ('txt', 470, 345, 'base 144', 'orange', 26)]),
], vb='20 40 620 320', w=560, title='The two bases'))
QLEFT(f01b, 'q-r26-t35-01')

video('solve-q-r26-t35-01', 'solution', qid='q-r26-t35-01', slides=[
    SM('Method 1 · The math way', 'The volume stays',
      L("Water in a box-shaped container with a base of ten by eight reaches a height of nine. All the water is poured "
        "into an empty cube with an edge of twelve. How high is the water in the cube?",
        pt('stem', 'Water in a box-shaped container', 'hl', 9.0), show(f01a['line'], 'Water in a box-shaped container'),
        voice='calm', pause=0.5),
      L("Like in the lesson, when we pour, the volume of the water stays the same. Only its height changes. We'll solve "
        "it in two different ways."),
      L("Let's start with the math way. First, how much water is there? The water in the box is a box itself, ten by "
        "eight by nine.", show(f01a['w'], 'The water in the box is a box itself')),
      L("Ten times eight is eighty, and eighty times nine is seven hundred twenty. So there are seven hundred twenty "
        "cubic centimeters of water.", show(f01r1, 'Ten times eight is eighty'), show(f01r2, 'eighty times nine')),
      L("Now the cube. Its base is twelve by twelve, one hundred forty-four.", show(f01a['base'], 'Now the cube'),
        show(f01r3, 'twelve by twelve')),
      L("The height of the water is its volume divided by the base area. So it's seven hundred twenty divided by one "
        "hundred forty-four.", show(f01r4, 'seven hundred twenty divided by')),
      L("Let's check with five. One hundred forty-four times five is seven hundred twenty, because a hundred times five "
        "is five hundred, and forty-four times five is two hundred twenty. So the height is five.",
        show(f01r5, 'One hundred forty-four times five'), show(f01a['new'], 'So the height is five')),
      L("Careful, nine is choice number one. That's the old height, and the height doesn't carry over. Only the volume "
        "does. Choice number three is our answer.", mk('cross', 'choice 1', 'nine is choice number one'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Understanding', 'Bigger base, lower water',
      L("Now by understanding, without the volume. The same water spreads over a new base. Its old base was ten times "
        "eight, eighty. The new base is twelve times twelve, one hundred forty-four.",
        show(f01b['line'], 'Now by understanding'), show(f01b['bases'], 'Its old base was')),
      L("So the new base is one hundred forty-four over eighty times as big. Let's simplify. Divide both by sixteen, "
        "and it's nine over five.", show(f01s1, 'Divide both by sixteen')),
      L("The volume is the base area times the height, and it stays the same. So if the base is multiplied by nine "
        "over five, the height is divided by nine over five. That means we multiply the old height by five over nine.",
        show(f01s2, 'we multiply the old height')),
      L("Nine times five over nine is five. Five again. Choice number three is our answer, and I'll see you in the next "
        "question.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-geo35-g122 - a cone four times a cylinder with the same base
# Hebrew geo 6324-6369 (equal volumes there -> 3h; four times here -> 12h): (1) the math way, an equation: pi r^2 h =
# pi r^2 H / 3, the base cancels; (2) understanding through volume ratios: same base and height -> the cone is a third;
# height x2 -> volume x2, x3 -> x3, so 3h; "some students read it and already know". R37: volume ratios are taught in
# geo-120 part 1 (this exact cone-and-cylinder case with 10 and 4); here applied with "like in the lesson". Traps 3h
# (equal volumes) and 4h (forgets the third) at their steps.
# V3: the copy, the two equal bases tinted, the heights h and H; method 2: the cone grows x3 then x4.
# =================================================================================================================
f122a = PIN(GEO('f122a', [
    ('line', [qraw('geo35-g122')]),
    ('bases', [_ell(215, 285, 62, 17, 'full', GTEAL, 4, False, GBAND), _ell(430, 285, 62, 17, 'full', GTEAL, 4, False, GBAND),
               ('txt', 320, 330, 'equal bases', 'teal', 24)]),
    ('hh', [sg((295, 165), (295, 285), 'orange', 5), sg((430, 95), (430, 285), 'orange', 5)]),
], vb='130 70 400 280', w=500, title='The cylinder and the cone'))
f122b = PIN(GEO('f122b', [
    ('line', cone_el(110, 300, 60, 70, 17) + [('txt', 110, 330, 'h: 1/3', 'teal', 22)]),
    ('three', cone_el(280, 300, 60, 210, 17) + [('txt', 280, 330, '3h: 1', 'teal', 22)]),
    ('twelve', [('txt', 450, 180, '× 4', 'orange', 34), ('txt', 450, 330, '12h: 4', 'orange', 24)]),
], vb='30 70 480 280', w=500, title='The same base: the volume follows the height'))
for _g in (f122a, f122b): QLEFT(_g, 'geo35-g122')
f122r1 = IH('f122r1', 'cylinder: $πr^2 \\cdot h$', size=30)
f122r2 = IH('f122r2', 'cone: $\\frac{πr^2 \\cdot H}{3}$', size=30)
f122r3 = IH('f122r3', '$\\frac{πr^2 H}{3} = 4 \\cdot πr^2 h$', size=30)
f122r4 = IH('f122r4', '$\\frac{H}{3} = 4h$', size=30)
f122r5 = IH('f122r5', '$H = 12h$', size=30)
f122s1 = IH('f122s1', 'height $h$: cone $= \\frac{1}{3}$ cylinder', size=30)
f122s2 = IH('f122s2', 'height $3h$: cone $=$ cylinder', size=30)
f122s3 = IH('f122s3', '$3h \\cdot 4 = 12h$', size=30)
FLOW([f122r1, f122r2, f122r3, f122r4, f122r5], QC('geo35-g122'))
FLOW([f122s1, f122s2, f122s3], QC('geo35-g122'))
NOFIG('solve-geo35-g122', 0, 1)

video('solve-geo35-g122', 'solution', qid='geo35-g122', slides=[
    SM('Method 1 · The math way', 'An equation',
      L("A cone and a cylinder have equal base areas. The volume of the cone is four times the volume of the cylinder. "
        "If the cylinder's height is h, what is the cone's height?", pt('stem', 'A cone and a cylinder', 'hl', 9.0),
        show(f122a['line'], 'A cone and a cylinder'), voice='calm', pause=0.5),
      L("So they want the cone's height, written with h. We'll solve it in two different ways, the math way, and then "
        "by understanding."),
      L("Let's start with the math way, with an equation. The cylinder is a straight solid, so its volume is the base "
        "area, pi r squared, times its height, h.", show(f122a['bases'], 'The cylinder is a straight solid'), show(f122r1, 'The cylinder is a straight solid')),
      L("The cone has the same base, pi r squared. Its height isn't given, so let's call it H. The cone is pointed, so "
        "its volume is pi r squared, times H, divided by three.", show(f122a['hh'], "let's call it H"), show(f122r2, 'so its volume is pi r squared, times H')),
      L("The given says the cone is four times the cylinder. So the cone's volume is equal to four times pi r squared "
        "h.", show(f122r3, 'four times pi r squared')),
      L("Pi r squared is on both sides, so we divide both sides by it. We're left with H over three is equal to four "
        "h.", show(f122r4, 'H over three is equal to four')),
      L("Now we multiply both sides by three. Three times four h is twelve h. So H is twelve h. Choice number four is "
        "our answer.", show(f122r5, 'So H is twelve h'), mk('tick', 'choice 4', 'Choice number four is'))),
    SM('Method 2 · Understanding', 'Volume ratios',
      L("Now by understanding, with volume ratios, like in the lesson. Some students know the answer without any "
        "equation. How?", show(f122b['line'], 'Now by understanding')),
      L("The cone and the cylinder have the same base. If the cone also had the same height, h, it would be one third "
        "of the cylinder.", show(f122s1, 'it would be one third')),
      L("When the base stays the same, the volume grows like the height. So to make the cone equal to the cylinder, we "
        "make it three times as tall, three h.", show(f122b['three'], 'three times as tall'), show(f122s2, 'three h.')),
      L("Careful, three h is choice number two, and it's a trap. Three h gives equal volumes. But the given says the "
        "cone is four times the cylinder.", mk('cross', 'choice 2', 'three h is choice number two')),
      L("So we make the cone four times as tall again. Three h times four is twelve h.",
        show(f122b['twelve'], 'four times as tall again'), show(f122s3, 'Three h times four')),
      L("And four h, choice number one, forgets that the cone is only a third. Choice number four is our answer, and "
        "I'll see you in the next question.", mk('cross', 'choice 1', 'choice number one, forgets'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])


# =================================================================================================================
# solve-geo35-g123 - a triangular prism cut from a box
# Hebrew geo 6372-6436 (x : x and 120 there -> 1/4, 30; 1 : 3 and 320 here -> 1/8, 40): (1) the math way: add unknowns
# (length 2x there, 4x here; depth y, height z) - "not clear yet what we'll do with it, but it's given, so we'll need it";
# the shaded solid: equal bottom and top bases -> straight, a triangular prism; the angle between x and y is 90 (the base
# of a box is a rectangle); x y / 2 times z = half of x y z; (2) the insight, symmetry from above: the line through M
# cuts the rectangle, the diagonal halves the strip; in the box a wall instead of a line, so the volume ratio = the area
# ratio; "almost always there's a shorter way". R37: straight / pointed and base area x height are geo-119 reminders.
# V3: the copy, AM = x and MB = 3x, the triangle AMD teal, the prism tinted; the top view pulled out as a flat rectangle.
# =================================================================================================================
_A3, _B3, _C3, _D3 = (135.388, 277.736), (424.975, 277.736), (504.612, 227.058), (215.025, 227.058)
_E3, _F3, _G3, _H3 = (135.388, 132.942), (424.975, 132.942), (504.612, 82.264), (215.025, 82.264)
_M3, _N3 = (207.785, 277.736), (207.785, 132.942)
f123a = PIN(GEO('f123a', [
    ('line', [qraw('geo35-g123')]),
    ('dims', [('txt', 22, 210, 'z', 'orange', 30, True), ('txt', 150, 252, 'y', 'orange', 30, True)]),
], vb='0 40 560 300', w=520, title='The box'))
f123c = PIN(GEO('f123c', [
    ('line', [qraw('geo35-g123'), ('txt', 22, 210, 'z', 'orange', 30, True), ('txt', 150, 252, 'y', 'orange', 30, True)]),
    ('prism', [('tint', [_A3, _M3, _N3, _E3], 'orange'), ('tint', [_E3, _N3, _H3], 'orange'), ('poly', [_E3, _N3, _H3], 'orange', 4)]),
    ('tri', [('tint', [_A3, _M3, _D3], 'teal'), ('poly', [_A3, _M3, _D3], 'teal', 4), rt(_A3, _M3, _D3, 12, 'teal')]),
], vb='0 40 560 300', w=520, title='The triangular prism'))
_tv = [(60, 300), (460, 300), (460, 120), (60, 120)]
f123b = PIN(GEO('f123b', [
    ('line', [('poly', _tv, 'ink', 3), ('txt', 40, 330, 'A', 'ink', 26, True), ('txt', 480, 330, 'B', 'ink', 26, True),
              ('txt', 480, 110, 'C', 'ink', 26, True), ('txt', 40, 110, 'D', 'ink', 26, True)]),
    ('cut', [sg((160, 300), (160, 120), 'teal', 3, True), ('txt', 160, 330, 'M', 'ink', 26, True),
             sg((260, 300), (260, 120), 'ink', 1.5, True), sg((360, 300), (360, 120), 'ink', 1.5, True),
             ('txt', 110, 345, 'x', 'teal', 26, True), ('txt', 310, 345, '3x', 'teal', 26, True)]),
    ('strip', [('tint', [(60, 300), (160, 300), (160, 120), (60, 120)], 'teal'), ('txt', 110, 210, '1/4', 'teal', 28)]),
    ('half', [sg((160, 300), (60, 120), 'orange', 4), ('tint', [(60, 300), (160, 300), (60, 120)], 'orange'),
              ('txt', 90, 260, '1/8', 'orange', 26)]),
], vb='20 80 480 290', w=520, title='The box seen from above'))
for _g in (f123a, f123b, f123c): QLEFT(_g, 'geo35-g123')
f123r1 = IH('f123r1', '$AB = x + 3x = 4x$', size=30)
f123r2 = IH('f123r2', '$4x \\cdot y \\cdot z = 320$', size=30)
f123r3 = IH('f123r3', 'triangle: $\\frac{x \\cdot y}{2}$', size=30)
f123r4 = IH('f123r4', 'prism: $\\frac{xy}{2} \\cdot z = \\frac{xyz}{2}$', size=30)
f123r5 = IH('f123r5', '$xyz = 320 \\div 4 = 80$', size=30)
f123r6 = IH('f123r6', '$80 \\div 2 = 40$', size=30)
f123s1 = IH('f123s1', 'the strip: $\\frac{1}{4}$ of the base', size=30)
f123s2 = IH('f123s2', 'the triangle: $\\frac{1}{2} \\cdot \\frac{1}{4} = \\frac{1}{8}$', size=30)
f123s3 = IH('f123s3', '$320 \\div 8 = 40$', size=30)
FLOW([f123r1, f123r2], QC('geo35-g123'))
FLOW([f123r3, f123r4, f123r5, f123r6], QC('geo35-g123'))
FLOW([f123s1, f123s2, f123s3], QC('geo35-g123'))
NOFIG('solve-geo35-g123', 0, 1, 2)
CARRY35['solve-geo35-g123'] = {1: ['$4x \\cdot y \\cdot z = 320$']}

video('solve-geo35-g123', 'solution', qid='geo35-g123', slides=[
    SM('Method 1 · The math way: add unknowns', 'The math way',
      L("The volume of box A B C D E F G H is three hundred twenty. M lies on A B, so that A M to M B is one to three. N "
        "lies right above M, on E F. What is the volume of the triangular prism A M D, E N H?",
        pt('stem', 'The volume of box', 'hl', 11.0), show(f123a['line'], 'The volume of box'), voice='calm', pause=0.5),
      L("We'll solve it in two different ways, the math way, and then with an insight. Let's start with the math way."),
      L("The volume of the box is given, three hundred twenty. A box is straight, so its volume is length times width "
        "times height."),
      L("The only other given is the ratio, one to three. So let's call A M x, and M B three x. Then the length, A B, "
        "is four x.", show(f123r1, 'is four x')),
      L("Nothing is given about the width or the height. So let's add unknowns, the width y and the height z. We don't "
        "know their values, but we can use these letters to write both volumes.", show(f123a['dims'], "let's add unknowns")),
      L("So four x times y times z is three hundred twenty.", show(f123r2, 'four x times y times z')),
    ),
    SM('Method 1 · The math way: add unknowns', 'The shaded prism',
      L("Now, they ask for the volume of the shaded solid. Is it straight or pointed? Its bottom base, A M D, and its top "
        "base, E N H, are the same triangle. So it's straight, a triangular prism.", show(f123c['line'], 'Now, they ask'), show(f123c['prism'], 'the volume of the shaded solid')),
      L("Its base is triangle A M D. The angle at A is a right angle, because the base of a box is a rectangle. So the "
        "triangle's area is x times y, divided by two.", show(f123c['tri'], 'Its base is triangle A M D'), show(f123r3, 'x times y, divided by two')),
      L("The prism's height is the box's height, z. So its volume is x times y, divided by two, times z. That's x times y times z, divided by two.",
        show(f123r4, 'So its volume is')),
      L("Now it clears up. Four x times y times z is three hundred twenty. So x times y times z is three hundred "
        "twenty divided by four, eighty. And half of eighty is forty. Choice number three is our answer.",
        show(f123r5, 'divided by four, eighty'), show(f123r6, 'half of eighty is forty'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Insight: from above', 'Look from above',
      L("Now the insight. There's a much shorter way. Let's look at the box from above, so we see only its base, the "
        "rectangle A B C D.", show(f123b['line'], "Let's look at the box from above")),
      L("A M to M B is one to three, so A B has four equal units. Draw parallel lines to divide the base into four "
        "equal strips, each as wide as A M. The strip on the left is one quarter of the base.", show(f123b['cut'], 'Draw parallel lines'), show(f123b['strip'], 'The strip on the left'),
        show(f123s1, 'one quarter of the base')),
      L("The diagonal from M to D cuts this strip in half. So triangle A M D is half of a quarter, one eighth of the "
        "base.", show(f123b['half'], 'The diagonal from M to D'), show(f123s2, 'half of a quarter')),
      L("In the box, instead of a line we have a wall, straight up, at the same height. So the prism is one eighth of "
        "the box too. Three hundred twenty divided by eight is forty.", show(f123s3, 'Three hundred twenty divided by eight')),
      L("So the insight was much shorter. On the exam, there's almost always a shorter way. Choice number three is our "
        "answer, and I'll see you in the next question.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-geo35-g124 - the lateral area of a triangular prism lying on its side
# Hebrew geo 6439-6468 (3-4-5, height 2 there -> 24; 9-12-15, height 5 here -> 180): (1) the formula: base perimeter x
# height; the triple; add 3 + 4 + 5, or "the average is 4, so 3 x 4"; (2) add the three faces; "pick the way that suits
# you" is NOT copied (R16). R37: perimeter x height and the prism lying down are geo-119 (reminders). Kept from the
# English: the trap 288 (the total surface area) at its step.
# V3: the copy, the two triangle bases tinted teal, the height BE orange, the missing leg 12; the three faces one by one.
# =================================================================================================================
_A4, _B4, _C4, _D4, _E4, _F4 = (240, 307), (411, 307), (240, 79), (292, 274), (463, 274), (292, 46)
f124a = PIN(GEO('f124a', [
    ('line', [qraw('geo35-g124')]),
    ('bases', [('tint', [_A4, _B4, _C4], 'teal'), ('poly', [_A4, _B4, _C4], 'teal', 4), ('poly', [_D4, _E4, _F4], 'teal', 3, True)]),
    ('h', [sg(_B4, _E4, 'orange', 7)]),
    ('ac', [('txt', 214, 195, '12', 'teal', 30)]),
], vb='160 10 360 340', w=440, title='The prism lying on its side'))
f124b = PIN(GEO('f124b', [
    ('line', [qraw('geo35-g124'), ('txt', 214, 195, '12', 'ink', 28)]),
    ('f1', [('tint', [_A4, _B4, _E4, _D4], 'teal'), ('txt', 350, 296, '45', 'teal', 26)]),
    ('f2', [('tint', [_A4, _C4, _F4, _D4], 'orange'), ('txt', 266, 170, '60', 'orange', 26)]),
    ('f3', [('tint', [_B4, _C4, _F4, _E4], 'teal'), ('txt', 370, 170, '75', 'teal', 26)]),
], vb='160 10 360 340', w=440, title='The three side faces'))
for _g in (f124a, f124b): QLEFT(_g, 'geo35-g124')
f124r1 = IH('f124r1', '$9, 12, 15 = 3 \\cdot (3, 4, 5)$', size=30)
f124r2 = IH('f124r2', '$9 + 12 + 15 = 36$', size=30)
f124r3 = IH('f124r3', 'or: $3 \\cdot 12 = 36$', size=30)
f124r4 = IH('f124r4', '$36 \\cdot 5 = 180$', size=30)
f124r5 = IH('f124r5', 'bases: $2 \\cdot \\frac{9 \\cdot 12}{2} = 108$', size=30)
f124r6 = IH('f124r6', '$180 + 108 = 288$: total, no', size=30)
f124s1 = IH('f124s1', '$9 \\cdot 5 = 45$', size=30)
f124s2 = IH('f124s2', '$12 \\cdot 5 = 60$', size=30)
f124s3 = IH('f124s3', '$15 \\cdot 5 = 75$', size=30)
f124s4 = IH('f124s4', '$45 + 75 = 120$, $\\ 120 + 60 = 180$', size=30)
FLOW([f124r1, f124r2, f124r3, f124r4, f124r5, f124r6], QC('geo35-g124'))
FLOW([f124s1, f124s2, f124s3, f124s4], QC('geo35-g124'))
NOFIG('solve-geo35-g124', 0, 1)

video('solve-geo35-g124', 'solution', qid='geo35-g124', slides=[
    SM('Method 1 · The math way: perimeter times height', 'Perimeter times height',
      L("The bases of a right triangular prism are right triangles. Each base has a leg of nine and a hypotenuse of "
        "fifteen. The height of the prism is five. What is its lateral surface area?",
        pt('stem', 'The bases of a right triangular prism', 'hl', 10.0), show(f124a['line'], 'The bases of a right triangular prism'),
        voice='calm', pause=0.5),
      L("Careful here, this prism lies on its side. Like in the first lesson, the bases are the two identical faces, the "
        "triangles at the front and at the back.", show(f124a['bases'], 'the bases are the two identical faces')),
      L("The height is the distance between them, the edge B E. It's five, and it lies flat on the floor.",
        show(f124a['h'], 'the edge B E')),
      L("The lateral area is the side faces only, without the two bases. We'll find it in two different ways. Let's "
        "start with the math way, the perimeter of the base times the height."),
      L("For the perimeter we need all three sides of the triangle. We have nine and fifteen. Nine and fifteen are three "
        "times three and three times five. So this is the triple three, four, five, times three, and the missing leg is "
        "three times four, twelve.", show(f124r1, 'So this is the triple'), show(f124a['ac'], 'the missing leg is')),
      L("So the perimeter is nine plus twelve plus fifteen, thirty-six. Or use twelve for all three sides. "
        "Nine is three below twelve, and fifteen is three above twelve. The three taken away and the three added cancel. "
        "So the sum is three times twelve, thirty-six.", show(f124r2, 'nine plus twelve plus fifteen'),
        show(f124r3, 'three times twelve')),
      L("Thirty-six times the height, five, is one hundred eighty.", show(f124r4, 'Thirty-six times the height')),
      L("Careful with two traps. The two triangle bases together are nine times twelve, which is one hundred eight, and "
        "that's choice number two. Adding them to one hundred eighty gives two hundred eighty-eight, choice number four. "
        "That's the total surface area, not the lateral area.", show(f124r5, 'The two triangle bases together'),
        show(f124r6, 'Adding them to one hundred eighty'), mk('cross', 'choice 2', "that's choice number two"),
        mk('cross', 'choice 4', 'choice number four'))),
    SM('Method 2 · The math way: add the faces', 'Add the faces',
      L("Now the second way, the math way face by face. There are three side faces, and each one is a rectangle. Its "
        "length is a side of the triangle, and its width is the height, five.", show(f124b['line'], 'Now the second way')),
      L("The bottom face is nine times five, forty-five.", show(f124b['f1'], 'The bottom face'), show(f124s1, 'nine times five')),
      L("The face at the back is twelve times five, sixty.", show(f124b['f2'], 'The face at the back'), show(f124s2, 'twelve times five')),
      L("And the slanted face is fifteen times five, seventy-five.", show(f124b['f3'], 'the slanted face'), show(f124s3, 'fifteen times five')),
      L("Forty-five plus seventy-five is one hundred twenty, plus sixty, one hundred eighty. Choice number one is our "
        "answer, and I'll see you in the next question.", show(f124s4, 'Forty-five plus seventy-five'),
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])


# =================================================================================================================
# solve-geo35-g125 - eighteen cubes: the smallest surface area
# Hebrew geo 6471-6555 (8 cubes in four shapes there, three of them not boxes; 18 cubes in four boxes here): a min / max
# question in geometry; surface = the sum of ALL the faces; "no formula for these shapes, so trial and error": one face =
# 1, count the front, the top and the side and double by symmetry; the out-of-time move ("24 < 34 already drops choice 1;
# this comes near the end of the section"); then the insight: apart = every face counts = the biggest surface; every
# contact loses 2 faces; the more compact, the smaller -> the cube. Her reason "no formula" fits non-box shapes; here
# the four choices are boxes, so the script says the box formula exists and that counting is the same thing and works
# for any shape (the staircase of the lesson geo-120 part 3, where a non-box shape is counted). R37: counting by
# direction and "a contact hides two faces" are taught in geo-120 part 3; here applied with "like in the lesson".
# V3: the 1 x 2 x 9 block and the 2 x 3 x 3 block built of cubes, the front / top / right faces tinted as counted.
# =================================================================================================================
_b1 = [(i, j, 0) for i in range(9) for j in range(2)]
_b2 = [(i, j, k) for i in range(3) for j in range(3) for k in range(2)]
_s5 = 42
f125a = PIN(GEO('f125a', [
    ('line', unit_cubes(_b1, 30, 230, _s5) + [('txt', 220, 262, '9', 'ink', 26), ('txt', 12, 190, '2', 'ink', 26), ('txt', 420, 220, '1', 'ink', 26)]),
    ('front', [('tint', cube_face(i, j, k, 'front', 30, 230, _s5), 'teal') for (i, j, k) in _b1] + [('txt', 200, 290, 'front 18', 'teal', 24)]),
    ('top', [('tint', cube_face(i, 1, 0, 'top', 30, 230, _s5), 'orange') for i in range(9)] + [('txt', 200, 112, 'top 9', 'orange', 24)]),
    ('right', [('tint', cube_face(8, j, 0, 'right', 30, 230, _s5), 'ink') for j in range(2)] + [('txt', 452, 170, 'side 2', 'ink', 24)]),
], vb='0 90 500 220', w=520, title='Choice 1: a block 1 by 2 by 9'))
f125b = PIN(GEO('f125b', [
    ('line', unit_cubes(_b2, 80, 300, 60) + [('txt', 170, 330, '3', 'ink', 26), ('txt', 58, 210, '3', 'ink', 26), ('txt', 300, 300, '2', 'ink', 26)]),
    ('front', [('tint', cube_face(i, j, 0, 'front', 80, 300, 60), 'teal') for i in range(3) for j in range(3)] + [('txt', 380, 250, 'front 9', 'teal', 24)]),
    ('top', [('tint', cube_face(i, 2, k, 'top', 80, 300, 60), 'orange') for i in range(3) for k in range(2)] + [('txt', 380, 90, 'top 6', 'orange', 24)]),
    ('right', [('tint', cube_face(2, j, k, 'right', 80, 300, 60), 'ink') for j in range(3) for k in range(2)] + [('txt', 380, 170, 'side 6', 'ink', 24)]),
], vb='40 50 420 300', w=440, title='Choice 2: a block 2 by 3 by 3'))
f125c = PIN(GEO('f125c', [
    ('line', unit_cubes(_b2, 80, 300, 60) + [('txt', 250, 340, 'the tightest block', 'teal', 26)]),
], vb='40 50 420 310', w=440, title='The tightest block: the most contacts'))
QLEFT(f125a, 'geo35-g125'); QLEFT(f125b, 'geo35-g125'); QLEFT(f125c, 'geo35-g125')
f125r1 = IH('f125r1', '(1) $18 + 9 + 2 = 29$', size=30)
f125r2 = IH('f125r2', '$2 \\cdot 29 = 58$', size=30)
f125r3 = IH('f125r3', '(2) $9 + 6 + 6 = 21$', size=30)
f125r4 = IH('f125r4', '$2 \\cdot 21 = 42 < 58$', size=30)
f125s1 = IH('f125s1', '(3) $18 + 18 + 1 = 37$, $\\ 74$', size=30)
f125s2 = IH('f125s2', '(4) $18 + 6 + 3 = 27$, $\\ 54$', size=30)
f125t1 = IH('f125t1', 'apart: $18 \\cdot 6 = 108$ faces', size=30)
f125t2 = IH('f125t2', 'every contact: $-2$', size=30)
FLOW([f125r1, f125r2, f125r3, f125r4], QC('geo35-g125'))
FLOW([f125s1, f125s2], QC('geo35-g125'))
FLOW([f125t1, f125t2], QC('geo35-g125'))
NOFIG('solve-geo35-g125', 0, 1, 2)

video('solve-geo35-g125', 'solution', qid='geo35-g125', slides=[
    SM('Method 1 · The math way: counting faces', 'Count the faces',
      L("Eighteen identical cubes, each with edge one, are joined face to face to form a block. Which block has the "
        "smallest total surface area?", pt('stem', 'Eighteen identical cubes', 'hl', 8.0), voice='calm', pause=0.5),
      L("So this is a minimum question in geometry. Each block is made of the same eighteen cubes, and we want the one "
        "whose surface is the smallest. The surface area is all the faces, also the ones we can't see, the back and the "
        "bottom."),
      L("We'll solve it in two different ways. Let's start with the math way, counting faces, like in the lesson. One "
        "small face has area one. These four blocks are boxes, so there's also a formula. But counting is the same "
        "thing, and it works for any shape."),
      L("Choice number one, a block one by two by nine. From the front we see two rows of nine, eighteen faces.",
        show(f125a['line'], 'a block one by two by nine'), show(f125a['front'], 'From the front')),
      L("From above, nine faces. And from the side, two.", show(f125a['top'], 'From above'), show(f125a['right'], 'from the side, two')),
      L("Eighteen plus nine plus two is twenty-nine. Every face has a twin on the opposite side, so we double it. Two "
        "times twenty-nine is fifty-eight.", show(f125r1, 'Eighteen plus nine plus two'), show(f125r2, 'Two times twenty-nine')),
      L("Choice number two, a block two by three by three. From the front, three rows of three, nine. From above, six. "
        "From the side, six.", show(f125b['line'], 'a block two by three by three'), show(f125b['front'], 'three rows of three'),
        show(f125b['top'], 'From above, six'), show(f125b['right'], 'From the side, six')),
      L("Nine plus six plus six is twenty-one, and two times twenty-one is forty-two. That's already less than "
        "fifty-eight. We want the smallest, so choice number one is out.",
        show(f125r3, 'Nine plus six plus six'), show(f125r4, 'two times twenty-one'), mk('cross', 'choice 1', 'so choice number one is out')),
      L("This kind of question usually comes near the end of the section. So if time runs short, cross out what you "
        "already can, and move on.")),
    SM('Method 1 · The math way: counting faces', 'The other two',
      L("Choice number three, the long stick, one by one by eighteen. Eighteen from the front, eighteen from above, and "
        "one from the side. That's thirty-seven, and twice that is seventy-four. Bigger, so it's out.",
        show(f125s1, 'That\'s thirty-seven'), mk('cross', 'choice 3', 'Bigger, so it\'s out')),
      L("Choice number four, one by three by six. From the front eighteen, from above six, and from the side three. That's twenty-seven, and twice that is "
        "fifty-four. Also bigger than forty-two, so it's out.", show(f125s2, "That's twenty-seven"),
        mk('cross', 'choice 4', 'Also bigger than forty-two')),
      L("So we counted all four, and choice number two has the smallest surface, forty-two. It's not hard, but it's "
        "long.", pt('choice 2', 'choice number two has the smallest surface'))),
    SM('Method 2 · Insight: pack them tight', 'Pack them tight',
      L("Now the insight. When is the surface area the biggest? Let's think the other way round."),
      L("Each cube has six faces. If the eighteen cubes lie apart, all eighteen times six, one hundred eight faces, "
        "count. Nothing is hidden. That's the biggest surface.", show(f125t1, 'one hundred eight faces')),
      L("Now we push them together. Like in the lesson, every place where two cubes touch hides two faces, one from "
        "each cube. So the more contacts, the smaller the surface.", show(f125t2, 'every place where two cubes touch')),
      L("The most contacts are in the tightest block, the one closest to a cube. Of our four blocks, that's two by "
        "three by three.", show(f125c['line'], 'the tightest block')),
      L("So choice number two, without counting a single face. Choice number two is our answer, and I'll see you in "
        "the next question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# solve-geo35-g126 - a cylinder inscribed in a box: the part outside
# Hebrew geo 6558-6648 (side a, height 2a, the ratio cylinder / box = pi / 4 there; side 2k, height 5k, the part outside
# = 1 - pi / 4 here): "inscribed and circumscribed, as in circles"; three ways: (1) the full math (the side is the
# diameter, r = a / 2 there, r = k here); (2) plug in numbers, "not automatically 1" (her reason: the radius would be a
# fraction; here: with k = 1 three choices are equal, so 1 can't separate them - take k = 2); (3) estimation: the ratio of
# two volumes stays the same when the shape grows (the rule from circles), so a choice with the letter is a distractor;
# pi / 2 is more than 1, impossible; pi / 4, about three quarters, makes sense. Her verdict ("full math not recommended,
# plugging in the safest") is not copied (R16).
# V3: the top view copy; the diameter = the side 2k teal, the radius k orange; plug-in labels 4 and 2; method 3: the
# choices with k crossed.
# =================================================================================================================
f126a = PIN(GEO('f126a', [
    ('line', [qraw('geo35-g126')]),
    ('d', [sg((215.714, 180), (424.286, 180), 'teal', 5), ('txt', 270, 165, '2k', 'teal', 28, True)]),
    ('r', [('txt', 372, 200, 'k', 'orange', 30, True), sg((320, 180), (424.286, 180), 'orange', 5)]),
], vb='180 50 280 280', w=380, title='The top view: a circle in a square'))
f126b = PIN(GEO('f126b', [
    ('line', [qraw('geo35-g126'), ('txt', 320, 330, 'k = 2: side 4, height 10', 'teal', 22)]),
    ('r', [sg((320, 180), (424.286, 180), 'orange', 5), ('txt', 372, 200, '2', 'orange', 30)]),
], vb='180 50 280 300', w=380, title='Plug in k = 2'))
for _g in (f126a, f126b): QLEFT(_g, 'geo35-g126')
f126r1 = IH('f126r1', 'box: $(2k)^2 \\cdot 5k = 20k^3$', size=30)
f126r2 = IH('f126r2', '$2r = 2k$, so $r = k$', size=30)
f126r3 = IH('f126r3', 'cylinder: $πk^2 \\cdot 5k = 5πk^3$', size=30)
f126r4 = IH('f126r4', '$\\frac{20k^3 - 5πk^3}{20k^3}$', size=30)
f126r5 = IH('f126r5', '$= 1 - \\frac{π}{4}$', size=30)
f126s1 = IH('f126s1', '$k = 1$: (1), (3), (4) the same', size=30)
f126s2 = IH('f126s2', 'box: $4 \\cdot 4 \\cdot 10 = 160$', size=30)
f126s3 = IH('f126s3', 'cylinder: $π \\cdot 2^2 \\cdot 10 = 40π$', size=30)
f126s4 = IH('f126s4', '$\\frac{160 - 40π}{160} = 1 - \\frac{π}{4}$', size=30)
f126s5 = IH('f126s5', '(1) $1 - \\frac{2π}{4} = 1 - \\frac{π}{2}$', size=30)
f126s6 = IH('f126s6', '(3) $1 - \\frac{π}{8}$', size=30)
f126s7 = IH('f126s7', '(2) $1 - \\frac{π}{2}$', size=30)
f126t1 = IH('f126t1', 'bigger box, same fraction: no $k$', size=30)
f126t2 = IH('f126t2', '$π > 3$, so $\\frac{π}{2} > 1$', size=30)
f126t3 = IH('f126t3', '$1 - \\frac{π}{2} < 0$', size=30)
FLOW([f126r1, f126r2, f126r3, f126r4, f126r5], QC('geo35-g126'))
FLOW([f126s1, f126s2, f126s3, f126s4], QC('geo35-g126'))
FLOW([f126s5, f126s6, f126s7], [(430, 1150, QTOP('geo35-g126') + 80, QBOT('geo35-g126'))])
FLOW([f126t1, f126t2, f126t3], QC('geo35-g126'))
NOFIG('solve-geo35-g126', 0, 1, 2, 3)
CARRY35['solve-geo35-g126'] = {2: ['$k = 2$: the part outside is $1 - \\frac{π}{4}$']}

video('solve-geo35-g126', 'solution', qid='geo35-g126', slides=[
    SM('Method 1 · The math way', 'The math way',
      L("A cylinder is inscribed in a box. The box has a square base with side two k, and its height is five k. The "
        "cylinder has the same height, and its circles are inscribed in the squares. What fraction of the box is outside "
        "the cylinder?", pt('stem', 'A cylinder is inscribed in a box', 'hl', 11.0), show(f126a['line'], 'A cylinder is inscribed'),
        voice='calm', pause=0.5),
      L("Inscribed means the cylinder fits exactly inside the box. We met inscribed shapes in circles, and here it's the "
        "same idea in three dimensions. We'll solve it in three different ways."),
      L("Let's start with the math way. The box is straight, so its volume is the base times the height. The base is two k "
        "times two k, four k squared. Times five k, that's twenty k to the power of three.", show(f126r1, 'The base is two k')),
      L("The cylinder is straight too, but we need its radius, written with k. The circle sits exactly inside the "
        "square. So the side of the square is the diameter of the circle. Two r is two k, so r is k.",
        show(f126a['d'], 'the side of the square is the diameter'), show(f126r2, 'Two r is two k'), show(f126a['r'], 'so r is k')),
      L("So the cylinder is pi times k squared, times five k. That's five pi k to the power of three.", show(f126r3, 'pi times k squared')),
      L("The part outside is the box minus the cylinder. To get a fraction of the box, we divide it by the box.",
        show(f126r4, 'we divide it by the box')),
      L("Divide each term on top by the box's volume, twenty k cubed. The first term gives one. In the second, "
        "k cubed cancels, and five over twenty is one over four. So the second term is pi over four. "
        "We subtract it, so it's one minus pi over four. Choice "
        "number four, but it was long.", show(f126r5, 'one minus pi over four'), mk('tick', 'choice 4', 'Choice number four, but'))),
    SM('Method 2 · Plugging in numbers', 'Plug in a number',
      L("Now let's plug in numbers, like with inscribed shapes in circles. Usually we'd think one is the easiest "
        "number."),
      L("But look at the choices. With k equal to one, choice numbers one, three and four all become one minus pi over "
        "four. One can't tell them apart.", show(f126s1, 'With k equal to one')),
      L("So let's take another easy number, k is two. Then the box is four by four by ten, one hundred sixty.",
        show(f126b['line'], 'k is two'), show(f126s2, 'four by four by ten')),
      L("The radius is half the side, two. So the cylinder is pi times two squared, times ten, forty pi.",
        show(f126b['r'], 'The radius is half the side'), show(f126s3, 'forty pi')),
      L("The part outside, divided by the box, is one hundred sixty minus forty pi, over one hundred sixty. That's one "
        "minus pi over four.", show(f126s4, 'over one hundred sixty')),
    ),
    SM('Method 2 · Plugging in numbers', 'Check the choices',
      L("Now we put k equal to two into the choices. Choice number one gives one minus two pi over four, that's one "
        "minus pi over two. Choice number three gives one minus pi over eight. Choice number two is one minus pi over "
        "two. None of them is one minus pi over four.", show(f126s5, 'Choice number one gives'), show(f126s6, 'Choice number three gives'), show(f126s7, 'Choice number two is one minus'),
        mk('cross', 'choice 1', 'Choice number one gives'), mk('cross', 'choice 3', 'Choice number three gives'),
        mk('cross', 'choice 2', 'Choice number two is one minus')),
      L("So choice number four again.", mk('tick', 'choice 4', 'So choice number four again'))),
    SM('Method 3 · Estimation', 'Estimate',
      L("And a third way, with an estimate. Remember the rule from circles. If we make the whole shape bigger or "
        "smaller, the ratio between its parts stays the same."),
      L("So the fraction of the box outside the cylinder is the same for any k. The answer can't have k in it. So "
        "choice numbers one and three are out.", show(f126t1, 'The answer can\'t have k in it'),
        mk('cross', 'choice 1', 'So choice numbers one and three'), mk('cross', 'choice 3', 'and three are out')),
      L("Choice number two is one minus pi over two. Pi is more than three, so pi over two is more than one and a "
        "half, more than one.", show(f126t2, 'Pi is more than three')),
      L("One minus something bigger than one is negative. A part of the box can't be a negative fraction, so choice "
        "number two is out.", show(f126t3, 'is negative'), mk('cross', 'choice 2', 'so choice number two is out')),
      L("And choice number four makes sense. Pi over four is a bit more than three quarters. So the cylinder fills a bit "
        "more than three quarters of the box, and a bit less than a quarter is outside. Choice number four is our "
        "answer, and I'll see you in the next question.", mk('tick', 'choice 4', 'Choice number four is our answer'))),
])


# =================================================================================================================
# solve-geo35-g127 - a pyramid removed from a cube
# Hebrew geo 6650-6692 (18 left there -> 9; 60 left here -> 30): (1) the math way: a scheme cube - pyramid = what's left,
# the edge a, a^3 - a^3 / 3 = 18, a = 3, 9; (2) volume ratios in ratio units: the pyramid 1, the cube 3, what's left 2
# -> 2 units = 18 -> 9, "volume ratios really help". Here a^3 = 90, so a is not a whole number - and we don't need it.
# R37: the units are taught in geo-120 part 1 (the cone in the cylinder, 40 left -> 20); here applied. The trap 90 (the
# cube) at its step.
# V3: the copy, the pyramid tinted orange inside the cube, the units written beside it.
# =================================================================================================================
_P7 = (302.243, 87.27); _A7, _B7, _C7, _D7 = (197.676, 286.541), (355.514, 286.541), (442.324, 231.297), (284.486, 231.297)
f127a = PIN(GEO('f127a', [
    ('line', [qraw('geo35-g127')]),
    ('pyr', [('tint', [_P7, _A7, _B7], 'orange'), ('tint', [_P7, _B7, _C7], 'orange'), ('poly', [_A7, _B7, _C7, _D7], 'orange', 3, True)]),
    ('left', [('txt', 520, 150, 'left: 60', 'teal', 28)]),
], vb='160 40 460 290', w=500, title='The pyramid inside the cube'))
f127b = PIN(GEO('f127b', [
    ('line', [qraw('geo35-g127'), ('tint', [_P7, _A7, _B7], 'orange'), ('tint', [_P7, _B7, _C7], 'orange')]),
    ('u', [('txt', 540, 110, 'pyramid: 1', 'orange', 26), ('txt', 540, 160, 'cube: 3', 'ink', 26), ('txt', 540, 210, 'left: 2', 'teal', 26)]),
], vb='160 40 480 290', w=500, title='Ratio units'))
for _g in (f127a, f127b): QLEFT(_g, 'geo35-g127')
f127r1 = IH('f127r1', 'cube $-$ pyramid $= 60$', size=28)
f127r2 = IH('f127r2', '$a^3 - \\frac{a^3}{3} = 60$', size=28)
f127r3 = IH('f127r3', '$\\frac{2}{3} a^3 = 60$', size=28)
f127r4 = IH('f127r4', '$a^3 = 60 \\cdot \\frac{3}{2} = 90$', size=28)
f127r5 = IH('f127r5', 'pyramid: $\\frac{a^3}{3} = \\frac{90}{3} = 30$', size=28)
f127s1 = IH('f127s1', '$2$ units $= 60$', size=30)
f127s2 = IH('f127s2', '$1$ unit $= 60 \\div 2 = 30$', size=30)
FLOW([f127r1, f127r2, f127r3, f127r4, f127r5], QC('geo35-g127'))
FLOW([f127s1, f127s2], QC('geo35-g127'))
NOFIG('solve-geo35-g127', 0, 1)

video('solve-geo35-g127', 'solution', qid='geo35-g127', slides=[
    SM('Method 1 · The math way', 'Cube minus pyramid',
      L("A pyramid is removed from a cube. The pyramid's base is the whole bottom face of the cube, and its top point "
        "is on the top face. The solid that's left has volume sixty. What was the volume of the pyramid?",
        pt('stem', 'A pyramid is removed from a cube', 'hl', 10.0), show(f127a['line'], 'A pyramid is removed'),
        voice='calm', pause=0.5),
      L("We'll solve it in two different ways, the math way, and then by understanding. Let's start with the math way. "
        "We build a scheme. The cube, minus the pyramid, is what's left, sixty.", show(f127a['pyr'], 'minus the pyramid'),
        show(f127r1, 'is what\'s left, sixty'), show(f127a['left'], "what's left, sixty")),
      L("No edge is given, so let's call it a. The cube is a to the power of three."),
      L("The pyramid has the same base as the cube. Its top point is on the top face, so its height is the cube's "
        "height too. So it's a pointed solid with the same base and height, one third of the cube.",
        show(f127r2, 'one third of the cube')),
      L("A whole cube minus one third of it is two thirds of it. So two thirds of a to the power of three is sixty.",
        show(f127r3, 'two thirds of a to the power of three')),
      L("To find a to the power of three, we multiply sixty by three over two. Sixty divided by two is thirty, times "
        "three, ninety.", show(f127r4, 'we multiply sixty by three over two')),
      L("Careful, ninety is choice number four. But ninety is the whole cube, not the pyramid.",
        mk('cross', 'choice 4', 'ninety is choice number four')),
      L("Here a isn't even a whole number. But we don't need a. The pyramid is a to the power of three, divided by "
        "three. Ninety divided by three is thirty. Choice number three is our answer.",
        show(f127r5, 'ninety divided by three'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Understanding: ratio units', 'Ratio units',
      L("Now by understanding, with ratio units, like the cone in the cylinder in the lesson.", show(f127b['line'], 'Now by understanding')),
      L("The pyramid has the same base and height as the cube, so it's one third of the cube. So the pyramid is one "
        "unit, the whole cube is three units, and what's left is two units.", show(f127b['u'], 'the pyramid is one unit')),
      L("What's left is sixty, so two units are sixty. One unit is sixty divided by two, thirty. And the pyramid is one "
        "unit.", show(f127s1, 'two units are sixty'), show(f127s2, 'One unit is sixty divided by two')),
      L("So the pyramid is thirty. Volume ratios really help on the exam. Choice number three is our answer, and I'll "
        "see you in the next question.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-geo35-g128 - the height of a square pyramid
# Hebrew geo 6695-6753 (side root 2, edge 4 -> root 15 there; side 4 root 2, edge 7 -> root 33 here): (1) the math way:
# "honestly it's not clear where to start, the height just hangs there"; connect the foot to a corner: an inner triangle,
# "a principle that keeps coming back"; right-angled because the height is perpendicular to every line on the base; half
# the diagonal from the silver triangles (divide by root 2); not a triple -> full Pythagoras; (2) estimation: the height
# is the shortest way from the top to the base, so it is less than the slanted edge; the anchor root 49 = 7 (hers root
# 16); "possible, not certain yet"; three out -> the fourth. R37: the inner right triangle and the pyramid case are taught
# in geo-120 part 2 (side 8, edge 9 -> 7); here applied slowly with "like in the lesson".
# V3: the copy; the diagonals dashed teal, O, the triangle POB tinted orange, pulled out next to the pyramid with 4, 7, h.
# =================================================================================================================
_A8, _B8, _C8, _D8 = (175.326, 300.668), (362.002, 300.668), (464.674, 235.332), (277.998, 235.332)
_P8, _O8 = (320.0, 78.429), (320.0, 268.0)
f128a = PIN(GEO('f128a', [
    ('line', [qraw('geo35-g128')]),
    ('tri', [('tint', [_P8, _O8, _B8], 'orange'), ('poly', [_P8, _O8, _B8], 'orange', 4), rt(_O8, _P8, _B8, 11, 'orange')]),
    ('diag', [sg(_A8, _C8, 'teal', 3, True), sg(_B8, _D8, 'teal', 3, True), ('txt', 350, 300, '4', 'teal', 28)]),
    ('cut', [('tint', [(540, 80), (540, 290), (620, 290)], 'orange'), ('poly', [(540, 80), (540, 290), (620, 290)], 'orange', 4),
             rt((540, 290), (540, 80), (620, 290), 12, 'orange'), ('txt', 580, 318, '4', 'teal', 28), ('txt', 600, 175, '7', 'orange', 28),
             ('txt', 520, 190, 'h', 'orange', 30, True)]),
    ('ans', [('txt', 492, 230, '√33', 'orange', 26)]),
], vb='140 40 520 300', w=520, title='The pyramid and the triangle inside it'))
f128b = PIN(GEO('f128b', [
    ('line', [qraw('geo35-g128')]),
    ('hp', [sg(_P8, _O8, 'teal', 5), sg(_P8, _B8, 'red', 5), ('txt', 300, 180, 'h', 'teal', 30, True)]),
], vb='140 40 360 300', w=420, title='The height is shorter than the slanted edge'))
for _g in (f128a, f128b): QLEFT(_g, 'geo35-g128')
f128r1 = IH('f128r1', 'diagonal: $4\\sqrt2 \\cdot \\sqrt2 = 4 \\cdot 2 = 8$', size=30)
f128r2 = IH('f128r2', '$OB = 8 \\div 2 = 4$', size=30)
f128r3 = IH('f128r3', '$h^2 + 4^2 = 7^2$', size=30)
f128r4 = IH('f128r4', '$h^2 = 49 - 16 = 33$', size=30)
f128r5 = IH('f128r5', '$h = \\sqrt{33}$', size=30)
f128s1 = IH('f128s1', '$h < 7 = \\sqrt{49}$', size=28)
f128s2 = IH('f128s2', '(1) $7\\sqrt2 > 7$, no', size=28)
f128s3 = IH('f128s3', '(2) $\\sqrt{33} < \\sqrt{49}$, possible', size=28)
f128s4 = IH('f128s4', '(3) $\\sqrt{65} > \\sqrt{49}$, no', size=28)
f128s5 = IH('f128s5', '(4) $5\\sqrt2 = \\sqrt{50} > \\sqrt{49}$, no', size=28)
FLOW([f128r1, f128r2, f128r3, f128r4, f128r5], QC('geo35-g128'))
FLOW([f128s1, f128s2, f128s3, f128s4, f128s5], QC('geo35-g128'))
NOFIG('solve-geo35-g128', 0, 1)

video('solve-geo35-g128', 'solution', qid='geo35-g128', slides=[
    SM('Method 1 · The math way: Pythagoras', 'A triangle inside',
      L("A pyramid has a square base with side four root two. Each slanted edge is seven. What is the height of the "
        "pyramid?", pt('stem', 'A pyramid has a square base', 'hl', 7.0), show(f128a['line'], 'A pyramid has a square base'),
        voice='calm', pause=0.5),
      L("We'll solve it in two different ways, the math way, and then with an estimate. Let's start with the math way."),
      L("We want the height, so let's call it h. Honestly, at first it's not clear where to start. The height just "
        "hangs there in the middle. What's given? The slanted edge, seven."),
      L("So, like in the lesson, we build a triangle inside the pyramid. We join the foot of the height, O, to the "
        "corner B. Now P O B is a triangle.", show(f128a['tri'], 'Now P O B is a triangle')),
      L("It's a right triangle. Why? The height stands straight on the base, so it makes a right angle with every line "
        "on the base from its foot. O B is such a line."),
      L("The hypotenuse is the edge, seven. We need the other leg, O B. All four slanted edges are equal, so the height "
        "meets the square at its center, where the diagonals meet. So O B is half of a diagonal.", show(f128a['diag'], 'where the diagonals meet')),
      L("Remember the silver triangle. The diagonal of a square is the side times root two. Four root two times root "
        "two is four times two, eight. Half of it is four. So O B is four.", show(f128r1, 'Four root two times root two'),
        show(f128r2, 'Half of it is four')),
      L("Let's pull the triangle out. A leg of four and a hypotenuse of seven. That's not a triple we know, so we use "
        "Pythagoras. h squared plus four squared is seven squared.", show(f128a['cut'], "Let's pull the triangle out"),
        show(f128r3, 'h squared plus four squared')),
      L("So h squared is forty-nine minus sixteen, thirty-three. Thirty-three has no whole root, so h is root "
        "thirty-three. Choice number two is our answer.", show(f128r4, 'forty-nine minus sixteen'),
        show(f128r5, 'so h is root'), show(f128a['ans'], 'so h is root'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · Estimation', 'Shorter than the edge',
      L("Now let's estimate. The slanted edge is seven. Must the height be less than seven?", show(f128b['line'], "Now let's estimate")),
      L("Yes. The height is the shortest way from the top point down to the base. The edge is slanted, so it's longer. "
        "So the height is less than seven.", show(f128b['hp'], 'The edge is slanted')),
      L("Our anchor is root forty-nine, which is exactly seven. So the height is less than root forty-nine.",
        show(f128s1, 'Our anchor is root forty-nine')),
      L("Choice number one, seven root two. Root two is more than one, so this is more than seven. Out.",
        show(f128s2, 'seven root two'), mk('cross', 'choice 1', 'Out.')),
      L("Choice number two, root thirty-three. It's less than root forty-nine. So it's possible. Not certain yet, but "
        "possible, so we keep it.", show(f128s3, 'root thirty-three')),
      L("Choice number three, root sixty-five. It's more than root forty-nine, more than seven. Out.",
        show(f128s4, 'root sixty-five'), mk('cross', 'choice 3', 'more than seven. Out.')),
      L("Choice number four, five root two. Let's put the five under the root. Five squared is twenty-five, times two is "
        "fifty. Root fifty is just above root forty-nine, so it's out.", show(f128s5, 'Five squared is twenty-five'),
        mk('cross', 'choice 4', "so it's out")),
      L("Three choices are out, so only one choice remains. Choice number two is our answer, and I'll see you in the next "
        "question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# r26-t35-cones (lesson) - REMOVED 2026-10-23 (Nitzan's decision: "no"). The lesson (solids made by turning, and a
# slant-height reminder) is out of the course: t35.py drop_cones_t35() unplaces it, and this spec no longer writes its
# script. The slant height is taught in geo-120 part 2 (r 5, slant 13 -> h 12), which solve-q-r26-t35-02 links to.
# Turning a shape stays only in practice geo35-core-p01 (p21 was already out), whose written explanation teaches it.


# =================================================================================================================
# solve-q-r26-t35-02 - a cone with radius 6 and slant height 10
# No Hebrew source (added question). R37: the cone's right triangle is taught in geo-120 part 2 (5, 13 -> 12); here
# applied with "like in the lesson". The traps 120 pi (10 as the height), 288 pi (no division by 3) and 360 pi (both)
# at their steps.
# V3: the copy, the triangle tinted and pulled out with 6, 10, 8.
# =================================================================================================================
f02a = PIN(GEO('f02a', [
    ('line', [qraw('q-r26-t35-02')]),
    ('tri', [('tint', [(320, 80), (320, 280), (425, 280)], 'teal'), ('poly', [(320, 80), (320, 280), (425, 280)], 'teal', 4)]),
    ('cut', [('tint', [(500, 80), (500, 280), (580, 280)], 'teal'), ('poly', [(500, 80), (500, 280), (580, 280)], 'teal', 4),
             rt((500, 280), (500, 80), (580, 280), 12, 'teal'), ('txt', 540, 306, '6', 'teal', 28), ('txt', 562, 170, '10', 'teal', 28),
             ('txt', 480, 180, 'h', 'orange', 30, True)]),
    ('h', [('txt', 476, 225, '8', 'orange', 30)]),
], vb='190 50 420 290', w=500, title='The cone and its right triangle'))
QLEFT(f02a, 'q-r26-t35-02')
f02r1 = IH('f02r1', '$6, 10 = 2 \\cdot (3, 5)$', size=30)
f02r2 = IH('f02r2', '$h = 2 \\cdot 4 = 8$', size=30)
f02r3 = IH('f02r3', '$\\frac{π \\cdot 6^2 \\cdot 8}{3}$', size=30)
f02r4 = IH('f02r4', '$36 \\div 3 = 12$, $\\ 12 \\cdot 8 = 96$', size=30)
f02r5 = IH('f02r5', '$96π$', size=30)
FLOW([f02r1, f02r2, f02r3, f02r4, f02r5], QC('q-r26-t35-02'))
NOFIG('solve-q-r26-t35-02', 0)

video('solve-q-r26-t35-02', 'solution', qid='q-r26-t35-02', slides=[
    SM('Method 1 · The math way: Pythagoras', 'Find the height first',
      L("A cone has a base radius of six and a slant height of ten. What is its volume?",
        pt('stem', 'A cone has a base radius of six', 'hl', 6.0), show(f02a['line'], 'A cone has a base radius'), voice='calm', pause=0.5),
      L("The volume of a cone is pi r squared, times the height, divided by three. We have the radius, six. But we "
        "don't have the height yet."),
      L("Careful, ten is not the height. It's the slant height, the line along the outside. Like in the lesson, the "
        "height, the radius and the slant height make a right triangle.", show(f02a['tri'], 'make a right triangle')),
      L("Let's pull it out. The slant height, ten, is the hypotenuse, and the radius, six, is a leg.",
        show(f02a['cut'], "Let's pull it out")),
      L("Six and ten are two times three and two times five. So it's the triple three, four, five, times two. The "
        "height is two times four, eight.", show(f02r1, 'two times three and two times five'), show(f02r2, 'The height is two times four'),
        show(f02a['h'], 'eight.')),
      L("Now the volume. Pi times six squared, times eight, divided by three.", show(f02r3, 'Pi times six squared')),
      L("Six squared is thirty-six, and thirty-six divided by three is twelve. Twelve times eight is ninety-six. So the "
        "volume is ninety-six pi.", show(f02r4, 'thirty-six divided by three is twelve'), show(f02r5, 'So the volume is')),
      L("Look at the traps. If we use ten as the height, we get one hundred twenty pi, choice number one. If we forget "
        "to divide by three, we get two hundred eighty-eight pi, choice number three.",
        mk('cross', 'choice 1', 'choice number one'), mk('cross', 'choice 3', 'choice number three')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# solve-geo35-g129 - the triangle BDG in a cube
# Hebrew geo 6755-6829 (edge root 2 there -> root 3; edge 4 root 2 here -> 16 root 3): (1) the full math: the base BD = a
# face diagonal (silver triangle, times root 2), the height from G through an inner right triangle (the edge stands on the
# base, so it is perpendicular to every line on it; the diagonals halve each other); not golden, not silver, not a triple
# -> full Pythagoras; (2) the flash: three face diagonals of equal squares -> equilateral -> side squared root 3 over 4;
# then "I want to use this question" - three angle situations in a cube: edge and the diagonal of the face it stands on
# 90, edge and a diagonal of the same face 45, two face diagonals from one corner 60 ("always, always, always"; connect
# the third diagonal). Kept from the English: the warning that the 90 needs one shared corner and the edge standing on
# that face. R37: inner right triangles and the face diagonal are geo-120 part 2 (reminders); the three angles are taught
# here (one question each on the real exam: 2025 autumn q2_14 = 90, 2022 winter q2_20 = 60).
# V3: the copy; BD teal with 8, M the middle, the triangle GCM tinted and pulled out; the three sides of BDG teal; the
# three angle situations on three small cubes.
# =================================================================================================================
_A9, _B9, _C9, _D9 = (207.785, 277.736), (352.579, 277.736), (432.215, 227.058), (287.421, 227.058)
_E9, _F9, _G9, _H9 = (207.785, 132.942), (352.579, 132.942), (432.215, 82.264), (287.421, 82.264)
_M9 = ((_B9[0] + _D9[0]) / 2.0, (_B9[1] + _D9[1]) / 2.0)
f129a = PIN(GEO('f129a', [
    ('line', [qraw('geo35-g129')]),
    ('bd', [sg(_B9, _D9, 'teal', 6), ('txt', 300, 268, '8', 'teal', 28)]),
    ('gm', [sg(_A9, _C9, 'teal', 2.5, True), ('dot', *_M9), sg(_G9, _M9, 'orange', 4, True), ('txt', _M9[0] - 4, _M9[1] + 22, 'M', 'ink', 24, True)]),
    ('tri', [('tint', [_G9, _C9, _M9], 'orange'), sg(_C9, _M9, 'orange', 4), sg(_G9, _C9, 'orange', 5), rt(_C9, _G9, _M9, 10, 'orange')]),
    ('cut', [('tint', [(500, 70), (500, 280), (590, 280)], 'orange'), ('poly', [(500, 70), (500, 280), (590, 280)], 'orange', 4),
             rt((500, 280), (500, 70), (590, 280), 12, 'orange'), ('txt', 545, 306, '4', 'orange', 28), ('txt', 470, 175, '4√2', 'orange', 26)]),
    ('ans', [('txt', 580, 160, '4√3', 'orange', 28)]),
], vb='170 40 450 290', w=520, title='The cube and the height of triangle BDG'))
f129b = PIN(GEO('f129b', [
    ('line', [qraw('geo35-g129')]),
    ('eq', [('poly', [_B9, _D9, _G9], 'teal', 6), ('txt', 300, 268, '8', 'teal', 26), ('txt', 345, 140, '8', 'teal', 26), ('txt', 410, 180, '8', 'teal', 26)]),
], vb='170 40 300 290', w=420, title='Three equal face diagonals'))
_cA = boxpts(40, 300, 110, 110, 110); _cB = boxpts(250, 300, 110, 110, 110); _cC = boxpts(460, 300, 110, 110, 110)
f129c = PIN(GEO('f129c', [
    ('line', box_el(_cA) + box_el(_cB) + box_el(_cC)),
    ('a90', [sg(_cA['A'], _cA['E'], 'teal', 6), sg(_cA['A'], _cA['C'], 'orange', 5, True), rt(_cA['A'], _cA['E'], _cA['C'], 12, 'teal'),
             ('txt', 100, 330, '90°', 'teal', 28)]),
    ('a45', [sg(_cB['A'], _cB['B'], 'teal', 6), sg(_cB['A'], _cB['F'], 'orange', 5), ang(_cB['A'], _cB['B'], _cB['F'], 34, 'orange'),
             ('txt', 310, 330, '45°', 'orange', 28)]),
    ('a60', [('poly', [_cC['A'], _cC['F'], _cC['C']], 'teal', 5), ang(_cC['F'], _cC['A'], _cC['C'], 28, 'teal'),
             ('txt', 520, 330, '60°', 'teal', 28)]),
], vb='20 60 640 290', w=620, title='Three angles in a cube'))
for _g in (f129a, f129b): QLEFT(_g, 'geo35-g129')
QLEFT(f129c, 'geo35-g129', w=1000)
f129r1 = IH('f129r1', '$BD = 4\\sqrt2 \\cdot \\sqrt2 = 8$', size=28)
f129r2 = IH('f129r2', '$CM = 8 \\div 2 = 4$', size=28)
f129r3 = IH('f129r3', '$GM^2 = 4^2 + (4\\sqrt2)^2$', size=28)
f129r3b = IH('f129r3b', '$= 16 + 32 = 48$', size=28)
f129r4 = IH('f129r4', '$GM = \\sqrt{48} = 4\\sqrt3$', size=28)
f129r5 = IH('f129r5', '$\\frac{8 \\cdot 4\\sqrt3}{2} = 16\\sqrt3$', size=28)
f129s1 = IH('f129s1', '$BD = DG = GB = 8$', size=30)
f129s2 = IH('f129s2', '$\\frac{8^2\\sqrt3}{4} = \\frac{64\\sqrt3}{4} = 16\\sqrt3$', size=30)
FLOW([f129r1, f129r2, f129r3, f129r3b, f129r4, f129r5], QC('geo35-g129'))
FLOW([f129s1, f129s2], QC('geo35-g129'))
NOFIG('solve-geo35-g129', 0, 1, 2)

video('solve-geo35-g129', 'solution', qid='geo35-g129', slides=[
    SM('Method 1 · The math way: area formulas', 'Base and height',
      L("The edge of cube A B C D E F G H is four root two. What is the area of triangle B D G?",
        pt('stem', 'The edge of cube', 'hl', 6.0), show(f129a['line'], 'The edge of cube'), voice='calm', pause=0.5),
      L("A triangle inside a cube again. We'll solve it in two different ways, the math way, and then with an insight."),
      L("Let's start with the math way. The area of a triangle is a base times its height, divided by two. Let's take "
        "B D as the base."),
      L("B D is a diagonal of the bottom face, a square. Like in the lesson, a face diagonal is the edge times root two. "
        "Four root two times root two is four times two, eight.", show(f129a['bd'], 'B D is a diagonal of the bottom face'),
        show(f129r1, 'Four root two times root two')),
      L("Now the height from G down to B D. G B and G D are diagonals of two equal squares, so they're equal. "
        "Triangle B D G is isosceles. Its height is also a median, so it meets B D at its middle. "
        "Call it M. It's the middle of the bottom face.", show(f129a['gm'], 'Call it M')),
      L("Look at triangle G C M. The edge C G stands on the bottom face, so it makes a right angle with C M.",
        show(f129a['tri'], 'Look at triangle G C M')),
      L("C M is half of the other diagonal, A C. The diagonals of a square are equal and halve each other. So C M is "
        "eight divided by two, four.", show(f129r2, 'eight divided by two')),
      L("Let's pull the triangle out. The legs are four and four root two. That's not a triple, so full Pythagoras. Four "
        "squared is sixteen, and the square of four root two is thirty-two. Together, forty-eight.", show(f129a['cut'], "Let's pull the triangle out"),
        show(f129r3, 'full Pythagoras'), show(f129r3b, 'Four squared is sixteen')),
      L("Root forty-eight is root sixteen times root three, four root three. That's the height.",
        show(f129r4, 'Root forty-eight is'), show(f129a['ans'], "That's the height")),
      L("So the area is eight times four root three, divided by two, sixteen root three. Choice number three is our "
        "answer.", show(f129r5, 'So the area is eight times'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Insight: equilateral', 'An equilateral triangle',
      L("Now the insight. Some students look at triangle B D G and see that it's equilateral. Why?", show(f129b['line'], 'Now the insight')),
      L("B D is a diagonal of the bottom face. D G is a diagonal of the back face. And G B is a diagonal of the right "
        "face. All the faces are equal squares, so all their diagonals are equal. Each one is eight.",
        show(f129b['eq'], 'B D is a diagonal of the bottom face'), show(f129s1, 'Each one is eight')),
      L("Remember the area of an equilateral triangle. The side squared, times root three, divided by four. Eight "
        "squared is sixty-four, and sixty-four divided by four is sixteen. So it's sixteen root three.",
        show(f129s2, 'Eight squared is sixty-four')),
      L("Choice number three again, and much shorter.", mk('tick', 'choice 3', 'Choice number three again'))),
    S('Three angles in a cube',
      L("I want to use this question to show you three angles in a cube. They come up on the exam.", show(f129c['line'], 'three angles in a cube')),
      L("The first one is an edge, and a diagonal of the face that the edge stands on, from the same corner. The edge is "
        "perpendicular to that whole face, so the angle is ninety.", show(f129c['a90'], 'an edge, and a diagonal of the face')),
      L("Careful, they must meet at one corner, and the edge must stand on that face. Otherwise the angle is "
        "different."),
      L("The second one is an edge and a diagonal on the same face. That's the diagonal of a square with its side, so the angle is "
        "forty-five.", show(f129c['a45'], 'an edge and a diagonal on the same face')),
      L("The third one is two face diagonals that start at the same corner. The angle between them is always sixty. Why? Join "
        "their ends with the third diagonal. All three are equal, so it's an equilateral triangle, just like B D G.",
        show(f129c['a60'], 'two face diagonals that start at the same corner')),
      L("So ninety, forty-five and sixty. And I'll see you in the next question.")),
])


# =================================================================================================================
# solve-geo35-g130 - the perimeter of triangle AEG in a cube
# Hebrew geo 6831-6913 (edge 1 there; edge 3 here): an edge, a face diagonal (times root 2), the angle AEG = 90 (the
# situation of the last question), Pythagoras -> root 3; then she widens: the body diagonal is always the edge times
# root 3 ("a square root 2, a 3D square root 3"), the exam example (edge 5 there; 8 in the English), back from the
# diagonal: divide by root 3 with her trick "drop the root, divide, put the root back" (12 -> 4 root 3 there; 27 -> 9
# root 3 here), and the box (two right triangles; the lesson geo-120 part 2 teaches it with 2 x 3 x 6, so here a one-line
# reminder). R37: the face and body diagonals are taught in geo-120 part 2; here the math way applies the triangles, the
# second way uses the rule from the lesson, and the backwards trick is taught here with its why (root 2 too).
# V3: the copy; AE, EG with the right angle, AG orange; the values written on the sides as found.
# =================================================================================================================
_A0, _E0, _G0 = (207.785, 277.736), (207.785, 132.942), (432.215, 82.264)
f130a = PIN(GEO('f130a', [
    ('line', [qraw('geo35-g130')]),
    ('ae', [sg(_A0, _E0, 'teal', 6), ('txt', 188, 205, '3', 'teal', 28)]),
    ('eg', [sg(_E0, _G0, 'teal', 6), ('txt', 320, 92, '3√2', 'teal', 26)]),
    ('right', [rt(_E0, _A0, _G0, 14, 'teal')]),
    ('ag', [sg(_A0, _G0, 'orange', 6), ('txt', 345, 205, '3√3', 'orange', 28)]),
], vb='160 40 320 290', w=440, title='Triangle AEG in the cube'))
f130b = PIN(GEO('f130b', [
    ('line', [qraw('geo35-g130')]),
    ('d', [sg(_E0, _G0, 'teal', 6), ('txt', 320, 92, '3√2', 'teal', 26), sg(_A0, _G0, 'orange', 6), ('txt', 345, 205, '3√3', 'orange', 28)]),
], vb='160 40 320 290', w=440, title='The two diagonals by the rule'))
for _g in (f130a, f130b): QLEFT(_g, 'geo35-g130')
f130r1 = IH('f130r1', '$AE = 3$', size=30)
f130r2 = IH('f130r2', '$EG = 3\\sqrt2$', size=30)
f130r3 = IH('f130r3', '$AG^2 = 3^2 + (3\\sqrt2)^2$', size=30)
f130r3b = IH('f130r3b', '$= 9 + 18 = 27$', size=30)
f130r4 = IH('f130r4', '$AG = \\sqrt{27} = 3\\sqrt3$', size=30)
f130r5 = IH('f130r5', '$3 + 3\\sqrt2 + 3\\sqrt3$', size=30)
f130s1 = IH('f130s1', 'face: $3\\sqrt2$, $\\ $ body: $3\\sqrt3$', size=30)
f130s2 = IH('f130s2', 'edge $8$: body $8\\sqrt3$', size=30)
f130s3 = IH('f130s3', '$\\frac{27}{\\sqrt3}$: $\\ 27 \\div 3 = 9$, so $9\\sqrt3$', size=30)
f130s4 = IH('f130s4', '$\\frac{27}{\\sqrt3} \\cdot \\frac{\\sqrt3}{\\sqrt3} = \\frac{27\\sqrt3}{3} = 9\\sqrt3$', size=30)
f130s5 = IH('f130s5', '$\\frac{14}{\\sqrt2} = 7\\sqrt2$', size=30)
FLOW([f130r1, f130r2, f130r3, f130r3b, f130r4, f130r5], QC('geo35-g130'))
FLOW([f130s1, f130s2], QC('geo35-g130'))
NOFIG('solve-geo35-g130', 0, 1, 2)
p130c = [I('p130c0', 'body diagonal $27$: edge $= \\frac{27}{\\sqrt3}$', size=32), f130s3, f130s4, f130s5]
FLOW(p130c, QW('geo35-g130'))

video('solve-geo35-g130', 'solution', qid='geo35-g130', slides=[
    SM('Method 1 · The math way: Pythagoras', 'Three kinds of segment',
      L("The edge of cube A B C D E F G H is three. What is the perimeter of triangle A E G?",
        pt('stem', 'The edge of cube', 'hl', 6.0), show(f130a['line'], 'The edge of cube'), voice='calm', pause=0.5),
      L("For the perimeter we need all three sides. Each side is a different kind of segment in the cube. We'll solve "
        "it in two different ways."),
      L("Let's start with the math way. A E is an edge, so it's three.", show(f130a['ae'], 'A E is an edge'), show(f130r1, "so it's three")),
      L("E G is a diagonal of the top face, a square with side three. A face diagonal is the edge times root two, so "
        "it's three root two.", show(f130a['eg'], 'E G is a diagonal of the top face'), show(f130r2, "it's three root two")),
      L("And A G goes through the inside of the cube. What's the angle at E? Like in the last question, the edge A E "
        "stands on the top face, and E G is a diagonal of that face, from the same corner. So it's ninety.",
        show(f130a['right'], "So it's ninety")),
      L("So A E G is a right triangle with legs three and three root two. Three squared is nine. The square of three root "
        "two is nine times two, eighteen. Together, twenty-seven.", show(f130r3, 'a right triangle with legs'), show(f130r3b, 'Three squared is nine')),
      L("Root twenty-seven is root nine times root three, three root three.", show(f130r4, 'Root twenty-seven is'),
        show(f130a['ag'], 'three root three.')),
      L("So the perimeter is three, plus three root two, plus three root three. Choice number four is our answer.",
        show(f130r5, 'So the perimeter is'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    SM('Method 2 · The math way: the diagonals', 'Use the rule',
      L("Now a second, shorter way, with the rule from the lesson. In every cube, the face diagonal is the edge times "
        "root two, and the body diagonal is the edge times root three.", show(f130b['line'], 'Now a second, shorter way')),
      L("E G is a face diagonal, so it's three root two. A G is the body diagonal, so it's three root three. We "
        "don't need any triangles here.", show(f130b['d'], 'E G is a face diagonal'), show(f130s1, 'A G is the body diagonal')),
      L("So again, three plus three root two plus three root three. Choice number four.",
        mk('tick', 'choice 4', 'Choice number four.')),
      L("A question like this was on the exam. A cube has edge eight. What's its body diagonal? Eight root three, at "
        "once.", show(f130s2, 'eight root three'))),
    S('Back from the diagonal',
      L("And the other way round. Say the body diagonal is twenty-seven. What's the edge? The diagonal is the edge times "
        "root three. So the edge is twenty-seven divided by root three.", show(p130c[0], 'Say the body diagonal is twenty-seven')),
      L("Here's a quick way. Ignore the root for a moment. Twenty-seven divided by three is nine. Now put the root back. "
        "So the edge is nine root three.", show(f130s3, 'Ignore the root for a moment')),
      L("Why does it work? Multiply the top and the bottom by root three. On the bottom, root three times root three is "
        "three. So it's twenty-seven root three over three, and twenty-seven over three is nine.",
        show(f130s4, 'Multiply the top and the bottom')),
      L("The same with root two. If a face diagonal is fourteen, the edge is fourteen over root two. Fourteen divided by "
        "two is seven, so it's seven root two.", show(f130s5, 'Fourteen divided by two is seven')),
      L("And in a box, the edges aren't equal, so there's no fixed ratio. Like in the lesson, we use two right "
        "triangles. And I'll see you in the next question.")),
])


# =================================================================================================================
# solve-geo35-g131 - how many cubes fit in a box
# Hebrew geo 6916-6969 (edge 2 into 6 x 4 x 5 there -> 12; edge 4 into 18 x 9 x 11 here -> 16): first ask, liquid or
# solid? a liquid spreads evenly and leaves no empty space; solids can fit exactly (small cubes in a cube) or leave gaps
# (only some fit in a crate); she DRAWS the packing: a floor (3 along, 2 deep there; 4 along, 2 deep here), a second
# floor, a third floor won't close the lid; then the exam way: how many times the edge goes into each dimension, ignore
# the remainder, multiply; "if you know these questions, they're simpler than their place". RESTORED (checklist): her
# drawn floor-by-floor packing, as its own step before the exam way. Kept from the English: the trap 27 (dividing the
# volumes, as if the cubes were water) at its step, without the long division (R36).
# V3: the copy of the box; the cubes of the first floor built in it, the leftover gaps orange, the second floor, the
# third floor red and sticking out; the exam way in rows.
# =================================================================================================================
_kx1, _ky1 = 36.4 / 66.0, 22.75 / 66.0
_fl1 = [(i, 0, k) for i in range(4) for k in range(2)]
_fl2 = [(i, 1, k) for i in range(4) for k in range(2)]
f131a = PIN(GEO('f131a', [
    ('line', [qraw('geo35-g131')]),
    ('floor', unit_cubes(_fl1, 130.556, 312, 66, _kx1, _ky1, fills={c: (GBAND, '#bfe6e0', '#a8dcd4') for c in _fl1})),
    ('gap', [('tint', [(394.556, 312), (427.556, 312), (427.556, 130.5), (394.556, 130.5)], 'orange'), ('txt', 411, 345, '2', 'orange', 24)]),
    ('second', unit_cubes(_fl2, 130.556, 312, 66, _kx1, _ky1, fills={c: (GBAND, '#bfe6e0', '#a8dcd4') for c in _fl2})),
    ('third', [('poly', cube_face(0, 2, 0, 'front', 130.556, 312, 66, _kx1, _ky1), 'red', 4, True),
               ('poly', cube_face(1, 2, 0, 'front', 130.556, 312, 66, _kx1, _ky1), 'red', 4, True),
               ('txt', 300, 70, 'no room', 'red', 26)]),
], vb='100 30 460 330', w=500, title='Cubes with edge 4 in the box, floor by floor'))
QLEFT(f131a, 'geo35-g131')
f131r1 = IH('f131r1', 'along 18: $4 \\cdot 4 = 16$, $\\ 2$ left', size=30)
f131r2 = IH('f131r2', 'along 9: $2 \\cdot 4 = 8$, $\\ 1$ left', size=30)
f131r3 = IH('f131r3', 'one floor: $4 \\cdot 2 = 8$ cubes', size=30)
f131r4 = IH('f131r4', 'two floors: $8$ high, $\\ 3$ left', size=30)
f131r5 = IH('f131r5', '$8 + 8 = 16$', size=30)
f131s1 = IH('f131s1', '$18 \\div 4 = 4$, remainder $2$', size=30)
f131s2 = IH('f131s2', '$9 \\div 4 = 2$, remainder $1$', size=30)
f131s3 = IH('f131s3', '$11 \\div 4 = 2$, remainder $3$', size=30)
f131s4 = IH('f131s4', '$4 \\cdot 2 \\cdot 2 = 16$', size=30)
FLOW([f131r1, f131r2, f131r3, f131r4, f131r5], QC('geo35-g131'))
FLOW([f131s1, f131s2, f131s3, f131s4], QC('geo35-g131'))
NOFIG('solve-geo35-g131', 0, 1, 2)
f131b = PIN(GEO('f131b', [('line', [qraw('geo35-g131')])], vb='100 30 460 330', w=500, title='The box'))
f131c = PIN(GEO('f131c', [('line', [qraw('geo35-g131')])], vb='100 30 460 330', w=500, title='The box'))
for _g in (f131b, f131c): QLEFT(_g, 'geo35-g131')

video('solve-geo35-g131', 'solution', qid='geo35-g131', slides=[
    S('Liquid or solid?',
      L("Identical cubes with edge four are placed in a box, eighteen by nine by eleven. The cube edges must be parallel "
        "to the box edges. What is the greatest number of cubes that can fit entirely inside the box?",
        pt('stem', 'Identical cubes with edge four', 'hl', 11.0), show(f131b['line'], 'Identical cubes with edge four'), voice='calm', pause=0.5),
      L("In these questions, we first ask one thing. Do we fill the box with a liquid, or with solids?"),
      L("Liquid can spread into small gaps. If we fill a container with liquid, we can use its whole volume."),
      L("Solids are different. Sometimes they fit exactly. Small cubes with edge three fill a cube with edge six "
        "exactly, two in each direction, eight cubes. But often the box isn't a whole number of cubes long, and a gap "
        "is left."),
      L("Here we put cubes into a box, a solid into a solid. So we can't just divide the volumes.")),
    SM('Method 1 · The math way: floor by floor', 'Draw the floors',
      L("Let's start by drawing it, floor by floor. Along the length, eighteen, how many cubes with edge four fit? Four "
        "cubes take four times four, sixteen. A fifth one would need twenty. So four fit, and two centimeters are left.",
        show(f131a['line'], "Let's start by drawing it"), show(f131r1, 'Four cubes take four times four'),
        show(f131a['gap'], 'two centimeters are left')),
      L("Along the width, nine, two cubes take eight, and one centimeter is left. So two fit.", show(f131r2, 'two cubes take eight')),
      L("So the bottom floor has four rows of two, eight cubes.", show(f131a['floor'], 'So the bottom floor'), show(f131r3, 'eight cubes')),
      L("Now the height, eleven. One floor is four high. Two floors are eight high, so a second floor fits, and three "
        "centimeters are left.", show(f131a['second'], 'a second floor fits'), show(f131r4, 'Two floors are eight high')),
      L("A third floor would need twelve, and we only have eleven. So the third floor doesn't fit. We can't close the "
        "lid.", show(f131a['third'], 'A third floor would need twelve')),
      L("So two floors of eight, sixteen cubes.", show(f131r5, 'So two floors of eight'), pt('choice 2', 'sixteen cubes'))),
    SM('Method 2 · The math way: each direction', 'The exam way',
      L("On the exam there's no time to draw. So we do the same thing with the numbers. How many times does four go into "
        "each length?", show(f131c['line'], "On the exam there's no time to draw")),
      L("Four goes into eighteen four whole times, with two left over. We ignore the remainder.", show(f131s1, 'Four goes into eighteen')),
      L("Four goes into nine twice, with one left over. And four goes into eleven twice, with three left over. We "
        "ignore those too.", show(f131s2, 'Four goes into nine twice'), show(f131s3, 'four goes into eleven twice')),
      L("Now we multiply. Four times two times two is sixteen.", show(f131s4, 'Four times two times two')),
      L("And the trap? Twenty-seven, choice number four, is what we'd get by dividing the volumes and keeping only the whole number, as if the cubes were "
        "water and could fill the gaps. Solids in a box aren't water.", mk('cross', 'choice 4', 'Twenty-seven, choice number four')),
      L("These questions look hard because of their place in the section, but they're simple once you know them. "
        "Choice number two is our answer, and I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# solve-geo35-g132 - remove a corner cube (a "Rubik's cube" question)
# Hebrew geo 6972-7025 (8 cubes of edge 1 there; 27 cubes of edge 4 here): "we call these Rubik's cube questions, the idea
# comes back quite a lot"; volume: one cube less, it drops; surface: the corner cube gave 3 faces, but 3 faces it hid
# appear -> unchanged; then three situations: a corner (0), the middle of an edge (shows 2, 4 appear: +2), the centre of
# a face (shows 1, 5 appear: +4); "lost + gained always completes 6". External finding (Codex final 2.3): the corner and
# the face-centre removal with BEFORE / AFTER pictures - "removing a cube adds four" is NOT a general rule; it depends on
# where the cube is. R37: "a contact hides two faces" is geo-120 part 3 (reminder); the three places are taught here.
# V3: the copy (the corner cube grey); the three faces it shows tinted orange, the three hidden ones that appear teal on
# an "after" picture; then three cubes before (the removed cube orange) and after (the new faces teal).
# =================================================================================================================
_ALL = [(i, j, k) for i in range(3) for j in range(3) for k in range(3)]
_sq = 54
_cn = (2, 2, 0)
f132a = PIN(GEO('f132a', [
    ('line', [qraw('geo35-g132')]),
    ('three', [('tint', [(302.587, 127.761), (356.165, 127.761), (385.633, 109.009), (332.055, 109.009)], 'orange'),
               ('tint', [(356.165, 181.339), (385.633, 162.587), (385.633, 109.009), (356.165, 127.761)], 'orange'),
               ('tint', [(302.587, 181.339), (356.165, 181.339), (356.165, 127.761), (302.587, 127.761)], 'orange'),
               ('txt', 520, 120, 'shows 3 faces', 'orange', 24)]),
], vb='170 50 480 260', w=480, title='The corner cube shows three faces'))
f132b = PIN(GEO('f132b', [
    ('line', unit_cubes([c for c in _ALL if c != _cn], 120, 300, _sq) + [('txt', 360, 330, 'after', 'ink', 24)]),
    ('new', [('tint', cube_face(1, 2, 0, 'right', 120, 300, _sq), 'teal'), ('tint', cube_face(2, 1, 0, 'top', 120, 300, _sq), 'teal'),
             ('tint', cube_face(2, 2, 1, 'front', 120, 300, _sq), 'teal'), ('txt', 400, 90, '3 new faces', 'teal', 24)]),
], vb='90 40 420 310', w=420, title='After: three hidden faces appear'))
LEFT(f132a, y=QTOP('geo35-g132'), x=410, w=330); LEFT(f132b, y=QTOP('geo35-g132'), x=750, w=250)
f132r1 = IH('f132r1', 'one cube: $4 \\cdot 4 \\cdot 4 = 64$', size=30)
f132r2 = IH('f132r2', 'one face: $4 \\cdot 4 = 16$', size=30)
f132r3 = IH('f132r3', 'lost $3$, gained $3$: no change', size=30)
FLOW([f132r1, f132r2, f132r3], [(1020, 570, QTOP('geo35-g132') + 5, QBOT('geo35-g132'))])
_s3 = 30
_pos = {'corner': (2, 2, 0), 'edge': (1, 2, 0), 'face': (1, 1, 0)}
_xs = {'corner': 40, 'edge': 230, 'face': 420}
_newf = {'corner': [(1, 2, 0, 'right'), (2, 1, 0, 'top'), (2, 2, 1, 'front')],
         'edge': [(0, 2, 0, 'right'), (1, 1, 0, 'top'), (1, 2, 1, 'front')],
         'face': [(0, 1, 0, 'right'), (1, 0, 0, 'top'), (1, 1, 1, 'front')]}
_bef = []; _aft = []; _aftn = []
for _nm_, _c in _pos.items():
    _x = _xs[_nm_]
    _bef += unit_cubes(_ALL, _x, 150, _s3, fills={_c: ('#f3d3a8', '#f3d3a8', '#e9bd86')})
    _aft += unit_cubes([c for c in _ALL if c != _c], _x, 320, _s3)
    _aftn += [('tint', cube_face(i, j, k, f, _x, 320, _s3), 'teal') for (i, j, k, f) in _newf[_nm_]]
f132c = PIN(GEO('f132c', [
    ('line', _bef + [('txt', 85, 175, 'a corner', 'ink', 22), ('txt', 275, 175, 'middle of an edge', 'ink', 20),
                     ('txt', 465, 175, 'middle of a face', 'ink', 20)]),
    ('corner', unit_cubes([c for c in _ALL if c != _pos['corner']], 40, 320, _s3) + _aftn[0:3] + [('txt', 85, 345, '−3 +3 = 0', 'teal', 22)]),
    ('edge', unit_cubes([c for c in _ALL if c != _pos['edge']], 230, 320, _s3) + _aftn[3:6] + [('txt', 275, 345, '−2 +4 = +2', 'teal', 22)]),
    ('face', unit_cubes([c for c in _ALL if c != _pos['face']], 420, 320, _s3) + _aftn[6:9] + [('txt', 465, 345, '−1 +5 = +4', 'teal', 22)]),
], vb='20 20 560 340', w=560, title='Three places: before and after'))
QLEFT(f132c, 'geo35-g132')
f132s1 = IH('f132s1', 'corner: $-3 + 3 = 0$', size=30)
f132s2 = IH('f132s2', 'edge: $-2 + 4 = +2$, $\\ +32$', size=30)
f132s3 = IH('f132s3', 'face: $-1 + 5 = +4$, $\\ +64$', size=30)
f132s4 = IH('f132s4', 'lost $+$ gained $= 6$', size=30)
FLOW([f132s1, f132s2, f132s3, f132s4], [(900, 690, QTOP('geo35-g132') + 5, QBOT('geo35-g132'))])
NOFIG('solve-geo35-g132', 0, 1)

video('solve-geo35-g132', 'solution', qid='geo35-g132', slides=[
    SM('Method 1 · Understanding', 'Volume, then surface',
      L("Twenty-seven identical cubes, each with edge four, form a big cube. One corner cube is removed. How do the "
        "volume and the total surface area of the solid change?", pt('stem', 'Twenty-seven identical cubes', 'hl', 9.0),
        show(f132a['line'], 'Twenty-seven identical cubes'), voice='calm', pause=0.5),
      L("We call these Rubik's cube questions, and the idea comes back quite a lot on the exam. We'll solve it by "
        "understanding, one part at a time."),
      L("First the volume. We take one cube out, so the volume goes down. One small cube is four times four times four, "
        "sixty-four. So the volume goes down by sixty-four.", show(f132r1, 'four times four times four')),
      L("Choice number one says the volume doesn't change, so it's out. The other three choices all say it goes down by "
        "sixty-four.", mk('cross', 'choice 1', "so it's out")),
      L("Now the surface area. This part is harder to see. What does the corner cube give to the surface? Three faces, "
        "the top, the front and the side.", show(f132a['three'], 'Three faces')),
      L("Each face is four times four, sixteen. So if we take the cube away, it looks like we lose three faces, forty-"
        "eight. That's choice number three, and it's a trap.", show(f132r2, 'Each face is four times four'),
        mk('cross', 'choice 3', "That's choice number three")),
      L("Why a trap? Once the corner cube is gone, we can see three faces that it was hiding. These are faces of its "
        "neighbors.", show(f132b['line'], 'Once the corner cube is gone'), show(f132b['new'], 'we can see three faces')),
      L("So we lost three faces, and we gained three faces. The surface area doesn't change. Choice number two is our "
        "answer.", show(f132r3, 'So we lost three faces'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Three places',
      L("Careful, this is not a rule for every cube we remove. It depends on where the cube is. In Rubik's cube "
        "questions, there are three places to tell apart.", show(f132c['line'], 'there are three places')),
      L("A corner, like in our question. It shows three faces, and three new faces appear. Minus three, plus three, no "
        "change.", show(f132c['corner'], 'A corner, like in our question'), show(f132s1, 'Minus three, plus three')),
      L("The middle of an edge. It shows two faces. Take it out, and four faces appear. So the surface goes up by two "
        "faces. Here that's two times sixteen, thirty-two.", show(f132c['edge'], 'The middle of an edge'),
        show(f132s2, 'Here that\'s two times sixteen')),
      L("The middle of a face. It shows only one face. Take it out, and five faces appear. So the surface "
        "goes up by four faces, sixty-four.", show(f132c['face'], 'The middle of a face'), show(f132s3, 'goes up by four faces')),
      L("There's a pattern here. The faces we lose plus the faces we gain always make six, the six faces of the cube we "
        "removed. And I'll see you in the next question.", show(f132s4, 'always make six'))),
])


# =================================================================================================================
# r26-t35-cubefacts (lesson) - Cube, box and cylinder facts
# No Hebrew lesson (added in the 2026-09 review; her g130 diagonal moves are the seed). R37 / R29: the box diagonal is a
# reminder (taught in geo-120 part 2), used here for "the longest rod". NEW: (1) the longest segment inside a cylinder =
# the diagonal of the rectangle 2r x h through the axis, and the whole-number version (the greatest whole length) -
# external finding (Claude E #3, Codex synthesis #7), verified on the real exam 2024 autumn q2_15 (r 3, h 10 -> 11; here
# r 3, h 8 -> 10 and r 2, h 5 -> root 41 -> 6); (2) counting faces, edges and vertices of a prism (n + 2, 3n, 2n) and a
# pyramid (n + 1, 2n, n + 1), the sum of a box's edges = 4 (l + w + h) - real exam 2020 spring q1_19 (2 : 3), 2020 winter
# q1_13 (sum 8 -> 32), the exam-coverage gap D5 (thin); (3) three face areas -> the volume (ab . bc . ca = (abc)^2). The
# old "quick checks" list is left out (W12: no checklists read aloud; each check is taught where it is used).
# Visuals: each fact on a clean solid, the segment / the counted parts teal, the rectangle through the axis pulled out.
# =================================================================================================================
_R6 = boxpts(40, 300, 100, 200, 170)
p_cf1 = G('p_cf1', [
    ('line', box_el(_R6) + [('txt', 90, 324, '2', 'ink', 26), ('txt', 200, 296, '4', 'ink', 26), ('txt', 22, 200, '4', 'ink', 26)]),
    ('rod', [sg(_R6['A'], _R6['G'], 'teal', 6), ('txt', 150, 150, '6', 'teal', 30)]),
], vb='0 20 300 330', w=340, title='The longest rod in a box')
p_cfa1 = H35('p_cfa1', '$\\sqrt{2^2 + 4^2 + 4^2} = \\sqrt{4 + 16 + 16}$')
p_cfa2 = H35('p_cfa2', '$= \\sqrt{36} = 6$')

_cy = 190
p_cf2 = G('p_cf2', [
    ('line', cyl_el(_cy, 310, 90, 230, 26) + [('txt', _cy + 45, 336, '3', 'ink', 26), ('txt', _cy + 112, 200, '8', 'ink', 26),
                                             sg((_cy, 310), (_cy + 90, 310), 'ink', 2.5)]),
    ('rect', [('tint', [(_cy - 90, 310), (_cy + 90, 310), (_cy + 90, 80), (_cy - 90, 80)], 'teal'),
              ('poly', [(_cy - 90, 310), (_cy + 90, 310), (_cy + 90, 80), (_cy - 90, 80)], 'teal', 3)]),
    ('diag', [sg((_cy - 90, 310), (_cy + 90, 80), 'orange', 6)]),
    ('cut', [('tint', [(380, 300), (500, 300), (500, 100), (380, 100)], 'teal'), ('poly', [(380, 300), (500, 300), (500, 100), (380, 100)], 'teal', 3),
             sg((380, 300), (500, 100), 'orange', 6), rt((500, 300), (380, 300), (500, 100), 12, 'teal'),
             ('txt', 440, 326, '6', 'teal', 28), ('txt', 520, 200, '8', 'teal', 28)]),
    ('ans', [('txt', 420, 190, '10', 'orange', 30)]),
], vb='80 60 480 290', w=520, title='The longest segment in a cylinder')
p_cfb1 = H35('p_cfb1', 'the rectangle: $2r$ by $h$')
p_cfb2 = H35('p_cfb2', '$6^2 + 8^2 = 36 + 64 = 100$')
p_cfb3 = H35('p_cfb3', '$\\sqrt{100} = 10$')
p_cfb4 = H35('p_cfb4', '$4^2 + 5^2 = 16 + 25 = 41$')
p_cfb5 = H35('p_cfb5', '$6^2 = 36 < 41 < 49 = 7^2$')
p_cfb6 = H35('p_cfb6', 'greatest whole length: $6$')

_tp = [pj(60, 300, 0, 0, 0, 0.45, 0.6), pj(60, 300, 170, 0, 0, 0.45, 0.6), pj(60, 300, 140, 0, 140, 0.45, 0.6)]
_tq = [(p[0], p[1] - 150) for p in _tp]
p_cf3 = G('p_cf3', [
    ('line', [_praw([_tp[0], _tp[1], _tq[1], _tq[0]], FACE_F), _praw([_tq[0], _tq[1], _tq[2]], FACE_T)]
             + edges_el([(_tp[0], _tp[1], True), (_tp[1], _tp[2], True), (_tp[2], _tp[0], False), (_tq[0], _tq[1], True), (_tq[1], _tq[2], True),
                         (_tq[2], _tq[0], True), (_tp[0], _tq[0], True), (_tp[1], _tq[1], True), (_tp[2], _tq[2], True)])),
    ('faces', [('tint', [_tq[0], _tq[1], _tq[2]], 'orange'), ('tint', [_tp[0], _tp[1], _tq[1], _tq[0]], 'teal'), ('txt', 440, 120, '3 + 2 = 5 faces', 'teal', 24)]),
    ('edges', [sg(_tp[0], _tq[0], 'orange', 6), sg(_tp[1], _tq[1], 'orange', 6), sg(_tp[2], _tq[2], 'orange', 6), ('txt', 440, 180, '3 + 3 + 3 = 9 edges', 'orange', 24)]),
    ('verts', [('dot', *p) for p in _tp + _tq] + [('txt', 440, 240, '3 + 3 = 6 vertices', 'ink', 24)]),
], vb='30 60 560 290', w=480, title='A triangular prism: faces, edges, vertices')
p_cfc1 = I('p_cfc1', 'prism, $n$ sides: $\\ n + 2$ faces, $\\ 3n$ edges, $\\ 2n$ vertices', size=26, col=1)
p_cfc2 = H35('p_cfc2', 'cube, $n = 4$: $\\ 6$, $12$, $8$')
p_cfc3 = I('p_cfc3', 'pyramid, $n$ sides: $\\ n + 1$ faces, $\\ 2n$ edges, $\\ n + 1$ vertices', size=26, col=1)
p_cfc4 = H35('p_cfc4', 'square pyramid: $5$, $8$, $5$')
p_cfc5 = H35('p_cfc5', 'box $2, 3, 4$: $4 \\cdot (2 + 3 + 4) = 36$')

_B5 = boxpts(40, 300, 150, 100, 180)
p_cf4 = G('p_cf4', [
    ('line', box_el(_B5)),
    ('faces', [('tint', [_B5['A'], _B5['B'], _B5['F'], _B5['E']], 'teal'), ('txt', 115, 255, '6', 'teal', 30),
               ('tint', [_B5['B'], _B5['C'], _B5['G'], _B5['F']], 'orange'), ('txt', 240, 205, '10', 'orange', 28),
               ('tint', [_B5['E'], _B5['F'], _B5['G'], _B5['H']], 'red'), ('txt', 180, 165, '15', 'red', 28)]),
], vb='0 60 340 280', w=380, title='A box with three face areas')
p_cfd1 = H35('p_cfd1', '$ab \\cdot bc \\cdot ca = (abc)^2$')
p_cfd0 = H35('p_cfd0', 'edges $a,b,c$: faces $ab,bc,ca$')
p_cfd2 = H35('p_cfd2', '$6 \\cdot 10 \\cdot 15 = 60 \\cdot 15 = 900$')
p_cfd3 = H35('p_cfd3', 'volume $= \\sqrt{900} = 30$')
p_cfd4 = H35('p_cfd4', 'edges $2, 3, 5$: $\\ 2 \\cdot 3 \\cdot 5 = 30$')

video('r26-t35-cubefacts', 'lesson', slides=[
    S('Cube and Box Facts',
      L("Now some more facts about boxes, cubes and cylinders. None of them is on the formula page, and each one comes "
        "up on the exam.")),
    S('The longest rod in a box',
      L("What's the longest straight rod that fits inside a box? It goes from one corner to the opposite corner, "
        "through the inside. That's the body diagonal.", show(p_cf1['line'], "What's the longest straight rod"),
        show(p_cf1['rod'], "That's the body diagonal")),
      L("Like in the lesson on right triangles, square each edge length and add the three squares. The body diagonal "
        "is the square root of that sum. Take a "
        "box two by four by four. Two squared plus four squared plus four squared is four plus sixteen plus sixteen.",
        show(p_cfa1, 'Two squared plus four squared')),
      L("That's thirty-six, and the root of thirty-six is six. So the longest rod is six.", show(p_cfa2, "That's thirty-six"))),
    S('The longest segment in a cylinder',
      L("And in a cylinder? Here's a cylinder with radius three and height eight. What's the longest segment inside "
        "it?", show(p_cf2['line'], "Here's a cylinder with radius three")),
      L("The longest one goes from the edge of the bottom circle, through the middle, to the opposite edge of the top "
        "circle. So it lies in a rectangle that cuts the cylinder through its middle.", show(p_cf2['rect'], 'it lies in a rectangle')),
      L("This rectangle is the diameter wide and the height tall. So it's two r by h. The longest segment is its diagonal.",
        show(p_cfb1, 'Two r by h'), show(p_cf2['diag'], 'The longest segment is its diagonal')),
      L("Let's pull it out. The diameter is two times three, six, and the height is eight. Six squared plus eight "
        "squared is thirty-six plus sixty-four, one hundred.", show(p_cf2['cut'], "Let's pull it out"), show(p_cfb2, 'Six squared plus eight')),
      L("The root of one hundred is ten. So the longest segment is ten. That's the triple six, eight, ten.",
        show(p_cfb3, 'The root of one hundred'), show(p_cf2['ans'], 'So the longest segment is ten')),
      L("Sometimes the question asks for the longest segment whose length is a whole number. Say the radius is two and "
        "the height is five. The diameter is four. Four squared plus five squared is sixteen plus twenty-five, "
        "forty-one.", show(p_cfb4, 'Four squared plus five squared')),
      L("Root forty-one isn't whole. It's between six and seven, because six squared is thirty-six, and seven squared "
        "is forty-nine.", show(p_cfb5, 'six squared is thirty-six')),
      L("So any segment inside is at most root forty-one long. Seven is too long. A shorter segment fits along that "
        "same line, so six fits. So the greatest whole length is six.", show(p_cfb6, 'So the greatest whole length'))),
    S('Faces, edges, vertices',
      L("Now counting. Some questions ask how many faces, edges or vertices a solid has. Here's a triangular prism.",
        show(p_cf3['line'], "Here's a triangular prism")),
      L("First the faces. Three side faces, one on each side of the triangle, plus the two bases. Three plus two is five.",
        show(p_cf3['faces'], 'Three side faces')),
      L("Now the edges. Three around the bottom, three around the top, and three going up. Three times three is nine.",
        show(p_cf3['edges'], 'Three around the bottom')),
      L("And the vertices, the corners. Three at the bottom and three at the top, six.", show(p_cf3['verts'], 'Three at the bottom and three')),
      L("So if the base has n sides, a prism has n plus two faces, three n edges and two n vertices.", show(p_cfc1, 'a prism has n plus two faces')),
      L("Let's check it on a cube. Its base is a square, so n is four. Six faces, twelve edges, eight vertices. That is exactly what a cube has.",
        show(p_cfc2, 'Six faces, twelve edges')),
      L("A pyramid has n side faces and one base, so n plus one faces. Its edges are n around the base and n up to the "
        "top, so two n. Its vertices are n around the base and the top point, n plus one.", show(p_cfc3, 'so n plus one faces')),
      L("A square pyramid has five faces, eight edges and five vertices.", show(p_cfc4, 'A square pyramid has five faces')),
      L("And one more. A box has twelve edges, four of each length. So the sum of all its edges is four times the sum "
        "of the length, the width and the height. For a box two by three by four, that's four times nine, thirty-six.",
        show(p_cfc5, 'four times nine'))),
    S('Three faces, one volume',
      L("Sometimes they give the areas of three faces that meet at one corner, instead of the edges. Here they're six, "
        "ten and fifteen. What's the volume?", show(p_cf4['line'], 'the areas of three faces'), show(p_cf4['faces'], 'six, ten and fifteen')),
      L("Call the length a, the width b and the height c. The three face areas are a times b, b times c, and c times a. "
        "So when we multiply the three areas, every edge appears twice. That's the whole product, length times width "
        "times height, all squared. So it's the volume, squared.", show(p_cfd0, 'Call the length a'), show(p_cfd1, 'every edge appears twice')),
      L("Six times ten is sixty, and sixty times fifteen is nine hundred. The root of nine hundred is thirty. So the "
        "volume is thirty.", show(p_cfd2, 'Six times ten is sixty'), show(p_cfd3, 'The root of nine hundred')),
      L("Let's check. The edges here are two, three and five. Two times three is six, two times five is ten, three times "
        "five is fifteen. And two times three times five is thirty.", show(p_cfd4, 'The edges here are')),
      L("Take a moment to memorize these facts, and I'll see you in the next video.")),
])



# =================================================================================================================
# solve-q-r26-t35-03 - the painted cube
# No Hebrew source (added question). A one-off, taught here (R37): count by position - a corner cube has 3 painted
# faces, an edge cube 2, a cube in the middle of a face 1, an inside cube 0; take off the border (5 - 2 = 3); the check
# 8 + 36 + 54 + 27 = 125; the traps 36 (two faces), 27 (no paint), 150 (all the small faces) at their steps.
# Visuals: the 5 x 5 x 5 cube; the corners orange, an edge row red, the 3 x 3 middles teal on the three faces we see.
# =================================================================================================================
_C125 = [(i, j, k) for i in range(5) for j in range(5) for k in range(5)]
_s6 = 40; _x6, _y6 = 60, 300
_vis = [c for c in _C125 if c[0] == 4 or c[1] == 4 or c[2] == 0]
f03a = PIN(GEO('f03a', [
    ('line', unit_cubes(_vis, _x6, _y6, _s6)),
    ('corner', [('tint', cube_face(4, 4, 0, f, _x6, _y6, _s6), 'orange') for f in ('front', 'top', 'right')]
               + [('tint', cube_face(0, 0, 0, 'front', _x6, _y6, _s6), 'orange'), ('txt', 330, 30, 'corner: 3', 'orange', 24)]),
    ('edge', [('tint', cube_face(i, 4, 0, f, _x6, _y6, _s6), 'red') for i in range(1, 4) for f in ('front', 'top')]
             + [('txt', 330, 60, 'edge: 2', 'red', 24)]),
    ('mid', [('tint', cube_face(i, j, 0, 'front', _x6, _y6, _s6), 'teal') for i in range(1, 4) for j in range(1, 4)]
            + [('tint', cube_face(i, 4, k, 'top', _x6, _y6, _s6), 'teal') for i in range(1, 4) for k in range(1, 4)]
            + [('tint', cube_face(4, j, k, 'right', _x6, _y6, _s6), 'teal') for j in range(1, 4) for k in range(1, 4)]
            + [('txt', 160, 330, '3 by 3 = 9', 'teal', 24)]),
], vb='30 0 400 350', w=440, title='A painted cube cut into 5 by 5 by 5'))
QLEFT(f03a, 'q-r26-t35-03')
f03r1 = IH('f03r1', '$5 - 2 = 3$', size=30)
f03r2 = IH('f03r2', '$3 \\cdot 3 = 9$ on each face', size=30)
f03r3 = IH('f03r3', '$6 \\cdot 9 = 54$', size=30)
f03r4 = IH('f03r4', 'corners: $8$', size=30)
f03r5 = IH('f03r5', 'edges: $12 \\cdot 3 = 36$', size=30)
f03r6 = IH('f03r6', 'inside: $3 \\cdot 3 \\cdot 3 = 27$', size=30)
f03r7 = IH('f03r7', '$8 + 36 + 54 + 27 = 125$', size=30)
FLOW([f03r1, f03r2, f03r3], QC('q-r26-t35-03'))
FLOW([f03r4, f03r5, f03r6, f03r7], QC('q-r26-t35-03'))
NOFIG('solve-q-r26-t35-03', 0, 1)
f03b = PIN(GEO('f03b', [('line', unit_cubes(_vis, _x6, _y6, _s6))], vb='30 0 400 350', w=440, title='The painted cube'))
QLEFT(f03b, 'q-r26-t35-03')

video('solve-q-r26-t35-03', 'solution', qid='q-r26-t35-03', slides=[
    SM('Method 1 · Understanding: count by position', 'Where are they?',
      L("A wooden cube is painted on all six faces. Then it's cut into one hundred twenty-five identical small cubes, "
        "five along each edge. How many small cubes have paint on exactly one face?",
        pt('stem', 'A wooden cube is painted', 'hl', 10.0), show(f03a['line'], 'A wooden cube is painted'), voice='calm', pause=0.5),
      L("I want to use this question to show you how we count in a painted cube. We don't count cube by cube. We ask, "
        "where is the small cube?"),
      L("A small cube on a corner of the big cube touches three painted faces. So it has three painted faces.",
        show(f03a['corner'], 'A small cube on a corner')),
      L("A small cube on an edge, but not on a corner, touches two painted faces.", show(f03a['edge'], 'A small cube on an edge')),
      L("A small cube in the middle of a face touches only one painted face. That's the one we want.",
        show(f03a['mid'], 'in the middle of a face')),
      L("And a small cube inside the big cube isn't painted at all."),
      L("So on each face, we take off the border. Each row has five cubes, and the border takes one at each end. Five "
        "minus two is three. So the middle of each face is three by three, nine cubes.",
        show(f03r1, 'Five minus two is three'), show(f03r2, 'three by three, nine cubes')),
      L("There are six faces, so six times nine, fifty-four. Choice number two is our answer.",
        show(f03r3, 'six times nine'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 1 · Understanding: count by position', 'Check the whole cube',
      L("Let's check that everything adds up to one hundred twenty-five. A cube has eight corners, so eight small cubes "
        "have three painted faces.", show(f03b['line'], "Let's check that everything adds up"), show(f03r4, 'A cube has eight corners')),
      L("A cube has twelve edges, and each edge has three small cubes between its corners. Twelve times three is "
        "thirty-six. These have two painted faces.", show(f03r5, 'Twelve times three')),
      L("Thirty-six is choice number one, and it's a trap. It's the number with two painted faces, not one.",
        mk('cross', 'choice 1', 'Thirty-six is choice number one')),
      L("The inside is a cube three by three by three, twenty-seven. They have no paint. That's choice number three, "
        "another trap.", show(f03r6, 'three by three by three'), mk('cross', 'choice 3', "That's choice number three")),
      L("Eight plus thirty-six is forty-four. Plus fifty-four is ninety-eight. Plus twenty-seven is one hundred "
        "twenty-five. Everything fits.", show(f03r7, 'Plus twenty-seven is')),
      L("And one hundred fifty, choice number four, is six times twenty-five, all the small painted squares, not the "
        "cubes. Choice number two is our answer, and I'll see you in the next question.",
        mk('cross', 'choice 4', 'choice number four, is six times'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])
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
 "geo35-g121": "A cone-shaped container with base radius $\\sqrt6$ cm and height 12 cm is full of water. Which of the following empty containers can hold all the water? The dimensions given are internal dimensions.",
 "q-r26-t35-01": "Water in a box-shaped container with a base of 10 cm × 8 cm reaches a height of 9 cm. All the water is poured into an empty cube-shaped container with an internal edge of 12 cm. How high is the water in the cube (in cm)?",
 "geo35-g122": "A cone and a cylinder have equal base areas. The volume of the cone is four times the volume of the cylinder. If the cylinder’s height is h, what is the cone’s height?",
 "geo35-g123": "The volume of box ABCDEFGH is 320 cm³. M lies on AB so that the ratio AM : MB is 1 : 3, and N lies directly above M on EF. What is the volume of triangular prism AMD–ENH (in cm³)?",
 "geo35-g124": "The bases of a right triangular prism are right triangles. Each base has a leg of 9 cm and a hypotenuse of 15 cm. The height of the prism is 5 cm. What is its lateral surface area (in cm²)?",
 "geo35-g125": "Eighteen identical cubes, each with edge 1 cm, are joined face to face to form a rectangular block. Which of the following block dimensions gives the smallest total surface area?",
 "geo35-g126": "A cylinder is inscribed in a box whose square base has side 2k and whose height is 5k. The cylinder has the same height as the box, and its circular bases are inscribed in the square bases. What fraction of the box’s volume lies outside the cylinder?",
 "geo35-g127": "A pyramid is removed from a cube. The pyramid’s base is the entire bottom face of the cube, and its apex lies on the top face. The remaining solid has volume 60 cm³. What was the volume of the pyramid (in cm³)?",
 "geo35-g128": "A pyramid has a square base with side $4\\sqrt2$ cm. Each lateral edge is 7 cm. What is the height of the pyramid (in cm)?",
 "q-r26-t35-02": "A cone has a base radius of 6 cm and a slant height of 10 cm. What is its volume (in cm³)?",
 "geo35-g129": "The edge of cube ABCDEFGH is $4\\sqrt2$ cm. What is the area of triangle BDG (in cm²)?",
 "geo35-g130": "The edge of cube ABCDEFGH is 3 cm. What is the perimeter of triangle AEG (in cm)?",
 "geo35-g131": "Identical cubes with edge 4 cm are placed in a box with internal dimensions 18 cm × 9 cm × 11 cm. The cube edges must be parallel to the box edges. What is the greatest number of cubes that can fit entirely inside the box?",
 "geo35-g132": "Twenty-seven identical cubes, each with edge 4 cm, form a larger cube. One corner cube is removed, as shown in the accompanying figure. How do the volume and total surface area of the remaining solid change?",
 "q-r26-t35-03": "A wooden cube is painted on all six faces. Then it is cut into 125 identical small cubes, 5 along each edge. How many small cubes have paint on exactly one face?"
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
MV.carry(_types.SimpleNamespace(**globals()), CARRY35)
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
