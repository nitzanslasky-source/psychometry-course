"""Topic 19 (Defining a New Operation) - the redo for the teacher's own-voice reading (2026-10-12), built exactly like topic 13
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

# ------------------------------------------------------------------------------------------------ q-541 (Hebrew: lesson 1 example)
# NEW at the step: the input takes a's place everywhere.  REMINDER: read the definition, then substitute (camera lesson).
# Hebrew: one method (substitute); a common-factor method is added.
a1 = I('a1', '$\\blacklozenge(6)=6^2-4\\cdot6$', hand='◆(6) = 6^2 − 4·6')
a2 = I('a2', '$=36-24=12$', hand='= 36 − 24 = 12')
a3 = I('a3', '$a^2-4a=a(a-4)$', hand='a^2 − 4a = a(a − 4)')
a4 = I('a4', '$\\blacklozenge(6)=6\\cdot2=12$', hand='◆(6) = 6·2 = 12')
video('solve-q-541', 'solution', qid='q-541', slides=[
    S('Method 1 · Substitute',
      L("The operation diamond is defined for every number a. Diamond of a is equal to a squared minus four a. Diamond of "
        "six is equal to what?", pt('stem', 'The operation diamond', 'hl', 7.0), voice='calm', pause=0.5),
      L("The most basic operation question. [short pause] We'll solve it two ways, substituting, and then taking out a "
        "common factor first.", pt('stem', 'The most basic')),
      L("[short pause] Let's start by substituting. Whatever goes into the diamond takes a's place, everywhere. So six "
        "instead of a. Six squared minus four times six.", show(a1, 'So six instead of a')),
      L("Thirty-six minus twenty-four is twelve. Choice number two is our answer.", show(a2, 'Thirty-six minus twenty-four'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · A common factor',
      L("[pause] Another way. What's different? We simplify the rule before putting the number in. a squared minus four a "
        "is a times, in brackets, a minus four.", show(a3, 'a squared minus four a is')),
      L("So diamond of six is six times six minus four, six times two, twelve. Choice number two. [pause] Okay. I'll see you "
        "in the next question.", show(a4, 'six times two'), mk('tick', 'choice 2', 'six times two, twelve'))),
])

# ------------------------------------------------------------------------------------------------ q-542 (Hebrew: lesson 1 example)
# NEW at the step: nested operations - inside out; the result of the inside is the input of the outside; the trap 25.
# REMINDER: inside out (camera lesson).  Hebrew: one method; an algebra method is added.
b1 = I('b1', '$\\blacklozenge(5)=5^2=25$', hand='◆(5) = 5^2 = 25')
b2 = I('b2', '$\\blacklozenge(\\blacklozenge(5))=\\blacklozenge(25)=25^2=625$', hand='◆(◆(5)) = ◆(25) = 25^2 = 625')
b3 = I('b3', '$(x^2)^2=x^4$: $\\ 5^4=625$', hand='(x^2)^2 = x^4 :    5^4 = 625')
video('solve-q-542', 'solution', qid='q-542', slides=[
    S('Method 1 · Inside out',
      L("The operation diamond is defined for every number x. Diamond of x is equal to x squared. Diamond of diamond of five "
        "is equal to what?", pt('stem', 'The operation diamond', 'hl', 7.0), voice='calm', pause=0.5),
      L("A diamond inside a diamond. [short pause] We'll solve it two ways, inside out, and then with algebra.",
        pt('stem', 'A diamond inside a diamond')),
      L("[short pause] Let's start inside out, like any brackets. The inner one first, diamond of five. The diamond squares, "
        "so five squared is twenty-five.", show(b1, 'diamond of five')),
      L("Now twenty-five takes its place, and the outer diamond works on it. Twenty-five squared is six hundred twenty-five. "
        "Choice number three is our answer. And careful, stopping at twenty-five is the trap. It's waiting in the choices.",
        show(b2, 'twenty-five takes its place'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Algebra',
      L("[pause] Another way. What's different? We look at the rule itself, not the numbers. Squaring, and then squaring "
        "again, is x to the fourth. Five to the fourth is six hundred twenty-five. Choice number three. [pause] Okay. I'll "
        "see you in the next question.", show(b3, 'Squaring, and then'), mk('tick', 'choice 3', 'Five to the fourth'))),
])

# ------------------------------------------------------------------------------------------------ q-543 (Hebrew: lesson 1 example)
# NEW at the step: no definition - put the input into each choice; "cannot be" = the one that misses.  Hebrew: one method,
# and every choice is checked "to learn"; here the three that CAN be come first, so the video ends on the answer.
c1 = I('c1', 'For example $\\ \\blacklozenge(x)=7x$: $\\ 7\\cdot3=21$', size=32, hand='For example   ◆(x) = 7x :    7·3 = 21')
c2 = I('c2', '(1) $27-6=21$ ✓ $\\quad$ (2) $3\\cdot7=21$ ✓', size=32, hand='(1)   27 − 6 = 21  ✓      (2)   3·7 = 21  ✓')
c3 = I('c3', '(4) $24-3=21$ ✓', size=32, hand='(4)   24 − 3 = 21  ✓')
c4 = I('c4', '(3) $15+5=20$ ✗', hand='(3)   15 + 5 = 20  ✗')
video('solve-q-543', 'solution', qid='q-543', slides=[
    S('Plugging in the answers',
      L("Given: diamond of three is equal to twenty-one. Which of the following cannot be the definition of the operation "
        "diamond?", pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("This time there's no definition. They took three, did the diamond, and got twenty-one. [short pause] We'll solve "
        "it by plugging in three into each choice.", pt('stem: g1', 'They took three')),
      L("[short pause] The rule could be endless things. Seven x, for example, seven times three is twenty-one. So we look "
        "for the one that can not give twenty-one.", show(c1, 'Seven x, for example')),
      L("Choice number one, three cubed minus six, twenty-seven minus six, twenty-one. It can be the rule, out. Choice "
        "number two, three times seven, twenty-one, out.", show(c2, 'three cubed minus six'), mk('cross', 'choice 1', 'It can be the rule, out'),
        mk('cross', 'choice 2', 'three times seven, twenty-one, out')),
      L("Choice number four, eight times three minus three, twenty-four minus three, twenty-one, out.", show(c3, 'eight times three'),
        mk('cross', 'choice 4', 'twenty-one, out')),
      L("Choice number three, five times three plus five, fifteen plus five, twenty. Not twenty-one, so this can't be the "
        "definition. Choice number three is our answer. In the exam, the moment you find it, mark it and move on. [pause] "
        "Okay. I'll see you in the next question.", show(c4, 'fifteen plus five'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t19-01 (added)
# NEW at the step: an expression goes in, in brackets; zero is a lazy test number (two choices tie) -> a second number.
# REMINDER: every input in brackets (camera lesson).  Methods: algebra, plugging in numbers.
d1 = I('d1', '$\\blacklozenge(x+1)=(x+1)^2-2(x+1)$', hand='◆(x + 1) = (x + 1)^2 − 2(x + 1)')
d2 = I('d2', '$=x^2+2x+1-2x-2=x^2-1$', hand='= x^2 + 2x + 1 − 2x − 2 = x^2 − 1')
e1 = I('e1', '$x=0$: $\\ \\blacklozenge(1)=1-2=-1$', hand='x = 0 :    ◆(1) = 1 − 2 = −1')
e2 = I('e2', 'Choices: $\\ 1,\\ -1,\\ -1,\\ 3$: $\\ $a tie', size=32, hand='Choices :    1,   −1,   −1,   3 :    a tie')
e3 = I('e3', '$x=2$: $\\ \\blacklozenge(3)=9-6=3$; $\\ 1,\\ 3,\\ -1,\\ 7$', size=32, hand='x = 2 :    ◆(3) = 9 − 6 = 3 ;    1,   3,   −1,   7')
video('solve-q-r26-t19-01', 'solution', qid='q-r26-t19-01', slides=[
    S('Method 1 · Algebra',
      L("For every number x, diamond of x is equal to x squared minus two x. Diamond of x plus one is equal to what?",
        pt('stem', 'For every number x', 'hl', 6.0), voice='calm', pause=0.5),
      L("This time the input is an expression, x plus one. [short pause] We'll solve it two ways, with algebra, and then "
        "plugging in numbers.", pt('stem', 'the input is an expression')),
      L("[short pause] Let's start with algebra. The whole x plus one goes where x was, in brackets. x plus one, squared, "
        "minus two times x plus one.", show(d1, 'The whole x plus one')),
      L("Open the brackets. x squared plus two x plus one, minus two x, minus two. The two x's cancel, and one minus two is "
        "negative one. x squared minus one, choice number two is our answer. The other choices are the traps, no brackets "
        "or a lost minus.", show(d2, 'Open the brackets'), mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Another way. Letters in the choices, so plug in a number. x is zero, so the input is one. One minus two is "
        "negative one.", show(e1, 'x is zero')),
      L("The choices with x zero give one, negative one, negative one, and three. Two choices tie. Zero is a lazy number, "
        "it wipes out whole terms.", show(e2, 'Two choices tie'), mk('cross', 'choice 1', 'give one, negative one'),
        mk('cross', 'choice 4', 'and three. Two choices tie')),
      L("So a second number, x is two. The input is three, nine minus six, three. The choices give one, three, negative one "
        "and seven. Only choice number two. [pause] Okay. I'll see you in the next question.", show(e3, 'x is two'),
        mk('cross', 'choice 3', 'and seven. Only'), mk('tick', 'choice 2', 'Only choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t19-02 (added)
# NEW: does the order of the inputs matter? "Not always" -> one counterexample (not equal numbers); "always" -> swap the
# letters.  REMINDER: order can matter (camera lesson).  Methods: plugging in numbers, algebra.
f1 = I('f1', '$a=1,\\ b=2$ $\\quad$ (not equal numbers)', size=32, hand='a = 1,   b = 2      (not equal numbers)')
f2 = I('f2', '(1) $2,\\ 4$ ✗ $\\quad$ (2) $3,\\ 6$ ✗ $\\quad$ (4) $2,\\ 3$ ✗', size=32, hand='(1)  2, 4  ✗      (2)  3, 6  ✗      (4)  2, 3  ✗')
f3 = I('f3', '(3) $1\\cdot2+1+2=5$, $\\ 2\\cdot1+2+1=5$', size=32, hand='(3)   1·2 + 1 + 2 = 5,    2·1 + 2 + 1 = 5')
g1 = I('g1', '$b\\star a=ba+b+a=ab+a+b=a\\star b$ ✓', size=34)
video('solve-q-r26-t19-02', 'solution', qid='q-r26-t19-02', slides=[
    S('Method 1 · Plugging in numbers',
      L("For which of the following operations is a star b equal to b star a, for all numbers a and b?",
        pt('stem', 'For which', 'hl', 6.0), voice='calm', pause=0.5),
      L("Does the order of the inputs matter? [short pause] We'll solve it two ways, plugging in numbers, and then with "
        "algebra.", pt('stem', 'the order of the inputs')),
      L("[short pause] Let's start with numbers. To knock a choice out, one counterexample is enough. a is one and b is two. "
        "Not equal numbers, because with a equal to b, every operation looks fine.", show(f1, 'a is one and b is two')),
      L("Choice number one, one star two is two, and two star one is four. Out. Choice number two, three and six. Out. "
        "Choice number four, two and three. Out.", show(f2, 'one star two is two'), mk('cross', 'choice 1', 'is four. Out'),
        mk('cross', 'choice 2', 'three and six. Out'), mk('cross', 'choice 4', 'two and three. Out')),
      L("Choice number three, one times two plus one plus two is five, and the other way, five too. Choice number three is "
        "our answer.", show(f3, 'one times two plus'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Algebra',
      L("[pause] Another way. What's different? Numbers can't prove always, algebra can. Swap the letters. b star a is b a, "
        "plus b, plus a. b a is a b, and b plus a is a plus b. Exactly a star b. So, not always, one example. Always, swap "
        "the letters. Choice number three. [pause] Okay. I'll see you in the next question.", show(g1, 'Swap the letters'),
        mk('tick', 'choice 3', 'Exactly a star b'))),
])

# ------------------------------------------------------------------------------------------------ operation-patterns (lesson)
# NEW: the inverse operation - undo the steps in reverse order (2x + 3 -> (y - 3)/2; 3x - 4 -> (y + 4)/3), check with a
# number, the trap (wrong order).  (The other advanced types are taught in the questions that follow.)
h1 = I('h1', '$\\blacklozenge(x)=2x+3$: $\\ \\times2$, then $+3$', size=38, hand='◆(x) = 2x + 3 :    × 2,  then  + 3')
h2 = I('h2', 'Undo: $\\ -3$, then $\\div2$: $\\ \\frac{y-3}{2}$', size=38, hand='Undo :    − 3,  then  ÷ 2 :    {y − 3/2}')
h3 = I('h3', '$4\\to11\\to\\frac{11-3}{2}=4$ ✓', size=38, hand='4  →  11  →  {11 − 3/2} = 4   ✓')
h4 = I('h4', 'Trap: $\\ \\frac y2-3$: $\\ 11\\to2.5$ ✗', size=34, hand='Trap :    {y/2} − 3 :    11  →  2.5   ✗')
h5 = I('h5', '$\\blacklozenge(x)=3x-4$: $\\ $undo $\\frac{y+4}{3}$: $\\ 5\\to11\\to5$', size=34, hand='◆(x) = 3x − 4 :    undo  {y + 4/3} :    5  →  11  →  5')
video('operation-patterns', 'lesson', slides=[
    S('Operation Patterns',
      L("Welcome back. Now the more advanced operation questions. Each question that follows shows one type, and teaches it. "
        "First, one type that only the practice has, the inverse operation.")),
    S('The inverse operation',
      L("The inverse operation undoes the diamond. Put in the result, and you get x back. Take diamond of x equals two x plus "
        "three. Read its steps, first times two, then plus three.", show(h1, 'Read its steps')),
      L("Undo them in reverse order. The last step comes off first, so minus three, and then divide by two. y minus three, "
        "over two.", show(h2, 'Undo them in reverse order')),
      L("Check with a number. Four goes to eleven. Eleven minus three is eight, and eight over two is four. Back to the "
        "start.", show(h3, 'Four goes to eleven')),
      L("And the trap undoes the steps in the wrong order. y over two, minus three. Eleven over two is five and a half, and "
        "five and a half minus three is two and a half. Not four.", show(h4, 'the trap undoes')),
      L("One more. Diamond of x is three x minus four. Undo, plus four, then divide by three. Five goes to eleven, and eleven "
        "plus four is fifteen, and fifteen over three is five. Back again. [pause] Okay. I'll see you in the next video.", show(h5, 'One more'))),
])

# ------------------------------------------------------------------------------------------------ q-544 (Hebrew: lesson 2, an operation on an expression)
# NEW: the operation works on 2x, not x - match the whole input first (2x = 14 -> x = 7); the trap 19 (14 straight into x).
# Hebrew: one method; a plugging-in check by rewriting the rule is added as method 2.
i1 = I('i1', '$\\hl{in}{2x}=14$: $\\ x=7$', hand='\\hl{in}{2x} = 14 :    x = 7')
i2 = I('i2', '$\\blacklozenge(14)=7+5=12$', hand='◆(14) = 7 + 5 = 12')
i3 = I('i3', 'Trap: $\\ 14+5=19$', size=32, hand='Trap :    14 + 5 = 19')
j1 = I('j1', 'In: $\\ 2x$ $\\quad$ out: $\\ x+5$: $\\ $halve, then $+5$', size=32, hand='In :   2x      out :   x + 5 :    halve,  then  + 5')
j2 = I('j2', '$\\blacklozenge(n)=\\frac n2+5$: $\\ \\frac{14}{2}+5=12$', hand='◆(n) = {n/2} + 5 :    {14/2} + 5 = 12')
video('solve-q-544', 'solution', qid='q-544', slides=[
    S('Method 1 · Match the input',
      L("The operation diamond is defined for every number x. Diamond of two x is equal to x plus five. Diamond of fourteen "
        "is equal to what?", pt('stem', 'The operation diamond', 'hl', 7.0), voice='calm', pause=0.5),
      L("Look closely, the diamond works on two x, not on x. An operation on an expression. [short pause] We'll solve it "
        "two ways, matching the input, and then rewriting the rule.", pt('stem', 'the diamond works on two x')),
      L("[short pause] Let's start by matching the input. Fourteen is not x. Fourteen is two x. So two x is fourteen, and x "
        "is seven.", show(i1, 'Fourteen is not x')),
      L("The rule says x plus five. Seven plus five is twelve. Choice number one is our answer.", show(i2, 'Seven plus five'),
        mk('tick', 'choice 1', 'Choice number one is our answer')),
      L("Now careful, the trap. Fourteen straight into x plus five gives nineteen, and it's waiting in the choices.",
        show(i3, 'the trap'))),
    S('Method 2 · Rewrite the rule',
      L("[pause] Another way. What's different? We rewrite the rule so it works on any input directly. Two x goes in, and x "
        "plus five comes out. So the diamond halves its input, then adds five.", show(j1, 'Two x goes in')),
      L("Diamond of n is n over two, plus five. Fourteen over two is seven, and seven plus five is twelve. Choice number one. [pause] "
        "Okay. I'll see you in the next question.", show(j2, 'Diamond of n is'), mk('tick', 'choice 1', 'seven plus five is twelve'))),
])

# ------------------------------------------------------------------------------------------------ q-545 (Hebrew: lesson 2, conditions)
# NEW: a rule with conditions - check the parity of the input at every step (the output can switch).
# REMINDER: inside out (q-542).  Hebrew: one method.
k1 = I('k1', '$\\blacklozenge(1)$: $\\ 1$ odd: $\\ 4\\cdot1=4$', hand='◆(1) :    1 odd :    4·1 = 4')
k2 = I('k2', '$\\blacklozenge(4)$: $\\ 4$ even: $\\ 16-9=7$', hand='◆(4) :    4 even :    16 − 9 = 7')
k3 = I('k3', '$\\blacklozenge(7)$: $\\ 7$ odd: $\\ 4\\cdot7=28$', hand='◆(7) :    7 odd :    4·7 = 28')
video('solve-q-545', 'solution', qid='q-545', slides=[
    S('Conditions, inside out',
      L("The operation diamond is defined for every integer x. Diamond of x is four x when x is odd, and x squared minus nine "
        "when x is even. Diamond of diamond of diamond of one is equal to what?", pt('stem', 'The operation diamond', 'hl', 9.0), voice='calm', pause=0.5),
      L("A rule with conditions, one for odd and one for even. [short pause] So before each step, we check the input. And "
        "three diamonds, so inside out.", pt('stem', 'A rule with conditions')),
      L("[short pause] Diamond of one. One is odd, so the odd rule, four x. Four times one is four.", show(k1, 'Diamond of one')),
      L("Now four goes in. Four is even, so switch rules. Four squared minus nine, sixteen minus nine, seven.", show(k2, 'Now four goes in')),
      L("Seven is odd again. Four times seven is twenty-eight. Choice number three is our answer. So check the parity at "
        "every step, because the output can switch sides. [pause] Okay. I'll see you in the next question.",
        show(k3, 'Seven is odd again'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t19-03 (added)
# NEW: conditions backwards - try both rules, keep an answer only if it fits the rule it came from (8 is even -> out).
# Methods: two cases, plugging in the answers.
l1 = I('l1', 'Odd: $\\ 3x=24$, $\\ x=8$: $\\ 8$ is even ✗', hand='Odd :    3x = 24,    x = 8 :    8 is even   ✗')
l2 = I('l2', 'Even: $\\ x^2-12=24$, $\\ x^2=36$, $\\ x=6$ ✓', hand='Even :    x^2 − 12 = 24,    x^2 = 36,    x = 6   ✓')
m1 = I('m1', '$\\blacklozenge(8)$: $\\ $even: $\\ 64-12=52$ ✗', hand='◆(8) :    even :    64 − 12 = 52   ✗')
m2 = I('m2', '$\\blacklozenge(6)$: $\\ $even: $\\ 36-12=24$ ✓', hand='◆(6) :    even :    36 − 12 = 24   ✓')
video('solve-q-r26-t19-03', 'solution', qid='q-r26-t19-03', slides=[
    S('Method 1 · Two cases',
      L("The operation diamond is defined for every positive integer x. Diamond of x is three x when x is odd, and x squared "
        "minus twelve when x is even. Given: diamond of x is equal to twenty-four. x is equal to what?",
        pt('stem', 'The operation diamond', 'hl', 9.0), voice='calm', pause=0.5),
      L("Conditions again, but backwards. They give the result. [short pause] We'll solve it two ways, two cases, and then "
        "plugging in the answers.", pt('stem', 'They give the result')),
      L("[short pause] We don't know if x is odd or even, so try both rules. The odd rule, three x is twenty-four, so x is "
        "eight. But eight is even, and an even number never uses the odd rule. Throw it out.", show(l1, 'The odd rule')),
      L("The even rule, x squared minus twelve is twenty-four, so x squared is thirty-six. x is positive, so six. And six is "
        "even, it fits. Choice number two is our answer. The traps are eight, and six or eight.", show(l2, 'The even rule'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Another way. What's different? We put each offered x into the operation, so the condition is checked for "
        "us. Eight is even, sixty-four minus twelve, fifty-two. Not twenty-four. Out.", show(m1, 'Eight is even'),
        mk('cross', 'choice 1', 'Not twenty-four. Out')),
      L("Six is even, thirty-six minus twelve, twenty-four. Found it. Choice number two. [pause] Okay. I'll see you in the "
        "next question.", show(m2, 'Six is even'), mk('tick', 'choice 2', 'Found it. Choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-546 (Hebrew: lesson 2, a circular rule)
# NEW: a circular rule - go down to the start value, then climb back up with numbers; the flip-flop pattern 2, 7, 2, 7.
# Hebrew: one method; the pattern is added as method 2.
n1 = I('n1', '$\\blacklozenge(6)=9-\\blacklozenge(4)$', hand='◆(6) = 9 − ◆(4)')
n2 = I('n2', '$\\blacklozenge(4)=9-\\blacklozenge(2)$', hand='◆(4) = 9 − ◆(2)')
n3 = I('n3', '$\\blacklozenge(2)=9-\\blacklozenge(0)$, $\\ \\blacklozenge(0)=2$', hand='◆(2) = 9 − ◆(0),    ◆(0) = 2')
n4 = I('n4', '$\\blacklozenge(2)=7,\\ \\ \\blacklozenge(4)=2,\\ \\ \\blacklozenge(6)=7$', hand='◆(2) = 7,    ◆(4) = 2,    ◆(6) = 7')
o1 = I('o1', '$0,\\ 2,\\ 4,\\ 6,\\ 8$: $\\ 2,\\ 7,\\ 2,\\ 7,\\ 2$', hand='0,  2,  4,  6,  8 :    2,  7,  2,  7,  2')
video('solve-q-546', 'solution', qid='q-546', slides=[
    S('Method 1 · Down, then back up',
      L("The operation diamond is defined for every even integer x that's zero or more. Diamond of x is two when x is zero, "
        "and nine minus diamond of x minus two when x is two or more. Diamond of six is equal to what?",
        pt('stem', 'The operation diamond', 'hl', 9.0), voice='calm', pause=0.5),
      L("A circular rule, the operation appears inside its own definition. [short pause] We'll solve it two ways, going down "
        "and back up, and then with the pattern.", pt('stem', 'A circular rule')),
      L("[short pause] Diamond of six is nine minus diamond of four. We don't know that yet, so keep going. Diamond of four is "
        "nine minus diamond of two.", show(n1, 'Diamond of six is'), show(n2, 'Diamond of four is')),
      L("Diamond of two is nine minus diamond of zero. And diamond of zero is given, two. Now only numbers are left.",
        show(n3, 'Diamond of two is')),
      L("Climb back up. Nine minus two is seven, so diamond of two is seven. Nine minus seven is two. And nine minus two is "
        "seven. Diamond of six is seven. Choice number four is our answer.", show(n4, 'Climb back up'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · The pattern',
      L("[pause] Another way. What's different? We look for the pattern instead of climbing every step. Two, seven, two, "
        "seven. Zero, four and eight give two, and two and six give seven. So six gives seven, choice number four, and even "
        "diamond of a hundred would be instant. [pause] Okay. I'll see you in the next question.", show(o1, 'Two, seven, two'),
        mk('tick', 'choice 4', 'So six gives seven'))),
])

# ------------------------------------------------------------------------------------------------ q-547 (Hebrew: lesson 2, a circular rule)
# NEW at the step: each step passes down to the start value.  REMINDER: circular rules (q-546).  Hebrew: one method.
p1 = I('p1', '$\\blacklozenge(7)=\\blacklozenge(6)=\\blacklozenge(5)=\\ldots=\\blacklozenge(1)$', hand='◆(7) = ◆(6) = ◆(5) = . . . = ◆(1)')
p2 = I('p2', '$1$ is not bigger than $1$: $\\ \\blacklozenge(1)=9$', hand='1  is not bigger than  1 :    ◆(1) = 9')
video('solve-q-547', 'solution', qid='q-547', slides=[
    S('Down to the start',
      L("The operation diamond is defined for every positive integer x. Diamond of x is nine when x is one, and diamond of x "
        "minus one when x is bigger than one. Diamond of seven is equal to what?", pt('stem', 'The operation diamond', 'hl', 8.0), voice='calm', pause=0.5),
      L("Another circular rule. [short pause] We'll go down to the start value.", pt('stem', 'Another circular rule')),
      L("[short pause] Seven is bigger than one, so diamond of seven is diamond of six. Diamond of six is diamond of five, and "
        "so on. Each one just passes to the one below, down to diamond of one.", show(p1, 'Seven is bigger than one')),
      L("And one is not bigger than one, so the start value. Diamond of one is nine. So diamond of seven is nine. Choice "
        "number four is our answer. [pause] Okay. I'll see you in the next question.", show(p2, 'one is not bigger'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-548 (Hebrew: lesson 2, isolate the operation)
# NEW: the operation on both sides - treat it as the unknown and isolate it (very rare on the exam).  Hebrew: one method.
q1 = I('q1', '$5\\blacklozenge(x)-4\\blacklozenge(x)=8+3x$', hand='5◆(x) − 4◆(x) = 8 + 3x')
q2 = I('q2', '$\\blacklozenge(x)=3x+8$', hand='◆(x) = 3x + 8')
q3 = I('q3', '$\\blacklozenge(4)=12+8=20$', hand='◆(4) = 12 + 8 = 20')
video('solve-q-548', 'solution', qid='q-548', slides=[
    S('Isolate the operation',
      L("For every number x, five times diamond of x, minus three x, is equal to eight plus four times diamond of x. Diamond "
        "of four is equal to what?", pt('stem', 'For every number x', 'hl', 7.0), voice='calm', pause=0.5),
      L("The diamond is on both sides. It's very rare on the exam, but good to know. [short pause] We treat the diamond like "
        "an unknown, and isolate it.", pt('stem', 'The diamond is on both sides')),
      L("[short pause] Move the four diamonds to the left, as a minus, and the minus three x to the right, as a plus. Five "
        "diamonds minus four diamonds is one diamond.", show(q1, 'Move the four diamonds')),
      L("So diamond of x is three x plus eight. Now it's an ordinary definition.", show(q2, 'three x plus eight')),
      L("Diamond of four is three times four plus eight, twelve plus eight, twenty. Choice number two is our answer. [pause] "
        "Okay. I'll see you in the next question.", show(q3, 'Diamond of four is'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-549 (Hebrew: lesson 2, must be true)
# NEW: the operation in every choice -> skip it, finish the section, come back; algebra marks at once, plugging in is
# faster (x = 1; a second number if two survive).  Hebrew: algebra, plugging in.
r1 = I('r1', 'Operation in every choice: $\\ $skip, come back at the end', size=28, col=1)
r2 = I('r2', '(1) $(6x)^2=36x^2$ ✓', hand='(1)   (6x)^2 = 36x^2   ✓')
r3 = I('r3', '(2) $(\\sqrt x)^2\\cdot(\\sqrt x)^2=x\\cdot x=x^2$ ✓', size=32, hand='(2)   (√{x})^2 · (√{x})^2 = x·x = x^2   ✓')
r4 = I('r4', '(4) $(x-7)^2=(7-x)^2$ ✓', hand='(4)   (x − 7)^2 = (7 − x)^2   ✓')
r5 = I('r5', '(3) $(5x)^2=25x^2\\ne5x^2$ ✗', hand='(3)   (5x)^2 = 25x^2 ≠ 5x^2   ✗')
s1 = I('s1', '$x=1$: $\\ $(1) $36=36$ $\\quad$ (2) $1=1$ $\\quad$ (4) $36=36$', size=32, hand='x = 1 :    (1)  36 = 36      (2)  1 = 1      (4)  36 = 36')
s2 = I('s2', '(3) $\\blacklozenge(5)=25$, $\\ 5\\cdot\\blacklozenge(1)=5$ ✗', hand='(3)   ◆(5) = 25,    5·◆(1) = 5   ✗')
video('solve-q-549', 'solution', qid='q-549', slides=[
    S('Method 1 · Algebra',
      L("For every number t, diamond of t is equal to t squared. In the choices, x is zero or more. Which of the following "
        "is not always true?", pt('stem', 'For every number t', 'hl', 7.0), voice='calm', pause=0.5),
      L("The diamond is in every choice, two or three times. That's a lot of work. So a tip first. In the exam, skip it, "
        "solve the rest of the section, and come back at the end. [short pause] We'll solve it two ways, with algebra, and "
        "then plugging in numbers.", pt('choice 1', 'in every choice'), show(r1, 'skip it')),
      L("[short pause] Let's start with algebra. The diamond squares its input. Choice number one, six x squared is thirty-six "
        "x squared, and thirty-six times x squared is the same. True. Out.", show(r2, 'six x squared'), mk('cross', 'choice 1', 'is the same. True')),
      L("Choice number two, root x squared is x, and x times x is x squared. True. Out. Choice number four, x minus seven and "
        "seven minus x are opposites, and squared they're equal. True. Out.", show(r3, 'root x squared'), show(r4, 'are opposites'),
        mk('cross', 'choice 2', 'x squared. True. Out'), mk('cross', 'choice 4', "they're equal. True. Out")),
      L("Choice number three, five x squared is twenty-five x squared, but five times x squared is only five x squared. Not "
        "equal. Choice number three is our answer.", show(r5, 'five x squared is'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Another way, and it's faster. What's different? No opening at all, just numbers. x is one. Choice number one, "
        "diamond of six is thirty-six, and thirty-six times diamond of one is thirty-six. Choice number two, one equals one. "
        "Choice number four, negative six and six squared are both thirty-six.", show(s1, 'x is one')),
      L("Choice number three, diamond of five is twenty-five, and five times diamond of one is five. Not equal, choice number "
        "three. One warning. Zero or one can make a false rule look true. If two choices had survived, we'd try a second "
        "number, like two. [pause] Okay. I'll see you in the next question.", show(s2, 'diamond of five is twenty-five'),
        mk('tick', 'choice 3', 'Not equal, choice number'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t19-18 (added)
# NEW: a property question - put each rule on trial with a test value (not 0 or 1); the families that undo themselves
# (c - x, c / x); a step property -> test two neighbours.  Methods: plugging in numbers, understanding.
t1 = I('t1', '$x=2$: $\\ $(1) $2\\to12\\to72$ ✗ $\\quad$ (2) $2\\to8\\to14$ ✗', size=32, hand='x = 2 :    (1)  2 → 12 → 72  ✗      (2)  2 → 8 → 14  ✗')
t2 = I('t2', '(3) $2\\to\\frac13\\to\\frac1{18}$ ✗ $\\quad$ (4) $2\\to3\\to2$ ✓', size=32, hand='(3)  2 → {1/3} → {1/18}  ✗      (4)  2 → 3 → 2  ✓')
u1 = I('u1', 'Undo themselves: $\\ c-x$, $\\ \\frac cx$', size=32, hand='Undo themselves :    c − x,    {c/x}')
u2 = I('u2', '$10-(10-x)=x \\qquad 6\\div\\frac6x=x$', size=34, hand='10 − (10 − x) = x        6 ÷ {6/x} = x')
u3 = I('u3', 'Step property? $\\ $Test two neighbours', size=28, col=1)
video('solve-q-r26-t19-18', 'solution', qid='q-r26-t19-18', slides=[
    S('Method 1 · Plugging in numbers',
      L("The operation diamond is defined for every positive number x. It is known that for every positive x, diamond of "
        "diamond of x is equal to x. Which of the following can be the definition of the operation diamond?",
        pt('stem', 'The operation diamond', 'hl', 9.0), voice='calm', pause=0.5),
      L("No definition, just a property. Do the diamond twice, and you're back at x. [short pause] We'll solve it two ways, "
        "plugging in numbers, and then by understanding.", pt('stem', 'just a property')),
      L("[short pause] Let's put each rule on trial. Pick a test value, not zero, not one. Two. Six x, two goes to twelve, and "
        "twelve goes to seventy-two. Not two, out. x plus six, eight, then fourteen. Out.", show(t1, 'Pick a test value'),
        mk('cross', 'choice 1', 'Not two, out'), mk('cross', 'choice 2', 'then fourteen. Out')),
      L("x over six, one third, then one eighteenth. Out. Six over x, two goes to three, and three goes back to two. Choice "
        "number four is our answer.", show(t2, 'x over six'), mk('cross', 'choice 3', 'one eighteenth. Out'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Understanding',
      L("[pause] Another way. What's different? We know which families undo themselves, c minus x and c over x. Ten minus, "
        "ten minus x, is x again. And six over, six over x, is x again.", show(u1, 'undo themselves'), show(u2, 'Ten minus')),
      L("So six over x, choice number four. Watch choice number three, x over six. It looks close, but the x is on top, and it "
        "just keeps shrinking. And a step property, like one step up in the input gives three times the result? Test two "
        "neighbours, like two and three. [pause] Okay. I'll see you in the next question.", show(u3, 'Test two neighbours'),
        mk('tick', 'choice 4', 'So six over x'))),
])

# ------------------------------------------------------------------------------------------------ q-550 (Hebrew Q1)
# NEW: an operation of three numbers (each to the power of the product of the other two); the insight: look at the OUTER
# call first - a zero there makes the inner value irrelevant (her example), here the two ones give 2 + z.
# Hebrew: the standard way, the insight.
v1 = I('v1', 'Inner: $\\ x=2,\\ y=1,\\ z=4$', hand='Inner :    x = 2,    y = 1,    z = 4')
v2 = I('v2', '$2^4+1^8+4^2=16+1+16=33$', hand='2^4 + 1^8 + 4^2 = 16 + 1 + 16 = 33')
v3 = I('v3', '$\\blacklozenge(1,1,33)=1^{33}+1^{33}+33^1=35$', hand='◆(1, 1, 33) = 1^33 + 1^33 + 33^1 = 35')
w1 = I('w1', '$\\blacklozenge(\\ldots,0,1)=(\\ldots)^0+0^{(\\ldots)}+1^0=1+0+1=2$', size=32)
w2 = I('w2', '$\\blacklozenge(1,1,z)=1+1+z^1=2+z$', hand='◆(1, 1, z) = 1 + 1 + z^1 = 2 + z')
w3 = I('w3', '$2+33=35$', hand='2 + 33 = 35')
video('solve-q-550', 'solution', qid='q-550', slides=[
    S('Method 1 · The standard way',
      L("For every three numbers x, y and z, diamond of x, y, z is equal to x to the power of y z, plus y to the power of x "
        "z, plus z to the power of x y. Diamond of one, one, and diamond of two, one, four, is equal to what?",
        pt('stem', 'For every three numbers', 'hl', 10.0), voice='calm', pause=0.5),
      L("A brand-new operation, but only numbers, no unknowns. [short pause] We'll solve it two ways, the standard way, and "
        "then a sharp shortcut.", pt('stem', 'only numbers')),
      L("[short pause] The diamond appears twice, so we run it twice, and always the inner one first. x is two, y is one, and "
        "z is four. Each number goes to the power of the product of the other two.", show(v1, 'x is two, y is one')),
      L("One times four is four, and two to the fourth is sixteen. Two times four is eight, and one to the eighth is one. "
        "Two times one is two, and four squared is sixteen. Thirty-three.", show(v2, 'One times four is four')),
      L("Now the outer one, one, one, thirty-three. One to any power is one, twice. One times one is one, and "
        "thirty-three to the first is thirty-three. One plus one plus thirty-three is thirty-five. Choice number three is our answer.",
        show(v3, 'Now the outer one'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Look at the outside first',
      L("[pause] And a shortcut. What's different? We look at the outer diamond before calculating anything. Sometimes a "
        "zero there makes the inner value irrelevant. Say the outer call were the inner value, zero, one. The inner value "
        "to the power zero is one, zero to a positive power is zero, and one to any power is one. Two, whatever is inside.",
        show(w1, 'Say the outer call')),
      L("Here there's no zero, but the two ones do something similar. One to any power, twice, and the last number to the "
        "power of one times one stays itself. So the outer diamond is two plus whatever is in the third slot.", show(w2, 'the two ones')),
      L("Two plus thirty-three is thirty-five. Choice number three. Shorter, if you spot it under pressure. If not, the first "
        "way always works. [pause] Okay. I'll see you in the next question.", show(w3, 'Two plus thirty-three'),
        mk('tick', 'choice 3', 'is thirty-five. Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-551 (Hebrew Q2)
# NEW: two operations in one question - three calculations; the shortcut: recognize the shortcut formulas (x - y)², (x + y)².
# REMINDER: the shortcut formulas (topic 4).  Hebrew: the standard way, the shortcut formulas.
x1 = I('x1', '$\\blacklozenge(10,6)=100-120+36=16$', hand='◆(10, 6) = 100 − 120 + 36 = 16')
x2 = I('x2', '$\\blacklozenge(5,4)=25-40+16=1$', hand='◆(5, 4) = 25 − 40 + 16 = 1')
x3 = I('x3', '$\\#(16,1)=256+32+1=289$', size=36)
y1 = I('y1', '$\\blacklozenge(x,y)=(x-y)^2 \\qquad \\#(x,y)=(x+y)^2$', size=36)
y2 = I('y2', '$(10-6)^2=16 \\qquad (5-4)^2=1$', hand='(10 − 6)^2 = 16        (5 − 4)^2 = 1')
y3 = I('y3', '$(16+1)^2=17^2=289$', hand='(16 + 1)^2 = 17^2 = 289')
video('solve-q-551', 'solution', qid='q-551', slides=[
    S('Method 1 · The standard way',
      L("For every two numbers x and y, two operations are defined. Diamond of x, y is x squared minus two x y plus y "
        "squared, and hash of x, y is x squared plus two x y plus y squared. Hash of diamond of ten, six, and diamond of five, "
        "four, is equal to what?", pt('stem', 'For every two numbers', 'hl', 11.0), voice='calm', pause=0.5),
      L("Two operations in one question. [short pause] We'll solve it two ways, the standard way, and then with the shortcut "
        "formulas.", pt('stem', 'Two operations')),
      L("[short pause] The diamond appears twice inside, and then the hash works on both results. Three calculations. The "
        "left diamond. Ten squared is a hundred. Two times ten times six is a hundred twenty, so minus a hundred twenty. "
        "Six squared is thirty-six. A hundred minus a hundred twenty plus thirty-six is sixteen.", show(x1, 'The left diamond')),
      L("The right diamond, twenty-five, minus forty, plus sixteen. One.", show(x2, 'The right diamond')),
      L("Now the hash of sixteen and one. Two fifty-six, plus two times sixteen times one, thirty-two, plus one. Two "
        "eighty-nine. Choice number two is our answer.", show(x3, 'Now the hash'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · The shortcut formulas',
      L("[pause] Another way. What's different? We recognize the shortcut formulas in the definitions. x squared minus two x "
        "y plus y squared is x minus y, squared. And the hash is x plus y, squared.", show(y1, 'x minus y, squared')),
      L("Ten minus six, squared, sixteen. Five minus four, squared, one.", show(y2, 'Ten minus six')),
      L("Sixteen plus one, squared, seventeen squared, two eighty-nine. Choice number two. Much shorter, if you see it. "
        "[pause] Okay. I'll see you in the next question.", show(y3, 'Sixteen plus one'), mk('tick', 'choice 2', 'seventeen squared'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t19-05 (added)
# NEW: f(2) - f(-2) for a polynomial: even powers and the constant cancel, odd powers double.  Methods: calculation, insight.
z1 = I('z1', '$\\blacklozenge(2)=32+48-16+4+8-7=69$', hand='◆(2) = 32 + 48 − 16 + 4 + 8 − 7 = 69')
z2 = I('z2', '$\\blacklozenge(-2)=-32+48+16+4-8-7=21$', hand='◆(−2) = −32 + 48 + 16 + 4 − 8 − 7 = 21')
z3 = I('z3', '$69-21=48$', hand='69 − 21 = 48')
z4 = I('z4', 'Even power, constant: $\\ $cancel $\\quad$ odd power: $\\ $doubled', size=32, hand='Even power, constant :   cancel      odd power :   doubled')
z5 = I('z5', '$2\\cdot(32-16+8)=2\\cdot24=48$', hand='2·(32 − 16 + 8) = 2·24 = 48')
video('solve-q-r26-t19-05', 'solution', qid='q-r26-t19-05', slides=[
    S('Method 1 · Calculate both',
      L("For every number x, diamond of x is x to the fifth, plus three x to the fourth, minus two x cubed, plus x squared, "
        "plus four x, minus seven. Diamond of two minus diamond of negative two is equal to what?",
        pt('stem', 'For every number x', 'hl', 9.0), voice='calm', pause=0.5),
      L("A long rule, a number and its opposite. [short pause] We'll solve it two ways, calculating both, and then a "
        "shortcut.", pt('stem', 'a number and its opposite')),
      L("[short pause] Diamond of two. Two to the fifth is thirty-two, three times sixteen is forty-eight, and two times "
        "eight is sixteen, with a minus. Thirty-two plus forty-eight is eighty, minus sixteen is sixty-four, plus four is "
        "sixty-eight, plus eight is seventy-six, minus seven is sixty-nine.", show(z1, 'Diamond of two')),
      L("Diamond of negative two. The odd powers turn negative, and the even powers stay. Negative thirty-two plus "
        "forty-eight is sixteen, plus sixteen is thirty-two, plus four is thirty-six, minus eight is twenty-eight, minus "
        "seven is twenty-one.", show(z2, 'Diamond of negative two')),
      L("Sixty-nine minus twenty-one is forty-eight. Choice number three is our answer.", show(z3, 'Sixty-nine minus'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Even cancels, odd doubles',
      L("[pause] Another way. What's different? We look at each term with two and negative two, instead of calculating "
        "everything. An even power and the plain number are the same for both, so in the subtraction they cancel. An odd "
        "power just changes its sign, and something minus its opposite is twice that thing.", show(z4, 'An even power')),
      L("So keep only the odd terms at two, thirty-two minus sixteen plus eight, twenty-four, and double it. Forty-eight. "
        "Choice number three. And with a plus instead, only the even terms survive, that's the ninety in the choices. "
        "[pause] Okay. I'll see you in the next question.", show(z5, 'keep only the odd terms'), mk('tick', 'choice 3', 'Forty-eight. Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-552 (Hebrew Q3)
# NEW: unknowns in the operation - the slot matters (8 times the FIRST squared); plugging in is the recommended way here;
# all choices are numbers -> one plug-in; some stop at the top (only one choice has 73).  REMINDER: roots (topic 9).
# Hebrew: the full math, plugging in numbers.
a5 = I('a5', '$\\blacklozenge(a,a)=\\sqrt{9a^2}=3a$', hand='◆(a, a) = √{9a^2} = 3a')
a6 = I('a6', 'Top: $\\ \\blacklozenge(3a,a)=\\sqrt{72a^2+a^2}=a\\sqrt{73}$', size=32, hand='Top :    ◆(3a, a) = √{72a^2 + a^2} = a√{73}')
a7 = I('a7', 'Bottom: $\\ \\blacklozenge(a,3a)=\\sqrt{8a^2+9a^2}=a\\sqrt{17}$', size=32, hand='Bottom :    ◆(a, 3a) = √{8a^2 + 9a^2} = a√{17}')
a8 = I('a8', '$\\frac{a\\sqrt{73}}{a\\sqrt{17}}=\\sqrt{\\frac{73}{17}}$', hand='{a√{73}/a√{17}} = √{{73/17}}')
b5 = I('b5', '$a=1$: $\\ \\blacklozenge(1,1)=\\sqrt9=3$', hand='a = 1 :    ◆(1, 1) = √{9} = 3')
b6 = I('b6', 'Top: $\\ \\blacklozenge(3,1)=\\sqrt{73}$ $\\quad$ bottom: $\\ \\blacklozenge(1,3)=\\sqrt{17}$', size=32, hand='Top :   ◆(3, 1) = √{73}      bottom :   ◆(1, 3) = √{17}')
video('solve-q-552', 'solution', qid='q-552', slides=[
    S('Method 1 · The full math',
      L("For every two numbers x and y, diamond of x, y is the square root of eight x squared plus y squared. Given: a is "
        "bigger than zero. Diamond of diamond of a, a, and a, over diamond of a, and diamond of a, a, is equal to what?",
        pt('stem', 'For every two numbers', 'hl', 10.0), voice='calm', pause=0.5),
      L("Unknowns this time. [short pause] We'll solve it two ways, the full math, and then plugging in numbers.",
        pt('stem', 'Unknowns this time')),
      L("[short pause] Four diamonds, but diamond of a, a is on top and at the bottom, so three calculations. The inner one, "
        "the root of eight a squared plus a squared, the root of nine a squared, three a.", show(a5, 'The inner one')),
      L("Top, three a goes in the first slot. Three a squared is nine a squared, times eight, seventy-two a squared, plus a "
        "squared. a root seventy-three.", show(a6, 'Top, three a'))),
    S('Method 1 · The full math',
      L("Bottom, now three a is in the second slot. Eight a squared plus nine a squared. a root seventeen.", show(a7, 'Bottom, now three a')),
      L("The a's cancel. Root seventy-three over root seventeen, one root of seventy-three seventeenths. Choice number three "
        "is our answer.", show(a8, "The a's cancel"), mk('tick', 'choice 3', 'Choice number three is our answer')),
      sb='Method 1 · The full math'),
    S('Method 2 · Plugging in numbers',
      L("[pause] Another way, and here it's the recommended one. What's different? No letters at all. The choices are plain "
        "numbers, so one plug-in is enough. a is positive, take one. Diamond of one, one is the root of nine, three.",
        show(b5, 'take one')),
      L("Top, diamond of three, one. Three is in the first slot, eight times nine is seventy-two, and seventy-two "
        "plus one is seventy-three, so root seventy-three. Some students stop here, only choice number three has seventy-three on top. Bottom, diamond of one, "
        "three. Eight plus nine, root seventeen. Choice number three. With unknowns in an operation, plugging in is the "
        "way. [pause] Okay. I'll see you in the next question.", show(b6, 'Top, diamond of three'),
        mk('tick', 'choice 3', 'Eight plus nine, root seventeen'))),
])

# ------------------------------------------------------------------------------------------------ q-553 (Hebrew Q4)
# NEW: don't open squared brackets early - they may cancel; (a - b)² = (b - a)²; check the choices differ before plugging
# in (her a = 1, b = 2 tie; here 1 and 2 are distinct).  Hebrew: the full math, the insight, plugging in (three methods).
c5 = I('c5', '$\\frac{(a-b)^2}{ab^3}\\cdot\\frac{ba^3}{(b-a)^2}$', hand='{(a − b)^2/ab^3} · {ba^3/(b − a)^2}')
c6 = I('c6', '$=\\frac{a^2}{b^2}$', hand='= {a^2/b^2}')
d5 = I('d5', '$(a-b)^2=(b-a)^2$', hand='(a − b)^2 = (b − a)^2')
d6 = I('d6', '$\\frac{ba^3}{ab^3}=\\frac{a^2}{b^2}$', hand='{ba^3/ab^3} = {a^2/b^2}')
e5 = I('e5', '$a=1,\\ b=2$: $\\ 1,\\ \\frac12,\\ \\frac14,\\ 4$ $\\ $(all different)', size=32, hand='a = 1,   b = 2 :    1,   {1/2},   {1/4},   4    (all different)')
e6 = I('e6', '$\\blacklozenge(1,2)=\\frac18 \\quad \\blacklozenge(2,1)=\\frac12 \\quad \\frac18\\div\\frac12=\\frac14$', size=32, hand='◆(1, 2) = {1/8}      ◆(2, 1) = {1/2}      {1/8} ÷ {1/2} = {1/4}')
video('solve-q-553', 'solution', qid='q-553', slides=[
    S('Method 1 · The full math',
      L("For every two numbers x and y that are not zero, diamond of x, y is x minus y, squared, over x times y cubed. Given: "
        "a and b are two different numbers, and neither of them is zero. Diamond of a, b over diamond of b, a is equal to "
        "what?", pt('stem', 'For every two numbers', 'hl', 11.0), voice='calm', pause=0.5),
      L("A hard one. [short pause] We'll solve it three ways, the full math, a sharp insight, and plugging in numbers.",
        pt('stem', 'A hard one')),
      L("[short pause] Top, diamond of a, b, a minus b, squared, over a b cubed. Bottom, diamond of b, a, b minus a, squared, "
        "over b a cubed. Dividing by a fraction, multiply by its reciprocal.", show(c5, 'Dividing by a fraction')),
      L("And a tip. Don't open the squared brackets, they might cancel. And they do. Then one a and one b cancel, and we're "
        "left with a squared over b squared. Choice number three is our answer.", show(c6, 'a squared over b squared'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · A sharp insight',
      L("[pause] Another way, for students who see the algebra. What's different? We notice it's the same two letters, just "
        "swapped. The tops are a minus b and b minus a, squared. Opposites, squared, are equal, so the tops cancel.",
        show(d5, 'Opposites, squared')),
      L("Only the bottoms are left, and dividing flips the second one. b a cubed over a b cubed. a squared over b squared. "
        "Choice number three.", show(d6, 'b a cubed over'), mk('tick', 'choice 3', 'a squared over b squared. Choice'))),
    S('Method 3 · Plugging in numbers',
      L("[pause] And the standard psychometric way, plugging in. What's different? No algebra at all. Letters in the choices, "
        "so first make sure they come out different. a and b can't be equal or zero. a is one, b is two. The choices give "
        "one, one half, one quarter and four. All different.", show(e5, 'a is one, b is two')),
      L("Top, one minus two, squared, is one, over one times eight, one eighth. Bottom, two minus one, squared, is one, over two times one, which is two. One half. One "
        "eighth divided by one half is one quarter. Choice number three. Strong in algebra? The insight. Everyone else, just "
        "plug in. [pause] Okay. I'll see you in the next question.", show(e6, 'Top, one minus two'),
        mk('tick', 'choice 3', 'is one quarter. Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-554 (Hebrew Q5)
# NEW: an operation on digits (two topics in one); the shortcut: the biggest power needs the smallest digit (min/max).
# Hebrew: the standard way, the insight.
f5 = I('f5', '(1) $214$: $\\ 16+1+16=33$', hand='(1)   214 :    16 + 1 + 16 = 33')
f6 = I('f6', '(2) $142$: $\\ 1+64+4=69$ $\\quad$ (3) $412$: $\\ 256+1+4=261$', size=32, hand='(2)   142 :    1 + 64 + 4 = 69      (3)   412 :    256 + 1 + 4 = 261')
f7 = I('f7', '(4) $124$: $\\ 1+8+16=25$', hand='(4)   124 :    1 + 8 + 16 = 25')
g5 = I('g5', 'Power $4$ on the hundreds: $\\ $smallest digit, $1$', size=32, hand='Power 4 on the hundreds :    smallest digit,  1')
g6 = I('g6', 'Power $3$ on the tens: $\\ 2$, not $4$: $\\ 124$', size=32, hand='Power 3 on the tens :    2,  not 4 :    124')
video('solve-q-554', 'solution', qid='q-554', slides=[
    S('Method 1 · The standard way',
      L("A, B and C are digits from one to nine. For every three-digit number A B C, the operation diamond is defined. Diamond "
        "of A B C is A to the fourth, plus B cubed, plus C squared. Which of the following is the smallest?",
        pt('stem', 'A, B and C', 'hl', 9.0), voice='calm', pause=0.5),
      L("Two topics in one, digits and a defined operation. And every choice has the operation, so we evaluate the choices. "
        "[short pause] We'll solve it two ways, the standard way, and then a shortcut.", pt('stem', 'Two topics in one')),
      L("[short pause] The hundreds digit to the fourth, the tens cubed, the units squared. Two one four, two to the fourth is "
        "sixteen, one cubed is one, four squared is sixteen. Thirty-three.", show(f5, 'Two one four')),
      L("One four two, one, sixty-four, four, sixty-nine. Bigger, out. Four one two, two fifty-six, one, four, two sixty-one. "
        "Out.", show(f6, 'One four two'), mk('cross', 'choice 2', 'sixty-nine. Bigger, out'), mk('cross', 'choice 3', 'two sixty-one')),
      L("One two four, one, eight, sixteen, twenty-five. Smaller than thirty-three, so choice number one is out too. Choice "
        "number four is our answer.", show(f7, 'One two four'), mk('cross', 'choice 1', 'choice number one is out too'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Think minimum',
      L("[pause] Another way. What's different? We think about where the big power goes, instead of calculating. Every "
        "choice uses the same digits, one, two and four. The biggest power, the fourth, sits on the hundreds digit, so that "
        "digit must be the smallest, one. Choice numbers one and three are out.", show(g5, 'The biggest power'),
        mk('cross', 'choice 1', 'Choice numbers one'), mk('cross', 'choice 3', 'and three are out')),
      L("The next power, the cube, sits on the tens, so the smaller of what's left, two. One two four. Choice number four, "
        "with no full calculation. [pause] Okay. I'll see you in the next question.", show(g6, 'The next power'),
        mk('tick', 'choice 4', 'One two four. Choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-555 (Hebrew Q6)
# NEW: "must be true for all positive a, b" - break each choice; technically (multiply by a positive, no flip) and by
# understanding (3/x is 3 times the reciprocal; a bigger denominator, a smaller fraction).  Hebrew: the technical way and
# the understanding, choice by choice -> two methods here; the wrong choices first, so each ends on the answer.
h6 = I('h6', '(1) $\\frac3a<3\\ \\to\\ 1<a$: $\\ a=\\frac12$: $\\ 6$ ✗', size=32, hand='(1)   {3/a} < 3   →   1 < a :    a = {1/2} :   6   ✗')
h7 = I('h7', '(3) $\\frac3a\\div\\frac3b=\\frac ba$ ✗', hand='(3)   {3/a} ÷ {3/b} = {b/a}   ✗')
h8 = I('h8', '(4) $\\frac3a<\\frac3{a+1}\\ \\to\\ a+1<a$ ✗', size=32, hand='(4)   {3/a} < {3/a + 1}   →   a + 1 < a   ✗')
h9 = I('h9', '(2) $\\frac3a\\cdot a=3=\\frac3b\\cdot b$ ✓', hand='(2)   {3/a} · a = 3 = {3/b} · b   ✓')
i6 = I('i6', '(1) $a=2,\\ 3$: $\\ \\frac32,\\ 1$ $\\quad a=1$: $\\ 3$ $\\quad a=\\frac12$: $\\ 6$', size=30, hand='(1)   a = 2, 3 :   {3/2},  1      a = 1 :   3      a = {1/2} :   6')
i7 = I('i7', '(3) $\\frac3x=3x^{-1}$: $\\ $a minus power flips', size=30, hand='(3)   {3/x} = 3x^{−1} :    a minus power flips')
i8 = I('i8', '(4) bigger denominator, smaller fraction: $\\ \\frac32>1$', size=30, hand='(4)   bigger denominator,  smaller fraction :    {3/2} > 1')
i9 = I('i9', '(2) a number times its reciprocal is $1$: $\\ 3\\cdot1=3$', size=30, hand='(2)   a number times its reciprocal is 1 :    3·1 = 3')
video('solve-q-555', 'solution', qid='q-555', slides=[
    S('Method 1 · Technically',
      L("For every number x that's not zero, diamond of x is three over x. Which of the following must be true for all "
        "positive a and b?", pt('stem', 'For every number x', 'hl', 6.0), voice='calm', pause=0.5),
      L("A hard one. Must be true, so we try to break each choice. [short pause] We'll solve it two ways, technically, and "
        "then by understanding.", pt('stem', 'must be true')),
      L("[short pause] Let's start technically. Choice number one, three over a is smaller than three. a is positive, so "
        "multiply by a with no flip, and divide by three. One is smaller than a. True only when a is above one, and a could "
        "be one half, then three over a is six. Out.", show(h6, 'Choice number one, three over a'), mk('cross', 'choice 1', 'is six. Out')),
      L("Choice number three, three over a divided by three over b. Multiply by the reciprocal, b over a, not a over b. Out.",
        show(h7, 'Choice number three'), mk('cross', 'choice 3', 'not a over b. Out'))),
    S('Method 1 · Technically',
      L("Choice number four, three over a smaller than three over a plus one. Both are positive, so cross-multiply with no "
        "flip and divide by three. a plus one smaller than a, so one smaller than zero. Never true. Out.", show(h8, 'Choice number four'),
        mk('cross', 'choice 4', 'Never true. Out')),
      L("Choice number two, three over a, times a. The a cancels, three. And three over b times b, three too. Three equals "
        "three for every a and b. Choice number two is our answer.", show(h9, 'Choice number two'),
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      sb='Method 1 · Technically'),
    S('Method 2 · By understanding',
      L("[pause] Another way. What's different? We read what the diamond does, instead of moving terms. Choice number one. "
        "For a above one it's true, two gives three halves, three gives one. But a equal to one gives three, and one half "
        "gives six.", show(i6, 'For a above one')),
      L("Choice number three. Three over x is three times x to the negative one, and a minus power means flip. So b over a. "
        "Choice number four. A bigger denominator makes a smaller fraction. a is two, three halves is not smaller than one.",
        show(i7, 'three times x to'), show(i8, 'A bigger denominator')),
      L("Choice number two. Three over a is three times the reciprocal of a, and a number times its reciprocal is one. So "
        "three, every time. Choice number two. [pause] Okay. I'll see you in the next question.", show(i9, 'its reciprocal is one'),
        mk('tick', 'choice 2', 'three, every time. Choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-556 (Hebrew Q7)
# NEW: a definition in words - write examples first (50 -> two 5s; 75, 7); x = 1 knocks out three; why: x5 adds exactly one
# five, squaring doubles the count, adding 5 says nothing.  REMINDER: prime factorization (topic 14).
# Hebrew: plugging in numbers, understanding.
j5 = I('j5', '$50=2\\cdot5\\cdot5$: $\\ 2 \\qquad 75=3\\cdot5\\cdot5$: $\\ 2 \\qquad 7$: $\\ 0$', size=32)
j6 = I('j6', '$x=1$: $\\ $(1) $1\\ne0$ ✗ $\\quad$ (2) $0\\ne1$ ✗ $\\quad$ (3) $1\\ne0$ ✗', size=32)
j7 = I('j7', '(4) $⟦5⟧=1=0+1$ ✓', size=34)
k5 = I('k5', '$\\times5$: $\\ $one more five $\\quad +5$: $\\ $says nothing', size=32)
k6 = I('k6', 'Squaring doubles the count $\\quad x=5^3$: $\\ 4\\ne15$', size=32)
video('solve-q-556', 'solution', qid='q-556', slides=[
    S('Method 1 · Plugging in numbers',
      L("For every positive integer x, the double bracket of x is the number of times five appears in the prime "
        "factorization of x. For example, fifty is two times five times five, it has two fives, so the double bracket of "
        "fifty is two. Which of the following must be true?", pt('stem', 'For every positive integer x', 'hl', 11.0), voice='calm', pause=0.5),
      L("Operations meet prime numbers. [short pause] We'll solve it two ways, plugging in numbers, and then by "
        "understanding.", pt('stem', 'Operations meet prime numbers')),
      L("[short pause] A definition in words is easy to misread, so a few examples first. Fifty has two fives. Seventy-five "
        "is three times five times five, two fives as well. And seven has no fives, zero.", show(j5, 'a few examples first')),
      L("Now plug in the simplest value, x is one, no fives at all. Choice number one, five has one five, and one squared has "
        "none. One against zero. Out. Choice number two, six has none, but zero plus one is one. Out. Choice number three, one "
        "against five times zero. Out.", show(j6, 'x is one, no fives'), mk('cross', 'choice 1', 'One against zero. Out'),
        mk('cross', 'choice 2', 'zero plus one is one. Out'), mk('cross', 'choice 3', 'five times zero. Out')),
      L("Choice number four, five has one five, and zero plus one is one. True. Three are out, so choice number four is our "
        "answer. One is a risky number, it can make a false rule look true, but here three failed and one survived.",
        show(j7, 'Choice number four, five has'), mk('tick', 'choice 4', 'choice number four is our'))),
    S('Method 2 · Understanding',
      L("[pause] Now why. What's different? We reason about the factors instead of trying numbers. Choice number two adds "
        "five, and adding says nothing about the factors. Choice number one squares x, and squaring doubles the number of "
        "fives.", show(k5, 'adds five')),
      L("Choice number three multiplies the count by five. x is five cubed, times five gives four fives, not fifteen.",
        show(k6, 'multiplies the count')),
      L("And choice number four. Multiply x by five, and you add exactly one more five to its factors. So the count goes up "
        "by exactly one, every time. Choice number four. [pause] Okay. I'll see you in the next question.",
        mk('tick', 'choice 4', 'by exactly one, every time'))),
])

# ------------------------------------------------------------------------------------------------ r26-t19-summary
# REMINDERS only, said the way they were taught; new numbers.
s1s = I('s1s', '$a\\heartsuit b=3(a+b)$: $\\ 4\\heartsuit2=18$ $\\quad 2\\star5\\ne5\\star2$', size=34)
s2s = I('s2s', '$\\blacklozenge(x)=x^2-5x$: $\\ \\blacklozenge(-2)=4+10=14$', size=34)
s3s = I('s3s', 'Operation first $\\quad$ nested: inside out', size=34)
s4s = I('s4s', '$F(4t)=t+3$: $\\ F(20)$: $\\ t=5$, $\\ 8$', size=34)
s5s = I('s5s', 'No definition? Test each choice $\\quad$ unknown input? An equation', size=32)
s6s = I('s6s', 'Conditions: which rule, at every step $\\quad$ backwards: does it fit?', size=32)
s7s = I('s7s', 'Circular: down to the start, back up $\\quad$ both sides: isolate', size=32)
s8s = I('s8s', 'Not always: one example $\\quad$ always: swap the letters', size=32)
s9s = I('s9s', 'Undo themselves: $\\ c-x,\\ \\frac cx$ $\\quad$ inverse: reverse order', size=32)
s10s = I('s10s', '$\\blacklozenge(k)-\\blacklozenge(-k)$: $\\ $odd powers, doubled $\\quad$ shortcut formulas', size=32)
video('r26-t19-summary', 'lesson', slides=[
    S('Defining a New Operation: Summary',
      L("Before you practice, here's a quick summary of the topic. Reading a definition, the types, and the shortcuts.")),
    S('Read, then substitute',
      L("A new operation is just a definition. Read it, then follow the whole recipe. a heart b is three times a plus b, so "
        "four heart two is eighteen. And the order can matter, two star five isn't always five star two.", show(s1s, 'A new operation')),
      L("Whatever goes in, goes in brackets. Diamond of x is x squared minus five x, so diamond of negative two is four plus "
        "ten, fourteen.", show(s2s, 'goes in brackets')),
      L("Inside a longer exercise, turn each operation into a number first. Nested? Inside out, and don't stop halfway.",
        show(s3s, 'turn each operation'))),
    S('The types',
      L("The operation works on an expression? Match the whole input first. F of four t is t plus three, so for F of twenty, t "
        "is five, and the answer is eight.", show(s4s, 'Match the whole input')),
      L("No definition? Put the input into each choice. An unknown input? Write the definition, and it's an equation.",
        show(s5s, 'No definition')),
      L("Conditions? Check which rule at every step. Backwards? Try every rule, and keep an answer only if it fits.",
        show(s6s, 'Conditions')),
      L("Circular? Go down to the start value, then climb back up. On both sides? Isolate it like an unknown.",
        show(s7s, 'Circular'))),
    S('Always, must, shortcuts',
      L("Not always? One example. Always? Swap the letters. Must be true? Plug in, but not zero, one or equal values, and try "
        "a second number if two survive. And a must-be-true question can eat your time, skip it and come back.",
        show(s8s, 'Not always')),
      L("Two families undo themselves, c minus x and c over x. An inverse operation undoes the steps in reverse order.",
        show(s9s, 'Two families')),
      L("A number minus its opposite? The even powers cancel, the odd ones double. And look for the shortcut formulas. "
        "[pause] That's it. Now go practice, and I'll see you in the next video.", show(s10s, 'A number minus its opposite'))),
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



for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _stem_parts(_v); _write_gap(_v)


if __name__ == '__main__':
    _bad = 0
    for _v in sys.argv[1:] or ORDER:
        _p = check(_v)
        if _p: print('PROBLEMS', _v, _p); _bad += 1
        print('script written:', write_json(_v), stats(_v))
    for x in WRITE_LATE: print('mark dropped (its item is still being written):', x)
    sys.exit(1 if _bad else 0)
