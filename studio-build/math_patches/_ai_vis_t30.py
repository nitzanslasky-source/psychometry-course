"""Topic 30 (Lines and Angles) - the scripts for the teacher's own-voice reading (2026-10-14), written from the first draft to
the Codex review standard, the clarity style, the method visuals (geometry: the angle figure built in layers, GEO below), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py / _ai_vis_t16.py / _ai_vis_t17.py / _ai_vis_t18.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The camera lesson 'geo-001' gets its own reading script here too, in parts of about 3-4 minutes (2026-10-14: she reads it
with the camera on). Every other topic-30 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t30.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t30.py ai_redo_t30() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods and EVERY method of the Hebrew solution (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-30-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t30ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-30 flow order of the scripts
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
CAM_BASE = 'geo-001'
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
            'style': "the teacher reads it herself (Reading Studio), topic-30 scripts (2026-10-14): math_patches/_ai_vis_t30.py is "
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


# ------------------------------------------------------------------------------------------- topic-30 geometry figures (V1)
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



CARRY30 = {}       # carry-over boxes (V2): {vid: {slide index: [tex, ...]}}, filled by the scripts


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


# ------------------------------------------------------------------------------------------------ geo-001 (camera lesson, in parts)
# 2026-10-14 her camera first lesson of geometry as a reading script (same style, handwriting, camera on), with more examples,
# split into parts of about 3-4 minutes (CAMERA_SPLIT at the end). Hebrew: geo 14-125 (every definition and rule kept);
# English additions kept: segments on a line (count the gaps), parallel or not (three rules, not to scale), the recap.
# Study plan: day 1, right after topic 1 - self-contained (no triangles, no plugging in).
# Visuals (V3): every figure is built step by step; small angles teal, large angles orange; a straight angle or a Z / U is
# traced while she names it; a focus step fades the figure and redraws only what is needed (the old highlight goes).


def _g1ray(cx, cy, deg, r):
    x, y = gpt(cx, cy, r, deg)
    return ('seg', cx, cy, x, y)


def _g1line(cx, cy, deg, r1, r2=None):
    r2 = r1 if r2 is None else r2
    (x1, y1), (x2, y2) = gpt(cx, cy, r1, deg + 180), gpt(cx, cy, r2, deg)
    return ('seg', x1, y1, x2, y2)


def _g1arr(x, y, deg):
    """a small arrowhead at (x, y) pointing in direction deg (a line that goes on forever)"""
    (ax, ay), (bx, by) = gpt(x, y, 16, deg + 152), gpt(x, y, 16, deg - 152)
    return [('seg', ax, ay, x, y, 'ink', 3), ('seg', bx, by, x, y, 'ink', 3)]


# ---- slide: a line and a segment
G1A = GEO('g1a', [
    ('line', [('dot', 220, 120, 'A'), ('dot', 420, 120, 'B')]),
    ('ln', [('seg', 50, 120, 590, 120)] + _g1arr(590, 120, 0) + _g1arr(50, 120, 180)),
    ('bent', [('path', [(220, 120), (320, 60), (420, 120)], 'red', 4), ('txt', 320, 40, 'not straight', 'red', 22)]),
    ('seg', [('dot', 220, 230, 'C', 0, 26), ('dot', 420, 230, 'D', 0, 26), ('seg', 220, 230, 420, 230, 'teal', 5),
             ('txt', 320, 205, 'segment CD', 'teal', 22)]),
], vb='0 20 640 250', w=900, col=0, title='A line through two points, and a segment')
# ---- slide: segments on a line
_P5 = [110, 215, 320, 425, 530]
G1B = GEO('g1b', [
    ('line', [('seg', 60, 90, 580, 90)] + [('dot', x, 90) for x in _P5]),
    ('pts', [('txt', x, 125, str(i + 1), 'ink', 22) for i, x in enumerate(_P5)]),
    ('gaps', [('arc', (a + b) / 2.0, 90, 52, 0, 180, 'teal') for a, b in zip(_P5, _P5[1:])] +
             [('txt', (a + b) / 2.0, 25, 'gap %d' % (i + 1), 'teal', 20) for i, (a, b) in enumerate(zip(_P5, _P5[1:]))]),
    ('len', [('txt', (a + b) / 2.0, 62, '3', 'orange', 24) for a, b in zip(_P5, _P5[1:])]),
], vb='0 0 640 150', w=900, col=0, title='Five points on a line make four gaps')
# ---- slide: angles around a point
_O = (320, 170)
G1C = GEO('g1c', [
    ('line', [_g1line(_O[0], _O[1], 20, 250), _g1line(_O[0], _O[1], 125, 160), ('dot', _O[0], _O[1])]),
    ('a1', [('arc', _O[0], _O[1], 40, 20, 125, 'orange', '105°', 72)]),
    ('a2', [('arc', _O[0], _O[1], 40, 125, 200, 'teal', '75°', 72)]),
    ('a3', [('arc', _O[0], _O[1], 40, 200, 305, 'orange', '105°', 72)]),
    ('a4', [('arc', _O[0], _O[1], 40, 305, 380, 'teal', '75°', 72)]),
    ('full', [('arc', _O[0], _O[1], 118, 0, 359.9, 'teal'), ('txt', 545, 40, '360°', 'teal', 30)]),
], vb='0 10 640 320', w=760, col=0, title='Two lines cross: four angles around one point')
G1C_t = IH('g1ct', '$105°+75°+105°+75°=360°$', size=30, col=0)
G1C_t2 = I('g1ct2', 'Three lines: $\\ 60°+50°+70°+60°+50°+70°=360°$', size=26, col=0)
# ---- slide: the right angle
G1D = GEO('g1d', [
    ('line', [('seg', 120, 170, 520, 170), ('seg', 320, 20, 320, 320), ('dot', 320, 170)]),
    ('sq', [('right', 320, 170, 0, 90, 22)]),
    ('all', [('right', 320, 170, 90, 180, 22), ('right', 320, 170, 180, 270, 22), ('right', 320, 170, 270, 360, 22),
             ('txt', 380, 105, '90°', 'teal', 26), ('txt', 260, 105, '90°', 'teal', 26), ('txt', 260, 235, '90°', 'teal', 26),
             ('txt', 380, 235, '90°', 'teal', 26)]),
], vb='0 10 640 320', w=580, col=0, title='Two perpendicular lines: four right angles')
G1D2 = GEO('g1d2', [
    ('line', [('seg', 40, 200, 500, 200), _g1ray(270, 200, 93, 170), ('dot', 270, 200)]),
    ('q', [('arc', 270, 200, 36, 0, 93, 'red'), ('txt', 360, 120, '90°?', 'red', 30), ('txt', 270, 245, 'not marked: not known', 'red', 24)]),
], vb='0 0 540 270', w=520, col=1, title='Looks like a right angle, but it is not marked')
# ---- slide: acute, obtuse and straight
G1E = GEO('g1e', [
    ('line', [('seg', 30, 230, 260, 230), ('dot', 40, 230), _g1ray(40, 230, 40, 220)]),
    ('ac', [('arc', 40, 230, 60, 0, 40, 'teal', '40°', 92), ('txt', 150, 280, 'acute', 'teal', 26), ('txt', 150, 312, 'also 75°', 'teal', 20)]),
    ('ob', [('seg', 360, 230, 600, 230), ('dot', 440, 230), _g1ray(440, 230, 130, 190),
            ('arc', 440, 230, 50, 0, 130, 'orange', '130°', 82), ('txt', 500, 280, 'obtuse', 'orange', 26), ('txt', 500, 312, 'also 160°', 'orange', 20)]),
    ('st', [('seg', 680, 230, 940, 230), ('dot', 810, 230), ('arc', 810, 230, 60, 0, 180, 'teal', '180°', 92),
            ('txt', 810, 280, 'straight angle', 'teal', 26)]),
], vb='0 20 960 310', w=1000, col=0, title='An acute angle, an obtuse angle and a straight angle')
# ---- slide: adjacent angles (three panels)
G1F = GEO('g1f', [
    ('line', [('seg', 20, 220, 300, 220), ('dot', 160, 220), _g1ray(160, 220, 50, 170)]),
    ('s50', [('arc', 160, 220, 46, 0, 50, 'teal', '50°', 76)]),
    ('l130', [('arc', 160, 220, 34, 50, 180, 'orange', '130°', 70)]),
    ('rr', [('seg', 340, 220, 620, 220), ('dot', 480, 220), _g1ray(480, 220, 90, 170), ('right', 480, 220, 0, 90, 22),
            ('right', 480, 220, 90, 180, 22), ('txt', 540, 170, '90°', 'teal', 24), ('txt', 420, 170, '90°', 'teal', 24)]),
], vb='0 30 640 270', w=580, col=0, title='Adjacent angles on a straight line')
G1F3 = GEO('g1f3', [
    ('line', [('dot', 160, 220), ('seg', 160, 220, 330, 220), _g1ray(160, 220, 70, 170), _g1ray(160, 220, 150, 170)]),
    ('non', [('arc', 160, 220, 46, 0, 70, 'red', '70°', 76), ('arc', 160, 220, 40, 70, 150, 'red', '80°', 70),
             ('txt', 180, 270, 'not on one line', 'red', 22)]),
], vb='0 30 360 270', w=460, col=1, title='Side by side, but not on one straight line')
G1F_t = IH('g1ft', '$180°-50°=130°\\quad 180°-108°=72°\\quad 90°+90°=180°$', size=28, col=0)
# ---- slide: vertical angles (a focus step redraws only what is needed)
_V = (320, 160)
_V1, _V2 = _g1line(_V[0], _V[1], 35, 240), _g1line(_V[0], _V[1], 180, 240)
def _g1v(*extra): return [_V1, _V2, ('dot', _V[0], _V[1])] + list(extra)
_a35 = ('arc', _V[0], _V[1], 54, 0, 35, 'teal', '35°', 92)
_a145 = ('arc', _V[0], _V[1], 44, 35, 180, 'orange', '145°', 80)
_a35b = ('arc', _V[0], _V[1], 54, 180, 215, 'teal', '35°', 92)
_a145b = ('arc', _V[0], _V[1], 44, 215, 360, 'orange', '145°', 80)
G1G = GEO('g1g', [
    ('line', _g1v()),
    ('a35', [_a35]),
    ('n145', [('path', [(80, 160), (560, 160)], 'teal', 12), _a145]),
    ('f2', [('dim', 0, 0, 640, 320), ('dim', 0, 0, 640, 320)] + _g1v(_a35, _a145, ('path', [gpt(_V[0], _V[1], 220, 35), gpt(_V[0], _V[1], 220, 215)], 'orange', 12), _a35b)),
    ('v145', [_a145b]),
], vb='0 0 640 320', w=760, col=0, title='Vertical angles')
G1G_t = IH('g1gt', '$72°\\to108°\\to72°$', size=30, col=0)
# ---- slide: the angle bisector
_B = (120, 250)
G1H = GEO('g1h', [
    ('line', [_g1ray(_B[0], _B[1], 0, 420), _g1ray(_B[0], _B[1], 80, 230), ('dot', _B[0], _B[1])]),
    ('w', [('arc', _B[0], _B[1], 70, 0, 80, 'orange'), ('txt',) + gpt(_B[0], _B[1], 100, 64) + ('80°', 'orange', 24)]),
    ('bis', [('seg', _B[0], _B[1]) + gpt(_B[0], _B[1], 380, 40) + ('teal', 4)]),
    ('h', [('arc', _B[0], _B[1], 150, 0, 40, 'teal', 'α', 176), ('arc', _B[0], _B[1], 150, 40, 80, 'teal', 'α', 176),
           ('txt', 450, 80, 'α = 80° ÷ 2 = 40°', 'teal', 26)]),
], vb='0 20 560 270', w=760, col=0, title='An angle bisector splits the angle in two equal halves')
G1H_t = IH('g1ht', '$130°\\div2=65°\\qquad 64°\\div2=32°$', size=30, col=0)
# ---- slide: naming angles
_N = (140, 230)
G1J = GEO('g1j', [
    ('line', [_g1ray(_N[0], _N[1], 0, 360), _g1ray(_N[0], _N[1], 50, 300), ('dot', _N[0], _N[1])]),
    ('al', [('arc', _N[0], _N[1], 70, 0, 50, 'teal', 'α', 100)]),
    ('greek', [('txt', 470, 60, 'α  β  γ  δ', 'teal', 34)]),
    ('pts', [('dot',) + gpt(_N[0], _N[1], 270, 50) + ('B', -26, -6), ('dot', _N[0], _N[1], 'A', -24, 6),
             ('dot',) + gpt(_N[0], _N[1], 330, 0) + ('C', 0, 30)]),
    ('path', [('path', [gpt(_N[0], _N[1], 270, 50), _N, gpt(_N[0], _N[1], 330, 0)], 'orange', 10)]),
], vb='0 0 560 290', w=700, col=0, title='Naming an angle: alpha, or angle BAC')
G1J_t1 = I('g1jt1', '$\\alpha,\\ \\ \\beta,\\ \\ \\gamma,\\ \\ \\delta$', size=36, col=0)
G1J_t2 = I('g1jt2', '$\\angle BAC$: $\\ B\\to A\\to C$, $\\ $vertex $A$', size=30, col=0)
G1J_t3 = I('g1jt3', '$\\angle DEF$: $\\ $vertex $E$', size=30, col=0)
# ---- slide: parallel lines
G1K = GEO('g1k', [
    ('line', [('seg', 40, 90, 600, 90), ('seg', 40, 210, 600, 210), ('txt', 22, 90, 'a', 'ink', 26, True), ('txt', 22, 210, 'b', 'ink', 26, True)]),
    ('d', [('seg', x, 90, x, 210, 'teal', 3, True) for x in (150, 320, 490)] +
          [('right', x, 210, 90, 180 if x > 160 else 0, 14) for x in (150, 320, 490)] +
          [('txt', x + 22, 150, 'd', 'teal', 26, True) for x in (150, 320, 490)]),
    ('arr', [('par', 40, 90, 600, 90), ('par', 40, 210, 600, 210)]),
], vb='0 40 640 220', w=900, col=0, title='Parallel lines: the distance between them never changes')
# ---- slide: parallel lines and a transversal (the 8 angles)
_PP = (380, 110); _QQ = gcross((0, 250), (640, 250), _PP, gpt(_PP[0], _PP[1], 100, 240))
def _g1t(P, Q, deg, ang=None):
    """two parallel lines y = P[1] and y = Q[1], and a transversal through P and Q"""
    base = [('seg', 40, P[1], 600, P[1]), ('seg', 40, Q[1], 600, Q[1]), _g1line(P[0], P[1], deg, 0.1, 90),
            ('seg', P[0], P[1], Q[0], Q[1]), _g1line(Q[0], Q[1], deg, 90, 0.1),
            ('txt', 22, P[1], 'a', 'ink', 26, True), ('txt', 22, Q[1], 'b', 'ink', 26, True),
            ('par', 40, P[1], 230, P[1]), ('par', 40, Q[1], 230, Q[1])]
    return base
_W = [(0, 60, 'small', 2), (60, 180, 'large', 1), (180, 240, 'small', 4), (240, 360, 'large', 3)]
def _g1w(P, k=0, r=30):
    return [('wedge', P[0], P[1], r, a, b, c) for a, b, c, n in _W]
def _g1n(P, off):
    return [('txt',) + gpt(P[0], P[1], 46, (a + b) / 2.0) + (str(n + off), 'ink', 22) for a, b, c, n in _W]
G1L = GEO('g1l', [
    ('line', _g1t(_PP, _QQ, 60)),
    ('nums', _g1n(_PP, 0) + _g1n(_QQ, 4)),
    ('small', [('wedge', P[0], P[1], 32, a, b, 'small') for P in (_PP, _QQ) for a, b, c, n in _W if c == 'small'] +
              [('txt', 545, 45, '2 = 4 = 6 = 8', 'teal', 26)]),
    ('large', [('wedge', P[0], P[1], 32, a, b, 'large') for P in (_PP, _QQ) for a, b, c, n in _W if c == 'large'] +
              [('txt', 545, 310, '1 = 3 = 5 = 7', 'orange', 26)]),
], vb='0 20 640 330', w=820, col=0, title='Two parallel lines and a transversal: eight angles')
G1L_t1 = I('g1lt1', 'Small: $\\ 2=4=6=8$', size=30, col=0)
G1L_t2 = I('g1lt2', 'Large: $\\ 1=3=5=7$', size=30, col=0)
G1L_t3 = IH('g1lt3', 'small $+$ large $=180°$', size=30, col=0)
# the values and the circle of angles moved down (same geometry, a new figure on its own slide)
def _g1vals(P):
    return [('arc', P[0], P[1], 26, a, b, c, '%d°' % (b - a), 50) for a, b, c, n in _W]
_MP = (380, 80); _MQ = gcross((0, 280), (640, 280), _MP, gpt(_MP[0], _MP[1], 100, 240))
_MS, _ME = gpt(_MP[0], _MP[1], 92, 200), gpt(_MQ[0], _MQ[1], 92, 160)
G1M = GEO('g1m', [
    ('line', _g1t(_MP, _MQ, 60)),
    ('top', _g1vals(_MP)),
    ('ring', [('arc', _MP[0], _MP[1], 84, 0, 359.9, 'teal')]),
    ('move', [('seg', _MS[0], _MS[1], _ME[0], _ME[1], 'teal', 3, True)] + _g1arr(_ME[0], _ME[1], gdir(_MS[0], _MS[1], _ME[0], _ME[1])) +
             [('arc', _MQ[0], _MQ[1], 84, 0, 359.9, 'teal')]),
    ('bot', _g1vals(_MQ)),
], vb='0 -15 640 390', w=780, col=0, title='The circle of angles at line a, moved down to line b')
G1M_t2 = I('g1mt2', 'Small $55°\\ \\to\\ $ large $180°-55°=125°$', size=28, col=0)
# ---- slide: the Z (two variations)
_ZP = (380, 100); _ZQ = gcross((0, 240), (640, 240), _ZP, gpt(_ZP[0], _ZP[1], 100, 228))
G1N = GEO('g1n', [
    ('line', _g1t(_ZP, _ZQ, 48)),
    ('z', [('path', [(110, _ZP[1]), _ZP, _ZQ, (560, _ZQ[1])], 'teal', 10)]),
    ('in', [('arc', _ZP[0], _ZP[1], 40, 180, 228, 'small', '48°', 70), ('arc', _ZQ[0], _ZQ[1], 40, 0, 48, 'small', '48°', 70)]),
], vb='0 40 640 270', w=580, col=0, title='The Z: the two angles in its corners are equal')
_Z2P = (260, 100); _Z2Q = gcross((0, 240), (640, 240), _Z2P, gpt(_Z2P[0], _Z2P[1], 100, 312))
G1N2 = GEO('g1n2', [
    ('line', [('seg', 40, 100, 600, 100), ('seg', 40, 240, 600, 240), _g1line(_Z2P[0], _Z2P[1], 132, 0.1, 90),
              ('seg', _Z2P[0], _Z2P[1], _Z2Q[0], _Z2Q[1]), _g1line(_Z2Q[0], _Z2Q[1], 132, 90, 0.1),
              ('txt', 22, 100, 'a', 'ink', 26, True), ('txt', 22, 240, 'b', 'ink', 26, True)]),
    ('z', [('path', [(560, 100), _Z2P, _Z2Q, (80, 240)], 'teal', 10)]),
    ('in', [('arc', _Z2P[0], _Z2P[1], 40, 312, 360, 'small', '48°', 70), ('arc', _Z2Q[0], _Z2Q[1], 40, 132, 180, 'small', '48°', 70)]),
], vb='0 40 640 270', w=520, col=1, title='Another Z, turned the other way')
# ---- slide: the U
_UP = (380, 100); _UQ = gcross((0, 240), (640, 240), _UP, gpt(_UP[0], _UP[1], 100, 242))
G1P = GEO('g1p', [
    ('line', _g1t(_UP, _UQ, 62)),
    ('u', [('path', [(560, _UP[1]), _UP, _UQ, (560, _UQ[1])], 'teal', 10)]),
    ('s', [('arc', _UQ[0], _UQ[1], 36, 0, 62, 'small', '62°', 64)]),
    ('l', [('arc', _UP[0], _UP[1], 36, 242, 360, 'large', '118°', 66)]),
], vb='0 40 640 270', w=760, col=0, title='The U: the two angles inside it add up to 180 degrees')
G1P_t = IH('g1pt', '$62°+118°=180°$', size=30, col=0)
G1P_t2 = IH('g1pt2', '$75°\\to105°$', size=30, col=0)
# ---- slide: parallel or not? (three proofs and the trap)
G1Q = GEO('g1q', [
    ('line', [('seg', 20, 200, 280, 200), ('seg', 80, 60, 80, 300), ('seg', 210, 60, 210, 300),
              ('right', 80, 200, 0, 90, 16), ('right', 210, 200, 0, 90, 16)]),
    ('p1', [('par', 80, 280, 80, 70), ('par', 210, 280, 210, 70), ('txt', 145, 335, 'both ⊥ the same line', 'teal', 26)]),
    ('r2', [('seg', 340, 90, 620, 90), ('seg', 340, 170, 620, 170), ('seg', 340, 250, 620, 250),
            ('txt', 325, 90, 'a', 'ink', 24, True), ('txt', 325, 170, 'c', 'ink', 24, True), ('txt', 325, 250, 'b', 'ink', 24, True),
            ('par', 340, 90, 480, 90), ('par', 340, 250, 480, 250), ('par', 340, 170, 480, 170, 2), ('par', 480, 170, 620, 170, 2)]),
    ('p2', [('par', 480, 90, 620, 90, 2), ('par', 480, 250, 620, 250, 2), ('txt', 480, 335, 'both ∥ c', 'teal', 26)]),
    ('r3', [('seg', 680, 110, 960, 110), ('seg', 680, 240, 960, 240), _g1line(820, 110, 70, 0.1, 80),
            ('seg', 820, 110) + gcross((0, 240), (1000, 240), (820, 110), gpt(820, 110, 100, 250)),
            _g1line(*gcross((0, 240), (1000, 240), (820, 110), gpt(820, 110, 100, 250)), deg=70, r1=80, r2=0.1),
            ('arc', 820, 110, 34, 250, 360, 'large', '110°', 62),
            ('arc',) + gcross((0, 240), (1000, 240), (820, 110), gpt(820, 110, 100, 250)) + (34, 0, 70, 'small', '70°', 60)]),
    ('p3', [('par', 680, 110, 780, 110), ('par', 680, 240, 780, 240), ('txt', 820, 335, '110° + 70° = 180°', 'teal', 26)]),
], vb='0 40 1000 320', w=1100, col=0, title='Three ways to know that two lines are parallel')
G1Q_t = I('g1qt', 'Not to scale: parallel only if given or proved $\\cdot$ $90°$ only if marked', size=26, col=0)
G1R = [I('g1r%d' % k, t, size=28) for k, t in enumerate([
    'Line: endless $\\cdot$ segment: two ends $\\cdot$ count the gaps, not the points',
    'Around a point $360°$ $\\cdot$ straight angle $180°$ $\\cdot$ right angle $90°$ (only if marked)',
    'Adjacent on a straight line: $180°$ $\\cdot$ vertical angles: equal $\\cdot$ bisector: two halves',
    'Parallel + transversal: small $=$ small, large $=$ large, small $+$ large $=180°$',
    'Z $\\to$ equal $\\cdot$ U $\\to$ $180°$ $\\cdot$ parallel only if given or proved'])]

video('geo-001', 'lesson', slides=[
    S('Lines and Angles',
      L("Welcome to geometry. In the quantitative part of the exam, about five questions out of twenty are geometry, so "
        "a quarter. Most of them are built on the rules, so if you know the rules well, you'll solve most of them. "
        "There are also questions that need a clever idea, but they're rarer. Let's start with the definitions.")),
    S('A line and a segment',
      L("A line passes through two points. Here are two points, A and B, and we draw a line through them.",
        show(G1A['line'], 'Here are two points'), show(G1A['ln'], 'we draw a line through them')),
      L("There's a basic rule: through two points there is exactly one straight line. Any other line through A and B "
        "can't be straight. It has to bend, like this one. And a line never ends. It goes on forever at both ends.",
        show(G1A['bent'], 'It has to bend'), pt('g1a_ln', 'a line never ends')),
      L("When we cut a line off between two points, we call it a segment. A segment has two ends, and it doesn't go on. "
        "This is segment C D, from C to D.", show(G1A['seg'], 'This is segment C D'))),
    S('Segments on a line',
      L("Points on a line make segments, and here's one trap for the exam. Five points, equally spaced. How many gaps "
        "are there between them?", show(G1B['line'], 'Five points, equally spaced'), show(G1B['pts'], 'How many gaps')),
      L("Count the spaces, not the points. One, two, three, four gaps. Five points make four gaps, one less than the "
        "number of points.", show(G1B['gaps'], 'Count the spaces')),
      L("Lengths live in the gaps. If every gap is three centimeters, then from the first point to the last one is four "
        "times three, twelve centimeters, not five times three, fifteen. And seven points in a row make six gaps.",
        show(G1B['len'], 'If every gap is three'), show(I('g1bt', '$4\\cdot3=12$, $\\ $not $5\\cdot3=15$', size=28, col=0),
                                                         'twelve centimeters'),
        show(I('g1bt2', '7 points: 6 gaps', size=28, col=0), 'And seven points in a row'))),
    S('Angles around a point',
      L("Intersecting lines are two straight lines that cross each other at one point. Around that point we get a kind "
        "of circle of angles, four angles.", show(G1C['line'], 'Intersecting lines are'), show(G1C['a1'], 'four angles')),
      L("A whole circle of angles is three hundred sixty degrees. For example, here the angles are a hundred five, "
        "seventy-five, a hundred five and seventy-five.", show(G1C['a2'], 'seventy-five, a hundred'),
        show(G1C['a3'], 'a hundred five and'), show(G1C['a4'], 'and seventy-five.')),
      L("Together, a hundred five plus seventy-five is a hundred eighty, and twice that is three hundred sixty. All the "
        "angles around one point always add up to three hundred sixty, even when more lines cross there.",
        show(G1C['full'], 'twice that is three hundred sixty'), show(G1C_t, 'All the angles around one point'),
        show(G1C_t2, 'even when more lines'))),
    S('The right angle',
      L("A right angle is exactly ninety degrees. Two lines that make a right angle are called perpendicular. We mark the "
        "right angle with a small square, and on the exam there's almost always a dot in the middle of it.",
        show(G1D['line'], 'Two lines that make a right angle'), show(G1D['sq'], 'with a small square')),
      L("Ninety is exactly a quarter of three hundred sixty. Around the point we have a quarter, a quarter, a quarter and "
        "a quarter. Ninety, ninety, ninety, ninety.", show(G1D['all'], 'a quarter, a quarter')),
      L("The rule for the exam: an angle is ninety degrees only if it's marked like this, or it's given. If it only looks "
        "like ninety, that's not enough. This angle looks right, but there's no square, so we don't know it.",
        show(G1D2['line'], 'This angle looks right'), show(G1D2['q'], "there's no square"))),
    S('Acute, obtuse and straight',
      L("An acute angle is smaller than ninety degrees, like this forty-degree angle. Seventy-five is acute too.",
        show(G1E['line'], 'An acute angle is'), show(G1E['ac'], 'like this forty-degree')),
      L("An obtuse angle is bigger than ninety degrees, like this one of a hundred thirty. A hundred sixty is obtuse "
        "too.", show(G1E['ob'], 'An obtuse angle is')),
      L("A straight angle is a hundred eighty degrees. It's really just a straight line with a vertex on it. Why a "
        "hundred eighty? A whole circle is three hundred sixty, and a straight line cuts it in half, a hundred eighty on "
        "this side, and a hundred eighty on the other side.", show(G1E['st'], 'A straight angle is'))),
    S('Adjacent angles',
      L("Adjacent angles are two angles side by side on one straight line. Together they make the straight angle, so "
        "they add up to a hundred eighty.", show(G1F['line'], 'side by side on one straight line')),
      L("Here one of them is fifty. So the other one is a hundred eighty minus fifty, a hundred thirty. One is acute, and "
        "the one next to it is obtuse. Another example: if one is a hundred eight, the other is seventy-two.",
        show(G1F['s50'], 'Here one of them is fifty'), show(G1F['l130'], 'a hundred thirty')),
      L("There's one special case. They can also both be right angles, and ninety plus ninety is a hundred eighty too.",
        show(G1F['rr'], 'both be right angles'), show(G1F_t, 'ninety plus ninety')),
      L("But careful. Two angles side by side that are not on one straight line don't have to add up to a hundred "
        "eighty. Here, seventy plus eighty is only a hundred fifty.", show(G1F3['line'], 'that are not on one straight line'),
        show(G1F3['non'], 'Here, seventy plus eighty'))),
    S('Vertical angles',
      L("When two lines cross, the angles that face each other, vertex to vertex, are called vertical angles. Vertical "
        "angles are equal. Let's see why.", show(G1G['line'], 'When two lines cross')),
      L("Say this angle is thirty-five degrees. It sits on this straight line, so the angle next to it completes it to a "
        "hundred eighty. That's a hundred forty-five.", show(G1G['a35'], 'Say this angle is thirty-five'),
        show(G1G['n145'], 'It sits on this straight line')),
      L("Now look at the other straight line. The same hundred forty-five sits on it too, so the angle on its other side "
        "also completes it to a hundred eighty. That's thirty-five again. So the two angles facing each other are "
        "equal, thirty-five and thirty-five.", show(G1G['f2'], 'Now look at the other straight line')),
      L("And the angle facing the hundred forty-five is a hundred forty-five too. Another example: if one angle is "
        "seventy-two, its neighbor is a hundred eight, and the angle facing it is seventy-two.",
        show(G1G['v145'], 'And the angle facing'), show(G1G_t, 'Another example'))),
    S('The angle bisector',
      L("An angle bisector is a line that leaves the vertex of an angle and splits the angle into two equal angles. It "
        "goes exactly through the middle. Here's an angle of eighty degrees.", show(G1H['line'], 'An angle bisector is'),
        show(G1H['w'], 'an angle of eighty')),
      L("The bisector cuts it in the middle, so we call both halves alpha. Each half is eighty divided by two, forty. If "
        "the whole angle is a hundred thirty, each half is sixty-five, and if it's sixty-four, each half is thirty-two.",
        show(G1H['bis'], 'The bisector cuts it'), show(G1H['h'], 'so we call both halves'),
        show(G1H_t, 'If the whole angle is'))),
    S('Naming angles',
      L("This is a good moment to talk about names. I marked this angle with alpha. That's a Greek letter, and we often "
        "name angles with Greek letters: alpha, beta, gamma, delta. Students sometimes mix up the names, and that's fine, "
        "it doesn't really matter.", show(G1J['line'], 'I marked this angle'), show(G1J['al'], 'with alpha'),
        show(G1J['greek'], 'alpha, beta, gamma, delta')),
      L("There's another way to name an angle, with three letters. Put the points B, A and C on the figure. Angle B A C "
        "means: start at B, move to A, and continue to C. The letter in the middle, A, is the vertex.",
        show(G1J['pts'], 'Put the points'), show(G1J['path'], 'start at B, move to A'), show(G1J_t2, 'The letter in the middle')),
      L("So angle D E F has its vertex at E. And of course, we can also just give the size, like thirty degrees.",
        show(G1J_t3, 'So angle D E F'))),
    S('Parallel lines',
      L("Parallel lines are lines whose distance from each other never changes. Here are two lines, a and b.",
        show(G1K['line'], 'Here are two lines')),
      L("The distance between two lines is always measured on a line that's perpendicular to both of them. Here it's d, "
        "here it's d, and here it's d again. As the lines go on, the distance stays the same.",
        show(G1K['d'], 'Here it')),
      L("So parallel lines never meet. They never cross each other, they just go on side by side. We mark them with "
        "small arrows.", show(G1K['arr'], 'We mark them'))),
    S('Parallel lines and a transversal',
      L("Now two parallel lines, a and b, and a line that cuts both of them. We call it a transversal. It makes eight "
        "angles, four at each crossing.", show(G1L['line'], 'Now two parallel lines'), show(G1L['nums'], 'It makes eight')),
      L("The angles with even numbers, two, four, six and eight, are the small angles. All the small angles are equal. "
        "Two and four are vertical angles, and six and eight are equal to them too.", show(G1L['small'], 'are the small angles')),
      L("The angles with odd numbers, one, three, five and seven, are the large angles. All the large angles are equal "
        "too.", show(G1L['large'], 'are the large angles')),
      L("And a small angle plus a large angle is always a hundred eighty. Why? Angles one and two sit side by side on "
        "line a, so they make a straight angle.", show(G1L_t3, 'a small angle plus a large angle'),
        pt('g1l_line', 'sit side by side'))),
    S('The same angles, moved down',
      L("Let's put numbers on it. At line a, the small angle is sixty degrees, so the large angle next to it is a "
        "hundred twenty. And around the crossing, sixty, a hundred twenty, sixty, a hundred twenty.",
        show(G1M['line'], "Let's put numbers"), show(G1M['top'], 'the small angle is sixty')),
      L("Now take this whole circle of angles at line a, as if we cut it out, and move it down to line b. It fits "
        "exactly. These are the same angles. So all the small ones are sixty, and all the large ones are a hundred "
        "twenty.", show(G1M['ring'], 'take this whole circle'), show(G1M['move'], 'move it down'),
        show(G1M['bot'], 'These are the same angles')),
      L("Another example: if a small angle is fifty-five, every large angle is a hundred eighty minus fifty-five, a "
        "hundred twenty-five.", show(G1M_t2, 'a hundred eighty minus fifty-five'))),
    S('The Z',
      L("In exam questions, whenever you see two parallel lines, look for this Z. It runs along line a, down the "
        "transversal, and along line b.", show(G1N['line'], 'whenever you see two parallel lines'),
        show(G1N['z'], 'look for this Z')),
      L("The Z holds two angles, one in each corner. The angle under line a and the angle above line b. They are equal. "
        "If this one is forty-eight, that one is forty-eight too.", show(G1N['in'], 'The Z holds two angles')),
      L("The Z can also be turned the other way, and it works the same. Here too, forty-eight and forty-eight.",
        show(G1N2['line'], 'turned the other way'), show(G1N2['z'], 'it works the same'), show(G1N2['in'], 'Here too')),
      L("In school these angles have names, but we don't need them. Mark the Z, find the two equal angles inside it, and "
        "from there you can get every other angle, either equal or completing to a hundred eighty.",
        pt('g1n_z', 'Mark the Z'))),
    S('The U',
      L("One more shape, the U. Here the two angles sit inside a U, on the same side of the transversal, between the two "
        "lines.", show(G1P['line'], 'One more shape'), show(G1P['u'], 'sit inside a U')),
      L("They're not equal. One is small and one is large. And small plus large is a hundred eighty. So if the small one "
        "is sixty-two, the large one is a hundred eighteen.", show(G1P['s'], 'One is small'), show(G1P['l'], 'the large one is'),
        show(G1P_t, 'a hundred eighteen')),
      L("Another example: seventy-five inside a U goes with a hundred five. So the Z means equal, and the U means they add "
        "up to a hundred eighty.", show(G1P_t2, 'Another example'))),
    S('Parallel or not?',
      L("When do we know that two lines are parallel? There are three rules. One: two lines that are both perpendicular "
        "to the same line are parallel. They both go straight up from it, in the same direction, so they never meet.",
        show(G1Q['line'], 'two lines that are both perpendicular'), show(G1Q['p1'], 'so they never meet')),
      L("Two: two lines that are both parallel to a third line are parallel to each other.",
        show(G1Q['r2'], 'both parallel to a third line'), show(G1Q['p2'], 'parallel to each other')),
      L("Three: if the angles behave like the angles of parallel lines, the lines are parallel. For example, two angles "
        "in a U that add up to a hundred eighty, like a hundred ten and seventy.", show(G1Q['r3'], 'if the angles behave'),
        show(G1Q['p3'], 'like a hundred ten and seventy')),
      L("And the trap: on the exam, figures are not drawn to scale. Two lines can look parallel and not be. They're "
        "parallel only if it's given, or one of these rules proves it, and an angle is ninety only if it's marked or "
        "given.", show(G1Q_t, 'figures are not drawn to scale'))),
    S('Recap',
      L("Let's sum up. A line goes on forever, and a segment has two ends. On a line, count the gaps, not the points.",
        show(G1R[0], 'A line goes on forever')),
      L("All the angles around a point add up to three hundred sixty. A straight angle is a hundred eighty, and a right "
        "angle is ninety, but only if it's marked or given.", show(G1R[1], 'All the angles around a point')),
      L("Adjacent angles on a straight line add up to a hundred eighty. Vertical angles are equal. A bisector cuts an "
        "angle into two equal halves.", show(G1R[2], 'Adjacent angles on a straight line')),
      L("Parallel lines and a transversal: all the small angles are equal, all the large ones are equal, and small plus "
        "large is a hundred eighty. The Z means equal, and the U means a hundred eighty. And lines are parallel only if "
        "it's given or proved. [pause] Okay. I'll see you in the next video.",
        show(G1R[3], 'Parallel lines and a transversal'), show(G1R[4], 'The Z means equal'))),
])

CAMERA_SPLIT = ('geo-001', 'Lines and Angles', [
    (1, None),
    (4, "Let's continue with lines and angles, and get to know the kinds of angles."),
    (8, "Let's continue with lines and angles: the bisector, the names of angles, and parallel lines."),
    (13, "Let's continue with parallel lines, and learn two shapes that help us find their angles."),
])

# =================================================================================================================
# Topic-30 question videos, learning block 1 (geo30-g002, q-r26-t30-01, q-r26-t30-02). Written 2026-10-14.
# The marks are drawn EXACTLY ON the question's own figure (V3: the figure fills up as the solution goes; the question
# figure itself stays black and white underneath): OV() below builds GEO layers whose viewBox is calibrated to the place
# where the studio draws the question figure (measured: board x, y, width of the figure for each question). The
# renderer draws a layer (over=1) at the top of the question (board y QY) without pushing it, so the viewBox is shifted to
# land on the figure. All the board work of these videos is in the overlay (a layer cannot follow another board item),
# including the short equations, written next to the figure. No "Method N" slide titles: a header item would move QY.
# =================================================================================================================
QY, BLEFT, BRIGHT, CTOP = 78.9, 410.0, 1540.0, 705.0


def OV(name, layers, box, title='Figure marks'):
    """GEO layers drawn on the question figure. box = (board x, board y, board width of the figure, its viewBox
    (u0, v0, uw, vh)); every element uses the question figure's own coordinates."""
    X0, Y0, W, (u0, v0, uw, vh) = box; s = W / uw
    ua, ub = u0 + (BLEFT - X0) / s, u0 + (BRIGHT - X0) / s
    va, vb_ = v0 + (QY - Y0) / s, v0 + (CTOP - Y0) / s
    out = GEO(name, layers, vb='%.3f %.3f %.3f %.3f' % (ua, va, ub - ua, vb_ - va), w=round((ub - ua) * s, 3), col=0,
              title=title)
    for _it in out.values(): _it['over'] = 1; _it['of'] = 'question-figure'; _it['_x'] = BLEFT
    return out


# ------------------------------------------------------------------------------------------------ geo30-g002 (Hebrew: the lesson's sample question)
# REMINDER (camera lesson geo-001): parallel lines and a cutting line - all the small angles are equal; the right-angle
# square; ignore the rest of the figure. Hebrew (geo 129-147): small angles equal (75 = 75), the right angle, x = 90 - 75;
# one method. English numbers 64 and 26 (the Hebrew "?" vertical step is not in this question).
# Visual steps (V3): highlight x and the 64 in the question figure; FOCUS: dim the extra line, the two parallel lines and
# the cutting line drawn over in ink with parallel arrows; the 64 at a traced, then the SAME teal arc and label at line b
# (the moved angle); the extra line drawn back in with its right-angle square; x traced in red as the second piece of the
# right angle; the equation written next to the figure; the value written on the figure next to x.
_A2, _B2 = 121.6, 238.4
_T2a, _T2b = (262.143, 301.667), (380.825, 58.333)
_Pa2 = gcross(_T2a, _T2b, (0, _A2), (640, _A2)); _Pb2 = gcross(_T2a, _T2b, (0, _B2), (640, _B2))
_Q1, _Q2 = (245.813, 215.386), (406.697, 293.854)
_up2 = gdir(_Pb2[0], _Pb2[1], _T2b[0], _T2b[1]); _pp2 = gdir(_Pb2[0], _Pb2[1], _Q2[0], _Q2[1])
_lb2 = gpt(_Pb2[0], _Pb2[1], 60, _up2 / 2.0)
g2 = OV('g2', [
    ('line', [('dim', 70, 40, 500, 290), ('seg', 105.9, _A2, 534.1, _A2), ('seg', 105.9, _B2, 534.1, _B2),
              ('seg', _T2a[0], _T2a[1], _T2b[0], _T2b[1]), ('txt', 93.7, _A2, 'a', 'ink', 20, True), ('txt', 93.7, _B2, 'b', 'ink', 20, True),
              ('par', 150, _A2, 230, _A2), ('par', 150, _B2, 230, _B2)]),
    ('top', [('arc', _Pa2[0], _Pa2[1], 32, 0, _up2, 'small'), ('txt', 394.066, 94.044, '64°', 'small', 19)]),
    ('bot', [('arc', _Pb2[0], _Pb2[1], 32, 0, _up2, 'small'), ('txt', _lb2[0] + 6, _lb2[1] - 4, '64°', 'small', 19)]),
    ('perp', [('seg', _Q1[0], _Q1[1], _Q2[0], _Q2[1], 'ink', 3), ('right', _Pb2[0], _Pb2[1], _pp2, _up2, 14)]),
    ('x', [('arc', _Pb2[0], _Pb2[1], 46, _pp2, 360, 'red'), ('txt', 357.3, 253.2, 'x', 'red', 20, True)]),
    ('eq1', [('txt', 640, 150, '64° + x = 90°', 'ink', 21)]),
    ('eq2', [('txt', 640, 190, 'x = 90° − 64°', 'ink', 21)]),
    ('val', [('txt', 640, 230, 'x = 26°', 'red', 23), ('txt', 397, 253, '= 26°', 'red', 18)]),
], (551.2133, 219.24, 847.5733, (0, 0, 640, 360)), title='Marks on the figure: parallel lines a and b')
video('solve-geo30-g002', 'solution', qid='geo30-g002', slides=[
    S('Small angles are equal',
      L("In the accompanying figure, a is parallel to b. The marked lines are perpendicular. What is the value of x?",
        pt('stem', 'In the accompanying figure', 'hl', 7.0), voice='calm', pause=0.5),
      L("x is at line b, between line b and the extra line. The only number we have, sixty-four, is up at line a. [short "
        "pause] So first we'll bring the sixty-four down to line b, and then we'll use the right angle.",
        pt('fig: x', 'x is at line b'), pt('fig: 64°', 'The only number we have')),
      L("[short pause] For now, let's look only at the two parallel lines and the line that cuts both of them. We'll ignore "
        "the extra line for a moment.", show(g2['line'], "let's look only at the two parallel lines")),
      L("The angle at line a is sixty-four degrees. It's smaller than ninety, so it's a small angle. When two parallel "
        "lines are cut by a line, all the small angles are equal. So the small angle at line b, above b and to the right "
        "of the cutting line, is sixty-four degrees too.", show(g2['top'], 'The angle at line a'),
        show(g2['bot'], 'So the small angle at line b'), pt('fig: 64°', 'is sixty-four degrees too')),
      L("Now let's bring back the extra line. The little square says it's perpendicular to the cutting line. So the angle "
        "between them is a right angle, ninety degrees.", show(g2['perp'], 'bring back the extra line')),
      L("That right angle is made of two pieces. Above line b, there's the sixty-four. Below line b, there's x. So sixty-four "
        "plus x is ninety.", show(g2['x'], 'Below line b'), show(g2['eq1'], 'So sixty-four plus x is ninety')),
      L("x is ninety minus sixty-four, which is twenty-six. Choice number two is our answer.", show(g2['eq2'], 'x is ninety minus'),
        show(g2['val'], 'which is twenty-six'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Careful with sixty-four, choice number one. That's the angle next to x, not x itself. [pause] Okay. I'll see you in "
        "the next question.", mk('cross', 'choice 1', 'Careful with sixty-four, choice number one'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t30-01 (added)
# REMINDER (geo-001): two lines perpendicular to the same line are parallel; small angles are equal; two angles side by
# side on one straight line add up to 180. NEW at the step: the parallel lines are not written - prove them first; the
# trap "cannot be determined". One method (as before).
# Visual steps (V3): highlight x and the 50 in the question figure; line c traced in teal with its two right-angle squares;
# the rule written next to the figure; parallel arrows drawn on a and b; FOCUS: c dimmed, a, b and d drawn over in ink; the
# 50 at a traced, then the SAME teal arc and label at line b; x traced in orange (a large angle) next to it on the straight
# line b; the equation next to the figure; the value written on the figure.
_A1, _B1 = 110.0, 250.0
_Da, _Db = (296.436, 290.0), (481.038, 70.0)
_Pa1 = gcross(_Da, _Db, (0, _A1), (640, _A1)); _Pb1 = gcross(_Da, _Db, (0, _B1), (640, _B1))
_up1 = gdir(_Pb1[0], _Pb1[1], _Db[0], _Db[1])
_lb1 = gpt(_Pb1[0], _Pb1[1], 58, _up1 / 2.0)
g1 = OV('g1', [
    ('line', [('seg', 170, 60, 170, 300, 'teal', 4), ('right', 170, _A1, 0, 90, 12), ('right', 170, _B1, 0, 90, 12)]),
    ('rule', [('txt', 745, 100, 'a ⊥ c,  b ⊥ c', 'ink', 30), ('txt', 745, 142, '→  a ∥ b', 'ink', 30)]),
    ('par', [('par', 230, _A1, 300, _A1, 1, 'teal'), ('par', 230, _B1, 300, _B1, 1, 'teal')]),
    ('focus', [('dim', 95, 35, 460, 275), ('seg', 120, _A1, 540, _A1), ('seg', 120, _B1, 540, _B1), ('seg', _Da[0], _Da[1], _Db[0], _Db[1]),
               ('txt', 105, _A1, 'a', 'ink', 20, True), ('txt', 105, _B1, 'b', 'ink', 20, True), ('txt', 491, 58, 'd', 'ink', 20, True),
               ('par', 230, _A1, 300, _A1, 1, 'teal'), ('par', 230, _B1, 300, _B1, 1, 'teal')]),
    ('top', [('arc', _Pa1[0], _Pa1[1], 28, 0, _up1, 'small'), ('txt', 491, 90, '50°', 'small', 18)]),
    ('bot', [('arc', _Pb1[0], _Pb1[1], 28, 0, _up1, 'small'), ('txt', _lb1[0] + 4, _lb1[1] - 2, '50°', 'small', 18)]),
    ('x', [('arc', _Pb1[0], _Pb1[1], 22, _up1, 180, 'large'), ('txt', 312, 212, 'x', 'large', 20, True)]),
    ('eq1', [('txt', 745, 200, '50° + x = 180°', 'ink', 30)]),
    ('eq2', [('txt', 745, 242, 'x = 180° − 50°', 'ink', 30)]),
    ('val', [('txt', 745, 288, 'x = 130°', 'red', 32), ('txt', 262, 212, '130° =', 'red', 18)]),
], (687.8889, 279.0, 574.2222, (0, 0, 640, 360)), title='Marks on the figure: lines a, b, c and d')
video('solve-q-r26-t30-01', 'solution', qid='q-r26-t30-01', slides=[
    S('Prove the lines are parallel',
      L("In the accompanying figure, lines a and b are both perpendicular to line c. Line d crosses lines a and b. What is "
        "the value of x?", pt('stem', 'In the accompanying figure', 'hl', 8.0), voice='calm', pause=0.5),
      L("x is at line b, and the only number we have, fifty degrees, is at line a. To move an angle from one line to the "
        "other, the two lines must be parallel. But the question doesn't say that a is parallel to b. [short pause] So "
        "first we'll check if we can prove it.", pt('fig: x', 'x is at line b'), pt('fig: 50°', 'the only number we have')),
      L("[short pause] Look at line c. Line a makes a right angle with it, and line b makes a right angle with it too. The "
        "little squares show that.", show(g1['line'], 'Look at line c')),
      L("Two lines that are perpendicular to the same line are parallel. They both go straight across, in the same "
        "direction, so they never meet. So a is parallel to b, even though the question doesn't write it.",
        show(g1['rule'], 'Two lines that are perpendicular to the same line'), show(g1['par'], 'So a is parallel to b')),
      L("Now we don't need line c anymore. It's the usual picture: two parallel lines, a and b, and line d that cuts them.",
        show(g1['focus'], "we don't need line c anymore"), pt('fig: d', 'line d that cuts them')),
      L("The fifty degrees at line a is a small angle. All the small angles are equal, so the small angle at line b, above "
        "b and to the right of d, is fifty degrees too.", show(g1['top'], 'The fifty degrees at line a'),
        show(g1['bot'], 'so the small angle at line b')),
      L("x is right next to that fifty, on the other side of line d. Together they make the straight line b, so fifty plus "
        "x is a hundred eighty.", show(g1['x'], 'x is right next to that fifty'), show(g1['eq1'], 'so fifty plus x')),
      L("x is a hundred eighty minus fifty, which is a hundred thirty. Choice number three is our answer.",
        show(g1['eq2'], 'x is a hundred eighty minus fifty'), show(g1['val'], 'which is a hundred thirty'),
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Careful with choice number four. It's true that the question doesn't write that a is parallel to b, but the two "
        "right angles prove it, so x can be found. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 4', 'Careful with choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t30-02 (added)
# REMINDER (geo-001): points on a line make segments; a length is the gap between two points. NEW: AC and BD overlap on BC.
# Methods (kept): step by step (AB = AD - BD, then BC = AC - AB); the overlap rule AC + BD = AD + BC.
# Visual steps (V3): each given is highlighted in the question as she reads it; its segment is drawn as a coloured bar
# on the figure's own line (AD above in ink, BD below in orange, AB below in teal with its calculation, AC lower in teal),
# the piece found tinted red on the line with its calculation; method 2 on a NEW slide from the givens: AC above (teal),
# BD below (orange), the overlap BC tinted red ("covered twice"), then the equation under the figure.
_X = {'A': 140, 'B': 248, 'C': 338, 'D': 500}
def _bar(p, q, y, col, label, ly, size=15):
    return [('seg', _X[p], y, _X[q], y, col, 4), ('seg', _X[p], y - 6, _X[p], y + 6, col, 2.5), ('seg', _X[q], y - 6, _X[q], y + 6, col, 2.5),
            ('txt', (_X[p] + _X[q]) / 2.0, ly, label, col, size)]
_BOX3 = (534.3, 373.77, 881.4, (90, 130, 460, 90))   # the 460 x 90 figure is centred in its 881 x 220 box (+24 px)
s1 = OV('s1', [
    ('line', _bar('A', 'D', 158, 'ink', 'AD = 20', 143)),
    ('bd', _bar('B', 'D', 232, 'orange', 'BD = 14', 248)),
    ('ab', _bar('A', 'B', 232, 'teal', 'AB = 20 − 14 = 6', 248)),
    ('ac', _bar('A', 'C', 266, 'teal', 'AC = 11', 282)),
    ('bc', [('seg', _X['B'], 180, _X['C'], 180, 'red', 6), ('tint', [(_X['B'], 170), (_X['C'], 170), (_X['C'], 190), (_X['B'], 190)], 'red'),
            ('txt', 320, 304, 'BC = AC − AB = 11 − 6 = 5', 'red', 15)]),
], _BOX3, title='Marks on the figure: segments on a line')
s2 = OV('s2', [
    ('line', _bar('A', 'C', 158, 'teal', 'AC = 11', 143)),
    ('bd', _bar('B', 'D', 232, 'orange', 'BD = 14', 248)),
    ('bc', [('tint', [(_X['B'], 150), (_X['C'], 150), (_X['C'], 240), (_X['B'], 240)], 'red'), ('txt', 293, 262, 'BC twice', 'red', 15)]),
    ('eq1', [('txt', 320, 284, 'AC + BD = AD + BC', 'ink', 15)]),
    ('eq2', [('txt', 320, 305, '11 + 14 = 20 + BC  →  BC = 5', 'ink', 15)]),
], _BOX3, title='Marks on the figure: AC and BD overlap on BC')
video('solve-q-r26-t30-02', 'solution', qid='q-r26-t30-02', slides=[
    S('Step by step',
      L("Points A, B, C and D lie on a line in this order, as shown in the accompanying figure. Given: A C is eleven, B D is "
        "fourteen, and A D is twenty. What is the length of B C?", pt('stem', 'Points A, B, C and D', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("B C is the short piece in the middle, between B and C. [short pause] We'll solve it two ways, finding the pieces "
        "one by one, and then with the overlap rule.", pt('fig: B', 'the short piece in the middle')),
      L("[short pause] The math way first. Let's put each length on the figure. A D is twenty, the whole line from A to D.",
        pt('stem: g3', "Let's put each length"), show(s1['line'], 'A D is twenty')),
      L("B D is fourteen, the part from B to the end. So what's left at the start, A B, is twenty minus fourteen, which is "
        "six.", pt('stem: g2', 'B D is fourteen'), show(s1['bd'], 'the part from B to the end'), show(s1['ab'], 'twenty minus fourteen')),
      L("Now A C is eleven, and A C is made of A B and B C. A B is six, so B C is eleven minus six, which is five. Choice "
        "number three is our answer.", pt('stem: g1', 'Now A C is eleven'), show(s1['ac'], 'A C is made of'),
        show(s1['bc'], 'so B C is eleven minus six'), mk('tick', 'choice 3', 'Choice number three is our answer')), sb='Method 1 · The math way'),
    S('The overlap rule',
      L("[pause] Now by understanding, with the overlap rule, in one line. Let's draw A C above the line and B D below it.",
        show(s2['line'], 'Let\'s draw A C above'), show(s2['bd'], 'and B D below it')),
      L("Together, A C and B D cover the whole line from A to D, and the middle piece, B C, is covered twice. So A C plus "
        "B D is the whole line, A D, plus B C one more time.", show(s2['bc'], 'is covered twice'), show(s2['eq1'], 'So A C plus B D')),
      L("Eleven plus fourteen is twenty-five, and the whole line is twenty. So twenty-five is twenty plus B C, and B C is "
        "five. Choice number three again.", show(s2['eq2'], 'Eleven plus fourteen'), mk('tick', 'choice 3', 'Choice number three again')),
      L("Careful with the other choices. Six, choice number two, is A B, the wrong piece. And twenty-five, choice number "
        "four, is A C plus B D, with B C counted twice. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 2', 'Six, choice number two'), mk('cross', 'choice 4', 'And twenty-five, choice number four')), sb='Method 2 · Understanding: the overlap rule'),
])

# ---- placement (this fragment's question videos): the question figure on the left (figw 0.56, as in the course's
# geometry videos), our board on the right, x = 1040, explicit y (the right column starts below the question text).
_F3_Q = {'solve-geo30-g005', 'solve-geo30-g006', 'solve-geo30-g007', 'solve-q-r26-t30-03'}


def _R(it, y, x=1040):
    """place an item (or every layer of a GEO figure) in the right column at y"""
    for t in (it.values() if '_name' not in it else [it]):
        t['_col'] = 1; t['_x'] = x; t['_y'] = y
    return it


def SM(sb, title, *lines):
    """a slide titled without 'Method N ·' (no header drawn over a tall question figure); the sidebar names the method"""
    return S(title, *lines, sb=sb)


_ss_before_f3 = studio_slides


def studio_slides(vid):
    out, sb = _ss_before_f3(vid)
    if vid in _F3_Q:
        for b in out:
            for it in b['pre']: it.update(figw=0.56, figalign='left')
    return out, sb


# ------------------------------------------------------------------------------------------------ geo-004 (lesson: Lines and Angles: Advanced)
# Hebrew (geo 147-155): the basics were the last lesson; now harder psychometric questions, only a few, because lines and
# angles is a narrow topic: there are standalone questions, but most of the time the rules are part of other geometry
# questions. Course addition kept: the three things that make these questions harder (each taught in the next questions).
h4a = I('h4a', '1 · A crowded figure: several pairs of lines', size=32)
h4b = I('h4b', '2 · Letters instead of numbers', size=32)
h4c = I('h4c', '3 · A missing line: we add one', size=32)
video('geo-004', 'lesson', slides=[
    S('Lines and Angles: Advanced',
      L("In the last lesson we learned the basics of lines and angles. In this lesson we'll practice harder exam "
        "questions.")),
    S('What makes it harder',
      L("We'll practice only a few questions, because lines and angles is a fairly narrow topic on the exam. There are "
        "questions only about lines and angles, but most of the time these rules are one part of a bigger geometry "
        "question. So you'll keep using them in every geometry topic."),
      L("So what makes a lines and angles question harder? Usually one of three things. A crowded figure, with several "
        "pairs of lines. Letters instead of numbers. Or a missing line that we have to add ourselves.",
        show(h4a, 'A crowded figure'), show(h4b, 'Letters instead of numbers'), show(h4c, 'Or a missing line')),
      L("We'll see each of them in the next questions, one at a time. [pause] Okay. I'll see you in the next video.",
        pt('h4a', 'We\'ll see each of them'))),
])

# ------------------------------------------------------------------------------------------------ geo30-g005 (Hebrew: two pairs of parallels)
# Hebrew: a full solve with the rules of lines only (one pair of parallel lines at a time, ignore the rest; the three
# angles on line b make 180), then the last-digit shortcut. V3: the whole figure, then FOCUS on one pair of parallel
# lines (the rest dimmed) with the Z traced, then the other pair, then the whole figure again with the values found.
_A5, _Q5, _P5 = (257.17, 137.06), (357.08, 137.06), (277.0, 222.94)
_g5lines = [('seg', 148.2, 137.06, 491.8, 137.06), ('seg', 148.2, 222.94, 491.8, 222.94), ('seg', 240.3, 64.06, 293.9, 295.9),
            ('seg', 340.2, 64.06, 393.8, 295.9), ('seg', 193.8, 312.2, 435.5, 52.95)]
_g5lab = [('txt', 128, 137.06, 'a', 'ink', 26, True), ('txt', 128, 222.94, 'b', 'ink', 26, True),
          ('txt', 224, 60, 'c', 'ink', 26, True), ('txt', 326, 60, 'd', 'ink', 26, True)]
g5 = GEO('g5', [
    ('line', _g5lines + _g5lab + [('par', 400, 137.06, 470, 137.06), ('par', 400, 222.94, 470, 222.94),
                                  ('par', 247, 94, 252, 116, 2), ('par', 347, 94, 352, 116, 2),
                                  ('arc', _A5[0], _A5[1], 25, 77, 180, 'small', '77°', 46), ('arc', _Q5[0], _Q5[1], 25, 47, 77, 'small', '56°', 46),
                                  ('arc', _P5[0], _P5[1], 31, 180, 227, 'red', 'x', 50)]),
    ('ab', [('dim', 115, 40, 395, 280), ('seg', 148.2, 137.06, 491.8, 137.06, 'ink', 4), ('seg', 148.2, 222.94, 491.8, 222.94, 'ink', 4),
            ('seg', 240.3, 64.06, 293.9, 295.9, 'ink', 4), ('txt', 128, 137.06, 'a', 'ink', 26, True), ('txt', 128, 222.94, 'b', 'ink', 26, True),
            ('txt', 224, 60, 'c', 'ink', 26, True), ('arc', _A5[0], _A5[1], 25, 77, 180, 'small', '77°', 46)]),
    ('z1', [('path', [(175, 137.06), _A5, _P5, (380, 222.94)], 'teal', 9), ('arc', _P5[0], _P5[1], 31, 257, 360, 'small', '77°', 52)]),
    ('cd', [('dim', 115, 40, 395, 280), ('seg', 240.3, 64.06, 293.9, 295.9, 'ink', 4), ('seg', 340.2, 64.06, 393.8, 295.9, 'ink', 4),
            ('seg', 193.8, 312.2, 435.5, 52.95, 'ink', 4), ('txt', 224, 60, 'c', 'ink', 26, True), ('txt', 326, 60, 'd', 'ink', 26, True),
            ('arc', _Q5[0], _Q5[1], 25, 47, 77, 'small', '56°', 46), ('arc', _P5[0], _P5[1], 44, 227, 257, 'small', '56°', 66)]),
], vb='115 40 395 280', w=470, title='Two pairs of parallel lines')
g5b = GEO('g5b', [
    ('line', _g5lines + _g5lab + [('wedge', _P5[0], _P5[1], 58, 180, 360, 'teal'),
                                  ('arc', _A5[0], _A5[1], 25, 77, 180, 'small', '77°', 46), ('arc', _Q5[0], _Q5[1], 25, 47, 77, 'small', '56°', 46),
                                  ('arc', _P5[0], _P5[1], 31, 180, 227, 'red', 'x', 50), ('arc', _P5[0], _P5[1], 44, 227, 257, 'small', '56°', 66),
                                  ('arc', _P5[0], _P5[1], 31, 257, 360, 'small', '77°', 52)]),
], vb='115 40 395 280', w=420, title='Two pairs of parallel lines')
k5a = IH('k5a', '$x+56°+77°=180°$', size=32)
k5b = IH('k5b', '$77°+56°=133°$', size=32)
k5c = IH('k5c', '$x=180°-133°=47°$', size=32)
k5d = I('k5d', '$7+6=13$: $\\ $ends in $3$ $\\to$ $x$ ends in $7$', size=30)
video('solve-geo30-g005', 'solution', qid='geo30-g005', slides=[
    SM('Method 1 · The math way', 'One pair at a time',
      L("In the accompanying figure, a is parallel to b, and c is parallel to d. What is the value of x?",
        pt('stem', 'In the accompanying figure', 'hl', 6.0), voice='calm', pause=0.5),
      L("We have two pairs of parallel lines, and x sits on line b, right next to two other angles. If we find those two "
        "angles, we can complete to one hundred eighty. [short pause] This question can also be solved with triangles or "
        "with quadrilaterals, but we haven't learned them yet, so we'll use only the rules of lines. Then we'll see a "
        "shortcut with the last digits.", pt('fig: x', 'x sits on line b')),
      L("[short pause] The math way first. Start with the first given, a is parallel to b, and line c cuts both of them. To see it simply, "
        "let's look only at these three lines and ignore the rest of the figure.", show(g5['line'], 'Start with the first given'),
        show(g5['ab'], 'look only at these three lines')),
      L("Seventy-seven degrees is a small angle where line c crosses line a. Line c crosses line b with the same angles, "
        "and all the small angles are equal. Look for the Z: from line a, down along line c, to line b. The two angles in "
        "its corners are equal. So the angle between line c and line b, below line b and to the right of line c, is also seventy-seven.",
        pt('fig: 77°', 'Seventy-seven degrees is a small angle'), show(g5['z1'], 'Look for the Z')),
      L("Now the second given, c is parallel to d, and the slanted line cuts both of them. Again, we look only at these "
        "three lines. Fifty-six is the small angle between the slanted line and line d. The slanted line crosses line c "
        "with the same angles. So the small angle between the slanted line and line c, just below line b, is also "
        "fifty-six.", show(g5['cd'], 'we look only at these'), pt('fig: 56°', 'Fifty-six is the small angle'))),
    SM('Method 1 · The math way', 'One pair at a time',
      L("Now back to the whole figure. Below line b, at the point where the three lines meet, there are three angles side "
        "by side, x, fifty-six and seventy-seven. Together they make the straight line b, so they add up to one hundred "
        "eighty.", show(g5b['line'], 'Now back to the whole figure'), show(k5a, 'so they add up to')),
      L("Seventy-seven plus fifty-six. Add the tens, seventy plus fifty is a hundred twenty, and seven plus six is "
        "thirteen, so together a hundred thirty-three. x plus a hundred thirty-three is a hundred eighty, so x is a "
        "hundred eighty minus a hundred thirty-three, which is forty-seven. Choice number four is our answer.",
        show(k5b, 'Add the tens'), show(k5c, 'so x is a hundred eighty minus'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    SM('Method 2 · Understanding: last digit', 'The last digit',
      L("[pause] Now by understanding. We could make the end shorter, with the last digits. Some students don't even write the equation. They "
        "say, one angle ends in seven, one ends in six, and x makes the sum a hundred eighty, which ends in zero. Seven plus "
        "six is thirteen, which ends in three. So x has to end in seven, because three plus seven makes a ten.",
        show(k5d, 'Seven plus six is thirteen')),
      L("Now straight to the choices. Thirty-three ends in three, out. Twenty-one ends in one, out. Fifty-nine ends in nine, "
        "out. Forty-seven ends in seven, so choice number four is our answer. On the exam, saving every second matters. "
        "[pause] Okay. I'll see you in the next question.", mk('cross', 'choice 1', 'Thirty-three ends in three'),
        mk('cross', 'choice 2', 'Twenty-one ends in one'), mk('cross', 'choice 3', 'Fifty-nine ends in nine'),
        mk('tick', 'choice 4', 'so choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo30-g006 (Hebrew: four lines through one point)
# Hebrew: three methods - the full math with an anchor (180 or 360; each angle gives its neighbour, 180 minus it; the four
# angles on one straight line), plugging in numbers (the same easy obtuse value for m, n and k; eliminate three choices),
# and the insight (m, n and k cover the full turn and x twice). Her remark on which method suits whom is kept short.
# V3: the neighbours drawn in one colour as she names them, the straight line traced; a second copy with the numbers;
# the overlap shown as three tints, with x tinted twice.
_O6 = (320.0, 180.0)
_g6lines = [('seg', 163.6, 180, 476.4, 180), ('seg', 191.9, 269.7, 448.1, 90.3), ('seg', 292.8, 334.1, 347.2, 25.9),
            ('seg', 398.2, 315.5, 241.8, 44.5)]
_g6giv = [('arc', 320, 180, 70, 35, 180, 'small', 'm', 92), ('arc', 320, 180, 55, 300, 80, 'small', 'n', 78),
          ('arc', 320, 180, 39, 180, 300, 'small', 'k', 60), ('arc', 320, 180, 94, 35, 80, 'red', 'x', 116)]
g6 = GEO('g6', [
    ('line', _g6lines + _g6giv),
    ('nm', [('wedge', 320, 180, 62, 180, 215, 'orange'), ('txt', 208, 214, '180−m', 'orange', 20)]),
    ('nn', [('wedge', 320, 180, 62, 80, 120, 'orange'), ('txt', 296, 70, '180−n', 'orange', 20)]),
    ('nk', [('wedge', 320, 180, 62, 120, 180, 'orange'), ('txt', 222, 132, '180−k', 'orange', 20)]),
    ('st', [('path', [(191.9, 269.7), (448.1, 90.3)], 'teal', 9)]),
], vb='150 18 345 322', w=380, title='Four lines through one point')
g6p = GEO('g6p', [
    ('line', _g6lines + [('arc', 320, 180, 70, 35, 180, 'small', '140°', 96), ('arc', 320, 180, 55, 300, 80, 'small', '140°', 84),
                         ('arc', 320, 180, 39, 180, 300, 'small', '140°', 66), ('arc', 320, 180, 94, 35, 80, 'red', 'x', 116)]),
    ('nb', [('wedge', 320, 180, 62, 180, 215, 'orange'), ('wedge', 320, 180, 62, 80, 120, 'orange'), ('wedge', 320, 180, 62, 120, 180, 'orange'),
            ('txt', 284, 192, '40°', 'orange', 17), ('txt', 313, 141, '40°', 'orange', 17), ('txt', 286, 161, '40°', 'orange', 17)]),
    ('xv', [('txt', 380, 64, '= 60°', 'red', 24)]),
], vb='150 18 345 322', w=380, title='Four lines through one point, with numbers')
g6o = GEO('g6o', [
    ('line', _g6lines),
    ('m', [('wedge', 320, 180, 92, 35, 180, 'teal'), ('arc', 320, 180, 70, 35, 180, 'small', 'm', 92)]),
    ('n', [('wedge', 320, 180, 92, 300, 80, 'orange'), ('arc', 320, 180, 55, 300, 80, 'orange', 'n', 78)]),
    ('k', [('wedge', 320, 180, 92, 180, 300, 'teal'), ('arc', 320, 180, 39, 180, 300, 'small', 'k', 60)]),
    ('x', [('arc', 320, 180, 98, 35, 80, 'red', 'x', 120)]),
], vb='150 18 345 322', w=380, title='m, n and k cover the full turn and x twice')
k6a = IH('k6a', '$(180°-m)+(180°-n)+(180°-k)+x=180°$', size=24)
k6a2 = I('k6a2', '$(180°-m)+(180°-n)$\n$+(180°-k)+x=180°$', size=28)
k6b = IH('k6b', '$x=m+n+k-360°$', size=32)
k6c = I('k6c', '$m=n=k=140°$: $\\ x=180°-3\\cdot40°=60°$', size=28)
k6d = I('k6d', '(1) $240°$ ✗ $\\quad$ (2) $140°$ ✗\n(3) negative ✗ $\\quad$ (4) $60°$ ✓', size=30)
k6e = IH('k6e', '$m+n+k=360°+x$', size=32)
video('solve-geo30-g006', 'solution', qid='geo30-g006', slides=[
    SM('Method 1 · The math way', 'An anchor: 180',
      L("In the accompanying figure, four lines intersect at one point. Which expression equals x?",
        pt('stem', 'In the accompanying figure', 'hl', 5.0), voice='calm', pause=0.5),
      L("What makes this question hard? Every angle is given with a letter, not a number. That's the main way exam "
        "geometry questions are made harder. [short pause] We'll solve it three ways, the math way, by plugging in "
        "numbers instead of the letters, and with an insight, for those who see it."),
      L("[short pause] The math way first. We need x, and there are many letters, so we need an anchor, a known total. That's "
        "either a full turn, three hundred sixty degrees, or a straight angle, one hundred eighty.",
        show(g6['line'], 'The math way first')),
      L("Start with m. The angle right next to m fills the rest of a straight line together with m, so it's one "
        "hundred eighty minus m. In the same way, the angle next to n is one hundred eighty minus n, and the angle next "
        "to k is one hundred eighty minus k.", pt('fig: m', 'Start with m'), show(g6['nm'], 'so it\'s one'),
        show(g6['nn'], 'the angle next to n'), show(g6['nk'], 'the angle next to k')),
      L("Now look at this slanted line. On one side of it there are exactly four angles, x and the three angles we just "
        "found. Together they make a straight angle, so they add up to one hundred eighty.", show(g6['st'], 'Now look at this slanted line'),
        show(k6a, 'so they add up to one hundred eighty'))),
    SM('Method 1 · The math way', 'An anchor: 180',
      L("Careful with the brackets. There's a plus in front of each bracket, so we can just drop them. The one hundred "
        "eighty on the left and the one hundred eighty on the right cancel. We keep x on the left, and move minus m, minus n "
        "and minus k to the right side as plus. The two one hundred eighties that are left make three hundred sixty, and "
        "they move across as minus three hundred sixty.", show(k6a2, 'Careful with the brackets')),
      L("So x equals m plus n plus k, minus three hundred sixty. Choice number four is our answer. Once you see the "
        "straight angle, the math is short. The hard part is seeing it on the last question of the section.",
        show(k6b, 'So x equals'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    SM('Method 2 · Plugging in numbers', 'Plugging in numbers',
      L("[pause] Now plugging in numbers. The question was made harder by putting letters instead of numbers, so we put "
        "numbers back. Why is that allowed? The right expression equals x for every possible m, n and k, so it also equals "
        "x for one example that we choose. We find x in our example, and then a choice that gives a different value is "
        "out.", show(g6p['line'], 'we put numbers back')),
      L("Which numbers? Numbers that fit the figure, and are easy. m looks obtuse, about one hundred forty degrees, so "
        "m is one hundred forty. And we choose one hundred forty for n and k too. Using the same number everywhere makes "
        "the choices much easier to check later.", pt('fig: m', 'm looks obtuse')),
      L("With numbers the neighbors are easy. The angle next to each one hundred forty is forty. Forty plus forty plus "
        "forty is a hundred twenty. With x they make a straight angle, so x is a hundred eighty minus a hundred twenty, "
        "which is sixty degrees, in our example.", show(g6p['nb'], 'The angle next to each'), show(g6p['xv'], 'which is sixty degrees'),
        show(k6c, 'in our example'))),
    SM('Method 2 · Plugging in numbers', 'Plugging in numbers',
      L("Now put one hundred forty into each choice and look for sixty. Choice number one, three times one hundred forty "
        "is four hundred twenty, minus one hundred eighty. That's far more than sixty, so it's out. Choice number two, one "
        "hundred forty minus one hundred forty is zero, plus one hundred forty is one hundred forty. Out. Choice number "
        "three, zero minus one hundred forty is negative. Out.", mk('cross', 'choice 1', 'so it\'s out.'),
        mk('cross', 'choice 2', 'is one hundred forty. Out'), mk('cross', 'choice 3', 'is negative. Out')),
      L("Choice number four, four hundred twenty minus three hundred sixty, is exactly sixty. Three choices are out, so "
        "choice number four is our answer. One more check: the four choices gave four different values, two hundred "
        "forty, one hundred forty, a negative and sixty. If two choices had given the same value, we'd plug in again with "
        "other numbers.", show(k6d, 'Choice number four, four hundred twenty'), mk('tick', 'choice 4', 'so choice number four is our answer'))),
    SM('Method 3 · Insight', 'Overlapping angles',
      L("[pause] And the insight. Look at the three angles m, n and k together. m and k go around most of the turn, and n "
        "covers the rest, so together they cover the whole full turn, three hundred sixty degrees. But they overlap. The "
        "part where m and n overlap is exactly x, so x is counted twice.", show(g6o['line'], 'Look at the three angles'),
        show(g6o['m'], 'm and k go around'), show(g6o['k'], 'most of the turn'), show(g6o['n'], 'and n covers the rest'),
        show(g6o['x'], 'is exactly x')),
      L("So m plus n plus k is three hundred sixty plus x. Move the three hundred sixty to the other side, and x equals m "
        "plus n plus k minus three hundred sixty. Choice number four. Strong students sometimes see this at once. Most "
        "students find plugging in numbers easier here, and the answer is just as sure. [pause] Okay. I'll see you in the "
        "next question.", show(k6e, 'So m plus n plus k'), mk('tick', 'choice 4', 'minus three hundred sixty. Choice number four'))),
])

# ------------------------------------------------------------------------------------------------ geo30-g007 (Hebrew: the bent line)
# Hebrew: the difficulty is the bent line; an auxiliary construction is needed. Constructions with triangles (extend a
# piece, or a line perpendicular to both) are mentioned, not used (triangles come later); the construction with the rules
# of lines: a line through the bend, parallel to a and b, splits x into two Z angles. Course addition kept: the zig-zag
# rule. V3: point to the bend first, then the dashed line in; each Z traced in its own colour with its value written.
_A7, _B7, _C7 = (320.0, 134.91), (354.59, 160.04), (320.0, 225.09)
_g7base = [('seg', 232, 134.91, 472, 134.91, 'ink', 2.5), ('seg', 232, 225.09, 472, 225.09, 'ink', 2.5), ('seg', 320, 134.91, 354.59, 160.04, 'ink', 2.5),
           ('seg', 320, 225.09, 354.59, 160.04, 'ink', 2.5), ('txt', 218, 134.91, 'a', 'ink', 18, True), ('txt', 218, 225.09, 'b', 'ink', 18, True),
           ('par', 430, 134.91, 462, 134.91), ('par', 430, 225.09, 462, 225.09)]
g7 = GEO('g7', [
    ('line', _g7base + [('arc', 320, 134.91, 30, 324, 360, 'small', '36°', 52), ('arc', 320, 225.09, 30, 0, 62, 'small', '62°', 52),
                        ('arc', 354.59, 160.04, 21, 144, 242, 'red', 'x', 40)]),
    ('bend', [('dot', 354.59, 160.04)]),
    ('aux', [('seg', 236, 160.04, 470, 160.04, 'teal', 2.2, True), ('par', 430, 160.04, 462, 160.04)]),
    ('z1', [('path', [(430, 134.91), _A7, _B7, (262, 160.04)], 'teal', 6), ('arc', 354.59, 160.04, 34, 144, 180, 'small', '36°', 60)]),
    ('z2', [('path', [(262, 160.04), _B7, _C7, (430, 225.09)], 'orange', 6), ('arc', 354.59, 160.04, 48, 180, 242, 'orange', '62°', 72)]),
], vb='205 110 275 130', w=520, title='Parallel lines and a bent line')
g7z = GEO('g7z', [
    ('line', _g7base),
    ('lt', [('arc', 320, 134.91, 30, 324, 360, 'small', '36°', 52), ('arc', 320, 225.09, 30, 0, 62, 'small', '62°', 52)]),
    ('rt', [('arc', 354.59, 160.04, 21, 144, 242, 'orange', 'x', 40)]),
], vb='205 110 275 130', w=520, title='The zig-zag rule')
k7a = IH('k7a', '$x=36°+62°=98°$', size=32)
k7b = I('k7b', 'Tips pointing left $=$ tips pointing right', size=30)
video('solve-geo30-g007', 'solution', qid='geo30-g007', slides=[
    S('Method 1 · The math way: a helper line',
      L("In the accompanying figure, a is parallel to b. What is the value of x?", pt('stem', 'In the accompanying figure', 'hl', 4.0),
        voice='calm', pause=0.5),
      L("The figure looks simple, two parallel lines, and the angles are numbers. So what makes it hard? The line between "
        "a and b is bent, and x is the angle between its two pieces. If one straight line cut both parallel lines, we'd "
        "know what to do, but here it's not clear where to start. [short pause] We'll solve it with a line we add "
        "ourselves, and then with a shortcut, the zig-zag rule.", pt('fig: x', 'x is the angle between its two pieces')),
      L("[short pause] The math way first. A line we add to the figure to help us solve it is called an auxiliary line. There are several "
        "options here. We could extend one of the pieces until it meets the other parallel line, or draw a line "
        "perpendicular to both parallel lines. Those options make triangles, which we'll learn later. If you solved it "
        "that way, that's completely fine. Here we'll use only the rules of lines.", show(g7['line'], 'There are several')),
      L("So here's our auxiliary line. Start at the bend, the point where x is, and draw a line through it, parallel to "
        "line a and to line b.", show(g7['bend'], 'Start at the bend'), show(g7['aux'], 'and draw a line through it')),
      L("The new line splits x into two parts. The upper part makes a Z with line a: from line a, along the upper piece, "
        "to the new line. The angles in the corners of a Z are equal, so the upper part is thirty-six.",
        pt('fig: 36°', 'The upper part makes a Z'), show(g7['z1'], 'so the upper part is thirty-six')),
      L("The lower part makes a Z with line b, the same way. So the lower part is sixty-two.", pt('fig: 62°', 'The lower part makes a Z'),
        show(g7['z2'], 'So the lower part is sixty-two')),
      L("So x is thirty-six plus sixty-two, which is ninety-eight degrees. Choice number two is our answer. Once you add "
        "the line, the question becomes an easy one. The hard part is realizing that a line is needed, and which one.",
        show(k7a, 'So x is thirty-six plus sixty-two'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Understanding: the zig-zag rule',
      L("[pause] Now a shortcut by understanding, for a line that zig-zags between two parallel lines. Look at each marked angle and ask, "
        "where does its tip, the vertex, point? The thirty-six points left, and the sixty-two points left too. x points "
        "right.", show(g7z['line'], 'Now a shortcut'), show(g7z['lt'], 'The thirty-six points left'), show(g7z['rt'], 'x points right')),
      L("The rule is, the angles that point left add up to the angles that point right. So x is thirty-six plus sixty-two, "
        "ninety-eight, in one step. Choice number two. It works because it's exactly what the line through the bend showed "
        "us. If you're not sure, draw the parallel line through the bend. That always works. [pause] Okay. I'll see you in "
        "the next question.", show(k7b, 'The rule is'), mk('tick', 'choice 2', 'ninety-eight, in one step'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t30-03 (added: two bends)
# Course question. Methods: the zig-zag rule (taught in g007), then a parallel line through each bend (always works).
# V3: tips coloured by direction; then the two dashed lines, one at a time, each Z traced and its value written.
_P1, _B1, _B2, _P2 = (250.0, 90.0), (326.61, 154.28), (248.66, 199.28), (378.23, 290.0)
_g8base = [('seg', 120, 90, 540, 90), ('seg', 120, 290, 540, 290), ('seg', 250, 90, 326.61, 154.28), ('seg', 326.61, 154.28, 248.66, 199.28),
           ('seg', 248.66, 199.28, 378.23, 290), ('txt', 104, 90, 'a', 'ink', 26, True), ('txt', 104, 290, 'b', 'ink', 26, True),
           ('par', 450, 90, 500, 90), ('par', 450, 290, 500, 290)]
_g8arcs = [('arc', 250, 90, 26, 320, 360, 'small', '40°', 50), ('arc', 326.61, 154.28, 22, 140, 210, 'red', 'x', 42),
           ('arc', 248.66, 199.28, 22, 325, 30, 'small', '65°', 46), ('arc', 378.23, 290, 26, 145, 180, 'small', '35°', 50)]
g8z = GEO('g8z', [
    ('line', _g8base + _g8arcs),
    ('lt', [('arc', 250, 90, 26, 320, 360, 'small', '40°', 50), ('arc', 248.66, 199.28, 22, 325, 30, 'small', '65°', 46)]),
    ('rt', [('arc', 326.61, 154.28, 22, 140, 210, 'orange', 'x', 42), ('arc', 378.23, 290, 26, 145, 180, 'orange', '35°', 50)]),
], vb='90 68 470 240', w=520, title='The zig-zag rule, two bends')
g8 = GEO('g8', [
    ('line', [('seg', 205, 90, 420, 90, 'ink', 2.2), ('seg', 205, 290, 420, 290, 'ink', 2.2), ('seg', 250, 90, 326.61, 154.28, 'ink', 2.2),
              ('seg', 326.61, 154.28, 248.66, 199.28, 'ink', 2.2), ('seg', 248.66, 199.28, 378.23, 290, 'ink', 2.2),
              ('txt', 212, 80, 'a', 'ink', 16, True), ('txt', 212, 280, 'b', 'ink', 16, True),
              ('arc', 250, 90, 22, 320, 360, 'small'), ('txt', 286.3, 106.9, '40°', 'teal', 15),
              ('arc', 326.61, 154.28, 18, 140, 210, 'red'), ('txt', 264.8, 148.9, 'x', 'red', 15),
              ('arc', 248.66, 199.28, 18, 325, 30, 'small'), ('txt', 314.6, 197.0, '65°', 'teal', 15),
              ('arc', 378.23, 290, 22, 145, 180, 'small'), ('txt', 338.8, 275.6, '35°', 'teal', 15)]),
    ('aux2', [('dot', 248.66, 199.28), ('seg', 210, 199.28, 410, 199.28, 'teal', 1.8, True)]),
    ('z35', [('path', [(300, 290), _P2, _B2, (330, 199.28)], 'teal', 5), ('arc', 248.66, 199.28, 28, 325, 360, 'small'), ('txt', 285.7, 214.3, '35°', 'teal', 15)]),
    ('r30', [('arc', 248.66, 199.28, 34, 0, 30, 'orange'), ('txt', 289.5, 182.8, '30°', 'orange', 15)]),
    ('aux1', [('dot', 326.61, 154.28), ('seg', 210, 154.28, 410, 154.28, 'teal', 1.8, True)]),
    ('z30', [('path', [(330, 199.28), _B2, _B1, (250, 154.28)], 'orange', 5), ('arc', 326.61, 154.28, 28, 180, 210, 'orange'), ('txt', 288.2, 165.3, '30°', 'orange', 15)]),
    ('z40', [('path', [(330, 90), _P1, _B1, (250, 154.28)], 'teal', 5), ('arc', 326.61, 154.28, 34, 140, 180, 'small'), ('txt', 285.8, 137.8, '40°', 'teal', 15)]),
], vb='200 70 225 235', w=400, title='A parallel line through each bend')
k8a = IH('k8a', '$40°+65°=x+35°$', size=32)
k8b = IH('k8b', '$x=105°-35°=70°$', size=32)
k8d = IH('k8d', '$x=40°+30°=70°$', size=32)
video('solve-q-r26-t30-03', 'solution', qid='q-r26-t30-03', slides=[
    S('Method 1 · Understanding: the zig-zag rule',
      L("In the accompanying figure, a is parallel to b. What is the value of x?", pt('stem', 'In the accompanying figure', 'hl', 4.0),
        voice='calm', pause=0.5),
      L("This time the line between a and b bends twice. [short pause] We'll solve it two ways, with the zig-zag rule, and "
        "then with a parallel line through each bend.", pt('fig: x', 'bends twice')),
      L("[short pause] First by understanding, with the zig-zag rule. The angles whose tips point left add up to the angles whose tips point right. Forty "
        "points left, and sixty-five points left. x points right, and thirty-five points right.", show(g8z['line'], 'The zig-zag rule'),
        show(g8z['lt'], 'Forty points left'), show(g8z['rt'], 'x points right')),
      L("So forty plus sixty-five equals x plus thirty-five. Forty plus sixty-five is a hundred five. x plus thirty-five is "
        "a hundred five, so x is a hundred five minus thirty-five, which is seventy. Choice number two is our answer.",
        show(k8a, 'So forty plus sixty-five equals'), show(k8b, 'so x is a hundred five minus'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Careful, a hundred five, choice number three, adds only the left side. And a hundred forty, choice number four, "
        "adds everything.", mk('cross', 'choice 3', 'adds only the left side'), mk('cross', 'choice 4', 'adds everything'))),
    S('Method 2 · The math way: helper lines',
      L("[pause] Now the math way. Not sure you remember the rule? Draw a parallel line through each bend. That always works. Start at the "
        "bottom, at the lower bend, the sixty-five, and draw a line through it, parallel to a and b.",
        show(g8['line'], 'Not sure you remember'), show(g8['aux2'], 'and draw a line through it')),
      L("The new line splits the sixty-five in two. The lower part makes a Z with the thirty-five at line b, so it's "
        "thirty-five. The upper part is sixty-five minus thirty-five, which is thirty.", show(g8['z35'], 'The lower part makes a Z'),
        show(g8['r30'], 'The upper part is sixty-five')),
      L("Now the upper bend, the x. Draw a parallel line through it too. It splits x in two. The lower part of x makes a Z "
        "with that thirty, so it's thirty. The upper part of x makes a Z with the forty at line a, so it's forty.",
        show(g8['aux1'], 'Draw a parallel line through it too'), show(g8['z30'], 'The lower part of x'), show(g8['z40'], 'The upper part of x')),
      L("So x is forty plus thirty, which is seventy. Choice number two again. [pause] Okay. I'll see you in the next "
        "question.", show(k8d, 'So x is forty plus thirty'), mk('tick', 'choice 2', 'Choice number two again'))),
])

# placement (right column)
for _g in (g5, g5b, g6, g6p, g6o, g7, g7z, g8z, g8): _R(_g, 235)
_R(g8, 230, x=1080)
for _it, _y in ((k5a, 545), (k5b, 595), (k5c, 645), (k5d, 250), (k6a, 610), (k6a2, 250), (k6b, 345), (k6c, 610), (k6d, 250),
                (k6e, 610), (k7a, 500), (k7b, 500), (k8a, 525), (k8b, 585), (k8d, 665)):
    _R(_it, _y)


# carry-over boxes on the continuation slides (V2): the next step uses these results
CARRY30 = globals().get('CARRY30', {})

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
 "geo30-g002": "In the accompanying figure, $a\\parallel b$. The marked lines are perpendicular. What is the value of $x$?",
 "q-r26-t30-01": "In the accompanying figure, lines $a$ and $b$ are both perpendicular to line $c$. Line $d$ crosses lines $a$ and $b$. What is the value of $x$?",
 "q-r26-t30-02": "Points $A$, $B$, $C$ and $D$ lie on a line in this order, as shown in the accompanying figure.\nGiven:\n$\\begin{cases} AC=11 \\\\ BD=14 \\\\ AD=20 \\end{cases}$\nWhat is the length of $BC$?",
 "geo30-g005": "In the accompanying figure, $a\\parallel b$ and $c\\parallel d$. What is the value of $x$?",
 "geo30-g006": "In the accompanying figure, four lines intersect at one point. Which expression equals $x$?",
 "geo30-g007": "In the accompanying figure, $a\\parallel b$. What is the value of $x$?",
 "q-r26-t30-03": "In the accompanying figure, $a\\parallel b$. What is the value of $x$?"
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
MV.carry(_types.SimpleNamespace(**globals()), CARRY30)
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
