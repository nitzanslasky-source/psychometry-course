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
# Topic 32, fragment f4 (2026-10-14): the kite (deltoid) lesson geo-052 and its question geo32-g053, the trapezoid lesson
# geo-054 and its questions geo32-g055 and q-r26-t32-02, and the short lesson geo-056 (Quadrilaterals in Questions).
# Hebrew: geo 2158-2369 (the kite, its sample question, the trapezoid, its sample question) and 2370-2373 (the practice
# intro). Question videos: the question figure on the left (FIG_LEFT), our colour copy in the right column (Rule V3).
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g053', 'solve-geo32-g055', 'solve-q-r26-t32-02'})


def f4_pin(g):
    """layers pinned to their base, so a typed item may come between them (lesson learned in topic 31)"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


def f4_poly(pts, col='ink', w=3):
    return [('seg', pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], col, w) for i in range(len(pts))]


def f4_arc(P, Q, R, r, col, lab=None, lr=None):
    """the arc of the angle at P between rays P->Q and P->R (the side under 180 degrees)"""
    a, b = gdir(P[0], P[1], Q[0], Q[1]), gdir(P[0], P[1], R[0], R[1])
    if (b - a) % 360 > 180: a, b = b, a
    e = ('arc', P[0], P[1], r, a, b, col)
    if lab: e += (lab,) + ((lr,) if lr else ())
    return e


def f4_right(P, Q, R, s=14, col='teal'):
    a, b = gdir(P[0], P[1], Q[0], Q[1]), gdir(P[0], P[1], R[0], R[1])
    if (b - a) % 360 > 180: a, b = b, a
    return ('right', P[0], P[1], a, b, s, col)


def f4_lab(*pts):
    return [('txt', x, y, t, 'ink', 26, True) for x, y, t in pts]


# ------------------------------------------------------------------------------------------------ geo-052 (lesson: The Kite (Deltoid))
# Hebrew (geo 2158-2204): a kite is a rhombus squashed from below or from above; the bottom sides stay equal, the top is
# squashed symmetrically, so right = left; symmetric right-to-left but not top-to-bottom (the top triangle is not the
# bottom one); the diagonals are not equal: the main one (the symmetry line, joining the two angles between equal sides)
# and the secondary one; the main diagonal makes two congruent triangles, the secondary one doesn't; the diagonals are
# perpendicular; the main diagonal bisects the secondary one and the two angles it joins, like the altitude of an isosceles
# triangle; the secondary diagonal doesn't bisect its angles; a kite = two isosceles triangles on the same base (the
# secondary diagonal); the area = the product of the diagonals over two, why: the triangle ADC has base AC and height half
# of BD, times two; "exactly like the rhombus and the square". Added (2-3 examples per idea): a second, wide kite; area
# examples 10 and 6 -> 30, 12 and 8 -> 48; a non-example: two equal sides that face each other make no kite.
# V3: the rhombus dashed, the top pushed down with a dashed arrow, then the kite solid; equal sides ticked as named; the
# fold = the same tint on the left and right halves, then top and bottom tinted in two colours (not equal); the main
# diagonal teal, the secondary orange; the right angle and the equal halves marked at the words; the two isosceles
# triangles tinted in turn; for the area, the triangle ADC tinted and its height (half of BD) traced.
f4kA0, f4kB0, f4kD0, f4kC0 = (240, 60), (150, 195), (330, 195), (240, 330)     # the rhombus (AO = CO = 135, BO = DO = 90)
f4kA1 = (240, 145)                                                             # the squashed top
f4_kw = [(530, 140), (430, 215), (630, 215), (530, 290)]                      # a second, wide kite
f4k1 = GEO('f4k1', [
    ('line', f4_poly([f4kA0, f4kB0, f4kC0, f4kD0], 'ink', 2) + [('seg', 150, 195, 240, 60, 'ink', 2, True)]
             + f4_lab((240, 40, 'A'), (128, 195, 'B'), (240, 356, 'C'), (352, 195, 'D'))),
    ('rh', [('tick', *f4kA0, *f4kB0), ('tick', *f4kA0, *f4kD0), ('tick', *f4kB0, *f4kC0), ('tick', *f4kD0, *f4kC0),
            ('txt', 240, 392, 'a rhombus: four equal sides', 'teal', 22)]),
    ('push', [('dim', 100, 25, 300, 185), ('seg', 240, 70, 240, 130, 'orange', 3, True), ('txt', 268, 100, '↓', 'orange', 30),
              ('seg', *f4kB0, *f4kA1, 'ink', 3.5), ('seg', *f4kD0, *f4kA1, 'ink', 3.5), ('dot', *f4kA1)]),
    ('kite', [('dim', 100, 360, 300, 50), ('seg', *f4kB0, *f4kC0, 'ink', 3.5), ('seg', *f4kD0, *f4kC0, 'ink', 3.5),
              ('tick', *f4kB0, *f4kC0, 2), ('tick', *f4kD0, *f4kC0, 2), ('tick', *f4kA1, *f4kB0), ('tick', *f4kA1, *f4kD0),
              ('txt', 240, 392, 'a kite: two pairs of equal sides', 'orange', 22), ('txt', 240, 125, 'A', 'ink', 26, True)]),
    ('wide', f4_poly(f4_kw, 'ink', 3.5) + [('tick', *f4_kw[0], *f4_kw[1]), ('tick', *f4_kw[0], *f4_kw[2]),
              ('tick', *f4_kw[1], *f4_kw[3], 2), ('tick', *f4_kw[2], *f4_kw[3], 2), ('txt', 530, 320, 'another kite', 'ink', 22)]),
], vb='90 20 580 390', w=880, col=0, title='A rhombus squashed into a kite')
f4_KA, f4_KB, f4_KC, f4_KD, f4_KO = (320, 110), (200, 190), (320, 340), (440, 190), (320, 190)
f4_kl = f4_poly([f4_KA, f4_KB, f4_KC, f4_KD], 'ink', 3.5) + f4_lab((320, 88, 'A'), (176, 190, 'B'), (320, 368, 'C'), (464, 190, 'D')) \
    + [('tick', *f4_KA, *f4_KB), ('tick', *f4_KA, *f4_KD), ('tick', *f4_KB, *f4_KC, 2), ('tick', *f4_KD, *f4_KC, 2)]
f4k2 = GEO('f4k2', [
    ('line', f4_kl),
    ('sym', [('seg', *f4_KA, *f4_KC, 'teal', 3.5, True)]),
    ('lr', [('tint', [f4_KA, f4_KB, f4_KC], 'teal'), ('tint', [f4_KA, f4_KD, f4_KC], 'teal'), ('txt', 320, 405, 'left = right', 'teal', 24)]),
    ('tb', [('dim', 140, 60, 360, 360), ('seg', *f4_KB, *f4_KD, 'orange', 3.5, True), ('tint', [f4_KA, f4_KB, f4_KD], 'teal'),
            ('tint', [f4_KB, f4_KC, f4_KD], 'orange'), ('txt', 520, 150, 'top', 'teal', 24), ('txt', 520, 260, 'bottom', 'orange', 24),
            ('txt', 520, 300, 'not the same', 'red', 24)]),
], vb='130 60 470 360', w=760, col=0, title='A kite is symmetric right to left')
f4k3 = GEO('f4k3', [
    ('line', f4_kl),
    ('main', [('seg', *f4_KA, *f4_KC, 'teal', 4), ('txt', 270, 280, 'main', 'teal', 22)]),
    ('heads', [f4_arc(f4_KA, f4_KB, f4_KD, 26, 'teal'), f4_arc(f4_KC, f4_KB, f4_KD, 30, 'teal')]),
    ('two', [('tint', [f4_KA, f4_KB, f4_KC], 'teal'), ('tint', [f4_KA, f4_KD, f4_KC], 'teal')]),
    ('sec', [('seg', *f4_KB, *f4_KD, 'orange', 4), ('txt', 400, 175, 'secondary', 'orange', 22)]),
    ('nosym', [('tint', [f4_KA, f4_KB, f4_KD], 'orange'), ('txt', 520, 230, 'top ≠ bottom', 'red', 24)]),
], vb='130 60 470 340', w=760, col=0, title='The main and the secondary diagonal')
f4k4 = GEO('f4k4', [
    ('line', f4_kl + [('seg', *f4_KA, *f4_KC, 'teal', 3), ('seg', *f4_KB, *f4_KD, 'orange', 3)]),
    ('perp', [f4_right(f4_KO, f4_KD, f4_KC, 16, 'ink')]),
    ('half', [('tick', *f4_KB, *f4_KO, 3, 'orange'), ('tick', *f4_KO, *f4_KD, 3, 'orange')]),
    ('bisA', [f4_arc(f4_KA, f4_KB, f4_KO, 34, 'teal'), f4_arc(f4_KA, f4_KO, f4_KD, 40, 'teal'),
              f4_arc(f4_KC, f4_KB, f4_KO, 46, 'teal'), f4_arc(f4_KC, f4_KO, f4_KD, 52, 'teal')]),
    ('notB', [f4_arc(f4_KB, f4_KA, f4_KO, 30, 'red'), f4_arc(f4_KB, f4_KO, f4_KC, 40, 'orange'), ('txt', 140, 250, '≠', 'red', 30)]),
    ('iso1', [('tint', [f4_KA, f4_KB, f4_KD], 'teal')]),
    ('iso2', [('tint', [f4_KB, f4_KC, f4_KD], 'orange'), ('txt', 560, 190, 'one shared base: BD', 'ink', 22)]),
], vb='110 60 600 340', w=880, col=0, title='The diagonals of a kite')
f4k5 = GEO('f4k5', [
    ('line', f4_kl + [('seg', *f4_KA, *f4_KC, 'teal', 3), ('seg', *f4_KB, *f4_KD, 'orange', 3)]),
    ('adc', [('tint', [f4_KA, f4_KD, f4_KC], 'teal'), ('txt', 300, 260, 'base AC', 'teal', 22)]),
    ('h', [('seg', *f4_KO, *f4_KD, 'red', 6), ('txt', 385, 172, '½ BD', 'red', 24)]),
    ('abc', [('tint', [f4_KA, f4_KB, f4_KC], 'teal'), ('txt', 210, 280, '× 2', 'teal', 26)]),
], vb='150 60 340 330', w=520, col=0, title='The area of a kite')
f4k5a = IH('f4k5a', '$S=\\frac{AC\\cdot BD}{2}$', size=36)
f4k5b = IH('f4k5b', '$\\frac{10\\cdot6}{2}=30 \\qquad \\frac{12\\cdot8}{2}=48$', size=32)
for _it, _y in [(f4k5a, 160), (f4k5b, 260)]:
    _R(_it, _y, x=1100)
f4k2n = I('f4k2n', 'Equal sides next to each other, not facing each other', size=28)
_R(f4k2n, 600, x=320)
for _g in (f4k1, f4k2, f4k3, f4k4, f4k5): f4_pin(_g)
video('geo-052', 'lesson', slides=[
    S('The Kite (Deltoid)',
      L("Now the kite. On the exam it's called a deltoid. It looks like a kite you fly, so that's how it got its name.")),
    S('A squashed rhombus',
      L("A kite is really a rhombus that someone squashed a little, from above or from below. Here's a rhombus. All four "
        "of its sides are equal.", show(f4k1['line'], "Here's a rhombus"), show(f4k1['rh'], 'All four')),
      L("Now push its top corner down. The two bottom sides don't move, so they're still equal to each other, just like in "
        "the rhombus. The top was squashed evenly, so its two sides are still equal to each other too.",
        show(f4k1['push'], 'Now push its top corner down'), show(f4k1['kite'], "The two bottom sides don't move")),
      L("So a kite has two pairs of equal sides. The equal sides sit next to each other, not facing each other. Here's "
        "another kite, wide and short, and it works the same way.", pt('f4k1_kite', 'two pairs of equal sides'),
        show(f4k1['wide'], "Here's another kite"), show(f4k2n, 'The equal sides sit next to each other'))),
    S('Symmetric, but only one way',
      L("A kite is still symmetric, but only from right to left. If we draw the line from the top corner A down to the "
        "bottom corner C, and fold along it, the left half lands exactly on the right half.",
        show(f4k2['line'], 'A kite is still symmetric'), show(f4k2['sym'], 'If we draw the line'), show(f4k2['lr'], 'and fold along it')),
      L("But it's not symmetric from top to bottom. If we cut it along the other line, from B to D, the top triangle and "
        "the bottom triangle are not the same. The top one is small, and the bottom one is big.", show(f4k2['tb'], 'If we cut it along'))),
    S('The two diagonals',
      L("The diagonals of a kite are not necessarily equal. We give them names, the main diagonal and the secondary "
        "diagonal.", show(f4k3['line'], 'The diagonals of a kite')),
      L("The main diagonal is the kite's line of symmetry. It joins the two corners that sit between equal sides, here A "
        "and C. It cuts the kite into two triangles, left and right, that are exactly the same.",
        show(f4k3['main'], 'The main diagonal is'), show(f4k3['heads'], 'It joins the two corners'), show(f4k3['two'], 'It cuts the kite')),
      L("The secondary diagonal, from B to D, doesn't cut the kite into two equal parts. The triangle on top and the "
        "triangle at the bottom are different.", show(f4k3['sec'], 'The secondary diagonal'), show(f4k3['nosym'], 'The triangle on top'))),
    S('Two isosceles triangles',
      L("The diagonals of a kite are perpendicular to each other. And the main diagonal cuts the secondary one into two "
        "equal halves.", show(f4k4['line'], 'The diagonals of a kite'), show(f4k4['perp'], 'perpendicular to each other'),
        show(f4k4['half'], 'into two equal halves')),
      L("It's just like in an isosceles triangle, where the altitude to the base is also the median and the angle "
        "bisector. So the main diagonal also cuts the corners A and C into two equal angles.", show(f4k4['bisA'], 'So the main diagonal also cuts')),
      L("The secondary diagonal doesn't do that. At B, the angle above it and the angle below it are not equal.",
        show(f4k4['notB'], 'At B, the angle above it')),
      L("Really, a kite is made of two isosceles triangles, one on top, and one at the bottom, upside down. And both of "
        "them stand on the same base, the secondary diagonal B D.", show(f4k4['iso1'], 'one on top'), show(f4k4['iso2'], 'and one at the bottom'))),
    S('The area',
      L("The area of a kite is the product of the diagonals, over two. That's exactly like the rhombus and the square.",
        show(f4k5a, 'The area of a kite')),
      L("Why? The diagonals are perpendicular. Take the triangle A D C, the right half of the kite. Its base is the main "
        "diagonal, A C. Its height is the distance from D to that base, and that's half of the secondary diagonal.",
        show(f4k5['line'], 'Why? The diagonals'), show(f4k5['adc'], 'Take the triangle A D C'), show(f4k5['h'], 'Its height is the distance')),
      L("So its area is A C, times half of B D, over two. The left half is exactly the same triangle, so we multiply by "
        "two, and we're left with A C times B D, over two.", show(f4k5['abc'], 'The left half is exactly')),
      L("For example, if the diagonals are ten and six, the area is ten times six, over two, which is thirty. If they're "
        "twelve and eight, it's twelve times eight, over two, which is forty-eight. Next, let's see a question about a "
        "kite. [pause] Okay. I'll see you in the next video.", show(f4k5b, 'For example, if the diagonals'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g053 (Hebrew: the kite's sample question)
# Hebrew (geo 2207-2243): triangle BDC is isosceles (the kite's equal sides) with a 60 -> equilateral, BD = the given side;
# at the top 45 -> ADB = 45 (isosceles) -> A = 90: the silver triangle; hypotenuse to leg: divide by root 2 ("ignore the
# root, divide, attach the root"); the perimeter: 4 + 4 = 8, only one choice starts with 8 -> mark it; the root-2 tip
# (silver -> root 2, gold -> root 3); "if I add it all to the end"; the close: a kite is symmetric right to left only.
# English: 10 instead of 4; two choices start with 20, so the root-2 tip settles it.
# V3: the colour copy; BDC tinted with its two equal sides ticked and the 60 marked, then the other two 60s and BD = 10
# written; ABD tinted, the 45s and the right angle at A, the hypotenuse BD traced, 5 root 2 written on both legs; the outer
# path traced for the perimeter.
f4gA, f4gB, f4gC, f4gD = (320.0, 62.638), (234.085, 148.553), (320.0, 297.362), (405.915, 148.553)
f4_53base = f4_poly([f4gA, f4gB, f4gC, f4gD], 'ink', 2.5) + [('seg', *f4gB, *f4gD, 'ink', 2.5)] \
    + [('txt', 320, 42, 'A', 'ink', 22, True), ('txt', 212, 148, 'B', 'ink', 22, True), ('txt', 320, 320, 'C', 'ink', 22, True),
       ('txt', 428, 148, 'D', 'ink', 22, True)]
f4_53bdc = [('tint', [f4gB, f4gC, f4gD], 'teal'), ('tick', *f4gB, *f4gC, 2), ('tick', *f4gD, *f4gC, 2),
            ('txt', 252, 232, '10', 'teal', 22), ('txt', 388, 232, '10', 'teal', 22), f4_arc(f4gB, f4gD, f4gC, 24, 'teal', '60°', 46)]
f4_53eq = [f4_arc(f4gD, f4gB, f4gC, 24, 'teal', '60°', 46), f4_arc(f4gC, f4gB, f4gD, 26, 'teal', '60°', 48), ('txt', 320, 197, 'BD = 10', 'teal', 22)]
f4_53top = [('tint', [f4gA, f4gB, f4gD], 'orange'), f4_arc(f4gB, f4gA, f4gD, 24, 'orange', '45°', 46),
            f4_arc(f4gD, f4gA, f4gB, 24, 'orange', '45°', 46), f4_right(f4gA, f4gB, f4gD, 14, 'orange'),
            ('txt', 240, 92, '5√2', 'orange', 22), ('txt', 400, 92, '5√2', 'orange', 22)]
_f4_53vb = dict(vb='190 25 260 310', w=320)
f4g53 = GEO('f4g53', [
    ('line', f4_53base),
    ('bdc', f4_53bdc),
    ('eq', f4_53eq[:2]),
    ('bd', f4_53eq[2:]),
], title='Kite ABCD made of two special triangles', **_f4_53vb)
f4g53s = GEO('f4g53s', [
    ('line', f4_53base + f4_53bdc + f4_53eq),
    ('abd', f4_53top[:2]),
    ('d45', f4_53top[2:3]),
    ('a90', f4_53top[3:4]),
    ('hyp', [('seg', *f4gB, *f4gD, 'red', 5)]),
    ('legs', f4_53top[4:]),
], title='Kite ABCD: the top triangle', **_f4_53vb)
f4g53p = GEO('f4g53p', [
    ('line', f4_53base + f4_53bdc + f4_53eq + f4_53top),
    ('per', [('path', [f4gA, f4gB, f4gC, f4gD, f4gA], 'red', 7)]),
], title='Kite ABCD: the perimeter', **_f4_53vb)
f4g53t1 = IH('f4g53t1', '$\\frac{10}{\\sqrt2}=5\\sqrt2$', size=32)
f4g53t2 = IH('f4g53t2', '$10+10=20$', size=32)
f4g53t4 = IH('f4g53t4', '$P=20+5\\sqrt2+5\\sqrt2=20+10\\sqrt2$', size=30)
f4g53t3 = I('f4g53t3', 'Silver triangle $\\rightarrow\\ \\sqrt2$ $\\quad$ gold $\\rightarrow\\ \\sqrt3$', size=28)
for _g in (f4g53, f4g53s, f4g53p): f4_pin(_g); _R(_g, 180)
for _it, _y in [(f4g53t1, 260), (f4g53t2, 230), (f4g53t3, 300), (f4g53t4, 380)]:
    _R(_it, _y, x=1400)
video('solve-geo32-g053', 'solution', qid='geo32-g053', slides=[
    S('Two special triangles',
      L("A B C D is a deltoid. Given: A B is equal to A D, C B and C D are both ten centimeters, angle A B D is forty-five "
        "degrees, and angle D B C is sixty degrees. What is the perimeter of the deltoid, in centimeters?",
        pt('stem', 'A B C D is a deltoid', 'hl', 11.0), voice='calm', pause=0.5),
      L("For the perimeter we need all four sides. We know two of them, the tens. The line B D cuts the kite into two "
        "triangles, so let's look at them one at a time. [short pause] We'll start with the bottom one.",
        pt('fig: 10', 'We know two of them')),
      L("[short pause] Triangle B D C. In a kite, the two bottom sides are equal, so C B is ten and C D is ten. That makes "
        "the triangle isosceles, and it also has a sixty-degree angle at B.", show(f4g53['line'], 'Triangle B D C'),
        show(f4g53['bdc'], 'the two bottom sides are equal')),
      L("An isosceles triangle with a sixty-degree angle must be equilateral. The angle at D equals the angle at B, so it's "
        "sixty too, and then the angle at C is one hundred eighty minus one hundred twenty, which is sixty. Sixty, sixty, "
        "sixty. So all its sides are equal, and B D is ten as well.", show(f4g53['eq'], 'The angle at D equals'),
        show(f4g53['bd'], 'and B D is ten as well'))),
    S('The silver triangle',
      L("Now the top triangle, A B D. Its angle at B is forty-five. A B equals A D, so it's isosceles, and the angle at D is "
        "forty-five too. What's left for A is ninety.", show(f4g53s['line'], 'Now the top triangle'), show(f4g53s['abd'], 'Its angle at B'), show(f4g53s['d45'], 'and the angle at D'),
        show(f4g53s['a90'], "What's left for A")),
      L("Forty-five, forty-five, ninety. That's our silver triangle. Its hypotenuse is B D, ten. To get from the hypotenuse "
        "to a leg, we divide by root two. Ignore the root for a moment: ten divided by two is five. Then put the root back: "
        "five root two. So A B and A D are both five root two.", show(f4g53s['hyp'], 'Its hypotenuse is B D'),
        show(f4g53t1, 'we divide by root two'), show(f4g53s['legs'], 'So A B and A D'))),
    S('Use the choices',
      L("Now the perimeter. The two tens make twenty. Before adding the rest, look at the choices. Only two of them start "
        "with twenty, choice numbers one and three. So that already rules out the other two.",
        show(f4g53p['line'], 'Now the perimeter'), show(f4g53p['per'], 'Now the perimeter'), show(f4g53t2, 'The two tens make twenty'),
        mk('cross', 'choice 2', 'Only two of them'), mk('cross', 'choice 4', 'So that already rules out')),
      L("One of them has root three, and the other has root two. We're in a silver triangle, so the answer will have a "
        "root two. A whole-number hypotenuse gives a leg with root two, and the other way round. Root three belongs to the "
        "gold triangle, not here.", show(f4g53t3, 'We\'re in a silver triangle'), mk('cross', 'choice 1', 'Root three belongs')),
      L("And if we add it all to the end, twenty plus five root two plus five root two is twenty plus ten root two. Choice "
        "number three is our answer.", show(f4g53t4, 'And if we add it all'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("So the kite is symmetric, but only from right to left. Remember that, and you don't need to memorize all its "
        "rules. [pause] Okay. I'll see you in the next question.", pt('f4g53p_line', 'So the kite is symmetric'))),
])

# ------------------------------------------------------------------------------------------------ geo-054 (lesson: The Trapezoid)
# Hebrew (geo 2247-2311): four sides; the bottom and top sides are the bases, the sides are the legs; the bases are
# parallel (not equal), the legs are not parallel (else a parallelogram); two angles on the same leg add up to 180 (small +
# large, parallel lines and a transversal); the area = (a + b) h / 2, why: copy, flip, attach -> a parallelogram with base
# a + b, the trapezoid is half of it; "in the exam you won't prove formulas, memorize"; the isosceles trapezoid (equal legs,
# equal base angles beta = beta, so alpha = alpha; symmetric like an isosceles triangle, the legs continued close into an
# isosceles triangle; the diagonals are equal and cut each other into matching pieces); the right trapezoid (two right
# angles, never only one, because the bases are parallel). Kept from the English lesson: opposite angles of an isosceles
# trapezoid add up to 180; in questions, drop the height from D (a rectangle and a right triangle, Pythagoras).
# Added examples: 70 -> 110 on a leg; areas (10 + 6) 4 / 2 = 32 and (9 + 3) 5 / 2 = 30; a base angle 65 -> 65, 115, 115.
# V3: a general trapezoid built part by part (bases traced teal with parallel arrows, legs orange); a non-example (legs
# parallel -> a parallelogram) drawn small and red; the U of topic 30 traced on a leg; the area: the height dashed, then the
# flipped copy tinted orange next to it, the long base a + b written; the isosceles trapezoid: equal legs ticked, the base
# angles, the symmetry line, the legs continued dashed up to the top, the diagonals with their matching pieces ticked; the
# right trapezoid: the right angles, then the height from D dashed, the rectangle and the right triangle tinted.
f4tB, f4tC, f4tA, f4tD = (150, 290), (560, 290), (222.8, 90), (420, 90)
f4_tl = f4_poly([f4tA, f4tB, f4tC, f4tD], 'ink', 3.5) + f4_lab((222.8, 66, 'A'), (128, 300, 'B'), (582, 300, 'C'), (420, 66, 'D'))
f4t1 = GEO('f4t1', [
    ('line', f4_tl),
    ('bases', [('path', [f4tB, f4tC], 'teal', 7), ('path', [f4tA, f4tD], 'teal', 7), ('par', *f4tB, *f4tC), ('par', *f4tA, *f4tD),
               ('txt', 355, 322, 'base', 'teal', 22), ('txt', 321, 66, 'base', 'teal', 22)]),
    ('legs', [('path', [f4tA, f4tB], 'orange', 7), ('path', [f4tD, f4tC], 'orange', 7), ('txt', 155, 180, 'leg', 'orange', 22),
              ('txt', 520, 180, 'leg', 'orange', 22)]),
    ('non', f4_poly([(660, 150), (630, 250), (760, 250), (790, 150)], 'red', 3) + [('par', 630, 250, 660, 150, 1, 'red'),
             ('par', 760, 250, 790, 150, 1, 'red'), ('txt', 710, 285, 'legs parallel:', 'red', 20), ('txt', 710, 310, 'a parallelogram', 'red', 20)]),
], vb='100 40 720 300', w=1040, col=0, title='A trapezoid: two bases and two legs')
f4t2 = GEO('f4t2', [
    ('line', f4_tl + [('par', *f4tB, *f4tC), ('par', *f4tA, *f4tD)]),
    ('u', [('path', [f4tD, f4tA, f4tB, f4tC], 'orange', 7)]),
    ('b', [f4_arc(f4tB, f4tC, f4tA, 32, 'small', '70°', 56)]),
    ('a', [f4_arc(f4tA, f4tB, f4tD, 28, 'large', '110°', 54)]),
    ('cd', [f4_arc(f4tC, f4tD, f4tB, 32, 'small', 'small', 60), f4_arc(f4tD, f4tA, f4tC, 28, 'large', 'large', 56)]),
], vb='100 40 520 300', w=620, col=0, title='Two angles on one leg')
f4t2a = IH('f4t2a', '$180°-70°=110°$', size=32)
_R(f4t2a, 320, x=1180)
f4qB, f4qC, f4qA, f4qD = (60, 290), (300, 290), (110, 130), (220, 130)
f4qA2, f4qB2 = (410, 290), (460, 130)
f4t3 = GEO('f4t3', [
    ('line', f4_poly([f4qA, f4qB, f4qC, f4qD], 'ink', 3.5) + [('txt', 180, 318, 'a', 'teal', 26, True), ('txt', 165, 112, 'b', 'teal', 26, True)]),
    ('h', [('dot', *f4qA), ('seg', 110, 130, 110, 290, 'teal', 3, True), ('right', 110, 290, 0, 90, 12), ('txt', 94, 210, 'h', 'teal', 26, True)]),
    ('copy', [('tint', [f4qA, f4qB, f4qC, f4qD], 'teal'), ('tint', [f4qD, f4qC, f4qA2, f4qB2], 'orange')] + f4_poly([f4qD, f4qC, f4qA2, f4qB2], 'orange', 3.5)
             + [('txt', 355, 318, 'b', 'orange', 26, True), ('txt', 340, 112, 'a', 'orange', 26, True)]),
    ('base', [('seg', 60, 350, 410, 350, 'ink', 3), ('seg', 60, 340, 60, 360, 'ink', 3), ('seg', 410, 340, 410, 360, 'ink', 3),
              ('txt', 235, 378, 'a + b', 'ink', 26)]),
], vb='40 90 440 310', w=560, col=0, title='Two copies of a trapezoid make a parallelogram')
f4t3a = IH('f4t3a', '$S=\\frac{(a+b)\\cdot h}{2}$', size=36)
f4t3b = IH('f4t3b', '$\\frac{(10+6)\\cdot4}{2}=32$', size=32)
f4t3c = IH('f4t3c', '$\\frac{(9+3)\\cdot5}{2}=30$', size=32)
for _it, _y in [(f4t3a, 160), (f4t3b, 280), (f4t3c, 360)]:
    _R(_it, _y, x=1160)
f4iA, f4iD, f4iB, f4iC, f4iO, f4iT = (260, 140), (380, 140), (140, 300), (500, 300), (320, 180), (320, 60)
f4t4 = GEO('f4t4', [
    ('line', f4_poly([f4iA, f4iB, f4iC, f4iD], 'ink', 3.5) + f4_lab((250, 122, 'A'), (120, 310, 'B'), (520, 310, 'C'), (390, 122, 'D'))),
    ('legs', [('tick', *f4iA, *f4iB), ('tick', *f4iD, *f4iC)]),
    ('beta', [f4_arc(f4iB, f4iC, f4iA, 30, 'small', 'β', 52), f4_arc(f4iC, f4iD, f4iB, 30, 'small', 'β', 52)]),
    ('alpha', [f4_arc(f4iA, f4iB, f4iD, 26, 'large', 'α', 48), f4_arc(f4iD, f4iA, f4iC, 26, 'large', 'α', 48)]),
    ('sym', [('seg', 320, 125, 320, 315, 'teal', 3, True)]),
    ('top', [('seg', *f4iA, *f4iT, 'ink', 2.5, True), ('seg', *f4iD, *f4iT, 'ink', 2.5, True), ('tint', [f4iT, f4iB, f4iC], 'teal')]),
    ('diag', [('dim', 100, 40, 440, 290)] + f4_poly([f4iA, f4iB, f4iC, f4iD], 'ink', 3) + [('seg', *f4iA, *f4iC, 'orange', 4), ('seg', *f4iB, *f4iD, 'orange', 4),
              ('tick', *f4iA, *f4iO, 2, 'orange'), ('tick', *f4iD, *f4iO, 2, 'orange'), ('tick', *f4iO, *f4iC, 3, 'orange'),
              ('tick', *f4iO, *f4iB, 3, 'orange')]),
], vb='100 40 440 290', w=600, col=0, title='An isosceles trapezoid')
f4t4a = IH('f4t4a', '$65°,\\ 65°,\\ 115°,\\ 115°$', size=32)
f4t4b = I('f4t4b', 'Opposite angles: $\\ \\alpha+\\beta=180°$', size=30)
for _it, _y in [(f4t4a, 220), (f4t4b, 320)]:
    _R(_it, _y, x=1160)
f4rA, f4rD, f4rB, f4rC, f4rE = (180, 110), (360, 110), (180, 300), (520, 300), (360, 300)
f4t5 = GEO('f4t5', [
    ('line', f4_poly([f4rA, f4rB, f4rC, f4rD], 'ink', 3.5) + f4_lab((160, 96, 'A'), (160, 314, 'B'), (540, 314, 'C'), (370, 92, 'D'))),
    ('rB', [('right', 180, 300, 0, 90, 16)]),
    ('rA', [('right', 180, 110, 270, 360, 16), ('path', [f4rD, f4rA, f4rB, f4rC], 'orange', 6)]),
    ('h', [('dot', *f4rD), ('seg', *f4rD, *f4rE, 'teal', 3, True), ('right', 360, 300, 0, 90, 14), ('txt', 362, 326, 'E', 'ink', 26, True)]),
    ('parts', [('tint', [f4rA, f4rB, f4rE, f4rD], 'teal'), ('tint', [f4rD, f4rE, f4rC], 'orange'), ('txt', 270, 210, 'rectangle', 'teal', 22),
               ('txt', 470, 260, 'right triangle', 'orange', 20)]),
], vb='120 70 460 270', w=700, col=0, title='A right trapezoid')
for _g in (f4t1, f4t2, f4t3, f4t4, f4t5): f4_pin(_g)
video('geo-054', 'lesson', slides=[
    S('The Trapezoid',
      L("And the last quadrilateral, the trapezoid.")),
    S('Bases and legs',
      L("A trapezoid has four sides. The bottom side and the top side are called the bases. The two sides on the sides are "
        "called the legs.", show(f4t1['line'], 'A trapezoid has four sides'), show(f4t1['bases'], 'are called the bases'),
        show(f4t1['legs'], 'are called the legs')),
      L("The bases are parallel to each other. They're not equal, but they're parallel. The legs are not parallel. If they "
        "were parallel too, it wouldn't be a trapezoid anymore. It would be a parallelogram.", pt('f4t1_bases', 'The bases are parallel'),
        show(f4t1['non'], 'If they were parallel too')),
      L("So a trapezoid has exactly one pair of parallel sides, the bases.", pt('f4t1_bases', 'exactly one pair'))),
    S('Two angles on a leg',
      L("Two angles that sit on the same leg add up to one hundred eighty. Look at the leg A B. The bases are two parallel "
        "lines, and the leg cuts both of them. It's the U from lines and angles, a small angle plus a large angle, one "
        "hundred eighty.", show(f4t2['line'], 'Two angles that sit'), show(f4t2['u'], "It's the U from lines")),
      L("For example, if the angle at B is seventy, then the angle at A is one hundred eighty minus seventy, which is one "
        "hundred ten.", show(f4t2['b'], 'if the angle at B is seventy'), show(f4t2['a'], 'then the angle at A'), show(f4t2a, 'which is one hundred ten')),
      L("The same is true on the other leg, C D. A small angle at C plus a large angle at D make one hundred eighty.",
        show(f4t2['cd'], 'The same is true'))),
    S('The area',
      L("Let's call the bases a and b, and the height h. The height is the distance between the two bases, so it's "
        "perpendicular to them.", show(f4t3['line'], "Let's call the bases"), show(f4t3['h'], 'and the height h')),
      L("The area of a trapezoid is the sum of the bases, times the height, over two.", show(f4t3a, 'The area of a trapezoid')),
      L("Why? Here's a simple way to see it. Make a copy of the trapezoid, turn it upside down, and attach it on the "
        "right. The two trapezoids together make one big parallelogram.", show(f4t3['copy'], 'Make a copy')),
      L("The base of this parallelogram is a plus b, and its height is h. A parallelogram's area is its base times its "
        "height, so a plus b, times h. Our trapezoid is only half of it, so it's a plus b, times h, over two.",
        show(f4t3['base'], 'The base of this parallelogram')),
      L("In the exam you won't prove formulas, so what matters is to remember it. For example, bases ten and six, and "
        "height four. Ten plus six is sixteen, times four is sixty-four, over two is thirty-two. Another one, bases nine "
        "and three, height five. Nine plus three is twelve, twelve times five is sixty, over two is thirty.",
        show(f4t3b, 'For example, bases ten and six'), show(f4t3c, 'Another one, bases nine'))),
    S('The isosceles trapezoid',
      L("An isosceles trapezoid is a trapezoid whose legs are equal, just like its name says. The left side equals the "
        "right side.", show(f4t4['line'], 'An isosceles trapezoid'), show(f4t4['legs'], 'whose legs are equal')),
      L("Its two base angles at the bottom are equal, beta and beta. Each leg's two angles add up to one hundred eighty, so "
        "the top angles are equal too, alpha and alpha.", show(f4t4['beta'], 'Its two base angles'), show(f4t4['alpha'], 'so the top angles')),
      L("It's symmetric from right to left, a bit like an isosceles triangle. In fact, if we continued the legs up, they "
        "would close into an isosceles triangle.", show(f4t4['sym'], "It's symmetric from right"), show(f4t4['top'], 'if we continued the legs up')),
      L("For example, if a base angle is sixty-five, the other base angle is sixty-five too, and each top angle is one "
        "hundred eighty minus sixty-five, which is one hundred fifteen.", show(f4t4a, 'if a base angle is sixty-five')),
      L("Its diagonals are equal too. And they cut each other into matching pieces. The top pieces are equal to each other, "
        "and the bottom pieces are equal to each other.", show(f4t4['diag'], 'Its diagonals are equal too')),
      L("And since alpha plus beta is one hundred eighty, opposite angles, like A and C, also add up to one hundred eighty. "
        "That's useful in angle questions.", show(f4t4b, 'opposite angles, like A and C'))),
    S('The right trapezoid',
      L("A right trapezoid is simply a trapezoid with right angles. It always has two of them, never just one.",
        show(f4t5['line'], 'A right trapezoid'), show(f4t5['rB'], 'with right angles')),
      L("Why? If the angle at B is ninety, then the angle at A, on the same leg, is one hundred eighty minus ninety, which "
        "is ninety too.", show(f4t5['rA'], 'then the angle at A')),
      L("In questions, it helps to drop a height from D to the bottom base. Then the trapezoid splits into a rectangle and "
        "a right triangle, and Pythagoras does the rest.", show(f4t5['h'], 'drop a height from D'), show(f4t5['parts'], 'splits into a rectangle')),
      L("So we've seen a general trapezoid, the isosceles trapezoid, which is symmetric, and the right trapezoid, with its "
        "two right angles. Next, let's see a question. [pause] Okay. I'll see you in the next video.",
        pt('f4t5_parts', 'the right trapezoid, with its'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g055 (Hebrew: the trapezoid's sample question)
# Hebrew (geo 2314-2367): EC from the area of triangle DEC (legs times legs over 2); the tip for every trapezoid question:
# drop the heights, both of them; symmetric, so BF = EC; FE = AD = x; the common mistake: the middle is NOT a square (the
# drawing isn't accurate), it's a rectangle; the left triangle has the same area; the middle rectangle = the trapezoid
# minus the two triangles; length times width -> x; then the long way with the trapezoid formula, same answer, "much
# longer"; we saved it by understanding the symmetry. English: area 65, DE = 5, triangle 10 -> EC = 4, x = 9.
# V3: the colour copy; DEC tinted and its 10 written, EC = 4 written; the second height from A dashed (A pointed first);
# ABF tinted the same, BF = 4 and 10 written; the middle rectangle tinted orange with x on AD and FE, a red "not a
# square" note; 45 written in it; method 2 on a new slide: the bases labelled x and 4 + x + 4.
f4eA, f4eB, f4eC, f4eD, f4eE, f4eF = (192.25, 70.5), (119.25, 289.5), (520.75, 289.5), (447.75, 70.5), (447.75, 289.5), (192.25, 289.5)
f4_el = f4_poly([f4eA, f4eB, f4eC, f4eD], 'ink', 2.5) + [('seg', *f4eD, *f4eE, 'ink', 2.5), ('right', 447.75, 289.5, 0, 90, 14, 'ink')] \
    + [('txt', 178, 52, 'A', 'ink', 24, True), ('txt', 102, 306, 'B', 'ink', 24, True), ('txt', 538, 306, 'C', 'ink', 24, True),
       ('txt', 462, 52, 'D', 'ink', 24, True), ('txt', 447.75, 314, 'E', 'ink', 24, True), ('txt', 432, 180, '5', 'ink', 24)]
f4_55dec = [('tint', [f4eD, f4eE, f4eC], 'teal'), ('txt', 478, 255, '10', 'teal', 24), ('txt', 484, 334, '4', 'teal', 26)]
f4_55af = [('seg', *f4eA, *f4eF, 'teal', 3, True), ('right', 192.25, 289.5, 90, 180, 14), ('txt', 192.25, 314, 'F', 'ink', 24, True),
           ('tint', [f4eA, f4eB, f4eF], 'teal'), ('txt', 166, 255, '10', 'teal', 24), ('txt', 156, 334, '4', 'teal', 26)]
f4g55 = GEO('f4g55', [
    ('line', f4_el),
    ('dec', f4_55dec[:2]),
    ('ec', f4_55dec[2:]),
    ('af', [('dot', *f4eA)] + f4_55af[:3]),
    ('abf', f4_55af[3:]),
], vb='80 25 480 320', w=400, title='Isosceles trapezoid ABCD with both heights')
f4g55m = GEO('f4g55m', [
    ('line', f4_el + f4_55dec + f4_55af),
    ('mid', [('tint', [f4eA, f4eF, f4eE, f4eD], 'orange'), ('txt', 320, 52, 'x', 'orange', 26, True), ('txt', 320, 312, 'x', 'orange', 26, True)]),
    ('nsq', [('txt', 320, 140, 'not a square!', 'red', 24)]),
    ('v45', [('txt', 320, 200, '45', 'orange', 34)]),
    ('v9', [('txt', 352, 52, '= 9', 'red', 26)]),
], vb='80 25 480 320', w=400, title='The middle rectangle AFED')
f4g55b = GEO('f4g55b', [
    ('line', f4_el + [('seg', *f4eA, *f4eF, 'teal', 3, True), ('txt', 320, 52, 'x', 'orange', 26, True)]),
    ('bc', [('txt', 156, 334, '4', 'teal', 24), ('txt', 320, 334, 'x', 'orange', 24), ('txt', 484, 334, '4', 'teal', 24),
            ('path', [f4eB, f4eC], 'orange', 7)]),
], vb='80 25 480 320', w=400, title='The bases: x and x + 8')
f4g55a = IH('f4g55a', '$\\frac{5\\cdot EC}{2}=10\\ \\Rightarrow\\ EC=4$', size=30)
f4g55c = IH('f4g55c', '$65-10-10=45$', size=30)
f4g55d = IH('f4g55d', '$5x=45\\ \\Rightarrow\\ x=9$', size=30)
f4g55e = IH('f4g55e', '$\\frac{(x+x+8)\\cdot5}{2}=65$', size=30)
f4g55f = IH('f4g55f', '$(2x+8)\\cdot5=130$', size=30)
f4g55g = IH('f4g55g', '$10x+40=130\\ \\Rightarrow\\ x=9$', size=30)
for _g in (f4g55, f4g55m, f4g55b): f4_pin(_g); _R(_g, 190)
for _it, _y in [(f4g55a, 480), (f4g55c, 480), (f4g55d, 535), ]:
    _R(_it, _y)
for _it, _y in [(f4g55e, 200), (f4g55f, 300), (f4g55g, 370)]:
    _R(_it, _y, x=1460)
video('solve-geo32-g055', 'solution', qid='geo32-g055', slides=[
    SM('Method 1 · Symmetry', 'Drop both heights',
      L("The area of isosceles trapezoid A B C D is sixty-five square centimeters. D E is an altitude, D E is five "
        "centimeters, and the area of triangle D E C is ten square centimeters. What is A D, in centimeters?",
        pt('stem', 'The area of isosceles trapezoid', 'hl', 10.0), voice='calm', pause=0.5),
      L("A D is the short base at the top. [short pause] We'll solve it two ways, by using the symmetry, and then with the "
        "trapezoid area formula.", pt('fig: A', 'A D is the short base')),
      L("[short pause] Start with the small triangle D E C on the right. Its area is ten, and it's a right triangle, so its "
        "area is one leg times the other, over two. Five times E C, over two, equals ten. So E C is four.",
        show(f4g55['line'], 'Start with the small triangle'), show(f4g55['dec'], 'Its area is ten'),
        show(f4g55a, 'Five times E C'), show(f4g55['ec'], 'So E C is four')),
      L("Here's a tip for every trapezoid question: drop the heights, both of them. One height is already given, so we drop "
        "the second one, from A down to the base. Call its foot F.", show(f4g55['af'], 'from A down to the base')),
      L("The trapezoid is isosceles, so it's symmetric. Right equals left. So B F is four too, and the triangle A B F on the "
        "left also has area ten.", show(f4g55['abf'], 'So B F is four too'))),
    SM('Method 1 · Symmetry', 'Not a square',
      L("The middle part, A F E D, is a rectangle. Its top is A D, and its bottom, F E, is the same length. Let's call it "
        "x.", show(f4g55m['line'], 'The middle part'), show(f4g55m['mid'], 'The middle part')),
      L("Careful, here's a common mistake. In the drawing it looks like a square, but drawings on the exam don't have to "
        "be accurate. We don't know that x equals five. It's a rectangle.", show(f4g55m['nsq'], "In the drawing it looks like a square")),
      L("The whole trapezoid is sixty-five, and the two triangles are ten each. So what's left in the middle is sixty-five "
        "minus ten minus ten, which is forty-five.", show(f4g55c, 'So what\'s left in the middle'), show(f4g55m['v45'], 'which is forty-five')),
      L("The area of a rectangle is length times width. Five times x is forty-five, so x is nine. A D is nine, and choice "
        "number two is our answer.", show(f4g55d, 'Five times x is forty-five'), show(f4g55m['v9'], 'A D is nine'),
        mk('tick', 'choice 2', 'choice number two is our answer'))),
    SM('Method 2 · The area formula', 'The long way',
      L("[pause] Now, if you hadn't noticed the symmetry, you'd probably use the trapezoid formula, because the question is "
        "about a trapezoid's area. It works, but look how much longer it is."),
      L("The top base is x. The bottom base is four, plus x, plus four, so x plus eight. The sum of the bases is x plus x "
        "plus eight. Times the height, five, over two, equals sixty-five.", show(f4g55b['line'], 'The top base is x'),
        show(f4g55b['bc'], 'The bottom base is four'), show(f4g55e, 'The sum of the bases')),
      L("Multiply both sides by two: two x plus eight, times five, is one hundred thirty. Open the bracket: ten x plus "
        "forty is one hundred thirty. So ten x is ninety, and x is nine. Choice number two again.",
        show(f4g55f, 'Multiply both sides by two'), show(f4g55g, 'Open the bracket'), mk('tick', 'choice 2', 'Choice number two again')),
      L("Same answer, but much longer. The first way saved all that, just by seeing that the trapezoid is symmetric, so the "
        "middle must be forty-five. [pause] Okay. I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ q-r26-t32-02 (course question: a right trapezoid)
# A course addition (no Hebrew source); its method is the one the trapezoid lesson gives: drop the height from D, a
# rectangle and a right triangle, a triple, then the area formula. Trap: the slanted leg 10 used as the height (120).
# V3: the colour copy; AB marked as a height we don't know; the height from D dashed (D pointed first); ABED tinted, 9 on
# BE, 6 on EC; DEC tinted orange, the triple 6-8-10, 8 written on DE; then the area.
f4rqA, f4rqB, f4rqC, f4rqD, f4rqE = (150.0, 130.0), (150.0, 290.0), (450.0, 290.0), (330.0, 130.0), (330.0, 290.0)
f4_rb = f4_poly([f4rqA, f4rqB, f4rqC, f4rqD], 'ink', 2.5) + [('right', 150, 290, 0, 90, 13, 'ink'), ('right', 150, 130, 270, 360, 13, 'ink')] \
    + [('txt', 136, 116, 'A', 'ink', 22, True), ('txt', 136, 304, 'B', 'ink', 22, True), ('txt', 464, 304, 'C', 'ink', 22, True),
       ('txt', 344, 116, 'D', 'ink', 22, True), ('txt', 240, 114, '9', 'ink', 22), ('txt', 300, 330, '15', 'ink', 22),
       ('txt', 406, 202, '10', 'ink', 22)]
f4_rh = [('seg', *f4rqD, *f4rqE, 'teal', 3, True), ('right', 330, 290, 90, 180, 13), ('txt', 330, 312, 'E', 'ink', 22, True)]
f4_rr = [('tint', [f4rqA, f4rqB, f4rqE, f4rqD], 'teal'), ('txt', 240, 270, '9', 'teal', 24)]
f4_re = [('txt', 390, 270, '6', 'orange', 24)]
f4r = GEO('f4r', [
    ('line', f4_rb),
    ('ab', [('path', [f4rqA, f4rqB], 'red', 6), ('txt', 120, 210, '?', 'red', 28)]),
    ('h', [('dot', *f4rqD)] + f4_rh),
    ('rect', f4_rr),
    ('ec', f4_re),
], vb='110 95 380 240', w=420, title='Right trapezoid ABCD with the height DE')
f4r2 = GEO('f4r2', [
    ('line', f4_rb + f4_rh + f4_rr + f4_re),
    ('tri', [('tint', [f4rqD, f4rqE, f4rqC], 'orange'), ('txt', 312, 210, '8', 'orange', 26)]),
], vb='110 95 380 240', w=420, title='Right trapezoid ABCD: the triangle DEC')
f4r_a = IH('f4r_a', '$BE=AD=9\\ \\Rightarrow\\ EC=15-9=6$', size=28)
f4r_b = I('f4r_b', '$6,\\ 8,\\ 10$', size=30)
f4r_c = IH('f4r_c', '$S=\\frac{(9+15)\\cdot8}{2}=12\\cdot8=96$', size=28)
for _g in (f4r, f4r2): f4_pin(_g); _R(_g, 190)
for _it, _y in [(f4r_a, 480)]:
    _R(_it, _y)
for _it, _y in [(f4r_b, 220), (f4r_c, 300)]:
    _R(_it, _y, x=1480)
video('solve-q-r26-t32-02', 'solution', qid='q-r26-t32-02', slides=[
    S('Drop the height',
      L("A B C D is a right trapezoid, with A D parallel to B C, and angle A B C is ninety degrees. Given: A D is nine "
        "centimeters, B C is fifteen centimeters, and C D is ten centimeters. What is the area of the trapezoid, in square "
        "centimeters?", pt('stem', 'A B C D is a right trapezoid', 'hl', 11.0), voice='calm', pause=0.5),
      L("For the area we need the two bases, which we have, nine and fifteen, and the height. A B is a height, because it's "
        "perpendicular to both bases, but we don't know its length.", show(f4r['line'], 'For the area we need'), show(f4r['ab'], 'A B is a height')),
      L("[short pause] So let's drop a height from D down to B C, and call its foot E. Now the trapezoid is a rectangle, A B "
        "E D, and a right triangle, D E C.", show(f4r['h'], "let's drop a height from D"), show(f4r['rect'], 'Now the trapezoid is a rectangle')),
      L("In the rectangle, B E equals A D, nine. So E C is fifteen minus nine, which is six.", show(f4r_a, 'In the rectangle'),
        show(f4r['ec'], 'which is six'))),
    S('A triple, then the area',
      L("Now the right triangle D E C. Its hypotenuse is C D, ten, and one leg is six. That's the triple six, eight, ten, so "
        "the other leg, D E, is eight. That's the height.", show(f4r2['line'], 'Now the right triangle'), show(f4r2['tri'], 'Its hypotenuse is C D'), show(f4r_b, "That's the triple")),
      L("Now the area. Nine plus fifteen is twenty-four. Times eight, over two. Twenty-four over two is twelve, and twelve "
        "times eight is ninety-six. Choice number two is our answer.", show(f4r_c, 'Now the area'),
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("If you got one hundred twenty, you used C D, ten, as the height. But the slanted leg is not the height. The height "
        "is perpendicular to the bases. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 1', 'If you got one hundred twenty'))),
])

# ------------------------------------------------------------------------------------------------ geo-056 (lesson: Quadrilaterals in Questions)
# Hebrew (geo 2370-2373): last lesson we learned the rules of the quadrilaterals; now a set of basic-level questions.
# Kept from the English lesson: try each question yourself first; the name of the shape is a given (write its properties on
# the figure, only the useful ones); the answer often hides in a triangle. Added: one concrete example of each move.
f4n1 = I('f4n1', 'The name of the shape $\\rightarrow$ its properties, on the figure', size=30)
f4n2 = I('f4n2', 'Rhombus: $\\ $four equal sides, $\\ $diagonals at $90°$', size=28)
f4n3 = I('f4n3', 'Look for a useful triangle: $\\ $isosceles, $\\ $a triple, $\\ $gold or silver', size=28)
video('geo-056', 'lesson', slides=[
    S('Quadrilaterals in Questions',
      L("In the last lessons we learned the rules of the quadrilaterals. Now we'll practice a set of questions at a basic "
        "level. Try each question yourself first, and then watch the solution.")),
    S('How to start',
      L("Every question opens with the name of a shape: a parallelogram, a rectangle, a rhombus, a square, a deltoid, or a "
        "trapezoid. The name is a given. Write what it gives you right on the figure.", show(f4n1, 'Every question opens')),
      L("For example, if it says rhombus, mark all four sides as equal, and the diagonals as perpendicular. But write only "
        "the properties that help you in this question, not all of them.", show(f4n2, 'if it says rhombus')),
      L("And most of the time, the answer hides in a triangle: an isosceles triangle, a Pythagorean triple, or a gold or "
        "silver triangle. Let's start. [pause] Okay. I'll see you in the next video.", show(f4n3, 'the answer hides in a triangle'))),
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
