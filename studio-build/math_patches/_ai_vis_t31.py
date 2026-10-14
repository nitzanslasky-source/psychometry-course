"""Topic 31 (Triangles) - the scripts for the teacher's own-voice reading (2026-10-14), written from the first draft to
the Codex review standard, the clarity style, the method visuals (geometry: the angle figure built in layers, GEO below), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py / _ai_vis_t16.py / _ai_vis_t17.py / _ai_vis_t18.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The camera lesson 'geo-009' gets its own reading script here too, in parts of about 3-4 minutes (2026-10-14: she reads it
with the camera on). Every other topic-31 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t31.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t31.py ai_redo_t31() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods and EVERY method of the Hebrew solution (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-31-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t31ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-31 flow order of the scripts
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
            'style': "the teacher reads it herself (Reading Studio), topic-31 scripts (2026-10-14): math_patches/_ai_vis_t31.py is "
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


# ------------------------------------------------------------------------------------------- topic-31 geometry figures (V1)
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



CARRY31 = {}       # carry-over boxes (V2): {vid: {slide index: [tex, ...]}}, filled by the scripts


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


# ------------------------------------------------------------------------------------------------ geo-009 (camera lesson, in parts)
# 2026-10-14 her camera first lesson of triangles as a reading script (same style, handwriting, camera on), with more
# examples, split into parts of about 3-4 minutes (CAMERA_SPLIT at the end). Hebrew: geo 405-495 (the triangles-basics
# lesson: median, altitude inside / outside, the angle sum with its proof, the exterior angle with its proof and "it can
# save time", side vs angle with the opening-angle image, two sides > the third with the lifting picture and the
# home-to-the-club walk, the extension: between the difference and the sum; the close: the angle sum is the one to take).
# Her worked questions (alpha 3alpha 2alpha; 2alpha + gamma; 5 and 9) are the videos g010, g011, g012. Kept from the
# English lesson: the angle bisector (taught in topic 30, here inside a triangle), "median / altitude / bisector are three
# different lines", the two routes for the exterior angle, the whole-number count. Special triangles, area and
# Pythagoras are later lessons (geo-013, geo-016, geo-019).
# Study plan: day 2, after topics 1, 30, 2, 4 - so lines and angles (the Z, adjacent angles, the bisector) are short
# reminders; nothing else assumed.
# Visuals (V3): every figure built step by step at her words; a line we draw IN (a median, an altitude, a parallel
# line, an extension) is teal (dashed when it is a construction / extension); equal pieces get tick marks, right angles the
# square; the angle under discussion teal, its partner orange; a wrong idea red; values written on the figure when found.
import math as _f1m


def f1_mid(p, q):
    return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)


def f1_foot(p, a, b):
    """the foot of the perpendicular from p to the line a-b"""
    ax, ay = a; bx, by = b; dx, dy = bx - ax, by - ay
    t = ((p[0] - ax) * dx + (p[1] - ay) * dy) / float(dx * dx + dy * dy)
    return (ax + t * dx, ay + t * dy)


def f1_bis(c, a, b):
    """where the bisector of the angle at c meets the side a-b"""
    la = _f1m.hypot(a[0] - c[0], a[1] - c[1]); lb = _f1m.hypot(b[0] - c[0], b[1] - c[1])
    t = la / (la + lb)
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def f1_ang(v, p, q):
    """the angle at v between v->p and v->q, in degrees"""
    d1, d2 = gdir(v[0], v[1], p[0], p[1]), gdir(v[0], v[1], q[0], q[1])
    d = (d2 - d1) % 360
    return min(d, 360 - d)


def f1_arcpts(v, p, q, r, col, lab=None, lr=None):
    """an angle arc at v between the rays to p and q (the smaller angle)"""
    d1, d2 = gdir(v[0], v[1], p[0], p[1]), gdir(v[0], v[1], q[0], q[1])
    if (d2 - d1) % 360 > 180: d1, d2 = d2, d1
    e = ('arc', v[0], v[1], r, d1, d2, col)
    if lab: e = e + (lab, lr if lr else r + 22)
    return e


def f1_tri(a, b, c, w=3):
    return [('seg', a[0], a[1], b[0], b[1], 'ink', w), ('seg', b[0], b[1], c[0], c[1], 'ink', w), ('seg', c[0], c[1], a[0], a[1], 'ink', w)]


def f1_lab(a, b, c, d=26, names=('A', 'B', 'C')):
    """vertex labels, pushed away from the centre"""
    g = ((a[0] + b[0] + c[0]) / 3.0, (a[1] + b[1] + c[1]) / 3.0); out = []
    for p, n in zip((a, b, c), names):
        L = _f1m.hypot(p[0] - g[0], p[1] - g[1]) or 1
        out.append(('txt', p[0] + (p[0] - g[0]) / L * d, p[1] + (p[1] - g[1]) / L * d, n, 'ink', 26, True))
    return out


# ---- the main triangle (acute), used for the three special lines
F1A, F1B, F1C = (110, 290), (530, 290), (250, 60)
F1M = f1_mid(F1A, F1B)                      # midpoint of AB
F1H = f1_foot(F1C, F1A, F1B)                # foot of the altitude from C
F1base = f1_tri(F1A, F1B, F1C) + f1_lab(F1A, F1B, F1C)

# ---- slide: the median
_mA = f1_mid(F1B, F1C); _mB = f1_mid(F1A, F1C)
_G = ((F1A[0] + F1B[0] + F1C[0]) / 3.0, (F1A[1] + F1B[1] + F1C[1]) / 3.0)
f1med = GEO('f1med', [
    ('line', F1base),
    ('mid', [('dot', F1M[0], F1M[1]), ('txt', F1M[0], F1M[1] + 28, 'M', 'ink', 24, True)]),
    ('med', [('seg', F1C[0], F1C[1], F1M[0], F1M[1], 'teal', 4)]),
    ('ticks', [('tick', F1A[0], F1A[1], F1M[0], F1M[1], 1), ('tick', F1M[0], F1M[1], F1B[0], F1B[1], 1),
               ('txt', (F1A[0] + F1M[0]) / 2, 318, '5', 'teal', 24), ('txt', (F1M[0] + F1B[0]) / 2, 318, '5', 'teal', 24),
               ('txt', 480, 50, 'AB = 10:  AM = MB = 5', 'teal', 22)]),
    ('not', [('txt', 470, 120, 'no right angle', 'red', 22), ('txt', 470, 150, 'no equal angles', 'red', 22)]),
    ('three', [('seg', F1A[0], F1A[1], _mA[0], _mA[1], 'teal', 4), ('seg', F1B[0], F1B[1], _mB[0], _mB[1], 'teal', 4),
               ('tick', F1B[0], F1B[1], _mA[0], _mA[1], 2), ('tick', _mA[0], _mA[1], F1C[0], F1C[1], 2),
               ('tick', F1A[0], F1A[1], _mB[0], _mB[1], 3), ('tick', _mB[0], _mB[1], F1C[0], F1C[1], 3)]),
    ('meet', [('dot', _G[0], _G[1]), ('arc', _G[0], _G[1], 14, 0, 359.9, 'orange')]),
], vb='60 20 540 330', w=740, col=0, title='A median joins a vertex to the middle of the opposite side')

# ---- slide: the altitude (acute)
_hA = f1_foot(F1A, F1B, F1C); _hB = f1_foot(F1B, F1A, F1C)
_O = (F1H[0], F1A[1] - (F1H[0] - F1A[0]) * (F1B[0] - F1C[0]) / float(F1C[1] - F1B[1]) * 0)  # placeholder, recomputed below


def _f1orth(a, b, c):
    """the meeting point of the altitudes"""
    hb = f1_foot(b, a, c); ha = f1_foot(a, b, c)
    return gcross(a, ha, b, hb)


_OR = _f1orth(F1A, F1B, F1C)
f1alt = GEO('f1alt', [
    ('line', F1base),
    ('alt', [('seg', F1C[0], F1C[1], F1H[0], F1H[1], 'teal', 4), ('dot', F1H[0], F1H[1]),
             ('txt', F1H[0], F1H[1] + 28, 'H', 'ink', 24, True)]),
    ('sq', [('right', F1H[0], F1H[1], 0, 90, 18)]),
    ('nomid', [('dot', F1M[0], F1M[1]), ('txt', F1M[0] + 2, F1M[1] + 28, 'middle', 'red', 20),
               ('txt', 470, 120, 'H is not the middle', 'red', 22), ('txt', 470, 150, 'a right angle only', 'teal', 22)]),
    ('three', [('seg', F1A[0], F1A[1], _hA[0], _hA[1], 'teal', 3, True), ('seg', F1B[0], F1B[1], _hB[0], _hB[1], 'teal', 3, True),
               ('dot', _OR[0], _OR[1])]),
], vb='60 20 540 330', w=740, col=0, title='An altitude meets the opposite side at a right angle')

# ---- slide: the altitude outside (obtuse)
P1A, P1B, P1C = (330, 270), (560, 270), (150, 110)        # obtuse at A
_ext_end = (110, 270)
P1H = f1_foot(P1C, P1A, P1B)
f1out = GEO('f1out', [
    ('line', f1_tri(P1A, P1B, P1C) + f1_lab(P1A, P1B, P1C)),
    ('obt', [f1_arcpts(P1A, P1B, P1C, 22, 'orange'), ('txt', 330, 235, 'obtuse', 'orange', 20)]),
    ('try', [('seg', P1C[0], P1C[1], 500, 270, 'red', 3, True), ('txt', 500, 300, 'slanted', 'red', 20)]),
    ('ext', [('seg', P1A[0], P1A[1], _ext_end[0], _ext_end[1], 'teal', 3, True), ('txt', 240, 255, 'extension', 'teal', 20)]),
    ('alt', [('seg', P1C[0], P1C[1], P1H[0], P1H[1], 'teal', 4), ('right', P1H[0], P1H[1], 0, 90, 16)]),
    ('floor', [('tint', [(90, 270), (600, 270), (600, 285), (90, 285)], 'orange'), ('txt', 240, 310, 'the floor', 'orange', 22)]),
], vb='80 60 520 270', w=740, col=0, title='In an obtuse triangle, an altitude can fall outside')

# ---- slide: the bisector
# ---- slide: the bisector (its own triangle: angles 60 at A, 50 at B, so exactly 70 at C)
B1A, B1B, B1C = (150, 290), (490, 290), (288.6, 50.0)
B1D = f1_bis(B1C, B1A, B1B)
f1bis = GEO('f1bis', [
    ('line', f1_tri(B1A, B1B, B1C) + f1_lab(B1A, B1B, B1C)),
    ('bis', [('seg', B1C[0], B1C[1], B1D[0], B1D[1], 'teal', 4), ('dot', B1D[0], B1D[1]),
             ('txt', B1D[0], B1D[1] + 28, 'D', 'ink', 24, True)]),
    ('halves', [f1_arcpts(B1C, B1A, B1D, 34, 'teal', 'α', 56), f1_arcpts(B1C, B1D, B1B, 44, 'teal', 'α', 66),
                ('txt', 480, 60, 'C = 70°:  35° and 35°', 'teal', 22)]),
    ('pieces', [('seg', B1A[0], 306, B1D[0], 306, 'orange', 4), ('seg', B1D[0], 314, B1B[0], 314, 'red', 4),
                ('txt', (B1A[0] + B1D[0]) / 2, 334, 'AD', 'orange', 22), ('txt', (B1D[0] + B1B[0]) / 2, 336, 'DB, longer', 'red', 22)]),
], vb='60 5 540 345', w=740, col=0, title='The angle bisector splits the angle at C into two equal angles')
f1three = I('f1three', 'Median: equal pieces $\\quad$ altitude: $90°$ $\\quad$ bisector: equal angles', size=26, col=0)

# ---- slide: the angle sum (the proof)
S1A, S1B, S1C = (120, 290), (520, 290), (300, 90)
f1sum = GEO('f1sum', [
    ('line', f1_tri(S1A, S1B, S1C) + f1_lab(S1A, S1B, S1C)),
    ('abc', [f1_arcpts(S1A, S1B, S1C, 36, 'teal', 'α', 60), f1_arcpts(S1B, S1A, S1C, 36, 'orange', 'β', 60),
             f1_arcpts(S1C, S1A, S1B, 30, 'red', 'γ', 52)]),
    ('par', [('seg', 40, 90, 600, 90, 'teal', 3, True), ('par', 470, 90, 560, 90), ('par', 300, 290, 420, 290)]),
    ('z1', [('path', [(60, 90), (300, 90), (120, 290), (330, 290)], 'teal', 7),
            ('arc', 300, 90, 30, 180, 180 + gdir(300, 90, 120, 290) - 180, 'teal', 'α', 54)]),
    ('z2', [('path', [(580, 90), (300, 90), (520, 290), (290, 290)], 'orange', 7),
            ('arc', 300, 90, 30, gdir(300, 90, 520, 290), 360, 'orange', 'β', 54)]),
    ('line180', [('arc', 300, 90, 70, 180, 360, 'teal'), ('txt', 300, 30, 'α + γ + β = 180°', 'teal', 26)]),
], vb='30 0 580 340', w=760, col=0, title='Why the three angles of a triangle add up to 180 degrees')
f1sum_t = IH('f1sumt', '$\\alpha+\\beta+\\gamma=180°$', size=34, col=1)
f1ex1 = IH('f1ex1', '$50°+60°+x=180°$: $\\ x=70°$', size=34, col=0)
f1ex2 = IH('f1ex2', '$90°+35°+x=180°$: $\\ x=55°$', size=34, col=0)
f1ex3 = I('f1ex3', '$100°+95°>180°$: $\\ $not a triangle', size=34, col=0)

# ---- slide: the exterior angle
E1A, E1B, E1C = (110, 290), (330, 80), (440, 290)
_Eext = (610, 290)
f1ext = GEO('f1ext', [
    ('line', f1_tri(E1A, E1B, E1C) + f1_lab(E1A, E1B, E1C)),
    ('ext', [('seg', E1C[0], E1C[1], _Eext[0], _Eext[1], 'teal', 3, True)]),
    ('delta', [f1_arcpts(E1C, _Eext, E1B, 34, 'teal', 'δ', 60)]),
    ('gamma', [f1_arcpts(E1C, E1A, E1B, 26, 'orange', 'γ', 48)]),
    ('ab', [f1_arcpts(E1A, E1C, E1B, 40, 'red', 'α', 64), f1_arcpts(E1B, E1A, E1C, 30, 'red', 'β', 52)]),
], vb='60 30 580 300', w=760, col=0, title='An exterior angle of a triangle')
f1ext_t1 = IH('f1ext1', '$\\gamma+\\delta=180°$', size=30, col=1)
f1ext_t2 = IH('f1ext2', '$\\alpha+\\beta+\\gamma=180°$', size=30, col=1)
f1ext_t3 = IH('f1ext3', '$\\delta=\\alpha+\\beta$', size=34, col=1)

# ---- slide: two routes (a number example)
R1A, R1B, R1C = (110, 290), (300, 70), (430, 290)
f1rt = GEO('f1rt', [
    ('line', f1_tri(R1A, R1B, R1C) + [('seg', R1C[0], R1C[1], 600, 290, 'teal', 3, True)]),
    ('given', [f1_arcpts(R1A, R1C, R1B, 40, 'red', '47°', 66), f1_arcpts(R1B, R1A, R1C, 30, 'red', '68°', 54)]),
    ('ex', [f1_arcpts(R1C, (600, 290), R1B, 34, 'teal', '115°', 66), ('txt', 700, 70, 'Shortcut: 47° + 68° = 115°', 'teal', 26)]),
    ('in', [f1_arcpts(R1C, R1A, R1B, 26, 'orange', '65°', 50), ('txt', 700, 130, 'Long way: 180° − 47° − 68° = 65°', 'orange', 26),
            ('txt', 700, 170, '180° − 65° = 115°', 'orange', 26)]),
    ('more', [('txt', 700, 240, 'Another: 30° + 80° = 110°', 'red', 26)]),
], vb='60 30 860 290', w=1060, col=0, title='The exterior angle: the shortcut and the long way')

# ---- slide: side against angle
K1A, K1B, K1C = (110, 290), (560, 290), (256.9, 35.6)   # angles 60, 40, 80 exactly
f1sa = GEO('f1sa', [
    ('line', f1_tri(K1A, K1B, K1C) + f1_lab(K1A, K1B, K1C)),
    ('angs', [f1_arcpts(K1A, K1B, K1C, 34, 'orange', '60°', 58), f1_arcpts(K1B, K1A, K1C, 46, 'teal', '40°', 74),
              f1_arcpts(K1C, K1A, K1B, 28, 'red', '80°', 50)]),
    ('small', [('seg', K1A[0], K1A[1], K1C[0], K1C[1], 'teal', 7), ('txt', 120, 170, 'shortest', 'teal', 22)]),
    ('big', [('seg', K1A[0], K1A[1], K1B[0], K1B[1], 'red', 7), ('txt', 335, 320, 'longest', 'red', 22)]),
    ('mid', [('seg', K1B[0], K1B[1], K1C[0], K1C[1], 'orange', 7), ('txt', 462, 132, 'middle', 'orange', 22)]),
], vb='60 0 560 340', w=600, col=0, title='The largest side lies opposite the largest angle')
f1sa_t = I('f1sat', 'Larger angle $\\leftrightarrow$ longer side opposite it', size=28, col=1)
# the opening angle: two sides of fixed length, the angle opens, the side opposite grows
f1open = GEO('f1open', [
    ('line', [('seg', 60, 200, 260, 200), ('seg', 60, 200, 60 + 200 * _f1m.cos(_f1m.radians(35)), 200 - 200 * _f1m.sin(_f1m.radians(35))),
              ('seg', 260, 200, 60 + 200 * _f1m.cos(_f1m.radians(35)), 200 - 200 * _f1m.sin(_f1m.radians(35)), 'teal', 5),
              ('arc', 60, 200, 40, 0, 35, 'teal', '35°', 78)]),
    ('wide', [('seg', 330, 200, 530, 200), ('seg', 330, 200, 330 + 200 * _f1m.cos(_f1m.radians(110)), 200 - 200 * _f1m.sin(_f1m.radians(110))),
              ('seg', 530, 200, 330 + 200 * _f1m.cos(_f1m.radians(110)), 200 - 200 * _f1m.sin(_f1m.radians(110)), 'red', 5),
              ('arc', 330, 200, 36, 0, 110, 'red', '110°', 74)]),
], vb='20 0 560 230', w=640, col=0, title='Open the angle wider, and the side opposite it gets longer')

# ---- slide: two sides are more than the third
T1L, T1R = (120, 260), (480, 260)        # the side 9 (40 px per cm)
_t4 = (T1L[0] + 160 * _f1m.cos(_f1m.radians(25)), T1L[1] - 160 * _f1m.sin(_f1m.radians(25)))
_t5 = (T1R[0] - 200 * _f1m.cos(_f1m.radians(25)), T1R[1] - 200 * _f1m.sin(_f1m.radians(25)))
f1ineq = GEO('f1ineq', [
    ('line', [('seg', T1L[0], T1L[1], T1R[0], T1R[1], 'ink', 4), ('txt', 300, 290, '9', 'ink', 26)]),
    ('flat', [('seg', T1L[0], 245, 280, 245, 'teal', 5), ('seg', 280, 237, 480, 237, 'orange', 5),
              ('txt', 200, 222, '4', 'teal', 24), ('txt', 380, 214, '5', 'orange', 24)]),
    ('lift', [('dim', 100, 200, 400, 60), ('seg', T1L[0], T1L[1], _t4[0], _t4[1], 'teal', 5), ('seg', T1R[0], T1R[1], _t5[0], _t5[1], 'orange', 5),
              ('txt', _t4[0] - 40, _t4[1] - 4, '4', 'teal', 24), ('txt', _t5[0] + 40, _t5[1] - 4, '5', 'orange', 24),
              ('seg', _t4[0], _t4[1], _t5[0], _t5[1], 'red', 3, True), ('txt', 300, 150, 'a gap', 'red', 24)]),
], vb='80 100 440 210', w=700, col=0, title='Two sides of 4 and 5 cannot close a triangle on a side of 9')
f1in1 = I('f1in1', '$4+5=9$: $\\ $no triangle', size=30, col=1)
f1in2 = IH('f1in2', '$5,\\ 6,\\ 9$: $\\ 5+6=11>9$ ✓', size=30, col=1)
f1in3 = IH('f1in3', '$2,\\ 3,\\ 8$: $\\ 2+3=5<8$ ✗', size=30, col=1)

# ---- slide: the shortest path
H1B, H1C, H1A = (120, 270), (520, 270), (300, 80)
f1walk = GEO('f1walk', [
    ('line', f1_tri(H1B, H1C, H1A) + [('txt', H1B[0], H1B[1] + 30, 'home', 'ink', 24), ('txt', H1C[0], H1C[1] + 30, 'club', 'ink', 24),
                                    ('txt', H1A[0], H1A[1] - 26, 'a stop', 'ink', 24)]),
    ('straight', [('seg', H1B[0], H1B[1] - 8, H1C[0], H1C[1] - 8, 'teal', 7), ('txt', 320, 300, 'straight: shorter', 'teal', 22)]),
    ('stop', [('path', [H1B, H1A, H1C], 'orange', 9), ('txt', 470, 110, 'via the stop: longer', 'orange', 22)]),
], vb='60 40 540 290', w=620, col=0, title='A straight line is the shortest way between two points')
f1walk_t = I('f1walkt', '$BA+AC>BC$', size=32, col=1)

# ---- slide: between the difference and the sum
f1rng = GEO('f1rng', [
    ('line', [('seg', 40, 120, 600, 120, 'ink', 3)] + [('seg', 40 + 40 * k, 112, 40 + 40 * k, 128, 'ink', 2) for k in range(15)] +
             [('txt', 40 + 40 * k, 150, str(k), 'ink', 18) for k in range(0, 15)]),
    ('ends', [('dot', 40 + 40 * 5, 120), ('dot', 40 + 40 * 13, 120), ('txt', 240, 88, '9 − 4', 'red', 22), ('txt', 560, 88, '9 + 4', 'red', 22)]),
    ('band', [('tint', [(240, 112), (560, 112), (560, 128), (240, 128)], 'teal'), ('txt', 400, 88, 'the third side', 'teal', 22)]),
    ('whole', [('dot', 40 + 40 * k, 120) for k in range(6, 13)] + [('txt', 400, 186, '6, 7, 8, 9, 10, 11, 12: seven lengths', 'teal', 22)]),
], vb='20 60 600 140', w=860, col=0, title='The third side is between the difference and the sum')
f1rg1 = IH('f1rg1', '$c<a+b$ $\\quad$ $c+b>a$: $\\ c>a-b$', size=28, col=0)
f1rg2 = IH('f1rg2', 'big $-$ small $<c<$ sum', size=30, col=0)
f1rg3 = I('f1rg3', '$4$ and $9$: $\\ 5<c<13$ $\\quad$ $3$ and $8$: $\\ 5<c<11$', size=28, col=0)
f1rg4 = I('f1rg4', 'Whole numbers: $\\ 2\\times$ the shorter side $-1$', size=28, col=0)

# ---- recap
f1r = [I('f1r%d' % k, t, size=26, col=0) for k, t in enumerate([
    'Median: midpoint $\\quad$ altitude: $90°$ (maybe outside) $\\quad$ bisector: equal angles',
    'Angle sum: $\\ \\alpha+\\beta+\\gamma=180°$',
    'Exterior angle $=$ the two interior angles not next to it',
    'Larger angle $\\leftrightarrow$ longer side opposite it',
    'big $-$ small $<$ a side $<$ sum'])]

video('geo-009', 'lesson', slides=[
    S('Triangles',
      L("Triangles. In this lesson we'll get to know the rules of triangles, the sides, the angles, the connection between "
        "them, and a few special lines that are important to know. Let's start.")),
    # ------------------------------------------------------------------ part 1: the special lines
    S('The median',
      L("The first line is called a median. A median is a segment that joins a vertex of the triangle to the middle of "
        "the side opposite it. Here's a triangle, A B C. The side opposite C is A B, and its middle point is M.",
        show(f1med['line'], "Here's a triangle"), show(f1med['mid'], 'its middle point is M')),
      L("The median goes from C to M, so it splits the side A B into two equal pieces. We mark equal pieces with the same "
        "little line. For example, if A B is ten, then A M is five and M B is five.",
        show(f1med['med'], 'The median goes from C to M'), show(f1med['ticks'], 'We mark equal pieces')),
      L("That's all a median promises, two equal pieces. It doesn't make a right angle with the side, and it doesn't "
        "split the angle at C into two equal angles.", show(f1med['not'], "It doesn't make a right angle")),
      L("Every triangle has three medians, one from each vertex. Here's one from A to the middle of B C, and one from B to "
        "the middle of A C. And look, the three medians meet at one point. There's also a rule about how they divide each "
        "other, two to one, but it isn't needed for the exam. If you know it, fine, and if you don't, that's fine too.",
        show(f1med['three'], 'one from each vertex'), show(f1med['meet'], 'the three medians meet'))),
    S('The altitude',
      L("The second line is the altitude. An altitude is a segment from a vertex to the opposite side, or to its extension, "
        "that makes a ninety degree angle with it. Here, from C, we go down to A B, straight down.",
        show(f1alt['line'], 'The second line is the altitude'), show(f1alt['alt'], 'from C, we go down to A B')),
      L("The little square tells us it's a right angle. Here the triangle is acute, all its angles are smaller than ninety, "
        "so the altitude falls inside the triangle.", show(f1alt['sq'], 'The little square')),
      L("Careful, an altitude doesn't promise the middle. H, where it meets the side, is not the middle of A B here. An "
        "altitude gives a right angle, not equal pieces.", show(f1alt['nomid'], "an altitude doesn't promise the middle"),
),
      L("There are three altitudes too, one from each vertex. From A, and from B. And here too, the three altitudes meet "
        "at one point.", show(f1alt['three'], 'From A, and from B'))),
    S('An altitude outside',
      L("Now an obtuse triangle. The angle at A is bigger than ninety degrees. Let's drop the altitude from C.",
        show(f1out['line'], 'Now an obtuse triangle'), show(f1out['obt'], 'The angle at A is bigger')),
      L("If I try to go down to the side A B itself, I can't make a right angle. The line comes out slanted, and the "
        "altitude must be at ninety degrees. So we continue the side A B beyond A. That's its extension.",
        show(f1out['try'], 'The line comes out slanted'), show(f1out['ext'], 'So we continue the side')),
      L("The altitude from C comes down to the extension, at a right angle. It's outside the triangle, but it's still the "
        "altitude of the triangle. Imagine that this line is the floor. Then this is simply the height of the triangle "
        "above the floor.", show(f1out['alt'], 'The altitude from C comes down'), show(f1out['floor'], 'Imagine that this line is the floor'))),
    S('The angle bisector',
      L("The third special line is the angle bisector. You met it with lines and angles. It splits an angle into two equal "
        "angles. Here it starts at C, splits the angle at C, and goes down to the side opposite it, at D.",
        show(f1bis['line'], 'The third special line'), show(f1bis['bis'], 'Here it starts at C')),
      L("The two halves are equal, so we call both of them alpha. For example, if the angle at C is seventy degrees, each "
        "half is thirty-five.", show(f1bis['halves'], 'The two halves are equal')),
      L("That's all it promises, two equal angles. It doesn't split the side into equal pieces. Look, A D is shorter than "
        "D B here. And it doesn't make a right angle.", show(f1bis['pieces'], 'Look, A D is shorter')),
      L("So these are three different lines. A median gives equal pieces, an altitude gives a right angle, and a bisector "
        "gives equal angles. In special triangles, which we'll meet in a later lesson, they can become one line.",
        show(f1three, 'So these are three different lines'))),
    # ------------------------------------------------------------------ part 2: the angles
    S('The angle sum',
      L("The angles of a triangle add up to a hundred eighty degrees. Alpha plus beta plus gamma equals a hundred eighty. "
        "Most of you know this rule, but have you ever thought about why it's true? Let's prove it quickly.",
        show(f1sum['line'], 'The angles of a triangle'), show(f1sum['abc'], 'Alpha plus beta plus gamma')),
      L("Through the top vertex, C, we draw a line parallel to the side A B.", show(f1sum['par'], 'we draw a line parallel')),
      L("Now we have parallel lines, so we look for the Z. Here's a Z on the left. The angle in its top corner equals "
        "alpha. And here's a Z on the right. The angle in its top corner equals beta.",
        show(f1sum['z1'], "Here's a Z on the left"), show(f1sum['z2'], "And here's a Z on the right")),
      L("Now look at the top. Alpha, gamma and beta sit side by side on one straight line, so together they make a "
        "straight angle, a hundred eighty. So the three angles of the triangle add up to a hundred eighty.",
        show(f1sum['line180'], 'sit side by side on one straight line'), show(f1sum_t, 'So the three angles of the triangle'))),
    S('Using the angle sum',
      L("Let's use it. Two angles are fifty and sixty. Fifty plus sixty is a hundred ten, so the third angle is a hundred "
        "eighty minus a hundred ten, which is seventy.", show(f1ex1, 'Two angles are fifty and sixty')),
      L("Another one. A right triangle has a ninety degree angle and a thirty-five degree angle. Ninety plus thirty-five "
        "is a hundred twenty-five, so the third angle is fifty-five.", show(f1ex2, 'A right triangle')),
      L("And a non-example. Can a triangle have one angle of a hundred degrees and another of ninety-five degrees? No. "
        "Together they're already more than a hundred eighty. So a triangle has at most one obtuse angle, or one right angle.",
        show(f1ex3, 'And a non-example'))),
    S('The exterior angle',
      L("Now the exterior angle. First, what is it? We continue one side of the triangle, here A C beyond C. The angle "
        "between this extension and the side C B is an exterior angle. It's outside the triangle. Let's call it delta.",
        show(f1ext['line'], 'Now the exterior angle'), show(f1ext['ext'], 'We continue one side'),
        show(f1ext['delta'], "Let's call it delta")),
      L("The rule says that an exterior angle equals the sum of the two angles inside the triangle that are not next to "
        "it. Gamma is next to delta, so the rule is about alpha and beta. Delta equals alpha plus beta.",
        show(f1ext['gamma'], 'Gamma is next to delta'), show(f1ext['ab'], 'so the rule is about alpha and beta')),
      L("Why? Gamma and delta sit side by side on a straight line, so gamma plus delta is a hundred eighty. And the angle "
        "sum says alpha plus beta plus gamma is also a hundred eighty. Both sums have gamma, and both make a hundred "
        "eighty, so what's left must be equal. Delta equals alpha plus beta.",
        show(f1ext_t1, 'Gamma and delta sit side by side'), show(f1ext_t2, 'And the angle sum says'),
        show(f1ext_t3, 'Delta equals alpha plus beta.'))),
    S('Two ways',
      L("This rule isn't used very often on the exam, and you don't really need it. We can always find the angle next to "
        "the exterior angle, and use the angle sum. But if you know it, it can save you time. For example, the two angles "
        "inside are forty-seven and sixty-eight.", show(f1rt['line'], "This rule isn't used very often"),
        show(f1rt['given'], 'the two angles inside are')),
      L("With the rule, it's one step. Forty-seven plus sixty-eight is a hundred fifteen. That's the exterior angle.",
        show(f1rt['ex'], 'With the rule')),
      L("The long way gives the same thing. The third angle is a hundred eighty minus forty-seven minus sixty-eight, which "
        "is sixty-five. And the exterior angle completes sixty-five to a hundred eighty, so it's a hundred fifteen again.",
        show(f1rt['in'], 'The third angle is')),
      L("One more. If the two angles inside are thirty and eighty, the exterior angle next to the third angle is thirty "
        "plus eighty, a hundred ten.", show(f1rt['more'], 'thirty plus eighty'))),
    # ------------------------------------------------------------------ part 3: the sides
    S('Sides and angles',
      L("In every triangle, the largest side lies opposite the largest angle, and the smallest side lies opposite the "
        "smallest angle. Here the angles are sixty at A, forty at B and eighty at C.",
        show(f1sa['line'], 'In every triangle'), show(f1sa['angs'], 'Here the angles are')),
      L("Forty is the smallest angle. The side opposite B is the side that doesn't touch B, that's A C. So A C is the "
        "shortest side. Eighty is the largest angle, so the side opposite C, A B, is the longest. And sixty is in the "
        "middle, so its side, B C, is in the middle.", show(f1sa['small'], 'So A C is the'),
        show(f1sa['big'], 'Eighty is the largest angle'), show(f1sa['mid'], 'And sixty is in the')),
      L("It works both ways. Opposite the longest side is the largest angle. So in a right triangle, the right angle is the "
        "largest angle, and the side opposite it is the longest side.", show(f1sa_t, 'It works both ways')),
      L("And it makes sense. Imagine two sides of a fixed length and the angle between them. When the angle opens wider, "
        "the side opposite it gets longer. When it closes, that side gets shorter.", show(f1open['line'], 'Imagine two sides'),
        show(f1open['wide'], 'When the angle opens wider'))),
    S('Two sides and the third',
      L("Here's another rule about sides. Any two sides of a triangle together are longer than the third side. Let's see "
        "what that means. Say one side is nine.", show(f1ineq['line'], 'Say one side is nine')),
      L("And the other two sides are four and five, exactly nine together. Lying flat, they cover the nine exactly.",
        show(f1ineq['flat'], 'Lying flat')),
      L("Now let's try to close a triangle. I lift the four up on one side and the five on the other. As soon as they "
        "rise, there's a gap between them. They don't meet. To close a triangle, one of them, or both, would have to be "
        "longer. So the two sides together must be more than nine, not just equal to it.",
        show(f1ineq['lift'], 'As soon as they rise'), show(f1in1, 'They don\'t meet')),
      L("For example, five, six and nine can be a triangle, because five plus six is eleven, more than nine. But two, "
        "three and eight can't, because two plus three is only five, less than eight.",
        show(f1in2, 'five, six and nine'), show(f1in3, 'But two, three and eight'))),
    S('The shortest way',
      L("There's another way to see it. Say this is my home, and this is the sports club.",
        show(f1walk['line'], 'Say this is my home')),
      L("Let's send two friends from home to the club, each on a different route. The first walks in a straight line. "
        "The second stops somewhere on the way, and then goes on to the club.", show(f1walk['straight'], 'The first walks'),
        show(f1walk['stop'], 'The second stops')),
      L("Who arrives first? The one who walked in a straight line, because his road is shorter. The one who stopped walked "
        "more. A straight line is always the shortest way between two points, so two sides together are longer than the "
        "third.", show(f1walk_t, 'so two sides together'))),
    S('Between the difference and the sum',
      L("Now let's extend this rule. Side c is less than a plus b, because two sides together are longer than the third. "
        "But c and b are also two sides, so together they're longer than a. Move b to the other side, and c is more than "
        "a minus b.", show(f1rg1, 'Side c is less than')),
      L("Together: a side of a triangle is less than the sum of the other two sides, and more than their difference. The "
        "difference is always the big one minus the small one, and it can't be equal to either end.",
        show(f1rg2, 'Together')),
      L("For example, two sides are four and nine. The third side is more than nine minus four, five, and less than nine "
        "plus four, thirteen.", show(f1rng['line'], 'two sides are four and nine'), show(f1rng['ends'], 'nine minus four'),
        show(f1rng['band'], 'and less than nine')),
      L("If the third side is a whole number, it can be six, seven, and so on up to twelve. That's seven lengths. A quick "
        "count is twice the shorter side, minus one. Twice four is eight, minus one is seven. With sides three and eight, "
        "the third side is between five and eleven, so six to ten, five lengths, and twice three minus one is five too.",
        show(f1rng['whole'], 'it can be six, seven'), show(f1rg4, 'A quick count'), show(f1rg3, 'With sides three and eight'))),
    S('Recap',
      L("So, a median goes to the middle, an altitude makes a right angle, and a bisector splits the angle. The angles add "
        "up to a hundred eighty, and an exterior angle equals the two angles inside that are not next to it.",
        show(f1r[0], 'a median goes to the middle'), show(f1r[1], 'The angles add'), show(f1r[2], 'an exterior angle')),
      L("The largest side is opposite the largest angle, and a side is between the difference and the sum of the other "
        "two. The most important rule to take from here is the angle sum. If you remember the exterior angle too, it can "
        "save you a few seconds. [pause] Okay. I'll see you in the next video.",
        show(f1r[3], 'The largest side'), show(f1r[4], 'a side is between'))),
])

CAMERA_SPLIT = ('geo-009', 'Triangles', [
    (1, None),
    (5, "Let's continue with triangles, this time with their angles."),
    (9, "Let's continue with triangles, this time with their sides."),
])

# =================================================================================================================
# Topic 31, fragment f2: the triangle-basics questions (g010, g011, g012), the lesson "Special Triangles" (geo-013) and its
# questions (g014, g015). Written 2026-10-14. Question videos: the question figure on the left (FIG_LEFT), our colour copy
# (same coordinates and labels) on the right, built at the words; values written on the figure when found (Rule V3).
# Colours: the given angles ink, the angle being found teal, an outside / supplementary angle orange, wrong red.
# =================================================================================================================
CARRY31.update({'solve-geo31-g012': {1: ['$7<x<19$']}})
FIG_LEFT.update({'solve-geo31-g010', 'solve-geo31-g011', 'solve-geo31-g012', 'solve-geo31-g014', 'solve-geo31-g015'})


def f2_tri(P, Q, R, c='ink', w=3):
    return [('seg', P[0], P[1], Q[0], Q[1], c, w), ('seg', Q[0], Q[1], R[0], R[1], c, w), ('seg', R[0], R[1], P[0], P[1], c, w)]


def f2_lab(*pts):
    return [('txt', x, y, t, 'ink', 24, True) for x, y, t in pts]


# ------------------------------------------------------------------------------------------------ geo31-g010 (Hebrew: the first sample question)
# Hebrew (geo 513-519): complete the vertical angle at A, then the angle sum: alpha + 3 alpha + 2 alpha = 180 -> 30. The
# course's numbers: 3x (vertical), 4x, 5x -> 15. One method. V3: the two crossing lines at A traced, the vertical angle
# copied inside; the triangle tinted for the sum; the angle values written when found.
f2_A0, f2_B0, f2_C0 = (165.0, 270.0), (485.0, 270.0), (367.872, 67.128)
f2_g10 = GEO('f2g10', [
    ('line', f2_tri(f2_A0, f2_B0, f2_C0) + [('seg', 103, 270, 165, 270), ('seg', 121.159, 313.841, 165, 270)]
             + f2_lab((181, 292, 'A'), (505, 290, 'B'), (367.9, 45, 'C'))
             + [('arc', 485, 270, 32, 120, 180, 'ink', '4x', 56), ('arc', 367.872, 67.128, 30, 225, 300, 'ink', '5x', 54),
                ('arc', 165, 270, 34, 180, 225, 'ink', '3x', 58)]),
    ('cross', [('path', [(103, 270), (330, 270)], 'teal', 7), ('path', [(121.159, 313.841), (262, 173)], 'teal', 7)]),
    ('vert', [('arc', 165, 270, 40, 0, 45, 'small', '3x', 64)]),
    ('sum', [('tint', [f2_A0, f2_B0, f2_C0], 'teal')]),
    ('e1', [('txt', 310, 340, '3x + 4x + 5x = 180°', 'ink', 26)]),
    ('e2', [('txt', 310, 374, '12x = 180°,   x = 15°', 'ink', 26)]),
    ('e3', [('txt', 310, 408, '45° + 60° + 75° = 180°  ✓', 'small', 26)]),
], vb='95 25 430 400', w=430, title='Triangle ABC with the vertical angle at A')
video('solve-geo31-g010', 'solution', qid='geo31-g010', slides=[
    S('Vertical angle, then angle sum',
      L("In triangle A B C, the marked angle outside the triangle and the interior angle at A are vertical angles. Based on "
        "this information and the information in the figure, what is the value of x?", pt('stem', 'In triangle A B C', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("We need x. Inside the triangle we know two angles, four x at B and five x at C. The third angle, at A, is "
        "missing, but there's a three x right next to it, outside the triangle. [short pause] So first we'll find the "
        "angle at A, and then we'll use the angle sum of a triangle.", pt('fig: 4x', 'four x at B'), pt('fig: 3x', "there's a three x")),
      L("[short pause] Look at point A. Two straight lines cross there, the line of side A B, and the line of side A C, "
        "which goes on past A. When two lines cross, the angles facing each other are vertical angles, and vertical angles "
        "are equal. So the angle inside the triangle at A is also three x.", show(f2_g10['line'], 'Look at point A'),
        show(f2_g10['cross'], 'Two straight lines cross there'), show(f2_g10['vert'], 'So the angle inside the triangle')),
      L("Now the angle sum. The three angles of a triangle always add up to one hundred eighty. So three x, plus four x, "
        "plus five x, equals one hundred eighty.", show(f2_g10['sum'], 'The three angles of a triangle'),
        show(f2_g10['e1'], 'So three x, plus four x')),
      L("Three x plus four x plus five x is twelve x. Twelve x equals one hundred eighty, so x is one hundred eighty "
        "divided by twelve. Twelve times fifteen is one hundred eighty, so x is fifteen. Choice number two is our answer.",
        show(f2_g10['e2'], 'Twelve x equals'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Let's check it. Three x is forty-five, four x is sixty, and five x is seventy-five. Forty-five plus sixty is a "
        "hundred five, and plus seventy-five is a hundred eighty. And careful, forty-five, choice number one, is three x, "
        "the angle at A, not x. [pause] Okay. I'll see you in the next question.", show(f2_g10['e3'], 'Forty-five plus sixty'), mk('cross', 'choice 1', 'forty-five, choice number one'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g011 (Hebrew: the second sample question)
# Hebrew (geo 521-541): end with ONE unknown; m is next to the inside angle (180 - beta); n is an exterior angle = the two
# inside angles not next to it (2 beta); 2 alpha + gamma = 360. Course question: m + n/2, the equal angles k -> 180.
# Course addition kept: plugging in k = 60 (explained here on its own: topic 51 comes later). V3: m with its neighbour k on
# the straight line; n with the two inside k's tinted; a second copy with the numbers.
f2_A1, f2_B1, f2_C1 = (211.727, 286.628), (428.273, 286.628), (390.670, 73.372)
f2_g11base = f2_tri(f2_A1, f2_B1, f2_C1) + [('seg', 164.481, 286.628, 211.727, 286.628), ('seg', 428.273, 286.628, 479.457, 286.628)] \
    + f2_lab((196, 308, 'A'), (444, 308, 'B'), (390.7, 51, 'C'))
f2_g11 = GEO('f2g11', [
    ('line', f2_g11base + [('arc', 211.727, 286.628, 24, 0, 50, 'ink', 'k', 42), ('arc', 390.67, 73.372, 24, 230, 280, 'ink', 'k', 44),
                           ('arc', 211.727, 286.628, 30, 50, 180, 'ink', 'm', 52), ('arc', 428.273, 286.628, 30, 0, 100, 'ink', 'n', 52)]),
    ('m', [('path', [(164.5, 286.6), (330, 286.6)], 'teal', 7), ('wedge', 211.727, 286.628, 30, 50, 180, 'orange'),
           ('wedge', 211.727, 286.628, 24, 0, 50, 'teal')]),
    ('n', [('wedge', 428.273, 286.628, 30, 0, 100, 'orange'), ('wedge', 390.67, 73.372, 24, 230, 280, 'teal'),
           ('wedge', 211.727, 286.628, 24, 0, 50, 'teal')]),
    ('e1', [('txt', 322, 345, 'm = 180° − k', 'ink', 24)]),
    ('e2', [('txt', 322, 385, 'n = k + k = 2k', 'ink', 24)]),
    ('e3', [('txt', 322, 425, 'm + n/2 = (180° − k) + k = 180°', 'ink', 22)]),
], vb='150 25 345 420', w=370, title='Triangle ABC with the angles k, m and n')
f2_g11p = GEO('f2g11p', [
    ('line', f2_g11base + [('arc', 211.727, 286.628, 24, 0, 50, 'small', '60°', 46), ('arc', 390.67, 73.372, 24, 230, 280, 'small', '60°', 48),
                           ('arc', 428.273, 286.628, 22, 100, 180, 'small', '60°', 42)]),
    ('mv', [('arc', 211.727, 286.628, 30, 50, 180, 'orange', 'm = 120°', 64)]),
    ('nv', [('arc', 428.273, 286.628, 30, 0, 100, 'orange', 'n = 120°', 66)]),
    ('e1', [('txt', 322, 350, 'm = 120°,   n = 120°', 'ink', 24)]),
    ('e2', [('txt', 322, 390, 'm + n/2 = 120° + 60° = 180°', 'ink', 24)]),
], vb='120 25 405 390', w=400, title='Triangle ABC with k = 60 degrees')
video('solve-geo31-g011', 'solution', qid='geo31-g011', slides=[
    SM('Method 1 · The angle rules', 'Down to one letter',
      L("In the accompanying figure, the angles at A and C are equal. What is the value of m plus n over two?",
        pt('stem', 'In the accompanying figure', 'hl', 6.0), voice='calm', pause=0.5),
      L("The figure has three letters, k, m and n, but the answer has to be one number. So we'll write m and n with the "
        "same letter, k, and hope that k cancels. [short pause] We'll solve it two ways, with the angle rules, and then by "
        "plugging in a number for k.", pt('fig: k', 'three letters')),
      L("[short pause] Start with m. m is outside the triangle at A, right next to the angle k inside. Together they make "
        "the straight line, so m and k add up to one hundred eighty. So m is one hundred eighty minus k.",
        show(f2_g11['line'], 'Start with m'), show(f2_g11['m'], 'Together they make'), show(f2_g11['e1'], 'So m is one hundred eighty')),
      L("Now n. n is outside the triangle at B, between side B C and the line of side A B that goes on past B. That's an "
        "exterior angle, and an exterior angle equals the two inside angles that are not next to it. Here they are the "
        "angles at A and at C, k and k. So n is k plus k, which is two k.", pt('fig: n', 'Now n'),
        show(f2_g11['n'], 'an exterior angle equals'), show(f2_g11['e2'], 'So n is k plus k')),
      L("Now the expression, m plus half of n. m is one hundred eighty minus k. Half of n is half of two k, which is k. So "
        "we get one hundred eighty minus k, plus k. Minus k and plus k cancel, and we're left with one hundred eighty. "
        "Choice number three is our answer.", show(f2_g11['e3'], 'Half of n is half'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Plugging in a number', 'Plugging in a number',
      L("[pause] Another way, plugging in a number. The answer is one number, so it comes out the same for every k that "
        "fits the figure. That means we're allowed to choose any k we like, and work with numbers instead of letters. "
        "Let's take an easy one, k is sixty.", show(f2_g11p['line'], "Let's take an easy one")),
      L("Then the angles at A and C are sixty. The angle at B is one hundred eighty minus one hundred twenty, which is "
        "sixty too. m is next to the sixty at A, so m is one hundred eighty minus sixty, which is one hundred twenty. n is "
        "the outside angle at B, so n is sixty plus sixty, which is one hundred twenty too.",
        show(f2_g11p['mv'], 'so m is one hundred eighty minus sixty'), show(f2_g11p['nv'], 'so n is sixty plus sixty'),
        show(f2_g11p['e1'], 'one hundred twenty too')),
      L("So m plus half of n is one hundred twenty plus sixty, which is one hundred eighty. Choice number three again. "
        "[pause] Okay. I'll see you in the next question.", show(f2_g11p['e2'], 'one hundred twenty plus sixty'),
        mk('tick', 'choice 3', 'Choice number three again'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g012 (Hebrew: the third sample question)
# Hebrew (geo 543-558): a side is between the difference and the sum of the other two (5 and 9 -> between 4 and 14, not
# equal to 4). Course numbers 6 and 13 -> between 7 and 19. Then her closing of the basics lesson (the angle sum is the
# rule to take; the exterior angle saves seconds). V3: x traced on the copy; the allowed lengths as a band on a number
# line, the choices placed on it and the ones outside crossed.
f2_A2, f2_B2, f2_C2 = (165.0, 290.0), (495.0, 290.0), (148.636, 110.745)
f2_g12 = GEO('f2g12', [
    ('line', f2_tri(f2_A2, f2_B2, f2_C2) + f2_lab((147, 310, 'A'), (513, 310, 'B'), (148.6, 88, 'C'))
             + [('txt', 335, 186, '13', 'ink', 24), ('txt', 132, 202, '6', 'ink', 24)]),
    ('x', [('path', [f2_A2, f2_B2], 'red', 8), ('txt', 330, 316, 'x', 'red', 26, True)]),
    ('e1', [('txt', 325, 356, '13 − 6 < x < 13 + 6', 'ink', 26)]),
    ('e2', [('txt', 325, 394, '7 < x < 19', 'ink', 26)]),
], vb='110 70 430 340', w=400, title='Triangle ABC: sides 6, 13 and x')
f2_X = lambda v: 50 + (v - 4) * 28.0          # the number line: 4 .. 23 over 50 .. 582
f2_z12 = GEO('f2z12', [
    ('line', [('seg', 30, 110, 600, 110, 'ink', 3)]),
    ('band', [('tint', [(f2_X(7), 100), (f2_X(19), 100), (f2_X(19), 120), (f2_X(7), 120)], 'teal'),
              ('txt', f2_X(13), 70, '7 < x < 19', 'small', 26)]),
    ('ch', [('dot', f2_X(v), 110) for v in (7, 11, 19, 21)] + [('txt', f2_X(v), 150, str(v), 'ink', 26) for v in (7, 11, 19, 21)]),
    ('cr', [('txt', f2_X(v), 185, '✗', 'red', 30) for v in (7, 19, 21)] + [('txt', f2_X(11), 185, '✓', 'small', 30)]),
], vb='20 40 600 170', w=560, title='x between 7 and 19')
video('solve-geo31-g012', 'solution', qid='geo31-g012', slides=[
    S('Between the difference and the sum',
      L("In triangle A B C, A C is six centimeters and B C is thirteen centimeters. Which of the following could be the "
        "length of A B, in centimeters?", pt('stem', 'In triangle A B C', 'hl', 7.0), voice='calm', pause=0.5),
      L("A B is the side marked x in the figure. We know the other two sides, six and thirteen, and we need a length the "
        "third side could have. [short pause] We'll use the rule about the three sides of a triangle.",
        pt('fig: x', 'A B is the side marked x')),
      L("[short pause] Remember the rule. A side of a triangle is shorter than the sum of the other two sides, and "
        "longer than their difference. If x were as long as six plus thirteen, the two other sides would lie flat on it, "
        "and they couldn't close a triangle.", show(f2_g12['line'], 'Remember the rule'), show(f2_g12['x'], 'If x were as long')),
      L("So x is less than thirteen plus six, which is nineteen, and more than thirteen minus six, which is seven. x is "
        "between seven and nineteen.", show(f2_g12['e1'], 'So x is less than'), show(f2_g12['e2'], 'x is between seven'))),
    S('Between the difference and the sum',
      L("Let's put that on a number line. x can be anywhere between seven and nineteen, but not on the edges.",
        show(f2_z12['line'], "Let's put that"), show(f2_z12['band'], 'x can be anywhere')),
      L("Now the choices. Twenty-one is more than nineteen, so it's too long. Seven and nineteen are the edges "
        "themselves, and x has to be strictly between them, not equal to them. So choice numbers one, two and four are "
        "out. Eleven is between seven and nineteen, so choice number three is our answer.", show(f2_z12['ch'], 'Now the choices'),
        show(f2_z12['cr'], 'So choice numbers one, two'), mk('cross', 'choice 2', 'Twenty-one is more'),
        mk('cross', 'choice 1', 'Seven and nineteen are the edges'), mk('cross', 'choice 4', 'and four are out'),
        mk('tick', 'choice 3', 'choice number three is our answer')),
      L("That's it for the basic rules of triangles. The rule to take with you is the angle sum, one hundred eighty, and "
        "the exterior angle rule can save you a few seconds. [pause] Okay. I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ geo-013 (lesson: Special Triangles)
# Hebrew (geo 558-603): the isosceles triangle (legs, base, base angles equal, the vertex angle; the median to the base is
# the altitude and the bisector: a symmetry line; fold the paper: two identical halves, so no rules to memorize - "we're
# not writing a proof"); the equilateral triangle (all sides, 60 each because 180 / 3; isosceles from every direction);
# the right triangle (legs, the hypotenuse opposite the 90, the longest side); the median to the hypotenuse = half of it,
# two isosceles triangles (rare on the exam). Kept from the English lesson: the backwards rule, the 44 -> 68 example, the
# "find the square, look across" trick. Added examples (2-3 per idea): 70 -> 40, a non-example 50/60/70, the wrong median,
# the three symmetry lines of the equilateral, a second right triangle turned, median 10 -> 5.
# V3: one generic figure per shape, built part by part; marks (ticks, equal arcs, squares) at the words; the symmetry line
# drawn after its two ends are shown; the fold = the same tint on both halves; the median's two triangles tinted in turn.
f2_P, f2_L, f2_R = (320.0, 60.0), (219.0, 300.0), (421.0, 300.0)
f2_M = (320.0, 300.0)
f2_isoT = f2_tri(f2_P, f2_L, f2_R) + f2_lab((320, 36, 'A'), (200, 318, 'B'), (440, 318, 'C'))
f2_bl = gdir(f2_L[0], f2_L[1], f2_P[0], f2_P[1])            # 67.2 degrees: the base angle as drawn
f2_iso = GEO('f2iso', [
    ('line', f2_isoT),
    ('legs', [('tick', f2_P[0], f2_P[1], f2_L[0], f2_L[1]), ('tick', f2_P[0], f2_P[1], f2_R[0], f2_R[1]),
              ('txt', 240, 170, 'leg', 'small', 22), ('txt', 400, 170, 'leg', 'small', 22)]),
    ('base', [('path', [f2_L, f2_R], 'orange', 7), ('txt', 320, 330, 'base', 'orange', 22)]),
    ('bang', [('arc', f2_L[0], f2_L[1], 30, 0, f2_bl, 'small'), ('arc', f2_R[0], f2_R[1], 30, 180 - f2_bl, 180, 'small')]),
    ('vang', [('arc', f2_P[0], f2_P[1], 30, 180 + f2_bl, 360 - f2_bl, 'orange')]),
    ('ex1', [('txt', 320, 118, '44°', 'orange', 22), ('txt', 268, 284, '68°', 'small', 22), ('txt', 372, 284, '68°', 'small', 22)]),
], vb='150 20 340 320', w=520, col=1, title='An isosceles triangle')
f2_k13a = IH('f2k13a', '$180°-44°=136°$, $\\ 136°\\div2=68°$', size=30)
f2_k13b = IH('f2k13b', '$70°+70°=140°$, $\\ 180°-140°=40°$', size=30)
f2_k13c = I('f2k13c', 'Two equal angles $\\Leftrightarrow$ two equal sides', size=30)
f2_k13d = I('f2k13d', '$50°,\\ 60°,\\ 70°$: $\\ $no equal sides ✗', size=30)
f2_sym = GEO('f2sym', [
    ('line', f2_isoT + [('tick', f2_P[0], f2_P[1], f2_L[0], f2_L[1]), ('tick', f2_P[0], f2_P[1], f2_R[0], f2_R[1])]),
    ('ends', [('dot', f2_P[0], f2_P[1]), ('dot', f2_M[0], f2_M[1])]),
    ('ax', [('seg', f2_P[0], f2_P[1], f2_M[0], f2_M[1], 'teal', 3.5, True)]),
    ('half', [('tick', f2_L[0], f2_L[1], f2_M[0], f2_M[1], 2), ('tick', f2_M[0], f2_M[1], f2_R[0], f2_R[1], 2)]),
    ('perp', [('right', f2_M[0], f2_M[1], 0, 90, 16), ('right', f2_M[0], f2_M[1], 90, 180, 16)]),
    ('bis', [('arc', f2_P[0], f2_P[1], 44, 180 + f2_bl, 270, 'small'), ('arc', f2_P[0], f2_P[1], 52, 270, 360 - f2_bl, 'small')]),
    ('bad', [('seg', f2_L[0], f2_L[1], (f2_P[0] + f2_R[0]) / 2, (f2_P[1] + f2_R[1]) / 2, 'red', 3, True),
             ('txt', 300, 210, '✗', 'red', 28)]),
], vb='150 20 340 320', w=560, col=0, title='The symmetry line of an isosceles triangle')
f2_k13e = I('f2k13e', 'To the base: $\\ $median $=$ altitude $=$ bisector', size=30)
f2_fold = GEO('f2fold', [
    ('line', f2_isoT + [('seg', f2_P[0], f2_P[1], f2_M[0], f2_M[1], 'teal', 3.5, True)]),
    ('left', [('tint', [f2_P, f2_L, f2_M], 'teal')]),
    ('right', [('tint', [f2_P, f2_R, f2_M], 'teal'), ('txt', 320, 345, 'right side = left side', 'small', 22)]),
], vb='150 20 340 340', w=560, col=0, title='Fold along the symmetry line')
f2_eq = GEO('f2eq', [
    ('line', f2_tri((320, 70), (190, 295.2), (450, 295.2)) + f2_lab((320, 46, 'A'), (172, 314, 'B'), (468, 314, 'C'))),
    ('sides', [('tick', 320, 70, 190, 295.2), ('tick', 320, 70, 450, 295.2), ('tick', 190, 295.2, 450, 295.2)]),
    ('ang', [('arc', 190, 295.2, 30, 0, 60, 'small'), ('arc', 450, 295.2, 30, 120, 180, 'small'), ('arc', 320, 70, 30, 240, 300, 'small'),
             ('txt', 250, 281, '60°', 'small', 20), ('txt', 390, 281, '60°', 'small', 20), ('txt', 300, 128, '60°', 'small', 20)]),
    ('calc', [('txt', 320, 340, '180° ÷ 3 = 60°', 'small', 28)]),
    ('s1', [('seg', 320, 70, 320, 295.2, 'teal', 3, True)]),
    ('s2', [('seg', 190, 295.2, 385, 182.6, 'orange', 3, True)]),
    ('s3', [('seg', 450, 295.2, 255, 182.6, 'orange', 3, True)]),
], vb='150 30 340 330', w=560, col=0, title='An equilateral triangle')
f2_rt = GEO('f2rt', [
    ('line', f2_tri((80, 290), (80, 90), (330, 290)) + f2_tri((470, 80), (390, 270), (610, 210))
             + [('right', 80, 290, 0, 90, 18)]),
    ('legs', [('path', [(80, 90), (80, 290), (330, 290)], 'teal', 7), ('txt', 58, 190, 'leg', 'small', 22),
              ('txt', 205, 316, 'leg', 'small', 22)]),
    ('hyp', [('path', [(80, 90), (330, 290)], 'orange', 7), ('txt', 290, 165, 'hypotenuse', 'orange', 22)]),
    ('long', [('txt', 330, 350, 'The hypotenuse is the longest side', 'orange', 24)]),
    ('sq2', [('right', 470, 80, gdir(470, 80, 610, 210), gdir(470, 80, 390, 270), 18)]),
    ('hyp2', [('path', [(390, 270), (610, 210)], 'orange', 7), ('txt', 330, 390, 'Find the square, look across: the hypotenuse', 'ink', 22)]),
], vb='30 60 600 345', w=900, col=0, title='Right triangles: two legs and the hypotenuse')
f2_MH = ((90 + 470) / 2.0, (80 + 290) / 2.0)
f2_med = GEO('f2med', [
    ('line', f2_tri((90, 290), (90, 80), (470, 290)) + [('right', 90, 290, 0, 90, 18)]
             + f2_lab((68, 306, 'C'), (68, 72, 'A'), (492, 306, 'B'))),
    ('ends', [('dot', 90, 290), ('dot', f2_MH[0], f2_MH[1], 'M', 6, -24)]),
    ('md', [('seg', 90, 290, f2_MH[0], f2_MH[1], 'teal', 3.5, True)]),
    ('eq', [('tick', 90, 80, f2_MH[0], f2_MH[1]), ('tick', f2_MH[0], f2_MH[1], 470, 290), ('tick', 90, 290, f2_MH[0], f2_MH[1])]),
    ('ex', [('txt', 280, 350, 'half the hypotenuse:   14 → 7,   10 → 5', 'ink', 22)]),
    ('t1', [('tint', [(90, 80), f2_MH, (90, 290)], 'teal')]),
    ('t2', [('tint', [(90, 290), f2_MH, (470, 290)], 'orange')]),
], vb='40 50 470 320', w=760, col=0, title='The median to the hypotenuse')
video('geo-013', 'lesson', slides=[
    S('Special Triangles',
      L("In the last lesson we learned the general triangle, the angle sum of one hundred eighty and so on. Now, special "
        "triangles. You probably remember them a little from school, the isosceles triangle, the equilateral triangle "
        "and the right triangle. Let's get to know them.")),
    S('The isosceles triangle',
      L("First, the isosceles triangle. An isosceles triangle has two equal sides. We mark equal sides with the same "
        "small line. These two equal sides are called the legs, and the third side is called the base.",
        show(f2_iso['line'], 'An isosceles triangle has'), show(f2_iso['legs'], 'We mark equal sides'), show(f2_iso['base'], 'the third side')),
      L("The two angles that sit on the base, between the base and each leg, are equal. They're called the base angles. "
        "The angle left at the top is called the vertex angle.", show(f2_iso['bang'], 'The two angles that sit on the base'),
        show(f2_iso['vang'], 'The angle left at the top')),
      L("For example, if the vertex angle is forty-four degrees, the two base angles share the rest. One hundred eighty "
        "minus forty-four is one hundred thirty-six, and half of that is sixty-eight. So each base angle is sixty-eight.",
        show(f2_iso['ex1'], 'For example, if the vertex angle'), show(f2_k13a, 'One hundred eighty minus forty-four')),
      L("Another example. If each base angle is seventy, together they make one hundred forty. So the vertex angle is "
        "one hundred eighty minus one hundred forty, which is forty.", show(f2_k13b, 'Another example')),
      L("And it works backwards too. If two angles of a triangle are equal, the sides opposite them are equal, so the "
        "triangle is isosceles. But a triangle with angles fifty, sixty and seventy has no two equal angles, so it has no "
        "two equal sides.", show(f2_k13c, 'And it works backwards too'), show(f2_k13d, 'But a triangle with angles'))),
    S('The symmetry line',
      L("Now a special line in the isosceles triangle. It goes from the vertex angle, at the top, down to the middle of "
        "the base.", show(f2_sym['line'], 'Now a special line'), show(f2_sym['ends'], 'It goes from the vertex angle'),
        show(f2_sym['ax'], 'down to the middle of the base')),
      L("This one line does three jobs. It cuts the base into two equal halves, so it's a median. It's perpendicular to "
        "the base, so it's the altitude. And it cuts the vertex angle into two equal halves, so it's also the angle "
        "bisector.", show(f2_sym['half'], 'It cuts the base into two equal'), show(f2_sym['perp'], "It's perpendicular"),
        show(f2_sym['bis'], 'And it cuts the vertex angle')),
      L("Only this line does all three. A line from a corner of the base to the middle of a leg is a median too, but it "
        "isn't perpendicular, and it doesn't cut the angle in half.", show(f2_sym['bad'], 'A line from a corner of the base'),
        show(f2_k13e, "doesn't cut the angle in half"))),
    S('Fold it',
      L("Here's the easy way to remember all of this. Imagine the triangle is a piece of paper, and you fold it along "
        "the dashed line. The left half lands exactly on the right half. They're two identical triangles, mirror images "
        "of each other.", show(f2_fold['line'], 'Imagine the triangle'), show(f2_fold['left'], 'The left half'),
        show(f2_fold['right'], 'lands exactly on the right half')),
      L("So everything on the right equals the left. The legs are equal, the base angles are equal, the two halves of "
        "the base are equal, and the two angles at the middle of the base are equal. Together they make one hundred "
        "eighty, so each one is ninety."),
      L("So instead of memorizing all the rules of the isosceles triangle, remember one thing. We're not writing a "
        "formal proof here. An isosceles triangle is symmetric. Draw the symmetry line, and everything on the right "
        "equals the left.", pt('f2fold_line', 'An isosceles triangle is symmetric'))),
    S('The equilateral triangle',
      L("The next one is the equilateral triangle. Just like its name, all three sides are equal.",
        show(f2_eq['line'], 'The next one'), show(f2_eq['sides'], 'all three sides are equal')),
      L("In an equilateral triangle, all the angles are sixty degrees. Why? The three angles add up to one hundred "
        "eighty, and they're all equal, so each one is one hundred eighty divided by three, which is sixty.",
        show(f2_eq['ang'], 'all the angles are sixty'), show(f2_eq['calc'], 'one hundred eighty divided by three')),
      L("An equilateral triangle is like an isosceles triangle, only from every direction. Here's the symmetry line from "
        "the top. But we can turn the triangle, and draw the same line from this corner, and from this one too. So "
        "everything we said about the isosceles triangle is true here from all three directions.",
        show(f2_eq['s1'], "Here's the symmetry line"), show(f2_eq['s2'], 'from this corner'), show(f2_eq['s3'], 'and from this one too'))),
    S('The right triangle',
      L("Now the right triangle. It has one right angle, so two of its sides are perpendicular to each other. These two "
        "sides are called the legs.", show(f2_rt['line'], 'Now the right triangle'), show(f2_rt['legs'], 'These two sides are called')),
      L("The third side, across from the right angle, is called the hypotenuse. It's the longest side, longer than each "
        "leg, because it's across from the biggest angle.", show(f2_rt['hyp'], 'The third side'), show(f2_rt['long'], "It's the longest side")),
      L("Here's a little trick. Find the square mark of the right angle first, and then look straight across from it. "
        "That's the hypotenuse, however the triangle is turned. In this second triangle, the square is at the top, so the "
        "hypotenuse is the bottom side.", show(f2_rt['sq2'], 'Find the square mark'),
        show(f2_rt['hyp2'], 'so the hypotenuse is the bottom side'))),
    S('The median to the hypotenuse',
      L("One more rule about the right triangle. It's rare on the exam, but let's learn it anyway. Take the right-angle "
        "corner and the middle of the hypotenuse, and draw the median between them.", show(f2_med['line'], 'One more rule'),
        show(f2_med['ends'], 'Take the right-angle'), show(f2_med['md'], 'draw the median')),
      L("This median is equal to half of the hypotenuse. So the median and the two halves of the hypotenuse are all the "
        "same length. If the hypotenuse is fourteen, the median is seven. If the hypotenuse is ten, the median is five.",
        show(f2_med['eq'], 'are all the same length'), show(f2_med['ex'], 'If the hypotenuse is fourteen')),
      L("And look what we get. The median makes two isosceles triangles, this one and this one, because each has two "
        "equal sides. Now let's see some sample questions. [pause] Okay. I'll see you in the next video.",
        show(f2_med['t1'], 'this one and'), show(f2_med['t2'], 'and this one, because'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g014 (Hebrew: the special-triangles sample question 1)
# Hebrew (geo 607-618): all angles 60 -> the other part is 30 too -> AD bisects the angle -> in an equilateral triangle a
# bisector is also perpendicular and a median -> BD = DC = 5, side 10. Course numbers: DC = 7 -> 14. One method.
# V3: the whole angle at A tinted (60), split into 30 + 30; AD traced with its right angle; the equal halves of BC ticked;
# 7 written on BD, then AB = 14 written on the figure.
f2_A4, f2_B4, f2_C4, f2_D4 = (320.0, 86.057), (206.444, 282.741), (433.556, 282.741), (320.0, 282.741)
f2_g14 = GEO('f2g14', [
    ('line', f2_tri(f2_A4, f2_B4, f2_C4) + [('seg', f2_A4[0], f2_A4[1], f2_D4[0], f2_D4[1])]
             + f2_lab((320, 64, 'A'), (190, 300, 'B'), (450, 300, 'C'), (320, 306, 'D'))
             + [('arc', 320, 86.057, 44, 270, 300, 'ink', '30°', 66), ('txt', 377, 300, '7', 'ink', 24)]),
    ('whole', [('wedge', 320, 86.057, 38, 240, 300, 'teal'), ('txt', 320, 44, '60°', 'small', 22)]),
    ('half', [('arc', 320, 86.057, 44, 240, 270, 'small', '30°', 66)]),
    ('ad', [('path', [f2_A4, f2_D4], 'teal', 7), ('right', 320, 282.741, 0, 90, 14)]),
    ('mid', [('tick', 206.444, 282.741, 320, 282.741, 2), ('tick', 320, 282.741, 433.556, 282.741, 2), ('txt', 263, 300, '7', 'small', 24)]),
    ('ab', [('txt', 236, 170, '14', 'red', 26)]),
    ('e2', [('txt', 320, 340, 'BD = DC = 7', 'ink', 24)]),
    ('e3', [('txt', 320, 374, 'AB = BC = 7 + 7 = 14', 'red', 24)]),
], vb='170 30 300 360', w=400, title='Equilateral triangle ABC and the line AD')
video('solve-geo31-g014', 'solution', qid='geo31-g014', slides=[
    S('The bisector is also a median',
      L("A B C is an equilateral triangle. Point D lies on B C. Given: angle D A C is thirty degrees, and D C is seven "
        "centimeters. What is A B, in centimeters?", pt('stem', 'A B C is an equilateral', 'hl', 8.0), voice='calm', pause=0.5),
      L("A B is a side of the triangle, and in an equilateral triangle all the sides are equal. So we're really looking "
        "for the side. We know two things, the thirty degrees at A, and D C is seven. [short pause] We'll see what the "
        "line A D does in this triangle.", pt('fig: 30°', 'the thirty degrees'), pt('fig: 7', 'and D C is seven')),
      L("[short pause] A B C is equilateral, so all its angles are sixty. So the whole angle at A is sixty. Thirty of it "
        "is between A D and A C, so the other part, between A B and A D, is sixty minus thirty, which is thirty too.",
        show(f2_g14['line'], 'A B C is equilateral'), show(f2_g14['whole'], 'So the whole angle at A'),
        show(f2_g14['half'], 'so the other part')),
      L("So A D cuts the angle at A into two equal halves. It's the angle bisector. An equilateral triangle is symmetric "
        "from every direction, so this line from the top is also the altitude and the median. As a median, it cuts B C "
        "into two equal parts.", show(f2_g14['ad'], 'So A D cuts the angle'), show(f2_g14['mid'], 'As a median')),
      L("So B D is seven too, and the whole side B C is seven plus seven, which is fourteen. All the sides are equal, so "
        "A B is fourteen. Choice number two is our answer.", show(f2_g14['e2'], 'So B D is seven too'),
        show(f2_g14['e3'], 'seven plus seven'), show(f2_g14['ab'], 'so A B is fourteen'),
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Careful, seven, choice number one, is only half of the side. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 1', 'seven, choice number one'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g015 (Hebrew: the special-triangles sample question 2)
# Hebrew (geo 620-640): two isosceles triangles: ABC (base angles (180 - 30) / 2 = 75), so the whole angle at C is 75 and
# the 75 choice is out ("only part of me can't be 75"); CBD isosceles -> the angle at D is 75 -> the lower angle at C is
# 30 -> the marked angle 75 - 30 = 45. Course numbers 28 / 76 / 28 / 48. One method.
# V3: the big triangle tinted with its base angles written; FOCUS on triangle BCD (the rest dimmed, BCD redrawn and
# tinted) with its angles written; back to the whole figure (redrawn over the dim) with x = 48 written.
f2_A5, f2_B5, f2_C5, f2_D5 = (130.0, 262.0), (510.0, 262.0), (465.52, 83.601), (421.04, 262.0)
f2_g15ticks = [('tick', 130, 262, 510, 262), ('tick', 130, 262, 465.52, 83.601),
               ('tick', 510, 262, 465.52, 83.601, 2), ('tick', 465.52, 83.601, 421.04, 262, 2)]
f2_g15all = f2_tri(f2_A5, f2_B5, f2_C5) + [('seg', 465.52, 83.601, 421.04, 262)] \
    + f2_lab((112, 280, 'A'), (528, 280, 'B'), (465.5, 60, 'C'), (421, 286, 'D')) + f2_g15ticks
f2_T = lambda p: (580 + (p[0] - 421.04) * 1.9, 55 + (p[1] - 83.601) * 1.9)   # the enlarged cut-out of BCD (x1.9)
f2_eB, f2_eC, f2_eD = f2_T(f2_B5), f2_T(f2_C5), f2_T(f2_D5)
f2_g15 = GEO('f2g15', [
    ('line', f2_g15all + [('arc', 130, 262, 70, 0, 28, 'ink', '28°', 94), ('arc', 465.52, 83.601, 46, 208, 256, 'ink', 'x', 64)]),
    ('big', [('tint', [f2_A5, f2_B5, f2_C5], 'teal')]),
    ('b76', [('arc', 510, 262, 22, 104, 180, 'small'), ('txt', 489, 246, '76°', 'small', 18), ('arc', 465.52, 83.601, 34, 208, 284, 'small'),
             ('txt', 505, 92, '76°', 'small', 22)]),
    # 1. the small triangle tinted and outlined inside the copy while it is named
    ('mark', [('tint', [f2_B5, f2_C5, f2_D5], 'orange')] + f2_tri(f2_B5, f2_C5, f2_D5, 'orange', 3.5)),
    # 2. the rest dimmed (BCD still outlined), and BCD as its own enlarged copy with the same labels and tint
    ('focus', [('dim', 95, 40, 470, 265)] + f2_tri(f2_B5, f2_C5, f2_D5, 'orange', 3.5)
              + [('tint', [f2_eB, f2_eC, f2_eD], 'orange')] + f2_tri(f2_eB, f2_eC, f2_eD, 'ink', 3)
              + [('tick', f2_eB[0], f2_eB[1], f2_eC[0], f2_eC[1], 2), ('tick', f2_eC[0], f2_eC[1], f2_eD[0], f2_eD[1], 2)]
              + f2_lab((f2_eB[0] + 18, f2_eB[1] + 20, 'B'), (f2_eC[0], f2_eC[1] - 22, 'C'), (f2_eD[0] - 18, f2_eD[1] + 20, 'D'))
              + [('arc', f2_eB[0], f2_eB[1], 34, 104, 180, 'small', '76°', 62)]),
    # 3. the values on the enlarged part
    ('d76', [('arc', f2_eD[0], f2_eD[1], 34, 0, 76, 'small', '76°', 62)]),
    ('c28', [('arc', f2_eC[0], f2_eC[1], 70, 256, 284, 'orange', '28°', 100)]),
    # back to the whole copy: redrawn over the dim, with the values found written on it too
    ('back', f2_g15all + [('arc', 130, 262, 70, 0, 28, 'ink', '28°', 94), ('arc', 510, 262, 22, 104, 180, 'small'), ('txt', 489, 246, '76°', 'small', 18),
                          ('arc', 421.04, 262, 22, 0, 76, 'small'), ('txt', 443, 246, '76°', 'small', 18), ('arc', 465.52, 83.601, 58, 256, 284, 'orange'), ('txt', 465.5, 205, '28°', 'orange', 20),
                          ('arc', 465.52, 83.601, 46, 208, 256, 'red', 'x', 64)]),
    ('e3', [('txt', 330, 345, 'x = 76° − 28° = 48°', 'red', 36)]),
], vb='95 20 690 410', w=500, title='Triangle ABC with point D on AB, and triangle BCD enlarged')
video('solve-geo31-g015', 'solution', qid='geo31-g015', slides=[
    S('Two isosceles triangles',
      L("In triangle A B C, point D lies on A B. Given: A B equals A C, angle B A C is twenty-eight degrees, and B C "
        "equals C D. What is angle A C D?", pt('stem', 'In triangle A B C', 'hl', 8.0), voice='calm', pause=0.5),
      L("There are two isosceles triangles here. A B equals A C, so the big triangle A B C is isosceles. And B C equals "
        "C D, so the small triangle B C D is isosceles too. [short pause] We'll find the angles step by step, starting "
        "from the twenty-eight at A.", pt('fig: 28°', 'starting from the twenty-eight')),
      L("[short pause] Start with the big triangle, A B C. A B equals A C, so the base angles, at B and at C, are equal. "
        "The angle at A is twenty-eight, so the base angles share one hundred eighty minus twenty-eight, which is one "
        "hundred fifty-two. Half of that is seventy-six. So the angle at B is seventy-six, and the whole angle at C is "
        "seventy-six.", show(f2_g15['line'], 'Start with the big triangle'), show(f2_g15['big'], 'A B equals A C, so the base'),
        show(f2_g15['b76'], 'So the angle at B is seventy-six')),
      L("That already rules out choice number four. x is only part of the angle at C, so it can't be the whole "
        "seventy-six.", mk('cross', 'choice 4', 'That already rules out choice number four')),
      L("Now the small triangle, B C D. Let's look only at it. B C equals C D, so its base angles, at B and at D, are "
        "equal. The angle at B is seventy-six, so the angle at D is seventy-six too.", show(f2_g15['mark'], 'Now the small triangle'), show(f2_g15['focus'], "Let's look only at it"),
        show(f2_g15['d76'], 'so the angle at D')),
      L("In triangle B C D, seventy-six plus seventy-six is one hundred fifty-two. So the angle at C, between C D and C B, "
        "is one hundred eighty minus one hundred fifty-two, which is twenty-eight.", show(f2_g15['c28'], 'So the angle at C, between')),
      L("Now back to the whole figure. The whole angle at C is seventy-six, and twenty-eight of it is between C D and C B. "
        "So x, the angle A C D, is seventy-six minus twenty-eight, which is forty-eight. Choice number three is our answer. "
        "[pause] Okay. I'll see you in the next question.", show(f2_g15['back'], 'Now back to the whole figure'),
        show(f2_g15['e3'], 'seventy-six minus twenty-eight'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# placement: question videos - the colour copy (with its equations) in the right column under the question text
for _g in (f2_g10, f2_g11, f2_g11p, f2_g12, f2_g14, f2_g15): _R(_g, 235)
_R(f2_z12, 300, x=1020)


def f2_pin(g):
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


for _g in (f2_g10, f2_g11, f2_g11p, f2_g12, f2_z12, f2_g14, f2_g15, f2_iso, f2_sym, f2_fold, f2_eq, f2_rt, f2_med): f2_pin(_g)

# =================================================================================================================
# Topic-31 fragment f3 (2026-10-14): geo-016 (Area of Triangles), solve-geo31-g017, solve-q-r26-t31-01,
# solve-q-r26-t31-02, geo-018-after (A Median Halves the Area), geo-019 (The Pythagorean Theorem).
# Hebrew: geo 665-759 (area: units, the unit square, the rectangle as rows of squares, the right triangle = half a
# rectangle, any triangle = half a rectangle via the altitude, "a side, not a base", the obtuse triangle's outside
# altitude; the parallel-lines question with both methods), 828-849 (a median halves the area), 852-870 (Pythagoras).
# Colours (V3, the same in every video): the part under study teal, the second part orange, a wrong path red,
# construction lines (altitudes, extensions, cuts) dashed.
# =================================================================================================================
import math as _f3m


def _f3p(o, x, y, s):
    """point (x, y) in units -> svg coordinates: origin o = (svg x, svg y of y=0), scale s (y up)"""
    return (o[0] + x * s, o[1] - y * s)


def _f3foot(p, a, b):
    """the foot of the perpendicular from p to the line a-b"""
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay; t = ((px - ax) * dx + (py - ay) * dy) / float(dx * dx + dy * dy)
    return (ax + t * dx, ay + t * dy)


def _f3tri(a, b, c, col='ink', w=3):
    return [('seg', a[0], a[1], b[0], b[1], col, w), ('seg', b[0], b[1], c[0], c[1], col, w), ('seg', c[0], c[1], a[0], a[1], col, w)]


def _f3mid(a, b, dx=0, dy=0):
    return ((a[0] + b[0]) / 2.0 + dx, (a[1] + b[1]) / 2.0 + dy)


# ------------------------------------------------------------------------------------------------ geo-016 (lesson: Area of Triangles)
# Hebrew (geo 665-726): length is measured in cm, area in cm², m², km²; the 1 x 1 square is 1 cm²; a rectangle of rows of
# squares (her 4 x 3 = 12; here 5 x 3 = 15 and 6 x 2 = 12); a right triangle is half a rectangle (the product of the legs
# over 2); any triangle in a rectangle: drop the altitude, two rectangles, each cut in half by the triangle's side;
# "a side times the altitude to that side, over 2" - why a side and not a base (turn the triangle); the obtuse triangle:
# extend the side, the altitude outside, but only the side itself counts. Examples: legs 6, 3 and 8, 5; side 9 / altitude
# 6; one triangle with two side-altitude pairs (12, 6 and 9, 8: both 36); side 7 / outside altitude 4 = 14 (non-example:
# the extended length 10 gives 20). V3: the unit square, then rows of squares counted; the diagonal cuts the rectangle;
# the altitude drawn in, each half-rectangle's two halves tinted; the triangle turned (two sides, each with its altitude in
# its own colour); the extension and the outside altitude dashed, the wrong length traced red.
F3U = GEO('f3u', [
    ('line', [('seg', 250, 50, 390, 50), ('seg', 390, 50, 390, 190), ('seg', 390, 190, 250, 190), ('seg', 250, 190, 250, 50)]),
    ('lab', [('txt', 320, 222, '1 cm', 'ink', 28), ('txt', 448, 120, '1 cm', 'ink', 28)]),
    ('area', [('tint', [(250, 50), (390, 50), (390, 190), (250, 190)], 'teal'), ('txt', 320, 120, '1 cm²', 'teal', 32)]),
], vb='150 20 360 220', w=600, col=0, title='A square of 1 cm by 1 cm: 1 cm²')
_f3g = [('seg', 120 + 80 * i, 30, 120 + 80 * i, 270, 'ink', 1.6) for i in range(1, 5)] + [('seg', 120, 30 + 80 * j, 520, 30 + 80 * j, 'ink', 1.6) for j in (1, 2)]
F3R = GEO('f3r', [
    ('line', [('seg', 120, 30, 520, 30), ('seg', 520, 30, 520, 270), ('seg', 520, 270, 120, 270), ('seg', 120, 270, 120, 30)]),
    ('grid', _f3g),
    ('rows', [('tint', [(120, 30), (520, 30), (520, 110), (120, 110)], 'teal'), ('tint', [(120, 190), (520, 190), (520, 270), (120, 270)], 'teal'),
              ('txt', 320, 300, '5', 'ink', 30), ('txt', 92, 150, '3', 'ink', 30)]),
], vb='60 10 520 310', w=600, col=0, title='A rectangle of 3 rows of 5 squares')
F3Ra = IH('f3ra', '$5\\times3=15$ cm²', size=34, col=1)
F3Rb = IH('f3rb', '$6\\times2=12$ cm²', size=34, col=1)
F3T = GEO('f3t', [
    ('line', [('seg', 140, 50, 500, 50), ('seg', 500, 50, 500, 230), ('seg', 500, 230, 140, 230), ('seg', 140, 230, 140, 50),
              ('txt', 320, 262, '6', 'ink', 30), ('txt', 112, 140, '3', 'ink', 30)]),
    ('diag', [('seg', 140, 50, 500, 230, 'teal', 3, True)]),
    ('half', [('tint', [(140, 50), (140, 230), (500, 230)], 'teal'), ('right', 140, 230, 0, 90, 18)]),
    ('other', [('tint', [(140, 50), (500, 50), (500, 230)], 'orange')]),
], vb='80 20 480 260', w=600, col=0, title='A right triangle is half a rectangle')
F3Ta = IH('f3ta', '$\\frac{6\\times3}{2}=\\frac{18}{2}=9$', size=34, col=1)
F3Tb = I('f3tb', 'Right triangle: $\\ \\dfrac{\\text{leg}\\times\\text{leg}}{2}$', size=32, col=1)
F3Tc = IH('f3tc', '$\\frac{8\\times5}{2}=20$', size=34, col=1)
F3A = GEO('f3a', [
    ('line', _f3tri((100, 260), (520, 260), (240, 60)) + [('dot', 240, 60)]),
    ('rect', [('seg', 100, 60, 520, 60, 'ink', 2, True), ('seg', 100, 60, 100, 260, 'ink', 2, True), ('seg', 520, 60, 520, 260, 'ink', 2, True)]),
    ('alt', [('seg', 240, 60, 240, 260, 'teal', 3, True), ('right', 240, 260, 0, 90, 16)]),
    ('left', [('tint', [(100, 260), (240, 260), (240, 60)], 'teal'), ('path', [(100, 260), (240, 60)], 'teal', 6)]),
    ('right', [('tint', [(240, 60), (240, 260), (520, 260)], 'orange'), ('path', [(240, 60), (520, 260)], 'orange', 6)]),
], vb='60 30 500 260', w=600, col=0, title='Any triangle is half of a rectangle')
F3Aa = I('f3aa', 'Area $=\\dfrac{\\text{side}\\times\\text{its altitude}}{2}$', size=32, col=1)
F3Ab = IH('f3ab', '$\\frac{9\\times6}{2}=27$', size=34, col=1)
# one triangle, two sides with their own altitudes: B(0,0), C(12,0), A(sqrt45, 6): BC 12 / 6, AB 9 / 8, area 36
_f3o, _f3s = (110, 270), 28
_f3B, _f3C, _f3A = _f3p(_f3o, 0, 0, _f3s), _f3p(_f3o, 12, 0, _f3s), _f3p(_f3o, _f3m.sqrt(45), 6, _f3s)
_f3H1 = (_f3A[0], _f3B[1]); _f3H2 = _f3foot(_f3C, _f3B, _f3A)
_f3d2 = gdir(_f3H2[0], _f3H2[1], _f3C[0], _f3C[1]); _f3d2b = gdir(_f3H2[0], _f3H2[1], _f3B[0], _f3B[1])
F3S = GEO('f3s', [
    ('line', _f3tri(_f3B, _f3C, _f3A) + [('txt', _f3B[0] - 22, _f3B[1] + 10, 'B', 'ink', 28, True), ('txt', _f3C[0] + 22, _f3C[1] + 10, 'C', 'ink', 28, True),
                                       ('txt', _f3A[0], _f3A[1] - 24, 'A', 'ink', 28, True)]),
    ('p1', [('seg', _f3B[0], _f3B[1], _f3C[0], _f3C[1], 'teal', 6), ('seg', _f3A[0], _f3A[1], _f3H1[0], _f3H1[1], 'teal', 3, True),
            ('right', _f3H1[0], _f3H1[1], 0, 90, 14), ('txt', 260, _f3B[1] + 30, '12', 'teal', 28), ('txt', _f3A[0] + 18, 175, '6', 'teal', 28)]),
    ('p2', [('seg', _f3B[0], _f3B[1], _f3A[0], _f3A[1], 'orange', 6), ('seg', _f3C[0], _f3C[1], _f3H2[0], _f3H2[1], 'orange', 3, True),
            ('right', _f3H2[0], _f3H2[1], _f3d2, _f3d2b, 14, 'orange'), ('txt', 172, 165, '9', 'orange', 28),
            ('txt', _f3m.floor((_f3C[0] + _f3H2[0]) / 2) + 18, (_f3C[1] + _f3H2[1]) / 2 - 14, '8', 'orange', 28)]),
], vb='60 50 500 270', w=600, col=0, title='Any side, with the altitude to that side')
F3Sa = IH('f3sa', '$\\frac{12\\times6}{2}=36$', size=32, col=1)
F3Sb = IH('f3sb', '$\\frac{9\\times8}{2}=36$', size=32, col=1)
# obtuse: B(0,0), C(7,0), A(10,4); the altitude falls outside, at x = 10
_f3o2, _f3s2 = (100, 250), 34
_f3Bo, _f3Co, _f3Ao = _f3p(_f3o2, 0, 0, _f3s2), _f3p(_f3o2, 7, 0, _f3s2), _f3p(_f3o2, 10, 4, _f3s2)
_f3Fo = (_f3Ao[0], _f3Bo[1])
F3O = GEO('f3o', [
    ('line', _f3tri(_f3Bo, _f3Co, _f3Ao) + [('txt', _f3Bo[0] - 22, _f3Bo[1] + 10, 'B', 'ink', 28, True), ('txt', _f3Co[0], _f3Co[1] + 30, 'C', 'ink', 28, True),
                                          ('txt', _f3Ao[0], _f3Ao[1] - 24, 'A', 'ink', 28, True)]),
    ('side', [('seg', _f3Bo[0], _f3Bo[1], _f3Co[0], _f3Co[1], 'teal', 6), ('txt', (_f3Bo[0] + _f3Co[0]) / 2, _f3Bo[1] + 30, '7', 'teal', 28)]),
    ('ext', [('seg', _f3Co[0], _f3Co[1], _f3Fo[0] + 30, _f3Fo[1], 'teal', 2.5, True)]),
    ('alt', [('seg', _f3Ao[0], _f3Ao[1], _f3Fo[0], _f3Fo[1], 'teal', 3, True), ('right', _f3Fo[0], _f3Fo[1], 90, 180, 14), ('txt', _f3Fo[0] + 22, 182, '4', 'teal', 28)]),
    ('calc', [('txt', 280, 60, '7 × 4 ÷ 2 = 14', 'teal', 28)]),
    ('wrong', [('path', [(_f3Bo[0], _f3Bo[1] + 44), (_f3Fo[0], _f3Fo[1] + 44)], 'red', 5), ('txt', (_f3Bo[0] + _f3Fo[0]) / 2, _f3Bo[1] + 72, '10 ✗', 'red', 26),
               ('txt', 280, 100, '10 × 4 ÷ 2 = 20 ✗', 'red', 26)]),
], vb='60 30 520 310', w=600, col=0, title='An obtuse triangle: the altitude falls outside')
F3Ea = I('f3ea', 'Rectangle: $\\ $length $\\times$ width', size=30, col=1)
F3Eb = I('f3eb', 'Right triangle: $\\ \\dfrac{\\text{leg}\\times\\text{leg}}{2}$', size=30, col=1)
F3Ec = I('f3ec', 'Any triangle: $\\ \\dfrac{\\text{side}\\times\\text{its altitude}}{2}$', size=30, col=1)
F3Ed = I('f3ed', 'Altitude outside? $\\ $Still only the side itself', size=30, col=1)
video('geo-016', 'lesson', slides=[
    S('Area of Triangles',
      L("Area of triangles. Before we find the area of a triangle, let's first understand what area even is.")),
    S('Length and area',
      L("Until now, we measured lengths, like a line, a distance or a side. We measure a length in centimeters, or in meters "
        "or kilometers."),
      L("Area is measured in square centimeters, or square meters, or square kilometers. What does that mean? Take a square "
        "whose side is one centimeter. One side is a centimeter, and the other side is a centimeter too. Its area is one "
        "square centimeter.", show(F3U['line'], 'Take a square'), show(F3U['lab'], 'One side is a centimeter'),
        show(F3U['area'], 'Its area is one square'))),
    S('A rectangle',
      L("Now take squares like that, and build a rectangle out of them. Here we have three rows, and five squares in every "
        "row.", show(F3R['line'], 'build a rectangle'), show(F3R['grid'], 'Here we have three rows'),
        show(F3R['rows'], 'five squares in every')),
      L("So to find the area, we take the length, five, times the width, three. Five times three is fifteen, so the area is "
        "fifteen square centimeters. That's three rows of five squares, and each square is one square centimeter.",
        show(F3Ra, 'Five times three is fifteen')),
      L("In the same way, a rectangle six centimeters long and two centimeters wide has two rows of six squares. Six times "
        "two is twelve square centimeters. That's how we find the area of a rectangle, length times width.",
        show(F3Rb, 'Six times two is twelve'))),
    S('A right triangle',
      L("Now the area of a right triangle. A right triangle is really half of a rectangle. Here's a rectangle, six by three. "
        "Draw its diagonal, and it cuts the rectangle into two equal triangles.", show(F3T['line'], "Here's a rectangle"),
        show(F3T['diag'], 'Draw its diagonal')),
      L("Each of them is a right triangle. This one has its right angle down here, and its two legs are six and three. The "
        "legs are the two sides that make the right angle.", show(F3T['half'], 'This one has its right angle')),
      L("The rectangle is six times three, which is eighteen. The triangle is exactly half of it, so its area is eighteen "
        "over two, which is nine.", show(F3T['other'], 'The triangle is exactly half'), show(F3Ta, 'so its area is eighteen')),
      L("So the area of a right triangle is one leg times the other leg, divided by two, because the legs are like the "
        "length and the width of the rectangle. Another example: legs eight and five. Eight times five is forty, and half "
        "of forty is twenty.", show(F3Tb, 'So the area of a right triangle'), show(F3Tc, 'Eight times five is forty'))),
    S('Any triangle',
      L("Now any triangle. We can put it inside a rectangle too. But is it really half of the rectangle? With the right "
        "triangle it was easy to see, but here it's not so clear.", show(F3A['line'], 'Now any triangle'),
        show(F3A['rect'], 'inside a rectangle too')),
      L("Let's drop an altitude from the top vertex, straight down to the bottom side. Now the big rectangle is cut into two "
        "rectangles.", show(F3A['alt'], 'drop an altitude')),
      L("Look at the left rectangle. The side of the triangle cuts it along its diagonal, so the shaded part is exactly half "
        "of it, and the white part is the other half. The right rectangle is the same, a shaded half and a white half.",
        show(F3A['left'], 'Look at the left rectangle'), show(F3A['right'], 'The right rectangle is the same')),
      L("So altogether, the triangle is half of the big rectangle. The rectangle's height is exactly the height of the "
        "triangle. So the area of a triangle is the base times the height, over two. Or, to say it more exactly, a side, "
        "times the altitude to that side, over two.", show(F3Aa, 'So the area of a triangle')),
      L("For example, a side of nine, and the altitude to that side is six. Nine times six is fifty-four, and half of that "
        "is twenty-seven.", show(F3Ab, 'Nine times six is'))),
    S('Any side as the base',
      L("Why do I say a side, and not the base? Because we can look at a triangle from another direction. We can turn it. A "
        "triangle doesn't really have a base. The base is only the side we happen to look from.",
        show(F3S['line'], 'we can look at a triangle')),
      L("Here, take the side B C, which is twelve, and the altitude to it from A, which is six. Now take the side A B, which "
        "is nine. The altitude to A B comes from C, and it's eight. What matters is a side, and the altitude that goes to "
        "that same side.", show(F3S['p1'], 'take the side B C'), show(F3S['p2'], 'Now take the side A B')),
      L("Twelve times six is seventy-two, and half of that is thirty-six. Nine times eight is also seventy-two, and half of "
        "that is thirty-six too. Any side with its own altitude gives the same area.",
        show(F3Sa, 'Twelve times six is'), show(F3Sb, 'Nine times eight is'))),
    S('The altitude outside',
      L("In an obtuse triangle, we do exactly the same thing, but the altitude falls outside the triangle. Take the side B C, "
        "which is seven.", show(F3O['line'], 'In an obtuse triangle'), show(F3O['side'], 'Take the side B C')),
      L("To drop the altitude from A, we first extend the side B C, and then we drop the altitude to that line, outside the "
        "triangle. Here it's four.", show(F3O['ext'], 'we first extend'), show(F3O['alt'], 'then we drop the altitude')),
      L("The area is still the side times the altitude to it, over two. Seven times four is twenty-eight, and half of that is "
        "fourteen. Careful, we don't use the whole extended line, from B all the way to the altitude. That's ten, and it "
        "would give twenty, which is wrong. Only the side of the triangle itself counts.",
        show(F3O['calc'], 'Seven times four is'), show(F3O['wrong'], "we don't use the whole extended line"))),
    S('Recap',
      L("So, a rectangle is length times width. A right triangle is one leg times the other leg, over two. Any triangle is a "
        "side times the altitude to that side, over two. And when the altitude falls outside, we still use only the side "
        "itself.", show(F3Ea, 'a rectangle is length'), show(F3Eb, 'A right triangle is one leg'),
        show(F3Ec, 'Any triangle is a side'), show(F3Ed, 'when the altitude falls outside')),
      L("Now let's see an example. [pause] Okay. I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ geo31-g017 (Hebrew: the lesson's example, geo 728-759)
# Hebrew: no numbers at all - start from the givens: CD = x, DE = 3x (here 5x); draw the height h, the same for both
# triangles because the lines are parallel; divide the two area expressions (multiply by the reciprocal, cancel); then
# the second way: cut DE into pieces of x, all the small triangles have the same base and height, so the same area.
# V3: our colour copy right of the question; x and 5x written on the bottom line; both heights dashed between the
# parallel lines; ACD tinted teal, BDE orange; method 2: the cutting points, the lines from B, the triangles numbered.
FIG_LEFT.update({'solve-geo31-g017'})
_f3gl = [('seg', 56.8, 96, 583.2, 96), ('seg', 56.8, 264, 583.2, 264), ('par', 470, 96, 540, 96), ('par', 470, 264, 540, 264)]
_f3gt = _f3tri((140, 96), (96, 264), (166, 264)) + _f3tri((400, 96), (166, 264), (516, 264))
_f3glab = [('txt', 140, 74, 'A', 'ink', 26, True), ('txt', 400, 74, 'B', 'ink', 26, True), ('txt', 86, 290, 'C', 'ink', 26, True),
           ('txt', 166, 290, 'D', 'ink', 26, True), ('txt', 523, 290, 'E', 'ink', 26, True)]
F3G = GEO('f3g', [
    ('line', _f3gl + _f3gt + _f3glab),
    ('x', [('txt', 131, 318, 'x', 'teal', 28, True), ('txt', 341, 318, '5x', 'orange', 28, True)]),
    ('h1', [('seg', 140, 96, 140, 264, 'teal', 3, True), ('right', 140, 264, 0, 90, 13), ('txt', 124, 180, 'h', 'teal', 28, True)]),
    ('h2', [('seg', 400, 96, 400, 264, 'orange', 3, True), ('right', 400, 264, 0, 90, 13, 'orange'), ('txt', 416, 180, 'h', 'orange', 28, True)]),
    ('tB', [('tint', [(400, 96), (166, 264), (516, 264)], 'orange')]),
    ('tA', [('tint', [(140, 96), (96, 264), (166, 264)], 'teal')]),
], vb='40 50 560 285', w=480, title='Two triangles between the same parallel lines')
_f3cut = [236, 306, 376, 446]
F3G2 = GEO('f3g2', [
    ('line', _f3gl + _f3gt + _f3glab),
    ('cuts', [('seg', 400, 96, c, 264, 'orange', 2.5, True) for c in _f3cut] + [('dot', c, 264) for c in _f3cut]),
    ('num', [('txt', 131, 318, 'x', 'teal', 26, True)] + [('txt', 201 + 70 * i, 318, 'x', 'orange', 26, True) for i in range(5)]
            + [('txt', 136 + 0, 232, '1', 'teal', 24)] + [('txt', 222 + 70 * i, 242, str(i + 1), 'orange', 24) for i in range(5)]),
    ('six', [('tint', [(140, 96), (96, 264), (166, 264)], 'teal')] + [('tint', [(400, 96), (166 + 70 * i, 264), (236 + 70 * i, 264)], 'orange' if i % 2 == 0 else 'teal') for i in range(5)]),
], vb='40 50 560 285', w=480, title='Cut into triangles with the same base and height')
F3Ga = I('f3ga', '$\\dfrac{S_{BDE}}{S_{ACD}}=\\dfrac{\\frac{5x\\cdot h}{2}}{\\frac{x\\cdot h}{2}}$', size=30)
F3Gb = I('f3gb', '$=\\dfrac{5x\\cdot h}{2}\\cdot\\dfrac{2}{x\\cdot h}=5$', size=28)
video('solve-geo31-g017', 'solution', qid='geo31-g017', slides=[
    SM('Method 1 · Letters', 'Use letters',
      L("Points A and B lie on one line, and C, D and E lie on a parallel line. Given: D E is equal to five times C D. What "
        "is the area of B D E divided by the area of A C D?", pt('stem', 'Points A and B', 'hl', 8.0), voice='calm', pause=0.5),
      L("Look, there are no numbers here at all, no area and no length. So how do we start? Simply from the givens. [short "
        "pause] We'll solve it two ways, with letters, and then by cutting the big triangle into small ones.",
        pt('stem', 'there are no numbers here')),
      L("[short pause] D E is five times C D. So let's call C D x, and then D E is five x.",
        show(F3G['line'], 'D E is five times'), show(F3G['x'], "let's call C D x")),
      L("We don't know the heights, but let's draw them anyway, and call them h. The height of A C D is the distance from A "
        "down to the bottom line. The height of B D E is the distance from B down to the same line. The lines are parallel, "
        "so the distance between them is the same everywhere. So both triangles have the same height, h.",
        show(F3G['h1'], 'The height of A C D'), show(F3G['h2'], 'The height of B D E')),
      L("Now the areas. The area of a triangle is a side times the altitude to that side, over two. Triangle B D E has the "
        "side five x and the height h, so its area is five x times h, over two. Triangle A C D has the side x and the same "
        "height h, so its area is x times h, over two.", show(F3G['tB'], 'Triangle B D E has'),
        show(F3G['tA'], 'Triangle A C D has'), show(F3Ga, 'so its area is x times h')),
      L("Now divide. To divide by a fraction, we multiply by its reciprocal, so we flip the bottom fraction. x times h "
        "cancels, and the twos cancel, so we get five. Choice number one is our answer.",
        show(F3Gb, 'flip the bottom fraction'), mk('tick', 'choice 1', 'Choice number one is our answer')),
      L("Careful, twenty-five, choice number three, would be right only if the heights were five times bigger too. But the "
        "heights are equal, so only the bases count.", mk('cross', 'choice 3', 'twenty-five, choice number three'))),
    SM('Method 2 · Equal small triangles', 'Equal small triangles',
      L("[pause] Another way, without any of that calculation. D E is five x, so we can cut it into five pieces, each of "
        "length x. Then we join B to each cutting point. Now B D E is made of five small triangles, and each one has a base "
        "of x.", show(F3G2['line'], 'Another way'), show(F3G2['cuts'], 'we join B to each'),
        show(F3G2['num'], 'B D E is made of five')),
      L("All five small triangles, and A C D too, have the same base, x, and the same height, h, because they all sit "
        "between the same two parallel lines. So all six triangles have the same area.",
        show(F3G2['six'], 'So all six triangles')),
      L("B D E is five of them, and A C D is one of them, so the ratio is five. Choice number one again. [pause] Okay. I'll "
        "see you in the next question.", mk('tick', 'choice 1', 'Choice number one again'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t31-01 (added)
# REMINDER: area = a side times the altitude to it, over 2 (geo-016); legs (geo-013); the median to the hypotenuse is
# half of it (geo-013). NEW at the step: an altitude -> the area two ways, set equal. V3: the legs traced teal (a side and
# its altitude), the area written inside; AB and CD traced orange; each equation written on the board as it is said and
# the found CD written next to it.
FIG_LEFT.update({'solve-q-r26-t31-01'})
_f3qA, _f3qB, _f3qC, _f3qD = (170, 290), (470, 290), (278, 146), (278, 290)
F3Q = GEO('f3q', [
    ('line', _f3tri(_f3qA, _f3qB, _f3qC) + [('seg', 278, 146, 278, 290), ('right', 278, 290, 0, 90, 12), ('right', 278, 146, gdir(278, 146, 170, 290), gdir(278, 146, 470, 290), 13),
              ('txt', 154, 304, 'A', 'ink', 24, True), ('txt', 486, 304, 'B', 'ink', 24, True), ('txt', 278, 126, 'C', 'ink', 24, True),
              ('txt', 278, 316, 'D', 'ink', 24, True), ('txt', 206, 206, '15', 'ink', 22), ('txt', 392, 206, '20', 'ink', 22), ('txt', 400, 314, '25', 'ink', 22)]),
    ('legs', [('seg', 170, 290, 278, 146, 'teal', 6), ('seg', 278, 146, 470, 290, 'teal', 6), ('right', 278, 146, gdir(278, 146, 170, 290), gdir(278, 146, 470, 290), 13)]),
    ('area', [('tint', [_f3qA, _f3qB, _f3qC], 'teal'), ('txt', 340, 262, '150', 'teal', 30)]),
    ('hyp', [('seg', 170, 290, 470, 290, 'orange', 6), ('seg', 278, 146, 278, 290, 'orange', 5)]),
], vb='130 100 400 230', w=380, title='Triangle ABC, right at C, with the altitude CD')
F3Qa = I('f3qa', '$\\frac{15\\times20}{2}=150$', size=28)
F3Qb = I('f3qb', '$\\frac{25\\times CD}{2}=150\\ \\to\\ CD=12$', size=26)
video('solve-q-r26-t31-01', 'solution', qid='q-r26-t31-01', slides=[
    S('The area two ways',
      L("Triangle A B C is right at C, and C D is the altitude to A B. Given: A C is fifteen centimeters, B C is twenty "
        "centimeters, and A B is twenty-five centimeters. What is C D, in centimeters?",
        pt('stem', 'Triangle A B C', 'hl', 9.0), voice='calm', pause=0.5),
      L("C D is an altitude, and an altitude always comes with an area. [short pause] So we'll find the area of the triangle "
        "in two ways, and then set them equal.", pt('fig: D', 'C D is an altitude')),
      L("[short pause] First way, with the legs. The right angle is at C, so A C and B C are perpendicular. That means B C is "
        "the altitude to the side A C. So the area is fifteen times twenty, over two. Fifteen times twenty is three hundred, "
        "and half of that is a hundred fifty.", show(F3Q['line'], 'First way'), show(F3Q['legs'], 'The right angle is at C'),
        show(F3Q['area'], 'So the area is fifteen')),
      L("Second way, with the side A B, which is twenty-five, and the altitude to it, which is C D. So the area is also "
        "twenty-five times C D, over two.", show(F3Q['hyp'], 'Second way')),
      L("It's the same triangle, so it's the same area. Twenty-five times C D, over two, is a hundred fifty, so twenty-five "
        "times C D is three hundred. Three hundred divided by twenty-five is twelve, so C D is twelve. Choice number two is "
        "our answer.", show(F3Qa, "It's the same triangle"), show(F3Qb, 'Twenty-five times C D, over two, is'),
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Careful with two traps. Six, choice number one, is a hundred fifty divided by twenty-five: someone forgot to double "
        "the area first. And twelve and a half, choice number three, is half of A B. That's the median to the hypotenuse, "
        "not the altitude.", mk('cross', 'choice 1', 'Six, choice number one'),
        mk('cross', 'choice 3', 'twelve and a half, choice number three')),
      L("A short way to remember it, in a right triangle: one leg times the other leg equals the hypotenuse times the "
        "altitude to it. Fifteen times twenty is three hundred, and three hundred divided by twenty-five is twelve. [pause] "
        "Okay. I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ q-r26-t31-02 (added)
# REMINDER: area = a side times the altitude to it, over 2; a leg is shorter than the hypotenuse (geo-013). NEW at the
# step: two sides and no angle - the area is not fixed; the biggest one; "could be" = one working case. V3 (general,
# 2-3 variations): BC on the floor, A swinging around B at distance 6 - low, leaning back, straight up - each with its
# height dashed; the biggest when AB stands up.
_f3wB, _f3wC = (140, 270), (460, 270)
_f3w = [(30, 'teal'), (120, 'teal'), (90, 'orange')]
_f3wl = []
for _f3ang, _f3col in _f3w:
    _f3Ap = gpt(_f3wB[0], _f3wB[1], 240, _f3ang)
    _f3wl.append([('seg', _f3wB[0], _f3wB[1], _f3Ap[0], _f3Ap[1], _f3col, 4), ('seg', _f3Ap[0], _f3Ap[1], _f3wC[0], _f3wC[1], _f3col, 2.5),
                  ('dot', _f3Ap[0], _f3Ap[1]), ('seg', _f3Ap[0], _f3Ap[1], _f3Ap[0], _f3wB[1], _f3col, 2.5, True)])
F3W = GEO('f3w', [
    ('line', [('seg', _f3wB[0], _f3wB[1], _f3wC[0], _f3wC[1], 'ink', 4), ('txt', _f3wB[0] - 6, 298, 'B', 'ink', 26, True),
              ('txt', _f3wC[0], 298, 'C', 'ink', 26, True), ('txt', 300, 298, '8', 'ink', 26), ('seg', 0, 270, 520, 270, 'ink', 1.5, True)]),
    ('a1', _f3wl[0] + [('txt', 260, 182, '6', 'teal', 24)]),
    ('a3', _f3wl[1] + [('txt', 64, 160, '6', 'teal', 24)]),
    ('a2', _f3wl[2] + [('right', 140, 270, 0, 90, 16, 'orange'), ('txt', 118, 150, '6', 'orange', 26)]),
], vb='0 10 520 300', w=560, col=0, title='Side AB of 6, at different angles to BC')
F3Wa = I('f3wa', 'Area $\\le\\dfrac{8\\cdot6}{2}=24$', size=32)
F3Wb = I('f3wb', 'Height $5$: $\\ \\dfrac{8\\cdot5}{2}=20$ ✓', size=32)
video('solve-q-r26-t31-02', 'solution', qid='q-r26-t31-02', slides=[
    S('The biggest area',
      L("In triangle A B C, A B is six centimeters, and B C is eight centimeters. Which of the following could be the area "
        "of the triangle, in square centimeters?", pt('stem', 'In triangle A B C', 'hl', 7.0), voice='calm', pause=0.5),
      L("We know two sides, but not the angle between them, so the area isn't fixed. It changes when the angle at B changes. "
        "[short pause] So first we'll find the biggest area this triangle can have, and then we'll check the choices.",
        pt('stem', 'We know two sides')),
      L("[short pause] Put the side B C, which is eight, on the floor. The height of the triangle is the distance from A "
        "straight down to the floor. A is always six away from B, because A B is six, but the side A B can lean at "
        "different angles.", show(F3W['line'], 'Put the side B C')),
      L("When A B leans low, the height is small. When A B leans back, the height is bigger. The height is a leg of a small "
        "right triangle, and A B is its hypotenuse, the longest side. So the height can never be more than six. It's exactly "
        "six only when A B stands straight up, with a right angle at B.", show(F3W['a1'], 'When A B leans low'),
        show(F3W['a3'], 'When A B leans back'), show(F3W['a2'], "It's exactly six only when")),
      L("So the biggest area is eight times six, over two, which is twenty-four. Twenty-five, forty-eight and twenty-eight "
        "are all more than twenty-four, so they're impossible.", show(F3Wa, 'So the biggest area'),
        mk('cross', 'choice 1', 'Twenty-five, forty-eight'), mk('cross', 'choice 2', 'forty-eight and twenty-eight'),
        mk('cross', 'choice 4', "so they're impossible")),
      L("The question asks what could be the area, so let's check that twenty really can happen. If A leans so that the "
        "height is five, the area is eight times five, over two, which is twenty. Five is less than six, so that's "
        "possible. Choice number three is our answer.", show(F3Wb, 'If A leans so that the height is five'),
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Careful, forty-eight is six times eight: someone forgot to divide by two. And many students find twenty-four and "
        "stop, but nobody said that the angle at B is ninety degrees. With two sides and no angle, the area can be anything "
        "up to half of their product. [pause] Okay. I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ geo-018-after (lesson: A Median Halves the Area)
# Hebrew (geo 828-849): one more small tip - a median cuts a triangle into two triangles with the same area: any
# triangle; BD = DC; the altitude from A is the height of both (outside for the obtuse one); same base, same height ->
# same area; "if you see a median, you automatically know". Course additions kept: same area is not the same shape; the
# vertex moving along a line parallel to the base. Numbers: BC 10, height 6 -> each half 15, the whole 30.
# V3: the triangle, the median with equal tick marks, the halves tinted teal / orange, the one altitude dashed (outside
# the right half), the numbers; then a generic picture: one base, the dashed parallel line, three apex positions.
_f3mo, _f3ms = (110, 260), 34
_f3mB, _f3mC, _f3mA = _f3p(_f3mo, 0, 0, _f3ms), _f3p(_f3mo, 10, 0, _f3ms), _f3p(_f3mo, 2, 6, _f3ms)
_f3mD = _f3p(_f3mo, 5, 0, _f3ms); _f3mH = (_f3mA[0], _f3mB[1])
F3M = GEO('f3m', [
    ('line', _f3tri(_f3mB, _f3mC, _f3mA) + [('txt', _f3mB[0] - 22, _f3mB[1] + 8, 'B', 'ink', 28, True), ('txt', _f3mC[0] + 22, _f3mC[1] + 8, 'C', 'ink', 28, True),
                                          ('txt', _f3mA[0], _f3mA[1] - 24, 'A', 'ink', 28, True)]),
    ('med', [('seg', _f3mA[0], _f3mA[1], _f3mD[0], _f3mD[1], 'teal', 4), ('dot', _f3mD[0], _f3mD[1], 'D', 0, 30),
             ('tick', _f3mB[0], _f3mB[1], _f3mD[0], _f3mD[1], 1), ('tick', _f3mD[0], _f3mD[1], _f3mC[0], _f3mC[1], 1)]),
    ('two', [('tint', [_f3mA, _f3mB, _f3mD], 'teal'), ('tint', [_f3mA, _f3mD, _f3mC], 'orange')]),
    ('alt', [('seg', _f3mA[0], _f3mA[1], _f3mH[0], _f3mH[1], 'ink', 3, True), ('right', _f3mH[0], _f3mH[1], 0, 90, 14, 'ink')]),
    ('nums', [('txt', (_f3mB[0] + _f3mD[0]) / 2, _f3mB[1] + 34, '5', 'teal', 26), ('txt', (_f3mD[0] + _f3mC[0]) / 2, _f3mB[1] + 34, '5', 'orange', 26),
              ('txt', _f3mA[0] - 18, 160, '6', 'ink', 26), ('txt', 210, 222, '15', 'teal', 26), ('txt', 300, 222, '15', 'orange', 26)]),
], vb='60 10 520 310', w=600, col=0, title='A median cuts a triangle into two triangles with the same area')
F3Ma = I('f3ma', 'A median splits a triangle into two triangles of equal area', size=30, col=1)
_f3pB, _f3pC = (150, 270), (390, 270)
F3P = GEO('f3p', [
    ('line', [('seg', _f3pB[0], _f3pB[1], _f3pC[0], _f3pC[1], 'ink', 4), ('seg', 30, 90, 610, 90, 'ink', 2, True),
              ('txt', _f3pB[0], 298, 'B', 'ink', 26, True), ('txt', _f3pC[0], 298, 'C', 'ink', 26, True)]),
    ('t1', [('seg', 80, 90, _f3pB[0], _f3pB[1], 'teal', 3), ('seg', 80, 90, _f3pC[0], _f3pC[1], 'teal', 3), ('dot', 80, 90)]),
    ('t2', [('seg', 270, 90, _f3pB[0], _f3pB[1], 'orange', 3), ('seg', 270, 90, _f3pC[0], _f3pC[1], 'orange', 3), ('dot', 270, 90)]),
    ('t3', [('seg', 560, 90, _f3pB[0], _f3pB[1], 'teal', 3), ('seg', 560, 90, _f3pC[0], _f3pC[1], 'teal', 3), ('dot', 560, 90),
            ('seg', 560, 90, 560, 270, 'teal', 2.5, True), ('seg', _f3pC[0], 270, 560, 270, 'teal', 2, True), ('right', 560, 270, 90, 180, 14)]),
], vb='0 60 640 260', w=600, col=0, title='The same base and the same height: the same area')
F3Pa = I('f3pa', 'Same base $\\cdot$ same height $\\Rightarrow$ same area', size=30, col=1)
video('geo-018-after', 'lesson', slides=[
    S('A Median Halves the Area',
      L("That's the area of triangles. Just one more small tip to finish.")),
    S('A median halves the area',
      L("A median of a triangle cuts it into two triangles with the same area. Remember, a median goes from a vertex to the "
        "middle of the opposite side. Here's a triangle, A B C. It doesn't have to be special. Not equilateral, not "
        "isosceles, just any triangle.", show(F3M['line'], "Here's a triangle")),
      L("Draw the median from A. It goes to D, the middle of B C, so B D and D C are equal.",
        show(F3M['med'], 'Draw the median from A')),
      L("Now we have two triangles, A B D and A D C. Their bases, B D and D C, are equal.",
        show(F3M['two'], 'Now we have two triangles')),
      L("And they have the same height. Drop the altitude from A to the line B C. This one altitude is the height of both "
        "triangles. For the triangle on the right, it falls outside, but that doesn't matter.",
        show(F3M['alt'], 'Drop the altitude from A')),
      L("Same base, same height, so the same area. For example, if B C is ten and the height is six, each half has a base of "
        "five, so its area is five times six over two, fifteen. And the whole triangle is ten times six over two, thirty, "
        "twice as much.", show(F3M['nums'], 'For example'), show(F3Ma, 'twice as much')),
      L("Careful, the same area doesn't mean the same shape. These two triangles look very different, and they're not "
        "congruent. Only their areas are equal.", pt('f3m_line', 'These two triangles look'))),
    S('Same base, same height',
      L("The same idea works when the top vertex moves along a line that's parallel to the base. Here the base is B C, and "
        "the dashed line is parallel to it.", show(F3P['line'], 'Here the base is B C')),
      L("Put the top vertex at the left, in the middle, or far to the right. The base stays the same, and the height is "
        "always the distance between the two parallel lines, so it doesn't change either. So all these triangles have the "
        "same area.", show(F3P['t1'], 'at the left'), show(F3P['t2'], 'in the middle'), show(F3P['t3'], 'far to the right'),
        show(F3Pa, 'So all these triangles')),
      L("So whenever you see a median, you automatically know that it cut the triangle into two triangles with equal areas. "
        "[pause] Okay. I'll see you in the next video.")),
])

# ------------------------------------------------------------------------------------------------ geo-019 (lesson: The Pythagorean Theorem)
# Hebrew (geo 852-870): a very important theorem, used all through geometry; Pythagoras and his followers (a kind of club
# that believed in mathematics); in every right triangle a² + b² = c² - the legs squared, the hypotenuse squared; only in a
# right triangle. Course additions kept: we square the sides, not the angles; find the right angle, then the hypotenuse;
# the legs can swap; add to find c, subtract to find a leg. Examples (new): 6, 8 -> 10; 13 and 5 -> 12; non-example 4, 5, 6.
# Squaring is explained in one line (exponents come later in the study plan). V3: the triangle with the right angle, the
# legs traced teal, the hypotenuse orange; each example on its own triangle, the calculation written on it, the found side
# written in last; the non-example with a red check.
_f3yB, _f3yA, _f3yC = (170, 250), (170, 70), (450, 250)
F3Y = GEO('f3y', [
    ('line', _f3tri(_f3yB, _f3yA, _f3yC) + [('right', 170, 250, 0, 90, 18)]),
    ('legs', [('seg', 170, 250, 170, 70, 'teal', 6), ('seg', 170, 250, 450, 250, 'teal', 6), ('txt', 142, 160, 'a', 'teal', 32, True),
              ('txt', 310, 282, 'b', 'teal', 32, True)]),
    ('hyp', [('seg', 170, 70, 450, 250, 'orange', 6), ('txt', 330, 138, 'c', 'orange', 32, True)]),
], vb='100 40 420 270', w=600, col=0, title='A right triangle: legs a and b, hypotenuse c')
F3Ya = I('f3ya', '$a^2+b^2=c^2$', size=44, col=1)
F3Yb = I('f3yb', '$6^2=6\\times6=36$', size=32, col=1)
_f3e = lambda w, h: [(150, 280), (150, 280 - h), (150 + w, 280)]
_f3e1 = _f3e(240, 180)
F3Y1 = GEO('f3y1', [
    ('line', _f3tri(*_f3e1) + [('right', 150, 280, 0, 90, 16), ('txt', 124, 190, '6', 'teal', 30), ('txt', 270, 312, '8', 'teal', 30),
                               ('txt', 284, 172, '?', 'orange', 34)]),
    ('c1', [('txt', 580, 120, '6² + 8²', 'ink', 30), ('txt', 580, 162, '= 36 + 64 = 100', 'ink', 30)]),
    ('c2', [('txt', 580, 220, '10 × 10 = 100', 'orange', 30)]),
    ('ans', [('seg', 150, 100, 390, 280, 'orange', 6), ('txt', 336, 168, '= 10', 'orange', 32)]),
], vb='90 50 600 290', w=600, col=0, title='Legs 6 and 8: the hypotenuse is 10')
_f3e2 = _f3e(240, 100)
F3Y2 = GEO('f3y2', [
    ('line', _f3tri(*_f3e2) + [('right', 150, 280, 0, 90, 16), ('txt', 124, 230, '5', 'teal', 30), ('txt', 286, 208, '13', 'orange', 30),
                               ('txt', 270, 312, '?', 'teal', 34)]),
    ('c1', [('txt', 560, 110, '13 × 13 = 169', 'ink', 28), ('txt', 560, 150, '169 − 25 = 144', 'ink', 28)]),
    ('c2', [('txt', 560, 200, '12 × 12 = 144', 'teal', 28)]),
    ('ans', [('seg', 150, 280, 390, 280, 'teal', 6), ('txt', 322, 312, '= 12', 'teal', 32)]),
], vb='90 60 590 280', w=600, col=0, title='Hypotenuse 13 and a leg of 5: the other leg is 12')
_f3nB, _f3nC, _f3nA = (160, 250), (400, 250), (250, 117.7)
F3N = GEO('f3n', [
    ('line', _f3tri(_f3nB, _f3nC, _f3nA) + [('txt', 190, 176, '4', 'ink', 30), ('txt', 342, 176, '5', 'ink', 30), ('txt', 280, 282, '6', 'ink', 30)]),
    ('no', [('txt', 520, 140, '4² + 5² = 16 + 25 = 41', 'red', 26), ('txt', 520, 180, '6² = 36   ✗', 'red', 26)]),
], vb='120 90 540 220', w=600, col=0, title='No right angle: the theorem does not hold')
F3Nc = I('f3nc', 'Find $c$: $\\ $add the squares\nFind a leg: $\\ $subtract', size=30, col=1)
video('geo-019', 'lesson', slides=[
    S('The Pythagorean Theorem',
      L("The Pythagorean theorem. It's a very important theorem, and we'll use it again and again, in almost every geometry "
        "topic on the exam."),
      L("Pythagoras was a Greek philosopher and mathematician who lived about two and a half thousand years ago. His followers "
        "were almost like a club that believed in mathematics. You can read about them sometime, it's a fascinating story. "
        "They proved many important things, and the most famous one is this theorem.")),
    S('The theorem',
      L("In a right triangle, the two sides that make the right angle are called the legs. The side across from the right "
        "angle is called the hypotenuse, and it's always the longest side.", show(F3Y['line'], 'In a right triangle'),
        show(F3Y['legs'], 'the two sides that make the right angle'), show(F3Y['hyp'], 'The side across from the right')),
      L("The theorem says: a squared plus b squared equals c squared. Squared means a number times itself, so six squared is "
        "six times six, which is thirty-six. In words: the first leg squared, plus the second leg squared, equals the "
        "hypotenuse squared. We square the sides, not the angles.", show(F3Ya, 'The theorem says'),
        show(F3Yb, 'so six squared is'))),
    S('Finding the hypotenuse',
      L("Let's try it. A right triangle has legs six and eight. How long is the hypotenuse?",
        show(F3Y1['line'], 'A right triangle has legs')),
      L("Six squared is thirty-six, and eight squared is sixty-four. Thirty-six plus sixty-four is a hundred. So the "
        "hypotenuse squared is a hundred.", show(F3Y1['c1'], 'Six squared is thirty-six')),
      L("Which number times itself gives a hundred? Ten, because ten times ten is a hundred. So the hypotenuse is ten. And "
        "it's longer than both legs, as it should be.", show(F3Y1['c2'], 'Which number times itself'),
        show(F3Y1['ans'], 'So the hypotenuse is ten'))),
    S('Finding a leg',
      L("Now the other way around. The hypotenuse is thirteen, and one leg is five. How long is the other leg?",
        show(F3Y2['line'], 'Now the other way around')),
      L("The legs squared add up to the hypotenuse squared, so to find a leg, we subtract. Thirteen squared is thirteen times "
        "thirteen: thirteen times ten is a hundred thirty, plus thirteen times three, thirty-nine, so a hundred sixty-nine. "
        "Five squared is twenty-five. A hundred sixty-nine minus twenty-five is a hundred forty-four.",
        show(F3Y2['c1'], 'Thirteen squared is')),
      L("Which number times itself gives a hundred forty-four? Twelve, because twelve times twelve is a hundred forty-four. "
        "So the other leg is twelve.", show(F3Y2['c2'], 'Which number times itself'), show(F3Y2['ans'], 'So the other leg is twelve'))),
    S('Only in a right triangle',
      L("But careful, this works only in a right triangle. Here's a triangle with sides four, five and six, and no right "
        "angle. Four squared plus five squared is sixteen plus twenty-five, which is forty-one. But six squared is "
        "thirty-six. They're not equal, so here the theorem doesn't hold.", show(F3N['line'], "Here's a triangle"),
        show(F3N['no'], 'Four squared plus')),
      L("So step one, find the right-angle mark. Step two, find the hypotenuse, the side across from the right angle. The two "
        "legs can swap places, because their squares are just added. But the hypotenuse stands alone on the other side. To "
        "find the hypotenuse, we add the squares, and to find a leg, we subtract.", show(F3Nc, 'To find the hypotenuse')),
      L("Next, we'll see sample questions. [pause] Okay. I'll see you in the next video.")),
])

# placement of the question videos' board (right column, below the question text)
for _f3g in (F3G, F3G2): _R(_f3g, 235)
_R(F3Q, 215)
for _f3it, _f3y in ((F3Ga, 490), (F3Gb, 590), (F3Qa, 425), (F3Qb, 478), (F3Wa, 380), (F3Wb, 470)): _R(_f3it, _f3y)

# =================================================================================================================
# Topic-31 fragment f4 (written 2026-10-14): the Pythagorean theorem in use - g020, g021, g022, q-r26-t31-03, the
# optional proof lesson geo-023, the triples lesson geo-024, g025. Hebrew: geo 869-1049 (three sample questions after the
# theorem's introduction, the proof "you don't need it", the triples lesson and its sample question).
# Placement: question figure on the left (FIG_LEFT), our colour copy and the steps in the right column (_R).
# Colours (Rule V3): the hypotenuse is always traced orange, the unknown side red, values found are written on the figure.
# =================================================================================================================
import math as _f4m

FIG_LEFT.update({'solve-geo31-g020', 'solve-geo31-g021', 'solve-geo31-g022', 'solve-geo31-g025'})


def f4_rt(A, B, C, labs, extra=()):
    """the base layer of a right triangle copy (right angle at B, A above B, C to the right of B): sides, right-angle mark,
    vertex letters, the question's side labels labs = [(x, y, text), ...]"""
    els = [('seg', A[0], A[1], B[0], B[1]), ('seg', B[0], B[1], C[0], C[1]), ('seg', A[0], A[1], C[0], C[1]),
           ('right', B[0], B[1], 0, 90, 18),
           ('txt', A[0] - 16, A[1] - 14, 'A', 'ink', 26, True), ('txt', B[0] - 18, B[1] + 16, 'B', 'ink', 26, True),
           ('txt', C[0] + 18, C[1] + 14, 'C', 'ink', 26, True)]
    els += [('txt', x, y, t, 'ink', 26) for x, y, t in labs]
    return els + list(extra)


def f4_qt(H, W, labs):
    """a compact right-triangle board copy for a question video: right angle at B, A above B, C right of B, the legs
    scaled to H (AB) and W (BC) svg units, in a 560 x 360 frame whose right part (x 300-560) holds the written steps.
    labs = (label on AB, label on BC, label on AC). -> (base elements, A, B, C, (x, y) of the AC label)"""
    A, B, C = (70, 60), (70, 60 + H), (70 + W, 60 + H)
    hl = ((A[0] + C[0]) / 2 + 18, (A[1] + C[1]) / 2 - 14)
    els = [('seg', A[0], A[1], B[0], B[1]), ('seg', B[0], B[1], C[0], C[1]), ('seg', A[0], A[1], C[0], C[1]),
           ('right', B[0], B[1], 0, 90, 16),
           ('txt', A[0] - 14, A[1] - 16, 'A', 'ink', 24, True), ('txt', B[0] - 16, B[1] + 16, 'B', 'ink', 24, True),
           ('txt', C[0] + 16, C[1] + 14, 'C', 'ink', 24, True),
           ('txt', A[0] - 26, (A[1] + B[1]) / 2, labs[0], 'ink', 24), ('txt', (B[0] + C[0]) / 2, B[1] + 24, labs[1], 'ink', 24),
           ('txt', hl[0], hl[1], labs[2], 'ink', 24)]
    return els, A, B, C, hl
_QX = 430          # the centre of the written steps


# ------------------------------------------------------------------------------------------------ geo31-g020 (Hebrew: the theorem's first sample question)
# Hebrew (geo 873-890): before solving, rule out the choices 3 and 4 - the hypotenuse is the longest side; then the
# theorem: 9 + 16 = 25, AC = 5. English numbers 20, 21 -> 29; the course adds 41 = 20 + 21 (two sides > third, taught in
# the camera lesson). R36: 29 squared shown as 29 times 30 minus 29.
_f4A0, _f4B0, _f4C0 = (197.36, 63.2), (197.36, 296.8), (442.64, 296.8)
_e, _A, _B, _C, _h = f4_qt(182, 191, ('20', '21', 'x'))
f4a = GEO('f4a', [
    ('line', _e),
    ('hyp', [('path', [_A, _C], 'orange', 9), ('txt', _QX, 110, 'AC: the hypotenuse', 'orange', 24),
             ('txt', _QX, 150, 'the longest side', 'orange', 24), ('txt', _QX, 200, 'AC > 21', 'orange', 30)]),
    ('k2', [('txt', _QX, 260, '41 = 20 + 21', 'red', 26), ('txt', _QX, 295, 'no triangle ✗', 'red', 26)]),
], vb='0 20 560 340', w=540, title='Right triangle ABC, right angle at B')
_e, _A, _B, _C, _h = f4_qt(182, 191, ('20', '21', 'x'))
f4b = GEO('f4b', [
    ('line', _e),
    ('th', [('txt', _QX, 110, 'AB² + BC² = AC²', 'ink', 28)]),
    ('sq', [('txt', _A[0] - 30, 178, '400', 'teal', 22), ('txt', 165, 292, '441', 'teal', 22),
            ('txt', _QX, 160, '400 + 441 = 841', 'ink', 28)]),
    ('res', [('path', [_A, _C], 'orange', 9), ('txt', _h[0] + 40, _h[1], '= 29', 'red', 26),
             ('txt', _QX, 210, '29 · 30 = 870', 'red', 26), ('txt', _QX, 250, '870 − 29 = 841', 'red', 26), ('txt', _QX, 300, 'AC = 29', 'red', 30)]),
], vb='0 20 560 340', w=540, title='Right triangle ABC: the theorem')
video('solve-geo31-g020', 'solution', qid='geo31-g020', slides=[
    SM('Method 1 · Rule out, then the theorem', 'Rule out first',
      L("Triangle A B C is a right triangle. Given: angle A B C is ninety degrees, A B is twenty centimeters, and B C is "
        "twenty-one centimeters. What is A C, in centimeters?", pt('stem', 'Triangle A B C', 'hl', 8.0), voice='calm', pause=0.5),
      L("The right angle is at B, and we need the side A C. [short pause] Before we calculate anything, let's look at the "
        "choices, because some of them can't be the answer at all. Then we'll find A C exactly, with the Pythagorean "
        "theorem.", pt('fig: x', 'we need the side A C')),
      L("[short pause] Which side is A C? It's the side across from the right angle, the side that doesn't touch B. So A C "
        "is the hypotenuse, and in a right triangle the hypotenuse is always the longest side. So A C must be longer than "
        "twenty and longer than twenty-one.", show(f4a['line'], 'Which side is A C'), show(f4a['hyp'], 'So A C is the hypotenuse')),
      L("So choice number three, twenty-one, and choice number four, twenty, are out. A C could be twenty-one and a little "
        "bit, but it can't be twenty-one or less.", mk('cross', 'choice 3', 'So choice number three'),
        mk('cross', 'choice 4', 'and choice number four, twenty, are out')),
      L("What about forty-one? That's twenty plus twenty-one. Remember, two sides of a triangle together are always longer "
        "than the third side. If A C were forty-one, the other two sides would lie flat on it, and there would be no room "
        "for a triangle. So choice number one is out too. Only twenty-nine is left, so choice number two is our answer.",
        show(f4a['k2'], "That's twenty plus twenty-one"), mk('cross', 'choice 1', 'So choice number one is out too'),
        mk('tick', 'choice 2', 'so choice number two is our answer'))),
    SM('Method 1 · Rule out, then the theorem', 'The theorem',
      L("[pause] Now let's also find A C with the theorem, because in most questions we can't rule out three choices. In a "
        "right triangle, leg squared plus leg squared equals the hypotenuse squared. Here the legs are A B and B C, so A B "
        "squared plus B C squared equals A C squared.", show(f4b['line'], "Now let's also find A C"), show(f4b['th'], 'so A B squared plus')),
      L("Twenty squared is four hundred, and twenty-one squared is four hundred forty-one. Four hundred plus four hundred "
        "forty-one is eight hundred forty-one. That's A C squared, not A C itself.", show(f4b['sq'], 'Twenty squared is four hundred')),
      L("To get A C, we take the root. Which number times itself is eight hundred forty-one? Thirty times thirty is nine "
        "hundred, a little too much. Try twenty-nine. Twenty-nine times thirty is eight hundred seventy, and twenty-nine "
        "less is eight hundred forty-one. So A C is twenty-nine. A length is positive, so we don't need the negative root. "
        "Choice number two again. [pause] Okay. I'll see you in the next question.", show(f4b['res'], 'Twenty-nine times thirty'), mk('tick', 'choice 2', 'Choice number two again'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g021 (Hebrew: the second sample question)
# Hebrew (geo 891-903): the same triangle, 4 + 9 = 13; not a round number - take the root of both sides, the root undoes
# the square, AC = root 13. English numbers 5, 7 -> root 74; the course adds a whole-number sense check (8 and 9).
_f4A1, _f4B1, _f4C1 = (156.48, 63.2), (156.48, 296.8), (483.52, 296.8)
_e, _A, _B, _C, _h = f4_qt(150, 210, ('5', '7', 'x'))
f4c = GEO('f4c', [
    ('line', _e),
    ('hyp', [('path', [_A, _C], 'orange', 9)]),
    ('th', [('txt', _QX, 90, 'AB² + BC² = AC²', 'ink', 28)]),
    ('sq', [('txt', _A[0] - 28, 162, '25', 'teal', 22), ('txt', 175, 262, '49', 'teal', 22), ('txt', _QX, 140, '25 + 49 = 74', 'ink', 28)]),
    ('res', [('txt', _h[0] + 46, _h[1], '= √74', 'red', 26), ('txt', _QX, 190, 'AC = √74', 'red', 30)]),
    ('chk', [('txt', _QX, 250, '64 < 74 < 81', 'teal', 26), ('txt', _QX, 290, '8 < √74 < 9', 'teal', 26)]),
], vb='0 20 560 300', w=540, title='Right triangle ABC, right angle at B')
video('solve-geo31-g021', 'solution', qid='geo31-g021', slides=[
    SM('The theorem', 'A root is a fine answer',
      L("Triangle A B C is a right triangle. Given: angle A B C is ninety degrees, A B is five centimeters, and B C is "
        "seven centimeters. What is A C, in centimeters?", pt('stem', 'Triangle A B C', 'hl', 8.0), voice='calm', pause=0.5),
      L("The same kind of triangle as before, with different numbers. The right angle is at B again, so A C, across from "
        "it, is the hypotenuse, and A B and B C are the legs. [short pause] We'll use the Pythagorean theorem.",
        show(f4c['line'], 'The same kind of triangle'), show(f4c['hyp'], 'is the hypotenuse')),
      L("[short pause] A B squared plus B C squared equals A C squared. Five squared is twenty-five, and seven squared is "
        "forty-nine. Twenty-five plus forty-nine is seventy-four. So A C squared is seventy-four.",
        show(f4c['th'], 'A B squared plus B C squared'), show(f4c['sq'], 'Five squared is twenty-five')),
      L("Last time we got a round number. Here we don't, and that's completely fine. We take the root of both sides. The "
        "root undoes the square, so A C is the square root of seventy-four. We leave it exactly like that. Choice number "
        "one is our answer.", show(f4c['res'], 'so A C is the square root'),
        mk('tick', 'choice 1', 'Choice number one is our answer')),
      L("A quick sense check. Eight squared is sixty-four and nine squared is eighty-one, so the root of seventy-four is "
        "between eight and nine. That's longer than each leg, as a hypotenuse should be, and shorter than five plus seven.",
        show(f4c['chk'], 'Eight squared is sixty-four')),
      L("The other choices are common mistakes. Twelve adds the lengths, not the squares. Seventy-four forgets the root. "
        "And the root of twenty-four subtracts the squares, as if we were looking for a leg. [pause] Okay. I'll see you in "
        "the next question.", mk('cross', 'choice 2', 'Twelve adds the lengths'), mk('cross', 'choice 4', 'Seventy-four forgets the root'),
        mk('cross', 'choice 3', 'And the root of twenty-four'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g022 (Hebrew: the third sample question)
# Hebrew (geo 905-922): a leg and the hypotenuse given - instead of adding, move a squared to the other side: hypotenuse
# squared minus one leg squared; 36 - 25 = 11, root 11; then "this is the base, a technique to master; next lessons:
# shortcuts (triples, special triangles); the next lesson is a proof - not required, warmly recommended".
# English numbers 7, 10 -> root 51; the traps 3 (lengths subtracted) and root 149 (BC treated as the hypotenuse).
_f4A2, _f4B2, _f4C2 = (200.84, 63.2), (200.84, 296.8), (439.16, 296.8)
_e, _A, _B, _C, _h = f4_qt(182, 186, ('7', 'x', '10'))
f4d = GEO('f4d', [
    ('line', _e),
    ('hyp', [('path', [_A, _C], 'orange', 9), ('path', [_B, _C], 'red', 9)]),
    ('th1', [('txt', _QX, 110, 'AB² + BC² = AC²', 'ink', 28)]),
    ('th2', [('txt', _QX, 160, 'BC² = AC² − AB²', 'ink', 28)]),
    ('sq', [('txt', _A[0] - 28, 178, '49', 'teal', 22), ('txt', _h[0] + 40, _h[1] - 4, '100', 'orange', 22), ('txt', _QX, 210, '100 − 49 = 51', 'ink', 28)]),
    ('res', [('txt', 163 + 52, 266, '= √51', 'red', 26), ('txt', _QX, 265, 'BC = √51', 'red', 30)]),
], vb='0 20 560 340', w=540, title='Right triangle ABC, right angle at B')
f4n4 = I('f4n4', 'Two sides known $\\to$ the third: $\\ $hypotenuse $a^2+b^2$, $\\ $leg $c^2-a^2$', size=26)
video('solve-geo31-g022', 'solution', qid='geo31-g022', slides=[
    SM('The theorem', 'Hypotenuse minus leg',
      L("Triangle A B C is a right triangle. Given: angle A B C is ninety degrees, A B is seven centimeters, and A C is ten "
        "centimeters. What is B C, in centimeters?", pt('stem', 'Triangle A B C', 'hl', 8.0), voice='calm', pause=0.5),
      L("Again a right triangle with the right angle at B. But this time we know a leg and the hypotenuse, and we need the "
        "other leg. A C is across from the right angle, so A C, ten, is the hypotenuse, and B C is a leg.",
        show(f4d['line'], 'Again a right triangle'), show(f4d['hyp'], 'so A C, ten, is the hypotenuse')),
      L("[short pause] The theorem is still the same: A B squared plus B C squared equals A C squared. We need B C "
        "squared, so we subtract A B squared from both sides. That leaves B C squared equals A C squared minus A B squared, "
        "the hypotenuse squared minus the other leg squared.", show(f4d['th1'], 'The theorem is still the same'),
        show(f4d['th2'], 'That leaves B C squared')),
      L("Ten squared is a hundred, and seven squared is forty-nine. A hundred minus forty-nine is fifty-one. So B C squared "
        "is fifty-one, and B C is the square root of fifty-one. Choice number four is our answer.",
        show(f4d['sq'], 'Ten squared is a hundred'), show(f4d['res'], 'and B C is the square root'),
        mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Careful, three is ten minus seven. We subtract the squares, not the lengths. And the root of a hundred forty-nine "
        "adds the squares, as if B C were the hypotenuse. But B C is a leg, so it must be shorter than ten.",
        mk('cross', 'choice 3', 'Careful, three is ten minus seven'), mk('cross', 'choice 1', 'And the root of a hundred forty-nine'))),
    SM('The theorem', 'What comes next',
      L("This is the base of the Pythagorean theorem. When two sides of a right triangle are known, we can always find "
        "the third. For the hypotenuse, we add the squares. For a leg, we subtract. It's a technique you really must "
        "master.", show(f4n4, 'For the hypotenuse')),
      L("Soon we'll learn shortcuts for it, Pythagorean triples and special right triangles. And there's a short lesson "
        "that proves the theorem. You don't have to watch it, but I warmly recommend it. [pause] Okay. I'll see you in the "
        "next question.")),
])

# ------------------------------------------------------------------------------------------------ q-r26-t31-03 (added: acute, right or obtuse from the sides)
# NEW: square the longest side and compare with the sum of the other two squares; why (V3 general shapes: the same two
# sides 6 and 7 with the angle between them closing / right / opening - the side across gets shorter / 85 / longer); the
# special angle is across from the longest side (side vs angle: the camera lesson). Trap: choice 4 (C touches AC).
def _f4hinge(bx, th, col, lab, ly):
    u = 18.0
    A = (bx + 6 * u, 190.0); C = (bx + 7 * u * _f4m.cos(_f4m.radians(th)), 190.0 - 7 * u * _f4m.sin(_f4m.radians(th)))
    els = [('seg', bx, 190, A[0], A[1]), ('seg', bx, 190, C[0], C[1]), ('seg', A[0], A[1], C[0], C[1], col, 5),
           ('txt', bx + 54, 212, '6', 'ink', 22), ('txt', (bx + C[0]) / 2 - 16, (190 + C[1]) / 2, '7', 'ink', 22),
           ('txt', (A[0] + C[0]) / 2 + 30, ly, lab, col, 22)]
    els += [('right', bx, 190, 0, 90, 14, 'teal')] if th == 90 else [('arc', bx, 190, 24, 0, th, 'large' if th > 90 else 'small')]
    return els
f4h = GEO('f4h', [
    ('line', _f4hinge(40, 90, 'ink', 'c² = 85', 112) + [('txt', 100, 245, 'ninety', 'ink', 20)]),
    ('ac', _f4hinge(290, 60, 'teal', 'c² < 85', 112) + [('txt', 350, 245, 'smaller', 'teal', 20)]),
    ('ob', _f4hinge(580, 120, 'orange', 'c² > 85', 92) + [('txt', 590, 245, 'bigger', 'orange', 20)]),
], vb='0 40 720 230', w=640, col=0, title='Sides 6 and 7 with the angle between them closing and opening')
f4p1 = I('f4p1', 'Longest side $c$:\n$c^2=a^2+b^2$: $\\ $right\n$c^2>a^2+b^2$: $\\ $obtuse\n$c^2<a^2+b^2$: $\\ $acute', size=28)
_f4tB = (200.0, 260.0); _f4tA = (344.0, 260.0)
_f4tC = (200 + 168 * _f4m.cos(_f4m.radians(100.29)), 260 - 168 * _f4m.sin(_f4m.radians(100.29)))
f4t = GEO('f4t', [
    ('line', [('seg', _f4tA[0], _f4tA[1], _f4tB[0], _f4tB[1]), ('seg', _f4tB[0], _f4tB[1], _f4tC[0], _f4tC[1]),
              ('seg', _f4tA[0], _f4tA[1], _f4tC[0], _f4tC[1]),
              ('txt', _f4tA[0] + 18, _f4tA[1] + 14, 'A', 'ink', 26, True), ('txt', _f4tB[0] - 18, _f4tB[1] + 14, 'B', 'ink', 26, True),
              ('txt', _f4tC[0] - 16, _f4tC[1] - 14, 'C', 'ink', 26, True), ('txt', 272, 284, '6', 'ink', 24),
              ('txt', 166, 180, '7', 'ink', 24), ('txt', 285, 160, '10', 'ink', 24)]),
    ('long', [('path', [_f4tA, _f4tC], 'orange', 9), ('txt', 560, 120, '10² = 100', 'orange', 30)]),
    ('oth', [('txt', 560, 170, '6² + 7² = 36 + 49 = 85', 'ink', 30)]),
    ('cmp', [('txt', 560, 220, '100 > 85  →  obtuse', 'red', 30)]),
    ('angB', [('wedge', _f4tB[0], _f4tB[1], 40, 0, 100.29, 'orange'), ('arc', _f4tB[0], _f4tB[1], 40, 0, 100.29, 'orange')]),
], vb='120 60 640 250', w=680, col=0, title='Triangle ABC with sides 6, 7 and 10')
video('solve-q-r26-t31-03', 'solution', qid='q-r26-t31-03', slides=[
    S('Compare the squares',
      L("In triangle A B C, A B is six centimeters, B C is seven centimeters, and A C is ten centimeters. Which of the "
        "following is true?", pt('stem', 'In triangle A B C', 'hl', 7.0), voice='calm', pause=0.5),
      L("We only have the three sides, with no figure and no angles. The choices ask if the triangle is acute, right or "
        "obtuse, and where the special angle is. [short pause] We'll compare the square of the longest side with the "
        "squares of the other two sides."),
      L("[short pause] First, why the squares? Take two sides, six and seven, joined at a corner, and look at the angle "
        "between them. When that angle is exactly ninety degrees, the side across from it is the hypotenuse, so its square "
        "is six squared plus seven squared, which is eighty-five.", show(f4h['line'], 'Take two sides, six and seven')),
      L("If the angle is smaller than ninety, the two sides close up, and the side across from it gets shorter. Its square "
        "is less than eighty-five. If the angle is bigger than ninety, the sides open wider, and the side across gets "
        "longer. Its square is more than eighty-five.", show(f4h['ac'], 'If the angle is smaller than ninety'),
        show(f4h['ob'], 'If the angle is bigger than ninety')),
      L("So we square the longest side and compare it with the other two squares added. Equal means a right angle. Bigger "
        "means an obtuse angle. Smaller means every angle is acute.", show(f4p1, 'So we square the longest side'))),
    S('Our triangle',
      L("The longest side here is A C, ten. Ten squared is a hundred. The other two, six squared plus seven squared, are "
        "thirty-six plus forty-nine, which is eighty-five.", show(f4t['line'], 'The longest side here'), show(f4t['long'], 'Ten squared is a hundred'),
        show(f4t['oth'], 'thirty-six plus forty-nine')),
      L("A hundred is more than eighty-five, so A C is too long for a right angle, and the angle across from A C is obtuse. "
        "So the triangle isn't acute and isn't right. Choice numbers one and two are out.", show(f4t['cmp'], 'A hundred is more than'),
        mk('cross', 'choice 1', 'Choice numbers one'), mk('cross', 'choice 2', 'and two are out')),
      L("Which angle is obtuse? The angle across from the longest side, at the corner that A C doesn't touch. A C goes from "
        "A to C, so the corner it doesn't touch is B. The obtuse angle is at B, and choice number three is our answer.",
        show(f4t['angB'], 'so the corner it doesn'), mk('tick', 'choice 3', 'and choice number three is our answer')),
      L("Choice number four is the trap. C is one end of A C, so it's next to the longest side, not across from it. "
        "[pause] Okay. I'll see you in the next question.", mk('cross', 'choice 4', 'Choice number four is the trap'))),
])

# ------------------------------------------------------------------------------------------------ geo-023 (lesson: Why Pythagoras Works - optional)
# Hebrew (geo 924-967): "not a lesson you must know, a short enrichment": the geometric meaning (the squares on the
# sides), seeing it (her animation moves the cut squares onto the hypotenuse square; here: the same four triangles
# rearranged in one big square), and the algebra: the big square = c squared + 4 ab/2 = (a + b) squared -> 2ab cancels.
def _f4sq(P, Q, side):
    """the square on segment P->Q, on the left of the direction P->Q (side=1) or the right (side=-1) -> polygon points"""
    dx, dy = Q[0] - P[0], Q[1] - P[1]; nx, ny = dy * side, -dx * side
    return [P, Q, (Q[0] + nx, Q[1] + ny), (P[0] + nx, P[1] + ny)]
_f4pB = (300.0, 220.0); _f4pA = (300.0, 130.0); _f4pC = (420.0, 220.0)       # legs a = 3, b = 4 (30 px), c = 5
_f4qa, _f4qb, _f4qc = _f4sq(_f4pA, _f4pB, -1), _f4sq(_f4pB, _f4pC, -1), _f4sq(_f4pC, _f4pA, -1)
def _f4poly(pts, col, w=3):
    return [('seg', pts[i][0], pts[i][1], pts[(i + 1) % 4][0], pts[(i + 1) % 4][1], col, w) for i in range(4)]
f4v = GEO('f4v', [
    ('line', [('seg', _f4pA[0], _f4pA[1], _f4pB[0], _f4pB[1]), ('seg', _f4pB[0], _f4pB[1], _f4pC[0], _f4pC[1]),
              ('seg', _f4pA[0], _f4pA[1], _f4pC[0], _f4pC[1]), ('right', _f4pB[0], _f4pB[1], 0, 90, 14),
              ('txt', 318, 175, 'a', 'ink', 26, True), ('txt', 360, 205, 'b', 'ink', 26, True), ('txt', 372, 165, 'c', 'ink', 26, True)]),
    ('sa', [('tint', _f4qa, 'teal')] + _f4poly(_f4qa, 'teal') + [('txt', 255, 175, 'a²', 'teal', 30)]),
    ('sb', [('tint', _f4qb, 'orange')] + _f4poly(_f4qb, 'orange') + [('txt', 360, 280, 'b²', 'orange', 30)]),
    ('sc', [('tint', _f4qc, 'red')] + _f4poly(_f4qc, 'red') + [('txt', 450, 118, 'c²', 'red', 30)]),
], vb='190 0 340 350', w=470, col=1, title='The squares on the sides of a right triangle')
_S0 = 280.0
def _f4big(ox, oy, kind):
    """the big square (side a + b = 7 units of 40 px) with four copies of the triangle: kind 'c' (a tilted square left
    in the middle) or 'ab' (two squares a and b left)"""
    P = lambda x, y: (ox + x, oy + y)
    sq = [('seg', ox, oy, ox + _S0, oy), ('seg', ox + _S0, oy, ox + _S0, oy + _S0), ('seg', ox + _S0, oy + _S0, ox, oy + _S0),
          ('seg', ox, oy + _S0, ox, oy)]
    if kind == 'c':
        tris = [[P(0, 0), P(120, 0), P(0, 160)], [P(120, 0), P(280, 0), P(280, 120)], [P(280, 120), P(280, 280), P(160, 280)],
                [P(160, 280), P(0, 280), P(0, 160)]]
        holes = [('tint', [P(120, 0), P(280, 120), P(160, 280), P(0, 160)], 'red'), ('txt', ox + 140, oy + 140, 'c²', 'red', 34)]
    else:
        tris = [[P(120, 0), P(280, 0), P(120, 120)], [P(280, 0), P(280, 120), P(120, 120)], [P(0, 120), P(120, 120), P(0, 280)],
                [P(120, 120), P(120, 280), P(0, 280)]]
        holes = [('tint', [P(0, 0), P(120, 0), P(120, 120), P(0, 120)], 'teal'), ('txt', ox + 60, oy + 60, 'a²', 'teal', 30),
                 ('tint', [P(120, 120), P(280, 120), P(280, 280), P(120, 280)], 'orange'), ('txt', ox + 200, oy + 200, 'b²', 'orange', 34)]
    tri = []
    for t in tris:
        tri += [('tint', t, 'ink')] + [('seg', t[i][0], t[i][1], t[(i + 1) % 3][0], t[(i + 1) % 3][1], 'ink', 2.5) for i in range(3)]
    return sq, tri, holes
_b1 = _f4big(30, 20, 'c'); _b2 = _f4big(380, 20, 'ab')
f4w = GEO('f4w', [
    ('line', _b1[0]), ('t1', _b1[1]), ('h1', _b1[2]),
    ('sq2', _b2[0] + [('txt', 345, 160, '→', 'ink', 40)]), ('t2', _b2[1]), ('h2', _b2[2]),
], vb='10 0 680 320', w=900, col=0, title='Four copies of the triangle in a big square, two ways')
_b3 = _f4big(40, 30, 'c')
f4x = GEO('f4x', [
    ('line', _b3[0] + _b3[1] + _b3[2] + [('txt', 100, 18, 'a', 'ink', 26, True), ('txt', 240, 18, 'b', 'ink', 26, True),
                                         ('txt', 26, 100, 'b', 'ink', 26, True), ('txt', 26, 250, 'a', 'ink', 26, True),
                                         ('seg', 40, 330, 320, 330, 'teal', 5), ('txt', 180, 350, 'side a + b', 'teal', 26)]),
], vb='0 0 360 365', w=330, col=1, title='The big square: side a + b')
f4r0 = I('f4r0', '$3^2+4^2=9+16=25=5^2$', size=30)
f4r1 = I('f4r1', 'Area $=c^2+4\\cdot\\frac{ab}{2}$', size=32, col=0)
f4r2 = I('f4r2', 'Area $=(a+b)^2$', size=32, col=0)
f4r3 = I('f4r3', '$a^2+2ab+b^2=c^2+2ab$', size=32, col=0)
f4r4 = I('f4r4', '$a^2+b^2=c^2$', size=36, col=0)
video('geo-023', 'lesson', slides=[
    S('Why Pythagoras Works',
      L("A proof of the Pythagorean theorem, just for interest.")),
    S('Only if you are curious',
      L("As I said, you don't need this for the exam. You won't be asked to prove the theorem. This is a short extra "
        "lesson, if you're curious: what the theorem says about areas, and a simple proof. If you prefer, you can skip to "
        "the next video.")),
    S('What a squared means',
      L("First, what is a squared in a picture? It's the area of a square whose side is a. So let's put a square on leg a. "
        "Its area is a squared. In the same way, a square on leg b has area b squared, and a square on the hypotenuse c has "
        "area c squared.", show(f4v['line'], 'First, what is a squared'), show(f4v['sa'], "So let's put a square on leg a"),
        show(f4v['sb'], 'a square on leg b'), show(f4v['sc'], 'a square on the hypotenuse c')),
      L("So the theorem says that the two squares on the legs together have exactly the same area as the square on the "
        "hypotenuse. With legs three and four and hypotenuse five, nine plus sixteen is twenty-five.",
        show(f4r0, 'With legs three and four'))),
    S('See it',
      L("Now let's see why. Take a big square, and put four copies of our right triangle in its corners. Their hypotenuses "
        "make a tilted square in the middle. The part the triangles don't cover is that middle square, c squared.",
        show(f4w['line'], 'Take a big square'), show(f4w['t1'], 'put four copies'), show(f4w['h1'], "The part the triangles don't cover")),
      L("Now take the same big square, and move the same four triangles into new places, two at the top right and two at "
        "the bottom left. Now the part they don't cover is a square with side a and a square with side b.",
        show(f4w['sq2'], 'Now take the same big square'), show(f4w['t2'], 'move the same four triangles'),
        show(f4w['h2'], "Now the part they don't cover")),
      L("The big square didn't change, and the four triangles didn't change. So the part they leave uncovered has the same "
        "area both times. a squared plus b squared equals c squared. That's the picture. Now let's write it with areas.",
        pt('f4w_line', 'So the part they leave uncovered'))),
    S('With areas',
      L("Look at the first picture again. The big square is made of the middle square, c squared, and four triangles around it. Each "
        "one is a right triangle, so its area is leg times leg over two, which is a b over two.",
        show(f4x['line'], 'Look at the first picture again'), show(f4r1, 'and four triangles around it')),
      L("But the big square also has its own area formula, side times side. Its side is a plus b, so its area is the "
        "bracket a plus b, squared.", pt('f4x_line', 'Its side is a plus b'), show(f4r2, 'so its area is the')),
      L("Both describe the same area, so they're equal. Open the bracket: a squared plus two a b plus b squared. On the "
        "other side, four times a b over two is two a b. Two a b is on both sides, so it cancels, and we're left with a "
        "squared plus b squared equals c squared. That's the theorem, and it was simpler than you thought. [pause] Okay. "
        "I'll see you in the next video.", show(f4r3, 'Open the bracket'), show(f4r4, "and we're left with"))),
])

# ------------------------------------------------------------------------------------------------ geo-024 (lesson: Pythagorean Triples)
# Hebrew (geo 970-1015): whole numbers that fit; 3-4-5 (5 the hypotenuse, the longest side), 5-12-13; rare - most pairs give
# a root (her 1, 2 -> root 5; here 2, 5 -> root 29); the exam loves them; 8-15-17 very rare, no need; a RATIO - scale it
# (her x2 and x3; here x7 and 5-12-13 x3), the longest side is always the hypotenuse; how to remember: 3, 4, 5 in a row,
# 5-12-13 "hamsa, bat mitzvah, bar mitzvah" -> the approved English "high five, a dozen, and one more".
# Course additions kept: why scaling works (k squared), the position trap (27, 36).
def _f4tri(B, a, b, u, labs, col='ink'):
    A = (B[0], B[1] - a * u); C = (B[0] + b * u, B[1])
    return [('seg', A[0], A[1], B[0], B[1], col), ('seg', B[0], B[1], C[0], C[1], col), ('seg', A[0], A[1], C[0], C[1], col),
            ('right', B[0], B[1], 0, 90, 12),
            ('txt', B[0] - 20, (A[1] + B[1]) / 2, labs[0], 'ink', 24), ('txt', (B[0] + C[0]) / 2, B[1] + 22, labs[1], 'ink', 24),
            ('txt', (A[0] + C[0]) / 2 + 22, (A[1] + B[1]) / 2 - 12, labs[2], 'orange', 24)]
f4y = GEO('f4y', [
    ('line', _f4tri((60, 230), 3, 4, 30, ('3', '4', '5')) + [('txt', 140, 290, '9 + 16 = 25', 'ink', 26)]),
    ('t2', _f4tri((300, 230), 5, 12, 22, ('5', '12', '13')) + [('txt', 450, 290, '25 + 144 = 169', 'ink', 26)]),
], vb='20 90 620 220', w=860, col=0, title='The triples 3, 4, 5 and 5, 12, 13')
f4z = GEO('f4z', [
    ('line', _f4tri((60, 270), 3, 4, 20, ('3', '4', '5'))),
    ('big', _f4tri((260, 270), 3, 4, 50, ('21', '28', '35'), 'teal') + [('txt', 200, 245, '× 7', 'teal', 30)]),
], vb='20 100 520 205', w=700, col=0, title='The same shape, every side times 7')
f4u = GEO('f4u', [
    ('line', _f4tri((60, 250), 3, 4, 34, ('27', '36', '45')) + [('txt', 140, 50, 'legs 27 and 36', 'teal', 24)]),
    ('bad', [('seg', 420, 250, 420, 100), ('seg', 420, 250, 560, 250), ('seg', 420, 100, 560, 250), ('right', 420, 250, 0, 90, 12),
             ('txt', 400, 175, '27', 'ink', 24), ('txt', 515, 165, '36', 'orange', 24), ('txt', 470, 50, 'hypotenuse 36', 'red', 24),
             ('txt', 490, 290, 'not 3 : 4 : 5', 'red', 24)]),
], vb='20 30 600 280', w=760, col=0, title='Where are the 27 and the 36?')
f4s3 = I('f4s3', 'Legs $2$ and $5$: $\\ 4+25=29$ $\\to$ hypotenuse $\\sqrt{29}$', size=30)
f4s4 = I('f4s4', 'On the exam: $\\ 3:4:5$ $\\quad 5:12:13$', size=32)
f4s5 = I('f4s5', '$3:4:5\\ =\\ 21:28:35$ $\\quad 5:12:13\\ =\\ 15:36:39$', size=30)
f4s6 = I('f4s6', '$(3k)^2+(4k)^2=9k^2+16k^2=25k^2=(5k)^2$', size=30)
f4s7 = I('f4s7', 'Half: $\\ 1.5:2:2.5$', size=30)
f4s8 = I('f4s8', '$3,\\ 4,\\ 5$: in a row $\\quad 5,\\ 12,\\ 13$: high five, a dozen, one more', size=28)
video('geo-024', 'lesson', slides=[
    S('Pythagorean Triples',
      L("Pythagorean triples, a shortcut for the Pythagorean theorem when all the sides are whole numbers.")),
    S('What a triple is',
      L("A Pythagorean triple is three whole numbers that fit the theorem, a squared plus b squared equals c squared. The "
        "best-known one is three, four and five. Five is the hypotenuse, because the hypotenuse is always the longest side. "
        "Three squared plus four squared is nine plus sixteen, which is twenty-five, and five squared is twenty-five. It "
        "works.", show(f4y['line'], 'The best-known one')),
      L("Another triple that shows up on the exam is five, twelve and thirteen. Five squared plus twelve squared is "
        "twenty-five plus a hundred forty-four, which is a hundred sixty-nine, and thirteen squared is a hundred sixty-nine. "
        "It works too.", show(f4y['t2'], 'Another triple')),
      L("This is quite rare. Most pairs of legs don't give a whole hypotenuse. Legs two and five give four plus "
        "twenty-five, which is twenty-nine, so the hypotenuse is the root of twenty-nine. Almost any pair gives a root "
        "somewhere, in a leg or in the hypotenuse. That's a fine answer, so don't force a whole number.",
        show(f4s3, 'Legs two and five')),
      L("That's exactly why the exam loves triples. Everything stays whole, with no messy roots. Most of the time, the exam "
        "uses these two triples: three, four, five, and five, twelve, thirteen. There are others, like eight, fifteen and "
        "seventeen, but they're very rare, so don't bother learning them. If one shows up, the ordinary theorem still "
        "works.", show(f4s4, 'the exam uses these two'))),
    S('A ratio',
      L("A triple is really a ratio of the sides, three to four to five. A ratio means we can multiply all three sides by "
        "the same number, and it still works. Multiply three, four and five by seven: twenty-one, twenty-eight and "
        "thirty-five. It's the same shape, just bigger, so it's also a right triangle.",
        show(f4z['line'], 'A triple is really a ratio'), show(f4z['big'], 'Multiply three, four and five by seven'), show(f4s5, 'It\'s the same shape')),
      L("In the same way, five, twelve, thirteen times three is fifteen, thirty-six and thirty-nine. We can multiply by "
        "two, by four, by ten, and it always works, as long as the same number multiplies all three sides. And the longest "
        "side is always the hypotenuse.", pt('f4s5', 'five, twelve, thirteen times three')),
      L("Why does it work? Multiply every side by some number k. Then every square is multiplied by k squared: nine k "
        "squared plus sixteen k squared is twenty-five k squared. So any positive number works, even a half. Half of three, "
        "four, five is one and a half, two, and two and a half.", show(f4s6, 'Then every square is multiplied'),
        show(f4s7, 'Half of three'))),
    S('How to remember',
      L("How do we remember them? Three, four, five is easy, three numbers in a row. For five, twelve, thirteen: high "
        "five, a dozen, and one more. Give me a high five, that's five. A dozen, like a box of eggs, that's twelve. And "
        "one more, thirteen.", show(f4s8, 'How do we remember them'))),
    S('Match the positions',
      L("One trap. In a right triangle, you see twenty-seven and thirty-six. If both of them are legs, that's three and "
        "four, times nine, so the hypotenuse is five times nine, which is forty-five.", show(f4u['line'], 'If both of them are legs')),
      L("But if thirty-six is the hypotenuse, the numbers aren't in the same places as three, four, five, and the triple "
        "doesn't fit. So first find the right angle, then match the triple. [pause] Okay. I'll see you in the next video.",
        show(f4u['bad'], 'But if thirty-six is the hypotenuse'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g025 (Hebrew: the triples sample question)
# Hebrew (geo 1020-1049): triangle by triangle - ABC: a leg and the hypotenuse, 5-12-13 noticed instead of the theorem;
# ACE: 9 and 12 "should jump out" -> 3-4-5 times 3; CED: 15 and 15, no triple - "there's something, we'll learn it soon",
# so the theorem: 2 times 225, root -> 15 root 2. English numbers 15, 39, 48, 60 -> 60 root 2.
# V3: FOCUS on one triangle at a time (the rest dimmed, the triangle tinted), each found side written on the figure.
# (The course's extra "full Pythagoras all the way" check is not kept: it needs 39 squared, 48 squared, beyond exam
# mental math - R36; the triples are exactly what saves that work, and that is said.)
_gA, _gB, _gC, _gE, _gD = (190, 80), (122.5, 80), (190, 242), (406, 80), (568, 296)
_g25lines = [('seg', _gB[0], _gB[1], _gA[0], _gA[1]), ('seg', _gA[0], _gA[1], _gC[0], _gC[1]), ('seg', _gB[0], _gB[1], _gC[0], _gC[1]),
             ('seg', _gA[0], _gA[1], _gE[0], _gE[1]), ('seg', _gC[0], _gC[1], _gE[0], _gE[1]), ('seg', _gE[0], _gE[1], _gD[0], _gD[1]),
             ('seg', _gC[0], _gC[1], _gD[0], _gD[1]), ('right', 190, 80, 180, 270, 12), ('right', 190, 80, 270, 0, 12),
             ('right', 406, 80, gdir(406, 80, 190, 242), gdir(406, 80, 568, 296), 12),
             ('txt', 184, 58, 'A', 'ink', 24, True), ('txt', 104, 70, 'B', 'ink', 24, True), ('txt', 176, 264, 'C', 'ink', 24, True),
             ('txt', 406, 58, 'E', 'ink', 24, True), ('txt', 586, 306, 'D', 'ink', 24, True)]
_g25giv = [('txt', 156, 62, '15', 'ink', 22), ('txt', 134, 172, '39', 'ink', 22), ('txt', 298, 62, '48', 'ink', 22),
           ('txt', 508, 176, '60', 'ink', 22), ('txt', 376, 292, 'x', 'ink', 22)]
_v36 = ('txt', 214, 165, '36', 'teal', 26)
_v60 = ('txt', 314, 182, '60', 'teal', 26)
def _f4focus(tri, vals):
    return ([('dim', 80, 30, 540, 300)] + [('seg', tri[i][0], tri[i][1], tri[(i + 1) % 3][0], tri[(i + 1) % 3][1], 'ink', 4) for i in range(3)]
            + [('tint', tri, 'teal')] + vals)
f4g = GEO('f4g', [
    ('line', _g25lines + _g25giv),
    ('abc', _f4focus([_gA, _gB, _gC], [('txt', 156, 62, '15', 'ink', 22), ('txt', 134, 172, '39', 'ink', 22),
                                         ('txt', 184, 58, 'A', 'ink', 24, True), ('txt', 104, 70, 'B', 'ink', 24, True), ('txt', 176, 264, 'C', 'ink', 24, True)])),
    ('abcz', [('dim', 380, 40, 250, 300), ('dim', 380, 40, 250, 300), ('dim', 380, 40, 250, 300),
              ('tint', [(538.0, 62.0), (430.0, 62.0), (538.0, 321.2)], 'teal'),
              ('seg', 430.0, 62.0, 538.0, 62.0, 'ink', 4), ('seg', 538.0, 62.0, 538.0, 321.2, 'ink', 4), ('seg', 430.0, 62.0, 538.0, 321.2, 'ink', 4),
              ('right', 538.0, 62.0, 180, 270, 16), ('txt', 544.0, 42.0, 'A', 'ink', 26, True), ('txt', 412.0, 54.0, 'B', 'ink', 26, True),
              ('txt', 558.0, 327.2, 'C', 'ink', 26, True), ('txt', 484.0, 46.0, '15', 'ink', 26), ('txt', 462.0, 197.6, '39', 'ink', 26)]),
    ('t1', [('txt', 225, 360, '15 = 5·3,  39 = 13·3', 'teal', 21)]),
    ('ac', [_v36, ('txt', 564.0, 191.6, '36', 'teal', 28), ('txt', 225, 395, 'AC = 12·3 = 36', 'teal', 21)]),
    ('ace', [('dim', 380, 40, 250, 300)] * 3 + _f4focus([_gA, _gC, _gE], [_v36, ('txt', 298, 62, '48', 'ink', 22), ('txt', 184, 58, 'A', 'ink', 24, True),
                                        ('txt', 176, 264, 'C', 'ink', 24, True), ('txt', 406, 58, 'E', 'ink', 24, True)])
             + [('txt', 225, 360, '15 = 5·3,  39 = 13·3', 'teal', 21), ('txt', 225, 395, 'AC = 12·3 = 36', 'teal', 21)]),
    ('t2', [('txt', 495, 360, '36 = 3·12,  48 = 4·12', 'teal', 21)]),
    ('ce', [_v60, ('txt', 495, 395, 'CE = 5·12 = 60', 'teal', 21)]),
], vb='90 40 540 375', w=540, title='Three right triangles in a chain')
f4g2 = GEO('f4g2', [
    ('line', _g25lines + _g25giv + [_v36, _v60]),
    ('ced', _f4focus([_gC, _gE, _gD], [_v60, ('txt', 508, 176, '60', 'ink', 22), ('txt', 176, 264, 'C', 'ink', 24, True),
                                        ('txt', 406, 58, 'E', 'ink', 24, True), ('txt', 586, 306, 'D', 'ink', 24, True),
                                        ('path', [_gC, _gD], 'red', 7)])),
    ('eq', [('txt', 360, 360, 'CD² = 60² + 60² = 2 · 60²', 'ink', 24)]),
    ('cd', [('txt', 400, 322, '= 60√2', 'red', 24), ('txt', 360, 398, 'CD = 60√2', 'red', 26)]),
], vb='90 40 540 375', w=540, title='Three right triangles: the last one')
video('solve-geo31-g025', 'solution', qid='geo31-g025', slides=[
    SM('Triangle by triangle', 'Triangle by triangle',
      L("The accompanying figure shows three right triangles. The marked side lengths are in centimeters. What is C D, in "
        "centimeters?", pt('stem', 'The accompanying figure', 'hl', 6.0), voice='calm', pause=0.5),
      L("Three right triangles, one next to the other, and we need C D, the bottom side. [short pause] We'll go triangle "
        "by triangle, and each one gives us a side for the next one.", pt('fig: x', 'and we need C D')),
      L("[short pause] Start with triangle A B C. The right angle is at A, so B C, thirty-nine, is the hypotenuse, and A B, "
        "fifteen, is a leg. We could use the theorem, thirty-nine squared minus fifteen squared. But look at the numbers. "
        "Fifteen is five times three, and thirty-nine is thirteen times three. That's the triple five, twelve, thirteen, "
        "times three. So A C is twelve times three, which is thirty-six.", show(f4g['line'], 'Start with triangle A B C'),
        show(f4g['abc'], 'The right angle is at A'), show(f4g['abcz'], 'We could use the theorem'), show(f4g['t1'], 'Fifteen is five times three'), show(f4g['ac'], 'So A C is twelve times three')),
      L("Now triangle A C E. It's also right-angled at A, with legs A C, thirty-six, and A E, forty-eight. After some "
        "practice, these numbers jump out. Thirty-six is three times twelve, and forty-eight is four times twelve. That's "
        "three, four, five, times twelve. So the hypotenuse C E is five times twelve, which is sixty.",
        show(f4g['ace'], 'Now triangle A C E'), show(f4g['t2'], 'Thirty-six is three times twelve'), show(f4g['ce'], 'So the hypotenuse C E'))),
    SM('Triangle by triangle', 'The last triangle',
      L("Now triangle C E D. The right angle is at E, and both legs are sixty. Sixty and sixty aren't in a triple. There "
        "is a shortcut for this kind of triangle, and we'll learn it soon. For now, the theorem: C D squared is sixty "
        "squared plus sixty squared.", show(f4g2['line'], 'Now triangle C E D'), show(f4g2['ced'], 'The right angle is at E'), show(f4g2['eq'], 'For now, the theorem')),
      L("Instead of adding it up, I write it as two times sixty squared, because I know the root will be simpler. The root "
        "of two times sixty squared is the root of two, times sixty. So C D is sixty root two, and choice number three is "
        "our answer.", show(f4g2['cd'], 'So C D is sixty root two'),
        mk('tick', 'choice 3', 'and choice number three is our answer')),
      L("Without the triples, we'd have to square numbers like thirty-nine and forty-eight. Noticing the triples saved all "
        "of that. [pause] Okay. I'll see you in the next question.", pt('f4g2_line', 'Without the triples'))),
])

# placement (right column, question videos)
for _g in (f4a, f4b, f4c, f4d, f4g, f4g2): _R(_g, 200)
_R(f4n4, 250)
_R(f4p1, 345, x=1110)

# =================================================================================================================
# Topic-31 fragment f5: the special right triangles. geo-026 (the 30-60-90 "gold" triangle), solve-geo31-g027,
# geo-017-after (the equilateral triangle's area), solve-geo31-g018, geo-027-after (the 45-45-90 "silver" triangle),
# solve-geo31-g028. Written 2026-10-14. Hebrew: geo 758-830 (the equilateral area, Pythagoras for the height, the
# "a-two-three-four" folk-dance count, the perimeter-6 question), geo 1053-1189 (gold and silver: the equilateral cut in
# two, Pythagoras for the long leg, the ratio, "one side is enough", the long-leg trap, dividing by a root, the two sample
# questions, the borekas). Numbers are the course's new ones. Roots stay exact (no decimal estimates).
# Colours (V3): the short leg / 30° teal, the long leg / 60° orange, a wrong step red, the triangle under study tinted teal.
# =================================================================================================================
import math as _f5m

_F5R3 = _f5m.sqrt(3)


def _f5lab(p, q, t, off=24, col='ink', size=26, side=1):
    """a side label at the middle of p-q, pushed off the side (side=1: to the left of p->q, -1: to the right)"""
    mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
    L = _f5m.hypot(q[0] - p[0], q[1] - p[1]); nx, ny = (q[1] - p[1]) / L * side, -(q[0] - p[0]) / L * side
    return ('txt', mx + nx * off, my + ny * off, t, col, size)


def _f5tri(a, b, c, col='ink', w=3):
    return [('seg', a[0], a[1], b[0], b[1], col, w), ('seg', b[0], b[1], c[0], c[1], col, w), ('seg', c[0], c[1], a[0], a[1], col, w)]


# ------------------------------------------------------------------------------------------------ geo-026 (lesson: the 30-60-90 triangle)
# Hebrew (geo 1053-1125): the gold triangle from school, cut an equilateral triangle with side 2a, the altitude is also a
# median, the half has 90, 60 and 30; Pythagoras gives the long leg a root 3 (the 2 is squared too!); the ratio a, a root 3,
# 2a; the short leg is half the hypotenuse; times root 3 / divided by root 3; one side is enough (vs Pythagoras: two
# sides); drills; the long-leg trap (1 opposite 60); dividing by a root (ignore the root, divide, attach it back). Course
# additions kept: the root that cancels, the 30-30-120 triangle (two gold halves) and its area.
# V3: the equilateral triangle built, the altitude drawn from the top after the top is pointed at, one half tinted INSIDE
# the triangle, then the same half (same tint, same labels) enlarged on its own; drills on two triangles turned
# differently (find the sides by the angles, not by how it's turned); the 30-30-120 triangle cut by its altitude.
_f5A, _f5B, _f5C, _f5D = (320.0, 30.2), (170.0, 290.0), (470.0, 290.0), (320.0, 290.0)
F5EQ = GEO('f5eq', [
    ('line', _f5tri(_f5A, _f5B, _f5C) + [('txt', 320, 12, 'A', 'ink', 26, True), ('txt', 150, 305, 'B', 'ink', 26, True),
                                          ('txt', 490, 305, 'C', 'ink', 26, True)]),
    ('side', [_f5lab(_f5B, _f5A, '2a', 26), _f5lab(_f5A, _f5C, '2a', 26),
              ('tick', _f5A[0], _f5A[1], _f5B[0], _f5B[1]), ('tick', _f5A[0], _f5A[1], _f5C[0], _f5C[1]), ('tick', _f5B[0], _f5B[1], _f5C[0], _f5C[1])]),
    ('top', [('dot', _f5A[0], _f5A[1])]),
    ('alt', [('seg', _f5A[0], _f5A[1], _f5D[0], _f5D[1], 'teal', 3, True), ('right', _f5D[0], _f5D[1], 0, 90, 16),
             ('txt', 334, 312, 'D', 'ink', 26, True), ('txt', 245, 314, 'a', 'teal', 28, True), ('txt', 395, 314, 'a', 'teal', 28, True)]),
    ('half', [('tint', [_f5A, _f5D, _f5C], 'teal'), ('arc', _f5C[0], _f5C[1], 40, 120, 180, 'large', '60°', 66),
              ('arc', _f5A[0], _f5A[1], 48, 270, 300, 'small', '30°', 74)]),
], vb='110 0 420 330', w=560, col=0, title='An equilateral triangle cut by its altitude')
# the half, enlarged: D (right angle), C (60), A (30). Short leg DC = a, hypotenuse CA = 2a, long leg AD = a root 3.
_f5d, _f5c, _f5a = (200.0, 320.0), (200.0 + 173.2, 320.0), (200.0, 20.0)
_f5half = [('tint', [_f5a, _f5d, _f5c], 'teal')] + _f5tri(_f5a, _f5d, _f5c) + [
    ('right', _f5d[0], _f5d[1], 0, 90, 18), ('arc', _f5c[0], _f5c[1], 36, 120, 180, 'large', '60°', 62),
    ('arc', _f5a[0], _f5a[1], 50, 270, 300, 'small', '30°', 76), ('txt', 200, 4, 'A', 'ink', 26, True),
    ('txt', 182, 338, 'D', 'ink', 26, True), ('txt', 390, 338, 'C', 'ink', 26, True)]
F5HALF = GEO('f5half', [
    ('line', _f5half + [_f5lab(_f5d, _f5c, 'a', 22, 'small', 28, -1), _f5lab(_f5a, _f5c, '2a', 28, 'ink', 28, -1)]),
    ('q', [('seg', _f5a[0], _f5a[1], _f5d[0], _f5d[1], 'red', 6), ('txt', 168, 170, '?', 'red', 30)]),
    ('e1', [('txt', 640, 120, '(2a)² − a² = 4a² − a² = 3a²', 'ink', 30)]),
    ('e2', [('txt', 640, 190, 'long leg = √(3a²) = a√3', 'large', 30)]),
    ('res', [('txt', 140, 210, 'a√3', 'large', 30)]),
], vb='100 -15 840 370', w=1000, col=0, title='The half: a 30-60-90 triangle')
F5RAT = GEO('f5rat', [
    ('line', _f5tri(_f5a, _f5d, _f5c) + [('right', _f5d[0], _f5d[1], 0, 90, 18), ('txt', 200, 4, 'A', 'ink', 26, True),
                                         ('txt', 182, 338, 'D', 'ink', 26, True), ('txt', 390, 338, 'C', 'ink', 26, True)]),
    ('s', [('seg', _f5d[0], _f5d[1], _f5c[0], _f5c[1], 'small', 7), ('arc', _f5a[0], _f5a[1], 50, 270, 300, 'small', '30°', 76),
           _f5lab(_f5d, _f5c, 'a', 22, 'small', 30, -1)]),
    ('l', [('seg', _f5a[0], _f5a[1], _f5d[0], _f5d[1], 'large', 7), ('arc', _f5c[0], _f5c[1], 36, 120, 180, 'large', '60°', 62),
           ('txt', 140, 210, 'a√3', 'large', 30)]),
    ('h', [('seg', _f5a[0], _f5a[1], _f5c[0], _f5c[1], 'ink', 7), _f5lab(_f5a, _f5c, '2a', 30, 'ink', 30, -1)]),
], vb='100 -15 340 370', w=420, col=0, title='Short leg, long leg, hypotenuse')
F5RAT_t1 = I('f5r1', '$a\\ :\\ a\\sqrt3\\ :\\ 2a$', size=40, col=1)
F5RAT_t2 = I('f5r2', 'short leg : long leg : hypotenuse', size=28, col=1)
F5RAT_t3 = IH('f5r3', 'Short $11\\ \\to\\ $ hypotenuse $22$', size=30, col=1)
F5RAT_t4 = IH('f5r4', 'Short $10\\ \\to\\ $ long $10\\sqrt3$', size=30, col=1)
# two drills, turned differently: tri 1 (right angle bottom-left), tri 2 (hypotenuse along the bottom)
_f5B1, _f5C1, _f5A1 = (110.0, 320.0), (110.0 + 150.0, 320.0), (110.0, 320.0 - 259.8)
_f5P, _f5Q, _f5Rr = (480.0, 320.0), (880.0, 320.0), (780.0, 320.0 - 173.2)
F5DR = GEO('f5dr', [
    ('line', _f5tri(_f5A1, _f5B1, _f5C1) + _f5tri(_f5P, _f5Q, _f5Rr) + [
        ('right', _f5B1[0], _f5B1[1], 0, 90, 16), ('arc', _f5A1[0], _f5A1[1], 40, 270, 300, 'small', '30°', 62),
        ('arc', _f5C1[0], _f5C1[1], 30, 120, 180, 'large', '60°', 54),
        ('right', _f5Rr[0], _f5Rr[1], 210, 300, 16), ('arc', _f5P[0], _f5P[1], 50, 0, 30, 'small', '30°', 76),
        ('arc', _f5Q[0], _f5Q[1], 34, 120, 180, 'large', '60°', 58),
        _f5lab(_f5B1, _f5C1, '7', 26, 'small', 30, -1), _f5lab(_f5P, _f5Q, '18', 28, 'ink', 30, -1)]),
    ('r1', [_f5lab(_f5C1, _f5A1, '14', 28, 'ink', 30, -1), _f5lab(_f5A1, _f5B1, '7√3', 40, 'large', 30, -1)]),
    ('r2', [_f5lab(_f5Q, _f5Rr, '9', 24, 'small', 30, -1), _f5lab(_f5Rr, _f5P, '9√3', 34, 'large', 30, -1)]),
], vb='20 40 900 330', w=1000, col=0, title='Two 30-60-90 triangles, turned differently')
F5DR_t1 = IH('f5d1', 'Short $7\\ \\to\\ $ long $7\\sqrt3$, $\\ $ hypotenuse $14$', size=30, col=0)
F5DR_t2 = IH('f5d2', 'Hypotenuse $18\\ \\to\\ $ short $9$, $\\ $ long $9\\sqrt3$', size=30, col=0)
F5LL = GEO('f5ll', [
    ('line', _f5tri(_f5a, _f5d, _f5c) + [('right', _f5d[0], _f5d[1], 0, 90, 18),
                                         ('arc', _f5a[0], _f5a[1], 50, 270, 300, 'small', '30°', 76),
                                         ('arc', _f5c[0], _f5c[1], 36, 120, 180, 'large', '60°', 62),
                                         ('txt', 150, 170, '5', 'ink', 34)]),
    ('opp', [('seg', _f5a[0], _f5a[1], _f5d[0], _f5d[1], 'large', 7), ('wedge', _f5c[0], _f5c[1], 60, 120, 180, 'large')]),
    ('s', [_f5lab(_f5d, _f5c, '5/√3', 24, 'small', 28, -1)]),
    ('h', [_f5lab(_f5a, _f5c, '10/√3', 34, 'ink', 28, -1)]),
], vb='100 -15 340 370', w=420, col=0, title='The 5 is opposite the 60° angle')
F5LL_t1 = I('f5l1', 'Long leg $5$ $\\ $(opposite $60°$)', size=30, col=1)
F5LL_t2 = IH('f5l2', 'Short leg $\\frac{5}{\\sqrt3}$', size=32, col=1)
F5LL_t3 = IH('f5l3', 'Hypotenuse $\\frac{10}{\\sqrt3}$', size=32, col=1)
F5LL_t4 = I('f5l4', 'Double only the SHORT leg', size=28, col=1)
F5DIV_t1 = IH('f5v1', 'Long leg $9\\ \\to\\ $ short leg $\\frac{9}{\\sqrt3}$', size=32, col=0)
F5DIV_t2 = IH('f5v2', '$\\frac{9}{\\sqrt3}=(9\\div3)\\sqrt3=3\\sqrt3$', size=34, col=0)
F5DIV_t3 = IH('f5v3', 'Why: $\\ \\frac{9\\cdot\\sqrt3}{\\sqrt3\\cdot\\sqrt3}=\\frac{9\\sqrt3}{3}=3\\sqrt3$', size=32, col=0)
F5DIV_t4 = IH('f5v4', 'Short $3\\sqrt3\\ \\to\\ $ hypotenuse $6\\sqrt3$', size=32, col=0)
F5DIV_t5 = IH('f5v5', 'Another one: $\\ \\frac{6}{\\sqrt3}=(6\\div3)\\sqrt3=2\\sqrt3$', size=30, col=0)
F5CAN_t1 = IH('f5c1', 'Long $12\\sqrt3\\ \\to\\ $ short $12\\ \\to\\ $ hypotenuse $24$', size=32, col=0)
# the 30-30-120 triangle: legs 300 (a), T at the top
_f5T, _f5L, _f5Rt, _f5M = (320.0, 100.0), (320.0 - 259.8, 250.0), (320.0 + 259.8, 250.0), (320.0, 250.0)
F5ISO = GEO('f5iso', [
    ('line', _f5tri(_f5T, _f5L, _f5Rt) + [('arc', _f5T[0], _f5T[1], 30, 210, 330, 'large', '120°', 60),
                                          ('arc', _f5L[0], _f5L[1], 60, 0, 30, 'small', '30°', 84),
                                          ('arc', _f5Rt[0], _f5Rt[1], 60, 150, 180, 'small', '30°', 84),
                                          _f5lab(_f5L, _f5T, 'a', 24, 'ink', 30, -1), _f5lab(_f5T, _f5Rt, 'a', 24, 'ink', 30, -1),
                                          ('tick', _f5L[0], _f5L[1], _f5T[0], _f5T[1]), ('tick', _f5T[0], _f5T[1], _f5Rt[0], _f5Rt[1])]),
    ('top', [('dot', _f5T[0], _f5T[1])]),
    ('alt', [('seg', _f5T[0], _f5T[1], _f5M[0], _f5M[1], 'teal', 3, True), ('right', _f5M[0], _f5M[1], 0, 90, 14),
             ('arc', _f5T[0], _f5T[1], 46, 210, 270, 'large', '60°', 104)]),
    ('half', [('tint', [_f5T, _f5L, _f5M], 'teal'), ('tint', [_f5T, _f5M, _f5Rt], 'teal')]),
    ('h', [('txt', 350, 218, 'a/2', 'small', 28)]),
    ('b', [('txt', 190, 278, 'a√3/2', 'large', 26), ('txt', 450, 278, 'a√3/2', 'large', 26)]),
    ('base', [('txt', 320, 320, 'base  a√3', 'large', 30)]),
], vb='30 60 580 280', w=800, col=0, title='A 30-30-120 triangle is two 30-60-90 halves')
F5ISO_t1 = I('f5i1', '$a\\ :\\ a\\ :\\ a\\sqrt3$ $\\quad$ leg : leg : base', size=32, col=0)
F5USE_t1 = IH('f5u1', 'Legs $8\\ \\to\\ $ base $8\\sqrt3$, $\\ $ height $4$', size=32, col=0)
F5USE_t2 = IH('f5u2', 'Base $6\\sqrt3\\ \\to\\ $ legs $6$, $\\ $ height $3$', size=32, col=0)
F5USE_t3 = IH('f5u3', 'Area $=\\frac{a\\sqrt3\\cdot\\frac a2}{2}=\\frac{a^2\\sqrt3}{4}$', size=34, col=0)
F5USE_t4 = I('f5u4', 'Seen in a rhombus with a $120°$ angle: its long diagonal cuts it into two of these', size=26, col=0)
video('geo-026', 'lesson', slides=[
    S('The 30°-60°-90° Triangle',
      L("As promised, now we learn special right triangles. Some of you may remember the gold triangle from school. It's a "
        "triangle with angles of thirty, sixty and ninety degrees, and its sides always keep the same ratio.")),
    S('Cut an equilateral triangle',
      L("Let's see where it comes from. Take an equilateral triangle, A B C. All its sides are equal, so let's call each "
        "side two a. And all its angles are sixty degrees.", show(F5EQ['line'], 'Take an equilateral triangle'),
        show(F5EQ['side'], "let's call each side two a")),
      L("Now from the top vertex, A, we drop an altitude straight down to the base. In an equilateral triangle the altitude "
        "is also a median, so it cuts the base exactly in the middle, into a and a.", show(F5EQ['top'], 'from the top vertex'),
        show(F5EQ['alt'], 'we drop an altitude')),
      L("Look at the half on the right, the triangle A D C. Its angle at D is ninety. Its angle at C is sixty, because C is a "
        "corner of the equilateral triangle. So the angle left at A is thirty. That's the gold triangle, thirty, sixty, "
        "ninety.", show(F5EQ['half'], 'Look at the half on the right'))),
    S('Find the long leg',
      L("Let's take that half out and look at it bigger. The same triangle, the same letters. The short leg, D C, is a. The "
        "hypotenuse, A C, is two a.", show(F5HALF['line'], "Let's take that half out")),
      L("We need the long leg, A D. How? With Pythagoras. The hypotenuse squared, minus the leg squared, gives the other leg "
        "squared.", show(F5HALF['q'], 'We need the long leg')),
      L("Two a, squared, is four a squared. Careful, the two is squared too, so it's four, not two. Four a squared minus a "
        "squared is three a squared. Now take the root, and the long leg is a times root three.",
        show(F5HALF['e1'], 'Two a, squared'), show(F5HALF['e2'], 'Now take the root'), show(F5HALF['res'], 'the long leg is a times'))),
    S('The ratio',
      L("We found it with a letter, not with numbers, so it's true for every gold triangle. The sides are always a, a root "
        "three, and two a. Short leg, long leg, hypotenuse.", show(F5RAT_t1, 'The sides are always'),
        show(F5RAT_t2, 'Short leg, long leg')),
      L("How do we know which side is which? By the angles, not by how the drawing is turned. The short leg is opposite "
        "the thirty degree angle. The long leg is opposite the sixty. And the hypotenuse is opposite the ninety.",
        show(F5RAT['line'], 'How do we know which side'), show(F5RAT['s'], 'The short leg is opposite'), show(F5RAT['l'], 'The long leg is opposite'),
        show(F5RAT['h'], 'And the hypotenuse')),
      L("And here's something nice. The short leg is always half the hypotenuse. If the short leg is eleven, the "
        "hypotenuse is twenty-two. To go from the short leg to the long leg, multiply by root three. Ten becomes ten root "
        "three. And from the long leg back to the short leg, divide by root three.", show(F5RAT_t3, 'If the short leg is eleven'),
        show(F5RAT_t4, 'Ten becomes ten root'))),
    S('One side is enough',
      L("Let's practice. Both of these are gold triangles, thirty, sixty, ninety, but they're turned differently. Until "
        "now, with Pythagoras, we always needed two sides to find the third. Here one side is enough to find the other two.",
        show(F5DR['line'], "Let's practice")),
      L("On the left, the seven is opposite the thirty, so it's the short leg. The hypotenuse is double, fourteen. The long "
        "leg is seven times root three, seven root three. We could use Pythagoras, but we don't need to, we just multiply.",
        show(F5DR['r1'], 'The hypotenuse is double')),
      L("On the right, the eighteen is opposite the ninety, so it's the hypotenuse. The short leg is half of it, nine. "
        "From the short leg to the long leg, times root three, nine root three.", show(F5DR['r2'], 'The short leg is half of it'))),
    S('From the long leg',
      L("Now here's a five, but look where it is. It's opposite the sixty degree angle, so it's the long leg, not the short "
        "leg.", show(F5LL['line'], "Now here's a five"), show(F5LL['opp'], "opposite the sixty degree angle"),
        ),
      L("So we can't say the hypotenuse is ten, or the long leg is five root three. To go from the long leg to the short "
        "leg, we divide by root three. The short leg is five over root three.", show(F5LL['s'], 'The short leg is five over'),
        ),
      L("And the hypotenuse is double the short leg, so ten over root three. Careful, we only ever double the short leg, "
        "never the long one. That's the most common mix-up.", show(F5LL['h'], 'so ten over root three'),
        show(F5LL_t4, 'we only ever double'))),
    S('Dividing by a root',
      L("One more. A long leg of nine. To get the short leg, we divide by root three. Nine over root three. There's a nice "
        "way to do this.", show(F5DIV_t1, 'A long leg of nine')),
      L("To divide a whole number by a root, first ignore the root for a moment. Nine divided by three is three. Now put the "
        "root three back. So nine over root three is three root three.", show(F5DIV_t2, 'Nine divided by three is three')),
      L("Why does it work? Multiply the top and the bottom by root three. Root three times root three is three. So we get "
        "nine root three over three, which is three root three. So the short leg is three root three, and the hypotenuse is "
        "double, six root three.", show(F5DIV_t3, 'Multiply the top and the bottom'), show(F5DIV_t4, 'and the hypotenuse is')),
      L("Let's try one more on our own. Six over root three. Ignore the root, six divided by three is two, and put the "
        "root back, two root three.", show(F5DIV_t5, 'Six over root three'))),
    S('A root that cancels',
      L("Sometimes the long leg already has a root three in it. Twelve root three, divided by root three. The roots cancel, "
        "so the short leg is twelve, and the hypotenuse is twenty-four. It looks harder, but it's actually shorter.",
        show(F5CAN_t1, 'Twelve root three'))),
    S('The 30°-30°-120° triangle',
      L("One more triangle, and it comes straight from the gold one. An isosceles triangle with a hundred twenty degrees at "
        "the top. The two base angles share what's left, a hundred eighty minus a hundred twenty, which is sixty, so thirty "
        "and thirty.", show(F5ISO['line'], 'An isosceles triangle')),
      L("It's not a right triangle. But from the top vertex, drop the altitude. In an isosceles triangle, the altitude is "
        "also a median and an angle bisector. So it cuts the hundred twenty into sixty and sixty, and the base into two "
        "equal halves.", show(F5ISO['top'], 'from the top vertex'), show(F5ISO['alt'], 'drop the altitude')),
      L("Now each half has thirty, sixty and ninety. Two gold triangles, back to back. The leg a is the hypotenuse of each "
        "half. The short leg, opposite the thirty, is half of it, a over two. That's the height.",
        show(F5ISO['half'], 'Two gold triangles'), show(F5ISO['h'], 'a over two')),
      L("The long leg is a over two times root three, a root three over two. The base is two of those, a root three. So the "
        "sides are a, a and a root three. Leg, leg, base. Nothing new to memorize, just cut it in half.",
        show(F5ISO['b'], 'a root three over two'), show(F5ISO['base'], 'The base is two of those'), show(F5ISO_t1, 'Leg, leg, base'))),
    S('Using the 30°-30°-120° triangle',
      L("Here too, one side is enough. Legs of eight, the base is eight root three, and the height, half a leg, is four. A "
        "base of six root three, divide by root three, and each leg is six. The height is three.",
        show(F5USE_t1, 'Legs of eight'), show(F5USE_t2, 'A base of six root three')),
      L("And its area. The base a root three, times the height a over two, divided by two. That's a squared root three over "
        "four. Keep this in mind, you'll see it again in the next lesson. Where do we meet this triangle? In a rhombus with "
        "a hundred twenty degree angle, the long diagonal cuts it into two of these. [pause] Okay. I'll see you in the next "
        "video.", show(F5USE_t3, 'And its area'), show(F5USE_t4, 'Where do we meet'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g027 (Hebrew: the gold sample question)
# Hebrew (geo 1127-1140): angle B 90, angle C 30, AB given: the ratio a, a root 3, 2a written on the triangle; "who still
# struggles" writes it with a; perimeter = add the sides. Course: a check with Pythagoras (kept as the second way).
# V3: the 30° and the 5 highlighted in the question; the colour copy; the side opposite the 30° traced teal (short leg, 5),
# then each value written on the copy when it is found; the perimeter written.
FIG_LEFT.update({'solve-geo31-g027', 'solve-geo31-g018', 'solve-geo31-g028'})
_f5qA, _f5qB, _f5qC = (130.34, 70.5), (130.34, 289.5), (509.66, 289.5)
F527 = GEO('f527', [
    ('line', _f5tri(_f5qA, _f5qB, _f5qC) + [('right', _f5qB[0], _f5qB[1], 0, 90, 18),
                                            ('arc', _f5qC[0], _f5qC[1], 60, 150, 180, 'small', '30°', 86),
                                            ('txt', 116, 54, 'A', 'ink', 26, True), ('txt', 112, 306, 'B', 'ink', 26, True),
                                            ('txt', 528, 306, 'C', 'ink', 26, True), ('txt', 104, 180, '5', 'ink', 30)]),
    ('s', [('seg', _f5qA[0], _f5qA[1], _f5qB[0], _f5qB[1], 'small', 7), ('wedge', _f5qC[0], _f5qC[1], 70, 150, 180, 'small')]),
    ('h', [_f5lab(_f5qA, _f5qC, '10', 26, 'ink', 30, -1)]),
    ('l', [_f5lab(_f5qB, _f5qC, '5√3', 30, 'large', 30, 1)]),
    ('rat', [('txt', 420, 72, 'a : a√3 : 2a', 'ink', 36), ('txt', 420, 122, 'a = 5:  5√3,  10', 'ink', 32)]),
], vb='80 30 480 300', w=380, title='Triangle ABC: a 30-60-90 triangle')
F527_t1 = I('f527a', '$a\\ :\\ a\\sqrt3\\ :\\ 2a$', size=34, col=1)
F527_t2 = IH('f527b', '$a=5$: $\\ 5\\sqrt3$, $\\ 10$', size=32, col=1)
F527_t3 = IH('f527c', '$5+10+5\\sqrt3=15+5\\sqrt3$', size=32, col=1)
F527_t4 = IH('f527d', '$BC^2=10^2-5^2=100-25=75$', size=30, col=1)
F527_t5 = IH('f527e', '$BC=\\sqrt{75}=\\sqrt{25\\cdot3}=5\\sqrt3$', size=30, col=1)
video('solve-geo31-g027', 'solution', qid='geo31-g027', slides=[
    SM('Method 1 · The side ratio', 'The side ratio',
      L("Triangle A B C is a right triangle. Given: angle A B C is ninety degrees, angle A C B is thirty degrees, and A B is "
        "five centimeters. What is the perimeter of the triangle, in centimeters?", pt('stem', 'Triangle A B C is a right triangle', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("A right triangle with a thirty degree angle, so the third angle is sixty. It's a gold triangle. For the perimeter we "
        "need all three sides, and we know only one. [short pause] We'll solve it with the side ratio, and then check it with "
        "Pythagoras.", pt('fig: 30°', 'A right triangle with a thirty degree angle')),
      L("[short pause] In a gold triangle the sides are a, a root three, and two a. Which side is A B? It's opposite the "
        "thirty degree angle at C, so it's the short leg. So a is five.", show(F527['line'], 'In a gold triangle'),
        pt('fig: 5', 'Which side is A B'), show(F527['s'], "It's opposite the thirty")),
      L("The hypotenuse, A C, is double the short leg, so ten. The long leg, B C, is five times root three, five root three. "
        "Once you've practiced enough, you can write these straight on the triangle. If it's still hard, write it with a. a "
        "is five, so a root three is five root three, and two a is ten.", show(F527['h'], 'is double the short leg'),
        show(F527['l'], 'five root three. Once'), show(F527['rat'], "If it's still hard")),
      L("The perimeter is the sum of the sides. Five plus ten is fifteen, and the five root three stays separate, because "
        "only one side has a root. So fifteen plus five root three. Choice number one is our answer.",
        show(F527_t3, 'Five plus ten is fifteen'), mk('tick', 'choice 1', 'Choice number one is our answer'))),
    SM('Method 2 · Check with Pythagoras', 'Check with Pythagoras',
      L("[pause] Let's check the long leg with Pythagoras. The hypotenuse is double the short leg, ten. The long leg squared "
        "is ten squared minus five squared, a hundred minus twenty-five, which is seventy-five.", show(F527_t4, 'The long leg squared')),
      L("Seventy-five is twenty-five times three, so its root is five root three. The same length. The ratio just gets there "
        "faster. Choice number one. [pause] Okay. I'll see you in the next question.", show(F527_t5, 'Seventy-five is twenty-five'),
        mk('tick', 'choice 1', 'Choice number one. '))),
])

# ------------------------------------------------------------------------------------------------ geo-017-after (lesson: the equilateral triangle's area)
# Hebrew (geo 760-793): drop the altitude (also a median: a over 2 and a over 2), Pythagoras for the height (a squared minus
# a over 2 squared), the area = side times height over 2, simplify to a squared root 3 over 4, learn it by heart because it
# is common on the exam, the folk-dance count "a-two-three-four". Course addition kept: the height straight from the gold
# triangle (first), the 30-30-120 link. Two worked examples (side 8, side 6).
# V3: the equilateral triangle built, the altitude drawn from the top, one half tinted inside the triangle (the gold half),
# the height written on the altitude; the count written beat by beat.
F5AR = GEO('f5ar', [
    ('line', _f5tri(_f5A, _f5B, _f5C) + [('txt', 320, 12, 'A', 'ink', 26, True), ('txt', 150, 305, 'B', 'ink', 26, True),
                                          ('txt', 490, 305, 'C', 'ink', 26, True), _f5lab(_f5B, _f5A, 'a', 24, 'ink', 30),
                                          _f5lab(_f5A, _f5C, 'a', 24, 'ink', 30)]),
    ('top', [('dot', _f5A[0], _f5A[1])]),
    ('alt', [('seg', _f5A[0], _f5A[1], _f5D[0], _f5D[1], 'teal', 3, True), ('right', _f5D[0], _f5D[1], 0, 90, 16),
             ('txt', 245, 314, 'a/2', 'small', 26), ('txt', 395, 314, 'a/2', 'small', 26)]),
    ('half', [('tint', [_f5A, _f5D, _f5C], 'teal'), ('arc', _f5C[0], _f5C[1], 40, 120, 180, 'large', '60°', 66),
              ('arc', _f5A[0], _f5A[1], 48, 270, 300, 'small', '30°', 74)]),
    ('h', [('txt', 352, 180, 'h', 'large', 32, True)]),
], vb='110 0 420 340', w=560, col=0, title='An equilateral triangle with side a, cut by its altitude')
F5AR_t1 = IH('f5a1', '$h=\\frac a2\\cdot\\sqrt3=\\frac{a\\sqrt3}{2}$', size=34, col=1)
F5AR_t2 = IH('f5a2', '$h^2=a^2-\\left(\\frac a2\\right)^2=a^2-\\frac{a^2}{4}=\\frac{3a^2}{4}$', size=30, col=1)
F5AR_t3 = IH('f5a3', '$h=\\frac{a\\sqrt3}{2}$', size=34, col=1)
F5AR_t4 = IH('f5a4', '$S=\\frac{a\\cdot\\frac{a\\sqrt3}{2}}{2}=\\frac{a^2\\sqrt3}{4}$', size=36, col=0)
F5AR_t5 = I('f5a5', '$a\\ \\ $ two $\\ \\ $ three $\\ \\ $ four', size=36, col=0)
F5AR_t6 = I('f5a6', '$a^2\\qquad\\sqrt3\\qquad\\div4$', size=36, col=0)
F5AR_t7 = IH('f5a7', 'Side $8$: $\\ \\frac{8^2\\sqrt3}{4}=\\frac{64\\sqrt3}{4}=16\\sqrt3$', size=32, col=0)
F5AR_t8 = IH('f5a8', 'Side $6$: $\\ \\frac{6^2\\sqrt3}{4}=\\frac{36\\sqrt3}{4}=9\\sqrt3$', size=32, col=0)
video('geo-017-after', 'lesson', slides=[
    S('Equilateral Triangle Area',
      L("Now let's see how we find the area of an equilateral triangle. Now that we know the gold triangle, it's quick.")),
    S('The height',
      L("For an area we need a side and the height to it. So here's an equilateral triangle, A B C, and every side is a. "
        "From the top vertex we drop an altitude to the base.", show(F5AR['line'], "So here's an equilateral triangle"),
        show(F5AR['top'], 'From the top vertex'), show(F5AR['alt'], 'we drop an altitude')),
      L("The altitude is also a median, so it cuts the base into a over two and a over two. Now look at the half on the "
        "right. Its angles are ninety, sixty and thirty, so it's a gold triangle. Its hypotenuse is a, and its short leg, "
        "opposite the thirty, is a over two.", show(F5AR['half'], 'Now look at the half on the right')),
      L("The height is the long leg, so it's the short leg times root three. a over two, times root three, is a root three "
        "over two.", show(F5AR['h'], 'The height is the long leg'), show(F5AR_t1, 'a over two, times root three'))),
    S('Check with Pythagoras',
      L("You can also get the height with Pythagoras, the same half triangle. The hypotenuse squared, minus the short leg "
        "squared. a over two, squared, is a squared over four, because the top and the bottom are both squared.",
        show(F5AR_t2, 'the same half triangle')),
      L("a squared minus a quarter of a squared is three quarters of a squared. Take the root, and the height is a root "
        "three over two. The same height. The gold triangle just gets there faster.", show(F5AR_t3, 'Take the root'))),
    S('The area formula',
      L("Now the area. A side, times the height to that side, divided by two. The side is a, the height is a root three over "
        "two, and we divide by two. a times a is a squared, and dividing by two and then by two again is dividing by four. "
        "So the area of an equilateral triangle is a squared times root three, over four.",
        show(F5AR_t4, 'A side, times the height')),
      L("Why learn it by heart? Because the area of an equilateral triangle comes up a lot on the exam, and we don't want to "
        "find the height every time and only then the area.")),
    S('a-two-three-four',
      L("At first the formula looks a bit complicated, but there's an easy way to remember it. Think of a folk dance "
        "teacher counting the beat, a-two-three-four, a-two-three-four.", show(F5AR_t5, 'a-two-three-four, a-two')),
      L("That's the formula. a, squared, root three, over four.", show(F5AR_t6, 'a, squared, root three')),
      L("Let's try it. Side eight. Eight squared is sixty-four, times root three, over four. Sixty-four divided by four is "
        "sixteen, so sixteen root three.", show(F5AR_t7, 'Side eight')),
      L("Side six. Six squared is thirty-six, times root three, over four. Thirty-six divided by four is nine, so nine root "
        "three. A little practice, and it'll stick. And the thirty, thirty, a hundred twenty triangle with legs a, from the "
        "last lesson, has the same area, a squared root three over four. [pause] Okay. I'll see you in the next video.",
        show(F5AR_t8, 'Side six'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g018 (Hebrew: the perimeter-6 question)
# Hebrew (geo 795-830): "respectively", each side from the perimeter, the halves, the small triangle is equilateral too (two
# equal sides around a 60° angle), big area minus small area, keep the 4 in the denominator for the subtraction. Course
# addition kept: half the side, so a quarter of the area (the side is squared in the formula).
# V3: the given highlighted part by part; the colour copy; 10 on each side, then 5 and 5; the small triangle DBE tinted
# inside the big one with its 60° angle and equal sides; then the quadrilateral tinted when it is found.
_g18A, _g18B, _g18C, _g18D, _g18E = (320.0, 76.4), (199.2, 285.7), (440.8, 285.7), (259.6, 181.1), (320.0, 285.7)
_g18cB, _g18cE, _g18cD = (520.0, 300.0), (780.0, 300.0), (650.0, 300.0 - 225.2)
F518 = GEO('f518', [
    ('line', _f5tri(_g18A, _g18B, _g18C) + [('seg', _g18D[0], _g18D[1], _g18E[0], _g18E[1], 'ink', 3),
                                            ('txt', 320, 56, 'A', 'ink', 26, True), ('txt', 180, 302, 'B', 'ink', 26, True),
                                            ('txt', 460, 302, 'C', 'ink', 26, True), ('txt', 238, 176, 'D', 'ink', 26, True),
                                            ('txt', 320, 312, 'E', 'ink', 26, True)]),
    ('ten', [_f5lab(_g18A, _g18C, '10', 26, 'ink', 28, -1), ('txt', 194, 130, '10', 'ink', 28)]),
    ('five', [('txt', 270, 122, '5', 'small', 28), ('txt', 212, 228, '5', 'small', 28), ('txt', 258, 312, '5', 'small', 28),
              ('txt', 382, 312, '5', 'small', 28)]),
    ('small', [('tint', [_g18D, _g18B, _g18E], 'teal'), ('arc', _g18B[0], _g18B[1], 30, 0, 60, 'small', '60°', 52),
               ('tick', _g18B[0], _g18B[1], _g18D[0], _g18D[1]), ('tick', _g18B[0], _g18B[1], _g18E[0], _g18E[1])]),
    # enlarged cut-out of DBE (same letters, same tint); the copy stays, dimmed, with DBE still outlined
    ('cut', [('dim', 150, 30, 340, 300), ('tint', [_g18D, _g18B, _g18E], 'teal')] + _f5tri(_g18D, _g18B, _g18E, 'teal', 3) +
            [('tint', [_g18cD, _g18cB, _g18cE], 'teal')] + _f5tri(_g18cD, _g18cB, _g18cE) +
            [('txt', 650, 52, 'D', 'ink', 30, True), ('txt', 506, 318, 'B', 'ink', 30, True), ('txt', 794, 318, 'E', 'ink', 30, True),
             _f5lab(_g18cB, _g18cD, '5', 26, 'small', 34, 1), _f5lab(_g18cB, _g18cE, '5', 28, 'small', 34, -1),
             ('tick', _g18cB[0], _g18cB[1], _g18cD[0], _g18cD[1]), ('tick', _g18cB[0], _g18cB[1], _g18cE[0], _g18cE[1]),
             ('arc', _g18cB[0], _g18cB[1], 44, 0, 60, 'small', '60°', 72)]),
    ('eqv', [('arc', _g18cD[0], _g18cD[1], 40, 240, 300, 'small', '60°', 68), ('arc', _g18cE[0], _g18cE[1], 44, 120, 180, 'small', '60°', 72),
             _f5lab(_g18cD, _g18cE, '5', 26, 'small', 34, 1), ('txt', 298, 226, '5', 'small', 24)]),
    ('quad', [('tint', [_g18A, _g18D, _g18E, _g18C], 'orange')] + _f5tri(_g18A, _g18B, _g18C) +
             [('seg', _g18D[0], _g18D[1], _g18E[0], _g18E[1], 'ink', 3)]),
], vb='150 30 680 300', w=500, title='Triangle ABC with the midpoints D and E, and DBE enlarged')
F518_t1 = IH('f518a', '$S_{ABC}=\\frac{10^2\\sqrt3}{4}=\\frac{100\\sqrt3}{4}$', size=30, col=1)
F518_t2 = IH('f518b', '$S_{DBE}=\\frac{5^2\\sqrt3}{4}=\\frac{25\\sqrt3}{4}$', size=30, col=1)
F518_t3 = IH('f518c', '$S_{ADEC}=\\frac{100\\sqrt3}{4}-\\frac{25\\sqrt3}{4}=\\frac{75\\sqrt3}{4}$', size=28, col=1)
F518_t4 = IH('f518d', 'Side $\\times\\frac12$ $\\ \\to\\ $ area $\\times\\frac14$', size=32, col=1)
F518_t5 = IH('f518e', '$\\frac34\\cdot\\frac{100\\sqrt3}{4}=\\frac{75\\sqrt3}{4}$', size=32, col=1)
video('solve-geo31-g018', 'solution', qid='geo31-g018', slides=[
    SM('Method 1 · Big minus small', 'Big minus small',
      L("A B C is an equilateral triangle with perimeter thirty centimeters. Points D and E are the midpoints of A B and B "
        "C, respectively. What is the area of quadrilateral A D E C, in square centimeters?", pt('stem', 'A B C is an equilateral triangle', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("What does respectively mean? The first point goes with the first side. So D is the midpoint of A B, and E is the "
        "midpoint of B C. [short pause] We'll solve it with the big triangle minus the small one, and then with a quicker "
        "ratio.", pt('fig: D', 'So D is the midpoint')),
      L("[short pause] The perimeter is thirty, and the three sides are equal, so each side is ten. D and E are midpoints, "
        "so A B is cut into five and five, and B C too.", show(F518['line'], 'The perimeter is thirty'), show(F518['ten'], 'so each side is ten'),
        show(F518['five'], 'so A B is cut into five and five')),
      L("Now look at the small triangle, D B E. B D is five and B E is five, so it's isosceles. And the angle at B is sixty, "
        "because B is a corner of the equilateral triangle. Its other two angles are equal and share a hundred eighty minus "
        "sixty, which is a hundred twenty, so sixty and sixty. All its angles are sixty, so D B E is equilateral too, with "
        "side five.", show(F518['small'], 'Now look at the small triangle'), show(F518['cut'], 'B D is five'),
        show(F518['eqv'], 'so sixty and sixty')),
      L("So the quadrilateral is the big triangle, A B C, minus the small triangle, D B E.", show(F518['quad'], 'So the quadrilateral'))),
    SM('Method 1 · Big minus small', 'Big minus small',
      L("Area of A B C, by the formula, a-two-three-four. The side is ten, so ten squared, a hundred, times root three, over "
        "four. We could simplify the four, but let's leave it. It'll help with the subtraction.", show(F518_t1, 'Area of A B C')),
      L("Area of D B E. The side is five, so twenty-five root three over four.", show(F518_t2, 'Area of D B E')),
      L("Now subtract. You see why we kept the four? Both have the same denominator, so there's no common denominator to "
        "find. A hundred minus twenty-five is seventy-five, so seventy-five root three over four. Choice number two is our "
        "answer.", show(F518_t3, 'Now subtract'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · A quicker ratio', 'A quicker ratio',
      L("[pause] Another way, from the formula itself. The small triangle has half the side of the big one. In the formula, "
        "the side is squared, so half the side gives a half squared, a quarter of the area.", show(F518_t4, 'the side is squared')),
      L("So the small triangle is a quarter of the big one, and the quadrilateral is the other three quarters. Three "
        "quarters of a hundred root three over four is seventy-five root three over four. Choice number two. [pause] Okay. "
        "I'll see you in the next question.", show(F518_t5, 'Three quarters of a hundred'), mk('tick', 'choice 2', 'Choice number two. '))),
])

# ------------------------------------------------------------------------------------------------ geo-027-after (lesson: the 45-45-90 triangle)
# Hebrew (geo 1141-1162): the silver triangle (our own name, "so it won't feel lonely"), the borekas triangle; right and
# isosceles, so 45 and 45; Pythagoras: a squared plus a squared, the hypotenuse a root 2; the ratio a, a, a root 2; leg to
# hypotenuse times root 2, back divided by root 2 (the same "ignore the root" method): 3 -> 3 root 2, 10 -> 5 root 2 (new
# numbers here). Course additions kept: the square sandwich cut corner to corner, a square's diagonal.
# V3: a square drawn, its diagonal drawn (corner to corner), one half tinted inside the square, then the same half on its
# own with the same tint and labels; the hypotenuse written when it is found.
_s4 = [(150.0, 40.0), (150.0, 300.0), (410.0, 300.0), (410.0, 40.0)]
F5SQ = GEO('f5sq', [
    ('line', [('seg', 150, 40, 150, 300), ('seg', 150, 300, 410, 300), ('seg', 410, 300, 410, 40), ('seg', 410, 40, 150, 40)]),
    ('diag', [('dot', 150, 40), ('dot', 410, 300), ('seg', 150, 40, 410, 300, 'teal', 4, True)]),
    ('half', [('tint', [(150, 40), (150, 300), (410, 300)], 'teal'), ('right', 150, 300, 0, 90, 18)]),
], vb='110 10 340 320', w=560, col=0, title='A square cut corner to corner')
_f5sA, _f5sB, _f5sC = (160.0, 30.0), (160.0, 300.0), (430.0, 300.0)
F5SV = GEO('f5sv', [
    ('line', [('tint', [_f5sA, _f5sB, _f5sC], 'teal')] + _f5tri(_f5sA, _f5sB, _f5sC) + [('right', _f5sB[0], _f5sB[1], 0, 90, 18),
              ('tick', _f5sA[0], _f5sA[1], _f5sB[0], _f5sB[1]), ('tick', _f5sB[0], _f5sB[1], _f5sC[0], _f5sC[1]),
              _f5lab(_f5sA, _f5sB, 'a', 26, 'small', 32, 1), _f5lab(_f5sB, _f5sC, 'a', 26, 'small', 32, 1)]),
    ('ang', [('arc', _f5sA[0], _f5sA[1], 46, 270, 315, 'small', '45°', 72), ('arc', _f5sC[0], _f5sC[1], 46, 135, 180, 'small', '45°', 72)]),
    ('hyp', [('seg', _f5sA[0], _f5sA[1], _f5sC[0], _f5sC[1], 'large', 7), _f5lab(_f5sA, _f5sC, '?', 32, 'large', 34, -1)]),
    ('e1', [('txt', 690, 110, 'a² + a² = 2a²', 'ink', 34)]),
    ('e2', [('txt', 690, 180, 'hypotenuse = √(2a²) = a√2', 'large', 30)]),
    ('hv', [_f5lab(_f5sA, _f5sC, 'a√2', 34, 'large', 32, 1)]),
], vb='100 0 840 340', w=1100, col=0, title='The 45-45-90 triangle: two equal legs')
F5SV_t1 = IH('f5s1', '$a^2+a^2=2a^2$', size=34, col=1)
F5SV_t2 = IH('f5s2', 'hypotenuse $=\\sqrt{2a^2}=a\\sqrt2$', size=32, col=1)
F5SV_t3 = I('f5s3', '$a\\ :\\ a\\ :\\ a\\sqrt2$', size=40, col=1)
F5SV_t4 = IH('f5s4', 'Leg $7\\ \\to\\ $ hypotenuse $7\\sqrt2$', size=32, col=0)
F5SV_t5 = IH('f5s5', 'Hypotenuse $16\\ \\to\\ $ leg $\\frac{16}{\\sqrt2}=8\\sqrt2$', size=32, col=0)
F5SV_t6 = IH('f5s6', 'Hypotenuse $6\\sqrt2\\ \\to\\ $ leg $6$', size=32, col=0)
F5SV_t7 = I('f5s7', "A square's diagonal $=$ side $\\cdot\\sqrt2$", size=30, col=0)
video('geo-027-after', 'lesson', slides=[
    S('The 45°-45°-90° Triangle',
      L("Let's continue to the silver triangle. The silver triangle is our own name, there isn't really such a name. We gave "
        "it one so the gold triangle won't feel lonely.")),
    S('Right and isosceles',
      L("It's a right triangle that is also isosceles. Here's a picture that helps. Take a square sandwich, and cut it "
        "from one corner to the opposite corner. Some students think of a triangle cheese pastry, a borekas.",
        show(F5SQ['line'], 'Take a square sandwich'), show(F5SQ['diag'], 'cut it from one corner')),
      L("Each half is exactly this triangle. It has a right angle, the corner of the square, and two equal legs, the two "
        "edges of the sandwich. The cut is the hypotenuse.", show(F5SQ['half'], 'Each half is exactly'))),
    S('The ratio',
      L("Let's look at the half on its own, the same triangle. The two legs are equal, so the angles opposite them are "
        "equal too. Together they make ninety, so each one is forty-five degrees.", show(F5SV['line'], "Let's look at the half on its own"),
        show(F5SV['ang'], 'so each one is forty-five')),
      L("Its sides always keep the ratio a, a, a root two. Let's see why. One leg is a, so the other leg is a too. To find "
        "the hypotenuse, we use Pythagoras. a squared plus a squared is two a squared.", show(F5SV['hyp'], 'To find the hypotenuse'),
        show(F5SV['e1'], 'a squared plus a squared')),
      L("Take the root, and the hypotenuse is a times root two. So the sides of the silver triangle are a, a, and a root "
        "two. Two legs and the hypotenuse.", show(F5SV['e2'], 'Take the root'), show(F5SV['hv'], 'the hypotenuse is a times'),
        show(F5SV_t3, 'So the sides of the silver triangle'))),
    S('Leg and hypotenuse',
      L("From a leg to the hypotenuse, multiply by root two. From the hypotenuse to a leg, divide by root two. Say a leg is "
        "seven. The hypotenuse is seven root two. And of course the other leg is also seven.", show(F5SV_t4, 'Say a leg is seven')),
      L("Now a hypotenuse of sixteen. The legs are equal, and each is sixteen over root two. Remember the method from the "
        "gold triangle, ignore the root. Sixteen divided by two is eight, and put the root two back, eight root two.",
        show(F5SV_t5, 'Now a hypotenuse of sixteen')),
      L("And a hypotenuse of six root two? Divide by root two, the roots cancel, and each leg is six.", show(F5SV_t6, 'six root two')),
      L("And a square's diagonal? It's the same triangle. The side of the square is a leg, and the diagonal is the "
        "hypotenuse, so the diagonal is the side times root two. Let's solve an example. [pause] Okay. I'll see you in the "
        "next video.", show(F5SV_t7, "a square's diagonal"))),
])

# ------------------------------------------------------------------------------------------------ geo31-g028 (Hebrew: the silver sample question)
# Hebrew (geo 1163-1188): a right triangle with a 45° angle, so the other is 45 too: silver; the hypotenuse matches a root 2;
# strong in algebra: divide by root 2 directly; otherwise as an equation a root 2 = 18; the "ignore the root" method; the
# perimeter. Course additions kept: not half of 18 (the factor is root 2, not 2); the equation with Pythagoras (2t² = 324);
# look at the angles before choosing a ratio.
# V3: the 45° and the 18 highlighted in the question; the colour copy; the second 45° written at A, the equal legs marked,
# each leg written when found, the perimeter.
_f8A, _f8B, _f8C = (222.67, 82.67), (222.67, 277.33), (417.33, 277.33)
F528 = GEO('f528', [
    ('line', _f5tri(_f8A, _f8B, _f8C) + [('right', _f8B[0], _f8B[1], 0, 90, 16), ('arc', _f8C[0], _f8C[1], 40, 135, 180, 'small', '45°', 66),
                                         ('txt', 208, 66, 'A', 'ink', 26, True), ('txt', 204, 294, 'B', 'ink', 26, True),
                                         ('txt', 436, 294, 'C', 'ink', 26, True), _f5lab(_f8A, _f8C, '18', 26, 'ink', 30, -1)]),
    ('a45', [('arc', _f8A[0], _f8A[1], 40, 270, 315, 'small', '45°', 66), ('tick', _f8A[0], _f8A[1], _f8B[0], _f8B[1]),
             ('tick', _f8B[0], _f8B[1], _f8C[0], _f8C[1])]),
    ('legs', [_f5lab(_f8A, _f8B, '9√2', 42, 'large', 30, -1), _f5lab(_f8B, _f8C, '9√2', 30, 'large', 30, -1)]),
    ('eq', [('txt', 450, 70, 'a : a : a√2', 'ink', 30), ('txt', 450, 112, 'a√2 = 18', 'ink', 28),
            ('txt', 450, 152, 'a = 18/√2 = 9√2', 'ink', 28)]),
], vb='140 40 440 300', w=340, title='Triangle ABC: a 45-45-90 triangle')
F528_t1 = I('f528a', '$a\\ :\\ a\\ :\\ a\\sqrt2$', size=34, col=1)
F528_t2 = IH('f528b', '$a\\sqrt2=18$: $\\ a=\\frac{18}{\\sqrt2}=9\\sqrt2$', size=30, col=1)
F528_t3 = IH('f528c', '$9\\sqrt2+9\\sqrt2+18=18+18\\sqrt2$', size=30, col=1)
F528_t4 = IH('f528d', '$t^2+t^2=18^2$: $\\ 2t^2=324$', size=30, col=1)
F528_t5 = IH('f528e', '$t^2=162=81\\cdot2$: $\\ t=9\\sqrt2$', size=30, col=1)
F528_t6 = I('f528f', '$30°$: $\\ a,\\ a\\sqrt3,\\ 2a$ $\\qquad 45°$: $\\ a,\\ a,\\ a\\sqrt2$', size=28, col=1)
video('solve-geo31-g028', 'solution', qid='geo31-g028', slides=[
    SM('Method 1 · The side ratio', 'The side ratio',
      L("Triangle A B C is a right triangle. Given: angle A B C is ninety degrees, angle A C B is forty-five degrees, and A C "
        "is eighteen centimeters. What is its perimeter, in centimeters?", pt('stem', 'Triangle A B C is a right triangle', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("A right triangle with a forty-five degree angle. The angles add up to a hundred eighty, so the third angle is "
        "forty-five too. It's a silver triangle, and its legs are equal. [short pause] We'll solve it with the side ratio, and "
        "then with an equation.", pt('fig: 45°', 'A right triangle with a forty-five'), show(F528['line'], "It's a silver triangle"),
        show(F528['a45'], 'its legs are equal')),
      L("[short pause] In a silver triangle the sides are a, a, and a root two. A C is opposite the right angle, so it's the "
        "hypotenuse, and it matches a root two.", pt('fig: 18', 'A C is opposite the right angle')),
      L("To go from the hypotenuse to a leg, we divide by root two, eighteen over root two. Ignore the root, eighteen "
        "divided by two is nine, and put the root two back, nine root two. If that's hard, look at it as an equation. a root "
        "two equals eighteen, so a is eighteen over root two, the same nine root two.", show(F528['legs'], 'nine root two. If'),
        show(F528['eq'], "If that's hard")),
      L("Careful, a leg is not half of eighteen. The factor here is root two, not two. So the legs are nine root two and nine "
        "root two. The perimeter is nine root two plus nine root two plus eighteen, which is eighteen plus eighteen root two. "
        "Choice number one is our answer.", show(F528_t3, 'The perimeter is nine root two'),
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
    SM('Method 2 · An equation', 'An equation',
      L("[pause] Another way, with Pythagoras. Call each leg t. t squared plus t squared is eighteen squared, so two t squared "
        "is three hundred twenty-four.", show(F528_t4, 'Call each leg t')),
      L("t squared is a hundred sixty-two, which is eighty-one times two. So t is nine root two. The same result. Choice "
        "number one.", show(F528_t5, 'which is eighty-one times two'), mk('tick', 'choice 1', 'The same result. Choice')),
      L("Before you pick a ratio, look at the angles. Thirty degrees means the gold triangle, the doubling rule and root "
        "three. Forty-five means the silver triangle, two equal legs and root two. With a little practice it becomes fast, "
        "and it saves you a lot of Pythagoras. [pause] Okay. I'll see you in the next question.", show(F528_t6, 'look at the angles'))),
])

# ---- placement in the question videos: the question figure is on the left (FIG_LEFT); our board copy and the typed steps
# go in the right column at explicit board y (a slide with only right-column items would otherwise move to the left)
_R(F527, 100); _R(F527_t3, 360); _R(F527_t4, 110); _R(F527_t5, 170)
_R(F518, 100); _R(F518_t1, 180); _R(F518_t2, 245); _R(F518_t3, 310); _R(F518_t4, 110); _R(F518_t5, 175)
_R(F528, 100); _R(F528_t3, 400); _R(F528_t4, 110); _R(F528_t5, 170); _R(F528_t6, 230)

# =================================================================================================================
# Topic-31 advanced block, part 1 (fragment f6, 2026-10-14): geo31-g031 ... geo31-g036, the Hebrew "triangles advanced"
# sample questions (geo 1200-1447). Question figure on the left (FIG_LEFT, figw 0.56), our colour copy built in layers on
# the right (Rule V3). Every Hebrew method is kept; plugging in numbers is explained on its own (topic 51 comes later).
# =================================================================================================================
FIG_LEFT.update({'solve-geo31-g031', 'solve-geo31-g032', 'solve-geo31-g033', 'solve-geo31-g035', 'solve-geo31-g036'})


def f6_tri(p, q, r, col='ink', w=3):
    """the three sides of a triangle as segments"""
    return [('seg', p[0], p[1], q[0], q[1], col, w), ('seg', q[0], q[1], r[0], r[1], col, w), ('seg', r[0], r[1], p[0], p[1], col, w)]


def f6_lab(pts, names, off):
    return [('txt', pts[k][0] + off[k][0], pts[k][1] + off[k][1], names[k], 'ink', 26, True) for k in range(len(pts))]


# ------------------------------------------------------------------------------------------------ geo31-g031 (Hebrew Q1 of the advanced lesson)
# Hebrew (geo 1200-1260): three methods - the angle sum in the highlighted triangle ABE (60, the vertical angle, 180 minus
# the given angle), the exterior-angle rule (shorter end), and plugging in a number (the letter in the choices; an obtuse
# value that fits the figure; eliminate three). English letters x (outside, at E) and y (at A), x = 110 -> y = 50.
# V3: the triangle ABE tinted inside the copy (the part we study), each of its angles written as it is found (60 at B,
# y at A in the same colour as the given y, 180 - x at E as an orange wedge next to x); method 2: x and the two far
# angles in matching colours; method 3: a copy with the numbers written on it.
f6A, f6B, f6C = (320.0, 139.783), (236.571, 284.286), (403.429, 284.286)
f6D, f6E, f6F = (303.314, 67.532), (353.371, 284.286), (361.714, 67.532)
f6aEA, f6aAF, f6aAD = gdir(*f6E, *f6A), gdir(*f6A, *f6F), gdir(*f6A, *f6D)
f6aAE, f6aAB, f6aBA = gdir(*f6A, *f6E), gdir(*f6A, *f6B), gdir(*f6B, *f6A)
f6g31_lines = (f6_tri(f6A, f6B, f6C) + [('seg', f6D[0], f6D[1], f6E[0], f6E[1], 'ink', 3), ('seg', f6A[0], f6A[1], f6F[0], f6F[1], 'ink', 3)]
               + f6_lab([f6A, f6B, f6C, f6D, f6E, f6F], 'ABCDEF', [(-20, -4), (-16, 14), (16, 14), (-16, -6), (2, 22), (16, -6)]))
f6g31_giv = [('arc', f6E[0], f6E[1], 27, 0, f6aEA, 'red', 'x', 46), ('arc', f6A[0], f6A[1], 31, f6aAF, f6aAD, 'small', 'y', 48)]
f6TINT = [('tint', [f6A, f6B, f6E], 'teal')]
f6g31 = GEO('f6g31', [
    ('line', f6g31_lines + f6g31_giv),
    ('abe', f6TINT + [('seg', f6A[0], f6A[1], f6B[0], f6B[1], 'teal', 5), ('seg', f6B[0], f6B[1], f6E[0], f6E[1], 'teal', 5),
                      ('seg', f6E[0], f6E[1], f6A[0], f6A[1], 'teal', 5)]),
    ('b60', [('arc', f6B[0], f6B[1], 30, 0, f6aBA, 'small', '60°', 52)]),
    ('ay', [('arc', f6A[0], f6A[1], 31, f6aAB, f6aAE, 'small', 'y', 48)]),
    ('e180', [('wedge', f6E[0], f6E[1], 34, f6aEA, 180, 'orange'), ('txt', f6E[0] - 24, f6E[1] - 52, '180°−x', 'orange', 20)]),
], vb='190 40 260 285', w=330, title='Equilateral triangle ABC with the line DE through A')
f6g31x = GEO('f6g31x', [
    ('line', f6g31_lines + f6g31_giv + f6TINT),
    ('far', [('arc', f6B[0], f6B[1], 30, 0, f6aBA, 'small', '60°', 52), ('arc', f6A[0], f6A[1], 31, f6aAB, f6aAE, 'small', 'y', 48),
             ('arc', f6E[0], f6E[1], 27, 0, f6aEA, 'red', 'x', 46)]),
], vb='190 40 260 285', w=300, title='x is an exterior angle of triangle ABE')
f6g31p = GEO('f6g31p', [
    ('line', f6g31_lines + [('arc', f6E[0], f6E[1], 27, 0, f6aEA, 'red', '110°', 60), ('arc', f6A[0], f6A[1], 31, f6aAF, f6aAD, 'small', 'y', 48)] + f6TINT),
    ('vals', [('arc', f6B[0], f6B[1], 30, 0, f6aBA, 'small', '60°', 52), ('arc', f6A[0], f6A[1], 31, f6aAB, f6aAE, 'small', '50°', 54),
              ('txt', 408, 122, 'y = 50°', 'small', 24)]),
], vb='190 40 260 285', w=260, title='Plugging in x = 110°')
f6k31a = IH('f6k31a', '$60°+y+(180°-x)=180°$', size=30)
f6k31b = IH('f6k31b', '$y=x-60°$', size=32)
f6k31c = IH('f6k31c', '$x=60°+y$', size=32)
f6k31d = I('f6k31d', '$x=110°$: $\\ $(1) $70°$ ✗ $\\ $(2) $50°$ ✓\n(3) $80°$ ✗ $\\ $(4) $30°$ ✗', size=28)
# placement (right column, below the question text, above the choices): explicit board y
for _it, _y in [(f6g31, 200), (f6g31x, 200), (f6g31p, 200), (f6k31a, 230), (f6k31b, 285), (f6k31c, 545), (f6k31d, 500)]:
    _R(_it, _y)

video('solve-geo31-g031', 'solution', qid='geo31-g031', slides=[
    SM('Method 1 · The angle sum', 'The angle sum',
      L("A B C is an equilateral triangle. D, A and E lie on one line, E lies on B C, and F lies on the extension of B A "
        "beyond A. Based on this information and the information in the figure, which expression equals y?",
        pt('stem', 'A B C is an equilateral triangle', 'hl', 10.0), voice='calm', pause=0.5),
      L("There are no numbers in the figure, only two letters, x and y. We need to write y using x. [short pause] We'll "
        "solve it three ways, with the angle sum in a triangle, with an exterior angle, and by plugging in a number.",
        pt('fig: x', 'only two letters'), pt('fig: y', 'We need to write y')),
      L("[short pause] Let's start with the angle sum. Look at the small triangle A B E, the one between line A E and side "
        "B C. We'll write each of its three angles with what we know.", show(f6g31['line'], "Let's start with the angle sum"),
        show(f6g31['abe'], 'Look at the small triangle')),
      L("The first given, A B C is equilateral. All its sides are equal, and all its angles are equal, sixty degrees each. "
        "So the angle at B is sixty.", show(f6g31['b60'], 'So the angle at B is sixty')),
      L("Next, the angle at A, between A B and A E. It's vertical to y, because the lines D E and F B cross at A. Vertical "
        "angles are equal, so this angle is y too.", show(f6g31['ay'], 'It\'s vertical to y')),
      L("The last angle is at E, between E A and E B. Together with x it makes the straight line B C, so it's one hundred "
        "eighty minus x.", show(f6g31['e180'], "so it's one hundred"))),
    SM('Method 1 · The angle sum', 'The angle sum',
      L("The angles of a triangle add up to one hundred eighty, so sixty, plus y, plus one hundred eighty minus x, equals "
        "one hundred eighty. The bracket has a plus in front of it, so we can just drop it.", show(f6k31a, 'The angles of a triangle')),
      L("One hundred eighty is on both sides, so it cancels. Now move minus x to the right side as plus x, and move the "
        "sixty to the right side as minus sixty. So y equals x minus sixty. Choice number two is our answer.",
        show(f6k31b, 'So y equals x minus sixty'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · An exterior angle', 'An exterior angle',
      L("[pause] Another way makes the end shorter. Look at x again. It's outside the triangle A B E, next to its angle at "
        "E. So x is an exterior angle of that triangle.", show(f6g31x['line'], 'Look at x again')),
      L("An exterior angle equals the sum of the two angles of the triangle that are not next to it. Here those are sixty "
        "at B, and y at A. So x equals sixty plus y. Move the sixty across, and y equals x minus sixty. Choice number two "
        "again. Instead of completing x to one hundred eighty, we used the exterior angle rule.",
        show(f6g31x['far'], 'Here those are sixty'), show(f6k31c, 'So x equals sixty plus y'), mk('tick', 'choice 2', 'Choice number two again'))),
    SM('Method 3 · Plugging in a number', 'Plugging in a number',
      L("[pause] And a third way, plugging in a number. The answer is an expression that is true for every x that fits "
        "the figure. So it must also be true for one x that we choose. We choose a number for x, find y, and then check "
        "which choice gives that y."),
      L("Which letter do we choose? The one that appears in the choices, x. In the figure x is an obtuse angle, so we "
        "choose an easy obtuse number, one hundred ten.", show(f6g31p['line'], 'choose an easy obtuse number')),
      L("Now find y. Sixty plus what gives one hundred ten? Fifty. So y is fifty.", show(f6g31p['vals'], 'Sixty plus what gives')),
      L("Now put one hundred ten into each choice, and cross out everything that isn't fifty. Choice number one, one "
        "hundred eighty minus one hundred ten is seventy. Out. Choice number two, one hundred ten minus sixty is fifty. It "
        "stays. Choice number three, twice one hundred ten is two hundred twenty, minus one hundred forty is eighty. Out. "
        "Choice number four, one hundred forty minus one hundred ten is thirty. Out.", show(f6k31d, 'Now put one hundred ten'),
        mk('cross', 'choice 1', 'is seventy. Out'), mk('cross', 'choice 3', 'is eighty. Out'), mk('cross', 'choice 4', 'is thirty. Out')),
      L("Three choices are out, so choice number two is our answer. [pause] Okay. I'll see you in the next question.",
        mk('tick', 'choice 2', 'so choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g032 (Hebrew Q2)
# Hebrew (geo 1262-1290): alpha + beta = 180 - B; "if they were equal" each would be half, so alpha is above and beta below;
# alpha is the largest angle; the largest angle faces the longest side; eliminate AB, mark BC, no need to check the last.
# English: B = 50, so beta (below 65) may be above or below 50 - we don't need the full order.
# V3: the two letter angles in one colour (their sum), the "equal" picture of 65 and 65, alpha marked largest (orange),
# then the side across from it traced in the same orange (angle -> opposite side); each eliminated choice shows its own
# angle-side pair.
f6P, f6Q, f6R = (195.0, 290.0), (445.0, 290.0), (230.865, 34.804)      # A, B, C
f6g32_lines = f6_tri(f6P, f6Q, f6R) + f6_lab([f6P, f6Q, f6R], 'ABC', [(-18, 16), (18, 16), (0, -20)])
f6aPQ, f6aPR = 0.0, gdir(*f6P, *f6R)
f6aQP, f6aQR = 180.0, gdir(*f6Q, *f6R)
f6aRP, f6aRQ = gdir(*f6R, *f6P), gdir(*f6R, *f6Q)
f6g32 = GEO('f6g32', [
    ('line', f6g32_lines + [('arc', f6Q[0], f6Q[1], 30, f6aQR, 180, 'ink', '50°', 56)]),
    ('ab', [('arc', f6P[0], f6P[1], 30, 0, f6aPR, 'small', 'α', 48), ('arc', f6R[0], f6R[1], 30, f6aRP, f6aRQ, 'small', 'β', 48),
            ('txt', 565, 110, 'α + β = 130°', 'small', 26)]),
    ('big', [('arc', f6P[0], f6P[1], 30, 0, f6aPR, 'orange', 'α', 48), ('txt', 565, 155, 'α > 65°', 'orange', 26), ('txt', 565, 195, 'β < 65°', 'orange', 26)]),
], vb='150 0 520 330', w=520, title='Triangle ABC')
f6g32b = GEO('f6g32b', [
    ('line', f6g32_lines + [('arc', f6Q[0], f6Q[1], 30, f6aQR, 180, 'ink', '50°', 56), ('arc', f6R[0], f6R[1], 30, f6aRP, f6aRQ, 'small', 'β', 48),
                            ('arc', f6P[0], f6P[1], 30, 0, f6aPR, 'orange', 'α', 48), ('txt', 565, 130, 'α is the biggest', 'orange', 26)]),
    ('side', [('seg', f6Q[0], f6Q[1], f6R[0], f6R[1], 'orange', 7), ('txt', 565, 180, 'across from α:', 'orange', 24),
              ('txt', 565, 215, 'the longest side', 'orange', 24)]),
], vb='150 0 520 330', w=520, title='Triangle ABC: the biggest angle and the side across from it')
for _it, _y in [(f6g32, 200), (f6g32b, 200)]:
    _R(_it, _y)
video('solve-geo31-g032', 'solution', qid='geo31-g032', slides=[
    S('Order the angles',
      L("In triangle A B C in the accompanying figure, angle A B C is fifty degrees, and alpha is bigger than beta. Which side "
        "is necessarily the longest?", pt('stem', 'In triangle A B C', 'hl', 7.0), voice='calm', pause=0.5),
      L("There are no lengths at all, only angles. So we'll find the biggest angle, and then the side across from it.",
        pt('fig: α', 'only angles')),
      L("[short pause] The angles of a triangle add up to one hundred eighty. Angle B is fifty, so alpha and beta together "
        "are one hundred eighty minus fifty, which is one hundred thirty.", show(f6g32['line'], 'The angles of a triangle'),
        show(f6g32['ab'], 'so alpha and beta together')),
      L("Now the second given, alpha is bigger than beta. If they were equal, each would be half of one hundred thirty, "
        "which is sixty-five. But alpha is bigger, so alpha is more than sixty-five, and beta is less than sixty-five.",
        pt('stem: g2', 'alpha is bigger than beta')),
      L("So alpha is bigger than beta, and it's also bigger than fifty. Alpha is the biggest angle in the triangle. Beta "
        "could be above fifty or below it, but we don't need to know, because we only want the longest side.",
        show(f6g32['big'], 'Alpha is the biggest angle'))),
    S('The longest side',
      L("Remember, the longest side is across from the biggest angle. Alpha is at A, so the side across from it is B C. "
        "That's the longest side.", show(f6g32b['line'], 'the longest side is across from'), show(f6g32b['side'], 'so the side across from it')),
      L("Let's check the choices. Choice number one, A B. It's across from beta, and beta is smaller than alpha, so A B is "
        "shorter than B C. Out. Choice number two, A C. It's across from the fifty degrees at B, which is also smaller "
        "than alpha. Out.", mk('cross', 'choice 1', 'Choice number one, A B'), mk('cross', 'choice 2', 'which is also smaller')),
      L("Choice number three is B C, the longest side, so it's our answer. We found it for sure, so there's no need to "
        "check the last choice. [pause] Okay. I'll see you in the next question.",
        mk('tick', 'choice 3', 'Choice number three is B C'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g033 (Hebrew Q3)
# Hebrew (geo 1292-1360): a minimum-maximum question. Minimum: two sides together are longer than the third, so the
# perimeter is more than twice AB. The min-max insight: one choice is out as too small, so two must be too big - the
# smallest choice above the minimum. Then the full maximum: the obtuse angle is the largest, so AB is the longest side,
# so the perimeter is less than three times AB.
# V3: AC + BC traced against AB (two sides longer than the third) on the copy; a number line of the choices (ZL) with
# the lower limit, then the unknown upper limit, then the crosses; the full maximum: each short side marked "< 10".
f6U, f6V, f6W = (113.882, 257.294), (526.118, 257.294), (320.0, 102.706)   # A, B, C
f6g33_lines = (f6_tri(f6U, f6V, f6W) + f6_lab([f6U, f6V, f6W], 'ABC', [(-18, 14), (18, 14), (0, -22)])
               + [('txt', 320, 282, '10', 'ink', 24), ('arc', f6W[0], f6W[1], 41, gdir(*f6W, *f6U), gdir(*f6W, *f6V), 'orange', '> 90°', 66)])
f6g33 = GEO('f6g33', [
    ('line', f6g33_lines),
    ('two', [('path', [f6U, f6W, f6V], 'teal', 9), ('seg', f6U[0], f6U[1], f6V[0], f6V[1], 'orange', 6),
             ('txt', 470, 88, 'AC + BC > 10', 'small', 26)]),
], vb='80 40 480 260', w=470, title='Obtuse triangle ABC')
f6g33m = GEO('f6g33m', [
    ('line', f6g33_lines),
    ('max', [('seg', f6U[0], f6U[1], f6V[0], f6V[1], 'orange', 6), ('txt', 196, 165, '< 10', 'small', 26), ('txt', 448, 165, '< 10', 'small', 26)]),
], vb='80 40 480 260', w=470, title='Obtuse triangle ABC: AB is the longest side')
f6z33 = ZL('f6z33', 16, 38, [('low', [('cross', 20), ('below', 20, 'more than 20')]),
                              ('ch', [('pt', 24, '24'), ('pt', 30, '30'), ('pt', 35, '35')]),
                              ('up', [('shade', 20.4, 28.5), ('below', 28.5, 'top ?')]),
                              ('out', [('cross', 30), ('cross', 35)])],
           ticks=((20, '20'), (30, '30')), w=520, col=1, title='The choices on a number line')
f6k33a = IH('f6k33a', 'Perimeter $=10+AC+BC>10+10=20$', size=28)
f6k33b = IH('f6k33b', 'Perimeter $<10+10+10=30$', size=28)
for _it, _y in [(f6g33, 205), (f6g33m, 205), (f6k33a, 480), (f6k33b, 480), (f6z33, 260)]:
    _R(_it, _y)
video('solve-geo31-g033', 'solution', qid='geo31-g033', slides=[
    SM('A minimum and a maximum', 'The minimum',
      L("A B C is an obtuse triangle, with angle A C B bigger than ninety degrees, and A B is ten centimeters. Which of the "
        "following could be its perimeter, in centimeters?", pt('stem', 'A B C is an obtuse triangle', 'hl', 8.0), voice='calm', pause=0.5),
      L("We know only one side, so we can't calculate the perimeter exactly. But we can find a number the perimeter must be "
        "bigger than, and a number it must be smaller than. [short pause] So this is a minimum and maximum question.",
        pt('fig: 10', 'We know only one side')),
      L("[short pause] Start with the minimum. In any triangle, two sides together are always longer than the third side. "
        "So A C plus B C is more than A B, which is ten.", show(f6g33['line'], 'Start with the minimum'), show(f6g33['two'], 'So A C plus B C')),
      L("The perimeter is ten, plus A C plus B C. That's ten plus something bigger than ten, so the perimeter is more than "
        "twenty. A choice of twenty or less can't be the perimeter. Twenty itself is out.",
        show(f6k33a, 'so the perimeter is more than'), mk('cross', 'choice 2', 'Twenty itself is out'))),
    SM('A minimum and a maximum', 'Which choice is left?',
      L("Before we find the maximum, look at the choices that are left, twenty-four, thirty and thirty-five. Only one of "
        "them is right. The others are out because they're too big.", show(f6z33['line'], 'look at the choices that are left'),
        show(f6z33['low'], 'twenty-four, thirty'), show(f6z33['ch'], 'Only one of')),
      L("The perimeter can be anything between twenty and some top limit. If thirty-five were inside that range, then "
        "twenty-four and thirty, which are between twenty and thirty-five, would be inside it too, and we'd have three "
        "right answers. That can't happen. So the right answer has to be the smallest choice above twenty, twenty-four.",
        show(f6z33['up'], 'between twenty and some top limit'), show(f6z33['out'], 'So the right answer'),
        mk('tick', 'choice 3', 'the smallest choice above twenty'))),
    SM('A minimum and a maximum', 'The maximum',
      L("[pause] Let's check it with the full maximum too. The angle at C is more than ninety, so it's the biggest angle "
        "of the triangle. The longest side is across from the biggest angle, so A B is the longest side.",
        show(f6g33m['line'], 'The angle at C is more than'), show(f6g33m['max'], 'so A B is the longest side')),
      L("So A C is shorter than ten, and B C is shorter than ten. The perimeter is ten, plus less than ten, plus less than "
        "ten, so it's less than thirty. Thirty and thirty-five are too big, and only twenty-four is between twenty and "
        "thirty. Choice number three. [pause] Okay. I'll see you in the next question.",
        show(f6k33b, "so it's less than thirty"), mk('cross', 'choice 1', 'Thirty and thirty-five'),
        mk('cross', 'choice 4', 'are too big'), mk('tick', 'choice 3', 'Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g034 (Hebrew Q4)
# Hebrew (geo 1362-1396): recall the isosceles properties (equal legs, equal base angles, the altitude to the base is a
# symmetry line: also a bisector and a median); go through the choices from the quick ones: the angles (find the third),
# altitude + bisector (symmetry), the unclear median - skip it and hope to eliminate the next, the median that is also
# perpendicular (two equal angles on a straight line are 90 each), then mark the unclear one. The course adds why it can
# fail (a median that leans). English choice order: (1) angles, (2) median perpendicular, (3) median 7 to 10, (4) altitude
# that bisects. V3: a clean generic isosceles triangle built mark by mark (equal legs, equal base angles, the symmetry line
# with its three meanings); the leaning-median sketch built step by step (the side, its midpoint, the median, the two sides).
f6Ap, f6Bp, f6Cp, f6Mp = (320.0, 60.0), (200.0, 280.0), (440.0, 280.0), (320.0, 280.0)
f6g34 = GEO('f6g34', [
    ('line', f6_tri(f6Ap, f6Bp, f6Cp)),
    ('legs', [('tick', f6Ap[0], f6Ap[1], f6Bp[0], f6Bp[1], 1), ('tick', f6Ap[0], f6Ap[1], f6Cp[0], f6Cp[1], 1)]),
    ('base', [('arc', f6Bp[0], f6Bp[1], 34, 0, gdir(*f6Bp, *f6Ap), 'small'), ('arc', f6Cp[0], f6Cp[1], 34, gdir(*f6Cp, *f6Ap), 180, 'small')]),
    ('sym', [('seg', f6Ap[0], f6Ap[1], f6Mp[0], f6Mp[1], 'orange', 3, True), ('right', f6Mp[0], f6Mp[1], 0, 90, 16, 'orange'),
             ('tick', f6Bp[0], f6Bp[1], f6Mp[0], f6Mp[1], 2, 'orange'), ('tick', f6Mp[0], f6Mp[1], f6Cp[0], f6Cp[1], 2, 'orange'),
             ('arc', f6Ap[0], f6Ap[1], 44, gdir(*f6Ap, *f6Bp), 270, 'orange'), ('arc', f6Ap[0], f6Ap[1], 50, 270, gdir(*f6Ap, *f6Cp), 'orange')]),
], vb='170 40 300 260', w=330, title='An isosceles triangle and its symmetry line')
f6S0, f6S1, f6SM = (180.0, 280.0), (480.0, 280.0), (330.0, 280.0)
f6ST = (330.0 + 210 * 0.5, 280.0 - 210 * 3 ** 0.5 / 2)
f6g34c = GEO('f6g34c', [
    ('line', [('seg', f6S0[0], f6S0[1], f6S1[0], f6S1[1], 'ink', 3), ('dot', f6SM[0], f6SM[1]),
              ('txt', 255, 304, '5', 'ink', 24), ('txt', 405, 304, '5', 'ink', 24)]),
    ('med', [('seg', f6SM[0], f6SM[1], f6ST[0], f6ST[1], 'teal', 4), ('txt', 362, 175, '7', 'small', 26)]),
    ('sides', [('seg', f6ST[0], f6ST[1], f6S0[0], f6S0[1], 'ink', 3), ('seg', f6ST[0], f6ST[1], f6S1[0], f6S1[1], 'ink', 3),
               ('txt', 270, 160, 'long', 'red', 24), ('txt', 492, 180, 'short', 'red', 24)]),
], vb='160 70 360 250', w=330, title='A median that leans to one side')
f6k34a = IH('f6k34a', '(1) $180°-64°-58°=58°$', size=28)
f6k34b = I('f6k34b', '(4) altitude $=$ bisector: symmetry ✓', size=26)
f6k34c = I('f6k34c', '(2) $\\alpha+\\alpha=180°$: $\\ \\alpha=90°$ ✓', size=26)
for _it, _y in [(f6g34, 195), (f6k34a, 205), (f6k34b, 255), (f6k34c, 305), (f6g34c, 205)]:
    _R(_it, _y)
video('solve-geo31-g034', 'solution', qid='geo31-g034', slides=[
    S('Isosceles: what we know',
      L("Which of the following triangles is not necessarily isosceles?", pt('stem', 'Which of the following triangles', 'hl', 4.0),
        voice='calm', pause=0.5),
      L("Not necessarily isosceles means it may be isosceles, but it doesn't have to be. Three of the choices are always "
        "isosceles, and we're looking for the one that can fail. [short pause] First, let's remember what we know about an "
        "isosceles triangle.", pt('stem', 'Not necessarily isosceles means')),
      L("[short pause] In an isosceles triangle, the two legs are equal, and the base angles across from them are equal "
        "too.", show(f6g34['line'], 'In an isosceles triangle'), show(f6g34['legs'], 'the two legs are equal'),
        show(f6g34['base'], 'and the base angles')),
      L("And the altitude to the base is a line of symmetry. That one line is also the angle bisector, and also the median, "
        "because it cuts the base into two equal halves. Now let's go through the choices, starting with the ones we can "
        "decide quickly.", show(f6g34['sym'], 'the altitude to the base is a line of symmetry'))),
    S('Go through the choices',
      L("Choice number one, a triangle with angles sixty-four and fifty-eight. Find the third angle. One hundred eighty "
        "minus sixty-four is one hundred sixteen, and minus fifty-eight is fifty-eight. Two equal angles mean two equal "
        "sides, so it's always isosceles. Out.", show(f6k34a, 'Find the third angle'), mk('cross', 'choice 1', 'so it\'s always isosceles. Out')),
      L("Choice number four, an altitude that also bisects the angle it starts from. An altitude that is also a bisector is "
        "a line of symmetry, so the triangle is always isosceles. Out.", show(f6k34b, 'An altitude that is also a bisector'),
        mk('cross', 'choice 4', 'so the triangle is always isosceles. Out')),
      L("Choice number three, a median of seven to a side of ten. It's a median, so it cuts the side into two halves. But "
        "it's not given as an altitude or as a bisector, and it's not clear what to do with these numbers. So we skip it, "
        "go to the next choice, and hope to cross that one out.", pt('choice 3', 'a median of seven')),
      L("Choice number two, a median that is perpendicular to the side it meets. Sometimes the right angle is hidden: the "
        "median makes two equal angles, alpha and alpha, on a straight line. Two alphas are one hundred eighty, so each "
        "alpha is ninety. So the median is also an altitude. That's a line of symmetry, so the triangle is isosceles. Out.",
        show(f6k34c, 'Two alphas are one hundred eighty'), mk('cross', 'choice 2', 'so the triangle is isosceles. Out')),
      L("Three choices are out, so we mark choice number three, the one that wasn't clear.", mk('tick', 'choice 3', 'so we mark choice number three'))),
    S('Why it can fail',
      L("Let's see why it can fail. Here's a side of ten, and its middle point, five and five. From the middle, a median "
        "of seven, leaning to one side.", show(f6g34c['line'], "Here's a side of ten"), show(f6g34c['med'], 'a median of seven')),
      L("Its top is the third corner. Join it to both ends of the side. One side comes out long, and the other short. So a "
        "median of seven to a side of ten doesn't make the triangle isosceles. [pause] Okay. I'll see you in the next "
        "question.", show(f6g34c['sides'], 'Join it to both ends'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g035 (Hebrew Q5)
# Hebrew (geo 1398-1431): two right triangles; the third side with a Pythagorean triple instead of the full theorem
# (3-4-5, then 5-12-13 "hamsa, bat mitzvah, bar mitzvah"); the quadrilateral's area = the two triangles; side times its
# altitude over two, cancelling first. English: 12-16-20 (3-4-5 times four) and 20-48-52 (5-12-13 times four).
# V3: the quadrilateral copied bigger; triangle ABC tinted while it is used (its third side written when found); then
# triangle ACD in another tint; each area written inside its triangle; the hypotenuse trap shown on CD vs AD.
f6a, f6b, f6c, f6d = (274.114, 267.6), (304.149, 307.646), (357.543, 267.6), (357.543, 67.371)
f6g35_lines = ([('seg', f6a[0], f6a[1], f6b[0], f6b[1], 'ink', 3), ('seg', f6b[0], f6b[1], f6c[0], f6c[1], 'ink', 3),
                ('seg', f6c[0], f6c[1], f6d[0], f6d[1], 'ink', 3), ('seg', f6d[0], f6d[1], f6a[0], f6a[1], 'ink', 3),
                ('seg', f6a[0], f6a[1], f6c[0], f6c[1], 'ink', 3),
                ('right', f6b[0], f6b[1], gdir(*f6b, *f6a), gdir(*f6b, *f6c), 9), ('right', f6c[0], f6c[1], 90, 180, 9),
                ('txt', 262, 283, '12', 'ink', 17), ('txt', 340, 300, '16', 'ink', 17), ('txt', 300, 160, '52', 'ink', 17)]
               + f6_lab([f6a, f6b, f6c, f6d], 'ABCD', [(-13, 0), (0, 15), (13, 4), (12, -8)]))
f6V35 = dict(vb='235 45 425 300', w=520)


def f6_big35(p, k=2.3, o=(425.0, 130.0)):
    """the enlarged cut-out of triangle ABC (A lands on o)"""
    return (o[0] + (p[0] - f6a[0]) * k, o[1] + (p[1] - f6a[1]) * k)


f6A2, f6B2, f6C2 = f6_big35(f6a), f6_big35(f6b), f6_big35(f6c)
f6g35_big = ([('tint', [f6A2, f6B2, f6C2], 'teal')] + f6_tri(f6A2, f6B2, f6C2, 'small', 4)
             + [('right', f6B2[0], f6B2[1], gdir(*f6B2, *f6A2), gdir(*f6B2, *f6C2), 14, 'small'),
                ('txt', f6A2[0] - 16, f6A2[1], 'A', 'ink', 24, True), ('txt', f6B2[0], f6B2[1] + 20, 'B', 'ink', 24, True),
                ('txt', f6C2[0] + 16, f6C2[1], 'C', 'ink', 24, True), ('txt', (f6A2[0] + f6B2[0]) / 2 - 16, (f6A2[1] + f6B2[1]) / 2 + 10, '12', 'ink', 22), ('txt', (f6B2[0] + f6C2[0]) / 2 + 18, (f6B2[1] + f6C2[1]) / 2 + 10, '16', 'ink', 22)])
f6g35_abc_ol = [('seg', f6a[0], f6a[1], f6b[0], f6b[1], 'small', 5), ('seg', f6b[0], f6b[1], f6c[0], f6c[1], 'small', 5),
                ('seg', f6c[0], f6c[1], f6a[0], f6a[1], 'small', 5)]
f6g35_acd_ol = [('seg', f6a[0], f6a[1], f6c[0], f6c[1], 'orange', 4), ('seg', f6c[0], f6c[1], f6d[0], f6d[1], 'orange', 4),
                ('seg', f6d[0], f6d[1], f6a[0], f6a[1], 'orange', 4)]
f6DIM35 = ('dim', 235, 45, 165, 300)
f6g35 = GEO('f6g35', [
    ('line', f6g35_lines),
    ('t1', [('tint', [f6a, f6b, f6c], 'teal')] + f6g35_abc_ol),
    ('cut', [f6DIM35] + f6g35_abc_ol + f6g35_big),
    ('t1v', [('txt', 316, 259, '20', 'small', 18), ('txt', (f6A2[0] + f6C2[0]) / 2, f6A2[1] - 14, '20', 'small', 24),
             ('txt', 540, 75, '12, 16, 20: 3, 4, 5 times 4', 'small', 20)]),
    ('t2', [('tint', [f6a, f6c, f6d], 'orange')] + f6g35_acd_ol + [('txt', 372, 168, '48', 'orange', 18),
            ('txt', 540, 290, '20, 48, 52:', 'orange', 22), ('txt', 540, 318, '5, 12, 13 times 4', 'orange', 22)]),
], title='Two right triangles: ABC and ACD', **f6V35)
f6g35b = GEO('f6g35b', [
    ('line', f6g35_lines + [('tint', [f6a, f6b, f6c], 'teal'), ('tint', [f6a, f6c, f6d], 'orange'), f6DIM35] + f6g35_abc_ol + f6g35_acd_ol
             + f6g35_big + [('txt', 316, 259, '20', 'small', 18), ('txt', 372, 168, '48', 'orange', 18),
                            ('txt', (f6A2[0] + f6C2[0]) / 2, f6A2[1] - 14, '20', 'small', 24)]),
    ('a1', [('txt', (f6A2[0] + f6B2[0] + f6C2[0]) / 3, (f6A2[1] + f6B2[1] + f6C2[1]) / 3 - 4, '96', 'small', 24), ('txt', 540, 75, '12 × 16 ÷ 2 = 96', 'small', 22)]),
    ('a2', [('txt', 330, 215, '480', 'orange', 18), ('txt', 540, 290, '20 × 48 ÷ 2 = 480', 'orange', 22)]),
    ('sum', [('txt', 540, 325, '96 + 480 = 576', 'ink', 26)]),
], title='The two areas', **f6V35)
for _it, _y in [(f6g35, 200), (f6g35b, 200)]:
    _R(_it, _y)
video('solve-geo31-g035', 'solution', qid='geo31-g035', slides=[
    S('Two triangles, two triples',
      L("In the accompanying figure, triangles A B C and A C D are right triangles. The marked lengths are in "
        "centimeters. What is the area of quadrilateral A B C D, in square centimeters?",
        pt('stem', 'In the accompanying figure', 'hl', 8.0), voice='calm', pause=0.5),
      L("The quadrilateral is made of two right triangles. If we know their sides, we can find both areas. [short pause] "
        "In a right triangle, when two sides are given, we can always find the third with the Pythagorean theorem. But "
        "with Pythagorean triples it's much faster.", show(f6g35['line'], 'The quadrilateral is made of two right triangles')),
      L("[short pause] Start with triangle A B C. Its legs are twelve and sixteen. That's three, four, five, times four, so "
        "the hypotenuse A C is five times four, which is twenty. No need for the full theorem.",
        show(f6g35['t1'], 'Start with triangle A B C'), show(f6g35['cut'], 'Its legs are twelve'),
        show(f6g35['t1v'], "That's three, four, five")),
      L("Now triangle A C D. The leg A C is twenty, and the hypotenuse A D is fifty-two. Another triple we learned is five, "
        "twelve, thirteen. Times four, that's twenty, forty-eight and fifty-two. We have twenty and fifty-two, so the "
        "missing leg C D is forty-eight.", pt('fig: 52', 'the hypotenuse A D is fifty-two'),
        show(f6g35['t2'], 'Times four'))),
    S('The two areas',
      L("The area of a triangle is a side times the altitude to it, over two. In a right triangle, the two legs are a side "
        "and its altitude. Triangle A B C, twelve times sixteen over two. Cancel first, sixteen over two is eight, and "
        "eight times twelve is ninety-six.", show(f6g35b['line'], 'The area of a triangle'), show(f6g35b['a1'], 'Triangle A B C, twelve times sixteen')),
      L("Triangle A C D, twenty times forty-eight over two. Cancel first, forty-eight over two is twenty-four, and "
        "twenty-four times twenty is four hundred eighty.", show(f6g35b['a2'], 'Triangle A C D, twenty times')),
      L("The quadrilateral is the two triangles together, ninety-six plus four hundred eighty, which is five hundred "
        "seventy-six. Choice number three is our answer.", show(f6g35b['sum'], 'ninety-six plus four hundred eighty'),
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Careful with choice number two. Fifty-two is the hypotenuse of triangle A C D, across from the right angle at C, "
        "so it's not a leg. If you use it as the altitude, you get six hundred sixteen. [pause] Okay. I'll see you in the "
        "next question.", mk('cross', 'choice 2', 'Careful with choice number two'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g036 (Hebrew Q6)
# Hebrew (geo 1433-1460): moving between the golden and the silver triangles: ABD has 30 and 90, so 60 - golden; from the
# hypotenuse to the short leg divide by 2, from the short leg to the long leg times root 3; BCD is silver (45-90-45);
# from the hypotenuse to a leg divide by root 2 - "ignore the root, divide, stick the root back on"; the perimeter.
# V3: triangle ABD tinted, its angles completed and each side written as found; then focus moves to BCD (its own tint,
# ABD dimmed back), BD traced as its hypotenuse; the outside path traced for the perimeter, BD left out.
f6p, f6q, f6r, f6s = (268.471, 61.615), (268.471, 240.118), (320.0, 291.647), (371.529, 240.118)   # A, B, C, D
f6g36_lines = ([('seg', f6p[0], f6p[1], f6q[0], f6q[1], 'ink', 3), ('seg', f6q[0], f6q[1], f6r[0], f6r[1], 'ink', 3),
                ('seg', f6r[0], f6r[1], f6s[0], f6s[1], 'ink', 3), ('seg', f6s[0], f6s[1], f6p[0], f6p[1], 'ink', 3),
                ('seg', f6q[0], f6q[1], f6s[0], f6s[1], 'ink', 3),
                ('right', f6q[0], f6q[1], 0, 90, 10), ('right', f6r[0], f6r[1], 45, 135, 10),
                ('arc', f6p[0], f6p[1], 40, gdir(*f6p, *f6q), gdir(*f6p, *f6s), 'ink', '30°', 58), ('txt', 343, 145, '20', 'ink', 20)]
               + f6_lab([f6p, f6q, f6r, f6s], 'ABCD', [(-14, -6), (-16, 4), (0, 18), (16, 4)]))
f6V36 = dict(vb='215 35 420 290', w=520)
f6g36 = GEO('f6g36', [
    ('line', f6g36_lines),
    ('abd', [('tint', [f6p, f6q, f6s], 'teal'), ('arc', f6s[0], f6s[1], 26, gdir(*f6s, *f6p), 180, 'small', '60°', 44)]),
    ('bd', [('txt', 294, 231, '10', 'small', 20), ('txt', 530, 110, 'BD = 20 ÷ 2 = 10', 'small', 22)]),
    ('ab', [('txt', 238, 150, '10√3', 'small', 20), ('txt', 530, 150, 'AB = 10√3', 'small', 22)]),
], title='Triangle ABD, the golden triangle', **f6V36)
def f6_big36(p, k=1.7, o=(430.0, 198.0)):
    """the enlarged cut-out of triangle BCD (B lands on o)"""
    return (o[0] + (p[0] - f6q[0]) * k, o[1] + (p[1] - f6q[1]) * k)


f6B3, f6C3, f6D3 = f6_big36(f6q), f6_big36(f6r), f6_big36(f6s)
f6g36_bcd_ol = [('seg', f6q[0], f6q[1], f6r[0], f6r[1], 'orange', 4), ('seg', f6r[0], f6r[1], f6s[0], f6s[1], 'orange', 4),
                ('seg', f6q[0], f6q[1], f6s[0], f6s[1], 'orange', 5)]
f6g36b = GEO('f6g36b', [
    ('line', f6g36_lines + [('txt', 294, 231, '10', 'small', 20), ('txt', 238, 150, '10√3', 'small', 20)]),
    ('bcd', [('tint', [f6q, f6r, f6s], 'orange')] + f6g36_bcd_ol),
    ('cut', [('dim', 215, 35, 175, 290)] + f6g36_bcd_ol + [('tint', [f6B3, f6C3, f6D3], 'orange')] + f6_tri(f6B3, f6C3, f6D3, 'orange', 4)
            + [('right', f6C3[0], f6C3[1], 45, 135, 14, 'orange'), ('arc', f6B3[0], f6B3[1], 30, 315, 360, 'orange', '45°', 52),
               ('arc', f6D3[0], f6D3[1], 30, 180, 225, 'orange', '45°', 52), ('txt', f6B3[0] - 16, f6B3[1], 'B', 'ink', 24, True),
               ('txt', f6C3[0], f6C3[1] + 20, 'C', 'ink', 24, True), ('txt', f6D3[0] + 16, f6D3[1], 'D', 'ink', 24, True),
               ('txt', (f6B3[0] + f6D3[0]) / 2, f6B3[1] - 14, '10', 'small', 24)]),
    ('legs', [('txt', (f6B3[0] + f6C3[0]) / 2 - 26, (f6B3[1] + f6C3[1]) / 2 + 12, '5√2', 'orange', 22),
              ('txt', (f6D3[0] + f6C3[0]) / 2 + 26, (f6D3[1] + f6C3[1]) / 2 + 12, '5√2', 'orange', 22), ('txt', 280, 280, '5√2', 'orange', 16),
              ('txt', 362, 280, '5√2', 'orange', 16), ('txt', 530, 80, '10 ÷ √2 = 5√2', 'orange', 22)]),
    ('per', [('path', [f6p, f6q, f6r, f6s, f6p], 'teal', 8), ('txt', 530, 115, '20 + 10√3 + 5√2 + 5√2', 'ink', 20),
             ('txt', 530, 145, '= 20 + 10√3 + 10√2', 'ink', 22)]),
], title='Triangle BCD, the silver triangle, and the perimeter', **f6V36)
for _it, _y in [(f6g36, 200), (f6g36b, 200)]:
    _R(_it, _y)
video('solve-geo31-g036', 'solution', qid='geo31-g036', slides=[
    S('The golden triangle',
      L("In the accompanying figure, triangles A B D and B C D are right triangles. Given: A D is twenty centimeters. "
        "What is the perimeter of quadrilateral A B C D, in centimeters?", pt('stem', 'In the accompanying figure', 'hl', 7.0),
        voice='calm', pause=0.5),
      L("This question is about moving from a golden triangle to a silver triangle. [short pause] We'll find the sides one "
        "triangle at a time.", show(f6g36['line'], 'moving from a golden triangle')),
      L("[short pause] Look at triangle A B D. The angle at A is thirty degrees, and the angle at B is ninety, so the angle "
        "at D is sixty. It's a golden triangle, thirty, sixty, ninety.", show(f6g36['abd'], 'Look at triangle A B D'),
        pt('fig: 30°', 'The angle at A is thirty')),
      L("Its hypotenuse is A D, which is twenty. In a golden triangle, to go from the hypotenuse to the short leg, we "
        "divide by two. The short leg is across from the thirty degrees, so B D is ten.", pt('fig: 20', 'Its hypotenuse is A D'),
        show(f6g36['bd'], 'so B D is ten')),
      L("To go from the short leg to the long leg, across from the sixty, we multiply by root three. So A B is ten root "
        "three.", show(f6g36['ab'], 'So A B is ten root three'))),
    S('The silver triangle',
      L("Now triangle B C D. It's a silver triangle, forty-five, ninety, forty-five, a right isosceles triangle. Careful: "
        "in the first triangle B D was a leg, but here it's the hypotenuse, across from the right angle at C.",
        show(f6g36b['line'], 'Now triangle B C D'), show(f6g36b['bcd'], "It's a silver triangle"), show(f6g36b['cut'], 'Careful')),
      L("From the hypotenuse to a leg, we divide by root two. How much is ten over root two? The way we learned: ignore "
        "the root, ten over two is five, and stick the root two back on. Five root two. So B C and C D are each five root "
        "two.", show(f6g36b['legs'], 'Five root two. So')),
      L("Now the perimeter, only the outside sides, not B D. Twenty, plus ten root three, plus five root two, plus five "
        "root two. Five root two plus five root two is ten root two. So the perimeter is twenty plus ten root three plus "
        "ten root two. Choice number four is our answer. [pause] Okay. I'll see you in the next question.",
        show(f6g36b['per'], 'Now the perimeter'),
        mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# =================================================================================================================
# Topic-31 advanced block, part 2 (fragment f7, 2026-10-14): geo31-g037, g038, g039, g040 (Hebrew geo 1463-1727).
# Question figure on the left (FIG_LEFT), our colour copy of it on the right, built step by step (Rule V3).
# =================================================================================================================
FIG_LEFT.update({'solve-geo31-g037', 'solve-geo31-g038', 'solve-geo31-g039', 'solve-geo31-g040'})

# ------------------------------------------------------------------------------------------------ geo31-g037 (Hebrew: the shaded area, DBC equilateral)
# Hebrew (geo 1463-1533): shaded areas are common; subtract areas (what minus what); complete the data: the altitude of
# the equilateral DBC is also a median (BE = EC), DE from the gold triangle (short leg x root 3); big minus small; the
# equilateral area formula a² root 3 / 4 as a check; then the insight: rotate, the shaded part is two triangles ADC and
# ADB, base AD, the OUTSIDE altitude from C is EC; symmetric, so twice. English numbers: BE = 4, AD = 3 root 3.
# V3: the shaded part tinted; ABC traced (the big one), DBC tinted (the part we take away); BE and EC ticked equal; FOCUS
# on triangle DEC (tinted) with its 30, 60 and right angle; values written on the figure when found. Method 2 on a new
# copy: ADC tinted, its base AD traced, the outside height EC traced red with the right angle; then ADB, the mirror.
f7A, f7B, f7C, f7D, f7E = (320, 58.07), (240.36, 299.46), (399.64, 299.46), (320, 161.52), (320, 299.46)
f7_37base = [('seg', f7A[0], f7A[1], f7B[0], f7B[1]), ('seg', f7A[0], f7A[1], f7C[0], f7C[1]), ('seg', f7B[0], f7B[1], f7C[0], f7C[1]),
             ('seg', f7D[0], f7D[1], f7B[0], f7B[1]), ('seg', f7D[0], f7D[1], f7C[0], f7C[1]),
             ('seg', f7A[0], f7A[1], f7E[0], f7E[1], 'ink', 2.5, True), ('right', f7E[0], f7E[1], 0, 90, 12),
             ('tint', [f7A, f7B, f7D], 'teal'), ('tint', [f7A, f7C, f7D], 'teal'),
             ('txt', 320, 40, 'A', 'ink', 24, True), ('txt', 224, 314, 'B', 'ink', 24, True), ('txt', 416, 314, 'C', 'ink', 24, True),
             ('txt', 338, 160, 'D', 'ink', 24, True), ('txt', 320, 330, 'E', 'ink', 24, True), ('txt', 280, 318, '4', 'ink', 22)]
f7g37 = GEO('f7g37', [
    ('line', f7_37base),
    ('big', [('path', [f7A, f7B, f7C, f7A], 'orange', 7)]),
    ('small', [('tint', [f7D, f7B, f7C], 'red'), ('txt', 320, 262, '−', 'red', 34)]),
    ('ec', [('tick', f7B[0], f7B[1], f7E[0], f7E[1]), ('tick', f7E[0], f7E[1], f7C[0], f7C[1]), ('txt', 362, 318, '4', 'teal', 22)]),
    ('dec', [('tint', [f7D, f7E, f7C], 'orange'), ('arc', f7C[0], f7C[1], 26, 120, 180, 'small', '60°', 44),
             ('arc', f7D[0], f7D[1], 28, 270, 300, 'small', '30°', 46)]),
    ('de', [('txt', 286, 232, '4√3', 'orange', 22)]),
    ('ae', [('txt', 270, 110, '3√3', 'ink', 22), ('txt', 425, 120, 'AE = 7√3', 'red', 22)]),
], vb='180 22 290 320', w=290, title='Triangle ABC with the equilateral triangle DBC')
f7g37b = GEO('f7g37b', [
    ('line', f7_37base),
    ('adc', [('tint', [f7A, f7C, f7D], 'orange'), ('path', [f7A, f7D], 'teal', 8), ('txt', 292, 110, '3√3', 'teal', 22)]),
    ('h', [('seg', f7E[0], f7E[1], f7C[0], f7C[1], 'red', 6), ('seg', f7D[0], f7D[1], f7E[0], f7E[1], 'teal', 3, True),
           ('txt', 362, 318, '4', 'red', 24)]),
    ('v1', [('txt', 338, 214, '6√3', 'orange', 20)]),
    ('adb', [('tint', [f7A, f7B, f7D], 'orange'), ('txt', 302, 214, '6√3', 'orange', 20)]),
], vb='180 22 290 320', w=240, title='The shaded part as two triangles')
f7k2 = I('f7k2', '$S_{ABC}=\\frac{8\\cdot7\\sqrt3}{2}=28\\sqrt3$', size=32)
f7k3 = I('f7k3', '$S_{DBC}=\\frac{8\\cdot4\\sqrt3}{2}=16\\sqrt3$', size=32)
f7k4 = I('f7k4', 'or $\\ \\frac{a^2\\sqrt3}{4}=\\frac{64\\sqrt3}{4}=16\\sqrt3$', size=30)
f7k5 = I('f7k5', '$28\\sqrt3-16\\sqrt3=12\\sqrt3$', size=32)
f7k6 = I('f7k6', '$S_{ADC}=\\frac{3\\sqrt3\\cdot4}{2}=6\\sqrt3$', size=26)
f7k7 = I('f7k7', '$2\\cdot6\\sqrt3=12\\sqrt3$', size=26)
f7s37 = I('f7s37', 'So far: $\\ BC=8,\\ \\ DE=4\\sqrt3,\\ \\ AE=7\\sqrt3$', size=26)   # V2, in the right column (a carry box would sit on the question figure)
video('solve-geo31-g037', 'solution', qid='geo31-g037', slides=[
    SM('Method 1 · Subtract areas', 'Big minus small',
      L("In triangle A B C, A E is the altitude to B C. Point D lies on A E, and D B C is an equilateral triangle. Given: B E is "
        "four centimeters, and A D is three root three centimeters. What is the shaded area, in square centimeters?",
        pt('stem', 'In triangle A B C', 'hl', 10.0), voice='calm', pause=0.5),
      L("Shaded areas are quite common on the exam. The main way to handle them is to subtract areas. We ask what the "
        "shaded part is made of, or what minus what gives it. [short pause] We'll solve it two ways, by subtracting areas, "
        "and then with a shorter insight.", pt('fig: shaded', 'what the shaded part is made of')),
      L("[short pause] Here, take the big triangle A B C, and take away the white triangle D B C. What's left is exactly the "
        "shaded part.", show(f7g37['line'], 'take the big triangle A B C'), show(f7g37['big'], 'and take away'),
        show(f7g37['small'], 'the white triangle D B C')),
      L("To find these areas, we first complete the data. B E is four, so E C is four too. Why? D B C is equilateral, and in an "
        "equilateral triangle the altitude is also a median. It cuts the base into two equal halves. So B C is eight.",
        show(f7g37['ec'], 'so E C is four too')),
      L("Now the altitude D E. Look at the small triangle D E C on the right. The altitude splits the equilateral triangle "
        "into two gold triangles, thirty, sixty, ninety. The short leg, opposite the thirty, is E C, four. The other leg is "
        "the short leg times root three, so D E is four root three.", show(f7g37['dec'], 'Look at the small triangle D E C'),
        show(f7g37['de'], 'so D E is four root three')),
      L("And the whole altitude A E is A D plus D E, three root three plus four root three, which is seven root three.",
        show(f7g37['ae'], 'which is seven root three'))),
    SM('Method 1 · Subtract areas', 'Big minus small',
      L("Now the big triangle. Its base B C is eight, and its height A E is seven root three. Eight times seven root three, "
        "over two. Eight over two is four, and four times seven root three is twenty-eight root three.", show(f7s37, 'Now the big triangle'),
        show(f7k2, 'Its base B C is eight')),
      L("The white triangle has the same base, eight, and its height D E is four root three. Eight times four root three, "
        "over two, is sixteen root three.", show(f7k3, 'The white triangle')),
      L("There's another way to get the white area, because it's equilateral. The area of an equilateral triangle is its "
        "side squared, times root three, over four. Eight squared is sixty-four, and sixty-four over four is sixteen. So "
        "again sixteen root three.", show(f7k4, 'The area of an equilateral triangle')),
      L("Now subtract. Twenty-eight root three minus sixteen root three is twelve root three. Choice number two is our "
        "answer.", show(f7k5, 'Now subtract'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · Two triangles', 'Two triangles',
      L("[pause] There's a shorter way, with an insight. Turn your head a little. The shaded part is two triangles, A D C on "
        "the right, and A D B on the left.", show(f7g37b['line'], 'There\'s a shorter way'), show(f7g37b['adc'], 'A D C on the right')),
      L("For the area of A D C we need a base and its height. The base is given, A D, three root three. The height to it, "
        "from C, is outside the triangle, because A D C has an obtuse angle at D. We extend the base A D down to E. E C is "
        "perpendicular to that line, and E C is four, the same as B E. So the height is four.", show(f7g37b['h'], 'We extend the base A D')),
      L("Three root three times four, over two, is six root three. That's one shaded triangle. The other one, A D B, is its "
        "mirror image, so it's six root three too. Twice six root three is twelve root three, choice number two again, "
        "with almost no calculating.", show(f7g37b['v1'], 'Three root three times four'), show(f7g37b['adb'], 'The other one, A D B'),
        show(f7k6, 'so it\'s six root three too'),
        show(f7k7, 'Twice six root three'), mk('tick', 'choice 2', 'choice number two again')),
      L("Careful, six root three, choice number three, is only one of the two shaded triangles. [pause] Okay. I'll see you "
        "in the next question.", mk('cross', 'choice 3', 'six root three, choice number three'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g038 (Hebrew: area 18, DC = 2BD)
# Hebrew (geo 1535-1593): math first (BD = x, DC = 2x, the altitude h from A, x·h from the given area, then each area; the
# left triangle's altitude is outside but it's the same altitude), then the insight: area ratio (same height, base twice as
# big, area twice as big), and splitting with a median into equal triangles. English: area 56, DC = 3BD.
# V3: the altitude h drawn dashed from A (point at A first), the bases labelled; each triangle tinted as its area is
# found; method 2 on a new copy: the two parts tinted in two colours, then DC cut into three pieces as long as BD, the
# lines from A drawn in, each small triangle labelled 14.
f7a, f7b, f7c, f7d, f7f = (280.8, 96), (96, 264), (544, 264), (208, 264), (280.8, 264)
f7_38base = [('seg', f7a[0], f7a[1], f7b[0], f7b[1]), ('seg', f7a[0], f7a[1], f7c[0], f7c[1]), ('seg', f7b[0], f7b[1], f7c[0], f7c[1]),
             ('seg', f7a[0], f7a[1], f7d[0], f7d[1]),
             ('txt', 280.8, 76, 'A', 'ink', 26, True), ('txt', 78, 280, 'B', 'ink', 26, True), ('txt', 562, 280, 'C', 'ink', 26, True),
             ('txt', 208, 288, 'D', 'ink', 26, True), ('txt', 152, 288, 'x', 'ink', 24, True), ('txt', 400, 288, '3x', 'ink', 24, True)]
f7g38 = GEO('f7g38', [
    ('line', f7_38base),
    ('h', [('dot', f7a[0], f7a[1]), ('seg', f7a[0], f7a[1], f7f[0], f7f[1], 'teal', 3, True), ('right', f7f[0], f7f[1], 0, 90, 12),
           ('txt', 296, 180, 'h', 'teal', 26, True)]),
], vb='60 60 520 245', w=500, title='Triangle ABC with D on BC')
f7_38h = [('seg', f7a[0], f7a[1], f7f[0], f7f[1], 'teal', 3, True), ('right', f7f[0], f7f[1], 0, 90, 12), ('txt', 296, 180, 'h', 'teal', 26, True)]
f7g38c = GEO('f7g38c', [
    ('line', f7_38base + f7_38h + [('txt', 490, 88, 'So far: x · h = 28', 'ink', 22)]),
    ('adc', [('tint', [f7a, f7d, f7c], 'orange'), ('txt', 400, 230, '42', 'orange', 28)]),
    ('abd', [('tint', [f7a, f7b, f7d], 'teal'), ('txt', 172, 236, '14', 'teal', 28)]),
], vb='60 60 520 245', w=400, title='The two triangles ABD and ADC')
f7g38b = GEO('f7g38b', [
    ('line', f7_38base),
    ('two', [('tint', [f7a, f7b, f7d], 'teal'), ('tint', [f7a, f7d, f7c], 'orange'), ('txt', 172, 236, '1 part', 'teal', 20),
             ('txt', 400, 236, '3 parts', 'orange', 22)]),
    ('cut', [('dim', 60, 210, 520, 40), ('seg', f7a[0], f7a[1], 320, 264, 'orange', 3, True), ('seg', f7a[0], f7a[1], 432, 264, 'orange', 3, True),
             ('tick', 96, 264, 208, 264), ('tick', 208, 264, 320, 264), ('tick', 320, 264, 432, 264), ('tick', 432, 264, 544, 264)]),
    ('val', [('txt', 168, 240, '14', 'teal', 24), ('txt', 264, 240, '14', 'orange', 24), ('txt', 350, 240, '14', 'orange', 24),
             ('txt', 445, 240, '14', 'orange', 24)]),
], vb='60 60 520 245', w=440, title='DC cut into three pieces as long as BD')
f7m1 = I('f7m1', '$S_{ABC}=\\frac{4x\\cdot h}{2}=56$', size=32)
f7m2 = IH('f7m2', '$x\\cdot h=28$', size=32)
f7m3 = I('f7m3', '$S_{ADC}=\\frac{3x\\cdot h}{2}=\\frac{3\\cdot28}{2}=42$', size=30)
f7m4 = I('f7m4', '$S_{ABD}=\\frac{x\\cdot h}{2}=\\frac{28}{2}=14$', size=30)
f7m5 = I('f7m5', '$42-14=28$', size=30)
f7m6 = I('f7m6', '$56\\div4=14$: $\\ 3\\cdot14=42$, $\\ 42-14=28$', size=30)
video('solve-geo31-g038', 'solution', qid='geo31-g038', slides=[
    SM('Method 1 · Algebra', 'Letters for the sides',
      L("Triangle A B C has an area of fifty-six square centimeters. Point D lies on B C, and D C is three times B D. What is "
        "the difference between the areas of A D C and A B D, in square centimeters?", pt('stem', 'Triangle A B C', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("We know only the area of the whole triangle and how B C is split. [short pause] We'll solve it two ways, with "
        "algebra, and then with an insight about area ratios."),
      L("[short pause] Neither the base nor the height is given, so we give them letters. B D is x. D C is three times B D, so "
        "D C is three x. Now draw the altitude from vertex A down to the line B C, and call it h.",
        show(f7g38['line'], 'so we give them letters'), show(f7g38['h'], 'Now draw the altitude')),
      L("The whole triangle A B C has the base B C, which is x plus three x, four x. Its height is h. So its area is four x "
        "times h, over two, and that's fifty-six. Two x h is fifty-six, so x h is twenty-eight. Let's keep that.",
        show(f7m1, 'So its area is'), show(f7m2, 'so x h is twenty-eight'))),
    SM('Method 1 · Algebra', 'Each area',
      L("Now A D C. Its base is three x, and its height is the same h. And A B D. Its base is x. A B D has an obtuse angle at D, "
        "so its height falls outside it, but it's the same altitude h from A.", show(f7g38c['line'], 'Now A D C'),
        show(f7g38c['adc'], 'Its base is three x'), show(f7g38c['abd'], 'And A B D')),
      L("The area of A D C is three x h over two. That's three times twenty-eight over two, which is forty-two. The area of "
        "A B D is x h over two, twenty-eight over two, which is fourteen.", show(f7m3, 'The area of A D C'),
        show(f7m4, 'The area of A B D')),
      L("The difference is forty-two minus fourteen, which is twenty-eight. Choice number three is our answer.",
        show(f7m5, 'The difference is'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Area ratio', 'Same height',
      L("[pause] Now the insight, about area ratios. Two triangles with the same base and the same height have the same "
        "area. And if the height is the same but one base is three times as long, that area is three times as big.",
        show(f7g38b['line'], 'Now the insight')),
      L("That's exactly our case. A B D and A D C have the same height, the altitude from A, and D C is three times B D. So A D C "
        "is three parts and A B D is one part. Together that's four equal parts of fifty-six.",
        show(f7g38b['two'], 'A B D and A D C have the same height')),
      L("You can even see the parts. Cut D C into three pieces, each as long as B D, and draw lines from A to the cuts. Now "
        "there are four small triangles, all with the same base and the same height, so they all have the same area. Fifty-six "
        "over four is fourteen.", show(f7g38b['cut'], 'Cut D C into three pieces'), show(f7g38b['val'], 'Fifty-six over four')),
      L("A D C has three of them, forty-two, and A B D has one, fourteen. The difference is two pieces, twenty-eight, choice "
        "number three. [pause] Okay. I'll see you in the next question.", show(f7m6, 'A D C has three of them'),
        mk('tick', 'choice 3', 'The difference is two pieces'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g039 (Hebrew: four squares, AEF minus AFG)
# Hebrew (geo 1595-1663): the full math (AE = two square diagonals, silver triangles; AF from Pythagoras; both perimeters,
# subtract), then the insight (shared sides cancel: AF in both, EF = FG), then the nuance: with seconds left, eliminate
# by the size (sign) of the choices. English: squares of side 5. No decimal estimates here: whole-number benchmarks only.
# V3: the four squares with every side 5; FOCUS on one small square (tinted), its diagonal traced, 5 root 2 written twice;
# the right triangle AGF tinted, AF traced; method 2 on a new copy: the two triangles outlined in two colours, the shared
# AF traced, EF and FG ticked equal, then AE and AG traced; method 3: typed sign checks.
f7_A, f7_G, f7_F, f7_E, f7_C, f7_H, f7_D, f7_O, f7_L = (210.5, 70.5), (429.5, 70.5), (429.5, 180), (429.5, 289.5), (210.5, 289.5), \
    (320, 70.5), (320, 289.5), (320, 180), (210.5, 180)
f7_39base = [('seg', f7_A[0], f7_A[1], f7_G[0], f7_G[1]), ('seg', f7_G[0], f7_G[1], f7_E[0], f7_E[1]), ('seg', f7_E[0], f7_E[1], f7_C[0], f7_C[1]),
             ('seg', f7_C[0], f7_C[1], f7_A[0], f7_A[1]), ('seg', f7_L[0], f7_L[1], f7_F[0], f7_F[1]), ('seg', f7_H[0], f7_H[1], f7_D[0], f7_D[1]),
             ('seg', f7_A[0], f7_A[1], f7_E[0], f7_E[1]), ('seg', f7_A[0], f7_A[1], f7_F[0], f7_F[1]),
             ('txt', 192, 56, 'A', 'ink', 24, True), ('txt', 448, 56, 'G', 'ink', 24, True), ('txt', 450, 180, 'F', 'ink', 24, True),
             ('txt', 448, 306, 'E', 'ink', 24, True), ('txt', 192, 306, 'C', 'ink', 24, True), ('txt', 265, 310, '5', 'ink', 22)]
f7g39 = GEO('f7g39', [
    ('line', f7_39base),
    ('sq', [('tint', [f7_A, f7_H, f7_O, f7_L], 'teal'), ('path', [f7_A, f7_O], 'teal', 8), ('txt', 250, 145, '5√2', 'teal', 22)]),
    ('sq2', [('tint', [f7_O, f7_F, f7_E, f7_D], 'teal'), ('path', [f7_O, f7_E], 'teal', 8), ('txt', 362, 254, '5√2', 'teal', 22),
             ('txt', 250, 268, 'AE = 10√2', 'red', 22)]),
    ('agf', [('tint', [f7_A, f7_G, f7_F], 'orange'), ('txt', 320, 54, '10', 'orange', 22), ('txt', 448, 125, '5', 'orange', 22),
             ('path', [f7_A, f7_F], 'orange', 7)]),
], vb='170 30 300 300', w=260, title='Four squares of side 5')
f7g39b = GEO('f7g39b', [
    ('line', f7_39base),
    ('two', [('path', [f7_A, f7_E, f7_F, f7_A], 'teal', 7), ('path', [f7_A, f7_F, f7_G, f7_A], 'orange', 5)]),
    ('af', [('seg', f7_A[0], f7_A[1], f7_F[0], f7_F[1], 'red', 6, True)]),
    ('eq', [('tick', f7_F[0], f7_F[1], f7_E[0], f7_E[1], 2, 'red'), ('tick', f7_G[0], f7_G[1], f7_F[0], f7_F[1], 2, 'red')]),
    ('left', [('txt', 300, 205, '10√2', 'teal', 22), ('txt', 320, 54, '10', 'orange', 22)]),
], vb='170 30 300 300', w=260, title='Triangles AEF and AFG')
f7p2 = I('f7p2', '$AF^2=10^2+5^2=125$, $\\ AF=5\\sqrt5$', size=30)
f7p3 = I('f7p3', '$P_{AEF}=5\\sqrt5+5+10\\sqrt2$', size=30)
f7p4 = I('f7p4', '$P_{AFG}=5\\sqrt5+5+10$', size=30)
f7p5 = I('f7p5', 'Difference $=10\\sqrt2-10$', size=30)
f7p6 = I('f7p6', '$AE-AG=10\\sqrt2-10$', size=32)
f7p7 = I('f7p7', '(1) $5\\sqrt3-5$: $\\ \\sqrt3>1$, positive', size=28)
f7p8 = I('f7p8', '(2) $10-10\\sqrt2$: $\\ \\sqrt2>1$, negative ✗', size=28)
f7p9 = I('f7p9', '(3) $5-5\\sqrt3$: $\\ $negative ✗', size=28)
f7s39 = I('f7s39', 'So far: $\\ AE=10\\sqrt2,\\ \\ AF=5\\sqrt5$', size=26)
video('solve-geo31-g039', 'solution', qid='geo31-g039', slides=[
    SM('Method 1 · Every side', 'Every side',
      L("Four congruent squares, each with a side of five centimeters, are arranged as in the accompanying figure. What is "
        "the perimeter of A E F minus the perimeter of A F G, in centimeters?", pt('stem', 'Four congruent squares', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("[short pause] We'll solve it three ways. First the full math, every side of both triangles. Then a shortcut, "
        "cancelling the sides they share. And then a quick check for when you have only a few seconds."),
      L("[short pause] The four squares are identical, so every side of every square is five. Now the length A E. It goes "
        "through two small squares, corner to corner, so it's made of two diagonals of the small squares.",
        show(f7g39['line'], 'The four squares are identical')),
      L("Look at the small square at the top left. Its diagonal cuts it into two silver triangles, forty-five, forty-five, "
        "ninety. The legs are five and five, so the diagonal is five root two. The second diagonal is five root two as "
        "well, so A E is ten root two.", show(f7g39['sq'], 'the small square at the top left'),
        show(f7g39['sq2'], 'The second diagonal')),
      L("Now A F. It's the longest side of the right triangle A G F. One leg, A G, is ten, two sides of a square. The other "
        "leg, G F, is five. By Pythagoras, A F squared is ten squared plus five squared, a hundred plus twenty-five, a "
        "hundred twenty-five. A hundred twenty-five is twenty-five times five, so A F is five root five.",
        show(f7g39['agf'], 'Now A F'), show(f7p2, 'By Pythagoras'))),
    SM('Method 1 · Every side', 'Every side',
      L("Now the perimeters. A E F has A F, five root five, plus E F, five, plus A E, ten root two. A F G has A F, five root five, "
        "plus F G, five, plus A G, ten.", show(f7s39, 'Now the perimeters'), show(f7p3, 'A E F has A F'), show(f7p4, 'A F G has A F')),
      L("Subtract. Five root five minus five root five is zero. Five minus five is zero. What's left is ten root two minus "
        "ten. Choice number four is our answer.", show(f7p5, 'What\'s left'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
    SM('Method 2 · Shared sides cancel', 'Shared sides cancel',
      L("[pause] Could we make it shorter? Yes, by cancelling sides. Look at the two triangles side by side. A F is a side "
        "of both, so it cancels in the difference. We don't need its length at all.",
        show(f7g39b['line'], 'Could we make it shorter'), show(f7g39b['two'], 'Look at the two triangles'),
        show(f7g39b['af'], 'A F is a side of both')),
      L("Next, E F and F G are both sides of a small square, five each. They're equal, so they cancel too.",
        show(f7g39b['eq'], 'E F and F G are both')),
      L("All that's left is A E, ten root two, minus A G, ten. Ten root two minus ten, choice number four, and no "
        "Pythagoras at all.", show(f7g39b['left'], 'All that\'s left'), show(f7p6, 'Ten root two minus ten'),
        mk('tick', 'choice 4', 'choice number four, and no'))),
    SM('Method 3 · A quick check', 'A quick check',
      L("[pause] One more idea. Say you reach this question at the very end of the exam, with ten or twenty seconds left. "
        "Sometimes you can rule out choices just by their sign. The answer here must be positive. A E F and A F G share A F, "
        "and E F equals F G, so the difference is A E minus A G. A E is the longest side of the big right triangle A G E, so it's "
        "longer than A G, and the difference is positive."),
      L("Root two and root three are both bigger than one, because one times one is only one. Choice number one, five root "
        "three minus five. Five root three is more than five, so this is positive. We can't rule it out.",
        show(f7p7, 'Choice number one, five root')),
      L("Choice number two, ten minus ten root two. Ten root two is more than ten, so this is negative. Out. Choice number "
        "three, five minus five root three, is negative too. Out.", show(f7p8, 'Choice number two, ten minus'),
        mk('cross', 'choice 2', 'so this is negative. Out'), show(f7p9, 'Choice number three, five minus'),
        mk('cross', 'choice 3', 'is negative too')),
      L("Two choices are left, and the sign can't separate them. But with no time left, a guess between two is much "
        "better than a guess between four. This trick does show up on the exam. [pause] Okay. I'll see you in the next "
        "question.", pt('choice 1', 'Two choices are left'))),
])

# ------------------------------------------------------------------------------------------------ geo31-g040 (Hebrew: two equilateral triangles, the bold line)
# Hebrew (geo 1665-1725): the math (every side a or b; the bold bottom is b minus a; b + b + (b − a) = the given; 3b = 4a
# and STOP: the ratio is 3:4 or 4:3, and the exam has no order distractor; "if you insist, not in the exam": divide by
# 4b), then plugging in the answers (1: a = b is impossible, a big and a small triangle; the next choice; check the bold
# line). English: three times the small perimeter, 3b = 10a, a/b = 3/10. Plugging in is explained on its own here.
# V3: every side labelled; the bold line traced in teal piece by piece; the bottom piece "b − a" with the gap a marked;
# then the typed equation lines; method 2: the sizes written for the choice being tested.
f7T, f7L2, f7R2 = (320, 69.21), (188.6, 296.8), (451.4, 296.8)
f7s1, f7s2, f7sT = (280.58, 296.8), (359.42, 296.8), (320, 228.52)
f7_40base = [('seg', f7T[0], f7T[1], f7L2[0], f7L2[1]), ('seg', f7T[0], f7T[1], f7R2[0], f7R2[1]), ('seg', f7L2[0], f7L2[1], f7R2[0], f7R2[1]),
             ('seg', f7s1[0], f7s1[1], f7sT[0], f7sT[1]), ('seg', f7s2[0], f7s2[1], f7sT[0], f7sT[1])]
f7g40 = GEO('f7g40', [
    ('line', f7_40base),
    ('sides', [('txt', 236, 178, 'b', 'ink', 26, True), ('txt', 404, 178, 'b', 'ink', 26, True), ('txt', 320, 322, 'b', 'ink', 26, True),
               ('txt', 284, 258, 'a', 'teal', 24, True), ('txt', 356, 258, 'a', 'teal', 24, True), ('txt', 320, 284, 'a', 'teal', 22, True)]),
    ('bold', [('path', [f7L2, f7T, f7R2], 'orange', 8)]),
    ('bottom', [('path', [f7L2, f7s1], 'orange', 8), ('path', [f7s2, f7R2], 'orange', 8), ('txt', 234, 322, 'b − a', 'orange', 22)]),
], vb='175 55 290 285', w=262, title='Two equilateral triangles')
f7r1 = IH('f7r1', '$b+b+(b-a)=3\\cdot3a$', size=28)
f7r2 = IH('f7r2', '$3b-a=9a$, $\\ 3b=10a$', size=28)
f7r3 = I('f7r3', '$\\to\\ 3:10$', size=28)
f7r4 = I('f7r4', '(1) $a=b$: $\\ $but $a<b$ ✗', size=30)
f7r5 = I('f7r5', '(2) $a=3,\\ b=10$: $\\ 10+10+7=27=3\\cdot9$ ✓', size=28)
video('solve-geo31-g040', 'solution', qid='geo31-g040', slides=[
    SM('Method 1 · Algebra', 'The bold line',
      L("The accompanying figure shows two equilateral triangles with side lengths a and b, where a is smaller than b. The "
        "total length of the bold segments is three times the perimeter of the smaller triangle. What is a over b?",
        pt('stem', 'The accompanying figure', 'hl', 10.0), voice='calm', pause=0.5),
      L("[short pause] We'll solve it two ways, with algebra, and then by testing the answer choices."),
      L("[short pause] Both triangles are equilateral. In the small one, all three sides are a. In the big one, all three "
        "sides are b.", show(f7g40['line'], 'Both triangles are equilateral'), show(f7g40['sides'], 'all three sides are a')),
      L("Now the bold line. It's the two slanted sides of the big triangle, b and b, and the bottom. But not the whole "
        "bottom. The small triangle's side, a, is missing from the middle. So the bold part of the bottom is b minus a.",
        show(f7g40['bold'], 'Now the bold line'), show(f7g40['bottom'], 'So the bold part')),
      L("The given says the bold line is three times the small perimeter. The small perimeter is three a, so three times "
        "it is nine a. So b plus b plus, in brackets, b minus a, equals nine a. Three b minus a equals nine a. Add a to both "
        "sides, and three b equals ten a.", show(f7r1, 'So b plus b plus'), show(f7r2, 'Three b minus a')),
      L("Many students get stuck here: how do I get to a over b? We don't really need to. Three b equals ten a means the "
        "ratio is three to ten, or ten to three. Only one choice is either of these, three tenths. So choice number two is "
        "our answer.", show(f7r3, 'means the ratio is three to ten'), mk('tick', 'choice 2', 'So choice number two is our answer')),
      L("If you really want the full step, not during the exam: divide both sides by ten b. On one side you get three "
        "tenths, and on the other side, a over b. And careful with the traps. One third comes from forgetting to take a off "
        "the bottom, and three eighths from adding it instead.", mk('cross', 'choice 3', 'One third comes from'),
        mk('cross', 'choice 4', 'and three eighths'))),
    SM('Method 2 · Testing the answers', 'Testing the answers',
      L("[pause] Now another way, testing the answers. Each choice says what a over b could be. We turn it into real sizes "
        "and check the given. If the sizes work, that's the answer, because the given fixes the ratio."),
      L("Choice number one says a over b is one, so a equals b. But the question has a big triangle and a small one, a is "
        "smaller than b. Out.", show(f7r4, 'Choice number one says'), mk('cross', 'choice 1', 'smaller than b. Out')),
      L("Choice number two, three tenths. So a is three and b is ten. The bold line is ten plus ten plus ten minus three, "
        "which is twenty-seven. The small perimeter is three times three, nine, and three times nine is twenty-seven. It "
        "works, so choice number two is our answer. [pause] Okay. I'll see you in the next question.",
        show(f7r5, 'So a is three and b is ten'), mk('tick', 'choice 2', 'It works, so choice number two'))),
])


# placement: the question figure on the left, our board in the right column (explicit y; the choices start near y 590)
for _g in (f7g37, f7g37b, f7g38, f7g38c, f7g38b, f7g39, f7g39b): _R(_g, 235)
_R(f7g40, 208)
for _it, _y in ((f7s37, 245), (f7k2, 305), (f7k3, 370), (f7k4, 435), (f7k5, 500), (f7k6, 515), (f7k7, 552),
                (f7m1, 485), (f7m2, 535), (f7m3, 430), (f7m4, 478), (f7m5, 526), (f7m6, 470),
                (f7p2, 512), (f7s39, 245), (f7p3, 305), (f7p4, 365), (f7p5, 425), (f7p6, 512), (f7p7, 260), (f7p8, 320), (f7p9, 380),
                (f7r1, 470), (f7r2, 506), (f7r4, 260), (f7r5, 320)):
    _R(_it, _y)
_R(f7r3, 506, x=1330)

# carry-over boxes on the continuation slides (V2): the next step uses these results
CARRY31 = globals().get('CARRY31', {})

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
 "geo31-g031": "ABC is an equilateral triangle. D, A and E lie on one line, E lies on BC, and F lies on the extension of BA beyond A. Based on this information and the information in the figure, which expression equals $y$?",
 "geo31-g032": "In triangle ABC in the accompanying figure, $\\angle ABC=50°$ and $\\alpha>\\beta$. Which side is necessarily the longest?",
 "geo31-g033": "ABC is an obtuse triangle, with $\\angle ACB>90°$ and $AB=10$ cm. Which of the following could be its perimeter (in cm)?",
 "geo31-g034": "Which of the following triangles is not necessarily isosceles?",
 "geo31-g035": "In the accompanying figure, triangles ABC and ACD are right triangles. The marked lengths are in cm. What is the area of quadrilateral ABCD (in cm²)?",
 "geo31-g036": "In the accompanying figure, triangles ABD and BCD are right triangles. Given: $AD=20$ cm. What is the perimeter of quadrilateral ABCD (in cm)?",
 "geo31-g037": "In triangle ABC, AE is the altitude to BC. Point D lies on AE, and DBC is an equilateral triangle.\nGiven:\n$\\begin{cases} BE=4\\text{ cm} \\\\ AD=3\\sqrt3\\text{ cm} \\end{cases}$\nWhat is the shaded area (in cm²)?",
 "geo31-g038": "Triangle ABC has area 56 cm². Point D lies on BC, and $DC=3BD$. What is the difference between the areas of ADC and ABD (in cm²)?",
 "geo31-g039": "Four congruent squares, each with side 5 cm, are arranged as in the accompanying figure. What is the perimeter of AEF minus the perimeter of AFG (in cm)?",
 "geo31-g040": "The accompanying figure shows two equilateral triangles with side lengths a and b, where $a<b$. The total length of the bold segments is three times the perimeter of the smaller triangle. What is $\\frac ab$?",
 "geo31-g014": "ABC is an equilateral triangle. Point D lies on BC.\nGiven:\n$\\begin{cases} \\angle DAC=30° \\\\ DC=7\\text{ cm} \\end{cases}$\nWhat is AB (in cm)?",
 "geo31-g015": "In triangle ABC, point D lies on AB.\nGiven:\n$\\begin{cases} AB=AC \\\\ \\angle BAC=28° \\\\ BC=CD \\end{cases}$\nWhat is $\\angle ACD$?",
 "geo31-g017": "Points A and B lie on one line, and C, D and E lie on a parallel line. Given: $DE=5CD$. What is $\\frac{\\text{area of }BDE}{\\text{area of }ACD}$?",
 "geo31-g018": "ABC is an equilateral triangle with perimeter 30 cm. Points D and E are the midpoints of AB and BC, respectively. What is the area of quadrilateral ADEC (in cm²)?",
 "geo31-g010": "In triangle ABC, the marked angle outside the triangle and the interior angle at A are vertical angles. Based on this information and the information in the figure, what is the value of $x$?",
 "geo31-g011": "In the accompanying figure, the angles at A and C are equal. What is the value of $m+\\frac{n}{2}$?",
 "geo31-g012": "In triangle ABC:\n$\\begin{cases} AC=6\\text{ cm} \\\\ BC=13\\text{ cm} \\end{cases}$\nWhich of the following could be the length of AB (in cm)?",
 "geo31-g020": "Triangle ABC is a right triangle.\nGiven:\n$\\begin{cases} \\angle ABC=90° \\\\ AB=20\\text{ cm} \\\\ BC=21\\text{ cm} \\end{cases}$\nWhat is AC (in cm)?",
 "geo31-g021": "Triangle ABC is a right triangle.\nGiven:\n$\\begin{cases} \\angle ABC=90° \\\\ AB=5\\text{ cm} \\\\ BC=7\\text{ cm} \\end{cases}$\nWhat is AC (in cm)?",
 "geo31-g022": "Triangle ABC is a right triangle.\nGiven:\n$\\begin{cases} \\angle ABC=90° \\\\ AB=7\\text{ cm} \\\\ AC=10\\text{ cm} \\end{cases}$\nWhat is BC (in cm)?",
 "geo31-g025": "The accompanying figure shows three right triangles. The marked side lengths are in cm. What is CD (in cm)?",
 "geo31-g027": "Triangle ABC is a right triangle.\nGiven:\n$\\begin{cases} \\angle ABC=90° \\\\ \\angle ACB=30° \\\\ AB=5\\text{ cm} \\end{cases}$\nWhat is the perimeter of the triangle (in cm)?",
 "geo31-g028": "Triangle ABC is a right triangle.\nGiven:\n$\\begin{cases} \\angle ABC=90° \\\\ \\angle ACB=45° \\\\ AC=18\\text{ cm} \\end{cases}$\nWhat is its perimeter (in cm)?",
 "q-r26-t31-01": "Triangle ABC is right at C, and CD is the altitude to AB.\nGiven:\n$\\begin{cases} AC=15\\text{ cm} \\\\ BC=20\\text{ cm} \\\\ AB=25\\text{ cm} \\end{cases}$\nWhat is CD (in cm)?",
 "q-r26-t31-02": "In triangle ABC:\n$\\begin{cases} AB=6\\text{ cm} \\\\ BC=8\\text{ cm} \\end{cases}$\nWhich of the following could be the area of the triangle (in cm²)?",
 "q-r26-t31-03": "In triangle ABC:\n$\\begin{cases} AB=6\\text{ cm} \\\\ BC=7\\text{ cm} \\\\ AC=10\\text{ cm} \\end{cases}$\nWhich of the following is true?"
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
MV.carry(_types.SimpleNamespace(**globals()), CARRY31)
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
