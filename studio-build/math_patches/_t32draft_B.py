"""Topic 32 (Quadrilaterals) - the scripts for the teacher's own-voice reading (2026-10-14), written from the first draft to
the Codex review standard, the clarity style, the method visuals (geometry: the angle figure built in layers, GEO below), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py / _ai_vis_t16.py / _ai_vis_t17.py / _ai_vis_t18.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The camera lesson 'geo-042' gets its own reading script here too, in parts of about 3-4 minutes (2026-10-14: she reads it
with the camera on). Every other topic-32 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t32.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t32.py ai_redo_t32() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods and EVERY method of the Hebrew solution (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-32-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t32ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-32 flow order of the scripts
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
            'style': "the teacher reads it herself (Reading Studio), topic-32 scripts (2026-10-14): math_patches/_ai_vis_t32.py is "
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


# ------------------------------------------------------------------------------------------- topic-32 geometry figures (V1)
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



CARRY32 = {}       # carry-over boxes (V2): {vid: {slide index: [tex, ...]}}, filled by the scripts


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


# =================================================================================================================
# Topic 32 fragment f2: the square, the rectangle, the parallelogram (lessons geo-043, geo-045, geo-047) and their
# sample questions (g044, g046). Hebrew: geo 1794-2050. Written 2026-10-14 to the guide (R1-R36, clarity, Codex review
# standard, V1-V3). Every figure is pinned (fig / of) so typed board lines can come between its layers.
# =================================================================================================================


def f2_poly(pts, c='ink', w=3):
    return [('seg', pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], c, w) for i in range(len(pts))]


def f2_labs(*rows):
    """rows of (x, y, text): vertex letters"""
    return [('txt', x, y, t, 'ink', 26, True) for x, y, t in rows]


def f2_pin(g):
    """pin a GEO figure: its later layers are drawn on their own base, even with other board items in between"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


def f2_grid(x0, y0, n, m, s, c='teal'):
    """an n (across) by m (down) grid of little squares of size s, top-left at (x0, y0)"""
    out = []
    for i in range(1, n): out.append(('seg', x0 + i * s, y0, x0 + i * s, y0 + m * s, c, 1.4))
    for j in range(1, m): out.append(('seg', x0, y0 + j * s, x0 + n * s, y0 + j * s, c, 1.4))
    return out


# ------------------------------------------------------------------------------------------------ geo-043 (lesson: The Square)
# Hebrew (geo 1795-1858): all sides equal, all angles 90; the diagonals are equal, bisect each other, perpendicular, and
# bisect the angles (45 each); four silver triangles (also two, and endlessly more); area = side squared ("that's why we
# call it squared"), counted on a grid; the area from the diagonal, d^2 / 2, with the why (half the diagonal, one small
# triangle, times four); "the square is YES" to every property. Kept from the English lesson: a turned square is still a
# square; scaling (x k -> area x k^2, counted on a grid). Added examples: a side of 5 and 7 -> diagonal 5 root 2, 7 root 2;
# 9 -> 81; the diagonal 12 -> 72 and 10 -> 50. Dropped: the percent example (percent is a later topic in the plan).
# V3: one generic square built part by part (ticks, right angles); a turned copy; the diagonals traced, then the halves
# ticked, the right angle, the 45s; the silver triangles tinted inside the square (one small one, then a half); the grid
# counted; the scaling as two grids side by side.
f2_SQ = [(210, 60), (210, 300), (450, 300), (450, 60)]          # A B C D, side 240
f2_O = (330, 180)
f2_sqT = f2_poly(f2_SQ) + f2_labs((190, 44, 'A'), (190, 318, 'B'), (470, 318, 'C'), (470, 44, 'D'))
f2_sq1 = f2_pin(GEO('f2sq1', [
    ('line', f2_sqT),
    ('sides', [('tick', 210, 60, 210, 300), ('tick', 210, 300, 450, 300), ('tick', 450, 300, 450, 60), ('tick', 450, 60, 210, 60)]),
    ('ang', [('right', 210, 300, 0, 90, 18), ('right', 450, 300, 90, 180, 18), ('right', 450, 60, 180, 270, 18), ('right', 210, 60, 270, 360, 18)]),
    ('turn', [('seg', 660, 60, 780, 180, 'ink', 3), ('seg', 780, 180, 660, 300, 'ink', 3), ('seg', 660, 300, 540, 180, 'ink', 3),
              ('seg', 540, 180, 660, 60, 'ink', 3), ('tick', 660, 60, 780, 180), ('tick', 780, 180, 660, 300), ('tick', 660, 300, 540, 180),
              ('tick', 540, 180, 660, 60), ('right', 660, 300, 45, 135, 16), ('txt', 660, 335, 'still a square', 'small', 24)]),
], vb='150 20 680 340', w=900, col=0, title='A square'))
f2_sq2 = f2_pin(GEO('f2sq2', [
    ('line', f2_sqT),
    ('diag', [('seg', 210, 60, 450, 300, 'small', 4), ('seg', 450, 60, 210, 300, 'small', 4)]),
    ('half', [('tick', 210, 60, 330, 180, 1, 'orange'), ('tick', 330, 180, 450, 300, 1, 'orange'), ('tick', 450, 60, 330, 180, 1, 'orange'),
              ('tick', 330, 180, 210, 300, 1, 'orange')]),
    ('perp', [('right', 330, 180, 225, 315, 18, 'orange')]),
    ('a45', [('arc', 210, 300, 40, 0, 45, 'small', '45°', 64), ('arc', 210, 300, 46, 45, 90, 'small', '45°', 70)]),
], vb='150 20 360 320', w=560, col=0, title='The diagonals of a square'))
f2_k43a = I('f2k43a', 'Equal $\\cdot$ cut each other in half $\\cdot$ perpendicular $\\cdot$ cut the angles in half', size=26, col=1)
f2_sq3 = f2_pin(GEO('f2sq3', [
    ('line', f2_sqT + [('seg', 210, 60, 450, 300, 'ink', 2), ('seg', 450, 60, 210, 300, 'ink', 2)]),
    ('small', [('tint', [(210, 300), (450, 300), f2_O], 'small'), ('right', 330, 180, 225, 315, 16, 'small'),
               ('tick', 330, 180, 210, 300, 1), ('tick', 330, 180, 450, 300, 1)]),
    ('halfsq', [('tint', [(210, 60), (210, 300), (450, 300)], 'orange'), ('right', 210, 300, 0, 90, 18, 'orange')]),
], vb='150 20 360 320', w=560, col=0, title='Silver triangles in a square'))
f2_k43b = I('f2k43b', 'Side $s$ $\\to$ diagonal $s\\sqrt2$', size=30, col=1)
f2_k43c = I('f2k43c', '$5\\to5\\sqrt2 \\qquad 7\\to7\\sqrt2$', size=30, col=1)
f2_sq4 = f2_pin(GEO('f2sq4', [
    ('line', f2_poly([(150, 40), (150, 310), (420, 310), (420, 40)])),
    ('grid', f2_grid(150, 40, 6, 6, 45)),
    ('count', [('txt', 172 + 45 * i, 336, str(i + 1), 'orange', 22) for i in range(6)]),
    ('all', [('tint', [(150, 40), (150, 310), (420, 310), (420, 40)], 'small'), ('txt', 285, 18, '36 little squares', 'small', 24)]),
], vb='110 0 360 355', w=500, col=0, title='A 6 by 6 square on a grid'))
f2_k43d = I('f2k43d', '$S=a^2$', size=34, col=1)
f2_k43e = IH('f2k43e', '$6^2=36$ cm²', size=32, col=1)
f2_k43f = IH('f2k43f', '$9^2=81$ cm²', size=32, col=1)
f2_sq5 = f2_pin(GEO('f2sq5', [
    ('line', f2_sqT + [('seg', 210, 60, 450, 300, 'ink', 2), ('seg', 450, 60, 210, 300, 'ink', 2)]),
    ('d12', [('txt', 395, 230, '12', 'small', 26)]),
    ('half', [('txt', 262, 260, '6', 'orange', 26), ('txt', 400, 255, '6', 'orange', 26), ('tick', 330, 180, 210, 300, 1, 'orange'),
              ('tick', 330, 180, 450, 300, 1, 'orange')]),
    ('tri', [('tint', [(210, 300), (450, 300), f2_O], 'small'), ('right', 330, 180, 225, 315, 16, 'small'), ('txt', 330, 268, '18', 'small', 26)]),
    ('four', [('txt', 330, 92, '18', 'small', 26), ('txt', 250, 180, '18', 'small', 26), ('txt', 410, 180, '18', 'small', 26)]),
], vb='150 20 360 320', w=560, col=0, title='The area from the diagonal'))
f2_k43g = I('f2k43g', '$S=\\frac{d\\cdot d}{2}=\\frac{d^2}{2}$', size=34, col=1)
f2_k43h = IH('f2k43h', '$4\\cdot18=72 \\qquad \\frac{12^2}{2}=\\frac{144}{2}=72$', size=30, col=1)
f2_k43i = IH('f2k43i', '$\\frac{10^2}{2}=\\frac{100}{2}=50$', size=30, col=1)
f2_sq6 = f2_pin(GEO('f2sq6', [
    ('line', f2_poly([(80, 190), (80, 310), (200, 310), (200, 190)]) + [('txt', 140, 336, '3', 'ink', 24)] + f2_grid(80, 190, 3, 3, 40)),
    ('big', f2_poly([(300, 70), (300, 310), (540, 310), (540, 70)]) + [('txt', 420, 336, '6', 'ink', 24)] + f2_grid(300, 70, 6, 6, 40)),
    ('areas', [('txt', 140, 168, '9', 'small', 30), ('txt', 420, 48, '36', 'orange', 30)]),
    ('rows', [('tint', [(300, 270), (300, 310), (540, 310), (540, 270)], 'orange'), ('txt', 600, 290, 'twice as long', 'orange', 20),
              ('tint', [(300, 70), (300, 310), (340, 310), (340, 70)], 'small'), ('txt', 320, 30, 'twice as many rows', 'small', 20)]),
], vb='40 0 620 355', w=580, col=0, title='Double the side: four times the area'))
f2_k43j = I('f2k43j', 'Every length $\\times k$ $\\ \\Rightarrow\\ $ area $\\times k^2$', size=30, col=1)
f2_k43k = I('f2k43k', 'Every length $\\times3$ $\\ \\Rightarrow\\ $ area $\\times9$', size=30, col=1)
f2_k43l = I('f2k43l', 'Square: every property $\\to$ YES', size=40, col=0)
f2_k43m = I('f2k43m', 'Sides equal? $\\cdot$ Diagonals equal? $\\cdot$ Perpendicular? $\\cdot$ Cut the angles in half?', size=32, col=0)
video('geo-043', 'lesson', slides=[
    S('The Square',
      L("The square. It's a shape almost all of us know, so let's go over its properties.")),
    S('Sides and angles',
      L("All four sides of a square are equal, and all four angles are ninety degrees.", show(f2_sq1['line'], 'All four sides'),
        show(f2_sq1['sides'], 'sides of a square are equal'), show(f2_sq1['ang'], 'all four angles')),
      L("If the square is turned on the page, it's still a square. What decides is what the question says, not how the "
        "figure is drawn.", show(f2_sq1['turn'], 'If the square is turned'))),
    S('The diagonals',
      L("Now the diagonals of the square. First, they're equal to each other.", show(f2_sq2['line'], 'Now the diagonals'),
        show(f2_sq2['diag'], "they're equal to each other")),
      L("They also cut each other in half. So all four halves are equal: this one, this one, this one and this one.",
        show(f2_sq2['half'], 'They also cut each other in half')),
      L("They're perpendicular to each other: they meet at ninety degrees.", show(f2_sq2['perp'], "They're perpendicular")),
      L("And they cut the square's angles in half. Each ninety splits into forty-five and forty-five, in every corner.",
        show(f2_sq2['a45'], "And they cut the square's angles in half"), show(f2_k43a, 'in every corner'))),
    S('Silver triangles',
      L("Look at one of the four small triangles. Its angle in the middle is ninety degrees, because the diagonals are "
        "perpendicular. And its two legs are equal, because they're halves of equal diagonals. That's a silver triangle, "
        "forty-five, forty-five, ninety. So the square is made of four silver triangles.",
        show(f2_sq3['line'], 'Look at one of the four'), show(f2_sq3['small'], 'Its angle in the middle')),
      L("It's also made of two silver triangles, depending on how we look. Take half the square, cut along one diagonal. It "
        "has a ninety-degree angle and two equal legs, the sides of the square. And if we keep drawing more crossing lines, "
        "we can cut the square into more and more silver triangles.", show(f2_sq3['halfsq'], 'Take half the square')),
      L("In a silver triangle, the hypotenuse is a leg times root two. In the half square, the hypotenuse is the diagonal, so "
        "the diagonal is the side times root two. A side of five gives a diagonal of five root two, and a side of seven "
        "gives seven root two.", show(f2_k43b, 'the diagonal is the side times'), show(f2_k43c, 'A side of five'))),
    S('Area: side squared',
      L("The area of a square is its side, squared. That's actually where the word squared comes from. If the side is a, the "
        "area is a squared.", show(f2_k43d, 'If the side is a')),
      L("Say each little square here is one square centimeter. Count the side: one, two, three, four, five, six. The side is "
        "six, so the area is six squared, thirty-six. And really, there are thirty-six little squares.",
        show(f2_sq4['line'], 'Say each little square'), show(f2_sq4['grid'], 'here is one square'),
        show(f2_sq4['count'], 'Count the side'), show(f2_sq4['all'], 'And really'), show(f2_k43e, 'the area is six squared')),
      L("Another example: a side of nine gives nine squared, which is eighty-one square centimeters.",
        show(f2_k43f, 'a side of nine'))),
    S('Area from the diagonal',
      L("There's another way to find the area of a square. It's less known and less used: with the diagonals. Multiply the "
        "diagonals and divide by two. The two diagonals are equal, so it's the diagonal squared, over two.",
        show(f2_k43g, 'Multiply the diagonals')),
      L("Why does it work? Say the diagonal is twelve. Then half the diagonal is six.", show(f2_sq5['line'], 'Why does it work'),
        show(f2_sq5['d12'], 'Say the diagonal is twelve'), show(f2_sq5['half'], 'Then half the diagonal')),
      L("Look at one small triangle. Its legs are two halves, six and six, and they're perpendicular. So its area is six "
        "times six over two, which is eighteen.", show(f2_sq5['tri'], 'Look at one small triangle')),
      L("The square is four of these triangles. Four times eighteen is seventy-two. And twelve squared over two is a "
        "hundred forty-four over two, also seventy-two.", show(f2_sq5['four'], 'The square is four'),
        show(f2_k43h, 'Four times eighteen')),
      L("One more: a diagonal of ten gives ten squared, a hundred, over two, which is fifty.", show(f2_k43i, 'a diagonal of ten'))),
    S('Scale it up',
      L("One more fact about area, and it's true for every shape. Double the side of a square, from three to six.",
        show(f2_sq6['line'], 'Double the side'), show(f2_sq6['big'], 'from three to six')),
      L("The area doesn't double. It goes from nine to thirty-six, four times as much. Count the little squares: every row is "
        "twice as long, and there are twice as many rows. Two times two is four.", show(f2_sq6['areas'], "The area doesn't double"),
        show(f2_sq6['rows'], 'Count the little squares')),
      L("So when every length is multiplied by some number k, the area is multiplied by k squared. For example, if every "
        "length is three times as long, the area is nine times as big.", show(f2_k43j, 'So when every length'),
        show(f2_k43k, 'For example')),
      L("Careful, this works only when all the lengths grow. If only one side grows, the area grows only by that side's "
        "number.", pt('f2k43j', 'Careful, this works'))),
    S('Square: all yes',
      L("That's the square, the simplest and the most perfect quadrilateral. For every property we ask about, the square's "
        "answer is yes.", show(f2_k43l, 'For every property')),
      L("Are the sides equal? Yes. Are the diagonals equal? Yes. Are they perpendicular? Yes. Do they cut the angles in half? "
        "Yes. Everything is yes. [pause] Okay. I'll see you in the next video.", show(f2_k43m, 'Are the sides equal'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g044 (Hebrew: the square's example)
# Hebrew (geo 1847-1855): "I could draw it and start Pythagoras to find the side, and then square it, but there's no
# reason": d^2 / 2 (her 10 -> 50; the course's 14 -> 98). Kept from the English script: the long way once, as a second
# method (s^2 + s^2 = 196 -> s^2 = 98, stop: s^2 IS the area), and the traps 196 and 49.
# V3: the question figure on the left; our copy on the right: the given diagonal traced with 14, the other diagonal drawn
# in (equal); method 2: triangle ABC tinted, its two legs s, the hypotenuse 14.
FIG_LEFT.update({'solve-geo32-g044', 'solve-geo32-g046'})
f2_g44T = f2_poly([(210.5, 70.5), (210.5, 289.5), (429.5, 289.5), (429.5, 70.5)]) + f2_labs((192, 54, 'A'), (192, 308, 'B'), (448, 308, 'C'), (448, 54, 'D'))
f2_g44 = f2_pin(GEO('f2g44', [
    ('line', f2_g44T + [('seg', 210.5, 70.5, 429.5, 289.5, 'ink', 3), ('txt', 345, 168, '14', 'ink', 24)]),
    ('d1', [('seg', 210.5, 70.5, 429.5, 289.5, 'small', 5)]),
    ('d2', [('seg', 429.5, 70.5, 210.5, 289.5, 'small', 4, True), ('txt', 404, 112, '14', 'small', 24)]),
    ('calc', [('txt', 320, 352, 'S = 14 · 14 / 2 = 196 / 2 = 98', 'ink', 21)]),
], vb='170 30 300 345', w=380, title='The square ABCD and its diagonals'))
f2_g44b = f2_pin(GEO('f2g44b', [
    ('line', f2_g44T + [('seg', 210.5, 70.5, 429.5, 289.5, 'ink', 3)]),
    ('tri', [('tint', [(210.5, 70.5), (210.5, 289.5), (429.5, 289.5)], 'small'), ('right', 210.5, 289.5, 0, 90, 18, 'small'),
             ('txt', 190, 180, 's', 'small', 28, True), ('txt', 320, 312, 's', 'small', 28, True), ('txt', 345, 168, '14', 'orange', 26)]),
    ('pyth', [('txt', 320, 345, 's² + s² = 14² = 196', 'ink', 22)]),
    ('half', [('txt', 320, 378, '2s² = 196,  s² = 98', 'ink', 22)]),
], vb='170 30 300 365', w=380, title='Half of the square: triangle ABC'))
_R(f2_g44, 200); _R(f2_g44b, 200)
video('solve-geo32-g044', 'solution', qid='geo32-g044', slides=[
    SM('Method 1 · The diagonals', 'The diagonals',
      L("The diagonal of a square is fourteen centimeters long. What is the area of the square, in square centimeters?",
        pt('stem', 'The diagonal of a square', 'hl', 6.0), voice='calm', pause=0.5),
      L("We know only the diagonal, and we need the area. [short pause] We'll solve it two ways, with the diagonal, and then "
        "the long way, through the side.", pt('fig: 14', 'We know only the diagonal')),
      L("[short pause] In principle, we could use Pythagoras to find the side, and then square it. But there's no need. The "
        "area of a square is the product of the diagonals, over two.", show(f2_g44['line'], 'In principle'),
        show(f2_g44['d1'], 'The area of a square')),
      L("The two diagonals of a square are equal, so both are fourteen. Fourteen times fourteen is a hundred ninety-six, and a "
        "hundred ninety-six over two is ninety-eight. Choice number two is our answer.", show(f2_g44['d2'], 'so both are fourteen'),
        show(f2_g44['calc'], 'Fourteen times fourteen'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · Through the side', 'Through the side',
      L("[pause] Now the long way, once. Call the side s. The diagonal cuts the square into two right triangles. In triangle "
        "A B C, the legs are s and s, and the hypotenuse is the diagonal, fourteen.", show(f2_g44b['line'], 'Now the long way'),
        show(f2_g44b['tri'], 'In triangle A B C')),
      L("By Pythagoras, s squared plus s squared is fourteen squared, a hundred ninety-six. So two s squared is a hundred "
        "ninety-six, and s squared is ninety-eight. But s squared is already the area of the square, so we stop here. "
        "Ninety-eight, choice number two.", show(f2_g44b['pyth'], 'By Pythagoras'), show(f2_g44b['half'], 'So two s squared'),
        mk('tick', 'choice 2', 'Ninety-eight, choice number two')),
      L("Careful with the traps. A hundred ninety-six is the diagonal squared, without dividing by two. And forty-nine is half "
        "the diagonal, squared. [pause] Okay. I'll see you in the next question.", mk('cross', 'choice 3', 'A hundred ninety-six is'),
        mk('cross', 'choice 1', 'And forty-nine'))),
])

# ------------------------------------------------------------------------------------------------ geo-045 (lesson: The Rectangle)
# Hebrew (geo 1867-1890): a square stretched sideways keeps some of its rules: opposite sides equal, all angles 90,
# opposite sides parallel; the diagonals are equal (symmetric) and bisect each other; NOT perpendicular, NOT angle
# bisectors (unlike the square); area length x width (or base x height), on a grid (her 10 x 5 = 50; the course's 8 x 3).
# Kept from the English lesson: adjacent sides not necessarily equal (if they are: a square). Added: 7 x 4 = 28.
# (Her "exaggerated drawing" tip comes right after her rectangle example: it's in g046.)
# V3: the square, then the same square stretched (the rectangle drawn over it); marks at the words; the diagonals traced,
# halves ticked; the not-90 angle and the unequal corner parts in red; the area grid counted.
f2_RC = [(110, 90), (110, 270), (530, 270), (530, 90)]          # A B C D
f2_rcT = f2_labs((92, 74, 'A'), (92, 288, 'B'), (548, 288, 'C'), (548, 74, 'D'))
f2_rc1 = f2_pin(GEO('f2rc1', [
    ('line', f2_poly([(110, 90), (110, 270), (290, 270), (290, 90)], 'ink', 3)),
    ('rect', [('dim', 60, 40, 520, 280)] + f2_poly(f2_RC, 'ink', 4) + f2_rcT
             + [('seg', 300, 180, 500, 180, 'small', 3, True), ('par', 300, 180, 500, 180, 1, 'small'), ('txt', 400, 160, 'stretched', 'small', 24)]),
    ('opp', [('tick', 110, 90, 530, 90, 1), ('tick', 110, 270, 530, 270, 1), ('tick', 110, 90, 110, 270, 2), ('tick', 530, 90, 530, 270, 2)]),
    ('ang', [('right', 110, 270, 0, 90, 18), ('right', 530, 270, 90, 180, 18), ('right', 530, 90, 180, 270, 18), ('right', 110, 90, 270, 360, 18),
             ('par', 230, 90, 410, 90), ('par', 230, 270, 410, 270), ('par', 110, 240, 110, 120, 2), ('par', 530, 240, 530, 120, 2)]),
], vb='60 40 520 280', w=580, col=0, title='A square stretched into a rectangle'))
f2_k45a = I('f2k45a', 'Sides next to each other: not necessarily equal', size=28, col=1)
f2_rc2 = f2_pin(GEO('f2rc2', [
    ('line', f2_poly(f2_RC) + f2_rcT),
    ('diag', [('seg', 110, 90, 530, 270, 'small', 4), ('seg', 530, 90, 110, 270, 'small', 4)]),
    ('half', [('tick', 110, 90, 320, 180, 1, 'orange'), ('tick', 320, 180, 530, 270, 1, 'orange'), ('tick', 530, 90, 320, 180, 1, 'orange'),
              ('tick', 320, 180, 110, 270, 1, 'orange')]),
    ('notp', [('arc', 320, 180, 34, gdir(320, 180, 530, 90), gdir(320, 180, 110, 90), 'red', 'not 90°', 60)]),
    ('notb', [('arc', 110, 90, 40, 270, gdir(110, 90, 530, 270), 'red'), ('arc', 110, 90, 52, gdir(110, 90, 530, 270), 360, 'red'),
              ('txt', 70, 130, '≠', 'red', 26)]),
], vb='60 30 520 280', w=580, col=0, title='The diagonals of a rectangle'))
f2_k45b = I('f2k45b', 'Equal $\\cdot$ cut each other in half', size=28, col=1)
f2_k45c = I('f2k45c', 'Not necessarily $\\perp$ $\\cdot$ not necessarily cut the angles in half', size=26, col=1)
f2_rc3 = f2_pin(GEO('f2rc3', [
    ('line', f2_poly([(80, 120), (80, 270), (480, 270), (480, 120)])),
    ('grid', f2_grid(80, 120, 8, 3, 50)),
    ('count', [('txt', 105 + 50 * i, 296, str(i + 1), 'orange', 22) for i in range(8)] + [('txt', 56, 145 + 50 * j, str(j + 1), 'small', 22) for j in range(3)]),
    ('all', [('tint', [(80, 120), (80, 270), (480, 270), (480, 120)], 'small'), ('txt', 280, 96, '24 little squares', 'small', 24)]),
], vb='30 70 480 250', w=580, col=0, title='An 8 by 3 rectangle on a grid'))
f2_k45d = I('f2k45d', '$S=a\\cdot b$', size=34, col=1)
f2_k45e = IH('f2k45e', '$8\\cdot3=24$ cm²', size=32, col=1)
f2_k45f = IH('f2k45f', '$7\\cdot4=28$ cm²', size=32, col=1)
video('geo-045', 'lesson', slides=[
    S('The Rectangle',
      L("The rectangle. A rectangle is really a square that someone stretched a little sideways.")),
    S('Stretch a square',
      L("Take a square and stretch it sideways. We get a rectangle, so it keeps some of the square's rules.",
        show(f2_rc1['line'], 'Take a square'), show(f2_rc1['rect'], 'We get a rectangle')),
      L("Opposite sides are equal: the top equals the bottom, and the left side equals the right side.",
        show(f2_rc1['opp'], 'Opposite sides are equal')),
      L("All the angles are still ninety degrees, because we didn't touch the angles. And opposite sides are parallel.",
        show(f2_rc1['ang'], 'All the angles are still')),
      L("But two sides next to each other don't have to be equal. If they are equal, it's a square.",
        show(f2_k45a, "two sides next to each other"))),
    S('The diagonals',
      L("Now the diagonals. First, they're equal to each other, because the rectangle is symmetric.",
        show(f2_rc2['line'], 'Now the diagonals'), show(f2_rc2['diag'], "they're equal to each other")),
      L("They also cut each other in half, so all four halves are equal.", show(f2_rc2['half'], 'They also cut each other'),
        show(f2_k45b, 'so all four halves')),
      L("Now pay attention. Are they perpendicular? Not necessarily. Here you can see that they don't meet at ninety degrees.",
        show(f2_rc2['notp'], 'Are they perpendicular')),
      L("Do they cut the rectangle's angles in half? Not necessarily either. At corner A, the two parts are not equal.",
        show(f2_rc2['notb'], 'At corner A')),
      L("In a square, the diagonals always do both, and a square is a special rectangle. But in a general rectangle, don't "
        "assume it.", show(f2_k45c, 'But in a general rectangle'))),
    S('Area: length times width',
      L("The area of a rectangle works like the square's. In the square we squared the side. Here the length and the width "
        "aren't equal, so we multiply them: length times width, or base times height.", show(f2_k45d, 'so we multiply them')),
      L("For example, a length of eight and a width of three. Eight times three is twenty-four. And really, there are three "
        "rows of eight little squares. We don't divide by two here, because it's the whole rectangle.",
        show(f2_rc3['line'], 'For example'), show(f2_rc3['grid'], 'a length of eight'), show(f2_rc3['count'], 'Eight times three'),
        show(f2_k45e, 'is twenty-four'), show(f2_rc3['all'], 'And really')),
      L("Another example: a length of seven and a width of four give seven times four, which is twenty-eight square "
        "centimeters. [pause] Okay. I'll see you in the next video.", show(f2_k45f, 'Another example'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g046 (Hebrew: the rectangle's example)
# Hebrew (geo 1891-1918): the diagonals bisect each other and are equal -> an isosceles triangle with 120 -> 30 and 30;
# the rectangle's angles are right -> triangle DBC is 30-60-90, the golden triangle; a = the short leg (her 2, the
# course's 5), the long leg a root 3; the area. Then her rectangle wrap-up: not sure about a diagonal rule? draw an
# exaggerated rectangle, very low and wide; triangles live inside quadrilateral questions.
# V3: the question figure on the left; the copy on the right: the two equal halves EB, EC ticked, the 120 at E, then the
# two 30s; slide 2: triangle DBC tinted (focus, the rest dimmed), 90 at C, the same 30 at B, 60 at D; CD = 5 written
# (the short leg, across from the 30), then BC = 5 root 3; the area; an exaggerated rectangle drawn for her tip.
f2_A, f2_B, f2_C, f2_D, f2_E = (168.272, 92.4), (168.272, 267.6), (471.728, 267.6), (471.728, 92.4), (320.0, 180.0)
f2_g46T = f2_poly([f2_A, f2_B, f2_C, f2_D]) + f2_labs((150, 76, 'A'), (150, 286, 'B'), (490, 286, 'C'), (490, 76, 'D'), (320, 156, 'E'))
f2_g46 = f2_pin(GEO('f2g46', [
    ('line', f2_g46T + [('seg', *f2_A, *f2_C, 'ink', 2.5), ('seg', *f2_B, *f2_D, 'ink', 2.5), ('txt', 492, 180, '5', 'ink', 24)]),
    ('iso', [('seg', *f2_E, *f2_B, 'small', 5), ('seg', *f2_E, *f2_C, 'small', 5), ('tick', *f2_E, *f2_B, 1, 'small'), ('tick', *f2_E, *f2_C, 1, 'small'),
             ('arc', *f2_E, 30, 210, 330, 'orange', '120°', 52)]),
    ('calc', [('txt', 320, 322, '(180° − 120°) ÷ 2 = 30°', 'ink', 22)]),
    ('b30', [('arc', *f2_B, 52, 0, 30, 'small', '30°', 80), ('arc', *f2_C, 52, 150, 180, 'small', '30°', 80)]),
], vb='120 50 400 290', w=460, title='Rectangle ABCD and its diagonals'))
f2_g46b = f2_pin(GEO('f2g46b', [
    ('line', f2_g46T + [('seg', *f2_B, *f2_D, 'ink', 2.5)]),
    ('tri', [('dim', 120, 50, 400, 270), ('tint', [f2_B, f2_C, f2_D], 'orange')] + f2_poly([f2_B, f2_C, f2_D], 'ink', 3.5)
            + f2_labs((150, 286, 'B'), (490, 286, 'C'), (490, 76, 'D'))
            + [('right', *f2_C, 90, 180, 18, 'ink'), ('arc', *f2_B, 52, 0, 30, 'small', '30°', 80), ('arc', *f2_D, 40, 210, 270, 'orange', '60°', 62)]),
    ('short', [('seg', *f2_C, *f2_D, 'small', 6), ('txt', 514, 180, '5', 'small', 30)]),
    ('ratio', [('txt', 330, 30, 'a  :  a√3  :  2a', 'ink', 22)]),
    ('long', [('seg', *f2_B, *f2_C, 'orange', 6), ('txt', 320, 300, '5√3', 'orange', 28)]),
    ('area', [('txt', 320, 338, 'S = 5 · 5√3 = 25√3', 'ink', 27)]),
], vb='120 5 430 350', w=460, title='Triangle DBC: a gold triangle'))
f2_g46c = f2_pin(GEO('f2g46c', [
    ('line', f2_poly([(60, 60), (60, 120), (580, 120), (580, 60)]) + [('seg', 60, 60, 580, 120, 'small', 3), ('seg', 580, 60, 60, 120, 'small', 3),
              ('txt', 320, 30, 'very low, very wide', 'small', 22)]),
], vb='30 10 580 130', w=500, title='An exaggerated rectangle'))
_R(f2_g46, 200); _R(f2_g46b, 200); _R(f2_g46c, 200)
video('solve-geo32-g046', 'solution', qid='geo32-g046', slides=[
    S('The isosceles triangle',
      L("The diagonals of rectangle A B C D intersect at E. Given: C D is five centimeters, and angle B E C is a hundred "
        "twenty degrees. What is the area of the rectangle, in square centimeters?", pt('stem', 'The diagonals of rectangle', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("For the area we need the length and the width. C D is five, so we still need B C. [short pause] The angle at E will "
        "lead us there.", pt('fig: 5', 'C D is five'), pt('fig: 120°', 'The angle at E')),
      L("[short pause] In a rectangle, the diagonals are equal, and they cut each other in half. So E B and E C are halves of "
        "equal diagonals, and they're equal. Triangle B E C is isosceles.", show(f2_g46['line'], 'In a rectangle'),
        show(f2_g46['iso'], 'So E B and E C')),
      L("Its top angle is a hundred twenty, so the two base angles share the rest. A hundred eighty minus a hundred twenty is "
        "sixty, and half of that is thirty. So angle E B C is thirty, and angle E C B is thirty.",
        show(f2_g46['calc'], 'A hundred eighty minus'), show(f2_g46['b30'], 'So angle E B C is thirty'))),
    S('The gold triangle',
      L("Now look at triangle D B C. Its angle at C is ninety, because it's a corner of the rectangle. Its angle at B is the "
        "same thirty we just found. So the last angle, at D, is sixty.", show(f2_g46b['line'], 'Now look at triangle'),
        show(f2_g46b['tri'], 'Its angle at C')),
      L("Thirty, sixty, ninety: that's the gold triangle. Its sides are in the ratio a, a root three, two a. The short leg, a, "
        "is across from the thirty. Across from the thirty at B is C D, so a is five.", show(f2_g46b['ratio'], "that's the gold triangle"),
        show(f2_g46b['short'], 'Across from the thirty at B')),
      L("The long leg is the short leg times root three. So B C is five root three.", show(f2_g46b['long'], 'So B C is')),
      L("Now the area of the rectangle, length times width: five root three times five, which is twenty-five root three. "
        "Choice number three is our answer.", show(f2_g46b['area'], 'Now the area'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('A tip for the diagonals',
      L("If you're not sure about a rule of the diagonals in the exam, draw an exaggerated rectangle, very low and very wide, "
        "and look at it. You'll see right away that the diagonals aren't perpendicular and don't cut the angles in half.",
        show(f2_g46c['line'], 'draw an exaggerated rectangle')),
      L("And notice how a gold triangle was hiding inside the rectangle. Triangles live inside quadrilateral questions, and "
        "later in circles too. [pause] Okay. I'll see you in the next question.", pt('fig: 120°', 'a gold triangle was hiding'))),
])

# ------------------------------------------------------------------------------------------------ geo-047 (lesson: The Parallelogram)
# Hebrew (geo 1942-2009): a rectangle squashed sideways; opposite sides equal and parallel (AD = BC, AB = DC); opposite
# angles equal (A = C, B = D); adjacent angles add up to 180 (all four pairs); WHY: extend the sides into parallel lines
# - the same crossing at every corner - small angles (green) alpha, large (orange) beta, alpha + beta = 180; diagonals: NOT
# equal (a long one and a short one), they DO bisect each other, NOT angle bisectors "though sometimes it looks like it"
# (exaggerate: very wide, very low), NOT perpendicular; area = base x height (a x h); WHY: a rectangle on the same base,
# cut the triangle out and move it in - the same area. Kept from the English lesson: equal diagonals -> rectangle,
# perpendicular -> rhombus; where the height lands (extend BC from D); special angles (30 / 45 / 60 / 150) with the
# 8, 6, 30 -> h = 3, area 24 example and the 8 x 6 trap. Added: two angle examples (70 / 110, 125 / 55).
# V3: the rectangle (dashed) squashed into the parallelogram; marks at the words; the sides extended into long parallel
# lines with small teal / large orange angles at every corner; the long (orange) and short (teal) diagonals, halves
# ticked, red "not" marks, an exaggerated copy; the height dashed with its square; the cut-and-move: the same teal triangle
# on the left (cut) and on the right (moved in); the special-angle example with the gold triangle tinted.
f2_PA, f2_PB, f2_PC, f2_PD = (230, 110), (140, 300), (460, 300), (550, 110)
f2_pT = f2_labs((222, 88, 'A'), (120, 318, 'B'), (468, 322, 'C'), (570, 98, 'D'))
f2_aB = gdir(*f2_PB, *f2_PA)                                   # the acute angle at B (64.6 degrees as drawn)
f2_pg1 = f2_pin(GEO('f2pg1', [
    ('line', f2_poly([(140, 110), (140, 300), (460, 300), (460, 110)], 'small', 3) + [('txt', 300, 205, 'rectangle', 'small', 22)]),
    ('para', f2_poly([f2_PA, f2_PB, f2_PC, f2_PD], 'ink', 4) + f2_pT),
    ('ad', [('tick', *f2_PA, *f2_PD, 1, 'orange'), ('tick', *f2_PB, *f2_PC, 1, 'orange'), ('par', *f2_PA, *f2_PD, 1, 'orange'), ('par', *f2_PB, *f2_PC, 1, 'orange')]),
    ('ab', [('tick', *f2_PB, *f2_PA, 2, 'small'), ('tick', *f2_PC, *f2_PD, 2, 'small'), ('par', *f2_PB, *f2_PA, 2, 'small'), ('par', *f2_PC, *f2_PD, 2, 'small')]),
], vb='90 60 510 280', w=580, col=0, title='A rectangle squashed into a parallelogram'))
f2_k47a = I('f2k47a', '$AD\\parallel BC,\\ AD=BC \\qquad AB\\parallel DC,\\ AB=DC$', size=28, col=1)
f2_pgT = f2_poly([f2_PA, f2_PB, f2_PC, f2_PD]) + f2_pT
f2_pg2 = f2_pin(GEO('f2pg2', [
    ('line', f2_pgT),
    ('opp', [('arc', *f2_PB, 36, 0, f2_aB, 'small'), ('arc', *f2_PD, 36, 180, 180 + f2_aB, 'small'),
             ('arc', *f2_PA, 32, 180 + f2_aB, 360, 'orange'), ('arc', *f2_PC, 32, f2_aB, 180, 'orange')]),
    ('ex1', [('txt', 196, 284, '70°', 'small', 22), ('txt', 506, 128, '70°', 'small', 22), ('txt', 262, 136, '110°', 'orange', 22),
             ('txt', 428, 276, '110°', 'orange', 22)]),
], vb='90 60 510 280', w=580, col=0, title='The angles of a parallelogram'))
f2_k47b = I('f2k47b', 'Opposite angles are equal', size=30, col=1)
f2_k47c = I('f2k47c', 'Next to each other: sum $180°$', size=30, col=1)
f2_k47d = IH('f2k47d', '$125°\\ \\to\\ 180°-125°=55°$', size=30, col=1)
f2_ext = lambda P, Q, k=0.8: (P[0] - (Q[0] - P[0]) * k, P[1] - (Q[1] - P[1]) * k, Q[0] + (Q[0] - P[0]) * k, Q[1] + (Q[1] - P[1]) * k)
f2_pg3 = f2_pin(GEO('f2pg3', [
    ('line', f2_pgT),
    ('l1', [('seg', 20, 110, 640, 110, 'ink', 2, True), ('seg', 20, 300, 640, 300, 'ink', 2, True)]),
    ('l2', [('seg', *f2_ext(f2_PB, f2_PA, 0.35), 'ink', 2, True), ('seg', *f2_ext(f2_PC, f2_PD, 0.35), 'ink', 2, True)]),
    ('ab', [('arc', *f2_PB, 34, 0, f2_aB, 'small', 'α', 56), ('arc', *f2_PD, 34, 180, 180 + f2_aB, 'small', 'α', 56),
            ('arc', *f2_PA, 30, 180 + f2_aB, 360, 'orange', 'β', 52), ('arc', *f2_PC, 30, f2_aB, 180, 'orange', 'β', 52)]),
    ('sum', [('txt', 330, 345, 'α + β = 180°', 'ink', 28)]),
], vb='0 40 660 330', w=860, col=0, title='Why: the sides are parallel lines'))
f2_pg4 = f2_pin(GEO('f2pg4', [
    ('line', f2_pgT),
    ('diag', [('seg', *f2_PB, *f2_PD, 'orange', 4), ('seg', *f2_PA, *f2_PC, 'small', 4), ('txt', 470, 170, 'long', 'orange', 22),
              ('txt', 300, 175, 'short', 'small', 22)]),
    ('half', [('tick', *f2_PB, 345, 205, 1, 'orange'), ('tick', 345, 205, *f2_PD, 1, 'orange'), ('tick', *f2_PA, 345, 205, 2, 'small'),
              ('tick', 345, 205, *f2_PC, 2, 'small')]),
    ('not', [('arc', *f2_PB, 46, 0, gdir(*f2_PB, *f2_PD), 'red'), ('arc', *f2_PB, 58, gdir(*f2_PB, *f2_PD), f2_aB, 'red'),
             ('txt', 140, 245, '≠', 'red', 26), ('txt', 345, 240, 'not 90°', 'red', 22)]),
    ('exag', f2_poly([(620, 300), (660, 260), (1060, 260), (1020, 300)], 'ink', 3) + [('seg', 620, 300, 1060, 260, 'orange', 3),
              ('arc', 620, 300, 46, 0, gdir(620, 300, 1060, 260), 'red'), ('arc', 620, 300, 58, gdir(620, 300, 1060, 260), 45, 'red'),
              ('txt', 840, 330, 'very wide, very low', 'small', 22)]),
], vb='90 60 1000 290', w=1060, col=0, title='The diagonals of a parallelogram'))
f2_k47e = I('f2k47e', 'Equal diagonals $\\to$ rectangle $\\qquad$ perpendicular $\\to$ rhombus', size=26, col=1)
f2_k47f = I('f2k47f', 'A parallelogram: the diagonals cut each other in half, that is all', size=26, col=1)
f2_H = (f2_PA[0], 300)
f2_pg5 = f2_pin(GEO('f2pg5', [
    ('line', f2_pgT + [('txt', 300, 326, 'a', 'ink', 26, True)]),
    ('h', [('seg', *f2_PA, *f2_H, 'small', 3.5, True), ('right', *f2_H, 0, 90, 16, 'small'), ('txt', 244, 210, 'h', 'small', 28, True)]),
    ('side', [('seg', *f2_PB, *f2_PA, 'red', 4), ('txt', 160, 190, 'not h', 'red', 22)]),
    ('ext', [('seg', 460, 300, 600, 300, 'ink', 2, True), ('seg', 550, 110, 550, 300, 'small', 3, True), ('right', 550, 300, 90, 180, 16, 'small'),
             ('dot', 550, 300)]),
], vb='90 60 540 290', w=580, col=0, title='The height of a parallelogram'))
f2_k47g = I('f2k47g', '$S=a\\cdot h$', size=34, col=1)
f2_pg6 = f2_pin(GEO('f2pg6', [
    ('line', f2_pgT + [('txt', 300, 326, 'a', 'ink', 26, True)]),
    ('rect', f2_poly([(140, 110), (140, 300), (460, 300), (460, 110)], 'small', 3) + [('txt', 300, 205, 'a × h', 'small', 26)]),
    ('left', [('tint', [(140, 110), f2_PB, f2_PA], 'small'), ('txt', 120, 160, 'cut', 'small', 22)]),
    ('right', [('tint', [(460, 110), f2_PC, f2_PD], 'small'), ('seg', 170, 92, 470, 92, 'small', 2, True), ('txt', 330, 74, 'move it', 'small', 22)]),
], vb='90 50 510 300', w=580, col=0, title='Cut and move: a rectangle with the same base and height'))
f2_k47h = I('f2k47h', 'Same base, same height $\\to$ same area', size=30, col=1)
f2_sB, f2_sC = (100, 300), (420, 300)
f2_sA = (100 + 240 * 0.8660254, 300 - 120)
f2_sD = (f2_sA[0] + 320, f2_sA[1])
f2_pg7 = f2_pin(GEO('f2pg7', [
    ('line', f2_poly([f2_sA, f2_sB, f2_sC, f2_sD]) + f2_labs((300, 160, 'A'), (84, 316, 'B'), (436, 316, 'C'), (650, 160, 'D'))
             + [('txt', 260, 326, '8', 'ink', 26), ('txt', 186, 222, '6', 'ink', 26), ('arc', *f2_sB, 52, 0, 30, 'small', '30°', 80)]),
    ('h', [('seg', *f2_sA, f2_sA[0], 300, 'small', 3.5, True), ('right', f2_sA[0], 300, 90, 180, 16, 'small')]),
    ('gold', [('tint', [f2_sB, f2_sA, (f2_sA[0], 300)], 'orange'), ('txt', 330, 245, 'h = 3', 'small', 26)]),
    ('wrong', [('txt', 520, 250, '8 × 6 ✗', 'red', 26)]),
], vb='60 140 620 210', w=580, col=0, title='A parallelogram with a 30 degree angle'))
f2_k47i = IH('f2k47i', '$S=8\\cdot3=24$', size=32, col=1)
f2_k47j = I('f2k47j', '$45°$: $\\ h=\\frac{\\text{side}}{\\sqrt2} \\qquad 60°$: $\\ h=\\frac{\\text{side}}{2}\\cdot\\sqrt3$', size=28, col=1)
video('geo-047', 'lesson', slides=[
    S('The Parallelogram',
      L("The parallelogram. It's like a rectangle that someone squashed a little sideways.")),
    S('Sides',
      L("Take a rectangle and squash it a little sideways. That's a parallelogram.", show(f2_pg1['line'], 'Take a rectangle'),
        show(f2_pg1['para'], "That's a parallelogram")),
      L("Its opposite sides are equal and parallel. A D is equal and parallel to B C, and A B is equal and parallel to D C.",
        show(f2_pg1['ad'], 'A D is equal'), show(f2_pg1['ab'], 'and A B is equal'), show(f2_k47a, 'and parallel to D C'))),
    S('Angles',
      L("What do we know about the angles? Opposite angles are equal. Angle A equals angle C, and angle B equals angle D.",
        show(f2_pg2['line'], 'What do we know'), show(f2_pg2['opp'], 'Angle A equals'), show(f2_k47b, 'Opposite angles are equal')),
      L("And any two angles next to each other add up to a hundred eighty. D and C, a hundred eighty. A and D, a hundred "
        "eighty. B and C, and A and B, also a hundred eighty.", show(f2_k47c, 'And any two angles')),
      L("For example, if angle B is seventy, then angle D is seventy too, and angles A and C are each a hundred ten. And if "
        "an angle is a hundred twenty-five, the angle next to it is fifty-five.", show(f2_pg2['ex1'], 'For example'),
        show(f2_k47d, 'And if an angle'))),
    S('Why: parallel lines',
      L("Let's see why. The opposite sides are parallel, so let's extend them into long parallel lines. These two sides are "
        "parallel too, so we extend them as well.", show(f2_pg3['line'], "Let's see why"), show(f2_pg3['l1'], 'so let\'s extend them'),
        show(f2_pg3['l2'], 'These two sides')),
      L("Remember, two parallel lines and a line that cuts them make small angles and large angles. And it's the same "
        "crossing at every corner of the parallelogram.", pt('f2pg3_line', 'it\'s the same crossing')),
      L("So all the large angles are equal, we'll call them beta, and all the small ones are equal, we'll call them alpha. "
        "That's the first rule: opposite angles are equal.", show(f2_pg3['ab'], 'So all the large angles')),
      L("And a small angle plus a large angle is a hundred eighty. So two angles next to each other add up to a hundred "
        "eighty: alpha plus beta is a hundred eighty.", show(f2_pg3['sum'], 'alpha plus beta'))),
    S('The diagonals',
      L("Now the diagonals. Are they equal? Not necessarily. Here there's a longer diagonal and a shorter one.",
        show(f2_pg4['line'], 'Now the diagonals'), show(f2_pg4['diag'], 'Here there\'s a longer')),
      L("What we do know is that they cut each other in half. This part equals this part, and this part equals this one.",
        show(f2_pg4['half'], 'they cut each other in half')),
      L("Do they cut the parallelogram's angles in half? Not necessarily, even though sometimes it looks like it. And they're "
        "not necessarily perpendicular either.", show(f2_pg4['not'], 'Do they cut')),
      L("If you're not sure, exaggerate. Draw a very wide, very low parallelogram, and draw a diagonal. You'll see right away "
        "that it doesn't cut the angle in half.", show(f2_pg4['exag'], 'Draw a very wide')),
      L("Two more facts: if the diagonals are equal, it's a rectangle, and if they're perpendicular, it's a rhombus. A general "
        "parallelogram promises only one thing about its diagonals: they cut each other in half.",
        show(f2_k47e, 'Two more facts'), show(f2_k47f, 'A general parallelogram'))),
    S('Area: base times height',
      L("The area of a parallelogram is simply base times height, a times h. The height is perpendicular to the base.",
        show(f2_pg5['line'], 'The area of a parallelogram'), show(f2_pg5['h'], 'The height is perpendicular'),
        show(f2_k47g, 'a times h')),
      L("It's not the sloping side. The sloping side is longer than the height.", show(f2_pg5['side'], "It's not the sloping side")),
      L("Be careful where you drop it. From A, the foot of the height lands on B C. From D, it would land outside B C, so "
        "first we extend B C.", show(f2_pg5['ext'], 'From D'))),
    S('Why: cut and move',
      L("Why base times height? Say we don't know the area of a parallelogram, but we do know the area of a rectangle. Let's "
        "draw a rectangle on the same base, with the same height.", show(f2_pg6['line'], 'Why base times height'),
        show(f2_pg6['rect'], "Let's draw a rectangle")),
      L("The difference between them is a triangle. This triangle on the left is in the rectangle, but not in the "
        "parallelogram.", show(f2_pg6['left'], 'This triangle on the left')),
      L("If we cut it out of the rectangle and move it to the right side, it fills exactly the part of the parallelogram "
        "that was missing. So the parallelogram has the same area as the rectangle.", show(f2_pg6['right'], 'If we cut it out')),
      L("The rectangle's area is base times height, so the parallelogram's area is a times h too.", show(f2_k47h, "The rectangle's area"))),
    S('Special angles',
      L("Exam questions love a parallelogram with a special angle: thirty, forty-five or sixty degrees. For example, sides of "
        "eight and six, with an angle of thirty degrees at B. What is the area?", show(f2_pg7['line'], 'For example')),
      L("Drop the height from A. A right triangle forms, with a thirty-degree angle: a gold triangle.",
        show(f2_pg7['h'], 'Drop the height'), show(f2_pg7['gold'], 'A right triangle forms')),
      L("The height is across from the thirty, so it's the short leg, half of the hypotenuse. The hypotenuse is the side of "
        "six, so the height is three. And the area is eight times three, which is twenty-four.",
        pt('f2pg7_line', 'The height is across'), show(f2_k47i, 'And the area')),
      L("A lot of students multiply eight times six, but the sloping side is not the height.", show(f2_pg7['wrong'], 'A lot of students')),
      L("With forty-five degrees, it's a silver triangle, and the height is the side over root two. With sixty, it's again a "
        "gold triangle, and the height is half the side times root three. And with an obtuse angle, like a hundred fifty, "
        "look at the angle next to it, which is thirty. [pause] Okay. I'll see you in the next video.",
        show(f2_k47j, 'With forty-five degrees'))),
])

# carry-over boxes on the continuation slides (V2): the next step uses these results
CARRY32 = globals().get('CARRY32', {})

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
 "geo32-g066": "Which of the following statements is not necessarily true?",
 "geo32-g067": "ABCD is a rectangle, and E lies on AD. The areas of triangles ABE and ECD are 6 cm² and 15 cm², respectively. What is the area of the shaded triangle EBC (in cm²)?",
 "geo32-g068": "ABCD is a rectangle. E lies on AD, G lies on BC, and F lies on AB. Given:\n$\\begin{cases} AE=3ED \\\\ BG=3GC \\end{cases}$\nTriangles FEG and EGC are shaded. Which of the following additional data is sufficient to determine the total shaded area?",
 "geo32-g069": "ABCD is an isosceles trapezoid. Given:\n$\\begin{cases} AD\\parallel BC \\\\ AD=5\\text{ cm} \\\\ BC=20\\text{ cm} \\end{cases}$\nThe shaded triangle ABD has area 15 cm². What is the area of the trapezoid (in cm²)?",
 "geo32-g070": "The rectangle in the accompanying figure consists of 40 congruent squares, each with side length 1 cm. What is the shaded area (in cm²)?",
 "geo32-g071": "In quadrilateral ABCD, angle A is α, angle B is 130° and angle C is β. E lies on AB, and DE bisects angle ADC. Which expression equals angle AED?",
 "geo32-g072": "Rectangle ABCD consists of six congruent rectangles, arranged as in the accompanying figure. The perimeter of ABCD is 40 cm. What is its area (in cm²)?",
 "geo32-g057": "The accompanying figure shows quadrilateral ABCD. Given: angle A is 118° and angle B is 96°. Which of the following cannot be the value of α?",
 "geo32-g058": "ABCD is a parallelogram, and E lies on AD. Given:\n$\\begin{cases} AB=9\\text{ cm} \\\\ AE=4\\text{ cm} \\\\ \\angle ABC=72° \\\\ \\angle BCE=54° \\end{cases}$\nWhat is the perimeter of the parallelogram (in cm)?",
 "geo32-g059": "The diagonals of rectangle ABCD intersect at E. Given: $BC=24$ cm, and the perimeter of triangle EBC is 50 cm. What is the area of triangle ABE (in cm²)?",
 "geo32-g060": "ABCD is a rhombus. Given:\n$\\begin{cases} BD=10\\text{ cm} \\\\ \\angle ABD=60° \\end{cases}$\nWhat is the area of the rhombus (in cm²)?",
 "geo32-g061": "ABCD is a square, and P is a point inside it such that triangle BPC is equilateral. What is angle PAD?",
 "geo32-g062": "ABCD is a deltoid, and its diagonals meet at O. Given:\n$\\begin{cases} AB=AD=17\\text{ cm} \\\\ CB=CD \\\\ BO=15\\text{ cm} \\\\ OC=12\\text{ cm} \\end{cases}$\nWhat is the area of the deltoid (in cm²)?",
 "geo32-g063": "ABCD is an isosceles trapezoid with $AD\\parallel BC$. Given:\n$\\begin{cases} AB=AD=7\\text{ cm} \\\\ \\angle ABD=30° \\end{cases}$\nWhat is its perimeter (in cm)?",
 "geo32-g044": "The diagonal of a square is 14 cm long. What is the area of the square (in cm²)?",
 "geo32-g046": "The diagonals of rectangle ABCD intersect at E. Given:\n$\\begin{cases} CD=5\\text{ cm} \\\\ \\angle BEC=120° \\end{cases}$\nWhat is the area of the rectangle (in cm²)?",
 "geo32-g048": "In parallelogram ABCD, the marked parts of angle B are $3\\alpha$ and $2\\alpha$, and the marked parts of angle C are $3\\beta$ and $2\\beta$. The segments BE and CE meet as in the accompanying figure. What is x?",
 "geo32-g049": "ABCD is a parallelogram, and $AE\\perp BC$. Given:\n$\\begin{cases} AD=24\\text{ cm} \\\\ CD=17\\text{ cm} \\\\ EC=16\\text{ cm} \\end{cases}$\nWhat is the area of the parallelogram (in cm²)?",
 "geo32-g051": "The sum of the lengths of the diagonals of a rhombus is 46 cm. The absolute difference between their lengths is 14 cm. What is its perimeter (in cm)?",
 "geo32-g053": "ABCD is a deltoid. Given:\n$\\begin{cases} AB=AD \\\\ CB=CD=10\\text{ cm} \\\\ \\angle ABD=45° \\\\ \\angle DBC=60° \\end{cases}$\nWhat is the perimeter of the deltoid (in cm)?",
 "geo32-g055": "The area of isosceles trapezoid ABCD is 65 cm². DE is an altitude, $DE=5$ cm, and the area of triangle DEC is 10 cm². What is AD (in cm)?",
 "q-r26-t32-01": "ABCD is a parallelogram. Given:\n$\\begin{cases} AB=10\\text{ cm} \\\\ BC=14\\text{ cm} \\\\ \\angle ABC=150° \\end{cases}$\nWhat is the area of the parallelogram (in cm²)?",
 "q-r26-t32-02": "ABCD is a right trapezoid with $AD\\parallel BC$ and $\\angle ABC=90°$. Given:\n$\\begin{cases} AD=9\\text{ cm} \\\\ BC=15\\text{ cm} \\\\ CD=10\\text{ cm} \\end{cases}$\nWhat is the area of the trapezoid (in cm²)?",
 "q-r26-t32-06": "All the angles in the accompanying figure are right angles. The figure is 12 cm wide and 8 cm tall, as marked. What is its perimeter (in cm)?",
 "q-r26-t32-07": "A rectangle has a perimeter of 34 cm, and its diagonal is 13 cm long. What is its area (in cm²)?"
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
MV.carry(_types.SimpleNamespace(**globals()), CARRY32)
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
