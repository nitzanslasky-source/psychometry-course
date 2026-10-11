"""Topic 14 (Prime Numbers) - the redo for the teacher's own-voice reading (2026-10-11), built exactly like topic 13
(math_patches/_ai_vis_t13.py, the model; its DSL and visual passes are copied here so the two topics stay independent).

The teacher records only the camera lesson 'primes' (re-record, never touched here). Every other topic-14 video gets a
script that SHE reads aloud in the Reading Studio (reading_studio.py); reading_to_video.py then times the handwriting and
the visuals to her words.

ONE spec per video drives all three sides, so they cannot drift apart:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t14.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: t14.py ai_redo_t14() (time-gated, runs LAST) rebuilds the slides from studio_slides(vid) - the
                    spoken lines are the script lines (tags dropped), one studio line per script line - and then
                    _ai_visual.apply() adds the cues and click items around them.

Every question video: the stem read aloud (calm voice), a first reaction, all the useful methods (each from the givens,
R30), every step with what / why / what it means (R31), every calculation said aloud (R33), traps at the step, "choice
number N" (R34), the answer, a takeaway only if it teaches something new, then "Okay. I'll see you in the next question."
NO "which way is better" verdict (teacher, 2026-10-11). Ideas taught earlier get a short reminder; the first real use of
an idea gets the full rule-examples-why-trap treatment (R29 / R32). The concept map is in the review file
~/Downloads/Topic-14-AI-scripts-review.md and in TEACHING_STYLE_GUIDE.md.

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

_s = importlib.util.spec_from_file_location('_shaded_nl_t14ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-14 flow order of the AI videos (primes = the camera lesson, not here)
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
    if t in ('stem',) or re.fullmatch(r'choice \d', t) or t.startswith('fig:'): return t
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
            'style': "the teacher reads it herself (Reading Studio), topic-14 redo (2026-10-11): math_patches/_ai_vis_t14.py is "
                     "the source - edit there and re-run it. Rules: real_exam/TEACHING_STYLE_GUIDE.md R1-R34 (no 'which way is "
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
# THE SCRIPTS (topic-14 flow order). NEW / REMINDER per video: see ~/Downloads/Topic-14-AI-scripts-review.md.
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ q-387 (Q1)
# NEW: test the prime next to the one the choices point at (9 x 2 = 18 is there, so: could a bigger prime work?); build
# powers from known ones (3^3 = 27, 3^4 = 81) and stop once it passes two digits (R35); a bigger base gives a bigger
# power, so x < 3 and x must be 2 - no need to calculate 2^6; the answer is 9x, not x.
# REMINDER: trial and error (topic 21), powers (topic 8).
h0 = I('h0', '$x^6$: two digits, so $x$ is small', size=30, col=1, hand='x^6 : two digits, so x is small')
t0 = I('t0', 'Try $3$', size=30, col=1, hand='Try  3')
t2 = I('t2', '$3^3=27,\\ \\ 3^4=81$', hand='3^3 = 27,    3^4 = 81')
t3 = I('t3', '$3^5$: past two digits ✗', hand='3^5 :   past two digits   ✗')
k1 = I('k1', 'Bigger prime, bigger power', size=30, col=1)
t4 = I('t4', '$x<3$, so $\\hl{x}{x=2}$', hand='x < 3,   so   \\hl{x}{x = 2}')
t5 = I('t5', '$9x=9\\cdot2=\\hl{ans}{18}$', hand='9x = 9·2 = \\hl{ans}{18}')
p0 = I('p0', '$x=\\frac{9x}{9}$', size=32, hand='x = {9x/9}')
p1 = I('p1', '$27\\to3,\\ \\ 18\\to2,\\ \\ 63\\to7,\\ \\ 45\\to5$', size=32, hand='27→3,   18→2,   63→7,   45→5')
p2 = I('p2', 'All four are primes', size=30, col=1)
p3 = I('p3', '$x=3$: $\\ 3^4=81$, $\\ 3^5$ too big ✗', hand='x = 3 :   3^4 = 81,   3^5  too big   ✗')
p4 = I('p4', '$x=5,\\ 7$: even bigger ✗', hand='x = 5, 7 :   even bigger   ✗')
p5 = I('p5', '$x=2$: the only one left ✓', hand='x = 2 :   the only one left   ✓')
video('solve-q-387', 'solution', qid='q-387', slides=[
    S('Method 1 · Trial and error',
      L("Given: x is a prime number, and x to the power of six is a two-digit number. What is nine x?",
        pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("So x is a prime, and its sixth power has only two digits. That's a big hint, because a sixth power grows really "
        "fast, so x must be a small number. And look, they don't ask for x, they ask for nine x. [short pause] We'll solve "
        "it two ways, trial and error first, and then plugging in the answers.",
        pt('stem', 'x is a prime'), show(h0, 'only two digits'), pt('h0', 'grows really fast'), pt('stem', 'they ask for nine x')),
      L("[short pause] Remember, with primes we can simply try numbers against the "
        "conditions. Let's start with three, a small prime whose powers are easy to build up.",
        show(t0, "Let's start with three"), pt('h0', 'easy to build up')),
      L("I don't write out three times three times three, six times. I build it from what I know. Three to the power of "
        "three is twenty-seven. Times three again, that's three to the power of four, eighty-one.",
        pt('t0', "I don't write out"), show(t2, 'Three to the power of')),
      L("And one more three? Eighty-one times three is already past two digits, and we still need one more three after "
        "that. So I don't even need the exact number. Three is too big.",
        show(t3, 'And one more three'), mk('cross', 't3', 'Three is too big')),
      L("And what does that mean? A bigger base only gives a bigger power, so x has to be smaller than three. And the only "
        "prime smaller than three is two. So x is two, and I don't even need to calculate it.",
        show(k1, 'A bigger base only'), show(t4, 'So x is two')),
      L("Now careful, because x isn't the answer. A lot of students find that x is two, and go looking for two in the "
        "choices. They ask for nine x. Nine times two is eighteen, so choice number two is our answer.",
        pt('t4', "x isn't the answer"), pt('stem', 'They ask for nine x'), show(t5, 'Nine times two'),
        mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Each choice is nine x, so to get x back, I divide the choice "
        "by nine. Twenty-seven over nine is three, eighteen over nine is two, sixty-three over nine is seven, and "
        "forty-five over nine is five.",
        pt('choice 1', 'Each choice is nine x'), show(p0, 'I divide the choice'), show(p1, 'Twenty-seven over nine'),
        pt('choice 2', 'eighteen over nine'), pt('choice 3', 'sixty-three over nine'), pt('choice 4', 'forty-five over nine')),
      L("Are they primes? Three, two, seven and five, yes, all four. So the prime condition doesn't rule anything out "
        "here, and the power has to decide.", show(p2, 'yes, all four'), pt('stem', 'the power has to decide')),
      L("Choice number one gives x is three. Three to the power of three is twenty-seven, and times three is eighty-one. One "
        "more three already passes two digits, so choice number one is out.",
        pt('choice 1', 'Choice number one gives'), show(p3, 'Three to the power of three'), mk('cross', 'choice 1', 'choice number one is out')),
      L("Choice numbers three and four give seven and five. They're bigger than three, so their powers are even bigger. "
        "Both out.", show(p4, 'give seven and five'), mk('cross', 'choice 3', 'even bigger'), mk('cross', 'choice 4', 'Both out')),
      L("Three choices are out, and choice number two, x is two, is the only one left. So choice number two is our answer.",
        show(p5, 'the only one left'), mk('tick', 'choice 2', 'So choice number two is our answer')),
      L("[pause] Okay. I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ q-r26-t14-01 (Q2)
# NEW (R32 - the camera lesson only names it in one line): the digit-sum test for 3, with an example and a non-example;
# 7 has no quick test, just divide; "never forget seven"; counting by sevens.  REMINDER: test only the primes up to the
# square root (camera lesson, with its why); fake primes 91 and 119 (camera lesson).
f0 = I('f0', 'Three fakes, one prime', size=30, col=1)
r0 = I('r0', 'Try only the primes up to $\\sqrt{n}$', size=30, col=1)
a1 = I('a1', '$81<91<100$: $\\ $try $2,\\ 3,\\ 5,\\ 7$', size=34, hand='81 < 91 < 100 :   try  2, 3, 5, 7')
d1 = I('d1', 'Digit sum divides by $3$: so does the number', size=26, col=1)
d2 = I('d2', '$51$: $\\ 5+1=6$ ✓ $\\quad 51=3\\cdot17$', size=30, col=1, hand='51 :  5+1 = 6  ✓    51 = 3·17')
d3 = I('d3', '$52$: $\\ 5+2=7$ ✗', size=30, col=1, hand='52 :  5+2 = 7  ✗')
a2 = I('a2', '$91$: $\\ 9+1=10$ ✗ $\\quad 91=\\hl{f}{7\\cdot13}$', size=34, hand='91 :  9+1 = 10  ✗     91 = \\hl{f}{7·13}')
a3 = I('a3', '$119=\\hl{f}{7\\cdot17}$', hand='119 = \\hl{f}{7·17}')
a4 = I('a4', '$133=\\hl{f}{7\\cdot19}$', hand='133 = \\hl{f}{7·19}')
a5 = I('a5', '$113$: odd, $\\ 1+1+3=5$, $\\ $ends in $3$', size=30, hand='113 :  odd,   1+1+3 = 5,   ends in 3')
a7 = I('a7', '$7\\cdot16=112$, $\\ $remainder $1$', size=30, hand='7·16 = 112,   remainder 1')
a6 = I('a6', '$113$ is $\\hl{p}{\\text{prime}}$', hand='113  is  \\hl{p}{prime}')
k3 = I('k3', 'Looks prime? Try $7$ too', size=30, col=1)
s1 = I('s1', '$\\hl{a}{91},\\ 98,\\ 105,\\ 112,\\ \\hl{b}{119},\\ 126,\\ \\hl{c}{133}$', size=30,
       hand='\\hl{a}{91},  98,  105,  112,  \\hl{b}{119},  126,  \\hl{c}{133}')
s0 = I('s0', 'Quick tests: $2$ even, $3$ digit sum, $5$ last digit', size=26, col=1)
s2 = I('s2', '$113$: not on the list, the last one left ✓', size=30, hand='113 :  not on the list,  the last one left   ✓')
video('solve-q-r26-t14-01', 'solution', qid='q-r26-t14-01', slides=[
    S('Method 1 · Test up to the root',
      L("Which of the following numbers is prime?", pt('stem', 'Which', 'hl', 2.5), voice='calm', pause=0.5),
      L("So four numbers, all odd, and every one of them looks prime. But three of them are fakes, and only one is really "
        "prime. [short pause] We'll solve it two ways, testing each number up to its root, and then counting by sevens.",
        pt('choice 1', 'four numbers'), pt('choice 4', 'all odd'), show(f0, 'three of them are fakes')),
      L("[short pause] Remember, to test a number, I divide it by the primes up to its square root, and no "
        "further. If none of them divides it, it's prime. Let's start with ninety-one. Nine squared is eighty-one, and ten "
        "squared is a hundred. So the root of ninety-one is between nine and ten, and I only try two, three, five and "
        "seven.", show(r0, 'up to its square root'), pt('choice 1', "start with ninety-one"), show(a1, 'Nine squared is'),
        pt('a1', 'I only try two')),
      L("Two? Ninety-one is odd, so no. Three? Here's a quick test, and it's worth knowing well. Add the digits, and if the "
        "digit sum divides by three, the whole number does too. Fifty-one, five plus one is six, and six divides by three. "
        "And really, fifty-one is three times seventeen. But fifty-two, five plus two is seven, so fifty-two doesn't divide "
        "by three. We don't need to prove this test, it simply always works.",
        pt('a1', 'Ninety-one is odd'), show(d1, 'Add the digits'), show(d2, 'Fifty-one, five plus one'), pt('d2', 'three times seventeen'),
        show(d3, 'But fifty-two'), pt('d1', "We don't need to prove")),
      L("So ninety-one, nine plus one is ten. Ten doesn't divide by three, so three doesn't divide ninety-one. Five? It "
        "doesn't end in zero or five, so no. And seven? Seven has no quick test, so I just divide. Seven times ten is "
        "seventy, and seven times three is twenty-one, together ninety-one. So ninety-one is seven times thirteen. It "
        "breaks, it's a fake, and choice number one is out.",
        show(a2, 'nine plus one is ten'), pt('a2', 'Five? It'), pt('a2', 'Seven has no quick test'), mk('circle', 'a2: f', 'seven times thirteen'),
        mk('cross', 'choice 1', 'choice number one is out'))),
    S('Method 1 · Test up to the root',
      L("A hundred nineteen. Ten squared is a hundred, and eleven squared is a hundred twenty-one, so again I try two, "
        "three, five and seven. It's odd. One plus one plus nine is eleven, not a multiple of three. It ends in nine, so not "
        "five. And seven? Seven times ten is seventy, and seven times seven is forty-nine, together a hundred nineteen. So "
        "it's seven times seventeen, a fake again, and choice number two is out.",
        pt('choice 2', 'A hundred nineteen'), show(a3, 'together a hundred nineteen'), mk('cross', 'choice 2', 'choice number two is out')),
      L("A hundred thirty-three. Eleven squared is a hundred twenty-one, and twelve squared is a hundred forty-four, so I "
        "try up to eleven. It's odd, one plus three plus three is seven, and it ends in three. Seven? Seven times twenty is "
        "a hundred forty, and one seven less is a hundred thirty-three. So it's seven times nineteen, and choice number "
        "four is out.", pt('choice 4', 'A hundred thirty-three'), show(a4, 'one seven less'), mk('cross', 'choice 4', 'choice number four is out')),
      L("In the exam you'd circle the last one and move on. Here, let's see why a hundred thirteen really is prime. Ten "
        "squared is a hundred and eleven squared is a hundred twenty-one, so I try two, three, five and seven. It's odd. "
        "One plus one plus three is five, not a multiple of three. It ends in three. And seven times sixteen, seventy plus "
        "forty-two, is a hundred twelve. So a hundred thirteen leaves a remainder of one.",
        pt('choice 3', 'circle the last one'), show(a5, "It's odd. One plus one"), show(a7, 'seven times sixteen')),
      L("Nothing up to the root divides it, so a hundred thirteen is prime. Choice number three is our answer.",
        show(a6, 'Nothing up to the root'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("And look, all three fakes broke on seven. So when a number looks prime, never forget to try seven.",
        pt('a3: f', 'all three fakes'), show(k3, 'never forget to try seven'), mk('underline', 'k3', 'try seven'))),
    S('Method 2 · Count by sevens',
      L("[pause] Our second method, counting by sevens. Why sevens? Because two, three and five have quick tests you can "
        "see on the number, even, the digit sum and the last digit. Seven is the one small prime with no quick test. So "
        "let's list the multiples of seven around a hundred.",
        show(s0, 'two, three and five have quick tests'), pt('s0', 'Seven is the one')),
      L("Seven times thirteen is ninety-one. Then I add seven each time. Ninety-one plus seven is ninety-eight, plus seven "
        "is a hundred five, then a hundred twelve, a hundred nineteen, a hundred twenty-six, and a hundred thirty-three.",
        show(s1, 'Seven times thirteen'), voice='calm'),
      L("Ninety-one, a hundred nineteen and a hundred thirty-three are all on the list. So they divide by seven, they're "
        "fakes, and choice numbers one, two and four are out.",
        mk('circle', 's1: a', 'Ninety-one, a'), mk('circle', 's1: b', 'hundred nineteen and'), mk('circle', 's1: c', 'hundred thirty-three are'),
        mk('cross', 'choice 1', 'choice numbers one'), mk('cross', 'choice 2', 'two and four'), mk('cross', 'choice 4', 'are out')),
      L("A hundred thirteen isn't on the list, and the other three choices are out. So there's nothing left to check, it's "
        "choice number three. [pause] Okay. I'll see you in the next question.",
        show(s2, "isn't on the list"), mk('tick', 'choice 3', 'choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-388 (Q3)
# NEW (R32 - one line in the camera lesson): unpacking a piece that isn't prime, 10^2 = 10·10 = 2·5·2·5 = 2^2·5^2, and the
# trap behind it ("no two in x"); the missing prime; dividing the real number as a second method.
# REMINDER: divisor = factor, "a divisor needs its primes, enough copies" (camera lesson slides 6 and 9).
r1 = I('r1', 'A divisor: its primes are in $x$, enough times', size=26, col=1)
u0 = I('u0', '$10$ is not a prime: unpack it', size=30, col=1)
u1 = I('u1', '$10^2=10\\cdot10=2\\cdot5\\cdot2\\cdot5=2^2\\cdot5^2$', size=34, hand='10^2 = 10·10 = 2·5·2·5 = 2^2·5^2')
u2 = I('u2', '$x=3\\cdot5^2\\cdot2^2\\cdot5^2=\\hl{x}{2^2\\cdot3\\cdot5^4}$', size=34, hand='x = 3·5^2·2^2·5^2 = \\hl{x}{2^2·3·5^4}')
u3 = I('u3', 'Two $2$s, one $3$, four $5$s', size=30, col=1, hand='two 2s,  one 3,  four 5s')
c1 = I('c1', '$20=2^2\\cdot5$ ✓', hand='20 = 2^2·5   ✓')
c2 = I('c2', '$22=2\\cdot\\hl{e}{11}$ ✗', hand='22 = 2·\\hl{e}{11}   ✗')
c3 = I('c3', '$75=3\\cdot5^2$ ✓', hand='75 = 3·5^2   ✓')
c4 = I('c4', '$60=2^2\\cdot3\\cdot5$ ✓', hand='60 = 2^2·3·5   ✓')
k1 = I('k1', 'Not a prime? Unpack it first', size=30, col=1)
u4 = I('u4', '$x=2^2\\cdot3\\cdot5^4$', size=34, col=1, hand='x = 2^2·3·5^4')
v1 = I('v1', '$x=3\\cdot25\\cdot100=\\hl{x}{7500}$', hand='x = 3·25·100 = \\hl{x}{7500}')
v2 = I('v2', '$7500\\div20=375$ ✓', hand='7500 ÷ 20 = 375   ✓')
v3 = I('v3', '$3750\\div11$: $\\ 11\\cdot340=3740$, $\\ $remainder ✗', size=30, hand='3750 ÷ 11 :   11·340 = 3740,  remainder  ✗')
v4 = I('v4', '$7500\\div75=100$ ✓', col=1, hand='7500 ÷ 75 = 100   ✓')
v5 = I('v5', '$7500\\div60=125$ ✓', col=1, hand='7500 ÷ 60 = 125   ✓')
video('solve-q-388', 'solution', qid='q-388', slides=[
    S('Method 1 · Break into primes',
      L("Given: x is equal to three, times five squared, times ten squared. Which of the following numbers does not divide "
        "x?", pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("So x is already broken into pieces, and they ask which number does not divide it. Divide is the same as factor, so "
        "they're asking which choice is not a factor of x, which one you can't build out of x. And careful, one of the "
        "pieces, ten, isn't a prime. [short pause] We'll solve it two ways, breaking everything into primes, and then "
        "dividing the real number.", pt('stem', 'already broken into pieces'), pt('stem', 'does not divide'), pt('stem', 'one of the pieces')),
      L("[short pause] Remember the check from the lesson. A number divides x only if every prime it "
        "needs is in x, at least as many times. So first, every piece of x has to be a prime. Three is a prime, and five is "
        "a prime, but ten isn't.", show(r1, 'every prime it needs'), show(u0, "but ten isn't")),
      L("So how do I unpack ten squared? Ten squared is ten times ten. And each ten is two times five. So ten squared is two "
        "times five, times two times five. That's two twos and two fives, two squared times five squared.",
        show(u1, 'Ten squared is ten times ten'), pt('u1', 'And each ten'), pt('u1', 'two twos and two fives')),
      L("Now careful here. A lot of students look at x, don't see a two anywhere, and cross out every even choice. But the "
        "twos are hiding inside the tens.", pt('stem', "don't see a two"), pt('u1', 'hiding inside the tens')),
      L("So let's count. Five squared from the start, and five squared from the ten squared, that's four fives. Two twos, "
        "and one three. So x is two squared, times three, times five to the power of four.",
        show(u2, "So let's count"), show(u3, 'Two twos'), mk('circle', 'u2: x', 'times five to the power of four'))),
    S('Method 1 · Break into primes',
      L("Now the choices. Twenty is two times ten, and ten is two times five. So twenty is two squared times five. Two twos, "
        "and x has two. One five, and x has four. Everything is in stock, so twenty divides x, and choice number one is "
        "out.", show(u4, 'Now the choices'), show(c1, 'Twenty is two times ten'), pt('u4', 'and x has two'),
        mk('cross', 'choice 1', 'choice number one is out')),
      L("Twenty-two is two times eleven. The two is there. But is there an eleven anywhere in x? No. Eleven is a prime that "
        "x simply doesn't have, so twenty-two can't divide x.",
        pt('choice 2', 'Twenty-two is'), show(c2, 'two times eleven'), mk('circle', 'c2: e', 'an eleven anywhere'), pt('u4', 'No. Eleven')),
      L("Can I circle it already? In the exam, yes, a missing prime settles it. Here, let's check the other two as well. "
        "Seventy-five is three times twenty-five, so three times five squared. One three and two fives, both in stock. "
        "Choice number three is out.", pt('choice 3', 'Seventy-five is'), show(c3, 'three times twenty-five'),
        mk('cross', 'choice 3', 'Choice number three is out')),
      L("Sixty is six times ten, so two times three, times two times five. That's two squared, times three, times five. Two "
        "twos, one three and one five, all in stock. Out too. So twenty-two, choice number two is our answer.",
        pt('choice 4', 'Sixty is'), show(c4, 'six times ten'), mk('cross', 'choice 4', 'Out too'), mk('tick', 'choice 2', 'choice number two is our answer')),
      L("So whenever a piece isn't a prime, like ten or six, unpack it into primes first.", show(k1, 'unpack it into primes first'))),
    S('Method 2 · Divide the number',
      L("[pause] Our second method, working out x as a number, and simply dividing. Five squared is twenty-five, and ten "
        "squared is a hundred. Three times twenty-five is seventy-five, and seventy-five times a hundred is seven thousand "
        "five hundred.", pt('stem', 'working out x'), show(v1, 'Five squared is'), mk('circle', 'v1: x', 'seven thousand five hundred'), voice='calm'),
      L("Twenty. Seven thousand five hundred over twenty is the same as seven hundred fifty over two, and that's three "
        "hundred seventy-five. A whole number, so twenty divides x, and choice number one is out.",
        pt('choice 1', 'Twenty. Seven'), show(v2, 'seven hundred fifty over two'), mk('cross', 'choice 1', 'choice number one is out')),
      L("Twenty-two. Half of seven thousand five hundred is three thousand seven hundred fifty, and now I divide by eleven. "
        "Eleven times three hundred forty is three thousand seven hundred forty, and that leaves ten. A remainder, so "
        "twenty-two doesn't divide x.", pt('choice 2', 'Twenty-two. Half'), show(v3, 'now I divide by eleven'), pt('v3', 'that leaves ten')),
      L("Seventy-five. Seventy-five times a hundred is seven thousand five hundred, so it divides exactly. Out. Sixty. Seven "
        "thousand five hundred over sixty is seven hundred fifty over six, and that's a hundred twenty-five. Out too. So "
        "again, choice number two. [pause] Okay. I'll see you in the next question.",
        show(v4, 'Seventy-five times a hundred'), mk('cross', 'choice 3', 'divides exactly'), show(v5, 'over sixty'),
        mk('cross', 'choice 4', 'Out too'), mk('tick', 'choice 2', 'again, choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-386 (Q4)
# NEW: write the numbers out on a line, mark the primes, count; "not including x"; the smallest product of two positive
# numbers = each as small as possible; every wrong choice is a trap (29 is prime, y = 40, the largest product).
# REMINDER: the primes up to 40 (camera lesson); a quick prime test for 41, 43, 47 (roots below 7).
P1 = STRIP('P1', 28, 48, [
    ('pr', [('prime', v) for v in (29, 31, 37, 41, 43, 47)]),
    ('down', [('span', 31, 37, 'two primes')]),
    ('x', [('lab', 30), ('cross', 29), ('ring', 30)]),
    ('up', [('span', 41, 43, 'two primes')]),
    ('y', [('lab', 44), ('lab', 45), ('lab', 46), ('ring', 44), ('cross', 47)]),
], base=(40,), w=1060)
q2 = I('q2', '$x=30$ $\\quad$ ($29$ is prime)', size=34, hand='x = 30    (29 is prime)')
q3 = I('q3', '$y$: $\\ \\hl{y}{44},\\ 45,\\ 46$', size=34, hand='y :   \\hl{y}{44},  45,  46')
q4 = I('q4', '$30\\cdot44=\\hl{ans}{1320}$', size=34, hand='30·44 = \\hl{ans}{1320}')
q5 = I('q5', '$29\\cdot44=1276\\quad 30\\cdot40=1200\\quad 30\\cdot46=1380$', size=30)
video('solve-q-386', 'solution', qid='q-386', slides=[
    S('Number line',
      L("x and y are integers that are not prime, and x is smaller than forty, which is smaller than y. Between x and forty "
        "there are exactly two prime numbers, not including x. Between forty and y there are exactly two prime numbers, not "
        "including y. What is the smallest possible value of x times y?", pt('stem', 'x and y are', 'hl', 14.0), voice='calm', pause=0.5),
      L("So x is below forty, y is above forty, and neither of them is prime. And we count the primes between each of them "
        "and forty. This is exactly why it's so important to know the primes by heart. [short pause] Let's draw the whole "
        "numbers around forty on a number line, and count.",
        pt('stem', 'neither of them is prime'), pt('stem', 'we count the primes'), show(P1['line'], 'on a number line')),
      L("Remember the primes below forty, twenty-nine, thirty-one and thirty-seven. And above forty, forty-one, forty-three "
        "and forty-seven. Why are those three prime? They're odd, their digit sums are five, seven and eleven, and they "
        "don't end in five. And their roots are less than seven, because seven squared is forty-nine. So two, three and "
        "five are all I need to try.",
        show(P1['pr'], 'Remember the primes'), pt('fig: 41', 'And above forty'), pt('P1_line', 'Why are those three'), pt('P1_line', 'seven squared')),
      L("Now x. Counting down from forty, the first prime is thirty-seven, and the second is thirty-one. Those are the two "
        "primes between x and forty. So the next prime down, twenty-nine, has to stay out.",
        pt('P1_line', 'Counting down from forty'), show(P1['down'], 'the second is thirty-one'), mk('circle', 'fig: 29', 'twenty-nine, has to stay out')),
      L("So where can x be? If x were below twenty-nine, then twenty-nine would be in between too, and that's three primes. "
        "And if x were thirty-one or more, thirty-one would drop out, and that's only one prime. So x is twenty-nine or "
        "thirty. Twenty-nine itself is allowed by the counting, because not including x means x itself isn't counted.",
        pt('P1_line', 'below twenty-nine'), pt('P1_line', 'thirty-one or more'), pt('P1_line', 'twenty-nine or'), pt('stem', 'not including x')),
      L("But the question says x is not prime, and twenty-nine is prime. So x is thirty.",
        pt('stem', 'x is not prime'), show(P1['x'], 'So x is thirty')),
      L("Now y, the same way upwards. The first two primes above forty are forty-one and forty-three, so forty-seven has to "
        "stay out. y has to come after forty-three, and it can't go past forty-seven. So y is forty-four, forty-five, "
        "forty-six or forty-seven. And forty-seven is prime, so it's not allowed anyway.",
        show(P1['up'], 'The first two primes above forty'), pt('P1_line', 'forty-seven has to stay out'), show(P1['y'], 'So y is forty-four'), pt('fig: 47', 'forty-seven is prime')),
      sb='Number line'),
    S('Number line',
      L("Now careful, they ask for the smallest product. Both numbers are positive, so the product is smallest when each of "
        "them is as small as possible. x has to be thirty, and the smallest y is forty-four.",
        pt('stem', 'they ask for the smallest product'), show(q2, 'x has to be thirty'), show(q3, 'the smallest y')),
      L("Thirty times forty-four. How? Ten times forty-four is four hundred forty, and times three is one thousand three "
        "hundred twenty. So choice number three is our answer.",
        show(q4, 'Thirty times forty-four'), mk('circle', 'q4: ans', 'one thousand three hundred twenty'), mk('tick', 'choice 3', 'choice number three is our answer'), voice='calm'),
      L("And look at the other choices, each one is a trap. Twenty-nine times forty-four is one thousand two hundred "
        "seventy-six, forty-four less than before, and that takes x as twenty-nine, which is prime. Thirty times forty is one thousand two "
        "hundred, but y has to be above forty. And thirty times forty-six is one thousand three hundred eighty, the largest "
        "product, not the smallest.", show(q5, 'each one is a trap'), mk('cross', 'choice 2', 'which is prime'),
        mk('cross', 'choice 1', 'above forty'), mk('cross', 'choice 4', 'the largest')),
      L("[pause] Okay. I'll see you in the next question.")),
])

# ------------------------------------------------------------------------------------------------ prime-tools (lesson)
# NEW: counting divisors (each exponent plus one, multiplied) with its why, a listed check (44 -> 6), a bigger number
# (675 -> 12) and the trap (it needs a REAL prime factorization: 56 = 4·14 is not 4 divisors, 56 = 2^3·7 has 8).
# The other tools (GCD, the guaranteed divisor, breaking and building) are taught inside the questions that use them.
b1 = I('b1', 'Break a number apart $\\quad\\cdot\\quad$ Build numbers from pieces', size=36)
b2 = I('b2', 'Which prime is missing, or there too few times?', size=36)
g1 = I('g1', '$44$: $\\ 1,\\ 2,\\ 4,\\ 11,\\ 22,\\ 44$', size=42, hand='44 :   1,  2,  4,  11,  22,  44')
g2 = I('g2', '$44=4\\cdot11=2^2\\cdot11$', size=42, hand='44 = 4·11 = 2^2·11')
g3 = I('g3', 'Twos: $\\ 0,\\ 1,\\ 2$ $\\ \\to\\ 3$ options', size=38, hand='Twos :   0,  1,  2   →   3 options')
g4 = I('g4', 'Elevens: $\\ 0,\\ 1$ $\\ \\to\\ 2$ options', size=38, hand='Elevens :   0,  1   →   2 options')
g5 = I('g5', '$3\\cdot2=6$ divisors', size=42, hand='3·2 = 6  divisors')
g6 = I('g6', 'Each exponent plus one, then multiply', size=38)
g7 = I('g7', '$3^3\\cdot5^2$: $\\ $no need to work it out', size=42, hand='3^3·5^2 :   no need to work it out')
g8 = I('g8', '$(3+1)(2+1)=4\\cdot3=12$ divisors', size=42, hand='(3+1)(2+1) = 4·3 = 12  divisors')
g9 = I('g9', '$56=4\\cdot14$: $\\ (1+1)(1+1)=4$ ✗', size=38, hand='56 = 4·14 :   (1+1)(1+1) = 4   ✗')
g10 = I('g10', '$56=2^3\\cdot7$: $\\ 4\\cdot2=8$ ✓', size=38, hand='56 = 2^3·7 :   4·2 = 8   ✓')
g12 = I('g12', 'Break into primes, add one to each exponent, multiply', size=32)
g11 = I('g11', '$1,\\ 2,\\ 4,\\ 7,\\ 8,\\ 14,\\ 28,\\ 56$', size=38, hand='1,  2,  4,  7,  8,  14,  28,  56')
video('prime-tools', 'lesson', slides=[
    S('Factor Tools',
      L("Welcome back. Now that we can break a number into primes, we're going to use the primes as tools. The next "
        "questions ask about the greatest common divisor, the greatest number that's sure to divide, and long stories that "
        "hide a simple factor question. Many students find them hard, and you'll see they're a lot simpler than they "
        "look.")),
    S('Break & build',
      L("Almost every question in this part does one of two things. It breaks a number apart into factors, or it builds "
        "numbers by multiplying pieces together.", show(b1, 'It breaks a number apart')),
      L("And then it asks something simple. Which prime is missing, or which prime is there too few times? Each of these "
        "tools, we'll learn inside the question that uses it.", show(b2, 'Which prime is missing'))),
    S('Counting divisors',
      L("But first, one tool that none of the next questions uses, and the practice questions do. How many divisors does a "
        "number have? Let's take forty-four. Its divisors are one, two, four, eleven, twenty-two and forty-four. That's "
        "six.", show(g1, "Let's take forty-four")),
      L("Listing them works for small numbers. But there's a faster way, from the prime factorization. Forty-four is four "
        "times eleven, so it's two squared times eleven.", show(g2, 'Forty-four is four')),
      L("Why does this help? A divisor of forty-four is built only from its primes, twos and elevens, and never more of each "
        "than forty-four has. So a divisor chooses how many twos it takes, zero, one or two. That's three options. And how "
        "many elevens, zero or one. That's two options.", pt('g2', 'built only from its primes'), show(g3, 'how many twos'),
        show(g4, 'how many elevens')),
      L("Any choice of twos goes with any choice of elevens, so I multiply the options. Three times two is six, exactly the "
        "six divisors we listed.", show(g5, 'Three times two'), pt('g1', 'exactly the six')),
      L("So the rule is, take each exponent, add one, and multiply. Why plus one? Because taking zero copies is also a "
        "choice. The divisor one, with no twos and no elevens, is that choice.",
        show(g6, 'take each exponent'), mk('underline', 'g6', 'add one, and multiply'), pt('g3', 'taking zero copies')),
      sb='Counting divisors'),
    S('Counting divisors',
      L("Let's see it on a bigger number, three cubed times five squared. Do I need to know what number that is? No. "
        "Listing its divisors would take a while, and the rule doesn't need it. Threes, zero to three, that's four options. "
        "Fives, zero to two, that's three options. Four times three is twelve divisors.",
        show(g7, 'three cubed times five squared'), show(g8, 'Threes, zero to three')),
      L("Now careful, the rule works only on a real prime factorization. Fifty-six is four times fourteen, and a lot of "
        "students say one plus one, times one plus one, four divisors. But four and fourteen aren't primes.",
        show(g9, 'Fifty-six is four times fourteen'), mk('cross', 'g9', "aren't primes")),
      L("Fifty-six is two cubed times seven. So it's three plus one, times one plus one, four times two, eight divisors. "
        "One, two, four, seven, eight, fourteen, twenty-eight and fifty-six.",
        show(g10, 'two cubed times seven'), show(g11, 'One, two, four, seven')),
      L("So, break into primes, add one to each exponent, and multiply. The factor tools card comes right after this video, "
        "and then seven questions. Try each one first, and then watch the solution. [pause] Okay. I'll see you in the next "
        "video.", show(g12, 'break into primes')),
      sb='Counting divisors'),
])

# ------------------------------------------------------------------------------------------------ q-389 (Q5)
# NEW: the GCD in plain words (the biggest number that divides both = the greatest common factor), "it's just taking out
# a common factor", each shared prime at its LOWER power + why, an example in numbers (her own 172 and 112, with factor
# trees and "multiply back to check"), choosing among the choices that divide both.  REMINDER: common factor (topic 4).
g0 = I('g0', 'GCD: the biggest number that divides both', size=26, col=1)
g1 = I('g1', 'GCD $=$ what comes out of both', size=26, col=1)
m1 = I('m1', '$p$: $\\ p^3$ and $p$ $\\ \\to\\ \\hl{a}{p}$', size=28, hand='p :   p^3  and  p   →   \\hl{a}{p}')
m2 = I('m2', '$q$: $\\ q^2$ and $q^5$ $\\ \\to\\ \\hl{a}{q^2}$', size=28, hand='q :   q^2  and  q^5   →   \\hl{a}{q^2}')
m3 = I('m3', '$r$: $\\ $only in $y$ $\\ \\to\\ $out', size=28, hand='r :   only in y   →   out')
m4 = I('m4', '$s$: $\\ s$ and $s^2$ $\\ \\to\\ \\hl{a}{s}$', size=28, hand='s :   s  and  s^2   →   \\hl{a}{s}')
k1 = I('k1', 'Each shared prime, at its lower power', size=26, col=1)
m5 = I('m5', 'GCD $=\\hl{g}{p\\cdot q^2\\cdot s}$', size=32, col=1, hand='GCD = \\hl{g}{p·q^2·s}')
T172 = TREE('T172', 172, [(2, 86), (2, 43)], w=380, col=0)
T112 = TREE('T112', 112, [(2, 56), (2, 28), (2, 14), (2, 7)], w=520, col=0)
w1 = I('w1', '$172=2^2\\cdot43$', size=32, col=1, hand='172 = 2^2·43')
w1b = I('w1b', '$172=2^2\\cdot43$', size=32, col=1, hand='172 = 2^2·43')
w2 = I('w2', '$112=2^4\\cdot7$', size=32, col=1, hand='112 = 2^4·7')
w3 = I('w3', 'GCD $=2^2=\\hl{f}{4}$', size=32, col=1, hand='GCD = 2^2 = \\hl{f}{4}')
n1 = I('n1', '(1) has $r$: $\\ $not in $x$ ✗', size=28, hand='(1)  has r :  not in x   ✗')
n2 = I('n2', '(2) $p^3$: $\\ y$ has one $p$ ✗', size=28, hand='(2)  p^3 :  y has one p   ✗')
n3 = I('n3', '(3) $p\\cdot q^2\\cdot s$ divides both ✓', size=28, hand='(3)  p·q^2·s  divides both   ✓')
n4 = I('n4', '(4) $p\\cdot q\\cdot s$ divides both, but smaller', size=28, hand='(4)  p·q·s  divides both,  but smaller')
video('solve-q-389', 'solution', qid='q-389', slides=[
    S('Method 1 · Common factor',
      L("p, q, r and s are different prime numbers. Given: x is equal to p cubed, times q squared, times s. And y is equal "
        "to p, times q to the power of five, times r, times s squared. What is the greatest common divisor of x and y?",
        pt('stem', 'p, q, r', 'hl', 12.0), voice='calm', pause=0.5),
      L("So two numbers, already written in primes, and they ask for their greatest common divisor. It sounds like a big "
        "name, so let's say it in plain words. A common divisor divides both numbers, and the greatest one is the biggest "
        "number that divides both. And divisor means factor, so it's really the greatest common factor. [short pause] "
        "We'll solve it two ways, taking out a common factor, and then checking which choices divide both.",
        pt('stem', 'already written in primes'), show(g0, 'the biggest number that divides both'), pt('g0', 'divisor means factor')),
      L("[short pause] You already know how to take out a common factor. Picture x plus y, and ask what I "
        "can take out of both, in front of the brackets. Whatever comes out of both, divides both. And the biggest thing "
        "that comes out is the GCD.", show(g1, 'Whatever comes out of both'), pt('stem', 'Picture x plus y')),
      L("So let's go prime by prime. p. x has p to the power of three, three p's, and y has just one p. How many p's are in "
        "both? Only one. So one p. Why not p cubed? Because y has only one p, so a number with two or three p's can't divide "
        "y.", show(m1, 'x has p to the power of three'), mk('circle', 'm1: a', 'So one p'), pt('m1', 'Why not p cubed')),
      L("q. x has q squared, two q's, and y has q to the power of five. Both of them have at least two q's, so q squared.",
        show(m2, 'x has q squared'), mk('circle', 'm2: a', 'so q squared')),
      L("r. Is r in x? No, only y has it. So r can't divide x, and it stays out.", show(m3, 'only y has it')),
      L("s. x has one s, and y has s squared, so one s. Each shared prime, at its lower power.",
        show(m4, 'x has one s'), mk('circle', 'm4: a', 'so one s'), show(k1, 'Each shared prime'), mk('underline', 'k1', 'at its lower power')),
      L("So the GCD is p, times q squared, times s. Choice number three is our answer.",
        show(m5, 'So the GCD is'), mk('tick', 'choice 3', 'Choice number three is our answer')),
      L("Now careful with choice number two. It takes every prime at its higher power, and that's too big, it doesn't even "
        "divide x. That's the smallest number that both of them divide, the least common multiple. It's the tool of the "
        "next question.", pt('choice 2', 'careful with choice number two'), mk('cross', 'choice 2', "it doesn't even divide x"))),
    S('Lower power, in numbers',
      L("Let's see the lower power in numbers. Take a hundred seventy-two and a hundred twelve. What do they share? I have "
        "no idea yet, so I start by dividing by two. A hundred seventy-two is two times eighty-six, and eighty-six is two "
        "times forty-three. Forty-three is a prime. So a hundred seventy-two is two squared times forty-three.",
        show(T172['root'], 'Take a hundred seventy-two'), show(T172[1], 'A hundred seventy-two is two times'),
        show(T172[2], 'eighty-six is two times'), show(w1, 'So a hundred seventy-two is')),
      sb='Method 1 · Common factor'),
    S('Lower power, in numbers',
      L("A hundred twelve is two times fifty-six, fifty-six is two times twenty-eight, twenty-eight is two times fourteen, "
        "and fourteen is two times seven. So a hundred twelve is two to the power of four, times seven.",
        show(T112['root'], 'A hundred twelve is'), show(T112[1], 'two times fifty-six'), show(T112[2], 'two times twenty-eight'),
        show(T112[3], 'two times fourteen'), show(T112[4], 'two times seven'), show(w1b, 'A hundred twelve is'), show(w2, 'So a hundred twelve is')),
      L("Not sure you broke it down right? Multiply back. Two to the power of four is sixteen, and sixteen times seven is a "
        "hundred twelve. Perfect.", pt('w2', 'Multiply back')),
      L("So what do they share? Only twos. A hundred twelve has four of them, but a hundred seventy-two has only two. So the "
        "GCD is two squared, just four. A hundred seventy-two over four is forty-three, and a hundred twelve over four is "
        "twenty-eight. Such big numbers, and the biggest thing they share is four.",
        pt('w1b', 'Only twos'), show(w3, 'So the GCD is two squared'), mk('circle', 'w3: f', 'just four')),
      sb='Method 1 · Common factor'),
    S('Method 2 · Which choices divide both',
      L("[pause] Our second method, going through the choices. The GCD has to divide both x and y. So first, I throw out "
        "every choice that doesn't divide both, and then, from what's left, I take the biggest.", pt('choice 1', 'going through the choices')),
      L("Choice number one has an r. x has no r at all, so it can't divide x. Out.",
        show(n1, 'Choice number one has an r'), mk('cross', 'choice 1', 'Out.')),
      L("Choice number two has p cubed. y has only one p, so p cubed can't divide y. Out.",
        show(n2, 'Choice number two has p cubed'), mk('cross', 'choice 2', 'Out.')),
      L("Choice number three, p, q squared, s. x has three p's, two q's and one s, enough of each. y has one p, five q's and "
        "two s's, enough again. So it divides both.", show(n3, 'Choice number three, p'), pt('stem', "x has three p's")),
      L("Choice number four, p, q, s, divides both too. But it's smaller, it has only one q, where choice number three has "
        "two. And they ask for the greatest. So choice number three. [pause] Okay. I'll see you in the next question.",
        show(n4, 'Choice number four, p'), mk('cross', 'choice 4', "But it's smaller"), mk('tick', 'choice 3', 'So choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-390 (Q6)
# NEW: "the greatest number guaranteed to divide" = the smallest number both divide (the LCM); every prime at its HIGHER
# power; an overlap is counted once (her 3 and 7 -> 21, 3 and 9 -> not 27); the trap 250; the smallest-number method;
# GCD x LCM = the product, with its why.  REMINDER: the LCM and running through multiples (topic 2 fraction-add).
e1 = I('e1', '$10=2\\cdot5\\qquad 25=5\\cdot5$', hand='10 = 2·5        25 = 5·5')
e2 = I('e2', '$3$ and $7$: $\\ 21$ ✓', size=30, col=1, hand='3  and  7 :   21   ✓')
e3 = I('e3', '$3$ and $9$: $\\ 27$? $\\ 9$ ✗', size=30, col=1, hand='3  and  9 :   27 ?    9   ✗')
e4 = I('e4', 'An overlap: count it once', size=28, col=1)
e5 = I('e5', 'Twos: $1\\qquad$ Fives: $2$', hand='Twos :  1          Fives :  2')
k2 = I('k2', 'Every prime at its higher power', size=28, col=1)
e6 = I('e6', '$2\\cdot5^2=2\\cdot25=\\hl{a}{50}$', hand='2·5^2 = 2·25 = \\hl{a}{50}')
e7 = I('e7', '$250$ does not divide $50$ ✗', size=30, hand='250  does not divide  50   ✗')
f0 = I('f0', 'Guaranteed: divides even the smallest one', size=28, col=1)
f1 = I('f1', 'Multiples of $25$: $\\ 25$ ✗ $\\ \\ \\hl{a}{50}$ ✓', hand='Multiples of 25 :   25  ✗     \\hl{a}{50}  ✓')
f2 = I('f2', '$25$ ✓ $\\quad 50$ ✓ $\\quad 100$ ✗ $\\quad 250$ ✗', hand='25 ✓     50 ✓     100 ✗     250 ✗')
f3 = I('f3', 'Greatest guaranteed divisor $=$ LCM', size=28, col=1)
h1 = I('h1', 'GCD $\\cdot$ LCM $=a\\cdot b$', hand='GCD · LCM = a·b')
h2 = I('h2', '$10\\cdot25=250$, $\\ $GCD $=5$', hand='10·25 = 250,    GCD = 5')
h3 = I('h3', 'LCM $=\\frac{250}{5}=\\hl{a}{50}$', hand='LCM = {250/5} = \\hl{a}{50}')
video('solve-q-390', 'solution', qid='q-390', slides=[
    S('Method 1 · Primes',
      L("A number is divisible without remainder by both ten and twenty-five. What is the greatest number that is "
        "guaranteed to divide it?", pt('stem', 'A number', 'hl', 7.0), voice='calm', pause=0.5),
      L("So we don't know the number. All we know is that ten divides it, and twenty-five divides it. And they ask, what's "
        "the biggest number we can be sure divides it? [short pause] We'll solve it three ways, with primes, with the "
        "smallest number that fits, and with a short formula.", pt('stem', 'ten divides it'), pt('stem', 'biggest number we can be sure')),
      L("[short pause] If ten divides the number, the number contains all of ten. And if "
        "twenty-five divides it, it contains all of twenty-five. So let's break both. Ten is two times five, and "
        "twenty-five is five times five.", show(e1, 'Ten is two times five')),
      L("Now, why not just multiply ten by twenty-five? Let's see it on simpler numbers. A number that divides by three and "
        "by seven surely divides by twenty-one, because three and seven share nothing. But a number that divides by three "
        "and by nine, does it divide by twenty-seven? Not necessarily. Nine itself divides by three and by nine, and it "
        "doesn't divide by twenty-seven. Nine already has the three inside it.",
        show(e2, 'by seven surely divides'), show(e3, 'and by nine, does it'), pt('e3', 'Nine itself')),
      L("The same thing happens here. The five in ten may be the very same five that's inside twenty-five. When there's an "
        "overlap, we don't count it twice.", pt('e1', 'The five in ten'), show(e4, "we don't count it twice")),
      L("So how many of each prime do I need? Twos, only ten has one, so one two. Fives, ten needs one and twenty-five "
        "needs two, and two fives cover both. So every prime at its higher power.",
        show(e5, 'Twos, only ten'), show(k2, 'every prime at its higher power')),
      L("Two times five squared, two times twenty-five, is fifty. So fifty, choice number three is our answer.",
        show(e6, 'Two times five squared'), mk('circle', 'e6: a', 'is fifty'), mk('tick', 'choice 3', 'choice number three is our answer')),
      L("And now careful with two hundred fifty, the trap. That's ten times twenty-five, the five counted twice. Can we "
        "promise it? The number might be just fifty, and two hundred fifty doesn't divide fifty. So choice number four is "
        "out.", pt('choice 4', 'two hundred fifty, the trap'), show(e7, 'The number might be just fifty'), mk('cross', 'choice 4', 'choice number four is out'))),
    S('Method 2 · The smallest number',
      L("[pause] Our second method, the smallest number that fits. A number that's guaranteed to divide must divide every "
        "number that fits, so it must divide even the smallest one. So let's find the smallest number that both ten and "
        "twenty-five divide. Remember the common denominator from fractions, I run through the multiples of the bigger "
        "one.", show(f0, 'divide even the smallest one'), pt('stem', 'both ten and')),
      L("Multiples of twenty-five. Twenty-five, does ten divide it? No. Fifty, does ten divide it? Yes, fifty is five tens. "
        "So fifty is the smallest number that fits.", show(f1, 'Multiples of twenty-five'), mk('circle', 'f1: a', 'So fifty is the smallest')),
      L("Now the choices. Twenty-five divides fifty, so it's guaranteed, but it's not the greatest. A hundred and two "
        "hundred fifty are bigger than fifty, so they can't divide it. Out. And fifty divides itself, so the greatest "
        "guaranteed divisor is fifty, choice number three.",
        show(f2, 'Now the choices'), mk('cross', 'choice 1', "it's not the greatest"), mk('cross', 'choice 2', 'A hundred and'),
        mk('cross', 'choice 4', "can't divide it"), mk('tick', 'choice 3', 'guaranteed divisor is fifty')),
      L("And this smallest common multiple has a name you saw with fractions, the LCM, the least common multiple. So the "
        "greatest guaranteed divisor is just the LCM.", show(f3, 'the least common multiple'))),
    S('Method 3 · Product over GCD',
      L("[pause] Our third method, a short formula. The GCD times the LCM equals the two numbers multiplied. Why? "
        "Multiplying ten by twenty-five counts the shared five twice. Dividing by the GCD, the part they share, takes the "
        "extra five off.", show(h1, 'The GCD times the LCM'), pt('h1', 'counts the shared five twice')),
      L("Ten times twenty-five is two hundred fifty. The GCD of ten and twenty-five is five, the one five they share. Two "
        "hundred fifty over five is fifty. Choice number three again. [pause] Okay. I'll see you in the next question.",
        show(h2, 'Ten times twenty-five'), show(h3, 'over five is fifty'),
        mk('tick', 'choice 3', 'Choice number three again'))),
])

# ------------------------------------------------------------------------------------------------ q-398 (Q7)
# NEW: building a product - it can only contain the primes the pieces bring (1 brings nothing), and no more pieces than
# there are digits; odd times odd is odd (why: no factor of two anywhere).  REMINDER: the missing prime (q-388).
l1 = I('l1', 'Digits bring only $3$s and $5$s', size=28, col=1)
l2 = I('l2', 'At most three of them', size=28, col=1)
l3 = I('l3', '$45=3\\cdot3\\cdot5$ $\\ \\to\\ 335$ ✓', hand='45 = 3·3·5   →   335   ✓')
l4 = I('l4', '$30=\\hl{t}{2}\\cdot3\\cdot5$ ✗', hand='30 = \\hl{t}{2}·3·5   ✗')
l5 = I('l5', '$25=1\\cdot5\\cdot5$ $\\ \\to\\ 155$ ✓', hand='25 = 1·5·5   →   155   ✓')
l6 = I('l6', '$15=1\\cdot3\\cdot5$ $\\ \\to\\ 135$ ✓', hand='15 = 1·3·5   →   135   ✓')
o1 = I('o1', 'odd $\\cdot$ odd $=$ odd', hand='odd · odd = odd')
o2 = I('o2', '$3\\cdot5=15\\qquad 5\\cdot5=25$', hand='3·5 = 15        5·5 = 25')
o3 = I('o3', 'Even needs a factor of $2$', size=28, col=1)
o4 = I('o4', '$30$ is even ✗', hand='30  is even   ✗')
video('solve-q-398', 'solution', qid='q-398', slides=[
    S('Method 1 · Break into primes',
      L("A lock code has three digits, and each digit is one, three or five. A digit may repeat. Which of the following "
        "cannot be the product of the three digits?", pt('stem', 'A lock code', 'hl', 8.0), voice='calm', pause=0.5),
      L("So we build a product out of three digits, and every digit is one, three or five. The question is which number "
        "can't be built, and that's really a question about a missing prime. [short pause] We'll solve it two ways, "
        "breaking each choice into primes, and then even and odd.", pt('stem', 'every digit is one, three or five'), pt('stem', "which number can't be built")),
      L("[short pause] What primes can the digits bring? One brings nothing, it doesn't change a product. "
        "Three brings a three, and five brings a five. So any product we build has only threes and fives in it, and at most "
        "three of them, because there are three digits.", show(l1, 'only threes and fives'), show(l2, 'at most three of them')),
      L("Forty-five. Forty-five is nine times five, and nine is three times three. So three, three, five. Exactly three "
        "digits, the code three, three, five. It works, so choice number one is out.",
        show(l3, 'Forty-five is nine times five'), mk('cross', 'choice 1', 'choice number one is out')),
      L("Thirty. Thirty is two times fifteen, so two times three times five. It needs a two. Can any digit bring a two? One, "
        "three, five, no. So thirty can't be built.", show(l4, 'Thirty is two times fifteen'), mk('circle', 'l4: t', 'It needs a two'), pt('l1', 'Can any digit')),
      L("In the exam you'd circle it and move on. Here, let's check the rest. Twenty-five is five times five. That's only "
        "two digits, so the third digit is one, the code one, five, five. Choice number three is out.",
        mk('tick', 'choice 2', 'circle it'), show(l5, 'Twenty-five is five times five'), mk('cross', 'choice 3', 'Choice number three is out')),
      L("Fifteen is three times five, and again a one for the third digit, one, three, five. Choice number four is out. So "
        "thirty, choice number two is our answer.", show(l6, 'Fifteen is three times five'), mk('cross', 'choice 4', 'Choice number four is out'),
        mk('tick', 'choice 2', 'choice number two is our answer'))),
    S('Method 2 · Even and odd',
      L("[pause] Now let's look at it with even and odd. All the digits are odd. And odd times odd is always odd. Three times five "
        "is fifteen, and five times five is twenty-five, odd every time. Why? An even product needs a factor of two "
        "somewhere, and odd numbers don't have a two in them.", show(o1, 'odd times odd is always odd'), show(o2, 'Three times five'),
        show(o3, 'An even product needs')),
      L("So a product of three odd digits is always odd. Thirty is even, so it can't be the product. Choice number two. "
        "[pause] Okay. I'll see you in the next question.", show(o4, 'Thirty is even'), mk('tick', 'choice 2', 'Choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-399 (Q8)
# NEW: listing factor pairs in order, from the smallest allowed factor up to the square root (why stop there: the pairs
# come back reversed); 10 x 10 is the pair students forget (the trap 33); the extremes method.
# REMINDER: |x - y| is the bigger minus the smaller (topic 13).
i0 = I('i0', '$A=|x-y|$: $\\ $bigger minus smaller', size=28, col=1, hand='A = |x−y| :  bigger minus smaller')
i1 = I('i1', '$2\\cdot50$: $\\ A=48$', size=28, hand='2·50 :   A = 48')
i2 = I('i2', '$4\\cdot25$: $\\ A=21$', size=28, hand='4·25 :   A = 21')
i3 = I('i3', '$5\\cdot20$: $\\ A=15$', size=28, hand='5·20 :   A = 15')
i4 = I('i4', '$10\\cdot10$: $\\ A=\\hl{z}{0}$', size=28, hand='10·10 :   A = \\hl{z}{0}')
i5 = I('i5', 'Stop at $\\sqrt{100}=10$', size=28, col=1, hand='Stop at  √{100} = 10')
i6 = I('i6', '$48-0=\\hl{a}{48}$', size=32, col=1, hand='48 − 0 = \\hl{a}{48}')
i7 = I('i7', 'Forgot $10\\cdot10$? $\\ 48-15=33$ ✗', size=28, col=1, hand='Forgot 10·10 ?   48 − 15 = 33   ✗')
j1 = I('j1', 'Far apart: $\\ 2\\cdot50$, $\\ 50-2=48$', hand='Far apart :   2·50,    50 − 2 = 48')
j2 = I('j2', 'Close: $\\ 10\\cdot10$, $\\ 10-10=0$', hand='Close :   10·10,    10 − 10 = 0')
j3 = I('j3', '$48-0=\\hl{a}{48}$', hand='48 − 0 = \\hl{a}{48}')
video('solve-q-399', 'solution', qid='q-399', slides=[
    S('Method 1 · Every pair',
      L("x and y are positive integers, and neither of them is one. Given: x times y is equal to a hundred, and A is equal "
        "to the absolute value of x minus y. What is the difference between the greatest possible value of A and the "
        "smallest possible value of A?", pt('stem', 'x and y are', 'hl', 12.0), voice='calm', pause=0.5),
      L("A long story, but underneath, it's just breaking a hundred into two factors. A is the distance between x and y. "
        "The bars make it positive, so it's the bigger one minus the smaller one. And they want the biggest A minus the "
        "smallest A. [short pause] We'll solve it two ways, listing every pair, and then thinking about the extremes.",
        pt('stem', 'breaking a hundred into two factors'), show(i0, 'The bars make it positive'), pt('stem', 'the biggest A')),
      L("[short pause] Let's start with every pair. I start with the smallest factor and go up. One isn't allowed, so no "
        "one times a hundred. Two times fifty, and the difference is forty-eight. Three? A hundred doesn't divide by three. "
        "Four times twenty-five, and the difference is twenty-one.",
        pt('stem', "One isn't allowed"), show(i1, 'Two times fifty'), show(i2, 'Four times twenty-five')),
      L("Five times twenty, and the difference is fifteen. Six, seven, eight and nine, none of them divide a hundred. And ten "
        "times ten, the difference is zero.", show(i3, 'Five times twenty'), show(i4, 'And ten times ten'), mk('circle', 'i4: z', 'the difference is zero')),
      L("Can I stop here? Yes. Why? After ten, the pairs just come back reversed. Twenty times five is the same pair as "
        "five times twenty. Ten is where they meet, because ten times ten is a hundred, ten is the square root.",
        show(i5, 'Can I stop here'), pt('i3', 'the same pair'), pt('i4', 'Ten is where they meet')),
      L("So the biggest A is forty-eight, and the smallest is zero. Forty-eight minus zero is forty-eight, so choice number "
        "three is our answer.", pt('i1', 'the biggest A'), pt('i4', 'the smallest is zero'), show(i6, 'Forty-eight minus zero'),
        mk('tick', 'choice 3', 'choice number three is our answer')),
      L("Now careful, ten times ten is the pair a lot of students forget, because x and y feel like they should be "
        "different. Without it, the smallest A is fifteen, and forty-eight minus fifteen is thirty-three. That's choice "
        "number one, the trap. And twenty-one and fifteen are just single values of A.",
        pt('i4', 'ten times ten is the pair'), show(i7, 'Without it'), mk('cross', 'choice 1', 'the trap'),
        mk('cross', 'choice 2', 'And twenty-one'), mk('cross', 'choice 4', 'and fifteen are'))),
    S('Method 2 · The extremes',
      L("[pause] Another way is to think about the extremes. When is A biggest? When x and y are as far apart as possible, so one of "
        "them is as small as it can be. One isn't allowed, so the smallest is two, and the other is a hundred over two, "
        "fifty. Fifty minus two is forty-eight.", pt('stem', "One isn't allowed"), show(j1, 'as far apart as possible')),
      L("When is A smallest? When they're as close as possible. Can they be equal? Only if a hundred is a perfect square, "
        "and it is, ten times ten. So the smallest A is ten minus ten, zero.", show(j2, 'as close as possible')),
      L("Forty-eight minus zero, forty-eight. Choice number three. The rest of the story, the greatest A and the smallest A, "
        "is just words to make it look harder. [pause] Okay. I'll see you in the next question.",
        show(j3, 'Forty-eight minus zero'), mk('tick', 'choice 3', 'Choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-400 (Q9)
# NEW: building every product in order (pairs, then all three); the order of the cards doesn't matter; "two or more"
# includes all three (the trap 59); a quick bound from the choices (the sum is more than 70).
z1 = I('z1', 'Pairs, then all three', size=28, col=1)
z2 = I('z2', '$2\\cdot5=10\\quad 2\\cdot7=14\\quad 5\\cdot7=35$', hand='2·5 = 10      2·7 = 14      5·7 = 35')
z3 = I('z3', '$2\\cdot5\\cdot7=\\hl{s}{70}$', hand='2·5·7 = \\hl{s}{70}')
z4 = I('z4', '$70+35+14+10=\\hl{a}{129}$', hand='70 + 35 + 14 + 10 = \\hl{a}{129}')
z5 = I('z5', 'Forgot $70$? $\\ 10+14+35=59$ ✗', size=28, col=1, hand='Forgot 70 ?   10 + 14 + 35 = 59   ✗')
y1 = I('y1', '$2\\cdot5\\cdot7=70$, $\\ $plus the pairs', hand='2·5·7 = 70,   plus the pairs')
y2 = I('y2', 'Sum $>70$: $\\ $only $129$', hand='Sum > 70 :   only 129')
video('solve-q-400', 'solution', qid='q-400', slides=[
    S('Method 1 · Build every product',
      L("Dan has three cards with the numbers two, five and seven. He picks two or more of the cards and multiplies their "
        "numbers. What is the sum of all the different products he can get?", pt('stem', 'Dan has', 'hl', 9.0), voice='calm', pause=0.5),
      L("So this time we don't break a number, we build numbers. Two or more cards, multiplied, and then we add up all the "
        "products. [short pause] We'll solve it two ways, building every product, and then a quick look at the choices.",
        pt('stem', 'Two or more cards, multiplied'), pt('stem', 'add up all the')),
      L("[short pause] So I don't miss any, I go in order, first every pair of cards, and then all three "
        "together. Does the order of the cards matter? No, two times five and five times two are the same product, so each "
        "pair counts once.", show(z1, 'first every pair')),
      L("Pairs. Two times five is ten. Two times seven is fourteen. Five times seven is thirty-five.",
        show(z2, 'Two times five is ten'), voice='calm'),
      L("And now careful, two or more includes all three. A lot of students stop at the pairs. Two times five times seven, "
        "ten times seven, is seventy.", pt('stem', 'two or more'), show(z3, 'Two times five times seven'), mk('circle', 'z3: s', 'is seventy')),
      L("Are they all different? Yes. With different primes, every group gives its own product. Now let's add, starting "
        "from the big one. Seventy plus thirty-five is a hundred five. Plus fourteen is a hundred nineteen. Plus ten is a "
        "hundred twenty-nine. Choice number one is our answer.",
        pt('z2', 'Are they all different'), show(z4, 'Seventy plus thirty-five'), mk('circle', 'z4: a', 'hundred twenty-nine.'),
        mk('tick', 'choice 1', 'Choice number one is our answer')),
      L("And look, if you forget the seventy, you get fifty-nine, and it's right there in the choices, choice number four. "
        "And seventy and fourteen are single products, not the sum.",
        show(z5, 'if you forget the seventy'), mk('cross', 'choice 4', 'choice number four'), mk('cross', 'choice 2', 'And seventy'),
        mk('cross', 'choice 3', 'and fourteen'))),
    S('Method 2 · Look at the choices',
      L("[pause] Now a quick look at the choices. One of the products is all three cards together, two times "
        "five times seven, seventy. And the pairs add more on top of it. So the sum is more than seventy.",
        show(y1, 'all three cards together'), pt('y1', 'the pairs add more')),
      L("Which choices are more than seventy? Only a hundred twenty-nine. Seventy, fourteen and fifty-nine are all seventy "
        "or less. So choice number one. [pause] Okay. I'll see you in the next question.",
        show(y2, 'Which choices are more'), mk('cross', 'choice 2', 'Seventy, fourteen'), mk('cross', 'choice 3', 'fourteen and'),
        mk('cross', 'choice 4', 'fifty-nine are'), mk('tick', 'choice 1', 'So choice number one'))),
])

# ------------------------------------------------------------------------------------------------ q-401 (Q10)
# NEW: the square root of a prime is never a whole number (why: a whole m makes m squared = m times m, which breaks; the
# edges 0, 1 and negative whole numbers too); prime / even / odd describe whole numbers only; the trap "m is prime".
# REMINDER: square roots between two perfect squares (topic 9).
n1 = I('n1', '$m$ whole: $\\ m^2=m\\cdot m$ breaks', size=32, hand='m whole :   m^2 = m·m  breaks')
n2 = I('n2', '$3^2=9=3\\cdot3$ ✗ $\\quad 4^2=16=4\\cdot4$ ✗', size=32, hand='3^2 = 9 = 3·3  ✗      4^2 = 16 = 4·4  ✗')
n3 = I('n3', '$(-3)^2=9$ ✗ $\\quad 0^2=0\\quad 1^2=1$', size=32, hand='(−3)^2 = 9  ✗      0^2 = 0      1^2 = 1')
n4 = I('n4', 'So $m$ is $\\hl{w}{\\text{not a whole number}}$', size=32, hand='So  m  is  \\hl{w}{not a whole number}')
k1 = I('k1', 'Prime, even, odd: whole numbers only', size=28, col=1)
p1 = I('p1', '$m^2=2$ $\\ \\to\\ m=\\sqrt{2}$', hand='m^2 = 2   →   m = √{2}')
p2 = I('p2', '$1^2=1<2<4=2^2$', hand='1^2 = 1 < 2 < 4 = 2^2')
p3 = I('p3', '$\\sqrt2$: $\\ $not prime, not even, not odd', size=32, hand='√{2} :   not prime,  not even,  not odd')
p4 = I('p4', 'Three out: $\\ m$ is not an integer ✓', size=32, hand='Three out :   m  is not an integer   ✓')
video('solve-q-401', 'solution', qid='q-401', slides=[
    S('Method 1 · Understanding',
      L("Given: m squared is a prime number. Which of the following is necessarily true?", pt('stem', 'Given', 'hl', 5.0), voice='calm', pause=0.5),
      L("A confusing one, and a lot of students fall for the trap here. They see prime, and decide that m is prime too. But "
        "it's m squared that's prime, not m. [short pause] We'll solve it two ways, understanding first, and then plugging "
        "in numbers.", pt('choice 1', 'decide that m is prime too'), pt('stem', "it's m squared that's prime")),
      L("[short pause] Remember, a prime can't be broken into two smaller whole numbers. So what if m were "
        "a whole number? Then m squared is m times m. Let's see it in numbers. Three squared is nine, three times three, so "
        "it breaks, not prime. Four squared is sixteen, four times four, it breaks too.",
        show(n1, 'what if m were'), show(n2, 'Three squared is nine')),
      L("And negative whole numbers? Negative three times negative three is nine as well, the same thing. And the edges, zero squared is "
        "zero, and one squared is one, and neither of them is prime.", show(n3, 'Negative three times')),
      L("So whatever whole number m is, m squared is never prime. And therefore m can't be a whole number at all.",
        show(n4, 'And therefore m')),
      L("Now the choices. Prime, even and odd are words for whole numbers only. A number that isn't whole is not prime, not "
        "even and not odd. So choice numbers one, three and four are out, and m is not an integer. Choice number two is our "
        "answer.", show(k1, 'Prime, even and odd'), mk('cross', 'choice 1', 'choice numbers one'), mk('cross', 'choice 3', 'three and four'),
        mk('cross', 'choice 4', 'are out'), mk('tick', 'choice 2', 'Choice number two is our'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers. Here I don't pick m, I pick m squared, because the given is about m "
        "squared. m squared is a prime, so let's take the smallest prime, two.", pt('stem', 'the given is about'), show(p1, 'the smallest prime, two')),
      L("m squared is two, so m is the square root of two. Is that a whole number? One squared is one, and two squared is "
        "four. So root two is between one and two, and it's not whole.", show(p2, 'One squared is one')),
      L("So m is root two. Is root two prime? No, only whole numbers can be prime. Even? Odd? No and no. Not an integer? "
        "Yes. So choice numbers one, three and four are out.",
        show(p3, 'Is root two prime'), mk('cross', 'choice 1', 'choice numbers one'), mk('cross', 'choice 3', 'three and four'), mk('cross', 'choice 4', 'are out')),
      L("Three choices are out, so there's no need to try another prime. Choice number two. [pause] Okay. I'll see you in "
        "the next question.", show(p4, 'no need to try another'), mk('tick', 'choice 2', 'Choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-402 (Q11)
# NEW: divisors come in pairs that multiply to the number; an odd count only when a divisor pairs with itself, so an odd
# count means a perfect square; exactly three divisors = a prime squared (why: the middle divisor's own divisors are
# among 1, d, k); the plugging-in check with k = 4.
d1 = I('d1', '$18$: $\\ 1\\cdot18,\\ \\ 2\\cdot9,\\ \\ 3\\cdot6$ $\\ \\to\\ 6$', size=32, hand='18 :   1·18,   2·9,   3·6   →   6')
d2 = I('d2', '$16$: $\\ 1\\cdot16,\\ \\ 2\\cdot8,\\ \\ \\hl{m}{4\\cdot4}$ $\\ \\to\\ 5$', size=32, hand='16 :   1·16,   2·8,   \\hl{m}{4·4}   →   5')
k2 = I('k2', 'Odd count: a perfect square', size=28, col=1)
d3 = I('d3', '$1,\\ \\hl{d}{d},\\ k$ $\\quad$ with $\\ d\\cdot d=k$', size=32, hand='1,   \\hl{d}{d},   k       d·d = k')
d4 = I('d4', '$d$ is prime, $\\ k=d^2$', size=32, hand='d  is prime,    k = d^2')
d5 = I('d5', '$49$: $\\ 1,\\ 7,\\ 49$', size=30, col=1, hand='49 :   1,   7,   49')
d6 = I('d6', '$C=\\sqrt{k}=d$: $\\ $prime, $\\ \\hl{a}{2}$ divisors', size=32, hand='C = √{k} = d :   prime,   \\hl{a}{2}  divisors')
q1 = I('q1', '$2$: $1,2\\quad 3$: $1,3\\quad 4$: $1,2,4$ ✓', hand='2 : 1, 2      3 : 1, 3      4 : 1, 2, 4  ✓')
q2 = I('q2', '$C=\\sqrt4=2$: $\\ 1,\\ 2$ $\\ \\to\\ \\hl{a}{2}$', hand='C = √{4} = 2 :   1, 2   →   \\hl{a}{2}')
q3 = I('q3', 'Every number has the divisor $1$', size=28, col=1)
video('solve-q-402', 'solution', qid='q-402', slides=[
    S('Method 1 · Divisor pairs',
      L("k is a positive integer with exactly three different divisors, including one and k. Given: C is equal to the "
        "square root of k. How many divisors does C have, including one and C?", pt('stem', 'k is a positive', 'hl', 10.0), voice='calm', pause=0.5),
      L("So k has exactly three divisors, and C is its square root. That sounds very abstract, so first let's understand "
        "which numbers have exactly three divisors. [short pause] We'll solve it two ways, with divisor pairs, and then "
        "plugging in a number.", pt('stem', 'exactly three divisors'), pt('stem', 'C is its square root')),
      L("[short pause] Let's start with divisor pairs. Divisors come in pairs that multiply to the number. Take eighteen. "
        "One times eighteen, two times nine, three times six. Six divisors, in three pairs.",
        show(d1, 'Take eighteen')),
      L("So most numbers have an even number of divisors. When can the count be odd? Only when one divisor has no partner, "
        "because it pairs with itself. Sixteen. One times sixteen, two times eight, and four times four. Four is counted "
        "once, so sixteen has five divisors, one, two, four, eight and sixteen.",
        pt('d1', 'an even number of divisors'), show(d2, 'Sixteen. One times'), mk('circle', 'd2: m', 'Four is counted once')),
      L("And a divisor that pairs with itself, times itself, gives the number. So an odd number of divisors means a perfect "
        "square.", show(k2, 'an odd number of divisors means'), mk('underline', 'k2', 'a perfect square'))),
    S('Method 1 · Divisor pairs',
      L("Now exactly three divisors. That's one pair, one times k, plus one middle divisor that pairs with itself. Call the "
        "middle divisor d, so d times d is k.", pt('stem', 'exactly three divisors'), show(d3, 'Call the middle divisor d')),
      L("And what are d's own divisors? Anything that divides d also divides k. k has only three divisors, one, d and k, "
        "and k is too big to divide d. So d has only one and itself. So d is a prime, and k is a prime squared.",
        pt('d3: d', "d's own divisors"), pt('d3', 'k is too big'), show(d4, 'So d is a prime')),
      L("For example, forty-nine. One, seven and forty-nine, three divisors, and seven is a prime.", show(d5, 'For example, forty-nine')),
      L("So C, the square root of k, is that middle prime. And a prime has exactly two divisors, one and itself. So two, "
        "choice number two is our answer.", show(d6, 'So C, the square root'), mk('circle', 'd6: a', 'exactly two divisors'),
        mk('tick', 'choice 2', 'choice number two is our answer')),
      sb='Method 1 · Divisor pairs'),
    S('Method 2 · Plugging in a number',
      L("[pause] Now let's try plugging in a number. I need a k with exactly three divisors, so let's try small numbers "
        "and count. Two has one and two, only two divisors. Three, the same. Four has one, two and four. Three divisors, so "
        "k is four.", show(q1, 'Two has one and two')),
      L("Then C is the square root of four, which is two. And two has two divisors, one and two.",
        show(q2, 'Then C is the square root of four'), mk('circle', 'q2: a', 'two divisors, one and two')),
      L("Now the choices, with k is four. One divisor? No. Two? Yes. k would mean four divisors, and C doesn't have four. "
        "Zero? Never, because every number has at least the divisor one. So three choices are out, and it's choice number "
        "two. [pause] Okay. I'll see you in the next question.",
        mk('cross', 'choice 1', 'One divisor? No'), mk('cross', 'choice 3', "C doesn't have four"), show(q3, 'every number has'),
        mk('cross', 'choice 4', 'Zero? Never'), mk('tick', 'choice 2', "it's choice number two"))),
])

# ------------------------------------------------------------------------------------------------ r26-t14-more-tools (lesson)
# NEW: a perfect square has every exponent even (why: each copy of the root brings one of each prime); not a square if
# one exponent is odd; the classic "smallest k so that 45k is a square" -> k = 5 (225 = 15^2), the trap k = 45.
s1 = I('s1', '$100=10\\cdot10=2^2\\cdot5^2$', size=42, hand='100 = 10·10 = 2^2·5^2')
s2 = I('s2', '$10\\cdot10=(2\\cdot5)\\cdot(2\\cdot5)$', size=40, hand='10·10 = (2·5)·(2·5)')
s3 = I('s3', '$50=2\\cdot5^2$: $\\ $odd exponent, not a square', size=38, hand='50 = 2·5^2 :   odd exponent,  not a square')
s4 = I('s4', 'Perfect square: every exponent is even', size=40)
c1 = I('c1', '$45k$ a square, $\\ $smallest $k$?', size=42, hand='45k  a square,   smallest k ?')
c2 = I('c2', '$45=9\\cdot5=3^2\\cdot5$', size=42, hand='45 = 9·5 = 3^2·5')
c3 = I('c3', '$3^2$: even ✓ $\\quad 5$: odd $\\ \\to\\ \\hl{k}{k=5}$', size=40, hand='3^2 : even  ✓       5 : odd   →   \\hl{k}{k = 5}')
c4 = I('c4', '$45\\cdot5=225=15^2$ ✓', size=42, hand='45·5 = 225 = 15^2   ✓')
c5 = I('c5', '$k=45$ works too, but it is not the smallest', size=34)
video('r26-t14-more-tools', 'lesson', slides=[
    S('More Factor Tools',
      L("Welcome back. In this part the prime questions get harder, and almost every one of them starts the same way, break "
        "the number into primes. Before the questions, one more tool that none of them teaches, perfect squares.")),
    S('Perfect squares',
      L("A perfect square is a whole number times itself, like nine, which is three times three, or a hundred, which is ten "
        "times ten. So when is a number a perfect square? Let's look at its primes. A hundred is two squared times five "
        "squared. Both exponents are even.", show(s1, 'A hundred is two squared')),
      L("Why even? A hundred is ten times ten, and each ten brings one two and one five. So the primes come in pairs, one "
        "copy from each ten, and every exponent is even.", show(s2, 'each ten brings')),
      L("Now fifty. Fifty is two times twenty-five, so two times five squared. The two has exponent one, and that's odd. So "
        "fifty is not a perfect square. And really, seven squared is forty-nine and eight squared is sixty-four, so fifty "
        "sits between them.", show(s3, 'Now fifty'), pt('s3', 'seven squared is forty-nine')),
      L("So here's the rule. In a perfect square, every exponent is even. And if even one exponent is odd, it's not a "
        "square.", show(s4, "So here's the rule"), mk('underline', 's4', 'every exponent is even'))),
    S('The classic question',
      L("Here's the classic question. What's the smallest k so that forty-five times k is a perfect square? First, break "
        "forty-five. It's nine times five, so three squared times five.", show(c1, 'the smallest k'), show(c2, 'break forty-five')),
      L("The three has exponent two, even, fine. The five has exponent one, odd. So the five is missing one copy, and k has "
        "to bring it. k is five.", show(c3, 'The three has exponent two'), mk('circle', 'c3: k', 'k is five')),
      L("Let's check it. Forty-five times five is two hundred twenty-five, and that's fifteen times fifteen. Ten times "
        "fifteen is a hundred fifty, and five times fifteen is seventy-five, together two hundred twenty-five.",
        show(c4, 'Forty-five times five')),
      L("Now careful, a lot of students take k as forty-five, to make forty-five squared. That's a square too, but it's not "
        "the smallest. The smallest k brings only the missing primes.", show(c5, 'take k as forty-five'), mk('underline', 'c3', 'only the missing primes')),
      L("There's a card with the factor tools right after this video, and then the advanced questions. Try each one first, "
        "and then watch the solution. [pause] Okay. I'll see you in the next video.", pt('c4', 'a card with the factor tools'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t14-03 (Q12)
# NEW (R32 - the camera lesson only says "same primes at the end" in one line): a number breaks into primes in only one
# way (18 = 2·9 = 3·6), so both sides must have the same twos and threes - match the exponents; dividing down as a
# second method; the swap trap (1) and a + b (5).  REMINDER: factor trees (camera lesson).
f1 = I('f1', 'A number breaks into primes in only one way', size=26, col=1)
f2 = I('f2', '$18=2\\cdot9=3\\cdot6=2\\cdot3^2$', size=30, col=1, hand='18 = 2·9 = 3·6 = 2·3^2')
f3 = I('f3', '$108=4\\cdot27=2^2\\cdot3^3$', hand='108 = 4·27 = 2^2·3^3')
f4 = I('f4', '$2^{\\hl{a}{a}}\\cdot3^{\\hl{b}{b}}=2^2\\cdot3^3$', hand='2^{\\hl{a}{a}}·3^{\\hl{b}{b}} = 2^2·3^3')
f5 = I('f5', '$a=2,\\ \\ b=3$', hand='a = 2,    b = 3')
f6 = I('f6', '$a-b=2-3=\\hl{r}{-1}$', hand='a − b = 2 − 3 = \\hl{r}{−1}')
f7 = I('f7', 'Swapped: $3-2=1$ ✗ $\\quad a+b=5$ ✗', size=28, col=1, hand='Swapped :  3 − 2 = 1  ✗      a + b = 5  ✗')
T108 = TREE('T108', 108, [(2, 54), (2, 27), (3, 9), (3, 3)], w=520, col=0)
f8 = I('f8', 'Twos: $2$ times $\\ \\to\\ a=2$', size=30, col=1, hand='Twos :  2 times   →   a = 2')
f9 = I('f9', 'Threes: $3$ times $\\ \\to\\ b=3$', size=30, col=1, hand='Threes :  3 times   →   b = 3')
f10 = I('f10', '$a-b=2-3=\\hl{r}{-1}$', size=30, col=1, hand='a − b = 2 − 3 = \\hl{r}{−1}')
video('solve-q-r26-t14-03', 'solution', qid='q-r26-t14-03', slides=[
    S('Method 1 · Break and match',
      L("a and b are positive integers. Given: two to the power of a, times three to the power of b, is equal to a hundred "
        "eight. What is a minus b?", pt('stem', 'a and b are', 'hl', 8.0), voice='calm', pause=0.5),
      L("So the left side is written in primes, and the right side is a plain number. The idea is to write a hundred eight "
        "in primes too, and match. [short pause] We'll solve it two ways, breaking and matching, and then dividing down.",
        pt('stem', 'written in primes'), pt('stem', 'a plain number')),
      L("[short pause] Why does matching work? A number breaks into primes in only one way. Wherever you "
        "start the factor tree, you end with the same primes. For example, eighteen. Two times nine breaks into two, three, "
        "three, and three times six breaks into three, two, three. The same primes, just in another order.",
        show(f1, 'in only one way'), show(f2, 'For example, eighteen')),
      L("So if both sides are the same number, they must have the same twos and the same threes. Now a hundred eight. It's "
        "four times twenty-seven, because four times twenty-five is a hundred, and four times two is eight. Four is two "
        "squared, and twenty-seven is three cubed.", pt('f1', 'the same twos'), show(f3, 'Now a hundred eight')),
      L("So two to the power of a, times three to the power of b, is two squared times three cubed. The twos match, so a is "
        "two. The threes match, so b is three.", show(f4, 'So two to the power of a'), mk('circle', 'f4: a', 'so a is two'),
        mk('circle', 'f4: b', 'so b is three'), show(f5, 'so b is three')),
      L("Now careful, they ask for a minus b, not b minus a. Two minus three is negative one, so choice number three is our "
        "answer.", show(f6, 'Two minus three'), mk('tick', 'choice 3', 'choice number three is our answer')),
      L("Choice number one, positive one, is what you get when you swap a and b. Choice number four, five, is a plus b. And "
        "two is just a.", show(f7, 'when you swap'), mk('cross', 'choice 1', 'swap a and b'), mk('cross', 'choice 4', 'is a plus b'),
        mk('cross', 'choice 2', 'two is just a'))),
    S('Method 2 · Divide down',
      L("[pause] Another way is to divide down. I divide by two as long as I can, and count. A hundred eight over two is "
        "fifty-four. Fifty-four over two is twenty-seven. Twenty-seven is odd, so no more twos. Two halvings, so a is two.",
        show(T108['root'], 'divide down'), show(T108[1], 'over two is fifty-four'), show(T108[2], 'Fifty-four over two'), pt('T108_root', 'Two halvings')),
      L("Then the threes. Twenty-seven over three is nine, nine over three is three, and three over three is one. Three "
        "times, so b is three.", show(T108[3], 'Twenty-seven over three'), show(T108[4], 'nine over three'), show(f8, 'Three times'),
        show(f9, 'so b is three')),
      L("a minus b, two minus three, negative one. Choice number three again. [pause] Okay. I'll see you in the next "
        "question.", show(f10, 'a minus b'), mk('tick', 'choice 3', 'Choice number three again'))),
])

# ------------------------------------------------------------------------------------------------ q-391 (Q13)
# NEW: take 2 off each choice and test what's left; 49 = 7·7 looks prime; trial and error would take forever, look for
# the one simple idea.  REMINDER (camera lesson slide 3): odd sum of two primes -> one of them is 2, with its why.
o1 = I('o1', 'All the choices are odd', size=28, col=1)
o2 = I('o2', 'odd $+$ odd $=$ even $\\quad 3+5=8$', size=28, col=1, hand='odd + odd = even      3 + 5 = 8')
o3 = I('o3', 'Odd sum: one prime is $2$', size=28, col=1)
a1 = I('a1', '$15=2+13$ ✓', hand='15 = 2 + 13   ✓')
a2 = I('a2', '$21=2+19$ ✓', hand='21 = 2 + 19   ✓')
a3 = I('a3', '$51=2+\\hl{f}{49}$, $\\ 49=7\\cdot7$ ✗', hand='51 = 2 + \\hl{f}{49},    49 = 7·7   ✗')
a4 = I('a4', '$43=2+41$ ✓', hand='43 = 2 + 41   ✓')
video('solve-q-391', 'solution', qid='q-391', slides=[
    S('The only even prime',
      L("p and q are prime numbers. Which of the following numbers cannot be p plus q?", pt('stem', 'p and q', 'hl', 4.5), voice='calm', pause=0.5),
      L("So two primes and their sum, and one choice can't be that sum. It looks brutal. Trial and error, splitting fifteen "
        "into two primes, then twenty-one, and so on, would take forever. But on this exam there's almost always one simple "
        "idea, and once you see it, the answer falls out.", pt('stem', 'their sum'), pt('choice 1', 'splitting fifteen')),
      L("Look at the choices. Every one of them is odd. And remember from the lesson, the primes are all odd except one, "
        "two, the only even prime. Odd plus odd is even, like three plus five is eight. Even plus even is even too. Only "
        "one even and one odd give an odd sum.", pt('choice 4', 'Every one of them is odd'), show(o1, 'Every one of them'), show(o2, 'Odd plus odd is even')),
      L("So if two primes have an odd sum, one of them must be two. Let's take two off each choice, and check whether what's "
        "left is a prime.", show(o3, 'one of them must be two')),
      L("Fifteen is two plus thirteen. Thirteen is a prime, so fifteen works, and choice number one is out.",
        show(a1, 'Fifteen is two plus thirteen'), mk('cross', 'choice 1', 'choice number one is out')),
      L("Twenty-one is two plus nineteen. Nineteen is a prime, so choice number two is out.",
        show(a2, 'Twenty-one is two plus nineteen'), mk('cross', 'choice 2', 'choice number two is out')),
      L("Fifty-one is two plus forty-nine. Is forty-nine a prime? It looks like one, but no, forty-nine is seven times "
        "seven. And without the two, both primes would be odd, and their sum would be even, not fifty-one. So no pair works, "
        "and fifty-one can't be the sum.", show(a3, 'Fifty-one is two plus'), mk('circle', 'a3: f', 'forty-nine is seven times'), pt('o2', 'without the two')),
      L("In the exam you'd circle it and move on. Here, let's check the last one. Forty-three is two plus forty-one. Forty-one "
        "is odd, its digit sum is five, it doesn't end in five, and its root is less than seven. So it's a prime, choice "
        "number four is out, and fifty-one, choice number three is our answer.",
        show(a4, 'Forty-three is two plus'), mk('cross', 'choice 4', 'choice number four is out'), mk('tick', 'choice 3', 'choice number three is our answer')),
      L("The whole question was one fact, two is the only even prime, and the exam loves it. [pause] Okay. I'll see you in "
        "the next question.", pt('o3', 'The whole question was one fact'))),
])

# ------------------------------------------------------------------------------------------------ q-392 (Q14)
# NEW: count in how many numbers each prime appears ("exactly two of them"); 91 = 7·13 links back to the fake primes.
# REMINDER: breaking numbers into primes (camera lesson); plugging in the answers (topic 51).
g1 = I('g1', '$14=2\\cdot7\\quad 21=3\\cdot7\\quad 5$', size=28, hand='14 = 2·7      21 = 3·7      5')
g2 = I('g2', '$2$: one $\\ \\ 3$: one $\\ \\ 5$: one $\\ \\ 7$: two $\\ \\to\\ \\hl{a}{a=7}$', size=28,
       hand='2 : one    3 : one    5 : one    7 : two   →   \\hl{a}{a = 7}')
g3 = I('g3', '$26=2\\cdot13\\quad 21=3\\cdot7\\quad 42=2\\cdot3\\cdot7$', size=28, hand='26 = 2·13      21 = 3·7      42 = 2·3·7')
g4 = I('g4', '$2,\\ 3,\\ 7$: two each $\\ \\ 13$: one $\\ \\to\\ \\hl{b}{b=13}$', size=28, hand='2, 3, 7 : two each     13 : one   →   \\hl{b}{b = 13}')
g5 = I('g5', '$a\\cdot b=7\\cdot13=\\hl{r}{91}$', col=1, hand='a·b = 7·13 = \\hl{r}{91}')
h1 = I('h1', '(1) $39=3\\cdot13$: $\\ a=3$? one ✗ $\\ a=13$? none ✗', size=26, hand='(1)  39 = 3·13 :   a = 3 ? one  ✗    a = 13 ? none  ✗')
h2 = I('h2', '(2) $26=2\\cdot13$: $\\ a=2$? one ✗ $\\ a=13$? none ✗', size=26, hand='(2)  26 = 2·13 :   a = 2 ? one  ✗    a = 13 ? none  ✗')
h3 = I('h3', '(3) $91=7\\cdot13$: $\\ a=7$ two ✓ $\\ b=13$ one ✓', size=26, hand='(3)  91 = 7·13 :   a = 7  two  ✓    b = 13  one  ✓')
h4 = I('h4', '(4) $21=3\\cdot7$: $\\ a=7,\\ b=3$: two ✗', size=26, hand='(4)  21 = 3·7 :   a = 7,  b = 3 :  two  ✗')
video('solve-q-392', 'solution', qid='q-392', slides=[
    S('Method 1 · Prime factorization',
      L("a and b are prime numbers. Exactly two of the numbers fourteen, twenty-one and five are divisible by a. Exactly "
        "one of the numbers twenty-six, twenty-one and forty-two is divisible by b. What is a times b?",
        pt('stem', 'a and b are', 'hl', 11.0), voice='calm', pause=0.5),
      L("So a and b are primes, and the clues tell us which numbers they divide. Divisible by a prime means that prime is "
        "inside the number. So the first thing is to break every number into primes. [short pause] We'll solve it two ways, "
        "breaking the numbers into primes, and then plugging in the answers.", pt('stem', 'which numbers they divide')),
      L("[short pause] The first group. Fourteen is two times seven. Twenty-one is three times seven. And "
        "five is a prime.", pt('stem', 'The first group'), show(g1, 'Fourteen is two times seven')),
      L("Exactly two of them divide by a. So which prime shows up in exactly two of them? Two is only in fourteen. Three is "
        "only in twenty-one. Five is only in five. Seven is in fourteen and in twenty-one, exactly two. So a is seven.",
        pt('g1', 'which prime shows up'), show(g2, 'Two is only in fourteen'), mk('circle', 'g2: a', 'So a is seven')),
      L("The second group. Twenty-six is two times thirteen. Twenty-one is three times seven. Forty-two is six times seven, "
        "so two times three times seven.", pt('stem', 'The second group'), show(g3, 'Twenty-six is two times thirteen')),
      L("Now exactly one of them divides by b. Two is in twenty-six and forty-two, that's two numbers. Three is in "
        "twenty-one and forty-two, two again. Seven is in twenty-one and forty-two, two again. Thirteen is only in "
        "twenty-six. So b is thirteen.", pt('g3', 'Two is in twenty-six'), show(g4, 'Thirteen is only')),
      L("So a times b is seven times thirteen. Seven times ten is seventy, and seven times three is twenty-one, together "
        "ninety-one. Choice number three is our answer. And remember ninety-one, the fake prime from the start of the "
        "topic.", show(g5, 'seven times thirteen'), mk('circle', 'g5: r', 'together ninety-one'), mk('tick', 'choice 3', 'Choice number three is our answer'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's try plugging in the answers. Each choice is a product of two primes. So I split it, and check "
        "which one could be a, and the other one b.", pt('choice 1', 'Each choice is a product')),
      L("Choice number one, thirty-nine, is three times thirteen. Could a be three? Only twenty-one divides by three, that's "
        "one number, not two. Could a be thirteen? None of fourteen, twenty-one and five divides by thirteen. Out.",
        show(h1, 'thirty-nine, is three times thirteen'), mk('cross', 'choice 1', 'Out.')),
      L("Choice number two, twenty-six, is two times thirteen. Is a two? Only fourteen divides by two. Is a thirteen? None. "
        "Out.", show(h2, 'twenty-six, is two times thirteen'), mk('cross', 'choice 2', 'Out.')),
      L("Choice number three, ninety-one, is seven times thirteen. a is seven, and fourteen and twenty-one divide by seven, "
        "exactly two. Then b is thirteen, and only twenty-six divides by thirteen, exactly one. It fits.",
        show(h3, 'ninety-one, is seven times thirteen'), mk('tick', 'choice 3', 'It fits')),
      L("In the exam you'd circle it and move on. Here, let's check the last one too. Twenty-one is three times seven. a "
        "can't be three, because only one number divides by three. So a is seven, and b is three. But three divides "
        "twenty-one and forty-two, that's two numbers, not one. Out. So choice number three. [pause] Okay. I'll see you in "
        "the next question.", show(h4, 'Twenty-one is three times seven'), mk('cross', 'choice 4', 'not one. Out'), mk('tick', 'choice 3', 'So choice number three'))),
])

# ------------------------------------------------------------------------------------------------ q-393 (Q15)
# NEW: take out a common factor to get a product, then factor pairs that aren't necessarily prime; why a is the smaller
# factor (a < b < b + 4); stop when b drops below a; plugging in the sums.  REMINDER: common factor (topic 4), listing
# factor pairs in order (q-399).
e1 = I('e1', '$a\\cdot b+4a=\\hl{f}{a(b+4)}=48$', hand='a·b + 4a = \\hl{f}{a(b+4)} = 48')
e2 = I('e2', '$a<b<b+4$: $\\ a$ is the small factor', size=28, col=1, hand='a < b < b+4 :   a is the small factor')
e3 = I('e3', '$1\\cdot48$: $\\ b=44,\\ \\ a+b=45$', size=32, hand='1·48 :   b = 44,    a+b = 45')
e4 = I('e4', '$2\\cdot24$: $\\ b=20,\\ \\ a+b=22$', size=32, hand='2·24 :   b = 20,    a+b = 22')
e5 = I('e5', '$3\\cdot16$: $\\ b=12,\\ \\ a+b=15$', size=32, hand='3·16 :   b = 12,    a+b = 15')
e6 = I('e6', '$4\\cdot12$: $\\ b=8,\\ \\ a+b=12$', size=32, hand='4·12 :   b = 8,    a+b = 12')
e7 = I('e7', '$6\\cdot8$: $\\ b=4<6$ ✗', size=30, col=1, hand='6·8 :   b = 4 < 6   ✗')
e8 = I('e8', 'Sums: $45,\\ 22,\\ 15,\\ 12$', size=30, col=1, hand='Sums :   45,  22,  15,  12')
x1 = I('x1', '$45$: $\\ a=1,\\ b=44$: $\\ 44+4=48$ ✓', size=30, hand='45 :   a = 1,  b = 44 :   44 + 4 = 48   ✓')
x2 = I('x2', '$15$: $\\ a=3,\\ b=12$: $\\ 36+12=48$ ✓', size=30, hand='15 :   a = 3,  b = 12 :   36 + 12 = 48   ✓')
x3 = I('x3', '$12$: $\\ a=4,\\ b=8$: $\\ 32+16=48$ ✓', size=30, hand='12 :   a = 4,  b = 8 :   32 + 16 = 48   ✓')
x4 = I('x4', '$17$: $\\ 20,\\ 38,\\ 54,\\ 68,\\ 80$ $\\ $never $48$ ✗', size=30, hand='17 :   20,  38,  54,  68,  80   never 48   ✗')
video('solve-q-393', 'solution', qid='q-393', slides=[
    S('Method 1 · Common factor, then pairs',
      L("a and b are positive integers. Given: a is smaller than b, and a times b, plus four a, is equal to forty-eight. "
        "Which of the following cannot be the value of a plus b?", pt('stem', 'a and b are', 'hl', 9.0), voice='calm', pause=0.5),
      L("Honestly, it's not obvious where to start here. So let's start with what we can do. We have an equation, and a "
        "appears in both terms on the left. [short pause] We'll solve it two ways, taking out a common factor, and then "
        "plugging in the answers.", pt('stem', 'a appears in both terms')),
      L("[short pause] a is in both terms, so I take it out as a common factor. a times b, plus four a, "
        "is a times, in brackets, b plus four. And that's forty-eight.", show(e1, 'I take it out'), mk('circle', 'e1: f', 'in brackets, b plus four')),
      L("So now it's a product of two whole numbers that equals forty-eight. Remember breaking a number into pairs. Here we "
        "break forty-eight into two factors, and they don't have to be primes.", pt('e1', 'a product of two whole numbers')),
      L("Which factor is a? The smaller one. Why? b is bigger than a, and b plus four is even bigger. So a is the small "
        "factor, and b plus four is the big one.", show(e2, 'Which factor is a')),
      L("One times forty-eight. a is one, b plus four is forty-eight, so b is forty-four, and a plus b is forty-five.",
        show(e3, 'One times forty-eight'), voice='calm'),
      L("Two times twenty-four. b plus four is twenty-four, so b is twenty, and a plus b is twenty-two. Not a choice, keep "
        "going. Three times sixteen. b is twelve, and a plus b is fifteen.", show(e4, 'Two times twenty-four'), show(e5, 'Three times sixteen'))),
    S('Method 1 · Common factor, then pairs',
      L("Four times twelve. b is eight, still bigger than four, and a plus b is twelve.", show(e6, 'Four times twelve'), voice='calm'),
      L("Five doesn't divide forty-eight. Six times eight? b plus four is eight, so b is four, and that's smaller than six. "
        "Not allowed. And after that, the factors swap, and a would be the bigger one. So no more options.",
        show(e7, 'Six times eight'), pt('e7', 'the factors swap')),
      L("So the sums can be forty-five, twenty-two, fifteen and twelve. Seventeen isn't one of them, so choice number three "
        "is our answer.", show(e8, 'So the sums can be'), mk('cross', 'choice 1', 'forty-five, twenty-two'), mk('cross', 'choice 2', 'fifteen and'),
        mk('cross', 'choice 4', 'and twelve'), mk('tick', 'choice 3', 'choice number three')),
      sb='Method 1 · Common factor, then pairs'),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's try plugging in the answers. Three choices can be the sum, and one can't. So for each sum, I "
        "try small values of a, and b is the sum minus a. Then I check a times b, plus four a.", pt('stem', 'plus four a')),
      L("Forty-five. a is one, so b is forty-four. One times forty-four is forty-four, and four times one is four. "
        "Forty-four plus four is forty-eight. It works, out.", show(x1, 'Forty-five. a is one'), mk('cross', 'choice 1', 'It works, out')),
      L("Fifteen. a is three, b is twelve. Three times twelve is thirty-six, and four times three is twelve. "
        "Thirty-six plus twelve, forty-eight. Out. Twelve. a is four, b is eight. Four times eight is thirty-two, and four "
        "times four is sixteen. Thirty-two plus sixteen, forty-eight. Out.",
        show(x2, 'Fifteen. a is three'), mk('cross', 'choice 2', 'Thirty-six plus twelve'), show(x3, 'Twelve. a is four'), mk('cross', 'choice 4', 'Thirty-two plus sixteen')),
      L("Seventeen. a is one, b is sixteen, sixteen plus four is twenty. a is two, b is fifteen, thirty plus eight is "
        "thirty-eight. a is three, b is fourteen, forty-two plus twelve is fifty-four, already above forty-eight. Four and "
        "thirteen give fifty-two plus sixteen, sixty-eight, and five and twelve give sixty plus twenty, eighty. It keeps "
        "growing, so it never comes back to forty-eight.", show(x4, 'Seventeen. a is one')),
      L("So seventeen can't be the sum, choice number three. [pause] Okay. I'll see you in the next question.",
        mk('tick', 'choice 3', "So seventeen can't be"))),
])

# ------------------------------------------------------------------------------------------------ q-396 (Q16)
# NEW: "exactly two prime factors: 2 and 3" means both and nothing else; build the smallest number; to grow it, multiply by
# its cheapest allowed prime; every wrong choice is a trap; plugging in from the smallest choice.
b1 = I('b1', '$a$: $\\ 2\\cdot3=6$', hand='a :   2·3 = 6')
b2 = I('b2', '$b$: $\\ 2\\cdot5=10$', hand='b :   2·5 = 10')
b3 = I('b3', '$b<a$? $\\ 10<6$ ✗ $\\ \\to\\ $grow $a$', size=32, hand='b < a ?   10 < 6  ✗   →   grow a')
b4 = I('b4', '$6\\cdot2=\\hl{a}{12}>10$ ✓ $\\quad 6\\cdot3=18$', size=32, hand='6·2 = \\hl{a}{12} > 10  ✓       6·3 = 18')
b5 = I('b5', '$\\frac{12\\cdot10}{15}=\\frac{120}{15}=\\hl{r}{8}$', hand='{12·10/15} = {120/15} = \\hl{r}{8}')
b6 = I('b6', '$\\frac{(2^2\\cdot3)(2\\cdot5)}{3\\cdot5}=2^3$', size=32, col=1, hand='{(2^2·3)(2·5)/3·5} = 2^3')
b7 = I('b7', '$\\frac{6\\cdot10}{15}=4\\quad \\frac{18\\cdot10}{15}=12\\quad \\frac{12\\cdot20}{15}=16$', size=28, col=1)
y1 = I('y1', '$a$: $\\ 6,\\ 12,\\ 18,\\ 24$ $\\qquad b$: $\\ 10,\\ 20,\\ 40,\\ 50$', size=30, hand='a :  6, 12, 18, 24        b :  10, 20, 40, 50')
y2 = I('y2', '$4$: $\\ a\\cdot b=60=6\\cdot10$, $\\ b<a$ ✗', size=30, hand='4 :   a·b = 60 = 6·10,    b < a  ✗')
y3 = I('y3', '$8$: $\\ a\\cdot b=120=12\\cdot10$ ✓', size=30, hand='8 :   a·b = 120 = 12·10   ✓')
video('solve-q-396', 'solution', qid='q-396', slides=[
    S('Method 1 · Build the smallest',
      L("a and b are positive integers. a has exactly two prime factors, two and three. b has exactly two prime factors, two "
        "and five. Given: b is smaller than a. What is the smallest possible value of a times b, over fifteen?",
        pt('stem', 'a and b are', 'hl', 11.0), voice='calm', pause=0.5),
      L("A minimum question, with primes. a is built from twos and threes, and b from twos and fives. And b has to be smaller "
        "than a. [short pause] We'll solve it two ways, building the smallest a and b, and then plugging in the answers, "
        "starting from the smallest.", pt('stem', 'built from twos and threes'), pt('stem', 'b has to be smaller')),
      L("[short pause] When is a times b over fifteen smallest? a and b are both on top of the fraction, "
        "so the smaller they are, the smaller the result. So let's build each one as small as possible.", pt('stem', 'over fifteen smallest')),
      L("a has exactly the prime factors two and three. Exactly means both of them must be there, and nothing else. The "
        "smallest is one two and one three, two times three, six. And b has two and five, so the smallest is two times "
        "five, ten.", show(b1, 'two times three, six'), show(b2, 'two times five, ten')),
      L("But wait, b has to be smaller than a, and ten isn't smaller than six. Can b get smaller than ten? No, it needs a two "
        "and a five. So we have to grow a.", show(b3, 'b has to be smaller than a'), pt('b2', 'Can b get smaller')),
      L("By how much? a can only contain twos and threes, so I can multiply it by two, or by three. Six times two is twelve, "
        "and six times three is eighteen. To keep it as small as possible, times two. Twelve is bigger than ten, it works.",
        show(b4, 'Six times two is twelve'), mk('circle', 'b4: a', 'times two. Twelve'))),
    S('Method 1 · Build the smallest',
      L("So a is twelve and b is ten. Twelve times ten is a hundred twenty, and a hundred twenty over fifteen is eight. Or "
        "with primes, two squared times three, times two times five, over three times five. The three and the five cancel, "
        "and two cubed is eight. Choice number one is our answer.",
        show(b5, 'Twelve times ten'), mk('circle', 'b5: r', 'over fifteen is eight'), show(b6, 'Or with primes'), mk('tick', 'choice 1', 'Choice number one is our answer')),
      L("And every other choice is a trap. Four is six times ten over fifteen, it forgets that b is smaller than a. Twelve "
        "grows a by three instead of two, eighteen times ten over fifteen. And sixteen grows b instead, twelve times twenty "
        "over fifteen.", show(b7, 'every other choice is a trap'), mk('cross', 'choice 4', 'it forgets'), mk('cross', 'choice 3', 'grows a by three'),
        mk('cross', 'choice 2', 'grows b instead')),
      sb='Method 1 · Build the smallest'),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's try plugging in the answers. They ask for the smallest, so I start from the smallest choice, "
        "four. If the result is four, then a times b is four times fifteen, sixty.", pt('choice 4', 'the smallest choice')),
      L("a is made of twos and threes, both of them, so a is six, twelve, eighteen, twenty-four and so on. And b is ten, "
        "twenty, forty, fifty and so on. Which pair multiplies to sixty? Only six times ten. But then b isn't smaller than "
        "a. So four is out.", show(y1, 'so a is six'), show(y2, 'Which pair multiplies to sixty'), mk('cross', 'choice 4', 'So four is out')),
      L("Next, eight. a times b is eight times fifteen, a hundred twenty. Twelve times ten is a hundred twenty, and ten is "
        "smaller than twelve. It works. So the smallest possible value is eight, choice number one. [pause] Okay. I'll see "
        "you in the next question.", show(y3, 'Next, eight'), mk('tick', 'choice 1', 'choice number one'))),
])

# ------------------------------------------------------------------------------------------------ q-394 (Q17)
# NEW: an exponent letter is not a factor (the trap); "enough copies" with letters (r < s, q < r); letters as primes ->
# plug in the smallest primes in the right order, and why; with plugging in, knock out three before you mark.
# REMINDER: a prime power divides only with enough copies (camera lesson slide 9, q-388).
u1 = I('u1', '$z$: $\\ p$, $\\ s$ times $\\cdot$ $q$, $\\ r$ times', size=32, hand='z :   p,  s times   ·   q,  r times')
u2 = I('u2', '$r,\\ s$: only exponents, not factors', size=28, col=1, hand='r, s :  only exponents,  not factors')
u3 = I('u3', 'Enough copies of each prime?', size=28, col=1)
u4 = I('u4', '(3) $q^s$: $\\ z$ has $q$ only $r$ times, $\\ r<s$ ✗', size=30, hand='(3)  q^s :   z has q only r times,   r < s   ✗')
u5 = I('u5', '(2) $p^r$: $\\ r<s$ ✓ $\\quad q^q$: $\\ q<r$ ✓', size=30, hand='(2)  p^r :   r < s  ✓      q^q :   q < r  ✓')
v1 = I('v1', '$p=2,\\ q=3,\\ r=5,\\ s=7$', hand='p = 2,   q = 3,   r = 5,   s = 7')
v2 = I('v2', '$z=2^7\\cdot3^5$', hand='z = 2^7·3^5')
v3 = I('v3', '(2) $2^5\\cdot3^3$: $\\ 5\\le7,\\ \\ 3\\le5$ ✓', size=30, hand='(2)  2^5·3^3 :    5 ≤ 7,    3 ≤ 5   ✓')
v4 = I('v4', '(3) $3^7$: $\\ $only five $3$s ✗ $\\quad$ (4) $7^3$ ✗', size=30, hand='(3)  3^7 :  only five 3s  ✗       (4)  7^3   ✗')
v5 = I('v5', 'Plugging in: knock out three first', size=28, col=1)
video('solve-q-394', 'solution', qid='q-394', slides=[
    S('Method 1 · Understanding',
      L("p, q, r and s are prime numbers, and p is smaller than q, which is smaller than r, which is smaller than s. Given: "
        "z is equal to p to the power of s, times q to the power of r. Which of the following necessarily divides z?",
        pt('stem', 'p, q, r', 'hl', 12.0), voice='calm', pause=0.5),
      L("A hard one, all letters. But underneath, it's a factor question. What is z built from? [short pause] We'll solve it "
        "two ways, understanding with the letters, and then the same idea with numbers.", pt('stem', 'What is z built from')),
      L("[short pause] z is p to the power of s, times q to the power of r. So z contains the prime p, s "
        "times, and the prime q, r times. And nothing else.", show(u1, 'So z contains the prime p')),
      L("Now careful, a lot of students see r and s in z, and think they're factors of z. They're not. They're only "
        "exponents, they count how many times p and q appear. The primes r and s themselves aren't inside z at all.",
        pt('stem', 'see r and s in z'), show(u2, "They're only exponents")),
      L("And remember the check. A power of a prime divides z only if z has that prime at least as many times.", show(u3, 'remember the check')),
      L("Choice number one, r. r isn't a factor of z, so it's out. Choice number four, s to the power of q. There's no s in "
        "z at all. Out.", mk('cross', 'choice 1', "so it's out"), pt('u2', 'no s in z'), mk('cross', 'choice 4', 'at all. Out')),
      L("Choice number three, q to the power of s. It needs s copies of q. z has q only r times, and r is smaller than s. "
        "Not enough q's, out.", show(u4, 'It needs s copies'), mk('cross', 'choice 3', "Not enough q's")),
      L("Three are out, so in the exam you'd circle choice number two. Here, let's see why it works. p to the power of r "
        "needs r copies of p. z has s of them, and r is smaller than s, so there are enough. q to the power of q needs q "
        "copies of q. z has r of them, and q is smaller than r, so enough again. So choice number two is our answer.",
        show(u5, 'p to the power of r'), mk('tick', 'choice 2', 'So choice number two is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's do the same with numbers, by plugging them in. When the primes are letters, plug in the smallest primes, in the "
        "right order. Why the smallest? Any primes in that order fit the givens, and small ones are the easiest to work "
        "with. So p is two, q is three, r is five, and s is seven.", pt('stem', 'in the right order'), show(v1, 'So p is two')),
      L("Then z is two to the power of seven, times three to the power of five. Seven twos and five threes.", show(v2, 'Then z is two')),
      L("Choice number one, r is five. z is built only from twos and threes, so five doesn't divide it. Out.", mk('cross', 'choice 1', 'Out.')),
      L("Choice number two, p to the power of r times q to the power of q, is two to the power of five, times three cubed. "
        "Five twos, and z has seven. Three threes, and z has five. It fits.", show(v3, 'Choice number two, p'), pt('v2', 'z has seven')),
      L("Can I circle it already? No. I'm plugging in numbers, so it might work only for these numbers. I have to knock out "
        "the other two first.", show(v5, 'knock out')),
      L("Choice number three, q to the power of s, is three to the power of seven. Seven threes, and z has only five. Out. "
        "Choice number four, s to the power of q, is seven cubed, and there's no seven in z at all. Out. So choice number "
        "two. [pause] Okay. I'll see you in the next question.", show(v4, 'Choice number three, q'), mk('cross', 'choice 3', 'only five. Out'),
        mk('cross', 'choice 4', 'at all. Out'), mk('tick', 'choice 2', 'So choice number two'))),
])

# ------------------------------------------------------------------------------------------------ q-395 (Q18)
# NEW: a prime in a product sits whole in one factor (why, with 42 = 2·21); 35 isn't prime, so its 5 and 7 can come from
# different numbers; squaring adds no new primes; "never true" is also "not necessarily true"; one failing example is
# enough for "not necessarily".  REMINDER: must / could / not necessarily (topic 1).
r1 = I('r1', '$35=5\\cdot7$: $\\ x$ has a $5$ and a $7$', size=32, hand='35 = 5·7 :   x has a 5 and a 7')
r2 = I('r2', 'A prime in a product: one factor holds it whole', size=26, col=1)
r3 = I('r3', '$42=2\\cdot21$: $\\ 7$ is inside $21$', size=28, col=1, hand='42 = 2·21 :   7 is inside 21')
r4 = I('r4', '$5\\cdot7\\cdot1=35$: $\\ $none is $35$', size=28, col=1, hand='5·7·1 = 35 :   none is 35')
r5 = I('r5', '(4) someone brings the $7$ ✓', size=30, hand='(4)  someone brings the 7   ✓')
r6 = I('r6', '(1) $35,\\ 1,\\ 2$: $\\ $possible ✓', size=30, hand='(1)  35,  1,  2 :   possible   ✓')
r7 = I('r7', '(3) $a$ brings the $5$: $\\ 10^2=100$ ✓', size=30, hand='(3)  a brings the 5 :   10^2 = 100   ✓')
r8 = I('r8', '$70=2\\cdot5\\cdot7$ $\\ \\to\\ 70^2=2^2\\cdot5^2\\cdot7^2$', size=32, hand='70 = 2·5·7   →   70^2 = 2^2·5^2·7^2')
r9 = I('r9', 'Same primes: never greater', size=28, col=1)
r10 = I('r10', 'Never true is also not necessarily true', size=26, col=1)
w1 = I('w1', '$a=5,\\ b=7,\\ c=1$: $\\ x=35$', hand='a = 5,   b = 7,   c = 1 :    x = 35')
w2 = I('w2', '(2) $35^2=5^2\\cdot7^2$: $\\ 2$ primes, not more ✗', size=30, hand='(2)  35^2 = 5^2·7^2 :   2 primes,  not more   ✗')
w3 = I('w3', '(4) $b=7$ ✓ $\\quad$ (3) $a^2=25$ ✓', size=30, hand='(4)  b = 7  ✓       (3)  a^2 = 25  ✓')
video('solve-q-395', 'solution', qid='q-395', slides=[
    S('Method 1 · Test each statement',
      L("a, b and c are different positive integers. Given: x, which is a times b times c, is divisible by thirty-five "
        "without remainder. Which of the following statements is not necessarily true?",
        pt('stem', 'a, b and c', 'hl', 9.0), voice='calm', pause=0.5),
      L("A hard one, and it's usually one of the last questions in the section. Read the wording carefully. They want the "
        "statement that is not necessarily true, so the statements that must be true are out. [short pause] We'll solve "
        "it two ways, understanding each statement, and then plugging in numbers.", pt('stem', 'not necessarily true')),
      L("[short pause] First, the given. Thirty-five is five times seven. So x divides by thirty-five "
        "means x contains the prime five and the prime seven.", show(r1, 'Thirty-five is five times seven')),
      L("And x is a times b times c. Here's the key rule. A prime can't be split between factors, one of them holds it "
        "whole. Why? A prime can't be broken into smaller pieces, so the seven has to sit inside one of the numbers. For "
        "example, forty-two is two times twenty-one, and its seven sits whole inside the twenty-one.",
        show(r2, "A prime can't be split"), show(r3, 'For example, forty-two')),
      L("But thirty-five isn't a prime, so its five and its seven may come from different numbers. Five times seven times "
        "one is thirty-five, and none of the three is divisible by thirty-five.", show(r4, 'Five times seven times'))),
    S('Method 1 · Test each statement',
      L("Now the statements. Choice number four says at least one of them is divisible by seven. Someone had to bring the "
        "seven, so it's always true. Out.", show(r5, 'Someone had to bring'), mk('cross', 'choice 4', "it's always true. Out")),
      L("Choice number one says it's possible that exactly one of them is divisible by thirty-five. Possible needs just one "
        "example. Thirty-five, one and two. They're different, thirty-five times one times two is seventy, and seventy "
        "divides by thirty-five. And only the thirty-five divides by thirty-five. So it's possible, true, and out.",
        show(r6, 'Thirty-five, one and two'), mk('cross', 'choice 1', 'true, and out')),
      L("Choice number three. If b and c aren't divisible by five, who brought the five? a must have. So a is five times "
        "something. Square a, and the five appears twice, so a squared is divisible by twenty-five. For example, a is ten, b "
        "is seven, c is one. Ten squared is a hundred, and a hundred divides by twenty-five. Always true, out.",
        pt('choice 3', 'who brought the five'), show(r7, 'Square a'), mk('cross', 'choice 3', 'Always true, out')),
      L("Three statements are out, so in the exam you'd circle choice number two and move on. Here, let's learn from it. "
        "Look at the word different, the number of different prime divisors.", pt('choice 2', 'Look at the word different')),
      L("Squaring x just makes every prime appear twice as often. No new prime shows up. For example, x is seventy, two "
        "times five times seven. Seventy squared is two squared times five squared times seven squared. The same three "
        "primes. So the count stays the same, it's never greater.", show(r8, 'For example, x is seventy'), show(r9, "it's never greater")),
      L("And careful with the wording. Choice number two is never true. And never true is also not necessarily true, "
        "because it certainly doesn't have to be true. So choice number two is our answer.",
        show(r10, 'never true is also'), mk('tick', 'choice 2', 'So choice number two is our answer')),
      sb='Method 1 · Test each statement'),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now let's try plugging in numbers. A statement that's not necessarily true fails for at least one "
        "example. So I pick numbers that fit, and look for a statement that fails. Five, seven and one. They're different, "
        "and their product is thirty-five.", show(w1, 'Five, seven and one')),
      L("Choice number two. x is thirty-five, with two different primes, five and seven. x squared is five squared times "
        "seven squared, still just five and seven. Two is not greater than two. It fails, so choice number two is not "
        "necessarily true.", show(w2, 'x squared is five squared'), mk('tick', 'choice 2', 'It fails')),
      L("And the others? Choice number four, b is seven, true. Choice number three, b and c aren't divisible by five, and a "
        "is five, so a squared is twenty-five, true. And choice number one is about what's possible, and thirty-five, one "
        "and two show that it is. So only choice number two fails. [pause] Okay. I'll see you in the next question.",
        show(w3, 'b is seven, true'), mk('cross', 'choice 4', 'b is seven'), mk('cross', 'choice 3', 'is twenty-five, true'),
        mk('cross', 'choice 1', 'show that it is'), mk('tick', 'choice 2', 'only choice number two fails'))),
])

# ------------------------------------------------------------------------------------------------ q-397 (Q19)
# NEW: bounding the prime by squares (14^2 = 196 < 200 < 225 = 15^2); counting primes up to 14; the trap 4 (one-digit
# primes only); 16 = 4^2 has five divisors (only squares of primes count).  REMINDER: exactly three divisors = a prime
# squared (q-402); trial and error to find a pattern (topic 21).
v1 = I('v1', 'Exactly $3$ divisors: a prime squared', size=28, col=1)
v2 = I('v2', '$14^2=196<200<225=15^2$', hand='14^2 = 196 < 200 < 225 = 15^2')
v3 = I('v3', '$2,\\ 3,\\ 5,\\ 7,\\ 11,\\ 13$ $\\ \\to\\ \\hl{s}{6}$ primes', size=32, hand='2,  3,  5,  7,  11,  13   →   \\hl{s}{6}  primes')
v4 = I('v4', '$4,\\ 9,\\ 25,\\ 49,\\ 121,\\ 169$', size=32, hand='4,  9,  25,  49,  121,  169')
v5 = I('v5', 'Only one-digit primes? $\\ 4$ ✗', size=28, col=1, hand='Only one-digit primes ?   4   ✗')
t1 = I('t1', '$4$: $\\ 1,2,4$ ✓ $\\quad 6$: $\\ 1,2,3,6\\quad 8$: $\\ 1,2,4,8$', size=30, hand='4 :  1, 2, 4  ✓      6 :  1, 2, 3, 6      8 :  1, 2, 4, 8')
t2 = I('t2', '$9$: $\\ 1,3,9$ ✓', size=30, hand='9 :  1, 3, 9   ✓')
t3 = I('t3', '$16$: $\\ 1,2,4,8,16$ $\\ \\to\\ 5$ ✗', size=30, hand='16 :  1, 2, 4, 8, 16   →   5   ✗')
t4 = I('t4', '$25,\\ 49,\\ 121,\\ 169$ $\\quad 17^2=289$ ✗', size=30, hand='25,  49,  121,  169       17^2 = 289   ✗')
t5 = I('t5', 'Squares of primes', size=28, col=1)
video('solve-q-397', 'solution', qid='q-397', slides=[
    S('Method 1 · The rule',
      L("a is an integer. Given: a is bigger than one and smaller than two hundred, and a has exactly three different "
        "divisors, including one and a. How many different values can a have?", pt('stem', 'a is an integer', 'hl', 9.0), voice='calm', pause=0.5),
      L("The whole question hides in one given, exactly three divisors. And we've seen this one before. [short pause] We'll "
        "solve it two ways, with the rule, and then with trial and error to find the pattern.", pt('stem', 'exactly three divisors')),
      L("[short pause] Remember, divisors come in pairs, and exactly three divisors means a prime squared. "
        "One, the prime, and the prime squared, like nine, with one, three and nine.", show(v1, 'means a prime squared')),
      L("So a is a prime squared, and a is less than two hundred. How big can the prime be? Fourteen squared is a hundred "
        "ninety-six, still below two hundred. Fifteen squared is two hundred twenty-five, too big. So the prime is fourteen "
        "or less.", show(v2, 'Fourteen squared is')),
      L("The primes up to fourteen are two, three, five, seven, eleven and thirteen. Six of them. Their squares are four, "
        "nine, twenty-five, forty-nine, a hundred twenty-one and a hundred sixty-nine, all below two hundred.",
        show(v3, 'The primes up to fourteen'), mk('circle', 'v3: s', 'Six of them'), show(v4, 'Their squares are')),
      L("So a has six values, and choice number three is our answer.", mk('tick', 'choice 3', 'choice number three is our answer')),
      L("Now careful, a lot of students stop at the one-digit primes, two, three, five and seven, and answer four, choice "
        "number four. But eleven squared and thirteen squared are still below two hundred.",
        show(v5, 'stop at the one-digit primes'), mk('cross', 'choice 4', 'choice number four'))),
    S('Method 2 · Trial and error',
      L("[pause] Another way is trial and error. Don't remember the rule? Run through the numbers, count the divisors, "
        "and look for the pattern. Two and three are prime, two divisors each. Four has one, two and four. Three divisors, "
        "the first one that fits. Five is prime. Six has one, two, three and six, that's four. Seven is prime. Eight has "
        "one, two, four and eight, four again.", show(t1, 'Four has one, two and four')),
      L("Nine has one, three and nine. It fits.", show(t2, 'Nine has one')),
      L("Stop and look for the pattern. Four is two squared, and nine is three squared, squares of primes. But careful, not "
        "every square. Sixteen is four squared, and it has one, two, four, eight and sixteen, five divisors, because four "
        "isn't a prime.", show(t5, 'squares of primes'), show(t3, 'Sixteen is four squared')),
      L("So the next ones are five squared, twenty-five, seven squared, forty-nine, eleven squared, a hundred twenty-one, "
        "and thirteen squared, a hundred sixty-nine. Seventeen squared is two hundred eighty-nine, too big. Six values, "
        "choice number three. [pause] Okay. I'll see you in the next question.", show(t4, 'five squared, twenty-five'),
        mk('tick', 'choice 3', 'Six values'))),
])

# ------------------------------------------------------------------------------------------------ r26-t14-summary
# REMINDERS only, said the way they were taught.
y1s = I('y1s', 'Prime: exactly two divisors, $1$ and itself', size=40)
y2s = I('y2s', '$0$, $1$, negatives: not prime $\\qquad 2$: the only even prime', size=36)
y3s = I('y3s', '$2,\\ 3,\\ 5,\\ 7,\\ 11,\\ 13,\\ 17,\\ 19,\\ 23,\\ 29,\\ 31,\\ 37$ $\\ \\cdot\\ 97$', size=36)
o1s = I('o1s', 'Two primes, odd sum or difference: one of them is $2$', size=36)
o2s = I('o2s', '$73=2+71$', size=44)
p1s = I('p1s', 'Is $n$ prime? Try the primes up to $\\sqrt{n}$', size=40)
p2s = I('p2s', '$69=3\\cdot23\\ (6+9=15)\\qquad 77=7\\cdot11\\qquad 161=7\\cdot23$', size=36)
f1s = I('f1s', '$44=2\\cdot2\\cdot11$: $\\ 2,\\ 4,\\ 11,\\ 22,\\ 44$', size=40)
f2s = I('f2s', 'A divisor: its primes, enough times. Unpack $6$, $10^2$ first', size=34)
f3s = I('f3s', 'Break apart $\\cdot$ build $\\cdot$ which prime is missing?', size=36)
g1s = I('g1s', 'GCD: shared primes, lower power $\\qquad$ LCM: every prime, higher power', size=32)
g2s = I('g2s', '$48=2^4\\cdot3,\\ \\ 60=2^2\\cdot3\\cdot5$: $\\ $GCD $12$, LCM $240$', size=34)
g3s = I('g3s', 'GCD $\\cdot$ LCM $=a\\cdot b$', size=40)
d1s = I('d1s', '$2^4\\cdot3$: $\\ (4+1)(1+1)=10$ divisors', size=40)
d2s = I('d2s', 'Odd number of divisors: a perfect square $\\qquad$ exactly $3$: a prime squared', size=32)
s1s = I('s1s', 'Perfect square: every exponent even', size=40)
s2s = I('s2s', '$20k$ a square: $\\ 20=2^2\\cdot5$, $\\ k=5$, $\\ 100=10^2$', size=38)
s3s = I('s3s', '$2^a\\cdot3^b=144=2^4\\cdot3^2$: $\\ a=4,\\ b=2$', size=38)
m1s = I('m1s', 'A prime in a product: one factor holds it whole', size=38)
m2s = I('m2s', 'Letters as primes: plug in $2,\\ 3,\\ 5,\\ 7$ in order, knock out three', size=34)
z1s = I('z1s', 'Did I break every number into primes?', size=38)
z2s = I('z2s', 'Really prime? Up to the root, and $7$?', size=38)
z3s = I('z3s', 'Odd sum or difference? One prime is $2$', size=38)
z4s = I('z4s', 'GCD or LCM: lower or higher power?', size=38)
video('r26-t14-summary', 'lesson', slides=[
    S('Prime Numbers — Summary',
      L("Before you practice, here's a quick summary of primes and factors. Everything important, in a few minutes.")),
    S('What a prime is',
      L("A prime has exactly two divisors, one and itself. One is not prime, and neither are zero and the negative numbers. "
        "Two is prime, and it's the only even prime.", show(y1s, 'exactly two divisors'), show(y2s, 'One is not prime')),
      L("Know the primes up to forty by heart. Two, three, five, seven, eleven, thirteen, seventeen, nineteen, twenty-three, "
        "twenty-nine, thirty-one and thirty-seven. And ninety-seven, the largest two-digit prime.", show(y3s, 'Know the primes'))),
    S('Odd sum or difference',
      L("All the other primes are odd. Odd plus odd is even, and odd minus odd is even too. So if two primes give an odd sum "
        "or an odd difference, one of them is two. Seventy-three as a sum of two primes? Two plus seventy-one.",
        show(o1s, 'So if two primes'), show(o2s, 'Seventy-three'))),
    S('Is it prime?',
      L("To test a number, divide it by the primes up to its square root, and no further. Watch out for the fakes. For "
        "three, add the digits, like sixty-nine, six plus nine is fifteen. And never forget to try seven, like seventy-seven, "
        "which is seven times eleven.", show(p1s, 'To test a number'), show(p2s, 'Watch out for the fakes'))),
    S('Break it down',
      L("Every number that isn't prime breaks into primes, in only one way. And it's divisible by every combination of its "
        "prime factors. Forty-four is two times two times eleven, so it divides by two, four, eleven, twenty-two and "
        "forty-four.", show(f1s, 'Forty-four is')),
      L("Is a number a divisor? Break it into primes too, and check that every prime is there, enough times. Unpack pieces "
        "like six or ten squared first.", show(f2s, 'Is a number a divisor')),
      L("Most questions just break a number apart, or build numbers from pieces, and look for the missing prime.", show(f3s, 'break a number apart'))),
    S('GCD and LCM',
      L("The greatest common divisor takes each shared prime at its lower power. The greatest number that's guaranteed to "
        "divide, the LCM, takes every prime at its higher power.", show(g1s, 'The greatest common divisor')),
      L("Forty-eight is two to the power of four times three, and sixty is two squared times three times five. The GCD is "
        "two squared times three, twelve. The LCM takes two to the power of four, three and five, and sixteen times fifteen is two hundred forty.",
        show(g2s, 'Forty-eight is')),
      L("The trap is just multiplying the two numbers, which counts a shared prime twice. And the GCD times the LCM is the "
        "two numbers multiplied.", show(g3s, 'the GCD times the LCM'))),
    S('Counting divisors',
      L("The number of divisors? Add one to each exponent, and multiply. Two to the power of four times three has five times "
        "two, ten divisors.", show(d1s, 'Add one to each exponent')),
      L("Divisors come in pairs, so only a perfect square has an odd number of them. And exactly three divisors means a "
        "prime squared, like four or a hundred twenty-one.", show(d2s, 'Divisors come in pairs'))),
    S('Squares and equations',
      L("In a perfect square, every exponent is even. Twenty k a square? Twenty is two squared times five, so it needs one "
        "more five. k is five, and twenty times five is a hundred, ten squared.", show(s1s, 'every exponent is even'), show(s2s, 'Twenty k')),
      L("And an equation in primes? Break the number, then match the exponents. Two to the power of a, times three to the "
        "power of b, is a hundred forty-four. That's sixteen times nine, two to the power of four times three squared, so a "
        "is four and b is two.", show(s3s, 'an equation in primes'))),
    S('A prime in a product',
      L("A prime can't be split between factors, one of them holds it whole.", show(m1s, "A prime can't be split")),
      L("And when the primes are letters, plug in the smallest primes in the right order, and knock out three choices before "
        "you mark one.", show(m2s, 'when the primes are letters'))),
    S('Before you practice',
      L("Before each question, ask yourself. Did I break every number into primes? Is it really prime, did I try up to the "
        "root, and seven? An odd sum or difference, is one of them two? GCD or LCM, lower power or higher power?",
        show(z1s, 'Did I break'), show(z2s, 'Is it really prime'), show(z3s, 'An odd sum'), show(z4s, 'GCD or LCM')),
      L("The common traps are calling one a prime, forgetting two, and multiplying instead of taking the LCM. [pause] That's "
        "it. Now go practice, and I'll see you in the next video.", mk('underline', 'z3s', 'forgetting two'), mk('underline', 'z4s', 'multiplying instead'))),
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


for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _write_gap(_v)


if __name__ == '__main__':
    _bad = 0
    for _v in sys.argv[1:] or ORDER:
        _p = check(_v)
        if _p: print('PROBLEMS', _v, _p); _bad += 1
        print('script written:', write_json(_v), stats(_v))
    for x in WRITE_LATE: print('mark dropped (its item is still being written):', x)
    sys.exit(1 if _bad else 0)
