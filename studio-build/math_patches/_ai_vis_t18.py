"""Topic 18 (Exercises with Letters) - the redo for the teacher's own-voice reading (2026-10-12), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py / _ai_vis_t16.py / _ai_vis_t17.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The teacher records only the camera lesson 'digit-puzzles' (re-record, never touched here). Every other topic-18 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t18.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t18.py ai_redo_t18() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods and EVERY method of the Hebrew solution (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-18-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t18ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-18 flow order of the scripts (digit-puzzles = the camera lesson, not here)
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
CAM_BASE = 'digit-puzzles'
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
            'style': "the teacher reads it herself (Reading Studio), topic-18 redo (2026-10-12): math_patches/_ai_vis_t18.py is "
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

# ------------------------------------------------------------------------------------------------ digit-puzzles (camera lesson)
# 2026-10-13 teacher: her camera first lesson is a reading script too (same style, handwriting, camera on, more examples).
# Hebrew lesson (alg 18204-18450): letters are digits ("a number in another language"), different digits only when the
# question says so, the leading digit is never 0 ("not an area code"), the four steps, every puzzle could be plugged in
# (a computer would), writing a number with its digits (27 = 10·2 + 7, 538, 10A + B, 100A + 10B + C), plugging in is
# usually faster.  Her worked examples became the question videos (q-512 the ones column and the leading 1, q-513 the
# special digits, q-514 AB − BA, q-516 subtraction into addition) and are not repeated here.  NEW examples: A4 + 3B = 71
# built with the COLS figure (V1), two puzzles in words (4 and 7 times the digit sum) with their non-examples.
_dpm_spec = importlib.util.spec_from_file_location('_method_visuals_dp18', os.path.join(HERE, '_method_visuals.py'))
_DPM = importlib.util.module_from_spec(_dpm_spec); _dpm_spec.loader.exec_module(_DPM)
dpc = _DPM.items(_layers, 'dpc', _DPM.COLS(['A4', '3B', '71'], '+', [
    ('line', dict(n=2, bar=False, res=False)), ('res', dict(bar=True, res=True)), ('o', dict(hl=0)),
    ('b7', dict(carry={1: '1'}, notes='B=7')), ('t', dict(hl=1)), ('a3', dict(hl=None, notes='A=3, B=7'))], size=50),
    col=1, own=True)
dp1 = I('dp1', '$\\overline{AB}$: $\\ A=4,\\ B=7$: $\\ 47$, not $4\\cdot7$', size=34, hand='AB :    A = 4,  B = 7 :    47,   not  4·7')
dp2 = I('dp2', '$A=2,\\ B=3$: $\\ \\overline{AB}=23$, not $6$', size=34, hand='A = 2,  B = 3 :    AB = 23,   not  6')
dp3 = I('dp3', '$\\overline{ABC}$: $\\ A=5,\\ B=3,\\ C=8$: $\\ 538$', size=34, hand='ABC :    A = 5,  B = 3,  C = 8 :    538')
dp4 = I('dp4', '$\\overline{AA}$: $\\ 33,\\ 77$ ✓ $\\quad 37$ ✗', size=34, hand='AA :    33,   77   ✓        37   ✗')
dp5 = I('dp5', 'Different digits only if the question says so: $\\ $then $\\overline{AB}\\ne22,\\ 55$', size=28)
dp6 = I('dp6', '$\\overline{AB}$: $\\ A$ from $1$ to $9$, $\\ B$ from $0$ to $9$ $\\quad$ no $08$', size=30)
dp7 = I('dp7', '$27=10\\cdot2+7 \\qquad 538=100\\cdot5+10\\cdot3+8$', size=32, hand='27 = 10·2 + 7        538 = 100·5 + 10·3 + 8')
dp8 = I('dp8', '$\\overline{AB}=10A+B \\qquad \\overline{ABC}=100A+10B+C$', size=32, hand='AB = 10A + B        ABC = 100A + 10B + C')
dp9 = I('dp9', '$A=6,\\ B=1$: $\\ 10\\cdot6+1=61$', size=32, hand='A = 6,  B = 1 :    10·6 + 1 = 61')
dp10 = I('dp10', '1. Write it vertically', size=28)
dp10b = I('dp10b', '2. The ones column', size=28)
dp10c = I('dp10c', '3. The leftmost digit, the size', size=28)
dp10d = I('dp10d', '4. Plug in', size=28)
dp11 = I('dp11', 'Plugging in always works. Steps 1-3 save tries.', size=28)
dp12 = I('dp12', '$34+37=71$ ✓', size=34, hand='34 + 37 = 71   ✓')
dp13 = I('dp13', '$10A+B=4(A+B)$', size=34, hand='10A + B = 4(A + B)')
dp13b = I('dp13b', '$10A+B=4A+4B$', size=34, hand='10A + B = 4A + 4B')
dp14 = I('dp14', '$6A=3B$: $\\ B=2A$', size=34, hand='6A = 3B :    B = 2A')
dp15 = I('dp15', '$12,\\ 24,\\ 36,\\ 48$ $\\quad A=5$: $\\ B=10$ ✗', size=32, hand='12,   24,   36,   48        A = 5 :    B = 10   ✗')
dp16 = I('dp16', '$24$: $\\ 4\\cdot(2+4)=24$ ✓', size=32, hand='24 :    4·(2 + 4) = 24   ✓')
dp17 = I('dp17', '$10A+B=7(A+B)$: $\\ 3A=6B$, $\\ A=2B$', size=32, hand='10A + B = 7(A + B) :    3A = 6B,    A = 2B')
dp18 = I('dp18', '$21,\\ 42,\\ 63,\\ 84$ $\\quad B=0$: $\\ A=0$ ✗', size=32, hand='21,   42,   63,   84        B = 0 :    A = 0   ✗')
video('digit-puzzles', 'lesson', slides=[
    S('Exercises with Letters',
      L("Welcome. Sometimes a calculation on the exam is written with letters instead of digits. Instead of thirty-two "
        "plus fifty-seven, we get letters, and each letter stands for a digit. It's a bit like the number puzzles in a "
        "weekend newspaper, only much smaller. Let's see what the letters mean, and a short technique for these puzzles.")),
    S('What the letters mean',
      L("Each letter stands for a digit. A B with a bar on top is a two-digit number. A is its tens digit, and B is its "
        "ones digit. It is not A times B. For example, if A is four and B is seven, A B is forty-seven, not four times "
        "seven.", show(dp1, 'if A is four and B is seven')),
      L("Think of it as a number written in another language. In that language, two is drawn as A, and three is drawn as "
        "B. So A B is simply twenty-three. It's not two times three, which is six.", show(dp2, 'So A B is simply twenty-three')),
      L("The bar on top tells us that the letters are the digits of one number. A B C with a bar is a three-digit number. "
        "If A is five, B is three and C is eight, A B C is five hundred thirty-eight.", show(dp3, 'If A is five, B is three'))),
    S('Same letter, different letters',
      L("The same letter always stands for the same digit. So A A can be thirty-three or seventy-seven, but never "
        "thirty-seven.", show(dp4, 'So A A can be thirty-three')),
      L("Different letters are different digits only when the question says so. In most exam questions it does say "
        "different digits, and then A B can't be twenty-two or fifty-five. If the question doesn't say it, A and B may be "
        "the same digit.", show(dp5, 'only when the question says so')),
      L("And the leftmost digit is never zero. Nobody writes oh eight. It's not a phone area code, it's just eight. So in "
        "A B, A is a digit from one to nine, and B can be any digit from zero to nine.", show(dp6, 'So in A B, A is a digit'))),
    S('A number written with its digits',
      L("Every number can be written with its digits. Twenty-seven has two tens and seven ones, so it's ten times two, "
        "plus seven. Five hundred thirty-eight is a hundred times five, plus ten times three, plus eight.",
        show(dp7, 'Twenty-seven has two tens')),
      L("Letters work the same way. A B is ten A plus B, because A is in the tens place. And A B C is a hundred A, plus ten "
        "B, plus C. For example, if A is six and B is one, ten times six plus one is sixty-one.",
        show(dp8, 'A B is ten A plus B'), show(dp9, 'if A is six and B is one')),
      L("Some students like to solve with this form. Usually, plugging in two numbers is faster, but this form is what we "
        "need when a puzzle comes in words.", pt('dp8', 'Some students like to solve'))),
    S('The four steps',
      L("Now the technique. Many letter puzzles are solved with four steps. One, write the calculation vertically, with "
        "the ones digits lined up. Two, check the ones column. Three, check the leftmost digit and the size of the numbers. "
        "And four, plug in numbers and see what fits. When they ask for one letter, we can plug in the answer choices for "
        "that letter.", show(dp10, 'One, write the calculation vertically'),
        show(dp10b, 'Two, check the ones column'), show(dp10c, 'Three, check the leftmost digit'), show(dp10d, 'And four, plug in numbers')),
      L("In fact, every letter puzzle could be solved just by plugging in. A computer would simply try every option, and "
        "it would be fast. We're not computers, so steps one to three are shortcuts. They tell us which numbers we no longer "
        "need to try. We use the steps that help in the question, not every step every time.",
        show(dp11, 'every letter puzzle could be solved'))),
    S('The steps on an example',
      L("Let's try them. A four, plus three B, equals seventy-one. Step one, we write it vertically, with the ones digits "
        "lined up.", show(dpc['line'], 'Step one, we write it vertically'), show(dpc['res'], 'with the ones digits')),
      L("Step two, the ones column. Four plus B ends in one. Four plus seven is eleven, which ends in one, and no other "
        "digit works. So B is seven, and we carry one to the tens column.", show(dpc['o'], 'Step two, the ones column'),
        show(dpc['b7'], 'So B is seven')),
      L("Step three, the tens column, which is the leftmost one here. A plus three, plus the carried one, is seven. So A "
        "plus four is seven, and A is three.", show(dpc['t'], 'Step three, the tens column'), show(dpc['a3'], 'and A is three')),
      L("Let's check. Thirty-four plus thirty-seven is seventy-one. It fits, and here we didn't even need step four.",
        show(dp12, 'Thirty-four plus thirty-seven'))),
    S('A puzzle in words',
      L("Sometimes the puzzle comes in words, with no columns. For example, a two-digit number is four times the sum of "
        "its digits. We write the number as ten A plus B, and its digit sum as A plus B. So ten A plus B equals four times "
        "the whole bracket, A plus B.", show(dp13, 'So ten A plus B equals four times')),
      L("Open the bracket: ten A plus B equals four A plus four B. Subtract four A and B from both sides, and six A equals "
        "three B. Divide both sides by three, and B equals two A. So B is twice A.", show(dp13b, 'Open the bracket'), show(dp14, 'and six A equals three B')),
      L("Now the digits that fit. A can't be zero, because it's the leftmost digit. A is one gives B is two, so twelve. "
        "Then twenty-four, thirty-six and forty-eight. A is five would need B to be ten, and ten is not a digit, so we stop "
        "there. Let's check one. Twenty-four has the digit sum six, and four times six is twenty-four.",
        show(dp15, 'A is one gives B is two'), show(dp16, "Let's check one"))),
    S('A puzzle in words',
      L("One more. A two-digit number is seven times the sum of its digits. Ten A plus B equals seven A plus seven B. "
        "Subtract seven A and B from both sides, and three A equals six B, so A equals two B. B is one gives twenty-one, "
        "and then forty-two, sixty-three and eighty-four. B is zero would make A zero too, and a number can't start with "
        "zero.", show(dp17, 'A two-digit number is seven times'), show(dp18, 'B is one gives twenty-one')),
      L("Each question that follows uses these steps, and teaches one more tool. Try each question first, and then watch "
        "its solution. [pause] Okay. I'll see you in the next video.", pt('dp18', 'Each question that follows')),
      sb='A puzzle in words'),
])

# ------------------------------------------------------------------------------------------------ q-512 (Hebrew: lesson example 1)
# NEW: the ones column - nothing carries in, so "A + A ends in A" means A = 0; the leading-digit rule (two numbers, more
# digits in the sum -> 1; why: 99 + 99 = 198; only for TWO numbers); B + D = 11 is enough, no need to know B and D.
# REMINDER: the 4 steps, what the letters mean (camera lesson).  Hebrew: one method (the four steps).
a1 = I('a1', '$\\begin{array}{r}BA\\\\+\\ DA\\\\\\hline CCA\\end{array}$', size=46, col=1)
a2 = I('a2', 'Ones: $\\ A+A$ ends in $A$: $\\ \\hl{a}{A=0}$', hand='Ones :    A + A  ends in  A :    \\hl{a}{A = 0}')
a3 = I('a3', '$5+0=5 \\qquad 8+0=8$', size=32, col=1, hand='5 + 0 = 5        8 + 0 = 8')
a4 = I('a4', 'Two numbers, more digits: $\\ \\hl{c}{C=1}$', hand='Two numbers,  more digits :    \\hl{c}{C = 1}')
a5 = I('a5', '$99+99=198 \\qquad 90+90=180$', size=30, hand='99 + 99 = 198        90 + 90 = 180')
a6 = I('a6', 'Tens: $\\ B+D=11$', hand='Tens :    B + D = 11')
a7 = I('a7', '$B+C+D=11+1=12$', hand='B + C + D = 11 + 1 = 12')
a8 = I('a8', '$30+80=110 \\qquad 40+70=110$', size=30, hand='30 + 80 = 110        40 + 70 = 110')
video('solve-q-512', 'solution', qid='q-512', slides=[
    S('The four steps',
      L("A, B, C and D represent digits. Given: B A, plus D A, is equal to C C A. B plus C plus D is equal to what?",
        pt('stem', 'A, B, C', 'hl', 7.0), voice='calm', pause=0.5),
      L("So an addition in letters, and each letter is a digit. [short pause] We'll solve it with our four steps.",
        pt('stem', 'an addition in letters')),
      L("[short pause] Step one, write it vertically. Now the columns line up, and we can see things.", show(a1, 'write it vertically')),
      L("Step two, the ones column. A plus A ends in A. Add something to A and land back on A? Nothing carries into the ones "
        "column, so that something must be zero. Five plus zero is five, eight plus zero is eight. So A is zero.",
        show(a2, 'A plus A ends in A'), show(a3, 'Five plus zero'))),
    S('The four steps',
      L("Step three, the leftmost digit. We added two two-digit numbers and got three digits. When you add two numbers and "
        "the sum has more digits, the new leading digit is one. So C is one.", show(a4, 'the new leading digit')),
      L("Why one? Even the biggest, ninety-nine plus ninety-nine, is one ninety-eight. And ninety plus ninety is one eighty. "
        "You can never reach two hundred. But careful, only for two numbers. Three or four numbers can start with two or "
        "more.", show(a5, 'ninety-nine plus ninety-nine')),
      L("Now the tens. B plus D gives C C, which is eleven, because A is zero and nothing carries from the ones. So B plus D "
        "is eleven. Three and eight, or four and seven, and we don't need to know which.", show(a6, 'So B plus D')),
      L("B plus C plus D is eleven plus one, twelve. Choice number four is our answer.", show(a7, 'eleven plus one'),
        mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("And to see it's real, thirty plus eighty is one ten, and forty plus seventy is one ten too. [pause] Okay. I'll see "
        "you in the next question.", show(a8, 'thirty plus eighty')),
      sb='The four steps'),
])

# ------------------------------------------------------------------------------------------------ q-513 (Hebrew: lesson example 2)
# NEW: the special digits 0, 1, 5, 6 (a digit times itself keeps its units digit; examples); 5 x even -> 0, 5 x odd -> 5;
# 6 x even keeps the digit (6·2, 6·4, 6·8).  Hebrew: one method (special digits).
b1 = I('b1', '$\\begin{array}{r}CB\\\\\\times\\ \\ \\ B\\\\\\hline ACB\\end{array}$', size=46, col=1)
b2 = I('b2', '$0\\cdot0=0 \\quad 1\\cdot1=1 \\quad 5\\cdot5=25 \\quad 6\\cdot6=36$', size=32, hand='0·0 = 0     1·1 = 1     5·5 = 25     6·6 = 36')
b3 = I('b3', '$7\\cdot7=49 \\qquad 4\\cdot4=16$', size=32, hand='7·7 = 49        4·4 = 16')
b4 = I('b4', '$5\\times$ even $\\to0$: $\\ 5\\cdot4=20$ $\\quad 5\\times$ odd $\\to5$: $\\ 5\\cdot3=15$', size=28, col=1, hand='5 × even → 0 :  5·4 = 20      5 × odd → 5 :  5·3 = 15')
b5 = I('b5', '$6\\times$ even keeps it: $\\ 6\\cdot4=24,\\ 6\\cdot8=48$', size=28, col=1, hand='6 × even keeps it :   6·4 = 24,   6·8 = 48')
b6 = I('b6', '$B=0$: $\\ $the product is $0$ ✗', size=32, hand='B = 0 :    the product is 0   ✗')
b7 = I('b7', '$25\\cdot5=125$ ✓', hand='25·5 = 125   ✓')
video('solve-q-513', 'solution', qid='q-513', slides=[
    S('Special digits',
      L("A, B and C represent digits. Given: C B, times B, is equal to A C B. Which of the following could be B?",
        pt('stem', 'A, B and C', 'hl', 6.0), voice='calm', pause=0.5),
      L("So a multiplication in letters, and we look for B. [short pause] Let's write it vertically and look at the ones "
        "column.", pt('stem: ask', 'we look for B'), show(b1, 'write it vertically')),
      L("B times B ends in B. A digit times itself that keeps its units digit. That happens only for four digits, zero, one, "
        "five and six. Zero times zero is zero, one times one is one, five times five is twenty-five, and six times six is "
        "thirty-six. These are the special digits.", show(b2, 'Zero times zero')),
      L("No other digit does it. Seven times seven is forty-nine, and four times four is sixteen. So choice numbers one and "
        "four are out.", show(b3, 'Seven times seven'), mk('cross', 'choice 1', 'So choice numbers one'), mk('cross', 'choice 4', 'and four are out')),
      L("Two more facts about them. Five times an even number ends in zero, five times four is twenty. Five times an odd "
        "number ends in five, five times three is fifteen. And six times an even number keeps that number's units digit. "
        "Six times four is twenty-four, and six times eight is forty-eight.", show(b4, 'Five times an even'), show(b5, 'six times an even')),
      L("Five or zero are left. Zero? Zero times anything is zero, not a three-digit number. Out.", show(b6, 'Zero times anything'),
        mk('cross', 'choice 3', 'not a three-digit number. Out')),
      L("So B is five, and it really works. Twenty-five times five is one twenty-five. Choice number two is our answer. "
        "[pause] Okay. I'll see you in the next question.", show(b7, 'Twenty-five times five'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-514 (Hebrew: lesson example 3)
# NEW: no result given -> plug in (two numbers that are not alike); the algebraic form AB = 10A + B, ABC = 100A + 10B + C
# (27, 538); AB + BA = 11(A + B), AB - BA = 9(A - B).  Hebrew: plugging in, the algebraic form.
c1 = I('c1', '$71+17=88$: $\\ $not by $3$, not by $10$', size=32, hand='71 + 17 = 88 :    not by 3,   not by 10')
c2 = I('c2', '$72+27=99$: $\\ $not by $4$', size=32, hand='72 + 27 = 99 :    not by 4')
c3 = I('c3', '$\\overline{AB}=10A+B \\qquad 47=10\\cdot4+7$', size=34, hand='AB = 10A + B        47 = 10·4 + 7')
c4 = I('c4', '$\\overline{ABC}=100A+10B+C \\qquad 538=500+30+8$', size=32, hand='ABC = 100A + 10B + C        538 = 500 + 30 + 8')
c5 = I('c5', '$(10A+B)+(10B+A)=11A+11B=11(A+B)$', size=32, hand='(10A + B) + (10B + A) = 11A + 11B = 11(A + B)')
c6 = I('c6', '$\\overline{AB}-\\overline{BA}=9(A-B)$: $\\ 62-26=36$', size=30, col=1, hand='AB − BA = 9(A − B) :    62 − 26 = 36')
video('solve-q-514', 'solution', qid='q-514', slides=[
    S('Method 1 · Plugging in numbers',
      L("A and B represent nonzero digits. Which of the following necessarily divides A B plus B A?",
        pt('stem', 'A and B', 'hl', 5.0), voice='calm', pause=0.5),
      L("So a number plus its reversal, and there's no result to work with. No columns to read. [short pause] We'll solve "
        "it two ways, plugging in numbers, and then the algebraic form.", pt('stem', 'a number plus its reversal')),
      L("[short pause] Let's start by plugging in. When there's nothing to read, plug in numbers. A B is seventy-one, so B A "
        "is seventeen. Seventy-one plus seventeen is eighty-eight. Eighty-eight doesn't divide by three or by ten, so "
        "choice numbers two and three are out.", show(c1, 'Seventy-one plus seventeen'), mk('cross', 'choice 2', 'choice numbers two'),
        mk('cross', 'choice 3', 'and three are out')),
      L("Two are left, so one more number. Seventy-two plus twenty-seven is ninety-nine, and ninety-nine doesn't divide by "
        "four. Out. So eleven, choice number one is our answer.", show(c2, 'Seventy-two plus twenty-seven'),
        mk('cross', 'choice 4', "doesn't divide by four. Out"), mk('tick', 'choice 1', 'choice number one is our answer'))),
    S('Method 2 · The math way: place values',
      L("[pause] Another way is the algebraic form. What's different? Instead of trying numbers, we write the number by its "
        "digits, and see why it always works. A B is ten A plus B, because A is in the tens. Forty-seven is ten times four, "
        "plus seven.", show(c3, 'A B is ten A plus B')),
      L("And a three-digit number A B C is a hundred A, plus ten B, plus C. Five thirty-eight is five hundred, plus thirty, "
        "plus eight.", show(c4, 'a three-digit number')),
      L("So A B plus B A is ten A plus B, plus ten B plus A. That's eleven A plus eleven B, eleven times, in brackets, A "
        "plus B. Always divisible by eleven. Choice number one.", show(c5, 'ten A plus B, plus ten B'),
        mk('tick', 'choice 1', 'Always divisible by eleven')),
      L("And the minus works the same way. A B minus B A is nine times, in brackets, A minus B. Sixty-two minus twenty-six "
        "is thirty-six, four nines. Both patterns come back on the exam. Many strong students like this way, but two quick "
        "numbers are usually faster. [pause] Okay. I'll see you in the next question.", show(c6, 'A B minus B A'))),
])

# ------------------------------------------------------------------------------------------------ r26-t18-facts (lesson)
# NEW: repdigits AA = 11A, AAA = 111A = 3·37·A, BBBB / BB = 101 (two examples each); the largest / smallest number with a
# given digit sum (two examples).  REMINDER: units digits of powers repeat in a cycle (topic 21).
d1 = I('d1', '$\\overline{AA}=11A$: $\\ 77=11\\cdot7,\\ \\ 44=11\\cdot4$', size=36, hand='AA = 11A :    77 = 11·7,    44 = 11·4')
d2 = I('d2', '$\\overline{AAA}=111A=3\\cdot37\\cdot A$', size=36, hand='AAA = 111A = 3·37·A')
d3 = I('d3', '$555=5\\cdot111=37\\cdot15 \\qquad 222=2\\cdot111=37\\cdot6$', size=32, hand='555 = 5·111 = 37·15        222 = 2·111 = 37·6')
d4 = I('d4', '$\\overline{BBBB}\\div\\overline{BB}=101$: $\\ 7777\\div77,\\ \\ 3333\\div33$', size=32, hand='BBBB ÷ BB = 101 :    7777 ÷ 77,    3333 ÷ 33')
e1 = I('e1', 'Digit sum $8$: $\\ $largest $800$, $\\ $smallest $107$', size=36, hand='Digit sum 8 :    largest 800,    smallest 107')
e2 = I('e2', 'Digit sum $12$: $\\ $largest $930$, $\\ $smallest $129$', size=36, hand='Digit sum 12 :    largest 930,    smallest 129')
e3 = I('e3', 'Largest: big digits left. Smallest: smallest feasible digits left', size=28)
video('r26-t18-facts', 'lesson', slides=[
    S('Number Facts',
      L("Welcome back. A few number facts that come back in letter puzzles. You'll meet them in the practice.")),
    S('One repeated digit',
      L("First, numbers made of one repeated digit. A A is eleven times A. Seventy-seven is eleven times seven, and "
        "forty-four is eleven times four.", show(d1, 'A A is eleven times A')),
      L("A A A is a hundred eleven times A. And a hundred eleven is three times thirty-seven. So A A A always divides by "
        "three and by thirty-seven.", show(d2, 'A A A is a hundred eleven')),
      L("Five fifty-five is thirty-seven times fifteen, and two twenty-two is thirty-seven times six.", show(d3, 'Five fifty-five')),
      L("And B B B B divided by B B is always one hundred one. Seven thousand seven hundred seventy-seven divided by "
        "seventy-seven, and three thousand three hundred thirty-three divided by thirty-three, both give one oh one.",
        show(d4, 'divided by B B'))),
    S('Largest and smallest',
      L("Second, the largest or the smallest number with a given digit sum. The largest three-digit number with digit sum "
        "eight? Put everything on the left. Eight hundred. The smallest? The leftmost digit can't be zero, so it's one. Then "
        "zero, and the rest goes on the right, seven. One oh seven.", show(e1, 'digit sum eight')),
      L("Digit sum twelve. The largest, nine on the left, then three, nine thirty. The smallest, one, then the biggest digit "
        "on the right, nine, and two in the middle. One twenty-nine.", show(e2, 'Digit sum twelve')),
      L("So for the largest, big digits on the left. For the smallest, choose the smallest possible digit on the left, "
        "and leave as much of the digit sum as possible for the right. The first digit cannot be zero, "
        "and each remaining digit can hold at most nine. In our two examples we can start with one, "
        "but that is not possible for every digit sum. And remember from patterns, the units digits of powers repeat in a cycle. [pause] Okay. I'll see you in the "
        "next video.", show(e3, 'big digits on the left'))),
])

# ------------------------------------------------------------------------------------------------ q-515 (Hebrew Q1)
# NEW at the step: no new digit -> no free one; the ones column again.  REMINDER: the 4 steps (camera lesson), the ones
# column and the leading-digit rule (q-512).  Hebrew: one method (the steps).
f1 = I('f1', '$\\begin{array}{r}BCA\\\\+\\ \\ \\ BC\\\\\\hline AAA\\end{array}$', size=46, col=1)
f2 = I('f2', 'Three digits $+$ two digits $=$ three digits: $\\ $no new digit', size=30, hand='3 digits + 2 digits = 3 digits :    no new digit')
f3 = I('f3', 'Ones: $\\ A+C$ ends in $A$: $\\ \\hl{c}{C=0}$', hand='Ones :    A + C  ends in  A :    \\hl{c}{C = 0}')
f4 = I('f4', '$303+30=333 \\qquad 404+40=444$', size=32, col=1, hand='303 + 30 = 333        404 + 40 = 444')
video('solve-q-515', 'solution', qid='q-515', slides=[
    S('The four steps',
      L("A, B and C represent digits. Given: B C A, plus B C, is equal to A A A. C is equal to what?",
        pt('stem', 'A, B and C', 'hl', 6.0), voice='calm', pause=0.5),
      L("So an addition again, and they ask only for C. [short pause] We'll solve it with the four steps. First, vertically.",
        pt('stem', 'they ask only for C'), show(f1, 'First, vertically')),
      L("The leftmost digit? A three-digit number plus a two-digit number, and the sum still has three digits. No new digit, "
        "so the rule about one doesn't help here.", show(f2, 'No new digit')),
      L("So the ones column. A plus C ends in A. Nothing carries into the ones, so adding C changed nothing. C is zero. "
        "Choice number two is our answer.", show(f3, 'A plus C ends in A'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("And it's real. With nothing carried, the tens give B equal to A. Three hundred three plus thirty is three hundred "
        "thirty-three, and four hundred four plus forty is four hundred forty-four. [pause] Okay. I'll see you in the next question.", show(f4, 'Three hundred three'))),
])

# ------------------------------------------------------------------------------------------------ q-516 (Hebrew Q2)
# NEW: flip a subtraction into an addition (why it helps; AA - BB = BB -> BB + BB = AA, so B is 1 to 4, 55 + 55 > 100);
# just calculate once A is known (the digit-by-digit way is correct but slow); the choices are letters too.
# REMINDER: the leading-digit rule (q-512).  Hebrew: one method (+ the remark on the slow way).
g1 = I('g1', '$\\begin{array}{r}AAA\\\\-\\ \\ \\ 46\\\\\\hline BC\\end{array}$', size=40, col=1)
g2 = I('g2', '$\\begin{array}{r}BC\\\\+\\ 46\\\\\\hline AAA\\end{array}$', size=40, col=1)
g3 = I('g3', '$\\overline{AA}-\\overline{BB}=\\overline{BB}\\ \\to\\ \\overline{BB}+\\overline{BB}=\\overline{AA}$: $\\ B\\le4$', size=26, hand='AA − BB = BB   →   BB + BB = AA :    B ≤ 4')
g4 = I('g4', '$55+55=110$: $\\ $too big', size=26, hand='55 + 55 = 110 :    too big')
g5 = I('g5', 'Two two-digit numbers, three digits: $\\ A=1$, $\\ \\overline{AAA}=111$', size=30, hand='2-digit + 2-digit = 3 digits :    A = 1,    AAA = 111')
g6 = I('g6', '$111-46=65$: $\\ B+C=6+5=\\hl{e}{11}$', hand='111 − 46 = 65 :    B + C = 6 + 5 = \\hl{e}{11}')
g7 = I('g7', '$\\overline{AA}=11$ ✓', hand='AA = 11   ✓')
video('solve-q-516', 'solution', qid='q-516', slides=[
    S('Flip it into an addition',
      L("A, B and C represent digits. Given: A A A minus forty-six is equal to B C. B plus C is equal to what?",
        pt('stem', 'A, B and C', 'hl', 6.0), voice='calm', pause=0.5),
      L("A subtraction, and look, the choices are letters too. [short pause] We'll solve it by flipping it into an addition.",
        pt('stem', 'A subtraction')),
      L("[short pause] First, vertically. A subtraction is hard to read, so flip it. A A A minus forty-six is B C means B C "
        "plus forty-six is A A A.", show(g1, 'First, vertically'), show(g2, 'B C plus forty-six')),
      L("Why does it help? Take A A minus B B equals B B. Flipped, it's B B plus B B equals A A. Now you see it at once, B "
        "is one, two, three or four. Five is too big, fifty-five plus fifty-five is one ten, three digits.",
        show(g3, 'Take A A minus'), show(g4, 'fifty-five plus fifty-five'))),
    S('Flip it into an addition',
      L("Back to ours. Two two-digit numbers, B C and forty-six, add up to a three-digit number. So the leading digit is "
        "one. A is one, and A A A is one eleven.", show(g5, 'Two two-digit numbers')),
      L("Some students go on digit by digit here. C plus six ends in one, so C is five, carry one, and so on. It's correct, "
        "but slow. Just calculate. One eleven minus forty-six is sixty-five. So B is six, C is five, and B plus C is "
        "eleven.", show(g6, 'One eleven minus forty-six')),
      L("Now the choices are letters. A is one, so A A is eleven. Choice number three is our answer. [pause] Okay. I'll see "
        "you in the next question.", show(g7, 'so A A is eleven'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      sb='Flip it into an addition'),
])

# ------------------------------------------------------------------------------------------------ q-517 (Hebrew Q3)
# NEW: estimate the size (squares near 600: 24² = 576, 25² = 625, 26² = 676, 27² = 729; 20² = 400, 30² = 900);
# "could be": one option is enough.  REMINDER: special digits (q-513), a leading digit is never 0 (camera lesson).
# Hebrew: the full math (size + units), the insight (units digit + the choices).
h1 = I('h1', '$\\overline{CA}^2=6\\ldots$', hand='CA^2 = 6 . . .')
h2 = I('h2', '$20^2=400 \\qquad 30^2=900$: $\\ C=2$', size=32, hand='20^2 = 400        30^2 = 900 :    C = 2')
h3 = I('h3', '$25^2=625\\ (2\\cdot3=6\\,|\\,25) \\quad 26^2=625+25+26=676$', size=30, hand='25^2 = 625   (2·3 = 6 | 25)      26^2 = 625 + 25 + 26 = 676')
h4 = I('h4', '$25$: $\\ A-C=3$ (not a choice) $\\quad 26$: $\\ A-C=\\hl{f}{4}$', size=30, hand='25 :   A − C = 3  (not a choice)      26 :   A − C = \\hl{f}{4}')
i1 = I('i1', '$A\\cdot A$ ends in $A$: $\\ A=0,\\ 1,\\ 5,\\ 6$', size=32, hand='A·A  ends in  A :    A = 0,  1,  5,  6')
i2 = I('i2', '(1) $6$: $\\ C=0$ ✗ $\\quad$ (3) $5$: $\\ 16^2=256$ ✗', size=30, hand='(1)  6 :   C = 0  ✗      (3)  5 :   16^2 = 256  ✗')
i3 = I('i3', '(2) $2$: $\\ 35^2=1225>999$ ✗ $\\quad$ (4) $4$: $\\ A=6,\\ C=2$ ✓', size=30, hand='(2)  2 :   35^2 = 1225 > 999  ✗      (4)  4 :   A = 6,  C = 2  ✓')
video('solve-q-517', 'solution', qid='q-517', slides=[
    S('Method 1 · Estimation',
      L("A, B and C represent digits. Given: C A times C A is equal to six B A. Which of the following could be A minus C?",
        pt('stem', 'A, B and C', 'hl', 7.0), voice='calm', pause=0.5),
      L("So a two-digit number squared gives six hundred and something. [short pause] We'll solve it two ways, the size "
        "first, and then starting from the choices.", pt('stem: g1', 'a two-digit number squared')),
      L("[short pause] Let's start with the size. C A squared is six hundred and something. Twenty squared is four hundred, "
        "and thirty squared is nine hundred. So C A is in the twenties, and C is two.", show(h1, 'C A squared is six'), show(h2, 'Twenty squared')),
      L("Which twenties? Twenty-four squared is five seventy-six, too small. Twenty-five squared is six twenty-five, twenty-six "
        "squared is six seventy-six, and twenty-seven squared is seven twenty-nine, too big. So twenty-five or twenty-six.",
        show(h3, 'Twenty-four squared')),
      L("Twenty-five gives A minus C, five minus two, three. Not a choice, and they ask what could be, so one option is "
        "enough. Twenty-six gives six minus two, four. Choice number four is our answer.", show(h4, 'Twenty-five gives'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Another way, and it's sharp. What's different? We don't estimate first. We take the ones column, and let "
        "the choices do the work. A times A ends in A, so A is a special digit, zero, one, five or six.", show(i1, 'A times A ends in A')),
      L("A minus C is six? Then A is six and C is zero, but a leading digit is never zero. Out. Five? A five would need C zero, so "
        "A is six and C is one, sixteen squared, two fifty-six, not six hundred and something. Out.", show(i2, 'A minus C is six'),
        mk('cross', 'choice 1', 'never zero. Out'), mk('cross', 'choice 3', 'two fifty-six')),
      L("Two? A five, C three, or A six, C four. Thirty-five and forty-six are too big, their squares have four digits. Out. "
        "Four? A six and C two, and twenty-six squared is six seventy-six. It fits. Choice number four. [pause] Okay. I'll "
        "see you in the next question.", show(i3, 'A five, C three'), mk('cross', 'choice 2', 'four digits. Out'),
        mk('tick', 'choice 4', 'It fits. Choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-518 (Hebrew Q4)
# NEW: flip a division into a multiplication; 7A ends in A -> 6A ends in 0 -> A = 0 or 5 (A = 0 is out: a leading digit);
# multiply in easy pieces (55·17 = 550 + 385).  REMINDER: 5 x odd ends in 5 (q-513).  Hebrew: one method.
j1 = I('j1', '$\\begin{array}{r}AA\\\\\\times\\ 17\\\\\\hline CBA\\end{array}$', size=46, col=1)
j2 = I('j2', '$7A$ ends in $A$: $\\ A=0$ or $5$ $\\quad 7\\cdot5=35$', size=32, hand='7A  ends in  A :    A = 0  or  5      7·5 = 35')
j3 = I('j3', '$A=0$: $\\ \\overline{AA}=00$ ✗ $\\quad \\to\\ A=5$', size=32, hand='A = 0 :   AA = 00  ✗      →   A = 5')
j4 = I('j4', '$55\\cdot17=550+385=935$', hand='55·17 = 550 + 385 = 935')
j5 = I('j5', '$9+3+5=17$', hand='9 + 3 + 5 = 17')
video('solve-q-518', 'solution', qid='q-518', slides=[
    S('Flip it into a multiplication',
      L("A, B and C represent digits. Given: C B A over A A is equal to seventeen. A plus B plus C is equal to what?",
        pt('stem', 'A, B and C', 'hl', 6.0), voice='calm', pause=0.5),
      L("A division in letters. [short pause] Just like a subtraction flips into an addition, a division flips into a "
        "multiplication. A A times seventeen is C B A.", pt('stem', 'A division in letters'), show(j1, 'A A times seventeen')),
      L("Now the ones. Seven times A ends in A. Take A away from both, and six A ends in zero. So A is zero or five. Check "
        "five, seven times five is thirty-five, it ends in five.", show(j2, 'Seven times A ends in A')),
      L("Zero? Then A A would be zero zero, and a number never starts with zero. So A is five.", show(j3, 'Zero? Then A A')),
      L("Now just multiply, fifty-five times seventeen, in easy pieces. Ten times fifty-five is five fifty, and seven times "
        "fifty-five is three eighty-five. Together, nine thirty-five. And it really ends in five.", show(j4, 'fifty-five times seventeen')),
      L("So C is nine, B is three, and A is five. Nine plus three plus five is seventeen. Choice number one is our answer. "
        "[pause] Okay. I'll see you in the next question.", show(j5, 'Nine plus three plus five'),
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-519 (Hebrew Q5)
# NEW: take inventory (the prime digits 2, 3, 5, 7: four letters, four primes, all used); plug in the choices (organized
# trial and error); two different primes add up to at least 5.  Hebrew: plugging in the answers, and in class the
# other choices are ruled out too - here the three wrong ones come first, so the video ends on the answer.
k1 = I('k1', '$\\begin{array}{r}AB\\\\+\\ BC\\\\\\hline CD\\end{array}$', size=46, col=1)
k2 = I('k2', 'Prime digits: $\\ 2,\\ 3,\\ 5,\\ 7$', hand='Prime digits :    2,   3,   5,   7')
k3 = I('k3', '(2), (3) $\\ C=2,\\ 3$: $\\ A+B\\ge2+3=5$ ✗', size=30, hand='(2), (3)   C = 2, 3 :    A + B ≥ 2 + 3 = 5   ✗')
k4 = I('k4', '(1) $C=7$: $\\ B+7=9,\\ 10,\\ 12$ $\\to\\ A=1$ ✗', size=30, hand='(1)   C = 7 :    B + 7 = 9,  10,  12    →   A = 1   ✗')
k5 = I('k5', '(4) $C=5$: $\\ A+B=5$: $\\ 2,\\ 3$ $\\quad B+5=D$: $\\ B=2,\\ D=7$', size=30, hand='(4)   C = 5 :    A + B = 5 :  2, 3      B + 5 = D :   B = 2,   D = 7')
k6 = I('k6', '$32+25=57$ ✓', hand='32 + 25 = 57   ✓')
video('solve-q-519', 'solution', qid='q-519', slides=[
    S('Plugging in the answers',
      L("A, B, C and D represent different digits, and each of them is a prime number. Given: A B plus B C is equal to C D. "
        "C is equal to what?", pt('stem', 'A, B, C and D', 'hl', 8.0), voice='calm', pause=0.5),
      L("Prime digits only. [short pause] We'll solve it by plugging in the choices, organized trial and error. First, "
        "vertically, and an inventory. The prime digits are two, three, five and seven. Four letters, four different "
        "primes, so every one of them is used.", pt('stem', 'Prime digits only'), show(k1, 'vertically'), show(k2, 'The prime digits')),
      L("C is two or three? In the tens, A plus B, maybe with a carry, has to give C. But two different primes add up to at "
        "least two plus three, five. So choice numbers two and three are out.", show(k3, 'C is two or three'),
        mk('cross', 'choice 2', 'So choice numbers two'), mk('cross', 'choice 3', 'and three are out')),
      L("C is seven? Then the ones are B plus seven. B two gives nine, and B three gives ten, and nine and zero aren't prime. "
        "B five gives twelve, so D is two and one carries. Then the tens, A plus five plus one is seven, so A is one. Not a "
        "prime. Out.", show(k4, 'C is seven'), mk('cross', 'choice 1', 'Not a prime. Out'))),
    S('Plugging in the answers',
      L("C is five. The tens, A plus B is five, so they're two and three. The ones, B plus five is D. B two gives seven, the "
        "prime that's left. So A is three, B is two, and D is seven.", show(k5, 'C is five')),
      L("Thirty-two plus twenty-five is fifty-seven. It works. Choice number four is our answer. [pause] Okay. I'll see you "
        "in the next question.", show(k6, 'Thirty-two plus twenty-five'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      sb='Plugging in the answers'),
])

# ------------------------------------------------------------------------------------------------ q-520 (Hebrew Q6)
# NEW: a digit puzzle in words: write x = 10T + U and collect (6T = U³ + 3U); a size bound (6T <= 54) and why U = 0 and
# U >= 4 are out (the value only grows).  REMINDER: 10A + B (camera lesson, q-514).  Hebrew: the math, plugging in the
# answers.  2026-10-13 full rewrite to the Codex review standard (the teacher re-records the whole video).
l1 = I('l1', '$x=10T+U$', hand='x = 10T + U')
l2 = I('l2', '$x=U^3+4(T+U)$', hand='x = U^3 + 4(T + U)')
l3 = I('l3', '$10T+U=U^3+4T+4U$', hand='10T + U = U^3 + 4T + 4U')
l3b = I('l3b', '$6T=U^3+3U$', hand='6T = U^3 + 3U')
l4 = I('l4', '$U=1,2,3,4$: $\\ 4,\\ 14,\\ \\hl{u}{36},\\ 76$', hand='U = 1, 2, 3, 4 :    4,   14,   \\hl{u}{36},   76')
l5 = I('l5', '$6T=36$: $\\ T=6$', hand='6T = 36 :    T = 6')
m1 = I('m1', '$T=7$: $\\ U^3+3U=42$ ✗', size=30, hand='T = 7 :    U^3 + 3U = 42   ✗')
m2 = I('m2', '$T=5$: $\\ 30$ ✗ $\\quad T=4$: $\\ 24$ ✗', size=30, hand='T = 5 :   30  ✗      T = 4 :   24  ✗')
m3 = I('m3', '$T=6$: $\\ U^3+3U=36$: $\\ U=3$, $\\ 63$', size=30, hand='T = 6 :    U^3 + 3U = 36 :    U = 3,    63')
m4 = I('m4', '$27+4\\cdot9=63$ ✓', hand='27 + 4·9 = 63   ✓')
video('solve-q-520', 'solution', qid='q-520', slides=[
    S('Method 1 · The math way: place values',
      L("x is a two-digit number. x is equal to the cube of its units digit, plus four times the sum of its digits. What is "
        "the tens digit of x?", pt('stem', 'x is a two-digit', 'hl', 7.0), voice='calm', pause=0.5),
      L("This digit puzzle is written in words, so first we turn the words into an equation. We need the tens digit of x. "
        "[short pause] We'll solve it two ways, writing the number with its digits, and then testing the answer choices.",
        pt('stem', 'This digit puzzle is written in words')),
      L("[short pause] Let's call the tens digit T and the ones digit U. A two-digit number is ten times its tens digit, "
        "plus its ones digit, so x is ten T plus U. The sum of its digits is T plus U.", show(l1, 'so x is ten T plus U')),
      L("Now the words of the question. The cube of the units digit is U cubed. Four times the sum of the digits is four "
        "times the whole bracket, T plus U. So x equals U cubed, plus four times the bracket T plus U. The four multiplies "
        "both digits, not just T.", show(l2, 'So x equals U cubed')),
      L("Both expressions equal x, so we set them equal. Ten T plus U equals U cubed plus four T plus four U. Now subtract "
        "four T and U from both sides. On the left, ten T minus four T leaves six T. On the right, four U minus U leaves "
        "three U. So six T equals U cubed plus three U.", show(l3, 'so we set them equal'), show(l3b, 'So six T equals'))),
    S('Method 1 · The math way: place values',
      # 2026-10-14 teacher-approved video correction (paragraph 6 re-read): say clearly that a two-digit number can't start with zero
      L("T is a digit, so it's at most nine, and six T is at most fifty-four. Can U be zero? Then U cubed plus three U is "
        "zero, so six T is zero, and T is zero. But T is the tens digit, and a two-digit number can't start with zero. So U "
        "isn't zero, and we test U from one."),
      L("U is one gives one plus three, which is four. U is two gives eight plus six, which is fourteen. U is three gives "
        "twenty-seven plus nine, which is thirty-six. U is four gives sixty-four plus twelve, which is seventy-six, already "
        "more than fifty-four. A bigger U only makes U cubed plus three U bigger, so we can stop.", show(l4, 'U is one gives')),
      L("Four and fourteen are not six times a digit, but thirty-six is. Six T is thirty-six, so T is six. Choice number "
        "three is our answer.", show(l5, 'Six T is thirty-six'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      sb='Method 1 · The math way: place values'),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's test the answer choices. Each choice gives a possible tens digit T, and then we need a digit U "
        "that fits the words of the question. Start with choice number one, seven. Then x is seventy plus U, and its digit "
        "sum is seven plus U. So seventy plus U must equal U cubed plus twenty-eight plus four U. Subtract twenty-eight and "
        "U from both sides, and U cubed plus three U must be forty-two.", show(m1, 'U cubed plus three U must be forty-two')),
      L("U is three gives twenty-seven plus nine, which is thirty-six, and U is four gives sixty-four plus twelve, which is "
        "seventy-six. As U grows, U cubed plus three U only grows, so it jumps from thirty-six straight to seventy-six. "
        "Forty-two is in between, so no digit U works, and choice number one is out.", mk('cross', 'choice 1', 'and choice number one is out')),
      L("The other tens digits work the same way. T is five needs U cubed plus three U to be thirty, and T is four needs it "
        "to be twenty-four. U is two gives only fourteen, and U is three already gives thirty-six. Thirty and twenty-four "
        "are in between, so no digit works, and choice numbers two and four are out.", show(m2, 'T is five needs'),
        mk('cross', 'choice 2', 'Thirty and twenty-four'), mk('cross', 'choice 4', 'choice numbers two and four are out')),
      L("T is six needs thirty-six, and U is three gives exactly that. So x is sixty-three. Let's check it in the words of "
        "the question. The units digit is three, and three cubed is twenty-seven. The digit sum is nine, and four times "
        "nine is thirty-six. Twenty-seven plus thirty-six is sixty-three. It fits, so choice number three is our answer. "
        "[pause] Okay. I'll see you in the next question.", show(m3, 'T is six needs thirty-six'),
        show(m4, "Let's check it in the words"), mk('tick', 'choice 3', 'It fits, so choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t18-01 (added)
# NEW: a middle column with a carry - "ends in the same digit" means 0 or 9 (the trap B = 0); a carry from two numbers
# is at most 1, from three or four numbers up to 2 or 3.  Methods: the columns, the algebraic form.
n1 = I('n1', '$\\begin{array}{r}2A6\\\\+\\ \\ B8\\\\\\hline 3A4\\end{array}$', size=46, col=1)
n2 = I('n2', 'Ones: $\\ 6+8=14$, $\\ $carry $1$', hand='Ones :    6 + 8 = 14,    carry 1')
n3 = I('n3', 'Tens: $\\ A+B+1$ ends in $A$: $\\ B+1=10$, $\\ \\hl{b}{B=9}$', size=32, hand='Tens :    A + B + 1  ends in  A :    B + 1 = 10,    \\hl{b}{B = 9}')
n4 = I('n4', '$256+98=354$ ✓', hand='256 + 98 = 354   ✓')
n5 = I('n5', 'Middle column, same digit: $\\ 0$ or $9$', size=28, col=1)
# Codex clarity pass 2026-10-12: a separate comparison slide avoids crowding the worked addition.
# These show/point phrases are live graphic cues, not words the teacher should read.
nc1 = I('nc1', 'No incoming carry: $A+C$ ends in $A$', size=30)
nc2 = I('nc2', '$C=0$: $5+0=5$', size=36, hand='C = 0 :    5 + 0 = 5')
nc3 = I('nc3', 'Incoming carry $1$: $A+B+1$ ends in $A$', size=30, col=1)
nc4 = I('nc4', '$B=9$: $5+9+1=15$', size=36, col=1, hand='B = 9 :    5 + 9 + 1 = 15')
nc5 = I('nc5', 'Check the incoming carry before choosing the digit', size=26)
o1 = I('o1', '$206+10A+10B+8=304+10A$', hand='206 + 10A + 10B + 8 = 304 + 10A')
o2 = I('o2', '$10B=304-214=90$: $\\ B=9$', hand='10B = 304 − 214 = 90 :    B = 9')
video('solve-q-r26-t18-01', 'solution', qid='q-r26-t18-01', slides=[
    S('Method 1 · The math way: columns',
      L("A and B represent digits. Given: two A six, plus B eight, is equal to three A four. B is equal to what?",
        pt('stem', 'A and B', 'hl', 6.0), voice='calm', pause=0.5),
      L("Two numbers with a letter in the middle. [short pause] We'll solve it two ways, with the columns, and then with the "
        "algebraic form.", pt('stem', 'a letter in the middle')),
      L("[short pause] Let's start with the columns. The ones, six plus eight is fourteen. Write four, it matches, and carry "
        "one.", show(n1, 'start with the columns'), show(n2, 'six plus eight')),
      L("The tens, A plus B plus the one ends in A. Now careful, a lot of students say ends in A, so B is zero. But there's a "
        "carry. A plus zero plus one ends in A plus one, not A. So choice number two is the trap.", mk('cross', 'choice 2', 'is the trap')),
      L("So B plus one has to be ten. B is nine, and one carries again. The hundreds, two plus one is three. It fits. Choice "
        "number four is our answer.", show(n3, 'B plus one has to be ten'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("With any A. Take five, two fifty-six plus ninety-eight is three fifty-four. So in a middle column, ends in the same "
        "digit means zero or nine, depending on the carry. And a carry from two numbers is at most one. Three or four numbers "
        "can carry two or three.", show(n4, 'two fifty-six'), show(n5, 'in a middle column'))),
    S('Method 1 · Why the carry changes the digit',
      L("Compare this with the earlier question where A plus C ended in A. That was the ones column, "
        "so nothing carried into it. C had to be zero. With A five, five plus zero is five, "
        "and the digit stays five.", show(nc1, 'A plus C ended in A'), show(nc2, 'C had to be zero')),
      L("Here we are in the tens column, and one carries in. So we add B and that one to A. "
        "To end in A again, those additions must make a full ten. B plus one is ten, so B is nine.",
        show(nc3, 'one carries in'), show(nc4, 'B is nine')),
      L("With A five, five plus nine plus one is fifteen. We write the five and carry the one. "
        "So the same ending digit does not always mean add zero. First check whether something carried into the column.",
        pt('nc4', 'five plus nine plus one is fifteen'), show(nc5, 'First check whether something carried')),
      sb='Method 1 · The math way: columns'),
    S('Method 2 · The math way: place values',
      L("[pause] Another way, with no columns at all. What's different? Each number is written by its digits, so no carry "
        "can be forgotten. Two hundred six plus ten A, plus ten B plus eight, equals three hundred four plus ten A.",
        show(o1, 'Two hundred six plus ten A')),
      L("Ten A is on both sides, it cancels, and that's why A can be any digit. Ten B is three hundred four minus two "
        "hundred fourteen, which is ninety. So B is nine. Choice number four. [pause] Okay. I'll see you in the next question.", show(o2, 'Ten B is'),
        mk('tick', 'choice 4', 'So B is nine'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t18-02 (added)
# NEW: ABC - CBA = 99(A - C) (why: the tens parts cancel).
# 2026-10-14 (teacher, her reading of 2026-10-14T07:33: "In 124 I changed it up a bit, because it seemed less complicated
# the way I did it"): the script now IS her reading (stumbles and failed takes left out). Her flow: the place values ->
# 99(A - C), a multiple of 99 -> count up from 99, adding 99 as "plus a hundred, minus one" (198, 297, 396) -> the
# pattern (hundreds digit up one, ones digit down one) -> 495 = choice 3. She dropped the old "nine in the middle" check
# (and its crosses) and the "build an example" part (621 - 126), so their visuals are gone. The clarity overlay entry of
# this lesson is reconciled (emptied): this spec holds her text directly. Visuals (all defined here, so the cue passes
# see them): the COLS figure of ABC - CBA (_method_visuals.COLS, built at her words, the tens column boxed when "the ten
# B parts cancel"), a "So far" box on slide 2 (Rule V2, the same item carry() makes), the +100 - 1 lines hand-written in
# chunks as she says them, and STACK99 below: the multiples in place-value columns (the COLS look), the hundreds column
# (+1) and the ones column (-1) boxed as she names them, 495 added in teal.
_mvs_spec = importlib.util.spec_from_file_location('_method_visuals_t18_stack', os.path.join(HERE, '_method_visuals.py'))
_MVS = importlib.util.module_from_spec(_mvs_spec); _mvs_spec.loader.exec_module(_MVS)


def STACK99(name, rows, steps, size=58, col=1):
    """three-digit numbers stacked in place-value columns, in the COLS look (fixed cells, the slide's math font, the
    teal box on a column): steps = [(key, change)], change: n = rows shown, h / o = the hundreds / ones column boxed
    with +1 / -1 between the rows, teal = indexes of the rows drawn in teal (the new one). Full snapshots, like COLS.
    -> {key: item} (the base 'line' first, then the layers in order)"""
    em = size; cw = em * 1.08; lab = em * 1.25; pad = em * .3; gap = em * 1.32; top = em * .55
    nrow = len(rows); W = int(2 * lab + 3 * cw + 2 * pad)
    Y = lambda r: top + em * .78 + gap * r
    H = int(Y(nrow - 1) + em * .5)
    X = lambda c: lab + pad + cw * (2 - c + .5)              # c = 0 ones, 1 tens, 2 hundreds
    st = dict(n=nrow, h=False, o=False, teal=())
    out = []
    for k, (key, ch) in enumerate(steps):
        st = dict(st, **ch)
        body = '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (W, H) if k else ''
        yb0, yb1 = top - em * .05, Y(st['n'] - 1) + em * .3
        for on, c in ((st['h'], 2), (st['o'], 0)):
            if on:
                body += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="%s" stroke="%s" stroke-width="3"/>'
                         % (X(c) - cw * .46, yb0, cw * .92, yb1 - yb0, _MVS.BAND, _MVS.TEAL))
        for r in range(st['n']):
            for c, d in enumerate(reversed(rows[r])):
                body += _MVS._glyph(d, X(c), Y(r), em, _MVS.TEAL if r in st['teal'] else _MVS.INK)[0]
        ls = em * .62
        for r in range(st['n'] - 1):
            ym = (Y(r) + Y(r + 1)) / 2 - em * .36 + ls * .36
            if st['h']: body += _MVS._gtext('+1', X(2) - cw * .5 - ls * 1.45, ym, ls, _MVS.TEAL)
            if st['o']: body += _MVS._gtext('−1', X(0) + cw * .5 + ls * .25, ym, ls, _MVS.TEAL)
        title = ('Multiples of 99 in columns: %s' % ', '.join(rows[:st['n']])) if not k else '%s: %s' % (key, ', '.join(rows[:st['n']]))
        out.append((key, _MVS._svg(W, H, body, title)))
    its = _MVS.items(_layers, name, out, col=col, own=True)
    return its


abc = _MVS.items(_layers, 'abc', _MVS.COLS(['ABC', 'CBA', ''], '−', [('line', dict(n=1, bar=False, res=False)),
                ('sub', dict(n=2, bar=True)), ('t', dict(hl=1, notes='10B − 10B = 0'))]), col=1, own=True)
keep1 = I('keep1', 'So far: $\\overline{ABC}-\\overline{CBA}=99(A-C)$', size=26, col=1); keep1['keep'] = 1
u1 = I('u1', '$\\overline{ABC}=100A+10B+C$', hand='ABC = 100A + 10B + C')
u2 = I('u2', '$\\overline{CBA}=100C+10B+A$', hand='CBA = 100C + 10B + A')
u3 = I('u3', '$\\overline{ABC}-\\overline{CBA}$', hand='ABC − CBA')
u4 = I('u4', '$=99A-99C$', hand='= 99A  − 99C')
u5 = I('u5', '$=99(A-C)$: $\\ $a multiple of $99$', hand='= 99(A − C) :  a multiple of 99')
c1 = I('c1', '$+100-1=+99$', hand='+100 − 1 = +99')
c2 = I('c2', '$99+100-1=198$', hand='99 + 100 − 1 = 198')
c3 = I('c3', '$198+100-1=297$', hand='198 + 100 − 1 = 297')
c4 = I('c4', '$297+100-1=396$', hand='297 + 100 − 1 = 396')
k99 = STACK99('k99', ['198', '297', '396', '495'], [('line', dict(n=3)), ('h', dict(h=True)), ('o', dict(o=True)),
                                                    ('n', dict(n=4, teal=(3,)))])
video('solve-q-r26-t18-02', 'solution', qid='q-r26-t18-02', slides=[
    S('Place values',
      L("A, B and C represent digits, and A is bigger than C, which is bigger than zero. Which of the following could be "
        "the value of A B C minus C B A?", pt('stem', 'A, B and C', 'hl', 7.0), voice='calm', pause=0.5),
      L("So we take the three-digit number A B C and subtract C B A, which is the same digits, just in reverse order. "
        "[short pause] We'll solve it in two different ways, writing their place values, and then trying numbers.",
        show(abc['line'], 'the three-digit number A B C'), show(abc['sub'], 'subtract C B A')),
      L("[short pause] Let's start with the place values. A B C equals a hundred A plus ten B plus C. C B A equals a "
        "hundred C plus ten B plus A. Subtract the second from the first, and the ten B parts cancel because B is in the "
        "same place in both of them. The A parts leave ninety-nine A, and the C parts leave minus ninety-nine C.",
        show(u1, 'A B C equals a hundred A'), show(u2, 'C B A equals a'), show(u3, 'Subtract the second from the first'),
        show(abc['t'], 'the ten B parts cancel'), show(u4, 'The A parts leave')),
      L("So the result is ninety-nine times A minus C. So it must be a multiple of ninety-nine.",
        show(u5, 'ninety-nine times')), sb='Method 1 · The math way: place values'),
    S('Trying numbers: count up by 99',
      L("Now let's check the answer choices, and we'll see which of the answer choices is divisible by ninety-nine. So one "
        "way for me to do this is to just count up from ninety-nine, right? So ninety-nine plus ninety-nine. Another way for "
        "me to do this, it's like doing plus a hundred minus one, right? That's the same as plus ninety-nine. So "
        "ninety-nine plus a hundred minus one is a hundred ninety-eight. A hundred ninety-eight plus a hundred minus one is "
        "two hundred ninety-seven. Two hundred ninety-seven plus a hundred minus one is three hundred ninety-six.",
        show(keep1, "Now let's check"), pt('keep1', "and we'll see which"), show(c1, 'like doing plus a hundred'), show(c2, 'So ninety-nine plus a hundred'),
        show(c3, 'A hundred ninety-eight plus'), show(c4, 'Two hundred ninety-seven plus')),
      L("Now we see that the pattern is that every time, we go up by one in the hundreds and down by one in the ones, "
        "right? Between two hundred ninety-seven and three hundred ninety-six, the hundreds digit goes up by one and the "
        "ones digit goes down by one. So now from three hundred ninety-six, I'll go up to four hundred ninety-five, right? "
        "And that's exactly our answer, four hundred ninety-five. So choice number three is our answer. [pause] I'll see "
        "you in the next question.",
        show(k99['line'], 'Now we see that the pattern'), show(k99['h'], 'up by one in the hundreds'),
        show(k99['o'], 'down by one in the ones'), show(k99['n'], "I'll go up to four hundred ninety-five"),
        pt('choice 3', "that's exactly our answer"), mk('tick', 'choice 3', 'So choice number three is our answer')),
      sb='Method 2 · Plugging in numbers'),
])

# ------------------------------------------------------------------------------------------------ q-r26-t18-03 (added)
# NEW: only the units digits decide the units digit of a product (3·7 = 21 -> 1); the size of a product (13·17 = 221 to
# 93·97, about 9,000).  Method: units digit and size (with a real example).
r1 = I('r1', '$3\\cdot7=21$: $\\ $ends in $1$', hand='3·7 = 21 :    ends in 1')
r2 = I('r2', 'Smallest: $\\ 13\\cdot17>10\\cdot10=100$', size=32, hand='Smallest :    13·17 > 10·10 = 100')
r3 = I('r3', 'Largest: $\\ 93\\cdot97<100\\cdot100=10{,}000$', size=32, hand='Largest :    93·97 < 100·100 = 10000')
r4 = I('r4', '$23\\cdot37=690+161=851$ ✓', hand='23·37 = 690 + 161 = 851   ✓')
video('solve-q-r26-t18-03', 'solution', qid='q-r26-t18-03', slides=[
    S('Units digit and size',
      L("A and B represent digits. Which of the following could be the value of A three, times B seven?",
        pt('stem', 'A and B', 'hl', 5.0), voice='calm', pause=0.5),
      L("A product with letters, and we don't need the letters, just two facts. [short pause] We'll solve it with the units "
        "digit and the size.", pt('stem', 'A product with letters')),
      L("[short pause] Fact one, only the units digits decide the units digit of a product. Three times seven is twenty-one, "
        "so the product ends in one. Eight fifty-seven ends in seven. Out.", show(r1, 'Three times seven'),
        mk('cross', 'choice 3', 'ends in seven. Out')),
      L("Fact two, the size. The smallest is thirteen times seventeen, two twenty-one. So ninety-one is too small. Out.",
        show(r2, 'thirteen times seventeen'), mk('cross', 'choice 1', 'too small. Out')),
      L("The largest is ninety-three times ninety-seven, less than a hundred times a hundred, ten thousand. So ten thousand "
        "and one is too big. Out.", show(r3, 'ninety-three times ninety-seven'), mk('cross', 'choice 4', 'too big. Out')),
      L("And eight fifty-one really happens. Twenty-three times thirty is six ninety, and twenty-three times seven is one "
        "sixty-one. Together, eight fifty-one. Choice number two is our answer. [pause] Okay. I'll see you in the next "
        "question.", show(r4, 'Twenty-three times thirty'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ r26-t18-summary
# REMINDERS only, said the way they were taught; new numbers.
s1s = I('s1s', '$\\overline{AB}=10A+B \\quad \\overline{ABC}=100A+10B+C$', size=36)
s2s = I('s2s', 'Same letter $\\to$ same digit $\\quad$ leading digit $\\ne0$', size=36)
s3s = I('s3s', 'Vertically $\\to$ units digit $\\to$ leftmost digit and size $\\to$ plug in', size=32)
s3w = I('s3w', 'Words: $\\ 10A+B=3(A+B)\\ \\to\\ 7A=2B$: $\\ 27$', size=32)
s4s = I('s4s', 'Ones column: $\\ X+Y$ ends in $X\\ \\to\\ Y=0$ $\\quad$ other columns: $\\ 0$ or $9$', size=32)
s5s = I('s5s', 'Two numbers, more digits $\\to$ leading digit $1$: $\\ 76+58=134$', size=32)
s6s = I('s6s', 'Special digits $0,\\ 1,\\ 5,\\ 6$: $\\ 15\\cdot15=225,\\ \\ 16\\cdot16=256$', size=32)
s7s = I('s7s', 'Subtraction $\\to$ addition $\\quad$ division $\\to$ multiplication', size=34)
s8s = I('s8s', '$\\overline{AB}+\\overline{BA}=11(A+B) \\quad \\overline{AB}-\\overline{BA}=9(A-B) \\quad \\overline{ABC}-\\overline{CBA}=99(A-C)$', size=28)
s9s = I('s9s', '$\\overline{AAA}=111A=3\\cdot37\\cdot A \\quad 444=37\\cdot12$', size=34)
s10s = I('s10s', 'Digit sum $10$: $\\ $largest $910$, $\\ $smallest $109$', size=34)
video('r26-t18-summary', 'lesson', slides=[
    S('Exercises with Letters: Summary',
      L("Before you practice, here's a quick summary of the topic. What the letters mean, the four steps, and the number "
        "facts.")),
    S('Letters are digits',
      L("A bar on top means the letters are the digits of one number. A B is ten A plus B, not A times B. And A B C is a "
        "hundred A, plus ten B, plus C.", show(s1s, 'A bar on top')),
      L("The same letter is always the same digit, and a leading digit is never zero. Different letters? Only if the question "
        "says so.", show(s2s, 'The same letter'))),
    S('The four steps',
      L("Write it vertically, check the units digit, check the leftmost digit and the size, and then plug in. One letter "
        "asked? Plug in the choices.", show(s3s, 'Write it vertically')),
      L("A puzzle in words, with no columns? Write the number as ten A plus B, and collect the letters on each side. Ten A "
        "plus B equals three times A plus B gives seven A equals two B, so the number is twenty-seven.", show(s3w, 'A puzzle in words')),
      L("In the ones column nothing carries in, so X plus Y ends in X means Y is zero. In any other column there may be a "
        "carry, so it's zero or nine.", show(s4s, 'In the ones column')),
      L("Two numbers, and the sum has more digits? The leading digit is one. Seventy-six plus fifty-eight is one thirty-four. "
        "Only for two numbers.", show(s5s, 'the sum has more digits'))),
    S('Tools',
      L("The special digits, zero, one, five and six, keep their units digit when multiplied by themselves. Fifteen times "
        "fifteen is two twenty-five, and sixteen times sixteen is two fifty-six.", show(s6s, 'The special digits')),
      L("A subtraction? Flip it into an addition. A division? Flip it into a multiplication.", show(s7s, 'Flip it into an addition')),
      L("A number plus its reversal divides by eleven, minus its reversal by nine, and with three digits, by ninety-nine.",
        show(s8s, 'plus its reversal'))),
    S('Number facts',
      L("A A A is a hundred eleven times A, so it divides by three and by thirty-seven. Four forty-four is thirty-seven times "
        "twelve.", show(s9s, 'A A A is a hundred eleven')),
      L("Largest with a given digit sum, big digits on the left. Smallest, choose the smallest possible digits on the left "
        "while leaving enough room for the rest of the digit sum. The first cannot be zero, and no digit can exceed nine. "
        "Digit sum ten, the largest is nine hundred ten and the smallest is one hundred nine. [pause] That's it. Now go practice, and I'll see you in the next "
        "video.", show(s10s, 'Largest with a given digit sum'))),
])

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
 "q-513": "A, B and C represent digits. Given: $\\overline{CB}\\times B=\\overline{ACB}$\nWhich of the following could be B?",
 "q-517": "A, B and C represent digits. Given: $\\overline{CA}\\times\\overline{CA}=\\overline{6BA}$\nWhich of the following could be $A-C$?"
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



# 2026-10-14 the camera lesson in parts of about 3-4 minutes (math_patches/_camera_parts.py), before the visual passes
_cp_spec = importlib.util.spec_from_file_location('_camera_parts', os.path.join(HERE, '_camera_parts.py'))
CP = importlib.util.module_from_spec(_cp_spec); _cp_spec.loader.exec_module(CP)
CP.split(globals(), 'digit-puzzles', 'Exercises with Letters', [(1, None), (4, "Let's continue with exercises with letters, and learn how to solve them.")])

for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _stem_parts(_v); _write_gap(_v)


# Spoken clarity revision: preserves the complete original board/cue plan.
_clarity_spec = importlib.util.spec_from_file_location(
    '_codex_script_clarity_20261012', os.path.join(HERE, '_codex_script_clarity_20261012.py'))
_clarity_module = importlib.util.module_from_spec(_clarity_spec)
_clarity_spec.loader.exec_module(_clarity_module)
_clarity_module.apply(VIDEOS)

# 2026-10-13 method visuals + carry-over boxes (math_patches/_method_visuals.py; teacher: "a method with a signature visual
# is shown with THAT visual, built step by step" and "when you clear the slide, something important should stay"). Runs
# AFTER the clarity overlay, so the overlay's cue checks see the plan they were made for. Visual only, no spoken text.
import types as _types
_mv_spec = importlib.util.spec_from_file_location('_method_visuals', os.path.join(HERE, '_method_visuals.py'))
_mv = importlib.util.module_from_spec(_mv_spec); _mv_spec.loader.exec_module(_mv)
_mv.post(_types.SimpleNamespace(**globals()), 18)

# 2026-10-14 (q-r26-t18-02, her own reading): her hand-written lines are written in chunks while she says each part
# ("= 198" only at "is a hundred ninety-eight"), so an auto POINT on such a line in the same paragraph would light a
# half-written line; the writing itself is the focus there (calm highlights). Drop those POINTs, and a POINT on a figure
# less than ~2 s (28 characters) after one of its layers was drawn (the new layer is what she is talking about).
for _ln in [l for _sl in VIDEOS['solve-q-r26-t18-02']['slides'] for l in _sl['lines']]:
    _hand = {c[1]['_name'] for c in _ln['cues'] if c[0] == 'show' and c[1].get('_hand')}
    _keep = []
    for c in _ln['cues']:
        _prev = _keep[-1] if _keep else None
        _just = (_prev and _prev[0] == 'show' and _base(_prev[1]['_name']) == c[1]
                 and 0 <= _phrase_pos(_ln['say'], c) - _phrase_pos(_ln['say'], _prev) < 28)
        if c[0] == 'point' and (c[1] in _hand or _just): continue
        _keep.append(c)
    _ln['cues'] = _keep

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
