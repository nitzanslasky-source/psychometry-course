"""Topic 26 (Work and rates) - the scripts for the teacher's own-voice reading (2026-10-21), written from the first draft
to the Codex review standard, the clarity style, W1-W21, R37 (core methods taught in the lessons), the method vocabulary
and the method visuals, built exactly like topics 22-25 (math_patches/_ai_vis_t25.py: the DSL and the visual passes are
copied here, so the topics stay independent; the stem-part highlighting as in topic 22).

The camera lesson 'wp-092' (Work, Rate and Time) gets a full reading script with more examples, split into three parts
of about 3-4 minutes (math_patches/_camera_parts.py). The lessons that carry the topic's core methods (R37) grew and are
split into parts too (not on camera): 'wp-094' (working together) and 'wp-097' (team questions, the V method). Every
other topic-26 video gets a script that SHE reads aloud in the Reading Studio; reading_to_video.py then times the
handwriting and the visuals to her words. The summary video r26-t26-summary is not read: summary_pages/t26.json
(python3 summary_pages.py 26) replaces it.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t26.py [vid ...] writes it);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t26.py ai_redo_t26() (runs LAST) rebuilds the slides from studio_slides(vid) and then
                    _ai_visual.apply() adds the click items, POINT highlights and pen marks around it.

Spec DSL (as in topic 25): video / S / L / I / IH (a hand-written board line) / show / pt / mk; the topic-26 pictures of
her Hebrew course, built in layers at the spoken words: TRI26 (the formula triangle, wp 5945-5962: work on top, rate and
time at the bottom, "I hide the one I want"), VT (the V method's team | work | time table, wp 6285-6341, from
_method_visuals.VTABLE: the table, row 1, row 2, the V or the upside-down V, the rule), TBL (the ratio table of topic 22,
the common-time rows of wp 6165-6206 / 6577-6600: a row per worker, stretched to the same time, then the sum row), SAW
(the seesaw of topic 25, for the average rate). The concept map (NEW / REMINDER per video) is in
~/Downloads/Topic-26-AI-scripts-review.md.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(HERE) != 'math_patches':      # a test copy elsewhere still reads and writes the real studio files
    HERE = '/Users/nitzanslasky/psychometry-course/studio-build/math_patches'
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t26ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-26 flow order of the scripts
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


# 2026-10-18 visual check: the last baseline of each question's stem on the board (measured on the rendered step
# frames). The right column starts just below it, so its rows keep their own spacing; otherwise the renderer pushes
# every row under the one above with a 14 px gap (cramped rows).
QBOT = {'solve-q-r26-t26-01': 181, 'solve-q-r26-t26-02': 242, 'solve-q-r26-t26-03': 242, 'solve-q-r26-t26-04': 242, 'solve-wp26-g093': 242, 'solve-wp26-g095': 229, 'solve-wp26-g096': 229, 'solve-wp26-g098': 181, 'solve-wp26-g100': 286, 'solve-wp26-g101': 286, 'solve-wp26-g102': 286, 'solve-wp26-g103': 242, 'solve-wp26-g104': 232, 'solve-wp26-g105': 242, 'solve-wp26-g105b': 242, 'solve-q-r26-t26-21': 286}   # measured on the frames (2026-10-21)


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
        out = []; ycol = max(100, QBOT.get(vid, 0) + 50) if V['kind'] == 'solution' else 78
        for it in items:
            d = {k: v for k, v in it.items() if not k.startswith('_')}
            if it['_col'] == 1 and not solo:
                if d['k'] == 'vis':
                    d['w'] = min(d.get('w', 540), 540); d['h'] = int(round(d['h'] * d['w'] / it['w']))
                y_here = ycol
                if not d.get('over'): ycol += (d['h'] if d['k'] == 'vis' else int(d.get('size', 36) * 1.55 * ((1.9 if '/' in it['_hand'] else 1.45) if it['_hand'] else 1))) + 16
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
CAM_BASE = 'wp-092'
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
            'style': "the teacher reads it herself (Reading Studio), topic-26 scripts (2026-10-21): math_patches/_ai_vis_t26.py is "
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
    L_, R_, Y_ = 40, 600, 112
    X = lambda v: L_ + 16 + (v - lo) / float(hi - lo) * (R_ - L_ - 32)
    INK, TEAL, BAND, FONT = SNL.INK, SNL.TEAL, SNL.BAND, SNL.FONT
    VB = '0 0 640 194'
    def txt(x, y, t, c, size=24, style=''):
        return ('<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="%d" font-weight="bold"%s>%s</text>'
                % (x, y, c, FONT, size, (' font-style="%s"' % style) if style else '', t))
    body = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.5"/>' % (L_ - 6, Y_, R_ + 6, Y_, INK) +
            '<path d="M %d %d l 12 -7 l 0 14 Z" fill="%s"/>' % (L_ - 10, Y_, INK) + '<path d="M %d %d l -12 -7 l 0 14 Z" fill="%s"/>' % (R_ + 10, Y_, INK))
    for t in ticks:
        v, lab = t if isinstance(t, tuple) else (t, ('−%s' % -t) if t < 0 else str(t))
        body += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2"/>' % (X(v), Y_ - 10, X(v), Y_ + 10, INK) + txt(X(v), Y_ + 44, lab, INK, 36)
    out = [('line', _svg(VB, body, title))]
    for key, marks in layers:
        b = ''
        for m in marks:
            if m[0] in ('pt', 'ink'):
                c = TEAL if m[0] == 'pt' else INK
                b += '<circle cx="%.1f" cy="%d" r="7" fill="%s"/>' % (X(m[1]), Y_, c) + txt(X(m[1]), Y_ - 18, m[2], c, 36, 'italic')
            elif m[0] == 'arrow':
                a, e = X(m[1]), X(m[2]); d = 1 if e > a else -1
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3"/>' % (a, Y_ - 58, e - 10 * d, Y_ - 58, TEAL) +
                      '<path d="M %.1f %d l %d -7 l 0 14 Z" fill="%s"/>' % (e, Y_ - 58, -14 * d, TEAL))
                if m[3]: b += txt((a + e) / 2, Y_ - 70, m[3], TEAL, 34)
            elif m[0] == 'shade':
                b += '<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (X(m[1]), Y_ - 7, X(m[2]) - X(m[1]), BAND, TEAL)
            elif m[0] == 'cross':
                x0 = X(m[1]); y0 = Y_ - 58
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (x0 - 14, y0 - 14, x0 + 14, y0 + 14, RED) +
                      '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (x0 + 14, y0 - 14, x0 - 14, y0 + 14, RED))
            elif m[0] == 'below':
                b += txt(X(m[1]), Y_ + 74, m[2], TEAL, 32)
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
    for a, b in [('\\blacklozenge', '◆'), ('\\times', '×'), ('\\cdot', '·'), ('\\ne', '≠'), ('\\le', '≤'), ('\\ge', '≥'), ('\\to', '→'),
                 ('\\quad', '    '), ('\\qquad', '      '), ('\\ ', ' '), ('\\,', ''), ('\\star', '⋆'), ('\\div', '÷'),
                 ('\\left', ''), ('\\right', ''), ('\\%', '%')]:
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


# ------------------------------------------------------------------------------------------- figures copied from topic 22 (V1)
# The word-problem pictures of her Hebrew course, built in layers at the spoken words (each layer a figure item drawn
# over its base; own=True: a layer finds its own base, so the written calculation lines can come in between):
#   TBL    the ratio table (wp 1300-1392: a column per quantity, row 1 the known pair, row 2 the new case and "?",
#          the times-k arrow across or down, else the diagonal of the triangle value) and the then-and-now table
#          (wp 1942-1990: "I stop and continue my table": a row for every time in the story)
#   UNITS  ratio units as boxes (3x and 10x as 3 and 10 equal boxes, the extra 7 bracketed) and the fraction bar for a
#          story (wp 2213-2267: "let's draw them as a rectangle", cut into 4, 3 kept)
#   ZL     a number line (the gap that turns around; the range of a price; where a mix must land)
ORANGE = '#c8641e'
_INK, _TEAL, _LIGHT = MV.INK, MV.TEAL, MV.LIGHT


def _tx(x, y, t, size=28, col=None, anchor='middle'):
    return MV._text(x, y, t, size, col or _INK, anchor)


def TBL(name, head, rowlab, layers, colw=200, labw=190, rowh=74, headh=56, col=0, w=None, side=0, size=34,
        title='Table'):
    """a table: head = the column names, rowlab = the row names ('' = no name column); layers = [(key, [mark, ...])]:
      ('c', r, c, text[, colour])      a cell value (r, c from 0; c counts the value columns only)
      ('q', r, c)                      a teal question mark
      ('cover', r, c, text)            the value found, over the question mark (teal)
      ('across', r, label)             an arrow across row r, from column 0 to column 1, with its label (x 7)
      ('down', c, r1, r2, label)       an arrow down beside column c (the first or the last), from row r1 to r2
      ('diag', (r1, c1), (r2, c2))     the diagonal of the triangle value
      ('box', r, c)                    a teal frame around a cell
    side = an empty margin left and right (for the down arrows)"""
    nr = len(rowlab); haslab = any(rowlab); lw = labw if haslab else 0
    x0 = 10 + side; y0 = 10
    xs = [x0 + lw + k * colw for k in range(len(head) + 1)]
    W = xs[-1] + 10 + side; H = y0 + headh + rowh * nr + 12
    top = lambda r: y0 + headh + rowh * r
    cy = lambda r: top(r) + rowh * .64
    cx = lambda c: (xs[c] + xs[c + 1]) / 2.0
    body = '<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (xs[0], y0, xs[-1] - xs[0], headh, _LIGHT)
    body += ''.join(_tx(cx(k), y0 + headh * .68, h, max(27, size - 2)) for k, h in enumerate(head))   # topic 25: the data sit in the head row
    left = x0 if haslab else xs[0]
    body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4"/>' % (xs[0], y0, xs[-1], y0, _INK)
    for r in range(nr + 1):
        y = top(r)
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s"/>' % (left if r else xs[0], y, xs[-1], y, _INK, 2.4 if r == 0 else 1.6)
    for x in xs:
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>' % (x, y0, x, top(nr), _INK)
    if haslab:
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>' % (x0, top(0), x0, top(nr), _INK)
        body += ''.join(_tx(x0 + lw / 2.0, cy(r), lab, max(26, size - 6)) for r, lab in enumerate(rowlab))
    out = [('line', MV._svg(W, H, body, title + ': ' + ', '.join(head)))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'c':
                b += _tx(cx(m[2]), cy(m[1]), m[3], size, m[4] if len(m) > 4 else _INK)
            elif k == 'q':
                b += _tx(cx(m[2]), cy(m[1]), '?', size + 2, _TEAL)
            elif k == 'cover':
                r, c = m[1], m[2]
                b += '<rect x="%.1f" y="%.1f" width="76" height="%.1f" fill="#ffffff"/>' % (cx(c) - 38, top(r) + 6, rowh - 12)
                b += _tx(cx(c), cy(r), m[3], size, _TEAL)
            elif k == 'across':
                r = m[1]; y = top(r) + rowh * .5
                xm = (cx(0) + cx(1)) / 2.0
                b += MV._arrow(cx(0) + 46, y + 6, cx(1) - 46, y + 6)
                b += '<rect x="%.1f" y="%.1f" width="66" height="27" rx="5" fill="#ffffff"/>' % (xm - 33, y - 25)
                b += _tx(xm, y - 3, m[2], 28, _TEAL)
            elif k == 'down':
                c, r1, r2 = m[1], m[2], m[3]
                y1, y2 = top(r1) + rowh * .32, top(r2) + rowh * .68
                if c == 0:
                    x = xs[0] - 20 - (lw if haslab else 0)
                    b += MV._arrow(x, y1, x, y2) + _tx(x - 10, (y1 + y2) / 2.0 + 10, m[4], 30, _TEAL, 'end')
                else:
                    x = xs[-1] + 20
                    b += MV._arrow(x, y1, x, y2) + _tx(x + 10, (y1 + y2) / 2.0 + 10, m[4], 30, _TEAL, 'start')
            elif k == 'diag':
                (r1, c1), (r2, c2) = m[1], m[2]
                x1, ya, x2, yb = cx(c1), top(r1) + rowh * .5, cx(c2), top(r2) + rowh * .5
                b += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3.2" stroke-linecap="round"/>'
                      % (x1 + (x2 - x1) * .22, ya + (yb - ya) * .22, x1 + (x2 - x1) * .78, ya + (yb - ya) * .78, _TEAL))
            elif k == 'box':
                r, c = m[1], m[2]
                b += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="none" stroke="%s" stroke-width="3"/>'
                      % (xs[c] + 5, top(r) + 5, colw - 10, rowh - 10, _TEAL))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def UNITS(name, rows, layers, unit=46, boxh=44, labw=150, gap=58, col=0, w=None, title='Ratio units', extra=0):
    """rows of equal boxes = ratio units: rows = [(label, number of boxes)]; layers = [(key, [mark, ...])]:
      ('fill', r, i0, i1[, colour])    tint boxes i0 .. i1-1 of row r (teal; 'orange')
      ('br', r, i0, i1, text[, 'up'])  a bracket under (or over) boxes i0 .. i1-1, with its text
      ('in', r, i, text)               a value inside box i
      ('right', r, text)               a value after the row
      ('tick', r, i, text)             a clock time over the edge before box i (a timeline)"""
    n = max(c for _, c in rows); x0 = 10 + labw; y0 = 46
    W = x0 + n * unit + 20 + extra; H = y0 + len(rows) * (boxh + gap) + 6
    rt = lambda r: y0 + r * (boxh + gap)
    bx = lambda i: x0 + i * unit
    body = ''
    for r, (lab, c) in enumerate(rows):
        body += _tx(x0 - 14, rt(r) + boxh * .7, lab, 30, _INK, 'end')
        body += ''.join('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" stroke-width="2.2"/>'
                        % (bx(i), rt(r), unit, boxh, _INK) for i in range(c))
    out = [('line', MV._svg(W, H, body, title))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'fill':
                r, i0, i1 = m[1], m[2], m[3]
                f = {'orange': '#fbe3cf', 'blue': '#dde6f3', 'grey': '#e2e2e2', 'yellow': '#fbf0c4'}.get(m[4] if len(m) > 4 else '', MV.BAND)
                b += ''.join('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="2.2"/>'
                             % (bx(i), rt(r), unit, boxh, f, _INK) for i in range(i0, i1))
            elif k == 'br':
                r, i0, i1, t = m[1], m[2], m[3], m[4]
                up = len(m) > 5 and m[5] == 'up'
                y = rt(r) - 8 if up else rt(r) + boxh + 8; d = -10 if up else 10
                xa, xb = bx(i0) + 3, bx(i1) - 3
                b += ('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="%s" stroke-width="2.6"/>'
                      % (xa, y, xa, y + d, xb, y + d, xb, y, _TEAL))
                b += _tx((xa + xb) / 2.0, y + d + (-8 if up else 30), t, 29, _TEAL)
            elif k == 'in':
                r, i, t = m[1], m[2], m[3]
                b += _tx(bx(i) + unit / 2.0, rt(r) + boxh * .7, t, 27, _TEAL)
            elif k == 'right':
                r, t = m[1], m[2]
                c = rows[r][1]
                b += _tx(bx(c) + 14, rt(r) + boxh * .7, t, 28, _TEAL, 'start')
            elif k == 'tick':                    # 2026-10-21 a clock time above the edge before box i (a timeline)
                r, i, t = m[1], m[2], m[3]
                b += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"/>' % (bx(i), rt(r) - 10, bx(i), rt(r) + boxh, _INK)
                      + _tx(bx(i), rt(r) - 16, t, 26, _INK))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def OWN(d, name):
    """a ZL number line whose layers find their own base (written lines may come in between)"""
    for it in d.values():
        if it.get('over'): it['of'] = name
        else: it['fig'] = name
    return d



CARRY26 = {}      # vid -> carry-over ("So far") boxes, _method_visuals.carry format
SPLITS = []       # lessons split into parts (not on camera)


# ------------------------------------------------------------------------------------------- topic-25 figures (V1)
# The pictures of her Hebrew topic-25 lessons, built in layers at the spoken words (each layer a figure item drawn over
# its base; own=True: a layer finds its own base, so the written calculation lines can come in between):
#   TOWERS  the cube towers (wp 5211-5235: «נבנה מגדלי קוביות בגבהים לפי המספרים... לפני שאנחנו מתחילים בואו נתחום רגע
#           את הממוצע... נעביר קוביות מהמגדלים הגבוהים למגדלים הנמוכים... כל המגדלים באותו גובה»): the towers, the two
#           limits (the tallest and the shortest tower), the blocks above the average (orange) and the empty places below
#           it (dashed), then the blocks moved: every tower at the average.
#   SAW     the seesaw in its exam form (wp 5750-5782: «אנחנו מציירים ציר... מעל הציר... את הציונים... מתחת... את המשקל...
#           נחלק אותו ל-5 יחידות מרחק»): the axis, the values above the ends, the weights below, the gap cut into equal
#           units, the pivot (the average) nearer the heavy side, the two distances.
_ORF2 = '#fbd9b9'
LIGHTH = MV.LIGHT


def TOWERS(name, hs, layers, cube=34, gapx=34, col=0, w=None, title='Towers of blocks'):
    """towers of cubes, heights hs (left to right), the value under each tower. layers = [(key, [mark, ...])]:
      ('lim', level, text)     a red dashed line at this height across the towers, its text at the right
      ('lvl', level, text)     a teal dashed line at this height (the average), its text at the right
      ('extra', level)         the cubes above `level` tinted orange (the blocks that will move)
      ('gap', level)           dashed empty places from each short tower up to `level`
      ('move', level)          the blocks moved: the orange cubes gone, the empty places filled teal"""
    n = len(hs); top = max(hs); x0 = 20; y0 = 26
    W = x0 + n * (cube + gapx) + 190; H = y0 + top * cube + 52
    X = lambda i: x0 + gapx / 2.0 + i * (cube + gapx)
    Y = lambda k: y0 + (top - k) * cube          # the top edge of cube number k (1 = the bottom cube)
    base = Y(0)
    def sq(i, k, fill, stroke=_INK, dash=''):
        return ('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="2"%s/>'
                % (X(i), Y(k), cube, cube, fill, stroke, (' stroke-dasharray="%s"' % dash) if dash else ''))
    body = '<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.6"/>' % (x0, base, X(n - 1) + cube + gapx / 2.0, base, _INK)
    for i, h in enumerate(hs):
        body += ''.join(sq(i, k, LIGHTH) for k in range(1, h + 1))
        body += _tx(X(i) + cube / 2.0, base + 34, str(h), 28, _INK)
    out = [('line', MV._svg(W, H, body, '%s: %s' % (title, ', '.join(str(h) for h in hs))))]
    xr = X(n - 1) + cube + gapx / 2.0
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k in ('lim', 'lvl'):
                y = Y(m[1]); c = RED if k == 'lim' else _TEAL
                b += ('<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3" stroke-dasharray="9 6"/>'
                      % (x0, y, xr, y, c) + _tx(xr + 10, y + 9, m[2], 26, c, 'start'))
            elif k == 'extra':
                for i, h in enumerate(hs):
                    b += ''.join(sq(i, kk, _ORF2) for kk in range(m[1] + 1, h + 1))
            elif k == 'gap':
                for i, h in enumerate(hs):
                    b += ''.join(sq(i, kk, 'none', _TEAL, '6 4') for kk in range(h + 1, m[1] + 1))
            elif k == 'move':
                for i, h in enumerate(hs):
                    b += ''.join('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="#ffffff"/>' % (X(i) - 2, Y(kk) - 2, cube + 4, cube + 4)
                                 for kk in range(m[1] + 1, h + 1))
                    b += ''.join(sq(i, kk, MV.BAND, _TEAL) for kk in range(h + 1, m[1] + 1))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def SAW(name, v1, v2, layers, col=0, w=None, title='The seesaw'):
    """the weighted-average axis (exam form): v1 left, v2 right (labels). layers = [(key, [mark, ...])]:
      ('vals',)                the two values above the ends
      ('wts', t1, t2)          the weights below the ends (teal)
      ('mid', text)            a dashed tick at the middle of the axis with its text above (the plain middle)
      ('units', n)             the gap cut into n equal units (ticks)
      ('pivot', k, n, text)    the pivot k units of n from the left end, its value under it
      ('dl', k, n, text)       the distance from the left end to the pivot, written above the axis
      ('dr', k, n, text)       the distance from the pivot to the right end, written above the axis
      ('heavy', side)          a thick teal ring around the heavy end's weight (0 left, 1 right)"""
    L_, R_, Y_ = 70, 570, 112; W, H = 640, 262
    X = lambda k, n: L_ + (R_ - L_) * k / float(n)
    body = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>' % (L_, Y_, R_, Y_, _INK) +
            ''.join('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (x, Y_ - 13, x, Y_ + 13, _INK) for x in (L_, R_)))
    out = [('line', MV._svg(W, H, body, '%s: %s and %s' % (title, v1, v2)))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'vals':
                b += _tx(L_, Y_ - 54, v1, 46) + _tx(R_, Y_ - 54, v2, 46)
            elif k == 'wts':
                b += _tx(L_, Y_ + 62, m[1], 40, _TEAL) + _tx(R_, Y_ + 62, m[2], 40, _TEAL)
            elif k == 'mid':
                x = (L_ + R_) / 2.0
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.4" stroke-dasharray="6 5"/>' % (x, Y_ - 52, x, Y_ + 14, ORANGE)
                      + _tx(x, Y_ - 60, m[1], 34, ORANGE))
            elif k == 'units':
                b += ''.join('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.4"/>' % (X(j, m[1]), Y_ - 11, X(j, m[1]), Y_ + 11, _TEAL)
                             for j in range(1, m[1]))
            elif k == 'pivot':
                x = X(m[1], m[2])
                b += ('<path d="M %.1f %d L %.1f %d L %.1f %d Z" fill="%s"/>' % (x, Y_ + 4, x - 20, Y_ + 40, x + 20, Y_ + 40, _TEAL)
                      + _tx(x, Y_ + 84, m[3], 44, _TEAL))
            elif k in ('dl', 'dr'):
                a, e = (L_, X(m[1], m[2])) if k == 'dl' else (X(m[1], m[2]), R_)
                b += ('<path d="M %.1f %d L %.1f %d L %.1f %d L %.1f %d" fill="none" stroke="%s" stroke-width="2"/>'
                      % (a + 4, Y_ - 14, a + 4, Y_ - 22, e - 4, Y_ - 22, e - 4, Y_ - 14, _TEAL)
                      + _tx((a + e) / 2.0, Y_ - 30, m[3], 32, _TEAL))
            elif k == 'heavy':
                x = L_ if m[1] == 0 else R_
                b += '<rect x="%d" y="%d" width="%d" height="52" rx="10" fill="none" stroke="%s" stroke-width="3.5"/>' % (x - 48, Y_ + 26, 96, _TEAL)
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)



# ------------------------------------------------------------------------------------------- topic-26 figures (V1)
# TRI26  the formula triangle (wp 5945-5962: «משולש ההספק... אני מסתיר אותו ומבצע כפל או חילוק בהתאם למה שנשאר»): the
#        triangle, the three names (work on top, rate and time at the bottom), then "cover" one name at a time (a teal
#        card over it; the card of the previous cover is lifted again in the same layer).
# VT     the V method (wp 6285-6341), _method_visuals.VTABLE: the empty team | work | time table, row 1, row 2, the V (or
#        the upside-down V when the work is asked), the rule "multiply the V, divide by the other two".
def TRI26(name, top='Work', left='Rate', right='Time', col=0, w=None, title='The formula triangle'):
    W, H = 360, 250
    pos = {'top': (180, 112, top, 30), 'left': (120, 200, left, 28), 'right': (240, 200, right, 28)}
    body = ('<path d="M 180 14 L 340 230 L 20 230 Z" fill="%s" stroke="%s" stroke-width="2.6"/>' % (_LIGHT, _INK) +
            '<line x1="80" y1="140" x2="280" y2="140" stroke="%s" stroke-width="2.4"/>' % _INK +
            '<line x1="180" y1="140" x2="180" y2="230" stroke="%s" stroke-width="2.4"/>' % _INK)
    out = [('line', MV._svg(W, H, body, title))]
    word = lambda k: _tx(pos[k][0], pos[k][1], pos[k][2], pos[k][3], _INK)
    out.append(('vals', MV._svg(W, H, ''.join(word(k) for k in ('top', 'left', 'right')), '%s = %s × %s' % (top, left, right))))
    def card(k):
        x, y, t, s = pos[k]
        return ('<rect x="%.1f" y="%.1f" width="96" height="44" rx="8" fill="%s" stroke="%s" stroke-width="2.4"/>'
                % (x - 48, y - 32, _TEAL, _TEAL) + _tx(x, y, '?', 32, '#ffffff'))
    def lift(k):
        x, y, t, s = pos[k]
        return ('<rect x="%.1f" y="%.1f" width="104" height="52" fill="%s"/>' % (x - 52, y - 36, _LIGHT)) + word(k)
    prev = None
    for k in ('top', 'right', 'left'):
        b = (lift(prev) if prev else '') + card(k)
        out.append(('cover_' + k, MV._svg(W, H, b, 'cover the %s' % pos[k][2].lower())))
        prev = k
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def VT(name, given, asked, unknown='time', col=0, w=None):
    """the V method table (own=True: the written calculation lines can come between its layers)"""
    return MV.items(_layers, name, MV.VTABLE(given, asked, unknown), w=w, col=col, own=True)


# =================================================================================================================
# THE SCRIPTS (topic-26 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-26-AI-scripts-review.md.
# Study plan before topic 26 (src/lib/planData.ts ORDER): 1, 30, 2, 4, 31, 6, 8, 32, 9, 10, 33, 51, (39, 42), 21, 3,
# (43), 22, (41), 5, 7, (44), 23, 11, 24, (49), 12, (45), 25, (40), 34, 13, 52 (charts lessons). So fractions and the
# common denominator (2, 3), equations (6, 7), the method names and plugging in (51), the ratio table, the triangle
# value, inverse proportion and "give it to the little guy" (22), percent multipliers (23) and the weighted average with
# the seesaw (25) are REMINDERS. Motion (27) comes LATER, so it is only named, never used.
# New here: the formula and the triangle, a rate is per one unit, matching units, direct and inverse (time / rate /
# work fixed), two changes multiply (same way as is, opposite way flipped), a rate in percent; adding rates (never the
# times), a worker against = minus, one job = 1, reading a combined rate, equal times, choosing a job size, the range
# check, the two-worker shortcut; team questions (spot them, the team's rate, the table, ratios, the V method, the
# upside-down V, ratios or V); worker-hours (one worker alone, splitting, stages, joining in the middle); and, in the
# questions, the clock time, the net rate and catching up, the average rate, the merged worker, who is the team,
# compare by factors in general and its limit.
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ wp-092 (camera lesson)
# Hebrew (wp 5923-6110): rate x time = work, "what I manage to do in one unit of time"; three quantities, two given, find
# the third; the triangle (cover the one you want); 8 in 2 minutes is "4 per minute", not 4 ("4 is nobody's rate"); work
# = everything we did, rate = what we do in one unit of time; her sample question (our g093); direct or inverse (time
# fixed, rate fixed, work fixed) with numbers. English (camera lesson, 2-3 examples per idea, numbers differ from the
# Hebrew and from the questions): the baker 6 x 4 = 24; the triangle with its three covers; the pump 150 / 30; the
# printer 48 / 6; 45 bottles in 5 minutes = 9 PER MINUTE; matching units (x 60, / 60; 4 a minute for 2 hours, the trap
# 8); the painter: time fixed, rate fixed (direct), work fixed (inverse; rate x time stays 12); R37: the core methods of
# the questions - two changes multiply (x2 and x4 = x8, not x6; checked), one change the opposite way (flipped), a rate
# in percent (+25% = x5/4, the time x4/5: 40 -> 32, the trap 30). Real exam: 2020_autumn_q1_10, 2024_spring_q2_02,
# 2023_winter_q1_16 (a rate change), 2021_autumn_q1_06, 2023_spring_q1_03 (units). NEW (all).
c_f1 = I('c_f1', 'Rate $\\times$ time $=$ work', size=46)
c_f2 = IH('c_f2', '$6$ cakes an hour, $\\ 4$ hours', size=36)
c_f3 = IH('c_f3', '$6\\times4=24$ cakes', size=36)
c_f4 = I('c_f4', 'Two are given: $\\ $we find the third', size=36)
c_tr = TRI26('c_tr', w=540)
c_t1 = IH('c_t1', 'work $=$ rate $\\times$ time', size=36, col=1)
c_t2 = IH('c_t2', 'time $=$ work $\\div$ rate', size=36, col=1)
c_t3 = IH('c_t3', 'rate $=$ work $\\div$ time', size=36, col=1)
c_e1 = I('c_e1', 'A pump: $\\ 30$ liters a minute. $\\ 150$ liters?', size=36)
c_e2 = IH('c_e2', 'time $=$ work $\\div$ rate', size=34)
c_e3 = IH('c_e3', '$150\\div30=5$ minutes', size=36)
c_e4 = I('c_e4', 'A printer: $\\ 48$ pages in $6$ minutes', size=36)
c_e5 = IH('c_e5', 'rate $=$ work $\\div$ time', size=34)
c_e6 = IH('c_e6', '$48\\div6=8$ pages a minute', size=36)
c_r0 = I('c_r0', '$45$ bottles in $5$ minutes', size=40)
c_r1 = IH('c_r1', 'work: $\\ 45$ bottles', size=36)
c_r2 = IH('c_r2', 'time: $\\ 5$ minutes', size=36)
c_r3 = IH('c_r3', 'rate: $\\ 45\\div5=9$', size=36)
c_r4 = I('c_r4', '$9$ bottles PER MINUTE', size=40)
c_r5 = IH('c_r5', '$\\frac{45}{5}=\\frac{9}{1}$', size=40, col=1)
c_r6 = I('c_r6', 'A rate always says: $\\ $per what?', size=34, col=1)
_wp092 = [
    S('Work, Rate and Time',
      L("Welcome back, and now a new topic, work and rate."),
      L("Work questions come up in almost every exam. Workers, machines, pipes and printers all get a job done over "
        "time. And one simple formula is behind all of them.")),
    S('The formula',
      L("Here it is. Rate times time is equal to work.", show(c_f1, 'Rate times time is equal to work')),
      L("The rate is what we do in one unit of time. For example, what we do in one hour."),
      L("The time is how long we work. And the work is everything we get done."),
      L("Let's see it in numbers. A baker makes six cakes an hour, and she works for four hours.",
        show(c_f2, 'A baker makes six cakes an hour')),
      L("So her rate is six cakes an hour, and the time is four hours. Six times four is twenty-four. So her work is "
        "twenty-four cakes.", show(c_f3, 'Six times four is twenty-four')),
      L("So there are three quantities, the rate, the time and the work. The question gives us two of them, and we "
        "find the third.", show(c_f4, 'The question gives us two of them'))),
    S('The triangle',
      L("If you're not sure when to multiply and when to divide, use the formula triangle.",
        show(c_tr['line'], 'use the formula triangle')),
      L("The work goes on top. The rate and the time go at the bottom, side by side.",
        show(c_tr['vals'], 'The work goes on top')),
      L("Now we cover the one we want. What's left tells us what to do."),
      L("Cover the work. The rate and the time are left, side by side. So the work is the rate times the time.",
        show(c_tr['cover_top'], 'Cover the work'), show(c_t1, 'So the work is the rate times')),
      L("Cover the time. The work is left, over the rate. So the time is the work divided by the rate.",
        show(c_tr['cover_right'], 'Cover the time'), show(c_t2, 'So the time is the work divided')),
      L("And cover the rate. The work is left, over the time. So the rate is the work divided by the time.",
        show(c_tr['cover_left'], 'And cover the rate'), show(c_t3, 'So the rate is the work divided'))),
    S('Find the time, find the rate',
      L("Let's use it. A pump moves thirty liters a minute. How long does it take to move a hundred fifty liters?",
        show(c_e1, 'A pump moves thirty liters')),
      L("They ask for the time. So we cover the time, and the time is the work divided by the rate.",
        show(c_e2, 'the time is the work divided by the rate')),
      L("A hundred fifty divided by thirty is five, because thirty times five is a hundred fifty. So it takes five "
        "minutes.", show(c_e3, 'A hundred fifty divided by thirty')),
      L("Now the other way. A printer prints forty-eight pages in six minutes. What is its rate?",
        show(c_e4, 'A printer prints forty-eight pages')),
      L("We cover the rate. The rate is the work divided by the time.", show(c_e5, 'The rate is the work divided')),
      L("Forty-eight divided by six is eight. So the printer prints eight pages a minute.",
        show(c_e6, 'Forty-eight divided by six'))),
    S('A rate is per one unit',
      L("Now careful here, because a lot of students mix up the work and the rate."),
      L("A machine fills forty-five bottles in five minutes. What is the work? Forty-five bottles. That's everything it "
        "did.", show(c_r0, 'A machine fills forty-five bottles'), show(c_r1, 'Forty-five bottles. That')),
      L("What is the time? Five minutes.", show(c_r2, 'Five minutes.')),
      L("And the rate is the work divided by the time. Forty-five divided by five is nine.",
        show(c_r3, 'Forty-five divided by five')),
      L("But the rate isn't just nine. It's nine bottles per minute.", show(c_r4, "It's nine bottles per minute")),
      L("Nine bottles is just an amount. Nine bottles per minute is a rate. So a rate always says per what.",
        show(c_r6, 'So a rate always says per what')),
      L("A rate is really a fraction, the work over the time. Forty-five bottles in five minutes is the same rate as "
        "nine bottles in one minute.", show(c_r5, 'A rate is really a fraction')),
      L("Both fractions say the same thing. So we can write a rate either way, whichever is easier.")),
]
c_u1 = IH('c_u1', '$1$ hour $=60$ minutes', size=36)
c_u2 = IH('c_u2', '$3$ hours $=3\\times60=180$ minutes', size=36)
c_u3 = IH('c_u3', '$30$ minutes $=\\frac{30}{60}=\\frac{1}{2}$ hour', size=36)
c_u4 = IH('c_u4', '$20$ minutes $=\\frac{20}{60}=\\frac{1}{3}$ hour', size=36)
c_u5 = I('c_u5', '$4$ parts a minute, $\\ $for $2$ hours', size=36, col=1)
c_u6 = IH('c_u6', '$2$ hours $=120$ minutes', size=34, col=1)
c_u7 = IH('c_u7', '$4\\times120=480$ parts', size=34, col=1)
c_u8 = IH('c_u8', '$4\\times2=8$: $\\ $the trap', size=34, col=1)
c_d0 = I('c_d0', 'The time is fixed: $\\ 5$ hours', size=36)
c_d1 = IH('c_d1', '$3$ walls an hour: $\\ 3\\times5=15$ walls', size=36)
c_d2 = IH('c_d2', '$6$ walls an hour: $\\ 6\\times5=30$ walls', size=36)
c_d3 = I('c_d3', 'rate $\\times2$, $\\ $work $\\times2$: $\\ $the same way', size=36)
c_d4 = I('c_d4', 'The rate is fixed: $\\ 3$ walls an hour', size=36)
c_d5 = IH('c_d5', '$4$ hours: $\\ 3\\times4=12$ walls', size=36)
c_d6 = IH('c_d6', '$2$ hours: $\\ 3\\times2=6$ walls', size=36)
c_d7 = I('c_d7', 'time $\\times\\frac{1}{2}$, $\\ $work $\\times\\frac{1}{2}$: $\\ $the same way', size=36)
c_i0 = I('c_i0', 'The work is fixed: $\\ 12$ walls', size=36)
c_i1 = IH('c_i1', '$3$ walls an hour: $\\ 12\\div3=4$ hours', size=36)
c_i2 = IH('c_i2', '$6$ walls an hour: $\\ 12\\div6=2$ hours', size=36)
c_i3 = I('c_i3', 'rate $\\times2$, $\\ $time $\\times\\frac{1}{2}$: $\\ $opposite ways', size=36)
c_i4 = IH('c_i4', '$3\\times4=12$', size=36, col=1)
c_i4b = IH('c_i4b', '$6\\times2=12$', size=36, col=1)
c_i5 = IH('c_i5', 'rate $\\times3$, $\\ $time $\\times\\frac{1}{3}$', size=36, col=1)
c_m0 = I('c_m0', '$10$ pages a minute, $\\ 3$ minutes', size=36)
c_m1 = IH('c_m1', '$10\\times3=30$ pages', size=36)
c_m2 = I('c_m2', 'rate $\\times2$, $\\ $time $\\times4$', size=36)
c_m3 = IH('c_m3', 'work $\\times2\\times4=\\times8$', size=36)
c_m4 = IH('c_m4', '$20$ pages a minute, $\\ 12$ minutes', size=34, col=1)
c_m5 = IH('c_m5', '$20\\times12=240$', size=34, col=1)
c_m6 = IH('c_m6', '$30\\times8=240$', size=34, col=1)
c_m7 = IH('c_m7', '$2+4=6$: $\\ $the trap', size=34, col=1)
c_o0 = I('c_o0', '$10$ hours. $\\ $The job $\\times3$, $\\ $the rate $\\times2$', size=36)
c_o1 = IH('c_o1', 'job $\\times3$: $\\ $the same way, $\\ 10\\times3=30$', size=36)
c_o2 = IH('c_o2', 'rate $\\times2$: $\\ $opposite, $\\ 30\\div2=15$ hours', size=36)
c_o3 = I('c_o3', 'The same way: $\\ $as it is. $\\ $Opposite ways: $\\ $flip it.', size=36)
c_p0 = I('c_p0', '$40$ minutes. $\\ $The rate: $\\ 25\\%$ faster', size=36)
c_p1 = IH('c_p1', 'rate $\\times1.25=\\times\\frac{5}{4}$', size=36)
c_p2 = IH('c_p2', 'time $\\times\\frac{4}{5}$', size=36)
c_p3 = IH('c_p3', '$40\\div5=8$', size=36)
c_p4 = IH('c_p4', '$8\\times4=32$ minutes', size=36)
c_p5 = IH('c_p5', '$40-10=30$: $\\ $the trap', size=34)
c_s1 = I('c_s1', 'Rate $\\times$ time $=$ work: $\\ $cover the one you want', size=34)
c_s2 = I('c_s2', 'A rate is per one unit of time. $\\ $Match the units.', size=34)
c_s3 = I('c_s3', 'Time or rate fixed: $\\ $the other two, the same way', size=34)
c_s4 = I('c_s4', 'Work fixed: $\\ $rate and time, opposite ways', size=34)
c_s5 = I('c_s5', 'Two changes: $\\ $multiply. $\\ $Opposite ways: $\\ $flip it.', size=34)
_wp092 += [
    S('Matching units',
      L("A rate has a time unit, per minute or per hour. So before we calculate, the units must match."),
      L("One hour is sixty minutes. So from hours to minutes, we multiply by sixty.", show(c_u1, 'One hour is sixty minutes')),
      L("Three hours is three times sixty, a hundred eighty minutes.", show(c_u2, 'Three hours is three times sixty')),
      L("From minutes to hours, we divide by sixty. Thirty minutes is thirty over sixty, half an hour.",
        show(c_u3, 'Thirty minutes is thirty over sixty')),
      L("And twenty minutes is twenty over sixty, a third of an hour.", show(c_u4, 'twenty minutes is twenty over sixty')),
      L("Let's see why it matters. A machine makes four parts a minute. How many parts does it make in two hours?",
        show(c_u5, 'A machine makes four parts a minute')),
      L("The rate is per minute, so the time must be in minutes too. Two hours is a hundred twenty minutes.",
        show(c_u6, 'Two hours is a hundred twenty minutes')),
      L("Four times a hundred twenty is four hundred eighty parts.", show(c_u7, 'Four times a hundred twenty')),
      L("A lot of students write four times two, eight. That mixes minutes with hours. So we always match the units "
        "first.", show(c_u8, 'A lot of students write four times two'))),
    S('The time is fixed',
      L("Now let's see how the three quantities move together. This helps a lot in the questions."),
      L("First, when the time is fixed, the rate and the work move the same way.", show(c_d0, 'when the time is fixed')),
      L("A painter paints three walls an hour, for five hours. Three times five is fifteen walls.",
        show(c_d1, 'A painter paints three walls an hour')),
      L("Now she paints twice as fast, six walls an hour, in the same five hours. Six times five is thirty walls.",
        show(c_d2, 'Now she paints twice as fast')),
      L("So twice the rate gives twice the work. That's called direct. The two go up together, by the same factor.",
        show(c_d3, 'So twice the rate gives twice the work'))),
    S('The rate is fixed',
      L("Second, when the rate is fixed, the time and the work also move the same way.",
        show(c_d4, 'when the rate is fixed')),
      L("The same painter, three walls an hour. In four hours, three times four is twelve walls.",
        show(c_d5, 'In four hours, three times four')),
      L("In two hours, that's half the time, three times two is six walls. That's half the work.",
        show(c_d6, 'In two hours')),
      L("So half the time gives half the work. That's direct too.", show(c_d7, 'So half the time gives half the work'))),
    S('The work is fixed',
      L("Third, when the work is fixed, the rate and the time move opposite ways. This is where students slip.",
        show(c_i0, 'when the work is fixed')),
      L("She has twelve walls to paint. At three walls an hour, twelve divided by three is four hours.",
        show(c_i1, 'At three walls an hour')),
      L("At six walls an hour, twice as fast, twelve divided by six is two hours. That's half the time.",
        show(c_i2, 'At six walls an hour')),
      L("So twice the rate gives half the time. The same job, done faster, takes less time. That's called inverse.",
        show(c_i3, 'So twice the rate gives half the time')),
      L("Why opposite? Because the rate times the time must stay twelve. Three times four is twelve. And six times two "
        "is twelve too.", show(c_i4, 'Three times four is twelve'), show(c_i4b, 'And six times two')),
      L("So three times as fast takes a third of the time.", show(c_i5, 'three times as fast'))),
    S('Two changes',
      L("Now what if two things change at once? Then we multiply the factors, one after the other."),
      L("A printer prints ten pages a minute, for three minutes. Ten times three is thirty pages.",
        show(c_m0, 'A printer prints ten pages a minute'), show(c_m1, 'Ten times three is thirty')),
      L("Now it prints twice as fast, and for four times as long. What happens to the work?",
        show(c_m2, 'twice as fast, and for four times')),
      L("Twice the rate doubles the work. And four times the time multiplies it by four again. Two times four is "
        "eight. So the work is eight times as big.", show(c_m3, 'Two times four is eight')),
      L("Let's check it. Twice as fast is twenty pages a minute. Four times as long is twelve minutes.",
        show(c_m4, 'Twice as fast is twenty pages')),
      L("Twenty times twelve is two hundred forty. And thirty times eight is also two hundred forty.",
        show(c_m5, 'Twenty times twelve'), show(c_m6, 'thirty times eight')),
      L("A lot of students add the factors, two plus four, six. But each change multiplies what is already there. So "
        "we multiply.", show(c_m7, 'two plus four, six'))),
    S('One change goes the opposite way',
      L("Now one change that goes the opposite way. A team needs ten hours for a job. Now the job is three times as "
        "big, and the team works twice as fast.", show(c_o0, 'A team needs ten hours for a job')),
      L("A bigger job takes more time. That's the same way, so the time is times three. Ten times three is thirty.",
        show(c_o1, 'Ten times three is thirty')),
      L("A faster team takes less time. That's the opposite way, so we flip the factor. Twice as fast means half the "
        "time. Thirty divided by two is fifteen hours.", show(c_o2, 'Thirty divided by two is fifteen')),
      L("So for each change, ask one question. Does my answer grow, or shrink? The same way, we multiply as it is. The "
        "opposite way, we flip it.", show(c_o3, 'The same way, we multiply as it is'))),
    S('A rate in percent',
      L("On the exam, a change in the rate often comes as a percent. Remember, a percent change is one multiplier."),
      L("A machine needs forty minutes for a job. Now it works twenty-five percent faster. How long does the job take "
        "now?", show(c_p0, 'A machine needs forty minutes')),
      L("Twenty-five percent faster is times one point two five. And one point two five is five quarters.",
        show(c_p1, 'times one point two five')),
      L("The job is the same, so the time goes the opposite way. We flip the factor. Five quarters becomes four "
        "fifths.", show(c_p2, 'Five quarters becomes four fifths')),
      L("Forty times four fifths. Forty divided by five is eight. Then eight times four is thirty-two minutes.",
        show(c_p3, 'Forty divided by five'), show(c_p4, 'eight times four')),
      L("Careful, the time doesn't drop by twenty-five percent. Forty minus a quarter of forty is thirty. That's the "
        "trap.", show(c_p5, 'Forty minus a quarter of forty'))),
    S('Recap',
      L("So let's sum it up. Rate times time is equal to work. In the triangle, cover the one you want.",
        show(c_s1, 'Rate times time is equal to work')),
      L("A rate is per one unit of time, and the units must match.", show(c_s2, 'A rate is per one unit')),
      L("When the time or the rate is fixed, the other two move the same way.", show(c_s3, 'When the time or the rate')),
      L("When the work is fixed, the rate and the time move opposite ways.", show(c_s4, 'When the work is fixed')),
      L("And with two changes, we multiply the factors. A factor that goes the opposite way gets flipped.",
        show(c_s5, 'And with two changes')),
      L("Take a moment to memorize this. Now try the first question, and I'll see you in the next video.")),
]
video('wp-092', 'lesson', slides=_wp092)
CAMERA_SPLIT = ('wp-092', 'Work, Rate and Time', [
    (1, None),
    (5, "Let's continue with work and rate, and look at the units first."),
    (9, "Let's continue, and see what happens when two things change.")])

# ------------------------------------------------------------------------------------------------ g093 (the volunteer)
# Hebrew (wp 6008-6040, her sample question: x hot dogs in y minutes, rate x 2, 3y minutes): ratios ("from y to 3y is
# x 3, so the work x 3 too"; across or down, the same 6x), then the triangle value for "whoever finds ratios hard".
# English keeps both and adds the formula and plugging in numbers (letter answers; R15). First question of the topic:
# two changes multiply (camera lesson part 3) applied slowly, "like in the lesson". Trap at its step: 8x adds 3 + 5.
g93t = TBL('g93t', ['flyers', 'minutes'], ['now', 'rate × 3', 'then'], [
    ('r1', [('c', 0, 0, 'x'), ('c', 0, 1, 'y')]),
    ('r2', [('c', 1, 0, '3x'), ('c', 1, 1, 'y')]),
    ('r3', [('c', 2, 1, '5y'), ('q', 2, 0)]),
    ('a5', [('down', 1, 1, 2, '×5')]),
    ('ans', [('cover', 2, 0, '15x'), ('down', 0, 1, 2, '×5')])], colw=150, labw=150, rowh=62, side=80, w=560, col=1)
g93a = IH('g93a', '$x\\times3=3x$', size=30)
g93b = IH('g93b', '$3x\\times5=15x$', size=30)
g93c = IH('g93c', '$3+5=8$: $\\ $the trap', size=30)
g93v = TBL('g93v', ['flyers', 'minutes'], ['', ''], [
    ('r1', [('c', 0, 0, '3x'), ('c', 0, 1, 'y')]), ('r2', [('q', 1, 0), ('c', 1, 1, '5y')]),
    ('dg', [('diag', (0, 0), (1, 1))])], colw=150, labw=0, rowh=62, w=330, col=1)
g93d = IH('g93d', '$?=\\frac{3x\\cdot5y}{y}$', size=30)
g93e = IH('g93e', '$=3x\\cdot5=15x$', size=30)
g93f = IH('g93f', 'rate $=\\frac{x}{y}$ a minute', size=30)
g93g = IH('g93g', 'new rate $=\\frac{3x}{y}$', size=30)
g93h = IH('g93h', 'work $=\\frac{3x}{y}\\cdot5y$', size=30)
g93i = IH('g93i', '$=3x\\cdot5=15x$', size=30)
g93j = IH('g93j', '$x=6$, $\\ y=2$: $\\ 6\\div2=3$ a minute', size=30)
g93k = IH('g93k', '$3\\times3=9$ a minute', size=30)
g93l = IH('g93l', '$5y=10$ minutes', size=30)
g93m = IH('g93m', '$9\\times10=90$ flyers', size=30)
g93n = IH('g93n', '(1) $\\ 8\\cdot6=48$, no', size=30, col=1)
g93o = IH('g93o', '(2) $\\ \\frac{5\\cdot6}{3}=10$, no', size=30, col=1)
g93p = IH('g93p', '(3) $\\ 15\\cdot6=90$', size=30, col=1)
g93q = IH('g93q', '(4) $\\ 3\\cdot6=18$, no', size=30, col=1)
video('solve-wp26-g093', 'solution', qid='wp26-g093', slides=[
    S('Method 1 · Understanding: ratios',
      L("A volunteer folds x flyers in y minutes at a constant rate, where x and y are positive. How many flyers will "
        "she fold in five y minutes, if her rate becomes three times as great?",
        pt('stem', 'A volunteer folds x flyers', 'hl', 10.0), voice='calm', pause=0.5),
      L("So they ask for the work, the number of flyers. And two things change, her rate and her time.",
        pt('stem: ask', 'So they ask for the work')),
      L("We'll solve it in four different ways. Let's start by understanding, with a ratio table, like in topic "
        "twenty-two. We take the two changes one at a time.", show(g93t['line'], 'with a ratio table')),
      L("Row one is what they give us. She folds x flyers in y minutes.", show(g93t['r1'], 'She folds x flyers')),
      L("First, her rate becomes three times as great. In the same y minutes, she folds three times as many flyers. "
        "So x times three, three x.", show(g93t['r2'], 'In the same y minutes'), show(g93a, 'So x times three')),
      L("Like in the lesson, the time is fixed, so the rate and the work go the same way."),
      L("Now the time changes from y to five y. That's times five.", show(g93t['r3'], 'from y to five y'),
        show(g93t['a5'], "That's times five")),
      L("Her new rate stays the same now. So the work goes the same way as the time, times five. Three x times five is "
        "fifteen x.", show(g93b, 'Three x times five'), show(g93t['ans'], 'fifteen x.')),
      L("Like in the lesson, two changes multiply. Three times five is fifteen."),
      L("Careful with eight x, choice number one. It adds three and five, instead of multiplying them.",
        show(g93c, 'It adds three and five'), mk('cross', 'choice 1', 'instead of multiplying them')),
      L("So she folds fifteen x flyers. That's choice number three.")),
    S('Method 2 · The math way: the triangle value',
      L("[pause] Now the math way, with the triangle value from topic twenty-two. We start again from the givens. With the "
        "new rate, she folds three x flyers in y minutes. And we ask about five y minutes.",
        show(g93v['line'], 'she folds three x flyers'), show(g93v['r1'], 'she folds three x flyers'),
        show(g93v['r2'], 'And we ask about five y')),
      L("Remember, we multiply along the diagonal, and divide by what's left. On top, five y times three x. At the bottom, y.",
        show(g93v['dg'], 'we multiply along the diagonal'), show(g93d, 'On top, five y times three x')),
      L("The y on top and the y at the bottom cancel. Three x times five is fifteen x.",
        show(g93e, 'Three x times five is fifteen x'))),
    S('Method 3 · The math way: the formula',
      L("[pause] Now the math way, with the formula from the lesson. The rate is the work divided by the time. She folds x "
        "flyers in y minutes, so her rate is x over y flyers a minute.", show(g93f, 'so her rate is x over y')),
      L("Three times as great is three x over y.", show(g93g, 'Three times as great is three x over y')),
      L("The work is the rate times the time. The new time is five y. So the work is three x over y, times five y.",
        show(g93h, 'So the work is three x over y')),
      L("The y's cancel again. Three x times five is fifteen x.", show(g93i, 'Three x times five'))),
    S('Method 4 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. It's a safety net when the answers have letters. We start again from the "
        "givens."),
      L("Let's say x is six flyers and y is two minutes. Both are allowed, and six divides easily by two. "
        "Six divided by two is three flyers a minute.", show(g93j, "Let's say x is six flyers")),
      L("Her rate becomes three times as great. Three times three is nine flyers a minute.",
        show(g93k, 'Three times three is nine')),
      L("The time is five y. Five times two is ten minutes.", show(g93l, 'Five times two is ten')),
      L("Nine flyers a minute for ten minutes. Nine times ten is ninety flyers. So the answer must be ninety when x is "
        "six.", show(g93m, 'Nine times ten is ninety')),
      L("Choice number one says eight x. Eight times six is forty-eight, not ninety. Out.",
        show(g93n, 'Eight times six'), mk('cross', 'choice 1', 'not ninety. Out')),
      L("Choice number two says five x over three. Five times six is thirty. Then thirty divided by three is ten. Out.",
        show(g93o, 'Five times six is thirty'), mk('cross', 'choice 2', 'divided by three is ten. Out')),
      L("Choice number three says fifteen x. Fifteen times six is ninety. That's our number.",
        show(g93p, 'Fifteen times six is ninety')),
      L("Choice number four says three x. Three times six is eighteen. Out.", show(g93q, 'Three times six is eighteen'),
        mk('cross', 'choice 4', 'is eighteen. Out')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t26-01 (the printer, +20%)
# No Hebrew (a September addition; real exams 2023_winter_q1_16, 2020_spring_q1_20). A rate in percent (camera lesson
# part 3: one multiplier, the work fixed, so the time goes the opposite way: flip it), applied slowly; percent
# multipliers are a reminder (topic 23). Trap at its step: 48 = 60 minus 20%. Method 2 plugs in a job size (R15: 300,
# because 60 divides it; no decimals).
q1a = IH('q1a', 'speed $\\times1.2=\\times\\frac{6}{5}$', size=30)
q1b = IH('q1b', 'time $\\times\\frac{5}{6}$', size=30)
q1c = IH('q1c', '$60\\div6=10$', size=30, col=1)
q1d = IH('q1d', '$10\\times5=50$ minutes', size=30, col=1)
q1e = IH('q1e', '$60-12=48$: $\\ $the trap', size=30, col=1)
q1f = IH('q1f', 'job: $\\ 300$ pages', size=30)
q1g = IH('q1g', '$300\\div60=5$ pages a minute', size=30)
q1h = IH('q1h', '$20\\%$ of $5$ is $1$: $\\ 5+1=6$ a minute', size=30)
q1i = IH('q1i', '$300\\div6=50$ minutes', size=30)
video('solve-q-r26-t26-01', 'solution', qid='q-r26-t26-01', slides=[
    S('Method 1 · Understanding: flip the factor',
      L("A printer finishes a job in sixty minutes. Its speed increases by twenty percent. How many minutes does the "
        "same job take now?", pt('stem', 'A printer finishes a job', 'hl', 7.0), voice='calm', pause=0.5),
      L("So the job stays the same, and only the speed changes. They ask for the new time.",
        pt('stem: ask', 'They ask for the new time')),
      L("We'll solve it in two different ways. First by understanding, with the factor, like in the lesson. Then by "
        "plugging in numbers."),
      L("A twenty percent rise is one multiplier. Twenty percent more is a hundred twenty percent, so times one point "
        "two. And one point two is six fifths.", show(q1a, 'so times one point two')),
      L("The job is the same, so the work is fixed. Like in the lesson, the speed and the time go opposite ways. So we "
        "flip the factor. Six fifths becomes five sixths.", show(q1b, 'Six fifths becomes five sixths')),
      L("Sixty times five sixths. Sixty divided by six is ten. Then ten times five is fifty minutes.",
        show(q1c, 'Sixty divided by six'), show(q1d, 'ten times five is fifty')),
      L("Does it make sense? Yes. Faster means less time, and fifty is less than sixty."),
      L("Careful with forty-eight, choice number one. Twenty percent of sixty is twelve. Then sixty minus twelve is "
        "forty-eight. But twenty percent faster doesn't mean twenty percent less time.",
        show(q1e, 'sixty minus twelve is'), mk('cross', 'choice 1', "doesn't mean twenty percent less time")),
      L("So the job takes fifty minutes now. That's choice number two.")),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. The job size isn't given, so we choose it."),
      L("Let's say the job is three hundred pages. We pick three hundred because sixty divides it.",
        show(q1f, "Let's say the job is three hundred pages")),
      L("Three hundred pages in sixty minutes. The rate is the work divided by the time. Three hundred divided by sixty "
        "is five pages a minute.", show(q1g, 'Three hundred divided by sixty')),
      L("The speed increases by twenty percent. Twenty percent of five is one. So the new speed is five plus one, six "
        "pages a minute.", show(q1h, 'Twenty percent of five is one')),
      L("The job is still three hundred pages. So the time is the work divided by the new rate. Three hundred divided "
        "by six is fifty minutes. The same answer.", show(q1i, 'Three hundred divided by six')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-094 (lesson: working together)
# Hebrew (wp 6111-6206): a combined rate = add the rates (3 + 2 = 5 exercises a minute); one works against = minus (5
# clean, 2 dirty = 3); her pump question (rates 1/6, 1/6, -1/9 -> 2/9 = "2 pools in 9 hours" -> one pool 4.5 h); her
# beer question (3 h and 2 h: "I can't add them, the times are different" -> 6 hours, 2 + 3 = 5 barrels in 6 hours ->
# one in 6/5 h). English (R37: the core methods of g095, g096, q-r26-t26-02, q-r26-t26-03, g103, g104 are taught here,
# 2-3 examples each, numbers differ from the Hebrew and the questions): add the rates (3 + 2, 8 + 12), never the times
# (3 h and 6 h is not 9), against = minus (5 - 2), one job = 1 (4 hours -> 1/4; check), reading a combined rate (1/4 +
# 1/12 = 1/3 -> one pool in 3 hours; 2/15 -> 7 1/2 hours); part 2: equal times (4 h and 6 h -> 12 h: 3 + 2 = 5 bags,
# one bag 2 2/5 h = 2 h 24 min), a job size (5 h and 20 h -> 20 units: 4 + 1 = 5 an hour, 4 hours), the range check
# (less than the fastest alone, more than half of it), the two-worker shortcut (24 / 10; equal workers half the time;
# only two workers). Real exam: 2019_spring_q1_08, 2022_autumn_q1_05, 2024_winter_q2_04, 2023_spring_q1_03. NEW (all).
t4a1 = IH('t4a1', 'Dan: $\\ 3$ a minute. $\\ $Noa: $\\ 2$ a minute.', size=36)
t4a2 = IH('t4a2', 'together: $\\ 3+2=5$ a minute', size=36)
t4a3 = I('t4a3', 'Together: $\\ $add the rates', size=38)
t4a4 = IH('t4a4', '$8+12=20$ liters a minute', size=36)
t4b1 = I('t4b1', 'Dan: $\\ 3$ hours. $\\ $Noa: $\\ 6$ hours.', size=36)
t4b2 = IH('t4b2', 'together: $\\ 3+6=9$ hours? $\\ $No', size=36)
t4b3 = I('t4b3', 'Add the rates, $\\ $never the times', size=38)
t4c1 = IH('t4c1', 'I wash $5$ plates a minute', size=36)
t4c2 = IH('t4c2', 'he makes $2$ plates dirty a minute', size=36)
t4c3 = IH('t4c3', '$5-2=3$ clean plates a minute', size=36)
t4c4 = I('t4c4', 'Working against: $\\ $a minus', size=38)
t4d1 = I('t4d1', 'One pool in $4$ hours', size=38)
t4d2 = IH('t4d2', 'rate $=\\frac{1}{4}$ of the pool an hour', size=36)
t4d3 = IH('t4d3', '$\\frac{1}{4}\\times4=1$ pool', size=36)
t4d4 = IH('t4d4', 'one job in $5$ hours: $\\ \\frac{1}{5}$ an hour', size=36)
t4e1 = I('t4e1', 'A: $\\ 4$ hours. $\\ $B: $\\ 12$ hours. $\\ $Together?', size=36)
t4e2 = IH('t4e2', '$\\frac{1}{4}+\\frac{1}{12}$', size=36)
t4e3 = IH('t4e3', '$=\\frac{3}{12}+\\frac{1}{12}=\\frac{4}{12}$', size=36)
t4e4 = IH('t4e4', '$=\\frac{1}{3}$', size=36)
t4e5 = IH('t4e5', '$1$ pool in $3$ hours', size=36, col=1)
t4e6 = IH('t4e6', '$\\frac{2}{15}$: $\\ 2$ pools in $15$ hours', size=34, col=1)
t4e7 = IH('t4e7', '$1$ pool: $\\ 15\\div2=7\\frac{1}{2}$ hours', size=34, col=1)
_wp094 = [
    S('Working Together',
      L("Now let's see what happens when workers work together."),
      L("Usually it's two workers, sometimes more. And usually each one has a different rate.")),
    S('Add the rates',
      L("When workers work together, they have one combined rate. Let's see it in numbers."),
      L("Dan solves three exercises a minute. Noa solves two exercises a minute.", show(t4a1, 'Dan solves three exercises')),
      L("Together they solve three plus two, five exercises a minute.", show(t4a2, 'Together they solve three plus two')),
      L("So to find a combined rate, we add the rates.", show(t4a3, 'we add the rates')),
      L("Another example. One pump fills eight liters a minute, and another pump fills twelve. Together, eight plus "
        "twelve is twenty liters a minute.", show(t4a4, 'Together, eight plus twelve'))),
    S('Never add the times',
      L("Now careful. We add the rates, never the times."),
      L("Dan finishes a job in three hours. Noa finishes the same job in six hours. Together, is it nine hours?",
        show(t4b1, 'Dan finishes a job in three hours')),
      L("No. Nine hours is more than Dan needs alone. With help, Dan finishes sooner, not later.", show(t4b2, 'No. Nine hours')),
      L("So the times don't add. Only the rates add. In a moment, we'll see how to get the rates from the times.",
        show(t4b3, 'Only the rates add'))),
    S('Working against',
      L("Sometimes one worker works against the others. Then his rate gets a minus."),
      L("I wash five plates a minute. My little brother makes two plates dirty every minute.",
        show(t4c1, 'I wash five plates a minute'), show(t4c2, 'My little brother makes two plates')),
      L("So each minute, only five minus two, three plates get clean.", show(t4c3, 'only five minus two')),
      L("A pipe that fills a tank and a drain that empties it work the same way. The drain gets a minus.",
        show(t4c4, 'The drain gets a minus'))),
    S('One job is one',
      L("Often the question doesn't say how big the job is. It only says how long the job takes."),
      L("Then we call the whole job one. For example, a pump fills one pool in four hours.", show(t4d1, 'a pump fills one pool')),
      L("The rate is the work divided by the time. So its rate is one over four, a quarter of the pool an hour.",
        show(t4d2, 'So its rate is one over four')),
      L("Let's check it. A quarter of the pool each hour, for four hours, is one whole pool.",
        show(t4d3, 'A quarter of the pool each hour')),
      L("In the same way, a job in five hours means a fifth of the job each hour.", show(t4d4, 'a job in five hours'))),
    S('Read the combined rate',
      L("Now let's add rates that are fractions. Pump A fills a pool in four hours. Pump B fills it in twelve hours. "
        "They work together.", show(t4e1, 'Pump A fills a pool in four hours')),
      L("Pump A's rate is a quarter of the pool an hour. Pump B's rate is a twelfth. So together it's a quarter plus a twelfth.",
        show(t4e2, 'So together')),
      L("We need a common denominator, twelve. A quarter is three twelfths. Three twelfths plus one twelfth is four "
        "twelfths.", show(t4e3, 'A quarter is three twelfths')),
      L("And four twelfths is a third.", show(t4e4, 'And four twelfths is a third')),
      L("What does a third mean? A rate is the work over the time. So a third means one pool in three hours.",
        show(t4e5, 'one pool in three hours')),
      L("Another one. A combined rate of two fifteenths means two pools in fifteen hours.",
        show(t4e6, 'two pools in fifteen hours')),
      L("So one pool takes half of that. Fifteen divided by two is seven and a half hours.",
        show(t4e7, 'Fifteen divided by two'))),
]
t4t = TBL('t4t', ['bags', 'hours'], ['Ella', 'Ella', 'Tom', 'Tom', 'together'], [
    ('r1', [('c', 0, 0, '1'), ('c', 0, 1, '4')]), ('r3', [('c', 2, 0, '1'), ('c', 2, 1, '6')]),
    ('h', [('c', 1, 1, '12'), ('c', 3, 1, '12')]),
    ('e', [('down', 1, 0, 1, '×3'), ('c', 1, 0, '3')]), ('t', [('down', 1, 2, 3, '×2'), ('c', 3, 0, '2')]),
    ('s', [('c', 4, 0, '5'), ('c', 4, 1, '12')])], colw=130, labw=150, rowh=58, side=70, w=580, col=0)
t4f1 = IH('t4f1', '$5$ bags in $12$ hours', size=34, col=1)
t4f2 = IH('t4f2', '$1$ bag: $\\ 12\\div5=2\\frac{2}{5}$ hours', size=34, col=1)
t4f3 = IH('t4f3', '$\\frac{1}{5}$ hour $=60\\div5=12$ minutes', size=34, col=1)
t4f4 = IH('t4f4', '$\\frac{2}{5}$ hour $=24$ minutes', size=34, col=1)
t4f5 = IH('t4f5', '$2$ hours and $24$ minutes', size=34, col=1)
t4g1 = I('t4g1', 'A: $\\ 5$ hours. $\\ $B: $\\ 20$ hours.', size=36)
t4g2 = IH('t4g2', 'the tank: $\\ 20$ units', size=36)
t4g3 = IH('t4g3', 'A: $\\ 20\\div5=4$ an hour', size=36)
t4g4 = IH('t4g4', 'B: $\\ 20\\div20=1$ an hour', size=36)
t4g5 = IH('t4g5', 'together: $\\ 4+1=5$ an hour', size=36)
t4g6 = IH('t4g6', '$20\\div5=4$ hours', size=36)
t4h1 = I('t4h1', 'Two workers helping: less time than the faster one alone', size=34)
t4h2 = I('t4h2', 'Different rates: more than half the faster one\'s time', size=34)
t4h3 = IH('t4h3', 'Ella and Tom: $\\ 4$ and $6$ hours', size=34)
t4h4 = IH('t4h4', 'less than $4$ hours', size=34)
t4h4b = IH('t4h4b', 'more than $4\\div2=2$ hours', size=34)
t4h5 = IH('t4h5', '$2$ hours $24$ minutes: $\\ $between them', size=34)
t4k1 = I('t4k1', 'Two workers: $\\ \\frac{a\\cdot b}{a+b}$', size=40)
t4k2 = IH('t4k2', '$\\frac{4\\cdot6}{4+6}=\\frac{24}{10}=2\\frac{2}{5}$ hours', size=36)
t4k3 = IH('t4k3', 'equal: $\\ \\frac{4\\cdot4}{4+4}=\\frac{16}{8}=2$ hours', size=36)
t4k4 = I('t4k4', 'Only for two workers', size=36)
t4s1 = I('t4s1', 'Together: $\\ $add the rates, $\\ $never the times', size=34)
t4s2 = I('t4s2', 'Working against: $\\ $a minus', size=34)
t4s3 = I('t4s3', 'One job in $4$ hours: $\\ \\frac{1}{4}$ of the job an hour', size=34)
t4s4 = I('t4s4', 'Or: $\\ $equal times, $\\ $or choose a job size', size=34)
t4s5 = I('t4s5', 'Two workers, different rates: between half the faster time and that full time', size=30)
_wp094 += [
    S('Equal times',
      L("There's another way, without adding fractions. Compare both workers over the same number of hours. "
        "Then add how much work they finish."),
      L("Ella fills one bag of leaves in four hours. Tom fills one bag in six hours.", show(t4t['line'], 'Ella fills one bag'),
        show(t4t['r1'], 'Ella fills one bag'), show(t4t['r3'], 'Tom fills one bag')),
      L("We can't add them yet, because the times are different. So we pick a time that works for both, twelve hours. "
        "Twelve divides by four and by six.", show(t4t['h'], 'twelve hours')),
      L("Four hours to twelve is times three. So in twelve hours, Ella fills three bags.", show(t4t['e'], 'Four hours to twelve')),
      L("Six hours to twelve is times two. So in twelve hours, Tom fills two bags.", show(t4t['t'], 'Six hours to twelve')),
      L("Now the times match. In the same twelve hours, together they fill three plus two, five bags.",
        show(t4t['s'], 'together they fill three plus two'), show(t4f1, 'five bags')),
      L("We add the bags, not the hours, because they both work during the same twelve hours."),
      L("They want one bag. Five bags to one bag is divided by five. So the time is divided by five too. Twelve divided "
        "by five is two and two fifths hours.", show(t4f2, 'Twelve divided by five')),
      L("A fifth of an hour is sixty divided by five, twelve minutes. So two fifths is twenty-four minutes.",
        show(t4f3, 'sixty divided by five'), show(t4f4, 'So two fifths')),
      L("So together they need two hours and twenty-four minutes.", show(t4f5, 'two hours and twenty-four'))),
    S('Choose a job size',
      L("We can also choose how big the job is. We pick a number that both times divide, so the rates are whole "
        "numbers."),
      L("Pipe A fills a tank in five hours. Pipe B fills it in twenty hours.", show(t4g1, 'Pipe A fills a tank in five')),
      L("Let's say the tank holds twenty units, because five and twenty both divide twenty.", show(t4g2, 'twenty units')),
      L("Pipe A fills twenty units in five hours. Twenty divided by five is four units an hour.",
        show(t4g3, 'Twenty divided by five is four')),
      L("Pipe B fills twenty units in twenty hours. That's one unit an hour.", show(t4g4, "That's one unit an hour")),
      L("Together, four plus one is five units an hour.", show(t4g5, 'four plus one is five')),
      L("Twenty units at five units an hour. Twenty divided by five is four hours.", show(t4g6, 'Twenty units at five')),
      L("It's just like plugging in numbers. The tank's real size doesn't matter, so we choose an easy one.")),
    S('Check the range first',
      L("Before we calculate, we can often rule out choices. Here's how."),
      L("Take two workers who both help with the same job. Together they finish sooner than the faster worker alone.",
        show(t4h1, 'Together they finish sooner')),
      L("Two workers as fast as the faster one would need half that time. If the other worker is slower, together "
        "they take more than that half. If their rates are equal, they take exactly half. This half-time limit is "
        "for two workers, not three or more.", show(t4h2, 'If the other worker is slower')),
      L("Ella needs four hours, and Tom needs six. So together, less than four hours.",
        show(t4h3, 'Ella needs four hours'), show(t4h4, 'So together, less than four hours')),
      L("And more than half of four, two hours. Our answer, two hours and twenty-four minutes, is between them.",
        show(t4h4b, 'And more than half of four'), show(t4h5, 'Our answer, two hours and twenty-four'))),
    S('A shortcut for two workers',
      L("And there's a short formula, only for two workers. We multiply the two times, and divide by their sum.",
        show(t4k1, 'We multiply the two times')),
      L("Ella and Tom, four and six hours. Four times six is twenty-four. Four plus six is ten. Twenty-four over ten is "
        "two and two fifths hours, the same answer.", show(t4k2, 'Twenty-four over ten is')),
      L("Why does it work? It comes from adding the two rates. We don't need to prove it here."),
      L("Two equal workers, four hours each? Four times four is sixteen. Then four plus four is eight. Sixteen over "
        "eight is two hours. Half the time, as we expect.", show(t4k3, 'Sixteen over')),
      L("Careful, the formula is only for two workers. With three workers, we add the rates.",
        show(t4k4, 'the formula is only for two workers'))),
    S('Recap',
      L("So let's sum it up. Working together, we add the rates, never the times.", show(t4s1, 'we add the rates, never')),
      L("A worker who works against the others gets a minus.", show(t4s2, 'gets a minus')),
      L("One job in four hours is a quarter of the job an hour.", show(t4s3, 'One job in four hours')),
      L("Or compare both workers over the same time. Another option is to choose an easy job size.",
        show(t4s4, 'compare both workers over the same time')),
      L("And for two workers with different positive rates, the time together is less than the faster one's time "
        "alone, but more than half of it.", show(t4s5, 'for two workers with different positive rates')),
      L("Take a moment to memorize this, and I'll see you in the next video.")),
]
video('wp-094', 'lesson', slides=_wp094)
SPLITS.append(('wp-094', 'Working Together', [
    (1, None),
    (6, "Let's continue with working together, and see more ways to find the time together.")]))

# ------------------------------------------------------------------------------------------------ g095 (the pond)
# Hebrew (wp 6139-6170, her pump question: 6 h, 6 h, minus 9 h, start 8:00): find the combined rate, the emptying pump
# gets a minus, "remember, a rate is work over time": 1/6, 1/6, -1/9 -> 2/9 = 2 pools in 9 hours, one pool: half the
# time, plus the start time. English keeps it (fractions, the clock time) and adds a job size of 60 (wp-094 part 2).
# First question with combined fractions: applied slowly, "like in the lesson". Trap at its step: 2:30 p.m. forgets
# the outlet (2/15 -> 7 1/2 hours).
g95a = IH('g95a', 'one hose: $\\ \\frac{1}{15}$ of the pond an hour', size=30)
g95b = IH('g95b', '$\\frac{1}{15}+\\frac{1}{15}$', size=30)
g95b2 = IH('g95b2', '$-\\frac{1}{20}$', size=30)
g95c = IH('g95c', '$\\frac{1}{15}=\\frac{4}{60}$', size=30, col=1)
g95c2 = IH('g95c2', '$\\frac{1}{20}=\\frac{3}{60}$', size=30, col=1)
g95d = IH('g95d', '$\\frac{4}{60}+\\frac{4}{60}-\\frac{3}{60}=\\frac{5}{60}$', size=30, col=1)
g95e = IH('g95e', '$\\frac{5}{60}=\\frac{1}{12}$', size=30)
g95f = IH('g95f', '$1$ pond in $12$ hours', size=30, col=1)
g95g = IH('g95g', '$7$ a.m. $+\\ 12$ hours $=7$ p.m.', size=30, col=1)
g95h = IH('g95h', 'no outlet: $\\ 15\\div2=7\\frac{1}{2}$ hours', size=30, col=1)
g95i = IH('g95i', 'the pond: $\\ 60$ units', size=30)
g95j = IH('g95j', 'a hose: $\\ 60\\div15=4$ an hour', size=30)
g95k = IH('g95k', 'the outlet: $\\ 60\\div20=3$ an hour', size=30)
g95l = IH('g95l', '$4+4-3=5$ units an hour', size=30)
g95m = IH('g95m', '$60\\div5=12$ hours', size=30)
CARRY26['solve-wp26-g095'] = {1: ['$\\frac{5}{60}$ of the pond an hour']}
video('solve-wp26-g095', 'solution', qid='wp26-g095', slides=[
    S('Method 1 · The math way: rates as fractions',
      L("Two identical hoses each fill a pond in fifteen hours. An outlet pipe empties a full pond in twenty hours. At "
        "seven a.m. the pond is empty, and both hoses and the outlet pipe are opened. At what time is the pond full?",
        pt('stem', 'Two identical hoses each fill', 'hl', 11.0), voice='calm', pause=0.5),
      L("So two hoses fill the pond, and one pipe empties it. And they ask for a clock time, not for a number of hours.",
        pt('stem: ask', 'And they ask for a clock time')),
      L("We'll solve it in two different ways. Let's start with the math way. Like in the lesson, the pond's size isn't "
        "given, so we call the whole pond one."),
      L("Each hose fills one pond in fifteen hours. The rate is the work over the time, so one fifteenth of the pond an "
        "hour.", show(g95a, 'so one fifteenth of the pond')),
      L("Working together, we add the rates. There are two hoses, so one fifteenth plus one fifteenth.",
        show(g95b, 'so one fifteenth plus one fifteenth')),
      L("The outlet works against them, so its rate gets a minus. It empties one pond in twenty hours, so minus one "
        "twentieth.", show(g95b2, 'so minus one')),
      L("Now a common denominator. Fifteen and twenty both divide sixty. One fifteenth is four sixtieths, because sixty "
        "divided by fifteen is four. One twentieth is three sixtieths, because sixty divided by twenty is three.",
        show(g95c, 'One fifteenth is four sixtieths'), show(g95c2, 'One twentieth is three sixtieths')),
      L("Four plus four is eight. Then eight minus three is five. So together, five sixtieths of the pond an hour.",
        show(g95d, 'So together, five sixtieths'))),
    S('Method 1 · The math way: rates as fractions',
      L("Five sixtieths is one twelfth, because sixty divided by five is twelve.", show(g95e, 'Five sixtieths is one twelfth')),
      L("What does one twelfth mean? Like in the lesson, it's one pond in twelve hours.", show(g95f, "it's one pond in twelve hours")),
      L("This isn't our final answer yet. They ask for a clock time. They started at seven a.m. Seven a.m. plus twelve "
        "hours is seven p.m.", show(g95g, 'Seven a.m. plus twelve hours')),
      L("Careful with two thirty p.m., choice number one. That's what we get if we forget the outlet. Two hoses alone "
        "fill two fifteenths an hour, so one pond in seven and a half hours.", show(g95h, 'Two hoses alone'),
        mk('cross', 'choice 1', 'one pond in seven and a half hours')),
      L("So the pond is full at seven p.m. That's choice number two.")),
    S('Method 2 · Plugging in numbers: a job size',
      L("[pause] Now let's plug in a number for the pond's size. We start again from the givens. Like in the lesson, we "
        "pick a size that fifteen and twenty both divide, sixty units.", show(g95i, 'sixty units')),
      L("Each hose fills sixty units in fifteen hours. Sixty divided by fifteen is four units an hour.",
        show(g95j, 'Sixty divided by fifteen')),
      L("The outlet empties sixty units in twenty hours. Sixty divided by twenty is three units an hour.",
        show(g95k, 'Sixty divided by twenty')),
      L("Each hour, the two hoses add four plus four, eight units. The outlet takes away three. So the pond gains eight "
        "minus three, five units an hour.", show(g95l, 'The outlet takes away three')),
      L("Sixty units at five units an hour. Sixty divided by five is twelve hours. The same twelve hours, so again, seven "
        "p.m.", show(g95m, 'Sixty divided by five')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g096 (the printers)
# Hebrew (wp 6171-6206, her beer question 3 h and 2 h): "I can't add them, the times are different", equal times (6
# hours: 2 + 3 = 5 barrels), one barrel = divide the time by 5, then minutes. English keeps it (30 hours, the common-time
# rows of wp-094 part 2) and adds the rates as fractions and the two-worker shortcut (both taught in wp-094). Minutes:
# 3 3/4 hours = 180 + 45 = 225. Trap at its step: 480 = the 8 batches read as hours.
g96t = TBL('g96t', ['batches', 'hours'], ['A', 'A', 'B', 'B', 'together'], [
    ('r1', [('c', 0, 0, '1'), ('c', 0, 1, '6')]), ('r3', [('c', 2, 0, '1'), ('c', 2, 1, '10')]),
    ('h', [('c', 1, 1, '30'), ('c', 3, 1, '30')]),
    ('a', [('down', 1, 0, 1, '×5'), ('c', 1, 0, '5')]), ('b', [('down', 1, 2, 3, '×3'), ('c', 3, 0, '3')]),
    ('s', [('c', 4, 0, '8'), ('c', 4, 1, '30')])], colw=130, labw=150, rowh=54, side=70, w=480, col=1)
g96a = IH('g96a', '$8$ batches in $30$ hours', size=30)
g96b = IH('g96b', '$1$ batch: $\\ \\frac{30}{8}=3\\frac{6}{8}=3\\frac{3}{4}$ hours', size=30)
g96c = IH('g96c', '$3$ hours $=180$ minutes', size=30)
g96d = IH('g96d', '$\\frac{3}{4}$ hour $=45$ minutes', size=30)
g96e = IH('g96e', '$180+45=225$ minutes', size=30)
g96f = IH('g96f', '$\\frac{1}{6}+\\frac{1}{10}$', size=30)
g96g = IH('g96g', '$=\\frac{5}{30}+\\frac{3}{30}=\\frac{8}{30}$', size=30)
g96h = IH('g96h', '$=\\frac{4}{15}$', size=30)
g96i = IH('g96i', '$4$ batches in $15$ hours', size=30, col=1)
g96j = IH('g96j', '$1$ batch: $\\ \\frac{15}{4}=3\\frac{3}{4}$ hours', size=30, col=1)
g96k = IH('g96k', '$225$ minutes', size=30, col=1)
g96l = IH('g96l', '$\\frac{6\\cdot10}{6+10}=\\frac{60}{16}$', size=30)
g96m = IH('g96m', '$=\\frac{15}{4}=3\\frac{3}{4}$ hours', size=30)
g96n = IH('g96n', '$225$ minutes', size=30)
CARRY26['solve-wp26-g096'] = {1: ['$1$ batch: $\\ 3\\frac{3}{4}$ hours']}
video('solve-wp26-g096', 'solution', qid='wp26-g096', slides=[
    S('Method 1 · The math way: equal times',
      L("Printer A prints one batch of catalogs in six hours, while printer B prints the same batch in ten hours. If "
        "they work together at their usual constant rates, how many minutes do they need for one batch?",
        pt('stem', 'Printer A prints one batch', 'hl', 10.0), voice='calm', pause=0.5),
      L("So two printers work together on one batch. And they ask for minutes, but the times are given in hours.",
        pt('stem: ask', 'And they ask for minutes')),
      L("We'll solve it in three different ways. Let's start with the math way, with equal times, like in the lesson.",
        show(g96t['line'], 'with equal times')),
      L("Printer A prints one batch in six hours. Printer B prints one batch in ten hours.",
        show(g96t['r1'], 'Printer A prints one batch in six'), show(g96t['r3'], 'Printer B prints one batch in ten')),
      L("The times are different, so we can't add yet. We need a time that six and ten both divide. That's thirty "
        "hours.", show(g96t['h'], "That's thirty hours")),
      L("Six hours to thirty is times five. So in thirty hours, printer A prints five batches.",
        show(g96t['a'], 'Six hours to thirty')),
      L("Ten hours to thirty is times three. So in thirty hours, printer B prints three batches.",
        show(g96t['b'], 'Ten hours to thirty')),
      L("They print side by side, during the same thirty hours. So we add the batches. Five plus three is eight batches "
        "in thirty hours.", show(g96t['s'], 'Five plus three is eight'), show(g96a, 'eight batches in thirty hours')),
      L("Careful, eight isn't our answer. Eight hours is four hundred eighty minutes, choice number three. But eight is "
        "the number of batches.", mk('cross', 'choice 3', 'But eight is the number of batches')),
      L("They ask for one batch. Eight batches to one batch is divided by eight. So the time is divided by eight too. "
        "Thirty over eight is three and six eighths, that's three and three quarters hours.",
        show(g96b, "that's three and three quarters")),
    ),
    S('Method 1 · The math way: equal times',
      L("Now minutes. Three hours is three times sixty, a hundred eighty minutes.", show(g96c, 'Three hours is three times sixty')),
      L("Three quarters of an hour is forty-five minutes. A hundred eighty plus forty-five is two hundred twenty-five "
        "minutes.", show(g96d, 'Three quarters of an hour'), show(g96e, 'A hundred eighty plus forty-five')),
      L("So that's choice number two.")),
    S('Method 2 · The math way: rates as fractions',
      L("[pause] Now the math way with the rates, like in the lesson. We start again from the givens. Printer A prints a "
        "sixth of the batch an hour, and printer B a tenth. Together, a sixth plus a tenth.",
        show(g96f, 'Together, a sixth plus a tenth')),
      L("The common denominator is thirty. A sixth is five thirtieths, and a tenth is three thirtieths. Together that's "
        "eight thirtieths.", show(g96g, "Together that's")),
      L("Eight thirtieths is four fifteenths, because we divide the top and the bottom by two.",
        show(g96h, 'Eight thirtieths is four fifteenths')),
      L("What does four fifteenths mean? Four batches in fifteen hours.", show(g96i, 'Four batches in fifteen hours')),
      L("So one batch takes fifteen divided by four. That's three and three quarters hours, the same as before. So two "
        "hundred twenty-five minutes.", show(g96j, 'fifteen divided by four'), show(g96k, 'So two hundred twenty-five'))),
    S('Method 3 · The math way: the shortcut',
      L("[pause] And there's the two-worker shortcut from the lesson. We multiply the two times, and divide by their sum."),
      L("Six times ten is sixty. Six plus ten is sixteen. So sixty over sixteen.", show(g96l, 'Six times ten is sixty')),
      L("We divide the top and the bottom by four. Sixty over sixteen is fifteen over four. That's three and three "
        "quarters hours again.", show(g96m, 'Sixty over sixteen is fifteen over four')),
      L("So two hundred twenty-five minutes.", show(g96n, 'So two hundred twenty-five minutes')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t26-02 (A 10 h, B 15 h)
# No Hebrew (a September addition; real exam 2019_spring_q1_08). The range check (wp-094 part 2) as an estimate first,
# then a job size (30 units) and the shortcut (both wp-094). Trap at its step: 12.5 = the average of the times.
q2a = IH('q2a', 'less than $10$ hours', size=30)
q2b = IH('q2b', '$\\frac{10+15}{2}=12\\frac{1}{2}$: $\\ $the trap', size=30)
q2c = IH('q2c', 'more than $10\\div2=5$ hours', size=30)
q2d = IH('q2d', 'between $5$ and $10$: $\\ $only $6$', size=30)
q2e = IH('q2e', 'the job: $\\ 30$ units', size=30)
q2f = IH('q2f', 'A: $\\ 30\\div10=3$ an hour', size=30)
q2g = IH('q2g', 'B: $\\ 30\\div15=2$ an hour', size=30)
q2h = IH('q2h', '$3+2=5$ an hour', size=30)
q2i = IH('q2i', '$30\\div5=6$ hours', size=30)
q2j = IH('q2j', '$\\frac{10\\cdot15}{10+15}=\\frac{150}{25}$', size=30)
q2k = IH('q2k', '$150\\div25=6$ hours', size=30)
video('solve-q-r26-t26-02', 'solution', qid='q-r26-t26-02', slides=[
    S('Method 1 · Estimation',
      L("Worker A can do a job alone in ten hours. Worker B can do the same job alone in fifteen hours. How many hours "
        "do they need if they work together?", pt('stem', 'Worker A can do a job alone', 'hl', 8.0), voice='calm', pause=0.5),
      L("So two workers, two different times, and they ask for the time together.", pt('stem: ask', 'they ask for the time together')),
      L("We'll solve it in three different ways. Let's start with an estimate, with the range check from the lesson. "
        "Maybe we won't need to calculate at all."),
      L("Worker A needs ten hours alone. With help, A finishes sooner. So together it's less than ten hours.",
        show(q2a, 'So together it')),
      L("Choice number one, twelve and a half, is out. And choice number two, twenty-five, is out.",
        mk('cross', 'choice 1', 'twelve and a half, is out'), mk('cross', 'choice 2', 'twenty-five, is out')),
      L("Careful, twelve and a half is the trap. It's the average of ten and fifteen. But two workers together are "
        "faster than each of them.", show(q2b, "It's the average of ten and fifteen")),
      L("Now, two workers as fast as A would need half of ten, five hours. Worker B is slower than A, so together they "
        "need more than five hours.", show(q2c, 'half of ten, five hours')),
      L("So choice number four, four hours, is out too.", mk('cross', 'choice 4', 'four hours, is out')),
      L("The answer is between five and ten hours. Only six is left. So six hours, choice number three, with no "
        "calculation at all.", show(q2d, 'Only six is left'))),
    S('Method 2 · Plugging in numbers: a job size',
      L("[pause] Now let's find it exactly, and plug in a job size. We start again from the givens. Like in the lesson, "
        "we pick a number that ten and fifteen both divide, thirty units.", show(q2e, 'thirty units')),
      L("Worker A does thirty units in ten hours. Thirty divided by ten is three units an hour.",
        show(q2f, 'Thirty divided by ten')),
      L("Worker B does thirty units in fifteen hours. Thirty divided by fifteen is two units an hour.",
        show(q2g, 'Thirty divided by fifteen')),
      L("Together we add the rates. Three plus two is five units an hour.", show(q2h, 'Three plus two is five')),
      L("Thirty units at five units an hour. Thirty divided by five is six hours.", show(q2i, 'Thirty divided by five'))),
    S('Method 3 · The math way: the shortcut',
      L("[pause] And the math way, with the two-worker shortcut. We multiply the two times, and divide by their sum."),
      L("Ten times fifteen is a hundred fifty. Ten plus fifteen is twenty-five.", show(q2j, 'Ten times fifteen')),
      L("A hundred fifty divided by twenty-five is six. Twenty-five times four is a hundred, and twenty-five times two "
        "is fifty. So six hours.", show(q2k, 'A hundred fifty divided by twenty-five')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-097 (lesson: team questions)
# Hebrew (wp 6207-6341): workers with the same constant rate, "like robots"; considered hard, they need understanding;
# how to spot one (identical, constant rate; a group); the table team | work | time, the work in the middle ("צריך עוד
# זמן" -> the approved English "Teamwork takes time"); her sample (4 carpenters, 20 chairs, 3 hours -> 6 carpenters, 60
# chairs): method 1 ratios ("what happens to the time when each one changes": work x3 -> time x3, team x1.5 -> time
# / 1.5), method 2 the V ("multiply the numbers on the line, divide by what's left"), the upside-down V when the work is
# missing; and later (wp 6782-6790): ratios when ONE thing changes, the V when two change. English (R37: the core
# methods of g098, g105, g105b, 2-3 examples, numbers differ from the Hebrew and the questions): the team's rate (4 an
# hour x 5 = 20), the cooks 6 / 30 / 2 -> 4 / 40 / ? = 4 hours, by ratios (x 4/3, x 3/2) and by the V; the
# upside-down V (4 cooks, 6 hours -> 60 pies; the sense check); ratios or the V. Real exam: 2024_autumn_q1_05,
# 2025_spring_q2_13, 2020_winter_q2_15. NEW (all).
t7s1 = I('t7s1', 'Identical workers, $\\ $a constant rate', size=36)
t7s2 = I('t7s2', 'A group of workers', size=36)
t7s3 = I('t7s3', 'Both: $\\ $a team question', size=36)
t7r1 = IH('t7r1', '$1$ worker: $\\ 4$ boxes an hour', size=36)
t7r2 = IH('t7r2', '$5$ workers: $\\ 5\\times4=20$ boxes an hour', size=36)
t7r3 = I('t7r3', 'The team\'s rate $=$ workers $\\times$ one worker\'s rate', size=34)
t7r4 = IH('t7r4', 'twice the workers: $\\ $twice the work', size=34)
t7r5 = IH('t7r5', 'or the same work in half the time', size=34)
t7q = I('t7q', '$6$ cooks, $\\ 30$ pies, $\\ 2$ hours. $\\ 4$ cooks, $\\ 40$ pies?', size=32, col=1)
t7t = VT('t7t', ('6', '30', '2'), ('4', '40', '?'))
t7w1 = IH('t7w1', 'pies $\\times\\frac{4}{3}$: $\\ $time $\\times\\frac{4}{3}$', size=34, col=1)
t7w2 = IH('t7w2', 'cooks $\\times\\frac{2}{3}$: $\\ $time $\\times\\frac{3}{2}$', size=34, col=1)
t7w3 = IH('t7w3', '$2\\times\\frac{4}{3}\\times\\frac{3}{2}$', size=34, col=1)
t7w4 = IH('t7w4', '$=2\\times2=4$ hours', size=34, col=1)
_wp097 = [
    S('Team Questions',
      L("Now team questions. They're also called worker questions."),
      L("They're considered hard. Not because of the arithmetic, but because they need real understanding. With one "
        "table and one method, they become quick.")),
    S('Spot a team question',
      L("In the last lesson, each worker had a different rate. Here, every worker has the same rate."),
      L("How do we spot a team question? First, the words identical, and constant rate.", show(t7s1, 'the words identical')),
      L("So the workers are like robots. They all work at the same speed, and they never get tired."),
      L("Second, a group of workers. Usually more than two, like five painters or eight machines.",
        show(t7s2, 'Second, a group of workers')),
      L("When we see both, it's a team question.", show(t7s3, "When we see both"))),
    S("The team's rate",
      L("In a team, every worker adds the same rate. Let's see it in numbers."),
      L("One worker packs four boxes an hour.", show(t7r1, 'One worker packs four boxes')),
      L("So five identical workers pack five times four, twenty boxes an hour.", show(t7r2, 'So five identical workers')),
      L("So the team's rate is the number of workers, times one worker's rate.", show(t7r3, "So the team's rate")),
      L("That's why the team size matters. Twice the workers do twice the work in the same time.",
        show(t7r4, 'Twice the workers do twice the work')),
      L("Or they do the same work in half the time. Like in the first lesson, the work is fixed, so the team and the "
        "time go opposite ways.", show(t7r5, 'the same work in half the time'))),
    S('The table',
      L("Every team question goes into a table with three columns, team, work and time.", show(t7t['line'], 'goes into a table')),
      L("The work always sits in the middle. How do we remember the order? Teamwork takes time. Team, work, time."),
      L("Row one is what they give us. Row two is what they ask about."),
      L("Here's an example. Six cooks make thirty pies in two hours. How many hours do four cooks need for forty pies?",
        show(t7q, 'Six cooks make thirty pies')),
      L("Row one is six cooks, thirty pies and two hours.", show(t7t['r1'], 'Row one is six cooks')),
      L("Row two is four cooks and forty pies. The question mark goes in the time.", show(t7t['r2'], 'Row two is four cooks'))),
    S('Ratios',
      L("The first way is ratios. We look at each change, and ask what it does to the time. We want the time, so we "
        "start from the two hours."),
      L("The pies go from thirty to forty. That's times four thirds. More work takes more time, the same way. So the "
        "time is times four thirds too.", show(t7w1, 'The pies go from thirty to forty')),
      L("The cooks go from six to four. That's times two thirds. Fewer cooks take more time. That's the opposite way, so "
        "we flip it. The time is times three halves.", show(t7w2, 'The cooks go from six to four')),
      L("So the time is two, times four thirds, times three halves.", show(t7w3, 'So the time is two, times')),
      L("Four thirds times three halves. The threes cancel, and four over two is two. So two times two is four hours.",
        show(t7w4, 'So two times two is four')),
      L("Like in the first lesson. The same way, we multiply as it is. The opposite way, we flip it.")),
]
t7u = VT('t7u', ('6', '30', '2'), ('4', '40', '?'))
t7v = VT('t7v', ('6', '30', '2'), ('4', '40', '?'))
t7x1 = IH('t7x1', '$?=\\frac{6\\cdot40\\cdot2}{30\\cdot4}$', size=34, col=1)
t7x2 = IH('t7x2', '$40\\div4=10$', size=34, col=1)
t7x3 = IH('t7x3', '$\\frac{6\\cdot10\\cdot2}{30}=\\frac{120}{30}$', size=34, col=1)
t7x4 = IH('t7x4', '$=4$ hours', size=34, col=1)
t7y0 = I('t7y0', '$4$ cooks for $6$ hours: $\\ $how many pies?', size=32)
t7y = VT('t7y', ('6', '30', '2'), ('4', '?', '6'), unknown='work')
t7y1 = IH('t7y1', '$?=\\frac{4\\cdot30\\cdot6}{6\\cdot2}$', size=34, col=1)
t7y2 = IH('t7y2', '$\\frac{4\\cdot30}{2}=\\frac{120}{2}=60$ pies', size=34, col=1)
t7y3 = IH('t7y3', 'fewer cooks, $\\ $but $3$ times the hours', size=32, col=1)
t7z1 = I('t7z1', 'One thing changes: $\\ $ratios', size=36)
t7z2 = IH('t7z2', 'the same job, $\\ $twice the time: $\\ $half the workers', size=34)
t7z3 = I('t7z3', 'Two things change: $\\ $the V', size=36)
t7k1 = I('t7k1', 'Identical, constant rate, $\\ $a group: $\\ $a team question', size=34)
t7k2 = I('t7k2', 'The table: $\\ $team, work, time', size=34)
t7k3 = I('t7k3', 'Ratios: $\\ $the same way as it is, $\\ $the opposite way flipped', size=34)
t7k4 = I('t7k4', 'The V: $\\ $multiply the V, $\\ $divide by the other two', size=34)
t7k5 = I('t7k5', 'The work is asked: $\\ $the V upside down', size=34)
_wp097[-1]['lines'][0]['cues'] += [show(t7u['line'], 'The first way is ratios'), show(t7u['r1'], 'The first way is ratios'),
                                   show(t7u['r2'], 'The first way is ratios')]
_wp097 += [
    S('The V method',
      L("Now a method that does all this thinking for us. It's called the V method.",
        show(t7v['line'], "It's called the V method"), show(t7v['r1'], "It's called the V method"),
        show(t7v['r2'], "It's called the V method")),
      L("We use the same table. The question mark is in row two, in the time column."),
      L("Now we draw a V. It starts at the team in row one, goes down to the work in row two, and up to the time in row "
        "one.", show(t7v['v'], 'Now we draw a V')),
      L("So the V joins six, forty and two."),
      L("The rule is, multiply the three numbers on the V, and divide by the other two.", show(t7v['calc'], 'The rule is')),
      L("On top, six times forty times two. At the bottom, thirty times four.", show(t7x1, 'On top, six times forty times two')),
      L("Let's cancel first. Forty divided by four is ten.", show(t7x2, 'Forty divided by four is ten')),
      L("So on top, six times ten times two. At the bottom, thirty. Six times ten times two is a hundred twenty.",
        show(t7x3, 'So on top, six times ten')),
      L("And a hundred twenty divided by thirty is four. So four hours, the same as with ratios.",
        show(t7x4, 'And a hundred twenty divided by thirty')),
      L("The V gives the same calculation as ratios: multiply by forty over thirty for the pies, and six over four "
        "for the cooks. The cooks are flipped because fewer cooks need more time.")),
    S('The V upside down',
      L("The V must join three numbers. So it depends on where the question mark is."),
      L("When the question mark is in the team or the time, we use the V like before."),
      L("But when the question mark is in the work, the V turns upside down. Let's see an example.",
        show(t7y0, 'the V turns upside down')),
      L("The same six cooks make thirty pies in two hours. How many pies do four cooks make in six hours?",
        show(t7y['line'], 'The same six cooks'), show(t7y['r1'], 'The same six cooks'), show(t7y['r2'], 'How many pies do four')),
      L("Now the V starts at the team in row two, goes up to the work in row one, and down to the time in row two. So it "
        "joins four, thirty and six.", show(t7y['v'], 'Now the V starts at the team in row two')),
      L("On top, four times thirty times six. At the bottom, the other two, six times two.", show(t7y1, 'On top, four times thirty'),
        show(t7y['calc'], 'At the bottom, the other two')),
      L("The sixes cancel. Four times thirty is a hundred twenty. And a hundred twenty divided by two is sixty pies.",
        show(t7y2, 'The sixes cancel')),
      L("Does it make sense? There are fewer cooks, but they work three times as many hours. So more than thirty pies "
        "makes sense.", show(t7y3, 'There are fewer cooks'))),
    S('Ratios or the V?',
      L("So when do we use which? When only one thing changes, ratios are quick.", show(t7z1, 'When only one thing changes')),
      L("For example, the same job with twice the time needs only half the workers.", show(t7z2, 'the same job with twice')),
      L("When two things change, the V does the thinking for us.", show(t7z3, 'When two things change')),
      L("Either way, the table always comes first. Team, work, time.")),
    S('Recap',
      L("So let's sum it up. Identical workers with a constant rate, in a group, means a team question.",
        show(t7k1, 'Identical workers with a constant rate')),
      L("We put it in a table. Team, work, time, with the work in the middle.", show(t7k2, 'We put it in a table')),
      L("With ratios, a change that goes the same way stays as it is. A change that goes the opposite way gets flipped.",
        show(t7k3, 'With ratios')),
      L("With the V, we multiply the three numbers on the V, and divide by the other two.", show(t7k4, 'With the V')),
      L("And when the work is asked, the V is upside down.", show(t7k5, 'when the work is asked')),
      L("Take a moment to memorize this, and I'll see you in the next video.")),
]
video('wp-097', 'lesson', slides=_wp097)
SPLITS.append(('wp-097', 'Team Questions', [
    (1, None),
    (5, "Let's continue with team questions, and learn the V method.")]))

# ------------------------------------------------------------------------------------------------ g098 (the gardeners)
# Hebrew (wp 6222-6341, the carpenters 4 / 20 / 3 -> 6 / 60): spot the team question, the table, method 1 ratios (work x3
# -> time x3; team x1.5 -> time / 1.5), method 2 the V. English keeps both (the lesson wp-097 taught them on the cooks;
# here applied slowly with "like in the lesson"). The old Method 3 (worker-hours) is cut: worker-hours come in the next
# lesson (wp-099). Traps at their steps: 16 (the team not flipped), 12 (the team change forgotten).
g98t = VT('g98t', ('3', '40', '5'), ('4', '96', '?'), col=1, w=400)
g98a = IH('g98a', '$\\frac{96}{40}=\\frac{12}{5}$', size=30)
g98b = IH('g98b', 'trees $\\times\\frac{12}{5}$: $\\ $time $\\times\\frac{12}{5}$', size=30)
g98c = IH('g98c', 'gardeners $\\times\\frac{4}{3}$: $\\ $time $\\times\\frac{3}{4}$', size=30)
g98d = IH('g98d', '$5\\times\\frac{12}{5}=12$', size=30, col=1)
g98e = IH('g98e', '$12\\times\\frac{3}{4}=9$ hours', size=30, col=1)
g98f = IH('g98f', '$12\\times\\frac{4}{3}=16$: $\\ $not flipped', size=30)
g98u = VT('g98u', ('3', '40', '5'), ('4', '96', '?'), col=1)
g98g = IH('g98g', '$?=\\frac{3\\cdot96\\cdot5}{40\\cdot4}$', size=30)
g98h = IH('g98h', '$96\\div4=24$', size=30)
g98i = IH('g98i', '$3\\cdot24=72$', size=30)
g98i2 = IH('g98i2', '$72\\cdot5=360$', size=30)
g98j = IH('g98j', '$360\\div40=9$ hours', size=30)
video('solve-wp26-g098', 'solution', qid='wp26-g098', slides=[
    S('Method 1 · Understanding: ratios',
      L("Three identical gardeners plant forty trees in five hours. How many hours do four such gardeners need to plant "
        "ninety-six trees?", pt('stem', 'Three identical gardeners plant', 'hl', 8.0), voice='calm', pause=0.5),
      L("Identical gardeners, and a group of them. So it's a team question, and they ask for the time.",
        pt('stem: ask', 'and they ask for the time')),
      L("We'll solve it in two different ways. Let's start by understanding, with ratios. Like in the lesson, first the "
        "table. Team, work, time.", show(g98t['line'], 'first the table')),
      L("Row one is three gardeners, forty trees and five hours. Row two is four gardeners, ninety-six trees, and the "
        "question mark in the time.", show(g98t['r1'], 'Row one is three gardeners'), show(g98t['r2'], 'Row two is four')),
      L("We want the time, so we ask what each change does to the time. We start from the five hours."),
      L("The trees go from forty to ninety-six. Ninety-six over forty. Both divide by eight, so it's twelve fifths.",
        show(g98a, 'Both divide by eight')),
      L("More trees take more time. That's the same way, so the time is times twelve fifths too.",
        show(g98b, 'More trees take more time')),
      L("The gardeners go from three to four. That's times four thirds. But more gardeners take less time. That's the "
        "opposite way, so we flip it. The time is times three quarters.", show(g98c, 'The gardeners go from three to four')),
      L("Now the time. Five times twelve fifths. The fives cancel, and we get twelve.", show(g98d, 'Five times twelve fifths')),
      L("Careful, twelve isn't our answer yet, and it's choice number three. We still need the change in the gardeners."),
      L("Twelve times three quarters. Twelve divided by four is three. Then three times three is nine hours.",
        show(g98e, 'Twelve times three quarters')),
      L("And careful with sixteen, choice number one. That's twelve times four thirds. It forgets to flip the gardeners.",
        show(g98f, "That's twelve times four thirds"), mk('cross', 'choice 1', 'It forgets to flip the gardeners')),
      L("So they need nine hours. That's choice number two.")),
    S('Method 2 · The math way: the V method',
      L("[pause] Now the math way, with the V method from the lesson. We start again from the givens, in the same table.",
        show(g98u['line'], 'in the same table'), show(g98u['r1'], 'in the same table'), show(g98u['r2'], 'in the same table')),
      L("The question mark is in the time. So the V starts at the team in row one, goes down to the work in row two, and "
        "up to the time in row one. It joins three, ninety-six and five.", show(g98u['v'], 'So the V starts at the team')),
      L("We multiply the three numbers on the V, and divide by the other two, forty and four.",
        show(g98u['calc'], 'We multiply the three numbers'), show(g98g, 'divide by the other two')),
      L("Let's cancel first. Ninety-six divided by four is twenty-four.", show(g98h, 'Ninety-six divided by four')),
      L("Three times twenty-four is seventy-two. Then seventy-two times five is three hundred sixty.",
        show(g98i, 'Three times twenty-four'), show(g98i2, 'Then seventy-two times five')),
      L("Three hundred sixty divided by forty is nine. Nine hours again.", show(g98j, 'Three hundred sixty divided by forty')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-099 (lesson: worker-hours)
# Hebrew (wp 6342-6382): "work time" = the time one worker needs alone = time x workers (2 workers, 3 hours -> 6);
# her road question (20 x 10 + 15 x 10 = 350, "I'm the contractor: how many days of pay?"). English (R37: the core of
# g100, g105, g105b, q-r26-t26-03, 2-3 examples, new numbers): 3 workers x 4 hours = 12 worker-hours (the boss who pays
# by the hour), splitting the 12 (6 workers, 2 workers, 3 hours), stages (5 x 3 + 2 x 4 = 23 worker-days; the trap 7 x
# 7), and someone joins in the middle: the whole job minus what's done is what's left (40 liters, 4 a minute for 5
# minutes, then 4 + 6; "how many more" or "in total"). Real exam: 2026_spring_q1_07, 2019_winter_q2_06, 2023_winter_q2_09.
t9a1 = IH('t9a1', '$3$ workers, $\\ 4$ hours each', size=36)
t9a2 = IH('t9a2', '$3\\times4=12$ worker hours', size=36)
t9a3 = I('t9a3', 'One worker alone: $\\ 12$ hours', size=36)
t9a4 = I('t9a4', 'Worker-hours $=$ workers $\\times$ hours', size=36)
t9b1 = IH('t9b1', '$6$ workers: $\\ 12\\div6=2$ hours', size=36)
t9b2 = IH('t9b2', '$2$ workers: $\\ 12\\div2=6$ hours', size=36)
t9b3 = IH('t9b3', 'in $3$ hours: $\\ 12\\div3=4$ workers', size=36)
t9c1 = IH('t9c1', '$5$ workers, $\\ 3$ days: $\\ 5\\times3=15$', size=36)
t9c2 = IH('t9c2', '$2$ workers, $\\ 4$ days: $\\ 2\\times4=8$', size=36)
t9c3 = IH('t9c3', '$15+8=23$ worker days', size=36)
t9c4 = IH('t9c4', '$(5+2)\\times(3+4)=49$: $\\ $the trap', size=34)
t9d0 = I('t9d0', 'A tank: $\\ 40$ liters. $\\ $Pipe A: $\\ 4$ a minute.', size=34)
t9d1 = I('t9d1', 'After $5$ minutes, $\\ $pipe B joins: $\\ 6$ a minute', size=34)
t9d2 = IH('t9d2', 'done: $\\ 4\\times5=20$ liters', size=34)
t9d3 = IH('t9d3', 'left: $\\ 40-20=20$ liters', size=34)
t9d4 = IH('t9d4', 'together: $\\ 4+6=10$ a minute', size=34)
t9d5 = IH('t9d5', '$20\\div10=2$ more minutes', size=34)
t9d6 = IH('t9d6', 'in total: $\\ 5+2=7$ minutes', size=34)
t9d7 = I('t9d7', 'The whole job $-$ done $=$ left', size=34)
t9k2 = I('t9k2', 'Share them among any team. $\\ $Stages: $\\ $add them up.', size=34)
t9k3 = I('t9k3', 'Joins or leaves: $\\ $the whole job $-$ done $=$ left', size=34)
# 2026-10-21 (external-course review, approved): two more time questions, after "someone joins in the middle" (part 2):
# staggered arrival (real exam 2023_spring_q2_07, the bees; new story and numbers): 30 flyers, a volunteer joins every
# minute, 2 flyers a minute each -> minute by minute in a table: 2, 6, 12, 20, 30 -> the first worked 5 minutes = 10
# (the check 10 + 8 + 6 + 4 + 2 = 30); and work-rest cycles (real exams 2019_winter_q1_20, 2025_autumn_q2_11): 8 boxes
# every 5 minutes of work, 10 minutes' rest after every 30 minutes of work; in one hour: work 0-30, rest 30-40, work
# 40-60 (the next break would start at 40 + 30 = 70) -> 50 working minutes = 10 x 5 -> 80 boxes (the trap 96).
t9e0 = I('t9e0', '$30$ flyers. $\\ $A volunteer joins every minute. $\\ 2$ flyers a minute each.', size=30)
t9e1 = I('t9e1', 'The first volunteer: $\\ $how many flyers?', size=30)
t9et = TBL('t9et', ['minute', 'volunteers', 'this minute', 'so far'], ['', '', '', '', ''], [
    ('r1', [('c', 0, 0, '1'), ('c', 0, 1, '1')]),
    ('r1work', [('c', 0, 2, '1×2=2')]), ('r1sum', [('c', 0, 3, '2')]),
    ('r2', [('c', 1, 0, '2'), ('c', 1, 1, '2')]),
    ('r2work', [('c', 1, 2, '2×2=4')]), ('r2sum', [('c', 1, 3, '2+4=6')]),
    ('r3', [('c', 2, 0, '3'), ('c', 2, 1, '3')]),
    ('r3work', [('c', 2, 2, '3×2=6')]), ('r3sum', [('c', 2, 3, '6+6=12')]),
    ('r4', [('c', 3, 0, '4'), ('c', 3, 1, '4')]),
    ('r4work', [('c', 3, 2, '4×2=8')]), ('r4sum', [('c', 3, 3, '12+8=20')]),
    ('r5', [('c', 4, 0, '5'), ('c', 4, 1, '5')]),
    ('r5work', [('c', 4, 2, '5×2=10')]), ('r5sum', [('c', 4, 3, '20+10=30')]),
    ('end', [('box', 4, 3)])], colw=170, rowh=64, size=30, w=560)
t9e2 = IH('t9e2', 'the first: $\\ 5\\times2=10$ flyers', size=30, col=1)
t9e3 = IH('t9e3', 'the third: $\\ 3\\times2=6$', size=30, col=1)
t9e4 = IH('t9e4', '$10+8+6+4+2=30$', size=30, col=1)
t9e5 = I('t9e5', 'Step by step, $\\ $until the whole job is done', size=30, col=1)
t9f0 = I('t9f0', '$8$ boxes every $5$ minutes of work. $\\ $After every $30$ minutes of work: $\\ 10$ minutes\' rest.', size=28)
t9f1 = I('t9f1', 'How many boxes in one hour?', size=30)
t9ft = UNITS('t9ft', [('', 12)], [
    ('t0', [('tick', 0, 0, '0'), ('tick', 0, 12, '60')]),
    ('w1', [('fill', 0, 0, 6), ('br', 0, 0, 6, 'work 30'), ('tick', 0, 6, '30')]),
    ('r', [('fill', 0, 6, 8, 'grey'), ('br', 0, 6, 8, 'rest 10'), ('tick', 0, 8, '40')]),
    ('w2', [('fill', 0, 8, 12), ('br', 0, 8, 12, 'work 20')])], unit=50, boxh=46, labw=10, gap=62, w=560,
    title='One hour, in steps of 5 minutes')
t9f2 = IH('t9f2', 'next break: $\\ 40+30=70$, $\\ $after the hour', size=30, col=1)
t9f3 = IH('t9f3', '$30+20=50$ minutes of work', size=30, col=1)
t9f4 = IH('t9f4', '$50\\div5=10$', size=30, col=1)
t9f5 = IH('t9f5', '$10\\times8=80$ boxes', size=30, col=1)
t9f6 = IH('t9f6', '$60\\div5=12$, $\\ 12\\times8=96$: $\\ $the trap', size=30, col=1)
t9f7 = I('t9f7', 'Breaks: $\\ $draw the timeline, $\\ $count only the working minutes', size=30)
t9k4 = I('t9k4', 'One after another: $\\ $step by step, in a table', size=34)
t9k5 = I('t9k5', 'Breaks: $\\ $count only the working minutes', size=34)
video('wp-099', 'lesson', slides=[
    S('Worker-Hours',
      L("Now the last type, worker-hours."),
      L("It's a small twist on team questions. And it helps a lot when the team changes during the job.")),
    S('What worker-hours are',
      L("Worker-hours tell us how big a job is. Here all workers have the same constant rate. So we can count the job "
        "in hours of one worker."),
      L("Let's see it in numbers. Three workers clean a hall in four hours. Each of them works four hours.",
        show(t9a1, 'Three workers clean a hall')),
      L("So three workers, four hours each. Three times four is twelve worker-hours.", show(t9a2, 'Three times four is twelve')),
      L("Only four hours pass on the clock. But there are twelve hours of work in that hall."),
      L("So one worker alone would need twelve hours.", show(t9a3, 'So one worker alone')),
      L("Think of the boss who pays the workers by the hour. She pays three workers for four hours each. That's twelve "
        "hours of pay."),
      L("With days instead of hours, it's worker-days. It's the same idea.")),
    S('Share the worker-hours',
      L("Once we know the worker-hours, we can share them in any way."),
      L("The hall needs twelve worker-hours. With six workers, twelve divided by six is two hours.",
        show(t9b1, 'With six workers')),
      L("With two workers, twelve divided by two is six hours.", show(t9b2, 'With two workers')),
      L("And to finish in three hours, twelve divided by three is four workers.", show(t9b3, 'to finish in three hours'))),
    S('Work in stages',
      L("Sometimes the team changes during the job. Then we count each stage, and add them up."),
      L("Five workers work for three days. Five times three is fifteen worker-days.", show(t9c1, 'Five workers work for three')),
      L("Then two workers work for four more days. Two times four is eight worker-days.", show(t9c2, 'Then two workers')),
      L("Fifteen plus eight is twenty-three worker-days. So one worker alone would need twenty-three days.",
        show(t9c3, 'Fifteen plus eight')),
      L("Careful, don't add the workers and the days first. Seven workers never worked seven days together. That gives "
        "forty-nine, which is the trap.", show(t9c4, "Seven workers never worked"))),
    S('Someone joins in the middle',
      L("Sometimes a worker joins in the middle, or leaves. Then we split the job into what's done and what's left."),
      L("A tank holds forty liters. Pipe A fills four liters a minute.", show(t9d0, 'A tank holds forty liters')),
      L("After five minutes, pipe B joins, with six liters a minute. How long until the tank is full?",
        show(t9d1, 'After five minutes')),
      L("First, what's done. Pipe A worked alone for five minutes. Four times five is twenty liters.",
        show(t9d2, 'Four times five is twenty')),
      L("So what's left is forty minus twenty, twenty liters.", show(t9d3, "So what's left")),
      L("Now they work together, so we add the rates. Four plus six is ten liters a minute.",
        show(t9d4, 'Four plus six is ten')),
      L("Twenty liters at ten liters a minute. Twenty divided by ten is two more minutes.",
        show(t9d5, 'Twenty divided by ten')),
      L("Careful, read what they ask. Two more minutes, or five plus two, seven minutes in total.",
        show(t9d6, 'five plus two, seven minutes')),
      L("So the whole job, minus what's done, is what's left. Then we divide what's left by the new rate.",
        show(t9d7, 'So the whole job, minus'))),
    S('One after another',
      L("Sometimes workers don't join just once. They join one after another, at fixed times. Then we go step by step, "
        "minute by minute, in a table."),
      L("A box holds thirty flyers. One volunteer starts handing them out. A minute later a second volunteer joins, a "
        "minute after that a third, and so on. Each volunteer hands out two flyers a minute, until the box is empty.",
        show(t9e0, 'A box holds thirty flyers')),
      L("How many flyers did the first volunteer hand out?", show(t9e1, 'How many flyers did the first')),
      L("Let's make a table. For each minute, we write how many volunteers are working, how many flyers they hand out "
        "in that minute, and how many are gone so far.", show(t9et['line'], "Let's make a table")),
      L("In the first minute, only one volunteer works. One times two is two flyers. So far, two flyers are gone.",
        show(t9et['r1'], 'In the first minute'), show(t9et['r1work'], 'One times two is two'),
        show(t9et['r1sum'], 'So far, two flyers')),
      L("In the second minute, two volunteers work. Two times two is four flyers. Two plus four is six so far.",
        show(t9et['r2'], 'In the second minute'), show(t9et['r2work'], 'Two times two is four'),
        show(t9et['r2sum'], 'Two plus four is six')),
      L("In the third minute, three volunteers work. Three times two is six. Six plus six is twelve so far.",
        show(t9et['r3'], 'In the third minute'), show(t9et['r3work'], 'Three times two is six'),
        show(t9et['r3sum'], 'Six plus six is twelve')),
      L("In the fourth minute, four volunteers hand out four times two, eight. Twelve plus eight is twenty so far.",
        show(t9et['r4'], 'In the fourth minute'), show(t9et['r4work'], 'four times two, eight'),
        show(t9et['r4sum'], 'Twelve plus eight is twenty')),
      L("In the fifth minute, five volunteers hand out five times two, ten. Twenty plus ten is thirty. That's the whole "
        "box, so they stop after five minutes.", show(t9et['r5'], 'In the fifth minute'),
        show(t9et['r5work'], 'five times two, ten'), show(t9et['r5sum'], 'Twenty plus ten is thirty'),
        show(t9et['end'], "That's the whole box")),
      L("Now we can answer the question. The first volunteer worked all five minutes, at two flyers a minute. Five times two is ten "
        "flyers.", show(t9e2, 'Five times two is ten')),
      L("Careful, the volunteers didn't all hand out the same. The third volunteer joined in the third minute, so she "
        "worked three minutes. Three times two is six flyers.", show(t9e3, 'Three times two is six flyers')),
      L("Let's check. From the first volunteer to the fifth, they handed out ten, eight, six, four and two flyers. That "
        "adds up to thirty, the whole box.", show(t9e4, 'they handed out ten, eight')),
      L("Here the box ran out exactly at the end of a minute. If it runs out in the middle of a minute, the last step is "
        "only part of a minute. So we go step by step, and stop when the total reaches the whole job.",
        show(t9e5, 'stop when the total reaches'))),
    S('Clock time and working time',
      L("One more kind of question. Sometimes a worker takes breaks. Then the time on the clock is not the same as the "
        "time she works."),
      L("A worker packs eight boxes every five minutes of work. After every thirty minutes of work, she rests for ten "
        "minutes.", show(t9f0, 'A worker packs eight boxes')),
      L("How many boxes does she pack in one hour?", show(t9f1, 'How many boxes does she pack')),
      L("Let's draw the hour as a timeline, in steps of five minutes. It starts at zero and ends at sixty.",
        show(t9ft['line'], "Let's draw the hour"), show(t9ft['t0'], 'It starts at zero')),
      L("She works for the first thirty minutes. So the clock shows thirty when her first break starts.",
        show(t9ft['w1'], 'She works for the first thirty')),
      L("She rests for ten minutes, from thirty to forty.", show(t9ft['r'], 'She rests for ten minutes')),
      L("Then she works again, from forty to sixty. That's twenty minutes of work.",
        show(t9ft['w2'], 'Then she works again')),
      L("Why is there no second break in the hour? Her next break comes after thirty more minutes of work. Forty plus "
        "thirty is seventy, and the hour ends at sixty.", show(t9f2, 'Forty plus thirty is seventy')),
      L("So her working time is thirty plus twenty, fifty minutes.", show(t9f3, 'thirty plus twenty, fifty')),
      L("She packs eight boxes in every five minutes of work. So how many five-minute parts are in fifty minutes? Fifty "
        "divided by five is ten.", show(t9f4, 'Fifty divided by five is ten')),
      L("Ten parts, eight boxes in each. Ten times eight is eighty boxes.", show(t9f5, 'Ten times eight is eighty')),
      L("A lot of students divide the whole hour by five. Sixty divided by five is twelve. And twelve times eight is "
        "ninety-six. But she doesn't pack while she rests.", show(t9f6, 'Sixty divided by five is twelve')),
      L("So draw the timeline, mark when each break starts, and count only the working minutes inside the time they "
        "ask about. And read the question carefully. Does the break come after thirty minutes of work, or every thirty "
        "minutes on the clock?", show(t9f7, 'count only the working minutes'))),
    S('Recap',
      L("So let's sum it up. With workers at the same constant rate, worker-hours are the workers times the hours. "
        "That's how long one worker alone would need.",
        show(t9a4, 'Worker-hours are the workers times')),
      L("We can share the worker-hours among any team. And in stages, we count each stage and add.",
        show(t9k2, 'We can share the worker-hours')),
      L("When someone joins or leaves, the whole job minus what's done is what's left.", show(t9k3, 'When someone joins')),
      L("When workers join one after another, we go step by step in a table, until the whole job is done.",
        show(t9k4, 'When workers join one after another')),
      L("And with breaks, we count only the working minutes.", show(t9k5, 'And with breaks')),
      L("Take a moment to memorize this, and I'll see you in the next video.")),
])
SPLITS.append(('wp-099', 'Worker-Hours', [
    (1, None),
    (5, "Let's continue, with two more questions where we follow the time step by step.")]))

# ------------------------------------------------------------------------------------------------ g100 (the fence)
# Hebrew (wp 6362-6382, the road 20 x 10 + 15 x 10 = 350): "I'm the contractor, how many days of pay?", each stage
# workers x days, add, = one worker alone. One method, as in the Hebrew (worker-days, wp-099: applied slowly with "like
# in the lesson"). Traps at their steps: 126 (only the first stage), 400 (20 workers x 20 days).
g10a = IH('g10a', '$10\\times9=90$', size=30)
g10a2 = IH('g10a2', '$4\\times9=36$', size=30)
g10b = IH('g10b', '$14\\times9=90+36=126$', size=30)
g10c = IH('g10c', '$6\\times11=66$', size=30)
g10d = IH('g10d', '$126+66=192$ worker days', size=30)
g10e = IH('g10e', '$126+70=196$', size=30, col=1)
g10e2 = IH('g10e2', '$196-4=192$', size=30, col=1)
g10f = IH('g10f', '$126$: $\\ $only the first stage', size=30, col=1)
g10g = IH('g10g', '$(14+6)\\times(9+11)=400$: $\\ $the trap', size=30, col=1)
video('solve-wp26-g100', 'solution', qid='wp26-g100', slides=[
    S('Method 1 · The math way: worker-days',
      L("A fence around a park is completed by fourteen workers working for nine days, followed by six workers working "
        "for eleven days. All work at the same constant rate. How many days would one worker need to complete the whole "
        "fence alone?", pt('stem', 'A fence around a park', 'hl', 11.0), voice='calm', pause=0.5),
      L("So the team changes in the middle of the job. And they ask how long one worker would need alone.",
        pt('stem: ask', 'they ask how long one worker')),
      L("Like in the lesson, that's the worker-days. Think of the boss who pays every worker for every day. How many "
        "days of pay does the whole fence take?"),
      L("The first stage is fourteen workers for nine days. Fourteen times nine. Ten times nine is ninety. Then four times "
        "nine is thirty-six.", show(g10a, 'Ten times nine is ninety'), show(g10a2, 'Then four times')),
      L("Ninety plus thirty-six is a hundred twenty-six worker-days.", show(g10b, 'Ninety plus thirty-six')),
      L("Careful, a hundred twenty-six is choice number one, but that's only the first stage.",
        show(g10f, "but that's only the first stage"), mk('cross', 'choice 1', "only the first stage")),
      L("The second stage is six workers for eleven days. Six times eleven is sixty-six worker-days.",
        show(g10c, 'Six times eleven is sixty-six')),
      L("Now we add the two stages. A hundred twenty-six plus sixty-six. Plus seventy is a hundred ninety-six, and then "
        "we take away four. That's a hundred ninety-two.", show(g10e, 'Plus seventy is a hundred ninety-six'), show(g10e2, 'we take away four')),
      L("So the whole fence takes a hundred ninety-two worker-days.", show(g10d, 'So the whole fence takes')),
      L("And one worker does one worker-day each day. So alone, one worker needs a hundred ninety-two days."),
      L("Careful with four hundred, choice number two. It adds the workers, fourteen plus six is twenty. It adds the "
        "days, nine plus eleven is twenty. And twenty times twenty is four hundred.", show(g10g, 'twenty times twenty')),
      L("But twenty workers never worked together, and no worker worked twenty days. So we count each stage on its own.",
        mk('cross', 'choice 2', 'So we count each stage on its own')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t26-03 (pipe B joins)
# No Hebrew (a September addition; real exams 2019_winter_q2_06, 2023_winter_q2_09). Someone joins in the middle (wp-099:
# the whole job minus what's done is what's left), with a job size (wp-094) and with fractions. Traps at their steps:
# 6 = the total time (they ask how many MORE), 4 = the whole pool together from the start.
q3a = IH('q3a', 'the pool: $\\ 12$ units', size=30)
q3b = IH('q3b', 'A: $\\ 12\\div12=1$ an hour', size=30)
q3c = IH('q3c', 'B: $\\ 12\\div6=2$ an hour', size=30)
q3d = IH('q3d', 'done: $\\ 3\\times1=3$', size=30)
q3e = IH('q3e', 'left: $\\ 12-3=9$', size=30, col=1)
q3f = IH('q3f', 'together: $\\ 1+2=3$ an hour', size=30, col=1)
q3g = IH('q3g', '$9\\div3=3$ more hours', size=30, col=1)
q3h = IH('q3h', '$3+3=6$ in total: $\\ $the trap', size=30, col=1)
q3i = IH('q3i', '$12\\div3=4$: $\\ $from the start', size=30, col=1)
q3j = IH('q3j', 'A: $\\ \\frac{1}{12}$ an hour, $\\ 3\\times\\frac{1}{12}=\\frac{1}{4}$', size=30)
q3k = IH('q3k', 'left: $\\ 1-\\frac{1}{4}=\\frac{3}{4}$', size=30)
q3l = IH('q3l', '$\\frac{1}{12}+\\frac{1}{6}=\\frac{1}{12}+\\frac{2}{12}=\\frac{3}{12}$', size=30, col=1)
q3m = IH('q3m', '$\\frac{3}{12}=\\frac{1}{4}$ an hour', size=30, col=1)
q3n = IH('q3n', '$\\frac{3}{4}$ at $\\frac{1}{4}$ an hour: $\\ 3$ hours', size=30, col=1)
video('solve-q-r26-t26-03', 'solution', qid='q-r26-t26-03', slides=[
    S('Method 1 · Plugging in numbers: a job size',
      L("Pipe A fills a pool in twelve hours. Pipe B fills the same pool in six hours. Pipe A runs alone for three hours, "
        "and then pipe B is also opened. How many more hours are needed to fill the pool?",
        pt('stem', 'Pipe A fills a pool', 'hl', 10.0), voice='calm', pause=0.5),
      L("So pipe B joins in the middle. And they ask how many more hours, after pipe B is opened.",
        pt('stem: ask', 'they ask how many more hours')),
      L("We'll solve it in two different ways. Let's start by plugging in a job size. The pool's size isn't given, so "
        "we choose twelve units, because twelve and six both divide twelve.", show(q3a, 'we choose twelve units')),
      L("Pipe A fills twelve units in twelve hours. That's one unit an hour.", show(q3b, "That's one unit an hour")),
      L("Pipe B fills twelve units in six hours. Twelve divided by six is two units an hour.", show(q3c, 'Twelve divided by six')),
      L("Like in the lesson, first what's done. Pipe A works alone for three hours. Three times one is three units.",
        show(q3d, 'Three times one is three')),
      L("So what's left is twelve minus three, nine units.", show(q3e, 'twelve minus three')),
      L("Now both pipes work, so we add the rates. One plus two is three units an hour.", show(q3f, 'One plus two is three')),
      L("Nine units at three units an hour. Nine divided by three is three more hours.", show(q3g, 'Nine divided by three')),
      L("Careful with six, choice number two. Three plus three is six hours in total. But they ask how many more hours.",
        show(q3h, 'Three plus three is six'), mk('cross', 'choice 2', 'they ask how many more hours')),
      L("And four, choice number four, is the whole pool with both pipes from the start. Twelve divided by three is "
        "four. But pipe A already did three units.", show(q3i, 'Twelve divided by three is four'),
        mk('cross', 'choice 4', 'But pipe A already did')),
      L("So three more hours. That's choice number three.")),
    S('Method 2 · The math way: rates as fractions',
      L("[pause] Now the math way, with fractions. We start again from the givens, and call the whole pool one."),
      L("Pipe A fills a twelfth of the pool an hour. In three hours, three twelfths, that's a quarter of the pool.",
        show(q3j, 'Pipe A fills a twelfth')),
      L("So what's left is one minus a quarter, three quarters of the pool.", show(q3k, 'one minus a quarter')),
      L("Together, a twelfth plus a sixth. A sixth is two twelfths, so together it's three twelfths.", show(q3l, "so together it's three twelfths")),
      L("Three twelfths is a quarter of the pool an hour.", show(q3m, 'Three twelfths is a quarter')),
      L("Three quarters of the pool, at a quarter an hour. That's three hours, the same answer.",
        show(q3n, 'Three quarters of the pool, at')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g101 (the dishwashers)
# Hebrew (wp 6383-6430, the scanners 4 fast = 2 x 6 slow): method 1 an equation, "give it to the poor one" (the approved
# English "give it to the little guy", taught in topic 22: a reminder here), many students double the bigger side;
# method 2 plugging in numbers ("I don't need to know where to start, I just start rolling"). Trap at its step: choice 1
# (the times two on the bigger side gives L = S).
g01a = IH('g01a', '$5L$ $\\ $and $\\ 10S$', size=30)
g01b = IH('g01b', '$5L=2\\cdot10S$', size=30)
g01c = IH('g01c', '$5L=20S$', size=30)
g01d = IH('g01d', '$L=4S$', size=30, col=1)
g01e = IH('g01e', '$2\\cdot5L=10S$: $\\ L=S$, $\\ $the trap', size=30, col=1)
g01f = IH('g01f', 'one small: $\\ 2$ plates a minute', size=30)
g01g = IH('g01g', '$10$ small: $\\ 10\\times2=20$ a minute', size=30)
g01h = IH('g01h', '$5$ large: $\\ 2\\times20=40$ a minute', size=30)
g01i = IH('g01i', 'one large: $\\ 40\\div5=8$ a minute', size=30, col=1)
g01j = IH('g01j', '$8\\div2=4$ times as fast', size=30, col=1)
video('solve-wp26-g101', 'solution', qid='wp26-g101', slides=[
    S('Method 1 · The math way: an equation',
      L("The combined rate of five large dishwashers is twice the combined rate of ten small dishwashers. Dishwashers "
        "of the same type are identical. How many times as fast is one large dishwasher as one small dishwasher?",
        pt('stem', 'The combined rate of five large', 'hl', 10.0), voice='calm', pause=0.5),
      L("So they compare the rate of one large dishwasher with the rate of one small one.",
        pt('stem: ask', 'So they compare the rate')),
      L("We'll solve it in two different ways. Let's start with the math way, with an equation. Let L be the rate of one "
        "large dishwasher, and S the rate of one small one."),
      L("The dishwashers of each type are identical. So five large ones have a rate of five L, and ten small ones have "
        "a rate of ten S.", show(g01a, 'five large ones have a rate')),
      L("Five L is twice ten S. So which side gets the times two? A lot of students double the bigger side, because it's "
        "the one that's twice as big."),
      L("Remember from topic twenty-two, give it to the little guy. Here that means the smaller combined rate, ten S. "
        "We want equal sides, so the times two goes on ten S, not five L. Doubling the smaller rate makes it equal "
        "to the larger one.", show(g01b, 'so the times two goes on ten S')),
      L("Two times ten S is twenty S. So five L is equal to twenty S.", show(g01c, 'Two times ten S is twenty S')),
      L("We divide both sides by five, so that one L is left alone. Twenty divided by five is four. So L is equal to "
        "four S.", show(g01d, 'We divide both sides by five')),
      L("Careful with choice number one. If we double five L, we get ten L is equal to ten S. Then L is equal to S, "
        "and that's one.", show(g01e, 'If we double five L'), mk('cross', 'choice 1', "and that's one")),
      L("So one large dishwasher is four times as fast as a small one. That's choice number four.")),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. We don't need to know where to start. We "
        "just pick a number, and follow the story."),
      L("Let's say one small dishwasher washes two plates a minute.", show(g01f, 'one small dishwasher washes two')),
      L("So ten small ones wash ten times two, twenty plates a minute.", show(g01g, 'ten times two, twenty')),
      L("The five large ones have twice that rate. Two times twenty is forty plates a minute.",
        show(g01h, 'Two times twenty is forty')),
      L("That's five large dishwashers together. So one large dishwasher washes forty divided by five, eight plates a "
        "minute.", show(g01i, 'forty divided by five')),
      L("One small one washes two, and one large one washes eight. Eight divided by two is four. So four times as "
        "fast.", show(g01j, 'Eight divided by two is four')),
      L("Choice number four is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g102 (the bakery queue)
# Hebrew (wp 6431-6531, the mole and the gardener): "let's start with some order", the digger x 5; the gardener's
# column is in minutes, "I must stay with the same units", 5 hours = 300 minutes, 75 -> 300 is x 4 (or the triangle
# value); the holes now + dug - covered; way 2: minutes to hours (75 minutes = 1 1/4 h). English keeps both and adds the
# net change every two hours (an insight), then (R37, a one-off taught here, about 2 minutes) catching up: the gap
# divided by the extra rate (real exam 2022_winter_q2_15, the popcorn machine; new numbers). Traps at their steps: 72
# (15 read as per hour), 40 minutes is not 0.4 hours, 30 / 16.
g02a = IH('g02a', 'customers: $\\ 18\\times4=72$', size=30)
g02b = IH('g02b', '$4$ hours $=4\\times60=240$ minutes', size=30)
g02c = IH('g02c', '$40\\times6=240$', size=30)
g02d = IH('g02d', 'the baker: $\\ 15\\times6=90$', size=30, col=1)
g02e = IH('g02e', '$60+72=132$', size=30, col=1)
g02f = IH('g02f', '$132-90=42$', size=30, col=1)
g02g = IH('g02g', '$60+72-60=72$: $\\ $the trap', size=30, col=1)
g02h = IH('g02h', '$40$ minutes $=\\frac{40}{60}=\\frac{2}{3}$ hour', size=30)
g02i = IH('g02i', 'not $0.4$ hours', size=30)
g02j = IH('g02j', '$\\frac{2}{3}\\times6=4$ hours', size=30, col=1)
g02k = IH('g02k', 'the baker: $\\ 15\\times6=90$', size=30, col=1)
g02k2 = IH('g02k2', '$60+72-90=42$', size=30, col=1)
g02l = IH('g02l', '$2$ hours $=120$ minutes $=3\\times40$', size=30)
g02m = IH('g02m', 'the baker: $\\ 3\\times15=45$', size=30)
g02n = IH('g02n', 'customers: $\\ 2\\times18=36$', size=30)
g02o = IH('g02o', '$45-36=9$ fewer every $2$ hours', size=30, col=1)
g02p = IH('g02p', '$4$ hours: $\\ 2\\times9=18$ fewer', size=30, col=1)
g02q = IH('g02q', '$60-18=42$', size=30, col=1)
g02r = I('g02r', 'Normally $6$ h a day. $\\ $Down $5$ days.', size=30)
g02s = I('g02s', 'Now $16$ h a day. $\\ $Caught up when?', size=30)
g02t = IH('g02t', 'behind: $\\ 5\\times6=30$ hours', size=30)
g02u = IH('g02u', 'extra a day: $\\ 16-6=10$ hours', size=30)
g02v = IH('g02v', '$30\\div10=3$ days', size=30, col=1)
g02w = IH('g02w', '$30\\div16$: $\\ $the trap', size=30, col=1)
g02x = I('g02x', 'Catching up: $\\ $gap $\\div$ extra rate', size=30, col=1)
video('solve-wp26-g102', 'solution', qid='wp26-g102', slides=[
    S('Method 1 · The math way: in minutes',
      L("Customers add eighteen orders to a bakery's queue each hour. The baker completes fifteen orders every forty "
        "minutes. There are sixty orders in the queue at the start. At these constant rates, how many orders are in the "
        "queue after four hours?", pt('stem', "Customers add eighteen orders", 'hl', 12.0), voice='calm', pause=0.5),
      L("So the customers add orders, and the baker takes orders away. They ask how many orders are left after four "
        "hours.", pt('stem: ask', 'They ask how many orders are left')),
      L("We'll solve it in three different ways. Let's start with the math way, and some order. First the customers. "
        "They add eighteen orders an hour, for four hours. Eighteen times four is seventy-two orders.",
        show(g02a, 'Eighteen times four is seventy-two')),
      L("Now the baker. Fifteen orders every forty minutes. That rate is in minutes. Like in the lesson, the units must "
        "match. So we turn the four hours into minutes. Four times sixty is two hundred forty minutes.",
        show(g02b, 'Four times sixty is two hundred forty')),
      L("Forty minutes to two hundred forty minutes is times six, because forty times six is two hundred forty.",
        show(g02c, 'because forty times six')),
      L("The rate is fixed, so the work goes the same way, times six. Fifteen times six is ninety orders.",
        show(g02d, 'Fifteen times six is ninety')),
      L("Now the queue. Sixty orders at the start, plus seventy-two new ones, is a hundred thirty-two.",
        show(g02e, 'plus seventy-two new ones')),
      L("The baker completed ninety. A hundred thirty-two minus ninety is forty-two.", show(g02f, 'A hundred thirty-two minus ninety')),
      L("Careful with seventy-two, choice number one. That's what we get if we read fifteen orders as fifteen an hour. "
        "Then the baker does only sixty.", show(g02g, 'Then the baker does only sixty'),
        mk('cross', 'choice 1', 'Then the baker does only sixty')),
      L("So forty-two orders are in the queue. That's choice number three.")),
    S('Method 2 · The math way: in hours',
      L("[pause] Now the math way again, but in hours. We start again from the givens. The customers add seventy-two "
        "orders, like before. Now we turn the baker's forty minutes into hours."),
      L("From minutes to hours, we divide by sixty. Forty over sixty is two thirds of an hour.",
        show(g02h, 'Forty over sixty is two thirds')),
      L("Careful, forty minutes isn't zero point four hours. An hour has sixty minutes, not a hundred.",
        show(g02i, "forty minutes isn't zero point four")),
      L("Two thirds of an hour to four hours is times six, because two thirds times six is four.",
        show(g02j, 'two thirds times six is four')),
      L("So the baker does fifteen times six, ninety orders again. And sixty plus seventy-two minus ninety is forty-two.",
        show(g02k, 'fifteen times six, ninety'), show(g02k2, 'And sixty plus seventy-two'))),
    S('Method 3 · Insight: the change every two hours',
      L("[pause] Now an insight. We start again from the givens. The customers and the baker work against each other. So "
        "let's see what happens to the queue in a short time where both numbers are whole."),
      L("Two hours is a hundred twenty minutes. That's three times forty minutes.", show(g02l, "That's three times forty")),
      L("So in two hours, the baker completes three times fifteen, forty-five orders.", show(g02m, 'three times fifteen')),
      L("In the same two hours, the customers add two times eighteen, thirty-six orders.", show(g02n, 'two times eighteen')),
      L("Forty-five minus thirty-six is nine. So the queue gets nine orders shorter every two hours.",
        show(g02o, 'Forty-five minus thirty-six')),
      L("Four hours is two times two hours. So two times nine, eighteen orders fewer.", show(g02p, 'So two times nine')),
      L("Sixty minus eighteen is forty-two. The same answer.", show(g02q, 'Sixty minus eighteen'))),
    S('The same idea: catching up',
      L("I want to use this question to show you one more tool from the same idea. When one rate works against another, "
        "only the difference counts."),
      L("A printer normally prints six hours a day. It was broken for five days. Now it prints sixteen hours a day. "
        "After how many days does it catch up?", show(g02r, 'A printer normally prints'), show(g02s, 'Now it prints sixteen')),
      L("First, how far behind is it? Five days, six hours a day. Five times six is thirty hours of printing.",
        show(g02t, 'Five times six is thirty')),
      L("Now it prints sixteen hours a day. But each day it still owes its normal six. So it gains only sixteen minus "
        "six, ten extra hours a day.", show(g02u, 'sixteen minus six')),
      L("Thirty hours behind, and ten extra hours a day. Thirty divided by ten is three days.", show(g02v, 'Thirty divided by ten')),
      L("A lot of students divide thirty by sixteen. But the normal work keeps coming every day. Only the extra part "
        "closes the gap.", show(g02w, 'divide thirty by sixteen')),
      L("So catching up is the gap divided by the extra rate. Choice number three was our answer, and I'll see you in "
        "the next question.", show(g02x, 'So catching up is the gap'), mk('tick', 'choice 3', 'Choice number three was our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t26-04 (the average rate)
# No Hebrew (a September addition; real exams 2019_spring_q2_19, 2020_spring_q1_20). A one-off here (R37, taught in this
# question): the average rate is the total work over the total time, NOT the average of the rates; the hours are the
# weights. The seesaw is a reminder from topic 25 (wp-086), built with its signature picture (V1). Trap at its step: 25.
q4a = IH('q4a', '$60\\div30=2$ hours', size=30)
q4b = IH('q4b', '$60\\div20=3$ hours', size=30)
q4c = IH('q4c', '$2+3=5$ hours', size=30)
q4d = IH('q4d', '$120\\div5=24$ an hour', size=30, col=1)
q4e = IH('q4e', '$\\frac{30+20}{2}=25$: $\\ $the trap', size=30, col=1)
q4f = I('q4f', 'Average rate $=\\dfrac{\\text{total work}}{\\text{total time}}$', size=32, col=1)
q4g = IH('q4g', '$3$ hours at $20$, $\\ 2$ hours at $30$', size=30)
q4h = IH('q4h', 'closer to $20$: $\\ $below $25$', size=30)
q4w = SAW('q4w', '20', '30', [
    ('vals', [('vals',)]), ('wts', [('wts', '3 h', '2 h'), ('heavy', 0)]), ('units', [('units', 5)]),
    ('pivot', [('pivot', 2, 5, '24'), ('dl', 2, 5, '4'), ('dr', 2, 5, '6')])], w=520, col=1)
q4i = IH('q4i', '$30-20=10$, $\\ 10\\div5=2$', size=30)
q4j = IH('q4j', '$20+2\\times2=24$', size=30)
video('solve-q-r26-t26-04', 'solution', qid='q-r26-t26-04', slides=[
    S('Method 1 · The math way: total work over total time',
      L("A machine makes sixty parts at a rate of thirty parts per hour, and then sixty more parts at a rate of twenty "
        "parts per hour. What is its average rate for all a hundred twenty parts, in parts per hour?",
        pt('stem', 'A machine makes sixty parts', 'hl', 10.0), voice='calm', pause=0.5),
      L("So the machine works at two different rates. They ask for one average rate for the whole job.",
        pt('stem: ask', 'They ask for one average rate')),
      L("We'll solve it in three different ways. Let's start with the math way. A rate is the work over the time. So the "
        "average rate is the total work, over the total time.", show(q4f, 'So the average rate is the total work')),
      L("The total work is a hundred twenty parts. Now the time. Sixty parts at thirty an hour. The time is the work "
        "divided by the rate. Sixty divided by thirty is two hours.", show(q4a, 'Sixty divided by thirty')),
      L("Sixty more parts at twenty an hour. Sixty divided by twenty is three hours.", show(q4b, 'Sixty divided by twenty')),
      L("So the total time is two plus three, five hours.", show(q4c, 'two plus three, five')),
      L("A hundred twenty parts in five hours. A hundred twenty divided by five is twenty-four parts an hour.",
        show(q4d, 'A hundred twenty divided by five')),
      L("Careful with twenty-five, choice number one. That's the average of thirty and twenty. But the machine doesn't "
        "spend the same time at each rate.", show(q4e, "That's the average of thirty"), mk('cross', 'choice 1', "doesn't spend the same time")),
      L("So the average rate is twenty-four parts an hour. That's choice number two.")),
    S('Method 2 · Estimation',
      L("[pause] Now let's estimate. We start again from the givens. Sixty divided by twenty is three hours. Sixty "
        "divided by thirty is two hours. So the machine works three hours at twenty, and only two hours at thirty.",
        show(q4g, 'So the machine works three hours at twenty')),
      L("It spends more time at the slow rate. So the average is closer to twenty than to thirty. That means it's below "
        "twenty-five.", show(q4h, 'So the average is closer to twenty')),
      L("So twenty-five, choice number one, is out. And fifty, choice number three, is more than both rates, so it's out "
        "too.", mk('cross', 'choice 1', 'choice number one, is out'), mk('cross', 'choice 3', 'is more than both rates')),
      L("Twenty-two or twenty-four are left. The estimate can't decide between them, so let's use the seesaw.")),
    S('Method 3 · Understanding: the seesaw',
      L("[pause] Remember the seesaw from averages. The hours are the weights here. So we put the two rates at the ends, "
        "twenty and thirty.", show(q4w['line'], 'So we put the two rates'), show(q4w['vals'], 'twenty and thirty')),
      L("Twenty has a weight of three hours, and thirty has a weight of two hours. So twenty is the heavy side.",
        show(q4w['wts'], 'Twenty has a weight of three')),
      L("Three plus two is five, so we cut the gap into five equal units. The gap is thirty minus twenty, ten. Ten divided "
        "by five is two. So each unit is two.", show(q4w['units'], 'we cut the gap into five'), show(q4i, 'Ten divided by five')),
      L("The pivot is closer to the heavy side. It's two units from twenty, and three units from thirty.",
        show(q4w['pivot'], 'The pivot is closer to the heavy side')),
      L("Two units is two times two, four. Twenty plus four is twenty-four. The same answer.", show(q4j, 'Twenty plus four')),
      L("So whenever they ask for an average rate, we divide the total work by the total time. The plain average of the "
        "rates works only when the times are equal. Otherwise, the answer is closer to the rate with more time."),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g103 (the polishers)
# Hebrew (wp 6532-6610, the lawn mowers 300 m² in 2 h and 50 m² in 3 h, 100 m² together): equal times (6 h: 900 + 100 =
# 1,000 m² in 360 minutes -> 36 minutes), "the trivial way, what we'd expect you to solve"; then an estimate: mower A
# alone 100 m² in 40 minutes, so together less than 40; two such mowers would take 20; B helps "but just a little",
# the elephant and the mouse ("look how much dust we're making"). English keeps both (12 hours here; the range check of
# wp-094). Minutes from A's 200 m² in 240 minutes: 10 m² in 12 minutes, 110 m² in 132 minutes.
g03t = TBL('g03t', ['m²', 'hours'], ['A', 'A', 'B', 'B', 'together'], [
    ('r1', [('c', 0, 0, '200'), ('c', 0, 1, '4')]), ('r3', [('c', 2, 0, '30'), ('c', 2, 1, '6')]),
    ('h', [('c', 1, 1, '12'), ('c', 3, 1, '12')]),
    ('a', [('down', 1, 0, 1, '×3'), ('c', 1, 0, '600')]), ('b', [('down', 1, 2, 3, '×2'), ('c', 3, 0, '60')]),
    ('s', [('c', 4, 0, '660'), ('c', 4, 1, '12')])], colw=130, labw=150, rowh=54, side=70, w=480, col=1)
g03a = IH('g03a', '$660\\div6=110$', size=30)
g03b = IH('g03b', '$12\\div6=2$ hours', size=30)
g03c = IH('g03c', '$2$ hours $=120$ minutes', size=30)
g03d = IH('g03d', 'A: $\\ 200$ in $240$ minutes', size=30)
g03e = IH('g03e', '$\\div20$: $\\ 10$ in $12$ minutes', size=30)
g03f = IH('g03f', '$110$: $\\ 11\\times12=132$ minutes', size=30)
g03g = IH('g03g', 'together: $\\ $less than $132$', size=30, col=1)
g03h = IH('g03h', 'two like A: $\\ 132\\div2=66$', size=30, col=1)
g03i = IH('g03i', 'B is slow: $\\ $more than $66$', size=30, col=1)
g03j = IH('g03j', 'between $66$ and $132$: $\\ 120$', size=30, col=1)
video('solve-wp26-g103', 'solution', qid='wp26-g103', slides=[
    S('Method 1 · The math way: equal times',
      L("Polisher A polishes two hundred square meters of floor in four hours. Polisher B polishes thirty square meters "
        "in six hours. Working together at these constant rates, how many minutes do they need for a hundred ten square "
        "meters?", pt('stem', 'Polisher A polishes two hundred', 'hl', 11.0), voice='calm', pause=0.5),
      L("So two polishers work together. They ask for minutes, for a hundred ten square meters.",
        pt('stem: ask', 'They ask for minutes')),
      L("We'll solve it in two different ways. Let's start with the math way, with equal times, like in the lesson.",
        show(g03t['line'], 'with equal times')),
      L("Polisher A does two hundred square meters in four hours. Polisher B does thirty in six hours.",
        show(g03t['r1'], 'Polisher A does two hundred'), show(g03t['r3'], 'Polisher B does thirty')),
      L("The times are different, so we need a time that four and six both divide. That's twelve hours.",
        show(g03t['h'], "That's twelve hours")),
      L("Four hours to twelve is times three. Two hundred times three is six hundred square meters.", show(g03t['a'], 'Four hours to twelve')),
      L("Six hours to twelve is times two. Thirty times two is sixty square meters.", show(g03t['b'], 'Six hours to twelve')),
      L("In the same twelve hours, together they polish six hundred plus sixty, six hundred sixty square meters.",
        show(g03t['s'], 'six hundred plus sixty')),
      L("They want a hundred ten. Six hundred sixty divided by six is a hundred ten. So the work is divided by six.",
        show(g03a, 'Six hundred sixty divided by six')),
      L("The rate is fixed, so the time is divided by six too. Twelve divided by six is two hours.",
        show(g03b, 'Twelve divided by six')),
      L("They ask for minutes. Two hours is a hundred twenty minutes. That's choice number one.",
        show(g03c, 'Two hours is a hundred twenty'))),
    S('Method 2 · Estimation',
      L("[pause] Now let's estimate, and rule out choices. We start again from the givens. First, polisher A alone."),
      L("Polisher A does two hundred square meters in four hours. Four hours is two hundred forty minutes.",
        show(g03d, 'Four hours is two hundred forty')),
      L("We divide both by twenty. So ten square meters in twelve minutes.", show(g03e, 'We divide both by twenty')),
      L("A hundred ten is eleven times ten. So eleven times twelve, a hundred thirty-two minutes, for polisher A alone.",
        show(g03f, 'eleven times twelve')),
      L("Like in the lesson, together is faster than A alone. So less than a hundred thirty-two minutes.",
        show(g03g, 'So less than a hundred thirty-two')),
      L("So choice number three, a hundred thirty-two, is out. And choice number four, a hundred fifty, is out.",
        mk('cross', 'choice 3', 'a hundred thirty-two, is out'), mk('cross', 'choice 4', 'a hundred fifty, is out')),
      L("Two polishers as fast as A would need half the time. A hundred thirty-two divided by two is sixty-six minutes.",
        show(g03h, 'A hundred thirty-two divided by two')),
      L("But polisher B is much slower. It does only thirty square meters in six hours. It helps, but only a little.",
        show(g03i, 'polisher B is much slower')),
      L("It's like the joke about the elephant and the mouse. They walk together, and the mouse says, look how much dust "
        "we're making."),
      L("So together it's more than sixty-six minutes. Choice number two is out.", mk('cross', 'choice 2', 'Choice number two is out')),
      L("Between sixty-six and a hundred thirty-two, only a hundred twenty is left.", show(g03j, 'only a hundred twenty is left')),
      L("Choice number one is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g104 (Omar, Priya and Sam)
# Hebrew (wp 6611-6724, Aviva, Batya and Geula 6 h / 12 h): "I don't know which part Batya does and which part Aviva
# does ... it doesn't matter to me" (Batya with a coffee while Aviva works), the two are like one worker, "Avivatya"
# (the approved English: a blended name, here "Omarpriya", said as one word), then equal times (12 h: all three 2 jobs,
# Avivatya 1, Geula the other); the insight: in 6 hours Avivatya does half, so Geula does the other half, Geula is as
# fast as the two together. English keeps both (a one-off trick taught here, R37) and adds the rates subtracted.
g04a = I('g04a', 'Omar $+$ Priya $=$ Omarpriya', size=32)
g04b = IH('g04b', 'all three: $\\ 1$ job in $9$ hours', size=30)
g04c = IH('g04c', 'Omarpriya: $\\ 1$ job in $18$ hours', size=30)
g04d = IH('g04d', 'all three: $\\ 2$ jobs in $18$ hours', size=30)
g04e = IH('g04e', 'Sam: $\\ 2-1=1$ job in $18$ hours', size=30, col=1)
g04f = IH('g04f', 'Sam: $\\ \\frac{1}{18}$ of the job an hour', size=30, col=1)
g04g = IH('g04g', '$9$ hours: $\\ $Omarpriya does $\\frac{1}{2}$', size=30)
g04h = IH('g04h', 'Sam: $\\ $the other $\\frac{1}{2}$ in $9$ hours', size=30)
g04i = IH('g04i', 'Sam: $\\ 1$ job in $18$ hours', size=30)
g04j = IH('g04j', '$\\frac{1}{9}-\\frac{1}{18}=\\frac{2}{18}-\\frac{1}{18}$', size=30)
g04k = IH('g04k', '$=\\frac{1}{18}$', size=30)
video('solve-wp26-g104', 'solution', qid='wp26-g104', slides=[
    S('Method 1 · The math way: equal times',
      L("Omar, Priya and Sam each work at a constant rate. Together they complete a job in nine hours. Omar and Priya "
        "together complete it in eighteen hours. What fraction of the job does Sam complete in one hour?",
        pt('stem', 'Omar, Priya and Sam each work', 'hl', 10.0), voice='calm', pause=0.5),
      L("So they ask for Sam's rate, the part of the job he does in one hour.", pt('stem: ask', "So they ask for Sam's rate")),
      L("We'll solve it in three different ways. This time there are three workers, and that's what makes it hard. So "
        "I want to use this question to show you a trick that turns three workers into two."),
      L("Omar and Priya together do one job in eighteen hours. Do we care how they split the work? Not really.",
        pt('stem: given', 'Omar and Priya together do one job')),
      L("Maybe they share it equally. Maybe Priya sits with a coffee, and Omar does everything. Together they still do "
        "one job in eighteen hours."),
      L("So they're like one worker. Let's give them one name, Omarpriya. Now it's a normal question with two workers, "
        "Omarpriya and Sam.", show(g04a, "Let's give them one name")),
      L("This works whenever a question gives the time of two workers together. We treat the two as one worker, with one "
        "rate."),
      L("Now the math way, with equal times, like in the lesson. All three do one job in nine hours.",
        show(g04b, 'All three do one job in nine hours')),
      L("Omarpriya does one job in eighteen hours.", show(g04c, 'Omarpriya does one job in eighteen')),
      L("The times are different. Nine to eighteen is times two. So in eighteen hours, all three do two jobs.",
        show(g04d, 'all three do two jobs')),
      L("Omarpriya does one of the two jobs. So Sam does the other one. Two minus one is one job in eighteen hours.",
        show(g04e, 'Two minus one is one job')),
      L("So in one hour, Sam does one eighteenth of the job.", show(g04f, 'Sam does one eighteenth')),
      L("So that's choice number three.")),
    S('Method 2 · Insight',
      L("[pause] Now the insight. We start again from the givens. All three work for nine hours, and finish the job."),
      L("Omarpriya needs eighteen hours for a whole job. Nine hours is half of that. So in nine hours, Omarpriya does half "
        "the job.", show(g04g, 'So in nine hours, Omarpriya does half')),
      L("So Sam does the other half, in the same nine hours.", show(g04h, 'So Sam does the other half')),
      L("Half a job in nine hours means a whole job in eighteen hours. So Sam alone is as fast as Omar and Priya "
        "together. And his rate is one eighteenth.", show(g04i, 'a whole job in eighteen hours'))),
    S('Method 3 · The math way: subtract the rates',
      L("[pause] And the math way with rates. We start again from the givens. All three together do a ninth of the job an "
        "hour. Omarpriya does an eighteenth."),
      L("Sam's rate is what's left. A ninth minus an eighteenth. A ninth is two eighteenths. So two eighteenths minus one "
        "eighteenth.", show(g04j, 'A ninth minus an eighteenth')),
      L("That's one eighteenth of the job an hour.", show(g04k, "That's one eighteenth of the job")),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g105 (the stage and the seating)
# Hebrew (wp 6725-6858, 10 carpenters a table in 3 h, 9 a chair in 5 h, both in 15 h): two teams working at the same
# time; way 1 the V (10 . 1 . 3 / 15 = 2; 9 . 1 . 5 / 15 = 3); way 2 ratios, "faster here": one thing changes, more time
# -> fewer workers, "send the rest home"; way 3 worker-hours, apart and together (75 / 15 = 5). English keeps all three
# (wp-097 and wp-099 taught them; "like in the lesson"). Trap at its step: 26 = 12 + 14.
g05t = VT('g05t', ('12', '1', '2'), ('?', '1', '8'), col=1, w=500)
g05u = VT('g05u', ('14', '1', '4'), ('?', '1', '8'), col=1, w=500)
g05a = IH('g05a', 'stage: $\\ \\frac{12\\cdot1\\cdot2}{1\\cdot8}=\\frac{24}{8}=3$', size=30)
g05b = IH('g05b', 'seating: $\\ \\frac{14\\cdot1\\cdot4}{1\\cdot8}=\\frac{56}{8}=7$', size=30)
g05c = IH('g05c', '$3+7=10$ workers', size=30)
g05d = IH('g05d', 'stage: $\\ 2$ to $8$ hours, $\\ \\times4$', size=30)
g05e = IH('g05e', '$12\\div4=3$ workers', size=30)
g05f = IH('g05f', 'seating: $\\ 4$ to $8$ hours, $\\ \\times2$', size=30)
g05g = IH('g05g', '$14\\div2=7$ workers', size=30)
g05h = IH('g05h', '$3+7=10$', size=30)
g05i = IH('g05i', 'stage: $\\ 12\\times2=24$ worker hours', size=30)
g05j = IH('g05j', 'seating: $\\ 14\\times4=56$ worker hours', size=30)
g05k = IH('g05k', '$24+56=80$ worker hours', size=30)
g05l = IH('g05l', '$80\\div8=10$ workers', size=30)
CARRY26['solve-wp26-g105'] = {1: ['stage: $\\ 3$ workers']}
video('solve-wp26-g105', 'solution', qid='wp26-g105', slides=[
    S('Method 1 · The math way: the V method',
      L("Twelve identical workers can set up one stage in two hours. Fourteen such workers can set up the seating in four "
        "hours. How many workers are needed to set up one stage and the seating in eight hours?",
        pt('stem', 'Twelve identical workers can set up', 'hl', 10.0), voice='calm', pause=0.5),
      L("Identical workers, in a group, so it's a team question. They ask for the number of workers.",
        pt('stem: ask', 'They ask for the number of workers')),
      L("But careful, there are two jobs. One team sets up the stage, and another team sets up the seating. Both teams "
        "work at the same time, during the same eight hours."),
      L("We'll solve it in three different ways. Let's start with the math way, with the V method. First the stage. Row "
        "one is twelve workers, one stage, two hours. Row two is the question mark, one stage, eight hours.",
        show(g05t['line'], 'First the stage'), show(g05t['r1'], 'Row one is twelve workers'), show(g05t['r2'], 'Row two is the question mark')),
      L("The question mark is in the team. So the V joins twelve, one and two. We multiply them, and divide by the other "
        "two, one and eight.", show(g05t['v'], 'So the V joins twelve'), show(g05t['calc'], 'and divide by the other two')),
      L("Twelve times one times two is twenty-four. Twenty-four divided by eight is three workers.", show(g05a, 'Twenty-four divided by eight')),
    ),
    S('Method 1 · The math way: the V method',
      L("Now the seating. Fourteen workers, one seating, four hours. And the question mark, one seating, eight hours.",
        show(g05u['line'], 'Now the seating'), show(g05u['r1'], 'Fourteen workers, one seating'), show(g05u['r2'], 'And the question mark')),
      L("The V joins fourteen, one and four. Fourteen times one times four is fifty-six. Fifty-six divided by eight is "
        "seven workers.", show(g05u['v'], 'The V joins fourteen'), show(g05b, 'Fifty-six divided by eight')),
      L("Three workers on the stage, and seven on the seating, at the same time. Three plus seven is ten workers.",
        show(g05c, 'Three plus seven is ten')),
      L("Careful with twenty-six, choice number one. That's twelve plus fourteen, the workers from the givens. But with "
        "eight hours, we need fewer workers.", mk('cross', 'choice 1', 'we need fewer workers')),
      L("So ten workers. That's choice number two.")),
    S('Method 2 · Understanding: ratios',
      L("[pause] Now by understanding, with ratios. We start again from the givens. Like in the lesson, here only one thing "
        "changes, the time. The job stays the same. So ratios are quick."),
      L("The stage took two hours, and now we have eight. Two to eight is times four.", show(g05d, 'Two to eight is times four')),
      L("More time means fewer workers. That's the opposite way, so we divide the workers by four. Twelve divided by four "
        "is three.", show(g05e, 'Twelve divided by four')),
      L("The seating took four hours, and now we have eight. That's times two.", show(g05f, "That's times two")),
      L("So half the workers. Fourteen divided by two is seven. And we send the rest home.", show(g05g, 'Fourteen divided by two')),
      L("Three plus seven is ten workers again.", show(g05h, 'Three plus seven is ten workers again'))),
    S('Method 3 · The math way: worker-hours',
      L("[pause] And the math way with worker-hours, like in the lesson. We start again from the givens. Think of the boss "
        "who pays by the hour."),
      L("The stage takes twelve workers for two hours. Twelve times two is twenty-four worker-hours.",
        show(g05i, 'Twelve times two is twenty-four')),
      L("The seating takes fourteen workers for four hours. Fourteen times four is fifty-six worker-hours.",
        show(g05j, 'Fourteen times four is fifty-six')),
      L("Both jobs together need twenty-four plus fifty-six, eighty worker-hours.", show(g05k, 'twenty-four plus fifty-six')),
      L("We have eight hours. So we need eighty divided by eight, ten workers.", show(g05l, 'eighty divided by eight')),
      L("Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ g105b (the hay)
# Hebrew (wp 6859-6981, the water tower: 220 dunams for 5 days -> 100 dunams): "this time I'll start, on purpose, with
# the psychometric way, an estimate" (less land lasts longer, and all the choices are more than 5 days; 110 is half of
# 220 -> 10 days; 100 is a bit less -> a bit more than 10 -> the estimate alone picks 11; "why the estimate? 100 is
# almost half, the half is easy to compute"); way 2 plugging in numbers (each dunam "drinks" a liter a day: 1,100 liters
# / 100 = 11); way 3 the team question: "who is the team and who is the work?" - the trees are the workers, their job is
# drinking, the water is the work and it doesn't change (5 . 1 . 220 / 100). "There are such questions lately." English
# keeps the three, in her order. W23 (2026-10-22): 150 sheep -> 90 sheep, so that her half-benchmark lands next to the
# answer again (100 sheep -> 18 days; 90 a bit fewer -> a bit more than 18 -> 20) and the estimate decides by itself.
g5ba = IH('g5ba', 'fewer sheep: $\\ $more than $9$ days', size=30)
g5bb = IH('g5bb', '$200\\div2=100$ sheep: $\\ 9\\times2=18$ days', size=30)
g5bc = IH('g5bc', '$90$ sheep: $\\ $a bit more than $18$', size=30)
g5bl = IH('g5bl', '$27=18+9$: $\\ $far too much', size=30, col=1)
g5bd = IH('g5bd', 'each sheep: $\\ 1$ unit a day', size=30)
g5be = IH('g5be', '$200\\times9=1800$ units', size=30)
g5bf = IH('g5bf', '$90$ sheep: $\\ 90$ units a day', size=30)
g5bg = IH('g5bg', '$1800\\div90=20$ days', size=30)
g5bh = IH('g5bh', '$90\\times20=1800$', size=30)
g5bt = VT('g5bt', ('200', '1', '9'), ('90', '1', '?'), col=1)
g5bi = IH('g5bi', '$?=\\frac{200\\cdot1\\cdot9}{1\\cdot90}$', size=30)
g5bj = IH('g5bj', '$\\frac{200}{90}=\\frac{20}{9}$', size=30)
g5bk = IH('g5bk', '$\\frac{20}{9}\\cdot9=20$ days', size=30)
video('solve-wp26-g105b', 'solution', qid='wp26-g105b', slides=[
    S('Method 1 · Estimation',
      L("A supply of hay is enough for two hundred identical sheep for nine days. Each sheep eats the same constant amount "
        "per day. For how many days would that supply feed ninety sheep?",
        pt('stem', 'A supply of hay is enough', 'hl', 9.0), voice='calm', pause=0.5),
      L("So the hay stays the same, and the number of sheep changes. They ask for the number of days.",
        pt('stem: ask', 'They ask for the number of days')),
      L("We'll solve it in three different ways. This time I'll start, on purpose, with an estimate. It helps us "
        "understand the question, because this one isn't simple."),
      L("Fewer sheep eat the same hay more slowly. So the hay lasts longer, more than nine days.", show(g5ba, 'So the hay lasts longer')),
      L("And really, all four choices are more than nine days. So the question is how many more."),
      L("Ninety is close to a hundred, and a hundred is exactly half of two hundred. Half is the easiest to work with, so "
        "let's go through it first."),
      L("Half of two hundred is a hundred. Half the sheep make the hay last twice as long. Nine times "
        "two is eighteen days.", show(g5bb, 'Half of two hundred is a hundred')),
      L("But we have ninety sheep, a bit fewer than a hundred. Fewer sheep make the hay last longer. So a bit more than "
        "eighteen days.", show(g5bc, 'a bit fewer than a hundred')),
      L("So eighteen, choice number two, is out. And fifteen, choice number one, is fewer than eighteen, so it's out too.",
        mk('cross', 'choice 2', 'So eighteen, choice number two'), mk('cross', 'choice 1', "so it's out too")),
      L("Twenty and twenty-seven are left. Ninety sheep are only ten fewer than a hundred, a small change. So the days grow "
        "only a little above eighteen. Twenty-seven is nine days more than eighteen, half as much again. That's far too "
        "much, so twenty-seven is out.", show(g5bl, 'Twenty-seven is nine days more'), mk('cross', 'choice 4', 'so twenty-seven is out')),
      L("So the estimate alone picks twenty, choice number three. Now let's see two exact ways.")),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. The amount each sheep eats isn't given. So "
        "let's say each sheep eats one unit of hay a day.", show(g5bd, 'each sheep eats one unit')),
      L("Two hundred sheep for nine days. Two hundred times nine is one thousand eight hundred units. That's all the hay.",
        show(g5be, 'Two hundred times nine')),
      L("Ninety sheep eat ninety units a day.", show(g5bf, 'Ninety sheep eat')),
      L("One thousand eight hundred divided by ninety. We can drop a zero from both numbers. A hundred eighty divided by "
        "nine is twenty. So twenty days.", show(g5bg, 'One thousand eight hundred divided by')),
      L("Let's check it. Ninety times twenty is one thousand eight hundred. That's all the hay.",
        show(g5bh, 'Ninety times twenty')),
      L("So twenty days. That's choice number three, just like the estimate.")),
    S('Method 3 · The math way: the V method',
      L("[pause] And this is even a team question, once we see who the team is. We start again from the givens."),
      L("The sheep are the workers. Their job is eating. The hay is the work, and the hay doesn't change. So the work is "
        "one supply in both rows.", show(g5bt['line'], 'The sheep are the workers'), show(g5bt['r1'], 'The hay is the work'),
        show(g5bt['r2'], 'one supply in both rows')),
      L("The question mark is in the time. So the V joins two hundred, one and nine. We divide by the rest, one and "
        "ninety.", show(g5bt['v'], 'So the V joins two hundred'), show(g5bt['calc'], 'We divide by the rest'),
        show(g5bi, 'one and ninety')),
      L("Two hundred over ninety is twenty ninths, because we divide both by ten.", show(g5bj, 'Two hundred over ninety')),
      L("Twenty ninths times nine. The nine cancels the ninth, and that leaves twenty days.",
        show(g5bk, 'Twenty ninths times nine')),
      L("The hard part was to see who the team is. Sometimes a supply gets used up at a constant rate, like hay, water or "
        "fuel. Then the ones who use it are the team. And the supply is the work. If you don't see it, the estimate and plugging in "
        "numbers work too."),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ r26-t26-factors (lesson)
# No Hebrew (an English addition: the general form of her "direct or inverse" lesson and of the ratios in team
# questions; real exams 2024_spring_q2_02, 2023_winter_q1_16, 2020_winter_q1_16). The camera lesson part 3 already taught
# two changes (multiply, flip the opposite way); here R37 makes it a general tool with 3 worked cases: Lia and Ben (only
# relations given), the car (a tank and fuel per kilometer), the cooks of wp-097 again (the V = this rule), and its
# limit (a fixed amount more is not a factor -> an equation). The first question that uses it is q-r26-t26-21.
f6a0 = I('f6a0', 'Lia: $\\ \\frac{3}{4}$ of Ben\'s hours a day, $\\ \\frac{2}{3}$ of his work an hour', size=32)
f6a1 = I('f6a1', 'Ben: $\\ 8$ days. $\\ $Lia?', size=34)
f6a2 = IH('f6a2', 'a day $=$ hours a day $\\times$ work an hour', size=32)
f6a3 = IH('f6a3', '$\\frac{3}{4}\\times\\frac{2}{3}=\\frac{6}{12}=\\frac{1}{2}$', size=34)
f6a4 = IH('f6a4', 'half each day: $\\ 8\\times2=16$ days', size=34)
f6b1 = I('f6b1', 'New $=$ old $\\times$ every factor that changed', size=34)
f6b2 = I('f6b2', 'The same way: $\\ $as it is. $\\ $Opposite: $\\ $flip it.', size=34)
f6b3 = IH('f6b3', 'days: $\\ 8\\times\\frac{4}{3}\\times\\frac{3}{2}$', size=34, col=1)
f6b4 = IH('f6b4', '$\\frac{4}{3}\\times\\frac{3}{2}=2$', size=34, col=1)
f6b5 = IH('f6b5', '$8\\times2=16$ days', size=34, col=1)
f6b6 = I('f6b6', 'The same for both: $\\ $it cancels', size=34, col=1)
f6c0 = I('f6c0', '$600$ km. $\\ $The tank $\\times\\frac{3}{2}$, $\\ $fuel a km $\\times\\frac{3}{4}$', size=32)
f6c1 = IH('f6c1', 'bigger tank: $\\ $the same way, $\\ \\times\\frac{3}{2}$', size=32)
f6c2 = IH('f6c2', 'less fuel a km: $\\ $opposite, $\\ \\times\\frac{4}{3}$', size=32)
f6c3 = IH('f6c3', '$600\\times\\frac{3}{2}=900$', size=34, col=1)
f6c4 = IH('f6c4', '$900\\div3=300$, $\\ 300\\times4=1200$ km', size=34, col=1)
f6d1 = IH('f6d1', 'the cooks: $\\ 2\\times\\frac{4}{3}\\times\\frac{3}{2}=4$', size=34)
f6d2 = I('f6d2', 'The V $=$ this rule, $\\ $in a table', size=34)
f6e1 = I('f6e1', 'Lia: $\\ 2$ more boxes an hour than Ben', size=34)
f6e2 = IH('f6e2', '$10$ and $12$: $\\ 20\\%$ more', size=32)
f6e3 = IH('f6e3', '$4$ and $6$: $\\ 50\\%$ more', size=32)
f6e4 = IH('f6e4', 'Ben: $\\ x$, $\\ $Lia: $\\ x+2$: $\\ $an equation', size=32)
f6e5 = I('f6e5', 'times, as many as, a fraction of, a percent of: $\\ $factors', size=30)
f6e6 = I('f6e6', 'Fixed amount more: multiplier still unknown; an equation can help', size=30)
f6s1 = I('f6s1', 'Only relations given: $\\ $multiply the factors', size=34)
f6s2 = I('f6s2', 'The same way: $\\ $as it is. $\\ $Opposite: $\\ $flipped. $\\ $Shared: $\\ $gone.', size=32)
f6s3 = I('f6s3', 'Unknown starting value + fixed amount more: no fixed multiplier yet', size=30)
video('r26-t26-factors', 'lesson', slides=[
    S('Compare by Factors',
      L("Now a general tool, compare by factors."),
      L("In the first lesson, we multiplied the factors when two things changed. Many exam questions give only "
        "relations, like three quarters as many, or twice as fast. This tool solves them in one line, with no "
        "equations.")),
    S('Only relations are given',
      L("Lia works three quarters as many hours a day as Ben. In each hour, she does two thirds of what he does.",
        show(f6a0, 'Lia works three quarters')),
      L("Ben finishes a job in eight days. How many days does Lia need?", show(f6a1, 'Ben finishes a job in eight days')),
      L("We don't know Ben's real hours, or his real rate. And we don't need them."),
      L("First, how much does Lia do in one day? A day of work is the hours a day, times the work in each hour.",
        show(f6a2, 'A day of work is the hours a day')),
      L("Her hours are times three quarters. Her work in each hour is times two thirds. Three quarters times two thirds. "
        "Three times two is six. Then four times three is twelve. Six twelfths is a half.", show(f6a3, 'Six twelfths is a half')),
      L("Why multiply, and not add? Because each change scales what is already there. She works fewer hours, and in each "
        "hour she does less."),
      L("So each day, Lia does half of what Ben does. The job is the same, so the days go the opposite way. Half as much "
        "each day means twice as many days. Eight times two is sixteen days.", show(f6a4, 'Eight times two is sixteen'))),
    S('The rule',
      L("So here's the rule. We start from the old value, and multiply by every factor that changed.",
        show(f6b1, 'multiply by every factor that changed')),
      L("For each factor, we ask one question. When it grows, does my answer grow too? If yes, we multiply as it is. If "
        "no, we flip it.", show(f6b2, 'For each factor')),
      L("Let's do Lia in one line. We want the days. More hours a day means fewer days. That's opposite, so three "
        "quarters flips to four thirds."),
      L("More work each hour also means fewer days. So two thirds flips to three halves.",
        show(f6b3, 'two thirds flips to three halves')),
      L("Four thirds times three halves is two, because the threes cancel and four over two is two.", show(f6b4, 'Four thirds times three halves')),
      L("So eight times two, sixteen days. The same answer, in one line.", show(f6b5, 'So eight times two')),
      L("And the size of the job is the same for both, so it cancels. We never need it.", show(f6b6, 'it cancels'))),
    S('Another example',
      L("A car drives six hundred kilometers on a full tank. A new car's tank is one and a half times as big. And it "
        "uses three quarters as much fuel for each kilometer. How far does the new car drive on a full tank?",
        show(f6c0, 'A car drives six hundred kilometers')),
      L("We want the distance. A bigger tank means a longer drive. That's the same way, so times three halves.",
        show(f6c1, 'A bigger tank means a longer drive')),
      L("Less fuel for each kilometer also means a longer drive. So when the fuel goes down, the distance goes up. "
        "That's the opposite way, so three quarters flips to four thirds.", show(f6c2, 'Less fuel for each kilometer')),
      L("Six hundred times three halves. Half of six hundred is three hundred, times three is nine hundred.",
        show(f6c3, 'Six hundred times three halves')),
      L("Nine hundred times four thirds. Nine hundred divided by three is three hundred. Then three hundred times four is "
        "twelve hundred kilometers.", show(f6c4, 'Nine hundred divided by three')),
      L("Does it make sense? Both changes make the drive longer, so the answer must be more than six hundred. And "
        "twelve hundred is more.")),
    S('The V is the same rule',
      L("We've seen this rule before. In the team lesson, the cooks went from six to four, and the pies from thirty to "
        "forty. With ratios, we multiplied two hours by four thirds, and by three halves. That's four hours.",
        show(f6d1, 'With ratios, we multiplied two hours')),
      L("That was exactly this rule. The V just does the flipping for us, in a table of team, work and time.",
        show(f6d2, 'That was exactly this rule'))),
    S("When it doesn't work",
      L("One limit. Every change must be a times change."),
      L("Say Lia packs two more boxes an hour than Ben.", show(f6e1, 'Lia packs two more boxes')),
      L("If Ben packs ten, Lia packs twelve. Two more than ten is twenty percent more.", show(f6e2, 'If Ben packs ten')),
      L("But if Ben packs four, Lia packs six. Two more than four is fifty percent more.", show(f6e3, 'But if Ben packs four')),
      L("So the factor depends on Ben's real number, and we don't know it. Here we give Ben's rate a letter, x. Lia's rate "
        "is x plus two, and we write an equation.", show(f6e4, "Here we give Ben's rate a letter")),
      L("So look at the words. Times, as many as, a fraction of, or a percent of, are factors.", show(f6e5, 'So look at the words')),
      L("If we only know a fixed amount more, we don't yet know the multiplier. An equation can help us find it.",
        show(f6e6, "we don't yet know the multiplier"))),
    S('Recap',
      L("So let's sum it up. When only relations are given, we multiply the old value by every factor that changed.",
        show(f6s1, 'When only relations are given')),
      L("The same way, as it is. The opposite way, flipped. And what is the same for both cancels.",
        show(f6s2, 'The same way, as it is')),
      L("A fixed amount more doesn't give a fixed multiplier when the starting value is unknown. Then an equation "
        "can help.", show(f6s3, 'A fixed amount more')),
      L("Take a moment to memorize this, and I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ q-r26-t26-21 (Dana's notebooks)
# No Hebrew (an English addition; real exams 2023_winter_q1_16, 2020_winter_q1_16). The first question after the
# factors lesson: compare by factors applied slowly ("like in the lesson"), then plugging in numbers (a price of 10, so
# the budget is 300). Traps at their steps: 54 (the price not flipped), 21 (the percents added).
q21a = I('q21a', 'notebooks $=$ budget $\\div$ price', size=32)
q21b = IH('q21b', 'budget $\\times1.2=\\times\\frac{6}{5}$: $\\ $the same way', size=30)
q21c = IH('q21c', 'price $\\times\\frac{3}{2}$: $\\ $opposite, $\\ \\times\\frac{2}{3}$', size=30)
q21d = IH('q21d', '$30\\times\\frac{6}{5}\\times\\frac{2}{3}$', size=30, col=1)
q21e = IH('q21e', '$30\\div5=6$', size=30, col=1)
q21e2 = IH('q21e2', '$6\\times6=36$', size=30, col=1)
q21f = IH('q21f', '$36\\div3=12$', size=30, col=1)
q21f2 = IH('q21f2', '$12\\times2=24$', size=30, col=1)
q21g = IH('q21g', '$36\\times\\frac{3}{2}=54$: $\\ $not flipped', size=30)
q21h = IH('q21h', '$20\\%-50\\%=-30\\%$: $\\ 21$, $\\ $the trap', size=30)
q21i = IH('q21i', 'price $10$: $\\ $budget $30\\times10=300$', size=30)
q21j = IH('q21j', 'budget $300+60=360$', size=30)
q21k = IH('q21k', 'price $10\\times1.5=15$', size=30)
q21l = IH('q21l', '$360\\div15=24$', size=30)
CARRY26['solve-q-r26-t26-21'] = {1: ['$30\\times\\frac{6}{5}\\times\\frac{2}{3}=24$']}
video('solve-q-r26-t26-21', 'solution', qid='q-r26-t26-21', slides=[
    S('Method 1 · Understanding: compare by factors',
      L("Last month Dana spent her whole budget on notebooks and bought thirty of them. This month her budget is twenty "
        "percent larger, and each notebook costs one and a half times as much as last month. How many notebooks can she "
        "buy this month with her whole budget?", pt('stem', 'Last month Dana spent', 'hl', 12.0), voice='calm', pause=0.5),
      L("So two things change, the budget and the price. And we know only relations, not the real budget or the real "
        "price.", pt('stem: given', 'So two things change')),
      L("We'll solve it in two different ways. Let's start by understanding, and compare by factors, like in the lesson. "
        "The number of notebooks is the budget divided by the price.", show(q21a, 'The number of notebooks is')),
      L("The budget is twenty percent larger. That's times one point two, or six fifths. A bigger budget buys more "
        "notebooks. That's the same way, so times six fifths as it is.", show(q21b, 'times one point two, or six fifths')),
      L("The price is times one and a half, that's three halves. A higher price buys fewer notebooks. That's the "
        "opposite way, so we flip it. Three halves becomes two thirds.", show(q21c, 'Three halves becomes two thirds')),
      L("So we start from the old value, thirty, and multiply by both factors. Thirty times six fifths times two thirds.",
        show(q21d, 'Thirty times six fifths times two thirds')),
      L("Thirty divided by five is six. Then six times six is thirty-six.", show(q21e, 'Thirty divided by five is six'), show(q21e2, 'Then six times six')),
      L("Thirty-six divided by three is twelve. Then twelve times two is twenty-four notebooks.",
        show(q21f, 'Thirty-six divided by three'), show(q21f2, 'Then twelve times two')),
    ),
    S('Method 1 · Understanding: compare by factors',
      L("Careful with fifty-four, choice number one. That's thirty-six times three halves. It forgets to flip the price.",
        show(q21g, "That's thirty-six times three halves"), mk('cross', 'choice 1', 'It forgets to flip the price')),
      L("And careful with twenty-one, choice number four. It adds the percents. It takes twenty percent more for the "
        "budget, and fifty percent fewer notebooks for the price. Twenty minus fifty is minus thirty percent, and thirty "
        "minus thirty percent is twenty-one.", show(q21h, 'Twenty minus fifty is minus thirty')),
      L("But each change multiplies. And a price that is fifty percent higher doesn't mean fifty percent fewer "
        "notebooks.", mk('cross', 'choice 4', "doesn't mean fifty percent fewer")),
      L("So she can buy twenty-four notebooks. That's choice number three.")),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. The real price isn't given, so we choose it. "
        "Let's say a notebook cost ten last month. Then the budget was thirty times ten, three hundred.",
        show(q21i, "Let's say a notebook cost ten")),
      L("This month the budget is twenty percent larger. Twenty percent of three hundred is sixty. So three hundred plus "
        "sixty, three hundred sixty.", show(q21j, 'So three hundred plus')),
      L("And the price is one and a half times ten, fifteen.", show(q21k, 'one and a half times ten')),
      L("Three hundred sixty divided by fifteen. Fifteen times twenty is three hundred. Then fifteen times four is sixty. "
        "So twenty-four notebooks.", show(q21l, 'Three hundred sixty divided by fifteen')),
      L("Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])
# 21 Oct direct clarity review: independent results reveal at their spoken clauses.
def _clause_rows(vid, name, *pieces):
    found = 0
    for sl in VIDEOS[vid]['slides']:
        for ln in sl['lines']:
            cues = []
            for cue in ln['cues']:
                if cue[0] == 'show' and cue[1]['_name'] == name:
                    old = cue[1]; found += 1
                    for j, (tex, anchor) in enumerate(pieces):
                        assert anchor.lower() in ln['say'].lower(), (vid, name, anchor)
                        make = IH if old.get('_hand') else I
                        it = make(name if not j else name+'_clause'+str(j), tex,
                                  size=old.get('size',30), col=old['_col'])
                        cues.append(show(it, anchor))
                else: cues.append(cue)
            ln['cues'] = sorted(cues, key=lambda c: _phrase_pos(ln['say'],c))
    assert found == 1, (vid, name, found)

def _later(vid, name, anchor):
    found = 0
    for sl in VIDEOS[vid]['slides']:
        for ln in sl['lines']:
            for j,c in enumerate(ln['cues']):
                if c[0]=='show' and c[1]['_name']==name:
                    assert anchor.lower() in ln['say'].lower(), (vid,name,anchor)
                    ln['cues'][j]=(c[0],c[1],anchor); found+=1
            ln['cues'].sort(key=lambda c: _phrase_pos(ln['say'],c))
    assert found==1,(vid,name,found)

# Position helper here because these edits run before the automatic visual passes.
def _phrase_pos(say, c):
    ph = c[2] if c[0] in ('show', 'point') else c[3]
    return -1 if ph.startswith('<') else say.lower().find(ph.lower())

for _name,_anchor in [('c_d1','Three times five is fifteen'),('c_d2','Six times five is thirty'),
                      ('c_d6','three times two is six'),('c_i1','twelve divided by three'),
                      ('c_i2','twelve divided by six')]:
    _later('wp-092',_name,_anchor)
_clause_rows('wp-092','c_m4',('$20$ pages a minute','Twice as fast is twenty'),
             ('$12$ minutes','Four times as long is twelve'))
_clause_rows('solve-wp26-g093','g93j',('$x=6$ flyers, $y=2$ minutes',"Let's say x is six"),
             ('$6\\div2=3$ flyers a minute','Six divided by two is three'))
_clause_rows('solve-wp26-g093','g93o',('$5\\times6=30$','Five times six is thirty'),
             ('$30\\div3=10$','Then thirty divided by three'))
_clause_rows('solve-q-r26-t26-01','q1h',('$20\\%$ of $5$ is $1$','Twenty percent of five is one'),
             ('$5+1=6$ pages a minute','five plus one, six'))
_clause_rows('wp-094','t4e3',('$\\frac{1}{4}=\\frac{3}{12}$','A quarter is three twelfths'),
             ('$\\frac{3}{12}+\\frac{1}{12}=\\frac{4}{12}$','Three twelfths plus one twelfth'))
_later('wp-094','t4t_e','Ella fills three bags')
_later('wp-094','t4t_t','Tom fills two bags')
_later('wp-094','t4g6','Twenty divided by five is four')
_later('wp-097','t7w1',"time is times four thirds too")
_later('wp-097','t7w2','The time is times three halves')
_clause_rows('wp-097','t7y2',('$4\\times30=120$','Four times thirty is a hundred twenty'),
             ('$120\\div2=60$ pies','a hundred twenty divided by two'))
_clause_rows('solve-q-r26-t26-03','q3j',('A: $\\frac{1}{12}$ of the pool an hour','Pipe A fills a twelfth'),
             ('$3\\times\\frac{1}{12}=\\frac{1}{4}$ of the pool','In three hours'))
_later('solve-wp26-g101','g01d','four S')
_later('solve-wp26-g101','g01e',"and that's one")
_clause_rows('solve-q-r26-t26-04','q4i',('$30-20=10$','The gap is thirty minus twenty'),
             ('$10\\div5=2$','Ten divided by five'))
# The seesaw layer contains 24 and distances 4/6: do not reveal it while merely describing the pivot.
_pivot = next(c for ln in VIDEOS['solve-q-r26-t26-04']['slides'][2]['lines'] for c in ln['cues']
              if c[0]=='show' and c[1]['_name']=='q4w_pivot')
_sl = VIDEOS['solve-q-r26-t26-04']['slides'][2]
for _ln in _sl['lines']:
    _ln['cues']=[c for c in _ln['cues'] if c is not _pivot]
_sl['lines'][4]['cues'].append(show(_pivot[1],'is twenty-four'))
_sl['lines'][4]['cues'].sort(key=lambda c:_phrase_pos(_sl['lines'][4]['say'],c))
_later('solve-wp26-g103','g03t_a','Two hundred times three is six hundred')
_later('solve-wp26-g103','g03t_b','Thirty times two is sixty')
_clause_rows('solve-wp26-g105b','g5bb',('$200\\div2=100$ sheep','Half of two hundred is a hundred'),
             ('$9\\times2=18$ days','Nine times two is eighteen'))
_later('solve-wp26-g105b','g5bg','So twenty days')
_later('solve-wp26-g105b','g5bk','that leaves twenty days')
_clause_rows('r26-t26-factors','f6c4',('$900\\div3=300$','Nine hundred divided by three'),
             ('$300\\times4=1200$ km','Then three hundred times four'))
_clause_rows('wp-099','t9f6',('$60\\div5=12$','Sixty divided by five is twelve'),
             ('$12\\times8=96$: the trap','twelve times eight'))
_later('wp-099','t9ft_w2',"That's twenty minutes of work")
_later('wp-099','t9e4','adds up to thirty')
_later('solve-wp26-g095','g95l','minus three, five units')
_clause_rows('solve-wp26-g096','g96l',('$6\\times10=60$','Six times ten is sixty'),
             ('$6+10=16$','Six plus ten is sixteen'),
             ('$\\frac{60}{16}$','So sixty over sixteen'))
_clause_rows('solve-q-r26-t26-02','q2j',('$10\\times15=150$','Ten times fifteen is a hundred fifty'),
             ('$10+15=25$','Ten plus fifteen is twenty-five'))
_later('solve-wp26-g098','g98c','The time is times three quarters')

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

# 2026-10-11 teacher: "when I talk about the second given, highlight only the second given" (from topic 13): a POINT on
# 'stem' becomes the part of the question her sentence is about (given = the story, ask = the question sentence). The
# stems are copied from the course (stemRich).
STEMS = {
 "wp26-g093": "A volunteer folds $x$ flyers in $y$ minutes at a constant rate, where $x$ and $y$ are positive. How many flyers will she fold in $5y$ minutes if her rate becomes 3 times as great?",
 "q-r26-t26-01": "A printer finishes a job in 60 minutes. Its speed increases by 20%. How many minutes does the same job take now?",
 "wp26-g095": "Two identical hoses each fill a pond in 15 hours. An outlet pipe empties a full pond in 20 hours. At 7 a.m. the pond is empty, and both hoses and the outlet pipe are opened. At what time is the pond full?",
 "wp26-g096": "Printer A prints one batch of catalogs in 6 hours, while printer B prints the same batch in 10 hours. If they work together at their usual constant rates, how many minutes do they need for one batch?",
 "q-r26-t26-02": "Worker A can do a job alone in 10 hours. Worker B can do the same job alone in 15 hours. How many hours do they need if they work together?",
 "wp26-g098": "Three identical gardeners plant 40 trees in 5 hours. How many hours do four such gardeners need to plant 96 trees?",
 "wp26-g100": "A fence around a park is completed by 14 workers working for 9 days, followed by 6 workers working for 11 days. All work at the same constant rate. How many days would one worker need to complete the whole fence alone?",
 "q-r26-t26-03": "Pipe A fills a pool in 12 hours. Pipe B fills the same pool in 6 hours. Pipe A runs alone for 3 hours, and then pipe B is also opened. How many more hours are needed to fill the pool?",
 "wp26-g101": "The combined rate of 5 large dishwashers is twice the combined rate of 10 small dishwashers. Dishwashers of the same type are identical. How many times as fast is one large dishwasher as one small dishwasher?",
 "wp26-g102": "Customers add 18 orders to a bakery’s queue each hour. The baker completes 15 orders every 40 minutes. There are initially 60 orders in the queue. At these constant rates, how many orders are in the queue after 4 hours?",
 "q-r26-t26-04": "A machine makes 60 parts at a rate of 30 parts per hour, and then 60 more parts at a rate of 20 parts per hour. What is its average rate for all 120 parts, in parts per hour?",
 "wp26-g103": "Polisher A polishes 200 m² of floor in 4 hours. Polisher B polishes 30 m² in 6 hours. Working together at these constant rates, how many minutes do they need for 110 m²?",
 "wp26-g104": "Omar, Priya and Sam each work at a constant rate. Together they complete a job in 9 hours. Omar and Priya together complete it in 18 hours. What fraction of the job does Sam complete in one hour?",
 "wp26-g105": "Twelve identical workers can set up one stage in 2 hours. Fourteen such workers can set up the seating in 4 hours. How many workers are needed to set up one stage and the seating in 8 hours?",
 "wp26-g105b": "A supply of hay is enough for 200 identical sheep for 9 days. Each sheep eats the same constant amount per day. For how many days would that supply feed 90 sheep?",
 "q-r26-t26-21": "Last month Dana spent her whole budget on notebooks and bought 30 of them. This month her budget is 20% larger, and each notebook costs 1.5 times as much as last month. How many notebooks can she buy this month with her whole budget?",
}   # word stems: "given" = the story, "ask" = the question sentence

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
    if 'Given:' not in head and head.strip():         # topic 22 word stems: the story (studio anStemParts: given = all before ask)
        parts['given'] = _words(re.sub(r'\$([^$]*)\$', lambda m: ' '.join(_tex_words(m.group(1))), head))
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
CP.split(globals(), *CAMERA_SPLIT)
for _sp in SPLITS: CP.split(globals(), *_sp)     # 2026-10-21 R37: the lessons that grew (core methods in them), in parts, not on camera

for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _stem_parts(_v); _write_gap(_v)



# 2026-10-13 carry-over boxes (V2) and the layer-order check (V1): after the visual passes, like topics 13-18
import types as _types
MV.carry(_types.SimpleNamespace(**globals()), CARRY26)
for _v in CARRY26:                                      # 2026-10-18 visual check: the So-far box at a readable size
    for _sl in VIDEOS[_v]['slides']:
        for _ln in _sl['lines']:
            for _c in _ln['cues']:
                if _c[0] == 'show' and _c[1].get('keep'): _c[1]['size'] = 30
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
