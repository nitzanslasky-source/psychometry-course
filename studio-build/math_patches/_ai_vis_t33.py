"""Topic 33 (Circles) - the scripts for the teacher's own-voice reading (2026-10-14), written from the first draft to
the Codex review standard, the clarity style, the method visuals (geometry: the angle figure built in layers, GEO below), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py / _ai_vis_t16.py / _ai_vis_t17.py / _ai_vis_t18.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The camera lesson 'geo-074' gets its own reading script here too, in parts of about 3-4 minutes (2026-10-14: she reads it
with the camera on). Every other topic-33 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t33.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t33.py ai_redo_t33() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods and EVERY method of the Hebrew solution (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-33-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t33ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-33 flow order of the scripts
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
CAM_BASE = 'geo-074'
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
            'style': "the teacher reads it herself (Reading Studio), topic-33 scripts (2026-10-14): math_patches/_ai_vis_t33.py is "
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



CARRY33 = {}       # carry-over boxes (V2): {vid: {slide index: [tex, ...]}}, filled by the scripts


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
import math as _f1m


def f1_C(cx, cy, r, o=True, ol=(-18, 20)):
    """a clean circle; o = with its center O"""
    e = [('circ', cx, cy, r, 'ink', 3)]
    if o: e += [('dot', cx, cy), ('txt', cx + ol[0], cy + ol[1], 'O', 'ink', 24, True)]
    return e


def f1_P(cx, cy, r, deg, name=None, d=26):
    """a point on the circle at deg, with its name outside"""
    x, y = gpt(cx, cy, r, deg); e = [('dot', x, y)]
    if name:
        lx, ly = gpt(cx, cy, r + d, deg); e.append(('txt', lx, ly, name, 'ink', 26, True))
    return e


def f1_S(cx, cy, r, d1, d2, col='teal', w=4, dashed=False):
    """the straight segment between two points of the circle (or the center, when d is None)"""
    p = (cx, cy) if d1 is None else gpt(cx, cy, r, d1); q = (cx, cy) if d2 is None else gpt(cx, cy, r, d2)
    return ('seg', p[0], p[1], q[0], q[1], col, w, dashed)


def f1_ang(v, p, q, r, col, lab=None, lr=None):
    """an angle arc at v between the rays to p and q (the smaller angle)"""
    d1, d2 = gdir(v[0], v[1], p[0], p[1]), gdir(v[0], v[1], q[0], q[1])
    if (d2 - d1) % 360 > 180: d1, d2 = d2, d1
    e = ('arc', v[0], v[1], r, d1, d2, col)
    if lab: e = e + (lab, lr if lr else r + 22)
    return e


def f1_mid(p, q, d=0, side=1):
    """the midpoint of p-q, pushed d units sideways (for a label next to a segment)"""
    mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
    L = _f1m.hypot(q[0] - p[0], q[1] - p[1]) or 1
    return mx - (q[1] - p[1]) / L * d * side, my + (q[0] - p[0]) / L * d * side


# ================================================================ part 1: circle, radius, chord, diameter
# ---- circle or disk
_c = (190, 180); _r = 140
f1disk = PIN(GEO('f1disk', [
    ('line', f1_C(*_c, _r, o=False)),
    ('trace', [('arcw', *_c, _r, 0, 359.9, 'teal', 7), ('txt', 540, 120, 'circle = the round line', 'teal', 28)]),
    ('in', [('circ', *_c, _r, 'ink', 3, False, 'teal'), ('txt', 540, 200, 'the inside = the flat shape', 'teal', 28)]),
    ('exam', [('txt', 540, 280, 'on the exam: "circle" for both', 'orange', 26)]),
], vb='30 25 780 310', w=1000, col=0, title='A circle and its inside'))

# ---- the radius: one, then spin it around
_c = (230, 185); _r = 140
def _f1_rad(deg, lab='r', col='teal', d=16):
    p = gpt(*_c, _r, deg)
    return [f1_S(*_c, _r, None, deg, col), ('dot', *p), ('txt', *f1_mid(_c, p, d), lab, col, 26, True)]
f1rad = PIN(GEO('f1rad', [
    ('line', f1_C(*_c, _r)),
    ('r1', _f1_rad(35)),
    ('spin', _f1_rad(120) + _f1_rad(200) + _f1_rad(290)),
    ('eq', [('txt', 560, 150, 'all the radii', 'teal', 28), ('txt', 560, 190, 'of this circle are equal', 'teal', 28)]),
], vb='60 30 720 315', w=960, col=0, title='The radius of a circle'))

# ---- three circles: every radius of one circle is the same (2, 3, 5 cm)
def _f1_three(cx, cy, r, lab, degs):
    e = f1_C(cx, cy, r, o=False) + [('dot', cx, cy)]
    for dg in degs:
        p = gpt(cx, cy, r, dg)
        e += [('seg', cx, cy, p[0], p[1], 'teal', 3.5), ('txt', *f1_mid((cx, cy), p, 14), lab, 'teal', 22)]
    e.append(('txt', cx, cy + r + 30, 'radius %s' % lab, 'ink', 24))
    return e
f1radv = PIN(GEO('f1radv', [
    ('line', _f1_three(80, 150, 48, '2', (40, 160, 270))),
    ('c3', _f1_three(260, 150, 72, '3', (60, 180, 300))),
    ('c5', _f1_three(500, 150, 120, '5', (20, 130, 240))),
], vb='10 20 640 300', w=900, col=0, title='Three circles, each with its own radius'))

# ---- two radii make an isosceles triangle (three central angles)
def _f1_iso(cx, cy, r, a, b):
    A, B = gpt(cx, cy, r, a), gpt(cx, cy, r, b); O = (cx, cy)
    return (f1_C(cx, cy, r, ol=(0, 22) if (a + b) / 2.0 > 0 and (a + b) / 2.0 < 180 else (0, -22)) +
            [('seg', cx, cy, A[0], A[1], 'teal', 3.5), ('seg', cx, cy, B[0], B[1], 'teal', 3.5),
             ('tick', cx, cy, A[0], A[1]), ('tick', cx, cy, B[0], B[1]), ('seg', A[0], A[1], B[0], B[1], 'ink', 3),
             ('dot', *A), ('dot', *B), ('tint', [O, A, B], 'teal'),
             f1_ang(A, O, B, 26, 'orange'), f1_ang(B, O, A, 26, 'orange')])
f1iso = PIN(GEO('f1iso', [
    ('line', _f1_iso(110, 160, 90, 65, 115)),
    ('t2', _f1_iso(330, 160, 90, 30, 150)),
    ('t3', _f1_iso(550, 160, 90, 200, 340)),
    ('lab', [('txt', 330, 290, 'two radii: an isosceles triangle, its base angles equal', 'teal', 24)]),
], vb='10 50 640 260', w=960, col=0, title='Two radii and a chord make an isosceles triangle'))

# ---- chords: long, short, very short
_c = (230, 185); _r = 140
f1chord = PIN(GEO('f1chord', [
    ('line', f1_C(*_c, _r, o=False)),
    ('ab', f1_P(*_c, _r, 165, 'A') + f1_P(*_c, _r, 20, 'B') + [f1_S(*_c, _r, 165, 20)]),
    ('cd', f1_P(*_c, _r, 220, 'C') + f1_P(*_c, _r, 290, 'D') + [f1_S(*_c, _r, 220, 290)]),
    ('ef', f1_P(*_c, _r, 330, 'E') + f1_P(*_c, _r, 350, 'F') + [f1_S(*_c, _r, 330, 350)]),
    ('lens', [('txt', 560, 110, 'A B: a long chord', 'teal', 26), ('txt', 560, 160, 'C D: a short chord', 'teal', 26),
              ('txt', 560, 210, 'E F: a very short chord', 'teal', 26)]),
], vb='60 15 720 340', w=960, col=0, title='Chords of a circle'))

# ---- the diameter: chords get longer toward the middle; the longest goes through O
_c = (220, 185); _r = 140
def _f1_hch(h, col='ink', w=3):
    """a horizontal chord at height h above the center"""
    import math
    dx = math.sqrt(_r * _r - h * h)
    return [('seg', _c[0] - dx, _c[1] - h, _c[0] + dx, _c[1] - h, col, w)]
_dA, _dB = (_c[0] - _r, _c[1]), (_c[0] + _r, _c[1])
f1diam = PIN(GEO('f1diam', [
    ('line', f1_C(*_c, _r, o=False)),
    ('c1', _f1_hch(120)),
    ('c2', _f1_hch(85)),
    ('c3', _f1_hch(45)),
    ('d', [('seg', *_dA, *_dB, 'teal', 5), ('dot', *_dA), ('dot', *_dB), ('txt', _dA[0] - 24, _dA[1], 'A', 'ink', 26, True),
           ('txt', _dB[0] + 24, _dB[1], 'B', 'ink', 26, True), ('dot', *_c), ('txt', _c[0], _c[1] + 24, 'O', 'ink', 24, True)]),
    ('rr', [('txt', _c[0] - 70, _c[1] + 22, 'r', 'teal', 28, True), ('txt', _c[0] + 70, _c[1] + 22, 'r', 'teal', 28, True),
            ('tick', *_dA, *_c), ('tick', *_c, *_dB)]),
    ('two', [('txt', 560, 160, 'diameter = r + r = 2r', 'teal', 30)]),
], vb='50 30 720 310', w=960, col=0, title='The diameter: the longest chord'))
f1d1 = IH('f1d1', '$\\text{diameter }14\\ \\to\\ \\text{radius }7$', size=30)
f1d2 = IH('f1d2', '$\\text{radius }6\\ \\to\\ \\text{diameter }12$', size=30)

# ---- a diameter in any direction cuts the circle into two halves
def _f1_half(cx, cy, r, deg):
    A, B = gpt(cx, cy, r, deg), gpt(cx, cy, r, deg + 180)
    return f1_C(cx, cy, r, ol=(0, 0) if False else (14, 22), o=False) + [
        ('cseg', cx, cy, r, deg, deg + 180, 'teal'), ('seg', A[0], A[1], B[0], B[1], 'teal', 4), ('dot', cx, cy)]
f1half = PIN(GEO('f1half', [
    ('line', _f1_half(110, 150, 90, 0)),
    ('h2', _f1_half(330, 150, 90, 60)),
    ('h3', _f1_half(550, 150, 90, 145) + [('txt', 330, 280, 'two halves: two semicircles', 'teal', 26)]),
], vb='10 45 640 260', w=960, col=0, title='A diameter in any direction makes two semicircles'))

# ================================================================ part 2: the angles, arcs, intercepts
# ---- the inscribed angle
_c = (230, 185); _r = 140
_iA, _iB, _iC = gpt(*_c, _r, 30), gpt(*_c, _r, 145), gpt(*_c, _r, 265)
f1insc = PIN(GEO('f1insc', [
    ('line', f1_C(*_c, _r, o=False)),
    ('c', f1_P(*_c, _r, 265, 'C')),
    ('ch', f1_P(*_c, _r, 30, 'A') + f1_P(*_c, _r, 145, 'B') + [f1_S(*_c, _r, 265, 30, 'ink', 3), f1_S(*_c, _r, 265, 145, 'ink', 3)]),
    ('ang', [f1_ang(_iC, _iA, _iB, 34, 'teal'), ('txt', 560, 140, 'vertex on the circle', 'teal', 28),
             ('txt', 560, 180, 'between two chords', 'teal', 28)]),
], vb='60 -12 720 367', w=960, col=0, title='An inscribed angle'))

# ---- inscribed: two more, then a vertex inside and a vertex outside (not inscribed)
def _f1_ins(cx, cy, r, v, a, b, col):
    V, A, B = gpt(cx, cy, r, v), gpt(cx, cy, r, a), gpt(cx, cy, r, b)
    return [('seg', V[0], V[1], A[0], A[1], 'ink', 3), ('seg', V[0], V[1], B[0], B[1], 'ink', 3), ('dot', *V),
            f1_ang(V, A, B, 24, col)]
def _f1_bad(cx, cy, r, P, a, b, lab, ly=None):
    A, B = gpt(cx, cy, r, a), gpt(cx, cy, r, b)
    return [('seg', P[0], P[1], A[0], A[1], 'red', 3), ('seg', P[0], P[1], B[0], B[1], 'red', 3), ('dot', *P),
            f1_ang(P, A, B, 20, 'red'), ('txt', cx, ly or cy + r + 34, lab, 'red', 22)]
f1insv = PIN(GEO('f1insv', [
    ('line', f1_C(90, 140, 70, o=False) + _f1_ins(90, 140, 70, 200, 60, 340, 'teal') + [('txt', 90, 244, 'inscribed ✓', 'teal', 22)]),
    ('e2', f1_C(260, 140, 70, o=False) + _f1_ins(260, 140, 70, 90, 210, 330, 'orange') + [('txt', 260, 244, 'inscribed ✓', 'teal', 22)]),
    ('in', f1_C(450, 140, 70, o=False) + _f1_bad(450, 140, 70, (450, 168), 60, 120, 'inside ✗')),
    ('out', f1_C(615, 115, 52, o=False) + _f1_bad(615, 115, 52, (615, 192), 225, 315, 'outside ✗', 244)),
], vb='10 55 680 225', w=1000, col=0, title='Inscribed angles and two angles that are not'))

# ---- the central angle
_c = (230, 185); _r = 140
_kA, _kB = gpt(*_c, _r, 20), gpt(*_c, _r, 110)
f1cent = PIN(GEO('f1cent', [
    ('line', f1_C(*_c, _r, ol=(-6, 26))),
    ('rr', f1_P(*_c, _r, 20, 'A') + f1_P(*_c, _r, 110, 'B') + [f1_S(*_c, _r, None, 20, 'ink', 3), f1_S(*_c, _r, None, 110, 'ink', 3)]),
    ('ang', [('arc', *_c, 34, 20, 110, 'teal'), ('txt', 560, 140, 'vertex at the center', 'teal', 28),
             ('txt', 560, 180, 'between two radii', 'teal', 28)]),
], vb='60 -12 720 367', w=900, col=0, title='A central angle'))

def _f1_cen(cx, cy, r, a, b, col, lab):
    A, B = gpt(cx, cy, r, a), gpt(cx, cy, r, b)
    return f1_C(cx, cy, r, o=False) + [('seg', cx, cy, A[0], A[1], 'ink', 3), ('seg', cx, cy, B[0], B[1], 'ink', 3),
                                       ('dot', cx, cy), ('dot', *A), ('dot', *B), ('arc', cx, cy, 22, a, b, col, lab, 52)]
f1cenv = PIN(GEO('f1cenv', [
    ('line', _f1_cen(110, 150, 85, 30, 75, 'teal', '45°')),
    ('c2', _f1_cen(330, 150, 85, 20, 140, 'orange', '120°')),
    ('c3', _f1_cen(550, 150, 85, 0, 180, 'orange', '180°')),
], vb='10 55 640 200', w=960, col=0, title='Three central angles'))

# ---- arcs: short, long, almost the whole circle
def _f1_arc(cx, cy, r, a1, a2, col, lab):
    return f1_C(cx, cy, r, o=False) + [('arcw', cx, cy, r, a1, a2, col, 8), ('txt', cx, cy + r + 32, lab, col, 22)]
f1arcv = PIN(GEO('f1arcv', [
    ('line', _f1_arc(110, 140, 80, 60, 110, 'teal', 'a short arc')),
    ('a2', _f1_arc(330, 140, 80, 150, 330, 'teal', 'a longer arc')),
    ('a3', _f1_arc(550, 140, 80, 120, 420, 'orange', 'almost all of it')),
], vb='10 40 640 230', w=960, col=0, title='Arcs: parts of the circle'))

# ---- a chord splits the circle into two arcs: minor and major
_c = (230, 185); _r = 140
f1arc = PIN(GEO('f1arc', [
    ('line', f1_C(*_c, _r, o=False)),
    ('ch', f1_P(*_c, _r, 120, 'A') + f1_P(*_c, _r, 200, 'B') + [f1_S(*_c, _r, 120, 200, 'ink', 3)]),
    ('mi', [('arcw', *_c, _r, 120, 200, 'teal', 9), ('txt', 560, 130, 'the short one: the minor arc', 'teal', 26)]),
    ('ma', [('arcw', *_c, _r, 200, 480, 'orange', 9), ('txt', 560, 180, 'the long one: the major arc', 'orange', 26)]),
], vb='50 -12 760 367', w=980, col=0, title='A chord splits the circle into two arcs'))

# ---- an angle intercepts an arc: stand at the vertex, the arms are walls
_c = (230, 185); _r = 140
_lA, _lB, _lC = gpt(*_c, _r, 15), gpt(*_c, _r, 105), gpt(*_c, _r, 250)
f1lean = PIN(GEO('f1lean', [
    ('line', f1_C(*_c, _r, ol=(-24, 6)) + f1_P(*_c, _r, 15, 'A') + f1_P(*_c, _r, 105, 'B')),
    ('arc', [('arcw', *_c, _r, 15, 105, 'teal', 9)]),
    ('cent', [f1_S(*_c, _r, None, 15, 'ink', 3), f1_S(*_c, _r, None, 105, 'ink', 3), ('arc', *_c, 30, 15, 105, 'teal')]),
    ('walls', [('path', [_lA, _c, _lB], 'orange', 12), ('txt', 560, 120, 'the arms are walls:', 'orange', 26),
               ('txt', 560, 160, 'you see only the teal arc', 'orange', 26)]),
    ('insc', f1_P(*_c, _r, 250, 'C') + [f1_S(*_c, _r, 250, 15, 'ink', 3), f1_S(*_c, _r, 250, 105, 'ink', 3), f1_ang(_lC, _lA, _lB, 34, 'teal')]),
    ('walls2', [('path', [_lA, _lC, _lB], 'orange', 12)]),
    ('both', [('txt', 560, 240, 'both angles intercept', 'teal', 26), ('txt', 560, 278, 'the arc A B', 'teal', 26)]),
], vb='50 -12 760 367', w=980, col=0, title='An angle intercepts an arc'))

# ---- another arc, and the arc an angle intercepts is the one between its arms
_c = (230, 185); _r = 140
_mA, _mB, _mD = gpt(*_c, _r, 200), gpt(*_c, _r, 330), gpt(*_c, _r, 80)
f1lean2 = PIN(GEO('f1lean2', [
    ('line', f1_C(*_c, _r, ol=(0, -24)) + f1_P(*_c, _r, 200, 'P') + f1_P(*_c, _r, 330, 'Q')),
    ('cent', [('arcw', *_c, _r, 200, 330, 'teal', 9), f1_S(*_c, _r, None, 200, 'ink', 3), f1_S(*_c, _r, None, 330, 'ink', 3),
              ('arc', *_c, 28, 200, 330, 'orange')]),
    ('insc', f1_P(*_c, _r, 80, 'D') + [f1_S(*_c, _r, 80, 200, 'ink', 3), f1_S(*_c, _r, 80, 330, 'ink', 3), f1_ang(_mD, _mA, _mB, 34, 'teal')]),
    ('look', [('txt', 560, 150, 'D looks down', 'teal', 26), ('txt', 560, 190, 'between its arms:', 'teal', 26),
              ('txt', 560, 230, 'the arc P Q', 'teal', 26)]),
], vb='50 -12 760 367', w=980, col=0, title='Another arc and the angles that intercept it'))

# ================================================================ part 3: tangent, sector, segment (the words only)
_c = (230, 185); _r = 120
def _f1_tan(deg, L=130, col='teal', name=None):
    T = gpt(*_c, _r, deg); p, q = gpt(T[0], T[1], L, deg + 90), gpt(T[0], T[1], L, deg - 90)
    e = [('seg', p[0], p[1], q[0], q[1], col, 4), ('dot', *T)]
    if name:
        lx, ly = gpt(*_c, _r + 24, deg); e.append(('txt', lx, ly, name, 'ink', 26, True))
    return e
f1tan = PIN(GEO('f1tan', [
    ('line', f1_C(*_c, _r, o=False)),
    ('t1', _f1_tan(90, name='T')),
    ('more', _f1_tan(215, 110) + _f1_tan(330, 110)),
    ('one', [('txt', 580, 150, 'touches the circle', 'teal', 28), ('txt', 580, 190, 'at exactly one point', 'teal', 28)]),
], vb='60 20 720 340', w=960, col=0, title='Tangents to a circle'))
f1tannot = PIN(GEO('f1tannot', [
    ('line', f1_C(110, 140, 75, o=False) + [('seg', 20, 200, 210, 70, 'red', 4), ('dot', *gpt(110, 140, 75, 213.4)),
              ('dot', *gpt(110, 140, 75, 35.4)), ('txt', 110, 250, 'crosses it: 2 points ✗', 'red', 22)]),
    ('miss', f1_C(400, 140, 75, o=False) + [('seg', 290, 40, 520, 40, 'red', 4), ('txt', 400, 250, 'misses it ✗', 'red', 22)]),
], vb='0 20 560 260', w=780, col=0, title='Two lines that are not tangents'))

# ---- the sector: two radii and the arc between them
_c = (230, 185); _r = 140
f1sec = PIN(GEO('f1sec', [
    ('line', f1_C(*_c, _r, ol=(-4, 26))),
    ('rr', f1_P(*_c, _r, 30, 'A') + f1_P(*_c, _r, 100, 'B') + [f1_S(*_c, _r, None, 30, 'ink', 3), f1_S(*_c, _r, None, 100, 'ink', 3),
                                                                ('arcw', *_c, _r, 30, 100, 'teal', 8)]),
    ('tint', [('wedge', *_c, _r, 30, 100, 'teal'), ('txt', 560, 150, 'a sector:', 'teal', 28),
              ('txt', 560, 190, 'a slice of the circle', 'teal', 28)]),
], vb='60 -12 720 367', w=840, col=0, title='A sector'))
def _f1_sv(cx, cy, r, a, b, lab, right=False):
    A, B = gpt(cx, cy, r, a), gpt(cx, cy, r, b)
    e = f1_C(cx, cy, r, o=False) + [('wedge', cx, cy, r, a, b, 'teal'), ('seg', cx, cy, A[0], A[1], 'ink', 3),
                                    ('seg', cx, cy, B[0], B[1], 'ink', 3), ('dot', cx, cy), ('txt', cx, cy + r + 32, lab, 'teal', 22)]
    if right: e.append(('right', cx, cy, a, b, 16))
    return e
f1secv = PIN(GEO('f1secv', [
    ('line', _f1_sv(110, 150, 85, 50, 90, 'a thin slice')),
    ('q', _f1_sv(330, 150, 85, 0, 90, 'a quarter', True)),
    ('h', _f1_sv(550, 150, 85, 0, 180, 'a half')),
], vb='10 55 640 225', w=960, col=0, title='Three sectors'))

# ---- the segment: a chord and its arc; next to the sector on the same arc
_c = (230, 185); _r = 140
f1seg = PIN(GEO('f1seg', [
    ('line', f1_C(*_c, _r, o=False)),
    ('ch', f1_P(*_c, _r, 30, 'A') + f1_P(*_c, _r, 120, 'B') + [f1_S(*_c, _r, 30, 120, 'ink', 3)]),
    ('tint', [('cseg', *_c, _r, 30, 120, 'orange'), ('arcw', *_c, _r, 30, 120, 'orange', 6),
              ('txt', 560, 150, 'a segment: between', 'orange', 28), ('txt', 560, 190, 'a chord and its arc', 'orange', 28)]),
], vb='60 -12 720 367', w=900, col=0, title='A segment of a circle'))
def _f1_cut(cx, cy, r, a, b, kind, lab):
    A, B = gpt(cx, cy, r, a), gpt(cx, cy, r, b)
    if kind == 'sector':
        e = [('wedge', cx, cy, r, a, b, 'teal'), ('seg', cx, cy, A[0], A[1], 'ink', 3), ('seg', cx, cy, B[0], B[1], 'ink', 3),
             ('dot', cx, cy)]
    else:
        e = [('cseg', cx, cy, r, a, b, 'orange'), ('seg', A[0], A[1], B[0], B[1], 'ink', 3)]
    return f1_C(cx, cy, r, o=False) + e + [('txt', cx, cy + r + 32, lab, 'teal' if kind == 'sector' else 'orange', 22)]
f1segv = PIN(GEO('f1segv', [
    ('line', _f1_cut(110, 150, 85, 40, 140, 'sector', 'sector')),
    ('s1', _f1_cut(330, 150, 85, 40, 140, 'segment', 'segment')),
    ('s2', _f1_cut(550, 150, 85, 160, 380, 'segment', 'a big segment')),
], vb='10 55 640 225', w=960, col=0, title='A sector and two segments'))


# ---- all together: name each line on one circle
_c = (230, 185); _r = 140
_T = gpt(*_c, _r, 105); _t1, _t2 = gpt(_T[0], _T[1], 95, 195), gpt(_T[0], _T[1], 95, 15)
f1all = PIN(GEO('f1all', [
    ('line', f1_C(*_c, _r, ol=(0, 26))),
    ('rad', f1_P(*_c, _r, 50, 'A') + [f1_S(*_c, _r, None, 50, 'teal', 4), ('txt', 600, 80, 'O A: a radius', 'teal', 26)]),
    ('dia', f1_P(*_c, _r, 165, 'B') + f1_P(*_c, _r, 345, 'C') + [f1_S(*_c, _r, 165, 345, 'teal', 4),
            ('txt', 600, 130, 'B C: a diameter', 'teal', 26), ('txt', 600, 164, '(and a chord)', 'teal', 22)]),
    ('ch', f1_P(*_c, _r, 220, 'D') + f1_P(*_c, _r, 290, 'E') + [f1_S(*_c, _r, 220, 290, 'teal', 4), ('txt', 600, 214, 'D E: a chord', 'teal', 26)]),
    ('tan', f1_P(*_c, _r, 105, 'T') + [('seg', *_t1, *_t2, 'teal', 4), ('txt', 600, 264, 'at T: a tangent', 'teal', 26)]),
], vb='50 -12 760 367', w=980, col=0, title='All the words on one circle'))


video('geo-074', 'lesson', slides=[
    S('Circle Vocabulary',
      L("Circles. Before we go through the rules we have in circles, the theorems, let's first get to know the lines and "
        "the angles we have in a circle.")),
    # ------------------------------------------------------------------ part 1
    S('The circle and its inside',
      L("So this is a circle. The round line we see here, going all the way around.", show(f1disk['line'], 'So this is a circle')),
      L("By the way, just for general knowledge. Most people don't know this, but strictly speaking, the circle is only "
        "the round line itself, the line around the outside. Everything inside it, the whole flat shape, is the inside of "
        "the circle, and in math it even has its own name. Think of a round wooden board. Its edge is the circle, and all "
        "the wood is the inside.",
        show(f1disk['trace'], 'the circle is only'), show(f1disk['in'], 'Everything inside it')),
      L("On the exam they don't keep this difference, and they don't use that name. They say circle for both. The area of the circle means the area "
        "inside, and the circumference is the length of the round line. That's fine, as long as we know which is which.",
        show(f1disk['exam'], 'They say circle for both'))),
    S('Radius',
      L("Radius. A radius is a straight line from the center of the circle to any point on the circle. We call the "
        "center O. Here's a radius, from O to the circle.", show(f1rad['line'], 'We call the center O'),
        show(f1rad['r1'], "Here's a radius")),
      L("All the radii of one circle are equal. Even if I draw more lines from the center to the circle, they're all "
        "the same length. Look. It's the same radius, just spinning around, and it's the same length in every direction.",
        show(f1rad['spin'], "It's the same radius, just spinning around"), show(f1rad['eq'], 'and it\'s the same length')),
      L("We usually mark the radius with the letter r.", pt('f1rad_r1', 'with the letter r'))),
    S('Every circle has its radius',
      L("So every circle has its own radius. Here's a circle with radius two. Every radius in it is two. A circle with "
        "radius three. Every radius in it is three. And a circle with radius five. Every radius is five. A different "
        "circle can have a different radius, but inside one circle, they're all the same.",
        show(f1radv['line'], "Here's a circle with radius two"), show(f1radv['c3'], 'A circle with radius three'),
        show(f1radv['c5'], 'And a circle with radius five'))),
    S('Two radii, a triangle',
      L("Why does this matter so much? Take two points on the circle, and join each one to the center. That's two radii. "
        "Now join the two points too. We get a triangle with two equal sides, an isosceles triangle. And we know from "
        "triangles that the two base angles of an isosceles triangle are equal.",
        show(f1iso['line'], 'Take two points on the circle'), pt('f1iso_line', 'two base angles')),
      L("Narrow, wide, or very wide, it's always the same. Two radii give an isosceles triangle. In questions, when you "
        "see two radii, mark them equal right away.",
        show(f1iso['t2'], 'Narrow, wide'), show(f1iso['t3'], 'or very wide'), show(f1iso['lab'], 'Two radii give an isosceles'))),
    S('Chord',
      L("Chord. A chord is a straight line that joins two points on the circle. Let's mark two points on the circle, A "
        "and B, and join them. That's a chord. Two more points, C and D. Join them. That's also a chord.",
        show(f1chord['line'], "Let's mark two points"), show(f1chord['ab'], 'A and B, and join them'),
        show(f1chord['cd'], 'Two more points')),
      L("We can draw as many chords as we like in a circle. And notice, they're not equal in length. A chord can be "
        "long, it can be short, and if I draw one here, it's a very short chord.",
        show(f1chord['ef'], 'if I draw one here'), show(f1chord['lens'], "it's a very short chord"))),
    S('Diameter',
      L("So which chord is the longest? Look at what happens when a chord moves toward the middle. Here's a short one. "
        "Closer to the middle, it's longer. Closer still, it's longer again.",
        show(f1diam['line'], 'So which chord is the longest'), show(f1diam['c1'], "Here's a short one"),
        show(f1diam['c2'], "Closer to the middle"), show(f1diam['c3'], 'Closer still')),
      L("The longest chord we can draw is the one that goes exactly through the middle, through the center. A chord "
        "like that is called a diameter.", show(f1diam['d'], 'exactly through the middle')),
      L("Its length is two r, because it's made of two radii. From A to the center is one radius, and from the center "
        "to B is another radius. So the diameter is r plus r, which is two r.",
        show(f1diam['rr'], 'From A to the center'), show(f1diam['two'], 'which is two r')),
      L("So if the diameter is fourteen, the radius is half of it, seven. And if the radius is six, the diameter is "
        "twelve. Many questions give you one and use the other, so switch between them right away.",
        show(f1d1, 'if the diameter is fourteen'), show(f1d2, 'if the radius is six'))),
    S('Two halves',
      L("A diameter also cuts the circle in half, into two equal halves. Each half is called a semicircle. And it "
        "doesn't matter which way we draw it. Across, at a slant, or another slant, it always goes through the center "
        "and makes two semicircles.",
        show(f1half['line'], 'cuts the circle in half'), show(f1half['h2'], 'at a slant'),
        show(f1half['h3'], 'or another slant'))),
    # ------------------------------------------------------------------ part 2
    S('Inscribed angle',
      L("Now the angles in a circle. The first one is the inscribed angle. An inscribed angle is an angle between two "
        "chords. Let's take a point C on the circle, and draw two chords from it, to A and to B.",
        show(f1insc['line'], 'Now the angles in a circle'), show(f1insc['c'], "Let's take a point C"),
        show(f1insc['ch'], 'draw two chords from it')),
      L("Its vertex, the point of the angle, is on the circle. That's why it's called inscribed. And the angle is "
        "exactly between the two chords.", show(f1insc['ang'], 'is on the circle'))),
    S('Is it inscribed?',
      L("Here's another inscribed angle, and another one, a big one. In both, the vertex is on the circle.",
        show(f1insv['line'], "Here's another inscribed angle"), show(f1insv['e2'], 'a big one')),
      L("But notice. If we just drew two lines and stopped somewhere in the middle of the circle, the vertex would be "
        "inside the circle. Or if they met out here, the vertex would be outside it. Those are not inscribed angles. "
        "An inscribed angle has its vertex on the circle.",
        show(f1insv['in'], 'stopped somewhere in the middle'), show(f1insv['out'], 'if they met out here'))),
    S('Central angle',
      L("Central angle. You can guess this one from the name. Its vertex is at the center of the circle, at O. And it's "
        "between two radii. Here's a radius, and here's a radius, and the angle between them is a central angle.",
        show(f1cent['line'], 'Central angle'), show(f1cent['rr'], "Here's a radius"),
        show(f1cent['ang'], 'the angle between them')),
      L("It can be small, like forty-five degrees. It can be big, like a hundred twenty. And when the two radii make a "
        "straight line, a diameter, it's a central angle of a hundred eighty degrees.",
        show(f1cenv['line'], 'like forty-five degrees'), show(f1cenv['c2'], 'like a hundred twenty'),
        show(f1cenv['c3'], 'when the two radii make a straight line'))),
    S('Arc',
      L("Arc. An arc is a part of the circle, a piece of the round line. Let's mark a piece of the circle. That's an "
        "arc. An arc can be short. It can be longer. And it can be very long, almost the whole circle.",
        show(f1arcv['line'], "Let's mark a piece of the circle"), show(f1arcv['a2'], 'It can be longer'),
        show(f1arcv['a3'], 'almost the whole circle')),
      L("An arc can be closed off by a chord. Here's a chord, A B. It splits the circle into two arcs. There's the arc on "
        "this side, the short one. On the exam it's called the minor arc.",
        show(f1arc['line'], 'closed off by a chord'), show(f1arc['ch'], "Here's a chord"), show(f1arc['mi'], 'the short one')),
      L("And there's another arc, a bigger one, all the way around the other side. That's the major arc. People often "
        "think an arc is always something short. But this whole long piece is an arc too, even though it's more than "
        "half the circle.", show(f1arc['ma'], 'a bigger one'))),
    S('Intercepts an arc',
      L("Now here's an arc, from A to B. We can close it off with two radii. That's a central angle that closes off our "
        "arc.", show(f1lean['line'], "Now here's an arc"), show(f1lean['arc'], 'from A to B'),
        show(f1lean['cent'], 'with two radii')),
      L("When an angle closes off an arc like this, we say that the angle intercepts the arc. What does that mean? "
        "Imagine I'm standing inside the angle, at O. The two radii are walls, tall walls. From where I stand, the part "
        "of the circle I can see is only this arc.", show(f1lean['walls'], 'The two radii are walls')),
      L("We can also close off the same arc with an inscribed angle. Take a point C on the circle, and draw two chords "
        "to A and to B. If I stand at C, the chords are tall walls, and again, the part of the circle I can see is only "
        "this arc.", show(f1lean['insc'], 'Take a point C'), show(f1lean['walls2'], 'the chords are tall walls')),
      L("So this central angle and this inscribed angle both intercept the same arc, the teal arc A B.",
        show(f1lean['both'], 'both intercept the same arc'))),
    S('Another arc',
      L("Here's one more arc, a bigger one, from P to Q, along the bottom. The central angle at O intercepts it. And an "
        "inscribed angle from D, up at the top, intercepts it too. Stand at D and look down between the two chords. "
        "What you see is the arc P Q. So the arc an angle intercepts is always the one between its arms, on the side "
        "it opens to.", show(f1lean2['line'], "Here's one more arc"), show(f1lean2['cent'], 'The central angle at O'),
        show(f1lean2['insc'], 'And an inscribed angle from D'), show(f1lean2['look'], 'Stand at D'))),
    # ------------------------------------------------------------------ part 3
    S('Tangent',
      L("A few more words that come up a lot. A tangent is a straight line that touches the circle at exactly one "
        "point. Here's a tangent. It touches the circle at T, and it doesn't go inside.",
        show(f1tan['line'], 'A tangent is a straight line'), show(f1tan['t1'], "Here's a tangent")),
      L("We can draw a tangent at any point of the circle. Here's one, and here's another. Each one touches the circle "
        "at just one point.", show(f1tan['more'], 'Here\'s one, and here\'s another'),
        show(f1tan['one'], 'at just one point')),
      L("A line that goes through the circle, and crosses it at two points, is not a tangent. And a line that misses "
        "the circle isn't one either. The rules of tangents get their own lesson.",
        show(f1tannot['line'], 'crosses it at two points'), show(f1tannot['miss'], 'misses the circle'))),
    S('Sector',
      L("A sector. Take two radii, O A and O B, and the arc between them. The part of the circle they close off is a "
        "sector. It's a slice of the circle, like a slice of pizza.",
        show(f1sec['line'], 'A sector'), show(f1sec['rr'], 'Take two radii'), show(f1sec['tint'], 'is a sector')),
      L("A sector can be a thin slice. It can be a quarter of the circle, when the central angle is ninety degrees. "
        "And a half, a semicircle, is a sector too. We'll learn the area of a sector in its own lesson.",
        show(f1secv['line'], 'a thin slice'), show(f1secv['q'], 'a quarter of the circle'), show(f1secv['h'], 'a semicircle'))),
    S('Segment',
      L("And the last one, a segment. Take a chord, A B. The part of the circle between the chord and its arc is called "
        "a segment.", show(f1seg['line'], 'And the last one'), show(f1seg['ch'], 'Take a chord'),
        show(f1seg['tint'], 'between the chord and its arc')),
      L("Don't mix it up with a sector. A sector goes all the way to the center, with two radii. A segment is cut off "
        "by a chord, and it doesn't reach the center. A segment can be small, or big, more than half the circle. On the "
        "exam it usually appears as a shaded region between a chord and an arc.",
        show(f1segv['line'], 'A sector goes all the way'), show(f1segv['s1'], 'A segment is cut off'),
        show(f1segv['s2'], 'or big'))),
    S('All together',
      L("Let's put it all together on one circle. Try to name each line before I do. O A goes from the center to the "
        "circle, so it's a radius. B C goes through the center, so it's a diameter. And it's also a chord, the longest "
        "one.", show(f1all['line'], "Let's put it all together"), show(f1all['rad'], 'O A goes from the center'),
        show(f1all['dia'], 'B C goes through the center')),
      L("D E joins two points on the circle, but it doesn't go through the center, so it's just a chord. And the line "
        "at T touches the circle at one point only, so it's a tangent.",
        show(f1all['ch'], "D E joins two points"), show(f1all['tan'], 'the line at T touches')),
      L("That's it for the words we use in a circle. In the next lesson we start on the rules, the angles in a circle, "
        "and what we know about them. [pause] Okay. I'll see you in the next video.")),
])

CAMERA_SPLIT = ('geo-074', 'Circle Vocabulary', [
    (1, None),
    (8, "Let's continue with circles, this time with the angles and the arcs."),
    (13, "Let's continue with circles, with one more arc and a few more words."),
])

# =================================================================================================================
# Topic-33 fragment f2 (TAG B, 2026-10-14): geo-075 "Angles in a Circle" (lesson), solve-geo33-g076 (the lesson's
# sample question), solve-q-r26-t33-01 (a course addition: a chord, its distance and the radius).
# Hebrew: geo 3513-3610 (angles in a circle + its sample question, AOC = 90 -> 135 there, 104 -> 128 here).
# Written to the guide (R1-R36, clarity, Codex standard, V1-V3). Every figure is PINned.
# =================================================================================================================
import math as _f2m

FIG_LEFT.update({'solve-geo33-g076', 'solve-q-r26-t33-01'})


def f2_on(c, r, deg):
    """a point on the circle with center c and radius r"""
    return gpt(c[0], c[1], r, deg)


def f2_lab(c, r, deg, name, d=24, size=26, col='ink'):
    """a point name just outside the circle, at the point's own direction"""
    x, y = gpt(c[0], c[1], r + d, deg)
    return ('txt', x, y, name, col, size, True)


def f2_ang(P, Q, R, r, col, label=None, lr=None):
    """the smaller angle at P between the rays P->Q and P->R"""
    a, b = gdir(*P, *Q), gdir(*P, *R)
    if (b - a) % 360 > 180: a, b = b, a
    e = ('arc', P[0], P[1], r, a, b, col)
    if label: e = e + (label,) + ((lr,) if lr else ())
    return e


def f2_right(P, Q, R, sz=14, col='teal'):
    return ('right', P[0], P[1], gdir(*P, *Q), gdir(*P, *R), sz, col)


def f2_seg(P, Q, col='ink', w=3, dash=False):
    return ('seg', P[0], P[1], Q[0], Q[1], col, w, dash)


def f2_dot(P):
    return ('dot', P[0], P[1])


def f2_albl(P, Q, R, d, text, col, size):
    """a label for the smaller angle at P, at distance d along its middle direction"""
    a, b = gdir(*P, *Q), gdir(*P, *R)
    if (b - a) % 360 > 180: a, b = b, a
    x, y = gpt(P[0], P[1], d, a + ((b - a) % 360) / 2.0)
    return ('txt', x, y, text, col, size)


def f2_wedge(P, Q, R, r, col, n=16):
    """a tinted sector for the smaller angle at P (a polygon)"""
    a, b = gdir(*P, *Q), gdir(*P, *R)
    if (b - a) % 360 > 180: a, b = b, a
    span = (b - a) % 360
    return ('tint', [P] + [gpt(P[0], P[1], r, a + span * k / float(n)) for k in range(n + 1)], col)


# ================================================================================================ geo-075 (lesson)
# Hebrew (geo 3513-3610): central = 2 x inscribed on the same arc ("it doesn't matter, the same thing"); the inscribed
# vertex can be here, or here, or here: inscribed angles on the same arc, or on equal arcs, are equal (why: each is half
# of the central); an inscribed angle on a diameter is 90 (why: the central is the straight 180, half is 90), "very very
# important", "these three rules are used a lot"; the inscribed quadrilateral (all four vertices on the circle; one inside
# or outside -> not inscribed), opposite angles add to 180 (70 -> 110 there, 75 -> 105 here), the proof with two radii,
# 2 alpha + 2 beta = 360; the summary "one important rule, the others come from it".
# Kept from the English lesson: the backwards rule (a right angle on the circle -> a diameter; right triangle / rectangle),
# the numbers 120/60 and 38/76, equal chords <-> equal arcs <-> equal central angles (Hebrew practice geo 3966-4000 uses it
# "as we learned").
# Added (course): the why of the main rule (the diameter from C, two isosceles triangles); the traps (vertex inside; a
# vertex on the arc itself sees the other arc; the hypotenuse is the diameter, not the radius; a corner at the center is
# not on the circle; same circle only; perpendicular only from the center); the radius perpendicular to a chord halves it
# (used in solve-q-r26-t33-01 and r26-t33-more-tools).
# V3: every rule on a clean generic circle, built at her words; the arc being discussed thick teal; central angles orange
# (large), inscribed teal (small), wrong red; construction lines (diameter, radii, perpendicular) dashed teal; values
# written on the figure; 2-3 positions for each rule.

F2O = (170.0, 180.0); F2R = 130.0
_o = F2O; _r = F2R


def f2_base(c=F2O, r=F2R, center=True, olab=(14, 14)):
    out = [('circ', c[0], c[1], r)]
    if center: out += [f2_dot(c), ('txt', c[0] + olab[0], c[1] + olab[1], 'O', 'ink', 24, True)]
    return out


# ---- rule 1: central = 2 x inscribed (120 / 60)
_A1, _B1, _C1 = f2_on(_o, _r, 340), f2_on(_o, _r, 100), f2_on(_o, _r, 220)
f2r1 = PIN(GEO('f2r1', [
    ('line', f2_base(olab=(-20, 6)) + [f2_dot(_A1), f2_dot(_B1), f2_lab(_o, _r, 340, 'A'), f2_lab(_o, _r, 100, 'B')]),
    ('arc', [('arcw', _o[0], _o[1], _r, 340, 100, 'teal')]),
    ('cen', [f2_seg(_o, _A1), f2_seg(_o, _B1), ('wedge', _o[0], _o[1], 34, 340, 100, 'orange'),
             ('arc', _o[0], _o[1], 34, 340, 100, 'orange', '120°', 62)]),
    ('ins', [f2_dot(_C1), f2_lab(_o, _r, 220, 'C'), f2_seg(_C1, _A1), f2_seg(_C1, _B1), f2_ang(_C1, _A1, _B1, 40, 'teal')]),
    ('rule', [('txt', 480, 120, 'central = 2 × inscribed', 'ink', 26), ('txt', 480, 160, 'inscribed = ½ central', 'ink', 26)]),
    ('ex1', [f2_wedge(_C1, _A1, _B1, 40, 'teal'), f2_ang(_C1, _A1, _B1, 40, 'teal', '60°', 66),
             ('txt', 480, 230, '120° ÷ 2 = 60°', 'teal', 28)]),
], vb='0 12 660 340', w=1100, col=0, title='The central angle is twice the inscribed angle'))

# ---- rule 1 again: a narrow arc, the center outside the inscribed angle (38 / 76)
_A2, _B2, _C2 = f2_on(_o, _r, 290), f2_on(_o, _r, 6), f2_on(_o, _r, 215)
f2r1b = PIN(GEO('f2r1b', [
    ('line', f2_base(olab=(-14, -16)) + [f2_dot(_A2), f2_dot(_B2), f2_dot(_C2), f2_lab(_o, _r, 290, 'A'), f2_lab(_o, _r, 6, 'B'),
                                         f2_lab(_o, _r, 215, 'C')]),
    ('ins', [('arcw', _o[0], _o[1], _r, 290, 6, 'teal'), f2_seg(_C2, _A2), f2_seg(_C2, _B2),
             f2_wedge(_C2, _A2, _B2, 56, 'teal'), f2_ang(_C2, _A2, _B2, 56, 'teal', '38°', 84)]),
    ('cen', [f2_seg(_o, _A2), f2_seg(_o, _B2), ('wedge', _o[0], _o[1], 30, 290, 6, 'orange'),
             ('arc', _o[0], _o[1], 30, 290, 6, 'orange', '76°', 72), ('txt', 480, 160, '38° × 2 = 76°', 'orange', 28),
             ('txt', 480, 205, 'O is outside the angle,', 'ink', 22), ('txt', 480, 235, 'the rule still works', 'ink', 22)]),
], vb='0 12 660 340', w=1100, col=0, title='The same rule on a narrow arc'))

# ---- why: the diameter from C, two isosceles triangles
_O3 = (170.0, 186.0); _r3 = 134.0
_A3, _B3, _C3, _D3 = f2_on(_O3, _r3, 5), f2_on(_O3, _r3, 160), f2_on(_O3, _r3, 270), f2_on(_O3, _r3, 90)
f2why = PIN(GEO('f2why', [
    ('line', f2_base(_O3, _r3, olab=(-18, 20)) + [f2_dot(_A3), f2_dot(_B3), f2_dot(_C3), f2_lab(_O3, _r3, 5, 'A'),
                                                  f2_lab(_O3, _r3, 160, 'B'), f2_lab(_O3, _r3, 270, 'C'),
                                                  f2_seg(_C3, _A3), f2_seg(_C3, _B3), f2_seg(_O3, _A3), f2_seg(_O3, _B3)]),
    ('diam', [f2_seg(_C3, _D3, 'teal', 3, True), f2_dot(_D3), f2_lab(_O3, _r3, 90, 'D')]),
    ('left', [('tint', [_O3, _C3, _A3], 'teal'), ('tick', _O3[0], _O3[1], _C3[0], _C3[1], 1), ('tick', _O3[0], _O3[1], _A3[0], _A3[1], 1),
              f2_ang(_C3, _D3, _A3, 60, 'teal', 'x', 82), f2_ang(_A3, _C3, _O3, 46, 'teal', 'x', 68)]),
    ('ext', [f2_ang(_O3, _A3, _D3, 30, 'teal', '2x', 52), ('txt', 490, 95, 'COA = 180° − 2x', 'teal', 26),
             ('txt', 490, 132, 'AOD = 2x', 'teal', 26)]),
    ('rt', [('tint', [_O3, _C3, _B3], 'orange'), ('tick', _O3[0], _O3[1], _B3[0], _B3[1], 1),
            f2_ang(_C3, _B3, _D3, 70, 'orange', 'y', 92), f2_ang(_B3, _O3, _C3, 46, 'orange', 'y', 68),
            f2_ang(_O3, _D3, _B3, 30, 'orange', '2y', 52), ('txt', 490, 180, 'BOD = 2y', 'orange', 26)]),
    ('sum', [('txt', 490, 245, 'inscribed: x + y', 'ink', 28), ('txt', 490, 288, 'central: 2x + 2y', 'ink', 28)]),
], vb='0 12 660 340', w=1100, col=0, title='Why the central angle is twice the inscribed angle'))


# ---- rule 2: same arc, same angle (100 / 50)
_A5, _B5 = f2_on(_o, _r, 40), f2_on(_o, _r, 140)
_C5, _D5, _E5, _F5 = f2_on(_o, _r, 205), f2_on(_o, _r, 268), f2_on(_o, _r, 330), f2_on(_o, _r, 90)
f2same = PIN(GEO('f2same', [
    ('line', f2_base(olab=(0, 22)) + [f2_dot(_A5), f2_dot(_B5), f2_lab(_o, _r, 40, 'A'), f2_lab(_o, _r, 140, 'B'),
                                      ('arcw', _o[0], _o[1], _r, 40, 140, 'teal')]),
    ('cen', [f2_seg(_o, _A5), f2_seg(_o, _B5), ('arc', _o[0], _o[1], 28, 40, 140, 'orange', '100°', 50)]),
    ('c', [f2_dot(_C5), f2_lab(_o, _r, 205, 'C'), f2_seg(_C5, _A5, 'teal', 2.5), f2_seg(_C5, _B5, 'teal', 2.5),
           f2_ang(_C5, _A5, _B5, 40, 'teal', '50°', 62)]),
    ('d', [f2_dot(_D5), f2_lab(_o, _r, 268, 'D'), f2_seg(_D5, _A5, 'teal', 2.5), f2_seg(_D5, _B5, 'teal', 2.5),
           f2_ang(_D5, _A5, _B5, 40, 'teal', '50°', 62)]),
    ('e', [f2_dot(_E5), f2_lab(_o, _r, 330, 'E'), f2_seg(_E5, _A5, 'teal', 2.5), f2_seg(_E5, _B5, 'teal', 2.5),
           f2_ang(_E5, _A5, _B5, 40, 'teal', '50°', 62), ('txt', 490, 150, 'same arc AB', 'teal', 26),
           ('txt', 490, 188, '→ equal angles', 'teal', 26)]),
    ('f', [f2_dot(_F5), f2_lab(_o, _r, 90, 'F', 22, 26, 'red'), f2_seg(_F5, _A5, 'red', 2.5), f2_seg(_F5, _B5, 'red', 2.5),
           f2_ang(_F5, _A5, _B5, 22, 'red'), ('txt', 490, 245, 'F sees the long arc:', 'red', 24), ('txt', 490, 277, 'not 50° ✗', 'red', 24)]),
], vb='0 12 660 340', w=1100, col=0, title='Inscribed angles on the same arc are equal'))

# ---- rule 3: on a diameter -> 90
_O6 = (170.0, 185.0)
_A6, _B6 = f2_on(_O6, _r, 180), f2_on(_O6, _r, 0)
_C6, _C6b, _C6c = f2_on(_O6, _r, 118), f2_on(_O6, _r, 50), f2_on(_O6, _r, 300)
f2diam = PIN(GEO('f2diam', [
    ('line', f2_base(_O6, olab=(-16, -16)) + [f2_seg(_A6, _B6), f2_dot(_A6), f2_dot(_B6), ('txt', _A6[0] - 22, _A6[1], 'A', 'ink', 26, True),
                                           ('txt', _B6[0] + 22, _B6[1], 'B', 'ink', 26, True)]),
    ('c', [f2_dot(_C6), f2_lab(_O6, _r, 118, 'C'), f2_seg(_C6, _A6, 'teal'), f2_seg(_C6, _B6, 'teal'), f2_right(_C6, _A6, _B6, 16)]),
    ('cen', [('arc', _O6[0], _O6[1], 30, 180, 360, 'orange', '180°', 54)]),
    ('calc', [('txt', 480, 120, '180° ÷ 2 = 90°', 'teal', 28)]),
    ('more', [f2_dot(_C6b), f2_seg(_C6b, _A6, 'teal', 2.5), f2_seg(_C6b, _B6, 'teal', 2.5), f2_right(_C6b, _A6, _B6, 14),
              f2_dot(_C6c), f2_seg(_C6c, _A6, 'teal', 2.5), f2_seg(_C6c, _B6, 'teal', 2.5), f2_right(_C6c, _A6, _B6, 14),
              ('txt', 480, 190, 'always 90°', 'teal', 28)]),
], vb='0 12 660 340', w=1100, col=0, title='An inscribed angle on a diameter is 90 degrees'))

# ---- rule 3 backwards: a right triangle and a rectangle in a circle
_Ol, _rl = (150.0, 185.0), 115.0
_Al, _Bl = f2_on(_Ol, _rl, 180), f2_on(_Ol, _rl, 0)
_Cl = f2_on(_Ol, _rl, 2 * _f2m.degrees(_f2m.atan(10 / 24.0)))       # BC : AC = 10 : 24
_Or, _rr = (500.0, 185.0), 115.0
_K = [f2_on(_Or, _rr, d) for d in (35, 145, 215, 325)]
f2back = PIN(GEO('f2back', [
    ('line', [('circ', _Ol[0], _Ol[1], _rl), f2_seg(_Al, _Bl), f2_seg(_Al, _Cl), f2_seg(_Cl, _Bl), f2_right(_Cl, _Al, _Bl, 14)]),
    ('hyp', [f2_seg(_Al, _Bl, 'teal', 6), f2_dot(_Ol), ('txt', _Ol[0], _Ol[1] + 26, 'diameter', 'teal', 22)]),
    ('num', [('txt', 120, 112, '24', 'ink', 24), ('txt', 278, 128, '10', 'ink', 24), ('txt', _Ol[0], _Ol[1] + 56, '26', 'teal', 26),
             ('txt', _Ol[0], 340, 'r = 26 ÷ 2 = 13', 'teal', 26)]),
    ('rect', [('circ', _Or[0], _Or[1], _rr)] + [f2_seg(_K[i], _K[(i + 1) % 4]) for i in range(4)]
     + [f2_seg(_K[0], _K[2], 'teal', 4), f2_seg(_K[1], _K[3], 'teal', 4), f2_dot(_Or),
        ('txt', _Or[0], 340, 'diagonal = diameter', 'teal', 26)]),
], vb='20 50 620 310', w=1060, col=0, title='A right angle on the circle sits on a diameter'))

# ---- the inscribed quadrilateral: definition (one yes, two no)
def _f2_mini(cx, pts_deg, extra):
    c = (cx, 160.0); r = 80.0
    pts = [f2_on(c, r, d) if isinstance(d, (int, float)) else d for d in pts_deg]
    return [('circ', c[0], c[1], r)] + extra(c, pts)
_cA = (110.0, 160.0); _cB = (330.0, 160.0); _cC = (550.0, 160.0)
_qa = [f2_on(_cA, 80, d) for d in (130, 220, 290, 10)]
_qb = [f2_on(_cB, 80, d) for d in (130, 220, 290)] + [(_cB[0] + 30, _cB[1] - 22)]
_qc = [f2_on(_cC, 80, d) for d in (150, 230, 320)] + [_cC]
f2qdef = PIN(GEO('f2qdef', [
    ('line', [('circ', _cA[0], _cA[1], 80)] + [f2_seg(_qa[i], _qa[(i + 1) % 4], 'teal') for i in range(4)]
     + [f2_dot(p) for p in _qa] + [('txt', _cA[0], 272, 'inscribed ✓', 'teal', 24)]),
    ('in', [('circ', _cB[0], _cB[1], 80)] + [f2_seg(_qb[i], _qb[(i + 1) % 4], 'red') for i in range(4)]
     + [f2_dot(p) for p in _qb] + [('txt', _cB[0], 272, 'a corner inside ✗', 'red', 24)]),
    ('ctr', [('circ', _cC[0], _cC[1], 80)] + [f2_seg(_qc[i], _qc[(i + 1) % 4], 'red') for i in range(4)]
     + [f2_dot(p) for p in _qc] + [('txt', _cC[0] + 14, _cC[1] - 18, 'O', 'red', 22, True),
                                   ('txt', _cC[0], 272, 'a corner at O ✗', 'red', 24)]),
], vb='10 60 640 230', w=1060, col=0, title='An inscribed quadrilateral: all four corners on the circle'))

# ---- rule 4: opposite angles add up to 180 (A 75, C 105; B 100, D 80)
_O8 = (170.0, 180.0)
_qA, _qB, _qC, _qD = f2_on(_O8, _r, 130), f2_on(_O8, _r, 220), f2_on(_O8, _r, 290), f2_on(_O8, _r, 10)
_Q8 = [_qA, _qB, _qC, _qD]
f2q8_line = (f2_base(_O8, center=False) + [f2_seg(_Q8[i], _Q8[(i + 1) % 4]) for i in range(4)] + [f2_dot(p) for p in _Q8]
             + [f2_lab(_O8, _r, 130, 'A'), f2_lab(_O8, _r, 220, 'B'), f2_lab(_O8, _r, 290, 'C'), f2_lab(_O8, _r, 10, 'D')])
f2quad = PIN(GEO('f2quad', [
    ('line', f2q8_line),
    ('ac', [f2_ang(_qA, _qB, _qD, 30, 'teal', '75°', 56), f2_ang(_qC, _qB, _qD, 30, 'orange', '105°', 58),
            ('txt', 480, 130, '75° + 105° = 180°', 'ink', 26), ('txt', 480, 175, 'same for B and D', 'ink', 24)]),
], vb='0 12 660 340', w=1100, col=0, title='Opposite angles of an inscribed quadrilateral'))

# ---- why: two radii, 2 alpha + 2 beta = 360
f2qwhy = PIN(GEO('f2qwhy', [
    ('line', f2q8_line + [f2_ang(_qA, _qB, _qD, 30, 'teal', 'α', 52), f2_ang(_qC, _qB, _qD, 30, 'orange', 'β', 52)]),
    ('rad', [f2_dot(_O8), ('txt', _O8[0] + 10, _O8[1] - 16, 'O', 'ink', 22, True), f2_seg(_O8, _qB, 'teal', 3, True),
             f2_seg(_O8, _qD, 'teal', 3, True)]),
    ('a', [('arcw', _O8[0], _O8[1], _r, 220, 10, 'teal'), ('arc', _O8[0], _O8[1], 40, 220, 10, 'teal'), ('txt', *gpt(_O8[0], _O8[1], 68, 330), '2α', 'teal', 26)]),
    ('b', [('arcw', _O8[0], _O8[1], _r, 10, 220, 'orange'), ('arc', _O8[0], _O8[1], 50, 10, 220, 'orange'), ('txt', *gpt(_O8[0], _O8[1], 72, 165), '2β', 'orange', 26)]),
    ('sum', [('txt', 480, 130, '2α + 2β = 360°', 'ink', 28), ('txt', 480, 180, 'α + β = 180°', 'red', 28)]),
], vb='0 12 660 340', w=1100, col=0, title='Why opposite angles add up to 180'))

# ---- equal chords <-> equal central angles <-> equal arcs (70 / 70)
_A9, _B9, _C9, _D9 = f2_on(_o, _r, 20), f2_on(_o, _r, 90), f2_on(_o, _r, 190), f2_on(_o, _r, 260)
f2chord = PIN(GEO('f2chord', [
    ('line', f2_base(olab=(16, 18)) + [f2_seg(_A9, _B9), f2_seg(_C9, _D9), f2_dot(_A9), f2_dot(_B9), f2_dot(_C9), f2_dot(_D9),
                                        f2_lab(_o, _r, 20, 'A'), f2_lab(_o, _r, 90, 'B'), f2_lab(_o, _r, 190, 'C'), f2_lab(_o, _r, 260, 'D'),
                                        ('tick', _A9[0], _A9[1], _B9[0], _B9[1], 2), ('tick', _C9[0], _C9[1], _D9[0], _D9[1], 2)]),
    ('rad', [f2_seg(_o, p, 'teal', 3, True) for p in (_A9, _B9, _C9, _D9)] + [('tint', [_o, _A9, _B9], 'teal'), ('tint', [_o, _C9, _D9], 'teal'),
             ('txt', 480, 110, 'r, r and the chord:', 'teal', 24), ('txt', 480, 142, 'the same triangle', 'teal', 24)]),
    ('ang', [('arc', _o[0], _o[1], 30, 20, 90, 'teal', '70°', 52), ('arc', _o[0], _o[1], 30, 190, 260, 'teal', '70°', 52)]),
    ('arcs', [('arcw', _o[0], _o[1], _r, 20, 90, 'teal'), ('arcw', _o[0], _o[1], _r, 190, 260, 'teal'),
              ('txt', 480, 200, 'equal arcs', 'teal', 26), ('txt', 480, 240, 'inscribed: 35° each', 'teal', 24)]),
    ('trap', [('txt', 480, 295, 'only in the same circle', 'red', 24)]),
], vb='0 12 660 340', w=1100, col=0, title='Equal chords cut off equal arcs'))

# ---- a perpendicular from the center halves the chord
_O10 = (170.0, 165.0)
_A10, _B10, _M10 = (58.0, 231.0), (282.0, 231.0), (170.0, 231.0)       # 66 - 112 - 130 (33-56-65 doubled)
_P10 = (240.0, 140.0); _F10 = (240.0, 231.0)
f2perp = PIN(GEO('f2perp', [
    ('line', f2_base(_O10, olab=(-18, -10)) + [f2_seg(_A10, _B10), f2_dot(_A10), f2_dot(_B10), ('txt', _A10[0] - 18, _A10[1] + 14, 'A', 'ink', 26, True),
                                               ('txt', _B10[0] + 18, _B10[1] + 14, 'B', 'ink', 26, True)]),
    ('perp', [f2_seg(_O10, _M10, 'teal', 3, True), f2_right(_M10, _O10, _B10, 14), f2_dot(_M10),
              ('txt', _M10[0], _M10[1] + 26, 'M', 'ink', 24, True)]),
    ('half', [('tick', _A10[0], _A10[1], _M10[0], _M10[1], 1), ('tick', _M10[0], _M10[1], _B10[0], _B10[1], 1),
              ('txt', 114, 262, '7', 'teal', 26), ('txt', 226, 262, '7', 'teal', 26), ('txt', 490, 110, 'AB = 14 → 7 and 7', 'teal', 26),
              ]),
    ('why', [f2_seg(_O10, _A10, 'teal', 3, True), f2_seg(_O10, _B10, 'teal', 3, True), ('tint', [_O10, _A10, _B10], 'teal'),
             ('tick', _O10[0], _O10[1], _A10[0], _A10[1], 2), ('tick', _O10[0], _O10[1], _B10[0], _B10[1], 2),
             ('txt', 490, 160, 'OA = OB: isosceles', 'teal', 24)]),
], vb='0 20 660 300', w=1100, col=0, title='A perpendicular from the center cuts a chord in half'))


f2s1 = I('f2s1', 'Inscribed angle = half the central angle (same arc)', size=40)
f2s2 = I('f2s2', 'Same arc → equal inscribed angles', size=40)
f2s3 = I('f2s3', 'On a diameter → 90°', size=40)
f2s4 = I('f2s4', 'Inscribed quadrilateral → opposite angles add up to 180°', size=40)
f2s5 = I('f2s5', 'Equal chords ↔ equal arcs ↔ equal central angles', size=40)
f2s6 = I('f2s6', 'Perpendicular from the center → cuts the chord in half', size=40)

video('geo-075', 'lesson', slides=[
    S('Angles in a Circle',
      L("Angles in a circle. Last lesson we learned the words of the circle. Now we start the rules. They come up in "
        "almost every circle question, and really, there's one main rule, and the others come from it.")),
    S('Central = 2 × inscribed',
      L("The main rule. A central angle is twice the inscribed angle that intercepts the same arc. Here's a circle with "
        "its center O, and two points, A and B.", show(f2r1['line'], "Here's a circle")),
      L("Here's the arc from A to B, and a central angle on it, a hundred twenty degrees. Its vertex is at the center, and its two radii close off the "
        "arc.",
        show(f2r1['arc'], "Here's the arc"), show(f2r1['cen'], 'and a central angle on it')),
      L("And here's an inscribed angle at C. Stand at C, between the two chords, and you see the same arc. "
        "Careful, the vertex of an inscribed angle must be on the circle, not inside it.",
        show(f2r1['ins'], "here's an inscribed angle")),
      L("The inscribed angle is half of the central angle. Or the central angle is twice the inscribed angle. It's the "
        "same thing. So here it's half of a hundred twenty, sixty.", show(f2r1['rule'], 'The inscribed angle is half'),
        show(f2r1['ex1'], "So here it's half"))),
    S('Another position',
      L("Another example, on a narrow arc. The inscribed angle at C is thirty-eight, so the central angle is twice that, "
        "seventy-six. Here the center is outside the angle, and the rule still works.",
        show(f2r1b['line'], 'Another example'), show(f2r1b['ins'], 'The inscribed angle at C'),
        show(f2r1b['cen'], 'so the central angle'))),
    S('Why it works',
      L("Why is it true? Let's draw the diameter from C, through the center, to D.",
        show(f2why['line'], 'Why is it true'), show(f2why['diam'], "Let's draw the diameter")),
      L("Triangle O C A has two radii, so it's isosceles, and its base angles are equal. Call them x. The angle at O "
        "inside it is a hundred eighty minus two x, so the angle next to it on the straight line is two x.",
        show(f2why['left'], 'Triangle O C A'), show(f2why['ext'], 'The angle at O')),
      L("The same on the other side, with y. So the inscribed angle is x plus y, and the central angle is two x plus two "
        "y, exactly twice as much.", show(f2why['rt'], 'The same on the other side'),
        show(f2why['sum'], 'So the inscribed angle'))),
    S('Same arc, same angle',
      L("The second rule. Inscribed angles that intercept the same arc are equal. Here the central angle on arc A B is a "
        "hundred.", show(f2same['line'], 'Here the central angle'), show(f2same['cen'], 'is a hundred')),
      L("An inscribed angle at C is half of it, fifty. Now let's move the vertex. Here at D, and here at E. It doesn't "
        "matter where we put it, each one is fifty.", show(f2same['c'], 'An inscribed angle at C'),
        show(f2same['d'], 'Here at D'), show(f2same['e'], 'and here at E')),
      L("Why? Each one is half of the same central angle, so they're all equal. And it's the same for two equal arcs.",
        pt('f2same_e', 'Each one is half')),
      L("But careful. Here at F, the vertex is on the arc A B itself. From F you see the long arc, so this angle is not "
        "fifty. Always check which arc the angle sees.", show(f2same['f'], 'Here at F'))),
    S('Angle on a diameter',
      L("The third rule. An inscribed angle on a diameter is ninety degrees. Here's a diameter, A B, and an inscribed angle "
        "on it, at C. Its chords go to the two ends of the diameter.", show(f2diam['line'], "Here's a diameter"), show(f2diam['c'], 'and an inscribed angle')),
      L("Why? It's the main rule again. The central angle on a diameter is the straight line at O, a hundred eighty. Half "
        "of a hundred eighty is ninety.", show(f2diam['cen'], 'The central angle on a diameter'),
        show(f2diam['calc'], 'Half of a hundred eighty')),
      L("And wherever C is, here, here, or even on the bottom half, it's always ninety. This one is very, very important "
        "for the exam. Really, these first three rules are used all the time.", show(f2diam['more'], 'And wherever C is'))),
    S('Backwards: a right angle',
      L("It also works backwards. When a right triangle has all three corners on a circle, its hypotenuse is a diameter.",
        show(f2back['line'], 'When a right triangle'), show(f2back['hyp'], 'its hypotenuse is a diameter')),
      L("Say the legs are ten and twenty-four. That's five, twelve, thirteen, doubled, so the hypotenuse is twenty-six. "
        "Careful, many students call that the radius. But twenty-six is the diameter, so the radius is thirteen. And in a "
        "rectangle inside a circle, each diagonal is a diameter.", show(f2back['num'], 'Say the legs'),
        show(f2back['rect'], 'And in a rectangle'))),
    S('Inscribed quadrilateral',
      L("The fourth rule. An inscribed quadrilateral has all four corners on the circle, like this one.",
        show(f2qdef['line'], 'like this one')),
      L("If even one corner is inside the circle, or outside it, it's not inscribed. A corner at the center doesn't count "
        "either, because the center is not on the circle.", show(f2qdef['in'], 'If even one corner'),
        show(f2qdef['ctr'], 'A corner at the center'))),
    S('Opposite angles: 180°',
      L("In an inscribed quadrilateral, opposite angles add up to a hundred eighty. So if angle A is seventy-five, the "
        "angle opposite it, C, is a hundred eighty minus seventy-five, a hundred five. The same for B and D.",
        show(f2quad['line'], 'In an inscribed quadrilateral'), show(f2quad['ac'], 'So if angle A is seventy-five'))),
    S('Why: 2α + 2β = 360°',
      L("Let's prove it. Call angle A alpha, and angle C beta. We draw two radii, to B and to D.",
        show(f2qwhy['line'], 'Call angle A alpha'), show(f2qwhy['rad'], 'We draw two radii')),
      L("The central angle on the arc through C is two alpha, because angle A intercepts that arc and is half of it. In "
        "the same way, the central angle on the other side is two beta.", show(f2qwhy['a'], 'The central angle on the arc'),
        show(f2qwhy['b'], 'In the same way')),
      L("Together they make a full circle, so two alpha plus two beta is three hundred sixty. Divide by two, and alpha plus "
        "beta is a hundred eighty.", show(f2qwhy['sum'], 'Together they make'))),
    S('Equal chords, equal arcs',
      L("Two more facts, about chords. In the same circle, equal chords cut off equal arcs and have equal central angles. "
        "Why? Join each chord's ends to the center. Both triangles have two radii and the same chord, so they're the same "
        "triangle, and the angles at O are equal.", show(f2chord['line'], 'In the same circle'),
        show(f2chord['rad'], 'Join each chord'), show(f2chord['ang'], 'and the angles at O')),
      L("So if angle A O B is seventy, angle C O D is seventy too, and the arcs are equal. An inscribed "
        "angle on either arc is half of seventy, thirty-five. It works backwards too, but only "
        "in the same circle.", show(f2chord['arcs'], 'and the arcs are equal'), show(f2chord['trap'], 'but only'))),
    S('Perpendicular to a chord',
      L("And a line from the center that is perpendicular to a chord cuts the chord in half. A chord of fourteen gives "
        "seven and seven. And this line, O M, is also the distance of the chord from the center.", show(f2perp['line'], 'And a line from the center'), show(f2perp['perp'], 'is perpendicular'),
        show(f2perp['half'], 'A chord of fourteen')),
      L("Why? O A and O B are radii, so triangle O A B is isosceles, and its height cuts the base in half.",
        show(f2perp['why'], 'O A and O B are radii'))),
    S('One rule behind it all',
      L("So, one main rule. An inscribed angle is half of the central angle on the same arc. From it, inscribed angles on "
        "the same arc are equal, an angle on a diameter is ninety, and opposite angles in an inscribed quadrilateral add "
        "up to a hundred eighty.", show(f2s1, 'An inscribed angle is half'), show(f2s2, 'inscribed angles on'),
        show(f2s3, 'an angle on a diameter'), show(f2s4, 'and opposite angles')),
      L("And for chords, equal chords cut off equal arcs, and a perpendicular from the center cuts a chord in half. Learn "
        "these by heart. [pause] Okay. I'll see you in the next video.", show(f2s5, 'equal chords cut off'),
        show(f2s6, 'and a perpendicular from the center'))),
])


# ================================================================================================ solve-geo33-g076
# Hebrew (geo 3567-3600, the lesson's sample question; AOC = 90 -> 135 there, 104 -> 128 here): "we just learned the
# inscribed quadrilateral, but AOCB is NOT inscribed: O is not on the circle", "you can see it with your eye" (much more
# than 90); way 1: draw an inscribed angle (D) on the same arc as O -> half (52), ABCD is inscribed -> 180 - 52; way 2
# ("a bit hard to see"): the angle completing 104 to 360 is 256, also a central angle, "wide open"; stand inside the angle
# at B, the walls: you see the long arc -> half of 256.
# Kept from the English video: the trap choice 76 named; the radii route (two isosceles triangles, 2(x + y) = 256).
# V3: the question's copy on the right; the trap: O ringed red with "not on the circle", 76 crossed; way 1: D on the long
# arc, DA and DC dashed teal, 52 at D, ABCD tinted, 128 at B; way 2 (fresh copy): the reflex angle at O as an orange wedge
# with 256, the long arc thick orange, the walls BA and BC traced; way 3 (fresh copy): OB dashed, the two isosceles
# triangles tinted teal / orange with alpha, alpha, beta, beta.
_gO, _gr = (320.0, 180.0), 109.5
_gA, _gB, _gC = (422.896, 142.549), (346.490, 73.753), (246.730, 98.626)
_gD = f2_on(_gO, _gr, 262)
f2g76_q = ([('circ', _gO[0], _gO[1], _gr, 'ink', 2.5), f2_dot(_gO), ('txt', 305, 195, 'O', 'ink', 22, True),
            f2_seg(_gA, _gB, 'ink', 2.5), f2_seg(_gB, _gC, 'ink', 2.5), f2_seg(_gC, _gA, 'ink', 2.5),
            f2_seg(_gO, _gA, 'ink', 2.5), f2_seg(_gO, _gC, 'ink', 2.5),
            ('txt', 440.751, 136.05, 'A', 'ink', 22, True), ('txt', 351.087, 55.317, 'B', 'ink', 22, True),
            ('txt', 234.017, 84.506, 'C', 'ink', 22, True),
            f2_ang(_gO, _gA, _gC, 25.55, 'orange', '104°', 44), f2_ang(_gB, _gA, _gC, 18.25, 'teal', 'x', 34)])
_gvb = '190 30 290 400'
f2g76t = PIN(GEO('f2g76t', [
    ('line', f2g76_q),
    ('o', [('circ', _gO[0], _gO[1], 13, 'red', 3), ('txt', 330, 335, 'O is not on the circle', 'red', 22)]),
    ('t76', [('txt', 330, 366, '180° − 104° = 76° ✗', 'red', 22)]),
], vb=_gvb, w=360, title='The circle with center O'))
_R(f2g76t, 230)
f2g76 = PIN(GEO('f2g76', [
    ('line', f2g76_q),
    ('d', [f2_dot(_gD), ('txt', _gD[0] - 2, _gD[1] + 20, 'D', 'ink', 22, True), f2_seg(_gD, _gA, 'teal', 2.5, True),
           f2_seg(_gD, _gC, 'teal', 2.5, True)]),
    ('d52', [f2_ang(_gD, _gA, _gC, 30, 'teal', '52°', 50)]),
    ('quad', [('tint', [_gA, _gB, _gC, _gD], 'teal')]),
    ('x', [('txt', 330, 393, 'x = 180° − 52° = 128°', 'teal', 22)]),
], vb=_gvb, w=360, title='The circle with center O'))
_R(f2g76, 230)

f2g76b = PIN(GEO('f2g76b', [
    ('line', f2g76_q),
    ('ref', [('wedge', _gO[0], _gO[1], 40, 132, 20, 'orange'), ('arc', _gO[0], _gO[1], 40, 132, 20, 'orange', '256°', 62),
             ('txt', 330, 340, '360° − 104° = 256°', 'orange', 22)]),
    ('long', [('arcw', _gO[0], _gO[1], _gr, 132, 20, 'orange', 8)]),
    ('walls', [f2_seg(_gB, _gA, 'teal', 6), f2_seg(_gB, _gC, 'teal', 6)]),
    ('x', [('txt', 330, 372, 'x = 256° ÷ 2 = 128°', 'teal', 22)]),
], vb=_gvb, w=360, title='The big central angle'))
_R(f2g76b, 230)

# the enlarged cut-out of the two triangles sits to the right of the circle in the same figure (same labels, same tints)
_zk = 1.5
_zT = lambda P: (500.0 + (P[0] - 247.0) * _zk, 112.0 + (P[1] - 74.0) * _zk)
_zO, _zA, _zB, _zC = _zT(_gO), _zT(_gA), _zT(_gB), _zT(_gC)
f2g76c = PIN(GEO('f2g76c', [
    ('line', f2g76_q),
    ('ob', [f2_seg(_gO, _gB, 'teal', 2.5, True), ('tick', _gO[0], _gO[1], _gA[0], _gA[1], 1), ('tick', _gO[0], _gO[1], _gB[0], _gB[1], 1),
            ('tick', _gO[0], _gO[1], _gC[0], _gC[1], 1)]),
    ('tri', [('tint', [_gO, _gA, _gB], 'teal'), ('tint', [_gO, _gB, _gC], 'orange'), f2_seg(_gO, _gA, 'teal', 3),
             f2_seg(_gA, _gB, 'teal', 3), f2_seg(_gB, _gC, 'orange', 3), f2_seg(_gC, _gO, 'orange', 3)]),
    ('zoom', [('arcw', _zO[0], _zO[1], _gr * _zk, 14, 138, 'ink', 2), f2_seg(_zA, _zB), f2_seg(_zB, _zC), f2_seg(_zO, _zA), f2_seg(_zO, _zC),
              f2_seg(_zO, _zB, 'teal', 3, True), ('tint', [_zO, _zA, _zB], 'teal'), ('tint', [_zO, _zB, _zC], 'orange'),
              ('txt', _zA[0] + 14, _zA[1] - 4, 'A', 'ink', 22, True), ('txt', _zB[0] + 4, _zB[1] - 20, 'B', 'ink', 22, True),
              ('txt', _zC[0] - 4, _zC[1] - 20, 'C', 'ink', 22, True), ('txt', _zO[0] - 18, _zO[1] + 8, 'O', 'ink', 22, True),
              ('txt', _zO[0] + 10, _zO[1] - 34, '104°', 'orange', 18)]),
    ('ab', [f2_wedge(_zA, _zO, _zB, 30, 'teal'), f2_albl(_zA, _zO, _zB, 46, 'α', 'teal', 22),
            f2_wedge(_zB, _zA, _zO, 30, 'teal'), f2_albl(_zB, _zA, _zO, 44, 'α', 'teal', 22),
            f2_wedge(_zB, _zO, _zC, 30, 'orange'), f2_albl(_zB, _zO, _zC, 44, 'β', 'orange', 22),
            f2_wedge(_zC, _zB, _zO, 30, 'orange'), f2_albl(_zC, _zB, _zO, 46, 'β', 'orange', 22),
            ('txt', 496, 322, 'x = α + β', 'ink', 24)]),
    ('o', [('txt', 496, 354, '(180° − 2α) + (180° − 2β) = 104°', 'ink', 23)]),
    ('x', [('txt', 496, 388, '2(α + β) = 256°,  α + β = 128°', 'teal', 23)]),
], vb='200 36 592 368', w=540, title='Two isosceles triangles'))
_R(f2g76c, 185)

video('solve-geo33-g076', 'solution', qid='geo33-g076', slides=[
    S('Not an inscribed quadrilateral',
      L("A, B and C lie on a circle with center O, and B is on the short arc A C. Angle A O C is one hundred four degrees. "
        "What is angle A B C?", pt('stem', 'A, B and C lie on a circle', 'hl', 8.0), voice='calm', pause=0.5),
      L("So we want the angle at B, marked x, and the only angle we know is the central angle at O. [short pause] We just "
        "learned about quadrilaterals in a circle, and A O C B looks like one. But careful. For a quadrilateral to be "
        "inscribed, all four corners must be on the circle.", show(f2g76t['line'], 'So we want the angle at B')),
      L("O is the center, so it's not on the circle. So A O C B is not an inscribed quadrilateral, and we can't say that "
        "its opposite angles add up to one hundred eighty.", show(f2g76t['o'], 'O is the center')),
      L("And that's exactly the trap. One hundred eighty minus one hundred four is seventy-six, and seventy-six is in the "
        "choices. Cross it out. You can see it in the figure too. The angle at B is much bigger than ninety, so it can't be "
        "seventy-six.", show(f2g76t['t76'], 'One hundred eighty minus one hundred four'),
        mk('cross', 'choice 3', 'Cross it out')),
      L("We'll solve it in two ways, and then I'll show you one more route.")),
    SM('Method 1 · The math way', 'An inscribed angle on the same arc',
      L("[pause] Let's start with the main rule. An inscribed angle is half of the central angle on the same arc. The one "
        "hundred four at O intercepts the short arc A C, the arc that B sits on. So let's draw an inscribed angle on that "
        "same arc. We take a point D on the other side, on the long arc, and join it to A and to C.",
        show(f2g76['line'], 'the central angle on the same arc'), show(f2g76['d'], 'We take a point D')),
      L("Angle A D C intercepts the same arc as the one hundred four. So it's half of it. Half of one hundred four is "
        "fifty-two.", show(f2g76['d52'], 'So it\'s half of it')),
      L("Now look at A B C D. All four corners are on the circle, so this time it really is an inscribed quadrilateral. "
        "Angles B and D are opposite, so they add up to one hundred eighty.", show(f2g76['quad'], 'Now look at A B C D')),
      L("So x is one hundred eighty minus fifty-two, which is one hundred twenty-eight. Choice number two is our answer.",
        show(f2g76['x'], 'So x is one hundred eighty'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("In the exam you'd mark it and move on. Here, let's see where the other choices come from. Fifty-two is angle D, "
        "not angle B. And one hundred four is the central angle itself.", mk('cross', 'choice 1', 'Fifty-two is angle D'),
        mk('cross', 'choice 4', 'one hundred four is the central angle itself'))),
    SM('Method 2 · The math way: the big central angle', 'The big central angle',
      L("[pause] Now another way, with the big central angle. It's not hard to understand, but some students find it hard to see.",
        show(f2g76b['line'], 'Now another way')),
      L("The angle at O is one hundred four. The angle that completes it to a full circle, three hundred sixty, is three "
        "hundred sixty minus one hundred four. That's two hundred fifty-six.", show(f2g76b['ref'], 'The angle that completes it')),
      L("This two hundred fifty-six is also a central angle. It's very big and wide open, but its vertex is at the center, "
        "and it's between two radii. It intercepts the long arc, all the way around from A to C.",
        show(f2g76b['long'], 'It intercepts the long arc')),
      L("Now stand at B. The chords B A and B C are your walls. What part of the circle do you see? The long arc, the same "
        "one. So angle A B C is the inscribed angle on the long arc.", show(f2g76b['walls'], 'Now stand at B')),
      L("So it's half of two hundred fifty-six. Half of two hundred is one hundred, and half of fifty-six is twenty-eight. "
        "Together, one hundred twenty-eight. Choice number two again.", show(f2g76b['x'], "So it's half of two hundred"),
        mk('tick', 'choice 2', 'Choice number two again'))),
    SM('Method 3 · The math way: radii', 'Two isosceles triangles',
      L("[pause] And one more route, step by step, just so you've seen it. Draw the radius O B. Now O A, O B and O C are all "
        "radii, so they're equal.", show(f2g76c['line'], 'And one more route'), show(f2g76c['ob'], 'Draw the radius O B')),
      L("So we get two isosceles triangles, A O B and B O C. Here they are, bigger. In triangle A O B, the base angles are "
        "equal. Call them alpha. In triangle B O C, call them beta. Angle A B C is made of both, so x is alpha plus beta.",
        show(f2g76c['tri'], 'So we get two isosceles'), show(f2g76c['zoom'], 'Here they are, bigger'),
        show(f2g76c['ab'], 'In triangle A O B, the base')),
      L("The angles of a triangle add up to one hundred eighty. So the angle at O in the first triangle is one hundred "
        "eighty minus two alpha, and in the second, one hundred eighty minus two beta. Together, they make the one hundred "
        "four.", show(f2g76c['o'], 'Together, they make')),
      L("So three hundred sixty, minus two alpha, minus two beta, is one hundred four. Then two alpha plus two beta is "
        "three hundred sixty minus one hundred four, which is two hundred fifty-six. And alpha plus beta is half of that, "
        "one hundred twenty-eight. Choice number two once more. [pause] Okay. I'll see you in the next question.",
        show(f2g76c['x'], 'Then two alpha plus two beta'), mk('tick', 'choice 2', 'Choice number two once more'))),
])


# ================================================================================================ solve-q-r26-t33-01
# Course addition (no Hebrew source): a chord and its distance from the center -> the radius -> the circumference.
# Methods: the distance is the perpendicular; the perpendicular from the center halves the chord (taught in geo-075);
# the radius to the end of the chord; Pythagoras / the triple 3-4-5 doubled; C = 2 pi r. Every wrong choice explained
# (100 pi the area, 10 pi ten as the diameter, 16 pi the chord taken as a diameter).
# V3: the copy; OM dashed teal after its ends are named, the right angle at M, 6 on OM; ticks and 8 | 8; OB dashed (ends
# named first) with r; triangle OMB tinted orange and shown again enlarged with 6, 8, r; the results under the figure.
_qO, _qr = (320.0, 180.0), 109.5
_qA, _qB, _qM = (232.549, 245.899), (407.451, 245.899), (320.0, 245.899)
f2q1_q = [('circ', _qO[0], _qO[1], _qr, 'ink', 2.5), f2_seg(_qA, _qB, 'ink', 2.5), f2_dot(_qO),
          ('txt', 217.375, 257.333, 'A', 'ink', 22, True), ('txt', 422.625, 257.333, 'B', 'ink', 22, True),
          ('txt', 320, 162, 'O', 'ink', 22, True), ('txt', 320, 265.899, '16', 'ink', 20)]
# the enlarged cut-out of triangle OMB (scale 1.5), to the right of the circle, with the same labels and tint
_k = 1.5
_cM = (490.0, 256.0); _cO = (_cM[0], _cM[1] - 65.899 * _k); _cB = (_cM[0] + 87.451 * _k, _cM[1])
f2q1 = PIN(GEO('f2q1', [
    ('line', f2q1_q),
    ('around', [('arcw', _qO[0], _qO[1], _qr, 0, 359.9, 'teal', 6), ('txt', 440, 70, 'C = 2πr', 'teal', 26)]),
    ('om', [f2_seg(_qO, _qM, 'teal', 2.5, True), f2_right(_qM, _qO, _qB, 10), ('txt', 307, 234, 'M', 'ink', 20, True),
            ('txt', 332, 208, '6', 'teal', 22)]),
    ('half', [('tick', _qA[0], _qA[1], _qM[0], _qM[1], 1), ('tick', _qM[0], _qM[1], _qB[0], _qB[1], 1),
              ('txt', 276, 268, '8', 'teal', 22), ('txt', 364, 268, '8', 'teal', 22)]),
    ('ob', [f2_seg(_qO, _qB, 'orange', 3, True), ('txt', 376, 200, 'r', 'orange', 24, True)]),
    ('tri', [('tint', [_qO, _qM, _qB], 'orange'),
             ('tint', [_cO, _cM, _cB], 'orange'), f2_seg(_cO, _cM, 'teal', 3), f2_seg(_cM, _cB, 'teal', 3), f2_seg(_cO, _cB, 'orange', 4),
             f2_right(_cM, _cO, _cB, 12), ('txt', _cO[0] - 14, _cO[1] - 6, 'O', 'ink', 20, True),
             ('txt', _cM[0] - 14, _cM[1] + 14, 'M', 'ink', 20, True), ('txt', _cB[0] + 14, _cB[1] + 6, 'B', 'ink', 20, True),
             ('txt', _cM[0] - 14, _cM[1] - 43, '6', 'teal', 22), ('txt', _cM[0] + 57, _cM[1] + 18, '8', 'teal', 22),
             ('txt', _cM[0] + 68, _cM[1] - 54, 'r', 'orange', 24, True)]),
    ('pyth', [('txt', 440, 330, 'r² = 6² + 8² = 100,  r = 10', 'orange', 24)]),
    ('c', [('txt', 440, 366, 'C = 2π · 10 = 20π', 'red', 26)]),
], vb='200 40 470 345', w=540, title='Chord AB of the circle with center O'))
_R(f2q1, 230)

video('solve-q-r26-t33-01', 'solution', qid='q-r26-t33-01', slides=[
    S('Draw the distance',
      L("Chord A B of a circle with center O is sixteen centimeters long. The distance from O to A B is six centimeters. "
        "What is the circumference of the circle, in centimeters?", pt('stem', 'Chord A B of a circle', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("They ask for the circumference. That's the length all the way around the circle. Its formula is two times pi "
        "times r, where r is the radius. Pi is a fixed number, a bit more than three, and there's a lesson on it soon. So "
        "really, they're asking for the radius.", show(f2q1['line'], 'They ask for the circumference'),
        show(f2q1['around'], 'the length all the way around')),
      L("[short pause] We have a chord and its distance from the center, so one helper line will connect them."),
      L("[short pause] First, what is the distance from a point to a line? It's the shortest way, and that's the "
        "perpendicular. So from O we draw a line down to the chord, at ninety degrees. Call its foot M. O M is six.",
        show(f2q1['om'], 'So from O we draw a line')),
      L("We learned that a perpendicular from the center cuts the chord in half. Sixteen divided by two is eight, so A M is "
        "eight, and M B is eight.", show(f2q1['half'], 'Sixteen divided by two')),
      L("Now the radius. We draw it from the center O to the end of the chord, B. O B is a radius, so it's r.",
        show(f2q1['ob'], 'We draw it from the center O')),
      L("[short pause] Look at triangle O M B. It has a right angle at M, its legs are six and eight, and the radius is its "
        "hypotenuse. Here it is, bigger.", show(f2q1['tri'], 'Look at triangle O M B')),
      L("By Pythagoras, r squared is six squared plus eight squared. Thirty-six plus sixty-four is one hundred, so r squared "
        "is one hundred, and r is ten. You can also spot the triple. Six, eight, ten is three, four, five, doubled.",
        show(f2q1['pyth'], 'By Pythagoras')),
      L("So the circumference is two pi times ten, which is twenty pi. Choice number three is our answer.",
        show(f2q1['c'], 'So the circumference is'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("In the exam you'd mark it and move on. Here, let's see where the other choices come from. One hundred pi is pi r "
        "squared. That's the area, the inside of the circle, and we'll meet it in that lesson too. Ten pi is what you get if you take ten as the diameter. And sixteen pi "
        "comes from taking the chord as a diameter. But this chord doesn't pass through the center, so it's not a diameter. "
        "[pause] Okay. I'll see you in the next question.", mk('cross', 'choice 4', 'One hundred pi is pi r'),
        mk('cross', 'choice 2', 'Ten pi is what you get'), mk('cross', 'choice 1', 'And sixteen pi comes'))),
])

# =================================================================================================================
# Topic 33 fragment f3 (TAG C, 2026-10-14): tangents and area / circumference. geo-077 (lesson: Tangents), g078,
# q-r26-t33-02 (added), geo-079 (lesson: Area and Circumference), g080, q-r26-t33-03 (added). Hebrew: geo 3611-3735.
# Written to the guide (R1-R36, clarity style, Codex review standard, V3). Every GEO figure is PIN-ned.
# =================================================================================================================
import math as _f3m

FIG_LEFT.update({'solve-geo33-g078', 'solve-q-r26-t33-02'})


def f3_ang(P, Q, R, r, col, label=None, lr=None):
    """the smaller angle at P between the rays P->Q and P->R"""
    a, b = gdir(*P, *Q), gdir(*P, *R)
    if (b - a) % 360 > 180: a, b = b, a
    e = ('arc', P[0], P[1], r, a, b, col)
    if label: e = e + (label,) + ((lr,) if lr else ())
    return e


def f3_rt(P, Q, R, sz=14, col='teal'):
    """the right-angle square at P between the rays P->Q and P->R"""
    a, b = gdir(*P, *Q), gdir(*P, *R)
    if (b - a) % 360 > 180: a, b = b, a
    return ('right', P[0], P[1], a, b, sz, col)


def f3_along(P, deg, L):
    return gpt(P[0], P[1], L, deg)


# ================================================================================================ geo-077 (lesson: Tangents)
# Hebrew (geo 3611-3654): a tangent is a straight line that just brushes the circle, at one point; a little further in it
# cuts the circle at two points and the inside part is a chord; further out it doesn't touch at all; the point of
# tangency. The radius is perpendicular to the tangent at the point of tangency - "a very, very important rule", very
# common in the exam - "every time you see tangents, without thinking too much: draw the radius to the point of
# tangency". Two tangents from the same point are equal, and with the radii they make a kite (two pairs of equal sides).
# The closing summary of the two rules. Added (R4-R6): numbers for each rule - r 5, OP 13 -> the tangent 12 (Pythagoras,
# the triple 5, 12, 13); the second tangent is 12 too, which is also the why (both right triangles share OP and r); a
# second number example 9 -> 9; the kite's line of symmetry OP (reminder from the kite lesson, used in g078's route 2).
# V3: the three lines (1 point, 2 points, 0 points) on one circle, each written as it is named; the rule on a clean
# circle, then two more tangents at other places (general); the number example: radius dashed, the right angle, the right
# triangle tinted, the values written as found; the two-tangent figure keeps 5 and 12 written; the second triangle in
# the other tint; equal ticks; OP dashed as the fold line.
f3_O1 = (230, 200)
f3t1 = PIN(GEO('f3t1', [
    ('line', [('circ', 230, 200, 110), ('dot', 230, 200, 'O', -18, 20)]),
    ('tan', [('seg', 60, 90, 400, 90, 'teal', 4), ('dot', 230, 90), ('txt', 500, 90, '1 point: tangent', 'teal', 24)]),
    ('sec', [('seg', 60, 150, 400, 150, 'ink', 2.5), ('seg', 132.0, 150, 328.0, 150, 'orange', 6), ('dot', 132.0, 150), ('dot', 328.0, 150),
             ('txt', 500, 150, '2 points', 'orange', 24), ('txt', 230, 172, 'chord', 'orange', 22)]),
    ('out', [('seg', 60, 35, 400, 35, 'ink', 2.5), ('txt', 500, 35, '0 points', 'ink', 24)]),
    ('pt', [('txt', 252, 112, 'D', 'ink', 26, True), ('txt', 230, 345, 'D: the point of tangency', 'teal', 24)]),
], vb='40 10 560 350', w=560, col=0, title='A tangent, a line that cuts the circle, and a line outside it'))
f3k1 = I('f3k1', 'Tangent: touches the circle at one point', size=28, col=0)

# ---- the rule: radius perpendicular to the tangent, then two more places on the circle
f3_O2, f3_r2 = (260, 190), 120


def f3_tanat(deg, L=130, col='ink'):
    D = gpt(f3_O2[0], f3_O2[1], f3_r2, deg)
    a, b = f3_along(D, deg + 90, L), f3_along(D, deg - 90, L)
    return D, [('seg', a[0], a[1], b[0], b[1], col, 3)]


f3_D2, f3_tl2 = f3_tanat(60)
f3_D2b, f3_tl2b = f3_tanat(200, 110)
f3_D2c, f3_tl2c = f3_tanat(300, 110)
f3t2 = PIN(GEO('f3t2', [
    ('line', [('circ', f3_O2[0], f3_O2[1], f3_r2), ('dot', f3_O2[0], f3_O2[1], 'O', -18, 4)] + f3_tl2
             + [('dot', *f3_D2), ('txt', f3_D2[0] + 16, f3_D2[1] - 22, 'D', 'ink', 26, True)]),
    ('rad', [('seg', f3_O2[0], f3_O2[1], f3_D2[0], f3_D2[1], 'teal', 3, True), ('right', f3_D2[0], f3_D2[1], 150, 240, 16, 'teal')]),
    ('more', f3_tl2b + f3_tl2c + [('seg', f3_O2[0], f3_O2[1], f3_D2b[0], f3_D2b[1], 'teal', 3, True), ('right', f3_D2b[0], f3_D2b[1], 20, 290, 16, 'teal'),
              ('seg', f3_O2[0], f3_O2[1], f3_D2c[0], f3_D2c[1], 'teal', 3, True), ('right', f3_D2c[0], f3_D2c[1], 30, 120, 16, 'teal'),
              ('dot', *f3_D2b), ('dot', *f3_D2c)]),
], vb='60 0 440 380', w=520, col=0, title='The radius to the point of tangency is perpendicular to the tangent'))
f3k2 = I('f3k2', 'Radius to the point of tangency $\\perp$ tangent', size=28, col=1)
f3k3 = I('f3k3', 'See a tangent $\\to$ draw that radius', size=28, col=1)

# ---- in numbers: r = 5, OP = 13 -> PD = 12 (16 px per unit)
f3_O3 = (170, 190); f3_u = 16
f3_P3 = (170 + 13 * f3_u, 190)
f3_th = _f3m.degrees(_f3m.acos(5 / 13.0))
f3_D3 = gpt(f3_O3[0], f3_O3[1], 5 * f3_u, f3_th)
f3_E3 = gpt(f3_O3[0], f3_O3[1], 5 * f3_u, -f3_th)
f3_base3 = [('circ', f3_O3[0], f3_O3[1], 5 * f3_u), ('dot', f3_O3[0], f3_O3[1], 'O', -20, 4),
            ('seg', f3_P3[0], f3_P3[1], f3_D3[0], f3_D3[1], 'ink', 3), ('dot', *f3_P3), ('txt', f3_P3[0] + 22, f3_P3[1], 'P', 'ink', 26, True),
            ('dot', *f3_D3), ('txt', f3_D3[0] - 4, f3_D3[1] - 24, 'D', 'ink', 26, True)]
f3_mPD = ((f3_P3[0] + f3_D3[0]) / 2.0, (f3_P3[1] + f3_D3[1]) / 2.0)
f3t3 = PIN(GEO('f3t3', [
    ('line', f3_base3),
    ('rad', [('seg', f3_O3[0], f3_O3[1], f3_D3[0], f3_D3[1], 'teal', 3, True), f3_rt(f3_D3, f3_O3, f3_P3, 14),
             ('txt', 168, 150, '5', 'teal', 26)]),
    ('op', [('seg', f3_O3[0], f3_O3[1], f3_P3[0], f3_P3[1], 'teal', 3, True), ('txt', 280, 212, '13', 'teal', 26)]),
    ('tri', [('tint', [f3_O3, f3_D3, f3_P3], 'teal')]),
    ('pd', [('txt', f3_mPD[0] + 14, f3_mPD[1] - 22, '12', 'orange', 28)]),
], vb='60 70 400 215', w=600, col=0, title='A tangent from P, with the radius to D'))
f3k4 = IH('f3k4', '$5^2+PD^2=13^2$', size=30, col=1)
f3k5 = IH('f3k5', '$25+PD^2=169$, $\\ PD^2=144$, $\\ PD=12$', size=30, col=1)
f3k6 = I('f3k6', 'The triple $5,\\ 12,\\ 13$', size=28, col=1)

# ---- two tangents from P: equal, and a kite
f3_mPE = ((f3_P3[0] + f3_E3[0]) / 2.0, (f3_P3[1] + f3_E3[1]) / 2.0)
f3t4 = PIN(GEO('f3t4', [
    ('line', f3_base3 + [('seg', f3_O3[0], f3_O3[1], f3_D3[0], f3_D3[1], 'ink', 3), f3_rt(f3_D3, f3_O3, f3_P3, 14, 'ink'),
                         ('txt', 168, 150, '5', 'ink', 24), ('txt', f3_mPD[0] + 14, f3_mPD[1] - 22, '12', 'ink', 26),
                         ('seg', f3_P3[0], f3_P3[1], f3_E3[0], f3_E3[1], 'ink', 3), ('dot', *f3_E3),
                         ('txt', f3_E3[0] - 4, f3_E3[1] + 26, 'E', 'ink', 26, True)]),
    ('tri1', [('tint', [f3_O3, f3_D3, f3_P3], 'teal'), ('seg', f3_O3[0], f3_O3[1], f3_P3[0], f3_P3[1], 'ink', 2, True)]),
    ('tri2', [('seg', f3_O3[0], f3_O3[1], f3_E3[0], f3_E3[1], 'teal', 3, True), f3_rt(f3_E3, f3_O3, f3_P3, 14),
              ('tint', [f3_O3, f3_E3, f3_P3], 'orange'), ('txt', 168, 230, '5', 'orange', 24)]),
    ('pe', [('txt', f3_mPE[0] + 14, f3_mPE[1] + 24, '12', 'orange', 28), ('tick', f3_P3[0], f3_P3[1], f3_D3[0], f3_D3[1], 2),
            ('tick', f3_P3[0], f3_P3[1], f3_E3[0], f3_E3[1], 2)]),
    ('kite', [('tick', f3_O3[0], f3_O3[1], f3_D3[0], f3_D3[1], 1), ('tick', f3_O3[0], f3_O3[1], f3_E3[0], f3_E3[1], 1),
              ('txt', 290, 322, 'a kite: 5, 5, 12, 12', 'teal', 24)]),
    ('sym', [('seg', f3_O3[0], f3_O3[1], f3_P3[0], f3_P3[1], 'teal', 4, True),
             f3_ang(f3_P3, f3_D3, f3_O3, 46, 'teal'), f3_ang(f3_P3, f3_O3, f3_E3, 52, 'teal'),
             ('txt', 290, 50, 'OP: the line of symmetry', 'teal', 22)]),
], vb='60 30 400 310', w=560, col=0, title='Two tangents from P'))
f3k7 = I('f3k7', '$PD=PE$', size=32, col=1)
f3k8 = I('f3k8', '$PD=9\\ \\to\\ PE=9$', size=30, col=1)
f3k9 = I('f3k9', '1. Radius to the point of tangency $\\perp$ tangent: draw it', size=30, col=0)
f3k10 = I('f3k10', '2. Two tangents from one point are equal: a kite', size=30, col=0)

video('geo-077', 'lesson', slides=[
    S('Tangents',
      L("Tangents to a circle. It's a short lesson, but its two rules come up in the exam all the time.")),
    S('Touches at one point',
      L("A tangent is a straight line that just brushes past the circle. It touches the circle at one point only.",
        show(f3t1['line'], 'A tangent is a straight line'), show(f3t1['tan'], 'It touches the circle at one point'),
        show(f3k1, 'at one point only')),
      L("If the line were a little further in, it would go through the circle and cut it at two points. Then the part "
        "inside the circle would be a chord.", show(f3t1['sec'], 'a little further in'), pt('f3t1_sec', 'Then the part inside')),
      L("And if the line passed outside, it wouldn't touch the circle at all. It's just a line.",
        show(f3t1['out'], 'And if the line passed outside')),
      L("So our tangent only brushes the circle, at one point. This point is called the point of tangency.",
        show(f3t1['pt'], 'This point is called'))),
    S('Radius ⊥ tangent',
      L("Now a very, very important rule. The radius is perpendicular to the tangent at the point of tangency.",
        show(f3t2['line'], 'Now a very, very important rule')),
      L("Here the tangent touches the circle at D. When I draw a radius to the point of tangency, from O to D, I get a "
        "ninety-degree angle between the radius and the tangent.", show(f3t2['rad'], 'from O to D'), show(f3k2, 'a ninety-degree angle')),
      L("It doesn't matter where the tangent touches. Here, and here, the radius to the point of tangency is always "
        "perpendicular to the tangent.", show(f3t2['more'], "It doesn't matter where")),
      L("This rule is used very often in the exam. So every time you see a circle question with tangents, don't think too "
        "much. Draw the radius to the point of tangency, and you get a right angle.", show(f3k3, 'Draw the radius to the point'))),
    S('A tangent in numbers',
      L("Let's see it in numbers. The radius of this circle is five, and P is thirteen away from the center. P D is a tangent. "
        "How long is it?", show(f3t3['line'], "Let's see it in numbers")),
      L("A tangent, so I draw the radius to the point of tangency, O D. It's five, and the angle at D is ninety. Now join O "
        "to P. That's thirteen.", show(f3t3['rad'], 'so I draw the radius'), show(f3t3['op'], 'Now join O to P')),
      L("So O D P is a right triangle, and thirteen is its hypotenuse, because it's across from the right angle. By "
        "Pythagoras, five squared plus P D squared is thirteen squared.", show(f3t3['tri'], 'So O D P is a right triangle'),
        show(f3k4, 'By Pythagoras')),
      L("Twenty-five plus P D squared is a hundred sixty-nine. So P D squared is a hundred sixty-nine minus twenty-five, "
        "which is a hundred forty-four, and P D is twelve.", show(f3k5, 'Twenty-five plus'), show(f3t3['pd'], 'and P D is twelve')),
      L("Or, faster, five and thirteen should remind you of the triple five, twelve, thirteen.", show(f3k6, 'the triple five'))),
    S('Two tangents from one point',
      L("From the same point P, we can draw a second tangent to the circle, on the other side. It touches the circle at E.",
        show(f3t4['line'], 'From the same point P')),
      L("The second rule. Two tangents that come out of the same point are equal to each other. Why? Look at the two right "
        "triangles. The first one is O D P.", show(f3t4['tri1'], 'Look at the two right triangles')),
      L("The second one is O E P. Its radius O E is also five, and it has the same hypotenuse, O P, thirteen. So Pythagoras "
        "gives the same thing, and P E is twelve too.", show(f3t4['tri2'], 'The second one is O E P'),
        show(f3t4['pe'], 'and P E is twelve too'), show(f3k7, 'and P E is twelve too')),
      L("So if one tangent from P is nine, the other tangent from P is nine too, with no calculation at all.",
        show(f3k8, 'So if one tangent from P is nine')),
      L("Now look at the whole shape, O D P E. The two radii are equal, and the two tangents are equal. Two pairs of equal "
        "sides next to each other, so it's a kite, five, five, twelve, twelve.", show(f3t4['kite'], 'Two pairs of equal sides')),
      L("Remember from the kite lesson, a kite has a line of symmetry. Here it's O P. So O P cuts the angle at P into two "
        "equal halves.", show(f3t4['sym'], 'Here it\'s O P'))),
    S('Two rules',
      L("So we have two important rules for tangents. One, the radius is perpendicular to the tangent at the point of "
        "tangency. So when you see a tangent, draw the radius, and you have ninety degrees.", show(f3k9, 'One, the radius')),
      L("Two, two tangents from the same point are always equal. Now let's solve a sample question. [pause] Okay. I'll see "
        "you in the next video.", show(f3k10, 'Two, two tangents'))),
])

# ================================================================================================ geo33-g078
# Hebrew (geo 3646-3658, her 40 -> 140 -> 70; the course: 68 -> 112 -> 56): "a circle with tangents - first of all draw
# radii", 90 twice, "always, automatically, it should be a reflex" (her Pavlov line said without the name); the
# quadrilateral of D, B (P), E and the centre, its angles add up to 360; "here I already have 180, so here I need another
# 180" -> the central angle; the marked angle is an inscribed angle of that central angle -> half. Kept from the English
# script: the traps 112 (stopping at the central angle) and 34 (half of 68), and the symmetry route (OP cuts the 68 in
# half; the right triangle ODP; 56 is half of the central angle, the same as the inscribed angle).
# V3: the question figure on the left; the copy on the right: radii dashed teal with their right angles; the quadrilateral
# tinted; 112 written at O; the minor arc DE traced, then 56 at A; route 2: a fresh copy, OP dashed, 34 | 34, triangle ODP
# tinted, 56 at O.
f3G = {'O': (249.856, 180.0), 'P': (499.644, 180.0), 'D': (297.857, 81.582), 'E': (297.857, 278.418), 'A': (140.356, 180.0)}
f3_gO, f3_gP, f3_gD, f3_gE, f3_gA = f3G['O'], f3G['P'], f3G['D'], f3G['E'], f3G['A']
f3_q78 = [('circ', f3_gO[0], f3_gO[1], 109.5), ('seg', *f3_gP, *f3_gD), ('seg', *f3_gP, *f3_gE), ('seg', *f3_gA, *f3_gD), ('seg', *f3_gA, *f3_gE),
          ('dot', *f3_gO), ('txt', 236, 196, 'O', 'ink', 22, True), ('txt', 520, 180, 'P', 'ink', 24, True),
          ('txt', 298, 60, 'D', 'ink', 24, True), ('txt', 298, 302, 'E', 'ink', 24, True), ('txt', 116, 180, 'A', 'ink', 24, True),
          f3_ang(f3_gA, f3_gD, f3_gE, 30, 'ink', 'x', 50)]
f3_q78a = f3_q78 + [f3_ang(f3_gP, f3_gD, f3_gE, 44, 'ink', '68°', 72)]
f3_rad78 = [('seg', *f3_gO, *f3_gD, 'teal', 3, True), ('seg', *f3_gO, *f3_gE, 'teal', 3, True),
            f3_rt(f3_gD, f3_gO, f3_gP, 13), f3_rt(f3_gE, f3_gO, f3_gP, 13)]
f3g78 = PIN(GEO('f3g78', [
    ('line', f3_q78a),
    ('rad', f3_rad78),
    ('quad', [('tint', [f3_gO, f3_gD, f3_gP, f3_gE], 'teal'), ('txt', 320, 345, '90° + 90° + 68° + ∠O = 360°', 'ink', 22)]),
    ('o112', [f3_ang(f3_gO, f3_gD, f3_gE, 30, 'orange', '112°', 58), ('txt', 320, 377, '∠O = 180° − 68° = 112°', 'orange', 22)]),
    ('arc', [('arcw', f3_gO[0], f3_gO[1], 109.5, 296, 64, 'teal', 8)]),
    ('x56', [f3_ang(f3_gA, f3_gD, f3_gE, 30, 'teal', '56°', 80), ('txt', 320, 409, 'x = 112° ÷ 2 = 56°', 'teal', 24)]),
], vb='95 40 450 385', w=480, title='Two tangents from P, and the point A on the circle'))
f3g78b = PIN(GEO('f3g78b', [
    ('line', f3_q78 + [f3_ang(f3_gP, f3_gD, f3_gE, 44, 'ink'), ('txt', 498, 146, '68°', 'ink', 22), ('seg', *f3_gO, *f3_gD, 'ink', 2.5), ('seg', *f3_gO, *f3_gE, 'ink', 2.5),
                       f3_rt(f3_gD, f3_gO, f3_gP, 13, 'ink'), f3_rt(f3_gE, f3_gO, f3_gP, 13, 'ink')]),
    ('op', [('seg', *f3_gO, *f3_gP, 'teal', 3, True)]),
    ('half', [f3_ang(f3_gP, f3_gD, f3_gO, 64, 'teal', '34°', 118), f3_ang(f3_gP, f3_gO, f3_gE, 70, 'teal', '34°', 118)]),
    ('tri', [('tint', [f3_gO, f3_gD, f3_gP], 'orange'), ('txt', 320, 345, '∠DOP = 180° − 90° − 34° = 56°', 'orange', 22)]),
    ('o56', [f3_ang(f3_gO, f3_gD, f3_gP, 30, 'orange', '56°', 56)]),
    ('same', [('txt', 320, 377, '∠DOP = half of ∠DOE = x', 'ink', 22), ('txt', 320, 409, 'x = 56°', 'teal', 24)]),
], vb='95 40 450 385', w=480, title='The line OP cuts the kite in half'))
_R(f3g78, 200); _R(f3g78b, 200)
video('solve-geo33-g078', 'solution', qid='geo33-g078', slides=[
    SM('Method 1 · The math way', 'Radii, then half',
      L("P D and P E are tangent to the circle at D and E. A lies on the major arc D E. Given: angle D P E is sixty-eight "
        "degrees. What is angle D A E?", pt('stem', 'P D and P E are tangent', 'hl', 8.0), voice='calm', pause=0.5),
      L("We know one angle, outside the circle, and we want an angle at A, on the circle. [short pause] We'll go from P to "
        "the center, and from the center to A. There's also a second way, with symmetry.", show(f3g78['line'], 'We know one angle')),
      L("[short pause] First of all, I see a circle question with tangents, so I draw radii to the points of tangency, O D "
        "and O E. The radius is perpendicular to the tangent, so I get ninety degrees, twice.",
        show(f3g78['rad'], 'so I draw radii')),
      L("Always, automatically. It should be a reflex. You see tangents to a circle, you draw the radii, and you have "
        "ninety degrees.", pt('f3g78_rad', 'Always, automatically')),
      L("Now I have a quadrilateral, O D P E, with the center as one of its corners. The angles of a quadrilateral add up to "
        "three hundred sixty.", show(f3g78['quad'], 'Now I have a quadrilateral')),
      L("The two right angles already give a hundred eighty. So the other two angles need another hundred eighty. "
        "Sixty-eight plus the angle at O is a hundred eighty, so the central angle is a hundred eighty minus sixty-eight, "
        "which is a hundred twelve.", show(f3g78['o112'], 'so the central angle is')),
      L("Careful, a hundred twelve is in the choices, but it's the central angle, not the angle we want. We're not done yet.",
        mk('cross', 'choice 1', "it's the central angle")),
      L("Now it's very easy. Stand at A and look between the two lines, A D and A E. You see the short arc D E, the same "
        "arc the central angle sees.", show(f3g78['arc'], 'You see the short arc')),
      L("So the angle at A is an inscribed angle on the same arc as the hundred twelve. An inscribed angle is half of the "
        "central angle. Half of a hundred twelve is fifty-six. Choice number four is our answer.",
        show(f3g78['x56'], 'Half of a hundred twelve'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    SM('Method 2 · Understanding: symmetry', 'Symmetry',
      L("[pause] Now the second way, by understanding the symmetry. We start again from the radii and the right angles. O D P E is a kite, because the "
        "radii are equal and the two tangents from P are equal. So let's draw its line of symmetry, O P.",
        show(f3g78b['line'], 'We start again from the radii'), show(f3g78b['op'], "let's draw its line of symmetry")),
      L("The line of symmetry cuts the angle at P into two equal halves. Half of sixty-eight is thirty-four, and thirty-four.",
        show(f3g78b['half'], 'Half of sixty-eight')),
      L("Careful, thirty-four is in the choices too. It's half of the angle at P, and that's not angle D A E.",
        mk('cross', 'choice 2', "and that's not angle D A E")),
      L("Now look at the right triangle O D P. Its angles add up to a hundred eighty. A hundred eighty minus ninety minus "
        "thirty-four is fifty-six. So angle D O P is fifty-six.", show(f3g78b['tri'], 'Now look at the right triangle'),
        show(f3g78b['o56'], 'So angle D O P is fifty-six')),
      L("By the same symmetry, O P also cuts the central angle D O E in half. So fifty-six is half of the central angle. And "
        "the inscribed angle at A is also half of the central angle. So angle D A E is fifty-six again, choice number four. "
        "Either way, it all started with the radii to the points of tangency. [pause] Okay. I'll see you in the next "
        "question.", show(f3g78b['same'], 'O P also cuts the central angle'), mk('tick', 'choice 4', 'fifty-six again, choice number four'))),
])

# ================================================================================================ q-r26-t33-02 (added)
# No Hebrew source (a course addition). NEW at the step: a circle inscribed in a triangle touches all three sides, so each
# side is made of tangent pieces; the r-by-r square at the right angle; the shortcut (a + b - c) / 2 as the same equation
# in one line. REMINDERS: Pythagoras and the triple 8, 15, 17 (topic 31), two tangents from one point (geo-077), the
# hypotenuse is a diameter of the circle around a right triangle (geo-075, the trap 8.5).
# V3: an enlarged copy (the question's triangle is small); the hypotenuse 17 written; the two radii to the legs dashed with
# right angles and the r-by-r square tinted; the leg pieces written; the matching hypotenuse pieces in the same colours;
# the equation under the shape.
f3_qT, f3_qR, f3_qC, f3_qI = (210.0, 170.0), (210.0, 290.0), (435.0, 290.0), (255.0, 245.0)
f3_qL, f3_qB = (210.0, 245.0), (255.0, 290.0)
f3_qH = (210 + 225 * 75 / 255.0, 170 + 120 * 75 / 255.0)
f3_q02 = [('seg', *f3_qT, *f3_qR), ('seg', *f3_qR, *f3_qC), ('seg', *f3_qC, *f3_qT), ('circ', f3_qI[0], f3_qI[1], 45),
          ('right', 210, 290, 0, 90, 12, 'ink'), ('txt', 158, 245, '8', 'ink', 22), ('txt', 322, 338, '15', 'ink', 22)]
f3_pcs = [('txt', 196, 270, 'r', 'ink', 22, True), ('txt', 178, 195, '8 − r', 'orange', 20),
          ('txt', 232, 310, 'r', 'ink', 22, True), ('txt', 345, 310, '15 − r', 'teal', 20)]
f3_hpcs = [('txt', 262, 166, '8 − r', 'orange', 20), ('txt', 374, 226, '15 − r', 'teal', 20),
           ('seg', *f3_qT, *f3_qH, 'orange', 5), ('seg', *f3_qH, *f3_qC, 'teal', 5),
           ('seg', *f3_qT, *f3_qL, 'orange', 5), ('seg', *f3_qB, *f3_qC, 'teal', 5)]
f3g02 = PIN(GEO('f3g02', [
    ('line', f3_q02),
    ('hyp', [('txt', 400, 160, '64 + 225 = 289', 'ink', 20), ('txt', 400, 188, 'hypotenuse 17', 'ink', 20)]),
    ('rad', [('dot', *f3_qI), ('seg', *f3_qI, *f3_qL, 'teal', 3, True), ('seg', *f3_qI, *f3_qB, 'teal', 3, True),
             ('tint', [f3_qR, f3_qL, f3_qI, f3_qB], 'teal'), ('right', 210, 245, 270, 0, 10, 'teal'), ('right', 255, 290, 90, 180, 10, 'teal')]),
    ('pcs', f3_pcs),
    ('hpc', [('seg', *f3_qI, *f3_qH, 'teal', 3, True), ('dot', *f3_qH)] + f3_hpcs),
    ('eq1', [('txt', 300, 370, '(8 − r) + (15 − r) = 17', 'ink', 22)]),
    ('eq2', [('txt', 300, 400, '23 − 2r = 17', 'ink', 22), ('txt', 300, 430, '2r = 6,  r = 3', 'red', 24)]),
], vb='130 135 350 310', w=460, title='A circle inside a right triangle with legs 8 and 15'))
f3g02b = PIN(GEO('f3g02b', [
    ('line', f3_q02 + [('dot', *f3_qI), ('seg', *f3_qI, *f3_qL, 'ink', 2, True), ('seg', *f3_qI, *f3_qB, 'ink', 2, True),
                       ('txt', 400, 188, 'hypotenuse 17', 'ink', 20)]),
    ('short', [('txt', 300, 370, '8 + 15 − 17 = 6', 'ink', 22), ('txt', 300, 400, 'r = 6 ÷ 2 = 3', 'red', 24)]),
    ('trap', [('txt', 300, 430, '17 ÷ 2 = 8.5: the circle around', 'orange', 20)]),
], vb='130 135 350 310', w=460, title='The shortcut for a right triangle'))
_R(f3g02, 200); _R(f3g02b, 200)
video('solve-q-r26-t33-02', 'solution', qid='q-r26-t33-02', slides=[
    SM('Method 1 · The math way', 'Tangent pieces',
      L("A circle is inscribed in a right triangle whose legs are eight centimeters and fifteen centimeters. What is the "
        "radius of the circle, in centimeters?", pt('stem', 'A circle is inscribed', 'hl', 7.0), voice='calm', pause=0.5),
      L("Inscribed in the triangle means the circle sits inside it and touches all three sides. So every side of the "
        "triangle is a tangent to the circle. [short pause] We'll use the tangent rules, and at the end there's a short "
        "formula too.", show(f3g02['line'], 'touches all three sides')),
      L("[short pause] First the third side, the hypotenuse. Eight squared is sixty-four, fifteen squared is two hundred "
        "twenty-five, and together that's two hundred eighty-nine. Eight, fifteen, seventeen is a Pythagorean triple, and "
        "seventeen squared really is two hundred eighty-nine. So the hypotenuse is seventeen.", show(f3g02['hyp'], 'First the third side')),
      L("Now the tangent rule. The sides are tangents, so I draw the radii to the two legs. Each radius is perpendicular to "
        "its leg. With the right angle of the triangle, we get a little square, r by r, in the corner.",
        show(f3g02['rad'], 'so I draw the radii')),
      L("So the corner pieces of the legs are r and r. The rest of the short leg is eight minus r, and the rest of the long "
        "leg is fifteen minus r.", show(f3g02['pcs'], 'So the corner pieces')),
      L("Now the second rule. Two tangents from the same point are equal. From the top corner come two tangents, so the "
        "top piece of the hypotenuse is also eight minus r. From the bottom corner on the right, the other piece is fifteen "
        "minus r.", show(f3g02['hpc'], 'From the top corner')),
      L("These two pieces make the whole hypotenuse, seventeen. So eight minus r plus fifteen minus r is seventeen.",
        show(f3g02['eq1'], 'So eight minus r')),
      L("Eight plus fifteen is twenty-three, so twenty-three minus two r is seventeen. Then two r is twenty-three minus "
        "seventeen, which is six, and r is three. Choice number three is our answer.", show(f3g02['eq2'], 'Eight plus fifteen is twenty-three'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · The math way: a short formula', 'The shortcut',
      L("[pause] The same equation in one line gives a shortcut for a right triangle. The radius of the circle inside is "
        "leg plus leg minus the hypotenuse, over two.", show(f3g02b['line'], 'The same equation in one line')),
      L("Eight plus fifteen minus seventeen is six, and half of six is three. Careful, six is in the choices too. That's "
        "someone who forgot to divide by two.", show(f3g02b['short'], 'Eight plus fifteen minus seventeen'),
        mk('cross', 'choice 1', 'someone who forgot to divide by two')),
      L("And eight and a half is half of the hypotenuse. Remember, in a right triangle the hypotenuse is a diameter of the "
        "circle around the triangle. So eight and a half is the radius of the circle around it, not inside it. The answer is "
        "three, choice number three. [pause] Okay. I'll see you in the next question.",
        show(f3g02b['trap'], 'And eight and a half'), mk('cross', 'choice 2', 'not inside it'),
        mk('tick', 'choice 3', 'three, choice number three'))),
])

# ================================================================================================ geo-079 (lesson: Area and Circumference)
# Hebrew (geo 3655-3719): two very basic formulas, used a lot; S = pi r squared, C = 2 pi r; pi is a letter, the radius we
# know; what is pi: peel off the circumference, lay it straight, count the diameters: three and a bit -> C is a bit more
# than 6r -> 2 pi a bit more than 6 -> pi a bit more than 3; pi is a fixed number, not an unknown like x; it isn't round,
# so we write a letter (her 3.14 / 6.28 move is said with "a bit more than three", teacher 2026-10-14: no decimals);
# examples: r -> S and C ("I put 5 in place of the radius"), C -> r ("the formula backwards"), S -> r (r squared, the root,
# minus not relevant). The course's numbers: r 6 -> 36 pi, 12 pi; C 22 pi -> 11; S 121 pi -> 11. Kept from the English
# lesson: only the area has r squared (units), "keep the pi", the wheels. Added: the diameter 14 trap example (R5) and a
# comparison with "pi is a bit more than three".
# V3: the area tinted and the circumference traced, so each formula is tied to its part; the unrolled circumference as an
# orange strip with the diameters laid along it one by one and the extra bit; in the examples the values are written on the
# circle as they are found (36 pi inside, 12 pi on the edge, r = 11 on the radius).
f3a1 = PIN(GEO('f3a1', [
    ('line', [('circ', 200, 180, 120), ('dot', 200, 180, 'O', -18, 4), ('seg', 200, 180, 320, 180, 'ink', 3),
              ('txt', 260, 162, 'r', 'ink', 28, True)]),
    ('S', [('circ', 200, 180, 120, 'teal', 1, False, 'teal'), ('txt', 200, 240, 'area: inside', 'teal', 24)]),
    ('C', [('arcw', 200, 180, 120, 0, 359.9, 'orange', 8), ('txt', 200, 330, 'circumference: around', 'orange', 24)]),
], vb='40 40 330 310', w=440, col=0, title='A circle with radius r'))
f3b1 = I('f3b1', 'Area $\\ S=πr^2$', size=36, col=1)
f3b2 = I('f3b2', 'Circumference $\\ C=2πr$', size=36, col=1)
f3b3 = I('f3b3', '$S$: cm² $\\qquad C$: cm', size=30, col=1)

f3a2 = PIN(GEO('f3a2', [
    ('line', [('circ', 150, 110, 60), ('dot', 150, 110), ('seg', 90, 110, 210, 110, 'teal', 3), ('txt', 150, 92, 'd', 'teal', 24, True)]),
    ('peel', [('arcw', 150, 110, 60, 0, 359.9, 'orange', 7), ('seg', 150, 175, 150, 225, 'orange', 2, True),
              ('seg', 60, 250, 437, 250, 'orange', 7)]),
    ('d1', [('seg', 60, 272, 180, 272, 'teal', 4), ('txt', 120, 296, 'd', 'teal', 24, True)]),
    ('d2', [('seg', 180, 272, 300, 272, 'teal', 4), ('txt', 240, 296, 'd', 'teal', 24, True)]),
    ('d3', [('seg', 300, 272, 420, 272, 'teal', 4), ('txt', 360, 296, 'd', 'teal', 24, True)]),
    ('bit', [('seg', 420, 272, 437, 272, 'red', 4), ('txt', 470, 230, 'a bit', 'red', 22)]),
], vb='30 30 480 280', w=600, col=0, title='The circumference laid out straight, with diameters along it'))
f3b4 = IH('f3b4', '$C=3d+$ a bit $=6r+$ a bit', size=30, col=1)
f3b5 = I('f3b5', '$2π$: a bit more than $6$', size=30, col=1)
f3b6 = I('f3b6', '$π$: a bit more than $3$', size=34, col=1)
f3b7 = I('f3b7', '$π$ is a fixed number, not an unknown like $x$', size=28, col=0)
f3b8 = I('f3b8', '$S=πr^2$: a bit more than $3r^2$', size=30, col=0)
f3b9 = I('f3b9', 'Is $4π$ more than $12$? $\\ 4\\cdot3=12$, so yes', size=30, col=0)
f3b10 = I('f3b10', 'Answers in $π$: keep the $π$', size=30, col=0)

f3a3 = PIN(GEO('f3a3', [
    ('line', [('circ', 200, 180, 110), ('dot', 200, 180)]),
    ('r6', [('seg', 200, 180, 310, 180, 'ink', 3), ('txt', 255, 162, '6', 'ink', 28)]),
    ('S', [('circ', 200, 180, 110, 'teal', 1, False, 'teal'), ('txt', 190, 225, '36π', 'teal', 30)]),
    ('C', [('arcw', 200, 180, 110, 0, 359.9, 'orange', 7), ('txt', 345, 80, '12π', 'orange', 30)]),
], vb='60 50 340 260', w=440, col=0, title='A circle with radius 6'))
f3b11 = IH('f3b11', '$S=π\\cdot6^2=36π$', size=32, col=1)
f3b12 = IH('f3b12', '$C=2π\\cdot6=12π$', size=32, col=1)

f3a4 = PIN(GEO('f3a4', [
    ('line', [('circ', 200, 180, 110), ('dot', 200, 180), ('seg', 90, 180, 310, 180, 'ink', 3), ('txt', 200, 290 + 22, 'd = 14', 'ink', 26)]),
    ('r7', [('txt', 145, 162, '7', 'teal', 28), ('txt', 255, 162, '7', 'teal', 28), ('tick', 90, 180, 200, 180, 1), ('tick', 200, 180, 310, 180, 1)]),
], vb='60 50 340 290', w=420, col=0, title='A circle with diameter 14'))
f3b13 = IH('f3b13', '$d=14\\ \\to\\ r=7$', size=32, col=1)
f3b14 = IH('f3b14', '$S=π\\cdot7^2=49π$', size=32, col=1)
f3b15 = IH('f3b15', '$C=2π\\cdot7=14π$', size=32, col=1)

f3a5 = PIN(GEO('f3a5', [
    ('line', [('circ', 200, 180, 110), ('dot', 200, 180), ('seg', 200, 180, 310, 180, 'ink', 3, True)]),
    ('C', [('arcw', 200, 180, 110, 0, 359.9, 'orange', 7), ('txt', 345, 80, '22π', 'orange', 30), ('txt', 255, 162, '?', 'red', 30)]),
    ('r', [('seg', 200, 180, 310, 180, 'teal', 4), ('txt', 255, 205, 'r = 11', 'teal', 28)]),
], vb='60 50 340 260', w=420, col=0, title='A circle with circumference 22 pi'))
f3b16 = IH('f3b16', '$2πr=22π$', size=34, col=1)
f3b17 = IH('f3b17', '$r=22π\\div2π=11$', size=34, col=1)

f3a6 = PIN(GEO('f3a6', [
    ('line', [('circ', 200, 180, 110), ('dot', 200, 180), ('seg', 200, 180, 310, 180, 'ink', 3, True)]),
    ('S', [('circ', 200, 180, 110, 'teal', 1, False, 'teal'), ('txt', 190, 235, '121π', 'teal', 30), ('txt', 255, 162, '?', 'red', 30)]),
    ('r', [('seg', 200, 180, 310, 180, 'teal', 4), ('txt', 268, 204, 'r = 11', 'teal', 28)]),
], vb='60 50 340 260', w=420, col=0, title='A circle with area 121 pi'))
f3b18 = IH('f3b18', '$πr^2=121π$', size=34, col=1)
f3b19 = IH('f3b19', '$r^2=121$', size=34, col=1)
f3b20 = I('f3b20', '$r=11$ $\\quad$ (not $-11$: a length)', size=32, col=1)

f3_wr = 60
f3a7 = PIN(GEO('f3a7', [
    ('line', [('seg', 30, 290, 570, 290, 'ink', 3), ('circ', 110, 230, f3_wr), ('dot', 110, 230), ('seg', 110, 230, 110, 290, 'ink', 2),
              ('seg', 50, 230, 170, 230, 'ink', 2), ('circ', 110, 290, 6, 'red', 3, False, 'red')]),
    ('turn', [('circ', 110 + 377, 230, f3_wr, 'ink', 2, True), ('circ', 110 + 377, 290, 6, 'red', 3, False, 'red'),
              ('seg', 110, 290, 487, 290, 'orange', 7), ('txt', 298, 324, 'one turn = one circumference', 'orange', 26)]),
], vb='20 150 560 190', w=600, col=0, title='A wheel rolling one full turn'))
f3b21 = IH('f3b21', 'One turn: $2π\\cdot10=20π$ cm', size=30, col=1)
f3b22 = I('f3b22', 'Same units first: $10π$ m $=1{,}000π$ cm', size=28, col=1)
f3b23 = IH('f3b23', '$1000π\\div20π=50$ turns', size=30, col=1)

video('geo-079', 'lesson', slides=[
    S('Area and Circumference',
      L("Area and circumference of a circle. These are two very basic formulas, and we use them a lot in exam questions.")),
    S('The two formulas',
      L("Here's a circle with radius r. The area of a circle is the space inside it, and its formula is pi r squared.",
        show(f3a1['line'], "Here's a circle with radius r"), show(f3a1['S'], 'the space inside it'), show(f3b1, 'pi r squared')),
      L("The circumference is the length all the way around the circle, and its formula is two pi r.",
        show(f3a1['C'], 'the length all the way around'), show(f3b2, 'two pi r')),
      L("This sign is a letter called pi, and the radius we know. Notice that only the area has r squared. The area is in "
        "square centimeters, and the circumference is a length, so it's in centimeters.", pt('f3b1', 'This sign is a letter'),
        show(f3b3, 'only the area has r squared'))),
    S('What is π?',
      L("So what is pi? Let's really see. Take a circle, and here is its diameter, d.", show(f3a2['line'], "Let's really see")),
      L("Now peel off the circumference, and lay it out as a straight line.", show(f3a2['peel'], 'Now peel off')),
      L("How many times does the diameter fit into it? Once, twice, three times, and a little bit is left over.",
        show(f3a2['d1'], 'Once'), show(f3a2['d2'], 'twice'), show(f3a2['d3'], 'three times'), show(f3a2['bit'], 'a little bit is left')),
      L("So the circumference is three diameters and a bit. One diameter is two r, so three diameters are six r. So the "
        "circumference is a bit more than six r.", show(f3b4, 'So the circumference is three diameters')),
      L("And the formula says the circumference is two pi r. So two pi is a bit more than six, and pi is a bit more than "
        "three.", show(f3b5, 'So two pi is a bit more than six'), show(f3b6, 'and pi is a bit more than three'))),
    S('π is a number',
      L("So pi is a number. It's a fixed number, always the same. It's not an unknown like x or y in an equation.",
        show(f3b7, "It's a fixed number")),
      L("It just isn't a round number. Its digits after the point never end, so instead of writing them, we give it a "
        "special sign, the letter pi. That's easier to write and easier to see in the formula.", pt('f3b7', 'It just isn')),
      L("So the area, pi r squared, is a bit more than three times r squared. And for the exam, that's all we need to know "
        "about pi. It's a bit more than three.", show(f3b8, 'is a bit more than three times')),
      L("For example, is four pi more than twelve? Four times three is twelve, and pi is a bit more than three, so four pi is "
        "a bit more than twelve. Yes.", show(f3b9, 'is four pi more than twelve')),
      L("And when the answers have pi in them, keep the pi. Don't change it into a number.", show(f3b10, 'keep the pi'))),
    S('From the radius',
      L("Let's see simple examples. Say the radius is six.", show(f3a3['line'], "Let's see simple examples"), show(f3a3['r6'], 'Say the radius is six')),
      L("The area is pi r squared, so pi times six squared. Six squared is thirty-six, so the area is thirty-six pi.",
        show(f3b11, 'so pi times six squared'), show(f3a3['S'], 'so the area is thirty-six pi')),
      L("The circumference is two pi r, so two pi times six, which is twelve pi.", show(f3b12, 'so two pi times six'),
        show(f3a3['C'], 'which is twelve pi')),
      L("I put six in place of the radius and found the area. I put six in place of the radius and found the circumference.",
        pt('f3b11', 'I put six in place'))),
    S('From the diameter',
      L("Now a circle with a diameter of fourteen. Careful here. The formulas use the radius, not the diameter.",
        show(f3a4['line'], 'Now a circle with a diameter')),
      L("So first, the radius is half of fourteen, which is seven.", show(f3a4['r7'], 'So first, the radius'), show(f3b13, 'which is seven')),
      L("The area is pi times seven squared, which is forty-nine pi, and not pi times fourteen squared. The circumference is "
        "two pi times seven, which is fourteen pi.", show(f3b14, 'The area is pi times seven squared'), show(f3b15, 'The circumference is two pi times seven'))),
    S('Back from C',
      L("Another example. I don't know the radius, but I'm given that the circumference is twenty-two pi. Let's find the "
        "radius.", show(f3a5['line'], "I don't know the radius"), show(f3a5['C'], 'the circumference is twenty-two pi')),
      L("I put it into the circumference formula. Two pi r equals twenty-two pi.", show(f3b16, 'Two pi r equals')),
      L("Divide both sides by two pi. On the left I get r, and on the right, twenty-two pi divided by two pi is eleven. So "
        "the radius is eleven.", show(f3b17, 'Divide both sides by two pi'), show(f3a5['r'], 'So the radius is eleven')),
      L("I used the formula backwards. Instead of going from the radius to the circumference, I went from the circumference "
        "to the radius.", pt('f3b16', 'I used the formula backwards'))),
    S('Back from the area',
      L("Now a circle whose area is a hundred twenty-one pi. Again, I don't know the radius. I put the area into the "
        "formula, so pi r squared equals a hundred twenty-one pi.", show(f3a6['line'], 'Now a circle whose area'),
        show(f3a6['S'], 'Again, I don'), show(f3b18, 'so pi r squared equals')),
      L("Divide both sides by pi, and r squared is a hundred twenty-one. Take the root of both sides, and r is eleven.",
        show(f3b19, 'Divide both sides by pi'), show(f3b20, 'Take the root'), show(f3a6['r'], 'and r is eleven')),
      L("Minus eleven isn't relevant here, because a radius is a length. It's positive, never negative.",
        pt('f3b20', 'Minus eleven')),
      L("So from the radius we find the area and the circumference, and from the area or the circumference we find the "
        "radius.", pt('f3a6_line', 'So from the radius'))),
    S('Wheels',
      L("One more idea that the exam likes, wheels. In one full turn, a wheel rolls exactly one circumference. Look at the "
        "red point. After one turn, it's at the bottom again, one circumference further.",
        show(f3a7['line'], 'One more idea'), show(f3a7['turn'], 'In one full turn')),
      L("Say a wheel has a radius of ten centimeters. One turn is two pi times ten, which is twenty pi centimeters.",
        show(f3b21, 'One turn is two pi times ten')),
      L("How many turns does it make along a road of ten pi meters? First the same units. One meter is a hundred "
        "centimeters, so ten pi meters are a thousand pi centimeters.", show(f3b22, 'First the same units')),
      L("A thousand pi divided by twenty pi is fifty, so the wheel makes fifty turns. Now let's see an exam question. "
        "[pause] Okay. I'll see you in the next video.", show(f3b23, 'A thousand pi divided by twenty pi'))),
])

# ================================================================================================ geo33-g080
# Hebrew (geo 3720-3735, her "area = circumference" -> 2; the course: area = 4 times the circumference -> 8): just work
# from the data; ignore the units (square centimeters and centimeters); pi r squared = (4 times) 2 pi r; divide by pi;
# divide by r; "let's really check" (both sides with r = 8). Kept from the English script: the short way S / C = r / 2.
# Added: why we may divide by r (a radius isn't zero), the traps 4 (forgot the 2 of 2 pi r) and 16 (the diameter).
# V3: no question figure. A circle on the right with the area tinted and the circumference traced (which is which), the
# equation built line by line on the left, the found radius written on the circle.
f3c0 = PIN(GEO('f3c0', [
    ('line', [('circ', 200, 180, 110), ('dot', 200, 180), ('seg', 200, 180, 310, 180, 'ink', 3), ('txt', 255, 162, 'r', 'ink', 28, True)]),
    ('S', [('circ', 200, 180, 110, 'teal', 1, False, 'teal'), ('txt', 190, 235, 'πr²', 'teal', 30)]),
    ('C', [('arcw', 200, 180, 110, 0, 359.9, 'orange', 7), ('txt', 350, 80, '2πr', 'orange', 30)]),
    ('r8', [('seg', 200, 180, 310, 180, 'red', 4), ('txt', 255, 205, 'r = 8', 'red', 28)]),
], vb='60 50 340 260', w=420, col=1, title='A circle: its area and its circumference'))
_R(f3c0, 330)
f3c1 = I('f3c1', 'Area $=4\\cdot$ circumference', size=34)
f3c2 = IH('f3c2', '$πr^2=4\\cdot2πr$', size=34)
f3c3 = IH('f3c3', '$πr^2=8πr$', size=34)
f3c4 = IH('f3c4', '$r^2=8r$', size=34)
f3c5 = IH('f3c5', '$r=8$ $\\quad$ ($r\\ne0$)', size=34)
f3c6 = IH('f3c6', '$S=π\\cdot8^2=64π$, $\\ C=2π\\cdot8=16π$', size=30)
f3c7 = IH('f3c7', '$4\\cdot16π=64π$ ✓', size=30)
f3c8 = I('f3c8', '$\\dfrac{S}{C}=\\dfrac{πr^2}{2πr}=\\dfrac{r}{2}$', size=34)
f3c9 = IH('f3c9', '$\\frac{r}{2}=4$, $\\ r=8$', size=34)
video('solve-geo33-g080', 'solution', qid='geo33-g080', slides=[
    S('Write it as an equation',
      L("The numerical value of a circle's area in square centimeters is four times as much as the numerical value of its "
        "circumference in centimeters. What is its radius, in centimeters?", pt('stem', 'The numerical value', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("All the question tells us is how the area and the circumference compare, and we want the radius. Both formulas "
        "have r in them. [short pause] So we'll simply write the given as an equation, and solve it.",
        show(f3c0['line'], 'how the area and the circumference compare')),
      L("[short pause] What I need to do is simply work from the data. You can ignore the square centimeters and the "
        "centimeters. Just read it as, the area is four times the circumference.", show(f3c1, 'the area is four times')),
      L("The area is pi r squared. The circumference is two pi r, and four times it is four times two pi r.",
        show(f3c0['S'], 'The area is pi r squared'), show(f3c0['C'], 'The circumference is two pi r'),
        show(f3c2, 'four times it is')),
      L("Four times two pi r is eight pi r. Careful not to lose the two of two pi r. Someone who loses it gets four, and "
        "that's choice number four.", show(f3c3, 'Four times two pi r is eight pi r'), mk('cross', 'choice 4', "that's choice number four")),
      L("Now divide both sides by pi. On the left I get r squared, and on the right, eight r.", show(f3c4, 'Now divide both sides by pi')),
      L("Then divide both sides by r. We're allowed to, because r is a radius, so it isn't zero. r squared divided by r is r, "
        "and eight r divided by r is eight. So r is eight. Choice number one is our answer.",
        show(f3c5, 'Then divide both sides by r'), show(f3c0['r8'], 'So r is eight'), mk('tick', 'choice 1', 'Choice number one is our answer')),
      L("Sixteen is in the choices too. That's the diameter, two times eight, but the question asks for the radius.",
        mk('cross', 'choice 2', "That's the diameter")), sb='Method 1 · The math way'),
    S('Let\'s really check',
      L("In the exam you'd mark it and move on. Here, let's really check. With a radius of eight, the area is pi times eight "
        "squared, sixty-four pi. The circumference is two pi times eight, sixteen pi.", show(f3c6, "Here, let's really check")),
      L("And four times sixteen pi is sixty-four pi. So the area really is four times the circumference.",
        show(f3c7, 'And four times sixteen pi')), sb='Method 1 · The math way'),
    SM('Method 2 · Understanding', 'Area over circumference',
      L("[pause] There's also a short way, by understanding. Divide the area by the circumference. Pi r squared over two pi r. The pi cancels, "
        "one r cancels, and we're left with r over two.", show(f3c8, 'Divide the area by the circumference')),
      L("Here the area is four times the circumference, so r over two is four, and r is eight. Choice number one again. "
        "[pause] Okay. I'll see you in the next question.", show(f3c9, 'so r over two is four'),
        mk('tick', 'choice 1', 'Choice number one again'))),
])

# ================================================================================================ q-r26-t33-03 (added)
# No Hebrew source (a course addition). Percent is a later topic, so the little needed is said here: 100 percent is the
# whole, 50 percent is half, 25 percent is a quarter. REMINDERS: C = 2 pi r (geo-079), every length times k -> the area
# times k squared (the square lesson, topic 32). Method 1: the circumference times one and a half -> the radius too -> the
# area times nine quarters -> up by one and a quarter = 125 percent. Method 2: an easy radius (2 -> 3). Traps at the step:
# 225 percent (the new area, not the increase) and 50 percent (forgot the square).
# V3: no question figure. Two circles side by side, radius 2 and radius 3, the circumference traced and the areas tinted,
# the values written on each circle as they are found.
f3d0 = PIN(GEO('f3d0', [
    ('line', [('circ', 110, 180, 64), ('dot', 110, 180), ('seg', 110, 180, 174, 180, 'ink', 3), ('txt', 142, 164, '2', 'ink', 26),
              ('circ', 360, 180, 96), ('dot', 360, 180), ('seg', 360, 180, 456, 180, 'ink', 3), ('txt', 408, 164, '3', 'ink', 26)]),
    ('C', [('arcw', 110, 180, 64, 0, 359.9, 'orange', 6), ('arcw', 360, 180, 96, 0, 359.9, 'orange', 6),
           ('txt', 110, 92, '4π', 'orange', 28), ('txt', 360, 60, '6π', 'orange', 28)]),
    ('S', [('circ', 110, 180, 64, 'teal', 1, False, 'teal'), ('circ', 360, 180, 96, 'teal', 1, False, 'teal'),
           ('txt', 110, 215, '4π', 'teal', 28), ('txt', 360, 225, '9π', 'teal', 28)]),
], vb='30 30 450 260', w=500, col=1, title='Radius 2 and radius 3'))
_R(f3d0, 330)
f3d1 = I('f3d1', '$50\\%$ more $=$ half more $=\\times\\dfrac{3}{2}$', size=32)
f3d2 = I('f3d2', '$C=2πr$: $\\ r\\times\\dfrac{3}{2}$', size=32)
f3d3 = IH('f3d3', 'Area $\\times\\left(\\dfrac{3}{2}\\right)^2=\\times\\dfrac{9}{4}=\\times2\\dfrac{1}{4}$', size=32)
f3d4 = I('f3d4', 'Up by $1\\dfrac{1}{4}$ of the old area $=125\\%$', size=32)
f3d5 = IH('f3d5', '$r=2$: $\\ C=4π$, $\\ 4π+2π=6π$, $\\ r=3$', size=30)
f3d6 = IH('f3d6', '$S$: $\\ 4π\\to9π$, up $5π$', size=30)
f3d7 = I('f3d7', '$\\dfrac{5π}{4π}=\\dfrac{5}{4}=1\\dfrac{1}{4}=125\\%$', size=32)
video('solve-q-r26-t33-03', 'solution', qid='q-r26-t33-03', slides=[
    S('Length × 3/2, area × 9/4',
      L("The circumference of a circle increases by fifty percent. By what percent does its area increase?",
        pt('stem', 'The circumference of a circle', 'hl', 5.0), voice='calm', pause=0.5),
      L("We're not given any lengths, only how much the circumference grows. And we're asked how much the area grows. [short "
        "pause] We'll solve it with the rule for growing lengths, and then check it with easy numbers.",
        pt('stem', 'only how much the circumference grows')),
      L("[short pause] We'll meet percent properly later. For now, all we need is this. A hundred percent is the whole "
        "thing, fifty percent is half of it, and twenty-five percent is a quarter of it. So fifty percent more means half "
        "more, and the circumference is multiplied by one and a half, three over two.", show(f3d1, 'So fifty percent more')),
      L("The circumference is two pi r. Two pi never changes, so if the circumference is multiplied by three over two, the "
        "radius is multiplied by three over two too.", show(f3d2, 'The circumference is two pi r')),
      L("Remember from the square lesson. When every length is multiplied by some number, the area is multiplied by that "
        "number squared. Three over two, squared, is nine over four, which is two and a quarter. So the new area is two and "
        "a quarter times the old area.", show(f3d3, 'Three over two, squared')),
      L("Careful, two and a quarter times is two hundred twenty-five percent, and that's choice number three. But that's the "
        "whole new area, not the increase.", mk('cross', 'choice 3', "and that's choice number three")),
      L("The increase is the new area minus the old one. Two and a quarter minus one is one and a quarter. One whole is a "
        "hundred percent, and a quarter is twenty-five percent, so the area increases by a hundred twenty-five percent. "
        "Choice number four is our answer.", show(f3d4, 'The increase is the new area'),
        mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("And fifty percent, choice number one, is someone who forgot to square. The area grows faster than the "
        "circumference.", mk('cross', 'choice 1', 'someone who forgot to square')), sb='Method 1 · Understanding'),
    SM('Method 2 · Plugging in numbers', 'Easy numbers',
      L("[pause] Now let's check by plugging in easy numbers. The question doesn't give a radius, so the answer is the same for "
        "every circle. Let's pick a radius of two, because it's small and easy.", show(f3d0['line'], "Let's pick a radius of two")),
      L("With a radius of two, the circumference is two pi times two, four pi. Fifty percent more is half more. Half of four "
        "pi is two pi, so the new circumference is six pi, and the new radius is three.", show(f3d0['C'], 'With a radius of two'),
        show(f3d5, 'Half of four')),
      L("Now the areas. Pi times two squared is four pi, and pi times three squared is nine pi. So the area went up by "
        "five pi.", show(f3d0['S'], 'Now the areas'), show(f3d6, 'So the area went up')),
      L("Out of the old four pi, that's five pi over four pi, five quarters, which is one and a quarter, a hundred "
        "twenty-five percent. The same answer, choice number four. [pause] Okay. I'll see you in the next question.",
        show(f3d7, 'five pi over four pi'), mk('tick', 'choice 4', 'The same answer, choice number four'))),
])

# =================================================================================================================
# Topic 33 fragment f4 (TAG D, 2026-10-14): the lesson "Sectors and Arcs" (geo-081) and its two examples (g082, g083).
# Hebrew: geo 3738-3884 (the arc-and-sector lesson, with its two examples inside it). The course's numbers are kept
# (25pi -> 40pi; the examples r 3 / arc 2pi -> r 10 / arc 4pi, and r 4 / 45 + 90 -> r 3 / 40 + 120).
# =================================================================================================================
FIG_LEFT.update({'solve-geo33-g082', 'solve-geo33-g083'})


def f4_cuts(cx, cy, r, n, start=0, col='ink', w=2, dashed=False):
    """n radii that cut the circle into n equal parts, the first one at `start` degrees"""
    out = []
    for k in range(n):
        x, y = gpt(cx, cy, r, start + 360.0 * k / n)
        out.append(('seg', cx, cy, x, y, col, w, dashed))
    return out


def f4_at(cx, cy, r, deg, t, col='ink', size=24):
    x, y = gpt(cx, cy, r, deg)
    return ('txt', x, y, t, col, size)


def f4_rad(cx, cy, r, deg, col='ink', w=3):
    x, y = gpt(cx, cy, r, deg)
    return ('seg', cx, cy, x, y, col, w)


def f4_o(cx, cy, dx=-16, dy=16):
    return [('dot', cx, cy), ('txt', cx + dx, cy + dy, 'O', 'ink', 22, True)]


# ------------------------------------------------------------------------------------------------ geo-081 (lesson)
# Hebrew (geo 3738-3828): a sector = the part between two radii and the arc between them, "a slice of pizza"; its area is
# its share of the circle; the formula alpha/360 * pi r^2 - "I recommend not using it", solve by understanding; a quarter
# (90, divide the area by 4); an eighth, "a family-size pizza slice" (45 = half of 90, "good to know, but what interests
# me: an eighth"); a fifth (360/5 = 72, area/5); the arc = a piece of the circle, its length its share; the formula
# alpha/360 * 2 pi r ("before times the area, now times the circumference"), leave it; a sixth (60), a third (120); two
# fifths (72 + 72 = 144); the summary (a third, a quarter, a fifth, a sixth - find the circumference or the area and
# divide); the angles to remember (90, 45, 60, 40, 36, 72) and the bigger ones built from them (270, 144, 120 two ways);
# "the exam doesn't check pocket calculators, nobody gives 23 and a half degrees". Kept from the English lesson: the
# worked numbers (r 6: 36pi -> 9pi, 9pi/2; 40pi -> 8pi; r 9: 18pi -> 3pi, 6pi) and the sector perimeter = arc + 2r.
# Cut: the repeats of "what really interests me" and of the formula advice.
# V3: every idea on a clean circle, built at her words: the radii, then the arc traced thick (arcw), then the sector
# tinted (wedge); the "cut into n" radii thin ink, the part under study always teal; the angle and the fraction written
# on the figure when they are found; 2-3 variations each (a thin and a wide sector; 4 and 8; 5; 6 and 3; two fifths).
_c = (180, 170); _r = 120
f4sec = PIN(GEO('f4sec', [
    ('line', [('circ', _c[0], _c[1], _r)] + f4_o(*_c, dx=-4, dy=22)),
    ('radii', [f4_rad(_c[0], _c[1], _r, 25, 'teal', 4), f4_rad(_c[0], _c[1], _r, 105, 'teal', 4)]),
    ('arc', [('arcw', _c[0], _c[1], _r, 25, 105, 'teal', 8)]),
    ('wedge', [('wedge', _c[0], _c[1], _r, 25, 105, 'teal'), f4_at(_c[0], _c[1], 72, 65, 'sector', 'teal', 22)]),
    ('more', [('circ', 470, 170, _r), ('dot', 470, 170), ('wedge', 470, 170, _r, 140, 300, 'teal'),
              ('arcw', 470, 170, _r, 140, 300, 'teal', 8), f4_rad(470, 170, _r, 140, 'teal', 4), f4_rad(470, 170, _r, 300, 'teal', 4),
              f4_at(470, 170, 66, 220, 'sector', 'teal', 22)]),
], vb='40 30 570 285', w=1000, col=0, title='A sector: two radii and the arc between them'))

f4ar = PIN(GEO('f4ar', [
    ('line', [('circ', _c[0], _c[1], _r), ('wedge', _c[0], _c[1], _r, 20, 110, 'teal'), f4_rad(_c[0], _c[1], _r, 20, 'teal', 4),
              f4_rad(_c[0], _c[1], _r, 110, 'teal', 4), ('arcw', _c[0], _c[1], _r, 20, 110, 'teal', 8)] + f4_o(*_c, dx=-4, dy=22)),
    ('alpha', [('arc', _c[0], _c[1], 34, 20, 110, 'teal', 'α', 56)]),
], vb='40 30 280 285', w=520, col=0, title='A sector with its central angle'))
f4k1 = I('f4k1', 'Sector area $=\\frac{\\alpha}{360°}\\cdot\\pi r^2$', size=34, col=1)
f4k2 = I('f4k2', 'Which part of the circle is it?', size=32, col=1)

# quarters and eighths: two circles side by side
_a, _b = (150, 170), (450, 170)
f4q = PIN(GEO('f4q', [
    ('line', [('circ', _a[0], _a[1], _r), ('dot', *_a)]),
    ('cut4', f4_cuts(_a[0], _a[1], _r, 4)),
    ('quarter', [('wedge', _a[0], _a[1], _r, 0, 90, 'teal'), ('right', _a[0], _a[1], 0, 90, 18),
                 f4_at(_a[0], _a[1], 62, 45, '90°', 'teal', 24), f4_at(_a[0], _a[1], _r + 30, 45, '1/4', 'teal', 28)]),
    ('cut8', [('circ', _b[0], _b[1], _r), ('dot', *_b)] + f4_cuts(_b[0], _b[1], _r, 8)),
    ('eighth', [('wedge', _b[0], _b[1], _r, 0, 45, 'teal'), ('arc', _b[0], _b[1], 30, 0, 45, 'teal'),
                f4_at(_b[0], _b[1], 76, 22.5, '45°', 'teal', 22), f4_at(_b[0], _b[1], _r + 30, 22.5, '1/8', 'teal', 28)]),
], vb='0 20 610 300', w=860, col=0, title='A quarter and an eighth of a circle'))
f4k3 = IH('f4k3', '$r=6$: $\\ \\pi\\cdot6^2=36\\pi$', size=34, col=0)
f4k4 = IH('f4k4', 'quarter: $36\\pi\\div4=9\\pi$', size=32, col=0)
f4k5 = IH('f4k5', 'eighth: $9\\pi\\div2=\\frac{9\\pi}{2}$', size=32, col=0)

f4f = PIN(GEO('f4f', [
    ('line', [('circ', _c[0], _c[1], _r), ('dot', *_c)] + f4_cuts(_c[0], _c[1], _r, 5, 18)),
    ('fifth', [('wedge', _c[0], _c[1], _r, 18, 90, 'teal'), ('arc', _c[0], _c[1], 30, 18, 90, 'teal'),
               f4_at(_c[0], _c[1], 66, 54, '72°', 'teal', 22), f4_at(_c[0], _c[1], _r + 30, 54, '1/5', 'teal', 28)]),
], vb='30 15 300 300', w=520, col=0, title='A fifth of a circle'))
f4k6 = IH('f4k6', '$360°\\div5=72°$', size=34, col=1)
f4k7 = IH('f4k7', '$40\\pi\\div5=8\\pi$', size=34, col=1)

f4arc = PIN(GEO('f4arc', [
    ('line', [('circ', _c[0], _c[1], _r), ('dot', *_c), ('arcw', _c[0], _c[1], _r, 30, 100, 'teal', 9),
              f4_at(_c[0], _c[1], _r + 28, 65, 'arc', 'teal', 24)]),
    ('alpha', [f4_rad(_c[0], _c[1], _r, 30, 'teal', 2), f4_rad(_c[0], _c[1], _r, 100, 'teal', 2),
               ('arc', _c[0], _c[1], 34, 30, 100, 'teal', 'α', 56)]),
], vb='40 15 280 300', w=520, col=0, title='An arc of a circle'))
f4k8 = I('f4k8', 'Arc length $=\\frac{\\alpha}{360°}\\cdot2\\pi r$', size=34, col=1)

f4s = PIN(GEO('f4s', [
    ('line', [('circ', _a[0], _a[1], _r), ('dot', *_a)] + f4_cuts(_a[0], _a[1], _r, 6, 30)),
    ('sixth', [('arcw', _a[0], _a[1], _r, 30, 90, 'teal', 9), ('arc', _a[0], _a[1], 30, 30, 90, 'teal'),
               f4_at(_a[0], _a[1], 62, 60, '60°', 'teal', 22), f4_at(_a[0], _a[1], _r + 30, 60, '1/6', 'teal', 28)]),
    ('cut3', [('circ', _b[0], _b[1], _r), ('dot', *_b)] + f4_cuts(_b[0], _b[1], _r, 3, 30)),
    ('third', [('arcw', _b[0], _b[1], _r, 30, 150, 'teal', 9), ('arc', _b[0], _b[1], 30, 30, 150, 'teal'),
               f4_at(_b[0], _b[1], 58, 90, '120°', 'teal', 22), f4_at(_b[0], _b[1], _r + 30, 90, '1/3', 'teal', 28)]),
], vb='0 10 610 310', w=860, col=0, title='A sixth and a third of a circle'))
f4k9 = IH('f4k9', '$r=9$: $\\ 2\\pi\\cdot9=18\\pi$', size=34, col=0)
f4k10 = IH('f4k10', 'sixth: $18\\pi\\div6=3\\pi$', size=32, col=0)
f4k11 = IH('f4k11', 'third: $18\\pi\\div3=6\\pi$', size=32, col=0)

f4t = PIN(GEO('f4t', [
    ('line', [('circ', _c[0], _c[1], _r), ('dot', *_c)] + f4_cuts(_c[0], _c[1], _r, 5, 18)),
    ('one', [('arcw', _c[0], _c[1], _r, 18, 90, 'teal', 9), ('arc', _c[0], _c[1], 30, 18, 90, 'teal'),
             f4_at(_c[0], _c[1], 66, 54, '72°', 'teal', 22), f4_at(_c[0], _c[1], _r + 30, 54, '1/5', 'teal', 26)]),
    ('two', [('arcw', _c[0], _c[1], _r, 90, 162, 'teal', 9), ('arc', _c[0], _c[1], 30, 90, 162, 'teal'),
             f4_at(_c[0], _c[1], 66, 126, '72°', 'teal', 22), f4_at(_c[0], _c[1], _r + 30, 126, '1/5', 'teal', 26)]),
], vb='30 15 300 300', w=520, col=0, title='Two fifths of a circle'))
f4k12 = IH('f4k12', '$72°+72°=144°$', size=34, col=1)
f4k13 = I('f4k13', '$\\frac15+\\frac15=\\frac25$ of the circle', size=34, col=1)

f4k14 = I('f4k14', '$90°=\\frac14\\qquad45°=\\frac18\\qquad60°=\\frac16$', size=40, col=0)
f4k15 = I('f4k15', '$40°=\\frac19\\qquad36°=\\frac1{10}\\qquad72°=\\frac15$', size=40, col=0)
f4k16 = I('f4k16', '$270°=3\\cdot90°=\\frac34$', size=36, col=0)
f4k17 = I('f4k17', '$144°=2\\cdot72°=\\frac25$', size=36, col=0)
f4k18 = I('f4k18', '$120°=2\\cdot60°=3\\cdot40°=\\frac13$', size=36, col=0)
f4k19 = I('f4k19', 'The exam checks understanding, not calculators', size=32, col=0)

f4p = PIN(GEO('f4p', [
    ('line', [('circ', _c[0], _c[1], _r), ('dot', *_c), f4_rad(_c[0], _c[1], _r, 30), f4_rad(_c[0], _c[1], _r, 90),
              ('arc', _c[0], _c[1], 30, 30, 90, 'ink', '60°', 54)]),
    ('arc', [('arcw', _c[0], _c[1], _r, 30, 90, 'teal', 9), f4_at(_c[0], _c[1], _r + 28, 60, '3π', 'teal', 26)]),
    ('radii', [f4_rad(_c[0], _c[1], _r, 30, 'orange', 6), f4_rad(_c[0], _c[1], _r, 90, 'orange', 6),
               ('txt', _c[0] - 18, _c[1] - 62, '9', 'orange', 26), ('txt', _c[0] + 62, _c[1] - 8, '9', 'orange', 26)]),
], vb='40 15 280 300', w=520, col=0, title='The arc and the perimeter of a sector'))
f4k20 = IH('f4k20', 'arc: $18\\pi\\div6=3\\pi$', size=32, col=1)
f4k21 = I('f4k21', 'perimeter: $3\\pi+9+9=3\\pi+18$', size=32, col=1, hand='perimeter :   3π + 9 + 9 = 3π + 18')
video('geo-081', 'lesson', slides=[
    S('Sectors and Arcs',
      L("Sectors and arcs. First, let's understand what a sector is and what an arc is.")),
    S('A sector',
      L("Here's a circle with its center. Let's draw two radii. Between them, there's an arc, a piece of the circle. The "
        "part enclosed by the two radii and the arc between them is called a sector. It's a bit like a slice of pizza.",
        show(f4sec['line'], "Here's a circle"), show(f4sec['radii'], "Let's draw two radii"),
        show(f4sec['arc'], "Between them, there's an arc"), show(f4sec['wedge'], 'is called a sector')),
      L("A sector can be thin or wide. This one is wider, but it's still two radii and the arc between them.",
        show(f4sec['more'], 'This one is wider'))),
    S('Sector area',
      L("The area of a sector is its share of the whole circle. There's a formula for it. The angle of the sector at the "
        "center is its central angle, alpha. We take alpha over three hundred sixty, times the area of the circle, pi r "
        "squared.", show(f4ar['line'], 'The area of a sector'), show(f4ar['alpha'], 'its central angle'),
        show(f4k1, 'We take alpha over')),
      L("I strongly recommend not using this formula, unless it's really the only way you understand it. It's much better "
        "to see which part of the circle it is. Let's see what I mean.", show(f4k2, 'which part of the circle it is'))),
    S('Quarters and eighths',
      L("Here's a circle. Let's cut it into four equal parts. This sector is a quarter of the circle. Three hundred sixty "
        "divided by four is ninety, so its angle is ninety degrees.", show(f4q['line'], "Here's a circle"),
        show(f4q['cut4'], 'cut it into four'), show(f4q['quarter'], 'This sector is a quarter')),
      L("Instead of the formula, all I need to see is that it's a quarter. So I take the area of the circle, and divide it "
        "by four.", pt('f4q_line', 'all I need to see')),
      L("Now let's cut a circle into eight. This sector, a real slice of family-size pizza, is an eighth of the circle. Its "
        "angle is forty-five, half of ninety. Good to know, but what matters is that it's an eighth.",
        show(f4q['cut8'], 'cut a circle into eight'), show(f4q['eighth'], 'is an eighth of the circle')),
      L("For example, with a radius of six, the area of the circle is pi times six squared, thirty-six pi. A quarter of it "
        "is nine pi, and an eighth is half of that, nine pi over two.", show(f4k3, 'pi times six squared'),
        show(f4k4, 'A quarter of it'), show(f4k5, 'an eighth is half of that'))),
    S('Fifths',
      L("This circle is cut into five equal sectors, so the angle is three hundred sixty divided by five, seventy-two "
        "degrees. But what matters is that the sector is a fifth of the circle. Say the circle's area is forty pi. Then the "
        "sector is forty pi divided by five, eight pi.", show(f4f['line'], 'This circle is cut into five'),
        show(f4k6, 'so the angle is three hundred sixty'), show(f4f['fifth'], 'the sector is a fifth'),
        show(f4k7, 'Then the sector is'))),
    S('Arc length',
      L("Now the arc. An arc is simply a piece of the circle itself. Its length is also its share of the whole circle.",
        show(f4arc['line'], 'An arc is simply'), show(f4arc['alpha'], 'its share of the whole circle')),
      L("There's a formula here too. Alpha over three hundred sixty, but this time times the circumference, two pi r. "
        "Before, it was times the area, because we wanted an area. Now we want a length. But here too, my advice is to "
        "leave the formula, and solve it by understanding.", show(f4k8, "There's a formula here too"))),
    S('Sixths and thirds',
      L("This circle is cut into six equal parts, so this arc is a sixth of the circle. We find the circumference and "
        "divide it by six. The angle, by the way, is sixty degrees, three hundred sixty divided by six.",
        show(f4s['line'], 'This circle is cut into six'), show(f4s['sixth'], 'so this arc is a sixth')),
      L("With a radius of nine, the circumference is two pi times nine, eighteen pi. A sixth of it is three pi.",
        show(f4k9, 'two pi times nine'), show(f4k10, 'A sixth of it')),
      L("Now a circle cut into three. The arc is a third, so eighteen pi divided by three, six pi. And the angle is a "
        "hundred twenty, three hundred sixty divided by three.", show(f4s['cut3'], 'a circle cut into three'),
        show(f4s['third'], 'The arc is a third'), show(f4k11, 'so eighteen pi divided by'))),
    S('Two fifths',
      L("A slightly harder one. Again the circle is cut into five, so every angle is seventy-two. But this arc covers two "
        "of those parts. It's one fifth here, and another fifth here, so together it's two fifths of the circle. And its "
        "angle is seventy-two plus seventy-two, a hundred forty-four.",
        show(f4t['line'], 'Again the circle is cut into five'), show(f4t['one'], 'one fifth here'),
        show(f4t['two'], 'and another fifth here'), show(f4k13, "together it's two fifths"),
        show(f4k12, 'seventy-two plus seventy-two')),
      L("So yes, the formulas work. But it's much simpler to see which part of the circle it is, a third, a quarter, a "
        "fifth, a sixth. Then find the circumference or the area, and divide.", pt('f4k13', 'which part of the circle it is'))),
    S('Angles to know',
      L("Here are the angles worth remembering. Ninety degrees is a quarter. Forty-five is an eighth, because it's half of "
        "ninety, and half of a quarter is an eighth. Sixty is a sixth.", show(f4k14, 'Ninety degrees is a quarter')),
      L("Forty is a ninth, because three hundred sixty divided by nine is forty. Thirty-six is a tenth, three hundred sixty "
        "divided by ten. And seventy-two is a fifth.", show(f4k15, 'Forty is a ninth')),
      L("We can also build bigger angles from them. Two hundred seventy is three times ninety, so it's three quarters. A "
        "hundred forty-four is twice seventy-two, so it's two fifths. A hundred twenty is a third. You can just know it, "
        "but it's also a sixth times two, or a ninth times three.",
        show(f4k16, 'Two hundred seventy is'), show(f4k17, 'hundred forty-four is twice'), show(f4k18, 'A hundred twenty is a third')),
      L("Remember these, and you'll find arcs and sectors in seconds. On the exam, these are the angles you'll get, not "
        "twenty-three and a half degrees. They check whether you understand that sixty degrees is a sixth of the circle.",
        show(f4k19, 'They check whether you understand'))),
    S('Arc or perimeter?',
      L("One last thing. The arc is only the curved part. Say the radius is nine and the angle is sixty degrees. The arc is "
        "a sixth of eighteen pi, which is three pi.", show(f4p['line'], 'One last thing'), show(f4p['arc'], 'The arc is only'),
        show(f4k20, 'a sixth of eighteen pi')),
      L("The perimeter of the sector goes all the way around it, the arc plus the two radii. So it's three pi plus nine "
        "plus nine, which is three pi plus eighteen. Read carefully what the question asks for. Now let's go to examples. "
        "[pause] Okay. I'll see you in the next video.", show(f4p['radii'], 'the arc plus the two radii'),
        show(f4k21, "So it's three pi plus nine"))),
])


# ------------------------------------------------------------------------------------------------ geo33-g082 (Hebrew: the lesson's first example)
# Hebrew (geo 3830-3845): "I could plug into the arc-length formula, alpha/360 * 2 pi r ... and if I confused you, great:
# no need"; the whole circumference 2 pi r; the arc out of the circumference is a fraction (her 2pi of 6pi = a third,
# here 4pi of 20pi = a fifth); the angle is the same fraction of 360 (her 120, here 72).
# V3: the colour copy on the right (same orientation and labels); the whole circumference traced dashed with 20pi; the
# arc traced thick teal with 4pi / 20pi = 1/5; the circle cut into five such arcs (dashed radii); the sector tinted teal
# and alpha = 72 written on it.
_O = (320.0, 180.0); _R0 = 109.5
f4q82 = [('circ', _O[0], _O[1], _R0, 'ink', 2.5), ('seg', 320, 180, 427.836, 160.986, 'ink', 2.5), ('seg', 320, 180, 335.239, 71.566, 'ink', 2.5),
         ('arcw', _O[0], _O[1], _R0, 10, 82, 'ink', 6), ('arc', _O[0], _O[1], 29.2, 10, 82, 'ink'), ('dot', 320, 180),
         ('txt', 351.954, 146.91, 'α', 'ink', 22), ('txt', 446.548, 157.686, 'A', 'ink', 22, True), ('txt', 337.884, 52.751, 'B', 'ink', 22, True),
         ('txt', 305, 195, 'O', 'ink', 22, True), ('txt', 415.516, 81.091, '4π', 'ink', 22)]
f4g82 = PIN(GEO('f4g82', [
    ('line', f4q82 + [('txt', 382, 192, '10', 'ink', 22)]),
    ('circ', [('circ', _O[0], _O[1], _R0, 'orange', 4, True), ('txt', 320, 322, 'whole circle: 2π · 10 = 20π', 'orange', 23)]),
    ('arc', [('arcw', _O[0], _O[1], _R0, 10, 82, 'teal', 10), ('txt', 320, 356, '4π out of 20π = 1/5', 'teal', 23)]),
    ('five', f4_cuts(_O[0], _O[1], _R0, 5, 10, 'teal', 2, True)),
    ('alpha', [('wedge', _O[0], _O[1], _R0, 10, 82, 'teal'), ('txt', 320, 390, 'α = 360° ÷ 5 = 72°', 'red', 25)]),
], vb='150 35 340 372', w=400, title='Circle with center O and the arc AB'))
_R(f4g82, 200)
video('solve-geo33-g082', 'solution', qid='geo33-g082', slides=[
    S('A fifth of the circle',
      L("A circle with center O has a radius of ten centimeters. The highlighted arc A B is four pi centimeters long. What "
        "is alpha?", pt('stem', 'A circle with center O', 'hl', 8.0), voice='calm', pause=0.5),
      L("We could put the numbers into the arc-length formula. Alpha over three hundred sixty, times two pi r, equals four "
        "pi, and so on. If that confused you a little, great, because we don't need it. [short pause] We'll see which part "
        "of the circle the arc is.", show(f4g82['line'], 'We could put the numbers')),
      L("We know the arc is four pi, and the radius is ten. So let's find the whole circumference. Two pi r is two pi times "
        "ten, which is twenty pi.", show(f4g82['circ'], "let's find the whole circumference")),
      L("So the whole circle is twenty pi, and the arc is four pi. Four pi out of twenty pi is like four out of twenty, "
        "which is a fifth. So the arc is a fifth of the circle. Five arcs like it go all the way around.",
        show(f4g82['arc'], 'Four pi out of twenty pi'), show(f4g82['five'], 'Five arcs like it')),
      L("And if the arc is a fifth of the circle, its central angle is also a fifth of the full turn. A fifth of three "
        "hundred sixty is seventy-two. So alpha is seventy-two degrees, choice number three. [pause] Okay. I'll see you in "
        "the next question.", show(f4g82['alpha'], 'its central angle is also a fifth'),
        mk('tick', 'choice 3', 'choice number three'))),
])


# ------------------------------------------------------------------------------------------------ geo33-g083 (Hebrew: the lesson's second example)
# Hebrew (geo 3847-3867): "I could plug into the formula, but I'll save myself that"; each angle as a part of the circle
# (her 90 = 1/4, 45 = 1/8; here 120 = 1/3, 40 = 1/9), marked on each sector; the sum in a common denominator (here
# 3/9 + 1/9 = 4/9); the area of the circle pi r^2 (9 pi); "I don't need the whole circle, only 4/9 of it" -> 4 pi. Kept
# from the English script: separately, a ninth pi and a third 3 pi. Added at the step: the traps 8pi/3 (4/9 of the
# circumference) and 3pi (only the big sector).
# V3: the colour copy on the right; the big sector tinted orange (a large angle) with 1/3, the small one teal with 1/9,
# each written outside its arc; the working in rows under the circle, the answer red.
f4q83 = [('circ', _O[0], _O[1], _R0, 'ink', 2.5), ('wedge', _O[0], _O[1], _R0, 0, 120, 'ink'), ('wedge', _O[0], _O[1], _R0, 200, 240, 'ink'),
         f4_rad(_O[0], _O[1], _R0, 0, 'ink', 2.2), f4_rad(_O[0], _O[1], _R0, 120, 'ink', 2.2), f4_rad(_O[0], _O[1], _R0, 200, 'ink', 2.2),
         f4_rad(_O[0], _O[1], _R0, 240, 'ink', 2.2), ('arc', _O[0], _O[1], 32.85, 0, 120, 'ink'), ('arc', _O[0], _O[1], 32.85, 200, 240, 'ink'),
         ('txt', 347, 133.235, '120°', 'ink', 20), ('txt', 277.102, 215.996, '40°', 'ink', 20), ('dot', 320, 180),
         ('txt', 338, 200, 'O', 'ink', 22, True)]
f4g83 = PIN(GEO('f4g83', [
    ('line', f4q83),
    ('third', [('wedge', _O[0], _O[1], _R0, 0, 120, 'orange'), ('arcw', _O[0], _O[1], _R0, 0, 120, 'orange', 6),
               f4_at(_O[0], _O[1], _R0 + 28, 60, '1/3', 'orange', 28)]),
    ('ninth', [('wedge', _O[0], _O[1], _R0, 200, 240, 'teal'), ('arcw', _O[0], _O[1], _R0, 200, 240, 'teal', 6),
               f4_at(_O[0], _O[1], _R0 + 28, 220, '1/9', 'teal', 28)]),
    ('sum', [('txt', 320, 318, '1/3 + 1/9 = 3/9 + 1/9 = 4/9', 'ink', 24)]),
    ('area', [('txt', 320, 347, 'circle: π · 3² = 9π', 'ink', 24)]),
    ('ans', [('txt', 320, 376, '4/9 of 9π = 4π', 'red', 26)]),
    ('sep', [('txt', 320, 405, 'or: π + 3π = 4π', 'teal', 24)]),
], vb='150 48 340 372', w=400, title='Circle with center O and two shaded sectors'))
_R(f4g83, 200)
video('solve-geo33-g083', 'solution', qid='geo33-g083', slides=[
    S('Parts of the circle',
      L("A circle with center O has a radius of three centimeters. Two shaded sectors that don't overlap have central "
        "angles of forty degrees and a hundred twenty degrees. What is their total area, in square centimeters?",
        pt('stem', 'A circle with center O', 'hl', 10.0), voice='calm', pause=0.5),
      L("Here too, we could put the numbers into the formula, but let's save ourselves that. We have a forty and a hundred "
        "twenty, and we know what part of the circle each one is.", show(f4g83['line'], 'Here too, we could')),
      L("[short pause] A hundred twenty degrees is a third of the circle. Forty degrees is a ninth, because three hundred "
        "sixty divided by nine is forty.", show(f4g83['third'], 'A hundred twenty degrees is a third'),
        show(f4g83['ninth'], 'Forty degrees is a ninth')),
      L("Together, that's a third plus a ninth. In ninths, a third is three ninths, and three ninths plus one ninth is four "
        "ninths. So the shaded part is four ninths of the circle's area.", show(f4g83['sum'], 'Together, that')),
      L("Now the area of the circle. Pi r squared is pi times three squared, which is nine pi. Careful, we need the area "
        "here, not the circumference. Four ninths of the circumference, six pi, would give eight pi over three, and that's "
        "choice number two, a trap.", show(f4g83['area'], 'Pi r squared is'), mk('cross', 'choice 2', 'a trap')),
      L("I don't need the whole circle, only four ninths of it. Nine pi divided by nine is pi, and four times that is four "
        "pi. Choice number three is our answer.", show(f4g83['ans'], 'Nine pi divided by nine'),
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("We can also take each sector separately. A ninth of nine pi is pi, and a third of nine pi is three pi. Together "
        "it's four pi again. Just don't stop at three pi, that's only the big sector. [pause] Okay. I'll see you in the next "
        "question.", show(f4g83['sep'], 'We can also take each sector'), mk('cross', 'choice 4', "that's only the big sector"))),
])

# =================================================================================================================
# Topic-33 fragment f5 (2026-10-14): geo-084 (the short intro "Circles in Questions") and the first four basic sample
# questions, geo33-g085 ... g088 (Hebrew "מעגלים יסודות לימוד", geo 3886-4088). Question figure on the left (FIG_LEFT,
# figw 0.56), our colour copy built in layers on the right (Rule V3); the working is written inside the copy (text rows
# beside or under the shape), so the layers stay consecutive. Every Hebrew method is kept.
# =================================================================================================================
FIG_LEFT.update({'solve-geo33-g085', 'solve-geo33-g086', 'solve-geo33-g087', 'solve-geo33-g088'})


def f5_ang(P, Q, R_, r, col, label=None, lr=None):
    """the inside angle at P between the rays P->Q and P->R_ (the smaller one)"""
    a, b = gdir(*P, *Q), gdir(*P, *R_)
    if (b - a) % 360 > 180: a, b = b, a
    e = ('arc', P[0], P[1], r, a, b, col)
    if label: e = e + (label,) + ((lr,) if lr else ())
    return e


def f5_rt(P, Q, R_, size=15, col='teal'):
    """the right-angle square at P between the rays P->Q and P->R_"""
    a, b = gdir(*P, *Q), gdir(*P, *R_)
    if (b - a) % 360 > 180: a, b = b, a
    return ('right', P[0], P[1], a, b, size, col)


def f5_s(P, Q, col='ink', w=3, dash=False):
    return ('seg', P[0], P[1], Q[0], Q[1], col, w, dash)


def f5_t(P, Q, n=1, col='teal'):
    return ('tick', P[0], P[1], Q[0], Q[1], n, col)


def f5_n(P, t, dx, dy, size=26):
    """a point name next to P"""
    return ('txt', P[0] + dx, P[1] + dy, t, 'ink', size, True)


def f5_poly(pts, col='ink', w=3):
    return [f5_s(pts[k], pts[(k + 1) % len(pts)], col, w) for k in range(len(pts))]


# ------------------------------------------------------------------------------------------------ geo-084 (lesson)
# Hebrew (geo 3886-3891): last lesson we learned the circle rules; now basic and advanced questions that use only these
# rules; let's start with a sample question. Kept from the course: the three rules that most questions come back to (as a
# short reminder, each on a clean generic circle, V3) and the idea of a helper line (taught in full in g088).
f5Lc1, f5Lc2, f5Lc3, f5LR = (160.0, 160.0), (480.0, 160.0), (800.0, 160.0), 115.0
f5LP, f5LQ = gpt(*f5Lc1, f5LR, 35), gpt(*f5Lc1, f5LR, 145)
f5LX, f5LY, f5LV = gpt(*f5Lc2, f5LR, 220), gpt(*f5Lc2, f5LR, 320), gpt(*f5Lc2, f5LR, 90)
f5LT = gpt(*f5Lc3, f5LR, 0)
f5L = PIN(GEO('f5L', [
    ('line', [('circ', *f5Lc1, f5LR), ('dot', *f5Lc1), f5_n(f5Lc1, 'O', 0, 24)]),
    ('p1', [f5_s(f5Lc1, f5LP), f5_s(f5Lc1, f5LQ), f5_s(f5LP, f5LQ), f5_t(f5Lc1, f5LP), f5_t(f5Lc1, f5LQ),
            ('txt', 160, 312, 'radii are equal', 'teal', 24)]),
    ('p1t', [('tint', [f5Lc1, f5LP, f5LQ], 'teal'), ('txt', 160, 344, 'an isosceles triangle', 'teal', 24)]),
    ('p2', [('circ', *f5Lc2, f5LR), ('dot', *f5Lc2), ('arcw', *f5Lc2, f5LR, 220, 320, 'teal'),
            f5_s(f5Lc2, f5LX), f5_s(f5Lc2, f5LY), f5_s(f5LV, f5LX), f5_s(f5LV, f5LY), ('dot', *f5LV)]),
    ('p2n', [f5_ang(f5Lc2, f5LX, f5LY, 26, 'large', '100°', 48), f5_ang(f5LV, f5LX, f5LY, 40, 'small', '50°', 62),
             ('txt', 480, 312, 'central = 2 × inscribed', 'ink', 24)]),
    ('p3', [('circ', *f5Lc3, f5LR), ('dot', *f5Lc3), ('seg', f5LT[0], 40, f5LT[0], 280, 'ink', 3), ('dot', *f5LT)]),
    ('p3r', [f5_s(f5Lc3, f5LT, 'teal', 3, True), ('right', f5LT[0], f5LT[1], 90, 180, 16),
             ('txt', 800, 312, 'radius ⊥ tangent', 'ink', 24), ('txt', 800, 344, 'a helper line', 'teal', 24)]),
], vb='20 25 940 340', w=1200, col=0, title='Three circle rules'))
video('geo-084', 'lesson', slides=[
    S('Circles in Questions',
      L("Circles in questions. In the last lessons we learned the rules of the circle.")),
    S('What we use',
      L("Now we'll practice exam questions, basic ones and a bit more advanced ones, that use only these rules. Try each "
        "question yourself first, and then watch the solution."),
      L("Most circle questions come back to a few rules. First, all the radii of a circle are equal. So two radii and the "
        "chord between them make an isosceles triangle. Isosceles triangles hide inside almost every circle.",
        show(f5L['line'], 'Most circle questions'), show(f5L['p1'], 'all the radii of a circle'),
        show(f5L['p1t'], 'make an isosceles triangle')),
      L("Second, a central angle is twice the inscribed angle on the same arc. A central angle of one hundred degrees "
        "gives an inscribed angle of fifty.", show(f5L['p2'], 'a central angle is twice'),
        show(f5L['p2n'], 'A central angle of one hundred')),
      L("And third, a radius to the point of tangency is perpendicular to the tangent, so we get ninety degrees.",
        show(f5L['p3'], 'And third'), show(f5L['p3r'], 'is perpendicular to the tangent')),
      L("Notice that this radius wasn't in the drawing. We added it ourselves. A line we add like this is called a helper "
        "line, and many circle questions only open up after we draw one. So watch for them in the solutions. Let's start "
        "with a sample question. [pause] Okay. I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ geo33-g085 (Hebrew: the first sample question)
# Hebrew (geo 3893-3922): angle AOC 120 -> the angle next to it 60 (completes to 180); in a circle isosceles triangles
# hide because the radii are equal: OB = OC; top angle 60 -> base angles share 120 -> 60 and 60; an isosceles triangle
# with a 60 angle is equilateral; AB is the diameter = two radii -> OB = 4 (English 10); the equilateral area formula
# "a-two-three-four", a squared root 3 over 4 -> 4 root 3 (English 25 root 3), choice 4. Added (short, as a safety net
# for a forgotten formula, the topic-31 way): the height cuts it into two gold triangles, base times height over two.
# V3: the copy with the 120; the 60 at O when found; the radii ticked and the triangle tinted when named isosceles; the
# base angles; the third tick (equilateral). Slide 2: the V3 enlarged cut-out (the small copy with the tinted triangle
# stays, the triangle pulled out big with the same labels, tint and 60s), the 10s written as found, the formula beside.
# Slide 3: the same cut-out, the dashed height, the gold half tinted, 5 and 5 root 3 written, base times height.
f5O5, f5R5 = (175.0, 172.0), 145.0
f5A5, f5B5, f5C5 = gpt(*f5O5, f5R5, 180), gpt(*f5O5, f5R5, 0), gpt(*f5O5, f5R5, 60)
f5g85 = PIN(GEO('f5g85', [
    ('line', [('circ', *f5O5, f5R5), f5_s(f5A5, f5B5), f5_s(f5O5, f5C5), f5_s(f5B5, f5C5), ('tint', [f5O5, f5B5, f5C5], 'ink'),
              ('dot', *f5O5), f5_n(f5A5, 'A', -18, 0), f5_n(f5B5, 'B', 18, 0), f5_n(f5C5, 'C', 12, -18), f5_n(f5O5, 'O', -14, 20),
              ('arc', *f5O5, 34, 60, 180, 'large', '120°', 62)]),
    ('adj', [('arc', *f5O5, 30, 0, 60, 'small', '60°', 58), ('txt', 470, 50, '180° − 120° = 60°', 'teal', 24)]),
    ('iso', [f5_t(f5O5, f5B5), f5_t(f5O5, f5C5), ('tint', [f5O5, f5B5, f5C5], 'teal'), ('txt', 470, 95, 'OB = OC  (radii)', 'ink', 24)]),
    ('base', [f5_ang(f5B5, f5O5, f5C5, 26, 'small', '60°', 52), f5_ang(f5C5, f5O5, f5B5, 26, 'small', '60°', 50),
              ('txt', 470, 140, '180° − 60° = 120°', 'ink', 24), ('txt', 470, 180, '120° ÷ 2 = 60°', 'teal', 24)]),
    ('eq', [f5_t(f5B5, f5C5), ('txt', 470, 230, 'all 60°: equilateral', 'teal', 24)]),
], vb='0 10 600 325', w=540, title='Circle with center O and triangle OBC'))
_R(f5g85, 200)
# the cut-out: a small copy (top left) and the triangle enlarged (right)
f5o5, f5r5 = (95.0, 100.0), 72.0
f5a5s, f5b5s, f5c5s = gpt(*f5o5, f5r5, 180), gpt(*f5o5, f5r5, 0), gpt(*f5o5, f5r5, 60)
f5O5b, f5B5b = (250.0, 290.0), (530.0, 290.0)
f5C5b = (390.0, 290.0 - 140.0 * 3 ** 0.5)
f5H5b = (390.0, 290.0)
f5small = [('circ', *f5o5, f5r5, 'ink', 2), f5_s(f5a5s, f5b5s, 'ink', 2), ('tint', [f5o5, f5b5s, f5c5s], 'teal'),
           f5_s(f5o5, f5b5s, 'teal', 3), f5_s(f5b5s, f5c5s, 'teal', 3), f5_s(f5c5s, f5o5, 'teal', 3), ('dot', *f5o5),
           f5_n(f5a5s, 'A', -14, 0, 20), f5_n(f5b5s, 'B', 14, 0, 20), f5_n(f5c5s, 'C', 10, -14, 20), f5_n(f5o5, 'O', -10, 16, 20)]
f5big = ([('tint', [f5O5b, f5B5b, f5C5b], 'teal')] + f5_poly([f5O5b, f5B5b, f5C5b], 'teal', 4)
         + [f5_n(f5O5b, 'O', -16, 16), f5_n(f5B5b, 'B', 16, 16), f5_n(f5C5b, 'C', 0, -20),
            f5_ang(f5O5b, f5B5b, f5C5b, 30, 'small', '60°', 58), f5_ang(f5B5b, f5O5b, f5C5b, 30, 'small', '60°', 58),
            f5_ang(f5C5b, f5O5b, f5B5b, 30, 'small', '60°', 56),
            f5_t(f5O5b, f5B5b), f5_t(f5B5b, f5C5b), f5_t(f5C5b, f5O5b)])
f5g85b = PIN(GEO('f5g85b', [
    ('line', f5small + f5big),
    ('r10', [('txt', 110, 210, 'AB = 20, r = 10', 'ink', 24), ('txt', 390, 316, '10', 'teal', 26)]),
    ('sides', [('txt', 296, 160, '10', 'teal', 26), ('txt', 484, 160, '10', 'teal', 26)]),
    ('f', [('txt', 110, 260, '10² · √3 / 4', 'ink', 26), ('txt', 110, 300, '= 100√3 / 4', 'ink', 26),
           ('txt', 110, 340, '= 25√3', 'red', 28)]),
], vb='0 15 600 345', w=540, title='Triangle OBC taken out and enlarged'))
_R(f5g85b, 200)
f5big3 = ([('tint', [f5O5b, f5B5b, f5C5b], 'teal')] + f5_poly([f5O5b, f5B5b, f5C5b], 'teal', 4)
          + [f5_n(f5O5b, 'O', -16, 16), f5_n(f5B5b, 'B', 16, 16), f5_n(f5C5b, 'C', 0, -20),
             f5_t(f5O5b, f5B5b), f5_t(f5B5b, f5C5b), f5_t(f5C5b, f5O5b),
             ('txt', 296, 160, '10', 'teal', 26), ('txt', 484, 160, '10', 'teal', 26)])
f5g85c = PIN(GEO('f5g85c', [
    ('line', f5small + f5big3),
    ('h', [f5_s(f5C5b, f5H5b, 'teal', 3, True), ('right', f5H5b[0], f5H5b[1], 90, 180, 14)]),
    ('half', [('tint', [f5O5b, f5H5b, f5C5b], 'orange'), ('txt', 320, 316, '5', 'orange', 26), ('txt', 460, 316, '5', 'teal', 26),
              f5_ang(f5O5b, f5B5b, f5C5b, 30, 'small', '60°', 58), f5_ang(f5C5b, f5O5b, f5H5b, 36, 'small', '30°', 62)]),
    ('hh', [('txt', 430, 205, '5√3', 'orange', 26), ('txt', 110, 210, 'short leg 5', 'orange', 24),
            ('txt', 110, 245, 'long leg 5√3', 'orange', 24)]),
    ('f', [('txt', 110, 295, '10 · 5√3 / 2', 'ink', 26), ('txt', 110, 335, '= 25√3', 'red', 28)]),
], vb='0 15 600 345', w=540, title='The height of the equilateral triangle'))
_R(f5g85c, 200)
video('solve-geo33-g085', 'solution', qid='geo33-g085', slides=[
    S('Equal radii',
      L("A B is a diameter of a circle with center O, and A B is twenty centimeters. Given: angle A O C is one hundred "
        "twenty degrees. What is the area of the shaded triangle O B C, in square centimeters?",
        pt('stem', 'A B is a diameter', 'hl', 10.0), voice='calm', pause=0.5),
      L("We want the area of a triangle, and we know one angle and one length. [short pause] Let's start with the first "
        "given, the angle, and see what it tells us about the triangle.", show(f5g85['line'], 'We want the area')),
      L("Angle A O C is one hundred twenty. A B is a straight line, so the angle next to it completes it to one hundred "
        "eighty. One hundred eighty minus one hundred twenty is sixty. So angle B O C is sixty degrees.",
        pt('fig: 120°', 'Angle A O C is one hundred twenty'), show(f5g85['adj'], 'So angle B O C is sixty')),
      L("Now notice something. Inside a circle, isosceles triangles usually hide, because all the radii are equal. O B and "
        "O C are both radii, so they're equal, and the shaded triangle is at least isosceles.",
        show(f5g85['iso'], 'O B and O C are both radii')),
      L("Its top angle, at O, is sixty. The three angles add up to one hundred eighty, so the two base angles share one "
        "hundred eighty minus sixty, which is one hundred twenty. They're equal, so each one is half of it, sixty.",
        show(f5g85['base'], 'so the two base angles share')),
      L("So all three angles are sixty. As we said in the triangles topic, an isosceles triangle with a sixty-degree "
        "angle is always equilateral.", show(f5g85['eq'], 'So all three angles are sixty'))),
    S('The area',
      L("[pause] Let's take the shaded triangle out and make it bigger, so it's easier to see.",
        show(f5g85b['line'], "Let's take the shaded triangle out")),
      L("Now the second given. A B is twenty, and A B is a diameter. A diameter is two radii, so one radius is twenty "
        "divided by two, which is ten. So O B is ten. And the triangle is equilateral, so all its sides are ten.",
        show(f5g85b['r10'], 'A diameter is two radii'), show(f5g85b['sides'], 'so all its sides are ten')),
      L("They ask for the area of an equilateral triangle with side ten. We have a formula for that. Remember the count, "
        "a-two-three-four. It's a squared, times root three, over four, where a is the side."),
      L("We put ten in place of a. Ten squared is one hundred, so we get one hundred root three, over four. One hundred "
        "over four is twenty-five, so the area is twenty-five root three. Choice number four is our answer.",
        show(f5g85b['f'], 'We put ten in place of a'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Without the formula',
      L("[pause] And if you don't remember the formula, there's another way. We already know the triangle is "
        "equilateral, with side ten. Let's draw its height, from C straight down to O B.",
        show(f5g85c['line'], "there's another way"), show(f5g85c['h'], "Let's draw its height")),
      L("In an equilateral triangle, the height cuts the base in half, so we get five and five. Each half is a gold "
        "triangle, thirty, sixty, ninety.", show(f5g85c['half'], 'so we get five and five')),
      L("Five is the short leg. The long leg is the short leg times root three, so the height is five root three.",
        show(f5g85c['hh'], 'so the height is five root three')),
      L("Now base times height, over two. Ten times five root three is fifty root three, and over two it's twenty-five "
        "root three. Again choice number four. [pause] Okay. I'll see you in the next question.",
        show(f5g85c['f'], 'Now base times height'), mk('tick', 'choice 4', 'Again choice number four'))),
])

# ------------------------------------------------------------------------------------------------ geo33-g086 (Hebrew: the second sample question)
# Hebrew (geo 3925-3962): two approaches, math and psychometric. Math: BAC is an inscribed angle on arc BC, BOC the
# central angle on the same arc -> twice it (Hebrew 60 -> equilateral; English 112 -> isosceles, not equilateral);
# OB = OC radii -> base angles (180 - 112) / 2 = 34; AB = AC -> base angles of ABC (180 - 56) / 2 = 62 (Hebrew 75);
# subtract: 62 - 34 = 28 (Hebrew 15), choice 1; "the math solution was quite short". Psychometric: symmetry and a helper
# line - the radius from O to A splits angle A into 28 and 28 (no need to prove: not a school exam, an easy question at
# the start of the section, no "cannot be determined" choice); triangle AOB isosceles (radii) -> x = 28; shorter, fewer
# calculations. The two traps 34 (choice 2) and 62 (choice 3) are named at their step.
# V3: the copy with 56 and x; arc BC thick when named, then the central 112; triangle BOC tinted with the radii ticked,
# its base angles 34. Slide 2: a fresh copy with 34 carried; AB, AC with a double tick; the whole angle B (orange) 62;
# x = 28 written. Slide 3: a fresh copy; the dashed radius OA; the two halves at A with matching arcs; triangle AOB
# tinted, OA and OB ticked; x = 28.
f5O6, f5R6 = (175.0, 172.0), 145.0
f5A6, f5B6, f5C6 = gpt(*f5O6, f5R6, 270), gpt(*f5O6, f5R6, 50), gpt(*f5O6, f5R6, 130)
f5q86 = ([('circ', *f5O6, f5R6)] + f5_poly([f5A6, f5B6, f5C6]) + [f5_s(f5O6, f5B6), f5_s(f5O6, f5C6), ('dot', *f5O6),
         f5_n(f5A6, 'A', 0, 22), f5_n(f5B6, 'B', 12, -16), f5_n(f5C6, 'C', -12, -16), f5_n(f5O6, 'O', 0, 22),
         f5_ang(f5A6, f5B6, f5C6, 44, 'small', '56°', 70)])
f5x86 = f5_ang(f5B6, f5A6, f5O6, 40, 'red', 'x', 62)
f5g86 = PIN(GEO('f5g86', [
    ('line', f5q86 + [f5x86]),
    ('arc', [('arcw', *f5O6, f5R6, 50, 130, 'teal')]),
    ('cent', [('arc', *f5O6, 30, 50, 130, 'large', '112°', 54), ('txt', 470, 60, '2 · 56° = 112°', 'orange', 24)]),
    ('iso', [('tint', [f5O6, f5B6, f5C6], 'teal'), f5_t(f5O6, f5B6), f5_t(f5O6, f5C6), ('txt', 470, 105, 'OB = OC  (radii)', 'ink', 24)]),
    ('b34', [f5_ang(f5B6, f5C6, f5O6, 26, 'small', '34°', 50), f5_ang(f5C6, f5B6, f5O6, 26, 'small', '34°', 50),
             ('txt', 470, 150, '180° − 112° = 68°', 'ink', 24),
             ('txt', 470, 190, '68° ÷ 2 = 34°', 'teal', 24)]),
], vb='0 15 600 345', w=540, title='Isosceles triangle ABC in a circle with center O'))
_R(f5g86, 200)
f5g86b = PIN(GEO('f5g86b', [
    ('line', f5q86 + [f5x86, f5_t(f5O6, f5B6), f5_t(f5O6, f5C6), f5_ang(f5B6, f5C6, f5O6, 26, 'small', '34°', 50),
                      f5_ang(f5C6, f5B6, f5O6, 26, 'small', '34°', 50)]),
    ('abac', [f5_t(f5A6, f5B6, 2, 'orange'), f5_t(f5A6, f5C6, 2, 'orange')]),
    ('b62', [f5_ang(f5B6, f5A6, f5C6, 92, 'large'), ('txt', 185, 136, '62°', 'orange', 24),
             ('txt', 470, 60, '180° − 56° = 124°', 'ink', 24), ('txt', 470, 100, '124° ÷ 2 = 62°', 'orange', 24)]),
    ('x', [('txt', 470, 150, 'x = 62° − 34°', 'red', 26), ('txt', 470, 190, 'x = 28°', 'red', 28)]),
], vb='0 15 600 345', w=540, title='Isosceles triangle ABC: the whole angle at B'))
_R(f5g86b, 200)
f5q86c = [x for x in f5q86 if not (x[0] == 'txt' and x[3] == 'O') and x[0] != 'arc'] + [
    f5_n(f5O6, 'O', -20, 8), f5_ang(f5A6, f5B6, f5C6, 44, 'small')]
f5g86c = PIN(GEO('f5g86c', [
    ('line', f5q86c + [f5x86]),
    ('oa', [f5_s(f5O6, f5A6, 'teal', 3, True)]),
    ('split', [f5_ang(f5A6, f5B6, f5O6, 64, 'small'), f5_ang(f5A6, f5O6, f5C6, 72, 'small'),
               ('txt', 222, 262, '28°', 'teal', 22), ('txt', 128, 262, '28°', 'teal', 22),
               ('txt', 470, 60, '56° ÷ 2 = 28°', 'teal', 24)]),
    ('aob', [('tint', [f5A6, f5O6, f5B6], 'teal'), f5_t(f5O6, f5A6), f5_t(f5O6, f5B6), ('txt', 470, 105, 'OA = OB  (radii)', 'ink', 24)]),
    ('x', [('txt', 470, 150, 'x = 28°', 'red', 28)]),
], vb='0 15 600 345', w=540, title='The radius OA cuts the angle at A in half'))
_R(f5g86c, 200)
video('solve-geo33-g086', 'solution', qid='geo33-g086', slides=[
    SM('Method 1 · The math way', 'The central angle',
      L("An isosceles triangle A B C is inscribed in a circle with center O, and A B equals A C. Given: angle B A C is "
        "fifty-six degrees. What is angle A B O?", pt('stem', 'An isosceles triangle', 'hl', 8.0), voice='calm', pause=0.5),
      L("Angle A B O is the angle marked x, at B, between B A and the radius B O. [short pause] There are two ways to "
        "solve this, a math way and a shorter psychometric way. Let's start with the math way.",
        show(f5g86['line'], 'Angle A B O is the angle marked x')),
      L("Angle B A C is an inscribed angle, and it intercepts the arc B C. Angle B O C is a central angle, and it "
        "intercepts the same arc.", show(f5g86['arc'], 'it intercepts the arc B C')),
      L("Remember, a central angle is twice the inscribed angle on the same arc. So angle B O C is two times fifty-six, "
        "which is one hundred twelve.", show(f5g86['cent'], 'So angle B O C is two times')),
      L("Now look at triangle B O C. O B and O C are both radii, so they're equal, and the triangle is isosceles. This "
        "time the top angle is one hundred twelve, not sixty, so it isn't equilateral.",
        show(f5g86['iso'], 'Now look at triangle B O C')),
      L("The two base angles share one hundred eighty minus one hundred twelve, which is sixty-eight. Half of sixty-eight "
        "is thirty-four. So angle O B C is thirty-four, and so is angle O C B.", show(f5g86['b34'], 'Half of sixty-eight')),
      L("Careful, thirty-four is angle O B C, not our x. It's choice number two, and it's a trap if you stop here.",
        mk('cross', 'choice 2', "It's choice number two"))),
    SM('Method 1 · The math way', 'Subtract at B',
      L("[pause] Now let's use the given we haven't used yet. A B equals A C, so triangle A B C is isosceles, and its base "
        "angles, at B and at C, are equal.", show(f5g86b['line'], 'Now let\'s use the given'),
        show(f5g86b['abac'], 'A B equals A C, so triangle')),
      L("The top angle is fifty-six. So the angles at B and C share one hundred eighty minus fifty-six, which is one "
        "hundred twenty-four. Half of one hundred twenty-four is sixty-two. So the whole angle A B C is sixty-two.",
        show(f5g86b['b62'], 'Half of one hundred twenty-four')),
      L("The whole angle at B is sixty-two, and its lower part, O B C, is thirty-four. So x is what's left, sixty-two minus "
        "thirty-four, which is twenty-eight. Choice number one is our answer. Notice that sixty-two, choice number three, "
        "is the whole angle, not x.", show(f5g86b['x'], 'So x is what\'s left'),
        mk('tick', 'choice 1', 'Choice number one is our answer'), mk('cross', 'choice 3', 'choice number three'))),
    SM('Method 2 · Understanding: symmetry', 'Symmetry',
      L("[pause] The math solution was quite short. Now the psychometric solution. It uses symmetry and a helper line.",
        show(f5g86c['line'], 'Now the psychometric solution')),
      L("From the center O, let's draw a radius to the vertex A.", show(f5g86c['oa'], "let's draw a radius")),
      L("Triangle A B C is isosceles, and an isosceles triangle is symmetric. So the radius O A cuts the angle at A into "
        "two equal parts. Fifty-six divided by two is twenty-eight, so we get twenty-eight and twenty-eight.",
        show(f5g86c['split'], 'Fifty-six divided by two')),
      L("We don't need to prove it. This isn't a school math exam. It's an easy question early in the section, and none "
        "of the choices says the answer can't be found. So we can trust the symmetry."),
      L("Now look at triangle A O B. O A and O B are both radii, so it's isosceles too, and its base angles are equal. So "
        "x equals angle O A B, which is twenty-eight. Choice number one again. This way is shorter, with fewer "
        "calculations. [pause] Okay. I'll see you in the next question.", show(f5g86c['aob'], 'Now look at triangle A O B'),
        show(f5g86c['x'], 'So x equals angle O A B'), mk('tick', 'choice 1', 'Choice number one again'))),
])

# ------------------------------------------------------------------------------------------------ geo33-g087 (Hebrew: the third sample question)
# Hebrew (geo 3964-4027): go statement by statement, look for the one that is surely false; anything always true or
# possible is out; hope to be left with one. (1) DAE = alpha, CAD = beta, inscribed angles on the equal chords ED and DC
# -> equal, out. (2) BOC = x, a central angle on chord BC; equal chords -> equal central angles, all four are x; 4x = 180,
# halve twice (90, 45), out. (3) ADE: an inscribed angle on the diameter is always 90 (half of 180), out. On the exam: mark
# the fourth and move on; in the lesson we check: triangle AOC, AO = OC = 1 (English 5), angle AOC = 45 + 45 = 90 -> the
# silver triangle, hypotenuse = leg times root 2 -> AC = root 2 (5 root 2), not root 3 (the gold triangle's ratio).
# V3: a fresh copy per statement (same orientation and labels). (1) alpha and beta drawn at A with matching teal arcs,
# then the arcs DE and CD they intercept thickened. (2) the radii OB, OC, OD drawn dashed (not in the figure), the four
# central angles marked x, the sum written beside. (3) the diameter AE thickened, the right angle at D. (4) the dashed OC,
# triangle AOC tinted, 5 and 5, the right angle at O, AC thickened red with 5 root 2.
f5O7, f5R7 = (175.0, 172.0), 145.0
f5A7, f5B7, f5C7, f5D7, f5E7 = [gpt(*f5O7, f5R7, d) for d in (180, 135, 90, 45, 0)]
f5q87 = ([('circ', *f5O7, f5R7), f5_s(f5A7, f5E7)] + f5_poly([f5A7, f5B7, f5C7, f5D7, f5E7])[:4]
         + [f5_s(f5A7, f5C7), f5_s(f5A7, f5D7), ('dot', *f5O7)]
         + [('tick', *f5A7, *f5B7, 1, 'ink'), ('tick', *f5B7, *f5C7, 1, 'ink'), ('tick', *f5C7, *f5D7, 1, 'ink'), ('tick', *f5D7, *f5E7, 1, 'ink')]
         + [f5_n(f5A7, 'A', -18, 0), f5_n(f5B7, 'B', -12, -14), f5_n(f5C7, 'C', 0, -18), f5_n(f5D7, 'D', 12, -14),
            f5_n(f5E7, 'E', 18, 0), f5_n(f5O7, 'O', -12, 20), ('txt', 102, 192, '5', 'ink', 24)])
f5V7 = '0 -10 600 340'
f5g87a = PIN(GEO('f5g87a', [
    ('line', f5q87),
    ('al', [f5_ang(f5A7, f5E7, f5D7, 120, 'small', 'α', 142)]),
    ('be', [f5_ang(f5A7, f5D7, f5C7, 120, 'small', 'β', 142)]),
    ('arcs', [('arcw', *f5O7, f5R7, 0, 45, 'teal'), ('arcw', *f5O7, f5R7, 45, 90, 'teal'),
              ('txt', 470, 60, 'DE = CD', 'ink', 24), ('txt', 470, 100, 'equal arcs', 'teal', 24), ('txt', 470, 140, 'α = β  ✓ true', 'teal', 26)]),
], vb=f5V7, w=540, title='Circle with diameter AE and four equal chords'))
_R(f5g87a, 200)
f5g87b = PIN(GEO('f5g87b', [
    ('line', f5q87),
    ('rad', [f5_s(f5O7, f5B7, 'teal', 3, True), f5_s(f5O7, f5C7, 'teal', 3, True), f5_s(f5O7, f5D7, 'teal', 3, True)]),
    ('xs', [('arc', *f5O7, 30, 0, 45, 'small', 'x', 50), ('arc', *f5O7, 30, 45, 90, 'small', 'x', 50),
            ('arc', *f5O7, 30, 90, 135, 'small', 'x', 50), ('arc', *f5O7, 30, 135, 180, 'small', 'x', 50)]),
    ('sum', [('txt', 470, 60, '4x = 180°', 'ink', 26), ('txt', 470, 100, '180 ÷ 2 = 90', 'ink', 24),
             ('txt', 470, 140, '90 ÷ 2 = 45', 'ink', 24), ('txt', 470, 185, 'x = 45°  ✓ true', 'teal', 26)]),
], vb=f5V7, w=540, title='The four central angles'))
_R(f5g87b, 200)
f5g87c = PIN(GEO('f5g87c', [
    ('line', f5q87),
    ('ade', [f5_s(f5D7, f5E7, 'teal', 4), f5_s(f5D7, f5A7, 'teal', 4)]),
    ('diam', [f5_s(f5A7, f5E7, 'orange', 6), ('txt', 470, 60, 'on the diameter AE', 'orange', 24)]),
    ('r90', [f5_rt(f5D7, f5A7, f5E7, 16), ('txt', 470, 100, '180° ÷ 2 = 90°', 'ink', 24), ('txt', 470, 145, 'ADE = 90°  ✓ true', 'teal', 26)]),
], vb=f5V7, w=540, title='The angle ADE on the diameter'))
_R(f5g87c, 200)
f5g87d = PIN(GEO('f5g87d', [
    ('line', f5q87),
    ('oc', [f5_s(f5O7, f5C7, 'teal', 3, True)]),
    ('aoc', [('tint', [f5A7, f5O7, f5C7], 'teal'), ('txt', 158, 100, '5', 'teal', 24), ('txt', 102, 192, '5', 'teal', 24),
             ('right', *f5O7, 90, 180, 14),
             ('txt', 470, 60, '45° + 45° = 90°', 'ink', 24)]),
    ('silver', [('txt', 470, 105, 'silver: 5, 5, 5√2', 'teal', 24)]),
    ('ac', [f5_s(f5A7, f5C7, 'red', 5), ('txt', 92, 84, '5√2', 'red', 22), ('txt', 470, 150, 'AC = 5√2', 'red', 26),
            ('txt', 470, 190, 'not 5√3  ✗', 'red', 26)]),
], vb=f5V7, w=540, title='Triangle AOC'))
_R(f5g87d, 200)
video('solve-geo33-g087', 'solution', qid='geo33-g087', slides=[
    S('Statement 1',
      L("A E is a diameter of a circle with center O. B, C and D lie on the same semicircle, in that order. Given: A B, B "
        "C, C D and D E are all equal, and A O is five centimeters. Which of the following statements is not true?",
        pt('stem', 'A E is a diameter', 'hl', 11.0), voice='calm', pause=0.5),
      L("We're looking for the one statement that is surely not true. [short pause] So we go statement by statement. A "
        "statement that's always true, or even possible, is out, and we hope to be left with one.",
        show(f5g87a['line'], 'So we go statement by statement')),
      L("Statement one. Angle D A E equals angle C A D. Lots of letters, so let's go slowly. D A E is the angle at A "
        "between A E and A D. Let's call it alpha.", pt('choice 1', 'Statement one'), show(f5g87a['al'], "Let's call it alpha")),
      L("C A D is the angle at A between A D and A C. Let's call it beta.", show(f5g87a['be'], "Let's call it beta")),
      L("Both are inscribed angles. Alpha intercepts the arc D E, and beta intercepts the arc C D. The chords D E and C D "
        "are equal, so their arcs are equal too. And inscribed angles on equal arcs are equal. So alpha equals beta.",
        show(f5g87a['arcs'], 'Alpha intercepts the arc')),
      L("Statement one is surely true, so choice number one is out.", mk('cross', 'choice 1', 'so choice number one is out'))),
    S('Statement 2',
      L("[pause] Statement two. Angle B O C is forty-five degrees. Let's call it x. Its vertex is at the center, so it's a "
        "central angle. To see it, let's draw the radii from O to B, to C and to D.", pt('choice 2', 'Statement two'),
        show(f5g87b['line'], "Let's call it x"), show(f5g87b['rad'], "let's draw the radii")),
      L("Equal chords give equal central angles. All four chords are equal, so all four central angles are x.",
        show(f5g87b['xs'], 'so all four central angles are x')),
      L("Together, the four angles make the straight angle A O E, one hundred eighty degrees. So four x is one hundred "
        "eighty. To divide by four, you can halve twice. Half of one hundred eighty is ninety, and half of ninety is "
        "forty-five. So x really is forty-five, and choice number two is out.", show(f5g87b['sum'], 'So four x is'),
        mk('cross', 'choice 2', 'and choice number two is out'))),
    S('Statement 3',
      L("[pause] Statement three. Angle A D E is ninety degrees. That's the angle at D, between D A and D E.",
        pt('choice 3', 'Statement three'), show(f5g87c['line'], 'Angle A D E is ninety'), show(f5g87c['ade'], "That's the angle at D")),
      L("It's an inscribed angle that lies on the diameter A E. An inscribed angle on a diameter is always ninety, because "
        "it's half of the central angle, and the central angle on a diameter is a straight angle, one hundred eighty. So "
        "it's true, and choice number three is out.", show(f5g87c['diam'], 'lies on the diameter'),
        show(f5g87c['r90'], 'An inscribed angle on a diameter'), mk('cross', 'choice 3', 'and choice number three is out')),
      L("On the exam, we're done. Three statements are out, so you mark choice number four and move on. There's no time to "
        "check it.", mk('tick', 'choice 4', 'so you mark choice number four'))),
    S('Check A C',
      L("[pause] But we're in a lesson, so let's check it. Is A C five root three? Look at triangle A O C. We need O C, so "
        "let's draw it, from O to C.", show(f5g87d['line'], "so let's check it"), show(f5g87d['oc'], "let's draw it")),
      L("A O is a radius, five. O C is a radius too, so it's also five. And angle A O C is forty-five plus forty-five, "
        "which is ninety.", show(f5g87d['aoc'], 'A O is a radius')),
      L("So triangle A O C is a right triangle with two equal legs. That's the silver triangle, forty-five, forty-five, "
        "ninety. In the silver triangle, the hypotenuse is the leg times root two.",
        show(f5g87d['silver'], "That's the silver triangle")),
      L("So A C is five root two, not five root three. Root three belongs to the gold triangle. So statement four is the "
        "one that's not true. Choice number four is our answer. [pause] Okay. I'll see you in the next question.",
        show(f5g87d['ac'], 'So A C is five root two'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo33-g088 (Hebrew: the fourth sample question)
# Hebrew (geo 4029-4087): no number at all; start from the givens; two tangents from M are equal and with the radii to
# the points of tangency make a kite; there's no kite yet -> a helper line (what it is: our own addition to the drawing);
# one of the most common: the radius to the point of tangency, perpendicular to the tangent -> 90 and 90; the kite's other
# two angles share 180, not enough; the unused given (congruent, touching) -> a second, less common helper line: join the
# centers, r + r = 2r (English 7 + 7 = 14); right triangle OAM, leg r, hypotenuse 2r: it must be a triangle we know,
# silver or gold; the hypotenuse exactly twice the leg only in the gold triangle -> 30 opposite the short leg; the lower
# triangle OBM the same. Hebrew asks the angle at M (60); the English asks angle AOB: 60 + 60 = 120, or the kite: 360 -
# 90 - 90 - 60 = 120 (the course's route kept). Her closing recap (two helper lines, the gold triangle backwards) kept.
# The course's line "inside each other, R minus r" kept as one sentence.
# V3: the copy of the two circles; the equal tangents ticked; the radii OA, OB dashed teal with the right angles and 7s;
# the kite tinted. Slide 2: a fresh copy with the radii carried; OM dashed (its ends named first), the touching point,
# 7 + 7. Slide 3: triangle OAM tinted, 30 at M; the lower triangle tinted, 30. Slide 4: the 60s at O, 120; the kite way.
f5O8, f5M8, f5r8 = (210.5, 180.0), (429.5, 180.0), 109.5
f5A8, f5B8, f5T8 = gpt(*f5O8, f5r8, 60), gpt(*f5O8, f5r8, 300), (320.0, 180.0)
f5q88 = [('circ', *f5O8, f5r8), ('circ', *f5M8, f5r8), f5_s(f5M8, f5A8), f5_s(f5M8, f5B8), ('dot', *f5O8), ('dot', *f5M8),
         f5_n(f5O8, 'O', -13, 20), f5_n(f5M8, 'M', 15, 20), f5_n(f5A8, 'A', -10, -21), f5_n(f5B8, 'B', -10, 21)]
f5rad8 = [f5_s(f5O8, f5A8, 'teal', 3, True), f5_s(f5O8, f5B8, 'teal', 3, True), f5_rt(f5A8, f5O8, f5M8, 13), f5_rt(f5B8, f5O8, f5M8, 13)]
f5sev8 = [('txt', 222, 124, '7', 'teal', 24), ('txt', 222, 236, '7', 'teal', 24)]
f5om8 = [f5_s(f5O8, f5M8, 'teal', 3, True), ('dot', *f5T8)]
f5V8 = '85 40 470 360'
f5g88 = PIN(GEO('f5g88', [
    ('line', f5q88),
    ('eq', [f5_t(f5M8, f5A8, 1, 'orange'), f5_t(f5M8, f5B8, 1, 'orange'), ('txt', 320, 325, 'MA = MB', 'orange', 24)]),
    ('rad', f5rad8 + f5sev8),
    ('kite', [('tint', [f5O8, f5A8, f5M8, f5B8], 'teal'), ('txt', 320, 360, '90° + 90° = 180°:  O + M = 180°', 'ink', 24)]),
], vb=f5V8, w=520, title='Two congruent circles that touch'))
_R(f5g88, 200)
f5g88b = PIN(GEO('f5g88b', [
    ('line', f5q88 + f5rad8 + f5sev8),
    ('om', f5om8),
    ('om7', [('txt', 265, 197, '7', 'teal', 24), ('txt', 375, 166, '7', 'teal', 24), ('txt', 320, 335, 'OM = 7 + 7 = 14', 'teal', 26)]),
], vb=f5V8, w=520, title='The line between the centers'))
_R(f5g88b, 200)
f5g88c = PIN(GEO('f5g88c', [
    ('line', f5q88 + f5rad8 + f5sev8 + f5om8 + [('txt', 286, 197, '14', 'teal', 24)]),
    ('tri', [('tint', [f5O8, f5A8, f5M8], 'teal'), ('txt', 320, 335, 'leg 7, hypotenuse 14 = 2 · 7', 'ink', 24)]),
    ('m30', [('arc', *f5M8, 56, 150, 180, 'small', '30°', 84), ('txt', 320, 372, 'gold: 30°, 60°, 90°', 'teal', 24)]),
    ('low', [('tint', [f5O8, f5B8, f5M8], 'teal'), ('arc', *f5M8, 56, 180, 210, 'small', '30°', 84)]),
], vb=f5V8, w=520, title='Two right triangles OAM and OBM'))
_R(f5g88c, 200)
f5g88d = PIN(GEO('f5g88d', [
    ('line', f5q88 + f5rad8 + f5sev8 + f5om8 + [('arc', *f5M8, 56, 150, 180, 'small', '30°', 84),
                                                ('arc', *f5M8, 56, 180, 210, 'small', '30°', 84)]),
    ('o60', [('arc', *f5O8, 36, 0, 60, 'small', '60°', 60), ('arc', *f5O8, 36, 300, 360, 'small', '60°', 60)]),
    ('aob', [('arc', *f5O8, 24, 300, 60, 'large'), ('txt', 320, 335, 'AOB = 60° + 60° = 120°', 'red', 26)]),
    ('kite', [('tint', [f5O8, f5A8, f5M8, f5B8], 'teal'), ('txt', 320, 372, '360° − 90° − 90° − 60° = 120°', 'ink', 24)]),
], vb=f5V8, w=520, title='The angle AOB'))
_R(f5g88d, 200)
video('solve-geo33-g088', 'solution', qid='geo33-g088', slides=[
    S('Radius to the tangent',
      L("Two congruent circles, with centers O and M, touch each other from the outside. Each one has a radius of seven "
        "centimeters. M A and M B are tangent to the circle with center O, at A and B. What is the smaller angle A O B?",
        pt('stem', 'Two congruent circles', 'hl', 11.0), voice='calm', pause=0.5),
      L("We need an angle, but the only number we have is a length, the radius seven. [short pause] It's not clear yet how "
        "we'll get there, so let's start from the givens and see what each one gives us.",
        show(f5g88['line'], 'We need an angle')),
      L("M A and M B are two tangents that come out of the same point, M. Remember, two tangents from the same point are "
        "equal. And together with the radii to the points of tangency, they make a kite.",
        show(f5g88['eq'], 'two tangents from the same point are')),
      L("But right now there's no kite in the drawing, because the radii aren't there. We need a helper line. A helper "
        "line is something we add to the drawing ourselves, so that we can solve the question. One of the most common "
        "helper lines is a radius to the point of tangency."),
      L("So let's draw the radius from O to A, and from O to B. Both are seven. A radius to the point of tangency is "
        "perpendicular to the tangent, so we get ninety degrees at A, and ninety at B.",
        show(f5g88['rad'], "So let's draw the radius")),
      L("Now we have a kite. Its angles add up to three hundred sixty. Ninety plus ninety is one hundred eighty, so the "
        "angles at O and at M share the other one hundred eighty. But we can't split it yet, so it's still not enough.",
        show(f5g88['kite'], 'Now we have a kite'))),
    S('Join the centers',
      L("[pause] There's a given we haven't used. The two circles are congruent, and they touch each other. To use it, we "
        "need a second helper line. It's less common, but this question asks for it. We join the two centers, O and M.",
        show(f5g88b['line'], "There's a given we haven't used"), show(f5g88b['om'], 'We join the two centers')),
      L("When two circles touch, the touching point lies on the line between the centers. So the first part of O M is a "
        "radius of circle O, seven. The second part is a radius of circle M, and the circles are congruent, so it's seven "
        "too. So O M is seven plus seven, which is fourteen.", show(f5g88b['om7'], 'So the first part of O M')),
      L("By the way, if one circle sat inside the other and they touched, the distance between the centers would be the "
        "big radius minus the small one.")),
    S('A gold triangle',
      L("[pause] Now look at the right triangle O A M. One leg, O A, is seven, and the hypotenuse, O M, is fourteen.",
        show(f5g88c['line'], 'Now look at the right triangle'), show(f5g88c['tri'], 'One leg, O A, is seven')),
      L("To get an angle from the sides, it has to be a triangle we know, the silver one or the gold one. In the silver "
        "triangle, the hypotenuse is the leg times root two. In the gold triangle, thirty, sixty, ninety, the sides are x, "
        "x root three and two x. So the hypotenuse is exactly twice the short leg."),
      L("Here the hypotenuse is exactly twice the leg, fourteen and seven. That only happens in the gold triangle. So O A "
        "is the short leg, and the angle across from it, at M, is thirty degrees.",
        show(f5g88c['m30'], 'the angle across from it')),
      L("The lower triangle, O B M, is the same triangle, so the angle at M there is thirty too. This time we went "
        "backwards, from the sides to the angle.", show(f5g88c['low'], 'The lower triangle'))),
    S('Angle A O B',
      L("[pause] In each gold triangle, the angles are thirty, sixty and ninety. The thirty is at M and the ninety is at A, "
        "so the sixty is at O. It's the same in both triangles.", show(f5g88d['line'], 'In each gold triangle'),
        show(f5g88d['o60'], 'so the sixty is at O')),
      L("So angle A O B is sixty plus sixty, which is one hundred twenty. Choice number three is our answer. Sixty, choice "
        "number one, is only half of the angle.", show(f5g88d['aob'], 'So angle A O B is sixty plus sixty'),
        mk('tick', 'choice 3', 'Choice number three is our answer'), mk('cross', 'choice 1', 'Sixty, choice')),
      L("You can also finish with the kite. The angle at M is thirty plus thirty, which is sixty. The kite's angles add up "
        "to three hundred sixty. Three hundred sixty minus ninety and ninety is one hundred eighty, and minus sixty is one "
        "hundred twenty. The same answer.", show(f5g88d['kite'], 'You can also finish with the kite')),
      L("So again, what did we do? We needed two helper lines. A very common one, the radius to the point of tangency, and "
        "a less common one that this question asked for, the line between the centers. And we spotted a gold triangle from "
        "its sides. [pause] Okay. I'll see you in the next question.")),
])

# =================================================================================================================
# Topic-33 fragment f6 (TAG F, 2026-10-14): geo33-g089 ... g092, the last four sample questions of the Hebrew basic
# circles practice ("מעגלים יסודות לימוד", geo 4090-4258). Question figure on the left (FIG_LEFT), our colour copy built in
# layers on the right (Rule V3); the typed working is written beside the figure inside the copy (text layers), so the
# layers stay consecutive. Every Hebrew method is kept, with the course's new numbers.
# =================================================================================================================
FIG_LEFT.update({'solve-geo33-g089', 'solve-geo33-g090', 'solve-geo33-g091', 'solve-geo33-g092'})


def f6_ring(cx1, cy1, r1, cx2, cy2, r2):
    """the svg path of a ring (big circle minus small circle, even-odd)"""
    def c(cx, cy, r):
        return 'M %.1f %.1f a %.1f %.1f 0 1 0 %.1f 0 a %.1f %.1f 0 1 0 %.1f 0 Z ' % (cx - r, cy, r, r, 2 * r, r, r, -2 * r)
    return c(cx1, cy1, r1) + c(cx2, cy2, r2)


def f6_row(y, t, col='ink', size=23, x=572):
    return ('txt', x, y, t, col, size)


def f6_name(p, t, dx, dy, size=24):
    return ('txt', p[0] + dx, p[1] + dy, t, 'ink', size, True)


def f6_seg(p, q, col='ink', w=3, dash=False):
    return ('seg', p[0], p[1], q[0], q[1], col, w, dash)


# ------------------------------------------------------------------------------------------------ geo33-g089 (Hebrew: the ring)
# Hebrew (geo 4091-4130): first given, the small circle's circumference -> can we find the radius? yes: 2πr = 6π, cancel
# π, two radii = the diameter = 6, r = 3; its area πr² = 9π, the white circle; second given, the dark area 16π -> the whole
# big circle 9π + 16π = 25π; from the area the radius: cancel π, r² = 25, r = 5, "remember it"; what was asked: 2πr = 10π;
# not in the choices -> they want an estimate; π is 3.14, going on forever; 10 · 3.14 = 31.4 -> between 31 and 32.
# English numbers: 10π, 39π -> r = 5, 25π, 64π, R = 8, 16π ≈ 50.24 -> between 50 and 51 (16 · 3.14 by 16 · 3 + 16 · 0.14;
# the π = 3 trap gives exactly 48, choice 1).
# V3: the ring tinted grey as given; the small circle outlined teal at its circumference, its dashed radius with 5; the
# small disc tinted teal with 25π; the ring tinted orange with it, so the whole large disc is coloured; the large dashed
# radius with 8; the working typed beside the figure, row by row.
f6BO, f6BR, f6SO, f6SR = (320.0, 180.0), 109.5, (338.25, 170.875), 48.667
f6g89 = PIN(GEO('f6g89', [
    ('line', [('region', f6_ring(f6BO[0], f6BO[1], f6BR, f6SO[0], f6SO[1], f6SR), 'ink', 0.16),
              ('circ', f6BO[0], f6BO[1], f6BR), ('circ', f6SO[0], f6SO[1], f6SR), ('txt', 252, 168, '39π', 'ink', 22)]),
    ('small', [('circ', f6SO[0], f6SO[1], f6SR, 'teal', 6), f6_row(66, '2πr = 10π', 'teal')]),
    ('r5', [('dot', f6SO[0], f6SO[1]), f6_seg(f6SO, (f6SO[0] + f6SR, f6SO[1]), 'teal', 4, True), ('txt', 363, 154, '5', 'teal', 26),
            f6_row(97, '2r = 10,  r = 5', 'teal')]),
    ('s25', [('circ', f6SO[0], f6SO[1], f6SR, 'teal', 0, False, 'teal'), ('txt', 336, 198, '25π', 'teal', 22),
             f6_row(128, 'π · 5² = 25π', 'teal')]),
    ('big', [('region', f6_ring(f6BO[0], f6BO[1], f6BR, f6SO[0], f6SO[1], f6SR), 'orange', 0.3)]),
    ('b64', [f6_row(159, '25π + 39π = 64π', 'orange')]),
    ('r8', [('dot', f6BO[0], f6BO[1]), f6_seg(f6BO, gpt(f6BO[0], f6BO[1], f6BR, 235), 'red', 4, True), ('txt', 272, 213, '8', 'red', 26),
            f6_row(190, 'πR² = 64π → R = 8', 'red')]),
    ('c16', [f6_row(221, 'C = 2π · 8 = 16π')]),
    ('est', [f6_row(252, '16 · 3.14 = 50.24', 'teal'), f6_row(283, 'between 50 and 51', 'teal')]),
    ('trap', [f6_row(314, 'π = 3?  48  ✗', 'red')]),
], vb='200 46 500 286', w=540, title='The small circle inside the large circle'))
_R(f6g89, 360)
video('solve-geo33-g089', 'solution', qid='geo33-g089', slides=[
    SM('From the small circle to the large one', 'From the small circle to the large one',
      L("The circumference of the smaller circle is ten pi centimeters, and the shaded area, inside the larger circle but "
        "outside the smaller one, is thirty-nine pi square centimeters. Between which two values is the circumference of "
        "the larger circle, in centimeters?", pt('stem', 'The circumference of the smaller circle', 'hl', 11.0), voice='calm', pause=0.5),
      L("We need the circumference of the large circle, so we need its radius. [short pause] We'll go from the small "
        "circle to the large one, one given at a time.", show(f6g89['line'], 'We need the circumference')),
      L("[short pause] Let's start with the first given. The circumference of the small circle is ten pi. If we know a "
        "circle's circumference, can we find its radius? Yes. The circumference is two pi r, so two pi r equals ten pi.",
        show(f6g89['small'], 'so two pi r equals ten pi')),
      L("We can cancel pi on both sides, so two r is ten. Two radii make a diameter, so the diameter is ten, and the "
        "radius is five. That's the radius of the small circle.", show(f6g89['r5'], 'and the radius is five')),
      L("Now its area. The area of a circle is pi r squared. Pi times five squared is twenty-five pi. That's the area of "
        "the small white circle.", show(f6g89['s25'], 'Pi times five squared')),
      L("On to the second given. The shaded ring is thirty-nine pi. The ring and the white circle together make the whole "
        "large circle. So the area of the large circle is twenty-five pi plus thirty-nine pi, which is sixty-four pi.",
        pt('stem', 'On to the second given'), show(f6g89['big'], 'together make the whole'),
        show(f6g89['b64'], 'So the area of the large circle')),
      L("If we know the area, we can find the radius. Pi R squared is sixty-four pi. Cancel pi, and R squared is "
        "sixty-four. So R is eight. Let's remember that.", show(f6g89['r8'], 'So R is eight')),
      L("Now let's see what they asked. The circumference of the large circle. Two pi R is two pi times eight, which is "
        "sixteen pi.", show(f6g89['c16'], 'Two pi R is two pi times eight')),
      L("But sixteen pi isn't in the choices. The choices are ranges, so they want us to estimate. How much is pi? Pi is "
        "three point one four, and its digits go on forever."),
      L("So sixteen pi is sixteen times three point one four. Sixteen times three is forty-eight. Sixteen times point one "
        "four: sixteen times fourteen is two hundred twenty-four, so it's two point two four. Together, fifty point two "
        "four, and a little more. That's between fifty and fifty-one. Choice number four is our answer.",
        show(f6g89['est'], 'Sixteen times three is forty-eight'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Careful with the trap. If you round pi down to three, you get exactly forty-eight, and choice number one looks "
        "right. But here the point one four matters. It adds more than two. [pause] Okay. I'll see you in the next "
        "question.", show(f6g89['trap'], 'If you round pi down to three'), mk('cross', 'choice 1', 'choice number one looks right'))),
])

# ------------------------------------------------------------------------------------------------ geo33-g090 (Hebrew: the circumscribed circle)
# Hebrew (geo 4133-4166): "but there's no circle here at all"; two rules: every triangle can be circumscribed (a circle
# through all three vertices), and there is only one such circle, with one radius, for every triangle; look for something
# special: 5, 12, 13 satisfy Pythagoras -> the triangle must be right-angled; "this is new: until now they gave a right
# triangle and asked for the third side; here three sides, and we had to see the right angle"; draw the circle around it;
# A is an inscribed angle; an inscribed angle on a diameter is 90, and the other way: an inscribed angle of 90 must rest
# on a diameter -> BC is a diameter; the circumference: no need to halve 13 and double again, 2πr = 2r · π = diameter
# times π -> 13π. English numbers 12, 35, 37 (not a well-known triple, so the squares are worked out) -> 37π.
# V3: rule one on two generic triangles (acute, obtuse), each getting its dashed circle (variations); the copy: the
# squares typed beside it; the right angle at A; the dashed circumscribed circle drawn in; BC traced teal with d = 37;
# the circumference row; the traps in red.
f6gA1, f6gB1, f6gC1 = gpt(110, 100, 70, 100), gpt(110, 100, 70, 215), gpt(110, 100, 70, 330)
f6gA2, f6gB2, f6gC2 = gpt(330, 100, 70, 140), gpt(330, 100, 70, 220), gpt(330, 100, 70, 70)
f6g90r = PIN(GEO('f6g90r', [
    ('line', [f6_seg(f6gA1, f6gB1), f6_seg(f6gB1, f6gC1), f6_seg(f6gC1, f6gA1),
              f6_seg(f6gA2, f6gB2), f6_seg(f6gB2, f6gC2), f6_seg(f6gC2, f6gA2)]),
    ('c1', [('circ', 110, 100, 70, 'teal', 3, True), ('dot', *f6gA1), ('dot', *f6gB1), ('dot', *f6gC1)]),
    ('c2', [('circ', 330, 100, 70, 'teal', 3, True), ('dot', *f6gA2), ('dot', *f6gB2), ('dot', *f6gC2)]),
    ('one', [('txt', 220, 196, 'one circle for every triangle', 'teal', 22)]),
], vb='30 22 380 190', w=460, title='Every triangle has a circumscribed circle'))
_R(f6g90r, 380, x=1070)
f6A0, f6B0, f6C0, f6O0 = (280.0, 300.0), (364.0, 300.0), (280.0, 55.0), (322.0, 177.5)
f6g90 = PIN(GEO('f6g90', [
    ('line', [f6_seg(f6A0, f6B0), f6_seg(f6B0, f6C0), f6_seg(f6C0, f6A0), f6_name(f6A0, 'A', -16, 14), f6_name(f6B0, 'B', 16, 14),
              f6_name(f6C0, 'C', -12, -16), ('txt', 322, 322, '12', 'ink', 24), ('txt', 258, 178, '35', 'ink', 24),
              ('txt', 348, 150, '37', 'ink', 24)]),
    ('sq', [f6_row(60, '12² = 144', x=592), f6_row(94, '35² = 1225', x=592), f6_row(128, '144 + 1225 = 1369', x=592)]),
    ('s37', [f6_row(162, '37² = 1369  ✓', 'teal', x=592)]),
    ('right', [('tint', [f6A0, f6B0, f6C0], 'teal'), ('right', f6A0[0], f6A0[1], 0, 90, 22)]),
    ('circ', [('circ', f6O0[0], f6O0[1], 129.5, 'teal', 3, True)]),
    ('diam', [f6_seg(f6B0, f6C0, 'teal', 6), ('dot', *f6O0), f6_row(198, 'BC = d = 37', 'teal', x=592)]),
    ('c37', [f6_row(234, 'C = π · d = 37π', 'red', 25, x=592)]),
    ('trap', [f6_row(270, '2π · 37 = 74π  ✗', 'red', x=592), f6_row(304, 'π · 18.5  ✗', 'red', x=592)]),
], vb='182 34 545 300', w=540, title='Triangle ABC and its circumscribed circle'))
_R(f6g90, 360)
video('solve-geo33-g090', 'solution', qid='geo33-g090', slides=[
    SM('Two rules', 'Two rules',
      L("The sides of triangle A B C are twelve centimeters, thirty-five centimeters, and thirty-seven centimeters. What is "
        "the circumference of the circle circumscribed about the triangle, in centimeters?",
        pt('stem', 'The sides of triangle', 'hl', 8.0), voice='calm', pause=0.5),
      L("A circle circumscribed about a triangle passes through all three of its vertices. But wait, there's no circle in "
        "the figure at all. [short pause] To solve this, we need two rules."),
      L("[short pause] Rule one. Every triangle can be circumscribed. Every triangle has a circle that passes through all "
        "three of its vertices. Here's an acute triangle with its circle, and here's an obtuse one with its circle.",
        show(f6g90r['line'], 'Rule one'), show(f6g90r['c1'], "Here's an acute triangle"), show(f6g90r['c2'], "and here's an obtuse one")),
      L("Rule two. There's only one such circle, with one radius. That's true for every triangle. So this triangle has "
        "exactly one circumscribed circle, and we need to find its size.", show(f6g90r['one'], "There's only one such circle")),
      L("[short pause] So let's look for something special in this triangle. Its sides are twelve, thirty-five and "
        "thirty-seven.", pt('fig: 35', 'Its sides are twelve'))),
    SM('The hypotenuse is a diameter', 'A right triangle',
      L("Let's check Pythagoras. Does twelve squared plus thirty-five squared equal thirty-seven squared? Twelve squared "
        "is one hundred forty-four. Thirty-five squared is thirty-five times thirty-five, one thousand two hundred "
        "twenty-five. Together, one thousand three hundred sixty-nine.", show(f6g90['line'], "Let's check Pythagoras"),
        show(f6g90['sq'], 'Twelve squared is')),
      L("And thirty-seven squared? Thirty-seven times thirty is one thousand one hundred ten, and thirty-seven times seven "
        "is two hundred fifty-nine. Together, one thousand three hundred sixty-nine. The same.",
        show(f6g90['s37'], 'Together, one thousand three hundred sixty-nine. The same')),
      L("The sides satisfy Pythagoras, so the triangle must be a right triangle. The right angle is across from the longest "
        "side, thirty-seven. That's the angle at A.", show(f6g90['right'], 'The right angle is across')),
      L("This is new. Until now, they gave us a right triangle with two of its sides, and we found the third. Here they "
        "gave us all three sides, and we had to see from them that the triangle is a right triangle."),
      L("Now let's draw the circle around the triangle, and remember one more rule. The angle at A sits on the circle, so "
        "it's an inscribed angle. We learned that an inscribed angle that rests on a diameter is ninety degrees. And the "
        "other way around. If an inscribed angle is ninety degrees, it must rest on a diameter.",
        show(f6g90['circ'], "let's draw the circle around")),
      L("So B C, the hypotenuse, is a diameter of the circle. The diameter is thirty-seven.",
        show(f6g90['diam'], 'is a diameter of the circle')),
      L("Now the question is simple. What's the circumference of a circle with a diameter of thirty-seven? It's two pi r. "
        "We could halve thirty-seven to get the radius, and then double it again. But there's a simpler way. Two pi r is "
        "two r times pi, and two r is the diameter. So the circumference is the diameter times pi, thirty-seven pi. "
        "Choice number two is our answer.", show(f6g90['c37'], 'So the circumference is the diameter times pi'),
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Careful with the traps. Thirty-seven is the diameter, not the radius. Two pi times thirty-seven gives seventy-four "
        "pi, choice number one. And eighteen and a half pi, choice number three, is pi times the radius. It forgets the "
        "two. [pause] Okay. I'll see you in the next question.", show(f6g90['trap'], 'Two pi times thirty-seven'),
        mk('cross', 'choice 1', 'choice number one'), mk('cross', 'choice 3', 'choice number three'))),
])

# ------------------------------------------------------------------------------------------------ geo33-g091 (Hebrew: alpha and beta in turn)
# Hebrew (geo 4171-4207): the dark area is part of the circle's area -> the circle's area and which part; area: πr²,
# (√12)² = 12, "the power cancels the root", 12π; which part: α and β have no number; what can we say? count them: 4α and
# 4β, all together 360 -> an equation; one equation, two unknowns: not each one, but the sum; "who sees it divides by 4,
# who doesn't takes out the common factor 4"; α + β = 90; could be 30 and 60, 10 and 80, endless options, it doesn't
# matter; 90 out of 360 = a quarter; 12π / 4 = 3π. English numbers: √35, five of each -> 35π, α + β = 72, 1/5, 7π.
# V3: the copy with the grey shaded sector as given; the whole disc tinted for its area; the five α arcs teal and the five
# β arcs orange as she counts; the five α + β pairs traced on the circle in turn (the circle = 5 pairs), the shaded pair
# in red; the working typed beside the figure.
f6CO, f6CR = (320.0, 180.0), 109.5
f6RAD = [90, 120, 162, 192, 234, 264, 306, 336, 18, 48]
f6g91 = PIN(GEO('f6g91', [
    ('line', [('wedge', f6CO[0], f6CO[1], f6CR, 90, 162, 'ink'), ('circ', f6CO[0], f6CO[1], f6CR)]
             + [f6_seg(f6CO, gpt(f6CO[0], f6CO[1], f6CR, a), 'ink', 2.5) for a in f6RAD] + [('dot', *f6CO)]
             + [('txt',) + gpt(f6CO[0], f6CO[1], 80, f6RAD[k] + (15 if k % 2 == 0 else 21)) + ('α' if k % 2 == 0 else 'β', 'ink', 22, True)
                for k in range(10)]),
    ('area', [('circ', f6CO[0], f6CO[1], f6CR, 'teal', 4, False, 'teal'), f6_row(76, 'π · (√35)² = 35π', 'teal')]),
    ('al', [('arc', f6CO[0], f6CO[1], 40, f6RAD[k], f6RAD[k + 1], 'small') for k in range(0, 10, 2)]),
    ('be', [('arc', f6CO[0], f6CO[1], 48, f6RAD[k], f6RAD[(k + 1) % 10], 'large') for k in range(1, 10, 2)]),
    ('eq', [f6_row(112, '5α + 5β = 360°')]),
    ('sum', [f6_row(148, '5(α + β) = 360°'), f6_row(184, 'α + β = 72°', 'red', 25)]),
    ('ex', [f6_row(220, '30 + 42?  12 + 60?', 'ink', 22)]),
    ('pairs', [('arcw', f6CO[0], f6CO[1], f6CR, 90 + 72 * k, 162 + 72 * k, 'teal' if k % 2 else 'orange', 9) for k in range(1, 5)]
              + [('arcw', f6CO[0], f6CO[1], f6CR, 90, 162, 'red', 9), ('txt', 232, 80, '72°', 'red', 24)]),
    ('fifth', [f6_row(256, '72° / 360° = 1/5', 'teal')]),
    ('ans', [f6_row(294, '1/5 · 35π = 7π', 'red', 26)]),
], vb='200 50 500 270', w=540, title='Central angles alpha and beta in turn'))
_R(f6g91, 360)
video('solve-geo33-g091', 'solution', qid='geo33-g091', slides=[
    SM('Find the sum, not each angle', 'Find the sum, not each angle',
      L("A circle has a radius of root thirty-five centimeters. Its central angles are alpha and beta in turn, five of "
        "each, as in the figure. One sector with angle alpha and one sector with angle beta are shaded. What is their total "
        "area, in square centimeters?", pt('stem', 'A circle has a radius', 'hl', 11.0), voice='calm', pause=0.5),
      L("The shaded part is part of the circle's area. So we need two things. The area of the whole circle, and which part "
        "of it is shaded.", show(f6g91['line'], 'The shaded part is part')),
      L("[short pause] Let's start with the area of the circle. The radius is given, so it's easy. Pi r squared."),
      L("Root thirty-five, squared, is thirty-five, because the square cancels the root. So the area is thirty-five pi. That's "
        "the whole circle.", show(f6g91['area'], 'So the area is thirty-five pi')),
      L("Now, which part. For that we need alpha and beta, but we don't get a number for either of them. So what can we "
        "say?", pt('fig: α', 'For that we need alpha')),
      L("Let's count them. One, two, three, four, five alphas. And five betas.",
        show(f6g91['al'], 'five alphas'), show(f6g91['be'], 'And five betas')),
      L("All ten angles go around the center, so together they make three hundred sixty degrees. So five alpha plus five "
        "beta is three hundred sixty.", show(f6g91['eq'], 'So five alpha plus five beta')),
      L("That's one equation with two unknowns. We can't find alpha or beta on its own, but we can find their sum."),
      L("If you see it, just divide by five. If not, take out the common factor five. Five times the sum, alpha plus beta, is "
        "three hundred sixty. Divide by five, and alpha plus beta is seventy-two.",
        show(f6g91['sum'], 'take out the common factor five')),
      L("What does that tell us about alpha and beta? We don't know. Alpha could be thirty and beta forty-two. Or twelve and "
        "sixty. There are endless options. But it doesn't matter.", show(f6g91['ex'], 'Alpha could be thirty')),
      L("One alpha and one beta together are seventy-two degrees, and the circle is made of five such pairs.", show(f6g91['pairs'], 'the circle is made of five such pairs')),
      L("The two shaded sectors are one pair. So they're seventy-two out of three hundred sixty, which is one fifth of the circle.",
        show(f6g91['fifth'], 'which is one fifth')),
      L("So the shaded area is one fifth of thirty-five pi, which is seven pi. Choice number two is our answer. [pause] "
        "Okay. I'll see you in the next question.", show(f6g91['ans'], 'one fifth of thirty-five pi'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo33-g092 (Hebrew: three tangent circles)
# Hebrew (geo 4210-4258): an arc length is part of the circumference: the angle out of 360 times 2πr; circle A's whole
# circumference 2π; peek at the choices: 2π is out (the whole circle; the arc must be less); "sharp-eyed students" cross
# out π too: half the circle needs an angle of 180 at A, but it is an angle of the triangle; the last two can't be split
# by a psychometric idea -> solve; if out of time guess one of them: 1 in 2 instead of 1 in 4; put in the radii 1,1 2,2
# 3,3; 1+2, 1+3, 2+3 -> 3, 4, 5, a Pythagorean triple -> the angle at A (opposite the hypotenuse 5) is 90; the angle we
# don't need is 90 = a quarter; the highlighted arc = 3/4 of the circumference; 3/4 of 2π: cancel 2 and 4 -> 1.5π.
# English numbers 6, 14, 15 -> 20, 21, 29 (20² + 21² = 841 = 29²), circumference 12π, 3/4 · 12π = 9π (a quarter is 3π).
# V3: the copy with the highlighted arc in orange; 12π typed; the triangle of centers drawn dashed (construction) with its
# angle at A for the elimination; the radii written as she names them; the sums and the squares typed; the right angle at
# A; the unwanted quarter arc traced teal; the answer.
f6A, f6B, f6C = (259.2, 250.4), (387.2, 250.4), (259.2, 116.0)
f6rA, f6rB, f6rC = 38.4, 89.6, 96.0
f6g92 = PIN(GEO('f6g92', [
    ('line', [('circ', f6A[0], f6A[1], f6rA), ('circ', f6B[0], f6B[1], f6rB), ('circ', f6C[0], f6C[1], f6rC),
              ('dot', *f6A), ('dot', *f6B), ('dot', *f6C), f6_name(f6A, 'A', -12, 16), f6_name(f6B, 'B', 15, 16),
              f6_name(f6C, 'C', 15, -16), ('arcw', f6A[0], f6A[1], f6rA, 90, 360, 'orange', 7)]),
    ('c12', [f6_row(34, '2π · 6 = 12π', x=600)]),
    ('tri', [f6_seg(f6A, f6B, 'teal', 3, True), f6_seg(f6A, f6C, 'teal', 3, True), f6_seg(f6B, f6C, 'teal', 3, True),
             ('arc', f6A[0], f6A[1], 20, 0, 90, 'small'), f6_row(66, 'half? ∠A = 180° ✗', 'red', 21, x=600)]),
    ('rA', [('txt', 280, 268, '6', 'teal', 22), ('txt', 245, 228, '6', 'teal', 22)]),
    ('rB', [('txt', 342, 270, '14', 'teal', 22), ('txt', 371, 204, '14', 'teal', 22)]),
    ('rC', [('txt', 241, 160, '15', 'teal', 22), ('txt', 306, 138, '15', 'teal', 22)]),
    ('sums', [f6_row(98, 'AB = 6 + 14 = 20', x=600), f6_row(129, 'AC = 6 + 15 = 21', x=600), f6_row(160, 'BC = 14 + 15 = 29', x=600)]),
    ('pyth', [f6_row(192, '400 + 441 = 841', x=600), f6_row(223, '29² = 841  ✓', 'teal', x=600)]),
    ('right', [('right', f6A[0], f6A[1], 0, 90, 14)]),
    ('quarter', [('arcw', f6A[0], f6A[1], f6rA, 0, 90, 'teal', 7), f6_row(255, '∠A = 90° → 1/4', 'teal', x=600)]),
    ('rest', [f6_row(287, 'the arc: 3/4', 'orange', x=600)]),
    ('ans', [f6_row(320, '3/4 · 12π = 9π', 'red', 26, x=600)]),
], vb='158 12 565 330', w=540, title='Three circles that touch'))
_R(f6g92, 360)
video('solve-geo33-g092', 'solution', qid='geo33-g092', slides=[
    SM('Eliminate, then find the angle', 'Eliminate, then find the angle',
      L("Three circles with centers A, B and C touch one another from the outside. Their radii are six centimeters, "
        "fourteen centimeters and fifteen centimeters. What is the length of the highlighted arc of the circle with center "
        "A, in centimeters?", pt('stem', 'Three circles with centers', 'hl', 10.0), voice='calm', pause=0.5),
      L("We need the length of an arc. An arc is part of the circumference. Its length is the angle out of three hundred "
        "sixty, times two pi r, the whole circumference.", show(f6g92['line'], 'We need the length of an arc')),
      L("[short pause] The radius of circle A is given, so the whole circumference is easy. Two pi r is two pi times six, "
        "which is twelve pi.", show(f6g92['c12'], 'Two pi r is two pi times six')),
      L("Let's peek at the choices. Choice number one is twelve pi. That's the whole circle, and the highlighted arc is "
        "only part of it, so it has to be less. Choice number one is out.", mk('cross', 'choice 1', 'Choice number one is out')),
      L("Sharp-eyed students cross out choice number four too. Six pi is exactly half the circle. For that, the angle at "
        "A, between the lines to B and to C, would have to be one hundred eighty. But connect the three centers, and that "
        "angle is an angle of triangle A B C. An angle of a triangle is less than one hundred eighty. So choice number four "
        "is out too.", show(f6g92['tri'], 'connect the three centers'), mk('cross', 'choice 4', 'So choice number four')),
      L("Choice number two and choice number three can't be split with a quick idea, so we have to solve. But if you're "
        "out of time, guess one of the two. That's a one in two chance instead of one in four."),
      L("[short pause] Let's put in the givens. The radius of circle A is six, so we write six and six on its two radii. "
        "Circle B, fourteen and fourteen. Circle C, fifteen and fifteen.", show(f6g92['rA'], 'we write six and six'),
        show(f6g92['rB'], 'Circle B, fourteen'), show(f6g92['rC'], 'Circle C, fifteen')),
      L("The circles touch, so the line between two centers passes through the point where they touch. It's made of the "
        "two radii. So A B is six plus fourteen, twenty. A C is six plus fifteen, twenty-one. And B C is fourteen plus "
        "fifteen, twenty-nine.", show(f6g92['sums'], 'So A B is six plus fourteen')),
      L("Twenty, twenty-one, twenty-nine. Let's check Pythagoras. Twenty squared is four hundred, and twenty-one squared "
        "is four hundred forty-one. Together, eight hundred forty-one. And twenty-nine squared? It's twenty-nine times thirty, "
        "minus twenty-nine. Twenty-nine times thirty is eight hundred seventy, and eight hundred seventy minus "
        "twenty-nine is eight hundred forty-one. The same, so it's a Pythagorean "
        "triple.", show(f6g92['pyth'], 'Together, eight hundred forty-one')),
      L("B C, twenty-nine, is the hypotenuse, so the angle across from it, the angle at A, is ninety degrees.",
        show(f6g92['right'], 'the angle at A, is ninety')),
      L("So the arc we don't need, inside that angle, is ninety out of three hundred sixty. That's a quarter of the circle. "
        "And the highlighted arc is the rest, three quarters of the circumference.",
        show(f6g92['quarter'], 'is ninety out of three hundred sixty'), show(f6g92['rest'], 'three quarters of the circumference')),
      L("Three quarters of twelve pi. A quarter of twelve pi is three pi, so three quarters is nine pi. Choice number three "
        "is our answer. [pause] Okay. I'll see you in the next question.", show(f6g92['ans'], 'so three quarters is nine pi'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# =================================================================================================================
# Topic-33 advanced block, part 1 (fragment f7, TAG G, 2026-10-14): geo-093 (the advanced level's opening), geo33-g094,
# g095, g096, g097 and geo-097-after (three nested shapes) - the Hebrew "circles advanced" lesson (geo 4260-4660).
# Question videos: the question figure on the left (FIG_LEFT), our colour copy built in layers on the right (Rule V3),
# the working written inside the copy so the layers stay together. Shaded areas: the whole shape is tinted, then the
# part we take away is cut out of it (a white 'region' over it), so the subtraction is seen.
# =================================================================================================================
FIG_LEFT.update({'solve-geo33-g094', 'solve-geo33-g095', 'solve-geo33-g096', 'solve-geo33-g097'})
GCOL['f7white'] = '#ffffff'          # a cut-out: a white region drawn over a tint removes that part


def f7_poly(pts, col='ink', w=3):
    """the sides of a closed polygon as segments"""
    return [('seg', pts[k][0], pts[k][1], pts[(k + 1) % len(pts)][0], pts[(k + 1) % len(pts)][1], col, w) for k in range(len(pts))]


def f7_seg(p, q, col='ink', w=3, dash=False):
    return ('seg', p[0], p[1], q[0], q[1], col, w, dash)


def f7_name(p, t, dx, dy, col='ink', size=26):
    return ('txt', p[0] + dx, p[1] + dy, t, col, size, True)


def f7_pd(pts):
    """an svg path (closed polygon)"""
    return 'M ' + ' L '.join('%.1f %.1f' % tuple(p) for p in pts) + ' Z'


def f7_sd(cx, cy, r, a1, a2):
    """an svg path of the sector a1 -> a2 (counter-clockwise)"""
    (x1, y1), (x2, y2) = gpt(cx, cy, r, a1), gpt(cx, cy, r, a2)
    return 'M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 %d 0 %.1f %.1f Z' % (cx, cy, x1, y1, r, r, 1 if (a2 - a1) % 360 > 180 else 0, x2, y2)


def f7_mid(p, q, t=0.5):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


# ------------------------------------------------------------------------------------------------ geo-093 (lesson: the advanced level)
# Hebrew (geo 4262-4269): we learned the basic rules and practiced basic and harder questions; in fact you already have
# the tools for most circle questions; now harder "edge" questions, a few principles that come back in them, and how exam
# thinking solves them much faster, or even when we're not sure of the full solution. Each tool is taught in the
# question that uses it (shaded areas and the stop-and-look partial calculation and estimating in g094, inscribed /
# circumscribed and plugging in in g096).
f7h1 = I('f7h1', 'Shaded areas: $\\ $what minus what?', size=32)
f7h2 = I('f7h2', 'Shapes in circles: $\\ $write every length with $r$', size=32)
f7h3 = I('f7h3', 'Exam shortcuts: $\\ $stop and look at the choices, plug in a number, estimate', size=30)
video('geo-093', 'lesson', slides=[
    S('Advanced Circles',
      L("Circles, the advanced level. In the last lessons we learned the basic rules of the circle, and we practiced basic "
        "questions and harder ones.")),
    S("What's ahead",
      L("In fact, you already have the tools for most circle questions on the exam. Now we'll practice harder questions, "
        "the kind that come near the end of the section."),
      L("We'll meet a few ideas that come back again and again in these questions. The first one is shaded areas. We'll "
        "ask which shape minus which shape gives the shaded part.", show(f7h1, 'The first one is shaded areas')),
      L("The second one is a shape inside a circle, or a circle inside a shape. There we'll write every length with the "
        "radius of the circle.", show(f7h2, 'The second one is a shape')),
      L("We'll also see quick exam ways. We'll stop halfway and look at the choices, we'll plug in a number instead of a "
        "letter, and we'll estimate sizes. With them we can solve these questions much faster, and sometimes even when "
        "we're not sure of the full solution.", show(f7h3, 'quick exam ways')),
      L("We'll explain each one in the question that uses it. Let's start. [pause] Okay. I'll see you in the next video.",
        pt('f7h3', "We'll explain each one"))),
])

# ------------------------------------------------------------------------------------------------ geo33-g094 (Hebrew: the tangent and the silver triangle)
# Hebrew (geo 4271-4386; Hebrew r = 2, answers 2pi-2 / 2-pi / 8-pi / 4-pi; course r = 6): two approaches, math and exam
# thinking. Shaded areas (met in quadrilaterals): subtract areas; build a scheme, what minus what: triangle AOB minus the
# sector. Put in the givens: OA = OB -> right AND isosceles, a silver triangle, base angles 45; AB tangent -> the automatic
# construction, the radius OC to the point of tangency, perpendicular; OC is the height to the base of an isosceles
# triangle, so also a bisector and a median (45, 45); OC = r; OCB silver too -> CB = AC = r. Triangle: base times height
# over 2 (the trap: "a hypotenuse in a silver triangle -> find the legs" - "why? don't work for nothing"). Partial
# calculation: the answer is 36 minus something with pi -> eliminate (pi in the wrong place; 18 not 36; 72 not 36). "In
# the exam mark and move on; in the lesson we calculate the sector": pi r^2, 90/360 = a quarter -> 9 pi. Estimating sizes
# (stuck / out of time): shaded < triangle, even < half; a negative answer hidden behind letters; bigger than the whole
# triangle; 36 - 9 pi between 0 and 9, looks right by eye. "If there's no choice, a great card up your sleeve."
# V3: the copy; the whole triangle tinted, the sector shown, then cut out (white) so the shaded part is left: the scheme;
# the givens marked as named (ticks, right angle, 45s); C pointed at, then the dashed radius OC with its right angle;
# the 45s at O; 6, 6, 6 written as found; the working under the figure. Slide 2: the copy again with the values and the
# shaded part tinted; the sector tinted orange when it is calculated. Slide 3: the shaded part tinted, the bounds written.
f7O4, f7r4 = (320.0, 180.0), 116.8
f7A4, f7B4, f7C4 = (203.2, 63.2), (436.8, 63.2), (320.0, 63.2)
f7s45, f7s135 = gpt(320, 180, f7r4, 45), gpt(320, 180, f7r4, 135)
f7g94_base = ([('circ', f7O4[0], f7O4[1], f7r4)] + f7_poly([f7O4, f7A4, f7B4]) + [('dot', f7O4[0], f7O4[1]),
              f7_name(f7O4, 'O', 0, 24), f7_name(f7A4, 'A', -18, -12), f7_name(f7B4, 'B', 18, -12)])
f7g94_sec = f7_sd(320, 180, f7r4, 45, 135)
f7g94_cut = [('region', f7g94_sec, 'f7white', 1), ('arc', 320, 180, f7r4, 45, 135, 'ink'), f7_seg(f7O4, f7s45), f7_seg(f7O4, f7s135),
             ('dot', f7O4[0], f7O4[1])]
f7g94_marks = [('tick', *f7O4, *f7A4, 1), ('tick', *f7O4, *f7B4, 1), ('right', 320, 180, 45, 135, 16),
               ('dot', f7C4[0], f7C4[1]), f7_name(f7C4, 'C', 0, -22), f7_seg(f7O4, f7C4, 'teal', 3, True), ('right', 320, 63.2, 270, 0, 13),
               ('txt', 334, 100, '6', 'small', 24), ('txt', 262, 46, '6', 'small', 24), ('txt', 378, 46, '6', 'small', 24)]
f7g94 = PIN(GEO('f7g94', [
    ('line', f7g94_base),
    ('tri', [('region', f7_pd([f7O4, f7A4, f7B4]), 'teal'), ('txt', 565, 50, 'triangle', 'small', 24)]),
    ('sec', [('wedge', 320, 180, f7r4, 45, 135, 'orange'), ('arcw', 320, 180, f7r4, 45, 135, 'orange', 6),
             ('txt', 565, 80, '− sector', 'orange', 24)]),
    ('cut', f7g94_cut + [('txt', 565, 110, '= shaded', 'ink', 24)]),
    ('eq', [('tick', *f7O4, *f7A4, 1), ('tick', *f7O4, *f7B4, 1), ('right', 320, 180, 45, 135, 16)]),
    ('b45', [('arc', f7A4[0], f7A4[1], 30, 315, 360, 'small', '45°', 66), ('arc', f7B4[0], f7B4[1], 30, 180, 225, 'small', '45°', 66)]),
    ('c', [('dot', f7C4[0], f7C4[1]), f7_name(f7C4, 'C', 0, -22)]),
    ('oc', [f7_seg(f7O4, f7C4, 'teal', 3, True), ('right', 320, 63.2, 270, 0, 13)]),
    ('o45', [('arc', 320, 180, 26, 45, 90, 'small'), ('arc', 320, 180, 30, 90, 135, 'small'),
             ('txt', 345, 134, '45°', 'small', 20), ('txt', 295, 134, '45°', 'small', 20)]),
    ('six', [('txt', 334, 100, '6', 'small', 24), ('txt', 378, 46, '6', 'small', 24), ('txt', 262, 46, '6', 'small', 24),
             ('txt', 565, 160, 'AB = 6 + 6 = 12', 'ink', 22)]),
    ('t36', [('txt', 565, 195, 'triangle:', 'ink', 22), ('txt', 565, 225, '12 · 6 ÷ 2 = 36', 'ink', 22)]),
], vb='175 22 505 282', w=540, title='Triangle AOB with the tangent AB'))
f7g94b = PIN(GEO('f7g94b', [
    ('line', f7g94_base + [('region', f7_pd([f7O4, f7A4, f7B4]) + ' ' + f7g94_sec, 'teal')] + f7g94_marks
     + [('txt', 565, 50, 'triangle = 36', 'small', 22)]),
    ('look', [('txt', 565, 85, 'shaded = 36 −', 'ink', 22), ('txt', 565, 113, '(something with π)', 'ink', 20)]),
    ('circ', [('txt', 565, 160, 'circle: π · 6² = 36π', 'ink', 21)]),
    ('sec', [('wedge', 320, 180, f7r4, 45, 135, 'orange'), ('txt', 565, 195, 'sector:', 'orange', 22),
             ('txt', 565, 225, '¼ · 36π = 9π', 'orange', 22)]),
], vb='175 22 505 282', w=540, title='Triangle AOB: 36 minus a sector'))
f7g94c = PIN(GEO('f7g94c', [
    ('line', f7g94_base + [('region', f7_pd([f7O4, f7A4, f7B4]) + ' ' + f7g94_sec, 'teal')] + f7g94_marks
     + [('txt', 565, 50, 'triangle = 36', 'small', 22)]),
    ('lt', [('txt', 565, 90, 'shaded < 36', 'ink', 22), ('txt', 565, 120, 'by eye: < 18', 'ink', 22)]),
    ('pi', [('txt', 565, 165, '3 < π < 4', 'ink', 22), ('txt', 565, 195, '27 < 9π < 36', 'ink', 22)]),
], vb='175 22 505 282', w=540, title='Estimating the shaded area'))
for _g in (f7g94, f7g94b, f7g94c):
    _R(_g, 200)
video('solve-geo33-g094', 'solution', qid='geo33-g094', slides=[
    SM('Method 1 · The math way: subtract areas', 'Triangle minus sector',
      L("A B is tangent to a circle with center O and radius six centimeters. Given, O A equals O B, and angle A O B is "
        "ninety degrees. What is the area inside triangle A O B but outside the circle, in square centimeters?",
        pt('stem', 'A B is tangent to a circle', 'hl', 11.0), voice='calm', pause=0.5),
      L("So they ask for the shaded area, the part of the triangle that is outside the circle. [short pause] We'll solve "
        "it the math way, and then we'll see two quick exam ways.", pt('stem: ask', 'So they ask for the shaded area')),
      L("[short pause] Shaded areas. We met them in quadrilaterals, and the most common way to solve them is to subtract "
        "areas. In the hard circle questions at the end of the section, shaded areas come back again and again.",
        show(f7g94['line'], 'Shaded areas. We met them')),
      L("So first we build a scheme. What minus what gives the shaded part? Look at the whole triangle A O B.",
        show(f7g94['tri'], 'Look at the whole triangle')),
      L("Inside it there's a sector of the circle. If we take the triangle and remove the sector, what's left is exactly "
        "the shaded part. So the shaded area is the triangle minus the sector. That's our scheme.",
        show(f7g94['sec'], "there's a sector of the circle"), show(f7g94['cut'], 'remove the sector')),
      L("Now let's put in the givens. O A equals O B, so we mark them equal. And the angle at O is ninety degrees.",
        show(f7g94['eq'], 'O A equals O B')),
      L("So triangle A O B isn't just a right triangle. It's right and isosceles, a silver triangle. In a silver triangle, "
        "the two base angles are forty-five degrees each.", show(f7g94['b45'], 'the two base angles')),
      L("The next given, A B is tangent to the circle. We learned an automatic construction. When there's a point of "
        "tangency, we draw the radius to it. Let's call that point C.", show(f7g94['c'], "Let's call that point C")),
      L("We draw the radius from O to C. The radius is perpendicular to the tangent, so the angle at C is ninety degrees.",
        show(f7g94['oc'], 'We draw the radius from O to C')),
      L("Triangle A O B is isosceles, and O C is the height to its base. In an isosceles triangle, this height is also an "
        "angle bisector and a median. So it cuts the angle at O into two angles of forty-five degrees.",
        show(f7g94['o45'], 'two angles of forty-five')),
      L("The radius is six, so O C is six. And triangle O C B is a silver triangle too, so C B equals O C, six. On the "
        "other side, A C is six too. So A B is six plus six, twelve.", show(f7g94['six'], 'so O C is six')),
      L("Now the triangle's area. The best way is base times height, over two. The base is A B, twelve, and the height "
        "is O C, six.", pt('f7g94_line', 'The best way is base times height')),
      L("A lot of students say, I have the hypotenuse of a silver triangle, so I'll find the two legs, multiply them, and "
        "divide by two. I ask, why? You already have a base and a height. Don't work for nothing, there's no time on the "
        "exam."),
      L("Twelve times six is seventy-two, and over two it's thirty-six. So the triangle is thirty-six.",
        show(f7g94['t36'], 'Twelve times six'))),
    SM('Method 2 · The math way: partial calculation', 'Stop and look at the choices',
      L("[pause] Now we could go on and find the sector. But wait. On the exam we also have the choices, and they often "
        "help us.", show(f7g94b['line'], 'Now we could go on')),
      L("We stop halfway, and we use what we already know to rule out choices. This is called a partial calculation. The "
        "shaded area is thirty-six, minus the sector. A sector is a part of a circle, so its area has pi in it. So we're "
        "looking for thirty-six minus something with pi.", show(f7g94b['look'], 'So we\'re looking for thirty-six')),
      L("Choice number three is eighteen pi minus eighteen. The pi is in the wrong place. That's like a circle minus a "
        "triangle, not a triangle minus a sector. So it's out.", mk('cross', 'choice 3', "So it's out")),
      L("Choice number one is eighteen minus nine pi. The pi is in the right place, but the triangle is thirty-six, not "
        "eighteen. It's out too.", mk('cross', 'choice 1', "It's out too")),
      L("Choice number four is seventy-two minus nine pi. It's the same problem, because we need thirty-six minus "
        "something. It's out.", mk('cross', 'choice 4', 'something. It\'s out')),
      L("Only choice number two is left, thirty-six minus nine pi. We started with the math, and halfway we switched to "
        "an exam shortcut. On the exam, we mark it and move on.", mk('tick', 'choice 2', 'Only choice number two is left')),
      L("[pause] But we're in a lesson, so let's also find the sector. A sector is a part of the circle. The whole circle "
        "is pi r squared, pi times six squared, thirty-six pi.", show(f7g94b['circ'], 'The whole circle')),
      L("Which part? The central angle decides it, and here it's ninety degrees. Some of you know by heart that ninety "
        "degrees is a quarter of the circle. Wonderful. If not, ninety out of three hundred sixty is a quarter. A quarter "
        "of thirty-six pi is nine pi.", show(f7g94b['sec'], 'Which part')),
      L("So the shaded area is thirty-six minus nine pi. The answer we found is really right, choice number two.",
        mk('tick', 'choice 2', 'choice number two'))),
    SM('Method 3 · Estimation', 'Estimating sizes',
      L("[pause] One more way, a full exam shortcut. It's called estimation. Maybe you put in the givens and don't "
        "know how to go on. Or maybe you run out of time, because this is one of the last questions in the section.",
        show(f7g94c['line'], 'called estimation')),
      L("What do we know? The triangle is thirty-six, and the shaded part is only a piece of it. So the shaded area is "
        "less than thirty-six. And by eye, it's even less than half of the triangle, less than eighteen.",
        show(f7g94c['lt'], 'So the shaded area is')),
      L("Now the choices. We need the size of pi. Pi is a bit more than three, and less than four. So nine pi is more "
        "than twenty-seven, and less than thirty-six.", show(f7g94c['pi'], 'Pi is a bit more than three')),
      L("Choice number one, eighteen minus nine pi. Nine pi is more than twenty-seven, so eighteen minus it is a negative "
        "number. They do this a lot on the exam, they hide a negative answer behind letters. An area can't be negative, "
        "so it's out.", mk('cross', 'choice 1', "An area can't be negative")),
      L("Choice number three, eighteen pi minus eighteen. Eighteen pi is more than eighteen times three, fifty-four. "
        "Minus eighteen, it's still more than thirty-six. That's bigger than the whole triangle, so it's out.",
        mk('cross', 'choice 3', "That's bigger than the whole triangle")),
      L("Choice number four, seventy-two minus nine pi. Nine pi is less than thirty-six, so seventy-two minus it is more "
        "than thirty-six. Too big again, it's out.", mk('cross', 'choice 4', 'Too big again')),
      L("Choice number two, thirty-six minus nine pi. Nine pi is between twenty-seven and thirty-six, so this is between "
        "zero and nine. That's a small piece of the triangle, just like the shaded part we see. Choice number two again.",
        mk('tick', 'choice 2', 'Choice number two again')),
      L("Estimating doesn't always rule out three choices. Sometimes it rules out only one or two. But when you're stuck "
        "or out of time, it's a great card up your sleeve. [pause] Okay. I'll see you in the next question.",
        pt('f7g94c_line', "Estimating doesn't always"))),
])

# ------------------------------------------------------------------------------------------------ geo33-g095 (Hebrew: the right triangle tangent at B and D)
# Hebrew (geo 4389-4462; Hebrew r = 6, course OE = EC = 4): shaded areas again, but the scheme is not trivial (the big
# triangle minus something? not clear); "work with the givens, put them in, and hope the solution shows itself"; B is a
# point of tangency, the 90 is marked; D is a point of tangency but no radius there -> draw the radius OD, mark 90 (the
# most basic construction); now the scheme: triangle ODC minus the sector, like the last question. Triangle: a leg and the
# hypotenuse - Pythagoras probably, but no need: the hypotenuse is twice the leg -> only in a gold triangle (30 opposite
# the short leg, 60 opposite DC), the long leg root 3 times the short one; leg times leg over 2. Partial calculation:
# look for 8 root 3 minus something (course: two choices keep 8 root 3, so the sector is needed - "the trick doesn't
# finish the job"); the sector: pi r^2, 60/360 = a sixth. "Some students find the sector first": something minus 8 pi/3.
# V3: the copy; the right angle at B highlighted with its radius OB; O and D pointed at, then the dashed radius OD and
# its right angle; 4 on OD; the triangle ODC tinted, the sector cut out of it (white): the scheme. Slide 2: ODC alone,
# enlarged, with the same labels, values and tint (the cut-out of V3); 30 and 60, 4 root 3, the working beside it, the
# sector tinted orange when it is calculated.
f7O5, f7r5 = (277.059, 211.49), 85.882
f7A5, f7B5, f7C5 = (191.176, 62.738), (191.176, 211.49), (448.824, 211.49)
f7D5, f7E5 = gpt(277.059, 211.49, f7r5, 60), (362.941, 211.49)
f7g95_base = ([('circ', f7O5[0], f7O5[1], f7r5)] + f7_poly([f7A5, f7B5, f7C5]) + [('right', f7B5[0], f7B5[1], 0, 90, 12), ('dot', *f7O5),
              f7_name(f7O5, 'O', -12, 20), f7_name(f7A5, 'A', -16, -14), f7_name(f7B5, 'B', -17, 14), f7_name(f7C5, 'C', 19, 14),
              f7_name(f7D5, 'D', 6, -22), f7_name(f7E5, 'E', 0, 22), ('txt', 320, 236, '4', 'ink', 22), ('txt', 406, 230, '4', 'ink', 22)])
f7g95_sec = f7_sd(f7O5[0], f7O5[1], f7r5, 0, 60)
f7g95 = PIN(GEO('f7g95', [
    ('line', f7g95_base),
    ('b', [f7_seg(f7O5, f7B5, 'teal', 5), ('right', f7B5[0], f7B5[1], 0, 90, 14)]),
    ('dpts', [('dot', *f7O5), ('dot', *f7D5)]),
    ('od', [f7_seg(f7O5, f7D5, 'teal', 3, True), ('right', f7D5[0], f7D5[1], 240, 330, 12)]),
    ('r4', [('txt', 283, 163, '4', 'small', 24)]),
    ('tri', [('region', f7_pd([f7O5, f7D5, f7C5]), 'teal')]),
    ('cut', [('region', f7g95_sec, 'f7white', 1), ('arc', f7O5[0], f7O5[1], f7r5, 0, 60, 'ink'), f7_seg(f7O5, f7E5),
             f7_seg(f7O5, f7D5, 'teal', 3, True), ('dot', *f7O5), ('txt', 535, 55, 'triangle ODC', 'small', 22), ('txt', 535, 83, '− sector DOE', 'orange', 22), ('txt', 535, 111, '= shaded', 'ink', 22)]),
], vb='120 22 520 284', w=520, title='Right triangle ABC tangent to the circle at B and D'))
# the enlarged triangle ODC (scale about 2), same labels and tint
f7zO, f7zR = (90.0, 330.0), 170.0
f7zD, f7zE, f7zC = gpt(90, 330, f7zR, 60), (260.0, 330.0), (430.0, 330.0)
f7g95b = PIN(GEO('f7g95b', [
    ('line', [('region', f7_pd([f7zO, f7zD, f7zC]) + ' ' + f7_sd(90, 330, f7zR, 0, 60), 'teal'),
              f7_seg(f7zO, f7zD, 'teal', 3, True), f7_seg(f7zD, f7zC), f7_seg(f7zO, f7zC), ('arc', 90, 330, f7zR, 0, 60, 'ink'),
              ('right', f7zD[0], f7zD[1], 240, 330, 16), ('dot', *f7zO), ('dot', *f7zE),
              f7_name(f7zO, 'O', -16, 18), f7_name(f7zD, 'D', -6, -22), f7_name(f7zC, 'C', 18, 16), f7_name(f7zE, 'E', 0, 22),
              ('txt', 118, 255, '4', 'small', 26), ('txt', 175, 352, '4', 'ink', 24), ('txt', 345, 352, '4', 'ink', 24)]),
    ('oc8', [('txt', 200, 392, 'OC = 4 + 4 = 8', 'ink', 24)]),
    ('ang', [('arc', f7zC[0], f7zC[1], 56, 150, 180, 'small', '30°', 84), ('arc', 90, 330, 34, 0, 60, 'small', '60°', 56)]),
    ('dc', [('txt', 318, 232, '4√3', 'small', 26)]),
    ('area', [('txt', 200, 424, 'triangle: 4 · 4√3 ÷ 2', 'ink', 24), ('txt', 200, 456, '= 8√3', 'ink', 24)]),
    ('look', [('txt', 520, 200, '8√3 − (… with π)', 'ink', 24)]),
    ('circ', [('txt', 490, 392, 'circle: π · 4² = 16π', 'ink', 24)]),
    ('sec', [('wedge', 90, 330, f7zR, 0, 60, 'orange'), ('txt', 490, 424, 'sector: ⅙ of 16π = 8π/3', 'orange', 22),
             ('txt', 200, 296, '8π/3', 'orange', 24)]),
    ('ans', [('txt', 490, 456, 'shaded: 8√3 − 8π/3', 'ink', 24)]),
], vb='40 148 600 325', w=540, title='Triangle ODC, enlarged'))
for _g in (f7g95, f7g95b):
    _R(_g, 200)
video('solve-geo33-g095', 'solution', qid='geo33-g095', slides=[
    SM('Find the scheme', 'Find the scheme',
      L("A B C is a right triangle whose sides A B and A C are tangent to a circle with center O, at B and at D. B, O, E "
        "and C lie on one straight line, and E is on the circle. Given, O E and E C are both four centimeters. What is the "
        "area of the shaded region between C D, C E and the minor arc D E, in square centimeters?",
        pt('stem', 'A B C is a right triangle', 'hl', 14.0), voice='calm', pause=0.5),
      L("The minor arc is the small arc between D and E. So it's a shaded-area question again, and we need a scheme, what "
        "minus what.", pt('stem: ask', 'The minor arc is the small arc')),
      L("[short pause] The problem is that here the scheme isn't clear. Is it the big triangle minus a few pieces? It's "
        "not clear yet.", show(f7g95['line'], "here the scheme isn't clear")),
      L("What do we do in cases like this? We work with the givens, we put them on the figure, and we hope the solution "
        "shows itself."),
      L("A B is tangent to the circle at B. B is a point of tangency, and the right angle is already marked there, "
        "because the radius O B is perpendicular to the tangent.", show(f7g95['b'], 'the right angle is already marked')),
      L("D is also a point of tangency, but there's no radius to it. So we add the automatic construction, from O to D.",
        show(f7g95['dpts'], 'from O to D')),
      L("That's the radius O D, and we mark the right angle at D. It's the most basic construction there is.",
        show(f7g95['od'], "That's the radius O D")),
      L("How long is the radius? O E is a radius, and it's four. So O D is a radius too, and it's four.",
        show(f7g95['r4'], 'So O D is a radius too')),
      L("And now the scheme is clear. Take triangle O D C, and remove the sector D O E. What's left is exactly the shaded "
        "part. It's just like the last question.", show(f7g95['tri'], 'Take triangle O D C'),
        show(f7g95['cut'], 'remove the sector'))),
    SM('Triangle O D C', 'The gold triangle',
      L("[pause] Let's look at triangle O D C on its own, bigger. It has a right angle at D. One leg, O D, is four. The "
        "hypotenuse O C is O E plus E C, four plus four, eight.", show(f7g95b['line'], "Let's look at triangle O D C"),
        show(f7g95b['oc8'], 'four plus four, eight')),
      L("The area of a right triangle is leg times leg, over two. So we need the other leg, D C. Pythagoras would work, but "
        "there's no need.", pt('f7g95b_line', 'So we need the other leg')),
      L("Look, the hypotenuse is exactly twice the leg, eight and four. That happens only in a gold triangle, the thirty, "
        "sixty, ninety triangle. So the angle opposite the short leg, at C, is thirty degrees. And the angle opposite D C, "
        "at O, is sixty degrees.", show(f7g95b['ang'], 'So the angle opposite the short leg')),
      L("In a gold triangle, the long leg is root three times the short leg. So D C is four root three.",
        show(f7g95b['dc'], 'So D C is four root three')),
      L("Leg times leg, over two. Four times four root three is sixteen root three, and over two it's eight root three.",
        show(f7g95b['area'], 'Four times four root three')),
      L("Should we find the sector now? We saw in the last question that we can stop halfway and look at the choices. "
        "We're looking for eight root three, minus something with pi.", show(f7g95b['look'], "We're looking for eight root three")),
      L("Choice number two has sixteen root three, and choice number four has four root three. Neither has eight root "
        "three, so they're both out.", mk('cross', 'choice 2', 'Choice number two has'), mk('cross', 'choice 4', "so they're both out")),
      L("But this time the trick doesn't finish the job. Two choices start with eight root three, choice number one and "
        "choice number three. So we need the sector too."),
      L("The sector is a part of the circle. The whole circle is pi r squared, pi times four squared, sixteen pi.",
        show(f7g95b['circ'], 'The whole circle')),
      L("Which part? The central angle D O E is sixty degrees, and sixty out of three hundred sixty is a sixth. A sixth of "
        "sixteen pi is sixteen pi over six. Divide the top and the bottom by two, and it's eight pi over three.",
        show(f7g95b['sec'], 'Which part')),
      L("Choice number one has four pi over three. That's only half of our sector, so it's out. Only choice number three "
        "has both parts right, eight root three minus eight pi over three. Choice number three is our answer.",
        mk('cross', 'choice 1', "so it's out"), show(f7g95b['ans'], 'has both parts right'),
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("By the way, some students find the sector first. Then they look for something minus eight pi over three, and "
        "that rules out choice number one and choice number four. Here we need both parts, and together they leave only "
        "choice number three. [pause] Okay. I'll see you in the next question.", pt('f7g95b_line', 'some students find the sector first'))),
])

# ------------------------------------------------------------------------------------------------ geo33-g096 (Hebrew: the triangle in the semicircle)
# Hebrew (geo 4465-4572; Hebrew: triangle / bold shape = 3/(2 + pi); course: semicircle / triangle = (pi + 2)/3):
# "inscribed - circumscribed" questions, common at the edge: write the inscribed (or circumscribing) shape with the
# radius. Several approaches. Algebra: KM = KN = r -> at least isosceles, base angles equal, 60 and 60 -> equilateral,
# MN = r, perimeter 3r; the bold shape: "many students take half the circumference - only partly right": the diameter 2r
# plus half of 2 pi r = pi r; take r out as a common factor and cancel. Plugging in (recommended for almost everyone):
# repeat with r = 1, saves algebra mistakes; put 1 into the choices too (course: three choices tie at r = 1, so r = 2 is
# the tie-breaker). Estimating sizes with r = 1: every arc is longer than its chord (the shortest line), "1 plus" each ->
# 3 plus, the bold shape 5 plus, the triangle 3; pi/3 about 1, out; the answers with r: "an interesting distractor" - try
# r = 2, r = 3, the ratio would keep changing, but enlarging or shrinking the figure doesn't change it: perimeter over
# perimeter or area over area -> r must cancel, any answer with r is out at first glance (unless area over perimeter).
# V3: the copy; method 1: r on KM and KN with ticks, the 60s, MN = r, the arc (orange) and the diameter (teal) each with
# its length, the working below; method 2: the copy with 1s, the r = 1 line, then the r = 2 line; method 3: the three
# arcs over their dashed chords, "1+" on each; a clean generic pair of figures, one twice the other, for the scale idea.
f7K6, f7r6 = (320.0, 277.333), 182.5
f7M6, f7N6 = gpt(320, 277.333, f7r6, 120), gpt(320, 277.333, f7r6, 60)
f7P6, f7Q6 = (137.5, 277.333), (502.5, 277.333)
f7g96_base = [('arc', 320, 277.333, f7r6, 0, 180, 'ink'), ('arcw', 320, 277.333, f7r6, 0, 180, 'ink', 5), f7_seg(f7P6, f7Q6, 'ink', 5),
              f7_seg(f7K6, f7M6), f7_seg(f7M6, f7N6), f7_seg(f7N6, f7K6), ('dot', *f7K6),
              f7_name(f7K6, 'K', 0, 22), f7_name(f7M6, 'M', -16, -18), f7_name(f7N6, 'N', 16, -18),
              ('arc', f7M6[0], f7M6[1], 34, 300, 360, 'ink', '60°', 60)]
f7g96 = PIN(GEO('f7g96', [
    ('line', f7g96_base),
    ('rr', [('tick', *f7K6, *f7M6, 1), ('tick', *f7K6, *f7N6, 1), ('txt', 258, 206, 'r', 'small', 28, True), ('txt', 382, 206, 'r', 'small', 28, True)]),
    ('n60', [('arc', f7N6[0], f7N6[1], 34, 180, 240, 'small', '60°', 60), ('arc', 320, 277.333, 30, 60, 120, 'small', '60°', 52)]),
    ('mn', [('tick', *f7M6, *f7N6, 1), ('txt', 320, 104, 'r', 'small', 28, True)]),
    ('p3', [('txt', 320, 322, 'triangle: r + r + r = 3r', 'ink', 24)]),
    ('arc', [('arcw', 320, 277.333, f7r6, 0, 180, 'orange', 7), ('txt', 150, 150, 'πr', 'orange', 30)]),
    ('dia', [f7_seg(f7P6, f7Q6, 'teal', 7), ('txt', 440, 298, '2r', 'small', 28)]),
    ('ps', [('txt', 320, 352, 'semicircle: πr + 2r', 'ink', 24)]),
    ('ratio', [('txt', 320, 382, '(πr + 2r) / 3r = r(π + 2) / 3r', 'ink', 24), ('txt', 320, 412, '= (π + 2) / 3', 'ink', 26)]),
], vb='100 70 440 360', w=480, title='Triangle KMN in a semicircle'))
f7g96b = PIN(GEO('f7g96b', [
    ('line', f7g96_base),
    ('one', [('txt', 258, 206, '1', 'small', 28), ('txt', 382, 206, '1', 'small', 28), ('txt', 320, 104, '1', 'small', 28),
             ('txt', 150, 150, 'π', 'orange', 30), ('txt', 440, 298, '2', 'small', 28)]),
    ('r1', [('txt', 320, 322, 'r = 1:  (π + 2) / 3', 'ink', 24)]),
    ('tie', [('txt', 320, 352, 'choices 2, 3, 4:  all (π + 2) / 3', 'red', 22)]),
    ('r2', [('txt', 320, 382, 'r = 2:  (2π + 4) / 6 = (π + 2) / 3', 'ink', 24)]),
], vb='100 70 440 330', w=480, title='Plug in a number for r'))
f7g96c = PIN(GEO('f7g96c', [
    ('line', f7g96_base),
    ('chords', [f7_seg(f7P6, f7M6, 'teal', 3, True), f7_seg(f7N6, f7Q6, 'teal', 3, True), ('txt', 258, 206, '1', 'small', 26),
                ('txt', 382, 206, '1', 'small', 26), ('txt', 320, 132, '1', 'small', 26), ('txt', 196, 250, '1', 'small', 26),
                ('txt', 444, 250, '1', 'small', 26)]),
    ('plus', [('arcw', 320, 277.333, f7r6, 0, 60, 'orange', 6), ('arcw', 320, 277.333, f7r6, 60, 120, 'orange', 6),
              ('arcw', 320, 277.333, f7r6, 120, 180, 'orange', 6), ('txt', 140, 150, '1+', 'orange', 26),
              ('txt', 320, 82, '1+', 'orange', 26), ('txt', 500, 150, '1+', 'orange', 26)]),
    ('tot', [('txt', 320, 322, 'semicircle: 2 + (more than 3) = 5+', 'ink', 22), ('txt', 320, 352, 'triangle: 3', 'ink', 22),
             ('txt', 320, 382, 'ratio: about 5+ / 3', 'ink', 24)]),
], vb='100 70 440 330', w=480, title='Estimating sizes with r = 1'))
f7sK1, f7sK2 = (110.0, 250.0), (390.0, 250.0)
def f7_semi(K, r, lab, tri_lab):
    M, N = gpt(K[0], K[1], r, 120), gpt(K[0], K[1], r, 60)
    return [('arc', K[0], K[1], r, 0, 180, 'ink'), f7_seg((K[0] - r, K[1]), (K[0] + r, K[1]), 'ink', 4), f7_seg(K, M), f7_seg(M, N), f7_seg(N, K),
            ('txt', K[0], K[1] + 30, lab, 'small', 22), ('txt', K[0], K[1] + 58, tri_lab, 'orange', 22)]
f7g96d = PIN(GEO('f7g96d', [
    ('line', f7_semi(f7sK1, 80, 'semicircle π + 2', 'triangle 3')),
    ('big', f7_semi(f7sK2, 160, 'semicircle 2π + 4', 'triangle 6') + [('txt', 205, 120, '× 2', 'red', 32)]),
    ('same', [('txt', 280, 345, 'both × 2: the ratio stays the same', 'ink', 24)]),
], vb='10 70 560 290', w=540, title='The same figure, twice as big'))
for _g in (f7g96, f7g96b, f7g96c, f7g96d):
    _R(_g, 200)
video('solve-geo33-g096', 'solution', qid='geo33-g096', slides=[
    SM('Method 1 · The math way', 'Algebra',
      L("A semicircle has center K and radius r. M and N lie on its curved boundary, and angle K M N is sixty degrees. "
        "What is the ratio of the perimeter of the semicircle to the perimeter of triangle K M N?",
        pt('stem', 'A semicircle has center K', 'hl', 10.0), voice='calm', pause=0.5),
      L("So they ask for the perimeter of the semicircle, divided by the perimeter of the triangle. [short pause] There's "
        "a shape inside a circle here. We call these inscribed and circumscribed questions, and they're common at the end "
        "of the section.", pt('stem: ask', 'So they ask for the perimeter')),
      L("What do we do in them? We write the lengths of both shapes with the radius of the circle. We'll solve it three "
        "ways, the math way, by plugging in a number, and by estimation."),
      L("[short pause] The math way first. K M and K N are radii, so each one is r. So the triangle is at least isosceles, and "
        "its base angles are equal.", show(f7g96['line'], 'The math way first'), show(f7g96['rr'], 'K M and K N are radii')),
      L("The angle at M is sixty, so the angle at N is sixty too. That leaves sixty for the angle at K. An isosceles "
        "triangle with a sixty-degree angle is equilateral, so M N is r too.", show(f7g96['n60'], 'the angle at N is sixty'),
        show(f7g96['mn'], 'so M N is r too')),
      L("So the perimeter of the triangle is r plus r plus r, three r.", show(f7g96['p3'], 'three r')),
      L("Now the semicircle. A lot of students take half of the circumference. That's only partly right. The perimeter "
        "has two parts, the curved part on top and the straight line at the bottom."),
      L("The curved part is half of the circumference. The circumference is two pi r, and half of it is pi r.",
        show(f7g96['arc'], 'The curved part is half')),
      L("The straight line is the diameter, two radii, so it's two r. So the perimeter of the semicircle is pi r plus two "
        "r.", show(f7g96['dia'], 'The straight line is the diameter'), show(f7g96['ps'], 'So the perimeter of the semicircle')),
      L("Now we divide, pi r plus two r, over three r. In the top, take r out as a common factor, so it's r times, in "
        "brackets, pi plus two. Now r is multiplied on the top and on the bottom, so we cancel it. We get pi plus two, "
        "over three. Choice number three is our answer.", show(f7g96['ratio'], 'Now we divide'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Plugging in numbers', 'Plugging in a number',
      L("[pause] Now the way I recommend for almost everyone, plugging in a number. Instead of the letter r, we pick an "
        "easy number for the radius, and we solve with numbers. Then we put the same number into the choices, and the "
        "right choice gives the same value. It saves us the algebra mistakes.", show(f7g96b['line'], 'plugging in a number')),
      L("The easiest number is one, so the radius is one. K M and K N are one, and the triangle is equilateral, so M N "
        "is one too. The triangle's perimeter is three.", show(f7g96b['one'], 'so the radius is one')),
      L("The semicircle has a curved part, half of two pi, which is pi. And the diameter is two. So the ratio is pi plus "
        "two, over three.", show(f7g96b['r1'], 'So the ratio is pi plus')),
      L("Now we put r equals one into the choices. Choice number one is pi over three, and that's different, so it's out. "
        "But in choices two, three and four, multiplying or dividing by one changes nothing. All three give pi plus two, "
        "over three.", mk('cross', 'choice 1', "so it's out"), show(f7g96b['tie'], 'All three give')),
      L("That's a tie, so one isn't a good number here. We need another number to break the tie, so let's take r equals "
        "two."),
      L("The triangle is two, two and two, so its perimeter is six. The curved part is half of two pi times two, so it's "
        "two pi. The diameter is four. So the ratio is two pi plus four, over six. Divide the top and the bottom by two, "
        "and it's pi plus two, over three.", show(f7g96b['r2'], 'The triangle is two, two and two')),
      L("Now r equals two in the choices. Choice number two divides by three r, which is six, so it's pi plus two over "
        "six. That's half of our value, so it's out. Choice number four multiplies by r, so it's twice our value. It's out "
        "too.", mk('cross', 'choice 2', 'That\'s half of our value'), mk('cross', 'choice 4', "It's out too")),
      L("Only choice number three gives pi plus two, over three. Choice number three again.",
        mk('tick', 'choice 3', 'Choice number three again'))),
    SM('Method 3 · Estimation', 'Estimating sizes',
      L("[pause] And the third way, estimation. Say the radius is one again. The triangle is equilateral, so each "
        "of its sides is one, and its perimeter is three.", show(f7g96c['line'], 'Say the radius is one again')),
      L("Now the curved part. The radii to M and N cut it into three arcs. Under each arc there's a straight line of "
        "length one, because the three small triangles at K are all equilateral, with sixty degrees each.",
        show(f7g96c['chords'], 'Under each arc')),
      L("And a straight line is the shortest way between two points. So each arc is a bit longer than one. Let's write one "
        "plus.", show(f7g96c['plus'], 'Let\'s write one plus')),
      L("So the curved part is a bit more than three. Add the diameter, two, and the semicircle is a bit more than five. "
        "The triangle is three. So the ratio is about five plus, over three.", show(f7g96c['tot'], 'So the curved part')),
      L("Choice number one, pi over three. Pi is less than four, so this is less than four over three. We need more than "
        "five over three, so it's out.", mk('cross', 'choice 1', "so it's out"))),
    SM('Method 3 · Estimation', 'Estimating sizes',
      L("[pause] Choices two and four have r in them. They're interesting distractors. If r were two, choice number two "
        "would be pi plus two over six. If r were three, it would be pi plus two over nine. The ratio would keep changing."),
      L("But look. Here's the same figure, and next to it the same figure twice as big. Every length is twice as long, "
        "so both perimeters are twice as big.", show(f7g96d['line'], "Here's the same figure"),
        show(f7g96d['big'], 'twice as big')),
      L("The semicircle goes from pi plus two to two pi plus four, and the triangle goes from three to six. When we divide, "
        "the two cancels. So when we make the figure bigger or smaller, the ratio doesn't change.",
        show(f7g96d['same'], 'the ratio doesn\'t change')),
      L("So when they ask for a perimeter over a perimeter, or an area over an area, the radius must cancel. Any choice "
        "with r in it is a distractor, and it's out at first glance. Choice number two and choice number four are out.",
        mk('cross', 'choice 2', 'Choice number two and'), mk('cross', 'choice 4', 'choice number four are out')),
      L("Careful, that's only for the same kind of thing. In an area over a perimeter, an r can stay, because an area has "
        "r squared and a perimeter has only r."),
      L("Choice number three is pi plus two, over three. Pi plus two is a bit more than five, so it's about five plus over "
        "three, just what we estimated. Choice number three again. [pause] Okay. I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three again'))),
])

# ------------------------------------------------------------------------------------------------ geo33-g097 (Hebrew: square, circle, square)
# Hebrew (geo 4575-4619; Hebrew big / small = 2, course small / big = 1/2): inscribed - circumscribed again; start with the
# exam way, plug in r = 1 (no need for letters); the outer side equals the diameter, 2 -> area 4; the inner square: many
# students go through silver triangles (1, 1 -> root 2, then square it) - possible but a bit long; a square's area is
# also diagonal times diagonal over 2, and its diagonals are diameters, 2 each -> 2; r appears in no choice; 2/4. The
# shortcut, symmetry: draw the diagonals of the inner square; the big square is made of 8 identical triangles and the
# small one of 4 (each pair: a diagonal halves a small square).
# V3: the copy; method 1: the radius 1 dashed, the outer side and the diameter (2), the corner silver triangle tinted
# orange (1, 1, root 2), then the inner square's diagonals dashed with 2; the working beside the figure; method 2: the
# diagonals dashed, one small square outlined with its two halves (teal inside, orange outside), then all eight.
f7K7, f7L7, f7M7, f7N7 = (210.5, 70.5), (210.5, 289.5), (429.5, 289.5), (429.5, 70.5)
f7O7, f7r7 = (320.0, 180.0), 109.5
f7P7, f7Q7, f7R7, f7S7 = (320.0, 70.5), (210.5, 180.0), (320.0, 289.5), (429.5, 180.0)
f7g97_base = (f7_poly([f7K7, f7L7, f7M7, f7N7]) + [('circ', f7O7[0], f7O7[1], f7r7)] + f7_poly([f7P7, f7Q7, f7R7, f7S7])
              + [('tint', [f7P7, f7Q7, f7R7, f7S7], 'ink'), ('dot', *f7O7),
                 f7_name(f7O7, 'O', 12, 17, 'ink', 22), f7_name(f7K7, 'K', -16, -16), f7_name(f7L7, 'L', -16, 16), f7_name(f7M7, 'M', 16, 16),
                 f7_name(f7N7, 'N', 16, -16), f7_name(f7P7, 'P', 0, -21), f7_name(f7Q7, 'Q', -21, 0), f7_name(f7R7, 'R', 0, 21),
                 f7_name(f7S7, 'S', 21, 0)])
f7g97 = PIN(GEO('f7g97', [
    ('line', f7g97_base),
    ('r1', [f7_seg(f7O7, (f7O7[0] + f7r7 * 0.707, f7O7[1] + f7r7 * 0.707), 'teal', 3, True), ('txt', 372, 218, '1', 'small', 24),
            ('txt', 570, 60, 'r = 1', 'small', 26)]),
    ('side', [f7_seg(f7L7, f7M7, 'orange', 6), ('txt', 375, 311, '2', 'orange', 26), f7_seg(f7Q7, f7S7, 'teal', 3, True),
              ('txt', 270, 166, '2', 'small', 24)]),
    ('big', [('txt', 570, 100, 'KLMN: 2 · 2 = 4', 'ink', 24)]),
    ('silver', [('tint', [f7K7, f7P7, f7Q7], 'orange'), ('txt', 265, 58, '1', 'orange', 22), ('txt', 198, 125, '1', 'orange', 22),
                ('txt', 250, 112, '√2', 'orange', 22), ('txt', 570, 140, 'side √2: (√2)² = 2', 'orange', 22)]),
    ('diag', [f7_seg(f7P7, f7R7, 'teal', 3, True), ('txt', 332, 248, '2', 'small', 24),
              ('txt', 570, 180, 'or 2 · 2 ÷ 2 = 2', 'small', 24)]),
    ('ratio', [('txt', 570, 225, '2 / 4 = 1/2', 'ink', 28)]),
], vb='150 25 520 310', w=500, title='Square KLMN around the circle, square PQRS inside it'))
f7g97b = PIN(GEO('f7g97b', [
    ('line', f7g97_base),
    ('mid', [f7_seg(f7P7, f7R7, 'teal', 3, True), f7_seg(f7Q7, f7S7, 'teal', 3, True)]),
    ('pair', [('path', [f7K7, f7P7, f7O7, f7Q7, f7K7], 'ink', 5), ('tint', [f7K7, f7P7, f7Q7], 'orange'), ('tint', [f7P7, f7O7, f7Q7], 'teal')]),
    ('all', [('tint', [f7P7, f7N7, f7S7], 'orange'), ('tint', [f7S7, f7M7, f7R7], 'orange'), ('tint', [f7R7, f7L7, f7Q7], 'orange'),
             ('tint', [f7P7, f7O7, f7S7], 'teal'), ('tint', [f7S7, f7O7, f7R7], 'teal'), ('tint', [f7R7, f7O7, f7Q7], 'teal'),
             ('txt', 570, 80, '8 equal triangles', 'ink', 22), ('txt', 570, 115, 'PQRS: 4 of them', 'small', 22)]),
    ('ratio', [('txt', 570, 160, '4 / 8 = 1/2', 'ink', 28)]),
], vb='150 25 520 310', w=500, title='Eight equal triangles'))
for _g in (f7g97, f7g97b):
    _R(_g, 200)
video('solve-geo33-g097', 'solution', qid='geo33-g097', slides=[
    SM('Method 1 · Plugging in numbers', 'Plugging in a number',
      L("Square K L M N is circumscribed about a circle, and square P Q R S is inscribed in the circle. What is the ratio "
        "of the area of P Q R S to the area of K L M N?", pt('stem', 'Square K L M N is circumscribed', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("Circumscribed means the big square is around the circle, and the circle touches its sides. Inscribed means the "
        "small square is inside the circle, with its corners on the circle. So they ask for the small square's area over "
        "the big square's area.", pt('stem: ask', 'So they ask for the small')),
      L("[short pause] It's an inscribed and circumscribed question again. We'll solve it by plugging in a number, and "
        "then with a symmetry shortcut."),
      L("No length is given, and the size of the figure doesn't change a ratio of areas. So we don't need letters. Like in "
        "the last question, we pick an easy radius, one.", show(f7g97['line'], 'we pick an easy radius'),
        show(f7g97['r1'], 'an easy radius, one')),
      L("Look at the big square's side, L M. It's as long as the diameter of the circle, because the circle touches both "
        "sides. So the side is two, and the area is two times two, four.", show(f7g97['side'], "Look at the big square's side"),
        show(f7g97['big'], 'the area is two times two')),
      L("Now the small square. A lot of students go through silver triangles. In the corner at K there's a silver "
        "triangle with legs of one and one, so its hypotenuse, the small square's side, is root two. Squaring it, the area "
        "is two.", show(f7g97['silver'], 'In the corner at K')),
      L("That's possible, but it's a bit long. A square's area is also diagonal times diagonal, over two. And the "
        "diagonals of P Q R S are diameters of the circle, two each. Two times two, over two, is two.",
        show(f7g97['diag'], 'the diagonals of P Q R S')),
      L("So the small square over the big one is two over four, a half. None of the choices has r in it, so we just look "
        "for a half. Choice number two is our answer.", show(f7g97['ratio'], 'two over four'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · Understanding: symmetry', 'Symmetry',
      L("[pause] Here there's also a shortcut, with symmetry. Draw the diagonals of the small square, P R and Q S. They "
        "cut the big square into four small squares.", show(f7g97b['line'], 'Here there\'s also a shortcut'),
        show(f7g97b['mid'], 'Draw the diagonals')),
      L("Look at the small square in the corner at K. The side P Q is its diagonal, so it cuts it into two identical "
        "triangles. One is inside P Q R S, and one is outside.", show(f7g97b['pair'], 'Look at the small square')),
      L("It's the same in every corner. So the big square is made of eight identical triangles, and P Q R S is made of "
        "four of them.", show(f7g97b['all'], 'the same in every corner')),
      L("Four out of eight is a half. So the big square is twice the small one, and the answer is a half. Choice number "
        "two again. [pause] Okay. I'll see you in the next question.", show(f7g97b['ratio'], 'Four out of eight'),
        mk('tick', 'choice 2', 'Choice number two again'))),
])

# ------------------------------------------------------------------------------------------------ geo-097-after (lesson: three nested shapes)
# Hebrew (geo 4620-4636): three objects that show up now and then; knowing them by heart saves precious time. Square,
# circle, square: the outer area is always twice the inner (a question like the last one, near the end - mark it
# automatically; it has appeared a few times); the outer side is root 2 times the inner. Circle, square, circle: almost
# the same, the outer circle's area exactly twice, the outer radius root 2 times. Triangle, circle, triangle (equilateral
# only): the outer area is 4 times the inner, the outer side twice. ("We didn't prove it; you can sit and prove it" - the
# course shows a short why for each, with r = 1 numbers.)
# V3: three clean generic figures (col 0), each built shape by shape from the outside in; the eight triangles (teal
# inside, orange outside); the radius 1, the side 2, the diagonal 2 root 2 and the big radius root 2 written as found;
# the triangle cut into four equal triangles (teal inside, orange corners), the midpoints ticked. The rules typed on
# the right.
f7ac, f7ah = (200.0, 200.0), 150.0
f7aS = [(50, 50), (50, 350), (350, 350), (350, 50)]
f7aI = [(200, 50), (50, 200), (200, 350), (350, 200)]
f7nA = PIN(GEO('f7nA', [
    ('line', f7_poly(f7aS)),
    ('circ', [('circ', 200, 200, 150)]),
    ('in', f7_poly(f7aI)),
    ('eight', [('seg', 200, 50, 200, 350, 'teal', 2.5, True), ('seg', 50, 200, 350, 200, 'teal', 2.5, True), ('tint', f7aI, 'teal'),
               ('tint', [(50, 50), (200, 50), (50, 200)], 'orange'), ('tint', [(200, 50), (350, 50), (350, 200)], 'orange'),
               ('tint', [(350, 200), (350, 350), (200, 350)], 'orange'), ('tint', [(50, 200), (50, 350), (200, 350)], 'orange')]),
    ('sides', [('txt', 200, 374, '2', 'orange', 28), ('txt', 112, 112, '√2', 'small', 28), ('txt', 215, 245, '1', 'small', 24),
               f7_seg((200, 200), (200, 350), 'small', 4)]),
], vb='20 20 360 375', w=560, col=0, title='Square, circle, square'))
f7bS = [(100, 100), (100, 300), (300, 300), (300, 100)]
f7nB = PIN(GEO('f7nB', [
    ('line', [('circ', 200, 200, 141.4)]),
    ('sq', f7_poly(f7bS)),
    ('in', [('circ', 200, 200, 100)]),
    ('r', [('dot', 200, 200), f7_seg((200, 200), (200, 300), 'teal', 3, True), ('txt', 213, 255, '1', 'small', 26)]),
    ('side', [f7_seg((100, 300), (300, 300), 'orange', 5), ('txt', 150, 320, '2', 'orange', 26)]),
    ('diag', [f7_seg((100, 300), (300, 100), 'teal', 3, True), ('txt', 135, 238, '2√2', 'small', 24)]),
    ('R', [f7_seg((200, 200), (300, 100), 'orange', 5), ('txt', 270, 165, '√2', 'orange', 26)]),
], vb='40 40 320 335', w=560, col=0, title='Circle, square, circle'))
f7cA, f7cB, f7cC = (200.0, 35.56), (30.0, 330.0), (370.0, 330.0)
f7cI = [f7_mid(f7cB, f7cC), f7_mid(f7cA, f7cB), f7_mid(f7cA, f7cC)]
f7nC = PIN(GEO('f7nC', [
    ('line', f7_poly([f7cA, f7cB, f7cC])),
    ('circ', [('circ', 200, 231.85, 98.15)]),
    ('in', f7_poly(f7cI)),
    ('four', [('tint', f7cI, 'teal'), ('tint', [f7cA, f7cI[1], f7cI[2]], 'orange'), ('tint', [f7cB, f7cI[0], f7cI[1]], 'orange'),
              ('tint', [f7cC, f7cI[0], f7cI[2]], 'orange'),
              ('tick', *f7cB, *f7cI[0], 1), ('tick', *f7cI[0], *f7cC, 1), ('tick', *f7cB, *f7cI[1], 1), ('tick', *f7cI[1], *f7cA, 1),
              ('tick', *f7cA, *f7cI[2], 1), ('tick', *f7cI[2], *f7cC, 1)]),
    ('sides', [('txt', 200, 168, '1', 'small', 26), ('txt', 115, 352, '1', 'orange', 26), ('txt', 285, 352, '1', 'orange', 26)]),
], vb='0 15 400 355', w=560, col=0, title='Triangle, circle, triangle'))
f7t1 = I('f7t1', 'Outer area $=2\\times$ inner area', size=30, col=1)
f7t2 = I('f7t2', 'Outer side $=\\sqrt2\\times$ inner side', size=30, col=1)
f7t3 = IH('f7t3', 'Areas: $\\pi\\cdot1^2=\\pi$, $\\ \\pi\\cdot(\\sqrt2)^2=2\\pi$', size=30, col=1)
f7t4 = I('f7t4', 'Outer area $=2\\times$ inner area', size=30, col=1)
f7t5 = I('f7t5', 'Outer radius $=\\sqrt2\\times$ inner radius', size=30, col=1)
f7t6 = I('f7t6', 'Equilateral triangles only', size=30, col=1)
f7t7 = I('f7t7', 'Outer area $=4\\times$ inner area', size=30, col=1)
f7t8 = I('f7t8', 'Outer side $=2\\times$ inner side', size=30, col=1)
f7t9 = I('f7t9', 'Sides $\\times\\sqrt2$ $\\to$ areas $\\times2$', size=30, col=1)
f7t10 = I('f7t10', 'Sides $\\times2$ $\\to$ areas $\\times4$', size=30, col=1)
video('geo-097-after', 'lesson', slides=[
    S('Three Nested Shapes',
      L("I want to use the last question to show you three objects that show up on the exam every now and then. If you "
        "know them by heart, you save precious time.")),
    S('Square, circle, square',
      L("The first one is square, circle, square. A square, a circle inside it, and a square inside the circle. It's "
        "exactly the case we just solved.", show(f7nA['line'], 'The first one is square'), show(f7nA['circ'], 'a circle inside it'),
        show(f7nA['in'], 'a square inside the circle')),
      L("We saw that the big square is made of eight identical triangles, and the small square of four. So the outer "
        "square's area is always twice the inner square's area.", show(f7nA['eight'], 'eight identical triangles'),
        show(f7t1, "the outer square's area is always twice")),
      L("A question like the last one comes near the end of the section, and it has appeared a few times. If you know "
        "this, you mark the answer at once.", pt('f7t1', 'If you know this')),
      L("It's also worth knowing the sides. With a radius of one, the outer side is two, and the inner side is root two. "
        "Two is root two times root two, so the outer side is root two times the inner side.",
        show(f7nA['sides'], 'With a radius of one'), show(f7t2, 'the outer side is root two times'))),
    S('Circle, square, circle',
      L("The second one is circle, square, circle. A circle, a square inside it, and a circle inside the square. It's "
        "almost the same case.", show(f7nB['line'], 'The second one is circle'), show(f7nB['sq'], 'a square inside it'),
        show(f7nB['in'], 'a circle inside the square')),
      L("Why? Say the small radius is one. The small circle touches the square's sides, so the square's side is a "
        "diameter, two.", show(f7nB['r'], 'Say the small radius is one'), show(f7nB['side'], "so the square's side")),
      L("The square's diagonal makes a silver triangle with two sides, so it's two root two. And that diagonal is a "
        "diameter of the big circle, so the big radius is half of it, root two.", show(f7nB['diag'], "The square's diagonal"),
        show(f7nB['R'], 'so the big radius is half')),
      L("So the outer radius is root two times the inner radius. Now the areas. The small circle is pi times one squared, "
        "pi. The big circle is pi times root two, squared, which is two pi.", show(f7t5, 'So the outer radius'), show(f7t3, 'Now the areas')),
      L("So again, the outer circle's area is exactly twice the inner circle's area.", show(f7t4, "the outer circle's area"))),
    S('Triangle, circle, triangle',
      L("The third and last one is triangle, circle, triangle. But only with equilateral triangles.",
        show(f7nC['line'], 'The third and last one'), show(f7nC['circ'], 'triangle, circle, triangle'),
        show(f7nC['in'], 'But only with equilateral'), show(f7t6, 'only with equilateral')),
      L("Here it's different. The outer triangle isn't twice the inner one, it's four times as big. And the outer side is "
        "twice the inner side.", show(f7t7, "it's four times as big"), show(f7t8, 'the outer side is')),
      L("Why? The circle touches each side of the big triangle right in its middle, because the equilateral triangle is "
        "symmetric. Turn the small triangle upside down, like here. Turning it doesn't change its size. Now its corners "
        "touch those middles.", show(f7nC['four'], 'right in its middle')),
      L("So the big triangle is cut into four equal triangles, and the small one is one of them. Its area is a quarter, "
        "and its side is half of the big side.", show(f7nC['sides'], 'cut into four equal triangles')),
      L("Now, this is important. A length factor isn't an area factor. Sides times root two give areas times two, and "
        "sides times two give areas times four.", show(f7t9, 'Sides times root two'), show(f7t10, 'sides times two give')),
      L("Learn these three objects by heart. [pause] Okay. I'll see you in the next video.", pt('f7t10', 'Learn these three'))),
])

# =================================================================================================================
# Topic-33 advanced block, part 2 (fragment f8, TAG H, 2026-10-14): geo33-g098 .. geo33-g102 (Hebrew geo 4669-5095).
# Question figure on the left (FIG_LEFT), our colour copy of it on the right, built step by step (Rule V3).
# =================================================================================================================
FIG_LEFT.update({'solve-geo33-g098', 'solve-geo33-g099', 'solve-geo33-g100', 'solve-geo33-g101', 'solve-geo33-g102'})


def f8_lab(items, size=24):
    return [('txt', x, y, t, 'ink', size, True) for x, y, t in items]


# ------------------------------------------------------------------------------------------------ geo33-g098 (Hebrew 4669-4762)
# Hebrew: an arc length needs a central angle; none on AG or ED, so a construction (radii AO, OD); the inscribed angle at
# B stands on the whole arc AF -> one more radius OF, central = 2 x; the same for C on FD; "lots of givens, lots of mess";
# each end angle alone is impossible, the sum is possible: AOD minus GOE; "maybe 30-30, maybe 20-40, I don't know and it
# doesn't matter" - the figure MOVED to show the sum stays; arc = part of the circumference. Course numbers: r 8, 28, 57,
# 80 -> 56 + 114 = 170, 170 - 80 = 90, a quarter of 16 pi = 4 pi.
# V3: the copy; the two target arcs traced teal; dashed radii OA, OD; angle B and its arc AF (drawn just outside the
# circle) teal, dashed OF and 56; angle C, arc FD orange, 114; the two end sectors tinted teal; 170 - 80 = 90 written.
# The "it doesn't matter" move: a clean generic pair of circles, the grey middle part in two positions.
f8c = (320.0, 180.0); f8R = 109.5
f8P = {k: gpt(320, 180, f8R, a) for k, a in dict(A=0, G=20, F=56, E=100, D=170, B=215, C=290).items()}
f8_98base = ([('circ', 320, 180, f8R)]
             + [('seg', *f8P[a], *f8P[b]) for a, b in (('B', 'A'), ('B', 'F'), ('C', 'F'), ('C', 'D'))]
             + [('seg', 320, 180, *f8P['G']), ('seg', 320, 180, *f8P['E']), ('dot', 320, 180),
                ('arcw', 320, 180, f8R, 0, 20, 'ink', 6), ('arcw', 320, 180, f8R, 100, 170, 'ink', 6),
                ('arc', 320, 180, 16, 20, 100, 'ink'), ('txt', 331, 124, '80°', 'ink', 20),
                ('arc', *f8P['B'], 34, 17.5, 45.5, 'ink'), ('txt', 290, 206, '28°', 'ink', 18),
                ('arc', *f8P['C'], 34, 83.0, 140.0, 'ink'), ('txt', 336, 232, '57°', 'ink', 18)]
             + f8_lab([(451, 180, 'A'), (443, 134, 'G'), (393, 70, 'F'), (297, 51, 'E'), (190, 157, 'D'), (212, 256, 'B'),
                       (366, 303, 'C'), (303, 197, 'O')]))
f8g98 = PIN(GEO('f8g98', [
    ('line', f8_98base),
    ('arcs', [('arcw', 320, 180, f8R, 0, 20, 'teal', 8), ('arcw', 320, 180, f8R, 100, 170, 'teal', 8)]),
    ('radii', [('dot', *f8P['A']), ('dot', *f8P['D']), ('seg', 320, 180, *f8P['A'], 'teal', 3, True),
               ('seg', 320, 180, *f8P['D'], 'teal', 3, True)]),
    ('af', [('path', [f8P['A'], f8P['B'], f8P['F']], 'teal', 6), ('arc', *f8P['B'], 34, 17.5, 45.5, 'small'),
            ('arcw', 320, 180, f8R + 11, 0, 56, 'teal', 4)]),
    ('of', [('dot', *f8P['F']), ('seg', 320, 180, *f8P['F'], 'teal', 3, True), ('arc', 320, 180, 30, 0, 56, 'small'),
            ('txt', 364, 150, '56°', 'teal', 22)]),
    ('fd', [('path', [f8P['F'], f8P['C'], f8P['D']], 'orange', 6), ('arc', *f8P['C'], 34, 83.0, 140.0, 'large'),
            ('arcw', 320, 180, f8R + 11, 56, 170, 'orange', 4), ('arc', 320, 180, 40, 56, 170, 'large'),
            ('txt', 262, 150, '114°', 'orange', 22)]),
    ('ends', [('wedge', 320, 180, f8R, 0, 20, 'teal'), ('wedge', 320, 180, f8R, 100, 170, 'teal')]),
    ('sum', [('txt', 250, 322, '170° − 80° = 90°', 'teal', 24)]),
], vb='165 35 300 300', w=400, title='Circle O with the arcs AG and ED'))

f8mv_l, f8mv_r = (160.0, 150.0), (480.0, 150.0); f8r2 = 100


def f8_split(cx, cy, g, e, a1, a2):
    """the middle part (grey, 80) from g to e, and the two end sectors (teal) with their sizes"""
    return [('wedge', cx, cy, f8r2, g, e, 'ink'), ('seg', cx, cy, *gpt(cx, cy, f8r2, g), 'ink', 3),
            ('seg', cx, cy, *gpt(cx, cy, f8r2, e), 'ink', 3), ('txt', *gpt(cx, cy, 62, (g + e) / 2.0), '80°', 'ink', 20),
            ('wedge', cx, cy, f8r2, 0, g, 'teal'), ('wedge', cx, cy, f8r2, e, 170, 'teal'),
            ('txt', *gpt(cx, cy, 120, g / 2.0), '%d°' % g, 'teal', 22), ('txt', *gpt(cx, cy, 122, (e + 170) / 2.0), '%d°' % (170 - e), 'teal', 22),
            ('txt', cx, cy + 128, '%d° + %d° = 90°' % (g, 170 - e), 'teal', 22)]


f8mv = PIN(GEO('f8mv', [
    ('line', [x for c in (f8mv_l, f8mv_r) for x in
              [('circ', c[0], c[1], f8r2), ('dot', c[0], c[1]), ('seg', c[0], c[1], *gpt(c[0], c[1], f8r2, 0), 'teal', 3, True),
               ('seg', c[0], c[1], *gpt(c[0], c[1], f8r2, 170), 'teal', 3, True),
               ('txt', gpt(c[0], c[1], f8r2, 0)[0] + 18, c[1], 'A', 'ink', 22, True),
               ('txt', gpt(c[0], c[1], f8r2, 170)[0] - 18, gpt(c[0], c[1], f8r2, 170)[1], 'D', 'ink', 22, True),
               ('txt', c[0] + 2, c[1] + 20, 'O', 'ink', 20, True)]]),
    ('p1', f8_split(*f8mv_l, 20, 100, 0, 170)),
    ('p2', f8_split(*f8mv_r, 50, 130, 0, 170)),
], vb='30 25 590 300', w=560, title='The middle part in two places'))
f8a1 = I('f8a1', '$2\\pi\\cdot8=16\\pi$', size=32, col=1)
f8a2 = I('f8a2', '$\\frac{90}{360}=\\frac14,\\quad \\frac14\\cdot16\\pi=4\\pi$', size=32, col=1, hand='{90/360} = {1/4},     {1/4}·16π = 4π')
f8k98 = I('f8k98', 'So far: $\\ \\angle AOG+\\angle EOD=90°$', size=26, col=1)
video('solve-geo33-g098', 'solution', qid='geo33-g098', slides=[
    SM('Central angles', 'Central angles',
      L("A circle with center O has a radius of eight centimeters. A, G, F, E and D lie on the same arc, in that order, and "
        "B and C lie on the other arc between A and D. Angle A B F is twenty-eight degrees, angle F C D is fifty-seven "
        "degrees, and angle G O E is eighty degrees. What is the sum of the lengths of the highlighted arcs, A G and E D?",
        pt('stem', 'A circle with center O', 'hl', 12.0), voice='calm', pause=0.5),
      L("So they want the two bold arcs together. To find the length of an arc, we first need its central angle. But no "
        "central angle stands on arc A G, or on arc E D. So we need a construction, and it's a natural one, because we "
        "must have central angles. Let's draw the radius O A and the radius O D.",
        show(f8g98['line'], 'So they want'), show(f8g98['arcs'], 'the two bold arcs together'),
        show(f8g98['radii'], "Let's draw the radius O A")),
      L("Now let's use the givens. Angle B is twenty-eight degrees. Which arc does it stand on? On A G plus G F, so on the "
        "whole arc A F. An inscribed angle doesn't give us a central angle directly. But remember, the central angle on "
        "the same arc is twice as big.", show(f8g98['af'], 'Angle B is twenty-eight degrees')),
      L("No central angle is drawn on arc A F, so let's draw one more radius, O F. Now angle A O F is two times "
        "twenty-eight, fifty-six degrees.", show(f8g98['of'], 'one more radius, O F')),
      L("Next, angle C is fifty-seven degrees, and it stands on arc F D. The central angle on that arc is twice as big, two "
        "times fifty-seven, a hundred fourteen degrees.", show(f8g98['fd'], 'angle C is fifty-seven')),
      L("That's a lot of givens and a lot of lines, so let's find our way. We need the two angles at the ends, angle A O G "
        "and angle E O D. We can't find each one alone. But we can find their sum.",
        show(f8g98['ends'], 'We need the two angles at the ends')),
      L("Together with the middle angle, G O E, they make the whole angle A O D. That's fifty-six plus a hundred fourteen, "
        "a hundred seventy degrees. Take away the middle angle, eighty, and the two end angles together are a hundred "
        "seventy minus eighty, ninety degrees.", show(f8g98['sum'], 'Take away the middle angle'))),
    SM('The sum, not each one', 'The sum, not each one',
      L("How is the ninety split between the two? Maybe forty-five and forty-five, maybe twenty and seventy. We don't know, "
        "and it doesn't matter. Let's see why. Here's only what we need, the angle A O D, a hundred seventy degrees.",
        show(f8mv['line'], "Here's only what we need")),
      L("Say the middle part, the eighty, sits here, in grey. Then the end angles are twenty and seventy, and together "
        "they're ninety.", show(f8mv['p1'], 'Say the middle part')),
      L("Now slide the whole middle part along the circle. The end angles change, to fifty and forty, but together they're "
        "still ninety. Wherever the middle part sits, the two ends always add up to a hundred seventy minus eighty.",
        show(f8mv['p2'], 'slide the whole middle part'))),
    SM('The arc length', 'The arc length',
      L("Now the length. An arc is a part of the circumference. The radius is eight, so the whole circumference is two pi "
        "times eight, sixteen pi.", show(f8k98, 'Now the length'), show(f8a1, 'the whole circumference')),
      L("Which part of it do we need? Ninety degrees out of three hundred sixty is one quarter. And one quarter of sixteen "
        "pi is four pi. Choice number three is our answer.", show(f8a2, 'Ninety degrees out of'),
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("When you can't find each part alone, look for the sum. Here it was the whole angle minus the middle part. [pause] "
        "Okay. I'll see you in the next question.", pt('f8a2', "When you can't find each part"))),
])

# ------------------------------------------------------------------------------------------------ geo33-g099 (Hebrew 4765-4855)
# Hebrew: shaded areas, but nothing to subtract; "a circle plus the bold part? how?"; go to the givens: a quarter of the
# circumference = central angle 90 -> construction OA, OB (and PA, PB), radii; four equal sides = at least a rhombus,
# right angles -> a square; "Pac-Man + square + Pac-Man"; 3/4 of the circle; estimation rules out two choices only
# (more than a circle and a half), 50-50, a gamble. Course numbers: r 6 -> 27 pi + 36 + 27 pi = 54 pi + 36.
# Added (task): the union as two whole circles minus the overlap counted twice (lens = 2 (9 pi - 18)).
# V3: the copy with the union grey; the minor arc AB of circle O traced teal, dashed radii with the right angle and 6;
# the same for P; the square OAPB traced and its right angles; the two Pac-Men orange, the square teal, values written.
# Method 2: the two circles outlined teal / orange, the lens red, the quarter circle AOB teal with the triangle orange.
# Estimation: the left circle teal, the right half of circle P orange.
f8O, f8Pc, f8A9, f8B9 = (242.572, 180.0), (397.428, 180.0), (320.0, 102.572), (320.0, 257.428)
f8union = 'M 320 102.572 A 109.5 109.5 0 1 0 320 257.428 A 109.5 109.5 0 1 0 320 102.572 Z'
f8lens = 'M 320 102.572 A 109.5 109.5 0 0 1 320 257.428 A 109.5 109.5 0 0 1 320 102.572 Z'
f8_99base = [('region', f8union, 'ink', 0.25), ('circ', *f8O, f8R), ('circ', *f8Pc, f8R), ('dot', *f8O), ('dot', *f8Pc)] + \
            f8_lab([(228, 198, 'O'), (412, 198, 'P'), (320, 82, 'A'), (320, 279, 'B')])
f8g99 = PIN(GEO('f8g99', [
    ('line', f8_99base),
    ('arcO', [('arcw', *f8O, f8R, -45, 45, 'teal', 7)]),
    ('radO', [('dot', *f8A9), ('dot', *f8B9), ('seg', *f8O, *f8A9, 'teal', 3, True), ('seg', *f8O, *f8B9, 'teal', 3, True),
              ('right', *f8O, -45, 45, 16), ('txt', 266, 130, '6', 'teal', 24), ('txt', 266, 232, '6', 'teal', 24)]),
    ('radP', [('arcw', *f8Pc, f8R, 135, 225, 'teal', 7), ('seg', *f8Pc, *f8A9, 'teal', 3, True), ('seg', *f8Pc, *f8B9, 'teal', 3, True),
              ('right', *f8Pc, 135, 225, 16), ('txt', 374, 130, '6', 'teal', 24), ('txt', 374, 232, '6', 'teal', 24)]),
    ('sq', [('path', [f8O, f8A9, f8Pc, f8B9, f8O], 'teal', 6), ('right', *f8A9, 225, 315, 14), ('right', *f8B9, 45, 135, 14)]),
    ('pac', [('wedge', *f8O, f8R, 45, 315, 'orange'), ('wedge', *f8Pc, f8R, 225, 135, 'orange'),
             ('tint', [f8O, f8A9, f8Pc, f8B9], 'teal'), ('txt', 180, 180, '27π', 'orange', 30), ('txt', 460, 180, '27π', 'orange', 30),
             ('txt', 320, 180, '36', 'teal', 28)]),
    ('b1', [('txt', 320, 325, '¾ · π · 6² = ¾ · 36π = 27π', 'orange', 24)]),
    ('b2', [('txt', 320, 362, '27π + 36 + 27π = 54π + 36', 'ink', 24)]),
], vb='120 60 400 320', w=420, title='Two congruent circles O and P'))
f8g99b = PIN(GEO('f8g99b', [
    ('line', f8_99base),
    ('two', [('circ', *f8O, f8R, 'teal', 5), ('circ', *f8Pc, f8R, 'orange', 5), ('txt', 190, 180, '36π', 'teal', 28),
             ('txt', 452, 180, '36π', 'orange', 28)]),
    ('lens', [('region', f8lens, 'red', 0.45)]),
    ('quarter', [('seg', *f8O, *f8A9, 'teal', 3, True), ('seg', *f8O, *f8B9, 'teal', 3, True), ('wedge', *f8O, f8R, -45, 45, 'teal'),
                 ('right', *f8O, -45, 45, 16)]),
    ('tri', [('seg', *f8A9, *f8B9, 'orange', 3, True), ('tint', [f8O, f8A9, f8B9], 'orange')]),
    ('b4', [('txt', 320, 325, 'overlap = 2(9π − 18) = 18π − 36', 'red', 24)]),
    ('b5', [('txt', 320, 362, '72π − (18π − 36) = 54π + 36', 'ink', 24)]),
], vb='120 60 400 320', w=420, title='Two whole circles and their overlap'))
f8g99c = PIN(GEO('f8g99c', [
    ('line', f8_99base),
    ('one', [('circ', *f8O, f8R, 'teal', 5, False, 'teal'), ('txt', 205, 180, '36π', 'teal', 30)]),
    ('half', [('wedge', *f8Pc, f8R, -90, 90, 'orange'), ('seg', f8Pc[0], 70.5, f8Pc[0], 289.5, 'orange', 3, True),
              ('txt', 450, 180, '18π', 'orange', 30)]),
    ('b6', [('txt', 320, 330, 'union > 36π + 18π = 54π', 'ink', 26)]),
], vb='120 60 400 320', w=420, title='More than a circle and a half'))
video('solve-geo33-g099', 'solution', qid='geo33-g099', slides=[
    SM('Method 1 · The math way', 'Pieces we know',
      L("Two congruent circles, with centers O and P, have a radius of six centimeters, and they intersect at A and B. The "
        "minor arc A B is one quarter of the circumference of each circle. What is the area of the union of the two "
        "circles?", pt('stem', 'Two congruent circles', 'hl', 9.0), voice='calm', pause=0.5),
      L("The union is everything that is inside at least one of the circles, the whole grey shape. It's a shaded-area "
        "question, but until now we usually subtracted, and here there's nothing to subtract from. Some students think, "
        "it's a circle plus an extra bit. But how do we find that bit? It's not clear. [short pause] We'll solve it two "
        "ways, by cutting it into pieces we know, and by taking away the overlap. Then we'll see what estimating can do.",
        show(f8g99['line'], 'The union is everything')),
      L("In a case like this, we go to the givens and see what we can get out of them. The minor arc A B is a quarter of "
        "the circumference of circle O. A quarter of the circle means a central angle of a quarter of three hundred sixty, "
        "ninety degrees.", show(f8g99['arcO'], 'The minor arc A B is a quarter')),
      L("But no central angle is drawn, so we draw one. A radius from O to A, and a radius from O to B. The angle between "
        "them is ninety degrees, and each radius is six.", show(f8g99['radO'], 'A radius from O to A')),
      L("The same in circle P. The circles are congruent, so P A and P B are also six, and the angle at P is also ninety.",
        show(f8g99['radP'], 'The same in circle P')),
      L("Now look at O A P B. All four sides are six, so it's at least a rhombus. And its angle at O is ninety degrees. A "
        "rhombus with a right angle is a square, so O A P B is a square.", show(f8g99['sq'], 'Now look at O A P B')),
      L("Now I see how to find the grey area. It's the left Pac-Man, plus the square, plus the right Pac-Man. Each Pac-Man "
        "is a circle without its quarter, so it's three quarters of the circle.", show(f8g99['pac'], 'the left Pac-Man')),
      L("One whole circle is pi r squared, pi times six squared, thirty-six pi. A quarter of thirty-six is nine, so three "
        "quarters of thirty-six pi is twenty-seven pi.", show(f8g99['b1'], 'One whole circle')),
      L("The square is six squared, thirty-six. So the union is twenty-seven pi, plus thirty-six, plus twenty-seven pi, "
        "which is fifty-four pi plus thirty-six. Choice number three is our answer.", show(f8g99['b2'], 'So the union is'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · The math way: subtract the overlap', 'Take away the overlap',
      L("[pause] Now a second way. Take the two whole circles. Each one is thirty-six pi, so together they're seventy-two "
        "pi.", show(f8g99b['line'], 'Now a second way'), show(f8g99b['two'], 'Take the two whole circles')),
      L("But the middle part, where the circles overlap, is inside both circles. So we counted it twice, and we must take "
        "it away once.", show(f8g99b['lens'], 'where the circles overlap')),
      L("How big is the overlap? The chord A B cuts it into two equal pieces. Look at the right piece, in circle O. It's "
        "the quarter circle A O B, minus the triangle A O B.", show(f8g99b['quarter'], 'Look at the right piece'),
        show(f8g99b['tri'], 'minus the triangle A O B')),
      L("The quarter circle is a quarter of thirty-six pi, nine pi. The triangle has two legs of six and a right angle, so "
        "its area is six times six over two, eighteen. So one piece is nine pi minus eighteen, and the whole overlap is "
        "two times that, eighteen pi minus thirty-six.", show(f8g99b['b4'], 'the whole overlap')),
      L("Now take it away. Seventy-two pi minus, the bracket, eighteen pi minus thirty-six. The minus before the bracket "
        "turns minus thirty-six into plus thirty-six. So we get fifty-four pi plus thirty-six, choice number three again.",
        show(f8g99b['b5'], 'Seventy-two pi minus'), mk('tick', 'choice 3', 'choice number three again'))),
    SM('Method 3 · Estimation', 'Estimating',
      L("[pause] Students often ask, can we just estimate the size here? It's hard to finish that way, but it's easy to "
        "rule out two choices. The left circle alone is thirty-six pi.", show(f8g99c['line'], 'Students often ask'),
        show(f8g99c['one'], 'The left circle alone')),
      L("And the grey shape has more than that. It also has the right half of circle P, eighteen pi, and a bit more in the "
        "middle. So the union is more than thirty-six pi plus eighteen pi, fifty-four pi.",
        show(f8g99c['half'], 'the right half of circle P'), show(f8g99c['b6'], 'So the union is more than')),
      L("Twenty-seven pi plus eighteen, and twenty-seven pi plus thirty-six, are much too small, so choice numbers one and "
        "four are out. But choice numbers two and three both have fifty-four pi, plus eighteen or plus thirty-six. That's "
        "too close to decide by estimating.", mk('cross', 'choice 1', 'are much too small'),
        mk('cross', 'choice 4', 'four are out')),
      L("So estimating raised our chances to fifty-fifty, but it can't settle it. If you're out of time, it's a reasonable "
        "guess between the two. With time, use one of the full solutions. [pause] Okay. I'll see you in the next question.",
        pt('stem', 'estimating raised our chances'))),
])

# ------------------------------------------------------------------------------------------------ geo33-g100 (Hebrew 4858-4891)
# Hebrew: two approaches, math and psychometric. Math: tangent at E and F -> EF is a diameter = the height AB; rectangle
# area = AB x BC; equation with pi r^2; isolate BC. Psychometric (order of magnitude): BC is less than the diameter; pi
# is 3-plus; rule out three choices and mark the fourth "without even calculating". Course numbers: r 4 -> 8 BC = 16 pi,
# BC = 2 pi; the bound made explicit with the 8 x 8 square around the circle (task: a geometric bound).
# V3: the copy; dashed radii OE, OF with the right angles and 4, 4 (a diameter); AB traced teal with 8. Method 2: the
# dashed square around the circle with its side 8, the circle tinted inside it.
f8_100base = ([('circ', 320, 180, f8R), ('seg', 234, 70.5, 234, 289.5), ('seg', 234, 289.5, 406, 289.5),
               ('seg', 406, 289.5, 406, 70.5), ('seg', 406, 70.5, 234, 70.5), ('dot', 320, 180)]
              + f8_lab([(217, 54, 'A'), (217, 307, 'B'), (423, 307, 'C'), (423, 54, 'D'), (320, 51, 'E'), (320, 310, 'F'),
                        (334, 197, 'O')]))
f8g100 = PIN(GEO('f8g100', [
    ('line', f8_100base),
    ('r', [('dot', 320, 70.5), ('dot', 320, 289.5), ('seg', 320, 180, 320, 70.5, 'teal', 3, True),
           ('seg', 320, 180, 320, 289.5, 'teal', 3, True), ('right', 320, 70.5, 270, 360, 14), ('right', 320, 289.5, 0, 90, 14),
           ('txt', 304, 125, '4', 'teal', 24), ('txt', 304, 240, '4', 'teal', 24)]),
    ('ab', [('seg', 234, 70.5, 234, 289.5, 'teal', 6), ('txt', 252, 150, '8', 'teal', 28)]),
    ('c0', [('txt', 600, 110, 'π · 4² = 16π', 'teal', 28)]),
    ('c1', [('txt', 600, 160, '8 · BC = 16π', 'ink', 28)]),
    ('c2', [('txt', 600, 210, 'BC = 16π ÷ 8 = 2π', 'ink', 28)]),
], vb='190 30 560 300', w=560, title='Rectangle ABCD and the circle O'))
f8g100b = PIN(GEO('f8g100b', [
    ('line', f8_100base),
    ('sq', [('seg', 210.5, 70.5, 429.5, 70.5, 'teal', 3, True), ('seg', 429.5, 70.5, 429.5, 289.5, 'teal', 3, True),
            ('seg', 429.5, 289.5, 210.5, 289.5, 'teal', 3, True), ('seg', 210.5, 289.5, 210.5, 70.5, 'teal', 3, True),
            ('circ', 320, 180, f8R, 'teal', 3, False, 'teal'), ('txt', 444, 180, '8', 'teal', 26), ('txt', 270, 312, '8', 'teal', 26)]),
    ('c3', [('txt', 600, 90, '8 · BC < 64', 'ink', 28)]),
    ('c3b', [('txt', 600, 132, 'BC < 8', 'teal', 28)]),
    ('c4', [('txt', 600, 180, '3π > 9', 'red', 28)]),
    ('c4b', [('txt', 600, 222, '4π > 12', 'red', 28)]),
    ('c4c', [('txt', 600, 264, '8π > 24', 'red', 28)]),
], vb='190 30 560 300', w=560, title='The square around the circle'))
video('solve-geo33-g100', 'solution', qid='geo33-g100', slides=[
    SM('Method 1 · The math way', 'An equation',
      L("A circle with center O has a radius of four centimeters. The opposite sides A D and B C of rectangle A B C D are "
        "tangent to the circle at E and F. The area of the rectangle equals the area of the circle. What is the length of "
        "B C?", pt('stem', 'A circle with center O', 'hl', 9.0), voice='calm', pause=0.5),
      L("We'll solve it two ways, with a short equation, and then with an estimate, a size check on the choices. [short pause] The "
        "equation first. A D touches the circle at E, and B C touches it at F. Remember, the radius to the point where a "
        "tangent touches the circle is perpendicular to the tangent.", show(f8g100['line'], 'The equation first'),
        show(f8g100['r'], 'Remember, the radius')),
      L("So O E and O F are both perpendicular to the two parallel sides, and together they make one straight line from E "
        "to F. That's a diameter, two times four, eight. And it's as long as the side A B, so the height of the rectangle "
        "is eight.", show(f8g100['ab'], "That's a diameter")),
      L("The area of the rectangle is A B times B C, so it's eight times B C. The area of the circle is pi r squared, pi "
        "times four squared, sixteen pi. The two areas are equal, so eight times B C is sixteen pi.",
        show(f8g100['c0'], 'The area of the circle is'), show(f8g100['c1'], 'so eight times B C is sixteen pi')),
      L("To get B C alone, we divide both sides by eight. Sixteen pi over eight is two pi. Choice number two is our answer. "
        "The math solution wasn't bad at all.", show(f8g100['c2'], 'we divide both sides by eight'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · Estimation', 'A size check',
      L("[pause] Now the same question with an estimate, a size check, and almost no calculation. Draw the square around the circle. "
        "Its side is the diameter, eight, so its area is eight times eight, sixty-four.",
        show(f8g100b['line'], 'Now the same question'), show(f8g100b['sq'], 'Draw the square around')),
      L("The circle is inside this square, so the circle's area is less than sixty-four. The rectangle has the same area as "
        "the circle, so eight times B C is also less than sixty-four. That means B C is less than eight.",
        show(f8g100b['c3'], 'eight times B C is also less'), show(f8g100b['c3b'], 'That means B C is less')),
      L("Now the choices. Pi is a bit more than three. So three pi is more than nine, four pi is more than twelve, and "
        "eight pi is more than twenty-four. All of them are more than eight, so choice numbers one, three and four are out.",
        show(f8g100b['c4'], 'So three pi is more than nine'), show(f8g100b['c4b'], 'four pi is more than twelve'),
        show(f8g100b['c4c'], 'eight pi is more than twenty-four'), mk('cross', 'choice 1', 'choice numbers one, three'),
        mk('cross', 'choice 3', 'three and four'), mk('cross', 'choice 4', 'are out')),
      L("Three choices are out, so we can mark choice number two for sure, without even working it out. [pause] Okay. I'll "
        "see you in the next question.", mk('tick', 'choice 2', 'we can mark choice number two'))),
])

# ------------------------------------------------------------------------------------------------ geo33-g101 (Hebrew 4894-4993)
# Hebrew: two ways, math and plugging in the answers. Math: shaded = big circle minus small circle; call the radii R and
# r; one unknown: write R with r ("easier to add than to subtract"); AB = 2r + 4 (course: + 10); R = half of it, take out
# 2 as a common factor and cancel (topic 4: ka + kb = k(a + b)); divide by pi; the first short formula (topic 4,
# r26-t04-formulas: (a + b)^2 = a^2 + 2ab + b^2); r^2 cancels; r = 3 (course: 65 pi -> r = 4). Plugging in the answers:
# start in the middle, two tries are always enough; try one, too small -> it and the smaller ones are out; try the next.
# Course: the choices are 5, 2, 3, 4 (not in order), so they are put in order first; try 3 (55 pi), then 4 (65 pi).
# V3: the copy with the ring grey; the ring traced orange as "big minus small"; AC teal with 2r; AB orange with 2r + 10;
# R = r + 5 written on the figure.
f8_101base = [('region', 'M 441.667 180 A 121.667 121.667 0 1 0 198.333 180 A 121.667 121.667 0 1 0 441.667 180 Z '
               'M 295.667 180 A 48.667 48.667 0 1 0 198.333 180 A 48.667 48.667 0 1 0 295.667 180 Z', 'ink', 0.25),
              ('circ', 320, 180, 121.667), ('circ', 247, 180, 48.667), ('seg', 198.333, 180, 441.667, 180),
              ('txt', 368.7, 163, '10', 'ink', 22)] + f8_lab([(180, 180, 'A'), (460, 180, 'B'), (309, 198, 'C')])
f8g101 = PIN(GEO('f8g101', [
    ('line', f8_101base),
    ('ring', [('region', 'M 441.667 180 A 121.667 121.667 0 1 0 198.333 180 A 121.667 121.667 0 1 0 441.667 180 Z '
               'M 295.667 180 A 48.667 48.667 0 1 0 198.333 180 A 48.667 48.667 0 1 0 295.667 180 Z', 'orange', 0.3)]),
    ('d0', [('txt', 600, 100, 'πR² − πr² = 65π', 'ink', 28)]),
    ('ac', [('seg', 198.333, 180, 295.667, 180, 'teal', 6), ('dot', 247, 180), ('txt', 247, 160, '2r', 'teal', 26, True)]),
    ('ab', [('seg', 198.333, 196, 441.667, 196, 'orange', 3), ('seg', 198.333, 188, 198.333, 204, 'orange', 3),
            ('seg', 441.667, 188, 441.667, 204, 'orange', 3), ('txt', 380, 214, '2r + 10', 'orange', 24, True)]),
    ('d1', [('txt', 600, 160, 'R = (2r + 10) ÷ 2', 'orange', 28)]),
    ('rr', [('txt', 600, 200, '= 2(r + 5) ÷ 2', 'orange', 28), ('txt', 600, 240, '= r + 5', 'orange', 28),
            ('txt', 320, 40, 'R = r + 5', 'orange', 28, True)]),
], vb='165 20 580 300', w=560, title='Two circles tangent at A'))
f8d2 = I('f8d2', '$\\pi(r+5)^2-\\pi r^2=65\\pi$', size=32, hand='π(r + 5)^2 − πr^2 = 65π')
f8d3 = IH('f8d3', '$(r+5)^2-r^2=65$', size=32)
f8d4 = I('f8d4', '$r^2+10r+25-r^2=65$', size=32)
f8d5 = I('f8d5', '$10r+25=65\\ \\Rightarrow\\ 10r=40\\ \\Rightarrow\\ r=4$', size=32, hand='10r + 25 = 65   →   10r = 40   →   r = 4')
f8d6 = I('f8d6', 'In order: $\\ 2,\\ 3,\\ 4,\\ 5$', size=32)
f8d7 = IH('f8d7', '$r=3$: $\\ AB=6+10=16,\\ \\ R=8$', size=30)
f8d8 = I('f8d8', '$64\\pi-9\\pi=55\\pi$ ✗ $\\ $too small', size=30)
f8d9 = IH('f8d9', '$r=4$: $\\ AB=8+10=18,\\ \\ R=9$', size=30)
f8d10 = I('f8d10', '$81\\pi-16\\pi=65\\pi$ ✓', size=30)
f8k101 = I('f8k101', 'So far: $\\ \\pi R^2-\\pi r^2=65\\pi,\\quad R=r+5$', size=26, col=1)
video('solve-geo33-g101', 'solution', qid='geo33-g101', slides=[
    SM('Method 1 · The math way', 'R with r',
      L("A smaller circle lies inside a larger circle and touches it from the inside at A. A B is a diameter of the larger "
        "circle, A C is a diameter of the smaller circle, and C B is ten centimeters. The area inside the larger circle "
        "but outside the smaller one is sixty-five pi. What is the radius of the smaller circle?",
        pt('stem', 'A smaller circle lies inside', 'hl', 10.0), voice='calm', pause=0.5),
      L("We'll solve it two ways, with an equation, and by plugging in the answers. [short pause] First the math way, with an equation. How "
        "do we find the shaded area? It's the area of the big circle minus the area of the small circle. We don't know "
        "either radius, so let's call the big one capital R, and the small one small r.",
        show(f8g101['line'], 'First the math way'), show(f8g101['ring'], 'the area of the big circle minus')),
      L("So pi R squared minus pi r squared is sixty-five pi. Two unknowns are too many, so we write the big radius with "
        "the small one. That's easier than the other way round, because adding is easier than subtracting.",
        show(f8g101['d0'], 'So pi R squared')),
      L("The small diameter, A C, is two r. The big diameter, A B, is A C plus C B, so it's two r plus ten.",
        show(f8g101['ac'], 'The small diameter'), show(f8g101['ab'], 'The big diameter')),
      L("The big radius is half of that, two r plus ten, over two. Both terms are multiples of two, so we take out two as a "
        "common factor and cancel it. So capital R is r plus five.", show(f8g101['d1'], 'The big radius is half'),
        show(f8g101['rr'], 'we take out two'))),
    SM('Method 1 · The math way', 'Solve the equation',
      L("Now we put r plus five in place of capital R. Pi times, the bracket r plus five, squared, minus pi r squared, is "
        "sixty-five pi.", show(f8k101, 'Now we put'), show(f8d2, 'Now we put r plus five')),
      L("Pi is in every term, so we divide the whole equation by pi. That leaves the bracket r plus five, squared, minus r "
        "squared, equals sixty-five.", show(f8d3, 'we divide the whole equation by pi')),
      L("Now we open the bracket with the first formula from expressions. A plus b, squared, is a squared plus two a b plus "
        "b squared. So r plus five, squared, is r squared, plus two times five times r, which is ten r, plus twenty-five.",
        show(f8d4, 'So r plus five, squared')),
      L("Then r squared minus r squared is zero, so they cancel. We're left with ten r plus twenty-five equals sixty-five. "
        "Take twenty-five off both sides, so ten r is forty, and r is four. Choice number four is our answer.",
        show(f8d5, "We're left with"), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    SM('Method 2 · Plugging in the answers', 'Plugging in the answers',
      L("[pause] Now a second way, plugging in the answers. The answer is one of the four choices. So we can put each "
        "choice into the story as the small radius, and see which one gives a shaded area of sixty-five pi. All the "
        "choices are small whole numbers, so it's easy here."),
      L("Where do we start? In order, the choices are two, three, four and five, and we start in the middle. Why? If a "
        "middle value gives a shaded area that's too small, we need a bigger radius, so the smaller values are out too. If "
        "it's too big, the bigger values are out. So two tries are always enough.", show(f8d6, 'In order, the choices are')),
      L("Let's try three. The small diameter is six, so the big diameter is six plus ten, sixteen, and the big radius is "
        "eight. Big minus small is sixty-four pi minus nine pi, fifty-five pi.", show(f8d7, "Let's try three"),
        show(f8d8, 'Big minus small')),
      L("That's not sixty-five pi, it's too small. We need a bigger shaded area, so bigger circles, and a bigger radius. So "
        "three is out, and two is out too.", mk('cross', 'choice 3', 'So three is out'), mk('cross', 'choice 2', 'and two is out too')),
      L("Let's try four. The small diameter is eight, so the big diameter is eight plus ten, eighteen, and the big radius "
        "is nine. Eighty-one pi minus sixteen pi is sixty-five pi. It fits. Choice number four is our answer again. "
        "[pause] Okay. I'll see you in the next question.", show(f8d9, "Let's try four"), show(f8d10, 'Eighty-one pi minus'),
        mk('tick', 'choice 4', 'Choice number four is our answer again'))),
])

# ------------------------------------------------------------------------------------------------ geo33-g102 (Hebrew 4996-5091)
# Hebrew: two ways. Full math: an arc length needs a central angle; isosceles -> the base angles are equal, each 90 -
# alpha/2; angle B is inscribed on the bold arc -> central 180 - alpha; "we divided by 2 and multiplied by 2 - spot it
# early"; arc = part of the circumference; glance at the choices (pi r in all): cancel 2 with 360; split the fraction
# (same denominator, so we may go back); 1 - alpha/180. Plugging in numbers: any unknown can be replaced by a number,
# a special case; 60 degrees -> equilateral; central 120; r = 1; arc 2 pi / 3; test every choice, do not mark a fit
# before three are out. Course: angle A = 4 theta -> 180 - 4 theta, 1 - theta/45; theta = 15, valid (0 < theta < 45).
# V3: the copy; the base angles teal with 90 - 2 theta; angle B traced orange with its sides to D and E and the bold arc
# DE orange; dashed radii OD, OE and the central angle; method 2: a copy with 60 at A, B, C, the central 120 and r = 1.
f8A2, f8B2, f8C2 = (320.0, 70.637), (216.941, 291.647), (423.059, 291.647)
f8O2, f8r102 = (271.906, 240.118), 75.342
f8D2, f8E2 = (276.049, 164.890), (326.871, 291.647)
f8aD, f8aE = gdir(*f8O2, *f8D2), gdir(*f8O2, *f8E2)
f8_102base = [('seg', *f8A2, *f8B2), ('seg', *f8B2, *f8C2), ('seg', *f8C2, *f8A2), ('circ', *f8O2, f8r102), ('dot', *f8O2),
              ('tick', *f8A2, *f8B2, 1, 'ink'), ('tick', *f8A2, *f8C2, 1, 'ink'), ('arc', *f8A2, 24, 245.0, 295.0, 'ink'),
              ('txt', 320, 110, '4θ', 'ink', 20), ('arcw', *f8O2, f8r102, f8aE, f8aD, 'ink', 6)] + \
             f8_lab([(320, 50, 'A'), (199, 307, 'B'), (441, 307, 'C'), (255, 250, 'O'), (257, 155, 'D'), (327, 312, 'E')])
f8g102 = PIN(GEO('f8g102', [
    ('line', f8_102base),
    ('base', [('arc', *f8B2, 26, 0, 65.0, 'small'), ('arc', *f8C2, 26, 115.0, 180, 'small')]),
    ('e1', [('txt', 600, 90, 'angle B = angle C', 'teal', 26), ('txt', 600, 135, '(180° − 4θ) ÷ 2', 'teal', 28),
            ('txt', 600, 180, '= 90° − 2θ', 'teal', 28)]),
    ('zone', [('circ', *f8O2, f8r102, 'orange', 5), ('circ', *f8O2, f8r102 + 14, 'orange', 2, True)]),
], vb='180 30 560 295', w=560, title='Isosceles triangle ABC and the circle O'))
# the enlarged cut-out of the circle around B (V3): the same labels, 1.6 times bigger
f8zB = [('seg', *f8B2, *gpt(*f8B2, 200, 65.0)), ('seg', *f8B2, *gpt(*f8B2, 200, 0)), ('circ', *f8O2, f8r102), ('dot', *f8O2),
        ('arcw', *f8O2, f8r102, f8aE, f8aD, 'ink', 6), ('arc', *f8B2, 26, 0, 65.0, 'small')] + \
       f8_lab([(201, 304, 'B'), (258, 154, 'D'), (330, 310, 'E'), (256, 252, 'O')], 22)
f8g102z = PIN(GEO('f8g102z', [
    ('line', f8zB + [('txt', 470, 150, 'angle B', 'teal', 22), ('txt', 470, 180, '= 90° − 2θ', 'teal', 22)]),
    ('insc', [('path', [f8D2, f8B2, f8E2], 'orange', 6), ('arc', *f8B2, 34, 0, 65.0, 'large'),
              ('arcw', *f8O2, f8r102, f8aE, f8aD, 'orange', 8)]),
    ('cent', [('dot', *f8D2), ('dot', *f8E2), ('seg', *f8O2, *f8D2, 'teal', 3, True), ('seg', *f8O2, *f8E2, 'teal', 3, True),
              ('arc', *f8O2, 20, f8aE, f8aD, 'small')]),
    ('e2', [('txt', 470, 222, 'central angle:', 'orange', 22), ('txt', 470, 252, '2(90° − 2θ)', 'orange', 22),
            ('txt', 470, 282, '= 180° − 4θ', 'orange', 22)]),
], vb='185 135 365 195', w=560, title='The circle around B, enlarged'))
f8e3 = I('f8e3', '$\\frac{180-4\\theta}{360}\\cdot2\\pi r$', size=34)
f8e4 = I('f8e4', '$=\\frac{180-4\\theta}{180}\\cdot\\pi r$', size=34)
f8e5 = I('f8e5', '$=\\left(\\frac{180}{180}-\\frac{4\\theta}{180}\\right)\\pi r$', size=34)
f8e6 = I('f8e6', '$=\\pi r\\left(1-\\frac{\\theta}{45}\\right)$', size=34)
f8g102b = PIN(GEO('f8g102b', [
    ('line', f8_102base),
    ('eq', [('txt', 355, 110, '= 60°', 'teal', 20), ('arc', *f8B2, 26, 0, 65.0, 'small'), ('arc', *f8C2, 26, 115.0, 180, 'small'),
            ('txt', 400, 270, '60°', 'teal', 22), ('txt', 205, 268, '60°', 'teal', 20)]),
    ('c120', [('seg', *f8O2, *f8D2, 'teal', 3, True), ('seg', *f8O2, *f8E2, 'teal', 3, True),
              ('arc', *f8O2, 20, f8aE, f8aD, 'small'), ('txt', 262, 200, '1', 'teal', 22),
              ('arcw', *f8O2, f8r102, f8aE, f8aD, 'orange', 8)]),
    ('e7', [('txt', 600, 60, 'central: 120°', 'teal', 28), ('txt', 600, 100, 'C = 2π · 1 = 2π', 'ink', 28), ('txt', 600, 140, '120 ÷ 360 = ⅓', 'teal', 28),
            ('txt', 600, 180, '⅓ · 2π = 2π/3', 'orange', 28)]),
], vb='180 30 560 295', w=560, title='An example: theta = 15 and r = 1'))
f8p1 = I('f8p1', '(1) $\\ 1-\\frac{15}{15}=0$ ✗', size=30)
f8p2 = I('f8p2', '(2) $\\ 1-\\frac{15}{30}=\\frac12\\ \\Rightarrow\\ \\frac{\\pi}{2}$ ✗', size=30)
f8p3 = I('f8p3', '(3) $\\ 1-\\frac{15}{90}=\\frac56\\ \\Rightarrow\\ \\frac{5\\pi}{6}$ ✗', size=30)
f8p4 = I('f8p4', '(4) $\\ 1-\\frac{15}{45}=\\frac23\\ \\Rightarrow\\ \\frac{2\\pi}{3}$ ✓', size=30)
f8k102a = I('f8k102a', 'So far: $\\ $central angle $=180°-4\\theta$', size=26, col=1)
f8k102b = I('f8k102b', 'So far: $\\ \\theta=15,\\ r=1$, $\\ $arc $=\\frac{2\\pi}{3}$', size=26, col=1)
video('solve-geo33-g102', 'solution', qid='geo33-g102', slides=[
    SM('Method 1 · The math way', 'The base angles',
      L("A B C is an isosceles triangle, with A B equal to A C, and angle B A C is four theta degrees, where theta is "
        "between zero and forty-five. B lies on a circle with center O and radius r. A B and B C meet the circle again at D "
        "and E. What is the length of the arc D E that does not contain B?",
        pt('stem', 'A B C is an isosceles triangle', 'hl', 11.0), voice='calm', pause=0.5),
      L("There are letters everywhere, so we'll solve it two ways, the math way, and then by plugging in numbers. "
        "[short pause] The math way first. We need an arc length, and for that we first need a central angle.",
        show(f8g102['line'], 'The math way first')),
      L("Let's start with the isosceles triangle. A B equals A C, so angle B equals angle C. Together they're a hundred "
        "eighty minus four theta. They're equal, so each one is half of that. Half of a hundred eighty is ninety, and half "
        "of four theta is two theta. So each base angle is ninety minus two theta.",
        show(f8g102['base'], 'so angle B equals angle C'), show(f8g102['e1'], 'So each base angle')),
      L("The arc we need is on the circle, around B. So let's take this part of the figure and look at it bigger.",
        show(f8g102['zone'], 'The arc we need is on the circle'))),
    SM('Method 1 · The math way', 'The central angle',
      L("Here's the circle around B, bigger. Angle B is still ninety minus two theta. Its sides go through D and E, so it's "
        "an inscribed angle in the circle, and it stands on the bold arc D E. The central angle on the same arc is twice "
        "as big.", show(f8g102z['line'], "Here's the circle around B"), show(f8g102z['insc'], 'Its sides go through D and E')),
      L("So let's draw the radii O D and O E. The central angle is two times, ninety minus two theta, which is a hundred "
        "eighty minus four theta.", show(f8g102z['cent'], 'draw the radii O D and O E'), show(f8g102z['e2'], 'The central angle is two times')),
      L("Did you notice? We divided by two, and then we multiplied by two. If you see that early, you can write a hundred "
        "eighty minus four theta right away.")),
    SM('Method 1 · The math way', 'The arc length',
      L("An arc is the part of the circumference set by the central angle, out of three hundred sixty. So the arc is a "
        "hundred eighty minus four theta, over three hundred sixty, times two pi r.", show(f8k102a, 'An arc is the part'), show(f8e3, 'So the arc is')),
      L("There are many letters, so let's glance at the choices and work toward them. Every choice has pi r, and we have "
        "two pi r. So we cancel the two with the three hundred sixty, and we're left with a hundred eighty at the bottom, "
        "times pi r.", show(f8e4, 'So we cancel the two')),
      L("Every choice also has a one in the bracket. So we split our fraction into two fractions with the same bottom, a "
        "hundred eighty over a hundred eighty, minus four theta over a hundred eighty. Why is that allowed? Two fractions "
        "with the same bottom are subtracted by subtracting the tops, so we can also go back the other way.",
        show(f8e5, 'So we split our fraction')),
      L("A hundred eighty over a hundred eighty is one. And four over a hundred eighty is one over forty-five, because a "
        "hundred eighty divided by four is forty-five. So the arc is pi r, times the bracket one minus theta over "
        "forty-five. Choice number four is our answer.", show(f8e6, 'So the arc is pi r'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
    SM('Method 2 · Plugging in numbers', 'An easy example',
      L("[pause] The algebra got a bit tangled at the end. Now a shorter way, plugging in numbers. The right choice must be "
        "true for every theta and every r that the question allows. So it must also be true for one example that we "
        "choose. We pick easy numbers, find the arc, and then put the same numbers in the choices.",
        show(f8g102b['line'], 'Now a shorter way')),
      L("Which example is the easiest? An equilateral triangle, with all its angles sixty degrees. Then four theta is sixty, "
        "so theta is fifteen. That's between zero and forty-five, so it's allowed.", show(f8g102b['eq'], 'An equilateral triangle')),
      L("So angle B is sixty, and the central angle on the bold arc is twice as big, a hundred twenty. The radius isn't "
        "given either, so let's take r as one, an easy number.", show(f8g102b['c120'], 'the central angle on the bold arc')),
      L("The whole circumference is two pi times one, two pi. A hundred twenty out of three hundred sixty is one third. So "
        "the arc is a third of two pi, two pi over three.", show(f8g102b['e7'], 'The whole circumference'))),
    SM('Method 2 · Plugging in numbers', 'Check the choices',
      L("Now we put theta fifteen and r one in every choice, and cross out any choice that doesn't give two pi over three. "
        "Even if one fits early, we check them all, because an example can fit more than one choice.",
        show(f8k102b, 'Now we put theta')),
      L("Choice number one: fifteen over fifteen is one, and one minus one is zero. Zero, so it's out.",
        show(f8p1, 'Choice number one'), mk('cross', 'choice 1', "so it's out")),
      L("Choice number two: fifteen over thirty is a half, and one minus a half is a half. That gives pi over two, out.",
        show(f8p2, 'Choice number two'), mk('cross', 'choice 2', 'That gives pi over two')),
      L("Choice number three: fifteen over ninety is a sixth, and one minus a sixth is five sixths. Five pi over six, out.",
        show(f8p3, 'Choice number three'), mk('cross', 'choice 3', 'Five pi over six')),
      L("Choice number four: fifteen over forty-five is a third, and one minus a third is two thirds. Two pi over three, it "
        "fits, and the other three are out. Choice number four is our answer. [pause] Okay. I'll see you in the next "
        "question.", show(f8p4, 'Choice number four:'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
])


# ------------------------------------------------------------------------------------------------ placement (right column)
# The question figure sits on the left; everything of ours goes in the right column (x 1040), between the stem and the
# choices (board y about 330-750). Typed lines beside a tall copy start at x 1370-1390.
for _it, _y, _x in [(f8g98, 330, 1040), (f8mv, 340, 1040), (f8k98, 340, 1040), (f8a1, 400, 1040), (f8a2, 460, 1040),
                    (f8g99, 320, 1040), (f8g99b, 320, 1040), (f8g99c, 320, 1040), (f8g100, 330, 1040), (f8g100b, 330, 1040),
                    (f8g101, 330, 1040),
                    (f8k101, 340, 1040), (f8d2, 400, 1040), (f8d3, 460, 1040), (f8d4, 520, 1040), (f8d5, 580, 1040),
                    (f8d6, 340, 1040), (f8d7, 400, 1040), (f8d8, 460, 1040), (f8d9, 520, 1040), (f8d10, 580, 1040),
                    (f8g102, 330, 1040), (f8g102z, 330, 1040),
                    (f8k102a, 335, 1040), (f8e3, 390, 1040), (f8e4, 455, 1040), (f8e5, 520, 1040), (f8e6, 585, 1040),
                    (f8g102b, 330, 1040),
                    (f8k102b, 335, 1040), (f8p1, 395, 1040), (f8p2, 450, 1040), (f8p3, 505, 1040), (f8p4, 560, 1040)]:
    _R(_it, _y, _x)

# =================================================================================================================
# Topic-33 fragment f9 (TAG I, 2026-10-14): r26-t33-more-tools (lesson "More Circle Tools"), solve-q-r26-t33-04 (a
# segment: sector minus triangle), solve-q-r26-t33-05 (the common tangent of two touching circles). Course additions,
# no direct Hebrew lesson; written with her moves from the Hebrew advanced circles part (geo 4260-5095):
#   - shaded areas: "subtracting areas is the most common way; first a scheme, what minus what" (4276-4283);
#   - "no central angle is drawn, so a helper line: radii to the points" + "four equal sides: at least a rhombus" (the two
#     identical circles, 4733-4760, the course's g099);
#   - the automatic helper line: a radius to the point of tangency, perpendicular (4291-4294, and 3621-3634 "like Pavlov");
#   - the height to the base of an isosceles triangle is also a median (4299-4300);
#   - partial calculation: once one part is known, look at the choices and rule out every choice without it in the right
#     place (4321-4333, 4422-4429);
#   - "they hide negative answers behind letters; an area can't be negative" (4378-4380);
#   - the ring = big circle minus small circle, pi divides out (4916-4930);
#   - "in the exam we mark and move on; in the lesson we check the others" (4334-4336).
# Study plan: day 5; triangles (equilateral area a²√3/4, gold and silver triangles, Pythagoras, triples), quadrilaterals
# (a diagonal halves a rhombus) and the earlier circle videos are short reminders.
# =================================================================================================================
import math as _f9m

FIG_LEFT.update({'solve-q-r26-t33-04', 'solve-q-r26-t33-05'})


def f9_poly(pts, col='ink', w=3, dashed=False):
    n = len(pts)
    return [('seg', pts[k][0], pts[k][1], pts[(k + 1) % n][0], pts[(k + 1) % n][1], col, w, dashed) for k in range(n)]


def f9_ring_d(cx, cy, R, r):
    """an svg path for a ring (two circles, even-odd)"""
    c = lambda q: 'M %.1f %.1f a %.1f %.1f 0 1 0 %.1f 0 a %.1f %.1f 0 1 0 %.1f 0 Z' % (cx - q, cy, q, q, 2 * q, q, q, -2 * q)
    return c(R) + ' ' + (c(r) if r > 0 else '')


# ================================================================================================ the lesson
# V3: generic clean figures built at her words. Two equal circles: the crossing points, the five radii dashed teal (a
# construction) with one tick each (all equal), the two equilateral triangles tinted teal with a small arc at every
# corner, the 120° angle orange. The shared region: the lens tinted, the chord dashed, the right piece outlined and tinted,
# then (the rest dimmed) the 120° sector teal and the triangle orange on top: what stays teal is the piece. Numbers: the
# rhombus tinted INSIDE the circles first, then pulled out as two enlarged copies with the same labels: cut by OP (two
# equilateral triangles, teal) and cut by AB (triangle AOB, orange). The ring: built step by step, the radius to the
# point of tangency dashed with its right angle, the halves h with ticks, the right triangle tinted orange. Same chord,
# same ring: three rings drawn to scale with the same chord 10, one after another.
F9O, F9P, F9r = (250.0, 190.0), (360.0, 190.0), 110.0
F9A = (305.0, 190.0 - F9r * _f9m.sin(_f9m.radians(60)))
F9B = (305.0, 190.0 + F9r * _f9m.sin(_f9m.radians(60)))
_f9circ = [('circ', F9O[0], F9O[1], F9r), ('circ', F9P[0], F9P[1], F9r)]
_f9OPl = [('dot', *F9O, 'O', -22, 16), ('dot', *F9P, 'P', 22, 16)]
_f9ABl = [('dot', *F9A, 'A', 0, -24), ('dot', *F9B, 'B', 0, 24)]
f9eq = PIN(GEO('f9eq', [
    ('line', _f9circ + _f9OPl),
    ('ab', _f9ABl),
    ('radii', [('seg', *F9O, *F9A, 'teal', 3, True), ('seg', *F9O, *F9B, 'teal', 3, True), ('seg', *F9P, *F9A, 'teal', 3, True),
               ('seg', *F9P, *F9B, 'teal', 3, True)]),
    ('op', [('seg', *F9O, *F9P, 'teal', 3, True)] + [('tick', *p, *q, 1) for p, q in
             ((F9O, F9A), (F9O, F9B), (F9P, F9A), (F9P, F9B), (F9O, F9P))]),
    ('tri', [('tint', [F9O, F9A, F9P], 'teal'), ('tint', [F9O, F9B, F9P], 'teal'),
             ('arc', *F9O, 24, 0, 60, 'teal'), ('arc', *F9O, 24, 300, 360, 'teal'), ('arc', *F9P, 24, 120, 180, 'teal'),
             ('arc', *F9P, 24, 180, 240, 'teal'), ('arc', *F9A, 24, 240, 300, 'teal'), ('arc', *F9B, 24, 60, 120, 'teal'),
             ('txt', 305, 162, '60°', 'teal', 20), ('txt', 305, 218, '60°', 'teal', 20)]),
    ('a120', [('arc', *F9O, 44, 300, 60, 'orange'), ('txt', 214, 160, '120°', 'orange', 26)]),
], vb='120 50 380 290', w=640, col=0, title='Two equal circles, each through the center of the other'))

_f9lens = ('M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f Z'
           % (F9A[0], F9A[1], F9r, F9r, F9B[0], F9B[1], F9r, F9r, F9A[0], F9A[1]))
f9lens = PIN(GEO('f9lens', [
    ('line', _f9circ + _f9OPl + _f9ABl + [('arc', *F9O, 44, 300, 60, 'orange'), ('txt', 214, 160, '120°', 'orange', 26)]),
    ('lens', [('region', _f9lens, 'teal', 0.22)]),
    ('chord', [('seg', *F9A, *F9B, 'teal', 3, True)]),
    ('piece', [('cseg', *F9O, F9r, 300, 60, 'teal'), ('arcw', *F9O, F9r, 300, 60, 'teal', 6)]),
    ('sector', [('dim', 120, 50, 380, 290), ('circ', F9O[0], F9O[1], F9r, 'ink', 2), ('wedge', *F9O, F9r, 300, 60, 'teal'),
                ('seg', *F9O, *F9A, 'teal', 3), ('seg', *F9O, *F9B, 'teal', 3), ('arcw', *F9O, F9r, 300, 60, 'teal', 5)]
               + _f9OPl[:1] + _f9ABl + [('txt', 404, 110, 'sector', 'teal', 24)]),
    ('tri', [('tint', [F9O, F9A, F9B], 'orange'), ('seg', *F9A, *F9B, 'orange', 3), ('txt', 404, 290, '− triangle', 'orange', 24)]),
], vb='120 50 380 290', w=640, col=0, title='The region the two circles share'))

f9r6 = PIN(GEO('f9r6', [
    ('line', _f9circ + _f9OPl + _f9ABl + [('seg', *F9O, *F9A, 'ink', 2.5), ('txt', 252, 142, '6', 'ink', 24)]),
    ('sec', [('wedge', *F9O, F9r, 300, 60, 'teal'), ('seg', *F9O, *F9B, 'teal', 2.5), ('txt', 300, 160, '12π', 'teal', 24)]),
    ('rh', f9_poly([F9O, F9A, F9P, F9B], 'teal', 4) + [('tint', [F9O, F9A, F9P, F9B], 'teal')]),
], vb='120 50 380 290', w=640, col=0, title='Two equal circles with radius 6'))

# the rhombus O A P B pulled out twice (enlarged, the same labels): cut by OP and cut by AB
_f9s = 1.2
def _f9rh(dx):
    O = (dx, 190.0); P = (dx + 110 * _f9s, 190.0)
    A = (dx + 55 * _f9s, 190 - 95.26 * _f9s); B = (dx + 55 * _f9s, 190 + 95.26 * _f9s)
    return O, A, P, B
_f9R1, _f9R2 = _f9rh(40), _f9rh(300)
def _f9rhl(R):
    O, A, P, B = R
    return (f9_poly([O, A, P, B], 'teal', 3) + [('txt', O[0] - 16, O[1], 'O', 'ink', 22, True), ('txt', P[0] + 16, P[1], 'P', 'ink', 22, True),
            ('txt', A[0], A[1] - 18, 'A', 'ink', 22, True), ('txt', B[0], B[1] + 20, 'B', 'ink', 22, True)])
f9num = PIN(GEO('f9num', [
    ('line', _f9rhl(_f9R1) + _f9rhl(_f9R2)),
    ('eq', [('seg', *_f9R1[0], *_f9R1[2], 'teal', 3), ('tint', [_f9R1[0], _f9R1[1], _f9R1[2]], 'teal'),
            ('tint', [_f9R1[0], _f9R1[3], _f9R1[2]], 'teal'), ('txt', _f9R1[1][0], 158, '9√3', 'teal', 24),
            ('txt', _f9R1[1][0], 224, '9√3', 'teal', 24)]),
    ('aob', [('seg', *_f9R2[1], *_f9R2[3], 'orange', 3), ('tint', [_f9R2[0], _f9R2[1], _f9R2[3]], 'orange'),
             ('txt', _f9R2[0][0] + 38, 190, '9√3', 'orange', 22), ('txt', 265, 356, 'each half = one equilateral triangle', 'ink', 22)]),
], vb='0 40 520 330', w=540, col=1, title='The rhombus OAPB cut two ways'))
f9t1 = I('f9t1', 'All five lines $=r\\ \\Rightarrow$ two equilateral triangles', size=28, col=1)
f9t2 = I('f9t2', '$\\angle AOB=60°+60°=120°$, a third of the circle', size=28, col=1)
f9t3 = I('f9t3', 'Shared region $=2\\times($sector $-$ triangle$)$', size=28, col=1)
f9t4 = IH('f9t4', 'Sector: $\\frac13\\cdot36\\pi=12\\pi$', size=30, col=1)
f9t5 = IH('f9t5', 'One piece: $12\\pi-9\\sqrt3$', size=30, col=1)
f9t6 = IH('f9t6', 'Shared region: $24\\pi-18\\sqrt3$', size=30, col=1)

# ---- the ring
F9C, F9RR, F9rr = (320.0, 180.0), 130.0, 80.0
F9M = (320.0, 180.0 + F9rr)
_f9hh = _f9m.sqrt(F9RR ** 2 - F9rr ** 2)
F9RA, F9RB = (320.0 - _f9hh, F9M[1]), (320.0 + _f9hh, F9M[1])
f9ring = PIN(GEO('f9ring', [
    ('line', [('region', f9_ring_d(F9C[0], F9C[1], F9RR, F9rr), 'teal', 0.22), ('circ', *F9C, F9RR), ('circ', *F9C, F9rr),
              ('dot', *F9C, 'O', -20, -14)]),
    ('chord', [('seg', *F9RA, *F9RB, 'ink', 3), ('dot', *F9RA, 'A', -16, 14), ('dot', *F9RB, 'B', 16, 14), ('dot', *F9M, 'M', 0, 24)]),
    ('om', [('seg', *F9C, *F9M, 'teal', 3, True), ('right', F9M[0], F9M[1], 0, 90, 14), ('txt', 306, 222, 'r', 'teal', 26, True)]),
    ('ob', [('seg', *F9C, *F9RA, 'teal', 3, True), ('seg', *F9C, *F9RB, 'teal', 3, True), ('txt', 392, 200, 'R', 'teal', 26, True)]),
    ('half', [('tick', *F9RA, *F9M, 1), ('tick', *F9M, *F9RB, 1), ('txt', 287, 286, 'h', 'teal', 26, True), ('txt', 353, 286, 'h', 'teal', 26, True)]),
    ('tri', [('tint', [F9C, F9M, F9RB], 'orange')]),
], vb='175 35 290 290', w=620, col=0, title='A ring, and a chord of the big circle that touches the small circle'))
f9t7 = IH('f9t7', 'Ring $=\\pi R^2-\\pi r^2$', size=32, col=1)
f9t8 = IH('f9t8', '$r^2+h^2=R^2\\ \\Rightarrow\\ R^2-r^2=h^2$', size=32, col=1)
f9t9 = IH('f9t9', 'Ring $=\\pi(R^2-r^2)=\\pi h^2$', size=32, col=1)
f9t10 = I('f9t10', 'Chord $10\\ \\Rightarrow\\ h=5\\ \\Rightarrow$ ring $=25\\pi$', size=32, col=1)
f9t11 = I('f9t11', 'Ring $=\\pi\\left(\\frac{\\text{chord}}{2}\\right)^2$', size=34, col=1)

# ---- same chord, same ring: three rings to scale (1 unit = 7), each with a chord of 10
def _f9rp(cx, R, r, t1, t2):
    cy = 175.0; y = cy + r * 7
    out = [('region', f9_ring_d(cx, cy, R * 7, r * 7), 'teal', 0.28), ('circ', cx, cy, R * 7, 'ink', 2.5)]
    if r > 0: out.append(('circ', cx, cy, r * 7, 'ink', 2))
    out += [('seg', cx - 35, y, cx + 35, y, 'orange', 4), ('dot', cx, cy), ('txt', cx, 300, t1, 'ink', 19), ('txt', cx, 328, t2, 'teal', 19)]
    return out
f9rings = PIN(GEO('f9rings', [
    ('line', _f9rp(100, 13, 12, 'r = 12, R = 13', '169π − 144π = 25π')),
    ('p2', _f9rp(275, 50 ** 0.5, 5, 'r = 5, R = 5√2', '50π − 25π = 25π')),
    ('p3', _f9rp(420, 5, 0, 'r = 0, R = 5', '25π')),
], vb='0 70 480 275', w=620, col=0, title='Three rings with the same chord, 10'))

video('r26-t33-more-tools', 'lesson', slides=[
    S('More Circle Tools',
      L("More circle tools. These two tools show up in the hardest circle questions, near the end of the section. And "
        "right after this lesson, two questions teach two more tools.")),
    S('Two equal circles',
      L("The first tool. Two equal circles, and each one passes through the center of the other. Here's a circle with "
        "center O, and an equal circle with center P. P is on the first circle, and O is on the second one.",
        show(f9eq['line'], "Here's a circle with center O")),
      L("The circles cross at two points, A and B. What can we say about this shape? No angle is given, so we add helper "
        "lines. We join the centers to the crossing points.", show(f9eq['ab'], 'The circles cross at two points'),
        show(f9eq['radii'], 'We join the centers')),
      L("O A and O B are radii of the first circle. P A and P B are radii of the second circle. And O P? P is on the first "
        "circle, so O P is also a radius. The circles are equal, so all five lines have the same length, r.",
        show(f9eq['op'], 'so O P is also a radius'), show(f9t1, 'all five lines')),
      L("So triangle O A P has three equal sides. It's equilateral, and triangle O B P is equilateral too. Every angle in "
        "them is sixty degrees.", show(f9eq['tri'], 'So triangle O A P')),
      L("Now the angle A O B. It's sixty plus sixty, a hundred twenty degrees. And a hundred twenty degrees is a third of "
        "the circle, because three times a hundred twenty is three hundred sixty.",
        show(f9eq['a120'], "It's sixty plus sixty"), show(f9t2, 'is a third of'))),
    S('The shared region',
      L("Questions love the region the two circles share, the shape in the middle. Draw the chord A B. It cuts this shape "
        "into two equal pieces.", show(f9lens['line'], 'Questions love the region'), show(f9lens['lens'], 'the shape in the middle'),
        show(f9lens['chord'], 'Draw the chord A B')),
      L("Look at the right piece. It's between the chord A B and an arc of the circle with center O. Take the sector A O "
        "B, a third of that circle. Then take away triangle A O B. What's left is exactly the right piece.",
        show(f9lens['piece'], 'Look at the right piece'), show(f9lens['sector'], 'Take the sector'),
        show(f9lens['tri'], 'Then take away triangle')),
      L("The left piece is the same, in the circle with center P. So the shared region is two times, the sector minus "
        "the triangle.", show(f9t3, 'So the shared region'))),
    S('In numbers',
      L("Let's see it in numbers. Say the radius is six. The whole circle is pi times six squared, thirty-six pi. The "
        "sector A O B is a third of it, so it's twelve pi.", show(f9r6['line'], 'Say the radius is six'),
        show(f9r6['sec'], 'The sector A O B'), show(f9t4, 'so it\'s twelve pi')),
      L("Now triangle A O B. The four radii make a rhombus, O A P B. Let's take it out. O P cuts it into our two "
        "equilateral triangles. Remember, the area of an equilateral triangle is a squared, times root three, over four. "
        "Six squared is thirty-six, and thirty-six over four is nine, so each one is nine root three.",
        show(f9r6['rh'], 'make a rhombus'), show(f9num['line'], "Let's take it out"), show(f9num['eq'], 'O P cuts it')),
      L("Now cut the same rhombus the other way, with the chord A B. A diagonal cuts a rhombus into two equal halves, and "
        "triangle A O B is one of them. So it's half of the rhombus, the same as one equilateral triangle, nine root "
        "three.", show(f9num['aob'], 'with the chord A B')),
      L("So one piece is twelve pi minus nine root three. The shared region is two pieces, twenty-four pi minus eighteen "
        "root three.", show(f9t5, 'So one piece'), show(f9t6, 'The shared region is two pieces'))),
    S('Chord of a ring',
      L("The second tool is a ring. Two circles with the same center, O, and the ring between them. The ring is the big "
        "circle minus the small circle, pi R squared minus pi r squared.", show(f9ring['line'], 'Two circles with the same center'),
        show(f9t7, 'The ring is the big circle')),
      L("Now a chord A B of the big circle that just touches the small circle, at the point M. M is a point of tangency, "
        "so the automatic helper line is the radius O M. It's perpendicular to the chord.",
        show(f9ring['chord'], 'Now a chord A B'), show(f9ring['om'], 'the automatic helper line')),
      L("Draw O A and O B too. They're radii of the big circle, so triangle A O B is isosceles. O M is the height to its "
        "base, and in an isosceles triangle that height is also a median. So M cuts the chord in half. Call each half h.",
        show(f9ring['ob'], 'Draw O A and O B'), show(f9ring['half'], 'So M cuts the chord in half')),
      L("Look at the right triangle O M B. Its legs are r and h, and its hypotenuse is R. By Pythagoras, r squared plus h "
        "squared is R squared. So R squared minus r squared is h squared.", show(f9ring['tri'], 'Look at the right triangle'),
        show(f9t8, 'By Pythagoras')),
      L("And the ring? Pi R squared minus pi r squared is pi times, R squared minus r squared. That's pi times h squared. "
        "So the ring depends only on the chord.", show(f9t9, 'And the ring'))),
    S('Same chord, same ring',
      L("So if the chord is ten, then h is five, and the ring is twenty-five pi. We don't need either radius.",
        show(f9t10, 'So if the chord is ten')),
      L("Let's check it on rings with a chord of ten. Radii twelve and thirteen, the five, twelve, thirteen triangle. A "
        "hundred sixty-nine pi minus a hundred forty-four pi is twenty-five pi.", show(f9rings['line'], 'Radii twelve and thirteen')),
      L("Radii five and five root two, a silver triangle with legs five and five. Five root two, squared, is fifty. Fifty "
        "pi minus twenty-five pi is twenty-five pi again.", show(f9rings['p2'], 'Radii five and five root two')),
      L("And if the small circle shrinks to a single point? Then the chord is a diameter of ten, and the ring is a whole "
        "circle with radius five, twenty-five pi. The same answer.", show(f9rings['p3'], 'shrinks to a single point')),
      L("So when a chord of the big circle touches the small circle, the ring is pi times half the chord, squared. Now "
        "let's see the other two tools in questions. [pause] Okay. I'll see you in the next video.",
        show(f9t11, 'So when a chord'))),
])


# ================================================================================================ solve-q-r26-t33-04
# V3: one board figure in the right column: the colour copy small on the left (same labels), the segment tinted teal and
# a dashed box around the sector; next to it the ENLARGED cut-out of the sector with the same labels and tint (the
# segment is thin). The scheme: the sector wedge teal, then the triangle orange on top (what stays teal is the segment).
# The values are written on the cut-out and in rows below it as they are found. The triangle slide: the radii 6, the
# base angles, AB = 6, the area; the dashed height (gold triangles) as the check. The traps slide: the cut-out with the
# result, and each trap written in red as it is ruled out.
F9QO, F9QR = (320.0, 180.0), 109.5
def _f9sm(p): return (110 + (p[0] - 320) * 0.85, 140 + (p[1] - 180) * 0.85)
def _f9bg(p): return (410 + (p[0] - 320) * 2.1, 300 + (p[1] - 180) * 2.1)
_f9qA, _f9qB = gpt(320, 180, F9QR, 120), gpt(320, 180, F9QR, 60)
_sO, _sA, _sB = _f9sm(F9QO), _f9sm(_f9qA), _f9sm(_f9qB)
_bO, _bA, _bB = _f9bg(F9QO), _f9bg(_f9qA), _f9bg(_f9qB)
_sR, _bR = F9QR * 0.85, F9QR * 2.1
_bM = ((_bA[0] + _bB[0]) / 2.0, _bA[1])
_f9small = [('circ', *_sO, _sR, 'ink', 2.5), ('seg', *_sA, *_sB, 'ink', 2.5), ('seg', *_sO, *_sA, 'ink', 2.5), ('seg', *_sO, *_sB, 'ink', 2.5),
            ('dot', *_sO), ('arc', *_sO, 20, 60, 120, 'ink'), ('txt', _sO[0], _sO[1] - 38, '60°', 'ink', 17),
            ('txt', _sA[0] - 10, _sA[1] - 15, 'A', 'ink', 22, True), ('txt', _sB[0] + 10, _sB[1] - 15, 'B', 'ink', 22, True),
            ('txt', _sO[0], _sO[1] + 20, 'O', 'ink', 22, True)]
_f9segS = [('cseg', *_sO, _sR, 60, 120, 'teal'), ('arcw', *_sO, _sR, 60, 120, 'teal', 4)]
_f9big = [('arc', *_bO, _bR, 55, 125, 'ink'), ('seg', *_bA, *_bB, 'ink', 3), ('seg', *_bO, *_bA, 'ink', 3), ('seg', *_bO, *_bB, 'ink', 3),
          ('dot', *_bO), ('arc', *_bO, 36, 60, 120, 'ink'), ('txt', _bO[0], _bO[1] - 54, '60°', 'ink', 24),
          ('txt', _bA[0] - 18, _bA[1] - 16, 'A', 'ink', 28, True), ('txt', _bB[0] + 18, _bB[1] - 16, 'B', 'ink', 28, True),
          ('txt', _bO[0], _bO[1] + 26, 'O', 'ink', 28, True)]
_f9segB = [('cseg', *_bO, _bR, 60, 120, 'teal'), ('arcw', *_bO, _bR, 60, 120, 'teal', 6)]
_bx0, _bx1, _by0, _by1 = _sA[0] - 8, _sB[0] + 8, _sO[1] - _sR - 8, _sO[1] + 8
_f9box = [('seg', _bx0, _by0, _bx1, _by0, 'teal', 2, True), ('seg', _bx1, _by0, _bx1, _by1, 'teal', 2, True),
          ('seg', _bx1, _by1, _bx0, _by1, 'teal', 2, True), ('seg', _bx0, _by1, _bx0, _by0, 'teal', 2, True),
          ('seg', _bx1 + 8, 80, 245, 80, 'teal', 2.5), ('seg', 233, 72, 246, 80, 'teal', 2.5), ('seg', 233, 88, 246, 80, 'teal', 2.5)]
_f9sch = [('txt', 115, 262, 'segment =', 'teal', 29), ('txt', 115, 294, 'sector − triangle', 'ink', 29)]
_f9secv = [('txt', 290, 364, 'sector: ⅙ · 36π = 6π', 'teal', 30)]
F9VB = '0 40 580 400'
f9q4a = PIN(GEO('f9q4a', [
    ('line', _f9small),
    ('seg', _f9segS),
    ('cut', _f9box + _f9big + _f9segB),
    ('sector', [('wedge', *_bO, _bR, 60, 120, 'teal'), ('seg', *_bO, *_bA, 'teal', 4), ('seg', *_bO, *_bB, 'teal', 4)]),
    ('tri', [('tint', [_bO, _bA, _bB], 'orange'), ('seg', *_bA, *_bB, 'orange', 4)]),
    ('scheme', _f9sch),
    ('secv', _f9secv),
], vb=F9VB, w=580, title='The circle with the shaded segment, and the sector enlarged'))

_f9b2 = _f9small + _f9segS + _f9box + _f9big + _f9segB + [('tint', [_bO, _bA, _bB], 'orange')] + _f9sch + _f9secv
f9q4b = PIN(GEO('f9q4b', [
    ('line', _f9b2),
    ('sides', [('txt', 320, 200, '6', 'orange', 32), ('txt', 500, 200, '6', 'orange', 32)]),
    ('ang', [('arc', *_bA, 36, 300, 360, 'orange'), ('arc', *_bB, 36, 180, 240, 'orange'),
             ('txt', _bA[0] + 58, _bA[1] + 22, '60°', 'orange', 26), ('txt', _bB[0] - 58, _bB[1] + 22, '60°', 'orange', 26)]),
    ('ab6', [('txt', _bM[0], _bM[1] - 16, '6', 'orange', 26)]),
    ('area', [('txt', 290, 398, '6² · √3 ÷ 4 = 36√3 ÷ 4 = 9√3', 'orange', 30), ('txt', 448, 150, '9√3', 'orange', 30)]),
    ('h', [('seg', *_bO, *_bM, 'teal', 3, True), ('right', _bM[0], _bM[1], 270, 360, 14), ('txt', 384, 160, '3√3', 'teal', 22),
           ('txt', 352, 90, '3', 'teal', 22)]),
    ('hv', [('txt', 290, 430, 'or: 6 · 3√3 ÷ 2 = 9√3', 'teal', 28)]),
    ('ans', [('txt', 115, 328, '= 6π − 9√3', 'ink', 31)]),
], vb=F9VB, w=580, title='Triangle AOB: equilateral with side 6'))

_f9b3 = _f9big + _f9segB + [('txt', 448, 150, '9√3', 'orange', 30), ('txt', 410, 372, 'segment = 6π − 9√3', 'teal', 31)]
f9q4c = PIN(GEO('f9q4c', [
    ('line', _f9b3),
    ('t1', [('txt', 118, 70, '6 · 6 ÷ 2 = 18', 'red', 29), ('txt', 118, 102, 'needs a right angle ✗', 'red', 23)]),
    ('t2', [('txt', 128, 160, '12π = ⅓ of the circle ✗', 'red', 22)]),
    ('t3a', [('txt', 118, 225, '3π < 3 · 4 = 12', 'ink', 29)]),
    ('t3b', [('txt', 118, 265, '9√3 = √243', 'ink', 29), ('txt', 118, 300, '> √144 = 12', 'ink', 29)]),
    ('t3c', [('txt', 118, 350, '3π − 9√3 < 0 ✗', 'red', 30)]),
], vb=F9VB, w=580, title='Where the other choices come from'))
for _f9g in (f9q4a, f9q4b, f9q4c): _R(_f9g, 210, x=1000)

video('solve-q-r26-t33-04', 'solution', qid='q-r26-t33-04', slides=[
    SM('Sector minus triangle', 'Sector minus triangle',
      L("In a circle with center O and radius six centimeters, angle A O B is sixty degrees. What is the area of the "
        "shaded region between the chord A B and the arc A B, in square centimeters?",
        pt('stem', 'In a circle with center O', 'hl', 10.0), voice='calm', pause=0.5),
      L("A shaded area again. In shaded areas, the most common way is subtracting areas. So first a scheme. What minus "
        "what gives the shaded part?", pt('stem: ask', 'A shaded area again')),
      L("[short pause] The shaded part sits between a chord and its arc. A region like this is called a segment. It's "
        "thin, so let's look at it bigger, with the same labels.", show(f9q4a['line'], 'The shaded part sits'),
        show(f9q4a['seg'], 'is called a segment'), show(f9q4a['cut'], "so let's look at it bigger")),
      L("Take the sector A O B, the slice from O out to the arc. Then take away triangle A O B. What's left is exactly the "
        "segment. So the segment is the sector minus the triangle.", show(f9q4a['sector'], 'Take the sector'),
        show(f9q4a['tri'], 'Then take away triangle'), show(f9q4a['scheme'], 'So the segment is')),
      L("The sector first. Sixty degrees is a sixth of the circle, because six times sixty is three hundred sixty. The "
        "whole circle is pi times six squared, thirty-six pi. A sixth of thirty-six pi is six pi.",
        show(f9q4a['secv'], 'A sixth of thirty-six pi')),
      L("Before we work on the triangle, let's look at the choices. The answer must be six pi minus the triangle. Choice "
        "number two starts with twelve pi, and choice number four starts with three pi. So both are out.",
        mk('cross', 'choice 2', 'Choice number two starts'), mk('cross', 'choice 4', 'choice number four starts'))),
    SM('The triangle', 'The triangle',
      L("Now triangle A O B. O A and O B are both radii, so both are six, and the triangle is isosceles. The angle between "
        "them is sixty. So the two base angles share a hundred eighty minus sixty, which is a hundred twenty. That's sixty "
        "each.", show(f9q4b['line'], 'Now triangle A O B'), show(f9q4b['sides'], 'so both are six'),
        show(f9q4b['ang'], "That's sixty each")),
      L("Sixty, sixty and sixty. So it's an equilateral triangle, and A B is six too.", show(f9q4b['ab6'], 'A B is six too')),
      L("The area of an equilateral triangle is a squared, times root three, over four. Six squared is thirty-six, and "
        "thirty-six over four is nine. So the area is nine root three.", show(f9q4b['area'], 'Six squared is thirty-six')),
      L("If you don't remember the formula, draw the height from O. It cuts the triangle into two gold triangles. The "
        "short leg is three, so the height is three root three. Six times three root three, over two, is nine root three "
        "again.", show(f9q4b['h'], 'draw the height from O'), show(f9q4b['hv'], 'Six times three root three')),
      L("So the segment is six pi minus nine root three. Choice number three is our answer. In the exam, we mark it and "
        "move on.", show(f9q4b['ans'], 'So the segment is'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('The traps', 'The traps',
      L("[pause] We're in a lesson, so let's see where the other choices come from. Choice number one is six pi minus "
        "eighteen. Eighteen is six times six, over two. That's the area of a right triangle with two legs of six, but our "
        "angle is sixty, not ninety.", show(f9q4c['line'], "We're in a lesson"), show(f9q4c['t1'], 'Eighteen is six times six'),
        mk('cross', 'choice 1', 'not ninety')),
      L("Choice number two is twelve pi minus nine root three. Twelve pi is a third of the circle. That's the sector of a "
        "hundred twenty degrees, not sixty.", show(f9q4c['t2'], 'Twelve pi is a third'), mk('cross', 'choice 2', 'not sixty')),
      L("And choice number four, three pi minus nine root three. Is it even positive? Pi is less than four, so three pi is "
        "less than twelve. And nine is the root of eighty-one, so nine root three is the root of two hundred forty-three. "
        "That's more than the root of a hundred forty-four, which is twelve.", show(f9q4c['t3a'], 'Pi is less than four'),
        show(f9q4c['t3b'], 'And nine is the root')),
      L("So three pi minus nine root three is a number below twelve, minus a number above twelve. It's negative, and an "
        "area can't be negative. They do that a lot, a negative answer hidden behind pi and roots.",
        show(f9q4c['t3c'], "It's negative"), mk('cross', 'choice 4', 'area can\'t be negative')),
      L("So when a shaded region sits between a chord and its arc, think sector minus triangle. [pause] Okay. I'll see "
        "you in the next question.", pt('f9q4c_line', 'think sector minus triangle'))),
])


# ================================================================================================ solve-q-r26-t33-05
# V3: a small colour copy (same labels) at the top left with the region of the trapezoid boxed, and next to it an
# ENLARGED cut-out of that region (the same labels; the circles as arcs), built at her words: the radii to the points of
# tangency dashed teal with their right angles, their values and parallel arrows; the line of the centers dashed through
# the touching point; the right trapezoid tinted. Slide 2: BE dashed from B, the rectangle EBCD tinted orange with
# equal-side ticks, AE traced thick with 6, the right triangle ABE tinted teal with 10 and 8, DC = 8 under DC; the
# working written in rows under the small copy. Slide 3: the traps drawn red on the cut-out (AB, AE) and written in red;
# the short formula and its check in rows.
F9QA, F9QB, F9QD, F9QC = (250.0, 192.0), (378.0, 288.0), (250.0, 320.0), (378.0, 320.0)
F9QT = (250 + 128 * 0.8, 192 + 128 * 0.6)
F9QE = (250.0, 288.0)
def _f9s5(p): return (10 + (p[0] - 102) * 0.6, 40 + (p[1] - 64) * 0.6)
def _f9z5(p): return (300 + (p[0] - 250) * 1.9, 120 + (p[1] - 192) * 1.9)
_sA5, _sB5, _sD5, _sC5 = [_f9s5(p) for p in (F9QA, F9QB, F9QD, F9QC)]
_zA, _zB, _zD, _zC, _zT, _zE = [_f9z5(p) for p in (F9QA, F9QB, F9QD, F9QC, F9QT, F9QE)]
_f9q5s = [('circ', *_sA5, 128 * 0.6, 'ink', 2.2), ('circ', *_sB5, 32 * 0.6, 'ink', 2.2), ('seg', *_f9s5((102, 320)), *_f9s5((480, 320)), 'ink', 2.2),
          ('dot', *_sA5), ('dot', *_sB5), ('txt', _sA5[0] - 12, _sA5[1] - 6, 'A', 'ink', 18, True),
          ('txt', _sB5[0] + 18, _sB5[1] - 16, 'B', 'ink', 18, True), ('txt', _sD5[0], _sD5[1] + 14, 'D', 'ink', 18, True),
          ('txt', _sC5[0], _sC5[1] + 14, 'C', 'ink', 18, True)]
_sx0, _sy0, _sx1, _sy1 = _sA5[0] - 7, _sA5[1] - 7, _sC5[0] + 7, _sC5[1] + 7
_f9q5cut = ([('tint', [_sA5, _sB5, _sC5, _sD5], 'teal'), ('seg', _sx0, _sy0, _sx1, _sy0, 'teal', 2, True), ('seg', _sx1, _sy0, _sx1, _sy1, 'teal', 2, True),
             ('seg', _sx1, _sy1, _sx0, _sy1, 'teal', 2, True), ('seg', _sx0, _sy1, _sx0, _sy0, 'teal', 2, True),
             ('seg', _sx1 + 6, 110, 262, 110, 'teal', 2.5), ('seg', 250, 102, 263, 110, 'teal', 2.5), ('seg', 250, 118, 263, 110, 'teal', 2.5)]
            + [('arc', *_zA, 128 * 1.9, 256, 300, 'ink'), ('circ', *_zB, 32 * 1.9, 'ink', 2.5), ('seg', 272, _zD[1], 608, _zD[1], 'ink', 3),
               ('dot', *_zA), ('dot', *_zB), ('dot', *_zD), ('dot', *_zC), ('txt', _zA[0] - 18, _zA[1] - 10, 'A', 'ink', 28, True),
               ('txt', _zB[0] + 2, _zB[1] - 24, 'B', 'ink', 28, True), ('txt', _zD[0], _zD[1] + 26, 'D', 'ink', 28, True),
               ('txt', _zC[0], _zC[1] + 26, 'C', 'ink', 28, True)])
_f9q5r = [('seg', *_sA5, *_sD5, 'teal', 2, True), ('seg', *_sB5, *_sC5, 'teal', 2, True),
          ('seg', *_zA, *_zD, 'teal', 3, True), ('seg', *_zB, *_zC, 'teal', 3, True), ('right', *_zD, 0, 90, 15), ('right', *_zC, 90, 180, 15)]
_f9q5v = [('txt', _zA[0] - 20, 225, '8', 'teal', 28), ('txt', _zC[0] + 18, 336, '2', 'teal', 26),
          ('par', *_zD, *_zA, 1), ('par', *_zC, *_zB, 1)]
_f9q5ab = [('seg', *_sA5, *_sB5, 'teal', 2, True), ('seg', *_zA, *_zB, 'teal', 3, True), ('dot', *_zT)]
_f9q5abv = [('txt', 432, 178, '10', 'teal', 28), ('txt', 126, 238, 'AB = 8 + 2 = 10', 'teal', 28)]
F9VB5 = '0 30 615 470'
f9q5a = PIN(GEO('f9q5a', [
    ('line', _f9q5s),
    ('cut', _f9q5cut),
    ('radii', _f9q5r),
    ('vals', _f9q5v),
    ('ab', _f9q5ab),
    ('abv', _f9q5abv),
    ('trap', [('tint', [_zA, _zB, _zC, _zD], 'teal'), ('txt', 126, 272, 'right trapezoid', 'teal', 28)]),
], vb=F9VB5, w=580, title='Two touching circles, and the part between the radii enlarged'))

_f9q5b0 = _f9q5s + _f9q5cut + _f9q5r + _f9q5v + _f9q5ab + _f9q5abv
f9q5b = PIN(GEO('f9q5b', [
    ('line', _f9q5b0),
    ('be', [('dot', *_zE), ('seg', *_zB, *_zE, 'teal', 3, True), ('txt', _zE[0] - 18, _zE[1] - 4, 'E', 'ink', 28, True)]),
    ('rect', [('tint', [_zE, _zB, _zC, _zD], 'orange'), ('tick', *_zE, *_zD, 1, 'orange'), ('tick', *_zB, *_zC, 1, 'orange'),
              ('tick', *_zE, *_zB, 2, 'orange'), ('tick', *_zD, *_zC, 2, 'orange'),
              ('txt', 126, 272, 'ED = BC = 2', 'orange', 28), ('txt', 126, 304, 'EB = DC', 'orange', 28)]),
    ('ae', [('seg', *_zA, *_zE, 'teal', 7), ('txt', _zA[0] + 18, 215, '6', 'teal', 28), ('txt', 126, 336, 'AE = 8 − 2 = 6', 'teal', 28)]),
    ('tri', [('tint', [_zA, _zB, _zE], 'teal')]),
    ('tv', [('txt', 470, 290, '8', 'teal', 28), ('txt', 126, 370, '10² − 6² = 64', 'teal', 28), ('txt', 126, 402, 'BE = √64 = 8', 'teal', 28)]),
    ('dc', [('txt', 421, _zD[1] + 26, '8', 'orange', 30), ('txt', 126, 438, 'DC = 8', 'ink', 28)]),
], vb=F9VB5, w=580, title='Cut off a right triangle'))

_f9q5c0 = (_f9q5s + _f9q5cut + _f9q5r + _f9q5v + _f9q5ab + [('txt', 432, 178, '10', 'teal', 28)]
           + [('dot', *_zE), ('seg', *_zB, *_zE, 'teal', 3, True), ('txt', _zE[0] - 18, _zE[1] - 4, 'E', 'ink', 28, True),
              ('txt', _zA[0] + 18, 215, '6', 'teal', 28), ('txt', 470, 290, '8', 'teal', 28), ('txt', 421, _zD[1] + 26, '8', 'orange', 30)])
f9q5c = PIN(GEO('f9q5c', [
    ('line', _f9q5c0),
    ('t1', [('seg', *_zA, *_zB, 'red', 5), ('txt', 126, 232, '10 = AB ✗', 'red', 28)]),
    ('t3', [('seg', *_zA, *_zE, 'red', 7), ('txt', 126, 264, '6 = AE ✗', 'red', 28)]),
    ('t4', [('txt', 126, 296, '6² + 10² = 136', 'red', 28), ('txt', 126, 328, '√136 = 2√34 > 10 ✗', 'red', 28)]),
    ('sc1', [('txt', 126, 366, 'DC = 2√(Rr)', 'teal', 28), ('txt', 126, 398, '= 2√16 = 8', 'teal', 28)]),
    ('sc2', [('txt', 126, 436, '9 and 4: √(13² − 5²) = 12', 'ink', 22), ('txt', 126, 466, '2√(9 · 4) = 2√36 = 12 ✓', 'ink', 22)]),
], vb=F9VB5, w=580, title='The traps and a short formula'))
for _f9g in (f9q5a, f9q5b, f9q5c): _R(_f9g, 210, x=1000)

video('solve-q-r26-t33-05', 'solution', qid='q-r26-t33-05', slides=[
    SM('Radii and the centers', 'Radii and the centers',
      L("Two circles with centers A and B touch each other from the outside. Their radii are eight centimeters and two "
        "centimeters. A line touches the two circles at D and C, as in the figure. What is the length of D C, in "
        "centimeters?", pt('stem', 'Two circles with centers A and B', 'hl', 11.0), voice='calm', pause=0.5),
      L("We need a length, D C, but the figure has only two circles and a line. So let's go to the givens and see what "
        "each one gives us. We'll build a right triangle, and at the end there's a short formula too.",
        pt('stem: ask', 'We need a length')),
      L("[short pause] Let's look at the bottom part of the figure, bigger. D and C are points of tangency. So the "
        "automatic helper line, a radius to each point of tangency. Draw A D and B C. A radius is perpendicular to the "
        "tangent, so there's a right angle at D and at C.", show(f9q5a['line'], "Let's look at the bottom part"),
        show(f9q5a['cut'], 'D and C are points'), show(f9q5a['radii'], 'Draw A D and B C')),
      L("A D is a radius of the big circle, eight. B C is a radius of the small circle, two. Both are perpendicular to the "
        "same line, so they're parallel to each other.", show(f9q5a['vals'], 'A D is a radius')),
      L("The circles touch, so a second helper line. Join the centers. A B passes through the point where the circles "
        "touch. The first part is a radius of the big circle, eight, and the second part is a radius of the small one, "
        "two. So A B is eight plus two, ten.", show(f9q5a['ab'], 'Join the centers'), show(f9q5a['abv'], 'So A B is eight plus two')),
      L("Now look at A B C D. It has two right angles, at D and at C, and two parallel sides. It's a right trapezoid, and "
        "D C, the side we want, is its bottom.", show(f9q5a['trap'], 'Now look at A B C D'))),
    SM('Cut off a right triangle', 'Cut off a right triangle',
      L("To use Pythagoras, we need a right triangle with D C in it, or a copy of D C. So from B, draw a line parallel to "
        "D C, until it meets A D. Call that point E.", show(f9q5b['line'], 'To use Pythagoras'), show(f9q5b['be'], 'from B, draw a line')),
      L("E B C D is a rectangle, because all its angles are right angles. So E D equals B C, which is two. And E B equals "
        "D C, the length we want.", show(f9q5b['rect'], 'E B C D is a rectangle')),
      L("Now A E is the whole radius A D, minus E D. Eight minus two is six.", show(f9q5b['ae'], 'Eight minus two')),
      L("Look at the right triangle A B E. The hypotenuse A B is ten, and one leg, A E, is six. Six and ten, that's the "
        "six, eight, ten triangle, so the other leg, B E, is eight. With Pythagoras, ten squared minus six squared is a "
        "hundred minus thirty-six, sixty-four. And the root of sixty-four is eight.",
        show(f9q5b['tri'], 'Look at the right triangle'), show(f9q5b['tv'], 'so the other leg')),
      L("B E equals D C, so D C is eight. Choice number two is our answer.", show(f9q5b['dc'], 'so D C is eight'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Traps and a shortcut', 'Traps and a shortcut',
      L("[pause] Now the traps. Ten, choice number one, is A B, the distance between the centers. It's not the tangent. "
        "And six, choice number three, is only A E, the difference between the radii.", show(f9q5c['line'], 'Now the traps'),
        show(f9q5c['t1'], 'Ten, choice number one'), mk('cross', 'choice 1', 'the distance between the centers'),
        show(f9q5c['t3'], 'And six, choice number three'), mk('cross', 'choice 3', 'the difference between the radii')),
      L("Two root thirty-four, choice number four, comes from adding the squares. Thirty-six plus a hundred is a hundred "
        "thirty-six, and the root of a hundred thirty-six is two root thirty-four. But A B is the hypotenuse, the longest "
        "side. Two root thirty-four is more than ten, and a leg can't be longer than the hypotenuse.",
        show(f9q5c['t4'], 'comes from adding the squares'), mk('cross', 'choice 4', "a leg can't be longer")),
      L("And now the short formula, for two circles that touch from the outside. D C is two times the root of R times r. "
        "Here that's two times the root of eight times two, two times the root of sixteen. Two times four is eight.",
        show(f9q5c['sc1'], 'D C is two times the root')),
      L("Let's check it on other circles, with radii nine and four. The centers are thirteen apart, and the difference "
        "of the radii is five. Five, twelve, thirteen, so the tangent is twelve. And the formula gives two times the root "
        "of thirty-six, two times six, twelve. The same.", show(f9q5c['sc2'], 'with radii nine and four')),
      L("The formula only works when the circles touch. If they don't, cut off the same right triangle, with the distance "
        "between the centers as its hypotenuse. [pause] Okay. I'll see you in the next question.",
        pt('f9q5c_line', 'The formula only works'))),
])

# carry-over boxes on the continuation slides (V2): the next step uses these results
CARRY33 = globals().get('CARRY33', {})

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
 "geo33-g094": "AB is tangent to a circle with center O and radius 6 cm. Given: $OA=OB$ and angle AOB is 90°. What is the area inside triangle AOB but outside the circle (in cm²)?",
 "geo33-g095": "ABC is a right triangle whose sides AB and AC are tangent to a circle with center O at B and D, respectively. B, O, E and C lie on one straight line, and E is on the circle. Given: $OE=EC=4$ cm. What is the area of the shaded region between CD, CE and the minor arc DE (in cm²)?",
 "geo33-g096": "A semicircle has center K and radius r. M and N lie on its curved boundary, and angle KMN is 60°. What is the ratio of the perimeter of the semicircle to the perimeter of triangle KMN?",
 "geo33-g097": "Square KLMN is circumscribed about a circle, and square PQRS is inscribed in the circle. What is the ratio of the area of PQRS to the area of KLMN?",
 "geo33-g098": "A circle with center O has radius 8 cm. A, G, F, E and D lie on the same arc, in that order. B and C lie on the arc AD that does not contain F. Given:\n$\\begin{cases} \\angle ABF=28° \\\\ \\angle FCD=57° \\\\ \\angle GOE=80° \\end{cases}$\nWhat is the sum of the lengths of the highlighted arcs AG and ED (in cm)?",
 "geo33-g099": "Two congruent circles with centers O and P have radius 6 cm and intersect at A and B. The minor arc AB is one quarter of the circumference of each circle. What is the area of the union of the two circles (in cm²)?",
 "geo33-g100": "A circle with center O has radius 4 cm. The opposite sides AD and BC of rectangle ABCD are tangent to the circle at E and F, respectively. The area of the rectangle equals the area of the circle. What is the length of BC (in cm)?",
 "geo33-g101": "A smaller circle lies inside a larger circle and is internally tangent to it at A. AB is a diameter of the larger circle, AC is a diameter of the smaller circle, and $CB=10$ cm. The area inside the larger circle but outside the smaller one is $65\\pi$ cm². What is the radius of the smaller circle (in cm)?",
 "geo33-g102": "ABC is an isosceles triangle. Given:\n$\\begin{cases} AB=AC \\\\ \\angle BAC=4\\theta\\text{ degrees, where }0<\\theta<45 \\end{cases}$\nB lies on a circle with center O and radius r. AB and BC meet the circle again at D and E, respectively. What is the length of the arc DE that does not contain B?",
 "geo33-g085": "AB is a diameter of a circle with center O, and $AB=20$ cm. Given: angle AOC is 120°. What is the area of the shaded triangle OBC (in cm²)?",
 "geo33-g086": "An isosceles triangle ABC is inscribed in a circle with center O, with $AB=AC$. Given: angle BAC is 56°. What is angle ABO?",
 "geo33-g087": "AE is a diameter of a circle with center O. B, C and D lie on the same semicircle, in that order. Given:\n$\\begin{cases} AB=BC=CD=DE \\\\ AO=5\\text{ cm} \\end{cases}$\nWhich of the following statements is not true?",
 "geo33-g088": "Two congruent circles with centers O and M are externally tangent. Each has radius 7 cm. MA and MB are tangent to the circle with center O at A and B. What is the smaller angle AOB?",
 "geo33-g089": "The circumference of the smaller circle is $10\\pi$ cm, and the shaded area inside the larger circle but outside the smaller one is $39\\pi$ cm². Between which two values is the circumference of the larger circle (in cm)?",
 "geo33-g090": "The sides of triangle ABC are 12 cm, 35 cm and 37 cm. What is the circumference of the circle circumscribed about the triangle (in cm)?",
 "geo33-g091": "A circle has radius $\\sqrt{35}$ cm. Its central angles are $\\alpha$ and $\\beta$ in turn, five of each, as in the figure. One sector with angle $\\alpha$ and one sector with angle $\\beta$ are shaded. What is their total area (in cm²)?",
 "geo33-g092": "Three circles with centers A, B and C are externally tangent to one another. Their radii are 6 cm, 14 cm and 15 cm, respectively. What is the length of the highlighted arc of the circle with center A (in cm)?",
 "geo33-g082": "A circle with center O has radius 10 cm. The highlighted arc AB has length $4\\pi$ cm. What is α?",
 "geo33-g083": "A circle with center O has radius 3 cm. Two non-overlapping shaded sectors have central angles of 40° and 120°. What is their total area (in cm²)?",
 "geo33-g076": "A, B and C lie on a circle with center O, with B on the minor arc AC. Given: angle AOC is 104°. What is angle ABC?",
 "geo33-g078": "PD and PE are tangent to the circle at D and E. A lies on the major arc DE. Given: angle DPE is 68°. What is angle DAE?",
 "geo33-g080": "The numerical value of a circle’s area in cm² is 4 times as much as the numerical value of its circumference in cm. What is its radius (in cm)?",
 "q-r26-t33-01": "Chord AB of a circle with center O is 16 cm long. The distance from O to AB is 6 cm. What is the circumference of the circle (in cm)?",
 "q-r26-t33-02": "A circle is inscribed in a right triangle whose legs are 8 cm and 15 cm. What is the radius of the circle (in cm)?",
 "q-r26-t33-03": "The circumference of a circle increases by 50%. By what percent does its area increase?",
 "q-r26-t33-04": "In a circle with center O and radius 6 cm, angle AOB is 60°. What is the area of the shaded region between chord AB and arc AB (in cm²)?",
 "q-r26-t33-05": "Two circles with centers A and B touch each other from the outside. Their radii are 8 cm and 2 cm. A line touches the two circles at D and C, as in the figure. What is the length of DC (in cm)?"
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
MV.carry(_types.SimpleNamespace(**globals()), CARRY33)
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
