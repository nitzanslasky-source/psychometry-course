"""Topic 15 (Division & Remainder) - the redo for the teacher's own-voice reading (2026-10-11), built exactly like topic 13
and topic 14 (math_patches/_ai_vis_t13.py / _ai_vis_t15.py; the DSL and the visual passes are copied here, so the topics stay
independent; the stem-part highlighting is copied from topic 13).

The teacher records only the camera lesson 'divisibility' (re-record, never touched here). Every other topic-15 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t15.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t15.py ai_redo_t15() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), nothing calculated that logic already decides and no "does another one also work" check (R35), the
answer, a takeaway only when it earns its place (R16), then "Okay. I'll see you in the next question." No verdict, and no
"Our first / second method" lines - the methods are announced once, and each switch has a spoken transition (R13). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-15-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t15ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-15 flow order of the scripts (divisibility = the camera lesson, not here)
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
            'style': "the teacher reads it herself (Reading Studio), topic-15 redo (2026-10-11): math_patches/_ai_vis_t15.py is "
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
# THE SCRIPTS (topic-15 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-15-AI-scripts-review.md.
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ q-423 (Q1)
# NEW: "what could it be" = rule out what it can't be; a fraction of a fraction - build the group from the inside
# (k -> 3k -> 15k): multiply the denominators, with a second example (half of a quarter -> 8).
# REMINDER: the sign for 5 (camera lesson).
a1 = I('a1', 'A fifth of the class: divisible by $5$', size=28, col=1)
a2 = I('a2', '$35$ ✓ $\\quad 45$ ✓ $\\quad 42$ ✗ $\\quad 32$ ✗', hand='35 ✓     45 ✓     42 ✗     32 ✗')
a3 = I('a3', 'A third of the basketball boys: divisible by $3$', size=26, col=1)
a4 = I('a4', '$35\\div5=7$, $\\ 7\\div3$ ✗', hand='35 ÷ 5 = 7,    7 ÷ 3   ✗')
a5 = I('a5', 'Only $45$ is left', hand='Only  45  is left')
b1 = I('b1', 'Guitar: $\\ k$', hand='Guitar :   k')
b2 = I('b2', 'Basketball: $\\ 3k$', hand='Basketball :   3k')
b3 = I('b3', 'Class: $\\ 5\\cdot3k=\\hl{c}{15k}$', hand='Class :   5·3k = \\hl{c}{15k}')
b4 = I('b4', 'Nested fractions with numerator $1$: multiply denominators', size=25, col=1)
b5 = I('b5', '$\\frac12$ of $\\frac14$: $\\ 2\\cdot4=8$', size=30, col=1, hand='{1/2} of {1/4} :   2·4 = 8')
b6 = I('b6', 'Multiples of $15$: $\\ 15,\\ 30,\\ \\hl{f}{45}$', hand='Multiples of 15 :   15,  30,  \\hl{f}{45}')
video('solve-q-423', 'solution', qid='q-423', slides=[
    S('Method 1 · Step by step',
      L("In Daniel's class, one fifth of the students are boys who play basketball, and among those, one third also play the "
        "guitar. What could be the number of students in the class?", pt('stem', "In Daniel's", 'hl', 9.0), voice='calm', pause=0.5),
      L("So we don't know the size of the class, and they ask what it could be. So we don't look for the number itself, we "
        "rule out what it can't be. And look at the fractions. There's no such thing as a fifth of a student. [short pause] "
        "We'll solve it two ways, step by step with the fractions, and then by building the class from the inside.",
        pt('stem: ask', 'what it could be'), pt('stem', 'look at the fractions')),
      L("[short pause] Let's start step by step. A fifth of the class are basketball boys, and a fifth of a class has to be a "
        "whole number of kids. So the class is divisible by five. And remember the sign for five, the last digit is zero or "
        "five.", pt('stem', 'A fifth of the class'), show(a1, 'So the class is divisible by five')),
      L("Thirty-five ends in five, and forty-five ends in five, so they stay. Forty-two and thirty-two don't, so choice "
        "numbers three and four are out.", show(a2, 'Thirty-five ends in five'), mk('cross', 'choice 3', 'choice numbers three'),
        mk('cross', 'choice 4', 'and four are out')),
      L("Now the second fraction. A third of the basketball boys play the guitar, so the basketball group has to divide by "
        "three. Thirty-five over five is seven basketball boys. A third of seven? Seven doesn't divide by three, so there's "
        "no such group. Choice number one is out.", show(a3, 'the basketball group has to divide'), show(a4, 'Thirty-five over five'),
        mk('cross', 'choice 1', 'Choice number one is out')),
      L("So forty-five is the only one left, and choice number two is our answer.", show(a5, 'the only one left'),
        mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Build from the inside',
      L("[pause] Another way is to build the class from the inside, from the smallest group out. Call the guitar players k, "
        "a whole number of kids. They're a third of the basketball boys, so there are three k basketball boys. And the "
        "basketball boys are a fifth of the class, so the class is five times three k, which is fifteen k.",
        show(b1, 'Call the guitar players k'), show(b2, 'three k basketball boys'), show(b3, 'the class is five times'),
        mk('circle', 'b3: c', 'fifteen k')),
      L("k is a whole number, so the class is always a multiple of fifteen. "
        "Here both fractions have one on top, one fifth and one third. For nested fractions like these, "
        "multiply the denominators. That is not a rule for every fraction of a fraction. "
        "Let's see the same idea with half of a quarter of a group. Two times four is eight, so the "
        "group divides by eight, not just by four. With eight kids, a quarter is two, and half of that is one.",
        show(b4, 'both fractions have one on top'), show(b5, 'half of a quarter'), pt('b5', 'With eight kids')),
      L("So which choice is a multiple of fifteen? Fifteen, thirty, forty-five. Forty-five, choice number two. Thirty-five, "
        "forty-two and thirty-two aren't on that list.", show(b6, 'Fifteen, thirty'), mk('tick', 'choice 2', 'Forty-five, choice number two'),
        mk('cross', 'choice 1', 'Thirty-five,'), mk('cross', 'choice 3', 'forty-two and'), mk('cross', 'choice 4', "thirty-two aren't")),
      L("[pause] Okay. I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ q-424 (Q2)
# NEW: leftover rows = remainders; testing the choices and stopping at the first that fits (one correct answer, R35);
# listing numbers with a given remainder by hopping by the divisor (why: a full row never changes the leftover).
# REMINDER: what a remainder is (camera lesson).
c1 = I('c1', '$28=25+3$ ✗', hand='28 = 25 + 3   ✗')
c2 = I('c2', '$40=40+0$ ✗', hand='40 = 40 + 0   ✗')
c3 = I('c3', '$34=30+4$ ✓', hand='34 = 30 + 4   ✓')
c4 = I('c4', '$34=33+1$ ✓', hand='34 = 33 + 1   ✓')
c5 = I('c5', 'One correct answer: stop', size=28, col=1)
P1 = STRIP('P1', 0, 40, [
    ('hops', [('prime', v) for v in (4, 9, 14, 19, 24, 29, 34, 39)]),
    ('pick', [('ring', 34)]),
], base=(0,), w=1060)
d1 = I('d1', 'A full row never changes the leftover', size=28, col=1)
d2 = I('d2', 'On the list: $\\ $only $34$', hand='On the list :   only  34')
video('solve-q-424', 'solution', qid='q-424', slides=[
    S('Method 1 · Test the choices',
      L("Tamar is putting her stamps into an album. If she arranges them in rows of five, with an equal number in each row, "
        "four stamps are left over. If she arranges them in rows of three, with an equal number in each row, one stamp is "
        "left over. What could be the number of stamps Tamar has?", pt('stem', 'Tamar is', 'hl', 14.0), voice='calm', pause=0.5),
      L("So two leftover conditions. Rows of five leave four stamps, and rows of three leave one. Those leftovers are just "
        "remainders. And they ask what the number could be, so we can test the choices. [short pause] We'll solve it two "
        "ways, testing the choices, and then listing the numbers that fit.", pt('stem', 'Rows of five leave four'),
        pt('stem', 'rows of three leave one'), pt('stem: ask', 'what the number could be')),
      L("[short pause] Let's start by testing the choices, rows of five first. Remember, the remainder is what's left after "
        "as many full rows as possible. Twenty-eight. Five rows of five are twenty-five, and twenty-eight minus twenty-five "
        "leaves three. We need four, so choice number one is out.", pt('choice 1', 'Twenty-eight.'), show(c1, 'Five rows of five'),
        mk('cross', 'choice 1', 'choice number one is out')),
      L("Forty. Eight rows of five are exactly forty, so nothing is left. Out.", show(c2, 'Eight rows of five'), mk('cross', 'choice 2', 'Out.')),
      L("Thirty-four. Six rows of five are thirty, and thirty-four minus thirty leaves four. That fits. Now rows of three. "
        "Eleven rows of three are thirty-three, and thirty-four minus thirty-three leaves one. That fits too.",
        show(c3, 'Six rows of five'), show(c4, 'Eleven rows of three')),
      L("Both conditions fit, and a question has one correct answer, so there's no need to check sixteen. Choice number three "
        "is our answer.", show(c5, 'one correct answer'), mk('tick', 'choice 3', 'Choice number three'))),
    S('Method 2 · List the numbers',
      L("[pause] Another way is to list the numbers that leave four in rows of five. Start at four, and hop by five. Why hop by five? One more full row of five never changes what's left over. Fourteen is two rows and four, and nineteen is three rows and four. Four, nine, fourteen, nineteen, twenty-four, "
        "twenty-nine, thirty-four, thirty-nine.", show(d1, 'Another way is to list'), show(P1['line'], 'list the numbers'), show(P1['hops'], 'Four, nine, fourteen')),
      L("Which choices are on the list? Twenty-eight, no. Forty, no. Thirty-four, yes. Sixteen, no. Only thirty-four is on it, "
        "so we don't even need the rows of three. Choice number three. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 1', 'Twenty-eight, no'), mk('cross', 'choice 2', 'Forty, no'), show(P1['pick'], 'Thirty-four, yes'),
        mk('cross', 'choice 4', 'Sixteen, no'), show(d2, 'Only thirty-four is on it'), mk('tick', 'choice 3', 'Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-425 (Q3)
# NEW: a product of two remainders is biggest when each remainder is; the trap 24 = the divisors themselves.
# REMINDER: the biggest remainder is the divisor minus one (camera lesson).
e1 = I('e1', 'Biggest remainder $=$ divisor $-\\ 1$', size=28, col=1)
e2 = I('e2', 'By $8$: $\\ 23=16+\\hl{s}{7}$', hand='By 8 :   23 = 16 + \\hl{s}{7}')
e3 = I('e3', 'By $3$: $\\ 11=9+\\hl{t}{2}$', hand='By 3 :   11 = 9 + \\hl{t}{2}')
e4 = I('e4', '$x\\cdot y\\le7\\cdot2=\\hl{a}{14}$', hand='x·y  ≤  7·2 = \\hl{a}{14}')
e5 = I('e5', '$24=8\\cdot3$: the divisors ✗', size=30, col=1, hand='24 = 8·3 :   the divisors   ✗')
f1 = I('f1', 'By $8$: $\\ 1,2,3,4,5,6,\\hl{s}{7},0,1,2$', size=32, hand='By 8 :   1, 2, 3, 4, 5, 6, \\hl{s}{7}, 0, 1, 2')
f2 = I('f2', 'By $3$: $\\ 1,\\hl{t}{2},0,1,2,0$', size=32, hand='By 3 :   1, \\hl{t}{2}, 0, 1, 2, 0')
f3 = I('f3', '$7\\cdot2=14$', hand='7·2 = 14')
video('solve-q-425', 'solution', qid='q-425', slides=[
    S('Method 1 · The biggest remainder',
      L("a and b are positive integers. x is the remainder when a is divided by eight, and y is the remainder when b is "
        "divided by three. What is the greatest possible value of x times y?", pt('stem', 'a and b are', 'hl', 9.0), voice='calm', pause=0.5),
      L("So x and y are remainders, and they want the biggest possible product. a and b can be any positive integers, so we "
        "get to choose them. [short pause] We'll solve it two ways, with the biggest-remainder rule, and then by listing the "
        "remainders.", pt('stem: ask', 'the biggest possible product'), pt('stem', 'we get to choose them')),
      L("[short pause] Let's start with the rule. x and y are zero or positive, so x times y is biggest when each of them is "
        "as big as possible. And remember, the biggest remainder is one less than the divisor. Dividing by eight, the "
        "biggest remainder is seven. Why not eight? With eight left over, one more eight would fit.",
        show(e1, 'the biggest remainder is one less')),
      L("For example, a is twenty-three. Two eights are sixteen, and twenty-three minus sixteen leaves seven.",
        show(e2, 'a is twenty-three'), mk('circle', 'e2: s', 'leaves seven')),
      L("Dividing by three, the biggest remainder is two. For example, b is eleven. Three threes are nine, and eleven minus "
        "nine leaves two.", show(e3, 'Dividing by three'), mk('circle', 'e3: t', 'leaves two')),
      L("So x times y is at most seven times two, which is fourteen. Choice number three is our answer.", show(e4, 'seven times two'),
        mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Now careful, twenty-four is the trap. That's eight times three, the divisors themselves, and a remainder never "
        "reaches the divisor. And seven and two are each just one of the remainders, not the product.",
        show(e5, 'twenty-four is the trap'), mk('cross', 'choice 4', 'never reaches the divisor'), mk('cross', 'choice 1', 'And seven and'),
        mk('cross', 'choice 2', 'two are each'))),
    S('Method 2 · List the remainders',
      L("[pause] Another way is to list the remainders by trying numbers. Divide one, two, three and so on by eight. One "
        "leaves one, two leaves two, and so on up to seven, which leaves seven. Eight leaves zero, nine leaves one again. So "
        "dividing by eight, the remainders go round from zero to seven.", show(f1, 'Divide one, two, three')),
      L("Dividing by three, they go round zero, one, two. So the biggest are seven and two, and seven times two is fourteen. "
        "Choice number three. [pause] Okay. I'll see you in the next question.", show(f2, 'Dividing by three'),
        show(f3, 'seven times two is fourteen'), mk('tick', 'choice 3', 'Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-426 (Q4)
# NEW: in an expression, split off the part that divides by 5 and look at what's left; in (5x + 2) squared everything
# built from 5x divides too, so only 2 squared matters; plugging in x = 0 is safe here (why).
# REMINDER: a number with remainder 4 by 5 is 5k + 4 (camera lesson); the (a + b)^2 formula (topic 4).
g1 = I('g1', 'Remainder $4$ by $5$: $\\ 5k+4$', size=30, col=1, hand='Remainder 4 by 5 :   5k + 4')
g2 = I('g2', '(1) $5x+\\hl{r}{7}$: $\\ 7=5+2$ ✗', size=32, hand='(1)   5x + \\hl{r}{7} :   7 = 5 + 2   ✗')
g3 = I('g3', '$(5x+2)^2=25x^2+20x+\\hl{r}{4}$', size=32, hand='(5x+2)^2 = 25x^2 + 20x + \\hl{r}{4}')
g4 = I('g4', 'Built from $5x$: divides by $5$. Check $2^2=4$', size=26, col=1)
g5 = I('g5', '(3) $10x+8$: $\\ 8=5+3$ ✗', size=32, hand='(3)   10x + 8 :   8 = 5 + 3   ✗')
g6 = I('g6', '(4) $5^2=25=5\\cdot5+0$ ✗', size=32, hand='(4)   5^2 = 25 = 5·5 + 0   ✗')
h1 = I('h1', '$x=0$: $\\ 7,\\ \\ 4,\\ \\ 8,\\ \\ 25$', hand='x = 0 :    7,   4,   8,   25')
h2 = I('h2', 'Remainders: $\\ 2,\\ \\ \\hl{r}{4},\\ \\ 3,\\ \\ 0$', hand='Remainders :    2,   \\hl{r}{4},   3,   0')
h3 = I('h3', 'The $5x$ part never changes the remainder', size=26, col=1)
video('solve-q-426', 'solution', qid='q-426', slides=[
    S('Method 1 · Split off the fives',
      L("A number leaves a remainder of four when divided by five. Which of the following expressions could represent the "
        "number? x is an integer.", pt('stem', 'A number leaves', 'hl', 7.0), voice='calm', pause=0.5),
      L("So we know the remainder by five, and every choice is an expression with x. Remember, a number that leaves four "
        "when divided by five is five k plus four, full fives plus four. [short pause] We'll solve it two ways, splitting "
        "off the fives in each choice, and then plugging in a number.", pt('choice 1', 'every choice is an expression'), show(g1, 'five k plus four')),
      L("[short pause] Let's start by splitting off the fives. In each choice, the part that divides by five doesn't matter, "
        "and only what's left decides. Choice number one, five x plus seven. Five x is always full fives. Seven is one five "
        "plus two, so it leaves two, not four. Out.", pt('choice 1', 'Choice number one'), show(g2, 'Five x is always'),
        mk('cross', 'choice 1', 'not four. Out')),
      L("Choice number two, in brackets, five x plus two, all squared. Let's open it with the formula, a plus b, all squared. "
        "The first term is five x, all squared. We square both the five and the x, so that is twenty-five x squared. "
        "The middle term is two times five x times two, which is twenty x. And the last term is two squared, which is four.",
        pt('choice 2', 'Choice number two'), show(g3, "Let's open it"), mk('circle', 'g3: r', 'two squared, which is four')),
      L("Twenty-five x squared and twenty x both divide by five, and what's left is four. That's exactly the remainder we "
        "need, so choice number two is our answer.", pt('g3', 'Twenty-five x squared and'), mk('tick', 'choice 2', 'choice number two is our answer')),
      L("And here's a shortcut for next time. Everything built from five x divides by five too, so I only need the square "
        "of the number at the end, two squared, four.", show(g4, "here's a shortcut"))),
    S('Method 1 · Split off the fives',
      L("In the exam you'd circle it and move on. Here, the other two with the shortcut. Ten x plus eight. Ten x is full "
        "fives, and eight is one five plus three. Out. Five x plus five, squared. The last number is five, and five squared "
        "is twenty-five, exactly five fives, nothing left. Out.",
        show(g5, 'Ten x plus eight'), mk('cross', 'choice 3', 'plus three. Out'), show(g6, 'Five x plus five'), mk('cross', 'choice 4', 'nothing left. Out')),
      sb='Method 1 · Split off the fives'),
    S('Method 2 · Plugging in a number',
      L("[pause] Now let's try plugging in a number. x is any integer, so I'll take zero. Why zero? Here every choice leaves "
        "the same remainder for every x, because the x part is always full fives. So the easiest number is the best.",
        show(h3, 'the x part is always full fives')),
      L("With x zero, the choices are seven, two squared, which is four, eight, and five squared, which is twenty-five.",
        show(h1, 'the choices are seven')),
      L("Divided by five, seven leaves two, four leaves four, eight leaves three, and twenty-five leaves nothing. Only four "
        "leaves four, so choice number two. [pause] Okay. I'll see you in the next question.",
        show(h2, 'Divided by five'), mk('circle', 'h2: r', 'Only four leaves four'), mk('tick', 'choice 2', 'so choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t15-01 (Q5)
# NEW (full): the remainder of a sum / difference / product = the same operation on the remainders (why, from the
# tags; an example of each); a negative result -> add the divisor (why: a full seven never changes the remainder; checked
# with 23 - 12 = 11); plugging in two pairs.  REMINDER: tags 7k + 2
# (camera lesson); different letters for different numbers.
j1 = I('j1', '$a=7k+2,\\ \\ \\ b=7m+5$', hand='a = 7k + 2,     b = 7m + 5')
j2 = I('j2', 'Different letters: different numbers', size=28, col=1)
j3 = I('j3', '$a-b=7k-7m+2-5$', hand='a − b = 7k − 7m + 2 − 5')
j4 = I('j4', '$=7(k-m)-3$', hand='= 7(k−m) − 3')
j5 = I('j5', '$=7(k-m-1)+\\hl{r}{4}$', hand='= 7(k−m−1) + \\hl{r}{4}')
j9 = I('j9', '$23-12=11=7+\\hl{r}{4}$ ✓', size=32, hand='23 − 12 = 11 = 7 + \\hl{r}{4}   ✓')
j10 = I('j10', 'Product: $\\ 9\\cdot12=108=105+3$, $\\ 2\\cdot5=10\\to3$', size=26, col=1, hand='Product :   9·12 = 108 = 105 + 3,    2·5 = 10 → 3')
j6 = I('j6', 'Only the remainders matter: $\\ 2-5=-3$, $\\ -3+7=4$', size=26, col=1, hand='Only the remainders :   2 − 5 = −3,    −3 + 7 = 4')
j7 = I('j7', 'Sum: $\\ 9+12=21$, $\\ 2+5=7\\to0$', size=26, col=1, hand='Sum :   9 + 12 = 21,    2 + 5 = 7 → 0')
j8 = I('j8', '$5-2=3$: the wrong order ✗', size=28, col=1, hand='5 − 2 = 3 :   the wrong order   ✗')
n1 = I('n1', '$a=9,\\ \\ b=5$: $\\ 9-5=\\hl{r}{4}$', hand='a = 9,   b = 5 :    9 − 5 = \\hl{r}{4}')
n2 = I('n2', '$a=16,\\ \\ b=12$: $\\ 16-12=\\hl{r}{4}$', hand='a = 16,   b = 12 :    16 − 12 = \\hl{r}{4}')
n3 = I('n3', 'Different pairs, the same remainder', size=28, col=1)
video('solve-q-r26-t15-01', 'solution', qid='q-r26-t15-01', slides=[
    S('Method 1 · Tag it',
      L("a and b are positive integers, and a is bigger than b. When a is divided by seven, the remainder is two. When b is "
        "divided by seven, the remainder is five. What will be the remainder if a minus b is divided by seven?",
        pt('stem', 'a and b are', 'hl', 11.0), voice='calm', pause=0.5),
      L("So we know the remainders of a and b, and they ask for the remainder of their difference. And one of the choices "
        "says it can't be determined. [short pause] We'll solve it two ways, writing each number as a tag, and then "
        "plugging in numbers.", pt('stem: ask', 'the remainder of their difference'), pt('choice 1', "it can't be determined")),
      L("[short pause] Let's start with the tags. Remember, a number that leaves two when divided by seven is seven k plus "
        "two, full sevens plus two. And b is seven m plus five. Why m and not k again? a and b are different numbers, so "
        "they get different letters.", show(j1, 'seven k plus two'), show(j2, 'Why m and not k')),
      L("Now subtract. a minus b is seven k minus seven m, plus two minus five. The sevens stay sevens, so seven times, in "
        "brackets, k minus m. And two minus five is negative three.", show(j3, 'Now subtract'), show(j4, 'The sevens stay sevens')),
      sb='Method 1 · Tag it'),
    S('Method 1 · Tag it',
      L("But a remainder can't be negative. Dividing by seven, it's zero to six. So add the divisor, seven. Negative three plus seven is four. Why is that allowed? Adding a full seven never changes the remainder. Four leaves four, and eleven, four plus seven, leaves four too. So a minus b is full sevens, plus four, and the remainder is four, for every pair.", show(j5, 'So add the divisor'), mk('circle', 'j5: r', 'plus four')),
      L("Let's check it with an actual division. Twenty-three leaves two, because three sevens are twenty-one. Twelve leaves "
        "five. Twenty-three minus twelve is eleven, and eleven divided by seven leaves four, because eleven is seven plus four.",
        show(j9, 'Twenty-three leaves two')),
      L("So four, choice number four is our answer. And can't be determined is out, because it's four for every pair.",
        mk('tick', 'choice 4', 'choice number four is our answer'), mk('cross', 'choice 1', "can't be determined is out")),
      L("And what does that mean? Only the remainders matter. For a difference, subtract the remainders, two minus five, "
        "negative three. A negative result? Add the divisor. Negative three plus seven is four. For a sum, add them. Nine leaves two and twelve leaves five, and nine plus twelve is twenty-one, three sevens. Two plus five is seven, and that leaves zero, the same. For a product, multiply them. Nine times twelve is a hundred eight, fifteen sevens and three. And two times five is ten, which also leaves three.", show(j6, 'Only the remainders matter'), show(j7, 'For a sum, add them'), show(j10, 'For a product, multiply them')),
      L("Now careful with the order. A lot of students do five minus two, which is three, and that's choice number three, the trap. "
        "It's a minus b, so it's two minus five.", show(j8, 'careful with the order'), mk('cross', 'choice 3', 'the trap')),
      sb='Method 1 · Tag it'),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers. I need an a that leaves two, so nine, which is seven plus two. And a b "
        "that leaves five and is smaller than a, so five itself. Nine minus five is four, and four divided by seven leaves "
        "four.", show(n1, 'so nine, which is seven')),
      L("Since one choice says it can't be determined, let's try a different pair. Sixteen, which is fourteen plus two, and "
        "twelve, which is seven plus five. Sixteen minus twelve is four again.", show(n2, 'Sixteen, which is'), show(n3, 'four again')),
      L("Different pairs, the same remainder, so choice number four. [pause] Okay. I'll see you in the next question.",
        mk('tick', 'choice 4', 'so choice number four'))),
])

# ------------------------------------------------------------------------------------------------ r26-t15-remainder-tools (lesson)
# 2026-10-11 (teacher: "make sure they really understand ... enough examples"): only the two tools no question video
# teaches stay here, each with two examples, the why and the trap - take away the remainder, and the tag for "divisible by
# both" (the LCM). Numbers in a row moved into q-432 and "a sum keeps only the shared factor" into q-r26-t15-15, where
# they are first used.  REMINDER: the remainder (camera lesson), the LCM by primes (topic 14).
l1 = I('l1', '$61=56+5$ $\\ \\to\\ 61-5=56=7\\cdot8$ ✓', size=40, hand='61 = 56 + 5   →   61 − 5 = 56 = 7·8   ✓')
l2 = I('l2', '$47=42+5$ $\\ \\to\\ 47-5=42=6\\cdot7$ ✓', size=40, hand='47 = 42 + 5   →   47 − 5 = 42 = 6·7   ✓')
l3 = I('l3', 'Take away the remainder: what is left divides exactly', size=34)
l4 = I('l4', 'Leaves $3$ by $4$: $\\ x-3$ divides by $4$ $\\quad 15-3=12$', size=34, hand='Leaves 3 by 4 :   x − 3  divides by 4      15 − 3 = 12')
t1 = I('t1', 'By $4$ and by $6$: $\\ 4=2^2,\\ \\ 6=2\\cdot3$ $\\ \\to\\ 2^2\\cdot3=12$', size=34, hand='By 4 and by 6 :    2^2 · 3 = 12')
t2 = I('t2', '$12,\\ 24,\\ 36,\\ 48$ ✓ $\\quad 24k$ misses $12$ and $36$', size=36, hand='12,  24,  36,  48  ✓      24k  misses  12  and  36')
t3 = I('t3', 'By $3$ and by $5$: $\\ 15k$ $\\quad 15,\\ 30,\\ 45$', size=36, hand='By 3 and by 5 :    15k      15,  30,  45')
video('r26-t15-remainder-tools', 'lesson', slides=[
    S('More Remainder Tools',
      L("Welcome back. Before the advanced questions, two short tools. The other tools you'll learn inside the questions that "
        "use them.")),
    S('Take away the remainder',
      L("First tool. If a number leaves a remainder, take the remainder away, and what's left divides exactly. Sixty-one "
        "divided by eight. Seven eights are fifty-six, so it leaves five. Sixty-one minus five is fifty-six, and that's seven "
        "times eight, no remainder.", show(l1, 'Sixty-one divided by eight')),
      L("Another one. Forty-seven divided by six. Seven sixes are forty-two, so it leaves five. Forty-seven minus five is "
        "forty-two, six times seven.", show(l2, 'Forty-seven divided by six')),
      L("Why does it work? The remainder is the only part that doesn't divide. Take it away, and only full groups are left.",
        show(l3, 'the only part that doesn')),
      L("So when a question says a number leaves three when divided by four, you know that the number minus three divides "
        "by four. Fifteen leaves three, and fifteen minus three is twelve, three fours.", show(l4, 'leaves three when divided by four'))),
    S('Divisible by both',
      L("Second tool. A number divisible by four and by six. Is it divisible by twenty-four? Not necessarily. Remember the "
        "LCM from primes, every prime at its higher power. Four is two squared, and six is two times three. So two squared times three, which is twelve.", show(t1, 'A number divisible by four and by six')),
      L("So the number is a multiple of twelve, twelve k. Twelve, twenty-four, thirty-six, forty-eight, all divide by four "
        "and by six. Twenty-four k would miss twelve and thirty-six, and they do divide by both.", show(t2, 'Twelve, twenty-four, thirty-six')),
      L("And when the two share nothing, just multiply. Divisible by three and by five is fifteen k, fifteen, thirty, "
        "forty-five. [pause] Okay. I'll see you in the next video.", show(t3, 'Divisible by three and by five'))),
])

# ------------------------------------------------------------------------------------------------ q-427 (Q6)
# NEW: a percent of a group -> a fraction -> build from the inside (a tenth = k, tennis = 3k) -> divisible by 3, with two
# examples (clubs of 50 and 70).  REMINDER: percent as a fraction (topic 23), the digit-sum sign for 3 (camera lesson).
p1 = I('p1', '$30\\%=\\frac{30}{100}=\\frac{3}{10}$', hand='30% = {30/100} = {3/10}')
p2 = I('p2', 'Club: $\\ 10k\\qquad$ Tennis: $\\ \\hl{t}{3k}$', hand='Club :   10k        Tennis :   \\hl{t}{3k}')
p6 = I('p6', '$50$: $\\ \\frac{50}{10}=5$, $\\ 3\\cdot5=15\\qquad 70$: $\\ 3\\cdot7=21$', size=28, col=1, hand='50 :  3·5 = 15        70 :  3·7 = 21')
p3 = I('p3', 'Divisible by $3$: digit sum', size=28, col=1)
p4 = I('p4', '$530$: $\\ 5+3+0=8$ ✗', hand='530 :   5 + 3 + 0 = 8   ✗')
p5 = I('p5', '$540$: $\\ 5+4+0=\\hl{n}{9}$ ✓', hand='540 :   5 + 4 + 0 = \\hl{n}{9}   ✓')
video('solve-q-427', 'solution', qid='q-427', slides=[
    S('A percent is a fraction',
      L("Thirty percent of the members of a sports club play tennis. Which of the following numbers could be the number of "
        "members who play tennis?", pt('stem', 'Thirty percent', 'hl', 7.0), voice='calm', pause=0.5),
      L("A percent question that's really a divisibility question. We don't know the size of the club, but the tennis "
        "players are a part of it, and a part of a group has to be a whole number of people. So first, let's turn the "
        "percent into a fraction.", pt('stem: ask', 'divisibility question'), pt('stem', 'a part of a group')),
      L("Thirty percent is thirty over a hundred, and that's three tenths.", show(p1, 'thirty over a hundred'), voice='calm'),
      L("Now build it from the inside. Call a tenth of the club k, a whole number of people. Then the club has ten k "
        "members, and three k of them play tennis. So the number of tennis players is always a multiple of three.",
        show(p2, 'Call a tenth of the club k'), mk('circle', 'p2: t', 'always a multiple of three')),
      L("Let's see it in numbers. A club of fifty members, a tenth is five, and three tenths is three times five, which is fifteen. "
        "A club of seventy, a tenth is seven, and three times seven is twenty-one. Fifteen and twenty-one, both multiples of "
        "three.", show(p6, 'A club of fifty')),
      L("And remember the sign for three, the digit sum divides by three. Five thirty, five plus three plus zero is eight, "
        "and eight doesn't divide by three. Choice number one is out.", show(p3, 'the sign for three'), show(p4, 'Five thirty'),
        mk('cross', 'choice 1', 'Choice number one is out')),
      L("Five forty, five plus four plus zero is nine, and nine divides by three. And a question has one correct answer, so "
        "there's no need to check the other two. Choice number two is our answer. [pause] Okay. I'll see you in the next "
        "question.", show(p5, 'Five forty'), mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-428 (Q7)
# NEW: an unknown digit and the digit sum - hop by 3 through the possible sums, and stop at the largest digit, 9;
# "both 2 and 3" (12 tokens); the trap 3 (forgetting "even").  REMINDER: signs for 2 and 3, 6 = 2 and 3 (camera).
q1 = I('q1', '$12$ tokens: $\\ $by $2$ AND by $3$', size=30, col=1, hand='12 tokens :   by 2  AND  by 3')
q2 = I('q2', '$6+1+X=7+X$', hand='6 + 1 + X = 7 + X')
q3 = I('q3', '$7+X=9,\\ \\ 12,\\ \\ 15$ $\\ \\to\\ X=2,\\ 5,\\ 8$', size=32, hand='7 + X = 9,  12,  15   →   X = 2,  5,  8')
q4 = I('q4', '$X\\le9$: $\\ 7+X\\le16$', size=28, col=1, hand='X ≤ 9 :    7 + X ≤ 16')
q5 = I('q5', '$612$ ✓ $\\quad 615$ ✗ odd $\\quad 618$ ✓', hand='612  ✓      615  ✗ odd      618  ✓')
q6 = I('q6', 'Even: $\\ X=0,\\ 2,\\ 4,\\ 6,\\ 8$', hand='Even :    X = 0,  2,  4,  6,  8')
q7 = I('q7', 'Digit sums: $\\ 7,\\ \\hl{a}{9},\\ 11,\\ 13,\\ \\hl{b}{15}$', hand='Digit sums :    7,  \\hl{a}{9},  11,  13,  \\hl{b}{15}')
video('solve-q-428', 'solution', qid='q-428', slides=[
    S('Method 1 · Divisible by 3 first',
      L("A game machine shows a three-digit number. Its hundreds digit is six, its tens digit is one, and its units digit is "
        "X. The machine pays four tokens if the number is divisible by two but not by three, eight tokens if it is divisible "
        "by three but not by two, and twelve tokens if it is divisible by both two and three. Noa played once and won twelve "
        "tokens. How many different values can X have?", pt('stem', 'A game machine', 'hl', 20.0), voice='calm', pause=0.5),
      L("A long story, but the only thing that matters is the twelve tokens. Twelve tokens means the number divides by two "
        "and by three. [short pause] We'll solve it two ways, with three first, and then with two first.",
        pt('stem', 'twelve tokens'), show(q1, 'divides by two and by three')),
      L("[short pause] Let's start with three. The digit sum must divide by three. Six plus one is seven, so the sum is seven "
        "plus X.", show(q2, 'Six plus one is seven')),
      L("X is one digit, zero to nine, so seven plus X is between seven and sixteen. The multiples of three in there are "
        "nine, twelve and fifteen. So X is two, five or eight.", show(q4, 'between seven and sixteen'), show(q3, 'nine, twelve and fifteen')),
      sb='Method 1 · Divisible by 3 first'),
    S('Method 1 · Divisible by 3 first',
      L("Now two. Six one two ends in two, even. Six one five ends in five, odd, so it's out. Six one eight ends in eight, "
        "even. So X has two values, two and eight, and choice number two is our answer.",
        show(q5, 'Six one two'), mk('tick', 'choice 2', 'choice number two is our answer')),
      L("Now careful, three is the trap. Those are the three digits that work for three, but five makes an odd number.",
        mk('cross', 'choice 3', 'three is the trap'))),
    S('Method 2 · Even first',
      L("[pause] Another way is to start with two. The number must be even, so X is zero, two, four, six or eight.", show(q6, 'start with two')),
      L("Now the digit sums. Seven plus zero is seven, seven plus two is nine, seven plus four is eleven, seven plus six is thirteen, and seven plus eight is fifteen. Only nine and fifteen divide by three, so X is two or eight. Two values, choice number two. "
        "[pause] Okay. I'll see you in the next question.", show(q7, 'Now the digit sums'), mk('circle', 'q7: a', 'Only nine'),
        mk('circle', 'q7: b', 'and fifteen divide'), mk('tick', 'choice 2', 'Two values, choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-429 (Q8)
# NEW: a divisor with no sign - build it from parts with no common factor (12 = 3·4) and let the part that differs
# decide; one correct answer (R35).  REMINDER: building divisors, the trap 2·6 (camera lesson), signs for 3 and 4.
w1 = I('w1', '$12=3\\cdot4$ $\\ $(not $2\\cdot6$)', hand='12 = 3·4     (not 2·6)')
w2 = I('w2', '$6,\\ 18$: by $2$ and by $6$, not by $12$', size=28, col=1, hand='6, 18 :   by 2 and by 6,  not by 12')
w7 = I('w7', '$36$: $\\ 36$ ✓ by $4$, $\\ 3+6=9$ ✓ $\\to\\ 36=3\\cdot12$', size=28, col=1, hand='36 :   by 4 ✓,   3 + 6 = 9 ✓   →   36 = 3·12')
w3 = I('w3', 'Last two digits: $\\ 28,\\ 52,\\ 72,\\ 16$ ✓', hand='Last two digits :   28,  52,  72,  16   ✓')
w4 = I('w4', 'All divide by $4$: the $3$ decides', size=28, col=1)
w5 = I('w5', '$1428$: $\\ 1+4+2+8=15$ ✓', hand='1428 :   1 + 4 + 2 + 8 = 15   ✓')
w6 = I('w6', '$3152$: $\\ 3+1+5+2=\\hl{e}{11}$ ✗', hand='3152 :   3 + 1 + 5 + 2 = \\hl{e}{11}   ✗')
video('solve-q-429', 'solution', qid='q-429', slides=[
    S('Build 12 from 3 and 4',
      L("Which of the following numbers is not divisible by twelve?", pt('stem', 'Which', 'hl', 3.0), voice='calm', pause=0.5),
      L("Twelve has no sign of its own. We could divide each choice by twelve, but that's slow. So let's build twelve from "
        "signs we know.", pt('stem: ask', 'Twelve has no sign'), pt('choice 1', 'divide each choice')),
      L("Remember, split it into parts with no common factor. Twelve is three times four. Let's see it in numbers. Thirty-six, the last two digits are thirty-six, which divides by four, and three plus six is nine, which divides by three. And really, thirty-six is three twelves. Why not two times six? Two and six share a two. Six itself divides by two and by six, and not by twelve. Eighteen too, it divides by two and by six, and eighteen over twelve isn't whole.", show(w1, 'Twelve is three times four'), show(w7, 'Thirty-six, the last'), show(w2, 'Six itself')),
      L("Four first, the last two digits. Twenty-eight, fifty-two, seventy-two and sixteen all divide by four. So four "
        "can't tell them apart, and three decides.", show(w3, 'the last two digits'), show(w4, 'three decides')),
      L("Three, the digit sum. One plus four plus two plus eight is fifteen, and fifteen divides by three. So choice number "
        "one divides by twelve, and it's out.", show(w5, 'One plus four'), mk('cross', 'choice 1', "and it's out")),
      L("Three plus one plus five plus two is eleven, and eleven doesn't divide by three. So three thousand one hundred "
        "fifty-two isn't divisible by three, so not by twelve either. Choice number two is our answer. [pause] Okay. I'll "
        "see you in the next question.", show(w6, 'Three plus one plus five'), mk('circle', 'w6: e', 'is eleven'),
        mk('tick', 'choice 2', 'Choice number two is our answer'))),
])

# ------------------------------------------------------------------------------------------------ q-430 (Q9)
# NEW: counting multiples - from 1, it's a division (1 to 30, multiples of 5: 30 / 5 = 6); in a range, first and last
# multiple, last minus first plus one (why: 3 to 7 is five numbers); comparing by "one in every 15" vs "one in every 17".
# REMINDER: both 3 and 5 = 15 (no common factor, camera lesson).
x1 = I('x1', 'Both: $\\ 15,\\ \\ 21,\\ \\ 26$', size=28, col=1, hand='Both :    15,   21,   26')
x7 = I('x7', '$1$ to $30$, by $5$: $\\ 5,10,15,20,25,30$ $\\ \\to\\ \\frac{30}{5}=6$', size=28, hand='1 to 30,  by 5 :   5, 10, 15, 20, 25, 30   →   {30/5} = 6')
x6 = I('x6', '$3$ to $7$: $\\ 3,4,5,6,7$ $\\ \\to\\ 7-3+1=5$', size=28, hand='3 to 7 :   3, 4, 5, 6, 7   →   7 − 3 + 1 = 5')
x2 = I('x2', 'Three digits: $\\ 100$ to $999$', size=28, col=1)
x3 = I('x3', '$15\\cdot\\hl{f}{7}=105\\qquad 15\\cdot\\hl{l}{66}=900+90=990$', size=30, hand='15·\\hl{f}{7} = 105        15·\\hl{l}{66} = 900 + 90 = 990')
x5 = I('x5', '$66-7+1=\\hl{c}{60}$', size=30, hand='66 − 7 + 1 = \\hl{c}{60}')
y1 = I('y1', '$17$: $\\ 17\\cdot6=102$ to $17\\cdot58=1020-34=986$: $\\ 53$', size=28, hand='17 :   17·6 = 102  to  17·58 = 1020 − 34 = 986 :   53')
y3 = I('y3', '$21$: $\\ 21\\cdot5$ to $21\\cdot47=1050-63$: $\\ 43$', size=28, hand='21 :   21·5  to  21·47 = 1050 − 63 :   43')
y4 = I('y4', '$26$: $\\ 26\\cdot4$ to $26\\cdot38=1040-52$: $\\ 35$', size=28, hand='26 :   26·4  to  26·38 = 1040 − 52 :   35')
y5 = I('y5', '$60>53$ ✓ $\\quad 43>35$ ✓', size=30, col=1, hand='60 > 53  ✓      43 > 35  ✓')
z1 = I('z1', 'One in every $15$ $\\ >\\ $ one in every $17$', size=30, hand='One in every 15   >   one in every 17')
z2 = I('z2', 'One in every $21$ $\\ >\\ $ one in every $26$', size=30, hand='One in every 21   >   one in every 26')
z3 = I('z3', 'Smaller divisor, more multiples', size=28, col=1)
z4 = I('z4', 'A long range: $900$ numbers', size=28, col=1)
video('solve-q-430', 'solution', qid='q-430', slides=[
    S('Method 1 · Count them',
      L("Yoav claims: there are more three-digit numbers divisible by both three and five, than three-digit numbers "
        "divisible by seventeen. Michal claims: there are more three-digit numbers divisible by both three and seven, than "
        "three-digit numbers divisible by both two and thirteen. Which of the following is correct?",
        pt('stem', 'Yoav claims', 'hl', 15.0), voice='calm', pause=0.5),
      L("So two claims about how many numbers divide by something. Divisible by both three and five means divisible by "
        "fifteen, because they share no factor. In the same way, three and seven make twenty-one, and two and thirteen make "
        "twenty-six. [short pause] We'll solve it two ways, counting the multiples, and then comparing without counting.",
        show(x1, 'divisible by fifteen'), pt('stem', 'how many numbers')),
      L("[short pause] Let's start with a small count. From one to thirty, how many multiples of five? Five, ten, fifteen, "
        "twenty, twenty-five, thirty, six of them. And that's just thirty over five, which is six.", show(x7, 'From one to thirty')),
      L("But here the range doesn't start at one. So I find the first and the last multiple, and count from one to the "
        "other. Last minus first, plus one. Why plus one? From three to seven there are five numbers, three, four, five, "
        "six, seven, and seven minus three is only four. Both ends count.", show(x6, 'From three to seven')),
      L("Fifteen. Fifteen times six is ninety, still two digits, so the first is fifteen times seven, which is a hundred five. And "
        "fifteen times sixty-six is nine hundred ninety, the last one below a thousand. So sixty-six minus seven is "
        "fifty-nine, and plus one is sixty.", show(x2, 'still two digits'), show(x3, 'the first is fifteen times seven'),
        show(x5, 'sixty-six minus seven'), mk('circle', 'x5: c', 'and plus one is sixty'))),
    S('Method 1 · Count them',
      L("Seventeen, the same way. Seventeen times six is a hundred two, and seventeen times fifty-eight is nine hundred "
        "eighty-six. Fifty-eight minus six is fifty-two, and plus one is fifty-three. Sixty is more than fifty-three, so "
        "Yoav is right.", show(y1, 'Seventeen times six')),
      L("Michal. Twenty-one times five is a hundred five, and twenty-one times forty-seven is nine hundred eighty-seven. "
        "Forty-seven minus five is forty-two, and plus one is forty-three. Twenty-six times four is a hundred four, and "
        "twenty-six times thirty-eight is nine hundred eighty-eight. Thirty-eight minus four is thirty-four, and plus one is "
        "thirty-five.", show(y3, 'Twenty-one times five'), show(y4, 'Twenty-six times four')),
      L("Forty-three is more than thirty-five, so Michal is right too. Both are right, choice number three.",
        show(y5, 'Forty-three is more'), mk('tick', 'choice 3', 'choice number three')),
      sb='Method 1 · Count them'),
    S('Method 2 · Compare without counting',
      L("[pause] Another way, without counting at all. Every fifteenth number divides by fifteen, and every seventeenth "
        "divides by seventeen. One in every fifteen is more than one in every seventeen. So fifteen has more multiples, "
        "and Yoav is right.", show(z1, 'One in every fifteen')),
      L("The same for Michal. One in every twenty-one is more than one in every twenty-six. So the smaller the divisor, the "
        "more multiples it has, and both are right.", show(z2, 'One in every twenty-one'), show(z3, 'the smaller the divisor')),
      L("Why can we trust it here? The range is long, nine hundred numbers, so the difference is big. In a short range, "
        "count exactly. Choice number three. [pause] Okay. I'll see you in the next question.",
        show(z4, 'The range is long'), mk('tick', 'choice 3', 'Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-431 (Q10)
# NEW: write every letter with one letter (b = 5a, c = 4a), then a sum is a number times a; "always by 6" is not "by 12";
# one example where a claim fails is enough for "not necessarily true".  REMINDER: tag it (the tools lesson).
k1 = I('k1', '$c=\\hl{c}{4a}$ $\\ \\to\\ $ divisible by $4$ ✓', hand='c = \\hl{c}{4a}   →   divisible by 4   ✓')
k2 = I('k2', '$a=\\frac{b}{5}$ $\\ \\to\\ b=\\hl{b}{5a}$ ✓', hand='a = {b/5}   →   b = \\hl{b}{5a}   ✓')
k3 = I('k3', '$a+b=a+5a=\\hl{s}{6a}$', hand='a + b = a + 5a = \\hl{s}{6a}')
k4 = I('k4', '$a=1$: $\\ 6$, not by $12$ ✗', hand='a = 1 :    6,   not by 12   ✗')
k5 = I('k5', '$a+b+c=a+5a+4a=10a$ ✓', size=32, hand='a + b + c = a + 5a + 4a = 10a   ✓')
k6 = I('k6', 'One letter: $\\ b=5a,\\ \\ c=4a$', size=28, col=1, hand='One letter :   b = 5a,   c = 4a')
m1 = I('m1', '$b=5$: $\\ a=1,\\ \\ c=4$', hand='b = 5 :    a = 1,    c = 4')
m2 = I('m2', '$c=4$ ✓ $\\quad b=5$ ✓', hand='c = 4  ✓       b = 5  ✓')
m4 = I('m4', '$a+b=1+5=6$ ✗ $\\quad a+b+c=10$ ✓', size=32, hand='a + b = 1 + 5 = 6  ✗      a + b + c = 10  ✓')
m3 = I('m3', 'One example where it fails is enough', size=28, col=1)
video('solve-q-431', 'solution', qid='q-431', slides=[
    S('Method 1 · One letter',
      L("Given: c is equal to four a, and a is equal to b over five. a, b and c are positive integers. Which claim is not "
        "necessarily true?", pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("So three letters tied together, and we're looking for the claim that doesn't have to be true. One example where "
        "it fails is enough to show that. [short pause] We'll solve it two ways, writing everything with one letter, and "
        "then plugging in numbers.", pt('stem: ask', "the claim that doesn't have to be true")),
      L("[short pause] Let's start with one letter, a. c is four a, so c is four times a whole number. It always divides by "
        "four, so choice number one is always true. Out.", pt('stem: g1', 'c is four a'), show(k6, "Let's start with one letter"), show(k1, 'c is four a, so'),
        mk('cross', 'choice 1', 'always true. Out')),
      L("a is b over five. Multiply both sides by five, and b is five a. So b always divides by five. Choice number two is "
        "out too.", pt('stem: g2', 'a is b over five'), show(k2, 'Multiply both sides by five'), mk('cross', 'choice 2', 'out too')),
      L("Now a plus b. That's a plus five a, which is six a. Six a always divides by six, but by twelve? Only when a is even. If a is two, a plus b is twelve, and that works. But if a is one, a plus b is six, and six doesn't divide by twelve. So this claim can fail, and choice number three is our "
        "answer.", pt('choice 3', 'Now a plus b'), show(k3, "That's a plus five a"), show(k4, 'If a is one'), mk('tick', 'choice 3', 'choice number three is our answer')),
      sb='Method 1 · One letter'),
    S('Method 1 · One letter',
      L("In the exam you'd circle it and move on. Here, the last one is a nice check of the idea. a plus b plus c is a plus five a plus four a, which is ten a. Always divisible by ten.", show(k5, 'a plus b plus c is'), mk('cross', 'choice 4', 'Always divisible by ten'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers. Start with the tricky condition, b over five has to be a whole number. "
        "So b divides by five, and the easiest is b is five. Then a is one, and c is four times one, which is four.",
        pt('stem: g2', 'b over five has to be'), show(m1, 'b is five')),
      L("c is four, divisible by four. b is five, divisible by five. a plus b is one plus five, which is six, not divisible by twelve. "
        "And a plus b plus c is ten, divisible by ten.", show(m2, 'c is four, divisible'), show(m4, 'a plus b is one plus five')),
      L("So the third claim fails with these numbers, and one failing example is all we need. Choice number three. [pause] "
        "Okay. I'll see you in the next question.", show(m3, 'one failing example'), mk('tick', 'choice 3', 'Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t15-15 (Q11)
# NEW (full, moved here from the tools lesson): a sum of tags keeps only the shared factor (why; 6k + 9m and 4k + 6m; a
# product of tags multiplies); the trap of equal values (x = y = 18); plugging in, different letters get different values.
# REMINDER: tags like 6k (camera lesson).
u1 = I('u1', '$x=6k,\\ \\ \\ y=9m$', hand='x = 6k,      y = 9m')
u2 = I('u2', '$x+y=6k+9m=\\hl{t}{3}(2k+3m)$', hand='x + y = 6k + 9m = \\hl{t}{3}(2k + 3m)')
u3 = I('u3', '$2k+3m$: $\\ 5,\\ 7$ $\\ $unknown', hand='2k + 3m :    5,   7    unknown')
u4 = I('u4', 'A sum keeps only the shared factor', size=28, col=1)
u5 = I('u5', '$4k+6m=2(2k+3m)$: $\\ 4+6=10$', size=28, col=1, hand='4k + 6m = 2(2k + 3m) :    4 + 6 = 10')
u6 = I('u6', 'Multiply: $\\ 6k\\cdot9m=54km$', size=28, col=1, hand='Multiply :    6k · 9m = 54km')
v1 = I('v1', '$6+9=15$: $\\ $not by $18$, not by $9$', size=32, hand='6 + 9 = 15 :   not by 18,  not by 9')
v2 = I('v2', '$12+9=21$: $\\ $not by $15$', size=32, hand='12 + 9 = 21 :   not by 15')
v3 = I('v3', 'Trap: $\\ 18+18=36$ ✗', size=30, col=1, hand='Trap :   18 + 18 = 36   ✗')
v4 = I('v4', 'Independent values: do not assume they are equal', size=26, col=1)
video('solve-q-r26-t15-15', 'solution', qid='q-r26-t15-15', slides=[
    S('Method 1 · Tag it',
      L("x and y are positive integers. x is divisible by six, and y is divisible by nine. What is the largest number that "
        "x plus y is necessarily divisible by?", pt('stem', 'x and y are', 'hl', 8.0), voice='calm', pause=0.5),
      L("So we add two multiples, and they want the largest number that always divides the sum. [short pause] We'll solve "
        "it two ways, with tags, and then plugging in numbers.", pt('stem: ask', 'the largest number that always divides')),
      L("[short pause] Let's start with the tags. x is six k, and y is nine m. "
        "We use separate letters because each multiple can be chosen independently. Nothing says k and m are equal. "
        "They may happen to be equal, but we cannot require it.", show(u1, 'x is six k')),
      L("Now, when we add two tags, only the factor they share comes out for sure. Six and nine share a three. So six k plus nine m is three times, in brackets, two k plus three m. Why only the three? What's in the brackets changes with k and m.", show(u4, 'only the factor they share'), show(u2, 'Six and nine share')),
      L("Let's see the rule once more, changing one thing. Multiples of four and of six. Four k plus six m, they share a two, "
        "so two times, in brackets, two k plus three m. Only the two is certain. Four plus six is ten, and ten doesn't even "
        "divide by four. And if we multiplied instead, the tags would multiply, six k times nine m is fifty-four k m.",
        show(u5, 'Multiples of four and of six'), show(u6, 'if we multiplied instead')),
      L("And two k plus three m? With k and m one, it's five, and with k two and m one, it's seven. "
        "The bracket changes, and five and seven share no factor greater than one. "
        "So no extra factor from the bracket is guaranteed. Only the three in front is certain. Three, choice number three is our answer.",
        show(u3, 'With k and m one'), mk('circle', 'u2: t', 'only the three in front'), mk('tick', 'choice 3', 'choice number three is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers, with a different value for each letter. x is six and y is nine. Six "
        "plus nine is fifteen, and fifteen doesn't divide by eighteen or by nine. So choice numbers one and four are out.",
        show(v4, 'a different value for each letter'), show(v1, 'Six plus nine'), mk('cross', 'choice 1', 'choice numbers one'), mk('cross', 'choice 4', 'and four are out')),
      L("Fifteen does divide by fifteen, so I need one more pair. x is twelve and y is nine. Twelve plus nine is twenty-one, "
        "and twenty-one doesn't divide by fifteen. Out. So three, choice number three.",
        show(v2, 'Twelve plus nine'), mk('cross', 'choice 2', 'by fifteen. Out'), mk('tick', 'choice 3', 'So three, choice number three')),
      L("Now careful, here's how students fall into choice number one. They take one number for both, eighteen and eighteen. "
        "Eighteen plus eighteen is thirty-six, and it divides by eighteen, so eighteen looks certain. But x and y are "
        "different letters, and nothing says they're equal. [pause] Okay. I'll see you in the next question.",
        show(v3, 'eighteen and eighteen'), pt('choice 1', 'eighteen looks certain'))),
])

# ------------------------------------------------------------------------------------------------ q-432 (Q12)
# NEW (full, moved here from the tools lesson): numbers in a row - two in a row divide by 2 (7·8, 4·5), three in a row by
# 6 (why; 4·5·6, 7·8·9), the non-example 3·5; a hidden product of three in a row (5(a-1)a(a+1)) -> 30; don't plug in
# a = 1 (it gives 0).  REMINDER: consecutive numbers (topic 1), the shortcut formula (topic 4), plugging in (topic 51).
o1 = I('o1', '$5a^3-5a=5a(a^2-1)$', hand='5a^3 − 5a = 5a(a^2 − 1)')
o2 = I('o2', '$=5(a-1)\\,a\\,(a+1)$', hand='= 5 (a−1) a (a+1)')
o8 = I('o8', 'Two in a row: one is even $\\to$ divisible by $2$', size=28, col=1)
o9 = I('o9', '$7\\cdot8=56\\qquad 4\\cdot5=20$', size=32, hand='7·8 = 56        4·5 = 20')
o10 = I('o10', 'Three in a row: by $3$ and by $2$ $\\to$ by $6$', size=28, col=1)
o11 = I('o11', '$4\\cdot5\\cdot6=120=6\\cdot20\\qquad 7\\cdot8\\cdot9=504=6\\cdot84$', size=28, hand='4·5·6 = 120 = 6·20       7·8·9 = 504 = 6·84')
o12 = I('o12', 'Not in a row: $\\ 3\\cdot5=15$ ✗', size=28, col=1, hand='Not in a row :   3·5 = 15   ✗')
o4 = I('o4', '$5\\cdot6=\\hl{t}{30}$', size=32, hand='5·6 = \\hl{t}{30}')
o5 = I('o5', '$a=1$: $\\ 5-5=0$ ✗', size=30, col=1, hand='a = 1 :   5 − 5 = 0   ✗')
o6 = I('o6', '$a=2$: $\\ 5\\cdot8-5\\cdot2=40-10=\\hl{t}{30}$', hand='a = 2 :   5·8 − 5·2 = 40 − 10 = \\hl{t}{30}')
o7 = I('o7', '$60$ ✗ $\\quad 40$ ✗ $\\quad 30$ ✓ $\\quad 20$ ✗', hand='60 ✗      40 ✗      30 ✓      20 ✗')
video('solve-q-432', 'solution', qid='q-432', slides=[
    S('Method 1 · Three in a row',
      L("Given: x is equal to five a cubed minus five a, and a is a positive integer. x is necessarily divisible by:",
        pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("So x is an expression with a cube, and they ask what always divides it. To see what always divides, we turn the "
        "expression into a product. [short pause] We'll solve it two ways, factoring, and then plugging in a number.",
        pt('stem', 'an expression with a cube'), pt('stem', 'what always divides')),
      L("[short pause] Let's start by factoring. Five a is in both terms, so take it out. Five a times, in brackets, a "
        "squared minus one.", show(o1, 'Five a is in both terms')),
      L("And a squared minus one is the shortcut formula, a minus one, times a plus one. So x is five, times a minus one, "
        "times a, times a plus one.", show(o2, 'the shortcut formula')),
      L("a minus one, a, and a plus one are three numbers in a row. And numbers in a row have a rule we haven't met yet. "
        "Let's build it.", pt('o2', 'three numbers in a row')),
      sb='Method 1 · Three in a row'),
    S('Method 1 · Three in a row',
      L("Two numbers in a row, and one of them is always even, because even and odd take turns. Seven and eight, eight is "
        "even, so seven times eight, which is fifty-six, is even. Four and five, four is even, and four times five is twenty. So two "
        "in a row always divide by two.", show(o8, 'Two numbers in a row'), show(o9, 'Seven and eight')),
      L("Three in a row. Every third number divides by three, so one of the three does. And at least one is even. Two and "
        "three share no factor, so the product divides by six. Four times five times six is a hundred twenty, twenty sixes. "
        "Seven times eight times nine is five hundred four, eighty-four sixes.", show(o10, 'Three in a row. Every third'), show(o11, 'Four times five times six')),
      L("Now careful, only numbers in a row. Three times five skips a number, it's fifteen, and fifteen isn't even.",
        show(o12, 'only numbers in a row')),
      L("So x is five times three in a row, five times a multiple of six. It always divides by five times six, which is thirty. "
        "Choice number three is our answer.", show(o4, 'five times six'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Plugging in a number',
      L("[pause] Now let's try plugging in a number. Careful, not a is one. Five minus five is zero, and zero divides by "
        "every choice, so it can't rule anything out.", show(o5, 'not a is one')),
      L("So a is two. Two cubed is eight, five times eight is forty, five times two is ten, and forty minus ten is thirty.",
        show(o6, 'So a is two'), voice='calm'),
      L("Thirty doesn't divide by sixty, by forty or by twenty, so those three are out, and only choice number three is "
        "left. [pause] Okay. I'll see you in the next question.", show(o7, "Thirty doesn't divide"), mk('cross', 'choice 1', 'by sixty'),
        mk('cross', 'choice 2', 'by forty'), mk('cross', 'choice 4', 'or by twenty'), mk('tick', 'choice 3', 'only choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-433 (Q13)
# NEW: divisible by 10 -> ends in 0 -> 14a ends in 4 -> 4 times the last digit of a ends in 4 -> the last digit is 1 or
# 6 (no need to work out 14a, R35).  REMINDER: the last digit of a product (topic 1), the sign for 10 (camera lesson).
s1 = I('s1', 'Divisible by $10$: ends in $0$', size=28, col=1)
s2 = I('s2', '$14a+6$ ends in $0$ $\\ \\to\\ 14a$ ends in $\\hl{f}{4}$', hand='14a + 6  ends in 0   →   14a  ends in \\hl{f}{4}')
s3 = I('s3', '$4\\cdot1=4\\qquad 4\\cdot6=2\\hl{f}{4}$', hand='4·1 = 4        4·6 = 2\\hl{f}{4}')
s4 = I('s4', 'The last digit of $a$: $\\ 1$ or $6$', hand='The last digit of a :    1  or  6')
s5 = I('s5', 'Last digits only', size=28, col=1)
s6 = I('s6', '$3$: $\\ 12\\to2+6=8$ ✗', size=30, hand='3 :   12 → 2 + 6 = 8   ✗')
s7 = I('s7', '$4$: $\\ 16\\to6+6=12$ ✗', size=30, hand='4 :   16 → 6 + 6 = 12   ✗')
s8 = I('s8', '$5$: $\\ 20\\to0+6=6$ ✗', size=30, hand='5 :   20 → 0 + 6 = 6   ✗')
video('solve-q-433', 'solution', qid='q-433', slides=[
    S('Method 1 · The last digit',
      L("Given: x is equal to fourteen a plus six, a is a positive integer, and x is divisible by ten. Which of the "
        "following could be the value of a?", pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("Divisible by ten, so it's all about the last digit. [short pause] We'll solve it two ways, working out which last "
        "digit a needs, and then testing the choices.", pt('stem', 'Divisible by ten')),
      L("[short pause] Let's start with the last digit. Remember the sign for ten, the last digit is zero. So fourteen a "
        "plus six ends in zero. And what plus six ends in zero? Something that ends in four. So fourteen a ends in four.",
        show(s1, 'the sign for ten'), show(s2, 'fourteen a plus six ends in zero')),
      L("And remember, the last digit of a product comes only from the last digits. So four times the last digit of a has "
        "to end in four. Four times one is four, and four times six is twenty-four. No other digit works.",
        show(s5, 'only from the last digits'), show(s3, 'Four times one is four')),
      L("So a ends in one or six. Only three hundred forty-six ends in six, so choice number four is our answer.",
        show(s4, 'a ends in one or six'), mk('tick', 'choice 4', 'choice number four is our answer'))),
    S('Method 2 · Test the choices',
      L("[pause] Another way is to test the choices, with last digits only. Three forty-three. Four times three is twelve, "
        "it ends in two, and two plus six is eight. x would end in eight, so it's out.", show(s6, 'Four times three'), mk('cross', 'choice 1', "so it's out")),
      L("Three forty-four. Four times four is sixteen, it ends in six, and six plus six is twelve, so x ends in two. Out. "
        "Three forty-five. Four times five is twenty, it ends in zero, and zero plus six is six. Out.",
        show(s7, 'Four times four'), mk('cross', 'choice 2', 'ends in two. Out'), show(s8, 'Four times five'), mk('cross', 'choice 3', 'plus six is six. Out')),
      L("Three choices are out, so three forty-six, choice number four. [pause] Okay. I'll see you in the next question.",
        mk('tick', 'choice 4', 'choice number four'))),
])

# ------------------------------------------------------------------------------------------------ q-434 (Q14)
# NEW: write what's left (900 - 6x) and take out the 6: what's left is a multiple of 6; or complete to 900 and check the
# paid part; the trap of checking only the 3.  REMINDER: 6 = 2 and 3 (camera lesson).
b1 = I('b1', 'Paid: $\\ x+2x+3x=6x$', hand='Paid :    x + 2x + 3x = 6x')
b2 = I('b2', 'Left: $\\ 900-6x=\\hl{s}{6}(150-x)$', hand='Left :    900 − 6x = \\hl{s}{6}(150 − x)')
b3 = I('b3', 'Left divides by $6$: $\\ $by $2$ and by $3$', size=28, col=1)
b4 = I('b4', '$15$: $\\ $odd ✗', hand='15 :   odd   ✗')
b5 = I('b5', '$24=6\\cdot4$ ✓', hand='24 = 6·4   ✓')
b6 = I('b6', 'Only $3$, not $2$? A trap', size=28, col=1)
c1 = I('c1', 'Paid $=900-$ left', hand='Paid = 900 − left')
c2 = I('c2', '$900-15=885$: $\\ $odd ✗', hand='900 − 15 = 885 :   odd   ✗')
c3 = I('c3', '$900-24=876$: $\\ $even, $\\ 8+7+6=21$ ✓', size=32, hand='900 − 24 = 876 :   even,   8 + 7 + 6 = 21   ✓')
video('solve-q-434', 'solution', qid='q-434', slides=[
    S('Method 1 · What is left',
      L("Yael loaded nine hundred points onto an amusement-park card. The first ride cost x points, the second ride cost "
        "two x points, and the third ride cost three x points. Which of the following could be the number of points left on "
        "her card after the three rides?", pt('stem', 'Yael loaded', 'hl', 13.0), voice='calm', pause=0.5),
      L("So a story with points, but underneath it's a divisibility question. Let's write what she paid, and what's left. "
        "[short pause] We'll solve it two ways, with what's left, and then with what she paid.", pt('stem', 'what she paid')),
      L("[short pause] Let's start with what's left. She paid x, then two x, then three x, so six x in all. Left on the "
        "card, nine hundred minus six x.", show(b1, 'She paid x')),
      L("Now, nine hundred is six times a hundred fifty. So I can take out the six. Nine hundred minus six x is six times, "
        "in brackets, a hundred fifty minus x. x is a whole number, so what's left is always a multiple of six.",
        show(b2, 'take out the six'), mk('circle', 'b2: s', 'always a multiple of six')),
      L("And a multiple of six divides by two and by three. Fifteen is odd, so it's out. Twenty-four is six times four, so "
        "it works. Choice number two is our answer.", show(b3, 'divides by two and by three'), show(b4, 'Fifteen is odd'),
        mk('cross', 'choice 1', "so it's out"), show(b5, 'Twenty-four is six times four'), mk('tick', 'choice 2', 'Choice number two is our answer')),
      L("Now careful, fifteen is the trap for anyone who checks only the three. Its digit sum is six, so it divides by three, "
        "but it's odd.", show(b6, 'checks only the three'))),
    S('Method 2 · What she paid',
      L("[pause] Another way is to complete each choice to nine hundred, and ask how much she paid. She paid six x, so the "
        "paid part has to divide by six.", show(c1, 'complete each choice')),
      L("Fifteen left means she paid nine hundred minus fifteen, which is eight hundred eighty-five. It's odd, so it doesn't divide by "
        "six. Out.", show(c2, 'Fifteen left means'), mk('cross', 'choice 1', 'Out.')),
      L("Twenty-four left means she paid nine hundred minus twenty-four, which is eight hundred seventy-six. It's even, and eight plus "
        "seven plus six is twenty-one, which divides by three. So it divides by six, and choice number two. [pause] Okay. "
        "I'll see you in the next question.", show(c3, 'Twenty-four left means'), mk('tick', 'choice 2', 'and choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-435 (Q15)
# NEW: claims about a new divisor - it must divide the old divisor to be known (8 -> 4 yes, 8 -> 12 no); one example
# (x = 4) proves a claim wrong, examples that work prove nothing.  REMINDER: the tag 8k + 4, changing the divisor
# (camera lesson), multiplying a remainder (q-r26-t15-01).
u1 = I('u1', 'If the new divisor divides $8$: $\\ $only the remainder matters', size=26, col=1)
u2 = I('u2', 'Yuval: $\\ 2\\cdot4=8$ ✓', hand='Yuval :    2 · 4 = 8   ✓')
u3 = I('u3', 'Noga: $\\ 4$ divides $8$: $\\ 4\\div4$ ✓', hand='Noga :    4 divides 8 :    4 ÷ 4   ✓')
u4 = I('u4', 'Itay: $\\ 12$ does not divide $8$', hand='Itay :    12  does not divide  8')
u5 = I('u5', '$x=4$: $\\ $not by $12$ ✗', hand='x = 4 :    not by 12   ✗')
e1 = I('e1', '$x=8k+4$', hand='x = 8k + 4')
e2 = I('e2', 'Yuval: $\\ 2x=16k+8=8(2k+1)$ ✓', size=32, hand='Yuval :    2x = 16k + 8 = 8(2k + 1)   ✓')
e3 = I('e3', 'Noga: $\\ x=4(2k+1)$ ✓', hand='Noga :    x = 4(2k + 1)   ✓')
e4 = I('e4', 'Itay: $\\ 4(2k+1)$, $\\ k=0$: $\\ 4$ ✗', hand='Itay :    4(2k + 1),    k = 0 :    4   ✗')
e6 = I('e6', 'For $12$ we need a $3$ inside $2k+1$: $\\ $not always', size=26, col=1)
f1 = I('f1', '$x=4,\\ \\ 12$', hand='x = 4,    12')
f2 = I('f2', '$2x=8,\\ 24$ ✓ $\\quad$ by $4$: ✓ ✓ $\\quad$ by $12$: $\\ 4$ ✗', size=30, hand='2x = 8, 24  ✓      by 4 :  ✓ ✓      by 12 :   4  ✗')
f3 = I('f3', 'Examples that work prove nothing. One that fails does', size=26, col=1)
video('solve-q-435', 'solution', qid='q-435', slides=[
    S('Method 1 · Understanding',
      L("When x is divided by eight, the remainder is four. Yuval claims: two x is necessarily divisible by eight. Noga "
        "claims: x is necessarily divisible by four. Itay claims: x is necessarily divisible by twelve. Which of the "
        "following is correct?", pt('stem', 'When x is', 'hl', 13.0), voice='calm', pause=0.5),
      L("So we know the remainder by eight, and three claims about other divisors. [short pause] We'll solve it three ways, "
        "by understanding, with algebra, and then plugging in numbers.", pt('stem', 'three claims')),
      L("[short pause] Let's start with understanding. x is full eights plus a remainder of four. When the new divisor "
        "divides eight, the full eights divide by it too, so only the remainder matters.", show(u1, 'When the new divisor')),
      L("Yuval, two x by eight. The same eight, so only the remainder counts, doubled. Two times four is eight, and eight "
        "divides by eight. Yuval is right.", pt('stem', 'Yuval'), show(u2, 'Two times four')),
      L("Noga, x by four. Four divides eight, so only the remainder matters. Four over four, no remainder. Noga is right.",
        pt('stem', 'Noga'), show(u3, 'Four divides eight')),
      sb='Method 1 · Understanding'),
    S('Method 1 · Understanding',
      L("Itay, x by twelve. Twelve doesn't divide eight, so from a remainder by eight we can't know the remainder by "
        "twelve. For example, x is four. Four divided by eight leaves four, and four doesn't divide by twelve. Itay is wrong.",
        pt('stem', 'Itay'), show(u4, "Twelve doesn't divide eight"), show(u5, 'x is four')),
      L("So only Itay is wrong, choice number two is our answer.", mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Algebra',
      L("[pause] Another way is algebra. What's different? Instead of thinking about the remainder, we write x as an "
        "expression and take out a common factor. x is full eights plus four, so x is eight k plus four.", show(e1, 'eight k plus four')),
      L("Yuval. Two x is sixteen k plus eight. Take out the eight, and it's eight times, in brackets, two k plus one. So it "
        "divides by eight. Yuval is right.", show(e2, 'Two x is sixteen k')),
      L("Noga. Take out a four from x, and it's four times, in brackets, two k plus one. So it divides by four. Noga is right.",
        show(e3, 'Take out a four')),
      sb='Method 2 · Algebra'),
    S('Method 2 · Algebra',
      L("Itay. x is four times two k plus one. For twelve, we'd need a three inside two k plus one, and it isn't always "
        "there. With k zero, two k plus one is one, and x is four, not divisible by twelve. Itay is wrong. Choice number two.",
        show(e4, 'With k zero'), show(e6, "we'd need a three"), mk('tick', 'choice 2', 'Itay is wrong. Choice number two'))),
    S('Method 3 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers that leave four when divided by eight, four and twelve.", show(f1, 'four and twelve')),
      L("Two x is eight or twenty-four, both divide by eight. Four and twelve both divide by four. But four doesn't divide by "
        "twelve, so Itay is wrong.", show(f2, 'Two x is eight')),
      L("Careful, examples that work don't prove Yuval and Noga right, the first two ways do. But one example that fails "
        "proves Itay wrong. So choice number two. [pause] Okay. I'll see you in the next question.", show(f3, "examples that work don't prove"),
        mk('tick', 'choice 2', 'So choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-436 (Q16)
# NEW: a sum divides by 6 exactly when its remainders add up to a multiple of 6; one counterexample (12, 5, 7).
# REMINDER: adding remainders (q-r26-t15-01), the biggest remainder (camera lesson).
g1 = I('g1', 'A sum: add the remainders', size=28, col=1)
g2 = I('g2', '(1) by $6$: $\\ $biggest remainder $5$ ✓', size=30, hand='(1)   by 6 :   biggest remainder 5   ✓')
g3 = I('g3', '(2) $12+5+7=24$', size=30, hand='(2)   12 + 5 + 7 = 24')
g4 = I('g4', 'Remainders $5+1=6$ ✗', size=30, hand='Remainders   5 + 1 = 6   ✗')
g5 = I('g5', '(3) $4+4+4=12$: $\\ 10+16+22=48$ ✓', size=30, hand='(3)   4 + 4 + 4 = 12 :   10 + 16 + 22 = 48   ✓')
g6 = I('g6', '(4) $0+0+?$ must be $0$ ✓', size=30, hand='(4)   0 + 0 + ?   must be 0   ✓')
video('solve-q-436', 'solution', qid='q-436', slides=[
    S('Think in remainders',
      L("The sum of three integers is divisible by six. Which of the following statements is not necessarily true?",
        pt('stem', 'The sum', 'hl', 6.0), voice='calm', pause=0.5),
      L("So we look for the statement that can fail, and one example where it fails is enough. And remember, when we add "
        "numbers, we can add their remainders. So the sum divides by six exactly when the remainders add up to zero, six, "
        "twelve, a multiple of six.", pt('stem: ask', 'the statement that can fail'), show(g1, 'add their remainders')),
      L("Choice number one, the greatest remainder by six is five. Always true, because the biggest remainder is one less "
        "than the divisor. Out.", show(g2, 'the greatest remainder'), mk('cross', 'choice 1', 'Out.')),
      L("Choice number two, if one of the numbers divides by six, then the other two do too. Let's try twelve, five and "
        "seven. Twelve plus five is seventeen, plus seven is twenty-four, and twenty-four divides by six. Twelve divides by "
        "six, but five and seven don't. Their remainders, five and one, add up to six, and that's enough.",
        show(g3, 'twelve, five and seven'), show(g4, 'Their remainders')),
      L("So this statement can fail, and choice number two is our answer.", mk('tick', 'choice 2', 'choice number two is our answer')),
      L("In the exam you'd circle it and move on. Here, the other two show the remainder idea. Choice number three, all three "
        "leave four. Four plus four plus four is twelve, a multiple of six, so it's possible. Ten, sixteen and twenty-two, "
        "and they add up to forty-eight. Out.", show(g5, 'Four plus four plus four'), mk('cross', 'choice 3', 'forty-eight. Out')),
      L("Choice number four, two of them divide by six. They bring no remainder, and the sum has none, so the third can't "
        "bring one either. Always true, out. [pause] Okay. I'll see you in the next question.",
        show(g6, 'They bring no remainder'), mk('cross', 'choice 4', 'Always true, out'))),
])

# ------------------------------------------------------------------------------------------------ r26-t15-summary
# REMINDERS only, said the way they were taught; new numbers.
y1s = I('y1s', '$2,\\ 5,\\ 10$: the last digit $\\qquad 3,\\ 9$: the digit sum', size=38)
y2s = I('y2s', '$4$: the last two digits $\\qquad 8$: the last three digits', size=38)
y3s = I('y3s', '$11$: $+\\,-\\,+\\,-$ gives $0$ or $\\pm11$ $\\quad 913$: $\\ 9-1+3=11$', size=36)
y4s = I('y4s', 'Bigger divisors: parts with no common factor $\\quad 36=4\\cdot9$, not $6\\cdot6$', size=34)
r1s = I('r1s', '$N=d\\cdot k+r,\\qquad 0\\le r<d$', size=42)
r2s = I('r2s', 'Biggest remainder $=$ divisor $-\\ 1$ $\\quad$ $5\\div8$: remainder $5$', size=36)
r3s = I('r3s', 'By $3$ or $9$: the digit sum $\\quad 4826$: $\\ 20\\to2$', size=36)
c1s = I('c1s', '$a$ leaves $5$, $b$ leaves $7$ (by $8$)', size=36)
c2s = I('c2s', '$a+b$: $\\ 12\\to4\\quad ab$: $\\ 35\\to3\\quad a-b$: $\\ -2+8=6$', size=36)
c3s = I('c3s', 'Take away the remainder: what is left divides', size=36)
c4s = I('c4s', 'By $12$ leaves $11$: by $4$ leaves $3$ $\\quad$ by $10$ $\\to$ by $4$: can\'t know', size=32)
n1s = I('n1s', 'Nested fractions with numerator $1$: multiply denominators', size=30)
n2s = I('n2s', 'Multiples in a range: last $-$ first $+\\ 1$', size=36)
n3s = I('n3s', 'Two in a row: $2$ $\\quad$ Three in a row: $6$ $\\quad a^3-a=(a-1)a(a+1)$', size=34)
n4s = I('n4s', 'Tag it: $6k+9m=3(2k+3m)$ $\\to$ only $3$', size=36)
n5s = I('n5s', 'Choose values independently; avoid $0$; look for counterexamples', size=30)
z1s = I('z1s', 'Parts with no common factor?', size=38)
z2s = I('z2s', 'Is my remainder smaller than the divisor?', size=38)
z3s = I('z3s', 'Negative remainder? Add the divisor.', size=38)
z4s = I('z4s', 'Does the new divisor divide the old one?', size=38)
video('r26-t15-summary', 'lesson', slides=[
    S('Division & Remainder: Summary',
      L("Before you practice, here's a quick summary of division and remainders. Everything important, in a few minutes.")),
    S('Divisibility signs',
      L("Two, five and ten, look at the last digit. Three and nine, the digit sum. Four, the last two digits, and eight, the "
        "last three.", show(y1s, 'Two, five and ten'), show(y2s, 'Four, the last two')),
      L("Eleven, go plus, minus, plus, minus, digit by digit. Nine thirteen, nine minus one plus three is eleven, so it "
        "divides by eleven.", show(y3s, 'Eleven, go plus')),
      L("A bigger divisor? Split it into parts with no common factor. Thirty-six is four times nine, not six times six.",
        show(y4s, 'A bigger divisor'))),
    S('Remainders',
      L("A number is the divisor times the quotient, plus the remainder, and the remainder is always smaller than the "
        "divisor. So the biggest remainder is the divisor minus one. And five divided by eight leaves five, not three.",
        show(r1s, 'the divisor times the quotient'), show(r2s, 'the biggest remainder')),
      L("Dividing by three or nine, the remainder is the same as the digit sum's. Four thousand eight hundred twenty-six, "
        "the digit sum is twenty, and twenty divided by nine leaves two.", show(r3s, 'Dividing by three or nine'))),
    S('Combine remainders',
      L("Only the remainders matter. a leaves five and b leaves seven, dividing by eight. a plus b, five plus seven is "
        "twelve, so it leaves four. a times b, five times seven is thirty-five, so it leaves three. a minus b, five minus "
        "seven is negative two, so add eight, six.", show(c1s, 'a leaves five'), show(c2s, 'a plus b')),
      L("Take away the remainder, and what's left divides exactly.", show(c3s, 'Take away the remainder')),
      L("A new divisor? It must divide the old one. Leaves eleven by twelve? By four, eleven leaves three. But from ten to "
        "four, you can't know.", show(c4s, 'A new divisor'))),
    S('The tools',
      L("Nested fractions with one on top, like one fifth of one third? Multiply the denominators. "
        "For other fractions, simplify and check that each group is a whole number. "
        "How many multiples in a range? Subtract the first multiplier from the last multiplier, then add one, because both ends count.",
        show(n1s, 'Nested fractions with one on top'), show(n2s, 'How many multiples')),
      L("Two in a row always divide by two, and three in a row by six. And a cubed minus a is three in a row in disguise.",
        show(n3s, 'Two in a row')),
      L("Necessarily divisible? Tag each condition, and read the number in front. And when you plug in, choose values independently "
        "unless a condition links them. Different letters do not have to be unequal, but do not assume they are equal. "
        "Avoid values that give zero, and remember that one failing example knocks a choice out.",
        show(n4s, 'Tag each condition'), show(n5s, 'when you plug in'))),
    S('Before you practice',
      L("Before each question, ask yourself. Parts with no common factor? Is my remainder smaller than the divisor? A "
        "negative remainder? Add the divisor. And does the new divisor divide the old one?",
        show(z1s, 'Parts with no'), show(z2s, 'Is my remainder'), show(z3s, 'A negative remainder'), show(z4s, 'does the new divisor')),
      L("That's it. Now go practice, and I'll see you in the next video.", mk('underline', 'z2s', 'go practice'))),
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
 "q-423": "In Daniel's class, $\\frac{1}{5}$ of the students are boys who play basketball, and among those, $\\frac{1}{3}$ also play the guitar. What could be the number of students in the class?",
 "q-424": "Tamar is putting her stamps into an album. If she arranges them in rows of 5 with an equal number in each row, 4 stamps are left over. If she arranges them in rows of 3 with an equal number in each row, 1 stamp is left over. What could be the number of stamps Tamar has?",
 "q-425": "$a$ and $b$ are positive integers. $x$ is the remainder when $a$ is divided by 8, and $y$ is the remainder when $b$ is divided by 3. What is the greatest possible value of $x\\cdot y$?",
 "q-426": "A number leaves a remainder of 4 when divided by 5. Which of the following expressions could represent the number ($x$ is an integer)?",
 "q-r26-t15-01": "$a$ and $b$ are positive integers, and $a>b$. When $a$ is divided by 7, the remainder is 2. When $b$ is divided by 7, the remainder is 5. What will be the remainder if $a-b$ is divided by 7?",
 "q-427": "$30\\%$ of the members of a sports club play tennis. Which of the following numbers could be the number of members who play tennis?",
 "q-428": "A game machine shows a three-digit number. Its hundreds digit is 6, its tens digit is 1, and its units digit is $X$.\nThe machine pays:\n4 tokens if the number is divisible by 2 but not by 3;\n8 tokens if it is divisible by 3 but not by 2;\n12 tokens if it is divisible by both 2 and 3.\nNoa played once and won 12 tokens. How many different values can $X$ have?",
 "q-429": "Which of the following numbers is not divisible by 12?",
 "q-430": "Yoav claims: \"There are more three-digit numbers divisible by both 3 and 5 than three-digit numbers divisible by 17.\"\nMichal claims: \"There are more three-digit numbers divisible by both 3 and 7 than three-digit numbers divisible by both 2 and 13.\"\nWhich of the following is correct?",
 "q-431": "Given:\n$\\begin{cases} c=4a \\\\ a=\\frac{b}{5} \\end{cases}$\n$a$, $b$ and $c$ are positive integers. Which claim is not necessarily true?",
 "q-r26-t15-15": "$x$ and $y$ are positive integers. $x$ is divisible by $6$, and $y$ is divisible by $9$.\nWhat is the largest number that $x+y$ is necessarily divisible by?",
 "q-434": "Yael loaded 900 points onto an amusement-park card. The first ride cost $x$ points, the second ride cost $2x$ points, and the third ride cost $3x$ points. Which of the following could be the number of points left on her card after the three rides?",
 "q-435": "When $x$ is divided by 8, the remainder is 4.\nYuval claims: \"$2x$ is necessarily divisible by 8.\"\nNoga claims: \"$x$ is necessarily divisible by 4.\"\nItay claims: \"$x$ is necessarily divisible by 12.\"\nWhich of the following is correct?",
 "q-436": "The sum of three integers is divisible by 6. Which of the following statements is not necessarily true?"
}   # q-432, q-433: inline letters in the givens - the whole stem only
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


# Spoken clarity revision: preserves the complete original board/cue plan.
_clarity_spec = importlib.util.spec_from_file_location(
    '_codex_script_clarity_20261012', os.path.join(HERE, '_codex_script_clarity_20261012.py'))
_clarity_module = importlib.util.module_from_spec(_clarity_spec)
_clarity_spec.loader.exec_module(_clarity_module)
_clarity_module.apply(VIDEOS)

# 2026-10-13 method visuals + carry-over boxes (math_patches/_method_visuals.py; teacher: "a method with a signature visual
# is shown with THAT visual, built step by step" and "when you clear the slide, something important should stay"). Runs
# AFTER the clarity overlay, so the overlay's cue checks see the plan they were made for. Visual only, no spoken text.
import types as _types
_mv_spec = importlib.util.spec_from_file_location('_method_visuals', os.path.join(HERE, '_method_visuals.py'))
_mv = importlib.util.module_from_spec(_mv_spec); _mv_spec.loader.exec_module(_mv)
_mv.post(_types.SimpleNamespace(**globals()), 15)

if __name__ == '__main__':
    _bad = 0
    for _v in sys.argv[1:] or ORDER:
        _p = check(_v)
        if _p: print('PROBLEMS', _v, _p); _bad += 1
        print('script written:', write_json(_v), stats(_v))
    for x in WRITE_LATE: print('mark dropped (its item is still being written):', x)
    sys.exit(1 if _bad else 0)
