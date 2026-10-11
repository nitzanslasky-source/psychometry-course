"""Topic 17 (The Number Line) - the redo for the teacher's own-voice reading (2026-10-12), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py / _ai_vis_t16.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The teacher records only the camera lesson 'number-line' (re-record, never touched here). Every other topic-17 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t17.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t17.py ai_redo_t17() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods and EVERY method of the Hebrew solution (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-17-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t17ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-17 flow order of the scripts (number-line = the camera lesson, not here)
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
            'style': "the teacher reads it herself (Reading Studio), topic-17 redo (2026-10-12): math_patches/_ai_vis_t17.py is "
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

# ------------------------------------------------------------------------------------------- topic-17 figures
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

# ------------------------------------------------------------------------------------------------ q-493 (Hebrew: lesson 1 example)
# REMINDER: strong on strong, x a number above one makes it bigger ("an energy drink") - camera lesson.  Hebrew: one method
# (strong on strong); a plugging-in method is added.
a1 = I('a1', 'Strong on strong, weak on weak', size=28, col=1)
a2 = I('a2', '$2\\cdot3$ vs $4\\cdot5$: $\\ 4>2,\\ 5>3$', size=30, col=1, hand='2·3  vs  4·5 :    4 > 2,   5 > 3')
a3 = I('a3', '(1) $p\\cdot q$ vs $r\\cdot r$: $\\ r>p,\\ r>q$ ✓', size=32, hand='(1)   p·q  vs  r·r :    r > p,   r > q   ✓')
a4 = I('a4', '(2) $s>q$, $\\ \\times p>1$: $\\ sp>q$ ✓', size=32, hand='(2)   s > q,    × p > 1 :    sp > q   ✓')
a5 = I('a5', '(3) $r>q$, $\\ \\times p>1$: $\\ \\hl{n}{rp>q}$ ✗', size=32, hand='(3)   r > q,    × p > 1 :    \\hl{n}{rp > q}   ✗')
b1 = I('b1', '$p=2,\\ q=3,\\ r=4,\\ s=5$', hand='p = 2,   q = 3,   r = 4,   s = 5')
b2 = I('b2', '(1) $6<16$ ✓ $\\quad$ (2) $3<10$ ✓ $\\quad$ (3) $8<3$ ✗', size=30, hand='(1)   6 < 16  ✓      (2)   3 < 10  ✓      (3)   8 < 3  ✗')
video('solve-q-493', 'solution', qid='q-493', slides=[
    S('Method 1 · Strong on strong',
      L("Given: one is smaller than p, which is smaller than q, which is smaller than r, which is smaller than s. Which of "
        "the following statements is not correct?", pt('stem', 'Given', 'hl', 7.0), voice='calm', pause=0.5),
      L("So four letters, all bigger than one, in order. And we look for the statement that's not correct. [short pause] "
        "We'll solve it two ways, strong on strong, and then plugging in numbers.", pt('stem', 'all bigger than one')),
      L("[short pause] Let's start with strong on strong. When you compare two products, match the big factor against the "
        "big one, and the small against the small. If one side wins both, it's bigger. For example, two times three "
        "against four times five. Four beats two, and five beats three, so four times five is bigger.",
        show(a1, 'match the big factor'), show(a2, 'two times three')),
      L("Choice number one. p times q against r squared, which is r times r. r beats p, and r beats q. The right side wins "
        "both, so p q is smaller. It's correct. Out.", show(a3, 'r squared, which is'), mk('cross', 'choice 1', "It's correct. Out")),
      L("Choice number two. q against s times p. Forget p for a second, s already beats q. And times p, a number bigger "
        "than one, s only gets bigger. So q is smaller. Correct. Out.", show(a4, 's already beats q'),
        mk('cross', 'choice 2', 'So q is smaller. Correct')),
      L("Choice number three. r times p against q. r already beats q, and times p, it gets even bigger. So r times p is "
        "bigger than q, but the statement says smaller. It's not correct, so choice number three is our answer.",
        show(a5, 'r already beats q'), mk('tick', 'choice 3', 'choice number three is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers in this order, all bigger than one. p is two, q is three, r is four, and "
        "s is five.", show(b1, 'p is two')),
      L("Choice number one, two times three is six, and four squared is sixteen. Six is smaller, correct. Choice number two, "
        "five times two is ten, and three is smaller, correct. Choice number three, four times two is eight, and eight "
        "isn't smaller than three. Not correct. So choice number three. [pause] Okay. I'll see you in the next question.",
        show(b2, 'Choice number one, two times'), mk('cross', 'choice 1', 'Six is smaller, correct'),
        mk('cross', 'choice 2', 'and three is smaller, correct'), mk('tick', 'choice 3', 'So choice number three'))),
])

# ------------------------------------------------------------------------------------------------ powers-on-number-line (lesson)
# NEW: the arrows (above 1 ->, 0..1 <-, -1..0 -> odd, below -1 <- odd), two examples each; a root = a smaller power;
# what counts as odd; the three steps (exceptions, roots -> powers, arrows; keep a negative power); finding the range
# (x < x^5 < x^4).  REMINDER: the four ranges, exceptional powers (camera lesson).
ar = ZL('ar', -2, 2, [('r4', [('arrow', 1.2, 1.85, '')]), ('r3', [('arrow', 0.8, 0.15, '')]),
                       ('r2', [('arrow', -0.8, -0.15, 'odd')]), ('r1', [('arrow', -1.2, -1.85, 'odd')])], w=900)
c1 = I('c1', 'Right $=$ bigger $\\quad$ Left $=$ smaller', size=34)
d1 = I('d1', '$2<4<8 \\qquad 3<9<27$', size=40, hand='2 < 4 < 8        3 < 9 < 27')
d2 = I('d2', '$1<x$: $\\ \\sqrt x<x<x^2<x^3$', size=40, hand='1 < x :    √{x} < x < x^2 < x^3')
e1 = I('e1', '$\\frac12>\\frac14 \\qquad \\frac13>\\frac19>\\frac1{27}$', size=40, hand='{1/2} > {1/4}        {1/3} > {1/9} > {1/27}')
e2 = I('e2', '$\\left(\\frac37\\right)^2=\\frac9{49}<\\frac37$', size=40, hand='({3/7})^2 = {9/49} < {3/7}')
e3 = I('e3', '$0<x<1$: $\\ x^3<x^2<x<\\sqrt x$', size=40, hand='0 < x < 1 :    x^3 < x^2 < x < √{x}')
f1 = I('f1', '$\\left(-\\frac12\\right)^3=-\\frac18 \\qquad \\left(-\\frac13\\right)^3=-\\frac1{27}$', size=38, hand='(−{1/2})^3 = −{1/8}        (−{1/3})^3 = −{1/27}')
f2 = I('f2', 'Even: $\\ \\left(-\\frac12\\right)^2=\\frac14>0$', size=36, hand='Even :    (−{1/2})^2 = {1/4} > 0')
f3 = I('f3', 'Odd: $\\ 3,\\ 5,\\ -1,\\ -3,\\ \\frac13,\\ \\frac15$', size=38, hand='Odd :    3,   5,   −1,   −3,   {1/3},   {1/5}')
g1 = I('g1', '$(-2)^3=-8 \\qquad (-3)^3=-27$', size=40, hand='(−2)^3 = −8        (−3)^3 = −27')
g2 = I('g2', 'Even powers jump to the positive side', size=32)
h1 = I('h1', '1 · Exceptions: a negative to an even power $\\to$ positive', size=32)
h2 = I('h2', '2 · Roots $\\to$ powers: $\\ \\sqrt[5]{x}=x^{\\frac15}$', size=32)
h3 = I('h3', '3 · The line and its arrows (keep a negative power)', size=32)
i1 = I('i1', 'Given: $\\ x<x^5<x^4$', size=40, hand='Given :    x < x^5 < x^4')
fr = ZL('fr', -2, 2, [('k1', [('cross', -1.5), ('cross', 0.5)]), ('k2', [('cross', 1.5)]), ('k3', [('shade', -1, 0), ('below', -0.5, 'x')])], w=900)
video('powers-on-number-line', 'lesson', slides=[
    S('Powers on the Number Line',
      L("Welcome back. Last time we saw the four ranges, and what multiplying and dividing do in each one. Now, what powers "
        "do in each range. The method looks a little strange at first, but practice it a bit, and it becomes one of your "
        "fastest tools.")),
    S('The arrows',
      L("Draw the number line with its four ranges. Below negative one, negative fractions, positive fractions, and above "
        "one. Each range gets an arrow, and the arrow shows where a number moves when the power gets bigger.",
        show(ar['line'], 'Draw the number line')),
      L("Above one, the arrow points right. Positive fractions, left.", show(ar['r4'], 'Above one'), show(ar['r3'], 'Positive fractions')),
      L("Negative fractions, right, and below negative one, left. On the negative side, only for odd powers.",
        show(ar['r2'], 'Negative fractions, right'), show(ar['r1'], 'below negative one, left')),
      L("Right means bigger, and left means smaller. And the bigger the power, the further you go along the arrow.",
        show(c1, 'Right means bigger'))),
    S('Above one',
      L("Above one, the arrow points right, so a bigger power gives a bigger number. Two, two squared is four, and two "
        "cubed is eight. Three, nine, twenty-seven. Bigger and bigger.", show(d1, 'Two, two squared')),
      L("And a square root is a power of one half, a smaller power. So it's smaller than x, but still above one. The square "
        "root of four is two, and the square root of nine is three. And exactly at one? They're all one. That's why the "
        "borders matter.", show(d2, 'a square root is a power'))),
    S('Positive fractions',
      L("Positive fractions, the arrow points left, so a bigger power gives a smaller number. One half squared is one "
        "quarter, smaller. One third squared is one ninth, and cubed, one twenty-seventh.", show(e1, 'One half squared')),
      L("And a less round one, three sevenths. Three sevenths squared is nine forty-ninths. Which is bigger? Don't "
        "calculate. The power went up, and the arrow points left, so the square is smaller.", show(e2, 'three sevenths squared')),
      L("The root goes the other way, it makes a positive fraction bigger. The square root of one ninth is one third. In the "
        "exam there'll be letters, not numbers, and that's exactly where the arrows save you.", show(e3, 'The root goes the other way'))),
    S('Negative fractions',
      L("Negative fractions, the arrow points right, for odd powers. Negative one half, cubed, is negative one eighth. That's "
        "to the right of negative one half, closer to zero. And negative one third cubed is negative one twenty-seventh, "
        "right again.", show(f1, 'Negative one half, cubed')),
      L("Why odd only? An even power makes a negative number positive. It jumps to the other side, and every positive beats "
        "every negative. Negative one half squared is one quarter, positive.", show(f2, 'An even power makes')),
      L("What counts as odd? Any power that keeps the minus. Three and five, negative one and negative three, and odd roots "
        "too. A cube root is a power of one third, and a fifth root is a power of one fifth.", show(f3, 'What counts as odd'))),
    S('Below negative one',
      L("Below negative one, the arrow points left, for odd powers. The number grows in size, but it stays negative, so it "
        "gets smaller. Negative two cubed is negative eight, and negative three cubed is negative twenty-seven.",
        show(g1, 'Negative two cubed')),
      L("And even powers jump to the positive side, so treat them on their own.", show(g2, 'even powers jump'))),
    S('Three steps',
      L("In a question that compares powers, work in three steps. First, exceptions. A negative number to an even power "
        "turns positive, it changes sides.", show(h1, 'First, exceptions')),
      L("Second, turn roots into powers, because a root gets in the way when you compare powers. The fifth root of x is x to "
        "the one fifth.", show(h2, 'turn roots into powers')),
      L("Third, draw the line and its arrows, and read the answer straight off. And a negative power? With the arrows, keep "
        "it. Negative one is just a small power.", show(h3, 'draw the line and its arrows'))),
    S('Finding the range',
      L("Sometimes it's the other way round. They give the order, and you find the range. For example, x is smaller than x "
        "to the fifth, which is smaller than x to the fourth.", show(i1, 'They give the order'), show(fr['line'], 'For example')),
      L("Take it in two parts. The left part, x is smaller than x to the fifth. The power went up, and the number went up. "
        "That's an arrow pointing right, above one or negative fractions. So below negative one and positive fractions are "
        "out.", show(fr['k1'], 'are out')),
      L("The right part, x to the fifth is smaller than x to the fourth. Above one, the bigger power would give the bigger "
        "number, so above one is out too. Only negative fractions are left.", show(fr['k2'], 'above one is out'),
        show(fr['k3'], 'Only negative fractions')),
      L("Why? x to the fourth is the exception, an even power, so it's positive, and it beats the negative x to the fifth. "
        "Questions like this are rarer, but they come up. You can always plug in numbers, but it takes time, and "
        "understanding each range solves these in seconds. [pause] Okay. I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ q-494 (Hebrew: lesson 2 example)
# REMINDER: the three steps, the arrows (lesson).  NEW at the step: the arrows already handle a negative power.
# Hebrew: one method (the three steps).
j1 = I('j1', '(3) $m^8>0$ ✗', hand='(3)   m^8 > 0   ✗')
j2 = I('j2', '(4) $\\sqrt[5]{m}=m^{\\frac15}$', hand='(4)   m^{1/5}')
jz = ZL('jz', -1.6, 0.6, [('a', [('shade', -1, 0), ('arrow', -0.85, -0.15, 'odd')])], ticks=(-1, 0), w=540, col=1)
j3 = I('j3', 'Powers: $\\ 3,\\ \\hl{s}{-3},\\ \\frac15$', hand='Powers :    3,    \\hl{s}{−3},    {1/5}')
j4 = I('j4', '$m=-\\frac12$: $\\ m^{-3}=(-2)^3=-8$', size=32, col=1, hand='m = −{1/2} :    m^{−3} = (−2)^3 = −8')
jz['line']['_y'] = jz['a']['_y'] = 250; j4['_y'] = 430
video('solve-q-494', 'solution', qid='q-494', slides=[
    S('Three steps',
      L("Given: negative one is smaller than m, which is smaller than zero. Which of the following expressions is the "
        "smallest?", pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("So m is a negative fraction, and the choices are powers and a root. [short pause] We'll solve it with the three "
        "steps, exceptions, roots into powers, and the arrows.", pt('stem', 'm is a negative fraction')),
      L("[short pause] First, exceptions. Is there a negative number to an even power? Yes, m to the eighth. It turns "
        "positive, and the others stay negative. We want the smallest, so a positive one is out.",
        show(j1, 'm to the eighth'), mk('cross', 'choice 3', 'a positive one is out')),
      L("Second, roots into powers. The fifth root of m is m to the one fifth.", show(j2, 'The fifth root of m')),
      L("Third, the line. m is a negative fraction, and there the arrow points right. A bigger power, a bigger number. So the "
        "smallest number has the smallest power.", show(jz['line'], 'Third, the line'), show(jz['a'], 'the arrow points right')),
      L("The powers are three, negative three, and one fifth. The smallest is negative three. And notice, the arrows already "
        "handle a negative power, no need to flip it. So m to the negative three, choice number two is our answer.",
        show(j3, 'The powers are'), mk('tick', 'choice 2', 'choice number two is our answer')),
      L("Let's see it in numbers. m is negative one half. m to the negative three flips it, negative two, cubed, negative "
        "eight. Far below the others, which are all between negative one and zero. [pause] Okay. I'll see you in the next "
        "question.", show(j4, 'm is negative one half'))),
])

# ------------------------------------------------------------------------------------------------ r26-t17-reading-the-line (lesson)
# NEW: times a negative jumps to the other side of zero and flips the order (3, 7 -> -3, -7; 2, 5 -> -4, -10).
# REMINDER: multiplying an inequality by a negative flips it (topic 12).  (Reciprocals: taught in q-r26-t17-03; testing
# at the edges: q-r26-t17-04; a picture of the line: q-r26-t17-01.)
tn = ZL('tn', -8.5, 8.5, [('a', [('ink', 3, '3'), ('ink', 7, '7')]), ('b', [('pt', -3, '−3'), ('pt', -7, '−7')])], ticks=(0,), w=900)
m1 = I('m1', '$3<7 \\ \\Rightarrow\\ -3>-7$', size=44, hand='3 < 7      ⇒      −3 > −7')
m2 = I('m2', '$2<5 \\ \\Rightarrow\\ -4>-10$', size=44, hand='2 < 5      ⇒      −4 > −10')
video('r26-t17-reading-the-line', 'lesson', slides=[
    S('Reading the Number Line',
      L("Welcome back. Before the advanced questions, one more move on the number line. Multiplying by a negative number.")),
    S('Times a negative',
      L("Times a positive number keeps a number on its side of zero. Times a negative number, it jumps to the other side, "
        "the mirror image. Three times negative one is negative three, and seven times negative one is negative seven.",
        show(tn['line'], 'Times a positive'), show(tn['a'], 'it jumps'), show(tn['b'], 'Three times negative one')),
      L("And look at the order. Three is smaller than seven, but negative three is bigger than negative seven. Times a "
        "negative, the order flips.", show(m1, 'look at the order')),
      L("One more. Two is smaller than five. Times negative two, they're negative four and negative ten. And negative four "
        "is the bigger one. The order flipped again.", show(m2, 'Two is smaller than five')),
      L("You know this from inequalities. Multiply both sides by a negative, and the sign flips. It's the same move. Now the "
        "advanced questions. Try each one first, and then watch. [pause] Okay. I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ q-495 (Hebrew Q1)
# NEW: smallest product of three factors above one = the smallest letters (a·a·a not a choice -> the closest, a·a·b);
# for "the smallest", one plug-in is enough.  REMINDER: x a number above one makes it bigger (camera lesson).
# Hebrew: understanding, plugging in numbers.
k1 = I('k1', '$a\\cdot a\\cdot c \\quad a\\cdot a\\cdot b \\quad a\\cdot b\\cdot c \\quad b\\cdot b\\cdot c$', hand='a·a·c      a·a·b      a·b·c      b·b·c')
k2 = I('k2', 'Smallest: $\\ a\\cdot a\\cdot a$ $\\ $(not a choice)', size=32, hand='Smallest :    a·a·a    (not a choice)')
k3 = I('k3', 'Closest: $\\ a\\cdot a\\cdot \\hl{b}{b}$ ✓', hand='Closest :    a·a·\\hl{b}{b}   ✓')
l1 = I('l1', '$a=2,\\ b=3,\\ c=5$', hand='a = 2,    b = 3,    c = 5')
l2 = I('l2', '(1) $20$ $\\quad$ (2) $12$ $\\quad$ (3) $30$ $\\quad$ (4) $45$', hand='(1)  20      (2)  12      (3)  30      (4)  45')
video('solve-q-495', 'solution', qid='q-495', slides=[
    S('Method 1 · Understanding',
      L("Given: one is smaller than a, which is smaller than b, which is smaller than c. Which of the following expressions "
        "is the smallest?", pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("So three letters, all bigger than one, and products in the choices. [short pause] We'll solve it two ways, by "
        "understanding, and then plugging in numbers.", pt('stem', 'all bigger than one')),
      L("[short pause] Let's start with understanding. Above one, multiplying makes a number bigger. And every choice is a "
        "product of three letters. a squared c is a times a times c, then a, a, b, then a, b, c, and b squared c is b, b, c.",
        show(k1, 'a squared c is')),
      L("When is a product of three letters the smallest? When each letter is as small as possible. The smallest letter is "
        "a, so the smallest product would be a times a times a. But a cubed isn't a choice.", show(k2, 'the smallest product would be')),
      L("So the closest to it. Two a's, and the smallest letter after a, which is b. Every other choice swaps a letter for a "
        "bigger one. So a times a times b, choice number two is our answer.", show(k3, 'Two a'),
        mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in. They ask for the smallest, so one plug-in is enough. a is two, b is three, and c "
        "is five.", show(l1, 'a is two')),
      L("Choice number one, four times five is twenty. Choice number two, four times three is twelve. Choice number three, "
        "two times three times five is thirty. Choice number four, nine times five is forty-five. The smallest is twelve, "
        "choice number two. [pause] Okay. I'll see you in the next question.", show(l2, 'Choice number one, four times'),
        mk('tick', 'choice 2', 'The smallest is twelve'))),
])

# ------------------------------------------------------------------------------------------------ q-496 (Hebrew Q2)
# NEW: place the givens on the line first; ÷ a positive fraction -> bigger, × a positive fraction -> smaller (examples);
# a difference = a distance; strong on strong with one win each = no decision -> break it at the edges.
# REMINDER: strong on strong (camera lesson).  Hebrew: understanding and algebra side by side -> two methods.
pl = ZL('pl', -0.35, 2.3, [('ab', [('pt', 0.3, 'a'), ('pt', 0.7, 'b')]), ('cd', [('pt', 1.4, 'c'), ('pt', 1.9, 'd')])], ticks=(0, 1), w=760)
n1 = I('n1', '(1) $\\div$ a fraction: bigger $\\quad 2\\div\\frac13=6$', size=30, hand='(1)   ÷ fraction ⇒ bigger :    2 ÷ {1/3} = 6')
n2 = I('n2', '(3) $\\times$ a fraction: smaller $\\quad 6\\cdot\\frac12=3$', size=30, hand='(3)   × fraction ⇒ smaller :    6 · {1/2} = 3')
n3 = I('n3', '(4) $d-a$: longer on both ends', size=30, hand='(4)   d − a :    longer on both ends')
n4 = I('n4', '(2) $d>c$ right, $\\ b>a$ left: $\\ $no decision', size=30, hand='(2)   d > c  right,    b > a  left :    no decision')
n5 = I('n5', '$a=\\frac14,\\ b=\\frac34,\\ c=2,\\ d=2\\frac14$: $\\ 2\\frac34>2\\frac12$ ✗', size=30, hand='a = {1/4},   b = {3/4},   c = 2,   d = 2{1/4} :    2{3/4} > 2{1/2}   ✗')
o1 = I('o1', '(1) $c<\\frac ca \\ \\Rightarrow\\ a<1$ ✓', hand='(1)   c < {c/a}    ⇒    a < 1   ✓')
o2 = I('o2', '(3) $bd<d \\ \\Rightarrow\\ b<1$ ✓', hand='(3)   bd < d    ⇒    b < 1   ✓')
o3 = I('o3', '(4) $c+a<d+b$: $\\ d>c,\\ b>a$ ✓', hand='(4)   c + a < d + b :    d > c,   b > a   ✓')
video('solve-q-496', 'solution', qid='q-496', slides=[
    S('Method 1 · Understanding',
      L("Given: zero is smaller than a, which is smaller than b, which is smaller than one, which is smaller than c, which is "
        "smaller than d. Which of the following statements is not necessarily true?", pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("So a and b are positive fractions, and c and d are bigger than one. Three statements are always true, and we look "
        "for the one that isn't. [short pause] We'll solve it two ways, by understanding, and then with algebra.",
        pt('stem', 'a and b are positive fractions')),
      L("[short pause] Let's start by placing them on the number line. a and b between zero and one, and c and d after one.",
        show(pl['line'], 'placing them'), show(pl['ab'], 'a and b between'), show(pl['cd'], 'c and d after one')),
      L("Choice number one, c over a. Dividing by a positive fraction moves a number away from zero, it gets bigger. Two "
        "divided by one third is six. So c over a is bigger than c. Always true. Out.", show(n1, 'Dividing by a positive fraction'),
        mk('cross', 'choice 1', 'bigger than c. Always true')),
      L("Choice number three, b times d. Multiplying by a positive fraction pulls a number toward zero, it gets smaller. "
        "Six times one half is three. So b d is smaller than d. Always true. Out.", show(n2, 'Multiplying by a positive fraction'),
        mk('cross', 'choice 3', 'smaller than d. Always true'))),
    S('Method 1 · Understanding',
      L("Choice number four, c minus b against d minus a. Each one is a distance on the line. d is further right than c, "
        "and a is further left than b, so the second distance is longer on both ends. Always true. Out.",
        show(n3, 'Each one is a distance'), mk('cross', 'choice 4', 'longer on both ends. Always true')),
      L("Three are out, so it's choice number two. In the exam you'd mark it and move on. Here, let's see why it can fail. "
        "c plus b against d plus a, strong on strong. The strong ones, d beats c, a win for the right side. The weak ones, "
        "b beats a, a win for the left side. One win each, so no decision.", show(n4, 'The strong ones')),
      L("So make it fail. c close to d, and b much bigger than a. a is one quarter, b is three quarters, c is two, and d is "
        "two and a quarter. c plus b is two and three quarters, and d plus a is two and a half. Two and three quarters isn't "
        "smaller. Not necessarily true, choice number two is our answer.", show(n5, 'a is one quarter'),
        mk('tick', 'choice 2', 'choice number two is our answer')),
      sb='Method 1 · Understanding'),
    S('Method 2 · Algebra',
      L("[pause] Another way is algebra. What's different? Instead of reading what each operation does, we simplify each "
        "statement until it's obvious. Choice number one, c is smaller than c over a. Multiply both sides by a, which is "
        "positive, and divide by c, also positive. a is smaller than one. True. Out.", show(o1, 'Multiply both sides by a'),
        mk('cross', 'choice 1', 'a is smaller than one. True')),
      L("Choice number three, b d is smaller than d. Divide both sides by d, which is positive. b is smaller than one. True. "
        "Out.", show(o2, 'Divide both sides by d'), mk('cross', 'choice 3', 'b is smaller than one. True')),
      L("Choice number four. Move the minuses across, and it's c plus a against d plus b. Strong on strong, d beats c, and "
        "weak on weak, b beats a. The right side wins twice. True. Out.", show(o3, 'Move the minuses across'),
        mk('cross', 'choice 4', 'The right side wins twice')),
      L("Three are always true, so choice number two. [pause] Okay. I'll see you in the next question.",
        mk('tick', 'choice 2', 'so choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-497 (Hebrew Q3)
# NEW: × a fraction pulls toward zero on BOTH sides - on the negative side that makes it bigger; signs first.
# REMINDER: the mirror image (camera lesson).  Hebrew: understanding, plugging in numbers (placed on the line).
p1 = I('p1', '$kn<0,\\ \\ k<0,\\ \\ kmn<0,\\ \\ km<0$', hand='kn < 0,     k < 0,     kmn < 0,     km < 0')
p2 = I('p2', '$\\times$ a fraction: toward $0$', size=30, col=1)
p3 = I('p3', 'Negative side: toward $0$ $=$ bigger', size=30, col=1)
q7 = ZL('q7', -1.35, 0.35, [('a', [('shade', -1, 0), ('arrow', -0.85, -0.12, 'bigger')])], ticks=(-1, 0), w=760)
r1 = I('r1', '$k=-\\frac13,\\ m=\\frac14,\\ n=\\frac12$', hand='k = −{1/3},    m = {1/4},    n = {1/2}')
r2 = I('r2', '(1) $-\\frac16$ $\\quad$ (2) $-\\frac13$ $\\quad$ (3) $-\\frac1{24}$ $\\quad$ (4) $-\\frac1{12}$', hand='(1)  −{1/6}      (2)  −{1/3}      (3)  −{1/24}      (4)  −{1/12}')
r7 = ZL('r7', -1.12, 0.14, [('a', [('pt', -0.78, '−1/3')]), ('b', [('pt', -0.52, '−1/6')]), ('c', [('pt', -0.28, '−1/12')]),
                             ('d', [('pt', -0.06, '−1/24')])], ticks=(-1, 0), w=760)
video('solve-q-497', 'solution', qid='q-497', slides=[
    S('Method 1 · Understanding',
      L("Given: negative one is smaller than k, which is smaller than zero, which is smaller than m, which is smaller than "
        "n, which is smaller than one. Which of the following expressions is the largest?", pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("So k is a negative fraction, and m and n are positive fractions. [short pause] We'll solve it two ways, by "
        "understanding, and then plugging in numbers.", pt('stem', 'k is a negative fraction')),
      L("[short pause] Let's start with the signs, maybe they knock something out. k n is negative times positive, negative. "
        "k is negative. k m n is negative times positive times positive, negative. And k m is negative. All four are "
        "negative, so the signs don't help.", show(p1, 'k n is negative')),
      L("So let's go deeper. Every choice is k, times some positive fractions. And multiplying by a fraction pulls a number "
        "toward zero. On the positive side, toward zero means smaller. On the negative side it's the mirror image, toward "
        "zero means bigger.", show(p2, 'pulls a number toward zero'), show(p3, 'On the negative side'),
        show(q7['line'], 'the mirror image'), show(q7['a'], 'toward zero means bigger')),
      L("k m n multiplies k by two fractions, so it's pulled the closest to zero. On the negative side, that's the largest. "
        "Choice number three is our answer.", mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] This idea isn't obvious, so let's see it with numbers. k is negative one third, m is one quarter, and n is "
        "one half.", show(r1, 'k is negative one third')),
      L("k n is negative one sixth. k is negative one third. k m n is negative one twenty-fourth. And k m is negative one "
        "twelfth.", show(r2, 'k n is negative one sixth')),
      L("On the number line, negative one third is the furthest from zero, then negative one sixth, then negative one "
        "twelfth, and negative one twenty-fourth is the closest. Closest to zero is the largest. Choice number three. "
        "[pause] Okay. I'll see you in the next question.", show(r7['line'], 'On the number line'),
        show(r7['a'], 'negative one third is the furthest'), show(r7['b'], 'then negative one sixth'),
        show(r7['c'], 'one twelfth'), show(r7['d'], 'twenty-fourth is the closest'),
        mk('tick', 'choice 3', 'Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-498 (Hebrew Q4)
# NEW at the step: a negative x is out at once (x^8 > 0 > x^7).  REMINDER: the arrows (lesson).
# Hebrew: the arrows, plugging in the answers.
s1 = I('s1', '$x<0$: $\\ x^8>0>x^7$ ✗', hand='x < 0 :    x^8 > 0 > x^7   ✗')
s8 = ZL('s8', -0.45, 2.1, [('up', [('arrow', 1.15, 1.85, '')]), ('x1', [('cross', 1.5)]), ('dn', [('arrow', 0.85, 0.15, ''), ('shade', 0, 1)])],
        ticks=(0, 1), w=760)
s2 = I('s2', '$0<x<1$: $\\ $bigger power, smaller', size=32, hand='0 < x < 1 :    bigger power,  smaller')
t1 = I('t1', '(2) $x=2$: $\\ 256<128$ ✗', hand='(2)   x = 2 :    256 < 128   ✗')
t2 = I('t2', '(4) $x=\\frac12$: $\\ \\frac1{256}<\\frac1{128}$ ✓', hand='(4)   x = {1/2} :    {1/256} < {1/128}   ✓')
video('solve-q-498', 'solution', qid='q-498', slides=[
    S('Method 1 · The arrows',
      L("Given: x to the power of eight is smaller than x to the power of seven. In which of the following ranges is x?",
        pt('stem', 'Given', 'hl', 5.0), voice='calm', pause=0.5),
      L("So it's about how powers behave, and the choices are ranges. [short pause] We'll solve it two ways, with the "
        "arrows, and then plugging in the answers.", pt('stem', 'the choices are ranges')),
      L("[short pause] Let's start with the arrows, and first the exception. If x were negative, x to the eighth, an even "
        "power, would be positive, and x to the seventh would be negative. A positive can't be smaller than a negative. So "
        "x is positive, and choice numbers one and three are out.", show(s1, 'If x were negative'),
        mk('cross', 'choice 1', 'choice numbers one'), mk('cross', 'choice 3', 'and three are out')),
      L("Now the positive side. Above one, the arrow points right, a bigger power gives a bigger number, so x to the eighth "
        "would be bigger. Out.", show(s8['line'], 'Now the positive side'), show(s8['up'], 'the arrow points right'),
        show(s8['x1'], 'would be bigger. Out'), mk('cross', 'choice 2', 'would be bigger. Out')),
      L("Positive fractions, the arrow points left, a bigger power gives a smaller number. So x to the eighth is smaller, "
        "just as given. Choice number four is our answer.", show(s8['dn'], 'the arrow points left'), show(s2, 'just as given'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's try plugging in the answers. Choice number two, x bigger than one, so take two. Two to the eighth "
        "is two fifty-six, and two to the seventh is one twenty-eight. Two fifty-six isn't smaller. Out.",
        show(t1, 'take two'), mk('cross', 'choice 2', "isn't smaller. Out")),
      L("Choice number four, a positive fraction, so take one half. One half to the eighth is one over two fifty-six, and to "
        "the seventh, one over one twenty-eight. One over two fifty-six is smaller, it works. And the negative ranges can't "
        "work, because an even power is positive. Choice number four. [pause] Okay. I'll see you in the next question.",
        show(t2, 'take one half'), mk('tick', 'choice 4', 'is positive. Choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-499 (Hebrew Q5)
# NEW: a smart plug-in = a number with a clean root (-1/8 for a cube root); the powers of a chain must keep one direction
# (no even power of a negative).  REMINDER: the arrows, what counts as odd (lesson).
# Hebrew: the arrows, plugging in numbers, a sharp shortcut (three methods).
u1 = I('u1', 'Powers: $\\ 7,\\ 1,\\ \\frac13,\\ -7$: $\\ $all odd ✓', hand='Powers :    7,   1,   {1/3},   −7 :    all odd   ✓')
uz = ZL('uz', -1.6, 0.6, [('a', [('shade', -1, 0), ('arrow', -0.85, -0.15, 'odd')])], ticks=(-1, 0), w=760)
u2 = I('u2', 'Biggest power $7$: $\\ y^7$ last', size=32, hand='Biggest power 7 :    y^7  last')
u3 = I('u3', 'Smallest power $-7$: $\\ y^{-7}$ first', size=32, hand='Smallest power −7 :    y^{−7}  first')
v1 = I('v1', '$y=-\\frac18$', hand='y = −{1/8}')
v2 = I('v2', '$y^7$: tiny $\\quad \\sqrt[3]{y}=-\\frac12 \\quad y^{-7}=(-8)^7$', size=32, hand='y^7 :  tiny       y^{1/3} = −{1/2}       y^{−7} = (−8)^7')
v3 = I('v3', '$y^{-7}$ by far the smallest: first', size=30, col=1)
w1 = I('w1', 'No even power of a negative: one direction', size=28, col=1)
w2 = I('w2', '(1) $1,\\ \\frac13,\\ 7,\\ -7$ ✗ $\\quad$ (2) $7,\\ -7,\\ \\frac13,\\ 1$ ✗', size=32, hand='(1)   1,  {1/3},  7,  −7   ✗        (2)   7,  −7,  {1/3},  1   ✗')
w3 = I('w3', '(4) $\\frac13,\\ -7,\\ 1,\\ 7$ ✗ $\\quad$ (3) $-7,\\ \\frac13,\\ 1,\\ 7$ ✓', size=32, hand='(4)   {1/3},  −7,  1,  7   ✗        (3)   −7,  {1/3},  1,  7   ✓')
video('solve-q-499', 'solution', qid='q-499', slides=[
    S('Method 1 · The arrows',
      L("Given: negative one is smaller than y, which is smaller than zero. Which of the following orders of y to the power "
        "of seven, y, the cube root of y, and y to the power of negative seven is correct?", pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("So y is a negative fraction, and we have to put four powers in order. [short pause] We'll solve it three ways, "
        "with the arrows, plugging in numbers, and a sharp shortcut.", pt('stem', 'y is a negative fraction')),
      L("[short pause] Let's start with the arrows. They're all powers, the cube root is a power of one third. y is a "
        "negative fraction, and there the arrow points right, as long as the powers are odd. Seven is odd, y is y to the "
        "one, odd, the cube root is an odd root, and negative seven is odd. So it works.", show(u1, 'They\'re all powers'),
        show(uz['line'], 'the arrow points right'), show(uz['a'], 'as long as the powers are odd')),
      L("Right means bigger. So the biggest power, seven, gives the biggest number, and y to the seventh must come last. "
        "Choice number one ends with y to the negative seven, and choice number two ends with y. Both out.",
        show(u2, 'the biggest power, seven'), mk('cross', 'choice 1', 'ends with y to the negative seven'),
        mk('cross', 'choice 2', 'Both out')),
      L("And the smallest power, negative seven, gives the smallest number, so it comes first. Choice number four starts "
        "with the root. Out. Choice number three starts with y to the negative seven, and it's our answer.",
        show(u3, 'the smallest power'), mk('cross', 'choice 4', 'starts with the root. Out'),
        mk('tick', 'choice 3', "and it's our answer"))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in. Usually negative one half is a good pick, but not here. The cube root of "
        "negative one half, with no calculator? So we pick a negative fraction with a clean cube root, negative one eighth.",
        show(v1, 'negative one eighth')),
      L("y to the seventh is a negative number with a huge denominator, so it's tiny, very close to zero. No need to "
        "calculate it. y is negative one eighth, and its cube root is negative one half. And y to the negative seven flips "
        "it, negative eight, to the seventh, a huge negative number.", show(v2, 'y to the seventh is')),
      L("So y to the negative seven is by far the smallest, and it comes first. Only choice number three starts with it. "
        "Choice number three.", show(v3, 'by far the smallest'), mk('tick', 'choice 3', 'Only choice number three'))),
    S('Method 3 · A sharp shortcut',
      L("[pause] And a sharp shortcut. What's different? We don't place anything, we only read the powers. With no even "
        "power of a negative number, the powers in a correct chain keep one direction, all up or all down. Write y as y to "
        "the one, and the root as y to the one third.", show(w1, 'keep one direction')),
      L("Choice number one, one, one third, seven, negative seven. Down, up, down. Impossible. Choice number two, seven, "
        "negative seven, one third, one. Down, then up. Impossible.", show(w2, 'Choice number one, one'),
        mk('cross', 'choice 1', 'Down, up, down'), mk('cross', 'choice 2', 'Down, then up. Impossible.')),
      L("Choice number four, one third, negative seven, one, seven. Down, then up again. Impossible. Choice number three, "
        "negative seven, one third, one, seven. Always up. Choice number three. [pause] Okay. I'll see you in the next "
        "question.", show(w3, 'Choice number four, one third'), mk('cross', 'choice 4', 'then up again'),
        mk('tick', 'choice 3', 'Always up'))),
])

# ------------------------------------------------------------------------------------------------ q-500 (Hebrew Q6)
# NEW: a root does the opposite of a power (a positive fraction gets bigger, still below 1); the swap - a number that
# sits in every choice the same way may be swapped for a small one (6 -> 2), never otherwise.
# REMINDER: x / ÷ a fraction, the arrows, hierarchy (camera lesson, lesson).  Hebrew: understanding, a smart plug-in.
x1 = I('x1', '(3) $0<t^6<t$', hand='(3)   0 < t^6 < t')
x2 = I('x2', '(4) $t<\\sqrt[6]{t}<1$', hand='(4)   t < t^{1/6} < 1')
x3 = I('x3', '(1) $6t<6$', hand='(1)   6t < 6')
x4 = I('x4', '(2) $\\frac6t>6$ ✓', hand='(2)   {6/t} > 6   ✓')
y1 = I('y1', 'The $6$ is in every choice: $\\ $swap it for $2$', size=28, col=1)
y2 = I('y2', '$2t,\\ \\ \\frac2t,\\ \\ t^2,\\ \\ \\sqrt t$', hand='2t,     {2/t},     t^2,     √{t}')
y3 = I('y3', '$t=\\frac19$: $\\ \\frac29,\\ \\ 18,\\ \\ \\frac1{81},\\ \\ \\frac13$', hand='t = {1/9} :    {2/9},    18,    {1/81},    {1/3}')
y4 = I('y4', 'Only when the same number is in every choice', size=28, col=1)
video('solve-q-500', 'solution', qid='q-500', slides=[
    S('Method 1 · Understanding',
      L("Given: zero is smaller than t, which is smaller than one. Which of the following expressions is the largest?",
        pt('stem', 'Given', 'hl', 5.0), voice='calm', pause=0.5),
      L("So t is a positive fraction, and four expressions. [short pause] We'll solve it two ways, by understanding, and "
        "then plugging in with a smart swap.", pt('stem', 't is a positive fraction')),
      L("[short pause] Let's start with understanding. Choice number three, t to the sixth. For a positive fraction the arrow "
        "points left, so a bigger power makes it smaller. But it stays positive. So it's between zero and t.",
        show(x1, 't to the sixth')),
      L("Choice number four, the sixth root. A root does the opposite of a power, it makes a positive fraction bigger. But "
        "it can't pass one, because there's no negative power to move it to another range. So it's between t and one.",
        show(x2, 'the sixth root')),
      L("Choice number one, six times t. Multiplying by a positive fraction makes a number smaller, so it's less than six.",
        show(x3, 'six times t')),
      L("Choice number two, six over t. Dividing by a positive fraction makes a number bigger, so it's more than six. Below "
        "one, below one, below six, and above six. Choice number two is our answer.", show(x4, 'six over t'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Plugging in with a swap',
      L("[pause] Now let's try plugging in. But t to the sixth, or the sixth root of a fraction, with no calculator? Hard. So "
        "here's a trick. The six sits in every choice, and it only tells us what kind of operation it is, a power, a root, "
        "times, or over. So swap every six for a two.", show(y1, 'swap every six')),
      L("Now it's two t, two over t, t squared, and the square root of t. Take t with a clean square root, one ninth. Two "
        "times one ninth is two ninths. Two over one ninth is eighteen. One ninth squared is one eighty-first. And the "
        "square root of one ninth is one third. Eighteen is the largest, choice number two.", show(y2, 'two t, two over t'),
        show(y3, 'one ninth. Two'), mk('tick', 'choice 2', 'Eighteen is the largest')),
      L("But careful. Swap a number only when the same number sits in every choice, the same way. Otherwise change only t, "
        "never the numbers in the question, or the order of the choices can change. [pause] Okay. I'll see you in the next "
        "question.", show(y4, 'Swap a number only'))),
])

# ------------------------------------------------------------------------------------------------ q-501 (Hebrew Q7)
# NEW: decode a chain first (p^2 < p -> 0 < p < 1; rq < q -> r < 1); "possible but not necessarily" = drop the always
# and the never; × a fraction pulls toward 0, so a product of fractions < each of them < their sum, and < 1.
# REMINDER: strong on strong (camera lesson).  Hebrew: one method (with strong on strong as a second look at one choice).
z1 = I('z1', '$p^2<p$: $\\ 0<p<1$', hand='p^2 < p :    0 < p < 1')
z2 = I('z2', '$rq<q$: $\\ \\div q>0$: $\\ r<1$', hand='rq < q :    ÷ q > 0 :    r < 1')
zl = ZL('zl', -0.25, 1.3, [('a', [('pt', 0.25, 'p'), ('pt', 0.55, 'q'), ('pt', 0.82, 'r')])], ticks=(0, 1), w=760)
z3 = I('z3', 'Always true ✗ $\\quad$ never true ✗', size=28, col=1)
z4 = I('z4', '(3) $pq<p<p+q$: $\\ $always ✗', hand='(3)   pq < p < p + q :    always   ✗')
z5 = I('z5', '(1) $\\div p$: $\\ pq<q<r$: $\\ $always ✗', hand='(1)   ÷ p :    pq < q < r :    always   ✗')
z6 = I('z6', '(2) $pq<1$: $\\ $never ✗', hand='(2)   pq < 1 :    never   ✗')
z7 = I('z7', '(4) $\\frac1{10}+\\frac12=\\frac35<1$ $\\quad \\frac14+\\frac78=\\frac98>1$', size=32, hand='(4)   {1/10} + {1/2} = {3/5} < 1        {1/4} + {7/8} = {9/8} > 1')
video('solve-q-501', 'solution', qid='q-501', slides=[
    S('Decode the chain',
      L("Given: p squared is smaller than p, which is smaller than r times q, which is smaller than q, which is smaller than "
        "r. Which of the following statements is possible but not necessarily true?", pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("A long chain of letters. So before the choices, let's decode it. [short pause] Start with p squared smaller than p. "
        "Can p be negative? No. Its square would be positive, and bigger than p. So p is positive, and squaring made it "
        "smaller. That happens only to positive fractions.", pt('stem', 'A long chain'), show(z1, 'Start with p squared')),
      L("p is positive, so everything bigger in the chain is positive too. Now r q is smaller than q. q is positive, so "
        "divide both sides by q, and r is smaller than one.", show(z2, 'Now r q is smaller')),
      L("So all of them are positive fractions, p the smallest, and r the biggest.", show(zl['line'], 'So all of them'),
        show(zl['a'], 'p the smallest'))),
    S('Then the choices',
      L("Now the question. Possible but not necessarily true. So anything always true is out, and anything never true is "
        "out too.", show(z3, 'anything always true')),
      L("Choice number three, p q against p plus q. Multiplying by a fraction pulls toward zero, so p q is smaller than p. "
        "Adding q makes p bigger. So the product is smaller than the sum, always. Out.", show(z4, 'p q against p plus q'),
        mk('cross', 'choice 3', 'smaller than the sum, always')),
      L("Choice number one. Divide both sides by p, which is positive, and it's p q against r. p q is smaller than q, and q "
        "is smaller than r. Always true. Out. Or strong on strong. p squared against p, p wins, and q against r, r wins. The "
        "right side wins twice.", show(z5, 'Divide both sides by p'), mk('cross', 'choice 1', 'Always true. Out')),
      L("Choice number two, p q bigger than one. A product of two positive fractions is always below one. Never true. Out.",
        show(z6, 'A product of two positive fractions'), mk('cross', 'choice 2', 'Never true. Out'))),
    S('Then the choices',
      L("Choice number four, p plus r smaller than one. Two fractions. Small ones add up to less than one, big ones to more. "
        "p is one tenth, q two fifths, and r one half. The chain holds, and p plus r is three fifths, smaller than one. But p "
        "one quarter, q three quarters, and r seven eighths. The chain still holds, and p plus r is nine eighths, more than "
        "one. Sometimes true, sometimes not. Choice number four is our answer. [pause] Okay. I'll see "
        "you in the next question.", show(z7, 'p is one tenth'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      sb='Then the choices'),
])

# ------------------------------------------------------------------------------------------------ q-r26-t17-01 (added)
# NEW: a picture of the line - write each letter's range; not drawn to scale -> trust the order, not the distances.
# REMINDER: signs of products and quotients (topic 16).  Methods: the ranges, plugging in numbers.
fa = I('fa', '$a<-1,\\ \\ -1<b<0,\\ \\ 0<c<1,\\ \\ d>1$', size=34, hand='a < −1,     −1 < b < 0,     0 < c < 1,     d > 1')
fb = I('fb', '(1) $\\frac{(-)}{(-)}>0$ ✗', hand='(1)   {(−)/(−)} > 0   ✗')
fc = I('fc', '(2) $(-)(+)(+)<0$ ✓', hand='(2)   (−)(+)(+) < 0   ✓')
fd = I('fd', '$a=-2,\\ b=-\\frac12,\\ c=\\frac12,\\ d=2$', hand='a = −2,   b = −{1/2},   c = {1/2},   d = 2')
fe = I('fe', '(1) $4$ ✗ $\\quad$ (3) $0$ ✗ $\\quad$ (4) $-\\frac18+\\frac12=\\frac38$ ✗', size=32, hand='(1)  4  ✗      (3)  0  ✗      (4)  −{1/8} + {1/2} = {3/8}  ✗')
fa['_y'] = 465; fb['_y'] = 535; fc['_y'] = 535; fc['_x'] = 900
fd['_y'] = 465; fe['_y'] = 545
video('solve-q-r26-t17-01', 'solution', qid='q-r26-t17-01', slides=[
    S('Method 1 · Ranges first',
      L("The figure shows the numbers a, b, c and d on a number line. The figure is not drawn to scale. Which of the "
        "following is necessarily negative?", pt('stem', 'The figure', 'hl', 7.0), voice='calm', pause=0.5),
      L("Letters on a line. So first, the range of each letter. And it's not drawn to scale, so we trust only the order, not "
        "the distances. [short pause] We'll solve it two ways, with the ranges, and then plugging in numbers.",
        pt('stem', 'not drawn to scale')),
      L("[short pause] Let's start with the ranges. a is below negative one. b is a negative fraction. c is a positive "
        "fraction. And d is above one.", show(fa, 'a is below negative one')),
      L("Choice number one, a over b. A negative over a negative is positive. Out.", show(fb, 'a over b'),
        mk('cross', 'choice 1', 'is positive. Out')),
      L("Choice number two, b times c times d. One negative and two positives, so it's negative, always. Choice number two "
        "is our answer.", show(fc, 'b times c times d'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers that fit the picture. a is negative two, b is negative one half, c is one "
        "half, and d is two.", show(fd, 'a is negative two')),
      L("Choice number one, a over b is four, positive. Out. Choice number three, a plus d is zero, and zero isn't negative. "
        "Out. Choice number four, b cubed is negative one eighth, and minus b adds one half, so it's three eighths, "
        "positive. Out. Three are out, so choice number two. [pause] Okay. I'll see you in the next question.",
        show(fe, 'a over b is four'), mk('cross', 'choice 1', 'is four, positive. Out'), mk('cross', 'choice 3', "zero isn't negative"),
        mk('cross', 'choice 4', 'three eighths'), mk('tick', 'choice 2', 'so choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t17-02 (added)
# NEW at the step: the square root = the power one half, a smaller power -> for a positive fraction, bigger (still < 1).
# REMINDER: the arrows (lesson).  Methods: the arrows, plugging in a number with a clean root.
g1 = I('g1', '$\\sqrt x=x^{\\frac12}$, $\\ \\frac12<1$: $\\ \\sqrt x>x$', hand='√{x} = x^{1/2},    {1/2} < 1 :    √{x} > x')
g2 = I('g2', '$x<\\sqrt x<1$: $\\ $M', hand='x < √{x} < 1 :    M')
g3 = I('g3', 'L: $\\ x^2$ $\\quad$ N: $\\ \\frac1x$', size=30, col=1)
h1 = I('h1', '$x=\\frac14$: $\\ \\sqrt x=\\frac12$', hand='x = {1/4} :    √{x} = {1/2}')
g1['_y'] = 465; g2['_y'] = 585; g3['_y'] = 585; h1['_y'] = 465
video('solve-q-r26-t17-02', 'solution', qid='q-r26-t17-02', slides=[
    S('Method 1 · The arrows',
      L("The figure shows the number x and the points K, L, M and N on a number line. The figure is not drawn to scale. "
        "Which of the points could represent the square root of x?", pt('stem', 'The figure', 'hl', 7.0), voice='calm', pause=0.5),
      L("So x is between zero and one, a positive fraction, and we look for its square root. [short pause] We'll solve it two "
        "ways, with the arrows, and then plugging in a number.", pt('stem', 'we look for its square root')),
      L("[short pause] Let's start with the arrows. The square root is a power of one half, and one half is smaller than "
        "one, the power of x itself. For a positive fraction the arrow points left, so a smaller power gives a bigger "
        "number. The root is bigger than x.", show(g1, 'The square root is a power')),
      L("But the root of a number below one stays below one. So it's between x and one, and only one point is there, M. "
        "Choice number three is our answer.", show(g2, 'stays below one'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Now careful, the traps. L is where x squared would be, and N is where one over x would be.", show(g3, 'the traps'))),
    S('Method 2 · Plugging in a number',
      L("[pause] Now let's try a number with a clean root. x is one quarter, and its square root is one half. That's bigger "
        "than one quarter, and still below one. So between x and one, M. Choice number three. [pause] Okay. I'll see you in "
        "the next question.", show(h1, 'x is one quarter'), mk('tick', 'choice 3', 'between x and one, M'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t17-03 (added)
# NEW: the reciprocal keeps the sign and, for numbers with the same sign, flips the order (why; 2 and 4; -4 and -2);
# × a positive keeps the order.  Methods: reciprocals, plugging in the ends.
i1 = I('i1', '$2<4 \\ \\Rightarrow\\ \\frac12>\\frac14$', hand='2 < 4    ⇒    {1/2} > {1/4}')
i2 = I('i2', '$-4<-2 \\ \\Rightarrow\\ -\\frac14>-\\frac12$', hand='−4 < −2    ⇒    −{1/4} > −{1/2}')
i3 = I('i3', '$-\\frac12<\\frac1x<-\\frac14$', hand='−{1/2} < {1/x} < −{1/4}')
i4 = I('i4', '$\\times6$: $\\ -3<\\frac6x<-\\frac32$', hand='× 6 :    −3 < {6/x} < −{3/2}')
j1 = I('j1', '$x=-4$: $\\ \\frac6{-4}=-\\frac32 \\qquad x=-2$: $\\ \\frac6{-2}=-3$', size=32, hand='x = −4 :   {6/−4} = −{3/2}        x = −2 :   {6/−2} = −3')
j2 = I('j2', '(1) $\\times$ instead of $\\div$ $\\quad$ (2) lost the minus $\\quad$ (4) $\\frac x6$', size=28, col=1)
video('solve-q-r26-t17-03', 'solution', qid='q-r26-t17-03', slides=[
    S('Method 1 · Reciprocals',
      L("Given: negative four is smaller than x, which is smaller than negative two. Which of the following is necessarily "
        "true?", pt('stem', 'Given', 'hl', 5.0), voice='calm', pause=0.5),
      L("So x is between negative four and negative two, and the choices say where six over x is. [short pause] We'll solve "
        "it two ways, with reciprocals, and then plugging in the ends.", pt('stem', 'between negative four and negative two')),
      L("[short pause] Six over x is six times one over x, so let's start with one over x, the reciprocal. Here's the rule. "
        "For numbers with the same sign, the reciprocal flips the order. Two is smaller than four, but one half is bigger "
        "than one quarter. One over a bigger number is a smaller piece.", show(i1, 'Two is smaller than four')),
      L("And on the negative side, the mirror image. Negative four is smaller than negative two, but negative one quarter is "
        "bigger than negative one half.", show(i2, 'Negative four is smaller')),
      L("So here, one over x is between negative one half and negative one quarter. Negative one half is the smaller end.",
        show(i3, 'So here, one over x')),
      L("Times six, a positive number, keeps the order. Six times negative one half is negative three, and six times "
        "negative one quarter is negative three halves. So six over x is between negative three and negative three halves. "
        "Choice number three is our answer.", show(i4, 'Times six'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Plugging in the ends',
      L("[pause] Now let's try plugging in the ends. Six over negative four is negative three halves, and six over negative "
        "two is negative three.", show(j1, 'Six over negative four')),
      L("So six over x goes between negative three halves and negative three. The smaller one, negative three, goes on the "
        "left. Between negative three and negative three halves, choice number three.", mk('tick', 'choice 3', 'choice number three.')),
      L("And the traps. Choice number one multiplied instead of dividing, choice number two lost the minus, and choice number "
        "four is upside down, x over six. [pause] Okay. I'll see you in the next question.", show(j2, 'And the traps'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t17-04 (added)
# NEW: to break "necessarily", push the numbers to the edges of their ranges (x = -2, y = -1/2).
# REMINDER: adding a negative moves left (topic 16).  Methods: understanding, plugging in at the edges.
k1 = I('k1', '(1) $x=-2,\\ y=-\\frac14$: $\\ xy=\\frac12$ ✗', hand='(1)   x = −2,   y = −{1/4} :    xy = {1/2}   ✗')
k2 = I('k2', '(2) $x<-1$, $\\ +\\,y<0$: $\\ x+y<-1$ ✓', hand='(2)   x < −1,    + y < 0 :    x + y < −1   ✓')
l1 = I('l1', 'Push to the edges: $\\ x=-2,\\ y=-\\frac12$', size=34, hand='Push to the edges :    x = −2,    y = −{1/2}')
l2 = I('l2', '(1) $1>1$ ✗ $\\quad$ (3) $4<\\frac14$ ✗ $\\quad$ (4) $4<1$ ✗', size=32, hand='(1)   1 > 1  ✗      (3)   4 < {1/4}  ✗      (4)   4 < 1  ✗')
video('solve-q-r26-t17-04', 'solution', qid='q-r26-t17-04', slides=[
    S('Method 1 · Understanding',
      L("Given: x is smaller than negative one, which is smaller than y, which is smaller than zero. Which of the following "
        "is necessarily true?", pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("So x is below negative one, and y is a negative fraction. [short pause] We'll solve it two ways, by understanding, "
        "and then plugging in numbers at the edges.", pt('stem', 'x is below negative one')),
      L("[short pause] Let's start with understanding. Choice number one, x times y. Negative times negative is positive. "
        "But how big? y can be close to zero, so the product can be small. x is negative two, and y is negative one quarter. "
        "The product is one half, not bigger than one. Not necessarily. Out.", show(k1, 'x is negative two, and y'),
        mk('cross', 'choice 1', 'Not necessarily. Out')),
      L("Choice number two, x plus y. x is already below negative one, and adding a negative y moves it further left. So x "
        "plus y is always below negative one. Choice number two is our answer.", show(k2, 'x is already below'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
    S('Method 2 · Plugging in at the edges',
      L("[pause] Now let's try plugging in. To break a statement, push the numbers to the edges of their ranges. x is "
        "negative two, and y is negative one half.", show(l1, 'push the numbers')),
      L("Choice number one, x times y is one, and one isn't bigger than one. Out. Choice number three, x squared is four, y "
        "squared is one quarter, and four isn't smaller. Out. Choice number four, x over y is four, not smaller than one. "
        "Out. So choice number two. [pause] Okay. I'll see you in the next question.", show(l2, 'x times y is one'),
        mk('cross', 'choice 1', "isn't bigger than one"), mk('cross', 'choice 3', "four isn't smaller"),
        mk('cross', 'choice 4', 'not smaller than one'), mk('tick', 'choice 2', 'So choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t17-05 (added)
# NEW: distance = bigger - smaller; a third of the way = a third of the distance, walked from the start; the midpoint
# is the average (a trap here).  Methods: the distance, plugging in the answers.
kl = ZL('kl', -8.5, 6.5, [('a', [('ink', -7, 'A'), ('ink', 5, 'B')]), ('b', [('arrow', -7, -3, '4'), ('pt', -3, 'C')])],
        ticks=((-7, '−7'), (-3, '−3'), 0, (5, '5')), w=700)
m5 = I('m5', '$AB=5-(-7)=12$', hand='AB = 5 − (−7) = 12')
m6 = I('m6', '$\\frac13\\cdot12=4$: $\\ -7+4=-3$', hand='{1/3} · 12 = 4 :    −7 + 4 = −3')
m7 = I('m7', '$4$: the distance $\\quad -1$: the midpoint', size=28, col=1)
m8 = I('m8', 'From $-7$: $\\ $(1) $8$ ✗ $\\quad$ (2) $6$ ✗ $\\quad$ (3) $4$ ✓', size=32, hand='From −7 :    (1)  8  ✗      (2)  6  ✗      (3)  4  ✓')
video('solve-q-r26-t17-05', 'solution', qid='q-r26-t17-05', slides=[
    S('Method 1 · The distance',
      L("On a number line, point A is at negative seven, and point B is at five. Point C is between A and B, and its "
        "distance from A is one third of the distance A B. What number is at point C?", pt('stem', 'On a number line', 'hl', 8.0), voice='calm', pause=0.5),
      L("So two points, and a point a third of the way from A. [short pause] We'll solve it two ways, with the distance, and "
        "then plugging in the answers.", pt('stem', 'a third of the way')),
      L("[short pause] Let's start with the distance from A to B. Bigger minus smaller, five minus negative seven, which is "
        "twelve.", show(m5, 'Bigger minus smaller')),
      L("C is a third of the way from A. A third of twelve is four. So start at A and walk four steps right. Negative seven "
        "plus four is negative three. Choice number three is our answer.", show(kl['line'], 'C is a third'),
        show(kl['a'], 'of the way from A'), show(kl['b'], 'walk four steps'), show(m6, 'Negative seven'),
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Now careful, the traps. Four is the distance, not the point. And negative one is the midpoint, negative seven plus "
        "five, over two. Not what they asked.", show(m7, 'the traps'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's try plugging in the answers. The right point is four away from A. One is eight away, out. "
        "Negative one is six away, out. Negative three is four away. Choice number three. [pause] Okay. I'll see you in the "
        "next question.", show(m8, 'One is eight away'), mk('cross', 'choice 1', 'eight away, out'),
        mk('cross', 'choice 2', 'six away, out'), mk('tick', 'choice 3', 'four away. Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ r26-t17-summary
# REMINDERS only, said the way they were taught; new numbers.
s1s = I('s1s', '$x<-1\\quad -1<x<0\\quad 0<x<1\\quad x>1$', size=36)
s2s = I('s2s', 'Borders: $\\ -1,\\ 0,\\ 1$ $\\quad$ negatives mirror the positives', size=34)
s3s = I('s3s', '$\\times$ above $1$, $\\div$ a fraction: bigger $\\quad 12\\div\\frac13=36$', size=34)
s4s = I('s4s', '$\\div$ above $1$, $\\times$ a fraction: smaller $\\quad 12\\cdot\\frac13=4$', size=34)
s5s = I('s5s', 'Times a negative: the order flips $\\quad 4<9\\Rightarrow -4>-9$', size=34)
s6s = I('s6s', 'Higher range: bigger $\\quad \\sqrt[3]{\\frac65}>\\sqrt{\\frac23}$', size=34)
s7s = I('s7s', 'Same operation: ignore it (positives) $\\quad$ strong on strong', size=34)
s8s = I('s8s', '$(-3)^2=9$ $\\quad -3^2=-9$ $\\quad \\left(\\frac23\\right)^{-2}=\\left(\\frac32\\right)^2$', size=34)
s9s = I('s9s', 'Arrows: $\\ x>1\\ \\rightarrow\\quad 0<x<1\\ \\leftarrow\\quad -1<x<0\\ \\rightarrow\\quad x<-1\\ \\leftarrow$', size=30)
s10s = I('s10s', 'Exceptions $\\to$ roots to powers $\\to$ arrows', size=34)
s11s = I('s11s', 'Same sign: $\\ \\frac1x$ flips the order $\\quad 3<5\\Rightarrow\\frac13>\\frac15$', size=34)
s12s = I('s12s', 'Test: $\\ 2,\\ \\frac12,\\ -\\frac12,\\ -2$ $\\quad$ clean roots: $\\ \\frac19,\\ -\\frac18$', size=34)
s13s = I('s13s', 'Necessarily? Push to the edges $\\quad$ a picture: trust the order', size=32)
s14s = I('s14s', 'Distance $=$ bigger $-$ smaller $\\quad$ midpoint $=$ the average', size=34)
video('r26-t17-summary', 'lesson', slides=[
    S('The Number Line: Summary',
      L("Before you practice, here's a quick summary of the topic. Ranges, powers, and reading the line.")),
    S('Four ranges',
      L("It all starts with four ranges. Below negative one, negative fractions, positive fractions, and above one. Every "
        "number in a range behaves the same way.", show(s1s, 'four ranges')),
      L("Watch the borders, negative one, zero and one. If they only say x is positive, it could be a fraction or above one. "
        "And the negative side is a mirror of the positive side.", show(s2s, 'Watch the borders'))),
    S('Multiply and divide',
      L("Times a number above one, or divided by a fraction, a positive number gets bigger. Twelve divided by one third is "
        "thirty-six. Divided by a number above one, or times a fraction, it gets smaller. Twelve times one third is four.",
        show(s3s, 'Times a number above one'), show(s4s, 'Divided by a number above one')),
      L("A negative number makes the same moves, away from zero or toward zero. And times a negative, you jump to the other "
        "side, and the order flips. Four is smaller than nine, but negative four is bigger than negative nine.",
        show(s5s, 'times a negative'))),
    S('Hierarchy',
      L("A number in a higher range stays bigger, after any positive power or root. Six fifths is above one, and two thirds "
        "is a fraction. So the cube root of six fifths is bigger, no calculating. On the negative side, odd powers and odd "
        "roots only.", show(s6s, 'A number in a higher range')),
      L("The same operation on two positive numbers? Ignore it. And strong on strong, weak times weak loses to strong times "
        "strong.", show(s7s, 'The same operation'))),
    S('Exceptions first',
      L("Exceptions move a number to another range, so handle them first. An even power of a negative number is positive. "
        "Negative three, squared, is nine. And read the brackets. Without them, it's minus, three squared, minus nine. A "
        "negative power flips the number. Two thirds to the power of negative two is three halves, squared, above one.",
        show(s8s, 'An even power of a negative'))),
    S('The arrows',
      L("The arrows show what a bigger power does. Above one, right. Positive fractions, left. Negative fractions, right, and "
        "below negative one, left, odd powers only. Right means bigger.", show(s9s, 'The arrows show')),
      L("Three steps. Exceptions, roots into powers, then the arrows, and with the arrows you may keep a negative power. "
        "They give the order and ask for the range? Use the arrows backwards, or plug in.", show(s10s, 'Three steps'))),
    S('Reciprocals and plugging in',
      L("One over x keeps the sign, and for numbers with the same sign, it flips the order. Three is smaller than five, but "
        "one third is bigger than one fifth.", show(s11s, 'One over x keeps the sign')),
      L("Not sure? Plug in one number from each allowed range, like two, one half, negative one half, and negative two. A "
        "root in the choices? Pick a number with a clean root, like one ninth for a square root, or negative one eighth for "
        "a cube root. And change only the letters. Unless the same number sits in every choice, then you may swap it for a "
        "small one.", show(s12s, 'Plug in one number'))),
    S('Must or could',
      L("Necessarily true? One example where it fails knocks it out, so push the numbers to the edges of their ranges. A "
        "picture of the line? Write the range of each letter, and trust only the order, not the distances.",
        show(s13s, 'Necessarily true')),
      L("And distance on the line is bigger minus smaller. A third of the way? Take a third of the distance, and walk it "
        "from the start. The midpoint is the average of the two ends. [pause] That's it. Now go practice, and I'll see you "
        "in the next video.", show(s14s, 'distance on the line'))),
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
 "q-493": "Given: $1<p<q<r<s$. Which of the following statements is not correct?",
 "q-494": "Given: $-1<m<0$. Which of the following expressions is the smallest?",
 "q-495": "Given: $1<a<b<c$. Which of the following expressions is the smallest?",
 "q-496": "Given: $0<a<b<1<c<d$. Which of the following statements is not necessarily true?",
 "q-497": "Given: $-1<k<0<m<n<1$. Which of the following expressions is the largest?",
 "q-498": "Given: $x^8<x^7$. In which of the following ranges is $x$?",
 "q-499": "Given: $-1<y<0$. Which of the following orders of $y^7$, $y$, $\\sqrt[3]{y}$ and $y^{-7}$ is correct?",
 "q-500": "Given: $0<t<1$. Which of the following expressions is the largest?",
 "q-501": "Given: $p^2<p<r\\cdot q<q<r$. Which of the following statements is possible but not necessarily true?",
 "q-r26-t17-03": "Given: $-4<x<-2$. Which of the following is necessarily true?",
 "q-r26-t17-04": "Given: $x<-1<y<0$. Which of the following is necessarily true?"
}   # picture / word stems (no "Given:"): the whole stem only
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
