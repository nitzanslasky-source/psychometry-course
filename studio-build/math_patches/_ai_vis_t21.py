"""Topic 21 (Trial, limits and patterns) - the scripts for the teacher's own-voice reading (2026-10-18), written from the
first draft to the guide (R1-R36, W1-W21, the clarity style, the Codex review standard, V1-V4, the method vocabulary),
built like topic 20 (math_patches/_ai_vis_t20.py: the DSL, the visual passes and the stem-part highlighting are copied
here, so the topics stay independent) and topics 30-33 (the camera lesson in parts, math_patches/_camera_parts.py).

The camera lesson 'wp-001' (the first lesson of word problems) is read with the camera on, in parts of about 3-4
minutes. Every other topic-21 video gets a script that SHE reads aloud in the Reading Studio (reading_studio.py);
reading_to_video.py then times the handwriting and the visuals to her words. The summary video r26-t21-summary is not
read: summary_pages/t21.json (python3 summary_pages.py 21) replaces it.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t21.py [vid ...] writes it);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t21.py ai_redo_t21() (runs LAST) rebuilds the slides from studio_slides(vid) and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), what they really ask, the roadmap, EVERY method of the Hebrew
solution (wp 20-1067; each from the givens, R30) plus the English course's added methods, every step with what / why /
what it means (R31, W21), every calculation said aloud (R33), traps at the step, "choice number N" (R34), the answer,
then "Choice number N is our answer, and I'll see you in the next question." No verdict. Concept map (NEW / REMINDER per
video): ~/Downloads/Topic-21-AI-scripts-review.md.

Spec DSL (as in topic 20)
  video(vid, kind, slides, qid=None)  ·  S(title, *lines, sb=None)  ·  L(say, *cues, voice=None, pause=None)
  I(name, tex, size=36, col=0, hand=None) / IH(name, tex) (hand-written)  ·  TBL / FLAGS (figures built in layers)
  cues: show(item, phrase) · pt(target, phrase, style=None, dur=None) · mk(kind, target, phrase)
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t21ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-21 flow order of the scripts
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
CAM_BASE = 'wp-001'
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
            'style': "the teacher reads it herself (Reading Studio), topic-21 scripts (2026-10-18): math_patches/_ai_vis_t21.py is "
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



# ------------------------------------------------------------------------------------------- topic-21 figures (V1)
# Word problems have no signature visual in the library for this topic; the Hebrew draws two things: a table / list that
# is filled in as she speaks (the hair ties, the eggs: "נכין איזושהי טבלה... אתם לא באמת צריכים") and the circle-and-line
# picture of a repeating pattern (the soccer kids, wp 900-936: "עם כדור עיגול, בלי כדור קו"). Both are built in layers here,
# each layer at the spoken words (shown right after its base, never another item in between).
TEAL, INK = MV.TEAL, MV.INK


def TBL(name, cols, nrows, colw, layers, rowh=56, col=0, w=None, title='Table', base=(), size=28):
    """a table built in layers: the empty table (with the `base` cells), then each layer's cells.
    layers = [(key, [(row, col, text[, colour]), ...]), ...]; colour 'teal' (found), 'red' (ruled out), default ink."""
    W, H, body, cell, xs = MV._table(cols, nrows, colw, rowh)
    colour = {'teal': TEAL, 'red': RED, None: INK}
    def one(c):
        x, y = cell(c[0], c[1]); k = c[3] if len(c) > 3 else None
        cover = ''
        if k == 'cover':     # a new value in place of an old one: a white patch over the old value, then the new one
            k = 'teal'; cover = '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#ffffff"/>' % (
                xs[c[1]] + 2, y - rowh * .62, xs[c[1] + 1] - xs[c[1]] - 4, rowh * .9)
        return cover + MV._text(x, y, c[2], size, colour[k])
    txt = lambda cs: ''.join(one(c) for c in cs)
    out = [('line', MV._svg(W, H, body + txt(base), title))]
    for key, cs in layers:
        out.append((key, MV._svg(W, H, txt(cs), '%s: %s' % (title, ', '.join(str(c[2]) for c in cs)))))
    return MV.items(_layers, name, out, w=w, col=col)


def FLAGS(name, n, layers, col=0, w=None, title='The pattern'):
    """the Hebrew circle-and-line picture: positions 1..n, a circle = red (has it), a line = not red; numbers under them.
    layers = [(key, [(position, 'red' | 'no'), ...]), ...]"""
    dx, x0, y = 52, 34, 46
    W, H = x0 * 2 + dx * (n - 1), 112
    body = ''.join(MV._text(x0 + dx * (i - 1), 98, str(i), 24, INK, weight='bold') for i in range(1, n + 1))
    body += '<line x1="10" y1="72" x2="%d" y2="72" stroke="#c9d3db" stroke-width="1.5"/>' % (W - 10)
    out = [('line', MV._svg(W, H, body, title + ': positions 1 to %d' % n))]
    for key, ms in layers:
        b = ''
        for p, kind in ms:
            x = x0 + dx * (p - 1)
            if kind == 'red':
                b += '<circle cx="%.1f" cy="%d" r="15" fill="%s" stroke="%s" stroke-width="3"/>' % (x, y, '#f6d4da', RED)
            else:
                b += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % (x - 15, y, x + 15, y, INK)
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, ', '.join('%d %s' % m for m in ms)))))
    return MV.items(_layers, name, out, w=w, col=col)


# =================================================================================================================
# THE SCRIPTS (topic-21 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-21-AI-scripts-review.md.
# Study plan before topic 21: 1, 30, 2, 4, 31, 6, 8, 32, 9, 10, 33, 51 (+ verbal). So must / could / cannot, remainders and
# the last digit of a product (topic 1), the least common multiple (topic 2) and plugging in numbers / answers (topic 51)
# are REMINDERS; worst luck + 1 (topic 20) and remainder patterns (topic 15) come LATER in the plan, so they are taught
# in full here.
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ wp-001 (camera lesson)
# Hebrew: the topic has no stand-alone first lesson - "ניסוי וטעייה תאוריה" (wp 14-18) goes straight into the three types
# (general problems wp 20-117, min-max wp 119-162, patterns wp 164-236). The English first lesson is the overview of the
# chapter; here it gets real examples (2-3 per idea): a trial-and-error story twice (the second try changes one number),
# a taste of each type, and the must / could / cannot reminder (topic 1) with four number cases.
# Split into 2 parts at the idea boundary (CAMERA_SPLIT at the end of the scripts).
a0 = I('a0', 'A total in parts $\\ \\cdot\\ $ a ratio $\\ \\cdot\\ $ a short list of cases', size=30)
a1 = I('a1', 'Pens $3$ dollars, notebooks $5$ dollars, total $19$ dollars', size=30)
a2 = IH('a2', '1 notebook: $\\ 19-5=14$, $\\ 14\\div3$ ✗', size=30)
a3 = IH('a3', '2 notebooks: $\\ 19-10=9$, $\\ 9\\div3=3$ pens ✓', size=30)
a4 = IH('a4', '3 notebooks: $\\ 19-15=4$ ✗', size=30)
a5 = I('a5', 'Total $20$ dollars:', size=30)
a6 = IH('a6', '1 notebook: $\\ 20-5=15$, $\\ 15\\div3=5$ pens ✓', size=30)
b0 = I('b0', '1 $\\cdot$ General problems: nothing says what to try first', size=30)
b1 = I('b1', '2 $\\cdot$ Minimum and maximum: which way to push', size=30)
b1e = IH('b1e', '3 friends, 10 sweets: $\\ 1+1+8$', size=30)
b1f = IH('b1f', '5 friends, 20 sweets: $\\ 1+1+1+1+16$', size=30)
b2 = I('b2', '3 $\\cdot$ Patterns: write the items one by one', size=30)
b2e = IH('b2e', '$3,\\ 6,\\ 12,\\ 24$', size=30)
b2f = IH('b2f', '$20,\\ 17,\\ 14,\\ 11$', size=30)
c0 = I('c0', 'Two positive whole numbers, sum $14$', size=30)
c1 = IH('c1', 'Could one be 3? $\\ 3+11=14$ ✓', size=30)
c2 = IH('c2', 'Must one be odd? $\\ 2+12=14$ ✗', size=30)
c3 = IH('c3', 'Must one be at least 7? $\\ $both $\\le6$: $\\ 6+6=12<14$, so yes ✓', size=30)
c4 = IH('c4', 'Can both be bigger than 7? $\\ 8+8=16>14$ ✗', size=30)
c5 = I('c5', 'could $\\to$ one example $\\quad$ must $\\to$ every case $\\quad$ cannot $\\to$ no case', size=26)
d0 = I('d0', 'Try the question first $\\ \\to\\ $ then watch and compare', size=30)
video('wp-001', 'lesson', slides=[
    S('How to Approach Word Problems',
      L("Welcome back, and now word problems. A word problem is a short story, with a question about it.")),
    S('What a word problem is',
      L("The story can be about anything. A queue at a shop, a water tank, a trip, or friends sharing sweets. But under every story there's some math."),
      L("Word problems are a big part of the quantitative section. Some questions are pure word problems. And many algebra and geometry questions are also written as a story. So this chapter pays off everywhere."),
      L("We won't learn a trick for every story. We'll learn to see what's under it. Sometimes it's a total that's cut into parts. Sometimes it's a ratio. And sometimes it's just a short list of cases.",
        show(a0, "Sometimes it's a total"))),
    S('Trial and error',
      L("We start with the most down-to-earth tool there is, trial and error. Trial and error means we try, we get it wrong, and we try again. There's no equation and no formula."),
      L("Let's see it in numbers. A shop sells pens at three dollars and notebooks at five dollars. Dan spends exactly nineteen dollars, and he buys at least one of each. How many notebooks does he buy?", show(a1, 'A shop sells pens')),
      L("What do we try? The notebooks, because there are fewer options. Four notebooks would already cost twenty dollars, more than nineteen. So Dan buys one, two or three notebooks. Let's try them in order."),
      L("One notebook costs five dollars, so nineteen minus five leaves fourteen for the pens. Fourteen doesn't divide by three, because three times four is twelve and three times five is fifteen. So one notebook doesn't work.",
        show(a2, 'leaves fourteen for the pens')),
      L("Two notebooks cost ten dollars, so nineteen minus ten leaves nine. Nine divided by three is three pens. That works, two notebooks and three pens.", show(a3, 'Two notebooks cost ten dollars')),
      L("And three notebooks cost fifteen, which leaves four dollars. Four doesn't divide by three, so that's out too. We tried in order, so we know the list is complete. The only answer is two notebooks.",
        show(a4, 'three notebooks cost fifteen')),
      L("Now let's change one thing. Say Dan spends twenty dollars. One notebook leaves twenty minus five, fifteen. Fifteen divided by three is five pens. It works on the very first try.", show(a5, 'Say Dan spends twenty dollars'),
        show(a6, 'One notebook leaves twenty minus five')),
      L("That's trial and error. Sometimes the first try works, and sometimes it takes a few. Each try is just a check against the story. And when we try in order, nothing gets lost.")),
    S('Three types',
      L("Trial and error comes in three types, and each type gets its own lesson, with questions."),
      L("Type one is general problems. Nothing in the question tells us what to try first. So we just try, like we did with the pens and the notebooks.", show(b0, 'Type one is general problems')),
      L("Type two is minimum and maximum. Here a little understanding tells us which way to push, so we need fewer tries. For example, three friends share ten sweets, and each gets at least one. What's the most one friend can get? To make one share as big as possible, we give the others as little as possible, one each. So the most is ten minus two, which is eight.", show(b1, 'Type two is minimum and maximum'), show(b1e, 'So the most is ten minus two')),
      L("The same push with other numbers. Five friends share twenty sweets. The other four get one each, that's four. So the most one friend can get is twenty minus four, sixteen.", show(b1f, 'The other four get one each')),
      L("Type three is patterns. A rule repeats again and again, and we write the items one by one. For example, a number starts at three and doubles each time. Three, six, twelve, twenty-four. So the fourth number is twenty-four.",
        show(b2, 'Type three is patterns'), show(b2e, 'starts at three and doubles')),
      L("Another rule. Start at twenty and take away three each time. Twenty, seventeen, fourteen, eleven. Here we hardly think and hardly make mistakes. It's mostly trial, and very little error.",
        show(b2f, 'Start at twenty and take away three'))),
    S('Must, could, cannot',
      L("One reminder from the first topic, because many of these questions ask it. Three words decide the question. Must, could and cannot."),
      L("Two positive whole numbers add up to fourteen. Could one of them be three? Yes. Three plus eleven is fourteen. For could, one example that works is enough.", show(c0, 'Two positive whole numbers'),
        show(c1, 'Three plus eleven is fourteen')),
      L("Must one of them be odd? Three and eleven are both odd. But two and twelve also add up to fourteen, and both are even. So one allowed example fails, and must is out.", show(c2, 'two and twelve also add up')),
      L("Must one of them be at least seven? Here no example can prove it, we need a reason. If both were six or less, the sum would be at most six plus six, twelve. That's less than fourteen. So yes, one of them is always at least seven.", show(c3, 'If both were six or less')),
      L("And cannot means it never works, for any allowed numbers. Can both be bigger than seven? No. The smallest whole numbers bigger than seven are eight and eight, and that's already sixteen. So could needs one example, must needs every case, and cannot means no case at all.",
        show(c4, 'Can both be bigger than seven'), show(c5, 'So could needs one example'))),
    S('How to use this chapter',
      L("Every question in this chapter comes before its video. So try it on paper first. Stuck? Write what you do know, the first try or two. Then watch the video, and compare.", show(d0, 'try it on paper first')),
      L("Let's start with type one. [pause] I'll see you in the next video.")),
])
CAMERA_SPLIT = ('wp-001', 'How to Approach Word Problems', [(1, None), (3, "Now let's look at the three types of trial and error.")])

# ------------------------------------------------------------------------------------------------ wp-003 General Problems
# Hebrew wp 20-33: general problems depend on luck; nothing says what to try first; sometimes the first try works,
# sometimes a few - "that's exactly how you're expected to solve them". REMINDER of the camera lesson's type one.
e0 = I('e0', 'Nothing says what to try first $\\ \\to\\ $ just try', size=30)
e1 = I('e1', 'The first try works $\\quad$ or it takes a few', size=30)
video('wp-003', 'lesson', slides=[
    S('General Problems',
      L("Welcome back. Now type one of trial and error, general problems.")),
    S('Try and err',
      L("What makes a problem a general problem? It depends on luck. Nothing in the question says try this first. We read it, and the only way forward is to try.", show(e0, 'Nothing in the question says')),
      L("Sometimes we hit it on the first try. Sometimes it takes a few tries. Both are fine, and that's exactly how these questions are meant to be solved.", show(e1, 'Sometimes we hit it')),
      L("Let's see two questions of this type. [pause] I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ wp21-g004 (bubbles)
# Hebrew wp 35-70 (the spaceships): draw, the first shot must hit a large one, the road splits into two routes, follow one,
# lucky on the first route; the other route shows what an "error" looks like. English adds the net change per pop
# (Insight). NEW: following a story and splitting into routes; "exactly three pops" (6 and 10 are earlier stages).
g4a = IH('g4a', 'Start: $\\ 2$ large', size=30)
g4b = IH('g4b', 'Pop 1 (large): $\\ 1$ large $+\\ 5$ small $=6$', size=30)
g4c = IH('g4c', 'Pop 2 (large): $\\ 0$ large $+\\ 10$ small $=10$', size=30)
g4d = IH('g4d', 'Pop 3 (small): $\\ 10-1=9$ ✓', size=30)
g4e = IH('g4e', 'Pop 1 (large): $\\ 1$ large $+\\ 5$ small $=6$', size=30)
g4f = IH('g4f', 'Pop 2 (small): $\\ 1$ large $+\\ 4$ small $=5$', size=30)
g4g = IH('g4g', 'Pop 3 (large): $\\ 0$ large $+\\ 9$ small $=9$', size=30)
g4h = IH('g4h', 'Pop 3 (small): $\\ 1$ large $+\\ 3$ small $=4$ ✗', size=30)
g4i = IH('g4i', 'Large pop: $\\ -1+5=+4$', size=30)
g4j = IH('g4j', 'Small pop: $\\ -1$', size=30)
g4k = IH('g4k', 'Two large, one small: $\\ 2+4+4-1=9$', size=30)
g4l = IH('g4l', 'One large, two small: $\\ 2+4-1-1=4$', size=30)
video('solve-wp21-g004', 'solution', qid='wp21-g004', slides=[
    S('Method 1 · Plugging in numbers: trial and error',
      L("A phone game starts with two large bubbles on the screen. Popping a large bubble splits it into five small bubbles. Popping a small bubble makes it disappear. After exactly three pops, how many bubbles can be on the screen?", pt('stem', 'A phone game', 'hl', 12.0), voice='calm', pause=0.5),
      L("So they don't ask how many there must be. They ask what can be. One road that really happens and ends on a choice is enough. Nothing tells us which bubble to pop first, so this is a general problem. [short pause] We'll solve it in two different ways, by trial and error, and then with an insight.", pt('stem: ask', 'They ask what can be')),
      L("[short pause] Let's start with trial and error. We try one road of pops and follow the game. At the start there are two large bubbles, and no small ones.", show(g4a, 'At the start there')),
      L("Pop one. There are no small bubbles yet, so the first pop has to hit a large one. That large bubble is gone, and five small ones appear. So we have one large and five small. One plus five is six bubbles. Six is in the choices, but that's after one pop only, so we keep going.",
        show(g4b, 'One plus five is six')),
      L("Now the road splits, because we can pop the large one or a small one. Let's take one road, and pop the other large bubble. It turns into five more small ones. So there are no large ones left, and five plus five is ten small ones. Ten is a choice too, but that's after two pops. The question says exactly three pops.", show(g4c, 'five plus five is ten')),
      L("Pop three. Only small bubbles are left, so we pop a small one, and it disappears. Ten minus one is nine bubbles.",
        show(g4d, 'Ten minus one is nine')),
      L("Nine is in the choices. They ask what can be, and this road really happens. So there can be nine bubbles, and choice number three is our answer. This time we were lucky on the first road.",
        mk('tick', 'choice 3', 'choice number three is our answer'))),
    S('Method 1 · Plugging in numbers: trial and error',
      L("What if we had taken the other road? Let's see it, because in another question the first road can miss. The first pop is the same, one large and five small.", show(g4e, 'The first pop is the same')),
      L("This time, pop two hits a small bubble, and it disappears. One of the five small ones is gone, so four small are left. So we have one large and four small, five bubbles.", show(g4f, 'One of the five small ones')),
      L("Pop three can go two ways. If we pop the large one, it turns into five small ones. Four plus five is nine small bubbles, nine again.", show(g4g, 'If we pop the large one')),
      L("If we pop a small one, one large and three small are left, four bubbles. Four is not in the choices. If this had been our first road, we'd just try again. That's trial and error. We try, we miss, and we try again.",
        show(g4h, 'If we pop a small one')),
      L("So every road ends at nine or at four, and only nine is in the choices. Choice number three is our answer.",
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      sb='Method 1 · Plugging in numbers: trial and error'),
    S('Method 2 · Insight: the change per pop',
      L("[pause] Now the insight. Instead of following the bubbles, let's look at what one pop changes. A large pop takes away one bubble and adds five. Minus one plus five is plus four.", show(g4i, 'A large pop takes')),
      L("A small pop just takes one bubble away, so it's minus one.", show(g4j, 'A small pop just takes')),
      L("There are only two large bubbles, and the first pop must be large. Say two pops are large and one is small. We start at two. Two plus four is six. Six plus four is ten. And ten minus one is nine.",
        show(g4k, 'We start at two')),
      L("Say only one pop is large. Two plus four is six, and then two small pops take away two. Six minus two is four. That's the four we found before. So the totals are nine and four, and only nine is in the choices. Choice number three is our answer, and I'll see you in the next question.", show(g4l, 'Say only one pop is large'),
        mk('tick', 'choice 3', 'only nine is in the choices'))),
])

# ------------------------------------------------------------------------------------------------ wp21-g005 (the line)
# Hebrew wp 73-109 (the traffic jam): no choice but to build lines and test the answers; start with one of each (at
# least one of each); the quick-adding tip (join the pieces into round numbers); the impossible length is skipped
# because even the smallest addition jumps past it. English adds the gap insight (length + 2 divides by 6).
h5a = IH('h5a', '1 truck $+$ 1 car: $\\ 10+2+4=16$', size=30)
h5b = IH('h5b', 'car $+$ gap $=6$ $\\quad$ truck $+$ gap $=12$', size=30)
h5c = IH('h5c', 'one more car: $\\ 16+6=22$', size=30)
h5d = IH('h5d', 'another car: $\\ 22+6=28$', size=30)
h5e = IH('h5e', '$16\\to22$: $\\ 20$ is skipped ✗', size=30)
h5f = IH('h5f', 'truck $12$, car $6$, the last gap missing: $\\ -2$', size=30)
h5g = IH('h5g', 'length $+\\ 2$ divides by $6$', size=30)
h5h = IH('h5h', '$16+2=18$ ✓ $\\quad 20+2=22$ ✗', size=30)
video('solve-wp21-g005', 'solution', qid='wp21-g005', slides=[
    S('Method 1 · Plugging in the answers',
      L("A line of vehicles waits at a traffic light. It has at least one truck ten meters long, and at least one car four meters long. There is a two meter gap between neighboring vehicles, and no gap at either end of the line. Which total length of the line is impossible?", pt('stem', 'A line of vehicles', 'hl', 14.0), voice='calm', pause=0.5),
      L("They ask what's impossible. So every length we can really build is out, and we cross out three choices. [short pause] We'll solve it in two different ways, by plugging in the answers, and then with an insight about the gaps.",
        pt('stem: ask', "They ask what's impossible")),
      L("[short pause] Let's start by plugging in the answers, and build lines in order. The question says at least one of each, so we have no choice. The shortest line has one truck and one car, with one gap between them."),
      L("Ten for the truck, plus two for the gap, is twelve. Twelve plus four for the car is sixteen meters. Sixteen is choice number one. We just built it, so it's possible, and choice number one is out.",
        show(h5a, 'Ten for the truck'), mk('cross', 'choice 1', 'and choice number one is out')),
      L("Now a tip for quick adding. Every extra vehicle comes with its own gap, so let's glue each vehicle to its gap. A car plus a gap is four plus two, six. A truck plus a gap is ten plus two, twelve.",
        show(h5b, 'A car plus a gap')),
      L("Let's add one more car to our sixteen. Sixteen plus six is twenty-two. That's choice number three, so it's possible, and it's out.", show(h5c, 'Sixteen plus six'), mk('cross', 'choice 3', "and it's out")),
      L("Choice number four is twenty-eight. Let's add another car. Twenty-two plus six is twenty-eight. Possible, so it's out too.", show(h5d, 'Twenty-two plus six'), mk('cross', 'choice 4', "so it's out too")),
      L("Only choice number two is left, twenty. Let's see why it can't be built. Sixteen is the shortest line. The smallest thing we can add is a car with its gap, six meters. That jumps from sixteen straight to twenty-two, and skips right over twenty. So twenty is impossible, and choice number two is our answer.",
        show(h5e, 'That jumps from sixteen'), mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Insight: the gaps',
      L("[pause] Now the insight. Let's give every vehicle the gap that comes after it. Then each truck counts as ten plus two, twelve, and each car as four plus two, six. But the last vehicle has no gap after it, because there's no gap at the end. So we take two away, once.", show(h5f, 'But the last vehicle')),
      L("So the length plus two is made of twelves and sixes only. Twelve and six both divide by six. So the length plus two always divides by six.", show(h5g, 'always divides by six')),
      L("Now we check that condition on the choices. Sixteen plus two is eighteen, and eighteen divides by six. Twenty plus two is twenty-two, and twenty-two doesn't divide by six. So twenty can never be the length. Choice number two is our answer, and I'll see you in the next question.", show(h5h, 'Sixteen plus two is eighteen'),
        mk('tick', 'choice 2', 'twenty can never be the length'))),
])

# ------------------------------------------------------------------------------------------------ wp-006 Minimum & Maximum
# Hebrew wp 119-128: min-max questions are about possible ranges; unlike general problems, understanding shortens the
# tries (which way to push); the motif comes back all over (geometry, overlap problems).
f0 = I('f0', 'Smallest possible? $\\quad$ Biggest possible?', size=30)
f1 = I('f1', 'Know which way to push $\\ \\to\\ $ fewer tries', size=30)
video('wp-006', 'lesson', slides=[
    S('Minimum & Maximum',
      L("Welcome back. Now type two of trial and error, minimum and maximum.")),
    S('Ranges',
      L("Minimum and maximum questions are about ranges. What's the smallest possible value, and what's the biggest?",
        show(f0, "What's the smallest possible")),
      L("Unlike general problems, we don't try blindly. A little understanding tells us which way to push, toward the smallest or toward the biggest. So we need far fewer tries.", show(f1, 'tells us which way to push'))),
    S('A recurring motif',
      L("By the way, minimum and maximum isn't only this lesson. It comes back all over the quantitative section. In geometry, in overlap problems later on, and in many other questions. So the thinking we build here pays off again and again."),
      L("Let's see a question of this type. [pause] I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ wp21-g007 (postcards)
# Hebrew wp 130-161 (the hair ties): bold words help; one friend could get all; to share among the most friends, give
# each as little as possible; 1, 2, 3 ... and the running total; the next friend can't be served, the rest goes to someone
# who already has. English adds the formula 1 + ... + k = k(k + 1)/2 with the pairing why (NEW, two examples).
p7 = TBL('p7', ('Friend', '1', '2', '3', '4', '5', '6', '7', '8', '9'), 2, [118] + [62] * 9,
         [('c1', [(0, 1, '1')]), ('c2', [(0, 2, '2')]), ('c38', [(0, c, str(c)) for c in range(3, 9)]),
          ('tot1', [(1, 1, '1'), (1, 2, '3'), (1, 3, '6'), (1, 4, '10'), (1, 5, '15')]),
          ('tot2', [(1, 6, '21'), (1, 7, '28'), (1, 8, '36', 'teal')]),
          ('no9', [(0, 9, '✗', 'red')]),
          ('fix', [(0, 8, '14', 'cover')])],
         base=[(0, 0, 'Cards'), (1, 0, 'Total')], title='Postcards per friend', w=760, size=26)
for _k, _it in p7.items():          # the layers find their base by id: board lines come between them
    if _it.get('over'): _it['of'] = 'p7'
    else: _it['fig'] = 'p7'
p7a = IH('p7a', '$42-36=6$ left $\\quad$ 9th friend needs $9$ ✗', size=30)
p7b = IH('p7b', 'friend 8: $\\ 8+6=14$ ✓', size=30)
q7a = IH('q7a', '$1+8=2+7=3+6=4+5=9$', size=30)
q7b = IH('q7b', '$4\\cdot9=36$', size=30)
q7c = I('q7c', '$1+2+\\ldots+k=\\frac{k(k+1)}{2}$', size=34)
q7d = IH('q7d', '$1+\\ldots+10$: $\\ \\frac{10\\cdot11}{2}=\\frac{110}{2}=55$', size=30, col=1)
q7e = IH('q7e', '8 friends: $\\ \\frac{8\\cdot9}{2}=36\\le42$ ✓', size=30, col=1)
q7f = IH('q7f', '9 friends: $\\ \\frac{9\\cdot10}{2}=45>42$ ✗', size=30, col=1)
video('solve-wp21-g007', 'solution', qid='wp21-g007', slides=[
    S('Method 1 · Understanding: give each the least',
      L("Noa shares forty-two postcards among her friends. Each friend receives a different number of postcards, a positive whole number, and all the postcards are given out. What is the largest possible number of friends?",
        pt('stem', 'Noa shares', 'hl', 11.0), voice='calm', pause=0.5),
      L("They ask for the largest possible number of friends. On the exam, a word like largest is printed in bold. Circle it, so you don't mix up the largest and the smallest. [short pause] We'll solve it in two different ways, by understanding which way to push, and then the math way, with a short formula.",
        pt('stem: ask', 'They ask for the largest')),
      L("[short pause] Let's start by understanding. In theory, Noa could give all forty-two postcards to one friend. That's allowed, but they want as many friends as possible. So we give each friend as little as possible. Then more is left for the next friend."),
      L("Each friend gets at least one, and every amount is different. So the first friend gets one. The second friend would love to get just one too, but the amounts must be different. So the second gets two. Then three, four, five, six, seven and eight.", show(p7['line'], 'Each friend gets at least one'), show(p7['c1'], 'So the first friend gets one'), show(p7['c2'], 'So the second gets two'), show(p7['c38'], 'Then three, four')),
      L("Now let's keep a running total. One plus two is three. Three plus three is six. Six plus four is ten. Ten plus five is fifteen.", show(p7['tot1'], 'keep a running total')),
      L("Fifteen plus six is twenty-one. Twenty-one plus seven is twenty-eight. And twenty-eight plus eight is thirty-six.",
        show(p7['tot2'], 'Fifteen plus six')),
      L("So eight friends use thirty-six postcards, and forty-two minus thirty-six leaves six. A ninth friend would need at least nine, because one to eight are taken. We only have six. So there's no ninth friend.",
        show(p7['no9'], 'A ninth friend would need'), show(p7a, 'We only have six')),
      L("But the six leftovers still have to be given out. We give them to someone who already has postcards, like the friend with eight. Eight plus six is fourteen. All the amounts are still different, and all forty-two are used. So eight friends really works, and choice number two is our answer.",
        show(p7['fix'], 'Eight plus six is fourteen'), show(p7b, 'All the amounts are still different'),
        mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · The math way: shortcut formula',
      L("[pause] Now the math way, with a short formula. The cheapest way to give different amounts to some friends is one, two, three, and so on. And there's a quick way to add that up."),
      L("Let's add one to eight by pairing the ends. One plus eight is nine. Two plus seven is nine. Three plus six is nine. Four plus five is nine. That's four pairs of nine, and four times nine is thirty-six.",
        show(q7a, 'One plus eight is nine'), show(q7b, 'four times nine')),
      L("Why does every pair give the same sum? Going in from both ends, one number goes up by one, and the other goes down by one. So the sum stays the same. In general, adding one, two, and so on up to k gives k times the next number, k plus one, and then half of that.", show(q7c, 'In general, adding one')),
      L("Let's check it once more, with ten. One to ten is ten times eleven, all divided by two. Ten times eleven is a hundred ten, and half of that is fifty-five. With pairs, it's five pairs of eleven, fifty-five again.",
        show(q7d, 'One to ten is ten times eleven')),
      L("Now back to our question. The friends need different amounts. Eight friends need at least eight times nine, all divided by two, which is thirty-six. That's not more than forty-two, so eight friends is possible.",
        show(q7e, 'Eight friends need at least')),
      L("Nine friends need at least nine times ten, all divided by two, which is forty-five. That's more than forty-two, so nine friends is impossible. Choice number two is our answer, and I'll see you in the next question.",
        show(q7f, 'Nine friends need at least'), mk('tick', 'choice 2', 'so nine friends is impossible'))),
])

# ------------------------------------------------------------------------------------------------ wp-008 Patterns
# Hebrew wp 164-200: the last type, mostly trial and little error; step by step (write the items one by one); sequences
# with a formula in n are rarer; don't use school sequence formulas; understanding is possible but rare.
k0 = I('k0', '1 $\\cdot$ Step by step $\\ \\to\\ $ write the items one by one', size=30)
k1 = I('k1', '2 $\\cdot$ A formula with $n$ in the choices $\\ \\to\\ $ plug in a number', size=30)
k2 = I('k2', 'No school sequence formulas', size=30)
video('wp-008', 'lesson', slides=[
    S('Patterns',
      L("Welcome back. Now the last type of trial and error, patterns. Here we barely think and barely make mistakes. It's mostly trial, careful trial.")),
    S('Two kinds',
      L("Patterns come in two kinds. The first kind is step by step. A rule repeats, and the simplest and best way is to write the items one at a time, exactly as the rule says, until we reach what they ask.",
        show(k0, 'The first kind is step by step')),
      L("The second kind is a sequence with a formula in n, in the choices. It's rarer, but it's good to know. Here we plug in a small number for n and check the answers.", show(k1, 'The second kind is a sequence')),
      L("If you remember the formulas for sequences from school, leave them. These aren't the sequences you know, and those formulas won't work here.", show(k2, 'leave them')),
      L("Solving these by pure understanding is possible, but every question is different, and very few students manage it. Plugging in is simple and safe. Let's see one question of each kind. [pause] I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ wp21-g009 (bakery)
# Hebrew wp 172-193 (the egg contest): step by step, item by item; a table only to make it comfortable - on the exam just
# write 1, 2, 3, 4; half first, then minus one. English adds plugging in the answers by running the rule backwards.
k9a = IH('k9a', 'Mon: $\\ 78$', size=30)
k9o = I('k9o', 'The rule: half, then $-\\,1$', size=30, col=1)
k9b = IH('k9b', 'Tue: $\\ 78\\div2=39$, $\\ 39-1=38$', size=30)
k9c = IH('k9c', 'Wed: $\\ 38\\div2=19$, $\\ 19-1=18$', size=30)
k9d = IH('k9d', 'Thu: $\\ 18\\div2=9$,', size=30)
k9d2 = IH('k9d2', '$9-1=8$ ✓', size=30)
k9u = I('k9u', 'Undo it: $\\ +\\,1$, then $\\times\\,2$', size=30)
k9e = IH('k9e', 'Thu $8$: $\\ 8+1=9$, $\\ 9\\cdot2=18$ (Wed)', size=30)
k9f = IH('k9f', '$18+1=19$, $\\ 19\\cdot2=38$ (Tue)', size=30)
k9g = IH('k9g', '$38+1=39$, $\\ 39\\cdot2=78$ (Mon) ✓', size=30)
video('solve-wp21-g009', 'solution', qid='wp21-g009', slides=[
    S('Method 1 · The math way: listing',
      L("A bakery bakes seventy-eight loaves of bread on Monday. On each later day, it bakes half the number of loaves of the day before, minus one. How many loaves does it bake on Thursday?", pt('stem', 'A bakery bakes', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("So the same rule repeats every day, and they ask about Thursday. That's a step-by-step pattern, so we write the days one by one. [short pause] We'll solve it in two different ways, by writing the days, and then by plugging in the answers and running the rule backwards.", pt('stem: ask', 'they ask about Thursday')),
      L("[short pause] Let's start by writing the days. Monday is seventy-eight. That's given, so we don't apply the rule to Monday. On the exam we don't need a table, just the days and the numbers.", show(k9a, 'Monday is seventy-eight')),
      L("Careful with the order. The rule says half of the day before, minus one. So we halve first, and only then take one away. Not the other way around.", show(k9o, 'So we halve first')),
      L("For Tuesday, half of seventy-eight is thirty-nine. Thirty-nine minus one is thirty-eight.",
        show(k9b, 'Half of seventy-eight')),
      L("For Wednesday, half of thirty-eight is nineteen, and nineteen minus one is eighteen. Eighteen is in the choices, but that's only Wednesday, so we keep going.",
        show(k9c, 'Half of thirty-eight')),
      L("For Thursday, half of eighteen is nine. Careful, nine is a choice too, but we still take one away. Nine minus one is eight. So the bakery bakes eight loaves on Thursday, and choice number one is our answer.", show(k9d, 'Half of eighteen'), show(k9d2, 'Nine minus one is eight'),
        mk('tick', 'choice 1', 'choice number one is our answer'))),
    S('Method 2 · Plugging in the answers: run it backwards',
      L("[pause] Now let's plug in the answers. We take a choice as Thursday, and undo the rule, day by day, back to Monday. If we land on seventy-eight, the choice is right."),
      L("How do we undo half, minus one? We do the opposite steps, in the opposite order. First we add one, and then we double.", show(k9u, 'We do the opposite steps')),
      L("Choice number one says eight. Eight plus one is nine, and nine doubled is eighteen. That's Wednesday.",
        show(k9e, 'Eight plus one is nine')),
      L("Eighteen plus one is nineteen, and nineteen doubled is thirty-eight. That's Tuesday.",
        show(k9f, 'Eighteen plus one')),
      L("Thirty-eight plus one is thirty-nine, and thirty-nine doubled is seventy-eight. That's Monday, exactly as the question says. Three days back, from Thursday to Monday, and it fits. So eight works. Choice number one is our answer, and I'll see you in the next question.", show(k9g, 'Thirty-eight plus one'),
        mk('tick', 'choice 1', 'So eight works'))),
])

# ------------------------------------------------------------------------------------------------ wp21-g010 (downloads)
# Hebrew wp 203-235 (the casino, x2 a day, total through day n): skip understanding; plug in n = 3 (small, easy to compute),
# check every choice; why not n = 1 - the exam builds the choices so that n = 1 leaves two standing; 3 is small enough to
# compute and big enough to separate. REMINDER: plugging in numbers (topic 51).
m0a = IH('m0a', 'Day 1: $\\ 5$ $\\quad$ Day 2: $\\ 10$ $\\quad$ Day 3: $\\ 20$', size=30)
m0b = IH('m0b', '$n=3$: $\\ 5+10+20=35$', size=30)
m0c = IH('m0c', '(1) $\\ 2^3=8$, $\\ 8-1=7$, $\\ 5\\cdot7=35$ ✓', size=30, col=1)
m0d = IH('m0d', '(2) $\\ 5\\cdot3^2=5\\cdot9=45$ ✗', size=30, col=1)
m0e = IH('m0e', '(3) $\\ 2^3+5=8+5=13$ ✗', size=30, col=1)
m0f = IH('m0f', '(4) $\\ 5\\cdot2^3=5\\cdot8=40$ ✗', size=30, col=1)
m0g = IH('m0g', '$n=1$: $\\ $total $5$', size=30)
m0h = IH('m0h', '(1) $5$ ✓ $\\quad$ (2) $5$ ✓', size=30)
m0h2 = IH('m0h2', '(3) $7$ ✗ $\\quad$ (4) $10$ ✗', size=30)
m0i = I('m0i', 'Two choices left? $\\ $Try $n=4$ too.', size=30)
video('solve-wp21-g010', 'solution', qid='wp21-g010', slides=[
    S('Method 1 · Plugging in numbers',
      L("A new app is downloaded five times on day one. On every later day, it is downloaded twice as many times as on the day before. How many times is it downloaded in total through day n?", pt('stem', 'A new app', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("So they ask for a formula, and there's an n in every choice. That's the second kind of pattern, a sequence. We don't use school formulas here. [short pause] We'll plug in a number for n, and check the choices.",
        pt('stem: ask', 'So they ask for a formula')),
      L("[short pause] Let's plug in n is three. Why did we pick three? Because it's small, so the days are easy to write out. And it's big enough to keep the choices apart. In a minute we'll see why not one."),
      L("Day one is five downloads. Every later day is twice the day before. So day two is ten, and day three is twenty.",
        show(m0a, 'Day one is five downloads')),
      L("The total through day three is five plus ten plus twenty. Five plus ten is fifteen. Fifteen plus twenty is thirty-five. So the right choice must give thirty-five when n is three.", show(m0b, 'Five plus ten is fifteen')),
      L("Choice number one is five times the difference, two to the power of n, minus one. Let's put in three. Two to the power of three is eight, and eight minus one is seven. Five times seven is thirty-five. It works.",
        show(m0c, 'Two to the power of three')),
      L("Choice number two is five n squared. Three squared is nine. Five times nine is forty-five. That's not thirty-five, so choice number two is out.", show(m0d, 'Three squared is nine'), mk('cross', 'choice 2', 'so choice number two is out')),
      L("Choice number three is two to the power of n, plus five. Eight plus five is thirteen, so choice number three is out.", show(m0e, 'Eight plus five'), mk('cross', 'choice 3', 'so choice number three is')),
      L("Choice number four is five times two to the power of n. Five times eight is forty, so it's out too. Only choice number one gives thirty-five, so choice number one is our answer.", show(m0f, 'Five times eight'),
        mk('cross', 'choice 4', "so it's out too"), mk('tick', 'choice 1', 'so choice number one is our answer'))),
    S('Method 1 · Why n is three',
      L("Why not plug in n is one? It's quicker, so let's see what happens. Through day one, the total is just five.",
        show(m0g, 'the total is just five')),
      L("Choice number one gives five times one, because two minus one is one. That's five. Choice number two gives five times one squared, also five. Choice number three gives two plus five, seven. Choice number four gives five times two, ten. So two choices survive, and we'd need another number anyway.", show(m0h, 'Choice number one gives five'), show(m0h2, 'Choice number three gives two')),
      L("That's how these questions are often built. Plugging in one leaves two choices standing. Three is small enough to calculate, and big enough to separate the choices. And if two choices still survive with three, plug in four as well. Choice number one is our answer, and I'll see you in the next question.",
        show(m0i, 'if two choices still survive'))
      , sb='Method 1 · Plugging in numbers'),
])

# ------------------------------------------------------------------------------------------------ wp-012 Smart Trial & Error
# Hebrew wp 240-266: it looks like luck, but there are techniques; why the exam tests it (it predicts the first year at
# university; school hands you the exact questions, university doesn't); who freezes and who starts.
r0 = I('r0', "Don't stare. Start trying.", size=44)
video('wp-012', 'lesson', slides=[
    S('Smart Trial & Error',
      L("Welcome back. Now trial and error at the advanced level.")),
    S('Why it matters',
      L("There's no formula here and no equation. We try, we miss, and we try again. It looks like luck, but it isn't. There are techniques that get us there much faster."),
      L("Why does the exam love these questions? The exam is meant to predict how we'll do in our first year at university. At school, we got the material, and often the exact questions too. At university, a lot is up to us, and nobody tells us exactly what to do."),
      L("So these questions test one thing. When there's no equation, do we freeze, or do we start? We try, we check, and we adjust. And we'll use this all through the quantitative section.", show(r0, 'do we freeze')),
      L("Now the techniques that make it faster. We'll learn them in the questions. [pause] I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ wp21-g013 (the chip)
# Hebrew wp 269-328 (the coin 7 / 11): they ask what cannot be - find what can and rule out three; work in order from the
# minimum; a swap adds a fixed amount; the skip (דילוג) when two values swap; a constant step -> every total leaves the same
# remainder. NEW: the skip, "inside the range is not enough", the remainder pattern (topic 15 comes later in the plan).
n3a = IH('n3a', 'all twos: $\\ 7\\cdot2=14$', size=30)
n3b = IH('n3b', 'one six: $\\ -2+6=+4$, $\\ 14+4=18$', size=30)
n3c = IH('n3c', '$18\\to22\\to26\\to30$', size=30)
n3d = IH('n3d', '$30\\to34$: $\\ 32$ is skipped ✗', size=30)
n3e = I('n3e', 'Inside the range is not enough', size=30)
n3f = IH('n3f', '$14=12+2$ $\\quad 18=16+2$ $\\quad 22=20+2$', size=30)
n3g = I('n3g', 'Every total leaves remainder $2$ when divided by $4$', size=30)
n3h = IH('n3h', '$32=8\\cdot4+0$ ✗', size=30)
n3i = IH('n3i', '$38=36+2$ $\\quad 30=28+2$', size=30)
video('solve-wp21-g013', 'solution', qid='wp21-g013', slides=[
    S('Method 1 · Plugging in numbers: trial and error',
      L("A plastic game chip has two written on one side and six on the other. It is tossed exactly seven times, and the numbers that land face up are added. Which total is impossible?", pt('stem', 'A plastic game chip', 'hl', 10.0),
        voice='calm', pause=0.5),
      L("They ask what's impossible. So we find the totals that can happen, and cross out three choices. The one that's left is the answer. [short pause] We'll solve it in two different ways, by trying totals in order, and then by understanding the pattern behind them.", pt('stem: ask', "They ask what's impossible")),
      L("[short pause] Let's start by trying, and let's work in order, so nothing gets lost. Only how many twos and how many sixes come up matters, not which toss came first. So we start from the smallest total. All seven tosses show two. Seven times two is fourteen.", show(n3a, 'Seven times two')),
      L("Fourteen can happen, so choice number three is out.", mk('cross', 'choice 3', 'so choice number three is out')),
      L("Now let's swap one two for a six. What does that change? We take away two and add six, so the total goes up by four. Fourteen plus four is eighteen.", show(n3b, 'We take away two and add six')),
      L("Each more six adds another four. Eighteen, twenty-two, twenty-six, thirty. So thirty can happen, and choice number four is out.", show(n3c, 'Eighteen, twenty-two'), mk('cross', 'choice 4', 'and choice number four is out')),
      L("The next swap gives thirty plus four, thirty-four. Look what happened. We jumped from thirty straight to thirty-four, and skipped thirty-two.", show(n3d, 'We jumped from thirty')),
      L("Thirty-two is between the smallest total and the biggest, and it still can't happen. Being inside the range is not enough. This is called the skip. It happens when two values swap with each other, like the two and the six here. So thirty-two is impossible, and choice number two is our answer.",
        show(n3e, 'Being inside the range'), mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Understanding: the remainder',
      L("[pause] Now let's solve it by understanding. Every swap adds four, so all the totals go up in steps of four from fourteen. A list like that has a pattern. Every number in it leaves the same remainder when we divide by four."),
      L("Why does it stay the same? Because fourteen is twelve plus two, so it leaves two. Adding four just adds one more four, so the remainder stays two. Eighteen is sixteen plus two. Twenty-two is twenty plus two.", show(n3f, 'Fourteen is twelve plus two')),
      L("So every possible total leaves remainder two when we divide it by four.", show(n3g, 'every possible total')),
      L("Now we check that condition on the choices. Choice number two is thirty-two. Thirty-two is eight fours exactly, so it leaves zero, not two. It can't be a total.", show(n3h, 'Thirty-two is eight fours')),
      L("The others leave two. Thirty-eight is thirty-six plus two. Thirty is twenty-eight plus two. Choice number two is our answer, and I'll see you in the next question.", show(n3i, 'Thirty-eight is thirty-six'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp21-g014 (the choir)
# Hebrew wp 331-392 (the safari): why "can be" and not exact (a range); plug in from the middle, the convenient one; one
# plug rules out two (it shows the direction); with number choices, once one fully works, mark it (no two right answers);
# the division elimination (twice -> even, three times -> divides by 3). English Method 2: the border case (tenors =
# sopranos gives 7 per alto, 63 / 7 = 9) + the division elimination, so the method stands on its own.
s4a = IH('s4a', '$27$ sopranos: $\\ 27\\div3=9$ altos', size=30)
s4b = IH('s4b', '$27+9=36$, $\\ 63-36=27$ tenors', size=30)
s4c = IH('s4c', '$27$ tenors, not more than $27$ ✗', size=30)
s4d = I('s4d', 'more sopranos $\\to$ fewer tenors: $\\ 30$ ✗', size=30, col=1)
s4e = IH('s4e', '$24$: $\\ 24\\div3=8$ altos', size=30, col=1)
s4e2 = IH('s4e2', '$24+8=32$, $\\ 63-32=31$', size=30, col=1)
s4f = IH('s4f', '$31>24$ ✓', size=30, col=1)
t4a = I('t4a', 'sopranos $=3\\cdot$ altos $\\to$ divides by $3$: $\\ 26$ ✗', size=30)
t4b = I('t4b', 'border: tenors $=$ sopranos $\\to$ $1+3+3=7$ per alto', size=30)
t4c = IH('t4c', '$63\\div7=9$ altos $\\to$ $27$ sopranos', size=30)
t4d = I('t4d', 'more tenors $\\to$ sopranos $<27$', size=30)
video('solve-wp21-g014', 'solution', qid='wp21-g014', slides=[
    S('Method 1 · Plugging in the answers: from the middle',
      L("A choir has only sopranos, altos and tenors. There are three times as many sopranos as altos, and there are more tenors than sopranos. The choir has sixty-three singers in total. Which of the following can be the number of sopranos?", pt('stem', 'A choir has only', 'hl', 13.0), voice='calm', pause=0.5),
      L("Why do they ask what can be, and not for an exact number? Because the givens don't fix one number. There's a range of possible values. [short pause] We'll solve it in two different ways, by plugging in the answers, and then by understanding where the range ends.", pt('stem: ask', 'Why do they ask what can be')),
      L("[short pause] Let's start by plugging in the answers. There are four choices, so we just test them. But we start from the middle, not from the smallest or the biggest. In order, the choices are twenty-four, twenty-six, twenty-seven and thirty. Twenty-seven is in the middle, and it divides by three, so it's convenient."),
      L("Choice number one, twenty-seven sopranos. There are three times as many sopranos as altos, so the altos are twenty-seven divided by three, which is nine.", show(s4a, 'twenty-seven divided by three')),
      L("Together that's twenty-seven plus nine, thirty-six singers. The choir has sixty-three, so the tenors are sixty-three minus thirty-six, which is twenty-seven.", show(s4b, 'twenty-seven plus nine')),
      L("Now let's check the other given. There must be more tenors than sopranos. Twenty-seven tenors and twenty-seven sopranos are equal, not more. So twenty-seven fails, and choice number one is out.", show(s4c, 'Twenty-seven tenors and'),
        mk('cross', 'choice 1', 'and choice number one is out')),
      L("And this one try tells us which way to go. More sopranos means more altos too, so fewer tenors are left. So a bigger choice fails too. Thirty is out, so choice number two is out as well. One plug, and two choices are gone. That's why we start from the middle.", show(s4d, 'More sopranos means'),
        mk('cross', 'choice 2', 'so choice number two is out')),
      L("Now a smaller one, twenty-four. Twenty-four divided by three is eight altos. Twenty-four plus eight is thirty-two. Sixty-three minus thirty-two is thirty-one tenors.", show(s4e, 'Twenty-four divided by three'), show(s4e2, 'Twenty-four plus eight')),
      L("Thirty-one is more than twenty-four, so the tenors are more. So twenty-four fits every given. When the choices are numbers, the moment one fully works, we can mark it, because a question can't have two right answers. Choice number three is our answer.", show(s4f, 'Thirty-one is more than'), mk('tick', 'choice 3', 'Choice number three is'))),
    S('Method 2 · Understanding: the border case',
      L("[pause] Now by understanding, from the givens again. There are three times as many sopranos as altos. So the number of sopranos must divide by three. Twenty-six doesn't divide by three, so choice number four is out, without any story.", show(t4a, 'must divide by three'), mk('cross', 'choice 4', 'so choice number four is out')),
      L("This works in general. If something is twice another whole number, it must be even. If it's three times another whole number, it must divide by three. That's a quick way to rule out choices."),
      L("Now where does the range end? Let's look at the border case, where the tenors are exactly equal to the sopranos. Then for every alto there are three sopranos and three tenors. One plus three plus three is seven singers for every alto.", show(t4b, 'One plus three plus three')),
      L("Sixty-three divided by seven is nine altos. Three times nine is twenty-seven sopranos. That's the border.",
        show(t4c, 'Sixty-three divided by seven')),
      L("But there must be more tenors than that. The total stays sixty-three, so more tenors leave fewer singers for the altos and the sopranos. So the sopranos must be fewer than twenty-seven. This is a useful habit. When a given says more than, first look at the case where it's exactly equal. That's the border, and the answer is on one side of it.", show(t4d, 'So the sopranos must be fewer')),
      L("So twenty-seven and thirty are out, and twenty-six doesn't divide by three. Only twenty-four is left. Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Only twenty-four is left'))),
])

# ------------------------------------------------------------------------------------------------ wp21-g015 (baskets)
# Hebrew wp 395-485 (the planters, "very high difficulty"): don't stare (trial and wonder, trial and staring); start
# plugging in the answers, or skip and come back; what cannot be -> find what can; each try; more than four is fine; in the
# exam stop after three, in the lesson check the last to understand; long is a minute or two, the quick questions buy the
# time; a shortcut comes in the next lesson (g021).
v5a = IH('v5a', '$8\\cdot3=24$, $\\ 80-24=56$ for $14$', size=30)
v5b = IH('v5b', '$56\\div14=4$ each ✓', size=30)
v5c = IH('v5c', '$11\\cdot3=33$, $\\ 80-33=47$ for $11$', size=30)
v5c2 = IH('v5c2', '$11\\cdot4=44$, $\\ 47-44=3$ more', size=30, col=1)
v5d = IH('v5d', '$10\\cdot4=40$, last one $7$ ✓', size=30, col=1)
v5e = IH('v5e', '$15\\cdot3=45$, $\\ 80-45=35$ for $7$', size=30, col=1)
v5f = IH('v5f', '$6\\cdot4=24$, last one $11$ ✓', size=30, col=1)
v5g = IH('v5g', '$7\\cdot3=21$, $\\ 80-21=59$ for $15$', size=30)
v5h = IH('v5h', '$15\\cdot4=60>59$ ✗', size=30)
video('solve-wp21-g015', 'solution', qid='wp21-g015', slides=[
    S('Method 1 · Plugging in the answers',
      L("Twenty-two baskets hold eighty apples altogether. Every basket holds at least three apples. Which number cannot be the number of baskets holding exactly three apples?", pt('stem', 'Twenty-two baskets', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("This is a hard question. Where do we even start? Some people try and wonder, and some just stare at it. The worst thing we can do here is stare. [short pause] So we start plugging in the answers. Or we skip it, move on, and come back at the end. Just don't sit and stare.", pt('stem: ask', 'Where do we even start')),
      L("[short pause] Let's plug in the answers. They ask what cannot be. So we find what can be, and cross out three choices. Let's start with choice number one, eight. Eight baskets with exactly three apples hold eight times three, twenty-four apples. Eighty minus twenty-four leaves fifty-six apples. Twenty-two minus eight leaves fourteen baskets.", show(v5a, 'Eighty minus twenty-four')),
      L("Those fourteen baskets must not hold exactly three, so each needs at least four. Fifty-six divided by fourteen is four, exactly four each. It works, so choice number one is out.", show(v5b, 'Fifty-six divided by fourteen'),
        mk('cross', 'choice 1', 'so choice number one is out')),
      L("Now choice number two, eleven. Eleven times three is thirty-three apples. Eighty minus thirty-three leaves forty-seven, for the other eleven baskets.", show(v5c, 'Eleven times three')),
      L("Eleven baskets with four each would hold forty-four. We have forty-seven, three more. That's fine, because more than four is allowed. Ten baskets get four, that's forty, and the last one gets seven. It works, so choice number two is out.", show(v5c2, 'Eleven baskets with four each'), show(v5d, 'Ten baskets get four'), mk('cross', 'choice 2', 'so choice number two is out')),
      L("Now choice number three, fifteen. Fifteen times three is forty-five. Eighty minus forty-five leaves thirty-five, for seven baskets.", show(v5e, 'Fifteen times three')),
      L("Six of them get four, that's twenty-four, and the last one gets the other eleven. It works, so choice number three is out. Three choices are out, so choice number four, seven, is our answer.", show(v5f, 'Six of them get four'),
        mk('cross', 'choice 3', 'so choice number three'), mk('tick', 'choice 4', 'seven, is our answer'))),
    S('Method 1 · Why seven fails',
      L("In the exam you'd circle it and move on. Here, let's see why seven fails, because it helps us understand the question. Seven baskets with three apples hold twenty-one. Eighty minus twenty-one leaves fifty-nine apples, for fifteen baskets.", show(v5g, 'Seven baskets with three')),
      L("Fifteen baskets with four each need sixty. We have only fifty-nine, one too few. So at least one more basket is stuck with three apples, and then there are eight, not seven.", show(v5h, 'Fifteen baskets with four')),
      L("Was it long? A minute or two, not twenty. That's fine, because the quick questions buy us the time for this one. And we'll come back to this type of question later, with a shortcut. Choice number four is our answer, and I'll see you in the next question.", mk('tick', 'choice 4', 'Choice number four is our answer')),
      sb='Method 1 · Plugging in the answers'),
])

# ------------------------------------------------------------------------------------------------ wp-016 More Min & Max
# Hebrew wp 488-493: understanding min-max shortens the tries, e.g. to maximize one, give the others the minimum; the
# nuances come in the questions. English: the three rules on one board (exam evidence in real_exam/audit_t21.md), each
# with its why and two examples (new numbers), and why rules 2 and 3 only sound opposite.
x0 = I('x0', 'Max of one $\\to$ give the others the least', size=30)
x0a = IH('x0a', '3 different: $\\ 1+2+23=26$', size=30)
x0b = IH('x0b', '4 different: $\\ 1+2+3+14=20$', size=30)
x1 = I('x1', 'Min of the biggest $\\to$ share as equally as you can', size=30)
x1a = IH('x1a', '$26\\div3=8$, $\\ 2$ left: $\\ 9+9+8=26$', size=30)
x1b = IH('x1b', '$30\\div4=7$, $\\ 2$ left: $\\ 8+8+7+7=30$', size=30)
x2 = I('x2', 'Min of one $\\to$ give the others the most', size=30)
x2a = IH('x2a', 'at most 10: $\\ 10+10+6=26$', size=30)
x2b = IH('x2b', 'at most 10: $\\ 10+10+10+1=31$', size=30)
video('wp-016', 'lesson', slides=[
    S('More Minimum & Maximum',
      L("Welcome back. Now more minimum and maximum. When we understand which way to push, we need far fewer tries.")),
    S('Push one up',
      L("Here are three rules that come up again and again. Each one tells us which way to push."),
      L("The first rule makes one number as big as possible. To do that, we give all the others the least they're allowed. Three different positive whole numbers add up to twenty-six. How big can the biggest be? The other two get the least, one and two. Twenty-six minus three leaves twenty-three.", show(x0, 'The first rule'), show(x0a, 'Twenty-six minus three')),
      L("Why does it work? The total is fixed. Every bit we take from the others goes to the one we want to grow. Here's another example. Four different positive numbers add up to twenty. The others get one, two and three, that's six. So the biggest can be twenty minus six, fourteen.", show(x0b, 'Four different positive numbers'))),
    S('Push the biggest down',
      L("The second rule makes the biggest number as small as possible. To do that, we share as equally as we can. Three whole numbers add up to twenty-six. Twenty-six divided by three is eight, with two left over. So the closest we can get is nine, nine and eight, and the biggest is at least nine.", show(x1, 'The second rule'), show(x1a, 'nine, nine and eight')),
      L("Why does it work? If we make one number smaller, another one has to grow. The biggest can never be smaller than an equal share. Here's another example. Four numbers add up to thirty. Thirty divided by four is seven, with two left over. So eight, eight, seven and seven, and the biggest is at least eight.", show(x1b, 'Four numbers add up to thirty'))),
    S('Push one down',
      L("The third rule makes one number as small as possible. To do that, we give all the others the most they're allowed. Three test scores, each at most ten, add up to twenty-six. The other two get ten each, that's twenty. So the smallest can be twenty-six minus twenty, six.", show(x2, 'The third rule'), show(x2a, 'twenty-six minus twenty')),
      L("Here's another example. Four scores, each at most ten, add up to thirty-one. Three of them get ten, that's thirty. So the smallest can be just one.", show(x2b, 'Four scores, each at most ten')),
      L("The second and third rules sound like opposites, but they aren't. In the second rule we push the biggest down, so the others can't pass it, and that's why we share equally. In the third rule we push one number down, so the others take as much as they can."),
      L("The nuances come in the questions. [pause] I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ wp21-g017 (spelling test)
# Hebrew wp 495-544 (the math test 9-15, a third or more, 18 students): one student first - the shortest test and the
# smallest share for the minimum, the longest test and ALL correct for the maximum ("a third or more"); then the last
# digit (it saves a bit of time and a silly mistake). Here the last digit can't split the maximum: said honestly.
y7a = IH('y7a', 'fewest: $\\ 10$ words, $\\ \\frac{1}{5}$ of $10=2$', size=30)
y7b = IH('y7b', '$14\\cdot2=28$', size=30)
y7c = IH('y7c', 'most: $\\ 25$ words, all correct', size=30)
y7d = IH('y7d', '$14\\cdot25=10\\cdot25+4\\cdot25$', size=30)
y7d2 = IH('y7d2', '$=250+100=350$', size=30)
z7a = IH('z7a', '$14\\cdot2$: $\\ 4\\cdot2=8$ $\\to$ ends in $8$', size=30)
z7b = IH('z7b', '$350$ and $140$ both end in $0$', size=30)
video('solve-wp21-g017', 'solution', qid='wp21-g017', slides=[
    S('Method 1 · Understanding: push to the extremes',
      L("A spelling test has between ten and twenty-five words, inclusive. Each of fourteen students spells at least one fifth of the words correctly. What are the smallest and the largest possible totals of correctly spelled words in the class?", pt('stem', 'A spelling test', 'hl', 12.0), voice='calm', pause=0.5),
      L("So they ask for a minimum and a maximum, the smallest and the biggest total for the whole class. [short pause] We'll solve it in two different ways, by understanding which way to push, and then with the last digit.",
        pt('stem: ask', 'the smallest and the biggest total')),
      L("[short pause] Let's start by understanding. To push the total to an extreme, we push everything around it. Let's start with one student. For the fewest correct words, the test is the shortest, ten words, and he spells the smallest share, one fifth. One fifth of ten is ten divided by five, which is two words.",
        show(y7a, 'One fifth of ten')),
      L("Fourteen students with two each is fourteen times two, twenty-eight. Choice numbers one and four start with seventy, not twenty-eight, so they're out. Seventy is one fifth of the longest test, five words each. But for the fewest, the test is the shortest too.", show(y7b, 'Fourteen students with two each'),
        mk('cross', 'choice 1', "so they're out"), mk('cross', 'choice 4', 'Seventy is one fifth')),
      L("Now let's find the most. The longest test has twenty-five words. Careful here, at least one fifth doesn't mean exactly one fifth. A student can spell all the words right. So one student spells at most twenty-five.",
        show(y7c, 'A student can spell all')),
      L("For the whole class it's fourteen times twenty-five. Ten times twenty-five is two hundred fifty. Four times twenty-five is a hundred. Two hundred fifty plus a hundred is three hundred fifty.",
        show(y7d, 'Ten times twenty-five'), show(y7d2, 'Two hundred fifty plus a hundred')),
      L("A hundred forty in choice number two is fourteen times ten, the shortest test, all correct. That's not the most. So the class spells between twenty-eight and three hundred fifty words, and choice number three is our answer.",
        mk('cross', 'choice 2', "That's not the most"), mk('tick', 'choice 3', 'choice number three is our answer'))),
    S('Method 2 · Understanding: the last digit',
      L("[pause] Now with the last digit. Remember, the last digit of a product comes only from the last digits. The fewest is the shortest test, ten words, and one fifth of it, two words, for each of fourteen students."),
      L("So it's fourteen times two. Look only at the last digits. Four times two is eight, so the total ends in eight. Twenty-eight ends in eight, and seventy ends in zero. So choice numbers one and four are out.",
        show(z7a, 'Four times two is eight'), mk('cross', 'choice 1', 'so choice numbers one and four'),
        mk('cross', 'choice 4', 'are out')),
      L("The most is the longest test, all twenty-five words, for each of fourteen students. Here the last digit can't help. Three hundred fifty and a hundred forty both end in zero.", show(z7b, 'both end in zero')),
      L("So here we simply multiply. Fourteen times twenty-five is three hundred fifty. The last digit helps only when the choices end in different digits. Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp21-g018 (piggy banks)
# Hebrew wp 547-570 (seven jars): the exact range = the minimum and the maximum; for the minimum give every jar before it
# the minimum (exactly the smallest step); why not less; for the maximum go from the other end with the smallest steps.
# English adds testing one value from the choices (the right range holds every possible value and nothing else),
# explained on the spot (the "most precise range" of topic 12 comes later in the plan).
w8a = IH('w8a', '$5\\to9\\to13\\to17$', size=30)
w8b = IH('w8b', '$47\\to43\\to39\\to35\\to31$', size=30)
w8c = IH('w8c', '$13$? $\\ $at least $5+3\\cdot4=17$ ✗', size=30)
w8d = IH('w8d', '$35$? $\\ $last at least $35+4\\cdot4=51>47$ ✗', size=30)
w8e = IH('w8e', '$17$? $\\ 5, 9, 13, 17, 21, 25, 29, 47$ ✓', size=30)
video('solve-wp21-g018', 'solution', qid='wp21-g018', slides=[
    S('Method 1 · Understanding: push to the extremes',
      L("Eight piggy banks stand in a row. The first holds five coins and the last holds forty-seven. Each piggy bank holds at least four more coins than the one before it. What is the exact range for the fourth piggy bank?",
        pt('stem', 'Eight piggy banks', 'hl', 11.0), voice='calm', pause=0.5),
      L("They ask for the exact range. That means the smallest and the biggest number of coins the fourth piggy bank can hold. [short pause] We'll solve it in two different ways, by understanding which way to push, and then by testing values from the choices.", pt('stem: ask', 'They ask for the exact range')),
      L("[short pause] Let's start with the smallest. For the fourth piggy bank to be as small as possible, every piggy bank before it gets the least it can. Each one holds at least four more than the one before. So we add exactly four each time. Five, then five plus four is nine, then thirteen, then seventeen.", show(w8a, 'then five plus four')),
      L("Can it be less? No, because every step needs at least four more. So the fourth holds at least seventeen. Choice numbers two and four don't start at seventeen, so they're out.", mk('cross', 'choice 2', "don't start at seventeen"),
        mk('cross', 'choice 4', "so they're out")),
      L("Now let's find the biggest. We work backwards from the last piggy bank, which holds forty-seven. To keep the fourth as big as possible, the steps after it are as small as they can be, four each. From the eighth back to the fourth is four steps. Forty-seven, then forty-seven minus four is forty-three, then thirty-nine, thirty-five, and thirty-one.",
        show(w8b, 'then forty-seven minus four')),
      L("So the fourth holds at most thirty-one. Choice number three goes up to thirty-five, so it's out. And both ends really happen, because the steps we didn't fix can simply be bigger. Seventeen to thirty-one, choice number one is our answer.", mk('cross', 'choice 3', "so it's out"), mk('tick', 'choice 1', 'choice number one'))),
    S('Method 2 · Plugging in the answers: test one value',
      L("[pause] Now let's test values from the choices. The choices are ranges. The right range holds every value that can happen, and no value that can't. So we test a number that some choices hold and others don't."),
      L("Choice number four starts at thirteen. Can the fourth piggy bank hold thirteen? From five, three steps of at least four each bring it to at least five plus twelve, seventeen. So thirteen is impossible, and choice number four is out.", show(w8c, 'From five, three steps'), mk('cross', 'choice 4', 'and choice number four is out')),
      L("Choice number three goes up to thirty-five. Can the fourth hold thirty-five? Then four more steps of at least four each bring the last one to at least thirty-five plus sixteen, fifty-one. But the last holds forty-seven. So thirty-five is impossible, and choice number three is out.", show(w8d, 'Then four more steps'),
        mk('cross', 'choice 3', 'and choice number three is out')),
      L("Now let's test seventeen. Choice number two starts at twenty-one, so it leaves seventeen out. Can the fourth hold seventeen? Five, nine, thirteen, seventeen, then twenty-one, twenty-five, twenty-nine, and a big step to forty-seven. Every step is at least four. So seventeen happens, and choice number two is out. Choice number one is our answer, and I'll see you in the next question.", show(w8e, 'Five, nine, thirteen, seventeen, then'),
        mk('cross', 'choice 2', 'and choice number two is out'), mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t21-01 (socks)
# Added question (Hebrew: none; the worst-luck idea is the Hebrew pigeonhole of topic 20, which comes LATER in the plan).
# NEW, full treatment: "to be sure" -> the worst luck, then one more; the warm-up (a pair: 3 can fail, 4 always works);
# why plus one; a second example (four of one color -> 10); the trap "three red" at the step.
k1a = IH('k1a', 'a pair: $\\ $red, blue, green $\\to$ no pair yet', size=30)
k1b = IH('k1b', '$3$ can fail $\\quad 3+1=4$ always works', size=30)
k1c = I('k1c', 'To be sure: $\\ $the worst luck $+\\ 1$', size=32)
k1d = IH('k1d', '4 of a color: $\\ 3+3+3=9$', size=30, col=1)
k1d2 = IH('k1d2', '$9+1=10$', size=30, col=1)
k1e = IH('k1e', '$2+2+2=6$ $\\to$ no 3 of a color', size=30, col=1)
k1f = IH('k1f', '$6+1=7$ ✓', size=30, col=1)
k1g = IH('k1g', '$4$: $\\ 2$ red, $1$ blue, $1$ green ✗', size=30)
k1h = IH('k1h', '$7$: $\\ $at most $2+2+2=6<7$ ✓', size=30)
video('solve-q-r26-t21-01', 'solution', qid='q-r26-t21-01', slides=[
    S('Method 1 · Understanding: the worst luck',
      L("A drawer holds ten red, eight blue and six green socks. In the dark, Dana takes out socks one at a time. What is the smallest number of socks she must take out to be sure she has three socks of the same color?",
        pt('stem', 'A drawer holds', 'hl', 11.0), voice='calm', pause=0.5),
      L("To be sure is the key. Dana can't see the colors, so she has to be ready for the worst luck. [short pause] We'll solve it in two different ways, by understanding the worst luck, and then by plugging in the answers.",
        pt('stem: ask', 'To be sure is the key')),
      L("[short pause] Let's start by understanding, with a simpler question first. How many socks must she take to be sure of two of the same color, a pair? With bad luck, the first three socks are red, blue and green, one of each. She still has no pair.", show(k1a, 'With bad luck')),
      L("But the fourth sock has to be red, blue or green. Whatever it is, it matches a sock she already has. So three socks can fail, and four always work.", show(k1b, 'So three socks can fail')),
      L("That's the rule for to be sure questions. Imagine the worst luck, the longest she can go without what she wants. Then add one more. Why plus one? The worst luck is the most socks she can take and still fail. One more sock, and failing is impossible.", show(k1c, "That's the rule")),
      L("Here's another example. To be sure of four socks of one color, the worst luck is three of each color. Three plus three plus three is nine socks. And still there are no four of one color. So she needs nine plus one, ten.", show(k1d, 'To be sure of four socks'), show(k1d2, 'So she needs nine plus one')),
      L("Now our question, three of the same color. Careful, it's any color, not three red socks. For three red socks, all eight blue and all six green could come out first. Eight plus six plus three is seventeen. How long can she avoid it? With the worst luck she gets two of every color. Two plus two plus two is six socks. And still no color has three.", show(k1e, 'Two plus two plus two')),
      L("The seventh sock is red, blue or green, and that color reaches three. So six socks can fail, and seven always work. Choice number two is our answer.", show(k1f, 'The seventh sock'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. They ask for the smallest number that makes her sure. So we start from the smallest choice and go up. The first one that always works is the answer."),
      L("Choice number four, four socks. Can four socks fail to give three of a color? They can. Two red, one blue and one green have no three of a color. So four isn't enough, and choice number four is out.", show(k1g, 'Two red, one blue'),
        mk('cross', 'choice 4', 'and choice number four is out')),
      L("Now choice number two, seven socks. Can seven socks avoid three of a color? To avoid it, each color can give at most two. Three colors with two each is only six socks. Seven is more than six, so one color must reach three. Seven always works.", show(k1h, 'Three colors with two each')),
      L("Nine and seventeen are bigger than seven, and we want the smallest number that is sure. Choice number two is our answer, and I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our'))),
])

# ------------------------------------------------------------------------------------------------ wp21-g019 (tickets)
# Hebrew wp 573-604 (the kindergarten sweets): what each child gets in total; fewest left = get the least and eat the most;
# most left = get the most and eat the least; times the children; then the last digit from the earlier question.
u9a = IH('u9a', 'gets: $\\ 3+2=5$ to $\\ 5+4=9$', size=30)
u9b = IH('u9b', 'fewest left: $\\ 5-3=2$', size=30)
u9c = IH('u9c', 'most left: $\\ 9-1=8$', size=30)
u9d = IH('u9d', '$23\\cdot2=46$', size=30)
u9e = IH('u9e', '$23\\cdot8=160+24=184$', size=30)
u9f = IH('u9f', '$23\\cdot2$: $\\ 3\\cdot2=6$ $\\to$ ends in $6$', size=30)
u9g = IH('u9g', '$23\\cdot8$: $\\ 3\\cdot8=24$ $\\to$ ends in $4$', size=30)
video('solve-wp21-g019', 'solution', qid='wp21-g019', slides=[
    S('Method 1 · Understanding: push to the extremes',
      L("At a fair, each of twenty-three children gets three to five tickets at the first booth, and two to four tickets at the second booth. Each child then uses one to three tickets on a ride. What are the smallest and the largest possible numbers of tickets left with all the children together?", pt('stem', 'At a fair', 'hl', 14.0),
        voice='calm', pause=0.5),
      L("This is minimum and maximum again. They ask for the fewest and the most tickets left, for all the children together. [short pause] We'll solve it in two different ways, by understanding which way to push, and then with the last digit.", pt('stem: ask', 'They ask for the fewest')),
      L("[short pause] Let's start with one child. How many tickets does a child get in total? Three to five at the first booth, plus two to four at the second. The least is three plus two, five. The most is five plus four, nine.",
        show(u9a, 'The least is three plus two')),
      L("The fewest left means the child gets the least and uses the most. Five minus three is two tickets.",
        show(u9b, 'Five minus three')),
      L("The most left means the child gets the most and uses the least. Careful, every child uses at least one ticket, so we don't stop at nine. Nine minus one is eight tickets.", show(u9c, 'Nine minus one')),
      L("Now all twenty-three children. The fewest is twenty-three times two, forty-six. So choice numbers one and four are out.", show(u9d, 'twenty-three times two'), mk('cross', 'choice 1', 'So choice numbers one and four'),
        mk('cross', 'choice 4', 'are out')),
      L("The most is twenty-three times eight. Twenty times eight is a hundred sixty. Three times eight is twenty-four. A hundred sixty plus twenty-four is a hundred eighty-four. Choice number two is our answer.",
        show(u9e, 'Twenty times eight'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Understanding: the last digit',
      L("[pause] Now with the last digit, which saves work and silly mistakes. Remember, the last digit of a product comes only from the last digits. The fewest is two tickets left for each of twenty-three children. Three times two is six, so the total ends in six.", show(u9f, 'Three times two is six')),
      L("Forty-six ends in six, and sixty-nine ends in nine. So choice numbers one and four are out.",
        mk('cross', 'choice 1', 'So choice numbers one and four'), mk('cross', 'choice 4', 'are out')),
      L("The most is eight tickets left for each child. Three times eight is twenty-four, so the total ends in four. A hundred eighty-four ends in four, and two hundred seven ends in seven. So choice number three is out too. Choice number two is our answer, and I'll see you in the next question.", show(u9g, 'Three times eight is twenty-four'),
        mk('cross', 'choice 3', 'So choice number three is out too'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp21-g020 (cards)
# Hebrew wp 607-678 (the marbles 21): plugging in the answers - for "at least" plug the smaller first, for "at most" the
# bigger first; then understanding: the maximum is easier (min to the others); the minimum: the biggest of two is more
# than half, of three more than a third; equal shares are not allowed, move one from the smallest.
l0a = IH('l0a', 'Lior $12$: $\\ $Maya $\\le11$, Noam $\\le10$', size=30)
l0a2 = IH('l0a2', '$12+11+10=33<36$ ✗', size=30)
l0b = IH('l0b', 'Lior $34$: $\\ 2$ left $\\to$ $1$ and $1$, not different ✗', size=30)
l1a = IH('l1a', 'Noam $1$, $\\ $Maya $2$', size=30)
l1b = IH('l1b', 'Lior: $\\ 36-3=33$', size=30)
l1c = I('l1c', 'The biggest of three $>$ a third', size=30)
l1d = IH('l1d', '$12, 12, 12$ ✗', size=30)
l1d2 = IH('l1d2', '$13, 12, 11$ ✓', size=30)
video('solve-wp21-g020', 'solution', qid='wp21-g020', slides=[
    S('Method 1 · Plugging in the answers: which one first',
      L("Lior, Maya and Noam share thirty-six cards. Their numbers of cards are different positive whole numbers, with Lior having the most and Noam the fewest. What are the smallest and the largest possible numbers of cards Lior has?", pt('stem', 'Lior, Maya and Noam', 'hl', 11.0), voice='calm', pause=0.5),
      L("So they ask for the fewest and the most cards Lior can have. Lior has the most, Noam the fewest, and Maya is in the middle. [short pause] We'll solve it in two different ways, by plugging in the answers, and then by understanding minimum and maximum.", pt('stem: ask', 'So they ask for the fewest')),
      L("[short pause] Let's start by plugging in the answers. For the smallest, the choices say twelve or thirteen. They ask for the smallest, so we try the smaller one first, twelve. If twelve works, it beats thirteen. If it doesn't, the answer is thirteen."),
      L("Say Lior has twelve. Maya and Noam must have fewer, and different numbers. So at most eleven and ten. Eleven plus ten is twenty-one. Twenty-one plus twelve is thirty-three. That's the most they can have together, and it's less than thirty-six. So twelve is impossible, and choice numbers one and two are out.", show(l0a, 'Say Lior has twelve'), show(l0a2, 'Eleven plus ten'),
        mk('cross', 'choice 1', 'and choice numbers one and two'), mk('cross', 'choice 2', 'are out')),
      L("For the biggest, the choices say thirty-three or thirty-four. They ask for the biggest, so we try the bigger one first, thirty-four. Then two cards are left for Maya and Noam. Each has at least one, so one and one. But their numbers must be different. So thirty-four is impossible, and choice number three is out.",
        show(l0b, 'Then two cards are left'), mk('cross', 'choice 3', 'and choice number three is out')),
      L("Only choice number four is left, thirteen and thirty-three. Choice number four is our answer.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Understanding: push to the extremes',
      L("[pause] Now let's solve it by understanding. The biggest is the easier part, so let's start there. To make Lior as big as possible, we give the others the least they can have. Noam gets one, because everyone has at least one. Maya must have more than Noam, so she gets two.", show(l1a, 'Noam gets one')),
      L("Lior gets the rest. Thirty-six minus three is thirty-three, so the most is thirty-three.",
        show(l1b, 'Thirty-six minus three')),
      L("The smallest needs a bit more thought. When two people share and one has more, he has more than half. In the same way, when three people share, the one with the most has more than a third. Why is that true? Because if he had a third or less, the other two have even less, and together they can't reach the total.", show(l1c, 'more than a third')),
      L("A third of thirty-six is twelve. If all three had twelve, the numbers would be equal, and that's not allowed. So Lior needs more than twelve. Let's move one card from Noam to Lior. Now it's thirteen, twelve and eleven. They're different. And thirteen plus twelve plus eleven is thirty-six.", show(l1d, 'If all three had twelve'), show(l1d2, "Now it's thirteen")),
      L("So Lior has thirteen to thirty-three cards. Choice number four is our answer, and I'll see you in the next question.", mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp21-g021 (stickers)
# Hebrew wp 682-783 (the planters again): the promised shortcut. Her two ways: (1) the range - the impossible value is at
# an end, so only the smallest or the biggest choice, one check; (2) the edge cases (all 20 at 3 is too few, 19 works, so
# the top is fine and the bad one is at the bottom). The English course corrected her "the range is always continuous"
# (t21_CHANGES, teacher 2026-10-08): no holes ONLY when the count moves by one; the chip counterexample. English adds the
# spare stickers (fill to the minimum, count what is left) as Method 1. All three are kept.
o1a = IH('o1a', '$26\\cdot3=20\\cdot3+6\\cdot3$', size=30)
o1a2 = IH('o1a2', '$=60+18=78$', size=30)
o1b = IH('o1b', '$90-78=12$ spare', size=30)
o1c = IH('o1c', 'at most $12$ go up $\\to$ at least $26-12=14$ stay at $3$', size=30)
o2a = IH('o2a', '$25\\cdot3=75$, $\\ 90-75=15$ for the last child', size=30)
o2b = I('o2b', '$14, 15, 16, \\ldots, 25$: $\\ $steps of $1$, no holes', size=30)
o2c = IH('o2c', '$13, 14, 17, 20$ $\\to$ $13$ or $20$', size=30)
o2d = IH('o2d', '$20\\cdot3=60$, $\\ 30$ for $6$: $\\ 5$ each ✓', size=30)
o2e = I('o2e', 'Fixed jumps leave holes: $\\ $the chip $14, 18, 22$', size=30)
o3a = IH('o3a', 'all $26$ at $3$: $\\ 78\\ne90$ ✗', size=30)
o3b = IH('o3b', '$25$ at $3$: $\\ 75+15=90$ ✓', size=30)
video('solve-wp21-g021', 'solution', qid='wp21-g021', slides=[
    S('Method 1 · Understanding: the spare stickers',
      L("Ninety stickers are shared among twenty-six children, and every child gets at least three stickers. Which number cannot be the number of children who get exactly three stickers?", pt('stem', 'Ninety stickers', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("This is the same type as the apple baskets, with new numbers. I promised a shortcut, and here it is. [short pause] We'll solve it in three different ways, by counting the spare stickers, by looking at the ends of the range, and by checking the edge cases.", pt('stem: ask', 'This is the same type')),
      L("[short pause] Let's start with the spare stickers. First we fill every child up to the minimum, three each. To get twenty-six times three, we take twenty times three, which is sixty. Then we add six times three, which is eighteen. Sixty plus eighteen is seventy-eight stickers.", show(o1a, 'To get twenty-six times three'), show(o1a2, 'Sixty plus eighteen')),
      L("Ninety minus seventy-eight leaves twelve spare stickers.", show(o1b, 'Ninety minus seventy-eight')),
      L("A child gets more than three only if at least one spare sticker goes to that child. Twelve spares can lift at most twelve children. So at least twenty-six minus twelve, fourteen children get exactly three.",
        show(o1c, 'Twelve spares can lift')),
      L("Thirteen is less than fourteen, so thirteen is impossible. Choice number two is our answer.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Understanding: only the ends',
      L("[pause] Now by looking at the ends of the range. The smallest count is fourteen, as the spares showed. The biggest is twenty-five. Twenty-five children get three each, that's seventy-five, and the last child gets ninety minus seventy-five, fifteen. All twenty-six can't get three, because that's only seventy-eight.",
        show(o2a, 'Twenty-five children get three')),
      L("And every count in between works too. Why is that? Because each spare sticker lifts one child, and moving one sticker changes the count by exactly one. So the count steps from fourteen up to twenty-five, one at a time, with no holes.",
        show(o2b, 'with no holes')),
      L("When the count changes by one at a time, the range has no holes. Then three choices are inside the range, and the impossible one must be at an end. In order, the choices are thirteen, fourteen, seventeen and twenty. So only thirteen or twenty can be outside.", show(o2c, 'In order, the choices are')),
      L("One check decides. Twenty children with three is sixty stickers. Thirty are left for the other six children, five each, more than three. So twenty works, and thirteen is the impossible one. Choice number two is our answer.",
        show(o2d, 'Twenty children with three'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("But careful, this is not a general rule. Remember the chip with two and six. Its totals jumped by four, fourteen, eighteen, twenty-two, and there were holes. Fixed jumps leave holes. There are no holes only when the value can move by one.", show(o2e, 'Fixed jumps leave holes'))),
    S('Method 3 · Understanding: the edge cases',
      L("[pause] Now the edge cases, a very easy calculation at the edge. Here too the count moves by one, so the impossible choice is at one end. What if every child gets exactly three? Twenty-six times three is seventy-eight, and we need ninety. So twenty-six doesn't work.", show(o3a, 'What if every child')),
      L("Now one child fewer at three. Twenty-five children with three is seventy-five, and the last child takes fifteen. That works, so twenty-five is the top of the range.", show(o3b, 'Twenty-five children with three')),
      L("Our choices twenty, seventeen and fourteen are all below twenty-five, so the top end is no problem. The impossible one must be at the bottom, the smallest choice, thirteen. Choice number two is our answer, and I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t21-02 (must be true)
# Added question. REMINDER: must = every allowed case, one failing case rules a choice out (topic 1). NEW at the step: the
# cheapest list 1..5 = 15 and the five spare (from g007 / g021); proving the survivor with the min-max bound.
mt1 = IH('mt1', '$1+2+3+4+5=15$ $\\to$ $5$ left', size=30)
mt2 = IH('mt2', '$1, 2, 3, 4, 10$: $\\ $largest $10$ ✗', size=30)
mt3 = IH('mt3', '$2, 3, 4, 5, 6$: $\\ $no $1$ ✗', size=30)
mt4 = IH('mt4', '$1, 3, 4, 5, 7=20$: $\\ $one even ✗', size=30)
mt5 = I('mt5', 'largest $\\le5$ $\\to$ only $1, 2, 3, 4, 5$', size=30)
mt5b = IH('mt5b', '$1+2+3+4+5=15\\ne20$ ✗', size=30)
mt6 = IH('mt6', '$2, 3, 4, 5, 6$: $\\ $largest $6$ ✓', size=30)
video('solve-q-r26-t21-02', 'solution', qid='q-r26-t21-02', slides=[
    S('Method 1 · Plugging in numbers: break the choices',
      L("Five different positive whole numbers have a sum of twenty. Which of the following must be true?",
        pt('stem', 'Five different positive', 'hl', 6.0), voice='calm', pause=0.5),
      L("Must be true means true in every allowed case. So one allowed case where a choice fails is enough to rule it out. [short pause] We'll solve it in two different ways, by plugging in numbers to break the choices, and then by understanding why the last one always holds.", pt('stem: ask', 'Must be true means')),
      L("[short pause] Let's start by plugging in numbers. The smallest five different positive numbers are one, two, three, four and five. Together that's fifteen, so five more are left to give out.", show(mt1, 'Together that')),
      L("Choice number two says the largest number is at most nine. To break it, we give all five extras to the largest. Five plus five is ten. So one, two, three, four and ten add up to twenty, and the largest is ten. That's not at most nine, so choice number two is out.", show(mt2, 'So one, two, three, four and ten'),
        mk('cross', 'choice 2', 'so choice number two is out')),
      L("Choice number one says one of the numbers is one. To break it, we give one extra to every number. Two, three, four, five and six. That's still twenty, and there's no one. So choice number one is out.",
        show(mt3, 'Two, three, four, five and six'), mk('cross', 'choice 1', 'So choice number one is out')),
      L("Choice number three says at least two of the numbers are even. Let's try to have only one even number, like one, three, four, five and seven. One plus three is four. Four plus four is eight. Eight plus five is thirteen. And thirteen plus seven is twenty. Only four is even, so choice number three is out.",
        show(mt4, 'One plus three is four'), mk('cross', 'choice 3', 'so choice number three is out')),
      L("Choice number four is the only one left. Choice number four is our answer.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Understanding: why it must be true',
      L("[pause] In the exam you'd stop there. But let's see why choice number four must be true. It says the largest number is at least six. That's a minimum and maximum question. How small can the largest number be?"),
      L("Say the largest were five or less. Then all five numbers are different, positive, and at most five. There's only one way to do that, one, two, three, four and five. Their sum is fifteen, not twenty. So the largest can't be five or less, and it must be at least six.", show(mt5, 'Say the largest were five or less'), show(mt5b, 'Their sum is fifteen')),
      L("And six really happens, with two, three, four, five and six. So it's true in every allowed case. Choice number four is our answer, and I'll see you in the next question.", show(mt6, 'And six really happens'),
        mk('tick', 'choice 4', 'Choice number four'))),
])

# ------------------------------------------------------------------------------------------------ wp-022 Patterns & Cycles
# Hebrew wp 787-801: a short reminder (no school sequence formulas, write it term by term), psychometric thinking can
# shorten it. English: cycles and the remainder (days of the week, last digits of powers; teacher kept, t21_CHANGES pass 2):
# NEW, full treatment with two examples each, the why, and the trap "remainder zero = the last one in the cycle".
cy1 = I('cy1', 'Tuesday $+\\ 30$ days?', size=30)
cy2 = IH('cy2', '$30=28+2$ $\\to$ remainder $2$ $\\to$ Thursday', size=30)
cy3 = IH('cy3', 'Sunday $+\\ 15$: $\\ 15=14+1$ $\\to$ Monday', size=30)
cy4 = I('cy4', 'Last digit of $3^{22}$?', size=30)
cy5 = IH('cy5', '$3, 9, 27, 81, 243$', size=30)
cy5b = IH('cy5b', 'last digits: $\\ 3, 9, 7, 1, 3$', size=30)
cy6 = IH('cy6', '$22=20+2$ $\\to$ 2nd in the cycle $\\to$ $9$', size=30)
cy7 = I('cy7', '$3^{20}$: $\\ 20=5\\cdot4+0$ $\\to$ the last one in the cycle $\\to$ $1$', size=30)
cy8 = IH('cy8', '$2^{10}$: $\\ 2, 4, 8, 6$; $\\ 10=8+2$ $\\to$ $4$ ($1024$)', size=30)
video('wp-022', 'lesson', slides=[
    S('Patterns & Cycles',
      L("Welcome back, and now more patterns. Remember, in pattern questions we don't use school formulas. We write it out, term by term, and a little psychometric thinking can make it shorter.")),
    S('Days of the week',
      L("Some patterns repeat in a cycle. Then one remainder trick saves us the whole list."),
      L("The days of the week repeat every seven days. Today is Tuesday. What day is it in thirty days? Thirty is four full weeks, twenty-eight days, plus two. Four full weeks bring us back to Tuesday. Two more days, and it's Thursday.",
        show(cy1, 'Today is Tuesday'), show(cy2, 'Thirty is four full')),
      L("Why does it work? A full cycle always brings us back to where we started. So only the part after the full cycles matters, and that's the remainder. Let's see one more example. Today is Sunday. What day is it in fifteen days? Fifteen is fourteen plus one. Two full weeks, and one more day, so it's Monday.", show(cy3, 'Today is Sunday'))),
    S('Last digits',
      L("Last digits of powers repeat too. What's the last digit of three to the power of twenty-two? Let's write the first few powers. Three, nine, twenty-seven, eighty-one, and then two hundred forty-three.",
        show(cy4, 'What'), show(cy5, 'Three, nine, twenty-seven')),
      L("The last digits are three, nine, seven, one, and then three again. Why does it repeat? The next last digit comes only from the last digit times three. After one, we get three again, so the cycle starts over. It's a cycle of four.", show(cy5b, 'The last digits are')),
      L("Twenty-two is five full cycles, twenty, plus two. So we land on the second digit of the cycle, nine.",
        show(cy6, 'Twenty-two is five full cycles')),
      L("Careful when the remainder is zero. Then it's not the first one, it's the last one in the cycle. Three to the power of twenty is exactly five cycles, so it ends in one, the last digit of the cycle.",
        show(cy7, 'Three to the power of twenty')),
      L("Let's see one more example, two to the power of ten. Two, four, eight, sixteen, thirty-two. The last digits are two, four, eight, six, and then two again. Ten is eight plus two, so it's the second digit, four. And really, two to the power of ten is one thousand twenty-four.", show(cy8, 'Two to the power of ten')),
      L("Days, last digits, and the flags in a coming question all use the same tool. We divide by the length of the cycle, and look at the remainder. Let's see patterns in real questions. [pause] I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ wp21-g023 (bacteria)
# Hebrew wp 804-852 (the chicken coop): working neatly, day by day; "wait" at the end - the edges: the start of the first
# day, the end of the last; inside the list it repeats, the trouble is always at the edges. One method, as in the Hebrew.
b3a = IH('b3a', 'Day 1: $\\ 40\\cdot2=80$,', size=30)
b3a2 = IH('b3a2', '$80-30=50$', size=30)
b3b = IH('b3b', 'Day 2: $\\ 50\\cdot2=100$, $\\ 100-30=70$', size=30)
b3c = IH('b3c', 'Day 3: $\\ 70\\cdot2=140$', size=30)
b3d = I('b3d', 'before the removal: $\\ 140$ $\\quad$ ($140-30=110$ is after)', size=30)
video('solve-wp21-g023', 'solution', qid='wp21-g023', slides=[
    S('Method 1 · The math way: listing',
      L("A lab dish has forty bacteria at the start of day one. During each day the number of bacteria doubles, and at the end of each day thirty bacteria are removed for testing. How many bacteria are in the dish on day three, just before that day's removal?", pt('stem', 'A lab dish', 'hl', 12.0), voice='calm', pause=0.5),
      L("So two things happen every day. The bacteria double during the day, and thirty are removed at the end. It's a step-by-step pattern, so we write it out, day by day. In pattern questions, working neatly is the most important thing.", pt('stem: ask', 'So two things happen')),
      L("[short pause] Day one starts with forty. During the day it doubles, so forty times two is eighty. At the end of the day, thirty are removed. Eighty minus thirty is fifty.", show(b3a, 'During the day it doubles'), show(b3a2, 'Eighty minus thirty')),
      L("So day two starts with fifty. It doubles to a hundred, and a hundred minus thirty is seventy.",
        show(b3b, 'So day two starts')),
      L("Day three starts with seventy. It doubles, and seventy times two is a hundred forty.",
        show(b3c, 'Day three starts with seventy')),
      L("Now wait a moment. In pattern questions, the edges are where the trap is. They ask for day three just before that day's removal. So we don't take away the thirty. A hundred ten would be the number after the removal, and that's the trap.", show(b3d, 'So we don')),
      L("So always ask yourself two things. Does the start include this step? Does the end include that one? Inside the list everything repeats, so the trouble is always at the edges."),
      L("There are a hundred forty bacteria. Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp21-g024 (flags)
# Hebrew wp 855-983 (the soccer kids, every 3 neighbours one ball): every three NEIGHBOURS, not separate blocks; the
# circle-and-line drawing (with the ball a circle, without a line); count along; the small shortcut (draw one block, count
# on it); then the constant cycle -> a remainder pattern (all leave 1 when divided by 3), check the choices.
fl = FLAGS('fl', 13, [('a', [(3, 'red')]), ('b', [(1, 'no'), (2, 'no'), (4, 'no'), (5, 'no')]),
                     ('c', [(6, 'no'), (7, 'no'), (8, 'red')]),
                     ('d', [(9, 'no'), (10, 'no'), (11, 'no'), (12, 'no'), (13, 'red')])], w=980)
for _k, _it in fl.items():
    if _it.get('over'): _it['of'] = 'fl'
    else: _it['fig'] = 'fl'
f4a = IH('f4a', '$3, 8, 13, 18, 23, 28, 33, 38, 43$ ✓', size=30)
f4b = IH('f4b', '$3=0+3$ $\\quad 8=5+3$ $\\quad 13=10+3$', size=30)
f4c = I('f4c', 'Every red flag leaves remainder $3$ when divided by $5$', size=30)
f4d = IH('f4d', '$43=40+3$ ✓ $\\quad 41, 42, 44$: $\\ 1, 2, 4$ ✗', size=30)
video('solve-wp21-g024', 'solution', qid='wp21-g024', slides=[
    S('Method 1 · The math way: listing',
      L("Sixty flags hang in a row along a street. In every group of five neighboring flags, exactly one is red. Flag three is red. Which flag can also be red?", pt('stem', 'Sixty flags', 'hl', 9.0), voice='calm', pause=0.5),
      L("Every group of five neighboring flags means every five in a row, not separate blocks of five. Flags one to five, flags two to six, and so on. [short pause] We'll solve it in two different ways, by drawing the pattern, and then with the remainder.", pt('stem: ask', 'Every group of five neighboring flags')),
      L("[short pause] Let's start by drawing the pattern. We don't draw real flags. A circle is red, and a line is not red. Flags one to five have exactly one red, and it's flag three. So flags one, two, four and five are not red.",
        show(fl['line'], "We don't draw real flags"), show(fl['a'], 'A circle is red'), show(fl['b'], 'So flags one, two')),
      L("Flags three to seven already have flag three, so six and seven are not red. Flags four to eight need a red too, and four to seven are not red. So flag eight is red.", show(fl['c'], 'So flag eight is red')),
      L("So the reds come every five flags. Three, eight, thirteen, and on it goes.", show(fl['d'], 'Three, eight, thirteen')),
      L("Now we count by fives from three. Three, eight, thirteen, eighteen, twenty-three, twenty-eight, thirty-three, thirty-eight, forty-three. So flag forty-three is red, and choice number three is our answer.",
        show(f4a, 'Now we count by fives'), mk('tick', 'choice 3', 'choice number three is our answer')),
      L("It looks long, but once you see the pattern, it takes ten seconds. And there's a small shortcut. Draw one block, a line, a line, a circle, a line and a line, and count along it again and again.")),
    S('Method 2 · Understanding: the remainder',
      L("[pause] Now let's solve it by understanding. The pattern repeats every five flags, a fixed cycle. And a fixed cycle gives a pattern in the numbers. Three is zero plus three. Eight is five plus three. Thirteen is ten plus three.",
        show(f4b, 'Three is zero plus three')),
      L("So every red flag leaves remainder three when we divide by five. We look for the choice that leaves three.",
        show(f4c, 'So every red flag')),
      L("Choice number three, forty-three, is forty plus three. It leaves three, so it's red. Forty-one leaves one, forty-two leaves two, and forty-four leaves four. Choice number three is our answer, and I'll see you in the next question.", show(f4d, 'is forty plus three'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp21-g025 (buses)
# Hebrew wp 986-1065 (coffee every 12 and 15 minutes): work neatly, list both; it takes long to find every match; the
# shortcut: the common multiple, found by jumping along the BIGGER number (fewer jumps); 8:00 counts as the first time.
# REMINDER: the least common multiple (topic 2). NEW: items and gaps (four times = three gaps).
bs1 = IH('bs1', 'Line 5: $\\ 6{:}40,\\ 6{:}56,\\ 7{:}12,\\ 7{:}28,\\ 7{:}44,\\ 8{:}00$', size=28)
bs2 = IH('bs2', 'Line 9: $\\ 6{:}40,\\ 7{:}00,\\ 7{:}20,\\ 7{:}40,\\ 8{:}00$', size=28)
bs3 = IH('bs3', 'together: $\\ 6{:}40$ and $8{:}00$ $\\to$ every $80$ minutes', size=28)
bs5 = IH('bs5', '4 times, 3 gaps: $\\ 6{:}40\\to8{:}00\\to9{:}20\\to10{:}40$', size=28)
bt1 = IH('bt1', '$20, 40, 60, 80$: $\\ 80=5\\cdot16$ ✓', size=30)
bt2 = IH('bt2', '$6{:}40+80$ min $=8{:}00$, $\\ 9{:}20$, $\\ 10{:}40$', size=30)
video('solve-wp21-g025', 'solution', qid='wp21-g025', slides=[
    S('Method 1 · The math way: listing',
      L("Two buses leave a station together at six forty. Line five leaves every sixteen minutes, and line nine leaves every twenty minutes. Counting six forty as the first time they leave together, when do they leave together for the fourth time?", pt('stem', 'Two buses leave', 'hl', 12.0), voice='calm', pause=0.5),
      L("So two schedules repeat, and we look for the times they meet. [short pause] We'll solve it in two different ways, by listing both schedules, and then with a common multiple.", pt('stem: ask', 'So two schedules repeat')),
      L("[short pause] Let's start by listing, neatly. Line five leaves every sixteen minutes. Six forty, six fifty-six, seven twelve, seven twenty-eight, seven forty-four, and eight o'clock.", show(bs1, 'Line five leaves every')),
      L("Line nine leaves every twenty minutes. Six forty, seven o'clock, seven twenty, seven forty, and eight o'clock.",
        show(bs2, 'Line nine leaves every')),
      sb='Method 1 · The math way: listing'),
    S('Method 1 · Four times, three gaps',
      L("So they meet again at eight o'clock. From six forty to eight o'clock is an hour and twenty minutes, eighty minutes. And at eight o'clock both start together again, so the same thing repeats. They meet every eighty minutes.", show(bs3, 'They meet every eighty')),
      L("Now careful with the count. Six forty is already the first time. Four times have only three gaps between them. So eight o'clock is the second time, nine twenty is the third, and ten forty is the fourth. This idea comes back a lot. Ten posts in a row have only nine gaps between them. So when you count times or items, count the gaps separately.",
        show(bs5, 'Four times have only three gaps')),
      L("Nine twenty is the trap, because that's only the third time. Choice number three is our answer. But listing every match takes a long time, so let's see a faster way.", mk('tick', 'choice 3', 'Choice number three is our answer')),
      sb='Method 1 · The math way: listing'),
    S('Method 2 · The math way: a common multiple',
      L("[pause] Now with a common multiple. When do two repeating things meet again? After a number of minutes that divides both by sixteen and by twenty."),
      L("The easy way is to take the bigger gap, twenty, and jump by it. We get twenty, forty, sixty and eighty. Twenty, forty and sixty don't divide by sixteen. Eighty is five times sixteen, so eighty divides by both sixteen and twenty.", show(bt1, 'We get twenty, forty')),
      L("Why the bigger one? Because it takes fewer jumps. Jumping by sixteen, we'd need five jumps to reach eighty. Jumping by twenty, only four."),
      L("So they leave together every eighty minutes, and the fourth time is three gaps after six forty. Eighty minutes is an hour and twenty minutes. Six forty plus an hour and twenty is eight o'clock, then nine twenty, then ten forty. Choice number three is our answer, and I'll see you in the next question.", show(bt2, 'Six forty plus an hour'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# carry-over boxes on the continuation slides (V2): the next step uses these results
CARRY21 = {'solve-wp21-g015': {1: ['(1), (2), (3) work $\\to$ (4)']},
           'solve-wp21-g010': {1: ['$n=3$: only (1) gives $35$']}}
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
 "wp21-g004": "A phone game starts with 2 large bubbles on the screen. Popping a large bubble splits it into 5 small bubbles. Popping a small bubble makes it disappear. After exactly 3 pops, how many bubbles can be on the screen?",
 "wp21-g005": "A line of vehicles waits at a traffic light. It has at least one truck 10 m long and at least one car 4 m long. There is a 2 m gap between neighboring vehicles, and no gap at either end of the line. Which total length of the line is impossible?",
 "wp21-g007": "Noa shares $42$ postcards among her friends. Each friend receives a different number of postcards (a positive integer), and all the postcards are given out. What is the largest possible number of friends?",
 "wp21-g009": "A bakery bakes 78 loaves of bread on Monday. On each later day, it bakes half the number of loaves of the day before, minus 1. How many loaves does it bake on Thursday?",
 "wp21-g010": "A new app is downloaded 5 times on day 1. On every later day, it is downloaded twice as many times as on the day before. How many times is it downloaded in total through day $n$?",
 "wp21-g013": "A plastic game chip has 2 written on one side and 6 on the other. It is tossed exactly 7 times, and the numbers that land face up are added. Which total is impossible?",
 "wp21-g014": "A choir has only sopranos, altos and tenors. There are $3$ times as many sopranos as altos, and there are more tenors than sopranos. The choir has $63$ singers in total. Which of the following can be the number of sopranos?",
 "wp21-g015": "Twenty-two baskets hold 80 apples altogether. Every basket holds at least 3 apples. Which number cannot be the number of baskets holding exactly 3 apples?",
 "wp21-g017": "A spelling test has between $10$ and $25$ words (inclusive). Each of $14$ students spells at least $\\frac15$ of the words correctly. What are the smallest and the largest possible totals of correctly spelled words in the class?",
 "wp21-g018": "Eight piggy banks stand in a row. The first holds 5 coins and the last holds 47. Each piggy bank holds at least 4 more coins than the one before it. What is the exact range for the fourth piggy bank?",
 "q-r26-t21-01": "A drawer holds $10$ red, $8$ blue and $6$ green socks. In the dark, Dana takes out socks one at a time. What is the smallest number of socks she must take out to be sure she has $3$ socks of the same color?",
 "wp21-g019": "At a fair, each of 23 children gets 3 to 5 tickets at the first booth and 2 to 4 tickets at the second booth. Each child then uses 1 to 3 tickets on a ride. What are the smallest and the largest possible numbers of tickets left with all the children together?",
 "wp21-g020": "Lior, Maya and Noam share 36 cards. Their numbers of cards are different positive integers, with Lior having the most and Noam the fewest. What are the smallest and the largest possible numbers of cards Lior has?",
 "wp21-g021": "Ninety stickers are shared among 26 children, and every child gets at least 3 stickers. Which number cannot be the number of children who get exactly 3 stickers?",
 "q-r26-t21-02": "Five different positive integers have a sum of $20$. Which of the following must be true?",
 "wp21-g023": "A lab dish has 40 bacteria at the start of day 1. During each day the number of bacteria doubles, and at the end of each day 30 bacteria are removed for testing. How many bacteria are in the dish on day 3, just before that day’s removal?",
 "wp21-g024": "Sixty flags hang in a row along a street. In every group of five neighboring flags, exactly one is red. Flag 3 is red. Which flag can also be red?",
 "wp21-g025": "Two buses leave a station together at 06:40. Line 5 leaves every 16 minutes and line 9 leaves every 20 minutes. Counting 06:40 as the first time they leave together, when do they leave together for the fourth time?",
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
MV.carry(_types.SimpleNamespace(**globals()), CARRY21)
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
