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
# Topic-32 question block 1 (fragment f5, 2026-10-14): geo32-g057 ... geo32-g060, the Hebrew "quadrilaterals basics
# learning" sample questions (geo 2370-2560). Question figure on the left (FIG_LEFT, figw 0.56), our colour copy built in
# layers on the right (Rule V3). All the working is written inside the copy (txt rows under / beside the shape), so the
# layers stay consecutive. Every Hebrew method is kept.
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g057', 'solve-geo32-g058', 'solve-geo32-g059', 'solve-geo32-g060'})


def f5_arc(P, Q, R, r, col, label=None, lr=None):
    """the inside angle at P between the rays P->Q and P->R (the smaller one)"""
    a, b = gdir(*P, *Q), gdir(*P, *R)
    if (b - a) % 360 > 180: a, b = b, a
    e = ('arc', P[0], P[1], r, a, b, col)
    if label: e = e + (label,) + ((lr,) if lr else ())
    return e


def f5_wedge(P, Q, R, r, col):
    a, b = gdir(*P, *Q), gdir(*P, *R)
    if (b - a) % 360 > 180: a, b = b, a
    return ('wedge', P[0], P[1], r, a, b, col)


def f5_poly(pts, col='ink', w=3):
    n = len(pts)
    return [('seg', pts[k][0], pts[k][1], pts[(k + 1) % n][0], pts[(k + 1) % n][1], col, w) for k in range(n)]


def f5_lab(pts, names, off, size=26):
    return [('txt', p[0] + o[0], p[1] + o[1], nm, 'ink', size, True) for p, nm, o in zip(pts, names, off)]


def f5_mid(P, Q):
    return ((P[0] + Q[0]) / 2.0, (P[1] + Q[1]) / 2.0)


def f5_pin(g):
    """every layer is drawn at its base figure's box (fig / of), so a base that the renderer shrinks to fit keeps its
    layers on top of it"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


def f5_sector(P, Q, R, r, col, n=14):
    """a tinted sector for the inside angle at P (a polygon: the board draws polygons exactly)"""
    a, b = gdir(*P, *Q), gdir(*P, *R)
    if (b - a) % 360 > 180: a, b = b, a
    span = (b - a) % 360
    return ('tint', [P] + [gpt(P[0], P[1], r, a + span * k / float(n)) for k in range(n + 1)], col)


# ------------------------------------------------------------------------------------------------ geo32-g057 (Hebrew: the first sample question)
# Hebrew (geo 2375-2408): the angle sum of every quadrilateral is 360; call the fourth angle beta; alpha + beta = 140 (here
# 146); 70/70 or 100/40 are possible, but neither angle can be 140 (146) or more, because the other would be 0; then the
# choices are checked one by one, including the "it looks acute" trap (figures are not to scale).
# V3: the copy with the two given angles; beta drawn at D when it is named; the sum written under the shape; the two
# unknown angles tinted together (they share 146); the impossible case in red; each choice checked in its own row; the
# "looks acute" trap: alpha's corner tinted red with "not to scale".
f5A, f5B, f5C, f5D = (180.0, 273.333), (460.0, 273.333), (499.514, 114.852), (127.555, 143.528)
f5q57 = f5_poly([f5A, f5B, f5C, f5D]) + f5_lab([f5A, f5B, f5C, f5D], 'ABCD', [(-18, 16), (18, 16), (18, -10), (-18, -10)])
f5g57 = GEO('f5g57', [
    ('line', f5q57 + [f5_arc(f5A, f5B, f5D, 36, 'orange', '118°', 62), f5_arc(f5B, f5A, f5C, 36, 'orange', '96°', 60),
                      f5_arc(f5C, f5B, f5D, 30, 'red', 'α', 52)]),
    ('beta', [f5_arc(f5D, f5A, f5C, 30, 'small', 'β', 52)]),
    ('sum', [('txt', 330, 335, '118° + 96° + α + β = 360°', 'ink', 26)]),
    ('ab', [('txt', 330, 375, 'α + β = 360° − 214° = 146°', 'red', 26)]),
    ('pair', [f5_sector(f5C, f5B, f5D, 30, 'red'), f5_sector(f5D, f5A, f5C, 30, 'teal')]),
    ('zero', [('txt', 330, 415, 'α = 146°  →  β = 0°   ✗', 'red', 26)]),
    ('c1', [('txt', 330, 445, '26 + 120 ✓   70 + 76 ✓', 'teal', 24)]),
    ('c3', [f5_sector(f5C, f5B, f5D, 30, 'red'), ('txt', 330, 78, 'drawn acute: not to scale', 'red', 22),
            ('txt', 330, 480, '124 + 22 ✓', 'teal', 24)]),
], vb='95 55 450 440', w=470, title='Quadrilateral ABCD')
_R(f5_pin(f5g57), 200)
video('solve-geo32-g057', 'solution', qid='geo32-g057', slides=[
    S('The angle sum 360°',
      L("The accompanying figure shows quadrilateral A B C D. Given: angle A is one hundred eighteen degrees, and angle B is "
        "ninety-six degrees. Which of the following cannot be the value of alpha?", pt('stem', 'The accompanying figure', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("We know two angles, and the question asks about alpha, the angle at C. The angle at D has no number at all. "
        "[short pause] So we'll use the rule that connects all four angles of a quadrilateral.",
        pt('fig: α', 'the angle at C'), show(f5g57['line'], 'The angle at D has no number')),
      L("[short pause] The angles of every quadrilateral add up to three hundred sixty degrees. Let's call the angle at D "
        "beta. So one hundred eighteen, plus ninety-six, plus alpha, plus beta, is three hundred sixty.",
        show(f5g57['beta'], "Let's call the angle at D"), show(f5g57['sum'], 'So one hundred eighteen, plus')),
      L("One hundred eighteen plus ninety-six is two hundred fourteen. Three hundred sixty minus two hundred fourteen is one "
        "hundred forty-six. So alpha and beta together are one hundred forty-six.",
        show(f5g57['ab'], 'Three hundred sixty minus'), show(f5g57['pair'], 'So alpha and beta together')),
      L("What does that tell us? The two angles share one hundred forty-six between them. They could be seventy-three each. "
        "Or alpha could be one hundred, and beta forty-six. But neither of them can be one hundred forty-six or more. If "
        "alpha were one hundred forty-six, beta would be zero, and an angle of zero degrees isn't a real angle. So alpha "
        "can't be one hundred forty-six, and choice number four is our answer.", show(f5g57['zero'], 'If alpha were'),
        mk('tick', 'choice 4', 'and choice number four is our answer')),
      L("In the exam you'd mark it and move on. But here, let's check the other choices too, because one of them hides a "
        "trap. Alpha twenty-six gives beta one hundred twenty, together one hundred forty-six, so it's possible. Alpha "
        "seventy gives beta seventy-six, also possible.", show(f5g57['c1'], 'Alpha twenty-six gives'),
        mk('cross', 'choice 1', "so it's possible"), mk('cross', 'choice 2', 'also possible')),
      L("Now alpha one hundred twenty-four. Some students say, wait, alpha looks acute in the figure, so it can't be one "
        "hundred twenty-four. But figures on the exam are not drawn to scale. An angle can be drawn acute and still be "
        "obtuse. Alpha one hundred twenty-four gives beta twenty-two, and that's possible too. So only one hundred "
        "forty-six is impossible, choice number four. [pause] Okay. I'll see you in the next question.",
        show(f5g57['c3'], 'figures on the exam are not drawn to scale'), mk('cross', 'choice 3', "and that's possible too"),
        mk('tick', 'choice 4', 'forty-six is impossible'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g058 (Hebrew: the second sample question)
# Hebrew (geo 2410-2460): the perimeter = the sum of the sides; opposite sides equal (CD = AB); AE is part of AD; opposite
# angles equal (D = B); neighbouring angles add to 180 (A, and C either way); ECD = C - BCE, so CE is a bisector; triangle
# EDC: the third angle by the angle sum, or by the Z (ED is parallel to BC); equal angles -> isosceles, ED = CD; then AD,
# BC and the perimeter. English numbers 9, 4, 72, 54 -> 44. The pattern line (a bisector in a parallelogram cuts off an
# isosceles triangle) is kept from the course.
# V3: values written on the copy the moment they are found (CD 9, D 72, C 108 split 54 + 54); triangle EDC tinted; the Z
# traced; ED 9 written; AD = 13 and BC = 13 written; the perimeter under the shape.
f5P, f5Q, f5R, f5S, f5E = (197.95, 69.217), (89.885, 290.783), (442.05, 290.783), (550.115, 69.217), (303.6, 69.217)   # A B C D E
f5q58 = (f5_poly([f5P, f5Q, f5R, f5S]) + [('seg', f5E[0], f5E[1], f5R[0], f5R[1], 'ink', 3)]
         + f5_lab([f5P, f5Q, f5R, f5S, f5E], 'ABCDE', [(-16, -14), (-16, 16), (14, 18), (16, -14), (0, -20)]))
f5g58 = GEO('f5g58', [
    ('line', f5q58 + [('txt', 128, 172, '9', 'ink', 24), ('txt', 251, 50, '4', 'ink', 24), f5_arc(f5Q, f5R, f5P, 34, 'small', '72°', 58),
                      f5_arc(f5R, f5Q, f5E, 34, 'small', '54°', 58)]),
    ('cd9', [('seg', f5R[0], f5R[1], f5S[0], f5S[1], 'teal', 5), ('txt', 520, 190, '9', 'teal', 26)]),
    ('d72', [f5_arc(f5S, f5P, f5R, 34, 'small', '72°', 58)]),
    ('c108', [f5_arc(f5R, f5Q, f5S, 54, 'orange'), ('txt', 520, 318, '108°', 'orange', 26)]),
    ('c54', [f5_arc(f5R, f5E, f5S, 34, 'small', '54°', 58)]),
    ('tri', [('tint', [f5E, f5S, f5R], 'teal')]),
    ('e54', [f5_arc(f5E, f5S, f5R, 30, 'small', '54°', 54)]),
    ('z', [('path', [(f5S[0], f5S[1]), (f5E[0], f5E[1]), (f5R[0], f5R[1]), (f5Q[0], f5Q[1])], 'teal', 7)]),
    ('ed9', [('seg', f5E[0], f5E[1], f5S[0], f5S[1], 'teal', 5), ('txt', 430, 50, '9', 'teal', 26)]),
    ('ad', [('txt', 320, 345, 'AD = BC = 4 + 9 = 13', 'ink', 26)]),
    ('per', [('txt', 320, 385, '9 + 13 + 9 + 13 = 44', 'red', 28)]),
], vb='60 25 530 385', w=500, title='Parallelogram ABCD with the line CE')
_R(f5_pin(f5g58), 200)
video('solve-geo32-g058', 'solution', qid='geo32-g058', slides=[
    S('A bisector in a parallelogram',
      L("A B C D is a parallelogram, and E lies on A D. Given: A B is nine centimeters, A E is four centimeters, angle A B C "
        "is seventy-two degrees, and angle B C E is fifty-four degrees. What is the perimeter of the parallelogram, in "
        "centimeters?", pt('stem', 'A B C D is a parallelogram', 'hl', 11.0), voice='calm', pause=0.5),
      L("The perimeter is the sum of the four sides, A B plus B C plus C D plus A D. We know only one side, A B, and a piece "
        "of A D. [short pause] So we'll find the missing sides one at a time, with the rules of the parallelogram.",
        show(f5g58['line'], 'The perimeter is the sum')),
      L("[short pause] In a parallelogram, opposite sides are parallel and equal. A B is nine, so C D is nine too. B C and A "
        "D are equal to each other, but we don't know them yet. We do know part of A D. A E is four, and that will probably "
        "help.", show(f5g58['cd9'], 'so C D is nine too'), pt('fig: 4', 'A E is four')),
      L("Now the angles. Angle B is seventy-two. Opposite angles in a parallelogram are equal, so angle D is seventy-two too. "
        "Angles next to each other add up to one hundred eighty, so the whole angle C is one hundred eighty minus "
        "seventy-two, which is one hundred eight.", show(f5g58['d72'], 'so angle D is seventy-two'),
        show(f5g58['c108'], 'so the whole angle C')),
      L("Angle B C E is fifty-four, so the rest of angle C, angle E C D, is one hundred eight minus fifty-four, which is "
        "fifty-four too. So C E cuts angle C into two equal halves. It's an angle bisector.",
        show(f5g58['c54'], 'so the rest of angle C')),
      L("Now look at triangle E D C. Two of its angles are known, seventy-two at D and fifty-four at C. The angles of a "
        "triangle add up to one hundred eighty. Seventy-two plus fifty-four is one hundred twenty-six, and one hundred "
        "eighty minus one hundred twenty-six is fifty-four. So angle D E C is fifty-four.",
        show(f5g58['tri'], 'Now look at triangle'), show(f5g58['e54'], 'So angle D E C is fifty-four')),
      L("There's also a shorter way to see it. E D is parallel to B C, so we get a Z, and the angles inside a Z are equal. "
        "So angle D E C equals angle B C E, fifty-four, right away.", show(f5g58['z'], 'so we get a Z')),
      L("In triangle E D C, the angles at E and at C are both fifty-four. Equal angles face equal sides, so the triangle is "
        "isosceles, and E D equals C D, which is nine. Remember this pattern. An angle bisector in a parallelogram cuts off "
        "an isosceles triangle.", show(f5g58['ed9'], 'and E D equals C D')),
      L("Almost done. All of A D is four plus nine, which is thirteen, and B C is thirteen too, because opposite sides are "
        "equal. The perimeter is nine plus thirteen plus nine plus thirteen. Nine and nine is eighteen, thirteen and "
        "thirteen is twenty-six, and together forty-four. Choice number three is our answer. [pause] Okay. I'll see you in "
        "the next question.", show(f5g58['ad'], 'All of A D is four plus nine'), show(f5g58['per'], 'The perimeter is nine'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g059 (Hebrew: the third sample question)
# Hebrew (geo 2462-2537): the diagonals of a rectangle bisect each other and are equal, so EA = EB = EC = ED; the
# perimeter of EBC gives EB + EC, so each half-diagonal and the diagonal AC; the other leg from a triple (here 5, 12, 13
# doubled: 10, 24, 26). Then THREE ways for the area of ABE, "know them all": (1) the median halves triangle ABC (same
# base, same height); (2) the diagonals cut every parallelogram into four triangles of equal area (why: top = bottom,
# left = right, and S1 = S2); (3) base times height, the height from E is half of BC.
# V3: setup - the four half-diagonals ticked equal, triangle EBC traced for its perimeter, 13 written on EB and EC, the
# right triangle ABC tinted with 10, 24, 26. Each method on its own slide with a fresh copy that keeps AB = 10 and
# BC = 24 written on it (same orientation and labels): method 1 the two halves of ABC tinted and the shared dashed height
# from B; method 2 the four triangles tinted in two colours; method 3 the dashed height from E to AB with 12.
f5RA, f5RB, f5RC, f5RD, f5RE = (80.0, 80.0), (80.0, 280.0), (560.0, 280.0), (560.0, 80.0), (320.0, 180.0)
f5q59 = (f5_poly([f5RA, f5RB, f5RC, f5RD]) + [('seg', f5RA[0], f5RA[1], f5RC[0], f5RC[1], 'ink', 3), ('seg', f5RB[0], f5RB[1], f5RD[0], f5RD[1], 'ink', 3)]
         + f5_lab([f5RA, f5RB, f5RC, f5RD], 'ABCD', [(-16, -12), (-16, 16), (16, 16), (16, -12)]) + [('txt', 320, 158, 'E', 'ink', 24, True)])
f5FT = (lambda t: (80 + t * 480 / 520.0, 80 + t * 200 / 520.0))((0 * 480 + 200 * 200) / 520.0)   # the foot of the height from B on AC
f5k59 = [('txt', 320, 304, '24', 'ink', 24), ('txt', 56, 180, '10', 'ink', 24)]
f5g59 = GEO('f5g59', [
    ('line', f5q59 + [('txt', 320, 304, '24', 'ink', 24)]),
    ('eq', [('tick', f5RE[0], f5RE[1], f5RA[0], f5RA[1], 1), ('tick', f5RE[0], f5RE[1], f5RB[0], f5RB[1], 1),
            ('tick', f5RE[0], f5RE[1], f5RC[0], f5RC[1], 1), ('tick', f5RE[0], f5RE[1], f5RD[0], f5RD[1], 1)]),
    ('ebc', [('tint', [f5RE, f5RB, f5RC], 'orange'), ('txt', 320, 345, 'EB + 24 + EC = 50  →  EB + EC = 26', 'orange', 24)]),
    ('h13', [('txt', 182, 250, '13', 'orange', 26), ('txt', 458, 250, '13', 'orange', 26), ('txt', 320, 380, 'EB = EC = 13,  AC = 26', 'orange', 24)]),
    ('abc', [('tint', [f5RA, f5RB, f5RC], 'teal'), ('seg', f5RA[0], f5RA[1], f5RC[0], f5RC[1], 'teal', 5), ('right', 80, 280, 0, 90, 16),
             ('txt', 300, 415, '24, 26: the triple 5, 12, 13 doubled', 'teal', 24)]),
    ('ab10', [('seg', f5RA[0], f5RA[1], f5RB[0], f5RB[1], 'teal', 6), ('txt', 56, 180, '10', 'teal', 26),
              ('txt', 320, 450, 'AB = 10', 'teal', 26)]),
], vb='30 40 580 430', w=500, title='Rectangle ABCD with its diagonals')
f5g59a = GEO('f5g59a', [
    ('line', f5q59 + f5k59),
    ('abc', [('tint', [f5RA, f5RB, f5RE], 'teal'), ('tint', [f5RE, f5RB, f5RC], 'orange'), ('seg', f5RB[0], f5RB[1], f5RE[0], f5RE[1], 'red', 5)]),
    ('h', [('seg', 80, 280, f5FT[0], f5FT[1], 'red', 3, True), ('txt', f5FT[0] - 22, f5FT[1] + 40, 'h', 'red', 26, True),
           ('txt', 320, 345, 'AE = EC, the same height h from B', 'ink', 24)]),
    ('s', [('txt', 320, 385, 'ABC = 10 · 24 / 2 = 120', 'ink', 24), ('txt', 320, 425, 'ABE = 120 / 2 = 60', 'red', 26)]),
], vb='30 40 580 410', w=500, title='The median BE of triangle ABC')
f5g59b = GEO('f5g59b', [
    ('line', f5q59 + f5k59),
    ('four', [('tint', [f5RA, f5RB, f5RE], 'teal'), ('tint', [f5RC, f5RD, f5RE], 'teal'), ('tint', [f5RB, f5RC, f5RE], 'orange'),
              ('tint', [f5RA, f5RD, f5RE], 'orange'), ('txt', 140, 185, 'S₁', 'teal', 26), ('txt', 500, 185, 'S₁', 'teal', 26),
              ('txt', 320, 245, 'S₂', 'orange', 26), ('txt', 320, 118, 'S₂', 'orange', 26)]),
    ('s', [('txt', 320, 345, 'S₁ = S₂: all four are equal', 'ink', 24), ('txt', 320, 385, '10 · 24 = 240,  240 / 4 = 60', 'red', 26)]),
], vb='30 40 580 370', w=500, title='The diagonals cut the rectangle into four triangles')
f5g59c = GEO('f5g59c', [
    ('line', f5q59 + f5k59),
    ('h', [('tint', [f5RA, f5RB, f5RE], 'teal'), ('seg', 320, 180, 80, 180, 'red', 3, True), ('right', 80, 180, 0, 270, 14, 'red'),
           ('txt', 200, 164, '12', 'red', 26)]),
    ('s', [('txt', 320, 345, 'height = 24 / 2 = 12', 'ink', 24), ('txt', 320, 385, 'ABE = 10 · 12 / 2 = 60', 'red', 26)]),
], vb='30 40 580 370', w=500, title='The height from E to AB')
for _g in (f5g59, f5g59a, f5g59b, f5g59c): _R(f5_pin(_g), 200)
video('solve-geo32-g059', 'solution', qid='geo32-g059', slides=[
    S('Half-diagonals',
      L("The diagonals of rectangle A B C D intersect at E. Given: B C is twenty-four centimeters, and the perimeter of "
        "triangle E B C is fifty centimeters. What is the area of triangle A B E, in square centimeters?",
        pt('stem', 'The diagonals of rectangle', 'hl', 10.0), voice='calm', pause=0.5),
      L("We have a rectangle, the perimeter of one triangle, and a question about another triangle. [short pause] First "
        "we'll find the missing lengths, and then we'll see three ways to get the area. It's worth knowing all three.",
        show(f5g59['line'], 'We have a rectangle')),
      L("[short pause] We'll probably need a property of the rectangle's diagonals. In a rectangle, the diagonals cut each "
        "other in half, and they're equal. So all four pieces, A E, E B, E C and E D, are equal.",
        show(f5g59['eq'], 'So all four pieces')),
      L("The perimeter of triangle E B C is E B plus twenty-four plus E C, and that's fifty. So E B and E C together are "
        "twenty-six. They're equal, so each one is thirteen. Then A E and E D are thirteen too, and the whole diagonal A C "
        "is twenty-six.", show(f5g59['ebc'], 'The perimeter of triangle E B C'), show(f5g59['h13'], 'so each one is thirteen')),
      L("Now the right triangle A B C. We know its hypotenuse, twenty-six, and one leg, twenty-four. That's the triple five, "
        "twelve, thirteen, doubled, ten, twenty-four, twenty-six. So A B is ten.", show(f5g59['abc'], 'Now the right triangle'),
        show(f5g59['ab10'], 'So A B is ten'))),
    SM('Method 1 · The median', 'The median',
      L("[pause] Now the area of A B E. The first way uses the median. Look at triangle A B C. E is the middle of A C, so B "
        "E is a median.", show(f5g59a['line'], 'Look at triangle A B C'), show(f5g59a['abc'], 'so B E is a median')),
      L("A median cuts a triangle into two triangles of equal area. Why? A E equals E C, so the two triangles have equal "
        "bases, and they share the same height from B to the line A C.", show(f5g59a['h'], 'they share the same height')),
      L("Triangle A B C is easy. Ten times twenty-four, over two, is one hundred twenty. A B E is half of it, sixty. Choice "
        "number two is our answer.", show(f5g59a['s'], 'Ten times twenty-four'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 2 · Four equal triangles', 'Four equal triangles',
      L("[pause] The second way. The diagonals of a rectangle always cut it into four triangles of equal area. By the way, "
        "that's true in every parallelogram, so also in a rhombus and in a square.", show(f5g59b['line'], 'The second way')),
      L("Why? The top triangle and the bottom triangle are the same triangle, and so are the left one and the right one. And "
        "we just saw that the left one and the bottom one have equal areas. So all four are equal.",
        show(f5g59b['four'], 'The top triangle and the bottom')),
      L("The rectangle is ten times twenty-four, which is two hundred forty. One triangle is a quarter of it, two hundred "
        "forty divided by four, which is sixty. Choice number two again.", show(f5g59b['s'], 'The rectangle is ten times'),
        mk('tick', 'choice 2', 'Choice number two again'))),
    SM('Method 3 · Base times height', 'Base times height',
      L("[pause] And the third way, the most basic one, base times height over two. The base is A B, ten. We need the "
        "height from E to A B.", show(f5g59c['line'], 'the most basic one')),
      L("The height from E to A B is the same as half of B C, because E is exactly in the middle. Half of twenty-four is "
        "twelve. So the area is ten times twelve, over two, which is sixty. Choice number two. [pause] Okay. I'll see you "
        "in the next question.", show(f5g59c['h'], 'The height from E to A B'), show(f5g59c['s'], 'So the area is ten times twelve'),
        mk('tick', 'choice 2', 'which is sixty. Choice number two'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g060 (Hebrew: the fourth sample question)
# Hebrew (geo 2539-2618): two area formulas for a rhombus (side times its height; diagonals multiplied over 2 - any
# quadrilateral with perpendicular diagonals); a diagonal is given, so the diagonal formula first: AC cuts BD into 5 and 5,
# the angle at O is 90, the golden triangle (5 opposite 30 is the short leg, the long leg times root 3), AC = 10 root 3,
# area 50 root 3; "once you've found all the inner pieces" other ways to add it up (the golden triangle x 4, BDA x 2,
# ADC x 2); then the shorter psychometric way: isosceles with 60 -> equilateral, two equilateral triangles. The course's
# link to the 30-30-120 triangle is kept as one short paragraph.
# V3: the rhombus copy is enlarged (the question's rhombus is narrow); AC drawn dashed after its ends are named; the
# halves 5 | 5 written on BD; the right angle at O; the golden triangle ABO tinted and outlined with 30, 60, 5, 5 root 3;
# AC's two halves written; the formula under the shape; the other ways as tints of the parts; method 2: a fresh copy,
# ABD tinted with its 60s and 10s, then BCD in the other tint.
f5HA, f5HB, f5HC, f5HD, f5HO = (320.0, 57.563), (249.311, 180.0), (320.0, 302.437), (390.689, 180.0), (320.0, 180.0)
f5q60 = (f5_poly([f5HA, f5HB, f5HC, f5HD]) + [('seg', f5HB[0], f5HB[1], f5HD[0], f5HD[1], 'ink', 3)]
         + f5_lab([f5HA, f5HB, f5HC, f5HD], 'ABCD', [(0, -18), (-20, 0), (0, 20), (20, 0)], 24))
f5g60 = GEO('f5g60', [
    ('line', f5q60 + [f5_arc(f5HB, f5HD, f5HA, 26, 'small', '60°', 46)]),
    ('ac', [('seg', f5HA[0], f5HA[1], f5HC[0], f5HC[1], 'teal', 3, True), ('txt', 332, 192, 'O', 'ink', 22, True)]),
    ('half', [('txt', 285, 196, '5', 'teal', 22), ('txt', 355, 196, '5', 'teal', 22), ('right', 320, 180, 0, 90, 12)]),
    ('gold', [('tint', [f5HA, f5HB, f5HO], 'orange'), ('seg', f5HA[0], f5HA[1], f5HB[0], f5HB[1], 'orange', 4),
              ('seg', f5HB[0], f5HB[1], f5HO[0], f5HO[1], 'orange', 4), ('seg', f5HO[0], f5HO[1], f5HA[0], f5HA[1], 'orange', 4),
              f5_arc(f5HA, f5HB, f5HO, 30, 'small', '30°', 50)]),
    ('ao', [('txt', 340, 118, '5√3', 'orange', 22), ('txt', 545, 85, 'short leg 5', 'orange', 24),
            ('txt', 545, 118, 'long leg 5√3', 'orange', 24)]),
    ('ac2', [('txt', 340, 245, '5√3', 'orange', 22), ('txt', 545, 165, 'AC = 10√3', 'ink', 24), ('txt', 545, 198, 'BD = 10', 'ink', 24)]),
    ('area', [('txt', 545, 245, '10 · 10√3 / 2', 'red', 26), ('txt', 545, 280, '= 50√3', 'red', 26)]),
], vb='215 25 450 310', w=500, title='Rhombus ABCD with its diagonals')
f5g60o = GEO('f5g60o', [
    ('line', f5q60 + [('seg', f5HA[0], f5HA[1], f5HC[0], f5HC[1], 'ink', 3), ('right', 320, 180, 0, 90, 12),
                      ('txt', 285, 196, '5', 'ink', 22), ('txt', 355, 196, '5', 'ink', 22), ('txt', 340, 118, '5√3', 'ink', 22),
                      ('txt', 340, 245, '5√3', 'ink', 22)]),
    ('t4', [('tint', [f5HA, f5HB, f5HO], 'orange'), ('txt', 545, 90, '4 · (5 · 5√3 / 2)', 'orange', 24)]),
    ('t2', [('tint', [f5HA, f5HB, f5HD], 'teal'), ('txt', 545, 150, '2 · (10 · 5√3 / 2)', 'teal', 24)]),
    ('t3', [('tint', [f5HA, f5HD, f5HC], 'red'), ('txt', 545, 210, '2 · (10√3 · 5 / 2)', 'red', 24)]),
], vb='215 25 450 310', w=500, title='Other ways to add up the area')
f5g60e = GEO('f5g60e', [
    ('line', f5q60 + [f5_arc(f5HB, f5HD, f5HA, 26, 'small', '60°', 46)]),
    ('abd', [('tint', [f5HA, f5HB, f5HD], 'teal'), ('tick', f5HA[0], f5HA[1], f5HB[0], f5HB[1], 1), ('tick', f5HA[0], f5HA[1], f5HD[0], f5HD[1], 1),
             f5_arc(f5HD, f5HB, f5HA, 26, 'small', '60°', 46)]),
    ('top', [f5_arc(f5HA, f5HB, f5HD, 26, 'small', '60°', 46), ('txt', 545, 80, 'top angle 60°', 'teal', 24),
             ('txt', 545, 112, 'all sides 10', 'teal', 24)]),
    ('bcd', [('tint', [f5HB, f5HC, f5HD], 'orange'), ('tick', f5HB[0], f5HB[1], f5HC[0], f5HC[1], 1), ('tick', f5HC[0], f5HC[1], f5HD[0], f5HD[1], 1),
             ('txt', 545, 160, 'two equilateral', 'orange', 24), ('txt', 545, 190, 'triangles', 'orange', 24)]),
    ('area', [('txt', 545, 235, '2 · 10²√3 / 4', 'red', 26), ('txt', 545, 268, '= 50√3', 'red', 26)]),
    ('link', [('txt', 545, 305, 'B = 120°: AC = 10√3', 'ink', 22)]),
], vb='215 25 450 310', w=500, title='Two equilateral triangles')
for _g in (f5g60, f5g60o, f5g60e): _R(f5_pin(_g), 200)
video('solve-geo32-g060', 'solution', qid='geo32-g060', slides=[
    SM('Method 1 · The diagonals', 'The diagonals',
      L("A B C D is a rhombus. Given: B D is ten centimeters, and angle A B D is sixty degrees. What is the area of the "
        "rhombus, in square centimeters?", pt('stem', 'A B C D is a rhombus', 'hl', 7.0), voice='calm', pause=0.5),
      L("We learned two formulas for the area of a rhombus. A rhombus is a parallelogram with all its sides equal, so one "
        "formula is side times the height to that side. The other is the two diagonals multiplied, over two. That one "
        "works for any quadrilateral whose diagonals are perpendicular. [short pause] A diagonal is given here, so we'll "
        "start with the diagonal formula.", show(f5g60['line'], 'We learned two formulas')),
      L("[short pause] In a rhombus, the diagonals cut each other in half. So let's draw the other diagonal, from A to C. "
        "It cuts B D into five and five.", show(f5g60['ac'], 'from A to C'), show(f5g60['half'], 'It cuts B D into five and five')),
      L("The diagonals of a rhombus are also perpendicular, so the angle at O is ninety. That makes a special triangle, A B "
        "O. It's a right triangle with a sixty-degree angle, so it's a golden triangle, thirty, sixty, ninety.",
        show(f5g60['gold'], 'That makes a special triangle')),
      L("In a golden triangle the sides have a fixed ratio. Five is across from the thirty-degree angle, so it's the short "
        "leg. To get the long leg, we multiply by root three. So A O is five root three.", show(f5g60['ao'], 'So A O is five root three')),
      L("The diagonals cut each other in half, so the bottom part, O C, is five root three too. The whole diagonal A C is "
        "five root three plus five root three, which is ten root three.", show(f5g60['ac2'], 'so the bottom part')),
      L("Now the formula. The diagonals multiplied, over two, is ten times ten root three, over two. Ten over two is five, "
        "and five times ten root three is fifty root three. Choice number two is our answer.",
        show(f5g60['area'], 'Now the formula'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
    SM('Method 1 · The diagonals', 'The diagonals',
      L("[pause] Once you've found all the inner pieces, you can add up the area in other ways too. Some students take the "
        "golden triangle, base five and height five root three, and multiply its area by four.",
        show(f5g60o['line'], 'Once you\'ve found all the inner pieces'), show(f5g60o['t4'], 'Some students take the golden triangle')),
      L("Some take the top triangle, B D A, with base ten and height five root three, twice. And some take the triangle on "
        "the right, A D C, with base ten root three and height five, twice too. There are many ways, and at this stage it's "
        "good to know them all.", show(f5g60o['t2'], 'Some take the top triangle'), show(f5g60o['t3'], 'And some take the triangle on'))),
    SM('Method 2 · Two equilateral triangles', 'Two equilateral triangles',
      L("[pause] And one more way. Well done if you saw this one. Some students notice the sixty degrees and say, wait, "
        "that's a hint.", show(f5g60e['line'], 'notice the sixty degrees')),
      L("In a rhombus all the sides are equal, so A B equals A D. That makes triangle A B D isosceles, and angle A D B is "
        "sixty too.", show(f5g60e['abd'], 'so A B equals A D')),
      L("Sixty plus sixty is one hundred twenty, so the top angle is sixty as well. The triangle is equilateral. It's worth "
        "remembering that an isosceles triangle with a sixty-degree angle is always equilateral. B D is ten, so A B and A D "
        "are ten.", show(f5g60e['top'], 'so the top angle is sixty as well')),
      L("All the sides of a rhombus are equal, so D C and B C are ten too. So the rhombus is two equilateral triangles.",
        show(f5g60e['bcd'], 'so D C and B C are ten too')),
      L("The area of one equilateral triangle is the side squared, times root three, over four. Twice that is two times one "
        "hundred root three, over four, which is fifty root three. That's the shorter way. Choice number two.",
        show(f5g60e['area'], 'Twice that is two times'), mk('tick', 'choice 2', "That's the shorter way. Choice number two")),
      L("And one more link to the triangles topic. Angle A B C is sixty plus sixty, one hundred twenty. So triangle A B C is "
        "the thirty, thirty, one hundred twenty triangle with sides ten and ten, and its long side, A C, is ten root three "
        "straight away. [pause] Okay. I'll see you in the next question.", show(f5g60e['link'], 'Angle A B C is sixty plus sixty'))),
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
