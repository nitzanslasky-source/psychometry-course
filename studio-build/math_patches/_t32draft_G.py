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
# Topic-32 advanced block (fragment f7, 2026-10-14): geo-067-after (the symmetry principle, stretched), geo32-g068,
# geo32-g069, geo32-g070 - the Hebrew "quadrilaterals advanced" lesson (geo 2955-3270). Lesson figures on the left
# (col 0, w 600) with typed lines on the right; question videos: the question figure on the left (FIG_LEFT), our colour
# copy built in layers on the right (Rule V3), its working written inside the copy so the layers stay together.
# Every Hebrew method is kept (g070: subtracting areas, completions, symmetry).
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g068', 'solve-geo32-g069', 'solve-geo32-g070'})


def f7_poly(pts, col='ink', w=3):
    """the sides of a closed polygon as segments"""
    return [('seg', pts[k][0], pts[k][1], pts[(k + 1) % len(pts)][0], pts[(k + 1) % len(pts)][1], col, w) for k in range(len(pts))]


def f7_lab(items):
    return [('txt', x, y, t, 'ink', 26, True) for x, y, t in items]


# ------------------------------------------------------------------------------------------------ geo-067-after (lesson)
# Hebrew (geo 2955-2995): a diagonal halves a rectangle (grey = white); a triangle inside a rectangle with its tip on the
# opposite side: drop a height, each grey piece equals its white twin; any number of triangles whose bases fill the
# side; the whole parallelogram family; a triangle on the base of a parallelogram (a line parallel to the sides makes two
# parallelograms); part of the base (her thirds -> 1/6; the course's quarters -> 1/8). "The symmetry principle is very
# important; some exam questions fall apart with it."
# V3: generic clean figures (not a question's), every pair of equal halves in ONE tint (teal pair, orange pair), the
# height / the parallel line dashed and drawn after its start point is named; the triangle moved to a second position to
# show it doesn't matter; the base cut into four with ticks.
f7R = [(110, 70), (110, 270), (500, 270), (500, 70)]          # a generic rectangle: A top-left, B, C, D
f7diag = GEO('f7diag', [
    ('line', f7_poly(f7R)),
    ('d', [('seg', 110, 70, 500, 270, 'ink', 3)]),
    ('halves', [('tint', [(110, 70), (110, 270), (500, 270)], 'teal'), ('tint', [(110, 70), (500, 70), (500, 270)], 'orange'),
                ('txt', 210, 215, 'half', 'small', 28), ('txt', 400, 125, 'half', 'orange', 28)]),
], vb='60 40 500 260', w=680, col=0, title='A diagonal halves a rectangle')
f7E1 = (230, 70)
f7in = GEO('f7in', [
    ('line', f7_poly(f7R) + [('seg', 110, 270, f7E1[0], f7E1[1], 'ink', 3), ('seg', f7E1[0], f7E1[1], 500, 270, 'ink', 3),
                             ('tint', [(110, 270), f7E1, (500, 270)], 'ink'), ('txt', f7E1[0], 48, 'E', 'ink', 26, True)]),
    ('h', [('dot', f7E1[0], f7E1[1]), ('seg', f7E1[0], 70, f7E1[0], 270, 'teal', 3, True), ('right', f7E1[0], 270, 0, 90, 14)]),
    ('left', [('tint', [(110, 70), (110, 270), f7E1], 'teal'), ('tint', [f7E1, (110, 270), (f7E1[0], 270)], 'teal'),
              ('txt', 140, 130, 'a', 'small', 28, True), ('txt', 195, 245, 'a', 'small', 28, True)]),
    ('right', [('tint', [f7E1, (500, 70), (500, 270)], 'orange'), ('tint', [f7E1, (f7E1[0], 270), (500, 270)], 'orange'),
               ('txt', 440, 110, 'b', 'orange', 28, True), ('txt', 330, 240, 'b', 'orange', 28, True)]),
], vb='60 30 500 270', w=680, col=0, title='A triangle in a rectangle: each grey piece has a white twin')
f7E2 = (420, 70)
f7move = GEO('f7move', [
    ('line', f7_poly(f7R) + [('seg', 110, 270, f7E2[0], f7E2[1], 'ink', 3), ('seg', f7E2[0], f7E2[1], 500, 270, 'ink', 3),
                             ('tint', [(110, 270), f7E2, (500, 270)], 'teal'), ('txt', f7E2[0], 48, 'E', 'ink', 26, True),
                             ('seg', f7E1[0], 70, 110, 270, 'red', 2, True), ('seg', f7E1[0], 70, 500, 270, 'red', 2, True),
                             ('txt', 300, 175, 'still half', 'small', 28)]),
], vb='60 30 500 270', w=680, col=0, title='Move E along the top side: still half')
f7many = GEO('f7many', [
    ('line', f7_poly(f7R)),
    ('tris', [('seg', 110, 270, 170, 70, 'ink', 3), ('seg', 170, 70, 250, 270, 'ink', 3), ('seg', 250, 270, 330, 70, 'ink', 3),
              ('seg', 330, 70, 380, 270, 'ink', 3), ('seg', 380, 270, 460, 70, 'ink', 3), ('seg', 460, 70, 500, 270, 'ink', 3),
              ('tint', [(110, 270), (170, 70), (250, 270)], 'teal'), ('tint', [(250, 270), (330, 70), (380, 270)], 'teal'),
              ('tint', [(380, 270), (460, 70), (500, 270)], 'teal')]),
    ('bases', [('seg', 110, 290, 250, 290, 'teal', 5), ('seg', 252, 290, 380, 290, 'orange', 5), ('seg', 382, 290, 500, 290, 'teal', 5),
               ('txt', 305, 318, 'the bases fill the side', 'ink', 24)]),
], vb='60 40 500 300', w=680, col=0, title='Many triangles with their tips on the top side')
f7P = [(170, 70), (110, 270), (440, 270), (500, 70)]           # a parallelogram: top-left, bottom-left, bottom-right, top-right
f7par = GEO('f7par', [
    ('line', f7_poly(f7P)),
    ('d', [('seg', 170, 70, 440, 270, 'ink', 3), ('tint', [(170, 70), (110, 270), (440, 270)], 'teal'),
           ('tint', [(170, 70), (500, 70), (440, 270)], 'orange')]),
], vb='60 40 500 260', w=680, col=0, title='A diagonal halves a parallelogram')
f7T = (320, 70)
f7par2 = GEO('f7par2', [
    ('line', f7_poly(f7P) + [('seg', 110, 270, f7T[0], f7T[1], 'ink', 3), ('seg', f7T[0], f7T[1], 440, 270, 'ink', 3),
                             ('tint', [(110, 270), f7T, (440, 270)], 'ink'), ('dot', f7T[0], f7T[1])]),
    ('cut', [('seg', f7T[0], 70, 260, 270, 'teal', 3, True)]),
    ('pairs', [('tint', [(170, 70), (110, 270), f7T], 'teal'), ('tint', [f7T, (110, 270), (260, 270)], 'teal'),
               ('tint', [f7T, (500, 70), (440, 270)], 'orange'), ('tint', [f7T, (260, 270), (440, 270)], 'orange')]),
], vb='60 40 500 260', w=680, col=0, title='A line parallel to the sides makes two parallelograms')
f7Q = [(110 + 97.5 * k, 270) for k in range(5)]
f7part = GEO('f7part', [
    ('line', f7_poly(f7R) + [('dot', x, y) for x, y in f7Q[1:4]] + [('tick', f7Q[k][0], 270, f7Q[k + 1][0], 270, 1) for k in range(4)]),
    ('tri', [('seg', f7Q[1][0], 270, 400, 70, 'ink', 3), ('seg', 400, 70, f7Q[2][0], 270, 'ink', 3),
             ('tint', [(f7Q[1][0], 270), (400, 70), (f7Q[2][0], 270)], 'teal')]),
    ('whole', [('seg', 110, 270, 400, 70, 'orange', 2.5, True), ('seg', 400, 70, 500, 270, 'orange', 2.5, True),
               ('txt', 305, 45, 'whole base: ½ of the rectangle', 'orange', 24)]),
    ('quarter', [('txt', 305, 302, '¼ of the base  →  ⅛ of the rectangle', 'small', 24)]),
], vb='60 20 500 300', w=680, col=0, title='A triangle on a quarter of the base')
f7a1 = I('f7a1', 'Diagonal: $\\ $grey $=$ white $=\\frac12$', size=30, col=1)
f7a2 = I('f7a2', 'Tip on the top side: $\\ $grey $=\\frac12$', size=30, col=1)
f7a3 = I('f7a3', 'Bases fill the side, tips on the top side', size=28, col=1)
f7a4 = I('f7a4', 'Parallelogram, rectangle, rhombus, square', size=28, col=1)
f7a5 = I('f7a5', 'Same base, same height $\\Rightarrow$ the same area', size=28, col=1)
f7a6 = IH('f7a6', '$\\frac14\\cdot\\frac12=\\frac18$', size=36, col=1)
video('geo-067-after', 'lesson', slides=[
    S('Equal Heights, Equal Halves',
      L("In the last question, the shaded triangle was exactly as big as the two white triangles together. Let's take "
        "that idea and stretch it.")),
    S('A diagonal',
      L("A rectangle, and a diagonal in it. The diagonal cuts the rectangle into two triangles, and they are exactly the "
        "same size. So the shaded half equals the white half, and each one is half of the rectangle. That's clear to all "
        "of us.", show(f7diag['line'], 'A rectangle, and a diagonal'), show(f7diag['d'], 'The diagonal cuts'),
        show(f7diag['halves'], 'So the shaded half equals'), show(f7a1, 'each one is half'))),
    S('A triangle inside',
      L("Now a shaded triangle inside a rectangle, like in the last question. Its base is the bottom side, and its tip, E, "
        "is on the top side. Here too, the shaded part is half of the rectangle, and the white parts together are the "
        "other half.", show(f7in['line'], 'Now a shaded triangle')),
      L("Why? From E, drop a height down to the bottom side. It cuts the rectangle into two smaller rectangles, and each "
        "small rectangle has a diagonal.", show(f7in['h'], 'drop a height')),
      L("In the left rectangle, the shaded piece and the white piece are the two halves, so they're equal. In the right "
        "rectangle too. So each shaded piece equals its white twin.", show(f7in['left'], 'In the left rectangle'),
        show(f7in['right'], 'In the right rectangle too')),
      L("And it doesn't matter where E is along the top side. Move it, and the shaded triangle is still half of the "
        "rectangle.", show(f7move['line'], 'Move it'), show(f7a2, 'still half'))),
    S('Many triangles',
      L("It's true here as well. It doesn't matter how many triangles there are inside the rectangle, as long as their "
        "bases fill the bottom side, one after the other, and their tips are on the top side.",
        show(f7many['line'], "It's true here as well"), show(f7many['tris'], 'how many triangles'),
        show(f7many['bases'], 'their bases fill'), show(f7a3, 'their tips are on the top side')),
      L("Then the shaded parts always add up to the white parts, and each is half of the rectangle.",
        pt('f7many_line', 'the shaded parts always'))),
    S('The parallelogram family',
      L("By the way, this isn't only true in a rectangle. It's true in the whole parallelogram family: a parallelogram, a "
        "rectangle, a rhombus and a square. A diagonal in a parallelogram also cuts it into two triangles with the same "
        "area.", show(f7par['line'], 'In the whole parallelogram family'), show(f7par['d'], 'A diagonal in a parallelogram'),
        show(f7a4, 'two triangles with the same')),
      L("And this one? A shaded triangle on the bottom side of a parallelogram, with its tip on the top side. It's harder "
        "to see, but from the tip, draw a line parallel to the slanted sides.", show(f7par2['line'], 'And this one'),
        show(f7par2['cut'], 'draw a line parallel')),
      L("Now we have two parallelograms, a left one and a right one. In each of them, the shaded piece and the white "
        "piece are the two halves. So the shaded triangle is half of the whole parallelogram. Same base and same height, "
        "and it doesn't matter how many triangles.", show(f7par2['pairs'], 'Now we have two parallelograms'),
        show(f7a5, 'Same base and same height'))),
    S('Part of the base',
      L("A slightly more advanced one. The bottom side is cut into four equal pieces. The shaded triangle stands on one "
        "piece, and its tip is on the top side. What part of the rectangle is it?",
        show(f7part['line'], 'cut into four equal pieces'), show(f7part['tri'], 'The shaded triangle stands')),
      L("A triangle on the whole bottom side, with its tip on the top side, would be half of the rectangle. Ours has the "
        "same height, but it stands on only a quarter of the bottom side. So it's a quarter of that half.",
        show(f7part['whole'], 'A triangle on the whole bottom side'), show(f7part['quarter'], 'So it\'s a quarter of that half')),
      L("A quarter of a half is an eighth. So the shaded triangle is an eighth of the rectangle.",
        show(f7a6, 'A quarter of a half')),
      L("This symmetry principle is very important. Some exam questions become easy with it, and we'll see one in the "
        "next question. [pause] Okay. I'll see you in the next video.", pt('f7a6', 'This symmetry principle'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g068 (Hebrew: "which data is sufficient")
# Hebrew (geo 3020-3088): an unclear wording - which ONE given would be enough to calculate the shaded area? Call the area
# of ECD s ("10, 100 - any number"); the diagonal halves the right rectangle (EGC = s); the left rectangle from the
# ratio (Hebrew: midpoints, equal; course: 3 to 1, three times); FEG is half of the left rectangle (symmetry); total;
# some students see it as a fraction of the rectangle; "in the exam we mark and run; in the lesson we check the rest":
# AFE and FBG fail because F's place is unknown (even with a number); "none" fails because one was enough.
# V3: the colour copy is built; E and G marked with their 3 : 1 pieces; the right rectangle outlined, ECD and EGC tinted
# orange with s written on each; the left rectangle with 6s; FEG tinted teal with 3s; the working written below.
f7A, f7B, f7C, f7D = (155.75, 70.5), (155.75, 289.5), (484.25, 289.5), (484.25, 70.5)
f7E, f7G, f7F = (402.125, 70.5), (402.125, 289.5), (155.75, 216.5)
f7g68_base = (f7_poly([f7A, f7B, f7C, f7D]) + [('seg', f7E[0], f7E[1], f7G[0], f7G[1], 'ink', 3), ('seg', f7F[0], f7F[1], f7E[0], f7E[1], 'ink', 3),
              ('seg', f7F[0], f7F[1], f7G[0], f7G[1], 'ink', 3), ('seg', f7E[0], f7E[1], f7C[0], f7C[1], 'ink', 3)]
              + f7_lab([(141, 55, 'A'), (141, 307, 'B'), (499, 307, 'C'), (499, 55, 'D'), (402, 50, 'E'), (402, 312, 'G'), (133, 216, 'F')]))
f7g68 = GEO('f7g68', [
    ('line', f7g68_base),
    ('ratio', [('txt', 279, 92, '3', 'teal', 26), ('txt', 443, 92, '1', 'orange', 26), ('txt', 279, 268, '3', 'teal', 26),
               ('txt', 443, 268, '1', 'orange', 26)]),
    ('ecd', [('tint', [f7E, f7C, f7D], 'orange'), ('txt', 462, 120, 's', 'orange', 30, True)]),
    ('egc', [('tint', [f7E, f7G, f7C], 'orange'), ('txt', 424, 245, 's', 'orange', 30, True), ('txt', 443, 332, '2s', 'orange', 30, True)]),
    ('left', [('tint', [f7A, f7B, f7G, f7E], 'teal'), ('txt', 279, 332, '3 · 2s = 6s', 'small', 28)]),
    ('feg', [('tint', [f7F, f7E, f7G], 'teal'), ('txt', 330, 175, '3s', 'small', 32), ('txt', 275, 50, 'shaded: s + 3s = 4s', 'ink', 24)]),
], vb='110 25 420 325', w=500, title='Rectangle ABCD with E on AD and G on BC')
f7Fp = (f7E[0], f7F[1])
f7g68b = GEO('f7g68b', [
    ('line', f7g68_base),
    ('afe', [('tint', [f7A, f7F, f7E], 'orange'), ('txt', 200, 120, 's', 'orange', 30, True), ('dot', f7Fp[0], f7Fp[1]),
             ('seg', f7F[0], f7F[1], f7Fp[0], f7Fp[1], 'orange', 3, True), ('txt', 270, 158, 's', 'orange', 30, True)]),
    ('low', [('tint', [f7F, f7B, f7G, f7Fp], 'red'), ('txt', 279, 262, '?', 'red', 40), ('txt', 275, 50, 'where is F?', 'red', 26)]),
], vb='110 25 420 325', w=500, title='Why the area of AFE is not enough')
for _it, _y in [(f7g68, 200), (f7g68b, 200)]:
    _R(_it, _y)
video('solve-geo32-g068', 'solution', qid='geo32-g068', slides=[
    SM('The area of E C D', 'The area of E C D',
      L("A B C D is a rectangle. E lies on A D, G lies on B C, and F lies on A B. A E is three times E D, and B G is three "
        "times G C. Triangles F E G and E G C are shaded. Which of the following additional data is sufficient to determine "
        "the total shaded area?", pt('stem', 'A B C D is a rectangle', 'hl', 12.0), voice='calm', pause=0.5),
      L("The wording isn't very clear. What do they want? They ask which one piece of data, if they gave it to us, would "
        "be enough to calculate the shaded area. [short pause] We'll use the symmetry principle from the last lesson.",
        pt('stem: ask', 'They ask which one piece')),
      L("[short pause] First, the figure. E cuts A D into two pieces, three to one, and G cuts B C the same way, three to "
        "one. So E is exactly above G, and E G is a straight line from top to bottom. It cuts the rectangle into a left "
        "rectangle and a right rectangle. And F? Nobody told us where F is on A B. Remember that.",
        show(f7g68['line'], 'First, the figure'), show(f7g68['ratio'], 'three to one'), pt('fig: F', 'And F')),
      L("Let's start with the data that works, the area of E C D. They don't say how big it is, so let's call it s. It "
        "could be ten, or a hundred, any number.", show(f7g68['ecd'], "let's call it s")),
      L("E C is a diagonal of the right rectangle, so it cuts it into two equal halves. That means the shaded triangle E G "
        "C is also s, and the right rectangle is s plus s, two s.", show(f7g68['egc'], 'the shaded triangle E G C')),
      L("The left rectangle has the same height, and its base is three times longer, three to one. So it's three times as "
        "big, three times two s, which is six s.", show(f7g68['left'], 'three times as big')),
      L("And the shaded triangle F E G? Its base is E G, the whole side of the left rectangle, and its tip F is on the "
        "opposite side, A B. That's the symmetry principle again, so it's half of the left rectangle, three s. Together, "
        "the shaded area is s plus three s, four s. So if they give us the area of E C D, we can find the shaded area.",
        show(f7g68['feg'], 'And the shaded triangle F E G')),
      L("Some students see it even faster. The whole rectangle is eight s, the shaded part is half of it, and E C D is "
        "an eighth. In the exam, once we've understood this, we mark choice number one and move on.",
        mk('tick', 'choice 1', 'we mark choice number one'))),
    SM('Why not the others?', 'Why not the others?',
      L("[pause] We're in a lesson, so let's see why the other choices fail. Choice number two, the area of A F E. Say "
        "it's s. A F E is half of a small rectangle at the top, so that rectangle is two s.",
        show(f7g68b['line'], "Choice number two, the area of A F E"), show(f7g68b['afe'], 'A F E is half of a small')),
      L("But how big is the rectangle under it? We can't know, because we don't know where F is. If they told us that F "
        "is the middle of A B, the two parts would match. They didn't. So even with a number, five, ten or twenty, we "
        "can't find the shaded area. Choice number two is out.", show(f7g68b['low'], 'how big is the rectangle under it'),
        mk('cross', 'choice 2', 'Choice number two is out')),
      L("Choice number three, the area of F B G, has exactly the same problem. We don't know where F is. It's out too.",
        mk('cross', 'choice 3', "It's out too")),
      L("And choice number four says none of the data is enough, but we already saw that the area of E C D is enough. "
        "So it's out, and choice number one is our answer. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 4', 'So it\'s out'), mk('tick', 'choice 1', 'choice number one is our answer'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g069 (Hebrew: the isosceles trapezoid)
# Hebrew (geo 3089-3168): two ways. The full math: the shaded triangle is obtuse, its only known base is AD, its height is
# outside (extend AD, drop the shortest distance from B); 3h/2 = 10 (course: 5h/2 = 15, h = 6); that height is also the
# trapezoid's height; (sum of bases) x h / 2. The psychometric way: the shaded and the white triangle have the same height,
# so the area ratio is the base ratio; illustrate by cutting BC into pieces as long as AD (she notices a parallelogram,
# BD its diagonal); "if the base were 3 times bigger the area would be 3 times bigger"; much shorter, you barely write.
# V3: the copy; AD and its 5 in teal; the dashed extension of AD, then the dashed outside height from B with its right
# angle and h; the working below; method 2: a new copy, BC cut into four pieces of 5 (ticks), dashed lines from D, 15 in
# each triangle; the parallelogram ABPD outlined.
f7a_, f7b_, f7c_, f7d_ = (271.333, 66.444), (125.333, 293.556), (514.667, 293.556), (368.667, 66.444)
f7H = (f7b_[0], f7a_[1])
f7g69_base = (f7_poly([f7a_, f7b_, f7c_, f7d_]) + [('seg', f7b_[0], f7b_[1], f7d_[0], f7d_[1], 'ink', 3),
              ('tint', [f7a_, f7b_, f7d_], 'ink')]
              + f7_lab([(257, 50, 'A'), (111, 312, 'B'), (529, 312, 'C'), (383, 50, 'D')])
              + [('txt', 320, 46, '5', 'ink', 24), ('txt', 320, 318, '20', 'ink', 24)])
f7g69 = GEO('f7g69', [
    ('line', f7g69_base),
    ('ad', [('seg', f7a_[0], f7a_[1], f7d_[0], f7d_[1], 'teal', 6)]),
    ('ext', [('seg', f7a_[0], f7a_[1], f7H[0] - 10, f7H[1], 'teal', 3, True)]),
    ('h', [('seg', f7b_[0], f7b_[1], f7H[0], f7H[1], 'teal', 3, True), ('right', f7H[0], f7H[1], 0, 270, 14),
           ('txt', f7H[0] - 20, 180, 'h', 'small', 30, True)]),
    ('h6', [('txt', f7H[0] + 6, 215, '= 6', 'small', 28), ('txt', 320, 18, '5h ÷ 2 = 15  →  h = 6', 'small', 24)]),
    ('area', [('txt', 320, 352, '(5 + 20) · 6 ÷ 2 = 75', 'ink', 26)]),
], vb='90 0 450 370', w=500, title='Isosceles trapezoid ABCD with the diagonal BD')
f7Pk = [(f7b_[0] + 97.333 * k, f7b_[1]) for k in range(5)]
f7g69b = GEO('f7g69b', [
    ('line', f7g69_base),
    ('same', [('seg', f7a_[0], f7a_[1], f7d_[0], f7d_[1], 'small', 6), ('seg', f7b_[0], f7b_[1], f7c_[0], f7c_[1], 'orange', 6),
              ('txt', 320, 18, 'same height: area ratio = base ratio', 'ink', 24)]),
    ('cuts', [('dot', x, y) for x, y in f7Pk[1:4]] + [('tick', f7Pk[k][0], f7Pk[k][1], f7Pk[k + 1][0], f7Pk[k + 1][1], 1) for k in range(4)]
             + [('seg', f7d_[0], f7d_[1], x, y, 'orange', 2.5, True) for x, y in f7Pk[1:4]]),
    ('par', [('path', [f7a_, f7b_, f7Pk[1], f7d_, f7a_], 'small', 5)]),
    ('vals', [('txt', 290, 110, '15', 'small', 28)] + [('txt', (f7Pk[k][0] + f7Pk[k + 1][0]) / 2 + 6, 276, '15', 'orange', 24) for k in range(4)]
             + [('txt', 320, 352, '15 + 4 · 15 = 75', 'ink', 26)]),
], vb='90 0 450 370', w=500, title='Cut BC into four pieces of 5')
for _it, _y in [(f7g69, 200), (f7g69b, 200)]:
    _R(_it, _y)
video('solve-geo32-g069', 'solution', qid='geo32-g069', slides=[
    SM('Method 1 · The full math', 'The full math',
      L("A B C D is an isosceles trapezoid. A D is parallel to B C, A D is five centimeters and B C is twenty centimeters. "
        "The shaded triangle A B D has an area of fifteen square centimeters. What is the area of the trapezoid?",
        pt('stem', 'A B C D is an isosceles trapezoid', 'hl', 10.0), voice='calm', pause=0.5),
      L("We know the area of the shaded triangle, and we need the area of the whole trapezoid. [short pause] We'll solve "
        "it two ways, with the full math, and then with a ratio principle.", pt('fig: 15 cm²', 'We know the area')),
      L("[short pause] The full math first. The shaded part is a triangle, an obtuse one. Its area is base times height, "
        "over two, and the only base we know is A D, five.", show(f7g69['line'], 'The full math first'),
        show(f7g69['ad'], 'the only base we know is A D')),
      L("Where is the height to A D? In an obtuse triangle the height is outside. So we extend A D, and from B we drop "
        "the shortest line to it, at a right angle. That's the height, h.", show(f7g69['ext'], 'we extend A D'),
        show(f7g69['h'], 'from B we drop')),
      L("So five times h, over two, is fifteen. Five h is thirty, so h is six.", show(f7g69['h6'], 'So five times h')),
      L("And look, this height is also the height of the trapezoid, the distance between the two parallel sides. The "
        "area of a trapezoid is the sum of the bases, times the height, over two. Five plus twenty is twenty-five, times "
        "six is a hundred fifty, over two is seventy-five. Choice number three is our answer.",
        show(f7g69['area'], 'The area of a trapezoid'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · A ratio', 'A ratio',
      L("[pause] Not too bad, but there's a much shorter way, with a ratio principle. Look at the shaded triangle A B D "
        "and the white triangle B C D. They have the same height, the height of the trapezoid. In the white one it's easy "
        "to see. In the shaded one, it's the outside height we drew.", show(f7g69b['line'], 'Look at the shaded triangle')),
      L("When two triangles have the same height, the ratio of their areas is the ratio of their bases. The shaded base "
        "is five, and the white base is twenty, four times bigger. So the white area is four times bigger too.",
        show(f7g69b['same'], 'the ratio of their areas')),
      L("Let's see it. Cut B C into four pieces of five, and draw lines from D. Now every triangle here has the same base, "
        "five, and the same height. A B and the first piece even make a parallelogram, with B D as its diagonal.",
        show(f7g69b['cuts'], 'Cut B C into four pieces'), show(f7g69b['par'], 'make a parallelogram')),
      L("So all the triangles have the same area, fifteen each. The whole trapezoid is fifteen plus four times fifteen, "
        "which is seventy-five. Choice number three again. Careful, sixty is only the white triangle, so choice number "
        "two is a trap.", show(f7g69b['vals'], 'fifteen each'), mk('tick', 'choice 3', 'Choice number three again'),
        mk('cross', 'choice 2', 'choice number two is a trap')),
      L("Same height, so the area ratio follows the base ratio. If the base were three times bigger, the area would be "
        "three times bigger. You barely write anything, you just see it. [pause] Okay. I'll see you in the next question.",
        pt('f7g69b_line', 'Same height, so the area ratio'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g070 (Hebrew: the shaded pentagon on a grid)
# Hebrew (geo 3171-3268): "a trapezoid? count the sides: a pentagon - we never learned it"; "shaded-area questions": two
# main approaches - subtract the white areas from a shape we know (the main and most common), or break the shaded area
# into familiar shapes, by completions or by symmetry. Course numbers: 8 x 5 grid, white triangles 3, 5, 3, 3, shaded 26.
# Completions are made EXACT here: every sloping side is the diagonal of a corner rectangle, so the cut pieces on its two
# sides are the same pieces turned around and complete each other (shaded part = half of that rectangle).
# V3: the copy with its grid; method 1: the four white corner triangles tinted orange one by one with their legs and
# areas; method 2: the five rectangles that tile the grid outlined, one corner rectangle with its two halves in two tints;
# method 3: the dashed line between the side vertices, the triangle above it teal, the middle rectangle and the two side
# triangles; the working written below the copy.
f7gx = lambda i: 174.0 + 36.5 * i
f7gy = lambda j: 78.75 + 36.5 * j
f7gp = lambda i, j: (f7gx(i), f7gy(j))
f7pent = [f7gp(3, 0), f7gp(8, 2), f7gp(6, 5), f7gp(2, 5), f7gp(0, 2)]
f7grid = ([('seg', f7gx(i), f7gy(0), f7gx(i), f7gy(5), 'ink', 1) for i in range(1, 8)]
          + [('seg', f7gx(0), f7gy(j), f7gx(8), f7gy(j), 'ink', 1) for j in range(1, 5)]
          + f7_poly([f7gp(0, 0), f7gp(8, 0), f7gp(8, 5), f7gp(0, 5)]) + f7_poly(f7pent) + [('tint', f7pent, 'ink')])
f7W = [([f7gp(0, 0), f7gp(3, 0), f7gp(0, 2)], '3', (1.0, 0.7)), ([f7gp(3, 0), f7gp(8, 0), f7gp(8, 2)], '5', (6.3, 0.6)),
       ([f7gp(8, 2), f7gp(8, 5), f7gp(6, 5)], '3', (7.3, 4.0)), ([f7gp(0, 2), f7gp(0, 5), f7gp(2, 5)], '3', (0.7, 4.0))]
f7vb = '150 30 340 305'
f7g70 = GEO('f7g70', [('line', f7grid)]
            + [('w%d' % k, [('tint', pts, 'orange')] + f7_poly(pts, 'orange', 4) + [('txt', f7gx(c[0]), f7gy(c[1]), v, 'orange', 30)])
               for k, (pts, v, c) in enumerate(f7W)]
            + [('rect', [('txt', 320, 55, 'rectangle: 8 · 5 = 40', 'ink', 24)]),
               ('sum', [('txt', 320, 288, 'white: 3 + 5 + 3 + 3 = 14', 'orange', 24), ('txt', 320, 318, '40 − 14 = 26', 'ink', 26)])],
            vb=f7vb, w=480, title='A shaded pentagon on an 8 by 5 grid')
f7g70b = GEO('f7g70b', [
    ('line', f7grid),
    ('tiles', [('seg', f7gx(3), f7gy(0), f7gx(3), f7gy(2), 'teal', 3, True), ('seg', f7gx(0), f7gy(2), f7gx(8), f7gy(2), 'teal', 3, True),
               ('seg', f7gx(2), f7gy(2), f7gx(2), f7gy(5), 'teal', 3, True), ('seg', f7gx(6), f7gy(2), f7gx(6), f7gy(5), 'teal', 3, True)]),
    ('pair', [('tint', [f7gp(0, 2), f7gp(3, 0), f7gp(3, 2)], 'small'), ('tint', [f7gp(0, 0), f7gp(3, 0), f7gp(0, 2)], 'orange'),
              ('txt', f7gx(2.1), f7gy(1.45), '3', 'small', 28)]),
    ('vals', [('txt', f7gx(5.8), f7gy(1.4), '5', 'small', 28), ('txt', f7gx(1.35), f7gy(3.8), '3', 'small', 28),
              ('txt', f7gx(6.65), f7gy(3.8), '3', 'small', 28), ('txt', f7gx(4), f7gy(3.6), '12', 'small', 32),
              ('txt', 320, 300, '3 + 5 + 3 + 3 + 12 = 26', 'ink', 26)]),
], vb=f7vb, w=480, title='Completions: each corner rectangle is cut in half')
f7g70c = GEO('f7g70c', [
    ('line', f7grid),
    ('cut', [('dot', f7gx(0), f7gy(2)), ('dot', f7gx(8), f7gy(2)), ('seg', f7gx(0), f7gy(2), f7gx(8), f7gy(2), 'teal', 3, True)]),
    ('top', [('tint', [f7gp(0, 2), f7gp(3, 0), f7gp(8, 2)], 'small'), ('txt', f7gx(3.6), f7gy(1.35), '8', 'small', 32)]),
    ('mid', [('tint', [f7gp(2, 2), f7gp(6, 2), f7gp(6, 5), f7gp(2, 5)], 'orange'), ('txt', f7gx(4), f7gy(3.6), '12', 'orange', 32)]),
    ('sides', [('tint', [f7gp(0, 2), f7gp(2, 2), f7gp(2, 5)], 'small'), ('tint', [f7gp(6, 2), f7gp(8, 2), f7gp(6, 5)], 'small'),
               ('txt', f7gx(1.35), f7gy(2.9), '3', 'small', 28), ('txt', f7gx(6.65), f7gy(2.9), '3', 'small', 28)]),
    ('sum', [('txt', 320, 300, '8 + 12 + 3 + 3 = 26', 'ink', 26)]),
], vb=f7vb, w=480, title='Symmetry: break the shape into familiar pieces')
for _it, _y in [(f7g70, 200), (f7g70b, 200), (f7g70c, 200)]:
    _R(_it, _y)
video('solve-geo32-g070', 'solution', qid='geo32-g070', slides=[
    SM('Method 1 · Subtracting areas', 'Subtracting areas',
      L("The rectangle in the accompanying figure is made of forty congruent squares, each with a side of one centimeter. "
        "What is the shaded area?", pt('stem', 'The rectangle in the accompanying figure', 'hl', 8.0), voice='calm', pause=0.5),
      L("What is the shaded shape? A trapezoid? Let's count its sides. One, two, three, four, five. It's a pentagon, and "
        "we never learned an area formula for it. We call these shaded-area questions, and there are two main "
        "approaches.", pt('stem: ask', 'What is the shaded shape')),
      L("[short pause] One approach takes an area we know, the rectangle, and subtracts the white parts. The other breaks "
        "the shaded area into shapes we know, with completions or with symmetry. We'll see all of them. Subtracting is "
        "the main one, and the most common, so we start with it.", show(f7g70['line'], 'One approach takes an area we know')),
      L("The rectangle has forty squares, so its area is forty. The white parts are four right triangles in the corners, "
        "and the area of a right triangle is leg times leg, over two.", show(f7g70['rect'], 'The rectangle has forty squares')),
      L("Top left: the legs are three and two. Three times two is six, over two is three. Top right: the legs are five "
        "and two, so it's five. The two bottom ones have legs of two and three, so three each.",
        show(f7g70['w0'], 'Top left'), show(f7g70['w1'], 'Top right'), show(f7g70['w2'], 'The two bottom ones'),
        show(f7g70['w3'], 'so three each')),
      L("All the white parts together are three plus five plus three plus three, fourteen. Forty minus fourteen is "
        "twenty-six. Choice number three is our answer. Careful, fourteen, choice number one, is the white part, not the "
        "shaded part.", show(f7g70['sum'], 'All the white parts together'), mk('tick', 'choice 3', 'Choice number three is our answer'),
        mk('cross', 'choice 1', 'Careful, fourteen, choice number one'))),
    SM('Method 2 · Completions', 'Completions',
      L("[pause] Now completions. Many students count whole squares, and when two pieces of squares complete each other "
        "into one whole square, they count them as one.", show(f7g70b['line'], 'Now completions')),
      L("Here the sloping sides cut squares into odd pieces, so we look at them in groups. Cut the grid into five "
        "rectangles: four in the corners, and one in the middle.", show(f7g70b['tiles'], 'Cut the grid into five rectangles')),
      L("Look at the top left rectangle, three by two. The sloping side goes from corner to corner, so every shaded piece "
        "has a white piece just like it, turned around. They complete each other, so the shaded part is half of six, "
        "three.", show(f7g70b['pair'], 'Look at the top left rectangle')),
      L("The same in the other corners: half of ten is five, and half of six is three, twice. The middle rectangle is all "
        "shaded, four by three, twelve whole squares. Three plus five plus three plus three plus twelve is twenty-six. "
        "Choice number three again.", show(f7g70b['vals'], 'The same in the other corners'), mk('tick', 'choice 3', 'Choice number three again'))),
    SM('Method 3 · Symmetry', 'Symmetry',
      L("[pause] And the third way, with the symmetry principle we already know. We break the shape into pieces we know. "
        "Draw a line between the two side corners of the pentagon.", show(f7g70c['line'], 'And the third way'),
        show(f7g70c['cut'], 'Draw a line between')),
      L("Above the line there's a triangle. Its base is the whole width, eight, and its tip is on the top side of an eight "
        "by two rectangle. So it's half of sixteen, eight.", show(f7g70c['top'], 'Above the line')),
      L("Below the line, the middle rectangle is four by three, twelve. And each side triangle is half of a two by three "
        "rectangle, half of six, three.", show(f7g70c['mid'], 'the middle rectangle'), show(f7g70c['sides'], 'each side triangle')),
      L("Eight plus twelve plus three plus three is twenty-six. Choice number three again. So in a shaded-area question, "
        "subtract the white parts from a shape you know, or break the shaded part into shapes you know. [pause] Okay. "
        "I'll see you in the next question.", show(f7g70c['sum'], 'Eight plus twelve'), mk('tick', 'choice 3', 'Choice number three again.'))),
])


def f7_pin(g):
    """pin every layer to its base (a layer is drawn on its own figure, at the same place and scale)"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


for _g in (f7diag, f7in, f7move, f7many, f7par, f7par2, f7part, f7g68, f7g68b, f7g69, f7g69b, f7g70, f7g70b, f7g70c): f7_pin(_g)

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
