"""Topic 51 (Psychometric Thinking) - the scripts for the teacher's own-voice reading (2026-10-14), written from the first draft to
the Codex review standard, the clarity style, the method visuals (geometry: the angle figure built in layers, GEO below), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py / _ai_vis_t16.py / _ai_vis_t17.py / _ai_vis_t18.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

EVERY topic-51 video is a camera video (2026-10-14: she reads all of topic 51 with the camera on); long lessons are split
into parts of about 3-4 minutes (CAMERA_SPLITS, math_patches/_camera_parts.py). Every topic-51 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t51.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: math_patches/_t51_reading.py ai_redo_t51() (called by build_verbal.py) (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods and EVERY method of the Hebrew solution (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-51-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t51ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-51 flow order of the scripts
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
            'style': "the teacher reads it herself (Reading Studio), topic-51 scripts (2026-10-14): math_patches/_ai_vis_t51.py is "
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
    for b in out:                      # topic 51 is all camera (V4): the stem stays left of the face bubble (top right)
        for it in b['pre']:
            if it.get('k') == 'q': it['stemw'] = STEMW
    return out, sb


STEMW = 0.8       # the question stem's width (renderer_patch.py it.stemw): it ends at about x 1310 of 1600, the bubble starts at 1344


def rebuild(M, vid):
    """replace the studio video's slides by the spec (spoken lines only); _ai_visual.apply adds cues + items."""
    if vid == 'solve-pt-q06':
        # Both -4 and -3 satisfy the givens; the choices ask for a possible value.
        M.set_q('pt-q06', stem=STEMS['pt-q06'])
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


# ------------------------------------------------------------------------------------------- topic-51 geometry figures (V1)
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



CARRY51 = {}       # carry-over boxes (V2): {vid: {slide index: [tex, ...]}}, filled by the scripts


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
# =================================================================================================================
# Topic 51, block 1 (fragment f1, TAG A, 2026-10-14): the intro lesson, the first five course-book questions, and the
# wrap-up. Hebrew: studio-build/pt_src/seg1_intro.txt (all of it). Camera videos, read by her.
# NEW here (full first teaching, R29 / R32): thinking instead of calculating (intro lesson, two examples), the last digit
# (q01 + 23 x 47), the size of the answer (q01 + root of 1,849). INTRODUCED here as in the Hebrew intro, with their why,
# one more example and the "when" (their full lessons come later): plugging in the answers (q02 + x^2 + x = 110),
# plugging in numbers (q03 + 2^(x+1) + 2^x), estimation (q04 + a circle in a square), insight questions (q05).
# Taught on the spot (not in the plan yet): the volume of a cylinder / a cube (q04), probability as good over all (q05).
# =================================================================================================================
import math as _f1m


def f1_fig(name, layers, vb, w, col=0, title='Figure'):
    """a figure built in layers from raw SVG bodies (same mechanics as GEO): layers = [(key, body), ...]"""
    out = [(k, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, title if k == 'line' else '%s: %s' % (title, k), title if k == 'line' else '%s: %s' % (title, k), b))
           for k, b in layers]
    g = _layers(name, out, w, col)
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


def f1_t(x, y, t, c=GINK, size=28, anchor='middle', italic=False):
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" dominant-baseline="middle" fill="%s" %s font-size="%d" font-weight="bold"%s>%s</text>'
            % (x, y, anchor, c, GFONT, size, ' font-style="italic"' if italic else '', t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')))


# =================================================================================================== pt51-intro (lesson)
f1i1 = I('f1i1', 'What stands behind the questions?', size=44)
f1i2 = I('f1i2', 'Understand it, and the questions get easier', size=38)
f1i3 = I('f1i3', 'The goal: to predict success in academic studies', size=38)
f1i4 = I('f1i4', 'A sorting exam: it ranks the candidates', size=38)
f1i5 = I('f1i5', 'The math way: a formula, an equation, a long calculation', size=36)
f1i6 = I('f1i6', 'The shortcut: think first, then calculate only what you need', size=36)
f1i7 = IH('f1i7', '$25\\cdot4\\cdot37\\div37=?$', size=40)
f1i8 = I('f1i8', '$\\times37$ and $\\div37$ cancel', size=36)
f1i8b = IH('f1i8b', '$25\\cdot4=100$', size=36)
f1i9 = IH('f1i9', '$999+999+999=?$', size=40)
f1i10 = IH('f1i10', '$999=1000-1$', size=36)
f1i10b = IH('f1i10b', '$3000-3=2997$', size=36)
f1i11 = I('f1i11', 'When? Every question: look at the numbers and the answers first', size=32)
f1i12 = I('f1i12', 'Tests for gifted children look for creative thinkers', size=38)
f1i13 = I('f1i13', 'A few methods let us solve as if we were gifted', size=38)
f1i14 = I('f1i14', '1 · Plugging in the answers', size=42)
f1i15 = I('f1i15', '2 · Plugging in numbers', size=42)
f1i16 = I('f1i16', '3 · Order-of-magnitude estimation: the size of the answer', size=38)
f1i17 = I('f1i17', 'And here and there: insight questions', size=38)
f1i18 = I('f1i18', 'Practice both ways when both fit the question', size=36)
f1i19 = I('f1i19', 'The math way, and the psychometric way', size=38)

video('pt51-intro', 'lesson', slides=[
    S('Psychometric Thinking',
      L("Welcome back. In this topic, we're learning psychometric thinking. We'll look for easier ways to solve quantitative reasoning questions.")),
    S('What stands behind the questions',
      L("In these lessons, we'll look at how the exam questions are built.", show(f1i1, 'how the exam questions are built')),
      L("That understanding will help you approach the questions in the right way, and in an easier way.",
        show(f1i2, 'That understanding will help'))),
    S('What the exam is for',
      L("So what is the goal of the psychometric exam? To predict success in academic studies.", show(f1i3, 'To predict success')),
      L("It's a sorting exam, so it has to rank the candidates. How does it do that? The questions on the exam are special "
        "questions.", show(f1i4, "It's a sorting exam"))),
    S('Special questions',
      L("What does that mean? Usually, when we solve a question, we use a way we know from school. We plug into a formula, "
        "we build an equation, and so on.", show(f1i5, 'we use a way we know from school')),
      L('On the exam, many questions also have a shortcut. We can notice something in the numbers or choices. That can get us to the answer faster.', show(f1i6, 'also have a shortcut')),
      L("That's psychometric thinking, and that's what the exam tests. It looks for the students who think this way, and it "
        "gives them an advantage.")),
    S('Think before you calculate',
      L("Let's see what that looks like on a small example. Twenty-five times four, times thirty-seven, divided by "
        "thirty-seven. The calculating way multiplies everything first, and then divides the product by thirty-seven. That's long, and "
        "it's easy to slip.", show(f1i7, 'Twenty-five times four')),
      L("The thinking way looks at the numbers first. Times thirty-seven, and then divided by thirty-seven, cancel each "
        "other, because dividing undoes the multiplying. So we're left with twenty-five times four, which is a hundred.",
        show(f1i8, 'Times thirty-seven, and then'), show(f1i8b, "So we're left with")),
      L("One more. Nine hundred ninety-nine, plus nine hundred ninety-nine, plus nine hundred ninety-nine. Instead of "
        "adding column by column, think of a thousand. Each one is a thousand minus one. So three of them are three "
        "thousand minus three, which is two thousand nine hundred ninety-seven.",
        show(f1i9, 'One more'), show(f1i10, 'Each one is a thousand minus one'), show(f1i10b, 'So three of them')),
      L("Why does this work? We didn't skip any math. We looked at the numbers before we started, and we chose an easier "
        "way to the same result. So when do we do it? On every question. Before you calculate, take a few seconds to look "
        "at the numbers and at the answers. If the calculation looks long, that's a sign there's a shorter way.",
        show(f1i11, 'So when do we do it'))),
    S('Like a test for gifted children',
      L("It's like the tests for gifted children. They look for the creative kids, the ones who think in a less obvious "
        "way. The exam questions work on a similar idea.", show(f1i12, 'tests for gifted children')),
      L("You don't need to be gifted to learn these shortcuts. A small number of methods can help us find them. We'll call these our super-methods.", show(f1i13, 'a small number of methods'))),
    S('The super-methods',
      L("There are three super-methods. Plugging in the answers. Plugging in numbers. And order-of-magnitude estimation, "
        "which means finding roughly how big the answer must be.",
        show(f1i14, 'Plugging in the answers'), show(f1i15, 'Plugging in numbers'), show(f1i16, 'order-of-magnitude')),
      L("And here and there, there are insight questions, with an idea that belongs to one question only.",
        show(f1i17, 'insight questions')),
      L("In the next sample questions, we'll meet each of them for the first time. Later, each method gets a lesson of "
        "its own.")),
    S('How to practice',
      L("When you do your homework, practice both ways when both fit the question. The mathematical way, and the "
        "psychometric way. Don't force a second method if it adds nothing.", show(f1i18, 'practice both ways'), show(f1i19, 'The mathematical way')),
      L("That's the right way to learn and to practice. Let's start with a sample question. [pause] Okay. I'll see you in "
        "the next video.")),
])


# =================================================================================================== solve-pt-q01
# Hebrew: no calculator, but answers; the calculating way = square every choice; the last digit (6 x 6 = 36, 4 x 4 = 16
# -> out; 8 x 8 = 64, 2 x 2 = 4 fit); two left; 200 x 200 = 40,000 -> 212 too big; 138 without calculating; what we
# learned: the answers are part of the question, thinking vs calculating. Course numbers: 19,044 (138, 156, 194, 212).
# Added: the why of the last digit (156 = 150 + 6), its limit (the trap), one more example of each shortcut and its "when".
f1a1 = IH('f1a1', '$19{,}04\\hl{u}{4}$ $\\ $ends in $4$', size=34)
f1a2 = IH('f1a2', '$156=150+6$', size=34)
f1a3 = IH('f1a3', '(2) $\\ 6\\cdot6=36$ $\\ $ends in $6$ ✗', size=32)
f1a4 = IH('f1a4', '(3) $\\ 4\\cdot4=16$ $\\ $ends in $6$ ✗', size=32)
f1a5 = IH('f1a5', '(1) $\\ 8\\cdot8=64$ ✓', size=32)
f1a6 = IH('f1a6', '(4) $\\ 2\\cdot2=4$ ✓', size=32)
f1b1 = IH('f1b1', '$200\\cdot200=40{,}000$', size=34)
f1b2 = IH('f1b2', '$19{,}044<40{,}000$', size=34)
f1b3 = IH('f1b3', '(4) $\\ 212>200\\ \\Rightarrow\\ 212^2>40{,}000$ ✗', size=32)
f1c1 = IH('f1c1', '$23\\cdot47=?$', size=36)
f1c2 = I('f1c2', '$1{,}079\\qquad 1{,}081\\qquad 1{,}084\\qquad 1{,}086$', size=34)
f1c3 = IH('f1c3', '$3\\cdot7=21$ $\\ $ends in $1$', size=34)
f1c4 = I('f1c4', '$1{,}081$ ✓', size=34)
f1c5 = I('f1c5', 'When? A whole-number calculation, and the choices end in different digits', size=28)
f1d1 = IH('f1d1', '$\\sqrt{1{,}849}=?$', size=36)
f1d2 = I('f1d2', '$33\\qquad 43\\qquad 53\\qquad 63$', size=34)
f1d3 = IH('f1d3', '$3\\cdot3=9$ $\\ $all four fit', size=32)
f1dn = ZL('f1dn', 28, 68, [('sq', [('below', 40, '1,600'), ('below', 50, '2,500')]),
                           ('band', [('shade', 40, 50)]),
                           ('ch', [('ink', 33, '33'), ('pt', 43, '43'), ('ink', 53, '53'), ('ink', 63, '63')]),
                           ('out', [('cross', 33), ('cross', 53), ('cross', 63)])],
          ticks=[(40, '40'), (50, '50')], w=900, title='Number line: 40 squared and 50 squared')
f1d5 = I('f1d5', 'When? The choices are far apart: compare with a round number', size=28)

video('solve-pt-q01', 'solution', qid='pt-q01', slides=[
    S('The last digit',
      L("The square root of nineteen thousand forty-four. What is it equal to?", pt('stem', 'The square root', 'hl', 5.0),
        voice='calm', pause=0.5),
      L("We need the number that, times itself, gives nineteen thousand forty-four. Working out that square root directly would take a long calculation, and on the exam there's no calculator. [short pause] No calculator, but I do have four answers.",
        pt('choice 1', 'I do have four answers')),
      L("The calculating way is to multiply each answer by itself, and see which one gives our number. But that's a long "
        "multiplication, maybe four times. That's where the shortcut comes in. We'll use the choices, with two quick "
        "checks, the last digit and the size."),
      L("First, the last digit. Our number ends in four. So the answer, times itself, must end in four.", show(f1a1, 'Our number ends in four')),
      L("And to see how a square ends, we only need the last digit. Why? Take a hundred fifty-six. It's a hundred fifty plus six. When we multiply this by itself, any part containing a hundred fifty ends in zero. Only six times six can change the last digit.", show(f1a2, "It's a hundred fifty plus six")),
      L("Six times six is thirty-six, so a hundred fifty-six squared ends in six. Six is not four, so I don't need to "
        "keep calculating. Choice number two is out.", show(f1a3, 'Six times six is thirty-six'),
        mk('cross', 'choice 2', 'Choice number two is out')),
      L("The same way, a hundred ninety-four. Four times four is sixteen, so it ends in six again. Choice number three is "
        "out too.", show(f1a4, 'Four times four is sixteen'), mk('cross', 'choice 3', 'Choice number three is out')),
      L('Now a hundred thirty-eight. Its last digit is eight. Eight times eight is sixty-four, which ends in four, so this choice stays. For two hundred twelve, two times two is four. That choice stays too.', show(f1a5, 'Now a hundred thirty-eight'), show(f1a6, 'For two hundred twelve')),
      L("So the last digit ruled out two answers, and two are still left. That's its limit. It can only rule choices "
        "out. When two choices both end the right way, it can't choose between them.")),
    S('The size',
      L("So we need a second shortcut, the size. Let's compare with a round number that's easy to square, and close to the biggest choice, two hundred twelve. How much is two "
        "hundred times two hundred? Two times two is four, and we add the four zeros. Forty thousand.",
        show(f1b1, 'How much is two hundred times two hundred')),
      L("Our number, nineteen thousand forty-four, is much less than forty thousand.", show(f1b2, 'Our number')),
      L("And two hundred twelve is more than two hundred, so its square is even more than forty thousand. Why? When we "
        "square a bigger positive number, we get a bigger result. So two hundred twelve is far too big, and choice number "
        "four is out.", show(f1b3, 'And two hundred twelve'), mk('cross', 'choice 4', 'choice number four is out')),
      L("Three choices are out, and one of the four must be right. So a hundred thirty-eight is the answer, and I don't "
        "even need to check it. Choice number one is our answer.", mk('tick', 'choice 1', 'Choice number one is our answer')),
      L('We solved it without doing the full calculation. First by understanding, with a rule about the last digit, and then with an order-of-magnitude estimate. Both get a lesson of their own later in this topic.')),
    S('Last digit: another example',
      L("Let's see each shortcut once more, on a new example. First the last digit. Twenty-three times forty-seven. The "
        "choices are one thousand seventy-nine, one thousand eighty-one, one thousand eighty-four, and one thousand "
        "eighty-six.", show(f1c1, 'Twenty-three times forty-seven'), show(f1c2, 'The choices are')),
      L("They're all close in size, so the size won't help here. But they all end in different digits. So we look only "
        "at the last digits. Three times seven is twenty-one, so the result ends in one.", show(f1c3, 'Three times seven')),
      L("Only one thousand eighty-one ends in one, so that's the answer, with no long multiplication.",
        show(f1c4, 'Only one thousand eighty-one')),
      L("So when do I use the last digit? When the question is a calculation with whole numbers, like a product, a "
        "square, or a square root, and the choices end in different digits. Then one small multiplication can rule out "
        "choices.", show(f1c5, 'So when do I use the last digit'))),
    S('The size: another example',
      L("Now the size. The square root of one thousand eight hundred forty-nine. The choices are thirty-three, forty-three, "
        "fifty-three, and sixty-three.", show(f1d1, 'The square root of one thousand'), show(f1d2, 'The choices are')),
      L("Let's try the last digit first. Three times three is nine, and our number ends in nine. But all four choices end "
        "in three, so they all fit, and the last digit can't help at all.", show(f1d3, 'Three times three is nine')),
      L("So we use the size. Forty squared is one thousand six hundred, and fifty squared is two thousand five hundred.",
        show(f1dn['line'], 'So we use the size'), show(f1dn['sq'], 'Forty squared')),
      L("Our number is between them, so its root is between forty and fifty. And the only choice between forty and fifty "
        "is forty-three. The others are out.", show(f1dn['band'], 'Our number is between them'),
        show(f1dn['ch'], 'the only choice between'), show(f1dn['out'], 'The others are out')),
      L("So when do I use the size? When the choices are far apart from each other. Then compare with a round number "
        "you can square or multiply in your head, like forty, fifty, or two hundred.",
        show(f1d5, 'So when do I use the size'))),
    S('What we learned',
      L('So what did we learn from this question? First, on the exam, the answers are part of the question. Without them, this looks like a calculator question. With them, the answers help us solve it.'),
      L("Second, thinking versus calculating. You can always calculate the way we know from school. But often there's a "
        "shortcut, and it gets you to the answer faster. [pause] Okay. I'll see you in the next question.")),
])


# =================================================================================================== solve-pt-q02
# Hebrew: a before / after table, x eggs; 7/11 -> multiply by 11, open, 900 = 18x, divide by 9 first, x = 50; then
# plugging in the answers: one of the four must be right; 25 is long to check; don't go in order, start from the most
# convenient (round) answer; 50 -> 35/55 = 7/11; the first round answer is often right (the exam gives an advantage).
# Course numbers: 500, 600, 9/13, 50. Added: the why of plugging in, the trap (forget to add to B), "when", x^2 + x = 110.
f1e1 = IH('f1e1', 'Before: $\\ A=500,\\ \\ B=600$', size=32)
f1e2 = IH('f1e2', 'After: $\\ A=500-x,\\ \\ B=600+x$', size=32)
f1e3 = IH('f1e3', '$500-x=\\frac{9}{13}(600+x)$', size=34)
f1e4 = IH('f1e4', '$13(500-x)=9(600+x)$', size=34)
f1e5 = IH('f1e5', '$6500-13x=5400+9x$', size=34)
f1e6 = IH('f1e6', '$1100=22x$', size=34)
f1e7 = IH('f1e7', '$100=2x\\ \\Rightarrow\\ x=50$', size=34)
for _it, _y in ((f1e5, 440), (f1e6, 510), (f1e7, 580)):
    _R(_it, _y, x=1040)
f1f1 = I('f1f1', '(1) $\\ 25$: $\\ \\frac{475}{625}=\\frac{9}{13}\\ ?$ $\\ $long to check', size=32)
f1f2 = I('f1f2', 'Start with the most convenient answer, usually a round one', size=28)
f1f3 = IH('f1f3', '(2) $\\ 50$: $\\ A=450,\\ \\ B=650$', size=32)
f1f4 = IH('f1f4', '$\\frac{450}{650}=\\frac{45}{65}=\\frac{9}{13}$ ✓', size=34)
f1f5 = I('f1f5', 'When? One number is asked, the choices are numbers, and a check is easy', size=28)
f1f6 = IH('f1f6', '$x>0,\\quad x^2+x=110,\\quad x=?$', size=34)
f1f7 = I('f1f7', '$9\\qquad 10\\qquad 11\\qquad 12$', size=34)
f1f8 = IH('f1f8', '$10$: $\\ 10^2+10=100+10=110$ ✓', size=34)

video('solve-pt-q02', 'solution', qid='pt-q02', slides=[
    S('Method 1 · The math way',
      L("Basket A contains five hundred eggs, and basket B contains six hundred eggs. How many eggs must be moved from "
        "basket A to basket B, so that basket A will contain nine thirteenths of the number of eggs in basket B?",
        pt('stem', 'Basket A contains', 'hl', 10.0), voice='calm', pause=0.5),
      L("So eggs move from A to B, and after the move, A should have nine thirteenths of what B has. [short pause] We'll "
        "solve it two ways, the math way, with an equation, and then by plugging in the answers."),
      L("Let's put the numbers in order, before and after. Before the move, A has five hundred and B has six hundred. We "
        "don't know how many eggs we move, so let's call that number x.", show(f1e1, 'Before the move')),
      L("After the move, A has lost x eggs, so it has five hundred minus x. And those same x eggs went into B, so B has "
        "six hundred plus x.", show(f1e2, 'After the move')),
      L("Now the condition. A after the move is nine thirteenths of B after the move. So five hundred minus x equals nine "
        "thirteenths, times the bracket six hundred plus x.", show(f1e3, 'So five hundred minus x equals')),
      L("To get rid of the fraction, we multiply both sides by thirteen. Thirteen times the bracket five hundred minus x, "
        "equals nine times the bracket six hundred plus x.", show(f1e4, 'we multiply both sides by thirteen')),
      L("Let's multiply each term inside the brackets. On the left, thirteen times five hundred is six thousand five hundred. Thirteen times minus x is minus thirteen x. On the right, nine times six hundred is five thousand four hundred. Nine times x is nine x. So we have six thousand five hundred minus thirteen x, equal to five thousand four hundred plus nine x.", show(f1e5, "Let's multiply each term")),
      L("Now we add thirteen x to both sides, and take five thousand four hundred off both sides, so that the x's are on one side and the plain numbers on the other. Six thousand five "
        "hundred minus five thousand four hundred is one thousand one hundred. And nine x plus thirteen x is twenty-two x.",
        show(f1e6, 'Six thousand five hundred minus')),
      L("Instead of dividing by twenty-two in one go, let's divide both sides by eleven first, because smaller numbers are easier. That gives a hundred equals "
        "two x, so x is fifty. We move fifty eggs, and choice number two is our answer.",
        show(f1e7, 'divide both sides by eleven first'), mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now a second way, with psychometric thinking. One of our super-methods is plugging in the answers. What "
        "does that mean? They ask for one number, and they already give us four options. One of them must be the answer. "
        "So instead of building an equation, we put a choice into the story and check if it works."),
      L("Why is that easier? A check is just arithmetic. We add, we subtract, and we compare. Building the equation and "
        "solving it took several steps, and in each one we could slip."),
      L("Let's start with choice number one, twenty-five. If we move twenty-five, A has four hundred seventy-five, and B "
        "has six hundred twenty-five. Is four hundred seventy-five over six hundred twenty-five equal to nine thirteenths? "
        "We could reduce it bit by bit, but that's a fairly long calculation.", show(f1f1, 'If we move twenty-five')),
      L("But we don't have to check the choices in order. A very important rule in plugging in the answers is to start "
        "with the answer that's most convenient for you, usually a round one. Here, that's fifty, choice number two.",
        show(f1f2, 'A very important rule')),
      L("If we move fifty eggs, A has five hundred minus fifty, four hundred fifty. And careful here, the same fifty eggs "
        "go into B. So B has six hundred plus fifty, six hundred fifty. A lot of students take the eggs out of A, and "
        "forget to add them to B.", show(f1f3, 'If we move fifty eggs')),
      L('Now we compare with the given. A has to be nine thirteenths of B, so we look at A over B. Four hundred fifty over six hundred fifty. Divide the top and the bottom by ten, and we get forty-five over sixty-five. Both are divisible by five. Forty-five divided by five is nine, and sixty-five divided by five is thirteen. Nine thirteenths, exactly what the question asked. Choice number two is our answer.',
        show(f1f4, 'Now we compare'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Once a choice fits every given, we can mark it. The question has only one correct answer. Starting with a round number makes the check easier. But it doesn't guarantee that the round number is right. We still have to check it.")),
    SM('Method 2 · Plugging in the answers', 'When do I plug in the answers?',
      L("So when do I plug in the answers? When the question asks for one number, the choices are plain numbers, and "
        "it's easy to put a choice back into the question. It helps most when the equation is long, or when you don't "
        "know how to solve it at all. It's a safety net.", show(f1f5, 'So when do I plug in the answers')),
      L("Let's see one more example. x is positive. x squared plus x equals a hundred ten. What is x, if the choices are nine, ten, "
        "eleven, and twelve? An equation with x squared and x together, we haven't learned to solve yet. But we don't "
        "need to.", show(f1f6, 'x squared plus x equals'), show(f1f7, 'if the choices are')),
      L("Start with the round answer, ten. Ten squared is a hundred, and a hundred plus ten is a hundred ten. That's exactly what the equation needs, so it fits. So "
        "x is ten, and we're done without solving anything. [pause] Okay. I'll see you in the next question.",
        show(f1f8, 'Ten squared is a hundred'))),
])


# =================================================================================================== solve-pt-q03
# Hebrew: "what does it equal" = one choice is an equivalent expression; open the short formula, collect, split into three
# fractions (allowed: same denominator), 2ab/2ab = 1, +1 and -1 cancel, reduce -> a/b + b/a; plugging in numbers (the
# second super-method, one of the most important): equivalent -> the same values give the same result; any values that
# keep the condition; a = 1, and b = 1 too (no rule says different, the easiest); expression = 2; check every choice:
# 2 (keep checking), 1, 0, 4 -> out; "we don't look for the right answer, we rule out three". Course: (a - b)^2 and + 1.
# Added: why rule out three (a + b also gives 2), the tie-breaker, "when", 2^(x+1) + 2^x.
f1g1 = IH('f1g1', '$(a-b)^2=a^2-2ab+b^2$', size=32)
f1g2 = I('f1g2', '$\\dfrac{a^2+b^2+a^2-2ab+b^2}{2ab}+1$', size=34)
f1g2b = I('f1g2b', '$=\\dfrac{2a^2+2b^2-2ab}{2ab}+1$', size=34)
f1g3 = I('f1g3', '$=\\dfrac{2a^2}{2ab}+\\dfrac{2b^2}{2ab}-\\hl{o}{\\dfrac{2ab}{2ab}}+1$', size=36)
f1g4 = I('f1g4', '$=\\dfrac{a}{b}+\\dfrac{b}{a}-1+1=\\dfrac{a}{b}+\\dfrac{b}{a}$', size=36)
f1h1 = I('f1h1', 'The same expression $\\Rightarrow$ the same result for every $a,\\ b$', size=28)
f1h2 = IH('f1h2', '$a=1,\\ \\ b=1$', size=34)
f1h3 = IH('f1h3', 'Top: $\\ 1^2+1^2+(1-1)^2=1+1+0=2$', size=30)
f1h3b = IH('f1h3b', 'Bottom: $\\ 2\\cdot1\\cdot1=2$', size=30)
f1h3c = I('f1h3c', '$\\dfrac22+1=1+1=2$', size=34)
f1h4 = I('f1h4', '(1) $\\ \\dfrac11+\\dfrac11=2$ ✓', size=34)
f1h5 = I('f1h5', '(2) $\\ \\dfrac12+\\dfrac12=1$ ✗', size=34)
f1h6 = I('f1h6', '(3) $\\ \\dfrac{2\\cdot0}{1}=0$ ✗', size=34)
f1h7 = I('f1h7', '(4) $\\ 2(1+1)=4$ ✗', size=34)
f1h8 = I('f1h8', 'Rule out three: $\\ a+b$ also gives $2$', size=30)
f1j1 = I('f1j1', 'When? Letters in the question and letters in the choices', size=28)
f1j2 = IH('f1j2', '$2^{x+1}+2^x=?$', size=34)
f1j3 = I('f1j3', '(1) $2^{2x+1}$ $\\quad$ (2) $3\\cdot2^x$ $\\quad$ (3) $4^x$ $\\quad$ (4) $2^{x+3}$', size=30)
f1j4 = IH('f1j4', '$x=1$: $\\ 2^2+2^1=4+2=6$', size=32)
f1j5 = IH('f1j5', '(1) $\\ 2^3=8$ ✗', size=30)
f1j6 = IH('f1j6', '(2) $\\ 3\\cdot2=6$ ✓', size=30)
f1j7 = IH('f1j7', '(3) $\\ 4$ ✗', size=30)
f1j8 = IH('f1j8', '(4) $\\ 2^4=16$ ✗', size=30)
# Keep the new example's checks beside its calculation, clear of the old answer strip.
for _it, _y in ((f1j1, 300), (f1j2, 360), (f1j3, 425), (f1j4, 500)):
    _it['_x'] = 410; _it['_y'] = _y
f1j3['w'] = 1100
for _it, _y in ((f1j5, 500), (f1j6, 560), (f1j7, 620), (f1j8, 680)):
    _R(_it, _y, x=1040)

video('solve-pt-q03', 'solution', qid='pt-q03', slides=[
    S('Method 1 · The math way',
      L("Given, a is not zero, and b is not zero. a squared plus b squared, plus the bracket a minus b, squared, all over "
        "two a b, plus one. What is it equal to?", pt('stem', 'Given', 'hl', 9.0), voice='calm', pause=0.5),
      L("What does what is it equal to mean here? It means one of the choices is the same expression, written another "
        "way. It gives the same value for every a and b that we're allowed to use. [short pause] We'll solve it two ways, "
        "the math way, with algebra, and then by plugging in numbers."),
      L("The math way first. We simplify the expression until it looks like one of the choices. We have the bracket a minus "
        "b, squared, so let's use the formula from expressions. a minus b, squared, is a squared minus two a b plus b "
        "squared.", show(f1g1, 'a minus b, squared, is')),
      L("So the top is a squared plus b squared, plus a squared minus two a b plus b squared. Now collect the like terms. "
        "a squared plus a squared is two a squared. b squared plus b squared is two b squared. And the minus two a b "
        "stays.", show(f1g2, 'So the top is'), show(f1g2b, 'Now collect the like terms'))),
    SM('Method 1 · The math way', 'Split the fraction',
      L("A lot of students take out two as a common factor here, and then get a bit tangled. Instead, let's split the "
        "fraction into three fractions with the same bottom. Why is that allowed? Fractions with the same bottom are "
        "added by adding the tops, so we can also go back the other way.", show(f1g3, "let's split the fraction")),
      L('Why split it? The third fraction is minus two a b over two a b. The top and bottom have the same size, so that fraction is minus one. The expression also has plus one outside the fraction. Minus one plus one is zero, so those two parts cancel.', pt('f1g3: o', 'two a b over two a b')),
      L("Now reduce the other two. In two a squared over two a b, the twos cancel, and one a cancels, so we're left with a over b. In two b squared over two a b, the twos cancel, and one factor of b cancels too, so we get b over a.",
        show(f1g4, 'Now reduce the other two')),
      L("So the expression is a over b plus b over a, and choice number one is our answer.",
        mk('tick', 'choice 1', 'choice number one is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now the psychometric way. Our second super-method is plugging in numbers, and it's one of the most "
        "important methods for the exam. The question has two letters, a and b, and so do the choices."),
      L("If two expressions are really the same, they must give the same result for every a and b. So we pick one pair "
        "of numbers, and put it into the question and into each choice. A choice that gives a different result can't be "
        "the same expression.", show(f1h1, 'If two expressions are really the same')),
      L("Which numbers? Easy ones, as long as we keep the condition, a and b are not zero. Let's take a equal to one. For "
        "b, I could take two, three, any number. But I can also take one again. Nobody said a and b must be different, "
        "and one is the easiest number to calculate with.", show(f1h2, "Let's take a equal to one")),
      L("Let's put one in for both letters. One squared is one, and the other one squared is one too. One minus one is zero, and zero squared is zero. So the top is one plus one plus zero, which is two. The bottom is two times one times one, also two. Two over two is one. Then we add the one outside the fraction, and get two.", show(f1h3, 'One squared is one'), show(f1h3b, 'The bottom'), show(f1h3c, 'Two over two is one'))),
    SM('Method 2 · Plugging in numbers', 'Rule out three',
      L("Now the choices, with a and b equal to one. A choice that gives two could be the right one. A choice that gives "
        "anything else is out."),
      L("Choice number one says a over b, plus b over a. One over one is one, plus one over one, one. That's two. It "
        "fits, but we can't mark it yet, so we keep checking.", pt('choice 1', 'Choice number one says', 'hl', 3.0),
        show(f1h4, 'One over one is one')),
      L("Choice number two says a over two b, plus b over two a. One over two is a half, plus another half, that's one. "
        "One is not two, so choice number two is out.", pt('choice 2', 'Choice number two says', 'hl', 3.0),
        show(f1h5, 'One over two is a half'), mk('cross', 'choice 2', 'so choice number two is out')),
      L("Choice number three says a plus b, times a minus b, all over a b. One minus one is zero, and zero on top makes "
        "the whole fraction zero. Zero is not two, so choice number three is out.", pt('choice 3', 'Choice number three says', 'hl', 3.5),
        show(f1h6, 'One minus one is zero'), mk('cross', 'choice 3', 'Choice number three is out')),
      L("Choice number four says two times, a squared plus b squared. One plus one is two, and two times two is four, "
        "not two. Choice number four is out too.", pt('choice 4', 'Choice number four says', 'hl', 3.0),
        show(f1h7, 'One plus one is two'), mk('cross', 'choice 4', 'Choice number four is out')),
      L("Three choices are out, so we can mark choice number one.", mk('tick', 'choice 1', 'so we can mark choice number one')),
      L("This is a very important point. One matching result doesn't prove a choice is right. We need to rule out the other three. A wrong expression can match by chance. For example, a plus b also gives two when both letters are one. But it isn't always equal to our expression. If two choices remain, we try another easy pair. We check the question again, and only those two choices.", show(f1h8, 'We need to rule out'))),
    SM('Method 2 · Plugging in numbers', 'When do I plug in numbers?',
      L("So when do I plug in numbers? When there are letters in the question and letters in the choices, like here. Any "
        "allowed numbers will do, so we choose easy ones. It's a safety net for when the algebra gets tangled.",
        show(f1j1, 'So when do I plug in numbers')),
      L("One more example. Two to the power of x plus one, plus two to the power of x. What is it equal to? The choices "
        "are two to the power of two x plus one, three times two to the power of x, four to the power of x, and two to "
        "the power of x plus three.", show(f1j2, 'One more example'), show(f1j3, 'The choices are')),
      L("Let's take x equal to one, because small powers of two are easy. Two squared is four, plus two to the power of "
        "one, two. So the expression gives six.", show(f1j4, "Let's take x equal to one")),
      L("Now the choices with x equal to one. The right one must give six too. The first gives two cubed, eight, so it's out. The second gives three times "
        "two, six. It fits. The third gives four, and the fourth gives two to the power of four, sixteen. Both are out. "
        "Three are out, so the answer is three times two to the power of x. [pause] Okay. I'll see you in the next "
        "question.", show(f1j5, 'The first gives'), show(f1j6, 'The second gives'), show(f1j7, 'The third gives'), show(f1j8, 'the fourth gives'))),
])


# =================================================================================================== solve-pt-q04
# Hebrew: the cylinder formula (pi r^2 h, the formula sheet; base area x height); slide the edge inward: the diameter =
# the edge; r = a/2, h = a; the bracket trap (square only a -> choice 1); pi a^3 / 4; the third super-method, estimation
# (as with 200^2 in the root question): the cube is a^3, the cylinder inside is a bit less; pi = 3 is enough; 3/2, 3, 4
# times the cube -> out; the fourth is 3/4 of the cube; the exam gave three impossible choices on purpose (an advantage to
# whoever thinks). Course: edge 3a -> 27 a^3 / 4. Added: why base x height, why a part < the whole, "when", a circle in a
# square. Visual (V3): the question figure on the left; our colour copy: the front edge slides in to the diameter (teal),
# the radius (orange), the height (teal); then the cube tinted teal and the cylinder orange.
FIG_LEFT.update({'solve-pt-q04', 'solve-pt-q04-2'})
f1_e1 = [(315.0, 265.0), (321.5, 253.0), (318.8, 244.9), (309.7, 238.2), (294.8, 233.3), (275.1, 230.5), (260.0, 230.0),
         (243.8, 230.5), (218.7, 233.3), (194.0, 238.2), (171.4, 244.9), (152.4, 253.0), (138.4, 261.9), (130.3, 271.1),
         (128.5, 277.0), (129.6, 282.5), (136.6, 289.7), (149.7, 295.3), (167.9, 298.8), (190.0, 300.0), (214.5, 298.8),
         (239.7, 295.3), (263.9, 289.7), (285.4, 282.5), (302.9, 274.1), (315.0, 265.0)]
f1_top = [(x, y - 180) for x, y in f1_e1]


def f1_poly(pts, stroke=GINK, w=2.2, fill='none', op=1):
    return '<path d="M %s Z" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"/>' % (
        ' L '.join('%.1f %.1f' % p for p in pts), fill, op, stroke, w)


def f1_ln(x1, y1, x2, y2, c=GINK, w=2.5, dash=False):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" stroke-linecap="round"%s/>' % (
        x1, y1, x2, y2, c, w, ' stroke-dasharray="7 6"' if dash else '')


f1_cube = (f1_ln(100, 300, 170, 230, w=1.6, dash=True) + f1_ln(170, 230, 350, 230, w=1.6, dash=True) +
           f1_ln(170, 230, 170, 50, w=1.6, dash=True) + f1_poly(f1_e1) + f1_poly(f1_top) +
           f1_ln(321.6, 72.3, 321.6, 252.3, w=2.2) + f1_ln(128.4, 97.7, 128.4, 277.7, w=2.2) +
           ''.join(f1_ln(*s) for s in [(100, 120, 280, 120), (280, 120, 280, 300), (280, 300, 100, 300), (100, 300, 100, 120),
                                       (100, 120, 170, 50), (280, 120, 350, 50), (170, 50, 350, 50), (350, 50, 350, 230),
                                       (280, 300, 350, 230)]))


def f1_hull(pts):
    pts = sorted(set(pts))
    cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


f1k = f1_fig('f1k', [
    ('line', f1_cube),
    ('edge', f1_ln(100, 300, 280, 300, GTEAL, 6) + f1_t(190, 324, '3a', GTEAL, 30, italic=True)),
    ('slide', f1_ln(110, 292, 140, 270, GTEAL, 2, True) + f1_ln(270, 292, 300, 270, GTEAL, 2, True) +
              f1_ln(135, 265, 315, 265, GTEAL, 6) + '<circle cx="225" cy="265" r="4.5" fill="%s"/>' % GINK +
              f1_t(395, 265, 'd = 3a', GTEAL, 32, italic=True)),
    ('r', f1_ln(225, 265, 315, 265, GORANGE, 7) + f1_t(270, 248, 'r', GORANGE, 32, italic=True)),
    ('h', f1_ln(321.6, 72.3, 321.6, 252.3, GTEAL, 6) + f1_t(395, 150, 'h = 3a', GTEAL, 32, italic=True)),
], vb='80 35 370 300', w=380, title='The cylinder in the cube')
f1m1 = I('f1m1', '$V=\\pi r^2\\cdot h$', size=34)
f1m2 = I('f1m2', '$r=\\frac{3a}{2}$', size=32)
f1m3 = I('f1m3', '$h=3a$', size=32)
f1n1 = IH('f1n1', '$V=\\pi(\\frac{3a}{2})^2\\cdot3a$', size=34)
f1n2 = IH('f1n2', '$(\\frac{3a}{2})^2=\\frac{9a^2}{4}$', size=34)
f1n3 = IH('f1n3', '$V=\\pi\\cdot\\frac{9a^2}{4}\\cdot3a=\\frac{27\\pi a^3}{4}$', size=34)
f1kk = f1_fig('f1kk', [
    ('line', f1_cube),
    ('cube', f1_poly([(100, 300), (100, 120), (170, 50), (350, 50), (350, 230), (280, 300)], GTEAL, 3, GTEAL, 0.18) +
             f1_t(375, 80, 'cube: 27a³', GTEAL, 40, 'start')),
    ('cyl', f1_poly(f1_hull(f1_e1 + f1_top), GORANGE, 3, GORANGE, 0.3) + f1_t(375, 150, 'cylinder < 27a³', GORANGE, 40, 'start')),
    ('pi', f1_t(375, 220, 'π ≈ 3', GINK, 40, 'start')),
], vb='80 35 600 290', w=600, title='The cube and the cylinder inside it')
f1o4 = I('f1o4', '(1) $\\ \\frac{27\\cdot3}{2}=40\\frac12$ ✗', size=30)
f1o5 = I('f1o5', '(2) $\\ 27\\cdot3=81$ ✗', size=30)
f1o6 = I('f1o6', '(3) $\\ 36\\cdot3=108$ ✗', size=30)
f1o7 = I('f1o7', '(4) $\\ \\frac{27\\cdot3}{4}=\\frac{81}{4}$, about $\\frac34$ of $27$', size=28)
f1o8 = I('f1o8', 'When? The choices are far apart in size', size=28)
f1o9 = I('f1o9', 'A circle in a square, side $10$: $\\ $area $=?$', size=28)
f1o10 = I('f1o10', 'Square $=100\\ \\Rightarrow\\ $circle $<100$', size=28)
f1o11 = I('f1o11', '$25\\pi\\approx75$ ✓ $\\quad 50\\pi\\approx150$ ✗', size=28)

video('solve-pt-q04', 'solution', qid='pt-q04', slides=[
    SM('Method 1 · The math way', 'The radius and the height',
      L("A cylinder is inscribed in a cube whose edge is three a, see the figure. What is the volume of the cylinder?",
        pt('stem', 'A cylinder is inscribed', 'hl', 6.0), voice='calm', pause=0.5),
      L("Inscribed means the cylinder sits inside the cube, and touches its sides. They ask for the volume of the "
        "cylinder. [short pause] We'll solve it two ways, the math way, with the formula, and then with an estimate.",
        show(f1k['line'], 'Inscribed means')),
      L("The volume of a cylinder is pi r squared, times h. If you don't remember it, it's on the formula sheet. Pi r "
        "squared is the area of the round base, and h is the height. Why multiply? A cylinder is like a stack of equal "
        "circles, so it's the area of one circle, times how tall the stack is.", show(f1m1, 'The volume of a cylinder')),
      L('So we need the radius of the base. The edge of the cube is three a. The circular base touches two opposite sides of the square base of the cube. So its diameter goes across the full width of that square. The diameter is three a.',
        show(f1k['edge'], 'The edge of the cube is three a'), show(f1k['slide'], 'The circular base touches')),
      L("The diameter is two radii, so the radius is half of three a, which is three a over two. And the height of the "
        "cylinder is the height of the cube, three a.", show(f1k['r'], 'The diameter is two radii'), show(f1m2, 'so the radius is half'),
        show(f1k['h'], 'And the height of the'), show(f1m3, 'the height of the cube'))),
    SM('Method 1 · The math way', 'The bracket trap',
      L("Now into the formula. Pi, times the radius squared, times the height.", show(f1n1, 'Now into the formula')),
      L("Careful here. Many students write three a over two without brackets. Then they square the three a, but not the "
        "two. They get twenty-seven pi a cubed over two, which is choice number one. They mark it, and they're wrong.",
        mk('cross', 'choice 1', 'which is choice number one')),
      L("If the radius is a fraction, put it in brackets, and square both the top and the bottom. Three a, squared, is "
        "nine a squared, and two squared is four. So the radius squared is nine a squared over four.",
        show(f1n2, 'put it in brackets')),
      L("Now times the height, three a. Nine times three is twenty-seven, and a squared times a is a cubed. So the volume "
        "is twenty-seven pi a cubed over four, and choice number four is our answer.",
        show(f1n3, 'Now times the height'), mk('tick', 'choice 4', 'choice number four is our answer'))),
    SM('Method 2 · Estimation', 'Compare with the cube',
      L("[pause] Now the psychometric way, our third super-method, order-of-magnitude estimation. We used it already in "
        "the question with the root, when two hundred squared was forty thousand. Here we don't calculate the exact "
        "volume. We only ask how big it can be.", show(f1kk['line'], 'Now the psychometric way')),
      L('The volume of a cube is its edge length cubed. Three a times three a times three a. Three times three times three is twenty-seven, so the cube is twenty-seven a cubed.',
        show(f1kk['cube'], 'Three times three times three')),
      L("The cylinder is inside the cube, so its volume must be less than the cube's. How much less? We don't know, and "
        "we don't need to. A part can't be bigger than the whole.",
        show(f1kk['cyl'], 'The cylinder is inside the cube')),
      L("Every choice is a number times a to the power of three. The cube's volume is twenty-seven times that same positive quantity. So we can compare the numbers in front of it. Pi is more than three. We'll use three to estimate those numbers. This makes each choice smaller. If even that smaller amount is above twenty-seven, the real choice is too big too.",
        show(f1kk['pi'], "We'll use three to estimate")),
      L("Choice number one says twenty-seven pi over two, times a cubed. Twenty-seven times three is eighty-one, and over two, that's forty and a half. That's more "
        "than twenty-seven, so the cylinder would be bigger than the cube. That makes no sense, so choice number one is "
        "out.", pt('choice 1', 'Choice number one says', 'hl', 3.0), show(f1o4, 'Twenty-seven times three is eighty-one'),
        mk('cross', 'choice 1', 'so choice number one is out')),
      L("Choice number two says twenty-seven pi, times a cubed. Twenty-seven times three is eighty-one, three times the "
        "cube. A cylinder inside the cube can't be bigger than it, so choice number two is out.", pt('choice 2', 'Choice number two says', 'hl', 3.0),
        show(f1o5, 'Twenty-seven times three'), mk('cross', 'choice 2', 'Choice number two is out')),
      L("Choice number three says thirty-six pi, times a cubed. Thirty-six times three is a hundred eight, four times "
        "the cube, so it's too big as well. Choice number three is out too.", pt('choice 3', 'Choice number three says', 'hl', 3.0), show(f1o6, 'Thirty-six times three'), mk('cross', 'choice 3', 'Choice number three is out')),
      L("Three choices make no sense, so we can mark choice number four.",
        mk('tick', 'choice 4', 'so we can mark choice number four'))),
    SM('Method 2 · Estimation', 'Why these answers?',
      L("By the way, choice number four says twenty-seven pi over four, times a cubed. With pi as three, it's eighty-one over four, a bit more than twenty. That's about "
        "three quarters of twenty-seven, and that makes sense for a cylinder inside a cube.",
        show(f1o7, 'By the way, choice number four')),
      L("Look at the choices they gave. Not three quarters, two thirds and four fifths of the cube, which would be hard "
        "to tell apart. They gave three choices that are each bigger than the whole cube. That's the exam's way of giving "
        "an advantage to whoever thinks. If you calculate the long way, it takes time, and you might slip. If you "
        "estimate, the choices help you."),
      L("So when do I estimate? When the choices are far apart in size, and you can compare the answer with something you know, like the whole shape around it. Use a rough estimate, like three for pi here, to rule out what's too big or too small.",
        show(f1o8, 'So when do I estimate')),
      L("One more example. A circle is inside a square with side ten, and it touches all four sides. What's the area of "
        "the circle, if the choices are twenty-five pi, fifty pi, a hundred pi, and two hundred pi?",
        show(f1o9, 'One more example')),
      L("The square's area is ten times ten, a hundred, so the circle is less than a hundred. With pi as three, "
        "twenty-five pi is seventy-five, and fifty pi is a hundred fifty, more than the whole square. The other two are even bigger. Only twenty-five "
        "pi fits. [pause] Okay. I'll see you in the next question.",
        show(f1o10, "The square's area"), show(f1o11, 'With pi as three'))),
])


# =================================================================================================== solve-pt-q05
# Hebrew: fair dice = regular dice; the blue result depends on the red; a table: red 1 -> blue 2-6, 1/6 x 5/6 = 5/36 ...
# red 6 -> 0; "and" -> multiply, "or" -> add; 15/36 = 5/12; the long mathematical way; then the insight: what an
# insight is (unique to the question, not a method, rarer, practise and open your mind); 36 options: red higher, blue
# higher or a tie; 6 doubles; 30 split equally (the blue die is not better than the red) -> 15. Course: "at least as
# large" (ties count): 21/36 = 7/12. Taught on the spot (probability is not in the plan yet): good results over all
# results, 6 x 6 = 36 pairs. Added: the twin pair (why the split is equal), the trap (a half), when to look for an insight.
f1p1 = I('f1p1', 'Probability $=\\dfrac{\\text{good results}}{\\text{all results}}$', size=36)
f1p2 = I('f1p2', 'All pairs: $\\ 6\\cdot6=36$', size=36)


def f1_row(red, blues, n, y):
    return (f1_t(70, y, str(red), GRED, 30) + f1_t(330, y, blues, GINK, 28) + f1_t(600, y, str(n), GTEAL, 30) +
            f1_ln(10, y + 26, 660, y + 26, '#9fb0bd', 1.2) + f1_ln(140, y - 26, 140, y + 26, GINK, 1.5) +
            f1_ln(520, y - 26, 520, y + 26, GINK, 1.5))


f1q = f1_fig('f1q', [
    ('line', f1_t(70, 26, 'Red', GRED, 28) + f1_t(330, 26, 'Good blue', GINK, 28) + f1_t(600, 26, 'Pairs', GTEAL, 28) +
             f1_ln(10, 52, 660, 52, GINK, 2.5) + f1_ln(140, 4, 140, 52, GINK, 1.5) + f1_ln(520, 4, 520, 52, GINK, 1.5)),
    ('r1', f1_row(1, '1, 2, 3, 4, 5, 6', 6, 78)),
    ('r2', f1_row(2, '2, 3, 4, 5, 6', 5, 130)),
    ('r3', f1_row(3, '3, 4, 5, 6', 4, 182) + f1_row(4, '4, 5, 6', 3, 234) + f1_row(5, '5, 6', 2, 286) +
           f1_row(6, '6', 1, 338)),
    ('tot', f1_t(330, 395, 'Total: 6 + 5 + 4 + 3 + 2 + 1', GINK, 28) + f1_t(600, 395, '21', GTEAL, 32)),
], vb='0 0 670 420', w=700, title='Red and the good blue numbers')
f1p3 = I('f1p3', 'Red 1: $\\ \\dfrac16\\cdot\\dfrac66=\\dfrac{6}{36}$', size=36)
f1p4 = I('f1p4', '$\\dfrac{21}{36}=\\dfrac{7}{12}$', size=38)
f1r1 = I('f1r1', '$36$ = red higher + blue higher + ties', size=30)
f1r2 = I('f1r2', 'Ties: $\\ $1-1, 2-2, ..., 6-6', size=30)
f1r2b = I('f1r2b', '$36-6=30$', size=30)
f1r3 = I('f1r3', '(red 5, blue 2) $\\leftrightarrow$ (red 2, blue 5)', size=30)
f1r4 = I('f1r4', '$30\\div2=15$ $\\ $blue higher', size=30)
f1r5 = I('f1r5', '$\\dfrac{15+6}{36}=\\dfrac{21}{36}=\\dfrac{7}{12}$', size=36)

video('solve-pt-q05', 'solution', qid='pt-q05', slides=[
    S('Method 1 · The math way: a table',
      L("Two fair dice, one blue and one red, are tossed. What is the probability that the number obtained on the blue "
        "die will be at least as large as the number obtained on the red die?", pt('stem', 'Two fair dice', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("Fair dice is the exam's way of saying regular dice, where each of the six numbers is equally likely. And at "
        "least as large means bigger or equal, so a tie counts too. [short pause] We'll solve it two ways, with a table "
        "of all the cases, and then with an insight."),
      L("We haven't learned probability yet, so here's the little we need. A probability is the number of good results, "
        "out of all the results, when every result is equally likely. For example, the chance of a five on one die is "
        "one out of six, one sixth.", show(f1p1, 'A probability is the number')),
      L("With two dice, each of the six red numbers can come with each of the six blue numbers. That's six times six, "
        "thirty-six pairs, and they're all equally likely.", show(f1p2, "That's six times six"))),
    SM('Method 1 · The math way: a table', 'Count the good pairs',
      L("How do we find the good pairs? The blue number we need depends on the red one. So let's make a table, with a "
        "row for each red number.", show(f1q['line'], "So let's make a table")),
      L("If the red shows one, every blue number is good. One, two, three, four, five or six, even the one, because "
        "equal is allowed. That's six good pairs.", show(f1q['r1'], 'If the red shows one')),
      L("We can write that same count as a probability. The chance of a red one is one sixth. The blue die can show any of its six numbers, so its chance of being good here is six sixths. The dice are independent: the red result doesn't change the blue result. So for these two results together, we multiply. One sixth times six sixths is six thirty-sixths. That's the same six good pairs out of thirty-six.", show(f1p3, 'So for these two results together')),
      L("If the red shows two, the blue must be two, three, four, five or six. That's five good pairs. And so on. Red "
        "three gives four, red four gives three, red five gives two, and red six gives only one, a blue six.",
        show(f1q['r2'], 'If the red shows two'), show(f1q['r3'], 'And so on')),
      L("The red die can show one, or two, and so on. These cases can't happen together in one toss. So we add their good pairs. Six plus five is eleven. Four plus three is seven, and two plus one is three. Eleven plus seven plus three is twenty-one good pairs.", show(f1q['tot'], 'So we add their good pairs')),
      L("So the probability is twenty-one out of thirty-six. Both are divisible by three, so it's seven twelfths, and choice number four is our answer.", show(f1p4, 'So the probability is'), mk('tick', 'choice 4', 'choice number four is our answer')),
      L("That was the mathematical way. It's long, because we listed every case. And it's not trivial. Many students "
        "don't get there at all.")),
    S('Method 2 · Insight',
      L("[pause] So far, we've met super-methods. In this question there's also an insight. What's an insight? We notice something special in this question that makes the work easier. There's no fixed procedure for finding it. A different question may need a different idea. These questions are rarer, but they're on the exam, so we'll practice them."),
      L("Here's the insight. Every one of the thirty-six pairs is one of three kinds. The red is higher, the blue is "
        "higher, or it's a tie, a double.", show(f1r1, 'one of three kinds')),
      L("Two dice have six doubles. One and one, two and two, and so on up to six and six. In a double, neither die "
        "is higher. Take them away for now, and thirty pairs are left.", show(f1r2, 'Two dice have six doubles'), show(f1r2b, 'Take them away')),
      L("Those thirty split equally. Why? The dice are the same, except for the color. Every pair where the red is "
        "higher has a twin where the blue is higher. Red five and blue two, swap them, and it's red two and blue five.",
        show(f1r3, 'Red five and blue two')),
      L("So in fifteen pairs the red is higher, and in fifteen the blue is higher.", show(f1r4, 'So in fifteen pairs')),
      L("Now, at least as large means ties count too. Fifteen pairs where the blue is higher, plus the six doubles, "
        "that's twenty-one out of thirty-six. Seven twelfths again, choice number four.",
        show(f1r5, 'Fifteen pairs where'), mk('tick', 'choice 4', 'Seven twelfths again')),
      L("Careful here. Whoever says it's symmetric, so it's a half, forgets the ties, and marks choice number two. That's "
        "the trap.", mk('cross', 'choice 2', 'marks choice number two')),
      L("So when do we look for an insight? There's no fixed sign, but here's a hint. When the long way means listing "
        "many cases, stop for a moment, and ask if something in the question is symmetric or special. [pause] Okay. I'll "
        "see you in the next question.")),
])


# =================================================================================================== pt51-intro-wrap (lesson)
# Hebrew: the summary of the intro lesson: two ways (the school way, the shortcut); three super-methods that work in very
# many questions; insight questions (rarer, unique to each question); a lesson for each method, watch and practise; at
# home solve both ways, on the exam use whatever comes to mind. Added: the "when do I use which" signs, in the same words
# as the question videos.
f1w1 = I('f1w1', 'The math way: calculations, algebra', size=38)
f1w2 = I('f1w2', 'The shortcut: creative thinking that solves faster', size=38)
f1w3 = I('f1w3', 'Plugging in the answers', size=40)
f1w4 = I('f1w4', 'Plugging in numbers', size=40)
f1w5 = I('f1w5', 'Order-of-magnitude estimation', size=40)
f1w6 = I('f1w6', 'And insight questions: rarer, unique to each question', size=36)
f1w7 = I('f1w7', 'Choices end in different digits $\\to$ the last digit', size=32)
f1w8 = I('f1w8', 'Choices far apart in size $\\to$ estimate with round numbers', size=32)
f1w9 = I('f1w9', 'One number asked, numbers in the choices $\\to$ plug in the answers', size=32)
f1w10 = I('f1w10', 'Letters in the question and the choices $\\to$ plug in numbers', size=32)
f1w11 = I('f1w11', 'A very long way, many cases $\\to$ look for an insight', size=32)
f1w12 = I('f1w12', 'At home: practice both ways when useful', size=36)
f1w13 = I('f1w13', 'On the exam: whatever comes to mind first', size=36)

video('pt51-intro-wrap', 'lesson', slides=[
    S('Thinking vs Calculating',
      L("Let's sum up what we've learned in these first questions.")),
    S('Two ways to solve',
      L("We saw that exam questions can be solved by calculating, the way we know from school, with calculations, math "
        "and algebra.", show(f1w1, 'the way we know from school')),
      L("But the questions are special questions. Often there's a shortcut, some creative thinking that gets us to the "
        "answer faster.", show(f1w2, "Often there's a shortcut"))),
    S('Three super-methods',
      L("We met three super-methods that work in very many questions. Plugging in the answers, plugging in numbers, and "
        "order-of-magnitude estimation.", show(f1w3, 'Plugging in the answers'), show(f1w4, 'plugging in numbers'),
        show(f1w5, 'order-of-magnitude estimation')),
      L("And here and there, there are insight questions, with something unique to each question. They're rarer, but "
        "they exist too.", show(f1w6, 'insight questions'))),
    S('Which one, when?',
      L("Here are the signs we met. If the choices end in different digits, check the last digit. If the choices are far "
        "apart in size, estimate the size with round numbers.",
        show(f1w7, 'If the choices end in different digits'), show(f1w8, 'If the choices are far apart')),
      L("If they ask for one number and the choices are plain numbers, plug in the answers, starting with the most "
        "convenient one. If there are letters in the question and in the choices, plug in numbers, and rule out three.",
        show(f1w9, 'If they ask for one number'), show(f1w10, 'If there are letters')),
      L("And if the long way means listing many cases, stop and look for an insight.", show(f1w11, 'listing many cases'))),
    S('Solve both ways',
      L("From here, each method gets a lesson of its own. It's very important to watch them, and to practice as much as "
        "you can."),
      L("Remember, when you solve at home, practice the mathematical way and the psychometric way when both are useful. "
        "That gives you more options on the exam, without repeating work for no reason.", show(f1w12, 'when you solve at home')),
      L("You'll be able to use whichever is more convenient, whatever comes to mind first at that moment. [pause] Okay. "
        "I'll see you in the next video.", show(f1w13, 'whichever is more convenient'))),
])

# ------------------------------------------------------------------------------------------------ V4: the bubble corner
# camera lessons: text lines wrap before the face bubble (top right, x 1344-1594, y 6-256)
for _v in ('pt51-intro', 'pt51-intro-wrap'):
    for _sl in VIDEOS[_v]['slides']:
        for _ln in _sl['lines']:
            for _c in _ln['cues']:
                if _c[0] == 'show' and _c[1]['k'] == 't': _c[1]['w'] = 860

# ------------------------------------------------------------------------------------------------ placement / carry-over
for _it, _y, _x in [(f1k, 290, 1040), (f1m1, 610, 1040), (f1m2, 665, 1040), (f1m3, 725, 1040),
                    (f1n1, 340, 1040), (f1n2, 420, 1040), (f1n3, 500, 1040),
                    (f1kk, 330, 1040), (f1o4, 640, 1040), (f1o5, 700, 1040), (f1o6, 760, 1040),
                    (f1p3, 330, 1100), (f1p4, 440, 1100),
                    (f1o7, 340, 1040), (f1o8, 420, 1040), (f1o9, 490, 1040), (f1o10, 555, 1040), (f1o11, 620, 1040)]:
    _R(_it, _y, _x)

CARRY51.update({
    'solve-pt-q01': {1: ['(2), (3) out: they end in $6$']},
    'solve-pt-q03-2': {2: ['$a=b=1$: $\\ $the question gives $2$']},
})

# the long question videos in two parts (about 2-3.5 minutes each), split where the second method starts
CAMERA_SPLITS = globals().get('CAMERA_SPLITS', []) + [
    ('solve-pt-q01', 'The Root of 19,044', [(0, None), (2, "Let's continue with two more examples of these shortcuts.")]),
    ('solve-pt-q02', 'Moving Eggs', [(0, None), (1, "Let's continue with this question, now with psychometric thinking.")]),
    ('solve-pt-q03', 'An Expression with a and b', [(0, None), (2, "Let's continue with this question, now with psychometric thinking.")]),
    ('solve-pt-q04', 'A Cylinder in a Cube', [(0, None), (2, "Let's continue with this question, now with an estimate.")]),
]

# =================================================================================================================
# Topic 51, fragment f2 (TAG B, 2026-10-14): plugging in the answers (lesson + pt-q06..q09) and insight questions
# (lesson + pt-q20..q23). Hebrew: pt_src/seg2_plug_answers.txt, seg5_insights.txt. Every video is read on camera.
# NEW here (full first-time teaching, R29/R32): plugging in the answers (what, why, the order to try the choices in,
# "one fit is enough" vs "rule out three", the trap, the "when") and insight questions (look before you calculate:
# what, why, an extra example, the trap, the "when"). Percents (topic 23) are not taught yet: the little that is needed
# is said on the spot (half, a tenth). Inequalities (topic 12) are not taught: only "is this number less than that one".
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ pt51-plug-answers
# Hebrew seg2: the answers help us; once a choice fits, mark it (no need to rule out three); estimation crosses out
# choices that make no sense; start with the convenient, round choices (usually, not always, the right one); three out
# -> mark the fourth without checking. ADDED (teacher 2026-10-14): what / why in plain words, the "when" (choices are
# numbers + conditions to check; letters in the choices = plugging in numbers, next lesson), the order (in order ->
# start in the middle, one try tells bigger or smaller), one fit is enough here vs "rule out three" with our own numbers
# (R15 / R35), the trap (a choice must pass EVERY given), and one extra example: x(x + 3) = 40 with 2, 4, 5, 8.
# Visuals: typed rule lines built one by one; the extra example as hand-written rows, each try in its own row.
f2a1 = I('f2a1', 'One of the four choices is right', size=36)
f2a2 = I('f2a2', 'Put a choice in $\\ \\to\\ $ check every given', size=34)
f2a3 = I('f2a3', 'It fits every given $\\ \\to\\ $ it is the answer', size=34)
f2w1 = I('f2w1', 'Sign 1: $\\ $the choices are numbers', size=34)
f2w2 = I('f2w2', 'Sign 2: $\\ $conditions we can check', size=34)
f2w3 = I('f2w3', 'Letters $\\ \\to\\ $ plugging in numbers (next lesson)', size=30)
f2e1 = I('f2e1', '$x$ is positive. $\\quad x(x+3)=40\\quad x=?$', size=36)
f2e2 = I('f2e2', 'Choices: $\\quad 2,\\ \\ 4,\\ \\ 5,\\ \\ 8$', size=34)
f2e3 = IH('f2e3', '$x=4:\\ \\ 4+3=7$', size=34)
f2e3b = IH('f2e3b', '$4\\cdot7=28$', size=34)
f2e4 = I('f2e4', '28 is too small $\\ \\to\\ $ 4 and 2 are out', size=32)
f2e5 = IH('f2e5', '$x=5:\\ \\ 5+3=8$', size=34)
f2e5b = IH('f2e5b', '$5\\cdot8=40$', size=34)
f2e6 = I('f2e6', 'It fits $\\ \\to\\ x=5$', size=32)
f2r1 = I('f2r1', 'A choice fits every given $\\ \\to\\ $ mark it', size=34)
f2r2 = I('f2r2', 'Three choices are out $\\ \\to\\ $ the fourth is right', size=34)
f2r3 = I('f2r3', 'Careful: $\\ $every given, not only one', size=34)
f2s1 = I('f2s1', '1. Cross out choices that make no sense', size=34)
f2s2 = I('f2s2', '2. Start with a round, easy choice', size=34)
f2s3 = I('f2s3', '3. Increasing result $\\ \\to\\ $ try a middle choice', size=34)
video('pt51-plug-answers', 'lesson', slides=[
    S('Plugging In the Answers',
      L("Psychometric thinking, plugging in the answers. In the intro lesson we met our super-methods for the first time. "
        "Now let's go deeper into the first one, plugging in the answers.")),
    S('What we do',
      L("On the exam, every question has four choices, and exactly one of them is right. That's not only a rule of the "
        "exam. It's a tool we can use.", show(f2a1, 'exactly one of them is right')),
      L("Instead of solving the question the way we learned at school, we take a choice, put it into the question, and "
        "check if it fits everything they tell us.", show(f2a2, 'we take a choice')),
      L("Why does this work? The right answer is the number the question is talking about, so it must fit every given. A "
        "wrong choice breaks at least one of them. So we're not guessing here. We're checking.",
        show(f2a3, 'so it must fit every given'))),
    S('When do I use it?',
      L("So when do we use it? There are two signs. The first sign is in the choices. They're plain numbers, like four, "
        "twelve or seventy-five.", show(f2w1, 'The first sign')),
      L("The second sign is in the question. It gives us conditions we can check with a number. An equation, a story with "
        "numbers, or a condition like less than zero.", show(f2w2, 'The second sign')),
      L("With both signs, each check is short, and often much shorter than the math way.", pt('f2w2', 'each check is short')),
      L("And when the choices have letters, like two x, that's a different method, plugging in numbers. We'll learn it in "
        "the next lesson.", show(f2w3, 'when the choices have letters'))),
    S('A first example',
      L("Let's see it in a short example. x is a positive number, and x times, the bracket x plus three, equals forty. "
        "What is x? The choices are two, four, five and eight.", show(f2e1, 'x is a positive number'),
        show(f2e2, 'The choices are two')),
      L("Opening the bracket gives x squared plus three x equals forty, and we haven't learned to solve that yet. But the "
        "choices are numbers, and we have an equation to check. Both signs are here, so let's plug in the answers.",
        pt('f2e2', 'choices are numbers'), pt('f2e1', 'we have an equation to check')),
      L("Which choice do we try first? Here the choices go from smallest to biggest. For positive x, a bigger x gives a bigger product. So we can start with a middle choice. If its result is too small, smaller choices are out too. If it's too big, bigger choices are out too.", pt('f2e2', 'Here the choices go from smallest')),
      L("Let's try four. Four plus three is seven, and four times seven is twenty-eight. We need forty, so twenty-eight "
        "is too small.", show(f2e3, 'Four plus three is seven'), show(f2e3b, 'four times seven is twenty-eight')),
      L("Too small means we need a bigger x. Why? When x gets bigger, both x and x plus three get bigger, so their "
        "product gets bigger too. So four is out, and two is out as well, because two gives even less.",
        show(f2e4, 'So four is out')),
      L("Five and eight are left. Let's try the next one up, five. Five plus three is eight, and five times eight is "
        "forty, exactly the forty we need. It fits, so x is five.", show(f2e5, 'Five plus three is eight'), show(f2e5b, 'five times eight is'), show(f2e6, 'It fits, so x is five')),
      L("Do we need to check eight? No. Only one choice is right, and five fits the equation, so five is the answer.",
        pt('f2e6', 'Do we need to check eight?'))),
    S('Found one? Mark it',
      L("That's the main rule of this method. When we plug in the answers, the moment a choice fits every given, we mark "
        "it, and we don't check the others. Why? Because we tested the answer itself, and only one answer can be right.",
        show(f2r1, 'the moment a choice fits every given')),
      L("In the next lesson you'll see plugging in numbers, and there it's different. There we test a number we chose "
        "ourselves, so two choices can fit by chance, and we rule out three. Here we test the real answer, so one fit is "
        "enough.", pt('f2r1', 'Here we test the real answer')),
      L("The same rule works the other way too. If three choices are out, the fourth one is right, and we don't even need "
        "to check it.", show(f2r2, 'If three choices are out')),
      L("Just be careful with one thing. A choice must fit every given, not only one of them. A choice can pass one "
        "condition and fail another, and that's a common trap. We'll see it in the next question.",
        show(f2r3, 'A choice must fit every given'))),
    S('Where do I start?',
      L("So which choice do we try first? First, cross out choices that make no sense, without calculating at all. "
        "Sometimes a quick look at the size of a choice is enough.", show(f2s1, 'cross out choices that make no sense')),
      L('Then start with a convenient choice, such as a round number. It makes the arithmetic easier. We choose it for an easy check, not because it must be right.',
        show(f2s2, 'Then start with a convenient choice')),
      L('In a question like our example, a bigger trial number gives a bigger result. Then it helps to start in the middle of the ordered choices. One try can show whether we need a bigger or smaller number.', show(f2s3, 'Then it helps to start in the middle')),
      L("We'll use each of these in the next questions. [pause] Okay. I'll see you in the next video.",
        pt('f2s1', "We'll use each of these"))),
])

# ------------------------------------------------------------------------------------------------ pt-q06 (Hebrew Q2)
# Hebrew: an "easy" question at the start of the section with two inequalities - why is it here? Because of the
# answers. Plug 1 (out); 3 is positive like 1, so it gives a positive result too (no calculation, R35); -3 -> -4 here
# fits both -> mark it, no need to rule out three. NITE puts seemingly hard questions in to see who stops and thinks.
# Course numbers: x^2 < 25, 3x + 6 < 0, choices 1, -4, 3, -7 (real-exam order). ADDED: the trap at the step (-7 passes only the second
# given), "less than" explained as comparing two numbers. Visuals: one row per given per choice, ticks and crosses.
f2q6a1 = I('f2q6a1', '$x=1:\\quad 1^2=1,\\ \\ 1<25$', size=32)
f2q6a2 = I('f2q6a2', '$3\\cdot1+6=3+6=9$', size=32)
f2q6a3 = I('f2q6a3', '9 is not less than 0', size=32)
f2q6b = I('f2q6b', '$x=3:\\quad$ positive', size=32)
f2q6b2 = I('f2q6b2', '$3x+6$ positive, not less than 0', size=32)
f2q6c1 = I('f2q6c1', '$x=-4:\\quad (-4)\\cdot(-4)=16,\\ \\ 16<25$', size=32)
f2q6c2 = I('f2q6c2', '$3\\cdot(-4)+6=-12+6=-6,\\ \\ -6<0$', size=32)
f2q6d = I('f2q6d', '$x=-7:\\quad (-7)\\cdot(-7)=49,\\ $ not less than 25', size=32)
CARRY51['solve-pt-q06'] = {2: ['choices 1 and 3 are out']}
video('solve-pt-q06', 'solution', qid='pt-q06', slides=[
    S('Why is it here?',
      L("x is an integer. We're given two conditions. x squared is less than twenty-five, and three x plus six is less than zero. Which of the following could be the value of x?", pt('stem', 'x is an integer', 'hl', 8.0), voice='calm', pause=0.5),
      L("This question comes at the beginning of the section, where the easy questions usually are. But two conditions "
        "with less than, and one of them with x squared? We haven't learned to solve conditions like that yet. So why is "
        "it here?", pt('stem', 'two conditions')),
      L("Because we have the answers, and they help us. Look at the two signs. The choices are numbers, and each given is "
        "a condition we can check. So let's plug in the answers.", pt('choice 1', 'The choices are numbers')),
      L("Checking a condition is easy. We work out the left side, and ask if it's less than the number on the right. And "
        "a choice must pass both givens, not just one.", pt('stem: given', 'a choice must pass both givens'))),
    S('Plug in the answers',
      L("Let's start with choice number one, x is one. The first given says x squared is less than twenty-five. One squared is one, and one is less than "
        "twenty-five. Yes.", show(f2q6a1, 'one squared is one')),
      L("The second given says three x plus six is less than zero. Three times one is three, plus six is nine. Is nine less than zero? No. So choice number one "
        "is out.", show(f2q6a2, 'three times one is three'), show(f2q6a3, 'Is nine less than zero?'), mk('cross', 'choice 1', 'So choice number one is out')),
      L("Before we go on, look at choice number three, which is three. We just saw that a positive x gives a positive "
        "result here. Three times a positive number is positive, and adding six keeps it positive. So it can't be less "
        "than zero, and choice number three is out too, without calculating.", show(f2q6b, 'look at choice number three'), show(f2q6b2, 'Three times a positive number'),
        mk('cross', 'choice 3', 'choice number three is out too'))),
    S('Choice number two',
      L("Now choice number two, which is minus four. The first given: minus four times minus four is sixteen, because minus times "
        "minus is plus. Sixteen is less than twenty-five. Yes.", show(f2q6c1, 'The first given: minus four times')),
      L("The second given: three times minus four is minus twelve, plus six is minus six. Minus six is less than zero. "
        "Yes.", show(f2q6c2, 'three times minus four is minus twelve')),
      L("So minus four passes both givens. And that's exactly why we check both. Choice number four is minus seven, and it's "
        "the trap. It passes the second given, but minus seven times minus seven is forty-nine, and forty-nine is not less "
        "than twenty-five.", show(f2q6d, 'minus seven times minus seven'), mk('cross', 'choice 4', 'and forty-nine is not less')),
      L("Minus four fits every given, so it's a possible value of x. Among the four choices, only this one fits both conditions. Choice number two is our "
        "answer.", mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('A test of thinking',
      L("By the way, it's no accident that a question that looks this hard sits at the beginning of the section. The exam "
        "puts in questions like this from time to time."),
      L("They want to see who starts solving the conditions the long math way, and who stops for a moment and asks, "
        "what's the best way to solve this? The exam gives an advantage to students who stop and think. [pause] Okay. "
        "I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ pt-q07 (Hebrew Q13)
# Hebrew: we could build an equation (n, 105 - n) - but why? Estimate first: Nadav has more -> more than half -> two
# choices out; of the two left plug in the convenient, round one (60 -> here 50); it fits. Starting from convenient
# answers is very important: the round answers are often where the right answer is; NITE builds the questions to
# reward thinking, not calculating. Course numbers: 90 cards, 1/5, choices 40, 43, 48, 50.
# Visuals: the estimate line (more than 45), then the plug-in rows for 50.
f2q7a = I('f2q7a', 'Nadav has more than Amit $\\ \\to\\ $ more than half of 90, $\\ $more than 45', size=30)
f2q7b = I('f2q7b', '40 ✗ $\\quad$ 43 ✗ $\\quad$ (less than 45)', size=32)
f2q7c = IH('f2q7c', 'Nadav 50, $\\ $ Amit $90-50=40$', size=32)
f2q7d = I('f2q7d', '$50-40=10$', size=32)
f2q7e = I('f2q7e', '$\\frac15\\cdot50=10$ $\\ $ ✓', size=32)
video('solve-pt-q07', 'solution', qid='pt-q07', slides=[
    S('Cross out first',
      L("Nadav and Amit have ninety cards together. Nadav has more cards than Amit. The difference between their numbers "
        "of cards is one fifth of the number of cards Nadav has. How many cards does Nadav have?",
        pt('stem', 'Nadav and Amit have', 'hl', 9.0), voice='calm', pause=0.5),
      L("We could build an equation. Nadav has n cards, Amit has ninety minus n, and then we write the difference as one "
        "fifth of n. But why? We have the answers. The choices are numbers, and the story gives us conditions we can "
        "check.", pt('choice 1', 'The choices are numbers')),
      L("Before we plug anything in, let's cross out what makes no sense. Nadav has more cards than Amit. So Nadav has "
        "more than half of the ninety cards, which means more than forty-five.", show(f2q7a, 'So Nadav has more than half')),
      L("So forty and forty-three are out, because they're less than half. For example, if Nadav had forty, Amit would "
        "have fifty, and then Amit would have more. So choice numbers one and two are out.",
        show(f2q7b, 'So forty and forty-three are out'), mk('cross', 'choice 1', 'So choice numbers one'),
        mk('cross', 'choice 2', 'and two are out'))),
    S('Plug in the round one',
      L("Two choices are left, forty-eight and fifty. Which one do we plug in? Let's start with fifty, because it's a round number. Finding one fifth of fifty will be easy.", pt('choice 4', "Let's start with fifty")),
      L("Nadav has fifty cards. Together they have ninety, so Amit has ninety minus fifty, forty. And Nadav has more than "
        "Amit, fifty against forty, so that given is fine.", show(f2q7c, 'Nadav has fifty cards')),
      L("Now the last given, the difference has to be one fifth of Nadav's cards. The difference between them is fifty "
        "minus forty, ten. And one fifth of fifty is ten, because fifty divided by five is ten. Ten and ten, so fifty fits every given. Choice number four is our "
        "answer.", show(f2q7d, 'The difference between them'), show(f2q7e, 'And one fifth of fifty'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Starting with a convenient choice can save work. Here fifty made the check easy, and it fitted every given. In another question, the convenient choice may fail. Then we cross it out and try another. We always choose easy arithmetic first, and still check the given conditions. I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ pt-q08 (Hebrew Q18)
# Hebrew: two equations, two unknowns - few students manage; plug in from the convenient answers: 100 -> 290, 200 ->
# 330 (out); "a bit disappointed"; usually the round ones, not always - this question is here to teach what to do: go
# on as usual; the rounder of the two left (180) -> out; three out -> mark the fourth without checking; the shortcut:
# 300 is much closer to 290 than to 330, so the answer is the one near 100. Course numbers: 280 instead of 500, choices
# 50, 75, 140, 150: 50 -> 270, 150 -> 310, 140 -> 306, so 75. ADDED: the little percent needed (half, a tenth), and
# in the shortcut "between them" (the bigger-or-smaller idea of the lesson). Visuals: one row per try; a "So far" box
# on the next slide; the shortcut as two matching scales (paid / shirt), 280 placed and carried down to the shirt.
f2q8p = I('f2q8p', '50% off: $\\ $pay half', size=30)
f2q8p2 = I('f2q8p2', '10% off: $\\ $take off a tenth', size=30)
f2q8q = I('f2q8q', 'pants $=500-$ shirt', size=30)
f2q8r1 = IH('f2q8r1', 'shirt 50, $\\ $ pants $500-50=450$', size=30)
f2q8r1b = IH('f2q8r1b', 'pants: $\\ 450\\div2=225$', size=30)
f2q8r1c = IH('f2q8r1c', 'shirt: $\\ 50-5=45$', size=30)
f2q8r2 = IH('f2q8r2', '$225+45=270$', size=30)
f2q8r3 = IH('f2q8r3', 'shirt 150, $\\ $ pants $500-150=350$', size=30)
f2q8r3b = IH('f2q8r3b', 'pants: $\\ 350\\div2=175$', size=30)
f2q8r3c = IH('f2q8r3c', 'shirt: $\\ 150-15=135$', size=30)
f2q8r4 = IH('f2q8r4', '$175+135=310$', size=30)
f2q8r5 = IH('f2q8r5', 'shirt 140, $\\ $ pants $500-140=360$', size=30)
f2q8r5b = IH('f2q8r5b', 'pants: $\\ 360\\div2=180$', size=30)
f2q8r5c = IH('f2q8r5c', 'shirt: $\\ 140-14=126$', size=30)
f2q8r6 = IH('f2q8r6', '$180+126=306$', size=30)
f2q8r7 = I('f2q8r7', 'Three out $\\ \\to\\ $ 75', size=32)
f2X = lambda v, a, b, xa=120, xb=520: xa + (v - a) * (xb - xa) / float(b - a)
f2x280 = f2X(280, 270, 310)
f2q8g = PIN(GEO('f2q8g', [
    ('line', [('seg', 100, 90, 560, 90), ('seg', 100, 200, 560, 200),
              ('txt', 50, 90, 'paid', 'ink', 28), ('txt', 50, 200, 'shirt', 'ink', 28),
              ('seg', 120, 78, 120, 102), ('seg', 520, 78, 520, 102), ('txt', 120, 55, '270', 'ink', 32),
              ('txt', 520, 55, '310', 'ink', 32),
              ('seg', 120, 188, 120, 212), ('seg', 520, 188, 520, 212), ('txt', 120, 238, '50', 'ink', 32),
              ('txt', 520, 238, '150', 'ink', 32),
              ('seg', 120, 104, 120, 186, 'ink', 1.5, True), ('seg', 520, 104, 520, 186, 'ink', 1.5, True)]),
    ('mid', [('seg', 120, 90, 520, 90, 'teal', 7), ('seg', 120, 200, 520, 200, 'teal', 7)]),
    ('t280', [('dot', f2x280, 90), ('txt', f2x280, 55, '280', 'teal', 34),
              ('txt', 170, 132, '10', 'teal', 28), ('txt', 370, 132, '30', 'orange', 28),
              ('seg', 122, 112, 218, 112, 'teal', 4), ('seg', 222, 112, 518, 112, 'orange', 4)]),
    ('down', [('seg', f2x280, 150, f2x280, 194, 'teal', 3, True),
              ('dot', f2x280, 200), ('txt', f2x280, 238, '?', 'teal', 34)]),
    ('ans', [('seg', f2X(140, 50, 150), 186, f2X(140, 50, 150), 214, 'red', 4), ('txt', f2X(140, 50, 150) - 8, 172, '140', 'red', 30),
             ('txt', f2x280, 276, '75', 'teal', 34)]),
], vb='10 25 590 270', w=860, col=0, title='What he paid and the shirt price'))
CARRY51['solve-pt-q08'] = {2: ['shirt 50 $\\to$ 270'], 3: ['shirt 50 $\\to$ 270', 'shirt 150 $\\to$ 310']}
for _part in f2q8g.values():
    _part['h'] = int(round(_part['h'] * 620 / _part['w'])); _part['w'] = 620
    _part['_x'] = 400; _part['_y'] = 350
f2delta1 = IH('f2delta1', 'Original: shirt $+10$, pants $-10$', size=28, col=1)
f2delta2 = IH('f2delta2', 'Paid: $+9-5=+4$', size=30, col=1)
_R(f2delta1, 400); _R(f2delta2, 455)
video('solve-pt-q08', 'solution', qid='pt-q08', slides=[
    S('Round answers first',
      L("Kobi bought a pair of pants at a fifty percent discount, and a shirt at a ten percent discount. He paid two "
        "hundred eighty shekels in total, instead of five hundred shekels. What was the price of the shirt before the "
        "discount?", pt('stem', 'Kobi bought a pair of pants', 'hl', 10.0), voice='calm', pause=0.5),
      L("The math way would use two unknowns and two equations. But we can also test the answers. The choices are numbers, "
        "and the story gives conditions we can check. We'll try a shirt price from the choices. Then we'll check "
        "whether the discounted prices add up to two hundred eighty.", pt('choice 1', 'The choices are numbers')),
      L("We haven't learned percents yet, so here's all we need. Fifty percent off means half the price is taken off, so "
        "he pays half. Ten percent off means a tenth of the price is taken off.", show(f2q8p, 'Fifty percent off means'), show(f2q8p2, 'Ten percent off means')),
      L("And one more thing from the story. Before the discounts, the pants and the shirt cost five hundred together. So "
        "once we know the shirt, the pants are five hundred minus the shirt.", show(f2q8q, 'the pants are five hundred minus'))),
    S('Try fifty',
      L("Which choice first? The round, convenient ones, fifty and a hundred fifty. Let's try fifty. If the shirt cost "
        "fifty, the pants cost five hundred minus fifty, four hundred fifty.", pt('choice 1', "Let's try fifty"),
        show(f2q8r1, 'the pants cost five hundred minus fifty')),
      L("The pants are half price, so he paid half of four hundred fifty, two hundred twenty-five. On the shirt, a tenth "
        "of fifty is five, so he paid fifty minus five, forty-five.", show(f2q8r1b, 'he paid half of four hundred fifty'), show(f2q8r1c, 'a tenth of fifty is five')),
      L("Together, two hundred twenty-five plus forty-five is two hundred seventy. But he paid two hundred eighty, so "
        "choice number one is out.", show(f2q8r2, 'Together, two hundred twenty-five'),
        mk('cross', 'choice 1', 'so choice number one is out'))),
    S('The next round one',
      L("Fifty didn't fit, so we cross it out and try another easy choice. Let's try a hundred fifty. Then the pants cost five hundred minus a hundred fifty, three hundred fifty, before the discount.",
        pt('choice 4', "Let's try a hundred fifty"), show(f2q8r3, 'Then the pants cost five hundred minus')),
      L("Half of three hundred fifty is a hundred seventy-five. A tenth of a hundred fifty is fifteen, so the shirt cost "
        "him a hundred fifty minus fifteen, a hundred thirty-five.", show(f2q8r3b, 'Half of three hundred fifty'), show(f2q8r3c, 'A tenth of a hundred fifty')),
      L("Together, a hundred seventy-five plus a hundred thirty-five is three hundred ten. That's not two hundred eighty "
        "either, so choice number four is out too.", show(f2q8r4, 'Together, a hundred seventy-five'),
        mk('cross', 'choice 4', 'so choice number four is out too'))),
    S('When round fails',
      L("Both convenient choices failed. That's fine: round numbers make checking easier, but they don't have to be right. We've ruled out two choices. Now we check one of the two that remain."),
      L("Two choices are left, seventy-five and a hundred forty. We try the rounder one, a hundred forty. Then the pants "
        "are five hundred minus a hundred forty, three hundred sixty.", pt('choice 3', 'We try the rounder one'), show(f2q8r5, 'Then the pants')),
      L("Half of three hundred sixty is a hundred eighty. A tenth of a hundred forty is fourteen, so the shirt cost him a "
        "hundred forty minus fourteen, a hundred twenty-six. Together, a hundred eighty plus a hundred twenty-six is three "
        "hundred six. Not two hundred eighty, so choice number three is out.",
        show(f2q8r5b, 'Half of three hundred sixty'), show(f2q8r5c, 'A tenth of a hundred forty'), show(f2q8r6, 'Together, a hundred eighty'), mk('cross', 'choice 3', 'so choice number three is out')),
      L("Now only choice number two is left. Can I mark it without checking? Yes. Three choices are out, so the one that's "
        "left must be right. Choice number two is our answer, seventy-five.", show(f2q8r7, "so the one that's"),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('A shortcut by estimating',
      L("Let's go back to the moment we had tried the two round answers. We could have saved a step there with an "
        "estimate.", show(f2q8g['line'], "Let's go back to the moment")),
      L("A shirt of fifty gave two hundred seventy, and a shirt of a hundred fifty gave three hundred ten. We need two "
        "hundred eighty, which is between them. So the shirt is between fifty and a hundred fifty.",
        show(f2q8g['mid'], 'We need two hundred eighty')),
      L("Why does closeness help here? The original total stays five hundred. If the shirt's original price goes up by ten, the pants' original price goes down by ten. The shirt's discount takes away a tenth of the extra ten, which is one. So we pay nine more for the shirt. The pants are half price, so we save only five there. Nine more minus five saved is four more paid. Each extra ten changes the paid total by the same four. Two hundred eighty is ten above two hundred seventy. It's thirty below three hundred ten. So the needed shirt price is closer to fifty than to a hundred fifty.",
        show(f2delta1, "the pants' original price goes down by ten"), show(f2delta2, 'four more paid'),
        show(f2q8g['t280'], "It's thirty below three hundred ten"), show(f2q8g['down'], 'So the needed shirt price is closer')),
      L("Of the two choices left, seventy-five is close to fifty, and a hundred forty is right next to a hundred fifty. So "
        "the answer is seventy-five.", show(f2q8g['ans'], 'seventy-five is close to fifty')),
      L("If you saw that, great. If not, no problem. We plugged in one more answer and crossed it out. [pause] Okay. "
        "I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ pt-q09 (Hebrew Q18b)
# Hebrew: the math way is possible (an equation, move stamps); plug in the answers instead; no round or convenient
# choice -> start with the first; 9 -> both 9, after 12 and 6, 12 = 2 x 6 -> the answer; "the end of the section, should
# be very hard, simple with the answers"; then the lesson's summary (kept here, at the end of the method's block).
# Course numbers: 4 stamps, choices 12, 8, 16, 4 (real-exam order) -> 12. Visuals: now / after rows, then the summary lines.
f2q9a = IH('f2q9a', 'now: $\\ $ Miri 12, $\\ $ Ron 12', size=32)
f2q9b = IH('f2q9b', 'after: $\\ $ Miri $12+4=16$', size=32)
f2q9b2 = IH('f2q9b2', 'Ron $12-4=8$', size=32)
f2q9c = I('f2q9c', '$16=2\\cdot8$ $\\quad$ ✓', size=32)
f2q9s1 = I('f2q9s1', 'Numbers in the choices + conditions to check', size=30)
f2q9s2 = I('f2q9s2', 'Cross out $\\ \\to\\ $ round first $\\ \\to\\ $ in order: the middle', size=30)
f2q9s3 = I('f2q9s3', 'One choice fits every given $\\ \\to\\ $ mark it', size=30)
f2q9s4 = I('f2q9s4', 'Three out $\\ \\to\\ $ the fourth, no check', size=30)
video('solve-pt-q09', 'solution', qid='pt-q09', slides=[
    S('No round answer',
      L("If Ron gives Miri four stamps, Miri will have two times as many stamps as Ron will have. Right now, the two of "
        "them have the same number of stamps. How many stamps does Miri have now?",
        pt('stem', 'If Ron gives Miri four stamps', 'hl', 8.0), voice='calm', pause=0.5),
      L("We could work the math way. Build an equation, give Ron a letter, move stamps to Miri, and so on. But let's do "
        "what we did in this whole lesson, and plug in the answers. The choices are numbers, and the story gives "
        "conditions we can check.", pt('choice 1', 'The choices are numbers')),
      L("Which choice first? None of them is rounder or more convenient than the others. They're all small, easy "
        "numbers. So I'll simply start with the first choice, twelve.", pt('choice 1', 'start with the first choice'))),
    S('Plug in twelve',
      L("They ask how many stamps Miri has now. So let's say Miri has twelve stamps now. How many does Ron have? The "
        "story says that right now they have the same number, so Ron also has twelve.",
        show(f2q9a, "let's say Miri has twelve")),
      L("Now Ron gives Miri four stamps. Miri gets four more, twelve plus four, sixteen. Ron has four fewer, twelve minus "
        "four, eight.", show(f2q9b, 'Miri gets four more'), show(f2q9b2, 'Ron has four fewer')),
      L("Is Miri's number twice Ron's? Two times eight is sixteen. Yes. So twelve fits every given, and it's the "
        "answer. Choice number one is our answer.", show(f2q9c, 'Two times eight is sixteen'),
        mk('tick', 'choice 1', 'Choice number one is our answer')),
      L("Look at that. This question comes toward the end of the section, so it's supposed to be a very hard one. And once "
        "we plugged in the answers, it was really simple.")),
    S('What we learned',
      L("Let's sum up plugging in the answers. When the choices are numbers, and the question gives conditions we can "
        "check, we can put each choice into the question and check it.", show(f2q9s1, "Let's sum up")),
      L('First we cross out choices that make no sense. Then we start with a round, convenient choice. And when a bigger trial number gives a bigger result, a middle choice can help us rule out more of the ordered choices.', show(f2q9s2, 'First we cross out')),
      L("The moment a choice fits every given, we mark it, and we don't need to check the rest. And if three choices are "
        "out, the fourth is right, even without checking. [pause] Okay. I'll see you in the next video.",
        show(f2q9s3, 'The moment a choice fits'), show(f2q9s4, 'if three choices are out'))),
])

# ------------------------------------------------------------------------------------------------ pt51-insights
# Hebrew seg5: the questions are special and reward creative thinking; three super-methods work in a large part of the
# questions; here and there "insight questions": the creative idea is specific to the question, what works in one does
# not work in another; prepare by practicing as many as possible, to open the mind. ADDED (teacher 2026-10-14): the
# idea before calculating (stop and look: what is special here?) with its why (the numbers are chosen on purpose), one
# extra example ((48 + 73 + 96) - (46 + 71 + 94): partners differ by 2, three pairs -> 6), the trap (calculating right
# away) and the "when" (a long or messy calculation, numbers that look chosen on purpose: repeats, double / half,
# shared parts, something that stays the same). Visuals: typed lines; the example's partners joined in the same row.
f2i1 = I('f2i1', 'Plugging in the answers', size=32)
f2i1b = I('f2i1b', 'Plugging in numbers', size=32)
f2i1c = I('f2i1c', 'Estimating', size=32)
f2i2 = I('f2i2', 'Insight question: $\\ $one idea, just for it', size=32)
f2i3 = I('f2i3', 'Before calculating: $\\ $what is special here?', size=34)
f2i4 = I('f2i4', 'numbers that repeat', size=30)
f2i4b = I('f2i4b', 'double or half', size=30)
f2i4c = I('f2i4c', 'parts that two things share', size=30)
f2i4d = I('f2i4d', 'something that stays the same', size=30)
f2i5 = IH('f2i5', '$(48+73+96)-(46+71+94)=?$', size=34)
f2i6a = IH('f2i6a', '$48+73=121$', size=32)
f2i6b = IH('f2i6b', '$121+96=217$', size=32)
f2i6c = IH('f2i6c', '$46+71=117$', size=32)
f2i6d = IH('f2i6d', '$117+94=211$', size=32)
f2i6 = IH('f2i6', '$217-211=6$', size=32)
f2i7 = I('f2i7', 'partners: $\\ 48,46\\quad 73,71\\quad 96,94$', size=32)
f2i8a = I('f2i8a', 'each pair: $\\ $smaller by 2', size=32)
f2i8 = IH('f2i8', '$2+2+2=6$', size=32)
f2i9 = I('f2i9', 'When? $\\ $a long, messy calculation', size=30)
f2i9b = I('f2i9b', 'and numbers that look chosen on purpose', size=30)
video('pt51-insights', 'lesson', slides=[
    S('Insight Questions',
      L("Now let's look at insight questions in psychometric thinking.")),
    S('Special questions',
      L("By now we already know that the questions on this exam are special. They give an advantage to students who "
        "think in a more creative way."),
      L("In the previous lessons we learned three super-methods, plugging in the answers, plugging in numbers, and "
        "estimating. They help us solve a large part of the exam questions faster and more easily.",
        show(f2i1, 'plugging in the answers, plugging'), show(f2i1b, 'plugging in numbers, and'), show(f2i1c, 'and estimating'))),
    S('What is an insight?',
      L("Here and there, we also meet insight questions. We need to notice something useful in that particular question. There isn't one fixed set of steps for finding it. A different question may need a different idea.",
        show(f2i2, 'we also meet insight questions')),
      L("These questions are rarer. Most questions fit our super-methods. But they're on the exam, so we'll practice "
        "them too.")),
    S('Look before you calculate',
      L("So how do we find the idea? Before you start calculating, stop for a few seconds and look at the question. Ask "
        "yourself, what's special here?", show(f2i3, 'Before you start calculating')),
      L("Look for numbers that repeat, for something that's exactly double or half of something else, for parts that two "
        "things share, or for something in the story that doesn't change.", show(f2i4, 'Look for numbers that repeat'), show(f2i4b, 'for something that\'s exactly double'), show(f2i4c, 'for parts that two'), show(f2i4d, 'or for something in the story')),
      L("Why does it work? Because the people who write the exam choose the numbers on purpose. When a question looks "
        "long, there's often a short way hidden in its numbers, and the exam rewards the student who spots it.",
        pt('f2i4', 'choose the numbers on purpose'))),
    S('An example',
      L("Here's a short example. Forty-eight plus seventy-three plus ninety-six, minus, the bracket forty-six plus "
        "seventy-one plus ninety-four. What is it?", show(f2i5, "Here's a short example")),
      L("One way is to calculate. Forty-eight plus seventy-three is a hundred twenty-one, plus ninety-six is two hundred "
        "seventeen. Forty-six plus seventy-one is a hundred seventeen, plus ninety-four is two hundred eleven. Two hundred "
        "seventeen minus two hundred eleven is six. It works, but it takes time, and it's easy to slip.",
        show(f2i6a, 'Forty-eight plus seventy-three is'), show(f2i6b, 'plus ninety-six is two hundred seventeen'), show(f2i6c, 'Forty-six plus seventy-one'), show(f2i6d, 'plus ninety-four is'), show(f2i6, 'Two hundred seventeen minus')),
      L("Now let's look before we calculate. Every number in the first bracket has a partner in the second bracket "
        "that's a little smaller. Forty-eight and forty-six, seventy-three and seventy-one, ninety-six and ninety-four.",
        show(f2i7, 'Forty-eight and forty-six')),
      L("Each partner is smaller by two. There are three pairs, so the whole difference is two plus two plus two, six. "
        "No big sums at all.", show(f2i8a, 'Each partner is smaller by two'), show(f2i8, 'so the whole difference')),
      L("Why is that allowed? When we take away a sum, we take away each of its numbers. So we can match each number "
        "with its partner, in any order we like.", pt('f2i7', 'Why is that allowed?'))),
    S('When do I use it?',
      L("So when do we look for an insight? When the calculation looks long or messy, and the numbers look chosen on "
        "purpose. When they repeat, when one is double another, or when two things share parts. That's the sign to stop "
        "and look before you calculate.", show(f2i9, 'When the calculation looks long'), show(f2i9b, 'and the numbers look chosen')),
      L("And the trap is the opposite. Starting to calculate right away, before you even looked at the question.",
        pt('f2i9', 'And the trap is the opposite')),
      L("How do we get ready for these questions? Simply by practicing as many of them as we can. That opens your mind, "
        "and it will help you on the exam. Let's see a few sample questions like this. [pause] Okay. I'll see you in the "
        "next video.")),
])

# ------------------------------------------------------------------------------------------------ pt-q20 (Hebrew Q6)
# Hebrew: calculate (common denominator 12 -> here 30: 11/30 over 22/30 -> 11/22 = 1/2); then the insight: the bottom
# is exactly twice the top, part by part (a banana and 2 bananas, an apple and 2 apples); NITE wrote 2/4 (here 2/6),
# not 1/2 (1/3), on purpose; "I love this question" - even in easy calculations the exam rewards creative thinking.
# ADDED: why (2/5 + 2/6 = 2 x (1/5 + 1/6)), the trap at the step (the flipped result, 2, is choice 2).
f2q20a = IH('f2q20a', '$\\frac15+\\frac16=\\frac{6}{30}+\\frac{5}{30}$', size=36)
f2q20a2 = IH('f2q20a2', '$=\\frac{11}{30}$', size=36)
f2q20b = IH('f2q20b', '$\\frac25+\\frac26=\\frac{12}{30}+\\frac{10}{30}$', size=36)
f2q20b2 = IH('f2q20b2', '$=\\frac{22}{30}$', size=36)
f2q20c = IH('f2q20c', '$\\frac{11}{30}\\cdot\\frac{30}{22}$', size=36)
f2q20c2 = IH('f2q20c2', '$=\\frac{11}{22}=\\frac12$', size=36)
f2q20d = I('f2q20d', '$\\frac25+\\frac26=2\\cdot\\left(\\frac15+\\frac16\\right)$', size=38)
f2q20e = I('f2q20e', '$\\frac{1\\text{ banana}\\ +\\ 1\\text{ apple}}{2\\text{ bananas}\\ +\\ 2\\text{ apples}}=\\frac12$', size=44)
video('solve-pt-q20', 'solution', qid='pt-q20', slides=[
    S('Calculate',
      L("One fifth plus one sixth, divided by two fifths plus two sixths. What is it?",
        pt('stem', 'One fifth plus one sixth', 'hl', 5.0), voice='calm', pause=0.5),
      L("We'll solve it two ways. First the math way, we calculate, and then we'll see the insight.", pt('stem', 'First we calculate')),
      L("The top has two fractions to add, and to add fractions we need the same bottom. Five and six have a common denominator of thirty. One fifth is six thirtieths, "
        "and one sixth is five thirtieths. Together, eleven thirtieths.", show(f2q20a, 'One fifth is six thirtieths'), show(f2q20a2, 'Together, eleven thirtieths')),
      L("The bottom has two fractions too, with the same common denominator, thirty. Two fifths is twelve thirtieths, and "
        "two sixths is ten thirtieths. Together, twenty-two thirtieths.", show(f2q20b, 'Two fifths is twelve thirtieths'), show(f2q20b2, 'Together, twenty-two thirtieths')),
      L("Now we divide. Dividing by a fraction means multiplying by its reciprocal, with the top and bottom swapped. So it's eleven over thirty, times thirty over twenty-two. The thirties cancel, and we're left with eleven over twenty-two, which is one half.",
        show(f2q20c, 'So it\'s eleven over thirty'), show(f2q20c2, 'The thirties cancel')),
      L("Careful to keep the top on top. If you flip it, you get two, and two is waiting as choice number two. Choice "
        "number one is our answer.", mk('cross', 'choice 2', 'two is waiting as choice number two'),
        mk('tick', 'choice 1', 'Choice number one is our answer')), sb='Method 1 · The math way'),
    S('The insight',
      L("Now the insight. Some students look at this and see right away that it's one half. How? Look at the bottom. Two "
        "fifths is exactly twice one fifth, and two sixths is exactly twice one sixth.", pt('stem', 'Look at the bottom')),
      L("So every part of the bottom is twice its partner on the top, and the whole bottom is twice the whole top. Why? "
        "Two fifths plus two sixths is two times, the bracket one fifth plus one sixth. And a nonzero number over twice itself is "
        "always one half.", show(f2q20d, 'Two fifths plus two sixths is two times')),
      L("Maybe it's easier to see it like this. Call one fifth a banana, and one sixth an apple. The top has one banana and one apple. The bottom has two bananas and two apples: twice that same total. So the top is half of the bottom, and the fraction is one half.", show(f2q20e, 'The top has one banana')),
      L("By the way, notice that the exam wrote two sixths, and not one third. They're the same number, but two sixths "
        "shows us that it's double one sixth. They wanted us to see it.", pt('stem', 'the exam wrote two sixths')),
      L("Honestly, I love this question. Even in an easy calculation, the exam gives an advantage to whoever stops and "
        "looks first. [pause] Okay. I'll see you in the next question."), sb='Method 2 · Insight'),
])

# ------------------------------------------------------------------------------------------------ pt-q21 (Hebrew Q19)
# Hebrew: solvable in seconds, without calculating; first a simpler example (100 shekels, a 10% plan: all of it ->
# 10%, half of it -> 5 shekels = 5% of the 100: "invested half, earned half"); back: half at 4% -> 2%, the other half
# 2%-8% -> 1%-4%; min 2 + 1, max 2 + 4 -> 3%-6%; if you calculate: ratios (2% is half of 4%, 8% is twice); found the
# minimum? stop and check the choices, only one fits. Course numbers: 60,000, 8%, 4%-16% -> 4%, 2%-8% -> 6%-12%.
# ADDED: what a percent means (said on the spot, topic 23 comes later); the trap at the step (choice 1 = 12%-24%, the
# halves forgotten). Visuals: two bars for the simple example (all of it / half of it); Roni's 60,000 as one bar cut
# into two halves, each half tinted with what it earns out of the total, then the sum.
f2q21g1 = PIN(GEO('f2q21g1', [
    ('line', [('path', [(60, 20), (580, 20), (580, 76), (60, 76), (60, 20)], 'ink', 3), ('txt', 320, 48, '100 shekels', 'ink', 30)]),
    ('all', [('tint', [(60, 20), (580, 20), (580, 76), (60, 76)], 'teal'),
             ('txt', 320, 108, 'all of it at 10% → earn 10 = 10%', 'teal', 30)]),
    ('half', [('path', [(60, 145), (580, 145), (580, 201), (60, 201), (60, 145)], 'ink', 3), ('seg', 320, 145, 320, 201),
              ('tint', [(60, 145), (320, 145), (320, 201), (60, 201)], 'teal'), ('txt', 190, 173, '50 invested', 'ink', 28),
              ('txt', 450, 173, '50 not invested', 'ink', 28)]),
    ('earn', [('txt', 320, 234, 'half of it at 10% → earn 5 = 5%', 'orange', 30)]),
], vb='40 5 560 250', w=820, col=0, title='One hundred shekels, all of it or half of it'))
f2q21g2 = PIN(GEO('f2q21g2', [
    ('line', [('path', [(60, 50), (580, 50), (580, 110), (60, 110), (60, 50)], 'ink', 3), ('seg', 320, 50, 320, 110),
              ('txt', 320, 24, '60,000', 'ink', 30), ('txt', 190, 80, '30,000', 'ink', 30), ('txt', 450, 80, '30,000', 'ink', 30)]),
    ('left', [('tint', [(60, 50), (320, 50), (320, 110), (60, 110)], 'teal'), ('txt', 190, 140, '8%', 'teal', 30),
              ('txt', 190, 175, '→ 4% of all', 'teal', 30)]),
    ('right', [('tint', [(320, 50), (580, 50), (580, 110), (320, 110)], 'orange'), ('txt', 450, 140, '4% to 16%', 'orange', 30),
               ('txt', 450, 175, '→ 2% to 8% of all', 'orange', 30)]),
    ('least', [('txt', 320, 222, 'least: 4% + 2% = 6%', 'ink', 30)]),
    ('most', [('txt', 320, 260, 'most: 4% + 8% = 12%', 'ink', 30)]),
], vb='40 0 560 280', w=730, col=0, title="Roni's money in two halves"))
f2q21a = IH('f2q21a', '$1\\%$ of 30,000 $=300$', size=30)
f2q21a2 = IH('f2q21a2', '$8\\%=8\\cdot300=2{,}400$', size=30)
f2q21b = IH('f2q21b', '$4\\%=2{,}400\\div2=1{,}200$', size=30)
f2q21b2 = IH('f2q21b2', '$16\\%=2{,}400\\cdot2=4{,}800$', size=30)
video('solve-pt-q21', 'solution', qid='pt-q21', slides=[
    S('A simpler example',
      L("Roni has sixty thousand shekels. He invests half of the money in a savings plan that gives a profit of eight "
        "percent a year. He invests the rest of the money in a fund that gives a profit of between four percent and "
        "sixteen percent a year. Roni's profit in the coming year will be at least what part of the total amount he "
        "invested, and at most what part?", pt('stem', 'Roni has sixty thousand shekels', 'hl', 14.0), voice='calm', pause=0.5),
      L("We can solve this without calculating the profit in shekels. Remember, eight percent means eight for every "
        "hundred invested. Here, only half the total money earns that rate.", pt('stem', 'Here, only half the total money')),
      L("Before the idea behind the question, let's take a simpler example. Say I have a hundred shekels, and a plan that "
        "gives ten percent. If I invest all hundred shekels, I earn ten shekels, which is ten percent of my money.",
        show(f2q21g1['line'], 'Say I have a hundred shekels'), show(f2q21g1['all'], 'If I invest all hundred')),
      L("But if I invest only half, fifty shekels, I earn ten percent of fifty, which is five shekels. And out of my "
        "hundred shekels, five shekels is five percent.", show(f2q21g1['half'], 'But if I invest only half'),
        show(f2q21g1['earn'], 'I earn ten percent of fifty')),
      L("The plan still pays ten percent on the money I put in. But I invested only half of all my money, so the profit is five percent of the whole amount. That's the whole idea.",
        pt('f2q21g1_line', 'I invested half the money'))),
    S('Half the money, half the percent',
      L("Back to Roni. Half of his money is in the plan with eight percent. If all of his money were there, he'd earn "
        "eight percent. But it's only half the money, so out of the total, he earns half of eight, four percent.",
        show(f2q21g2['line'], 'Back to Roni'), show(f2q21g2['left'], 'so out of the total, he earns half of eight')),
      L("The other half is in the fund, with four to sixteen percent. Again, it's only half the money, so out of the "
        "total, he earns half of that. Half of four is two, and half of sixteen is eight. So between two and eight percent.",
        show(f2q21g2['right'], 'Half of four is two')),
      L("Now we add the two profits, both measured as percentages of all his money. Careful: don't add the plans' full rates, eight plus four or eight plus sixteen. That would give twelve and twenty-four, choice number one. Each rate applies to only half his money. So we add their contributions to the whole, after halving each rate.",
        mk('cross', 'choice 1', 'choice number one')),
      L('The plan always contributes four percent of the total money, so only the fund changes. At the least, four plus two, six percent. At the most, four plus eight, twelve percent. So between six and twelve percent. Choice number three is our answer. We solved it just by understanding, without calculating the profit in shekels.',
        show(f2q21g2['least'], 'At the least, four plus two'), show(f2q21g2['most'], 'At the most, four plus eight'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('If you calculate',
      L("By the way, if you still choose to calculate, there are shortcuts here too. Say you worked out eight percent of "
        "thirty thousand, the half in the plan. One percent of thirty thousand is three hundred, so eight percent is two thousand four hundred.",
        show(f2q21a, 'One percent of thirty thousand'), show(f2q21a2, 'so eight percent is')),
      L("You don't need to start over for four percent and sixteen percent. Four is half of eight, so it's half of two "
        "thousand four hundred, one thousand two hundred. And sixteen is twice eight, so it's four thousand eight hundred.",
        show(f2q21b, 'Four is half of eight'), show(f2q21b2, 'And sixteen is twice eight')),
      L("And one more shortcut. Say you found the minimum first, six percent. Stop and look at the choices. Only one "
        "choice starts with six percent, choice number three, so you don't need the maximum at all. Remember, the answers "
        "help us. [pause] Okay. I'll see you in the next question.", pt('choice 3', 'Only one choice starts with six'))),
])

# ------------------------------------------------------------------------------------------------ pt-q22 (Hebrew Q16)
# Hebrew: the long way (each perimeter, the slanted side by Pythagoras twice, subtract); the fast way: DE is in both,
# cancel it; AB and DC are both x, cancel; left x - y and x, minus y; a line parallel to AB cuts AD into two pieces, the
# one equal to EC cancels; left 2(x - y). ADDED: the "when" as a reusable takeaway (a difference of two shapes -> cancel
# the shared parts first). Visuals (V3): the question figure on the left; our colour copy on the right, the two shapes
# tinted, DE teal (in both), AB and DC orange (equal), what is left traced, the dashed parallel line from E, the piece
# equal to EC red (cancels), the two x - y pieces teal.
FIG_LEFT.add('solve-pt-q22')
f2A, f2D, f2B, f2C, f2E, f2F = (150, 40), (430, 40), (150, 320), (430, 320), (338, 320), (338, 40)
f2q22base = [('seg', *f2A, *f2D), ('seg', *f2D, *f2C), ('seg', *f2C, *f2B), ('seg', *f2B, *f2A), ('seg', *f2D, *f2E),
              ('txt', 132, 24, 'A', 'ink', 24, True), ('txt', 448, 24, 'D', 'ink', 24, True), ('txt', 132, 338, 'B', 'ink', 24, True),
              ('txt', 448, 338, 'C', 'ink', 24, True), ('txt', 338, 344, 'E', 'ink', 24, True),
              ('txt', 124, 180, 'x', 'ink', 24, True), ('txt', 384, 302, 'y', 'ink', 22, True)]
f2q22shapes = [('tint', [f2A, f2B, f2E, f2D], 'teal'), ('tint', [f2E, f2C, f2D], 'orange')]
f2q22g = PIN(GEO('f2q22g', [('line', f2q22base), ('shapes', f2q22shapes)], vb='95 0 400 360', w=400,
                 title='Square ABCD with the segment DE'))
f2q22h = PIN(GEO('f2q22h', [
    ('line', f2q22base + f2q22shapes),
    ('de', [('seg', *f2D, *f2E, 'teal', 7), ('txt', 245, 190, 'D E: in both', 'teal', 24)]),
    ('abdc', [('seg', *f2A, *f2B, 'orange', 7), ('seg', *f2D, *f2C, 'orange', 7), ('txt', 470, 180, 'x', 'orange', 24, True)]),
    ('rest', [('seg', *f2B, *f2E, 'teal', 7), ('seg', *f2A, *f2D, 'teal', 7), ('seg', *f2E, *f2C, 'red', 7)]),
    ('par', [('seg', *f2E, *f2F, 'teal', 3, True)]),
    ('rpiece', [('seg', *f2F, *f2D, 'red', 7), ('txt', 384, 22, 'y', 'red', 24, True)]),
    ('lpiece', [('txt', 244, 22, 'x − y', 'teal', 24, True), ('txt', 244, 344, 'x − y', 'teal', 24, True)]),
], vb='95 0 400 360', w=400, title='Square ABCD with the segment DE'))
f2q22a = I('f2q22a', '$(x-y)+(x-y)=2(x-y)$', size=30, col=1)
video('solve-pt-q22', 'solution', qid='pt-q22', slides=[
    SM('The long way', 'The long way',
      L("In the figure, A B C D is a square. The side of the square is x centimeters, and E C is y centimeters. What is "
        "the difference between the perimeter of the quadrilateral A B E D, and the perimeter of the triangle E C D?",
        pt('stem', 'In the figure', 'hl', 9.0), voice='calm', pause=0.5),
      L("So we need the quadrilateral's perimeter minus the triangle's perimeter. By the way, the quadrilateral is a "
        "trapezoid, because A D and B E are parallel.", show(f2q22g['line'], 'So we need'), show(f2q22g['shapes'], 'minus the triangle')),
      L("The long way is to find each perimeter and subtract. The quadrilateral has x, x, and B E, which is x minus y, "
        "and then the slanted side D E, which we'd find with Pythagoras. The triangle has y, x, and D E again. That's a "
        "lot of work, so let's look for a faster way.", pt('f2q22g_line', 'The long way'))),
    SM('Cancel what is shared', 'Cancel what is shared',
      L("We need the quadrilateral minus the triangle. But wait, look at D E. It's a side of both shapes. In the "
        "difference, it's added once and taken away once, so it cancels. We don't need it at all, and that means no "
        "Pythagoras.", show(f2q22h['line'], 'We need the quadrilateral'), show(f2q22h['de'], 'look at D E')),
      L("Now A B and D C. Both are sides of the square, so both are x. A B is in the quadrilateral, and D C is in the "
        "triangle, so they cancel too.", show(f2q22h['abdc'], 'Now A B and D C')),
      L("What's left? From the quadrilateral, B E and A D. From the triangle, E C. So we need B E plus A D, minus E C.",
        show(f2q22h['rest'], "What's left?")),
      L("Let's draw a line from E straight up, parallel to A B. It divides the square into two rectangles. The right piece of A D is opposite E C, so those lengths are equal. Both are y. In our subtraction, that plus y and minus E C cancel. The left piece of A D is opposite B E. Those lengths are equal too, and each is x minus y.",
        show(f2q22h['par'], "Let's draw a line from E"), show(f2q22h['rpiece'], 'The right piece of A D'), show(f2q22h['lpiece'], 'The left piece of A D')),
      L("So we're left with B E and the left piece, x minus y twice. That's two times, the bracket x minus y. Choice "
        "number two is our answer.", show(f2q22a, "So we're left with"), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("When a question asks for the difference between two perimeters, look for the parts they share, and cancel them before you calculate anything. [pause] Okay. I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ pt-q23 (Hebrew Q20)
# Hebrew: first 30 games, 20% won: 10% is 3, 20% is 6 -> lost 24; from game 31 only wins - until when? until wins =
# losses (50% = exactly 50:50); so 24 wins; "solved in seconds, only an insight"; then the lesson's summary (every
# question had something different; super-methods + insight questions; practice as many as you can). Course numbers:
# 40 games, 30% -> 12 wins, 28 losses -> 28. ADDED: the trap at the step (20 = half of 40, the season went on).
# Visuals: two bars (wins teal, losses orange), then the wins bar grows to the length of the losses bar.
f2q23a = I('f2q23a', '10% of 40 $=4$', size=30)
f2q23a2 = I('f2q23a2', '30% of 40 $=3\\cdot4=12$ wins', size=30)
f2q23b = I('f2q23b', 'Fifty percent = half', size=30)
f2q23b2 = I('f2q23b2', 'wins = losses', size=30)
f2W = 15.0
f2q23layers = [
    ('line', [('txt', 60, 60, 'wins', 'ink', 30), ('txt', 60, 140, 'losses', 'ink', 30),
              ('tint', [(120, 40), (120 + 12 * f2W, 40), (120 + 12 * f2W, 80), (120, 80)], 'teal'),
              ('path', [(120, 40), (120 + 12 * f2W, 40), (120 + 12 * f2W, 80), (120, 80), (120, 40)], 'teal', 3),
              ('txt', 120 + 6 * f2W, 60, '12', 'ink', 30),
              ('tint', [(120, 120), (120 + 28 * f2W, 120), (120 + 28 * f2W, 160), (120, 160)], 'orange'),
              ('path', [(120, 120), (120 + 28 * f2W, 120), (120 + 28 * f2W, 160), (120, 160), (120, 120)], 'orange', 3),
              ('txt', 120 + 14 * f2W, 140, '28', 'ink', 30)]),
    ('grow', [('seg', 120 + 12 * f2W + 8, 60, 120 + 17 * f2W, 60, 'teal', 4), ('path', [(120 + 17 * f2W - 12, 50), (120 + 17 * f2W, 60), (120 + 17 * f2W - 12, 70)], 'teal', 4),
              ('txt', 120 + 17 * f2W + 75, 60, 'only wins', 'teal', 28)]),
    ('eq', [('tint', [(120 + 12 * f2W, 40), (120 + 28 * f2W, 40), (120 + 28 * f2W, 80), (120 + 12 * f2W, 80)], 'teal'),
            ('seg', 120 + 12 * f2W, 40, 120 + 28 * f2W, 40, 'teal', 3, True), ('seg', 120 + 12 * f2W, 80, 120 + 28 * f2W, 80, 'teal', 3, True),
            ('seg', 120 + 28 * f2W, 40, 120 + 28 * f2W, 80, 'teal', 3, True),('seg', 120 + 28 * f2W, 20, 120 + 28 * f2W, 180, 'teal', 2, True), ('txt', 120 + 28 * f2W + 62, 100, '28 = 28', 'teal', 28)]),
]
f2q23g = PIN(GEO('f2q23g', f2q23layers[:1], vb='0 10 720 190', w=1000, col=0, title='Wins and losses'))
f2q23h = PIN(GEO('f2q23h', f2q23layers, vb='0 10 720 190', w=1000, col=0, title='Wins and losses'))
video('solve-pt-q23', 'solution', qid='pt-q23', slides=[
    S('The first forty games',
      L("In a certain season, a basketball team won thirty percent of its first forty games. From the forty-first game "
        "on, the team won all of its games until the end of the season. Because of that, its overall winning percentage "
        "rose to fifty percent. How many games in total did the team win in this season?",
        pt('stem', 'In a certain season', 'hl', 12.0), voice='calm', pause=0.5),
      L("At first it won thirty percent of its games, and in the end, fifty percent. Let's see what that means in games.",
        pt('stem', 'At first it won thirty percent')),
      L("We haven't learned percents yet, so here's what we need. Ten percent means a tenth. A tenth of forty games is "
        "four games. Thirty percent is three tenths. So thirty percent is three times four, twelve games.", show(f2q23a, 'A tenth of forty games'), show(f2q23a2, 'So thirty percent is')),
      L("So it won twelve of the first forty games, and it lost all the rest. Forty minus twelve is twenty-eight losses.",
        show(f2q23g['line'], 'Forty minus twelve'))),
    S('Win until it is even',
      L("From game forty-one, the team only wins. No more losses at all. So the number of losses stays twenty-eight until "
        "the end of the season.", show(f2q23h['line'], 'From game forty-one'), show(f2q23h['grow'], 'the team only wins')),
      L("Until when does it keep winning? Fifty percent is half. So in the end, exactly half of the games are wins, and "
        "half are losses. That means the number of wins equals the number of losses.",
        show(f2q23b, 'Fifty percent is half'), show(f2q23b2, 'That means the number of wins')),
      L("So it wins the next game, and the next one, and the next, until it has as many wins as losses. The losses are "
        "twenty-eight, so in the end it has twenty-eight wins.", show(f2q23h['eq'], 'until it has as many wins as losses')),
      L("Careful with choice number three, twenty. That's half of forty, but the season didn't stop at forty games. It "
        "went on until the wins caught up with the losses. Choice number four is our answer.",
        mk('cross', 'choice 3', 'Careful with choice number three'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("This question comes at the end of the section, and it's solved in seconds, with almost no calculation. The key to understanding it is that the number of losses stays the same. It won twelve and lost twenty-eight, so it needs to reach twenty-eight wins.")),
    S('Keep practicing',
      L("So in these questions we saw insights, and in every question the idea was different. A bottom that's twice the "
        "top, half the money, sides that two shapes share, and losses that stay the same."),
      L("We have our super-methods, and they help in most questions. Here and there, there's an insight question too. To "
        "be ready for them, solve as many as you can, to open your mind. [pause] Okay. I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ placement (q22 right column)
_R(f2q22g, 330, 1040)
_R(f2q22h, 330, 1040)
_R(f2q22a, 720, 1040)

# =================================================================================================================
# Topic-51 fragment f3 (TAG C, 2026-10-14): the lesson "Plugging In Numbers" (camera, in 3 parts) and its sample
# questions pt-q10 ... pt-q15 and pt-q24 (Hebrew: pt_src/seg3_plug_numbers.txt).
#
# Hebrew moves kept (each at the question that shows it):
#   q10  an expression with a letter + number choices -> one particular case; the smallest allowed value (x = 4)
#   q11  a letter in the choices; a value that fits the figure (not 120); rule out 3, the 4th without checking;
#        "ends in 5, not round"; plugging in flattens the difficulty (the same question with numbers is an early one)
#   q12  the factorial taught on the spot; a = 1 leaves two -> a second plug-in, the ruled-out ones are not rechecked;
#        8! passes 48 at 8 x 7 -> stop
#   q13  1 makes every choice equal -> choose values that give different results (x = 2, y = 1)
#   q14  percent: 100 at the whole, not at x (40 out of 140 is not nice)
#   q15  a ratio: the numbers don't matter; "who chose the 1? I did, so I may change it" (1 -> 3)
#   lesson (her summary): when (expression with a letter, letters in the choices, ratios), the rules (rule out 3, a
#        second plug-in, different results, convenient numbers), "the most important technique".
# Added (the course's R15 words, the clarity style, the teacher's "a bit more explanation" 2026-10-14):
#   why it works (right for every number -> right for ours), an explicit "when do I use it", 0 and 1 make choices tie,
#   different letters -> different numbers, the tie-breaker number, "a safety net", keep the conditions (x = 0 in q10
#   breaks the root; alpha = 40 in q11 breaks the triangle), "not always" = one counterexample / "always" needs more
#   (q24 uses it), case 4 (more letters than equations, pt-q24), the algebra as a second method where it is short.
#   Lesson examples are new numbers (not the course's questions); one more example than usual (4 worked examples
#   in parts 1-2, plus the ratio, case-4 and counterexample examples in part 3).
# Extremes: the Hebrew of this lesson has none; the edge value is used here (x = 4 in q10, "the edge of what is
# allowed" in the lesson) and the min / max idea is taught with pt-q21 (insights).
# =================================================================================================================
FIG_LEFT.update({'solve-pt-q11'})


# ------------------------------------------------------------------------------------------------ pt51-plug-numbers (lesson)
# Visuals: typed / hand-written board lines built at her words; every choice checked in its own row with ✓ / ✗.
f3w1 = I('f3w1', 'Letters $\\to$ numbers that we choose', size=36)
f3w2 = I('f3w2', 'A hard question $\\to$ an easy one, and faster', size=34)
f3s1 = I('f3s1', 'Sign 1: $\\ $an expression with a letter $\\ =\\ ?$ $\\quad$ choices: numbers', size=32)
f3s2 = I('f3s2', 'Sign 2: $\\ $letters in the choices $\\ (x+4,\\ \\ x^2y,\\ \\dots)$', size=32)
f3s3 = I('f3s3', 'Not here: $\\ 3x+5=20$ $\\ \\to\\ $ $x$ has one value $\\to$ plug in the answers', size=30)
f3e1 = I('f3e1', 'Example: $\\ (x+2)^2-x(x+4)=\\ ?$ $\\quad$ choices: numbers', size=34)
f3e1a = IH('f3e1a', '$x=1$: $\\ (1+2)^2-1\\cdot(1+4)$', size=34)
f3e1a0 = IH('f3e1a0', '$1+2=3$, $\\ 3^2=9$', size=32)
f3e1a1 = IH('f3e1a1', '$1+4=5$, $\\ 1\\cdot5=5$', size=32)
f3e1a2 = IH('f3e1a2', '$=9-5=4$', size=34)
f3e1b = IH('f3e1b', '$x=3$: $\\ (3+2)^2-3\\cdot(3+4)$', size=34)
f3e1b0 = IH('f3e1b0', '$3+2=5$, $\\ 5^2=25$', size=32)
f3e1b1 = IH('f3e1b1', '$3+4=7$, $\\ 3\\cdot7=21$', size=32)
f3e1b2 = IH('f3e1b2', '$=25-21=4$', size=34)
f3e1c = IH('f3e1c', '$(x+2)^2=x^2+4x+4$', size=30, col=1)
f3e1d = IH('f3e1d', '$x(x+4)=x^2+4x$', size=30, col=1)
f3e1e = IH('f3e1e', '$x^2+4x+4-(x^2+4x)=4$', size=30, col=1)
f3e2 = I('f3e2', '$(x+3)^2-(x+1)^2=\\ ?$', size=36)
f3e2c = I('f3e2c', 'Choices: $\\ 4x+8,\\quad 2x+8,\\quad 4x+10,\\quad 8$', size=32)
f3e2x0 = IH('f3e2x0', '$x=2$: $\\ (2+3)^2-(2+1)^2$', size=34)
f3e2x = IH('f3e2x', '$=25-9=16$', size=34)
f3e2r1 = IH('f3e2r1', '$4\\cdot2+8=16$ ✓', size=32, col=1)
f3e2r2 = IH('f3e2r2', '$2\\cdot2+8=12$ ✗', size=32, col=1)
f3e2r3 = IH('f3e2r3', '$4\\cdot2+10=18$ ✗', size=32, col=1)
f3e2r4 = IH('f3e2r4', '$8\\ne16$ ✗', size=32, col=1)
f3e2n = I('f3e2n', 'Three out $\\to$ $\\ 4x+8$ $\\ $ (no check needed)', size=30, col=1)
f3net = I('f3net', 'Plugging in = a safety net', size=34, col=1)
# part 2: choosing the number
f3k1 = I('f3k1', '$x\\ge4$ $\\ \\to\\ $ $x=4,\\ 5,\\ 6,\\ \\dots$ $\\quad$ not $2$', size=32)
f3k2 = I('f3k2', '$a$ a positive integer $\\to$ $1,\\ 2,\\ 3,\\ \\dots$ $\\quad$ not $0$, not $\\frac12$', size=32)
f3k3 = I('f3k3', '$\\frac{5}{x}$ $\\ \\to\\ $ $x\\ne0$', size=32)
f3k4 = I('f3k4', 'A figure: $\\ $fit the given conditions, not its appearance', size=32)
f3k5 = I('f3k5', 'Often easiest: $\\ $the edge, $\\ x=4$', size=32)
# part 2 (2026-10-21 external fixes, the teacher's decision rule): restrictions -> an easy allowed number -> what it rules
# out -> another easy number only if more than one choice is left (only those). Zero is out only where a restriction
# forbids it; different letters may share a number. Hand-written rows are pen-safe (", no" instead of a cross).
f3t9 = I('f3t9', 'Zero is often the fastest, if it is allowed', size=30)
f3t0 = I('f3t0', '$x(x+1)=\\ ?$', size=36)
f3t1 = I('f3t1', 'Choices: $\\ x^2+x,\\quad 3x,\\quad x^2+1,\\quad 4x$', size=32)
f3t2 = IH('f3t2', 'No restriction. $\\ x=0$: $\\ 0\\cdot1=0$', size=34)
f3t3a = IH('f3t3a', '$x^2+x=0$', size=32)
f3t3a2 = IH('f3t3a2', '$3x=0$', size=32)
f3t3b = IH('f3t3b', '$x^2+1=1$, no', size=32)
f3t3b2 = IH('f3t3b2', '$4x=0$', size=32)
f3t3c = I('f3t3c', 'Three left $\\to$ again, only those three', size=30)
f3t4 = IH('f3t4', '$x=1$: $\\ 1\\cdot2=2$', size=34, col=1)
f3t5 = IH('f3t5', '$x^2+x=1+1=2$', size=32, col=1)
f3t6 = IH('f3t6', '$3x=3$, no', size=32, col=1)
f3t6b = IH('f3t6b', '$4x=4$, no', size=32, col=1)
f3t7 = I('f3t7', 'One left $\\to$ no third try', size=30, col=1)
f3t8 = I('f3t8', 'Restrictions $\\to$ easy number $\\to$ what is out?', size=28)
f3t8b = I('f3t8b', 'Another number only if needed', size=28)
f3z0 = I('f3z0', '$\\frac{x^2\\cdot x^3}{x}=\\ ?$ $\\quad$ choices: $\\ x^4,\\ \\ x^5,\\ \\ x^6,\\ \\ x^3$', size=32)
f3z2 = I('f3z2', 'Restriction: $\\ x$ is at the bottom $\\to$ $x\\ne0$', size=32)
f3z1 = IH('f3z1', '$x=1$: $\\ 1$, $\\ $and the choices $1,\\ 1,\\ 1,\\ 1$', size=32)
f3z3 = IH('f3z3', '$x=2$: $\\ \\frac{2^2\\cdot2^3}{2}=\\frac{4\\cdot8}{2}$', size=32)
f3z3b = IH('f3z3b', '$=\\frac{32}{2}=16$', size=32)
f3z3c = IH('f3z3c', '(1) $\\ 2^4=16$', size=32, col=1)
f3z3d = IH('f3z3d', '(2) $\\ 2^5=32$, no', size=32, col=1)
f3z3e = IH('f3z3e', '(3) $\\ 2^6=64$, no', size=32, col=1)
f3z3f = IH('f3z3f', '(4) $\\ 2^3=8$, no', size=32, col=1)
f3z4 = I('f3z4', 'Zero or one make the choices tie? $\\ \\to$ the next easy allowed number', size=30)
f3d0 = I('f3d0', '$(a+3)(b+3)-3a-3b-ab=\\ ?$', size=34)
f3d0c = I('f3d0c', 'Choices: $\\ 0,\\quad 3,\\quad 6,\\quad 9$', size=32)
f3d1 = IH('f3d1', '$a=b=0$: $\\ 3\\cdot3=9$', size=34)
f3d1c = IH('f3d1c', '$3a,\\ 3b,\\ ab$ are $0$ $\\to$ $9$', size=34)
f3d1b = I('f3d1b', 'Number choices $\\to$ only one is $9$: $\\ $one try', size=30)
f3d2 = I('f3d2', 'Letter choices: $\\ a^2b$ $\\ $ and $\\ ab^2$', size=32)
f3d3 = IH('f3d3', '$a=b=1$: $\\ 1$ and $1$, a tie', size=32)
f3d4 = IH('f3d4', '$a=1,\\ b=2$: $\\ a^2b=1\\cdot2=2$', size=32)
f3d4c = IH('f3d4c', '$ab^2=1\\cdot4=4$', size=32)
f3d5 = I('f3d5', 'The same number is allowed; $\\ $change one only for a tie', size=30)
# part 3: two more cases, and "always"
f3r0 = I('f3r0', '$1:2\\ =\\ 2:4\\ =\\ 10:20$', size=36)
f3r1 = I('f3r1', 'Half of a number $+$ a third of it $=$ what part of it?', size=32)
f3r2a = IH('f3r2a', 'Number $=6$: $\\ 6\\div2=3$', size=34)
f3r2c = IH('f3r2c', '$6\\div3=2$', size=34)
f3r2 = IH('f3r2', '$3+2=5$', size=34)
f3r2b = I('f3r2b', '$5$ out of $6$ $\\to\\ \\frac56$ of the number', size=34)
f3q0 = I('f3q0', '$4x+6y=18$ $\\qquad 6x+9y=\\ ?$', size=36)
f3q1 = IH('f3q1', '$x=0$: $\\ 6y=18$', size=34)
f3q1b = IH('f3q1b', '$y=18\\div6=3$', size=34)
f3q2 = IH('f3q2', '$6\\cdot0+9\\cdot3=27$', size=34)
f3q3 = I('f3q3', 'Choose one letter, solve for the other', size=32)
f3q4 = I('f3q4', '$6x+9y=1\\frac12\\,(4x+6y)=1\\frac12\\cdot18=27$', size=32)
f3v0 = I('f3v0', '$n$ friends share $P$; $\\ k$ more join. $\\ $Each pays how much less?', size=30)
f3v1 = I('f3v1', '$k=0$: $\\ $nobody joins $\\to$ $0$ less', size=34)
f3v2 = I('f3v2', 'A choice that isn\'t $0$ at $k=0$ $\\to$ out', size=32)
f3v3 = I('f3v3', 'Two left $\\to$ a tie-breaker, $\\ k=1$', size=32)
f3n0 = I('f3n0', 'Is $\\ a^2+b^2=(a+b)^2\\ $ always?', size=34)
f3n1 = IH('f3n1', '$a=1,\\ b=2$: $\\ a^2+b^2=1+4=5$', size=34)
f3n1b = IH('f3n1b', '$(a+b)^2=3^2=9$', size=34)
f3n1c = IH('f3n1c', '$5\\ne9$', size=34)
f3n2 = I('f3n2', 'Not always: $\\ $one counterexample is enough', size=32)
f3n3 = I('f3n3', 'Always: $\\ $examples don\'t prove it $\\to$ rule out the other three', size=30)
# "cannot be determined" / "none of the above" (2026-10-21 external fixes): no number rules it out; the last other
# choice is broken by a different KIND of number (0, big, negative, fraction, within the restrictions); the same
# result every time -> a reason. Example (ours): x != 0; x^2 >= x / x^2 < x / x^2 = x / none -> 1, 2, -2, 1/2.
f3c9 = I('f3c9', 'One working example does not rule out "None"', size=28)
f3c0 = I('f3c0', 'Given: $\\ x\\ne0$. $\\ $Necessarily true?', size=32)
f3c1 = I('f3c1', '(1) $\\ x^2\\ge x$', size=32)
f3c1d = I('f3c1d', '(2) $\\ x^2<x$', size=32)
f3c1c = I('f3c1c', '(3) $\\ x^2=x$', size=32)
f3c1b = I('f3c1b', '(4) $\\ $None of the above is necessarily true', size=28)
f3c2 = IH('f3c2', '$x=0$ not allowed. $\\ x=1$: $\\ 1^2=1$', size=32)
f3c3a = IH('f3c3a', '(1) $\\ 1\\ge1$', size=32, col=1)
f3c3b = IH('f3c3b', '(2) $\\ 1<1$, no', size=32, col=1)
f3c3c = IH('f3c3c', '(3) $\\ 1=1$', size=32, col=1)
f3c4 = IH('f3c4', '$x=2$: $\\ $(1) $\\ 4\\ge2$', size=32, col=1)
f3c4b = IH('f3c4b', '(3) $\\ 4=2$, no', size=32, col=1)
f3c10 = I('f3c10', 'Left: $\\ $(1) $\\ x^2\\ge x$ $\\quad$ and $\\quad$ (4) None', size=32)
f3c5 = I('f3c5', 'Break (1)? $\\ $Change the kind: zero, big, negative, fraction', size=28)
f3c6 = IH('f3c6', '$x=-2$: $\\ 4\\ge-2$, (1) stays', size=32)
f3c7 = IH('f3c7', '$x=\\frac12$: $\\ \\frac12\\cdot\\frac12=\\frac14$', size=32)
f3c7b = IH('f3c7b', '$\\frac14\\ge\\frac12$, no $\\ \\to$ (1) is out', size=32)
f3c8 = I('f3c8', 'Answer: $\\ $(4) None of the above', size=32)
f3c11 = I('f3c11', 'Examples agree? $\\ \\to$ still need the reason', size=30)
f3cd0 = I('f3cd0', 'Given: $x+y=6$. $\\ $Find $x-y$.', size=32)
f3cd1 = IH('f3cd1', '$x=1,\\ y=5:\\ 1+5=6$', size=30)
f3cd2 = IH('f3cd2', '$x-y=1-5=-4$', size=32, col=1)
f3cd3 = IH('f3cd3', '$x=2,\\ y=4:\\ 2+4=6$', size=30)
f3cd4 = IH('f3cd4', '$x-y=2-4=-2$', size=32, col=1)
f3cd5 = I('f3cd5', 'Both fit the given; different answers: cannot be determined', size=28)
f3m1 = I('f3m1', 'When: $\\ =?$ with number choices $\\ $·$\\ $ letters in choices', size=30)
f3m1b = I('f3m1b', '$\\qquad\\quad$ a ratio $\\ $·$\\ $ more letters than equations', size=30)
f3m2 = I('f3m2', '1. Check every restriction', size=30)
f3m3 = I('f3m3', '2. An easy allowed number (often zero); $\\ $say why', size=30)
f3m4 = I('f3m4', '3. Which choices does it rule out?', size=30)
f3m5 = I('f3m5', '4. More than one left $\\to$ another number, only those', size=30)
f3m7 = I('f3m7', '"None" or "Cannot be determined": examples alone are not proof', size=28)
f3m6 = I('f3m6', 'It\'s your safety net', size=30)

video('pt51-plug-numbers', 'lesson', slides=[
    S('Plugging In Numbers',
      L("Psychometric thinking, plugging in numbers. Of all our super-methods, this is the one you'll use the most.")),
    # ------------------------------------------------------------------ part 1: what, why, when
    S('Why it matters',
      L("On the exam, many hard questions are full of letters. An expression with x, or choices with x and y. The school "
        "way is to work with the letters. That takes time, and it's easy to make a mistake on the way."),
      L("Plugging in numbers turns the letters into numbers that we choose ourselves. Then a hard question from the end of "
        "the section becomes an easy one, like a question from the beginning. It makes the question easier, and it saves "
        "time.", show(f3w1, 'turns the letters into numbers'), show(f3w2, 'Then a hard question'))),
    S('When do I use it?',
      L("So when do I use it? Look for letters. There are two main signs."),
      L("The first sign. The question has an expression with a letter, and it asks what it equals. Something equals a "
        "question mark. And the choices are numbers.", show(f3s1, 'The first sign')),
      L("The second sign. The choices have letters in them, like x plus four, or x squared y.",
        show(f3s2, 'The second sign')),
      L("Careful, an equation with one letter is different. In three x plus five equals twenty, x has one fixed value, so "
        "I can't choose it. There I plug in the answer choices instead. That's the method from the last lesson.",
        show(f3s3, 'an equation with one letter'))),
    S('Why it works',
      L("Why does it work? Let's see an example. What is the bracket x plus two, squared, minus x times the bracket x plus "
        "four? And the choices are numbers.", show(f3e1, "Let's see an example")),
      L("x can be any number here. But the answer is one number, so the expression must give the same number for every x. "
        "And if it's right for every number, then it's right for the number I choose."),
      L("So which number? x equals one, because it's small and easy. One plus two is three, and three squared is nine. In the part we subtract, x is one and x plus four is five. One times five is five. Nine minus five is four.", show(f3e1a, 'x equals one, because'), show(f3e1a0, 'One plus two is three'), show(f3e1a1, 'One times five is five'), show(f3e1a2, 'Nine minus five')),
      L("Let's check with another number, x equals three, to see that it really gives the same result. Three plus two is five, and five squared is twenty-five. Three "
        "times seven is twenty-one. Twenty-five minus twenty-one is four again.", show(f3e1b, 'x equals three'), show(f3e1b0, 'Three plus two is five'), show(f3e1b1, 'Three times seven is twenty-one'),
        show(f3e1b2, 'Twenty-five minus twenty-one')),
      L('Both examples gave four. They show what happens with our chosen numbers. The algebra explains why it always works: x plus two, squared, is x squared plus four x plus four. And x times x plus four is x squared plus four x. Subtracting leaves four. So in this question, where the choices are numbers, one allowed trial gives the answer.', show(f3e1c, 'x plus two, squared, is'), show(f3e1d, 'And x times x plus four'), show(f3e1e, 'Subtracting leaves four'))),
    S('Letters in the choices',
      L("Now the second sign, letters in the choices. The bracket x plus three, squared, minus the bracket x plus one, "
        "squared. The choices are four x plus eight, two x plus eight, four x plus ten, and eight.",
        show(f3e2, 'Now the second sign'), show(f3e2c, 'The choices are')),
      L("First I say which number and why, before I use it. x equals two, because it's small, and two squared is easy.",
        show(f3e2x0, 'x equals two, because')),
      L("Two plus three is five, and five squared is twenty-five. Two plus one is three, and three squared is nine. "
        "Twenty-five minus nine is sixteen. So the right choice must give sixteen when x is two.",
        show(f3e2x, 'Twenty-five minus nine')),
      L("Now we check the choices against sixteen. Choice number one says four x plus eight. With x as two, four times two plus eight is sixteen, so it stays. Choice number two says two x plus eight. Two times two plus eight is twelve, not sixteen, so it's out.",
        show(f3e2r1, 'Four times two plus eight'), show(f3e2r2, 'Two times two plus eight')),
      L("Choice number three says four x plus ten. Four times two plus ten is eighteen, not sixteen, so it's out. Choice number four is eight. Eight is not sixteen, so that choice is out too.", show(f3e2r3, 'Four times two plus ten'),
        show(f3e2r4, 'Eight is not sixteen')),
      L("Three choices are out, so the one that's left is the answer, four x plus eight. We don't need to check it, because "
        "one of the four must be right. And why not stop at the first one that gave sixteen? Because another choice can "
        "give sixteen too, by chance. We'll see that in a minute.", show(f3e2n, 'Three choices are out')),
      L("That's why plugging in is a safety net. When you know the algebra, a number checks it. And when the algebra gets "
        "stuck, a number still gets you to the answer.", show(f3net, 'a safety net'))),
    # ------------------------------------------------------------------ part 2: choosing the number
    S('Keep the conditions',
      L("How do we choose the number? First, we check every restriction in the question. The number must obey "
        "all of them. If it says x is at least four, x can't be two.",
        show(f3k1, 'If it says x is at least four')),
      L("If a must be positive and whole, it can't be zero, and it can't be one half. Now look at five divided by x. "
        "Here x is the denominator, the bottom of the fraction. x can't be zero, because we can't divide by zero.",
        show(f3k2, 'If a must be positive and whole'), show(f3k3, 'five divided by x')),
      L("In a figure, choose values that fit the given conditions. Don't choose an angle just because it looks that size in the drawing. The figure may not be drawn to scale.", show(f3k4, 'In a figure')),
      L("And a good first try is often the edge of what's allowed. If x is at least four, try four itself.",
        show(f3k5, 'the edge of what'))),
    S('Choose, check, try again',
      L("Second, we choose an easy number that's allowed. Zero is often the fastest, because multiplying by zero gives "
        "zero. But check every restriction first. We can't use zero if it makes the denominator zero.",
        show(f3t9, 'Zero is often the fastest')),
      L("Here's an example. x times the bracket x plus one. The choices are x squared plus x, three x, x squared plus one, "
        "and four x.", show(f3t0, "Here's an example"), show(f3t1, 'The choices are')),
      L("Is there a restriction? No, x can be any number. So zero is allowed, and we take x equals zero. Zero times one is "
        "zero. So the right choice must give zero when x is zero.", show(f3t2, 'Zero times one is zero')),
      L("Third, we check what zero rules out. Choice number one says x squared plus x. Zero plus zero is zero, so it stays. "
        "Choice number two says three x. Three times zero is zero, so it stays too.", show(f3t3a, 'Zero plus zero is zero'),
        show(f3t3a2, 'Three times zero is zero')),
      L("Choice number three says x squared plus one. Zero plus one is one, not zero, so it's out. Choice number four says "
        "four x. Four times zero is zero, so it stays.", show(f3t3b, 'Zero plus one is one'), show(f3t3b2, 'Four times zero is zero')),
      L("Three choices give zero, so zero can't tell them apart. That's why we don't stop at the first choice that fits. "
        "Fourth, we try another easy allowed number, and we check only the three choices that are left.",
        show(f3t3c, 'Three choices give zero')),
      L("Now x equals one. One times two is two, so the right choice must give two. x squared plus x is one plus one, two, "
        "so it stays. Three x is three, not two, so it's out. Four x is four, not two, so it's out too.",
        show(f3t4, 'One times two is two'), show(f3t5, 'x squared plus x is one plus one'),
        show(f3t6, "so it's out"), show(f3t6b, "so it's out too")),
      L("Only x squared plus x is left, so it's the answer. No third try is needed. So that's how we choose. Check the "
        "restrictions, choose an easy allowed number, and see what it rules out. Try another number only if more than one "
        "choice is left.", show(f3t7, 'Only x squared plus x is left'), show(f3t8, 'Check the'),
        show(f3t8b, 'Try another number only if'))),
    S('Choices that tie',
      L("Here's an example where zero isn't allowed. x squared times x to the power of three, all divided by x. The choices "
        "are x to the power of four, x to the power of five, x to the power of six, and x to the power of three.",
        show(f3z0, "Here's an example")),
      L("First the restrictions. x is at the bottom of the fraction, and we can't divide by zero. So zero isn't allowed "
        "here.", show(f3z2, 'First the restrictions')),
      L("The next easy number is one. One to any power is one. So the question gives one, and all four choices give one "
        "too. Nothing is ruled out, so we need another try.", show(f3z1, 'So the question gives one')),
      L("Now x equals two. Two squared is four, and two to the power of three is eight. Four times eight is thirty-two, and "
        "thirty-two over two is sixteen. So the right choice must give sixteen.", show(f3z3, 'Now x equals two'),
        show(f3z3b, 'thirty-two over two is sixteen')),
      L("Now check each choice with x as two. Choice number one is x to the power of four, which gives sixteen. "
        "Choice number two is x to the power of five, which gives thirty-two, not sixteen. "
        "Choice number three is x to the power of six, which gives sixty-four, not sixteen. "
        "Choice number four is x to the power of three, which gives eight, not sixteen. "
        "Only choice number one matches the expression's sixteen.",
        show(f3z3c, 'which gives sixteen'), show(f3z3d, 'which gives thirty-two'),
        show(f3z3e, 'which gives sixty-four'), show(f3z3f, 'which gives eight')),
      L("So zero and one are fine to start with, when allowed. But with powers in the choices, they often make every choice give the "
        "same result. Then we just take the next easy allowed number.",
        show(f3z4, 'they often make every choice'))),
    S('Two letters',
      L("Two letters may get the same number, unless the question says they're different. Giving them the same number "
        "is often the fastest. "
        "For example, the bracket a plus three, times the bracket b plus three. From that product we "
        "subtract three a, three b, and a b. The choices are zero, three, six and nine.", show(f3d0, 'For example'),
        show(f3d0c, 'The choices are zero')),
      L("There's no restriction, so let's take zero for both letters. Zero plus three is three, and three times three is "
        "nine. Three a, three b and a b are all zero. So the expression is nine.",
        show(f3d1, 'three times three is nine'), show(f3d1c, 'So the expression is nine')),
      L("The choices are numbers, so only one of them can be nine, choice number four. One try is enough.",
        show(f3d1b, 'The choices are numbers')),
      L("With letters in the choices, the same number can make two choices tie. Look at two choices, a squared b, and a b "
        "squared. With a and b both one, both choices give one.", show(f3d2, 'Look at two choices'),
        show(f3d3, 'both choices give one')),
      L("So we keep a as one, and we change b to two. Then we check only those two choices. a squared b is one times two, "
        "two. And a b squared is one times four, four. Now they're different. So different letters don't need different "
        "numbers. We change one only when the same number makes choices tie.", show(f3d4, 'a squared b is one times two'), show(f3d4c, 'And a b squared is one times four'),
        show(f3d5, "So different letters don't need"))),
    # ------------------------------------------------------------------ part 3: two more cases, and "always"
    S('No letters: a ratio',
      L("A third case. Sometimes there are no letters at all, but an amount is unknown, and they ask for a ratio or a part. In a ratio, "
        "the actual numbers don't matter. One to two, two to four and ten to twenty are the same ratio.",
        show(f3r0, 'One to two, two to four')),
      L("So I may choose the amount myself. For example, half of a number plus a third of the same number. What part of the "
        "number is it?", show(f3r1, 'half of a number plus a third')),
      L("Which number? Six, because both two and three go into it. Half of six is three, and a third of six is two. "
        "Together five, out of six. So it's five sixths of the number, whatever the number is.",
        show(f3r2a, 'Half of six is three'), show(f3r2c, 'a third of six is two'),
        show(f3r2, 'Together five'), show(f3r2b, "So it's five sixths"))),
    S('Case 4: pick values',
      L("The fourth case. An equation, but with more letters than equations, and they ask for one value. For example, four x "
        "plus six y equals eighteen. What is six x plus nine y?", show(f3q0, 'For example, four x')),
      L("An equation with two letters can have many allowed solutions. Sometimes the result they ask for changes between them. Then it cannot be determined. But here, both terms they ask for are one and a half times the terms in the given equation. So their sum is fixed too. Let's use one easy solution to calculate it."),
      L('I give one letter a value, and I solve the equation for the other. x equals zero, because multiplying by zero makes the whole x term zero. Then six y equals eighteen. Divide both sides by six to find y. Eighteen divided by six is three, so y is three.', show(f3q3, 'I give one letter a value'), show(f3q1, 'Then six y equals eighteen'), show(f3q1b, 'Eighteen divided by six is three')),
      L("Now what they ask. Six times zero is zero, and nine times three is twenty-seven. So six x plus nine y is "
        "twenty-seven.", show(f3q2, 'nine times three is twenty-seven')),
      L("Here zero makes the calculation easy, and it's allowed. But I chose only x. The equation then made y equal to three. I can't choose both letters freely: they still have to satisfy the equation."),
      L("And it's really true. Six x plus nine y is one and a half times four x plus six y, because each part is one and a half times as big. And one and a half times "
        "eighteen is twenty-seven.", show(f3q4, "And it's really true"))),
    S('Nothing-changes value',
      L('One more trick for choosing the number. In a story with letters, look for an allowed value where nothing changes. If nobody joins or nothing is added, sometimes we know the result without a formula. But that value must still be allowed by the question.'),
      L('For example, n friends rent a boat for P shekels and share the cost. Then k more friends may join. In this example k may be zero: nobody has to join. They share the cost again. By how much less does each one pay?', show(f3v0, 'For example, n friends')),
      L("Plug in k equals zero. Nobody joined, so nobody pays less, and the answer must be zero. So every choice that "
        "doesn't give zero when k is zero is out, with no calculation at all.", show(f3v1, 'Plug in k equals zero'),
        show(f3v2, 'So every choice')),
      L("This value often leaves two choices. Then use a tie-breaker, an ordinary number like k equals one, and check only "
        "the two that are left.", show(f3v3, 'This value often leaves'))),
    S('Always or not always',
      L("Now, questions about what is always true, or not always true. To show that something is not always true, one "
        "example where it fails is enough."),
      L("For example, is a squared plus b squared always equal to the bracket a plus b, squared? Let a equal one and b "
        "equal two, two small, easy numbers. One plus four is five, and three squared is nine. Five is not nine, so it's not always true. One "
        "counterexample, and we're done.", show(f3n0, 'For example, is a squared'), show(f3n1, 'One plus four is five'),
        show(f3n1b, 'three squared is nine'), show(f3n1c, 'Five is not nine'), show(f3n2, 'One counterexample')),
      L("But always is different. A few examples that work don't prove always, because the next number might fail. In a "
        "question with choices, we don't prove it. We rule out the other three choices, and the one that's left is the "
        "answer.", show(f3n3, 'But always is different'))),
    S('Cannot be determined',
      L("Some questions have a choice that says cannot be determined. That means the givens don't fix one answer. "
        "Another choice you may see is none of the above is necessarily true. That means none of the listed statements "
        "is true in every allowed case."),
      L("One working example doesn't rule out either kind of choice. Why? Because another allowed example might give "
        "a different result, or make the statement false. We need to look beyond that one example.",
        show(f3c9, "One working example doesn't rule out")),
      L("For example, given: x is not equal to zero. Which of the following is necessarily true? Choice number one, x "
        "squared is greater than or equal to x. Choice number two, x squared is smaller than x. Choice number three, x "
        "squared is equal to x. And choice number four, none of the above is necessarily true.",
        show(f3c0, 'For example, given'), show(f3c1, 'Choice number one'), show(f3c1d, 'Choice number two'), show(f3c1c, 'Choice number three'),
        show(f3c1b, 'And choice number four')),
      L("Necessarily true means true for every allowed x. So one x where a choice is false rules it out. Zero isn't "
        "allowed, so the easiest number is one. One squared is one.", show(f3c2, 'One squared is one')),
      L("Choice number one says x squared is greater than or equal to x. One is equal to one, so it stays. Choice number "
        "two says x squared is smaller than x. One isn't smaller than one, so it's out.",
        show(f3c3a, 'One is equal to one'), show(f3c3b, "One isn't smaller")),
      L("Choice number three says x squared is equal to x. One equals one, so it stays too. Choice number four stays too. "
        "We haven't shown that either remaining statement is always true.", show(f3c3c, 'One equals one')),
      L("Now we try another easy number, two, and we check only choice numbers one and three. Two squared is four. Four is "
        "greater than two, so choice number one stays. Four isn't equal to two, so choice number three is out.",
        show(f3c4, 'Four is greater than two'), show(f3c4b, "Four isn't equal to two"))),
    S('Change the kind of number',
      L("Choice number one and choice number four are left. Our examples haven't proved choice number one. So we ask: is "
        "choice number one always true? Three or ten would keep choice number one true, just like two.", show(f3c10, 'Choice number one and')),
      L("To check whether choice number one can fail, we try a different kind of number. Zero, a big number, a negative number, or "
        "a fraction, as long as the restriction allows it. Zero isn't allowed here.",
        show(f3c5, 'we try a different kind of number')),
      L("A negative number, minus two. Its square is four, and four is greater than minus two. So choice number one still "
        "stays.", show(f3c6, 'four is greater than minus two')),
      L("A fraction, one half. One half times one half is one quarter. Is one quarter greater than or equal to one half? "
        "No, it's smaller. So choice number one isn't always true, and it's out.",
        show(f3c7, 'One half times one half'), show(f3c7b, "No, it's smaller")),
      L("Only choice number four is left. None of the above is necessarily true, so that's the answer.",
        show(f3c8, 'Only choice number four is left')),
      L("And what if all the numbers we tried agree? That still doesn't prove always. We need a reason covering every "
        "allowed case, like in our earlier equation example. There the requested expression was always one and a half "
        "times the given eighteen, so its value was fixed.", show(f3c11, "That still doesn't prove always"))),
    S('When the answer is not fixed',
      L("Now let's see cannot be determined in numbers. Given, x plus y is six. What is x minus y?", show(f3cd0, 'x plus y is six')),
      L("Try x equals one and y equals five. One plus five is six, so they fit the given. But one minus five is minus four.",
        show(f3cd1, 'One plus five is six'), show(f3cd2, 'is minus four')),
      L("Now try x equals two and y equals four. Two plus four is six, so this pair fits too. Two minus four is minus two.",
        show(f3cd3, 'Two plus four is six'), show(f3cd4, 'is minus two')),
      L("Both pairs fit the same given, but the requested answers are different. So the given doesn't fix x minus y. "
        "It cannot be determined. Two different results are enough to show that.", show(f3cd5, 'It cannot be determined'))),
    S('So when do I use it?',
      L("So, when do I plug in numbers? When there's an expression with a letter and the choices are numbers. When there "
        "are letters in the choices. When the amount doesn't matter, like in a ratio. And when there are more letters than "
        "equations.", show(f3m1, 'when do I plug in numbers'), show(f3m1b, 'When the amount')),
      L("And how? First, check every restriction. Then choose an easy allowed number, often zero, and say why before you "
        "use it. See which choices it rules out. If more than one is left, try another easy number, and check only those.",
        show(f3m2, 'check every restriction'), show(f3m3, 'Then choose an easy allowed number'),
        show(f3m4, 'See which choices'), show(f3m5, 'If more than one is left')),
      L("Don't cross out none of the above or cannot be determined just because your examples agreed. Test a different "
        "kind of allowed number, or explain why the result must stay the same. And remember, it's your safety net.",
        show(f3m7, "Don't cross out none of the above"),
        show(f3m6, "it's your safety net")),
      L("It's the most important technique on the exam, so practice it a lot. Now let's see it in sample questions. "
        "[pause] Okay. I'll see you in the next video.")),
])

CAMERA_SPLITS = globals().get('CAMERA_SPLITS', []) + [
    ('pt51-plug-numbers', 'Plugging In Numbers', [
        (1, None),
        (5, "Let's continue with plugging in numbers, and how to choose the number."),
        (8, "Let's continue with two letters, and two more cases."),
        (12, "Let's continue with what is always true, and a special kind of choice."),
    ]),
]


# ------------------------------------------------------------------------------------------------ pt-q10
# Hebrew: an expression with x, number choices -> any allowed x gives the same value; x >= 3 (course: 4) -> the
# smallest, most convenient; inside the root 0; root 6. "The school way: spot the shortcut formula, brackets, root".
# Added: x = 0 breaks the root (keep the conditions, at the step); the school way as a short second method.
f3a1 = I('f3a1', 'Asked: one value valid for every allowed $x\\ge4$', size=30)
f3a2 = IH('f3a2', '$x=4$: $\\ 4^2-8\\cdot4+16$', size=34)
f3a2b = IH('f3a2b', '$=16-32+16=0$', size=34)
f3a3 = I('f3a3', '$\\sqrt{4+2-\\sqrt0}=\\sqrt6$', size=36)
f3a0 = I('f3a0', '$x=0$: $\\ \\sqrt{16}=4$, $\\ 2-4=-2$ ✗ not allowed', size=30, col=1)
f3a4 = I('f3a4', '$x^2-8x+16=(x-4)^2$', size=34)
f3a5 = I('f3a5', '$x\\ge4$: $\\ \\sqrt{(x-4)^2}=x-4$', size=34)
f3a6 = I('f3a6', '$\\sqrt{x+2-(x-4)}$', size=34)
f3a6b = I('f3a6b', '$=\\sqrt{x+2-x+4}$', size=34)
f3a6c = I('f3a6c', '$=\\sqrt6$', size=34)
video('solve-pt-q10', 'solution', qid='pt-q10', slides=[
    S('Method 1 · Plugging in numbers',
      L('Given: x is greater than or equal to four. We have a square root inside another square root. Inside the outer root is x plus two, minus the square root of x squared minus eight x plus sixteen. What does this whole expression equal?', pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("So it's an expression with x, and they ask what it equals. And all four choices are numbers. That's the first sign "
        "for plugging in numbers. [short pause] We'll solve it two ways, by plugging in a number, and then with algebra.",
        pt('stem: ask', 'they ask what it equals')),
      L("x can be any number that is four or more. Here they ask for one value that works for every allowed x. "
        "The correct choice must therefore work for an easy example too. So we may check one case.", show(f3a1, 'x can be any number')),
      L("Which number? Four, because it's the smallest number allowed. It's the edge, and at the edge things often become "
        "zero. Careful, zero is not allowed here. If you try it, the inner root is four, and two minus four is negative "
        "two. There's no square root of a negative number.", show(f3a0, 'Careful, zero is not allowed')),
      L("So x equals four. Inside the inner root, four squared is sixteen, and eight times four is thirty-two. Sixteen minus "
        "thirty-two plus sixteen is zero, and the root of zero is zero.", show(f3a2, 'So x equals four'), show(f3a2b, 'Sixteen minus')),
      L('The inner root is now zero. Inside the outer root, we have four plus two minus zero, which is six. So the whole expression is the root of six. Choice number four is our answer.',
        show(f3a3, 'So the whole expression is the root'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · The math way',
      L("[pause] Now the math way, with algebra. Remember the shortcut formula. The bracket x minus four, squared, is x squared minus "
        "eight x plus sixteen.", show(f3a4, 'Remember the shortcut formula')),
      L("The root of a square gives back the number, as long as it isn't negative. x is at least four, so x minus four is "
        "zero or more. So the inner root is x minus four.", show(f3a5, 'The root of a square')),
      L('Inside the outer root, we subtract x minus four from x plus two. We subtract both terms of x minus four. So that becomes x plus two minus x plus four. The x terms cancel, and two plus four is six. The outer root is still there, so the answer is the root of six. Choice number four again.',
        show(f3a6, 'Inside the outer root'), show(f3a6b, 'We subtract both terms'), show(f3a6c, 'The x'),
        mk('tick', 'choice 4', 'choice number four again')),
      L("For the algebra you had to spot the formula and keep the signs right. The number took one line, and it's a "
        "safety net when you don't see the formula. [pause] Okay. I'll see you in the next question.",
        pt('f3a6c', 'For the algebra you had to'))),
])


# ------------------------------------------------------------------------------------------------ pt-q11 (question figure)
# Hebrew: alpha is in all the answers -> for each alpha a matching beta -> a particular case; a value that looks logical
# in the figure (not 120): 50 -> 40, 40, base angles 80, D = 20, beta = 120; we don't look for the right answer, we rule out
# three: 110 out, "ends in 5, not round" out, 20 out -> the last without checking; the regular way (angle sums) is long;
# flattening: with 50 instead of alpha it would be a question from the start of the section.
# V3: the question figure on the left; our colour copy on the right, filled as the angles are found (B's two halves teal,
# the base angle at C and D orange, triangle D B (crossing) tinted for beta). Slide 2: the choice rows; slide 3 (algebra):
# the same copy with the expressions.
f3B, f3C, f3D, f3A = (110.0, 360.0), (410.0, 360.0), (260.0, 23.1), (410.0, 165.2)
f3E = gcross(f3B, f3A, f3D, f3C)


def f3_ang(P, Q, R_, r, col, label=None, lr=None):
    """the inside angle at P between the rays P->Q and P->R_ (the smaller one)"""
    a, b = gdir(*P, *Q), gdir(*P, *R_)
    if (b - a) % 360 > 180: a, b = b, a
    e = ('arc', P[0], P[1], r, a, b, col)
    if label: e = e + (label,) + ((lr,) if lr else ())
    return e


f3base = [('seg', *f3B, *f3C), ('seg', *f3C, *f3D), ('seg', *f3D, *f3B), ('seg', *f3B, *f3A), ('seg', *f3A, *f3C),
          ('right', *f3C, 90, 180, 16, 'ink'), f3_ang(f3A, f3B, f3C, 34, 'ink'), f3_ang(f3E, f3D, f3B, 26, 'ink'),
          ('txt', 395, 216, 'α', 'ink', 24), ('txt', 300, 192, 'β', 'ink', 24),
          ('txt', 260, 2, 'D', 'ink', 24, True), ('txt', 428, 152, 'A', 'ink', 24, True),
          ('txt', 92, 378, 'B', 'ink', 24, True), ('txt', 428, 378, 'C', 'ink', 24, True)]
f3g11 = PIN(GEO('f3g11', [
    ('line', f3base),
    ('a50', [('txt', 440, 214, '50°', 'teal', 22)]),
    ('b1', [f3_ang(f3B, f3C, f3A, 70, 'small', '40°', 92)]),
    ('b2', [f3_ang(f3B, f3A, f3D, 52, 'small', '40°', 74)]),
    ('c80', [('tick', *f3D, *f3B, 1), ('tick', *f3D, *f3C, 1), f3_ang(f3C, f3B, f3D, 34, 'large', '80°', 58)]),
    ('d20', [f3_ang(f3D, f3B, f3C, 44, 'large', '20°', 64)]),
    ('beta', [('tint', [f3D, f3B, f3E], 'teal'), ('txt', 300, 230, '120°', 'teal', 24)]),
], vb='70 -17 400 422', w=340, title='Triangles ABC and DBC with the angles for alpha 50'))
_R(f3g11, 210, x=1180)
f3h0 = I('f3h0', 'So far: $\\ \\alpha=50°$ $\\to$ $\\beta=120°$', size=28, col=1)
f3h1 = I('f3h1', '(1) $60°+50°=110°$ ✗', size=30, col=1)
f3h2 = I('f3h2', '(2) $90°+25°=115°$ ✗ $\\ $(ends in 5)', size=30, col=1)
f3h3 = I('f3h3', '(3) $200°-180°=20°$ ✗ $\\ $(angle D)', size=30, col=1)
f3h4 = I('f3h4', 'Three out $\\to$ (4) ✓', size=30, col=1)
f3j1 = I('f3j1', '$\\angle B=90°-\\alpha$', size=30, col=1)
f3j1b = I('f3j1b', '$\\angle DBC=180°-2\\alpha$', size=30, col=1)
f3j2 = I('f3j2', '$\\angle D=180°-2(180°-2\\alpha)$', size=30, col=1)
f3j2b = I('f3j2b', '$=4\\alpha-180°$', size=30, col=1)
f3j3 = I('f3j3', '$\\beta=180°-(4\\alpha-180°)-(90°-\\alpha)$', size=30, col=1)
f3j3b = I('f3j3b', '$=270°-3\\alpha$', size=30, col=1)
for _it, _y in ((f3h0, 200), (f3h1, 260), (f3h2, 320), (f3h3, 380), (f3h4, 440), (f3j1, 230), (f3j1b, 280), (f3j2, 330),
                 (f3j2b, 380), (f3j3, 430), (f3j3b, 480)):
    _R(_it, _y, x=1010)
video('solve-pt-q11', 'solution', qid='pt-q11', slides=[
    SM('Method 1 · Plugging in numbers', 'Plugging in a number',
      L("In the figure, A B C is a right triangle, and D B C is an isosceles triangle, with D B equal to D C. A B bisects "
        "angle D B C. What is beta?", pt('stem', 'In the figure', 'hl', 8.0), voice='calm', pause=0.5),
      L("Beta is the angle where A B crosses D C. And all the choices have alpha in them. Letters in the choices, that's "
        "the second sign for plugging in numbers. [short pause] We'll solve it two ways, by plugging in a number, and then "
        "with the angles in letters.", show(f3g11['line'], 'Beta is the angle')),
      L("For every alpha there's a matching beta. So let's choose one alpha and calculate beta. Which number? An easy one that fits the angle conditions. Alpha is in a right triangle, so it's less than ninety. Let's take fifty, a round number. We'll check the other triangle's angles too.", show(f3g11['a50'], "Let's take fifty")),
      L("In triangle A B C, two angles are fifty and ninety. Together they're a hundred forty. The three angles must total a hundred eighty. So angle B is a hundred eighty minus a hundred forty, which is forty.",
        show(f3g11['b1'], 'So angle B is a hundred eighty')),
      L("A B bisects angle D B C, so the angle above it is also forty. So the whole angle D B C is eighty.",
        show(f3g11['b2'], 'the angle above it is also forty')),
      L("D B equals D C, so the base angles are equal, and angle C is also eighty. That's why our number must fit the angle conditions, not just the drawing. With alpha forty, the base angles would be a hundred each, and a triangle can't have two angles of a hundred.", show(f3g11['c80'], 'angle C is also eighty')),
      L("Eighty plus eighty is a hundred sixty. The angles of a triangle add up to a hundred eighty, so angle D is a hundred eighty minus a hundred sixty, twenty degrees.",
        show(f3g11['d20'], 'So angle D is')),
      L("Now look at the triangle with corners D, B and the crossing point. Its angles are twenty at D and forty at B. "
        "Twenty plus forty is sixty, so beta is a hundred eighty minus sixty, a hundred twenty degrees.",
        show(f3g11['beta'], 'Now look at the triangle'))),
    SM('Method 1 · Plugging in numbers', 'Rule out three',
      L("Now which choice gives a hundred twenty? Actually, we don't look for it. We rule out three choices, with alpha "
        "equal to fifty.", show(f3h0, 'Now which choice')),
      L("Choice number one says sixty plus alpha. Sixty plus fifty is a hundred ten, not a hundred twenty. Out.", pt('choice 1', 'Choice number one says', 'hl', 2.5),
        show(f3h1, 'is a hundred ten'),
        mk('cross', 'choice 1', 'is a hundred ten')),
      L("Choice number two says ninety plus half alpha. That's ninety plus half of fifty. Half of fifty is twenty-five, so the result ends in five, and a "
        "hundred twenty ends in zero. Out, without finishing.", pt('choice 2', 'Choice number two says', 'hl', 2.5),
        pt('choice 2', "That's ninety plus"), show(f3h2, 'so the result ends in five'),
        mk('cross', 'choice 2', 'Out, without finishing')),
      L("Choice number three says four alpha minus a hundred eighty. Four times fifty is two hundred, and two hundred minus a hundred eighty is twenty. That's angle D, not beta. "
        "Out.", pt('choice 3', 'Choice number three says', 'hl', 3.0), pt('choice 3', 'Four times fifty'), show(f3h3, "That's angle D"), mk('cross', 'choice 3', "That's angle D")),
      L("Choice number four says two hundred seventy minus three alpha. Three choices are out, so choice number four is "
        "our answer, without checking it. One choice must be right, and we showed the other three are wrong.",
        pt('choice 4', 'Choice number four says', 'hl', 3.0), show(f3h4, 'so choice number four is our answer'),
        mk('tick', 'choice 4', 'so choice number four is our answer'))),
    SM('Method 2 · The math way', 'With letters',
      L("[pause] Now the math way, the same steps with alpha. In triangle A B C, angle B is ninety minus alpha. The angle above it is the "
        "same, so angle D B C is two times the bracket ninety minus alpha, a hundred eighty minus two alpha.",
        show(f3j1, 'angle B is ninety minus alpha'), show(f3j1b, 'so angle D B C is')),
      L("Angle C is the other base angle, so it's the same, a hundred eighty minus two alpha. So angle D is a hundred eighty minus two times that. That's "
        "a hundred eighty minus three hundred sixty plus four alpha, so four alpha minus a hundred eighty.",
        show(f3j2, 'So angle D is'), show(f3j2b, 'so four alpha minus')),
      L('Now look at the small triangle with angle beta. Its other angles are D and B. So beta is a hundred eighty, minus angle D, minus angle B. Angle D is four alpha minus a hundred eighty. Subtracting that gives minus four alpha plus a hundred eighty. Angle B is ninety minus alpha. Subtracting that gives minus ninety plus alpha. The numbers give two hundred seventy, and minus four alpha plus alpha gives minus three alpha. So beta is two hundred seventy minus three alpha, choice number four again.',
        show(f3j3, 'So beta is a hundred eighty'), show(f3j3b, 'So beta is two hundred seventy'), mk('tick', 'choice 4', 'choice number four again')),
      L("Look at what the number did. With fifty instead of alpha, this is an easy angle question from the beginning of the "
        "section. The letters are what made it hard. [pause] Okay. I'll see you in the next question.",
        pt('f3j3b', 'Look at what the number did'))),
])


# ------------------------------------------------------------------------------------------------ pt-q12
# Hebrew: the factorial taught (5!, 4!, 3!); an expression with a letter -> plug in; a = 1 (the smallest positive
# integer): 1! 3! = 6; 24 out, 6 stays, 3 out, 6 stays -> only two out -> another plug-in, the ruled-out ones not rechecked;
# a = 2: 48; 8!: 8 x 7 = 56 is already too big -> out; mark the 4th. Added: why 1 tied (1 hides differences), the short algebra.
f3f1 = I('f3f1', '$5!=5\\cdot4\\cdot3\\cdot2\\cdot1$', size=32)
f3f2 = IH('f3f2', '$4!=4\\cdot3\\cdot2\\cdot1=24$', size=32)
f3f3 = IH('f3f3', '$3!=3\\cdot2\\cdot1=6$ $\\quad 2!=2$ $\\quad 1!=1$', size=32)
f3p1 = IH('f3p1', '$a=1$: $\\ 1!\\cdot3!$', size=34)
f3p1b = IH('f3p1b', '$=1\\cdot6=6$', size=34)
f3p2 = IH('f3p2', '(1) $4!=24$ ✗', size=30, col=1)
f3p3 = IH('f3p3', '(2) $3!=6$ ✓', size=30, col=1)
f3p4 = IH('f3p4', '(3) $1\\cdot3=3$ ✗', size=30, col=1)
f3p5 = IH('f3p5', '(4) $1\\cdot2\\cdot3=6$ ✓', size=30, col=1)
f3p6 = IH('f3p6', '$a=2$: $\\ 2!\\cdot4!$', size=34)
f3p6b = IH('f3p6b', '$=2\\cdot24=48$', size=34)
f3p7 = I('f3p7', '(2) $\\ 2^2+2\\cdot2=8$ $\\to$ $8!$', size=30)
f3p7b = I('f3p7b', '$8\\cdot7=56>48$ ✗', size=30)
f3p8 = I('f3p8', 'Three out $\\to$ (4) ✓', size=30)
f3p9 = I('f3p9', '$(a+2)!=(a+2)(a+1)\\cdot a!$', size=34)
f3p10 = I('f3p10', '$a!\\cdot(a+2)!=(a!)^2\\cdot(a+1)(a+2)$', size=34)
CARRY51['solve-pt-q12'] = {2: ['$a=1$: $\\ $(2) ✓ $\\ $(4) ✓']}
video('solve-pt-q12', 'solution', qid='pt-q12', slides=[
    S('What is a factorial?',
      L("a is a positive integer. a factorial, times the bracket a plus two, factorial. What does it equal?",
        pt('stem', 'a is a positive integer', 'hl', 6.0), voice='calm', pause=0.5),
      L("First, what is this exclamation mark? It's called a factorial. It means we multiply all the whole numbers from "
        "that number down to one.", pt('stem', 'what is this exclamation mark')),
      L("For example, five factorial is five times four times three times two times one. Four factorial is four times "
        "three times two times one, twenty-four.", show(f3f1, 'five factorial'), show(f3f2, 'Four factorial')),
      L("Three factorial is three times two times one, six. Two factorial is two times one, two. And one factorial is just "
        "one.", show(f3f3, 'Three factorial')),
      L("Few students solve this with algebra. But it's an expression with a letter, and the choices have letters. So we "
        "can plug in numbers. [short pause] We'll solve it by plugging in, and then see the short algebra too.",
        pt('stem', 'an expression with a letter'))),
    S('Method 1 · Plugging in numbers',
      L("Which number? a must be positive and whole, so the smallest is one. It keeps the factorials tiny.",
        show(f3p1, 'the smallest is one')),
      L("One factorial is one. One plus two is three, and three factorial is six. One times six is six. So the right "
        "choice must give six.", show(f3p1b, 'One times six')),
      L("Choice number one, two a plus two, factorial. Two plus two is four, and four factorial is twenty-four. Not six, "
        "so it's out.", show(f3p2, 'Two plus two is four'), mk('cross', 'choice 1', 'so it')),
      L("Choice number two, a squared plus two a, factorial. One plus two is three, and three factorial is six. It fits, "
        "so it stays for now.", show(f3p3, 'One plus two is three, and three factorial')),
      L("Choice number three, a factorial squared, times a plus two. One squared is one, and one times three is three, not six. Out.",
        show(f3p4, 'One squared is one'), mk('cross', 'choice 3', 'times three is three')),
      L("Choice number four, a factorial squared, times a plus one, times a plus two. One times two times three is six. It "
        "stays too.", show(f3p5, 'One times two times three')),
      L("Only two choices are out, and we need three. Why the tie? Because of the number one. One squared is one, and "
        "one factorial is one, so it hides the differences between the choices.", pt('f3p5', 'Only two choices are out'))),
    S('A tie-breaker number',
      L("So we plug in a second number, a tie-breaker, and we check only the two choices that are left. The ones that are "
        "out stay out. a equals two, the next positive whole number."),
      L("Two factorial is two. Two plus two is four, and four factorial is twenty-four. Two times twenty-four is "
        "forty-eight.", show(f3p6, 'Two factorial is two'), show(f3p6b, 'Two times twenty-four')),
      L("Choice number two. Two squared is four, and two times two is four. Four plus four is eight, so it's eight factorial. Eight times seven "
        "is already fifty-six. That's more than forty-eight, and we still have more numbers to multiply. So it's out, "
        "without finishing.", show(f3p7, 'Two squared is four'), show(f3p7b, 'Eight times seven'), mk('cross', 'choice 2', 'without finishing')),
      L("Three choices are out, so choice number four is our answer.", show(f3p8, 'Three choices are out'),
        mk('tick', 'choice 4', 'so choice number four is our answer'))),
    S('Method 2 · The math way',
      L('Now the math way, the short algebra. The factorial of a plus two starts with a plus two, times a plus one. After those two factors, we have a, times all the whole numbers below it down to one. That last part is a factorial. So we can write the factorial of a plus two as a plus two, times a plus one, times a factorial.',
        show(f3p9, 'Now the math way')),
      L("So the question is a factorial, times a factorial, times a plus one, times a plus two. That's a factorial squared, "
        "times a plus one, times a plus two. Choice number four again. [pause] Okay. I'll see you in the next question.",
        show(f3p10, 'So the question is'), mk('tick', 'choice 4', 'Choice number four again'))),
])


# ------------------------------------------------------------------------------------------------ pt-q13
# Hebrew: each pen writes x/y words, "and then times..." - confusing; letters in the answers -> plug in; x = y = 1: one
# pen, one word -> every choice gives 1 (power, product, quotient: 1 changes nothing) -> choose values that give
# different results; x = 2, y = 1: 2 words a pen, (course) 8 words -> 4 pens; 8 out, the fractions out -> choice 1.
# Check the choices for a tie before the story (R15). After x=y=1 ties them all,
# change only x to 2, keeping y=1 easy. Equal letters are allowed; different
# letters never require different values without a given. Finish the algebra too.
f3i1 = IH('f3i1', '$x=y=1$: $\\ 1,\\ 1,\\ 1,\\ 1$ ✗ tie', size=32)
f3i2 = IH('f3i2', '$x=y=2$: $\\ 16,\\ 16$ ✗ tie', size=32)
f3i3 = IH('f3i3', '$x=2,\\ y=1$', size=32)
f3i4 = I('f3i4', 'A pen: $2$ cm³, $\\ $a word: $1$ cm³ $\\to$ $2$ words a pen', size=30, col=1)
f3i5 = I('f3i5', 'Words: $2^3\\cdot1=8$', size=30, col=1)
f3i5b = I('f3i5b', 'Pens: $\\ 8\\div2=4$', size=30, col=1)
f3i6 = I('f3i6', '(1) $4$ ✓', size=30, col=1)
f3i6b = I('f3i6b', '(2) $8$ ✗', size=30, col=1)
f3i6c = I('f3i6c', '(3) $\\frac14$ ✗ $\\quad$ (4) $\\frac18$ ✗', size=30, col=1)
f3i7 = I('f3i7', 'Words a pen: $\\ \\frac{x}{y}$', size=34)
f3i8 = I('f3i8', 'Pens: $\\ x^3y\\div\\frac{x}{y}$', size=34)
f3i8b = I('f3i8b', '$=x^3y\\cdot\\frac{y}{x}$', size=34)
f3i8c = I('f3i8c', '$=x^2y^2$', size=34)
video('solve-pt-q13', 'solution', qid='pt-q13', slides=[
    S('Method 1 · Plugging in numbers',
      L("One pen holds x cubic centimeters of ink. To write one word, you need y cubic centimeters of ink. Hagai's pens "
        "were enough for him to write x cubed times y words. How many pens did Hagai have?",
        pt('stem', 'One pen holds', 'hl', 9.0), voice='calm', pause=0.5),
      L("Let's try to understand it. A pen holds x cubic centimeters of ink, and each word needs y cubic centimeters, so one pen writes x over y words. Then we'd divide x cubed y by x over y, and that's where many students get tangled.", pt('stem', 'A pen holds x cubic centimeters of ink')),
      L("But look at the choices. They have x and y in them, so we can plug in numbers. [short pause] We'll solve it by "
        "plugging in, and then finish the algebra.", pt('choice 1', 'look at the choices')),
      L("Which numbers? The easiest would be x and y both one. But look at the choices first. They have powers, a product "
        "and fractions. With ones, every choice is one, and nothing is ruled out. So one can't tell them apart here.",
        show(f3i1, 'With ones, every choice is one')),
      L("Let's keep y as one, and change only x to two. That changes how much ink a pen holds. "
        "The ink needed for one word stays at one.", show(f3i3, 'change only x to two')),
      L("Now the story with these numbers. A pen holds two cubic centimeters, and a word needs one. So each pen writes two "
        "words.", show(f3i4, 'A pen holds two cubic')),
      L("He wrote x cubed times y words. Two cubed is eight, and eight times one is eight words. Eight words, two words a pen, so he "
        "had four pens.", show(f3i5, 'Two cubed is eight'), show(f3i5b, 'Eight words, two words a pen')),
      L("He had four pens, so the right choice must give four. Choice number one, x squared y squared, gives four. It fits. Choice number two, x cubed y, gives eight, out. "
        "Choice numbers three and four, one over x squared y squared, and one over x cubed y, are fractions, a quarter "
        "and an eighth, out. So choice number one is our answer.",
        show(f3i6, 'Choice number one, x squared'), show(f3i6b, 'Choice number two, x cubed'), mk('cross', 'choice 2', 'gives eight, out'),
        show(f3i6c, 'Choice numbers three'),
        mk('cross', 'choice 3', 'a quarter and an eighth'), mk('cross', 'choice 4', 'and an eighth, out'),
        mk('tick', 'choice 1', 'So choice number one is our answer'))),
    S('Method 2 · The math way',
      L("[pause] Now the math way, the algebra we started. One pen writes x over y words. The number of pens is all the words, divided "
        "by the words a pen writes.", show(f3i7, 'One pen writes x over y')),
      L("So it's x cubed y divided by x over y. Dividing by a fraction is multiplying by its reciprocal. We swap the top and bottom, so we multiply by y over x. An x cancels, so x cubed becomes x squared, and y times y is y squared. x squared y squared, choice number one again. [pause] Okay. I'll see you in the next question.", show(f3i8, 'So it'), show(f3i8b, 'Dividing by a fraction'), show(f3i8c, 'An x cancels'),
        mk('tick', 'choice 1', 'choice number one again'))),
])


# ------------------------------------------------------------------------------------------------ pt-q14
# Hebrew: an unknown in the answers -> plug in; percent questions: plug in 100; where? at x -> 120 (course 140), 20 out of
# 120 is not convenient; at the whole (the price before) -> after 80 (course 60); 20% (course 40%); check: 100/100 -> 20
# stays; 16 out; 1 out; 500 out -> the first. Added: "percent = out of a hundred" on the spot (percent is topic 23,
# later); the algebra in one line.
f3c1 = I('f3c1', 'Percent: $\\ 40$ out of $100$ = $40\\%$', size=30)
f3c2 = I('f3c2', '$100$ at $x$: $\\ 40$ out of $140$ ✗', size=30)
f3c3 = IH('f3c3', 'Before $100$, after $60$ $\\to$ $x=60$', size=32)
f3c4 = I('f3c4', 'Discount: $\\ 40$ out of $100$ = $40\\%$', size=32)
f3c5 = I('f3c5', '(1) $\\frac{40\\cdot100}{60+40}=\\frac{4000}{100}=40$ ✓', size=30, col=1)
f3c6 = I('f3c6', '(2) $\\frac{40\\cdot60}{100}=\\frac{2400}{100}=24$ ✗', size=30, col=1)
f3c7 = I('f3c7', '(3) $\\frac{60+40}{100}=1$ ✗', size=30, col=1)
f3c8 = I('f3c8', '(4) $\\frac{100\\cdot100}{40}=250$ ✗', size=30, col=1)
f3c9 = I('f3c9', 'Before: $\\ x+40$', size=34)
f3c9b = I('f3c9b', 'Percent: $\\ \\frac{40}{x+40}\\cdot100$', size=34)
video('solve-pt-q14', 'solution', qid='pt-q14', slides=[
    S('Method 1 · Plugging in numbers',
      L("Dana bought a dress at a discount of forty shekels. The price of the dress after the discount was x shekels. What "
        "was the discount on the dress, in percent?", pt('stem', 'Dana bought a dress', 'hl', 7.0), voice='calm', pause=0.5),
      L("There's an x in the choices, so we can plug in numbers. [short pause] We'll solve it by plugging in, and then with "
        "a line of algebra.", pt('choice 1', "There's an x in the choices")),
      L("First, what is a percent? Percent means out of a hundred. A discount of forty shekels on a price of a hundred "
        "shekels is a discount of forty percent. The percent always compares to the whole price, the price before the "
        "discount.", show(f3c1, 'Percent means out of a hundred')),
      L("So where do we put a number? In this percent question, we choose a hundred for the whole price, the price before the discount. Why? Some students put the hundred at x, the price after the discount. Then the price before is a hundred forty, and we'd need forty out of a hundred forty. That's not a nice calculation.", show(f3c2, 'Some students put the hundred at x')),
      L("So we put the hundred at the price before. The discount is forty, so the price after is a hundred minus forty, "
        "sixty. So x is sixty.", show(f3c3, 'The discount is forty, so')),
      L("And the discount is forty out of a hundred, forty percent. So the right choice must give forty when x is sixty.",
        show(f3c4, 'And the discount is forty')),
      L("Now we rule out whatever isn't forty. Choice number one says forty times a hundred, over x plus forty. With x "
        "sixty, that's forty times a hundred, over sixty plus forty. Sixty plus forty is a hundred, and the hundreds cancel. That leaves forty, so it stays.", pt('choice 1', 'Choice number one says', 'hl', 3.0),
        pt('choice 1', 'With x sixty'), pt('choice 1', 'Sixty plus forty is a hundred'), show(f3c5, 'so it stays')),
      L("Choice number two says forty x over a hundred. That's forty times sixty, over a hundred. Forty times sixty is two thousand four hundred, and over a "
        "hundred is twenty-four. Out.", pt('choice 2', 'Choice number two says', 'hl', 2.5), pt('choice 2', "That's forty times sixty"),
        show(f3c6, 'is twenty-four'), mk('cross', 'choice 2', 'is twenty-four')),
      L("Choice number three says x plus forty, over a hundred. That's sixty plus forty, over a hundred. A hundred over a hundred is one. Out.",
        pt('choice 3', 'Choice number three says', 'hl', 2.5), pt('choice 3', "That's sixty plus forty"),
        show(f3c7, 'is one. Out'), mk('cross', 'choice 3', 'is one. Out')),
      L("Choice number four says x plus forty, times a hundred, over forty. That's a hundred times a hundred, over "
        "forty. A hundred over forty is two and a half, and times a "
        "hundred it's two hundred fifty. Out. So choice number one is our answer.",
        pt('choice 4', 'Choice number four says', 'hl', 3.0), pt('choice 4', "That's a hundred times"),
        show(f3c8, "it's two hundred fifty"), mk('cross', 'choice 4', "it's two hundred fifty"),
        mk('tick', 'choice 1', 'So choice number one is our answer'))),
    S('Method 2 · The math way',
      L("Now the math way. The price after the discount is x. To get the original price, we add back the forty-shekel discount. So the price before is x plus forty. We divide the discount, forty, by that original price. Then we multiply by a hundred to get the percent. That's forty over x plus forty, times a hundred, choice number one. I'll see you in the next question.",
        show(f3c9, 'the price before is x plus forty'), show(f3c9b, 'We divide the discount'), mk('tick', 'choice 1', 'choice number one'))),
])


# ------------------------------------------------------------------------------------------------ pt-q15
# Hebrew: no expression with an unknown, no unknowns in the answers - but a ratio: the third case (1 : 2, 2 : 4, 10 : 20);
# a table Orit / Batya, committed / paid; 1 each ("a cheap trip"); a quarter (course: a third) is a fraction -> "who chose
# the 1? I did, so I can change it" -> 4 (course 3); Orit 1, Batya the rest; 7 : 4 (course 5 : 3).
f3o1 = I('f3o1', '$1:2\\ =\\ 2:4\\ =\\ 10:20$', size=32, col=1)
f3o2 = IH('f3o2', 'Agreed: $\\ 1$ each $\\to$ Orit pays $\\frac13$ ✗ not nice', size=32)
f3o3 = IH('f3o3', 'Agreed: $\\ 3$ each $\\ $(total $6$)', size=32)
f3o4 = IH('f3o4', 'Orit paid $\\frac13\\cdot3=1$', size=32)
f3o5 = IH('f3o5', 'Batya paid $6-1=5$', size=32)
f3o6 = I('f3o6', 'Batya: $\\ $paid $:$ agreed $=5:3$', size=34)
video('solve-pt-q15', 'solution', qid='pt-q15', slides=[
    S('Plugging in an amount',
      L("Orit and Batya decided to go on a trip and to share the expenses. Each of them agreed to pay half of the total. In "
        "the end, Orit paid only a third of the amount she had agreed to pay, and Batya paid all the rest of the expenses. "
        "What is the ratio between the amount Batya actually paid and the amount she agreed to pay?",
        pt('stem', 'Orit and Batya', 'hl', 14.0), voice='calm', pause=0.5),
      L("Wait, there's no letter here. Not in the question, and not in the choices. But they ask for a ratio, and in a "
        "ratio the actual amounts don't matter. One to two, two to four and ten to twenty are the same ratio. So we may "
        "choose the amounts ourselves.", pt('stem: ask', 'they ask for a ratio'), show(f3o1, 'One to two')),
      L("Each one agreed to pay half. Let's start small. Say each one agreed to pay one shekel. A cheap trip. Orit paid "
        "only a third of her one shekel. That's a third of a shekel, a fraction, and that's not convenient.",
        show(f3o2, 'Say each one agreed to pay one shekel')),
      L("But who chose the one? I did. So I may change it. Let's choose a number that a third goes into nicely, three.",
        pt('f3o2', 'who chose the one')),
      L("So each one agreed to pay three shekels, six in all. Orit paid a third of three, which is one shekel.",
        show(f3o3, 'So each one agreed to pay three'), show(f3o4, 'Orit paid a third of three')),
      L("Batya paid all the rest. Six minus one is five, so Batya paid five shekels.", show(f3o5, 'Six minus one is five')),
      L("They ask for what Batya actually paid, to what she agreed to pay. That's five to three. Choice number one is our "
        "answer. [pause] Okay. I'll see you in the next question.", show(f3o6, 'That'),
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])


# ------------------------------------------------------------------------------------------------ pt-q24 (original)
# Case 4 (more letters than equations): x = 0 (allowed, kills the x terms) -> y = 2; choices 1, 3 out; the tie-breaker x = 1
# -> y = 2 again; two examples are not "always" (the adaptive-counterexample rule) -> the algebra shows why; the condition
# x != -5 is the hint.
f3y1 = I('f3y1', 'Choose $x$, solve for $y$', size=32)
f3y2 = IH('f3y2', '$x=0$: $\\ 5y=10$, $\\ y=2$', size=34)
f3y3 = IH('f3y3', '$x=1$: $\\ 6y=12$, $\\ y=2$', size=34)
f3y4 = I('f3y4', 'Two examples $\\ne$ always', size=30)
f3y5 = I('f3y5', '$y(x+5)=2(x+5)$', size=36)
f3y6 = I('f3y6', '$x\\ne-5$ $\\to$ $x+5\\ne0$', size=36)
f3y6b = I('f3y6b', '$y=2$ $\\ $for every allowed $x$', size=36)
video('solve-pt-q24', 'solution', qid='pt-q24', slides=[
    S('Method 1 · Plugging in numbers',
      L("Given: x is not equal to negative five. x y plus five y equals two x plus ten. What is y?",
        pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("One equation with two letters, x and y, and they ask for one value. Some students say, one equation and two "
        "letters, it can't be solved. So they choose cannot be determined. That's the trap.",
        pt('choice 4', 'they choose cannot be determined')),
      L("This is the case of more letters than equations. [short pause] We'll solve it by plugging in numbers, and then "
        "see why it works the math way.", show(f3y1, 'more letters than equations')),
      L("If y has one value, it's the same for every allowed x. So I may choose x myself. Which x? Zero, because it makes every term with x equal to zero. And it's allowed, because the only condition is that x isn't negative five.",
        pt('stem: g1', 'the only condition')),
      L("So x equals zero. x y is zero, and two x is zero. We're left with five y equals ten, so y is two.",
        show(f3y2, "We're left with five y")),
      L("With x equal to zero, y is two. So y is not negative five, and it's not negative two. Choice numbers one and three "
        "are out.", mk('cross', 'choice 1', 'Choice numbers one'), mk('cross', 'choice 3', 'and three are out')),
      L("Two choices are left, two, and cannot be determined. If y changed when x changes, the answer would be cannot be "
        "determined. So the tie-breaker is a different x. Let's take x equals one.", pt('choice 4', 'Two choices are left')),
      L("With x equal to one, x y is just y, and two x is two. So y plus five y is six y, and two plus ten is twelve. Six y equals twelve, so y is two again.",
        show(f3y3, 'Six y equals twelve')),
      L("Two examples gave the same y. That's a strong hint, but a few examples never prove always. So let's see why it's "
        "always two.", show(f3y4, 'a few examples never prove always'))),
    S('Method 2 · The math way',
      L('Now the math way. On the left, both terms contain y. We can write x y plus five y as y times the sum x plus five. Multiplying y by each part gives x y and five y again. On the right, both terms contain a factor of two. Two x plus ten is two times the sum x plus five. So both sides contain the same factor, x plus five.', show(f3y5, 'We can write x y plus five y')),
      L("x plus five is not zero, because x is not negative five. So we may divide both sides by it, and y is two, for "
        "every allowed x. Choice number two is our answer.", show(f3y6, 'x plus five is not zero'), show(f3y6b, 'and y is two'),
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Now you see why they gave the condition. If x were negative five, both sides would be zero, and y could be "
        "anything. [pause] Okay. I'll see you in the next question.", pt('stem: g1', 'why they gave the condition'))),
])


# ------------------------------------------------------------------------------------------------ V4: the bubble corner
# lesson right-column items start below the face bubble (top right, x 1344-1594, y 6-256); text lines wrap before it
for _it, _y in ((f3e1c, 300), (f3e1d, 365), (f3e1e, 430),
                (f3e2r1, 300), (f3e2r2, 360), (f3e2r3, 420), (f3e2r4, 480), (f3e2n, 540), (f3net, 620),
                (f3t4, 300), (f3t5, 360), (f3t6, 420), (f3t6b, 480), (f3t7, 540),
                (f3z3c, 300), (f3z3d, 360), (f3z3e, 420), (f3z3f, 480),
                (f3c3a, 300), (f3c3b, 360), (f3c3c, 420), (f3c4, 500), (f3c4b, 560)):
    _R(_it, _y, x=1010)
for _v in ('pt51-plug-numbers',):
    for _sl in VIDEOS[_v]['slides']:
        for _ln in _sl['lines']:
            for _c in _ln['cues']:
                if _c[0] == 'show' and _c[1]['k'] == 't' and _c[1]['_col'] == 0: _c[1]['w'] = 860

# f3c4 above is now the dress-discount reminder, not the earlier counterexample.
# Keep it with the price on the left, away from the choice calculations.
f3c4['_col'] = 0
f3c4.pop('_x', None)
f3c4.pop('_y', None)

# =================================================================================================================
# Topic-51 fragment f4 (TAG D, 2026-10-14): the lesson "Estimation" (camera, in 2 parts) and its sample questions
# pt-q16 ... pt-q19 (Hebrew: pt_src/seg4_estimation.txt, order-of-magnitude estimation).
#
# Hebrew moves kept (each at the question that shows it):
#   q16  shaded = sector - triangle; we don't look for the right answer, we rule out three; where is the pi (pi minus a
#        number); sometimes the pi is right in every choice, sometimes in one only; pi about 3; a negative area is out
#        (the exam hides the minus behind pi); the pizza (4 slices 90, 8 slices 45 -> one eighth); pi r^2 = 4 pi, the
#        sector pi / 2; peek at the choices instead of the triangle = "partial calculation"
#   q17  a fraction asked, no fractions in the choices -> get rid of the bottom; multiply by 1 (the partner), the
#        difference of squares; "if I don't know the trick" -> an approximate calculation, the choices are far enough
#        apart. Her sqrt2 = 1.4 / 14/34 -> 14/35 is a DECIMAL estimate (banned): replaced by whole-number benchmarks and
#        squaring (1 < sqrt2 < 1 1/2 because (1 1/2)^2 = 2 1/4); her "a close fraction that reduces nicely" is taught in
#        the lesson with whole numbers (29/59 -> 30/60).
#   q18  area = length x width, the height is given, the middle part needs a helper line + Pythagoras -> estimate it;
#        "figures need not be accurate?" - most are, and regular shapes are (one way to draw it, the ratios stay; a
#        whole lesson later); more than a radius, less than the diameter; the eraser; width between 6 and 8 -> area
#        between 24 and 32, not equal to either; 32 and 40 out. Her sqrt3 = 1.7 / sqrt2 = 1.4 replaced by: area / 16
#        must be more than 1 1/2, and sqrt2 < 1 1/2 (squaring). 2026-10-23 (Nitzan: "whatever the Hebrew version does"):
#        her figure estimate is Method 1 again (it had been replaced by "we shouldn't measure the sketch"); the helper
#        line + Pythagoras is Method 2, the math way, ending exactly (root 12 = 2 root 3); her "a whole lesson later"
#        is not promised.
#   q19  20% of 3.2 (10% = divide by 10); 3% of 2 is negligible -> "0.64 and a little more"; built on purpose to reward
#        whoever thinks; most students can do the 20%, the 3% takes time. Added: percent and concentration explained
#        on the spot (topic 23 is later), and the bound that makes "negligible" valid (3% < 10% of 2 = 0.2).
#   lesson (her summary at the end of q19): a new super-method; it saves time; it helps when we're stuck (a geometry
#        helper line we don't see, an expression we don't know how to start) -> in "When do I use it".
# Added (the teacher's "a bit more explanation" 2026-10-14): what order of magnitude means, why it works (the rounding
#   error is small, the choices are far apart; a size picture on a number line), the round benchmarks (10 x 10, 20^2,
#   30^2, pi between 3 and 4, a root between two whole roots, sqrt2 and sqrt3 against 1 1/2), three lesson examples (one
#   more than usual: a product, roots on a number line, fractions), "when do I use it" (choices far apart, a long
#   calculation or stuck, "about" / "closest to"), and the trap (close choices -> the last digit), a one-line reminder of
#   the cylinder in the cube (pt-q04).
# =================================================================================================================
FIG_LEFT.update({'solve-pt-q16', 'solve-pt-q18'})

# ------------------------------------------------------------------------------------------------ pt51-estimation (lesson)
# Visuals: typed / hand-written board lines built at her words; two number lines (ZL) as the size picture: the choices
# of the first example ten times apart, and the roots example with the band between 14 and 16.
f4w1 = I('f4w1', 'Order of magnitude: $\\ $about $10$? $\\ 100$? $\\ 1{,}000$?', size=34)
f4w2 = I('f4w2', 'Rule out what is far too big or far too small', size=34)
f4w3 = I('f4w3', 'The cylinder in the cube: $\\ $three choices $>$ the whole cube ✗', size=30)
f4e1q = I('f4e1q', '$19\\cdot51=\\ ?$', size=38)
f4e1n = PIN(ZL('f4e1n', -0.5, 3.5, [
    ('ten', [('below', 0.5, '×10'), ('below', 1.5, '×10'), ('below', 2.5, '×10')]),
    ('est', [('pt', 1.0, 'about 1,000')]),
    ('x', [('cross', 0), ('cross', 2), ('cross', 3)]),
], ticks=((0, '96.9'), (1, '969'), (2, '9,690'), (3, '96,900')), w=900, title='The four choices, each ten times the one before'))
f4e1r = IH('f4e1r', '$20\\cdot50=1{,}000$', size=36)
f4e1s = I('f4e1s', 'About $1{,}000$ $\\to$ $\\ 969$ ✓', size=34)
f4e1w = I('f4e1w', 'Rounding error: a few tens. $\\ $Gaps between the choices: hundreds and more', size=30)
f4b1 = I('f4b1', '$10\\cdot10=100$, $\\quad 20^2=400$, $\\quad 30^2=900$', size=36)
f4b2 = I('f4b2', '$3<\\pi<4$ $\\quad\\to\\quad$ for an estimate, $\\ \\pi\\approx3$', size=36)
f4b3 = IH('f4b3', '$49<50<64$ $\\ \\to\\ $ $7<\\sqrt{50}<8$', size=36)
f4b4 = IH('f4b4', '$1<2<4$ $\\ \\to\\ $ $1<\\sqrt2<2$', size=36)
f4b5 = IH('f4b5', '$\\left(1\\frac12\\right)^2=2\\frac14$ $\\ \\to\\ $ $\\sqrt2<1\\frac12<\\sqrt3<2$', size=36)
f4e2q = I('f4e2q', 'Closest to $\\ \\sqrt{90}+\\sqrt{26}$? $\\quad$ Choices: $\\ 8,\\ \\ 11,\\ \\ 15,\\ \\ 25$', size=32)
f4e2a = IH('f4e2a', '$81<90<100$ $\\ \\to\\ $ $9<\\sqrt{90}<10$', size=34)
f4e2b = IH('f4e2b', '$25<26<36$ $\\ \\to\\ $ $5<\\sqrt{26}<6$', size=34)
f4e2c = IH('f4e2c', '$9+5=14$, $\\ 10+6=16$ $\\ \\to\\ $ between $14$ and $16$', size=34)
f4e2n = PIN(ZL('f4e2n', 0, 26, [
    ('ch', [('ink', 8, '8'), ('ink', 11, '11'), ('ink', 15, '15'), ('ink', 25, '25')]),
    ('band', [('shade', 14, 16)]),
    ('x', [('cross', 8), ('cross', 11), ('cross', 25)]),
    ('ok', [('below', 15, '✓ closest')]),
], ticks=(0, 5, 10, 15, 20, 25), w=900, title='The four choices and the band between 14 and 16'))
f4e2t = I('f4e2t', 'Trap: $\\ \\sqrt{90}+\\sqrt{26}\\ne\\sqrt{116}$', size=32)
f4e3q = I('f4e3q', 'Closest to $\\ \\frac{29}{59}+\\frac{39}{81}$? $\\quad$ Choices: $\\ \\frac{1}{10},\\ \\ \\frac12,\\ \\ 1,\\ \\ 2$', size=32)
f4e3a = IH('f4e3a', '$\\frac{29}{59}\\approx\\frac{30}{60}=\\frac12$', size=36)
f4e3b = IH('f4e3b', '$\\frac{39}{81}\\approx\\frac{40}{80}=\\frac12$', size=36)
f4e3c = I('f4e3c', '$\\frac12+\\frac12=1$ $\\ \\to\\ $ about $1$ ✓', size=36)
f4m1 = I('f4m1', '1. $\\ $The choices are far apart in size', size=34)
f4m2 = I('f4m2', '2. $\\ $The exact way is long, or I\'m stuck', size=34)
f4m3 = I('f4m3', '3. $\\ $"About", "approximately", "closest to"', size=34)
f4m4 = I('f4m4', 'Areas and volumes with $\\pi$ or roots in the choices', size=32)
f4t1 = I('f4t1', '$29\\cdot41=\\ ?$', size=36)
f4t1b = I('f4t1b', 'Choices: $\\ 1{,}189,\\ \\ 1{,}196,\\ \\ 1{,}204,\\ \\ 1{,}212$', size=32)
f4t2 = IH('f4t2', '$30\\cdot40=1200$ $\\ \\to\\ $ all four are close ✗', size=34)
f4t3 = IH('f4t3', 'Last digit: $\\ 9\\cdot1=9$ $\\ \\to\\ 1189$ ✓', size=34)
f4t4 = I('f4t4', 'Close choices: tighter bounds, calculate, or check the last digit', size=30)

video('pt51-estimation', 'lesson', slides=[
    S('Estimation',
      L("Psychometric thinking, order-of-magnitude estimation. It's a little less known than plugging in, but it works "
        "very well.")),
    # ------------------------------------------------------------------ part 1: what, why, the numbers we know
    S('What is it?',
      L("Order of magnitude means the rough size of a number. Is it about ten, about a hundred, or about a thousand? In "
        "an estimate, we don't calculate the answer exactly. We only ask how big it must be, roughly.",
        show(f4w1, 'Order of magnitude means')),
      L("Then we don't look for the right choice. We rule out the choices that are far too big or far too small. When "
        "three choices are out, the fourth one is the answer.", show(f4w2, 'We rule out the choices')),
      L("We did it once already, with the cylinder inside the cube. The cylinder had to be smaller than the cube, and "
        "three choices were bigger than the whole cube.", show(f4w3, 'with the cylinder inside the cube'))),
    S('Why it works',
      L("Let's see why it works. How much is nineteen times fifty-one? The choices are ninety-six point nine, nine "
        "hundred sixty-nine, nine thousand six hundred ninety, and ninety-six thousand nine hundred.",
        show(f4e1q, 'How much is nineteen')),
      L("Let's put the choices on a line. Each one is ten times the one before it. So they're very far apart in size. Here we can use that difference in size instead of calculating the exact product.", show(f4e1n['line'], "Let's put the choices on a line"),
        show(f4e1n['ten'], 'Each one is ten times')),
      L("So let's round. Nineteen is almost twenty, and fifty-one is almost fifty. So we need twenty times fifty. Two times "
        "five is ten, and then we add the two zeros. That's a thousand.", show(f4e1r, 'So we need twenty times fifty')),
      L("So the answer is about a thousand. On the line, only nine hundred sixty-nine is near a thousand. The other choices are ten times smaller, or ten times bigger, so they're out. The answer is nine hundred sixty-nine, and we never did the exact multiplication.", show(f4e1n['est'], 'So the answer is about a thousand'),
        show(f4e1n['x'], 'The other choices'), show(f4e1s, 'The answer is nine hundred')),
      L("That's why it works. Here, rounding changes the result by only a little, a few tens. But the choices are hundreds and thousands apart, so a small mistake can't move us to another choice.", show(f4e1w, "That's why it works"))),
    S('Numbers we know',
      L("To estimate, we use round numbers that we know by heart. Ten times ten is a hundred. Twenty squared is four "
        "hundred, and thirty squared is nine hundred.", show(f4b1, 'Ten times ten')),
      L("Pi is a bit more than three, and less than four. For an estimate, three is usually enough.",
        show(f4b2, 'Pi is a bit more than three')),
      L("A root that isn't a whole number sits between two whole numbers. Root fifty is between seven and eight, because "
        "seven squared is forty-nine and eight squared is sixty-four. We met this in the roots topic.",
        show(f4b3, 'Root fifty is between')),
      L("Root two is between one and two, because one squared is one, and two squared is four.",
        show(f4b4, 'Root two is between one and two')),
      L("And when we need a bit more, we use one and a half. One and a half squared is two and a quarter. That's more "
        "than two, so root two is less than one and a half. And two and a quarter is less than three, so root three is "
        "more than one and a half, but less than two.", show(f4b5, 'One and a half squared')),
      L("So we never need the digits of root two. We only need to know which two numbers it's between.")),
    # ------------------------------------------------------------------ part 2: two more examples, when, the trap
    S('Roots on a line',
      L("Now let's use these numbers. Which number is closest to root ninety plus root twenty-six? The choices are eight, "
        "eleven, fifteen and twenty-five.", show(f4e2q, 'Which number is closest')),
      L("Root ninety first. Ninety is between eighty-one and a hundred, so root ninety is between nine and ten.",
        show(f4e2a, 'Ninety is between')),
      L("Now root twenty-six. Twenty-six is between twenty-five and thirty-six, so root twenty-six is between five and "
        "six.", show(f4e2b, 'Twenty-six is between')),
      L('Each root is bigger than its lower bound. So their sum is bigger than nine plus five, fourteen. Each root is also smaller than its upper bound. So the sum is smaller than ten plus six, sixteen. The sum is strictly between fourteen and sixteen.', show(f4e2c, 'So their sum is bigger')),
      L("Here it is on a number line, with the four choices. Our sum is somewhere in this band, between fourteen and "
        "sixteen.", show(f4e2n['line'], 'Here it is on a number line'), show(f4e2n['ch'], 'with the four choices'),
        show(f4e2n['band'], 'Our sum is somewhere')),
      L("Eight, eleven and twenty-five are far from the band, so they're out. Fifteen is right in the middle of it. So "
        "fifteen is the closest, and we never found either root exactly.", show(f4e2n['x'], 'are far from the band'),
        show(f4e2n['ok'], 'Fifteen is right in the middle')),
      L("And watch out for eleven. Some students add under the root, ninety plus twenty-six, and take the root of a "
        "hundred sixteen. That's between ten and eleven. But roots don't add like that, so eleven is a trap.",
        show(f4e2t, 'Some students add under the root'))),
    S('A nicer fraction',
      L("One more example, with fractions. Which number is closest to twenty-nine over fifty-nine, plus thirty-nine over "
        "eighty-one? The choices are one tenth, a half, one, and two.", show(f4e3q, 'One more example')),
      L("Twenty-nine over fifty-nine doesn't reduce nicely. So we look for a close fraction that does. Twenty-nine is "
        "almost thirty, and fifty-nine is almost sixty. Thirty over sixty is a half.",
        show(f4e3a, 'Twenty-nine is almost thirty')),
      L("In the same way, thirty-nine over eighty-one is close to forty over eighty. That's also a half.",
        show(f4e3b, 'thirty-nine over eighty-one is close')),
      L("A half plus a half is one. Each fraction is a little less than a half, so the sum is a little less than one. "
        "But it's much closer to one than to a half or to two. So the answer is one.",
        show(f4e3c, 'A half plus a half is one'))),
    S('When do I use it?',
      L("So when do I estimate? The first sign is the choices. They're far apart in size. One is ten times another, or "
        "some are clearly too big or too small.", show(f4m1, 'The first sign')),
      L("The second sign. The exact way is a long calculation, or I'm stuck. For example, a geometry question where I "
        "don't see the helper line, or an expression where I don't know where to start.",
        show(f4m2, 'The second sign')),
      L("The third sign is in the words. When the question says about, approximately, or which number is closest to, "
        "it's asking for an estimate.", show(f4m3, 'The third sign')),
      L("And estimates are very strong in areas and volumes, when the choices have pi or roots in them. We'll see that "
        "in the next questions.", show(f4m4, 'in areas and volumes'))),
    S('The trap: close choices',
      L("Now the trap. A rough estimate may not separate close choices. Look at twenty-nine times forty-one. The "
        "choices are one thousand one hundred eighty-nine, one thousand one hundred ninety-six, one thousand two hundred "
        "four, and one thousand two hundred twelve.", show(f4t1, 'Look at twenty-nine times'), show(f4t1b, 'The choices are one thousand')),
      L("Thirty times forty is twelve hundred. But all four choices are close to twelve hundred, so the estimate can't "
        "choose. If I just mark the choice nearest to twelve hundred, I'll mark a wrong one.",
        show(f4t2, 'Thirty times forty is twelve hundred')),
      L("When the choices are close, use another tool. Here the last digit works. Nine times one is nine, so the answer "
        "ends in nine. Only one thousand one hundred eighty-nine ends in nine.", show(f4t3, 'Here the last digit works')),
      L("So before you estimate, look at the choices. If they're far apart, a rough estimate may be enough. "
        "Close choices need tighter bounds, an exact calculation, or another check, like the last digit. "
        "[pause] Okay. I'll see you in the next video.", show(f4t4, 'So before you estimate'))),
])

CAMERA_SPLITS = globals().get('CAMERA_SPLITS', []) + [
    ('pt51-estimation', 'Estimation', [
        (1, None),
        (4, "Let's continue with estimation, and use the numbers we know."),
    ]),
]


# ------------------------------------------------------------------------------------------------ pt-q16 (question figure)
# V3: the question figure on the left; our colour copy on the right (same orientation): the sector tinted teal when
# named, the right triangle orange; the "pi part minus a number" lines under it. Slide 2: the bound pi < 4 and the
# negative bracket. Slide 3 (partial calculation): a fresh copy, the pizza cut into 4 (dashed) and then 8, the slice
# marked one eighth, then the circle and sector areas.
# 2026-10-22 Hebrew restore (reviews/hebrew-vs-english-t51.md row 4b): slide 1 is her "where is the pi?" pattern (the pi
# is in the sector -> pi minus a number; (1) number minus pi and (3) pi over a number out before any numbers). It replaces
# the triangle area + the decimal bound 3 < pi < 3.2 (no decimal estimates); the triangle moved into method 2 as the check
# after the sector piece leaves only choice 4.
f4O = (230.0, 250.0)
f4A, f4B = gpt(*f4O, 170, 65), gpt(*f4O, 170, 20)


def f4_foot(P, Q, X):
    """the foot of the perpendicular from X to the line P-Q"""
    dx, dy = Q[0] - P[0], Q[1] - P[1]
    t = ((X[0] - P[0]) * dx + (X[1] - P[1]) * dy) / float(dx * dx + dy * dy)
    return P[0] + t * dx, P[1] + t * dy


f4F = f4_foot(f4O, f4B, f4A)
f4shade = 'M %.1f %.1f L %.1f %.1f A 170 170 0 0 0 %.1f %.1f Z' % (f4F[0], f4F[1], f4B[0], f4B[1], f4A[0], f4A[1])
f4base16 = [('circ', *f4O, 170), ('region', f4shade, 'ink', 0.16),
            ('seg', *f4O, *f4A), ('seg', *f4O, *f4B), ('seg', *f4A, *f4F),
            ('right', f4F[0], f4F[1], gdir(*f4F, *f4O), gdir(*f4F, *f4A), 14, 'ink'),
            ('arc', *f4O, 40, 20, 65, 'ink', '45°', 66), ('dot', *f4O),
            ('txt', f4O[0], f4O[1] + 24, 'O', 'ink', 24, True), ('txt', f4A[0] - 6, f4A[1] - 20, 'A', 'ink', 24, True),
            ('txt', f4B[0] + 18, f4B[1] + 4, 'B', 'ink', 24, True), ('txt', 236, 172, '2', 'ink', 24)]
f4g16 = PIN(GEO('f4g16', [
    ('line', f4base16),
    ('sec', [('wedge', *f4O, 170, 20, 65, 'teal')]),
    ('tri', [('tint', [f4O, f4F, f4A], 'orange'), ('seg', *f4O, *f4F, 'orange', 4), ('seg', *f4F, *f4A, 'orange', 4),
             ('seg', *f4A, *f4O, 'orange', 4)]),
], vb='40 60 380 380', w=200, title='Sector AOB and the right triangle inside it'))
_R(f4g16, 330)
f4h0 = I('f4h0', 'Shaded $=$ sector $-$ triangle', size=26, col=1)
f4h1 = IH('f4h1', 'Equal leg squares: $2+2=4$', size=28, col=1)
f4h3 = IH('f4h3', 'Triangle: $\\frac{2}{2}=1$', size=28, col=1)
f4sector = IH('f4sector', 'Sector: $\\frac18\\cdot4\\pi=\\frac\\pi2$', size=28, col=1)
# 2026-10-22 Hebrew restore: her "where is the pi?" pattern replaces the decimal bound 3 < pi < 3.2 (no decimal estimates)
f4w1 = I('f4w1', 'Where is the $\\pi$? $\\ $In the sector', size=30, col=1)
f4w2 = I('f4w2', 'Pattern: $\\ \\pi$ (with a fraction) $-$ a number', size=29, col=1)
f4w3 = IH('f4w3', '(1) $\\ 4-\\pi$: $\\ $a number $-\\ \\pi$, no', size=29, col=1)
f4w4 = IH('f4w4', '(3) $\\ \\frac{\\pi}{\\sqrt2}$: $\\ $nothing taken away, no', size=29, col=1)
f4w5 = IH('f4w5', '(2) $\\ \\frac{\\pi}{4}-1$ $\\quad$ (4) $\\ \\frac{\\pi}{2}-1$', size=29, col=1)
f4n0 = I('f4n0', 'So far: $\\ $(1), (3) out', size=26, col=1)
f4n1 = IH('f4n1', '$3<\\pi<4$', size=32, col=1)
f4n2 = IH('f4n2', '$\\pi<4$ $\\ \\to\\ $ $\\frac{\\pi}{2}<2$', size=32, col=1)
f4n3 = IH('f4n3', '$\\frac{\\pi}{2}-2<0$ $\\ \\to\\ $ (2) is negative ✗', size=30, col=1)
f4n4 = I('f4n4', 'An area can\'t be negative', size=28, col=1)
f4g16b = PIN(GEO('f4g16b', [
    ('line', [('circ', *f4O, 170), ('wedge', *f4O, 170, 20, 65, 'teal'), ('seg', *f4O, *f4A), ('seg', *f4O, *f4B),
              ('arc', *f4O, 40, 20, 65, 'ink', '45°', 66), ('dot', *f4O),
              ('txt', f4O[0], f4O[1] + 24, 'O', 'ink', 24, True), ('txt', f4A[0] - 6, f4A[1] - 20, 'A', 'ink', 24, True),
              ('txt', f4B[0] + 18, f4B[1] + 4, 'B', 'ink', 24, True)]),
    ('q', [('seg', *f4O, *gpt(*f4O, 170, a), 'teal', 2.5, True) for a in (110, 200, 290)]),
    ('e', [('seg', *f4O, *gpt(*f4O, 170, a), 'teal', 2.5, True) for a in (155, 245, 335)]
          + [('txt', *gpt(*f4O, 118, 42.5), '1/8', 'teal', 26)]),
], vb='40 60 380 380', w=190, title='The circle cut into eight equal slices'))
_R(f4g16b, 360)
f4p1 = IH('f4p1', 'Circle: $\\ \\pi\\cdot2^2=4\\pi$', size=32, col=1)
f4p2 = IH('f4p2', 'Sector: $\\ \\frac{4\\pi}{8}=\\frac{\\pi}{2}$', size=32, col=1)
f4p3 = IH('f4p3', 'Shaded $=\\frac{\\pi}{2}-1$', size=28, col=1)
for _it, _y in ((f4n0, 330), (f4n1, 390), (f4n2, 450), (f4n3, 520), (f4n4, 590)):
    _R(_it, _y)
for _it, _y, _x in ((f4p1, 380, 1250), (f4p2, 440, 1250),
                     (f4h1, 545, 1040), (f4h3, 595, 1040), (f4p3, 650, 1040)):
    _R(_it, _y, x=_x)
for _it, _yy in ((f4h0, 330), (f4w1, 378), (f4w2, 426), (f4w3, 474), (f4w4, 526), (f4w5, 590)):
    _R(_it, _yy)

video('solve-pt-q16', 'solution', qid='pt-q16', slides=[
    SM('Method 1 · Estimation', 'Where is the π?',
      L("A O B is a sector of a circle with center O and a radius of two centimeters. Based on this and the figure, what "
        "is the area of the shaded region, in square centimeters?", pt('stem', 'A O B is a sector', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("The shaded region is the sector, minus the right triangle inside it. So shaded equals sector minus triangle. "
        "[short pause] We'll solve it two ways, by estimating the choices, and then with a partial calculation.",
        show(f4h0, 'So shaded equals')),
      L("Let's start with estimation, before any numbers. First we look at the pattern of the calculation, and ask, "
        "where is the pi?", show(f4w1, 'where is the pi')),
      L("The pi is in the sector. The sector is part of the circle, and the circle's area is pi r squared. "
        "For this triangle, Pythagoras gives the side lengths without using pi. So its area has no pi term. "
        "So sector minus triangle gives the pattern pi minus a number. "
        "The pi can come with a fraction, like pi over two. But it comes first, and a number is taken away from it.",
        pt('f4w1', 'The pi is in the sector'), show(f4w2, 'gives the pattern pi minus a number')),
      L("Choice number one says four minus pi. That's a number minus pi, the opposite pattern. Here the pi is the part "
        "taken away, so choice number one is out.", show(f4w3, 'the opposite pattern'), mk('cross', 'choice 1', 'so choice number one is out')),
      L("Choice number three says pi over root two. That's pi divided by a number, and nothing is taken away. The "
        "triangle is missing, so choice number three is out too.", show(f4w4, 'nothing is taken away'),
        mk('cross', 'choice 3', 'so choice number three is out too')),
      L("Choice number two says one half, times pi over two minus two. The half multiplies both parts, so it's pi over "
        "four, minus one. Choice number four says pi over two, minus one. Both have the pattern pi minus a number, so "
        "this test can't split them.", show(f4w5, "so it's pi over"), pt('f4w5', 'Choice number four says')),
      L("Sometimes the pattern rules out three choices, and sometimes none. Here it ruled out two, in seconds. And it "
        "works only because we know which part has the pi: here, the sector.")),
    SM('Method 1 · Estimation', 'A negative area?',
      L("[pause] Two choices are left. Now let's estimate their size. Pi is a bit more than three, and less than four.",
        show(f4n0, 'Two choices are left'), show(f4n1, 'Pi is a bit more than three')),
      L("Look at choice number two. Inside the bracket, we have pi over two, minus two. Pi is less than four, so pi over "
        "two is less than four over two, which is two.", show(f4n2, 'Pi is less than four')),
      L("If we take two away from something less than two, we get a negative number. And half of a negative number is still negative. So choice "
        "number two is a negative number.", show(f4n3, 'If we take two away')),
      L("But an area can't be negative, so choice number two is out. The exam won't write minus five. It hides the minus "
        "behind the pi, and an estimate shows it at once.", show(f4n4, "But an area can't be negative"),
        mk('cross', 'choice 2', 'so choice number two is out')),
      L("Three choices are out, so choice number four is our answer.",
        mk('tick', 'choice 4', 'so choice number four is our answer'))),
    SM('Method 2 · The math way: partial calculation', 'Partial calculation',
      L("[pause] Now a second way, the math way, for whoever wants to calculate. Even then, we don't have to calculate everything. "
        "Let's find only the sector.", show(f4g16b['line'], 'Now a second way')),
      L("What part of the circle is the sector? Think of a pizza. If we cut it into four slices, each slice has ninety "
        "degrees. If we cut it into eight, each slice has forty-five degrees.", show(f4g16b['q'], 'into four slices'),
        show(f4g16b['e'], 'If we cut it into eight')),
      L("Our angle is forty-five degrees, so the sector is one of eight equal slices. It's one eighth of the circle.",
        pt('f4g16b_line', 'Our angle is forty-five')),
      L("The area of the circle is pi r squared. The radius is two, and two squared is four, so the circle is four pi. "
        "One eighth of four pi is four pi over eight, which is pi over two.", show(f4p1, 'The area of the circle'),
        show(f4p2, 'One eighth of four pi')),
      L("Now let's peek at the choices. Which of them has the sector, pi over two? Choice number four, pi over two minus "
        "one, has it. Choice number two has a half outside. The half multiplies the pi over two too, so it gives pi over "
        "four. That's not our sector, so choice number two is out.", mk('cross', 'choice 2', 'so choice number two is out')),
      L("Choice number one has minus pi, and choice number three has pi over root two. Those two don't have pi over two at all. So the "
        "sector alone leaves only choice number four. To be sure, let's check the other piece, the triangle."),
      L("The triangle has a right angle and an angle of forty-five degrees. So its third angle is forty-five too, and its "
        "legs are equal. The hypotenuse is the radius, two. By Pythagoras, the two equal legs squared add up to four. So "
        "each leg squared is two.", show(f4h1, 'each leg squared is two')),
      L("The triangle's area is leg times leg, divided by two. The legs are equal, so leg times leg is a leg squared, two. "
        "Two divided by two is one. So the shaded area is pi over two minus one. That's exactly choice number four, our "
        "answer.", show(f4h3, 'Two divided by two is one'), show(f4p3, 'pi over two minus one'),
        mk('tick', 'choice 4', "That's exactly choice number four")),
      L("This is a partial calculation: find a useful piece, then look at the choices. Here the sector alone ruled out "
        "every choice but one. I'll see you in the next question.")),
])


# ------------------------------------------------------------------------------------------------ pt-q17
# Visuals: the algebra in hand-written lines (the partner, the bottom, the top, divide by two); the estimate: the
# benchmarks of root two (squaring), then each check in its own row with its mark (right column).
f4a1 = IH('f4a1', '$\\frac{\\sqrt2}{2+\\sqrt2}\\cdot\\frac{2-\\sqrt2}{2-\\sqrt2}$', size=34)
f4a2 = IH('f4a2', 'Bottom: $\\ (2+\\sqrt2)(2-\\sqrt2)=4-2=2$', size=32)
f4a3 = IH('f4a3', 'Top: $\\ \\sqrt2(2-\\sqrt2)=2\\sqrt2-2$', size=32)
f4a4 = IH('f4a4', '$\\frac{2\\sqrt2-2}{2}=\\sqrt2-1$', size=34)
f4c1 = IH('f4c1', '$1<\\sqrt2<2$', size=32)
f4c2 = IH('f4c2', '$1<\\sqrt2<1\\frac12$', size=32)
f4c3 = I('f4c3', 'Bottom $>$ top $\\ \\to\\ $ fraction $<1$', size=32)
f4c4 = I('f4c4', '(2) $\\ 2\\sqrt2>2$ ✗ $\\qquad$ (3) $\\ \\sqrt2+1>2$ ✗', size=28, col=1)
f4c5 = I('f4c5', '(4) $\\ \\sqrt2-1<\\frac12$', size=28, col=1)
f4c6 = I('f4c6', '(1) $\\ (\\sqrt2-1)^2<\\frac14$', size=28, col=1)
f4c7 = I('f4c7', 'Top $>1$, bottom $<4$ $\\to$ $>\\frac14$', size=28, col=1)
f4c8 = I('f4c8', '(1) ✗ $\\ \\to\\ $ (4) ✓', size=28, col=1)
for _it, _y in ((f4c4, 290), (f4c5, 345), (f4c6, 400), (f4c7, 455), (f4c8, 510)):
    _R(_it, _y)

video('solve-pt-q17', 'solution', qid='pt-q17', slides=[
    S('Method 1 · The math way',
      L("Root two, over the bracket two plus root two. What does it equal?", pt('stem', 'Root two, over the bracket',
                                                                                 'hl', 4.0), voice='calm', pause=0.5),
      L("It's a fraction with a root on the bottom, and none of the choices is a fraction. So we need to get rid of the "
        "bottom. [short pause] We'll solve it two ways, the math way, with algebra, and then with an estimate."),
      L("In the roots topic we learned how. When the bottom is a sum with a root, we multiply the top and the bottom by its partner, called the conjugate. The partner of two plus root two is two minus root two. The top and the bottom are multiplied by the same thing, so it's like multiplying by one, and the value doesn't change.",
        show(f4a1, 'we multiply the top and the bottom')),
      L("Why the partner? On the bottom we get two plus root two, times two minus root two. That's the difference of "
        "squares, a squared minus b squared. Two squared is four, and root two squared is two. Four minus two is two, "
        "so the root is gone.", show(f4a2, 'On the bottom we get')),
      L("On the top, root two times two is two root two. And root two times root two is two. So the top is two root two "
        "minus two.", show(f4a3, 'On the top')),
      L("So we have two root two minus two, over two. We divide each part by two, and we get root two minus one. Choice "
        "number four is our answer.", show(f4a4, 'We divide each part by two'),
        mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Many students don't think of the partner here, and they get stuck. That's exactly when an estimate helps.")),
    S('Method 2 · Estimation',
      L("[pause] Now the estimate. We don't need root two exactly. We only need to know between which numbers it is."),
      L("From the estimate we learned, root two is between one and two.",
        show(f4c1, 'root two is between one and two')),
      L("We also narrowed that down: root two is between one and one and a half. We'll use these bounds to compare "
        "the choices.", show(f4c2, 'root two is between one and one and a half')),
      L("Now the size of our fraction. The bottom is the top plus two, so the bottom is bigger than the top. That means "
        "the fraction is less than one.", show(f4c3, 'The bottom is the top plus two')),
      L("Choice number two, two root two, is more than two, because root two is more than one. Choice number three, root "
        "two plus one, is also more than two. Both are more than one, so both are out.",
        show(f4c4, 'Choice number two, two root two'), mk('cross', 'choice 2', 'is more than two, because'),
        mk('cross', 'choice 3', 'so both are out')),
      L("Two choices are left. Choice number four, root two minus one, is less than a half, because root two is less "
        "than one and a half.", show(f4c5, 'Choice number four, root two minus one')),
      L('Choice number one is root two minus one, squared. Root two is between one and one and a half. So root two minus one is positive and less than a half. A half squared is a quarter. Squaring a smaller positive number gives less than a quarter. So choice number one is less than a quarter.', show(f4c6, 'Choice number one is root two')),
      L("So is our fraction more than a quarter? The top, root two, is more than one. The bottom, two plus root two, is "
        "less than two plus two, which is four. A bigger top and a smaller bottom both make a fraction bigger. So the "
        "fraction is more than one over four, a quarter.", show(f4c7, 'The top, root two, is more than one')),
      L("So choice number one is out, because it's less than a quarter. Choice number four is our answer again. [pause] "
        "Okay. I'll see you in the next question.", show(f4c8, 'So choice number one is out'),
        mk('cross', 'choice 1', "because it's less than a quarter"), mk('tick', 'choice 4', 'Choice number four is our answer again'))),
])


# ------------------------------------------------------------------------------------------------ pt-q18 (question figure)
# V3: the question figure on the left; our colour copy on the right: the two radii on side AD teal (2 and 2), the middle
# part orange with "?". Slide 2: a fresh copy; the middle part copied under the rectangle and compared with a radius bar
# (teal, 2) and with the dashed diameter of circle O + a bar of 4 (ink); then the width and area lines. Slide 3: the
# choices, each in its own row, with the carried range.
f4rect = [('seg', 110, 60, 421.8, 60), ('seg', 421.8, 60, 421.8, 240), ('seg', 421.8, 240, 110, 240),
          ('seg', 110, 240, 110, 60),
          ('arc', 110, 60, 90, 270, 360, 'ink'), ('arc', 421.8, 60, 90, 180, 270, 'ink'),
          ('arc', 110, 240, 90, 0, 90, 'ink'), ('arc', 421.8, 240, 90, 90, 180, 'ink'),
          ('circ', 265.9, 150, 90), ('dot', 265.9, 150), ('txt', 270, 172, 'O', 'ink', 22, True),
          ('txt', 96, 44, 'A', 'ink', 24, True), ('txt', 436, 44, 'D', 'ink', 24, True),
          ('txt', 96, 258, 'B', 'ink', 24, True), ('txt', 436, 258, 'C', 'ink', 24, True),
          ('txt', 82, 150, '4', 'ink', 26)]
f4r2 = [('seg', 110, 60, 200, 60, 'teal', 6), ('seg', 331.8, 60, 421.8, 60, 'teal', 6),
        ('txt', 155, 40, '2', 'teal', 26), ('txt', 376.8, 40, '2', 'teal', 26)]
f4mid = [('seg', 200, 60, 331.8, 60, 'orange', 6), ('txt', 265.9, 40, '?', 'orange', 28)]
f4g18 = PIN(GEO('f4g18', [
    ('line', f4rect),
    ('r', f4r2),
    ('mid', f4mid),
], vb='40 15 430 260', w=300, title='Rectangle ABCD with the parts of side AD'))
_R(f4g18, 330)
f4g18b = PIN(GEO('f4g18b', [
    ('line', f4rect + f4r2 + f4mid),
    ('c1', [('seg', 200, 280, 331.8, 280, 'orange', 6), ('txt', 180, 282, '?', 'orange', 26),
            ('seg', 200, 308, 290, 308, 'teal', 6), ('txt', 180, 310, '2', 'teal', 26)]),
    ('c2', [('seg', 175.9, 150, 355.9, 150, 'teal', 2.5, True),
            ('seg', 200, 336, 380, 336, 'ink', 6), ('txt', 180, 338, '4', 'ink', 26)]),
], vb='40 15 430 340', w=300, title='The middle part compared with a radius and a diameter'))
_R(f4g18b, 330)
f4s1 = IH('f4s1', '$AO=2+2=4$, $\\ AH=2$', size=28, col=1)
f4s2 = IH('f4s2', '$x^2=4^2-2^2=16-4=12$', size=28, col=1)
f4u1 = IH('f4u1', '$3^2<12<4^2\\quad\\to\\quad3<x<4$', size=28, col=1)
f4u2 = IH('f4u2', '$AD=x+x=2x$', size=30, col=1)
f4u2b = IH('f4u2b', '$6<AD<8$', size=30, col=1)
f4u3 = IH('f4u3', '$4\\cdot6=24$, $\\ 4\\cdot8=32$ $\\ \\to\\ $ $24<$ area $<32$', size=28, col=1)
f4k0 = I('f4k0', 'So far: $\\ 24<$ area $<32$', size=26, col=1)
f4k1 = I('f4k1', '(4) $\\ 40>32$ ✗', size=30, col=1)
f4k2 = I('f4k2', '(3) $\\ 32$: $\\ $the area is less than $32$ ✗', size=30, col=1)
f4k3 = IH('f4k3', '(2) $\\ 16\\cdot1\\frac12=24$', size=30, col=1)
f4k4 = IH('f4k4', '$\\left(1\\frac12\\right)^2=2\\frac14>2$ $\\to$ $\\sqrt2<1\\frac12$', size=30, col=1)
f4k5 = I('f4k5', '$\\to\\ 16\\sqrt2<24$ ✗', size=30, col=1)
f4k6 = I('f4k6', 'Three out $\\to$ (1) $\\ 16\\sqrt3$ ✓', size=30, col=1)
for _it, _y in ((f4s1, 560), (f4s2, 610), (f4u1, 595), (f4u2, 645), (f4u2b, 695), (f4u3, 745)):
    _R(_it, _y)
for _it, _y in ((f4k0, 330), (f4k1, 390), (f4k2, 450), (f4k3, 510), (f4k4, 570), (f4k5, 630), (f4k6, 695)):
    _R(_it, _y)
f4helperbase = f4rect
f4helpertriangle = [('dot', 110, 150), ('txt', 94, 150, 'H', 'ink', 22, True), ('seg', 110, 60, 265.9, 150, 'teal', 3, True),
    ('seg', 110, 150, 265.9, 150, 'teal', 3, True),
    ('right', 110, 150, 0, 270, 12), ('txt', 178, 85, '4', 'teal', 24),
    ('txt', 129, 110, '2', 'teal', 24), ('txt', 183, 170, 'x', 'teal', 24, True)]
f4helperother = [('seg', 265.9, 150, 421.8, 150, 'orange', 3, True),
    ('seg', 265.9, 150, 421.8, 60, 'orange', 3, True),
    ('right', 421.8, 150, 180, 270, 12), ('txt', 346, 85, '4', 'orange', 24),
    ('txt', 403, 110, '2', 'orange', 24), ('txt', 343, 170, 'x', 'orange', 24, True)]
f4help = PIN(GEO('f4help', [('line', f4helperbase),
    ('radii', [('seg', 265.9, 60, 265.9, 240, 'teal', 2, True), ('txt', 281, 110, '2', 'teal', 22), ('txt', 281, 200, '2', 'teal', 22)]),
    ('triangle', f4helpertriangle)], vb='40 15 430 260', w=300, title='Use the given lengths, not measurements'))
f4help2 = PIN(GEO('f4help2', [('line', f4helperbase+f4helpertriangle), ('other', f4helperother)],
    vb='40 15 430 260', w=300, title='Two equal horizontal lengths'))
_R(f4help, 330); _R(f4help2, 330)
f4help['line']['over'] = 1
f4help['line']['of'] = f4g18['line']['_name']
for _key in ('radii', 'triangle'):
    f4help[_key]['of'] = f4g18['line']['_name']
# The original question remains at the left; the helper copy replaces the old measured-length comparison.
# 2026-10-23 (Nitzan: "whatever the Hebrew version does"): her estimate from the figure is Method 1 again, with her
# accuracy rule (not necessarily drawn to scale, but most figures are accurate; regular shapes are; the eraser); the
# helper line + Pythagoras is Method 2, the math way, finished exactly (root 12 = 2 root 3 -> 16 root 3).
f4a1 = I('f4a1', 'Most exam figures are accurate', size=26, col=1)
f4a2 = I('f4a2', 'Regular shapes are accurate:', size=26, col=1)
f4a3 = I('f4a3', 'square, circle, equilateral triangle, cube', size=26, col=1)
f4e1 = IH('f4e1', '$2<$ middle part $<4$', size=26, col=1)
f4e2 = IH('f4e2', '$AD=2+$ middle part $+2$', size=26, col=1)
f4exact1 = IH('f4exact1', '$x^2=12\\quad\\to\\quad x=\\sqrt{12}$', size=30, col=1)
f4exact2 = IH('f4exact2', '$\\sqrt{12}=\\sqrt{4\\times3}=2\\sqrt3$', size=30, col=1)
f4exact3 = IH('f4exact3', '$AD=2x=4\\sqrt3$', size=30, col=1)
f4exact4 = IH('f4exact4', 'Area $=4\\times4\\sqrt3=16\\sqrt3$', size=30, col=1)
for _it, _y in ((f4a1, 560), (f4a2, 605), (f4a3, 650)):
    _R(_it, _y)
for _it, _y in ((f4e1, 590), (f4e2, 635), (f4u2b, 680), (f4u3, 725)):
    _R(_it, _y)
for _it, _yy in ((f4s2, 560), (f4u2, 610)):
    _R(_it, _yy)
for _it, _yy in ((f4exact1, 330), (f4exact2, 390), (f4exact3, 450), (f4exact4, 510)):     # their own slide, no figure
    _R(_it, _yy)

video('solve-pt-q18', 'solution', qid='pt-q18', slides=[
    SM('Method 1 · Estimation', 'The width is the problem',
      L("In the figure, each vertex of rectangle A B C D is the center of a circle with a radius of two centimeters. "
        "Point O is the center of a circle that is tangent to the four quarter circles, and to sides A D and B C. What "
        "is the area of rectangle A B C D, in square centimeters?", pt('stem', 'In the figure', 'hl', 10.0),
        voice='calm', pause=0.5),
      L("The area of a rectangle is length times width. The short side, A B, is four, and it's written in the figure. "
        "So we need the long side, A D.", show(f4g18['line'], 'The area of a rectangle')),
      L("Along A D, the first part is a radius of the quarter circle at A, so it's two. The last part is a radius of the "
        "quarter circle at D, so it's also two.", show(f4g18['r'], 'the first part is a radius')),
      L("We'll solve it in two different ways. Let's start with estimation. To calculate that middle part exactly, we'd "
        "need a helper line and Pythagoras. But what if we don't see the helper line? Then we estimate the middle part "
        "from the figure.", show(f4g18['mid'], 'that middle part')),
      L("But wait. On the exam, a figure is not necessarily drawn to scale. So how can we estimate from the figure?"),
      L("In most cases, we can tell. First, most figures on the exam are accurate. Second, a rule of thumb. Regular "
        "shapes are drawn accurately: a square, a circle, an equilateral triangle, a cube.",
        show(f4a1, 'most figures on the exam are accurate'), show(f4a2, 'Regular shapes are drawn accurately'),
        show(f4a3, 'a square, a circle')),
      L("Why? A regular shape can't be drawn any other way. Here we have circles, and the middle circle touches all "
        "four quarter circles. If we make the figure bigger or smaller, the ratios between the parts stay the same. So "
        "here we can estimate from the figure.")),
    SM('Method 1 · Estimation', 'Estimate the middle',
      L("Look at the middle part. It's longer than a radius of the corner circles, and that radius is two.",
        show(f4g18b['line'], 'Look at the middle part'), show(f4g18b['c1'], "It's longer than a radius")),
      L("And it's shorter than the diameter of the middle circle. That diameter goes from the top side to the bottom "
        "side, so it's four.", show(f4g18b['c2'], "it's shorter than the diameter")),
      L("Can't tell by eye? Use your eraser. Mark the length of the middle part on its edge. Then hold it against a "
        "radius, and against the diameter."),
      L("So the middle part is more than two and less than four. A D is made of three parts: two, the middle part, and "
        "two. Two plus two plus two is six, and two plus four plus two is eight. So A D is between six and eight.",
        show(f4e1, 'So the middle part is more than two'), show(f4e2, 'A D is made of three parts'),
        show(f4u2b, 'So A D is between six and eight')),
      L("The area is four times A D. Four times six is twenty-four, and four times eight is thirty-two. So the area is "
        "between twenty-four and thirty-two, and it isn't equal to either one.", show(f4u3, 'The area is four times'))),
    SM('Method 1 · Estimation', 'Check the choices',
      L("[pause] Now the choices. Choice number four, forty, is more than thirty-two. It's out.",
        show(f4k0, 'Now the choices'), show(f4k1, 'Choice number four, forty'), mk('cross', 'choice 4', "It's out")),
      L("Choice number three, thirty-two. The middle part is less than four, so the area is less than thirty-two. It's "
        "out too.", show(f4k2, 'Choice number three, thirty-two'), mk('cross', 'choice 3', "It's out too")),
      L("Choice number two, sixteen root two. The area has to be more than twenty-four. Sixteen times one and a half is sixteen plus eight, twenty-four. So to pass "
        "twenty-four, the root has to be more than one and a half.", show(f4k3, 'Sixteen times one and a half')),
      L("But one and a half squared is two and a quarter, which is more than two. So root two is less than one and a "
        "half, and sixteen root two is less than twenty-four. It's out.",
        show(f4k4, 'But one and a half squared'), show(f4k5, 'sixteen root two is less than twenty-four'),
        mk('cross', 'choice 2', "It's out")),
      L("Three choices are out, so choice number one, sixteen root three, is our answer.",
        show(f4k6, 'Three choices are out'), mk('tick', 'choice 1', 'so choice number one'))),
    SM('Method 2 · The math way: Pythagoras', 'A helper line',
      L("[pause] Now the math way. The estimate came from the figure. The math way uses only the given lengths, so it "
        "proves the answer. The middle circle touches the top and bottom sides, four apart. Its diameter is four, so its "
        "radius is two. Draw a line from A to O, joining two touching circles' centers.",
        show(f4help['line'], 'Now the math way'), show(f4help['radii'], 'Its diameter is four')),
      L('The corner circle has radius two, and the middle circle has radius two. The circles touch from the outside, so A O is two plus two, four. From O, draw a perpendicular to side A B. Call its foot H. O is two below the top side, so A H is two. Now A H O is a right triangle, with hypotenuse four and one leg two.', show(f4help['triangle'], 'A O is two plus two, four'), show(f4s1, 'hypotenuse four and one leg two'))),
    SM('Method 2 · The math way: Pythagoras', 'The exact width',
      L('Call O H x. By Pythagoras, x squared plus two squared is four squared. Four squared is sixteen, and two squared is four. Subtract four, and x squared is twelve.', show(f4help2['line'], 'Call O H x'), show(f4s2, 'x squared is twelve')),
      L("The same construction on the right has the same hypotenuse, four, and the same vertical leg, two. So its horizontal length is also x. The whole rectangle is x plus x across. That's why A D is two x, not just x.", show(f4help2['other'], 'same construction on the right'), show(f4u2, 'A D is two x'))),
    SM('Method 2 · The math way: Pythagoras', 'Finish exactly',
      L("Now x itself. x squared is twelve, so x is the root of twelve. Twelve is four times three. So the root of twelve "
        "is the root of four, times the root of three. That's two root three.",
        show(f4exact1, 'so x is the root of twelve'), show(f4exact2, "That's two root three")),
      L("A D is two x, so it's four root three. The other side is four. Four times four root three is sixteen root "
        "three. That's choice number one, just like the estimate. Choice number one is our answer, and I'll see you in "
        "the next question.", show(f4exact3, "so it's four root three"), show(f4exact4, 'Four times four root three'),
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])


# ------------------------------------------------------------------------------------------------ pt-q19
# Visuals: percent explained in one line; bottle A in hand-written lines (divide by ten, double); bottle B bounded by
# 10% of 2; the total bounded; each choice in one row with its mark (right column).
f4q1 = I('f4q1', '$20\\%$ $=20$ out of every $100$', size=32)
f4q2 = IH('f4q2', '$10\\%$ of $3.2$: $\\ 3.2\\div10=0.32$', size=32)
f4q3 = IH('f4q3', '$20\\%$ of $3.2$: $\\ 2\\cdot0.32=0.64$', size=32)
f4q4 = IH('f4q4', '$10\\%$ of $2=0.2$ $\\ \\to\\ $ $3\\%$ of $2<0.2$', size=30, col=1)
f4q5 = IH('f4q5', 'Total: $\\ 0.64+$ a little $\\ <0.84$', size=30, col=1)
f4q6 = I('f4q6', '(1) $\\ 0.7$ ✓ $\\quad$ (2) $\\ 0.95$ ✗', size=30, col=1)
f4q7 = I('f4q7', '(3) $\\ 1.24$ ✗ $\\quad$ (4) $\\ 3.1$ ✗', size=30, col=1)

video('solve-pt-q19', 'solution', qid='pt-q19', slides=[
    S('Bottle A',
      L("Bottle A contains three point two liters of a solution with an alcohol concentration of twenty percent. Bottle B "
        "contains two liters of a solution with an alcohol concentration of three percent. How many liters of alcohol "
        "are there in the two bottles together?", pt('stem', 'Bottle A contains', 'hl', 10.0), voice='calm', pause=0.5),
      L("An alcohol concentration of twenty percent means that twenty percent of the liquid is alcohol. Percent means out "
        "of a hundred. So in every hundred liters, twenty liters are alcohol.", show(f4q1, 'Percent means out of a hundred')),
      L("So we need twenty percent of three point two, and three percent of two. Then we add them."),
      L("Let's start with bottle A. Ten percent is one tenth, so we divide by ten. Three point two divided by ten is zero "
        "point three two.", show(f4q2, 'Ten percent is one tenth')),
      L("Twenty percent is twice ten percent. Two times zero point three two is zero point six four. So bottle A has zero "
        "point six four liters of alcohol.", show(f4q3, 'Twenty percent is twice'))),
    S('A tiny part',
      L("[pause] Now bottle B, three percent of two liters. Do we really need to calculate it? Let's first see how big it "
        "can be."),
      L("Ten percent of two is zero point two. Three percent is less than ten percent, so it's less than zero point two. "
        "It's a tiny amount.", show(f4q4, 'Ten percent of two')),
      L('We add the alcohol from the two bottles. Bottle A contributes zero point six four liters. Bottle B contributes a positive amount less than zero point two. So the total is more than zero point six four, but less than zero point eight four liters.', show(f4q5, 'So the total is more than')),
      L("Now the choices. Choice number one, zero point seven, is zero point six four and a little more, so it fits. "
        "Choice number two, zero point nine five, is more than zero point eight four, so it's out.",
        show(f4q6, 'Now the choices'), mk('cross', 'choice 2', 'so it\'s out')),
      L("Choice number three, one point two four, and choice number four, three point one, are even bigger. They're out "
        "too.", show(f4q7, 'Choice number three, one point two four'), mk('cross', 'choice 3', 'are even bigger'),
        mk('cross', 'choice 4', "They're out too")),
      L("Three choices are out, so choice number one, zero point seven, is our answer.",
        mk('tick', 'choice 1', 'so choice number one')),
      L("Most students can find twenty percent of three point two. The three percent takes longer, and it's easy to slip. "
        "But we didn't need it at all. The question is built that way on purpose, to reward whoever stops and sees that "
        "this part is tiny. [pause] Okay. I'll see you in the next question.")),
])
CARRY51.update({'solve-pt-q19': {1: ['Bottle A: $\\ 0.64$ liters']}})

# =================================================================================================== pt51-understanding (lesson)
# 2026-10-15 (teacher-approved, coordinator): the sixth core method of the one vocabulary (math_patches/_method_names.CORE),
# "Understanding" (her Hebrew הבנה / פתרון באמצעות הבנה, ~112x in her course; she uses it from absolute value on). Topic 51's
# Hebrew lessons don't name it, so this short camera lesson introduces it after the insight block: what it is, how it
# differs from an insight, three worked examples from topics taught BEFORE 51 (topic 1: the sign rules of
# multiplication, even = 2k / odd = 2k + 1, must / could / cannot; new numbers), when to use it, and where it comes back
# (absolute value, the number line, integers). V4: every given written when it is named, every step at its clause, the
# results only when they are said, the text column 860 wide (the face bubble, top right, stays clear).
u51d1 = I('u51d1', 'Understanding: $\\ $reason with rules we already know', size=34)
u51d2 = I('u51d2', 'signs · size · even and odd · order', size=32)
u51d3 = I('u51d3', 'no long calculation', size=32)
u51d4 = I('u51d4', 'e.g. $\\ $ends in $6$, squared $\\to$ ends in $6$', size=32)
u51a0 = I('u51a0', '$a<0,\\ \\ b>0$. $\\ $Which is necessarily negative?', size=34)
u51a1 = I('u51a1', '$a\\cdot b$: $\\ $different signs $\\to$ negative ✓', size=32)
u51a2 = I('u51a2', '$b-a=b+(\\text{a positive})$ $\\to$ positive ✗', size=32)
u51a3 = I('u51a3', '$a\\cdot a$: $\\ $same signs $\\to$ positive, $\\ $so $a^2\\cdot b$ is positive ✗', size=32)
u51a4 = I('u51a4', '$a+b$: $\\ $depends on which is bigger in size ✗', size=32)
u51b0 = I('u51b0', '$n$ is an integer. $\\ $Which is necessarily odd?', size=34)
u51b1 = I('u51b1', '$4n$ $=2\\cdot(2n)$ $\\to$ always even', size=32)
u51b2 = I('u51b2', '$4n+3$ $=$ even $+\\,3$ $\\to$ always odd ✓', size=32)
u51b3 = I('u51b3', '$n+3$: $\\ $depends on $n$ ✗', size=32)
u51c0 = I('u51c0', '$0<x<1$. $\\ $Which is bigger, $\\ x$ or $x^2$?', size=34)
u51c1 = I('u51c1', '$x^2=x\\cdot x$: $\\ x$ times a number smaller than $1$', size=32)
u51c2 = I('u51c2', '$\\to$ $x^2$ is smaller: $\\ x^2<x$', size=32)
u51c3 = I('u51c3', 'check: $\\ \\frac13\\cdot\\frac13=\\frac19<\\frac13$', size=32)
u51e1 = I('u51e1', 'Insight: $\\ $one idea for one question', size=32)
u51e2 = I('u51e2', 'Understanding: $\\ $general rules, again and again', size=32)
u51w1 = I('u51w1', 'When? $\\ $must / could / cannot be true', size=32)
u51w2 = I('u51w2', 'signs, $\\ $which is bigger, $\\ $even and odd, $\\ $order', size=32)
u51w3 = I('u51w3', 'Later: $\\ $absolute value, $\\ $the number line, $\\ $integers', size=32)
u51w4 = I('u51w4', 'Not sure the rule always holds? $\\ $Plug in numbers.', size=32)

video('pt51-understanding', 'lesson', slides=[
    S('Understanding',
      L('In psychometric thinking, we also solve by understanding.')),
    S('What is understanding?',
      L("We have one more way to solve, and we'll use it all through the course. We call it understanding.",
        show(u51d1, 'We call it understanding')),
      L("When we solve by understanding, we don't start with a long calculation. We use rules we already know about positive and negative numbers, size, even and odd numbers, and order. We check which rule fits the given conditions. Then we use it to decide what must be true.",
        show(u51d3, "we don't start with a long calculation"), show(u51d2, 'about positive and negative numbers')),
      L("You already used it in the very first question of this topic. When we square a number that ends in six, the result ends in six. That's a rule about the last digit, so we ruled out two choices without doing the full multiplication.", show(u51d4, 'When we square a number that ends in six'))),
    S('Example 1 · Signs',
      L("Here's the first example. a is negative and b is positive. Which of the following is necessarily negative?",
        show(u51a0, 'a is negative and b is positive')),
      L("Look at a times b. Remember the rule for multiplying: different signs give a negative. a is negative and b is "
        "positive, so a times b is always negative, for every a and b that fit.", show(u51a1, 'so a times b is always negative')),
      L("Why not the others? b minus a. Taking away any negative number is like adding its opposite, so b minus a is "
        "positive plus positive. It's positive.", show(u51a2, "It's positive.")),
      L("a squared times b. a times a has the same signs, so it's positive. And positive times positive b is positive.",
        show(u51a3, 'And positive times positive b')),
      L("And a plus b can be positive, negative, or zero. It depends on whether the positive amount or the negative amount has the bigger absolute value. The given conditions don't decide that. So a plus b isn't necessarily negative.", show(u51a4, "So a plus b isn't necessarily"))),
    S('Example 2 · Even and odd',
      L("The second example. n is an integer. Which is necessarily odd, four n plus three, or n plus three?",
        show(u51b0, 'n is an integer')),
      L("Four n is two times two n, and two times an integer is always even. That's the definition of even.",
        show(u51b1, 'is always even')),
      L("Even plus three is always odd, because even plus one is odd, and adding two more keeps it odd. So four n plus "
        "three is odd for every integer n.", show(u51b2, 'So four n plus')),
      L("But n plus three depends on n. If n is even, it's odd, and if n is odd, it's even. So it isn't necessarily odd.",
        show(u51b3, "So it isn't necessarily odd"))),
    S('Example 3 · Size',
      L("And the third example. x is between zero and one. Which is bigger, x, or x squared?",
        show(u51c0, 'x is between zero and one')),
      L("x squared is x times x. So it's x, times a number smaller than one.", show(u51c1, 'x squared is x times x')),
      L('When we multiply a positive number by a positive number smaller than one, we take only a part of it, so it gets smaller. So x squared is smaller than x.', show(u51c2, 'So x squared is smaller')),
      L("We can check with one number. A third times a third is a ninth, and a ninth is smaller than a third. The check "
        "agrees with the rule.", show(u51c3, 'and a ninth is smaller'))),
    S('Understanding or insight?',
      L("How is this different from an insight? With an insight, we notice something special in that question. There isn't one fixed procedure we can repeat for every insight question.", show(u51e1, 'With an insight')),
      L("Understanding uses general rules, the same ones again and again, in many questions. That's why it's worth "
        "learning as a method.", show(u51e2, 'Understanding uses general rules'))),
    S('When do I use it?',
      L("So when do we solve by understanding? When they ask what must be true, what could be true, or what cannot be "
        "true. And when the question is about signs, about which number is bigger, about even and odd, or about order.",
        show(u51w1, 'When they ask what must be true'), show(u51w2, 'And when the question is about signs')),
      L("Later in the course you'll use it a lot. Most questions on absolute value, on the number line and on integers are "
        "solved by understanding.", show(u51w3, "Later in the course you'll use it a lot")),
      L("And the trap. Use only a rule that's always true. If you're not sure, plug in numbers as a safety net. [pause] "
        "Okay. I'll see you in the next video.", show(u51w4, 'If you\'re not sure'))),
])
for _sl in VIDEOS['pt51-understanding']['slides']:
    for _ln in _sl['lines']:
        for _c in _ln['cues']:
            if _c[0] == 'show' and _c[1]['k'] == 't': _c[1]['w'] = 860
# a new course video (not in modulesV51.py): _t51_reading.py creates it in the Learn section, after the video named here
NEW_VIDEOS = {'pt51-understanding': ('solve-pt-q23', 'Understanding')}

# ------------------------------------------------------------------------------------------------ the flow order
# the course order of topic 51 (modulesV51.py / build_verbal flow): the insight block comes after the estimation block.
# Camera parts are inserted after their video later (tail.py, CAMERA_SPLITS), so only the base ids are listed here.
F9_FLOW = ['pt51-intro', 'solve-pt-q01', 'solve-pt-q02', 'solve-pt-q03', 'solve-pt-q04', 'solve-pt-q05', 'pt51-intro-wrap',
           'pt51-plug-answers', 'solve-pt-q06', 'solve-pt-q07', 'solve-pt-q08', 'solve-pt-q09',
           'pt51-plug-numbers', 'solve-pt-q10', 'solve-pt-q11', 'solve-pt-q12', 'solve-pt-q13', 'solve-pt-q14', 'solve-pt-q15',
           'solve-pt-q24', 'pt51-estimation', 'solve-pt-q16', 'solve-pt-q17', 'solve-pt-q18', 'solve-pt-q19',
           'pt51-insights', 'solve-pt-q20', 'solve-pt-q21', 'solve-pt-q22', 'solve-pt-q23', 'pt51-understanding']
assert sorted(F9_FLOW) == sorted(ORDER), (set(F9_FLOW) ^ set(ORDER))
ORDER[:] = F9_FLOW

# carry-over boxes on the continuation slides (V2): the next step uses these results
CARRY51 = globals().get('CARRY51', {})

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
 "pt-q01": "$\\sqrt{19{,}044}=?$",
 "pt-q02": "Basket A contains 500 eggs, and basket B contains 600 eggs.\nHow many eggs must be moved from basket A to basket B so that basket A will contain $\\frac{9}{13}$ of the number of eggs in basket B?",
 "pt-q03": "Given: $a\\ne0$ and $b\\ne0$\n$\\frac{a^2+b^2+(a-b)^2}{2ab}+1=?$",
 "pt-q04": "A cylinder is inscribed in a cube whose edge is 3a (see figure).\nWhat is the volume of the cylinder?",
 "pt-q05": "Two fair dice, one blue and one red, are tossed.\nWhat is the probability that the number obtained on the blue die will be at least as large as the number obtained on the red die?",
 "pt-q06": "x is an integer.\nGiven:\n$\\begin{cases} x^2<25 \\\\ 3x+6<0 \\end{cases}$\nWhich of the following could be the value of $x$?",
 "pt-q07": "Nadav and Amit have a total of 90 cards. Nadav has more cards than Amit. The difference between the numbers of cards the two of them have is equal to $\\frac{1}{5}$ of the number of cards Nadav has.\nHow many cards does Nadav have?",
 "pt-q08": "Kobi bought a pair of pants at a 50% discount and a shirt at a 10% discount, and paid a total of 280 shekels instead of 500 shekels.\nWhat was the price of the shirt before the discount (in shekels)?",
 "pt-q09": "If Ron gives Miri 4 stamps, the number of stamps she has will be 2 times the number of stamps he will have. If it is known that the two of them now have the same number of stamps, how many stamps does Miri have now?",
 "pt-q10": "Given: $x\\ge4$\n$\\sqrt{x+2-\\sqrt{x^2-8x+16}}=?$",
 "pt-q11": "In the accompanying figure, ABC is a right triangle, and DBC is an isosceles triangle ($DB=DC$).\nGiven: AB bisects angle DBC.\nBased on this information and the information in the figure,\n$\\beta=?$",
 "pt-q12": "a is a positive integer.\n$a!\\cdot(a+2)!=?$",
 "pt-q13": "One pen contains x cm³ of ink. To write one word, y cm³ of ink are needed. Hagai's supply of pens was enough for him to write $x^3y$ words.\nHow many pens did Hagai have?",
 "pt-q14": "Dana bought a dress at a discount of 40 shekels. The price of the dress after the discount was x shekels. What was the discount on the dress, in percent?",
 "pt-q15": "Orit and Batya decided to go on a trip and to share the expenses. Each of them undertook to pay $\\frac{1}{2}$ of the total. In the end, Orit paid only $\\frac{1}{3}$ of the amount she had undertaken to pay, and Batya paid all the rest of the expenses.\nWhat is the ratio between the amount of money Batya actually paid and the amount of money she undertook to pay?",
 "pt-q24": "Given: $x\\ne-5$\n$xy+5y=2x+10$\n$y=?$",
 "pt-q16": "AOB is a sector of a circle with center O and a radius of 2 cm.\nBased on this information and the information in the figure, what is the area of the shaded region (in cm²)?",
 "pt-q17": "$\\frac{\\sqrt2}{2+\\sqrt2}=?$",
 "pt-q18": "In the accompanying figure, each of the vertices of rectangle ABCD is the center of a circle with a radius of 2 cm. Point O is the center of a circle that is tangent to the four quarter circles and to sides AD and BC of the rectangle.\nWhat is the area of rectangle ABCD (in cm²)?",
 "pt-q19": "Bottle A contains 3.2 liters of a solution with an alcohol concentration of 20%. Bottle B contains 2 liters of a solution with an alcohol concentration of 3%.\nHow many liters of alcohol are there in the two bottles together?",
 "pt-q20": "$\\frac{\\frac{1}{5}+\\frac{1}{6}}{\\frac{2}{5}+\\frac{2}{6}}=?$",
 "pt-q21": "Roni has 60,000 shekels. He invests half of the money in a savings plan that yields a profit of 8% per year. He invests the rest of the money in a mutual fund that yields a profit ranging from 4% to 16% per year.\nRoni's profit in the coming year will be at least ____ of the total amount he invested, and at most ____ of the total amount he invested.",
 "pt-q22": "In the accompanying figure, ABCD is a square.\nBased on this information and the information in the figure, what is the difference between the perimeter of quadrilateral ABED and the perimeter of triangle ECD (in cm)?",
 "pt-q23": "In a certain season, a basketball team won 30% of its first 40 games. From the 41st game on, the team won all of its games until the end of the season, and as a result, its overall winning percentage rose to 50%.\nHow many games in total did the team win in this season?"
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
for _cs in globals().get('CAMERA_SPLITS', []): CP.split(globals(), *_cs)     # topic 51: several lessons in parts

for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _stem_parts(_v); _write_gap(_v)



# 2026-10-13 carry-over boxes (V2) and the layer-order check (V1): after the visual passes, like topics 13-18
import types as _types
MV.carry(_types.SimpleNamespace(**globals()), CARRY51)
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
