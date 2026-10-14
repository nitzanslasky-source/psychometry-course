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
# Topic-32 advanced block, part 2 (fragment f8, 2026-10-14): geo32-g071, geo32-g072, r26-t32-perimeter, q-r26-t32-06,
# q-r26-t32-07 (Hebrew geo 3272-3443 for g071 and g072; the perimeter lesson and its two questions are course additions).
# Question figure on the left (FIG_LEFT), our colour copy of it on the right, built step by step (Rule V3).
# =================================================================================================================
FIG_LEFT.update({'solve-geo32-g071', 'solve-geo32-g072', 'solve-q-r26-t32-06', 'solve-q-r26-t32-07'})


def f8_pin(g):
    """a figure whose later layers may come after other board items: the base is the figure, the layers draw on it"""
    base = g['line']; base['fig'] = base['_name']
    for k, it in g.items():
        if k != 'line': it['of'] = base['_name']
    return g


# ------------------------------------------------------------------------------------------------ geo32-g071 (Hebrew: the bisector in a general quadrilateral)
# Hebrew (geo 3272-3367): what makes it hard (through the quadrilateral to D, halve it, then triangle AED, all with letters,
# in under a minute, second-to-last question); the full math (360, isolate D, halve, triangle AED, cross out choices as
# the number and the beta term appear); then plugging in (choose numbers that look like the drawing, put them in the
# drawing AND in the answers; the drawback: cross out the others to be sure; "if time runs out, a reasonable guess");
# which way for whom. English: angle B = 130 (Hebrew 90); plug-in alpha = 110, beta = 80 (they look like the drawing).
# V3: the quadrilateral traced with its four angles; D marked "?"; the bisector DE drawn with two equal arcs at D; FOCUS on
# triangle AED (tinted, the rest dimmed) with x in red. Method 2 on a new copy: the chosen numbers written on the figure,
# D, its halves and x written as they are found.
f8A, f8B, f8C, f8D, f8E = (238.889, 293.556), (433.556, 293.556), (489.039, 141.117), (167.126, 72.692), (412.42, 293.556)
f8_71base = [('seg', *f8A, *f8B), ('seg', *f8B, *f8C), ('seg', *f8C, *f8D), ('seg', *f8D, *f8A), ('seg', *f8D, *f8E),
             ('txt', 222, 312, 'A', 'ink', 24, True), ('txt', 452, 312, 'B', 'ink', 24, True), ('txt', 510, 132, 'C', 'ink', 24, True),
             ('txt', 150, 56, 'D', 'ink', 24, True), ('txt', 412, 318, 'E', 'ink', 24, True)]
f8_aA = gdir(*f8A, *f8D); f8_aCB = gdir(*f8C, *f8B); f8_aCD = gdir(*f8C, *f8D); f8_aBC = gdir(*f8B, *f8C)
f8_aDA = gdir(*f8D, *f8A); f8_aDE = gdir(*f8D, *f8E); f8_aDC = gdir(*f8D, *f8C); f8_aED = gdir(*f8E, *f8D)
f8g71 = f8_pin(GEO('f8g71', [
    ('line', f8_71base),
    ('quad', [('path', [f8A, f8B, f8C, f8D, f8A], 'teal', 6),
              ('arc', *f8A, 30, 0, f8_aA, 'small', 'α', 50), ('arc', *f8B, 30, f8_aBC, 180, 'large', '130°', 58),
              ('arc', *f8C, 30, f8_aCD, f8_aCB, 'small', 'β', 50), ('arc', *f8D, 30, f8_aDA, f8_aDC, 'large', '?', 50)]),
    ('half', [('seg', *f8D, *f8E, 'teal', 4), ('arc', *f8D, 44, f8_aDA, f8_aDE, 'small'), ('arc', *f8D, 50, f8_aDE, f8_aDC, 'small'),
              ('arc', *f8D, 54, f8_aDE, f8_aDC, 'small')]),
    ('aed', [('dim', 140, 40, 400, 290), ('tint', [f8A, f8E, f8D], 'teal'), ('path', [f8A, f8E, f8D, f8A], 'teal', 5),
             ('txt', 222, 312, 'A', 'ink', 24, True), ('txt', 412, 318, 'E', 'ink', 24, True), ('txt', 150, 56, 'D', 'ink', 24, True),
             ('arc', *f8A, 30, 0, f8_aA, 'small', 'α', 50), ('arc', *f8D, 44, f8_aDA, f8_aDE, 'small', '½D', 66),
             ('arc', *f8E, 26, f8_aED, 180, 'red', 'x', 44)]),
], vb='130 30 410 300', w=360, title='Quadrilateral ABCD with the bisector DE'))
f8n1 = I('f8n1', '$\\angle D=230°-\\alpha-\\beta$', size=28)
f8n2 = I('f8n2', '$\\angle ADE=115°-\\frac\\alpha2-\\frac\\beta2$', size=28)
f8n3 = I('f8n3', '$x=180°-\\alpha-\\left(115°-\\frac\\alpha2-\\frac\\beta2\\right)$', size=28)
f8n4 = I('f8n4', '$x=65°-\\frac\\alpha2+\\frac\\beta2$', size=30)
f8g71b = f8_pin(GEO('f8g71b', [
    ('line', f8_71base),
    ('nums', [('arc', *f8A, 30, 0, f8_aA, 'orange', '110°', 54), ('arc', *f8B, 30, f8_aBC, 180, 'large', '130°', 58),
              ('arc', *f8C, 30, f8_aCD, f8_aCB, 'small', '80°', 54)]),
    ('d', [('arc', *f8D, 30, f8_aDA, f8_aDC, 'large', '40°', 52)]),
    ('halves', [('seg', *f8D, *f8E, 'teal', 4), ('txt', 330, 70, 'each half: 20°', 'small', 24)]),
    ('x', [('arc', *f8E, 26, f8_aED, 180, 'red', '50°', 48)]),
], vb='130 30 410 300', w=360, title='The same figure with alpha = 110 and beta = 80'))
f8p0 = I('f8p0', '$\\frac\\alpha2=55,\\ \\ \\frac\\beta2=40$, $\\ $we need $\\ 50$', size=28)
f8p3 = I('f8p3', '(1) $65+55-40=80$ ✗', size=28)
f8p6 = I('f8p6', '(2) $130+55-40=145$ ✗', size=28)
f8p4 = I('f8p4', '(3) $65-55+40=50$ ✓', size=28)
f8p5 = I('f8p5', '(4) $130-55+40=115$ ✗', size=28)
video('solve-geo32-g071', 'solution', qid='geo32-g071', slides=[
    SM('Method 1 · Algebra', 'The plan',
      L("In quadrilateral A B C D, angle A is alpha, angle B is a hundred thirty degrees, and angle C is beta. E lies on A B, "
        "and D E bisects angle A D C. Which expression equals angle A E D?", pt('stem', 'In quadrilateral A B C D', 'hl', 9.0),
        voice='calm', pause=0.5),
      L("What makes this hard? We have to go through the whole quadrilateral to find angle D, cut it in half, and then work "
        "in triangle A E D. And all of it with letters, in about a minute, when it's one of the last questions in the "
        "section. [short pause] We'll solve it two ways, with the full algebra, and then by plugging in numbers.",
        pt('fig: x', 'triangle A E D')),
      L("[short pause] Here's the plan on the figure. The four angles of the quadrilateral add up to three hundred sixty "
        "degrees, and only angle D is missing.", show(f8g71['line'], "Here's the plan on the figure"),
        show(f8g71['quad'], 'The four angles of the quadrilateral')),
      L("D E bisects angle D, so it cuts it into two equal halves.", show(f8g71['half'], 'D E bisects angle D')),
      L("And x is an angle of triangle A E D, whose angles add up to a hundred eighty. Its other two angles are alpha and "
        "half of angle D.", show(f8g71['aed'], 'And x is an angle of triangle A E D'))),
    SM('Method 1 · Algebra', 'The algebra',
      L("Now the algebra. Angle D plus alpha plus a hundred thirty plus beta is three hundred sixty. Three hundred sixty "
        "minus a hundred thirty is two hundred thirty. So angle D is two hundred thirty, minus alpha, minus beta.",
        show(f8n1, 'So angle D is two hundred thirty')),
      L("Half of two hundred thirty is a hundred fifteen. So each half, angle A D E, is a hundred fifteen, minus half alpha, "
        "minus half beta.", show(f8n2, 'So each half')),
      L("In triangle A E D, x is a hundred eighty, minus alpha, minus the whole bracket, a hundred fifteen minus half alpha "
        "minus half beta.", show(f8n3, 'In triangle A E D')),
      L("A hundred eighty minus a hundred fifteen is sixty-five. So the number in the answer is sixty-five, and choice "
        "numbers two and four are out, because they have a hundred thirty. The minus in front of the bracket turns minus "
        "half beta into plus half beta, so choice number one is out too. And minus alpha plus half alpha leaves minus half "
        "alpha. So x is sixty-five, minus half alpha, plus half beta. Choice number three is our answer.",
        mk('cross', 'choice 2', 'choice numbers two and four are out'), mk('cross', 'choice 4', 'because they have a hundred thirty'),
        mk('cross', 'choice 1', 'so choice number one is out too'), show(f8n4, 'So x is sixty-five'),
        mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Plugging in numbers', 'Plug in numbers',
      L("[pause] That was long and tiring. Now a shorter way: plugging in numbers. The right answer has to be true for "
        "every alpha and beta that the drawing allows. So it must also be true for one example that we choose. We choose "
        "easy numbers that look like the drawing, put them in the drawing and in the choices, and keep the choice that "
        "matches.", show(f8g71b['line'], 'Now a shorter way')),
      L("Alpha looks obtuse, so let's take a hundred ten. Beta looks a little less than ninety, so let's take eighty. You "
        "could choose other numbers too, as long as they fit the drawing.", show(f8g71b['nums'], 'so let\'s take a hundred ten')),
      L("Angle D: a hundred ten plus a hundred thirty plus eighty is three hundred twenty. Three hundred sixty minus three "
        "hundred twenty is forty. D E cuts it in half, so each half is twenty.", show(f8g71b['d'], 'Three hundred sixty minus three'),
        show(f8g71b['halves'], 'so each half is twenty')),
      L("Now x is easy. In triangle A E D, a hundred ten plus twenty is a hundred thirty, and a hundred eighty minus a hundred "
        "thirty is fifty. So with these numbers, x is fifty degrees.", show(f8g71b['x'], 'So with these numbers'))),
    SM('Method 2 · Plugging in numbers', 'Check the choices',
      L("Now we put alpha a hundred ten and beta eighty into each choice. Half alpha is fifty-five, and half beta is forty. "
        "Choice number one: sixty-five plus fifty-five minus forty is eighty. Not fifty, out. Choice number two: a hundred "
        "thirty plus fifty-five minus forty is a hundred forty-five. Out.", show(f8p0, 'Now we put alpha'), show(f8p3, 'Choice number one'), show(f8p6, 'Choice number two'),
        mk('cross', 'choice 1', 'Not fifty, out'), mk('cross', 'choice 2', 'is a hundred forty-five. Out')),
      L("Choice number three: sixty-five minus fifty-five plus forty is fifty. It matches. But one match isn't enough to be "
        "sure: to mark it, we cross out the other choices too. That's the drawback of plugging in. If you're out of time, "
        "though, it's a very reasonable guess.", show(f8p4, 'Choice number three'), pt('choice 3', 'It matches')),
      L("Choice number four: a hundred thirty minus fifty-five plus forty is a hundred fifteen. Out. So choice number three "
        "is our answer.", show(f8p5, 'Choice number four'), mk('cross', 'choice 4', 'is a hundred fifteen. Out'),
        mk('tick', 'choice 3', 'So choice number three is our answer')),
      L("If you're strong in algebra and can do the full solution in about a minute, that's great. For most students, at "
        "the end of a section, plugging in numbers is much easier. [pause] Okay. I'll see you in the next question.",
        pt('f8p4', 'plugging in numbers is much easier'))),
])

# ------------------------------------------------------------------------------------------------ geo32-g072 (Hebrew: five identical rectangles)
# Hebrew (geo 3398-3438): the main difficulty is to see the fixed ratio between the length and the width of a small
# rectangle, which comes from how they are put together; width x, the marked rectangle covers three x's (ratio 1:3); label
# every side; the perimeter in x; x = 2; "we weren't asked for x, it's not in the choices"; area = base times height.
# English: six rectangles, ratio 1:4, perimeter 40, area 96. Course addition kept: the sides as a ratio 2:3 of half the
# perimeter. (The old "check from the answers" view is dropped: it re-solves the same equation.)
# V3: one stacked rectangle tinted, its short side x; the four x's up the stack; a standing rectangle tinted orange with
# its long side "4x" next to the stack; every side labelled (4x, x + 4x + x = 6x); values 8 and 12 written on the sides.
f8L, f8R, f8T, f8Bt = 174.0, 466.0, 82.667, 277.333
f8x1, f8x2 = 222.667, 417.333
f8_72base = [('seg', f8L, f8T, f8R, f8T), ('seg', f8R, f8T, f8R, f8Bt), ('seg', f8R, f8Bt, f8L, f8Bt), ('seg', f8L, f8Bt, f8L, f8T),
             ('seg', f8x1, f8T, f8x1, f8Bt), ('seg', f8x2, f8T, f8x2, f8Bt)] + \
            [('seg', f8x1, y, f8x2, y) for y in (131.333, 180.0, 228.667)] + \
            [('txt', 158, 66, 'A', 'ink', 24, True), ('txt', 158, 296, 'B', 'ink', 24, True),
             ('txt', 482, 296, 'C', 'ink', 24, True), ('txt', 482, 66, 'D', 'ink', 24, True)]
f8g72 = f8_pin(GEO('f8g72', [
    ('line', f8_72base),
    ('one', [('tint', [(f8x1, 228.667), (f8x2, 228.667), (f8x2, f8Bt), (f8x1, f8Bt)], 'teal'), ('txt', 392, 253, 'x', 'teal', 24, True)]),
    ('stack', [('txt', 392, 107, 'x', 'teal', 24, True), ('txt', 392, 156, 'x', 'teal', 24, True), ('txt', 392, 204, 'x', 'teal', 24, True)]),
    ('stand', [('tint', [(f8L, f8T), (f8x1, f8T), (f8x1, f8Bt), (f8L, f8Bt)], 'orange'), ('txt', 198, 180, '4x', 'orange', 24, True),
               ('txt', 198, 296, 'x', 'teal', 22, True)]),
    ('sides', [('txt', 140, 180, '4x', 'ink', 26, True), ('txt', 320, 300, 'x + 4x + x = 6x', 'ink', 22, True)]),
], vb='110 40 420 280', w=400, title='Rectangle ABCD made of six congruent rectangles'))
f8g72c = f8_pin(GEO('f8g72c', [
    ('line', f8_72base + [('txt', 140, 180, '4x', 'ink', 26, True), ('txt', 320, 300, '6x', 'ink', 24, True)]),
    ('vals', [('txt', 140, 214, '= 8', 'red', 24), ('txt', 320, 66, '6x = 12', 'red', 24)]),
], vb='110 40 420 280', w=250, title='Rectangle ABCD: the sides 4x and 6x'))
f8r2 = I('f8r2', '$P=2(4x+6x)=20x=40\\ \\Rightarrow\\ x=2$', size=28)
f8r2b = I('f8r2b', '$4x=8,\\ \\ 6x=12$', size=30)
f8r3 = I('f8r3', '$S=4x\\cdot6x=8\\cdot12=96$', size=30)
f8r4 = I('f8r4', 'sides $4x:6x=2:3$, $\\ $half the perimeter $20$', size=26)
f8r5 = I('f8r5', '$20\\div5=4$: $\\ 2\\cdot4=8,\\ \\ 3\\cdot4=12$', size=28)
video('solve-geo32-g072', 'solution', qid='geo32-g072', slides=[
    SM('Method 1 · The hidden ratio', 'The hidden ratio',
      L("Rectangle A B C D consists of six congruent rectangles, arranged as in the accompanying figure. The perimeter of A B "
        "C D is forty centimeters. What is its area, in square centimeters?", pt('stem', 'Rectangle A B C D', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("The main difficulty here is to see that each small rectangle has a fixed ratio between its long side and its short "
        "side. That ratio comes from the way the six rectangles fit together. [short pause] We'll find the ratio first, and "
        "then the perimeter and the area.", pt('stem', 'a fixed ratio')),
      L("[short pause] Call the short side of a small rectangle x. Look at one of the lying rectangles in the middle. Its "
        "short side is x. All six are the same, so each of the four lying rectangles is x high.",
        show(f8g72['line'], 'Call the short side'), show(f8g72['one'], 'Look at one of the lying rectangles'),
        show(f8g72['stack'], 'each of the four lying rectangles')),
      L("Now look at a standing rectangle on the side. Its long side is as tall as the four lying rectangles together, four "
        "x's. So the long side is four x, and the ratio is one to four.", show(f8g72['stand'], 'Now look at a standing rectangle')),
      L("Now every side of A B C D. The height is four x. Across, there's x, then four x, then x again, so the width is six x.",
        show(f8g72['sides'], 'Now every side of A B C D'))),
    SM('Method 1 · The hidden ratio', 'Perimeter and area',
      L("The perimeter is two times, four x plus six x, which is twenty x. It's forty, so x is two.", show(f8r2, 'The perimeter is two times')),
      L("Careful, nobody asked for x, and two isn't even a choice. They asked for the area. Base times height: four x is "
        "eight, and six x is twelve. Eight times twelve is ninety-six. Choice number three is our answer.",
        show(f8r2b, 'four x is eight'), show(f8r3, 'Eight times twelve'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    SM('Method 2 · Parts of the perimeter', 'Parts of the perimeter',
      L("[pause] Once we have the sides as four x and six x, there's a shorter way to finish. The sides are in the ratio two "
        "to three. Half the perimeter, one height plus one width, is twenty.", show(f8r4, 'The sides are in the ratio two')),
      L("Two parts plus three parts is five parts, and five parts are twenty, so one part is four. The sides are two times "
        "four, eight, and three times four, twelve. Eight times twelve is ninety-six again. [pause] Okay. I'll see you in "
        "the next question.", show(f8r5, 'one part is four'), mk('tick', 'choice 3', 'is ninety-six again'))),
])

# ------------------------------------------------------------------------------------------------ r26-t32-perimeter (lesson, course addition)
# Two perimeter tricks, each with two examples and a non-example: a cut is counted twice (the pieces' perimeters add up to
# the original plus twice each cut); a notch adds twice its depth (a corner step adds nothing, preview of the staircase).
# V3: a generic 10 x 6 rectangle; the cut drawn dashed as named, each piece tinted in its own colour; the cut traced red
# twice ("it belongs to both"); the notch: its bottom pushed up (dashed arrows), the two walls in orange as "extra".
f8u = 36   # px per unit; rectangle 10 x 6 at (140, 60)
f8X0, f8Y0 = 140, 60
f8_rect = [('seg', f8X0, f8Y0, f8X0 + 10 * f8u, f8Y0), ('seg', f8X0 + 10 * f8u, f8Y0, f8X0 + 10 * f8u, f8Y0 + 6 * f8u),
           ('seg', f8X0 + 10 * f8u, f8Y0 + 6 * f8u, f8X0, f8Y0 + 6 * f8u), ('seg', f8X0, f8Y0 + 6 * f8u, f8X0, f8Y0),
           ('txt', f8X0 + 5 * f8u, f8Y0 - 18, '10', 'ink', 26), ('txt', f8X0 - 22, f8Y0 + 3 * f8u, '6', 'ink', 26)]
f8cx = f8X0 + 4 * f8u
f8cut = f8_pin(GEO('f8cut', [
    ('line', f8_rect),
    ('cut', [('seg', f8cx, f8Y0, f8cx, f8Y0 + 6 * f8u, 'teal', 4, True)]),
    ('pieces', [('tint', [(f8X0, f8Y0), (f8cx, f8Y0), (f8cx, f8Y0 + 6 * f8u), (f8X0, f8Y0 + 6 * f8u)], 'teal'),
                ('tint', [(f8cx, f8Y0), (f8X0 + 10 * f8u, f8Y0), (f8X0 + 10 * f8u, f8Y0 + 6 * f8u), (f8cx, f8Y0 + 6 * f8u)], 'orange'),
                ('txt', f8X0 + 2 * f8u, f8Y0 + 3 * f8u, '4 × 6', 'teal', 26), ('txt', f8X0 + 7 * f8u, f8Y0 + 3 * f8u, '6 × 6', 'orange', 26)]),
    ('twice', [('seg', f8cx - 5, f8Y0 + 4, f8cx - 5, f8Y0 + 6 * f8u - 4, 'red', 5), ('seg', f8cx + 5, f8Y0 + 4, f8cx + 5, f8Y0 + 6 * f8u - 4, 'red', 5),
               ('txt', f8cx, f8Y0 + 6 * f8u + 26, 'counted twice', 'red', 22)]),
], vb='90 20 470 300', w=600, col=0, title='A 10 by 6 rectangle cut into two'))
f8c1 = I('f8c1', '$P_1+P_2=20+24=44$', size=30)
f8c2 = I('f8c2', '$44=32+2\\cdot6$', size=30)
f8c3 = I('f8c3', 'Cut across: $\\ 24+28=52=32+2\\cdot10$', size=28)
f8c4 = I('f8c4', 'Pieces $=$ original $+\\ 2\\times$ each cut', size=28)
f8ny = f8Y0 + 2 * f8u; f8n1x, f8n2x = f8X0 + 4 * f8u, f8X0 + 7 * f8u
f8notch = f8_pin(GEO('f8notch', [
    ('line', [('seg', f8X0, f8Y0, f8n1x, f8Y0), ('seg', f8n1x, f8Y0, f8n1x, f8ny), ('seg', f8n1x, f8ny, f8n2x, f8ny),
              ('seg', f8n2x, f8ny, f8n2x, f8Y0), ('seg', f8n2x, f8Y0, f8X0 + 10 * f8u, f8Y0),
              ('seg', f8X0 + 10 * f8u, f8Y0, f8X0 + 10 * f8u, f8Y0 + 6 * f8u), ('seg', f8X0 + 10 * f8u, f8Y0 + 6 * f8u, f8X0, f8Y0 + 6 * f8u),
              ('seg', f8X0, f8Y0 + 6 * f8u, f8X0, f8Y0), ('txt', f8X0 + 5 * f8u, f8Y0 + 6 * f8u + 26, '10', 'ink', 26),
              ('txt', f8X0 - 22, f8Y0 + 3 * f8u, '6', 'ink', 26)]),
    ('up', [('seg', f8n1x, f8ny, f8n2x, f8ny, 'teal', 5), ('seg', f8n1x, f8Y0, f8n2x, f8Y0, 'teal', 4, True),
            ('seg', f8n1x + 54, f8ny - 8, f8n1x + 54, f8Y0 + 10, 'teal', 2.5, True), ('txt', (f8n1x + f8n2x) / 2, f8ny + 26, 'push up', 'teal', 22)]),
    ('walls', [('seg', f8n1x, f8Y0, f8n1x, f8ny, 'orange', 6), ('seg', f8n2x, f8Y0, f8n2x, f8ny, 'orange', 6),
               ('txt', f8n1x - 30, f8Y0 + f8u, '2', 'orange', 24), ('txt', f8n2x + 26, f8Y0 + f8u, '2', 'orange', 24)]),
], vb='90 20 470 300', w=600, col=0, title='A 10 by 6 rectangle with a notch 2 deep'))
f8t1 = I('f8t1', '$P=32+2\\cdot2=36$', size=30)
f8t2 = I('f8t2', 'Depth $3$: $\\ P=32+2\\cdot3=38$', size=28)
f8t3 = I('f8t3', 'A step at a corner: $\\ P=32$ (nothing extra)', size=28)
video('r26-t32-perimeter', 'lesson', slides=[
    S('Perimeter Tricks',
      L("Perimeter tricks. Two quick rules that turn long perimeter questions into one line, and a third one in the next "
        "question.")),
    S('A cut counts twice',
      L("Here's a rectangle, ten by six. Its perimeter is two times, ten plus six, which is thirty-two. Now cut it into two "
        "smaller rectangles, four by six and six by six.", show(f8cut['line'], "Here's a rectangle"), show(f8cut['cut'], 'Now cut it'),
        show(f8cut['pieces'], 'four by six and six by six')),
      L("The perimeter of the first piece is two times, four plus six, twenty. The second is two times, six plus six, "
        "twenty-four. Together, forty-four. That's more than thirty-two. Why?", show(f8c1, 'Together, forty-four')),
      L("Every outside side is counted once, just like before. But the cut is a side of both pieces, so it's counted twice. "
        "The cut is six, so the pieces add up to thirty-two plus two times six, forty-four.",
        show(f8cut['twice'], 'so it\'s counted twice'), show(f8c2, 'the pieces add up to thirty-two')),
      L("Cut the same rectangle across instead, into ten by two and ten by four. Twenty-four plus twenty-eight is fifty-two, "
        "and that's thirty-two plus two times ten, because this cut is ten long. So the rule: the pieces add up to the "
        "original perimeter plus two times each cut.", show(f8c3, 'Cut the same rectangle across'), show(f8c4, 'So the rule'))),
    S('A notch adds',
      L("Now a notch: the border goes into the shape and comes back out. Here the notch is two deep. Push the bottom of the "
        "notch up to the top line, and the width is still covered, ten, just like the plain rectangle.",
        show(f8notch['line'], 'Now a notch'), show(f8notch['up'], 'Push the bottom of the notch up')),
      L("But the two walls of the notch have nowhere to go. They are extra. Each one is two, so the perimeter is thirty-two "
        "plus two times two, thirty-six. A notch three deep would add six, so thirty-eight.",
        show(f8notch['walls'], 'But the two walls'), show(f8t1, 'thirty-two plus two times two'), show(f8t2, 'A notch three deep')),
      L("Careful, a step cut out at a corner is not a notch. Its two sides can both be pushed out to the border, so it adds "
        "nothing. You'll see that in the next question. [pause] Okay. I'll see you in the next video.",
        show(f8t3, 'a step cut out at a corner'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t32-06 (course addition: the staircase)
# Push every horizontal step up to the top line and every vertical step out to the side: no length changes, the outline
# becomes the 12 by 8 rectangle. Traps: "cannot be determined" and 96 (the area).
# V3: the horizontal steps traced teal, then shown pushed up onto the top line (dashed arrows), "12"; the vertical steps
# traced orange, then pushed out to the right side, "8"; the full rectangle traced, P = 40 written.
f8H = [((130, 60), (220, 60)), ((220, 90), (310, 90)), ((310, 150), (400, 150)), ((400, 210), (490, 210))]
f8V = [((220, 60), (220, 90)), ((310, 90), (310, 150)), ((400, 150), (400, 210)), ((490, 210), (490, 300))]
f8_06base = [('seg', 130, 300, 490, 300), ('seg', 130, 60, 130, 300)] + [('seg', *p, *q) for p, q in f8H + f8V] + \
            [('txt', 310, 325, '12', 'ink', 26), ('txt', 108, 180, '8', 'ink', 26)]
f8g06 = f8_pin(GEO('f8g06', [
    ('line', f8_06base),
    ('h', [('seg', *p, *q, 'teal', 6) for p, q in f8H]),
    ('hup', [('dim', 90, 30, 470, 305)] + [('seg', p[0], 60, q[0], 60, 'teal', 6) for p, q in f8H] +
            [('seg', (p[0] + q[0]) / 2, p[1] - 4, (p[0] + q[0]) / 2, 66, 'teal', 2.5, True) for p, q in f8H[1:]] +
            [('txt', 310, 44, '12', 'teal', 26)]),
    ('v', [('seg', *p, *q, 'orange', 6) for p, q in f8V]),
    ('vout', [('seg', 490, p[1], 490, q[1], 'orange', 6) for p, q in f8V] +
             [('seg', p[0] + 4, (p[1] + q[1]) / 2, 484, (p[1] + q[1]) / 2, 'orange', 2.5, True) for p, q in f8V[:3]] +
             [('txt', 514, 180, '8', 'orange', 26)]),
    ('rect', [('path', [(130, 60), (490, 60), (490, 300), (130, 300), (130, 60)], 'teal', 4)]),
], vb='90 30 470 305', w=360, title='The staircase figure'))
f8s1 = I('f8s1', '$P=2(12+8)=40$', size=32)
video('solve-q-r26-t32-06', 'solution', qid='q-r26-t32-06', slides=[
    SM('Push the steps out', 'Push the steps out',
      L("All the angles in the accompanying figure are right angles. The figure is twelve centimeters wide and eight "
        "centimeters tall, as marked. What is its perimeter, in centimeters?", pt('stem', 'All the angles', 'hl', 8.0),
        voice='calm', pause=0.5),
      L("We don't know the length of a single step, so many students choose cannot be determined. But this is a staircase, "
        "and a staircase only has to be pushed. [short pause] Let's see why.", pt('choice 4', 'cannot be determined')),
      L("[short pause] Look at all the horizontal steps. Push each one straight up to the top line. Together they cover the "
        "whole top, from the left side to the right side. That's twelve.", show(f8g06['line'], 'Look at all the horizontal steps'),
        show(f8g06['h'], 'Look at all the horizontal steps'), show(f8g06['hup'], 'Push each one straight up')),
      L("Now the vertical steps. Push each one out to the right side. Together they cover the whole right side, from top to "
        "bottom. That's eight.", show(f8g06['v'], 'Now the vertical steps'), show(f8g06['vout'], 'Push each one out')),
      L("No length changed. So the perimeter is the same as the full rectangle's: two times, twelve plus eight, which is "
        "forty. Choice number two is our answer.", show(f8g06['rect'], 'No length changed'), show(f8s1, 'two times, twelve plus eight'),
        mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Careful, ninety-six is twelve times eight. That's an area, not a perimeter. [pause] Okay. I'll see you in the next "
        "question.", mk('cross', 'choice 3', 'ninety-six is twelve times eight'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t32-07 (course addition)
# Method 1: a + b = 17 and a² + b² = 169; the shortcut formula (a + b)² = a² + 2ab + b² (topic 4) gives 2ab = 120, ab = 60.
# Method 2: 13 suggests the triple 5, 12, 13; sides 5 and 12 fit the perimeter too; the question has one area, so 60.
# Traps: 120 (2ab), 30 (half), 65 (the diagonal as a side).
# V3: a and b written on two sides; the half perimeter traced (top + left); triangle ABC tinted with the diagonal orange
# and the right angle at B; method 2 on a new copy: 5 and 12 written on the sides.
f8a, f8b, f8c, f8d = (150, 90), (150, 270), (490, 270), (490, 90)
f8_07base = [('seg', *f8a, *f8b), ('seg', *f8b, *f8c), ('seg', *f8c, *f8d), ('seg', *f8d, *f8a), ('seg', *f8a, *f8c),
             ('txt', 134, 74, 'A', 'ink', 24, True), ('txt', 134, 288, 'B', 'ink', 24, True), ('txt', 506, 288, 'C', 'ink', 24, True),
             ('txt', 506, 74, 'D', 'ink', 24, True), ('txt', 330, 160, '13', 'ink', 24)]
f8g07 = f8_pin(GEO('f8g07', [
    ('line', f8_07base),
    ('ab', [('txt', 126, 180, 'b', 'teal', 28, True), ('txt', 320, 296, 'a', 'teal', 28, True)]),
    ('half', [('path', [(150, 90), (150, 270), (490, 270)], 'teal', 6), ('txt', 250, 245, 'a + b = 17', 'teal', 26)]),
    ('tri', [('tint', [f8a, f8b, f8c], 'teal'), ('seg', *f8a, *f8c, 'orange', 5), ('right', 150, 270, 0, 90, 14),
             ('txt', 405, 125, 'a² + b² = 169', 'orange', 26)]),
], vb='100 50 440 270', w=380, title='Rectangle ABCD with the diagonal AC'))
f8e1 = I('f8e1', '$a+b=17\\qquad a^2+b^2=169$', size=30)
f8e2 = I('f8e2', '$(a+b)^2=a^2+2ab+b^2$', size=30)
f8e3 = I('f8e3', '$289=169+2ab\\ \\Rightarrow\\ 2ab=120,\\ \\ ab=60$', size=28)
f8g07b = f8_pin(GEO('f8g07b', [
    ('line', f8_07base),
    ('sides', [('txt', 126, 180, '5', 'teal', 28), ('txt', 320, 296, '12', 'teal', 28)]),
    ('perim', [('txt', 405, 125, 'P = 2(5 + 12) = 34 ✓', 'teal', 24)]),
    ('area', [('tint', [f8a, f8b, f8c, f8d], 'orange'), ('txt', 250, 235, 'S = 5 · 12 = 60', 'orange', 26)]),
], vb='100 50 440 270', w=380, title='Sides 5 and 12'))
video('solve-q-r26-t32-07', 'solution', qid='q-r26-t32-07', slides=[
    SM('Method 1 · A shortcut formula', 'A shortcut formula',
      L("A rectangle has a perimeter of thirty-four centimeters, and its diagonal is thirteen centimeters long. What is its "
        "area, in square centimeters?", pt('stem', 'A rectangle has a perimeter', 'hl', 7.0), voice='calm', pause=0.5),
      L("We know the perimeter and the diagonal, but not the sides. [short pause] We'll solve it two ways, with a shortcut "
        "formula, and then with a Pythagorean triple."),
      L("[short pause] Call the sides a and b. Half the perimeter is one a and one b, so a plus b is seventeen.",
        show(f8g07['line'], 'Call the sides a and b'), show(f8g07['ab'], 'Call the sides a and b'), show(f8g07['half'], 'Half the perimeter')),
      L("The diagonal makes a right triangle with two sides of the rectangle. By Pythagoras, a squared plus b squared is "
        "thirteen squared, a hundred sixty-nine.", show(f8g07['tri'], 'The diagonal makes a right triangle'))),
    SM('Method 1 · A shortcut formula', 'The shortcut formula',
      L("We want the area, a times b. Here a shortcut formula from expressions helps: the bracket a plus b, squared, is a "
        "squared plus two a b plus b squared.", show(f8e1, 'We want the area'), show(f8e2, 'Here a shortcut formula')),
      L("Seventeen squared is seventeen times seventeen: a hundred seventy plus a hundred nineteen, two hundred eighty-nine. "
        "So two hundred eighty-nine is a hundred sixty-nine plus two a b. Two a b is a hundred twenty, and the area, a b, is "
        "sixty. Choice number one is our answer.", show(f8e3, 'So two hundred eighty-nine'),
        mk('tick', 'choice 1', 'Choice number one is our answer'))),
    SM('Method 2 · A triple', 'A triple',
      L("[pause] Another way. A diagonal of thirteen should remind us of the triple five, twelve, thirteen. Let's try sides "
        "five and twelve: their diagonal is thirteen.", show(f8g07b['line'], 'Another way'), show(f8g07b['sides'], "Let's try sides")),
      L("Now check the other given, the perimeter: two times, five plus twelve, is thirty-four. It fits both givens. The "
        "question has only one area, so it's five times twelve, sixty. Choice number one again.",
        show(f8g07b['perim'], 'Now check the other given'), show(f8g07b['area'], 'five times twelve, sixty'), mk('tick', 'choice 1', 'Choice number one again')),
      L("The traps: a hundred twenty is two a b, without dividing by two. Thirty is half the rectangle. And sixty-five uses "
        "the diagonal as if it were a side. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 3', 'a hundred twenty is two a b'), mk('cross', 'choice 4', 'Thirty is half the rectangle'),
        mk('cross', 'choice 2', 'sixty-five uses the diagonal'))),
])


# typed lines of the question videos: the right column, under the colour copy (the left column is the question figure)
def f8_col(y0, *items, dy=54):
    for k, it in enumerate(items): _R(it, y0 + k * dy)


_R(f8g71, 222); _R(f8g71b, 222); _R(f8g72, 222); _R(f8g06, 222); _R(f8g07, 222); _R(f8g07b, 222)
f8_col(230, f8n1, f8n2, f8n3, f8n4, dy=62)
f8_col(226, f8p0, f8p3, f8p6, f8p4, f8p5, dy=52)
f8_col(240, f8r2, f8r2b, f8r3, dy=62)
f8_col(250, f8r4, f8r5, dy=60)
f8_col(470, f8s1)
f8_col(240, f8e1, f8e2, f8e3, dy=62)

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
