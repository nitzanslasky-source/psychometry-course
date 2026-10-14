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
# Topic-32 fragment f6 (2026-10-14): geo32-g061, g062, g063 (the end of the Hebrew "quadrilaterals basics" sample
# questions, geo 2636-2789), geo-065 (the advanced lesson's opening, geo 2794-2799), geo32-g066 and g067 (the first two
# advanced sample questions, geo 2801-2950). Question figure on the left (FIG_LEFT), our colour copy built in layers on
# the right (Rule V3); the typed working is written inside the copy (text layers), so the layers stay consecutive.
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g061', 'solve-geo32-g062', 'solve-geo32-g063', 'solve-geo32-g067'})


def f6_poly(pts, col='ink', w=3):
    """the sides of a closed polygon as segments"""
    return [('seg', pts[k][0], pts[k][1], pts[(k + 1) % len(pts)][0], pts[(k + 1) % len(pts)][1], col, w) for k in range(len(pts))]


def f6_name(p, t, dx, dy):
    return ('txt', p[0] + dx, p[1] + dy, t, 'ink', 26, True)


def f6_seg(p, q, col='ink', w=3, dash=False):
    return ('seg', p[0], p[1], q[0], q[1], col, w, dash)


# ------------------------------------------------------------------------------------------------ geo32-g061 (Hebrew: the square and the equilateral triangle)
# Hebrew (geo 2636-2693): start from the square; choose which of its many properties matter (no diagonals here); mark all
# the sides with one tick, mark the right angles next to the angle we want; the equilateral triangle: its sides get the
# same tick - "the catch", the triangle's sides equal the square's; all its angles 60; look at the triangle that holds
# the angle: isosceles ("if we hadn't marked the sides we might not see it"); equal sides -> equal angles alpha; the top
# angle 90 - 60 = 30; 30 + 2 alpha = 180, alpha = 75. English asks one step more: angle PAD = 90 - 75 = 15 (75 is the trap).
# V3: the copy built at the words; ticks and squares as each given is marked; the studied triangle ABP tinted and held;
# the values written on the figure when found; the working typed beside the figure.
f6B1, f6A1, f6D1, f6C1, f6P1 = (210.5, 70.5), (210.5, 289.5), (429.5, 289.5), (429.5, 70.5), (320.0, 260.16)
f6g61 = GEO('f6g61', [
    ('line', f6_poly([f6B1, f6A1, f6D1, f6C1]) + [f6_seg(f6B1, f6P1), f6_seg(f6C1, f6P1), f6_seg(f6A1, f6P1),
              f6_name(f6B1, 'B', -18, -14), f6_name(f6A1, 'A', -18, 16), f6_name(f6D1, 'D', 18, 16), f6_name(f6C1, 'C', 18, -14),
              f6_name(f6P1, 'P', 4, -26), ('arc', f6A1[0], f6A1[1], 52, 0, 15, 'red', 'x', 76)]),
    ('sq', [('tick', *f6B1, *f6A1), ('tick', *f6A1, *f6D1), ('tick', *f6D1, *f6C1), ('tick', *f6C1, *f6B1)]),
    ('r90', [('right', f6B1[0], f6B1[1], 270, 0, 16), ('right', f6A1[0], f6A1[1], 0, 90, 16)]),
    ('eqs', [('tick', *f6B1, *f6P1), ('tick', *f6C1, *f6P1)]),
    ('e60', [('arc', f6B1[0], f6B1[1], 44, 300, 360, 'small', '60°', 66), ('arc', f6C1[0], f6C1[1], 30, 180, 240, 'small', '60°', 52),
             ('arc', f6P1[0], f6P1[1], 24, 60, 120, 'small', '60°', 44)]),
    ('abp', [('tint', [f6A1, f6B1, f6P1], 'teal'), ('path', [f6A1, f6B1, f6P1, f6A1], 'teal', 6)]),
    ('alpha', [('arc', f6A1[0], f6A1[1], 32, 15, 90, 'small', 'α', 52), ('arc', f6P1[0], f6P1[1], 34, 120, 195, 'small', 'α', 54)]),
    ('b30', [('arc', f6B1[0], f6B1[1], 30, 270, 300, 'orange', '30°', 52), ('txt', 600, 110, '∠ABP = 90° − 60° = 30°', 'ink', 22)]),
    ('t2', [('txt', 600, 160, '30° + α + α = 180°', 'ink', 22)]),
    ('t3', [('txt', 600, 210, '2α = 150°,  α = 75°', 'teal', 22), ('txt', 262, 238, '75°', 'teal', 20)]),
    ('t4', [('txt', 600, 270, '∠PAD = 90° − 75° = 15°', 'red', 23), ('txt', 300, 306, 'x = 15°', 'red', 22)]),
], vb='170 30 560 300', w=540, title='Square ABCD with the equilateral triangle BPC')
_R(f6g61, 205)
video('solve-geo32-g061', 'solution', qid='geo32-g061', slides=[
    SM('Mark the givens', 'Mark the givens',
      L("A B C D is a square, and P is a point inside it, so that triangle B P C is equilateral. What is angle P A D?",
        pt('stem', 'A B C D is a square', 'hl', 7.0), voice='calm', pause=0.5),
      L("We need angle P A D, the small angle at A, between A P and the side A D. [short pause] We'll mark what each given "
        "tells us on the figure, and then use the triangle that holds the angle at A.", pt('fig: x', 'We need angle P A D')),
      L("[short pause] Where do we start? With the square. A square has lots of properties. All its sides are equal, and "
        "all its angles are ninety. Its diagonals are equal, they cut each other in half, they're perpendicular, and they "
        "cut the angles in half. We need to decide which of these matter here.", show(f6g61['line'], 'Where do we start')),
      L("There are no diagonals in this figure. P is inside the square, but it's not the point where the diagonals meet. "
        "So we probably won't need the diagonal properties."),
      L("What we will need is this. All the sides are equal, so let's mark all four with the same little line. And all the "
        "angles are ninety. I'll mark the two that sit next to the angle we want, at B and at A. We may need them.",
        show(f6g61['sq'], 'mark all four with the same little line'), show(f6g61['r90'], "I'll mark the two")),
      L("Done with the square. The next given, B P C is equilateral. In an equilateral triangle all three sides are "
        "equal, B C, P C and B P. B C already has the mark, so P C and B P get the same mark. That's the catch in this "
        "question. The sides of the triangle are equal to the sides of the square. And all the angles of the triangle are "
        "sixty.", show(f6g61['eqs'], 'get the same mark'), show(f6g61['e60'], 'And all the angles of the triangle')),
      L("Now look at the triangle that holds the angle at A, triangle A B P. Two of its sides have the mark, B A and B P. "
        "So it's isosceles. If we hadn't marked the sides, we might not have noticed that.",
        show(f6g61['abp'], 'Now look at the triangle that holds')),
      L("In an isosceles triangle, the angles across from the equal sides are equal. So angle B A P and angle B P A are "
        "equal. Let's call both of them alpha.", show(f6g61['alpha'], 'call both of them alpha')),
      L("The angle at B, the top of this triangle, is ninety minus sixty, which is thirty.",
        show(f6g61['b30'], 'is ninety minus sixty')),
      L("The angles of a triangle add up to one hundred eighty. So thirty plus alpha plus alpha is one hundred eighty. "
        "Move the thirty across. One hundred eighty minus thirty is one hundred fifty, and that's two alpha. So one alpha "
        "is seventy-five.", show(f6g61['t2'], 'So thirty plus alpha'), show(f6g61['t3'], 'So one alpha')),
      L("Careful. Seventy-five is angle B A P, and seventy-five is choice number four. But the question asks for angle P A "
        "D. Angle B A P and angle P A D together fill the square's corner at A, which is ninety. So angle P A D is ninety "
        "minus seventy-five, which is fifteen. Choice number one is our answer. [pause] Okay. I'll see you in the next "
        "question.", mk('cross', 'choice 4', 'seventy-five is choice number four'), show(f6g61['t4'], 'So angle P A D is ninety'),
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g062 (Hebrew: the deltoid's area)
# Hebrew (geo 2695-2743): the area formula (product of the diagonals over 2); what's given is a part of each diagonal;
# a deltoid = two isosceles triangles; in an isosceles triangle the height is also a median and a bisector, so the main
# diagonal is perpendicular to the other one and cuts it in half (BO = OD; not AO = OC); triangle ADO is right-angled ->
# a Pythagorean triple; the area, cancel first; other ways: the two isosceles triangles, or four right triangles.
# English numbers: 17, 15, 12 -> AO = 8 (8, 15, 17; Pythagoras with a difference of squares for who doesn't know the
# triple - topic 4 comes earlier in the study plan), area 300.
# V3: the two isosceles triangles tinted in turn with their ticks; the right angle at O; OD written; then a new slide
# with the right triangle AOD tinted inside the copy, the rest dimmed and AOD enlarged with the same labels and tint;
# AO written on both; the area written. Other ways: the two halves tinted with their areas.
f6A2, f6B2, f6C2, f6D2, f6O2 = (320.0, 47.27), (160.73, 113.64), (320.0, 312.73), (479.27, 113.64), (320.0, 113.64)
f6g62base = (f6_poly([f6A2, f6B2, f6C2, f6D2]) + [f6_seg(f6A2, f6C2), f6_seg(f6B2, f6D2),
             f6_name(f6A2, 'A', 0, -20), f6_name(f6B2, 'B', -20, 0), f6_name(f6C2, 'C', 0, 22), f6_name(f6D2, 'D', 20, 0),
             f6_name(f6O2, 'O', 16, -16), ('txt', 411, 66, '17', 'ink', 22), ('txt', 240, 134, '15', 'ink', 22), ('txt', 300, 213, '12', 'ink', 22)])
f6g62 = GEO('f6g62', [
    ('line', f6g62base + [('txt', 640, 70, 'S = AC · BD ÷ 2', 'ink', 24)]),
    ('need', [('seg', f6A2[0], f6A2[1], f6O2[0], f6O2[1], 'red', 6), ('txt', 300, 80, '?', 'red', 26),
              ('seg', f6O2[0], f6O2[1], f6D2[0], f6D2[1], 'red', 6), ('txt', 400, 134, '?', 'red', 26)]),
    ('abd', [('tint', [f6A2, f6B2, f6D2], 'teal'), ('tick', *f6A2, *f6B2, 1), ('tick', *f6A2, *f6D2, 1)]),
    ('dcb', [('tint', [f6D2, f6C2, f6B2], 'orange'), ('tick', *f6B2, *f6C2, 2, 'orange'), ('tick', *f6D2, *f6C2, 2, 'orange')]),
    ('perp', [('right', f6O2[0], f6O2[1], 0, 270, 14), ('txt', 640, 140, 'AC ⊥ BD', 'teal', 24)]),
    ('od', [('tick', *f6B2, *f6O2, 1, 'red'), ('tick', *f6O2, *f6D2, 1, 'red'), ('txt', 400, 134, '15', 'teal', 22),
            ('txt', 640, 190, 'BO = OD = 15', 'teal', 24)]),
    ('warn', [('txt', 640, 240, 'but AO ≠ OC', 'red', 24)]),
], vb='120 15 660 320', w=540, title='Deltoid ABCD with its diagonals')
f6Z = 1.7
def f6zz(p): return (520 + (p[0] - 320) * f6Z, 110 + (p[1] - 47.27) * f6Z)
f6zA, f6zO, f6zD = f6zz(f6A2), f6zz(f6O2), f6zz(f6D2)
f6g62b = GEO('f6g62b', [
    ('line', f6g62base + [('right', f6O2[0], f6O2[1], 0, 270, 14), ('txt', 400, 134, '15', 'teal', 22),
                          ('tint', [f6A2, f6O2, f6D2], 'teal'), ('path', [f6A2, f6O2, f6D2, f6A2], 'teal', 6)]),
    ('cut', [('dim', 120, 15, 380, 320), ('path', [f6A2, f6O2, f6D2, f6A2], 'teal', 6),
             ('tint', [f6zA, f6zO, f6zD], 'teal'), ('path', [f6zA, f6zO, f6zD, f6zA], 'teal', 6), ('right', f6zO[0], f6zO[1], 0, 270, 18),
             f6_name(f6zA, 'A', -18, -12), f6_name(f6zO, 'O', -20, 18), f6_name(f6zD, 'D', 20, 14),
             ('txt', (f6zO[0] + f6zD[0]) / 2, f6zO[1] + 26, '15', 'ink', 24), ('txt', (f6zA[0] + f6zD[0]) / 2 + 18, (f6zA[1] + f6zD[1]) / 2 - 18, '17', 'ink', 24)]),
    ('ao', [('txt', f6zA[0] - 22, (f6zA[1] + f6zO[1]) / 2, '8', 'red', 28), ('txt', 304, 80, '8', 'red', 24)]),
    ('ac', [('txt', 640, 270, 'AC = 8 + 12 = 20', 'ink', 24)]),
    ('bd', [('txt', 640, 300, 'BD = 15 + 15 = 30', 'ink', 24)]),
    ('s', [('txt', 640, 330, 'S = 20 · 30 ÷ 2 = 20 · 15 = 300', 'red', 24)]),
], vb='120 15 660 330', w=540, title='The right triangle AOD, enlarged')
f6g62c = GEO('f6g62c', [
    ('line', f6g62base + [('right', f6O2[0], f6O2[1], 0, 270, 14), ('txt', 400, 134, '15', 'ink', 22), ('txt', 304, 80, '8', 'ink', 22)]),
    ('two', [('tint', [f6A2, f6B2, f6D2], 'teal'), ('tint', [f6D2, f6C2, f6B2], 'orange'),
             ('txt', 640, 90, '30 · 8 ÷ 2 = 120', 'teal', 24), ('txt', 640, 135, '30 · 12 ÷ 2 = 180', 'orange', 24),
             ('txt', 640, 180, '120 + 180 = 300', 'ink', 24)]),
    ('four', [('seg', f6A2[0], f6A2[1], f6C2[0], f6C2[1], 'red', 4), ('seg', f6B2[0], f6B2[1], f6D2[0], f6D2[1], 'red', 4),
              ('txt', 640, 240, '2 · 15·8÷2 + 2 · 15·12÷2', 'red', 22), ('txt', 640, 270, '= 120 + 180 = 300', 'red', 22)]),
], vb='120 15 660 320', w=540, title='Other ways to the same area')
for _g in (f6g62, f6g62b, f6g62c): _R(_g, 205)
# (V2: the redrawn copy on slide 2 carries the found values - 15 on OD and the right angle - so no separate box)
video('solve-geo32-g062', 'solution', qid='geo32-g062', slides=[
    SM('The main diagonal', 'The main diagonal',
      L("A B C D is a deltoid, and its diagonals meet at O. Given: A B and A D are seventeen centimeters, C B equals C D, "
        "B O is fifteen centimeters, and O C is twelve centimeters. What is the area of the deltoid, in square centimeters?",
        pt('stem', 'A B C D is a deltoid', 'hl', 11.0), voice='calm', pause=0.5),
      L("We learned how to find the area of a deltoid. The product of the diagonals, over two. [short pause] But only "
        "parts of the diagonals are given, so first we'll find the missing parts.", show(f6g62['line'], 'The product of the diagonals')),
      L("[short pause] On the long diagonal A C we know O C, twelve, and we need A O. On the short diagonal B D we know B "
        "O, fifteen, and we need O D.", show(f6g62['need'], 'we need A O')),
      L("Let's remember what a deltoid is. It's a quadrilateral made of two isosceles triangles. Triangle A B D is "
        "isosceles, because A D equals A B. And triangle D C B is isosceles too, because C B equals C D.",
        show(f6g62['abd'], 'Triangle A B D is'), show(f6g62['dcb'], 'And triangle D C B')),
      L("In an isosceles triangle, the height from the top is also a median and an angle bisector. So the main diagonal A "
        "C is perpendicular to the other diagonal, B D. It cuts the angles in half, and it cuts B D in half. So B O equals "
        "O D. B O is fifteen, so O D is fifteen too.", show(f6g62['perp'], 'is perpendicular to the other diagonal'),
        show(f6g62['od'], 'So B O equals')),
      L("But careful, not the other way around. In a deltoid, A O is not equal to O C. We still have to find A O.",
        show(f6g62['warn'], 'A O is not equal to O C'))),
    SM('The main diagonal', 'The main diagonal',
      L("The diagonals are perpendicular, so triangle A O D is a right triangle. Its hypotenuse A D is seventeen, and its "
        "leg O D is fifteen. Let's look at it on its own.", show(f6g62b['line'], 'triangle A O D is a right triangle'),
        show(f6g62b['cut'], "Let's look at it on its own")),
      L("If you know the triple eight, fifteen, seventeen, you see it at once. The other leg is eight. If not, use "
        "Pythagoras. A O squared is seventeen squared minus fifteen squared. That's a difference of squares, so it's "
        "seventeen minus fifteen, times seventeen plus fifteen. Two times thirty-two is sixty-four, and the root of "
        "sixty-four is eight. So A O is eight.", show(f6g62b['ao'], 'So A O is eight')),
      L("Now we have everything. A C is eight plus twelve, which is twenty. B D is fifteen plus fifteen, which is thirty.",
        show(f6g62b['ac'], 'A C is eight plus twelve'), show(f6g62b['bd'], 'B D is fifteen plus fifteen')),
      L("The area is twenty times thirty, over two. We could multiply first, but it's easier to cancel first. Thirty over "
        "two is fifteen, and twenty times fifteen is three hundred. Choice number three is our answer.",
        show(f6g62b['s'], 'The area is twenty times thirty'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Other ways', 'Other ways',
      L("[pause] Once we've found all the pieces, there are other ways to get the area. Some students take the two "
        "isosceles triangles. Triangle A B D has base thirty and height eight, so it's one hundred twenty. Triangle C B D "
        "has base thirty and height twelve, so it's one hundred eighty. Together, three hundred.",
        show(f6g62c['line'], 'there are other ways'), show(f6g62c['two'], 'Some students take the two')),
      L("Others take four right triangles. Two small ones, fifteen by eight over two, and two big ones, fifteen by twelve "
        "over two. Again three hundred. Choice number three. [pause] Okay. I'll see you in the next question.",
        show(f6g62c['four'], 'Others take four right triangles'), mk('tick', 'choice 3', 'Again three hundred'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g063 (Hebrew: the isosceles trapezoid)
# Hebrew (geo 2745-2789): AB = AD -> isosceles triangle ABD, the base angles 30 and 30, A = 120; in every trapezoid the
# angles on one leg add up to 180 -> B = 60, its lower part DBC = 30 (or: our familiar Z, the bases are parallel); the
# trapezoid is isosceles -> C = B = 60; triangle BCD is 30-60-90, a gold triangle; the short leg (opposite the 30) is CD
# = AB; the hypotenuse is twice it; the perimeter. English numbers 7 -> BC = 14, P = 35. The course's bonus (ABD is the
# 30-30-120 triangle, BD = 7 root 3, matching the long leg) is kept short.
# V3: the copy built at the words; ABD tinted with its ticks and both 30s; 120 written at A; 60 at B; the Z traced for the
# second way; 60 at C; then BCD tinted orange with its right angle, CD ticked like AB, BC written when found.
f6A3, f6B3, f6C3, f6D3 = (204.68, 80.13), (89.36, 279.87), (550.64, 279.87), (435.32, 80.13)
f6g63 = GEO('f6g63', [
    ('line', f6_poly([f6A3, f6B3, f6C3, f6D3]) + [f6_seg(f6B3, f6D3),
              f6_name(f6A3, 'A', -14, -18), f6_name(f6B3, 'B', -16, 16), f6_name(f6C3, 'C', 16, 16), f6_name(f6D3, 'D', 14, -18),
              ('txt', 130, 170, '7', 'ink', 24), ('txt', 320, 62, '7', 'ink', 24), ('arc', f6B3[0], f6B3[1], 52, 30, 60, 'small', '30°', 80)]),
    ('abd', [('tint', [f6A3, f6B3, f6D3], 'teal'), ('tick', *f6A3, *f6B3, 1), ('tick', *f6A3, *f6D3, 1),
             ('arc', f6D3[0], f6D3[1], 52, 180, 210, 'small', '30°', 80)]),
    ('a120', [('arc', f6A3[0], f6A3[1], 28, 240, 360, 'orange', '120°', 50), ('txt', 340, 340, '∠A = 180° − 30° − 30° = 120°', 'ink', 22)]),
    ('b60', [('arc', f6B3[0], f6B3[1], 34, 0, 30, 'small', '30°', 56), ('txt', 340, 368, '∠B = 180° − 120° = 60°', 'ink', 22)]),
    ('z', [('path', [(330, 80.13), f6D3, f6B3, (200, 279.87)], 'teal', 7)]),
    ('c60', [('arc', f6C3[0], f6C3[1], 32, 120, 180, 'small', '60°', 56)]),
    ('bcd', [('tint', [f6B3, f6C3, f6D3], 'orange'), ('right', f6D3[0], f6D3[1], 210, 300, 16)]),
    ('cd', [('tick', *f6C3, *f6D3, 1), ('txt', 512, 170, '7', 'teal', 24)]),
    ('bc', [('txt', 320, 304, '14', 'red', 26), ('txt', 340, 396, 'BC = 2 · 7 = 14', 'red', 22)]),
    ('p', [('txt', 340, 426, 'P = 7 + 7 + 7 + 14 = 35', 'red', 24)]),
    ('bonus', [('txt', 300, 196, '7√3', 'teal', 22), ('txt', 340, 456, 'BD = 7√3 (30°-30°-120°)', 'teal', 20)]),
], vb='60 30 560 445', w=540, title='Isosceles trapezoid ABCD with the diagonal BD')
_R(f6g63, 200)
video('solve-geo32-g063', 'solution', qid='geo32-g063', slides=[
    SM('Angles, then the gold triangle', 'Angles, then the gold triangle',
      L("A B C D is an isosceles trapezoid, with A D parallel to B C. Given: A B and A D are seven centimeters, and angle A "
        "B D is thirty degrees. What is its perimeter, in centimeters?", pt('stem', 'A B C D is an isosceles trapezoid', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("The perimeter is the sum of the four sides. Three of them are given, A B, A D, and C D, which equals A B because the "
        "trapezoid is isosceles. [short pause] We need the fourth side, B C.", show(f6g63['line'], 'The perimeter is the sum')),
      L("[short pause] Start with the first given. A B equals A D, so triangle A B D is isosceles. In an isosceles triangle "
        "the base angles are equal. Angle A B D is thirty, so angle A D B is thirty too.", show(f6g63['abd'], 'so triangle A B D is isosceles')),
      L("Thirty and thirty. So the top angle, A, is one hundred eighty minus sixty, which is one hundred twenty.",
        show(f6g63['a120'], 'So the top angle')),
      L("In every trapezoid, the two angles on the same leg add up to one hundred eighty. A is one hundred twenty, so all "
        "of angle B is sixty. Its lower part, angle D B C, is sixty minus thirty, which is thirty.", show(f6g63['b60'], 'so all of angle B is sixty')),
      L("Another way to see the thirty is our familiar Z. The bases are parallel, so the two angles in the corners of the "
        "Z are equal. Thirty and thirty.", show(f6g63['z'], 'our familiar Z')),
      L("The trapezoid is isosceles, so the two angles on the bottom base are equal. Angle C equals angle B, sixty. You can "
        "also see it because angle C completes angle A to one hundred eighty.", show(f6g63['c60'], 'Angle C equals angle B')),
      L("What did we get? Triangle B C D has thirty and sixty, together ninety. So the angle at D completes it to one "
        "hundred eighty, and it's ninety. It's not just a right triangle. It's a gold triangle, thirty, sixty, ninety.",
        show(f6g63['bcd'], 'Triangle B C D has thirty and sixty')),
      L("Its short leg is the one across from the thirty, C D. The trapezoid is isosceles, so C D equals A B, seven.",
        show(f6g63['cd'], 'so C D equals A B')),
      L("When we know the short leg, the hypotenuse is easy. It's exactly twice the short leg. So B C is fourteen.",
        show(f6g63['bc'], 'So B C is fourteen')),
      L("The perimeter is seven plus seven plus seven plus fourteen, which is thirty-five. Choice number two is our "
        "answer.", show(f6g63['p'], 'The perimeter is seven plus'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("One more link. Triangle A B D has angles thirty, thirty and one hundred twenty, the triangle we met with the "
        "special triangles. So B D is seven root three. That matches the gold triangle, where the long leg is the short "
        "leg times root three. [pause] Okay. I'll see you in the next question.", show(f6g63['bonus'], 'So B D is seven root three'))),
])

# ------------------------------------------------------------------------------------------------ geo-065 (lesson: the advanced level)
# Hebrew (geo 2794-2799): the last lesson learned the rules and basic questions; now harder psychometric questions and
# nuances that come back now and then; start with a sample question. The course's "what's ahead" lines are kept, each
# taught in the questions that follow.
f6h1 = I('f6h1', 'Which shape is also which? $\\ $Read the definitions', size=32)
f6h2 = I('f6h2', 'Areas: symmetry and equal heights, $\\ $a long way and a short way', size=32)
f6h3 = I('f6h3', 'Angles with letters: $\\ $plug in numbers', size=32)
video('geo-065', 'lesson', slides=[
    S('Advanced Quadrilaterals',
      L("Quadrilaterals, the advanced level. In the last lesson we learned the rules of the quadrilaterals and practiced "
        "basic questions.")),
    S("What's ahead",
      L("In this lesson we'll practice harder exam questions, and meet a few small points that come back on the exam "
        "every now and then."),
      L("There are questions about which shape is also which, and they're solved by reading the definitions carefully.",
        show(f6h1, 'which shape is also which')),
      L("There are area questions that a long calculation solves, and that a short idea, like symmetry or an equal height, "
        "solves in a few seconds.", show(f6h2, 'There are area questions')),
      L("And there are angle questions full of letters, where plugging in numbers helps. For most questions we'll see two "
        "ways, the full math way and the short way. Let's start with a sample question. [pause] Okay. I'll see you in the "
        "next video.", show(f6h3, 'And there are angle questions'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g066 (Hebrew: which statement is not necessarily true)
# Hebrew (geo 2801-2861): statement by statement, eliminate whatever is surely true, hope to be left with one; "every X is
# a Y" = X has all the properties of Y (not the other way round); rectangle -> parallelogram, rhombus -> deltoid (two
# isosceles triangles on the short diagonal; a deltoid with equal sides IS a rhombus), square -> rectangle (an upgraded
# rectangle); three eliminated -> on the exam mark the fourth without checking; in the lesson we check it. English order
# and the last statement differ (perpendicular diagonals: a rhombus property; a 9 by 4 rectangle as the counterexample).
# V3 (general properties on clean generic shapes): one panel per statement, built as it is discussed; the shared property
# in the same tint on both shapes; the counterexample's diagonals with their angle in red.
def f6P(x, y, pts): return [(x + a, y + b) for a, b in pts]
f6rh = f6P(30, 30, [(110, 0), (40, 70), (110, 140), (180, 70)])          # rhombus (diagonal BD horizontal)
f6ki = f6P(250, 30, [(80, 0), (20, 50), (80, 160), (140, 50)])            # deltoid
f6sq = f6P(40, 230, [(0, 0), (0, 120), (120, 120), (120, 0)])             # square
f6re = f6P(230, 230, [(0, 0), (0, 120), (190, 120), (190, 0)])            # rectangle
f6re2 = f6P(460, 230, [(0, 0), (0, 120), (190, 120), (190, 0)])           # rectangle (statement 3)
f6pa = f6P(470, 30, [(40, 0), (0, 120), (160, 120), (200, 0)])            # parallelogram
f6r9 = f6P(720, 120, [(0, 0), (0, 120), (270, 120), (270, 0)])            # the 9 by 4 rectangle
f6g66 = GEO('f6g66', [
    ('line', [('txt', 300, 14, ' ', 'ink', 10)]),
    ('p1', f6_poly(f6rh) + [f6_seg(f6rh[1], f6rh[3], 'teal', 3, True), ('tint', [f6rh[0], f6rh[1], f6rh[3]], 'teal'),
                            ('tint', [f6rh[2], f6rh[1], f6rh[3]], 'orange')] + [('tick', *f6rh[k], *f6rh[(k + 1) % 4]) for k in range(4)]
           + [('txt', 140, 196, 'rhombus', 'ink', 22)]),
    ('p1k', f6_poly(f6ki) + [f6_seg(f6ki[1], f6ki[3], 'teal', 3, True), ('tint', [f6ki[0], f6ki[1], f6ki[3]], 'teal'),
                             ('tint', [f6ki[2], f6ki[1], f6ki[3]], 'orange'), ('txt', 330, 214, 'deltoid', 'ink', 22)]),
    ('p2', f6_poly(f6sq) + [('right', *f6sq[k], a1, a2, 14) for k, (a1, a2) in enumerate([(270, 0), (0, 90), (90, 180), (180, 270)])]
           + [('tick', *f6sq[k], *f6sq[(k + 1) % 4]) for k in range(4)] + [('txt', 100, 380, 'square', 'ink', 22)]),
    ('p2r', f6_poly(f6re) + [('right', *f6re[k], a1, a2, 14) for k, (a1, a2) in enumerate([(270, 0), (0, 90), (90, 180), (180, 270)])]
            + [('txt', 325, 380, 'rectangle', 'ink', 22)]),
    ('p3', f6_poly(f6pa) + [('par', *f6pa[1], *f6pa[2], 1), ('par', *f6pa[0], *f6pa[3], 1), ('par', *f6pa[0], *f6pa[1], 2), ('par', *f6pa[3], *f6pa[2], 2),
                            ('txt', 570, 180, 'parallelogram', 'ink', 22)]
           + f6_poly(f6re2) + [('par', *f6re2[1], *f6re2[2], 1), ('par', *f6re2[0], *f6re2[3], 1), ('par', *f6re2[0], *f6re2[1], 2),
                               ('par', *f6re2[3], *f6re2[2], 2), ('txt', 555, 380, 'rectangle', 'ink', 22)]),
    ('p4', f6_poly(f6r9) + [f6_seg(f6r9[0], f6r9[2], 'red', 3), f6_seg(f6r9[1], f6r9[3], 'red', 3),
                            ('txt', 855, 262, '9', 'ink', 24), ('txt', 702, 180, '4', 'ink', 24), ('txt', 855, 100, 'not 90°', 'red', 24)]),
], vb='0 0 1010 400', w=540, title='Quadrilateral families')
_R(f6g66, 215)
video('solve-geo32-g066', 'solution', qid='geo32-g066', slides=[
    SM('Statement by statement', 'Statement by statement',
      L("Which of the following statements is not necessarily true?", pt('stem', 'Which of the following', 'hl', 4.0),
        voice='calm', pause=0.5),
      L("Four statements, and one of them is not necessarily true. That means it can fail for some shape. [short pause] So "
        "we go statement by statement. Anything that's surely true, we cross out, and we hope to be left with one.",
        show(f6g66['line'], 'we go statement by statement')),
      L("[short pause] Statement one, every rhombus is a deltoid. What does that mean? Every rhombus has all the "
        "properties of a deltoid. A deltoid is two isosceles triangles on a shared base, the short diagonal.",
        show(f6g66['p1k'], 'A deltoid is two isosceles triangles')),
      L("A rhombus has all its sides equal. But look, its short diagonal also makes two isosceles triangles on a shared "
        "base. So a rhombus has every property of a deltoid. It's true, so choice number one is out. Not every deltoid is a "
        "rhombus, by the way. But a deltoid with all four sides equal is a rhombus.", show(f6g66['p1'], 'its short diagonal also makes'),
        mk('cross', 'choice 1', "so choice number one is out")),
      L("Statement two, every square is a rectangle. A rectangle has its opposite sides equal and all its angles ninety. A "
        "square has all that, and more, because all its sides are equal. It's like an upgraded rectangle. So it's true, and "
        "choice number two is out. Not every rectangle is a square, because its sides don't have to be all equal.",
        show(f6g66['p2r'], 'A rectangle has its opposite sides'), show(f6g66['p2'], 'A square has all that'),
        mk('cross', 'choice 2', 'and choice number two is out')),
      L("Statement three, every rectangle is a parallelogram. A parallelogram has its opposite sides equal and parallel, "
        "its opposite angles equal, and neighbouring angles that add up to one hundred eighty. A rectangle has all of these. "
        "So it's true, and choice number three is out. The other way around isn't true, because not every parallelogram "
        "has four right angles.", show(f6g66['p3'], 'A parallelogram has its opposite sides'),
        mk('cross', 'choice 3', 'and choice number three is out')),
      L("Three statements are out. On the exam, you'd mark choice number four without checking it. Since we're in a lesson, "
        "let's check it anyway. Every parallelogram has perpendicular diagonals."),
      L("Perpendicular diagonals are a property of the rhombus, and not every parallelogram has them. Take a rectangle, "
        "nine by four. It's a parallelogram, but its diagonals are not perpendicular. One shape where it fails is enough, so "
        "this statement is not necessarily true. Choice number four is our answer. [pause] Okay. I'll see you in the next "
        "question.", show(f6g66['p4'], 'Take a rectangle'), mk('tick', 'choice 4', 'Choice number four is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g067 (Hebrew: two corner areas)
# Hebrew (geo 2862-2950): two ways. The math way: ABE is a right triangle (every angle of a rectangle is 90), legs not
# given -> letters: AB = h (the rectangle's height), AE = x; xh / 2 = 3 (English 6) -> xh = 6 (12); ECD: same height h, a
# new part y; yh = 18 (30); the shaded triangle: base x + y, height h (drop it from E: the rectangle's height); open the
# brackets; 12 (21); "the long and tiring solution" but the base is our anchor when we don't see the short way. Then the
# psychometric way: symmetry - drop a height from E, two rectangles, a diagonal cuts a rectangle into two equal halves,
# so the shaded parts are 3 and 9 (6 and 15); easy-plus = question 5 or 6. Her generalization is the next lesson
# (geo-067-after, "Equal Heights, Equal Halves").
# V3: method 1 - each letter written on its segment as it is defined (h orange, x and y teal), each triangle tinted as its
# area is used, the shaded triangle's height dashed from E; method 2 (new copy, from the givens): E pointed at first, then
# the dashed height EF, the two rectangles outlined in turn, each diagonal half tinted with its area.
f6A7, f6B7, f6C7, f6D7, f6E7, f6F7 = (101.0, 82.67), (101.0, 277.33), (539.0, 277.33), (539.0, 82.67), (222.67, 82.67), (222.67, 277.33)
f6g67base = (f6_poly([f6A7, f6B7, f6C7, f6D7]) + [f6_seg(f6E7, f6B7), f6_seg(f6E7, f6C7),
             f6_name(f6A7, 'A', -16, -16), f6_name(f6B7, 'B', -16, 18), f6_name(f6C7, 'C', 16, 18), f6_name(f6D7, 'D', 16, -16),
             f6_name(f6E7, 'E', 0, -22), ('txt', 140, 140, '6', 'ink', 24), ('txt', 440, 140, '15', 'ink', 24)])
f6g67 = GEO('f6g67', [
    ('line', f6g67base),
    ('abe', [('tint', [f6A7, f6B7, f6E7], 'teal'), ('right', f6A7[0], f6A7[1], 270, 0, 16)]),
    ('h', [('seg', f6A7[0], f6A7[1], f6B7[0], f6B7[1], 'orange', 6), ('txt', 78, 180, 'h', 'orange', 28, True)]),
    ('x', [('seg', f6A7[0], f6A7[1], f6E7[0], f6E7[1], 'teal', 6), ('txt', 162, 60, 'x', 'teal', 28, True),
           ('txt', 300, 350, 'x · h ÷ 2 = 6  →  xh = 12', 'ink', 24)]),
    ('y', [('tint', [f6E7, f6C7, f6D7], 'orange'), ('seg', f6E7[0], f6E7[1], f6D7[0], f6D7[1], 'teal', 6), ('txt', 380, 60, 'y', 'teal', 28, True),
           ('txt', 300, 385, 'y · h ÷ 2 = 15  →  yh = 30', 'ink', 24)]),
    ('base', [('seg', f6B7[0], f6B7[1], f6C7[0], f6C7[1], 'red', 6), ('txt', 320, 300, 'x + y', 'red', 26, True)]),
    ('ht', [('dot', *f6E7), f6_seg(f6E7, f6F7, 'orange', 3, True), ('right', f6F7[0], f6F7[1], 0, 90, 14), ('txt', 240, 220, 'h', 'orange', 28, True)]),
    ('s', [('txt', 300, 420, 'S = (x + y)·h ÷ 2 = (12 + 30) ÷ 2 = 21', 'red', 24)]),
], vb='40 30 560 410', w=540, title='Rectangle ABCD with E on AD')
f6g67b = GEO('f6g67b', [
    ('line', f6g67base),
    ('e', [('dot', *f6E7), ('seg', f6E7[0], f6E7[1], f6F7[0], f6F7[1], 'teal', 3, True), ('right', f6F7[0], f6F7[1], 0, 90, 14),
           f6_name(f6F7, 'F', 0, 24)]),
    ('left', [('path', [f6A7, f6B7, f6F7, f6E7, f6A7], 'teal', 6)]),
    ('l6', [('tint', [f6E7, f6B7, f6F7], 'teal'), ('txt', 196, 240, '6', 'teal', 26)]),
    ('right', [('path', [f6E7, f6F7, f6C7, f6D7, f6E7], 'orange', 6)]),
    ('r15', [('tint', [f6E7, f6F7, f6C7], 'orange'), ('txt', 300, 250, '15', 'orange', 26)]),
    ('sum', [('txt', 300, 360, '6 + 15 = 21', 'red', 28)]),
], vb='40 30 560 360', w=540, title='Drop the height from E')
for _g in (f6g67, f6g67b): _R(_g, 205)
video('solve-geo32-g067', 'solution', qid='geo32-g067', slides=[
    SM('Method 1 · Algebra', 'Letters for the sides',
      L("A B C D is a rectangle, and E lies on A D. The areas of triangles A B E and E C D are six square centimeters and "
        "fifteen square centimeters. What is the area of the shaded triangle E B C, in square centimeters?",
        pt('stem', 'A B C D is a rectangle', 'hl', 10.0), voice='calm', pause=0.5),
      L("We know the two white corner triangles and need the shaded one in the middle. [short pause] We'll solve it two "
        "ways, the math way with letters, and then a short way with symmetry.", pt('fig: shaded', 'need the shaded one')),
      L("[short pause] Start with triangle A B E. It's a right triangle, because every angle of a rectangle is ninety. So "
        "its area is leg times leg, over two. But neither leg is given, so we give them letters.",
        show(f6g67['line'], 'Start with triangle A B E'), show(f6g67['abe'], "It's a right triangle")),
      L("A B is the height of the rectangle. Let's call it h. A E is a part of the rectangle's length. Let's call it x. So x "
        "times h, over two, is six. Multiply both sides by two, and x h is twelve.", show(f6g67['h'], "Let's call it h"),
        show(f6g67['x'], "Let's call it x")),
      L("Now triangle E C D. It's a right triangle too, with the same height h. E D is another part of the length, not x. So "
        "it's a new unknown, y. y times h, over two, is fifteen, so y h is thirty.", show(f6g67['y'], "So it's a new unknown")),
      L("Now the shaded triangle E B C. Its base, B C, is the whole length, x plus y. And its height? We drop it from E to B "
        "C, and it's exactly the height of the rectangle, h.", show(f6g67['base'], 'Its base, B C'),
        show(f6g67['ht'], 'We drop it from E')),
      L("So its area is x plus y, times h, over two. Open the brackets. It's x h plus y h, over two, so twelve plus thirty, "
        "over two. That's forty-two over two, which is twenty-one. Choice number two is our answer.",
        show(f6g67['s'], 'So its area is'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("This was a long and tiring solution. But it's an important base. We won't always see the short way, and then we "
        "have something solid to work with.")),
    SM('Method 2 · Symmetry', 'Symmetry',
      L("[pause] Now the short way, with symmetry. Symmetry is a very important tool in geometry, especially in "
        "quadrilaterals. From the point E, let's drop a height down to B C, and call its foot F.",
        show(f6g67b['line'], 'Now the short way'), show(f6g67b['e'], 'From the point E')),
      L("Now we have a rectangle on the left, A B F E. Its diagonal E B cuts it into two triangles. A diagonal cuts a "
        "rectangle into two triangles with the same area. So the shaded triangle E B F is six, like the white triangle A B "
        "E.", show(f6g67b['left'], 'Now we have a rectangle on the left'), show(f6g67b['l6'], 'So the shaded triangle E B F')),
      L("The same on the right. E F C D is a rectangle, its diagonal is E C, and the white triangle E C D is fifteen. So the "
        "shaded triangle E F C is fifteen too.", show(f6g67b['right'], 'The same on the right'),
        show(f6g67b['r15'], 'So the shaded triangle E F C')),
      L("So the shaded area is equal to the two white areas together, six plus fifteen, which is twenty-one. Choice number "
        "two. Much shorter. That's why this question counts as easy-plus. On the exam it's about question five or six. The "
        "math is long, but the short way is quick.", show(f6g67b['sum'], 'six plus fifteen'), mk('tick', 'choice 2', 'Choice number two. Much shorter')),
      L("This idea is very important, and in the next lesson we'll stretch it to more shapes. [pause] Okay. I'll see you in "
        "the next question.")),
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
