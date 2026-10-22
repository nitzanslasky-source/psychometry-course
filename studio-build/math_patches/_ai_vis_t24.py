"""Topic 24 (Overlapping groups) - the scripts for the teacher's own-voice reading (2026-10-20), written from the first
draft to the Codex review standard, the clarity style, W1-W21, the method vocabulary and the method visuals, built exactly
like topic 22 (math_patches/_ai_vis_t22.py: the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting as in topic 22, with the word stem's story as the "given" part).

The camera lesson 'wp-067' (Overlapping Groups) gets a full reading script with more examples, split into three parts of
about 3-4 minutes (math_patches/_camera_parts.py). Every other topic-24 video gets a script that SHE reads aloud in the
Reading Studio; reading_to_video.py then times the handwriting and the visuals to her words. The summary video
r26-t24-summary is not read: summary_pages/t24.json (python3 summary_pages.py 24) replaces it.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t24.py [vid ...] writes it);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t24.py ai_redo_t24() (runs LAST) rebuilds the slides from studio_slides(vid) and then
                    _ai_visual.apply() adds the cues and click items around them.

Spec DSL (as in topic 22): video / S / L / I / IH (a hand-written board line) / show / pt / mk; the topic-24 pictures of
her Hebrew course, built in layers at the spoken words: VENN2 (the two circles, wp 4339-4354: the circles, both first,
each "only", neither), STRIP (the squares method, wp 4570-4646: one long rectangle cut into 4 boxes, the two brackets
that share the middle box, filled "like a sudoku"), PIZZA (wp 4361-4387), UNITS (people as boxes, handing things out,
wp 4412-4428; the missing people of three groups side by side), TBL (the two-way table). The concept map (NEW / REMINDER
per video) is in ~/Downloads/Topic-24-AI-scripts-review.md.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(HERE) != 'math_patches':      # a test copy elsewhere still reads and writes the real studio files
    HERE = '/Users/nitzanslasky/psychometry-course/studio-build/math_patches'
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR

_s = importlib.util.spec_from_file_location('_shaded_nl_t24ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-24 flow order of the scripts
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
QBOT = {'solve-q-r26-t24-01': 181, 'solve-q-r26-t24-02': 286, 'solve-q-r26-t24-03': 242, 'solve-wp24-g070': 181, 'solve-wp24-g071': 242, 'solve-wp24-g072': 287, 'solve-wp24-g074': 242, 'solve-wp24-g075': 242, 'solve-wp24-g076': 264, 'solve-wp24-g077': 242, 'solve-wp24-g078': 242}   # measured on the frames (2026-10-20)


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
CAM_BASE = 'wp-067'
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
            'style': "the teacher reads it herself (Reading Studio), topic-24 scripts (2026-10-20): math_patches/_ai_vis_t24.py is "
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
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def OWN(d, name):
    """a ZL number line whose layers find their own base (written lines may come in between)"""
    for it in d.values():
        if it.get('over'): it['of'] = name
        else: it['fig'] = name
    return d


# ------------------------------------------------------------------------------------------- topic-24 figures (V1)
# The pictures of her Hebrew topic-24 lessons, built in layers at the spoken words (each layer a figure item drawn over
# its base; own=True: a layer finds its own base, so the written calculation lines can come in between):
#   VENN2  the two circles (wp 4339-4354: «סירות המפרש, העיגול הכחול, וסירות המנוע, העיגול הכתום... גם וגם... רק מפרש...
#          לא ולא»): the frame of everyone, the two circles with their names, then the regions one at a time, the
#          overlap ("both") first, each "only", then neither outside both circles; values written in their region.
#   STRIP  the squares method (wp 4568-4646: «המלבן הזה מייצג... ניצור ביניהם חפיפה... ריבוע נוסף מצד שמאל שזה הלא ולא...
#          כמו סודוקו»; «אני ישר מצייר מלבן ארוך וישר מחלק אותו ל-4 ריבועים»): one long rectangle cut into 4 boxes, left to
#          right  neither | B only | both | A only  (so "going left" reaches neither, as in her picture), the B bracket
#          over boxes 2-3, the A bracket under boxes 3-4 (the two brackets SHARE the middle box), all four = the total,
#          then the boxes filled like a sudoku.
#   PIZZA  the pizza (wp 4361-4387): six slices, the mushroom slices shaded, an O on every olive slice.
_BLUE, _BLUEF, _ORF, _GREYF = '#2f5d9a', '#dde6f3', '#fbe3cf', '#ececec'
_REG_FILL = {'both': MV.BAND, 'a': _BLUEF, 'b': '#d9efe9', 'out': '#f2f2f2'}


def _ml(x, y, t, size=22, col=None, anchor='middle'):
    """text with '\\n' = a second line (each line its own <text>)"""
    parts = t.split('\n'); out = ''
    for k, p in enumerate(parts):
        out += _tx(x, y + (k - (len(parts) - 1) / 2.0) * size * 1.08, p, size, col, anchor)
    return out


def VENN2(name, la, lb, layers, tot=None, col=0, w=None, title='Two groups'):
    """two overlapping circles inside a frame (everyone). layers = [(key, [mark, ...])]:
      ('tint', region)          shade a region: 'both' | 'a' (A only) | 'b' (B only) | 'out' (neither)
      ('ring', 'A' | 'B')       the WHOLE circle A (or B) traced thick in teal ("the whole music circle")
      ('val', region, text)     a big value in the region
      ('lab', region, text)     the region's name (small, under its value place)
      ('tot', text)             the frame's label (top left: everyone)"""
    W, H = 620, 330; cy, r = 190, 108; c1, c2 = 240, 380
    d = (c2 - c1) / 2.0; hh = (r * r - d * d) ** .5; xm = (c1 + c2) / 2.0
    top, bot = '%.1f %.1f' % (xm, cy - hh), '%.1f %.1f' % (xm, cy + hh)
    P = {'both': 'M %s A %d %d 0 0 1 %s A %d %d 0 0 1 %s Z' % (top, r, r, bot, r, r, top),
         'a': 'M %s A %d %d 0 1 0 %s A %d %d 0 0 1 %s Z' % (top, r, r, bot, r, r, top),
         'b': 'M %s A %d %d 0 1 1 %s A %d %d 0 0 0 %s Z' % (top, r, r, bot, r, r, top),
         'out': 'M 8 48 H 612 V 322 H 8 Z M %s A %d %d 0 1 0 %s A %d %d 0 1 0 %s Z' % (top, r, r, bot, r, r, top)}
    POS = {'both': (xm, cy + 8), 'a': (c1 - 52, cy + 8), 'b': (c2 + 52, cy + 8), 'out': (560, 300)}
    rings = ('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="2.8"/>' % (c1, cy, r, _BLUE) +
             '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="2.8"/>' % (c2, cy, r, _TEAL))
    nsz = 30 if max(len(la), len(lb)) < 11 else 24
    names = _tx(c1 - 50, 78, la, nsz, _BLUE) + _tx(c2 + 50, 78, lb, nsz, _TEAL)
    body = ('<rect x="8" y="48" width="604" height="274" rx="12" fill="none" stroke="%s" stroke-width="1.8"/>' % _INK + rings + names)
    out = [('line', MV._svg(W, H, body, '%s: %s and %s' % (title, la, lb)))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'tint':
                b += '<path d="%s" fill="%s" fill-rule="evenodd" stroke="none"/>' % (P[m[1]], _REG_FILL[m[1]]) + rings + names
            elif k == 'ring':
                cx = c1 if m[1] == 'A' else c2
                b += '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="7" stroke-opacity="0.85"/>' % (cx, cy, r, ORANGE)
            elif k == 'val':
                x, y = POS[m[1]]
                b += _tx(x, y + 6, m[2], 40 if len(m[2]) < 3 else (32 if len(m[2]) < 5 else 27), _INK)
            elif k == 'lab':
                x, y = POS[m[1]]
                b += _ml(x, (y - 6 if len(m) > 3 else y + 44) if m[1] != 'out' else y - 40, m[2], 23, _TEAL if m[1] == 'both' else _INK)
            elif k == 'tot':
                b += _tx(14, 36, m[1], 27, _INK, 'start')
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


_V3_FILL = {'three': MV.BAND, 'two': '#fbe3cf', 'one': _BLUEF}


def VENN3(name, names, layers, col=0, w=None, title='Three groups'):
    """three equal overlapping circles (2026-10-21, exact three-group counts; no frame: everyone is in a circle).
    names = the three circle names (top left, top right, bottom). Each region kind is its own exact shape (arcs sampled
    into a polygon), so the layers can be shown in any order. layers = [(key, [mark, ...])]:
      ('tint', kind)           shade every region of a kind: 'three' (the middle) | 'two' (the 3 pair regions, outside
                               the middle) | 'one' (the 3 outer parts)
      ('lab', kind, text)      the text ('\\n' = a second line) in every region of that kind
      ('val', kind, text)      a big value in the region (only for 'three': one region)
      ('tag', kind, text)      a small teal tag under the label in every region of that kind (x1, x2, x3)"""
    import math
    W, H, r, d = 470, 440, 124, 132; xm = W / 2.0
    C = [(xm - d / 2.0, 178), (xm + d / 2.0, 178), (xm, 178 + d * 3 ** .5 / 2)]
    G = (xm, sum(c[1] for c in C) / 3.0)
    ins = lambda p, i: (p[0] - C[i][0]) ** 2 + (p[1] - C[i][1]) ** 2 < r * r - 1e-6
    def cross(i, j):
        (x1, y1), (x2, y2) = C[i], C[j]
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); a = L / 2.0; h = (r * r - a * a) ** .5
        mx, my = x1 + dx / 2.0, y1 + dy / 2.0
        return [(mx - h * dy / L, my + h * dx / L), (mx + h * dy / L, my - h * dx / L)]
    def pts(i, j):                          # (inner = inside the third circle, outer)
        k = 3 - i - j; p, q = cross(i, j)
        return (p, q) if ins(p, k) else (q, p)
    def arc(i, p, q, want):                 # on circle i from p to q, the way whose middle has membership `want`
        cx, cy = C[i]; a1 = math.atan2(p[1] - cy, p[0] - cx); a2 = math.atan2(q[1] - cy, q[0] - cx)
        for s in (1, -1):
            span = (a2 - a1) * s % (2 * math.pi)
            am = a1 + s * span / 2.0; m = (cx + r * math.cos(am), cy + r * math.sin(am))
            if all(ins(m, k) == want[k] for k in range(3) if k != i):
                n = max(8, int(span * 40))
                return [(cx + r * math.cos(a1 + s * span * t / n), cy + r * math.sin(a1 + s * span * t / n)) for t in range(n + 1)]
        raise ValueError('arc')
    def poly(ps): return 'M ' + ' L '.join('%.1f %.1f' % p for p in ps) + ' Z'
    I = {(i, j): pts(i, j) for i, j in ((0, 1), (0, 2), (1, 2))}
    P = lambda i, j: I[tuple(sorted((i, j)))][0]
    O = lambda i, j: I[tuple(sorted((i, j)))][1]
    T3 = (True, True, True)
    reg = {'three': [poly(arc(0, P(0, 1), P(0, 2), T3) + arc(2, P(0, 2), P(1, 2), T3) + arc(1, P(1, 2), P(0, 1), T3))]}
    reg['two'] = []; reg['one'] = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        k = 3 - i - j; w2 = [True] * 3; w2[k] = False
        reg['two'].append(poly(arc(i, O(i, j), P(i, k), w2) + arc(k, P(i, k), P(j, k), T3) + arc(j, P(j, k), O(i, j), w2)))
    for i in range(3):
        j, k = [x for x in range(3) if x != i]; w1 = [False] * 3; w1[i] = True
        wj = [False] * 3; wj[i] = True                     # the inner edges: inside i only
        reg['one'].append(poly(arc(i, O(i, j), O(i, k), w1) + arc(k, O(i, k), P(j, k), wj) + arc(j, P(j, k), O(i, j), wj)))
    def mid(u, want):                       # the middle of the region with membership `want` along the ray G + t u
        ts = [t * .5 for t in range(1, 900) if [ins((G[0] + u[0] * t * .5, G[1] + u[1] * t * .5), k) for k in range(3)] == want]
        t = sum(ts) / len(ts); return (G[0] + u[0] * t, G[1] + u[1] * t)
    unit = lambda v: (v[0] / math.hypot(*v), v[1] / math.hypot(*v))
    POS = {'three': [G], 'two': [], 'one': []}
    for i, j in ((0, 1), (0, 2), (1, 2)):
        k = 3 - i - j; w2 = [True] * 3; w2[k] = False
        POS['two'].append(mid(unit((G[0] - C[k][0], G[1] - C[k][1])), w2))
    for i in range(3):
        w1 = [False] * 3; w1[i] = True
        POS['one'].append(mid(unit((C[i][0] - G[0], C[i][1] - G[1])), w1))
    cols = (_BLUE, _TEAL, ORANGE)
    rings = ''.join('<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s" stroke-width="2.8"/>' % (x, y, r, c)
                    for (x, y), c in zip(C, cols))
    nm = (_tx(C[0][0] - 92, 40, names[0], 28, cols[0]) + _tx(C[1][0] + 92, 40, names[1], 28, cols[1]) +
          _tx(C[2][0] + 118, C[2][1] + r - 4, names[2], 28, cols[2], 'start'))
    out = [('line', MV._svg(W, H, rings + nm, '%s: %s' % (title, ', '.join(names))))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'tint':
                b += ''.join('<path d="%s" fill="%s" stroke="none"/>' % (p, _V3_FILL[m[1]]) for p in reg[m[1]]) + rings + nm
            elif k == 'lab':
                b += ''.join(_ml(x, y + 2, m[2], 20 if m[1] != 'three' else 23, _INK) for x, y in POS[m[1]])
            elif k == 'val':
                x, y = POS[m[1]][0]
                b += _tx(x, y + 50, m[2], 34, _TEAL)
            elif k == 'tag':
                b += ''.join(_tx(x, y + 40, m[2], 21, _TEAL) for x, y in POS[m[1]])
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


def STRIP(name, lb, la, layers, col=0, w=None, title='The squares method'):
    """the squares method: boxes 0..3 = neither | lb only | both | la only (left to right).
      lb = the group whose bracket is drawn OVER boxes 1-2, la = the group whose bracket is UNDER boxes 2-3.
    layers = [(key, [mark, ...])]:
      ('B', text)               the bracket over boxes 1-2 (lb's group), with its value
      ('A', text)               the bracket under boxes 2-3 (la's group), with its value
      ('T', text)               the total: a long bracket under all four boxes
      ('top', i0, i1, text)     a second bracket above, over boxes i0..i1-1 (e.g. "not morning")
      ('v', i, text)            a value in box i
      ('q', i)                  a teal question mark in box i
      ('hl', i0, i1)            a thick teal frame around boxes i0..i1-1 (what we look at)"""
    W, H = 620, 330; x0, bw = 10, 150; yh, ybx, bh = 100, 146, 76
    X = lambda i: x0 + i * bw
    names = ['neither', lb + '\nonly', 'both', la + '\nonly']
    body = ''.join('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="2.4"/>'
                   % (X(i), yh, bw, ybx - yh, LIGHTH if i == 2 else '#ffffff', _INK) for i in range(4))
    body += ''.join('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="2.4"/>'
                    % (X(i), ybx, bw, bh, _INK) for i in range(4))
    body += ''.join(_ml(X(i) + bw / 2.0, (yh + ybx) / 2.0 + 7, t.replace('\nonly', ' only') if len(t) < 11 else t, 23 if len(t) < 11 else 21)
                    for i, t in enumerate(names))
    out = [('line', MV._svg(W, H, body, '%s: neither, %s only, both, %s only' % (title, lb, la)))]

    def br(i0, i1, y, up, lab, colr):
        xa, xb = X(i0) + 8, X(i1) - 8; dd = -12 if up else 12
        return ('<path d="M %d %d L %d %d L %d %d L %d %d" fill="none" stroke="%s" stroke-width="2.8"/>'
                % (xa, y - dd, xa, y, xb, y, xb, y - dd, colr) + _tx((xa + xb) / 2.0, y - 9 if up else y + 29, lab, 27, colr))
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'B': b += br(1, 3, yh - 18, True, m[1], _TEAL)
            elif k == 'A': b += br(2, 4, ybx + bh + 14, False, m[1], _BLUE)
            elif k == 'T': b += br(0, 4, ybx + bh + 66, False, m[1], _INK)
            elif k == 'top':
                b += br(m[1], m[2], yh - 58, True, m[3], ORANGE)
            elif k == 'v':
                b += _tx(X(m[1]) + bw / 2.0, ybx + bh * .68, m[2], 40 if len(m[2]) < 5 else 32, _TEAL)
            elif k == 'q':
                b += _tx(X(m[1]) + bw / 2.0, ybx + bh * .68, '?', 40, _TEAL)
            elif k == 'hl':
                b += ('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="none" stroke="%s" stroke-width="5"/>'
                      % (X(m[1]) + 3, yh + 3, (m[2] - m[1]) * bw - 6, ybx + bh - yh - 6, ORANGE))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


LIGHTH = MV.LIGHT
_MUSH = '#f1dcb8'


def PIZZA(name, layers, n=2, col=0, w=None, title='A pizza in six slices'):
    """n pizzas of 6 slices side by side. layers = [(key, [mark, ...])]:
      ('m', p, [slices])        shade these slices of pizza p (mushrooms)
      ('o', p, [slices])        an O (olives) on these slices
      ('x', p, [slices])        'none' on these slices (no topping)
      ('cap', p, text)          a caption under pizza p
      ('key',)                  the key: shaded = mushrooms, O = olives"""
    import math
    W = 330 * n; H = 360; r = 118
    C = [(165 + 330 * p, 150) for p in range(n)]
    def wedge(p, s, fill):
        cx, cy = C[p]; a0, a1 = math.radians(-90 + 60 * s), math.radians(-30 + 60 * s)
        return ('<path d="M %d %d L %.1f %.1f A %d %d 0 0 1 %.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2.4"/>'
                % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, cx + r * math.cos(a1), cy + r * math.sin(a1), fill, _INK))
    def mid(p, s, k):
        cx, cy = C[p]; a = math.radians(-60 + 60 * s)
        return cx + k * r * math.cos(a), cy + k * r * math.sin(a)
    body = ''.join(wedge(p, s, '#ffffff') for p in range(n) for s in range(6))
    out = [('line', MV._svg(W, H, body, title))]
    for key, marks in layers:
        b = ''
        for m in marks:
            if m[0] == 'm': b += ''.join(wedge(m[1], s, _MUSH) for s in m[2])
            elif m[0] == 'o':
                for s in m[2]:
                    x, y = mid(m[1], s, .62); b += _tx(x, y + 11, 'O', 32, _TEAL)
            elif m[0] == 'x':
                for s in m[2]:
                    x, y = mid(m[1], s, .6); b += _tx(x, y + 8, 'none', 23, RED)
            elif m[0] == 'cap':
                b += _tx(C[m[1]][0], 302, m[2], 25, _TEAL)
            elif m[0] == 'key':
                kx = W / 2.0 - (200 if n > 1 else 140)
                b += ('<rect x="%d" y="332" width="22" height="14" fill="%s" stroke="%s" stroke-width="1.5"/>' % (kx, _MUSH, _INK) +
                      _tx(kx + 30, 346, 'mushrooms', 21, _INK, 'start') + _tx(kx + 175, 348, 'O', 24, _TEAL, 'start') +
                      _tx(kx + 200, 346, 'olives', 21, _INK, 'start'))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


# =================================================================================================================
# THE SCRIPTS (topic-24 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-24-AI-scripts-review.md.
# Study plan before topic 24: 1, 30, 2, 4, 31, 6, 8, 32, 9, 10, 33, 51, 39, 42, 21, 3, 43, 22, 41, 5, 7, 44, 23, 11. So
# fractions (2, 3), equations (6), the method names and plugging in (51), ratios, x for one part and the ratio table (22),
# percents (23: plug in a hundred, "of" points at the whole, 10% then 5%, the complement, the flip rule) are REMINDERS;
# inequalities (12) and averages / weights (25) come LATER and are not used. New here (all of it): the two circles and
# the four regions, a whole group = its only part + both, range vs exact, the biggest overlap (the smaller group), the
# smallest overlap (the sum minus the total, or zero), counting each one once, the squares method, neither = 0 when the
# total counts only the lists, fractions (the whole is 1) and percents (the whole is 100%) in overlap questions, which
# overlap makes ANOTHER region small or big, "must an overlap exist?" (more than the whole), two-way tables, three
# groups (count who is missing, the smallest group, the smallest pair).
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ wp-067 (camera lesson)
# Hebrew (wp 4330-4392): overlap problems = groups with members in both; the marina (sail and motor boats) as two
# circles: both ("גם וגם"), sail only, motor only, neither ("לא ולא") - four sub-groups; two kinds on the exam: a range
# (min / max) and an exact overlap; the pizza (5 mushroom slices, tomatoes on 4: "no matter what we do, at least one
# slice has both", "a topping is a topping", at most 4); sometimes enough data to know exactly.
# English (camera lesson, 2-3 examples per idea): a class (music / sport) and a parking lot (red / electric) for the
# four regions; the whole circle = only + both (with numbers, a common mistake); the pizza for the range and the same
# pizza with one more fact for the exact kind; counting each one once (A + B - both + neither = total, why: the middle
# is counted twice) with two examples. Numbers and stories differ from the Hebrew. NEW (all).
a_t1 = I('a_t1', 'Students in a class: $\\ $music $\\cdot$ sport', size=30)
a_v1 = VENN2('a_v1', 'music', 'sport', [
    ('both', [('tint', 'both'), ('lab', 'both', 'both')]), ('a', [('lab', 'a', 'music\nonly')]),
    ('b', [('lab', 'b', 'sport\nonly')]), ('out', [('tint', 'out'), ('lab', 'out', 'neither')])], w=660)
a_r1 = I('a_r1', '$4$ regions: $\\ $music only $\\cdot$ both $\\cdot$ sport only $\\cdot$ neither', size=28)
a_r2 = I('a_r2', 'Every student is in exactly one region', size=28)
a_t2 = I('a_t2', 'Cars in a parking lot: $\\ $red $\\cdot$ electric', size=30)
a_v2 = VENN2('a_v2', 'red', 'electric', [
    ('both', [('tint', 'both'), ('lab', 'both', 'both')]), ('a', [('lab', 'a', 'red,\ngas')]),
    ('b', [('lab', 'b', 'white,\nelectric')]), ('out', [('tint', 'out'), ('lab', 'out', 'white,\ngas')])], w=660)
a_t3 = I('a_t3', '$10$ play music, $\\ 4$ of them also play a sport', size=30)
a_v3 = VENN2('a_v3', 'music', 'sport', [
    ('both', [('tint', 'both'), ('val', 'both', '4')]), ('a', [('val', 'a', '6')]), ('ring', [('ring', 'A')]),
    ('b', [('val', 'b', '3')])], w=560, col=0)
a_c1 = IH('a_c1', '$10-4=6$', size=30, col=1)
a_c2 = IH('a_c2', '$6+4=10$', size=30, col=1)
a_c2b = I('a_c2b', 'music $=$ the whole circle', size=28, col=1)
a_c3 = IH('a_c3', '$7-4=3$', size=30, col=1)
a_c3b = I('a_c3b', 'sport $=$ sport only $+$ both', size=28, col=1)
# part 2
a_k1 = I('a_k1', 'Kind 1 $\\cdot$ a range: $\\ $the smallest and the biggest overlap', size=30)
a_k2 = I('a_k2', 'Kind 2 $\\cdot$ exact: $\\ $every region is one number', size=30)
a_p1 = PIZZA('a_p1', [('m', [('m', 0, [0, 1, 2, 3]), ('m', 1, [0, 1, 2, 3]), ('key',)]),
                      ('o1', [('o', 0, [0, 1, 2])]), ('c1', [('cap', 0, 'both: 3, the most')]),
                      ('o2', [('o', 1, [4, 5])]), ('o3', [('o', 1, [0])]), ('c2', [('cap', 1, 'both: 1, the least')])], w=760)
a_p1t = I('a_p1t', '$6$ slices $\\cdot$ mushrooms on $4$ $\\cdot$ olives on $3$', size=30)
a_p1r = IH('a_p1r', 'both: from $1$ to $3$', size=32)
a_p2t = I('a_p2t', 'The same pizza $+$ exactly $1$ slice has no topping', size=30)
a_p2 = PIZZA('a_p2', [('m', [('m', 0, [0, 1, 2, 3]), ('key',)]), ('x', [('x', 0, [4])]), ('o1', [('o', 0, [5])]),
                      ('o2', [('o', 0, [0, 1])]), ('c', [('cap', 0, 'both: exactly 2')])], n=1, w=380)
a_p2a = IH('a_p2a', '$3-1=2$ on mushrooms', size=30, col=1)
# part 3
a_e1 = I('a_e1', '$30$ students: $\\ 12$ music, $\\ 15$ sport, $\\ 5$ both. $\\ $Neither?', size=30)
a_v4 = VENN2('a_v4', 'music', 'sport', [
    ('tot', [('tot', '30 students')]), ('both', [('tint', 'both'), ('val', 'both', '5')]), ('a', [('val', 'a', '7')]),
    ('b', [('val', 'b', '10')]), ('out', [('tint', 'out'), ('val', 'out', '8')])], w=560)
a_e2 = IH('a_e2', '$12-5=7$', size=30, col=1)
a_e3 = IH('a_e3', '$15-5=10$', size=30, col=1)
a_e4 = IH('a_e4', '$7+5+10=22$', size=30, col=1)
a_e5 = IH('a_e5', '$30-22=8$', size=30, col=1)
a_f1 = IH('a_f1', '$12+15=27$', size=30)
a_f2 = IH('a_f2', '$27-5=22$', size=30)
a_f3 = I('a_f3', '$A+B-$ both $+$ neither $=$ total', size=34)
a_f4 = IH('a_f4', '$12+15-5+$ neither $=30$', size=30)
a_f5 = IH('a_f5', '$22+$ neither $=30$, $\\ $neither $=8$', size=30)
a_g1 = I('a_g1', '$45$ members: $\\ 22$ swim, $\\ 18$ tennis, $\\ 10$ both', size=30)
a_g2 = IH('a_g2', '$22+18=40$', size=30)
a_g3 = IH('a_g3', '$40-10=30$', size=30)
a_g4 = IH('a_g4', 'neither: $\\ 45-30=15$', size=30)
a_s1 = I('a_s1', 'Two groups $\\to$ $4$ regions; $\\ $everyone is in exactly one', size=30)
a_s2 = I('a_s2', 'A whole group $=$ its only part $+$ both', size=30)
a_s3 = I('a_s3', 'A range, $\\ $or exact', size=30)
a_s4 = I('a_s4', '$A+B-$ both $+$ neither $=$ total', size=30)
video('wp-067', 'lesson', slides=[
    S('Overlapping Groups',
      L("Welcome back, and now a new topic, overlapping groups. These questions are about two groups of people, or of "
        "things. And some members belong to both groups."),
      L("Overlap questions show up in about half of the real exams. The good news is that they follow a few clear rules. "
        "With the right picture, they become quick questions.")),
    S('Two groups',
      L("Let's start with an example. In a class, some students play music, and some students play a sport. And some "
        "students do both.", show(a_t1, 'In a class, some students')),
      L("Let's draw it as two circles. One circle is the students who play music. The other circle is the students who "
        "play a sport.", show(a_v1['line'], "Let's draw it as two circles")),
      L("The circles cross each other. The part in the middle is inside both circles. So these students play music, and "
        "they also play a sport. We call this part both, or the overlap.", show(a_v1['both'], 'The part in the middle')),
      L("Now the part of the music circle that is outside the sport circle. These students play music, but no sport. We "
        "call it music only.", show(a_v1['a'], 'We call it music only')),
      L("In the same way, inside the sport circle but outside the music circle is sport only. These students play a "
        "sport, but no music.", show(a_v1['b'], 'inside the sport circle')),
      L("And there's one more group, the students outside both circles. They don't play music, and they don't play a "
        "sport. We call them neither.", show(a_v1['out'], 'the students outside both circles')),
      L("So two groups give us four regions. Music only, both, sport only, and neither. Every student is in exactly one "
        "of these four regions.", show(a_r1, 'So two groups give us four regions'), show(a_r2, 'Every student is in exactly one'))),
    S('Four regions again',
      L("Let's see the four regions once more, with something else. In a parking lot, some cars are red, and some cars "
        "are electric.", show(a_t2, 'In a parking lot'), show(a_v2['line'], 'some cars are electric')),
      L("A red electric car is in the middle, both. A red car that runs on gas is red only. A white electric car is "
        "electric only.", show(a_v2['both'], 'A red electric car'), show(a_v2['a'], 'A red car that runs on gas'),
        show(a_v2['b'], 'A white electric car')),
      L("And a white car that runs on gas? It's not red, and it's not electric. So it's neither, outside both circles.",
        show(a_v2['out'], "So it's neither")),
      L("Is there a car with no region? No. Every car is red or not, and electric or not. So every car is in exactly "
        "one region.")),
    S('The whole group',
      L("Now careful, because here's a mistake many students make. Let's put numbers in our class. Ten students play "
        "music. Four of them also play a sport.", show(a_t3, 'Ten students play music'), show(a_v3['line'], 'Four of them also play')),
      L("So where do the ten go? Not all ten go into music only. The four who also play a sport are in the middle, "
        "both.", show(a_v3['both'], 'are in the middle')),
      L("So music only is ten minus four, six.", show(a_c1, 'ten minus four'), show(a_v3['a'], 'six')),
      L("So the music students means the whole music circle. That's music only plus both. Six plus four is ten.",
        show(a_v3['ring'], 'the whole music circle'), show(a_c2b, "That's music only plus both"), show(a_c2, 'Six plus four is ten')),
      L("Let's look at the sport circle too. Say seven students play a sport. Four of them are in both. So sport only "
        "is seven minus four, three.", show(a_c3, 'seven minus four'), show(a_v3['b'], 'three')),
      L("So when a question says seven play a sport, it means the whole sport circle, sport only plus both. It doesn't "
        "mean sport only.", show(a_c3b, 'sport only plus both'))),
    S('Two kinds of questions',
      L("On the exam, overlap questions come in two kinds."),
      L("In the first kind, a fact is missing, so we can't know the exact size of the overlap. We can only find a range, "
        "the smallest it can be and the biggest it can be.", show(a_k1, 'We can only find a range')),
      L("In the second kind, we get every fact we need. Then we can find the exact number in each region.",
        show(a_k2, 'In the second kind')),
      L("Let's see both kinds on one simple example, a pizza.")),
    S('A pizza: a range',
      L("We order a pizza cut into six slices. We put mushrooms on four slices. Here they are, shaded.",
        show(a_p1t, 'We order a pizza'), show(a_p1['line'], 'cut into six slices'), show(a_p1['m'], 'Here they are, shaded')),
      L("Now we put olives on three slices. Where can the olives go? Let's try it in two different ways."),
      L("On the first pizza, we put all the olives on slices with mushrooms. All three olive slices have mushrooms. So "
        "three slices have both.", show(a_p1['o1'], 'All three olive slices')),
      L("Can more than three slices have both? No, because there are only three olive slices. So three is the most.",
        show(a_p1['c1'], 'So three is the most')),
      L("On the second pizza, someone doesn't like mushrooms. So first we put olives on the plain slices. There are two "
        "plain slices, so two olive slices are used.", show(a_p1['o2'], 'There are two plain slices')),
      L("One olive slice is left, and no plain slice is left. So it has to go on a slice with mushrooms. No matter what "
        "we do, at least one slice has both.", show(a_p1['o3'], 'So it has to go'), show(a_p1['c2'], 'at least one slice has both')),
      L("And we can't put olives on the same slice twice. A slice either has olives, or it doesn't."),
      L("So the number of slices with both is at least one, and at most three. That's a range, the first kind of "
        "question.", show(a_p1r, 'at least one, and at most three'))),
    S('A pizza: exact',
      L("Now the second kind. The same pizza, six slices, mushrooms on four and olives on three. But now there's one "
        "more fact. Exactly one slice has no topping at all.", show(a_p2t, 'The same pizza'),
        show(a_p2['line'], 'six slices'), show(a_p2['m'], 'mushrooms on four'), show(a_p2['x'], 'Exactly one slice has no topping')),
      L("Let's see what that fact does. Two slices have no mushrooms. One of them is the slice with no topping. So the "
        "other one must get olives.", show(a_p2['o1'], 'So the other one must get olives')),
      L("There are three olive slices, and one of them is on a plain slice. So the other two olive slices are on "
        "mushroom slices.", show(a_p2a, 'So the other two olive slices'), show(a_p2['o2'], 'are on mushroom slices')),
      L("So exactly two slices have both. It's not a range this time, it's one number. One more fact turned a range "
        "into an exact answer.", show(a_p2['c'], 'So exactly two slices have both'))),
    S('Count each one once',
      L("Now the four regions with numbers. A class has thirty students. Twelve play music, fifteen play a sport, and five "
        "do both. How many do neither?", show(a_e1, 'A class has thirty students'), show(a_v4['line'], 'Twelve play music'),
        show(a_v4['tot'], 'How many do neither')),
      L("Let's put it in the circles. Five do both, so five go in the middle.", show(a_v4['both'], 'so five go in the middle')),
      L("Music is twelve, the whole circle. So music only is twelve minus five, seven.", show(a_e2, 'twelve minus five'),
        show(a_v4['a'], 'seven')),
      L("Sport is fifteen. So sport only is fifteen minus five, ten.", show(a_e3, 'fifteen minus five'), show(a_v4['b'], 'ten')),
      L("Now everyone in at least one circle. Seven plus five plus ten is twenty-two.", show(a_e4, 'Seven plus five plus ten')),
      L("There are thirty students. So thirty minus twenty-two, eight do neither.", show(a_e5, 'thirty minus twenty-two'),
        show(a_v4['out'], 'eight do neither'))),
    S('The rule: count each one once',
      L("Now a faster way. A lot of students just add the two groups. Twelve plus fifteen is twenty-seven. But we "
        "counted only twenty-two students in the circles. Why the difference?", show(a_f1, 'Twelve plus fifteen is twenty-seven')),
      L("Because the five in the middle are inside the music circle, and also inside the sport circle. So when we add the "
        "two groups, we count them twice."),
      L("So we subtract them once. Twenty-seven minus five is twenty-two. That's everyone in at least one group.",
        show(a_f2, 'Twenty-seven minus five')),
      L("Then we add the ones outside, neither. So here's the rule. Group A plus group B, minus both, plus neither, is "
        "equal to the total.", show(a_f3, "So here's the rule")),
      L("In our class, twelve plus fifteen, minus five, plus neither, is equal to thirty. So twenty-two plus neither is "
        "thirty, and neither is eight. The same eight.", show(a_f4, 'In our class'), show(a_f5, 'So twenty-two plus neither'))),
    S('One more example',
      L("Let's use the rule once more. A club has forty-five members. Twenty-two swim, eighteen play tennis, and ten do "
        "both. How many do neither?", show(a_g1, 'A club has forty-five members')),
      L("Twenty-two plus eighteen is forty. The ten in both were counted twice, so forty minus ten, thirty are in at "
        "least one group. So forty-five minus thirty, fifteen do neither.", show(a_g2, 'Twenty-two plus eighteen'),
        show(a_g3, 'so forty minus ten'), show(a_g4, 'So forty-five minus thirty')),
      L("Why does the rule work? Because now every member is counted exactly once. That's the whole idea. Count each "
        "one once.")),
    S('Summary',
      L("Let's sum up this lesson. Two groups make four regions. A only, both, B only, and neither. Every member is in "
        "exactly one region.", show(a_s1, 'Two groups make four regions')),
      L("A whole group is its only part plus both. So ten music students means music only plus both.",
        show(a_s2, 'A whole group is its only part')),
      L("Some questions give only a range, and some give an exact answer.", show(a_s3, 'Some questions give only a range')),
      L("And to count everyone, we add the two groups, subtract both once, and add neither.", show(a_s4, 'And to count everyone')),
      L("Take a moment to memorize this. Next we'll learn the range questions, the smallest and the biggest overlap. "
        "I'll see you in the next video.")),
])
CAMERA_SPLIT = ('wp-067', 'Overlapping Groups', [
    (1, None),
    (4, "Let's continue with overlapping groups, and look at the two kinds of questions."),
    (7, "Let's continue, and see how the four regions add up to the total.")])


# ------------------------------------------------------------------------------------------------ wp-068 (lesson: ranges)
# Hebrew (wp 4394-4528): a fact is missing, so only a range: the biggest possible overlap and the smallest that must be
# (remember the pizza); 8 children, 5 hats, 4 horses handed out (horses to the children without a hat first -> at least
# 1; all horses to hat children -> at most 4); the technique: the biggest = the smaller group (why: no more horses), the
# smallest = the sum minus the total (why: 9 items for 8 children, one child must get two); equal groups; not over the
# total -> 0, "it's not minus 1"; the words (at most -> "more" = maximum, at least -> "less" = minimum, the greatest, the
# smallest, what could be, choices like "between 3 and 9"); recap; a kindergarten of 20 (15 hats, 12 glasses): 12 and 7,
# by the formula and by logic (5 without hats get glasses first). English: 15 students (art 10, drama 9) handed out as
# boxes, a second "biggest" example, the equal case, the zero case and the "not negative" trap with numbers, a full
# second example (24 players) by the formula and by logic, and the hidden total (24 hours a day; real exam
# 2020_winter_q1_14 type, the card's teacher-approved tip). NEW: all of it (the pizza is a reminder).
r_q1 = I('r_q1', 'the biggest overlap that is possible', size=30)
r_q2 = I('r_q2', 'the smallest overlap that must be', size=30)
r_ex = I('r_ex', '$15$ students: $\\ 10$ art, $\\ 9$ drama. $\\ $How many could take both?', size=30)
r_u = UNITS('r_u', [('fewest', 15), ('most', 15)], [
    ('a1', [('fill', 0, 0, 10)]), ('d1', [('in', 0, i, 'D') for i in range(10, 15)]),
    ('d2', [('in', 0, i, 'D') for i in range(4)]), ('b1', [('br', 0, 0, 4, 'both: 4')]),
    ('a2', [('fill', 1, 0, 10)]), ('d3', [('in', 1, i, 'D') for i in range(9)]), ('b2', [('br', 1, 0, 9, 'both: 9')])],
    unit=56, labw=150, gap=70, w=1000)
r_u1 = IH('r_u1', '$9-5=4$', size=30)
r_u2 = IH('r_u2', 'both: from $4$ to $9$', size=32)
r_m1 = I('r_m1', 'Biggest overlap $=$ the smaller group', size=32)
r_m2 = IH('r_m2', '$10$ and $9$: $\\ $biggest $9$', size=30)
r_m3 = IH('r_m3', 'dog $8$, cat $12$: $\\ $biggest $8$', size=30)
r_m4 = IH('r_m4', '$6$ and $6$: $\\ $biggest $6$', size=30)
r_n1 = I('r_n1', 'Smallest overlap $=A+B-$ total', size=32)
r_n2 = IH('r_n2', '$10+9=19$', size=30)
r_n3 = IH('r_n3', '$19-15=4$', size=30)
r_n4 = I('r_n4', '$19$ places, $\\ 15$ students: $\\ 4$ get two', size=30)
r_n5 = I('r_n5', '$30$ players: $\\ 18$ cap, $\\ 21$ gloves', size=28, col=1)
r_n6 = IH('r_n6', '$18+21=39$', size=30, col=1)
r_n7 = IH('r_n7', '$39-30=9$', size=30, col=1)
r_z1 = IH('r_z1', '$8+12=20$, $\\ $not over $20$', size=30)
r_z2 = IH('r_z2', 'smallest: $\\ 0$', size=30)
r_z3 = IH('r_z3', '$5+12=17$', size=30)
r_z4 = IH('r_z4', '$17<20$: $\\ $smallest $0$, $\\ $not $-3$', size=30)
r_z5 = I('r_z5', 'Not over the total? $\\ $Smallest overlap $=0$', size=32)
r_w1 = I('r_w1', 'at most $\\cdot$ the greatest: $\\ $the biggest possible', size=30)
r_w2 = I('r_w2', 'at least $\\cdot$ the smallest: $\\ $the smallest that must be', size=30)
r_w3 = I('r_w3', 'could be $\\cdot$ possible: $\\ $a range', size=30)
r_w4 = I('r_w4', 'choices like "between $3$ and $9$": $\\ $a range', size=30)
r_x1 = I('r_x1', '$24$ players: $\\ 18$ wear a cap, $\\ 14$ wear gloves. $\\ $How many could wear both?', size=30)
r_x2 = IH('r_x2', 'biggest: $\\ 14$', size=30)
r_x3 = IH('r_x3', '$18+14=32$', size=30)
r_x4 = IH('r_x4', '$32-24=8$', size=30)
r_x5 = IH('r_x5', '$24-18=6$ without a cap', size=30, col=1)
r_x6 = IH('r_x6', '$14-6=8$ gloves left', size=30, col=1)
r_x7 = IH('r_x7', 'both: from $8$ to $14$', size=32, col=1)
r_h1 = I('r_h1', 'One machine: $\\ 14$ hours a day. $\\ $Another: $\\ 16$ hours a day.', size=30)
r_h2 = IH('r_h2', 'total: $\\ 24$ hours', size=30)
r_h3 = IH('r_h3', '$14+16=30$', size=30)
r_h4 = IH('r_h4', '$30-24=6$', size=30)
r_h5 = IH('r_h5', 'both work: $\\ $from $6$ to $14$ hours', size=30)
# 2026-10-21 R37 (core methods back in the lesson): percents and fractions (the whole is 100% / 1; stay in percent),
# other regions ("at least / at most" is about the region they ask; which overlap makes it small or big) and neither
# ranges (the overlap of the two "not" groups). The lesson is split into 3 parts (WP068_SPLIT, at the end).
r_p0 = I('r_p0', 'In percent: $\\ $the whole $=100\\%$', size=30)
r_p1 = I('r_p1', '$200$ people: $\\ 60\\%$ bike, $\\ 55\\%$ car. $\\ $At least how many have both?', size=28)
r_p2 = IH('r_p2', '$60\\%+55\\%=115\\%$', size=30)
r_p3 = IH('r_p3', '$115\\%-100\\%=15\\%$', size=30)
r_p4 = IH('r_p4', '$15\\%$ of $200$: $\\ 20+10=30$', size=30, col=1)
r_p5 = IH('r_p5', 'both: $\\ $from $15\\%$ to $55\\%$', size=30, col=1)
r_f0 = I('r_f0', 'In fractions: $\\ $the whole $=1$', size=30)
r_f1 = I('r_f1', '$\\frac{7}{10}$ drink coffee, $\\ \\frac{1}{2}$ drink tea. $\\ $At least what part drink both?', size=30)
r_f2 = IH('r_f2', '$\\frac{7}{10}+\\frac{5}{10}=\\frac{12}{10}$', size=34)
r_f3 = IH('r_f3', '$\\frac{12}{10}-1=\\frac{2}{10}=\\frac{1}{5}$', size=34)
r_f4 = IH('r_f4', '$70\\%+50\\%=120\\%$: $\\ 20\\%$', size=30, col=1)
r_o1 = I('r_o1', '$15$ students: $\\ 10$ art, $\\ 9$ drama. $\\ $At least how many take art only?', size=28)
r_o2 = IH('r_o2', 'art only $=10-$ both', size=30)
r_o3 = IH('r_o3', 'small art only: $\\ $big both', size=30)
r_o4 = IH('r_o4', '$10-9=1$', size=30)
r_o5 = IH('r_o5', '$10-4=6$: $\\ $the most', size=30)
r_o6 = IH('r_o6', 'art only: $\\ $from $1$ to $6$', size=30)
r_o7 = I('r_o7', '$30$ players: $\\ 18$ cap, $\\ 21$ gloves', size=28, col=1)
r_o8 = IH('r_o8', 'gloves only $=21-$ both', size=30, col=1)
r_o9 = IH('r_o9', '$21-9=12$', size=30, col=1)
r_e1 = I('r_e1', '$15$ students: $\\ 10$ art, $\\ 9$ drama. $\\ $At most how many take neither?', size=28)
r_e2 = IH('r_e2', 'not art: $\\ 15-10=5$', size=30, col=1)
r_e3 = IH('r_e3', 'not drama: $\\ 15-9=6$', size=30, col=1)
r_ev = VENN2('r_ev', 'not art 5', 'not drama 6', [('both', [('tint', 'both'), ('lab', 'both', 'neither', 'mid')])], w=560)
r_e4 = IH('r_e4', 'biggest: $\\ 5$', size=30, col=1)
r_e5 = IH('r_e5', '$5+6=11$, $\\ $not over $15$: $\\ 0$', size=30, col=1)
r_e6 = IH('r_e6', 'neither: $\\ $from $0$ to $5$', size=30, col=1)
r_s1 = I('r_s1', 'Biggest overlap $=$ the smaller group', size=30)
r_s2 = I('r_s2', 'Smallest overlap $=A+B-$ total $\\ $(not over? $\\ 0$)', size=30)
r_s3 = I('r_s3', 'Percents: $\\ $the whole $=100\\%$. $\\ $Fractions: $\\ $the whole $=1$', size=30)
r_s4 = I('r_s4', 'Another region? $\\ $Which overlap makes it small or big?', size=30)
r_s5 = I('r_s5', 'Neither $=$ the overlap of the two "not" groups', size=30)
video('wp-068', 'lesson', slides=[
    S('Overlap Ranges',
      L("Welcome back, and now the first kind of overlap question, the range. Here a fact is missing, so we can't find "
        "the exact overlap.")),
    S('A fact is missing',
      L("Remember the pizza? We couldn't say exactly how many slices have both. We could only say the least, one, and the "
        "most, three."),
      L("So in a range question we look for two numbers. The biggest overlap that is possible. And the smallest overlap "
        "that must be, because there's no other choice.", show(r_q1, 'The biggest overlap that is possible'),
        show(r_q2, 'And the smallest overlap')),
      L("Let's see an example. There are fifteen students. Ten take art, and nine take drama. How many could take both?",
        show(r_ex, 'There are fifteen students')),
      L("We don't know how many take neither, and we don't know how many take both. That's the missing fact. So the "
        "answer is a range.")),
    S('Hand them out',
      L("Let's draw the fifteen students as fifteen boxes. The ten shaded boxes are the art students.",
        show(r_u['line'], "Let's draw the fifteen students"), show(r_u['a1'], 'The ten shaded boxes')),
      L("First the smallest overlap. We want as few students in both as we can. So we give drama to the students "
        "without art first."),
      L("Five students don't take art, so five drama places go to them.", show(r_u['d1'], 'so five drama places')),
      L("Nine minus five is four. So four drama places are left, and every student without art already takes "
        "drama.", show(r_u1, 'Nine minus five is four')),
      L("So the last four have to go to art students. There's no other choice. So at least four students take both.",
        show(r_u['d2'], 'So the last four'), show(r_u['b1'], 'at least four students take both')),
      L("Now the biggest overlap. This time we want as many students in both as we can. So we give all nine drama "
        "places to art students.", show(r_u['a2'], 'Now the biggest overlap'), show(r_u['d3'], 'So we give all nine')),
      L("Can it be more than nine? No, because only nine students take drama. So the overlap is somewhere from four to "
        "nine.", show(r_u['b2'], 'Can it be more than nine'), show(r_u2, 'somewhere from four to nine'))),
    S('The biggest overlap',
      L("Now let's find these two numbers without drawing. The biggest overlap is the size of the smaller group.",
        show(r_m1, 'The biggest overlap is the size')),
      L("Why? We put the whole small group inside the big group. So every drama student also takes art. And it can't be "
        "more, because the small group has no more members."),
      L("Ten and nine, so the biggest overlap is nine. There's nothing to calculate.", show(r_m2, 'Ten and nine')),
      L("Let's see it with other numbers. There are twenty students. Eight have a dog, and twelve have a cat. The biggest "
        "overlap is eight, the smaller group. All eight dog owners can also have a cat.", show(r_m3, 'Eight have a dog')),
      L("And if the groups are equal? Say six and six. Then the biggest overlap is six. The two groups can be the very "
        "same six people.", show(r_m4, 'Say six and six'))),
    S('The smallest overlap',
      L("The smallest overlap is the sum of the two groups, minus the total. In other words, how far do the two groups go "
        "over the total?", show(r_n1, 'The smallest overlap is the sum')),
      L("Ten plus nine is nineteen. But there are only fifteen students. Nineteen minus fifteen is four.",
        show(r_n2, 'Ten plus nine is nineteen'), show(r_n3, 'Nineteen minus fifteen')),
      L("Why does this work? Think of nineteen places in art and drama, for only fifteen students. Even if every student "
        "gets one place, four places are left over.", show(r_n4, 'Think of nineteen places')),
      L("Those four places have to go to students who already have one. So four students must take both. It's the same "
        "four we found with the boxes."),
      L("One more example. There are thirty players. Eighteen wear a cap, and twenty-one wear gloves. Eighteen plus twenty-one is "
        "thirty-nine. Thirty-nine minus thirty is nine. So at least nine wear both.", show(r_n5, 'There are thirty players'),
        show(r_n6, 'Eighteen plus twenty-one'), show(r_n7, 'Thirty-nine minus thirty'))),
    S('When nothing goes over',
      L("Now what if the two groups don't go over the total? Let's go back to the twenty students. Eight have a dog, and "
        "twelve have a cat."),
      L("Eight plus twelve is twenty, exactly the total. So we can give the dogs and the cats to different students. "
        "Nobody has to have both.", show(r_z1, 'Eight plus twelve is twenty')),
      L("So the smallest overlap is zero.", show(r_z2, 'So the smallest overlap is zero')),
      L("And if the sum is even smaller? Say only five have a dog. Five plus twelve is seventeen, less than twenty.",
        show(r_z3, 'Five plus twelve is seventeen')),
      L("A lot of students take seventeen minus twenty, and get minus three. But an overlap can't be negative. Nothing goes over "
        "the total, so the smallest overlap is zero.", show(r_z4, 'A lot of students take')),
      L("So we always ask, how far do the groups go over the total? If they don't go over it, the smallest overlap is "
        "zero.", show(r_z5, "If they don't go over it"))),
    S('How to spot a range question',
      L("How do we know it's a range question? By the words."),
      L("At most, the most, the greatest. These ask for the biggest possible value. At most has the word most, so think "
        "maximum.", show(r_w1, 'At most, the most, the greatest')),
      L("At least, the least, the smallest. These ask for the smallest value that must be. At least has the word least, "
        "so think minimum.", show(r_w2, 'At least, the least, the smallest')),
      L("What could be, or which of these is possible. The givens may allow several overlaps. We find their range, then "
        "choose the answer inside it.",
        show(r_w3, 'What could be')),
      L("And sometimes the choices give it away. A choice like between three and nine, or at least three and at most "
        "eight, is a range.", show(r_w4, 'A choice like between three and nine')),
      L("So far we asked about both. In the next part, we'll also ask about other regions, like neither.")),
    S('One more example',
      L("Let's do one more, from start to end. A team has twenty-four players. Eighteen wear a cap, and fourteen wear "
        "gloves. How many could wear both?", show(r_x1, 'A team has twenty-four players')),
      L("Could means a range. The biggest overlap is the smaller group, fourteen. All fourteen players with gloves can "
        "also wear a cap.", show(r_x2, 'The biggest overlap is the smaller group')),
      L("The smallest overlap is the sum minus the total. Eighteen plus fourteen is thirty-two. Thirty-two minus "
        "twenty-four is eight.", show(r_x3, 'Eighteen plus fourteen'), show(r_x4, 'Thirty-two minus')),
      L("We can also think it through. Twenty-four minus eighteen is six, so six players don't wear a cap. We give "
        "gloves to those six first.", show(r_x5, 'Twenty-four minus eighteen')),
      L("That leaves fourteen minus six, eight gloves. Those eight have to go to players with a cap.",
        show(r_x6, 'fourteen minus six')),
      L("Both ways give eight. So the number with both is from eight to fourteen.", show(r_x7, 'from eight to fourteen'))),
    S('When the total is hidden',
      L("Sometimes the total isn't written in the question. Then we look for a total we all know."),
      L("For example, one machine works fourteen hours a day, and another machine works sixteen hours a day. How many hours a day "
        "do both work at the same time?", show(r_h1, 'one machine works fourteen hours')),
      L("A day has twenty-four hours, so that's our total.", show(r_h2, 'A day has twenty-four hours')),
      L("Fourteen plus sixteen is thirty. Thirty minus twenty-four is six. So both work together at least six hours a "
        "day.", show(r_h3, 'Fourteen plus sixteen'), show(r_h4, 'Thirty minus twenty-four')),
      L("And at most fourteen hours, the smaller one. So it's from six to fourteen hours a day.",
        show(r_h5, 'from six to fourteen hours'))),
    S('Groups in percent',
      L("Many range questions give the groups in percent, not in people. Then the whole is a hundred percent. And the two "
        "rules work the same way.", show(r_p0, 'the whole is a hundred percent')),
      L("Let's see an example. A town has two hundred people. Sixty percent have a bike, and fifty-five percent have a "
        "car. At least how many people have both?", show(r_p1, 'A town has two hundred people')),
      L("A lot of students first turn every percent into people. We don't have to. The rules work on any whole, so we "
        "stay in percent."),
      L("The smallest overlap is the sum minus the whole. Sixty plus fifty-five is a hundred fifteen percent.",
        show(r_p2, 'Sixty plus fifty-five')),
      L("The whole is a hundred percent. So a hundred fifteen minus a hundred is fifteen percent. Careful, we take away a "
        "hundred percent, not the two hundred people.", show(r_p3, 'So a hundred fifteen minus a hundred')),
      L("Only now we turn it into people, because they ask how many people. Ten percent of two hundred is twenty, and five "
        "percent is ten. So fifteen percent is twenty plus ten, thirty people.", show(r_p4, 'Ten percent of two hundred')),
      L("And the biggest overlap is the smaller group, fifty-five percent. So both is from fifteen to fifty-five percent.",
        show(r_p5, 'So both is from fifteen'))),
    S('Groups in fractions',
      L("Fractions work the same way. When we get fractions of everyone, the whole is one.",
        show(r_f0, 'the whole is one')),
      L("For example, seven tenths of the workers drink coffee, and one half drink tea. At least what part drink both?",
        show(r_f1, 'seven tenths of the workers')),
      L("To add them, we need the same bottom. A half is five tenths. Seven tenths plus five tenths is twelve tenths.",
        show(r_f2, 'Seven tenths plus five tenths')),
      L("The whole is one, and one is ten tenths. So twelve tenths minus one is two tenths, and that's one fifth. At least "
        "a fifth of the workers drink both.", show(r_f3, 'So twelve tenths minus one')),
      L("Often it's faster in percent. Seven tenths is seventy percent, and a half is fifty percent. Seventy plus fifty is "
        "a hundred twenty, so twenty percent. That's the same fifth.", show(r_f4, 'Seventy plus fifty')),
      L("So when you see percents or fractions of everyone, the whole is a hundred percent, or one. And in an exact "
        "question too, all four boxes together make the whole.")),
    S('Other regions: only',
      L("So far, they asked about both. But a range question can ask about another region. Let's go back to our fifteen "
        "students, ten in art and nine in drama. At least how many take art only?", show(r_o1, 'Let\'s go back to our fifteen')),
      L("First we write that region with both in it. Art only is the art students who are not in both. So art only is "
        "ten minus both.", show(r_o2, 'So art only is ten minus both')),
      L("Now we ask, what makes art only small? The bigger both is, the less is left for art only. So we need the "
        "biggest overlap.", show(r_o3, 'So we need the biggest overlap')),
      L("The biggest overlap is the smaller group, nine. So art only is ten minus nine, one. At least one student takes "
        "only art.", show(r_o4, 'ten minus nine')),
      L("Here's the trap. At least makes us think of the smallest overlap, four. But ten minus four is six. That's the "
        "most art only can be, not the least.", show(r_o5, 'But ten minus four is six')),
      L("So art only is from one to six. At least or at most is always about the region they ask.",
        show(r_o6, 'So art only is from one to six')),
      L("Let's try it with the thirty players. Eighteen wear a cap, and twenty-one wear gloves. The smallest overlap was "
        "nine, and the biggest is eighteen. At most how many wear only gloves?", show(r_o7, 'Eighteen wear a cap')),
      L("Gloves only is twenty-one minus both. For the most gloves only, we need the smallest both, nine. Twenty-one minus "
        "nine is twelve. So at most twelve wear only gloves.", show(r_o8, 'Gloves only is twenty-one minus both'),
        show(r_o9, 'Twenty-one minus nine'))),
    S('Other regions: neither',
      L("Now the region that confuses students most, neither. Again the fifteen students, ten in art and nine in drama. "
        "At most how many take neither?", show(r_e1, 'Again the fifteen students')),
      L("Neither means not in art, and also not in drama. Not in art is fifteen minus ten, five. Not in drama is fifteen "
        "minus nine, six.", show(r_e2, 'Not in art is fifteen minus ten'), show(r_e3, 'Not in drama is fifteen')),
      L("So neither is the students who are in both of these new groups. It's the overlap of not art and not drama.",
        show(r_ev['line'], 'in both of these new groups'), show(r_ev['both'], "It's the overlap of not art")),
      L("Now we use the same two rules on them. The biggest overlap is the smaller group, five. So at most five take "
        "neither.", show(r_e4, 'The biggest overlap is the smaller group, five')),
      L("And the smallest? Five plus six is eleven. That's not over fifteen, so the smallest overlap is zero.",
        show(r_e5, 'Five plus six is eleven')),
      L("So neither is from zero to five. And look, the most neither comes when all nine drama students also take art. "
        "Then only ten students are in a group, and fifteen minus ten is five.", show(r_e6, 'So neither is from zero to five')),
      L("So a big overlap gives a big neither. Before you pick a rule, ask which overlap makes the region they ask about "
        "small or big.")),
    S('Summary',
      L("Let's sum up. The biggest overlap is the smaller group. We put the small group inside the big one.",
        show(r_s1, 'The biggest overlap is the smaller group')),
      L("The smallest overlap is the sum of the groups minus the total. If they don't go over the total, it's zero, never "
        "negative.", show(r_s2, 'The smallest overlap is the sum')),
      L("In percent the whole is a hundred percent, and in fractions it's one.", show(r_s3, 'In percent the whole')),
      L("For another region, we write it with both in it, and ask which overlap makes it small or big. And neither is the "
        "overlap of the two not groups.", show(r_s4, 'For another region'), show(r_s5, 'And neither is the overlap')),
      L("Take a moment to memorize these rules. Next come the exact questions, and the squares method. I'll see you in the "
        "next video.")),
])
WP068_SPLIT = ('wp-068', 'Overlap Ranges', [
    (1, None),
    (6, "Let's continue with ranges, and see how to spot a range question."),
    (11, "Let's continue with ranges, and ask about the other regions.")])

# ------------------------------------------------------------------------------------------------ wp-069 (lesson: exact)
# Hebrew (wp 4530-4604): the questions that give every fact: both, neither ("לא ולא"), only one group; the SAME example
# as the range lesson plus one fact ("exactly one child has no horse and no hat"): handed out -> exactly 2; then the
# squares method on it (two rectangles that overlap = the two circles, a fourth box on the left for neither, all four =
# the total; neither 1 + the horse rectangle 4 = 5, so hat only 3, both 2: "like a sudoku"). Her next three examples
# (snorkels, boats, the frustrated students) are our questions g070, g071, g072. English: the same 15 students plus
# "exactly 2 take neither", the common mistake (the brackets must share the middle box) at the step, a second start box,
# and "exactly one" (an English addition for the practice: A + B - 2 both, why: both sits inside each group). NEW.
e_ex = I('e_ex', '$15$ students: $\\ 10$ art, $\\ 9$ drama', size=30)
e_fa = I('e_fa', 'One more fact: $\\ $exactly $2$ take neither', size=30)
e_u = UNITS('e_u', [('', 15)], [
    ('a', [('fill', 0, 0, 10)]), ('n', [('fill', 0, 10, 12, 'grey'), ('br', 0, 10, 12, 'neither: 2')]),
    ('d1', [('in', 0, i, 'D') for i in range(12, 15)]), ('d2', [('in', 0, i, 'D') for i in range(6)]),
    ('b', [('br', 0, 0, 6, 'both: 6')])], unit=60, labw=20, gap=70, w=940)
e_u1 = IH('e_u1', '$5-2=3$', size=30)
e_u2 = IH('e_u2', '$9-3=6$', size=30)
e_s = STRIP('e_s', 'drama', 'art', [
    ('T', [('T', 'all four: 15')]), ('A', [('A', 'art: 10')]), ('B', [('B', 'drama: 9')])], w=580)
e_f = STRIP('e_f', 'drama', 'art', [
    ('base', [('T', 'all four: 15'), ('A', 'art: 10'), ('B', 'drama: 9')]),
    ('v0', [('v', 0, '2')]), ('h', [('top', 0, 3, 'neither + drama: 11')]), ('v3', [('v', 3, '4')]), ('v2', [('v', 2, '6')]), ('v1', [('v', 1, '3')])], w=580)
e_s1 = IH('e_s1', '$2+9=11$', size=30, col=1)
e_s2 = IH('e_s2', '$15-11=4$', size=30, col=1)
e_s3 = IH('e_s3', '$10-4=6$', size=30, col=1)
e_s4 = IH('e_s4', '$9-6=3$', size=30, col=1)
e_s5 = IH('e_s5', '$2+4+6+3=15$', size=30, col=1)
e_k = I('e_k', 'The two brackets share the middle box', size=28)
e_t = STRIP('e_t', 'drama', 'art', [
    ('base', [('T', 'all four: 15'), ('A', 'art: 10'), ('B', 'drama: 9'), ('v', 3, '4')]),
    ('v2', [('v', 2, '6')]), ('v1', [('v', 1, '3')]), ('v0', [('v', 0, '2')])], w=580)
e_t0 = I('e_t0', 'Given instead: $\\ 4$ take art only', size=30)
e_t1 = IH('e_t1', '$10-4=6$', size=30, col=1)
e_t2 = IH('e_t2', '$9-6=3$', size=30, col=1)
e_t3 = IH('e_t3', '$4+6+3=13$', size=30, col=1)
e_t4 = IH('e_t4', '$15-13=2$', size=30, col=1)
e_o = STRIP('e_o', 'drama', 'art', [
    ('base', [('A', 'art: 10'), ('B', 'drama: 9'), ('v', 0, '2'), ('v', 1, '3'), ('v', 2, '6'), ('v', 3, '4')]),
    ('h1', [('hl', 1, 2)]), ('h3', [('hl', 3, 4)])], w=580)
e_o1 = IH('e_o1', '$3+4=7$', size=30, col=1)
e_o2 = I('e_o2', 'exactly one $=A+B-2\\cdot$ both', size=30)
e_o3 = IH('e_o3', '$10+9=19$', size=30, col=1)
e_o4 = IH('e_o4', '$2\\cdot6=12$', size=30, col=1)
e_o5 = IH('e_o5', '$19-12=7$', size=30, col=1)
# 2026-10-21 R37: neither = 0 when everyone is in a group (moved back from g078: core, also in practice p01 / p08 and
# "quite a few questions" in her Hebrew, wp 5160-5170): tea or coffee (every guest drank one), different stamps, and a
# non-example (a class: neither unknown -> a range).
e_n0 = I('e_n0', '$30$ guests, $\\ $each drank tea, coffee or both. $\\ 18$ tea, $\\ 17$ coffee', size=28)
e_n = STRIP('e_n', 'coffee', 'tea', [
    ('T', [('T', 'all four: 30')]), ('A', [('A', 'tea: 18')]), ('B', [('B', 'coffee: 17')]), ('v0', [('v', 0, '0')]),
    ('h', [('top', 0, 2, 'not tea')]), ('v1', [('v', 1, '12')]), ('v2', [('v', 2, '5')])], w=580)
e_n1 = IH('e_n1', 'neither $=0$', size=30, col=1)
e_n2 = IH('e_n2', '$30-18=12$', size=30, col=1)
e_n3 = IH('e_n3', '$17-12=5$', size=30, col=1)
e_w1 = I('e_w1', 'Together: $\\ 20$ different stamps. $\\ $One has $12$, $\\ $one has $11$.', size=28)
e_w2 = IH('e_w2', '$12+11=23$', size=30)
e_w3 = IH('e_w3', '$23-20=3$', size=30)
e_w4 = I('e_w4', 'A class of $20$: $\\ 12$ chess, $\\ 11$ music', size=28)
e_w5 = IH('e_w5', 'neither not given: $\\ $BOTH ranges from $3$ to $11$', size=30)
e_w6 = I('e_w6', 'The total counts only members of at least one group: $\\ $neither $=0$', size=28)
e_z1 = I('e_z1', 'Four boxes: $\\ $neither $\\cdot$ B only $\\cdot$ both $\\cdot$ A only', size=30)
e_z2 = I('e_z2', 'The brackets share "both"; $\\ $all four $=$ the total', size=30)
e_z3 = I('e_z3', 'Put in what you know, $\\ $then fill it like a sudoku', size=30)
video('wp-069', 'lesson', slides=[
    S('Exact Overlap',
      L("Welcome back, and now the second kind of overlap question. Here the question gives us every fact we need. So we "
        "can find the exact number in each region.")),
    S('One more fact',
      L("Let's go back to our fifteen students. Ten take art, and nine take drama. In the last lesson, both could be "
        "anything from four to nine.", show(e_ex, 'Ten take art, and nine take drama')),
      L("Now we add one more fact. Exactly two students take neither art nor drama.", show(e_fa, 'Exactly two students take neither')),
      L("Let's hand out the places again. The ten shaded boxes are the art students, so five students don't take art.",
        show(e_u['line'], "Let's hand out the places again"), show(e_u['a'], 'The ten shaded boxes')),
      L("Exactly two of those five take neither. Let's mark them in grey.", show(e_u['n'], "Let's mark them in grey")),
      L("So the other three students without art must take drama. Five minus two is three, and nobody else is outside "
        "art.", show(e_u['d1'], 'So the other three'), show(e_u1, 'Five minus two is three')),
      L("Drama has nine students, and three of them are drama only. So nine minus three, six drama places are left. They "
        "go to art students.", show(e_u2, 'So nine minus three'), show(e_u['d2'], 'They go to art students')),
      L("So exactly six students take both. Not a range this time, one number. The fact about neither fixed it.",
        show(e_u['b'], 'So exactly six students take both'))),
    S('The squares method',
      L("With small numbers we can hand things out. With bigger numbers, there's a faster tool, the squares method."),
      L("We draw one long rectangle, and cut it into four boxes. Each box is one of the four regions. Neither, drama only, "
        "both, and art only.", show(e_s['line'], 'We draw one long rectangle')),
      L("It's the same as the two circles, just drawn in a line. Every student is in exactly one box. So all four boxes "
        "together are the total, fifteen.", show(e_s['T'], 'all four boxes')),
      L("The art bracket covers two boxes, both and art only. Together they're ten.", show(e_s['A'], 'The art bracket')),
      L("The drama bracket covers drama only and both. Together they're nine.", show(e_s['B'], 'The drama bracket')),
      L("Careful here, this is a common mistake. The two brackets must share the middle box, both. If they don't share a "
        "box, there's no overlap at all.", show(e_k, 'The two brackets must share'))),
    S('Fill it like a sudoku',
      L("Now we fill the boxes like a sudoku, starting from what we know. Neither is two.",
        show(e_f['line'], 'Now we fill the boxes'), show(e_f['base'], 'like a sudoku'), show(e_f['v0'], 'Neither is two')),
      L("Neither plus the whole drama bracket is two plus nine, eleven. That's every box except art only.",
        show(e_s1, 'two plus nine'), show(e_f['h'], "That's every box except")),
      L("The four boxes make fifteen. So art only is fifteen minus eleven, four.", show(e_s2, 'fifteen minus eleven'),
        show(e_f['v3'], 'four')),
      L("The art bracket is ten. Art only is four, so both is ten minus four, six.", show(e_s3, 'ten minus four'),
        show(e_f['v2'], 'six')),
      L("And drama only is nine minus six, three.", show(e_s4, 'nine minus six'), show(e_f['v1'], 'three')),
      L("Let's check. Two plus four plus six plus three is fifteen. It fits, and it's the same six as before.",
        show(e_s5, 'Two plus four plus six'))),
    S('Start from any box',
      L("We can start from any box the question gives us. Say the question gives art only instead. The same fifteen "
        "students, ten in art, nine in drama, and four take art only.", show(e_t0, 'Say the question gives art only'),
        show(e_t['line'], 'The same fifteen'), show(e_t['base'], 'four take art only')),
      L("The art bracket is ten, and art only is four. So both is ten minus four, six.", show(e_t1, 'ten minus four'),
        show(e_t['v2'], 'six')),
      L("The drama bracket is nine, so drama only is nine minus six, three.", show(e_t2, 'nine minus six'),
        show(e_t['v1'], 'three')),
      L("Then four plus six plus three is thirteen students in at least one group. So neither is fifteen minus thirteen, "
        "two.", show(e_t3, 'four plus six plus three'), show(e_t4, 'fifteen minus thirteen'), show(e_t['v0'], 'two.')),
      L("And we fill only the boxes we need. If they ask for both, we stop at both.")),
    S('When neither is zero',
      L("Sometimes neither isn't written as a number, but the words still tell us what it is. For example, each of thirty "
        "guests drank tea, coffee, or both. Eighteen drank tea, and seventeen drank coffee. How many drank both?",
        show(e_n0, 'each of thirty guests')),
      L("Every guest drank something. So nobody is outside both groups, and neither is zero.", show(e_n1, 'and neither is zero')),
      L("Now it's an exact question, so let's draw the boxes. All four together are thirty. Tea is eighteen, and coffee "
        "is seventeen. And the first box, neither, is zero.", show(e_n['line'], "so let's draw the boxes"),
        show(e_n['T'], 'All four together are thirty'), show(e_n['A'], 'Tea is eighteen'), show(e_n['B'], 'and coffee'),
        show(e_n['v0'], 'neither, is zero')),
      L("Neither plus coffee only is everyone outside tea. That's thirty minus eighteen, twelve. Neither is zero, so "
        "coffee only is twelve.", show(e_n['h'], 'everyone outside tea'), show(e_n2, 'thirty minus eighteen'),
        show(e_n['v1'], 'so coffee only is twelve')),
      L("The coffee bracket is seventeen. So both is seventeen minus twelve, five.", show(e_n3, 'seventeen minus twelve'),
        show(e_n['v2'], 'five.'))),
    S('Words that mean neither is zero',
      L("The same happens with different things. Two friends have twenty different stamps together. One has twelve, and "
        "the other has eleven.", show(e_w1, 'Two friends have twenty')),
      L("Twenty counts only the stamps they have, so no stamp is outside both groups. Neither is zero."),
      L("So we count each stamp once. Twelve plus eleven is twenty-three. But there are only twenty stamps, so twenty-three "
        "minus twenty, three stamps were counted twice. Both friends have those three.", show(e_w2, 'Twelve plus eleven'),
        show(e_w3, 'twenty-three minus twenty')),
      L("Now compare it with a class of twenty students. Twelve play chess, and eleven play music.",
        show(e_w4, 'a class of twenty students')),
      L("Here some students may play nothing, so neither isn't given. Then it's a range again. Both is from three, the "
        "sum minus the total, to eleven, the smaller group.", show(e_w5, 'so neither isn')),
      L("So check what the total counts, not just one word. If it counts only people or things in at least one group, "
        "neither is zero. That's the box to start from.", show(e_w6, 'If it counts only people or things'))),
    S('Exactly one',
      L("There's one more region a question can ask about, exactly one. Exactly one means one group, but not both. So art "
        "only, or drama only.", show(e_o['line'], 'There\'s one more region'), show(e_o['base'], 'exactly one'),
        show(e_o['h1'], 'So art only'), show(e_o['h3'], 'or drama only')),
      L("In our boxes, that's four plus three, seven.", show(e_o1, 'four plus three')),
      L("Without the boxes, add the two groups, then subtract both twice. Why twice? The six in both were counted in "
        "art and in drama. We don't want them in exactly one, so we remove both copies.", show(e_o2, 'then subtract both twice')),
      L("Ten plus nine is nineteen. Two times six is twelve. Nineteen minus twelve is seven. The same seven.",
        show(e_o3, 'Ten plus nine'), show(e_o4, 'Two times six'), show(e_o5, 'Nineteen minus twelve'))),
    S('Summary',
      L("Let's sum up. In an exact question, we draw the four boxes. Neither, B only, both, and A only.",
        show(e_z1, 'we draw the four boxes')),
      L("The two brackets share the middle box, and all four boxes make the total.", show(e_z2, 'The two brackets share')),
      L("And when everyone is in a group, neither is zero."),
      L("We put in what we know, and fill the rest like a sudoku. Now let's practice it on three questions. I'll see you "
        "in the next video.", show(e_z3, 'We put in what we know'))),
])


# ------------------------------------------------------------------------------------------------ wp24-g070 (Hebrew: the fish, snorkels and floats)
# Hebrew (wp 4606-4646): the squares method straight away (one long rectangle cut into 4); the common mistake - the
# second bracket must overlap the first; both 12 in the middle; snorkel only 15 - 12 = 3; "I'm trying to get to neither,
# that's why I go left"; floats bracket 21 + 3 = 24, 32 - 24 = 8; "we could find the 9, but we don't need it". English
# second method: count each one once (taught in the camera lesson). REMINDERS: the squares method (wp-069), the rule
# (wp-067). Trap at the step: 14 = pool only.
g70s = STRIP('g70s', 'gym', 'pool', [
    ('T', [('T', 'all four: 52')]), ('A', [('A', 'pool: 31')]), ('B', [('B', 'gym: 26')]),
    ('v2', [('v', 2, '17')]), ('v1', [('v', 1, '9')]), ('h', [('top', 1, 4, 'at least one: 40')]), ('v0', [('v', 0, '12')])], w=560)
g70a = IH('g70a', '$26-17=9$', size=30, col=1)
g70b = IH('g70b', '$31+9=40$', size=30, col=1)
g70c = IH('g70c', '$52-40=12$', size=30, col=1)
g70d = IH('g70d', 'pool only: $\\ 31-17=14$', size=30, col=1)
g70r = I('g70r', '$A+B-$ both $+$ neither $=$ total', size=30)
g70e = IH('g70e', '$31+26=57$', size=30, col=1)
g70f = IH('g70f', '$57-17=40$', size=30, col=1)
g70g = IH('g70g', '$40+$ neither $=52$', size=30, col=1)
g70h = IH('g70h', 'neither $=52-40=12$', size=30, col=1)
g70i = IH('g70i', '$57-52=5$: $\\ $the trap', size=30, col=1)
video('solve-wp24-g070', 'solution', qid='wp24-g070', slides=[
    S('Method 1 · The math way: the squares method',
      L("Of fifty-two hotel guests, thirty-one use the pool, twenty-six use the gym, and seventeen use both. How many use "
        "neither?", pt('stem', 'Of fifty-two hotel guests', 'hl', 6.0), voice='calm', pause=0.5),
      L("So they ask for neither, the guests who use no pool and no gym. We know the total, both groups, and both. Every "
        "fact is here, so it's an exact question. We'll solve it in two different ways, with the squares method, and then "
        "by counting each guest once.", pt('stem', 'So they ask for neither')),
      L("Let's start with the math way, the squares method. We draw four boxes. Neither, gym only, both, and pool only. "
        "All four boxes together are the fifty-two guests.", show(g70s['line'], 'We draw four boxes'),
        show(g70s['T'], 'All four boxes together')),
      L("The pool bracket covers both and pool only, thirty-one. The gym bracket covers gym only and both, twenty-six. "
        "The two brackets share the middle box, both.", show(g70s['A'], 'The pool bracket'), show(g70s['B'], 'The gym bracket')),
      L("The question says seventeen use both. So we write seventeen in the middle box.", pt('stem', 'The question says seventeen'),
        show(g70s['v2'], 'So we write seventeen')),
      L("The gym bracket is twenty-six, and seventeen of them are in both. So gym only is twenty-six minus seventeen, "
        "nine.", show(g70a, 'twenty-six minus seventeen'), show(g70s['v1'], 'nine.')),
      L("We want neither, so we move to the left. The pool bracket plus gym only is thirty-one plus nine, forty. These "
        "forty guests use at least one.", show(g70b, 'thirty-one plus nine'), show(g70s['h'], 'These forty guests')),
      L("The four boxes make fifty-two. So neither is fifty-two minus forty, twelve.", show(g70c, 'fifty-two minus forty'),
        show(g70s['v0'], 'twelve')),
      L("We could also find pool only, thirty-one minus seventeen, fourteen. But we don't need it. And careful, fourteen "
        "is choice number two. That's pool only, not neither.", show(g70d, 'thirty-one minus seventeen'),
        mk('cross', 'choice 2', "That's pool only, not neither")),
      L("So twelve guests use neither. Choice number three is our answer.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · The math way: count each once',
      L("[pause] Now the second way, with the rule from the first lesson. We start again from the givens. A plus B, minus "
        "both, plus neither, is equal to the total.", show(g70r, 'A plus B, minus both')),
      L("Thirty-one plus twenty-six is fifty-seven. That's more than the fifty-two guests, so some guests were counted "
        "twice. They're the seventeen in both.", show(g70e, 'Thirty-one plus twenty-six')),
      L("So we subtract them once. Fifty-seven minus seventeen is forty. That's every guest who uses at least one.",
        show(g70f, 'Fifty-seven minus seventeen')),
      L("Then forty plus neither is fifty-two. So neither is fifty-two minus forty, twelve again.",
        show(g70g, 'Then forty plus neither'), show(g70h, 'So neither is fifty-two minus forty')),
      L("If we forget to subtract both, we might take fifty-seven minus fifty-two, five. That's choice number one, the "
        "trap. Choice number three is our answer, and I'll see you in the next question.",
        show(g70i, 'fifty-seven minus fifty-two'), mk('cross', 'choice 1', "That's choice number one"),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp24-g071 (Hebrew: the marina, 15 boats)
# Hebrew (wp 4649-4674): the squares method: neither 2 + the sail bracket 8 = 10, so motor only 5 (to reach 15), both
# 10 - 5 = 5 ("a little sudoku", "you see? very simple"). English second method: count each one once (the 24 that do at
# least one job, 29 - 24 = 5 counted twice). Trap at the step: 2 = 29 - 27 forgets neither. REMINDERS.
g71s = STRIP('g71s', 'posters', 'color', [
    ('T', [('T', 'all four: 27')]), ('B', [('B', 'posters: 13')]), ('A', [('A', 'color: 16')]),
    ('v0', [('v', 0, '3')]), ('h', [('top', 0, 3, 'neither + posters: 16')]), ('v3', [('v', 3, '11')]), ('v2', [('v', 2, '5')])], w=560)
g71a = IH('g71a', '$3+13=16$', size=30, col=1)
g71b = IH('g71b', '$27-16=11$', size=30, col=1)
g71c = IH('g71c', '$16-11=5$', size=30, col=1)
g71d = IH('g71d', '$27-3=24$', size=30, col=1)
g71e = IH('g71e', '$16+13=29$', size=30, col=1)
g71f = IH('g71f', '$29-24=5$', size=30, col=1)
g71g = IH('g71g', '$29-27=2$: $\\ $forgets neither', size=30, col=1)
video('solve-wp24-g071', 'solution', qid='wp24-g071', slides=[
    S('Method 1 · The math way: the squares method',
      L("A print shop has twenty-seven printers. Of them, sixteen print in color, thirteen print large posters, and three "
        "do neither. How many printers both print in color and print large posters?",
        pt('stem', 'A print shop has twenty-seven', 'hl', 7.0), voice='calm', pause=0.5),
      L("So this time neither is given, three, and they ask for both. We have the total, both groups, and neither, so it's "
        "an exact question. We'll solve it in two different ways, with the squares method, and then by counting each "
        "printer once.", pt('stem', 'So this time neither is given')),
      L("Let's start with the math way, the squares method. We draw four boxes. Neither, posters only, both, and color only. All "
        "four together are the twenty-seven printers.", show(g71s['line'], 'Four boxes'), show(g71s['T'], 'All four together')),
      L("The poster bracket covers posters only and both, thirteen. The color bracket covers both and color only, "
        "sixteen.", show(g71s['B'], 'The poster bracket'), show(g71s['A'], 'The color bracket')),
      L("Three printers do neither, so we write three in the first box.", show(g71s['v0'], 'so we write three')),
      L("Neither plus the whole poster bracket is three plus thirteen, sixteen. That covers every box except color only.",
        show(g71a, 'three plus thirteen'), show(g71s['h'], 'That covers every box')),
      L("The four boxes make twenty-seven. So color only is twenty-seven minus sixteen, eleven.",
        show(g71b, 'twenty-seven minus sixteen'), show(g71s['v3'], 'eleven')),
      L("The color bracket is sixteen, and eleven of them are color only. So both is sixteen minus eleven, five.",
        show(g71c, 'sixteen minus eleven'), show(g71s['v2'], 'five.')),
      L("So five printers do both jobs. Choice number four is our answer.", mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · The math way: count each once',
      L("[pause] Now by counting each printer once. We start again from the givens. Three printers do neither. So "
        "twenty-seven minus three, twenty-four printers do at least one job.", show(g71d, 'twenty-seven minus three')),
      L("Now we add the two groups. Sixteen plus thirteen is twenty-nine. But only twenty-four printers do a job. "
        "Twenty-nine minus twenty-four is five.", show(g71e, 'Sixteen plus thirteen'), show(g71f, 'Twenty-nine minus twenty-four')),
      L("Those five extra were counted twice, once in color and once in posters. So five printers do both, the same "
        "five."),
      L("Careful with choice number two, two. Two is twenty-nine minus twenty-seven. That's what we get if we forget the "
        "three that do neither. Choice number four is our answer, and I'll see you in the next question.",
        show(g71g, 'Two is twenty-nine minus'), mk('cross', 'choice 2', 'if we forget the'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp24-g072 (Hebrew: the frustrated economics students)
# Hebrew (wp 4677-4706): "the wording confuses me completely, but bottom line: two groups"; the overlap is 1/5 of one
# and 1/3 of the other; "I could plug in 1, but let's call it x": 5x and 3x, the only parts 4x and 2x, twice; "a very,
# very hard question - when it was on the exam many students didn't know what to do; once it's in the squares it's
# simple". English: method 2 plugging in numbers (her "plug in 1", here 2: any number works), method 3 the flip rule
# (topic 23, a reminder) with the shared part taken out. Trap at the step: 9 : 4 = the whole clubs.
g72s = STRIP('g72s', 'robotics', 'chess', [
    ('v2', [('v', 2, 'x')]), ('A', [('A', 'chess: 9x')]), ('v3', [('v', 3, '8x')]), ('B', [('B', 'robotics: 4x')]),
    ('v1', [('v', 1, '3x')])], w=560)
g72t = STRIP('g72t', 'robotics', 'chess', [
    ('base', [('v', 2, 'x'), ('A', 'chess: 9x'), ('v', 3, '8x'), ('B', 'robotics: 4x'), ('v', 1, '3x')])], w=560)
g72a = IH('g72a', 'chess $=9x$', size=30, col=1)
g72b = IH('g72b', '$9x-x=8x$', size=30, col=1)
g72c = IH('g72c', 'robotics $=4x$', size=30, col=1)
g72d = IH('g72d', '$4x-x=3x$', size=30, col=1)
g72e = IH('g72e', '$8x:3x=8:3$', size=32, col=1)
g72p0 = IH('g72p0', 'both $=2$', size=30)
g72p1 = IH('g72p1', 'chess: $\\ 9\\cdot2=18$', size=30)
g72p2 = IH('g72p2', 'robotics: $\\ 4\\cdot2=8$', size=30)
g72p3 = IH('g72p3', '$18-2=16$, $\\ 8-2=6$', size=30, col=1)
g72p4 = IH('g72p4', '$16:6=8:3$', size=32, col=1)
g72f1 = IH('g72f1', 'chess : robotics $=9:4$', size=30)
g72f2 = IH('g72f2', '$\\frac{1}{9}\\cdot9=1$, $\\ \\frac{1}{4}\\cdot4=1$', size=30)
g72f3 = IH('g72f3', '$9-1=8$, $\\ 4-1=3$', size=30, col=1)
g72f4 = IH('g72f4', '$8:3$', size=32, col=1)
video('solve-wp24-g072', 'solution', qid='wp24-g072', slides=[
    S('Method 1 · The math way: the squares method',
      L("The students who are in both the chess club and the robotics club make up one ninth of the chess club and one "
        "quarter of the robotics club. What is the ratio of chess club students who are not in the robotics club to "
        "robotics club students who are not in the chess club?", pt('stem', 'The students who are in both', 'hl', 11.0),
        voice='calm', pause=0.5),
      L("The wording is long, so let's say it simply. They ask for chess only, compared with robotics only. And the same "
        "students, the ones in both, are a ninth of one club and a quarter of the other.", pt('stem', 'They ask for chess only')),
      L("Questions like this scare a lot of students, but in the boxes it's simple. We'll solve it in three different "
        "ways. The squares method, plugging in numbers, and the flip rule."),
      L("Let's start with the math way, the squares method. We draw four boxes. Neither, robotics only, both, and chess only. We "
        "don't know how many are in both, so let's call it x.", show(g72s['line'], 'Four boxes'), show(g72s['v2'], "let's call it x")),
      L("The question says x is a ninth of the chess club. So the whole chess club is nine times x, nine x.",
        pt('stem', 'The question says x is a ninth'), show(g72a, 'So the whole chess club'), show(g72s['A'], 'nine x.')),
      L("Chess only is the chess club without both. Nine x minus x is eight x.", show(g72b, 'Nine x minus x'),
        show(g72s['v3'], 'eight x')),
      L("x is also a quarter of the robotics club. So the robotics club is four x. Robotics only is four x minus x, three "
        "x.", show(g72c, 'So the robotics club is four x'), show(g72s['B'], 'four x.'), show(g72d, 'four x minus x'),
        show(g72s['v1'], 'three x'))),
    S('Method 1 · The math way: the squares method',
      L("So chess only to robotics only is eight x to three x. Both have x, so we divide both by x, and we get eight to "
        "three.", show(g72t['line'], 'So chess only'), show(g72t['base'], 'So chess only'), show(g72e, 'eight x to three x')),
      L("We never needed neither, because they didn't ask about it."),
      L("And careful with choice number three, nine to four. That's the whole chess club to the whole robotics club. They "
        "asked about the students in only one club. Choice number two is our answer.",
        mk('cross', 'choice 3', 'the whole chess club'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's plug in numbers. We start again from the givens. Both is a ninth of chess and a quarter of "
        "robotics. Any positive whole number works for both, because the ratio stays the same. Let's say two students are in both.",
        show(g72p0, 'two students are in both')),
      L("Two is a ninth of the chess club, so the chess club is nine times two, eighteen. Two is a quarter of the robotics "
        "club, so the robotics club is four times two, eight.", show(g72p1, 'nine times two'), show(g72p2, 'four times two')),
      L("Chess only is eighteen minus two, sixteen. Robotics only is eight minus two, six.", show(g72p3, 'eighteen minus two')),
      L("So it's sixteen to six. Both divide by two, so it's eight to three. Choice number two again.",
        show(g72p4, 'Both divide by two'))),
    S('Method 3 · Understanding: the flip rule',
      L("[pause] And now by understanding, with the flip rule from percents. We start again from the givens. The same "
        "students are a ninth of chess and a quarter of robotics."),
      L("Remember the flip rule. The overlap is the same number of students in both clubs. But it's a smaller fraction "
        "of the chess club, one ninth rather than one quarter. So the whole chess club must be bigger."),
      L("We flip the two fractions to get the ratio of the whole clubs. Chess to robotics is nine to four.",
        show(g72f1, 'Chess to robotics is nine to four')),
      L("Let's check with nine and four. A ninth of nine is one, and a quarter of four is one. The same one student is in "
        "both.", show(g72f2, 'A ninth of nine is one')),
      L("So chess has nine parts, robotics has four parts, and one part is in both. We take the shared part out of each "
        "club. Nine minus one is eight, and four minus one is three.", show(g72f3, 'Nine minus one is eight')),
      L("So it's eight to three. When the overlap is given as a fraction of each group, call the overlap x, or one part. Then "
        "write each group in those parts. Choice number two is our answer, and I'll see you in the next question.",
        show(g72f4, "So it's eight to three"), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp24-g078 (Hebrew: the owls, 24 and 18, 30 different)
# Hebrew (wp 5118-5170): understanding first: "they didn't say there are 30 owls, they said both photographed 30" ->
# neither is 0 ("not given, it's implied, you have to understand it from the wording"); 6 not Amir -> Zehava's, 18 - 6
# = 12; then the squares method from neither = 0; "there are quite a few questions where neither is 0, notice it with
# practice". R37 2026-10-21: APPLICATION of neither = 0 (taught in wp-069). Trap at the step: 11 = second only.
g78a = IH('g78a', 'neither $=0$', size=32, col=1)
g78b = IH('g78b', '$45-34=11$', size=30, col=1)
g78c = IH('g78c', '$27-11=16$', size=30, col=1)
g78s = STRIP('g78s', 'second', 'first', [
    ('T', [('T', 'all four: 45')]), ('A', [('A', 'first list: 34')]), ('B', [('B', 'second list: 27')]),
    ('v0', [('v', 0, '0')]), ('h', [('top', 0, 2, 'not on the first list')]), ('v1', [('v', 1, '11')]), ('v2', [('v', 2, '16')])], w=560)
g78d = IH('g78d', 'not on the first: $\\ 45-34=11$', size=30, col=1)
g78e = IH('g78e', '$27-11=16$', size=30, col=1)
g78f = IH('g78f', '$34+27=61$', size=30, col=1)
g78g = IH('g78g', '$61-45=16$', size=30, col=1)
video('solve-wp24-g078', 'solution', qid='wp24-g078', slides=[
    S('Method 1 · Understanding: neither is zero',
      L("Two friends list the movies they watched this year. One lists thirty-four movies and the other lists twenty-seven. "
        "Together, their lists show forty-five different movies. How many movies appear on both lists?",
        pt('stem', 'Two friends list the movies', 'hl', 9.0), voice='calm', pause=0.5),
      L("So they ask for both, the movies on both lists. The hard part here isn't the math. It's one fact that isn't "
        "written in the question. We'll solve it in two different ways, by understanding, and then with the squares "
        "method.", pt('stem', 'So they ask for both')),
      L("Let's start by understanding the forty-five, like the stamps in the lesson. They didn't say forty-five movies "
        "came out this year. They said the two lists show forty-five different movies.", pt('stem', 'They said the two lists show')),
      L("So every one of the forty-five movies is on at least one list. No movie is on neither list. So neither is zero.",
        show(g78a, 'So neither is zero')),
      L("It's not written, but it comes from the words. Here the total is only the movies on the lists."),
      L("The first friend lists thirty-four of the forty-five movies. So forty-five minus thirty-four, eleven movies are "
        "not on the first list.", show(g78b, 'forty-five minus thirty-four')),
      L("Those eleven movies are still on a list, so they're on the second list only."),
      L("The second list has twenty-seven movies, and eleven are only on the second list. So twenty-seven minus eleven, "
        "sixteen are on both lists.", show(g78c, 'twenty-seven minus eleven')),
      L("And careful, eleven is choice number two. That's the second list only, not both. Choice number one is our "
        "answer.", mk('cross', 'choice 2', "That's the second list only"), mk('tick', 'choice 1', 'Choice number one is our answer'))),
    S('Method 2 · The math way: the squares method',
      L("[pause] Now the math way, the squares method. We start again from the givens. We draw four boxes. Neither, second only, "
        "both, and first only. All four together are the forty-five different movies.", show(g78s['line'], 'Four boxes'),
        show(g78s['T'], 'All four together')),
      L("The first list covers both and first only, thirty-four. The second list covers second only and both, "
        "twenty-seven.", show(g78s['A'], 'The first list covers'), show(g78s['B'], 'The second list covers')),
      L("The forty-five counts only the movies on the lists, so no movie is on neither. The first box is zero.",
        show(g78s['v0'], 'The first box is zero')),
      L("Neither plus second only is everything outside the first list. That's forty-five minus thirty-four, eleven. And "
        "neither is zero, so second only is eleven.", show(g78s['h'], 'everything outside the first list'),
        show(g78d, 'forty-five minus thirty-four'), show(g78s['v1'], 'so second only is eleven')),
      L("The second list is twenty-seven. So both is twenty-seven minus eleven, sixteen.", show(g78e, 'twenty-seven minus eleven'),
        show(g78s['v2'], 'sixteen')),
      L("And with counting each movie once, thirty-four plus twenty-seven is sixty-one. Sixty-one minus forty-five is "
        "sixteen. Those sixteen movies were counted twice.", show(g78f, 'thirty-four plus twenty-seven'),
        show(g78g, 'Sixty-one minus forty-five')),
      L("Choice number one is our answer, and I'll see you in the next question.", mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp24-g077 (Hebrew: lunch, rice 1/3, mash 1/5, both 1/10 = 6)
# Hebrew (wp 5026-5115): the squares method in fractions (the whole is 1; not rice 2/3; mash only 1/5 - 1/10 = 1/10;
# neither 2/3 - 1/10 = 17/30; then 1/10 = 6 -> 17/30 by the triangle value = 34); then the insight: 1/10 = 6 so the total
# is 60, everything in numbers in the squares (rice 20, mash 12, not rice 40, mash only 6, neither 34): "this is the way
# I want you to work on the exam, not with the fractions". APPLICATION (R37): the whole is 1 (wp-068 part 2); NEW: the
# insight (find the total first). Traps at the step: 28 takes both away twice, 16 = at least one.
g77s = STRIP('g77s', 'evening', 'morning', [
    ('T', [('T', 'all four: 1')]), ('A', [('A', 'morning: 1/4')]), ('B', [('B', 'evening: 1/6')]),
    ('v2', [('v', 2, '1/12')]), ('v1', [('v', 1, '1/12')])], w=560)
g77s2 = STRIP('g77s2', 'evening', 'morning', [
    ('base', [('T', 'all four: 1'), ('A', 'morning: 1/4'), ('B', 'evening: 1/6'), ('v', 2, '1/12'), ('v', 1, '1/12')]),
    ('top', [('top', 0, 2, 'not morning')]), ('v0', [('v', 0, '8/12')])], w=560)
g77t = IH('g77t', 'the whole $=1$', size=30, col=1)
g77a = IH('g77a', '$\\frac{1}{6}=\\frac{2}{12}$', size=30, col=1)
g77b = IH('g77b', '$\\frac{2}{12}-\\frac{1}{12}=\\frac{1}{12}$', size=30, col=1)
g77c = IH('g77c', '$1-\\frac{1}{4}=\\frac{3}{4}=\\frac{9}{12}$', size=30, col=1)
g77d = IH('g77d', '$\\frac{9}{12}-\\frac{1}{12}=\\frac{8}{12}$', size=30, col=1)
g77e = IH('g77e', '$\\frac{1}{12}=4$ people', size=30, col=1)
g77f = IH('g77f', '$8\\cdot4=32$', size=32, col=1)
g77u = STRIP('g77u', 'evening', 'morning', [
    ('T', [('T', 'all four: 48')]), ('A', [('A', 'morning: 12')]), ('B', [('B', 'evening: 8')]), ('v2', [('v', 2, '4')]),
    ('v1', [('v', 1, '4')]), ('top', [('top', 0, 2, 'not morning: 36')]), ('v0', [('v', 0, '32')])], w=560)
g77g = IH('g77g', '$12\\cdot4=48$', size=30)
g77h = IH('g77h', '$48\\div4=12$, $\\ 48\\div6=8$', size=30, col=1)
g77i = IH('g77i', '$8-4=4$', size=30, col=1)
g77j = IH('g77j', '$48-12=36$', size=30, col=1)
g77k = IH('g77k', '$36-4=32$', size=32, col=1)
g77m = IH('g77m', '$12+8-4=16$: $\\ $at least one', size=28, col=1)
g77l = IH('g77l', '$48-12-8=28$: $\\ $both taken twice', size=28, col=1)
video('solve-wp24-g077', 'solution', qid='wp24-g077', slides=[
    S('Method 1 · The math way: the squares method',
      L("At a conference, one quarter of the participants attend the morning workshop, one sixth attend the evening "
        "workshop, and one twelfth attend both. Exactly four participants attend both. How many participants attend "
        "neither workshop?", pt('stem', 'At a conference', 'hl', 10.0), voice='calm', pause=0.5),
      L("So they ask for neither. We get fractions, and one real number of people, four. Every fact is here, so it's an "
        "exact question. We'll solve it in two different ways. The squares method in fractions, and then by finding the "
        "number of participants first.", pt('stem', 'So they ask for neither')),
      L("Let's start with the math way, the squares method, with fractions. Like in the lesson, the givens are fractions "
        "of the participants, so all the participants together are one whole.", show(g77t, 'all the participants together')),
      L("We draw four boxes. Neither, evening only, both, and morning only. All four together are one. The morning bracket is a "
        "quarter, and the evening bracket is a sixth.", show(g77s['line'], 'Four boxes'), show(g77s['T'], 'All four together are one'),
        show(g77s['A'], 'The morning bracket'), show(g77s['B'], 'the evening bracket')),
      L("Both is a twelfth, so we write a twelfth in the middle box.", show(g77s['v2'], 'so we write a twelfth')),
      L("Evening only is a sixth minus a twelfth. A sixth is two twelfths. Two twelfths minus one twelfth is one twelfth.",
        show(g77a, 'A sixth is two twelfths'), show(g77b, 'Two twelfths minus one twelfth'), show(g77s['v1'], 'is one twelfth'))),
    S('Method 1 · The math way: the squares method',
      L("Now let's find neither. Not in the morning is one minus a quarter, three quarters. That's neither plus evening only, the "
        "boxes outside the morning bracket.", show(g77s2['line'], "Now let's find neither"), show(g77s2['base'], "Now let's find neither"),
        show(g77s2['top'], 'Not in the morning is one minus'),
        show(g77c, 'three quarters')),
      L("Three quarters is nine twelfths. Take away evening only, one twelfth, and we get eight twelfths. So neither is "
        "eight twelfths.", show(g77d, 'Take away evening only'), show(g77s2['v0'], 'So neither is eight twelfths')),
      L("But the choices are numbers of people. The question says the twelfth in both is four people. So each twelfth is "
        "four people, and we have eight twelfths. Eight times four is thirty-two people.", pt('stem', 'The question says the twelfth'), show(g77e, 'is four people'),
        show(g77f, 'Eight times four')),
      L("Choice number two is our answer.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Insight: the total first',
      L("[pause] Now an insight, so we don't work with fractions at all. We start again from the givens. A twelfth of the "
        "participants is four people. So all the participants are twelve times four, forty-eight.",
        show(g77g, 'twelve times four')),
      L("Now let's write everything in people. The morning is a quarter of forty-eight, twelve. The evening is a sixth of "
        "forty-eight, eight. And four are in both.", show(g77h, 'a quarter of forty-eight'),
        show(g77u['line'], "Now let's write everything"), show(g77u['T'], "Now let's write everything"),
        show(g77u['A'], 'twelve.'), show(g77u['B'], 'eight.'), show(g77u['v2'], 'And four are in both')),
      L("Evening only is eight minus four, four.", show(g77i, 'eight minus four'), show(g77u['v1'], 'four.')),
      L("Not in the morning is forty-eight minus twelve, thirty-six. That's neither plus evening only.",
        show(g77j, 'forty-eight minus twelve'), show(g77u['top'], "That's neither plus evening only")),
      L("So neither is thirty-six minus four, thirty-two. The same thirty-two.", show(g77k, 'thirty-six minus four'),
        show(g77u['v0'], 'thirty-two.'))),
    S('Method 2 · Insight: the total first',
      L("Careful with choice number four, twenty-eight. That's forty-eight minus twelve minus eight. It takes the four in "
        "both away twice.", show(g77l, 'forty-eight minus twelve minus eight'), mk('cross', 'choice 4', 'It takes the four')),
      L("And choice number one, sixteen, is everyone in at least one workshop. Twelve plus eight minus four is sixteen. "
        "But they asked for neither.", show(g77m, 'Twelve plus eight minus four'), mk('cross', 'choice 1', 'But they asked for neither')),
      L("So when fractions come with one real number of people, find the total first, and work in people. Choice number "
        "two is our answer, and I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
])


# ------------------------------------------------------------------------------------------------ wp24-g074 (Hebrew: the wedding, 160 guests, 25% and 85%)
# Hebrew (wp 4711-4834): way 1 with numbers (a quarter of 160 = 40; 85% through the complement 15% = 16 + 8 = 24, so
# 136; "write the data in order"; the biggest overlap 40 as a free reminder; the smallest = how far the sum goes over
# the whole, 176 - 160 = 16); way 2 in percent ("in the exam I wouldn't calculate the numbers... step back": 25 + 85 =
# 110, 10% of 160 = 16); way 3 by understanding with the two circles (10% both, 15% bride only, 75% groom only; review:
# 15% both -> 5% neither; the biggest, 25%: bride only 0, neither 15%). APPLICATION (R37): percents, the whole is 100% (wp-068 part 2; the whole
# is 100%). REMINDERS: 10% and 5% of a number, the complement (topic 23), the two range rules (wp-068).
g74a = IH('g74a', '$10\\%=36$', size=30, col=1)
g74b = IH('g74b', '$40\\%=4\\cdot36=144$', size=30, col=1)
g74c = IH('g74c', '$5\\%=18$', size=30, col=1)
g74d = IH('g74d', '$144+18=162$', size=30, col=1)
g74e = IH('g74e', '$30\\%=3\\cdot36=108$', size=30, col=1)
g74f = IH('g74f', '$360-108=252$', size=30, col=1)
g74g = I('g74g', 'total $360$ $\\cdot$ artist $162$ $\\cdot$ owner $252$', size=30)
g74h = IH('g74h', 'biggest: $\\ 162$', size=30)
g74i = IH('g74i', '$162+252=414$', size=30, col=1)
g74j = IH('g74j', '$414-360=54$', size=30, col=1)
g74k = IH('g74k', '$45\\%+70\\%=115\\%$', size=30, col=1)
g74l = IH('g74l', '$115\\%-100\\%=15\\%$', size=30, col=1)
g74m = IH('g74m', '$15\\%$: $\\ 36+18=54$', size=30, col=1)
g74v = VENN2('g74v', 'artist 45%', 'owner 70%', [
    ('both', [('tint', 'both'), ('val', 'both', '15%')]), ('a', [('val', 'a', '30%')]), ('b', [('val', 'b', '55%')]),
    ('out', [('val', 'out', '0')])], w=560)
g74n = IH('g74n', '$45-15=30$, $\\ 70-15=55$', size=30, col=1)
g74o = IH('g74o', '$30+15+55=100$', size=30, col=1)
g74v20 = VENN2('g74v20', 'artist 45%', 'owner 70%', [
    ('both', [('tint', 'both'), ('val', 'both', '20%')]), ('a', [('val', 'a', '25%')]),
    ('b', [('val', 'b', '50%')]), ('out', [('val', 'out', '5%')])], w=560)
g74v45 = VENN2('g74v45', 'artist 45%', 'owner 70%', [
    ('both', [('tint', 'both'), ('val', 'both', '45%')]), ('a', [('val', 'a', '0')]),
    ('b', [('val', 'b', '25%')]), ('out', [('val', 'out', '30%')])], w=560)
g74p = IH('g74p', 'artist only: $45-20=25\\%$', size=30, col=1)
g74p2 = IH('g74p2', 'owner only: $70-20=50\\%$', size=30, col=1)
g74p3 = IH('g74p3', '$25+20+50=95\\%$', size=30, col=1)
g74p4 = IH('g74p4', 'neither: $100-95=5\\%$', size=30, col=1)
g74q = IH('g74q', 'artist only: $0$', size=30, col=1)
g74q2 = IH('g74q2', 'owner only: $70-45=25\\%$', size=30, col=1)
g74q3 = IH('g74q3', 'neither: $100-70=30\\%$', size=30, col=1)
g74r = IH('g74r', 'both: $\\ $from $15\\%$ to $45\\%$', size=30, col=1)
video('solve-wp24-g074', 'solution', qid='wp24-g074', slides=[
    S('Method 1 · The math way',
      L("At a gallery opening with three hundred sixty guests, forty-five percent know the artist and seventy percent "
        "know the gallery owner. What is the minimum number of guests who know both?",
        pt('stem', 'At a gallery opening', 'hl', 8.0), voice='calm', pause=0.5),
      L("They ask for the minimum, so this is a range question. We know the total and the two groups, but not neither. "
        "We'll solve it in three different ways. With the numbers, then in percent, and then with the two circles.",
        pt('stem', 'They ask for the minimum')),
      L("Let's start with the math way. First we turn the percents into numbers of guests. Ten percent of three hundred "
        "sixty is thirty-six. So forty percent is four times thirty-six, a hundred forty-four.",
        show(g74a, 'Ten percent of three hundred'), show(g74b, 'So forty percent')),
      L("Five percent is half of thirty-six, eighteen. Together, a hundred forty-four plus eighteen, a hundred sixty-two "
        "guests know the artist.", show(g74c, 'Five percent is half'), show(g74d, 'a hundred forty-four plus eighteen'))),
    S('Method 1 · The math way',
      L("For seventy percent, it's easier to use the rest, thirty percent. Thirty percent is three times thirty-six, a "
        "hundred eight. So seventy percent is three hundred sixty minus a hundred eight, two hundred fifty-two.",
        show(g74e, 'Thirty percent is three times'), show(g74f, 'three hundred sixty minus')),
      L("Let's write the data in order. There are three hundred sixty guests. A hundred sixty-two know the artist, and two hundred "
        "fifty-two know the owner.", show(g74g, 'Let\'s write the data in order')),
      L("Remember, the biggest overlap is the smaller group, a hundred sixty-two. They don't ask for it, but we get it "
        "for free. And careful, a hundred sixty-two is choice number two. It's the most, not the least.",
        show(g74h, 'the biggest overlap is the smaller group'), mk('cross', 'choice 2', "It's the most, not the least")),
      L("The smallest overlap is the sum minus the total. A hundred sixty-two plus two hundred fifty-two is four hundred "
        "fourteen. Four hundred fourteen minus three hundred sixty is fifty-four.",
        show(g74i, 'A hundred sixty-two plus'), show(g74j, 'Four hundred fourteen minus')),
      L("So at least fifty-four guests know both. Choice number one is our answer.",
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
    S('Method 2 · Insight: stay in percent',
      L("[pause] Now an insight, the one from the lesson. Many students see the percents and start calculating numbers "
        "right away. But we can stay in percent. We start again from the givens. In percent, the whole is a hundred percent."),
      L("Forty-five percent plus seventy percent is a hundred fifteen percent. That's fifteen percent over the hundred "
        "percent.", show(g74k, 'Forty-five percent plus seventy'), show(g74l, "That's fifteen percent over")),
      L("So at least fifteen percent know both. Now just one calculation. Ten percent of three hundred sixty is "
        "thirty-six, and five percent is eighteen. Thirty-six plus eighteen is fifty-four.",
        show(g74m, 'Thirty-six plus eighteen')),
      L("One small calculation instead of four, and that's why we stay in percent. Choice number one again.")),
    S('Method 3 · Understanding: the two circles',
      L("[pause] Now let's see it by understanding, with the two circles. We start again from the givens. Forty-five "
        "percent know the artist, and seventy percent know the owner.", show(g74v['line'], 'with the two circles')),
      L("Forty-five plus seventy is a hundred fifteen. The guests are only a hundred percent. So the circles must overlap "
        "by at least fifteen percent.", show(g74v['both'], 'So the circles must overlap')),
      L("Then artist only is forty-five minus fifteen, thirty percent. Owner only is seventy minus fifteen, fifty-five "
        "percent.", show(g74n, 'forty-five minus fifteen'), show(g74v['a'], 'thirty percent'), show(g74v['b'], 'fifty-five percent')),
      L("Thirty plus fifteen plus fifty-five is a hundred percent. So neither is zero.",
        show(g74o, 'Thirty plus fifteen plus'), show(g74v['out'], 'So neither is zero')),
    ),
    S('Method 3 · Understanding: the two circles',
      L("Must the overlap be fifteen? No, fifteen is only the smallest. Say twenty percent know both. Artist only is "
        "forty-five minus twenty, twenty-five. Owner only is seventy minus twenty, fifty. Together, twenty-five plus "
        "twenty plus fifty is ninety-five percent. So a hundred minus ninety-five, five percent know neither.",
        show(g74v20['line'], 'Say twenty percent know both'), show(g74v20['both'], 'twenty percent know both'),
        show(g74p, 'forty-five minus twenty'), show(g74v20['a'], 'twenty-five. Owner'),
        show(g74p2, 'seventy minus twenty'), show(g74v20['b'], 'fifty. Together'),
        show(g74p3, 'twenty-five plus twenty plus fifty'), show(g74p4, 'a hundred minus ninety-five'),
        show(g74v20['out'], 'five percent know neither'))),
    S('Method 3 · Understanding: the two circles',
      L("And the biggest overlap is forty-five percent. Put the whole artist group inside the owner group. Then artist "
        "only is zero. Owner only is seventy minus forty-five, twenty-five. Everyone in either group is in the owner's "
        "seventy percent. So a hundred minus seventy, thirty percent know neither.",
        show(g74v45['line'], 'the biggest overlap is forty-five percent'), show(g74v45['both'], 'forty-five percent'),
        show(g74q, 'artist only is zero'), show(g74v45['a'], 'artist only is zero'),
        show(g74q2, 'seventy minus forty-five'), show(g74v45['b'], 'twenty-five. Everyone'),
        show(g74q3, 'a hundred minus seventy'), show(g74v45['out'], 'thirty percent know neither')),
      L("So the overlap can be anything from fifteen to forty-five percent. They ask for the least, fifteen percent, "
        "fifty-four guests. Choice number one is our answer, and I'll see you in the next question.",
        show(g74r, 'anything from fifteen to forty-five'), mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp24-g075 (Hebrew: the farm school, 40 students, orchard 18, barn 7)
# Hebrew (wp 4837-4910): "neither in a range question confuses us, that's what makes it harder"; way 1 the range rules
# on the two complements (not orchard 22, not barn 33; "neither" = both of them; the biggest 22 rules out two choices,
# the smallest 55 - 40 = 15 rules out 11; the range 15 to 22); way 2 the insight (two choices left, only one can be
# right, so one is inside the range and the other too small: the bigger one; "not trivial, with practice; and if not,
# one more small calculation"). English method 3 (kept from the September course): through "at least one place".
# APPLICATION (R37, first use; taught in wp-068 part 3): a range question about neither; neither = the overlap of the two "not" groups.
g75a = IH('g75a', 'not library: $\\ 52-24=28$', size=30, col=1)
g75b = IH('g75b', 'not kitchen: $\\ 52-13=39$', size=30, col=1)
g75v = VENN2('g75v', 'not library 28', 'not kitchen 39', [('both', [('tint', 'both'), ('lab', 'both', 'neither', 'mid')])], w=560)
g75c = IH('g75c', 'biggest: $\\ 28$', size=30, col=1)
g75d = IH('g75d', '$28+39=67$', size=30, col=1)
g75e = IH('g75e', '$67-52=15$', size=30, col=1)
g75f = IH('g75f', 'neither: $\\ $from $15$ to $28$', size=30, col=1)
g75g = IH('g75g', 'neither $\\le28$', size=30, col=1)
g75h = IH('g75h', '$13,\\ 19$: $\\ $one in, one too small', size=30, col=1)
g75i = IH('g75i', 'fewest in a place: $\\ 24$', size=30, col=1)
g75j = IH('g75j', 'most in a place: $\\ 24+13=37$', size=30, col=1)
g75k = IH('g75k', '$52-37=15$', size=30, col=1)
g75l = IH('g75l', '$52-24=28$', size=30, col=1)
video('solve-wp24-g075', 'solution', qid='wp24-g075', slides=[
    S('Method 1 · The math way: the range rules',
      L("A class has fifty-two students. Of them, twenty-four help in the library and thirteen help in the kitchen. Which "
        "of the following could be the number of students who help in neither place?",
        pt('stem', 'A class has fifty-two', 'hl', 8.0), voice='calm', pause=0.5),
      L("Could be, so this is a range question. But this time they ask about neither, not about both. That's what makes "
        "it harder. We'll solve it in three different ways. With the range rules, with an insight, and through the "
        "students in at least one place.", pt('stem', 'Could be, so this is a range')),
      L("Let's start with the math way, like the art students in the lesson. Neither means not in the library, and also "
        "not in the kitchen. So first let's find these two groups."),
      L("Not in the library is fifty-two minus twenty-four, twenty-eight students. Not in the kitchen is fifty-two minus "
        "thirteen, thirty-nine students.", show(g75a, 'fifty-two minus twenty-four'), show(g75b, 'fifty-two minus thirteen')),
      L("Neither is the students who are in both of these groups. Not in the library, and also not in the kitchen. So "
        "neither is the overlap of these two new groups.", show(g75v['line'], 'in both of these groups'),
        show(g75v['both'], 'So neither is the overlap')),
      L("Now we use the range rules on them. The biggest overlap is the smaller group, twenty-eight. So neither is at most "
        "twenty-eight.", show(g75c, 'The biggest overlap is the smaller group')),
      L("So choice number one, thirty-six, and choice number four, thirty-one, are out. Both are more than twenty-eight.",
        mk('cross', 'choice 1', 'So choice number one'), mk('cross', 'choice 4', 'choice number four, thirty-one'))),
    S('Method 1 · The math way: the range rules',
      L("The smallest overlap is the sum minus the total. Twenty-eight plus thirty-nine is sixty-seven. Sixty-seven minus "
        "fifty-two is fifteen. So neither is at least fifteen.", show(g75d, 'Twenty-eight plus thirty-nine'),
        show(g75e, 'Sixty-seven minus fifty-two')),
      L("So choice number two, thirteen, is out. It's less than fifteen.", mk('cross', 'choice 2', "It's less than fifteen")),
      L("So neither is from fifteen to twenty-eight, and nineteen fits. Choice number three is our answer.",
        show(g75f, 'from fifteen to twenty-eight'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Insight',
      L("[pause] Now an insight that saves a calculation. We start again from the givens. Fifty-two minus twenty-four "
        "is twenty-eight students not in the library. Neither must be among those students, so neither is at most "
        "twenty-eight. That rules out thirty-six and thirty-one.",
        show(g75g, 'so neither is at most twenty-eight'), mk('cross', 'choice 1', 'That rules out'),
        mk('cross', 'choice 4', 'thirty-six and thirty-one')),
      L("Two choices are left, thirteen and nineteen. A question has only one right answer. So one of them is inside the "
        "range, and the other one is outside it.", show(g75h, 'Two choices are left')),
      L("Both are less than twenty-eight, so the wrong one must be too small. Which one is too small? The smaller one, "
        "thirteen.", mk('cross', 'choice 2', 'The smaller one, thirteen')),
      L("So the answer is nineteen, without calculating the minimum at all. It takes practice. And if you're not sure, "
        "the minimum is just one more small calculation. Choice number three again.", mk('tick', 'choice 3', 'Choice number three again'))),
    S('Method 3 · Understanding: at least one place',
      L("[pause] And one more way, by understanding. We start again from the givens. Neither is the total minus the "
        "students who help in at least one place."),
      L("The fewest in at least one place is when all thirteen kitchen helpers also help in the library. Then it's just "
        "the twenty-four library helpers.", show(g75i, 'The fewest in at least one place')),
      L("The most in at least one place is when nobody helps in both. Twenty-four plus thirteen is thirty-seven. That's "
        "less than fifty-two, so it can happen.", show(g75j, 'Twenty-four plus thirteen')),
      L("Neither is fifty-two minus that number. Fifty-two minus thirty-seven is fifteen. And fifty-two minus twenty-four "
        "is twenty-eight. The same range, fifteen to twenty-eight.", show(g75k, 'Fifty-two minus thirty-seven'),
        show(g75l, 'fifty-two minus twenty-four')),
      L("So a big overlap means few students in at least one place, and many in neither. Choice number three is our "
        "answer, and I'll see you in the next question.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t24-01 (added: the least of another region)
# English addition (real exam 2020_autumn_q1_11: "at most ... not soccer and not swimming" = the same logic). R37 2026-10-21: APPLICATION (taught in wp-068 part 3,
# two examples): "at least / at most" is about the region they ask; which overlap makes THAT region small or big; the
# trap (the smallest overlap gives the MOST swim only). The second example (at most neither) was cut: the lesson now
# teaches neither ranges and g075 applies them.
q1a = IH('q1a', 'swim only $=32-$ both', size=30, col=1)
q1b = IH('q1b', 'small swim only: $\\ $big both', size=30, col=1)
q1c = IH('q1c', 'biggest both $=27$', size=30, col=1)
q1d = IH('q1d', '$32-27=5$', size=32, col=1)
q1e = IH('q1e', '$32+27=59$, $\\ 59-50=9$', size=30, col=1)
q1f = IH('q1f', '$32-9=23$: $\\ $the most', size=30, col=1)
q1s = STRIP('q1s', 'run', 'swim', [
    ('T', [('T', 'all four: 50')]), ('A', [('A', 'swim: 32')]), ('B', [('B', 'run: 27')]), ('v2', [('v', 2, '27')]),
    ('v1', [('v', 1, '0')]), ('v3', [('v', 3, '5')]), ('v0', [('v', 0, '18')])], w=560)
q1g = IH('q1g', '$32-27=5$', size=30, col=1)
q1h = IH('q1h', '$50-32=18$', size=30, col=1)
video('solve-q-r26-t24-01', 'solution', qid='q-r26-t24-01', slides=[
    S('Method 1 · Understanding: which overlap?',
      L("A club has fifty members. Of them, thirty-two swim and twenty-seven run. At least how many members swim but do "
        "not run?", pt('stem', 'A club has fifty members', 'hl', 6.0), voice='calm', pause=0.5),
      L("At least, so it's a range question. But careful, they don't ask about both. They ask about the members who swim "
        "but don't run, swim only. We'll solve it in two different ways, by understanding, and then with the squares "
        "method.", pt('stem', 'They ask about the members who swim')),
      L("Let's start by understanding, like art only in the lesson. First we write the region with both in it. Swim only "
        "is the swimmers who are not in both. So swim only is thirty-two minus both.", show(q1a, 'So swim only is thirty-two minus both')),
      L("Now the key question. To make swim only as small as possible, what should both be? The bigger both is, the "
        "smaller swim only is. So we need the biggest overlap.", show(q1b, 'So we need the biggest overlap')),
      L("The biggest overlap is the smaller group. All twenty-seven runners also swim.", show(q1c, 'All twenty-seven runners')),
      L("So swim only is thirty-two minus twenty-seven, five. At least five members swim but don't run.",
        show(q1d, 'thirty-two minus twenty-seven'))),
    S('Method 1 · Understanding: which overlap?',
      L("Here's the trap. At least makes us think of the smallest overlap. Thirty-two plus twenty-seven is fifty-nine. "
        "Fifty-nine minus fifty is nine. That's choice number three, but nine is both, not swim only.",
        show(q1e, 'Thirty-two plus twenty-seven'), mk('cross', 'choice 3', "That's choice number three")),
      L("And with that smallest overlap, swim only is thirty-two minus nine, twenty-three. That's choice number four. But "
        "twenty-three is the most swim only can be, the opposite of what they ask.", show(q1f, 'thirty-two minus nine'),
        mk('cross', 'choice 4', "That's choice number four")),
      L("So here at least is about swim only, not about both. Choice number two is our answer.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · The math way: the squares method',
      L("[pause] Now let's see it with the squares method. We start again from the givens. We draw four boxes. Neither, run only, "
        "both, and swim only. All four together are fifty.", show(q1s['line'], 'Four boxes'), show(q1s['T'], 'All four together'),
        show(q1s['A'], 'swim only'), show(q1s['B'], 'run only')),
      L("For the least swim only, we put all twenty-seven runners in both. So run only is zero.",
        show(q1s['v2'], 'we put all twenty-seven'), show(q1s['v1'], 'So run only is zero')),
      L("Swim only is thirty-two minus twenty-seven, five.", show(q1g, 'thirty-two minus twenty-seven'), show(q1s['v3'], 'five.')),
      L("And neither is fifty minus the thirty-two swimmers, eighteen. Every box works, so five can really happen.",
        show(q1h, 'fifty minus the thirty-two'), show(q1s['v0'], 'eighteen')),
      L("Could swim only be less than five? Only if more than twenty-seven were in both. But there are only twenty-seven "
        "runners. So five is the least. Choice number two is our answer, and I'll see you in the next question.",
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ wp24-g076 (Hebrew: the company, 1/3 English, 3/4 car, 1/4 teens, 2/5 line)
# Hebrew (wp 4912-5024): each choice is "at least one is in both" = must there be an overlap?; add the fractions (the
# whole is 1): more than 1 -> forced (the statement is true, the choice is out); exactly 1 -> not forced (60 workers: 15
# teens without a licence, 45 car owners); less than 1 -> also not forced, "the minimum is 0, not minus"; way 2 in
# percent (1/3 = 33%, "I wrote 33 and not 33 and a third, the third is negligible unless near 100"); "this is what you
# do! in the exam, convert to percent". APPLICATION (R37): must an overlap exist? (the smallest-overlap rule, wp-068), fractions -> percent (wp-068 part 2). W17: every
# choice read in full first.
# W23 (2026-10-22): night shifts 3/10 -> 1/3, so her "write 33, not 33 and a third: the third only matters right next to
# 100, and 33 + 75 is far above it" acts on a fraction that is in the question again.
g76r = I('g76r', 'Over the whole? $\\ $An overlap must exist', size=28, col=1)
g76a = IH('g76a', 'not new $\\frac{3}{4}$, $\\ $not nights $\\frac{2}{3}$', size=34)
g76b = IH('g76b', '$\\frac{9}{12}+\\frac{8}{12}=\\frac{17}{12}>1$', size=34, col=1)
g76c = IH('g76c', '$\\frac{4}{12}+\\frac{9}{12}=\\frac{13}{12}>1$', size=34, col=1)
g76d = IH('g76d', '$\\frac{1}{4}+\\frac{3}{4}=1$', size=34, col=1)
g76e = IH('g76e', '$12$ nurses: $\\ 3$ new, $\\ 9$ drive', size=28)
g76f = IH('g76f', '$\\frac{3}{6}+\\frac{4}{6}=\\frac{7}{6}>1$', size=34, col=1)
g76g = IH('g76g', 'nights $33$, $\\ $drive $75$, $\\ $new $25$, $\\ $part time $50$', size=28)
g76h = IH('g76h', 'not new $75$, $\\ $not nights $67$', size=28, col=1)
g76i = IH('g76i', '(1) $\\ 75+67=142$', size=28, col=1)
g76j = IH('g76j', '(2) $\\ 33+75=108$', size=28, col=1)
g76m = IH('g76m', 'with the third: $\\ 108\\frac{1}{3}$, $\\ $far above $100$', size=28, col=1)
g76k = IH('g76k', '(3) $\\ 25+75=100$', size=28, col=1)
g76l = IH('g76l', '(4) $\\ 50+67=117$', size=28, col=1)
video('solve-wp24-g076', 'solution', qid='wp24-g076', slides=[
    S('Method 1 · The math way: add the fractions',
      L("Of a hospital's nurses, one third work night shifts, three quarters drive to work, one quarter are new, and "
        "one half work part time. Which statement is not necessarily true?", pt('stem', "Of a hospital's nurses", 'hl', 8.0),
        voice='calm', pause=0.5),
      L("Every choice says that at least one nurse is in two groups at once. So every choice claims that an overlap must "
        "exist. We need the one claim that is not forced. We'll solve it in two different ways, by adding fractions, and "
        "then in percent.", pt('choice 1', 'Every choice says')),
      L("Let's start with the math way. When must an overlap exist? Remember the smallest overlap. Only when the two "
        "groups add up to more than the total. Here the givens are fractions, so like in the lesson, the total is one.",
        show(g76r, 'Only when the two groups add up')),
      L("Choice number one says, at least one nurse who is not new does not work night shifts. Not new is one minus a "
        "quarter, three quarters. Not nights is one minus a third, two thirds.", pt('choice 1', 'Choice number one says'),
        show(g76a, 'Not new is one minus a quarter')),
      L("Three quarters is nine twelfths, and two thirds is eight twelfths. Together, that's seventeen twelfths. "
        "That's more than one, so an overlap must exist.", show(g76b, 'Three quarters is nine twelfths')),
      L("So the statement is true. They ask for the one that's not necessarily true, so choice number one is out.",
        mk('cross', 'choice 1', 'so choice number one is out'))),
    S('Method 1 · The math way: add the fractions',
      L("Choice number two says, at least one night-shift nurse drives to work. A third plus three quarters. Four "
        "twelfths plus nine twelfths is thirteen twelfths. More than one, so it's true, and choice number two "
        "is out.", pt('choice 2', 'Choice number two says'), show(g76c, 'Four twelfths plus nine'),
        mk('cross', 'choice 2', "so it's true, and choice number two")),
      L("Choice number three says, at least one new nurse drives to work. A quarter plus three quarters is exactly one. "
        "It's not more than one.", pt('choice 3', 'Choice number three says'), show(g76d, 'A quarter plus three quarters')),
      L("Exactly one doesn't force an overlap. The two groups can sit side by side. Let's see it in numbers. Say there are "
        "twelve nurses, because twelve splits into thirds and quarters. A quarter, three, are new. Three quarters, nine, "
        "drive.", show(g76e, 'Say there are twelve nurses')),
      L("The three new nurses come by bus, and the other nine drive. Every fraction still works, and no new nurse "
        "drives. So choice number three is not necessarily true.")),
    S('Method 1 · The math way: add the fractions',
      L("In the exam you'd circle it and move on. Here, let's check the last one too. Choice number four says, at least "
        "one part-time nurse does not work night shifts. A half plus two thirds is three sixths plus four sixths, seven "
        "sixths. More than one, so it's true.", pt('choice 4', 'Choice number four says'), show(g76f, 'three sixths plus four sixths'),
        mk('cross', 'choice 4', "More than one, so it's true")),
      L("Choice number three is our answer. And if two groups add up to less than one, then no overlap is forced either. "
        "The smallest overlap is zero, never negative.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Insight: work in percent',
      L("[pause] Now an insight, the one from the lesson. Adding fractions takes time, and percents are much faster. We "
        "start again from the givens, and turn every fraction into percent. Again, we need the claim that isn't forced."),
      L("A third is thirty-three and a third percent. Let's write just thirty-three, and in a moment we'll see why that's "
        "fine. Three quarters is seventy-five percent. A quarter is twenty-five percent, and a half is fifty percent.",
        show(g76g, 'A third is thirty-three')),
      L("Not new is a hundred minus twenty-five, seventy-five. Not nights is a hundred minus thirty-three, sixty-seven.",
        show(g76h, 'Not new is a hundred minus'))),
    S('Method 2 · Insight: work in percent',
      L("Choice number one says at least one nurse who is not new does not work night shifts. Seventy-five plus sixty-seven "
        "is a hundred forty-two. That's more than a hundred, so the overlap is forced. Choice number two says at least "
        "one night-shift nurse drives to work. Thirty-three plus seventy-five is a hundred eight. Again, the overlap is forced.",
        show(g76i, 'Seventy-five plus sixty-seven'), show(g76j, 'Thirty-three plus seventy-five')),
      L("Now, why could we drop the third of a percent? With it, choice number two would be a hundred eight and a third. "
        "Dropping the third changes a sum by less than one. So it matters only when the sum lands right next to a hundred, like "
        "ninety-nine and a bit. A hundred eight is far above a hundred, so the overlap is forced with or without the third.",
        show(g76m, 'With it, choice number two would be'))),
    S('Method 2 · Insight: work in percent',
      L("Choice number three says at least one new nurse drives to work. Twenty-five plus seventy-five is exactly a "
        "hundred, so the overlap isn't forced. Choice number four says at least one part-time nurse does not work night "
        "shifts. Fifty plus sixty-seven is a hundred seventeen, more than a hundred. That overlap is forced.",
        show(g76k, 'Twenty-five plus seventy-five'), show(g76l, 'Fifty plus sixty-seven')),
      L("So in the exam, turn the fractions into percent. Choice number three is our answer, and I'll see you in the next "
        "question.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
])


# ------------------------------------------------------------------------------------------------ r26-t24-two-way (lesson, English addition)
# Real exam: 2025_winter_q1_15, 2024_winter_q2_02, 2021_autumn_q2_11, 2020_autumn_q1_11 (a percent of a sub-group, two
# traits). A short intro (the table is built in the guided question after it): two yes/no traits = the four regions as
# a table with totals; the trap - percents of different wholes can't be added or averaged - with the numbers that show
# why (40 women, 60 men: 26%, not 50% and not 25%). NEW. REMINDER: 10% of a number (topic 23).
w_t = TBL('w_t', ['Walk', "Don't walk", 'Total'], ['Upper', 'Lower', 'Total'], [
    ('reg', [('box', 0, 0), ('box', 0, 1), ('box', 1, 0), ('box', 1, 1)])], colw=170, labw=130, size=30)
w_a = IH('w_a', '$20\\%$ of the women, $\\ 30\\%$ of the men', size=30)
w_b = IH('w_b', '$20\\%+30\\%=50\\%$? $\\ $No', size=30, col=1)
w_c = IH('w_c', 'average $25\\%$? $\\ $Not guaranteed', size=30, col=1)
w_ex = TBL('w_ex', ['Glasses', 'No glasses', 'Total'], ['Women', 'Men', 'Total'], [
    ('women', [('c', 0, 2, '40')]), ('men', [('c', 1, 2, '60')]), ('all', [('c', 2, 2, '100')]),
    ('wg', [('c', 0, 0, '8')]), ('mg', [('c', 1, 0, '18')]), ('glasses', [('c', 2, 0, '26')])],
    colw=150, labw=110, rowh=62, headh=48, size=30, w=560)
w_d = IH('w_d', '$40$ women: $\\ 20\\%$ of $40=8$', size=30, col=1)
w_e = IH('w_e', '$60$ men: $\\ 30\\%$ of $60=18$', size=30, col=1)
w_f = IH('w_f', '$8+18=26$: $\\ 26\\%$', size=32, col=1)
w_g = I('w_g', 'Find each group\'s count first. $\\ $Then add counts, not percents.', size=28)
video('r26-t24-two-way', 'lesson', slides=[
    S('Two-Way Tables',
      L("Welcome back. Sometimes every person in a question has two traits. For example, a student is in the upper "
        "grades or the lower grades. And the student walks to school, or doesn't.")),
    S('Two traits, four boxes',
      L("These are really our four regions again. A student can be upper and walk, or upper and not walk. Or the student "
        "can be lower and walk, or lower and not walk. Here a table is clearer than circles.", show(w_t['line'], 'These are really'),
        show(w_t['reg'], 'A student can be upper')),
      L("Each row is one group, and each column is the other trait. And we add a total for every row and every column.")),
    S('The trap: different wholes',
      L("Here's the trap in these questions. Say twenty percent of the women wear glasses, and thirty percent of the men "
        "wear glasses. What percent of everyone wears glasses?", show(w_a, 'Say twenty percent of the women')),
      L("A lot of students add, and say fifty percent. Others take the average, twenty-five percent. But twenty-five "
        "isn't guaranteed either. We don't know the group sizes yet.",
        show(w_b, 'A lot of students add'), show(w_c, 'Others take the average')),
      L("Why? Because the twenty percent is of the women, and the thirty percent is of the men. These are percents of "
        "different wholes."),
      L("Let's see it in numbers. Put women and men in rows. Say there are forty women and sixty men, a hundred people. "
        "In the glasses column, twenty percent of forty is eight. Thirty percent of sixty is eighteen.",
        show(w_ex['line'], 'Put women and men in rows'), show(w_ex['women'], 'forty women'), show(w_ex['men'], 'sixty men'),
        show(w_ex['all'], 'a hundred people'), show(w_d, 'twenty percent of forty'), show(w_ex['wg'], 'is eight'),
        show(w_e, 'Thirty percent of sixty'), show(w_ex['mg'], 'is eighteen')),
      L("Eight plus eighteen is twenty-six. So twenty-six people out of a hundred wear glasses, twenty-six percent. Not "
        "fifty, and not twenty-five.", show(w_f, 'Eight plus eighteen'), show(w_ex['glasses'], 'Eight plus eighteen')),
      L("So find how many wear glasses in each group first. Add those counts, and compare with the total number of "
        "people. The table keeps the groups clear. Let's see it in a guided question. Try it first, and I'll see you in the next video.",
        show(w_g, 'Add those counts'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t24-02 (added: a two-way table, percent of the walkers)
# Real exam 2025_winter_q1_15 type. NEW (full): filling the table (plug in 100; a percent of a row is of that row's
# total), rows add across and columns add down, "of the students who walk" = the whole is the walk column, each wrong
# choice = a wrong whole. REMINDERS: plug in a hundred, 10% of a number, "of" points at the whole (topic 23).
q2t = TBL('q2t', ['Walk', "Don't walk", 'Total'], ['Upper', 'Lower', 'Total'], [
    ('t100', [('c', 2, 2, '100')]), ('rows', [('c', 0, 2, '40'), ('c', 1, 2, '60')]), ('u', [('c', 0, 0, '12')]),
    ('l', [('c', 1, 0, '36')]), ('w', [('c', 2, 0, '48')])],
    colw=150, labw=110, rowh=62, headh=48, size=30, col=0, w=560)
q2t2 = TBL('q2t2', ['Walk', "Don't walk", 'Total'], ['Upper', 'Lower', 'Total'], [
    ('vals', [('c', 2, 2, '100'), ('c', 0, 2, '40'), ('c', 1, 2, '60'), ('c', 0, 0, '12'), ('c', 1, 0, '36'), ('c', 2, 0, '48')]),
    ('col', [('box', 0, 0), ('box', 1, 0), ('box', 2, 0)])], colw=150, labw=110, rowh=62, headh=48, size=30, col=0, w=560)
q2a = IH('q2a', '$100-40=60$', size=30)
q2b = IH('q2b', '$10\\%$ of $40=4$, $\\ 30\\%=12$', size=30, col=1)
q2c = IH('q2c', '$10\\%$ of $60=6$, $\\ 60\\%=36$', size=30, col=1)
q2d = IH('q2d', '$12+36=48$', size=30, col=1)
q2e = IH('q2e', '$\\frac{12}{48}=\\frac{1}{4}=25\\%$', size=34, col=1)
q2f = IH('q2f', '(1) $\\ 12$ out of $100$', size=30, col=1)
q2g = IH('q2g', '(3) $\\ 12$ out of $36$', size=30, col=1)
q2h = IH('q2h', '(4) $\\ 40$ out of $100$', size=30, col=1)
q2i = I('q2i', 'Percent of what? $\\ $The words after "of" give the whole.', size=28)
video('solve-q-r26-t24-02', 'solution', qid='q-r26-t24-02', slides=[
    S('Method 1 · Plugging in numbers',
      L("In a school, forty percent of the students are in the upper grades, and the rest are in the lower grades. Thirty "
        "percent of the upper-grade students and sixty percent of the lower-grade students walk to school. What percent "
        "of the students who walk to school are in the upper grades?", pt('stem', 'In a school', 'hl', 12.0), voice='calm',
        pause=0.5),
      L("So the whole here is not all the students. They ask about the students who walk. Each student has two traits, "
        "the grade and walking, so we'll use a table.", pt('stem', 'They ask about the students who walk')),
      L("Let's plug in numbers. There are only percents in the question, so let's say there are a hundred students. A "
        "hundred makes every percent of the school a number of students.", show(q2t['line'], "let's say there are a hundred"),
        show(q2t['t100'], 'A hundred makes every percent')),
      L("Forty percent are in the upper grades, so forty students. The rest, a hundred minus forty, sixty, are in the lower "
        "grades.", show(q2a, 'a hundred minus forty'), show(q2t['rows'], 'are in the lower grades')),
      L("Now let's fill in walking. The question says thirty percent of the upper-grade students walk. So it's thirty percent of the "
        "forty, not of the hundred. Ten percent of forty is four, so thirty percent is twelve.",
        pt('stem', 'The question says thirty percent'), show(q2b, 'Ten percent of forty'), show(q2t['u'], 'so thirty percent is twelve')),
      L("Sixty percent of the sixty lower-grade students walk. Ten percent of sixty is six, so sixty percent is "
        "thirty-six.", show(q2c, 'Ten percent of sixty'), show(q2t['l'], 'thirty-six')),
      L("Rows add across, and columns add down. So down the walk column, twelve plus thirty-six is forty-eight students "
        "who walk.", show(q2d, 'twelve plus thirty-six'), show(q2t['w'], 'forty-eight students'))),
    S('Method 1 · Plugging in numbers',
      L("Now let's read the question again. Of the students who walk. So the whole is the walk column, forty-eight "
        "students, not a hundred.", pt('stem: ask', "Now let's read the question again"), show(q2t2['line'], 'Of the students who walk'),
        show(q2t2['vals'], 'Of the students who walk'), show(q2t2['col'], 'So the whole is the walk column')),
      L("Twelve of the forty-eight walkers are in the upper grades. Twelve out of forty-eight is a quarter, because four "
        "times twelve is forty-eight. A quarter is twenty-five percent.", show(q2e, 'Twelve out of forty-eight')),
      L("Choice number two is our answer.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('The traps',
      L("Each wrong choice comes from the wrong whole. Choice number one, twelve percent, is twelve out of all the hundred "
        "students.", show(q2f, 'twelve out of all the hundred'), mk('cross', 'choice 1', 'Choice number one, twelve percent')),
      L("Choice number three, thirty-three and a third percent, compares twelve with the thirty-six lower-grade walkers. "
        "Twelve out of thirty-six is a third. But the whole is all the walkers.", show(q2g, 'Twelve out of thirty-six'),
        mk('cross', 'choice 3', 'But the whole is all the walkers')),
      L("Choice number four, forty percent, is the upper grades out of all the students. It ignores walking.",
        show(q2h, 'the upper grades out of all'), mk('cross', 'choice 4', 'It ignores walking')),
      L("So always ask, percent of what? The words after of tell us the whole, the row or the column we divide by. Choice "
        "number two is our answer, and I'll see you in the next question.", show(q2i, 'percent of what'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ r26-t24-three-groups (lesson, English addition)
# Real exam 2024_autumn_q1_19 (the least in all three = 0, by who is missing) and 2023_autumn_q2_20 (every pair shares
# 10 -> from 0 to 10). Not in the Hebrew course. NEW: count who is missing (as if all different people), the link to
# two groups (the same as the sum minus the total), more missing than the total -> 0 (with a construction that shows 0
# can happen), the most in all three = the smallest group, pairs given -> the smallest pair. The lesson's numbers are
# not the practice questions' numbers.
t_r1 = I('t_r1', 'In all three, at least: $\\ $total $-$ the ones who miss a group', size=30)
t_x1 = I('t_x1', '$10$ friends: $\\ $tea $8$, $\\ $coffee $9$, $\\ $juice $7$', size=30)
t_x2 = IH('t_x2', 'miss: $\\ 2,\\ 1,\\ 3$', size=30, col=1)
t_x3 = IH('t_x3', '$2+1+3=6$', size=30, col=1)
t_x4 = IH('t_x4', '$10-6=4$', size=30, col=1)
t_y1 = IH('t_y1', 'two groups: $\\ 5+6=11$, $\\ 15-11=4$', size=30)
t_z0 = I('t_z0', '$50$ readers: $\\ $fiction $30$, $\\ $history $35$, $\\ $science $25$', size=30)
t_z1 = IH('t_z1', 'miss: $\\ 20+15+25=60$', size=30, col=1)
t_z2 = IH('t_z2', '$60>50$: $\\ $smallest $0$', size=30, col=1)
t_z3 = I('t_z3', 'fiction and history $15$ $\\cdot$ fiction and science $15$ $\\cdot$ history and science $10$ $\\cdot$ only history $10$', size=26)
t_z4 = IH('t_z4', 'fiction: $\\ 15+15=30$', size=30, col=1)
t_z5 = IH('t_z5', 'history: $\\ 15+10+10=35$', size=30, col=1)
t_z6 = IH('t_z6', 'science: $\\ 15+10=25$', size=30, col=1)
t_z7 = I('t_z7', 'Most in all three $=$ the smallest group', size=30)
t_p0 = I('t_p0', 'chess $40$, $\\ $drama $35$, $\\ $music $30$', size=30)
t_p1 = I('t_p1', 'pairs: $\\ $chess and drama $12$, $\\ $chess and music $9$, $\\ $drama and music $15$', size=28)
t_p2 = IH('t_p2', 'smallest pair: $\\ 9$', size=30, col=1)
t_p3 = I('t_p3', 'Pairs given? $\\ $Most in all three $=$ the smallest pair', size=30)
t_p4 = IH('t_p4', 'chess: $\\ 12+9=21\\le40$', size=30, col=1)
t_p5 = IH('t_p5', 'drama: $\\ 12+15=27\\le35$', size=30, col=1)
t_p6 = IH('t_p6', 'music: $\\ 9+15=24\\le30$', size=30, col=1)
t_p7 = IH('t_p7', 'all three: $\\ $from $0$ to $9$', size=30, col=1)
# 2026-10-21 (external-course review, approved): exact three-group counts by counting appearances (memberships), not
# people: 3 performances x 9 actors = 27 appearances; all three 3 x 3 = 9, exactly two 6 x 2 = 12, 27 - 21 = 6 -> 6
# actors in exactly one (15 actors). New numbers (not the other course's 3 x 7). The pair regions are never filled one by
# one (their split is unknown); the link back to two groups (wp-069: exactly one = A + B - 2 x both).
t_e0 = I('t_e0', 'A play: $\\ 3$ performances, $\\ 9$ actors in each', size=28)
t_e1 = I('t_e1', 'all three: $\\ 3$ actors, $\\ $exactly two: $\\ 6$ actors', size=28)
t_ev = VENN3('t_ev', ['first', 'second', 'third'], [
    ('three', [('tint', 'three'), ('lab', 'three', 'all\nthree')]),
    ('two', [('tint', 'two'), ('lab', 'two', 'exactly\ntwo')]),
    ('one', [('tint', 'one'), ('lab', 'one', 'exactly\none')]),
    ('x1', [('tag', 'one', '×1')]), ('x2', [('tag', 'two', '×2')]), ('x3', [('tag', 'three', '×3')])], w=560)
t_e2 = IH('t_e2', '$3\\times9=27$ appearances', size=30, col=1)
t_e4 = IH('t_e4', 'all three: $\\ 3\\times3=9$', size=30, col=1)
t_e5 = IH('t_e5', 'exactly two: $\\ 6\\times2=12$', size=30, col=1)
t_e6 = IH('t_e6', '$9+12=21$', size=30, col=1)
t_e7 = IH('t_e7', '$27-21=6$', size=30, col=1)
t_e8 = IH('t_e8', 'exactly one: $\\ 6$ actors', size=30, col=1)
t_e9 = IH('t_e9', 'actors: $\\ 3+6+6=15$', size=30, col=1)
t_ek = I('t_ek', 'Add the groups: $\\ $appearances, not people', size=26, col=1)
t_el = I('t_el', 'The totals only, $\\ $not who is in which pair', size=26, col=1)
video('r26-t24-three-groups', 'lesson', slides=[
    S('Three Groups',
      L("Welcome back, and now three groups. Sometimes the exam adds a third group, and asks how many must be in all "
        "three.")),
    S('Count who is missing',
      L("At least how many are in all three groups? Let's turn the question around. Who is not in all three? Anyone who "
        "misses at least one group."),
      L("So we count the people who miss each group, as if they're all different people. That's the most people who can "
        "miss something. Everyone else must be in all three.", show(t_r1, 'Everyone else must be in all three')),
      L("Let's see it in numbers. There are ten friends. Eight like tea, nine like coffee, and seven like juice.",
        show(t_x1, 'There are ten friends')),
      L("Two don't like tea, one doesn't like coffee, and three don't like juice. Two plus one plus three is six.",
        show(t_x2, "Two don't like tea"), show(t_x3, 'Two plus one plus three')),
      L("So at most six friends miss something. The other ten minus six, four friends, must like all three.",
        show(t_x4, 'The other ten minus six')),
      L("It's the same idea as with two groups. Fifteen students, ten in art and nine in drama. Five miss art, and six "
        "miss drama. Five plus six is eleven, so at least fifteen minus eleven, four are in both. The same four as the "
        "sum minus the total.", show(t_y1, 'Five plus six is eleven'))),
    S('Can it be zero?',
      L("Now careful. What if the people who miss a group add up to more than the total? There are fifty readers. Thirty read "
        "fiction, thirty-five read history, and twenty-five read science.", show(t_z0, 'There are fifty readers')),
      L("Twenty miss fiction, fifteen miss history, and twenty-five miss science. Twenty plus fifteen plus twenty-five is "
        "sixty. That's more than fifty readers.", show(t_z1, 'Twenty plus fifteen plus')),
      L("Fifty minus sixty would be negative. But a number of people can't be negative. So, just like with two groups, "
        "the smallest is zero.", show(t_z2, 'the smallest is zero')),
      L("Is zero really possible? Here's one way. Fifteen read fiction and history. Fifteen read fiction and science. Ten "
        "read history and science. And ten read only history.", show(t_z3, "Here's one way")),
      L("Fiction is fifteen plus fifteen, thirty. History is fifteen plus ten plus ten, thirty-five. Science is fifteen "
        "plus ten, twenty-five. That's fifty readers, and nobody reads all three.", show(t_z4, 'Fiction is fifteen plus fifteen'),
        show(t_z5, 'History is fifteen plus ten'), show(t_z6, 'Science is fifteen plus ten')),
      L("And the most in all three? The people in all three are inside every group. So it can't be more than the smallest "
        "group. Here that's twenty-five.", show(t_z7, 'the smallest group'))),
    S('Pairs given',
      L("One more case. Sometimes they also tell us how many each pair of groups shares. Here are three clubs. Forty "
        "students are in chess, thirty-five in drama, and thirty in music.", show(t_p0, 'Here are three clubs')),
      L("Twelve are in both chess and drama. Nine are in both chess and music. And fifteen are in both drama and music. At "
        "most how many are in all three?", show(t_p1, 'Twelve are in both chess and drama')),
      L("Someone in all three clubs is also in every pair. So the all-three group fits inside each pair. It can't be "
        "bigger than the smallest pair, nine.", show(t_p2, 'the smallest pair, nine')),
      L("So the most is nine, not thirty. When we know only the groups, the smallest group is the limit. When the pairs "
        "are given, the smallest pair is the limit.", show(t_p3, 'When the pairs are given')),
      L("And the least? Here it can be zero. In chess, twelve plus nine is twenty-one, and that fits in forty. In drama, "
        "twelve plus fifteen is twenty-seven, and that fits in thirty-five. In music, nine plus fifteen is twenty-four, "
        "and that fits in thirty. So the pairs can all be different people.", show(t_p4, 'twelve plus nine is twenty-one'),
        show(t_p5, 'twelve plus fifteen is twenty-seven'), show(t_p6, 'nine plus fifteen is twenty-four')),
      L("So here it's from zero to nine.", show(t_p7, 'from zero to nine'))),
    S('Count the appearances',
      L("Now a question with exact numbers. A school play had three performances, with nine actors in each "
        "performance.", show(t_e0, 'A school play had three performances')),
      L("Three actors were in all three performances, and six actors were in exactly two. How many actors were in "
        "exactly one performance?", show(t_e1, 'Three actors were in all three')),
      L("Let's draw the three performances as three circles. Each circle holds the nine actors of one performance.",
        show(t_ev['line'], 'as three circles')),
      L("The circles make three kinds of regions. In the middle are the actors in all three performances.",
        show(t_ev['three'], 'In the middle are the actors')),
      L("Where just two circles overlap, outside the middle, are the actors in exactly two.",
        show(t_ev['two'], 'Where just two circles overlap')),
      L("And the outer part of each circle is for the actors in exactly one performance. That's what we're looking "
        "for.", show(t_ev['one'], 'And the outer part of each circle')),
      L("We don't know how the six actors in exactly two are split among the three pairs. And we don't need it. "
        "So instead of people, we count appearances. Every time an actor plays in one performance, that's one appearance."),
      L("There are three performances, with nine actors in each. So three times nine is twenty-seven appearances.",
        show(t_e2, 'So three times nine')),
      L("Now, how many appearances does each actor make? An actor in exactly one performance appears once. An actor "
        "in exactly two appears twice. And an actor in all three appears three times.",
        show(t_ev['x1'], 'An actor in exactly one performance appears once'),
        show(t_ev['x2'], 'in exactly two appears twice'), show(t_ev['x3'], 'And an actor in all three')),
      L("Remember, with two groups, we took both away twice, because the people in both are counted in each group. "
        "Here it's the same idea, with three groups."),
      L("The three actors in all three performances make three times three, nine appearances.",
        show(t_e4, 'three times three, nine')),
      L("The six actors in exactly two make six times two, twelve appearances.", show(t_e5, 'six times two, twelve')),
      L("Together that's nine plus twelve, twenty-one appearances. Twenty-seven minus twenty-one leaves six "
        "appearances.", show(t_e6, 'nine plus twelve'), show(t_e7, 'Twenty-seven minus twenty-one')),
      L("Who made those six appearances? Only the actors in exactly one performance are left, and each of them appears "
        "once. So six actors were in exactly one performance.", show(t_e8, 'So six actors were in exactly one')),
      L("So when we add up the groups, we count appearances, not people. How many different actors were there? Three "
        "plus six plus six is fifteen. So there were fifteen actors, not twenty-seven.", show(t_ek, 'we count appearances, not people'),
        show(t_e9, 'Three plus six plus six')),
      L("Here we know every group's size, and the counts in all three and exactly two. So we can subtract their "
        "appearances to find exactly one. We need those other counts too, not just the group sizes. Counting appearances doesn't tell us which "
        "pair each actor was in, and we don't need that.", show(t_el, "doesn't tell us which pair")),
      L("Now let's see a guided question. Try it first, and I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ q-r26-t24-03 (added: three groups, the least in all three)
# Real exam 2024_autumn_q1_19 type. REMINDERS: count who is missing (the lesson before), plug in 100 (topic 23). The
# bar: the hundred people as 20 boxes of 5, the missing people side by side. Traps at the step: 55% (two groups only),
# 70% (the most = the smallest group).
q3u = UNITS('q3u', [('100', 20)], [
    ('p', [('fill', 0, 0, 4, 'blue'), ('br', 0, 0, 4, 'no phone 20')]),
    ('l', [('fill', 0, 4, 9, 'orange'), ('br', 0, 4, 9, 'no laptop 25', 'up')]),
    ('t', [('fill', 0, 9, 15, 'yellow'), ('br', 0, 9, 15, 'no tablet 30')]),
    ('a', [('fill', 0, 15, 20), ('br', 0, 15, 20, 'all three: 25', 'up')])], unit=26, boxh=40, labw=70, gap=60, w=560)
q3a = IH('q3a', '$100-80=20$', size=30, col=1)
q3b = IH('q3b', '$100-75=25$', size=30, col=1)
q3c = IH('q3c', '$100-70=30$', size=30, col=1)
q3d = IH('q3d', '$20+25+30=75$', size=30, col=1)
q3e = IH('q3e', '$100-75=25$', size=32, col=1)
q3r = I('q3r', '$A+B+C-2\\cdot$ total', size=30)
q3f = IH('q3f', '$80+75+70=225$', size=30, col=1)
q3g = IH('q3g', '$225-200=25$', size=32, col=1)
q3h = IH('q3h', 'missing: $\\ 300-225=75$', size=30, col=1)
q3i = IH('q3i', '$80+75-100=55$: $\\ $two groups', size=28, col=1)
video('solve-q-r26-t24-03', 'solution', qid='q-r26-t24-03', slides=[
    S('Method 1 · Understanding: count who is missing',
      L("In a survey, eighty percent of the people own a phone, seventy-five percent own a laptop, and seventy percent "
        "own a tablet. At least what percent of the people own all three?", pt('stem', 'In a survey', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("They ask for the smallest percent who own all three items. We'll solve it in two different ways, by counting "
        "who is missing, and then with a short formula.", pt('stem', 'the smallest percent who own all three items')),
      L("Let's start by understanding. There are only percents here, so let's plug in a hundred people. Then each percent "
        "is a number of people.", show(q3u['line'], "let's plug in a hundred people")),
      L("Who doesn't own each item? A hundred minus eighty, twenty have no phone. A hundred minus seventy-five, "
        "twenty-five have no laptop. And a hundred minus seventy, thirty have no tablet.",
        show(q3a, 'A hundred minus eighty'), show(q3u['p'], 'twenty have no phone'), show(q3b, 'A hundred minus seventy-five'),
        show(q3u['l'], 'twenty-five have no laptop'), show(q3c, 'A hundred minus seventy,'), show(q3u['t'], 'thirty have no tablet')),
      L("We put them side by side, as if they're all different people. Twenty plus twenty-five plus thirty is "
        "seventy-five.", show(q3d, 'Twenty plus twenty-five plus thirty')),
      L("So at most seventy-five people miss at least one item. The other twenty-five must own all three. That's "
        "twenty-five percent.", show(q3e, 'The other twenty-five'), show(q3u['a'], 'must own all three')),
      L("Choice number two is our answer.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · The math way: the formula',
      L("[pause] Now the math way, with a short formula. We start again from the givens. We add the three groups, and "
        "subtract the total twice.", show(q3r, 'We add the three groups')),
      L("Eighty plus seventy-five plus seventy is two hundred twenty-five. Two times a hundred is two hundred. Two hundred "
        "twenty-five minus two hundred is twenty-five.", show(q3f, 'Eighty plus seventy-five plus seventy'),
        show(q3g, 'Two hundred twenty-five minus two hundred')),
      L("Why subtract two hundreds? If everyone owned all three items, we'd count everyone three times, three hundred. "
        "We actually count two hundred twenty-five. So three hundred minus two hundred twenty-five is seventy-five missing "
        "places in the groups. Those can belong to at most seventy-five different people. A hundred minus seventy-five "
        "leaves at least twenty-five with all three. That's the same as two hundred twenty-five minus two hundred.", show(q3h, 'three hundred minus two hundred')),
      L("Careful with choice number three, fifty-five percent. That's eighty plus seventy-five minus a hundred, only the "
        "phone and the laptop.", show(q3i, 'eighty plus seventy-five minus a hundred'), mk('cross', 'choice 3', 'only the phone and the laptop')),
      L("And choice number four, seventy percent, is the most, the smallest group. They ask for the least. Choice number "
        "two is our answer, and I'll see you in the next question.", mk('cross', 'choice 4', 'They ask for the least'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])
# 21 Oct Codex review: independent results get individual spoken-clause rows.
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
                        it = IH(name if not j else name+'_clause'+str(j), tex,
                                size=old.get('size',30), col=old['_col'])
                        cues.append(show(it, anchor))
                else: cues.append(cue)
            def cue_pos(c):
                anchor = c[2] if c[0] in ('show','point') else c[3]
                return -1 if anchor.startswith('<') else ln['say'].lower().find(anchor.lower())
            ln['cues'] = sorted(cues, key=cue_pos)
    assert found == 1, (vid, name, found)

_clause_rows('wp-067', 'a_f5',
    ('$22+$ neither $=30$', 'So twenty-two plus neither is thirty'),
    ('neither $=8$', 'neither is eight'))
_clause_rows('wp-068', 'r_m3',
    ('dog $8$, cat $12$: $\\ $biggest $8$', 'The biggest overlap is eight'))
_clause_rows('wp-068', 'r_m4',
    ('$6$ and $6$: $\\ $biggest $6$', 'Then the biggest overlap is six'))
_clause_rows('wp-068', 'r_z4',
    ('$17-20=-3$: $\\ $not an overlap', 'seventeen minus twenty, and get minus three'),
    ('smallest overlap: $0$', 'so the smallest overlap is zero'))
_clause_rows('wp-068', 'r_p4',
    ('$10\\%$ of $200=20$', 'Ten percent of two hundred is twenty'),
    ('$5\\%$ of $200=10$', 'five percent is ten'),
    ('$15\\%$: $20+10=30$ people', 'So fifteen percent is twenty plus ten'))
_clause_rows('wp-068', 'r_f4',
    ('$70\\%+50\\%=120\\%$', 'Seventy plus fifty is a hundred twenty'),
    ('$120\\%-100\\%=20\\%$', 'so twenty percent'))
_clause_rows('wp-068', 'r_e5',
    ('$5+6=11$', 'Five plus six is eleven'),
    ('$11<15$: $\\ $smallest $0$', 'so the smallest overlap is zero'))
_clause_rows('solve-wp24-g072', 'g72p3',
    ('chess only: $18-2=16$', 'Chess only is eighteen minus two'),
    ('robotics only: $8-2=6$', 'Robotics only is eight minus two'))
_clause_rows('solve-wp24-g072', 'g72f2',
    ('$\\frac{1}{9}\\cdot9=1$', 'A ninth of nine is one'),
    ('$\\frac{1}{4}\\cdot4=1$', 'a quarter of four is one'))
_clause_rows('solve-wp24-g072', 'g72f3',
    ('$9-1=8$', 'Nine minus one is eight'),
    ('$4-1=3$', 'four minus one is three'))
_clause_rows('solve-wp24-g077', 'g77h',
    ('morning: $48\\div4=12$', 'a quarter of forty-eight, twelve'),
    ('evening: $48\\div6=8$', 'a sixth of forty-eight, eight'))
_clause_rows('solve-wp24-g074', 'g74n',
    ('artist only: $45-15=30$', 'forty-five minus fifteen'),
    ('owner only: $70-15=55$', 'seventy minus fifteen'))
# Restore the already-spoken subtraction in the independent shortcut method.
for _sl in VIDEOS['solve-wp24-g075']['slides']:
    for _ln in _sl['lines']:
        if _ln['say'].startswith('[pause] Now an insight that saves a calculation.'):
            _ln['cues'].insert(0, show(IH('g75g_start', '$52-24=28$ not in the library', size=30, col=1),
                                      'Fifty-two minus twenty-four'))
for _sl in VIDEOS['solve-q-r26-t24-03']['slides']:
    for _ln in _sl['lines']:
        if 'Two times a hundred is two hundred.' in _ln['say']:
            _ln['cues'].insert(1, show(IH('q3_twice_total', '$2\\cdot100=200$', size=30, col=1),
                                      'Two times a hundred is two hundred'))
_clause_rows('solve-q-r26-t24-01', 'q1e',
    ('$32+27=59$', 'Thirty-two plus twenty-seven is fifty-nine'),
    ('$59-50=9$', 'Fifty-nine minus fifty is nine'))
_clause_rows('solve-wp24-g076', 'g76a',
    ('not new: $1-\\frac{1}{4}=\\frac{3}{4}$', 'Not new is one minus a quarter'),
    ('not nights: $1-\\frac{1}{3}=\\frac{2}{3}$', 'Not nights is one minus a third'))
_clause_rows('solve-wp24-g076', 'g76e',
    ('$12$ nurses: $\\ 3$ new', 'A quarter, three, are new'),
    ('$9$ drive', 'Three quarters, nine, drive'))
_clause_rows('solve-wp24-g076', 'g76g',
    ('nights: $33\\%$', 'Let\'s write just thirty-three'),
    ('drive: $75\\%$', 'Three quarters is seventy-five percent'),
    ('new: $25\\%$', 'A quarter is twenty-five percent'),
    ('part time: $50\\%$', 'a half is fifty percent'))
_clause_rows('solve-wp24-g076', 'g76h',
    ('not new: $100-25=75\\%$', 'Not new is a hundred minus twenty-five'),
    ('not nights: $100-33=67\\%$', 'Not nights is a hundred minus thirty-three'))
# Keep the four conversions in two readable columns, clear of the choices.
for _sl in VIDEOS['solve-wp24-g076']['slides']:
    for _ln in _sl['lines']:
        for _cue in _ln['cues']:
            if _cue[0] == 'show' and _cue[1]['_name'] in ('g76g_clause2', 'g76g_clause3'):
                _cue[1]['_col'] = 1
_clause_rows('r26-t24-two-way', 'w_f',
    ('$8+18=26$ people', 'Eight plus eighteen is twenty-six'),
    ('$26$ out of $100=26\\%$', 'twenty-six people out of a hundred'))
_clause_rows('solve-q-r26-t24-02', 'q2b',
    ('$10\\%$ of $40=4$', 'Ten percent of forty is four'),
    ('$30\\%$ of $40=12$', 'so thirty percent is twelve'))
_clause_rows('solve-q-r26-t24-02', 'q2c',
    ('$10\\%$ of $60=6$', 'Ten percent of sixty is six'),
    ('$60\\%$ of $60=36$', 'so sixty percent is thirty-six'))
_clause_rows('r26-t24-three-groups', 't_x2',
    ('no tea: $2$', "Two don't like tea"),
    ('no coffee: $1$', "one doesn't like coffee"),
    ('no juice: $3$', "three don't like juice"))
_clause_rows('r26-t24-three-groups', 't_y1',
    ('$5+6=11$', 'Five plus six is eleven'),
    ('$15-11=4$', 'fifteen minus eleven, four are in both'))
_clause_rows('r26-t24-three-groups', 't_z3',
    ('fiction and history only: $15$', 'Fifteen read fiction and history'),
    ('fiction and science only: $15$', 'Fifteen read fiction and science'),
    ('history and science only: $10$', 'Ten read history and science'),
    ('history only: $10$', 'And ten read only history'))

CARRY24 = {}
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
 "wp24-g070": "Of 52 hotel guests, 31 use the pool, 26 use the gym, and 17 use both. How many use neither?",
 "wp24-g071": "A print shop has 27 printers. Of them, 16 print in color, 13 print large posters, and 3 do neither. How many printers both print in color and print large posters?",
 "wp24-g072": "The students who are in both the chess club and the robotics club make up $\\frac19$ of the chess club and $\\frac14$ of the robotics club. What is the ratio of chess club students who are not in the robotics club to robotics club students who are not in the chess club?",
 "wp24-g078": "Two friends list the movies they watched this year. One lists 34 movies and the other lists 27. Together, their lists show 45 different movies. How many movies appear on both lists?",
 "wp24-g077": "At a conference, $\\frac14$ of the participants attend the morning workshop, $\\frac16$ attend the evening workshop, and $\\frac1{12}$ attend both. Exactly 4 participants attend both. How many participants attend neither workshop?",
 "wp24-g074": "At a gallery opening with 360 guests, 45% know the artist and 70% know the gallery owner. What is the minimum number of guests who know both?",
 "wp24-g075": "A class has 52 students. Of them, 24 help in the library and 13 help in the kitchen. Which of the following could be the number of students who help in neither place?",
 "q-r26-t24-01": "A club has 50 members. Of them, 32 swim and 27 run. At least how many members swim but do not run?",
 "wp24-g076": "Of a hospital's nurses, $\\frac13$ work night shifts, $\\frac34$ drive to work, $\\frac14$ are new, and $\\frac12$ work part time. Which statement is not necessarily true?",
 "q-r26-t24-02": "In a school, $40\\%$ of the students are in the upper grades and the rest are in the lower grades. $30\\%$ of the upper-grade students and $60\\%$ of the lower-grade students walk to school. What percent of the students who walk to school are in the upper grades?",
 "q-r26-t24-03": "In a survey, $80\\%$ of the people own a phone, $75\\%$ own a laptop, and $70\\%$ own a tablet. At least what percent of the people own all three?",
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
CP.split(globals(), *WP068_SPLIT)    # 2026-10-21 R37: the range lesson grew (core methods back in it), 3 parts, not on camera

for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _stem_parts(_v); _write_gap(_v)



# 2026-10-13 carry-over boxes (V2) and the layer-order check (V1): after the visual passes, like topics 13-18
import types as _types
MV.carry(_types.SimpleNamespace(**globals()), CARRY24)
for _v in CARRY24:                                      # 2026-10-18 visual check: the So-far box at a readable size
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
