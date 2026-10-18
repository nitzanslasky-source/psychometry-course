"""Topic 32 (Quadrilaterals) - the scripts for the teacher's own-voice reading (2026-10-14), written from the first draft to
the Codex review standard, the clarity style, the method visuals (geometry: the angle figure built in layers, GEO below), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py / _ai_vis_t16.py / _ai_vis_t17.py / _ai_vis_t18.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The camera lesson 'geo-042' gets its own reading script here too, in parts of about 3-4 minutes (2026-10-14: she reads it
with the camera on). Every other topic-32 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t32.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t32.py ai_redo_t32() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods and EVERY method of the Hebrew solution (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-32-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

Spec DSL (as in topic 13)
  video(vid, kind, slides, qid=None)        kind 'solution' (every slide is a question slide with the question pre-loaded)
                                            or 'lesson' (slide 1 is the title slide, the rest concept slides)
  S(title, *lines, sb=None)                 a slide; sb = its sidebar label (default: the title)
  L(say, *cues, voice=None, pause=None)     one spoken paragraph (= one script line); [short pause] / [pause] tags allowed
  I(name, tex, size=36, col=0, hand=None)   a board item: col 0 = left column, col 1 = right column; hand = its
                                            hand-written text (studio_handwrite.py syntax) - the item becomes a 'write' cue
  NL / STRIP / TREE                         figures: a figure item; a number strip built in layers; a factor ladder built
                                            in layers (show the layers in order)
  cues: show(item, phrase) · pt(target, phrase, style=None, dur=None) · mk(kind, target, phrase)
        target = 'stem' | 'choice N' | 'fig: label' | '<item name>' | '<item name>: <\\hl part>'
        phrase = a phrase of this line ("<phrase" = of the previous line)
"""
import importlib.util, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _geo_hand as _GH

HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t32ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-32 flow order of the scripts
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
            out.append((it, d))
        per.append(out)
    return names, per


# 2026-10-14 Rule V4.8 (camera lessons: the face bubble never covers math). Her bubble is composited top right (board
# x >= 1344, y <= 256). In the camera lesson and its parts: a right-column stack that would start above y 262 moves down
# as a whole (its own order and spacing kept), and a left-column item is at most 920 wide (ends left of x 1330; a figure
# and its layers are scaled down together, text wraps). Other videos are unchanged.
CAM_BASE = 'geo-042'
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
            'style': "the teacher reads it herself (Reading Studio), topic-32 scripts (2026-10-14): math_patches/_ai_vis_t32.py is "
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


_studio_slides_plain = studio_slides


def studio_slides(vid):
    out, sb = _studio_slides_plain(vid)
    if vid in FIG_LEFT:
        for b in out:
            for it in b['pre']: it.update(figw=0.56, figalign='left')
    for k, b in enumerate(out):
        if (vid, k) in NOFIG32:
            for it in b['pre']: it.update(nofig=1)
    return out, sb


NOFIG32 = set()     # 2026-10-18 (batch C): (video, slide index) whose working needs the whole board (no question figure)


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


# ------------------------------------------------------------------------------------------- topic-32 geometry figures (V1)
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
    if k == 'wipe':         # ('wipe', x, y, w, h)  2026-10-18: hides what is drawn there (an old label / an old template)
        return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#ffffff"/>' % tuple(e[1:5])
    if k == 'wipep':        # ('wipep', [(x, y), ...])  2026-10-18: hides a region (a piece that was cut out and moved)
        return '<path d="M %s Z" fill="#ffffff" stroke="none"/>' % ' L '.join('%.1f %.1f' % tuple(p) for p in e[1])
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



CARRY32 = {}       # carry-over boxes (V2): {vid: {slide index: [tex, ...]}}, filled by the scripts


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


# ------------------------------------------------------------------------------------------------ geo-042 (camera lesson, in parts)
# 2026-10-14 her camera first lesson of quadrilaterals as a reading script (camera on), with more examples, split into
# parts of about 3-4 minutes (CAMERA_SPLIT at the end). Hebrew: geo 1729-1790 (the quadrilaterals intro lesson): the
# kingdom of quadrilaterals; a quadrilateral = a closed shape with 4 sides; one angle can even be bigger than 180; the
# angle sum 360 with its proof (a diagonal makes two triangles, the blue and the green angles); "almost the only rule for a
# general quadrilateral"; the family (square, rectangle, parallelogram, rhombus, kite, trapezoid) and how one turns into
# another (stretch, step on it / squash, shorten, turn it like on playing cards, move the sides); next: a lesson on each one,
# starting with the square. Kept from the English lesson: "if the question doesn't say so, don't add it", the names carry
# information (underline the name), the family tree ("a special kind of": down the tree a shape gains properties, up the
# tree "not necessarily").
# Added examples: two more quadrilaterals and two non-examples (an open shape, five sides); three angle-sum examples
# (a regular one, one with two right angles, one with an angle bigger than 180), each drawn with its real angles.
# Study plan: day 5, after 1, 30, 2, 4, 31, 6, 8 - the triangle angle sum (topic 31) is a short reminder.
# Visuals (V3): every figure built step by step at her words; the sides numbered as they are counted; a non-example red;
# the diagonal dashed teal (a line we add); the two triangles' angles teal and orange (her blue and green); values written
# on the figure when found; the family shapes appear one after another with the move written on the arrow.
import math as _f1m


def f1_poly(pts, col='ink', w=3):
    n = len(pts)
    return [('seg', pts[i][0], pts[i][1], pts[(i + 1) % n][0], pts[(i + 1) % n][1], col, w) for i in range(n)]


def f1_names(pts, names, d=26, size=26):
    gx = sum(p[0] for p in pts) / float(len(pts)); gy = sum(p[1] for p in pts) / float(len(pts)); out = []
    for p, nm in zip(pts, names):
        L = _f1m.hypot(p[0] - gx, p[1] - gy) or 1
        out.append(('txt', p[0] + (p[0] - gx) / L * d, p[1] + (p[1] - gy) / L * d, nm, 'ink', size, True))
    return out


def f1_inner(pts, i, r, col, lab=None, lr=None):
    """the interior angle arc at vertex i of a polygon listed counter-clockwise on the screen (any order works for convex;
    for a concave vertex the arc is the reflex one): measured inside the shape"""
    n = len(pts); p, a, b = pts[i], pts[i - 1], pts[(i + 1) % n]
    d1, d2 = gdir(p[0], p[1], b[0], b[1]), gdir(p[0], p[1], a[0], a[1])
    # the interior side: test the middle direction with a point just inside
    mid = (d1 + ((d2 - d1) % 360) / 2.0) % 360
    t = gpt(p[0], p[1], 6, mid)
    if not f1_inside(t, pts): d1, d2 = d2, d1
    e = ('arc', p[0], p[1], r, d1, d2, col)
    if lab: e = e + (lab, lr if lr else r + 24)
    return e


def f1_inside(q, pts):
    x, y = q; c = False; n = len(pts)
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / float(y2 - y1): c = not c
    return c


def f1_ang(pts, i):
    """the interior angle at vertex i, in degrees (reflex if concave)"""
    n = len(pts); p, a, b = pts[i], pts[i - 1], pts[(i + 1) % n]
    d1, d2 = gdir(p[0], p[1], b[0], b[1]), gdir(p[0], p[1], a[0], a[1])
    mid = (d1 + ((d2 - d1) % 360) / 2.0) % 360
    s = (d2 - d1) % 360
    return s if f1_inside(gpt(p[0], p[1], 6, mid), pts) else 360 - s


def f1_ray(p, deg, L):
    return gpt(p[0], p[1], L, deg)


# ================================================================ part 1: what a quadrilateral is, and its angles
# ---- a general quadrilateral, the sides counted 1, 2, 3, 4
F1Q = [(150, 300), (470, 320), (520, 110), (230, 70)]
_qm = [((F1Q[i][0] + F1Q[(i + 1) % 4][0]) / 2.0, (F1Q[i][1] + F1Q[(i + 1) % 4][1]) / 2.0) for i in range(4)]
_qg = (sum(p[0] for p in F1Q) / 4.0, sum(p[1] for p in F1Q) / 4.0)
def _f1_out(m, d=26):
    L = _f1m.hypot(m[0] - _qg[0], m[1] - _qg[1]); return (m[0] + (m[0] - _qg[0]) / L * d, m[1] + (m[1] - _qg[1]) / L * d)
f1what = GEO('f1what', [
    ('line', [('dot', *F1Q[0]), ('dot', *F1Q[1]), ('dot', *F1Q[2]), ('dot', *F1Q[3])]),
    ('s1', [('seg', *F1Q[0], *F1Q[1], 'teal', 4), ('txt', *_f1_out(_qm[0]), '1', 'teal', 28)]),
    ('s2', [('seg', *F1Q[1], *F1Q[2], 'teal', 4), ('txt', *_f1_out(_qm[1]), '2', 'teal', 28)]),
    ('s3', [('seg', *F1Q[2], *F1Q[3], 'teal', 4), ('txt', *_f1_out(_qm[2]), '3', 'teal', 28)]),
    ('s4', [('seg', *F1Q[3], *F1Q[0], 'teal', 4), ('txt', *_f1_out(_qm[3]), '4', 'teal', 28),
            ('txt', 335, 200, 'closed, 4 sides', 'teal', 26)]),
], vb='60 30 560 330', w=900, col=0, title='A quadrilateral: a closed shape with four sides')

# ---- more examples and two non-examples, one panel at a time
_e1 = [(40, 250), (170, 270), (190, 120), (70, 150)]
_e2 = [(250, 270), (380, 240), (350, 100), (230, 160)]
_n1 = [(450, 270), (580, 270), (590, 150), (525, 100), (462, 150)]   # open: four sides, but the ends don't meet (a gap)
_p5 = [(640, 270), (770, 270), (790, 170), (710, 100), (630, 170)]
f1more = GEO('f1more', [
    ('line', f1_poly(_e1) + [('txt', 115, 310, 'quadrilateral', 'teal', 22)]),
    ('e2', f1_poly(_e2) + [('txt', 315, 310, 'quadrilateral', 'teal', 22)]),
    ('n1', [('seg', *_n1[0], *_n1[1], 'red', 3), ('seg', *_n1[1], *_n1[2], 'red', 3), ('seg', *_n1[2], *_n1[3], 'red', 3),
            ('seg', *_n1[3], *_n1[4], 'red', 3), ('dot', *_n1[0]), ('dot', *_n1[4]), ('txt', 432, 212, 'gap', 'red', 20),
            ('txt', 520, 310, '4 sides, not closed ✗', 'red', 22)]),
    ('n2', f1_poly(_p5, 'red') + [('txt', 710, 310, '5 sides ✗', 'red', 22)]),
], vb='0 70 820 260', w=1000, col=0, title='Two more quadrilaterals and two shapes that are not')

# ---- an angle bigger than 180 (a concave quadrilateral)
F1K = [(140, 310), (520, 310), (330, 220), (300, 50)]
_kA = f1_ang(F1K, 2)
f1bend = GEO('f1bend', [
    ('line', f1_poly(F1K) + f1_names(F1K, ['A', 'B', 'C', 'D'])),
    ('big', [f1_inner(F1K, 2, 30, 'orange'), ('txt', 440, 190, 'more than 180°', 'orange', 24)]),
    ('four', [('txt', 520, 120, 'still 4 sides', 'teal', 26)]),
], vb='80 -5 520 355', w=860, col=0, title='A quadrilateral with an angle bigger than 180 degrees')

# ---- the proof: a diagonal makes two triangles
F1P = [(130, 300), (500, 320), (545, 110), (230, 60)]          # A B C D
_A, _B, _C, _D = F1P
def _f1_part(p, a, b, r, col):
    d1, d2 = gdir(p[0], p[1], a[0], a[1]), gdir(p[0], p[1], b[0], b[1])
    if (d2 - d1) % 360 > 180: d1, d2 = d2, d1
    return ('arc', p[0], p[1], r, d1, d2, col)
f1sum = GEO('f1sum', [
    ('line', f1_poly(F1P) + f1_names(F1P, ['A', 'B', 'C', 'D'])),
    ('diag', [('seg', *_B, *_D, 'teal', 3, True)]),
    ('t1', [('tint', [_A, _B, _D], 'teal'), _f1_part(_A, _B, _D, 30, 'teal'), _f1_part(_B, _A, _D, 34, 'teal'),
            _f1_part(_D, _A, _B, 34, 'teal'), ('txt', 270, 250, '180°', 'teal', 30)]),
    ('t2', [('tint', [_B, _C, _D], 'orange'), _f1_part(_C, _B, _D, 30, 'orange'), _f1_part(_B, _C, _D, 46, 'orange'),
            _f1_part(_D, _B, _C, 46, 'orange'), ('txt', 420, 170, '180°', 'orange', 30)]),
    ('all', [('txt', 330, 352, '180° + 180° = 360°', 'ink', 30)]),
], vb='80 20 640 360', w=920, col=0, title='A diagonal splits a quadrilateral into two triangles')

# ---- using the angle sum: three examples, each drawn with its real angles
def _f1_quad(A, a_deg, AB, b_deg, BC, c_deg):
    """a quadrilateral A B C D (counter-clockwise on the screen) with the interior angles a, b, c at A, B, C"""
    B = (A[0] + AB, A[1])
    dBC = 180 - b_deg; C = gpt(B[0], B[1], BC, dBC)
    dCD = dBC + (180 - c_deg)
    D = gcross(C, gpt(C[0], C[1], 100, dCD), A, gpt(A[0], A[1], 100, a_deg))
    return [A, B, C, D]
_x1 = _f1_quad((40, 300), 80, 230, 95, 150, 110)
_x2 = _f1_quad((330, 300), 90, 150, 90, 130, 120)
# the concave one: tips 30 at A, 40 at B, 50 at D, the angle at C bigger than 180
_cA, _cB = (60, 300), (600, 300)
_cD = gpt(_cA[0], _cA[1], 470, 30)
_cC = gcross(_cB, gpt(_cB[0], _cB[1], 100, 140), _cD, gpt(_cD[0], _cD[1], 100, 260))
_x3 = [_cA, _cB, _cC, _cD]
F1X = (_x1, _x2, _x3)
f1use = GEO('f1use', [
    ('line', f1_poly(_x1) + [f1_inner(_x1, 0, 26, 'teal', '80°', 50), f1_inner(_x1, 1, 26, 'teal', '95°', 50),
                             f1_inner(_x1, 2, 24, 'teal', '110°', 50), ('txt', _x1[3][0] - 6, _x1[3][1] - 28, 'x', 'red', 28, True)]),
    ('x1', [f1_inner(_x1, 3, 24, 'red', '75°', 50)]),
], vb='0 15 330 330', w=520, col=0, title='A quadrilateral and its angle sum')
f1useB = GEO('f1useB', [
    ('line', f1_poly(_x2) + [('right', _x2[0][0], _x2[0][1], 0, 90, 16), ('right', _x2[1][0], _x2[1][1], 90, 180, 16),
                            f1_inner(_x2, 2, 26, 'teal', '120°', 52), ('txt', _x2[3][0] + 14, _x2[3][1] - 24, 'y', 'red', 28, True)]),
    ('x2', [f1_inner(_x2, 3, 26, 'red', '60°', 54)]),
], vb='290 40 240 290', w=430, col=0, title='A quadrilateral with two right angles, and its angle sum')
f1use3 = GEO('f1use3', [
    ('line', f1_poly(_x3) + f1_names(_x3, ['A', 'B', 'C', 'D']) + [f1_inner(_x3, 0, 60, 'teal', '30°', 92),
              f1_inner(_x3, 1, 50, 'teal', '40°', 84), f1_inner(_x3, 3, 44, 'teal', '50°', 72)]),
    ('x3', [f1_inner(_x3, 2, 26, 'red'), ('txt', _cC[0] + 10, _cC[1] + 56, '240°', 'red', 28)]),
], vb='20 10 640 340', w=600, col=0, title='A quadrilateral with an angle bigger than 180, and its angle sum')
# 2026-10-18 (batch C #211): every step its own row, at its own clause (no result before it is said); the rows sit to the
# right of the figure (below the face bubble), so the figure keeps its size
f1u1a = _R(IH('f1u1a', '$80°+95°=175°$', size=32), 290, x=1000)
f1u1b = _R(IH('f1u1b', '$175°+110°=285°$', size=32), 362, x=1000)
f1u1c = _R(IH('f1u1c', '$x=360°-285°$', size=32), 434, x=1000)
f1u1d = _R(IH('f1u1d', '$360°-280°=80°$', size=32), 506, x=1000)
f1u1e = _R(IH('f1u1e', '$80°-5°=75°$', size=32), 578, x=1000)
f1u2a = _R(IH('f1u2a', '$90°+90°=180°$', size=32), 290, x=1000)
f1u2b = _R(IH('f1u2b', '$180°+120°=300°$', size=32), 362, x=1000)
f1u2c = _R(IH('f1u2c', '$y=360°-300°$', size=32), 434, x=1000)
f1u2d = _R(IH('f1u2d', '$y=60°$', size=32), 506, x=1000)
f1u3a = _R(IH('f1u3a', '$30°+40°=70°$', size=32), 290, x=1040)
f1u3b = _R(IH('f1u3b', '$70°+50°=120°$', size=32), 362, x=1040)
f1u3c = _R(IH('f1u3c', '$360°-120°$', size=32), 434, x=1040)
f1u3d = _R(IH('f1u3d', '$=240°$', size=32), 506, x=1040)

# ================================================================ part 2: the family
_sq = [(40, 260), (160, 260), (160, 140), (40, 140)]
_re = [(250, 260), (450, 260), (450, 160), (250, 160)]
_pa = [(540, 260), (720, 260), (770, 160), (590, 160)]
def _f1_arrow(x1, x2, y, text):
    return [('seg', x1, y, x2 - 10, y, 'teal', 3), ('seg', x2 - 22, y - 9, x2 - 8, y, 'teal', 3),
            ('seg', x2 - 22, y + 9, x2 - 8, y, 'teal', 3), ('txt', (x1 + x2) / 2.0, y - 26, text, 'teal', 22)]
f1fam1 = GEO('f1fam1', [
    ('line', f1_poly(_sq) + [('txt', 100, 300, 'square', 'ink', 24)]),
    ('re', _f1_arrow(170, 240, 200, 'stretch') + f1_poly(_re) + [('txt', 350, 300, 'rectangle', 'ink', 24)]),
    ('pa', _f1_arrow(460, 535, 200, 'squash') + f1_poly(_pa) + [('txt', 655, 300, 'parallelogram', 'ink', 24)]),
], vb='20 110 780 220', w=1060, col=0, title='Square, rectangle, parallelogram')

_pa2 = [(40, 260), (220, 260), (270, 170), (90, 170)]
_rh = [(370, 260), (480, 260), (540, 160), (430, 160)]          # all sides about 110-117: a rhombus lying down
_dia = [(760, 290), (820, 200), (760, 110), (700, 200)]          # the same rhombus turned onto a corner
f1fam2 = GEO('f1fam2', [
    ('line', f1_poly(_pa2) + [('txt', 155, 300, 'parallelogram', 'ink', 24)]),
    ('rh', _f1_arrow(280, 360, 215, 'shorten') + f1_poly(_rh) + [('txt', 455, 300, 'rhombus', 'ink', 24),
           ('tick', 370, 260, 480, 260), ('tick', 480, 260, 540, 160), ('tick', 540, 160, 430, 160), ('tick', 430, 160, 370, 260)]),
    ('turn', _f1_arrow(570, 680, 215, 'turn it') + f1_poly(_dia) + [('txt', 760, 325, 'rhombus', 'ink', 24),
             ('tick', 760, 290, 820, 200), ('tick', 820, 200, 760, 110), ('tick', 760, 110, 700, 200), ('tick', 700, 200, 760, 290)]),
], vb='20 90 840 260', w=1060, col=0, title='Parallelogram, rhombus, a rhombus on its corner')

_sq2 = [(60, 260), (170, 260), (170, 150), (60, 150)]
_rh2 = [(330, 275), (390, 205), (330, 135), (270, 205)]
f1sqrh = GEO('f1sqrh', [
    ('line', f1_poly(_sq2) + [('txt', 115, 300, 'square', 'ink', 24)]),
    ('rh', _f1_arrow(185, 260, 205, 'squash') + f1_poly(_rh2) + [('txt', 330, 310, 'rhombus', 'ink', 24),
           ('tick', 330, 275, 390, 205), ('tick', 390, 205, 330, 135), ('tick', 330, 135, 270, 205), ('tick', 270, 205, 330, 275)]),
], vb='30 110 400 220', w=560, col=0, title='A squashed square is a rhombus')

_rh3 = [(150, 300), (220, 200), (150, 100), (80, 200)]
_ki = [(420, 310), (480, 170), (420, 110), (360, 170)]          # a kite: two short sides at the top, two long ones below
_re2 = [(560, 270), (740, 270), (740, 170), (560, 170)]
_tz = [(900, 270), (1100, 270), (1050, 170), (950, 170)]
f1fam3 = GEO('f1fam3', [
    ('line', f1_poly(_rh3) + [('txt', 150, 340, 'rhombus', 'ink', 24)]),
    ('ki', _f1_arrow(240, 345, 200, 'pull a corner') + f1_poly(_ki) + [('txt', 420, 345, 'kite (deltoid)', 'ink', 24),
           ('tick', 420, 110, 480, 170), ('tick', 420, 110, 360, 170), ('tick', 480, 170, 420, 310, 2), ('tick', 360, 170, 420, 310, 2)]),
    ('re', f1_poly(_re2) + [('txt', 650, 310, 'rectangle', 'ink', 24)]),
    ('tz', _f1_arrow(755, 890, 220, 'move 2 corners') + f1_poly(_tz) + [('txt', 1000, 310, 'trapezoid', 'ink', 24),
           ('par', 950, 170, 1050, 170), ('par', 900, 270, 1100, 270)]),
], vb='40 80 1080 290', w=1060, col=0, title='Rhombus to kite, rectangle to trapezoid')

# ---- the family tree: read every arrow as "a special kind of"
_nodes = {'Q': (380, 50, 'quadrilateral'), 'T': (140, 150, 'trapezoid'), 'P': (380, 150, 'parallelogram'),
          'K': (620, 150, 'kite'), 'R': (270, 250, 'rectangle'), 'H': (500, 250, 'rhombus'), 'S': (380, 340, 'square')}
def _f1_node(k, col='ink'):
    x, y, t = _nodes[k]; return [('txt', x, y, t, col, 26)]
def _f1_edge(a, b, col='teal'):
    (x1, y1, _), (x2, y2, _) = _nodes[a], _nodes[b]
    return [('seg', x1, y1 + 16, x2, y2 - 20, col, 2.5)]
f1tree = GEO('f1tree', [
    ('line', _f1_node('Q')),
    ('l2', _f1_edge('Q', 'T') + _f1_edge('Q', 'P') + _f1_edge('Q', 'K') + _f1_node('T') + _f1_node('P') + _f1_node('K')),
    ('rect', _f1_edge('P', 'R') + _f1_node('R')),
    ('rhom', _f1_edge('P', 'H') + _f1_edge('K', 'H') + _f1_node('H')),
    ('sq', _f1_edge('R', 'S') + _f1_edge('H', 'S') + _f1_node('S')),
    ('down', [('path', [(380, 75), (380, 125), (290, 225), (370, 315)], 'teal', 7), ('txt', 150, 300, 'down a line:', 'teal', 22),
              ('txt', 150, 326, 'more properties', 'teal', 22)]),
    ('up', [('path', [(370, 315), (290, 225)], 'orange', 7), ('txt', 640, 300, 'rectangle: not', 'orange', 22),
            ('txt', 640, 326, 'necessarily a square', 'orange', 22)]),
], vb='20 20 780 345', w=960, col=0, title='The quadrilateral family tree')

# ---- also / not necessarily: two quick checks on real shapes
f1also = GEO('f1also', [
    ('line', f1_poly([(40, 260), (150, 260), (150, 150), (40, 150)]) + [('right', 40, 260, 0, 90, 14), ('right', 150, 260, 90, 180, 14),
             ('right', 150, 150, 180, 270, 14), ('right', 40, 150, 270, 360, 14), ('txt', 95, 300, 'a square is a rectangle ✓', 'teal', 22)]),
    ('rect', f1_poly([(330, 260), (530, 260), (530, 150), (330, 150)]) + [('right', 330, 260, 0, 90, 14), ('right', 530, 260, 90, 180, 14),
             ('txt', 430, 285, '3', 'ink', 22), ('txt', 548, 205, '2', 'ink', 22),
             ('txt', 430, 320, 'a rectangle is not', 'red', 22), ('txt', 430, 346, 'necessarily a square ✗', 'red', 22)]),
], vb='-80 120 680 250', w=900, col=0, title='Up and down the tree')
f1r1 = I('f1r1', 'square → rectangle rules + rhombus rules', size=30)
f1r2 = I('f1r2', 'rectangle → not necessarily a square', size=30)
f1r3 = I('f1r3', 'The name carries information: underline it', size=30)

def f1_pin(g):
    """layers that come after another board item: pin them to their base figure (fig / of)"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


for _f1g in (f1use, f1useB, f1use3, f1tree): f1_pin(_f1g)

video('geo-042', 'lesson', slides=[
    S('Quadrilaterals',
      L("So far we've finished lines, angles and triangles. Now let's look at quadrilaterals, shapes with four sides. "
        "We'll start with a general one.")),
    S('What it is',
      L("A quadrilateral is a closed shape with four sides. Here are four points. Let's join them. One side, two, three, "
        "and four, back to where we started. The shape is closed, and it has four sides, so it's a quadrilateral.",
        show(f1what['line'], 'Here are four points'), show(f1what['s1'], 'One side'), show(f1what['s2'], 'two, three'),
        show(f1what['s3'], 'three, and four'), show(f1what['s4'], 'back to where we started')),
      L("Its sides don't have to be equal, and its angles don't have to be right angles. If the question doesn't say so, "
        "don't add it yourself.", pt('f1what_line', "Its sides don't have to be equal"))),
    S('More examples',
      L("Here are two more quadrilaterals. They look different, but each one is closed and has four sides. And here are "
        "two shapes that are not quadrilaterals. This one has four sides, but its ends don't meet, so it isn't closed. "
        "And this one is closed, but it has five sides.", show(f1more['line'], 'Here are two more quadrilaterals'), show(f1more['e2'], 'They look different'),
        show(f1more['n1'], "but its ends don't meet"), show(f1more['n2'], 'it has five sides'))),
    S('It can bend inward',
      L("A quadrilateral can also look like this. Its angles don't all have to be smaller than a hundred eighty degrees. "
        "One angle can even be bigger than a hundred eighty, like the angle at C here.",
        show(f1bend['line'], 'A quadrilateral can also look like this'), show(f1bend['big'], 'One angle can even be bigger')),
      L("It still has four sides, and it's closed, so it's still a quadrilateral.", show(f1bend['four'], 'It still has four sides'))),
    S('The angle sum',
      L("Now the sum of the angles in a quadrilateral. Here's a quadrilateral, A B C D. Let's draw a diagonal, a line from "
        "B to D. It splits the quadrilateral into two triangles.",
        show(f1sum['line'], "Here's a quadrilateral"), show(f1sum['diag'], "Let's draw a diagonal")),
      L("We know that the angles in a triangle add up to a hundred eighty degrees. So the three teal angles of triangle A B "
        "D add up to a hundred eighty. And the three orange angles of triangle B C D add up to a hundred eighty too.",
        show(f1sum['t1'], 'So the three teal angles'), show(f1sum['t2'], 'And the three orange angles')),
      L("Now look at the corners of the quadrilateral. The angles at A and at C are whole. The angles at B and at D are "
        "each made of a teal piece and an orange piece. So all the pieces together are exactly the four angles of the "
        "quadrilateral. A hundred eighty plus a hundred eighty is three hundred sixty.",
        pt('f1sum_line', 'Now look at the corners'), show(f1sum['all'], 'A hundred eighty plus a hundred eighty')),
      L("So the angles in a quadrilateral add up to three hundred sixty degrees. That's almost the only rule we have for a "
        "general quadrilateral, at least the only one that matters for the exam.", pt('f1sum_all', 'So the angles in a quadrilateral'))),
    S('Using the angle sum',
      L("Let's use it. Here the angles are eighty, ninety-five and a hundred ten degrees, and we want x. All four angles "
        "add up to three hundred sixty, so first we add the three we know. Eighty plus ninety-five is a hundred "
        "seventy-five. And plus a hundred ten is two hundred eighty-five.",
        show(f1use['line'], 'Here the angles are eighty'), show(f1u1a, 'Eighty plus ninety-five'),
        show(f1u1b, 'And plus a hundred ten')),
      L("What's left of the three hundred sixty is x. So x is three hundred sixty minus two hundred eighty-five. Let's "
        "take away two hundred eighty first. Three hundred sixty minus two hundred eighty is eighty. Then we take away "
        "five more, so x is seventy-five degrees.",
        show(f1u1c, "What's left of the three hundred sixty"), show(f1u1d, 'Three hundred sixty minus two hundred eighty is'),
        show(f1u1e, 'Then we take away'), show(f1use['x1'], 'so x is seventy-five'))),
    S('Using the angle sum',
      L("Here's another one, with two right angles and a hundred twenty degrees. Ninety plus ninety is a hundred eighty. "
        "And plus a hundred twenty is three hundred. So y is three hundred sixty minus three hundred, which is sixty degrees.",
        show(f1useB['line'], 'two right angles'), show(f1u2a, 'Ninety plus ninety'), show(f1u2b, 'And plus a hundred twenty'),
        show(f1u2c, 'So y is three hundred sixty'), show(f1u2d, 'which is sixty degrees'), show(f1useB['x2'], 'sixty degrees.'))),
    S('An angle bigger than 180',
      L("And one with an angle bigger than a hundred eighty. The other angles are thirty, forty and fifty degrees. Thirty "
        "plus forty is seventy. And plus fifty, that's a hundred twenty. So the angle at the inward corner is three hundred "
        "sixty minus a hundred twenty, which is two hundred forty degrees. The rule still works for every quadrilateral.",
        show(f1use3['line'], 'And one with an angle bigger'), show(f1u3a, 'Thirty plus forty'), show(f1u3b, 'And plus fifty'),
        show(f1u3c, 'sixty minus a hundred twenty'), show(f1u3d, 'which is two hundred forty'),
        show(f1use3['x3'], 'two hundred forty degrees'))),
    # ------------------------------------------------------------------ part 2
    S('The family',
      L("So which kinds of quadrilaterals are there? What do you remember from school? There's the ordinary "
        "quadrilateral, and then a whole family of special ones. Let's see how one turns into another."),
      L("Here's a square, a perfect quadrilateral, with all its sides equal. Take a square and stretch it a little, and you "
        "get a rectangle. The angles are still right angles, but now only the opposite sides are equal.",
        show(f1fam1['line'], "Here's a square"), show(f1fam1['re'], 'stretch it a little')),
      L("Now take a rectangle and step on it, squash it a bit to the side, and you get a parallelogram. The opposite sides "
        "stay parallel and equal, but the angles aren't right angles any more.", show(f1fam1['pa'], 'step on it'))),
    S('The rhombus',
      L("Now take a parallelogram and shorten its two longer sides, until all four sides are equal. The opposite sides "
        "stay parallel. It becomes a rhombus. I know it doesn't "
        "really look like one, because it's lying down. We're used to seeing a rhombus like on playing cards, standing on a "
        "corner. So let's turn it a little. Now it really looks like a rhombus.",
        show(f1fam2['line'], 'take a parallelogram'), show(f1fam2['rh'], 'It becomes a rhombus'), show(f1fam2['turn'], "let's turn it")),
      L("You can also squash a square a bit, and get a rhombus. All four sides stay equal.",
        show(f1sqrh['line'], 'squash a square'), show(f1sqrh['rh'], 'and get a rhombus'))),
    S('The kite and the trapezoid',
      L("Take a rhombus and pull its bottom corner down, and you get a kite, also called a deltoid. A kite has two equal "
        "sides next to each other. The other two sides are equal too. In this picture, the top pair is shorter. All four "
        "sides can also be equal, as in a rhombus.", show(f1fam3['line'], 'Take a rhombus'), show(f1fam3['ki'], 'and you get a kite')),
      L("And take a rectangle, and move its two top corners toward each other, and you get a trapezoid. Its top and "
        "bottom stay parallel, but the other two sides are no longer parallel.",
        show(f1fam3['re'], 'take a rectangle'), show(f1fam3['tz'], 'and you get a trapezoid')),
      L("So those are all our quadrilaterals, and how one turns into another. The name of a shape carries a lot of "
        "information, so when a question names the shape, underline it.", show(f1r3, 'when a question names the shape'))),
    S('Who is also who?',
      L("Now the same family as a tree. Read every line going down as a special kind of. At the top is the general "
        "quadrilateral. A trapezoid, a parallelogram and a kite are special kinds of quadrilateral.",
        show(f1tree['line'], 'At the top'), show(f1tree['l2'], 'A trapezoid, a parallelogram and a kite')),
      L("A rectangle is a special parallelogram, a parallelogram with right angles. A rhombus is a special parallelogram, "
        "and also a special kite, with all four sides equal. And at the bottom is the square. It's a rectangle and a "
        "rhombus at the same time.", show(f1tree['rect'], 'A rectangle is a special parallelogram'),
        show(f1tree['rhom'], 'A rhombus is a special'), show(f1tree['sq'], 'And at the bottom')),
      L("Going down a line of the tree, a shape only gains properties. So a square has all the rectangle rules. It also "
        "has all the rhombus rules. But knowing that a shape is a rectangle doesn't guarantee that it's a square.",
        show(f1tree['down'], 'Going down a line'), show(f1r1, 'all the rectangle rules'),
        show(f1tree['up'], "doesn't guarantee"))),
    S('Up and down the tree',
      L("For example, every square is a rectangle, because it has four right angles. But a rectangle is not necessarily a "
        "square. This rectangle is three by two, so its sides are not all equal.",
        show(f1also['line'], 'every square is a rectangle'), show(f1also['rect'], 'This rectangle is three by two')),
      L("That's why we say not necessarily. A rhombus is always a parallelogram, but a kite is not necessarily a rhombus. "
        "From here, there's a lesson on each shape. We start with the square, the easiest to understand, because we all "
        "know what a square is. [pause] Okay. I'll see you in the next video.", show(f1r2, "That's why we say not necessarily"))),
])

CAMERA_SPLIT = ('geo-042', 'Quadrilaterals', [
    (1, None),
    (8, "Let's continue with quadrilaterals, and meet the whole family."),
])

# =================================================================================================================
# Topic 32 fragment f2: the square, the rectangle, the parallelogram (lessons geo-043, geo-045, geo-047) and their
# sample questions (g044, g046). Hebrew: geo 1794-2050. Written 2026-10-14 to the guide (R1-R36, clarity, Codex review
# standard, V1-V3). Every figure is pinned (fig / of) so typed board lines can come between its layers.
# =================================================================================================================


def f2_poly(pts, c='ink', w=3):
    return [('seg', pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], c, w) for i in range(len(pts))]


def f2_labs(*rows):
    """rows of (x, y, text): vertex letters"""
    return [('txt', x, y, t, 'ink', 26, True) for x, y, t in rows]


def f2_pin(g):
    """pin a GEO figure: its later layers are drawn on their own base, even with other board items in between"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


def f2_grid(x0, y0, n, m, s, c='teal'):
    """an n (across) by m (down) grid of little squares of size s, top-left at (x0, y0)"""
    out = []
    for i in range(1, n): out.append(('seg', x0 + i * s, y0, x0 + i * s, y0 + m * s, c, 1.4))
    for j in range(1, m): out.append(('seg', x0, y0 + j * s, x0 + n * s, y0 + j * s, c, 1.4))
    return out


# ------------------------------------------------------------------------------------------------ geo-043 (lesson: The Square)
# Hebrew (geo 1795-1858): all sides equal, all angles 90; the diagonals are equal, bisect each other, perpendicular, and
# bisect the angles (45 each); four silver triangles (also two, and endlessly more); area = side squared ("that's why we
# call it squared"), counted on a grid; the area from the diagonal, d^2 / 2, with the why (half the diagonal, one small
# triangle, times four); "the square is YES" to every property. Kept from the English lesson: a turned square is still a
# square; scaling (x k -> area x k^2, counted on a grid). Added examples: a side of 5 and 7 -> diagonal 5 root 2, 7 root 2;
# 9 -> 81; the diagonal 12 -> 72 and 10 -> 50. Dropped: the percent example (percent is a later topic in the plan).
# V3: one generic square built part by part (ticks, right angles); a turned copy; the diagonals traced, then the halves
# ticked, the right angle, the 45s; the silver triangles tinted inside the square (one small one, then a half); the grid
# counted; the scaling as two grids side by side.
f2_SQ = [(210, 60), (210, 300), (450, 300), (450, 60)]          # A B C D, side 240
f2_O = (330, 180)
f2_sqT = f2_poly(f2_SQ) + f2_labs((190, 44, 'A'), (190, 318, 'B'), (470, 318, 'C'), (470, 44, 'D'))
f2_sq1 = f2_pin(GEO('f2sq1', [
    ('line', f2_sqT),
    ('sides', [('tick', 210, 60, 210, 300), ('tick', 210, 300, 450, 300), ('tick', 450, 300, 450, 60), ('tick', 450, 60, 210, 60)]),
    ('ang', [('right', 210, 300, 0, 90, 18), ('right', 450, 300, 90, 180, 18), ('right', 450, 60, 180, 270, 18), ('right', 210, 60, 270, 360, 18)]),
    ('turn', [('seg', 660, 60, 780, 180, 'ink', 3), ('seg', 780, 180, 660, 300, 'ink', 3), ('seg', 660, 300, 540, 180, 'ink', 3),
              ('seg', 540, 180, 660, 60, 'ink', 3), ('tick', 660, 60, 780, 180), ('tick', 780, 180, 660, 300), ('tick', 660, 300, 540, 180),
              ('tick', 540, 180, 660, 60), ('right', 660, 300, 45, 135, 16), ('txt', 660, 335, 'still a square', 'small', 24)]),
], vb='150 20 680 340', w=900, col=0, title='A square'))
f2_sq2 = f2_pin(GEO('f2sq2', [
    ('line', f2_sqT),
    ('diag', [('seg', 210, 60, 450, 300, 'small', 4), ('seg', 450, 60, 210, 300, 'small', 4)]),
    ('half', [('tick', 210, 60, 330, 180, 1, 'orange'), ('tick', 330, 180, 450, 300, 1, 'orange'), ('tick', 450, 60, 330, 180, 1, 'orange'),
              ('tick', 330, 180, 210, 300, 1, 'orange')]),
    ('perp', [('right', 330, 180, 225, 315, 18, 'orange')]),
    ('a45', [('arc', 210, 300, 40, 0, 45, 'small', '45°', 64), ('arc', 210, 300, 46, 45, 90, 'small', '45°', 70)]),
], vb='150 20 360 320', w=560, col=0, title='The diagonals of a square'))
f2_k43a = I('f2k43a', 'Equal $\\cdot$ cut each other in half $\\cdot$ perpendicular $\\cdot$ cut the angles in half', size=26, col=1)
f2_sq3 = f2_pin(GEO('f2sq3', [
    ('line', f2_sqT + [('seg', 210, 60, 450, 300, 'ink', 2), ('seg', 450, 60, 210, 300, 'ink', 2)]),
    ('small', [('tint', [(210, 300), (450, 300), f2_O], 'small'), ('right', 330, 180, 225, 315, 16, 'small'),
               ('tick', 330, 180, 210, 300, 1), ('tick', 330, 180, 450, 300, 1)]),
    # 2026-10-18 (batch C #213): the small triangle fades at the switch; the half square's legs are the SIDES AB and BC
    ('halfsq', [('dim', 150, 20, 360, 320)] + f2_sqT + [('seg', 210, 60, 450, 300, 'ink', 2), ('seg', 450, 60, 210, 300, 'ink', 2),
                ('tint', [(210, 60), (210, 300), (450, 300)], 'orange'), ('right', 210, 300, 0, 90, 18, 'orange'),
                ('seg', 210, 60, 210, 300, 'orange', 5), ('seg', 210, 300, 450, 300, 'orange', 5),
                ('tick', 210, 60, 210, 300, 1, 'orange'), ('tick', 210, 300, 450, 300, 1, 'orange')]),
    ('more', [('seg', 210, 300, 330, 180, 'small', 5), ('right', 330, 180, 135, 225, 14, 'small'), ('right', 330, 180, 225, 315, 14, 'small'),
              ('txt', 330, 342, 'two smaller silver triangles', 'small', 20)]),
], vb='150 20 360 336', w=560, col=0, title='Silver triangles in a square'))
f2_k43b = I('f2k43b', 'Side $s$ $\\to$ diagonal $s\\sqrt2$', size=30, col=1)
f2_k43c = IH('f2k43c', '$5\\to5\\sqrt{2} \\qquad 7\\to7\\sqrt{2}$', size=30, col=1)
f2_sq4 = f2_pin(GEO('f2sq4', [
    ('line', f2_poly([(150, 40), (150, 310), (420, 310), (420, 40)])),
    ('grid', f2_grid(150, 40, 6, 6, 45)),
    ('count', [('txt', 172 + 45 * i, 336, str(i + 1), 'orange', 22) for i in range(6)]),
    ('all', [('tint', [(150, 40), (150, 310), (420, 310), (420, 40)], 'small'), ('txt', 285, 18, '36 little squares', 'small', 24)]),
], vb='110 0 360 355', w=500, col=0, title='A 6 by 6 square on a grid'))
f2_k43d = I('f2k43d', '$S=a^2$', size=34, col=1)
f2_k43e = IH('f2k43e', '$6^2=36$ cm²', size=32, col=1)
f2_k43f = IH('f2k43f', '$9^2=81$ cm²', size=32, col=1)
f2_sq5 = f2_pin(GEO('f2sq5', [
    ('line', f2_sqT + [('seg', 210, 60, 450, 300, 'ink', 2), ('seg', 450, 60, 210, 300, 'ink', 2)]),
    # 2026-10-18 (batch C #213): the WHOLE diagonal AC is traced (its length 12 is written in the column, AC = 12); each
    # half gets its own 6, clear of the ticks
    ('d12', [('seg', 210, 60, 450, 300, 'small', 5), ('dot', 210, 60), ('dot', 450, 300)]),
    ('half', [('txt', 246, 216, '6', 'orange', 26), ('txt', 414, 216, '6', 'orange', 26), ('tick', 330, 180, 210, 300, 1, 'orange'),
              ('tick', 330, 180, 450, 300, 1, 'orange')]),
    ('tri', [('tint', [(210, 300), (450, 300), f2_O], 'small'), ('right', 330, 180, 225, 315, 16, 'small')]),
    ('tri18', [('txt', 330, 268, '18', 'small', 26)]),
    ('four', [('txt', 330, 92, '18', 'small', 26), ('txt', 244, 166, '18', 'small', 26), ('txt', 416, 166, '18', 'small', 26)]),
], vb='150 20 360 320', w=560, col=0, title='The area from the diagonal'))
f2_k43g = I('f2k43g', '$S=\\frac{d\\cdot d}{2}=\\frac{d^2}{2}$', size=34, col=1)
f2_k43ac = I('f2k43ac', '$AC=d=12$', size=30, col=1)
f2_k43t1 = IH('f2k43t1', '$6\\cdot6=36$', size=30, col=1)
f2_k43t2 = IH('f2k43t2', '$\\frac{36}{2}=18$', size=30, col=1)
f2_k43h = IH('f2k43h', '$4\\cdot18=72$', size=30, col=1)
f2_k43h2 = IH('f2k43h2', '$\\frac{12^2}{2}=\\frac{144}{2}$', size=30, col=1)
f2_k43h3 = IH('f2k43h3', '$=72$', size=30, col=1)
f2_k43i = IH('f2k43i', '$10^2=100$', size=30, col=1)
f2_k43i2 = IH('f2k43i2', '$\\frac{100}{2}=50$', size=30, col=1)
f2_sq6 = f2_pin(GEO('f2sq6', [
    ('line', f2_poly([(80, 190), (80, 310), (200, 310), (200, 190)]) + [('txt', 140, 336, '3', 'ink', 24)] + f2_grid(80, 190, 3, 3, 40)),
    ('big', f2_poly([(300, 70), (300, 310), (540, 310), (540, 70)]) + [('txt', 420, 336, '6', 'ink', 24)] + f2_grid(300, 70, 6, 6, 40)),
    ('areas', [('txt', 140, 168, '9', 'small', 30), ('txt', 420, 48, '36', 'orange', 30)]),
    ('rows', [('tint', [(300, 270), (300, 310), (540, 310), (540, 270)], 'orange'), ('txt', 600, 290, 'twice as long', 'orange', 20),
              ('tint', [(300, 70), (300, 310), (340, 310), (340, 70)], 'small'), ('txt', 320, 30, 'twice as many rows', 'small', 20)]),
], vb='40 0 620 355', w=580, col=0, title='Double the side: four times the area'))
f2_k43j = I('f2k43j', 'Every length $\\times k$ $\\ \\Rightarrow\\ $ area $\\times k^2$', size=30, col=1)
f2_k43k = I('f2k43k', 'Every length $\\times3$ $\\ \\Rightarrow\\ $ area $\\times9$', size=30, col=1)
f2_sq7 = f2_pin(GEO('f2sq7', [
    ('line', f2_poly([(40, 100), (40, 190), (130, 190), (130, 100)]) + f2_grid(40, 100, 3, 3, 30) + [('txt', 85, 214, '3', 'ink', 22),
              ('txt', 22, 145, '3', 'ink', 22), ('txt', 85, 80, '9', 'small', 26)]),
    ('long', f2_poly([(200, 100), (200, 190), (380, 190), (380, 100)]) + f2_grid(200, 100, 6, 3, 30) + [('txt', 290, 214, '6', 'ink', 22),
              ('txt', 396, 145, '3', 'ink', 22), ('txt', 290, 80, '18', 'orange', 26)]),
], vb='0 55 420 175', w=460, col=1, title='Only the length doubles: the area doubles'))
f2_k43l = I('f2k43l', 'Square: all of these hold ✓', size=40, col=0)
f2_k43m = I('f2k43m', 'Sides equal ✓ $\\cdot$ Diagonals equal ✓ $\\cdot$ Perpendicular ✓ $\\cdot$ Cut the angles in half ✓', size=32, col=0)
video('geo-043', 'lesson', slides=[
    S('The Square',
      L("The square. It's a shape almost all of us know, so let's go over its properties.")),
    S('Sides and angles',
      L("All four sides of a square are equal, and all four angles are ninety degrees.", show(f2_sq1['line'], 'All four sides'),
        show(f2_sq1['sides'], 'sides of a square are equal'), show(f2_sq1['ang'], 'all four angles')),
      L("If the square is turned on the page, it's still a square. What decides is what the question says, not how the "
        "figure is drawn.", show(f2_sq1['turn'], 'If the square is turned'))),
    S('The diagonals',
      L("Now the diagonals of the square. First, they're equal to each other.", show(f2_sq2['line'], 'Now the diagonals'),
        show(f2_sq2['diag'], "they're equal to each other")),
      L("They also cut each other in half. So all four halves are equal: this one, this one, this one and this one.",
        show(f2_sq2['half'], 'They also cut each other in half')),
      L("They're perpendicular to each other: they meet at ninety degrees.", show(f2_sq2['perp'], "They're perpendicular")),
      L("And they cut the square's angles in half. Each ninety splits into forty-five and forty-five, in every corner.",
        show(f2_sq2['a45'], "And they cut the square's angles in half"), show(f2_k43a, 'in every corner'))),
    S('Silver triangles',
      L("Look at one of the four small triangles. Its angle in the middle is ninety degrees, because the diagonals are "
        "perpendicular. And its two legs are equal, because they're halves of equal diagonals. That's a silver triangle, "
        "forty-five, forty-five, ninety. So the square is made of four silver triangles.",
        show(f2_sq3['line'], 'Look at one of the four'), show(f2_sq3['small'], 'Its angle in the middle')),
      L("It's also made of two silver triangles, depending on how we look. Take half the square, cut along one diagonal. It "
        "has a ninety-degree angle and two equal legs, the sides of the square. And we can keep cutting. Draw a line from "
        "the right angle at B to the middle of the diagonal. That cuts the half square into two smaller silver triangles, "
        "and we can cut each of them again in the same way.", show(f2_sq3['halfsq'], 'Take half the square'),
        show(f2_sq3['more'], 'Draw a line from')),
      L("In a silver triangle, the hypotenuse is a leg times root two. In the half square, the hypotenuse is the diagonal, so "
        "the diagonal is the side times root two. A side of five gives a diagonal of five root two, and a side of seven "
        "gives seven root two.", show(f2_k43b, 'the diagonal is the side times'), show(f2_k43c, 'A side of five'))),
    S('Area: side squared',
      L("The area of a square is its side, squared. That's actually where the word squared comes from. If the side is a, the "
        "area is a squared.", show(f2_k43d, 'If the side is a')),
      L("Say each little square here is one square centimeter. Count the side: one, two, three, four, five, six. The side is "
        "six, so the area is six squared, thirty-six. And really, there are thirty-six little squares.",
        show(f2_sq4['line'], 'Say each little square'), show(f2_sq4['grid'], 'here is one square'),
        show(f2_sq4['count'], 'Count the side'), show(f2_sq4['all'], 'And really'), show(f2_k43e, 'the area is six squared')),
      L("Another example: a side of nine gives nine squared, which is eighty-one square centimeters.",
        show(f2_k43f, 'a side of nine'))),
    S('Area from the diagonal',
      L("There's another way to find the area of a square. It's less known and less used: with the diagonals. Multiply the "
        "diagonals and divide by two. The two diagonals are equal, so it's the diagonal squared, over two.",
        show(f2_k43g, 'Multiply the diagonals')),
      L("Why does it work? Say the whole diagonal, from A to C, is twelve. Then half of it is six. The other diagonal is "
        "also twelve, so its halves are six too.", show(f2_sq5['line'], 'Why does it work'),
        show(f2_sq5['d12'], 'Say the whole diagonal'), show(f2_k43ac, 'is twelve'), show(f2_sq5['half'], 'Then half of it')),
      L("Look at one small triangle. Its legs are two halves, six and six, and they're perpendicular. So its area is six "
        "times six over two. Six times six is thirty-six, and half of thirty-six is eighteen.",
        show(f2_sq5['tri'], 'Look at one small triangle'), show(f2_k43t1, 'Six times six is'), show(f2_k43t2, 'and half of thirty-six'),
        show(f2_sq5['tri18'], 'is eighteen')),
      L("The square is four of these triangles. Four times eighteen is seventy-two.", show(f2_sq5['four'], 'The square is four'),
        show(f2_k43h, 'Four times eighteen')),
      L("Now let's check the formula, the diagonal squared over two. Twelve squared over two is a hundred forty-four over "
        "two, and that's also seventy-two. Every square has these four equal triangles, and a longer or shorter diagonal "
        "doesn't change that split. So the formula works for every square.",
        show(f2_k43h2, 'Twelve squared over two'), show(f2_k43h3, "that's also seventy-two"), pt('f2k43g', 'Every square has these')),
      L("Let's check one more: a diagonal of ten. Ten squared is a hundred, and a hundred over two is fifty.",
        show(f2_k43i, 'Ten squared is'), show(f2_k43i2, 'a hundred over two'))),
    S('Scale it up',
      L("One more fact about area, and it's true for every shape. Double the side of a square, from three to six.",
        show(f2_sq6['line'], 'Double the side'), show(f2_sq6['big'], 'from three to six')),
      L("The area doesn't double. It goes from nine to thirty-six, four times as much. Count the little squares: every row is "
        "twice as long, and there are twice as many rows. Two times two is four.", show(f2_sq6['areas'], "The area doesn't double"),
        show(f2_sq6['rows'], 'Count the little squares')),
      L("So when every length is multiplied by some number k, the area is multiplied by k squared. For example, if every "
        "length is three times as long, the area is nine times as big.", show(f2_k43j, 'So when every length'),
        show(f2_k43k, 'For example')),
      L("Careful, this works only when all the lengths grow. For a rectangle, if we double its length but keep its width "
        "the same, the area only doubles. Three by three is nine, and six by three is eighteen. Both sides must double for "
        "the area to become four times as big.", pt('f2k43j', 'Careful, this works'), show(f2_sq7['line'], 'Three by three'),
        show(f2_sq7['long'], 'six by three'), pt('f2sq6_line', 'Both sides must double'))),
    S('Square: all yes',
      L("That's the square, the simplest and the most perfect quadrilateral. All the properties we just checked hold for a "
        "square.", show(f2_k43l, 'All the properties we just checked')),
      L("Its sides are equal. Its diagonals are equal, they're perpendicular, and they cut the angles in half. [pause] Take a "
        "moment to memorize this. I'll see you in the next video.", show(f2_k43m, 'Its sides are equal'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g044 (Hebrew: the square's example)
# Hebrew (geo 1847-1855): "I could draw it and start Pythagoras to find the side, and then square it, but there's no
# reason": d^2 / 2 (her 10 -> 50; the course's 14 -> 98). Kept from the English script: the long way once, as a second
# method (s^2 + s^2 = 196 -> s^2 = 98, stop: s^2 IS the area), and the traps 196 and 49.
# V3: the question figure on the left; our copy on the right: the given diagonal traced with 14, the other diagonal drawn
# in (equal); method 2: triangle ABC tinted, its two legs s, the hypotenuse 14.
FIG_LEFT.update({'solve-geo32-g044', 'solve-geo32-g046'})
f2_g44T = f2_poly([(210.5, 70.5), (210.5, 289.5), (429.5, 289.5), (429.5, 70.5)]) + f2_labs((192, 54, 'A'), (192, 308, 'B'), (448, 308, 'C'), (448, 54, 'D'))
f2_g44 = f2_pin(GEO('f2g44', [
    ('line', f2_g44T + [('seg', 210.5, 70.5, 429.5, 289.5, 'ink', 3), ('txt', 345, 168, '14', 'ink', 24)]),
    ('d1', [('seg', 210.5, 70.5, 429.5, 289.5, 'small', 5)]),
    ('d2', [('seg', 429.5, 70.5, 210.5, 289.5, 'small', 4, True), ('txt', 404, 112, '14', 'small', 24)]),
], vb='170 30 300 300', w=240, title='The square ABCD and its diagonals'))
f2_g44b = f2_pin(GEO('f2g44b', [
    ('line', f2_g44T + [('seg', 210.5, 70.5, 429.5, 289.5, 'ink', 3)]),
    ('tri', [('tint', [(210.5, 70.5), (210.5, 289.5), (429.5, 289.5)], 'small'), ('right', 210.5, 289.5, 0, 90, 18, 'small'),
             ('txt', 190, 180, 's', 'small', 28, True), ('txt', 320, 312, 's', 'small', 28, True), ('txt', 345, 168, '14', 'orange', 26)]),
], vb='170 30 300 300', w=240, title='Half of the square: triangle ABC'))
_R(f2_g44, 200); _R(f2_g44b, 200)
# 2026-10-18 (batch C #214): the working is written in the column under the copy, one step per clause (readable size)
f2_g44r = [IH('f2g44r%d' % i, t, size=30) for i, t in enumerate(['$S=d^2/2$', '$S=14\\cdot14/2$', '$14\\cdot14=196$',
                                                                 '$196/2=98$'])]
f2_g44q = [IH('f2g44q%d' % i, t, size=30) for i, t in enumerate(['$s^2+s^2=14^2$', '$2s^2=196$', '$2s^2/2=196/2$',
                                                                 '$s^2=98$'])]
for _k, _it in enumerate(f2_g44r + f2_g44q): _R(_it, 452 + (_k % 4) * 58)
video('solve-geo32-g044', 'solution', qid='geo32-g044', slides=[
    SM('Method 1 · The math way: the diagonals', 'The diagonals',
      L("The diagonal of a square is fourteen centimeters long. What is the area of the square, in square centimeters?",
        pt('stem', 'The diagonal of a square', 'hl', 6.0), voice='calm', pause=0.5),
      L("We know only the diagonal, and we need the area. [short pause] We'll solve it in two different ways. First the "
        "math way, with the diagonal formula. Then we'll use Pythagoras.", pt('fig: 14', 'We know only the diagonal')),
      L("[short pause] Let's start with the formula. The area of a square is the product of the diagonals, over two.",
        show(f2_g44['line'], "Let's start with the formula"), show(f2_g44['d1'], 'The area of a square'),
        show(f2_g44r[0], 'the product of the diagonals')),
      L("The two diagonals of a square are equal, so both are fourteen. So the area is fourteen times fourteen, over two.",
        show(f2_g44['d2'], 'so both are fourteen'), show(f2_g44r[1], 'So the area is')),
      L("Fourteen times fourteen is a hundred ninety-six. Careful, that's not the area yet, because we still divide by two. "
        "Choice number three, a hundred ninety-six, is the trap for anyone who forgets. A hundred ninety-six over two is "
        "ninety-eight. Choice number two is our answer.", show(f2_g44r[2], 'Fourteen times fourteen'),
        mk('cross', 'choice 3', 'Choice number three, a hundred'), show(f2_g44r[3], 'A hundred ninety-six over two'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · The math way: through the side', 'Through the side',
      L("[pause] Now let's use Pythagoras to find the area through the side. Call the side s. The diagonal cuts the square "
        "into two right triangles. In triangle A B C, the legs are s and s, and the hypotenuse is the whole diagonal, "
        "fourteen.", show(f2_g44b['line'], 'Now let\'s use Pythagoras'), show(f2_g44b['tri'], 'In triangle A B C')),
      L("Careful, the side is not half the diagonal. Seven squared is forty-nine, choice number one, and that's a trap.",
        mk('cross', 'choice 1', 'Seven squared is forty-nine')),
      L("By Pythagoras, s squared plus s squared is fourteen squared. That's a hundred ninety-six, so two s squared is a "
        "hundred ninety-six. We want s squared alone, so we divide both sides by two. That gives s squared is ninety-eight.",
        show(f2_g44q[0], 'By Pythagoras'), show(f2_g44q[1], 'so two s squared'), show(f2_g44q[2], 'we divide both sides by two'),
        show(f2_g44q[3], 'That gives s squared')),
      L("But s squared is already the area of the square, because the area is the side squared. So we can stop here. "
        "Ninety-eight, choice number two.", pt('f2g44q3', 'But s squared is already'), mk('tick', 'choice 2', 'Ninety-eight, choice number two')),
      L("This comes back a lot. When they ask for the area of a square, and you reach s squared, stop there. You don't need "
        "the side itself, so there's no root to take. Here s would be root ninety-eight, and we never needed it. [pause] "
        "Okay. I'll see you in the next question.", pt('f2g44q3', 'When they ask for the area'))),
])

# ------------------------------------------------------------------------------------------------ geo-045 (lesson: The Rectangle)
# Hebrew (geo 1867-1890): a square stretched sideways keeps some of its rules: opposite sides equal, all angles 90,
# opposite sides parallel; the diagonals are equal (symmetric) and bisect each other; NOT perpendicular, NOT angle
# bisectors (unlike the square); area length x width (or base x height), on a grid (her 10 x 5 = 50; the course's 8 x 3).
# Kept from the English lesson: adjacent sides not necessarily equal (if they are: a square). Added: 7 x 4 = 28.
# (Her "exaggerated drawing" tip comes right after her rectangle example: it's in g046.)
# V3: the square, then the same square stretched (the rectangle drawn over it); marks at the words; the diagonals traced,
# halves ticked; the not-90 angle and the unequal corner parts in red; the area grid counted.
f2_RC = [(110, 90), (110, 270), (530, 270), (530, 90)]          # A B C D
f2_rcT = f2_labs((92, 74, 'A'), (92, 288, 'B'), (548, 288, 'C'), (548, 74, 'D'))
f2_rc1 = f2_pin(GEO('f2rc1', [
    ('line', f2_poly([(110, 90), (110, 270), (290, 270), (290, 90)], 'ink', 3)),
    ('rect', [('dim', 60, 40, 520, 280)] + f2_poly(f2_RC, 'ink', 4) + f2_rcT
             + [('seg', 300, 180, 500, 180, 'small', 3, True), ('par', 300, 180, 500, 180, 1, 'small'), ('txt', 400, 160, 'stretched', 'small', 24)]),
    ('opp', [('tick', 110, 90, 530, 90, 1), ('tick', 110, 270, 530, 270, 1), ('tick', 110, 90, 110, 270, 2), ('tick', 530, 90, 530, 270, 2)]),
    ('ang', [('right', 110, 270, 0, 90, 18), ('right', 530, 270, 90, 180, 18), ('right', 530, 90, 180, 270, 18), ('right', 110, 90, 270, 360, 18),
             ('par', 230, 90, 410, 90), ('par', 230, 270, 410, 270), ('par', 110, 240, 110, 120, 2), ('par', 530, 240, 530, 120, 2)]),
], vb='60 40 520 280', w=580, col=0, title='A square stretched into a rectangle'))
f2_k45a = I('f2k45a', 'Sides next to each other: not necessarily equal', size=28, col=1)
f2_rc2 = f2_pin(GEO('f2rc2', [
    ('line', f2_poly(f2_RC) + f2_rcT),
    ('diag', [('seg', 110, 90, 530, 270, 'small', 4), ('seg', 530, 90, 110, 270, 'small', 4)]),
    # 2026-10-18 (batch C #215): WHY they are equal - fold the rectangle down the middle, one diagonal lands on the other
    ('fold', [('seg', 320, 50, 320, 128, 'orange', 3, True), ('seg', 320, 200, 320, 300, 'orange', 3, True), ('txt', 320, 316, 'fold here', 'orange', 22)]),
    ('half', [('tick', 110, 90, 320, 180, 1, 'orange'), ('tick', 320, 180, 530, 270, 1, 'orange'), ('tick', 530, 90, 320, 180, 1, 'orange'),
              ('tick', 320, 180, 110, 270, 1, 'orange')]),
    ('notp', [('arc', 320, 180, 34, gdir(320, 180, 530, 90), gdir(320, 180, 110, 90), 'red', 'not 90°', 60)]),
    ('notb', [('arc', 110, 90, 40, 270, gdir(110, 90, 530, 270), 'red'), ('arc', 110, 90, 52, gdir(110, 90, 530, 270), 360, 'red'),
              ('txt', 70, 130, '≠', 'red', 26)]),
], vb='60 30 520 300', w=580, col=0, title='The diagonals of a rectangle'))
f2_k45b = I('f2k45b', 'Equal $\\cdot$ cut each other in half', size=28, col=1)
f2_k45c = I('f2k45c', 'Not necessarily $\\perp$ $\\cdot$ not necessarily cut the angles in half', size=26, col=1)
f2_rc3 = f2_pin(GEO('f2rc3', [
    ('line', f2_poly([(80, 120), (80, 270), (480, 270), (480, 120)])),
    ('grid', f2_grid(80, 120, 8, 3, 50)),
    ('count', [('txt', 105 + 50 * i, 296, str(i + 1), 'orange', 22) for i in range(8)] + [('txt', 56, 145 + 50 * j, str(j + 1), 'small', 22) for j in range(3)]),
    ('all', [('tint', [(80, 120), (80, 270), (480, 270), (480, 120)], 'small'), ('txt', 280, 96, '24 little squares', 'small', 24)]),
], vb='30 70 480 250', w=580, col=0, title='An 8 by 3 rectangle on a grid'))
f2_k45d = I('f2k45d', '$S=$ length $\\times$ width', size=34, col=1)
f2_k45e = IH('f2k45e', '$8\\cdot3=24$ cm²', size=32, col=1)
f2_k45f = IH('f2k45f', '$7\\cdot4=28$ cm²', size=32, col=1)
video('geo-045', 'lesson', slides=[
    S('The Rectangle',
      L("The rectangle. A rectangle is really a square that someone stretched a little sideways.")),
    S('Stretch a square',
      L("Take a square and stretch it sideways. We get a rectangle, so it keeps some of the square's rules.",
        show(f2_rc1['line'], 'Take a square'), show(f2_rc1['rect'], 'We get a rectangle')),
      L("Opposite sides are equal: the top equals the bottom, and the left side equals the right side.",
        show(f2_rc1['opp'], 'Opposite sides are equal')),
      L("All the angles are still ninety degrees, because we didn't touch the angles. And opposite sides are parallel.",
        show(f2_rc1['ang'], 'All the angles are still')),
      L("But two sides next to each other don't have to be equal. If they are equal, it's a square.",
        show(f2_k45a, "two sides next to each other"))),
    S('The diagonals',
      L("Now the diagonals. First, they're equal to each other. Why are they equal? Imagine folding the rectangle down the middle, from "
        "top to bottom. The left half lands on the right half, and one diagonal lands exactly on the other. So their "
        "lengths are equal.", show(f2_rc2['line'], 'Now the diagonals'), show(f2_rc2['diag'], "they're equal to each other"),
        show(f2_rc2['fold'], 'Imagine folding')),
      L("They also cut each other in half, so all four halves are equal.", show(f2_rc2['half'], 'They also cut each other'),
        show(f2_k45b, 'so all four halves')),
      L("Now pay attention. Are they perpendicular? Not necessarily. Here you can see that they don't meet at ninety degrees.",
        show(f2_rc2['notp'], 'Are they perpendicular')),
      L("Do they cut the rectangle's angles in half? Not necessarily either. At corner A, the two parts are not equal.",
        show(f2_rc2['notb'], 'At corner A')),
      L("In a square, the diagonals always do both, and a square is a special rectangle. But in a general rectangle, don't "
        "assume it.", show(f2_k45c, 'But in a general rectangle'))),
    S('Area: length times width',
      L("The area of a rectangle works like the square's. We count how many little squares are in each row, and how many "
        "rows there are. So the area is length times width, or base times height. The two lengths can be different, or "
        "equal, as in a square.", show(f2_rc3['line'], 'We count how many'), show(f2_rc3['grid'], 'little squares are in each row'),
        show(f2_k45d, 'So the area is length times width')),
      L("For example, a length of eight and a width of three. Each row has eight little squares, and there are three rows. "
        "Eight times three is twenty-four. We don't divide by two here, because it's the whole rectangle.",
        show(f2_rc3['count'], 'Each row has eight'), show(f2_k45e, 'Eight times three'), show(f2_rc3['all'], 'is twenty-four')),
      L("Another example: a length of seven and a width of four give seven times four, which is twenty-eight square "
        "centimeters. [pause] Okay. I'll see you in the next video.", show(f2_k45f, 'Another example'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g046 (Hebrew: the rectangle's example)
# Hebrew (geo 1891-1918): the diagonals bisect each other and are equal -> an isosceles triangle with 120 -> 30 and 30;
# the rectangle's angles are right -> triangle DBC is 30-60-90, the gold triangle; a = the short leg (her 2, the
# course's 5), the long leg a root 3; the area. Then her rectangle wrap-up: not sure about a diagonal rule? draw an
# exaggerated rectangle, very low and wide; triangles live inside quadrilateral questions.
# V3: the question figure on the left; the copy on the right: the two equal halves EB, EC ticked, the 120 at E, then the
# two 30s; slide 2: triangle DBC tinted (focus, the rest dimmed), 90 at C, the same 30 at B, 60 at D; CD = 5 written
# (the short leg, across from the 30), then BC = 5 root 3; the area; an exaggerated rectangle drawn for her tip.
f2_A, f2_B, f2_C, f2_D, f2_E = (168.272, 92.4), (168.272, 267.6), (471.728, 267.6), (471.728, 92.4), (320.0, 180.0)
f2_g46T = f2_poly([f2_A, f2_B, f2_C, f2_D]) + f2_labs((150, 76, 'A'), (150, 286, 'B'), (490, 286, 'C'), (490, 76, 'D'), (320, 156, 'E'))
f2_g46 = f2_pin(GEO('f2g46', [
    ('line', f2_g46T + [('seg', *f2_A, *f2_C, 'ink', 2.5), ('seg', *f2_B, *f2_D, 'ink', 2.5), ('txt', 492, 180, '5', 'ink', 24)]),
    ('iso', [('seg', *f2_E, *f2_B, 'small', 5), ('seg', *f2_E, *f2_C, 'small', 5), ('tick', *f2_E, *f2_B, 1, 'small'), ('tick', *f2_E, *f2_C, 1, 'small'),
             ('arc', *f2_E, 30, 210, 330, 'orange', '120°', 52)]),
    ('calc1', [('txt', 320, 318, '180° − 120° = 60°', 'ink', 24)]),
    ('calc2', [('txt', 320, 352, '60° ÷ 2 = 30°', 'ink', 24)]),
    ('b30', [('arc', *f2_B, 52, 0, 30, 'small', '30°', 80), ('arc', *f2_C, 52, 150, 180, 'small', '30°', 80)]),
], vb='120 50 400 320', w=460, title='Rectangle ABCD and its diagonals'))
f2_g46b = f2_pin(GEO('f2g46b', [
    ('line', f2_g46T + [('seg', *f2_B, *f2_D, 'ink', 2.5)]),
    ('tri', [('dim', 120, 50, 400, 270), ('tint', [f2_B, f2_C, f2_D], 'orange')] + f2_poly([f2_B, f2_C, f2_D], 'ink', 3.5)
            + f2_labs((150, 286, 'B'), (490, 286, 'C'), (490, 76, 'D'), (320, 156, 'E'))
            + [('right', *f2_C, 90, 180, 18, 'ink')]),
    # 2026-10-18 (batch C #216): E is on BD, so angle DBC is the same 30; then 60 at D; at the area the WHOLE rectangle
    ('b30', [('dot', *f2_E), ('seg', *f2_B, *f2_E, 'small', 5), ('arc', *f2_B, 52, 0, 30, 'small', '30°', 80)]),
    ('d60', [('arc', *f2_D, 40, 210, 270, 'orange', '60°', 62)]),
    ('short', [('seg', *f2_C, *f2_D, 'small', 6), ('txt', 514, 180, '5', 'small', 30)]),
    ('ratio', [('txt', 330, 30, 'a  :  a√3  :  2a', 'ink', 22)]),
    ('long', [('seg', *f2_B, *f2_C, 'orange', 6), ('txt', 320, 300, '5√3', 'orange', 28)]),
    ('whole', [('dim', 120, 5, 430, 350), ('tint', [f2_A, f2_B, f2_C, f2_D], 'small')] + f2_poly([f2_A, f2_B, f2_C, f2_D], 'ink', 4)
              + f2_labs((150, 76, 'A'), (150, 286, 'B'), (490, 286, 'C'), (490, 76, 'D'))
              + [('right', *f2_C, 90, 180, 18, 'ink'), ('seg', *f2_C, *f2_D, 'small', 6), ('txt', 514, 180, '5', 'small', 30),
                 ('seg', *f2_B, *f2_C, 'orange', 6), ('txt', 320, 300, '5√3', 'orange', 28)]),
    ('area1', [('txt', 320, 338, 'S = 5√3 · 5', 'ink', 27)]),
    ('area2', [('txt', 320, 372, '= 25√3', 'ink', 27)]),
], vb='120 5 430 385', w=460, title='Triangle DBC: a gold triangle'))
f2_g46c = f2_pin(GEO('f2g46c', [
    ('line', f2_poly([(60, 60), (60, 120), (580, 120), (580, 60)]) + [('seg', 60, 60, 580, 120, 'small', 3), ('seg', 580, 60, 60, 120, 'small', 3),
              ('txt', 320, 30, 'very low, very wide', 'small', 22)]),
], vb='30 10 580 130', w=500, title='An exaggerated rectangle'))
_R(f2_g46, 200); _R(f2_g46b, 200); _R(f2_g46c, 200)
video('solve-geo32-g046', 'solution', qid='geo32-g046', slides=[
    S('The isosceles triangle',
      L("The diagonals of rectangle A B C D intersect at E. Given: C D is five centimeters, and angle B E C is a hundred "
        "twenty degrees. What is the area of the rectangle, in square centimeters?", pt('stem', 'The diagonals of rectangle', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("For the area we need the length and the width. C D is five, so we still need B C. [short pause] The angle at E will "
        "lead us there.", pt('fig: 5', 'C D is five'), pt('fig: 120°', 'The angle at E')),
      L("[short pause] In a rectangle, the diagonals are equal, and they cut each other in half. So E B and E C are halves of "
        "equal diagonals, and they're equal. Triangle B E C is isosceles.", show(f2_g46['line'], 'In a rectangle'),
        show(f2_g46['iso'], 'So E B and E C')),
      L("Its top angle is a hundred twenty. In an isosceles triangle the base angles are equal, so they share the rest "
        "equally. A hundred eighty minus a hundred twenty is sixty, and half of that is thirty. So angle E B C is thirty, "
        "and angle E C B is thirty.", show(f2_g46['calc1'], 'A hundred eighty minus'), show(f2_g46['calc2'], 'and half of that'),
        show(f2_g46['b30'], 'So angle E B C is thirty'))),
    S('The gold triangle',
      L("Now look at triangle D B C. Its angle at C is ninety, because it's a corner of the rectangle. E lies on the "
        "diagonal B D, so B E and B D lie along the same line. So angle D B C is the same thirty as angle E B C.",
        show(f2_g46b['line'], 'Now look at triangle'), show(f2_g46b['tri'], 'Its angle at C'), show(f2_g46b['b30'], 'E lies on the')),
      L("The angles of a triangle add up to a hundred eighty, so the last angle, at D, is sixty.", show(f2_g46b['d60'], 'the last angle, at D')),
      L("Thirty, sixty, ninety: that's the gold triangle. Its sides are in the ratio a, a root three, two a. The short leg, a, "
        "is across from the thirty. Across from the thirty at B is C D, so a is five.", show(f2_g46b['ratio'], "that's the gold triangle"),
        show(f2_g46b['short'], 'Across from the thirty at B')),
      L("The long leg is the short leg times root three. So B C is five root three.", show(f2_g46b['long'], 'So B C is')),
      L("Now the area of the whole rectangle. B C and C D are its length and its width, and they're perpendicular. So the "
        "area is five root three times five, which is twenty-five root three. Choice number three is our answer.",
        show(f2_g46b['whole'], 'Now the area of the whole rectangle'), show(f2_g46b['area1'], 'So the area is'),
        show(f2_g46b['area2'], 'which is twenty-five root three'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('A tip for the diagonals',
      L("If you're not sure whether a diagonal rule is guaranteed, draw an exaggerated rectangle, very low and very wide. "
        "It's still a rectangle, and you'll see right away that its diagonals aren't perpendicular and don't cut the angles "
        "in half. So we can't assume either one in a rectangle.",
        show(f2_g46c['line'], 'draw an exaggerated rectangle')),
      L("And notice how a gold triangle was hiding inside the rectangle. Triangles live inside quadrilateral questions, and "
        "later in circles too. [pause] Okay. I'll see you in the next question.", pt('fig: 120°', 'a gold triangle was hiding'))),
])

# ------------------------------------------------------------------------------------------------ geo-047 (lesson: The Parallelogram)
# Hebrew (geo 1942-2009): a rectangle squashed sideways; opposite sides equal and parallel (AD = BC, AB = DC); opposite
# angles equal (A = C, B = D); adjacent angles add up to 180 (all four pairs); WHY: extend the sides into parallel lines
# - the same crossing at every corner - small angles (green) alpha, large (orange) beta, alpha + beta = 180; diagonals: NOT
# equal (a long one and a short one), they DO bisect each other, NOT angle bisectors "though sometimes it looks like it"
# (exaggerate: very wide, very low), NOT perpendicular; area = base x height (a x h); WHY: a rectangle on the same base,
# cut the triangle out and move it in - the same area. Kept from the English lesson: equal diagonals -> rectangle,
# perpendicular -> rhombus; where the height lands (extend BC from D); special angles (30 / 45 / 60 / 150) with the
# 8, 6, 30 -> h = 3, area 24 example and the 8 x 6 trap. Added: two angle examples (70 / 110, 125 / 55).
# V3: the rectangle (dashed) squashed into the parallelogram; marks at the words; the sides extended into long parallel
# lines with small teal / large orange angles at every corner; the long (orange) and short (teal) diagonals, halves
# ticked, red "not" marks, an exaggerated copy; the height dashed with its square; the cut-and-move: the same teal triangle
# on the left (cut) and on the right (moved in); the special-angle example with the gold triangle tinted.
f2_PA, f2_PB, f2_PC, f2_PD = (230, 110), (140, 300), (460, 300), (550, 110)
f2_pT = f2_labs((222, 88, 'A'), (120, 318, 'B'), (468, 322, 'C'), (570, 98, 'D'))
f2_aB = gdir(*f2_PB, *f2_PA)                                   # the acute angle at B (64.6 degrees as drawn)
f2_pg1 = f2_pin(GEO('f2pg1', [
    ('line', f2_poly([(140, 110), (140, 300), (460, 300), (460, 110)], 'small', 3) + [('txt', 300, 205, 'rectangle', 'small', 22)]),
    # 2026-10-18 (batch C #217): the old rectangle fades and its label goes, so only the parallelogram is named
    ('para', [('dim', 90, 60, 510, 280), ('wipe', 250, 190, 100, 30)] + f2_poly([f2_PA, f2_PB, f2_PC, f2_PD], 'ink', 4) + f2_pT),
    ('ad', [('tick', *f2_PA, *f2_PD, 1, 'orange'), ('tick', *f2_PB, *f2_PC, 1, 'orange'), ('par', *f2_PA, *f2_PD, 1, 'orange'), ('par', *f2_PB, *f2_PC, 1, 'orange')]),
    ('ab', [('tick', *f2_PB, *f2_PA, 2, 'small'), ('tick', *f2_PC, *f2_PD, 2, 'small'), ('par', *f2_PB, *f2_PA, 2, 'small'), ('par', *f2_PC, *f2_PD, 2, 'small')]),
], vb='90 60 510 280', w=580, col=0, title='A rectangle squashed into a parallelogram'))
f2_k47a = I('f2k47a', '$AD\\parallel BC,\\ AD=BC \\qquad AB\\parallel DC,\\ AB=DC$', size=28, col=1)
f2_pgT = f2_poly([f2_PA, f2_PB, f2_PC, f2_PD]) + f2_pT
f2_pg2 = f2_pin(GEO('f2pg2', [
    ('line', f2_pgT),
    ('opp', [('arc', *f2_PB, 36, 0, f2_aB, 'small'), ('arc', *f2_PD, 36, 180, 180 + f2_aB, 'small'),
             ('arc', *f2_PA, 32, 180 + f2_aB, 360, 'orange'), ('arc', *f2_PC, 32, f2_aB, 180, 'orange')]),
    ('ex1', [('txt', 196, 284, '70°', 'small', 22), ('txt', 506, 128, '70°', 'small', 22), ('txt', 262, 136, '110°', 'orange', 22),
             ('txt', 428, 276, '110°', 'orange', 22)]),
], vb='90 60 510 280', w=580, col=0, title='The angles of a parallelogram'))
f2_k47b = I('f2k47b', 'Opposite angles are equal', size=30, col=1)
f2_k47c = I('f2k47c', 'Next to each other: sum $180°$', size=30, col=1)
f2_k47d = IH('f2k47d', '$125°\\ \\to\\ 180°-125°=55°$', size=30, col=1)
f2_ext = lambda P, Q, k=0.8: (P[0] - (Q[0] - P[0]) * k, P[1] - (Q[1] - P[1]) * k, Q[0] + (Q[0] - P[0]) * k, Q[1] + (Q[1] - P[1]) * k)
f2_pg3 = f2_pin(GEO('f2pg3', [
    ('line', f2_pgT),
    ('l1', [('seg', 20, 110, 640, 110, 'ink', 2, True), ('seg', 20, 300, 640, 300, 'ink', 2, True)]),
    ('l2', [('seg', *f2_ext(f2_PB, f2_PA, 0.35), 'ink', 2, True), ('seg', *f2_ext(f2_PC, f2_PD, 0.35), 'ink', 2, True)]),
    ('u', [('path', [(420, 110), f2_PA, f2_PB, (330, 300)], 'orange', 7)]),
    ('ab', [('arc', *f2_PB, 34, 0, f2_aB, 'small', 'α', 56), ('arc', *f2_PD, 34, 180, 180 + f2_aB, 'small', 'α', 56),
            ('arc', *f2_PA, 30, 180 + f2_aB, 360, 'orange', 'β', 52), ('arc', *f2_PC, 30, f2_aB, 180, 'orange', 'β', 52)]),
    ('sum', [('txt', 330, 345, 'α + β = 180°', 'ink', 28)]),
], vb='0 40 660 330', w=860, col=0, title='Why: the sides are parallel lines'))
f2_pg4 = f2_pin(GEO('f2pg4', [
    ('line', f2_pgT),
    ('diag', [('seg', *f2_PB, *f2_PD, 'orange', 4), ('seg', *f2_PA, *f2_PC, 'small', 4), ('txt', 470, 170, 'long', 'orange', 22),
              ('txt', 300, 175, 'short', 'small', 22)]),
    ('half', [('tick', *f2_PB, 345, 205, 1, 'orange'), ('tick', 345, 205, *f2_PD, 1, 'orange'), ('tick', *f2_PA, 345, 205, 2, 'small'),
              ('tick', 345, 205, *f2_PC, 2, 'small')]),
    ('not', [('arc', *f2_PB, 46, 0, gdir(*f2_PB, *f2_PD), 'red'), ('arc', *f2_PB, 58, gdir(*f2_PB, *f2_PD), f2_aB, 'red'),
             ('txt', 140, 245, '≠', 'red', 26), ('txt', 345, 240, 'not 90°', 'red', 22)]),
    ('exag', f2_poly([(620, 300), (660, 260), (1060, 260), (1020, 300)], 'ink', 3) + [('seg', 620, 300, 1060, 260, 'orange', 3),
              ('arc', 620, 300, 46, 0, gdir(620, 300, 1060, 260), 'red'), ('arc', 620, 300, 58, gdir(620, 300, 1060, 260), 45, 'red'),
              ('txt', 840, 330, 'very wide, very low', 'small', 22)]),
], vb='90 60 1000 290', w=1060, col=0, title='The diagonals of a parallelogram'))
f2_k47f = I('f2k47f', 'A general parallelogram: the diagonals cut each other in half', size=28, col=0)
# 2026-10-18 (batch C #217): the two recognition facts, each with its own shape, and both start FROM a parallelogram
f2_pg8 = f2_pin(GEO('f2pg8', [
    ('line', f2_poly([(30, 70), (30, 200), (230, 200), (230, 70)]) + [('seg', 30, 70, 230, 200, 'small', 3), ('seg', 230, 70, 30, 200, 'small', 3),
              ('tick', 30, 70, 230, 200, 1, 'small'), ('tick', 230, 70, 30, 200, 1, 'small'), ('right', 30, 200, 0, 90, 14),
              ('txt', 130, 232, 'equal diagonals', 'small', 20), ('txt', 130, 256, '→ rectangle', 'small', 20)]),
    ('rh', f2_poly([(370, 200), (430, 135), (370, 70), (310, 135)]) + [('seg', 370, 70, 370, 200, 'orange', 3), ('seg', 310, 135, 430, 135, 'orange', 3),
            ('right', 370, 135, 0, 90, 12, 'orange'), ('tick', 370, 200, 430, 135), ('tick', 430, 135, 370, 70), ('tick', 370, 70, 310, 135), ('tick', 310, 135, 370, 200),
            ('txt', 370, 232, 'perpendicular', 'orange', 20), ('txt', 370, 256, '→ rhombus', 'orange', 20)]),
    ('ki', f2_poly([(560, 215), (610, 110), (560, 80), (510, 110)], 'red') + [('seg', 560, 80, 560, 215, 'red', 2.5), ('seg', 510, 110, 610, 110, 'red', 2.5),
            ('right', 560, 110, 0, 90, 12, 'red'), ('txt', 560, 240, 'kite: perpendicular,', 'red', 20), ('txt', 560, 264, 'not a parallelogram', 'red', 20)]),
], vb='0 50 660 230', w=900, col=0, title='Equal or perpendicular diagonals in a parallelogram'))
f2_k47e = I('f2k47e', 'If it is a parallelogram: equal diagonals $\\to$ rectangle $\\cdot$ perpendicular diagonals $\\to$ rhombus', size=28, col=0)
f2_H = (f2_PA[0], 300)
f2_pg5 = f2_pin(GEO('f2pg5', [
    ('line', f2_pgT + [('txt', 300, 326, 'a', 'ink', 26, True)]),
    ('h', [('seg', *f2_PA, *f2_H, 'small', 3.5, True), ('right', *f2_H, 0, 90, 16, 'small'), ('txt', 244, 210, 'h', 'small', 28, True)]),
    ('side', [('seg', *f2_PB, *f2_PA, 'red', 4), ('txt', 160, 190, 'not h', 'red', 22)]),
    ('ext', [('seg', 460, 300, 600, 300, 'ink', 2, True), ('seg', 550, 110, 550, 300, 'small', 3, True), ('right', 550, 300, 90, 180, 16, 'small'),
             ('dot', 550, 300)]),
], vb='90 60 540 290', w=580, col=0, title='The height of a parallelogram'))
f2_k47g = I('f2k47g', '$S=a\\cdot h$', size=34, col=1)
f2_pg6 = f2_pin(GEO('f2pg6', [
    ('line', f2_pgT + [('txt', 300, 326, 'a', 'ink', 26, True)]),
    ('rect', f2_poly([(140, 110), (140, 300), (460, 300), (460, 110)], 'small', 3) + [('txt', 300, 205, 'a × h', 'small', 26)]),
    ('left', [('tint', [(140, 110), f2_PB, f2_PA], 'small'), ('txt', 120, 160, 'cut', 'small', 22)]),
    # 2026-10-18 (batch C #217): the cut piece leaves the left side as it arrives on the right
    ('right', [('wipep', [(141.5, 111.5), (141.5, 298.5), (228, 111.5)]), ('seg', 140, 110, 140, 300, 'small', 1.5, True),
               ('seg', 140, 110, 230, 110, 'small', 1.5, True), ('seg', *f2_PB, *f2_PA, 'ink', 3), ('txt', 172, 150, 'empty', 'small', 17),
               ('tint', [(460, 110), f2_PC, f2_PD], 'small'), ('seg', 170, 70, 470, 70, 'small', 2, True), ('txt', 330, 56, 'move it', 'small', 22)]),
], vb='90 30 510 320', w=580, col=0, title='Cut and move: a rectangle with the same base and height'))
f2_k47h = I('f2k47h', 'Same base, same height $\\to$ same area', size=30, col=1)
f2_sB, f2_sC = (100, 300), (420, 300)
f2_sA = (100 + 240 * 0.8660254, 300 - 120)
f2_sD = (f2_sA[0] + 320, f2_sA[1])
f2_pg7 = f2_pin(GEO('f2pg7', [
    ('line', f2_poly([f2_sA, f2_sB, f2_sC, f2_sD]) + f2_labs((300, 160, 'A'), (84, 316, 'B'), (436, 316, 'C'), (650, 160, 'D'))
             + [('txt', 260, 326, '8', 'ink', 26), ('txt', 186, 222, '6', 'ink', 26), ('arc', *f2_sB, 52, 0, 30, 'small', '30°', 80)]),
    ('h', [('seg', *f2_sA, f2_sA[0], 300, 'small', 3.5, True), ('right', f2_sA[0], 300, 90, 180, 16, 'small')]),
    ('gold', [('tint', [f2_sB, f2_sA, (f2_sA[0], 300)], 'orange'), ('txt', 330, 245, 'h = 3', 'small', 26)]),
    ('wrong', [('txt', 520, 250, '8 × 6 ✗', 'red', 26)]),
], vb='60 140 620 210', w=580, col=0, title='A parallelogram with a 30 degree angle'))
f2_k47i = IH('f2k47i', '$S=8\\cdot3=24$', size=32, col=1)
# 2026-10-18 (batch C #217): 45, 60 and 150 each get their own right triangle (slanted side 8 in all three) and steps
def _f2_sp(B, deg, L=150, base=220):
    import math
    A = (B[0] + L * math.cos(math.radians(deg)), B[1] - L * math.sin(math.radians(deg)))
    C = (B[0] + base, B[1]); D = (A[0] + base, A[1]); H = (A[0], B[1])
    return A, B, C, D, H
_s45 = _f2_sp((50, 170), 45); _s60 = _f2_sp((50, 390), 60); _s150 = _f2_sp((180, 580), 150)
def _f2_spl(S, deg, lab):
    A, B, C, D, H = S
    return f2_poly([A, B, C, D]) + [('arc', *B, 30, 0, deg, 'small', lab, 54 if deg < 90 else 50),
                                     ('txt', (A[0] + B[0]) / 2 - (20 if deg < 90 else 0), (A[1] + B[1]) / 2 - (8 if deg < 90 else 22), '8', 'ink', 26)]
def _f2_sph(S, lab, ang=None):
    A, B, C, D, H = S
    out = [('tint', [A, B, H], 'orange'), ('seg', *A, *H, 'small', 3, True), ('right', *H, 0, 90, 12, 'small') if H[0] < B[0] else ('right', *H, 90, 180, 12, 'small'),
           ('txt', H[0] + 18, (A[1] + H[1]) / 2 - 10, 'h', 'small', 28, True)]
    return out
f2_pg9 = f2_pin(GEO('f2pg9', [
    ('line', _f2_spl(_s45, 45, '45°')),
    ('h45', _f2_sph(_s45, 'h')),
    ('p60', _f2_spl(_s60, 60, '60°')),
    ('h60', _f2_sph(_s60, 'h') + [('arc', *_s60[0], 26, 240, 270, 'orange', '30°', 48)]),
    ('p150', _f2_spl(_s150, 150, '150°')),
    ('h150', [('seg', _s150[1][0], _s150[1][1], 30, _s150[1][1], 'ink', 2, True)] + _f2_sph(_s150, 'h')
             + [('arc', *_s150[1], 44, 150, 180, 'orange', '30°', 70)]),
], vb='10 20 420 590', w=520, col=0, title='Parallelograms with 45, 60 and 150 degree angles'))
f2_k47s = [_R(IH('f2k47s%d' % i, t, size=30), y, x=1000) for i, (t, y) in enumerate([
    ('$h=\\frac{8}{\\sqrt2}$', 160), ('$=4\\sqrt2$', 225), ('$\\frac{8}{2}=4$', 420), ('$h=4\\sqrt3$', 485),
    ('$180°-150°=30°$', 680), ('$h=\\frac{8}{2}=4$', 745)])]
video('geo-047', 'lesson', slides=[
    S('The Parallelogram',
      L("The parallelogram. It's like a rectangle that someone squashed a little sideways.")),
    S('Sides',
      L("Take a rectangle and squash it a little sideways. That's a parallelogram.", show(f2_pg1['line'], 'Take a rectangle'),
        show(f2_pg1['para'], "That's a parallelogram")),
      L("Its opposite sides are equal and parallel. A D is equal and parallel to B C, and A B is equal and parallel to D C.",
        show(f2_pg1['ad'], 'A D is equal'), show(f2_pg1['ab'], 'and A B is equal'), show(f2_k47a, 'and parallel to D C'))),
    S('Angles',
      L("What do we know about the angles? Opposite angles are equal. Angle A equals angle C, and angle B equals angle D.",
        show(f2_pg2['line'], 'What do we know'), show(f2_pg2['opp'], 'Angle A equals'), show(f2_k47b, 'Opposite angles are equal')),
      L("And any two angles next to each other add up to a hundred eighty. D and C, a hundred eighty. A and D, a hundred "
        "eighty. B and C, and A and B, also a hundred eighty.", show(f2_k47c, 'And any two angles')),
      L("For example, if angle B is seventy, then angle D, across from it, is seventy too. Angles A and C sit next to B, so each one is a hundred eighty minus seventy, a hundred ten. And if "
        "an angle is a hundred twenty-five, the angle next to it is fifty-five.", show(f2_pg2['ex1'], 'For example'),
        show(f2_k47d, 'And if an angle'))),
    S('Why: parallel lines',
      L("Let's see why. The opposite sides are parallel, so let's extend them into long parallel lines. These two sides are "
        "parallel too, so we extend them as well.", show(f2_pg3['line'], "Let's see why"), show(f2_pg3['l1'], 'so let\'s extend them'),
        show(f2_pg3['l2'], 'These two sides')),
      L("Remember, when a line crosses two parallel lines, it makes small angles and large angles. Here the side A B "
        "crosses the two parallel lines through A D and B C. The angles at B and at A sit inside this U, so they add up to "
        "a hundred eighty.", pt('f2pg3_line', 'Here the side A B'), show(f2_pg3['u'], 'inside this U')),
      L("The side C D crosses the same two lines, and it's parallel to A B, so it makes the same angles. So in this tilted "
        "example, all the large angles are equal, we'll call them beta, and all the small ones are equal, we'll call them "
        "alpha. That's the first rule: opposite angles are equal. In a rectangle, they're all ninety.",
        show(f2_pg3['ab'], 'all the large angles')),
      L("And a small angle plus a large angle is a hundred eighty. So two angles next to each other add up to a hundred "
        "eighty: alpha plus beta is a hundred eighty.", show(f2_pg3['sum'], 'alpha plus beta'))),
    S('The diagonals',
      L("Now the diagonals. Are they equal? Not necessarily. Here there's a longer diagonal and a shorter one.",
        show(f2_pg4['line'], 'Now the diagonals'), show(f2_pg4['diag'], 'Here there\'s a longer')),
      L("What we do know is that they cut each other in half. This part equals this part, and this part equals this one.",
        show(f2_pg4['half'], 'they cut each other in half')),
      L("Do they cut the parallelogram's angles in half? Not necessarily, even though sometimes it looks like it. And they're "
        "not necessarily perpendicular either.", show(f2_pg4['not'], 'Do they cut')),
      L("If you're not sure, exaggerate. Draw a very wide, very low parallelogram, and draw a diagonal. You'll see right away "
        "that it doesn't cut the angle in half.", show(f2_pg4['exag'], 'Draw a very wide')),
      L("So a general parallelogram promises only one thing about its diagonals: they cut each other in half.",
        show(f2_k47f, 'a general parallelogram'))),
    S('Equal or perpendicular diagonals',
      L("Two more facts help us recognise special parallelograms. Both start from a shape we already know is a "
        "parallelogram. We don't need to prove them, just to know them."),
      L("If a parallelogram also has equal diagonals, it's a rectangle. Like this one: its diagonals are equal, and its "
        "angles are ninety degrees.", show(f2_pg8['line'], 'also has equal diagonals')),
      L("If a parallelogram also has perpendicular diagonals, it's a rhombus. Like this one: its diagonals meet at ninety "
        "degrees, and all four sides are equal.", show(f2_pg8['rh'], 'also has perpendicular diagonals')),
      L("Careful, both facts start from a parallelogram. This kite also has perpendicular diagonals, but it isn't a "
        "parallelogram, so it isn't a rhombus.", show(f2_pg8['ki'], 'This kite also has'), show(f2_k47e, 'both facts start from')), sb='The diagonals'),
    S('Area: base times height',
      L("The area of every parallelogram is simply base times height, a times h. The height is perpendicular to the base.",
        show(f2_pg5['line'], 'The area of every parallelogram'), show(f2_pg5['h'], 'The height is perpendicular'),
        show(f2_k47g, 'a times h')),
      L("It's not the sloping side. The sloping side is longer than the height.", show(f2_pg5['side'], "It's not the sloping side")),
      L("Be careful where you drop it. From A, the foot of the height lands on B C. From D, it would land outside B C, so "
        "first we extend B C.", show(f2_pg5['ext'], 'From D'))),
    S('Why: cut and move',
      L("Why base times height? Say we don't know the area of a parallelogram, but we do know the area of a rectangle. Let's "
        "draw a rectangle on the same base, with the same height.", show(f2_pg6['line'], 'Why base times height'),
        show(f2_pg6['rect'], "Let's draw a rectangle")),
      L("The difference between them is a triangle. This triangle on the left is in the rectangle, but not in the "
        "parallelogram.", show(f2_pg6['left'], 'This triangle on the left')),
      L("If we cut it out of the rectangle and move it to the right side, it fills exactly the part of the parallelogram "
        "that was missing. So the parallelogram has the same area as the rectangle.", show(f2_pg6['right'], 'If we cut it out')),
      L("The rectangle's area is base times height, so the parallelogram's area is a times h too.", show(f2_k47h, "The rectangle's area"))),
    S('Special angles',
      L("Exam questions love a parallelogram with a special angle: thirty, forty-five or sixty degrees. For example, sides of "
        "eight and six, with an angle of thirty degrees at B. What is the area?", show(f2_pg7['line'], 'For example')),
      L("Drop the height from A. A right triangle forms, with a thirty-degree angle: a gold triangle.",
        show(f2_pg7['h'], 'Drop the height'), show(f2_pg7['gold'], 'A right triangle forms')),
      L("The height is across from the thirty, so it's the short leg, half of the hypotenuse. The hypotenuse is the side of "
        "six, so the height is three. And the area is eight times three, which is twenty-four.",
        pt('f2pg7_line', 'The height is across'), show(f2_k47i, 'And the area')),
      L("A lot of students multiply eight times six, but the sloping side is not the height.", show(f2_pg7['wrong'], 'A lot of students')),
      L("The other special angles work the same way, each with its own right triangle.", pt('f2pg7_line', 'The other special angles'))),
    S('Forty-five, sixty, a hundred fifty',
      L("Let's start with forty-five degrees. Say the slanted side is eight, and the angle at B is forty-five. The height cuts off a right "
        "triangle with forty-five and forty-five, a silver triangle. The slanted side is its hypotenuse, so the height is a "
        "leg, eight over root two. Eight divided by two is four, so the height is four root two.",
        show(f2_pg9['line'], 'start with forty-five degrees'), show(f2_pg9['h45'], 'The height cuts off'),
        show(f2_k47s[0], 'eight over root two'), show(f2_k47s[1], 'so the height is four root two')),
      L("With sixty degrees at B, the right triangle is a gold triangle again. Its angle at the top is thirty. Across from "
        "the thirty is the short leg, at the bottom, so it's half of eight, four. The height is the long leg, so it's four "
        "root three.", show(f2_pg9['p60'], 'With sixty degrees'), show(f2_pg9['h60'], 'the right triangle is a gold'),
        show(f2_k47s[2], "so it's half of eight"), show(f2_k47s[3], 'The height is the long leg')),
      L("And with a hundred fifty degrees at B, the height from A lands outside, past B. So we extend C B beyond B. The angle "
        "next to the hundred fifty, on the straight line, is a hundred eighty minus a hundred fifty, which is thirty. So "
        "again the height is half the slanted side, four. [pause] Okay. I'll see you in the next video.",
        show(f2_pg9['p150'], 'And with a hundred fifty'), show(f2_pg9['h150'], 'So we extend C B'),
        show(f2_k47s[4], 'a hundred eighty minus a hundred fifty'), show(f2_k47s[5], 'half the slanted side')), sb='Special angles'),
])

# =================================================================================================================
# Topic-32 fragment f3 (2026-10-14): the parallelogram questions geo32-g048, geo32-g049, q-r26-t32-01, the rhombus lesson
# geo-050 and the rhombus question geo32-g051 (Hebrew geo 2016-2160). Question figure on the left (FIG_LEFT, figw 0.56),
# our colour copy built in layers on the right (Rule V3). Every Hebrew method is kept; plugging in numbers (a course
# addition in g048) is explained on its own, because psychometric thinking comes later in the study plan.
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g048', 'solve-geo32-g049', 'solve-q-r26-t32-01', 'solve-geo32-g051'})


def f3_pin(g):
    """keep every layer on its base figure even when a typed board item comes between them"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


def f3_poly(pts, col='ink', w=3):
    return [('seg', pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], col, w) for i in range(len(pts))]


def f3_lab(pts, names, off, size=26):
    return [('txt', pts[k][0] + off[k][0], pts[k][1] + off[k][1], names[k], 'ink', size, True) for k in range(len(pts))]


# ------------------------------------------------------------------------------------------------ geo32-g048 (Hebrew: the parallelogram's first example)
# Hebrew (geo 2018-2041): only angles; opposite angles equal, adjacent angles add up to 180; all of angle B plus all of
# angle C is 180, divide to get alpha + beta; the angle sum in the small triangle; "we never found alpha or beta, but the
# angle is ...". English numbers 3a/2a, 3b/2b -> 72. Course addition kept: plugging in equal numbers (a rectangle).
# V3: the copy; the whole angle B tinted teal (5 alpha), the whole angle C tinted orange (5 beta); then the small triangle
# BCE tinted inside the copy, then taken out and ENLARGED (same tint, labels 3 alpha, 3 beta, x) with the rest dimmed;
# x = 72 written on the enlarged triangle when found; the plug-in slide writes 90, 90 and 54, 54 the same way.
f3A8, f3B8, f3C8, f3D8, f3E8 = (291.283, 58.333), (202.717, 301.667), (348.717, 301.667), (437.283, 58.333), (306.937, 207.827)
f3aBA, f3aBE = gdir(*f3B8, *f3A8), gdir(*f3B8, *f3E8)
f3aCD, f3aCE = gdir(*f3C8, *f3D8), gdir(*f3C8, *f3E8)
f3aEB, f3aEC = gdir(*f3E8, *f3B8), gdir(*f3E8, *f3C8)
f3g48_lines = (f3_poly([f3A8, f3B8, f3C8, f3D8]) + [('seg', *f3B8, *f3E8, 'ink', 3), ('seg', *f3C8, *f3E8, 'ink', 3)]
               + f3_lab([f3A8, f3B8, f3C8, f3D8, f3E8], 'ABCDE', [(-14, -14), (-16, 16), (16, 16), (14, -14), (6, -22)])
               + [('arc', *f3B8, 26, 0, f3aBE, 'ink'), ('txt', 250, 286, '3α', 'ink', 20), ('arc', *f3B8, 44, f3aBE, f3aBA, 'ink'),
                  ('txt', 238, 246, '2α', 'ink', 20), ('arc', *f3C8, 26, f3aCE, 180, 'ink'), ('txt', 306, 276, '3β', 'ink', 20),
                  ('arc', *f3C8, 44, f3aCD, f3aCE, 'ink'), ('txt', 350, 234, '2β', 'ink', 20), ('arc', *f3E8, 20, f3aEB, f3aEC, 'ink'),
                  ('txt', 304, 238, 'x', 'ink', 20, True)])
f3g48 = f3_pin(GEO('f3g48', [
    ('line', f3g48_lines),
    ('wb', [('wedge', *f3B8, 62, 0, f3aBA, 'teal'), ('txt', 150, 262, '5α', 'teal', 28)]),
    ('wc', [('wedge', *f3C8, 62, f3aCD, 180, 'orange'), ('txt', 402, 262, '5β', 'orange', 28)]),
], vb='130 25 350 310', w=330, title='Parallelogram ABCD with the segments BE and CE'))
# the enlarged cut-out of triangle BCE (x2), drawn to the right of the parallelogram
f3eB, f3eC = (470.0, 300.0), (762.0, 300.0)
f3eE = (f3eB[0] + (f3E8[0] - f3B8[0]) * 2, f3eB[1] - (f3B8[1] - f3E8[1]) * 2)
f3BCE = [f3B8, f3C8, f3E8]
f3inside = [('tint', f3BCE, 'teal')] + f3_poly(f3BCE, 'teal', 4)


def f3_big(a3, b3, xl, col_x='red'):
    """the enlarged BCE with its three angle labels"""
    return ([('tint', [f3eB, f3eC, f3eE], 'teal')] + f3_poly([f3eB, f3eC, f3eE], 'teal', 4)
            + [('arc', *f3eB, 40, 0, f3aBE, 'teal'), ('txt', 535, 284, a3, 'teal', 26),
               ('arc', *f3eC, 40, f3aCE, 180, 'teal'), ('txt', 702, 278, b3, 'teal', 26),
               ('arc', *f3eE, 30, f3aEB, f3aEC, col_x), ('txt', f3eE[0], f3eE[1] + 58, xl, col_x, 26),
               ('txt', 455, 322, 'B', 'ink', 26, True), ('txt', 778, 322, 'C', 'ink', 26, True),
               ('txt', f3eE[0], f3eE[1] - 22, 'E', 'ink', 26, True)])


f3g48b = f3_pin(GEO('f3g48b', [
    ('line', f3g48_lines + [('txt', 300, 350, 'So far:  α + β = 36°', 'teal', 24)]),
    ('tri', f3inside),
    ('cut', [('dim', 130, 25, 330, 300)] + f3inside + f3_big('3α', '3β', 'x')),
    ('val', [('txt', f3eE[0] + 70, f3eE[1] + 8, '= 72°', 'red', 28)]),
], vb='130 25 660 340', w=440, title='The small triangle BCE, taken out and enlarged'))
# 2026-10-18 (batch C #218): the plug-in case is its own, correctly drawn RECTANGLE (an allowed parallelogram), with E
# where both base angles are 54 degrees (E above the middle of BC); the given figure on the left stays as it is
import math as _f3m
f3rB, f3rC, f3rA, f3rD = (150.0, 300.0), (450.0, 300.0), (150.0, 60.0), (450.0, 60.0)
f3rE = (300.0, 300.0 - 150.0 * _f3m.tan(_f3m.radians(54)))
f3g48p = f3_pin(GEO('f3g48p', [
    ('line', f3_poly([f3rA, f3rB, f3rC, f3rD]) + [('seg', *f3rB, *f3rE, 'ink', 3), ('seg', *f3rC, *f3rE, 'ink', 3)]
             + f3_lab([f3rA, f3rB, f3rC, f3rD, f3rE], 'ABCDE', [(-16, -14), (-16, 18), (16, 18), (16, -14), (0, -22)])
             + [('txt', 300, 340, 'a rectangle: one allowed case', 'teal', 20)]),
    ('b90', [('right', *f3rB, 0, 90, 18, 'teal'), ('right', *f3rC, 90, 180, 18, 'orange'),
             ('txt', 110, 230, '90°', 'teal', 22), ('txt', 490, 230, '90°', 'orange', 22)]),
    ('v54', [('tint', [f3rB, f3rC, f3rE], 'teal')] + f3_poly([f3rB, f3rC, f3rE], 'teal', 4)
            + [('arc', *f3rB, 44, 0, 54, 'teal', '54°', 74), ('arc', *f3rC, 44, 126, 180, 'teal', '54°', 74),
               ('arc', *f3rB, 64, 54, 90, 'ink', '36°', 88)]),
    ('x', [('arc', *f3rE, 26, gdir(*f3rE, *f3rB), gdir(*f3rE, *f3rC), 'red', 'x = 72°', 66)]),
], vb='90 20 420 335', w=300, title='Plugging in a rectangle: alpha = beta = 18'))
f3k48a = IH('f3k48a', '$5\\alpha+5\\beta=180°$', size=28)
f3k48b = IH('f3k48b', '$\\alpha+\\beta=36°$', size=28)
f3k48c = [IH('f3k48c%d' % i, t, size=28) for i, t in enumerate(['$x=180°-3\\alpha-3\\beta$', '$3\\alpha+3\\beta=3(\\alpha+\\beta)$',
                                                               '$=3\\cdot36°=108°$', '$x=180°-108°=72°$'])]
f3k48p = [IH('f3k48p%d' % i, t, size=26) for i, t in enumerate(['$5\\alpha=90°$', '$\\alpha=18°$', '$3\\cdot18°=54°$',
                                                               '$54°+54°=108°$', '$x=180°-108°$', '$x=72°$'])]
for _it, _y in [(f3g48, 200), (f3g48b, 200), (f3g48p, 200)]:
    _R(_it, _y)
f3k48w = I('f3k48w', 'Need the combination, not each letter', size=24)
for _k, _it in enumerate(f3k48c + [f3k48w]): _R(_it, 440 + 50 * _k)
for _k, _it in enumerate(f3k48p): _R(_it, 200 + 52 * _k, x=1350)
_R(f3k48a, 300, x=1375); _R(f3k48b, 355, x=1375)

video('solve-geo32-g048', 'solution', qid='geo32-g048', slides=[
    S('Adjacent angles',
      L("In parallelogram A B C D, the marked parts of angle B are three alpha and two alpha, and the marked parts of angle C "
        "are three beta and two beta. The segments B E and C E meet as in the accompanying figure. What is x?",
        pt('stem', 'In parallelogram A B C D', 'hl', 9.0), voice='calm', pause=0.5),
      L("There are only angles here, and letters instead of numbers. We need x, the angle at E between B E and C E. [short "
        "pause] We'll solve it in two different ways, the math way with the angle rules of a parallelogram, and then by "
        "plugging in numbers.",
        pt('fig: x', 'We need x')),
      L("[short pause] The math way first. What do we know about the angles of a parallelogram? Opposite angles are equal, and two angles next "
        "to each other add up to one hundred eighty. Angles B and C are next to each other, at the two ends of side B C.",
        show(f3g48['line'], 'What do we know')),
      L("All of angle B is three alpha plus two alpha, which is five alpha. All of angle C is three beta plus two beta, five "
        "beta. Together they make one hundred eighty.", show(f3g48['wb'], 'All of angle B'), show(f3g48['wc'], 'All of angle C'),
        show(f3k48a, 'Together they make')),
      L("Divide both sides by five, so that only alpha plus beta is left. Alpha plus beta is thirty-six. We don't know alpha or beta on their own, but we know "
        "their sum.", show(f3k48b, 'Divide both sides by five')), sb='Method 1 · The math way'),
    S('The triangle',
      L("Now look at triangle B C E, the small triangle at the bottom. Its angles are three alpha at B, three beta at C, and "
        "x at E. The angles of a triangle add up to one hundred eighty.", show(f3g48b['line'], 'Now look at triangle'),
        show(f3g48b['tri'], 'the small triangle at the bottom'), show(f3g48b['cut'], 'Its angles are three alpha')),
      L("So x is one hundred eighty minus three alpha minus three beta.", show(f3k48c[0], 'So x is one hundred eighty minus')),
      L("We know that alpha plus beta is thirty-six. Both terms, three alpha and three beta, have a factor three, so we can "
        "write them as three times that whole sum. Three times thirty-six is a hundred eight.",
        show(f3k48c[1], 'so we can write them'), show(f3k48c[2], 'Three times thirty-six')),
      L("So x is one hundred eighty minus a hundred eight, which is seventy-two.", show(f3k48c[3], 'So x is one hundred eighty'),
        show(f3g48b['val'], 'which is seventy-two')),
      L("We never found alpha or beta, but x is seventy-two. Choice number two is our answer.",
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("This idea comes back a lot. When we can't find each letter on its own, we look for the combination the question "
        "needs. Here x needed three alpha plus three beta, and that's three times the sum we knew. So we never needed "
        "alpha or beta alone.", show(f3k48w, 'we look for the combination')),
      sb='Method 1 · The math way'),
    S('Plugging in numbers',
      L("[pause] Now let's plug in numbers. The question expects one value of x for every parallelogram that fits the "
        "figure. So we may choose one allowed parallelogram that's easy to work with. A rectangle is a parallelogram, so "
        "let's try ninety degrees at B and at C.", show(f3g48p['line'], 'A rectangle is a parallelogram'),
        show(f3g48p['b90'], "let's try ninety degrees")),
      L("Angle B is five alpha, so five alpha is ninety, and alpha is eighteen. Angle C is five beta, so in the same way, "
        "beta is eighteen.", show(f3k48p[0], 'so five alpha is ninety'), show(f3k48p[1], 'and alpha is eighteen')),
      L("In triangle B C E, three alpha is three times eighteen, fifty-four, and three beta is fifty-four too.",
        show(f3k48p[2], 'three alpha is three times eighteen'), show(f3g48p['v54'], 'and three beta is fifty-four')),
      L("The angles of a triangle add up to one hundred eighty. Fifty-four plus fifty-four is a hundred eight. So x is one "
        "hundred eighty minus a hundred eight, which is seventy-two. That's the same seventy-two as in the math way. "
        "Choice number two again. [pause] Okay. I'll see you in the next question.",
        show(f3k48p[3], 'Fifty-four plus fifty-four'), show(f3k48p[4], 'So x is one hundred eighty'),
        show(f3k48p[5], 'which is seventy-two'), show(f3g48p['x'], 'is seventy-two. That'), mk('tick', 'choice 2', 'Choice number two again')), sb='Method 2 · Plugging in numbers'),
])

# ------------------------------------------------------------------------------------------------ geo32-g049 (Hebrew: the parallelogram's second example)
# Hebrew (geo 2044-2069): the perpendicular makes a right triangle -> Pythagoras ("a lot"; similarity later); draw the
# givens conveniently: opposite sides equal (AB = CD, BC = AD), BE = what's left; a Pythagorean triple gives the height;
# area = base x height. English numbers 24, 17, 16 -> 8, 15, 17 -> 360. Course addition kept: the 408 trap.
# V3: the copy; AB traced teal with 17, BC traced orange with 24, BE red with 8; the right triangle ABE tinted inside the
# copy, then a focus step (the rest dimmed, ABE kept with its labels; it is big enough, no enlargement); 15 written on AE.
f3PA, f3PB, f3PC, f3PD, f3PE = (194.857, 54.857), (90.571, 305.143), (445.143, 305.143), (549.429, 54.857), (194.857, 305.143)
f3g49_lines = (f3_poly([f3PA, f3PB, f3PC, f3PD]) + [('seg', *f3PA, *f3PE, 'ink', 3), ('right', *f3PE, 90, 0, 16, 'ink')]
               + f3_lab([f3PA, f3PB, f3PC, f3PD, f3PE], 'ABCDE', [(-14, -16), (-16, 16), (16, 16), (14, -16), (0, 28)])
               + [('txt', 372, 34, '24', 'ink', 24), ('txt', 523, 180, '17', 'ink', 24), ('txt', 320, 330, '16', 'ink', 24)])
# the enlarged cut-out of triangle ABE (legs 8 and 15, hypotenuse 17), drawn on a cleared patch on the right
f3cE, f3cA, f3cB = (560.0, 300.0), (560.0, 70.0), (437.0, 300.0)
f3g49 = f3_pin(GEO('f3g49', [
    ('line', f3g49_lines),
    ('ab', [('seg', *f3PA, *f3PB, 'teal', 5), ('txt', 116, 172, '17', 'teal', 26)]),
    ('bc', [('seg', *f3PB, *f3PC, 'orange', 5), ('txt', 250, 352, 'BC = 24', 'orange', 24)]),
    ('be', [('seg', *f3PB, *f3PE, 'red', 6), ('txt', 142, 330, '8', 'red', 26)]),
    ('tri', [('tint', [f3PA, f3PB, f3PE], 'teal'), ('seg', *f3PA, *f3PB, 'teal', 4), ('seg', *f3PB, *f3PE, 'teal', 4),
             ('seg', *f3PE, *f3PA, 'teal', 4)]),
    ('cut', [('dim', 60, 10, 570, 360), ('tint', [f3PA, f3PB, f3PE], 'teal'), ('seg', *f3PA, *f3PB, 'teal', 4),
             ('seg', *f3PB, *f3PE, 'teal', 4), ('seg', *f3PE, *f3PA, 'teal', 4), ('right', *f3PE, 90, 180, 16, 'teal'),
             ('txt', 180, 38, 'A', 'ink', 26, True), ('txt', 74, 322, 'B', 'ink', 26, True), ('txt', 195, 332, 'E', 'ink', 26, True),
             ('txt', 116, 172, '17', 'teal', 28), ('txt', 142, 330, '8', 'red', 28)]),
    ('h15', [('txt', 220, 180, '15', 'orange', 30)]),
    # 2026-10-18 (batch C #219): back to the WHOLE parallelogram for its area: base BC 24 and the height AE 15
    ('whole', [('dim', 60, 10, 570, 360), ('tint', [f3PA, f3PB, f3PC, f3PD], 'teal')] + f3_poly([f3PA, f3PB, f3PC, f3PD], 'ink', 3)
              + f3_lab([f3PA, f3PB, f3PC, f3PD, f3PE], 'ABCDE', [(-14, -16), (-16, 16), (16, 16), (14, -16), (0, 28)])
              + [('seg', *f3PB, *f3PC, 'orange', 6), ('txt', 320, 352, 'BC = 24', 'orange', 26), ('seg', *f3PA, *f3PE, 'orange', 4, True),
                 ('right', *f3PE, 90, 0, 16, 'orange'), ('txt', 222, 180, '15', 'orange', 30)]),
], vb='60 10 570 360', w=300, title='Parallelogram ABCD with the height AE'))
f3k49 = [IH('f3k49%s' % i, t, size=28) for i, t in enumerate(['$S=24\\cdot15$', '$24\\cdot10=240$', '$24\\cdot5=120$', '$240+120=360$'])]
f3k49a = f3k49[0]
_R(f3g49, 200)
for _k, _it in enumerate(f3k49): _R(_it, 200 + 54 * _k, x=1350)

video('solve-geo32-g049', 'solution', qid='geo32-g049', slides=[
    S('Opposite sides, then Pythagoras',
      L("A B C D is a parallelogram, and A E is perpendicular to B C. Given: A D is twenty-four centimeters, C D is "
        "seventeen centimeters, and E C is sixteen centimeters. What is the area of the parallelogram, in square "
        "centimeters?", pt('stem', 'A B C D is a parallelogram', 'hl', 9.0), voice='calm', pause=0.5),
      L("The area of a parallelogram is base times height. The base can be B C, and its height is A E, the perpendicular. "
        "But we don't know A E. [short pause] A E is perpendicular to B C, so A B E is a right triangle. We can use it, "
        "with Pythagoras, to find the height.", pt('fig: E', 'so A B E is a right triangle')),
      L("[short pause] Let's write the givens on the figure in a more convenient way. Opposite sides of a parallelogram are "
        "equal. C D is seventeen, so A B is also seventeen.", show(f3g49['line'], "Let's write the givens"),
        show(f3g49['ab'], 'so A B is also seventeen')),
      L("A D is twenty-four, so all of B C is twenty-four too. E C is sixteen, so what's left, B E, is twenty-four minus "
        "sixteen, which is eight.", show(f3g49['bc'], 'so all of B C'), show(f3g49['be'], "so what's left")),
      L("Now look at the right triangle A B E. Let's look only at it. Its legs are B E, eight, and A E, which "
        "we're looking for. Its hypotenuse is A B, seventeen.", show(f3g49['tri'], 'Now look at the right triangle'),
        show(f3g49['cut'], "Let's look only at it")),
      L("Eight, fifteen, seventeen is a Pythagorean triple. So the missing leg is fifteen, and that's the height A E.",
        show(f3g49['h15'], 'So the missing leg is fifteen')),
      L("Now back to the whole parallelogram. The area is base times height, so it's B C, twenty-four, times A E, fifteen.",
        show(f3g49['whole'], 'Now back to the whole parallelogram'), show(f3k49[0], "so it's B C, twenty-four")),
      L("Twenty-four times fifteen is twenty-four times ten plus twenty-four times five. Twenty-four times ten is two "
        "hundred forty. Twenty-four times five is a hundred twenty. Two hundred forty plus a hundred twenty is three hundred "
        "sixty. Choice number three is our answer.", show(f3k49[1], 'Twenty-four times ten is'), show(f3k49[2], 'Twenty-four times five is'),
        show(f3k49[3], 'Two hundred forty plus'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Careful, choice number four, four hundred eight, uses the slanted side seventeen instead of the height. That isn't "
        "the area formula. [pause] Okay. I'll see you in the next question.", mk('cross', 'choice 4', 'choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t32-01 (course question)
# Course question (no Hebrew source): the height of an obtuse parallelogram falls outside; extend the base; the angle on
# the straight line is 30; a gold triangle (30-60-90, topic 31): the short leg is half the hypotenuse; area = 14 x 5.
# Traps kept: 140 (the slanted side), 70 root 3 (the long leg), 35 (the triangle formula).
# V3: the copy; the base BC traced teal with 14; point at B, then the dashed extension of CB; the dashed height AH with its
# right angle; the 30 at B; triangle ABH tinted, then taken out ENLARGED below (10, 30, right angle); 5 written on AH
# (in the copy and the cut-out) when found.
f3QA, f3QB, f3QC, f3QD, f3QH = (79.474, 140.0), (270.0, 250.0), (578.0, 250.0), (387.474, 140.0), (79.474, 250.0)
f3aBAq = gdir(*f3QB, *f3QA)
# the enlarged cut-out of ABH (x1.3) under the parallelogram
f3eH1, f3eB1 = (60.0, 440.0), (60.0 + 1.3 * 190.526, 440.0)
f3eA1 = (60.0, 440.0 - 1.3 * 110.0)
f3t01_lines = (f3_poly([f3QA, f3QB, f3QC, f3QD]) + f3_lab([f3QA, f3QB, f3QC, f3QD], 'ABCD', [(-12, -16), (6, 26), (16, 20), (12, -16)])
               + [('arc', *f3QB, 26, 0, f3aBAq, 'ink'), ('txt', 300, 205, '150°', 'ink', 22), ('txt', 424, 278, '14', 'ink', 28),
                  ('txt', 150, 198, '10', 'ink', 28)])
f3t01 = f3_pin(GEO('f3t01', [
    ('line', f3t01_lines),
    ('base', [('seg', *f3QB, *f3QC, 'teal', 5)]),
    ('ext', [('dot', *f3QB), ('seg', *f3QB, *f3QH, 'teal', 3, True)]),
    ('h', [('seg', *f3QA, *f3QH, 'orange', 3, True), ('right', *f3QH, 0, 90, 16, 'orange'), ('txt', 62, 272, 'H', 'ink', 26, True)]),
    ('a30', [('tint', [f3QA, f3QB, f3QH], 'teal'), ('arc', *f3QB, 46, f3aBAq, 180, 'teal', '30°', 70)]),
    ('cut', [('tint', [f3eA1, f3eB1, f3eH1], 'teal')] + f3_poly([f3eA1, f3eB1, f3eH1], 'teal', 4)
             + [('right', *f3eH1, 0, 90, 18, 'orange'), ('arc', *f3eB1, 50, gdir(*f3eB1, *f3eA1), 180, 'teal', '30°', 82),
                ('txt', 196, 356, '10', 'ink', 28), ('txt', 44, 300, 'A', 'ink', 26, True),
                ('txt', 326, 462, 'B', 'ink', 26, True), ('txt', 44, 462, 'H', 'ink', 26, True)]),
    ('ah', [('txt', 500, 350, 'AH = 10 ÷ 2 = 5', 'red', 30)]),
    ('h5', [('txt', 54, 196, '5', 'orange', 34), ('txt', 40, 376, '5', 'orange', 34)]),
    # 2026-10-18 (batch C #220): the area of the WHOLE parallelogram, BC 14 with AH 5; the cut-out stays as the reference
    ('whole', [('tint', [f3QA, f3QB, f3QC, f3QD], 'small'), ('seg', *f3QB, *f3QC, 'teal', 5), ('seg', *f3QA, *f3QH, 'orange', 4, True)]),
    ('area', [('txt', 500, 410, 'S = 14 · 5', 'red', 30)]),
    ('area2', [('txt', 500, 452, '= 70', 'red', 30)]),
], vb='20 100 610 375', w=470, title='Parallelogram ABCD with the height AH outside'))
_R(f3t01, 215)

video('solve-q-r26-t32-01', 'solution', qid='q-r26-t32-01', slides=[
    S('Extend the base',
      L("A B C D is a parallelogram. Given: A B is ten centimeters, B C is fourteen centimeters, and angle A B C is one "
        "hundred fifty degrees. What is the area of the parallelogram, in square centimeters?",
        pt('stem', 'A B C D is a parallelogram', 'hl', 8.0), voice='calm', pause=0.5),
      L("The area of a parallelogram is base times height. The base B C is fourteen, so we need the height to B C. [short "
        "pause] Angle B is obtuse, so first we need to see where that height falls.", pt('fig: 150°', 'Angle B is obtuse')),
      L("[short pause] Here's the base, B C, fourteen. Angle B is obtuse, so A is to the left of B. The perpendicular from A "
        "would land left of B, outside the segment B C.", show(f3t01['line'], "Here's the base"), show(f3t01['base'], 'B C, fourteen')),
      L("So first we start at B and extend C B beyond B. Now we draw the perpendicular from A to that line, and call its "
        "foot H.", show(f3t01['ext'], 'So first we start at B'), show(f3t01['h'], 'Now we draw the perpendicular')),
      L("Angle A B H and angle A B C sit together on one straight line, so angle A B H is one hundred eighty minus one "
        "hundred fifty, which is thirty.", show(f3t01['a30'], 'so angle A B H is')),
      L("Triangle A B H has a right angle and a thirty degree angle, so it's a gold triangle, thirty, sixty, ninety. A B is "
        "its hypotenuse, ten. The height A H is across from the thirty, so it's the short leg, and the short leg is half "
        "the hypotenuse. Half of ten is five.", show(f3t01['cut'], 'Triangle A B H has'), show(f3t01['ah'], 'Half of ten is five'),
        show(f3t01['h5'], 'Half of ten')),
      L("Careful, the long leg is B H, five root three, and it isn't the height. That's where seventy root three, choice "
        "number two, comes from. And the height is five, not the slanted side ten. Fourteen times ten, a hundred forty, is "
        "choice number one, another trap.", mk('cross', 'choice 2', 'That\'s where seventy root three'),
        mk('cross', 'choice 1', 'Fourteen times ten, a hundred forty')),
      L("Now the area of the whole parallelogram, base times height. The base is B C, fourteen, and the height to it is A "
        "H, five. Fourteen times five is seventy. We don't divide by two, because it's a parallelogram, not a triangle. "
        "Thirty-five, choice number four, is that trap. Choice number three is our answer.",
        show(f3t01['whole'], 'Now the area of the whole parallelogram'), show(f3t01['area'], 'Fourteen times five'),
        show(f3t01['area2'], 'is seventy'), mk('cross', 'choice 4', 'Thirty-five, choice number four'),
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("So here's the rule. When the slanted side meets the base at thirty or at a hundred fifty degrees, the height to "
        "that base is half the slanted side. Here A B meets the line of B C at a hundred fifty, so A H is half of A B. "
        "[pause] Okay. I'll see you in the next question.", pt('fig: 150°', 'When the slanted side meets'),
        pt('f3t01_line', 'Here A B meets'))),
])

# ------------------------------------------------------------------------------------------------ geo-050 (lesson: The Rhombus)
# Hebrew (geo 2074-2120): all sides equal, opposite angles equal; a "perfected parallelogram"; we shortened a parallelogram
# into a rhombus; the diagonals: perpendicular, not equal (long and short), bisect each other, bisect the angles; instead of
# remembering the rules remember the shape and its symmetry (right = left, top = bottom); area = diagonal x diagonal / 2,
# with why (half-diagonals = legs, x 4). Course additions kept: equal diagonals -> a square; diagonals 10 and 6 -> 30; base x
# height works too. Added examples: side 7 -> perimeter 28; 60 and 120 angles; diagonals 8 and 12 -> 48.
# V3: a clean generic rhombus; ticks on all four sides; opposite angles in matching colours; the diagonals drawn in at the
# words with their right angle, halves ticked and half-angles; the symmetry as tints (left/right teal, top/bottom orange);
# for the area one small right triangle tinted, its legs = the half-diagonals.
f3RA, f3RB, f3RC, f3RD, f3RO = (320.0, 30.0), (200.0, 180.0), (320.0, 330.0), (440.0, 180.0), (320.0, 180.0)
f3rh = [f3RA, f3RB, f3RC, f3RD]
f3rh_lab = f3_lab(f3rh, 'ABCD', [(0, -18), (-22, 0), (0, 22), (22, 0)])
f3aAB, f3aAD = gdir(*f3RA, *f3RB), gdir(*f3RA, *f3RD)
f3aBA, f3aBC = gdir(*f3RB, *f3RA), gdir(*f3RB, *f3RC)
f3aCB, f3aCD = gdir(*f3RC, *f3RB), gdir(*f3RC, *f3RD)
f3aDC, f3aDA = gdir(*f3RD, *f3RC), gdir(*f3RD, *f3RA)
f3sides = [('tick', *f3RA, *f3RB, 1), ('tick', *f3RB, *f3RC, 1), ('tick', *f3RC, *f3RD, 1), ('tick', *f3RD, *f3RA, 1)]
f3r1 = GEO('f3r1', [
    ('line', f3_poly(f3rh) + f3rh_lab + f3sides),
    ('ang', [('arc', *f3RA, 34, f3aAB, f3aAD, 'small'), ('arc', *f3RC, 34, f3aCD, f3aCB, 'small'),
             ('arc', *f3RB, 30, f3aBC, f3aBA, 'large'), ('arc', *f3RD, 30, f3aDA, f3aDC, 'large')]),
    ('par', [('par', *f3RB, *f3RA, 1), ('par', *f3RC, *f3RD, 1), ('par', *f3RA, *f3RD, 2), ('par', *f3RB, *f3RC, 2)]),
], vb='140 -15 360 370', w=520, col=0, title='A rhombus')
f3r2 = GEO('f3r2', [
    ('line', f3_poly(f3rh) + f3rh_lab),
    ('diag', [('seg', *f3RA, *f3RC, 'teal', 3), ('seg', *f3RB, *f3RD, 'teal', 3), ('right', *f3RO, 0, 90, 16, 'teal')]),
    ('len', [('txt', 350, 96, 'long', 'orange', 24), ('txt', 270, 164, 'short', 'teal', 24)]),
    ('half', [('tick', *f3RA, *f3RO, 1, 'orange'), ('tick', *f3RO, *f3RC, 1, 'orange'), ('tick', *f3RB, *f3RO, 2, 'teal'),
              ('tick', *f3RO, *f3RD, 2, 'teal')]),
    ('hang', [('arc', *f3RA, 40, f3aAB, 270, 'small'), ('arc', *f3RA, 48, 270, f3aAD, 'small'),
              ('arc', *f3RB, 30, f3aBC, 0, 'large'), ('arc', *f3RB, 38, 0, f3aBA, 'large')]),
], vb='140 -15 360 370', w=520, col=0, title='The diagonals of a rhombus')
f3r3 = GEO('f3r3', [
    ('line', f3_poly(f3rh) + f3rh_lab + f3sides + [('seg', *f3RA, *f3RC, 'ink', 2, True), ('seg', *f3RB, *f3RD, 'ink', 2, True)]),
    ('lr', [('tint', [f3RA, f3RB, f3RC], 'teal'), ('tint', [f3RA, f3RD, f3RC], 'teal'), ('seg', *f3RA, *f3RC, 'teal', 5)]),
    ('tb', [('dim', 140, -15, 360, 370), ('tint', [f3RB, f3RA, f3RD], 'orange'), ('tint', [f3RB, f3RC, f3RD], 'orange'),
            ('seg', *f3RB, *f3RD, 'orange', 5)] + f3_poly(f3rh) + f3rh_lab),
], vb='140 -15 360 370', w=520, col=0, title='The rhombus is symmetric')
f3r4 = GEO('f3r4', [
    ('line', f3_poly(f3rh) + f3rh_lab + [('seg', *f3RA, *f3RC, 'ink', 2, True), ('seg', *f3RB, *f3RD, 'ink', 2, True)]),
    ('q', [('tint', [f3RA, f3RO, f3RD], 'teal'), ('right', *f3RO, 0, 90, 16, 'teal'), ('txt', 340, 108, 'd₁/2', 'orange', 22),
           ('txt', 380, 200, 'd₂/2', 'teal', 22)]),
    # 2026-10-18 (batch C #221): the four matching quarters, then the WHOLE rhombus for the whole-area formula
    ('four', [('tint', [f3RA, f3RO, f3RB], 'orange'), ('tint', [f3RB, f3RO, f3RC], 'teal'), ('tint', [f3RC, f3RO, f3RD], 'orange'),
              ('right', *f3RO, 90, 180, 16, 'teal'), ('right', *f3RO, 180, 270, 16, 'teal'), ('right', *f3RO, 270, 360, 16, 'teal')]),
    ('whole', f3_poly(f3rh, 'teal', 5)),
], vb='140 -15 360 370', w=520, col=0, title='One of the four right triangles')
f3r5 = GEO('f3r5', [
    ('line', f3_poly(f3rh, 'ink', 3) + f3rh_lab + [('tint', f3rh, 'teal'), ('seg', *f3RA, *f3RC, 'orange', 3), ('seg', *f3RB, *f3RD, 'teal', 3),
              ('right', *f3RO, 0, 90, 16, 'teal'), ('txt', 296, 105, '6', 'orange', 26), ('txt', 296, 255, '6', 'orange', 26),
              ('txt', 260, 200, '4', 'teal', 26), ('txt', 380, 200, '4', 'teal', 26)]),
    ('q', [('tint', [f3RA, f3RO, f3RD], 'orange'), ('seg', *f3RA, *f3RD, 'orange', 4)]),
], vb='140 -15 360 370', w=460, col=0, title='A rhombus with diagonals 12 and 8')
f3r2sq = GEO('f3r2sq', [
    ('line', f3_poly([(40, 30), (40, 150), (160, 150), (160, 30)]) + [('seg', 40, 30, 160, 150, 'teal', 3), ('seg', 160, 30, 40, 150, 'teal', 3),
              ('tick', 40, 30, 160, 150, 1, 'orange'), ('tick', 160, 30, 40, 150, 1, 'orange'), ('right', 100, 90, 225, 315, 12, 'teal'),
              ('txt', 260, 70, 'IF the diagonals', 'teal', 20), ('txt', 260, 96, 'are equal:', 'teal', 20), ('txt', 260, 122, 'a square', 'teal', 20)]),
], vb='20 10 340 160', w=420, col=1, title='A rhombus with equal diagonals is a square')
for _g in (f3r1, f3r2, f3r3, f3r4, f3r5, f3r2sq): f3_pin(_g)
f3r_t1 = IH('f3r_t1', 'Side $7$: $\\ P=4\\cdot7=28$', size=30, col=1)
f3r_t2 = I('f3r_t2', '$60°$ and $60°$, $\\ 120°$ and $120°$', size=30, col=1)
f3r_t4 = I('f3r_t4', '$S=\\frac{d_1\\cdot d_2}{2}$', size=36, col=1)
f3r_q1 = IH('f3r_q1', '$\\frac{d_1}{2}\\cdot\\frac{d_2}{2}=\\frac{d_1 d_2}{4}$', size=30, col=1)
f3r_q2 = IH('f3r_q2', 'one triangle: $\\frac{d_1 d_2}{4}\\div2=\\frac{d_1 d_2}{8}$', size=30, col=1)
f3r_q3 = IH('f3r_q3', '$4\\cdot\\frac{d_1 d_2}{8}=\\frac{d_1 d_2}{2}$', size=30, col=1)
f3r_e = [IH('f3r_e%d' % i, t, size=30, col=1) for i, t in enumerate(['$\\frac{4\\cdot6}{2}=12$', '$4\\cdot12=48$', '$8\\cdot12=96$',
                                                                   '$\\frac{96}{2}=48$', '$10\\cdot6=60$', '$\\frac{60}{2}=30$'])]
f3r_t7 = I('f3r_t7', 'Symmetric: right $=$ left, top $=$ bottom', size=28, col=1)

video('geo-050', 'lesson', slides=[
    S('The Rhombus',
      L("The rhombus.")),
    S('Four equal sides',
      L("A rhombus is a quadrilateral with all four sides equal. Its opposite angles are equal too.",
        show(f3r1['line'], 'A rhombus is a quadrilateral'), show(f3r1['ang'], 'Its opposite angles')),
      L("A rhombus is a parallelogram with all four sides equal. So, like every parallelogram, its opposite sides are "
        "equal and parallel, and on top of that, all four sides are equal. In the quadrilaterals lesson, we shortened a parallelogram until all its "
        "sides were equal, and that gave us a rhombus.", show(f3r1['par'], 'its opposite sides are equal and parallel')),
      L("For example, a rhombus with side seven has a perimeter of four times seven, twenty-eight. And if one angle is sixty "
        "degrees, the opposite angle is sixty too, and the other two are one hundred twenty each, because two angles next "
        "to each other add up to one hundred eighty, like in every parallelogram.", show(f3r_t1, 'a rhombus with side seven'),
        show(f3r_t2, 'if one angle is sixty'))),
    S('The diagonals',
      L("Now the diagonals. They're perpendicular to each other, so they meet at a right angle.",
        show(f3r2['line'], 'Now the diagonals'), show(f3r2['diag'], "They're perpendicular")),
      L("Are they equal? Not necessarily. Usually there's a long diagonal and a short one, like here. Only if the two "
        "diagonals are equal, the rhombus is a square, like this one.", show(f3r2['len'], "Usually there's a long diagonal"),
        show(f3r2sq['line'], 'Only if the two')),
      L("Let's go back to our rhombus. Its diagonals cut each other in half, and they also cut the angles of the rhombus in half.",
        show(f3r2['half'], 'Its diagonals cut each other'), show(f3r2['hang'], 'they also cut the angles'))),
    S('Remember: symmetry',
      L("Instead of remembering all these rules, the sides, the angles and the diagonals, just remember the shape, and "
        "remember that it's symmetric.", show(f3r3['line'], 'just remember the shape'), show(f3r_t7, "remember that it's symmetric")),
      L("The diagonal A C is a line of symmetry. Fold along it, and the triangle on the right lands exactly on the triangle "
        "on the left. So the "
        "sides up here are equal, the sides down here are equal, and the angle on the right equals the angle on the left.",
        show(f3r3['lr'], 'The diagonal A C is a line of symmetry')),
      L("And the other diagonal, B D, is a line of symmetry too. Fold along it, and the top triangle lands exactly on the "
        "bottom one. So the top angle equals the bottom angle.", show(f3r3['tb'], 'the other diagonal, B D')),
      L("So all the sides are equal, opposite angles are equal, and the diagonals are perpendicular, cut each other in half, "
        "and cut the angles in half.", pt('f3r_t7', 'So all the sides are equal'))),
    S('Area: d₁ × d₂ / 2',
      L("The area of a rhombus is the product of the diagonals, over two. Why? The diagonals meet at ninety degrees, and they "
        "cut each other in half. So they split the rhombus into four equal right triangles. Look at one of them. Its legs "
        "are half of one diagonal and half of the other.", show(f3r4['line'], 'The area of a rhombus'),
        show(f3r4['q'], 'Look at one of them')),
      L("Its area is leg times leg, over two. Half of one diagonal times half of the other is the product of the "
        "diagonals, over four. Then we divide by two, so one triangle is the product of the diagonals, over eight.",
        show(f3r_q1, 'Half of one diagonal times'), show(f3r_q2, 'Then we divide by two')),
      L("The rhombus is four of these triangles, so we multiply by four. Four times that is the product of the "
        "diagonals, over two. That's diagonal times diagonal, over two.", show(f3r4['four'], 'The rhombus is four'),
        show(f3r_q3, 'Four times that is'), show(f3r4['whole'], "That's diagonal times diagonal"), show(f3r_t4, 'diagonal times diagonal, over two'))),
    S('Area: two examples',
      L("Let's see it in numbers, with diagonals twelve and eight. The legs of one small triangle are six and four. Its area "
        "is four times six over two, which is twelve.", show(f3r5['line'], 'with diagonals twelve and eight'),
        show(f3r5['q'], 'The legs of one small triangle'), show(f3r_e[0], 'Its area is four times six')),
      L("Four triangles make four times twelve, forty-eight. And with the formula, eight times twelve is ninety-six, and "
        "ninety-six over two is forty-eight too.", show(f3r_e[1], 'Four triangles make'), show(f3r_e[2], 'eight times twelve is'),
        show(f3r_e[3], 'ninety-six over two')),
      L("Another one, diagonals ten and six. Ten times six is sixty, and sixty over two is thirty.",
        show(f3r_e[4], 'Ten times six'), show(f3r_e[5], 'sixty over two')),
      L("And a rhombus is also a parallelogram, so base times height works too, if that's what you're given. [pause] Okay. "
        "I'll see you in the next video.", pt('f3r5_line', 'base times height works too')), sb='Area: d₁ × d₂ / 2'),
])

# ------------------------------------------------------------------------------------------------ geo32-g051 (Hebrew: the rhombus question)
# Hebrew (geo 2122-2159): why "absolute" difference; two equations with two unknowns (a the bigger one), add them, b
# cancels; the other diagonal; the diagonals bisect each other (halves); the side from a right triangle and a Pythagorean
# triple; all sides equal -> perimeter; the closing tip (a rhombus is symmetric). English 46 / 14 -> 30, 16 -> 15, 8, 17 -> 68.
# Course addition: the 240 trap (the area).
# V3: typed equations first; then the copy (enlarged, the rhombus is thin) with the diagonals traced and their lengths, the
# halves written on, one quarter triangle tinted inside the copy and then an ENLARGED cut-out of it (same tint, labels 8 and
# 15) where the side 17 is found; 17 written on the original side too.
f3MA, f3MB, f3MC, f3MD, f3MO = (320.0, 45.231), (263.846, 180.0), (320.0, 314.769), (376.154, 180.0), (320.0, 180.0)
f3g51_lines = f3_poly([f3MA, f3MB, f3MC, f3MD]) + [('seg', *f3MA, *f3MC, 'ink', 3), ('seg', *f3MB, *f3MD, 'ink', 3)] + \
    f3_lab([f3MA, f3MB, f3MC, f3MD], 'ABCD', [(0, -20), (-22, 0), (0, 24), (22, 0)])
f3qE, f3qT, f3qR = (470.0, 320.0), (470.0, 80.0), (598.0, 320.0)       # enlarged quarter: legs 15 (up) and 8 (right)
f3g51 = f3_pin(GEO('f3g51', [
    ('line', f3g51_lines),
    ('ac', [('seg', *f3MA, *f3MC, 'teal', 5), ('txt', 236, 112, 'AC = 30', 'teal', 26)]),
    ('bd', [('seg', *f3MB, *f3MD, 'orange', 5), ('txt', 236, 252, 'BD = 16', 'orange', 26)]),
    ('half', [('tick', *f3MA, *f3MO, 1, 'teal'), ('tick', *f3MO, *f3MC, 1, 'teal'), ('tick', *f3MB, *f3MO, 2, 'orange'),
              ('tick', *f3MO, *f3MD, 2, 'orange'), ('txt', 302, 120, '15', 'teal', 24), ('txt', 352, 162, '8', 'orange', 24)]),
    ('q', [('tint', [f3MA, f3MO, f3MD], 'teal'), ('seg', *f3MA, *f3MD, 'teal', 5), ('right', *f3MO, 0, 90, 12, 'teal')]),
    ('cut', [('tint', [f3qT, f3qE, f3qR], 'teal')] + f3_poly([f3qT, f3qE, f3qR], 'teal', 4)
            + [('right', *f3qE, 0, 90, 18, 'teal'), ('txt', 450, 200, '15', 'teal', 30), ('txt', 534, 346, '8', 'orange', 30),
               ('txt', 470, 62, 'A', 'ink', 24, True), ('txt', 452, 340, 'O', 'ink', 24, True),
               ('txt', 612, 340, 'D', 'ink', 24, True)]),
    ('s17', [('txt', 560, 190, '17', 'red', 32), ('txt', 372, 100, '17', 'red', 24)]),
    ('per', [('txt', 560, 45, 'P = 4 · 17 = 68', 'red', 24)]),
], vb='170 5 470 355', w=520, title='Rhombus ABCD with its diagonals'))
f3k51a = IH('f3k51a', '$a+b=46$', size=32)
f3k51b = IH('f3k51b', '$a-b=14$', size=32)
f3k51 = [IH('f3k51c%d' % i, t, size=30) for i, t in enumerate(['$2a=60$', '$a=\\frac{60}{2}=30$', '$30+b=46$', '$b=46-30=16$'])]
for _it, _y in [(f3k51a, 230), (f3k51b, 290), (f3g51, 190)] + [(_x, 360 + 62 * _k) for _k, _x in enumerate(f3k51)]:
    _R(_it, _y)

video('solve-geo32-g051', 'solution', qid='geo32-g051', slides=[
    S('Two equations',
      L("The sum of the lengths of the diagonals of a rhombus is forty-six centimeters. The absolute difference between "
        "their lengths is fourteen centimeters. What is its perimeter, in centimeters?",
        pt('stem', 'The sum of the lengths', 'hl', 8.0), voice='calm', pause=0.5),
      L("What does absolute difference mean? It means the gap between the two lengths, whichever one we name first. Here "
        "that gap is fourteen. [short pause] We'll find the two diagonals first, and then use them to find the side.",
        pt('stem', 'What does absolute difference mean')),
      L("[short pause] Let's call the longer diagonal a and the shorter one b. Then a plus b is forty-six. And the gap is "
        "fourteen, so a minus b is fourteen.", show(f3k51a, 'Then a plus b is forty-six'), show(f3k51b, 'so a minus b')),
      L("Both equations are true. So we can add their left sides, and add their right sides. On the left, plus b and minus "
        "b cancel, and a plus a leaves two a. On the right, forty-six plus fourteen is sixty. So two a is sixty.",
        pt('f3k51a', 'Both equations are true'), show(f3k51[0], 'So two a is sixty')),
      L("We want a alone, so we divide both sides by two. A is thirty, and that's the longer diagonal.",
        show(f3k51[1], 'we divide both sides by two')),
      L("Now we put thirty for a in the first equation. Thirty plus b is forty-six. So b is forty-six minus thirty, which is "
        "sixteen.", show(f3k51[2], 'Thirty plus b is forty-six'), show(f3k51[3], 'So b is forty-six minus thirty'))),
    S('Half-diagonals and a triple',
      L("Now the figure. The long diagonal is thirty, and the short one is sixteen. The diagonals of a rhombus cut each "
        "other in half, so we split thirty into fifteen and fifteen, and sixteen into eight and eight. So A O, the top "
        "half of A C, is fifteen, and O D, half of B D, is eight.",
        show(f3g51['line'], 'Now the figure'), show(f3g51['ac'], 'The long diagonal is thirty'),
        show(f3g51['bd'], 'and the short one is sixteen'), show(f3g51['half'], 'so we split thirty')),
      L("We need the perimeter, so we need the side. The diagonals are perpendicular, so each quarter of the rhombus is a "
        "right triangle, with legs eight and fifteen, and the side as its hypotenuse. Here it is, bigger.",
        show(f3g51['q'], 'each quarter of the rhombus'), show(f3g51['cut'], 'Here it is, bigger')),
      L("Eight, fifteen, seventeen is a Pythagorean triple. So the side is seventeen.", show(f3g51['s17'], 'So the side is seventeen')),
      L("All four sides of a rhombus are equal, so the perimeter is four times seventeen, sixty-eight. Choice number two is "
        "our answer. Careful, two hundred forty is thirty times sixteen over two, the area, not the perimeter.",
        show(f3g51['per'], 'four times seventeen'), mk('tick', 'choice 2', 'Choice number two is our answer'),
        mk('cross', 'choice 4', 'Careful, two hundred forty')),
      L("One tip to take from here. Instead of remembering all the rules of a rhombus, remember that it's symmetric, right "
        "equals left and top equals bottom. Then you can always see its angles, its sides and its diagonals. [pause] Okay. "
        "I'll see you in the next question."),
      sb='Half-diagonals and a triple'),
])

# =================================================================================================================
# Topic 32, fragment f4 (2026-10-14): the kite (deltoid) lesson geo-052 and its question geo32-g053, the trapezoid lesson
# geo-054 and its questions geo32-g055 and q-r26-t32-02, and the short lesson geo-056 (Quadrilaterals in Questions).
# Hebrew: geo 2158-2369 (the kite, its sample question, the trapezoid, its sample question) and 2370-2373 (the practice
# intro). Question videos: the question figure on the left (FIG_LEFT), our colour copy in the right column (Rule V3).
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g053', 'solve-geo32-g055', 'solve-q-r26-t32-02'})


def f4_pin(g):
    """layers pinned to their base, so a typed item may come between them (lesson learned in topic 31)"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


def f4_poly(pts, col='ink', w=3):
    return [('seg', pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], col, w) for i in range(len(pts))]


def f4_arc(P, Q, R, r, col, lab=None, lr=None):
    """the arc of the angle at P between rays P->Q and P->R (the side under 180 degrees)"""
    a, b = gdir(P[0], P[1], Q[0], Q[1]), gdir(P[0], P[1], R[0], R[1])
    if (b - a) % 360 > 180: a, b = b, a
    e = ('arc', P[0], P[1], r, a, b, col)
    if lab: e += (lab,) + ((lr,) if lr else ())
    return e


def f4_right(P, Q, R, s=14, col='teal'):
    a, b = gdir(P[0], P[1], Q[0], Q[1]), gdir(P[0], P[1], R[0], R[1])
    if (b - a) % 360 > 180: a, b = b, a
    return ('right', P[0], P[1], a, b, s, col)


def f4_lab(*pts):
    return [('txt', x, y, t, 'ink', 26, True) for x, y, t in pts]


# ------------------------------------------------------------------------------------------------ geo-052 (lesson: The Kite (Deltoid))
# Hebrew (geo 2158-2204): a kite is a rhombus squashed from below or from above; the bottom sides stay equal, the top is
# squashed symmetrically, so right = left; symmetric right-to-left but not top-to-bottom (the top triangle is not the
# bottom one); the diagonals are not equal: the main one (the symmetry line, joining the two angles between equal sides)
# and the secondary one; the main diagonal makes two congruent triangles, the secondary one doesn't; the diagonals are
# perpendicular; the main diagonal bisects the secondary one and the two angles it joins, like the altitude of an isosceles
# triangle; the secondary diagonal doesn't bisect its angles; a kite = two isosceles triangles on the same base (the
# secondary diagonal); the area = the product of the diagonals over two, why: the triangle ADC has base AC and height half
# of BD, times two; "exactly like the rhombus and the square". Added (2-3 examples per idea): a second, wide kite; area
# examples 10 and 6 -> 30, 12 and 8 -> 48; a non-example: two equal sides that face each other make no kite.
# V3: the rhombus dashed, the top pushed down with a dashed arrow, then the kite solid; equal sides ticked as named; the
# fold = the same tint on the left and right halves, then top and bottom tinted in two colours (not equal); the main
# diagonal teal, the secondary orange; the right angle and the equal halves marked at the words; the two isosceles
# triangles tinted in turn; for the area, the triangle ADC tinted and its height (half of BD) traced.
f4kA0, f4kB0, f4kD0, f4kC0 = (240, 60), (150, 195), (330, 195), (240, 330)     # the rhombus (AO = CO = 135, BO = DO = 90)
f4kA1 = (240, 145)                                                             # the squashed top
f4_kw = [(440, 215), (510, 160), (650, 215), (510, 270)]                      # 2026-10-18: a second kite, simple and turned (axis left-right)
f4k1 = GEO('f4k1', [
    ('line', f4_poly([f4kA0, f4kB0, f4kC0, f4kD0], 'ink', 2) + [('seg', 150, 195, 240, 60, 'ink', 2, True)]
             + f4_lab((240, 40, 'A'), (128, 195, 'B'), (240, 356, 'C'), (352, 195, 'D'))),
    ('rh', [('tick', *f4kA0, *f4kB0), ('tick', *f4kA0, *f4kD0), ('tick', *f4kB0, *f4kC0), ('tick', *f4kD0, *f4kC0),
            ('txt', 240, 392, 'a rhombus: four equal sides', 'teal', 22)]),
    ('push', [('dim', 100, 25, 300, 185), ('seg', 240, 70, 240, 130, 'orange', 3, True), ('txt', 268, 100, '↓', 'orange', 30),
              ('seg', *f4kB0, *f4kA1, 'ink', 3.5), ('seg', *f4kD0, *f4kA1, 'ink', 3.5), ('dot', *f4kA1)]),
    ('kite', [('dim', 100, 360, 300, 50), ('seg', *f4kB0, *f4kC0, 'ink', 3.5), ('seg', *f4kD0, *f4kC0, 'ink', 3.5),
              ('tick', *f4kB0, *f4kC0, 2), ('tick', *f4kD0, *f4kC0, 2), ('tick', *f4kA1, *f4kB0), ('tick', *f4kA1, *f4kD0),
              ('txt', 240, 425, 'a kite: two pairs of equal sides', 'orange', 22), ('txt', 240, 125, 'A', 'ink', 26, True)]),
    ('wide', f4_poly(f4_kw, 'ink', 3.5) + [('tick', *f4_kw[0], *f4_kw[1]), ('tick', *f4_kw[0], *f4_kw[3]),
              ('tick', *f4_kw[1], *f4_kw[2], 2), ('tick', *f4_kw[3], *f4_kw[2], 2), ('txt', 545, 310, 'another kite, turned', 'ink', 22)]),
], vb='90 20 580 420', w=820, col=0, title='A rhombus squashed into a kite')
f4_KA, f4_KB, f4_KC, f4_KD, f4_KO = (320, 110), (200, 190), (320, 340), (440, 190), (320, 190)
f4_kl = f4_poly([f4_KA, f4_KB, f4_KC, f4_KD], 'ink', 3.5) + f4_lab((320, 88, 'A'), (176, 190, 'B'), (320, 368, 'C'), (464, 190, 'D')) \
    + [('tick', *f4_KA, *f4_KB), ('tick', *f4_KA, *f4_KD), ('tick', *f4_KB, *f4_KC, 2), ('tick', *f4_KD, *f4_KC, 2)]
f4k2 = GEO('f4k2', [
    ('line', f4_kl),
    ('sym', [('seg', *f4_KA, *f4_KC, 'teal', 3.5, True)]),
    ('lr', [('tint', [f4_KA, f4_KB, f4_KC], 'teal'), ('tint', [f4_KA, f4_KD, f4_KC], 'teal'), ('txt', 320, 405, 'left = right', 'teal', 24)]),
    ('tb', [('dim', 140, 60, 360, 360), ('seg', *f4_KB, *f4_KD, 'orange', 3.5, True), ('tint', [f4_KA, f4_KB, f4_KD], 'teal'),
            ('tint', [f4_KB, f4_KC, f4_KD], 'orange'), ('txt', 520, 150, 'top', 'teal', 24), ('txt', 520, 260, 'bottom', 'orange', 24),
            ('txt', 520, 300, 'here: different', 'red', 24)]),
], vb='130 60 470 360', w=760, col=0, title='A kite is symmetric along its main diagonal')
f4k3 = GEO('f4k3', [
    ('line', f4_kl),
    ('main', [('seg', *f4_KA, *f4_KC, 'teal', 4), ('txt', 320, 394, 'main', 'teal', 22)]),
    ('heads', [f4_arc(f4_KA, f4_KB, f4_KD, 26, 'teal'), f4_arc(f4_KC, f4_KB, f4_KD, 30, 'teal')]),
    ('two', [('tint', [f4_KA, f4_KB, f4_KC], 'teal'), ('tint', [f4_KA, f4_KD, f4_KC], 'teal')]),
    ('sec', [('seg', *f4_KB, *f4_KD, 'orange', 4), ('txt', 530, 192, 'secondary', 'orange', 22)]),
    ('nosym', [('tint', [f4_KA, f4_KB, f4_KD], 'orange'), ('txt', 530, 240, 'here: top ≠ bottom', 'red', 24)]),
], vb='130 60 470 340', w=760, col=0, title='The main and the secondary diagonal')
f4k4 = GEO('f4k4', [
    ('line', f4_kl + [('seg', *f4_KA, *f4_KC, 'teal', 3), ('seg', *f4_KB, *f4_KD, 'orange', 3)]),
    ('perp', [f4_right(f4_KO, f4_KD, f4_KC, 16, 'ink')]),
    ('half', [('tick', *f4_KB, *f4_KO, 3, 'orange'), ('tick', *f4_KO, *f4_KD, 3, 'orange')]),
    ('bisA', [f4_arc(f4_KA, f4_KB, f4_KO, 34, 'teal'), f4_arc(f4_KA, f4_KO, f4_KD, 40, 'teal'),
              f4_arc(f4_KC, f4_KB, f4_KO, 46, 'teal'), f4_arc(f4_KC, f4_KO, f4_KD, 52, 'teal')]),
    ('notB', [f4_arc(f4_KB, f4_KA, f4_KO, 30, 'red'), f4_arc(f4_KB, f4_KO, f4_KC, 40, 'orange'), ('txt', 176, 228, '≠', 'red', 30)]),
    ('iso1', [('tint', [f4_KA, f4_KB, f4_KD], 'teal')]),
    ('iso2', [('tint', [f4_KB, f4_KC, f4_KD], 'orange'), ('txt', 600, 190, 'one shared base: BD', 'ink', 22)]),
], vb='110 60 600 340', w=880, col=0, title='The diagonals of a kite')
f4k5 = GEO('f4k5', [
    ('line', f4_kl + [('seg', *f4_KA, *f4_KC, 'teal', 3), ('seg', *f4_KB, *f4_KD, 'orange', 3)]),
    ('adc', [('tint', [f4_KA, f4_KD, f4_KC], 'teal'), ('txt', 500, 285, 'base AC', 'teal', 22)]),
    ('h', [('seg', *f4_KO, *f4_KD, 'red', 6), ('txt', 378, 218, '½ BD', 'red', 24)]),
    ('abc', [('tint', [f4_KA, f4_KB, f4_KC], 'teal'), ('txt', 210, 280, '× 2', 'teal', 26)]),
], vb='150 60 340 330', w=520, col=0, title='The area of a kite')
f4k5a = IH('f4k5a', '$S=\\frac{AC\\cdot BD}{2}$', size=36)
f4k5h = [IH('f4k5h%d' % i, t, size=30) for i, t in enumerate(['$S_{ADC}=AC\\cdot\\frac{BD}{2}\\div2$', '$2\\cdot S_{ADC}=\\frac{AC\\cdot BD}{2}$'])]
f4k5e = [IH('f4k5e%d' % i, t, size=30) for i, t in enumerate(['$10\\cdot6=60$', '$\\frac{60}{2}=30$', '$12\\cdot8=96$', '$\\frac{96}{2}=48$'])]
for _it, _y in [(f4k5a, 150), (f4k5h[0], 245), (f4k5h[1], 320)] + [(_x, 410 + 66 * _k) for _k, _x in enumerate(f4k5e)]:
    _R(_it, _y, x=1100)
f4k2n = I('f4k2n', 'Each pair: equal sides next to each other', size=26)
_R(f4k2n, 610, x=1000)
for _g in (f4k1, f4k2, f4k3, f4k4, f4k5): f4_pin(_g)
video('geo-052', 'lesson', slides=[
    S('The Kite',
      L("Now the kite. On the exam it's called a deltoid. It looks like a kite you fly, so that's how it got its name.")),
    S('A squashed rhombus',
      L("A kite is really a rhombus that someone squashed a little, from above or from below. Here's a rhombus. All four "
        "of its sides are equal.", show(f4k1['line'], "Here's a rhombus"), show(f4k1['rh'], 'All four')),
      L("Now push its top corner down. The two bottom sides don't move, so they're still equal to each other, just like in "
        "the rhombus. The top was squashed evenly, so its two sides are still equal to each other too.",
        show(f4k1['push'], 'Now push its top corner down'), show(f4k1['kite'], "The two bottom sides don't move")),
      L("So a kite has two pairs of equal sides. In each pair, the equal sides sit next to each other, not facing each "
        "other. In this kite, the two pairs have different lengths. They can also be equal, and then it's a rhombus.",
        pt('f4k1_kite', 'two pairs of equal sides'), show(f4k2n, 'In each pair')),
      L("Here's another kite, turned on its side, and it works the same way.", show(f4k1['wide'], "Here's another kite"))),
    S('Symmetric along A C',
      L("A kite is symmetric along the line that joins the two corners between equal sides, here A and C. If we fold along "
        "A C, the left half lands exactly on the right half. That works even when the kite is turned on the page.",
        show(f4k2['line'], 'A kite is symmetric'), show(f4k2['sym'], 'If we fold along'), show(f4k2['lr'], 'the left half lands')),
      L("Now the other line, from B to D. In this kite, the two pairs have different lengths, so the top triangle and the "
        "bottom triangle are not the same. The top one is small, and the bottom one is big. So a kite is not necessarily "
        "symmetric along B D.", show(f4k2['tb'], 'Now the other line'))),
    S('The two diagonals',
      L("The diagonals of a kite are not necessarily equal. We give them names, the main diagonal and the secondary "
        "diagonal.", show(f4k3['line'], 'The diagonals of a kite')),
      L("The main diagonal is the kite's line of symmetry. It joins the two corners that sit between equal sides, here A "
        "and C. It cuts the kite into two triangles, left and right, that are exactly the same.",
        show(f4k3['main'], 'The main diagonal is'), show(f4k3['heads'], 'It joins the two corners'), show(f4k3['two'], 'It cuts the kite')),
      L("The secondary diagonal, from B to D, does not necessarily cut the kite into two equal parts. In this kite, the "
        "triangle on top and the triangle at the bottom are different.", show(f4k3['sec'], 'The secondary diagonal'),
        show(f4k3['nosym'], 'In this kite, the'))),
    S('Two isosceles triangles',
      L("The diagonals of a kite are perpendicular to each other. And the main diagonal cuts the secondary one into two "
        "equal halves.", show(f4k4['line'], 'The diagonals of a kite'), show(f4k4['perp'], 'perpendicular to each other'),
        show(f4k4['half'], 'into two equal halves')),
      L("It's just like in an isosceles triangle, where the altitude to the base is also the median and the angle "
        "bisector. So the main diagonal also cuts the corners A and C into two equal angles.", show(f4k4['bisA'], 'So the main diagonal also cuts')),
      L("The secondary diagonal does not necessarily do that. In this kite, at B, the angle above it and the angle below it "
        "are not equal.", show(f4k4['notB'], 'at B, the angle above it')),
      L("Really, a kite is made of two isosceles triangles, one on top, and one at the bottom, upside down. And both of "
        "them stand on the same base, the secondary diagonal B D.", show(f4k4['iso1'], 'one on top'), show(f4k4['iso2'], 'and one at the bottom'))),
    S('The area',
      L("The area of a kite is the product of the diagonals, over two. That's exactly like the rhombus and the square.",
        show(f4k5a, 'The area of a kite')),
      L("Why? The diagonals are perpendicular. Take the triangle A D C, the right half of the kite. Its base is the main "
        "diagonal, A C. Its height is the distance from D to that base, and that's half of the secondary diagonal.",
        show(f4k5['line'], 'Why? The diagonals'), show(f4k5['adc'], 'Take the triangle A D C'), show(f4k5['h'], 'Its height is the distance')),
      L("So its area is A C, times half of B D, over two. The left half is exactly the same triangle, so we multiply by "
        "two, and we're left with A C times B D, over two.", show(f4k5h[0], 'So its area is A C'),
        show(f4k5['abc'], 'The left half is exactly'), show(f4k5h[1], "we're left with")),
      L("For example, if the diagonals are ten and six, ten times six is sixty, and sixty over two is thirty.",
        show(f4k5e[0], 'ten times six is sixty'), show(f4k5e[1], 'sixty over two')),
      L("If they're twelve and eight, twelve times eight is ninety-six, and ninety-six over two is forty-eight. Next, let's "
        "see a question about a kite. [pause] Okay. I'll see you in the next video.", show(f4k5e[2], 'twelve times eight'),
        show(f4k5e[3], 'ninety-six over two'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g053 (Hebrew: the kite's sample question)
# Hebrew (geo 2207-2243): triangle BDC is isosceles (the kite's equal sides) with a 60 -> equilateral, BD = the given side;
# at the top 45 -> ADB = 45 (isosceles) -> A = 90: the silver triangle; hypotenuse to leg: divide by root 2 ("ignore the
# root, divide, attach the root"); the perimeter: 4 + 4 = 8, only one choice starts with 8 -> mark it; the root-2 tip
# (silver -> root 2, gold -> root 3); "if I add it all to the end"; the close: a kite is symmetric right to left only.
# English: 10 instead of 4; two choices start with 20, so the root-2 tip settles it.
# V3: the colour copy; BDC tinted with its two equal sides ticked and the 60 marked, then the other two 60s and BD = 10
# written; ABD tinted, the 45s and the right angle at A, the hypotenuse BD traced, 5 root 2 written on both legs; the outer
# path traced for the perimeter.
f4gA, f4gB, f4gC, f4gD = (320.0, 62.638), (234.085, 148.553), (320.0, 297.362), (405.915, 148.553)
f4_53base = f4_poly([f4gA, f4gB, f4gC, f4gD], 'ink', 2.5) + [('seg', *f4gB, *f4gD, 'ink', 2.5)] \
    + [('txt', 320, 42, 'A', 'ink', 22, True), ('txt', 212, 148, 'B', 'ink', 22, True), ('txt', 320, 320, 'C', 'ink', 22, True),
       ('txt', 428, 148, 'D', 'ink', 22, True)]
f4_53bdc = [('tint', [f4gB, f4gC, f4gD], 'teal'), ('tick', *f4gB, *f4gC, 2), ('tick', *f4gD, *f4gC, 2),
            ('txt', 252, 232, '10', 'teal', 22), ('txt', 388, 232, '10', 'teal', 22), f4_arc(f4gB, f4gD, f4gC, 24, 'teal', '60°', 46)]
f4_53eq = [f4_arc(f4gD, f4gB, f4gC, 24, 'teal', '60°', 46), f4_arc(f4gC, f4gB, f4gD, 26, 'teal', '60°', 48), ('txt', 320, 197, 'BD = 10', 'teal', 22)]
f4_53top = [('tint', [f4gA, f4gB, f4gD], 'orange'), f4_arc(f4gB, f4gA, f4gD, 24, 'orange', '45°', 46),
            f4_arc(f4gD, f4gA, f4gB, 24, 'orange', '45°', 46), f4_right(f4gA, f4gB, f4gD, 14, 'orange'),
            ('txt', 240, 92, '5√2', 'orange', 22), ('txt', 400, 92, '5√2', 'orange', 22)]
_f4_53vb = dict(vb='190 25 260 310', w=300)
f4g53 = GEO('f4g53', [
    ('line', f4_53base),
    ('bdc', f4_53bdc),
    ('eq', f4_53eq[:2]),
    ('bd', f4_53eq[2:]),
], title='Kite ABCD made of two special triangles', **_f4_53vb)
f4g53s = GEO('f4g53s', [
    ('line', f4_53base + f4_53bdc + f4_53eq),
    ('abd', f4_53top[:2]),
    ('d45', f4_53top[2:3]),
    ('a90', f4_53top[3:4]),
    ('hyp', [('seg', *f4gB, *f4gD, 'red', 5)]),
    ('legs', f4_53top[4:]),
], title='Kite ABCD: the top triangle', **_f4_53vb)
f4g53p = GEO('f4g53p', [
    ('line', f4_53base + f4_53bdc + f4_53eq + f4_53top),
    ('per', [('path', [f4gA, f4gB, f4gC, f4gD, f4gA], 'red', 7)]),
], title='Kite ABCD: the perimeter', **_f4_53vb)
f4g53r = [IH('f4g53r%d' % i, t, size=30) for i, t in enumerate(['$\\frac{10}{\\sqrt2}$', '$=\\frac{10}{2}\\cdot\\sqrt2$', '$=5\\sqrt2$'])]
f4g53t2 = IH('f4g53t2', '$10+10=20$', size=32)
f4g53t4 = IH('f4g53t4', '$P=20+10\\sqrt2$', size=26)
f4g53t3 = I('f4g53t3', '$5\\sqrt2+5\\sqrt2$', size=26)
f4g53t3b = I('f4g53t3b', 'only a $\\sqrt2$ part', size=24)
for _g in (f4g53, f4g53s, f4g53p): f4_pin(_g); _R(_g, 180)
for _it, _y in [(f4g53r[0], 220), (f4g53r[1], 290), (f4g53r[2], 360), (f4g53t2, 230), (f4g53t3, 290), (f4g53t3b, 345), (f4g53t4, 400)]:
    _R(_it, _y, x=1355)
video('solve-geo32-g053', 'solution', qid='geo32-g053', slides=[
    S('Two special triangles',
      L("A B C D is a deltoid. Given: A B is equal to A D, C B and C D are both ten centimeters, angle A B D is forty-five "
        "degrees, and angle D B C is sixty degrees. What is the perimeter of the deltoid, in centimeters?",
        pt('stem', 'A B C D is a deltoid', 'hl', 11.0), voice='calm', pause=0.5),
      L("For the perimeter we need all four sides. We know two of them, the tens. The line B D cuts the kite into two "
        "triangles, so let's look at them one at a time. [short pause] We'll start with the bottom one.",
        pt('fig: 10', 'We know two of them')),
      L("[short pause] Triangle B D C. In a kite, the two bottom sides are equal, so C B is ten and C D is ten. That makes "
        "the triangle isosceles, and it also has a sixty-degree angle at B.", show(f4g53['line'], 'Triangle B D C'),
        show(f4g53['bdc'], 'the two bottom sides are equal')),
      L("An isosceles triangle with a sixty-degree angle must be equilateral. The angle at D equals the angle at B, because they sit across from the equal sides. So it's "
        "sixty too, and then the angle at C is one hundred eighty minus one hundred twenty, which is sixty. Sixty, sixty, "
        "sixty. So all its sides are equal, and B D is ten as well.", show(f4g53['eq'], 'The angle at D equals'),
        show(f4g53['bd'], 'and B D is ten as well'))),
    S('The silver triangle',
      L("Now the top triangle, A B D. Its angle at B is forty-five. A B equals A D, so it's isosceles, and the angle at D is "
        "forty-five too. What's left for A is ninety.", show(f4g53s['line'], 'Now the top triangle'), show(f4g53s['abd'], 'Its angle at B'), show(f4g53s['d45'], 'and the angle at D'),
        show(f4g53s['a90'], "What's left for A")),
      L("Forty-five, forty-five, ninety. That's our silver triangle. Its hypotenuse is B D, ten. To get from the hypotenuse "
        "to a leg, we divide by root two.", show(f4g53s['hyp'], 'Its hypotenuse is B D'), show(f4g53r[0], 'we divide by root two')),
      L("Remember the shortcut. To divide ten by root two, we divide ten by two, and then multiply by root two. Ten over "
        "two is five, so each leg is five root two. So A B and A D are both five root two.",
        show(f4g53r[1], 'we divide ten by two'), show(f4g53r[2], 'so each leg is five root two'), show(f4g53s['legs'], 'So A B and A D'))),
    S('Use the choices',
      L("Now the perimeter. The two tens give twenty. The other two sides are both five root two, so together they add a "
        "root two part, and no root three. So the perimeter is twenty plus some root two.",
        show(f4g53p['line'], 'Now the perimeter'), show(f4g53p['per'], 'Now the perimeter'), show(f4g53t2, 'The two tens give twenty'),
        show(f4g53t3, 'The other two sides are both'), show(f4g53t3b, 'so together they add')),
      L("Now look at the choices. Choice numbers two and four start with ten, not twenty, so they're out. Choice number "
        "one has root three, so it's out too. Only choice number three has twenty plus a root two part.",
        mk('cross', 'choice 2', 'Choice numbers two and four'), mk('cross', 'choice 4', "start with ten, not twenty"),
        mk('cross', 'choice 1', 'one has root three')),
      L("And if we add it all up, twenty plus five root two plus five root two is twenty plus ten root two. Choice "
        "number three is our answer.", show(f4g53t4, 'And if we add it all'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("So in a kite, the main diagonal, here A C, is always a line of symmetry. The other diagonal, B D, doesn't have to "
        "be one, and here it isn't. [pause] Okay. I'll see you in the next question.", pt('f4g53p_line', 'So in a kite'))),
])

# ------------------------------------------------------------------------------------------------ geo-054 (lesson: The Trapezoid)
# Hebrew (geo 2247-2311): four sides; the bottom and top sides are the bases, the sides are the legs; the bases are
# parallel (not equal), the legs are not parallel (else a parallelogram); two angles on the same leg add up to 180 (small +
# large, parallel lines and a transversal); the area = (a + b) h / 2, why: copy, flip, attach -> a parallelogram with base
# a + b, the trapezoid is half of it; "in the exam you won't prove formulas, memorize"; the isosceles trapezoid (equal legs,
# equal base angles beta = beta, so alpha = alpha; symmetric like an isosceles triangle, the legs continued close into an
# isosceles triangle; the diagonals are equal and cut each other into matching pieces); the right trapezoid (two right
# angles, never only one, because the bases are parallel). Kept from the English lesson: opposite angles of an isosceles
# trapezoid add up to 180; in questions, drop the height from D (a rectangle and a right triangle, Pythagoras).
# Added examples: 70 -> 110 on a leg; areas (10 + 6) 4 / 2 = 32 and (9 + 3) 5 / 2 = 30; a base angle 65 -> 65, 115, 115.
# V3: a general trapezoid built part by part (bases traced teal with parallel arrows, legs orange); a non-example (legs
# parallel -> a parallelogram) drawn small and red; the U of topic 30 traced on a leg; the area: the height dashed, then the
# flipped copy tinted orange next to it, the long base a + b written; the isosceles trapezoid: equal legs ticked, the base
# angles, the symmetry line, the legs continued dashed up to the top, the diagonals with their matching pieces ticked; the
# right trapezoid: the right angles, then the height from D dashed, the rectangle and the right triangle tinted.
f4tB, f4tC, f4tA, f4tD = (150, 290), (560, 290), (222.8, 90), (420, 90)
f4_tl = f4_poly([f4tA, f4tB, f4tC, f4tD], 'ink', 3.5) + f4_lab((222.8, 66, 'A'), (128, 300, 'B'), (582, 300, 'C'), (420, 66, 'D'))
f4t1 = GEO('f4t1', [
    ('line', f4_tl),
    ('bases', [('path', [f4tB, f4tC], 'teal', 7), ('path', [f4tA, f4tD], 'teal', 7), ('par', *f4tB, *f4tC), ('par', *f4tA, *f4tD),
               ('txt', 355, 322, 'base', 'teal', 22), ('txt', 321, 66, 'base', 'teal', 22)]),
    ('legs', [('path', [f4tA, f4tB], 'orange', 7), ('path', [f4tD, f4tC], 'orange', 7), ('txt', 155, 180, 'leg', 'orange', 22),
              ('txt', 520, 180, 'leg', 'orange', 22)]),
    ('non', f4_poly([(660, 150), (630, 250), (760, 250), (790, 150)], 'red', 3) + [('par', 630, 250, 660, 150, 1, 'red'),
             ('par', 760, 250, 790, 150, 1, 'red'), ('txt', 710, 285, 'legs parallel:', 'red', 20), ('txt', 710, 310, 'a parallelogram', 'red', 20)]),
], vb='100 40 720 300', w=1040, col=0, title='A trapezoid: two bases and two legs')
f4t2 = GEO('f4t2', [
    ('line', f4_tl + [('par', *f4tB, *f4tC), ('par', *f4tA, *f4tD)]),
    ('u', [('path', [f4tD, f4tA, f4tB, f4tC], 'orange', 7)]),
    ('b', [f4_arc(f4tB, f4tC, f4tA, 32, 'small', '70°', 56)]),
    ('a', [f4_arc(f4tA, f4tB, f4tD, 28, 'large', '110°', 54)]),
    ('cd', [f4_arc(f4tC, f4tD, f4tB, 32, 'small', 'small', 60), f4_arc(f4tD, f4tA, f4tC, 28, 'large', 'large', 56)]),
], vb='100 40 520 300', w=620, col=0, title='Two angles on one leg')
f4t2a = IH('f4t2a', '$180°-70°=110°$', size=32)
_R(f4t2a, 320, x=1180)
f4qB, f4qC, f4qA, f4qD = (60, 290), (300, 290), (110, 130), (220, 130)
f4qA2, f4qB2 = (410, 290), (460, 130)
f4t3 = GEO('f4t3', [
    ('line', f4_poly([f4qA, f4qB, f4qC, f4qD], 'ink', 3.5) + [('txt', 180, 318, 'a', 'teal', 26, True), ('txt', 165, 112, 'b', 'teal', 26, True)]),
    ('h', [('dot', *f4qA), ('seg', 110, 130, 110, 290, 'teal', 3, True), ('right', 110, 290, 0, 90, 12), ('txt', 94, 210, 'h', 'teal', 26, True)]),
    ('copy', [('tint', [f4qA, f4qB, f4qC, f4qD], 'teal'), ('tint', [f4qD, f4qC, f4qA2, f4qB2], 'orange')] + f4_poly([f4qD, f4qC, f4qA2, f4qB2], 'orange', 3.5)
             + [('txt', 355, 318, 'b', 'orange', 26, True), ('txt', 340, 112, 'a', 'orange', 26, True)]),
    ('base', [('seg', 60, 350, 410, 350, 'ink', 3), ('seg', 60, 340, 60, 360, 'ink', 3), ('seg', 410, 340, 410, 360, 'ink', 3),
              ('txt', 235, 378, 'a + b', 'ink', 26)]),
], vb='40 90 440 310', w=560, col=0, title='Two copies of a trapezoid make a parallelogram')
f4t3a = IH('f4t3a', '$S=\\frac{(a+b)\\cdot h}{2}$', size=36)
# 2026-10-18 (batch C #225): each example its own column, one step per row at its clause
f4t3e1 = [IH('f4t3e1%d' % i, t, size=28) for i, t in enumerate(['$\\frac{(10+6)\\cdot4}{2}$', '$10+6=16$', '$16\\cdot4=64$', '$\\frac{64}{2}=32$'])]
f4t3e2 = [IH('f4t3e2%d' % i, t, size=28) for i, t in enumerate(['$\\frac{(9+3)\\cdot5}{2}$', '$9+3=12$', '$12\\cdot5=60$', '$\\frac{60}{2}=30$'])]
_R(f4t3a, 140, x=1000)
for _k, _x in enumerate(f4t3e1 + f4t3e2): _R(_x, 230 + 58 * _k, x=1000)
f4iA, f4iD, f4iB, f4iC, f4iO, f4iT = (260, 140), (380, 140), (140, 300), (500, 300), (320, 180), (320, 60)
f4t4 = GEO('f4t4', [
    ('line', f4_poly([f4iA, f4iB, f4iC, f4iD], 'ink', 3.5) + f4_lab((250, 122, 'A'), (120, 310, 'B'), (520, 310, 'C'), (390, 122, 'D'))),
    ('legs', [('tick', *f4iA, *f4iB), ('tick', *f4iD, *f4iC)]),
    ('beta', [f4_arc(f4iB, f4iC, f4iA, 30, 'small', 'β', 52), f4_arc(f4iC, f4iD, f4iB, 30, 'small', 'β', 52)]),
    ('alpha', [f4_arc(f4iA, f4iB, f4iD, 26, 'large', 'α', 48), f4_arc(f4iD, f4iA, f4iC, 26, 'large', 'α', 48)]),
    ('sym', [('seg', 320, 125, 320, 315, 'teal', 3, True)]),
    ('top', [('seg', *f4iA, *f4iT, 'ink', 2.5, True), ('seg', *f4iD, *f4iT, 'ink', 2.5, True), ('tint', [f4iT, f4iB, f4iC], 'teal')]),
    ('diag', [('dim', 100, 40, 440, 290)] + f4_poly([f4iA, f4iB, f4iC, f4iD], 'ink', 3) + [('seg', *f4iA, *f4iC, 'orange', 4), ('seg', *f4iB, *f4iD, 'orange', 4),
              ('tick', *f4iA, *f4iO, 2, 'orange'), ('tick', *f4iD, *f4iO, 2, 'orange'), ('tick', *f4iO, *f4iC, 3, 'orange'),
              ('tick', *f4iO, *f4iB, 3, 'orange')]),
], vb='100 40 440 290', w=600, col=0, title='An isosceles trapezoid')
f4t4a = IH('f4t4a', '$65°,\\ 65°,\\ 115°,\\ 115°$', size=32)
f4t4b = I('f4t4b', 'Isosceles: opposite angles $\\ \\alpha+\\beta=180°$', size=28)
for _it, _y in [(f4t4a, 220), (f4t4b, 320)]:
    _R(_it, _y, x=1010)
f4rA, f4rD, f4rB, f4rC, f4rE = (180, 110), (360, 110), (180, 300), (520, 300), (360, 300)
f4t5 = GEO('f4t5', [
    ('line', f4_poly([f4rA, f4rB, f4rC, f4rD], 'ink', 3.5) + f4_lab((160, 96, 'A'), (160, 314, 'B'), (540, 314, 'C'), (370, 92, 'D'))),
    ('rB', [('right', 180, 300, 0, 90, 16)]),
    ('rA', [('right', 180, 110, 270, 360, 16), ('path', [f4rD, f4rA, f4rB, f4rC], 'orange', 6)]),
    ('h', [('dot', *f4rD), ('seg', *f4rD, *f4rE, 'teal', 3, True), ('right', 360, 300, 0, 90, 14), ('txt', 362, 326, 'E', 'ink', 26, True)]),
    ('parts', [('tint', [f4rA, f4rB, f4rE, f4rD], 'teal'), ('tint', [f4rD, f4rE, f4rC], 'orange'), ('txt', 270, 210, 'rectangle', 'teal', 22),
               ('txt', 400, 258, 'right', 'orange', 18), ('txt', 400, 280, 'triangle', 'orange', 18)]),
], vb='120 70 460 270', w=700, col=0, title='A right trapezoid')
for _g in (f4t1, f4t2, f4t3, f4t4, f4t5): f4_pin(_g)
video('geo-054', 'lesson', slides=[
    S('The Trapezoid',
      L("And the last quadrilateral, the trapezoid.")),
    S('Bases and legs',
      L("A trapezoid has four sides. Two of them are parallel, and those two are called the bases. Here they're A D and B "
        "C. The other two sides, A B and C D, are called the legs.", show(f4t1['line'], 'A trapezoid has four sides'),
        show(f4t1['bases'], 'are called the bases'), show(f4t1['legs'], 'are called the legs')),
      L("The bases are parallel to each other, but they're not equal. The legs are not parallel. If they "
        "were parallel too, it wouldn't be a trapezoid anymore. It would be a parallelogram.", pt('f4t1_bases', 'The bases are parallel'),
        show(f4t1['non'], 'If they were parallel too')),
      L("So a trapezoid has exactly one pair of parallel sides, the bases.", pt('f4t1_bases', 'exactly one pair'))),
    S('Two angles on a leg',
      L("Two angles that sit on the same leg add up to one hundred eighty. Look at the leg A B. The bases are two parallel "
        "lines, and the leg cuts both of them. It's the U from lines and angles, a small angle plus a large angle, one "
        "hundred eighty.", show(f4t2['line'], 'Two angles that sit'), show(f4t2['u'], "It's the U from lines")),
      L("For example, if the angle at B is seventy, then the angle at A is one hundred eighty minus seventy, which is one "
        "hundred ten.", show(f4t2['b'], 'if the angle at B is seventy'), show(f4t2['a'], 'then the angle at A'), show(f4t2a, 'which is one hundred ten')),
      L("The same is true on the other leg, C D. A small angle at C plus a large angle at D make one hundred eighty.",
        show(f4t2['cd'], 'The same is true'))),
    S('The area',
      L("Let's call the bases a and b, and the height h. The height is the distance between the two bases, so it's "
        "perpendicular to them.", show(f4t3['line'], "Let's call the bases"), show(f4t3['h'], 'and the height h')),
      L("The area of a trapezoid is the sum of the bases, times the height, over two.", show(f4t3a, 'The area of a trapezoid')),
      L("Why? Here's a simple way to see it. Make a copy of the trapezoid, turn it upside down, and attach it on the "
        "right. The two trapezoids together make one big parallelogram.", show(f4t3['copy'], 'Make a copy')),
      L("The base of this parallelogram is a plus b, and its height is h. The area of every parallelogram is its base times "
        "its height, so a plus b, times h. Our trapezoid is only half of it, so it's a plus b, times h, over two.",
        show(f4t3['base'], 'The base of this parallelogram')),
      L("In the exam you won't prove formulas, so what matters is to remember it. For example, bases ten and six, and "
        "height four. Ten plus six is sixteen. Sixteen times four is sixty-four. And sixty-four over two is thirty-two.",
        show(f4t3e1[0], 'For example, bases ten and six'), show(f4t3e1[1], 'Ten plus six is'), show(f4t3e1[2], 'Sixteen times four'),
        show(f4t3e1[3], 'sixty-four over two')),
      L("Another one, bases nine and three, height five. Nine plus three is twelve. Twelve times five is sixty. And sixty "
        "over two is thirty.", show(f4t3e2[0], 'Another one, bases nine'), show(f4t3e2[1], 'Nine plus three is'),
        show(f4t3e2[2], 'Twelve times five'), show(f4t3e2[3], 'sixty over two'))),
    S('The isosceles trapezoid',
      L("An isosceles trapezoid is a trapezoid whose legs are equal, just like its name says. The left side equals the "
        "right side.", show(f4t4['line'], 'An isosceles trapezoid'), show(f4t4['legs'], 'whose legs are equal')),
      L("Its two base angles at the bottom are equal, beta and beta. Each leg's two angles add up to one hundred eighty, so "
        "the top angles are equal too, alpha and alpha.", show(f4t4['beta'], 'Its two base angles'), show(f4t4['alpha'], 'so the top angles')),
      L("It's symmetric from right to left, a bit like an isosceles triangle. In fact, if we continued the legs up, they "
        "would close into an isosceles triangle.", show(f4t4['sym'], "It's symmetric from right"), show(f4t4['top'], 'if we continued the legs up')),
      L("For example, if a base angle is sixty-five, the other base angle is sixty-five too, and each top angle is one "
        "hundred eighty minus sixty-five, which is one hundred fifteen.", show(f4t4a, 'if a base angle is sixty-five')),
      L("Its diagonals are equal too. And they cut each other into matching pieces. The two top pieces are equal to each "
        "other, and the two bottom pieces are equal to each other. But the top pieces need not equal the bottom pieces, so "
        "the diagonals are not generally cut in half.", show(f4t4['diag'], 'Its diagonals are equal too')),
      L("And in an isosceles trapezoid, alpha plus beta is one hundred eighty, so opposite angles, like A and C, also add up "
        "to one hundred eighty. That's useful in angle questions.", show(f4t4b, 'opposite angles, like A and C'))),
    S('The right trapezoid',
      L("A right trapezoid is simply a trapezoid with right angles. It always has two of them, never just one.",
        show(f4t5['line'], 'A right trapezoid'), show(f4t5['rB'], 'with right angles')),
      L("Why? If the angle at B is ninety, then the angle at A, on the same leg, is one hundred eighty minus ninety, which "
        "is ninety too.", show(f4t5['rA'], 'then the angle at A')),
      L("In questions, it helps to drop a height from D to the bottom base. Then the trapezoid splits into a rectangle and "
        "a right triangle, and Pythagoras does the rest.", show(f4t5['h'], 'drop a height from D'), show(f4t5['parts'], 'splits into a rectangle')),
      L("So we've seen a general trapezoid, the isosceles trapezoid, which is symmetric, and the right trapezoid, with its "
        "two right angles. Next, let's see a question. [pause] Okay. I'll see you in the next video.",
        pt('f4t5_parts', 'the right trapezoid, with its'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g055 (Hebrew: the trapezoid's sample question)
# Hebrew (geo 2314-2367): EC from the area of triangle DEC (legs times legs over 2); the tip for every trapezoid question:
# drop the heights, both of them; symmetric, so BF = EC; FE = AD = x; the common mistake: the middle is NOT a square (the
# drawing isn't accurate), it's a rectangle; the left triangle has the same area; the middle rectangle = the trapezoid
# minus the two triangles; length times width -> x; then the long way with the trapezoid formula, same answer, "much
# longer"; we saved it by understanding the symmetry. English: area 65, DE = 5, triangle 10 -> EC = 4, x = 9.
# V3: the colour copy; DEC tinted and its 10 written, EC = 4 written; the second height from A dashed (A pointed first);
# ABF tinted the same, BF = 4 and 10 written; the middle rectangle tinted orange with x on AD and FE, a red "not a
# square" note; 45 written in it; method 2 on a new slide: the bases labelled x and 4 + x + 4.
f4eA, f4eB, f4eC, f4eD, f4eE, f4eF = (192.25, 70.5), (119.25, 289.5), (520.75, 289.5), (447.75, 70.5), (447.75, 289.5), (192.25, 289.5)
f4_el = f4_poly([f4eA, f4eB, f4eC, f4eD], 'ink', 2.5) + [('seg', *f4eD, *f4eE, 'ink', 2.5), ('right', 447.75, 289.5, 0, 90, 14, 'ink')] \
    + [('txt', 178, 52, 'A', 'ink', 24, True), ('txt', 102, 306, 'B', 'ink', 24, True), ('txt', 538, 306, 'C', 'ink', 24, True),
       ('txt', 462, 52, 'D', 'ink', 24, True), ('txt', 447.75, 314, 'E', 'ink', 24, True), ('txt', 432, 180, '5', 'ink', 24)]
# 2026-10-18 (batch C #226): Understanding needs only the two equal AREAS (10 and 10); the lengths EC = BF = 4 belong to the
# math way, where the formula needs the bottom base
f4_55dec = [('tint', [f4eD, f4eE, f4eC], 'teal'), ('txt', 478, 255, '10', 'teal', 24)]
f4_55af = [('seg', *f4eA, *f4eF, 'teal', 3, True), ('right', 192.25, 289.5, 90, 180, 14), ('txt', 192.25, 314, 'F', 'ink', 24, True),
           ('tint', [f4eA, f4eB, f4eF], 'teal'), ('txt', 166, 255, '10', 'teal', 24)]
f4g55 = GEO('f4g55', [
    ('line', f4_el),
    ('af', [('dot', *f4eA)] + f4_55af[:3]),
    ('dec', f4_55dec),
    ('abf', f4_55af[3:]),
], vb='80 25 480 320', w=300, title='Isosceles trapezoid ABCD with both heights')
f4g55m = GEO('f4g55m', [
    ('line', f4_el + f4_55dec + f4_55af),
    ('mid', [('tint', [f4eA, f4eF, f4eE, f4eD], 'orange'), ('txt', 320, 52, 'x', 'orange', 26, True), ('txt', 320, 312, 'x', 'orange', 26, True)]),
    ('nsq', [('txt', 320, 140, 'not a square!', 'red', 24)]),
    ('v45', [('txt', 320, 200, '45', 'orange', 34)]),
    ('v9', [('txt', 352, 52, '= 9', 'red', 26)]),
], vb='80 25 480 320', w=300, title='The middle rectangle AFED')
f4g55b = GEO('f4g55b', [
    ('line', f4_el + [('seg', *f4eA, *f4eF, 'teal', 3, True), ('right', 192.25, 289.5, 90, 180, 14), ('txt', 192.25, 314, 'F', 'ink', 24, True),
              ('txt', 320, 52, 'x', 'orange', 26, True)]),
    ('dec', [('tint', [f4eD, f4eE, f4eC], 'teal'), ('txt', 478, 255, '10', 'teal', 24)]),
    ('ec', [('txt', 484, 334, '4', 'teal', 26)]),
    ('bf', [('tint', [f4eA, f4eB, f4eF], 'teal'), ('txt', 156, 334, '4', 'teal', 26)]),
    ('fe', [('txt', 320, 334, 'x', 'orange', 26, True)]),
    ('bc', [('path', [f4eB, f4eC], 'orange', 7)]),
], vb='80 25 480 342', w=300, title='The bases: x and x + 8')
f4g55b2 = GEO('f4g55b2', [
    ('line', f4_el + [('seg', *f4eA, *f4eF, 'teal', 3, True), ('txt', 320, 52, 'x', 'orange', 26, True), ('txt', 156, 334, '4', 'teal', 24),
              ('txt', 320, 334, 'x', 'orange', 24), ('txt', 484, 334, '4', 'teal', 24), ('path', [f4eB, f4eC], 'orange', 7)]),
], vb='80 25 480 342', w=300, title='The bases: x and x + 8')
f4g55a = [IH('f4g55a%d' % i, t, size=28) for i, t in enumerate(['$\\frac{5\\cdot EC}{2}=10$', '$5\\cdot EC=20,\\ EC=4$'])]
f4g55c = [IH('f4g55c%d' % i, t, size=26) for i, t in enumerate(['$10+10=20$', '$65-20=45$'])]
f4g55d = [IH('f4g55d%d' % i, t, size=26) for i, t in enumerate(['$5x=45$', '$x=\\frac{45}{5}=9$'])]
f4g55e = IH('f4g55e', '$\\frac{(x+x+8)\\cdot5}{2}=65$', size=26)
f4g55f = IH('f4g55f', '$(2x+8)\\cdot5=130$', size=26)
f4g55g = [IH('f4g55g%d' % i, t, size=26) for i, t in enumerate(['$10x+40=130$', '$10x=90$', '$x=\\frac{90}{10}=9$'])]
for _g in (f4g55, f4g55m, f4g55b): f4_pin(_g); _R(_g, 190)
f4_pin(f4g55b2); _R(f4g55b2, 190)
f4g55a = [IH('f4g55a%d' % i, t, size=26) for i, t in enumerate(['$\\frac{5\\cdot EC}{2}=10$', '$5\\cdot EC=20$', '$EC=4$'])]
for _rows in (f4g55c + f4g55d, f4g55a, [f4g55e, f4g55f] + f4g55g):
    for _k, _x in enumerate(_rows): _R(_x, 200 + 56 * _k, x=1350)
video('solve-geo32-g055', 'solution', qid='geo32-g055', slides=[
    SM('Method 1 · Understanding: symmetry', 'Drop both heights',
      L("The area of isosceles trapezoid A B C D is sixty-five square centimeters. D E is an altitude, D E is five "
        "centimeters, and the area of triangle D E C is ten square centimeters. What is A D, in centimeters?",
        pt('stem', 'The area of isosceles trapezoid', 'hl', 10.0), voice='calm', pause=0.5),
      L("A D is the short base at the top. [short pause] We'll solve it in two different ways. First by understanding, "
        "using the symmetry, and then the math way, with the trapezoid area formula.", pt('fig: A', 'A D is the short base')),
      L("[short pause] Let's start with understanding. One height, D E, is given. Here a second height lets us compare the "
        "two end triangles, so we drop it from A down to the base. Call its foot F. In general, heights often split a "
        "trapezoid into a rectangle and right triangles.", show(f4g55['line'], "Let's start with understanding"),
        show(f4g55['af'], 'so we drop it from A')),
      L("The trapezoid is isosceles, so it's symmetric, right equals left. The triangle D E C on the right has area ten. "
        "So the triangle A B F on the left matches it, and also has area ten.", show(f4g55['dec'], 'The triangle D E C on the right'),
        show(f4g55['abf'], 'So the triangle A B F'))),
    SM('Method 1 · Understanding: symmetry', 'Not a square',
      L("The middle part, A F E D, is a rectangle. Its top is A D, and its bottom, F E, is the same length. Let's call it "
        "x.", show(f4g55m['line'], 'The middle part'), show(f4g55m['mid'], 'The middle part')),
      L("Careful, here's a common mistake. In the drawing it looks like a square, but drawings on the exam don't have to "
        "be accurate. We don't know that x equals five. It's a rectangle.", show(f4g55m['nsq'], "In the drawing it looks like a square")),
      L("The whole trapezoid is sixty-five, and the two triangles are ten each. Ten plus ten is twenty. So what's left in "
        "the middle is sixty-five minus twenty, which is forty-five.", show(f4g55c[0], 'Ten plus ten is twenty'),
        show(f4g55c[1], "So what's left in the middle"), show(f4g55m['v45'], 'which is forty-five')),
      L("The area of a rectangle is length times width. Its height is D E, five, and its area is forty-five. So five times "
        "x is forty-five. We divide both sides by five, so x is nine. A D is nine, and choice number two is our answer.",
        show(f4g55d[0], 'So five times x is forty-five'), show(f4g55d[1], 'We divide both sides by five'), show(f4g55m['v9'], 'A D is nine'),
        mk('tick', 'choice 2', 'choice number two is our answer'))),
    SM('Method 2 · The math way: the area formula', 'The bases',
      L("[pause] Now the math way, with the trapezoid area formula. Again we call A D x, and we use the two heights, D E and "
        "A F. For the formula, we need the bottom base too.", show(f4g55b['line'], 'Now the math way')),
      L("Start with the small triangle D E C. It's a right triangle, so its area is one leg times the other, over two. Its "
        "legs are D E, which is five, and E C. Five times E C, over two, equals ten. So five times E C is twenty, and E C "
        "is four.", show(f4g55b['dec'], 'Start with the small triangle'), show(f4g55a[0], 'Five times E C, over two'),
        show(f4g55a[1], 'So five times E C is twenty'), show(f4g55a[2], 'and E C is four'), show(f4g55b['ec'], 'is four.')),
      L("The two end triangles match because the trapezoid is isosceles, so B F is four too. And F E is the bottom of the "
        "rectangle, so it's x.", show(f4g55b['bf'], 'so B F is four too'), show(f4g55b['fe'], 'so it\'s x')),
      L("So the top base is x. The bottom base is four plus x plus four, which is x plus eight.",
        show(f4g55b['bc'], 'The bottom base is four'))),
    SM('Method 2 · The math way: the area formula', 'The formula',
      L("The area formula says the sum of the bases, times the height, over two. The sum of the bases is x plus x plus "
        "eight, which is two x plus eight. We multiply that sum by five, divide by two, and we get sixty-five.",
        show(f4g55b2['line'], 'The area formula says'), show(f4g55e, 'We multiply that sum by five')),
      L("Multiply both sides by two, to get rid of the over two. So two x plus eight, multiplied by five, gives one hundred "
        "thirty.",
        show(f4g55f, 'Multiply both sides by two')),
      L("Five times two x is ten x. And five times eight is forty. So ten x plus forty is one hundred thirty.",
        show(f4g55g[0], 'So ten x plus forty')),
      L("Take forty away from both sides, so ten x is ninety. Now divide both sides by ten, and x is nine. Choice number "
        "two again. [pause] Okay. I'll see you in the next question.", show(f4g55g[1], 'Take forty away'),
        show(f4g55g[2], 'Now divide both sides by ten'), mk('tick', 'choice 2', 'Choice number two again'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t32-02 (course question: a right trapezoid)
# A course addition (no Hebrew source); its method is the one the trapezoid lesson gives: drop the height from D, a
# rectangle and a right triangle, a triple, then the area formula. Trap: the slanted leg 10 used as the height (120).
# V3: the colour copy; AB marked as a height we don't know; the height from D dashed (D pointed first); ABED tinted, 9 on
# BE, 6 on EC; DEC tinted orange, the triple 6-8-10, 8 written on DE; then the area.
f4rqA, f4rqB, f4rqC, f4rqD, f4rqE = (150.0, 130.0), (150.0, 290.0), (450.0, 290.0), (330.0, 130.0), (330.0, 290.0)
f4_rb = f4_poly([f4rqA, f4rqB, f4rqC, f4rqD], 'ink', 2.5) + [('right', 150, 290, 0, 90, 13, 'ink'), ('right', 150, 130, 270, 360, 13, 'ink')] \
    + [('txt', 136, 116, 'A', 'ink', 22, True), ('txt', 136, 304, 'B', 'ink', 22, True), ('txt', 464, 304, 'C', 'ink', 22, True),
       ('txt', 344, 116, 'D', 'ink', 22, True), ('txt', 240, 114, '9', 'ink', 22), ('txt', 300, 330, '15', 'ink', 22),
       ('txt', 406, 202, '10', 'ink', 22)]
f4_rh = [('seg', *f4rqD, *f4rqE, 'teal', 3, True), ('right', 330, 290, 90, 180, 13), ('txt', 330, 312, 'E', 'ink', 22, True)]
f4_rr = [('tint', [f4rqA, f4rqB, f4rqE, f4rqD], 'teal'), ('txt', 240, 270, '9', 'teal', 24)]
f4_re = [('txt', 390, 270, '6', 'orange', 24)]
f4r = GEO('f4r', [
    ('line', f4_rb),
    ('ab', [('path', [f4rqA, f4rqB], 'red', 6), ('txt', 120, 210, '?', 'red', 28)]),
    ('h', [('dot', *f4rqD)] + f4_rh),
    ('rect', f4_rr),
    ('ec', f4_re),
], vb='110 95 380 240', w=300, title='Right trapezoid ABCD with the height DE')
f4r2 = GEO('f4r2', [
    ('line', f4_rb + f4_rh + f4_rr + f4_re),
    ('tri', [('tint', [f4rqD, f4rqE, f4rqC], 'orange'), ('txt', 312, 210, '8', 'orange', 26)]),
    # 2026-10-18 (batch C #227): the area is the WHOLE trapezoid's
    ('whole', [('dim', 110, 95, 380, 240)] + f4_rb + [('tint', [f4rqA, f4rqB, f4rqC, f4rqD], 'teal')] + f4_poly([f4rqA, f4rqB, f4rqC, f4rqD], 'teal', 5)
              + [('seg', *f4rqD, *f4rqE, 'orange', 3, True), ('txt', 312, 210, '8', 'orange', 26)]),
], vb='110 95 380 240', w=300, title='Right trapezoid ABCD: the triangle DEC')
f4r_a = IH('f4r_a', '$EC=15-9=6$', size=28)
f4r_b = I('f4r_b', '$6,\\ 8,\\ 10$', size=28)
f4r_c = [IH('f4r_c%d' % i, t, size=28) for i, t in enumerate(['$9+15=24$', '$S=\\frac{24\\cdot8}{2}$', '$\\frac{24}{2}=12$', '$12\\cdot8=96$'])]
for _g in (f4r, f4r2): f4_pin(_g); _R(_g, 190)
_R(f4r_a, 230, x=1340)
# 2026-10-18: the working sits to the RIGHT of the copy (the stem is tall, so a column under the copy would be shrunk)
for _k, _x in enumerate([f4r_b] + f4r_c): _R(_x, 200 + 54 * _k, x=1340)
video('solve-q-r26-t32-02', 'solution', qid='q-r26-t32-02', slides=[
    S('Drop the height',
      L("A B C D is a right trapezoid, with A D parallel to B C, and angle A B C is ninety degrees. Given: A D is nine "
        "centimeters, B C is fifteen centimeters, and C D is ten centimeters. What is the area of the trapezoid, in square "
        "centimeters?", pt('stem', 'A B C D is a right trapezoid', 'hl', 11.0), voice='calm', pause=0.5),
      L("For the area we need the two bases, which we have, nine and fifteen, and the height. A B is a height, because it's "
        "perpendicular to both bases, but we don't know its length.", show(f4r['line'], 'For the area we need'), show(f4r['ab'], 'A B is a height')),
      L("[short pause] So let's drop a height from D down to B C, and call its foot E. Now we've split the trapezoid into a "
        "rectangle, A B E D, and a right triangle, D E C.", show(f4r['h'], "let's drop a height from D"),
        show(f4r['rect'], "Now we've split the trapezoid")),
      L("In the rectangle, B E equals A D, nine. So E C is fifteen minus nine, which is six.", show(f4r_a, 'So E C is fifteen minus nine'),
        show(f4r['ec'], 'which is six'))),
    S('A triple, then the area',
      L("Now the right triangle D E C. Its hypotenuse is C D, ten, and one leg is six. That's the triple six, eight, ten, so "
        "the other leg, D E, is eight. That's the height.", show(f4r2['line'], 'Now the right triangle'), show(f4r2['tri'], 'Its hypotenuse is C D'), show(f4r_b, "That's the triple")),
      L("Now the area of the whole trapezoid. The area of a trapezoid is the sum of the bases, times the height, over two. "
        "Nine plus fifteen is twenty-four. So the area is twenty-four times eight, over two.",
        show(f4r2['whole'], 'Now the area of the whole trapezoid'), show(f4r_c[0], 'Nine plus fifteen'),
        show(f4r_c[1], 'So the area is twenty-four')),
      L("Let's halve the twenty-four first. Twenty-four over two is twelve, and twelve times eight is ninety-six. Choice "
        "number two is our answer.", show(f4r_c[2], 'Twenty-four over two'), show(f4r_c[3], 'twelve times eight'),
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("If you got one hundred twenty, you used C D, ten, as the height. But the slanted leg is not the height. The height "
        "is perpendicular to the bases. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 1', 'If you got one hundred twenty'))),
])

# ------------------------------------------------------------------------------------------------ geo-056 (lesson: Quadrilaterals in Questions)
# Hebrew (geo 2370-2373): last lesson we learned the rules of the quadrilaterals; now a set of basic-level questions.
# Kept from the English lesson: try each question yourself first; the name of the shape is a given (write its properties on
# the figure, only the useful ones); the answer often hides in a triangle. Added: one concrete example of each move.
f4n1 = I('f4n1', 'The name of the shape $\\rightarrow$ its properties, on the figure', size=30)
f4n2 = I('f4n2', 'Rhombus: $\\ $four equal sides, $\\ $diagonals at $90°$', size=28)
f4n3 = I('f4n3', 'Look for a useful triangle: $\\ $isosceles, $\\ $a triple, $\\ $gold or silver', size=28)
video('geo-056', 'lesson', slides=[
    S('Quadrilaterals in Questions',
      L("In the last lessons we learned the rules of the quadrilaterals. Now we'll practice a set of questions at a basic "
        "level. Try each question yourself first, and then watch the solution.")),
    S('How to start',
      L("Every question opens with the name of a shape: a parallelogram, a rectangle, a rhombus, a square, a deltoid, or a "
        "trapezoid. The name is a given. Write what it gives you right on the figure.", show(f4n1, 'Every question opens')),
      L("For example, if it says rhombus, mark all four sides as equal, and the diagonals as perpendicular. But write only "
        "the properties that help you in this question, not all of them.", show(f4n2, 'if it says rhombus')),
      L("And most of the time, the answer hides in a triangle: an isosceles triangle, a Pythagorean triple, or a gold or "
        "silver triangle. Let's start. [pause] Okay. I'll see you in the next video.", show(f4n3, 'the answer hides in a triangle'))),
])

# =================================================================================================================
# Topic-32 question block 1 (fragment f5, 2026-10-14): geo32-g057 ... geo32-g060, the Hebrew "quadrilaterals basics
# learning" sample questions (geo 2370-2560). Question figure on the left (FIG_LEFT, figw 0.56), our colour copy built in
# layers on the right (Rule V3). All the working is written inside the copy (txt rows under / beside the shape), so the
# layers stay consecutive. Every Hebrew method is kept.
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g057', 'solve-geo32-g058', 'solve-geo32-g059', 'solve-geo32-g060'})


def f5_arc(P, Q, R, r, col, label=None, lr=None):
    """the inside angle at P between the rays P->Q and P->R (the smaller one)"""
    a, b = gdir(*P, *Q), gdir(*P, *R)
    if (b - a) % 360 > 180: a, b = b, a
    e = ('arc', P[0], P[1], r, a, b, col)
    if label: e = e + (label,) + ((lr,) if lr else ())
    return e


def f5_wedge(P, Q, R, r, col):
    a, b = gdir(*P, *Q), gdir(*P, *R)
    if (b - a) % 360 > 180: a, b = b, a
    return ('wedge', P[0], P[1], r, a, b, col)


def f5_poly(pts, col='ink', w=3):
    n = len(pts)
    return [('seg', pts[k][0], pts[k][1], pts[(k + 1) % n][0], pts[(k + 1) % n][1], col, w) for k in range(n)]


def f5_lab(pts, names, off, size=26):
    return [('txt', p[0] + o[0], p[1] + o[1], nm, 'ink', size, True) for p, nm, o in zip(pts, names, off)]


def f5_mid(P, Q):
    return ((P[0] + Q[0]) / 2.0, (P[1] + Q[1]) / 2.0)


def f5_pin(g):
    """every layer is drawn at its base figure's box (fig / of), so a base that the renderer shrinks to fit keeps its
    layers on top of it"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


def f5_sector(P, Q, R, r, col, n=14):
    """a tinted sector for the inside angle at P (a polygon: the board draws polygons exactly)"""
    a, b = gdir(*P, *Q), gdir(*P, *R)
    if (b - a) % 360 > 180: a, b = b, a
    span = (b - a) % 360
    return ('tint', [P] + [gpt(P[0], P[1], r, a + span * k / float(n)) for k in range(n + 1)], col)


# ------------------------------------------------------------------------------------------------ geo32-g057 (Hebrew: the first sample question)
# Hebrew (geo 2375-2408): the angle sum of every quadrilateral is 360; call the fourth angle beta; alpha + beta = 140 (here
# 146); 70/70 or 100/40 are possible, but neither angle can be 140 (146) or more, because the other would be 0; then the
# choices are checked one by one, including the "it looks acute" trap (figures are not to scale).
# V3: the copy with the two given angles; beta drawn at D when it is named; the sum written under the shape; the two
# unknown angles tinted together (they share 146); the impossible case in red; each choice checked in its own row; the
# "looks acute" trap: alpha's corner tinted red with "not to scale".
f5A, f5B, f5C, f5D = (180.0, 273.333), (460.0, 273.333), (499.514, 114.852), (127.555, 143.528)
f5q57 = f5_poly([f5A, f5B, f5C, f5D]) + f5_lab([f5A, f5B, f5C, f5D], 'ABCD', [(-18, 16), (18, 16), (18, -10), (-18, -10)])
f5g57 = GEO('f5g57', [
    ('line', f5q57 + [f5_arc(f5A, f5B, f5D, 36, 'orange', '118°', 62), f5_arc(f5B, f5A, f5C, 36, 'orange', '96°', 60),
                      f5_arc(f5C, f5B, f5D, 30, 'red', 'α', 52)]),
    ('beta', [f5_arc(f5D, f5A, f5C, 30, 'small', 'β', 52)]),
    ('pair', [f5_sector(f5C, f5B, f5D, 30, 'red'), f5_sector(f5D, f5A, f5C, 30, 'teal')]),
    ('zero', [('txt', 127, 100, 'β = 0°: no corner', 'red', 20)]),
    ('c3', [f5_sector(f5C, f5B, f5D, 30, 'red'), ('txt', 330, 78, 'drawn acute: not to scale', 'red', 22)]),
], vb='95 55 450 255', w=300, title='Quadrilateral ABCD')
_R(f5_pin(f5g57), 200)
# 2026-10-18 (batch C #229): one row per step, at its clause; the optional choice checks in their own column
f5g57r = [IH('f5g57r%d' % i, t, size=26) for i, t in enumerate(['$118°+96°+\\alpha+\\beta=360°$', '$118°+100°=218°$', '$218°-4°=214°$',
                                                               '$\\alpha+\\beta=360°-214°=146°$', '$\\alpha=146°\\ \\to\\ \\beta=0°$ ✗'])]
f5g57c = [IH('f5g57c%d' % i, t, size=24) for i, t in enumerate(['$26°+120°$ ✓', '$70°+76°$ ✓', '$124°+22°$ ✓'])]
for _k, _x in enumerate(f5g57r): _R(_x, 390 + 48 * _k)
for _k, _x in enumerate(f5g57c): _R(_x, 200 + 52 * _k, x=1350)
video('solve-geo32-g057', 'solution', qid='geo32-g057', slides=[
    S('The angle sum 360°',
      L("The accompanying figure shows quadrilateral A B C D. Given: angle A is one hundred eighteen degrees, and angle B is "
        "ninety-six degrees. Which of the following cannot be the value of alpha?", pt('stem', 'The accompanying figure', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("We know two angles, and the question asks about alpha, the angle at C. The angle at D has no number at all. "
        "[short pause] So we'll use the rule that connects all four angles of a quadrilateral.",
        pt('fig: α', 'the angle at C'), show(f5g57['line'], 'The angle at D has no number')),
      L("[short pause] The angles of every quadrilateral add up to three hundred sixty degrees. Let's call the angle at D "
        "beta. So one hundred eighteen, plus ninety-six, plus alpha, plus beta, is three hundred sixty.",
        show(f5g57['beta'], "Let's call the angle at D"), show(f5g57r[0], 'So one hundred eighteen, plus')),
      L("First, one hundred eighteen plus ninety-six. One hundred eighteen plus a hundred is two hundred eighteen. We added "
        "four too many, so we take away four, and it's two hundred fourteen.", show(f5g57r[1], 'One hundred eighteen plus a hundred'),
        show(f5g57r[2], 'so we take away four')),
      L("Three hundred sixty minus two hundred fourteen is one hundred forty-six. So alpha and beta together are one "
        "hundred forty-six.", show(f5g57r[3], 'Three hundred sixty minus'), show(f5g57['pair'], 'So alpha and beta together')),
      L("What does that tell us? The two angles share one hundred forty-six between them. They could be seventy-three each. "
        "Or alpha could be one hundred, and beta forty-six. But neither of them can be one hundred forty-six or more."),
      L("If alpha were one hundred forty-six, beta would be zero. That would leave zero degrees at D, so D would no longer "
        "be a proper corner of this quadrilateral. So alpha can't be one hundred forty-six, and choice number four is our "
        "answer.", show(f5g57r[4], 'If alpha were'), show(f5g57['zero'], 'That would leave zero degrees'),
        mk('tick', 'choice 4', 'and choice number four is our answer')),
      L("In the exam you'd mark it and move on. But here, let's check the other choices too, because one of them hides a "
        "trap. Alpha twenty-six gives beta one hundred twenty, together one hundred forty-six, so it's possible.",
        show(f5g57c[0], 'Alpha twenty-six gives'), mk('cross', 'choice 1', "so it's possible")),
      L("Alpha seventy gives beta seventy-six, together one hundred forty-six, also possible.",
        show(f5g57c[1], 'Alpha seventy gives'), mk('cross', 'choice 2', 'also possible')),
      L("Now alpha one hundred twenty-four. Some students say, wait, alpha looks acute in the figure, so it can't be one "
        "hundred twenty-four. But figures on the exam are not drawn to scale. An angle can be drawn acute and still be "
        "obtuse. Alpha one hundred twenty-four gives beta twenty-two, and that's possible too. So only one hundred "
        "forty-six is impossible, choice number four. [pause] Okay. I'll see you in the next question.",
        show(f5g57['c3'], 'figures on the exam are not drawn to scale'), show(f5g57c[2], 'Alpha one hundred twenty-four gives'),
        mk('cross', 'choice 3', "and that's possible too"), mk('tick', 'choice 4', 'forty-six is impossible'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g058 (Hebrew: the second sample question)
# Hebrew (geo 2410-2460): the perimeter = the sum of the sides; opposite sides equal (CD = AB); AE is part of AD; opposite
# angles equal (D = B); neighbouring angles add to 180 (A, and C either way); ECD = C - BCE, so CE is a bisector; triangle
# EDC: the third angle by the angle sum, or by the Z (ED is parallel to BC); equal angles -> isosceles, ED = CD; then AD,
# BC and the perimeter. English numbers 9, 4, 72, 54 -> 44. The pattern line (a bisector in a parallelogram cuts off an
# isosceles triangle) is kept from the course.
# V3: values written on the copy the moment they are found (CD 9, D 72, C 108 split 54 + 54); triangle EDC tinted; the Z
# traced; ED 9 written; AD = 13 and BC = 13 written; the perimeter under the shape.
f5P, f5Q, f5R, f5S, f5E = (197.95, 69.217), (89.885, 290.783), (442.05, 290.783), (550.115, 69.217), (303.6, 69.217)   # A B C D E
f5q58 = (f5_poly([f5P, f5Q, f5R, f5S]) + [('seg', f5E[0], f5E[1], f5R[0], f5R[1], 'ink', 3)]
         + f5_lab([f5P, f5Q, f5R, f5S, f5E], 'ABCDE', [(-16, -14), (-16, 16), (14, 18), (16, -14), (0, -20)]))
f5g58 = GEO('f5g58', [
    ('line', f5q58 + [('txt', 128, 172, '9', 'ink', 24), ('txt', 251, 50, '4', 'ink', 24), f5_arc(f5Q, f5R, f5P, 34, 'small', '72°', 58),
                      f5_arc(f5R, f5Q, f5E, 34, 'small', '54°', 58)]),
    ('cd9', [('seg', f5R[0], f5R[1], f5S[0], f5S[1], 'teal', 5), ('txt', 520, 190, '9', 'teal', 26)]),
    ('d72', [f5_arc(f5S, f5P, f5R, 34, 'small', '72°', 58)]),
    ('c108', [f5_arc(f5R, f5Q, f5S, 54, 'orange'), ('txt', 520, 318, '108°', 'orange', 26)]),
    ('c54', [f5_arc(f5R, f5E, f5S, 34, 'small', '54°', 58)]),
    ('tri', [('tint', [f5E, f5S, f5R], 'teal')]),
    ('e54', [f5_arc(f5E, f5S, f5R, 30, 'small', '54°', 54)]),
    ('z', [('path', [(f5S[0], f5S[1]), (f5E[0], f5E[1]), (f5R[0], f5R[1]), (f5Q[0], f5Q[1])], 'teal', 7)]),
    ('ed9', [('seg', f5E[0], f5E[1], f5S[0], f5S[1], 'teal', 5), ('txt', 430, 50, '9', 'teal', 26)]),
    ('ad', [('txt', 250, 30, '13', 'red', 24), ('txt', 266, 315, '13', 'red', 26)]),
], vb='60 15 530 320', w=300, title='Parallelogram ABCD with the line CE')
_R(f5_pin(f5g58), 200)
f5g58p = GEO('f5g58p', [
    ('line', f5q58 + [('txt', 128, 172, '9', 'ink', 24), ('txt', 251, 50, '4', 'ink', 24), ('txt', 520, 190, '9', 'teal', 26),
                      ('txt', 430, 50, '9', 'teal', 26), ('tint', [f5E, f5S, f5R], 'teal')]),
    ('ad', [('path', [f5P, f5S], 'red', 6), ('txt', 374, 34, '13', 'red', 24), ('txt', 266, 315, '13', 'red', 26)]),
    ('per', [('path', [f5P, f5Q, f5R, f5S, f5P], 'red', 5)]),
], vb='60 15 530 320', w=300, title='Parallelogram ABCD: the perimeter')
_R(f5_pin(f5g58p), 200)
# 2026-10-18 (batch C #230): every spoken step written at its clause, in a working column under the copy
f5g58r = [IH('f5g58r%d' % i, t, size=26) for i, t in enumerate(['$180°-72°=108°$', '$108°-54°=54°$', '$72°+54°=126°$', '$180°-126°=54°$'])]
f5g58s = [IH('f5g58s%d' % i, t, size=26) for i, t in enumerate(['$AD=4+9=13$', '$9+9=18$', '$13+13=26$', '$18+26=44$'])]
f5g58w = [I('f5g58w0', 'bisector + Z', size=22), I('f5g58w1', '→ isosceles', size=22)]
for _k, _x in enumerate(f5g58r + f5g58w): _R(_x, 200 + 54 * _k, x=1350)
for _k, _x in enumerate(f5g58s): _R(_x, 200 + 54 * _k, x=1350)
video('solve-geo32-g058', 'solution', qid='geo32-g058', slides=[
    S('A bisector in a parallelogram',
      L("A B C D is a parallelogram, and E lies on A D. Given: A B is nine centimeters, A E is four centimeters, angle A B C "
        "is seventy-two degrees, and angle B C E is fifty-four degrees. What is the perimeter of the parallelogram, in "
        "centimeters?", pt('stem', 'A B C D is a parallelogram', 'hl', 11.0), voice='calm', pause=0.5),
      L("The perimeter is the sum of the four sides, A B plus B C plus C D plus A D. We know only one side, A B, and a piece "
        "of A D. [short pause] So we'll find the missing sides one at a time, with the rules of the parallelogram.",
        show(f5g58['line'], 'The perimeter is the sum')),
      L("[short pause] In a parallelogram, opposite sides are parallel and equal. A B is nine, so C D is nine too. B C and A "
        "D are equal to each other, but we don't know them yet. We do know part of A D. A E is four, and that will probably "
        "help.", show(f5g58['cd9'], 'so C D is nine too'), pt('fig: 4', 'A E is four')),
      L("Now the angles. Angle B is seventy-two. Opposite angles in a parallelogram are equal, so angle D is seventy-two too. "
        "Angles next to each other add up to one hundred eighty, so the whole angle C is one hundred eighty minus "
        "seventy-two, which is one hundred eight.", show(f5g58['d72'], 'so angle D is seventy-two'),
        show(f5g58r[0], 'so the whole angle C'), show(f5g58['c108'], 'which is one hundred eight')),
      L("Angle B C E is fifty-four, so the rest of angle C, angle E C D, is one hundred eight minus fifty-four, which is "
        "fifty-four too. So C E cuts angle C into two equal halves. It's an angle bisector.",
        show(f5g58r[1], 'one hundred eight minus fifty-four'), show(f5g58['c54'], 'which is fifty-four too')),
      L("Now look at triangle E D C. Two of its angles are known, seventy-two at D and fifty-four at C. The angles of a "
        "triangle add up to one hundred eighty. Seventy-two plus fifty-four is one hundred twenty-six, and one hundred "
        "eighty minus one hundred twenty-six is fifty-four. So angle D E C is fifty-four.",
        show(f5g58['tri'], 'Now look at triangle'), show(f5g58r[2], 'Seventy-two plus fifty-four'),
        show(f5g58r[3], 'and one hundred eighty minus'), show(f5g58['e54'], 'So angle D E C is fifty-four')),
      L("There's also a shorter way to see it. E D is parallel to B C, and C E crosses them. Follow B C, then C E, then E "
        "D, and we get a Z. The angles inside a Z are equal, so angle D E C equals angle B C E, fifty-four, right away.",
        show(f5g58['z'], 'Follow B C, then C E')),
      L("In triangle E D C, the angles at E and at C are both fifty-four. Equal angles face equal sides. The angle at E "
        "faces C D, and the angle at C faces E D. So E D equals C D, which is nine.", show(f5g58['ed9'], 'So E D equals C D')),
      L("Remember this pattern. An angle bisector in a parallelogram cuts off an isosceles triangle. Why does it always "
        "happen? The bisector cuts the angle into two equal parts. The opposite sides are parallel, so the Z gives that "
        "same angle again at the other end. So the triangle has two equal angles, and it's isosceles.",
        show(f5g58w[0], 'An angle bisector in a parallelogram'), show(f5g58w[1], 'So the triangle has two equal angles'))),
    S('The perimeter',
      L("Almost done. All of A D is four plus nine, which is thirteen, and B C is thirteen too, because opposite sides are "
        "equal.", show(f5g58p['line'], 'Almost done'), show(f5g58s[0], 'All of A D is four plus nine'),
        show(f5g58p['ad'], 'and B C is thirteen too')),
      L("The perimeter is nine plus thirteen plus nine plus thirteen. Nine and nine is eighteen. Thirteen and thirteen is "
        "twenty-six. And together, that's forty-four. Choice number three is our answer. [pause] Okay. I'll see you in the next "
        "question.", show(f5g58s[1], 'Nine and nine is eighteen'), show(f5g58s[2], 'Thirteen and thirteen'),
        show(f5g58p['per'], 'The perimeter is nine'), show(f5g58s[3], "And together, that's forty-four"),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g059 (Hebrew: the third sample question)
# Hebrew (geo 2462-2537): the diagonals of a rectangle bisect each other and are equal, so EA = EB = EC = ED; the
# perimeter of EBC gives EB + EC, so each half-diagonal and the diagonal AC; the other leg from a triple (here 5, 12, 13
# doubled: 10, 24, 26). Then THREE ways for the area of ABE, "know them all": (1) the median halves triangle ABC (same
# base, same height); (2) the diagonals cut every parallelogram into four triangles of equal area (why: top = bottom,
# left = right, and S1 = S2); (3) base times height, the height from E is half of BC.
# V3: setup - the four half-diagonals ticked equal, triangle EBC traced for its perimeter, 13 written on EB and EC, the
# right triangle ABC tinted with 10, 24, 26. Each method on its own slide with a fresh copy that keeps AB = 10 and
# BC = 24 written on it (same orientation and labels): method 1 the two halves of ABC tinted and the shared dashed height
# from B; method 2 the four triangles tinted in two colours; method 3 the dashed height from E to AB with 12.
f5RA, f5RB, f5RC, f5RD, f5RE = (80.0, 80.0), (80.0, 280.0), (560.0, 280.0), (560.0, 80.0), (320.0, 180.0)
f5q59 = (f5_poly([f5RA, f5RB, f5RC, f5RD]) + [('seg', f5RA[0], f5RA[1], f5RC[0], f5RC[1], 'ink', 3), ('seg', f5RB[0], f5RB[1], f5RD[0], f5RD[1], 'ink', 3)]
         + f5_lab([f5RA, f5RB, f5RC, f5RD], 'ABCD', [(-16, -12), (-16, 16), (16, 16), (16, -12)]) + [('txt', 320, 158, 'E', 'ink', 24, True)])
f5FT = (lambda t: (80 + t * 480 / 520.0, 80 + t * 200 / 520.0))((0 * 480 + 200 * 200) / 520.0)   # the foot of the height from B on AC
f5k59 = [('txt', 320, 304, '24', 'ink', 24), ('txt', 56, 180, '10', 'ink', 24)]
# 2026-10-18 (batch C #231): the copies show the shape only; every calculation is its own row in a working panel under
# the copy, at its clause
f5g59 = GEO('f5g59', [
    ('line', f5q59 + [('txt', 320, 304, '24', 'ink', 24)]),
    ('eq', [('tick', f5RE[0], f5RE[1], f5RA[0], f5RA[1], 1), ('tick', f5RE[0], f5RE[1], f5RB[0], f5RB[1], 1),
            ('tick', f5RE[0], f5RE[1], f5RC[0], f5RC[1], 1), ('tick', f5RE[0], f5RE[1], f5RD[0], f5RD[1], 1)]),
    ('ebc', [('tint', [f5RE, f5RB, f5RC], 'orange')]),
    ('h13', [('txt', 182, 250, '13', 'orange', 26), ('txt', 458, 250, '13', 'orange', 26)]),
    ('abc', [('tint', [f5RA, f5RB, f5RC], 'teal'), ('seg', f5RA[0], f5RA[1], f5RC[0], f5RC[1], 'teal', 5), ('right', 80, 280, 0, 90, 16)]),
    ('ab10', [('seg', f5RA[0], f5RA[1], f5RB[0], f5RB[1], 'teal', 6), ('txt', 56, 180, '10', 'teal', 26)]),
], vb='30 40 580 280', w=300, title='Rectangle ABCD with its diagonals')
f5g59a = GEO('f5g59a', [
    ('line', f5q59 + f5k59),
    ('abc', [('tint', [f5RA, f5RB, f5RE], 'teal'), ('tint', [f5RE, f5RB, f5RC], 'orange'), ('seg', f5RB[0], f5RB[1], f5RE[0], f5RE[1], 'red', 5)]),
    ('h', [('seg', 80, 280, f5FT[0], f5FT[1], 'red', 3, True), ('txt', f5FT[0] - 22, f5FT[1] + 40, 'h', 'red', 26, True)]),
], vb='30 40 580 280', w=300, title='The median BE of triangle ABC')
f5g59b = GEO('f5g59b', [
    ('line', f5q59 + f5k59),
    ('opp', [('tint', [f5RA, f5RB, f5RE], 'teal'), ('tint', [f5RC, f5RD, f5RE], 'teal'), ('tint', [f5RB, f5RC, f5RE], 'orange'),
             ('tint', [f5RA, f5RD, f5RE], 'orange'), ('txt', 140, 185, 'S₁', 'teal', 26), ('txt', 500, 185, 'S₁', 'teal', 26),
             ('txt', 320, 245, 'S₂', 'orange', 26), ('txt', 320, 118, 'S₂', 'orange', 26)]),
    ('adj', [('seg', f5RB[0], f5RB[1], f5RE[0], f5RE[1], 'red', 5), ('txt', 214, 222, 'median', 'red', 20)]),
], vb='30 40 580 280', w=300, title='The diagonals cut the rectangle into four triangles')
f5g59c = GEO('f5g59c', [
    ('line', f5q59 + f5k59),
    ('h', [('tint', [f5RA, f5RB, f5RE], 'teal'), ('seg', 320, 180, 80, 180, 'red', 3, True), ('right', 80, 180, 0, 270, 14, 'red'),
           ('txt', 200, 164, '12', 'red', 26)]),
    ('across', [('seg', 320, 180, 560, 180, 'orange', 3, True), ('txt', 440, 164, '12', 'orange', 26), ('dot', 320, 180)]),
], vb='30 40 580 280', w=300, title='The height from E to AB')
_f5t = lambda pre, rows: [IH('%s%d' % (pre, i), t, size=26) for i, t in enumerate(rows)]
f5g59r0 = [IH('f5g59r0_%d' % i, t, size=22) for i, t in enumerate( ['$EB+24+EC=50$', '$EB+EC=26$', '$EB=EC=13$'])]
f5g59r1 = _f5t('f5g59r1_', ['$AC=2\\cdot13=26$', '$10,\\ 24,\\ 26=2\\cdot(5,12,13)$', '$AB=10$'])
f5g59ra = [I('f5g59ra_t', 'AE = EC, the same height from B', size=24)] + _f5t('f5g59ra', ['$10\\cdot24=240$', '$S_{ABC}=\\frac{240}{2}=120$', '$S_{ABE}=\\frac{120}{2}=60$'])
f5g59rb = [I('f5g59rb_t', 'Equal areas: $S_1=S_2$', size=24)] + _f5t('f5g59rb', ['$10\\cdot24=240$', '$\\frac{240}{4}=60$'])
f5g59rc = _f5t('f5g59rc', ['$\\frac{24}{2}=12$', '$10\\cdot12=120$', '$\\frac{120}{2}=60$'])
for _k, _x in enumerate(f5g59r0): _R(_x, 200 + 54 * _k, x=1340)
for _k, _x in enumerate(f5g59r1): _R(_x, 360 + 50 * _k)
for _rows in (f5g59ra[1:], f5g59rb[1:], f5g59rc):
    for _k, _x in enumerate(_rows): _R(_x, 200 + 56 * _k, x=1350)
_R(f5g59ra[0], 360); _R(f5g59rb[0], 360)
for _g in (f5g59, f5g59a, f5g59b, f5g59c): _R(f5_pin(_g), 200)
video('solve-geo32-g059', 'solution', qid='geo32-g059', slides=[
    S('Half-diagonals',
      L("The diagonals of rectangle A B C D intersect at E. Given: B C is twenty-four centimeters, and the perimeter of "
        "triangle E B C is fifty centimeters. What is the area of triangle A B E, in square centimeters?",
        pt('stem', 'The diagonals of rectangle', 'hl', 10.0), voice='calm', pause=0.5),
      L("We have a rectangle, the perimeter of one triangle, and a question about another triangle. [short pause] First "
        "we'll find the missing lengths. Then we'll find the area in three different ways, twice by understanding and "
        "once the math way.",
        show(f5g59['line'], 'We have a rectangle')),
      L("[short pause] We'll probably need a property of the rectangle's diagonals. In a rectangle, the diagonals cut each "
        "other in half, and they're equal. So all four pieces, A E, E B, E C and E D, are equal.",
        show(f5g59['eq'], 'So all four pieces')),
      L("The perimeter of triangle E B C is E B plus twenty-four plus E C, and that's fifty. So E B and E C together are "
        "twenty-six.", show(f5g59['ebc'], 'The perimeter of triangle E B C'), show(f5g59r0[0], 'E B plus twenty-four plus E C'),
        show(f5g59r0[1], 'So E B and E C together')),
      L("They're equal, so each one is thirteen. Then A E and E D are thirteen too, and the whole diagonal A C is twice "
        "thirteen, twenty-six.", show(f5g59r0[2], 'so each one is thirteen'), show(f5g59['h13'], 'Then A E and E D'),
        show(f5g59r1[0], 'and the whole diagonal A C')),
      L("Now the right triangle A B C. We know its hypotenuse, twenty-six, and one leg, twenty-four. That's the triple five, "
        "twelve, thirteen, doubled, ten, twenty-four, twenty-six. So A B is ten.", show(f5g59['abc'], 'Now the right triangle'),
        show(f5g59r1[1], "That's the triple five"), show(f5g59r1[2], 'So A B is ten'), show(f5g59['ab10'], 'So A B is ten'))),
    SM('Method 1 · Understanding: the median', 'The median',
      L("[pause] Now the area of A B E. Let's start by understanding, with the median. Look at triangle A B C. E is the middle of A C, so B "
        "E is a median.", show(f5g59a['line'], 'Look at triangle A B C'), show(f5g59a['abc'], 'so B E is a median')),
      L("A median cuts a triangle into two triangles of equal area. Why? A E equals E C, so the two triangles have equal "
        "bases, and they share the same height from B to the line A C.", show(f5g59a['h'], 'they share the same height'),
        show(f5g59ra[0], 'A E equals E C')),
      L("Triangle A B C is easy. It's a right triangle with legs ten and twenty-four, so its area is leg times leg, over "
        "two. Ten times twenty-four is two hundred forty, and over two that's one hundred twenty.",
        show(f5g59ra[1], 'Ten times twenty-four is'), show(f5g59ra[2], 'and over two')),
      L("The median cuts it into two triangles of equal area, so A B E is half of it. Half of a hundred twenty is sixty. "
        "Choice number two is our answer.", show(f5g59ra[3], 'Half of a hundred twenty'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · Understanding: four equal triangles', 'Four equal triangles',
      L("[pause] Now by understanding again, with a rule about the diagonals. The diagonals of a rectangle cut it into four "
        "triangles of equal area.", show(f5g59b['line'], 'Now by understanding again')),
      L("Why? Opposite triangles match in size and shape. A E D matches B E C, and A E B matches C E D. Triangles next to "
        "each other, like A E B and B E C, don't have to have the same shape. But they have the same area, because B E is "
        "a median of triangle A B C, as we just saw. So all four areas are equal.",
        show(f5g59b['opp'], 'Opposite triangles match'), show(f5g59b['adj'], 'because B E is a median'), show(f5g59rb[0], 'So all four areas are equal')),
      L("This works because the diagonals cut each other in half, and that's true in every parallelogram. So the rule "
        "holds in every parallelogram, also in a rhombus and in a square.", pt('f5g59b_line', 'This works because')),
      L("The rectangle is ten times twenty-four, which is two hundred forty. One triangle is a quarter of it, two hundred "
        "forty divided by four, which is sixty. Choice number two again.", show(f5g59rb[1], 'The rectangle is ten times'),
        show(f5g59rb[2], 'forty divided by four'), mk('tick', 'choice 2', 'Choice number two again'))),
    SM('Method 3 · The math way: base times height', 'Base times height',
      L("[pause] And the third way, the math way, base times height over two. The base is A B, ten. We need the height from "
        "E to A B.", show(f5g59c['line'], 'the math way, base times height')),
      L("Draw the line from E straight to A B, and continue it across to C D. That whole line is as long as B C, "
        "twenty-four. E is the middle of the diagonals, so it's halfway between A B and C D. So the height from E to A B is "
        "half of twenty-four, twelve.", show(f5g59c['h'], 'Draw the line from E'), show(f5g59c['across'], 'and continue it across'),
        show(f5g59rc[0], 'half of twenty-four, twelve')),
      L("So the area is ten times twelve, over two. Ten times twelve is a hundred twenty, and over two that's sixty. Choice "
        "number two. [pause] Okay. I'll see you in the next question.", show(f5g59rc[1], 'Ten times twelve is'),
        show(f5g59rc[2], "and over two that's sixty"), mk('tick', 'choice 2', 'Choice number two'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g060 (Hebrew: the fourth sample question)
# Hebrew (geo 2539-2618): two area formulas for a rhombus (side times its height; diagonals multiplied over 2 - any
# quadrilateral with perpendicular diagonals); a diagonal is given, so the diagonal formula first: AC cuts BD into 5 and 5,
# the angle at O is 90, the gold triangle (5 opposite 30 is the short leg, the long leg times root 3), AC = 10 root 3,
# area 50 root 3; "once you've found all the inner pieces" other ways to add it up (the gold triangle x 4, BDA x 2,
# ADC x 2); then the shorter psychometric way: isosceles with 60 -> equilateral, two equilateral triangles. The course's
# link to the 30-30-120 triangle is kept as one short paragraph.
# V3: the rhombus copy is enlarged (the question's rhombus is narrow); AC drawn dashed after its ends are named; the
# halves 5 | 5 written on BD; the right angle at O; the gold triangle ABO tinted and outlined with 30, 60, 5, 5 root 3;
# AC's two halves written; the formula under the shape; the other ways as tints of the parts; method 2: a fresh copy,
# ABD tinted with its 60s and 10s, then BCD in the other tint.
f5HA, f5HB, f5HC, f5HD, f5HO = (320.0, 57.563), (249.311, 180.0), (320.0, 302.437), (390.689, 180.0), (320.0, 180.0)
f5q60 = (f5_poly([f5HA, f5HB, f5HC, f5HD]) + [('seg', f5HB[0], f5HB[1], f5HD[0], f5HD[1], 'ink', 3)]
         + f5_lab([f5HA, f5HB, f5HC, f5HD], 'ABCD', [(0, -18), (-20, 0), (0, 20), (20, 0)], 24))
# 2026-10-18 (batch C #232): AO and OC are labelled on the LEFT with leaders to the half-diagonals (clear of side AD);
# the whole rhombus is outlined for its area; each extra decomposition has its own triangle, base and height, the old
# selection fades; the working is written in rows under the copy
_f5ao = [('seg', 250, 118, 316, 118, 'orange', 1.5), ('txt', 222, 118, 'AO', 'orange', 20), ('txt', 222, 140, '5√3', 'orange', 22)]
_f5oc = [('seg', 250, 242, 316, 242, 'orange', 1.5), ('txt', 222, 242, 'OC', 'orange', 20), ('txt', 222, 264, '5√3', 'orange', 22)]
f5g60 = GEO('f5g60', [
    ('line', f5q60 + [f5_arc(f5HB, f5HD, f5HA, 26, 'small', '60°', 46)]),
    ('ac', [('seg', f5HA[0], f5HA[1], f5HC[0], f5HC[1], 'teal', 3, True), ('txt', 332, 192, 'O', 'ink', 22, True)]),
    ('half', [('txt', 285, 196, '5', 'teal', 22), ('txt', 355, 196, '5', 'teal', 22), ('right', 320, 180, 0, 90, 12)]),
    ('gold', [('tint', [f5HA, f5HB, f5HO], 'orange'), ('seg', f5HA[0], f5HA[1], f5HB[0], f5HB[1], 'orange', 4),
              ('seg', f5HB[0], f5HB[1], f5HO[0], f5HO[1], 'orange', 4), ('seg', f5HO[0], f5HO[1], f5HA[0], f5HA[1], 'orange', 4),
              f5_arc(f5HA, f5HB, f5HO, 30, 'small', '30°', 50)]),
    ('ao', _f5ao),
    ('ac2', _f5oc),
    ('whole', [('tint', [f5HA, f5HB, f5HC, f5HD], 'teal')] + f5_poly([f5HA, f5HB, f5HC, f5HD], 'teal', 5)),
], vb='170 25 260 300', w=270, title='Rhombus ABCD with its diagonals')
_f5base = f5q60 + [('seg', f5HA[0], f5HA[1], f5HC[0], f5HC[1], 'ink', 3), ('right', 320, 180, 0, 90, 12),
                   ('txt', 285, 196, '5', 'ink', 22), ('txt', 355, 196, '5', 'ink', 22)] + [(e[:5] + ('ink',) + e[6:]) if e[0] == 'seg' else (e[:4] + ('ink',) + e[5:]) for e in _f5ao + _f5oc]
f5g60o = GEO('f5g60o', [
    ('line', _f5base),
    ('t4', [('tint', [f5HA, f5HB, f5HO], 'orange')] + f5_poly([f5HA, f5HB, f5HO], 'orange', 4)),
    ('t2', [('dim', 170, 25, 260, 300)] + _f5base + [('tint', [f5HA, f5HB, f5HD], 'teal'), ('seg', *f5HB, *f5HD, 'teal', 5),
            ('seg', *f5HA, *f5HO, 'orange', 4, True)]),
    ('t2b', [('tint', [f5HC, f5HB, f5HD], 'teal')]),
    ('t3', [('dim', 170, 25, 260, 300)] + _f5base + [('tint', [f5HA, f5HD, f5HC], 'red'), ('seg', *f5HA, *f5HC, 'red', 5),
            ('seg', *f5HO, *f5HD, 'orange', 4, True)]),
    ('t3b', [('tint', [f5HA, f5HB, f5HC], 'red')]),
], vb='170 25 260 300', w=270, title='Other ways to add up the area')
f5g60e = GEO('f5g60e', [
    ('line', f5q60 + [f5_arc(f5HB, f5HD, f5HA, 26, 'small', '60°', 46)]),
    ('abd', [('tint', [f5HA, f5HB, f5HD], 'teal'), ('tick', f5HA[0], f5HA[1], f5HB[0], f5HB[1], 1), ('tick', f5HA[0], f5HA[1], f5HD[0], f5HD[1], 1),
             f5_arc(f5HD, f5HB, f5HA, 26, 'small', '60°', 46)]),
    ('top', [f5_arc(f5HA, f5HB, f5HD, 26, 'small', '60°', 46)]),
    ('bcd', [('tint', [f5HB, f5HC, f5HD], 'orange'), ('tick', f5HB[0], f5HB[1], f5HC[0], f5HC[1], 1), ('tick', f5HC[0], f5HC[1], f5HD[0], f5HD[1], 1)]),
], vb='170 25 260 300', w=270, title='Two equilateral triangles')
for _g in (f5g60, f5g60o, f5g60e): _R(f5_pin(_g), 200)
_f5r = lambda pre, rows, size=26: [IH('%s%d' % (pre, i), t, size=size) if t.startswith('$') else I('%s%d' % (pre, i), t, size=size - 2)
                                   for i, t in enumerate(rows)]
f5g60l = _f5r('f5g60l', ['short leg $5$', 'long leg $5\\sqrt3$', '$AC=10\\sqrt3$'])
f5g60r = _f5r('f5g60r', ['$S=\\frac{10\\cdot10\\sqrt3}{2}$', '$\\frac{10}{2}=5$', '$5\\cdot10\\sqrt3=50\\sqrt3$'])
f5g60d = _f5r('f5g60d', ['$4\\cdot\\frac{5\\cdot5\\sqrt3}{2}$', '$BDA:\\ \\frac{10\\cdot5\\sqrt3}{2}$', '$\\times2$',
                         '$ADC:\\ \\frac{10\\sqrt3\\cdot5}{2}$', '$\\times2$'], 24)
f5g60t = _f5r('f5g60t', ['two equilateral triangles'], 24)
f5g60q = _f5r('f5g60q', ['$10^2=100$', 'one: $\\frac{100\\sqrt3}{4}$', 'two: $\\frac{200\\sqrt3}{4}$', '$=50\\sqrt3$', '$B=120°$: $AC=10\\sqrt3$'], 24)
for _k, _x in enumerate(f5g60l + f5g60r): _R(_x, 200 + 50 * _k, x=1330)
for _k, _x in enumerate(f5g60d): _R(_x, 200 + 54 * _k, x=1330)
for _k, _x in enumerate(f5g60t + f5g60q): _R(_x, 200 + 50 * _k, x=1330)
video('solve-geo32-g060', 'solution', qid='geo32-g060', slides=[
    SM('Method 1 · The math way: the diagonals', 'The diagonals',
      L("A B C D is a rhombus. Given: B D is ten centimeters, and angle A B D is sixty degrees. What is the area of the "
        "rhombus, in square centimeters?", pt('stem', 'A B C D is a rhombus', 'hl', 7.0), voice='calm', pause=0.5),
      L("We learned two formulas for the area of a rhombus. A rhombus is a parallelogram with all its sides equal, so one "
        "formula is side times the height to that side. The other is the two diagonals multiplied, over two. That one "
        "works for any quadrilateral whose diagonals are perpendicular. [short pause] A diagonal is given here, so we'll "
        "start with the diagonal formula.", show(f5g60['line'], 'We learned two formulas')),
      L("[short pause] In a rhombus, the diagonals cut each other in half. So let's draw the other diagonal, from A to C. "
        "It cuts B D into five and five.", show(f5g60['ac'], 'from A to C'), show(f5g60['half'], 'It cuts B D into five and five')),
      L("The diagonals of a rhombus are also perpendicular, so the angle at O is ninety. That makes a special triangle, A B "
        "O. It's a right triangle with a sixty-degree angle, so it's a gold triangle, thirty, sixty, ninety.",
        show(f5g60['gold'], 'That makes a special triangle')),
      L("In a gold triangle the sides have a fixed ratio. Five is across from the thirty-degree angle, so it's the short "
        "leg. To get the long leg, we multiply by root three. So A O is five root three.", show(f5g60l[0], "so it's the short"),
        show(f5g60l[1], 'To get the long leg'), show(f5g60['ao'], 'So A O is five root three')),
      L("The diagonals cut each other in half, so the bottom part, O C, is five root three too. The whole diagonal A C is "
        "five root three plus five root three, which is ten root three.", show(f5g60['ac2'], 'so the bottom part'),
        show(f5g60l[2], 'which is ten root three')),
      L("Now the formula, for the whole rhombus. The diagonals multiplied, over two, is ten times ten root three, over two.",
        show(f5g60['whole'], 'for the whole rhombus'), show(f5g60r[0], 'The diagonals multiplied')),
      L("Ten over two is five, and five times ten root three is fifty root three. Choice number two is our answer.",
        show(f5g60r[1], 'Ten over two is five'), show(f5g60r[2], 'and five times ten root three'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 1 · The math way: the diagonals', 'The diagonals',
      L("[pause] Once you've found all the inner pieces, you can add up the area in other ways too. Some students take the "
        "gold triangle, base five and height five root three, and multiply its area by four, because the rhombus is made of four of these triangles.",
        show(f5g60o['line'], 'Once you\'ve found all the inner pieces'), show(f5g60o['t4'], 'Some students take the gold triangle'),
        show(f5g60d[0], 'multiply its area by four')),
      L("Some take the top triangle, B D A. Its base is B D, ten, and its height is A O, five root three. The bottom "
        "triangle, B D C, is the same, so we take it twice.", show(f5g60o['t2'], 'Some take the top triangle'),
        show(f5g60d[1], 'Its base is B D'), show(f5g60o['t2b'], 'The bottom triangle, B D C'), show(f5g60d[2], 'so we take it twice')),
      L("And some take the triangle on the right, A D C. Its base is A C, ten root three, and its height is O D, five. The "
        "left triangle is the same, so again we take it twice. These all use rules we know, so pick whichever you see "
        "first.", show(f5g60o['t3'], 'And some take the triangle on'), show(f5g60d[3], 'Its base is A C'),
        show(f5g60o['t3b'], 'The left triangle is the same'), show(f5g60d[4], 'so again we take it twice'))),
    SM('Method 2 · Insight', 'Two equilateral triangles',
      L("[pause] And one more way, an insight. Some students notice the sixty degrees and say, wait, that's a hint.",
        show(f5g60e['line'], 'notice the sixty degrees')),
      L("In a rhombus all the sides are equal, so A B equals A D. That makes triangle A B D isosceles, and angle A D B is "
        "sixty too.", show(f5g60e['abd'], 'so A B equals A D')),
      L("Sixty plus sixty is one hundred twenty, so the top angle is sixty as well. The triangle is equilateral. It's worth "
        "remembering that an isosceles triangle with a sixty-degree angle is always equilateral. B D is ten, so A B and A D "
        "are ten.", show(f5g60e['top'], 'so the top angle is sixty as well')),
      L("All the sides of a rhombus are equal, so D C and B C are ten too. So the rhombus is two equilateral triangles.",
        show(f5g60e['bcd'], 'so D C and B C are ten too'), show(f5g60t[0], 'So the rhombus is two equilateral')),
      L("The area of one equilateral triangle is the side squared, times root three, over four. The side is ten, and ten "
        "squared is a hundred. So one triangle is a hundred root three, over four.", show(f5g60q[0], 'ten squared is a hundred'),
        show(f5g60q[1], 'So one triangle is')),
      L("The rhombus is two of these triangles, so we take it twice. That's two hundred root three, over four, which is "
        "fifty root three. Choice number two.", show(f5g60q[2], "That's two hundred root three"), show(f5g60q[3], 'which is fifty root three'),
        mk('tick', 'choice 2', 'fifty root three. Choice number two')),
      L("And one more link to the triangles topic. Angle A B C is sixty plus sixty, one hundred twenty. So triangle A B C is "
        "the thirty, thirty, one hundred twenty triangle with sides ten and ten, and its long side, A C, is ten root three "
        "straight away. [pause] Okay. I'll see you in the next question.", show(f5g60q[4], 'Angle A B C is sixty plus sixty'))),
])

# =================================================================================================================
# Topic-32 fragment f6 (2026-10-14): geo32-g061, g062, g063 (the end of the Hebrew "quadrilaterals basics" sample
# questions, geo 2636-2789), geo-065 (the advanced lesson's opening, geo 2794-2799), geo32-g066 and g067 (the first two
# advanced sample questions, geo 2801-2950). Question figure on the left (FIG_LEFT), our colour copy built in layers on
# the right (Rule V3); the typed working is written inside the copy (text layers), so the layers stay consecutive.
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g061', 'solve-geo32-g062', 'solve-geo32-g063', 'solve-geo32-g067'})


def f6_poly(pts, col='ink', w=3):
    """the sides of a closed polygon as segments"""
    return [('seg', pts[k][0], pts[k][1], pts[(k + 1) % len(pts)][0], pts[(k + 1) % len(pts)][1], col, w) for k in range(len(pts))]


def f6_name(p, t, dx, dy):
    return ('txt', p[0] + dx, p[1] + dy, t, 'ink', 26, True)


def f6_seg(p, q, col='ink', w=3, dash=False):
    return ('seg', p[0], p[1], q[0], q[1], col, w, dash)


# ------------------------------------------------------------------------------------------------ geo32-g061 (Hebrew: the square and the equilateral triangle)
# Hebrew (geo 2636-2693): start from the square; choose which of its many properties matter (no diagonals here); mark all
# the sides with one tick, mark the right angles next to the angle we want; the equilateral triangle: its sides get the
# same tick - "the catch", the triangle's sides equal the square's; all its angles 60; look at the triangle that holds
# the angle: isosceles ("if we hadn't marked the sides we might not see it"); equal sides -> equal angles alpha; the top
# angle 90 - 60 = 30; 30 + 2 alpha = 180, alpha = 75. English asks one step more: angle PAD = 90 - 75 = 15 (75 is the trap).
# V3: the copy built at the words; ticks and squares as each given is marked; the studied triangle ABP tinted and held;
# the values written on the figure when found; the working typed beside the figure.
f6B1, f6A1, f6D1, f6C1, f6P1 = (210.5, 70.5), (210.5, 289.5), (429.5, 289.5), (429.5, 70.5), (320.0, 260.16)
f6g61 = GEO('f6g61', [
    ('line', f6_poly([f6B1, f6A1, f6D1, f6C1]) + [f6_seg(f6B1, f6P1), f6_seg(f6C1, f6P1), f6_seg(f6A1, f6P1),
              f6_name(f6B1, 'B', -18, -14), f6_name(f6A1, 'A', -18, 16), f6_name(f6D1, 'D', 18, 16), f6_name(f6C1, 'C', 18, -14),
              f6_name(f6P1, 'P', 22, 16), ('arc', f6A1[0], f6A1[1], 60, 0, 15, 'red'), ('txt', 286, 280, 'x', 'red', 22, True)]),
    ('sq', [('tick', *f6B1, *f6A1), ('tick', *f6A1, *f6D1), ('tick', *f6D1, *f6C1), ('tick', *f6C1, *f6B1)]),
    ('r90', [('right', f6B1[0], f6B1[1], 270, 360, 16), ('right', f6A1[0], f6A1[1], 0, 90, 16)]),
    ('eqs', [('tick', *f6B1, *f6P1), ('tick', *f6C1, *f6P1)]),
    ('e60', [('arc', f6B1[0], f6B1[1], 44, 300, 360, 'small', '60°', 66), ('arc', f6C1[0], f6C1[1], 30, 180, 240, 'small', '60°', 52),
             ('arc', f6P1[0], f6P1[1], 24, 60, 120, 'small', '60°', 44)]),
    ('abp', [('tint', [f6A1, f6B1, f6P1], 'teal'), ('path', [f6A1, f6B1, f6P1, f6A1], 'teal', 6)]),
], vb='175 40 290 290', w=300, title='Square ABCD with the equilateral triangle BPC')
_R(f5_pin(f6g61), 200)
# 2026-10-18 (batch C #233): triangle ABP on its own, bigger, same orientation and labels; a stub of AD shows the square's
# corner at A, split into BAP (alpha = 75) and PAD (x = 15), each with its own arc and value
f6g61b = GEO('f6g61b', [
    ('line', [('tint', [f6A1, f6B1, f6P1], 'teal')] + f6_poly([f6A1, f6B1, f6P1], 'teal', 4)
             + [('seg', f6A1[0], f6A1[1], 350, f6A1[1], 'ink', 2.5, True), f6_name(f6B1, 'B', -18, -10), f6_name(f6A1, 'A', -18, 14),
                f6_name(f6P1, 'P', 20, -14), ('tick', *f6B1, *f6A1), ('tick', *f6B1, *f6P1), ('txt', 330, 306, 'D →', 'ink', 18)]),
    ('b30', [('arc', f6B1[0], f6B1[1], 40, 270, 300, 'orange', '30°', 64)]),
    ('alpha', [('arc', f6A1[0], f6A1[1], 34, 15, 90, 'small', 'α', 54), ('arc', f6P1[0], f6P1[1], 30, 120, 195, 'small', 'α', 50)]),
    ('v75', [('txt', 252, 236, '75°', 'teal', 20), ('txt', 286, 218, '75°', 'teal', 20)]),
    ('x', [('arc', f6A1[0], f6A1[1], 70, 0, 15, 'red', '15°', 96)]),
], vb='178 38 180 285', w=200, title='Triangle ABP, enlarged')
_R(f5_pin(f6g61b), 200)
f6g61r = [IH('f6g61r%d' % i, t, size=26) for i, t in enumerate(['$\\angle ABP=90°-60°=30°$', '$30°+\\alpha+\\alpha=180°$',
                                                               '$2\\alpha=150°$', '$\\alpha=\\frac{150°}{2}=75°$', '$\\angle PAD=90°-75°=15°$'])]
for _k, _x in enumerate(f6g61r): _R(_x, 200 + 58 * _k, x=1250)
video('solve-geo32-g061', 'solution', qid='geo32-g061', slides=[
    SM('Mark the givens', 'Mark the givens',
      L("A B C D is a square, and P is a point inside it, so that triangle B P C is equilateral. What is angle P A D?",
        pt('stem', 'A B C D is a square', 'hl', 7.0), voice='calm', pause=0.5),
      L("We need angle P A D, the small angle at A, between A P and the side A D. [short pause] We'll mark what each given "
        "tells us on the figure, and then use the triangle that holds the angle at A.", pt('fig: x', 'We need angle P A D')),
      L("[short pause] Where do we start? With the square. We need its equal sides and its ninety-degree corners. P is not "
        "the point where the diagonals meet, so we can't treat it as the centre, and we won't use the diagonals.",
        show(f6g61['line'], 'Where do we start')),
      L("All the sides are equal, so let's mark all four with the same little line. And all the angles are ninety. I'll "
        "mark the two that sit next to the angle we want, at B and at A. We may need them.",
        show(f6g61['sq'], 'mark all four with the same little line'), show(f6g61['r90'], "I'll mark the two")),
      L("Done with the square. The next given, B P C is equilateral. In an equilateral triangle all three sides are "
        "equal, B C, P C and B P. B C already has the mark, so P C and B P get the same mark. That's the catch in this "
        "question. The sides of the triangle are equal to the sides of the square. And all the angles of the triangle are "
        "sixty.", show(f6g61['eqs'], 'get the same mark'), show(f6g61['e60'], 'And all the angles of the triangle')),
      L("Now look at the triangle that holds the angle at A, triangle A B P. Two of its sides have the mark, B A and B P. "
        "So it's isosceles. If we hadn't marked the sides, we might not have noticed that.",
        show(f6g61['abp'], 'Now look at the triangle that holds'))),
    SM('Mark the givens', 'The triangle ABP',
      L("Here's triangle A B P on its own, bigger. In an isosceles triangle, the angles across from the equal sides are "
        "equal. So angle B A P and angle B P A are equal. Let's call both of them alpha.",
        show(f6g61b['line'], "Here's triangle A B P on its own"), show(f6g61b['alpha'], 'call both of them alpha')),
      L("The corner of the square at B is ninety, and the equilateral triangle takes sixty of it, angle P B C. So the angle "
        "at B, the top of this triangle, is ninety minus sixty, which is thirty.", show(f6g61r[0], 'is ninety minus sixty'),
        show(f6g61b['b30'], 'which is thirty')),
      L("The angles of a triangle add up to one hundred eighty. So thirty plus alpha plus alpha is one hundred eighty.",
        show(f6g61r[1], 'So thirty plus alpha')),
      L("Subtract thirty from both sides, and two alpha is one hundred fifty. Divide by two, so alpha is seventy-five.",
        show(f6g61r[2], 'Subtract thirty from both sides'), show(f6g61r[3], 'Divide by two'), show(f6g61b['v75'], 'so alpha is seventy-five')),
      L("Careful. Seventy-five is angle B A P, and seventy-five is choice number four. But the question asks for angle P A "
        "D. Angle B A P and angle P A D together fill the square's corner at A, which is ninety. So angle P A D is ninety "
        "minus seventy-five, which is fifteen. Choice number one is our answer. [pause] Okay. I'll see you in the next "
        "question.", mk('cross', 'choice 4', 'seventy-five is choice number four'), show(f6g61r[4], 'So angle P A D is ninety'),
        show(f6g61b['x'], 'which is fifteen'), mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g062 (Hebrew: the deltoid's area)
# Hebrew (geo 2695-2743): the area formula (product of the diagonals over 2); what's given is a part of each diagonal;
# a deltoid = two isosceles triangles; in an isosceles triangle the height is also a median and a bisector, so the main
# diagonal is perpendicular to the other one and cuts it in half (BO = OD; not AO = OC); triangle ADO is right-angled ->
# a Pythagorean triple; the area, cancel first; other ways: the two isosceles triangles, or four right triangles.
# English numbers: 17, 15, 12 -> AO = 8 (8, 15, 17; Pythagoras with a difference of squares for who doesn't know the
# triple - topic 4 comes earlier in the study plan), area 300.
# V3: the two isosceles triangles tinted in turn with their ticks; the right angle at O; OD written; then a new slide
# with the right triangle AOD tinted inside the copy, the rest dimmed and AOD enlarged with the same labels and tint;
# AO written on both; the area written. Other ways: the two halves tinted with their areas.
f6A2, f6B2, f6C2, f6D2, f6O2 = (320.0, 47.27), (160.73, 113.64), (320.0, 312.73), (479.27, 113.64), (320.0, 113.64)
f6g62base = (f6_poly([f6A2, f6B2, f6C2, f6D2]) + [f6_seg(f6A2, f6C2), f6_seg(f6B2, f6D2),
             f6_name(f6A2, 'A', 0, -20), f6_name(f6B2, 'B', -20, 0), f6_name(f6C2, 'C', 0, 22), f6_name(f6D2, 'D', 20, 0),
             f6_name(f6O2, 'O', 16, -16), ('txt', 411, 66, '17', 'ink', 22), ('txt', 240, 134, '15', 'ink', 22), ('txt', 300, 213, '12', 'ink', 22)])
# 2026-10-18 (batch C #234): main diagonal AC / other diagonal BD (AC = 20 is the SHORTER one here); "AO = OC" is not
# assumed (not "AO is not OC"); the Pythagoras route is written, and the square-minus-square shortcut is taught here
# (identities come later in the plan): why, two checks, the trap; the whole kite comes back for the area
f6g62 = GEO('f6g62', [
    ('line', f6g62base),
    ('need', [('seg', f6A2[0], f6A2[1], f6O2[0], f6O2[1], 'red', 6), ('txt', 300, 80, '?', 'red', 26),
              ('seg', f6O2[0], f6O2[1], f6D2[0], f6D2[1], 'red', 6), ('txt', 400, 134, '?', 'red', 26)]),
    ('abd', [('tint', [f6A2, f6B2, f6D2], 'teal'), ('tick', *f6A2, *f6B2, 1), ('tick', *f6A2, *f6D2, 1)]),
    ('dcb', [('tint', [f6D2, f6C2, f6B2], 'orange'), ('tick', *f6B2, *f6C2, 2, 'orange'), ('tick', *f6D2, *f6C2, 2, 'orange')]),
    ('perp', [('right', f6O2[0], f6O2[1], 0, 270, 14)]),
    ('od', [('tick', *f6B2, *f6O2, 1, 'red'), ('tick', *f6O2, *f6D2, 1, 'red'), ('txt', 400, 134, '15', 'teal', 22)]),
], vb='130 20 380 310', w=300, title='Deltoid ABCD with its diagonals')
_R(f5_pin(f6g62), 200)
f6zs = 1.5
def f6zz(p): return (40 + (p[0] - 320) * f6zs, 40 + (p[1] - 47.27) * f6zs)
f6zA, f6zO, f6zD = f6zz(f6A2), f6zz(f6O2), f6zz(f6D2)
f6g62b = GEO('f6g62b', [
    ('line', [('tint', [f6zA, f6zO, f6zD], 'teal'), ('path', [f6zA, f6zO, f6zD, f6zA], 'teal', 6), ('right', f6zO[0], f6zO[1], 0, 90, 18),
              f6_name(f6zA, 'A', -18, -12), f6_name(f6zO, 'O', -20, 18), f6_name(f6zD, 'D', 20, 14),
              ('txt', (f6zO[0] + f6zD[0]) / 2, f6zO[1] + 26, '15', 'ink', 24), ('txt', (f6zA[0] + f6zD[0]) / 2 + 22, (f6zA[1] + f6zD[1]) / 2 - 14, '17', 'ink', 24)]),
    ('ao', [('txt', f6zA[0] - 22, (f6zA[1] + f6zO[1]) / 2, '8', 'red', 28)]),
], vb='5 5 290 180', w=220, title='The right triangle AOD, enlarged')
_R(f5_pin(f6g62b), 200)
f6g62w = GEO('f6g62w', [
    ('line', f6g62base + [('right', f6O2[0], f6O2[1], 0, 270, 14), ('txt', 400, 134, '15', 'ink', 22), ('txt', 304, 80, '8', 'ink', 22)]),
    ('whole', [('tint', [f6A2, f6B2, f6C2, f6D2], 'teal')] + f6_poly([f6A2, f6B2, f6C2, f6D2], 'teal', 5)),
    ('ac', [('seg', *f6A2, *f6C2, 'orange', 5)]),
    ('bd', [('seg', *f6B2, *f6D2, 'red', 5)]),
], vb='130 20 380 310', w=300, title='The whole deltoid')
_R(f5_pin(f6g62w), 200)
f6g62c = GEO('f6g62c', [
    ('line', f6g62base + [('right', f6O2[0], f6O2[1], 0, 270, 14), ('txt', 400, 134, '15', 'ink', 22), ('txt', 304, 80, '8', 'ink', 22)]),
    ('t1', [('tint', [f6A2, f6B2, f6D2], 'teal'), ('seg', *f6A2, *f6O2, 'teal', 5)]),
    ('t2', [('tint', [f6D2, f6C2, f6B2], 'orange'), ('seg', *f6O2, *f6C2, 'orange', 5)]),
    ('four', [('dim', 130, 20, 380, 310)] + f6g62base + [('seg', f6A2[0], f6A2[1], f6C2[0], f6C2[1], 'red', 4), ('seg', f6B2[0], f6B2[1], f6D2[0], f6D2[1], 'red', 4),
              ('tint', [f6A2, f6O2, f6B2], 'teal'), ('tint', [f6A2, f6O2, f6D2], 'teal'), ('tint', [f6C2, f6O2, f6B2], 'orange'), ('tint', [f6C2, f6O2, f6D2], 'orange')]),
], vb='130 20 380 310', w=300, title='Other ways to the same area')
_R(f5_pin(f6g62c), 200)
_f6r = lambda pre, rows, size=26: [IH('%s%d' % (pre, i), t, size=size) if t.startswith('$') else I('%s%d' % (pre, i), t, size=size - 2) for i, t in enumerate(rows)]
f6r1 = _f6r('f6r1_', ['$S=\\frac{AC\\cdot BD}{2}$', '$AC\\perp BD$', '$BO=OD=15$', '$AO=OC$?', 'not given'])
f6r2 = _f6r('f6r2_', ['$8,\\ 15,\\ 17$', '$AO^2=17^2-15^2$', '$=(17-15)(17+15)$'])
f6r3 = _f6r('f6r3_', ['$(a-b)(a+b)$', '$=a^2+ab-ab-b^2$', '$=a^2-b^2$', '$5^2-3^2=25-9=16$', '$(5-3)(5+3)=2\\cdot8=16$'], 30)
f6r3b = _f6r('f6r3b', ['$4^2-1^2=15$', '$(4-1)(4+1)=15$', '$(17-15)^2=4$ ✗', '$2\\cdot32=64$', '$AO=\\sqrt{64}=8$'], 30)
f6r4 = _f6r('f6r4_', ['$AC=8+12=20$', '$BD=15+15=30$', '$S=\\frac{20\\cdot30}{2}$', '$\\frac{30}{2}=15$', '$20\\cdot15=300$'])
f6r5 = _f6r('f6r5_', ['$ABD:\\ \\frac{30\\cdot8}{2}=120$', '$CBD:\\ \\frac{30\\cdot12}{2}=180$', '$120+180=300$',
                     '$2\\cdot\\frac{15\\cdot8}{2}=120$', '$2\\cdot\\frac{15\\cdot12}{2}=180$'], 24)
for _rows, _x0 in ((f6r1, 1350), (f6r4, 1350), (f6r5, 1350)):
    for _k, _x in enumerate(_rows): _R(_x, 200 + 56 * _k, x=_x0)
for _k, _x in enumerate(f6r2): _R(_x, 200 + 60 * _k, x=1270)
for _k, _x in enumerate(f6r3): _R(_x, 222 + 62 * _k, x=420)
for _k, _x in enumerate(f6r3b): _R(_x, 222 + 62 * _k, x=1000)
NOFIG32.add(('solve-geo32-g062', 2))
video('solve-geo32-g062', 'solution', qid='geo32-g062', slides=[
    SM('The main diagonal', 'The main diagonal',
      L("A B C D is a deltoid, and its diagonals meet at O. Given: A B and A D are seventeen centimeters, C B equals C D, "
        "B O is fifteen centimeters, and O C is twelve centimeters. What is the area of the deltoid, in square centimeters?",
        pt('stem', 'A B C D is a deltoid', 'hl', 11.0), voice='calm', pause=0.5),
      L("We learned how to find the area of a deltoid. The product of the diagonals, over two. [short pause] But only "
        "parts of the diagonals are given, so first we'll find the missing parts.", show(f6g62['line'], 'We learned how'),
        show(f6r1[0], 'The product of the diagonals')),
      L("[short pause] On the main diagonal, A C, we know O C, twelve, and we need A O. On the other diagonal, B D, we know "
        "B O, fifteen, and we need O D.", show(f6g62['need'], 'we need A O')),
      L("Let's remember what a deltoid is. It's a quadrilateral made of two isosceles triangles. Triangle A B D is "
        "isosceles, because A D equals A B. And triangle D C B is isosceles too, because C B equals C D.",
        show(f6g62['abd'], 'Triangle A B D is'), show(f6g62['dcb'], 'And triangle D C B')),
      L("In an isosceles triangle, the height from the top is also a median and an angle bisector. So the main diagonal A "
        "C is perpendicular to the other diagonal, B D. It cuts the angles in half, and it cuts B D in half. So B O equals "
        "O D. B O is fifteen, so O D is fifteen too.", show(f6g62['perp'], 'is perpendicular to the other diagonal'),
        show(f6r1[1], 'It cuts the angles in half'), show(f6g62['od'], 'So B O equals'), show(f6r1[2], 'so O D is fifteen too')),
      L("But careful, not the other way around. We cannot assume that A O equals O C. The main diagonal cuts B D in half, "
        "but B D doesn't have to cut A C in half. So we still need to find A O.", show(f6r1[3], 'We cannot assume'), show(f6r1[4], 'So we still need to find A O'))),
    SM('The main diagonal', 'Pythagoras',
      L("The diagonals are perpendicular, so triangle A O D is a right triangle. Its hypotenuse A D is seventeen, and its "
        "leg O D is fifteen. Here it is on its own.", show(f6g62b['line'], 'Here it is on its own')),
      L("If you know the triple eight, fifteen, seventeen, you see it at once. The other leg is eight.",
        show(f6r2[0], 'If you know the triple'), show(f6g62b['ao'], 'The other leg is eight')),
      L("If not, use Pythagoras. A O squared is seventeen squared minus fifteen squared.", show(f6r2[1], 'A O squared is')),
      L("There's a shortcut for a square minus a square. Seventeen squared minus fifteen squared is the product of "
        "seventeen minus fifteen and seventeen plus fifteen.", show(f6r2[2], 'Seventeen squared minus fifteen squared is'))),
    SM('The main diagonal', 'A square minus a square',
      L("Why does that work? Multiply out the product of a minus b and a plus b. We get a squared, plus a b, minus a b, minus b "
        "squared. The two middle terms cancel, and we're left with a squared minus b squared.",
        show(f6r3[0], 'Multiply out the product'), show(f6r3[1], 'We get a squared'), show(f6r3[2], "we're left with")),
      L("Let's check it with small numbers. Five squared minus three squared is twenty-five minus nine. That's sixteen. And "
        "the product of five minus three and five plus three is two times eight. That's sixteen too.", show(f6r3[3], 'Five squared minus three squared'),
        show(f6r3[4], 'the product of five minus three')),
      L("Let's do one more. Four squared minus one squared is sixteen minus one. That's fifteen. And the product "
        "of four minus one and four plus one is three times five. That's fifteen.", show(f6r3b[0], 'Four squared minus one squared'), show(f6r3b[1], 'of four minus one')),
      L("Careful, it works only for a square minus a square. It's not seventeen minus fifteen, squared. That would be only "
        "four.", show(f6r3b[2], "It's not seventeen minus fifteen")),
      L("So here, seventeen minus fifteen is two. And seventeen plus fifteen is thirty-two. Two times thirty-two is "
        "sixty-four, and the root of sixty-four is eight. So A O is eight, just like the triple.",
        show(f6r3b[3], 'Two times thirty-two'), show(f6r3b[4], 'the root of sixty-four'))),
    SM('The main diagonal', 'The area',
      L("Now back to the whole deltoid. In this kite, A O is eight and O C is twelve, so they really are different. The "
        "main diagonal A C is eight plus twelve, which is twenty. B D is fifteen plus fifteen, which is thirty.",
        show(f6g62w['line'], 'Now back to the whole deltoid'), show(f6g62w['whole'], 'Now back to the whole deltoid'),
        show(f6g62w['ac'], 'The main diagonal A C'), show(f6r4[0], 'is eight plus twelve'), show(f6g62w['bd'], 'B D is fifteen plus fifteen'),
        show(f6r4[1], 'B D is fifteen plus fifteen')),
      L("The area is twenty times thirty, over two. We could multiply first, but it's easier to cancel first.",
        show(f6r4[2], 'The area is twenty times thirty')),
      L("Thirty over two is fifteen, and twenty times fifteen is three hundred. Choice number three is our answer.",
        show(f6r4[3], 'Thirty over two is fifteen'), show(f6r4[4], 'and twenty times fifteen'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Other ways', 'Other ways',
      L("[pause] Once we've found all the pieces, there are other ways to get the area. Some students take the two "
        "isosceles triangles. Triangle A B D has base B D, thirty, and height A O, eight. Thirty times eight, over two, is "
        "one hundred twenty.", show(f6g62c['line'], 'there are other ways'), show(f6g62c['t1'], 'Triangle A B D has base'),
        show(f6r5[0], 'Thirty times eight, over two')),
      L("Triangle C B D has base thirty and height O C, twelve. Thirty times twelve, over two, is one hundred eighty. "
        "Together, one hundred twenty plus one hundred eighty is three hundred.", show(f6g62c['t2'], 'Triangle C B D has base'),
        show(f6r5[1], 'Thirty times twelve, over two'), show(f6r5[2], 'Together, one hundred twenty')),
      L("Others take four right triangles. Each small one has legs fifteen and eight, so it's sixty, and the two small ones "
        "make one hundred twenty. Each big one has legs fifteen and twelve, so it's ninety, and the two big ones make one "
        "hundred eighty. Again three hundred. Choice number three. "
        "[pause] Okay. I'll see you in the next question.", show(f6g62c['four'], 'Others take four right triangles'),
        show(f6r5[3], 'Each small one has legs'), show(f6r5[4], 'Each big one has legs'), mk('tick', 'choice 3', 'Again three hundred'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g063 (Hebrew: the isosceles trapezoid)
# Hebrew (geo 2745-2789): AB = AD -> isosceles triangle ABD, the base angles 30 and 30, A = 120; in every trapezoid the
# angles on one leg add up to 180 -> B = 60, its lower part DBC = 30 (or: our familiar Z, the bases are parallel); the
# trapezoid is isosceles -> C = B = 60; triangle BCD is 30-60-90, a gold triangle; the short leg (opposite the 30) is CD
# = AB; the hypotenuse is twice it; the perimeter. English numbers 7 -> BC = 14, P = 35. The course's bonus (ABD is the
# 30-30-120 triangle, BD = 7 root 3, matching the long leg) is kept short.
# V3: the copy built at the words; ABD tinted with its ticks and both 30s; 120 written at A; 60 at B; the Z traced for the
# second way; 60 at C; then BCD tinted orange with its right angle, CD ticked like AB, BC written when found.
f6A3, f6B3, f6C3, f6D3 = (204.68, 80.13), (89.36, 279.87), (550.64, 279.87), (435.32, 80.13)
f6g63 = GEO('f6g63', [
    ('line', f6_poly([f6A3, f6B3, f6C3, f6D3]) + [f6_seg(f6B3, f6D3),
              f6_name(f6A3, 'A', -14, -18), f6_name(f6B3, 'B', -16, 16), f6_name(f6C3, 'C', 16, 16), f6_name(f6D3, 'D', 14, -18),
              ('txt', 130, 170, '7', 'ink', 24), ('txt', 320, 62, '7', 'ink', 24), ('arc', f6B3[0], f6B3[1], 52, 30, 60, 'small', '30°', 80)]),
    ('abd', [('tint', [f6A3, f6B3, f6D3], 'teal'), ('tick', *f6A3, *f6B3, 1), ('tick', *f6A3, *f6D3, 1),
             ('arc', f6D3[0], f6D3[1], 52, 180, 210, 'small', '30°', 80)]),
    ('a120', [('arc', f6A3[0], f6A3[1], 28, 240, 360, 'orange', '120°', 50)]),
    ('b60', [('arc', f6B3[0], f6B3[1], 34, 0, 30, 'small', '30°', 56)]),
    ('z', [('path', [(330, 80.13), f6D3, f6B3, (200, 279.87)], 'teal', 7), ('arc', f6D3[0], f6D3[1], 60, 180, 210, 'red'),
           ('arc', f6B3[0], f6B3[1], 42, 0, 30, 'red')]),
    ('c60', [('arc', f6C3[0], f6C3[1], 32, 120, 180, 'small', '60°', 56)]),
    ('bcd', [('tint', [f6B3, f6C3, f6D3], 'orange'), ('right', f6D3[0], f6D3[1], 210, 300, 16)]),
    ('cd', [('tick', *f6C3, *f6D3, 1), ('txt', 512, 170, '7', 'teal', 24)]),
    ('bc', [('txt', 320, 304, '14', 'red', 26)]),
    ('p', [('dim', 55, 50, 520, 262)] + f6_poly([f6A3, f6B3, f6C3, f6D3], 'red', 5)
          + [('txt', 130, 170, '7', 'ink', 24), ('txt', 320, 62, '7', 'ink', 24), ('txt', 512, 170, '7', 'ink', 24), ('txt', 320, 304, '14', 'red', 26)]),
    ('bonus', [('seg', *f6B3, *f6D3, 'teal', 4), ('txt', 300, 196, '7√3', 'teal', 22)]),
], vb='55 50 520 262', w=300, title='Isosceles trapezoid ABCD with the diagonal BD')
_R(f5_pin(f6g63), 200)
# the gold-triangle slide: the same copy with every angle found so far (V2: the values carried over)
f6g63b = GEO('f6g63b', [
    ('line', f6_poly([f6A3, f6B3, f6C3, f6D3]) + [f6_seg(f6B3, f6D3),
              f6_name(f6A3, 'A', -14, -18), f6_name(f6B3, 'B', -16, 16), f6_name(f6C3, 'C', 16, 16), f6_name(f6D3, 'D', 14, -18),
              ('txt', 130, 170, '7', 'ink', 24), ('txt', 320, 62, '7', 'ink', 24), ('tick', *f6A3, *f6B3, 1), ('tick', *f6A3, *f6D3, 1),
              ('arc', f6B3[0], f6B3[1], 52, 30, 60, 'small', '30°', 80), ('arc', f6D3[0], f6D3[1], 52, 180, 210, 'small', '30°', 80),
              ('arc', f6A3[0], f6A3[1], 28, 240, 360, 'orange', '120°', 50), ('arc', f6B3[0], f6B3[1], 34, 0, 30, 'small', '30°', 56),
              ('arc', f6C3[0], f6C3[1], 32, 120, 180, 'small', '60°', 56)]),
    ('bcd', [('tint', [f6B3, f6C3, f6D3], 'orange'), ('right', f6D3[0], f6D3[1], 210, 300, 16)]),
    ('cd', [('tick', *f6C3, *f6D3, 1), ('txt', 512, 170, '7', 'teal', 24)]),
    ('bc', [('txt', 320, 304, '14', 'red', 26)]),
    ('p', [('dim', 55, 50, 520, 262)] + f6_poly([f6A3, f6B3, f6C3, f6D3], 'red', 5)
          + [('txt', 130, 170, '7', 'ink', 24), ('txt', 320, 62, '7', 'ink', 24), ('txt', 512, 170, '7', 'ink', 24), ('txt', 320, 304, '14', 'red', 26)]),
    ('bonus', [('seg', *f6B3, *f6D3, 'teal', 4), ('txt', 300, 196, '7√3', 'teal', 22)]),
], vb='55 50 520 262', w=300, title='Triangle BCD: a gold triangle')
_R(f5_pin(f6g63b), 200)
# 2026-10-18 (batch C #235): each step its own row, to the right of the copy
f6g63r = [IH('f6g63r%d' % i, t, size=24) for i, t in enumerate(['$30°+30°=60°$', '$\\angle A=180°-60°$', '$\\angle B=180°-120°$',
                                                               '$60°-30°=30°$', '$BC=2\\cdot7=14$', '$P=7+7+7+14$', '$=35$', '$BD=7\\sqrt3$'])]
f6g63q = [IH('f6g63q%d' % i, t, size=24) for i, t in enumerate(['$=120°$', '$=60°$'])]
for _k, _x in enumerate([f6g63r[0], f6g63r[1], f6g63q[0], f6g63r[2], f6g63q[1], f6g63r[3]]): _R(_x, 200 + 50 * _k, x=1350)
for _k, _x in enumerate(f6g63r[4:]): _R(_x, 200 + 54 * _k, x=1350)
video('solve-geo32-g063', 'solution', qid='geo32-g063', slides=[
    SM('Angles, then the gold triangle', 'Angles, then the gold triangle',
      L("A B C D is an isosceles trapezoid, with A D parallel to B C. Given: A B and A D are seven centimeters, and angle A "
        "B D is thirty degrees. What is its perimeter, in centimeters?", pt('stem', 'A B C D is an isosceles trapezoid', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("The perimeter is the sum of the four sides. Three of them are given, A B, A D, and C D, which equals A B because the "
        "trapezoid is isosceles. [short pause] We need the fourth side, B C.", show(f6g63['line'], 'The perimeter is the sum')),
      L("[short pause] Start with the first given. A B equals A D, so triangle A B D is isosceles. In an isosceles triangle "
        "the base angles are equal. Angle A B D is thirty, so angle A D B is thirty too.", show(f6g63['abd'], 'so triangle A B D is isosceles')),
      L("The two base angles of this triangle add up to sixty degrees. So the top angle, A, is one hundred eighty minus "
        "sixty, which is one hundred twenty.", show(f6g63r[0], 'add up to sixty degrees'), show(f6g63r[1], 'So the top angle'),
        show(f6g63q[0], 'which is one hundred twenty'), show(f6g63['a120'], 'one hundred twenty.')),
      L("In every trapezoid, the two angles on the same leg add up to one hundred eighty. A is one hundred twenty, so all "
        "of angle B is sixty. Its lower part, angle D B C, is sixty minus thirty, which is thirty.",
        show(f6g63r[2], 'A is one hundred twenty, so'), show(f6g63q[1], 'so all of angle B is sixty'), show(f6g63r[3], 'Its lower part'),
        show(f6g63['b60'], 'which is thirty')),
      L("Another way to see the thirty is our familiar Z. A D and B C are the parallel bases, and B D crosses them. So the "
        "angles in the two corners of the Z, angle A D B and angle D B C, are equal. Thirty and thirty.",
        show(f6g63['z'], 'our familiar Z')),
      L("The trapezoid is isosceles, so the two angles on the bottom base are equal. Angle C equals angle B, sixty. And "
        "because this trapezoid is isosceles, its opposite angles add up to one hundred eighty, so angle C also completes "
        "angle A to one hundred eighty.", show(f6g63['c60'], 'Angle C equals angle B')),
    ),
    SM('Angles, then the gold triangle', 'The gold triangle',
      L("What did we get? Triangle B C D has thirty and sixty, together ninety. So the angle at D completes it to one "
        "hundred eighty, and it's ninety. It's not just a right triangle. It's a gold triangle, thirty, sixty, ninety.",
        show(f6g63b['line'], 'What did we get'), show(f6g63b['bcd'], 'Triangle B C D has thirty and sixty')),
      L("Its short leg is the one across from the thirty, C D. The trapezoid is isosceles, so C D equals A B, seven.",
        show(f6g63b['cd'], 'so C D equals A B')),
      L("When we know the short leg, the hypotenuse is easy. It's exactly twice the short leg. So B C is two times seven, "
        "fourteen.", show(f6g63r[4], 'So B C is two times seven'), show(f6g63b['bc'], 'fourteen.')),
      L("Now the perimeter, all four outer sides. Seven plus seven plus seven plus fourteen is thirty-five. Choice number "
        "two is our answer.", show(f6g63b['p'], 'Now the perimeter'), show(f6g63r[5], 'Seven plus seven plus seven'),
        show(f6g63r[6], 'is thirty-five'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("One more link. Triangle A B D has angles thirty, thirty and one hundred twenty, the triangle we met with the "
        "special triangles. So B D is seven root three. That matches the gold triangle, where the long leg is the short "
        "leg times root three. [pause] Okay. I'll see you in the next question.", show(f6g63b['bonus'], 'So B D is seven root three'),
        show(f6g63r[7], 'That matches the gold triangle'))),
])

# ------------------------------------------------------------------------------------------------ geo-065 (lesson: the advanced level)
# Hebrew (geo 2794-2799): the last lesson learned the rules and basic questions; now harder psychometric questions and
# nuances that come back now and then; start with a sample question. The course's "what's ahead" lines are kept, each
# taught in the questions that follow.
f6h1 = I('f6h1', 'Which shape is also which? $\\ $Read the definitions', size=32)
f6h2 = I('f6h2', 'Areas: symmetry and equal heights', size=32)
f6h3 = I('f6h3', 'Angles with letters: $\\ $plug in numbers', size=32)
video('geo-065', 'lesson', slides=[
    S('Advanced Quadrilaterals',
      L("Now let's try harder quadrilateral questions. In the last lesson we learned the rules of the quadrilaterals and "
        "practiced basic questions.")),
    S("What's ahead",
      L("In this lesson we'll practice harder exam questions, and meet a few small points that come back on the exam "
        "every now and then."),
      L("There are questions about which shape is also which, and they're solved by reading the definitions carefully.",
        show(f6h1, 'which shape is also which')),
      L("There are area questions where an idea, like symmetry or an equal height, helps us see the answer.",
        show(f6h2, 'There are area questions')),
      L("And there are angle questions full of letters, where plugging in numbers helps. We'll use the math way, "
        "understanding, and plugging in numbers, each where it helps. Let's start with a sample question. [pause] Okay. "
        "I'll see you in the next video.", show(f6h3, 'And there are angle questions'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g066 (Hebrew: which statement is not necessarily true)
# Hebrew (geo 2801-2861): statement by statement, eliminate whatever is surely true, hope to be left with one; "every X is
# a Y" = X has all the properties of Y (not the other way round); rectangle -> parallelogram, rhombus -> deltoid (two
# isosceles triangles on the short diagonal; a deltoid with equal sides IS a rhombus), square -> rectangle (an upgraded
# rectangle); three eliminated -> on the exam mark the fourth without checking; in the lesson we check it. English order
# and the last statement differ (perpendicular diagonals: a rhombus property; a 9 by 4 rectangle as the counterexample).
# V3 (general properties on clean generic shapes): one panel per statement, built as it is discussed; the shared property
# in the same tint on both shapes; the counterexample's diagonals with their angle in red.
def f6P(x, y, pts): return [(x + a, y + b) for a, b in pts]
f6rh = f6P(30, 30, [(110, 0), (40, 70), (110, 140), (180, 70)])          # rhombus (diagonal BD horizontal)
f6ki = f6P(250, 30, [(80, 0), (20, 50), (80, 160), (140, 50)])            # deltoid
f6sq = f6P(40, 230, [(0, 0), (0, 120), (120, 120), (120, 0)])             # square
f6re = f6P(230, 230, [(0, 0), (0, 120), (190, 120), (190, 0)])            # rectangle
f6re2 = f6P(460, 230, [(0, 0), (0, 120), (190, 120), (190, 0)])           # rectangle (statement 3)
f6pa = f6P(470, 30, [(40, 0), (0, 120), (160, 120), (200, 0)])            # parallelogram
f6r9 = f6P(720, 120, [(0, 0), (0, 120), (270, 120), (270, 0)])            # the 9 by 4 rectangle
f6g66 = GEO('f6g66', [
    ('line', [('txt', 300, 14, ' ', 'ink', 10)]),
    # 2026-10-18 (batch C #237): the kite by its definition (two pairs of equal sides next to each other), checked directly
    # on the rhombus; no "short diagonal" in the definition
    ('p1', f6_poly(f6rh) + [('tick', *f6rh[k], *f6rh[(k + 1) % 4]) for k in range(4)]
           + [('path', [f6rh[1], f6rh[0], f6rh[3]], 'teal', 6), ('path', [f6rh[1], f6rh[2], f6rh[3]], 'orange', 6), ('txt', 140, 196, 'rhombus', 'ink', 22)]),
    ('p1k', f6_poly(f6ki) + [('tick', *f6ki[0], *f6ki[1], 1), ('tick', *f6ki[0], *f6ki[3], 1), ('tick', *f6ki[1], *f6ki[2], 2, 'orange'),
                             ('tick', *f6ki[3], *f6ki[2], 2, 'orange'), ('path', [f6ki[1], f6ki[0], f6ki[3]], 'teal', 6),
                             ('path', [f6ki[1], f6ki[2], f6ki[3]], 'orange', 6), ('txt', 330, 214, 'deltoid', 'ink', 22)]),
    ('p2', f6_poly(f6sq) + [('right', *f6sq[k], a1, a2, 14) for k, (a1, a2) in enumerate([(270, 0), (0, 90), (90, 180), (180, 270)])]
           + [('tick', *f6sq[k], *f6sq[(k + 1) % 4]) for k in range(4)] + [('txt', 100, 380, 'square', 'ink', 22)]),
    ('p2r', f6_poly(f6re) + [('right', *f6re[k], a1, a2, 14) for k, (a1, a2) in enumerate([(270, 0), (0, 90), (90, 180), (180, 270)])]
            + [('txt', 325, 380, 'rectangle', 'ink', 22)]),
    ('p3', f6_poly(f6pa) + [('par', *f6pa[1], *f6pa[2], 1), ('par', *f6pa[0], *f6pa[3], 1), ('par', *f6pa[0], *f6pa[1], 2), ('par', *f6pa[3], *f6pa[2], 2),
                            ('txt', 570, 180, 'parallelogram', 'ink', 22)]
           + f6_poly(f6re2) + [('par', *f6re2[1], *f6re2[2], 1), ('par', *f6re2[0], *f6re2[3], 1), ('par', *f6re2[0], *f6re2[1], 2),
                               ('par', *f6re2[3], *f6re2[2], 2), ('txt', 555, 380, 'rectangle', 'ink', 22)]),
    ('p4', f6_poly(f6r9) + [f6_seg(f6r9[0], f6r9[2], 'red', 3), f6_seg(f6r9[1], f6r9[3], 'red', 3),
                            ('txt', 855, 262, '9', 'ink', 24), ('txt', 702, 180, '4', 'ink', 24), ('txt', 855, 100, 'not 90°', 'red', 24)]),
], vb='0 0 1010 400', w=960, col=0, title='Quadrilateral families')
for _it in f6g66.values(): _it['_x'] = 420; _it['_y'] = 175     # no question figure: the panels get the wide board under the stem
video('solve-geo32-g066', 'solution', qid='geo32-g066', slides=[
    SM('Statement by statement', 'Statement by statement',
      L("Which of the following statements is not necessarily true?", pt('stem', 'Which of the following', 'hl', 4.0),
        voice='calm', pause=0.5),
      L("Four statements, and one of them is not necessarily true. That means it can fail for some shape. [short pause] So "
        "we go statement by statement. Anything that's surely true, we cross out, and we hope to be left with one.",
        show(f6g66['line'], 'we go statement by statement')),
      L("[short pause] Statement one, every rhombus is a deltoid. What does that mean? Every rhombus has everything a "
        "deltoid is guaranteed to have. A deltoid has two pairs of equal sides, and in each pair the equal sides are next "
        "to each other.", show(f6g66['p1k'], 'A deltoid has two pairs')),
      L("A rhombus has all four sides equal. So the two top sides are equal and next to each other, and so are the two "
        "bottom sides. That's two pairs, so every rhombus is a deltoid. It's true, so choice number one is out. Not every "
        "deltoid is a rhombus, by the way. But a deltoid with all four sides equal is a rhombus.",
        show(f6g66['p1'], 'A rhombus has all four sides equal'), mk('cross', 'choice 1', "so choice number one is out")),
      L("Statement two, every square is a rectangle. A rectangle has its opposite sides equal and all its angles ninety. A "
        "square has all that, and more, because all its sides are equal. It's like an upgraded rectangle. So it's true, and "
        "choice number two is out. Not every rectangle is a square, because its sides don't have to be all equal.",
        show(f6g66['p2r'], 'A rectangle has its opposite sides'), show(f6g66['p2'], 'A square has all that'),
        mk('cross', 'choice 2', 'and choice number two is out')),
      L("Statement three, every rectangle is a parallelogram. A parallelogram has its opposite sides equal and parallel, "
        "its opposite angles equal, and neighbouring angles that add up to one hundred eighty. A rectangle has all of these. "
        "So it's true, and choice number three is out. The other way around isn't true, because not every parallelogram "
        "has four right angles.", show(f6g66['p3'], 'A parallelogram has its opposite sides'),
        mk('cross', 'choice 3', 'and choice number three is out')),
      L("Three statements are out. On the exam, you'd mark choice number four without checking it. Since we're in a lesson, "
        "let's check it anyway. Every parallelogram has perpendicular diagonals."),
      L("Perpendicular diagonals are a property of the rhombus, and not every parallelogram has them. Take a rectangle, "
        "nine by four. It's a parallelogram. If its diagonals were perpendicular, it would be a rhombus, and a rectangle "
        "that's a rhombus is a square. This one is not a square, so its diagonals are not perpendicular. One shape where it "
        "fails is enough, so this statement is not necessarily true. Choice number four is our answer. [pause] Okay. I'll see you in the next "
        "question.", show(f6g66['p4'], 'Take a rectangle'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g067 (Hebrew: two corner areas)
# Hebrew (geo 2862-2950): two ways. The math way: ABE is a right triangle (every angle of a rectangle is 90), legs not
# given -> letters: AB = h (the rectangle's height), AE = x; xh / 2 = 3 (English 6) -> xh = 6 (12); ECD: same height h, a
# new part y; yh = 18 (30); the shaded triangle: base x + y, height h (drop it from E: the rectangle's height); open the
# brackets; 12 (21); "the long and tiring solution" but the base is our anchor when we don't see the short way. Then the
# psychometric way: symmetry - drop a height from E, two rectangles, a diagonal cuts a rectangle into two equal halves,
# so the shaded parts are 3 and 9 (6 and 15); easy-plus = question 5 or 6. Her generalization is the next lesson
# (geo-067-after, "Equal Heights, Equal Halves").
# V3: method 1 - each letter written on its segment as it is defined (h orange, x and y teal), each triangle tinted as its
# area is used, the shaded triangle's height dashed from E; method 2 (new copy, from the givens): E pointed at first, then
# the dashed height EF, the two rectangles outlined in turn, each diagonal half tinted with its area.
f6A7, f6B7, f6C7, f6D7, f6E7, f6F7 = (101.0, 82.67), (101.0, 277.33), (539.0, 277.33), (539.0, 82.67), (222.67, 82.67), (222.67, 277.33)
f6g67base = (f6_poly([f6A7, f6B7, f6C7, f6D7]) + [f6_seg(f6E7, f6B7), f6_seg(f6E7, f6C7),
             f6_name(f6A7, 'A', -16, -16), f6_name(f6B7, 'B', -16, 18), f6_name(f6C7, 'C', 16, 18), f6_name(f6D7, 'D', 16, -16),
             f6_name(f6E7, 'E', 0, -22), ('txt', 140, 140, '6', 'ink', 24), ('txt', 440, 140, '15', 'ink', 24)])
f6g67 = GEO('f6g67', [
    ('line', f6g67base),
    ('abe', [('tint', [f6A7, f6B7, f6E7], 'teal'), ('right', f6A7[0], f6A7[1], 270, 0, 16)]),
    ('h', [('seg', f6A7[0], f6A7[1], f6B7[0], f6B7[1], 'orange', 6), ('txt', 78, 180, 'h', 'orange', 28, True)]),
    ('x', [('seg', f6A7[0], f6A7[1], f6E7[0], f6E7[1], 'teal', 6), ('txt', 162, 60, 'x', 'teal', 28, True)]),
    ('y', [('tint', [f6E7, f6C7, f6D7], 'orange'), ('seg', f6E7[0], f6E7[1], f6D7[0], f6D7[1], 'teal', 6), ('txt', 380, 60, 'y', 'teal', 28, True)]),
    # 2026-10-18 (batch C #238): the corner tints fade, and the shaded triangle EBC is the one in focus for its formula
    ('ebc', [('dim', 40, 30, 560, 300)] + f6g67base + [('tint', [f6E7, f6B7, f6C7], 'red')]),
    ('base', [('seg', f6B7[0], f6B7[1], f6C7[0], f6C7[1], 'red', 6), ('txt', 320, 300, 'x + y', 'red', 26, True)]),
    ('ht', [('dot', *f6E7), f6_seg(f6E7, f6F7, 'orange', 3, True), ('right', f6F7[0], f6F7[1], 0, 90, 14), ('txt', 240, 220, 'h', 'orange', 28, True)]),
], vb='40 30 560 300', w=300, title='Rectangle ABCD with E on AD')
f6g67b = GEO('f6g67b', [
    ('line', f6g67base),
    ('e', [('dot', *f6E7), ('seg', f6E7[0], f6E7[1], f6F7[0], f6F7[1], 'teal', 3, True), ('right', f6F7[0], f6F7[1], 0, 90, 14),
           f6_name(f6F7, 'F', 0, 24)]),
    ('left', [('path', [f6A7, f6B7, f6F7, f6E7, f6A7], 'teal', 6)]),
    ('l6', [('tint', [f6E7, f6B7, f6F7], 'teal'), ('txt', 196, 240, '6', 'teal', 26)]),
    ('right', [('path', [f6E7, f6F7, f6C7, f6D7, f6E7], 'orange', 6)]),
    ('r15', [('tint', [f6E7, f6F7, f6C7], 'orange'), ('txt', 300, 250, '15', 'orange', 26)]),
], vb='40 30 560 300', w=300, title='Drop the height from E')
for _g in (f6g67, f6g67b): _R(f5_pin(_g), 200)
f6g67r = _f6r('f6g67r', ['$\\frac{x\\cdot h}{2}=6$', '$xh=12$', '$\\frac{y\\cdot h}{2}=15$', '$yh=30$'])
f6g67s = _f6r('f6g67s', ['$S=\\frac{(x+y)\\cdot h}{2}$', '$=\\frac{xh+yh}{2}$', '$=\\frac{12+30}{2}$', '$=\\frac{42}{2}=21$'])
f6g67t = _f6r('f6g67t', ['$S_{EBF}=6$', '$S_{EFC}=15$', '$6+15=21$'])
for _k, _x in enumerate(f6g67r): _R(_x, 372 + 54 * _k)
for _k, _x in enumerate(f6g67s): _R(_x, 200 + 62 * _k, x=1350)
for _k, _x in enumerate(f6g67t): _R(_x, 200 + 56 * _k, x=1350)
video('solve-geo32-g067', 'solution', qid='geo32-g067', slides=[
    SM('Method 1 · The math way', 'Letters for the sides',
      L("A B C D is a rectangle, and E lies on A D. The areas of triangles A B E and E C D are six square centimeters and "
        "fifteen square centimeters. What is the area of the shaded triangle E B C, in square centimeters?",
        pt('stem', 'A B C D is a rectangle', 'hl', 10.0), voice='calm', pause=0.5),
      L("We know the two white corner triangles and need the shaded one in the middle. [short pause] We'll solve it in two "
        "different ways. First the math way with letters, and then by understanding, with symmetry.",
        pt('fig: shaded', 'need the shaded one')),
      L("[short pause] Start with triangle A B E. It's a right triangle, because every angle of a rectangle is ninety. So "
        "its area is leg times leg, over two. But neither leg is given, so we give them letters.",
        show(f6g67['line'], 'Start with triangle A B E'), show(f6g67['abe'], "It's a right triangle")),
      L("A B is the height of the rectangle. Let's call it h. A E is a part of the rectangle's length. Let's call it x. So x "
        "times h, over two, is six. Multiply both sides by two, to get rid of the over two, and x h is twelve.", show(f6g67['h'], "Let's call it h"),
        show(f6g67['x'], "Let's call it x"), show(f6g67r[0], 'So x times h, over two'), show(f6g67r[1], 'and x h is twelve')),
      L("Now triangle E C D. It's a right triangle too, with the same height h. E D is another part of the length, not x. So "
        "it's a new unknown, y. y times h, over two, is fifteen, so y h is thirty.", show(f6g67['y'], "So it's a new unknown"),
        show(f6g67r[2], 'y times h, over two'), show(f6g67r[3], 'so y h is thirty')),
      L("Now the shaded triangle E B C. Its base, B C, is the whole length, x plus y. And its height? We drop it from E to B "
        "C, and it's exactly the height of the rectangle, h.", show(f6g67['ebc'], 'Now the shaded triangle'),
        show(f6g67['base'], 'Its base, B C'), show(f6g67['ht'], 'We drop it from E')),
      L("So its area is x plus y, times h, over two. Open the brackets on top. We get x h plus y h, and both products are "
        "still over two.", show(f6g67s[0], 'So its area is'), show(f6g67s[1], 'We get x h plus y h')),
      L("We found that x h is twelve and y h is thirty, so it's twelve plus thirty, over two. That's forty-two over two, "
        "which is twenty-one. Choice number two is our answer.", show(f6g67s[2], 'so it\'s twelve plus thirty'),
        show(f6g67s[3], "That's forty-two over two"), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("The math way works even when we don't see a shortcut, so it's a solid base.")),
    SM('Method 2 · Understanding: symmetry', 'Symmetry',
      L("[pause] Now by understanding, with symmetry. Symmetry is a very important tool in geometry, especially in "
        "quadrilaterals. From the point E, let's drop a height down to B C, and call its foot F.",
        show(f6g67b['line'], 'Now by understanding'), show(f6g67b['e'], 'From the point E')),
      L("Now we have a rectangle on the left, A B F E. Its diagonal E B cuts it into two triangles. A diagonal cuts a "
        "rectangle into two triangles with the same area. So the shaded triangle E B F is six, like the white triangle A B "
        "E.", show(f6g67b['left'], 'Now we have a rectangle on the left'), show(f6g67b['l6'], 'So the shaded triangle E B F'),
        show(f6g67t[0], 'is six, like the white')),
      L("The same on the right. E F C D is a rectangle, its diagonal is E C, and the white triangle E C D is fifteen. So the "
        "shaded triangle E F C is fifteen too.", show(f6g67b['right'], 'The same on the right'),
        show(f6g67b['r15'], 'So the shaded triangle E F C'), show(f6g67t[1], 'is fifteen too')),
      L("So the shaded area is equal to the two white areas together, six plus fifteen, which is twenty-one. Choice number "
        "two.", show(f6g67t[2], 'six plus fifteen'), mk('tick', 'choice 2', 'Choice number two')),
      L("The reason is that each small rectangle is split into two equal areas by its diagonal. This idea is very "
        "important, and in the next lesson we'll stretch it to more shapes. [pause] Okay. I'll see you in the next "
        "question.", pt('f6g67b_line', 'each small rectangle is split'))),
])

# =================================================================================================================
# Topic-32 advanced block (fragment f7, 2026-10-14): geo-067-after (the symmetry principle, stretched), geo32-g068,
# geo32-g069, geo32-g070 - the Hebrew "quadrilaterals advanced" lesson (geo 2955-3270). Lesson figures on the left
# (col 0, w 600) with typed lines on the right; question videos: the question figure on the left (FIG_LEFT), our colour
# copy built in layers on the right (Rule V3), its working written inside the copy so the layers stay together.
# Every Hebrew method is kept (g070: subtracting areas, completions, symmetry).
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g068', 'solve-geo32-g069', 'solve-geo32-g070'})


def f7_poly(pts, col='ink', w=3):
    """the sides of a closed polygon as segments"""
    return [('seg', pts[k][0], pts[k][1], pts[(k + 1) % len(pts)][0], pts[(k + 1) % len(pts)][1], col, w) for k in range(len(pts))]


def f7_lab(items):
    return [('txt', x, y, t, 'ink', 26, True) for x, y, t in items]


# ------------------------------------------------------------------------------------------------ geo-067-after (lesson)
# Hebrew (geo 2955-2995): a diagonal halves a rectangle (grey = white); a triangle inside a rectangle with its tip on the
# opposite side: drop a height, each grey piece equals its white twin; any number of triangles whose bases fill the
# side; the whole parallelogram family; a triangle on the base of a parallelogram (a line parallel to the sides makes two
# parallelograms); part of the base (her thirds -> 1/6; the course's quarters -> 1/8). "The symmetry principle is very
# important; some exam questions fall apart with it."
# V3: generic clean figures (not a question's), every pair of equal halves in ONE tint (teal pair, orange pair), the
# height / the parallel line dashed and drawn after its start point is named; the triangle moved to a second position to
# show it doesn't matter; the base cut into four with ticks.
f7R = [(110, 70), (110, 270), (500, 270), (500, 70)]          # a generic rectangle: A top-left, B, C, D
f7diag = GEO('f7diag', [
    ('line', f7_poly(f7R)),
    ('d', [('seg', 110, 70, 500, 270, 'ink', 3)]),
    ('halves', [('tint', [(110, 70), (110, 270), (500, 270)], 'teal'), ('tint', [(110, 70), (500, 70), (500, 270)], 'orange'),
                ('txt', 210, 215, 'half', 'small', 28), ('txt', 400, 125, 'half', 'orange', 28)]),
], vb='60 40 500 260', w=680, col=0, title='A diagonal halves a rectangle')
f7E1 = (230, 70)
f7in = GEO('f7in', [
    ('line', f7_poly(f7R) + [('seg', 110, 270, f7E1[0], f7E1[1], 'ink', 3), ('seg', f7E1[0], f7E1[1], 500, 270, 'ink', 3),
                             ('tint', [(110, 270), f7E1, (500, 270)], 'ink'), ('txt', f7E1[0], 48, 'E', 'ink', 26, True)]),
    ('h', [('dot', f7E1[0], f7E1[1]), ('seg', f7E1[0], 70, f7E1[0], 270, 'teal', 3, True), ('right', f7E1[0], 270, 0, 90, 14)]),
    ('left', [('tint', [(110, 70), (110, 270), f7E1], 'teal'), ('tint', [f7E1, (110, 270), (f7E1[0], 270)], 'teal'),
              ('txt', 140, 130, 'a', 'small', 28, True), ('txt', 195, 245, 'a', 'small', 28, True)]),
    # 2026-10-18 (batch C #239): one pair at a time - the left pair fades before the right pair lights up
    ('right', [('dim', 60, 30, 500, 270)] + f7_poly(f7R) + [('seg', 110, 270, f7E1[0], f7E1[1], 'ink', 3), ('seg', f7E1[0], f7E1[1], 500, 270, 'ink', 3),
               ('seg', f7E1[0], 70, f7E1[0], 270, 'teal', 3, True), ('txt', f7E1[0], 48, 'E', 'ink', 26, True),
               ('tint', [f7E1, (500, 70), (500, 270)], 'orange'), ('tint', [f7E1, (f7E1[0], 270), (500, 270)], 'orange'),
               ('txt', 440, 110, 'b', 'orange', 28, True), ('txt', 330, 240, 'b', 'orange', 28, True)]),
], vb='60 30 500 270', w=680, col=0, title='A triangle in a rectangle: each shaded piece has a white twin')
f7E2 = (420, 70)
f7move = GEO('f7move', [
    ('line', f7_poly(f7R) + [('seg', 110, 270, f7E2[0], f7E2[1], 'ink', 3), ('seg', f7E2[0], f7E2[1], 500, 270, 'ink', 3),
                             ('tint', [(110, 270), f7E2, (500, 270)], 'teal'), ('txt', f7E2[0], 48, 'E', 'ink', 26, True),
                             ('seg', f7E1[0], 70, 110, 270, 'red', 2, True), ('seg', f7E1[0], 70, 500, 270, 'red', 2, True),
                             ('txt', 300, 175, 'still half', 'small', 28)]),
], vb='60 30 500 270', w=680, col=0, title='Move E along the top side: still half')
f7many = GEO('f7many', [
    ('line', f7_poly(f7R)),
    ('tris', [('seg', 110, 270, 170, 70, 'ink', 3), ('seg', 170, 70, 250, 270, 'ink', 3), ('seg', 250, 270, 330, 70, 'ink', 3),
              ('seg', 330, 70, 380, 270, 'ink', 3), ('seg', 380, 270, 460, 70, 'ink', 3), ('seg', 460, 70, 500, 270, 'ink', 3),
              ('tint', [(110, 270), (170, 70), (250, 270)], 'teal'), ('tint', [(250, 270), (330, 70), (380, 270)], 'teal'),
              ('tint', [(380, 270), (460, 70), (500, 270)], 'teal')]),
    ('bases', [('seg', 110, 290, 250, 290, 'teal', 5), ('seg', 252, 290, 380, 290, 'orange', 5), ('seg', 382, 290, 500, 290, 'teal', 5),
               ('txt', 305, 318, 'no overlap, no gaps', 'ink', 24)]),
    ('h', [('seg', 530, 70, 530, 270, 'red', 3, True), ('seg', 520, 70, 540, 70, 'red', 3), ('seg', 520, 270, 540, 270, 'red', 3),
           ('txt', 548, 170, 'h', 'red', 28, True)]),
], vb='60 40 510 300', w=580, col=0, title='Many triangles with their tips on the top side')
f7P = [(170, 70), (110, 270), (440, 270), (500, 70)]           # a parallelogram: top-left, bottom-left, bottom-right, top-right
f7par = GEO('f7par', [
    ('line', f7_poly(f7P)),
    ('d', [('seg', 170, 70, 440, 270, 'ink', 3), ('tint', [(170, 70), (110, 270), (440, 270)], 'teal'),
           ('tint', [(170, 70), (500, 70), (440, 270)], 'orange')]),
], vb='60 40 500 260', w=680, col=0, title='A diagonal halves a parallelogram')
f7T = (320, 70)
f7par2 = GEO('f7par2', [
    ('line', f7_poly(f7P) + [('seg', 110, 270, f7T[0], f7T[1], 'ink', 3), ('seg', f7T[0], f7T[1], 440, 270, 'ink', 3),
                             ('tint', [(110, 270), f7T, (440, 270)], 'ink'), ('dot', f7T[0], f7T[1])]),
    ('cut', [('seg', f7T[0], 70, 260, 270, 'teal', 3, True)]),
    ('pairs', [('tint', [(170, 70), (110, 270), f7T], 'teal'), ('tint', [f7T, (110, 270), (260, 270)], 'teal'),
               ('tint', [f7T, (500, 70), (440, 270)], 'orange'), ('tint', [f7T, (260, 270), (440, 270)], 'orange')]),
    ('h', [('seg', f7T[0], 70, f7T[0], 270, 'red', 3, True), ('right', f7T[0], 270, 0, 90, 14, 'red'), ('txt', f7T[0] + 18, 200, 'h', 'red', 28, True)]),
], vb='60 40 500 260', w=680, col=0, title='A line parallel to the sides makes two parallelograms')
f7Q = [(110 + 97.5 * k, 270) for k in range(5)]
f7part = GEO('f7part', [
    ('line', f7_poly(f7R) + [('dot', x, y) for x, y in f7Q[1:4]] + [('tick', f7Q[k][0], 270, f7Q[k + 1][0], 270, 1) for k in range(4)]),
    ('tri', [('seg', f7Q[1][0], 270, 400, 70, 'ink', 3), ('seg', 400, 70, f7Q[2][0], 270, 'ink', 3),
             ('tint', [(f7Q[1][0], 270), (400, 70), (f7Q[2][0], 270)], 'teal')]),
    ('whole', [('seg', 110, 270, 400, 70, 'orange', 2.5, True), ('seg', 400, 70, 500, 270, 'orange', 2.5, True),
               ('txt', 305, 45, 'whole base: ½ of the rectangle', 'orange', 24)]),
    ('quarter', [('txt', 305, 302, '¼ of the base  →  ⅛ of the rectangle', 'small', 24)]),
], vb='60 20 500 300', w=680, col=0, title='A triangle on a quarter of the base')
f7a1 = I('f7a1', 'Diagonal: $\\ $shaded $=$ white $=\\frac12$', size=30, col=1)
f7a2 = I('f7a2', 'Tip on the top side: $\\ $shaded $=\\frac12$', size=30, col=1)
f7a2k = I('f7a2k', 'Same colour, same area', size=26, col=1)
f7a3 = I('f7a3', 'No overlap, no gaps: $\\ $shaded $=\\frac12$', size=26, col=1)
f7a3b = IH('f7a3b', '$\\frac{b_1h}{2}+\\frac{b_2h}{2}+\\frac{b_3h}{2}=\\frac{(b_1+b_2+b_3)h}{2}$', size=26, col=1)
f7a4 = I('f7a4', 'Parallelogram, rectangle, rhombus, square', size=28, col=1)
f7a5 = I('f7a5', 'Same base, same perpendicular height $\\Rightarrow$ the same area', size=26, col=1)
f7a6 = IH('f7a6', '$\\frac14\\cdot\\frac12=\\frac18$', size=36, col=1)
video('geo-067-after', 'lesson', slides=[
    S('Equal Heights, Equal Halves',
      L("In the last question, the shaded triangle was exactly as big as the two white triangles together. Let's take "
        "that idea and stretch it.")),
    S('A diagonal',
      L("A rectangle, and a diagonal in it. The diagonal cuts the rectangle into two triangles, and they are exactly the "
        "same size. So the shaded half equals the white half, and each one is half of the rectangle.", show(f7diag['line'], 'A rectangle, and a diagonal'), show(f7diag['d'], 'The diagonal cuts'),
        show(f7diag['halves'], 'So the shaded half equals'), show(f7a1, 'each one is half'))),
    S('A triangle inside',
      L("Now a shaded triangle inside a rectangle, like in the last question. Its base is the bottom side, and its tip, E, "
        "is on the top side. Here too, the shaded part is half of the rectangle, and the white parts together are the "
        "other half.", show(f7in['line'], 'Now a shaded triangle')),
      L("Why? From E, drop a height down to the bottom side. It cuts the rectangle into two smaller rectangles, and each "
        "small rectangle has a diagonal.", show(f7in['h'], 'drop a height')),
      L("In the left rectangle, the shaded piece and the white piece are the two halves, so they're equal. In the right "
        "rectangle too. So each shaded piece equals its white twin. The same colour means the same area.",
        show(f7in['left'], 'In the left rectangle'), show(f7in['right'], 'In the right rectangle too'), show(f7a2k, 'The same colour means')),
      L("And it doesn't matter where E is along the top side. Move it, and the shaded triangle is still half of the "
        "rectangle.", show(f7move['line'], 'Move it'), show(f7a2, 'still half'))),
    S('Many triangles',
      L("Now three shaded triangles in a rectangle. Their tips are on the top side, and their bases sit one after the other "
        "on the bottom side. The triangles do not overlap, and their bases cover the whole bottom side without gaps.",
        show(f7many['line'], 'Now three shaded triangles'), show(f7many['tris'], 'Their tips are on the top side'),
        show(f7many['bases'], 'The triangles do not overlap'), show(f7a3, 'without gaps')),
      L("Why is the shaded part still half? All three triangles have the same height, the height of the rectangle. So "
        "each area is its base times h, over two. And the three bases together make the whole bottom side. So the sum is "
        "the whole base times h, over two, which is half of the rectangle.", show(f7many['h'], 'All three triangles have the same height'),
        show(f7a3b, 'And the three bases together'))),
    S('The parallelogram family',
      L("By the way, this isn't only true in a rectangle. It's true in the whole parallelogram family: a parallelogram, a "
        "rectangle, a rhombus and a square. A diagonal in a parallelogram also cuts it into two triangles with the same "
        "area.", show(f7par['line'], 'In the whole parallelogram family'), show(f7par['d'], 'A diagonal in a parallelogram'),
        show(f7a4, 'two triangles with the same')),
      L("And this one? A shaded triangle on the bottom side of a parallelogram, with its tip on the top side. It's harder "
        "to see, but from the tip, draw a line parallel to the slanted sides.", show(f7par2['line'], 'And this one'),
        show(f7par2['cut'], 'draw a line parallel')),
      L("Now we have two parallelograms, a left one and a right one. In each of them, the shaded piece and the white "
        "piece are the two halves. So the shaded triangle is half of the whole parallelogram.", show(f7par2['pairs'], 'Now we have two parallelograms')),
      L("Its height is the perpendicular distance between the two parallel sides, not the slanted line we drew. Same base "
        "and same height, the same area. And several triangles work too, as long as they don't overlap and their bases "
        "cover the bottom side without gaps.", show(f7par2['h'], 'Its height is the perpendicular distance'),
        show(f7a5, 'Same base and same height'))),
    S('Part of the base',
      L("A slightly more advanced one. The bottom side is cut into four equal pieces. The shaded triangle stands on one "
        "piece, and its tip is on the top side. What part of the rectangle is it?",
        show(f7part['line'], 'cut into four equal pieces'), show(f7part['tri'], 'The shaded triangle stands')),
      L("A triangle on the whole bottom side, with its tip on the top side, would be half of the rectangle. Ours has the "
        "same height, but it stands on only a quarter of the bottom side. So it's a quarter of that half.",
        show(f7part['whole'], 'A triangle on the whole bottom side'), show(f7part['quarter'], 'So it\'s a quarter of that half')),
      L("A quarter of a half is an eighth. So the shaded triangle is an eighth of the rectangle.",
        show(f7a6, 'A quarter of a half')),
      L("This symmetry principle is very important. Some exam questions become easy with it, and we'll see one in the "
        "next question. [pause] Okay. I'll see you in the next video.", pt('f7a6', 'This symmetry principle'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g068 (Hebrew: "which data is sufficient")
# Hebrew (geo 3020-3088): an unclear wording - which ONE given would be enough to calculate the shaded area? Call the area
# of ECD s ("10, 100 - any number"); the diagonal halves the right rectangle (EGC = s); the left rectangle from the
# ratio (Hebrew: midpoints, equal; course: 3 to 1, three times); FEG is half of the left rectangle (symmetry); total;
# some students see it as a fraction of the rectangle; "in the exam we mark and run; in the lesson we check the rest":
# AFE and FBG fail because F's place is unknown (even with a number); "none" fails because one was enough.
# V3: the colour copy is built; E and G marked with their 3 : 1 pieces; the right rectangle outlined, ECD and EGC tinted
# orange with s written on each; the left rectangle with 6s; FEG tinted teal with 3s; the working written below.
f7A, f7B, f7C, f7D = (155.75, 70.5), (155.75, 289.5), (484.25, 289.5), (484.25, 70.5)
f7E, f7G, f7F = (402.125, 70.5), (402.125, 289.5), (155.75, 216.5)
f7g68_base = (f7_poly([f7A, f7B, f7C, f7D]) + [('seg', f7E[0], f7E[1], f7G[0], f7G[1], 'ink', 3), ('seg', f7F[0], f7F[1], f7E[0], f7E[1], 'ink', 3),
              ('seg', f7F[0], f7F[1], f7G[0], f7G[1], 'ink', 3), ('seg', f7E[0], f7E[1], f7C[0], f7C[1], 'ink', 3)]
              + f7_lab([(141, 55, 'A'), (141, 307, 'B'), (499, 307, 'C'), (499, 55, 'D'), (402, 50, 'E'), (402, 312, 'G'), (133, 216, 'F')]))
f7g68 = GEO('f7g68', [
    ('line', f7g68_base),
    ('ratio', [('txt', 279, 92, '3 parts', 'teal', 22), ('txt', 443, 92, '1', 'orange', 22), ('txt', 279, 268, '3 parts', 'teal', 22),
               ('txt', 443, 268, '1', 'orange', 22)] + [('tick', 155.75 + 82.125 * k, 70.5, 155.75 + 82.125 * (k + 1), 70.5, 1, 'small') for k in range(4)]
              + [('tick', 155.75 + 82.125 * k, 289.5, 155.75 + 82.125 * (k + 1), 289.5, 1, 'small') for k in range(4)]),
    ('perp', [('seg', f7E[0], f7E[1], f7G[0], f7G[1], 'red', 4), ('right', f7G[0], f7G[1], 90, 180, 14, 'red')]),
    ('ecd', [('tint', [f7E, f7C, f7D], 'orange'), ('txt', 462, 120, 's', 'orange', 30, True)]),
    ('egc', [('tint', [f7E, f7G, f7C], 'orange'), ('txt', 424, 245, 's', 'orange', 30, True)]),
    ('left', [('tint', [f7A, f7B, f7G, f7E], 'teal')]),
    ('feg', [('tint', [f7F, f7E, f7G], 'teal'), ('txt', 330, 175, '3s', 'small', 32)]),
], vb='110 25 420 310', w=300, title='Rectangle ABCD with E on AD and G on BC')
f7Fp = (f7E[0], f7F[1])
f7g68b = GEO('f7g68b', [
    ('line', f7g68_base),
    ('afe', [('tint', [f7A, f7F, f7E], 'orange'), ('txt', 200, 120, 's', 'orange', 30, True), ('dot', f7Fp[0], f7Fp[1]),
             ('seg', f7F[0], f7F[1], f7Fp[0], f7Fp[1], 'orange', 3, True), ('txt', 270, 158, 's', 'orange', 30, True)]),
    ('low', [('tint', [f7F, f7B, f7G, f7Fp], 'red'), ('txt', 279, 262, '?', 'red', 40)]),
], vb='110 25 420 310', w=300, title='Why the area of AFE is not enough')
# two allowed shapes with the same AF and AE (so the same area of AFE), the second one taller: its shaded area is bigger
def _f7mini(x0, H):
    A_, B_, C_, D_ = (x0, 20), (x0, 20 + H), (x0 + 160, 20 + H), (x0 + 160, 20)
    E_, G_, F_ = (x0 + 120, 20), (x0 + 120, 20 + H), (x0, 50)
    return (f7_poly([A_, B_, C_, D_]) + [('seg', *E_, *G_, 'ink', 2), ('seg', *F_, *E_, 'ink', 2), ('seg', *F_, *G_, 'ink', 2), ('seg', *E_, *C_, 'ink', 2),
            ('tint', [F_, E_, G_], 'teal'), ('tint', [E_, G_, C_], 'teal'), ('tint', [A_, F_, E_], 'orange')])
f7g68c = GEO('f7g68c', [
    ('line', _f7mini(20, 110) + [('txt', 100, 152, 'shaded: smaller', 'small', 18)]),
    ('tall', _f7mini(220, 200) + [('txt', 300, 244, 'shaded: bigger', 'small', 18), ('txt', 200, 268, 'same A F E (orange)', 'orange', 18)]),
], vb='10 10 380 270', w=260, title='Same area of AFE, different shaded areas')
for _it, _y in [(f7g68, 200), (f7g68b, 200)]:
    _R(f5_pin(_it), _y)
_R(f5_pin(f7g68c), 200, x=1340)
f7g68r = [IH('f7g68r%d' % i, t, size=22) if t.startswith('$') else I('f7g68r%d' % i, t, size=20) for i, t in enumerate([
    '$S_{ECD}=s$', '$S_{EGC}=s$', 'right rectangle $=2s$', 'left $=3\\cdot2s=6s$', '$S_{FEG}=\\frac{6s}{2}=3s$', 'shaded $=s+3s=4s$',
    'whole $=8s$: shaded is half'])]
for _k, _x in enumerate(f7g68r[1:]): _R(_x, 200 + 42 * _k, x=1350)
f7g68q = [I('f7g68q0', 'now $s=S_{AFE}$', size=22), I('f7g68q1', 'where is F?', size=22)]
for _k, _x in enumerate(f7g68q): _R(_x, 430 + 44 * _k)
video('solve-geo32-g068', 'solution', qid='geo32-g068', slides=[
    SM('The area of E C D', 'The area of E C D',
      L("A B C D is a rectangle. E lies on A D, G lies on B C, and F lies on A B. A E is three times E D, and B G is three "
        "times G C. Triangles F E G and E G C are shaded. Which of the following additional data is sufficient to determine "
        "the total shaded area?", pt('stem', 'A B C D is a rectangle', 'hl', 12.0), voice='calm', pause=0.5),
      L("They ask which one piece of data, if they gave it to us, would be enough to calculate the shaded area. [short "
        "pause] We'll use the symmetry principle from the last lesson.", pt('stem: ask', 'They ask which one piece')),
      L("[short pause] First, the figure. A E is three times E D, so A D is cut into four equal parts, three and one. B C "
        "is cut the same way. So E and G are both three parts from the left side. That puts E exactly above G.",
        show(f7g68['line'], 'First, the figure'), show(f7g68['ratio'], 'cut into four equal parts')),
      L("A D and B C are parallel, and A B is perpendicular to them. E G joins two points at the same distance from A B, "
        "so it's parallel to A B, and perpendicular to the bases. It cuts the rectangle into a left rectangle and a right "
        "rectangle. And F? Nobody told us where F is on A B. Remember that.", show(f7g68['perp'], 'so it\'s parallel to A B'),
        pt('fig: F', 'And F')),
      L("Let's try choice number one, the area of E C D. They don't say how big it is, so let's call it s. It could be ten, "
        "or a hundred, any number.", show(f7g68['ecd'], "let's call it s")),
      L("E C is a diagonal of the right rectangle, so it cuts it into two equal halves. That means the shaded triangle E G "
        "C is also s, and the right rectangle is s plus s, two s.", show(f7g68['egc'], 'the shaded triangle E G C'),
        show(f7g68r[1], 'is also s'), show(f7g68r[2], 'and the right rectangle is s plus s')),
      L("The left rectangle has the same height, and its base is three times longer, three to one. So it's three times as "
        "big, three times two s, which is six s.", show(f7g68['left'], 'The left rectangle has the same height'),
        show(f7g68r[3], 'three times two s')),
      L("And the shaded triangle F E G? Its base is E G, the whole side of the left rectangle, and its tip F is on the "
        "opposite side, A B. That's the symmetry principle again, so it's half of the left rectangle. Half of six s is three "
        "s.", show(f7g68['feg'], 'And the shaded triangle F E G'), show(f7g68r[4], 'Half of six s')),
      L("Together, the shaded area is s plus three s, four s. So if they give us the area of E C D, we can find the shaded "
        "area. In the exam, once we've understood this, we mark choice number one and move on.",
        show(f7g68r[5], 'the shaded area is s plus three s'), mk('tick', 'choice 1', 'we mark choice number one')),
      L("Some students see it even faster. The whole rectangle is six s plus two s, eight s. The shaded four s is half of "
        "it, and E C D is an eighth.", show(f7g68r[6], 'The whole rectangle is six s'))),
    SM('Why not the others?', 'Why not the others?',
      L("[pause] We're in a lesson, so let's see why the other choices fail. Choice number two, the area of A F E. Now s "
        "means a new area, the area of A F E. A F E is half of a small rectangle at the top, so that rectangle is two s.",
        show(f7g68b['line'], "Choice number two, the area of A F E"), show(f7g68q[0], 'Now s means a new area'),
        show(f7g68b['afe'], 'A F E is half of a small')),
      L("But how big is the rectangle under it? We can't know, because we don't know where F is.",
        show(f7g68b['low'], 'how big is the rectangle under it'), show(f7g68q[1], "we don't know where F is")),
      L("Here are two allowed shapes. In both, A F and A E are the same, so A F E has the same area. But the second "
        "rectangle is taller, so its shaded area is bigger. So the area of A F E doesn't fix the shaded area. Choice number "
        "two is out.", show(f7g68c['line'], 'Here are two allowed shapes'), show(f7g68c['tall'], 'But the second rectangle is taller'),
        mk('cross', 'choice 2', 'Choice number two is out')),
      L("Choice number three, the area of F B G, has exactly the same problem. We don't know where F is. It's out too.",
        mk('cross', 'choice 3', "It's out too")),
      L("And choice number four says none of the data is enough, but we already saw that the area of E C D is enough. "
        "So it's out, and choice number one is our answer. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 4', 'So it\'s out'), mk('tick', 'choice 1', 'choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g069 (Hebrew: the isosceles trapezoid)
# Hebrew (geo 3089-3168): two ways. The full math: the shaded triangle is obtuse, its only known base is AD, its height is
# outside (extend AD, drop the shortest distance from B); 3h/2 = 10 (course: 5h/2 = 15, h = 6); that height is also the
# trapezoid's height; (sum of bases) x h / 2. The psychometric way: the shaded and the white triangle have the same height,
# so the area ratio is the base ratio; illustrate by cutting BC into pieces as long as AD (she notices a parallelogram,
# BD its diagonal); "if the base were 3 times bigger the area would be 3 times bigger"; much shorter, you barely write.
# V3: the copy; AD and its 5 in teal; the dashed extension of AD, then the dashed outside height from B with its right
# angle and h; the working below; method 2: a new copy, BC cut into four pieces of 5 (ticks), dashed lines from D, 15 in
# each triangle; the parallelogram ABPD outlined.
f7a_, f7b_, f7c_, f7d_ = (271.333, 66.444), (125.333, 293.556), (514.667, 293.556), (368.667, 66.444)
f7H = (f7b_[0], f7a_[1])
f7g69_base = (f7_poly([f7a_, f7b_, f7c_, f7d_]) + [('seg', f7b_[0], f7b_[1], f7d_[0], f7d_[1], 'ink', 3),
              ('tint', [f7a_, f7b_, f7d_], 'ink')]
              + f7_lab([(257, 50, 'A'), (111, 312, 'B'), (529, 312, 'C'), (383, 50, 'D')])
              + [('txt', 320, 46, '5', 'ink', 24), ('txt', 320, 318, '20', 'ink', 24)])
f7g69 = GEO('f7g69', [
    ('line', f7g69_base),
    ('ad', [('seg', f7a_[0], f7a_[1], f7d_[0], f7d_[1], 'teal', 6)]),
    ('ext', [('seg', f7a_[0], f7a_[1], f7H[0] - 10, f7H[1], 'teal', 3, True)]),
    ('h', [('seg', f7b_[0], f7b_[1], f7H[0], f7H[1], 'teal', 3, True), ('right', f7H[0], f7H[1], 0, 270, 14),
           ('txt', f7H[0] - 20, 180, 'h', 'small', 30, True)]),
    ('h6', [('txt', f7H[0] + 6, 215, '= 6', 'small', 28)]),
    ('whole', [('tint', [f7a_, f7b_, f7c_, f7d_], 'small')] + f7_poly([f7a_, f7b_, f7c_, f7d_], 'small', 5)),
], vb='90 30 450 300', w=300, title='Isosceles trapezoid ABCD with the diagonal BD')
f7Pk = [(f7b_[0] + 97.333 * k, f7b_[1]) for k in range(5)]
f7g69b = GEO('f7g69b', [
    ('line', f7g69_base),
    # 2026-10-18 (batch C #241): BOTH perpendicular heights - from B to the line of AD, and from D down to BC
    ('heights', [('seg', f7a_[0], f7a_[1], f7H[0] - 10, f7H[1], 'small', 2.5, True), ('seg', f7b_[0], f7b_[1], f7H[0], f7H[1], 'small', 3, True),
                 ('right', f7H[0], f7H[1], 0, 270, 12, 'small'), ('seg', f7d_[0], f7d_[1], f7d_[0], f7b_[1], 'orange', 3, True),
                 ('right', f7d_[0], f7b_[1], 0, 90, 12, 'orange')]),
    ('same', [('seg', f7a_[0], f7a_[1], f7d_[0], f7d_[1], 'small', 6), ('seg', f7b_[0], f7b_[1], f7c_[0], f7c_[1], 'orange', 6)]),
    ('cuts', [('dot', x, y) for x, y in f7Pk[1:4]] + [('tick', f7Pk[k][0], f7Pk[k][1], f7Pk[k + 1][0], f7Pk[k + 1][1], 1) for k in range(4)]
             + [('seg', f7d_[0], f7d_[1], x, y, 'orange', 2.5, True) for x, y in f7Pk[1:4]]),
    ('par', [('path', [f7a_, f7b_, f7Pk[1], f7d_, f7a_], 'small', 5)]),
    ('vals', [('txt', 290, 110, '15', 'small', 28)] + [('txt', (f7Pk[k][0] + f7Pk[k + 1][0]) / 2 + 6, 276, '15', 'orange', 24) for k in range(4)]),
], vb='90 30 450 300', w=300, title='Cut BC into four pieces of 5')
for _it, _y in [(f7g69, 200), (f7g69b, 200)]:
    _R(_it, _y)
f7g69r = [IH('f7g69r%d' % i, t, size=24) for i, t in enumerate(['$\\frac{5h}{2}=15$', '$5h=30$', '$h=6$', '$5+20=25$', '$25\\cdot6=150$', '$\\frac{150}{2}=75$'])]
f7g69q = [IH('f7g69q%d' % i, t, size=24) if t.startswith('$') else I('f7g69q%d' % i, t, size=22) for i, t in enumerate([
    'same height:', 'area ratio = base ratio', '$20=4\\cdot5$', '$4\\cdot15=60$', '$15+60=75$'])]
for _k, _x in enumerate(f7g69r): _R(_x, 200 + 50 * _k, x=1350)
for _k, _x in enumerate(f7g69q): _R(_x, 200 + 50 * _k, x=1350)
video('solve-geo32-g069', 'solution', qid='geo32-g069', slides=[
    SM('Method 1 · The math way', 'The full math',
      L("A B C D is an isosceles trapezoid. A D is parallel to B C, A D is five centimeters and B C is twenty centimeters. "
        "The shaded triangle A B D has an area of fifteen square centimeters. What is the area of the trapezoid?",
        pt('stem', 'A B C D is an isosceles trapezoid', 'hl', 10.0), voice='calm', pause=0.5),
      L("We know the area of the shaded triangle, and we need the area of the whole trapezoid. [short pause] We'll solve "
        "it in two different ways. First the math way, and then by understanding, with equal heights.", pt('fig: 15 cm²', 'We know the area')),
      L("[short pause] The math way first. The shaded part is a triangle, an obtuse one. Its area is base times height, "
        "over two, and the only base we know is A D, five.", show(f7g69['line'], 'The math way first'),
        show(f7g69['ad'], 'the only base we know is A D')),
      L("Where is the height to A D? For this base, A D, the perpendicular from B lands beyond A. So we extend D A past A, "
        "and from B we draw the perpendicular to that line. Its length, the perpendicular distance, is the height h.",
        show(f7g69['ext'], 'So we extend D A past A'), show(f7g69['h'], 'from B we draw the perpendicular')),
      L("So five times h, over two, is fifteen. Multiply both sides by two, and five h is thirty. Divide by five, so h is "
        "six.", show(f7g69r[0], 'So five times h'), show(f7g69r[1], 'and five h is thirty'), show(f7g69r[2], 'so h is six'),
        show(f7g69['h6'], 'six.')),
      L("And look, this height is also the height of the trapezoid, the distance between the two parallel sides. The area "
        "of a trapezoid is the sum of the bases, times the height, over two.", show(f7g69['whole'], 'this height is also the height of the trapezoid')),
      L("Five plus twenty is twenty-five. Twenty-five times six is a hundred fifty. And a hundred fifty over two is "
        "seventy-five. Choice number three is our answer.", show(f7g69r[3], 'Five plus twenty'), show(f7g69r[4], 'Twenty-five times six'),
        show(f7g69r[5], 'a hundred fifty over two'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Understanding: a ratio', 'A ratio',
      L("[pause] Now by understanding, using equal heights. Look at the shaded triangle A B D and the white triangle B C D. "
        "They have the same height, the distance between the parallel sides. For B C D, it's the perpendicular from D down "
        "to B C. For A B D, it's the perpendicular from B to the line of A D.", show(f7g69b['line'], 'Look at the shaded triangle'),
        show(f7g69b['heights'], 'For B C D')),
      L("When two triangles have the same height, the ratio of their areas is the ratio of their bases. The shaded base "
        "is five, and the white base is twenty, four times bigger. So the white area is four times bigger too.",
        show(f7g69b['same'], 'the ratio of their areas'), show(f7g69q[0], 'When two triangles have the same height'),
        show(f7g69q[1], 'the ratio of their areas'), show(f7g69q[2], 'four times bigger. So')),
      L("Let's see it. Cut B C into four pieces of five, and draw lines from D. Now every triangle here has the same base, "
        "five, and the same height. A B and the first piece even make a parallelogram, with B D as its diagonal.",
        show(f7g69b['cuts'], 'Cut B C into four pieces'), show(f7g69b['par'], 'make a parallelogram')),
      L("So all the triangles have the same area, fifteen each. The four small white ones make four times fifteen, sixty. "
        "The whole trapezoid is the shaded fifteen plus sixty, which is seventy-five. Choice number three again. Careful, "
        "sixty is only the white triangle, so choice number two is a trap.", show(f7g69b['vals'], 'fifteen each'),
        show(f7g69q[3], 'make four times fifteen'), show(f7g69q[4], 'The whole trapezoid is the shaded'),
        mk('tick', 'choice 3', 'Choice number three again'), mk('cross', 'choice 2', 'choice number two is a trap')),
      L("So when two triangles have the same perpendicular height, the area ratio is the base ratio. If the base were three "
        "times bigger, the area would be three times bigger. We didn't use that the trapezoid is isosceles, so this works "
        "for any trapezoid with these bases and this area. [pause] Okay. I'll see you in the next question.",
        pt('f7g69b_line', 'So when two triangles'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g070 (Hebrew: the shaded pentagon on a grid)
# Hebrew (geo 3171-3268): "a trapezoid? count the sides: a pentagon - we never learned it"; "shaded-area questions": two
# main approaches - subtract the white areas from a shape we know (the main and most common), or break the shaded area
# into familiar shapes, by completions or by symmetry. Course numbers: 8 x 5 grid, white triangles 3, 5, 3, 3, shaded 26.
# Completions are made EXACT here: every sloping side is the diagonal of a corner rectangle, so the cut pieces on its two
# sides are the same pieces turned around and complete each other (shaded part = half of that rectangle).
# V3: the copy with its grid; method 1: the four white corner triangles tinted orange one by one with their legs and
# areas; method 2: the five rectangles that tile the grid outlined, one corner rectangle with its two halves in two tints;
# method 3: the dashed line between the side vertices, the triangle above it teal, the middle rectangle and the two side
# triangles; the working written below the copy.
f7gx = lambda i: 174.0 + 36.5 * i
f7gy = lambda j: 78.75 + 36.5 * j
f7gp = lambda i, j: (f7gx(i), f7gy(j))
f7pent = [f7gp(3, 0), f7gp(8, 2), f7gp(6, 5), f7gp(2, 5), f7gp(0, 2)]
f7grid = ([('seg', f7gx(i), f7gy(0), f7gx(i), f7gy(5), 'ink', 1) for i in range(1, 8)]
          + [('seg', f7gx(0), f7gy(j), f7gx(8), f7gy(j), 'ink', 1) for j in range(1, 5)]
          + f7_poly([f7gp(0, 0), f7gp(8, 0), f7gp(8, 5), f7gp(0, 5)]) + f7_poly(f7pent) + [('tint', f7pent, 'ink')])
f7W = [([f7gp(0, 0), f7gp(3, 0), f7gp(0, 2)], '3', (1.0, 0.7)), ([f7gp(3, 0), f7gp(8, 0), f7gp(8, 2)], '5', (6.3, 0.6)),
       ([f7gp(8, 2), f7gp(8, 5), f7gp(6, 5)], '3', (7.3, 4.0)), ([f7gp(0, 2), f7gp(0, 5), f7gp(2, 5)], '3', (0.7, 4.0))]
f7vb = '150 30 340 305'
f7g70 = GEO('f7g70', [('line', f7grid)]
            + [('w%d' % k, [('tint', pts, 'orange')] + f7_poly(pts, 'orange', 4) + [('txt', f7gx(c[0]), f7gy(c[1]), v, 'orange', 30)])
               for k, (pts, v, c) in enumerate(f7W)]
            , vb='150 55 340 240', w=300, title='A shaded pentagon on an 8 by 5 grid')
f7g70b = GEO('f7g70b', [
    ('line', f7grid),
    ('tiles', [('seg', f7gx(3), f7gy(0), f7gx(3), f7gy(2), 'teal', 3, True), ('seg', f7gx(0), f7gy(2), f7gx(8), f7gy(2), 'teal', 3, True),
               ('seg', f7gx(2), f7gy(2), f7gx(2), f7gy(5), 'teal', 3, True), ('seg', f7gx(6), f7gy(2), f7gx(6), f7gy(5), 'teal', 3, True)]),
    # 2026-10-18 (batch C #242): the five rectangles' dimensions first, then each shaded part at its own clause
    ('dims', [('txt', f7gx(1.5), f7gy(0) - 10, '3', 'teal', 20), ('txt', f7gx(5.5), f7gy(0) - 10, '5', 'teal', 20),
              ('txt', f7gx(0) - 12, f7gy(1), '2', 'teal', 20), ('txt', f7gx(0) - 12, f7gy(3.5), '3', 'teal', 20),
              ('txt', f7gx(1), f7gy(5) + 16, '2', 'teal', 20), ('txt', f7gx(4), f7gy(5) + 16, '4', 'teal', 20), ('txt', f7gx(7), f7gy(5) + 16, '2', 'teal', 20)]),
    ('pair', [('tint', [f7gp(0, 2), f7gp(3, 0), f7gp(3, 2)], 'small'), ('tint', [f7gp(0, 0), f7gp(3, 0), f7gp(0, 2)], 'orange'),
              ('txt', f7gx(2.1), f7gy(1.45), '3', 'small', 28)]),
    ('v1', [('txt', f7gx(5.8), f7gy(1.4), '5', 'small', 28)]),
    ('v2', [('txt', f7gx(1.35), f7gy(3.8), '3', 'small', 28), ('txt', f7gx(6.65), f7gy(3.8), '3', 'small', 28)]),
    ('v3', [('tint', [f7gp(2, 2), f7gp(6, 2), f7gp(6, 5), f7gp(2, 5)], 'orange'), ('txt', f7gx(4), f7gy(3.6), '12', 'small', 32)]),
], vb='140 50 350 260', w=300, title='Completions: each corner rectangle is cut in half')
f7g70c = GEO('f7g70c', [
    ('line', f7grid),
    ('cut', [('dot', f7gx(0), f7gy(2)), ('dot', f7gx(8), f7gy(2)), ('seg', f7gx(0), f7gy(2), f7gx(8), f7gy(2), 'teal', 3, True)]),
    ('top', [('tint', [f7gp(0, 2), f7gp(3, 0), f7gp(8, 2)], 'small'), ('txt', f7gx(3.6), f7gy(1.35), '8', 'small', 32)]),
    ('mid', [('tint', [f7gp(2, 2), f7gp(6, 2), f7gp(6, 5), f7gp(2, 5)], 'orange'), ('txt', f7gx(4), f7gy(3.6), '12', 'orange', 32)]),
    ('sides', [('tint', [f7gp(0, 2), f7gp(2, 2), f7gp(2, 5)], 'small'), ('tint', [f7gp(6, 2), f7gp(8, 2), f7gp(6, 5)], 'small'),
               ('txt', f7gx(1.35), f7gy(2.9), '3', 'small', 28), ('txt', f7gx(6.65), f7gy(2.9), '3', 'small', 28)]),
], vb='150 55 340 240', w=300, title='Symmetry: break the shape into familiar pieces')
for _it, _y in [(f7g70, 200), (f7g70b, 200), (f7g70c, 200)]:
    _R(_it, _y)
_f7r = lambda pre, rows: [IH('%s%d' % (pre, i), t, size=24) for i, t in enumerate(rows)]
f7g70r = _f7r('f7g70r', ['$8\\cdot5=40$', '$\\frac{3\\cdot2}{2}=3$', '$\\frac{5\\cdot2}{2}=5$', '$\\frac{2\\cdot3}{2}=3,\\ 3$', '$3+5+3+3=14$', '$40-14=26$'])
f7g70s = _f7r('f7g70s', ['$\\frac{3\\cdot2}{2}=3$', '$\\frac{5\\cdot2}{2}=5$', '$\\frac{2\\cdot3}{2}=3,\\ 3$', '$4\\cdot3=12$', '$3+5+3+3+12$', '$=26$'])
f7g70t = _f7r('f7g70t', ['$\\frac{8\\cdot2}{2}=8$', '$4\\cdot3=12$', '$\\frac{2\\cdot3}{2}=3$', '$8+12+3+3=26$'])
for _rows in (f7g70r, f7g70s, f7g70t):
    for _k, _x in enumerate(_rows): _R(_x, 200 + 50 * _k, x=1350)
video('solve-geo32-g070', 'solution', qid='geo32-g070', slides=[
    SM('Method 1 · The math way: subtract areas', 'Subtracting areas',
      L("The rectangle in the accompanying figure is made of forty congruent squares, each with a side of one centimeter. "
        "What is the shaded area?", pt('stem', 'The rectangle in the accompanying figure', 'hl', 8.0), voice='calm', pause=0.5),
      L("What is the shaded shape? A trapezoid? Let's count its sides. One, two, three, four, five. It's a pentagon, and "
        "we never learned an area formula for it. We call these shaded-area questions, and there are two main "
        "approaches.", pt('stem: ask', 'What is the shaded shape')),
      L("[short pause] One approach takes an area we know, the rectangle, and subtracts the white parts. The other breaks "
        "the shaded area into shapes we know, with completions or with symmetry. We'll see all of them. Subtracting is "
        "the main one, and the most common, so we start with it, the math way.", show(f7g70['line'], 'One approach takes an area we know')),
      L("The rectangle is eight by five, so its area is eight times five, forty. The white parts are four right triangles "
        "in the corners, and the area of a right triangle is leg times leg, over two.", show(f7g70r[0], 'so its area is eight times five')),
      L("Top left, the legs are three and two. Three times two is six, and over two that's three.",
        show(f7g70['w0'], 'Top left'), show(f7g70r[1], 'Three times two is six')),
      L("Top right, the legs are five and two. Five times two is ten, and over two that's five.",
        show(f7g70['w1'], 'Top right'), show(f7g70r[2], 'Five times two is ten')),
      L("The two bottom ones have legs of two and three. Two times three is six, and half of six is three. So each one is three.",
        show(f7g70['w2'], 'The two bottom ones'), show(f7g70['w3'], 'legs of two and three'), show(f7g70r[3], 'Two times three is six')),
      L("All the white parts together are three plus five plus three plus three, fourteen. Forty minus fourteen is "
        "twenty-six. Choice number three is our answer. Careful, fourteen, choice number one, is the white part, not the "
        "shaded part.", show(f7g70r[4], 'All the white parts together'), show(f7g70r[5], 'Forty minus fourteen'),
        mk('tick', 'choice 3', 'Choice number three is our answer'), mk('cross', 'choice 1', 'Careful, fourteen, choice number one'))),
    SM('Method 2 · Understanding: completions', 'Completions',
      L("[pause] Now let's use understanding: pair the pieces that make a whole. Many students count whole squares, and "
        "when two pieces of squares complete each other into one whole square, they count them as one.",
        show(f7g70b['line'], "Now let's use understanding")),
      L("Here the sloping sides cut squares into odd pieces, so we look at them in groups. Cut the grid into five "
        "rectangles, four in the corners and one in the middle. On top, three by two and five by two. At the bottom, two by "
        "three, four by three, and two by three.", show(f7g70b['tiles'], 'Cut the grid into five rectangles'),
        show(f7g70b['dims'], 'On top, three by two')),
      L("Look at the top left rectangle, three by two. The sloping side goes from corner to corner, so every shaded piece "
        "has a white piece just like it, turned around. They complete each other, so the shaded part is half of six, "
        "three.", show(f7g70b['pair'], 'Look at the top left rectangle'), show(f7g70s[0], 'so the shaded part is half of six')),
      L("The same in the other corners. Top right, half of ten is five. At the bottom, half of six is three, twice.",
        show(f7g70b['v1'], 'Top right, half of ten'), show(f7g70s[1], 'Top right, half of ten'),
        show(f7g70b['v2'], 'At the bottom, half of six'), show(f7g70s[2], 'At the bottom, half of six')),
      L("The middle rectangle is all shaded. Four times three is twelve whole squares.", show(f7g70b['v3'], 'The middle rectangle'),
        show(f7g70s[3], 'Four times three')),
      L("Three plus five plus three plus three plus twelve is twenty-six. Choice number three again.",
        show(f7g70s[4], 'Three plus five plus three'), show(f7g70s[5], 'is twenty-six'), mk('tick', 'choice 3', 'Choice number three again'))),
    SM('Method 3 · Understanding: symmetry', 'Symmetry',
      L("[pause] And the third way, by understanding again, with the symmetry principle we already know. We break the shape into pieces we know. "
        "Draw a line between the two side corners of the pentagon.", show(f7g70c['line'], 'And the third way'),
        show(f7g70c['cut'], 'Draw a line between')),
      L("Above the line there's a triangle. Its base is the whole width, eight, and its tip is on the top side of an eight "
        "by two rectangle. So it's half of sixteen, eight.", show(f7g70c['top'], 'Above the line'), show(f7g70t[0], "So it's half of sixteen")),
      L("Below the line, the middle rectangle is four by three, twelve. And each side triangle is half of a two by three "
        "rectangle, half of six, three.", show(f7g70c['mid'], 'the middle rectangle'), show(f7g70t[1], 'four by three, twelve'),
        show(f7g70c['sides'], 'each side triangle'), show(f7g70t[2], 'half of six, three')),
      L("Eight plus twelve plus three plus three is twenty-six. Choice number three again. So in a shaded-area question, "
        "subtract the white parts from a shape you know, or break the shaded part into shapes you know. [pause] Okay. "
        "I'll see you in the next question.", show(f7g70t[3], 'Eight plus twelve'), mk('tick', 'choice 3', 'Choice number three again.'))),
])


def f7_pin(g):
    """pin every layer to its base (a layer is drawn on its own figure, at the same place and scale)"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


for _g in (f7diag, f7in, f7move, f7many, f7par, f7par2, f7part, f7g68, f7g68b, f7g69, f7g69b, f7g70, f7g70b, f7g70c): f7_pin(_g)

# =================================================================================================================
# Topic-32 advanced block, part 2 (fragment f8, 2026-10-14): geo32-g071, geo32-g072, r26-t32-perimeter, q-r26-t32-06,
# q-r26-t32-07 (Hebrew geo 3272-3443 for g071 and g072; the perimeter lesson and its two questions are course additions).
# Question figure on the left (FIG_LEFT), our colour copy of it on the right, built step by step (Rule V3).
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g071', 'solve-geo32-g072', 'solve-q-r26-t32-06', 'solve-q-r26-t32-07'})


def f8_pin(g):
    """a figure whose later layers may come after other board items: the base is the figure, the layers draw on it"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


# ------------------------------------------------------------------------------------------------ geo32-g071 (Hebrew: the bisector in a general quadrilateral)
# Hebrew (geo 3272-3367): what makes it hard (through the quadrilateral to D, halve it, then triangle AED, all with letters,
# in under a minute, second-to-last question); the full math (360, isolate D, halve, triangle AED, cross out choices as
# the number and the beta term appear); then plugging in (choose numbers that look like the drawing, put them in the
# drawing AND in the answers; the drawback: cross out the others to be sure; "if time runs out, a reasonable guess");
# which way for whom. English: angle B = 130 (Hebrew 90); plug-in alpha = 110, beta = 80 (they look like the drawing).
# V3: the quadrilateral traced with its four angles; D marked "?"; the bisector DE drawn with two equal arcs at D; FOCUS on
# triangle AED (tinted, the rest dimmed) with x in red. Method 2 on a new copy: the chosen numbers written on the figure,
# D, its halves and x written as they are found.
f8A, f8B, f8C, f8D, f8E = (238.889, 293.556), (433.556, 293.556), (489.039, 141.117), (167.126, 72.692), (412.42, 293.556)
f8_71base = [('seg', *f8A, *f8B), ('seg', *f8B, *f8C), ('seg', *f8C, *f8D), ('seg', *f8D, *f8A), ('seg', *f8D, *f8E),
             ('txt', 222, 312, 'A', 'ink', 24, True), ('txt', 452, 312, 'B', 'ink', 24, True), ('txt', 510, 132, 'C', 'ink', 24, True),
             ('txt', 150, 56, 'D', 'ink', 24, True), ('txt', 412, 318, 'E', 'ink', 24, True)]
f8_aA = gdir(*f8A, *f8D); f8_aCB = gdir(*f8C, *f8B); f8_aCD = gdir(*f8C, *f8D); f8_aBC = gdir(*f8B, *f8C)
f8_aDA = gdir(*f8D, *f8A); f8_aDE = gdir(*f8D, *f8E); f8_aDC = gdir(*f8D, *f8C); f8_aED = gdir(*f8E, *f8D)
f8g71 = f8_pin(GEO('f8g71', [
    ('line', f8_71base),
    ('quad', [('path', [f8A, f8B, f8C, f8D, f8A], 'teal', 6),
              ('arc', *f8A, 30, 0, f8_aA, 'small', 'α', 50), ('arc', *f8B, 30, f8_aBC, 180, 'large', '130°', 58),
              ('arc', *f8C, 30, f8_aCD, f8_aCB, 'small', 'β', 50), ('arc', *f8D, 30, f8_aDA, f8_aDC, 'large', '?', 50)]),
    ('half', [('seg', *f8D, *f8E, 'teal', 4), ('arc', *f8D, 44, f8_aDA, f8_aDE, 'small'), ('arc', *f8D, 50, f8_aDE, f8_aDC, 'small'),
              ('arc', *f8D, 54, f8_aDE, f8_aDC, 'small')]),
    ('aed', [('dim', 140, 40, 400, 290), ('tint', [f8A, f8E, f8D], 'teal'), ('path', [f8A, f8E, f8D, f8A], 'teal', 5),
             ('txt', 222, 312, 'A', 'ink', 24, True), ('txt', 412, 318, 'E', 'ink', 24, True), ('txt', 150, 56, 'D', 'ink', 24, True),
             ('arc', *f8A, 30, 0, f8_aA, 'small', 'α', 50), ('arc', *f8D, 44, f8_aDA, f8_aDE, 'small', '½D', 66),
             ('arc', *f8E, 26, f8_aED, 180, 'red', 'x', 44)]),
], vb='130 30 410 300', w=360, title='Quadrilateral ABCD with the bisector DE'))
f8n1 = I('f8n1', '$\\angle D=230°-\\alpha-\\beta$', size=26)
f8n2 = I('f8n2', '$\\angle ADE=115°-\\frac\\alpha2-\\frac\\beta2$', size=26)
f8n3 = I('f8n3', '$x=180°-\\alpha-\\left(115°-\\frac\\alpha2-\\frac\\beta2\\right)$', size=26)
f8n4 = I('f8n4', '$x=65°-\\frac\\alpha2+\\frac\\beta2$', size=28)
f8g71b = f8_pin(GEO('f8g71b', [
    ('line', f8_71base),
    ('nums', [('arc', *f8A, 30, 0, f8_aA, 'orange', '110°', 54), ('arc', *f8B, 30, f8_aBC, 180, 'large', '130°', 58),
              ('arc', *f8C, 30, f8_aCD, f8_aCB, 'small', '80°', 54)]),
    ('d', [('arc', *f8D, 30, f8_aDA, f8_aDC, 'large', '40°', 52)]),
    ('halves', [('seg', *f8D, *f8E, 'teal', 4), ('arc', *f8D, 44, f8_aDA, f8_aDE, 'small', '20°', 66)]),
    ('x', [('arc', *f8E, 26, f8_aED, 180, 'red', '50°', 48)]),
], vb='130 30 410 300', w=300, title='The same figure with alpha = 110 and beta = 80'))
# 2026-10-18 (batch C #243): every step of both methods written at its clause
f8n0 = I('f8n0', '$\\angle D+\\alpha+130°+\\beta=360°$', size=26)
f8n0b = I('f8n0b', '$360°-130°=230°$', size=26)
f8n3b = I('f8n3b', '$x=180°-\\alpha-115°+\\frac\\alpha2+\\frac\\beta2$', size=26)
f8m = [IH('f8m%d' % i, t, size=22) for i, t in enumerate(['$110+130+80=320$', '$\\angle D=360-320=40$', '$\\frac{40}{2}=20$',
                                                         '$110+20=130$', '$x=180-130=50$'])]
f8p0 = I('f8p0', '$\\frac\\alpha2=55,\\ \\ \\frac\\beta2=40$, $\\ $we need $\\ 50$', size=28)
f8p3 = IH('f8p3', '(1) $65+55-40=80$ ✗', size=28)
f8p6 = IH('f8p6', '(2) $130+55-40=145$ ✗', size=28)
f8p4 = I('f8p4', '(3) $65-55+40=50$ ✓', size=28)
f8p5 = I('f8p5', '(4) $130-55+40=115$ ✗', size=28)
video('solve-geo32-g071', 'solution', qid='geo32-g071', slides=[
    SM('Method 1 · The math way', 'The plan',
      L("In quadrilateral A B C D, angle A is alpha, angle B is a hundred thirty degrees, and angle C is beta. E lies on A B, "
        "and D E bisects angle A D C. Which expression equals angle A E D?", pt('stem', 'In quadrilateral A B C D', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("What makes this hard? We have to go through the whole quadrilateral to find angle D, cut it in half, and then work "
        "in triangle A E D, all with letters. [short pause] We'll solve it in two different ways, the math way, with "
        "algebra, and then by plugging in numbers.", pt('fig: x', 'triangle A E D')),
      L("[short pause] Here's the plan on the figure. The four angles of the quadrilateral add up to three hundred sixty "
        "degrees, and only angle D is missing.", show(f8g71['line'], "Here's the plan on the figure"),
        show(f8g71['quad'], 'The four angles of the quadrilateral')),
      L("D E bisects angle D, so it cuts it into two equal halves.", show(f8g71['half'], 'D E bisects angle D')),
      L("And x is an angle of triangle A E D, whose angles add up to a hundred eighty. Its other two angles are alpha and "
        "half of angle D.", show(f8g71['aed'], 'And x is an angle of triangle A E D'))),
    SM('Method 1 · The math way', 'The algebra',
      L("Now the algebra. Angle D plus alpha plus a hundred thirty plus beta is three hundred sixty.",
        show(f8n0, 'Angle D plus alpha plus')),
      L("Three hundred sixty minus a hundred thirty is two hundred thirty. So angle D is two hundred thirty, minus alpha, "
        "minus beta.", show(f8n0b, 'Three hundred sixty minus a hundred thirty'), show(f8n1, 'So angle D is two hundred thirty')),
      L("Half of two hundred thirty is a hundred fifteen. So each half, angle A D E, is a hundred fifteen, minus half alpha, "
        "minus half beta.", show(f8n2, 'So each half')),
      L("In triangle A E D, x is a hundred eighty, minus alpha, minus angle A D E. And angle A D E is a hundred fifteen "
        "minus half alpha minus half beta.", show(f8n3, 'In triangle A E D')),
      L("Now we open the bracket. The minus in front of it changes every sign inside. So it's minus a hundred fifteen, plus "
        "half alpha, plus half beta.", show(f8n3b, 'So it\'s minus a hundred fifteen')),
      L("A hundred eighty minus a hundred fifteen is sixty-five. So the number in the answer is sixty-five, and choice "
        "numbers two and four are out, because they have a hundred thirty. We got plus half beta, so choice number one is "
        "out too. And minus alpha plus half alpha leaves minus half alpha. So x is sixty-five, minus half alpha, plus half "
        "beta. Choice number three is our answer.",
        mk('cross', 'choice 2', 'choice numbers two and four are out'), mk('cross', 'choice 4', 'because they have a hundred thirty'),
        mk('cross', 'choice 1', 'so choice number one is out too'), show(f8n4, 'So x is sixty-five'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Plugging in numbers', 'Plug in numbers',
      L("[pause] Now let's plug in numbers. The right answer has to be true for every alpha and beta that the givens "
        "allow. So it must also be true for one example that we choose. We put our numbers into the figure and into the "
        "choices.", show(f8g71b['line'], "Now let's plug in numbers")),
      L("The figure is not drawn to scale, so we don't read values from it. Let's take alpha a hundred ten and beta "
        "eighty, because they're easy to add and to halve. Any other allowed values would work too. We just have to check "
        "that they're allowed.", show(f8g71b['nums'], 'Let\'s take alpha a hundred ten')),
      L("Let's find angle D. The four angles of the quadrilateral add up to three hundred sixty, so we add the three we "
        "know. A hundred ten plus a hundred thirty plus eighty is three hundred twenty. Three hundred sixty minus three "
        "hundred twenty is forty. Forty is positive, so our numbers are allowed.", show(f8m[0], 'A hundred ten plus a hundred thirty'),
        show(f8m[1], 'Three hundred sixty minus three'), show(f8g71b['d'], 'is forty')),
      L("D E cuts angle D in half, so each half is twenty.", show(f8m[2], 'so each half is twenty'), show(f8g71b['halves'], 'is twenty.')),
      L("Now let's find x. In triangle A E D, a hundred ten plus twenty is a hundred thirty, and a hundred eighty minus a hundred "
        "thirty is fifty. All three angles of the triangle are positive, so x is fifty degrees.",
        show(f8m[3], 'a hundred ten plus twenty'), show(f8m[4], 'and a hundred eighty minus a hundred'), show(f8g71b['x'], 'so x is fifty degrees'))),
    SM('Method 2 · Plugging in numbers', 'Check the choices',
      L("Now we put alpha a hundred ten and beta eighty into each choice. With these numbers x is fifty, so the right choice has to give fifty. Half alpha is fifty-five, and half beta is forty. "
        "Choice number one says sixty-five, plus half alpha, minus half beta. Sixty-five plus fifty-five minus forty is "
        "eighty. Not fifty, out. Choice number two says a hundred thirty, plus half alpha, minus half beta. A hundred "
        "thirty plus fifty-five minus forty is a hundred forty-five. Out.", show(f8p0, 'Half alpha is fifty-five'), pt('choice 1', 'Choice number one says', 'hl', 3.0), show(f8p3, 'Sixty-five plus fifty-five'), pt('choice 2', 'Choice number two says', 'hl', 3.0), show(f8p6, 'A hundred thirty plus fifty-five'),
        mk('cross', 'choice 1', 'Not fifty, out'), mk('cross', 'choice 2', 'is a hundred forty-five. Out')),
      L("Choice number three says sixty-five, minus half alpha, plus half beta. Sixty-five minus fifty-five plus forty "
        "is fifty. It matches. But a match alone isn't enough if another choice also matches, so we check the last one too.",
        pt('choice 3', 'Choice number three says', 'hl', 3.0), show(f8p4, 'Sixty-five minus fifty-five'), pt('choice 3', 'It matches')),
      L("Choice number four says a hundred thirty, minus half alpha, plus half beta. A hundred thirty minus fifty-five "
        "plus forty is a hundred fifteen. Out. A mismatch rules a choice out right away, and only choice number three "
        "matched. So choice number three is our answer. [pause] Okay. I'll see you in the next question.",
        pt('choice 4', 'Choice number four says', 'hl', 3.0), show(f8p5, 'A hundred thirty minus fifty-five'), mk('cross', 'choice 4', 'is a hundred fifteen. Out'),
        mk('tick', 'choice 3', 'So choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g072 (Hebrew: five identical rectangles)
# Hebrew (geo 3398-3438): the main difficulty is to see the fixed ratio between the length and the width of a small
# rectangle, which comes from how they are put together; width x, the marked rectangle covers three x's (ratio 1:3); label
# every side; the perimeter in x; x = 2; "we weren't asked for x, it's not in the choices"; area = base times height.
# English: six rectangles, ratio 1:4, perimeter 40, area 96. Course addition kept: the sides as a ratio 2:3 of half the
# perimeter. (The old "check from the answers" view is dropped: it re-solves the same equation.)
# V3: one stacked rectangle tinted, its short side x; the four x's up the stack; a standing rectangle tinted orange with
# its long side "4x" next to the stack; every side labelled (4x, x + 4x + x = 6x); values 8 and 12 written on the sides.
f8L, f8R, f8T, f8Bt = 174.0, 466.0, 82.667, 277.333
f8x1, f8x2 = 222.667, 417.333
f8_72base = [('seg', f8L, f8T, f8R, f8T), ('seg', f8R, f8T, f8R, f8Bt), ('seg', f8R, f8Bt, f8L, f8Bt), ('seg', f8L, f8Bt, f8L, f8T),
             ('seg', f8x1, f8T, f8x1, f8Bt), ('seg', f8x2, f8T, f8x2, f8Bt)] + \
            [('seg', f8x1, y, f8x2, y) for y in (131.333, 180.0, 228.667)] + \
            [('txt', 158, 66, 'A', 'ink', 24, True), ('txt', 158, 296, 'B', 'ink', 24, True),
             ('txt', 482, 296, 'C', 'ink', 24, True), ('txt', 482, 66, 'D', 'ink', 24, True)]
f8g72 = f8_pin(GEO('f8g72', [
    ('line', f8_72base),
    ('one', [('tint', [(f8x1, 228.667), (f8x2, 228.667), (f8x2, f8Bt), (f8x1, f8Bt)], 'teal'), ('txt', 392, 253, 'x', 'teal', 24, True)]),
    ('stack', [('txt', 392, 107, 'x', 'teal', 24, True), ('txt', 392, 156, 'x', 'teal', 24, True), ('txt', 392, 204, 'x', 'teal', 24, True)]),
    ('stand', [('tint', [(f8L, f8T), (f8x1, f8T), (f8x1, f8Bt), (f8L, f8Bt)], 'orange'), ('txt', 198, 180, '4x', 'orange', 24, True),
               ('txt', 198, 296, 'x', 'teal', 22, True)]),
    ('sides', [('txt', 140, 180, '4x', 'ink', 26, True), ('txt', 320, 300, 'x + 4x + x = 6x', 'ink', 22, True)]),
], vb='110 40 420 280', w=300, title='Rectangle ABCD made of six congruent rectangles'))
# 2026-10-18 (batch C #244): the labelled tile diagram stays on the board for the working; 8 and 12 go on those sides
f8_72lab = [('tint', [(f8L, f8T), (f8x1, f8T), (f8x1, f8Bt), (f8L, f8Bt)], 'orange'), ('txt', 198, 180, '4x', 'orange', 22, True),
            ('txt', 392, 253, 'x', 'teal', 22, True), ('txt', 140, 180, '4x', 'ink', 24, True), ('txt', 320, 300, '6x', 'ink', 24, True)]
f8g72b = f8_pin(GEO('f8g72b', [
    ('line', f8_72base + f8_72lab),
    ('v', [('wipe', 120, 165, 40, 30), ('txt', 140, 180, '8', 'red', 28), ('wipe', 290, 288, 60, 26), ('txt', 320, 300, '12', 'red', 28)]),
], vb='110 40 420 280', w=300, title='The tiles with their sides'))
f8g72c = f8_pin(GEO('f8g72c', [
    ('line', f8_72base + [('txt', 140, 180, '4x', 'ink', 24, True), ('txt', 320, 300, '6x', 'ink', 24, True)]),
    ('parts', [('seg', 150, f8T, 150, f8Bt, 'teal', 4), ('tick', 150, f8T, 150, 180, 1, 'teal'), ('tick', 150, 180, 150, f8Bt, 1, 'teal'),
               ('seg', f8L, 312, f8R, 312, 'orange', 4)] + [('tick', f8L + (f8R - f8L) * k / 3.0, 312, f8L + (f8R - f8L) * (k + 1) / 3.0, 312, 1, 'orange') for k in range(3)]
              + [('txt', 128, 140, '2', 'teal', 24), ('txt', 320, 334, '3 parts', 'orange', 22)]),
    ('v', [('txt', 128, 220, '= 8', 'red', 24), ('txt', 420, 334, '= 12', 'red', 22)]),
], vb='100 40 430 310', w=300, title='Two parts and three parts'))
_R(f8g72b, 222); _R(f8g72c, 222)
f8q = [IH('f8q%d' % i, t, size=24) for i, t in enumerate(['$P=2(4x+6x)$', '$=20x=40$', '$x=\\frac{40}{20}=2$', '$4x=8,\\ 6x=12$', '$S=8\\cdot12=96$'])]
f8uu = [IH('f8u%d' % i, t, size=24) for i, t in enumerate(['$4x:6x=2:3$', '$\\frac{40}{2}=20$', '$2+3=5$ parts', '$\\frac{20}{5}=4$',
                                                         '$2\\cdot4=8,\\ 3\\cdot4=12$', '$8\\cdot12=96$'])]
for _rows in (f8q, f8uu):
    for _k, _x in enumerate(_rows): _R(_x, 222 + 52 * _k, x=1350)
f8r2 = I('f8r2', '$P=2(4x+6x)=20x=40\\ \\Rightarrow\\ x=2$', size=25)
f8r2b = I('f8r2b', '$4x=8,\\ \\ 6x=12$', size=30)
f8r3 = I('f8r3', '$S=4x\\cdot6x=8\\cdot12=96$', size=30)
f8r4 = IH('f8r4', 'sides $4x:6x=2:3$, $\\ $half the perimeter $20$', size=26)
f8r5 = IH('f8r5', '$20\\div5=4$: $\\ 2\\cdot4=8,\\ \\ 3\\cdot4=12$', size=28)
video('solve-geo32-g072', 'solution', qid='geo32-g072', slides=[
    SM('Method 1 · The math way', 'The hidden ratio',
      L("Rectangle A B C D consists of six congruent rectangles, arranged as in the accompanying figure. The perimeter of A B "
        "C D is forty centimeters. What is its area, in square centimeters?", pt('stem', 'Rectangle A B C D', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("The main difficulty here is to see that each small rectangle has a fixed ratio between its long side and its short "
        "side. That ratio comes from the way the six rectangles fit together. [short pause] We'll find the ratio first, and "
        "then the perimeter and the area.", pt('stem', 'a fixed ratio')),
      L("[short pause] Call the short side of a small rectangle x. Look at one of the lying rectangles in the middle. Its "
        "short side is x. All six are the same, so each of the four lying rectangles is x high.",
        show(f8g72['line'], 'Call the short side'), show(f8g72['one'], 'Look at one of the lying rectangles'),
        show(f8g72['stack'], 'each of the four lying rectangles')),
      L("Now look at a standing rectangle on the side. Its long side is as tall as the four lying rectangles together, four "
        "x's. So the long side is four x, and the ratio is one to four.", show(f8g72['stand'], 'Now look at a standing rectangle')),
      L("Now every side of A B C D. The height is four x. Across, there's x, then four x, then x again, so the width is six x.",
        show(f8g72['sides'], 'Now every side of A B C D'))),
    SM('Method 1 · The math way', 'Perimeter and area',
      L("Here are the sides again, four x and six x. The perimeter is two times, four x plus six x, which is twenty x.",
        show(f8g72b['line'], 'Here are the sides again'), show(f8q[0], 'The perimeter is two times'), show(f8q[1], 'which is twenty x')),
      L("The perimeter is forty, so twenty x is forty. Divide forty by twenty, so x is two.", show(f8q[2], 'Divide forty by twenty')),
      L("Careful, nobody asked for x, and two isn't even a choice. They asked for the area, base times height. Four x is "
        "eight, and six x is twelve. Eight times twelve is ninety-six. Choice number three is our answer.",
        show(f8q[3], 'Four x is eight'), show(f8g72b['v'], 'and six x is twelve'), show(f8q[4], 'Eight times twelve'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Understanding', 'Parts of the perimeter',
      L("[pause] Now by understanding, with a different finish. We start from the same tiles, which gave us the sides four x "
        "and six x. So the sides are in the ratio two to three, because four x to six x is like four to six, two to three.",
        show(f8g72c['line'], 'We start from the same tiles'), show(f8uu[0], 'So the sides are in the ratio'), show(f8g72c['parts'], 'two to three, because')),
      L("Half the perimeter, one height plus one width, is half of forty, twenty.", show(f8uu[1], 'is half of forty')),
      L("Two parts plus three parts is five parts. Five parts are twenty, so one part is twenty over five, four.",
        show(f8uu[2], 'Two parts plus three parts'), show(f8uu[3], 'so one part is twenty over five')),
      L("The sides are two times four, eight, and three times four, twelve. Eight times twelve is ninety-six again. [pause] "
        "Okay. I'll see you in the next question.", show(f8uu[4], 'The sides are two times four'), show(f8g72c['v'], 'and three times four, twelve'),
        show(f8uu[5], 'Eight times twelve'), mk('tick', 'choice 3', 'is ninety-six again'))),
])

# ------------------------------------------------------------------------------------------------ r26-t32-perimeter (lesson, course addition)
# Two perimeter tricks, each with two examples and a non-example: a cut is counted twice (the pieces' perimeters add up to
# the original plus twice each cut); a notch adds twice its depth (a corner step adds nothing, preview of the staircase).
# V3: a generic 10 x 6 rectangle; the cut drawn dashed as named, each piece tinted in its own colour; the cut traced red
# twice ("it belongs to both"); the notch: its bottom pushed up (dashed arrows), the two walls in orange as "extra".
f8u = 36   # px per unit; rectangle 10 x 6 at (140, 60)
f8X0, f8Y0 = 140, 60
f8_rect = [('seg', f8X0, f8Y0, f8X0 + 10 * f8u, f8Y0), ('seg', f8X0 + 10 * f8u, f8Y0, f8X0 + 10 * f8u, f8Y0 + 6 * f8u),
           ('seg', f8X0 + 10 * f8u, f8Y0 + 6 * f8u, f8X0, f8Y0 + 6 * f8u), ('seg', f8X0, f8Y0 + 6 * f8u, f8X0, f8Y0),
           ('txt', f8X0 + 5 * f8u, f8Y0 - 18, '10', 'ink', 26), ('txt', f8X0 - 22, f8Y0 + 3 * f8u, '6', 'ink', 26)]
f8cx = f8X0 + 4 * f8u
f8cut = f8_pin(GEO('f8cut', [
    ('line', f8_rect),
    ('cut', [('seg', f8cx, f8Y0, f8cx, f8Y0 + 6 * f8u, 'teal', 4, True)]),
    ('pieces', [('tint', [(f8X0, f8Y0), (f8cx, f8Y0), (f8cx, f8Y0 + 6 * f8u), (f8X0, f8Y0 + 6 * f8u)], 'teal'),
                ('tint', [(f8cx, f8Y0), (f8X0 + 10 * f8u, f8Y0), (f8X0 + 10 * f8u, f8Y0 + 6 * f8u), (f8cx, f8Y0 + 6 * f8u)], 'orange'),
                ('txt', f8X0 + 2 * f8u, f8Y0 + 3 * f8u, '4 × 6', 'teal', 26), ('txt', f8X0 + 7 * f8u, f8Y0 + 3 * f8u, '6 × 6', 'orange', 26)]),
    ('twice', [('seg', f8cx - 5, f8Y0 + 4, f8cx - 5, f8Y0 + 6 * f8u - 4, 'red', 5), ('seg', f8cx + 5, f8Y0 + 4, f8cx + 5, f8Y0 + 6 * f8u - 4, 'red', 5),
               ('txt', f8cx, f8Y0 + 6 * f8u + 26, 'counted twice', 'red', 22)]),
], vb='90 20 470 300', w=600, col=0, title='A 10 by 6 rectangle cut into two'))
# 2026-10-18 (batch C #245): every perimeter written at its clause; the cut ACROSS gets its own figure (a 10-long cut)
f8cy = f8Y0 + 2 * f8u
f8cut2 = f8_pin(GEO('f8cut2', [
    ('line', f8_rect),
    ('cut', [('seg', f8X0, f8cy, f8X0 + 10 * f8u, f8cy, 'teal', 4, True)]),
    ('pieces', [('tint', [(f8X0, f8Y0), (f8X0 + 10 * f8u, f8Y0), (f8X0 + 10 * f8u, f8cy), (f8X0, f8cy)], 'teal'),
                ('tint', [(f8X0, f8cy), (f8X0 + 10 * f8u, f8cy), (f8X0 + 10 * f8u, f8Y0 + 6 * f8u), (f8X0, f8Y0 + 6 * f8u)], 'orange'),
                ('txt', f8X0 + 5 * f8u, f8Y0 + f8u, '10 × 2', 'teal', 26), ('txt', f8X0 + 5 * f8u, f8Y0 + 4 * f8u, '10 × 4', 'orange', 26)]),
    ('twice', [('seg', f8X0 + 4, f8cy - 5, f8X0 + 10 * f8u - 4, f8cy - 5, 'red', 5), ('seg', f8X0 + 4, f8cy + 5, f8X0 + 10 * f8u - 4, f8cy + 5, 'red', 5)]),
], vb='90 20 470 300', w=600, col=0, title='The same rectangle cut across'))
f8c = [IH('f8cc%d' % i, t, size=30, col=1) for i, t in enumerate(['$P=2(10+6)=32$', '$P_1=2(4+6)=20$', '$P_2=2(6+6)=24$', '$20+24=44$', '$44=32+2\\cdot6$'])]
f8d = [IH('f8d%d' % i, t, size=30, col=1) for i, t in enumerate(['$2(10+2)=24$', '$2(10+4)=28$', '$24+28=52$', '$52=32+2\\cdot10$'])]
f8c4 = I('f8c4', 'Pieces $=$ original $+\\ 2\\times$ each cut', size=28, col=1)
f8ny = f8Y0 + 2 * f8u; f8n1x, f8n2x = f8X0 + 4 * f8u, f8X0 + 7 * f8u
f8notch = f8_pin(GEO('f8notch', [
    ('line', [('seg', f8X0, f8Y0, f8n1x, f8Y0), ('seg', f8n1x, f8Y0, f8n1x, f8ny), ('seg', f8n1x, f8ny, f8n2x, f8ny),
              ('seg', f8n2x, f8ny, f8n2x, f8Y0), ('seg', f8n2x, f8Y0, f8X0 + 10 * f8u, f8Y0),
              ('seg', f8X0 + 10 * f8u, f8Y0, f8X0 + 10 * f8u, f8Y0 + 6 * f8u), ('seg', f8X0 + 10 * f8u, f8Y0 + 6 * f8u, f8X0, f8Y0 + 6 * f8u),
              ('seg', f8X0, f8Y0 + 6 * f8u, f8X0, f8Y0), ('txt', f8X0 + 5 * f8u, f8Y0 + 6 * f8u + 26, '10', 'ink', 26),
              ('txt', f8X0 - 22, f8Y0 + 3 * f8u, '6', 'ink', 26)]),
    ('up', [('seg', f8n1x, f8ny, f8n2x, f8ny, 'teal', 5), ('seg', f8n1x, f8Y0, f8n2x, f8Y0, 'teal', 4, True),
            ('seg', f8n1x + 54, f8ny - 8, f8n1x + 54, f8Y0 + 10, 'teal', 2.5, True), ('txt', (f8n1x + f8n2x) / 2, f8ny + 26, 'push up', 'teal', 22)]),
    ('walls', [('seg', f8n1x, f8Y0, f8n1x, f8ny, 'orange', 6), ('seg', f8n2x, f8Y0, f8n2x, f8ny, 'orange', 6),
               ('txt', f8n1x - 30, f8Y0 + f8u, '2', 'orange', 24), ('txt', f8n2x + 26, f8Y0 + f8u, '2', 'orange', 24)]),
], vb='90 20 470 300', w=600, col=0, title='A 10 by 6 rectangle with a notch 2 deep'))
f8t1 = IH('f8t1', '$P=32+2\\cdot2=36$', size=30, col=1)
f8ny3 = f8Y0 + 3 * f8u
f8notch3 = f8_pin(GEO('f8notch3', [
    ('line', [('seg', f8X0, f8Y0, f8n1x, f8Y0), ('seg', f8n1x, f8Y0, f8n1x, f8ny3, 'orange', 6), ('seg', f8n1x, f8ny3, f8n2x, f8ny3),
              ('seg', f8n2x, f8ny3, f8n2x, f8Y0, 'orange', 6), ('seg', f8n2x, f8Y0, f8X0 + 10 * f8u, f8Y0),
              ('seg', f8X0 + 10 * f8u, f8Y0, f8X0 + 10 * f8u, f8Y0 + 6 * f8u), ('seg', f8X0 + 10 * f8u, f8Y0 + 6 * f8u, f8X0, f8Y0 + 6 * f8u),
              ('seg', f8X0, f8Y0 + 6 * f8u, f8X0, f8Y0), ('txt', f8X0 + 5 * f8u, f8Y0 + 6 * f8u + 26, '10', 'ink', 26),
              ('txt', f8X0 - 22, f8Y0 + 3 * f8u, '6', 'ink', 26), ('txt', f8n1x - 30, f8Y0 + 1.5 * f8u, '3', 'orange', 24),
              ('txt', f8n2x + 26, f8Y0 + 1.5 * f8u, '3', 'orange', 24)]),
], vb='90 20 470 300', w=420, col=0, title='A notch 3 deep'))
f8kx, f8ky = f8X0 + 7 * f8u, f8Y0 + 2 * f8u          # a corner step: 3 wide, 2 deep, cut from the top right corner
f8corner = f8_pin(GEO('f8corner', [
    ('line', [('seg', f8X0, f8Y0, f8kx, f8Y0), ('seg', f8kx, f8Y0, f8kx, f8ky), ('seg', f8kx, f8ky, f8X0 + 10 * f8u, f8ky),
              ('seg', f8X0 + 10 * f8u, f8ky, f8X0 + 10 * f8u, f8Y0 + 6 * f8u), ('seg', f8X0 + 10 * f8u, f8Y0 + 6 * f8u, f8X0, f8Y0 + 6 * f8u),
              ('seg', f8X0, f8Y0 + 6 * f8u, f8X0, f8Y0), ('txt', f8X0 + 5 * f8u, f8Y0 + 6 * f8u + 26, '10', 'ink', 26),
              ('txt', f8X0 - 22, f8Y0 + 3 * f8u, '6', 'ink', 26)]),
    ('match', [('seg', f8kx, f8ky, f8X0 + 10 * f8u, f8ky, 'teal', 6), ('seg', f8kx, f8Y0, f8X0 + 10 * f8u, f8Y0, 'teal', 3, True),
               ('seg', f8kx, f8Y0, f8kx, f8ky, 'orange', 6), ('seg', f8X0 + 10 * f8u, f8Y0, f8X0 + 10 * f8u, f8ky, 'orange', 3, True),
               ('txt', f8kx + 1.5 * f8u, f8ky + 22, '3', 'teal', 22), ('txt', f8kx - 20, f8Y0 + f8u, '2', 'orange', 22)]),
], vb='90 20 470 300', w=420, col=0, title='A step cut from a corner'))
f8t2 = IH('f8t2', '$P=32+2\\cdot3=38$', size=30, col=1)
f8t3 = IH('f8t3', 'corner step: $\\ P=32$', size=30, col=1)
video('r26-t32-perimeter', 'lesson', slides=[
    S('Perimeter Tricks',
      L("Let's look at two useful perimeter shortcuts. They turn long perimeter questions into one line, and there's a "
        "third one in the next question.")),
    S('A cut counts twice',
      L("Here's a rectangle, ten by six. Its perimeter is two times, ten plus six, which is thirty-two.",
        show(f8cut['line'], "Here's a rectangle"), show(f8c[0], 'Its perimeter is two times')),
      L("Now cut it into two smaller rectangles, four by six and six by six.", show(f8cut['cut'], 'Now cut it'),
        show(f8cut['pieces'], 'four by six and six by six')),
      L("The perimeter of the first piece is two times, four plus six, twenty. The second is two times, six plus six, "
        "twenty-four. Together, forty-four. That's more than thirty-two. Why?", show(f8c[1], 'The perimeter of the first piece'),
        show(f8c[2], 'The second is two times'), show(f8c[3], 'Together, forty-four')),
      L("Every outside side is counted once, just like before. But the cut is a side of both pieces, so it's counted twice. "
        "The cut is six, so the pieces add up to thirty-two plus two times six, forty-four.",
        show(f8cut['twice'], "so it's counted twice"), show(f8c[4], 'the pieces add up to thirty-two'))),
    S('Cut across', 
      L("Now cut the same rectangle across instead, with a cut ten long. We get ten by two and ten by four.",
        show(f8cut2['line'], 'Now cut the same rectangle across'), show(f8cut2['cut'], 'with a cut ten long'),
        show(f8cut2['pieces'], 'We get ten by two')),
      L("Ten by two has a perimeter of two times, ten plus two. That's twenty-four. Ten by four has two times, ten plus "
        "four. That's twenty-eight. Together, that's fifty-two.", show(f8d[0], 'Ten by two has a perimeter'), show(f8d[1], 'Ten by four has'),
        show(f8d[2], "Together, that's fifty-two")),
      L("And that's thirty-two plus two times ten. This cut is ten long, and it's counted twice.",
        show(f8cut2['twice'], 'This cut is ten long'), show(f8d[3], "And that's thirty-two plus")),
      L("So the rule, for straight cuts like these: the pieces add up to the original perimeter plus two times each cut.",
        show(f8c4, 'So the rule')), sb='A cut counts twice'),
    S('A notch adds',
      L("Now let's look at a notch. The border goes into the shape and comes back out. Here it's a rectangular notch, two deep.",
        show(f8notch['line'], 'look at a notch')),
      L("The bottom of the notch is a horizontal segment. Slide it straight up to the top line. It keeps its length, and "
        "it fills exactly the gap in the top side. So the width is covered once, ten, just like the plain rectangle.",
        show(f8notch['up'], 'Slide it straight up')),
      L("But the two walls of the notch have nowhere to go. They are extra. Each one is two, so the perimeter is thirty-two "
        "plus two times two, thirty-six.", show(f8notch['walls'], 'But the two walls'), show(f8t1, 'thirty-two plus two times two'))),
    S('Deeper, and a corner',
      L("A notch three deep has walls of three. So it adds two times three, six, and the perimeter is thirty-eight.",
        show(f8notch3['line'], 'A notch three deep'), show(f8t2, 'and the perimeter is thirty-eight')),
      L("Careful, a step cut out at a corner is not a notch. Its new bottom side matches the piece of the top side that "
        "was cut away, three. Its new wall matches the piece of the right side that was cut away, two. So it adds "
        "nothing, and the perimeter stays thirty-two.", show(f8corner['line'], 'a step cut out at a corner'),
        show(f8corner['match'], 'Its new bottom side matches'), show(f8t3, 'the perimeter stays thirty-two')),
      L("These rules are for straight, rectangular cuts like these. You'll see the corner idea again in the next "
        "question. [pause] Okay. I'll see you in the next video.", pt('f8corner_line', 'These rules are for straight'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t32-06 (course addition: the staircase)
# Push every horizontal step up to the top line and every vertical step out to the side: no length changes, the outline
# becomes the 12 by 8 rectangle. Traps: "cannot be determined" and 96 (the area).
# V3: the horizontal steps traced teal, then shown pushed up onto the top line (dashed arrows), "12"; the vertical steps
# traced orange, then pushed out to the right side, "8"; the full rectangle traced, P = 40 written.
f8H = [((130, 60), (220, 60)), ((220, 90), (310, 90)), ((310, 150), (400, 150)), ((400, 210), (490, 210))]
f8V = [((220, 60), (220, 90)), ((310, 90), (310, 150)), ((400, 150), (400, 210)), ((490, 210), (490, 300))]
f8_06base = [('seg', 130, 300, 490, 300), ('seg', 130, 60, 130, 300)] + [('seg', *p, *q) for p, q in f8H + f8V] + \
            [('txt', 310, 325, '12', 'ink', 26), ('txt', 108, 180, '8', 'ink', 26)]
f8g06 = f8_pin(GEO('f8g06', [
    ('line', f8_06base),
    ('h', [('seg', *p, *q, 'teal', 6) for p, q in f8H]),
    ('hup', [('dim', 90, 30, 470, 305)] + [('seg', p[0], 60, q[0], 60, 'teal', 6) for p, q in f8H] +
            [('seg', (p[0] + q[0]) / 2, p[1] - 4, (p[0] + q[0]) / 2, 66, 'teal', 2.5, True) for p, q in f8H[1:]] +
            [('txt', 310, 44, '12', 'teal', 26)]),
    ('v', [('seg', *p, *q, 'orange', 6) for p, q in f8V]),
    ('vout', [('seg', 490, p[1], 490, q[1], 'orange', 6) for p, q in f8V] +
             [('seg', p[0] + 4, (p[1] + q[1]) / 2, 484, (p[1] + q[1]) / 2, 'orange', 2.5, True) for p, q in f8V[:3]] +
             [('txt', 514, 180, '8', 'orange', 26)]),
    ('rect', [('path', [(130, 60), (490, 60), (490, 300), (130, 300), (130, 60)], 'teal', 4)]),
], vb='90 30 470 305', w=360, title='The staircase figure'))
f8s1 = IH('f8s1', '$P=12+8+12+8=40$', size=30)
video('solve-q-r26-t32-06', 'solution', qid='q-r26-t32-06', slides=[
    SM('Push the steps out', 'Push the steps out',
      L("All the angles in the accompanying figure are right angles. The figure is twelve centimeters wide and eight "
        "centimeters tall, as marked. What is its perimeter, in centimeters?", pt('stem', 'All the angles', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("We don't know the length of a single step, so many students choose cannot be determined. But here the stair path "
        "only goes right and down, with no part going back in. [short pause] Let's see why that's enough.",
        pt('choice 4', 'cannot be determined')),
      L("[short pause] Look at all the horizontal steps. Each one keeps its length when we slide it straight up to the top "
        "line. Together they cover the whole top once, with no overlap and no gap. So together they're twelve.",
        show(f8g06['line'], 'Look at all the horizontal steps'), show(f8g06['h'], 'Look at all the horizontal steps'),
        show(f8g06['hup'], 'when we slide it straight up')),
      L("Now the vertical steps. Slide each one out to the right side. They cover the whole right side once, from top to "
        "bottom. So together they're eight.", show(f8g06['v'], 'Now the vertical steps'), show(f8g06['vout'], 'Slide each one out')),
      L("The bottom, twelve, and the left side, eight, don't change. So the perimeter is twelve plus eight plus twelve plus "
        "eight, which is forty. Choice number two is our answer.", show(f8g06['rect'], "don't change"),
        show(f8s1, 'twelve plus eight plus twelve'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Careful, this works because the path only goes right and down. A rectangular notch going back in would add its "
        "two walls, like in the last lesson. And ninety-six is twelve times eight. That's an area, not a perimeter. [pause] "
        "Okay. I'll see you in the next question.", mk('cross', 'choice 3', 'ninety-six is twelve times eight'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t32-07 (course addition)
# Method 1: a + b = 17 and a² + b² = 169; the shortcut formula (a + b)² = a² + 2ab + b² (topic 4) gives 2ab = 120, ab = 60.
# Method 2: 13 suggests the triple 5, 12, 13; sides 5 and 12 fit the perimeter too; the question has one area, so 60.
# Traps: 120 (2ab), 30 (half), 65 (the diagonal as a side).
# V3: a and b written on two sides; the half perimeter traced (top + left); triangle ABC tinted with the diagonal orange
# and the right angle at B; method 2 on a new copy: 5 and 12 written on the sides.
f8a, f8b, f8c, f8d = (150, 90), (150, 270), (490, 270), (490, 90)
f8_07base = [('seg', *f8a, *f8b), ('seg', *f8b, *f8c), ('seg', *f8c, *f8d), ('seg', *f8d, *f8a), ('seg', *f8a, *f8c),
             ('txt', 134, 74, 'A', 'ink', 24, True), ('txt', 134, 288, 'B', 'ink', 24, True), ('txt', 506, 288, 'C', 'ink', 24, True),
             ('txt', 506, 74, 'D', 'ink', 24, True), ('txt', 330, 160, '13', 'ink', 24)]
f8g07 = f8_pin(GEO('f8g07', [
    ('line', f8_07base),
    ('ab', [('txt', 126, 180, 'b', 'teal', 28, True), ('txt', 320, 296, 'a', 'teal', 28, True)]),
    ('half', [('path', [(150, 90), (150, 270), (490, 270)], 'teal', 6), ('txt', 250, 245, 'a + b = 17', 'teal', 26)]),
    ('tri', [('tint', [f8a, f8b, f8c], 'teal'), ('seg', *f8a, *f8c, 'orange', 5), ('right', 150, 270, 0, 90, 14),
             ('txt', 405, 125, 'a² + b² = 169', 'orange', 26)]),
], vb='100 50 440 270', w=300, title='Rectangle ABCD with the diagonal AC'))
# 2026-10-18 (batch C #247): squaring a sum is taught here (identities come later in the plan): what it means, the four
# products, why 2ab, two checks and the a^2 + b^2 trap; then 17^2 and every step of the solution at its clause
f8e1 = I('f8e1', '$a+b=17\\qquad a^2+b^2=169$', size=28)
f8sq = [IH('f8sq%d' % i, t, size=30) for i, t in enumerate(['$(a+b)^2=(a+b)(a+b)$', '$=a^2+ab+ba+b^2$', '$=a^2+2ab+b^2$',
                                                           '$(2+3)^2=5^2=25$', '$4+12+9=25$'])]
f8sq2 = [IH('f8sqb%d' % i, t, size=30) for i, t in enumerate(['$(3+1)^2=4^2=16$', '$9+6+1=16$', '$2^2+3^2=13$ ✗'])]
f8e = [IH('f8ee%d' % i, t, size=26) for i, t in enumerate(['$17\\cdot10=170$', '$17\\cdot7=119$', '$17^2=170+119=289$',
                                                         '$289=169+2ab$', '$2ab=289-169=120$', '$ab=\\frac{120}{2}=60$'])]
f8g07b = f8_pin(GEO('f8g07b', [
    ('line', f8_07base),
    ('sides', [('txt', 126, 180, '5', 'teal', 28), ('txt', 320, 296, '12', 'teal', 28)]),
    ('perim', [('txt', 320, 72, 'P = 2(5 + 12) = 34 ✓', 'teal', 24)]),
    ('area', [('tint', [f8a, f8b, f8c, f8d], 'orange'), ('txt', 250, 235, 'S = 5 · 12 = 60', 'orange', 26)]),
], vb='100 50 440 270', w=300, title='Sides 5 and 12'))
video('solve-q-r26-t32-07', 'solution', qid='q-r26-t32-07', slides=[
    SM('Method 1 · The math way: shortcut formula', 'A shortcut formula',
      L("A rectangle has a perimeter of thirty-four centimeters, and its diagonal is thirteen centimeters long. What is its "
        "area, in square centimeters?", pt('stem', 'A rectangle has a perimeter', 'hl', 7.0), voice='calm', pause=0.5),
      L("We know the perimeter and the diagonal, but not the sides. [short pause] We'll solve it in two different ways. "
        "First the math way, with a formula for squaring a sum, and then by understanding, with a Pythagorean triple."),
      L("[short pause] Let's start with the math way. Call the sides a and b. Half the perimeter is one a and one b, so a "
        "plus b is seventeen.", show(f8g07['line'], 'Call the sides a and b'), show(f8g07['ab'], 'Call the sides a and b'),
        show(f8g07['half'], 'Half the perimeter')),
      L("The diagonal makes a right triangle with two sides of the rectangle. By Pythagoras, a squared plus b squared is "
        "thirteen squared, a hundred sixty-nine.", show(f8g07['tri'], 'The diagonal makes a right triangle'))),
    SM('Method 1 · The math way: shortcut formula', 'Squaring a sum',
      L("We want the area, a times b. There's a tool for this, squaring a sum. a plus b, squared, means a plus b, times a "
        "plus b.", show(f8sq[0], 'squared, means')),
      L("We multiply each part by each part. a times a is a squared. a times b is a b. b times a is another a b. And b "
        "times b is b squared.", show(f8sq[1], 'We multiply each part by each part')),
      L("The two a b terms are the same, so together they're two a b. So a plus b, squared, is a squared plus two a b plus "
        "b squared.", show(f8sq[2], 'The two a b terms are the same')),
      L("Let's check it. Two plus three is five, so it's five squared. That's twenty-five. With the formula, two "
        "squared is four. Two times two times three is twelve. And three squared is nine. Four plus twelve plus nine is twenty-five too.",
        show(f8sq[3], 'Two plus three is five'), show(f8sq[4], 'Four plus twelve plus nine')),
      L("Let's do another one. Three plus one is four. Four squared is sixteen. With the formula, nine plus six plus one is "
        "sixteen.", show(f8sq2[0], 'Three plus one is four'), show(f8sq2[1], 'nine plus six plus one')),
      L("Careful, a plus b, squared, is not a squared plus b squared. Two squared plus three squared is only thirteen, not "
        "twenty-five. The two a b is missing.", show(f8sq2[2], 'Two squared plus three squared'))),
    SM('Method 1 · The math way: shortcut formula', 'Back to the rectangle',
      L("Now back to our rectangle. We know a plus b is seventeen. And a squared plus b squared is a hundred sixty-nine.",
        show(f8e1, 'Now back to our rectangle')),
      L("So a plus b, squared, is seventeen squared. Seventeen times ten is a hundred seventy. Seventeen times seven is a "
        "hundred nineteen. Together, that's two hundred eighty-nine.", show(f8e[0], 'Seventeen times ten'),
        show(f8e[1], 'Seventeen times seven'), show(f8e[2], "Together, that's two hundred")),
      L("By the formula, two hundred eighty-nine is a squared plus b squared, plus two a b. So it's a hundred sixty-nine "
        "plus two a b.", show(f8e[3], "So it's a hundred sixty-nine")),
      L("Two hundred eighty-nine minus a hundred sixty-nine is a hundred twenty, so two a b is a hundred twenty. Careful, "
        "a hundred twenty is choice number three, but it's two a b, not the area.", show(f8e[4], 'Two hundred eighty-nine minus'),
        mk('cross', 'choice 3', 'a hundred twenty is choice number three')),
      L("We want a b alone, so we divide both sides by two. That gives a b is sixty. Choice number one is our answer.",
        show(f8e[5], 'we divide both sides by two'), mk('tick', 'choice 1', 'Choice number one is our answer'))),
    SM('Method 2 · Understanding: a triple', 'A triple',
      L("[pause] Now by understanding, with a triple. A diagonal of thirteen should remind us of the triple five, twelve, "
        "thirteen. Let's try sides five and twelve. Their diagonal is thirteen, so they fit the diagonal.",
        show(f8g07b['line'], 'Now by understanding'), show(f8g07b['sides'], "Let's try sides")),
      L("Careful, thirteen is the diagonal, not a side. Five times thirteen, sixty-five, is choice number two, and that's "
        "a trap.", mk('cross', 'choice 2', 'Five times thirteen, sixty-five')),
      L("Now check the other given, the perimeter. Five plus twelve is seventeen, and two times seventeen is thirty-four. So this rectangle fits both "
        "givens, and its area is five times twelve, sixty. The math way already showed that every rectangle with these "
        "givens has area sixty. Choice number one again.", show(f8g07b['perim'], 'Now check the other given'),
        show(f8g07b['area'], 'its area is five times twelve'), mk('tick', 'choice 1', 'Choice number one again')),
      L("And thirty, choice number four, is half of sixty. That's the area of the triangle A B C, not of the rectangle. "
        "[pause] Okay. I'll see you in the next question.", mk('cross', 'choice 4', 'And thirty, choice number four'))),
])


# typed lines of the question videos: the right column, under the colour copy (the left column is the question figure)
def f8_col(y0, *items, dy=54):
    for k, it in enumerate(items): _R(it, y0 + k * dy)


_R(f8g71, 222); _R(f8g71b, 222); _R(f8g72, 222); _R(f8g06, 222); _R(f8g07, 222); _R(f8g07b, 222)
f8_col(222, f8n0, f8n0b, f8n1, f8n2, f8n3, f8n3b, f8n4, dy=54)
for _k, _x in enumerate(f8m): _R(_x, 222 + 52 * _k, x=1335)
f8_col(226, f8p0, f8p3, f8p6, f8p4, f8p5, dy=52)

_R(f8s1, 470)
for _k, _x in enumerate(f8sq): _R(_x, 222 + 64 * _k, x=420)
for _k, _x in enumerate(f8sq2): _R(_x, 222 + 64 * _k, x=1000)
NOFIG32.add(('solve-q-r26-t32-07', 1))
f8_col(222, f8e1, *f8e, dy=52)

# carry-over boxes on the continuation slides (V2): the next step uses these results
CARRY32 = globals().get('CARRY32', {})

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
 "geo32-g066": "Which of the following statements is not necessarily true?",
 "geo32-g067": "ABCD is a rectangle, and E lies on AD. The areas of triangles ABE and ECD are 6 cm² and 15 cm², respectively. What is the area of the shaded triangle EBC (in cm²)?",
 "geo32-g068": "ABCD is a rectangle. E lies on AD, G lies on BC, and F lies on AB. Given:\n$\\begin{cases} AE=3ED \\\\ BG=3GC \\end{cases}$\nTriangles FEG and EGC are shaded. Which of the following additional data is sufficient to determine the total shaded area?",
 "geo32-g069": "ABCD is an isosceles trapezoid. Given:\n$\\begin{cases} AD\\parallel BC \\\\ AD=5\\text{ cm} \\\\ BC=20\\text{ cm} \\end{cases}$\nThe shaded triangle ABD has area 15 cm². What is the area of the trapezoid (in cm²)?",
 "geo32-g070": "The rectangle in the accompanying figure consists of 40 congruent squares, each with side length 1 cm. What is the shaded area (in cm²)?",
 "geo32-g071": "In quadrilateral ABCD, angle A is α, angle B is 130° and angle C is β. E lies on AB, and DE bisects angle ADC. Which expression equals angle AED?",
 "geo32-g072": "Rectangle ABCD consists of six congruent rectangles, arranged as in the accompanying figure. The perimeter of ABCD is 40 cm. What is its area (in cm²)?",
 "geo32-g057": "The accompanying figure shows quadrilateral ABCD. Given: angle A is 118° and angle B is 96°. Which of the following cannot be the value of α?",
 "geo32-g058": "ABCD is a parallelogram, and E lies on AD. Given:\n$\\begin{cases} AB=9\\text{ cm} \\\\ AE=4\\text{ cm} \\\\ \\angle ABC=72° \\\\ \\angle BCE=54° \\end{cases}$\nWhat is the perimeter of the parallelogram (in cm)?",
 "geo32-g059": "The diagonals of rectangle ABCD intersect at E. Given: $BC=24$ cm, and the perimeter of triangle EBC is 50 cm. What is the area of triangle ABE (in cm²)?",
 "geo32-g060": "ABCD is a rhombus. Given:\n$\\begin{cases} BD=10\\text{ cm} \\\\ \\angle ABD=60° \\end{cases}$\nWhat is the area of the rhombus (in cm²)?",
 "geo32-g061": "ABCD is a square, and P is a point inside it such that triangle BPC is equilateral. What is angle PAD?",
 "geo32-g062": "ABCD is a deltoid, and its diagonals meet at O. Given:\n$\\begin{cases} AB=AD=17\\text{ cm} \\\\ CB=CD \\\\ BO=15\\text{ cm} \\\\ OC=12\\text{ cm} \\end{cases}$\nWhat is the area of the deltoid (in cm²)?",
 "geo32-g063": "ABCD is an isosceles trapezoid with $AD\\parallel BC$. Given:\n$\\begin{cases} AB=AD=7\\text{ cm} \\\\ \\angle ABD=30° \\end{cases}$\nWhat is its perimeter (in cm)?",
 "geo32-g044": "The diagonal of a square is 14 cm long. What is the area of the square (in cm²)?",
 "geo32-g046": "The diagonals of rectangle ABCD intersect at E. Given:\n$\\begin{cases} CD=5\\text{ cm} \\\\ \\angle BEC=120° \\end{cases}$\nWhat is the area of the rectangle (in cm²)?",
 "geo32-g048": "In parallelogram ABCD, the marked parts of angle B are $3\\alpha$ and $2\\alpha$, and the marked parts of angle C are $3\\beta$ and $2\\beta$. The segments BE and CE meet as in the accompanying figure. What is x?",
 "geo32-g049": "ABCD is a parallelogram, and $AE\\perp BC$. Given:\n$\\begin{cases} AD=24\\text{ cm} \\\\ CD=17\\text{ cm} \\\\ EC=16\\text{ cm} \\end{cases}$\nWhat is the area of the parallelogram (in cm²)?",
 "geo32-g051": "The sum of the lengths of the diagonals of a rhombus is 46 cm. The absolute difference between their lengths is 14 cm. What is its perimeter (in cm)?",
 "geo32-g053": "ABCD is a deltoid. Given:\n$\\begin{cases} AB=AD \\\\ CB=CD=10\\text{ cm} \\\\ \\angle ABD=45° \\\\ \\angle DBC=60° \\end{cases}$\nWhat is the perimeter of the deltoid (in cm)?",
 "geo32-g055": "The area of isosceles trapezoid ABCD is 65 cm². DE is an altitude, $DE=5$ cm, and the area of triangle DEC is 10 cm². What is AD (in cm)?",
 "q-r26-t32-01": "ABCD is a parallelogram. Given:\n$\\begin{cases} AB=10\\text{ cm} \\\\ BC=14\\text{ cm} \\\\ \\angle ABC=150° \\end{cases}$\nWhat is the area of the parallelogram (in cm²)?",
 "q-r26-t32-02": "ABCD is a right trapezoid with $AD\\parallel BC$ and $\\angle ABC=90°$. Given:\n$\\begin{cases} AD=9\\text{ cm} \\\\ BC=15\\text{ cm} \\\\ CD=10\\text{ cm} \\end{cases}$\nWhat is the area of the trapezoid (in cm²)?",
 "q-r26-t32-06": "All the angles in the accompanying figure are right angles. The figure is 12 cm wide and 8 cm tall, as marked. What is its perimeter (in cm)?",
 "q-r26-t32-07": "A rectangle has a perimeter of 34 cm, and its diagonal is 13 cm long. What is its area (in cm²)?"
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



# the camera lesson in parts of about 3-4 minutes (math_patches/_camera_parts.py), before the visual passes
_cp_spec = importlib.util.spec_from_file_location('_camera_parts', os.path.join(HERE, '_camera_parts.py'))
CP = importlib.util.module_from_spec(_cp_spec); _cp_spec.loader.exec_module(CP)
if 'CAMERA_SPLIT' in globals(): CP.split(globals(), *CAMERA_SPLIT)

for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _stem_parts(_v); _write_gap(_v)



# 2026-10-13 carry-over boxes (V2) and the layer-order check (V1): after the visual passes, like topics 13-18
import types as _types
MV.carry(_types.SimpleNamespace(**globals()), CARRY32)
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
