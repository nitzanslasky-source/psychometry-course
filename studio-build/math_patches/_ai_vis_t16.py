"""Topic 16 (Integers) - the redo for the teacher's own-voice reading (2026-10-11), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t14.py / _ai_vis_t15.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The teacher records only the camera lesson 'whole-numbers' (re-record, never touched here). Every other topic-16 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t16.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t16.py ai_redo_t16() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-16-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t16ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-16 flow order of the scripts (whole-numbers = the camera lesson, not here)
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
            'style': "the teacher reads it herself (Reading Studio), topic-16 redo (2026-10-11): math_patches/_ai_vis_t16.py is "
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



# ------------------------------------------------------------------------------------------- topic-14 figures
# Both figures are BUILT in layers at the spoken words (like DIST in topic 13): every layer is a figure item of the same
# size drawn at the same place (over=1), shown in order. Labels are big and bold (about the size of the handwriting).
def _svg(vb, body, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, title, title, body))


LAYER_BASE = {}     # a figure layer's item name -> its base item's name (a POINT on a layer lights nothing visible)


def _layers(name, out, w, col):
    items = {}
    base = '%s_%s' % (name, out[0][0])
    for k, sv in out:
        it = NL('%s_%s' % (name, k), sv, w=w, col=col)
        if k != 'line' and k != 'root': it['over'] = 1; it['gap'] = 0; LAYER_BASE[it['_name']] = base
        items[k] = it
    return items


RED = '#d62d48'


def STRIP(name, lo, hi, layers, base=(), w=1060, col=0):
    """a number strip from lo to hi: a short tick at EVERY whole number, a label under each number in `base`.
    layers = [(key, [mark, ...]), ...] drawn on top, in order. Marks:
      ('prime', v)          a teal dot on v and a bold teal label (a prime)
      ('lab', v)            a label under v (ink)
      ('cross', v)          a red cross over v's label (ruled out)
      ('ring', v)           a teal ring around v's label (the pick)
      ('span', a, b, text)  a teal bracket above the line from a to b, with text above it
    -> {key: item}; show them in order (the base line is key 'line')."""
    L_, R_, Y_ = 30, 610, 70
    X = lambda v: L_ + 14 + (v - lo) / float(hi - lo) * (R_ - L_ - 28)
    INK, TEAL, FONT = SNL.INK, SNL.TEAL, SNL.FONT
    lab = lambda v, col_, fw='bold': ('<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="19" font-weight="%s">%d</text>'
                                     % (X(v), Y_ + 32, col_, FONT, fw, v))
    body = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.5"/>' % (L_ - 6, Y_, R_ + 6, Y_, INK) +
            '<path d="M %d %d l 11 -6 l 0 12 Z" fill="%s"/>' % (L_ - 10, Y_, INK) + '<path d="M %d %d l -11 -6 l 0 12 Z" fill="%s"/>' % (R_ + 10, Y_, INK) +
            ''.join('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.6"/>' % (X(v), Y_ - 7, X(v), Y_ + 7, INK) for v in range(lo, hi + 1)) +
            ''.join(lab(v, INK) for v in base))
    out = [('line', _svg('0 10 640 112', body, 'Whole numbers from %d to %d' % (lo, hi)))]
    for key, marks in layers:
        b = ''
        for m in marks:
            if m[0] == 'prime':
                b += '<circle cx="%.1f" cy="%d" r="6" fill="%s"/>' % (X(m[1]), Y_, TEAL) + lab(m[1], TEAL)
            elif m[0] == 'lab':
                b += lab(m[1], INK)
            elif m[0] == 'cross':
                x0 = X(m[1]); b += ('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3"/>' % (x0 - 11, Y_ + 14, x0 + 11, Y_ + 38, RED) +
                                    '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3"/>' % (x0 + 11, Y_ + 14, x0 - 11, Y_ + 38, RED))
            elif m[0] == 'ring':
                b += '<rect x="%.1f" y="%d" width="30" height="28" rx="9" fill="none" stroke="%s" stroke-width="2.6"/>' % (X(m[1]) - 15, Y_ + 12, TEAL)
            elif m[0] == 'span':
                a, c = X(m[1]), X(m[2])
                b += ('<path d="M %.1f %d L %.1f %d L %.1f %d L %.1f %d" fill="none" stroke="%s" stroke-width="2.4"/>' % (a, Y_ - 12, a, Y_ - 22, c, Y_ - 22, c, Y_ - 12, TEAL) +
                      '<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="19" font-weight="bold">%s</text>' % ((a + c) / 2, Y_ - 30, TEAL, FONT, m[3]))
        out.append((key, _svg('0 10 640 112', b, key)))
    return _layers(name, out, w, col)


def TREE(name, root, steps, w=330, col=1, dx=92, dy=50):
    """a factor ladder: root at the top; step i splits the number on the right into (prime, rest) - the prime is circled
    at the lower left, the rest goes on down to the right (the last rest, a prime, is circled too). -> {'root': item,
    1: item, 2: item, ...}; show 'root' first, then the steps in order. Labels are plain digits."""
    INK, TEAL, FONT = SNL.INK, SNL.TEAL, SNL.FONT
    n = len(steps); x0, y0 = 92, 40
    W = x0 + n * dx + 70; H = y0 + n * dy + 34
    pos = lambda i: (x0 + i * dx, y0 + i * dy)
    def node(x, y, t, prime):
        s = '<text x="%.1f" y="%.1f" text-anchor="middle" fill="%s" %s font-size="30" font-weight="bold">%s</text>' % (x, y + 10, TEAL if prime else INK, FONT, t)
        if prime: s += '<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s" stroke-width="2.6"/>' % (x, y, 15 + 6 * (len(str(t)) - 1), TEAL)
        return s
    vb = '0 0 %d %d' % (W, H)
    out = [('root', _svg(vb, node(x0, y0, root, False), 'Factor tree of %s' % root))]
    for i, (p, rest) in enumerate(steps):
        (ax, ay), (bx, by) = pos(i), pos(i + 1)
        lx = ax - dx * 0.7; last = i == n - 1
        body = ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4"/>' % (ax - 10, ay + 22, lx + 6, by - 22, INK) +
                '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4"/>' % (ax + 10, ay + 22, bx - 6, by - 22, INK) +
                node(lx, by, p, True) + node(bx, by, rest, last))
        out.append((i + 1, _svg(vb, body, '%s splits into %s and %s' % (root if i == 0 else steps[i - 1][1], p, rest))))
    items = _layers(name, out, w, col)
    return items



# =================================================================================================================
# THE SCRIPTS (topic-16 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-16-AI-scripts-review.md.
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ q-457 (Q1)
# NEW: find the pieces that are surely positive, and the one piece left decides the sign; why "a is not 0" is given;
# the trap "b < 0" (we learn nothing about b's sign).  REMINDER: even powers and absolute values are never negative,
# an odd power keeps the sign (camera lesson, topic 8).
a1 = I('a1', '$|a|>0$ $\\quad b^2>0$', hand='|a| > 0      b^2 > 0')
a2 = I('a2', 'So the top is negative: $\\ a^5<0$', size=32, hand='So the top is negative :   a^5 < 0')
a3 = I('a3', 'Odd power keeps the sign: $\\ \\hl{a}{a<0}$', size=32, hand='Odd power keeps the sign :   \\hl{a}{a < 0}')
a4 = I('a4', 'Find the surely positive pieces first', size=28, col=1)
a6 = I('a6', '$\\frac{(-2)^3\\cdot4}{2}<0\\qquad\\frac{(-2)^2\\cdot4}{2}>0$', size=28, col=1, hand='{(−2)^3·4/2} < 0        {(−2)^2·4/2} > 0')
a5 = I('a5', '$b$: only $b\\ne0$ ✗', size=30, col=1, hand='b :   only  b ≠ 0   ✗')
b1 = I('b1', '$a=1,\\ b=1$: $\\ \\frac{1}{1}=1$ ✗', hand='a = 1,  b = 1 :    {1/1} = 1   ✗')
b2 = I('b2', '$a=-1,\\ b=1$: $\\ \\frac{-1}{1}=-1$ ✓', hand='a = −1,  b = 1 :    {−1/1} = −1   ✓')
b3 = I('b3', 'Positive $b$ works: $\\ $(2) ✗', size=30, col=1, hand='Positive b works :   (2) ✗')
video('solve-q-457', 'solution', qid='q-457', slides=[
    S('Method 1 · Positive pieces first',
      L("Given: a is not equal to zero, and a to the power of five, times b squared, over the absolute value of a, is "
        "smaller than zero. Which of the following is necessarily true?", pt('stem', 'Given', 'hl', 9.0), voice='calm', pause=0.5),
      L("So it's a sign question, not a calculation. The whole fraction is negative, and we have to find out what that says about a and b. The trick is to find the pieces that are surely positive, because then the piece that's left decides the sign. For example, negative two cubed, times four, over two. Four and two are positive, so the sign comes from negative two cubed, negative eight, and the whole thing is negative. And negative two squared times four, over two? Every piece is positive, so it's positive. [short pause] We'll solve it two ways, piece by piece, and then plugging in numbers.",
        pt('stem: g2', 'The whole fraction is negative'), show(a6, 'For example, negative two cubed')),
      L("[short pause] Let's start piece by piece, and first find the pieces that are surely positive. Why do they tell us "
        "a isn't zero? So the bottom isn't zero. The bottom is the absolute value of a, and remember, an absolute value is "
        "zero or positive. It can't be zero here, so it's positive.", show(a4, 'the pieces that are surely positive'), pt('stem: g1', "a isn't zero")),
      L("b squared is an even power, so it's never negative. And b can't be zero, because then the whole fraction would be "
        "zero, not smaller than zero. So b squared is positive too.", show(a1, 'b squared is an even power')),
      L("So the bottom is positive, and one piece on top is positive. For the fraction to be negative, the piece that's "
        "left must be negative. So a to the power of five is negative.", show(a2, 'the piece that\'s left')),
      L("And an odd power keeps the sign. So a itself is negative. Choice number four is our answer.",
        show(a3, 'an odd power keeps the sign'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Now careful, choice number two is the trap. It says b is negative too. But all we learned about b is that it isn't "
        "zero. It can be positive or negative.", show(a5, 'all we learned about b'), mk('cross', 'choice 2', 'positive or negative'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers. Is a positive possible? a is one and b is one. One to the power of five is one, b squared is one, and the bottom is one, so the fraction is one. That's not smaller than zero, so a can't be positive.", show(b1, 'a is one and b is one')),
      L("So a negative a. a is negative one, b is one. Negative one to the power of five is negative one, and b squared and the bottom are both one, so the fraction is negative one. It works. And b was positive here, so b doesn't have to be negative.",
        show(b2, 'a is negative one'), show(b3, 'b was positive here')),
      L("Choice numbers one and three say a is positive, so they're out, and choice number two needs b negative, out too. "
        "So choice number four. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 1', 'Choice numbers one'), mk('cross', 'choice 3', 'and three say'), mk('cross', 'choice 2', 'out too'),
        mk('tick', 'choice 4', 'So choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t16-01 (Q2)
# NEW: in a sum with mixed signs, the one bigger in size wins (why); a positive sum -> the positive one is bigger in
# size.  REMINDER: sign rules for products (camera lesson), absolute value as size (topic 13).
c1 = I('c1', 'Mixed signs: the bigger size wins', size=28, col=1)
c2 = I('c2', '$-2+5=3$ $\\quad -5+2=-3$', size=32, col=1, hand='−2 + 5 = 3      −5 + 2 = −3')
c3 = I('c3', '$x+y>0$: $\\ y$ wins, $\\ \\hl{a}{|y|>|x|}$', hand='x + y > 0 :    y wins,   \\hl{a}{|y| > |x|}')
c4 = I('c4', '(3) $xy$: $\\ (-)(+)<0$ ✗', size=32, hand='(3)   xy :   (−)(+) < 0   ✗')
c5 = I('c5', '(4) $x-y$: smaller $-$ bigger $<0$ ✗', size=32, hand='(4)   x − y :   smaller − bigger < 0   ✗')
d1 = I('d1', '$x=-1,\\ y=3$: $\\ -1+3=2>0$ ✓', hand='x = −1,  y = 3 :    −1 + 3 = 2 > 0   ✓')
d2 = I('d2', '(1) $1>3$ ✗ $\\quad$(3) $-3>0$ ✗ $\\quad$(4) $-4>0$ ✗', size=30, hand='(1)  1 > 3  ✗     (3)  −3 > 0  ✗     (4)  −4 > 0  ✗')
video('solve-q-r26-t16-01', 'solution', qid='q-r26-t16-01', slides=[
    S('Method 1 · The bigger size wins',
      L("Given: x is smaller than zero, which is smaller than y, and x plus y is bigger than zero. Which of the following is "
        "necessarily true?", pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("So x is negative and y is positive, mixed signs. And their sum is positive. [short pause] We'll solve it two ways, "
        "with the sizes, and then plugging in numbers.", pt('stem: g1', 'x is negative and y is positive'), pt('stem: g2', 'their sum is positive')),
      L("[short pause] Let's start with the sizes. When you add a negative and a positive, they fight, and the one that's "
        "bigger in size wins. Negative two plus five is three, positive, because five is bigger in size. Negative five plus "
        "two is negative three.", show(c1, 'the one that\'s bigger in size wins'), show(c2, 'Negative two plus five')),
      L("Here the sum is positive, so the positive one won. y is bigger in size than x. Choice number two is our answer. And "
        "choice number one is the opposite.", show(c3, 'the positive one won'), mk('tick', 'choice 2', 'Choice number two is our answer'),
        mk('cross', 'choice 1', 'is the opposite')),
      L("In the exam you'd circle it and move on. Here, the other two read the signs. x times y, a negative times a positive, "
        "is negative. Out. x minus y, the smaller minus the bigger, is negative too. Out.",
        show(c4, 'x times y'), mk('cross', 'choice 3', 'is negative. Out'), show(c5, 'x minus y'), mk('cross', 'choice 4', 'negative too. Out'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers that fit. x is negative one and y is three. Negative one plus three is "
        "two, positive, so they fit.", show(d1, 'x is negative one')),
      L("Choice number one, one bigger than three? No. Choice number three, negative one times three is negative three, "
        "bigger than zero? No. Choice number four, negative one minus three is negative four. No. Three are out, so choice "
        "number two. [pause] Okay. I'll see you in the next question.",
        show(d2, 'Choice number one, one bigger'), mk('cross', 'choice 1', 'than three? No'), mk('cross', 'choice 3', 'zero? No'),
        mk('cross', 'choice 4', 'negative four. No'), mk('tick', 'choice 2', 'so choice number two'))),
])

# ------------------------------------------------------------------------------------------------ consecutive-integers (lesson)
# NEW: three ways into consecutive numbers - one letter (from the middle), plugging in the smallest legal numbers
# (check the choices first), the differences with their signs; "bigger than zero" doesn't mean starting at one.
# REMINDER: what consecutive (even / odd) numbers are (topic 1).
e1 = I('e1', '$5,\\ 6,\\ 7\\qquad -3,\\ -2,\\ -1\\qquad 4,\\ 6,\\ 8$', size=40, hand='5, 6, 7        −3, −2, −1        4, 6, 8')
e2 = I('e2', '$b-1,\\ \\ b,\\ \\ b+1$ $\\quad b=8$: $\\ 7,\\ 8,\\ 9$', size=40, hand='b − 1,   b,   b + 1      b = 8 :   7,  8,  9')
e3 = I('e3', 'Evens or odds: $\\ b-2,\\ \\ b,\\ \\ b+2$', size=40, hand='Evens or odds :    b − 2,   b,   b + 2')
e4 = I('e4', 'Plug in: $\\ 1,\\ 2,\\ 3$ $\\ $(choices must differ)', size=38, hand='Plug in :    1,  2,  3     (choices must differ)')
e5 = I('e5', '$8-7=1\\quad 7-8=-1\\quad 9-7=2\\quad 7-9=-2$', size=38, hand='8 − 7 = 1     7 − 8 = −1     9 − 7 = 2     7 − 9 = −2')
e6 = I('e6', '$x>0$: $\\ $maybe $23,\\ 24,\\ 25$', size=40, hand='x > 0 :    maybe  23,  24,  25')
video('consecutive-integers', 'lesson', slides=[
    S('Consecutive Integers',
      L("Welcome back. Now consecutive numbers. Questions about them usually have more than one way in, so we'll learn three, "
        "and you pick the one that's easiest for you.")),
    S('Three ways in',
      L("Remember, consecutive numbers are integers in a row, each one more than the one before. Five, six, seven. Negatives "
        "count too, negative three, negative two, negative one. And consecutive even numbers, or odd numbers, go up by two, "
        "four, six, eight.", show(e1, 'Five, six, seven')),
      L("The first way, one letter. Write all of them with one letter, and the middle one is usually the neatest. Three in a row are b minus one, b, and b plus one. If b is eight, that's seven, eight, nine, and if b is twenty, nineteen, twenty, twenty-one. For evens or odds, b minus two, b, and b plus two, so with b eight, six, eight, ten.",
        show(e2, 'Three in a row are'), show(e3, 'For evens or odds')),
      L("The second way, plugging in numbers. Take the smallest legal numbers, like one, two, three, because they're the "
        "easiest to work with. But first check that the choices come out different with them. If two choices tie, take "
        "other numbers.", show(e4, 'the smallest legal numbers')),
      L("The third way, the differences. Bigger minus smaller is one, and smaller minus bigger is negative one. Eight minus seven is one, but seven minus eight is negative one. And two steps apart, nine minus seven is two, and seven minus nine is negative two. The size is the same, but the sign isn't, so watch the sign.", show(e5, 'Bigger minus smaller')),
      L("And one trap. If they say the numbers are bigger than zero, it doesn't mean they start at one. They could be "
        "twenty-three, twenty-four, twenty-five. [pause] Okay. I'll see you in the next video.", show(e6, 'bigger than zero'))),
])

# ------------------------------------------------------------------------------------------------ q-458 (Q3)
# NEW: write consecutive evens around the middle (q - 2, q, q + 2); r^2 - p^2 as (r - p)(r + p); the trap 2 (a gap of
# one).  REMINDER: the third shortcut formula (topic 4), plugging in the smallest legal numbers (lesson).
f1 = I('f1', '$p=q-2,\\ \\ \\ r=q+2$', hand='p = q − 2,      r = q + 2')
f2 = I('f2', '$r^2-p^2=(r-p)(r+p)$', hand='r^2 − p^2 = (r − p)(r + p)')
f3 = I('f3', '$r-p=4,\\ \\ \\ r+p=2q$', hand='r − p = 4,      r + p = 2q')
f4 = I('f4', '$\\frac{4\\cdot2q}{2q}=\\hl{a}{4}$', hand='{4·2q/2q} = \\hl{a}{4}')
f5 = I('f5', 'Evens: the gap is $2$, not $1$', size=28, col=1)
g1 = I('g1', '$p=2,\\ q=4,\\ r=6$', hand='p = 2,   q = 4,   r = 6')
g2 = I('g2', '$\\frac{36-4}{8}=\\frac{32}{8}=\\hl{a}{4}$', hand='{36 − 4/8} = {32/8} = \\hl{a}{4}')
video('solve-q-458', 'solution', qid='q-458', slides=[
    S('Method 1 · One letter',
      L("p, q and r are consecutive even numbers, and zero is smaller than p, which is smaller than q, which is smaller than "
        "r. What is r squared minus p squared, over two q?", pt('stem', 'p, q and r', 'hl', 10.0), voice='calm', pause=0.5),
      L("So three consecutive even numbers, and an expression. [short pause] We'll solve it two ways, with one letter, and "
        "then plugging in numbers.", pt('stem', 'three consecutive even numbers')),
      L("[short pause] Let's start with one letter, the middle one, q. Consecutive even numbers go up by two, so p is q "
        "minus two, and r is q plus two.", show(f1, 'p is q minus two'), show(f5, 'go up by two')),
      L("Now the top, r squared minus p squared. That's the third shortcut formula, r minus p, times r plus p.",
        show(f2, 'the third shortcut formula')),
      L("r minus p is q plus two, minus q minus two, four. And r plus p is q plus two plus q minus two, two q.",
        show(f3, 'r minus p is')),
      L("So the top is four times two q, and over two q, that's four. Choice number four is our answer.",
        show(f4, 'four times two q'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Now careful, two is the trap. It comes from a gap of one, but these are even numbers, and the gap is two.",
        mk('cross', 'choice 2', 'two is the trap'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in the smallest legal numbers. Bigger than zero, even and in a row, so two, four "
        "and six.", show(g1, 'two, four and six')),
      L("Six squared is thirty-six, two squared is four, and thirty-six minus four is thirty-two. Two times the middle, two "
        "times four, is eight. Thirty-two over eight is four. Choice number four. [pause] Okay. I'll see you in the next "
        "question.", show(g2, 'Six squared is thirty-six'), mk('tick', 'choice 4', 'Choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-459 (Q4)
# NEW: the minus between two fractions - work out each fraction first; the trap 0.  REMINDER: plugging in 1, 2, 3, 4;
# the differences with their signs (lesson).
h1 = I('h1', '$p=1,\\ q=2,\\ r=3,\\ s=4$', hand='p = 1,   q = 2,   r = 3,   s = 4')
h2 = I('h2', '$\\frac{3-1}{4-3}=\\frac{2}{1}=2$', hand='{3 − 1/4 − 3} = {2/1} = 2')
h3 = I('h3', '$\\frac{2-4}{3-2}=\\frac{-2}{1}=-2$', hand='{2 − 4/3 − 2} = {−2/1} = −2')
h4 = I('h4', '$2-(-2)=\\hl{a}{4}$', hand='2 − (−2) = \\hl{a}{4}')
h5 = I('h5', 'Each fraction first, then the minus', size=28, col=1)
k1 = I('k1', '$r-p=2\\qquad s-r=1$', hand='r − p = 2        s − r = 1')
k2 = I('k2', '$q-s=-2\\qquad r-q=1$', hand='q − s = −2        r − q = 1')
k3 = I('k3', '$\\frac21-\\frac{-2}{1}=2+2=\\hl{a}{4}$', hand='{2/1} − {−2/1} = 2 + 2 = \\hl{a}{4}')
video('solve-q-459', 'solution', qid='q-459', slides=[
    S('Method 1 · Plugging in numbers',
      L("p, q, r and s are consecutive integers, and p is smaller than q, which is smaller than r, which is smaller than s. "
        "What is r minus p, over s minus r, minus q minus s, over r minus q?", pt('stem', 'p, q, r and s', 'hl', 11.0), voice='calm', pause=0.5),
      L("So four numbers in a row, and two fractions of differences. [short pause] We'll solve it two ways, plugging in "
        "numbers, and then reading the differences.", pt('stem', 'four numbers in a row')),
      L("[short pause] Let's start by plugging in the smallest numbers, one, two, three and four.", show(h1, 'one, two, three and four')),
      L("The first fraction. Three minus one is two, and four minus three is one, so two over one, two.", show(h2, 'Three minus one is two')),
      L("The second fraction. Two minus four is negative two, and three minus two is one, so negative two.", show(h3, 'Two minus four')),
      L("Now careful with the minus between the fractions. Work out each fraction first, and only then subtract. Two minus "
        "negative two is two plus two, four. Choice number four is our answer.", show(h5, 'Work out each fraction first'),
        show(h4, 'Two minus negative two'), mk('tick', 'choice 4', 'Choice number four is our answer')),
      L("Got zero? That's the trap, the minus of the second fraction got lost.", mk('cross', 'choice 3', "That's the trap"))),
    S('Method 2 · The differences',
      L("[pause] Another way is to read the differences, with their signs. r minus p, bigger minus smaller, two steps, so "
        "two. s minus r, one.", show(k1, 'r minus p')),
      L("q minus s, smaller minus bigger, two steps back, negative two. r minus q, one.", show(k2, 'q minus s')),
      L("So two over one, minus negative two over one. Two plus two, four. Choice number four. [pause] Okay. I'll see you in "
        "the next question.", show(k3, 'So two over one'), mk('tick', 'choice 4', 'Choice number four'))),
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
 "q-457": "Given:\n$\\begin{cases} a\\ne0 \\\\ \\frac{a^5\\cdot b^2}{|a|}<0 \\end{cases}$\nWhich of the following is necessarily true?",
 "q-r26-t16-01": "Given:\n$\\begin{cases} x<0<y \\\\ x+y>0 \\end{cases}$\nWhich of the following is necessarily true?",
 "q-r26-t16-02": "The sum of seven consecutive integers is $91$. What is the largest of them?",
 "q-r26-t16-03": "The sum of four consecutive integers is always —",
 "q-460": "m and n are positive integers, and $m+n$ is odd. Which of the following is true about the expression $m^n+n^m+9+4n$?",
 "q-461": "a and b are integers. a is odd, and b is even and not $0$. Which of the following is the most precise description of $\\frac{6a}{b^2}$?",
 "q-462": "a and b are integers. Given: $a-b=6$. Which of the following expressions is necessarily even?",
 "q-463": "n is an odd number. Which of the following is the most precise description of $\\frac{9n^2-1}{4}$?",
 "q-464": "n is an integer. The expression $\\frac{n-n^3}{3}$ is always —",
 "q-r26-t16-04": "n is a positive odd number. The product $n(n+2)(n+4)$ is necessarily divisible by —",
 "q-465": "Given: $w<x<0<y<z$. Which of the following expressions is necessarily negative?",
 "q-466": "Given:\n$\\begin{cases} x>y \\\\ xy<0 \\end{cases}$\nWhich of the following expressions is necessarily positive?",
 "q-467": "Given:\n$\\begin{cases} p>q \\\\ p+q+r<0 \\end{cases}$\nWhich of the following additional givens makes r necessarily negative?",
 "q-470": "b and y are integers. Given: $y=(b-3)^2+(b+8)^3$. Which of the following statements is necessarily true?",
 "q-471": "k, a, b and c are integers. Given: $2k+1=a^3\\cdot(b+1)^2\\cdot(c-5)^4$. Which of the numbers k, a, b, c is necessarily odd?",
 "q-472": "a is an odd positive number, and b is an even positive number. Which of the following expressions is not necessarily an integer?"
}   # "=?" questions (no question sentence): the whole stem only
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
