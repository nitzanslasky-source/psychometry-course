"""Topic 19 (Defining a New Operation) - the redo for the teacher's own-voice reading (2026-10-12; rewritten 2026-10-13 in the
clarity style, with the method visuals SLOT / CHAIN of math_patches/_method_visuals.py), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py / _ai_vis_t16.py / _ai_vis_t17.py / _ai_vis_t18.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The teacher records only the camera lesson 'new-operation' (re-record, never touched here). Every other topic-19 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t19.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t19.py ai_redo_t19() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods and EVERY method of the Hebrew solution (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-19-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t19ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-19 flow order of the scripts (new-operation = the camera lesson, not here)
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
CAM_BASE = 'new-operation'
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
            'style': "the teacher reads it herself (Reading Studio), topic-19 redo (2026-10-12): math_patches/_ai_vis_t19.py is "
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


# =================================================================================================================
# THE SCRIPTS (topic-19 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-19-AI-scripts-review.md.
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ new-operation (camera lesson)
# 2026-10-13 teacher: her camera first lesson as a reading script too ("the same style, with the handwriting and all
# that, but maybe a bit more examples"). Hebrew lesson alg 18767-18985: a new operation is new on the psychometric but
# needs only known tools; the dot / plus (new symbols) and the small 2 up high and roots (real new operations); the heart
# (x heart y = 2(x + y)); the exam's $ / hash / brackets; THE SAME TEMPLATE ($(a) = a² - a: put the number where a was);
# the operation comes before everything except brackets ($a + $b is not $(a + b): 3² + 4² is not 7²; "think what you'd
# do with a square"); nested: inner brackets first (the inner value coloured, then put in its place); finding the
# operation from one result (8x was one guess; test the choices; in the exam mark and move on, here check the rest to
# learn). Kept from the English lesson: brackets on every input (negative, an expression) and the trap; the order can
# matter (one counterexample; letters for "always"; equal inputs prove nothing); an unknown input = an equation.
# Every concept gets 2-3 examples and a non-example where it helps; new numbers (not the Hebrew's, not the questions').
nos1 = SLOT('nos1', '[[a]] ♥ [[b]] = 5·([[a]] + [[b]])', [('in', '{{7}} ♥ {{3}} = 5·({{7}} + {{3}})'), ('sum', '= 5·10'), ('calc', '= 50')])   # 2026-10-15 Codex batch A: one step per clause
nos2 = SLOT('nos2', '◆([[a]]) = [[a]]^2 − 3·[[a]]', [('in', '◆({{5}}) = {{5}}^2 − 3·{{5}}'), ('sq', '= 25 − 3·5'), ('tm', '= 25 − 15'), ('calc', '= 10')])   # 2026-10-15 Codex batch A
nos3 = SLOT('nos3', '◆([[x]]) = [[x]]^2 + 3·[[x]]', [('in', '◆({{−2}}) = {{(−2)}}^2 + 3·{{(−2)}}'), ('calc', '= 4 − 6 = −2')])
noc1 = CHAIN('noc1', [('line', '◆([[◆(2)]])'), ('in', '[[◆(2)]] = 2^2 = {{4}}'), ('out', '◆({{4}}) = 4^2 = {{16}}')])
no1 = I('no1', '$3\\cdot7$ $\\ \\to\\ $ $3\\times7=21$', size=36)
no2 = IH('no2', '$5^2=5\\cdot5=25$', size=34)
no3 = IH('no3', '$2^3=2\\cdot2\\cdot2=8$', size=34)
no4 = I('no4', '$7\\heartsuit3=\\ ?$', size=36)
no5 = I('no5', '$2\\heartsuit6$', size=32)
no5a = I('no5a', '$=5\\cdot(2+6)$', size=32)
no5b = I('no5b', '$=5\\cdot8$', size=32)
no5c = I('no5c', '$=40$', size=32)
no6 = I('no6', '$7\\cdot5+3=38$ ✗ $\\quad$ the $5$ multiplies the whole sum', size=28)
no7 = I('no7', 'On the exam: a dollar sign, $\\#$, brackets $\\quad$ here: $\\blacklozenge$', size=30, col=1)   # 2026-10-14: a literal \\$ broke the caption's math
no8 = IH('no8', '$\\blacklozenge(2)=2^2-3\\cdot2$', size=32)
no8b = IH('no8b', '$=4-6$', size=32)
no8c = IH('no8c', '$=-2$', size=32)
no9 = IH('no9', '$-2^2=-4$ ✗ $\\quad (-2)^2=4$ ✓', size=32, col=1)
no10 = IH('no10', '$\\blacklozenge(x+2)=(x+2)^2+3(x+2)$', size=32)
no11 = IH('no11', '$=x^2+4x+4$', size=32)
no11a = IH('no11a', '$\\quad+3x+6$', size=32)
no11b = IH('no11b', '$4x+3x=7x$', size=30, col=1)
no11c = IH('no11c', '$4+6=10$', size=30, col=1)
no11d = IH('no11d', '$=x^2+7x+10$', size=32)
no12 = I('no12', 'Inside its brackets first, then the definition, then the rest', size=30)
no13 = IH('no13', '$\\blacklozenge(3)+\\blacklozenge(4)=9+16=25$', size=32)
no14 = I('no14', '$\\blacklozenge(7)=49$ ✗ $\\quad 3^2+4^2\\ne7^2$', size=32)
no15 = IH('no15', '$\\blacklozenge(3+4)=\\blacklozenge(7)=49$', size=32)
no16 = I('no16', '$a\\star b=3a+b^2$', size=34, col=1)
no17 = IH('no17', '$(1\\star2)\\star3$', size=32)
no17b = IH('no17b', '$1\\star2=3+4=7$', size=32)
no17c = IH('no17c', '$(1\\star2)\\star3=7\\star3$', size=32)
no18 = IH('no18', '$7\\star3=21+9=30$', size=32)
no19 = I('no19', '$\\blacklozenge(5)=30$: $\\ 6x$? $\\ 6\\cdot5=30$', size=30)
no19b = I('no19b', '$5x+5$? $\\ 25+5=30$', size=30)
no20 = I('no20', '$x^2+5$: $\\ 25+5=30$ ✓ could be', size=28)
no20b = I('no20b', '$4x+8$: $\\ 20+8=28$ ✗ cannot', size=28)
no21d = I('no21d', '$a\\star b=3a+b^2$', size=32, col=1)
no21 = IH('no21', '$2\\star4=6+16=22$', size=32)
no21b = IH('no21b', '$4\\star2=12+4=16$', size=32)
no22 = I('no22', 'Not always? One example where it fails.', size=30)
no23 = I('no23', 'Always? Use letters', size=28)
no23a = I('no23a', '$a\\heartsuit b=5(a+b)$', size=30, col=1)
no23b = I('no23b', '$b\\heartsuit a=5(b+a)=5(a+b)=a\\heartsuit b$', size=28)
no24 = I('no24', 'Order questions: equal inputs show nothing ($4\\star4=4\\star4$)', size=28)
no25 = IH('no25', '$x\\star4=25$', size=32)
no25d = I('no25d', '$a\\star b=3a+b^2$', size=30, col=1)
no25a = IH('no25a', '$3x+16=25$', size=32)
no25b = IH('no25b', '$3x=9$', size=32)
no25e = IH('no25e', '$x=9\\div3=3$', size=32)
no25c = IH('no25c', '$3\\cdot3+16=9+16=25$ ✓', size=32)
no26 = I('no26', '$k\\heartsuit2=35$', size=32)
no26d = I('no26d', '$a\\heartsuit b=5(a+b)$', size=30, col=1)
no26a = IH('no26a', '$5(k+2)=35$', size=32)
no26b = IH('no26b', '$k+2=35\\div5=7$', size=32)
no26c = IH('no26c', '$k=7-2=5$', size=32)
no27 = I('no27', 'Read the definition, put each input in its slot, in brackets', size=28)
no28 = I('no28', 'Input, then the operation, then the rest $\\quad$ nested: inside out $\\quad$ no definition: test each choice', size=26)
video('new-operation', 'lesson', slides=[
    S('Defining a New Operation',
      L("Welcome to a new topic, defining a new operation. It's a type of question you probably never met at school. It's "
        "new on the psychometric. But everything you need to solve it, you already know: putting a number in place of a "
        "letter, opening brackets, powers, fractions, and isolating an unknown.")),
    S('A new symbol',
      L("So what is a new operation? You've actually met new operations before, nobody just called them that. Imagine a "
        "little kid who sees three, then a dot, then seven. What is it? The kid has no idea. Not because they can't "
        "multiply, but because nobody told them what the dot means.", show(no1, 'three, then a dot, then seven')),
      L("Once someone explains that the dot means times, it's easy. Three times seven is twenty-one. It was the same with "
        "the plus sign. Until someone told you that plus means adding, it was just a mark. Those were new symbols for "
        "things you already knew how to do."),
      L("And this one really was a new operation: a small two up high, like five with a small two. Someone told you to "
        "multiply the number by itself, so five times five, twenty-five. Then you learned that a small three means: multiply "
        "three copies of the number. So two with a small three is two times two times two, which is eight. Square roots were the same story. A "
        "symbol, a definition, and then you could solve.", show(no2, 'so five times five'), show(no3, 'two times two times two'))),
    S('The heart',
      L("Now I'll teach you a brand-new operation, the heart. What is seven heart three? Right now, nobody can say, "
        "because I haven't told you what the heart does.", show(no4, 'What is seven heart three')),
      L("So let's define it. a heart b means: add a and b, and then multiply the sum by five. a is whatever sits before "
        "the heart, and b is whatever sits after it.", show(nos1['line'], 'a heart b means')),
      L("Seven sits before the heart, so it goes in the place of a. Three sits after it, so it goes in the place of b. "
        "Seven plus three is ten, and ten times five is fifty. So seven heart three is fifty.",
        show(nos1['in'], 'in the place of b'), show(nos1['sum'], 'Seven plus three is ten'),
        show(nos1['calc'], 'is fifty')),
      L("One more. Two heart six. Two goes in the place of a, and six goes in the place of b. Two plus six is eight, and "
        "eight times five is forty.", show(no5, 'Two heart six'), show(no5a, 'six goes in the place of b'),
        show(no5b, 'Two plus six is eight'), show(no5c, 'is forty')),
      L("Careful to follow the whole rule. If you do seven times five, and then add three, you get thirty-eight. That's a "
        "different rule, not the heart. In the heart, the five multiplies the whole sum. That's all a new operation is: a "
        "definition, and then you follow it exactly.", show(no6, 'you get thirty-eight'))),
    S('The same template',
      L("On the exam, they rarely use hearts. Most of the time the symbol is a dollar sign. Sometimes it's a hash, or a "
        "special bracket. In the questions in this course you'll see a diamond. The idea is exactly the same: read the "
        "definition first, and then substitute.", show(no7, 'Most of the time the symbol')),
      L("For example, diamond of a is equal to a squared minus three a. What is diamond of five? Whatever goes into the "
        "diamond takes the place of a, in every spot where a appears. Here a appears in two spots, in a squared and in "
        "three a. So we write the same template again, and put five in both spots.",
        show(nos2['line'], 'diamond of a is equal to'), show(nos2['in'], 'put five in both spots')),
      L("Five squared is twenty-five, and three times five is fifteen. Twenty-five minus fifteen is ten. So diamond of "
        "five is ten.", show(nos2['sq'], 'is twenty-five'), show(nos2['tm'], 'is fifteen'), show(nos2['calc'], 'fifteen is ten')),
      L("Another one, diamond of two. Again, two goes in both spots. Two squared is four, and three times two is six. Four "
        "minus six is negative two.", show(no8, 'two goes in both spots'), show(no8b, 'is six'),
        show(no8c, 'is negative two'))),
    S('Brackets on every input',
      L("On the exam, they often put a negative number, or a whole expression, into the operation. So remember this rule. "
        "Whatever goes in, goes in brackets, every time. Let's take diamond of x equals x squared plus three x. What is "
        "diamond of negative two? Negative two goes in brackets, in both spots.",
        show(nos3['line'], 'diamond of x equals x squared plus'), show(nos3['in'], 'goes in brackets, in both spots')),
      L("The bracket negative two, squared, is positive four, because a negative times a negative is positive. Three times "
        "negative two is negative six. Four minus six is negative two.", show(nos3['calc'], 'Four minus six')),
      L("Here's the trap. Without brackets, negative two squared means the negative of two squared, which is negative "
        "four. That gives a completely different answer. With brackets, it's positive four.", show(no9, "Here's the trap")),
      L("Now a whole expression, x plus two. The whole x plus two goes where x was, in brackets. So diamond of x plus two "
        "is the bracket x plus two, squared, plus three times the bracket x plus two.", show(no10, 'The whole x plus two goes')),
      L("Now open the brackets. The bracket x plus two, squared, is x squared plus four x plus four. Three times the "
        "bracket x plus two is three x plus six, because the three multiplies both parts. Now add the x's together, "
        "and the numbers together. Four x plus three x is seven x, and four plus six is ten. Together, that's x squared plus seven x plus ten.",
        show(no11, 'is x squared plus four x plus four'), show(no11a, 'is three x plus six'),
        show(no11b, 'is seven x'), show(no11c, 'four plus six is ten'), show(no11d, "Together, that's"))),
    S('Inside first, then the definition',
      L("Where does a new operation fit in a longer exercise? First, work out everything inside the operation's own "
        "brackets. Then use the definition, so the operation becomes a plain number. Only then do the rest of the exercise.",
        show(no12, 'First, work out everything')),
      L("Let's say diamond of x is x squared. What is diamond of three plus diamond of four? First turn each diamond into a "
        "plain number. Diamond of three is nine, and diamond of four is sixteen. Then add them. Nine plus sixteen is "
        "twenty-five.", show(no13, 'What is diamond of three plus')),
      L("Careful, we can't join them into diamond of seven. Diamond of seven is forty-nine, a different number. Think of "
        "squares: three squared plus four squared is not seven squared. If you're not sure what comes first, ask yourself "
        "what you would do if it were a square.", show(no14, "we can't join them")),
      L("But when the plus sits inside the diamond's own brackets, like diamond of, in brackets, three plus four, the "
        "brackets come first. Three plus four is seven, and diamond of seven is forty-nine.",
        show(no15, 'when the plus sits inside'))),
    S('Inside out',
      L("When an operation sits inside another operation, we start with the inner brackets and work outwards, just like "
        "brackets inside brackets. Let's say diamond of x is x squared again. What is diamond of diamond of two?",
        show(noc1['line'], 'What is diamond of diamond of two')),
      L("The inner one is diamond of two. Two squared is four. Now four takes the place of the whole inner diamond, so "
        "the outer diamond works on four. Four squared is sixteen.", show(noc1['in'], 'Two squared is four'),
        show(noc1['out'], 'the outer diamond works on four')),
      L("The same with an operation of two numbers. Let's define a new one, the star. a star b is three times the first "
        "number, plus the square of the second.", show(no16, 'a star b is three times')),
      L("What is the bracket one star two, star three? Inner brackets first. One star two is three times one, plus two "
        "squared, so three plus four, seven. Now seven takes its place. Seven star three is three times seven, plus three "
        "squared, so twenty-one plus nine, thirty. The result of the inside becomes the input of the outside.",
        show(no17, 'What is the bracket one star two'), show(no17b, 'One star two is'), show(no17c, 'Now seven takes its place'),
        show(no18, 'Seven star three is'))),
    S('No definition',
      L("Another type: they don't give you the definition at all. They only say that diamond of five is thirty. Someone "
        "took five, used the diamond, and got thirty. That's all you know."),
      L("The operation could be many different things. Six x is one example, because six times five is thirty. Five x "
        "plus five is another, because twenty-five plus five is thirty. So a question like this asks which definition "
        "cannot be the operation.", show(no19, 'Six x is one example'),
        show(no19b, 'Five x plus five is another')),
      L("Your move is to go through the choices and put five into each one. A choice that gives thirty could be the rule. "
        "The one that doesn't give thirty cannot be the rule. For example, x squared plus five gives twenty-five plus "
        "five, thirty, so it could be the rule. But four x plus eight gives twenty plus eight, twenty-eight, so it cannot.",
        show(no20, 'x squared plus five gives'), show(no20b, 'But four x plus eight')),
      L("In the exam, the moment you find the one that doesn't fit, you mark it and move on. In some question videos "
        "we'll check the other choices too, just to learn.")),
    S('The order can matter',
      L("Back to the star: three times the first number, plus the square of the second. Two star four is six plus "
        "sixteen, twenty-two. Four star two is twelve plus four, sixteen. Swap the inputs, and you get a different answer. "
        "So don't assume a new operation behaves like plus, where the order doesn't matter. Before you calculate, check "
        "which number goes into which slot.", show(no21d, 'Back to the star'), show(no21, 'Two star four is'), show(no21b, 'Four star two is')),
      L("A question may ask: is a star b always equal to b star a? To show that it's not always true, one example where it "
        "fails is enough, like two and four.", show(no22, "To show that it's not always true")),
      L("To show that it's always true, numbers are not enough, because they only check some cases. One way is to write "
        "the rule with letters. Remember, the heart adds the two numbers, and then multiplies by five. So b heart a is five "
        "times the bracket b plus a. And b plus a is the same as a plus b, so b heart a is always equal to a heart b. For "
        "the heart, the order never matters. In a multiple-choice question, ruling out the other three choices also works.",
        show(no23, 'write the rule with letters'), show(no23a, 'Remember, the heart adds'), show(no23b, 'So b heart a')),
      L("One warning for order questions: don't test with two equal numbers. Four star four equals four star four for "
        "every operation, so it can't show anything about the order.", show(no24, "don't test with two equal numbers"))),
    S('An unknown input',
      L("And if an input is unknown? Write the definition, and it becomes an ordinary equation. For example, x star four "
        "is twenty-five. By the definition, x star four is three x plus four squared, which is three x plus sixteen. So "
        "three x plus sixteen is equal to twenty-five. Subtract sixteen from both sides, and three x is nine. Divide nine "
        "by three, and x is three.",
        show(no25, 'For example, x star four'), show(no25d, 'By the definition'), show(no25a, 'So three x plus sixteen'),
        show(no25b, 'and three x is nine'), show(no25e, 'and x is three')),
      L("Let's check it. Three times three is nine, and nine plus sixteen is twenty-five. It works. One more: k heart two "
        "is thirty-five. By the definition, that's five times the bracket k plus two. Divide thirty-five by five, and k plus "
        "two is seven. Subtract two from seven, and k is five.", show(no25c, "Let's check it"),
        show(no26, 'k heart two is thirty-five'), show(no26d, 'By the definition'), show(no26a, "that's five times"),
        show(no26b, 'and k plus two is seven'), show(no26c, 'and k is five')),
      L("On the exam you can also work back from the answers: put each choice into the rule, and see which one gives the "
        "result.")),
    S('Recap',
      L("Let's sum up. Read the definition, and put each input in its slot, in brackets.", show(no27, 'Read the definition')),
      L("Work out what's inside each operation, and then turn the operation into a number. Nested operations go from the "
        "inside out. With no definition, test the input in each choice. For order questions, one example can show it's "
        "not always true, and letters can show it's always true. Nothing complicated here, just follow the rule exactly. "
        "[pause] I'll see you in the next video.",
        show(no28, "Work out what's inside"))),
])

# ------------------------------------------------------------------------------------------------ q-541 (Hebrew: lesson 1)
# REMINDER: read the rule, then substitute (camera lesson).  NEW at the step: the same template with the input in EVERY
# slot (SLOT, the Hebrew picture); the trap of a half substitution.  Hebrew: one method; a common-factor method is added.
s541 = SLOT('s541', '◆([[a]]) = [[a]]^2 − 4·[[a]]', [('in', '◆({{6}}) = {{6}}^2 − 4·{{6}}'), ('calc', '= 36 − 24 = 12')])
a3 = IH('a3', '$a^2-4a=a(a-4)$')
a4 = IH('a4', '$\\blacklozenge(6)=6\\cdot(6-4)=6\\cdot2=12$')
video('solve-q-541', 'solution', qid='q-541', slides=[
    S('Method 1 · The math way',
      L("The operation diamond is defined for every number a. Diamond of a is equal to a squared minus four a. Diamond of "
        "six is equal to what?", pt('stem', 'The operation diamond', 'hl', 7.0), voice='calm', pause=0.5),
      L("So we have a rule, and we need to use it on the number six. [short pause] We'll solve it two ways, first by "
        "putting six straight into the rule, and then by simplifying the rule before we use it.", pt('stem', 'use it on the number six')),
      L("[short pause] Remember what the rule means. Whatever goes into the diamond takes the place of a, in every spot "
        "where a appears. Here a appears in two spots, in a squared and in four a. So we write the same template again, "
        "and put six in both spots.", show(s541['line'], 'Whatever goes into the diamond'), show(s541['in'], 'put six in both spots')),
      L("So diamond of six is six squared minus four times six. Six squared is thirty-six. Four times six is twenty-four. "
        "Thirty-six minus twenty-four is twelve.", show(s541['calc'], 'Thirty-six minus twenty-four')),
      L("So diamond of six is twelve, and choice number two is our answer. Careful, thirty-six, choice number one, is what "
        "you get if you put six only into a squared and forget the four a.", mk('tick', 'choice 2', 'choice number two is our answer'),
        pt('s541_in', 'only into a squared'), mk('cross', 'choice 1', 'thirty-six, choice number one'))),
    S('Method 2 · The math way: common factor',
      L("[pause] Another way is to simplify the rule first, and only then put the number in. Both parts of a squared minus "
        "four a have an a in them: a squared is a times a, and four a is a times four. So we can write the whole "
        "expression as a times something. a squared minus four a is a times, in brackets, a minus four. Let's check it. a times a is a squared, and a times negative four is negative four a.",
        show(a3, 'a squared minus four a is a times')),
      L("Now put six in. Six times, in brackets, six minus four. Six minus four is two, and six times two is twelve. Again "
        "twelve, choice number two. [pause] Okay. I'll see you in the next question.", show(a4, 'Now put six in'),
        mk('tick', 'choice 2', 'Again twelve'))),
])

# ------------------------------------------------------------------------------------------------ q-542 (Hebrew: lesson 1)
# REMINDER: nested, inside out (camera lesson).  NEW at the step: the inner value flows into the outer slot (CHAIN, her
# "I coloured it orange" picture); the trap of stopping halfway (25).  Hebrew: one method; algebra is added.
c542 = CHAIN('c542', [('line', '◆([[◆(5)]])'), ('in', '[[◆(5)]] = 5^2 = {{25}}'), ('out', '◆({{25}}) = 25^2 = {{625}}')])
b3 = IH('b3', '$\\blacklozenge(\\blacklozenge(x))=(x^2)^2=x^4$')
b4 = IH('b4', '$5^4=25^2=625$')
video('solve-q-542', 'solution', qid='q-542', slides=[
    S('Method 1 · The math way: inside out',
      L("The operation diamond is defined for every number x. Diamond of x is equal to x squared. Diamond of diamond of five "
        "is equal to what?", pt('stem', 'The operation diamond', 'hl', 7.0), voice='calm', pause=0.5),
      L("So a diamond inside a diamond. The question is which one we do first. [short pause] We'll solve it two ways, from "
        "the inside out, and then with the rule itself.", pt('stem', 'a diamond inside a diamond')),
      L("[short pause] Just like brackets inside brackets, we start with the inner one. The inner one is diamond of five. "
        "The diamond squares its input, so diamond of five is five squared, which is twenty-five.",
        show(c542['line'], 'we start with the inner one'), show(c542['in'], 'so diamond of five is')),
      L("Now twenty-five takes the place of the whole inner diamond. So the outer diamond works on twenty-five. Twenty-five "
        "squared is twenty-five times twenty-five. Twenty times twenty-five is five hundred, and five times twenty-five is "
        "a hundred twenty-five. Together, six hundred twenty-five.", show(c542['out'], 'So the outer diamond works')),
      L("Careful, a lot of students stop after the inner diamond and mark twenty-five. But twenty-five is only halfway, "
        "because the outer diamond still has to work on it. So choice number one is the trap, and choice number three is "
        "our answer.", mk('cross', 'choice 1', 'choice number one is the trap'), mk('tick', 'choice 3', 'choice number three is'))),
    S('Method 2 · Understanding',
      L("[pause] Another way is to write the same two squarings with a power. The first diamond squares the number. The "
        "second diamond squares the result again. So we get x squared, all squared. x squared times x squared is x to the power of "
        "four.", show(b3, 'So we get x squared')),
      L("So we need five to the power of four. Five squared is twenty-five, and twenty-five squared is six hundred "
        "twenty-five. Choice number three again. [pause] Okay. I'll see you in the next question.",
        show(b4, 'five to the power of four'), mk('tick', 'choice 3', 'Choice number three again'))),
])

# ------------------------------------------------------------------------------------------------ q-543 (Hebrew: lesson 1)
# REMINDER: no definition -> put the input into each choice; "cannot be" (camera lesson).  Hebrew: one method, and every
# choice is checked "to learn" - kept, in order, with "in the exam you'd circle it".
c1 = I('c1', 'For example $\\ \\blacklozenge(x)=7x$: $\\ 7\\cdot3=21$', size=28, col=1)
c2 = IH('c2', '(1) $3^3-6=27-6=21$ ✓', size=30)
c3 = IH('c3', '(2) $3\\cdot(3+4)=3\\cdot7=21$ ✓', size=30)
c4 = IH('c4', '(3) $5\\cdot3+5=15+5=20$ ✗', size=30)
c5 = IH('c5', '(4) $8\\cdot3-3=24-3=21$ ✓', size=30)
video('solve-q-543', 'solution', qid='q-543', slides=[
    S('Plugging in the answers',
      L("Given: diamond of three is equal to twenty-one. Which of the following cannot be the definition of the operation "
        "diamond?", pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("This time they don't give us the rule. They only tell us one result. Someone took three, used the diamond, and got "
        "twenty-one. [short pause] We'll put three into the choices, one by one, until one of them doesn't give twenty-one.", pt('stem: g1', 'Someone took three')),
      L("[short pause] Many different rules could turn three into twenty-one. Seven x is one example, because seven times "
        "three is twenty-one. So a choice that gives twenty-one could be the rule, and we can't rule it out. We're looking "
        "for the one choice that does not give twenty-one.", show(c1, 'Seven x is one example')),
      L("Choice number one, x cubed minus six. Three cubed is twenty-seven, and twenty-seven minus six is twenty-one. It "
        "gives twenty-one, so it could be the rule. Choice number one is out.", show(c2, 'Three cubed is'),
        mk('cross', 'choice 1', 'Choice number one is out')),
      L("Choice number two, x times, in brackets, x plus four. Three plus four is seven, and three times seven is "
        "twenty-one. It could be the rule too, so choice number two is out.", show(c3, 'Three plus four is seven'),
        mk('cross', 'choice 2', 'so choice number two is out')),
      L("Choice number three, five x plus five. Five times three is fifteen, and fifteen plus five is twenty. Twenty is not "
        "twenty-one. So this rule cannot turn three into twenty-one, and it cannot be the definition. Choice number three is "
        "our answer.", show(c4, 'Five times three is fifteen'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("In the exam, you'd stop here, because we already found the one that fails. But to learn, let's check the last one "
        "too. Choice number four, eight x minus three. Eight times three is twenty-four, and twenty-four minus three is "
        "twenty-one. So it could be the rule, and only choice number three can't. [pause] Okay. I'll see you in the next "
        "question.", show(c5, 'Eight times three is twenty-four'), mk('cross', 'choice 4', 'So it could be the rule'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t19-01 (added)
# REMINDER: an expression goes in, in brackets (camera lesson).  NEW at the step: the minus goes to both parts of the
# bracket; zero is a lazy test number (two choices tie) -> a second number.  Methods: algebra, plugging in numbers.
s01 = SLOT('s01', '◆([[x]]) = [[x]]^2 − 2·[[x]]', [('in', '◆({{x+1}}) = {{(x+1)}}^2 − 2·{{(x+1)}}'),
                                                   ('calc', '= x^2 + 2x + 1 − 2x − 2'), ('res', '= x^2 − 1')])
e1 = IH('e1', '$x=0$: $\\ \\blacklozenge(1)=1-2=-1$', size=30)
e2 = I('e2', 'Choices: $\\ 1,\\ -1,\\ -1,\\ 3$', size=30)
e3 = IH('e3', '$x=2$: $\\ \\blacklozenge(3)=9-6=3$', size=30)
e4 = I('e4', '(2) $4-1=3$ ✓ $\\quad$ (3) $4-4-1=-1$ ✗', size=30)
video('solve-q-r26-t19-01', 'solution', qid='q-r26-t19-01', slides=[
    S('Method 1 · The math way',
      L("For every number x, diamond of x is equal to x squared minus two x. Diamond of x plus one is equal to what?",
        pt('stem', 'For every number x', 'hl', 6.0), voice='calm', pause=0.5),
      L("This time the input is not a number. It's a whole expression, x plus one. [short pause] We'll solve it two ways, "
        "with algebra, and then by plugging in numbers.", pt('stem', 'a whole expression')),
      L("[short pause] Remember, whatever goes in takes the place of x, and an expression goes in brackets. So we write the "
        "same template, with the whole x plus one, in brackets, in both spots. Diamond of x plus one is the bracket x plus "
        "one, squared, minus two times the bracket x plus one.", show(s01['line'], 'whatever goes in takes the place'),
        show(s01['in'], 'with the whole x plus one')),
      L("Now open the brackets. The bracket x plus one, squared, is x squared plus two x plus one. And minus two times the "
        "bracket x plus one is minus two x minus two. Careful, the minus goes to both parts inside the brackets.",
        show(s01['calc'], 'Now open the brackets')),
      L("Now collect. Two x minus two x is zero, so the x terms cancel. One minus two is negative one. So we get x squared "
        "minus one, and choice number two is our answer.", show(s01['res'], 'So we get x squared'),
        mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers. There are letters in the choices, so I can pick a value for x and "
        "compare. The easiest value is x is zero. Then the input is zero plus one, which is one. Diamond of one is one "
        "squared minus two times one, so one minus two, which is negative one.", show(e1, 'The easiest value')),
      L("Now the choices with x is zero. Choice number one gives one. Choice number two gives negative one. Choice number "
        "three gives negative one too. And choice number four gives three. So choice numbers one and four are out.",
        show(e2, 'Now the choices with'), mk('cross', 'choice 1', 'So choice numbers one'), mk('cross', 'choice 4', 'and four are out')),
      L("Zero was an easy first test, and it already ruled out two choices. But the two choices that are left both give "
        "negative one at zero, so zero can't tell them apart. So we try the next easy value, x is two. Then the input is three. Diamond of three is nine minus six, which is three.",
        show(e3, 'x is two')),
      L("Choice number two gives four minus one, which is three. Choice number three gives four minus four minus one, which "
        "is negative one. So choice number three is out, and choice number two is our answer. [pause] Okay. I'll see you in "
        "the next question.", show(e4, 'gives four minus one'), mk('cross', 'choice 3', 'So choice number three is out'),
        mk('tick', 'choice 2', 'and choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t19-02 (added)
# REMINDER: the order can matter; "not always" = one counterexample, "always" = swap the letters; no equal numbers
# (camera lesson).  Methods: plugging in numbers, algebra.
f1 = I('f1', '$a=1,\\ b=2$ $\\quad$ (not equal numbers)', size=30)
f2 = IH('f2', '(1) $1^2\\cdot2=2$, $\\ 2^2\\cdot1=4$ ✗', size=30)
f3 = IH('f3', '(2) $1\\cdot3=3$, $\\ 2\\cdot3=6$ ✗', size=30)
f4 = IH('f4', '(4) $(1-2)^2+1=2$, $\\ (2-1)^2+2=3$ ✗', size=30)
f5 = I('f5', '(3) $2+1+2=5$, $\\ 2+2+1=5$ ✓', size=30)
g1 = I('g1', '$b\\star a=ba+b+a$', size=34)
g2 = I('g2', '$=ab+a+b=a\\star b$ ✓', size=34)
video('solve-q-r26-t19-02', 'solution', qid='q-r26-t19-02', slides=[
    S('Method 1 · Plugging in numbers',
      L("For which of the following operations is a star b equal to b star a, for all numbers a and b?",
        pt('stem', 'For which', 'hl', 6.0), voice='calm', pause=0.5),
      L("So they ask when the order of the two inputs doesn't matter, for every a and b. [short pause] We'll solve it two "
        "ways, plugging in numbers to knock out choices, and then algebra to prove the one that's left.",
        pt('stem', 'the order of the two inputs')),
      L("[short pause] To show that a rule doesn't always work, one example where it fails is enough. Let's take a is one "
        "and b is two. Why not two equal numbers? Because with equal numbers, swapping them changes nothing, in every rule. "
        "So they can't knock anything out.", show(f1, 'a is one')),
      L("Choice number one, a squared times b. One star two is one squared times two, which is two. Two star one is two "
        "squared times one, which is four. Two is not four, so choice number one is out.", show(f2, 'One star two is one squared'),
        mk('cross', 'choice 1', 'so choice number one is out')),
      L("Choice number two, a times, in brackets, a plus b. One star two is one times three, which is three. Two star one is "
        "two times three, which is six. Out. Choice number four, the bracket a minus b, squared, plus a. One star two: one minus two is negative one, and "
        "negative one squared is one. Then we add a, which is one, so one plus one is two. Two star one: two minus one is "
        "one, and one squared is one. Now a is two, so one plus two is three. Out.", show(f3, 'is one times three'),
        mk('cross', 'choice 2', 'which is six. Out'), show(f4, 'Choice number four, the bracket'), mk('cross', 'choice 4', 'so one plus two is three')),
      L("Choice number three, a b plus a plus b. One star two is two plus one plus two, which is five. Two star one is two "
        "plus two plus one, which is five too. It stays. Three choices are out, so choice number three is our answer.",
        show(f5, 'is two plus one plus two'), mk('tick', 'choice 3', 'so choice number three is our answer'))),
    S('Method 2 · The math way',
      L("[pause] Ruling out the other three already answers the question. Now let's see why choice number three works "
        "for every a and b. One example can't show that, so we swap the letters in the rule itself. b star a means b times a, plus b, plus a.", show(g1, 'b star a means')),
      L("b times a is the same as a times b, and b plus a is the same as a plus b. So b star a is a b plus a plus b, which "
        "is exactly a star b, for every a and b. Choice number three. [pause] Okay. I'll see you in the next question.",
        show(g2, 'So b star a is'), mk('tick', 'choice 3', 'exactly a star b'))),
])

# ------------------------------------------------------------------------------------------------ operation-patterns (lesson)
# NEW: the inverse operation - read the steps, undo them in reverse order (socks and shoes), check with a number, the
# trap (the same order); two examples (2x + 3, 3x - 4).  Only the practice has this type.
h1 = I('h1', '$\\blacklozenge(x)=2x+3$: $\\ \\times2$, then $+3$', size=36)
h2 = I('h2', 'Undo $y$: $\\ -3$, then $\\div2$: $\\ \\frac{y-3}{2}$', size=36)
h3 = I('h3', '$4\\ \\xrightarrow{\\times2}\\ 8$', size=32)
h3b = I('h3b', '$8\\ \\xrightarrow{+3}\\ 11$', size=32)
h3c = I('h3c', '$11\\ \\xrightarrow{-3}\\ 8$', size=32)
h3d = I('h3d', '$8\\ \\xrightarrow{\\div2}\\ 4$ ✓', size=32)
h4 = I('h4', 'Wrong order: $\\ \\frac{11}{2}-3=2.5$ ✗', size=34)
h5 = I('h5', '$\\blacklozenge(x)=3x-4$: $\\ \\times3$, then $-4$', size=30, col=1)
h5b = I('h5b', 'Undo $y$: $\\ +4$, then $\\div3$: $\\ \\frac{y+4}{3}$', size=30, col=1)
h5c = I('h5c', '$5\\ \\xrightarrow{\\times3}\\ 15$', size=30, col=1)
h5d = I('h5d', '$15\\ \\xrightarrow{-4}\\ 11$', size=30, col=1)
h5e = I('h5e', '$11\\ \\xrightarrow{+4}\\ 15$', size=30, col=1)
h5f = I('h5f', '$15\\ \\xrightarrow{\\div3}\\ 5$ ✓', size=30, col=1)
video('operation-patterns', 'lesson', slides=[
    S('Operation Patterns',
      L("Welcome back. Now we move to the more advanced operation questions. Each question that follows shows one type, and "
        "teaches it right there. But first, one type that appears only in the practice, the inverse operation.")),
    S('The inverse operation',
      L("The inverse operation undoes the diamond. You put in the result, and you get the original x back. Let's take "
        "diamond of x equals two x plus three. First, read its steps in order. It multiplies x by two, and then it adds "
        "three.", show(h1, 'The inverse operation undoes')),
      L("Let's call the result y. That's the number that came out of the diamond, and the inverse should give us back the "
        "original x. To undo it, we go backwards. The last step comes off first, like taking off your shoes before your "
        "socks. So first we subtract three from y. Then we divide the result by two. The inverse is y minus three, all "
        "divided by two.", show(h2, 'The last step comes off first')),
      L("Let's check it with a number. Four goes into the diamond. Two times four is eight, and eight plus three is eleven. "
        "Now undo it. Eleven minus three is eight, and eight over two is four. We're back at four, so the inverse works.",
        show(h3, 'Two times four is eight'), show(h3b, 'eight plus three is eleven'), show(h3c, 'Eleven minus three is eight'),
        show(h3d, 'eight over two is four')),
      L("Here's the trap. A lot of students undo the steps in the same order, not backwards. First divide by two, then "
        "subtract three. That's y over two, minus three. With eleven, eleven over two is five point five, and five point "
        "five minus three is two point five. That's not four, so the order matters.", show(h4, "Here's the trap")),
      L("One more example. Diamond of x is three x minus four. Its steps are times three, then minus four. Again, y is "
        "the result we want to undo. So the inverse adds four first. Then it divides the result by three. "
        "That's y plus four, all divided by three. Let's check with five. Three times five is "
        "fifteen, and fifteen minus four is eleven. Eleven plus four is fifteen, and fifteen over three is five. Back to "
        "five.", show(h5, 'Diamond of x is three x minus four'), show(h5b, 'So the inverse adds four first'),
        show(h5c, 'is fifteen'), show(h5d, 'fifteen minus four is eleven'), show(h5e, 'Eleven plus four is fifteen'),
        show(h5f, 'fifteen over three is five')),
      L("So to undo an operation, read its steps, and undo them in reverse order, the last step first. [pause] I'll "
        "see you in the next video.", pt('h5b', 'undo them in reverse order'))),
])

# ------------------------------------------------------------------------------------------------ q-544 (Hebrew: lesson 2)
# NEW: an operation on an expression - match the whole input slot first (14 sits in the 2x slot, so 2x = 14, x = 7);
# the trap 19 (14 straight into x + 5), at the step.  Hebrew: one method; rewriting the rule is added (checked on 6).
s544 = SLOT('s544', '◆([[2x]]) = x + 5', [('in', '◆({{14}})'), ('x', '2x = 14,   x = 7'), ('calc', '◆(14) = 7 + 5 = 12')])
j1 = IH('j1', '$\\blacklozenge(n)=\\frac{n}{2}+5$')
j2 = IH('j2', '$n=6$: $\\ \\frac62+5=8$ ✓', size=30)
j3 = IH('j3', '$\\frac{14}{2}+5=7+5=12$')
video('solve-q-544', 'solution', qid='q-544', slides=[
    S('Method 1 · The math way',
      L("The operation diamond is defined for every number x. Diamond of two x is equal to x plus five. Diamond of fourteen "
        "is equal to what?", pt('stem', 'The operation diamond', 'hl', 7.0), voice='calm', pause=0.5),
      L("Look closely at the rule. The diamond works on two x, not on x. So this is an operation on an expression. [short "
        "pause] We'll solve it two ways, matching the input, and then rewriting the rule for any input.",
        pt('stem', 'The diamond works on two x')),
      L("[short pause] In the rule, the input slot holds two x. In the question, fourteen sits in that same slot. So two x "
        "is fourteen, and x is fourteen divided by two, which is seven.", show(s544['line'], 'the input slot holds two x'),
        show(s544['in'], 'fourteen sits in that same slot'), show(s544['x'], 'So two x is fourteen')),
      L("Now the rule says the output is x plus five. x is seven, so seven plus five is twelve. Diamond of fourteen is "
        "twelve, and choice number one is our answer.", show(s544['calc'], 'seven plus five is twelve'),
        mk('tick', 'choice 1', 'choice number one is our answer')),
      L("Careful, if you put fourteen straight into x plus five, you get nineteen, choice number two. That treats fourteen "
        "as x, but fourteen took the place of two x.", mk('cross', 'choice 2', 'you get nineteen, choice number two'))),
    S('Method 2 · Understanding',
      L("[pause] Another way is to rewrite the rule so it works on any input. Two x goes in, and x plus five comes out. "
        "What does the diamond do to its input? x is half of two x. So the diamond takes half of its input, and then adds "
        "five.", show(j1, 'takes half of its input')),
      L("Let's check this with a number we know. If x is three, the input is six, and the rule gives three plus five, "
        "eight. Half of six is three, and three plus five is eight. It matches.", show(j2, 'Half of six is three')),
      L("Now fourteen. Half of fourteen is seven, and seven plus five is twelve. Choice number one again. [pause] Okay. "
        "I'll see you in the next question.", show(j3, 'Half of fourteen is seven'), mk('tick', 'choice 1', 'Choice number one again'))),
])

# ------------------------------------------------------------------------------------------------ q-545 (Hebrew: lesson 2)
# NEW: a rule with conditions - check odd / even at EVERY step, because the rule can switch (CHAIN, inside out).
# REMINDER: inside out (q-542).  Hebrew: one method.
c545 = CHAIN('c545', [('line', '◆(◆([[◆(1)]]))'), ('r1', '[[◆(1)]]:  1 odd,  4·1 = {{4}}'),
                      ('r2', '◆({{4}}):  4 even,  16 − 9 = {{7}}'), ('r3', '◆({{7}}):  7 odd,  4·7 = {{28}}')])
video('solve-q-545', 'solution', qid='q-545', slides=[
    S('Conditions, inside out',
      L("The operation diamond is defined for every integer x. Diamond of x is four x when x is odd, and x squared minus nine "
        "when x is even. Diamond of diamond of diamond of one is equal to what?", pt('stem', 'The operation diamond', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("This rule has conditions. There's one rule for odd numbers and another for even numbers. And there are three "
        "diamonds. [short pause] So we'll work from the inside out, and before every step, we check whether the input is "
        "odd or even.", pt('stem', 'one rule for odd numbers')),
      L("[short pause] The innermost diamond is diamond of one. One is odd, so we use the odd rule, four x. Four times one "
        "is four.", show(c545['line'], 'The innermost diamond'), show(c545['r1'], 'Four times one is four')),
      L("Now four goes into the middle diamond. Careful, four is even, so the rule switches. We use x squared minus nine. "
        "Four squared is sixteen, and sixteen minus nine is seven.", show(c545['r2'], 'Four squared is sixteen')),
      L("Seven goes into the outer diamond. Seven is odd, so we're back to the odd rule. Four times seven is twenty-eight. "
        "Choice number three is our answer. [pause] Okay. I'll see you in the next question.",
        show(c545['r3'], 'Four times seven'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t19-03 (added)
# NEW: conditions backwards - try both rules, keep an answer only if it fits the rule it came from (8 is even -> out).
# REMINDER: conditions (q-545).  Methods: two cases, plugging in the answers.
l1 = IH('l1', 'Odd: $\\ 3x=24$, $\\ x=8$: $\\ 8$ is even ✗', size=32)
l2 = IH('l2', 'Even: $\\ x^2-12=24$, $\\ x^2=36$, $\\ x=6$ ✓', size=32)
m1 = IH('m1', '(1) $8$ even: $\\ 64-12=52$ ✗', size=32)
m2 = IH('m2', '(2) $6$ even: $\\ 36-12=24$ ✓', size=32)
video('solve-q-r26-t19-03', 'solution', qid='q-r26-t19-03', slides=[
    S('Method 1 · The math way: two cases',
      L("The operation diamond is defined for every positive integer x. Diamond of x is three x when x is odd, and x squared "
        "minus twelve when x is even. Given: diamond of x is equal to twenty-four. x is equal to what?",
        pt('stem', 'The operation diamond', 'hl', 9.0), voice='calm', pause=0.5),
      L("This time it's backwards. They give us the result, twenty-four, and we need the input. And we don't know if x is "
        "odd or even. [short pause] We'll solve it two ways, trying both rules, and then plugging in the answers.",
        pt('stem', 'They give us the result')),
      L("[short pause] Let's try both rules. First the odd rule. Three x is twenty-four, so x is twenty-four divided by "
        "three, which is eight. But wait. Eight is even, and an even number never uses the odd rule. So eight doesn't fit "
        "the rule it came from, and we throw it out.", show(l1, 'First the odd rule')),
      L("Now the even rule. x squared minus twelve is twenty-four. Add twelve to both sides, so x squared is thirty-six. x "
        "is positive, so x is six. And six is even, so it really uses the even rule. It fits.", show(l2, 'Now the even rule')),
      L("So x is six, and choice number two is our answer. Choice numbers one and three keep the eight, which came from the "
        "wrong rule.", mk('tick', 'choice 2', 'choice number two is our answer'), mk('cross', 'choice 1', 'Choice numbers one'),
        mk('cross', 'choice 3', 'and three keep the eight'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. Each choice tells us x, so we first check if it's odd or even, and then use "
        "the right rule. Choice number one is eight. Eight is even, so the even rule. Eight squared is sixty-four, and "
        "sixty-four minus twelve is fifty-two. That's not twenty-four, so eight is out.", show(m1, 'Eight is even'),
        mk('cross', 'choice 1', 'so eight is out')),
      L("Choice number two is six. Six is even, so again the even rule. Six squared is thirty-six, and thirty-six minus "
        "twelve is twenty-four. It works.", show(m2, 'Six is even')),
      L("Choice number three says six or eight, so it claims that both values work. Eight doesn't work, so the whole choice "
        "is wrong, even though six works. And six works, so choice number four, no such x, is out. Choice number two is our "
        "answer. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 3', 'so the whole choice'), mk('cross', 'choice 4', 'no such x, is'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-546 (Hebrew: lesson 2)
# NEW: a circular rule - go down to the start value, then climb back up (CHAIN with up=, her picture).
# Hebrew: one method; the pattern (2, 7, 2, 7) is added as a second method.
c546 = CHAIN('c546', [('line', '◆(6) = 9 − [[◆(4)]]'), ('a', '[[◆(4)]] = 9 − [[◆(2)]]'), ('b', '[[◆(2)]] = 9 − [[◆(0)]]'),
                      ('c', '[[◆(0)]] = {{2}}')], up=[('u1', '7'), ('u2', '2'), ('u3', '7')])
o1 = I('o1', '$x$: $\\ \\ 0,\\ \\ 2,\\ \\ 4,\\ \\ 6,\\ \\ 8$', size=34)
o2 = I('o2', '$\\blacklozenge$: $\\ \\ 2,\\ \\ 7,\\ \\ 2,\\ \\ 7,\\ \\ 2$', size=34)
video('solve-q-546', 'solution', qid='q-546', slides=[
    S('Method 1 · The math way',
      L("The operation diamond is defined for every even integer x that's zero or more. Diamond of x is two when x is zero. "
        "When x is two or more, diamond of x is nine minus diamond of, in brackets, x minus two. Diamond of six is equal to what?",
        pt('stem', 'The operation diamond', 'hl', 9.0), voice='calm', pause=0.5),
      L("This rule uses itself. To find the diamond of a number, we need the diamond of the number two below it. We keep "
        "going down until we reach the given start value, diamond of zero. [short pause] We'll solve it two ways, going down "
        "to the start value and back up, and then with the pattern.", pt('stem', 'This rule uses itself')),
      L("[short pause] Six is two or more, so we use the second rule. The input of the inner diamond is x minus two, so "
        "first six minus two, which is four. So diamond of six is nine minus diamond of four. But we don't know diamond of four yet, so we keep going down.",
        show(c546['line'], 'Diamond of six is nine minus')),
      L("Diamond of four is nine minus diamond of two. And diamond of two is nine minus diamond of zero.",
        show(c546['a'], 'Diamond of four is'), show(c546['b'], 'And diamond of two is')),
      L("Diamond of zero is given, it's two. This is where the chain stops, because now we have a real number.",
        show(c546['c'], 'Diamond of zero is given')),
      L("Now we climb back up. Diamond of two is nine minus two, which is seven. Diamond of four is nine minus seven, which "
        "is two. And diamond of six is nine minus two, which is seven. Choice number four is our answer.",
        show(c546['u1'], 'Diamond of two is nine minus two'), show(c546['u2'], 'Diamond of four is nine minus seven'),
        show(c546['u3'], 'And diamond of six is'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Understanding: the pattern',
      L("[pause] Another way is to look for a pattern. Let's list the values from the start. Diamond of zero is two. Each "
        "next value is nine minus the one before it. Nine minus two is seven. Nine minus seven is two. So the values go "
        "two, seven, two, seven.", show(o1, 'list the values'), show(o2, 'So the values go')),
      L("So zero, four and eight give two, and two and six give seven. Six gives seven, choice number four. And the pattern "
        "also gives big inputs at once. The values come back to two every two steps, and each step adds two to the input. So the value is two again every "
        "time the input grows by four. A hundred is a multiple of four, like zero, four and eight, so diamond of a hundred "
        "is two. [pause] "
        "Okay. I'll see you in the next question.", mk('tick', 'choice 4', 'Six gives seven'))),
])

# ------------------------------------------------------------------------------------------------ q-547 (Hebrew: lesson 2)
# REMINDER: circular rules (q-546).  NEW at the step: each step just passes the question down; the trap 1 (the input
# where the chain stops, not its value).  Hebrew: one method.
c547 = CHAIN('c547', [('line', '◆(7) = [[◆(6)]]'), ('a', '[[◆(6)]] = [[◆(5)]] = … = [[◆(2)]]'), ('b', '[[◆(2)]] = [[◆(1)]]'),
                      ('c', '[[◆(1)]] = {{9}}')])
video('solve-q-547', 'solution', qid='q-547', slides=[
    S('Down to the start',
      L("The operation diamond is defined for every positive integer x. Diamond of x is nine when x is one, and diamond of, in "
        "brackets, x minus one, when x is bigger than one. Diamond of seven is equal to what?", pt('stem', 'The operation diamond', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("This rule uses itself too, like in the last question. [short pause] So we go down to the start value, the same "
        "way as before.", pt('stem', 'This rule uses itself too')),
      L("[short pause] Seven is bigger than one, so we use the second rule. Its input is seven minus one, which is six. So "
        "diamond of seven is diamond of six. Six is bigger than one too, so diamond of six is diamond of five. Each step "
        "just passes the question down to the number below.", show(c547['line'], 'so diamond of seven is'), show(c547['a'], 'so diamond of six is diamond of five')),
      L("We keep going down until we reach diamond of one. Two is still bigger than one, so diamond of two is diamond of "
        "one. But one is not bigger than one, so now the first rule works. Diamond of one is nine.",
        show(c547['b'], 'so diamond of two is'), show(c547['c'], 'Diamond of one is nine')),
      L("On the way down, the rule never adds or subtracts anything from the result. It only says that the diamond of a "
        "number equals the diamond of the number below it. So every diamond on the chain is nine. Diamond of seven is nine, and "
        "choice number four is our answer. Careful, choice number one is a trap. One is the input where the chain stops, "
        "not its value. [pause] Okay. I'll see you in the next question.", mk('tick', 'choice 4', 'choice number four is our answer'),
        mk('cross', 'choice 1', 'choice number one is a trap'))),
])

# ------------------------------------------------------------------------------------------------ q-548 (Hebrew: lesson 2)
# NEW: the operation on both sides - treat it as one unknown (a box) and isolate it.
# Hebrew: one method.  The last substitution uses the same template (SLOT).
q1 = IH('q1', '$5\\blacklozenge(x)-4\\blacklozenge(x)-3x=8$', size=32)
q2 = IH('q2', '$\\blacklozenge(x)-3x=8$', size=32)
q3 = IH('q3', '$\\blacklozenge(x)=3x+8$', size=32)
s548 = SLOT('s548', '◆([[x]]) = 3·[[x]] + 8', [('in', '◆({{4}}) = 3·{{4}} + 8 = 20')], size=32)
video('solve-q-548', 'solution', qid='q-548', slides=[
    S('Isolate the operation',
      L("For every number x, five times diamond of x, minus three x, is equal to eight plus four times diamond of x. Diamond "
        "of four is equal to what?", pt('stem', 'For every number x', 'hl', 7.0), voice='calm', pause=0.5),
      L("Diamond of x appears on both sides of the equation. [short pause] We'll treat diamond of x like an unknown, and isolate it.", pt('stem', 'appears on both sides')),
      L("[short pause] Think of diamond of x as one unknown, like a box. On the left there are five boxes, and on the right "
        "there are four boxes. To get all the boxes on one side, we subtract four boxes from both sides. On the right, the "
        "four boxes are gone, and eight is left. On the left, we have five boxes minus four boxes, minus three x.",
        show(q1, 'subtract four boxes from both sides')),
      L("Five boxes minus four boxes is one box. So diamond of x minus three x is equal to eight. Now add three x to both "
        "sides, and diamond of x is three x plus eight. Now it's an ordinary definition.", show(q2, 'Five boxes minus four boxes'),
        show(q3, 'Now add three x')),
      L("Now put four into the same template. Three times four is twelve, and twelve plus eight is twenty. Choice number two "
        "is our answer. [pause] Okay. I'll see you in the next question.", show(s548['line'], 'Now put four'),
        show(s548['in'], 'Three times four is twelve'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-549 (Hebrew: lesson 2)
# NEW: the operation in every choice -> skip it, finish the section, come back (her tip); algebra can mark at once;
# plugging in x = 1 (one failing example proves "not always"; one answer only).  Hebrew: algebra, plugging in.
r1 = I('r1', 'Looks long? $\\ $you can leave it for the end', size=26, col=1)
r2 = IH('r2', '(1) $(6x)^2=36x^2$ ✓', size=30)
r3 = IH('r3', '(2) $(\\sqrt{x})^2\\cdot(\\sqrt{x})^2=x\\cdot x=x^2$ ✓', size=30)
r4 = IH('r4', '(3) $(5x)^2=25x^2\\ne5x^2$ for $x>0$ ✗', size=30)
r5 = IH('r5', '(4) $(x-7)^2=(7-x)^2$ ✓', size=30)
s1 = I('s1', '$x=1$: $\\ $(1) $36=36$ $\\quad$ (2) $1=1$', size=30)
s2 = I('s2', '(3) $25\\ne5$ ✗', size=30)
video('solve-q-549', 'solution', qid='q-549', slides=[
    S('Method 1 · The math way',
      L("For every number t, diamond of t is equal to t squared. In the choices, x is zero or more. Which of the following "
        "is not always true?", pt('stem', 'For every number t', 'hl', 7.0), voice='calm', pause=0.5),
      L("Before we start, a small tip. Look at the choices. The diamond appears in every choice, and we have to use it "
        "two or three times in each one. That can take time. So in the exam, if a question like this looks long, you can "
        "leave it for later. Solve the rest of the section first, and come back to it at the end. Here in the lesson, "
        "let's solve it. [short pause] We'll solve it in two different ways, with algebra, and then by plugging in a number.",
        pt('choice 1', 'in every choice'), show(r1, 'leave it for later')),
      L("[short pause] Let's start with the math way. With algebra, we write what the diamond does on each side. The diamond squares whatever goes in. "
        "Choice number one. On the left, six x goes in, so we get six x, squared. That's six squared times x squared, "
        "thirty-six x squared. On the right, thirty-six times x squared. Both sides are equal for every x, so this one is "
        "always true, and it's out.", show(r2, 'six x goes in'), mk('cross', 'choice 1', "and it's out")),
      L("Choice number two. Diamond of root x is root x, squared, which is x. So the left side is x times x, which is x "
        "squared. The right side is diamond of x, x squared too. Always true, so it's out.", show(r3, 'Diamond of root x'),
        mk('cross', 'choice 2', "Always true, so it's out")),
      L("Choice number three. On the left, five x, squared, is twenty-five x squared. On the right, five times x squared is "
        "only five x squared. These are equal only when x is zero. For any other x, they're different. So this one is not "
        "always true, and choice number three is our answer.", show(r4, 'is twenty-five x squared'), mk('tick', 'choice 3', 'and choice number three is our answer')),
      L("In the exam you'd circle it and move on. But choice number four teaches something useful. x minus seven and seven "
        "minus x are opposites, and opposites have the same square. So the two sides are always equal.",
        show(r5, 'are opposites'), mk('cross', 'choice 4', 'always equal'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in a number. It's usually faster, because we don't open anything. Let's take x is one, because "
        "it's easy and it's not zero. Zero is allowed too, but zero turns many of these products into zero. Choice number one. Diamond of six is thirty-six, and thirty-six times diamond of one is thirty-six "
        "times one, thirty-six. Equal. Choice number two. Diamond of one is one, and one times one is one. Diamond of one is "
        "one too. Equal.", show(s1, 'take x is one')),
      L("Choice number three. Diamond of five is twenty-five, but five times diamond of one is five times one, which is "
        "five. Twenty-five is not five, so choice number three fails.", show(s2, 'Diamond of five is twenty-five')),
      L("One allowed example where a choice fails proves it's not always true, so we can stop here without checking "
        "choice number four. Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'is our answer, and'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t19-18 (added)
# NEW: a property question - put each rule on trial twice with a test value (2, not 1); the rules that undo themselves
# (c / x, c - x), with the why.  Methods: plugging in numbers, understanding.
t1 = I('t1', '$x=2$: $\\ $(1) $\\ 2,\\ 12,\\ 72$ ✗', size=30)
t1b = I('t1b', '(2) $\\ 2,\\ 8,\\ 14$ ✗', size=30)
t2 = I('t2', '(3) $\\ 2,\\ \\frac13,\\ \\frac1{18}$ ✗', size=30)
t2b = I('t2b', '(4) $\\ 2,\\ 3,\\ 2$ ✓', size=30)
u1 = IH('u1', '$\\frac{6}{6/x}=6\\cdot\\frac{x}{6}=x$', size=34)
u2 = I('u2', '$10-(10-x)=x$, $\\ $but $x=20$: $\\ 10-20<0$ ✗', size=30)
video('solve-q-r26-t19-18', 'solution', qid='q-r26-t19-18', slides=[
    S('Method 1 · Plugging in numbers',
      L("The operation diamond is defined for every positive number x. It is known that for every positive x, diamond of "
        "diamond of x is equal to x. Which of the following can be the definition of the operation diamond?",
        pt('stem', 'The operation diamond', 'hl', 9.0), voice='calm', pause=0.5),
      L("There's no rule here, only a property. Doing the diamond twice brings us back to x. [short pause] We'll solve it "
        "two ways, testing each rule with a number, and then by understanding which rules undo themselves.",
        pt('stem', 'only a property')),
      L("[short pause] For each choice, let's apply the rule twice and see if we get back to where we started. Let's take x "
        "is two. Why two? It's easy to calculate, and it isn't one, because one can stay one under some rules and fool us.",
        pt('stem', 'apply the rule twice')),
      L("Choice number one, six x. Two goes to twelve, and twelve goes to seventy-two. Seventy-two is not two, so choice "
        "number one is out. Choice number two, x plus six. Two goes to eight, and eight goes to fourteen. Not two, out.",
        show(t1, 'Two goes to twelve'), mk('cross', 'choice 1', 'so choice number one is out'), show(t1b, 'Choice number two, x plus six'), mk('cross', 'choice 2', 'Not two, out')),
      L("Choice number three, x over six. Two goes to two sixths, which is one third. And one third over six is one "
        "eighteenth. Not two, out. Choice number four, six over x. Two goes to six over two, which is three. And three goes "
        "to six over three, which is two. We're back at two.", show(t2, 'Two goes to two sixths'),
        mk('cross', 'choice 3', 'eighteenth. Not two, out'), show(t2b, 'Choice number four, six over x')),
      L("One example can't prove always, but the other three are out, so choice number four is our answer.",
        mk('tick', 'choice 4', 'so choice number four is our answer'))),
    S('Method 2 · Understanding',
      L("[pause] Another way is to know which kind of rule undoes itself. Six over x turns a number into six divided by it. "
        "Do it again, and we divide six by six over x. Dividing by a fraction is multiplying by its reciprocal. So six times "
        "x over six, which is x. It always comes back.", show(u1, 'Do it again')),
      L("A rule like ten minus x also comes back when both steps are allowed. Ten minus x, and then ten minus that, is "
        "ten minus ten plus x, which is x. But here the diamond is defined only for positive numbers. With x is twenty, "
        "ten minus twenty is negative ten, and the diamond can't take that. So ten minus x would not work for every "
        "positive x.", show(u2, 'Ten minus x, and then')),
      L("But six x, x plus six and x over six all keep moving the same way. Times six makes a number bigger, and doing it "
        "again makes it even bigger. So they never come back. Choice number four. [pause] Okay. I'll see you in the next "
        "question.", mk('tick', 'choice 4', 'So they never come back'))),
])

# ------------------------------------------------------------------------------------------------ q-550 (Hebrew Q1)
# NEW: an operation of three numbers - each number to the power of the product of the other two (SLOT: the same
# template); the shortcut: read the OUTER diamond first (1, 1, z -> 2 + z; her zero case: (z, 0, 1) -> 2 whatever z is).
# Hebrew: the standard way, the insight.
s550 = SLOT('s550', '◆([[x]], [[y]], [[z]]) = [[x]]^{yz} + [[y]]^{xz} + [[z]]^{xy}',
            [('in', '◆({{2}}, {{1}}, {{4}}) = {{2}}^{1·4} + {{1}}^{2·4} + {{4}}^{2·1}'), ('calc', '= 16 + 1 + 16 = 33')], size=30)
v3 = IH('v3', '$\\blacklozenge(1,1,33)=1+1+33=35$', size=32)
w1 = I('w1', '$\\blacklozenge(1,1,z)=1^{z}+1^{z}+z^{1\\cdot1}=2+z$', size=32)
w2 = IH('w2', '$2+33=35$', size=32)
w3 = IH('w3', '$\\blacklozenge(z,0,1)=z^{0}+0^{z}+1^{0}=1+0+1=2$', size=30)
video('solve-q-550', 'solution', qid='q-550', slides=[
    S('Method 1 · The math way',
      L("For every three numbers x, y and z, diamond of x, y, z is equal to x to the power of the product y z, plus y to "
        "the power of the product x z, plus z to the power of the product x y. Diamond of one, one, and diamond of two, one, four, is equal to what?",
        pt('stem', 'For every three numbers', 'hl', 10.0), voice='calm', pause=0.5),
      L("A new operation of three numbers, but there are only numbers here, no unknowns. [short pause] We'll solve it two "
        "ways, the standard way, and then by simplifying the outer diamond first.", pt('stem', 'only numbers here')),
      L("[short pause] There are two diamonds, so we work from the inside out, like with brackets. The inner one is diamond "
        "of two, one, four. So x is two, y is one, and z is four. Let's write the same template, with these numbers in "
        "their slots.", show(s550['line'], 'The inner one is diamond'), show(s550['in'], 'with these numbers in')),
      L("Each number goes to the power of the product of the other two. For the first part, the power is one times four, "
        "which is four. So two to the power of four, sixteen. For the second part, the power is two times four, which is "
        "eight, and one to any power is one. For the third part, the power is two times one, which is two. So four "
        "squared, sixteen. Sixteen plus one plus sixteen is thirty-three.", show(s550['calc'], 'Sixteen plus one plus sixteen')),
      L("Careful, thirty-three is only the inner diamond, and it's waiting as choice number one. Now the outer diamond, "
        "diamond of one, one, thirty-three. One to any power is one, and that happens twice. And thirty-three goes to the "
        "power of one times one, which is one, so it stays thirty-three. One plus one plus thirty-three is thirty-five. "
        "Choice number three is our answer.", mk('cross', 'choice 1', 'waiting as choice number one'),
        show(v3, 'Now the outer diamond'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Understanding',
      L("[pause] Another way is to simplify the outer diamond first. We still need the inner value, but the outer step "
        "becomes easy. Its first two numbers are one and "
        "one. One to any power is one, so the first two parts are one and one, whatever the inner value is. And the last "
        "part is z to the power of one times one, which is just z. So the outer diamond is always two plus z.",
        show(w1, 'Its first two numbers')),
      L("So we only need the inner value, thirty-three, from the first method's calculation. Two plus thirty-three is "
        "thirty-five, choice number three.", show(w2, 'Two plus thirty-three'), mk('tick', 'choice 3', 'thirty-five, choice number three')),
      L("Sometimes the outer slots make the inner value not matter at all. For example, diamond of z, zero, one, for a "
        "positive z. z to the power of zero is one, zero to a positive power is zero, and one to any power is one. That's "
        "two, whatever z is. [pause] Okay. I'll see you in the next question.", show(w3, 'diamond of z, zero, one'))),
])

# ------------------------------------------------------------------------------------------------ q-551 (Hebrew Q2)
# NEW: two operations in one question - three calculations, inside first (CHAIN); the shortcut: the shortcut formulas
# in the definitions.  REMINDER: (x - y)², (x + y)² (topic 4).  Hebrew: the standard way, the shortcut formulas.
c551 = CHAIN('c551', [('line', '#([[◆(10, 6)]], [[◆(5, 4)]])'), ('r1', '[[◆(10, 6)]] = 100 − 120 + 36 = {{16}}'),
                      ('r2', '[[◆(5, 4)]] = 25 − 40 + 16 = {{1}}'), ('r3', '#({{16}}, {{1}}) = 256 + 32 + 1 = {{289}}')],
             size=30, links=())
y1 = I('y1', '$\\blacklozenge(x,y)=(x-y)^2\\qquad \\#(x,y)=(x+y)^2$', size=32)
y2 = IH('y2', '$(10-6)^2=16 \\qquad (5-4)^2=1$', size=32)
y3 = IH('y3', '$(16+1)^2=17^2=289$', size=32)
video('solve-q-551', 'solution', qid='q-551', slides=[
    S('Method 1 · The math way',
      L("For every two numbers x and y, two operations are defined. Diamond of x, y is x squared minus two x y plus y "
        "squared, and hash of x, y is x squared plus two x y plus y squared. Hash of diamond of ten, six, and diamond of five, "
        "four, is equal to what?", pt('stem', 'For every two numbers', 'hl', 11.0), voice='calm', pause=0.5),
      L("Two operations in one question, the diamond and the hash. [short pause] We'll solve it two ways, the standard way, "
        "and then with the shortcut formulas.", pt('stem', 'Two operations in one question')),
      L("[short pause] Inside the hash there are two diamonds. So we calculate both diamonds first, and then the hash works "
        "on the two results. That's three calculations. The left diamond is diamond of ten and six, so x is ten and y is "
        "six. Ten squared is a hundred. Two times ten times six is a hundred twenty, and it's subtracted. Six squared is "
        "thirty-six. A hundred minus a hundred twenty is negative twenty, plus thirty-six is sixteen.",
        show(c551['line'], 'Inside the hash there are'), show(c551['r1'], 'Ten squared is a hundred')),
      L("The right diamond is diamond of five and four. Five squared is twenty-five. Two times five times four is forty, "
        "subtracted. Four squared is sixteen. Twenty-five minus forty is negative fifteen, plus sixteen is one.",
        show(c551['r2'], 'Five squared is twenty-five')),
      L("So the left diamond gives sixteen, and the right diamond gives one. These two results are the two inputs of the "
        "hash, sixteen first and one second. Now the hash of sixteen and one. Sixteen squared is two hundred fifty-six. Two times sixteen times one is "
        "thirty-two. One squared is one. Two hundred fifty-six plus thirty-two is two hundred eighty-eight, plus one is two "
        "hundred eighty-nine. Choice number two is our answer.", show(c551['r3'], 'Sixteen squared is'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Understanding: shortcut formulas',
      L("[pause] Another way is to recognize the shortcut formulas inside the definitions. x squared minus two x y plus y "
        "squared is the formula for x minus y, all squared. And x squared plus two x y plus y squared is x plus y, all "
        "squared.", show(y1, 'is the formula for')),
      L("So diamond of ten and six is ten minus six, which is four, squared, sixteen. Diamond of five and four is five minus "
        "four, which is one, squared, one.", show(y2, 'is ten minus six')),
      L("And the hash of sixteen and one is sixteen plus one, which is seventeen, squared. Seventeen squared is seventeen "
        "times seventeen. Seventeen times ten is a hundred seventy, and seventeen times seven is a hundred nineteen. "
        "Together, two hundred eighty-nine. Choice number two. [pause] Okay. I'll see you in the next question.",
        show(y3, 'sixteen plus one'), mk('tick', 'choice 2', 'Choice number two.'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t19-05 (added)
# NEW: f(2) - f(-2) for a polynomial: even powers and the constant cancel, odd powers double (why: 8 - (-8) = 16).
# Methods: calculate both, the shortcut.
z1 = IH('z1', '$\\blacklozenge(2)=32+48-16+4+8-7=69$', size=30)
z2 = IH('z2', '$\\blacklozenge(-2)=-32+48+16+4-8-7=21$', size=30)
z3 = IH('z3', '$69-21=48$', size=32)
z4 = I('z4', 'Even powers, the constant: $\\ $cancel', size=30)
z5 = IH('z5', 'Odd powers: $\\ 8-(-8)=16=2\\cdot8$', size=30)
z6 = IH('z6', '$2\\cdot(32-16+8)=2\\cdot24=48$', size=32)
video('solve-q-r26-t19-05', 'solution', qid='q-r26-t19-05', slides=[
    S('Method 1 · The math way',
      L("For every number x, diamond of x is x to the power of five, plus three x to the power of four, minus two x cubed, "
        "plus x squared, plus four x, minus seven. Diamond of two minus diamond of negative two is equal to what?",
        pt('stem', 'For every number x', 'hl', 9.0), voice='calm', pause=0.5),
      L("A long rule, and we need its value at two minus its value at negative two. [short pause] We'll solve it two ways, "
        "calculating both values, and then a shortcut with even and odd powers.", pt('stem', 'A long rule')),
      L("[short pause] Diamond of two first. Two to the power of five is thirty-two. Two to the power of four is sixteen, "
        "and three times sixteen is forty-eight. Two cubed is eight, and two times eight is sixteen, with a minus. Two "
        "squared is four. Four times two is eight. And minus seven. Now add them step by step. Thirty-two plus forty-eight "
        "is eighty. Eighty minus sixteen is sixty-four. Sixty-four plus four is sixty-eight. Sixty-eight plus eight is "
        "seventy-six. Seventy-six minus seven is sixty-nine.", show(z1, 'Diamond of two first')),
      L("Now diamond of negative two. An odd power of a negative number stays negative, and an even power becomes "
        "positive. So negative two to the power of five is negative thirty-two. Negative two to the power of four is "
        "sixteen, and three times sixteen is forty-eight. Negative two cubed is negative eight, and minus two times negative "
        "eight is plus sixteen. Negative two squared is four. Four times negative two is negative eight. And minus seven.",
        show(z2, 'Now diamond of negative two')),
      L("Negative thirty-two plus forty-eight is sixteen. Sixteen plus sixteen is thirty-two. Thirty-two plus four is "
        "thirty-six. Thirty-six minus eight is twenty-eight. Twenty-eight minus seven is twenty-one. So sixty-nine minus "
        "twenty-one is forty-eight. Choice number three is our answer.", show(z3, 'So sixty-nine minus'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Understanding',
      L("[pause] Another way is to compare each term at two and at negative two, instead of calculating everything. An even "
        "power gives the same value for two and for negative two. The plain number, minus seven, is also the same. So in "
        "the subtraction, all of these cancel.", show(z4, 'An even power gives')),
      L("An odd power changes only its sign. For example, two cubed is eight, and negative two cubed is negative eight. "
        "Eight minus negative eight is sixteen, which is twice eight. So every term with an odd power of x counts twice its "
        "value at two.",
        show(z5, 'An odd power changes')),
      L("So we keep only the terms with an odd power of x, and double their values at two. Those terms are x to the power "
        "of five, minus two x cubed, and four x, which has x to the power of one. Their coefficients stay. At two, that's thirty-two minus sixteen plus eight, which is twenty-four. Twice twenty-four is "
        "forty-eight. Choice number three. [pause] Okay. I'll see you in the next question.", show(z6, 'keep only the terms'),
        mk('tick', 'choice 3', 'Choice number three.'))),
])

# ------------------------------------------------------------------------------------------------ q-552 (Hebrew Q3)
# NEW: unknowns in the operation - the slot matters (eight times the FIRST input squared); the root of 9a² is 3a because
# a > 0; all choices are numbers -> one plug-in; some stop at the top (why it's enough).  REMINDER: roots (topic 9).
# Hebrew: the full math, plugging in numbers (her recommended way here).
s552 = SLOT('s552', '◆([[x]], [[y]]) = √(8·[[x]]^2 + [[y]]^2)', [('in', '◆({{a}}, {{a}}) = √(8·{{a}}^2 + {{a}}^2)'),
                                                                  ('calc', '= √(9a^2) = 3a')], size=30)
a6 = IH('a6', 'Top: $\\ \\blacklozenge(3a,a)=\\sqrt{72a^2+a^2}=a\\sqrt{73}$', size=30)
a7 = IH('a7', 'Bottom: $\\ \\blacklozenge(a,3a)=\\sqrt{8a^2+9a^2}=a\\sqrt{17}$', size=30)
a8 = IH('a8', '$\\frac{a\\sqrt{73}}{a\\sqrt{17}}=\\sqrt{\\frac{73}{17}}$', size=34)
b5 = IH('b5', '$a=1$: $\\ \\blacklozenge(1,1)=\\sqrt{9}=3$', size=30)
b6 = IH('b6', 'Top: $\\ \\blacklozenge(3,1)=\\sqrt{72+1}=\\sqrt{73}$', size=30)
b7 = IH('b7', 'Bottom: $\\ \\blacklozenge(1,3)=\\sqrt{8+9}=\\sqrt{17}$', size=30)
video('solve-q-552', 'solution', qid='q-552', slides=[
    S('Method 1 · The math way',
      L("For every two numbers x and y, diamond of x, y is the square root of the whole sum, eight x squared plus y squared. Given: a is "
        "bigger than zero. Diamond of diamond of a, a, and a, over diamond of a, and diamond of a, a, is equal to what?",
        pt('stem', 'For every two numbers', 'hl', 10.0), voice='calm', pause=0.5),
      L("This time there are unknowns inside the operation. And the order of the inputs matters, because only the first one "
        "is multiplied by eight. [short pause] We'll solve it two ways, the full math, and then plugging in a number.",
        pt('stem', 'unknowns inside the operation')),
      L("[short pause] There are four diamonds, but diamond of a, a appears twice, on the top and at the bottom. So we only "
        "need three calculations. Start with diamond of a, a. x is a and y is a. Eight a squared plus a squared is nine a "
        "squared. The root of nine a squared is three a, because a is positive.", show(s552['line'], 'Start with diamond of a, a'),
        show(s552['in'], 'x is a and y is a'), show(s552['calc'], 'The root of nine a squared')),
      L("Now the top, diamond of three a and a. Here three a is in the first slot, so it's the one multiplied by eight. "
        "Three a, squared, is nine a squared, and eight times nine a squared is seventy-two a squared. Plus a squared is "
        "seventy-three a squared. The root is a times root seventy-three.", show(a6, 'Now the top')),
      L("Now the bottom, diamond of a and three a. Now three a is in the second slot, so it's not multiplied by eight. Eight "
        "a squared plus nine a squared is seventeen a squared. The root is a times root seventeen.", show(a7, 'Now the bottom'))),
    S('Method 1 · The math way',
      L("So the fraction is a root seventy-three over a root seventeen. The a's cancel, because a is not zero. Root "
        "seventy-three over root seventeen is the root of seventy-three over seventeen. Choice number three is our answer.",
        show(a8, 'The a\'s cancel'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      sb='Method 1 · The math way'),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in a number. In the full math, the a's cancelled, so the answer doesn't depend on a. So we "
        "can use an easy allowed value. Let's take a is one, the easiest positive number. "
        "Diamond of one and one is the root of eight plus one, root nine, which is three.", show(b5, 'Diamond of one and one')),
      L("The top is diamond of three and one. Three is in the first slot, so eight times three squared. Three squared is "
        "nine, and eight times nine is seventy-two. Plus one squared, one, makes seventy-three. So the top is root "
        "seventy-three.", show(b6, 'The top is diamond of three')),
      L("Careful, the top alone doesn't give the answer. The answer is the whole fraction, top over bottom, so we need the "
        "bottom too. The bottom is diamond of one and three. Now three is in the second slot, so eight times one squared is "
        "eight, plus three squared, nine, which makes seventeen. So the bottom is root seventeen, and the fraction is root "
        "seventy-three over root seventeen, the root of seventy-three over seventeen. That's choice number three. [pause] "
        "Okay. I'll see you in the next question.", show(b7, 'The bottom is diamond of one and three'),
        mk('tick', 'choice 3', "That's choice number three"))),
])

# ------------------------------------------------------------------------------------------------ q-553 (Hebrew Q4)
# NEW: don't open squared brackets early - they may cancel; (a - b)² = (b - a)² (opposites, the same square); dividing by a
# fraction flips it; check the choices differ before plugging in.  Hebrew: the full math, the insight, plugging in.
c5a = IH('c5a', 'Top: $\\ \\frac{(a-b)^2}{ab^3}$', size=30, col=1)
c5b = IH('c5b', 'Bottom: $\\ \\frac{(b-a)^2}{ba^3}$', size=30, col=1)
c5 = IH('c5', '$\\frac{(a-b)^2}{ab^3}\\cdot\\frac{ba^3}{(b-a)^2}$', size=32)
c6 = IH('c6', '$=\\frac{ba^3}{ab^3}=\\frac{a^2}{b^2}$', size=32)
d5 = IH('d5', '$(a-b)^2=(b-a)^2$', size=32)
d6 = IH('d6', '$\\frac{ba^3}{ab^3}=\\frac{a^2}{b^2}$', size=32)
e5 = IH('e5', '$a=1,\\ b=2$: $\\ 1,\\ \\frac{1}{2},\\ \\frac{1}{4},\\ 4$ $\\ $(all different)', size=30)
e6 = IH('e6', '$\\blacklozenge(1,2)=\\frac{1}{1\\cdot8}=\\frac18 \\qquad \\blacklozenge(2,1)=\\frac{1}{2\\cdot1}=\\frac12$', size=30)
e7 = IH('e7', '$\\frac18\\div\\frac12=\\frac18\\cdot2=\\frac14$', size=32)
video('solve-q-553', 'solution', qid='q-553', slides=[
    S('Method 1 · The math way',
      L("For every two numbers x and y that are not zero, diamond of x, y is x minus y, squared, over x times y cubed. Given: "
        "a and b are two different numbers, and neither of them is zero. Diamond of a, b over diamond of b, a is equal to "
        "what?", pt('stem', 'For every two numbers', 'hl', 11.0), voice='calm', pause=0.5),
      L("The same two letters go into the diamond on the top and at the bottom, only in a different order. [short pause] "
        "We'll solve it three ways, the math way, by understanding the definition, and by plugging in numbers.",
        pt('stem', 'only in a different')),
      L("[short pause] The math way first. The top is diamond of a, b, so x is a and y is b. That's a minus b, squared, over a times b cubed. "
        "The bottom is diamond of b, a, so now x is b and y is a. That's b minus a, squared, over b times a cubed.",
        show(c5a, 'The top is diamond of a, b'), show(c5b, 'The bottom is diamond of b, a')),
      L("To divide by a fraction, we multiply by its reciprocal. So we flip the bottom fraction and multiply. And a tip, "
        "don't open the squared brackets yet, because they might cancel. And they do. a minus b and b minus a are "
        "opposites, and opposites have the same square. And a and b are different, so that square is not zero. So the "
        "squared parts cancel.", show(c5, 'So we flip the bottom')),
      L("We're left with b times a cubed, over a times b cubed. One a cancels from a cubed, which leaves a squared on top. "
        "One b cancels from b cubed, which leaves b squared at the bottom. So the answer is a squared over b squared. Choice "
        "number three is our answer.", show(c6, "We're left with"), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Understanding',
      L("[pause] Now by understanding. We read the definition before calculating. The top and the bottom use the same two numbers, "
        "just swapped. The squared part is x minus y. Swapping x and y gives the opposite number inside, but the square is "
        "the same. So both fractions have the same top. When we divide one fraction by another with the same nonzero top, "
        "that top cancels.", show(d5, 'but the square is the same')),
      L("So only the two denominators matter. The first fraction has a times b cubed, where b, its second input, is "
        "cubed. The second has b times a cubed, where a is cubed. These are not always equal, so they don't cancel. When "
        "we divide by the second fraction, its denominator, b a cubed, goes to the top. So we get b a cubed over a b cubed. One "
        "a and one b cancel, and we get a squared over b squared. Choice number three.", show(d6, 'so we get b a cubed'),
        mk('tick', 'choice 3', 'a squared over b squared. Choice'))),
    S('Method 3 · Plugging in numbers',
      L("[pause] And plugging in numbers. a and b must be different, and neither can be zero. So let's take a is one and b "
        "is two. First, check that the choices come out different. One, one half, one quarter and four. All different, so "
        "one plug-in is enough.", show(e5, 'a is one and b')),
      L("The top is diamond of one and two. One minus two is negative one, and squared that's one. Below it, one times two "
        "cubed is eight. So the top is one eighth. The bottom is diamond of two and one. Two minus one is one, squared one. "
        "Below it, two times one cubed is two. So the bottom is one half.", show(e6, 'The top is diamond of one and two')),
      L("One eighth divided by one half is one eighth times two, which is one quarter. That's choice number three. [pause] "
        "Okay. I'll see you in the next question.", show(e7, 'One eighth divided by'), mk('tick', 'choice 3', "That's choice number three"))),
])

# ------------------------------------------------------------------------------------------------ q-554 (Hebrew Q5)
# NEW: an operation on digits (two topics in one; SLOT: each digit into its own slot); the shortcut: the biggest power
# needs the smallest digit (min / max).  Hebrew: the standard way, the insight.
s554 = SLOT('s554', '◆([[A]][[B]][[C]]) = [[A]]^4 + [[B]]^3 + [[C]]^2', [('in', '◆({{2}}{{1}}{{4}}) = {{2}}^4 + {{1}}^3 + {{4}}^2'),
                                                                     ('calc', '= 16 + 1 + 16 = 33')], size=30)
f6 = IH('f6', '(2) $1+64+4=69$ ✗', size=30)
f7 = I('f7', '(3) $4^4=256$, already too big ✗', size=30)
f8 = IH('f8', '(4) $1+8+16=25$ ✓', size=30)
g5a = IH('g5a', '$4^2=16$, $\\ 4^4=256$', size=28)
g5 = I('g5', 'Power $4$ on the hundreds: $\\ $the smallest digit, $1$', size=28)
g6a = IH('g6a', '$4^3=64$, $\\ 4^2=16$', size=28)
g6b = IH('g6b', '$2^3=8$, $\\ 2^2=4$', size=28)
g6 = I('g6', 'Power $3$ on the tens: $\\ 2$, not $4$: $\\ 124$', size=28)
video('solve-q-554', 'solution', qid='q-554', slides=[
    S('Method 1 · The math way',
      L("A, B and C are digits from one to nine. For every three-digit number A B C, the operation diamond is defined. "
        "Diamond of A B C is A to the power of four, plus B cubed, plus C squared. Which of the following is the smallest?",
        pt('stem', 'A, B and C', 'hl', 9.0), voice='calm', pause=0.5),
      L("Two topics in one question, digits and a new operation. And the diamond is in every choice, so we have to work out "
        "the choices. [short pause] We'll solve it two ways, the math way, calculating each choice, and then by "
        "understanding where the biggest power goes.", pt('stem', 'Two topics in one question')),
      L("[short pause] The hundreds digit goes to the power of four, the tens digit is cubed, and the units digit is "
        "squared. Choice number one, two one four. Two to the power of four is sixteen. One cubed is one. Four squared is "
        "sixteen. Sixteen plus one plus sixteen is thirty-three.", show(s554['line'], 'The hundreds digit goes'),
        show(s554['in'], 'Choice number one, two one four'), show(s554['calc'], 'Sixteen plus one plus sixteen')),
      L("Choice number two, one four two. One to the power of four is one. Four cubed is sixty-four. Two squared is four. "
        "One plus sixty-four plus four is sixty-nine. That's bigger than thirty-three, so choice number two is out.",
        show(f6, 'One plus sixty-four'), mk('cross', 'choice 2', 'so choice number two is out')),
      L("Choice number three, four one two. Four to the power of four is two hundred fifty-six. That's already much bigger "
        "than thirty-three, so we don't need the rest. Out.", show(f7, 'Four to the power of four'), mk('cross', 'choice 3', "the rest. Out")),
      L("Choice number four, one two four. One to the power of four is one, two cubed is eight, and four squared is "
        "sixteen. One plus eight plus sixteen is twenty-five. Twenty-five is smaller than thirty-three, so choice number one "
        "is out too, and choice number four is our answer.", show(f8, 'One plus eight plus sixteen'),
        mk('cross', 'choice 1', 'so choice number one'), mk('tick', 'choice 4', 'and choice number four is our answer'))),
    S('Method 2 · Understanding',
      L("[pause] Now by understanding. Let's think about the powers. Every choice uses the same three digits, one, two and four. "
        "One stays one at any power, so giving it the biggest power costs nothing. But four grows a lot. Four squared is "
        "sixteen, and four to the power of four is two hundred fifty-six. So the fourth power, on the hundreds digit, "
        "should go to the one. Choice numbers one and three start with two and four, so they're out.",
        show(g5a, 'Four squared is'),
        show(g5, 'should go to the one'), mk('cross', 'choice 1', 'Choice numbers one and three'),
        mk('cross', 'choice 3', "so they're out")),
      L("Between one four two and one two four, look at the next power, the cube, on the tens digit. Four cubed is "
        "sixty-four, but four squared is only sixteen. Two changes much less, from eight to four. So the four should get "
        "the square, and the two goes in the tens. One two four, choice number four. [pause] Okay. I'll see you in the next "
        "question.", show(g6a, 'Four cubed is'), show(g6b, 'from eight to four'), show(g6, 'So the four should get'),
        mk('tick', 'choice 4', 'One two four, choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-555 (Hebrew Q6)
# NEW: "must be true for all positive a, b" - break each choice; with algebra (multiply by a positive: no flip) and by
# understanding (3/x = 3 times the reciprocal; a bigger denominator, a smaller fraction).  Hebrew: both, choice by
# choice -> two methods here; the wrong choices first, so each method ends on the answer.
h6 = IH('h6', '(1) $\\frac{3}{a}<3\\ \\to\\ 1<a$: $\\ a=\\frac{1}{2}$: $\\ 6$ ✗', size=30)
h7 = IH('h7', '(3) $\\frac3a\\cdot\\frac b3=\\frac ba$ ✗', size=30)
h8 = IH('h8', '(4) $\\frac3a<\\frac3{a+1}$', size=30)
h8b = IH('h8b', '$3(a+1)<3a$', size=30)
h8c = IH('h8c', '$a+1<a$', size=30)
h8d = IH('h8d', '$1<0$ ✗', size=30)
h9 = IH('h9', '(2) $\\frac3a\\cdot a=3=\\frac3b\\cdot b$ ✓', size=30)
i6 = IH('i6', '(1) $a=2$: $\\ \\frac{3}{2}<3$ ✓', size=28)
i6b = IH('i6b', '$a=1$: $\\ \\frac31=3$, not $<3$ ✗', size=28)
i7 = I('i7', '(3) $\\div\\frac3b=\\times\\frac b3$: $\\ \\frac ba$ ✗', size=28)
i8 = I('i8', '(4) bigger denominator, smaller fraction ✗', size=28)
i9 = I('i9', '(2) a number times its reciprocal is $1$: $\\ 3\\cdot1=3$ ✓', size=28)
video('solve-q-555', 'solution', qid='q-555', slides=[
    S('Method 1 · The math way',
      L("For every number x that's not zero, diamond of x is three over x. Which of the following must be true for all "
        "positive a and b?", pt('stem', 'For every number x', 'hl', 6.0), voice='calm', pause=0.5),
      L("Must be true means true for every positive a and b. So for each choice, we test whether it works for every "
        "positive a and b, and one allowed pair where it fails rules it out. [short pause] We'll solve it two ways, the "
        "math way, with algebra on each inequality or equation, and then by understanding what the diamond does.", pt('stem', 'Must be true means')),
      L("[short pause] Let's start with the math way. Choice number one says three over a is smaller than three. a is positive, "
        "so we can multiply both sides by a without flipping the sign. We get three is smaller than three a. Divide both "
        "sides by three, and one is smaller than a. That's true only when a is bigger than one. But a could be one half. "
        "Then three over one half is six, and six is not smaller than three. So choice number one is out.",
        show(h6, 'Choice number one says'), mk('cross', 'choice 1', 'So choice number one is out')),
      L("Choice number three. Three over a, divided by three over b. To divide by a fraction, multiply by its reciprocal. "
        "Three over a times b over three. The threes cancel, and we get b over a. The choice says a over b, and b over a "
        "equals a over b only when a and b are equal. For example, a is one and b is two. Then b over a is two, but a over "
        "b is one half. So it's not true for every positive a and b, and choice number three is out.", show(h7, 'Choice number three. Three over a'), mk('cross', 'choice 3', 'and choice number three is out'))),
    S('Method 1 · The math way',
      L("Choice number four says three over a is smaller than three over, in brackets, a plus one. The whole a plus one "
        "is the bottom of that fraction. Both bottoms are positive, so we can "
        "multiply both sides by a and by a plus one without flipping. We get three times, in brackets, a plus one, is "
        "smaller than three a. Divide by three, and a plus one is smaller than a. Take a off both sides, and one is smaller "
        "than zero. That's never true. So choice number four is out.", show(h8, 'Choice number four says'),
        show(h8b, 'We get three times'), show(h8c, 'and a plus one is smaller than a'), show(h8d, 'and one is smaller than zero'),
        mk('cross', 'choice 4', 'So choice number four is out')),
      L("Choice number two. Three over a, times a. The a cancels, and we get three. And three over b, times b, is three "
        "too. Three equals three for every a and b. So choice number two must be true, and it's our answer.",
        show(h9, 'Choice number two. Three over a'), mk('tick', 'choice 2', "and it's our answer")),
      sb='Method 1 · The math way'),
    S('Method 2 · Understanding',
      L("[pause] Now by understanding. Three over x means three divided by x. Choice number one. For a bigger than one it "
        "works. Three over two is smaller than three. But for a equal to one, we get three, which isn't smaller than three. "
        "So not always.", show(i6, 'For a bigger than one'),
        show(i6b, 'But for a equal to one')),
      L("Choice number three. Dividing by three over b is like multiplying by b over three. So the a ends up at the bottom "
        "and the b on top, b over a. That's a over b only when a equals b. For example, a is one and b is two. Then b over "
        "a is two, but a over b is one half. So not always.", show(i7, 'Dividing by three over b')),
      L("Choice number four. Both fractions have the same positive top, three, and positive bottoms. With the same "
        "positive top, a bigger denominator makes a smaller fraction. a plus one is bigger than a, so three over the whole "
        "a plus one is smaller than three over a. That's the opposite of what the choice says, so it's never true.",
        show(i8, 'A bigger denominator')),
      L("Choice number two. Three over a is three times one over a, and one over a is the reciprocal of a. A number times "
        "its reciprocal is one. So three over a, times a, is three times one, three, for every a. The same for b. So it's "
        "always three equals three, choice number two. [pause] Okay. I'll see you in the next question.",
        show(i9, 'A number times its reciprocal'), mk('tick', 'choice 2', 'always three equals three'))),
])

# ------------------------------------------------------------------------------------------------ q-556 (Hebrew Q7)
# NEW: a definition in words - see it in numbers first (50, 75, 7); x = 1 knocks out three; why: times 5 adds exactly one
# five, squaring doubles the count, adding 5 says nothing (x = 125: 4 fives, not 15).  REMINDER: prime factors (14).
# Hebrew: plugging in numbers, understanding.
j5 = IH('j5', '$50=2\\cdot5\\cdot5$: $\\ 2 \\qquad 75=3\\cdot5\\cdot5$: $\\ 2 \\qquad 7$: $\\ 0$', size=30)
j6 = I('j6', '$x=1$: $\\ $⟦$1$⟧ $=0$', size=30)
j6a = I('j6a', '(1) ⟦$5$⟧ $=1$, $\\ $⟦$1^2$⟧ $=0$', size=30)
j6b = I('j6b', '(2) ⟦$6$⟧ $=0$, $\\ $⟦$1$⟧ $+1=1$', size=30)
j6c = I('j6c', '(3) ⟦$5$⟧ $=1$, $\\ 5\\cdot$⟦$1$⟧ $=0$', size=30)
j7 = I('j7', '(4) ⟦$5$⟧ $=1$, $\\ $⟦$1$⟧ $+1=1$ ✓', size=30)
k5 = IH('k5', '$\\times5$: $\\ $one more five $\\quad 50\\to250$: $\\ 2\\to3$', size=30)
video('solve-q-556', 'solution', qid='q-556', slides=[
    S('Method 1 · Plugging in numbers',
      L("For every positive integer x, the double bracket of x is the number of times five appears in the prime "
        "factorization of x. For example, fifty is two times five times five, it has two fives, so the double bracket of "
        "fifty is two. Which of the following must be true?", pt('stem', 'For every positive integer x', 'hl', 11.0), voice='calm', pause=0.5),
      L("This question mixes a new operation with prime factors. [short pause] We'll solve it two ways, plugging in a "
        "number, and then by understanding.", pt('stem', 'mixes a new operation')),
      L("[short pause] A definition in words is easy to misread, so let's see it in numbers first. Fifty is two times five "
        "times five, so it has two fives. Seventy-five is three times five times five, two fives as well. And seven has no "
        "fives at all, so its count is zero.", show(j5, "let's see it in numbers")),
      L("Now let's plug in the simplest value, x is one. One has no fives, so its count is zero. Choice number one. Five "
        "times one is five, which has one five. One squared is one, with no fives. One is not zero, so choice number one is "
        "out. Choice number two. One plus five is six, and six is two times three, no fives, so zero. On the right, zero "
        "plus one is one. Zero is not one, out. Choice number three. Five has one five, but five times zero is zero. One is "
        "not zero, out.", show(j6, 'One has no fives'), show(j6a, 'with no fives'), mk('cross', 'choice 1', 'so choice number one is'),
        show(j6b, 'zero plus one is one'),
        mk('cross', 'choice 2', 'Zero is not one, out'), show(j6c, 'five times zero is zero'), mk('cross', 'choice 3', 'not zero, out')),
      L("Choice number four. Five has one five, and zero plus one is one. One equals one. Three choices are out, so choice "
        "number four is our answer.", show(j7, 'One equals one'), mk('tick', 'choice 4', 'number four is our answer'))),
    S('Method 2 · Understanding',
      L("[pause] Now by understanding. Let's see why it's always true. When we multiply x by five, we add exactly one more five to its prime "
        "factors, whatever x is. So the count of fives goes up by exactly one. That's choice number four, for every x. For "
        "example, fifty has two fives, and two hundred fifty has three.", show(k5, 'we add exactly one more five'),
        mk('tick', 'choice 4', "That's choice number four")),
      L("The others are not always true, and x is one already showed that. So choice number four is our answer, and I'll "
        "see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ r26-t19-summary
# REMINDERS only, said the way they were taught, with new numbers; the same template (SLOT) for substitution.
s1s = SLOT('s1s', '◆([[x]]) = [[x]]^2 − 5·[[x]]', [('in', '◆({{−2}}) = {{(−2)}}^2 − 5·{{(−2)}} = 4 + 10 = 14')], size=30)
s2s = I('s2s', '$a\\heartsuit b=3(a+b)$: $\\ 4\\heartsuit2=18$ $\\quad 2\\star5\\ne5\\star2$?', size=30)
s3s = I('s3s', 'Operation first $\\quad$ nested: inside out', size=30)
s4s = I('s4s', '$F(4t)=t+3$: $\\ F(20)$: $\\ 4t=20$, $\\ t=5$, $\\ 8$', size=30)
s5s = I('s5s', 'Rule missing: test each candidate (twice for a property) $\\quad$ unknown input: an equation', size=26)
s6s = I('s6s', 'Conditions: which rule, at every step $\\quad$ backwards: does it fit?', size=28)
s7s = I('s7s', 'Uses itself: down to the start, back up $\\quad$ both sides: isolate', size=28)
s8s = I('s8s', 'Not always: one failing example $\\quad$ always: algebra (order: swap the letters)', size=26)
s9s = I('s9s', 'Undo themselves where defined: $\\ \\frac cx,\\ c-x$ $\\quad$ inverse: reverse order', size=28)
s10s = I('s10s', '$\\blacklozenge(k)-\\blacklozenge(-k)$: $\\ $odd powers, doubled $\\quad$ shortcut formulas', size=28)
video('r26-t19-summary', 'lesson', slides=[
    S('Defining a New Operation: Summary',
      L("Before you practice, here's a quick summary of the topic. How to read a definition, the types of questions, and the "
        "shortcuts.")),
    S('Read, then substitute',
      L("A new operation is just a definition. Read it, and then follow the whole rule. Whatever goes in takes the place of "
        "the letter, in every spot, and in brackets. Diamond of x is x squared minus five x. So diamond of negative two is "
        "negative two, squared, minus five times negative two. That's four plus ten, which is fourteen.",
        show(s1s['line'], 'A new operation is just'), show(s1s['in'], 'So diamond of negative two')),
      L("Read which input goes in which slot. a heart b is three times, in brackets, a plus b, so four heart two is three "
        "times six, eighteen. And the order can matter, so don't assume that two star five is five star two.",
        show(s2s, 'Read which input')),
      L("Inside a longer exercise, turn each operation into a number first. And nested operations go from the inside out. "
        "The inner result becomes the outer input, so don't stop halfway.", show(s3s, 'turn each operation'))),
    S('The types',
      L("When the operation works on an expression, match the whole input first. F of four t is t plus three. For F of twenty, "
        "four t is twenty, so t is five, and the answer is five plus three, eight.", show(s4s, 'Match the whole input')),
      L("When an input and its result are given but the rule is missing, put that input into each candidate rule. When "
        "only a property is given, like doing the diamond twice brings back x, apply each candidate twice. And when the "
        "input is unknown, write the definition, and it's an ordinary equation.", show(s5s, 'the rule is missing')),
      L("When the rule has conditions, check which rule to use at every step, because the input changes. When we go "
        "backwards, from the result to the input, try every rule, and keep an answer only if it fits the rule it came "
        "from.", show(s6s, 'When the rule has conditions')),
      L("When the rule uses itself, go down to the start value, then climb back up. When the operation is on both sides of "
        "an equation, treat it as one unknown and isolate it.", show(s7s, 'When the rule uses itself'))),
    S('Always, must, shortcuts',
      L("When the question asks what is not always true, one allowed example where a choice fails is enough. When it asks "
        "what must be true, a failing example rules a choice out, and when all the other choices are out, the one that's "
        "left is the answer. So plug in an easy allowed value, check the "
        "choices right away, and use another value only if more than one choice is left. To see why a rule always works, "
        "use algebra, and when the question is about the order of the inputs, swap the letters. And skip a question only if "
        "its calculation would really take long.", show(s8s, 'what is not always true')),
      L("Some rules undo themselves, as long as every step stays where the operation is defined. Six over x does, for "
        "positive x. Ten minus x comes back too, but not for every positive x, because ten minus twenty is negative. And an "
        "inverse operation undoes the steps in reverse order.", show(s9s, 'Some rules undo themselves')),
      L("A value minus its value at the opposite number? The terms with even powers of x and the plain number cancel, and "
        "the terms with odd powers of x double. And look for "
        "the shortcut formulas inside a definition. [pause] That's it. Now go practice, and I'll see you in the next video.",
        show(s10s, 'A value minus its value'))),
])

# carry-over boxes on the continuation slides (V2): the next step uses these results
CARRY19 = {'solve-q-552': {1: ['Top: $a\\sqrt{73}$', 'Bottom: $a\\sqrt{17}$']},
           'solve-q-555': {1: ['(1), (3) out']}}

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
 "q-543": "Given: $\\blacklozenge(3)=21$. Which of the following cannot be the definition of the operation $\\blacklozenge$?"
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
CP.split(globals(), 'new-operation', 'Defining a New Operation', [(1, None), (4, "Let's continue with new operations, and see what to watch out for when we use them."), (7, "Let's continue with new operations, and look at a few more question types.")])
for _v in ('new-operation', 'new-operation-2'):   # batch A shared fix 4 (W16): no "Okay." before the goodbye (unrecorded parts)
    _ln = VIDEOS[_v]['slides'][-1]['lines'][-1]; _ln['say'] = _ln['say'].replace(" [pause] Okay. I'll see you in the next part.", " [pause] I'll see you in the next part.")

for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _stem_parts(_v); _write_gap(_v)



# 2026-10-13 carry-over boxes (V2) and the layer-order check (V1): after the visual passes, like topics 13-18
import types as _types
MV.carry(_types.SimpleNamespace(**globals()), CARRY19)
MV.calm(_types.SimpleNamespace(**globals()))     # 2026-10-13 steady highlights (visual only)
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
