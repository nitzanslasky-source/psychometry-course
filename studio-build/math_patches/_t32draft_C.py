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
# Topic-32 fragment f3 (2026-10-14): the parallelogram questions geo32-g048, geo32-g049, q-r26-t32-01, the rhombus lesson
# geo-050 and the rhombus question geo32-g051 (Hebrew geo 2016-2160). Question figure on the left (FIG_LEFT, figw 0.56),
# our colour copy built in layers on the right (Rule V3). Every Hebrew method is kept; plugging in numbers (a course
# addition in g048) is explained on its own, because psychometric thinking comes later in the study plan.
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g048', 'solve-geo32-g049', 'solve-q-r26-t32-01', 'solve-geo32-g051'})


def f3_pin(g):
    """keep every layer on its base figure even when a typed board item comes between them"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


def f3_poly(pts, col='ink', w=3):
    return [('seg', pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], col, w) for i in range(len(pts))]


def f3_lab(pts, names, off, size=26):
    return [('txt', pts[k][0] + off[k][0], pts[k][1] + off[k][1], names[k], 'ink', size, True) for k in range(len(pts))]


# ------------------------------------------------------------------------------------------------ geo32-g048 (Hebrew: the parallelogram's first example)
# Hebrew (geo 2018-2041): only angles; opposite angles equal, adjacent angles add up to 180; all of angle B plus all of
# angle C is 180, divide to get alpha + beta; the angle sum in the small triangle; "we never found alpha or beta, but the
# angle is ...". English numbers 3a/2a, 3b/2b -> 72. Course addition kept: plugging in equal numbers (a rectangle).
# V3: the copy; the whole angle B tinted teal (5 alpha), the whole angle C tinted orange (5 beta); then the small triangle
# BCE tinted with its two angles 3 alpha / 3 beta traced and x in red; x = 72 written at E when found.
f3A8, f3B8, f3C8, f3D8, f3E8 = (291.283, 58.333), (202.717, 301.667), (348.717, 301.667), (437.283, 58.333), (306.937, 207.827)
f3aBA, f3aBE = gdir(*f3B8, *f3A8), gdir(*f3B8, *f3E8)
f3aCD, f3aCE = gdir(*f3C8, *f3D8), gdir(*f3C8, *f3E8)
f3aEB, f3aEC = gdir(*f3E8, *f3B8), gdir(*f3E8, *f3C8)
f3g48_lines = (f3_poly([f3A8, f3B8, f3C8, f3D8]) + [('seg', *f3B8, *f3E8, 'ink', 3), ('seg', *f3C8, *f3E8, 'ink', 3)]
               + f3_lab([f3A8, f3B8, f3C8, f3D8, f3E8], 'ABCDE', [(-14, -14), (-16, 16), (16, 16), (14, -14), (6, -22)])
               + [('arc', *f3B8, 26, 0, f3aBE, 'ink'), ('txt', 250, 286, '3α', 'ink', 20), ('arc', *f3B8, 44, f3aBE, f3aBA, 'ink'),
                  ('txt', 238, 246, '2α', 'ink', 20), ('arc', *f3C8, 26, f3aCE, 180, 'ink'), ('txt', 306, 276, '3β', 'ink', 20),
                  ('arc', *f3C8, 44, f3aCD, f3aCE, 'ink'), ('txt', 350, 234, '2β', 'ink', 20), ('arc', *f3E8, 20, f3aEB, f3aEC, 'ink'),
                  ('txt', 304, 238, 'x', 'ink', 20, True)])
f3g48 = f3_pin(GEO('f3g48', [
    ('line', f3g48_lines),
    ('wb', [('wedge', *f3B8, 62, 0, f3aBA, 'teal'), ('txt', 150, 262, '5α', 'teal', 28)]),
    ('wc', [('wedge', *f3C8, 62, f3aCD, 180, 'orange'), ('txt', 402, 262, '5β', 'orange', 28)]),
], vb='130 25 350 310', w=330, title='Parallelogram ABCD with the segments BE and CE'))
f3g48b = f3_pin(GEO('f3g48b', [
    ('line', f3g48_lines + [('txt', 300, 352, 'So far:  α + β = 36°', 'teal', 22)]),
    ('tri', [('tint', [f3B8, f3C8, f3E8], 'teal'), ('arc', *f3B8, 26, 0, f3aBE, 'teal', None), ('arc', *f3C8, 26, f3aCE, 180, 'teal'),
             ('arc', *f3E8, 22, f3aEB, f3aEC, 'red')]),
    ('val', [('txt', 425, 200, 'x = 72°', 'red', 26)]),
], vb='130 25 350 340', w=330, title='The small triangle BCE'))
f3g48p = f3_pin(GEO('f3g48p', [
    ('line', f3g48_lines),
    ('b90', [('txt', 205, 348, 'B = 5·18° = 90°', 'teal', 20), ('txt', 395, 348, 'C = 5·18° = 90°', 'orange', 20)]),
    ('v54', [('tint', [f3B8, f3C8, f3E8], 'teal'), ('txt', 425, 240, '3α = 54°', 'teal', 22), ('txt', 425, 270, '3β = 54°', 'teal', 22),
             ('txt', 425, 200, 'x = 72°', 'red', 26)]),
], vb='130 25 350 340', w=330, title='Plugging in alpha = beta = 18'))
f3k48a = IH('f3k48a', '$5\\alpha+5\\beta=180°$', size=28)
f3k48b = IH('f3k48b', '$\\alpha+\\beta=36°$', size=28)
f3k48c = IH('f3k48c', '$x=180°-3(\\alpha+\\beta)=180°-108°$', size=30)
for _it, _y in [(f3g48, 200), (f3g48b, 200), (f3k48c, 525), (f3g48p, 200)]:
    _R(_it, _y)
_R(f3k48a, 300, x=1375); _R(f3k48b, 355, x=1375)

video('solve-geo32-g048', 'solution', qid='geo32-g048', slides=[
    S('Adjacent angles',
      L("In parallelogram A B C D, the marked parts of angle B are three alpha and two alpha, and the marked parts of angle C "
        "are three beta and two beta. The segments B E and C E meet as in the accompanying figure. What is x?",
        pt('stem', 'In parallelogram A B C D', 'hl', 9.0), voice='calm', pause=0.5),
      L("There are only angles here, and letters instead of numbers. We need x, the angle at E between B E and C E. [short "
        "pause] We'll solve it two ways, with the angle rules of a parallelogram, and then by plugging in numbers.",
        pt('fig: x', 'We need x')),
      L("[short pause] What do we know about the angles of a parallelogram? Opposite angles are equal, and two angles next "
        "to each other add up to one hundred eighty. Angles B and C are next to each other, at the two ends of side B C.",
        show(f3g48['line'], 'What do we know')),
      L("All of angle B is three alpha plus two alpha, which is five alpha. All of angle C is three beta plus two beta, five "
        "beta. Together they make one hundred eighty.", show(f3g48['wb'], 'All of angle B'), show(f3g48['wc'], 'All of angle C'),
        show(f3k48a, 'Together they make')),
      L("Divide both sides by five, and alpha plus beta is thirty-six. We don't know alpha or beta on their own, but we know "
        "their sum.", show(f3k48b, 'Divide both sides by five'))),
    S('The triangle',
      L("Now look at triangle B C E, the small triangle at the bottom. Its angles are three alpha at B, three beta at C, and "
        "x at E. The angles of a triangle add up to one hundred eighty.", show(f3g48b['line'], 'Now look at triangle'),
        show(f3g48b['tri'], 'Its angles are three alpha')),
      L("So x is one hundred eighty minus three alpha minus three beta. Three alpha plus three beta is three times alpha "
        "plus beta, three times thirty-six, which is a hundred eight. So x is one hundred eighty minus a hundred eight, "
        "seventy-two.", show(f3k48c, 'So x is one hundred eighty minus three alpha'), show(f3g48b['val'], 'seventy-two')),
      L("We never found alpha or beta, but x is seventy-two. Choice number two is our answer.",
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      sb='Adjacent angles'),
    S('Plugging in numbers',
      L("[pause] Now a faster way, plugging in numbers. Only the sum of alpha and beta is fixed, thirty-six. The question "
        "expects one value of x, so any alpha and beta that add up to thirty-six must give that same x. So we can choose "
        "easy numbers that fit."),
      L("Let's take them equal, eighteen and eighteen. Then angle B is five times eighteen, ninety, and angle C is ninety "
        "too. The parallelogram becomes a rectangle, and that's allowed, because a rectangle is a parallelogram.",
        show(f3g48p['line'], "Let's take them equal"), show(f3g48p['b90'], 'Then angle B is five times eighteen')),
      L("In triangle B C E, three alpha is three times eighteen, fifty-four, and three beta is fifty-four too. So x is one "
        "hundred eighty minus fifty-four minus fifty-four, which is seventy-two. Choice number two again. [pause] Okay. "
        "I'll see you in the next question.", show(f3g48p['v54'], 'three alpha is three times eighteen'),
        mk('tick', 'choice 2', 'Choice number two again'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g049 (Hebrew: the parallelogram's second example)
# Hebrew (geo 2044-2069): the perpendicular makes a right triangle -> Pythagoras ("a lot"; similarity later); draw the
# givens conveniently: opposite sides equal (AB = CD, BC = AD), BE = what's left; a Pythagorean triple gives the height;
# area = base x height. English numbers 24, 17, 16 -> 8, 15, 17 -> 360. Course addition kept: the 408 trap.
# V3: the copy; AB traced teal with 17, BC traced orange with 24, BE red with 8; the right triangle ABE tinted inside the
# copy, then a focus step (the rest dimmed, ABE kept with its labels; it is big enough, no enlargement); 15 written on AE.
f3PA, f3PB, f3PC, f3PD, f3PE = (194.857, 54.857), (90.571, 305.143), (445.143, 305.143), (549.429, 54.857), (194.857, 305.143)
f3g49_lines = (f3_poly([f3PA, f3PB, f3PC, f3PD]) + [('seg', *f3PA, *f3PE, 'ink', 3), ('right', *f3PE, 90, 0, 16, 'ink')]
               + f3_lab([f3PA, f3PB, f3PC, f3PD, f3PE], 'ABCDE', [(-14, -16), (-16, 16), (16, 16), (14, -16), (0, 28)])
               + [('txt', 372, 34, '24', 'ink', 24), ('txt', 523, 180, '17', 'ink', 24), ('txt', 320, 330, '16', 'ink', 24)])
# the enlarged cut-out of triangle ABE (legs 8 and 15, hypotenuse 17), drawn on a cleared patch on the right
f3cE, f3cA, f3cB = (560.0, 300.0), (560.0, 70.0), (437.0, 300.0)
f3g49 = f3_pin(GEO('f3g49', [
    ('line', f3g49_lines),
    ('ab', [('seg', *f3PA, *f3PB, 'teal', 5), ('txt', 116, 172, '17', 'teal', 26)]),
    ('bc', [('seg', *f3PB, *f3PC, 'orange', 5), ('txt', 250, 352, 'BC = 24', 'orange', 24)]),
    ('be', [('seg', *f3PB, *f3PE, 'red', 6), ('txt', 142, 330, '8', 'red', 26)]),
    ('tri', [('tint', [f3PA, f3PB, f3PE], 'teal'), ('seg', *f3PA, *f3PB, 'teal', 4), ('seg', *f3PB, *f3PE, 'teal', 4),
             ('seg', *f3PE, *f3PA, 'teal', 4)]),
    ('cut', [('dim', 60, 10, 570, 360), ('tint', [f3PA, f3PB, f3PE], 'teal'), ('seg', *f3PA, *f3PB, 'teal', 4),
             ('seg', *f3PB, *f3PE, 'teal', 4), ('seg', *f3PE, *f3PA, 'teal', 4), ('right', *f3PE, 90, 180, 16, 'teal'),
             ('txt', 180, 38, 'A', 'ink', 26, True), ('txt', 74, 322, 'B', 'ink', 26, True), ('txt', 195, 332, 'E', 'ink', 26, True),
             ('txt', 116, 172, '17', 'teal', 28), ('txt', 142, 330, '8', 'red', 28)]),
    ('h15', [('txt', 220, 180, '15', 'orange', 30)]),
], vb='60 10 570 360', w=520, title='Parallelogram ABCD with the height AE'))
f3k49a = IH('f3k49a', '$S=24\\cdot15=360$', size=34)
for _it, _y in [(f3g49, 200), (f3k49a, 540)]:
    _R(_it, _y)

video('solve-geo32-g049', 'solution', qid='geo32-g049', slides=[
    S('Opposite sides, then Pythagoras',
      L("A B C D is a parallelogram, and A E is perpendicular to B C. Given: A D is twenty-four centimeters, C D is "
        "seventeen centimeters, and E C is sixteen centimeters. What is the area of the parallelogram, in square "
        "centimeters?", pt('stem', 'A B C D is a parallelogram', 'hl', 9.0), voice='calm', pause=0.5),
      L("The area of a parallelogram is base times height. The base can be B C, and its height is A E, the perpendicular. "
        "But we don't know A E. [short pause] Look, the moment we drop a perpendicular, we get a right triangle, A B E, and "
        "that takes us straight back to Pythagoras. When we need a missing side, we use Pythagoras a lot. Later we'll also "
        "find missing sides with similar triangles, but Pythagoras is the main tool.", pt('fig: E', 'we get a right triangle')),
      L("[short pause] Let's write the givens on the figure in a more convenient way. Opposite sides of a parallelogram are "
        "equal. C D is seventeen, so A B is also seventeen.", show(f3g49['line'], "Let's write the givens"),
        show(f3g49['ab'], 'so A B is also seventeen')),
      L("A D is twenty-four, so all of B C is twenty-four too. E C is sixteen, so what's left, B E, is twenty-four minus "
        "sixteen, which is eight.", show(f3g49['bc'], 'so all of B C'), show(f3g49['be'], "so what's left")),
      L("Now look at the right triangle A B E. Let's look only at it. Its legs are B E, eight, and A E, which "
        "we're looking for. Its hypotenuse is A B, seventeen.", show(f3g49['tri'], 'Now look at the right triangle'),
        show(f3g49['cut'], "Let's look only at it")),
      L("Eight, fifteen, seventeen is a Pythagorean triple. So the missing leg is fifteen, and that's the height A E.",
        show(f3g49['h15'], 'So the missing leg is fifteen')),
      L("The area is base times height. Twenty-four times fifteen is twenty-four times ten, two hundred forty, plus "
        "twenty-four times five, a hundred twenty. That's three hundred sixty. Choice number three is our answer.",
        show(f3k49a, 'Twenty-four times fifteen'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Careful, seventeen times twenty-four is four hundred eight, choice number four. That uses the slanted side "
        "seventeen instead of the height. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 4', 'choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t32-01 (course question)
# Course question (no Hebrew source): the height of an obtuse parallelogram falls outside; extend the base; the angle on
# the straight line is 30; a gold triangle (30-60-90, topic 31): the short leg is half the hypotenuse; area = 14 x 5.
# Traps kept: 140 (the slanted side), 70 root 3 (the long leg), 35 (the triangle formula).
# V3: the copy; the base BC traced teal with 14; point at B, then the dashed extension of CB; the dashed height AH with its
# right angle; the 30 at B; triangle ABH tinted (the gold triangle), 10 on AB, 5 written on AH when found.
f3QA, f3QB, f3QC, f3QD, f3QH = (79.474, 140.0), (270.0, 250.0), (578.0, 250.0), (387.474, 140.0), (79.474, 250.0)
f3aBAq = gdir(*f3QB, *f3QA)
f3t01_lines = (f3_poly([f3QA, f3QB, f3QC, f3QD]) + f3_lab([f3QA, f3QB, f3QC, f3QD], 'ABCD', [(-12, -16), (6, 26), (16, 20), (12, -16)])
               + [('arc', *f3QB, 26, 0, f3aBAq, 'ink'), ('txt', 300, 205, '150°', 'ink', 22), ('txt', 424, 278, '14', 'ink', 28),
                  ('txt', 150, 198, '10', 'ink', 28)])
f3t01 = f3_pin(GEO('f3t01', [
    ('line', f3t01_lines),
    ('base', [('seg', *f3QB, *f3QC, 'teal', 5)]),
    ('ext', [('dot', *f3QB), ('seg', *f3QB, *f3QH, 'teal', 3, True)]),
    ('h', [('seg', *f3QA, *f3QH, 'orange', 3, True), ('right', *f3QH, 0, 90, 16, 'orange'), ('txt', 62, 272, 'H', 'ink', 26, True)]),
    ('a30', [('tint', [f3QA, f3QB, f3QH], 'teal'), ('arc', *f3QB, 46, f3aBAq, 180, 'teal', '30°', 70)]),
    ('h5', [('txt', 54, 196, '5', 'orange', 34)]),
], vb='30 100 600 200', w=540, title='Parallelogram ABCD with the height AH outside'))
f3k01a = IH('f3k01a', '$AH=\\frac{10}{2}=5$', size=32)
f3k01b = IH('f3k01b', '$S=14\\cdot5=70$', size=32)
for _it, _y in [(f3t01, 230), (f3k01a, 460), (f3k01b, 520)]:
    _R(_it, _y)

video('solve-q-r26-t32-01', 'solution', qid='q-r26-t32-01', slides=[
    S('Extend the base',
      L("A B C D is a parallelogram. Given: A B is ten centimeters, B C is fourteen centimeters, and angle A B C is one "
        "hundred fifty degrees. What is the area of the parallelogram, in square centimeters?",
        pt('stem', 'A B C D is a parallelogram', 'hl', 8.0), voice='calm', pause=0.5),
      L("The area of a parallelogram is base times height. The base B C is fourteen, so we need the height to B C. [short "
        "pause] Angle B is obtuse, so first we need to see where that height falls.", pt('fig: 150°', 'Angle B is obtuse')),
      L("[short pause] Here's the base, B C, fourteen. We drop the height from A, straight down to the line of B C. Because "
        "angle B is obtuse, A is to the left of B, so the height falls outside the parallelogram.",
        show(f3t01['line'], "Here's the base"), show(f3t01['base'], 'B C, fourteen')),
      L("So we start at B and extend C B beyond B. Then we drop the height from A to that line, and call its foot H.",
        show(f3t01['ext'], 'So we start at B'), show(f3t01['h'], 'Then we drop the height')),
      L("Angle A B H and angle A B C sit together on one straight line, so angle A B H is one hundred eighty minus one "
        "hundred fifty, which is thirty.", show(f3t01['a30'], 'so angle A B H is')),
      L("Triangle A B H has a right angle and a thirty degree angle, so it's a gold triangle, thirty, sixty, ninety. A B is "
        "its hypotenuse, ten. The height A H is across from the thirty, so it's the short leg, and the short leg is half "
        "the hypotenuse. Half of ten is five.", show(f3k01a, 'Half of ten is five'), show(f3t01['h5'], 'Half of ten')),
      L("The area is base times height, fourteen times five, seventy. Choice number three is our answer.",
        show(f3k01b, 'fourteen times five'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("So when you see a thirty degree angle, or a hundred fifty next to it, the height is half the slanted side. And the "
        "other choices are traps. A hundred forty is fourteen times ten, the slanted side instead of the height. Seventy "
        "root three uses the long leg instead of the short one. And thirty-five divides by two, which is the triangle "
        "formula. [pause] Okay. I'll see you in the next question.", mk('cross', 'choice 1', 'A hundred forty is'),
        mk('cross', 'choice 2', 'Seventy root three uses'), mk('cross', 'choice 4', 'And thirty-five divides'))),
])

# ------------------------------------------------------------------------------------------------ geo-050 (lesson: The Rhombus)
# Hebrew (geo 2074-2120): all sides equal, opposite angles equal; a "perfected parallelogram"; we shortened a parallelogram
# into a rhombus; the diagonals: perpendicular, not equal (long and short), bisect each other, bisect the angles; instead of
# remembering the rules remember the shape and its symmetry (right = left, top = bottom); area = diagonal x diagonal / 2,
# with why (half-diagonals = legs, x 4). Course additions kept: equal diagonals -> a square; diagonals 10 and 6 -> 30; base x
# height works too. Added examples: side 7 -> perimeter 28; 60 and 120 angles; diagonals 8 and 12 -> 48.
# V3: a clean generic rhombus; ticks on all four sides; opposite angles in matching colours; the diagonals drawn in at the
# words with their right angle, halves ticked and half-angles; the symmetry as tints (left/right teal, top/bottom orange);
# for the area one small right triangle tinted, its legs = the half-diagonals.
f3RA, f3RB, f3RC, f3RD, f3RO = (320.0, 30.0), (200.0, 180.0), (320.0, 330.0), (440.0, 180.0), (320.0, 180.0)
f3rh = [f3RA, f3RB, f3RC, f3RD]
f3rh_lab = f3_lab(f3rh, 'ABCD', [(0, -18), (-22, 0), (0, 22), (22, 0)])
f3aAB, f3aAD = gdir(*f3RA, *f3RB), gdir(*f3RA, *f3RD)
f3aBA, f3aBC = gdir(*f3RB, *f3RA), gdir(*f3RB, *f3RC)
f3aCB, f3aCD = gdir(*f3RC, *f3RB), gdir(*f3RC, *f3RD)
f3aDC, f3aDA = gdir(*f3RD, *f3RC), gdir(*f3RD, *f3RA)
f3sides = [('tick', *f3RA, *f3RB, 1), ('tick', *f3RB, *f3RC, 1), ('tick', *f3RC, *f3RD, 1), ('tick', *f3RD, *f3RA, 1)]
f3r1 = GEO('f3r1', [
    ('line', f3_poly(f3rh) + f3rh_lab + f3sides),
    ('ang', [('arc', *f3RA, 34, f3aAB, f3aAD, 'small'), ('arc', *f3RC, 34, f3aCD, f3aCB, 'small'),
             ('arc', *f3RB, 30, f3aBC, f3aBA, 'large'), ('arc', *f3RD, 30, f3aDA, f3aDC, 'large')]),
    ('par', [('par', *f3RB, *f3RA, 1), ('par', *f3RC, *f3RD, 1), ('par', *f3RA, *f3RD, 2), ('par', *f3RB, *f3RC, 2)]),
], vb='140 -15 360 370', w=520, col=0, title='A rhombus')
f3r2 = GEO('f3r2', [
    ('line', f3_poly(f3rh) + f3rh_lab),
    ('diag', [('seg', *f3RA, *f3RC, 'teal', 3), ('seg', *f3RB, *f3RD, 'teal', 3), ('right', *f3RO, 0, 90, 16, 'teal')]),
    ('len', [('txt', 350, 96, 'long', 'orange', 24), ('txt', 236, 164, 'short', 'teal', 24)]),
    ('half', [('tick', *f3RA, *f3RO, 1, 'orange'), ('tick', *f3RO, *f3RC, 1, 'orange'), ('tick', *f3RB, *f3RO, 2, 'teal'),
              ('tick', *f3RO, *f3RD, 2, 'teal')]),
    ('hang', [('arc', *f3RA, 40, f3aAB, 270, 'small'), ('arc', *f3RA, 48, 270, f3aAD, 'small'),
              ('arc', *f3RB, 30, f3aBC, 0, 'large'), ('arc', *f3RB, 38, 0, f3aBA, 'large')]),
], vb='140 -15 360 370', w=520, col=0, title='The diagonals of a rhombus')
f3r3 = GEO('f3r3', [
    ('line', f3_poly(f3rh) + f3rh_lab + f3sides + [('seg', *f3RA, *f3RC, 'ink', 2, True), ('seg', *f3RB, *f3RD, 'ink', 2, True)]),
    ('lr', [('tint', [f3RA, f3RB, f3RC], 'teal'), ('tint', [f3RA, f3RD, f3RC], 'teal'), ('seg', *f3RA, *f3RC, 'teal', 5)]),
    ('tb', [('dim', 140, -15, 360, 370), ('tint', [f3RB, f3RA, f3RD], 'orange'), ('tint', [f3RB, f3RC, f3RD], 'orange'),
            ('seg', *f3RB, *f3RD, 'orange', 5)] + f3_poly(f3rh) + f3rh_lab),
], vb='140 -15 360 370', w=520, col=0, title='The rhombus is symmetric')
f3r4 = GEO('f3r4', [
    ('line', f3_poly(f3rh) + f3rh_lab + [('seg', *f3RA, *f3RC, 'ink', 2, True), ('seg', *f3RB, *f3RD, 'ink', 2, True)]),
    ('q', [('tint', [f3RA, f3RO, f3RD], 'teal'), ('right', *f3RO, 0, 90, 16, 'teal'), ('txt', 340, 108, 'd₁/2', 'orange', 22),
           ('txt', 380, 200, 'd₂/2', 'teal', 22)]),
], vb='140 -15 360 370', w=520, col=0, title='One of the four right triangles')
for _g in (f3r1, f3r2, f3r3, f3r4): f3_pin(_g)
f3r_t1 = I('f3r_t1', 'Side $7$: $\\ P=4\\cdot7=28$', size=30, col=1)
f3r_t2 = I('f3r_t2', '$60°$ and $60°$, $\\ 120°$ and $120°$', size=30, col=1)
f3r_t3 = I('f3r_t3', 'Equal diagonals $\\to$ a square', size=30, col=1)
f3r_t4 = I('f3r_t4', '$S=\\frac{d_1\\cdot d_2}{2}$', size=36, col=1)
f3r_t5 = I('f3r_t5', '$10$ and $6$: $\\ \\frac{10\\cdot6}{2}=30$', size=30, col=1)
f3r_t6 = I('f3r_t6', '$8$ and $12$: $\\ \\frac{8\\cdot12}{2}=48$', size=30, col=1)
f3r_t7 = I('f3r_t7', 'Symmetric: right $=$ left, top $=$ bottom', size=28, col=1)

video('geo-050', 'lesson', slides=[
    S('The Rhombus',
      L("The rhombus.")),
    S('Four equal sides',
      L("A rhombus is a quadrilateral with all four sides equal. Its opposite angles are equal too.",
        show(f3r1['line'], 'A rhombus is a quadrilateral'), show(f3r1['ang'], 'Its opposite angles')),
      L("A rhombus is like a perfected parallelogram. Like a parallelogram, its opposite sides are equal and parallel, and "
        "on top of that, all four sides are equal. In the quadrilaterals lesson, we shortened a parallelogram until all its "
        "sides were equal, and that gave us a rhombus.", show(f3r1['par'], 'its opposite sides are equal and parallel')),
      L("For example, a rhombus with side seven has a perimeter of four times seven, twenty-eight. And if one angle is sixty "
        "degrees, the opposite angle is sixty too, and the other two are one hundred twenty each, because two angles next "
        "to each other add up to one hundred eighty, like in every parallelogram.", show(f3r_t1, 'a rhombus with side seven'),
        show(f3r_t2, 'if one angle is sixty'))),
    S('The diagonals',
      L("Now the diagonals. They're perpendicular to each other, so they meet at a right angle.",
        show(f3r2['line'], 'Now the diagonals'), show(f3r2['diag'], "They're perpendicular")),
      L("Are they equal? Not necessarily. Usually there's a long diagonal and a short one. If the two diagonals are equal, "
        "the rhombus is a square.", show(f3r2['len'], "Usually there's a long diagonal"), show(f3r_t3, 'If the two diagonals are equal')),
      L("They cut each other in half, and they also cut the angles of the rhombus in half.",
        show(f3r2['half'], 'They cut each other in half'), show(f3r2['hang'], 'they also cut the angles'))),
    S('Remember: symmetry',
      L("Instead of remembering all these rules, the sides, the angles and the diagonals, just remember the shape, and "
        "remember that it's symmetric.", show(f3r3['line'], 'just remember the shape'), show(f3r_t7, "remember that it's symmetric")),
      L("This diagonal is a line of symmetry. The triangle on the right is exactly like the triangle on the left. So the "
        "sides up here are equal, the sides down here are equal, and the angle on the right equals the angle on the left.",
        show(f3r3['lr'], 'This diagonal is a line of symmetry')),
      L("And it's not only symmetric right to left, it's also symmetric top to bottom. The top triangle is exactly like the "
        "bottom one, and the top angle equals the bottom angle.", show(f3r3['tb'], "it's also symmetric top to bottom")),
      L("So all the sides are equal, opposite angles are equal, and the diagonals are perpendicular, cut each other in half, "
        "and cut the angles in half.", pt('f3r_t7', 'So all the sides are equal'))),
    S('Area: d₁ × d₂ / 2',
      L("The area of a rhombus is the product of the diagonals, over two. Why? Take half of one diagonal and half of the "
        "other. They're the legs of a small right triangle.", show(f3r4['line'], 'The area of a rhombus'),
        show(f3r4['q'], 'Take half of one diagonal')),
      L("Its area is leg times leg, over two. The rhombus is four of these triangles, so we multiply by four. What we end up "
        "with is diagonal times diagonal, over two.", show(f3r_t4, 'diagonal times diagonal')),
      L("For example, diagonals ten and six. Ten times six is sixty, over two, thirty. Another one, diagonals eight and "
        "twelve. Eight times twelve is ninety-six, over two, forty-eight.", show(f3r_t5, 'diagonals ten and six'),
        show(f3r_t6, 'diagonals eight and twelve')),
      L("And a rhombus is also a parallelogram, so base times height works too, if that's what you're given. [pause] Okay. "
        "I'll see you in the next video.", pt('f3r_t4', 'base times height works too'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g051 (Hebrew: the rhombus question)
# Hebrew (geo 2122-2159): why "absolute" difference; two equations with two unknowns (a the bigger one), add them, b
# cancels; the other diagonal; the diagonals bisect each other (halves); the side from a right triangle and a Pythagorean
# triple; all sides equal -> perimeter; the closing tip (a rhombus is symmetric). English 46 / 14 -> 30, 16 -> 15, 8, 17 -> 68.
# Course addition: the 240 trap (the area).
# V3: typed equations first; then the copy (enlarged, the rhombus is thin) with the diagonals traced and their lengths, the
# halves written on, one quarter triangle tinted inside the copy and then an ENLARGED cut-out of it (same tint, labels 8 and
# 15) where the side 17 is found; 17 written on the original side too.
f3MA, f3MB, f3MC, f3MD, f3MO = (320.0, 45.231), (263.846, 180.0), (320.0, 314.769), (376.154, 180.0), (320.0, 180.0)
f3g51_lines = f3_poly([f3MA, f3MB, f3MC, f3MD]) + [('seg', *f3MA, *f3MC, 'ink', 3), ('seg', *f3MB, *f3MD, 'ink', 3)] + \
    f3_lab([f3MA, f3MB, f3MC, f3MD], 'ABCD', [(0, -20), (-22, 0), (0, 24), (22, 0)])
f3qE, f3qT, f3qR = (470.0, 320.0), (470.0, 80.0), (598.0, 320.0)       # enlarged quarter: legs 15 (up) and 8 (right)
f3g51 = f3_pin(GEO('f3g51', [
    ('line', f3g51_lines),
    ('ac', [('seg', *f3MA, *f3MC, 'teal', 5), ('txt', 292, 108, '30', 'teal', 26)]),
    ('bd', [('seg', *f3MB, *f3MD, 'orange', 5), ('txt', 286, 204, '16', 'orange', 26)]),
    ('half', [('tick', *f3MA, *f3MO, 1, 'teal'), ('tick', *f3MO, *f3MC, 1, 'teal'), ('tick', *f3MB, *f3MO, 2, 'orange'),
              ('tick', *f3MO, *f3MD, 2, 'orange'), ('txt', 340, 252, '15', 'teal', 24), ('txt', 352, 162, '8', 'orange', 24)]),
    ('q', [('tint', [f3MA, f3MO, f3MD], 'teal'), ('seg', *f3MA, *f3MD, 'teal', 5), ('right', *f3MO, 0, 90, 12, 'teal')]),
    ('cut', [('tint', [f3qT, f3qE, f3qR], 'teal')] + f3_poly([f3qT, f3qE, f3qR], 'teal', 4)
            + [('right', *f3qE, 0, 90, 18, 'teal'), ('txt', 450, 200, '15', 'teal', 30), ('txt', 534, 346, '8', 'orange', 30),
               ('txt', 470, 62, 'A', 'ink', 24, True), ('txt', 452, 340, 'O', 'ink', 24, True),
               ('txt', 612, 340, 'D', 'ink', 24, True)]),
    ('s17', [('txt', 560, 190, '17', 'red', 32), ('txt', 372, 100, '17', 'red', 24)]),
    ('per', [('txt', 560, 45, 'P = 4 · 17 = 68', 'red', 24)]),
], vb='230 25 410 335', w=470, title='Rhombus ABCD with its diagonals'))
f3k51a = IH('f3k51a', '$a+b=46$', size=32)
f3k51b = IH('f3k51b', '$a-b=14$', size=32)
f3k51c = IH('f3k51c', '$2a=60$: $\\ a=30,\\ b=16$', size=32)
for _it, _y in [(f3k51a, 230), (f3k51b, 290), (f3k51c, 360), (f3g51, 190)]:
    _R(_it, _y)

video('solve-geo32-g051', 'solution', qid='geo32-g051', slides=[
    S('Two equations',
      L("The sum of the lengths of the diagonals of a rhombus is forty-six centimeters. The absolute difference between "
        "their lengths is fourteen centimeters. What is its perimeter, in centimeters?",
        pt('stem', 'The sum of the lengths', 'hl', 8.0), voice='calm', pause=0.5),
      L("Why does it say absolute difference? So we don't get tangled up with big minus small or small minus big. A length "
        "can't be negative, so the difference is simply the big one minus the small one. [short pause] We'll find the two "
        "diagonals first, and then use them to find the side.", pt('stem', 'Why does it say absolute difference')),
      L("[short pause] Let's call the diagonals a and b, with a the bigger one. Then a plus b is forty-six, and a minus b is "
        "fourteen. Two equations, two unknowns.", show(f3k51a, 'Then a plus b is forty-six'), show(f3k51b, 'and a minus b')),
      L("Add the two equations. Plus b and minus b cancel, so two a is sixty, and a is thirty. That's the bigger diagonal. "
        "And b, thirty minus what gives fourteen? Sixteen. So b is sixteen.", show(f3k51c, 'so two a is sixty'))),
    S('Half-diagonals and a triple',
      L("Now the figure. The long diagonal is thirty, and the short one is sixteen. The diagonals of a rhombus cut each "
        "other in half, so we split thirty into fifteen and fifteen, and sixteen into eight and eight.",
        show(f3g51['line'], 'Now the figure'), show(f3g51['ac'], 'The long diagonal is thirty'),
        show(f3g51['bd'], 'and the short one is sixteen'), show(f3g51['half'], 'so we split thirty')),
      L("We need the perimeter, so we need the side. The diagonals are perpendicular, so each quarter of the rhombus is a "
        "right triangle, with legs eight and fifteen, and the side as its hypotenuse. Here it is, bigger.",
        show(f3g51['q'], 'each quarter of the rhombus'), show(f3g51['cut'], 'Here it is, bigger')),
      L("Eight, fifteen, seventeen is a Pythagorean triple. So the side is seventeen.", show(f3g51['s17'], 'So the side is seventeen')),
      L("All four sides of a rhombus are equal, so the perimeter is four times seventeen, sixty-eight. Choice number two is "
        "our answer. Careful, two hundred forty is thirty times sixteen over two, the area, not the perimeter.",
        show(f3g51['per'], 'four times seventeen'), mk('tick', 'choice 2', 'Choice number two is our answer'),
        mk('cross', 'choice 4', 'Careful, two hundred forty')),
      L("One tip to take from here. Instead of remembering all the rules of a rhombus, remember that it's symmetric, right "
        "equals left and top equals bottom. Then you can always see its angles, its sides and its diagonals. [pause] Okay. "
        "I'll see you in the next question."),
      sb='Half-diagonals and a triple'),
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
