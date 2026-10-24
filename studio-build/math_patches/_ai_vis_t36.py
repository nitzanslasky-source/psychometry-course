"""Topic 36 (Similarity and scale) - the scripts for the teacher's own-voice reading (2026-10-24), written from the first
draft to the guide (R1-R37, W1-W25), the clarity style, the Codex review standard and Rule V3/V4 geometry visuals, built
exactly like topic 35 (math_patches/_ai_vis_t35.py: the DSL, the GEO colour builders, the solid helpers, the geometry
handwriting hook and the visual passes are copied here, so the topics stay independent).

The camera lesson 'geo-134' (similarity, the linear ratio and the area ratio) gets its own reading script, in parts of
about 3-4 minutes (CAMERA_SPLIT). Every other topic-36 video gets a script that SHE reads aloud in the Reading Studio;
reading_to_video.py times the handwriting and the visuals to her words. The summary video r26-t36-summary is replaced by
the printable page summary_pages/t36.json.

ONE spec per video drives the script (ai_scripts/<vid>.json), the visual plan (VIS[vid], _ai_visual.py format) and the
studio video (t36.py ai_redo_t36() rebuilds the slides from studio_slides(vid), then _ai_visual.apply()).

R37 (2026-10-21): the core methods of similarity are taught in the LESSONS - geo-134 (camera, 3 parts): similar vs
congruent, matching lines, the linear ratio (every pair), the angles stay, the area ratio = the linear ratio squared (and
back with the root), ratio units, the man with glasses; geo-135: regular shapes are always similar, ratio units, a
circumference is a line; geo-139 (parts): two equal angles, matching sides sit opposite equal angles, the small-big table
and the triangle value, the three exam pictures (parallel to the base with part to part, the altitude to the hypotenuse,
the hourglass), rectangles; geo-141: similar solids, the volume ratio = the linear ratio to the power of three; geo-143:
volume changes (cube, height, radius, both, the reverse direction, factor vs percent); r26-t36-map-scale: the scale, the
unit ladder, areas with the scale squared. The first question that uses a method applies it slowly with a one-sentence
link to the lesson; one-off tricks (circles on a diameter, the midpoint segment, a numeric angle, expanding a ratio to
whole numbers, partial similarity) are taught in their question.

Spec DSL (as in topic 35): video / S / SM / L / I / IH / show / pt / mk / GEO / PIN / _R / LEFT / ROWS / FLOW, plus the
solid helpers (boxpts, box_el, cyl_el, cone_el, pyr_el, unit_cubes, pj, G, H36).
"""
import importlib.util, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _geo_hand as _GH

HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t36ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-36 flow order of the scripts
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
                if not d.get('over'):    # (topic 36) a hand-written row is taller, a fraction taller still
                    _sz = d.get('size', 36); _tt = d.get('t') or ''
                    ycol += (d['h'] if d['k'] == 'vis' else int(_sz * 1.55 * (1.2 if it.get('_hand') else 1)
                                                               + (_sz * 0.8 if '\\frac' in _tt else 0))) + 16
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
CAM_BASE = 'geo-134'
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
               for it, d in sl):     # topic 35/36: every right-column stack of a camera part starts below the bubble
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
            'style': "the teacher reads it herself (Reading Studio), topic-36 scripts (2026-10-24): math_patches/_ai_vis_t36.py is "
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
        if (vid, k) in NOFIG36:
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



CARRY36 = {}       # carry-over boxes (V2): {vid: {slide index: [tex, ...]}}, filled by the scripts


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
NOFIG36 = set()       # 2026-10-18 (batch C, as NOFIG31 in topic 31): (video, slide index) that show our enlarged copy
                      # instead of the question figure; the working is written in readable rows on the right (ROWS)


def LEFT(g, y=300, x=410, w=None):
    """(batch C) place a GEO figure (every layer) in the left work area of a NOFIG36 slide, optionally at a new width"""
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


def H36(name, tex, size=34, col=1):
    """a hand-written row in the right column of a lesson"""
    return IH(name, tex, size=size, col=col)


def water_el(P, frac, col='teal'):
    """water filling the box P up to frac of its height: the front and right faces of the water and its surface"""
    lv = lambda a, b: (a[0] + (b[0] - a[0]) * frac, a[1] + (b[1] - a[1]) * frac)
    e1, f1, g1, h1 = lv(P['A'], P['E']), lv(P['B'], P['F']), lv(P['C'], P['G']), lv(P['D'], P['H'])
    return [('tint', [P['A'], P['B'], f1, e1], col), ('tint', [P['B'], P['C'], g1, f1], col),
            ('tint', [e1, f1, g1, h1], col), ('poly', [e1, f1, g1, h1], col, 2.5)]


# the questions' own black-and-white figures (questionVisual of the built course, 22 Oct 2026): the base of our copies
# the questions' own black-and-white figures (questionVisual of the built course, 24 Oct 2026): the base of our copies
QSVG = {
 'geo36-g136': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Regular 10-sided polygon"><title>Regular 10-sided polygon</title><polygon points="320.0,72.6 256.9,93.1 217.9,146.8 217.9,213.2 256.9,266.9 320.0,287.4 383.1,266.9 422.1,213.2 422.1,146.8 383.1,93.1" fill="none" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><text x="320.0" y="56.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="247.4" y="80.1" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="202.6" y="141.8" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="202.6" y="218.2" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="247.4" y="279.9" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">E</text><text x="320.0" y="303.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">F</text><text x="392.6" y="279.9" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">G</text><text x="437.4" y="218.2" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">H</text><text x="437.4" y="141.8" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">I</text><text x="392.6" y="80.1" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">J</text></svg>',
 'geo36-g137': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Six equal small circles whose diameters cover the diameter AB of a larger circle"><title>Six equal small circles whose diameters cover the diameter AB of a larger circle</title><circle cx="320.000" cy="180.000" r="127.750" fill="none" stroke="#000000" stroke-width="2.5"/><line x1="192.2" y1="180.0" x2="447.8" y2="180.0" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><circle cx="213.542" cy="180.000" r="21.292" fill="none" stroke="#000000" stroke-width="4"/><circle cx="256.125" cy="180.000" r="21.292" fill="none" stroke="#000000" stroke-width="4"/><circle cx="298.708" cy="180.000" r="21.292" fill="none" stroke="#000000" stroke-width="4"/><circle cx="341.292" cy="180.000" r="21.292" fill="none" stroke="#000000" stroke-width="4"/><circle cx="383.875" cy="180.000" r="21.292" fill="none" stroke="#000000" stroke-width="4"/><circle cx="426.458" cy="180.000" r="21.292" fill="none" stroke="#000000" stroke-width="4"/><text x="174.2" y="180.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="465.8" y="180.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text></svg>',
 'geo36-g138': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="A small circle whose diameter AC is one quarter of the larger diameter AB"><title>A small circle whose diameter AC is one quarter of the larger diameter AB</title><circle cx="320.000" cy="180.000" r="109.500" fill="none" stroke="#000000" stroke-width="2.5"/><circle cx="237.875" cy="180.000" r="27.375" fill="#d9d9d9" stroke="#000000" stroke-width="2.5"/><line x1="210.5" y1="180.0" x2="429.5" y2="180.0" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="192.5" y="180.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="447.5" y="180.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="275.2" y="198.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text></svg>',
 'geo36-g140': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="In triangle ABC, a segment DE is parallel to BC: AD = 4, DB = 3"><title>In triangle ABC, a segment DE is parallel to BC: AD = 4, DB = 3</title><polygon points="320.0,50.0 211.4,192.9 428.6,192.9" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="320.0,50.0 130.0,300.0 510.0,300.0" fill="none" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="211.4" y1="192.9" x2="428.6" y2="192.9" stroke="#000000" stroke-width="2.5"/><text x="320.0" y="30.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="112.0" y="314.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="528.0" y="314.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="193.4" y="192.9" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="446.6" y="192.9" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">E</text><text x="251.4" y="110.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">4</text><text x="156.4" y="235.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">3</text></svg>',
 'q-r26-t36-01': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Triangle ABC with a point D on BC and the height from A"><title>Triangle ABC with a point D on BC and the height from A</title><polygon points="180.0,60.0 110.0,300.0 278.0,300.0" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="180.0,60.0 110.0,300.0 530.0,300.0" fill="none" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="180.0" y1="60.0" x2="278.0" y2="300.0" stroke="#000000" stroke-width="2.5"/><line x1="180.0" y1="60.0" x2="180.0" y2="300.0" stroke="#000000" stroke-width="2.2" stroke-dasharray="7 5"/><line x1="180.0" y1="289.0" x2="191.0" y2="289.0" stroke="#000000" stroke-width="1.7"/><line x1="191.0" y1="289.0" x2="191.0" y2="300.0" stroke="#000000" stroke-width="1.7"/><text x="180.0" y="40.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="92.0" y="314.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="548.0" y="314.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="292.0" y="286.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text></svg>',
 'q-r26-t36-02': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Trapezoid ABCD with its diagonals meeting at O"><title>Trapezoid ABCD with its diagonals meeting at O</title><polygon points="210.0,110.0 410.0,110.0 314.0,186.0" fill="#d9d9d9" stroke="#000000" stroke-width="1.8" stroke-linejoin="round"/><polygon points="170.0,300.0 470.0,300.0 314.0,186.0" fill="#d9d9d9" stroke="#000000" stroke-width="1.8" stroke-linejoin="round"/><polygon points="210.0,110.0 410.0,110.0 470.0,300.0 170.0,300.0" fill="none" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="210.0" y1="110.0" x2="470.0" y2="300.0" stroke="#000000" stroke-width="2"/><line x1="410.0" y1="110.0" x2="170.0" y2="300.0" stroke="#000000" stroke-width="2"/><text x="196.0" y="96.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="424.0" y="96.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="486.0" y="314.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="154.0" y="314.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="336.0" y="188.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">O</text><text x="310.0" y="92.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">4</text><text x="320.0" y="322.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">6</text></svg>',
 'geo36-g142': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="A large cube-shaped box and a small cubic block, each with one face shaded"><title>A large cube-shaped box and a small cubic block, each with one face shaded</title><polygon points="150.0,257.5 177.5,257.5 192.6,247.9 165.1,247.9" fill="#eeeeee" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="177.5,257.5 192.6,247.9 192.6,275.4 177.5,285.0" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="150.0,257.5 177.5,257.5 177.5,285.0 150.0,285.0" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="300.0,120.0 465.0,120.0 555.8,62.3 390.8,62.3" fill="#eeeeee" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="465.0,120.0 555.8,62.3 555.8,227.2 465.0,285.0" fill="#ffffff" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="300.0,120.0 465.0,120.0 465.0,285.0 300.0,285.0" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><text x="164.0" y="312.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">block</text><text x="382.0" y="312.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">box</text></svg>',
 'geo36-g144': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="A segment ED parallel to AB inside triangle ABC"><title>A segment ED parallel to AB inside triangle ABC</title><polygon points="267.5,51.5 424.9,308.5 215.1,308.5" fill="none" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="246.5" y1="154.3" x2="341.0" y2="308.5" stroke="#000000" stroke-width="3"/><text x="267.5" y="31.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="442.9" y="325.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="197.1" y="325.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="341.0" y="328.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="226.5" y="154.3" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">E</text><text x="235.0" y="102.9" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">4</text><text x="278.0" y="343.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">15</text><text x="383.0" y="343.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">10</text></svg>',
 'geo36-g145': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="A square inside a right triangle creates two smaller similar triangles"><title>A square inside a right triangle creates two smaller similar triangles</title><polygon points="147.105,64.737 492.895,295.263 147.105,295.263" fill="none" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="285.421,156.947 285.421,295.263 147.105,295.263 147.105,156.947" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="147.105" y1="282.968" x2="159.400" y2="282.968" stroke="#000000" stroke-width="1.7"/><line x1="159.400" y1="282.968" x2="159.400" y2="295.263" stroke="#000000" stroke-width="1.7"/><text x="147.105" y="44.737" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="510.895" y="311.263" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="129.105" y="311.263" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="300.421" y="139.947" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="285.421" y="315.263" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">E</text><text x="127.105" y="156.947" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">F</text><text x="125.105" y="110.842" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">5</text><text x="216.263" y="330.263" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">x</text></svg>',
 'geo36-g146': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="An altitude divides the hypotenuse of a right triangle into lengths 3 and 27"><title>An altitude divides the hypotenuse of a right triangle into lengths 3 and 27</title><polygon points="137.5,152.6 91.9,289.5 548.1,289.5" fill="none" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><line x1="137.5" y1="152.6" x2="137.5" y2="289.5" stroke="#000000" stroke-width="2.5"/><line x1="137.5" y1="278.5" x2="148.5" y2="278.5" stroke="#000000" stroke-width="1.7"/><line x1="148.5" y1="278.5" x2="148.5" y2="289.5" stroke="#000000" stroke-width="1.7"/><line x1="133.7" y1="164.0" x2="145.1" y2="167.8" stroke="#000000" stroke-width="1.7"/><line x1="145.1" y1="167.8" x2="148.9" y2="156.4" stroke="#000000" stroke-width="1.7"/><text x="137.5" y="132.6" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="73.9" y="305.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="566.1" y="305.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="141.5" y="309.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="108.7" y="326.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">3</text><text x="342.8" y="324.5" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">27</text></svg>',
 'geo36-g147': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Concentric circles with radii r and 1.3r"><title>Concentric circles with radii r and 1.3r</title><circle cx="320.000" cy="180.000" r="127.750" fill="#d9d9d9" stroke="#000000" stroke-width="2.5"/><circle cx="320.000" cy="180.000" r="98.269" fill="white" stroke="#000000" stroke-width="2.5"/><line x1="320.0" y1="180.0" x2="320.0" y2="278.3" stroke="#000000" stroke-width="2.5"/><line x1="320.0" y1="180.0" x2="447.8" y2="180.0" stroke="#000000" stroke-width="2.5"/><circle cx="320.0" cy="180.0" r="3.2" fill="#000000"/><text x="304.0" y="229.1" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">r</text><text x="391.9" y="164.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">1.3r</text></svg>',
 'geo36-g148': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="A triangle cut by the segment joining two side midpoints"><title>A triangle cut by the segment joining two side midpoints</title><polygon points="340.857,75.714 174.000,284.286 466.000,284.286" fill="none" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><polygon points="340.857,75.714 257.429,180.000 403.429,180.000" fill="#d9d9d9" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><text x="340.857" y="55.714" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="156.000" y="300.286" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="484.000" y="300.286" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="237.429" y="180.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="423.429" y="180.000" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">F</text><line x1="303.052" y1="130.984" x2="295.234" y2="124.730" stroke="#000000" stroke-width="1.8"/><line x1="219.623" y1="235.270" x2="211.805" y2="229.016" stroke="#000000" stroke-width="1.8"/><line x1="374.826" y1="122.599" x2="366.241" y2="127.750" stroke="#000000" stroke-width="1.8"/><line x1="378.045" y1="127.964" x2="369.460" y2="133.115" stroke="#000000" stroke-width="1.8"/><line x1="437.397" y1="226.885" x2="428.812" y2="232.036" stroke="#000000" stroke-width="1.8"/><line x1="440.616" y1="232.250" x2="432.032" y2="237.401" stroke="#000000" stroke-width="1.8"/></svg>',
 'geo36-g149': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Regular 6-sided polygon"><title>Regular 6-sided polygon</title><polygon points="320.000,72.647 227.030,126.324 227.030,233.676 320.000,287.353 412.970,233.676 412.970,126.324" fill="none" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/><text x="320.000" y="56.544" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">A</text><text x="213.084" y="118.272" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">B</text><text x="213.084" y="241.728" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">C</text><text x="320.000" y="303.456" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">D</text><text x="426.916" y="241.728" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">E</text><text x="426.916" y="118.272" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">F</text></svg>',
 'geo36-g150': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="A small ball inside a larger glass globe, shown in cross section"><title>A small ball inside a larger glass globe, shown in cross section</title><circle cx="320.000" cy="180.000" r="109.500" fill="#eeeeee" stroke="#000000" stroke-width="2.5"/><circle cx="372.000" cy="180.000" r="27.375" fill="#d9d9d9" stroke="#000000" stroke-width="2.5"/><line x1="210.5" y1="180.0" x2="429.5" y2="180.0" stroke="#000000" stroke-width="2.5" stroke-dasharray="7 5"/><text x="320.0" y="99.7" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">Glass globe</text><text x="372.0" y="140.0" text-anchor="middle" dominant-baseline="middle" fill="#000000" font-family="DejaVu Sans,Arial,sans-serif" font-size="16">Ball</text></svg>',
 'geo36-g151': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Right circular cone"><title>Right circular cone</title><polygon points="232.400,296.800 407.600,296.800 320.000,63.200" fill="#d9d9d9" stroke="none" stroke-width="2.5" stroke-linejoin="round"/><path d="M 232.4 296.8 A 87.6 24.528000000000002 0 0 1 407.6 296.8" fill="none" stroke="#000000" stroke-width="2" stroke-dasharray="6 5"/><path d="M 232.4 296.8 A 87.6 24.528000000000002 0 0 0 407.6 296.8" fill="none" stroke="#000000" stroke-width="2.5"/><line x1="232.400" y1="296.800" x2="320.000" y2="63.200" stroke="#000000" stroke-width="2.5"/><line x1="320.000" y1="63.200" x2="407.600" y2="296.800" stroke="#000000" stroke-width="2.5"/></svg>',
}

QSTEM = {
 "geo36-g136": "The side length of a regular decagon is multiplied by $5$. By what factor is its perimeter multiplied?",
 "geo36-g137": "AB is a diameter of a circle with radius $9$ cm. Six congruent smaller circles have their centers on AB. Their diameters cover AB from end to end, as shown in the figure. What is the sum of the circumferences of the six smaller circles (in cm)?",
 "geo36-g138": "AB is a diameter of a circle. Point C lies on AB, and $AC=\\frac14AB$. A smaller circle has diameter AC. What is the ratio of the area of the smaller circle to the area inside the larger circle but outside the smaller circle?",
 "geo36-g140": "In triangle ABC, point D lies on AB and point E lies on AC, and $DE\\parallel BC$. Given: $\\begin{cases} AD=4\\text{ cm} \\\\ DB=3\\text{ cm} \\end{cases}$ What is the ratio of the area of triangle ADE to the area of trapezoid DBCE?",
 "q-r26-t36-01": "In triangle ABC, point D lies on BC. The ratio $BD:DC=2:3$. The area of triangle ABC is $40$ cm². What is the area of triangle ABD (in cm²)?",
 "q-r26-t36-02": "ABCD is a trapezoid with $AB\\parallel DC$. Its diagonals meet at O. Given: $\\begin{cases} AB=4\\text{ cm} \\\\ DC=6\\text{ cm} \\end{cases}$ The area of triangle AOB is $8$ cm². What is the area of the trapezoid (in cm²)?",
 "geo36-g142": "A large cube-shaped box is filled completely with small cubic blocks. The area of one face of the box is $36$ times the area of one face of a block. How many blocks fill the box?",
 "geo36-g144": "In triangle ABC, point D lies on BC and point E lies on AC, and $ED\\parallel AB$. Given: $\\begin{cases} BD=10\\text{ cm} \\\\ DC=15\\text{ cm} \\\\ AE=4\\text{ cm} \\end{cases}$ What is the length of AC (in cm)?",
 "geo36-g145": "ABC is a right triangle with the right angle at C. DECF is a square: D lies on AB, E lies on BC, and F lies on AC. $AF=5$ cm, and the side of the square is $x$ cm. What is the length of BE (in cm)?",
 "geo36-g146": "ABC is a right triangle with the right angle at A. AD is perpendicular to BC. Given: $\\begin{cases} BD=3\\text{ cm} \\\\ DC=27\\text{ cm} \\end{cases}$ What is the length of AD (in cm)?",
 "geo36-g147": "Two concentric circles have radii $r$ and $1.3r$. Noah claims that the outer circumference is $1.3$ times the inner circumference. Emma claims that the area of the ring between the circles is greater than the area of the inner circle. Who is correct?",
 "geo36-g148": "D and F are the midpoints of sides AB and AC of triangle ABC. The area of trapezoid DBCF is $21$ cm². What is the area of triangle ADF (in cm²)?",
 "geo36-g149": "Two regular hexagons have areas $150\\sqrt3$ cm² and $30\\sqrt3$ cm². What is the ratio of the perimeter of the first hexagon to the perimeter of the second?",
 "geo36-g150": "A hollow glass globe contains a small solid ball. The small ball’s diameter is $\\frac12$ of the globe’s radius. What is the ratio of the difference between their volumes to the small ball’s volume?",
 "geo36-g151": "A cone-shaped container with base radius $r$ and height $h$ is filled with sand using a cone-shaped scoop. The scoop's radius is $\\frac r2$, and its height is $\\frac h6$. How many full scoops are needed to fill the container? (Assume that no sand is spilled.)",
 "q-r26-t36-03": "Each edge of a cube is increased by $20\\%$. By what percent does the volume of the cube increase?",
 "q-r26-t36-04": "A map has a scale of $1:20{,}000$. On the map, the distance between two towns is $7.5$ cm. What is the real distance between the towns (in km)?",
 "q-r26-t36-05": "A map has a scale of $1:40{,}000$. A lake covers $5$ cm² on the map. What is the real area of the lake (in km²)?",
}
# =================================================================================================================
# Question videos (topic 36). Layout (as topic 34, batch C NOFIG): on every slide our enlarged colour copy of the
# question's figure sits on the left (LEFT; its base layer is the question's own black-and-white figure) and the working
# is written in readable hand rows on the right (FLOW), each at its own clause.
# =================================================================================================================
def QY(vid, y):
    return y


def NOFIG(vid, *slides):
    NOFIG36.update((vid, k) for k in slides)


COLS = [(920, 660, 240, 860)]
LONGCH = set()      # choices written as sentences: one column of four rows, from about y 715


def QTOP(qid):
    """where the work area starts: below the question's lines (measured on the frames: about 72 px a line)"""
    import math
    n = math.ceil(len(re.sub(r'\$[^$]*\$', 'xxxx', QSTEM[qid])) / 80.0)
    return 40 + 72 * n


def QBOT(qid):
    return {}.get(qid, 590 if qid in LONGCH else 700)


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




def QC2(qid, top=None):
    """(topic 36) two narrower columns of hand-written rows on the right of the copy"""
    t = (top or QTOP(qid)) + 5
    return [(870, 360, t, QBOT(qid)), (1235, 360, t, QBOT(qid))]


# =================================================================================================================
# geo-134 (camera lesson, in 3 parts) - Similarity: the linear ratio and the area ratio
# Hebrew geo 7031-7219 (her first similarity lesson, all of it): why similarity comes last; similar = the same shape in
# another size, the same size = congruent; matching lines (radius with radius, circumference with circumference, never a
# diameter with a chord); the linear ratio is the same for every pair of matching lines; the angles don't change; not only
# sides (heights, medians, diagonals, even differences of sides; the square's diagonal x2 -> its side x2); the area ratio =
# the linear ratio squared (her grid: a square 1 -> 2 = 4 squares, a right triangle 1, 2 -> 3, 6 = 9 triangles, "let's see
# it with another number"); the circle 1 : 2 -> 1 : 4; THE MAN WITH GLASSES (two small circles on the diameter: the top
# leftover = one small circle, "Kenny from South Park", "Batman"); recap.
# English numbers (renumbered course, kept): the triangles 4 and 6 (2 : 3; 8 -> 12, 2 -> 3), the squares 2 -> 6 (9), the
# triangles 1, 2 -> 4, 8 (16), sides 8, 5 -> 16, 10 (the difference 3 -> 6), 4 : 5 -> 16 : 25 and back 25 : 49 -> 5 : 7.
# Added for R2/R5: a stretched (not similar) non-example; the why of the square (two directions); the man with glasses is
# counted in RATIO UNITS (her own "one unit" there) - the method every question of the topic uses. Reminder (R29): area x
# k^2 was met with squares (topic 32 geo-043); here it is taught fully, as similarity.
# Visuals (V3): every picture built at her words - the copy / the enlargement / the stretch; the matching radius teal and
# the circumferences orange, the wrong pair red; the two triangles with their bases teal, their left sides orange and the
# equal angles marked; the two squares' diagonals and sides; the 3 x 3 grid counted; the 16 small triangles; the man with
# glasses tinted part by part with its units.
# =================================================================================================================
f134a = G('f134a', [
    ('line', [('poly', [(30, 300), (130, 300), (55, 210)], 'ink', 3), ('txt', 80, 332, 'original', 'ink', 22)]),
    ('copy', [('tint', [(170, 300), (270, 300), (195, 210)], 'teal'), ('poly', [(170, 300), (270, 300), (195, 210)], 'teal', 3),
              ('txt', 220, 332, 'congruent', 'teal', 22)]),
    ('big', [('tint', [(320, 300), (500, 300), (365, 138)], 'orange'), ('poly', [(320, 300), (500, 300), (365, 138)], 'orange', 3),
             ('txt', 410, 332, 'similar', 'orange', 22)]),
    ('stretch', [('poly', [(560, 300), (780, 300), (615, 210)], 'red', 3, True), ('txt', 670, 332, 'not similar', 'red', 22)]),
], vb='10 120 790 230', w=900, title='Congruent, similar, and not similar')
r134c = H36('r134c', 'same shape, same size: congruent')
r134s = H36('r134s', 'same shape, any size: similar')

f134b = G('f134b', [
    ('line', [('circ', 150, 180, 55), ('dot', 150, 180), ('circ', 430, 180, 110), ('dot', 430, 180)]),
    ('r', [('seg', 150, 180, 205, 180, 'teal', 5), ('txt', 178, 162, 'r', 'teal', 26, True),
           ('seg', 430, 180, 540, 180, 'teal', 5), ('txt', 485, 162, 'R', 'teal', 26, True)]),
    ('c', [('circ', 150, 180, 55, 'orange', 6), ('circ', 430, 180, 110, 'orange', 6)]),
    ('wrong', [('seg', 150, 125, 150, 235, 'red', 4), ('txt', 150, 262, 'diameter', 'red', 20),
               sg(gpt(430, 180, 110, 205), gpt(430, 180, 110, 320), 'red', 4, True), ('txt', 430, 318, 'chord', 'red', 20)]),
], vb='60 50 520 300', w=760, title='Matching lines in two circles')
r134l = H36('r134l', 'linear ratio: matching lines')

_A1, _B1, _C1 = (40, 300), (140, 300), (70, 225)
_A2, _B2, _C2 = (220, 300), (370, 300), (265, 187.5)


def _f134c(name, extra=()):
    base = [('poly', [_A1, _B1, _C1], 'ink', 3), ('poly', [_A2, _B2, _C2], 'ink', 3),
            ('txt', 90, 324, '4', 'ink', 26), ('txt', 295, 324, '6', 'ink', 26)]
    return G(name, [('line', base + list(extra)),
                    ('base', [sg(_A1, _B1, 'teal', 6), sg(_A2, _B2, 'teal', 6)]),
                    ('left', [sg(_A1, _C1, 'orange', 6), sg(_A2, _C2, 'orange', 6)]),
                    ('ang', [ang(_A1, _B1, _C1, 18, 'teal'), ang(_A2, _B2, _C2, 24, 'teal'), ang(_B1, _A1, _C1, 18, 'orange'),
                             ang(_B2, _A2, _C2, 24, 'orange'), ang(_C1, _A1, _B1, 16, 'red'), ang(_C2, _A2, _B2, 22, 'red')])],
             vb='20 170 370 175', w=800, title='Two similar triangles: the bases 4 and 6')


f134c = _f134c('f134c')
f134c2 = _f134c('f134c2')
r134a = H36('r134a', '$4 : 6 = 2 : 3$')
r134b = H36('r134b', 'big $= 1.5 \\cdot$ small')
r134d = H36('r134d', '$8 \\to 12$')
r134e = H36('r134e', '$2 \\to 3$')
r134f = H36('r134f', 'lengths grow, angles stay')

_S134 = [
    S('Similarity',
      L("Welcome back. Today we start a new topic in geometry, similarity."),
      L("We left it for almost the end, and that's on purpose."),
      L("Similarity shows up in every shape we've learned. In triangles, in quadrilaterals, in polygons and in circles."),
      L("So first we had to learn all those shapes. Only now can we talk about similarity.")),
    S('Similar or congruent',
      L("So first, what is similarity? Here's a triangle.", show(f134a['line'], "Here's a triangle")),
      L("Now let's copy it, exactly as it is. The copy has the same shape and the same size. Two shapes like this are "
        "called congruent.", show(f134a['copy'], "Now let's copy it"), show(r134c, 'are called congruent')),
      L("Now let's take the same triangle and make it bigger. It's the same shape, just in another size. Two shapes "
        "like this are called similar.", show(f134a['big'], 'make it bigger'), show(r134s, 'are called similar')),
      L("So similar means the same shape, but not necessarily the same size. One shape is an enlarged copy of the other."),
      L("And here's a shape that is not similar. We stretched the triangle only sideways. It got wider, but not taller, "
        "so it's not the same shape anymore.", show(f134a['stretch'], 'We stretched the triangle only sideways'))),
    S('Matching lines',
      L("Now, the linear ratio. To understand it, we first need matching lines."),
      L("Matching lines are lines of the same kind, one in each shape. Let's see it with two circles.",
        show(f134b['line'], 'with two circles')),
      L("Two circles really are similar. A small circle and a big circle have the same shape."),
      L("Take the radius of the small circle. Its matching line is the radius of the big circle. And the circumference "
        "matches the circumference.", show(f134b['r'], 'Its matching line is the radius'),
        show(f134b['c'], 'the circumference matches')),
      L("What we can't do is compare a diameter in one circle with a chord in the other. They're not the same kind of "
        "line.", show(f134b['wrong'], 'compare a diameter')),
      L("So the linear ratio is the ratio between two matching lines.", show(r134l, 'So the linear ratio is'))),
    S('The linear ratio',
      L("Here are two similar triangles. I took the small one and enlarged it.", show(f134c['line'], 'Here are two similar triangles')),
      L("The base of the small triangle is four. The matching base in the big one is six. They match, because it's "
        "the same side of the triangle.", show(f134c['base'], 'The base of the small triangle')),
      L("For now we just look. Soon we'll learn how to know exactly what matches what."),
      L("So the linear ratio, from small to big, is four to six. Both numbers divide by two, so it's two to three.",
        show(r134a, 'from small to big, is four to six')),
      L("Six is four, plus half of four. So the big triangle is one and a half times the small one.",
        show(r134b, 'So the big triangle is one and a half')),
      L("And here's the important part. This ratio is the same for every pair of matching lines."),
      L("We don't know the other sides. But if this side is eight, its partner is eight plus half of eight, twelve. If "
        "this side is two, its partner is three.", show(f134c['left'], 'if this side is eight'),
        show(r134d, 'its partner is eight plus half'), show(r134e, 'its partner is three')),
      L("Why is it always the same ratio? Because the big triangle is an enlarged copy. Every line in it was multiplied "
        "by the same number, one and a half.")),
    S('The angles stay',
      L("Now look at the angles. The angles of the two triangles don't change.", show(f134c2['line'], 'Now look at the angles'), show(f134c2['ang'], 'Now look at the angles')),
      L("The angle on the left of the base is the same in both triangles. So is the angle on the right of the base, "
        "and so is the top angle."),
      L("So when we enlarge a shape, the lengths grow, but the angles stay the same. We'll use this a lot with similar "
        "triangles.", show(r134f, 'the lengths grow'))),
]

# ---- part 2: not only sides; the area ratio
f134d = G('f134d', [
    ('line', [('poly', [(40, 300), (110, 300), (110, 230), (40, 230)], 'ink', 3),
              ('poly', [(180, 300), (390, 300), (390, 90), (180, 90)], 'ink', 3)]),
    ('diag', [('seg', 40, 300, 110, 230, 'teal', 5), ('txt', 88, 278, 'd', 'teal', 24, True),
              ('seg', 180, 300, 390, 90, 'teal', 5), ('txt', 300, 220, '3d', 'teal', 26, True)]),
    ('side', [('seg', 40, 300, 110, 300, 'orange', 6), ('txt', 75, 324, 'a', 'orange', 24, True),
              ('seg', 180, 300, 390, 300, 'orange', 6), ('txt', 285, 324, '3a', 'orange', 26, True)]),
], vb='20 70 400 270', w=600, title='Two squares: the diagonal and the side grow together')
r134g = H36('r134g', 'heights, medians, diagonals, perimeters')
r134h = H36('r134h', '$8 - 5 = 3$')
r134i = H36('r134i', '$16 - 10 = 6$')

_g = [(160 + 70 * i, 300 - 70 * j) for i in range(3) for j in range(3)]
f134e = G('f134e', [
    ('line', [('poly', [(40, 300), (110, 300), (110, 230), (40, 230)], 'ink', 3), ('txt', 75, 324, '2', 'ink', 26),
              ('poly', [(160, 300), (370, 300), (370, 90), (160, 90)], 'ink', 3), ('txt', 265, 324, '6', 'ink', 26)]),
    ('grid', [('seg', 230, 300, 230, 90, 'teal', 2.5), ('seg', 300, 300, 300, 90, 'teal', 2.5),
              ('seg', 160, 230, 370, 230, 'teal', 2.5), ('seg', 160, 160, 370, 160, 'teal', 2.5)]),
    ('count', [('txt', x + 35, y - 35, str(k + 1), 'teal', 26) for k, (x, y) in
               enumerate(sorted(_g, key=lambda p: (-p[1], p[0])))]),
], vb='20 70 370 270', w=560, title='A square with side 2 and a square with side 6')
r134j = H36('r134j', 'lengths $1 : 3$')
r134k = H36('r134k', 'areas $1^2 : 3^2 = 1 : 9$')

# the right triangle with legs 1 (up) and 2 (along), and the one with legs 4 and 8, cut into 16 small copies
_tri16 = []
for _i in range(4):
    for _j in range(4 - _i):
        _p = [(160 + 80 * _i, 300 - 40 * _j), (240 + 80 * _i, 300 - 40 * _j), (160 + 80 * _i, 260 - 40 * _j)]
        _tri16.append(cen(_p))
for _i in range(3):
    for _j in range(3 - _i):
        _p = [(240 + 80 * _i, 300 - 40 * _j), (160 + 80 * _i, 260 - 40 * _j), (240 + 80 * _i, 260 - 40 * _j)]
        _tri16.append(cen(_p))
_tri16.sort(key=lambda p: (-p[1], p[0]))
f134f = G('f134f', [
    ('line', [('poly', [(30, 300), (110, 300), (30, 260)], 'ink', 3), rt((30, 300), (110, 300), (30, 260), 10, 'ink'),
              ('txt', 70, 324, '2', 'ink', 24), ('txt', 14, 282, '1', 'ink', 24)]),
    ('big', [('poly', [(160, 300), (480, 300), (160, 140)], 'ink', 3), rt((160, 300), (480, 300), (160, 140), 12, 'ink'),
             ('txt', 320, 324, '8', 'ink', 24), ('txt', 142, 220, '4', 'ink', 24)]),
    ('grid', [('seg', 160, 260, 400, 260, 'teal', 2), ('seg', 160, 220, 320, 220, 'teal', 2), ('seg', 160, 180, 240, 180, 'teal', 2),
              ('seg', 240, 300, 240, 180, 'teal', 2), ('seg', 320, 300, 320, 220, 'teal', 2), ('seg', 400, 300, 400, 260, 'teal', 2),
              ('seg', 240, 300, 160, 260, 'teal', 2), ('seg', 320, 300, 160, 220, 'teal', 2), ('seg', 400, 300, 160, 180, 'teal', 2)]),
    ('count', [('txt', x, y + 2, str(k + 1), 'teal', 15) for k, (x, y) in enumerate(_tri16)]),
], vb='0 125 500 215', w=820, title='Legs 1 and 2, and legs 4 and 8: sixteen small triangles')
r134l1 = H36('r134l1', 'lengths $1 : 4$')
r134l2 = H36('r134l2', 'areas $1 : 16$')
r134l3 = H36('r134l3', '$1 \\cdot 2 \\div 2 = 1$')
r134l4 = H36('r134l4', '$4 \\cdot 8 \\div 2 = 16$')

r134m1 = H36('r134m1', 'lengths $4 : 5$')
r134m2 = H36('r134m2', 'areas $16 : 25$')
r134m3 = H36('r134m3', 'areas $25 : 49$')
r134m4 = H36('r134m4', 'lengths $\\sqrt{25} : \\sqrt{49} = 5 : 7$')

_S134 += [
    S('Not only sides',
      L("The linear ratio isn't only between sides. It works for every pair of matching lines."),
      L("Heights, medians, diagonals and perimeters all keep the same ratio. Even the difference between two sides "
        "keeps it.", show(r134g, 'Heights, medians')),
      L("Let's see it with two squares. All squares have the same shape, so any two squares are similar.",
        show(f134d['line'], 'with two squares')),
      L("Say the big square's diagonal is three times the small one's. Then its side is also three times as long.",
        show(f134d['diag'], "Say the big square's diagonal"), show(f134d['side'], 'Then its side is also')),
      L("Now a difference of sides. Say a triangle has sides eight and five. Eight minus five is three.",
        show(r134h, 'Eight minus five')),
      L("Now we double the triangle. The sides become sixteen and ten. Sixteen minus ten is six, so the difference "
        "doubled too.", show(r134i, 'Sixteen minus ten')),
      L("So one ratio, between one pair of matching lines, holds for all of them.")),
    S('The area ratio',
      L("Now the area ratio. In similar shapes, the area ratio is equal to the linear ratio, squared."),
      L("You saw a taste of this with squares. Double the side, and the area is four times as big. Let's see why, "
        "with a grid."),
      L("Here's a small square with side two, and a big square with side six. Six is three times two, so the linear "
        "ratio is one to three.", show(f134e['line'], "Here's a small square with side two"),
        show(r134j, 'so the linear ratio is one to three')),
      L("How many small squares fit inside the big one? There are three in each row, and there are three rows.",
        show(f134e['grid'], 'three in each row')),
      L("Let's count them. One, two, three, and so on, up to nine. Nine small squares.", show(f134e['count'], "Let's count them")),
      L("So the linear ratio is one to three, and we square both numbers. One squared is one, and three squared is "
        "nine. The area ratio is one to nine.", show(r134k, 'The area ratio is one to nine')),
      L("Nine times the area, not three times. Why? Because the square grows three times in its length, and three "
        "times in its width. Three times three is nine.")),
    S('Not only squares',
      L("Let's check it with another shape, not a square. Here's a right triangle with legs one and two.",
        show(f134f['line'], 'a right triangle with legs one and two')),
      L("And here's a bigger one, with legs four and eight. One times four is four, and two times four is eight. So "
        "both legs grew four times.", show(f134f['big'], 'with legs four and eight')),
      L("So the linear ratio is one to four. Then the area ratio should be one squared to four squared, one to "
        "sixteen.", show(r134l1, 'the linear ratio is one to four'), show(r134l2, 'one to sixteen')),
      L("Let's check it with the area formula. The small triangle is one times two, divided by two. That's one.",
        show(r134l3, 'The small triangle is one times two')),
      L("The big triangle is four times eight, divided by two. Four times eight is thirty-two, and half of thirty-two "
        "is sixteen.", show(r134l4, 'The big triangle is four times eight')),
      L("And on the grid, exactly sixteen small triangles fit inside the big one.", show(f134f['grid'], 'And on the grid'),
        show(f134f['count'], 'exactly sixteen small triangles'))),
    S('Square both numbers',
      L("So remember this rule. It's very, very important. Many similarity questions are about exactly this, the "
        "linear ratio and the area ratio."),
      L("The ratio doesn't need a one in it. Say the linear ratio is four to five.", show(r134m1, 'the linear ratio is four to five')),
      L("We square both numbers. Four squared is sixteen, and five squared is twenty-five. So the areas are sixteen to "
        "twenty-five.", show(r134m2, 'So the areas are sixteen')),
      L("And we can go back. Say the areas are twenty-five to forty-nine. What's the linear ratio?",
        show(r134m3, 'Say the areas are twenty-five')),
      L("From lengths to areas we squared. So from areas back to lengths, we take the square root of both numbers. The "
        "root of twenty-five is five, and the root of forty-nine is seven.", show(r134m4, 'the root of forty-nine is seven')),
      L("So the linear ratio is five to seven. A lot of students keep twenty-five to forty-nine for the sides too. "
        "But that's the ratio of the areas, not of the lengths."),
      L("So from lengths to areas, we square. From areas back to lengths, we take the root.")),
]

# ---- part 3: circles and the man with glasses
_TOP = 'M 200 180 A 120 120 0 0 1 440 180 A 60 60 0 0 0 320 180 A 60 60 0 0 0 200 180 Z'
_BOT = 'M 200 180 A 120 120 0 0 0 440 180 A 60 60 0 0 1 320 180 A 60 60 0 0 1 200 180 Z'
f134g = G('f134g', [
    ('line', [('circ', 320, 180, 120), ('seg', 200, 180, 440, 180, 'ink', 2, True), ('dot', 320, 180)]),
    ('small1', [('circ', 260, 180, 60, 'teal', 4, False, 'teal')]),
    ('dd', [('seg', 200, 180, 320, 180, 'teal', 6), ('txt', 260, 202, 'd', 'teal', 24, True),
            ('seg', 200, 320, 440, 320, 'orange', 4), ('txt', 320, 342, '2d', 'orange', 24, True)]),
    ('small2', [('circ', 380, 180, 60, 'teal', 4, False, 'teal')]),
    ('u', [('txt', 260, 160, '1', 'teal', 30), ('txt', 380, 160, '1', 'teal', 30)]),
    ('top', [('region', _TOP, 'orange', 0.35), ('txt', 320, 92, '1', 'orange', 30)]),
    ('bottom', [('region', _BOT, 'orange', 0.35), ('txt', 320, 270, '1', 'orange', 30)]),
], vb='180 45 280 315', w=470, title='A circle, a circle with half its diameter, and the man with glasses')
f134h = G('f134h', [
    ('line', [('circ', 320, 180, 120), ('seg', 200, 180, 440, 180, 'ink', 2, True), ('dot', 320, 180),
              ('circ', 260, 180, 60, 'teal', 4, False, 'teal')]),
    ('dd', [('seg', 200, 180, 320, 180, 'teal', 6), ('txt', 260, 202, 'd', 'teal', 24, True),
            ('seg', 200, 320, 440, 320, 'orange', 4), ('txt', 320, 342, '2d', 'orange', 24, True)]),
    ('small2', [('circ', 380, 180, 60, 'teal', 4, False, 'teal')]),
    ('u', [('txt', 260, 160, '1', 'teal', 30), ('txt', 380, 160, '1', 'teal', 30)]),
    ('top', [('region', _TOP, 'orange', 0.35), ('txt', 320, 92, '1', 'orange', 30)]),
    ('bottom', [('region', _BOT, 'orange', 0.35), ('txt', 320, 270, '1', 'orange', 30)]),
], vb='180 45 280 315', w=470, title='A circle, a circle with half its diameter, and the man with glasses')
r134n1 = H36('r134n1', 'diameters $1 : 2$')
r134n2 = H36('r134n2', 'areas $1 : 4$')
r134o1 = H36('r134o1', 'small circle: $1$ unit')
r134o2 = H36('r134o2', 'big circle: $4$ units')
r134o3 = H36('r134o3', '$4 - 2 = 2$ units left')
r134o4 = H36('r134o4', 'top $= 1$ unit $=$ a small circle')
z134a = I('z134a', 'Similar: the same shape, another size $\\cdot$ the same size too: congruent', size=28)
z134b = I('z134b', 'Linear ratio: the same for every pair of matching lines', size=28)
z134c = I('z134c', 'Area ratio $=$ (linear ratio)$^2$ $\\cdot$ back to lengths: the square root', size=28)

_S134 += [
    S('Circles',
      L("Now let's look at circles. Here's a big circle and its diameter.", show(f134g['line'], "Here's a big circle")),
      L("Inside it, a small circle. Its diameter is exactly half of the big diameter.", show(f134g['small1'], 'Inside it, a small circle'),
        show(f134g['dd'], 'Its diameter is exactly half')),
      L("So the linear ratio here is one to two. And the area ratio is one squared to two squared, one to four.",
        show(r134n1, 'the linear ratio here is one to two'), show(r134n2, 'one to four')),
      L("So the small circle's area is exactly a quarter of the big circle's area.")),
    S('The man with glasses',
      L("Now let's add a second small circle, the same size, next to the first one. Together, their diameters fill the "
        "big diameter.", show(f134h['line'], 'Now let'), show(f134h['small2'], 'add a second small circle')),
      L("This picture comes back a lot on the exam, so it's worth knowing well."),
      L("We don't know the real areas. So let's count in ratio units. Say each small circle is one unit.",
        show(f134h['u'], 'Say each small circle is one unit'), show(r134o1, 'is one unit')),
      L("The big circle is four times a small one, so it's four units.", show(r134o2, "so it's four units")),
      L("The two small circles together are two units. Four minus two is two, so two units are left outside them.",
        show(r134o3, 'Four minus two is two')),
      L("The diameter cuts the picture into two mirror halves. So the two units split equally. One unit is on top, and "
        "one unit is at the bottom.", show(f134h['top'], 'One unit is on top'), show(f134h['bottom'], 'one unit is at the bottom')),
      L("So the white part on top has exactly the same area as one small circle.", show(r134o4, 'So the white part on top')),
      L("I call this shape the man with glasses. The two small circles are his glasses. Some people see Kenny from "
        "South Park in it, or a Batman mask."),
      L("Some questions ask which is bigger, the top part or a small circle. We don't need to calculate and subtract. "
        "We already know they're equal.")),
    S('Recap',
      L("Let's sum up the lesson."),
      L("Similar shapes have the same shape, in another size. If the size is the same too, they're congruent.",
        show(z134a, 'Similar shapes have the same shape')),
      L("The linear ratio is the ratio between matching lines. It's the same for every pair of matching lines.",
        show(z134b, 'The linear ratio is the ratio')),
      L("And the area ratio is the linear ratio, squared. To go back from areas to lengths, we take the square root.",
        show(z134c, 'the area ratio is the linear ratio, squared')),
      L("Next we'll see similarity in regular shapes. Take a moment to memorize these rules, and I'll see you in the "
        "next video.")),
]
video('geo-134', 'lesson', slides=_S134)
CAMERA_SPLIT = ('geo-134', 'Similarity', [
    (1, None),
    (5, "Let's continue with the linear ratio."),
    (8, "Let's continue with the area ratio."),
])


# =================================================================================================================
# geo-135 (lesson) - Similarity in regular shapes
# Hebrew geo 7221-7279: regular shapes are always similar ("every circle in the world looks exactly the same"); the
# equilateral triangle (side 1 : 2 -> 4 small inside); squares 3 : 5 -> 9 : 25 IN RATIO UNITS ("if this is 9, that is 25;
# if 18, then 50 ... 9 ratio units, 25 ratio units"); hexagons 2 : 3 ("try to think before I reveal it") -> 4 : 9; circles
# 1 : 3 -> 1 : 9; the circumference is a LINE -> the linear ratio (4 -> 12).
# English numbers (kept): equilateral 1 : 3 -> 9, squares 4 : 7 -> 16 : 49 (16 -> 49, 32 -> 98), hexagons 5 : 6, circles
# 2 : 5 and the circumference 8 -> 20. Added: the same number of sides; NOT always similar (rectangles, right triangles,
# with pictures - R2 non-examples); ratio units USED once (48 -> 147), the method the questions need (R37).
# Reminder (R29): what a regular shape is (topic 34). Visuals: each pair drawn, the 9 small triangles counted, the units
# written in the squares, the hexagons' areas, the circles' radii teal and their circumferences orange.
# =================================================================================================================
f135n = G('f135n', [
    ('line', [('poly', [(30, 160), (230, 160), (230, 220), (30, 220)], 'ink', 3), ('poly', [(280, 120), (400, 120), (400, 220), (280, 220)], 'ink', 3),
              ('txt', 215, 250, 'not similar', 'red', 24)]),
    ('tri', [('poly', [(30, 380), (170, 380), (30, 299)], 'ink', 3), rt((30, 380), (170, 380), (30, 299), 12, 'ink'),
             ('poly', [(250, 380), (350, 380), (250, 280)], 'ink', 3), rt((250, 380), (350, 380), (250, 280), 12, 'ink'),
             ('txt', 190, 410, 'not similar', 'red', 24)]),
], vb='10 100 400 325', w=480, title='Two rectangles and two right triangles that are not similar')
r135a = H36('r135a', 'regular, same number of sides: similar')

_ep = lambda i, j: (150 + 60 * i + 30 * j, 300 - 52 * j)
_e9 = [cen([_ep(i, j), _ep(i + 1, j), _ep(i, j + 1)]) for i in range(3) for j in range(3 - i)]
_e9 += [cen([_ep(i + 1, j), _ep(i, j + 1), _ep(i + 1, j + 1)]) for i in range(2) for j in range(2 - i)]
_e9.sort(key=lambda p: (-p[1], p[0]))
f135e = G('f135e', [
    ('line', [('poly', [(30, 300), (90, 300), (60, 248)], 'ink', 3), ('txt', 60, 324, 'a', 'ink', 24, True),
              ('poly', [(150, 300), (330, 300), (240, 144)], 'ink', 3), ('txt', 240, 324, '3a', 'ink', 24, True)]),
    ('grid', [sg(_ep(0, 1), _ep(2, 1), 'teal', 2), sg(_ep(0, 2), _ep(1, 2), 'teal', 2), sg(_ep(1, 0), _ep(1, 2), 'teal', 2),
              sg(_ep(2, 0), _ep(2, 1), 'teal', 2), sg(_ep(1, 0), _ep(0, 1), 'teal', 2), sg(_ep(2, 0), _ep(0, 2), 'teal', 2)]),
    ('count', [('txt', x, y + 3, str(k + 1), 'teal', 20) for k, (x, y) in enumerate(_e9)]),
], vb='10 130 340 210', w=520, title='Equilateral triangles with sides a and 3a: nine small triangles')
r135b = H36('r135b', 'sides $1 : 3$')
r135c = H36('r135c', 'areas $1 : 9$')
r135d = H36('r135d', 'perimeters $1 : 3$')

f135s = G('f135s', [
    ('line', [('poly', [(40, 300), (120, 300), (120, 220), (40, 220)], 'ink', 3), ('txt', 80, 324, '4', 'ink', 26),
              ('poly', [(190, 300), (330, 300), (330, 160), (190, 160)], 'ink', 3), ('txt', 260, 324, '7', 'ink', 26)]),
    ('u', [('txt', 80, 262, '16', 'teal', 30), ('txt', 260, 232, '49', 'teal', 34)]),
], vb='20 140 330 200', w=470, title='Squares with sides 4 and 7')
r135e = H36('r135e', 'areas $4^2 : 7^2 = 16 : 49$')
r135f = H36('r135f', '$16 \\to 49$')
r135g = H36('r135g', '$32 \\to 98$')
r135h = H36('r135h', '$16$ units $= 48$')
r135i = H36('r135i', '$1$ unit $= 48 \\div 16 = 3$')
r135j = H36('r135j', 'big: $49 \\cdot 3 = 147$')

_h1 = rp(110, 200, 62.5, 6, 0)
_h2 = rp(310, 200, 75, 6, 0)
f135h = G('f135h', [
    ('line', [('poly', _h1, 'ink', 3), ('poly', _h2, 'ink', 3), side_lab(_h1[4], _h1[5], '5', (110, 200), 18, 'ink', 26),
              side_lab(_h2[4], _h2[5], '6', (310, 200), 18, 'ink', 26)]),
    ('a', [('txt', 110, 200, '25', 'teal', 30), ('txt', 310, 200, '36', 'teal', 32)]),
], vb='30 105 370 205', w=500, title='Regular hexagons with sides 5 and 6')
r135k = H36('r135k', 'areas $5^2 : 6^2 = 25 : 36$')

f135c = G('f135c', [
    ('line', [('circ', 90, 190, 40), ('dot', 90, 190), ('circ', 270, 190, 100), ('dot', 270, 190)]),
    ('r', [('seg', 90, 190, 130, 190, 'teal', 5), ('txt', 110, 174, '2', 'teal', 24),
           ('seg', 270, 190, 370, 190, 'teal', 5), ('txt', 320, 174, '5', 'teal', 26)]),
    ('c', [('circ', 90, 190, 40, 'orange', 6), ('circ', 270, 190, 100, 'orange', 6), ('txt', 90, 250, '8', 'orange', 28)]),
    ('C', [('txt', 270, 312, '20', 'orange', 30)]),
], vb='30 80 360 250', w=470, title='Circles with radii 2 and 5')
r135l = H36('r135l', 'radii $2 : 5$')
r135m = H36('r135m', 'areas $2^2 : 5^2 = 4 : 25$')
r135n = H36('r135n', '$5 \\div 2 = 2.5$')
r135o = H36('r135o', '$8 \\cdot 2.5 = 8 \\cdot 2 + 4 = 20$')
z135a = I('z135a', 'Regular shapes of the same kind: always similar', size=30)
z135b = I('z135b', 'Lines (sides, perimeters, circumferences): the linear ratio', size=30)
z135c = I('z135c', 'Areas: the linear ratio squared $\\cdot$ ratio units', size=30)

video('geo-135', 'lesson', slides=[
    S('Similarity in Regular Shapes',
      L("Welcome back. Now let's look at similarity in regular shapes."),
      L("Remember, in a regular shape all the sides are equal, and all the angles are equal. A square and an "
        "equilateral triangle are regular shapes."),
      L("Regular shapes of the same kind are always similar. Let's see why, and how it helps us.")),
    S('Always similar',
      L("Why are they always similar? Think of a circle. Every circle in the world looks exactly the same. Only the size "
        "changes."),
      L("It's the same with squares, with equilateral triangles and with regular hexagons. Each kind has only one shape."),
      L("But the number of sides must be the same. A regular pentagon and a regular hexagon aren't similar. They're "
        "different shapes.", show(r135a, 'the number of sides must be the same')),
      L("Careful, other shapes are not always similar. Here are two rectangles. One is long and thin, and the other is "
        "almost a square.", show(f135n['line'], 'Here are two rectangles')),
      L("And here are two right triangles. Their sharp angles are different, so they don't have the same shape.",
        show(f135n['tri'], 'here are two right triangles')),
      L("For shapes like these, we have to check. We'll learn how in the next lesson.")),
    S('Equilateral triangles',
      L("First example, the equilateral triangle. Every equilateral triangle has three angles of sixty degrees. So all "
        "equilateral triangles are similar.", show(f135e['line'], 'First example')),
      L("Here the small triangle has side a, and the big one has side three a. The big one is an enlarged picture of "
        "the small one."),
      L("How many small triangles fit inside the big one? Let's count. One, two, three, and so on, up to nine.",
        show(f135e['grid'], 'How many small triangles'), show(f135e['count'], "Let's count")),
      L("That's exactly what we learned in the last lesson. The linear ratio is one to three. So the area ratio is one "
        "squared to three squared, one to nine.", show(r135b, 'The linear ratio is one to three'),
        show(r135c, 'one to nine')),
      L("And the perimeters? A perimeter is a line, so it keeps the linear ratio. The perimeters are one to three too.",
        show(r135d, 'The perimeters are one to three'))),
    S('Squares and ratio units',
      L("Squares are similar too. Here the sides are four and seven.", show(f135s['line'], 'Here the sides are four and seven')),
      L("Cutting the big square into small ones would be hard here. So we don't. We just use the rule. The area ratio "
        "is the linear ratio, squared."),
      L("Four squared is sixteen, and seven squared is forty-nine. So the areas are sixteen to forty-nine.",
        show(r135e, 'Four squared is sixteen')),
      L("What does that mean? If the small square is sixteen square centimeters, the big one is forty-nine.",
        show(r135f, 'the big one is forty-nine')),
      L("If the small square is thirty-two, that's double sixteen. So the big one is double forty-nine, ninety-eight.",
        show(r135g, 'double forty-nine, ninety-eight')),
      L("So we think of it as sixteen ratio units against forty-nine ratio units. One unit can be any number, but it's "
        "the same number in both squares.", show(f135s['u'], 'sixteen ratio units against')),
      L("Let's use it. Say the small square is forty-eight. Then sixteen units are forty-eight.", show(r135h, 'sixteen units are forty-eight')),
      L("So one unit is forty-eight divided by sixteen. That's three, because sixteen times three is forty-eight.",
        show(r135i, 'So one unit is forty-eight divided by')),
      L("The big square is forty-nine units. Forty times three is a hundred twenty, and nine times three is twenty-seven. "
        "So it's a hundred forty-seven.", show(r135j, 'The big square is forty-nine units'))),
    S('Regular hexagons',
      L("A regular hexagon is a regular shape too. So all regular hexagons are similar."),
      L("Here's a small hexagon and a big hexagon. Their sides are five and six.", show(f135h['line'], "Here's a small hexagon")),
      L("What's the area ratio? Try to think about it before I say it."),
      L("Twenty-five to thirty-six. Five squared is twenty-five, and six squared is thirty-six.",
        show(r135k, 'Twenty-five to thirty-six'), show(f135h['a'], 'Five squared is twenty-five')),
      L("We don't need to cut each hexagon into six equilateral triangles. The similarity already did the work.")),
    S('Circles: a circumference is a line',
      L("Now circles. Here the radii are two and five. So the linear ratio is two to five.",
        show(f135c['line'], 'Now circles'), show(f135c['r'], 'Here the radii are two and five'), show(r135l, 'So the linear ratio')),
      L("The area ratio is two squared to five squared, four to twenty-five.", show(r135m, 'The area ratio is two squared')),
      L("Now careful. Say they tell us the small circumference is eight. What's the big circumference?",
        show(f135c['c'], 'the small circumference is eight')),
      L("A circumference is a line. So we stay with the linear ratio, and we don't square it."),
      L("Five divided by two is two and a half. So the big circle is two and a half times the small one.",
        show(r135n, 'Five divided by two')),
      L("Eight times two is sixteen, and half of eight is four. Sixteen plus four is twenty. So the big circumference is "
        "twenty.", show(r135o, 'Eight times two is sixteen'), show(f135c['C'], 'So the big circumference is')),
      L("So we treat the circumference as a line, because that's what it is. Only areas get squared.")),
    S('Recap',
      L("So let's sum up."),
      L("Regular shapes of the same kind are always similar, if they have the same number of sides.",
        show(z135a, 'Regular shapes of the same kind')),
      L("Lines, like sides, perimeters and circumferences, keep the linear ratio.", show(z135b, 'Lines, like sides')),
      L("Areas get the linear ratio squared. And with ratio units, we turn the ratio into real numbers.",
        show(z135c, 'Areas get the linear ratio squared')),
      L("Take a moment to memorize this, and I'll see you in the next video.")),
])


# =================================================================================================================
# solve-geo36-g136 - a regular decagon, side x 5: the perimeter
# Hebrew geo 7281-7302 (a regular pentagon, side x 3): "regular, so we have similarity here; we just talked about the
# perimeter"; she DRAWS it (x -> 3x, 5x -> 15x), then "honestly we didn't need the drawing": the side is a line, the
# perimeter is a line -> x 3. English: a decagon, x 5 (10s -> 50s). Both methods kept, in her order. Added: the traps
# 25 (the area factor) and 50 (the new perimeter, not the factor) at their steps.
# V3: the copy's side AB teal (s), every side orange (10s).
# =================================================================================================================
_D10 = [(320.0, 72.6), (256.9, 93.1), (217.9, 146.8), (217.9, 213.2), (256.9, 266.9), (320.0, 287.4), (383.1, 266.9),
        (422.1, 213.2), (422.1, 146.8), (383.1, 93.1)]
f136a = PIN(GEO('f136a', [
    ('line', [qraw('geo36-g136')]),
    ('side', [sg(_D10[0], _D10[1], 'teal', 7), ('txt', 270, 66, 's', 'teal', 32, True)]),
    ('all', [('poly', _D10, 'orange', 5)]),
    ('p', [('txt', 320, 180, '10s', 'orange', 36, True)]),
], vb='170 40 300 290', w=420, title='The decagon: one side s, the perimeter 10s'))
QLEFT(f136a, 'geo36-g136')
f136b = PIN(GEO('f136b', [
    ('line', [qraw('geo36-g136')]),
    ('x5', [('poly', _D10, 'teal', 5), ('txt', 320, 165, 'side × 5', 'teal', 28), ('txt', 320, 205, 'perimeter × 5', 'teal', 28)]),
], vb='170 40 300 290', w=420, title='Side times 5, perimeter times 5'))
QLEFT(f136b, 'geo36-g136')
r136a = IH('r136a', '$P = 10s$', size=30)
r136b = IH('r136b', 'new side: $5s$', size=30)
r136c = IH('r136c', '$10 \\cdot 5s = 50s$', size=30)
r136d = IH('r136d', '$50s \\div 10s = 5$', size=30)
r136e = IH('r136e', 'side $\\times 5$, perimeter $\\times 5$', size=30)
r136f = IH('r136f', '$5^2 = 25$: the area', size=30)
FLOW([r136a, r136b, r136c, r136d], QC('geo36-g136'))
FLOW([r136e, r136f], QC('geo36-g136'))
NOFIG('solve-geo36-g136', 0, 1)

video('solve-geo36-g136', 'solution', qid='geo36-g136', slides=[
    SM('Method 1 · The math way: draw it', 'Draw it',
      L("Now a new question. The side length of a regular decagon is multiplied by five. By what factor is its "
        "perimeter multiplied?", pt('stem', 'Now a new question', 'hl', 7.0), show(f136a['line'], 'Now a new question'),
        voice='calm', pause=0.5),
      L("So we're given a regular decagon, a shape with ten equal sides. We need to find how many times bigger its "
        "perimeter gets."),
      L("Regular means that the big decagon and the small one are similar. And we just talked about perimeters. We'll "
        "solve it in two different ways."),
      L("Let's start with the math way, and draw it. Say each side of the decagon is s.", show(f136a['side'], 'Say each side')),
      L("It has ten sides, so its perimeter is ten times s, ten s.", show(f136a['all'], 'It has ten sides'),
        show(f136a['p'], 'so its perimeter is ten times s'), show(r136a, 'so its perimeter is ten times s')),
      L("Now a second decagon, with a side five times as long. So each of its sides is five s.", show(r136b, 'each of its sides is five s')),
      L("Its perimeter is ten sides of five s. Ten times five is fifty, so its perimeter is fifty s.",
        show(r136c, 'Ten times five is fifty')),
      L("Fifty s against ten s. Fifty divided by ten is five. So the perimeter is five times as big.",
        show(r136d, 'Fifty divided by ten is five'))),
    SM('Method 2 · Understanding: a line keeps the ratio', 'A perimeter is a line',
      L("Now by understanding. Honestly, we didn't need the drawing.", show(f136b['line'], 'Now by understanding')),
      L("The decagon is regular, so the two decagons are similar. The side grew five times, and a side is a line."),
      L("The perimeter is a line too. So, like in the lesson, it keeps the same linear ratio. It also grows five times.",
        show(f136b['x5'], 'It also grows five times'), show(r136e, 'The perimeter is a line too')),
      L("Careful with twenty-five. That's five squared, so that's what happens to the area. But they asked about the "
        "perimeter, and the perimeter is a line.", show(r136f, 'Careful with twenty-five'),
        mk('cross', 'choice 1', 'Careful with twenty-five')),
      L("And fifty is ten sides times five. That's the new perimeter, written with s. It isn't the factor.",
        mk('cross', 'choice 3', 'And fifty is ten sides')),
      L("So the perimeter is multiplied by five. Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# solve-geo36-g137 - six circles on a diameter of radius 9: the sum of their circumferences
# Hebrew geo 7304-7380 (three circles on a radius-5 diameter, 10 pi): the radius 5/3 is "annoying" ("I can, even with
# algebra, but it's annoying"); "lucky for us we're in the similarity lesson": small radius r, big 3r -> 1 : 3, the
# circumference is a line -> each small one is a third -> three of them = the big one = 2 pi 5 = 10 pi; "see how easily";
# THE GENERAL RULE: the big circumference always equals the sum of the circumferences on its diameter, any number, even
# different sizes. English: six circles, R = 9 (radius 3/2) -> 18 pi. Her annoying calculation is now done in full as the
# math way (R13: the standard way first); her similarity way second. Added: WHY the rule holds (C = pi times d) with a
# second example (diameters 6 and 12); the warning that the areas do NOT add up (a sixth of the area).
# V3: the copy's AB orange (18), one small diameter teal; the radii r and 6r; the big circumference orange (18 pi); a
# clean second picture with circles of diameters 6 and 12.
# =================================================================================================================
f137a = PIN(GEO('f137a', [
    ('line', [qraw('geo36-g137')]),
    ('ab', [('seg', 192.2, 180, 447.8, 180, 'orange', 5), ('txt', 320, 330, 'AB = 18', 'orange', 28)]),
    ('d', [('circ', 213.542, 180, 21.292, 'teal', 5), ('txt', 213.5, 140, '3', 'teal', 28)]),
], vb='160 40 320 310', w=440, title='Six small circles on the diameter A B'))
QLEFT(f137a, 'geo36-g137')
f137b = PIN(GEO('f137b', [
    ('line', [qraw('geo36-g137')]),
    ('r', [('seg', 213.542, 180, 234.834, 180, 'teal', 6), ('txt', 224, 150, 'r', 'teal', 28, True)]),
    ('R', [('seg', 320, 180, 447.8, 180, 'orange', 6), ('txt', 384, 215, '6r', 'orange', 30, True)]),
    ('C', [('circ', 320, 180, 127.75, 'orange', 6)]),
    ('Cv', [('txt', 320, 335, '18π', 'orange', 32)]),
], vb='160 40 320 310', w=440, title='The small radius r and the big radius 6r'))
QLEFT(f137b, 'geo36-g137')
f137c = PIN(GEO('f137c', [
    ('line', [('circ', 320, 180, 120), ('seg', 200, 180, 440, 180, 'ink', 2, True)]),
    ('two', [('circ', 240, 180, 40, 'teal', 4), ('circ', 360, 180, 80, 'orange', 4),
             ('txt', 240, 128, '6', 'teal', 28), ('txt', 360, 88, '12', 'orange', 28), ('txt', 320, 330, '18', 'ink', 28)]),
], vb='180 40 280 310', w=400, title='Circles with diameters 6 and 12 on a diameter of 18'))
QLEFT(f137c, 'geo36-g137')
r137a = IH('r137a', '$AB = 2 \\cdot 9 = 18$', size=30)
r137b = IH('r137b', '$18 \\div 6 = 3$', size=30)
r137c = IH('r137c', '$r = 3 \\div 2 = 1.5$', size=30)
r137d = IH('r137d', '$2π \\cdot 1.5 = 3π$', size=30)
r137e = IH('r137e', '$6 \\cdot 3π = 18π$', size=30)
r137f = IH('r137f', 'radii $1 : 6$', size=30)
r137g = IH('r137g', 'circumferences $1 : 6$', size=30)
r137h = IH('r137h', '$6$ small $=$ the big one', size=30)
r137i = IH('r137i', '$2π \\cdot 9 = 18π$', size=30)
r137j = IH('r137j', '$C = π \\cdot d$', size=30)
r137k = IH('r137k', '$6π + 12π = 18π$', size=30)
r137l = IH('r137l', 'area: $6 \\cdot \\frac{1}{36} = \\frac{1}{6}$ only', size=30)
FLOW([r137a, r137b, r137c, r137d, r137e], QC('geo36-g137'))
FLOW([r137f, r137g, r137h, r137i], QC('geo36-g137'))
FLOW([r137j, r137k, r137l], QC('geo36-g137'))
NOFIG('solve-geo36-g137', 0, 1, 2)

video('solve-geo36-g137', 'solution', qid='geo36-g137', slides=[
    SM('Method 1 · The math way', 'The annoying radius',
      L("Now a new question. A B is a diameter of a circle with radius nine. Six identical smaller circles have their "
        "centers on A B. Their diameters cover A B from end to end. What is the sum of the circumferences of the six "
        "smaller circles?", pt('stem', 'Now a new question', 'hl', 11.0), show(f137a['line'], 'Now a new question'),
        voice='calm', pause=0.5),
      L("So we need the six small circumferences, all added together. We'll solve it in two different ways."),
      L("Let's start with the math way. The big radius is nine, so the diameter A B is two times nine, eighteen.",
        show(f137a['ab'], 'so the diameter A B'), show(r137a, 'two times nine')),
      L("Six small diameters fill A B. So each small diameter is eighteen divided by six, three.",
        show(f137a['d'], 'Six small diameters fill A B'), show(r137b, 'eighteen divided by six')),
      L("A radius is half a diameter. So the small radius is three divided by two, one and a half.", show(r137c, 'three divided by two')),
      L("Honestly, a radius of one and a half is a bit annoying. It's a fraction. But we can still calculate. The "
        "circumference is two pi r."),
      L("Two times one and a half is three. So one small circumference is three pi.", show(r137d, 'Two times one and a half')),
      L("There are six of them. Six times three pi is eighteen pi. Now let's see a faster way, with no annoying "
        "radius.", show(r137e, 'Six times three pi'))),
    SM('Method 2 · Understanding: similarity', 'One sixth of the big circle',
      L("Now by understanding, with similarity. All circles are similar to each other.", show(f137b['line'], 'Now by understanding')),
      L("Let's call the small radius r. The big diameter is six small diameters. So the big radius is six small radii, "
        "six r.", show(f137b['r'], "call the small radius r"), show(f137b['R'], 'So the big radius is')),
      L("So the linear ratio is one to six. A circumference is a line. So the circumferences are one to six too.",
        show(r137f, 'the linear ratio is one to six'), show(r137g, 'the circumferences are one to six')),
      L("So each small circumference is a sixth of the big one. Six sixths make a whole. So the six small "
        "circumferences together are exactly the big circumference.", show(r137h, 'Six sixths make a whole')),
      L("The big circumference is easy, two pi r. The radius is nine, and two times nine is eighteen. So it's eighteen "
        "pi.", show(f137b['C'], 'The big circumference is easy'), show(r137i, 'two times nine is eighteen'), show(f137b['Cv'], "So it's eighteen pi")),
      L("We got eighteen pi again, and we didn't need the small radius at all.")),
    SM('Method 2 · Understanding: similarity', 'Any circles on a diameter',
      L("By the way, this is always true. Take circles whose diameters fill the diameter of a big circle. Their "
        "circumferences always add up to the big circumference."),
      L("It doesn't matter how many circles there are. They don't even need to be the same size.",
        show(f137c['line'], "It doesn't matter how many")),
      L("Why? A circumference is pi times the diameter. The small diameters add up to the big diameter. So pi times "
        "them adds up too.", show(r137j, 'A circumference is pi times')),
      L("For example, circles with diameters six and twelve sit on a diameter of eighteen. Six pi plus twelve pi is "
        "eighteen pi, the big circumference.", show(f137c['two'], 'circles with diameters six and twelve'),
        show(r137k, 'Six pi plus twelve pi')),
      L("But careful, this is only for circumferences. Each small circle has a sixth of the radius, so a thirty-sixth "
        "of the area. Six of them cover only six thirty-sixths, a sixth of the big area.",
        show(r137l, 'Six of them cover only')),
      L("So the sum of the circumferences is eighteen pi. Choice number four is our answer, and I'll see you in the "
        "next question.", mk('tick', 'choice 4', 'Choice number four is our answer'))),
])


# =================================================================================================================
# solve-geo36-g138 - a small circle on a quarter of the diameter: small : the rest
# Hebrew geo 7382-7438 (AO = half AB, dark : white): linear 1 : 2 -> areas 1 : 4, "but they didn't ask for the small
# circle against the big one" -> 4 - 1 = 3 -> 1 : 3; her tip about the choices; "of course I can always calculate (x,
# 2x)... but with similarity, in seconds, with understanding". English: AC = a quarter of AB -> 1 : 16 -> 16 - 1 = 15 ->
# 1 : 15. DECIDED by the teacher (23 Oct): her generalisation "the common-mistake answer usually isn't among the choices"
# is NOT said (unsafe). Only the safe part: "the choices help: if your answer isn't among them, read the question
# again" - and the English trap choice (1 : 16 is choice 1) is kept. Her "always calculate" = method 2 (r = 1, R = 4).
# V3: the copy's AC teal (1) and AB orange (4); the units 1 and 16; the ring tinted (15).
# =================================================================================================================
_RING138 = ('M 210.5 180 a 109.5 109.5 0 1 0 219 0 a 109.5 109.5 0 1 0 -219 0 Z '
            'M 210.5 180 a 27.375 27.375 0 1 0 54.75 0 a 27.375 27.375 0 1 0 -54.75 0 Z')
f138a = PIN(GEO('f138a', [
    ('line', [qraw('geo36-g138')]),
    ('ac', [('seg', 210.5, 180, 265.25, 180, 'teal', 6), ('txt', 238, 225, '1', 'teal', 28)]),
    ('ab', [('seg', 210.5, 310, 429.5, 310, 'orange', 5), ('txt', 320, 334, '4', 'orange', 28)]),
], vb='170 40 300 310', w=430, title='A C is a quarter of A B'))
QLEFT(f138a, 'geo36-g138')
f138b = PIN(GEO('f138b', [
    ('line', [qraw('geo36-g138')]),
    ('u', [('txt', 238, 225, '1', 'teal', 28), ('txt', 330, 100, '16', 'orange', 30)]),
    ('ring', [('region', _RING138, 'teal', 0.3), ('txt', 360, 240, '15', 'teal', 34)]),
], vb='170 40 300 290', w=430, title='The small circle and the rest of the big circle'))
QLEFT(f138b, 'geo36-g138')
f138c = PIN(GEO('f138c', [
    ('line', [qraw('geo36-g138')]),
    ('rr', [('seg', 237.875, 180, 265.25, 180, 'teal', 6), ('txt', 251, 220, '1', 'teal', 26),
            ('seg', 320, 180, 429.5, 180, 'orange', 6), ('txt', 375, 160, '4', 'orange', 28)]),
], vb='170 40 300 290', w=430, title='The radii 1 and 4'))
QLEFT(f138c, 'geo36-g138')
r138a = IH('r138a', 'lengths $1 : 4$', size=30)
r138b = IH('r138b', 'areas $1^2 : 4^2 = 1 : 16$', size=30)
r138c = IH('r138c', 'small $1$, big $16$', size=30)
r138d = IH('r138d', 'the rest: $16 - 1 = 15$', size=30)
r138e = IH('r138e', 'small : rest $= 1 : 15$', size=30)
r138f = IH('r138f', '$r = 1$, $R = 4$', size=30)
r138g = IH('r138g', 'small: $π \\cdot 1^2 = π$', size=30)
r138h = IH('r138h', 'big: $π \\cdot 4^2 = 16π$', size=30)
r138i = IH('r138i', 'rest: $16π - π = 15π$', size=30)
r138j = IH('r138j', '$π : 15π = 1 : 15$', size=30)
FLOW([r138a, r138b], QC('geo36-g138'))
FLOW([r138c, r138d, r138e], QC('geo36-g138'))
FLOW([r138f, r138g, r138h, r138i, r138j], QC('geo36-g138'))
NOFIG('solve-geo36-g138', 0, 1, 2)

video('solve-geo36-g138', 'solution', qid='geo36-g138', slides=[
    SM('Method 1 · Understanding: ratio units', 'Linear, then area',
      L("Now a new question. A B is a diameter of a circle. Point C lies on A B, and A C is a quarter of A B. A smaller "
        "circle has diameter A C. What is the ratio of the area of the smaller circle to the area inside the larger "
        "circle but outside the smaller circle?", pt('stem', 'Now a new question', 'hl', 12.0),
        show(f138a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("So we compare two areas. The small circle, and the part of the big circle that's left outside it. We'll solve "
        "it in two different ways."),
      L("Let's start by understanding, with similarity. The two circles are similar. The small diameter, A C, is a "
        "quarter of the big diameter, A B.", show(f138a['ac'], 'The small diameter, A C'), show(f138a['ab'], 'the big diameter, A B')),
      L("So the linear ratio is one to four. And the area ratio is one squared to four squared, one to sixteen.",
        show(r138a, 'the linear ratio is one to four'), show(r138b, 'one to sixteen'))),
    SM('Method 1 · Understanding: ratio units', 'What do they compare?',
      L("Careful, sixteen isn't our final answer yet. They didn't ask for the small circle against the whole big "
        "circle. They asked for the small circle against what's left outside it.", show(f138b['line'], 'Careful, sixteen'),
        pt('stem: ask', 'They asked for the small circle')),
      L("Here's a tip about the choices. The choices are there to help us. If the answer we got isn't among them, we "
        "read the question again."),
      L("And sometimes a trap is there too. Here one to sixteen is choice number one. So before we circle anything, we "
        "check exactly what they compare.", mk('cross', 'choice 1', 'one to sixteen is choice number one')),
      L("So let's count in ratio units. The small circle is one unit, and the whole big circle is sixteen units.",
        show(f138b['u'], "let's count in ratio units"), show(r138c, 'The small circle is one unit')),
      L("The part that's left is the big circle minus the small one. Sixteen minus one is fifteen units.",
        show(f138b['ring'], "The part that's left"), show(r138d, 'Sixteen minus one')),
      L("So the small circle to the part that's left is one to fifteen. That's choice number two.",
        show(r138e, 'is one to fifteen'))),
    SM('Method 2 · Plugging in numbers', 'Real radii',
      L("Now let's plug in numbers. We can always calculate with real radii. The radii must be one to four, so let's "
        "take a small radius of one, and a big radius of four.", show(f138c['line'], "Now let's plug in numbers"),
        show(f138c['rr'], "take a small radius of one"), show(r138f, 'a small radius of one')),
      L("The small area is pi times one squared, so it's pi.", show(r138g, 'The small area is pi times')),
      L("The big area is pi times four squared. Four squared is sixteen, so it's sixteen pi.", show(r138h, 'The big area is pi times')),
      L("What's left is sixteen pi minus pi, fifteen pi.", show(r138i, "What's left is sixteen pi")),
      L("So it's pi to fifteen pi. Pi is in both, so it cancels, and we get one to fifteen again.", show(r138j, 'Pi is in both')),
      L("With similarity and ratio units, it takes only a few seconds. Choice number two is our answer, and I'll see "
        "you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# geo-139 (lesson, 4 parts) - Similar triangles and rectangles
# Hebrew geo 7440-7703: shapes that aren't regular - harder to know WHAT MATCHES WHAT; similar triangles = all angles
# equal, two are enough (the third completes 180); matching sides sit OPPOSITE equal angles (a regular polygon has no
# such question); "I strongly recommend, from years of experience: students tried ratios and division the way they were
# taught and got tangled - make a SMALL-BIG TABLE, write the matching sides one opposite the other, and with the TRIANGLE
# VALUE find the missing side"; turning the triangle doesn't matter (look at the angle); the ratio between two sides of
# the SAME triangle is equal too (6/8 = 3/4), a fraction is just a colon; the exam's three pictures: (1) a line PARALLEL
# TO THE BASE (the common mistake AE <-> EC: EC is not a side of a triangle at all; AE goes with the WHOLE AC), (2)
# "diagonal similarity" = the ALTITUDE TO THE HYPOTENUSE (almost only in right triangles; the matching sides sit on
# different sides of the drawing), (3) the HOURGLASS (the Z, "it looks like an S but we call it Z"; a side matches its
# own continuation); rectangles: check both ratios, or the ratio inside each rectangle; the exam's rectangle with its
# corner on the big one's diagonal = similar, the leftover pieces too; "90% of the cases a triangle or a rectangle".
# English numbers (kept): the 12-16-20 / 18-24-30 pair, AD 3, DB 2, AE 6, EC 4, the 15-20-25 altitude (BD 9, AD 12),
# rectangles 5 x 3 / 10 x 6, the 12 x 8 rectangle with AP 9. Restored (hebrew-vs-english-t36 3.2): the triangle value is
# taught HERE, on numbers (16 x 18 / 12 = 24), as in word problems (topic 22 reminder). Added on numbers: the hourglass
# 4 / 8 / 3 -> 6, the two altitude shortcuts with their why (core for g146 / practice), part to part (core for g144),
# the rare SSS / SAS in one line. Reminders (R29): corresponding and Z angles (topic 30), the angle sum (topic 31).
# Visuals (V3): every figure built at her words; equal angles in matching colours (alpha teal, beta orange); the
# matching sides lit pair by pair; the small triangle tinted INSIDE the big one; EC crossed out red; the table built row
# by row (the small-big table = DST layout with columns small | big), the triangle value's diagonal drawn (RATIO).
# =================================================================================================================
def SBT(name, rows, col=1, w=None, title='The small-big table', cols=('small', 'big')):
    """the small-big table: a row per pair of matching sides, columns small | big (built row by row)"""
    return MV.items(_layers, name, MV.DST(rows, cols=cols, title=title), w=w, col=col)


def TVAL(name, given, asked, col=1, w=None, cols=('small', 'big')):
    """the triangle value (topic 22): two rows, the diagonal through the unknown's partner"""
    return MV.items(_layers, name, MV.RATIO(cols, given, asked, diag=True, title='The triangle value'), w=w, col=col)


# ---- two angles are enough
_T1 = [(40, 300), (160, 300), (40, 231)]
_T2 = [(240, 300), (432, 300), (240, 189)]
f139a = G('f139a', [
    ('line', [('poly', _T1, 'ink', 3), ('poly', _T2, 'ink', 3), rt(_T1[0], _T1[1], _T1[2], 12, 'ink'), rt(_T2[0], _T2[1], _T2[2], 14, 'ink'),
              ang(_T1[1], _T1[0], _T1[2], 30, 'teal', '30°', 52), ang(_T2[1], _T2[0], _T2[2], 40, 'teal', '30°', 64)]),
    ('third', [ang(_T1[2], _T1[0], _T1[1], 20, 'orange', '60°', 40), ang(_T2[2], _T2[0], _T2[1], 26, 'orange', '60°', 50)]),
], vb='20 170 430 150', w=560, title='Two triangles with 90 and 30 degrees')
r139a = H36('r139a', '$180 - 90 - 30 = 60$')
r139b = H36('r139b', '$90°, 30°$ and $90°, 40°$: not similar')

# ---- the 12-16-20 and 18-24-30 pair (scale 7)
_C1, _A1, _B1 = (30, 300), (30, 216), (142, 300)
_C2, _A2, _B2 = (220, 300), (220, 174), (388, 300)


def _f139b(name, w=760):
    return G(name, [
        ('line', [('poly', [_C1, _A1, _B1], 'ink', 3), ('poly', [_C2, _A2, _B2], 'ink', 3), rt(_C1, _B1, _A1, 10, 'ink'),
                  rt(_C2, _B2, _A2, 12, 'ink'), ('txt', 14, 258, '12', 'ink', 22), ('txt', 86, 322, '16', 'ink', 22),
                  ('txt', 100, 248, '20', 'ink', 22), ('txt', 200, 237, '18', 'ink', 24), ('txt', 304, 324, '24', 'ink', 24),
                  ('txt', 318, 226, '30', 'ink', 24)]),
        ('ang', [ang(_B1, _A1, _C1, 26, 'teal', 'α', 44), ang(_B2, _A2, _C2, 36, 'teal', 'α', 56),
                 ang(_A1, _C1, _B1, 18, 'orange', 'β', 36), ang(_A2, _C2, _B2, 24, 'orange', 'β', 44)]),
        ('p1', [sg(_C1, _A1, 'teal', 7), sg(_C2, _A2, 'teal', 7)]),
        ('p2', [sg(_C1, _B1, 'orange', 7), sg(_C2, _B2, 'orange', 7)]),
        ('p3', [sg(_A1, _B1, 'red', 6), sg(_A2, _B2, 'red', 6)]),
    ], vb='0 160 410 180', w=w, title='Right triangles 12, 16, 20 and 18, 24, 30')


f139b = _f139b('f139b')
f139c = _f139b('f139c', 560)
f139t = _f139b('f139t', 560)
t139a = SBT('t139a', [('opposite α', '12', '18'), ('opposite β', '16', '24'), ('opposite 90°', '20', '30')], col=0, w=560)
r139c = H36('r139c', 'every row: $\\times 1.5$')
t139b = TVAL('t139b', ('12', '18'), ('16', '?'), col=0, w=440)
r139d = H36('r139d', '$? = 16 \\cdot 18 \\div 12$')
r139e = H36('r139e', '$18 \\div 6 = 3$, $12 \\div 6 = 2$')
r139f = H36('r139f', '$16 \\cdot 3 \\div 2 = 48 \\div 2 = 24$')

# ---- turned upside down
_C3, _A3, _B3 = (388, 174), (388, 300), (220, 174)
f139d = G('f139d', [
    ('line', [('poly', [_C1, _A1, _B1], 'ink', 3), ('poly', [_C3, _A3, _B3], 'ink', 3), rt(_C1, _B1, _A1, 10, 'ink'),
              rt(_C3, _B3, _A3, 12, 'ink'), ('txt', 14, 258, '12', 'ink', 22), ('txt', 86, 322, '16', 'ink', 22),
              ('txt', 408, 237, '18', 'ink', 24), ('txt', 304, 156, '24', 'ink', 24)]),
    ('ang', [ang(_B1, _A1, _C1, 26, 'teal', 'α', 44), ang(_B3, _A3, _C3, 36, 'teal', 'α', 56),
             ang(_A1, _C1, _B1, 18, 'orange', 'β', 36), ang(_A3, _C3, _B3, 24, 'orange', 'β', 44)]),
    ('opp', [sg(_C3, _A3, 'teal', 7), sg(_C3, _B3, 'orange', 7)]),
], vb='0 140 430 200', w=720, title='The big triangle turned upside down')
r139g = H36('r139g', '$\\frac{12}{16} = \\frac{3}{4}$')
r139g2 = H36('r139g2', '$\\frac{18}{24} = \\frac{3}{4}$')
r139h = H36('r139h', '$\\frac{16}{20} = \\frac{4}{5}$')
r139h2 = H36('r139h2', '$\\frac{24}{30} = \\frac{4}{5}$')
r139i = H36('r139i', '$4 : 5$ is the same as $\\frac{4}{5}$')

_S139 = [
    S('Similar Triangles and Rectangles',
      L("Welcome back. Now similarity in shapes that aren't regular."),
      L("In regular shapes, the similarity was easy to see. Here it's harder. Not to see that the shapes are similar, "
        "but to know what matches what."),
      L("This lesson is long and very important, so I'll take it in parts. Let's start with triangles.")),
    S('Two equal angles are enough',
      L("Similar triangles are triangles whose angles are all equal. And it's enough that two angles are equal."),
      L("Why? The three angles of a triangle always add up to a hundred eighty. So if two angles are equal, the third "
        "one must be equal too."),
      L("Here are two triangles. Both have a right angle, and both have an angle of thirty degrees.",
        show(f139a['line'], 'Here are two triangles')),
      L("So the third angle is a hundred eighty minus ninety minus thirty, sixty, in both of them. They're similar.",
        show(r139a, 'a hundred eighty minus ninety'), show(f139a['third'], 'sixty, in both of them')),
      L("But a triangle with ninety and forty degrees isn't similar to them. Its third angle is fifty, not sixty.",
        show(r139b, 'ninety and forty degrees'))),
    S('Matching sides',
      L("Here are two more similar triangles. Both have a right angle.", show(f139b['line'], 'Here are two more similar triangles')),
      L("The other angles are the same in both too. Let's call them alpha and beta.", show(f139b['ang'], "Let's call them alpha and beta")),
      L("In a regular polygon, there's no question of matching. Every side is the same. But in this triangle, the sides "
        "are different. There's a short leg, a long leg, and a hypotenuse."),
      L("So how do we know which side matches which? Here's the rule. In similar triangles, the matching sides are the "
        "sides opposite the equal angles."),
      L("Twelve is opposite alpha in the small triangle. Opposite alpha in the big one is eighteen. So twelve goes with "
        "eighteen.", show(f139b['p1'], 'Twelve is opposite alpha')),
      L("Sixteen is opposite beta. Opposite beta in the big one is twenty-four. So sixteen goes with twenty-four.",
        show(f139b['p2'], 'Sixteen is opposite beta')),
      L("And the hypotenuse is opposite the right angle in both. So twenty goes with thirty.",
        show(f139b['p3'], 'the hypotenuse is opposite the right angle'))),
    S('The small-big table',
      L("Now I strongly recommend something, and I'm telling you this from years of experience.",
        show(f139t['line'], 'Now I strongly recommend')),
      L("Students used to work with ratios and divisions, the way they learned in school. And they got tangled."),
      L("So make a little table. One column for the small triangle, and one column for the big triangle.",
        show(t139a['line'], 'make a little table')),
      L("In each row we write one pair of matching sides. Twelve and eighteen, opposite alpha.", show(t139a['r1'], 'Twelve and eighteen')),
      L("Sixteen and twenty-four, opposite beta.", show(t139a['r2'], 'Sixteen and twenty-four')),
      L("And twenty and thirty, the two hypotenuses.", show(t139a['r3'], 'And twenty and thirty')),
      L("Look at each row. Eighteen is twelve plus half of twelve. So every row is times one and a half. The table shows "
        "us exactly what matches what.", show(r139c, 'So every row is times one and a half'))),
    S('Find the missing side',
      L("The table also finds a missing side. Say we didn't know the twenty-four. We know twelve goes with eighteen, and "
        "sixteen goes with a question mark.", show(t139b['line'], 'Say we didn'), show(t139b['r1'], 'twelve goes with eighteen'),
        show(t139b['r2'], 'sixteen goes with a question mark')),
      L("Like in word problems, we use the triangle value. We multiply along the diagonal, and divide by what's left.",
        show(t139b['diag'], 'We multiply along the diagonal')),
      L("The diagonal is sixteen and eighteen, and what's left is twelve. So it's sixteen times eighteen, divided by "
        "twelve.", show(r139d, 'So it')),
      L("Let's make the numbers smaller first. Eighteen and twelve both divide by six. Eighteen becomes three, and twelve "
        "becomes two.", show(r139e, 'Eighteen and twelve both divide by six')),
      L("So it's sixteen times three, divided by two. Sixteen times three is forty-eight, and half of forty-eight is "
        "twenty-four. That's our missing side.", show(r139f, 'Sixteen times three is forty-eight'))),
    S('Turn it around',
      L("Here it was easy, because the triangles stood the same way. But even if we turn a triangle, we can still find "
        "the matching sides.", show(f139d['line'], 'even if we turn a triangle')),
      L("Here the big triangle is upside down. We don't look at left or right. We look at the angles.",
        show(f139d['ang'], 'We look at the angles')),
      L("Eighteen is still opposite alpha, and twenty-four is still opposite beta. So the pairs haven't changed.",
        show(f139d['opp'], 'Eighteen is still opposite alpha'))),
    S('A ratio inside one triangle',
      L("And here's something useful. The ratio between two sides of the same triangle is also equal in both "
        "triangles.", show(f139c['line'], "here's something useful")),
      L("Twelve over sixteen is three quarters. Eighteen over twenty-four is also three quarters.",
        show(f139c['p1'], 'Twelve over sixteen'), show(r139g, 'Twelve over sixteen is three quarters'), show(r139g2, 'Eighteen over twenty-four')),
      L("Another pair. Sixteen over twenty is four fifths, and twenty-four over thirty is four fifths too.",
        show(r139h, 'Sixteen over twenty is four fifths'), show(r139h2, 'twenty-four over thirty')),
      L("Until now we wrote ratios with a colon, like four to five. A fraction is exactly the same thing. We write it "
        "as a fraction, because fractions are easy to reduce.", show(r139i, 'A fraction is exactly the same thing'))),
]

# ---- part 2: a line parallel to the base
_PA, _PB, _PC = (200, 60), (60, 300), (380, 300)
_PD, _PE = lerp(_PA, _PB, 0.6), lerp(_PA, _PC, 0.6)


def _f139p(name, extra=(), title='DE parallel to BC'):
    return G(name, [
        ('line', [('poly', [_PA, _PB, _PC], 'ink', 3), sg(_PD, _PE, 'ink', 3), nm(_PA, 'A', cen([_PA, _PB, _PC]), 24),
                  nm(_PB, 'B', cen([_PA, _PB, _PC]), 24), nm(_PC, 'C', cen([_PA, _PB, _PC]), 24),
                  at(_PD, 'D', -22, 0, italic=True), at(_PE, 'E', 22, 0, italic=True)] + list(extra)),
        ('par', [('par', _PD[0], _PD[1], _PE[0], _PE[1], 1, 'teal'), ('par', _PB[0], _PB[1], _PC[0], _PC[1], 1, 'teal')]),
        ('ang', [ang(_PD, _PA, _PE, 22, 'teal', 'α', 40), ang(_PB, _PA, _PC, 22, 'teal', 'α', 40),
                 ang(_PE, _PA, _PD, 22, 'orange', 'β', 40), ang(_PC, _PA, _PB, 22, 'orange', 'β', 40)]),
        ('small', [('tint', [_PA, _PD, _PE], 'teal'), ('poly', [_PA, _PD, _PE], 'teal', 4)]),
        ('de', [sg(_PD, _PE, 'teal', 7), sg(_PB, _PC, 'orange', 7)]),
        ('trap', [sg(_PE, _PC, 'red', 7, True), ('txt', 402, 244, 'not a side', 'red', 20)]),
        ('ae', [sg(_PA, _PE, 'teal', 7), sg(_PA, _PC, 'orange', 4, True)]),
    ], vb='30 15 420 320', w=500, title=title)


f139e = _f139p('f139e')
f139f = _f139p('f139f', [('txt', 136, 120, '3', 'ink', 24), ('txt', 72, 252, '2', 'ink', 24), ('txt', 268, 120, '6', 'ink', 24),
                          ('txt', 362, 252, '4', 'ink', 24)], title='AD 3, DB 2, AE 6, EC 4')
r139j = H36('r139j', 'DE goes with BC')
r139k = H36('r139k', 'AE goes with the whole AC')
r139l = H36('r139l', 'AD goes with the whole AB')
r139m = H36('r139m', '$\\frac{AD}{DB} = \\frac{AE}{EC}$')
r139n = H36('r139n', '$\\frac{3}{2} = \\frac{6}{4}$')
r139o = H36('r139o', '$\\frac{DE}{BC} = \\frac{AD}{AB} = \\frac{3}{5}$')
r139p = H36('r139p', '$AB = 3 + 2 = 5$')

_S139 += [
    S('Parallel to the base',
      L("Now, how do similar triangles usually show up on the exam? They come in three pictures. Let's start with the first one, "
        "a line parallel to the base."),
      L("Here's a triangle, A B C. Inside it we draw D E, parallel to the base, B C.", show(f139e['line'], "Here's a triangle"),
        show(f139e['par'], 'parallel to the base')),
      L("The lines are parallel, so the angle at D is equal to the angle at B. These are corresponding angles, like we "
        "learned with parallel lines. In the same way, the angle at E is equal to the angle at C.",
        show(f139e['ang'], 'the angle at D is equal')),
      L("So the small triangle, A D E, and the big triangle, A B C, have the same angles. They're similar.",
        show(f139e['small'], 'So the small triangle')),
      L("This picture is a bit confusing, and here's why. Let's match the sides by the angles."),
      L("D E sits opposite the angle at A, in the small triangle. In the big one, B C sits opposite that angle. So D E "
        "matches B C.", show(f139e['de'], 'D E sits opposite'), show(r139j, 'So D E matches')),
      L("Now A E. A common mistake is to say that A E matches E C. But E C isn't a side of either triangle. It's a "
        "side of the trapezoid at the bottom.", show(f139e['trap'], 'A common mistake')),
      L("A E is opposite alpha, the angle at D, in the small triangle. Opposite alpha in the big triangle, the angle at "
        "B, is the whole side, A C. So A E matches the whole A C.", show(f139e['ae'], 'A E is opposite alpha'),
        show(r139k, 'So A E matches the whole')),
      L("In the same way, A D is opposite beta, so it matches the whole side, A B. Always check which angle a side is "
        "opposite.",
        show(r139l, 'so it matches the whole side'))),
    S('Part to part',
      L("There's one more rule here. It's only about the two sides, A B and A C.", show(f139f['line'], "There's one more rule here")),
      L("A line parallel to the base cuts these two sides in the same ratio. So A D to D B is equal to A E to E C. "
        "That's the part to part rule.", show(r139m, 'So A D to D B')),
      L("Here A D is three and D B is two. A E is six and E C is four. Three over two is one and a half, and six over "
        "four is also one and a half.", show(r139n, 'Three over two')),
      L("So why did we say that A E doesn't match E C? Because of D E. D E isn't a part of a side. It matches the whole "
        "B C.", show(f139f['de'], 'Because of D E')),
      L("A B is three plus two, five. So D E to B C is three to five, like A D to the whole A B. It's not three to two.",
        show(r139p, 'A B is three plus two'), show(r139o, 'So D E to B C is three to five')),
      L("So for the parts of the two sides, part to part is fine. But the parallel line itself always goes with the "
        "whole side.")),
]

# ---- part 3: the altitude to the hypotenuse and the hourglass (scale 12: 15, 20, 25 -> 180, 240, 300)
_HB, _HC, _HD, _HA = (40, 300), (340, 300), (148, 300), (148, 156)
_hc = cen([_HA, _HB, _HC])
f139g = G('f139g', [
    ('line', [('poly', [_HA, _HB, _HC], 'ink', 3), sg(_HA, _HD, 'ink', 3), rt(_HA, _HB, _HC, 12, 'ink'), rt(_HD, _HC, _HA, 12, 'ink'),
              nm(_HA, 'A', _hc, 24), nm(_HB, 'B', _hc, 24), nm(_HC, 'C', _hc, 24), at(_HD, 'D', 0, 24, italic=True),
              ('txt', 80, 220, '15', 'ink', 24), ('txt', 262, 210, '20', 'ink', 24), ('txt', 250, 330, '25', 'ink', 24)]),
    ('small', [('tint', [_HA, _HB, _HD], 'teal'), ('poly', [_HA, _HB, _HD], 'teal', 4)]),
    ('angB', [ang(_HB, _HA, _HC, 26, 'teal', 'α', 44)]),
    ('big', [('poly', [_HA, _HB, _HC], 'orange', 4)]),
    ('nums', [('txt', 96, 324, '9', 'teal', 26), ('txt', 166, 232, '12', 'teal', 26)]),
], vb='0 115 380 240', w=500, title='The altitude to the hypotenuse')
t139c = SBT('t139c', [('hypotenuse', 'AB = 15', 'CB = 25'), ('opposite B', 'AD', 'CA = 20'), ('third side', 'BD', 'BA = 15')],
            col=1, w=520)
r139q = H36('r139q', '$\\frac{15}{25} = \\frac{3}{5}$')
r139r = H36('r139r', '$AD = 20 \\cdot \\frac{3}{5} = 12$')
r139s = H36('r139s', '$BD = 15 \\cdot \\frac{3}{5} = 9$')

f139h = G('f139h', [
    ('line', [('poly', [_HA, _HB, _HC], 'ink', 3), sg(_HA, _HD, 'ink', 3), rt(_HA, _HB, _HC, 12, 'ink'), rt(_HD, _HC, _HA, 12, 'ink'),
              nm(_HA, 'A', _hc, 24), nm(_HB, 'B', _hc, 24), nm(_HC, 'C', _hc, 24), at(_HD, 'D', 0, 24, italic=True),
              ('txt', 96, 324, '9', 'ink', 24), ('txt', 244, 324, '16', 'ink', 24), ('txt', 166, 232, '12', 'ink', 24)]),
    ('two', [('tint', [_HA, _HB, _HD], 'teal'), ('tint', [_HA, _HD, _HC], 'orange')]),
    ('leg', [sg(_HA, _HB, 'teal', 7), ('txt', 80, 220, '15', 'teal', 26)]),
], vb='0 115 380 240', w=500, title='The two shortcuts')
r139t = H36('r139t', '$\\frac{AD}{BD} = \\frac{DC}{AD}$')
r139u = H36('r139u', '$AD^2 = BD \\cdot DC$')
r139v = H36('r139v', '$12^2 = 144 = 9 \\cdot 16$')
r139w0 = H36('r139w0', '$\\frac{BD}{AB} = \\frac{AB}{CB}$')
r139w = H36('r139w', '$AB^2 = BD \\cdot BC$')
r139x = H36('r139x', '$15^2 = 225 = 9 \\cdot 25$')

_GA, _GB, _GC, _GD, _GE = (100, 80), (220, 80), (200, 160), (160, 320), (400, 320)
f139i = G('f139i', [
    ('line', [sg(_GA, _GB), sg(_GD, _GE), sg(_GA, _GE), sg(_GB, _GD), nm(_GA, 'A', None, 22), nm(_GB, 'B', None, 22),
              at(_GC, 'C', 26, 0, italic=True), at(_GD, 'D', -12, 26, italic=True), at(_GE, 'E', 12, 26, italic=True),
              ('txt', 160, 66, '4', 'ink', 24), ('txt', 280, 344, '8', 'ink', 24), ('txt', 136, 132, '3', 'ink', 24)]),
    ('par', [('par', _GA[0], _GA[1], _GB[0], _GB[1], 1, 'teal'), ('par', _GD[0], _GD[1], _GE[0], _GE[1], 1, 'teal')]),
    ('z', [('path', [_GA, _GB, _GD, _GE], 'teal', 7), ang(_GB, _GA, _GD, 22, 'teal'), ang(_GD, _GE, _GB, 22, 'teal')]),
    ('v', [ang(_GC, _GA, _GB, 18, 'red'), ang(_GC, _GE, _GD, 18, 'red'), ang(_GA, _GB, _GC, 22, 'orange'), ang(_GE, _GD, _GC, 22, 'orange')]),
    ('six', [sg(_GC, _GE, 'teal', 6), ('txt', 330, 236, '6', 'teal', 28)]),
], vb='60 40 380 320', w=440, title='The hourglass: AB parallel to DE')
t139d = SBT('t139d', [('opposite C', 'AB = 4', 'ED = 8'), ('opposite B', 'AC = 3', 'EC = ?'), ('opposite A', 'BC', 'DC')],
            col=1, w=520)
r139y = H36('r139y', '$4 \\to 8$: $\\times 2$, so $EC = 3 \\cdot 2 = 6$')

_S139 += [
    S('The altitude to the hypotenuse',
      L("The second picture is the altitude to the hypotenuse. Here's a right triangle, with the right angle at A. From "
        "A we draw the altitude, A D, to the hypotenuse, B C.", show(f139g['line'], "Here's a right triangle")),
      L("Why do we call it that? We could draw a slanted line in any triangle. But on the exam, this picture comes almost "
        "only in a right triangle."),
      L("Look at the small triangle, A B D, and the whole triangle, C B A. Both have a right angle, at D and at A. And "
        "the angle at B is in both of them.", show(f139g['small'], 'Look at the small triangle'), show(f139g['big'], 'and the whole triangle'),
        show(f139g['angB'], 'the angle at B is in both')),
      L("Two equal angles, so they're similar. But careful, the matching sides sit in different places in the drawing."),
      L("A B is the hypotenuse of the small triangle. In the big one, it's a leg. So again, we match by the angles, with "
        "the table.", show(t139c['line'], 'with the table')),
      L("The hypotenuses go together, fifteen and twenty-five.", show(t139c['r1'], 'The hypotenuses go together')),
      L("A D is opposite the angle at B in the small triangle. In the big triangle, C A is opposite B. So A D goes with "
        "twenty.", show(t139c['r2'], 'A D is opposite the angle at B')),
      L("And B D goes with the last side, B A, fifteen.", show(t139c['r3'], 'And B D goes with')),
      L("Fifteen over twenty-five is three fifths. So A D is three fifths of twenty, twelve. And B D is three fifths of "
        "fifteen, nine.", show(r139q, 'Fifteen over twenty-five'), show(r139r, 'So A D is three fifths'),
        show(r139s, 'And B D is three fifths'), show(f139g['nums'], 'fifteen, nine'))),
    S('Two shortcuts',
      L("This picture gives two shortcuts that save a lot of time. Here they are, with the reason.",
        show(f139h['line'], 'This picture gives two shortcuts')),
      L("Look at the two small triangles, on the left and on the right. They're similar too.", show(f139h['two'], 'Look at the two small triangles')),
      L("In the left one, the short leg is B D, and the long leg is A D. In the right one, the short leg is A D, and the "
        "long leg is D C."),
      L("Long leg over short leg is the same in both. So A D over B D is equal to D C over A D.", show(r139t, 'So A D over B D')),
      L("Multiply crosswise, and A D squared is equal to B D times D C. The altitude squared is the two parts of the "
        "hypotenuse, multiplied.", show(r139u, 'A D squared is equal to')),
      L("Let's check it. Twelve squared is a hundred forty-four. And nine times sixteen is also a hundred forty-four.",
        show(r139v, 'Twelve squared is')),
      L("The second shortcut comes from our table. B D went with B A, and A B went with C B. So B D over A B is equal "
        "to A B over C B.", show(f139h['leg'], 'The second shortcut'), show(r139w0, 'So B D over A B')),
      L("Multiply crosswise, and A B squared is B D times B C. A leg squared is its own part of the hypotenuse, times "
        "the whole hypotenuse.", show(r139w, 'A B squared is B D times')),
      L("Fifteen squared is two hundred twenty-five. And nine times twenty-five is also two hundred twenty-five.",
        show(r139x, 'Fifteen squared is'))),
    S('The hourglass',
      L("The third picture is the hourglass. A B is parallel to D E, and two lines cross between them at C. So we get "
        "two triangles.", show(f139i['line'], 'The third picture is the hourglass'), show(f139i['par'], 'A B is parallel to D E')),
      L("Between the parallel lines we have a Z. It looks more like an S here, but we still call it a Z. It shows us two "
        "equal angles.", show(f139i['z'], 'Between the parallel lines')),
      L("The angles at C are vertical angles, so they're equal too. And the angles at A and E are equal, by another Z.",
        show(f139i['v'], 'The angles at C are vertical angles')),
      L("So the triangles are similar. Let's make the table. A B and E D are both opposite the angle at C.",
        show(t139d['line'], "Let's make the table"), show(t139d['r1'], 'A B and E D')),
      L("Now notice. A C goes with E C. So here a side matches its own continuation, on the other side of C.",
        show(t139d['r2'], 'A C goes with E C')),
      L("And B C goes with D C, its continuation too.", show(t139d['r3'], 'And B C goes with D C')),
      L("A B is four and D E is eight, so the big one is twice the small one. A C is three, so E C is three times two, "
        "six.", show(r139y, 'A B is four and D E is eight'), show(f139i['six'], 'so E C is three times two')),
      L("So on the exam, similar triangles come in three pictures. A line parallel to the base, the altitude to the "
        "hypotenuse, and the hourglass. When you see one of them, think similar triangles, and make the table.")),
]

# ---- part 4: rectangles
f139j = G('f139j', [
    ('line', [('poly', [(40, 300), (165, 300), (165, 225), (40, 225)], 'ink', 3), ('txt', 102, 324, '5', 'ink', 24), ('txt', 24, 262, '3', 'ink', 24),
              ('poly', [(220, 300), (470, 300), (470, 150), (220, 150)], 'ink', 3), ('txt', 345, 324, '10', 'ink', 24), ('txt', 200, 225, '6', 'ink', 24)]),
    ('no', [('poly', [(220, 300), (470, 300), (470, 75), (220, 75)], 'red', 3, True), ('txt', 345, 60, '10 by 9: not similar', 'red', 22)]),
], vb='10 40 480 300', w=600, title='Rectangles 5 by 3 and 10 by 6')
r139z1 = H36('r139z1', '$5 \\to 10$: $\\times 2$')
r139z2 = H36('r139z2', '$3 \\to 6$: $\\times 2$')
r139z3 = H36('r139z3', '$\\frac{5}{3} = \\frac{10}{6}$')
r139z4 = H36('r139z4', 'lengths $1 : 2$, areas $1 : 4$')

_RA, _RB, _RC, _RD = (40, 300), (340, 300), (340, 100), (40, 100)
_RP, _RQ, _RR = (265, 300), (265, 150), (40, 150)
f139k = G('f139k', [
    ('line', [('poly', [_RA, _RB, _RC, _RD], 'ink', 3), sg(_RA, _RC, 'ink', 2.5), ('txt', 190, 346, '12', 'ink', 24),
              ('txt', 362, 200, '8', 'ink', 24), nm(_RA, 'A', (190, 200), 22), nm(_RB, 'B', (190, 200), 22),
              nm(_RC, 'C', (190, 200), 22), nm(_RD, 'D', (190, 200), 22)]),
    ('small', [('tint', [_RA, _RP, _RQ, _RR], 'teal'), ('poly', [_RA, _RP, _RQ, _RR], 'teal', 4), ('dot', _RQ[0], _RQ[1]),
               at(_RP, 'P', 0, 24, italic=True), at(_RR, 'R', -20, 0, italic=True), ('txt', 152, 286, '9', 'teal', 26)]),
    ('w', [('txt', 58, 225, '6', 'teal', 28)]),
    ('left', [sg(_RR, _RD, 'orange', 7), ('txt', 20, 125, '2', 'orange', 26), sg(_RP, _RB, 'orange', 7), ('txt', 302, 286, '3', 'orange', 26)]),
], vb='0 60 400 300', w=500, title='A rectangle with its corner on the diagonal')
r139z5 = H36('r139z5', '$\\frac{8}{12} = \\frac{2}{3}$')
r139z6 = H36('r139z6', '$AR = \\frac{2}{3} \\cdot 9 = 6$')
r139z7 = H36('r139z7', '$RD = 8 - 6 = 2$')
r139z7b = H36('r139z7b', '$PB = 12 - 9 = 3$')
r139z8 = H36('r139z8', '$\\frac{2}{6} = \\frac{3}{9} = \\frac{1}{3}$')
z139a = I('z139a', 'Two equal angles $\\to$ similar triangles', size=28)
z139b = I('z139b', 'Match the sides opposite equal angles: the small-big table', size=28)
z139c = I('z139c', 'Parallel to the base $\\cdot$ altitude to the hypotenuse $\\cdot$ hourglass', size=28)
z139d = I('z139d', 'Rectangles: both sides, one factor', size=28)

_S139 += [
    S('Rectangles',
      L("Now similarity in another shape that isn't regular, the rectangle."),
      L("To know that two rectangles are similar, we must check both ratios. The ratio of the lengths, and the ratio of "
        "the widths."),
      L("Here's a rectangle five by three, and a rectangle ten by six.", show(f139j['line'], "Here's a rectangle five by three")),
      L("Five to ten is times two, and three to six is times two. The same factor, so they're similar.",
        show(r139z1, 'Five to ten is times two'), show(r139z2, 'three to six is times two')),
      L("But if the length grows two times and the width three times, it's not the same shape. A rectangle ten by nine "
        "isn't similar to them.", show(f139j['no'], 'A rectangle ten by nine')),
      L("There's another way to check. Compare the length to the width inside each rectangle. Five over three, and ten "
        "over six, which is also five over three.", show(r139z3, 'Five over three, and ten')),
      L("And since the linear ratio is one to two, the areas are one to four.", show(r139z4, 'the areas are one to four'))),
    S('A rectangle on the diagonal',
      L("On the exam, similar rectangles usually come in this picture. A rectangle with its diagonal, and a smaller "
        "rectangle whose corner sits on that diagonal.", show(f139k['line'], 'A rectangle with its diagonal'),
        show(f139k['small'], 'a smaller rectangle whose corner')),
      L("In this picture the two rectangles are similar. We can prove it, but we won't. Let's see how we use it."),
      L("The big rectangle is twelve by eight. The small one has length A P, nine. What is its width, A R?"),
      L("The width over the length is the same in both. In the big one, it's eight over twelve, two thirds.",
        show(r139z5, 'eight over twelve, two thirds')),
      L("So A R is two thirds of nine. A third of nine is three, so two thirds is six.", show(r139z6, 'So A R is two thirds'),
        show(f139k['w'], 'so two thirds is six')),
      L("And the leftover pieces keep the ratio too. The top piece, R D, is eight minus six, two. The piece on the "
        "right, P B, is twelve minus nine, three.", show(f139k['left'], 'The top piece'), show(r139z7, 'eight minus six'), show(r139z7b, 'twelve minus nine')),
      L("Two over six is a third, and three over nine is a third. The same ratio.", show(r139z8, 'Two over six is a third')),
      L("So when you see a rectangle inside a rectangle, with its corner on the big diagonal, think similar rectangles.")),
    S('Recap',
      L("Let's sum up this lesson."),
      L("Two equal angles are enough for similar triangles.", show(z139a, 'Two equal angles')),
      L("We match the sides by the angles they're opposite, and we write them in the small-big table.",
        show(z139b, 'We match the sides')),
      L("On the exam we usually see three pictures. A line parallel to the base, the altitude to the hypotenuse, and the "
        "hourglass.", show(z139c, 'three pictures')),
      L("Rectangles are similar when both sides grow by the same factor.", show(z139d, 'Rectangles are similar')),
      L("In about nine questions out of ten, similarity is about triangles or rectangles, and mostly triangles. There "
        "are two more ways to prove similar triangles, with three sides, or two sides and the angle between them. You'll "
        "rarely need them."),
      L("Take a moment to memorize the three pictures, and I'll see you in the next video.")),
]
video('geo-139', 'lesson', slides=_S139)
MORE_SPLITS = [('geo-139', 'Similar Triangles and Rectangles', [
    (1, None),
    (7, "Let's continue with the pictures of similar triangles on the exam."),
    (9, "Let's continue with two more pictures."),
    (12, "Let's continue with rectangles."),
])]


# =================================================================================================================
# solve-geo36-g140 - DE parallel to BC, AD 4, DB 3: triangle ADE : trapezoid DBCE
# Hebrew geo 7705-7743 (AD 2, DB 1, dark : white): "the common mistake: the linear ratio is NOT 2 : 1, DB is not a side of
# the triangle at all"; check which angle each side is opposite (her orange and green angles) -> AD goes with the WHOLE
# AB -> 2 : 3 -> 4 : 9 -> the trapezoid 9 - 4 = 5 -> 4 : 5. English: 4 : 7 -> 16 : 49 -> 33 -> 16 : 33. One method, as
# hers. R37: the first question after geo-139 part 2 (parallel to the base) - applied slowly, with "like in the lesson".
# Traps at their steps: 4 : 3 (choice 2), 16 : 49 (choice 1), 4 : 7 (choice 4).
# V3: the copy's parallel arrows, the small triangle tinted; DB red dashed (not a side), AB orange (7); the units 16 / 33.
# =================================================================================================================
_KA, _KB, _KC, _KD, _KE = (320, 50), (130, 300), (510, 300), (211.4, 192.9), (428.6, 192.9)
f140a = PIN(GEO('f140a', [
    ('line', [qraw('geo36-g140')]),
    ('par', [('par', _KD[0], _KD[1], _KE[0], _KE[1], 1, 'teal'), ('par', _KB[0], _KB[1], _KC[0], _KC[1], 1, 'teal')]),
    ('small', [('poly', [_KA, _KD, _KE], 'teal', 5)]),
    ('db', [sg(_KD, _KB, 'red', 7, True)]),
    ('ang', [ang(_KE, _KA, _KD, 34, 'teal'), ang(_KC, _KA, _KB, 34, 'teal')]),
    ('ab', [sg(_KA, _KB, 'orange', 6), ('txt', 196, 140, '7', 'orange', 30)]),
], vb='100 20 440 320', w=460, title='DE parallel to BC: AD 4, DB 3'))
QLEFT(f140a, 'geo36-g140')
f140b = PIN(GEO('f140b', [
    ('line', [qraw('geo36-g140')]),
    ('u', [('txt', 320, 150, '16', 'teal', 34)]),
    ('big', [('txt', 470, 110, '49', 'orange', 34)]),
    ('trap', [('tint', [_KD, _KB, _KC, _KE], 'orange'), ('txt', 320, 258, '33', 'orange', 34)]),
], vb='100 20 440 320', w=460, title='The units: 16, 49 and 33'))
QLEFT(f140b, 'geo36-g140')
# (V3 cut-out) the small triangle ADE and the big triangle ABC pulled apart, the same way up
_qA1, _qD1, _qE1 = (170, 50), (61.4, 192.9), (278.6, 192.9)
_qA2, _qB2, _qC2 = (570, 50), (380, 300), (760, 300)
f140p = PIN(GEO('f140p', [
    ('line', [('tint', [_qA1, _qD1, _qE1], 'teal'), ('poly', [_qA1, _qD1, _qE1], 'ink', 3), ('poly', [_qA2, _qB2, _qC2], 'ink', 3),
              nm(_qA1, 'A', (170, 145), 24), nm(_qD1, 'D', (170, 145), 24), nm(_qE1, 'E', (170, 145), 24),
              nm(_qA2, 'A', (570, 217), 24), nm(_qB2, 'B', (570, 217), 24), nm(_qC2, 'C', (570, 217), 24),
              ('txt', 98, 112, '4', 'teal', 28), ang(_qD1, _qA1, _qE1, 28, 'teal'), ang(_qB2, _qA2, _qC2, 34, 'teal'),
              ang(_qE1, _qA1, _qD1, 28, 'orange'), ang(_qC2, _qA2, _qB2, 34, 'orange')]),
    ('ab', [sg(_qA2, _qB2, 'orange', 6), ('txt', 452, 165, '7', 'orange', 30)]),
], vb='30 20 760 310', w=480, col=1, title='The two triangles pulled apart'))
_R(f140p, QTOP('geo36-g140') + 150, 900)
r140a = IH('r140a', '$AB = 4 + 3 = 7$', size=30)
r140b = IH('r140b', 'lengths $4 : 7$', size=30)
r140c = IH('r140c', 'areas $4^2 : 7^2 = 16 : 49$', size=30)
r140d = IH('r140d', 'trapezoid: $49 - 16 = 33$', size=30)
r140e = IH('r140e', '$16 : 33$', size=30)
FLOW([r140a, r140b], QC('geo36-g140'))
FLOW([r140c, r140d, r140e], QC('geo36-g140'))
NOFIG('solve-geo36-g140', 0, 1)

video('solve-geo36-g140', 'solution', qid='geo36-g140', slides=[
    SM('Method 1 · The math way: similar triangles', 'The whole side',
      L("Now a new question. In triangle A B C, point D lies on A B and point E lies on A C, and D E is parallel to B C. "
        "Given, A D is four and D B is three. What is the ratio of the area of triangle A D E to the area of trapezoid "
        "D B C E?", pt('stem', 'Now a new question', 'hl', 12.0), show(f140a['line'], 'Now a new question'),
        voice='calm', pause=0.5),
      L("So we compare the small triangle at the top with the trapezoid below it. Careful, the second shape isn't the "
        "big triangle. It's what's left of it."),
      L("Like in the lesson, D E is parallel to the base. So the small triangle, A D E, is similar to the big triangle, "
        "A B C.", show(f140a['par'], 'D E is parallel to the base'), show(f140a['small'], 'So the small triangle')),
      L("Now the common mistake. A lot of students say the linear ratio is four to three. But three is D B, and D B isn't "
        "a side of either triangle. It's a side of the trapezoid.", show(f140a['db'], 'But three is D B')),
      L("Four to three is choice number two, and it's a trap.", mk('cross', 'choice 2', 'Four to three is choice number two')),
      L("So we match by the angles. A D is opposite the angle at E. In the big triangle, the matching angle is at C. "
        "The side opposite it is the whole side, A B.", show(f140a['ang'], 'A D is opposite the angle at E'),
        show(f140a['ab'], 'the whole side, A B'), show(f140p['line'], 'So we match by the angles')),
      L("A B is four plus three, seven. So the linear ratio, small to big, is four to seven.",
        show(r140a, 'A B is four plus three'), show(f140p['ab'], 'A B is four plus three'), show(r140b, 'is four to seven'))),
    SM('Method 1 · The math way: similar triangles', 'Square it, then subtract',
      L("Now the areas. The area ratio is the linear ratio squared. Four squared is sixteen, and seven squared is "
        "forty-nine.", show(f140b['line'], 'Now the areas'), show(r140c, 'Four squared is sixteen')),
      L("Careful, sixteen to forty-nine isn't our answer yet. That's the small triangle against the whole big triangle. "
        "It's choice number one, and it's a trap.", mk('cross', 'choice 1', "It's choice number one")),
      L("So let's count in ratio units. The small triangle is sixteen units, and the whole big triangle is forty-nine "
        "units.", show(f140b['u'], 'The small triangle is sixteen units'), show(f140b['big'], 'the whole big triangle is forty-nine')),
      L("The trapezoid is the big triangle minus the small one. Forty-nine minus sixteen is thirty-three units.",
        show(f140b['trap'], 'The trapezoid is the big triangle'), show(r140d, 'Forty-nine minus sixteen')),
      L("So the small triangle to the trapezoid is sixteen to thirty-three.", show(r140e, 'is sixteen to thirty-three')),
      L("And four to seven, choice number four, forgot to square. Choice number three is our answer, and I'll see you "
        "in the next question.", mk('cross', 'choice 4', 'forgot to square'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-q-r26-t36-01 - BD : DC = 2 : 3, the whole triangle 40: triangle ABD (same height, NOT similar)
# No Hebrew source (an English addition, kept): the contrast with similarity - the two triangles are not similar, so the
# ratio is NOT squared; they share the height, so the areas follow the bases (topic 31 reminder, solve-geo31-g038).
# Taught with one number check (height 10: areas 10 and 15). Ratio units: 5 units = 40 -> 8 -> 16.
# Traps: 6.4 (squared, choice 2) and 24 (the other triangle, choice 3).
# V3: the height teal; BD teal (2), DC orange (3); the units in each triangle; 16 written.
# =================================================================================================================
_JA, _JB, _JC, _JD = (180, 60), (110, 300), (530, 300), (278, 300)
f01a = PIN(GEO('f01a', [
    ('line', [qraw('q-r26-t36-01')]),
    ('angs', [ang(_JB, _JA, _JC, 26, 'teal'), ang(_JC, _JA, _JB, 40, 'orange')]),
    ('h', [sg(_JA, (180, 300), 'teal', 6), ('txt', 196, 200, 'h', 'teal', 30, True)]),
    ('bases', [sg(_JB, _JD, 'teal', 8), ('txt', 194, 330, '2', 'teal', 30), sg(_JD, _JC, 'orange', 8), ('txt', 404, 330, '3', 'orange', 30)]),
], vb='80 20 470 330', w=460, title='D on BC: BD to DC is 2 to 3'))
QLEFT(f01a, 'q-r26-t36-01')
f01b = PIN(GEO('f01b', [
    ('line', [qraw('q-r26-t36-01')]),
    ('u', [('txt', 216, 250, '2', 'teal', 34), ('txt', 330, 250, '3', 'orange', 34)]),
    ('v', [('txt', 216, 200, '16', 'teal', 30)]),
], vb='80 20 470 330', w=460, title='Two units and three units'))
QLEFT(f01b, 'q-r26-t36-01')
r01a = IH('r01a', 'not similar: no squaring', size=30)
r01b = IH('r01b', 'area $= \\frac{\\text{base} \\cdot h}{2}$', size=30)
r01c = IH('r01c', 'same $h$: areas $2 : 3$', size=30)
r01d = IH('r01d', '$h = 10$: $\\frac{2 \\cdot 10}{2} = 10$, $\\frac{3 \\cdot 10}{2} = 15$', size=28)
r01e = IH('r01e', '$2 + 3 = 5$ units $= 40$', size=30)
r01f = IH('r01f', '$1$ unit $= 40 \\div 5 = 8$', size=30)
r01g = IH('r01g', '$ABD = 2 \\cdot 8 = 16$', size=30)
r01h = IH('r01h', 'squared: $40 \\cdot \\frac{4}{25} = 6.4$', size=30)
FLOW([r01a, r01b, r01c, r01d], QC('q-r26-t36-01'))
FLOW([r01e, r01f, r01g, r01h], QC('q-r26-t36-01'))
NOFIG('solve-q-r26-t36-01', 0, 1)

video('solve-q-r26-t36-01', 'solution', qid='q-r26-t36-01', slides=[
    SM('Method 1 · The math way: the same height', 'Similar? No',
      L("Now a new question. In triangle A B C, point D lies on B C. The ratio B D to D C is two to three. The area of "
        "triangle A B C is forty. What is the area of triangle A B D?", pt('stem', 'Now a new question', 'hl', 9.0),
        show(f01a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("So the big triangle is cut into two triangles. We need the area of the left one, A B D."),
      L("After this topic, our reflex is to square the ratio. Two to three, squared, is four to nine. But wait. Are "
        "these two triangles similar?"),
      L("Look at the angles. Triangle A B D has the angle at B. Triangle A D C has the angle at C instead, and it's a "
        "different angle. So they're not similar, and we don't square.", show(f01a['angs'], 'Look at the angles'),
        show(r01a, "So they're not similar")),
      L("But they do share something, the height. It's the same distance, from A straight down to B C.",
        show(f01a['h'], 'the height')),
      L("Remember from triangles, the area is the base times the height, divided by two. The height is the same in both. "
        "So the areas are in the ratio of the bases, two to three.", show(r01b, 'the area is the base times'),
        show(f01a['bases'], 'in the ratio of the bases'), show(r01c, 'two to three')),
      L("Let's see it in numbers. Say the height is ten. Then the areas are two times ten over two, ten, and three times "
        "ten over two, fifteen. Ten to fifteen is two to three.", show(r01d, 'Say the height is ten'))),
    SM('Method 1 · The math way: the same height', 'Ratio units',
      L("So let's count in ratio units. A B D is two units, and A D C is three units. The whole triangle is two plus "
        "three, five units.", show(f01b['line'], "let's count in ratio units"), show(f01b['u'], 'A B D is two units'),
        show(r01e, 'two plus three, five units')),
      L("Five units are forty. So one unit is forty divided by five, eight.", show(r01f, 'forty divided by five')),
      L("Triangle A B D is two units. Two times eight is sixteen.", show(r01g, 'Two times eight is sixteen'),
        show(f01b['v'], 'Two times eight')),
      L("Careful with six point four. That's what we get if we square the ratio. Four twenty-fifths of forty is six "
        "point four.", show(r01h, 'Four twenty-fifths of forty'), mk('cross', 'choice 2', 'Careful with six point four')),
      L("And twenty-four is the other triangle, A D C. It's three units times eight.", mk('cross', 'choice 3', 'And twenty-four is the other')),
      L("So when two triangles aren't similar, but they have the same height, the areas follow the bases. No squaring. "
        "Choice number one is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])


# =================================================================================================================
# solve-q-r26-t36-02 - a trapezoid with its diagonals, AB 4, DC 6, AOB = 8: the whole trapezoid
# No Hebrew source (English addition, kept): the hourglass (geo-139 part 3) gives the top and bottom triangles 4 and 9
# units; the side triangles share a height with them, so they follow OB : OD = 2 : 3 (6 units each); 25 units, 1 unit =
# 2 -> 50. The reusable fact a^2, ab, ab, b^2 after the answer (W11). Traps 26 (no side triangles) and 42 (side = top).
# V3: the copy's hourglass triangles tinted teal / orange with 4 and 9; AOD outlined with its height from A to BD; 6 and 6.
# =================================================================================================================
_TA, _TB, _TC, _TD, _TO = (210, 110), (410, 110), (470, 300), (170, 300), (314, 186)
_TF = foot(_TA, _TB, _TD)
f02a = PIN(GEO('f02a', [
    ('line', [qraw('q-r26-t36-02')]),
    ('tb', [('poly', [_TA, _TB, _TO], 'teal', 5), ('poly', [_TD, _TC, _TO], 'orange', 5)]),
    ('o', [ang(_TO, _TA, _TB, 20, 'red'), ang(_TO, _TC, _TD, 20, 'red')]),
    ('u', [('txt', 312, 140, '4', 'teal', 32), ('txt', 320, 262, '9', 'orange', 34)]),
], vb='130 60 380 290', w=460, title='The hourglass inside the trapezoid'))
QLEFT(f02a, 'q-r26-t36-02')
f02b = PIN(GEO('f02b', [
    ('line', [qraw('q-r26-t36-02'), ('txt', 312, 140, '4', 'teal', 32), ('txt', 320, 262, '9', 'orange', 34)]),
    ('side', [('poly', [_TA, _TO, _TD], 'teal', 5), ('poly', [_TA, _TO, _TB], 'teal', 3, True)]),
    ('h', [sg(_TA, _TF, 'teal', 4, True), rt(_TF, _TA, _TB, 10, 'teal')]),
    ('ob', [sg(_TO, _TB, 'orange', 7), sg(_TO, _TD, 'teal', 7)]),
    ('six', [('txt', 232, 206, '6', 'teal', 32), ('txt', 400, 206, '6', 'teal', 32)]),
], vb='130 60 380 290', w=460, title='The side triangles'))
QLEFT(f02b, 'q-r26-t36-02')
f02c = PIN(GEO('f02c', [
    ('line', [qraw('q-r26-t36-02'), ('txt', 312, 140, '4', 'teal', 32), ('txt', 320, 262, '9', 'orange', 34),
              ('txt', 232, 206, '6', 'teal', 32), ('txt', 400, 206, '6', 'teal', 32)]),
], vb='130 60 380 290', w=460, title='The four triangles in units'))
QLEFT(f02c, 'q-r26-t36-02')
r02a = IH('r02a', '$4 : 6 = 2 : 3$', size=30)
r02b = IH('r02b', 'areas $2^2 : 3^2 = 4 : 9$', size=30)
r02c = IH('r02c', '$OB : OD = 2 : 3$', size=30)
r02d = IH('r02d', '$AOB : AOD = 2 : 3$', size=30)
r02e = IH('r02e', '$4 = 2 \\cdot 2$, so $AOD = 3 \\cdot 2 = 6$', size=30)
r02f = IH('r02f', '$BOC = 6$ too', size=30)
r02g = IH('r02g', '$4 + 6 + 6 + 9 = 25$ units', size=30)
r02h = IH('r02h', '$4$ units $= 8$, $1$ unit $= 2$', size=30)
r02i = IH('r02i', '$25 \\cdot 2 = 50$', size=30)
r02j = IH('r02j', '$a^2$, $ab$, $ab$, $b^2$', size=30)
FLOW([r02a, r02b], QC('q-r26-t36-02'))
FLOW([r02c, r02d, r02e, r02f, r02g], QC('q-r26-t36-02'))
FLOW([r02h, r02i, r02j], QC('q-r26-t36-02'))
NOFIG('solve-q-r26-t36-02', 0, 1, 2)

video('solve-q-r26-t36-02', 'solution', qid='q-r26-t36-02', slides=[
    SM('Method 1 · The math way: ratio units', 'The hourglass',
      L("Now a new question. A B C D is a trapezoid with A B parallel to D C. Its diagonals meet at O. Given, A B is "
        "four and D C is six. The area of triangle A O B is eight. What is the area of the trapezoid?",
        pt('stem', 'Now a new question', 'hl', 11.0), show(f02a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("So we know one small triangle, and we need the whole trapezoid. The diagonals cut the trapezoid into four "
        "triangles."),
      L("Look at the top triangle, A O B, and the bottom one, C O D. A B is parallel to D C, so this is an hourglass, "
        "like in the lesson.", show(f02a['tb'], 'Look at the top triangle')),
      L("So the two triangles are similar. A B matches D C, because both are opposite the vertical angles at O. Four "
        "to six is two to three.", show(f02a['o'], 'the vertical angles at O'), show(r02a, 'Four to six is two to three')),
      L("The area ratio is the square. Two squared is four, and three squared is nine. So the top triangle is four "
        "units, and the bottom one is nine units.", show(r02b, 'Two squared is four'), show(f02a['u'], 'So the top triangle is four'))),
    SM('Method 1 · The math way: ratio units', 'The side triangles',
      L("Now the triangles on the sides. Look at A O D and A O B. They're not similar. But they have the same height, "
        "from A down to the diagonal B D.", show(f02b['line'], 'Now the triangles on the sides'), show(f02b['side'], 'Look at A O D'),
        show(f02b['h'], 'the same height')),
      L("So their areas follow their bases on B D. The bases are O B and O D.", show(f02b['ob'], 'The bases are O B and O D')),
      L("O B is in the top triangle, and O D is in the bottom one. In the hourglass, they're matching sides. So O B to "
        "O D is two to three, like A B to D C.", show(r02c, 'So O B to O D')),
      L("So A O B to A O D is two to three as well. A O B is four units, and four is two times two. So A O D is three "
        "times two, six units.", show(r02d, 'So A O B to A O D'), show(r02e, 'four is two times two')),
      L("The other side triangle, B O C, works the same way, from C. It's also six units.", show(r02f, "It's also six units"),
        show(f02b['six'], 'The other side triangle')),
      L("In all, four plus six plus six plus nine is twenty-five units.", show(r02g, 'four plus six plus six'))),
    SM('Method 1 · The math way: ratio units', 'Units to square centimeters',
      L("The top triangle is four units, and its area is eight. So one unit is eight divided by four, two.",
        show(f02c['line'], 'The top triangle is four units'), show(r02h, 'eight divided by four')),
      L("The trapezoid is twenty-five units. Twenty-five times two is fifty.", show(r02i, 'Twenty-five times two')),
      L("Careful with twenty-six. That's only the top and the bottom, four plus nine units, times two. It forgets the "
        "side triangles.", mk('cross', 'choice 1', 'Careful with twenty-six')),
      L("And forty-two treats each side triangle as four units, like the top one.", mk('cross', 'choice 2', 'And forty-two')),
      L("Here's one fact worth remembering. When the bases are a and b, the four triangles are always a squared, a times b, a "
        "times b, and b squared. Here that's four, six, six and nine.", show(r02j, "Here's one fact worth remembering")),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# geo-141 (lesson) - Similar solids
# Hebrew geo 7753-7817: areas were squared, in 3D we talk about volumes - the volume ratio = the linear ratio to the
# power of three; similar solids = ALL matching edges in one ratio (an edge in a cube / box, the height and the radius in a
# cylinder / cone); the cube is regular, all cubes are similar: edge 1 -> 2, count 8 small cubes (areas 1 : 4, volumes
# 1 : 8); cylinders (and cones) are similar ONLY if the radii and the heights share the ratio (2 : 3 and 4 : 6 -> 4 : 9,
# 8 : 27); "very important: check that they really are similar".
# English numbers (kept): the cube 1 -> 4 (16 per layer, 64), cylinders radii 2 : 4 and heights 4 : 8 (1 : 4, 1 : 8).
# Kept English additions: the surface is still an area (squared); all spheres are similar; the half-height cone glass
# holds 1/8 (with WHY it is similar: the water surface is parallel to the top). Added: why the power of three (three
# directions), and the non-example (only the radius doubled: not similar - its rule comes in geo-143).
# Visuals: the small cube and the big one, the bottom layer of 16 tinted, then all 64; the two cylinders with their radii
# teal and heights orange; the cone glass with the water tinted and the heights 1 and 2.
# =================================================================================================================
_lay = [(i, 0, k) for i in range(4) for k in range(4)]
_all = [(i, j, k) for i in range(4) for j in range(4) for k in range(4)]
_TL = ('#bfe6e1', '#d5f1ed', '#a9dbd5')
f141a = G('f141a', [
    ('line', unit_cubes([(0, 0, 0)], 30, 300, 40) + box_el(boxpts(150, 300, 160, 160, 160)) +
             [('txt', 50, 324, '1', 'ink', 24), ('txt', 230, 324, '4', 'ink', 26)]),
    ('layer', unit_cubes(_lay, 150, 300, 40, fills={c: _TL for c in _lay})),
    ('all', unit_cubes(_all, 150, 300, 40, fills={c: _TL for c in _lay})),
], vb='10 60 410 280', w=470, title='A cube with edge 1 and a cube with edge 4')
r141a = H36('r141a', 'length $k$, area $k^2$, volume $k^3$')
r141b = H36('r141b', 'one layer: $4 \\cdot 4 = 16$')
r141c = H36('r141c', '$16 \\cdot 4 = 64$')
r141d = H36('r141d', 'lengths $1 : 4$')
r141e = H36('r141e', 'areas $1^2 : 4^2 = 1 : 16$')
r141f = H36('r141f', 'volumes $1^3 : 4^3 = 1 : 64$')

f141b = G('f141b', [
    ('line', cyl_el(80, 300, 40, 80, 12) + cyl_el(280, 300, 80, 160, 24)),
    ('r', [sg((80, 300), (120, 300), 'teal', 5), ('txt', 100, 328, '2', 'teal', 26),
           sg((280, 300), (360, 300), 'teal', 5), ('txt', 320, 334, '4', 'teal', 26)]),
    ('h', [sg((136, 300), (136, 220), 'orange', 5, True), ('txt', 154, 260, '4', 'orange', 26),
           sg((376, 300), (376, 140), 'orange', 5, True), ('txt', 396, 220, '8', 'orange', 26)]),
], vb='20 100 400 250', w=470, title='Two cylinders: radii 2 and 4, heights 4 and 8')
r141g = H36('r141g', 'radii $2 : 4 = 1 : 2$')
r141h = H36('r141h', 'heights $4 : 8 = 1 : 2$')
r141i = H36('r141i', 'areas $1 : 4$')
r141i2 = H36('r141i2', 'volumes $1^3 : 2^3 = 1 : 8$')

f141c = G('f141c', [
    ('line', [sg((200, 320), (90, 100)), sg((200, 320), (310, 100)), _ell(200, 100, 110, 25)]),
    ('water', [('tint', [(200, 320), (145, 210), (255, 210)], 'teal'), _ell(200, 210, 55, 12.5, 'full', GTEAL, 3, False, GBAND)]),
    ('half', [sg((350, 320), (350, 210), 'teal', 5), ('txt', 330, 265, '1', 'teal', 28),
              sg((380, 320), (380, 100), 'orange', 5), ('txt', 402, 210, '2', 'orange', 28)]),
], vb='70 70 360 270', w=440, title='A cone glass filled to half its height')
r141j = H36('r141j', 'lengths $1 : 2$')
r141k = H36('r141k', 'volumes $1^3 : 2^3 = 1 : 8$')
z141a = I('z141a', 'Lines $k$ $\\cdot$ areas $k^2$ $\\cdot$ volumes $k^3$', size=30)
z141b = I('z141b', 'Similar solids: every matching edge, the same ratio', size=30)
z141c = I('z141c', 'Cylinder or cone: check the radius AND the height', size=30)

video('geo-141', 'lesson', slides=[
    S('Similar Solids',
      L("Welcome back. Now similarity in three-dimensional shapes, solids."),
      L("Until now we talked about lengths and areas. An area is two-dimensional, so the area ratio is the linear ratio, "
        "squared."),
      L("A cube, a box and a cylinder are three-dimensional. So now we'll talk about volumes.")),
    S('Volume: to the power of three',
      L("In similar solids, the volume ratio is the linear ratio to the power of three."),
      L("So lengths keep the ratio, areas get it squared, and volumes get it to the power of three. If the ratio is k, "
        "that's k, k squared and k to the power of three.", show(r141a, 'If the ratio is k')),
      L("And the surface area of a solid? It's still an area, so it gets the ratio squared."),
      L("Now, this is important. Two solids are similar only when all their matching edges have the same ratio."),
      L("In a cube or a box, these are the edges. In a cylinder or a cone, it's the radius and the height."),
      L("So a box is similar to another box only if all three of its edges grow by the same factor. The length, the "
        "width and the height."),
      L("And spheres? Like circles, every sphere has the same shape. So all spheres are similar.")),
    S('Cubes: count them',
      L("Let's start with a regular solid, the cube. All the cubes in the world are similar, just like all the squares."),
      L("Here's a small cube, and a big cube whose edge is four times as long. So the linear ratio is one to four.",
        show(f141a['line'], "Here's a small cube"), show(r141d, 'So the linear ratio is one to four')),
      L("How many small cubes fit inside the big one? Let's count. One layer is four by four, sixteen cubes.",
        show(f141a['layer'], 'One layer is four by four'), show(r141b, 'One layer is four by four')),
      L("And there are four layers. Sixteen times four is sixty-four.", show(f141a['all'], 'And there are four layers'),
        show(r141c, 'Sixteen times four')),
      L("So the areas are one squared to four squared, one to sixteen. And the volumes are one to the power of three, to "
        "four to the power of three, one to sixty-four.", show(r141e, 'So the areas are one squared'),
        show(r141f, 'And the volumes are one')),
      L("Why to the power of three? The cube grows four times in its length, four times in its width and four times in "
        "its height. Four times four times four is sixty-four.")),
    S('Cylinders: check both',
      L("The cube was easy, because it's regular. A cylinder isn't regular, so two cylinders aren't always similar."),
      L("Two cylinders are similar only if their radii and their heights have the same ratio. The same goes for cones."),
      L("Here the radii are two and four. Two to four is one to two.", show(f141b['line'], 'Here the radii are two and four'),
        show(f141b['r'], 'Here the radii'), show(r141g, 'Two to four is one to two')),
      L("The heights are four and eight. Four to eight is also one to two. The same ratio, so these cylinders are "
        "similar.", show(f141b['h'], 'The heights are four and eight'), show(r141h, 'Four to eight is also')),
      L("So their areas are one to four, and their volumes are one to the power of three to two to the power of three. "
        "That's one to eight.", show(r141i, 'So their areas are one to four'), show(r141i2, "That's one to eight")),
      L("Careful. If only the radius doubled, and the height stayed the same, they wouldn't be similar. Then the power "
        "of three doesn't work. We'll see that case in the next lesson.")),
    S('Half the height of a cone',
      L("Here's a famous trap. A glass shaped like a cone stands on its point. We fill it with water up to half its "
        "height.", show(f141c['line'], 'A glass shaped like a cone'), show(f141c['water'], 'We fill it with water')),
      L("Is the glass half full? It looks like it, but no."),
      L("The water is a small cone. Its surface is parallel to the top of the glass, like a line parallel to the base. "
        "So the water cone is similar to the glass."),
      L("Its height is half the glass's height, so the linear ratio is one to two.", show(f141c['half'], 'Its height is half'),
        show(r141j, 'so the linear ratio is one to two')),
      L("The volumes are one to the power of three to two to the power of three, one to eight. So the water fills only "
        "one eighth of the glass.", show(r141k, 'The volumes are one')),
      L("The other seven eighths are in the wide part at the top.")),
    S('Recap',
      L("So let's sum up. In similar solids, lengths keep the ratio, areas get it squared, and volumes get it to the "
        "power of three.", show(z141a, 'In similar solids')),
      L("Solids are similar only when every matching edge has the same ratio.", show(z141b, 'Solids are similar only')),
      L("In a cylinder or a cone, check both the radius and the height. Cubes and spheres are always similar.",
        show(z141c, 'In a cylinder or a cone')),
      L("Take a moment to memorize this, and I'll see you in the next video.")),
])


# =================================================================================================================
# solve-geo36-g142 - a cube box filled with cube blocks; one face is 36 times a block's face
# Hebrew geo 7819-7849 (9 times -> 27): "they mix us up a little: not an edge but an area, and at the end they ask about
# volumes - I need an in-between step": cubes are similar; area 1 : 9 -> the root -> edges 1 : 3 -> to the power of three
# -> 1 : 27; "if the small cube's volume is 1, the big one's is 27". English: 36 -> 6 -> 216. Her method kept (method 1).
# Method 2 (R30, from the givens): the face of the box is a 6 by 6 grid of block faces -> 36 blocks in a layer, 6 layers
# (the course's "you can see it" check, now a method). Traps: 36 (the area ratio) and 1296 (36 squared) at their steps.
# V3: the box's front face shaded, then the 6 by 6 grid of block faces teal; the edge 6 orange.
# =================================================================================================================
_gx = [300 + 27.5 * k for k in range(1, 6)]
f142a = PIN(GEO('f142a', [
    ('line', [qraw('geo36-g142')]),
    ('faces', [('tint', [(150, 257.5), (177.5, 257.5), (177.5, 285), (150, 285)], 'teal'), ('poly', [(150, 257.5), (177.5, 257.5), (177.5, 285), (150, 285)], 'teal', 4),
               ('tint', [(300, 120), (465, 120), (465, 285), (300, 285)], 'orange'), ('poly', [(300, 120), (465, 120), (465, 285), (300, 285)], 'orange', 4)]),
    ('e', [('txt', 136, 272, '1', 'teal', 28), ('txt', 282, 205, '6', 'orange', 32)]),
], vb='120 40 450 310', w=460, title='The block and the box'))
QLEFT(f142a, 'geo36-g142')
f142b = PIN(GEO('f142b', [
    ('line', [qraw('geo36-g142')]),
    ('grid', [sg((x, 120), (x, 285), 'teal', 2) for x in _gx] + [sg((300, 285 - (x - 300)), (465, 285 - (x - 300)), 'teal', 2) for x in _gx]),
    ('six', [('txt', 382, 335, '6 blocks', 'teal', 28)]),
], vb='120 40 450 310', w=460, title='The face of the box: 6 by 6 block faces'))
QLEFT(f142b, 'geo36-g142')
r142a = IH('r142a', 'areas $1 : 36$', size=30)
r142b = IH('r142b', 'edges $1 : \\sqrt{36} = 1 : 6$', size=30)
r142c = IH('r142c', 'volumes $1^3 : 6^3$', size=30)
r142d = IH('r142d', '$6 \\cdot 6 = 36$', size=30)
r142d2 = IH('r142d2', '$36 \\cdot 6 = 180 + 36 = 216$', size=30)
r142e = IH('r142e', '$36^2 = 1296$: no', size=30)
r142f = IH('r142f', 'face: $36 = 6 \\cdot 6$', size=30)
r142g = IH('r142g', 'one layer: $36$ blocks', size=30)
r142h = IH('r142h', '$6$ layers: $36 \\cdot 6 = 216$', size=30)
FLOW([r142a, r142b, r142c, r142d, r142d2, r142e], QC2('geo36-g142'))
FLOW([r142f, r142g, r142h], QC('geo36-g142'))
NOFIG('solve-geo36-g142', 0, 1)

video('solve-geo36-g142', 'solution', qid='geo36-g142', slides=[
    SM('Method 1 · The math way: similar solids', 'Area, length, volume',
      L("Now a new question. A large cube-shaped box is filled completely with small cubic blocks. The area of one face "
        "of the box is thirty-six times the area of one face of a block. How many blocks fill the box?",
        pt('stem', 'Now a new question', 'hl', 11.0), show(f142a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("They mix us up a little. We're given an area, not an edge. And they ask about volumes, because the number of "
        "blocks is the big volume divided by the small one. So we need a step in between. We'll solve it in two "
        "different ways."),
      L("Let's start with the math way. The box and the blocks are cubes, so they're similar. The faces give us the "
        "area ratio, one to thirty-six.", show(f142a['faces'], 'The faces give us the area ratio'), show(r142a, 'one to thirty-six')),
      L("Like in the lesson, to go from areas back to lengths, we take the square root. The root of thirty-six is six. "
        "So the edges are one to six.", show(r142b, 'The root of thirty-six is six'), show(f142a['e'], 'So the edges are one to six')),
      L("Now from lengths to volumes, we take the power of three. So the volumes are one to the power of three, to six "
        "to the power of three.", show(r142c, 'So the volumes are one')),
      L("Six times six is thirty-six. Now thirty-six times six. Thirty times six is a hundred eighty, and six times six "
        "is thirty-six. Together, that's two hundred sixteen.", show(r142d, 'Six times six is thirty-six'),
        show(r142d2, "Together, that's two hundred sixteen")),
      L("So if a block is one unit, the box is two hundred sixteen units. Two hundred sixteen blocks fill the box."),
      L("Careful with thirty-six. That's the area ratio, not the volume. And one thousand two hundred ninety-six is "
        "thirty-six squared. It squares the area ratio, instead of going back to the edge.",
        mk('cross', 'choice 1', 'Careful with thirty-six'), show(r142e, 'one thousand two hundred ninety-six'),
        mk('cross', 'choice 3', 'It squares the area ratio'))),
    SM('Method 2 · Understanding: count the layers', 'Count the layers',
      L("Now by understanding, by counting. Look at one face of the box. It's thirty-six times a block's face.",
        show(f142b['line'], 'Now by understanding')),
      L("Thirty-six is six times six. So the face of the box is a square of six rows of six block faces.",
        show(r142f, 'Thirty-six is six times six'), show(f142b['grid'], 'six rows of six')),
      L("So six blocks fit along each edge. The bottom layer of the box holds six times six, thirty-six blocks.",
        show(f142b['six'], 'So six blocks fit along'), show(r142g, 'The bottom layer')),
      L("The box is a cube, so it's six blocks high. That's six layers. Thirty-six times six is two hundred sixteen.",
        show(r142h, 'Thirty-six times six')),
      L("Two hundred sixteen blocks again. Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# geo-143 (lesson, 2 parts) - Volume changes
# Hebrew geo 7851-7984: "how many times did the volume grow or shrink - mostly by understanding, without the formula";
# the cube edge x 3: count (9 in a floor, 3 floors = 27) and the formula (3a)^3 = 27 a^3 "the 3 goes to the power of
# three"; a cylinder or a cone: "check what changed and by how much" - the height only: directly (a can on a can, "easy to
# see"); the radius: by the square of the change, "hard to see, the old cylinder is inside the wider one, so let's see it
# in the formula" pi (3r)^2 h = 9 pi r^2 h; the cone with the height x 3 (the 3 cancels with the 3 of the formula);
# recap: a cube to the power of three; a cylinder / cone: the height the same way, the radius squared.
# English numbers (kept): the edge x 5 (25 a layer, 125), the radius x 2 (4), the cone height x 5. Kept English
# additions: both change -> multiply (x2 and x5 -> 20; half and x3 -> 3/4); factor vs percent (x4 = +300%, x3/4 = -25%).
# EXAM GAP restored (reviews/exam-coverage-geometry.md D2, ~/Downloads/Exam-coverage-audit.md 10; real exam 2026 spring
# q1_20: the volume of a cube x 2 -> the surface?): BACKWARDS - the volume x 8 -> the edge x 2 -> the surface x 4, then
# the volume x 3 -> the edge x the cube root of 3 -> the surface x (the cube root of 3) squared = the cube root of 9; why
# not x 6 (all six faces change alike). Reminders (R29): the volume follows the height and the radius is squared in the
# base (topic 35 geo-120 part 1), the cube root (topic 9 roots), percent -> factor (topic 23).
# Visuals: the small cube and the 5 x 5 x 5 cube (a layer tinted, then all); the cans stacked; the wide cylinder drawn
# around the narrow one (orange); every formula step its own hand row.
# =================================================================================================================
_lay5 = [(i, 0, k) for i in range(5) for k in range(5)]
_all5 = [(i, j, k) for i in range(5) for j in range(5) for k in range(5)]
f143a = G('f143a', [
    ('line', unit_cubes([(0, 0, 0)], 30, 300, 30) + box_el(boxpts(120, 300, 150, 150, 150)) +
             [('txt', 45, 324, '1', 'ink', 24), ('txt', 195, 324, '5', 'ink', 26)]),
    ('layer', unit_cubes(_lay5, 120, 300, 30, fills={c: _TL for c in _lay5})),
    ('all', unit_cubes(_all5, 120, 300, 30, fills={c: _TL for c in _lay5})),
], vb='10 80 360 260', w=440, title='A cube with edge 1 and a cube with edge 5')
r143a = H36('r143a', 'one layer: $5 \\cdot 5 = 25$')
r143b = H36('r143b', '$25 \\cdot 5 = 125$')
r143c = H36('r143c', '$V = a^3$')
r143d = H36('r143d', 'new: $(5a)^3$')
r143e = H36('r143e', '$= 5^3 \\cdot a^3 = 125a^3$')
r143f = H36('r143f', 'edge $\\times n$ $\\to$ volume $\\times n^3$')

f143b = G('f143b', [
    ('line', cyl_el(120, 300, 50, 80, 15)),
    ('two', cyl_el(120, 220, 50, 80, 15)),
    ('three', cyl_el(120, 140, 50, 80, 15)),
], vb='50 40 150 290', w=300, title='Soda cans stacked')
r143g = H36('r143g', 'height $\\times 2$ $\\to$ volume $\\times 2$')
r143h = H36('r143h', 'height $\\times 5$ $\\to$ volume $\\times 5$')

f143c = G('f143c', [
    ('line', cyl_el(200, 300, 40, 130, 12)),
    ('wide', [_ell(200, 170, 80, 24, 'full', GORANGE, 3), _ell(200, 300, 80, 24, 'front', GORANGE, 3),
              sg((120, 170), (120, 300), 'orange', 3), sg((280, 170), (280, 300), 'orange', 3),
              sg((200, 300), (240, 300), 'teal', 5), ('txt', 220, 286, 'r', 'teal', 26, True),
              sg((200, 340), (280, 340), 'orange', 5), ('txt', 240, 360, '2r', 'orange', 26, True)]),
], vb='100 130 200 245', w=380, title='The radius doubled, the height the same')
r143i = H36('r143i', 'radius $\\times 2$ $\\to$ volume $\\times 4$')
r143j = H36('r143j', 'radius $\\times 3$ $\\to$ volume $\\times 9$')
r143k = H36('r143k', '$V = πr^2h$')
r143l = H36('r143l', 'new: $π(2r)^2h$')
r143m = H36('r143m', '$= π \\cdot 4r^2 \\cdot h = 4πr^2h$')
r143n = H36('r143n', 'cone: $V = \\frac{πr^2h}{3}$')
r143o = H36('r143o', 'new: $\\frac{πr^2 \\cdot 5h}{3} = 5 \\cdot \\frac{πr^2h}{3}$')

r143p = H36('r143p', 'radius $\\times 2$: $\\times 4$')
r143p2 = H36('r143p2', 'height $\\times 5$: $\\times 5$')
r143q = H36('r143q', '$4 \\cdot 5 = 20$')
r143r = H36('r143r', 'radius $\\times \\frac{1}{2}$: $\\times \\frac{1}{4}$')
r143r2 = H36('r143r2', 'height $\\times 3$: $\\times 3$')
r143s = H36('r143s', '$\\frac{1}{4} \\cdot 3 = \\frac{3}{4}$')
r143t = H36('r143t', 'both $\\times k$: $k^2 \\cdot k = k^3$')
r143u = H36('r143u', 'volume $\\times 8$: $2 \\cdot 2 \\cdot 2 = 8$')
r143v = H36('r143v', 'edge $\\times 2$')
r143w = H36('r143w', 'surface $\\times 2^2 = 4$')
r143x = H36('r143x', 'volume $\\times 3$')
r143x2 = I('r143x2', 'edge $\\times \\sqrt[3]{3}$', size=34, col=1)
r143y = I('r143y', 'surface $\\times \\left(\\sqrt[3]{3}\\right)^2$', size=34, col=1)
r143y2 = I('r143y2', '$= \\sqrt[3]{9}$', size=34, col=1)
r143z = H36('r143z', '$\\times 4$: plus $300$ percent')
r143z2 = H36('r143z2', '$\\times \\frac{3}{4}$: minus $25$ percent')
z143a = I('z143a', 'Cube: edge $\\times n$ $\\to$ volume $\\times n^3$', size=30)
z143b = I('z143b', 'Cylinder, cone: height $\\times n$ $\\to$ $\\times n$ $\\cdot$ radius $\\times n$ $\\to$ $\\times n^2$', size=30)
z143c = I('z143c', 'Both change: multiply $\\cdot$ backwards: the cube root', size=30)

_S143 = [
    S('Volume Changes',
      L("Welcome back. Now questions about a change in volume. How many times did the volume grow, or shrink?"),
      L("In most of these questions, we don't need to put numbers into the formula. We just need to understand how each "
        "change affects the volume.")),
    S('A cube: the edge times five',
      L("The edge of a cube is made five times longer. How many times does the volume grow?", show(f143a['line'], 'The edge of a cube')),
      L("Now the length, the width and the height of the cube are each five small cubes long."),
      L("Let's count. One layer is five by five, twenty-five cubes.", show(f143a['layer'], 'One layer is five by five'),
        show(r143a, 'One layer is five by five')),
      L("And there are five layers. Twenty-five times five is a hundred twenty-five.", show(f143a['all'], 'And there are five layers'),
        show(r143b, 'Twenty-five times five')),
      L("Now let's understand why, with the formula. The volume of a cube is its edge to the power of three, a to the "
        "power of three.", show(r143c, 'The volume of a cube is')),
      L("We make the edge five times longer, five a. So the new volume is five a, to the power of three.",
        show(r143d, 'So the new volume is five a')),
      L("Each part inside the brackets gets the power of three. Five to the power of three is a hundred twenty-five, and "
        "a to the power of three stays.", show(r143e, 'Five to the power of three')),
      L("And a to the power of three is the old volume. So the volume grew a hundred twenty-five times."),
      L("So when we multiply the edge of a cube by some number, the volume is multiplied by that number to the power of "
        "three.", show(r143f, 'So when we multiply the edge'))),
    S('Only the height',
      L("A cylinder or a cone is different. The volume changes by what they changed, the radius or the height, and by "
        "how much."),
      L("Remember from the solids lesson. If only the height changes, and the radius stays, the volume changes in the "
        "same way."),
      L("Think of a soda can. Put another can on top of it. The height is twice as much, and so is the volume.",
        show(f143b['line'], 'Think of a soda can'), show(f143b['two'], 'Put another can on top'), show(r143g, 'The height is twice')),
      L("Put a third can on top. Three times the height, three times the volume.", show(f143b['three'], 'Put a third can')),
      L("So height times five gives volume times five, as long as the radius stays the same.", show(r143h, 'So height times five'))),
    S('Only the radius',
      L("Our problem is when they change the radius. When the radius changes, the volume changes by the square of the "
        "change."),
      L("Radius times two gives volume times two squared, four. Radius times three gives volume times three squared, "
        "nine.", show(r143i, 'Radius times two'), show(r143j, 'Radius times three')),
      L("Why? Here it's hard to see, because the old cylinder sits inside the wider one. So let's see it in the formula.",
        show(f143c['line'], "Here it's hard to see"), show(f143c['wide'], 'inside the wider one')),
      L("The volume of a cylinder is pi r squared, times h.", show(r143k, 'The volume of a cylinder')),
      L("The new radius is two r. So the new volume is pi, times the square of two r, times h.", show(r143l, 'The new radius is two r')),
      L("Inside the brackets, each part gets squared. Two squared is four, and r squared stays. So it's four pi r "
        "squared h.", show(r143m, 'Two squared is four')),
      L("And pi r squared h is the old volume. So the volume is four times as big. The four came from the two, squared."),
      L("Careful with the brackets. If we square only the r, we lose the four.")),
    S('A cone: the same rules',
      L("A cone works the same way. Its volume is the cylinder's volume, divided by three.", show(r143n, 'Its volume is')),
      L("Let's make its height five times bigger. The new volume is pi r squared, times five h, divided by three.",
        show(r143o, 'times five h')),
      L("We take the five out, and we get five times the old volume. The divided by three is in both volumes, so it "
        "doesn't change the factor."),
      L("So for a cone too, height times five gives volume times five. And radius times two gives volume times four.")),
    S('Both change',
      L("What if they change both? Then we multiply the two changes."),
      L("Radius times two gives times four. Height times five gives times five.", show(r143p, 'Radius times two gives'), show(r143p2, 'Height times five gives')),
      L("Four times five is twenty. So the volume is twenty times as big.", show(r143q, 'Four times five is twenty')),
      L("Another one. The radius is halved, and the height is tripled. A half squared is a quarter. So the radius gives "
        "times a quarter, and the height gives times three.", show(r143r, 'So the radius gives'), show(r143r2, 'the height gives times three')),
      L("A quarter times three is three quarters. So the cylinder is taller, but its volume is smaller. It's only three "
        "quarters of what it was.", show(r143s, 'A quarter times three')),
      L("And if both change by the same number, k? Then it's k squared, times k. That's k to the power of three, the "
        "similar solids rule again.", show(r143t, 'if both change by the same number'))),
    S('Backwards',
      L("Sometimes the exam goes backwards. It tells us how the volume changed, and asks about the edge or the surface."),
      L("Let's start with an easy one. The volume of a cube is multiplied by eight. What happens to its edge?"),
      L("The volume is the edge to the power of three. So we need a number whose power of three is eight. Two times two "
        "times two is eight.", show(r143u, 'Two times two times two')),
      L("So the edge is multiplied by two.", show(r143v, 'So the edge is multiplied by two')),
      L("And the surface? It's an area, so it gets the edge's change squared. Two squared is four. The surface is "
        "multiplied by four.", show(r143w, 'Two squared is four')),
      L("Now a harder one. The volume of a cube is multiplied by three. No whole number to the power of three gives "
        "three. So the edge is multiplied by the cube root of three.", show(r143x, 'the volume of a cube is multiplied by three'),
        show(r143x2, 'So the edge is multiplied by the cube root')),
      L("Remember from roots, the cube root of three is the number whose power of three is three."),
      L("And the surface gets the edge's change squared. That's the square of the cube root of three. We can also write it "
        "as the cube root of nine.", show(r143y, 'the square of the cube root'), show(r143y2, 'as the cube root of nine')),
      L("Careful, a lot of students multiply by six, because a cube has six faces. But all six faces change in the same "
        "way. So the whole surface changes like one face."),
      L("So from the volume back to the edge, we take the cube root. And from the edge to the surface, we square.")),
    S('A factor or a percent',
      L("One last thing. Read what they ask, a factor or a percent."),
      L("Four times the volume is the old volume, plus three more volumes. That's an increase of three hundred percent, "
        "not four hundred.", show(r143z, 'Four times the volume')),
      L("Three quarters of the volume is a decrease of one quarter. That's a decrease of twenty-five percent, not "
        "seventy-five.", show(r143z2, 'Three quarters of the volume'))),
    S('Recap',
      L("Let's sum up."),
      L("A cube, edge times n, volume times n to the power of three.", show(z143a, 'A cube, edge times n')),
      L("A cylinder or a cone, check what changed. The height changes the volume in the same way. The radius changes it "
        "by the square.", show(z143b, 'A cylinder or a cone')),
      L("If both change, we multiply. And backwards, from the volume to the edge, we take the cube root.",
        show(z143c, 'If both change, we multiply')),
      L("Take a moment to memorize this, and I'll see you in the next video.")),
]
video('geo-143', 'lesson', slides=_S143)
MORE_SPLITS += [('geo-143', 'Volume Changes', [
    (1, None),
    (5, "Let's continue with volume changes."),
])]


# =================================================================================================================
# solve-q-r26-t36-03 - each edge of a cube + 20%: the volume in percent
# No Hebrew source (English addition, kept; practice p20 is its backwards twin). Method 1: the percent -> the factor 1.2
# (topic 23 reminder) -> to the power of three (similar solids, geo-141/143) -> 1.728 -> +72.8% (the mental math split:
# 1.44 x 1 + 1.44 x 0.2). Method 2 (plugging in numbers, R15: why 10): 1000 -> 1728 (144 x 12 = 1440 + 288). The trap
# 60% (3 x 20, the gut feeling "three directions") at the start; 44% (one face) at its step.
# Board: no question figure; the working in one wide column, each row at its clause.
# =================================================================================================================
r03a = IH('r03a', 'plus $20$ percent $= \\times 1.2$', size=30)
r03b = IH('r03b', 'volume: $\\times 1.2^3$', size=30)
r03c = IH('r03c', '$12 \\cdot 12 = 144$, so $1.2^2 = 1.44$', size=30)
r03d = IH('r03d', '$1.44 \\cdot 1 = 1.44$, $1.44 \\cdot 0.2 = 0.288$', size=30)
r03e = IH('r03e', '$1.44 + 0.288 = 1.728$', size=30)
r03f = IH('r03f', '$\\times 1.728$: plus $72.8$ percent', size=30)
r03g = IH('r03g', 'edge $10$: $10^3 = 1000$', size=30)
r03h = IH('r03h', 'new edge: $10 + 2 = 12$', size=30)
r03i = IH('r03i', '$144 \\cdot 10 = 1440$, $144 \\cdot 2 = 288$', size=30)
r03j = IH('r03j', '$12^3 = 1440 + 288 = 1728$', size=30)
r03k = IH('r03k', '$1728 - 1000 = 728$', size=30)
r03l = IH('r03l', '$\\frac{728}{1000}$: $72.8$ percent', size=30)
r03m = IH('r03m', 'one face: $1.2^2 = 1.44$', size=30)
FLOW([r03a, r03b, r03c, r03d, r03e, r03f], QW('q-r26-t36-03'))
FLOW([r03g, r03h, r03i, r03j, r03k, r03l, r03m], [(430, 560, QTOP('q-r26-t36-03') + 5, 700), (1010, 560, QTOP('q-r26-t36-03') + 5, 700)])

video('solve-q-r26-t36-03', 'solution', qid='q-r26-t36-03', slides=[
    SM('Method 1 · The math way: percent to a factor', 'Percent to a factor',
      L("Now a new question. Each edge of a cube is increased by twenty percent. By what percent does the volume of the "
        "cube increase?", pt('stem', 'Now a new question', 'hl', 7.0), voice='calm', pause=0.5),
      L("So the edge grows by a percent, and we need the volume's growth, also as a percent. We'll solve it in two "
        "different ways."),
      L("A lot of students say three times twenty, sixty percent. It feels right, because a cube has three directions. "
        "But percents don't add up like that. Sixty percent is choice number one, and it's a trap.",
        mk('cross', 'choice 1', 'Sixty percent is choice number one')),
      L("Let's start with the math way. First we turn the percent into a factor. Remember from percents, plus twenty "
        "percent means times one point two.", show(r03a, 'plus twenty percent means')),
      L("The new cube is similar to the old one. So, like in the lesson, the volume gets the factor to the power of "
        "three.", show(r03b, 'the volume gets the factor')),
      L("One point two squared is one point four four, because twelve times twelve is a hundred forty-four.",
        show(r03c, 'One point two squared')),
      L("Now times one point two again. One point four four times one is one point four four. One point four four times "
        "zero point two is zero point two eight eight.", show(r03d, 'Now times one point two again')),
      L("Together, that's one point seven two eight.", show(r03e, "Together, that's")),
      L("Times one point seven two eight means the old volume, plus zero point seven two eight of it. That's an increase "
        "of seventy-two point eight percent.", show(r03f, "That's an increase of seventy-two"))),
    SM('Method 2 · Plugging in numbers', 'An edge of ten',
      L("Now let's plug in numbers. Let's take an edge of ten, because ten is easy to cube, and twenty percent of ten is "
        "easy to find. The old volume is ten to the power of three, a thousand.", show(r03g, 'The old volume is ten')),
      L("Twenty percent of ten is two, so the new edge is twelve.", show(r03h, 'so the new edge is twelve')),
      L("Twelve squared is a hundred forty-four. Now times twelve. A hundred forty-four times ten is one thousand four "
        "hundred forty, and a hundred forty-four times two is two hundred eighty-eight.", show(r03i, 'A hundred forty-four times ten')),
      L("Together, the new volume is one thousand seven hundred twenty-eight.", show(r03j, 'Together, the new volume')),
      L("The volume grew by one thousand seven hundred twenty-eight minus one thousand. That's seven hundred twenty-eight.",
        show(r03k, 'The volume grew by')),
      L("Seven hundred twenty-eight out of a thousand is seventy-two point eight percent. The same answer.",
        show(r03l, 'Seven hundred twenty-eight out of')),
      L("And forty-four percent? That's what happens to one face, one point two squared. But they asked about the "
        "volume.", show(r03m, 'And forty-four percent'), mk('cross', 'choice 2', 'And forty-four percent')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-geo36-g144 - ED parallel to AB; BD 10, DC 15, AE 4: AC
# Hebrew geo 7986-8071 (BD 2, DC 6, AE 3 -> 12): first PROVE the similarity, angle-angle ("on the exam one rule is
# enough"); then two ways: (1) the full math: opposite equal angles, x for EC, AC = x + 3; "work in a fixed order, small
# triangle over big triangle"; cross-multiply; "gather the x's on the side with more x"; and the same-triangle version
# ("swap the x and the 8, the same expression"); (2) psychometric, the parts of the sides: BD : DC = AE : EC (1 : 3), and
# "vertically" (x 1.5 from DC to EC). Her verdict ("here the psychometric way is much shorter") is not said (R16).
# English: 10, 15, 4 -> EC 6, AC 10; the across ratio = AE is two fifths of BD. R37: the first question with the
# small-big table (geo-139 part 1) - applied slowly; why the triangle value can't be used here (x in two cells).
# Traps: 6 = EC (not yet the answer, W-elaboration 8), 25 = BC.
# V3: the copy's parallel arrows, alpha teal at A and E, beta orange at B and D, the angle C red, the small triangle
# tinted; x on EC, 25 under CB; method 2: the parts BD / DC and AE / EC lit in pairs.
# =================================================================================================================
_MA, _MB, _MC, _ME, _MD = (267.5, 51.5), (424.9, 308.5), (215.1, 308.5), (246.5, 154.3), (341.0, 308.5)
f144a = PIN(GEO('f144a', [
    ('line', [qraw('geo36-g144')]),
    ('par', [('par', _ME[0], _ME[1], _MD[0], _MD[1], 1, 'teal'), ('par', _MA[0], _MA[1], _MB[0], _MB[1], 1, 'teal')]),
    ('a', [ang(_MA, _MC, _MB, 26, 'teal', 'α', 44), ang(_ME, _MC, _MD, 24, 'teal', 'α', 42)]),
    ('b', [ang(_MB, _MA, _MC, 26, 'orange', 'β', 44), ang(_MD, _ME, _MC, 24, 'orange', 'β', 42)]),
    ('c', [ang(_MC, _MA, _MB, 22, 'red')]),
    ('small', [('tint', [_MC, _ME, _MD], 'teal'), ('poly', [_MC, _ME, _MD], 'teal', 4)]),
    ('x', [('txt', 206, 238, 'x', 'teal', 30, True), ('txt', 320, 372, '25', 'orange', 28)]),
], vb='150 15 320 375', w=400, title='ED parallel to AB'))
QLEFT(f144a, 'geo36-g144')
f144b = PIN(GEO('f144b', [
    ('line', [qraw('geo36-g144')]),
    ('p1', [sg(_MB, _MD, 'orange', 7), sg(_MD, _MC, 'teal', 7)]),
    ('p2', [sg(_MA, _ME, 'orange', 7), sg(_ME, _MC, 'teal', 7), ('txt', 206, 238, '6', 'teal', 30)]),
], vb='150 15 320 375', w=400, title='The parts of the two sides'))
QLEFT(f144b, 'geo36-g144')

# (V3 cut-out) the two triangles pulled apart, side by side, the same way up, with the equal angles marked
_pC1, _pE1, _pD1 = (65.1, 308.5), (96.5, 154.3), (191.0, 308.5)
_pC2, _pA2, _pB2 = (445.1, 308.5), (497.5, 51.5), (654.9, 308.5)
f144p = PIN(GEO('f144p', [
    ('line', [('tint', [_pC1, _pE1, _pD1], 'teal'), ('poly', [_pC1, _pE1, _pD1], 'ink', 3), ('poly', [_pC2, _pA2, _pB2], 'ink', 3),
              nm(_pC1, 'C', (117, 257), 22), nm(_pE1, 'E', (117, 257), 22), nm(_pD1, 'D', (117, 257), 22),
              nm(_pC2, 'C', (532, 223), 22), nm(_pA2, 'A', (532, 223), 22), nm(_pB2, 'B', (532, 223), 22),
              ('txt', 128, 334, '15', 'ink', 24), ('txt', 58, 225, 'x', 'teal', 26, True),
              ('txt', 550, 334, '25', 'ink', 24), ('txt', 432, 170, 'x + 4', 'ink', 24)]),
    ('ang', [ang(_pE1, _pC1, _pD1, 26, 'teal', 'α', 46), ang(_pA2, _pC2, _pB2, 34, 'teal', 'α', 56),
             ang(_pD1, _pE1, _pC1, 24, 'orange', 'β', 44), ang(_pB2, _pA2, _pC2, 30, 'orange', 'β', 52),
             ang(_pC1, _pE1, _pD1, 20, 'red'), ang(_pC2, _pA2, _pB2, 26, 'red')]),
], vb='20 20 680 335', w=560, col=1, title='The two triangles pulled apart'))
_R(f144p, QTOP('geo36-g144') + 85, 900)
t144a = SBT('t144a', [('opposite α', 'DC = 15', 'BC = 25'), ('opposite β', 'EC = x', 'AC = x + 4')], col=1, w=500)
_R(t144a, 260, 960)
r144b = IH('r144b', '$\\frac{15}{25} = \\frac{x}{x + 4}$', size=30)
r144c = IH('r144c', '$\\frac{3}{5} = \\frac{x}{x + 4}$', size=30)
r144d = IH('r144d', '$3(x + 4) = 5x$', size=30)
r144e = IH('r144e', '$3x + 12 = 5x$', size=30)
r144f = IH('r144f', '$12 = 2x$, $x = 6$', size=30)
r144g = IH('r144g', '$AC = 6 + 4 = 10$', size=30)
r144h = IH('r144h', '$\\frac{15}{x} = \\frac{25}{x + 4}$', size=30)
r144i = IH('r144i', '$BD : DC = 10 : 15 = 2 : 3$', size=30)
r144j = IH('r144j', '$AE : EC = 2 : 3$', size=30)
r144k = IH('r144k', '$2$ parts $= 4$, $1$ part $= 2$', size=30)
r144l = IH('r144l', '$EC = 3 \\cdot 2 = 6$, $AC = 10$', size=30)
r144m = IH('r144m', '$4$ is $\\frac{2}{5}$ of $10$', size=30)
r144n = IH('r144n', '$EC = \\frac{2}{5} \\cdot 15 = 6$', size=30)
FLOW([r144b, r144c], [(960, 300, 520, 700), (1270, 300, 520, 700)])
r144c2 = IH('r144c2', '$\\frac{3}{5} = \\frac{x}{x + 4}$', size=30)
FLOW([r144c2, r144d, r144e, r144f, r144g], QC('geo36-g144'))
FLOW([r144h], QC('geo36-g144'))
FLOW([r144i, r144j, r144k, r144l, r144m, r144n], QC('geo36-g144'))
NOFIG('solve-geo36-g144', 0, 1, 2, 3, 4, 5)
f144c = PIN(GEO('f144c', [('line', [qraw('geo36-g144'), ('poly', [_MC, _ME, _MD], 'teal', 4), ('txt', 206, 238, 'x', 'teal', 30, True),
                                    ('txt', 320, 372, '25', 'orange', 28)])], vb='150 15 320 375', w=400, title='The two triangles'))
QLEFT(f144c, 'geo36-g144')
f144d = PIN(GEO('f144d', [('line', [qraw('geo36-g144'), ('poly', [_MC, _ME, _MD], 'teal', 4), ('txt', 206, 238, 'x', 'teal', 30, True),
                                    ('txt', 320, 372, '25', 'orange', 28)])], vb='150 15 320 375', w=400, title='Inside one triangle'))
QLEFT(f144d, 'geo36-g144')
f144e = PIN(GEO('f144e', [('line', [qraw('geo36-g144'), ('poly', [_MC, _ME, _MD], 'teal', 4), ('txt', 206, 238, 'x', 'teal', 30, True),
                                    ('txt', 320, 372, '25', 'orange', 28)])], vb='150 15 320 375', w=400, title='Solve the equation'))
QLEFT(f144e, 'geo36-g144')

video('solve-geo36-g144', 'solution', qid='geo36-g144', slides=[
    SM('Method 1 · The math way: similar triangles', 'Prove the similarity',
      L("Now a new question. In triangle A B C, point D lies on B C and point E lies on A C, and E D is parallel to A B. "
        "Given, B D is ten, D C is fifteen, and A E is four. What is the length of A C?",
        pt('stem', 'Now a new question', 'hl', 11.0), show(f144a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("So we need the whole side A C. We know only its top part, A E. We'll solve it in two different ways."),
      L("First, we prove that the small triangle, E D C, is similar to the big triangle, A B C. On the exam, one rule is "
        "enough. We need two equal angles.", show(f144a['par'], 'First, we prove')),
      L("Let's call the angle at A alpha. E D is parallel to A B, so the angle at E is also alpha. They're corresponding "
        "angles between parallel lines.", show(f144a['a'], "Let's call the angle at A alpha")),
      L("The angle at B, let's call it beta. For the same reason, the angle at D is also beta.", show(f144a['b'], 'The angle at B')),
      L("And the angle at C is in both triangles. So all the angles are equal, and the small triangle E D C is similar to "
        "the big triangle A B C.", show(f144a['c'], 'And the angle at C'), show(f144a['small'], 'So all the angles are equal')),
      L("Let's pull the two triangles apart, so we can see them side by side, the same way up. Alpha, beta and the angle "
        "at C are in both.", show(f144p['line'], "Let's pull the two triangles apart"), show(f144p['ang'], 'Alpha, beta'))),
    SM('Method 1 · The math way: similar triangles', 'Small over big',
      L("Let's start with the math way. To compare the triangles, we need matching sides, opposite equal angles. Like in "
        "the lesson, let's make the small-big table.", show(f144c['line'], "Let's start with the math way"),
        show(t144a['line'], "let's make the small-big table")),
      L("Opposite alpha in the small triangle is D C, fifteen. Opposite alpha in the big one is the whole side B C. Ten "
        "plus fifteen is twenty-five.", show(t144a['r1'], 'Opposite alpha in the small triangle')),
      L("Opposite beta in the small triangle is E C. We don't know it, so let's call it x. Opposite beta in the big one "
        "is A C. That's x plus four.", show(t144a['r2'], 'Opposite beta in the small triangle')),
      L("Here x is in both cells of the row, so the triangle value won't help. We write the ratios in a fixed order, "
        "small over big. Fifteen over twenty-five is equal to x over x plus four.", show(r144b, 'Fifteen over twenty-five is equal')),
      L("Fifteen and twenty-five both divide by five. So it's three fifths.", show(r144c, 'So it'))),
    SM('Method 1 · The math way: similar triangles', 'Solve the equation',
      L("So three fifths is equal to x over x plus four.", show(f144e['line'], 'So three fifths'), show(r144c2, 'So three fifths')),
      L("Now we cross-multiply. Three times x plus four is equal to five x. That's three x plus twelve, equal to five x.",
        show(r144d, 'Three times x plus four'), show(r144e, "That's three x plus twelve")),
      L("We gather the x's on the side that has more x. Five x minus three x is two x, so twelve is equal to two x, and x "
        "is six.", show(r144f, 'so twelve is equal to two x')),
      L("Careful, six isn't our final answer yet. Six is E C, and it's choice number one. They asked for A C. Six plus "
        "four is ten.", mk('cross', 'choice 1', 'Six is E C'), show(r144g, 'Six plus four is ten'))),
    SM('Method 1 · The math way: similar triangles', 'Inside one triangle',
      L("Some students write the ratio inside each triangle instead. In the small triangle, fifteen over x. In the big "
        "triangle, twenty-five over x plus four.", show(f144d['line'], 'Some students write the ratio'), show(r144h, 'In the small triangle')),
      L("Like in the lesson, the ratio of two sides inside one triangle is the same in both triangles. So these fractions "
        "are equal."),
      L("Swap the x and the twenty-five in our first equation, and you get exactly this one. So it gives the same x, six. "
        "Both ways are correct."),
      L("So A C is ten. In the exam, you'd circle choice number three and move on. Now the second way.")),
    SM('Method 2 · The math way: part to part', 'Part to part',
      L("Now the second way, with the part to part rule from the lesson. E D is parallel to A B. So it cuts the other "
        "two sides in the same ratio.", show(f144b['line'], 'Now the second way')),
      L("On side C B, B D is ten and D C is fifteen. Ten to fifteen is two to three.", show(f144b['p1'], 'On side C B'),
        show(r144i, 'Ten to fifteen')),
      L("So on side C A, A E to E C is also two to three. Part to part is fine here.", show(r144j, 'A E to E C is also')),
      L("A E is four, and it's two parts. So one part is two.", show(r144k, "A E is four, and it's two parts")),
      L("E C is three parts, three times two, six. And all of A C is four plus six, ten.", show(r144l, 'E C is three parts'),
        show(f144b['p2'], 'three times two, six'))),
    SM('Method 2 · The math way: part to part', 'Across',
      L("We can also compare across. B D is ten, and the part next to it on the other side, A E, is four. Four is two "
        "fifths of ten.", show(r144m, 'Four is two fifths')),
      L("So E C is two fifths of D C. A fifth of fifteen is three, so two fifths is six. Again A C is four plus six, ten.",
        show(r144n, 'So E C is two fifths')),
      L("Only the parallel line itself, E D, must go with a whole side. The parts of the sides can go part to part."),
      L("And twenty-five is B C, the other side. Choice number three is our answer, and I'll see you in the next "
        "question.", mk('cross', 'choice 2', 'And twenty-five is B C'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-geo36-g145 - a square DECF in a right triangle; AF 5, the square's side x: BE
# Hebrew geo 8073-8164 (AF 2 -> x^2/2): "first understand: three similar triangles in this object" (alpha, 90 - alpha,
# the square's 90 and the angle next to it); "letters in the question and in the answers -> we can plug in numbers";
# (1) the full math with the TWO SMALL triangles ("personally I think it's simpler"), top over bottom in a fixed order,
# opposite equal angles, and "simpler with the triangle value: multiply diagonally, divide by the one left" -> x^2/2;
# (2) plugging in: "our automatic choice is 1 - is it convenient? the legs 2 and 1, not a triangle we know" -> plug in
# x = AF: silver triangles, CONGRUENT (1 : 1) -> BE = 2; "plugging in only rules choices out, after three are out one is
# left". English: AF 5 -> x^2/5, plug in x = 5. Her "pick what's comfortable" verdict is not said (R16).
# V3: the copy with the top triangle teal and the bottom one orange; alpha / 90 - alpha marked in all three; x on FD and
# DE, a question mark on BE; method 2: every side 5 written on the copy.
# =================================================================================================================
_SA, _SB, _SC = (147.1, 64.7), (492.9, 295.3), (147.1, 295.3)
_SD, _SE, _SF = (285.4, 156.9), (285.4, 295.3), (147.1, 156.9)
f145a = PIN(GEO('f145a', [
    ('line', [qraw('geo36-g145')]),
    ('big', [ang(_SA, _SC, _SB, 30, 'teal', 'α', 50), ang(_SB, _SA, _SC, 40, 'orange')]),
    ('bot', [('tint', [_SD, _SE, _SB], 'orange'), rt(_SE, _SB, _SD, 12, 'ink'), ang(_SD, _SE, _SB, 24, 'teal', 'α', 42)]),
    ('top', [('tint', [_SA, _SF, _SD], 'teal'), rt(_SF, _SA, _SD, 12, 'ink'), ang(_SD, _SA, _SF, 24, 'orange')]),
    ('x', [('txt', 216, 140, 'x', 'teal', 28, True), ('txt', 302, 226, 'x', 'orange', 28, True), ('txt', 389, 320, '?', 'orange', 30)]),
], vb='100 30 430 320', w=470, title='The square in the right triangle'))
QLEFT(f145a, 'geo36-g145')
f145b = PIN(GEO('f145b', [
    ('line', [qraw('geo36-g145'), ('tint', [_SA, _SF, _SD], 'teal'), ('tint', [_SD, _SE, _SB], 'orange'),
              ('txt', 216, 140, 'x', 'teal', 28, True), ('txt', 302, 226, 'x', 'orange', 28, True), ('txt', 389, 320, '?', 'orange', 30)]),
], vb='100 30 430 320', w=470, title='The two small triangles'))
QLEFT(f145b, 'geo36-g145')
f145c = PIN(GEO('f145c', [
    ('line', [qraw('geo36-g145')]),
    ('five', [('txt', 216, 140, '5', 'teal', 30), ('txt', 302, 226, '5', 'orange', 30)]),
    ('be', [('txt', 389, 320, '5', 'orange', 30)]),
], vb='100 30 430 320', w=470, title='Plug in x = 5'))
QLEFT(f145c, 'geo36-g145')
t145a = TVAL('t145a', ('AF = 5', 'DE = x'), ('FD = x', '?'), col=1, w=420, cols=('top', 'bottom'))
_R(t145a, QTOP('geo36-g145') + 10, 960)
r145a = IH('r145a', '$BE = \\frac{x \\cdot x}{5} = \\frac{x^2}{5}$', size=30)
r145b = IH('r145b', '$x = 5$: legs $5$ and $5$', size=30)
r145c = IH('r145c', '$BE = FD = 5$', size=30)
r145d = IH('r145d', '(1) $5x = 25$, no', size=30)
r145e = IH('r145e', '(2) $x^2 = 25$, no', size=30)
r145f = IH('r145f', '(3) $\\frac{25}{5} = 5$', size=30)
r145g = IH('r145g', '(4) $\\frac{5}{5} = 1$, no', size=30)
_R(r145a, QTOP('geo36-g145') + 210, 960)
FLOW([r145b, r145c, r145d, r145e, r145f, r145g], QC2('geo36-g145'))
NOFIG('solve-geo36-g145', 0, 1, 2)

video('solve-geo36-g145', 'solution', qid='geo36-g145', slides=[
    SM('Method 1 · The math way: similar triangles', 'Three similar triangles',
      L("Now a new question. A B C is a right triangle with the right angle at C. D E C F is a square. D lies on A B, E "
        "lies on B C, and F lies on A C. A F is five, and the side of the square is x. What is the length of B E?",
        pt('stem', 'Now a new question', 'hl', 12.0), show(f145a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("So the answer is an expression with x. There are letters in the question and in the choices, so later we can "
        "also plug in numbers. We'll solve it in two different ways."),
      L("First, let's understand the picture. It hides three similar triangles. The big one, A B C, the top one, A F D, "
        "and the bottom one, D E B."),
      L("Let's prove it. In the big triangle, C is ninety. Let's call the angle at A alpha. The angles add up to a "
        "hundred eighty, so the angle at B is ninety minus alpha.", show(f145a['big'], 'Let')),
      L("Now the bottom triangle. The square's corner at E is ninety, so the angle next to it, inside the triangle, is "
        "ninety too. It has ninety minus alpha at B, so the angle at D is alpha.", show(f145a['bot'], 'Now the bottom triangle')),
      L("And the top triangle. The angle at F is ninety, for the same reason, and the angle at A is alpha. So the angle "
        "at D is ninety minus alpha.", show(f145a['top'], 'And the top triangle')),
      L("All three triangles have the same angles, so all three are similar.", show(f145a['x'], 'All three triangles'))),
    SM('Method 1 · The math way: similar triangles', 'The two small triangles',
      L("Let's start with the math way. All the sides of the square are x. We could compare the big triangle with a "
        "small one, but I think the two small triangles give a simpler solution.", show(f145b['line'], "Let's start with the math way")),
      L("We'll make the table, with the top triangle and the bottom triangle, always in this order.", show(t145a['line'], "We'll make the table")),
      L("Opposite ninety minus alpha in the top triangle is A F, five. In the bottom one, it's D E, x.",
        show(t145a['r1'], 'Opposite ninety minus alpha')),
      L("Opposite alpha in the top triangle is F D, x. In the bottom one, it's B E. That's what we're looking for.",
        show(t145a['r2'], 'Opposite alpha in the top triangle')),
      L("We're looking for one of the four, so we use the triangle value. Multiply along the diagonal, and divide by "
        "what's left. x times x, divided by five. That's x squared over five.", show(t145a['diag'], 'Multiply along the diagonal'),
        show(r145a, 'x times x, divided by five')),
      L("x squared over five is choice number three. Now let's check it in another way.", pt('choice 3', 'x squared over five is choice'))),
    SM('Method 2 · Plugging in numbers', 'Plug in x = 5',
      L("Now let's plug in numbers. Our usual first try is one. But is one convenient here?", show(f145c['line'], "Now let's plug in numbers")),
      L("With x equal to one, the top triangle has legs five and one. That's not a triangle we know, so we'd still need "
        "the whole similarity to find B E."),
      L("So let's choose x to make a special case. Let's take x equal to five, the same as A F. Then the top triangle "
        "has two legs of five.", show(f145c['five'], 'Let'), show(r145b, "Let's take x equal to five")),
      L("Its corner is a right angle, so it's a silver triangle, forty-five, forty-five, ninety. And the bottom triangle "
        "has the same angles, and the side D E is also five, like A F."),
      L("So the two small triangles aren't only similar. They're identical, a ratio of one to one. So B E is equal to F "
        "D, five.", show(r145c, 'So B E is equal'), show(f145c['be'], 'So B E is equal')),
      L("Now we put five into every choice, and look for five. Choice number one says five x. Five times five is "
        "twenty-five, so it's out.", show(r145d, 'Five times five'), mk('cross', 'choice 1', "so it's out")),
      L("Choice number two says x squared. That's twenty-five too, so it's out.", show(r145e, 'Choice number two says'),
        mk('cross', 'choice 2', 'That')),
      L("Choice number three says x squared over five. Twenty-five over five is five. It stays.", show(r145f, 'Twenty-five over five')),
      L("Choice number four says x over five. Five over five is one, so it's out.", show(r145g, 'Choice number four says'),
        mk('cross', 'choice 4', 'Five over five is one')),
      L("Remember, plugging in numbers only rules choices out. Three are out, so one is left. Choice number three is our "
        "answer, and I'll see you in the next question.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# solve-geo36-g146 - the altitude to the hypotenuse; BD 3, DC 27: AD
# Hebrew geo 8166-8241 (4 and 9 -> 6, "hard"): the same object, three similar triangles; "until now we wrote alpha, 90 -
# alpha - easier for most students: plug in a NUMERIC angle" (C = 20, B = 70; 20, 70, 90 in all three); her WARNING: we
# may plug in angles only to see what matches what - not 45, 45 and then "silver" (a contradiction); "a number seems to be
# missing": two numbers, but an equation of fractions has four parts; work inside the SAME triangle, long leg over short
# leg: AD / BD = DC / AD -> AD squared -> the root. English: 3 and 27 -> 81 -> 9.
# Method 2 = the altitude shortcut taught in geo-139 part 3 (h^2 = the two parts multiplied), with a check by the figure
# (the teacher's rule, 23 Oct: most figures are accurate - an estimate next to the proof: AD is about 3 times BD).
# The old English Pythagoras check (27 squared, 2h^2 + 738 = 900) is dropped: not hers, and beyond exam mental math (R36).
# Traps: 15 (half of BC, the median's length, not the altitude's) and 3 root 10 (the leg AB).
# V3: the copy with 20 / 70 written in the three triangles; the left triangle teal, the right one orange; AD lit.
# =================================================================================================================
_NA, _NB, _NC, _ND = (137.5, 152.6), (91.9, 289.5), (548.1, 289.5), (137.5, 289.5)
f146a = PIN(GEO('f146a', [
    ('line', [qraw('geo36-g146')]),
    ('c20', [('txt', 470, 276, '20°', 'orange', 24)]),
    ('b70', [('txt', 112, 272, '70°', 'teal', 22)]),
    ('left', [('tint', [_NA, _NB, _ND], 'teal'), ('txt', 125, 190, '20°', 'orange', 20)]),
    ('right', [('tint', [_NA, _ND, _NC], 'orange'), ('txt', 158, 196, '70°', 'teal', 20)]),
], vb='60 110 520 230', w=500, title='The altitude AD: the angles 20, 70, 90'))
QLEFT(f146a, 'geo36-g146')
# (V3 cut-out) the two small triangles pulled out of the figure and turned the same way: the right angle at the bottom
# left, the short leg up, the long leg along the bottom; 20 degrees at the right end, 70 at the top
_LD, _LB, _LA = (40, 250), (40, 200), (190, 250)
_RD, _RA, _RC = (240, 250), (240, 160), (510, 250)
f146b = PIN(GEO('f146b', [
    ('line', [('tint', [_LD, _LB, _LA], 'teal'), ('poly', [_LD, _LB, _LA], 'ink', 3), rt(_LD, _LA, _LB, 10, 'ink'),
              ('tint', [_RD, _RA, _RC], 'orange'), ('poly', [_RD, _RA, _RC], 'ink', 3), rt(_RD, _RC, _RA, 12, 'ink'),
              ('txt', 40, 180, 'BD = 3', 'ink', 20), ('txt', 115, 276, 'AD', 'ink', 22), ('txt', 375, 276, '27', 'ink', 24),
              ang(_LA, _LD, _LB, 40, 'orange', '20°', 64), ang(_LB, _LD, _LA, 16, 'teal', '70°', 36),
              ang(_RC, _RD, _RA, 60, 'orange', '20°', 86), ang(_RA, _RD, _RC, 22, 'teal', '70°', 44)]),
    ('ad', [sg(_LD, _LA, 'red', 7), sg(_RD, _RA, 'red', 7), ('txt', 212, 205, 'AD', 'red', 22)]),
    ('nine', [('txt', 115, 300, '9', 'red', 28), ('txt', 212, 232, '9', 'red', 28)]),
], vb='10 140 520 175', w=540, title='The two small triangles, pulled out and turned the same way'))
QLEFT(f146b, 'geo36-g146', w=540)
QLEFT(f146b, 'geo36-g146')
f146c = PIN(GEO('f146c', [
    ('line', [qraw('geo36-g146')]),
    ('eye', [sg(_NB, _ND, 'teal', 6), sg(_NA, _ND, 'orange', 6), ('txt', 166, 225, '≈ 3 · BD', 'orange', 20)]),
], vb='60 110 520 230', w=500, title='A look at the figure'))
QLEFT(f146c, 'geo36-g146')
r146a = IH('r146a', '$C = 20°$, $B = 70°$', size=30)
r146b = IH('r146b', 'left: $90°, 70°$, so $20°$ at A', size=30)
r146c = IH('r146c', 'right: $90°, 20°$, so $70°$ at A', size=30)
r146d = IH('r146d', '$\\frac{AD}{BD} = \\frac{DC}{AD}$', size=30)
r146e = IH('r146e', '$\\frac{AD}{3} = \\frac{27}{AD}$', size=30)
r146f = IH('r146f', '$AD^2 = 3 \\cdot 27 = 81$', size=30)
r146g = IH('r146g', '$AD = \\sqrt{81} = 9$', size=30)
r146h = IH('r146h', '$AD^2 = BD \\cdot DC$', size=30)
r146i = IH('r146i', '$3 \\cdot 27 = 81$, $AD = 9$', size=30)
r146j = IH('r146j', 'half of $BC$: $30 \\div 2 = 15$', size=30)
FLOW([r146a, r146b, r146c], QC('geo36-g146'))
FLOW([r146d, r146e, r146f, r146g], QC('geo36-g146'))
FLOW([r146h, r146i, r146j], QC('geo36-g146'))
NOFIG('solve-geo36-g146', 0, 1, 2)

video('solve-geo36-g146', 'solution', qid='geo36-g146', slides=[
    SM('Method 1 · The math way: similar triangles', 'Plug in an angle',
      L("Now a new question. A B C is a right triangle with the right angle at A. A D is perpendicular to B C. Given, B "
        "D is three and D C is twenty-seven. What is the length of A D?", pt('stem', 'Now a new question', 'hl', 10.0),
        show(f146a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("So we need the altitude, A D. It looks like a number is missing, and that's what makes this question hard. "
        "Let's see how we deal with it. We'll solve it in two different ways."),
      L("Let's start with the math way. Like in the lesson, the altitude to the hypotenuse makes three similar "
        "triangles. The left one, A B D, the right one, A D C, and the big one, A B C."),
      L("Until now we wrote alpha and ninety minus alpha. Most students find it easier with a number. So let's plug in "
        "an angle. C is a sharp angle, so let's say C is twenty degrees.", show(f146a['c20'], "let's say C is twenty")),
      L("A is ninety, so B is a hundred eighty minus ninety minus twenty, seventy.", show(f146a['b70'], 'so B is'),
        show(r146a, 'A is ninety, so B is')),
      L("The left triangle has ninety at D, and seventy at B. So the angle at the top is twenty.", show(f146a['left'], 'The left triangle'),
        show(r146b, 'The left triangle has ninety')),
      L("The right triangle has ninety at D, and twenty at C. So its angle at the top is seventy.", show(f146a['right'], 'The right triangle'),
        show(r146c, 'The right triangle has ninety')),
      L("Twenty, seventy and ninety in all three triangles. So they're similar."),
      L("Here's a small warning. We plug in angles only to see what matches what. We can't plug in forty-five and forty-five, "
        "and then use a silver triangle. Then A D would be three, like B D, and also twenty-seven, like D C. That's "
        "impossible.")),
    SM('Method 1 · The math way: similar triangles', 'Inside the same triangle',
      L("Why is it hard? We have only two numbers, three and twenty-seven. But an equation of two fractions has four "
        "parts. Usually we need three of them.", show(f146b['line'], 'Why is it hard')),
      L("To find A D, we compare the two triangles that contain A D, the left one and the right one. Let's pull them out "
        "and turn them the same way. This time, we work inside each triangle.", show(f146b['ad'], 'that contain A D')),
      L("In the left triangle, opposite seventy is the long leg, A D. Opposite twenty is the short leg, B D."),
      L("In the right triangle, opposite seventy is the long leg, D C, twenty-seven. Opposite twenty is the short leg, A "
        "D."),
      L("Long leg over short leg is the same in both triangles. So A D over B D is equal to D C over A D.",
        show(r146d, 'So A D over B D')),
      L("Now we put in the numbers. A D over three is equal to twenty-seven over A D.", show(r146e, 'A D over three')),
      L("A D appears twice. That's why two numbers are enough. It's one unknown in one equation."),
      L("Cross-multiply. A D squared is three times twenty-seven, eighty-one.", show(r146f, 'A D squared is three times')),
      L("The square root of eighty-one is nine. So A D is nine.", show(r146g, 'The square root of eighty-one'), show(f146b['nine'], 'So A D is nine'))),
    SM('Method 2 · The math way: the altitude shortcut', 'The shortcut',
      L("Now the shortcut from the lesson. The altitude to the hypotenuse, squared, is the two parts of the hypotenuse "
        "multiplied.", show(f146c['line'], 'Now the shortcut'), show(r146h, 'The altitude to the hypotenuse')),
      L("Three times twenty-seven is eighty-one. So the altitude is the root of eighty-one, nine. That's the whole solution, in one line.",
        show(r146i, 'Three times twenty-seven')),
      L("And a quick check with the figure. Most exam figures are drawn accurately. Here A D looks about three times B "
        "D, so about nine. That fits.", show(f146c['eye'], 'Here A D looks about three times')),
      L("Careful with fifteen. That's half of B C, thirty divided by two. It's the length of the median from A, not of "
        "the altitude.", show(r146j, 'thirty divided by two'), mk('cross', 'choice 1', 'Careful with fifteen')),
      L("And three root ten is the leg A B. Choice number two is our answer, and I'll see you in the next question.",
        mk('cross', 'choice 3', 'And three root ten'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# solve-geo36-g147 - concentric circles r and 1.3r; Noah: the outer circumference is 1.3 times; Emma: the ring is bigger
# Hebrew geo 8243-8317 (r and 1.5r, Yitzhak and Nitza, both right): two ways - (1) the math way with circle rules, no
# similarity: 3 pi r vs 2 pi r -> Yitzhak right -> choices 2 and 3 out; the ring = the big circle minus the small one
# ("grey areas we solve with a scheme"), 9/4 - 1 = 5/4 > 1 -> Nitza right; (2) similarity: "similar shapes aren't only
# triangles", the linear ratio is kept -> x 1.5 at once; the areas: "we don't like fractions - EXPAND the ratio to whole
# numbers" 1 : 1.5 -> 2 : 3 -> 4 : 9 -> the ring 5 units > 4. English: 1.3 -> 10 : 13 -> 100 : 169 -> the ring 69 < 100,
# so only Noah (the result differs on purpose). The old slide titles "Liam" / "Maya" (hebrew-vs-english-t36 4) are gone.
# Her closing ("much shorter with similarity") is kept as a fact, not a verdict.
# V3: the copy's radii teal (r) and orange (1.3r); the circumferences; the ring tinted; the units 100 / 169 / 69.
# =================================================================================================================
_RING147 = ('M 192.25 180 a 127.75 127.75 0 1 0 255.5 0 a 127.75 127.75 0 1 0 -255.5 0 Z '
            'M 221.731 180 a 98.269 98.269 0 1 0 196.538 0 a 98.269 98.269 0 1 0 -196.538 0 Z')
f147a = PIN(GEO('f147a', [
    ('line', [qraw('geo36-g147')]),
    ('r', [sg((320, 180), (320, 278.3), 'teal', 6), sg((320, 180), (447.8, 180), 'orange', 6)]),
    ('c', [('circ', 320, 180, 98.269, 'teal', 5), ('circ', 320, 180, 127.75, 'orange', 5)]),
], vb='180 40 280 290', w=400, title='Two circles with radii r and 1.3r'))
QLEFT(f147a, 'geo36-g147')
f147b = PIN(GEO('f147b', [
    ('line', [qraw('geo36-g147')]),
    ('ring', [('region', _RING147, 'orange', 0.35)]),
    ('in', [('circ', 320, 180, 98.269, 'teal', 5, False, 'teal')]),
], vb='180 40 280 290', w=400, title='The ring and the inner circle'))
QLEFT(f147b, 'geo36-g147')
f147c = PIN(GEO('f147c', [
    ('line', [qraw('geo36-g147')]),
    ('u', [('txt', 282, 140, '100', 'teal', 30), ('txt', 320, 64, '169', 'orange', 26)]),
    ('ring', [('region', _RING147, 'orange', 0.35), ('txt', 225, 290, '69', 'orange', 30)]),
], vb='180 40 280 290', w=400, title='The units 100 and 169'))
QLEFT(f147c, 'geo36-g147')
r147a = IH('r147a', 'outer: $2π \\cdot 1.3r = 2.6πr$', size=30)
r147b = IH('r147b', 'inner: $2πr$', size=30)
r147c = IH('r147c', '$2.6 = 1.3 \\cdot 2$: Noah, yes', size=30)
r147d = IH('r147d', '$13^2 = 169$, so $1.3^2 = 1.69$', size=30)
r147e = IH('r147e', 'big: $1.69πr^2$', size=30)
r147f = IH('r147f', 'ring: $1.69πr^2 - πr^2 = 0.69πr^2$', size=30)
r147g = IH('r147g', '$0.69 < 1$: Emma, no', size=30)
r147h = IH('r147h', '$1 : 1.3 = 10 : 13$', size=30)
r147i = IH('r147i', 'areas $10^2 : 13^2 = 100 : 169$', size=30)
r147j = IH('r147j', 'ring: $169 - 100 = 69 < 100$', size=30)
FLOW([r147a, r147b, r147c], QC('geo36-g147'))
FLOW([r147d, r147e, r147f, r147g], QC('geo36-g147'))
FLOW([r147h, r147i, r147j], QC('geo36-g147'))
NOFIG('solve-geo36-g147', 0, 1, 2)

video('solve-geo36-g147', 'solution', qid='geo36-g147', slides=[
    SM('Method 1 · The math way: circle formulas', 'Noah',
      L("Now a new question. Two circles with the same center have radii r and one point three r. Noah says that the outer "
        "circumference is one point three times the inner circumference. Emma says that the area of the ring between the "
        "circles is bigger than the area of the inner circle. Who is right?", pt('stem', 'Now a new question', 'hl', 14.0),
        show(f147a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("So we check two claims, and decide who is right. Noah, Emma, both, or neither. We'll solve it in two different "
        "ways."),
      L("Let's start with the math way, with the circle formulas and no similarity. Noah talks about circumferences. The "
        "circumference of a circle is two pi r.", show(f147a['r'], 'Noah talks about circumferences')),
      L("The outer radius is one point three r. Two times one point three is two point six. So the outer circumference "
        "is two point six pi r.", show(f147a['c'], 'The outer radius is'), show(r147a, 'Two times one point three')),
      L("The inner radius is r, so the inner circumference is two pi r.", show(r147b, 'so the inner circumference')),
      L("Two point six is one point three times two. So the outer circumference is one point three times the inner one. "
        "Noah is right.", show(r147c, 'Two point six is one point three times')),
      L("So the choices that say Noah is wrong are out. Neither is choice number three, and Emma only is choice number "
        "four.", mk('cross', 'choice 3', 'Neither is choice number three'), mk('cross', 'choice 4', 'Emma only is choice')),
      L("Now it's Noah only, or both of them.")),
    SM('Method 1 · The math way: circle formulas', 'Emma',
      L("Now Emma. She says the ring is bigger than the inner circle. The ring is the big circle minus the small circle.",
        show(f147b['line'], 'Now Emma'), show(f147b['ring'], 'The ring is the big circle')),
      L("The big circle is pi, times the square of one point three r. One point three squared is one point six nine, because "
        "thirteen squared is a hundred sixty-nine.", show(r147d, 'thirteen squared')),
      L("So the big circle is one point six nine pi r squared.", show(r147e, 'So the big circle is')),
      L("The small circle is pi r squared. So the ring is one point six nine minus one, zero point six nine pi r squared.",
        show(r147f, 'So the ring is one point six nine minus')),
      L("The inner circle is one pi r squared. Zero point six nine is less than one. So the ring is smaller, and Emma is "
        "wrong.", show(f147b['in'], 'The inner circle is one'), show(r147g, 'Zero point six nine is less')),
      L("In the figure, the ring may look big. Our eye isn't good at comparing a ring with a circle, so we calculate."),
      L("So only Noah is right. That's choice number two. Now a shorter way, with similarity.")),
    SM('Method 2 · Understanding: similarity', 'With similarity',
      L("Now by understanding, with similarity. Similar shapes aren't only triangles. Any two circles are similar, like "
        "any two squares or two regular hexagons.", show(f147c['line'], 'Now by understanding')),
      L("First, Noah's claim. In similar shapes, every line keeps the linear ratio. The radius is one point three times as big. So the "
        "circumference is one point three times as big too. No calculation. Noah is right."),
      L("Now Emma's claim. From the linear ratio to the area ratio, we square. But one to one point three isn't comfortable. We don't "
        "like decimals."),
      L("So let's expand the ratio to whole numbers. We multiply both numbers by ten. One to one point three is the same "
        "ratio as ten to thirteen.", show(r147h, 'One to one point three is the same')),
      L("We didn't change the ratio. We only made it easier to work with. Now we square both numbers. Ten squared is a "
        "hundred, and thirteen squared is a hundred sixty-nine.", show(r147i, 'Ten squared is a hundred')),
      L("So the inner circle is a hundred ratio units, and the big circle is a hundred sixty-nine units.",
        show(f147c['u'], 'So the inner circle is a hundred')),
      L("The ring is a hundred sixty-nine minus a hundred, sixty-nine units. Sixty-nine is less than a hundred. So the ring "
        "is smaller, and Emma is wrong.", show(f147c['ring'], 'The ring is a hundred sixty-nine'), show(r147j, 'Sixty-nine is less')),
      L("Questions like this one are much shorter with similarity. Choice number two is our answer, and I'll see you in "
        "the next question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# solve-geo36-g148 - D, F midpoints of AB, AC; the trapezoid DBCF is 21: triangle ADF
# Hebrew geo 8319-8422 (trapezoid 6 -> 2): the midpoint segment is always parallel to the third side -> the top triangle
# is similar to the big one (alpha, beta); three ways: (1) the full math: x, x, 2x -> 1 : 2; y, 2y; heights h and 2h, the
# trapezoid's height h; (3y)h/2 = 6 -> yh = 4 ("keep it") -> yh/2 = 2; (2) linear 1 : 2 -> areas 1 : 4 -> the trapezoid 3
# units = 6 -> 1 unit = 2 ("much shorter, no unknowns"); (3) the midpoint-segment property: find the third midpoint, join
# -> 4 congruent triangles (or 3 parallelograms with a diagonal each) -> 6 / 3 = 2. Her order of preference ("know the
# rule - the shortest; else the ratios; the default the full math") is not said as a verdict (R16). English: 21 -> 7.
# NEW here (one-off, taught fully): the midpoint segment (parallel to the third side) and the four identical triangles.
# Traps: 10.5 (half the trapezoid) and 5.25 (a quarter of it).
# V3: the copy's DF and BC with parallel arrows and the equal angles; x, x, y, 2y, h, h; the units 1 / 3; the third
# midpoint M joined, the four triangles tinted with 7 in each.
# =================================================================================================================
_QA, _QB, _QC, _QD, _QF = (340.857, 75.714), (174.0, 284.286), (466.0, 284.286), (257.429, 180.0), (403.429, 180.0)
_QM = (320.0, 284.286)
f148a = PIN(GEO('f148a', [
    ('line', [qraw('geo36-g148')]),
    ('par', [('par', _QD[0], _QD[1], _QF[0], _QF[1], 1, 'teal'), ('par', _QB[0], _QB[1], _QC[0], _QC[1], 1, 'teal')]),
    ('ang', [ang(_QD, _QA, _QF, 20, 'teal', 'α', 36), ang(_QB, _QA, _QC, 20, 'teal', 'α', 36),
             ang(_QF, _QA, _QD, 20, 'orange', 'β', 36), ang(_QC, _QA, _QB, 20, 'orange', 'β', 36)]),
], vb='130 30 380 300', w=440, title='D and F are midpoints'))
QLEFT(f148a, 'geo36-g148')
f148b = PIN(GEO('f148b', [
    ('line', [qraw('geo36-g148')]),
    ('x', [('txt', 280, 118, 'x', 'teal', 26, True), ('txt', 196, 222, 'x', 'teal', 26, True)]),
    ('y', [('txt', 304, 168, 'y', 'orange', 26, True), ('txt', 320, 312, '2y', 'orange', 26, True)]),
    ('h', [sg(_QA, (340.857, 180), 'red', 3, True), ('txt', 356, 140, 'h', 'red', 26, True),
           sg((340.857, 180), (340.857, 284.286), 'red', 3, True), ('txt', 356, 236, 'h', 'red', 26, True)]),
], vb='130 30 380 300', w=440, title='The letters x, y and h'))
QLEFT(f148b, 'geo36-g148')
f148c = PIN(GEO('f148c', [
    ('line', [qraw('geo36-g148')]),
    ('u1', [('txt', 333, 150, '1', 'teal', 30)]),
    ('u3', [('tint', [_QD, _QB, _QC, _QF], 'orange'), ('txt', 320, 238, '3', 'orange', 32)]),
], vb='130 30 380 300', w=440, title='The units 1 and 3'))
QLEFT(f148c, 'geo36-g148')
_c4 = [cen([_QA, _QD, _QF]), cen([_QD, _QB, _QM]), cen([_QF, _QM, _QC]), cen([_QD, _QM, _QF])]
f148d = PIN(GEO('f148d', [
    ('line', [qraw('geo36-g148')]),
    ('m', [('dot', _QM[0], _QM[1]), ('txt', _QM[0], 310, 'M', 'teal', 24, True), sg(_QD, _QM, 'teal', 4), sg(_QF, _QM, 'teal', 4)]),
    ('four', [('tint', [_QD, _QB, _QM], 'teal'), ('tint', [_QF, _QM, _QC], 'teal'), ('tint', [_QD, _QM, _QF], 'orange')]),
    ('seven', [('txt', x, y + 4, '7', 'ink', 28) for (x, y) in _c4]),
], vb='130 30 380 300', w=440, title='Four identical triangles'))
QLEFT(f148d, 'geo36-g148')
r148a = IH('r148a', '$AD : AB = x : 2x = 1 : 2$', size=30)
r148b = IH('r148b', '$DF = y$, $BC = 2y$', size=30)
r148c = IH('r148c', 'heights $h$ and $2h$', size=30)
r148d = IH('r148d', '$\\frac{(y + 2y) \\cdot h}{2} = 21$', size=30)
r148e = IH('r148e', '$3yh = 42$', size=30)
r148f = IH('r148f', '$yh = 14$', size=30)
r148g = IH('r148g', '$ADF = \\frac{yh}{2} = \\frac{14}{2} = 7$', size=30)
r148h = IH('r148h', 'lengths $1 : 2$, areas $1 : 4$', size=30)
r148i = IH('r148i', 'trapezoid: $4 - 1 = 3$ units', size=30)
r148j = IH('r148j', '$3$ units $= 21$, $1$ unit $= 7$', size=30)
r148k = IH('r148k', '$21 \\div 3 = 7$', size=30)
FLOW([r148a, r148b, r148c, r148d, r148e, r148f, r148g], QC2('geo36-g148'))
FLOW([r148h, r148i, r148j], QC('geo36-g148'))
FLOW([r148k], QC('geo36-g148'))
NOFIG('solve-geo36-g148', 0, 1, 2, 3)

video('solve-geo36-g148', 'solution', qid='geo36-g148', slides=[
    SM('Method 1 · The math way: letters', 'The midpoint segment',
      L("Now a new question. D and F are the midpoints of sides A B and A C of triangle A B C. The area of trapezoid D B C F "
        "is twenty-one. What is the area of triangle A D F?", pt('stem', 'Now a new question', 'hl', 9.0),
        show(f148a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("So we know the trapezoid at the bottom, and we need the small triangle at the top. We'll solve it in three "
        "different ways."),
      L("First, let's understand the given. D and F are midpoints. A segment that joins the midpoints of two sides of a "
        "triangle is called a midpoint segment."),
      L("A midpoint segment has a property worth knowing. It's always parallel to the third side. So D F is parallel to "
        "B C.", show(f148a['par'], "It's always parallel")),
      L("So the angle at D is equal to the angle at B, and the angle at F is equal to the angle at C. They're "
        "corresponding angles.", show(f148a['ang'], 'So the angle at D is equal')),
      L("So the top triangle, A D F, is similar to the big triangle, A B C.")),
    SM('Method 1 · The math way: letters', 'With letters',
      L("Let's start with the math way, with letters. Let's call A D x. D is the midpoint, so D B is also x, and the whole "
        "A B is two x.", show(f148b['line'], "Let's start with the math way"), show(f148b['x'], "Let's call A D x")),
      L("So the linear ratio, small to big, is x to two x. That's one to two.", show(r148a, 'So the linear ratio')),
      L("Let's call D F y. Then B C is twice as long, two y.", show(f148b['y'], "Let's call D F y"), show(r148b, 'Then B C is twice')),
      L("We need areas, so we need heights. Let's call the small triangle's height h. The ratio holds for heights too, so "
        "the big triangle's height is two h.", show(r148c, 'the big triangle')),
      L("So the trapezoid's height is two h minus h, just h.", show(f148b['h'], "So the trapezoid")),
      L("The trapezoid's area is the sum of its bases, times the height, divided by two. And it's twenty-one.",
        show(r148d, "The trapezoid's area is the sum")),
      L("y plus two y is three y. We multiply both sides by two, so three y h is forty-two.", show(r148e, 'so three y h is forty-two')),
      L("Now we divide both sides by three. y h is fourteen. Let's keep that.", show(r148f, 'y h is fourteen')),
      L("The small triangle's area is its base, y, times its height, h, divided by two. That's y h over two. Fourteen over "
        "two is seven.", show(r148g, 'Fourteen over two is seven'))),
    SM('Method 2 · Understanding: ratio units', 'Ratio units',
      L("Now the second way, by understanding, with ratio units. The top triangle is similar to the big one. D is the "
        "midpoint of A B, so the linear ratio is one to two.", show(f148c['line'], 'Now the second way')),
      L("So the areas are one squared to two squared, one to four.", show(r148h, 'So the areas are one squared')),
      L("The small triangle is one unit, and the big triangle is four units. The trapezoid is the big one minus the small "
        "one, four minus one, three units.", show(f148c['u1'], 'The small triangle is one unit'), show(f148c['u3'], 'The trapezoid is the big one'),
        show(r148i, 'four minus one, three units')),
      L("Three units are twenty-one. So one unit is twenty-one divided by three, seven. And the small triangle is one "
        "unit, seven.", show(r148j, 'Three units are twenty-one')),
      L("Seven again. Much shorter, and with no letters.")),
    SM('Method 3 · Insight: four identical triangles', 'Four triangles',
      L("And one more way, with another property of the midpoint segment.", show(f148d['line'], 'And one more way')),
      L("We have the midpoints of two sides. Let's find the midpoint of the third side, B C, and join all three midpoints.",
        show(f148d['m'], "find the midpoint of the third side")),
      L("We always get four identical triangles. The top one, the two at the bottom corners, and the one in the middle.",
        show(f148d['four'], 'We always get four identical')),
      L("Why? The three midpoint segments are parallel to the three sides. So they cut the big triangle into three "
        "parallelograms. And a diagonal cuts a parallelogram into two identical triangles."),
      L("The trapezoid is made of three of these triangles. So each one is twenty-one divided by three, seven. The top "
        "triangle is one of them, so it's seven too.", show(r148k, 'twenty-one divided by three'), show(f148d['seven'], 'The top triangle is one of them')),
      L("Careful with ten point five. That's half of the trapezoid. And five point two five is a quarter of it.",
        mk('cross', 'choice 1', 'Careful with ten point five'), mk('cross', 'choice 2', 'And five point two five')),
      L("Choice number four is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])


# =================================================================================================================
# solve-geo36-g149 - two regular hexagons, areas 150 root 3 and 30 root 3: the perimeter ratio
# Hebrew geo 8424-8490 (12 root 3 and 6 root 3 -> root 2 : 1): two ways - (1) the math way with polygons, no similarity:
# a hexagon = 6 equilateral triangles, 6 a^2 root 3 / 4 = area -> cancel the 6 and the root 3 -> a, b; the perimeters
# 6a : 6b; take a factor out of the root (root 8 = 2 root 2) -> root 2 : 1; (2) similarity: two regular shapes of the same
# family are similar; the areas give the area ratio; back to the linear ratio with the root; the perimeter IS a linear
# ratio. English: 150 / 30 -> a = 10, b = 2 root 5 -> root 5 : 1. Traps 5 : 1 (no root) and 25 : 1.
# Reminders (R29): the hexagon as 6 equilateral triangles and the area a^2 root 3 / 4 (topics 31, 34).
# V3: the copy cut into six equilateral triangles (teal); the side a orange.
# =================================================================================================================
_H6 = [(320.0, 72.647), (227.03, 126.324), (227.03, 233.676), (320.0, 287.353), (412.97, 233.676), (412.97, 126.324)]
f149a = PIN(GEO('f149a', [
    ('line', [qraw('geo36-g149')]),
    ('six', [sg((320, 180), p, 'teal', 3) for p in _H6]),
    ('a', [sg(_H6[0], _H6[1], 'orange', 7), ('txt', 262, 88, 'a', 'orange', 30, True)]),
], vb='190 40 260 290', w=380, title='A regular hexagon: six equilateral triangles'))
QLEFT(f149a, 'geo36-g149')
f149b = PIN(GEO('f149b', [('line', [qraw('geo36-g149'), ('poly', _H6, 'teal', 5)])], vb='190 40 260 290', w=380, title='The perimeter'))
QLEFT(f149b, 'geo36-g149')
f149c = PIN(GEO('f149c', [('line', [qraw('geo36-g149')])], vb='190 40 260 290', w=380, title='Two similar hexagons'))
QLEFT(f149c, 'geo36-g149')
r149a = IH('r149a', '$6 \\cdot \\frac{a^2\\sqrt{3}}{4} = 150\\sqrt{3}$', size=30)
r149b = IH('r149b', '$\\frac{a^2}{4} = 150 \\div 6 = 25$', size=30)
r149c = IH('r149c', '$a^2 = 100$, $a = 10$', size=30)
r149d = IH('r149d', '$\\frac{b^2}{4} = 30 \\div 6 = 5$', size=30)
r149e = IH('r149e', '$b^2 = 20$, $b = \\sqrt{20} = 2\\sqrt{5}$', size=30)
r149f = IH('r149f', '$6 \\cdot 10 : 6 \\cdot 2\\sqrt{5}$', size=30)
r149g = IH('r149g', '$= 10 : 2\\sqrt{5} = 5 : \\sqrt{5}$', size=30)
r149h = IH('r149h', '$5 = \\sqrt{5} \\cdot \\sqrt{5}$, so $\\sqrt{5} : 1$', size=30)
r149i = IH('r149i', 'areas $150\\sqrt{3} : 30\\sqrt{3} = 5 : 1$', size=30)
r149j = IH('r149j', 'lengths $\\sqrt{5} : \\sqrt{1} = \\sqrt{5} : 1$', size=30)
FLOW([r149a, r149b, r149c, r149d, r149e], QC('geo36-g149'))
FLOW([r149f, r149g, r149h], QC('geo36-g149'))
FLOW([r149i, r149j], QC('geo36-g149'))
NOFIG('solve-geo36-g149', 0, 1, 2)

video('solve-geo36-g149', 'solution', qid='geo36-g149', slides=[
    SM('Method 1 · The math way: polygons', 'The sides',
      L("Now a new question. Two regular hexagons have areas one hundred fifty root three and thirty root three. What is "
        "the ratio of the perimeter of the first hexagon to the perimeter of the second?",
        pt('stem', 'Now a new question', 'hl', 9.0), show(f149a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("So we know the two areas, and they ask about the perimeters. We'll solve it in two different ways."),
      L("Let's start with the math way, with polygons and no similarity. Remember, a regular hexagon is made of six "
        "equilateral triangles.", show(f149a['six'], 'a regular hexagon is made of six')),
      L("An equilateral triangle with side a has the area a squared root three over four. So the hexagon is six times "
        "that.", show(f149a['a'], 'An equilateral triangle with side a')),
      L("For the first hexagon, six times a squared root three over four is equal to one hundred fifty root three.",
        show(r149a, 'For the first hexagon')),
      L("Root three is on both sides, so it cancels. And one hundred fifty divided by six is twenty-five. So a squared "
        "over four is twenty-five.", show(r149b, 'one hundred fifty divided by six')),
      L("We multiply by four, so a squared is one hundred. So a is ten.", show(r149c, 'a squared is one hundred')),
      L("For the second hexagon, let's call its side b. In the same way, thirty divided by six is five. So b squared over "
        "four is five.", show(r149d, 'thirty divided by six')),
      L("So b squared is twenty, and b is root twenty. Twenty is four times five, so root twenty is two root five.",
        show(r149e, 'So b squared is twenty'))),
    SM('Method 1 · The math way: polygons', 'The perimeters',
      L("Now the perimeters. A hexagon has six sides. So the first perimeter is six times ten, and the second is six times "
        "two root five.", show(f149b['line'], 'Now the perimeters'), show(r149f, 'So the first perimeter')),
      L("The sixes cancel, so it's ten to two root five. We divide both by two, and it's five to root five.",
        show(r149g, 'The sixes cancel')),
      L("And five is root five times root five. So we divide both by root five, and it's root five to one.",
        show(r149h, 'And five is root five times'))),
    SM('Method 2 · Understanding: similarity', 'Back to the lengths',
      L("Now with similarity. Two regular hexagons are similar, because they're regular shapes of the same kind.",
        show(f149c['line'], 'Now with similarity')),
      L("The areas give us the area ratio. One hundred fifty root three is five times thirty root three. So the area ratio "
        "is five to one.", show(r149i, 'So the area ratio is five to one')),
      L("From lengths to areas we square. So from areas back to lengths, we take the square root. Root five to root one, "
        "which is root five to one.", show(r149j, 'Root five to root one')),
      L("A perimeter is a line, so the perimeters keep that linear ratio, root five to one. All we did was go back from "
        "the area ratio to the linear ratio."),
      L("Careful with five to one. That's the area ratio, without the root. And twenty-five to one squares it again.",
        mk('cross', 'choice 3', 'Careful with five to one'), mk('cross', 'choice 2', 'And twenty-five to one')),
      L("Choice number one is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])


# =================================================================================================================
# solve-geo36-g150 - a small ball inside a glass globe; the small diameter = half the globe's radius
# Hebrew geo 8492-8518 (a rattle: the small diameter = the big radius -> 1 : 2 -> 1 : 8 -> 7): "a psychometric approach
# only": two spheres are similar solids -> the linear ratio to the power of three; the linear ratio from the givens (a
# diameter = two small radii); "1 : 8, but we're not done" -> the difference 8 - 1 = 7 units -> 7 : 1. English: the extra
# half -> 1 : 4 -> 1 : 64 -> 63 : 1 (radius with radius). Traps 64 : 1 (no subtraction), 16 : 1 / 15 : 1 (squared).
# V3: the copy's big radius orange (R), the small diameter teal, then the small radius; the units 1 and 64.
# =================================================================================================================
f150a = PIN(GEO('f150a', [
    ('line', [qraw('geo36-g150')]),
    ('R', [sg((320, 180), (429.5, 180), 'orange', 6), ('txt', 300, 205, 'R', 'orange', 30, True)]),
    ('d', [sg((344.6, 180), (399.4, 180), 'teal', 7), ('txt', 372, 225, 'd', 'teal', 28, True)]),
    ('r', [sg((372, 180), (399.4, 180), 'red', 7), ('txt', 395, 160, 'r', 'red', 28, True)]),
    ('u', [('txt', 372, 248, '1', 'teal', 28), ('txt', 250, 140, '64', 'orange', 30)]),
], vb='190 50 260 270', w=380, title='The globe and the small ball'))
QLEFT(f150a, 'geo36-g150')
r150a = IH('r150a', '$d = \\frac{1}{2}R$', size=30)
r150b = IH('r150b', '$r = \\frac{1}{2}d = \\frac{1}{4}R$', size=30)
r150c = IH('r150c', 'radii $1 : 4$', size=30)
r150d = IH('r150d', 'volumes $1^3 : 4^3 = 1 : 64$', size=30)
r150e = IH('r150e', 'difference: $64 - 1 = 63$', size=30)
r150f = IH('r150f', '$63 : 1$', size=30)
FLOW([r150a, r150b, r150c, r150d, r150e, r150f], QC2('geo36-g150'))
NOFIG('solve-geo36-g150', 0)

video('solve-geo36-g150', 'solution', qid='geo36-g150', slides=[
    SM('Method 1 · Understanding: similar solids', 'Radius with radius',
      L("Now a new question. A hollow glass globe has a small solid ball inside it. The small ball's diameter is half of "
        "the globe's radius. What is the ratio of the difference between their volumes to the small ball's volume?",
        pt('stem', 'Now a new question', 'hl', 11.0), show(f150a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("So we need two volumes. The small ball, and the difference, the globe minus the small ball. Then we compare "
        "them. We'll solve it by understanding, with similarity."),
      L("Two balls are spheres, and all spheres are similar. So, like in the lesson, the volume ratio is the linear ratio "
        "to the power of three."),
      L("What's the linear ratio? Careful, we must compare a radius with a radius, not a diameter with a radius."),
      L("Let's call the globe's radius R. The small ball's diameter is half of R.", show(f150a['R'], "Let's call the globe"),
        show(f150a['d'], "The small ball's diameter"), show(r150a, 'is half of R')),
      L("A radius is half of a diameter. So the small radius is half of a half of R, a quarter of R.",
        show(f150a['r'], 'A radius is half of a diameter'), show(r150b, 'So the small radius is')),
      L("So the radii are one to four.", show(r150c, 'So the radii are one to four')),
      L("The volumes are one to the power of three, to four to the power of three. Four times four is sixteen, and "
        "sixteen times four is sixty-four. So it's one to sixty-four.", show(r150d, 'Four times four is sixteen')),
      L("But we're not done. The small ball is one unit, and the globe is sixty-four units.", show(f150a['u'], 'The small ball is one unit')),
      L("The difference is sixty-four minus one, sixty-three units. So the difference to the small ball is sixty-three to "
        "one.", show(r150e, 'sixty-four minus one'), show(r150f, 'sixty-three to one')),
      L("Careful with sixty-four to one. That's the whole globe, before we subtract. And sixteen to one and fifteen to "
        "one come from squaring, like areas. But a ball has a volume.", mk('cross', 'choice 1', 'Careful with sixty-four'),
        mk('cross', 'choice 3', 'And sixteen to one'), mk('cross', 'choice 2', 'fifteen to one')),
      L("Choice number four is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])


# =================================================================================================================
# solve-geo36-g151 - a cone container (r, h) filled with a cone scoop (r/2, h/6)
# Hebrew geo 8520-8583 (h/3, r/5 -> 75): "it looks like a 3D question, but we can solve it with PARTIAL SIMILARITY";
# (1) the full math with 3D: both volumes, "we save some work: the denominator is 3 in both, compare only the tops";
# (2) partial similarity: the cones are not similar (different changes), but the bases are circles (similar) and the
# heights are lines -> the height x 3 -> the volume x 3; the radius x 5 -> the base x 25 -> x 75. English: x 6 and
# x 2 -> 6 x 4 = 24. R37: the rule was taught in geo-143 (the height the same way, the radius squared, both: multiply);
# here it gets her name, partial similarity. Traps 12 (6 x 2) and 8 (2 to the power of three, as if similar).
# V3: the copy's height teal, its radius orange; the scoop drawn inside.
# =================================================================================================================
f151a = PIN(GEO('f151a', [
    ('line', [qraw('geo36-g151')]),
    ('hr', [sg((320, 63.2), (320, 296.8), 'teal', 4, True), ('txt', 306, 170, 'h', 'teal', 30, True),
            sg((320, 296.8), (407.6, 296.8), 'orange', 6), ('txt', 364, 330, 'r', 'orange', 30, True)]),
    ('scoop', [('tint', [(276.2, 296.8), (363.8, 296.8), (320, 257.9)], 'red'), ('poly', [(276.2, 296.8), (363.8, 296.8), (320, 257.9)], 'red', 3),
               ('txt', 470, 270, 'scoop', 'red', 24)]),
], vb='200 40 320 310', w=420, title='The container and the scoop'))
QLEFT(f151a, 'geo36-g151')
f151b = PIN(GEO('f151b', [
    ('line', [qraw('geo36-g151')]),
    ('h', [sg((320, 63.2), (320, 296.8), 'teal', 6), ('txt', 296, 170, '× 6', 'teal', 28)]),
    ('r', [sg((320, 296.8), (407.6, 296.8), 'orange', 6), ('txt', 364, 330, '× 2', 'orange', 28)]),
], vb='200 40 320 310', w=420, title='The height times 6, the radius times 2'))
QLEFT(f151b, 'geo36-g151')
r151a = IH('r151a', 'container: $\\frac{πr^2 \\cdot h}{3}$', size=30)
r151b = IH('r151b', '$(\\frac{r}{2})^2 = \\frac{r^2}{4}$', size=30)
r151c = IH('r151c', 'scoop: $\\frac{π \\cdot \\frac{r^2}{4} \\cdot \\frac{h}{6}}{3}$', size=30)
r151d = IH('r151d', '$= \\frac{πr^2h \\div 24}{3}$', size=30)
r151e = IH('r151e', '$πr^2h$ vs $πr^2h \\div 24$', size=30)
r151f = IH('r151f', 'height $\\times 6$: volume $\\times 6$', size=30)
r151g = IH('r151g', 'radius $\\times 2$: base $\\times 4$', size=30)
r151h = IH('r151h', '$6 \\cdot 4 = 24$', size=30)
r151i = IH('r151i', '$6 \\cdot 2 = 12$, $2^3 = 8$: no', size=30)
FLOW([r151a, r151b, r151c, r151d, r151e], QC2('geo36-g151'))
FLOW([r151f, r151g, r151h, r151i], QC('geo36-g151'))
NOFIG('solve-geo36-g151', 0, 1)

video('solve-geo36-g151', 'solution', qid='geo36-g151', slides=[
    SM('Method 1 · The math way: two volumes', 'Two volumes',
      L("Now a new question. A cone-shaped container with base radius r and height h is filled with sand, using a "
        "cone-shaped scoop. The scoop's radius is r over two, and its height is h over six. How many full scoops are needed "
        "to fill the container? No sand is spilled.", pt('stem', 'Now a new question', 'hl', 13.0),
        show(f151a['line'], 'Now a new question'), voice='calm', pause=0.5),
      L("So we need how many times the container's volume is bigger than the scoop's. It looks like a three-dimensional "
        "question, but we can also solve it with similarity. We'll solve it in two different ways."),
      L("Let's start with the math way, with both volumes. The volume of a cone is the base area, times the height, "
        "divided by three. So the container is pi r squared, times h, divided by three.", show(f151a['hr'], 'So the container is'),
        show(r151a, 'So the container is pi')),
      L("The scoop's radius is r over two. To square a fraction, we square the top and the bottom. So it's r squared "
        "over four.", show(f151a['scoop'], "The scoop's radius"), show(r151b, 'To square a fraction')),
      L("So the scoop is pi, times r squared over four, times h over six, divided by three.", show(r151c, 'So the scoop is pi')),
      L("Four times six is twenty-four. So the top is pi r squared h, divided by twenty-four.", show(r151d, 'Four times six is twenty-four')),
      L("Let's save some work. Both volumes are divided by three, so we can compare only the tops. The container's top is "
        "pi r squared h. The scoop's top is the same, divided by twenty-four.", show(r151e, "Let")),
      L("So the container is twenty-four times the scoop. That's twenty-four scoops.")),
    SM('Method 2 · Understanding: partial similarity', 'Partial similarity',
      L("Now by understanding, with partial similarity. The two cones aren't similar. The height changed by six, but the "
        "radius changed by two. For similar cones, both would change by the same number.", show(f151b['line'], 'Now by understanding')),
      L("But some parts are similar. The bases are circles, and all circles are similar. And the heights are lines. So we "
        "look at each part on its own, like in the lesson about volume changes."),
      L("First, the height. From the scoop to the container, the height is six times as big. A height is a line, so the volume "
        "grows six times too.", show(f151b['h'], 'First, the height'), show(r151f, 'A height is a line')),
      L("Now the radius. It's two times as big. The base is a circle, so its area grows two squared, four times. And the "
        "volume grows four times with it.", show(f151b['r'], 'Now the radius'), show(r151g, 'so its area grows')),
      L("Together, six times four, twenty-four.", show(r151h, 'six times four')),
      L("Careful with twelve. That's six times two. It forgets to square the radius's change. And eight is two to the "
        "power of three, as if the cones were similar.", show(r151i, 'Careful with twelve'),
        mk('cross', 'choice 1', 'Careful with twelve'), mk('cross', 'choice 4', 'And eight is two')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# =================================================================================================================
# r26-t36-map-scale (lesson) - Map scale
# No Hebrew source (the topic title "and scale" is English-only); kept, and verified against the real exam: 2026 spring
# q1_18 (the smallest scale at which two buildings 5 m apart can be told apart, 1 : 50,000). R37: the core method of the
# two map questions is taught here, on numbers (was a 2-slide overview): the scale = the linear ratio; the unit ladder
# (cm -> m -> km, divide by 100, then by 1000); lengths both ways (6 cm -> 3 km, 4 km -> 8 cm); finding the scale (3 km on
# 6 cm -> 1 : 50,000; a bigger number = a smaller map); areas with the scale squared ("first change ONE map centimeter
# into the real unit, then square": 1 cm2 -> a quarter of a km2; 8 cm2 -> 2 km2, the trap 4).
# Visuals: the unit ladder built step by step; one map square and its real square.
# =================================================================================================================
f300a = G('f300a', [
    ('line', [('txt', 80, 120, 'cm', 'ink', 34)]),
    ('m', [('seg', 120, 120, 230, 120, 'teal', 4), ('raw', '<path d="M 236 120 l -14 -8 l 0 16 Z" fill="%s"/>' % GTEAL),
           ('txt', 175, 98, '÷ 100', 'teal', 26), ('txt', 270, 120, 'm', 'ink', 34)]),
    ('km', [('seg', 300, 120, 410, 120, 'orange', 4), ('raw', '<path d="M 416 120 l -14 -8 l 0 16 Z" fill="%s"/>' % GORANGE),
            ('txt', 355, 98, '÷ 1000', 'orange', 26), ('txt', 455, 120, 'km', 'ink', 34)]),
], vb='40 70 460 80', w=520, title='The unit ladder: centimeters, meters, kilometers')
r300a = H36('r300a', '$1 : 50000$')
r300b = H36('r300b', '$1$ cm on the map $= 50000$ cm')
r300c = H36('r300c', '$50000 \\div 100 = 500$ m')
r300d = H36('r300d', '$500 \\div 1000 = 0.5$ km')
r300e = H36('r300e', '$6 \\cdot 0.5 = 3$ km')
r300f = H36('r300f', '$4$ km $= 4 \\cdot 2 = 8$ cm')
r300g = H36('r300g', '$3$ km $= 3000$ m $= 300000$ cm')
r300h = H36('r300h', '$300000 \\div 6 = 50000$')
r300i = H36('r300i', 'scale $1 : 50000$')
f300b = G('f300b', [
    ('line', [('poly', [(40, 260), (90, 260), (90, 210), (40, 210)], 'ink', 3), ('txt', 65, 285, '1 cm', 'ink', 22),
              ('txt', 65, 190, 'map', 'ink', 22)]),
    ('real', [('tint', [(170, 260), (370, 260), (370, 60), (170, 60)], 'teal'), ('poly', [(170, 260), (370, 260), (370, 60), (170, 60)], 'teal', 3),
              ('txt', 270, 285, '0.5 km', 'teal', 22), ('txt', 415, 160, '0.5 km', 'teal', 22), ('txt', 270, 160, 'real', 'teal', 24)]),
], vb='20 40 450 270', w=520, title='One map square centimeter and its real square')
r300j = H36('r300j', '$1$ cm$^2$ $\\to$ $0.5 \\cdot 0.5 = 0.25$ km$^2$')
r300k = H36('r300k', '$8 \\cdot 0.25 = 2$ km$^2$')
r300l = H36('r300l', '$8 \\cdot 0.5 = 4$: not squared')
z300a = I('z300a', 'Scale $1 : n$: lengths $\\times n$ $\\cdot$ areas $\\times n^2$', size=30)
z300b = I('z300b', 'cm $\\div 100$ $\\to$ m $\\div 1000$ $\\to$ km', size=30)
z300c = I('z300c', 'Areas: change ONE map cm first, then square it', size=30)

video('r26-t36-map-scale', 'lesson', slides=[
    S('Map Scale',
      L("Welcome back. The last part of the topic is scale."),
      L("A map is a similar copy of the real world, only much smaller. So everything we learned about similarity works on "
        "maps.")),
    S('What a scale means',
      L("The scale is a ratio. A length on the map, to the same length in reality."),
      L("Say the scale is one to fifty thousand. Every centimeter on the map is fifty thousand centimeters in reality.",
        show(r300a, 'Say the scale is'), show(r300b, 'Every centimeter on the map')),
      L("The map and the land are similar shapes, and the scale is their linear ratio. So every real length is fifty "
        "thousand times the length on the map.")),
    S('The unit ladder',
      L("Fifty thousand centimeters isn't a useful distance. So we change the units, step by step, like on a ladder.",
        show(f300a['line'], 'So we change the units')),
      L("From centimeters to meters, we divide by a hundred, because a meter is a hundred centimeters.",
        show(f300a['m'], 'From centimeters to meters')),
      L("From meters to kilometers, we divide by a thousand, because a kilometer is a thousand meters.",
        show(f300a['km'], 'From meters to kilometers')),
      L("So fifty thousand centimeters is fifty thousand divided by a hundred, five hundred meters.", show(r300c, 'five hundred meters')),
      L("And five hundred meters is five hundred divided by a thousand, half a kilometer.", show(r300d, 'half a kilometer')),
      L("So on this map, one centimeter is half a kilometer in reality.")),
    S('Lengths, both ways',
      L("Now on numbers. On this map, two towns are six centimeters apart. How far apart are they really?"),
      L("Every map centimeter is half a kilometer. So six centimeters are six halves, three kilometers.", show(r300e, 'six halves')),
      L("And backwards. Two towns are really four kilometers apart. How far apart are they on the map?"),
      L("One centimeter is half a kilometer, so each kilometer is two map centimeters. So four kilometers are four times "
        "two, eight centimeters.", show(r300f, 'four times two'))),
    S('Finding the scale',
      L("Sometimes they give both distances, and ask for the scale. Say three kilometers in reality are six centimeters on "
        "the map."),
      L("First we write both in centimeters. Three kilometers are three thousand meters, and three thousand meters are "
        "three hundred thousand centimeters.", show(r300g, 'Three kilometers are three thousand meters')),
      L("So six map centimeters are three hundred thousand real centimeters. One map centimeter is three hundred thousand "
        "divided by six, fifty thousand.", show(r300h, 'divided by six')),
      L("So the scale is one to fifty thousand.", show(r300i, 'So the scale is one')),
      L("And remember, a bigger number in the scale means a smaller map. On a scale of one to two hundred, a house is "
        "big. On one to fifty thousand, it's only a dot.")),
    S('Areas: the scale squared',
      L("Now areas. The map and the land are similar. So, like any similar shapes, the areas use the scale squared."),
      L("Here's the easiest way. First change one map centimeter into the real unit they want. Then square it."),
      L("On our map, one centimeter is half a kilometer. So one square centimeter on the map is a real square, half a "
        "kilometer by half a kilometer.", show(f300b['line'], 'one square centimeter on the map'), show(f300b['real'], 'a real square')),
      L("Half times half is a quarter. So it's a quarter of a square kilometer.", show(r300j, 'Half times half')),
      L("So a lake of eight square centimeters on the map is eight quarters, two square kilometers.", show(r300k, 'eight quarters')),
      L("Be careful here. A lot of students multiply eight by half a kilometer, and get four. That forgets to square.",
        show(r300l, 'and get four'))),
    S('Recap',
      L("Let's sum up. The scale is the linear ratio between the map and reality. Lengths are multiplied by the scale, and "
        "areas by the scale squared.", show(z300a, 'The scale is the linear ratio')),
      L("Change units with the ladder, step by step.", show(z300b, 'Change units with the ladder')),
      L("And for areas, change one map centimeter into the real unit first. Then square it.", show(z300c, 'And for areas')),
      L("Take a moment to memorize this, and I'll see you in the next video.")),
])


# =================================================================================================================
# solve-q-r26-t36-04 - scale 1 : 20,000, 7.5 cm on the map: the real distance in km
# English addition (kept). R37: the first question after the map lesson - the ladder applied slowly. Method 1: the real
# length in cm, then the ladder; method 2: one map centimeter first (0.2 km), then times 7.5. The three unit-mistake
# choices (15, 150, 0.15) are each one decimal step off.
# =================================================================================================================
r04a = IH('r04a', '$7.5 \\cdot 2 = 15$', size=30)
r04b = IH('r04b', '$7.5 \\cdot 20000 = 150000$ cm', size=30)
r04c = IH('r04c', '$150000 \\div 100 = 1500$ m', size=30)
r04d = IH('r04d', '$1500 \\div 1000 = 1.5$ km', size=30)
r04e = IH('r04e', '$1$ cm $\\to$ $20000$ cm $= 200$ m $= 0.2$ km', size=30)
r04f = IH('r04f', '$7.5 \\cdot 0.2 = 1.5$ km', size=30)
FLOW([r04a, r04b, r04c, r04d], QW('q-r26-t36-04'))
FLOW([r04e, r04f], QW('q-r26-t36-04'))

video('solve-q-r26-t36-04', 'solution', qid='q-r26-t36-04', slides=[
    SM('Method 1 · The math way: the unit ladder', 'Map to reality',
      L("Now a new question. A map has a scale of one to twenty thousand. On the map, the distance between two towns is "
        "seven point five centimeters. What is the real distance between the towns, in kilometers?",
        pt('stem', 'Now a new question', 'hl', 10.0), voice='calm', pause=0.5),
      L("So we know a distance on the map, and we need the real distance, in kilometers. We'll solve it in two different "
        "ways."),
      L("Let's start with the math way. Like in the lesson, the scale tells us that every real length is twenty thousand "
        "times the length on the map."),
      L("So it's seven point five times twenty thousand. Seven point five times two is fifteen.", show(r04a, 'Seven point five times two')),
      L("Twenty thousand is two times ten thousand. So it's fifteen times ten thousand, a hundred fifty thousand. That's "
        "in centimeters.", show(r04b, 'a hundred fifty thousand')),
      L("Now we climb the ladder. From centimeters to meters, we divide by a hundred. A hundred fifty thousand divided by "
        "a hundred is one thousand five hundred meters.", show(r04c, 'we divide by a hundred')),
      L("From meters to kilometers, we divide by a thousand. That's one point five kilometers.", show(r04d, 'we divide by a thousand'))),
    SM('Method 2 · The math way: one centimeter first', 'One centimeter first',
      L("Now another way. First we change one map centimeter into kilometers. Twenty thousand centimeters are two hundred "
        "meters, and two hundred meters are zero point two kilometers.", show(r04e, 'Twenty thousand centimeters are')),
      L("So seven point five centimeters are seven point five times zero point two. Seven point five times two is fifteen, "
        "so seven point five times zero point two is one point five kilometers.", show(r04f, 'seven point five times zero point two')),
      L("The other choices are unit mistakes. Fifteen and zero point one five are one step of the decimal point away. A "
        "hundred fifty is two steps away. So climb the ladder step by step.", mk('cross', 'choice 1', 'Fifteen and zero'),
        mk('cross', 'choice 4', 'zero point one five'), mk('cross', 'choice 3', 'hundred fifty is two steps')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# =================================================================================================================
# solve-q-r26-t36-05 - scale 1 : 40,000, a lake of 5 cm2 on the map: the real area in km2
# English addition (kept), the map lesson's area rule ("one map centimeter first, then square"): 1 cm -> 0.4 km ->
# 1 cm2 -> 0.16 km2 -> 5 x 0.16 = 0.8. The trap 2 (5 x 0.4, not squared) at its step; 8 and 0.08 one decimal step off.
# =================================================================================================================
r05a = IH('r05a', '$40000$ cm $= 400$ m $= 0.4$ km', size=30)
r05b = IH('r05b', '$1$ cm$^2$ $\\to$ $0.4 \\cdot 0.4 = 0.16$ km$^2$', size=30)
r05c = IH('r05c', '$4 \\cdot 4 = 16$', size=30)
r05d = IH('r05d', '$5 \\cdot 0.16 = 0.8$ km$^2$', size=30)
r05e = IH('r05e', '$5 \\cdot 0.4 = 2$: not squared', size=30)
FLOW([r05a, r05b, r05c, r05d, r05e], QW('q-r26-t36-05'))

video('solve-q-r26-t36-05', 'solution', qid='q-r26-t36-05', slides=[
    SM('Method 1 · The math way: one centimeter first', 'One centimeter, then square',
      L("Now a new question. A map has a scale of one to forty thousand. A lake covers five square centimeters on the map. "
        "What is the real area of the lake, in square kilometers?", pt('stem', 'Now a new question', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("So we know an area on the map, and we need the real area, in square kilometers. It's an area, so the scale will "
        "be squared."),
      L("Like in the lesson, first we change one map centimeter into kilometers. Forty thousand centimeters are four "
        "hundred meters, and four hundred meters are zero point four kilometers.", show(r05a, 'Forty thousand centimeters are')),
      L("Now the area. One square centimeter on the map is a real square, zero point four kilometers by zero point four "
        "kilometers.", show(r05b, 'One square centimeter on the map')),
      L("Four times four is sixteen, so zero point four times zero point four is zero point one six square kilometers.",
        show(r05c, 'Four times four is sixteen')),
      L("The lake is five square centimeters. Five times zero point one six is zero point eight. So the lake is zero point "
        "eight square kilometers.", show(r05d, 'Five times zero point one six')),
      L("Careful with two. That's five times zero point four, without squaring. And eight and zero point zero eight are "
        "one step of the decimal point away.", show(r05e, 'Careful with two'), mk('cross', 'choice 2', 'Careful with two'),
        mk('cross', 'choice 4', 'And eight and'), mk('cross', 'choice 1', 'zero point zero eight')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
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
STEMS = QSTEM   # "=?" stems and stems with no "Given:": the whole stem only
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
MV.carry(_types.SimpleNamespace(**globals()), CARRY36)
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
