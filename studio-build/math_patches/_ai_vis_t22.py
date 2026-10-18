"""Topic 22 (General word problems and ratios) - the scripts for the teacher's own-voice reading (2026-10-18), written from
the first draft to the Codex review standard, the clarity style, W1-W21, the method vocabulary and the method visuals,
built exactly like topic 20 (math_patches/_ai_vis_t20.py: the DSL and the visual passes are copied here, so the topics
stay independent; the stem-part highlighting is copied from topic 13, with the word stems' story as the "given" part).

The camera lesson 'wp-027' (From Words to Equations) gets a full reading script with more examples, split into three
parts of about 3-4 minutes (math_patches/_camera_parts.py). Every other topic-22 video gets a script that SHE reads aloud
in the Reading Studio; reading_to_video.py then times the handwriting and the visuals to her words. The summary video
r26-t22-summary is not read: summary_pages/t22.json (python3 summary_pages.py 22) replaces it.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t22.py [vid ...] writes it);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t22.py ai_redo_t22() (runs LAST) rebuilds the slides from studio_slides(vid) and then
                    _ai_visual.apply() adds the cues and click items around them.

Spec DSL (as in topic 20): video / S / L / I / IH (a hand-written board line) / show / pt / mk; figures TBL (the ratio
table and the then-and-now table), UNITS (ratio units, the fraction bar of a story), ZL (a number line), all built in
layers at the spoken words. The concept map (NEW / REMINDER per video) is in ~/Downloads/Topic-22-AI-scripts-review.md.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(HERE) != 'math_patches':      # a test copy elsewhere still reads and writes the real studio files
    HERE = '/Users/nitzanslasky/psychometry-course/studio-build/math_patches'
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t22ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-22 flow order of the scripts
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
QBOT = {'solve-q-r26-t22-01': 242, 'solve-q-r26-t22-02': 242, 'solve-q-r26-t22-03': 242, 'solve-q-r26-t22-04': 181, 'solve-q-r26-t22-05': 242, 'solve-q-r26-t22-20': 242, 'solve-wp22-g029': 181, 'solve-wp22-g030': 181, 'solve-wp22-g032': 286, 'solve-wp22-g033': 229, 'solve-wp22-g035': 252, 'solve-wp22-g036': 242, 'solve-wp22-g038': 286, 'solve-wp22-g039': 181, 'solve-wp22-g040': 242, 'solve-wp22-g042': 242, 'solve-wp22-g043': 252, 'solve-wp22-g044': 192, 'solve-wp22-g045': 232, 'solve-wp22-g046': 287, 'solve-wp22-g047': 286, 'solve-wp22-g048': 242, 'solve-wp22-g049': 239, 'solve-wp22-g050': 239}


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
CAM_BASE = 'wp-027'
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
            'style': "the teacher reads it herself (Reading Studio), topic-22 scripts (2026-10-18): math_patches/_ai_vis_t22.py is "
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
    VB = '0 0 640 186'
    def txt(x, y, t, c, size=24, style=''):
        return ('<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="%d" font-weight="bold"%s>%s</text>'
                % (x, y, c, FONT, size, (' font-style="%s"' % style) if style else '', t))
    body = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.5"/>' % (L_ - 6, Y_, R_ + 6, Y_, INK) +
            '<path d="M %d %d l 12 -7 l 0 14 Z" fill="%s"/>' % (L_ - 10, Y_, INK) + '<path d="M %d %d l -12 -7 l 0 14 Z" fill="%s"/>' % (R_ + 10, Y_, INK))
    for t in ticks:
        v, lab = t if isinstance(t, tuple) else (t, ('−%s' % -t) if t < 0 else str(t))
        body += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2"/>' % (X(v), Y_ - 10, X(v), Y_ + 10, INK) + txt(X(v), Y_ + 40, lab, INK, 30)
    out = [('line', _svg(VB, body, title))]
    for key, marks in layers:
        b = ''
        for m in marks:
            if m[0] in ('pt', 'ink'):
                c = TEAL if m[0] == 'pt' else INK
                b += '<circle cx="%.1f" cy="%d" r="7" fill="%s"/>' % (X(m[1]), Y_, c) + txt(X(m[1]), Y_ - 18, m[2], c, 30, 'italic')
            elif m[0] == 'arrow':
                a, e = X(m[1]), X(m[2]); d = 1 if e > a else -1
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3"/>' % (a, Y_ - 58, e - 10 * d, Y_ - 58, TEAL) +
                      '<path d="M %.1f %d l %d -7 l 0 14 Z" fill="%s"/>' % (e, Y_ - 58, -14 * d, TEAL))
                if m[3]: b += txt((a + e) / 2, Y_ - 70, m[3], TEAL, 28)
            elif m[0] == 'shade':
                b += '<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (X(m[1]), Y_ - 7, X(m[2]) - X(m[1]), BAND, TEAL)
            elif m[0] == 'cross':
                x0 = X(m[1]); y0 = Y_ - 58
                b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (x0 - 14, y0 - 14, x0 + 14, y0 + 14, RED) +
                      '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (x0 + 14, y0 - 14, x0 - 14, y0 + 14, RED))
            elif m[0] == 'below':
                b += txt(X(m[1]), Y_ + 68, m[2], TEAL, 28)
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


# ------------------------------------------------------------------------------------------- topic-22 figures (V1)
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
    body += ''.join(_tx(cx(k), y0 + headh * .68, h, 27) for k, h in enumerate(head))
    left = x0 if haslab else xs[0]
    body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4"/>' % (xs[0], y0, xs[-1], y0, _INK)
    for r in range(nr + 1):
        y = top(r)
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s"/>' % (left if r else xs[0], y, xs[-1], y, _INK, 2.4 if r == 0 else 1.6)
    for x in xs:
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>' % (x, y0, x, top(nr), _INK)
    if haslab:
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>' % (x0, top(0), x0, top(nr), _INK)
        body += ''.join(_tx(x0 + lw / 2.0, cy(r), lab, 26) for r, lab in enumerate(rowlab))
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
      ('right', r, text)               a value after the row"""
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
                f = '#fbe3cf' if len(m) > 4 and m[4] == 'orange' else MV.BAND
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
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def OWN(d, name):
    """a ZL number line whose layers find their own base (written lines may come in between)"""
    for it in d.values():
        if it.get('over'): it['of'] = name
        else: it['fig'] = name
    return d


# =================================================================================================================
# THE SCRIPTS (topic-22 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-22-AI-scripts-review.md.
# Study plan before topic 22: 1, 30, 2, 4, 31, 6, 8, 32, 9, 10, 33, 51, 21, 3. So equations and systems (6), fractions
# (2, 3), the five method names and plugging in (51), trial and error (21) are REMINDERS; inequalities (12), absolute
# value (13), divisibility signs (15), percents (23), work (26) and averages (25) come LATER - explained on the spot or
# avoided. New here: translating phrases, the ratio table and the triangle value, inverse proportion, "or part of",
# ratio units, the shared group, the part that stays, the gap that changes by two, give it to the little guy, the
# tools of the advanced questions (write it all first, start from the end, what changed, same factor, assume all the
# same, one equation with two unknowns).
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ wp-027 (camera lesson)
# Hebrew (wp 1068-1272): a quarter of the section (really more); three stages, the third a concentration check (x = 8
# but they ask x - 1 or 2x); not every word problem needs an equation; the example read phrase by phrase ("wow, take a
# breath"), every equation is a sentence; the phrase table: more by 3, less by 5 (the same fact both ways), twice /
# double = always x 2 (like a half = always / 2), less by a quarter (the whole is the thing we compare with), the
# difference (bars: "always positive", we don't care who is bigger), "makes up" -> "is", "of" = times, 2B = 3P ("as" =
# equals), a ratio 2 : 3 -> 2x and 3x (a lesson of its own later); recap: step by step, don't panic, learn the table.
# English additions (teacher: 2-3 examples per concept on camera): a second worked example (x + 15 = 4x, they ask
# x - 1), a number check for every phrase, a third-less case. Numbers and names differ from the Hebrew.
# NEW (all of it). Reminders later: every question video ("x = what they ask", "step by step").
c_st1 = I('c_st1', '1 · Translate the words into an equation', size=30)
c_st2 = I('c_st2', '2 · Solve the equation', size=30)
c_st3 = I('c_st3', '3 · Answer what they asked', size=30)
c_st3b = IH('c_st3b', '$x=8$, they ask for $x-1$', size=30)
c_st3c = IH('c_st3c', '$8-1=7$', size=30)
c_e1q = I('c_e1q', 'A number is multiplied by $3$, and then $24$ is added. The result is $7$ times the original number. What is twice the number?', size=30)
c_e1a = IH('c_e1a', 'the number $=x$', size=30)
c_e1b = IH('c_e1b', '$3x+24$', size=30)
c_e1c = IH('c_e1c', '$3x+24=7x$', size=30)
c_e1d0 = IH('c_e1d0', '$7x-3x=4x$', size=30)
c_e1d = IH('c_e1d', '$24=4x$', size=30)
c_e1e = IH('c_e1e', '$x=24\\div4=6$', size=30)
c_e1f = IH('c_e1f', 'twice: $\\ 2x=2\\cdot6=12$', size=30)
c_e2q = I('c_e2q', 'A number plus $15$ is equal to $4$ times the number. What is the number minus $1$?', size=30)
c_e2a = IH('c_e2a', '$x+15=4x$', size=30)
c_e2b0 = IH('c_e2b0', '$4x-x=3x$', size=30)
c_e2b = IH('c_e2b', '$15=3x$', size=30)
c_e2c = IH('c_e2c', '$x=15\\div3=5$', size=30)
c_e2d = IH('c_e2d', '$x-1=5-1=4$', size=30)
c_m1 = I('c_m1', '$A$ is $3$ more than $B$', size=32)
c_m1e = IH('c_m1e', '$A=B+3$', size=30)
c_m1b = IH('c_m1b', '$B=10\\ \\to\\ A=10+3=13$', size=30)
c_m1c = I('c_m1c', 'Dana is $3$ years older than Ella: $\\quad D=E+3$', size=32)
c_m2 = I('c_m2', '$B$ is $5$ less than $A$', size=32)
c_m2e = IH('c_m2e', '$B=A-5$', size=30)
c_m2c = I('c_m2c', 'Ben has $5$ fewer marbles than Sam: $\\quad B=S-5$', size=32)
c_m2b = IH('c_m2b', 'the same fact: $\\ A=B+5$', size=30)
c_m2d0 = IH('c_m2d0', 'Sam $12$, Ben $5$ fewer: $\\ 7$', size=30)
c_m2d = IH('c_m2d', '$B=S-5$: $\\ 12-5=7$ ✓', size=30)
c_t1 = I('c_t1', '$A$ is $4$ times $B$: $\\quad A=4B$', size=32)
c_t1b = IH('c_t1b', '$B=3\\ \\to\\ A=4\\cdot3=12$', size=30)
c_t1c = IH('c_t1c', '$4$ more: $\\ 3+4=7$', size=30)
c_t1d = IH('c_t1d', '$4$ times: $\\ 4\\cdot3=12$', size=30)
c_t2 = I('c_t2', 'twice $=$ double $=$ always $\\times2$', size=32)
c_t2h = I('c_t2h', 'half $=$ always $\\div2$', size=32)
c_t2b = I('c_t2b', '$A$ is twice $B$: $\\quad A=2B$', size=32)
c_t2c = I('c_t2c', "Ella's salary is double Noa's: $\\quad E=2N$", size=32)
c_f1 = I('c_f1', '$B$ is a quarter less than $A$', size=32)
c_f1b = IH('c_f1b', '$B=A-\\frac{1}{4}A=\\frac{3}{4}A$', size=32)
c_f1c = IH('c_f1c', 'laptop $400$: $\\ \\frac{1}{4}$ of $400=100$', size=30)
c_f1d = IH('c_f1d', 'tablet $=400-100=300$', size=30)
c_f1e = IH('c_f1e', '$300=\\frac{3}{4}\\cdot400$', size=30)
c_f2 = I('c_f2', '$C$ is a third less than $D$', size=32)
c_f2e = IH('c_f2e', '$C=D-\\frac{1}{3}D=\\frac{2}{3}D$', size=30)
c_f2b = IH('c_f2b', '$D=30$: $\\ \\frac{1}{3}$ of $30=10$', size=30)
c_f2c = IH('c_f2c', '$C=30-10=20$', size=30)
c_d1 = I('c_d1', 'The difference between $A$ and $B$ is $12$', size=32)
c_d2 = IH('c_d2', '$A-B=12\\ $ or $\\ B-A=12$', size=30)
c_d3 = IH('c_d3', '$20$ and $8$: $\\ 20-8=12$', size=30)
c_d4 = I('c_d4', 'Ron is older: $\\quad R-G=12$', size=32)
c_i1 = I('c_i1', '$A$ is (makes up) $\\frac{2}{3}$ of $B$', size=32)
c_i2a = I('c_i2a', 'is: $\\ =$', size=32)
c_i2 = I('c_i2', 'of: $\\ \\times$', size=32)
c_i3 = IH('c_i3', '$A=\\frac{2}{3}\\cdot B$', size=32)
c_i4 = IH('c_i4', '$B=30$: $\\ \\frac{1}{3}$ of $30=10$', size=30)
c_i4b = IH('c_i4b', '$\\frac{2}{3}$ of $30=20=A$', size=30)
c_i5 = I('c_i5', '$2$ mugs cost the same as $5$ pens', size=32)
c_i5b = IH('c_i5b', '$2M=5P$', size=30)
c_r1 = I('c_r1', 'The ratio of $A$ to $B$ is $2:3$', size=32)
c_r2 = IH('c_r2', '$A=2x,\\ \\ B=3x$', size=30)
c_r3 = IH('c_r3', '$x=5\\ \\to\\ 10$ apples, $15$ pears', size=30)
c_s1 = I('c_s1', 'Step by step: one phrase at a time', size=30)
c_s2 = I('c_s2', '$1$ translate $\\cdot$ $2$ solve $\\cdot$ $3$ answer what they asked', size=30)
c_s3 = I('c_s3', 'more $+$ $\\cdot$ less $-$ $\\cdot$ times $\\times$ $\\cdot$ twice $\\times2$', size=30)
c_s3b = I('c_s3b', 'a quarter less $\\frac34$ $\\cdot$ of $\\times$ $\\cdot$ is, the same as $=$', size=30)
video('wp-027', 'lesson', slides=[
    S('From Words to Equations',
      L("Welcome back, and now we're starting a new topic, word problems. In the quantitative section, about five of the "
        "twenty questions are word problems. That's a quarter of the section."),
      L("And honestly, it's even more than a quarter. Many algebra and geometry questions are written in words too. For "
        "example, a question can say that a number is divided by five and leaves a remainder of two. That's an algebra "
        "question, but it's written in words. So first we have to read it and understand what it means in math.")),
    S('Three stages',
      L("So how do we solve a word problem? In three stages. Stage one, we translate the words into an equation. This is "
        "the stage of understanding, and it's the hardest part.", show(c_st1, 'Stage one, we translate')),
      L("Stage two, we solve the equation. That part is technical. It's the algebra we already know, moving terms to the "
        "other side, opening brackets, a common denominator. It's a shame to lose points here.",
        show(c_st2, 'Stage two, we solve')),
      L("Stage three, we answer the question. Careful here, because solving the equation doesn't always finish the job. "
        "Say we find that x is eight, but they ask for x minus one. Then the answer is seven, not eight. It's not a "
        "trick. It's a concentration check. So at the end, always look again at what they asked.",
        show(c_st3, 'Stage three, we answer'), show(c_st3b, 'Say we find that x is eight'),
        show(c_st3c, 'Then the answer is seven')),
      L("And not every word problem needs an equation. Some we solve by trial and error, like in the last topic, and some "
        "by plugging in the answers. But right now our topic is the translation, how the words become an equation.")),
    S('Step by step',
      L("Let's see it on an example. A number is multiplied by three, and then twenty-four is added. The result is seven "
        "times the original number. What is twice the number?", show(c_e1q, 'A number is multiplied')),
      L("Wow, a lot of words. Don't panic, we'll go piece by piece. We don't know the number, so let's call it x.",
        show(c_e1a, "so let's call it x")),
      L("Multiplied by three, that's three x. And then twenty-four is added, so three x plus twenty-four.",
        show(c_e1b, 'And then twenty-four is added')),
      L("The result is. That's our equals sign. Seven times the original number, that's seven x.",
        show(c_e1c, 'Seven times the original number')),
      L("Now let's read the equation back in words. A number times three, plus twenty-four, is equal to seven times the "
        "number. It's almost word for word the question. Every equation is really a sentence in words."),
      L("Stage two is technical. We want the x's on one side, so we take three x away from both sides. Seven x minus three "
        "x is four x, so twenty-four is equal to four x. Then we divide both sides by four, and x is six.",
        show(c_e1d0, 'Seven x minus three'), show(c_e1d, 'so twenty-four is equal to four x'), show(c_e1e, 'Then we divide both sides by four')),
      L("Stage three. Did they ask for the number? No, they asked for twice the number. Two times six is twelve. So the "
        "answer is twelve, not six.", show(c_e1f, 'Two times six is twelve'))),
    S('One more example',
      L("Let's do one more, a shorter one. A number plus fifteen is equal to four times the number. What is the number "
        "minus one?", show(c_e2q, 'A number plus fifteen')),
      L("Again, the number is x. A number plus fifteen is x plus fifteen. Is equal to, that's the equals sign. Four times "
        "the number is four x.", show(c_e2a, 'Four times the number is four x')),
      L("Now we solve. We take x away from both sides. Four x minus x is three x, so fifteen is equal to three x. Then we "
        "divide by three, and x is five.", show(c_e2b0, 'Four x minus x'), show(c_e2b, 'so fifteen is equal to three x'), show(c_e2c, 'Then we divide by three')),
      L("And stage three. They asked for the number minus one, so five minus one is four. Five would be the trap, because "
        "that's the number itself.", show(c_e2d, 'so five minus one is four')),
      L("So again, what did we do? We translated one phrase at a time, we solved, and then we checked what they asked. Now "
        "let's learn the phrases one by one, and how each one is written in math.")),
    S('More and less',
      L("The first phrase. A is three more than B. What does that mean? If we start with B and add three, we get A. So A "
        "is equal to B plus three.", show(c_m1, 'A is three more than B'), show(c_m1e, 'So A is equal to B plus three')),
      L("Let's see it in numbers. If B is ten, then A is ten plus three, thirteen. And in a question it sounds like this. "
        "Dana is three years older than Ella. So Dana is Ella plus three.", show(c_m1b, 'If B is ten'),
        show(c_m1c, 'So Dana is Ella plus three')),
      L("Now the opposite. B is five less than A. So we start with A and take away five. B is equal to A minus five. In "
        "a question, Ben has five fewer marbles than Sam. So Ben is Sam minus five.", show(c_m2, 'B is five less than A'),
        show(c_m2e, 'B is equal to A minus five'), show(c_m2c, 'So Ben is Sam minus five')),
      L("These two ways are really the same idea, written the other way round. If B is five less than A, then A is five "
        "more than B, so A is equal to B plus five. Both are right, as long as we write it the right way.",
        show(c_m2b, 'so A is equal to B plus five')),
      L("How do we know we wrote it the right way? We check with a number. Say Sam has twelve marbles. Then Ben has five "
        "fewer, seven. And in our equation, twelve minus five is seven. It fits.", show(c_m2d0, 'Say Sam has twelve marbles'),
        show(c_m2d, 'twelve minus five is seven'))),
    S('Times and twice',
      L("Next, times. A is four times B. That means A is equal to four B, four times B. In numbers, if B is three, then A "
        "is four times three, twelve.", show(c_t1, 'That means A is equal to four B'), show(c_t1b, 'if B is three')),
      L("Careful not to mix up four times with four more. Four more than three is three plus four, seven. Four times three "
        "is twelve. These are two different things.", show(c_t1c, 'Four more than three'), show(c_t1d, 'Four times three is twelve')),
      L("And here's a word that is always the same. Twice, or double, is always times two. If I want times three, I don't "
        "say double, I say three times. Just like half is always divided by two. I can cut a cake into three parts, but "
        "not into three halves. Halves are always two.", show(c_t2, 'Twice, or double, is always'), show(c_t2h, 'Just like half is always')),
      L("So A is twice B means A is equal to two B. In a question it can sound like this. Ella's salary is double Noa's "
        "salary. So Ella's salary is two times Noa's salary.", show(c_t2b, 'So A is twice B'),
        show(c_t2c, "So Ella's salary is two times"))),
    S('A fraction less',
      L("Now a phrase with a fraction. B is a quarter less than A. What does that mean? We take A, and take away a quarter "
        "of A. A whole A minus a quarter of A leaves three quarters of A. So B is three quarters of A.",
        show(c_f1, 'B is a quarter less than A'), show(c_f1b, 'A whole A minus a quarter')),
      L("Let's see it in numbers. A tablet costs a quarter less than a laptop, and the laptop costs four hundred credits. "
        "A quarter of four hundred is a hundred. So the tablet costs four hundred minus a hundred, three hundred credits. "
        "And three hundred is exactly three quarters of four hundred.", show(c_f1c, 'A quarter of four hundred'),
        show(c_f1d, 'So the tablet costs'), show(c_f1e, 'And three hundred is exactly')),
      L("Careful here. A quarter of what? A quarter of the laptop, the thing we compare with. The whole is the laptop, so "
        "the quarter is taken from the laptop's price, not from the tablet's price."),
      L("One more, with a third. C is a third less than D. So we take away a third of D, and two thirds of D are left. If "
        "D is thirty, a third of thirty is ten, and C is thirty minus ten, twenty.", show(c_f2, 'C is a third less than D'), show(c_f2e, 'and two thirds of D are left'),
        show(c_f2b, 'If D is thirty'), show(c_f2c, 'and C is thirty minus ten'))),
    S('The difference',
      L("The difference between A and B is twelve. A difference is always positive. It's the bigger number minus the "
        "smaller one.", show(c_d1, 'The difference between A and B')),
      L("But often we don't know which one is bigger. So there are two options. If A is bigger, A minus B is twelve. And "
        "if B is bigger, B minus A is twelve.", show(c_d2, 'So there are two options')),
      L("Let's see it in numbers. Twenty and eight have a difference of twelve, because twenty minus eight is twelve. And eight and "
        "twenty have the same difference, twelve. We never say the difference is minus twelve.",
        show(c_d3, 'Twenty and eight have a difference')),
      L("In a question it can sound like this. The difference between Ron's age and Gal's age is twelve. We don't care "
        "who is older. And when the story does tell us who is bigger, say Ron is older, we simply write Ron minus Gal is "
        "twelve. By the way, in math books you'll sometimes see a difference written with two straight bars. That's "
        "absolute value, a topic we'll learn later. For now, bigger minus smaller.", show(c_d4, 'say Ron is older'))),
    S('Is, of, the same as',
      L("Now three small words that turn into math signs. The first one is the word is. A is two thirds of B. The word is "
        "becomes the equals sign.", show(c_i1, 'A is two thirds of B'), show(c_i2a, 'The word is becomes')),
      L("Sometimes the question uses a more formal word, like A makes up two thirds of B. Just swap it for is. A is two "
        "thirds of B."),
      L("The second word is of. Of means times. Two thirds of B is two thirds times B. So A is equal to two thirds B.",
        show(c_i2, 'Of means times'), show(c_i3, 'So A is equal to two thirds B')),
      L("Let's see it in numbers. If B is thirty, a third of thirty is ten, and two thirds of thirty is twenty. So A is "
        "twenty. In a question it can sound like this. Amit's salary is two thirds of Ben's salary.",
        show(c_i4, 'If B is thirty'), show(c_i4b, 'two thirds of thirty is twenty')),
      L("The third one is costs the same as, or weighs the same as. Two mugs cost the same as five pens. We write it the "
        "way we hear it. Two mugs is two M. Cost the same as is the equals sign. Five pens is five P. So two M is equal "
        "to five P.", show(c_i5, 'Two mugs cost the same as five pens'),
        show(c_i5b, 'So two M is equal to five P'))),
    S('A ratio',
      L("And the last phrase, a ratio. The ratio of A to B is two to three. That means for every two A, there are three "
        "B.", show(c_r1, 'The ratio of A to B')),
      L("So we write A as two x and B as three x. For example, if there are two apples for every three pears, the apples "
        "are two x and the pears are three x.", show(c_r2, 'So we write A as two x')),
      L("If x is five, that's ten apples and fifteen pears, and it's still two apples for every three pears. We'll have a "
        "whole lesson on ratios soon, so for now, this is just the translation.", show(c_r3, 'If x is five'))),
    S('Summary',
      L("Let's sum up this lesson. The biggest tip is to work step by step. Many students see a question with a lot of "
        "words and panic. Don't. Take one phrase at a time, and write it in math.", show(c_s1, 'work step by step')),
      L("Then come the three stages. Translate, solve, and answer what they asked.", show(c_s2, 'Then come the three stages')),
      L("And go over the table of phrases on the memory card after this video, so that every phrase becomes automatic. "
        "[pause] This is just the start of word problems, and there are many more kinds ahead. I'll see you in the next "
        "video.", show(c_s3, 'the table of phrases'), show(c_s3b, 'on the memory card'))),
])
CAMERA_SPLIT = ('wp-027', 'From Words to Equations', [
    (1, None),
    (4, "Let's continue with word problems, and translate the phrases that come up again and again."),
    (7, "Let's continue with the phrases, starting with the difference between two numbers.")])

# ------------------------------------------------------------------------------------------------ wp-028 (lesson)
# Hebrew (wp 1278-1292): a very, very important lesson, a technique for the whole section (geometry, algebra, all kinds
# of problems), because many questions rest on equal ratios; the easiest way is an example. The example and the tools
# are taught in the next two questions (the ratio table: g029; the triangle value and cross-multiplying: g030).
r_l1 = I('r_l1', 'Same rate in two cases', size=32)
r_l2 = I('r_l2', 'the two cases have equal ratios', size=32)
video('wp-028', 'lesson', slides=[
    S('Equal Ratios',
      L("Equal ratios. A short lesson, but one of the most important in the whole course.")),
    S('Same rate, two cases',
      L("We're going to learn a technique that follows us through the whole quantitative section. In word problems, in "
        "geometry, and in algebra too. Many questions rest on one idea, the same rate in two different cases.",
        show(r_l1, 'the same rate in two different cases')),
      L("For example, every box holds the same number of pens. Or a machine works at a steady pace. When the rate stays the "
        "same, the two cases have equal ratios. The easiest way to learn it is on an example, so let's go straight to the "
        "questions. I'll see you in the next video.", show(r_l2, 'the two cases have equal ratios'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g029 (Hebrew: 5 trays, 30 cookies)
# Hebrew (wp 1293-1345): a simple example on purpose, the ratio table (a column per quantity), across x 6 (a whole
# ratio) and down x 4, the same 120. NEW here (full): the ratio table, across and down, the why (the same rate in both
# rows), with an easy warm-up first (W10). Ours: across x 7 is whole, down is x 1 1/2 (shown with the half).
g29w = TBL('g29w', ['Boxes', 'Pens'], ['', ''], [
    ('r1', [('c', 0, 0, '3'), ('c', 0, 1, '12')]), ('r2', [('c', 1, 0, '10'), ('q', 1, 1)]),
    ('h1', [('across', 0, '×4')]), ('h2', [('across', 1, '×4')]), ('ans', [('cover', 1, 1, '40')])], col=1, colw=150)
g29a = IH('g29a', '$3\\cdot4=12$', size=30)
g29b = IH('g29b', '$10\\cdot4=40$', size=30)
g29t = TBL('g29t', ['Vases', 'Roses'], ['', ''], [
    ('r1', [('c', 0, 0, '8'), ('c', 0, 1, '56')]), ('r2', [('c', 1, 0, '12'), ('q', 1, 1)]),
    ('h1', [('across', 0, '×7')]), ('h2', [('across', 1, '×7')]), ('ans', [('cover', 1, 1, '84')])], col=1, colw=150)
g29c = IH('g29c', '$8\\cdot7=56$', size=30)
g29d = IH('g29d', '$10\\cdot7=70$', size=30)
g29d2 = IH('g29d2', '$2\\cdot7=14$', size=30)
g29d3 = IH('g29d3', '$12\\cdot7=70+14=84$', size=30)
g29u = TBL('g29u', ['Vases', 'Roses'], ['', ''], [
    ('r1', [('c', 0, 0, '8'), ('c', 0, 1, '56')]), ('r2', [('c', 1, 0, '12'), ('q', 1, 1)]),
    ('v1', [('down', 0, 0, 1, '×1½')]), ('v2', [('down', 1, 0, 1, '×1½')]), ('ans', [('cover', 1, 1, '84')])],
    col=1, colw=150, side=100)
g29e = IH('g29e', '$12=8+4$', size=30)
g29e2 = IH('g29e2', '$4=\\frac{1}{2}\\cdot8$', size=30)
g29f = IH('g29f', '$\\frac{1}{2}\\cdot56=28$', size=30)
g29g = IH('g29g', '$56+28=84$', size=30)
video('solve-wp22-g029', 'solution', qid='wp22-g029', slides=[
    S('Method 1 · The math way: across',
      L("Eight vases hold fifty-six roses. With the same number of roses in each vase, how many roses are in twelve vases?",
        pt('stem', 'Eight vases', 'hl', 6.0), voice='calm', pause=0.5),
      L("The key words are the same number of roses in each vase. The rate stays the same, so this is a question of equal "
        "ratios. We'll solve it two ways, both with the ratio table, once across and once down.",
        pt('stem', 'The key words are')),
      L("Let's start with the math way, and learn a tool called the ratio table. It's a small table, with a column for "
        "each quantity. Let's see it first on easy numbers. Three boxes hold twelve pens, the same number in each box. How "
        "many pens are in ten boxes?", show(g29w['line'], 'Three boxes hold twelve pens')),
      L("In the first row we write what we know, three boxes and twelve pens. In the second row we write the new case, "
        "ten boxes, and a question mark for the pens.", show(g29w['r1'], 'In the first row'),
        show(g29w['r2'], 'In the second row')),
      L("Now look across the first row, from three to twelve. Three times four is twelve, so across we multiply by four. "
        "That's four pens in every box.", show(g29w['h1'], 'Now look across the first row'), show(g29a, 'Three times four is twelve')),
      L("The rate is the same in both rows, four pens a box. So across the second row, we also multiply by four. Ten "
        "times four is forty pens.", show(g29w['h2'], 'So across the second row'), show(g29b, 'Ten times four is forty'),
        show(g29w['ans'], 'forty pens'))),
    S('Method 1 · The math way: across',
      L("Now our question. Vases in one column, roses in the other. In the first row, what we know, eight vases and "
        "fifty-six roses. In the second row, the new case, twelve vases, and a question mark.",
        show(g29t['line'], 'Vases in one column'), show(g29t['r1'], 'In the first row'), show(g29t['r2'], 'In the second row')),
      L("Across the first row, from eight to fifty-six. Eight times seven is fifty-six, so across we multiply by seven. "
        "That means seven roses in each vase.", show(g29t['h1'], 'Across the first row'), show(g29c, 'Eight times seven')),
      L("The question says the same number of roses is in each vase. So the second row gets the same times seven. So we need twelve "
        "times seven. Ten times seven is seventy. Two times seven is fourteen. Together that's eighty-four.",
        pt('stem', 'The question says'), show(g29t['h2'], 'So the second row gets'), show(g29d, 'Ten times seven is seventy'),
        show(g29d2, 'Two times seven is fourteen'), show(g29d3, "Together that's eighty-four"), show(g29t['ans'], "that's eighty-four")),
      L("So twelve vases hold eighty-four roses. Choice number three is our answer.",
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Why does this work? Because the rate is the same in both rows. Every vase gets seven roses, whether there are "
        "eight vases or twelve. So whatever turns the vases into roses in one row, turns them into roses in the other "
        "row too.")),
    S('Method 2 · The math way: down',
      L("[pause] Now the same table, but down, from the first row to the second. We start again from the givens, eight "
        "vases, fifty-six roses, and twelve vases.", show(g29u['line'], 'Now the same table'),
        show(g29u['r1'], 'eight vases, fifty-six roses'), show(g29u['r2'], 'and twelve vases')),
      L("Down the vases column, from eight to twelve. Twelve is eight plus four, and four is half of eight. So twelve is "
        "one and a half times eight.", show(g29e, 'Twelve is eight plus four'), show(g29e2, 'four is half of eight'),
        show(g29u['v1'], 'So twelve is one and a half')),
      L("The rate is the same, so the roses are also multiplied by one and a half. One and a half times fifty-six means "
        "fifty-six plus half of fifty-six. Half of fifty-six is twenty-eight, and fifty-six plus twenty-eight is "
        "eighty-four.", show(g29u['v2'], 'so the roses are also multiplied'), show(g29f, 'Half of fifty-six is twenty-eight'),
        show(g29g, 'and fifty-six plus twenty-eight'), show(g29u['ans'], 'is eighty-four')),
      L("We get the same eighty-four. Across, the multiplier was a whole number, seven, so across was easier to calculate. So "
        "first look across and down, and use the one that gives a whole number. Choice number three is our answer, and "
        "I'll see you in the next question.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g030 (Hebrew: 6 minutes, 15 exercises)
# Hebrew (wp 1346-1415): neither ratio is whole, so the triangle value ("cross-multiply": the diagonal times, divided
# by what is left; why "triangle"; cancel first), then the same as an equation (the diagonal products are equal);
# either is fine. NEW here (full, two examples): the triangle value; cross-multiplying. The sense check before
# calculating is a first reaction (bigger or smaller). The second example (4 kg, 14 credits) has new numbers.
g30t = TBL('g30t', ['Minutes', 'Potatoes'], ['', ''], [
    ('r1', [('c', 0, 0, '12'), ('c', 0, 1, '18')]), ('r2', [('c', 1, 0, '20'), ('q', 1, 1)]),
    ('dg', [('diag', (1, 0), (0, 1))]), ('ans', [('cover', 1, 1, '30')])], col=1, colw=170)
g30s = IH('g30s', '$?>18$', size=30, col=1)
g30s2 = IH('g30s2', '$?<2\\cdot18=36$', size=30, col=1)
g30a = IH('g30a', 'across: $\\ 12\\to18$ is $\\times1\\frac{1}{2}$, $\\ $not whole', size=30)
g30b = IH('g30b', 'down: $\\ \\frac{20}{12}=\\frac{5}{3}$, $\\ $not whole', size=30)
g30c = IH('g30c', '$?=\\frac{20\\cdot18}{12}$', size=32)
g30d0 = IH('g30d0', '$18\\div6=3$', size=30)
g30d1 = IH('g30d1', '$12\\div6=2$', size=30)
g30d = IH('g30d', '$?=\\frac{20\\cdot3}{2}$', size=32)
g30e = IH('g30e', '$=\\frac{60}{2}$', size=32)
g30e2 = IH('g30e2', '$=30$', size=32)
g30k = TBL('g30k', ['Kilos', 'Credits'], ['', ''], [
    ('r1', [('c', 0, 0, '4'), ('c', 0, 1, '14')]), ('r2', [('c', 1, 0, '6'), ('q', 1, 1)]),
    ('dg', [('diag', (1, 0), (0, 1))]), ('ans', [('cover', 1, 1, '21')])], col=1, colw=170)
g30f = IH('g30f', '$?=\\frac{6\\cdot14}{4}$', size=32)
g30f2 = IH('g30f2', '$=\\frac{6\\cdot7}{2}$', size=32)
g30g = IH('g30g', '$=\\frac{42}{2}$', size=32)
g30g2 = IH('g30g2', '$=21$', size=32)
g30x = TBL('g30x', ['Minutes', 'Potatoes'], ['', ''], [
    ('r1', [('c', 0, 0, '12'), ('c', 0, 1, '18')]), ('r2', [('c', 1, 0, '20'), ('c', 1, 1, 'x', _TEAL)]),
    ('d1', [('diag', (1, 0), (0, 1))]), ('d2', [('diag', (0, 0), (1, 1))])], col=1, colw=170)
g30h = IH('g30h', '$12x=20\\cdot18$', size=32)
g30i = IH('g30i', '$2\\cdot18=36$', size=30)
g30i2 = IH('g30i2', '$20\\cdot18=36\\cdot10=360$', size=30)
g30j = IH('g30j', '$x=360\\div12$', size=32)
g30j2 = IH('g30j2', '$x=30$', size=32, col=1)
g30j3 = IH('g30j3', '$12\\cdot30=360$ ✓', size=30, col=1)
video('solve-wp22-g030', 'solution', qid='wp22-g030', slides=[
    S('Method 1 · The math way: the triangle value',
      L("Working at a steady pace, a cook peels eighteen potatoes in twelve minutes. How many potatoes does he peel in "
        "twenty minutes?", pt('stem', 'Working at a steady pace', 'hl', 6.0), voice='calm', pause=0.5),
      L("A steady pace means the same rate all the time, so again it's equal ratios. Before we calculate, should the "
        "answer be bigger or smaller? Twenty minutes is more than twelve, so he peels more than eighteen. And twenty is "
        "less than twice twelve, so he peels fewer than twice eighteen, fewer than thirty-six. So choice number two, "
        "thirty-six, is out. We'll solve it two ways, with the triangle value, and then by cross-multiplying.",
        pt('stem', 'A steady pace means'), show(g30s, 'so he peels more than eighteen'),
        show(g30s2, 'fewer than twice eighteen'), mk('cross', 'choice 2', 'is out')),
      L("Let's start with the math way, the ratio table. Minutes in one column, potatoes in the other. In the first row, "
        "twelve minutes and eighteen potatoes. In the second row, twenty minutes and a question mark.", show(g30t['line'], 'Minutes in one column'),
        show(g30t['r1'], 'In the first row'), show(g30t['r2'], 'In the second row')),
      L("Across the first row, from twelve to eighteen, is times one and a half. That's not a whole number. Down the "
        "minutes, from twelve to twenty, is twenty over twelve, five thirds. That's not whole either. So an easy multiplier "
        "doesn't help us here.", show(g30a, 'Across the first row'), show(g30b, 'Down the minutes')),
      L("When neither one is whole, we use the triangle value. We draw a line along the diagonal, from the twenty to the "
        "eighteen. We multiply the two numbers on the diagonal, and divide by the number that's left, the twelve.",
        show(g30t['dg'], 'We draw a line along the diagonal'), show(g30c, 'We multiply the two numbers')),
      L("Why is it called the triangle value? Because the three numbers we use, twenty, eighteen and twelve, make a "
        "triangle in the table. Multiply along the diagonal, and divide by what's left.")),
    S('Method 1 · The math way: the triangle value',
      L("Now the calculation. Before we multiply, let's make the numbers smaller. Eighteen and twelve both divide by six. "
        "Eighteen divided by six is three. Twelve divided by six is two. So now we have twenty times three, over "
        "two.", show(g30d0, 'Eighteen divided by six'), show(g30d1, 'Twelve divided by six'),
        show(g30d, 'So now we have twenty times three')),
      L("Twenty times three is sixty. And sixty divided by two is thirty. So he peels thirty potatoes. And thirty is "
        "between eighteen and thirty-six, just as our check said. Choice number one is our answer.",
        show(g30e, 'Twenty times three is sixty'), show(g30e2, 'sixty divided by two is thirty'),
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
    S('Method 1 · The math way: the triangle value',
      L("Let's try the triangle value once more, on other numbers. Four kilos of apples cost fourteen credits. How much "
        "do six kilos cost? Kilos and credits, four and fourteen, six and a question mark.",
        show(g30k['line'], 'Four kilos of apples'), show(g30k['r1'], 'four and fourteen'), show(g30k['r2'], 'six and a question mark')),
      L("Four to fourteen isn't whole, and four to six isn't whole either. So along the diagonal, six times fourteen, "
        "and we divide by what's left, four. Fourteen and four both divide by two, so it's six times seven, over two. "
        "Six times seven is forty-two. And forty-two divided by two is twenty-one credits.",
        show(g30k['dg'], 'So along the diagonal'), show(g30f, 'six times fourteen'), show(g30f2, "so it's six times seven"),
        show(g30g, 'Six times seven is forty-two'), show(g30g2, 'divided by two is twenty-one'),
        show(g30k['ans'], 'twenty-one credits'))),
    S('Method 2 · The math way: cross-multiplying',
      L("[pause] Now the second way, cross-multiplying. We start again from the table of the question. Twelve minutes and "
        "eighteen potatoes, and twenty minutes. This time we call the missing number x.",
        show(g30x['line'], 'Now the second way'), show(g30x['r1'], 'Twelve minutes and eighteen'),
        show(g30x['r2'], 'This time we call')),
      L("In equal ratios, the two diagonal products are equal. Twelve times x is equal to twenty times eighteen.",
        show(g30x['d1'], 'the two diagonal products'), show(g30x['d2'], 'are equal'), show(g30h, 'Twelve times x is equal')),
      L("Now we work out twenty times eighteen. Two times eighteen is thirty-six. Then times ten, it's three hundred sixty. So twelve x is "
        "three hundred sixty.", show(g30i, 'Two times eighteen is thirty-six'), show(g30i2, 'Then times ten')),
      L("To find x, we divide both sides by twelve. Three hundred sixty divided by twelve is thirty. We know it because twelve times "
        "thirty is three hundred sixty. We get the same thirty.", show(g30j, 'we divide both sides by twelve'),
        show(g30j2, 'divided by twelve is thirty'), show(g30j3, 'twelve times thirty')),
      L("Both ways are the same idea. The triangle value writes the answer straight away, and cross-multiplying builds an "
        "equation first. So when three numbers are known, the rate is the same, and one number is missing, multiply "
        "along the diagonal and divide by what's left. Choice number one is our answer, and I'll see you in the next "
        "question.", mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t22-02 (added: inverse proportion)
# English addition (real exam: 2025_spring_q2_13, 2024_autumn_q1_05, 2026_spring_q1_07). NEW here (full): more or
# fewer first; the ratio table trap (6 2/3); the whole job in worker-days; one worker; the rule "one up, one down,
# the product stays" with a second example (hikers, food). The old 2026-10-09 AI pilot of this video is off.
i_0 = IH('i_0', 'fewer workers $\\to$ more than $10$ days', size=30)
i_tr = IH('i_tr', 'ratio table: $\\ \\frac{4\\cdot10}{6}$', size=30)
i_tr2 = IH('i_tr2', '$=6\\frac{2}{3}$ days', size=30)
i_tr3 = I('i_tr3', 'fewer workers, fewer days? $\\ $No.', size=30)
i_1 = I('i_1', 'whole job $=$ workers $\\times$ days', size=30)
i_2 = IH('i_2', '$6\\cdot10=60$', size=32)
i_3 = IH('i_3', '$4d=60$', size=32)
i_4 = IH('i_4', '$d=60\\div4=15$', size=32)
i_5 = IH('i_5', '$4\\cdot12=48\\ne60$', size=30, col=1)
i_6 = IH('i_6', '$1$ worker: $\\ 10\\cdot6=60$ days', size=30)
i_7 = IH('i_7', '$4$ workers: $\\ 60\\div4=15$ days', size=30)
i_8 = I('i_8', 'One up, one down:', size=30, col=1)
i_8b = I('i_8b', 'the product stays the same', size=30, col=1)
i_9 = IH('i_9', '$8\\cdot6=48$ hiker days', size=30, col=1)
i_10 = IH('i_10', '$48\\div12=4$ days', size=30, col=1)
video('solve-q-r26-t22-02', 'solution', qid='q-r26-t22-02', slides=[
    S('More days or fewer?',
      L("Six workers paint a hall in ten days. All the workers work at the same rate. How many days would four workers "
        "need to paint the same hall?", pt('stem', 'Six workers paint a hall', 'hl', 7.0), voice='calm', pause=0.5),
      L("Before any calculation, let's ask, more days or fewer? Fewer workers paint the same hall. So less gets done "
        "each day, and the job takes longer. So it takes more than ten days.", pt('stem', 'Fewer workers paint'),
        show(i_0, 'So it takes more than ten days')),
      L("So choice number one, six and two thirds, and choice number four, eight, are out. Both are less than ten days.",
        mk('cross', 'choice 1', 'So choice number one'), mk('cross', 'choice 4', 'are out')),
      L("Careful, this is the trap of this question. With the ratio table, we'd multiply four times ten, divide by six, "
        "and get six and two thirds. That's fewer days with fewer workers, which makes no sense. The ratio table works "
        "when the two quantities grow together. Here, when the workers go down, the days go up.",
        show(i_tr, 'With the ratio table'), show(i_tr2, 'and get six and two thirds'),
        show(i_tr3, 'which makes no sense')),
      L("We'll solve it two ways, the math way with the whole job, and then by understanding, with one worker.")),
    S('Method 1 · The math way: the whole job',
      L("Let's start with the math way. It's the same hall, so the whole job stays the same. We measure it in "
        "worker-days. One worker-day is one worker working for one day.", show(i_1, 'the whole job stays the same')),
      L("Six workers for ten days. Six times ten is sixty worker-days. That's the whole hall.",
        show(i_2, 'Six times ten is sixty')),
      L("Now four workers do the same sixty worker-days. So four times the number of days is sixty. The days are sixty "
        "divided by four, fifteen.", show(i_3, 'So four times the number of days'), show(i_4, 'The days are sixty divided')),
      L("Fifteen is more than ten, just as we expected. Choice number three is our answer.",
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Why not twelve, choice number two? Twelve comes from two fewer workers, so two more days. But workers and days "
        "don't change by the same amount. Four workers for twelve days is only forty-eight worker-days, not sixty. Out.",
        show(i_5, 'Four workers for twelve days'), mk('cross', 'choice 2', 'not sixty. Out'))),
    S('Method 2 · Understanding: one worker',
      L("[pause] Now by understanding. We start again from the givens. Six workers paint the hall in ten days. How long "
        "would one worker need alone? Six times as long, because he does the work of six people by himself. Ten times "
        "six is sixty days.", pt('stem', 'Six workers paint the hall'), show(i_6, 'Ten times six is sixty days')),
      L("Now four workers. Four people share the job, so it takes a quarter of the time of one worker. Sixty divided by "
        "four is fifteen days.", show(i_7, 'Sixty divided by four is fifteen')),
      L("So here's the rule. When one quantity goes up and the other goes down, their product stays the same. Workers and "
        "days on the same job. Speed and time on the same road. People and the days a food supply lasts.",
        show(i_8, 'So here\'s the rule'), show(i_8b, 'their product stays the same')),
      L("Let's see it once more. Eight hikers have food for six days. How long does the same food last for twelve hikers? "
        "Eight times six is forty-eight hiker-days. Forty-eight divided by twelve is four days. More hikers, fewer days.",
        show(i_9, 'Eight times six is forty-eight'), show(i_10, 'Forty-eight divided by twelve')),
      L("So before you build a ratio table, ask yourself, when one grows, does the other grow too, or does it shrink? "
        "Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-031 (lesson)
# Hebrew (wp 1417-1426): some problems only test reading comprehension, no hard calculation or equation; a hard
# wording, or a lot of information to see if we panic; work step by step. The details are taught in g032 (label every
# number) and g033 ("or part of").
o_1 = I('o_1', 'Not all at once: $\\ $step by step', size=32)
video('wp-031', 'lesson', slides=[
    S('Read, Organize, Calculate',
      L("Some word problems are really reading-comprehension tests. There's no tricky equation here, and no complicated "
        "calculation. The question just checks that we understand what we read.")),
    S('Reading, not algebra',
      L("Sometimes the wording is a bit hard to follow. And sometimes they just give us a lot of information, to see if "
        "we can handle it without panicking."),
      L("Some students see a long question full of numbers and skip it. Don't. The technique is the same as always. We "
        "don't try to solve it all at once. We go step by step, one piece of information at a time.",
        show(o_1, 'step by step, one piece')),
      L("The calculations themselves are simple. What matters is noticing every detail. A price for every hundred grams, "
        "two small words like or part, and what exactly they ask. Let's see it in two questions. I'll see you in the next "
        "video.")),
])

# ------------------------------------------------------------------------------------------------ wp22-g032 (Hebrew: the family pizza)
# Hebrew (wp 1427-1480): a lot of text, students skip; step by step: the cost of each ingredient (400 g at 5 per 100 g:
# equal ratios, x 4), then price minus cost. One method. REMINDER: equal ratios (g029). NEW at the step: label every
# number (per 100 g); 35 = the cost is a choice (the trap).
s_1 = IH('s_1', 'bread: $\\ 100$ g $\\to4$, $\\ 200$ g $\\to4\\cdot2=8$', size=28)
s_2 = IH('s_2', 'cheese: $\\ 100$ g $\\to8$, $\\ 300$ g $\\to8\\cdot3=24$', size=28)
s_3 = IH('s_3', 'olives: $\\ 6\\cdot\\frac{1}{2}=3$', size=28)
s_4 = IH('s_4', '$8+24=32$', size=30, col=1)
s_5 = IH('s_5', '$32+3=35$ $\\ $ cost', size=30, col=1)
s_6 = IH('s_6', '$47-35=12$', size=30, col=1)
video('solve-wp22-g032', 'solution', qid='wp22-g032', slides=[
    S('Method 1 · The math way: step by step',
      L("A café sells a sandwich for forty-seven credits. Making it uses two hundred grams of bread at four credits per "
        "hundred grams, three hundred grams of cheese at eight credits per hundred grams, and six olives at half a credit "
        "each. Ignoring other costs, what is the selling price minus the ingredient cost?",
        pt('stem', 'A café sells a sandwich', 'hl', 14.0), voice='calm', pause=0.5),
      L("A lot of text, and a lot of numbers. Don't skip it, we'll go step by step. What do they ask? The selling price "
        "minus the cost of the ingredients. So first we need the cost of making one sandwich.",
        pt('stem', 'What do they ask')),
      L("Let's start with the math way, one ingredient at a time. And let's label every number. The bread costs four "
        "credits per hundred grams, not per gram. And we need two hundred grams.", pt('stem', 'The bread costs')),
      L("From a hundred grams to two hundred grams, we multiply by two. The price of every gram stays the same, so it's "
        "equal ratios again, and the price is also multiplied by two. Four times two is eight credits.",
        show(s_1, 'Four times two is eight')),
      L("The cheese costs eight credits per hundred grams, and we need three hundred grams. From a hundred to three "
        "hundred is times three. So the cheese costs eight times three, twenty-four credits.",
        show(s_2, 'eight times three, twenty-four')),
      L("Six olives at half a credit each. Half of six is three credits.", show(s_3, 'Half of six is three')),
      L("Now the total cost. Eight plus twenty-four is thirty-two. Then thirty-two plus three is thirty-five credits.",
        show(s_4, 'Eight plus twenty-four'), show(s_5, 'thirty-two plus three')),
      L("Careful, thirty-five is choice number two. But that's the cost, not what they asked. They asked for the selling "
        "price minus the cost.", mk('cross', 'choice 2', "But that's the cost")),
      L("The sandwich sells for forty-seven. Forty-seven minus thirty-five is twelve credits. Choice number three is our "
        "answer, and I'll see you in the next question.", show(s_6, 'Forty-seven minus thirty-five'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g033 (Hebrew: phone companies)
# Hebrew (wp 1481-1534): easy to understand, the catch is noticing every detail, "or part of it": 22 minutes, then
# half a minute still costs 2; 20 minutes = 2 blocks, 2.5 minutes left = one more block. One method. NEW (full here,
# with a second example, people and vans): "or part of" means round up to the next whole unit.
b_1 = IH('b_1', 'A: $\\ 9$ h $\\to9\\cdot4=36$', size=30)
b_2a = IH('b_2a', '$+\\frac{1}{2}$ h $\\to+4$', size=30)
b_2 = IH('b_2', '$36+4=40$', size=30)
b_3 = IH('b_3', 'B: $\\ 2$ blocks $=8$ h $\\to2\\cdot17=34$', size=30, col=1)
b_4 = IH('b_4', '$+1\\frac{1}{2}$ h $\\to$ one more block', size=30, col=1)
b_5 = IH('b_5', '$34+17=51$', size=30, col=1)
b_6 = IH('b_6', '$51-40=11$', size=30, col=1)
b_7 = IH('b_7', '$50$ people, vans of $12$', size=30)
b_7a = IH('b_7a', '$4\\cdot12=48$, $\\ 50-48=2$ left', size=30)
b_7b = IH('b_7b', '$2$ left $\\to$ one more van: $\\ 5$ vans', size=30)
video('solve-wp22-g033', 'solution', qid='wp22-g033', slides=[
    S('Method 1 · The math way: round up',
      L("Bike shop A charges four credits for every hour or part of an hour. Bike shop B charges seventeen credits for "
        "every four-hour block or part of a block. What is the difference between the two charges for a nine and a half "
        "hour rental?", pt('stem', 'Bike shop A charges', 'hl', 12.0), voice='calm', pause=0.5),
      L("This one is easy to understand. The question is whether we notice every detail. And the detail here is two little "
        "words, or part. Let's see what they mean.", pt('stem', 'two little words')),
      L("Let's start with the math way, shop A. Four credits for every hour or part of an hour. Nine and a half hours is "
        "nine whole hours, and then half an hour. The nine whole hours cost nine times four, thirty-six credits.",
        pt('stem', 'Four credits for every hour'), show(b_1, 'nine times four, thirty-six')),
      L("Now the half hour. Or part of an hour means that any part of an hour costs like a whole hour. Half an hour, a "
        "quarter of an hour, even one minute, it's still four credits. So thirty-six plus four is forty credits.",
        show(b_2a, "it's still four credits"), show(b_2, 'So thirty-six plus four')),
      L("Now shop B. Seventeen credits for every block of four hours, or part of a block. Two blocks cover eight hours, and "
        "two times seventeen is thirty-four credits.", pt('stem', 'Seventeen credits for every block'),
        show(b_3, 'two times seventeen is thirty-four')),
      L("But we rent for nine and a half hours. After eight hours, an hour and a half are left. That's part of a block, so "
        "it costs a whole block, another seventeen. Thirty-four plus seventeen is fifty-one credits.",
        show(b_4, "That's part of a block"), show(b_5, 'Thirty-four plus seventeen')),
      L("They ask for the difference between the two charges. Fifty-one minus forty is eleven. Choice number four is our "
        "answer.", show(b_6, 'Fifty-one minus forty'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 1 · The math way: round up',
      L("So or part of means we round up to the next whole unit. The same idea comes up with people. Fifty people need "
        "vans, and every van seats twelve. Four vans take four times twelve, forty-eight people, and two people are left.",
        show(b_7, 'Fifty people need vans'), show(b_7a, 'Four vans take')),
      L("Those two people still need a van. So the answer is five vans, not four. Whenever a leftover still needs a whole "
        "unit, a whole hour, a whole van, or a whole box, we round up. Choice number four is our answer, and I'll see you "
        "in the next question.", show(b_7b, 'So the answer is five vans'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-034 (lesson: Ratios)
# Hebrew (wp 1535-1749): ratio in everyday talk vs. math (how many times); pens : pencils 2 : 5, "for every 2 ... 5",
# 2.5 times as many; a ratio is a fraction; read in order; expand and reduce, usually reduced; no amounts from a ratio
# (20 & 50, 10 & 25), we know them only from one real number; write 2x and 5x; part of a whole (3/5 of the bottle:
# 3x and 5x); the plain x for the smaller one (2.5 times -> x and 2.5x -> 2x and 5x); the arcs (not crossing); the
# reversed "4 peaches cost like 5 bananas" (choose a number both sides reach: 20). The difference / total divisibility
# and a given difference are taught in g035 and g036. New numbers and names.
w_bead = UNITS('w_bead', [('red', 3), ('blue', 7)], [('red', [('fill', 0, 0, 3, 'orange')]), ('blue', [('fill', 1, 0, 7)])],
               unit=70, boxh=54, labw=110, gap=30)
w_0 = IH('w_0', '$7=2\\frac{1}{3}\\cdot3$', size=30)
w_1 = I('w_1', 'red : blue $=3:7=\\frac{3}{7}$', size=32)
w_arc = None   # the arcs: built below (a figure of its own)
w_2 = IH('w_2', '$6:14=3:7$ $\\quad$ (divide both by $2$)', size=30)
w_3 = I('w_3', '$3:7$ could be $\\ 3$ & $7$, $\\ 6$ & $14$, $\\ 30$ & $70$', size=30)
w_4 = IH('w_4', 'red $=3x,\\ $ blue $=7x$', size=30)
w_4b = IH('w_4b', '$\\frac{3x}{7x}=\\frac{3}{7}$', size=30)
w_5 = IH('w_5', '$3x+7x=10x=50$', size=30)
w_6 = IH('w_6', '$x=50\\div10=5$', size=30)
w_6b = IH('w_6b', 'red $=3\\cdot5=15$', size=30)
w_6c = IH('w_6c', 'blue $=7\\cdot5=35$', size=30)
w_7 = I('w_7', 'Dan drank $\\frac{2}{5}$ of the bottle', size=30)
w_8 = IH('w_8', 'drank $=2x,\\ $ bottle $=5x$', size=30)
w_9 = IH('w_9', 'left $=5x-2x=3x$', size=30)
w_10 = I('w_10', "Ann's salary is $2\\frac{1}{2}$ times Ben's", size=30)
w_11 = IH('w_11', 'Ben $=x,\\ $ Ann $=2\\frac{1}{2}x$', size=30)
w_12 = IH('w_12', 'expand by $2$: $\\ $Ben $=2x,\\ $ Ann $=5x$', size=30)
w_13 = I('w_13', '$3$ mugs cost the same as $8$ plates: $\\quad 3M=8P$', size=30)
w_14 = IH('w_14', '$3$ mugs: $\\ 3\\cdot8=24$', size=30)
w_14b = IH('w_14b', '$8$ plates: $\\ 8\\cdot3=24$', size=30)
w_15 = IH('w_15', '$M:P=8:3$ $\\ $ (reversed)', size=30)


def _arcs():
    """the arcs (Hebrew wp 1680-1690 «מעביר 2 קשתות... לא חוצות»): the names on top in order, the numbers under them;
    left: an arc from each name to its own number - the arcs don't cross (matched in order); right: red with 7 and
    blue with 3 - the lines cross (wrong)"""
    W, H = 900, 256
    base = (_tx(110, 60, 'red', 32) + _tx(200, 60, ':', 32) + _tx(290, 60, 'blue', 32) +
            _tx(110, 205, '3', 38) + _tx(200, 205, ':', 38) + _tx(290, 205, '7', 38) +
            '')
    a1 = '<path d="M 100 76 C 70 115, 70 150, 100 172" fill="none" stroke="%s" stroke-width="3.6"/>' % ORANGE
    a2 = ('<path d="M 300 76 C 330 115, 330 150, 300 172" fill="none" stroke="%s" stroke-width="3.6"/>' % _TEAL
          + _tx(200, 244, "✓ don't cross", 30, _TEAL))
    bad = (_tx(610, 60, 'red', 32) + _tx(700, 60, ':', 32) + _tx(790, 60, 'blue', 32) +
           _tx(610, 205, '3', 38) + _tx(700, 205, ':', 38) + _tx(790, 205, '7', 38) +
           '<line x1="450" y1="20" x2="450" y2="235" stroke="#c9d3da" stroke-width="2"/>' + '<path d="M 615 78 C 680 110, 740 140, 785 172" fill="none" stroke="%s" stroke-width="3.2" stroke-dasharray="8 6"/>' % MV.RED
           + '<path d="M 785 78 C 740 110, 680 140, 615 172" fill="none" stroke="%s" stroke-width="3.2" stroke-dasharray="8 6"/>' % MV.RED
           + _tx(700, 244, '✗ cross: wrong', 30, MV.RED))
    out = [('line', MV._svg(W, H, base, 'red to blue is 3 to 7')), ('a1', MV._svg(W, H, a1, 'red goes with 3')),
           ('a2', MV._svg(W, H, a2, 'blue goes with 7')), ('bad', MV._svg(W, H, bad, 'red with 7: the lines cross'))]
    return MV.items(_layers, 'w_arc', out, col=0, w=900, own=True)


w_arc = _arcs()
video('wp-034', 'lesson', slides=[
    S('Ratios',
      L("Welcome back, and now an important lesson, ratios. Ratios show up all over the quantitative section. Side ratios "
        "in geometry, and rates in work and motion questions. So let's really understand what a ratio is.")),
    S('What a ratio tells you',
      L("In everyday talk, when I say he's tall compared to me, I only know that he's taller. I don't know by how much. "
        "In math, a ratio tells us exactly how many times."),
      L("The ratio of red beads to blue beads is three to seven. That means for every three red beads, there are seven "
        "blue beads.", show(w_bead['line'], 'The ratio of red beads'), show(w_bead['red'], 'for every three red beads'),
        show(w_bead['blue'], 'there are seven blue beads')),
      L("So there are more blue beads. And not just more. Seven is two and a third times three, so there are two and a "
        "third times as many blue beads as red beads.", show(w_0, 'Seven is two and a third times three'))),
    S('A ratio is a fraction',
      L("The first thing to know is that a ratio is really a fraction. Three to seven is three over seven, three divided "
        "by seven. The two dots just mean divided by.", show(w_1, 'a ratio is really a fraction')),
      L("We read a ratio in order. The first name goes with the first number. Red comes first, so red gets the three. Blue "
        "comes second, so blue gets the seven. The exam writes ratios this way, the ratio between the red beads and the "
        "blue beads, so always match the names to the numbers in order."),
      L("Here's a little trick to match them. Draw an arc from the first name to the first number, and another arc from "
        "the second name to the second number. If the arcs don't cross, you matched them right.",
        show(w_arc['line'], 'Draw an arc'), show(w_arc['a1'], 'from the first name to the first number'),
        show(w_arc['a2'], 'from the second name to the second number')),
      L("If we matched red with the seven, and blue with the three, the lines would cross. So crossing lines mean we "
        "matched them wrong.", show(w_arc['bad'], 'the lines would cross')),
      L("And because a ratio is a fraction, we can expand it or reduce it, just like a fraction. Six to fourteen is three "
        "to seven, because we divide both numbers by two. Usually we write a ratio fully reduced, like a fraction.",
        show(w_2, 'Six to fourteen is three to seven'))),
    S('No amounts',
      L("Now the most important thing. From a ratio alone, we can't know the amounts. Three red beads and seven blue? Six "
        "and fourteen? Thirty and seventy? All of them have the ratio three to seven.", show(w_3, 'Three red beads and seven blue')),
      L("We know the amounts only when they give us one real number. A total, a difference, or the size of one of the "
        "groups."),
      L("That's why we write the amounts with x. Red is three x, and blue is seven x. If we cancel the x, three x over "
        "seven x is still three over seven. So the ratio is kept, and now we have amounts we can build an equation with.",
        show(w_4, 'Red is three x'), show(w_4b, 'three x over')),
      L("Let's see it in numbers. Say there are fifty beads in all. Three x plus seven x is ten x, and ten x is fifty. So "
        "x is five. Red is three times five, fifteen. And blue is seven times five, thirty-five.",
        show(w_5, 'Three x plus seven x is ten x'), show(w_6, 'So x is five'),
        show(w_6b, 'Red is three times five'), show(w_6c, 'And blue is seven times five'))),
    S('Part of a whole',
      L("The same idea hides in other wording. Dan drank two fifths of the water in a bottle. That's two out of five.",
        show(w_7, 'Dan drank two fifths')),
      L("The numerator goes with the first thing, what Dan drank. The denominator goes with the whole, the bottle. So Dan "
        "drank two x, and the whole bottle is five x.", show(w_8, 'So Dan drank two x')),
      L("And what's left in the bottle? The whole minus what he drank. Five x minus two x is three x.",
        show(w_9, 'Five x minus two x'))),
    S('The plain x for the smaller one',
      L("Sometimes there's a fraction in it. Ann's salary is two and a half times Ben's salary. Who should be x?",
        show(w_10, "Ann's salary is two and a half")),
      L("Ben is the smaller one, so let's make Ben x. Then Ann is two and a half x. If we made Ann x, Ben would be x "
        "divided by two and a half, and that's a messy fraction.", show(w_11, "so let's make Ben x")),
      L("And we can get rid of the half too. We expand by two. Ben is two x, and Ann is five x. Now the ratio of Ben to Ann "
        "is two to five, whole numbers, much easier to work with.", show(w_12, 'We expand by two'))),
    S('Reversed: the same as',
      L("One more kind of wording. It doesn't look like a ratio, but it is one, and it's reversed. Three mugs cost the "
        "same as eight plates. Which is more expensive, a mug or a plate?", show(w_13, 'Three mugs cost the same')),
      L("Let's pick a total that both sides can reach, twenty-four. Three mugs cost twenty-four if each mug costs eight. "
        "Eight plates cost twenty-four if each plate costs three.", show(w_14, 'Three mugs cost twenty-four'), show(w_14b, 'Eight plates cost twenty-four')),
      L("So a mug costs eight and a plate costs three. The ratio of the mug's price to the plate's price is eight to "
        "three. That's the opposite of the numbers in the sentence.", show(w_15, 'The ratio of the mug')),
      L("Does it make sense? Yes. Fewer mugs cost as much as more plates, so each mug must cost more. The three is next to "
        "the mugs in the sentence, but the mugs get the eight."),
      L("So again, what did we learn? A ratio is a fraction, and we read it in order. A ratio alone gives no amounts, so "
        "we write three x and seven x. And with costs the same as, the ratio is reversed. Now let's see ratios in the "
        "questions. I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ wp22-g035 (Hebrew: boys are 2/7 of the class)
# Hebrew (wp 1717-1739): the common way a ratio appears (a fraction of something else); boys 2x of 7x, girls 5x, the
# difference 3x divides by 3; also boys divide by 2, girls by 5, the class by 7. One method. REMINDER: part of a whole
# (wp-034). NEW here: x counts whole units, so the difference 2x is even; one working case settles "could be" (x = 11).
p_bar = UNITS('p_bar', [('campers', 12)], [('sw', [('fill', 0, 0, 5), ('br', 0, 0, 5, 'swimmers 5x')]),
              ('ru', [('fill', 0, 5, 12, 'orange'), ('br', 0, 5, 12, 'runners 7x')]),
              ('df', [('br', 0, 10, 12, '2x more', 'up')])], unit=34, labw=130, gap=60)
p_1 = IH('p_1', 'swimmers $=5x,\\ $ all $=12x$', size=30)
p_2 = IH('p_2', 'runners $=12x-5x=7x$', size=30)
p_3 = IH('p_3', 'difference $=7x-5x=2x$', size=30)
p_3b = I('p_3b', '$x$ whole, so $2x$ is even', size=32, col=1)
p_4 = IH('p_4', '$2x=22$, $\\ x=11$', size=30)
p_4b = IH('p_4b', 'swimmers $5\\cdot11=55$', size=30)
p_4c = IH('p_4c', 'runners $7\\cdot11=77$', size=30)
p_6 = I('p_6', 'total $=12x$: $\\ $divisible by $5+7=12$', size=32)
p_5 = IH('p_5', '$77-55=22$ ✓', size=30)
video('solve-wp22-g035', 'solution', qid='wp22-g035', slides=[
    S('Method 1 · The math way: ratio units',
      L("At a sports camp, swimmers make up five twelfths of all the campers, and the rest are runners. Which could be the "
        "difference between the numbers of runners and swimmers?", pt('stem', 'At a sports camp', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("They don't tell us how many campers there are, only a fraction. So we can't find the difference exactly. They ask "
        "what it could be. So we'll find a rule that the difference must follow, and rule out the choices that break it.",
        pt('stem: ask', 'They ask what it could be')),
      L("Let's start with the math way, with ratio units. Remember, a fraction of the whole is a ratio. Swimmers are five "
        "out of twelve, so the swimmers are five x, and all the campers are twelve x.",
        show(p_bar['line'], 'a fraction of the whole is a ratio'), show(p_bar['sw'], 'Swimmers are five'),
        show(p_1, 'so the swimmers are five x')),
      L("The rest are runners. Twelve x minus five x is seven x.", show(p_bar['ru'], 'The rest are runners'),
        show(p_2, 'Twelve x minus five x')),
      L("The difference between the runners and the swimmers is seven x minus five x, two x.",
        show(p_bar['df'], 'The difference between the runners'), show(p_3, 'seven x minus five x, two x')),
      L("What does two x tell us? x is the size of one unit, a number of campers, so x is a whole number. Two times a whole "
        "number is always even. So the difference must be even.", show(p_3b, 'Two times a whole'))),
    S('Method 1 · The math way: ratio units',
      L("Now the choices. Twenty-one is odd, so choice number one is out. Fifteen is odd, so choice number three is out. "
        "Nineteen is odd, so choice number four is out.", mk('cross', 'choice 1', 'so choice number one is out'),
        mk('cross', 'choice 3', 'so choice number three is out'), mk('cross', 'choice 4', 'so choice number four is out')),
      L("Only twenty-two is even. And they ask what could be, so one case that really works is enough. Two x is "
        "twenty-two, so x is eleven. Five times eleven is fifty-five swimmers. And seven times eleven is seventy-seven "
        "runners.", show(p_4, 'so x is eleven'), show(p_4b, 'Five times eleven'), show(p_4c, 'And seven times eleven')),
      L("Seventy-seven minus fifty-five is twenty-two. It works. Choice number two is our answer.",
        show(p_5, 'Seventy-seven minus fifty-five'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("This works for every part of a ratio. The swimmers are five x, so their number divides by five. The runners "
        "divide by seven. And all the campers, twelve x, divide by twelve. So when a ratio counts people, the total "
        "always divides by the sum of the ratio numbers. Choice number two is our answer, and I'll see you in the next "
        "question.", show(p_6, 'the total'), mk('tick', 'choice 2', 'Choice number two is our answer, and'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g036 (Hebrew: motorcycle : car 4 : 7)
# Hebrew (wp 1740-1768): a real number is given (the difference) so every amount can be found: 4x, 7x, 3x = 12,000,
# x = 4,000, the sum 11x = 44,000; even if 4 and 7 were swapped, the difference and the sum stay. One method.
# REMINDER: write the ratio with x (wp-034). NEW at the step: x is not the answer.
q_u = UNITS('q_u', [('sofa', 3), ('piano', 10)], [('s', [('fill', 0, 0, 3, 'orange')]), ('p', [('fill', 1, 0, 10)]),
            ('d', [('br', 1, 3, 10, '7 units = 14,000')])], unit=40, labw=110, gap=56, col=1)
q_1 = IH('q_1', 'sofa $=3x,\\ $ piano $=10x$', size=30)
q_2 = IH('q_2', '$10x-3x=7x=14,000$', size=30)
q_3 = IH('q_3', '$x=14,000\\div7=2,000$', size=30)
q_4 = IH('q_4', '$3x+10x=13x$', size=30)
q_5 = IH('q_5', '$13\\cdot2,000=26,000$', size=30)
video('solve-wp22-g036', 'solution', qid='wp22-g036', slides=[
    S('Method 1 · The math way: ratio units',
      L("The prices of a sofa and a piano are in the ratio three to ten. The piano costs fourteen thousand credits more "
        "than the sofa. What is their combined price?", pt('stem', 'The prices of a sofa', 'hl', 8.0), voice='calm', pause=0.5),
      L("This time they give us a real number, the difference. And once we have one real number, we can find every "
        "amount.", pt('stem', 'they give us a real number')),
      L("Let's start with the math way. The ratio of sofa to piano is three to ten. The sofa comes first, so the sofa is "
        "three x, and the piano is ten x.", show(q_u['line'], 'The ratio of sofa to piano'), show(q_u['s'], 'so the sofa is'),
        show(q_u['p'], 'and the piano is ten x'), show(q_1, 'and the piano is ten x')),
      L("The piano costs fourteen thousand more than the sofa. So the difference, ten x minus three x, is fourteen "
        "thousand. Ten x minus three x is seven x.", show(q_u['d'], 'The piano costs fourteen thousand'),
        show(q_2, 'Ten x minus three x is seven x')),
      L("To find x, we divide both sides by seven. Fourteen thousand divided by seven is two thousand.",
        show(q_3, 'Fourteen thousand divided by seven')),
      L("Careful, x is not the answer. They ask for the combined price, the sum. Three x plus ten x is thirteen x. And "
        "thirteen times two thousand is twenty-six thousand credits. Choice number two is our answer.",
        pt('stem: ask', 'They ask for the combined price'), show(q_4, 'Three x plus ten x'),
        show(q_5, 'thirteen times two thousand'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("And here's something nice. Even if we mixed up which one is three and which one is ten, the difference would "
        "still be seven x, and the sum would still be thirteen x. So in this question, the order didn't even matter. "
        "Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer, and'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t22-01 (added: two ratios, a shared group)
# English addition (real exam: 2020_spring_q2_06 nurses : head nurses : secretaries, 2025_autumn_q1_15). NEW here
# (full): the shared group must be the same number in both ratios (why: 3 altos and 4 altos are different units), an
# easy warm-up (1 : 2 and 2 : 3), the trap 2 : 3 : 5 at its step; the second way from the real number (the tenors).
h_1 = IH('h_1', '$S:A=2:3$', size=30)
h_2 = IH('h_2', '$A:T=4:5$', size=30)
h_3 = IH('h_3', '$2:3:5$? $\\ 5x=30$, $\\ 10x=60$', size=30, col=1)
h_3b = IH('h_3b', 'wrong: $\\ 3$ altos and $4$ altos', size=30, col=1)
h_4 = IH('h_4', 'easy: $\\ A:B=1:2$, $\\ B:C=2:3$', size=30, col=1)
h_4b = IH('h_4b', '$A:B:C=1:2:3$', size=30, col=1)
h_4c = IH('h_4c', 'altos: $\\ 3\\cdot4=12$', size=30)
h_5 = IH('h_5', '$S:A=2:3$ $\\ (\\cdot4)$', size=30)
h_5b = IH('h_5b', '$=8:12$', size=30)
h_6 = IH('h_6', '$A:T=4:5$ $\\ (\\cdot3)$', size=30)
h_6b = IH('h_6b', '$=12:15$', size=30)
h_7 = IH('h_7', '$S:A:T=8:12:15$', size=30, col=1)
h_8 = IH('h_8', '$15x=30$, $\\ x=2$', size=30, col=1)
h_9 = IH('h_9', '$8x+12x+15x$', size=30, col=1)
h_9b = IH('h_9b', '$=35x$', size=30, col=1)
h_10 = IH('h_10', '$35\\cdot2=70$', size=30, col=1)
h_11 = IH('h_11', 'altos $=\\frac{4}{5}$ of $30$', size=30)
h_11b = IH('h_11b', '$\\frac{1}{5}\\cdot30=6$', size=30)
h_11c = IH('h_11c', '$4\\cdot6=24$ altos', size=30)
h_12 = IH('h_12', 'sopranos $=\\frac{2}{3}$ of $24$', size=30, col=1)
h_12b = IH('h_12b', '$\\frac{1}{3}\\cdot24=8$', size=30, col=1)
h_12c = IH('h_12c', '$2\\cdot8=16$ sopranos', size=30, col=1)
h_13 = IH('h_13', '$16+24=40$', size=30)
h_13b = IH('h_13b', '$40+30=70$', size=30)
video('solve-q-r26-t22-01', 'solution', qid='q-r26-t22-01', slides=[
    S('Method 1 · The math way: one shared number',
      L("In a choir, the ratio of sopranos to altos is two to three, and the ratio of altos to tenors is four to five. "
        "There are thirty tenors. How many singers are in the choir?", pt('stem', 'In a choir', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("We have two ratios, and one group, the altos, appears in both. That's the key. We'll solve it two ways, the math "
        "way with one shared number, and then the math way starting from the tenors.", pt('stem', 'We have two ratios')),
      L("Let's start with the math way. Here are the two ratios. Sopranos to altos is two to three, and altos to tenors "
        "is four to five.", show(h_1, 'Sopranos to altos is two to three'), show(h_2, 'altos to tenors is four to five')),
      L("Many students glue them together and write two to three to five. That gives sixty, choice number two, and it's "
        "wrong. Why? The three altos in the first ratio and the four altos in the second ratio are different kinds of "
        "units. Three and four aren't the same, so we can't join the ratios yet.", show(h_3, 'two to three to five'),
        show(h_3b, 'The three altos in the first ratio')),
      L("Let's see the idea on easy numbers first. If A to B is one to two, and B to C is two to three, then B is two in "
        "both ratios. So we can write A to B to C as one to two to three.", show(h_4, 'If A to B is one to two'),
        show(h_4b, 'So we can write A to B to C')),
      L("In our question, the altos are three in one ratio and four in the other. So we need one number that both three "
        "and four go into. Three times four is twelve.", show(h_4c, 'Three times four is twelve'))),
    S('Method 1 · The math way: one shared number',
      L("Sopranos to altos is two to three. To turn the three into twelve, we multiply by four. We multiply both numbers, "
        "so the ratio stays the same. Two times four is eight. Three times four is twelve. So the ratio is eight to twelve.",
        show(h_5, 'we multiply by four'), show(h_5b, 'Three times four is twelve')),
      L("Altos to tenors is four to five. To turn the four into twelve, we multiply by three. Four times three is twelve. "
        "Five times three is fifteen. So the ratio is twelve to fifteen.", show(h_6, 'we multiply by three'),
        show(h_6b, 'Five times three is fifteen')),
      L("Now the altos are twelve in both ratios, so we can join them. Sopranos to altos to tenors is eight to twelve to "
        "fifteen.", show(h_7, 'Sopranos to altos to tenors')),
      L("Now the real number. There are thirty tenors, and the tenors are fifteen x. Fifteen x is thirty, so x is two.",
        pt('stem', 'There are thirty tenors'), show(h_8, 'Fifteen x is thirty')),
      L("The whole choir is eight x plus twelve x plus fifteen x. Eight plus twelve is twenty. Twenty plus fifteen is "
        "thirty-five. So that's thirty-five x. Thirty-five times two is seventy singers. Choice number three is our answer.",
        show(h_9, 'The whole choir is'), show(h_9b, "So that's thirty-five x"), show(h_10, 'Thirty-five times two'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · The math way: from the tenors',
      L("[pause] Now a second way. We start again from the givens, and this time from the real number. There are thirty "
        "tenors.", pt('stem', 'There are thirty')),
      L("Altos to tenors is four to five, four altos for every five tenors. So the altos are four fifths of the tenors. A "
        "fifth of thirty is six, and four fifths is four times six, twenty-four altos.", show(h_11, 'So the altos are four fifths'),
        show(h_11b, 'fifth of thirty is six'), show(h_11c, 'four times six')),
      L("Sopranos to altos is two to three. So the sopranos are two thirds of the altos. A third of twenty-four is eight, "
        "and two thirds is sixteen sopranos.", show(h_12, 'So the sopranos are two thirds'),
        show(h_12b, 'A third of twenty-four is eight'), show(h_12c, 'and two thirds is sixteen')),
      L("Altogether, sixteen plus twenty-four is forty. Then forty plus thirty is seventy. We get the same seventy.",
        show(h_13, 'Altogether, sixteen plus twenty-four'), show(h_13b, 'Then forty plus thirty')),
      L("So when two ratios share a group, first make that group the same number in both ratios. Then you can join them "
        "into one ratio. Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t22-03 (added: the part that stays)
# English addition (0 real exam questions; the original practice wp22-p31 and p35 need it - audit_t22.md). NEW here
# (full): find the part nobody touched (the girls), make it the same number of units, the change shows up in units;
# the traps 27 (units) and 44 (the club after). Second way: the equation (cross-multiplying, g030).
k_1 = IH('k_1', 'before $5:4$, $\\ $ after $5:6$', size=30)
k_2 = IH('k_2', 'before $5:4=15:12$ $\\ (\\times3)$', size=30)
k_3 = IH('k_3', 'after $5:6=10:12$ $\\ (\\times2)$', size=30)
k_4 = IH('k_4', 'boys: $\\ 15-10=5$ units', size=30, col=1)
k_5 = IH('k_5', '$5$ units $=10$ boys', size=30, col=1)
k_5b = IH('k_5b', '$1$ unit $=10\\div5=2$', size=30, col=1)
k_6 = IH('k_6', '$15+12=27$ units', size=30, col=1)
k_7 = IH('k_7', '$27\\cdot2=54$', size=30, col=1)
k_8 = IH('k_8', 'boys $5x,\\ $ girls $4x$', size=30)
k_9 = IH('k_9', '$\\frac{5x-10}{4x}=\\frac{5}{6}$', size=34)
k_10 = IH('k_10', '$6(5x-10)=5\\cdot4x$', size=30)
k_11 = IH('k_11', '$30x-60=20x$', size=30, col=1)
k_12 = IH('k_12', '$10x=60$', size=30, col=1)
k_12b = IH('k_12b', '$x=6$', size=30, col=1)
k_13 = IH('k_13', '$5x+4x=9x$', size=30, col=1)
k_13b = IH('k_13b', '$9\\cdot6=54$', size=30, col=1)
video('solve-q-r26-t22-03', 'solution', qid='q-r26-t22-03', slides=[
    S('Method 1 · The math way: the part that stays',
      L("In a club, the ratio of boys to girls is five to four. Then ten boys leave the club, and the ratio of boys to "
        "girls becomes five to six. How many members did the club have at first?", pt('stem', 'In a club', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("The ratio changes because boys leave. The trick in questions like this is to find the part that doesn't change. "
        "Only boys leave, so the girls stay the same. We'll solve it two ways, the math way with ratio units, and then the "
        "math way with an equation.", pt('stem', 'because boys leave')),
      L("Let's start with ratio units. Before, boys to girls is five to four. After, it's five to six. The girls are the "
        "same people in both ratios, but they're four units in one ratio and six units in the other. So first, we make "
        "the girls the same number of units.", show(k_1, 'Before, boys to girls is five to four')),
      L("Four and six both go into twelve. Before, five to four, times three, is fifteen to twelve. After, five to six, "
        "times two, is ten to twelve.", show(k_2, 'Before, five to four, times three'), show(k_3, 'After, five to six, times two')),
      L("Now a unit is the same size in both ratios, because twelve units are the same girls. The boys went from fifteen "
        "units to ten units. That's five units less.", show(k_4, 'The boys went from fifteen units')),
      L("Those five units are the ten boys who left. So five units are ten boys, and one unit is two.",
        show(k_5, 'So five units are ten boys'), show(k_5b, 'and one unit is two')),
      L("At first, the club had fifteen units of boys and twelve units of girls. Fifteen plus twelve is twenty-seven "
        "units. Then twenty-seven times two is fifty-four members.", show(k_6, 'Fifteen plus twelve is twenty-seven'),
        show(k_7, 'twenty-seven times two')),
      L("Careful, twenty-seven is choice number two, but that's the number of units, not people. And forty-four is the "
        "club after the ten boys left. They ask about the club at first. Choice number three is our answer.",
        mk('cross', 'choice 2', "that's the number of units"), mk('cross', 'choice 1', 'And forty-four is the club'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · The math way: an equation',
      L("[pause] Now with an equation. We start again from the givens. Before, boys to girls is five to four, so the boys "
        "are five x and the girls are four x.", show(k_8, 'so the boys are five x')),
      L("Ten boys leave. So the boys are now five x minus ten, and the girls are still four x. The new ratio is five to "
        "six. So five x minus ten, over four x, is equal to five over six.", show(k_9, 'So five x minus ten, over four x')),
      L("Now we cross-multiply. Six times five x minus ten is equal to five times four x. We multiply the six by both "
        "parts. Six times five x is thirty x. Six times ten is sixty. And five times four x is twenty x.",
        show(k_10, 'Now we cross-multiply'), show(k_11, 'And five times four x')),
      L("Now we take twenty x from both sides, and add sixty to both sides. Thirty x minus twenty x is ten x, so ten x is "
        "sixty, and x is six.", show(k_12, 'so ten x is sixty'), show(k_12b, 'and x is six')),
      L("The club at first is five x plus four x, nine x. Nine times six is fifty-four. We get the same answer.",
        show(k_13, 'The club at first is five x'), show(k_13b, 'Nine times six')),
      L("So when one part of a ratio changes, find the part nobody touched. Make it the same number in both ratios, and "
        "then the change shows up in units. Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-037 (lesson)
# Hebrew (wp 1769-1779): building an equation or an expression is needed everywhere (word problems, algebra, geometry -
# an area that is the difference of two areas - even charts); read, build step by step, solve. The tip "x = what they
# ask" (Hebrew: told in the first question, wp 1918-1930) is said here and used in g038.
e_1 = I('e_1', '$1$ read $\\cdot$ $2$ build step by step $\\cdot$ $3$ solve', size=32)
e_2 = I('e_2', 'Tip: $\\ x=$ what they ask', size=32)
video('wp-037', 'lesson', slides=[
    S('Build the Equation',
      L("Welcome back, and now building an equation, or an expression. We need this all through the quantitative "
        "section.")),
    S('Equations everywhere',
      L("In word problems, of course, we translate the story into an equation. But also in algebra, and in geometry. For "
        "example, an area that is the difference of two other areas. We build an expression for it, and then we "
        "calculate it. Sometimes we even need it in charts."),
      L("The method doesn't change. We read the question, we build the equation step by step, slowly, and then we solve "
        "it.", show(e_1, 'We read the question')),
      L("And a small tip. In most questions, it's best to let x be the thing they ask for. Not always, but most questions "
        "are built that way. Then, when we find x, we already have the answer. Let's see it in the questions. I'll see "
        "you in the next video.", show(e_2, 'let x be the thing they ask for'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g038 (Hebrew: 5 rooms, one becomes a store room)
# Hebrew (wp 1780-1930): build slowly, x = workers per room as planned; 4 rooms with x + 2; the number of workers did not
# change, so 5x = 4(x + 2); x = 8 = what they asked; the tip x = what they ask; (the lesson's end: an equation question
# can also be solved by plugging in the answers, wp 2121-2135). Methods: the equation (Hebrew), the removed row
# (an insight, added: the chairs of the removed row were spread 3 to each of the 7 rows), plugging in the answers.
# NEW at the step: moved around -> the total stays.
r_1 = IH('r_1', 'plan: $\\ 8$ rows $\\cdot\\ x=8x$', size=30)
r_2 = IH('r_2', 'actual: $\\ 7$ rows $\\cdot\\ (x+3)=7(x+3)$', size=30)
r_3 = IH('r_3', '$8x=7(x+3)$', size=30, col=1)
r_4 = IH('r_4', '$8x=7x+21$', size=30, col=1)
r_5 = IH('r_5', '$x=21$', size=30, col=1)
r_6 = IH('r_6', '$7$ rows $\\cdot\\ 3$ more $=21$ chairs', size=30)
r_7 = IH('r_7', '$=$ the removed row', size=30)
r_8 = IH('r_8', '(1) $24$: $\\ 8\\cdot24=192$', size=30)
r_8b = IH('r_8b', '$7\\cdot27=140+49=189$, no', size=30)
r_5b = IH('r_5b', '$21+3=24$: $\\ $the new rows', size=30, col=1)
r_7b = IH('r_7b', 'every row: $\\ 21$ chairs', size=30)
r_9 = IH('r_9', '(2) $21$: $\\ 8\\cdot21=168$', size=30)
r_9b = IH('r_9b', '$7\\cdot24=140+28=168$ ✓', size=30)
video('solve-wp22-g038', 'solution', qid='wp22-g038', slides=[
    S('Method 1 · The math way: an equation',
      L("A hall manager plans to set out the same number of chairs in each of eight rows. One row must be removed to make "
        "room for a stage. Each of the seven remaining rows must then hold three more chairs. How many chairs per row were "
        "originally planned?", pt('stem', 'A hall manager plans', 'hl', 12.0), voice='calm', pause=0.5),
      L("They ask how many chairs per row were planned. So, as in the tip, let x be exactly that. We'll solve it three "
        "ways, the math way with an equation, with an insight, and by plugging in the answers.",
        pt('stem: ask', 'They ask how many chairs')),
      L("Let's start with the math way, slowly. The plan was eight rows, with x chairs in each row. So the plan has eight "
        "x chairs.", show(r_1, 'So the plan has eight x')),
      L("In reality, one row was removed, so seven rows are left. And each row gets three more chairs, x plus three. So in "
        "reality there are seven times x plus three chairs.", pt('stem', 'In reality, one row'), show(r_2, 'So in reality there are')),
      L("Why can we write an equation? Because the number of chairs didn't change. They're the same chairs, just set out "
        "in fewer rows. So eight x is equal to seven times x plus three.", show(r_3, 'So eight x is equal')),
      L("This is worth remembering. When things only move around, the total stays the same. When some are removed, the "
        "total drops, and when some are added, it grows."),
      L("Now we open the brackets. Seven times x is seven x. Seven times three is twenty-one. So eight x is seven x "
        "plus twenty-one. Take seven x from both sides, and x is twenty-one.", show(r_4, 'So eight x is seven x'),
        show(r_5, 'Take seven x from both sides')),
      L("What is x? The number of chairs per row in the plan, exactly what they asked. Twenty-four, choice number one, is "
        "a trap. It's the new number per row, twenty-one plus three. Choice number two is our answer.",
        mk('cross', 'choice 1', 'Twenty-four, choice number one'), show(r_5b, 'twenty-one plus three'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Insight: the removed row',
      L("[pause] Now the insight. We start again from the givens, and think about the chairs of the row that was removed. "
        "Those chairs didn't disappear. They were moved to the other rows.", pt('stem', 'the row that was removed')),
      L("Seven rows are left, and each one got three more chairs. Seven times three is twenty-one. So the removed row had "
        "twenty-one chairs.", show(r_6, 'Seven times three is twenty-one'), show(r_7, 'So the removed row had')),
      L("And every row was planned with the same number of chairs. So every row had twenty-one chairs in the plan.",
        show(r_7b, 'So every row had'))),
    S('Method 3 · Plugging in the answers',
      L("[pause] And we can also plug in the answers. We start again from the givens. A choice works if eight rows of it "
        "hold the same number of chairs as seven rows of three more.", pt('stem', 'A choice works if')),
      L("Choice number one, twenty-four. Eight times twenty-four is a hundred ninety-two. Seven rows of twenty-seven are "
        "seven times twenty-seven. That's a hundred forty plus forty-nine, a hundred eighty-nine. Not the same, so it's out.",
        show(r_8, 'Eight times twenty-four'), show(r_8b, 'a hundred eighty-nine'), mk('cross', 'choice 1', "Not the same, so it's out")),
      L("Choice number two, twenty-one. Eight times twenty-one is a hundred sixty-eight. Seven rows of twenty-four are "
        "seven times twenty, a hundred forty, plus seven times four, twenty-eight. Together that's a hundred sixty-eight too. The "
        "same chairs, so it fits. Choice number two is our answer, and I'll see you in the next question.",
        show(r_9, 'Eight times twenty-one'), show(r_9b, "Together that's a hundred sixty-eight"),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t22-20 (added: the gap changes by two)
# 2026-10-01 elite addition (real exam: 2024_spring_q2_03 and 2020_spring_q2_07, "Rona gave Gila 7 ... Gila gave Rona
# 3"). NEW here (full, warm-up first, W10): every item that moves changes the gap by 2; equal = give half the gap; the
# gap can turn around. Methods: understanding the gap (with the picture), the before-and-after table.
g_t = TBL('g_t', ['Dan', 'Ella', 'gap'], ['start', 'gives 1', 'gives 3', 'gives 4'], [
    ('r0', [('c', 0, 0, '10'), ('c', 0, 1, '4'), ('c', 0, 2, '6')]),
    ('r1', [('c', 1, 0, '9'), ('c', 1, 1, '5'), ('c', 1, 2, '4')]),
    ('r2', [('c', 2, 0, '7'), ('c', 2, 1, '7'), ('c', 2, 2, '0')]),
    ('r3', [('c', 3, 0, '6'), ('c', 3, 1, '8'), ('c', 3, 2, 'Ella +2', _TEAL)])], colw=170, labw=170, rowh=64, col=0, size=32)
g_n = OWN(ZL('g_n', -10, 30, [('a', [('ink', 26, 'A +26')]), ('b', [('arrow', 26, 0, '26')]), ('c', [('arrow', 0, -6, '6'), ('ink', -6, 'B +6')])],
             ticks=((0, '0'),), w=580, col=0, title='The gap'), 'g_n')
g_1 = IH('g_1', '$26+6=32$', size=30, col=1)
g_2 = IH('g_2', '$32\\div2=16$', size=30, col=1)
g_3 = IH('g_3', 'B $=10$, $\\ $A $=36$', size=30)
g_3b = IH('g_3b', 'A: $\\ 36-16=20$, $\\ $B: $\\ 10+16=26$', size=30)
g_3c = IH('g_3c', '$26-20=6$ ✓', size=30)
g_h = IH('g_h', '$6\\div2=3$', size=30)
g_4 = IH('g_4', 'before: $\\ $B $=x,\\ $ A $=x+26$', size=30)
g_5 = IH('g_5', 'after: $\\ $A $=x+26-k,\\ $ B $=x+k$', size=30)
g_6 = IH('g_6', '$(x+k)-(x+26-k)=6$', size=30)
g_7 = IH('g_7', '$2k-26=6$', size=30, col=1)
g_8 = IH('g_8', '$2k=32$', size=30, col=1)
g_8b = IH('g_8b', '$k=16$', size=30, col=1)
video('solve-q-r26-t22-20', 'solution', qid='q-r26-t22-20', slides=[
    S('Method 1 · Understanding: the gap',
      L("Shelf A has twenty-six more books than shelf B. Some books are moved from shelf A to shelf B. After the move, "
        "shelf B has six more books than shelf A. How many books were moved?", pt('stem', 'Shelf A has twenty-six', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("Books move from one shelf to the other, and the whole question is about the gap between the shelves. We'll solve "
        "it two ways, by understanding the gap, and then the math way with a before-and-after table.",
        pt('stem', 'Books move from one shelf')),
      L("Let's start by understanding what happens to a gap when one side gives to the other. Let's use easy numbers first. Dan has "
        "ten cards and Ella has four. The gap is six.", show(g_t['line'], 'Easy numbers first'), show(g_t['r0'], 'Dan has ten cards')),
      L("Dan gives Ella one card. Now Dan has nine and Ella has five. The gap went from six to four. One card, and the gap "
        "changed by two. Why? Because Dan lost one, and Ella gained one.", show(g_t['r1'], 'Dan gives Ella one card')),
      L("Dan gives three cards. He has seven, and she has seven. They're equal. So to make two people equal, you give half "
        "the gap. Half of six is three.", show(g_t['r2'], 'Dan gives three cards'), show(g_h, 'Half of six is three')),
      L("And if he gives four? Dan has six, and Ella has eight. Now Ella is ahead by two. The gap went down to zero, turned "
        "around, and grew on the other side.", show(g_t['r3'], 'And if he gives four'))),
    S('Method 1 · Understanding: the gap',
      L("Now our shelves. At the start, A is twenty-six ahead. If we only wanted them equal, we'd move half the gap, "
        "thirteen books. That's choice number two. But B must end up ahead, so we need more.",
        show(g_n['line'], 'Now our shelves'), show(g_n['a'], 'A is twenty-six ahead'), mk('cross', 'choice 2', "That's choice number two")),
      L("So the gap goes from twenty-six down to zero, and then on to six on the other side, where B is six ahead.",
        show(g_n['b'], 'So the gap goes from twenty-six'), show(g_n['c'], 'and then on to six')),
      L("In all, the gap changes by twenty-six plus six, thirty-two. Careful, thirty-two is choice number four, but it's "
        "the change in the gap, not the number of books.", show(g_1, 'twenty-six plus six, thirty-two'),
        mk('cross', 'choice 4', 'not the number of books')),
      L("Every book that moves changes the gap by two. So the number of books is thirty-two divided by two, sixteen.",
        show(g_2, 'thirty-two divided by two')),
      L("Let's check it. Say B had ten books, so A had thirty-six. After sixteen books move, A has twenty and B has "
        "twenty-six. B has six more, just like the question says. Choice number three is our answer.",
        show(g_3, 'Say B had ten books'), show(g_3b, 'After sixteen books move'),
        show(g_3c, 'B has six more'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · The math way: before and after',
      L("[pause] Now the math way. We start again from the givens. Let B be x, the smaller shelf. Then A is x plus "
        "twenty-six.", show(g_4, 'Let B be x')),
      L("Let's call the number of books that move k. A loses k, so A has x plus twenty-six minus k. B gains k, so B has x "
        "plus k.", show(g_5, 'A loses k')),
      L("After the move, B has six more than A. So B minus A is six.", show(g_6, 'So B minus A is six')),
      L("Now we open the brackets. x minus x is zero, so the x's cancel. k minus minus k is two k. And the minus twenty-six "
        "stays. So two k minus twenty-six is six.", show(g_7, 'So two k minus twenty-six')),
      L("We add twenty-six to both sides. Two k is thirty-two, so k is sixteen. We get the same sixteen.",
        show(g_8, 'Two k is thirty-two'), show(g_8b, 'so k is sixteen')),
      L("So when one side gives to the other, each item changes the gap by two. To make them equal, give half the gap. "
        "Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp-039 (lesson)
# Hebrew (wp 1931-1934): "give it to the little guy" («תן למסכן», the approved English version), a very important
# technique when building equations; it sounds funny but really helps, even strong students slip. Taught in g039.
l_1 = I('l_1', 'Building an equation: $\\ $twice $\\cdot$ three times $\\cdot$ ages', size=30)
video('wp-039', 'lesson', slides=[
    S('Give It to the Little Guy',
      L("Now a technique that sounds a bit funny, but it really saves points, even for strong students. We call it give it "
        "to the little guy.")),
    S('Where it helps',
      L("We use it when we build an equation with words like twice, or three times. It comes up a lot in age questions, "
        "and in questions about money.", show(l_1, 'with words like twice')),
      L("Let's see it in an age question. And after it, one more question about building, this time with an inequality. "
        "I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ wp22-g039 (Hebrew: Uri and Yaron)
# Hebrew (wp 1935-2056): x = the younger one, the one they ask about (no minus signs); the mistake: jumping to the
# equation; stop and add a row to the table for "3 years ago"; "give it to the little guy" (4 and 8); open the
# brackets, x = 7 = what they ask; plugging in the answers (rule out 3, mark the 4th); the sharp-eyed tip: a gap of 4
# and double -> 4 and 8. Three methods, in her order. NEW (full): the then-and-now table, the times-two goes on the
# smaller side (4 and 8 + the why), the gap stays and the ratio changes.
y_t = TBL('y_t', ['Tom', 'Maya'], ['now', '5 years ago'], [
    ('r0', [('c', 0, 0, 'x'), ('c', 0, 1, 'x + 9')]), ('r1', [('c', 1, 0, 'x − 5'), ('c', 1, 1, 'x + 4')])],
    colw=150, labw=170, col=1, size=28)
y_t2 = TBL('y_t2', ['Tom', 'Maya'], ['now', '5 years ago'], [
    ('r0', [('c', 0, 0, 'x'), ('c', 0, 1, 'x + 9')]), ('r1', [('c', 1, 0, 'x − 5'), ('c', 1, 1, 'x + 4')])],
    colw=150, labw=170, col=1, size=28)
y_0 = IH('y_0', 'Tom: $\\ x-5$', size=30)
y_0b = IH('y_0b', 'Maya: $\\ x+9-5=x+4$', size=30)
y_0c = IH('y_0c', 'gap: $\\ (x+4)-(x-5)=9$', size=30)
y_1 = I('y_1', 'Twice? $\\times2$ on the smaller side', size=30)
y_2 = IH('y_2', '$4$ and $8$: $\\ 2\\cdot4=8$', size=30)
y_3 = IH('y_3', '$2(x-5)=x+4$', size=30)
y_4 = IH('y_4', '$2x-10=x+4$', size=30)
y_5 = IH('y_5', '$x=14$', size=30)
y_6 = IH('y_6', '(1) $9\\to4$, $\\ $Maya $8$', size=30)
y_6b = IH('y_6b', 'gap $8-4=4$, no', size=30)
y_7 = IH('y_7', '(2) $12\\to7$, $\\ $Maya $14$', size=30)
y_7b = IH('y_7b', 'gap $14-7=7$, no', size=30)
y_8 = IH('y_8', '(3) $14\\to9$, $\\ $Maya $18$', size=30, col=1)
y_8b = IH('y_8b', 'gap $18-9=9$ ✓', size=30, col=1)
y_9a = IH('y_9a', 'gap $9$, $\\ $Maya $=2\\cdot$Tom', size=30)
y_9 = IH('y_9', '$9$ and $18$', size=30)
y_10 = IH('y_10', 'Tom $t$, $\\ $Maya $2t$', size=30, col=1)
y_10b = IH('y_10b', 'gap $2t-t=t=9$', size=30, col=1)
y_11 = IH('y_11', 'Tom now: $\\ 9+5=14$', size=30)
video('solve-wp22-g039', 'solution', qid='wp22-g039', slides=[
    S('Method 1 · The math way: a table',
      L("Maya is nine years older than her cousin Tom. Five years ago, Maya was twice Tom's age. How old is Tom now?",
        pt('stem', 'Maya is nine years older', 'hl', 6.0), voice='calm', pause=0.5),
      L("They ask for Tom's age now. So let's make Tom now our x. We'll solve it three ways, the math way with a table, "
        "plugging in the answers, and an insight.", pt('stem: ask', "They ask for Tom's age now")),
      L("Let's start with the math way. Why Tom and not Maya? Because they ask about Tom, and Tom is the younger one. So "
        "Tom is x, Maya is x plus nine, and there are no minus signs.", show(y_t['line'], 'Why Tom and not Maya'),
        show(y_t['r0'], 'So Tom is x')),
      L("Here's where a lot of students go wrong. They read five years ago, Maya was twice Tom's age, and they jump straight "
        "to the equation. Stop. Before the equation, add a row to the table for five years ago."),
      L("Five years ago, everyone was five years younger. Tom was x minus five. Maya was x plus nine, minus five, which "
        "is x plus four.", show(y_0, 'Tom was x minus five'), show(y_0b, 'Maya was x plus nine'),
        show(y_t['r1'], 'which is x plus four')),
      L("And look. The gap between them is still nine. Everyone gets older at the same speed, so the gap stays the same. "
        "Only the ratio between their ages changes.", show(y_0c, 'The gap between them is still nine'))),
    S('Method 1 · The math way: a table',
      L("Now the equation. Five years ago, Maya was twice Tom's age. So who gets the times two? Many students give it to "
        "Maya, because the sentence says Maya was twice. But that's backwards.", show(y_t2['line'], 'Now the equation'),
        show(y_t2['r0'], 'Five years ago, Maya'), show(y_t2['r1'], 'So who gets the times two')),
      L("Think of four and eight. Eight is twice four. To make them equal, which one do we multiply by two? The four, the "
        "smaller one. Two times four is eight. So the times two goes to the little guy.",
        show(y_2, 'Think of four and eight'), show(y_1, 'So the times two goes')),
      L("Five years ago, the little guy was Tom, x minus five. So two times x minus five is equal to x plus four.",
        show(y_3, 'So two times x minus five')),
      L("Now we open the brackets. Two times x is two x. Two times five is ten. So two x minus ten is x plus four. We "
        "take x from both sides, and add ten to both sides. x is fourteen.", show(y_4, 'So two x minus ten'),
        show(y_5, 'x is fourteen')),
      L("x is Tom's age now, exactly what they asked. Choice number three is our answer.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. We start again from the givens. For each choice, we go back five years, "
        "double Tom, and check that the gap is nine, as the question says.", pt('stem', 'We start again from the givens')),
      L("Choice number one, Tom is nine now. Five years ago he was four, and Maya was twice that, eight. But the gap "
        "between eight and four is four, not nine. Out.", show(y_6, 'Five years ago he was four'), show(y_6b, 'But the gap'),
        mk('cross', 'choice 1', 'not nine. Out')),
      L("Choice number two, twelve. Five years ago Tom was seven, and Maya was fourteen. The gap is seven. Out.",
        show(y_7, 'Five years ago Tom was seven'), show(y_7b, 'The gap is seven'), mk('cross', 'choice 2', 'The gap is seven. Out')),
      L("Choice number three, fourteen. Five years ago Tom was nine, and Maya was eighteen. The gap is nine. It fits. In "
        "the exam, you'd mark it and move on.", show(y_8, 'Five years ago Tom was nine'), show(y_8b, 'The gap is nine'),
        mk('tick', 'choice 3', 'The gap is nine. It fits'))),
    S('Method 3 · Insight',
      L("[pause] And an insight. We start again from the givens. The gap is always nine. And five years ago, Maya was "
        "twice Tom. A gap of nine, and one of them twice the other. That can only be nine and eighteen.",
        pt('stem', 'The gap is always nine'), show(y_9a, 'And five years ago, Maya was'),
        show(y_9, 'That can only be nine and eighteen')),
      L("Why only those? If Tom is some number, and Maya is twice it, the gap is twice the number minus the number, which "
        "is the number itself. So Tom was nine, the size of the gap.", show(y_10, 'If Tom is some number'), show(y_10b, 'the gap is twice the number')),
      L("Careful, nine is choice number one, but that's Tom five years ago. Now he's nine plus five, fourteen.",
        show(y_11, 'Now he\'s nine plus five')),
      L("And this works for anything that grows by the same amount, like two plants that each grow the same number of "
        "centimeters. The gap stays, and only the ratio changes. Choice number three is our answer, and I'll see you in "
        "the next question.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g040 (Hebrew: 50 shekels, 4 bottles not 5)
# Hebrew (wp 2057-2116): "could be" -> a range; 4B <= 50 -> B <= 12.5 (rules out two), 50 < 5B -> B > 10; an
# inequality instead of an equation; plugging in the answers (9: 9 x 5 = 45 also fits -> out). Inequalities are
# taught later (topic 12), so the symbol and dividing by a positive number are explained here in one sentence each.
# NEW here: "enough for 6 but not 7" = two inequalities; "exactly enough still counts".
d_1 = IH('d_1', '$6p\\le105$', size=30)
d_2a = IH('d_2a', '$6\\cdot17=102$, $\\ 3$ left, $\\ \\frac{3}{6}=\\frac{1}{2}$', size=30)
d_2 = IH('d_2', '$p\\le105\\div6=17\\frac{1}{2}$', size=30)
d_3 = IH('d_3', '$7p>105$', size=30)
d_4 = IH('d_4', '$p>105\\div7=15$', size=30)
d_z = ZL('d_z', 13.5, 21, [('a', [('shade', 15, 17.5)]), ('b', [('pt', 17, '17')])],
         ticks=((15, '15'), (17.5, '17½'), (20, '20')), w=540, col=1, title='The price')
d_tc = IH('d_tc', 'enough for $6$, not for $7$:', size=30, col=1)
d_tc2 = IH('d_tc2', '$6p\\le105<7p$', size=32, col=1)
d_5 = IH('d_5', '(1) $15$: $\\ 6\\cdot15=90\\le105$ ✓', size=30)
d_5b = IH('d_5b', '$7\\cdot15=105$, $\\ $not more, no', size=30)
d_6 = IH('d_6', '(2) $17$: $\\ 6\\cdot17=102\\le105$ ✓', size=30)
d_6b = IH('d_6b', '$7\\cdot17=70+49=119>105$ ✓', size=30)
video('solve-wp22-g040', 'solution', qid='wp22-g040', slides=[
    S('Method 1 · The math way: two inequalities',
      L("Dana has a hundred five credits. That is enough for six identical movie tickets, but not enough for seven. Which "
        "could be the price of one ticket?", pt('stem', 'Dana has a hundred five', 'hl', 7.0), voice='calm', pause=0.5),
      L("They ask what the price could be. So we're not looking for one exact price, but for a range of prices that fit. "
        "We'll solve it two ways, the math way with two inequalities, and then by plugging in the answers.",
        pt('stem: ask', 'They ask what the price could be')),
      L("Let's start with the math way. We call the price of one ticket p. Enough for six tickets means six tickets cost a "
        "hundred five or less. Exactly a hundred five still counts as enough. So six p is at most a hundred five.",
        show(d_1, 'So six p is at most')),
      L("This symbol means smaller than or equal to. It's like an equation, but instead of equals, we have at most. And "
        "like in an equation, we may divide both sides by six. Dividing by a positive number keeps the symbol the same "
        "way."),
      L("A hundred five divided by six. Six times seventeen is a hundred two, and three are left. Three sixths is a half. "
        "So p is at most seventeen and a half.", show(d_2a, 'Six times seventeen is a hundred two'),
        show(d_2, 'So p is at most')),
      L("So a ticket costs seventeen and a half or less. Eighteen and twenty cost more, so choice numbers three and four "
        "are out.", mk('cross', 'choice 3', 'Eighteen and twenty'), mk('cross', 'choice 4', 'are out'))),
    S('Method 1 · The math way: two inequalities',
      L("Now the second part. Not enough for seven tickets means seven tickets cost more than a hundred five. So seven p "
        "is bigger than a hundred five.", pt('stem', 'Not enough for seven tickets'), show(d_3, 'So seven p is bigger')),
      L("We divide both sides by seven. A hundred five divided by seven is fifteen. That's because seven times fifteen is a "
        "hundred five. So p is bigger than fifteen.", show(d_4, 'We divide both sides by seven')),
      L("Bigger than fifteen, not equal to it. So fifteen itself is out, choice number one.",
        mk('cross', 'choice 1', 'So fifteen itself is out')),
      L("So the price is more than fifteen, and at most seventeen and a half. Only seventeen is in that range. Choice "
        "number two is our answer.", show(d_z['line'], 'So the price is more than fifteen'), show(d_z['a'], 'and at most seventeen'),
        show(d_z['b'], 'Only seventeen is in that range'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. We start again from the givens. Each price must pass two tests. Six "
        "tickets cost a hundred five or less, and seven tickets cost more than a hundred five.",
        pt('stem', 'Each price must pass two tests')),
      L("Choice number one, fifteen. Six tickets cost ninety, which is enough. But seven tickets cost a hundred five, "
        "exactly what she has. So she can buy seven, and the question says she can't. Out.",
        show(d_5, 'Six tickets cost ninety'), show(d_5b, 'But seven tickets cost'), mk('cross', 'choice 1', "and the question says she can't")),
      L("Choice number two, seventeen. Six tickets cost a hundred two, which is enough. Seven tickets cost seven times "
        "seventeen. That's seventy plus forty-nine, a hundred nineteen. That's more than a hundred five, so it's not enough. "
        "Both tests pass.", show(d_6, 'Six tickets cost a hundred two'),
        show(d_6b, 'a hundred nineteen')),
      L("Let's keep the idea from this question. Enough for six, but not enough for seven, gives two inequalities. Six "
        "tickets cost the money or less, and seven tickets cost more than the money. So the price is squeezed between "
        "two numbers. Whenever you see enough for some number, but not for one more, write both of them.",
        show(d_tc, 'gives two inequalities'), show(d_tc2, 'seven tickets cost more than the money')),
      L("A question that builds an equation or an inequality can almost always be solved by plugging in the answers too. "
        "Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ r26-t22-shortcuts (lesson)
# Hebrew (wp 2155-2163, advanced learning): general problems are those of no special type (not motion, percents, work,
# where a formula guides us); here we build an equation, or understand and calculate, or use techniques we'll see.
a_1 = I('a_1', 'Build an equation, or understand and calculate', size=32)
video('r26-t22-shortcuts', 'lesson', slides=[
    S('Shortcuts Ahead',
      L("Welcome back, and now the advanced questions of this topic, general problems.")),
    S('No formula here',
      L("Into this topic go all the problems that are not of one special type. Not motion, not percents, and not work. "
        "In those topics there's usually a formula that guides us. Here there isn't."),
      L("So we deal with each question by what's in it. Sometimes we build an equation, and sometimes we just understand "
        "what they want and calculate.", show(a_1, 'Sometimes we build an equation')),
      L("And almost every question here also has a psychometric shortcut. A size estimate, plugging in numbers, or a small "
        "insight. Try each question yourself first, and then watch. I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ wp22-g042 (Hebrew: one gold coin, mango / apples / plums)
# Hebrew (wp 2164-2204): the easy fruits first; equal ratios with the triangle value for the awkward one (4 / 2.5), get
# rid of the decimal by x 2, not x 10; then an estimate (more than one coin, less than two coins -> rule out three).
# REMINDERS: the ratio table and the triangle value (g029, g030), estimation (topic 51).
n_1 = IH('n_1', '$8$ kiwis: $\\ 2$ credits', size=30, col=1)
n_2 = IH('n_2', '$5$ limes: $\\ 1$ credit', size=30, col=1)
n_t = TBL('n_t', ['Credits', 'Pineapples'], ['', ''], [
    ('r1', [('c', 0, 0, '1'), ('c', 0, 1, '1.5')]), ('r2', [('q', 1, 0), ('c', 1, 1, '2')]),
    ('dg', [('diag', (0, 0), (1, 1))]), ('ans', [('cover', 1, 0, '4/3')])], colw=170, col=1)
n_3a = IH('n_3a', '$?=\\frac{2\\cdot1}{1.5}$', size=30)
n_3 = IH('n_3', '$=\\frac{2\\cdot2}{1.5\\cdot2}$', size=30)
n_3c = IH('n_3c', '$=\\frac{4}{3}$', size=30)
n_4 = IH('n_4', '$2+1=3=\\frac{9}{3}$', size=30)
n_5 = IH('n_5', '$\\frac{9}{3}+\\frac{4}{3}=\\frac{13}{3}$', size=30)
n_6 = IH('n_6', 'kiwis and limes: $\\ 2+1=3$', size=30)
n_7 = IH('n_7', 'pineapples $>1$, $\\ $total $>3+1=4$', size=30)
n_8 = IH('n_8', '$2$ credits $\\to3$ pineapples, so pineapples $<2$', size=28)
n_9 = IH('n_9', 'total $<3+2=5$', size=30)
n_10 = IH('n_10', '$4<\\frac{13}{3}=4\\frac{1}{3}<5$', size=30)
video('solve-wp22-g042', 'solution', qid='wp22-g042', slides=[
    S('Method 1 · The math way: equal ratios',
      L("One credit buys four kiwis, one and a half pineapples, or five limes, with costs proportional to quantity. What "
        "is the cost of eight kiwis, two pineapples, and five limes? Fractional credits may be paid.",
        pt('stem', 'One credit buys four kiwis', 'hl', 10.0), voice='calm', pause=0.5),
      L("Three fruits, three different prices, and they ask for the cost of a mix. Proportional means the same rate, so "
        "equal ratios. We'll solve it two ways, the math way with equal ratios, and then with an estimate.",
        pt('stem: ask', 'they ask for the cost of a mix')),
      L("Let's start with the math way, with the easy fruits first. One credit buys four kiwis. We need eight kiwis, twice "
        "as many, so two credits.", show(n_1, 'We need eight kiwis')),
      L("One credit buys five limes, and we need exactly five limes. So that's one credit.", show(n_2, 'So that\'s one credit')),
      L("Now the awkward one, the pineapples. One credit buys one and a half pineapples, and we need two. Let's put it in a "
        "ratio table, one column for credits and one for pineapples. One credit, one and a half pineapples. And a question mark for two "
        "pineapples.", show(n_t['line'], "Let's put it in a"), show(n_t['r1'], 'One credit, one and a half'),
        show(n_t['r2'], 'And a question mark')),
      L("From one and a half to two isn't a whole multiplier, so we use the triangle value. Multiply along the diagonal, "
        "two times one, and divide by what's left, one and a half.", show(n_t['dg'], 'Multiply along the diagonal'), show(n_3a, 'and divide by what')),
      L("One and a half on the bottom isn't nice, so let's get rid of the half. We could multiply the top and the bottom by "
        "ten, but that only makes bigger numbers. Times two is enough. Two times two is four. One and a half times two "
        "is three. So four thirds of a credit.", show(n_3, 'Times two is enough'), show(n_3c, 'So four thirds of a credit'),
        show(n_t['ans'], 'four thirds of a credit'))),
    S('Method 1 · The math way: equal ratios',
      L("Now we add it all up. Two credits for the kiwis and one for the limes, that's three. Three is nine thirds, and nine "
        "thirds plus four thirds is thirteen thirds. Choice number one is our answer.", show(n_4, "that's three"),
        show(n_5, 'nine thirds plus four thirds'), mk('tick', 'choice 1', 'Choice number one is our answer'))),
    S('Method 2 · Estimation',
      L("[pause] Now let's estimate, and save the fraction work. We start again from the givens. The kiwis and the limes "
        "are easy, two credits and one credit, three credits together.", show(n_6, 'three credits together')),
      L("Now the pineapples. One credit buys one and a half, and we need two. That's more than one and a half, so the "
        "pineapples cost more than one credit. So the total is more than three plus one, more than four. Choice number "
        "three, three credits, is out.", show(n_7, 'So the total is more than'), mk('cross', 'choice 3', 'is out')),
      L("Now the upper limit. Two credits buy two times one and a half, three pineapples. We need only two. So the "
        "pineapples cost less than two credits, and the total is less than three plus two, less than five.",
        show(n_8, 'Two credits buy'), show(n_9, 'less than three plus two')),
      L("So the total is between four and five. Five and six, choice numbers two and four, are out. Thirteen thirds is four "
        "and a third, between four and five. Choice number one is our answer, and I'll see you in the next question.",
        mk('cross', 'choice 2', 'Five and six'), mk('cross', 'choice 4', 'are out'), show(n_10, 'Thirteen thirds is four'),
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g043 (Hebrew: 128 cadets, 7/8 stay)
# Hebrew (wp 2205-2247): understand and calculate; the group as a rectangle cut into 8, 7 stay; 7/8 of 128 by splitting
# 128 = 80 + 48; stage 2 starts with 112 -> 98; then the "little insight": write the whole exercise first,
# 128 x 7/8 x 7/8 = 2 x 49. NEW (full): the fraction bar for a story; a stage acts on what's left; write it all first.
v_b1 = UNITS('v_b1', [('level 1', 4)], [('k', [('fill', 0, 0, 3), ('br', 0, 0, 4, '160', 'up')]),
             ('v', [('in', 0, 0, '40'), ('in', 0, 1, '40'), ('in', 0, 2, '40'), ('in', 0, 3, '40')])], unit=90, labw=120, gap=40, col=1)
v_b2 = UNITS('v_b2', [('level 2', 4)], [('k', [('fill', 0, 0, 3), ('br', 0, 0, 4, '120', 'up')]),
             ('v', [('in', 0, 0, '30'), ('in', 0, 1, '30'), ('in', 0, 2, '30'), ('in', 0, 3, '30')])], unit=90, labw=120, gap=40, col=1)
v_0 = IH('v_0', '$160\\div2=80$', size=30)
v_1 = IH('v_1', '$80\\div2=40$', size=30)
v_2 = IH('v_2', '$40\\cdot3=120$', size=30)
v_2t = IH('v_2t', '$160-40-40=80$? $\\ $No', size=30)
v_3 = IH('v_3', '$120\\div4=30$', size=30)
v_4 = IH('v_4', '$30\\cdot3=90$', size=30)
v_5 = IH('v_5', '$160\\cdot\\frac{3}{4}\\cdot\\frac{3}{4}$', size=32)
v_6a = IH('v_6a', '$3\\cdot3=9$, $\\ 4\\cdot4=16$', size=30)
v_6 = IH('v_6', '$=160\\cdot\\frac{9}{16}$', size=32)
v_7 = IH('v_7', '$160\\div16=10$', size=30, col=1)
v_8 = IH('v_8', '$10\\cdot9=90$', size=30, col=1)
video('solve-wp22-g043', 'solution', qid='wp22-g043', slides=[
    S('Method 1 · The math way: level by level',
      L("A video game starts with a hundred sixty players. At the end of each level, three quarters of the players who "
        "began that level are still in the game. How many players are still in the game after two levels?",
        pt('stem', 'A video game starts', 'hl', 9.0), voice='calm', pause=0.5),
      L("Here we just have to understand what they want, and calculate. We'll solve it two ways, the math way level by "
        "level, and then with an insight, writing the whole exercise first.", pt('stem: ask', 'understand what they want')),
      L("Let's start with the math way. A hundred sixty players start level one. At the end of the level, three quarters "
        "of them are still in. Let's picture them as a bar, cut into four equal parts. Three of the parts stay.",
        show(v_b1['line'], "Let's picture them as a bar"), show(v_b1['k'], 'Three of the parts stay')),
      L("One part is a quarter of a hundred sixty. Half of a hundred sixty is eighty, and half again is forty. So one part "
        "is forty, and three parts are three times forty, a hundred twenty.", show(v_0, 'Half of a hundred sixty'),
        show(v_1, 'and half again is forty'), show(v_b1['v'], 'So one part'), show(v_2, 'three times forty'))),
    S('Method 1 · The math way: level by level',
      L("Careful, this is where the trap is. If we took forty away twice, we'd get eighty, choice number two. But level two "
        "works on the players who began level two, a hundred twenty, not a hundred sixty. So now a hundred twenty players "
        "are the whole bar.", show(v_2t, 'If we took forty away twice'), mk('cross', 'choice 2', 'choice number two'),
        show(v_b2['line'], 'So now a hundred twenty'), show(v_b2['k'], 'are the whole bar')),
      L("A quarter of a hundred twenty is thirty, and three quarters is three times thirty, ninety. So ninety players are "
        "still in the game after two levels. Choice number three is our answer.", show(v_3, 'A quarter of a hundred twenty'),
        show(v_b2['v'], 'is thirty'), show(v_4, 'three times thirty'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Insight: write it all first',
      L("[pause] Now the insight. We start again from the givens. Instead of calculating as we go, let's first write the "
        "whole exercise. A hundred sixty, times three quarters for level one, times three quarters for level two.",
        show(v_5, 'A hundred sixty, times three quarters')),
      L("We multiply the fractions. Three times three is nine on top. Four times four is sixteen on the bottom. So it's "
        "a hundred sixty times nine sixteenths.", show(v_6a, 'Three times three is nine'), show(v_6, 'So it\'s a hundred sixty times')),
      L("And now it's easy to see. A hundred sixty divided by sixteen is ten. And ten times nine is ninety.",
        show(v_7, 'A hundred sixty divided by sixteen'), show(v_8, 'ten times nine is ninety')),
      L("So when a question has several stages, don't rush to calculate each one. Write the whole exercise first. The "
        "numbers usually cancel nicely. Choice number three is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g044 (Hebrew: girls = 4/5 of the boys)
# Hebrew (wp 2248-2275): an equation G = 4/5 B -> G / B = 4/5 (a ratio is a fraction); matching the ratio units
# directly; then plug in 5 boys and 4 girls -> 4 out of 9. REMINDERS: a ratio is a fraction, the numerator goes with
# the first (wp-034), plugging in (topic 51). NEW at the step: part out of the other part vs. part out of everyone.
c_1 = IH('c_1', '$C=\\frac{5}{8}\\cdot T$', size=32)
c_2 = IH('c_2', '$\\frac{C}{T}=\\frac{5}{8}$', size=32)
c_2b = IH('c_2b', '$C:T=5:8$', size=32, col=1)
c_3 = IH('c_3', '$C=5x,\\ T=8x$', size=30, col=1)
c_4 = IH('c_4', 'all $=5x+8x=13x$', size=30, col=1)
c_5 = IH('c_5', '$\\frac{5x}{13x}$', size=32, col=1)
c_5b = IH('c_5b', '$=\\frac{5}{13}$', size=32, col=1)
c_6 = IH('c_6', '$T=8$', size=30)
c_7 = IH('c_7', '$C=\\frac{5}{8}\\cdot8=5$', size=30)
c_8 = IH('c_8', 'all $=8+5=13$', size=30)
c_9 = IH('c_9', 'coaches: $\\ \\frac{5}{13}$', size=30)
video('solve-wp22-g044', 'solution', qid='wp22-g044', slides=[
    S('Method 1 · The math way: a ratio',
      L("At a training center, there are five eighths as many coaches as trainees. What fraction of all the people are "
        "coaches?", pt('stem', 'At a training center', 'hl', 6.0), voice='calm', pause=0.5),
      L("This question is all about matching the ratio units, what goes with what, and then reading carefully what they "
        "ask. We'll solve it two ways, the math way with a ratio, and then by plugging in numbers.",
        pt('stem', 'matching the ratio units')),
      L("Let's start with the math way. There are five eighths as many coaches as trainees. So the coaches, C, are five "
        "eighths of the trainees, T. C is equal to five eighths times T.", show(c_1, 'C is equal to five eighths')),
      L("We divide both sides by T. C over T is five eighths. And a ratio is a fraction, so the ratio of coaches to "
        "trainees is five to eight. Or we match the units directly. The numerator goes with the coaches, and the "
        "denominator goes with the trainees.", show(c_2, 'C over T is five eighths'), show(c_2b, 'trainees is five to eight')),
      L("So the coaches are five x and the trainees are eight x. But careful, they don't ask for coaches out of trainees. "
        "That would be five eighths, choice number one, and that's the trap. They ask for coaches out of all the people.",
        show(c_3, 'So the coaches are five x'), mk('cross', 'choice 1', "and that's the trap"),
        pt('stem: ask', 'out of all the people')),
      L("All the people are five x plus eight x, thirteen x. So the coaches are five x out of thirteen x. The x cancels, "
        "and we get five thirteenths. Choice number four is our answer.", show(c_4, 'All the people are'),
        show(c_5, 'So the coaches are five x out of'), show(c_5b, 'and we get five thirteenths'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. No amounts are given, only a fraction, so we "
        "may choose the amounts ourselves. The coaches are five eighths of the trainees. So let's choose eight trainees, "
        "because then five eighths of them is a whole number.", show(c_6, "let's choose eight trainees")),
      L("Five eighths of eight is five, so there are five coaches. Everyone together, eight plus five, is thirteen "
        "people.", show(c_7, 'Five eighths of eight is five'), show(c_8, 'eight plus five, is thirteen')),
      L("So the coaches are five out of thirteen, five thirteenths. Five to eight compares one group with the other "
        "group. Five out of thirteen compares one group with everyone. Choice number four is our answer, and I'll see you "
        "in the next question.", show(c_9, 'So the coaches are five out of thirteen'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g045 (Hebrew: peaches for export / the local market)
# Hebrew (wp 2276-2350): two groups, different fractions; x and 3x possible, but plugging in is easier; 1 and 3, then
# "we chose the numbers, so we may change them" (4 and 12, the smallest that divides by 4); 5 of 16; then the estimate
# (between the two fractions: less than 1/3, more than 1/4). REMINDER: plugging in (topic 51). NEW here: a mix lands
# between the two groups' fractions.
m_1 = IH('m_1', 'cafe $1$, $\\ $supermarket $2$', size=30)
m_1b = IH('m_1b', 'supermarket: $\\ \\frac{1}{2}\\cdot2=1$ ✓', size=30)
m_1c = IH('m_1c', 'cafe: $\\ \\frac{1}{5}\\cdot1$? $\\ $No', size=30)
m_2 = IH('m_2', 'cafe $5$, $\\ $supermarket $10$', size=30)
m_3 = IH('m_3', 'cafe: $\\ \\frac{1}{5}\\cdot5=1$', size=30)
m_3b = IH('m_3b', 'supermarket: $\\ \\frac{1}{2}\\cdot10=5$', size=30)
m_4 = IH('m_4', 'whole wheat: $\\ 1+5=6$', size=30)
m_4b = IH('m_4b', 'all: $\\ 5+10=15$', size=30, col=1)
m_5 = IH('m_5', '$\\frac{6}{15}=\\frac{2}{5}$', size=32, col=1)
m_6 = IH('m_6', 'both $\\frac{1}{2}$: $\\ $all $\\frac{1}{2}$', size=30)
m_6b = IH('m_6b', 'cafe only $\\frac{1}{5}$: $\\ $all $<\\frac{1}{2}$', size=30)
m_7 = IH('m_7', 'both $\\frac{1}{5}$: $\\ $all $\\frac{1}{5}$', size=30, col=1)
m_7b = IH('m_7b', 'supermarket $\\frac{1}{2}$: $\\ $all $>\\frac{1}{5}$', size=30, col=1)
m_z = ZL('m_z', 0.1, 0.75, [('a', [('shade', 0.2, 0.5)]), ('b', [('pt', 0.4, '2/5')])],
         ticks=((0.2, '1/5'), (0.5, '1/2'), (0.7, '7/10')), w=540, col=1, title='Between a fifth and a half')
video('solve-wp22-g045', 'solution', qid='wp22-g045', slides=[
    S('Method 1 · Plugging in numbers',
      L("A bakery sends twice as many loaves to supermarkets as to cafés. One half of the supermarket loaves and one fifth "
        "of the café loaves are whole-wheat. What fraction of all the loaves is whole-wheat?",
        pt('stem', 'A bakery sends twice', 'hl', 9.0), voice='calm', pause=0.5),
      L("There are two groups of loaves, and each group has a different fraction of whole-wheat. We'll solve it two ways, "
        "by plugging in numbers, and then with an estimate.", pt('stem', 'two groups of loaves')),
      L("We could write the cafés as x and the supermarkets as two x, and build an equation. But no amounts are given, only "
        "fractions, so plugging in numbers is more comfortable. Let's try one loaf for the cafés and two for the "
        "supermarkets. That's twice as many, good.", show(m_1, "Let's try one loaf")),
      L("Half of the supermarket loaves are whole-wheat. Half of two is one, fine. A fifth of the café loaves. A fifth of "
        "one loaf? That's no good, we can't have part of a loaf.", show(m_1b, 'Half of two is one'),
        show(m_1c, 'A fifth of one loaf')),
      L("No problem. We chose the numbers, so we may change them. The cafés need a number that a fifth can come out of, "
        "and the smallest is five. So five café loaves, and twice that, ten supermarket loaves.",
        show(m_2, 'So five café loaves'))),
    S('Method 1 · Plugging in numbers',
      L("A fifth of five is one whole-wheat loaf. Half of ten is five whole-wheat loaves. Together, one plus five is six "
        "whole-wheat loaves. All the loaves are five plus ten, fifteen loaves.", show(m_3, 'A fifth of five is one'),
        show(m_3b, 'Half of ten is five'), show(m_4, 'Together, one plus five'), show(m_4b, 'All the loaves are')),
      L("So that's six out of fifteen. Six fifteenths reduces by three to two fifths. Choice number one is our answer.",
        show(m_5, 'Six fifteenths reduces'), mk('tick', 'choice 1', 'Choice number one is our answer'))),
    S('Method 2 · Estimation',
      L("[pause] Now let's estimate. We start again from the givens. If both groups were half whole-wheat, then all the "
        "loaves together would be half whole-wheat. But the café group is only a fifth, less than a half. So all together "
        "it's less than a half.", show(m_6, 'If both groups were half'),
        show(m_6b, 'But the café group')),
      L("A half itself, choice number two, is out. And seven tenths is more than a half, so choice number three is out "
        "too.", mk('cross', 'choice 2', 'A half itself'), mk('cross', 'choice 3', 'so choice number three is out')),
      L("Now the other end. If both groups were a fifth whole-wheat, all together would be a fifth. But the supermarket "
        "group is a half, more than a fifth. So all together it's more than a fifth. One sixth is less than a fifth, so "
        "choice number four is out.", show(m_7, 'If both groups were a fifth'), show(m_7b, 'But the supermarket'), mk('cross', 'choice 4', 'so choice number four is out')),
      L("Only two fifths is between a fifth and a half. This is worth remembering. When two groups are mixed, the fraction "
        "of the whole mix always lands between the fractions of the two groups. Choice number one is our answer, and "
        "I'll see you in the next question.", show(m_z['line'], 'Only two fifths is between'), show(m_z['a'], 'between a fifth and a half'),
        show(m_z['b'], 'When two groups are mixed'), mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g046 (Hebrew: silver and gold coins)
# Hebrew (wp 2351-2440): a very hard question; we don't know which leftover is which, so we check; 18 = 4/5 -> 18 / 4
# not whole -> swap; units: 6/7 = 18 -> a seventh is 3 -> 21; 4/5 = 8 -> 10; 31. Then the estimate: we don't care
# which pile, 26 left, a little was given -> a bit more than 26; 27 too few (at least one coin from each), 52 double
# (would mean giving half), 156 too many. Two methods, in her order.
u_b1 = UNITS('u_b1', [('vanilla', 6)], [('k', [('fill', 0, 0, 5), ('br', 0, 0, 5, '14?')])], unit=60, labw=120, gap=40, col=1)
u_b2 = UNITS('u_b2', [('vanilla', 6), ('chocolate', 3)], [
    ('k1', [('fill', 0, 0, 5), ('br', 0, 0, 5, '10')]), ('v1', [('in', 0, i, '2') for i in range(6)]),
    ('k2', [('fill', 1, 0, 2, 'orange'), ('br', 1, 0, 2, '14')]), ('v2', [('in', 1, i, '7') for i in range(3)])],
    unit=56, labw=150, gap=60, col=1)
u_1 = IH('u_1', 'vanilla $14$? $\\ \\frac{1}{6}=14\\div5$', size=30)
u_1b = IH('u_1b', 'not whole, so no', size=30)
u_2 = IH('u_2', 'vanilla: $\\ \\frac{1}{6}=10\\div5=2$', size=30)
u_2b = IH('u_2b', '$6\\cdot2=12$', size=30)
u_3 = IH('u_3', 'chocolate: $\\ \\frac{1}{3}=14\\div2=7$', size=30)
u_3b = IH('u_3b', '$3\\cdot7=21$', size=30)
u_4 = IH('u_4', '$12+21=33$', size=30, col=1)
u_5 = IH('u_5', '$10+14=24$ left', size=30)
u_6 = IH('u_6', '(2) $26$: $\\ $sold $\\ge\\frac{1}{6}\\cdot26>4$', size=30)
u_6b = IH('u_6b', 'left $<22$, $\\ $not $24$', size=30)
u_7 = IH('u_7', '(1) $48$: $\\ $sold $\\le\\frac{1}{3}\\cdot48=16$', size=30, col=1)
u_7b = IH('u_7b', 'left $\\ge32$, $\\ $not $24$', size=30, col=1)
u_8 = IH('u_8', '(3) $72$: $\\ $even more left', size=30, col=1)
video('solve-wp22-g046', 'solution', qid='wp22-g046', slides=[
    S('Method 1 · The math way: two options',
      L("A baker has chocolate and vanilla cupcakes. She sells one third of the chocolate cupcakes and one sixth of the "
        "vanilla cupcakes, always selling whole cupcakes. The cupcakes left are ten of one flavor and fourteen of the "
        "other, in an unknown order. How many cupcakes did she have at first?", pt('stem', 'A baker has chocolate', 'hl', 14.0),
        voice='calm', pause=0.5),
      L("The hard part here is that we don't know which leftover belongs to which flavor. So we'll simply check both "
        "options. We'll solve it two ways, the math way checking both options, and then with an estimate.",
        pt('stem', 'which leftover belongs')),
      L("Let's start with the math way. She sold a sixth of the vanilla cupcakes, so what's left of the vanilla is five "
        "sixths. Let's say fourteen vanilla cupcakes are left. Then fourteen is five sixths of the vanilla.",
        show(u_b1['line'], 'so what\'s left of the vanilla'), show(u_b1['k'], 'Then fourteen is five sixths')),
      L("Five sixths are fourteen cupcakes, so one sixth would be fourteen divided by five. That's not a whole number. But "
        "she sells only whole cupcakes, so one sixth must be a whole number of cupcakes. So fourteen can't be the "
        "vanilla.", show(u_1, 'fourteen divided by five'), show(u_1b, "That's not a whole number"), pt('stem', 'she sells only whole cupcakes')),
      L("So it's the other way round. Ten vanilla cupcakes are left, and fourteen chocolate.")),
    S('Method 1 · The math way: two options',
      L("First the vanilla. Ten is five sixths, so one sixth is ten divided by five, two cupcakes. She sold one sixth, so we give it "
        "back. Six sixths are six times two, twelve vanilla cupcakes.", show(u_b2['line'], 'Ten is five sixths'),
        show(u_b2['k1'], 'so one sixth is'), show(u_2, 'ten divided by five'), show(u_b2['v1'], 'two cupcakes'),
        show(u_2b, 'Six sixths are six times two')),
      L("Now the chocolate. She sold a third, so two thirds are left. Fourteen is two thirds, so one third is seven. Three thirds "
        "are three times seven, twenty-one chocolate cupcakes.", show(u_b2['k2'], 'Fourteen is two thirds'),
        show(u_3, 'so one third is seven'), show(u_b2['v2'], 'Three thirds'), show(u_3b, 'three times seven')),
      L("At first she had twelve plus twenty-one, thirty-three cupcakes. Choice number four is our answer.",
        show(u_4, 'twelve plus twenty-one'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Estimation',
      L("[pause] Now let's estimate, and we don't even care which pile is which. We start again from the givens. Ten plus "
        "fourteen is twenty-four cupcakes left.", show(u_5, 'Ten plus fourteen')),
      L("She sold a third of one flavor and a sixth of the other. That's not much, so she started with a bit more than "
        "twenty-four. Let's check the choices."),
      L("Choice number two, twenty-six. She sold at least a sixth of every flavor, so at least a sixth of all the "
        "cupcakes. A sixth of twenty-six is more than four. So more than four were sold, and fewer than twenty-two would "
        "be left. But twenty-four are left. Out.", show(u_6, 'A sixth of twenty-six'), show(u_6b, 'fewer than twenty-two'), mk('cross', 'choice 2', 'are left. Out')),
      L("Choice number one, forty-eight. She sold at most a third of every flavor, so at most a third of all. A third of "
        "forty-eight is sixteen. So at least thirty-two would be left, not twenty-four. Out.",
        show(u_7, 'A third of'), show(u_7b, 'So at least thirty-two'), mk('cross', 'choice 1', 'not twenty-four. Out')),
      L("And choice number three, seventy-two, is even bigger, so even more would be left. Out too. Only thirty-three is "
        "left. Choice number four is our answer, and I'll see you in the next question.", show(u_8, 'so even more would be left'),
        mk('cross', 'choice 3', 'Out too'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g047 (Hebrew: two kindergartens)
# Hebrew (wp 2441-2496): an equation (x and 2x, move 2, 3/5, brackets, x = 16 is not the answer, 3x = 48); then the
# psychometric insight of divisibility (the total divides by 3, then by 8 -> three ruled out with no calculation).
# REMINDERS: the plain x for the smaller one (wp-034), the little guy (g039), ratio units -> the total divides by the
# sum (g035). Divisibility by 3 is checked by plain multiplication (the digit-sum sign is topic 15, later).
z_1 = IH('z_1', 'B $=x,\\ $ A $=4x$', size=30)
z_2 = IH('z_2', 'after: $\\ $A $=4x-6$', size=30)
z_2b = IH('z_2b', 'B $=x+6$', size=30)
z_3 = IH('z_3', '$2(x+6)=4x-6$', size=30)
z_4 = IH('z_4', '$2x+12=4x-6$', size=30, col=1)
z_5 = IH('z_5', '$12+6=18$', size=30, col=1)
z_5b = IH('z_5b', '$18=2x$, $\\ x=9$', size=30, col=1)
z_6 = IH('z_6', 'total $=x+4x=5x$', size=30)
z_6b = IH('z_6b', '$5\\cdot9=45$', size=30)
z_7 = IH('z_7', 'before: $\\ 1+4=5$ parts', size=30)
z_7b = IH('z_7b', 'total divisible by $5$', size=30)
z_8 = IH('z_8', 'after: $\\ 1+2=3$ parts', size=30)
z_8b = IH('z_8b', 'total divisible by $3$', size=30)
z_9 = IH('z_9', '$40=39+1$, $\\ 39=3\\cdot13$, $\\ $no', size=30, col=1)
z_9b = IH('z_9b', '$50=48+2$, $\\ 48=3\\cdot16$, $\\ $no', size=30, col=1)
z_10 = IH('z_10', '$45=5\\cdot9$ ✓', size=30, col=1)
z_10b = IH('z_10b', '$45=3\\cdot15$ ✓', size=30, col=1)
video('solve-wp22-g047', 'solution', qid='wp22-g047', slides=[
    S('Method 1 · The math way: an equation',
      L("A school has two buses. Bus A carries four times as many students as bus B. Six students move from bus A to bus "
        "B. Afterwards, bus B carries half as many students as bus A. How many students are on the two buses altogether?",
        pt('stem', 'A school has two buses', 'hl', 11.0), voice='calm', pause=0.5),
      L("Students move from one bus to the other, and the ratio changes. We'll solve it two ways, the math way with an "
        "equation, and then by understanding, with divisibility, which needs almost no calculation.",
        pt('stem', 'Students move from one bus')),
      L("Let's start with the math way. Bus A carries four times as many as bus B. Remember, the plain x goes to the "
        "smaller one. B is the smaller bus, so B is x and A is four x. No fractions, and no dividing later.",
        show(z_1, 'so B is x and A is four x')),
      L("Six students move from A to B. A loses six, so A has four x minus six. B gains six, so B has x plus six.",
        show(z_2, 'A loses six'), show(z_2b, 'B gains six')),
      L("Afterwards, B carries half as many as A. So B is the little guy, and it gets the times two. Two times B is equal "
        "to A. Two times x plus six is equal to four x minus six.", pt('stem', 'Afterwards, B carries half'),
        show(z_3, 'Two times x plus six')),
      L("Now we open the brackets. So two x plus twelve is equal to four x minus six. We take two x from both sides, and add six to "
        "both sides. Twelve plus six is eighteen, so eighteen is two x, and x is nine.", show(z_4, 'Two x plus twelve'),
        show(z_5, 'Twelve plus six is eighteen'), show(z_5b, 'so eighteen is two x'))),
    S('Method 1 · The math way: an equation',
      L("Careful, don't mark nine. That's bus B at the start, and they ask about both buses together. Moving students "
        "doesn't change the total, so the total is x plus four x, five x. Five times nine is forty-five. Choice number two "
        "is our answer.", pt('stem: ask', 'they ask about both buses'), show(z_6, 'so the total is x plus four x'), show(z_6b, 'Five times nine'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Understanding: divisibility',
      L("[pause] Now by understanding. We start again from the givens. At the start, A has four times B. So for every one "
        "student on B, there are four on A. One part and four parts, five parts in all. So the total divides by five.",
        pt('stem', 'At the start, A has four times'), show(z_7, 'One part and four parts'), show(z_7b, 'So the total')),
      L("Forty-eight doesn't divide by five, so choice number three is out.", mk('cross', 'choice 3', 'Forty-eight')),
      L("After the move, B has half of A. One part and two parts, three parts in all. And the total didn't change, because "
        "the students only moved. So the total also divides by three.", show(z_8, 'One part and two parts'), show(z_8b, 'So the total')),
      L("Forty is thirty-nine plus one. And thirty-nine is three times thirteen. So forty doesn't divide by three. Fifty "
        "is forty-eight plus two. And forty-eight is three times sixteen. So fifty doesn't either. Choice numbers one and "
        "four are out.", show(z_9, 'Forty is thirty-nine plus one'), show(z_9b, 'Fifty is forty-eight'), mk('cross', 'choice 1', 'Choice numbers one and'),
        mk('cross', 'choice 4', 'four are out')),
      L("Only forty-five is left, and it divides by both. Forty-five is five times nine. It's also three times fifteen. So when "
        "a total is split in a ratio, it divides by the sum of the ratio numbers, before and after. Choice number two is "
        "our answer, and I'll see you in the next question.", show(z_10, 'Forty-five is five times nine'), show(z_10b, "It's also three times"),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g048 (Hebrew: pocket money, a fixed sum + per task)
# Hebrew (wp 2497-2565): two equations, subtract (K cancels), 4M = 120; plugging in the answers (50: 400 > 290 -> 50
# and 60 out; 30: fee 50 in both months); the insight (4 tasks more, 120 more -> 30 each). Three methods, her order.
# REMINDER: subtracting two equations (topic 6). NEW here (TC): a fixed part disappears in the difference.
f_1 = IH('f_1', '$f+7h=385$', size=30)
f_2 = IH('f_2', '$f+4h=250$', size=30)
f_3 = IH('f_3', 'subtract: $\\ 3h=135$', size=30)
f_4 = IH('f_4', '$h=135\\div3=45$', size=30)
f_5 = IH('f_5', '(3) $65$: $\\ 4\\cdot65=260$', size=30)
f_5b = IH('f_5b', '$260>250$, $\\ $no', size=30)
f_6 = IH('f_6', '(4) $50$: $\\ $fee $250-200=50$', size=30)
f_6b = IH('f_6b', '$7\\cdot50=350$, $\\ $fee $385-350=35$, no', size=30)
f_7 = IH('f_7', '(2) $45$: $\\ $fee $250-180=70$', size=30)
f_7b = IH('f_7b', '$7\\cdot45=315$', size=30)
f_7c = IH('f_7c', 'fee $385-315=70$ ✓', size=30)
f_8 = IH('f_8', '$7-4=3$ hours', size=30)
f_9 = IH('f_9', '$385-250=135$ credits', size=30)
f_10 = IH('f_10', '$135\\div3=45$', size=30)
video('solve-wp22-g048', 'solution', qid='wp22-g048', slides=[
    S('Method 1 · The math way: two equations',
      L("A plumber charges a fixed call-out fee plus the same amount for each hour of work. A seven-hour job costs three "
        "hundred eighty-five credits, and a four-hour job costs two hundred fifty credits. What is the charge per hour?",
        pt('stem', 'A plumber charges', 'hl', 11.0), voice='calm', pause=0.5),
      L("Each bill has two parts, a fixed fee that's the same every time, and a charge for every hour. We'll solve it "
        "three ways, the math way with two equations, by plugging in the answers, and with an insight.",
        pt('stem', 'Each bill has two parts')),
      L("Let's start with the math way. We call the fixed fee f, and the charge per hour h. The seven-hour job is the fee "
        "plus seven hours, so f plus seven h is three hundred eighty-five.", show(f_1, 'so f plus seven h')),
      L("The four-hour job is the fee plus four hours. So f plus four h is two hundred fifty.", show(f_2, 'So f plus four h')),
      L("Two equations, and the fee f is the same in both. Remember, if we subtract one equation from the other, the f "
        "cancels. Seven h minus four h is three h. And three hundred eighty-five minus two hundred fifty is a hundred "
        "thirty-five.", show(f_3, 'And three hundred eighty-five minus')),
      L("We divide both sides by three. A hundred thirty-five divided by three is forty-five. That's because three times "
        "forty-five is a hundred thirty-five. So the charge is forty-five credits an hour. Choice number two is our "
        "answer.", show(f_4, 'We divide both sides by three'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers. We start again from the givens. For each hourly charge, we find the fee "
        "from one job, and check that the other job gives the same fee. Let's start with the four-hour job, because four "
        "is easier to multiply by.", pt('stem', "Let's start with the four-hour job")),
      L("Choice number three, sixty-five. Four hours cost sixty-five times four, two hundred sixty. But the whole bill was "
        "two hundred fifty, less than the hours alone. Impossible, so it's out.", show(f_5, 'Four hours cost sixty-five'), show(f_5b, 'But the whole bill'),
        mk('cross', 'choice 3', "Impossible, so it's out")),
      L("Choice number four, fifty. Four hours cost two hundred, so the fee is two hundred fifty minus two hundred, fifty. "
        "Now the seven-hour job. Seven times fifty is three hundred fifty. So the fee there is three hundred eighty-five "
        "minus three hundred fifty, thirty-five. The fee must be the same in both jobs, and fifty isn't thirty-five. Out.",
        show(f_6, 'so the fee is two hundred fifty minus'), show(f_6b, 'So the fee there'), mk('cross', 'choice 4', "and fifty isn't thirty-five"))),
    S('Method 2 · Plugging in the answers',
      L("Choice number two, forty-five. Four hours cost a hundred eighty, so the fee is seventy. Seven hours cost three "
        "hundred fifteen, so the fee is three hundred eighty-five minus three hundred fifteen, seventy again. The same fee "
        "in both jobs. It fits.", show(f_7, 'so the fee is seventy'), show(f_7b, 'Seven hours cost three hundred fifteen'), show(f_7c, 'seventy again'), mk('tick', 'choice 2', 'It fits'))),
    S('Method 3 · Insight: what changed?',
      L("[pause] And the insight. We start again from the givens, and ask what changed between the two jobs. The fixed fee "
        "didn't change. Only the hours changed.", pt('stem', 'what changed between the two jobs')),
      L("Seven hours minus four hours is three more hours. And three hundred eighty-five minus two hundred fifty is a "
        "hundred thirty-five more credits.", show(f_8, 'Seven hours minus four hours'), show(f_9, 'a hundred thirty-five more credits')),
      L("So three extra hours cost a hundred thirty-five extra credits. One hour costs a hundred thirty-five divided by "
        "three, forty-five.", show(f_10, 'One hour costs')),
      L("So when there's a fixed amount plus a price for each item, compare the two cases. The fixed part disappears in the "
        "difference. Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g049 (Hebrew: 6 apples and 10 bananas)
# Hebrew (wp 2566-2620): first understand: an apple and a banana cost 10 - each alone? no; 2 and 2? yes, 20; 2 and 1? no;
# then the same factor (x 1.5 on both, so the result too); or reduce by 2 and multiply by 3. Two methods.
# NEW (full, with the easy case first): every part times the same number -> the total too; one equation with two
# unknowns gives only such multiples (taught again in the exam-tools lesson).
x_1 = IH('x_1', '$1$ large $+\\ 1$ small $=10$', size=30)
x_1b = IH('x_1b', '$1+9$, $\\ 4+6$, $\\ 5+5$: $\\ $each alone? no', size=30)
x_2 = IH('x_2', '$2$ large $+\\ 2$ small $=2\\cdot10=20$ ✓', size=30)
x_3 = IH('x_3', '$2$ large $+\\ 1$ small $=\\ ?$', size=30)
x_4 = IH('x_4', '$9\\to12=9+3$, $\\ 3=\\frac{1}{3}\\cdot9$', size=30)
x_5 = IH('x_5', '$6\\to8=6+2$, $\\ 2=\\frac{1}{3}\\cdot6$', size=30)
x_6 = IH('x_6', '$\\frac{1}{3}\\cdot240=80$', size=30)
x_6b = IH('x_6b', '$240+80=320$', size=30)
x_7 = IH('x_7', '$9L+6S=240$', size=30)
x_8 = IH('x_8', '$\\div3$: $\\ 3L+2S=80$', size=30)
x_9 = IH('x_9', '$\\times4$: $\\ 12L+8S$', size=30)
x_9b = IH('x_9b', '$=80\\cdot4=320$', size=30)
video('solve-wp22-g049', 'solution', qid='wp22-g049', slides=[
    S('Method 1 · Understanding: the same factor',
      L("Nine large crates and six small crates weigh two hundred forty kilos altogether. All large crates weigh the same, "
        "and all small crates weigh the same. How much do twelve large and eight small crates weigh?",
        pt('stem', 'Nine large crates', 'hl', 10.0), voice='calm', pause=0.5),
      L("One equation, and two unknowns, the large crate and the small crate. Before we solve, let's understand one idea "
        "about questions like this. We'll solve it two ways, by understanding, and then the math way.",
        pt('stem', 'Nine large crates and six')),
      L("Let's solve it by understanding, with easy numbers first. Say one large crate and one small crate weigh ten kilos "
        "together. Can we know what each one weighs? No. It could be one and nine, or four and six, or five and five.",
        show(x_1, 'Say one large crate'), show(x_1b, 'It could be one and nine')),
      L("But what do two large crates and two small crates weigh? That we can know. We doubled every part, so the weight "
        "doubles too, twenty kilos.", show(x_2, 'We doubled every part')),
      L("And two large crates and one small crate? That we can't know, because only one part was doubled. The other part "
        "stayed the same.", show(x_3, 'And two large crates and one')),
      L("So the rule is, when every part is multiplied by the same number, the total is multiplied by that number too. So "
        "in our question, we ask, did both counts grow by the same factor?")),
    S('Method 1 · Understanding: the same factor',
      L("From nine large crates to twelve. Twelve is nine plus three, and three is a third of nine. So the large crates "
        "grew by a third of themselves.", show(x_4, 'Twelve is nine plus three')),
      L("From six small crates to eight. Eight is six plus two, and two is a third of six. They also grew by a third.",
        show(x_5, 'Eight is six plus two')),
      L("Both counts grew by a third, so the weight grows by a third too. A third of two hundred forty is eighty, and two "
        "hundred forty plus eighty is three hundred twenty. Choice number two is our answer.",
        show(x_6, 'A third of two hundred forty'), show(x_6b, 'and two hundred forty plus eighty'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · The math way: shrink, then grow',
      L("[pause] Now the math way. We start again from the given equation. Nine L plus six S is two hundred forty.",
        show(x_7, 'Nine L plus six S')),
      L("Nine, six and two hundred forty all divide by three. So we divide every term of the equation by three. Three L "
        "plus two S is eighty.", show(x_8, 'Three L plus two S is eighty')),
      L("Now we multiply every term by four. Three L times four is twelve L. Two S times four is eight S. And eighty times "
        "four is three hundred twenty. That's exactly the crates they asked about.", show(x_9, 'Two S times four'), show(x_9b, 'And eighty times four')),
      L("We may do this, because we divided and multiplied every term, on both sides. Choice number two is our answer, and "
        "I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp22-g050 (Hebrew: Asher and Betty, 48 candies)
# Hebrew (wp 2621-2683): two equations (A + B = 48, A - 8 = B + 8 -> A - B = 16, add them), then the insight: start
# from the end (equal at the end: 24 and 24, go back in time). REMINDER: adding two equations (topic 6). NEW (TC):
# when the end of the story is simple, start there.
t_1 = IH('t_1', '$n+e=70$', size=30)
t_2 = IH('t_2', '$n-15=e+15$', size=30)
t_3 = IH('t_3', '$n-e=30$', size=30)
t_4 = IH('t_4', 'add: $\\ 2n=70+30=100$', size=30, col=1)
t_4b = IH('t_4b', '$n=50$', size=30, col=1)
t_5 = IH('t_5', '$e=70-50=20$', size=30)
t_6 = IH('t_6', '$\\frac{50}{20}$', size=32, col=1)
t_6b = IH('t_6b', '$=\\frac{5}{2}$', size=32, col=1)
t_7 = IH('t_7', 'end: $\\ 70\\div2=35$ each', size=30)
t_8 = IH('t_8', 'start: $\\ $Noa $35+15=50$', size=30)
t_9 = IH('t_9', 'Eli $35-15=20$', size=30)
t_10 = IH('t_10', '$\\frac{50}{20}=\\frac{5}{2}$', size=32)
video('solve-wp22-g050', 'solution', qid='wp22-g050', slides=[
    S('Method 1 · The math way: two equations',
      L("Noa and Eli have seventy stickers altogether. Noa gives Eli fifteen stickers, and then they have the same number. "
        "What was Noa's original number of stickers divided by Eli's original number?", pt('stem', 'Noa and Eli have', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("They ask for Noa's original number divided by Eli's original number, so we need both original numbers. We'll solve "
        "it two ways, the math way with two equations, and then with an insight, starting from the end.",
        pt('stem: ask', "They ask for Noa's original")),
      L("Let's start with the math way. We call Noa's original number n, and Eli's e. Together they have seventy, so n "
        "plus e is seventy.", show(t_1, 'so n plus e is seventy')),
      L("Noa gives Eli fifteen. Now Noa has n minus fifteen, and Eli has e plus fifteen. And then they're equal. So n "
        "minus fifteen is equal to e plus fifteen.", show(t_2, 'So n minus fifteen is equal')),
      L("Let's move the terms. We take e from both sides, and add fifteen to both sides. n minus e is fifteen plus fifteen, "
        "thirty.", show(t_3, 'n minus e is fifteen plus fifteen')),
      L("Now we have two equations. If we add them, the plus e and the minus e cancel. n plus n is two n. And seventy plus "
        "thirty is a hundred. So two n is a hundred, and n is fifty.", show(t_4, 'So two n is a hundred'), show(t_4b, 'and n is fifty')),
      L("Noa had fifty, and together they had seventy. So Eli had seventy minus fifty, twenty.", show(t_5, 'So Eli had seventy minus')),
      L("Noa's number divided by Eli's is fifty over twenty. We divide the top and the bottom by ten, five over two. Choice "
        "number four is our answer.", show(t_6, 'is fifty over twenty'), show(t_6b, 'five over two'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Insight: start from the end',
      L("[pause] Now the insight. Here it's easier to start from the end. What do we know about the end? They're equal, and "
        "the total is still seventy, because the stickers only moved between them.", pt('stem', "They're equal, and the total")),
      L("So at the end, they have seventy divided by two, thirty-five each. That's the only way to split seventy equally.",
        show(t_7, 'seventy divided by two')),
      L("Now we go back in time. Noa gave fifteen, so before that she had fifteen more. Thirty-five plus fifteen is fifty. "
        "And Eli had fifteen fewer. Thirty-five minus fifteen is twenty.", show(t_8, 'Thirty-five plus fifteen'),
        show(t_9, 'Thirty-five minus fifteen')),
      L("Fifty over twenty is five over two again. So when the end of the story is simple, start there and go backwards. "
        "Choice number four is our answer, and I'll see you in the next question.", show(t_10, 'Fifty over twenty is five'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ r26-t22-exam-tools (lesson)
# English addition (real exam: one equation, two unknowns 2020_autumn_q1_01, 2021_spring_q2_06; "It cannot be
# determined" choices 2024_autumn_q1_14, 2025_autumn_q1_06). Taught here (no question video teaches it); the two other
# tools (letters in the choices, assume all the same) are taught in the next two questions.
j_1 = I('j_1', '$2a+3p=13$', size=34)
j_2 = IH('j_2', '$a=2,\\ p=3$', size=30)
j_2b = IH('j_2b', '$4+9=13$ ✓', size=30)
j_3 = IH('j_3', '$a=5,\\ p=1$: $\\ 10+3=13$', size=30)
j_4 = IH('j_4', '$4a+6p=2(2a+3p)$', size=30)
j_4b = IH('j_4b', '$=2\\cdot13=26$ ✓', size=30)
j_5 = IH('j_5', '$3a+2p$: $\\ 6+6=12$', size=30)
j_5b = IH('j_5b', 'or $\\ 15+2=17$: $\\ $cannot be determined', size=30)
j_6 = I('j_6', 'One equation, two unknowns: $\\ $only a multiple of it', size=30)
video('r26-t22-exam-tools', 'lesson', slides=[
    S('Three Exam Tools',
      L("Welcome back. Here are three more tools the exam loves. The first one we'll learn here, knowing when we can't find "
        "the answer. The other two we'll learn in the questions.")),
    S('One equation, two unknowns',
      L("Say a question gives us one equation with two unknowns. Two a plus three p is thirteen. Can we find a and p? No, "
        "because many pairs work.", show(j_1, 'Two a plus three p is thirteen')),
      L("For example, a is two and p is three. Two times two is four. Three times three is nine. And four plus nine is "
        "thirteen. Or a is five and p is one. Ten plus three is thirteen too. Both pairs fit.",
        show(j_2, 'a is two and p is three'), show(j_2b, 'And four plus nine'), show(j_3, 'Or a is five and p is one')),
      L("But what if they ask for four a plus six p? That's exactly double the equation. Every term is times two, so the "
        "total is times two too. Two times thirteen is twenty-six. That we can find.", show(j_4, "That's exactly double"), show(j_4b, 'Two times thirteen is')),
      L("And three a plus two p? That's not a multiple of the equation. With the first pair, it's six plus six, twelve. "
        "With the second pair, it's fifteen plus two, seventeen. Two different results, so it cannot be determined.",
        show(j_5, 'With the first pair'), show(j_5b, 'With the second pair')),
      L("So remember, with one equation and two unknowns, we can find only a multiple of that equation. Anything else "
        "cannot be determined, and the exam does offer that as a choice. Let's see the other two tools in the questions. "
        "I'll see you in the next video.", show(j_6, 'with one equation and two unknowns'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t22-04 (added: letters in the choices)
# English addition (real exam: 2019_spring_q1_15, 2022_winter_q1_19, 2020_winter_q1_16). REMINDER: plugging in numbers
# (topic 51, R15: not 0 or 1, different letters different numbers, test every choice, a tie -> new numbers). W17: every
# choice read in full first. Methods: plugging in numbers, building the expression (and why choice 1 is the trap).
oq_1 = IH('oq_1', '$x=2,\\ y=3$', size=30)
oq_2 = IH('oq_2', 'pen $2$, $\\ $notebook $2+3=5$', size=30)
oq_3 = IH('oq_3', 'pens $3\\cdot2=6$, $\\ $notebooks $3\\cdot5=15$', size=30)
oq_3b = IH('oq_3b', '$6+15=21$', size=30)
oq_4 = IH('oq_4', '(1) $2xy+3$: $\\ 2\\cdot2\\cdot3=12$', size=30, col=1)
oq_4b = IH('oq_4b', '$12+3=15$, no', size=30, col=1)
oq_5 = IH('oq_5', '(2) $y(2x+3)$: $\\ 4+3=7$', size=30, col=1)
oq_5b = IH('oq_5b', '$3\\cdot7=21$ ✓', size=30, col=1)
oq_6 = IH('oq_6', '(3) $y(x+3)$: $\\ 3\\cdot5=15$, no', size=30, col=1)
oq_7 = IH('oq_7', '(4) $2y(x+3)$: $\\ 6\\cdot5=30$, no', size=30, col=1)
oq_8 = IH('oq_8', 'pen $x$, $\\ $notebook $x+3$', size=30)
oq_9 = IH('oq_9', 'a pair: $\\ x+x+3=2x+3$', size=30)
oq_10 = IH('oq_10', '$y$ pairs: $\\ y(2x+3)$', size=30)
oq_11 = IH('oq_11', '$2xy+3$: $\\ $the $3$ only once, no', size=30, col=1)
video('solve-q-r26-t22-04', 'solution', qid='q-r26-t22-04', slides=[
    S('Method 1 · Plugging in numbers',
      L("A pen costs x credits. A notebook costs three credits more than a pen. How much do y pens and y notebooks cost "
        "altogether?", pt('stem', 'A pen costs x credits', 'hl', 6.0), voice='calm', pause=0.5),
      L("There are letters in the question and in the choices. That's a hint that we can plug in numbers. We'll solve it "
        "two ways, by plugging in numbers, and then the math way, building the expression.", pt('stem', 'There are letters')),
      L("Let's plug in numbers. We choose easy numbers, but not zero or one, because those often make different choices "
        "look the same. And a different number for each letter. So x is two, and y is three.", show(oq_1, 'So x is two')),
      L("A pen costs x, two credits. A notebook costs three credits more, two plus three, five credits.",
        show(oq_2, 'A notebook costs three credits more')),
      L("We buy y pens and y notebooks, so three of each. Three pens cost three times two, six. Three notebooks cost three "
        "times five, fifteen. And six plus fifteen is twenty-one.", show(oq_3, 'Three pens cost three times two'), show(oq_3b, 'And six plus fifteen')),
      L("So the right choice must give twenty-one when x is two and y is three. Choice number one says two x y plus three. "
        "Two times two times three is twelve. Plus three, that's fifteen. Not twenty-one, so it's out.",
        show(oq_4, 'Two times two times three'), show(oq_4b, "Plus three, that's fifteen"), mk('cross', 'choice 1', "Not twenty-one, so it's out")),
      L("Choice number two says y, times two x plus three. First we work out two x plus three. That's four plus three, seven. Then "
        "three times seven is twenty-one. It works, so we keep it.", show(oq_5, "That's four plus three"), show(oq_5b, 'Then three times seven')),
      L("Choice number three says y, times x plus three. x plus three is five, and three times five is fifteen. Out. "
        "Choice number four says two y, times x plus three. Two y is six, and six times five is thirty. Out.",
        show(oq_6, 'and three times five is fifteen'), mk('cross', 'choice 3', 'is fifteen. Out'), show(oq_7, 'and six times five is thirty'),
        mk('cross', 'choice 4', 'is thirty. Out')),
      L("Only choice number two gives twenty-one. If two choices had given twenty-one, we'd choose new numbers and test "
        "only those two. Choice number two is our answer.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · The math way: build it',
      L("[pause] Now the math way. We start again from the givens, and build the expression step by step. A pen costs x. "
        "A notebook costs three more, x plus three.", show(oq_8, 'A pen costs x')),
      L("One pen and one notebook together cost x plus x plus three, which is two x plus three.",
        show(oq_9, 'One pen and one notebook together')),
      L("We buy y pens and y notebooks. That's y pairs, with a pen and a notebook in each pair. So the cost is y, times two "
        "x plus three. That's choice number two.", show(oq_10, "That's y pairs"), mk('tick', 'choice 2', "That's choice number two")),
      L("Choice number one says two x y plus three. It's the trap, because it multiplies the two x by y, but adds the three "
        "only once. Every notebook costs three more, so the three is paid y times. Choice number two is our answer, and "
        "I'll see you in the next question.", show(oq_11, 'Choice number one says two x y'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t22-05 (added: assume all the same)
# English addition (real exam: 2021_spring_q2_08, 80 tickets at 30 or 20, total 1,800). Methods: the equation with one
# letter (the math way first, R13), then the insight "assume they're all the same kind" (NEW, full: why each swap adds 2,
# and the faster version with the kind they don't ask about).
w2_1 = IH('w2_1', 'motorcycles $m$, $\\ $cars $30-m$', size=30)
w2_2 = IH('w2_2', '$2m+4(30-m)=96$', size=30)
w2_3 = IH('w2_3', '$2m+120-4m=96$', size=30, col=1)
w2_4 = IH('w2_4', '$120-2m=96$', size=30, col=1)
w2_5a = IH('w2_5a', '$120-96=24$', size=30, col=1)
w2_5 = IH('w2_5', '$24=2m$, $\\ m=12$', size=30, col=1)
w2_6 = IH('w2_6', 'all motorcycles: $\\ 30\\cdot2=60$', size=30)
w2_7 = IH('w2_7', '$96-60=36$ missing', size=30)
w2_8 = IH('w2_8', 'a car instead: $\\ +2$ wheels', size=30)
w2_8b = IH('w2_8b', '$36\\div2=18$ cars', size=30)
w2_9 = IH('w2_9', '$30-18=12$', size=30)
w2_10 = IH('w2_10', 'all cars: $\\ 30\\cdot4=120$', size=30, col=1)
w2_10b = IH('w2_10b', '$120-96=24$ too many', size=30, col=1)
w2_11 = IH('w2_11', '$24\\div2=12$ motorcycles', size=30, col=1)
video('solve-q-r26-t22-05', 'solution', qid='q-r26-t22-05', slides=[
    S('Method 1 · The math way: an equation',
      L("A parking lot has thirty vehicles, cars and motorcycles. Each car has four wheels, and each motorcycle has two "
        "wheels. There are ninety-six wheels in total. How many motorcycles are in the parking lot?",
        pt('stem', 'A parking lot has thirty', 'hl', 9.0), voice='calm', pause=0.5),
      L("Two kinds of vehicles, a known number of vehicles, and a known number of wheels. They ask for the motorcycles. "
        "We'll solve it two ways, the math way with an equation, and then with an insight, pretending they're all the "
        "same kind.", pt('stem: ask', 'They ask for the motorcycles')),
      L("Let's start with the math way. They ask for the motorcycles, so let m be the motorcycles. There are thirty "
        "vehicles, so the cars are thirty minus m.", show(w2_1, 'so let m be the motorcycles')),
      L("Now the wheels. Each motorcycle has two wheels, so two m. Each car has four wheels, so four times thirty minus m. "
        "Together they have ninety-six wheels.", show(w2_2, 'Now the wheels')),
      L("We open the brackets. Four times thirty is a hundred twenty. Four times m is four m. So two m plus a hundred "
        "twenty minus four m is ninety-six. And two m minus four m is minus two m.", show(w2_3, 'We open the brackets'),
        show(w2_4, 'And two m minus four m')),
      L("So a hundred twenty minus two m is ninety-six. We add two m to both sides, and take ninety-six from both sides. A "
        "hundred twenty minus ninety-six is twenty-four. So twenty-four is two m, and m is twelve.",
        show(w2_5a, 'A hundred twenty minus ninety-six'), show(w2_5, 'So twenty-four is two m')),
      L("So there are twelve motorcycles. Choice number two is our answer.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Insight: assume all the same',
      L("[pause] Now the insight. We start again from the givens, and imagine that all thirty vehicles are motorcycles. "
        "Thirty times two is sixty wheels.", show(w2_6, 'Thirty times two is sixty')),
      L("But there are ninety-six wheels. Ninety-six minus sixty is thirty-six wheels missing.", show(w2_7, 'Ninety-six minus sixty')),
      L("Every time we swap a motorcycle for a car, we add two wheels, because a car has four and a motorcycle has two. "
        "Thirty-six divided by two is eighteen swaps. So eighteen of the vehicles are cars.",
        show(w2_8, 'Every time we swap'), show(w2_8b, 'Thirty-six divided by two')),
      L("Careful, eighteen is choice number one, but those are the cars, and they ask for the motorcycles. Thirty minus "
        "eighteen is twelve.", mk('cross', 'choice 1', 'but those are the cars'), show(w2_9, 'Thirty minus eighteen')),
      L("And a faster way. Assume they're all the kind they don't ask about, the cars. Thirty times four is a hundred "
        "twenty wheels. That's twenty-four too many. Each motorcycle has two wheels fewer than a car, so twenty-four "
        "divided by two is twelve motorcycles, straight away.", show(w2_10, 'Thirty times four is a hundred'), show(w2_10b, "That's twenty-four too many"),
        show(w2_11, 'so twenty-four divided by two')),
      L("So when there are two kinds, a known total count, and a known total of something else, pretend they're all one "
        "kind, and then fix the difference one swap at a time. Choice number two is our answer, and I'll see you in the "
        "next question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# carry-over boxes on the continuation slides (V2): the next step uses these results
CARRY22 = {
    'solve-wp22-g030': {1: ['$?=20\\cdot18\\div12$']},
    'solve-wp22-g035': {1: ['difference $=2x$, $\\ $even']},
    'solve-q-r26-t22-01': {1: ['altos: $\\ 12$ in both ratios']},
    'solve-q-r26-t22-20': {1: ['each book: $\\ $the gap changes by $2$']},
    'solve-wp22-g040': {1: ['$p\\le17\\frac{1}{2}$', '(3), (4) out']},
    'solve-wp22-g047': {1: ['$x=9$ (bus B)']},
    'solve-wp22-g048': {2: ['(3), (4) out']},
    'solve-wp22-g045': {1: ['cafe $5$, $\\ $supermarket $10$']},
    'solve-wp22-g042': {1: ['kiwis $2$, $\\ $limes $1$, $\\ $pineapples $\\frac{4}{3}$']},
    'solve-wp22-g043': {1: ['after level 1: $\\ 120$ players']},
    'solve-wp22-g049': {1: ['every part $\\times k$, so the total $\\times k$']},
}
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
 "wp22-g029": "Eight vases hold 56 roses. With the same number of roses in each vase, how many roses are in 12 vases?",
 "wp22-g030": "Working at a steady pace, a cook peels 18 potatoes in 12 minutes. How many potatoes does he peel in 20 minutes?",
 "q-r26-t22-02": "Six workers paint a hall in 10 days. All the workers work at the same rate. How many days would 4 workers need to paint the same hall?",
 "wp22-g032": "A café sells a sandwich for 47 credits. Making it uses 200 g of bread at 4 credits per 100 g, 300 g of cheese at 8 credits per 100 g, and 6 olives at half a credit each. Ignoring other costs, what is the selling price minus the ingredient cost?",
 "wp22-g033": "Bike shop A charges 4 credits for every hour or part of an hour. Bike shop B charges 17 credits for every 4-hour block or part of a block. What is the difference between the two charges for a 9.5-hour rental?",
 "wp22-g035": "At a sports camp, swimmers make up $\\frac{5}{12}$ of all the campers, and the rest are runners. Which could be the difference between the numbers of runners and swimmers?",
 "wp22-g036": "The prices of a sofa and a piano are in the ratio $3:10$. The piano costs 14,000 credits more than the sofa. What is their combined price?",
 "q-r26-t22-01": "In a choir, the ratio of sopranos to altos is $2:3$, and the ratio of altos to tenors is $4:5$. There are 30 tenors. How many singers are in the choir?",
 "q-r26-t22-03": "In a club, the ratio of boys to girls is $5:4$. Then 10 boys leave the club, and the ratio of boys to girls becomes $5:6$. How many members did the club have at first?",
 "wp22-g038": "A hall manager plans to set out the same number of chairs in each of 8 rows. One row must be removed to make room for a stage. Each of the 7 remaining rows must then hold 3 more chairs. How many chairs per row were originally planned?",
 "q-r26-t22-20": "Shelf A has 26 more books than shelf B. Some books are moved from shelf A to shelf B. After the move, shelf B has 6 more books than shelf A. How many books were moved?",
 "wp22-g039": "Maya is 9 years older than her cousin Tom. Five years ago, Maya was twice Tom’s age. How old is Tom now?",
 "wp22-g040": "Dana has 105 credits. That is enough for 6 identical movie tickets but not enough for 7. Which could be the price of one ticket?",
 "wp22-g042": "One credit buys 4 kiwis, 1.5 pineapples, or 5 limes, with costs proportional to quantity. What is the cost of 8 kiwis, 2 pineapples, and 5 limes? Fractional credits may be paid.",
 "wp22-g043": "A video game starts with 160 players. At the end of each level, $\\frac34$ of the players who began that level are still in the game. How many players are still in the game after two levels?",
 "wp22-g044": "At a training center, there are $\\frac58$ as many coaches as trainees. What fraction of all the people are coaches?",
 "wp22-g045": "A bakery sends twice as many loaves to supermarkets as to cafés. One half of the supermarket loaves and one fifth of the café loaves are whole-wheat. What fraction of all the loaves is whole-wheat?",
 "wp22-g046": "A baker has chocolate and vanilla cupcakes. She sells $\\frac13$ of the chocolate cupcakes and $\\frac16$ of the vanilla cupcakes, always selling whole cupcakes. The cupcakes left are 10 of one flavor and 14 of the other, in an unknown order. How many cupcakes did she have at first?",
 "wp22-g047": "A school has two buses. Bus A carries 4 times as many students as bus B. Six students move from bus A to bus B. Afterwards, bus B carries half as many students as bus A. How many students are on the two buses altogether?",
 "wp22-g048": "A plumber charges a fixed call-out fee plus the same amount for each hour of work. A 7-hour job costs 385 credits, and a 4-hour job costs 250 credits. What is the charge per hour?",
 "wp22-g049": "Nine large crates and six small crates weigh 240 kg altogether. All large crates weigh the same, and all small crates weigh the same. How much do twelve large and eight small crates weigh?",
 "wp22-g050": "Noa and Eli have 70 stickers altogether. Noa gives Eli 15 stickers, and then they have the same number. What was Noa’s original number of stickers divided by Eli’s original number?",
 "q-r26-t22-04": "A pen costs $x$ credits. A notebook costs 3 credits more than a pen. How much do $y$ pens and $y$ notebooks cost altogether?",
 "q-r26-t22-05": "A parking lot has 30 vehicles: cars and motorcycles. Each car has 4 wheels, and each motorcycle has 2 wheels. There are 96 wheels in total. How many motorcycles are in the parking lot?",
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

for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _stem_parts(_v); _write_gap(_v)



# 2026-10-13 carry-over boxes (V2) and the layer-order check (V1): after the visual passes, like topics 13-18
import types as _types
MV.carry(_types.SimpleNamespace(**globals()), CARRY22)
for _v in CARRY22:                                      # 2026-10-18 visual check: the So-far box at a readable size
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
