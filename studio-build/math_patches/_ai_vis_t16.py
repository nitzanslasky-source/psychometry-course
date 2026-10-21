"""Topic 16 (Integers) - the redo for the teacher's own-voice reading (2026-10-11), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The teacher records only the camera lesson 'whole-numbers' (re-record, never touched here). Every other topic-16 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t16.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t16.py ai_redo_t16() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-16-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t16ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-16 flow order of the scripts (whole-numbers = the camera lesson, not here)
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
            out.append((it, d))
        per.append(out)
    return names, per


# 2026-10-14 Rule V4.8 (camera lessons: the face bubble never covers math). Her bubble is composited top right (board
# x >= 1344, y <= 256). In the camera lesson and its parts: a right-column stack that would start above y 262 moves down
# as a whole (its own order and spacing kept), and a left-column item is at most 920 wide (ends left of x 1330; a figure
# and its layers are scaled down together, text wraps). Other videos are unchanged.
CAM_BASE = 'whole-numbers'
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
    if re.search(r'\b(point|dot) (zero|one|two|three|four|five|six|seven|eight|nine)\b|\d\.\d', allt): probs.append('a decimal - no decimal estimates')
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
            'style': "the teacher reads it herself (Reading Studio), topic-16 redo (2026-10-11): math_patches/_ai_vis_t16.py is "
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



# ------------------------------------------------------------------------------------------- topic-14 figures
# Both figures are BUILT in layers at the spoken words (like DIST in topic 13): every layer is a figure item of the same
# size drawn at the same place (over=1), shown in order. Labels are big and bold (about the size of the handwriting).
def _svg(vb, body, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, title, title, body))


LAYER_BASE = {}     # a figure layer's item name -> its base item's name (a POINT on a layer lights nothing visible)


def _layers(name, out, w, col):
    items = {}
    base = '%s_%s' % (name, out[0][0])
    for k, sv in out:
        it = NL('%s_%s' % (name, k), sv, w=w, col=col)
        if k != 'line' and k != 'root': it['over'] = 1; it['gap'] = 0; LAYER_BASE[it['_name']] = base
        items[k] = it
    return items


RED = '#d62d48'


def STRIP(name, lo, hi, layers, base=(), w=1060, col=0):
    """a number strip from lo to hi: a short tick at EVERY whole number, a label under each number in `base`.
    layers = [(key, [mark, ...]), ...] drawn on top, in order. Marks:
      ('prime', v)          a teal dot on v and a bold teal label (a prime)
      ('lab', v)            a label under v (ink)
      ('cross', v)          a red cross over v's label (ruled out)
      ('ring', v)           a teal ring around v's label (the pick)
      ('span', a, b, text)  a teal bracket above the line from a to b, with text above it
    -> {key: item}; show them in order (the base line is key 'line')."""
    L_, R_, Y_ = 30, 610, 70
    X = lambda v: L_ + 14 + (v - lo) / float(hi - lo) * (R_ - L_ - 28)
    INK, TEAL, FONT = SNL.INK, SNL.TEAL, SNL.FONT
    lab = lambda v, col_, fw='bold': ('<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="19" font-weight="%s">%d</text>'
                                     % (X(v), Y_ + 32, col_, FONT, fw, v))
    body = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.5"/>' % (L_ - 6, Y_, R_ + 6, Y_, INK) +
            '<path d="M %d %d l 11 -6 l 0 12 Z" fill="%s"/>' % (L_ - 10, Y_, INK) + '<path d="M %d %d l -11 -6 l 0 12 Z" fill="%s"/>' % (R_ + 10, Y_, INK) +
            ''.join('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.6"/>' % (X(v), Y_ - 7, X(v), Y_ + 7, INK) for v in range(lo, hi + 1)) +
            ''.join(lab(v, INK) for v in base))
    out = [('line', _svg('0 10 640 112', body, 'Whole numbers from %d to %d' % (lo, hi)))]
    for key, marks in layers:
        b = ''
        for m in marks:
            if m[0] == 'prime':
                b += '<circle cx="%.1f" cy="%d" r="6" fill="%s"/>' % (X(m[1]), Y_, TEAL) + lab(m[1], TEAL)
            elif m[0] == 'lab':
                b += lab(m[1], INK)
            elif m[0] == 'cross':
                x0 = X(m[1]); b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3"/>' % (x0 - 11, Y_ + 14, x0 + 11, Y_ + 38, RED) +
                                    '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3"/>' % (x0 + 11, Y_ + 14, x0 - 11, Y_ + 38, RED))
            elif m[0] == 'ring':
                b += '<rect x="%.1f" y="%d" width="30" height="28" rx="9" fill="none" stroke="%s" stroke-width="2.6"/>' % (X(m[1]) - 15, Y_ + 12, TEAL)
            elif m[0] == 'span':
                a, c = X(m[1]), X(m[2])
                b += ('<path d="M %.1f %d L %.1f %d L %.1f %d L %.1f %d" fill="none" stroke="%s" stroke-width="2.4"/>' % (a, Y_ - 12, a, Y_ - 22, c, Y_ - 22, c, Y_ - 12, TEAL) +
                      '<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="19" font-weight="bold">%s</text>' % ((a + c) / 2, Y_ - 30, TEAL, FONT, m[3]))
        out.append((key, _svg('0 10 640 112', b, key)))
    return _layers(name, out, w, col)


def TREE(name, root, steps, w=330, col=1, dx=92, dy=50):
    """a factor ladder: root at the top; step i splits the number on the right into (prime, rest) - the prime is circled
    at the lower left, the rest goes on down to the right (the last rest, a prime, is circled too). -> {'root': item,
    1: item, 2: item, ...}; show 'root' first, then the steps in order. Labels are plain digits."""
    INK, TEAL, FONT = SNL.INK, SNL.TEAL, SNL.FONT
    n = len(steps); x0, y0 = 92, 40
    W = x0 + n * dx + 70; H = y0 + n * dy + 34
    pos = lambda i: (x0 + i * dx, y0 + i * dy)
    def node(x, y, t, prime):
        s = '<text x="%.1f" y="%.1f" text-anchor="middle" fill="%s" %s font-size="30" font-weight="bold">%s</text>' % (x, y + 10, TEAL if prime else INK, FONT, t)
        if prime: s += '<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s" stroke-width="2.6"/>' % (x, y, 15 + 6 * (len(str(t)) - 1), TEAL)
        return s
    vb = '0 0 %d %d' % (W, H)
    out = [('root', _svg(vb, node(x0, y0, root, False), 'Factor tree of %s' % root))]
    for i, (p, rest) in enumerate(steps):
        (ax, ay), (bx, by) = pos(i), pos(i + 1)
        lx = ax - dx * 0.7; last = i == n - 1
        body = ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4"/>' % (ax - 10, ay + 22, lx + 6, by - 22, INK) +
                '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4"/>' % (ax + 10, ay + 22, bx - 6, by - 22, INK) +
                node(lx, by, p, True) + node(bx, by, rest, last))
        out.append((i + 1, _svg(vb, body, '%s splits into %s and %s' % (root if i == 0 else steps[i - 1][1], p, rest))))
    items = _layers(name, out, w, col)
    return items



# =================================================================================================================
# THE SCRIPTS (topic-16 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-16-AI-scripts-review.md.
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ whole-numbers (camera lesson)
# 2026-10-13 teacher: her camera first lesson as a reading script too ("the same style, with the handwriting ... maybe a
# bit more examples"), read with the camera on. NEW (the whole topic relies on it): the sign rules for multiplying and
# dividing (2-3 examples each + the non-example "a positive product is not two positives"), counting the minuses (odd /
# even, why), even powers, odd powers, absolute value, -x = the opposite, zero, sums (the farther-from-zero number wins;
# counting minuses does not work there), and the sign-question habit (surely positive pieces first; the given "not
# zero"). Hebrew lesson (alg 15738-15814): every rule kept; its sample question is q-457.
# 2026-10-15 batch-A review (Codex, reviews/batch-A.md #67): every example is its own board line at its clause (V4); the
# sign-question habit is exact (x not zero -> x squared and |x| positive; x = 0 -> both 0; a positive factor of a product
# or quotient keeps the sign); "minus nine is farther from zero"; the equal-distance case -4 + 4 = 0.
wn1 = I('wn1', '$4\\cdot5=20$', size=32, hand='4·5 = 20')
wn1b = I('wn1b', '$(-4)\\cdot(-5)=20$', size=32, hand='(−4)·(−5) = 20')
wn2 = I('wn2', '$(-4)\\cdot5=-20$', size=32, hand='(−4)·5 = −20')
wn2a = I('wn2a', '$4\\cdot(-5)=-20$', size=32, hand='4·(−5) = −20')
wn2b = I('wn2b', '$(-3)\\cdot(-6)=18$', size=32, hand='(−3)·(−6) = 18')
wn3 = I('wn3', '$ab>0$: same sign', size=28)
wn3b = I('wn3b', '$ab<0$: different signs', size=28)
wn3c = I('wn3c', '$ab=0$: at least one is $0$', size=28)
wn4 = I('wn4', '$(-2)\\cdot3\\cdot(-1)\\cdot(-4)$: $\\ 3$ minuses $\\to\\ -24$', size=32, hand='(−2)·3·(−1)·(−4) :    3 minuses  →  −24')
wn5 = I('wn5', '$(-2)\\cdot(-3)\\cdot(-1)\\cdot(-4)$: $\\ 4$ minuses $\\to\\ 24$', size=32, hand='(−2)·(−3)·(−1)·(−4) :    4 minuses  →  24')
wn6 = I('wn6', '$(-24)\\div(-8)=3$', size=32, hand='(−24) ÷ (−8) = 3')
wn6b = I('wn6b', '$(-24)\\div8=-3$', size=32, hand='(−24) ÷ 8 = −3')
wn6c = I('wn6c', '$24\\div(-8)=-3$', size=32, hand='24 ÷ (−8) = −3')
wn7 = I('wn7', '$\\frac{(-6)\\cdot(-2)}{-3}$: $\\ 3$ minuses', size=34, hand='{(−6)·(−2)/−3} :    3 minuses')
wn7b = I('wn7b', '$6\\cdot2=12,\\ \\ \\frac{12}{3}=4\\ \\to\\ -4$', size=34, hand='6·2 = 12,    {12/3} = 4   →   −4')
wn8 = I('wn8', '$3^2=9$', size=32, hand='3^2 = 9')
wn8b = I('wn8b', '$(-3)^2=9$', size=32, hand='(−3)^2 = 9')
wn8c = I('wn8c', '$(-2)^4=16$', size=32, hand='(−2)^4 = 16')
wn9 = I('wn9', '$2^3=8$', size=32, hand='2^3 = 8')
wn9b = I('wn9b', '$(-2)^3=-8$', size=32, hand='(−2)^3 = −8')
wn9c = I('wn9c', '$(-1)^5=-1$', size=32, hand='(−1)^5 = −1')
wn10 = I('wn10', '$|-7|=7$', size=32, col=1, hand='|−7| = 7')
wn10b = I('wn10b', '$|7|=7$', size=32, col=1, hand='|7| = 7')
wn10c = I('wn10c', '$|0|=0$', size=32, col=1, hand='|0| = 0')
wn11 = I('wn11', '$x=-9\\ \\to\\ -x=9$', size=30, col=1, hand='x = −9  →  −x = 9')
wn11b = I('wn11b', '$x=5\\ \\to\\ -x=-5$', size=30, col=1, hand='x = 5  →  −x = −5')
wn12 = I('wn12', '$(-3)+(-5)=-8$', size=32, hand='(−3) + (−5) = −8')
wn13 = I('wn13', '$-9+4=-5$', size=32, hand='−9 + 4 = −5')
wn13b = I('wn13b', '$-4+9=5$', size=32, hand='−4 + 9 = 5')
wn13c = I('wn13c', '$-4+4=0$', size=32, hand='−4 + 4 = 0')
wn13d = I('wn13d', '$-2+7=5$', size=32, hand='−2 + 7 = 5')
wn14 = I('wn14', '$x\\ne0$: $\\ x^2>0,\\ \\ |x|>0$', size=30, hand='x ≠ 0 :    x^2 > 0,    |x| > 0')
wn14b = I('wn14b', '$x=0$: $\\ x^2=|x|=0$', size=30, hand='x = 0 :    x^2 = |x| = 0')
wn14c = I('wn14c', 'Product or quotient: a positive piece keeps the sign', size=28)
video('whole-numbers', 'lesson', slides=[
    S('Integers',
      L("Welcome to integers. Some algebra questions don't ask for a number at all. They ask whether an expression is "
        "positive, negative, or whether we can't tell. These questions rest on a few basic sign rules, and usually they're "
        "easy, so let's go through the rules one by one.")),
    S('Multiplying',
      L("Let's start with multiplying. When two numbers have the same sign, the result is positive. Four times five is "
        "twenty, and negative four times negative five is also twenty.", show(wn1, 'Four times five is twenty'),
        show(wn1b, 'negative four times negative five')),
      L("When the signs are different, the result is negative, and the order doesn't matter. Negative four times five is "
        "negative twenty, and four times negative five is negative twenty too.", show(wn2, 'Negative four times five'),
        show(wn2a, 'and four times negative five')),
      L("Careful here. A positive product doesn't mean both numbers are positive. Negative three times negative six is "
        "eighteen, which is positive, but both numbers are negative. So a positive product only tells us that the two "
        "numbers have the same sign. A negative product tells us their signs are different. And a product of zero means "
        "at least one of them is zero.", show(wn2b, 'Negative three times negative six'),
        show(wn3, 'A positive product only tells us'), show(wn3b, 'A negative product tells us'), show(wn3c, 'And a product of zero'))),
    S('Count the minuses',
      L("Now a time saver. When many numbers are multiplied, the plus signs don't change the sign of the result. Only the "
        "minus signs do. So we just count the minuses."),
      L("Negative two, times three, times negative one, times negative four. Let's count the minuses: one, two, three. "
        "Three is odd, so the result is negative. Let's check. Two times three times one times four is twenty-four, so the "
        "result is negative twenty-four.", show(wn4, "Let's count the minuses")),
      L("Now negative two, times negative three, times negative one, times negative four. That's four minuses, an even "
        "number, so the result is positive, twenty-four.", show(wn5, 'That\'s four minuses')),
      L("Why does this work? Negative times negative is positive. So every two minuses cancel into a plus and stop "
        "mattering. An even number of minuses cancel completely, and an odd number leaves one minus.")),
    S('Dividing',
      L("Division follows exactly the same rules, so there's nothing new to remember. Negative twenty-four divided by "
        "negative eight is three, positive, because the signs are the same. Negative twenty-four divided by eight is "
        "negative three, and twenty-four divided by negative eight is negative three too, because the signs are "
        "different.", show(wn6, 'Negative twenty-four divided by negative eight'),
        show(wn6b, 'Negative twenty-four divided by eight'), show(wn6c, 'and twenty-four divided by negative eight')),
      L("So we can count the minuses when we multiply and divide together. Negative six times negative two, over negative "
        "three. That's three minuses, so the result is negative. Six times two is twelve, and twelve over three is four, "
        "so it's negative four.", show(wn7, 'Negative six times negative two'), show(wn7b, 'Six times two is twelve'))),
    S('Powers, absolute value, the opposite',
      L("Now powers. A number to an even power is never negative. Three squared is nine, negative three, squared, is also "
        "nine, and negative two to the power of four is sixteen. The only way to get zero is a base of zero.",
        show(wn8, 'Three squared is nine'), show(wn8b, 'negative three, squared'), show(wn8c, 'negative two to the power of four')),
      L("An odd power keeps the sign of the number. Two to the power of three is eight, negative two to the power of three "
        "is negative eight, and negative one to the power of five is negative one.", show(wn9, 'Two to the power of three'),
        show(wn9b, 'negative two to the power of three'), show(wn9c, 'negative one to the power of five')),
      L("An absolute value is zero or positive. The absolute value of negative seven is seven, the absolute value of seven "
        "is seven, and the absolute value of zero is zero. So if y isn't zero, the absolute value of y is positive.",
        show(wn10, 'The absolute value of negative seven'), show(wn10b, 'the absolute value of seven is'),
        show(wn10c, 'the absolute value of zero')),
      L("And a minus in front of a letter doesn't mean the number is negative. It means the opposite number. If x is "
        "negative nine, minus x is nine, which is positive. If x is five, minus x is negative five. And zero is neither "
        "positive nor negative.", show(wn11, 'If x is negative nine'), show(wn11b, 'If x is five'))),
    S('Adding',
      L("Adding works differently. Two negative numbers add up to a negative number. Negative three plus negative five is "
        "negative eight.", show(wn12, 'Negative three plus negative five')),
      L("With different signs, the number that's farther from zero decides the sign. Negative nine plus four is negative "
        "five, because negative nine is farther from zero than four. But negative four plus nine is five, positive. And "
        "when they're the same distance from zero, like negative four plus four, the result is zero. So counting the "
        "minuses works only for multiplying and dividing. Negative two plus seven has one minus, but the result, five, is "
        "positive.", show(wn13, 'Negative nine plus four'), show(wn13b, 'But negative four plus nine'),
        show(wn13c, 'like negative four plus four'), show(wn13d, 'but the result, five'))),
    S('In a sign question',
      L("So how do we use all this in a question? First find the pieces that are surely positive. If x isn't zero, x "
        "squared and the absolute value of x are positive. If x is zero, they're both zero. In a product or a quotient, a "
        "positive piece doesn't change the sign. So the other piece decides the sign. And when the question says that a "
        "letter is not zero, it's usually so that the bottom of a fraction isn't zero. You'll see all of this in the next "
        "question. [pause] I'll see you in the next video.", show(wn14, "If x isn't zero"), show(wn14b, "If x is zero, they're"),
        show(wn14c, 'In a product or a quotient'))),
])

# ------------------------------------------------------------------------------------------------ q-457 (Q1)
# NEW: find the pieces that are surely positive, and the one piece left decides the sign; why "a is not 0" is given;
# the trap "b < 0" (we learn nothing about b's sign).  REMINDER: even powers and absolute values are never negative,
# an odd power keeps the sign (camera lesson, topic 8).
a1 = I('a1', '$|a|>0$ $\\quad b^2>0$', hand='|a| > 0      b^2 > 0')
a2 = I('a2', 'So the top is negative: $\\ a^5<0$', size=32, hand='So the top is negative :   a^5 < 0')
a3 = I('a3', 'Odd power keeps the sign: $\\ \\hl{a}{a<0}$', size=32, hand='Odd power keeps the sign :   \\hl{a}{a < 0}')
a4 = I('a4', 'Find the surely positive pieces first', size=28, col=1)
a6 = I('a6', '$\\frac{(-2)^3\\cdot4}{2}<0\\qquad\\frac{(-2)^2\\cdot4}{2}>0$', size=28, col=1, hand='{(−2)^3·4/2} < 0        {(−2)^2·4/2} > 0')
a5 = I('a5', '$b$: only $b\\ne0$ ✗', size=30, col=1, hand='b :   only  b ≠ 0   ✗')
b1 = I('b1', '$a=1,\\ b=1$: $\\ \\frac{1}{1}=1$ ✗', hand='a = 1,  b = 1 :    {1/1} = 1   ✗')
b2 = I('b2', '$a=-1,\\ b=1$: $\\ \\frac{-1}{1}=-1$ ✓', hand='a = −1,  b = 1 :    {−1/1} = −1   ✓')
b3 = I('b3', 'Positive $b$ works: $\\ $(2) ✗', size=30, col=1, hand='Positive b works :   (2) ✗')
video('solve-q-457', 'solution', qid='q-457', slides=[
    S('Method 1 · Understanding',
      L("Given: a is not equal to zero, and a to the power of five, times b squared, over the absolute value of a, is "
        "smaller than zero. Which of the following is necessarily true?", pt('stem', 'Given', 'hl', 9.0), voice='calm', pause=0.5),
      L("So it's a sign question, not a calculation. The whole fraction is negative, and we have to find out what that says about a and b. The trick is to find the pieces that are surely positive, because then the piece that's left decides the sign. For example, negative two cubed, times four, over two. Four and two are positive, so the sign comes from negative two cubed, negative eight, and the whole thing is negative. And negative two squared times four, over two? Every piece is positive, so it's positive. [short pause] We'll solve it two ways, piece by piece, and then plugging in numbers.",
        pt('stem: g2', 'The whole fraction is negative'), show(a6, 'For example, negative two cubed')),
      L("[short pause] Let's start piece by piece, and first find the pieces that are surely positive. Why do they tell us "
        "a isn't zero? So the bottom isn't zero. The bottom is the absolute value of a, and remember, an absolute value is "
        "zero or positive. It can't be zero here, so it's positive.", show(a4, 'the pieces that are surely positive'), pt('stem: g1', "a isn't zero")),
      L("b squared is an even power, so it's never negative. And b can't be zero, because then the whole fraction would be "
        "zero, not smaller than zero. So b squared is positive too.", show(a1, 'b squared is an even power')),
      L("So the bottom is positive, and one piece on top is positive. For the fraction to be negative, the piece that's "
        "left must be negative. So a to the power of five is negative.", show(a2, 'the piece that\'s left')),
      L("And an odd power keeps the sign. So a itself is negative. Choice number four is our answer.",
        show(a3, 'an odd power keeps the sign'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Now careful, choice number two is the trap. It says b is negative too. But all we learned about b is that it isn't "
        "zero. It can be positive or negative.", show(a5, 'all we learned about b'), mk('cross', 'choice 2', 'positive or negative'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers. Is a positive possible? a is one and b is one. One to the power of five is one, b squared is one, and the bottom is one, so the fraction is one. That's not smaller than zero, so a can't be positive.", show(b1, 'a is one and b is one')),
      L("So a negative a. a is negative one, b is one. Negative one to the power of five is negative one, and b squared and the bottom are both one, so the fraction is negative one. It works. And b was positive here, so b doesn't have to be negative.",
        show(b2, 'a is negative one'), show(b3, 'b was positive here')),
      L("Choice numbers one and three say a is positive, so they're out, and choice number two needs b negative, out too. "
        "So choice number four. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 1', 'Choice numbers one'), mk('cross', 'choice 3', 'and three say'), mk('cross', 'choice 2', 'out too'),
        mk('tick', 'choice 4', 'So choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t16-01 (Q2)
# NEW: in a sum with mixed signs, the one bigger in size wins (why); a positive sum -> the positive one is bigger in
# size.  REMINDER: sign rules for products (camera lesson), absolute value as size (topic 13).
c1 = I('c1', 'Mixed signs: the bigger size wins', size=28, col=1)
c2 = I('c2', '$-2+5=3$ $\\quad -5+2=-3$', size=32, col=1, hand='−2 + 5 = 3      −5 + 2 = −3')
c3 = I('c3', '$x+y>0$: $\\ y$ wins, $\\ \\hl{a}{|y|>|x|}$', hand='x + y > 0 :    y wins,   \\hl{a}{|y| > |x|}')
d1 = I('d1', '$x=-1,\\ y=3$: $\\ -1+3=2>0$ ✓', hand='x = −1,  y = 3 :    −1 + 3 = 2 > 0   ✓')
d2 = I('d2', '(1) $1>3$ ✗ $\\quad$(3) $-3>0$ ✗ $\\quad$(4) $-4>0$ ✗', size=30, hand='(1)  1 > 3  ✗     (3)  −3 > 0  ✗     (4)  −4 > 0  ✗')
video('solve-q-r26-t16-01', 'solution', qid='q-r26-t16-01', slides=[
    S('Method 1 · Understanding',
      L("Given: x is smaller than zero, which is smaller than y, and x plus y is bigger than zero. Which of the following is "
        "necessarily true?", pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("So x is negative and y is positive, mixed signs. And their sum is positive. [short pause] We'll solve it two ways, "
        "with the sizes, and then plugging in numbers.", pt('stem: g1', 'x is negative and y is positive'), pt('stem: g2', 'their sum is positive')),
      L("[short pause] Let's start with the sizes. When you add a negative and a positive, they fight, and the one that's "
        "bigger in size wins. Negative two plus five is three, positive, because five is bigger in size. Negative five plus "
        "two is negative three.", show(c1, 'the one that\'s bigger in size wins'), show(c2, 'Negative two plus five')),
      L("Here the sum is positive, so the positive one won. y is bigger in size than x. Choice number two is our answer. And "
        "choice number one is the opposite.", show(c3, 'the positive one won'), mk('tick', 'choice 2', 'Choice number two is our answer'),
        mk('cross', 'choice 1', 'is the opposite'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers that fit. x is negative one and y is three. Negative one plus three is "
        "two, positive, so they fit.", show(d1, 'x is negative one')),
      L("Choice number one, one bigger than three? No. Choice number three, negative one times three is negative three, "
        "bigger than zero? No. Choice number four, negative one minus three is negative four. No. Three are out, so choice "
        "number two. [pause] Okay. I'll see you in the next question.",
        show(d2, 'Choice number one, one bigger'), mk('cross', 'choice 1', 'than three? No'), mk('cross', 'choice 3', 'zero? No'),
        mk('cross', 'choice 4', 'negative four. No'), mk('tick', 'choice 2', 'so choice number two'))),
])

# ------------------------------------------------------------------------------------------------ consecutive-integers (lesson)
# NEW: three ways into consecutive numbers - one letter (from the middle), plugging in the smallest legal numbers
# (check the choices first), the differences with their signs; "bigger than zero" doesn't mean starting at one.
# REMINDER: what consecutive (even / odd) numbers are (topic 1).
e1 = I('e1', '$5,\\ 6,\\ 7\\qquad -3,\\ -2,\\ -1\\qquad 4,\\ 6,\\ 8$', size=40, hand='5, 6, 7        −3, −2, −1        4, 6, 8')
e2 = I('e2', '$b-1,\\ \\ b,\\ \\ b+1$ $\\quad b=8$: $\\ 7,\\ 8,\\ 9$', size=40, hand='b − 1,   b,   b + 1      b = 8 :   7,  8,  9')
e3 = I('e3', 'Evens or odds: $\\ b-2,\\ \\ b,\\ \\ b+2$', size=40, hand='Evens or odds :    b − 2,   b,   b + 2')
e4 = I('e4', 'Plug in: $\\ 1,\\ 2,\\ 3$ $\\ $(choices must differ)', size=38, hand='Plug in :    1,  2,  3     (choices must differ)')
e5 = I('e5', '$8-7=1\\quad 7-8=-1\\quad 9-7=2\\quad 7-9=-2$', size=38, hand='8 − 7 = 1     7 − 8 = −1     9 − 7 = 2     7 − 9 = −2')
e6 = I('e6', '$x>0$: $\\ $maybe $23,\\ 24,\\ 25$', size=40, hand='x > 0 :    maybe  23,  24,  25')
video('consecutive-integers', 'lesson', slides=[
    S('Consecutive Integers',
      L("Welcome back. Now consecutive numbers. Questions about them usually have more than one way in, so we'll learn three, "
        "and you pick the one that's easiest for you.")),
    S('Three ways in',
      L("Remember, consecutive numbers are integers in a row, each one more than the one before. Five, six, seven. Negatives "
        "count too, negative three, negative two, negative one. And consecutive even numbers, or odd numbers, go up by two, "
        "four, six, eight.", show(e1, 'Five, six, seven')),
      L("The first way, one letter. Write all of them with one letter, and the middle one is usually the neatest. Three in a row are b minus one, b, and b plus one. If b is eight, that's seven, eight, nine, and if b is twenty, nineteen, twenty, twenty-one. For evens or odds, b minus two, b, and b plus two, so with b eight, six, eight, ten.",
        show(e2, 'Three in a row are'), show(e3, 'For evens or odds')),
      L("The second way, plugging in numbers. Take the smallest legal numbers, like one, two, three, because they're the "
        "easiest to work with. But first check that the choices come out different with them. If two choices tie, take "
        "other numbers.", show(e4, 'the smallest legal numbers')),
      L("The third way, the differences. Bigger minus smaller is one, and smaller minus bigger is negative one. Eight minus seven is one, but seven minus eight is negative one. And two steps apart, nine minus seven is two, and seven minus nine is negative two. The size is the same, but the sign isn't, so watch the sign.", show(e5, 'Bigger minus smaller')),
      L("And one trap. If they say the numbers are bigger than zero, it doesn't mean they start at one. They could be "
        "twenty-three, twenty-four, twenty-five. [pause] Okay. I'll see you in the next video.", show(e6, 'bigger than zero'))),
])

# ------------------------------------------------------------------------------------------------ q-458 (Q3)
# NEW: write consecutive evens around the middle (q - 2, q, q + 2); r^2 - p^2 as (r - p)(r + p); the trap 2 (a gap of
# one).  REMINDER: the third shortcut formula (topic 4), plugging in the smallest legal numbers (lesson).
f1 = I('f1', '$p=q-2,\\ \\ \\ r=q+2$', hand='p = q − 2,      r = q + 2')
f2 = I('f2', '$r^2-p^2=(r-p)(r+p)$', hand='r^2 − p^2 = (r − p)(r + p)')
f3 = I('f3', '$r-p=4,\\ \\ \\ r+p=2q$', hand='r − p = 4,      r + p = 2q')
f4 = I('f4', '$\\frac{4\\cdot2q}{2q}=\\hl{a}{4}$', hand='{4·2q/2q} = \\hl{a}{4}')
f5 = I('f5', 'Evens: the gap is $2$, not $1$', size=28, col=1)
g1 = I('g1', '$p=2,\\ q=4,\\ r=6$', hand='p = 2,   q = 4,   r = 6')
g2 = I('g2', '$\\frac{36-4}{8}=\\frac{32}{8}=\\hl{a}{4}$', hand='{36 − 4/8} = {32/8} = \\hl{a}{4}')
video('solve-q-458', 'solution', qid='q-458', slides=[
    S('Method 1 · The math way: one letter',
      L("p, q and r are consecutive even numbers, and zero is smaller than p, which is smaller than q, which is smaller than "
        "r. What is r squared minus p squared, over two q?", pt('stem', 'p, q and r', 'hl', 10.0), voice='calm', pause=0.5),
      L("So three consecutive even numbers, and an expression. [short pause] We'll solve it two ways, with one letter, and "
        "then plugging in numbers.", pt('stem', 'three consecutive even numbers')),
      L("[short pause] Let's start with one letter, the middle one, q. Consecutive even numbers go up by two, so p is q "
        "minus two, and r is q plus two.", show(f1, 'p is q minus two'), show(f5, 'go up by two')),
      L("Now the top, r squared minus p squared. That's the third shortcut formula, r minus p, times r plus p.",
        show(f2, 'the third shortcut formula')),
      L("r minus p is q plus two, minus q minus two, four. And r plus p is q plus two plus q minus two, two q.",
        show(f3, 'r minus p is')),
      L("So the top is four times two q, and over two q, that's four. Choice number four is our answer.",
        show(f4, 'four times two q'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Now careful, two is the trap. It comes from a gap of one, but these are even numbers, and the gap is two.",
        mk('cross', 'choice 2', 'two is the trap'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in the smallest legal numbers. Bigger than zero, even and in a row, so two, four "
        "and six.", show(g1, 'two, four and six')),
      L("Six squared is thirty-six, two squared is four, and thirty-six minus four is thirty-two. Two times the middle, two "
        "times four, is eight. Thirty-two over eight is four. Choice number four. [pause] Okay. I'll see you in the next "
        "question.", show(g2, 'Six squared is thirty-six'), mk('tick', 'choice 4', 'Choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-459 (Q4)
# NEW: the minus between two fractions - work out each fraction first; the trap 0.  REMINDER: plugging in 1, 2, 3, 4;
# the differences with their signs (lesson).
h1 = I('h1', '$p=1,\\ q=2,\\ r=3,\\ s=4$', hand='p = 1,   q = 2,   r = 3,   s = 4')
h2 = I('h2', '$\\frac{3-1}{4-3}=\\frac{2}{1}=2$', hand='{3 − 1/4 − 3} = {2/1} = 2')
h3 = I('h3', '$\\frac{2-4}{3-2}=\\frac{-2}{1}=-2$', hand='{2 − 4/3 − 2} = {−2/1} = −2')
h4 = I('h4', '$2-(-2)=\\hl{a}{4}$', hand='2 − (−2) = \\hl{a}{4}')
h5 = I('h5', 'Each fraction first, then the minus', size=28, col=1)
k1 = I('k1', '$r-p=2\\qquad s-r=1$', hand='r − p = 2        s − r = 1')
k2 = I('k2', '$q-s=-2\\qquad r-q=1$', hand='q − s = −2        r − q = 1')
k3 = I('k3', '$\\frac21-\\frac{-2}{1}=2+2=\\hl{a}{4}$', hand='{2/1} − {−2/1} = 2 + 2 = \\hl{a}{4}')
video('solve-q-459', 'solution', qid='q-459', slides=[
    S('Method 1 · Plugging in numbers',
      L("p, q, r and s are consecutive integers, and p is smaller than q, which is smaller than r, which is smaller than s. "
        "What is r minus p, over s minus r, minus q minus s, over r minus q?", pt('stem', 'p, q, r and s', 'hl', 11.0), voice='calm', pause=0.5),
      L("So four numbers in a row, and two fractions of differences. [short pause] We'll solve it two ways, plugging in "
        "numbers, and then reading the differences.", pt('stem', 'four numbers in a row')),
      L("[short pause] Let's start by plugging in the smallest numbers, one, two, three and four.", show(h1, 'one, two, three and four')),
      L("The first fraction. Three minus one is two, and four minus three is one, so two over one, two.", show(h2, 'Three minus one is two')),
      L("The second fraction. Two minus four is negative two, and three minus two is one, so negative two.", show(h3, 'Two minus four')),
      L("Now careful with the minus between the fractions. Work out each fraction first, and only then subtract. Two minus "
        "negative two is two plus two, four. Choice number four is our answer.", show(h5, 'Work out each fraction first'),
        show(h4, 'Two minus negative two'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Got zero? That's the trap, the minus of the second fraction got lost.", mk('cross', 'choice 3', "That's the trap"))),
    S('Method 2 · The math way',
      L("[pause] Another way is to read the differences, with their signs. r minus p, bigger minus smaller, two steps, so "
        "two. s minus r, one.", show(k1, 'r minus p')),
      L("q minus s, smaller minus bigger, two steps back, negative two. r minus q, one.", show(k2, 'q minus s')),
      L("So two over one, minus negative two over one. Two plus two, four. Choice number four. [pause] Okay. I'll see you in "
        "the next question.", show(k3, 'So two over one'), mk('tick', 'choice 4', 'Choice number four'))),
])

# ------------------------------------------------------------------------------------------------ r26-t16-consecutive-sums (lesson)
# NEW: counting only the evens (or odds) in a range - steps of two, plus one (4 to 20 -> 9; 3 to 11 -> 5); squares of
# neighbors b^2 - a^2 = a + b (why; 5 and 4, 8 and 7; non-example 6 and 4).  REMINDER: last - first + 1 (topic 15),
# the third shortcut formula (topic 4).
m1 = I('m1', '$3$ to $10$: $\\ 10-3+1=8$', size=40, hand='3 to 10 :    10 − 3 + 1 = 8')
m2 = I('m2', 'Evens $4$ to $20$: $\\ \\frac{20-4}{2}+1=9$', size=40, hand='Evens 4 to 20 :    {20 − 4/2} + 1 = 9')
m3 = I('m3', 'Odds $3$ to $11$: $\\ \\frac{11-3}{2}+1=5$', size=40, hand='Odds 3 to 11 :    {11 − 3/2} + 1 = 5')
m4 = I('m4', '$3,\\ 5,\\ 7,\\ 9,\\ 11$', size=40, hand='3,  5,  7,  9,  11')
q1 = I('q1', '$b^2-a^2=(b-a)(b+a)$', size=44, hand='b^2 − a^2 = (b − a)(b + a)')
q2 = I('q2', 'Neighbors: $\\ b-a=1$ $\\ \\to\\ b^2-a^2=a+b$', size=40, hand='Neighbors :   b − a = 1   →   b^2 − a^2 = a + b')
q3 = I('q3', '$5^2-4^2=25-16=9=4+5$', size=40, hand='5^2 − 4^2 = 25 − 16 = 9 = 4 + 5')
q4 = I('q4', '$8^2-7^2=64-49=15=7+8$', size=40, hand='8^2 − 7^2 = 64 − 49 = 15 = 7 + 8')
q5 = I('q5', 'Not neighbors: $\\ 6^2-4^2=20\\ne10$', size=38, hand='Not neighbors :    6^2 − 4^2 = 20 ≠ 10')
video('r26-t16-consecutive-sums', 'lesson', slides=[
    S('Sums of Consecutive Integers',
      L("Welcome back. Two short tools for numbers in a row, before the next two questions. Those questions teach the main "
        "rule, count times middle.")),
    S('Counting in a range',
      L("Remember, how many integers are there from three to ten? The last minus the first, plus one, because both ends "
        "count. Ten minus three is seven, and plus one is eight.", show(m1, 'from three to ten')),
      L("Now only the even numbers, from four to twenty. They go in steps of two. So count the steps, twenty minus four is sixteen, sixteen over two is eight steps, and plus one is nine even numbers.", show(m2, 'only the even numbers')),
      L("Odd numbers the same way. From three to eleven, eleven minus three is eight, eight over two is four steps, and plus one is five. And really, three, five, seven, nine, eleven.", show(m3, 'From three to eleven'), show(m4, 'And really'))),
    S('Squares of neighbors',
      L("Second tool. b squared minus a squared is the third shortcut formula, b minus a, times b plus a.", show(q1, 'the third shortcut formula')),
      L("And if a and b are neighbors, with b bigger, then b minus a is one. So b squared minus a squared is just a plus b.",
        show(q2, 'if a and b are neighbors')),
      L("Let's see it in numbers. Five squared is twenty-five and four squared is sixteen. Twenty-five minus sixteen is nine, and four plus five is nine. Eight squared is sixty-four and seven squared is forty-nine. Sixty-four minus forty-nine is fifteen, and seven plus eight is fifteen.",
        show(q3, 'Five squared is twenty-five'), show(q4, 'Eight squared is sixty-four')),
      L("But only for neighbors. Six squared is thirty-six and four squared is sixteen. Thirty-six minus sixteen is twenty, not six plus four, which is ten. "
        "[pause] Okay. I'll see you in the next video.", show(q5, 'only for neighbors'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t16-02 (Q5)
# NEW: sum of numbers in a row = count x middle (why: the numbers pair up around the middle; 4 + 5 + 6, 10 to 14);
# the trap 13 (the middle, not the largest).  REMINDER: one letter around the middle (lesson).
# Codex clarity pass 2026-10-12: narration AND graphics live here, not only in the HTML.
# See codex-clarity-handoff-2026-10-12.json in this directory for changed IDs and checks.
n0 = I('n0', 'From averages: sum $=$ count $\\times$ average', size=26, col=1)
n0b = I('n0b', 'Consecutive, odd count: average $=$ middle', size=26, col=1)
n1 = I('n1', 'Sum $=$ count $\\times$ middle', size=30, col=1)
n2 = I('n2', '$4+5+6=15=3\\cdot5$', size=32, col=1, hand='4 + 5 + 6 = 15 = 3·5')
n3 = I('n3', '$10+\\ldots+14=60=5\\cdot12$', size=32, col=1, hand='10 + 11 + 12 + 13 + 14 = 60 = 5·12')
n4 = I('n4', 'Middle: $\\ \\frac{91}{7}=\\hl{m}{13}$', hand='Middle :    {91/7} = \\hl{m}{13}')
n5 = I('n5', '$10,\\ 11,\\ 12,\\ \\hl{m}{13},\\ 14,\\ 15,\\ \\hl{l}{16}$', hand='10,  11,  12,  \\hl{m}{13},  14,  15,  \\hl{l}{16}')
n6 = I('n6', '$13$ is the middle, not the largest ✗', size=28, col=1, hand='13  is the middle,  not the largest   ✗')
o1 = I('o1', '$(b-3)+\\ldots+(b+3)=7b$', hand='b − 3  up to  b + 3 :    sum = 7b')
o2 = I('o2', '$7b=91$, $\\ b=13$, $\\ b+3=\\hl{l}{16}$', hand='7b = 91,   b = 13,   b + 3 = \\hl{l}{16}')
video('solve-q-r26-t16-02', 'solution', qid='q-r26-t16-02', slides=[
    S('Method 1 · Understanding: the middle',
      L("The sum of seven consecutive integers is ninety-one. What is the largest of them?", pt('stem', 'The sum', 'hl', 5.0), voice='calm', pause=0.5),
      L("So seven numbers in a row, and all we know is their sum. [short pause] We'll solve it two ways, with count times "
        "middle, and then with one letter.", pt('stem: ask', 'all we know is their sum')),
      L("Remember what we learned in averages. The average is the sum divided by the number of values. "
        "So the sum is the number of values times their average. Here we have seven numbers, so their sum is seven times their average.",
        show(n0, 'The average is the sum')),
      L("And why is the average the middle number here? The numbers are consecutive, so the gaps are equal. "
        "The number one below the middle pairs with the number one above it. Together they make twice the middle. "
        "The same happens two below and two above, and three below and three above. "
        "So the average is the middle number, and we can use count times middle.",
        show(n0b, 'The numbers are consecutive'), pt('n0b', 'So the average is the middle')),
      L("Here's the rule for an odd count of consecutive integers. The sum is the count times the middle number. "
        "Seven is an odd count, so there is one actual middle number, the fourth.",
        show(n1, 'the count times the middle')),
      L("Let's see it in numbers. Four plus five plus six is fifteen, and that's three times the middle, five. Ten to "
        "fourteen, five numbers, add up to sixty, five times the middle, twelve.", show(n2, 'Four plus five plus six'), show(n3, 'Ten to fourteen')),
      L("So here the middle is the sum over the count, ninety-one over seven, thirteen. That's the fourth number, with three "
        "below it and three above it, ten up to sixteen.", show(n4, 'ninety-one over seven'), show(n5, 'three below it')),
      L("The largest is sixteen, so choice number three is our answer.", mk('circle', 'n5: l', 'The largest is sixteen'),
        mk('tick', 'choice 3', 'choice number three is our answer')),
      L("Now careful, thirteen is the trap. It's the middle, not the largest.", show(n6, 'thirteen is the trap'), mk('cross', 'choice 1', "It's the middle"))),
    S('Method 2 · The math way: one letter',
      L("[pause] Another way is one letter, around the middle, b. The seven numbers are b minus three up to b plus three. "
        "The minuses and the pluses cancel, so the sum is seven b.", show(o1, 'b minus three up to')),
      L("Seven b is ninety-one, so b is ninety-one over seven, thirteen. And the largest is b plus three, sixteen. Choice "
        "number three. [pause] Okay. I'll see you in the next question.", show(o2, 'Seven b is ninety-one'),
        mk('tick', 'choice 3', 'Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t16-03 (Q6)
# NEW: the sum of four in a row is 4a + 6 = 2(2a + 3): even, and 4(a + 1) + 2 never divides by 4 (1..4 = 10, 2..5 =
# 14); odd count -> the sum divides by the count, even count -> never (4 + 5 + 6 = 15).  REMINDER: one letter (lesson);
# one plug-in that kills three choices (topic 15).
r1 = I('r1', '$a+(a+1)+(a+2)+(a+3)=4a+6$', size=32, hand='a + (a+1) + (a+2) + (a+3) = 4a + 6')
r2 = I('r2', '$4a+6=2(2a+3)$: $\\ $even', size=32, hand='4a + 6 = 2(2a + 3) :    even')
r3 = I('r3', '$4a+6=4(a+1)+2$: $\\ $leaves $2$ by $4$', size=32, hand='4a + 6 = 4(a + 1) + 2 :    leaves 2 by 4')
r4 = I('r4', '$1+2+3+4=10\\qquad 2+3+4+5=14$', size=30, col=1, hand='1 + 2 + 3 + 4 = 10        2 + 3 + 4 + 5 = 14')
r5 = I('r5', 'Odd count: divides by the count. Even count: never', size=26, col=1)
r6 = I('r6', '$4+5+6=15=3\\cdot5$ ✓', size=30, col=1, hand='4 + 5 + 6 = 15 = 3·5   ✓')
s1 = I('s1', '$1+2+3+4=\\hl{t}{10}$', hand='1 + 2 + 3 + 4 = \\hl{t}{10}')
s2 = I('s2', 'by $4$? ✗ $\\quad$ odd? ✗ $\\quad$ by $3$? ✗', hand='by 4 ?  ✗      odd ?  ✗      by 3 ?  ✗')
video('solve-q-r26-t16-03', 'solution', qid='q-r26-t16-03', slides=[
    S('Method 1 · The math way: one letter',
      L("The sum of four consecutive integers is always:", pt('stem', 'The sum', 'hl', 3.0), voice='calm', pause=0.5),
      L("So any four numbers in a row, and what's always true about their sum. [short pause] We'll solve it two ways, with "
        "one letter, and then plugging in numbers.", pt('stem', 'what\'s always true')),
      L("[short pause] Let's start with one letter. Four in a row are a, a plus one, a plus two and a plus three. Add them, "
        "four a, and one plus two plus three is six. Four a plus six.", show(r1, 'Four in a row are')),
      L("Take out a two, two times, in brackets, two a plus three. So the sum is always even, and choice number two, odd, is "
        "out.", show(r2, 'Take out a two'), mk('cross', 'choice 2', 'is out')),
      L("And four? Four a plus six is four a plus four, plus two, four times a plus one, plus two. So it always leaves two "
        "when divided by four, and never divides by four. Choice number one is out.", show(r3, 'four a plus four'),
        mk('cross', 'choice 1', 'Choice number one is out')),
      L("Let's see it in numbers. One to four is ten, and two to five is fourteen. Both are even, and they don't divide by four. So "
        "even, but not divisible by four, choice number three is our answer.", show(r4, 'One to four is ten'),
        mk('tick', 'choice 3', 'choice number three is our answer')),
      L("And here's the pattern behind it. With an odd count in a row, the sum divides by the count, like four plus five plus "
        "six, fifteen, three fives. With an even count, it never does.", show(r5, 'the pattern behind it'), show(r6, 'like four plus five'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers, one, two, three and four. They add up to ten.", show(s1, 'They add up to ten')),
      L("Ten doesn't divide by four, so choice number one is out. Ten isn't odd, so choice number two is out. Ten doesn't "
        "divide by three, so choice number four is out. Three are out, so choice number three. [pause] Okay. I'll see you in "
        "the next question.", show(s2, "Ten doesn't divide by four"), mk('cross', 'choice 1', 'choice number one is out'),
        mk('cross', 'choice 2', 'choice number two is out'), mk('cross', 'choice 4', 'choice number four is out'), mk('tick', 'choice 3', 'so choice number three'))),
])

# ------------------------------------------------------------------------------------------------ parity (lesson)
# NEW: count the odd terms in a sum; one even factor makes a product even (and odd only if every factor is odd);
# division rules (four cases, two examples each); powers keep parity; one plug-in per parity case for + and x, three
# close plug-ins for division.  REMINDER: even, odd and zero (topic 1), odd + odd = even (topic 14), odd x odd = odd
# (topic 15), one failing example knocks out "always" (topic 15).
p1 = I('p1', 'Even: divisible by $2$ $\\quad 572,\\ \\ 9150,\\ \\ 0$', size=38, hand='Even :   572,   9150,   0')
p2 = I('p2', '$8+12=20\\quad 7+11=18\\quad 8+7=15$', size=38, hand='8 + 12 = 20      7 + 11 = 18      8 + 7 = 15')
p3 = I('p3', '$8+\\hl{o}{5}-2+\\hl{o}{11}+\\hl{o}{3}=25$: $\\ $three odds $\\to$ odd', size=34, hand='8 + 5 − 2 + 11 + 3 = 25 :    three odds  →  odd')
p4 = I('p4', '$4+7-10+9=10$: $\\ $two odds $\\to$ even', size=34, hand='4 + 7 − 10 + 9 = 10 :    two odds  →  even')
p5 = I('p5', 'One even factor: even $\\quad 4\\cdot15=60\\quad 9\\cdot8=72$', size=34, hand='4·15 = 60      9·8 = 72')
p6 = I('p6', 'Odd only if every factor is odd $\\quad 7\\cdot3=21$', size=34, hand='7·3 = 21')
p7 = I('p7', '$2(x+7)$: even $\\quad 2x+7$: odd $\\quad x=1$: $\\ 16,\\ 9$', size=34, hand='2(x+7) : even      2x + 7 : odd      x = 1 :   16,   9')
d1 = I('d1', 'Odd $\\div$ odd: $\\ \\frac{21}{7}=3$ or $\\frac73$', size=36, hand='Odd ÷ odd :   {21/7} = 3   or   {7/3}')
d2 = I('d2', 'Even $\\div$ odd: $\\ \\frac{12}{3}=4$ or $\\frac83$', size=36, hand='Even ÷ odd :   {12/3} = 4   or   {8/3}')
d3 = I('d3', 'Odd $\\div$ even: $\\ \\frac72,\\ \\frac94$ $\\ $always a fraction', size=36, hand='Odd ÷ even :   {7/2},  {9/4}    always a fraction')
d4 = I('d4', 'Even $\\div$ even: $\\ \\frac{18}{6}=3,\\ \\frac{12}{2}=6,\\ \\frac64$', size=36, hand='Even ÷ even :   {18/6} = 3,   {12/2} = 6,   {6/4}')
w1 = I('w1', '$2^2=4,\\ 2^3=8\\qquad 3^2=9,\\ 3^3=27$', size=38, hand='2^2 = 4,   2^3 = 8        3^2 = 9,   3^3 = 27')
w2 = I('w2', 'Powers keep parity: you may drop them', size=36)
w3 = I('w3', '$+,\\ \\times$: one plug-in per case $\\quad 2\\cdot3=6$', size=34, hand='+,  × :   one plug-in per case      2·3 = 6')
w4 = I('w4', '$\\div$: test different outcomes $\\quad \\frac62=3,\\ \\frac82=4,\\ \\frac{10}{4}$', size=30, hand='÷ :   test different outcomes      {6/2} = 3,   {8/2} = 4,   {10/4}')
video('parity', 'lesson', slides=[
    S('Even & Odd',
      L("Welcome back. Now even and odd, and how each operation decides whether the result is even or odd.")),
    S('Adding',
      L("Remember, an even number is an integer that divides by two, like five seventy-two, or nine thousand one fifty, and "
        "zero is even too. An odd number is an integer that isn't even.", show(p1, 'five seventy-two')),
      L("And remember adding. Even plus even is even, eight plus twelve is twenty. Odd plus odd is even, seven plus eleven is "
        "eighteen. Even plus odd is odd, eight plus seven is fifteen. Subtracting works the same.", show(p2, 'eight plus twelve')),
      L("So in a long sum, the even numbers don't matter at all, and only the odd ones count. Eight plus five minus two plus "
        "eleven plus three. The odd ones are five, eleven and three, three of them. Two of them pair up into an even, and "
        "one is left over, so the total is odd. And really, it's twenty-five.", show(p3, 'Eight plus five minus two')),
      L("Four plus seven minus ten plus nine. Only two odd ones, seven and nine, and they pair up, so the total is even. "
        "It's ten.", show(p4, 'Four plus seven minus ten'))),
    S('Multiplying',
      L("Multiplying. One even factor is enough to make the whole product even, because it brings a two in. Four times "
        "fifteen is sixty, and nine times eight is seventy-two.", show(p5, 'One even factor')),
      L("So a product is odd only when every factor is odd. Seven times three is twenty-one, odd.", show(p6, 'every factor is odd')),
      L("Careful with brackets. Two times, in brackets, x plus seven, is even, because the two multiplies everything. But "
        "two x plus seven is odd. With x one, the first is sixteen, and the second is nine.", show(p7, 'Careful with brackets'))),
    S('Dividing',
      L("Dividing is different, because you can almost always get a fraction. Odd over odd is odd, or a fraction. Twenty-one "
        "over seven is three, and seven over three is a fraction.", show(d1, 'Odd over odd')),
      L("Even over odd is even, or a fraction. Twelve over three is four, and eight over three is a fraction.", show(d2, 'Even over odd')),
      L("Odd over even is always a fraction. Seven over two, nine over four. Why? An even number has a two inside, and an "
        "odd number has no two to cancel it.", show(d3, 'Odd over even')),
      L("And even over even can be anything. Eighteen over six is three, odd. Twelve over two is six, even. Six over four "
        "is a fraction.", show(d4, 'even over even'))),
    S('Powers and plugging in',
      L("Positive whole-number powers don't change parity. Two squared is four, two cubed is eight, even. Three squared is nine, three cubed is "
        "twenty-seven, odd. A power just multiplies the same number again and again. So in a parity question, you may drop "
        "the powers.", show(w1, 'Two squared is four'), show(w2, 'you may drop')),
      L("And plugging in. For adding and multiplying, the parity of the result depends only on the parities you put in. So "
        "one plug-in for each case settles it. Two times three is six, and even times odd is always even.", show(w3, 'one plug-in for each case')),
      L("For dividing, test different possible outcomes, not just three nearby numbers. Six over two is three, odd. "
        "Eight over two is four, even. And ten over four is a fraction, not a whole number. "
        "Three examples help us see what can happen, but three matches do not prove always. "
        "One example that fails knocks out an always claim. To establish always, explain why the result holds for every allowed value. "
        "[pause] Okay. I'll see you in the next video.", show(w4, 'test different possible outcomes'))),
])

# ------------------------------------------------------------------------------------------------ q-460 (Q7)
# NEW: drop the powers in a parity question (the lesson's rule used); "m + n odd" means one is even and one is odd.
# REMINDER: count the odd terms, one plug-in per case (parity lesson).
t1 = I('t1', '$m+n$ odd: $\\ $one even, one odd', size=28, col=1, hand='m + n  odd :   one even,  one odd')
t2 = I('t2', 'Drop the powers: $\\ m+n+9+4n$', hand='Drop the powers :    m + n + 9 + 4n')
t3 = I('t3', 'odd $+$ odd $+$ even $=$ \\hl{e}{even}', hand='odd + odd + even = \\hl{e}{even}')
u1 = I('u1', '$m=1,\\ n=2$: $\\ 1+2+9+8=20$', hand='m = 1,  n = 2 :    1 + 2 + 9 + 8 = 20')
u2 = I('u2', '$m=2,\\ n=1$: $\\ 2+1+9+4=16$', hand='m = 2,  n = 1 :    2 + 1 + 9 + 4 = 16')
u3 = I('u3', 'Both cases even', size=28, col=1)
video('solve-q-460', 'solution', qid='q-460', slides=[
    S('Method 1 · Understanding',
      L("m and n are positive integers, and m plus n is odd. Which of the following is true about the expression m to the "
        "power of n, plus n to the power of m, plus nine, plus four n?", pt('stem', 'm and n are', 'hl', 10.0), voice='calm', pause=0.5),
      L("So m plus n is odd, and that tells us something. Odd plus odd is even, and even plus even is even. So one of them is "
        "even and the other is odd. [short pause] We'll solve it two ways, dropping the powers, and then plugging in both "
        "cases.", pt('stem', 'm plus n is odd'), show(t1, 'one of them is even')),
      L("[short pause] Let's start by dropping the powers. Remember, a power doesn't change parity, so in a parity question "
        "I may drop it. What's left is m plus n, plus nine, plus four n.", show(t2, 'dropping the powers')),
      L("m plus n is odd, it's given. Nine is odd. Four n is even, because of the four. And the evens don't matter, so odd "
        "plus odd, even. It's always even, choice number one is our answer.", show(t3, 'm plus n is odd, it'),
        mk('tick', 'choice 1', 'choice number one is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in. There are only two cases, m odd and n even, or the other way round. m is one and "
        "n is two. One squared is one, and two to the power of one is two. One plus two plus nine plus eight is twenty, even.", show(u1, 'm is one and n is two')),
      L("Now swapped, m is two and n is one. Two to the power of one is two, and one squared is one. Two plus one plus nine plus four is sixteen, even again. Both cases are even, so it's always even. Choice number one. [pause] Okay. I'll see you in "
        "the next question.", show(u2, 'Now swapped'), show(u3, 'Both cases are even'), mk('tick', 'choice 1', 'Choice number one'))),
])

# ------------------------------------------------------------------------------------------------ q-461 (Q8)
# NEW: in a fraction, cancel first - the two inside 6 cancels with a two inside b (b = 2k) - and then odd over even is
# always a fraction; the trap "even over even = anything".  REMINDER: division rules, three close plug-ins (parity
# lesson).
v1 = I('v1', 'Even $\\div$ even: anything? A trap', size=28, col=1)
v2 = I('v2', '$b=2k$: $\\ \\frac{6a}{4k^2}=\\frac{3a}{2k^2}$', hand='b = 2k :    {6a/4k^2} = {3a/2k^2}')
v3 = I('v3', 'odd $\\div$ even: always a fraction', hand='odd ÷ even :   always a fraction')
v4 = I('v4', 'Cancel first, then judge', size=28, col=1)
v5 = I('v5', '$a=1,b=2$: $\\frac64$ $\\quad a=3,b=2$: $\\frac{18}{4}$ $\\quad a=3,b=4$: $\\frac{18}{16}$', size=28,
       hand='a=1, b=2 :  {6/4}      a=3, b=2 :  {18/4}      a=3, b=4 :  {18/16}')
video('solve-q-461', 'solution', qid='q-461', slides=[
    S('Method 1 · The math way',
      L("a and b are integers. a is odd, and b is even and not zero. Which of the following is the most precise "
        "description of six a over b squared?", pt('stem', 'a and b are', 'hl', 8.0), voice='calm', pause=0.5),
      L("Division and parity, and a trap. Six a on top is even, and b squared at the bottom is even. Even over even, and the "
        "rule says it can be anything. So choice number one? That's the trap. [short pause] We'll solve it two ways, "
        "cancelling first, and then plugging in three times.", show(v1, 'Even over even'), pt('choice 1', 'So choice number one')),
      L("[short pause] Let's start by cancelling. b is even, so b is two k, for some integer k. Two k squared is four k "
        "squared. Six over four, cancel a two, and it's three a over two k squared.", show(v2, 'b is two k')),
      L("Now three a is odd times odd, odd. And two k squared is even. Odd over even is always a fraction, because the odd "
        "top has no two to cancel the bottom's two. Choice number two is our answer.", show(v3, 'Odd over even'),
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("So in a fraction, cancel first, and only then judge. The two inside the six cancelled with a two hiding in b.",
        show(v4, 'cancel first'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in. It's division, so three plug-ins, close together. a is one and b is two, six over "
        "four. A fraction. a is three and b is two, eighteen over four, a fraction. a is three and b is four, eighteen over "
        "sixteen, a fraction.", show(v5, 'a is one and b is two')),
      L("Each example gives a fraction, but those examples alone do not prove always. "
        "What makes it certain? b is even and nonzero, so b is two k with k nonzero. "
        "After cancelling a two, the fraction is three a over two k squared. "
        "a is odd, so the top is odd and cannot cancel the two on the bottom. "
        "That applies to every allowed pair, so it is always a fraction, choice number two. "
        "[pause] Okay. I'll see you in the next question.",
        mk('tick', 'choice 2', 'choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-462 (Q9)
# NEW: an even difference means the same parity (both even or both odd); factor b^2 + ab = b(b + a); choose odd numbers
# to plug in (two evens make every choice even - the tie).  REMINDER: one plug-in per case (parity lesson).
x1 = I('x1', '$a-b=6$ even: $\\ $same parity', size=28, col=1, hand='a − b = 6  even :   same parity')
x2 = I('x2', '$b^2+ab=b(b+a)$', hand='b^2 + ab = b(b + a)')
x3 = I('x3', '$a+b$: even + even or odd + odd $=$ \\hl{e}{even}', size=32, hand='a + b :   even + even  or  odd + odd  =  \\hl{e}{even}')
x4 = I('x4', '$8-2=6\\qquad 9-3=6$', size=30, col=1, hand='8 − 2 = 6        9 − 3 = 6')
y1 = I('y1', '$a=7,\\ b=1$ $\\ $(odd: evens make all even)', size=30, hand='a = 7,  b = 1     (odd: evens make all even)')
y2 = I('y2', '(1) $49+1+5=55$ ✗ $\\quad$ (2) $1+7=8$ ✓', size=30, hand='(1)   49 + 1 + 5 = 55  ✗      (2)   1 + 7 = 8  ✓')
y3 = I('y3', '(3) $42-1=41$ ✗ $\\quad$ (4) $5\\cdot49+4$: odd ✗', size=30, hand='(3)   42 − 1 = 41  ✗      (4)   5·49 + 4 :  odd  ✗')
video('solve-q-462', 'solution', qid='q-462', slides=[
    S('Method 1 · Understanding',
      L("a and b are integers. Given: a minus b is equal to six. Which of the following expressions is necessarily even?",
        pt('stem', 'a and b are', 'hl', 6.0), voice='calm', pause=0.5),
      L("So we know the difference, six, and we look for the expression that's always even. [short pause] We'll solve it "
        "two ways, with the parities, and then plugging in numbers.", pt('stem: g1', 'the difference, six')),
      L("[short pause] Let's start with the parities. Six is even, and when is a difference even? When both are even, like "
        "eight minus two, or both are odd, like nine minus three. So a and b have the same parity.",
        show(x4, 'eight minus two'), show(x1, 'the same parity')),
      L("Now choice number two, b squared plus a b. Take out b, and it's b times, in brackets, b plus a. And b plus a is "
        "even plus even or odd plus odd, so it's always even. A product with an even factor is even, so choice number two is "
        "our answer.", show(x2, 'Take out b'), show(x3, 'b plus a is'), mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in. Which numbers? If I take two even numbers, every choice comes out even, and they "
        "won't help. So two odd numbers with a difference of six, a is seven and b is one.", show(y1, 'a is seven and b is one')),
      L("Choice number one, forty-nine plus one plus five is fifty-five, odd. Out. Choice number two, one plus seven is "
        "eight, even. Choice number three, forty-two minus one is forty-one, odd. Out. Choice number four, two forty-five "
        "plus four is two forty-nine, odd. Out.", show(y2, 'Choice number one, forty-nine'),
        mk('cross', 'choice 1', 'fifty-five, odd. Out'), show(y3, 'Choice number three'), mk('cross', 'choice 3', 'forty-one, odd. Out'),
        mk('cross', 'choice 4', 'forty-nine, odd. Out')),
      L("Three are out, so choice number two. [pause] Okay. I'll see you in the next question.", mk('tick', 'choice 2', 'so choice number two'))),
])

# ------------------------------------------------------------------------------------------------ consecutive-products (lesson)
# NEW: four in a row divide by 24 (why; 1·2·3·4, 2·3·4·5); products of evens - two evens by 4, two consecutive evens by 8
# (why; 2·4, 6·8, 10·12); count the twos (m^2(n + 1)/8 whole, m(n + 1)/8 not); hidden products x^2 - 1 (x odd -> by 8).
# The smallest-case trick is taught in q-r26-t16-04, where it is first used.  REMINDER: two in a row by 2, three by 6,
# x^3 - x (topic 15).
c1 = I('c1', 'Two in a row: $2\\quad$ Three in a row: $6$', size=40, hand='Two in a row :  2      Three in a row :  6')
c2 = I('c2', 'Four in a row: $\\ 8\\cdot3=24$', size=40, hand='Four in a row :    8·3 = 24')
c3 = I('c3', '$1\\cdot2\\cdot3\\cdot4=24\\qquad 2\\cdot3\\cdot4\\cdot5=120=5\\cdot24$', size=36, hand='1·2·3·4 = 24        2·3·4·5 = 120 = 5·24')
c4 = I('c4', 'Two evens: $\\ (2a)(2b)=4ab$ $\\quad 2\\cdot6=12\\quad 4\\cdot10=40$', size=34, hand='(2a)(2b) = 4ab       2·6 = 12      4·10 = 40')
c5 = I('c5', 'Two consecutive evens: by $8$ $\\quad 2\\cdot4=8\\quad 6\\cdot8=48\\quad 10\\cdot12=120$', size=32,
       hand='2·4 = 8      6·8 = 48      10·12 = 120')
c6 = I('c6', '$m$ even, $n$ odd: $\\ \\frac{m^2(n+1)}{8}$: $\\ 2+1=3$ twos ✓', size=34, hand='{m^2(n+1)/8} :    2 + 1 = 3 twos   ✓')
c7 = I('c7', '$m=2,n=1$: $\\frac{4\\cdot2}{8}=1\\quad m=2,n=3$: $\\frac{4\\cdot4}{8}=2$', size=32, hand='m=2, n=1 :  {4·2/8} = 1      m=2, n=3 :  {4·4/8} = 2')
c8 = I('c8', '$\\frac{m(n+1)}{8}$: $\\ $two twos ✗ $\\quad \\frac{2\\cdot2}{8}=\\frac12$', size=34, hand='{m(n+1)/8} :   two twos  ✗      {2·2/8} = {1/2}')
c9 = I('c9', '$x^2-1=(x-1)(x+1)$ $\\quad x=5$: $\\ 24\\quad x=7$: $\\ 48$', size=34, hand='x^2 − 1 = (x−1)(x+1)      x = 5 :  24      x = 7 :  48')
video('consecutive-products', 'lesson', slides=[
    S('Products of Consecutive Integers',
      L("Welcome back. Products of numbers in a row, and of even numbers, follow some very handy rules. Let's build them.")),
    S('Four in a row',
      L("Remember, two numbers in a row always divide by two, and three in a row by six.", show(c1, 'two numbers in a row')),
      L("Four in a row. One of them divides by four, and another one is even, so that's eight. And one of them divides by "
        "three. Eight and three share nothing, so the product divides by eight times three, twenty-four.", show(c2, 'Four in a row')),
      L("Let's see it in numbers. One times two times three times four is twenty-four. Two times three times four times five "
        "is a hundred twenty, five twenty-fours.", show(c3, 'One times two times three'))),
    S('Even products',
      L("Now even numbers. Each even number is two times something, so two evens together are four times something. Two "
        "times six is twelve, and four times ten is forty, both divide by four.", show(c4, 'Each even number is two times')),
      L("Two consecutive even numbers are even better. One of them always divides by four, and the other by two, so the "
        "product divides by eight. Two times four is eight, six times eight is forty-eight, and ten times twelve is a hundred "
        "twenty, fifteen eights.", show(c5, 'Two consecutive even numbers'))),
    S('Count the twos',
      L("Is a fraction a whole number? Count the twos. m is even and n is odd. m squared over eight, times n plus one. m is "
        "even, so m squared has at least two twos. n is odd, so n plus one is even, one more two. Three twos on top, and "
        "eight is two times two times two. It cancels, always whole.", show(c6, 'Count the twos')),
      L("Let's check. m is two and n is one, four times two over eight is one. m is two and n is three, four times four over "
        "eight is two.", show(c7, 'm is two and n is one')),
      L("But m times n plus one, over eight, has only two twos for sure. With m two and n one, two times two over eight is "
        "a half. Not whole.", show(c8, 'only two twos for sure'))),
    S('Hidden products',
      L("On the exam, the products hide inside expressions. x squared minus one is x minus one, times x plus one, the "
        "neighbors of x. If x is odd, they're two consecutive even numbers, so x squared minus one divides by eight. x is "
        "five, twenty-five minus one is twenty-four. x is seven, forty-nine minus one is forty-eight.", show(c9, 'x squared minus one')),
      L("And x cubed minus x is three in a row, as you saw. You'll meet both in the next questions. [pause] Okay. I'll see "
        "you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ q-463 (Q10)
# NEW: 9n^2 - 1 = (3n - 1)(3n + 1), two consecutive evens when n is odd -> 8k -> over 4 is 2k.  REMINDER: three close
# plug-ins for division (parity lesson), consecutive evens divide by 8 (products lesson).
g1 = I('g1', '$n=1$: $\\ \\frac{9-1}{4}=\\frac84=2$', size=32, hand='n = 1 :    {9 − 1/4} = {8/4} = 2')
g2 = I('g2', '$n=3$: $\\ \\frac{81-1}{4}=\\frac{80}{4}=20$', size=32, hand='n = 3 :    {81 − 1/4} = {80/4} = 20')
g3 = I('g3', '$n=5$: $\\ \\frac{225-1}{4}=\\frac{224}{4}=56$', size=32, hand='n = 5 :    {225 − 1/4} = {224/4} = 56')
g4 = I('g4', 'Plug-ins point, the math proves', size=28, col=1)
h1 = I('h1', '$9n^2-1=(3n)^2-1^2=(3n-1)(3n+1)$', size=32, hand='9n^2 − 1 = (3n)^2 − 1^2 = (3n − 1)(3n + 1)')
h2 = I('h2', '$n$ odd: $\\ 3n$ odd $\\to$ two consecutive evens', size=30, hand='n odd :   3n odd   →   two consecutive evens')
h3 = I('h3', '$\\frac{8k}{4}=\\hl{e}{2k}$', hand='{8k/4} = \\hl{e}{2k}')
video('solve-q-463', 'solution', qid='q-463', slides=[
    S('Method 1 · Plugging in numbers',
      L("n is an odd number. Which of the following is the most precise description of nine n squared minus one, over "
        "four?", pt('stem', 'n is an odd', 'hl', 7.0), voice='calm', pause=0.5),
      L("A division with parity, and the choices are descriptions. [short pause] We'll solve it two ways, plugging in three "
        "times, and then with the shortcut formula.", pt('stem: ask', 'the choices are descriptions')),
      L("[short pause] Let's start by plugging in. It's a division, so three plug-ins, close together, and n has to be odd. "
        "n is one. Nine times one is nine, minus one is eight, and eight over four is two.", show(g1, 'n is one')),
      L("n is three. Nine times nine is eighty-one, minus one is eighty, and eighty over four is twenty.", show(g2, 'n is three'), voice='calm'),
      L("n is five. Nine times twenty-five is two twenty-five, minus one is two twenty-four, and over four "
        "is fifty-six.", show(g3, 'n is five'), voice='calm'),
      L("Two, twenty, fifty-six, even every time. That points to choice number one, always even. But plug-ins that work "
        "don't prove always, so let's see why.", show(g4, "plug-ins that work"), pt('choice 1', 'That points to choice number one'))),
    S('Method 2 · The math way: shortcut formula',
      L("[pause] Nine n squared is three n, squared, and one is one squared. So it's the third shortcut formula, three n "
        "minus one, times three n plus one.", show(h1, 'Nine n squared is three n')),
      L("n is odd, so three n is odd too. So three n minus one and three n plus one are the even numbers just before and "
        "just after it, two consecutive even numbers. And remember, two consecutive evens always divide by eight.", show(h2, 'n is odd, so three n')),
      L("So the top is eight k, and eight k over four is two k. Always even. Choice number one. [pause] Okay. I'll see you "
        "in the next question.", show(h3, 'eight k over four'), mk('tick', 'choice 1', 'Choice number one'))),
])

# ------------------------------------------------------------------------------------------------ q-464 (Q11)
# NEW: n - n^3 = -(n - 1)n(n + 1); a minus in front doesn't change divisibility; don't plug in n = 1 (it gives 0).
# REMINDER: three in a row divide by 6 (topic 15), three plug-ins, both parities (parity lesson).
i1 = I('i1', '$n=1$: $\\ 0$ $\\ $(divides by everything)', size=28, col=1, hand='n = 1 :   0    (divides by everything)')
i2 = I('i2', '$n=2$: $\\ \\frac{2-8}{3}=\\frac{-6}{3}=\\hl{a}{-2}$', size=32, hand='n = 2 :    {2 − 8/3} = {−6/3} = \\hl{a}{−2}')
i3 = I('i3', '$n=3$: $\\ \\frac{3-27}{3}=\\frac{-24}{3}=-8$', size=32, hand='n = 3 :    {3 − 27/3} = {−24/3} = −8')
i4 = I('i4', '$n=4$: $\\ \\frac{4-64}{3}=\\frac{-60}{3}=-20$', size=32, hand='n = 4 :    {4 − 64/3} = {−60/3} = −20')
i5 = I('i5', '$-2$: not by $4$ ✗ $\\quad$ never a fraction ✗ $\\quad$ never odd ✗', size=28, hand='−2 : not by 4 ✗     never a fraction ✗     never odd ✗')
j1 = I('j1', '$n-n^3=-(n^3-n)=-(n-1)\\,n\\,(n+1)$', size=32, hand='n − n^3 = −(n^3 − n) = −(n − 1) n (n + 1)')
j2 = I('j2', 'Three in a row: $\\ 6k$ $\\quad \\frac{-6k}{3}=\\hl{e}{-2k}$', size=32, hand='Three in a row :   6k      {−6k/3} = \\hl{e}{−2k}')
video('solve-q-464', 'solution', qid='q-464', slides=[
    S('Method 1 · Plugging in numbers',
      L("n is an integer. The expression n minus n cubed, over three, is always:", pt('stem', 'n is an integer', 'hl', 5.0), voice='calm', pause=0.5),
      L("So an expression with any integer n, and what's always true about it. [short pause] We'll solve it two ways, "
        "plugging in, and then factoring.", pt('stem', 'any integer n')),
      L("[short pause] Let's start by plugging in. Careful, not n is one. One minus one is zero, and zero divides by "
        "everything, so it can't rule anything out.", show(i1, 'not n is one')),
      L("n is two. Two cubed is eight, two minus eight is negative six, and over three is negative two. n is three. Three "
        "cubed is twenty-seven, three minus twenty-seven is negative twenty-four, and over three is negative eight.",
        show(i2, 'n is two'), show(i3, 'n is three')),
      L("Division, so a third one. n is four. Four cubed is sixty-four, four minus sixty-four is negative sixty, and over "
        "three is negative twenty.", show(i4, 'n is four')),
      L("Negative two doesn't divide by four, so choice number one is out. None of them is a fraction or odd, so choice "
        "numbers two and four are out. Choice number three, even.", show(i5, "Negative two doesn't divide"),
        mk('cross', 'choice 1', 'choice number one is out'), mk('cross', 'choice 2', 'choice numbers two'), mk('cross', 'choice 4', 'and four are out'),
        mk('tick', 'choice 3', 'Choice number three, even'))),
    S('Method 2 · The math way: three in a row',
      L("[pause] Another way, factoring. n minus n cubed is minus, in brackets, n cubed minus n. And n cubed minus n is n "
        "minus one, times n, times n plus one, three in a row.", show(j1, 'n minus n cubed is minus')),
      L("Remember, three in a row divide by six, and the minus in front doesn't change that. So the top is six k, and over "
        "three, two k. Always even. Choice number three. [pause] Okay. I'll see you in the next question.",
        show(j2, 'three in a row divide by six'), mk('tick', 'choice 3', 'Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t16-04 (Q12)
# NEW (full): the smallest case gives only a candidate - cross out what doesn't divide it, then test a second case that
# AVOIDS the factor you check (7·9·11, not 3·5·7 or 5·7·9); why 3 always: one of three odd numbers in a row divides by 3.
# 2026-10-15 batch-A review (Codex, reviews/batch-A.md #83): the warning about groups with a five comes BEFORE the second
# test; the second test uses only the last digit (7 x 9 ends in 3, times 11 still ends in 3), so no 693 and no products
# after the answer; the odd numbers written in a row with 3, 9, 15 marked. Paragraphs 5-7 and 8-9 now live here (their
# clarity-overlay entries were folded into this spec, reconciled with _codex_script_clarity_20261012.json). The second
# test continues on a second Method-1 slide (frame check: one slide overlapped the choices), with a So-far box;
# the warning in the right column, the last-digit test in the left column.
k1 = I('k1', 'Smallest: $\\ 1\\cdot3\\cdot5=15$', hand='Smallest :    1·3·5 = 15')
k2 = I('k2', '$45$ does not divide $15$ ✗', size=30, hand='45  does not divide  15   ✗')
k3 = I('k3', 'Smallest case: only a candidate', size=28, col=1)
k0 = I('k0', 'So far: $\\ $(1) out, (2)–(4) left', size=26, col=1); k0['keep'] = 1
k6 = I('k6', '$3\\cdot5\\cdot7$', size=28, col=1, hand='3·5·7')
k6b = I('k6b', 'a $5$ and a $3$ $\\to$ divides by $15$', size=26, col=1, hand='a 5 and a 3  →  divides by 15')
k6c = I('k6c', '$5\\cdot7\\cdot9$: $\\ $the same', size=26, col=1, hand='5·7·9 :   the same')
k4 = I('k4', 'No $5$: $\\ 7\\cdot9\\cdot11$', size=28, hand='No 5 :    7·9·11')
k4b = I('k4b', '$7\\cdot9=63$: $\\ $last digit $3$', size=28, hand='7·9 = 63 :   last digit 3')
k4c = I('k4c', '$\\times11$: $\\ $last digit $3\\cdot1=3$', size=28, hand='×11 :   last digit  3·1 = 3')
k5 = I('k5', 'Ends in $3$ $\\to$ not by $5$', size=28, hand='Ends in 3  →  not by 5')
k5b = I('k5b', 'So not by $15$ ✗', size=28, hand='So not by 15   ✗')
k7 = I('k7', '$7,\\ \\hl{n}{9},\\ 11\\qquad 11,\\ 13,\\ \\hl{n}{15}$', hand='7,  \\hl{n}{9},  11        11,  13,  \\hl{n}{15}')
k8 = I('k8', 'Odd: $\\ 1,\\ \\hl{m}{3},\\ 5,\\ 7,\\ \\hl{m}{9},\\ 11,\\ 13,\\ \\hl{m}{15}$', size=30,
       hand='Odd :   1,  \\hl{m}{3},  5,  7,  \\hl{m}{9},  11,  13,  \\hl{m}{15}')
video('solve-q-r26-t16-04', 'solution', qid='q-r26-t16-04', slides=[
    S('Method 1 · Plugging in numbers',
      L("n is a positive odd number. The product n, times n plus two, times n plus four, is necessarily divisible by:",
        pt('stem', 'n is a positive', 'hl', 7.0), voice='calm', pause=0.5),
      L("So three odd numbers in a row, and what always divides their product. [short pause] We'll solve it two ways, the "
        "two cases, and then the reason.", pt('stem', 'three odd numbers in a row')),
      L("[short pause] Let's start with the smallest case, one, three and five. One times three times five is fifteen. "
        "Forty-five doesn't divide fifteen, so choice number one is out.", show(k1, 'One times three times five'), show(k2, "Forty-five doesn't"),
        mk('cross', 'choice 1', 'choice number one is out')),
      L("But careful, the smallest case only gives a candidate, the biggest number that could work. Fifteen, five and three "
        "all divide fifteen, so I need a second case.", show(k3, 'only gives a candidate'))),
    S('Method 1 · Plugging in numbers',
      L("Now we need a second group, and we have to choose it carefully. Take three, five and seven. Five is in the multiplication, and so is three. So the product is divisible by fifteen, and it can't rule out fifteen. Five, seven and nine has the same problem. So we need a group with no multiple of five.", show(k0, 'Now we need'),
        show(k6, 'Take three, five and seven'), show(k6b, 'So the product is divisible by fifteen'),
        show(k6c, 'Five, seven and nine')),
      L("Let's choose seven, nine and eleven. To check five, we only need the last digit of the product, because a number is divisible by five only when it ends in zero or five. The last digit of a product comes only from the last digits. Seven times nine is sixty-three, which ends in three. Times eleven, it still ends in three, because three times one is three.", show(k4, 'seven, nine and eleven'),
        show(k4b, 'Seven times nine is sixty-three'), show(k4c, 'because three times one')),
      L("A number that ends in three isn't divisible by five. So it isn't divisible by fifteen either, because fifteen is five times three. Choice numbers two and four are out. Only three is left, and choice number three is our answer.", show(k5, "isn't divisible by five"),
        show(k5b, "So it isn't divisible by fifteen"), mk('cross', 'choice 2', 'Choice numbers two'),
        mk('cross', 'choice 4', 'four are out'), mk('tick', 'choice 3', 'choice number three is our answer'))),
    S('Method 2 · Understanding',
      L("Now by understanding. Why is the product always divisible by three? Let's write the odd numbers in a row: one, three, five, seven, nine, eleven, thirteen, fifteen. Three, nine and fifteen are divisible by three. Why every third odd number? Multiples of three go three, six, nine, twelve, fifteen. They alternate odd and even. So the odd multiples are six apart. The odd numbers go up by two, so six is three steps along that list. Every three odd numbers in a row therefore include a multiple of three.", show(k8, 'one, three, five, seven'), pt('k8: m', 'Three, nine and fifteen are divisible'),
        pt('k8: m', 'Every three odd numbers in a row')),
      L("Seven, nine and eleven include nine. Eleven, thirteen and fifteen include fifteen. So one number in the multiplication is divisible by three, and the whole product is divisible by three too. Choice number three is our answer, and I'll see you in the next question.", show(k7, 'Seven, nine and'), mk('tick', 'choice 3', 'Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-465 (Q13)
# NEW: bigger minus smaller is positive, smaller minus bigger is negative, even when both are negative (5 - 3, -3 - (-5),
# 3 - 5); mark each bracket + or -.  REMINDER: product signs (camera lesson), knock out three when plugging in (topic 51).
l1 = I('l1', 'Bigger $-$ smaller $>0$ $\\quad 5-3=2\\quad -3-(-5)=2$', size=28, col=1, hand='5 − 3 = 2      −3 − (−5) = 2')
l2 = I('l2', 'Smaller $-$ bigger $<0$ $\\quad 3-5=-2$', size=28, col=1, hand='3 − 5 = −2')
l3 = I('l3', '(1) $(x-w)$: $+$ $\\quad (y-z)$: $-$', hand='(1)   (x − w) :  +      (y − z) :  −')
l4 = I('l4', '$(+)\\cdot(-)=(-)$ ✓', hand='(+)·(−) = (−)   ✓')
m1 = I('m1', '$w=-2,\\ x=-1,\\ y=1,\\ z=2$', hand='w = −2,   x = −1,   y = 1,   z = 2')
m2 = I('m2', '(1) $1\\cdot(-1)=-1$ ✓ $\\quad$ (2) $-1\\cdot(-4)=4$ ✗', size=30, hand='(1)   1·(−1) = −1  ✓      (2)   −1·(−4) = 4  ✗')
m3 = I('m3', '(3) $1\\cdot1=1$ ✗ $\\quad$ (4) $-1\\cdot(-1)=1$ ✗', size=30, hand='(3)   1·1 = 1  ✗      (4)   −1·(−1) = 1  ✗')
video('solve-q-465', 'solution', qid='q-465', slides=[
    S('Method 1 · Understanding',
      L("Given: w is smaller than x, which is smaller than zero, which is smaller than y, which is smaller than z. Which of "
        "the following expressions is necessarily negative?", pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("So we know the order of four numbers, two negative and two positive, and each choice is a product of brackets. "
        "[short pause] We'll solve it two ways, reading the signs, and then plugging in numbers.", pt('stem: g1', 'the order of four numbers')),
      L("[short pause] Let's start with the signs, and here's the rule. Bigger minus smaller is positive, even when both "
        "are negative. Five minus three is two, and negative three minus negative five is also two. And smaller minus "
        "bigger is negative, three minus five is negative two.", show(l1, 'Bigger minus smaller'), show(l2, 'smaller minus bigger')),
      L("Choice number one. x minus w, x is bigger, so it's positive. y minus z, y is smaller, so it's negative.",
        show(l3, 'Choice number one. x minus w')),
      L("Positive times negative is negative, and that's what they asked for. So choice number one is our answer.",
        show(l4, 'Positive times negative'), mk('tick', 'choice 1', 'choice number one is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in simple numbers in this order, negative two, negative one, one and two.", show(m1, 'negative two, negative one')),
      L("Choice number one, negative one minus negative two is one, and one minus two is negative one. One times negative one "
        "is negative one. Choice number two, x is negative one, and negative two minus two is negative four, so negative one "
        "times negative four is four.", show(m2, 'Choice number one, negative one')),
      L("Choice number three, two minus one is one, and negative one minus negative two is one, so one. Choice number four, "
        "minus y is negative one, and negative two minus negative one is negative one, so the product is one.",
        show(m3, 'Choice number three, two minus one'), mk('cross', 'choice 2', 'Choice number three'), mk('cross', 'choice 3', 'Choice number four'),
        mk('cross', 'choice 4', 'the product is one')),
      L("When I plug in, I knock out three before I mark. Only choice number one is negative. Choice number one. [pause] "
        "Okay. I'll see you in the next question.", mk('tick', 'choice 1', 'Only choice number one is negative'))),
])

# ------------------------------------------------------------------------------------------------ q-466 (Q14)
# NEW: two givens pin the signs (xy < 0 -> opposite signs, x > y -> x is the positive one); zero is neither positive nor
# negative (choice 3 gives 0).  REMINDER: product and quotient signs (camera lesson).
n1 = I('n1', '$xy<0$: $\\ $opposite signs', size=28, col=1, hand='xy < 0 :    opposite signs')
n2 = I('n2', '$x>y$: $\\ \\hl{s}{y<0<x}$', size=30, col=1, hand='x > y :    \\hl{s}{y < 0 < x}')
n3 = I('n3', '(1) $\\frac{x^2-y}{y}=\\frac{(+)}{(-)}<0$ ✗', size=30, hand='(1)   {x^2 − y/y} = {(+)/(−)} < 0   ✗')
n4 = I('n4', '(2) $\\frac{y-x}{y}=\\frac{(-)}{(-)}>0$ ✓', size=30, hand='(2)   {y − x/y} = {(−)/(−)} > 0   ✓')
p1 = I('p1', 'From the givens: $\\ y<0<x$', size=28, col=1, hand='From the givens :    y < 0 < x')
p2 = I('p2', '(1) $\\frac{x^2}{y}-1$: $\\ (-)-1<0$ ✗', size=30, hand='(1)   {x^2/y} − 1 :    (−) − 1 < 0   ✗')
p3 = I('p3', '(3) $\\frac{(x-y)(x+y)}{x-y}=x+y$: $\\ $? ✗', size=30, hand='(3)   {(x − y)(x + y)/x − y} = x + y :    ?   ✗')
p4 = I('p4', '(4) $\\frac{x^2y}{xy^2}=\\frac{x}{y}<0$ ✗', size=30, hand='(4)   {x^2 y/x y^2} = {x/y} < 0   ✗')
p5 = I('p5', '(2) $1-\\frac{x}{y}=1+(+)>0$ ✓', size=30, hand='(2)   1 − {x/y} = 1 + (+) > 0   ✓')
o1 = I('o1', '$x=1,\\ y=-1$', hand='x = 1,    y = −1')
o2 = I('o2', '(1) $\\frac{2}{-1}=-2$ ✗ $\\quad$ (2) $\\frac{-2}{-1}=2$ ✓', size=30, hand='(1)   {2/−1} = −2  ✗      (2)   {−2/−1} = 2  ✓')
o3 = I('o3', '(3) $\\frac{0}{2}=0$ ✗ $\\quad$ (4) $\\frac{-1}{1}=-1$ ✗', size=30, hand='(3)   {0/2} = 0  ✗      (4)   {−1/1} = −1  ✗')
o4 = I('o4', 'Zero is not positive', size=28, col=1)
video('solve-q-466', 'solution', qid='q-466', slides=[
    S('Method 1 · Understanding',
      L("Given: x is bigger than y, and x times y is smaller than zero. Which of the following expressions is necessarily "
        "positive?", pt('stem', 'Given', 'hl', 7.0), voice='calm', pause=0.5),
      L("So two givens, and fractions in the choices. First let's find the signs of x and y. [short pause] We'll solve it "
        "three ways, reading the signs, simplifying each fraction, and then plugging in numbers.", pt('stem: given', 'two givens')),
      L("[short pause] Let's start with the signs. x times y is negative, so x and y have opposite signs, one positive and "
        "one negative. And x is bigger than y. Can the negative one be bigger? No. So y is negative, and x is positive.",
        pt('stem: g2', 'x times y is negative'), show(n1, 'opposite signs'), pt('stem: g1', 'x is bigger than y'), show(n2, 'So y is negative')),
      L("Choice number one. x squared is positive, and minus y, minus a negative, is positive. So the top is positive, and "
        "the bottom, y, is negative. Positive over negative is negative. Out.", show(n3, 'x squared is positive'), mk('cross', 'choice 1', 'Out.')),
      L("Choice number two. y minus x is negative minus positive, negative. And over y, a negative. Negative over negative "
        "is positive. So choice number two is our answer.", show(n4, 'y minus x is'), mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · The math way',
      L("[pause] Another way is to simplify each fraction first, and only then read the signs. What's different? Before, we "
        "read the sign of the whole top and the whole bottom. Here we first break each fraction into simpler pieces. From "
        "the givens, as before, y is negative and x is positive.", show(p1, 'From the givens')),
      L("Choice number one. Divide each term on top by y, and it's x squared over y, minus one. x squared over y is positive "
        "over negative, negative, and minus one makes it even smaller. Negative. Out.", show(p2, 'x squared over y, minus one'),
        mk('cross', 'choice 1', 'smaller. Negative. Out')),
      L("Choice number three. The top is the third shortcut formula, x minus y, times x plus y. Cancel x minus y, and x plus y "
        "is left. A positive plus a negative, and it depends on which is bigger in size. So not necessarily positive. Out.",
        show(p3, 'The top is the third'), mk('cross', 'choice 3', 'not necessarily positive. Out'))),
    S('Method 2 · The math way',
      L("Choice number four. Cancel x times y, and x over y is left. Positive over negative, negative. Out.",
        show(p4, 'Cancel x times y'), mk('cross', 'choice 4', 'negative. Out')),
      L("Choice number two. y over y is one, minus x over y. x over y is negative, so one minus a negative is one plus "
        "something positive. Always positive. Choice number two.", show(p5, 'y over y is one'), mk('tick', 'choice 2', 'Always positive. Choice number two')),
      sb='Method 2 · The math way'),
    S('Method 3 · Plugging in numbers',
      L("[pause] Now let's try plugging in. x is positive and y is negative, so x is one and y is negative one.", show(o1, 'x is one and y is')),
      L("Choice number one. The top is one plus one, which is two, and two over negative one is negative two. Choice number two. The top is negative one minus one, which is negative two, and negative two over negative one is two.", show(o2, 'The top is one plus one')),
      L("Choice number three, one minus one is zero on top, so zero, and zero is not positive. Choice number four, negative "
        "one over one, negative one. Only choice number two is positive. [pause] Okay. I'll see you in the next question.",
        show(o3, 'Choice number three, one minus one'), show(o4, 'zero is not positive'), mk('cross', 'choice 1', 'Choice number four'),
        mk('cross', 'choice 3', 'negative one over one'), mk('cross', 'choice 4', 'Only choice number two'), mk('tick', 'choice 2', 'is positive'))),
])

# ------------------------------------------------------------------------------------------------ q-467 (Q15)
# NEW: work smart - start with the choice that pins both letters to one case (q > 0 makes p > 0 too); a counterexample
# for each other choice.  REMINDER: the sum of positives is positive (camera lesson).
p1 = I('p1', '(4) $0<q<p$: $\\ p+q>0$', hand='(4)   0 < q < p :    p + q > 0')
p2 = I('p2', 'So $r$ pulls the sum down: $\\ \\hl{r}{r<0}$', hand='So r pulls the sum down :    \\hl{r}{r < 0}')
p3 = I('p3', '$p=3,\\ q=2$: $\\ 5+r<0$, $\\ r<-5$', size=30, col=1, hand='p = 3,  q = 2 :    5 + r < 0,   r < −5')
p4 = I('p4', 'One case is faster than three', size=28, col=1)
q1 = I('q1', '(1) $p=-1,\\ q=-2,\\ r=1$: $\\ -2<0$ ✗', size=30, hand='(1)   p = −1,  q = −2,  r = 1 :    −2 < 0   ✗')
q2 = I('q2', '(2), (3) $p=1,\\ q=-10,\\ r=1$: $\\ -8<0$ ✗', size=30, hand='(2), (3)   p = 1,  q = −10,  r = 1 :    −8 < 0   ✗')
q3 = I('q3', '$r$ positive and the givens hold: $\\ $not necessarily', size=26, col=1)
video('solve-q-467', 'solution', qid='q-467', slides=[
    S('Method 1 · Understanding',
      L("Given: p is bigger than q, and p plus q plus r is smaller than zero. Which of the following additional givens makes "
        "r necessarily negative?", pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("So we add one choice to the givens, and look for the one that forces r to be negative. [short pause] We'll solve "
        "it two ways, starting with the smartest choice, and then knocking out the others with numbers.", pt('stem: ask', 'forces r to be negative')),
      L("[short pause] Where do I start? Choice number two says p is positive. Then q could be positive, zero or negative, "
        "three cases. Slow. Choice number four says q is positive, and p is bigger than q, so p is positive too. One case "
        "only. So let's start there.", pt('choice 2', 'Choice number two says'), pt('choice 4', 'Choice number four says'), show(p4, 'One case only')),
      L("p and q are both positive, so p plus q is positive. But the sum of all three is negative. So r has to pull the sum "
        "down, and r must be negative.", show(p1, 'p and q are both positive'), show(p2, 'r has to pull the sum down')),
      L("Let's see it in numbers. p is three and q is two, so five plus r is smaller than zero, and r is smaller than "
        "negative five. Choice number four is our answer.", show(p3, 'p is three and q is two'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Another way is to knock out the other choices with numbers. For each one, I look for a positive r that still "
        "fits the givens.", show(q3, 'a positive r that still fits')),
      L("Choice number one, p is negative. p is negative one, q is negative two, and r is one. Negative one plus negative two "
        "plus one is negative two, smaller than zero. The givens hold, and r is positive. Out.",
        show(q1, 'p is negative one'), mk('cross', 'choice 1', 'r is positive. Out')),
      L("Choice numbers two and three. p is one, q is negative ten, and r is one. One plus negative ten plus one is negative "
        "eight. p is positive and q is negative, so both choices fit, and r is still positive. Both out. So choice number "
        "four. [pause] Okay. I'll see you in the next question.", show(q2, 'p is one, q is negative ten'),
        mk('cross', 'choice 2', 'so both choices fit'), mk('cross', 'choice 3', 'Both out'), mk('tick', 'choice 4', 'So choice number'))),
])

# ------------------------------------------------------------------------------------------------ q-468 (Q16)
# NEW: b^2 - a^2 for consecutive evens = (b - a)(b + a) = 2(2a + 2) = 4a + 4 (6^2 - 4^2 = 20 = 4·4 + 4); get rid of the
# letters the choices don't use; check that the choices come out different before plugging in (a = c = 2 ties).
# REMINDER: the third shortcut formula (topic 4), consecutive evens b = a + 2 (lesson).
s1 = I('s1', '$b=a+2,\\ \\ \\ d=c+2$', hand='b = a + 2,      d = c + 2')
s2 = I('s2', '$b^2-a^2=(b-a)(b+a)=2(2a+2)=4a+4$', size=30, hand='b^2 − a^2 = (b − a)(b + a) = 2(2a + 2) = 4a + 4')
s3 = I('s3', '$6^2-4^2=20=4\\cdot4+4$ ✓', size=28, col=1, hand='6^2 − 4^2 = 20 = 4·4 + 4   ✓')
s4 = I('s4', 'Top: $\\ 4a+4+4c+4=4(a+c+2)$', size=32, hand='Top :    4a + 4 + 4c + 4 = 4(a + c + 2)')
s5 = I('s5', 'Bottom: $\\ a+d=a+c+2$ $\\ \\to\\ \\hl{f}{4}$', size=32, hand='Bottom :    a + d = a + c + 2    →    \\hl{f}{4}')
s6 = I('s6', 'Gap of $1$? The trap: $\\ 2$', size=28, col=1)
t1 = I('t1', '$a=c=2$: $\\ 16,\\ 2,\\ 4,\\ 4$ $\\ $tie ✗', size=30, hand='a = c = 2 :    16,  2,  4,  4    tie  ✗')
t2 = I('t2', '$a=2,\\ c=8$: $\\ 40,\\ 2,\\ 10,\\ 4$ ✓', size=30, hand='a = 2,  c = 8 :    40,  2,  10,  4   ✓')
t3 = I('t3', '$\\frac{16-4+100-64}{2+10}=\\frac{48}{12}=\\hl{f}{4}$', hand='{16 − 4 + 100 − 64/2 + 10} = {48/12} = \\hl{f}{4}')
video('solve-q-468', 'solution', qid='q-468', slides=[
    S('Method 1 · The math way: shortcut formula',
      L("a and b are consecutive even numbers, and c and d are consecutive even numbers. Given: a is smaller than b, c is "
        "smaller than d, and a plus d is not zero. What is b squared minus a squared, plus d squared minus c squared, over a "
        "plus d?", pt('stem', 'a and b are', 'hl', 14.0), voice='calm', pause=0.5),
      L("So two pairs of consecutive evens, and the choices use only a and c. So we'll get rid of b and d. [short pause] "
        "We'll solve it two ways, with the shortcut formula, and then plugging in numbers.", pt('choice 1', 'the choices use only a and c')),
      L("[short pause] Let's start with the formula. Consecutive evens go up by two, so b is a plus two, and d is c plus "
        "two.", show(s1, 'b is a plus two')),
      L("b squared minus a squared is b minus a, times b plus a. b minus a is two, and b plus a is two a plus two. So it's "
        "two times two a plus two, which is four a plus four. For example, six squared is thirty-six and four squared is sixteen. Thirty-six minus sixteen is twenty, and four times four plus four is twenty too.", show(s2, 'b squared minus a squared is'), show(s3, 'For example, six squared is')),
      L("In the same way, d squared minus c squared is four c plus four. So the top is four a plus four c plus eight, which "
        "is four times, in brackets, a plus c plus two.", show(s4, 'So the top is')),
      L("And the bottom, a plus d, is a plus c plus two, the same bracket. It cancels, and we get four. Choice number four is "
        "our answer.", show(s5, 'And the bottom'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Now careful, two is the trap. It comes from a gap of one, but these are even numbers, with a gap of two.",
        show(s6, 'two is the trap'), mk('cross', 'choice 2', 'a gap of one'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in. The choices use a and c, so I choose them. But first, check that the choices come "
        "out different. With a and c both two, choice number three gives four, and choice number four gives four. A tie, so "
        "that pick is bad.", show(t1, 'With a and c both two')),
      L("So a is two and c is eight. The choices give forty, two, ten and four, all different.", show(t2, 'a is two and c is eight')),
      L("Then b is four and d is ten. Sixteen minus four is twelve, and a hundred minus sixty-four is thirty-six, so the top "
        "is forty-eight. The bottom is two plus ten, which is twelve. Forty-eight over twelve is four. Choice number four. "
        "[pause] Okay. I'll see you in the next question.", show(t3, 'Then b is four'), mk('tick', 'choice 4', 'Choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-469 (Q17)
# NEW: one letter around the middle turns x^2 + y^2 = z^2 into y^2 = 4y; don't divide by y (y = 0 is a solution too);
# x + z is twice the middle; the trap 12 = 3 + 4 + 5.  REMINDER: shortcut formulas (topic 4), don't divide by an unknown
# that may be 0 (topic 6), the 3-4-5 triangle (topic 31).
u1 = I('u1', '$(y-1)^2+y^2=(y+1)^2$', hand='(y − 1)^2 + y^2 = (y + 1)^2')
u2 = I('u2', '$y^2-2y+1+y^2=y^2+2y+1$', size=32, hand='y^2 − 2y + 1 + y^2 = y^2 + 2y + 1')
u3 = I('u3', '$y^2=4y$ $\\ \\to\\ y(y-4)=0$', hand='y^2 = 4y    →    y(y − 4) = 0')
u4 = I('u4', 'Don\'t divide by $y$: $\\ y=0$ works too', size=28, col=1)
u5 = I('u5', '$y=4$: $\\ 3,4,5$, $\\ x+z=\\hl{e}{8}$ $\\quad y=0$: $\\ x+z=0$', size=30, hand='y = 4 :   3, 4, 5,   x + z = \\hl{e}{8}      y = 0 :   x + z = 0')
u6 = I('u6', '$3+4+5=12$: $\\ $only $x+z$ ✗', size=28, col=1, hand='3 + 4 + 5 = 12 :   only x + z   ✗')
v1 = I('v1', '$x+z=2y$: $\\ $the middle is half', size=30, hand='x + z = 2y :    the middle is half')
v2 = I('v2', '$10$: $\\ 4,5,6$: $\\ 16+25=41\\ne36$ ✗', size=30, hand='10 :   4, 5, 6 :    16 + 25 = 41 ≠ 36   ✗')
v3 = I('v3', '$8$: $\\ 3,4,5$: $\\ 9+16=25$ ✓', size=30, hand='8 :   3, 4, 5 :    9 + 16 = 25   ✓')
video('solve-q-469', 'solution', qid='q-469', slides=[
    S('Method 1 · The math way: one letter',
      L("x, y and z are consecutive integers, and x is smaller than y, which is smaller than z. Given: x squared plus y "
        "squared is equal to z squared. Which of the following could be the value of x plus z?", pt('stem', 'x, y and z', 'hl', 11.0), voice='calm', pause=0.5),
      L("So three numbers in a row, and one equation. [short pause] We'll solve it two ways, with one letter, and then "
        "plugging in the answers.", pt('stem', 'one equation')),
      L("[short pause] Let's start with one letter, the middle one, y. So x is y minus one, and z is y plus one. Then the "
        "equation is y minus one, squared, plus y squared, equals y plus one, squared.", show(u1, 'the equation is')),
      L("Open the brackets with the shortcut formulas. On the left, y squared minus two y plus one, plus y squared. On the "
        "right, y squared plus two y plus one.", show(u2, 'Open the brackets')),
      L("Take y squared and one off both sides, and add two y. What's left is y squared equals four y. Now careful, don't "
        "divide by y, because y could be zero. Move it over instead, y times, in brackets, y minus four, is zero.",
        show(u3, 'y squared equals four y'), show(u4, "don't divide by y")),
      L("So y is four, or y is zero. y is four gives three, four, five, and x plus z is three plus five, eight. y is zero "
        "gives negative one, zero, one, and x plus z is zero. Could be, so eight, choice number two is our answer.",
        show(u5, 'So y is four'), mk('tick', 'choice 2', 'choice number two is our answer')),
      L("And careful, a lot of students see three, four, five and add all three, twelve. But they ask only for x plus z.",
        show(u6, 'add all three'), mk('cross', 'choice 3', 'only for x plus z'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's try plugging in the answers. x and z are one below and one above the middle, so x plus z is two "
        "times the middle. So the middle is half of the choice.", show(v1, 'two times the middle')),
      L("Ten, the middle is five, so four, five, six. Sixteen plus twenty-five is forty-one, and six squared is thirty-six. "
        "Not equal. Out.", show(v2, 'the middle is five'), mk('cross', 'choice 1', 'Not equal. Out')),
      L("Eight, the middle is four, so three, four, five. Nine plus sixteen is twenty-five, and five squared is twenty-five. "
        "It works, so choice number two. [pause] Okay. I'll see you in the next question.",
        show(v3, 'the middle is four'), mk('tick', 'choice 2', 'It works, so choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-470 (Q18)
# NEW: in a parity question you may drop the powers (never in a regular equation); shifting b by an odd number vs an
# even number gives brackets of different parity.  REMINDER: powers keep parity, count the odd terms (parity lesson).
w4 = I('w4', 'From $b-3$ to $b+8$: $\\ $a jump of $11$, odd', size=30, hand='From  b − 3  to  b + 8 :    a jump of 11,  odd')
w5 = I('w5', '$2 \\to 13 \\quad 5 \\to 16$: $\\ $one even, one odd', size=28, col=1, hand='2 → 13      5 → 16 :    one even,  one odd')
w6 = I('w6', 'Powers keep parity: $\\ $odd $+$ even $=$ \\hl{o}{odd}', size=30, hand='Powers keep parity :    odd + even  =  \\hl{o}{odd}')
w1 = I('w1', 'Drop the powers: $\\ (b-3)+(b+8)=2b+5$', size=32, hand='Drop the powers :    (b − 3) + (b + 8) = 2b + 5')
w2 = I('w2', '$2b$ even $+\\ 5$ $=$ \\hl{p}{odd}', hand='2b  even  + 5  =  \\hl{p}{odd}')
w3 = I('w3', 'Only in parity questions, never in equations', size=26, col=1)
x1 = I('x1', '$b=1$: $\\ (-2)^2+9^3=4+729=733$', size=32, hand='b = 1 :    (−2)^2 + 9^3 = 4 + 729 = 733')
x2 = I('x2', '$b=2$: $\\ (-1)^2+10^3=1+1000=1001$', size=32, hand='b = 2 :    (−1)^2 + 10^3 = 1 + 1000 = 1001')
x3 = I('x3', '$b$ odd or even, $\\ y$ odd both times', size=28, col=1)
video('solve-q-470', 'solution', qid='q-470', slides=[
    S('Method 1 · Understanding: even and odd',
      L("b and y are integers. Given: y is equal to b minus three, squared, plus b plus eight, cubed. Which of the following "
        "statements is necessarily true?", pt('stem', 'b and y are', 'hl', 8.0), voice='calm', pause=0.5),
      L("So all the choices are about even and odd. [short pause] We'll solve it three ways, with the two brackets, "
        "dropping the powers, and then plugging in numbers.", pt('choice 1', 'about even and odd')),
      L("[short pause] Let's start with the two brackets. Both are built from the same b. From b minus three up to b plus "
        "eight is a jump of eleven, an odd jump.", show(w4, 'From b minus three')),
      L("And an odd jump always switches between even and odd. From two, a jump of eleven lands on thirteen, and from five, "
        "on sixteen. So one bracket is even, and the other is odd.", show(w5, 'From two, a jump')),
      L("A power doesn't change parity, so after the powers, still one even and one odd. Odd plus even is odd. So y is "
        "always odd. Choice number four is our answer.", show(w6, "A power doesn't change"), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Understanding: drop the powers',
      L("[pause] Another way, and it's the shortest. It uses the same rule, powers don't change parity, but instead of "
        "thinking about the brackets, we just drop the powers. In a parity question that's allowed, and I'd never do that in "
        "a regular equation.", show(w3, 'never do that in a regular equation')),
      L("Without the powers, b minus three plus b plus eight is two b plus five. Two b is always even, whatever b is, and "
        "even plus five is odd. So y is always odd. Choice number four.", show(w1, 'Without the powers'),
        show(w2, 'Two b is always even'), mk('tick', 'choice 4', 'So y is always odd. Choice number four'))),
    S('Method 3 · Plugging in numbers',
      L("[pause] Now let's try plugging in. It's easier to choose b than y. b is one. One minus three is negative two, and "
        "squared is four. One plus eight is nine, and nine cubed is seven twenty-nine. Four plus seven "
        "twenty-nine is seven thirty-three, odd.", show(x1, 'b is one')),
      L("b is two. Two minus three is negative one, and squared is one. Two plus eight is ten, and ten cubed is a thousand. "
        "One plus a thousand is a thousand one, odd again.", show(x2, 'b is two')),
      L("So b can be odd or even, and choice numbers one and three are out. y was odd both times, so choice number two is "
        "out. Choice number four. [pause] Okay. I'll see you in the next question.", show(x3, 'b can be odd or even'),
        mk('cross', 'choice 1', 'choice numbers one'), mk('cross', 'choice 3', 'and three are out'), mk('cross', 'choice 2', 'choice number two is'),
        mk('tick', 'choice 4', 'Choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-471 (Q19)
# NEW: 2k + 1 is odd for every k; an odd product means every factor is odd, powers dropped (a odd, b + 1 odd -> b even,
# c - 5 odd -> c even); one example knocks out k, b, c.  REMINDER: one even factor makes a product even (parity lesson).
y1 = I('y1', '$2k+1$: $\\ $odd for every $k$ $\\quad k=2$: $5$, $\\ k=3$: $7$', size=28, hand='2k + 1 :   odd for every k      k = 2 :  5,   k = 3 :  7')
y2 = I('y2', 'Odd product: every factor odd', size=28, col=1)
y3 = I('y3', '$a$ odd ✓ $\\quad b+1$ odd $\\to b$ even $\\quad c-5$ odd $\\to c$ even', size=28,
       hand='a  odd  ✓      b + 1  odd  →  b  even      c − 5  odd  →  c  even')
z1 = I('z1', '$a=1,\\ b=0,\\ c=6$: $\\ 1\\cdot1\\cdot1=1$', size=32, hand='a = 1,   b = 0,   c = 6 :    1·1·1 = 1')
z2 = I('z2', '$2k+1=1$, $\\ k=0$: $\\ k,\\ b,\\ c$ even ✗', size=32, hand='2k + 1 = 1,   k = 0 :    k,  b,  c  even   ✗')
video('solve-q-471', 'solution', qid='q-471', slides=[
    S('Method 1 · Understanding',
      L("k, a, b and c are integers. Given: two k plus one is equal to a cubed, times b plus one, squared, times c minus "
        "five, to the power of four. Which of the numbers k, a, b, c is necessarily odd?", pt('stem', 'k, a, b and c', 'hl', 11.0), voice='calm', pause=0.5),
      L("It looks scary, but it's one rule about odd products. [short pause] We'll solve it two ways, with that rule, and "
        "then plugging in numbers.", pt('stem: g1', "It looks scary")),
      L("[short pause] Let's start with the left side, two k plus one. Two k is always even, and plus one makes it odd. k is "
        "two gives five, and k is three gives seven, both odd. So k can be anything, and the left side is odd.",
        show(y1, 'Two k is always even')),
      L("So the right side is odd too. And a product is odd only when every factor is odd, because one even factor brings a "
        "two in. The powers don't matter, so let's go factor by factor.", show(y2, 'every factor is odd')),
      L("a cubed is odd, so a is odd. b plus one is odd, so b is even. c minus five is odd, so c is even. Only a is "
        "necessarily odd, choice number two is our answer.", show(y3, 'a cubed is odd'), mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in, and look for an example where k, b and c are even. a is one, b is zero, and c is "
        "six. One cubed is one, zero plus one is one, and six minus five is one. So the right side is one.", show(z1, 'a is one, b is zero')),
      L("Two k plus one is one, so k is zero. And k, b and c are all even here, so choice numbers one, three and four are "
        "out. Choice number two. [pause] Okay. I'll see you in the next question.", show(z2, 'Two k plus one is one'),
        mk('cross', 'choice 1', 'choice numbers one'), mk('cross', 'choice 3', 'three and four'), mk('cross', 'choice 4', 'are out'),
        mk('tick', 'choice 2', 'Choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-472 (Q20)
# NEW: count the twos with b = 2k in each fraction; "not necessarily" = a third two may come by luck (b = 4) but not for
# every b; plug in the SMALLEST numbers, or the luck hides the answer.  REMINDER: two consecutive evens divide by 8, count
# the twos (products lesson), the shortcut formulas (topic 4).
a1 = I('a1', '$b=2k$', hand='b = 2k')
a2 = I('a2', '(1) $b^3=8k^3$ ✓', size=30, hand='(1)   b^3 = 8k^3   ✓')
a3 = I('a3', '(2) $(a+1)(a+3)$: consecutive evens ✓', size=30, hand='(2)   (a + 1)(a + 3) :   consecutive evens   ✓')
a4 = I('a4', '(3) $2a^2+2b^2-2a^2=2b^2=8k^2$ ✓', size=30, hand='(3)   2a^2 + 2b^2 − 2a^2 = 2b^2 = 8k^2   ✓')
a5 = I('a5', '(4) $ab^2=4ak^2$: $\\ $two twos ✗', size=30, hand='(4)   ab^2 = 4ak^2 :    two twos   ✗')
a6 = I('a6', '$a=1,\\ b=2$: $\\ \\frac48=\\frac12\\quad a=1,\\ b=4$: $\\ \\frac{16}{8}=2$', size=28, col=1, hand='a=1, b=2 :  {4/8} = {1/2}      a=1, b=4 :  {16/8} = 2')
b1 = I('b1', '$a=1,\\ b=2$ $\\ $(the smallest)', hand='a = 1,    b = 2     (the smallest)')
b2 = I('b2', '(1) $\\frac{8\\cdot3}{8}=3\\quad$ (2) $\\frac{2\\cdot4}{8}=1$', size=30, hand='(1)   {8·3/8} = 3      (2)   {2·4/8} = 1')
b3 = I('b3', '(3) $\\frac{9+1-2}{8}=1\\quad$ (4) $\\frac{4}{8}=\\frac12$ ✗', size=30, hand='(3)   {9 + 1 − 2/8} = 1      (4)   {4/8} = {1/2}   ✗')
b4 = I('b4', '$b=4$ would hide it: $\\ \\frac{16}{8}=2$', size=28, col=1, hand='b = 4  would hide it :    {16/8} = 2')
video('solve-q-472', 'solution', qid='q-472', slides=[
    S('Method 1 · Understanding: count the twos',
      L("a is an odd positive number, and b is an even positive number. Which of the following expressions is not "
        "necessarily an integer?", pt('stem', 'a is an odd', 'hl', 7.0), voice='calm', pause=0.5),
      L("So every choice is over eight, and eight is three twos. Three choices always have enough twos on top, and one "
        "doesn't. [short pause] We'll solve it two ways, counting the twos, and then plugging in the smallest numbers.",
        pt('choice 1', 'every choice is over eight')),
      L("[short pause] Let's count the twos. b is even, so b is two k.", show(a1, 'b is two k')),
      L("Choice number one, b cubed is two k, cubed, eight k cubed. The whole eight is there, always whole. Out.",
        show(a2, 'b cubed is'), mk('cross', 'choice 1', 'always whole. Out')),
      L("Choice number two. a is odd, so a plus one and a plus three are two consecutive even numbers, and they always "
        "divide by eight. Out.", show(a3, 'a plus one and a plus three'), mk('cross', 'choice 2', 'divide by eight. Out'))),
    S('Method 1 · Understanding: count the twos',
      L("Choice number three. Open both squares. The two a b terms cancel, and two a squared plus two b squared, minus two "
        "a squared, leaves two b squared. That's two times four k squared, eight k squared. Out.", show(a4, 'Open both squares'),
        mk('cross', 'choice 3', 'eight k squared. Out')),
      L("Choice number four, a times b squared. b squared is four k squared, two twos, and a is odd, no twos at all. Only two "
        "twos, and eight needs three. A third two can come from k by luck, but not necessarily. Choice number four is our "
        "answer.", show(a5, 'a times b squared'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Let's see it in numbers. a is one and b is two, four over eight is a half. But a is one and b is four, sixteen over "
        "eight is two. Whole by luck.", show(a6, 'a is one and b is two')),
      sb='Method 1 · Understanding: count the twos'),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in. Which numbers? The smallest, a is one and b is two, so no extra two sneaks in.",
        show(b1, 'The smallest')),
      L("Choice number one, two cubed is eight, times three is twenty-four, over eight is three. Choice number two, two times "
        "four is eight, over eight is one.", show(b2, 'two cubed is eight')),
      L("Choice number three, nine plus one minus two is eight, over eight is one. Choice number four, one times four is "
        "four, over eight is a half. Not whole, so choice number four.", show(b3, 'nine plus one minus two'), mk('tick', 'choice 4', 'Not whole, so choice number four')),
      L("And see why the smallest. With b four, choice number four gives sixteen over eight, two, and it would hide the "
        "answer. [pause] Okay. I'll see you in the next question.", show(b4, 'With b four'))),
])

# ------------------------------------------------------------------------------------------------ r26-t16-summary
# REMINDERS only, said the way they were taught; new numbers.
y1s = I('y1s', 'Same signs $+$ · different signs $-$ $\\quad (-2)(-5)=10\\quad (-2)\\cdot5=-10$', size=34)
y2s = I('y2s', 'Count the minuses: odd $\\to -$, even $\\to +$', size=36)
y3s = I('y3s', 'Mixed signs: the bigger size wins $\\quad -9+4=-5$', size=36)
y4s = I('y4s', 'Bigger $-$ smaller $>0$ $\\quad -3-(-8)=5$', size=36)
y5s = I('y5s', 'Even power $\\ge0$ $\\quad (-3)^3=-27$ keeps the sign $\\quad x<0\\Rightarrow -x>0$', size=32)
c1s = I('c1s', 'One letter: $\\ b-1,\\ b,\\ b+1$ $\\quad$ evens: $\\ b-2,\\ b,\\ b+2$', size=34)
c2s = I('c2s', 'Sum $=$ count $\\times$ middle $\\quad 16+\\ldots+20=5\\cdot18=90$', size=34)
c3s = I('c3s', 'From $a$ to $b$: $\\ b-a+1$ $\\quad$ neighbors: $\\ b^2-a^2=a+b$', size=34)
e1s = I('e1s', 'In a sum, count the odd terms $\\quad$ one even factor: even', size=34)
e2s = I('e2s', 'Odd $\\div$ nonzero even: a fraction. Positive integer powers keep parity', size=28)
e3s = I('e3s', 'Test the cases; examples alone do not prove always', size=30)
p1s = I('p1s', 'In a row: $2,\\ 3\\to6,\\ 4\\to24$ $\\quad$ consecutive evens $\\to8$', size=34)
p2s = I('p2s', 'Count the twos $\\quad$ smallest case: only a candidate', size=34)
video('r26-t16-summary', 'lesson', slides=[
    S('Integers: Summary',
      L("Before you practice, here's a quick summary of the topic. Signs, numbers in a row, and even and odd.")),
    S('Signs',
      L("Multiplying and dividing, same signs give plus, and different signs give minus. Negative two times negative five is "
        "ten, and negative two times five is negative ten. With many factors, count the minuses.", show(y1s, 'same signs give plus'), show(y2s, 'count the minuses')),
      L("Adding with mixed signs, the bigger size wins. Negative nine plus four is negative five. And bigger minus smaller is "
        "positive, even with negatives. Negative three minus negative eight is five.", show(y3s, 'the bigger size wins'), show(y4s, 'bigger minus smaller')),
      L("An even power is never negative, an odd power keeps the sign, and minus x is positive when x is negative.",
        show(y5s, 'An even power'))),
    S('Numbers in a row',
      L("Numbers in a row? One letter, around the middle. Evens or odds go up by two.", show(c1s, 'One letter')),
      L("The sum is the count times the middle. Sixteen to twenty is five numbers, and five times eighteen is ninety.",
        show(c2s, 'the count times the middle')),
      L("From a to b there are b minus a plus one integers. And for neighbors, b squared minus a squared is a plus b.",
        show(c3s, 'From a to b'))),
    S('Even and odd',
      L("In a sum, only the odd terms count. In a product, one even factor makes it even.", show(e1s, 'only the odd terms count')),
      L("Odd over nonzero even is always a fraction. Positive whole-number powers preserve parity, so you may drop them when judging even or odd.", show(e2s, 'Odd over')),
      L("Plugging in? Test the relevant cases, and look for different outcomes in division. "
        "Examples alone do not prove always. Explain why every allowed value works, or rule out the other answer choices with counterexamples.",
        show(e3s, 'Test the relevant cases'))),
    S('Products',
      L("Two in a row divide by two, three by six, and four by twenty-four. Two consecutive evens divide by eight.", show(p1s, 'Two in a row')),
      L("Is it a whole number? Count the twos. And the smallest case is only a candidate, so test a second case that avoids "
        "the factor. [pause] That's it. Now go practice, and I'll see you in the next video.", show(p2s, 'Count the twos'))),
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
 "q-457": "Given:\n$\\begin{cases} a\\ne0 \\\\ \\frac{a^5\\cdot b^2}{|a|}<0 \\end{cases}$\nWhich of the following is necessarily true?",
 "q-r26-t16-01": "Given:\n$\\begin{cases} x<0<y \\\\ x+y>0 \\end{cases}$\nWhich of the following is necessarily true?",
 "q-r26-t16-02": "The sum of seven consecutive integers is $91$. What is the largest of them?",
 "q-r26-t16-03": "The sum of four consecutive integers is always —",
 "q-460": "m and n are positive integers, and $m+n$ is odd. Which of the following is true about the expression $m^n+n^m+9+4n$?",
 "q-461": "a and b are integers. a is odd, and b is even and not $0$. Which of the following is the most precise description of $\\frac{6a}{b^2}$?",
 "q-462": "a and b are integers. Given: $a-b=6$. Which of the following expressions is necessarily even?",
 "q-463": "n is an odd number. Which of the following is the most precise description of $\\frac{9n^2-1}{4}$?",
 "q-464": "n is an integer. The expression $\\frac{n-n^3}{3}$ is always —",
 "q-r26-t16-04": "n is a positive odd number. The product $n(n+2)(n+4)$ is necessarily divisible by —",
 "q-465": "Given: $w<x<0<y<z$. Which of the following expressions is necessarily negative?",
 "q-466": "Given:\n$\\begin{cases} x>y \\\\ xy<0 \\end{cases}$\nWhich of the following expressions is necessarily positive?",
 "q-467": "Given:\n$\\begin{cases} p>q \\\\ p+q+r<0 \\end{cases}$\nWhich of the following additional givens makes r necessarily negative?",
 "q-470": "b and y are integers. Given: $y=(b-3)^2+(b+8)^3$. Which of the following statements is necessarily true?",
 "q-471": "k, a, b and c are integers. Given: $2k+1=a^3\\cdot(b+1)^2\\cdot(c-5)^4$. Which of the numbers k, a, b, c is necessarily odd?",
 "q-472": "a is an odd positive number, and b is an even positive number. Which of the following expressions is not necessarily an integer?"
}   # "=?" questions (no question sentence): the whole stem only
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
_mv.post(_types.SimpleNamespace(**globals()), 16)

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
