"""Topic 20 (Algebraic Understanding) - the scripts for the teacher's own-voice reading (2026-10-13), written from the first
draft to the Codex review standard, the clarity style and the method visuals (math_patches/_method_visuals.py), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py / _ai_vis_t16.py / _ai_vis_t17.py / _ai_vis_t18.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The camera lesson 'algebraic-understanding' gets its own reading script here too (2026-10-13: she reads it with the camera on).
Every other topic-20 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t20.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t20.py ai_redo_t20() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods and EVERY method of the Hebrew solution (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-20-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t20ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-20 flow order of the scripts
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
            'style': "the teacher reads it herself (Reading Studio), topic-20 scripts (2026-10-13): math_patches/_ai_vis_t20.py is "
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
# THE SCRIPTS (topic-20 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-20-AI-scripts-review.md.
# Written to the Codex review standard (TEACHING_STYLE_GUIDE "Codex review standard (2026-10-13)") from the first draft:
# connect each given to the next action, the question's exact logical request (must / could / cannot / not necessarily),
# one easy allowed value first and the choices checked at once, stop when the request is settled, concrete reasons, no
# labels ("a hard one"), math shown grouped in the prompter, steady highlights.
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ algebraic-understanding (camera lesson)
# 2026-10-13 teacher: her camera first lesson as a reading script too (same style, handwriting, camera on), with more
# examples. Hebrew (alg 19914-19929): the last algebra topic; questions that belong to no one topic or mix topics; the
# solution is sometimes algebra, sometimes understanding, sometimes the psychometric tools (plugging in numbers or
# answers); a small part of the exam, the questions don't repeat, no repeating principle - the lesson and the practice
# give tools that "open your head". English additions kept: the three tools in order, numbers first.
# NEW here, with examples: plugging in (two regions + a non-allowed number), testing the answers, algebra / understanding
# (a shortcut formula instead of finding the letters; integer gaps).  Reminders later: q-r26-t20-01, q-577, q-578, q-579.
w0 = I('w0', '1 · Plug in numbers $\\quad$ 2 · Test the answers $\\quad$ 3 · Algebra and understanding', size=28)
w1 = I('w1', '$a>0$: $\\ a=3$: $\\ 9>3$ ✓ $\\quad a=\\frac13$: $\\ \\frac19<\\frac13$ ✗', size=30)
w2 = I('w2', '$a<0$: $\\ 3$ is not allowed $\\quad a=-2$: $\\ 4>-2$', size=30)
w3 = I('w3', '$x^2-x=6$: $\\ x=2\\to2$ ✗ $\\quad x=3\\to6$ ✓', size=30)
w4 = I('w4', '$a+b=10,\\ a-b=4$: $\\ a^2-b^2=(a+b)(a-b)=40$', size=30)
w5 = I('w5', 'Integer $n<5\\ \\to\\ n\\le4$', size=30)
video('algebraic-understanding', 'lesson', slides=[
    S('Algebraic Understanding',
      L("That's it, we've reached the last topic in algebra, algebraic understanding. These are algebra questions that don't "
        "belong to any one topic we've learned, or that mix a few topics together.")),
    S('Three tools',
      L("Sometimes the solution is algebra, sometimes it's understanding what the givens really say, and sometimes it's one "
        "of the tools from psychometric thinking, plugging in numbers or testing the answers. To be honest, it's a fairly "
        "small part of the exam, and the questions don't repeat themselves. There's no single rule I can give you that "
        "solves them all.", show(w0, 'Sometimes the solution is algebra')),
      L("But the questions in this topic, and the practice after them, give you tools that open your head for questions "
        "like these. Three tools open almost all of them. Plug in numbers, test the answers, and use algebra and "
        "understanding. Try numbers first, because they're fast and safe, and use algebra when the numbers don't decide.",
        pt('w0', 'Three tools open almost all of them'))),
    S('Plug in numbers',
      L("The first tool, plugging in numbers. Say a is a positive number, and the question asks if a squared is always "
        "bigger than a. Try a is three. Three squared is nine, and nine is bigger than three. So far, yes.",
        show(w1, 'Try a is three')),
      L("But positive numbers can also be between zero and one. Try a is one third. One third squared is one ninth, and one "
        "ninth is smaller than one third. So a squared is not always bigger than a. One allowed number where it fails is "
        "enough to say not always.", pt('w1', 'Try a is one third')),
      L("And use only numbers that the givens allow. If the question said a is negative, three and one third would not be "
        "allowed at all. Then we'd try a negative number, like negative two. Negative two squared is four, and four is "
        "bigger than negative two.", show(w2, 'use only numbers that the givens allow'))),
    S('Test the answers',
      L("The second tool, testing the answers. Say x squared minus x is six, and the choices are two, three, four and six. "
        "We don't have to solve anything. We put each choice into the question. Two squared minus two is four minus two, "
        "which is two, not six. Three squared minus three is nine minus three, which is six. So three works.",
        show(w3, 'Two squared minus two'))),
    S('Algebra and understanding',
      L("The third tool, algebra and understanding. Say a plus b is ten, a minus b is four, and they ask for a squared minus "
        "b squared. We don't need to find a and b. a squared minus b squared is the bracket a plus b, times the bracket a "
        "minus b. That's ten times four, which is forty.", show(w4, 'We don\'t need to find a and b')),
      L("Understanding also means reading what a given really says. If n is an integer and n is smaller than five, then n "
        "is at most four, because there's no integer between four and five. Gaps like this will help us find the biggest "
        "or smallest possible value.", show(w5, 'If n is an integer')),
      L("As usual, we'll learn the rest through sample questions, where you'll see these tools at work. [pause] Okay. I'll "
        "see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ q-r26-t20-01 (added)
# REMINDER: plugging in (topic 51), the regions of the positive numbers and squaring between 0 and 1 (topic 17).
# NEW at the step: "must be true" - a failing allowed pair rules a choice out; a second pair from the other region only
# because three choices are still left.  Methods: plugging in numbers, algebra (why the survivor always works).
z1 = ZL('z1', -0.4, 3.6, [('a', [('pt', 3, 'x'), ('pt', 2, 'y')])], ticks=(0, 1), w=760, col=1)
z2 = ZL('z2', -0.4, 3.6, [('a', [('pt', 0.62, 'x'), ('pt', 0.3, 'y'), ('below', 0.62, '½'), ('below', 0.3, '¼')])],
        ticks=(0, 1), w=760, col=1)
a1 = I('a1', '$x=3,\\ y=2$: $\\ $(1) $9>3$ ✓ $\\ $(2) $6>2$ ✓ $\\ $(3) $9>4$ ✓', size=28)
a2 = IH('a2', '(4) $\\frac32>3$ ✗', size=30)
a3 = I('a3', '$x=\\frac12,\\ y=\\frac14$: $\\ $(1) $\\frac14>\\frac12$ ✗ $\\quad$ (2) $\\frac18>\\frac14$ ✗', size=28)
b1 = IH('b1', '$x^2-y^2=(x-y)(x+y)$', size=32)
b2 = I('b2', '$x-y>0,\\ \\ x+y>0$: $\\ x^2-y^2>0$ ✓', size=32)
video('solve-q-r26-t20-01', 'solution', qid='q-r26-t20-01', slides=[
    S('Method 1 · Plugging in numbers',
      L("Given: x and y are positive numbers, and x is bigger than y. Which of the following must be true?",
        pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("Must be true means true for every allowed pair. So one allowed pair where a choice fails is enough to rule that "
        "choice out. [short pause] We'll solve it two ways, plugging in numbers, and then with algebra, to see why the "
        "answer always works.", pt('stem: ask', 'Must be true means')),
      L("[short pause] Let's start with easy whole numbers that fit the givens. x is three and y is two. Both are "
        "positive, and three is bigger than two.", show(z1['line'], 'easy whole numbers'), show(z1['a'], 'x is three and y is two')),
      L("Choice number one, x squared is bigger than x. Three squared is nine, and nine is bigger than three, so it works "
        "here. Choice number two, x y is bigger than y. Three times two is six, and six is bigger than two. It works. "
        "Choice number three, x squared is bigger than y squared. Nine is bigger than four. It works too.",
        show(a1, 'Three squared is nine')),
      L("Choice number four, x over y is bigger than x. Three over two is one and a half, and one and a half is not bigger "
        "than three. So choice number four fails for an allowed pair, and it's out.", show(a2, 'Three over two is'),
        mk('cross', 'choice 4', "and it's out"))),
    S('Method 1 · Plugging in numbers',
      L("Three choices still work, so one pair wasn't enough. Positive numbers can also be between zero and one, and there, "
        "squaring makes a number smaller. So let's try x is one half and y is one quarter. Both are positive, and one half "
        "is bigger than one quarter.", show(z2['line'], 'between zero and one'), show(z2['a'], 'x is one half and y')),
      L("Choice number one. One half squared is one quarter, and one quarter is not bigger than one half, so it's out. "
        "Choice number two. One half times one quarter is one eighth, and one eighth is not bigger than one quarter, so it's "
        "out too.", show(a3, 'One half squared is one quarter'), mk('cross', 'choice 1', "so it's out."),
        mk('cross', 'choice 2', "so it's out too")),
      L("Only choice number three is left, so choice number three is our answer.",
        mk('tick', 'choice 3', 'so choice number three is our answer')),
      sb='Method 1 · Plugging in numbers'),
    S('Method 2 · Algebra',
      L("[pause] Now let's see why choice number three is true for every allowed pair. x squared minus y squared is, in "
        "brackets, x minus y, times, in brackets, x plus y.", show(b1, 'x squared minus y squared is')),
      L("x is bigger than y, so x minus y is positive. Both numbers are positive, so x plus y is positive too. A positive "
        "number times a positive number is positive. So x squared minus y squared is positive, which means x squared is "
        "bigger than y squared, always. Choice number three. [pause] Okay. I'll see you in the next question.",
        show(b2, 'so x minus y is positive'), mk('tick', 'choice 3', 'bigger than y squared, always'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t20-02 (added)
# REMINDER: the range between -1 and 0 and powers there (topic 17); ordering negatives.  NEW at the step: "the smallest
# for every x in the range" - one easy number from the range decides.  Methods: one number, placing the choices.
n1 = ZL('n1', -2.4, 0.3, [('a', [('pt', -2, '−2'), ('pt', -0.78, '−½'), ('pt', -0.47, '−¼'), ('pt', -0.17, '−⅛')])],
        ticks=(-1, 0), w=760, col=1)
n2 = ZL('n2', -2.4, 0.3, [('a', [('shade', -1, 0), ('below', -0.5, '(1), (2), (3)')]), ('b', [('pt', -1.75, '1/x')])],
        ticks=(-1, 0), w=760, col=1)
c1 = IH('c1', '$x=-\\frac12$: $\\ $(1) $-\\frac18$ $\\quad$ (2) $-\\frac12$', size=30)
c2 = IH('c2', '(3) $-\\frac14$ $\\quad$ (4) $-2$', size=30)
c3 = I('c3', '$\\frac{1}{-1/2}=-2,\\quad \\frac{1}{-1/10}=-10$', size=30)
video('solve-q-r26-t20-02', 'solution', qid='q-r26-t20-02', slides=[
    S('Method 1 · One number',
      L("Given: x is between negative one and zero. Which of the following is the smallest?",
        pt('stem', 'Given', 'hl', 5.0), voice='calm', pause=0.5),
      L("The answer has to be the smallest for every x in this range. So it's also the smallest at any one number we pick "
        "from the range, and one easy number can decide. [short pause] We'll solve it two ways, with one number, and then "
        "by placing each choice on the number line without numbers.", pt('stem: ask', 'The answer has to be the smallest')),
      L("[short pause] Let's take x is negative one half. It's between negative one and zero, and it's easy to work with. "
        "Choice number one, x cubed. Negative one half, cubed, is negative one half times negative one half times negative "
        "one half. Three negatives multiply to a negative, so it's negative one eighth. Choice number two is x itself, "
        "negative one half.", show(c1, 'Choice number one, x cubed')),
      L("Choice number three, negative x squared. First x squared: negative one half, squared, is one quarter. Then the "
        "minus in front makes it negative one quarter. Choice number four, one over x. One over negative one half is "
        "negative two.", show(c2, 'Choice number three, negative x squared')),
      L("Now compare the four values. With negative numbers, the farther a number is from zero, the smaller it is. "
        "Negative two is the farthest from zero, so it's the smallest. Choice number four is our answer.",
        show(n1['line'], 'Now compare the four values'), show(n1['a'], 'the farther a number is from zero'),
        mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Careful with choice number one. Cubing a number between negative one and zero brings it closer to zero. So "
        "negative one eighth is bigger than negative one half, not smaller.", mk('cross', 'choice 1', 'Careful with choice number one'))),
    S('Method 2 · Place the choices',
      L("[pause] Now without numbers. A number between negative one and zero stays between negative one and zero when we "
        "cube it. And x squared is between zero and one, so negative x squared is between negative one and zero. So choice "
        "numbers one, two and three are all between negative one and zero.", show(n2['line'], 'Now without numbers'),
        show(n2['a'], 'So choice numbers one, two and three')),
      L("Now one over x. x is closer to zero than negative one, so one over x is farther from zero than negative one. For "
        "example, one over negative one half is negative two, and one over negative one tenth is negative ten. So one over "
        "x is always below negative one, smaller than the other three. Choice number four. [pause] Okay. I'll see you in "
        "the next question.", show(n2['b'], 'Now one over x'), show(c3, 'For example, one over negative one half'),
        mk('tick', 'choice 4', 'smaller than the other three'))),
])

# ------------------------------------------------------------------------------------------------ q-580 (Hebrew: the formula question)
# NEW: a formula described in words - test how each expression reacts when ONE letter grows; in a fraction with positive
# parts a bigger top -> bigger, a bigger bottom -> smaller.  Hebrew: one method, choice by choice; the fraction choice
# is kept as a clearly separate teaching check after the answer (the Hebrew's wrong choice was its last).
d0 = I('d0', 'More $C$ or $S$: score up $\\quad$ more $M$: score down', size=30)
d1 = I('d1', '(1) $C+S-M$: $\\ $fits', size=30)
d2 = I('d2', '(2) $C\\cdot S\\cdot M$: $\\ $more $M$, bigger ✗', size=30)
d3 = I('d3', '(3) $\\frac{C^S}{M}$: $\\ $bigger top $\\to$ bigger, bigger bottom $\\to$ smaller', size=30)
video('solve-q-580', 'solution', qid='q-580', slides=[
    S('Check each letter',
      L("A player's score in a computer game is given by a formula. The score increases when the player collects more "
        "coins, C, and more stars, S, and decreases when the player makes more mistakes, M. C, S and M are all greater than "
        "one. Which of the following expressions cannot give the player's score?", pt('stem', "A player's score", 'hl', 12.0),
        voice='calm', pause=0.5),
      L("There's nothing to calculate here. We check how each expression reacts when one letter grows. [short pause] For "
        "each choice, we ask three things. When C grows, does the expression grow? When S grows, does it grow? And when M "
        "grows, does it get smaller? A choice that breaks even one of these cannot give the score.",
        show(d0, 'For each choice, we ask three things')),
      L("[short pause] Choice number one, C plus S minus M. C and S are added, so when either one grows, the result grows. "
        "M is subtracted, so when M grows, the result gets smaller. Every rule fits, so this expression could give the "
        "score, and choice number one is out.", show(d1, 'C and S are added'), mk('cross', 'choice 1', 'and choice number one is out')),
      L("Choice number two, C times S times M. All the letters are positive, so a bigger C or a bigger S makes the product "
        "bigger. That part is fine. But M is multiplied too, so more mistakes make the product bigger. That's the opposite "
        "of the rule. This expression cannot give the score, and choice number two is our answer.",
        show(d2, 'But M is multiplied too'), mk('tick', 'choice 2', 'and choice number two is our answer'))),
    S('A fraction with a power',
      L("[pause] In the exam you'd mark it and move on. But choice number three teaches something useful about fractions, "
        "so let's look at it. C to the power of S, over M. In a fraction with positive parts, a bigger top gives a bigger "
        "result, and a bigger bottom gives a smaller result.", show(d3, 'In a fraction with positive parts')),
      L("When C grows, the top grows. When S grows, C is multiplied by itself more times, and because C is bigger than one, "
        "the top grows again. When M grows, the bottom grows, so the result gets smaller. So choice number three fits every "
        "rule. [pause] Okay. I'll see you in the next question.", pt('d3', 'When C grows, the top grows'))),
])

# ------------------------------------------------------------------------------------------------ q-577 (Hebrew: first sample question)
# NEW: integer gaps - "smaller than 16" is "at most 15", and c < b < a puts c at least two below a; a "cannot be" with a
# hidden biggest value.  Hebrew: three methods - the biggest value, numbers that make b + c biggest, testing the answers
# (she starts with the possible ones; here the biggest choice is tested first and we stop, because one impossible value
# answers a "cannot").  Letters on the axis (topic 13/16/17 picture).
lz = ZL('lz', -0.5, 2.5, [('c', [('pt', 0, 'c')]), ('b', [('pt', 1, 'b'), ('arrow', 0.08, 0.92, 'at least 1')]),
                          ('a', [('pt', 2, 'a'), ('arrow', 1.08, 1.92, 'at least 1')])], ticks=(), w=760, col=1)
e1 = IH('e1', '$a+b<16\\ \\to\\ a+b\\le15$', size=32)
e2 = IH('e2', '$b+c=(a+b)-(a-c)$', size=32)
e3 = IH('e3', '$b+c\\le15-2=13$', size=32)
f1 = IH('f1', '$a=8,\\ b=7$: $\\ 8+7=15$', size=32)
f2 = IH('f2', '$c=6$: $\\ b+c=13$', size=32)
f3 = I('f3', '$b+c=14$: $\\ b\\ge8,\\ a\\ge9$: $\\ a+b\\ge17$ ✗', size=32)
video('solve-q-577', 'solution', qid='q-577', slides=[
    S('Method 1 · The biggest value',
      L("Given: a, b and c are integers, c is smaller than b, which is smaller than a, and a plus b is smaller than "
        "sixteen. Which of the following cannot be the value of b plus c?", pt('stem', 'Given', 'hl', 9.0), voice='calm', pause=0.5),
      L("They ask what b plus c cannot be. So we'll find the biggest value b plus c can ever have. [short pause] We'll "
        "solve it three ways, with the biggest possible value, with numbers that make b plus c as big as possible, and by "
        "testing the answers.", pt('stem: ask', 'They ask what b plus c cannot be')),
      L("[short pause] Let's start with the second given. a and b are integers, so a plus b is an integer too. Smaller "
        "than sixteen means at most fifteen.", show(e1, 'Smaller than sixteen means')),
      L("Now compare the two sums. a plus b is the sum of the two biggest numbers, and b plus c is the sum of the two "
        "smallest. Both sums have b, so the difference between them is a minus c.", show(e2, 'Both sums have b')),
      L("How big is a minus c? These are integers, so c is at least one below b, and b is at least one below a. So c is "
        "at least two below a, and a minus c is at least two.", show(lz['line'], 'How big is a minus c'), show(lz['c'], 'c is at least one below b'),
        show(lz['b'], 'and b is at least one'), show(lz['a'], 'So c is at least two below a')),
      L("So b plus c is a plus b, which is at most fifteen, minus a minus c, which is at least two. That's at most "
        "thirteen. Fourteen is more than thirteen, so b plus c can never be fourteen. Choice number four is our answer.",
        show(e3, "That's at most thirteen"), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('Method 2 · Numbers for the biggest sum',
      L("[pause] Another way is to build numbers that make b plus c as big as possible. a has to be bigger than b, and a "
        "plus b has to stay at most fifteen. To make b as big as it can be, take a and b as close as possible: a is eight "
        "and b is seven. Eight plus seven is fifteen, which is allowed.", show(f1, 'a is eight')),
      L("c has to be smaller than b, so the biggest c is six. Then b plus c is seven plus six, which is thirteen. If we try "
        "a bigger a, like nine, then b can only be six, and b plus c gets smaller. So thirteen is the biggest b plus c can "
        "be, and fourteen is out of reach. Choice number four.", show(f2, 'so the biggest c is six'),
        mk('tick', 'choice 4', 'fourteen is out of reach'))),
    S('Method 3 · Testing the answers',
      L("[pause] And a third way, testing the answers. The question hides a biggest value, so it makes sense to start with "
        "the biggest choice, fourteen. Can b plus c be fourteen? c is smaller than b, so b has to be at least eight, with c "
        "at most six. Then a is bigger than b, so a is at least nine, and a plus b is at least seventeen. That's not "
        "smaller than sixteen.", show(f3, 'Can b plus c be fourteen')),
      L("So b plus c can't be fourteen, and choice number four is our answer. The question asks for the one value that "
        "cannot happen, so we can stop here. [pause] Okay. I'll see you in the next question.",
        mk('tick', 'choice 4', 'and choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-578 (Hebrew: second sample question)
# NEW: "one letter is multiplied - by what is the other multiplied?" - start from an easy pair that fits (1 and 1), then
# the new value; powers of 5 instead of 25 cubed (R36).  REMINDER: power rules (topic 8), roots (9).
# Hebrew: plugging in first (her recommendation for most students), then the algebra with k, and the strong students'
# shortcut in the head.
g1 = IH('g1', '$b=1$: $\\ y^2=1^3=1$, $\\ y=1$', size=32)
g2 = IH('g2', '$b=25$: $\\ y^2=25^3=(5^2)^3=5^6$', size=32)
g3 = IH('g3', '$y=5^3=125$: $\\ 1\\to125$', size=32)
h1 = IH('h1', '$(ky)^2=(25b)^3$', size=32)
h2 = IH('h2', '$k^2y^2=25^3b^3$', size=32)
h3 = IH('h3', '$k^2=25^3=5^6$, $\\ k=5^3=125$', size=32)
h4 = I('h4', '$25^3=25^2\\cdot5^2=(25\\cdot5)^2=125^2$', size=30, col=1)
video('solve-q-578', 'solution', qid='q-578', slides=[
    S('Method 1 · Plugging in numbers',
      L("Given: b and y are positive, and y squared is equal to b cubed. If b is multiplied by twenty-five, by what factor "
        "is y multiplied?", pt('stem', 'Given', 'hl', 7.0), voice='calm', pause=0.5),
      L("So b changes, and we need to know how y has to change so that the equation still holds. [short pause] We'll solve "
        "it two ways. This time we start with plugging in numbers, because here it's the simpler way for most students, "
        "and then we'll do the algebra.", pt('stem: ask', 'how y has to change')),
      L("[short pause] First we need one pair of numbers that fits the equation. The easiest pair is b is one and y is one, "
        "because one squared and one cubed are both one. If you don't see it, put b is one. Then y squared is one. y could "
        "be one or negative one, but y is positive, so y is one.", show(g1, 'put b is one')),
      L("Now multiply b by twenty-five, so the new b is twenty-five. Then y squared is twenty-five cubed. Twenty-five is "
        "five squared, so twenty-five cubed is five to the power of six.", show(g2, 'Then y squared is twenty-five cubed')),
      L("Which positive number, squared, gives five to the power of six? Five cubed, because five cubed times five cubed is "
        "five to the power of six. Five cubed is a hundred twenty-five. So y went from one to a hundred twenty-five, which "
        "means it was multiplied by a hundred twenty-five. Choice number one is our answer.",
        show(g3, 'Five cubed is a hundred twenty-five'), mk('tick', 'choice 1', 'Choice number one is our answer'))),
    S('Method 2 · Algebra',
      L("[pause] Now the algebra. When b is multiplied by twenty-five, the right side becomes the bracket twenty-five b, "
        "cubed. To keep the equation true, y has to be multiplied by some number too. Let's call that number k. So the "
        "bracket k y, squared, equals the bracket twenty-five b, cubed.", show(h1, "Let's call that number k")),
      L("Open the brackets with the power rules. k squared times y squared equals twenty-five cubed times b cubed. We know "
        "that y squared equals b cubed, and it isn't zero, so we can divide both sides by it.", show(h2, 'Open the brackets')),
      L("That leaves k squared equals twenty-five cubed, which is five to the power of six. y stays positive, so k is "
        "positive, and k is five cubed, a hundred twenty-five. Choice number one again.",
        show(h3, 'That leaves k squared'), mk('tick', 'choice 1', 'Choice number one again')),
      L("Some students see this in their head. Twenty-five cubed is twenty-five squared times twenty-five, and twenty-five "
        "is five squared. So twenty-five cubed is the square of twenty-five times five, which is a hundred twenty-five. "
        "[pause] Okay. I'll see you in the next question.", show(h4, 'Some students see this in their head'))),
])

# ------------------------------------------------------------------------------------------------ q-579 (Hebrew: third sample question)
# NEW: simplify first (common denominator), then "not necessarily true" = one allowed case where it fails; Pythagorean
# triples (3, 4, 5 and 6, 8, 10).  REMINDER: Pythagoras and the triangle inequality (topic 31, earlier in the plan).
# Hebrew: simplify, then the right-triangle picture (the hypotenuse is the longest side, two sides are longer than the
# third, the smallest triple).  Methods: whole numbers (find the failing case), the right triangle (why the others hold).
TRI20 = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 230" role="img" aria-label="A right triangle with legs p '
         'and q and the longest side r"><title>A right triangle with legs p and q and the longest side r</title>'
         '<path d="M 60 190 L 300 190 L 60 40 Z" fill="none" stroke="#203344" stroke-width="3"/>'
         '<path d="M 60 168 L 82 168 L 82 190" fill="none" stroke="#203344" stroke-width="2.5"/>'
         '<text x="38" y="122" text-anchor="middle" fill="#087f83" font-family="DejaVu Sans,Arial,sans-serif" font-size="30" '
         'font-weight="bold" font-style="italic">p</text>'
         '<text x="180" y="222" text-anchor="middle" fill="#087f83" font-family="DejaVu Sans,Arial,sans-serif" font-size="30" '
         'font-weight="bold" font-style="italic">q</text>'
         '<text x="196" y="104" text-anchor="middle" fill="#087f83" font-family="DejaVu Sans,Arial,sans-serif" font-size="30" '
         'font-weight="bold" font-style="italic">r</text></svg>')
tr = NL('tr', TRI20, w=300, col=1)
k1 = IH('k1', '$\\frac pq+\\frac qp=\\frac{p^2+q^2}{pq}$', size=32)
k2 = IH('k2', '$r^2=p^2+q^2$', size=34)
k3 = IH('k3', '$3,4,5$: $\\ 9+16=25$, $\\ r=5$', size=32)
k4 = IH('k4', '$6,8,10$: $\\ 36+64=100$, $\\ r=10$ ✗', size=32)
m1 = I('m1', 'Longest side: $\\ r>p,\\ r>q$ $\\quad$ (1), (4)', size=30)
m2 = I('m2', 'Two sides beat the third: $\\ p+q>r$ $\\quad$ (2)', size=30)
video('solve-q-579', 'solution', qid='q-579', slides=[
    S('Simplify first',
      L("Given: p, q and r are different positive integers, and r squared over p q is equal to p over q plus q over p. "
        "Which of the following is not necessarily true?", pt('stem', 'Given', 'hl', 9.0), voice='calm', pause=0.5),
      L("The equation looks complicated, so first we simplify it. Not necessarily true means it fails in at least one "
        "allowed case. So we're looking for the claim that can fail. [short pause] We'll solve it two ways, with whole "
        "numbers that fit, and then with a right triangle, which shows why the other claims always hold.",
        pt('stem: ask', 'Not necessarily true means')),
      L("[short pause] Let's simplify the right side. To add p over q and q over p, we need a common denominator, p times "
        "q. p over q is p squared over p q, and q over p is q squared over p q. So the right side is p squared plus q "
        "squared, over p q.", show(k1, 'we need a common denominator')),
      L("Both sides now have the same denominator, p q, so their tops are equal. r squared equals p squared plus q "
        "squared.", show(k2, 'r squared equals p squared'))),
    S('Method 1 · Whole numbers',
      L("[pause] Now we need positive integers that fit r squared equals p squared plus q squared. The best-known ones are "
        "three, four and five, because nine plus sixteen is twenty-five. Here r is five.", show(k3, 'three, four and five')),
      L("Choice number three says r is smaller than eight. With three, four and five it's true, but we need a case where "
        "it fails. Let's double all three numbers: six, eight and ten. Thirty-six plus sixty-four is a hundred, which is "
        "ten squared, so they fit too, and they're different positive integers. Now r is ten, and ten is not smaller than "
        "eight.", show(k4, 'six, eight and ten')),
      L("So choice number three fails in an allowed case. It's not necessarily true, and choice number three is our "
        "answer. One allowed case where it fails is all the question asks for, so we can stop here.",
        mk('tick', 'choice 3', 'and choice number three is our')),
      sb='Method 1 · Whole numbers'),
    S('Method 2 · A right triangle',
      L("[pause] Now let's see why the other three claims always hold. r squared equals p squared plus q squared is "
        "Pythagoras. So p, q and r can be the sides of a right triangle, with legs p and q, and the longest side, r.",
        show(tr, 'can be the sides of a right triangle')),
      L("In a right triangle, the longest side is longer than each leg. So r is bigger than p and bigger than q, always. "
        "Those are choice numbers one and four. With algebra it's the same idea: r squared is q squared plus a positive "
        "number, and all the numbers are positive, so r is bigger than q.", show(m1, 'the longest side is longer')),
      L("And in any triangle, two sides together are longer than the third side. So p plus q is bigger than r, always. "
        "That's choice number two.", show(m2, 'two sides together are longer')),
      L("But nothing in the triangle says how long r is. For three, four, five it's five, and for six, eight, ten it's ten. "
        "So only choice number three can fail. Choice number three. [pause] Okay. I'll see you in the next question.",
        mk('tick', 'choice 3', 'So only choice number three can fail'))),
])

# ------------------------------------------------------------------------------------------------ r26-t20-counting (lesson)
# REMINDER: from a to b, both ends included, b - a + 1 (topic 16).  NEW: strictly between (b - a - 1), one end (b - a);
# the pigeonhole principle with two everyday examples and the remainder version (remainders: topic 15).
p1 = I('p1', 'From $a$ to $b$, both included: $\\ b-a+1$ $\\quad 5$ to $12$: $\\ 8$', size=30)
p2 = I('p2', 'Strictly between: $\\ b-a-1$ $\\quad 6,7,8,9,10,11$: $\\ 6$', size=30)
p3 = I('p3', 'One end included: $\\ b-a$ $\\quad 5$ to $11$: $\\ 7$', size=30)
p4 = I('p4', 'Not sure? Count a small case. Letters? Plug in and count.', size=28)
q1 = I('q1', 'More items than boxes $\\to$ one box gets two', size=30)
q2 = I('q2', '$13$ people, $12$ months $\\to$ two share a month', size=30)
q3 = I('q3', '$\\div12$: remainders $0$ to $11$ $\\to$ $13$ numbers: two share one', size=30)
q4 = I('q4', '$17$ and $41$: remainder $5$ $\\to$ $41-17=24=2\\cdot12$', size=30)
video('r26-t20-counting', 'lesson', slides=[
    S('Counting Integers & Pigeonhole',
      L("Two more tools that the exam likes. Counting the whole numbers in a range, and the pigeonhole principle.")),
    S('Counting whole numbers',
      L("From a to b, with both ends included, there are b minus a, plus one, whole numbers. You learned this with "
        "consecutive integers. For example, from five to twelve, it's twelve minus five, plus one, which is eight numbers.",
        show(p1, 'From a to b')),
      L("Strictly between five and twelve means both ends are out. That leaves six, seven, eight, nine, ten and eleven, "
        "which is six numbers. That's twelve minus five, minus one.", show(p2, 'Strictly between five and twelve')),
      L("With one end in and one end out, it's just b minus a. From five to twelve, with five included and twelve not, "
        "that's five to eleven, which is seven numbers.", show(p3, 'With one end in')),
      L("If you're not sure which rule to use, count a small case on your fingers, like from one to three. And if the "
        "answer choices have letters, plug in small numbers, count by hand, and see which choice gives your count.",
        show(p4, "If you're not sure"))),
    S('The pigeonhole principle',
      L("Now the pigeonhole principle. If there are more items than boxes, at least one box gets two items. Think of four "
        "pigeons and three holes. Even if each of the first three pigeons gets its own hole, the fourth one has to share.",
        show(q1, 'If there are more items than boxes')),
      L("Another example. Thirteen people, and there are only twelve months. Even if the first twelve were born in twelve "
        "different months, the thirteenth shares a month with someone. So at least two of them were born in the same "
        "month.", show(q2, 'Thirteen people')),
      L("On the exam it often comes with remainders. When we divide a whole number by twelve, the remainder is one of "
        "twelve options, zero to eleven. So among any thirteen whole numbers, two have the same remainder.",
        show(q3, 'it often comes with remainders')),
      L("And two numbers with the same remainder have a difference that divides by twelve. For example, seventeen and "
        "forty-one both leave a remainder of five. Their difference is twenty-four, which is two times twelve. Next, two "
        "questions, one on counting odd numbers and one on being sure. [pause] Okay. I'll see you in the next video.",
        show(q4, 'seventeen and forty-one'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t20-03 (added)
# REMINDER: counting evens / odds in steps of two (topic 16), the + 1 trap.  Methods: steps of two, half of all.
r1 = IH('r1', '$21,\\ 23,\\ \\ldots,\\ 79$', size=32)
r2 = IH('r2', '$\\frac{79-21}{2}=29$, $\\ 29+1=30$', size=32)
r3 = IH('r3', '$21$ to $80$: $\\ 80-21+1=60$', size=32)
r4 = IH('r4', '$60\\div2=30$', size=32)
video('solve-q-r26-t20-03', 'solution', qid='q-r26-t20-03', slides=[
    S('Method 1 · Steps of two',
      L("How many odd numbers are there between twenty and eighty?", pt('stem', 'How many odd numbers', 'hl', 4.0),
        voice='calm', pause=0.5),
      L("We need to count them without listing all of them. [short pause] We'll solve it two ways, jumping by two from the "
        "first odd number to the last, and then taking half of all the numbers.", pt('stem', 'without listing')),
      L("[short pause] Twenty and eighty are even, so they wouldn't count anyway. The first odd number after twenty is "
        "twenty-one, and the last odd number before eighty is seventy-nine.", show(r1, 'The first odd number after twenty')),
      L("Odd numbers go up in steps of two. From twenty-one to seventy-nine is seventy-nine minus twenty-one, which is "
        "fifty-eight. Fifty-eight divided by two is twenty-nine steps. Each step lands on a new odd number, and we also "
        "count the first one, twenty-one. So twenty-nine plus one is thirty. Choice number two is our answer.",
        show(r2, 'Fifty-eight divided by two'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Careful, twenty-nine, choice number one, is the number of steps. It forgets to count the first number.",
        mk('cross', 'choice 1', 'Careful, twenty-nine, choice number one'))),
    S('Method 2 · Half of all',
      L("[pause] Another way. Count all the whole numbers from twenty-one to eighty, both ends included. Eighty minus "
        "twenty-one, plus one, is sixty.", show(r3, 'Eighty minus twenty-one')),
      L("They take turns, odd, even, odd, even. The list starts with an odd number, twenty-one, and ends with an even "
        "number, eighty, so they come in pairs, and exactly half of them are odd. Sixty divided by two is thirty. Choice "
        "number two again. Sixty, choice number four, forgets to take half. [pause] Okay. I'll see you in the next "
        "question.", show(r4, 'Sixty divided by two'), mk('tick', 'choice 2', 'Choice number two again'),
        mk('cross', 'choice 4', 'forgets to take half'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t20-04 (added)
# REMINDER: the pigeonhole principle (r26-t20-counting).  NEW at the step: "to be sure" = the worst luck, then one more.
s1 = I('s1', 'Worst luck: $\\ $red, blue, green $\\to$ $3$ socks, no pair', size=30)
s2 = I('s2', '$4$th sock: red, blue or green $\\to$ a pair ✓', size=30)
s3 = I('s3', '$3$ colors $=3$ boxes: $\\ 4$ socks $\\to$ one box gets two', size=30)
video('solve-q-r26-t20-04', 'solution', qid='q-r26-t20-04', slides=[
    S('The worst luck',
      L("A drawer holds five red socks, seven blue socks and nine green socks. Dana takes socks out of the drawer without "
        "looking. What is the smallest number of socks she must take out to be sure she has two socks of the same color?",
        pt('stem', 'A drawer holds', 'hl', 11.0), voice='calm', pause=0.5),
      L("To be sure means it has to work even with the worst luck. [short pause] We'll solve it by imagining the worst "
        "luck, and then we'll see the pigeonhole principle behind it.", pt('stem: ask', 'To be sure means')),
      L("[short pause] With the worst luck, the first socks are all different colors. There are three colors, so the first "
        "three socks could be one red, one blue and one green. Three socks, and still no pair. So two or three socks are "
        "not enough.", show(s1, 'With the worst luck'), mk('cross', 'choice 2', 'So two or three socks'),
        mk('cross', 'choice 3', 'are not enough')),
      L("Now the fourth sock. It's red, blue or green, so whatever it is, it matches one of the socks she already has. So "
        "four socks always give a pair, and three socks don't. The smallest number is four. Choice number four is our "
        "answer.", show(s2, 'Now the fourth sock'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    S('The pigeonhole principle',
      L("[pause] This is the pigeonhole principle. The three colors are three boxes, and the socks are the items. Four "
        "socks in three boxes means at least one box gets two socks. Choice number four.", show(s3, 'The three colors are three boxes'),
        mk('tick', 'choice 4', 'at least one box gets two socks')),
      L("The numbers five, seven and nine don't change the answer, because every color has more than one sock. [pause] "
        "Okay. I'll see you in the next question.", pt('stem', 'The numbers five, seven and nine'))),
])

# ------------------------------------------------------------------------------------------------ r26-t20-summary
# REMINDERS only, as connected sentences (Codex review standard: no headings read aloud), new numbers.
t1 = I('t1', 'Plug in numbers $\\quad$ test the answers $\\quad$ algebra', size=30)
t2 = I('t2', 'Must: one failing case rules it out $\\quad$ could: one working example', size=26)
t3 = I('t3', 'Cannot: never works (find the biggest / smallest) $\\quad$ not necessarily: fails once', size=26)
t4 = I('t4', 'Allowed numbers only $\\quad$ positive: $\\ x>1$ and $0<x<1$', size=28)
t5 = I('t5', 'Letters may be equal? Try equal values too.', size=28)
t6 = I('t6', '$0<x<1$: $\\ x^2<x<\\sqrt{x}<1<\\frac1x$ $\\quad$ negatives: $-7<-3$', size=28)
t7 = I('t7', 'Integer $<20\\ \\to\\ \\le19$ $\\quad a>b>c$ integers: $\\ a\\ge c+2$', size=28)
t8 = I('t8', '$x^2=a^3$: $\\ a=1\\to9$: $\\ x^2=9^3=3^6$, $\\ x=27$', size=28)
t9 = I('t9', '$c^2=a^2+b^2$ whole numbers: $\\ c$ longest, $\\ a+b>c$, $\\ 3,4,5$', size=28)
t10 = I('t10', 'Both ends: $\\ b-a+1$ $\\quad$ none: $\\ b-a-1$ $\\quad$ one: $\\ b-a$ $\\quad$ odd only: $\\ \\frac{\\text{last}-\\text{first}}{2}+1$', size=24)
t11 = I('t11', 'More items than boxes: one box gets two $\\quad$ to be sure: worst luck, then one more', size=26)
video('r26-t20-summary', 'lesson', slides=[
    S('Algebraic Understanding: Summary',
      L("Before you practice, here's a quick summary of the topic. The three tools, how to choose numbers, and the "
        "counting tools.")),
    S('Three tools',
      L("There's no fixed recipe in this topic, but three tools open almost every question. Plug in numbers, test the "
        "answer choices, and use algebra when the numbers don't decide. Numbers are usually the fastest place to start.",
        show(t1, 'three tools open almost every question')),
      L("Read the question word first. When it asks what must be true, one allowed case where a choice fails rules that "
        "choice out. When it asks what could be true, one allowed example that works is enough.", show(t2, 'Read the question word first')),
      L("When it asks what cannot be true, look for the one value that never works, often by finding the biggest or the "
        "smallest possible value. And not necessarily true means it fails in at least one allowed case.",
        show(t3, 'When it asks what cannot be true'))),
    S('Which numbers?',
      L("Use only numbers the givens allow. Start with an easy one, check the choices right away, and try a number from "
        "another region only if more than one choice is left. For positive numbers, the two regions are numbers bigger "
        "than one, and numbers between zero and one.", show(t4, 'Use only numbers the givens allow')),
      L("Different letters can be equal unless the question says they're different. So when equal values are allowed, "
        "try them too.", show(t5, 'Different letters can be equal')),
      L("Between zero and one, squaring makes a number smaller, and the square root makes it bigger. With negative "
        "numbers, the farther a number is from zero, the smaller it is. And when the question asks for the smallest or the "
        "biggest for every x in a range, one easy number from the range decides.", show(t6, 'Between zero and one'))),
    S('Gaps, scaling, other topics',
      L("Integers leave gaps. An integer smaller than twenty is at most nineteen. And if a is bigger than b, which is "
        "bigger than c, all integers, then a is at least c plus two. Use these gaps to find the biggest or the smallest "
        "possible value.", show(t7, 'Integers leave gaps')),
      L("When one letter is multiplied, start from an easy pair that fits, like one and one, then put in the new value. "
        "For example, if x squared equals a cubed, x is positive, and a is multiplied by nine, then a is nine, and x "
        "squared is nine cubed, which is three to the power of six. So x is three cubed, twenty-seven, and x was "
        "multiplied by twenty-seven.", show(t8, 'When one letter is multiplied')),
      L("Sometimes the key is a structure from another topic. If whole numbers fit c squared equals a squared plus b "
        "squared, think of a right triangle. c is the longest side, a plus b is longer than c, and the smallest whole "
        "numbers that fit are three, four and five.", show(t9, 'a structure from another topic'))),
    S('Counting and pigeonhole',
      L("To count whole numbers from a to b: with both ends in, it's b minus a, plus one. With both ends out, b minus a, "
        "minus one. With one end in, just b minus a. For only odd or only even numbers, find the first and the last that "
        "count, take the difference, divide by two, and add one.", show(t10, 'To count whole numbers')),
      L("More items than boxes means some box gets two. To be sure, imagine the worst luck, one item in every box, and "
        "then add one more. [pause] That's it. Now go practice, and with that you've finished algebra. I'll see you in "
        "the next video.", show(t11, 'More items than boxes'))),
])

# carry-over boxes on the continuation slides (V2): the next step uses these results
CARRY20 = {'solve-q-r26-t20-01': {1: ['(4) out']}}

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
 "q-r26-t20-01": "Given: $x$ and $y$ are positive numbers, and $x>y$. Which of the following must be true?",
 "q-r26-t20-02": "Given: $-1<x<0$. Which of the following is the smallest?",
 "q-577": "Given: $a$, $b$ and $c$ are integers, and\n$\\begin{cases} c<b<a \\\\ a+b<16 \\end{cases}$\nWhich of the following cannot be the value of $b+c$?",
 "q-578": "Given:\n$\\begin{cases} b>0,\\ y>0 \\\\ y^2=b^3 \\end{cases}$\nIf $b$ is multiplied by $25$, by what factor is $y$ multiplied?",
 "q-579": "Given: $p$, $q$ and $r$ are different positive integers, and $\\frac{r^2}{pq}=\\frac{p}{q}+\\frac{q}{p}$. Which of the following is not necessarily true?"
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



# 2026-10-13 carry-over boxes (V2) and the layer-order check (V1): after the visual passes, like topics 13-18
import types as _types
MV.carry(_types.SimpleNamespace(**globals()), CARRY20)
MV.calm(_types.SimpleNamespace(**globals()), ORDER)     # 2026-10-13 steady highlights (visual only)
_lp = [(v, p) for v in ORDER for p in MV.check_layers(VIDEOS[v])]
assert not _lp, ('figure layers out of order', _lp)


if __name__ == '__main__':
    _bad = 0
    for _v in sys.argv[1:] or ORDER:
        _p = check(_v)
        if _p: print('PROBLEMS', _v, _p); _bad += 1
        print('script written:', write_json(_v), stats(_v))
    for x in WRITE_LATE: print('mark dropped (its item is still being written):', x)
    sys.exit(1 if _bad else 0)
