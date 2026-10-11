"""Topic 13 (Absolute Value) - the AI-narration redo, the model for the ~800 AI math videos (2026-10-11).

ONE spec per video drives all three sides, so they cannot drift apart:
  - the AI script   ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t13.py [vid ...] writes it: say / voice / pause /
                    at - the at phrases come from the cues below);
  - the visual plan VIS[vid] in the _ai_visual.py format ({spoken line N: [cue, ...]}; _ai_visual.py merges it into its
                    own VIS, so `python3 math_patches/_ai_visual.py` and apply() work for these videos too);
  - the studio video: t13.py ai_redo_t13() (time-gated) rebuilds the slides from slides(vid) - the spoken lines are the
                    AI lines (tags dropped), one studio line per AI line - and then _ai_visual.apply() adds the cues and
                    click items around them.

Every video: the stem read aloud (calm voice), first reaction, all the useful methods (standard first), traps at the
step, the answer as "value, number N", a verdict + a reusable takeaway, "Okay. I'll see you in the next question."
Rules: real_exam/TEACHING_STYLE_GUIDE.md R1-R29 (R29: ideas taught earlier in the study plan / earlier in topic 13 get a
SHORT reminder, new ideas the full rule-examples-why-trap treatment), NITZAN_RHYTHM_DELIVERY.md P1-P13.

Spec DSL
  video(vid, kind, slides, qid=None)        kind 'solution' (every slide is a question slide with the question pre-loaded)
                                            or 'lesson' (slide 1 is the title slide, the rest concept slides)
  S(title, *lines, sb=None)                 a slide; sb = its sidebar label (default: the title)
  L(say, *cues, voice=None, pause=None)     one spoken line (= one AI line); [short pause] / [pause] tags allowed
  I(name, tex, size=36, col=0, hand=None)   a board item: col 0 = left column (stacks under the question), col 1 =
                                            right column; hand = its hand-written text (the item becomes a 'write' cue -
                                            it is hand-written only if the handwriting style is switched on later)
  NL(name, svg, w=560, col=0)               a number-line figure (_shaded_nl.fig)
  cues: show(item, phrase) · pt(target, phrase, style=None, dur=None) · mk(kind, target, phrase)
        target = 'stem' | 'choice N' | '<item name>' | '<item name>: <\\hl part>'   (names are resolved to 'item K')
        phrase = a phrase of this line ("<phrase" = of the previous line)
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q

_s = importlib.util.spec_from_file_location('_shaded_nl_t13ai', os.path.join(HERE, '_shaded_nl.py'))
SNL = importlib.util.module_from_spec(_s); _s.loader.exec_module(SNL)

VIDEOS = {}
ORDER = []          # topic-13 flow order of the AI videos (absolute-value = the camera lesson, not here)
TAG = re.compile(r'\[(short pause|pause|long pause)\]')


# ------------------------------------------------------------------------------------------------------------- DSL
def I(name, tex, size=36, col=0, hand=None):
    return {'_name': name, '_col': col, '_hand': hand, 'k': 't', 't': tex, 'size': size, 'gap': 16}


def NL(name, svg, w=560, col=0):
    vb = [float(t) for t in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    return {'_name': name, '_col': col, '_hand': None, 'k': 'vis', 'v': {'type': 'geometry', 'svg': svg}, 'w': w,
            'h': int(round(w * vb[3] / vb[2])), 'gap': 16}


def DIST(name, lo, hi, c, r, base=(0,), band=None, w=1060):
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
        closed = band != 'open'
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
    if band:
        a, b = X(c - r), X(c + r)
        out['band'] = svg('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (a, Y_ - 7, b - a, BAND, TEAL)
                          + dot(c - r) + dot(c + r) + '<circle cx="%.1f" cy="%d" r="6" fill="%s"/>' % (X(c), Y_, INK),
                          'between %s and %s' % (fmt(c - r), fmt(c + r)))
    items = {}
    for k, sv in out.items():
        it = NL('%s_%s' % (name, k), sv, w=w)
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
        out = []
        for it in items:
            d = {k: v for k, v in it.items() if not k.startswith('_')}
            if it['_col'] == 1 and not solo:
                d.update(x=1010, w=540, y=100 if V['kind'] == 'solution' else 78)
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
    caps = [c for c in caps if c not in ('I', 'OK')]
    if len(caps) > 1: probs.append('CAPS words: %s (at most one)' % caps)
    bangs = re.findall(r'[A-Za-z][^.?!]*!', re.sub(r'\b(No|Yes|Exactly)!', '', allt))
    if len(bangs) > 1: probs.append('%d "!" sentences (at most one)' % len(bangs))
    if re.search(r'\bchoice (one|two|three|four)\b', allt, re.I): probs.append('says "choice N" - say "number N"')
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
            'style': "her real voice, topic-13 AI redo (2026-10-11): math_patches/_ai_vis_t13.py is the source - edit there "
                     "and re-run it. Rules: real_exam/TEACHING_STYLE_GUIDE.md R1-R29 + NITZAN_RHYTHM_DELIVERY.md P1-P13. "
                     "Segmented (mix 3): calm preset on the question reading and the plain calculation lines.",
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


# =================================================================================================================
# THE SCRIPTS (topic-13 flow order). See the review file ~/Downloads/Topic-13-AI-scripts-review.md for NEW / REMINDER.
# =================================================================================================================

# ------------------------------------------------------------------------------------------------ q-358 (Q1)
# NEW: "signs only, no sizes", the tie-breaker plug (why: necessarily = for every pair); plugging in finds the signs by trying (y = 3 fails, x = -8 fails) -
# R30, each method stands on its own.  REMINDER: product sign (topic 1), y < |y| clue (lesson).
c1 = I('c1', '$\\hl{xy}{x\\cdot y<0}$: opposite signs', hand='\\hl{xy}{x·y < 0} : opposite signs')
c2 = I('c2', '$(+)\\cdot(-)=(-)$', size=32, col=1, hand='(+)·(−) = (−)')
c3 = I('c3', '$\\hl{y}{y<|y|}$: $y$ is negative', hand='\\hl{y}{y < |y|} : y is negative')
c4 = I('c4', 'So $\\hl{x}{x>0}$', hand='So    \\hl{x}{x > 0}')
c5 = I('c5', 'Signs only, no sizes', size=32, col=1)
c6 = I('c6', '$|x|=x$ when $x\\ge0$', size=32, col=1, hand='|x| = x  when  x ≥ 0')
t1 = I('t1', '$y=3$: $\\ 3<|3|$? ✗', size=30, hand='y = 3 :   3 < |3| ?  ✗')
t2 = I('t2', '$y=-3$: $\\ -3<3$ ✓', size=30, hand='y = −3 :   −3 < 3  ✓')
t3 = I('t3', '$x=-8$: $\\ (-3)(-8)=24>0$ ✗', size=30, hand='x = −8 :   (−3)(−8) = 24 > 0  ✗')
k1 = I('k1', 'Negative product: opposite signs', size=28, col=1)
k2 = I('k2', 'Smaller than its absolute value: negative', size=28, col=1)
p1 = I('p1', '$y=-3,\\ \\ x=8$: $\\ -24<0$ ✓', size=30, hand='y = −3,  x = 8 :   −24 < 0  ✓')
p2 = I('p2', '$\\left|\\frac{-3}{8}\\right|=\\frac{3}{8}<1$', size=32, hand='|{−3/8}| = {3/8} < 1')
p3 = I('p3', '$y=-6,\\ \\ x=2$', col=1, hand='y = −6,  x = 2')
p4 = I('p4', '$\\left|\\frac{-6}{2}\\right|=\\hl{three}{3}$', size=32, col=1, hand='|{−6/2}|  =   \\hl{three}{3}')
video('solve-q-358', 'solution', qid='q-358', slides=[
    S('Method 1 · Understanding',
      L("Given: x times y, is smaller than zero, and y is smaller than the absolute value of y. Which of the following is "
        "necessarily true?", pt('stem', 'Given', 'hl', 9.0), voice='calm', pause=0.5),
      L("So here we have no numbers at all, just signs. And look at the choices, some of them talk about signs and some about "
        "sizes. [short pause] We'll solve this two ways, first by understanding the givens, and then by plugging in numbers.",
        pt('stem', 'no numbers at all'), pt('choice 4', 'look at the choices'), pt('choice 1', 'about signs'), pt('choice 2', 'some about'),
        pt('choice 3', 'sizes.'), pt('stem', 'understanding the givens', 'hl', 3.0)),
      L("Let's take the givens one at a time. When is x times y negative? Only when they have opposite signs, one positive "
        "and one negative. Remember, plus times minus is minus. And if both were positive, or both negative, the product "
        "would be positive.",
        pt('stem', 'one at a time'), show(c1, 'Only when they have opposite signs'), pt('c1', 'one positive and one'),
        show(c2, 'plus times minus is minus'), pt('c2', 'both were positive'), pt('c1: xy', 'both negative')),
      L("But which one is the negative one? We don't know yet. So let's look at the second given.", pt('c1', 'which one')),
      L("When is a number smaller than its own absolute value? Only when it's negative. If y were positive, they'd just be "
        "equal, right? Four is equal to its absolute value. But negative four is smaller than four.",
        pt('stem', 'its own absolute value'), show(c3, 'Only when it'), pt('c3', 'If y were'),
        pt('c3: y', 'just be equal'), pt('c3: y', 'Four is equal'), pt('c3: y', 'negative four is smaller')),
      L("So y is negative, and the signs are opposite. And therefore x is the positive one.",
        pt('c3', 'So y is negative'), pt('c1', 'the signs are opposite'), show(c4, 'And therefore x'), mk('circle', 'c4: x', 'the positive one')),
      L("[short pause] Now the choices. Number one says x is negative. But we just found that x is positive, so number one "
        "is out.", pt('choice 1', 'Now the choices'), pt('c4: x', 'we just found'), mk('cross', 'choice 1', 'is out')),
      L("Now careful here, because a lot of students think the negative one is also the smaller one. But the givens only "
        "tell us signs, nothing about sizes. So we can't know which absolute value is bigger, and numbers two and three "
        "don't have to be true.",
        pt('choice 2', 'a lot of students', 'both', 3.5), show(c5, 'only tell us signs'),
        mk('underline', 'c5', 'nothing about sizes'), pt('choice 2', 'which absolute value'), pt('choice 3', 'numbers two and three')),
      L("Number four says the absolute value of x is equal to x. When is a number equal to its absolute value? When it's "
        "zero or positive. And x is positive, so this is always true. So number four is our answer.",
        pt('choice 4', 'Number four says', 'hl', 3.5), pt('choice 4', 'When is a number equal'),
        show(c6, "When it's zero"), pt('c4: x', 'And x is positive'), mk('tick', 'choice 4', 'number four is our'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Now our second method, plugging in numbers. It's a great safety net when you're not sure. I need numbers "
        "that obey both givens, and I'll find them by trying. Let's start with y, because the second given has only y in it.",
        pt('stem', 'obey both givens'), pt('stem', 'only y in it')),
      L("Why do I try a positive y first? Because it's the most natural guess, so let's see if it works. y is three. Is "
        "three smaller than the absolute value of three? No, they're equal. And zero is equal to its absolute value too. So "
        "y can't be positive, and it can't be zero.",
        show(t1, 'y is three'), mk('cross', 't1', "No, they're equal")),
      L("So let's try a negative y, negative three. Is negative three smaller than three? Yes. So negative three works, and "
        "now I know y has to be negative.", show(t2, 'a negative y'), pt('t2', 'now I know')),
      L("Now x. What does that mean for x? The first given says x times y is negative. Let's try a negative x too, negative "
        "eight. Why eight? So x and y are different numbers, and both stay away from zero and one. Negative three times "
        "negative eight is twenty-four. That's positive, so it breaks the first given.",
        pt('stem', 'The first given says'), show(t3, 'negative eight. Why'), mk('cross', 't3', "That's positive")),
      L("So I adjust, and make x positive, x is eight. Negative three times eight is negative twenty-four, and that's "
        "smaller than zero. Now both givens work, so y is negative three and x is eight.",
        show(p1, 'make x positive'), pt('p1', 'Now both givens work')),
      L("Number one, x is negative? Eight isn't negative, so it's out. Number two says the absolute value of x is smaller. "
        "The absolute value of eight is eight, and of negative three it's three. Is eight smaller than three? No, out.",
        mk('cross', 'choice 1', "so it's out"), pt('choice 2', 'Number two says'), mk('cross', 'choice 2', 'No, out'), voice='calm'),
      L("Number three, negative three over eight, in absolute value, is three eighths. That's less than one, so number three stays. And "
        "number four, the absolute value of eight is eight, so it stays too.",
        pt('choice 3', 'Number three, negative'), pt('p1', 'in absolute value'), show(p2, 'is three eighths'), pt('choice 3', 'number three stays'),
        pt('choice 4', 'And number four'), pt('p1', 'the absolute value of eight'), pt('choice 4', 'stays too'), voice='calm'),
      L("Two choices survive. Can I already circle one and move on? I can't, because a necessarily true choice has to work "
        "for every pair that fits the givens. So I need a tie-breaker, a new pair that might break one of them. Choice number three is about "
        "sizes, so this time I'll make y the bigger one in size, and keep the signs that work. y is negative six, and x is "
        "two. Negative six times two is negative twelve, so both givens still hold.",
        pt('choice 3', 'Two choices survive'), pt('choice 4', 'move on'), pt('p2', 'I need a tie-breaker'), pt('choice 3', 'the bigger one in size'), show(p3, 'y is negative six')),
      L("Negative six over two is negative three, and its absolute value is three. That's not less than one, so number three "
        "is out. And the absolute value of two is still two. Aaand it's number four, again.",
        show(p4, 'Negative six over two'), pt('p4: three', 'its absolute value is three'), mk('circle', 'p4: three', 'not less than one'), mk('cross', 'choice 3', 'number three is out'), pt('p3', 'still two'),
        mk('tick', 'choice 4', "it's number four, again"), voice=None),
      L("So which way is better? Here understanding is faster, because the signs give it all away. And the numbers are a great "
        "check. [short pause] Negative product, opposite signs. A number smaller than its absolute value, negative. "
        "[pause] Okay. I'll see you in the next question.",
        pt('p1', 'which way is better'), pt('stem', 'the signs give it all away'), pt('p3', 'a great check'),
        show(k1, 'Negative product'), show(k2, 'A number smaller'))),
])

# ------------------------------------------------------------------------------------------------ q-359 (Q2)
# NEW: "could be" with two answers and one offered; the -2 trap; the number-line method in full (|a - b| = the distance
# between a and b, why, x + 7 = the distance from -7, reading the picture) - the camera lesson only names it in one line.
# REMINDER: two cases.
a0 = I('a0', 'Inside $=9$ $\;$ or $\;$ inside $=-9$', size=32, hand='inside = 9   or   inside = −9')
a1 = I('a1', '$x+7=9$, so $x=\\hl{two}{2}$', hand='x+7 = 9,  so  x  =   \\hl{two}{2}')
a2 = I('a2', '$x+7=-9$, so $x=\\hl{m16}{-16}$', hand='x+7 = −9,  so  x  =    \\hl{m16}{−16}')
n1 = DIST('n1', -18, 4, -7, 9)
b1 = I('b1', '$|16+7|=23$ $\\quad |-2+7|=5$', size=32, col=1, hand='|16+7| = 23    |−2+7| = 5')
m0 = I('m0', '$\\hl{a}{\\text{Two cases}}\\ \\cdot\\ \\hl{b}{\\text{number line}}\\ \\cdot\\ \\hl{c}{\\text{plugging in}}$', size=28, col=1)
r9 = I('r9', '$|9|=9,\\ \\ |-9|=9$', size=32, col=1, hand='|9| = 9,   |−9| = 9')
d9 = I('d9', '$|5-2|=3$: from $2$ to $5$ is $3$ steps', size=30, hand='|5−2| = 3 :  from 2 to 5 is 3 steps')
d0 = I('d0', '$x+7=x-(-7)$', size=32, hand='x+7 = x − (−7)')
w1 = I('w1', 'Two cases: the standard way', size=30)
w2 = I('w2', 'Numbers in the choices: plug in', size=30)
w3 = I('w3', 'Bars $=$ number: two cases, two answers', size=30)
b2 = I('b2', '$|-16+7|=|-9|=\\hl{nine}{9}$', size=32, col=1, hand='|−16+7| = |−9|  =   \\hl{nine}{9}')
video('solve-q-359', 'solution', qid='q-359', slides=[
    S('Method 1 · Two cases',
      L("Given: x plus seven, in absolute value, is equal to nine. Which of the following could be the value of x?",
        pt('stem', 'Given', 'hl', 8.0), voice='calm', pause=0.5),
      L("So we have an equation with an absolute value, and all the choices are numbers. We'll solve it three ways, two "
        "cases, the number line, and plugging in the answers.", pt('stem', 'an equation with'), pt('choice 1', 'all the choices'),
        pt('choice 4', 'are numbers'), show(m0, 'three ways'), pt('m0: a', 'two cases, the'), pt('m0: b', 'the number line'),
        pt('m0: c', 'plugging in the answers')),
      L("[short pause] Our first method, two cases. Remember, which numbers have an absolute value of nine? Nine, and "
        "negative nine. So the inside, x plus seven, is nine, or it's negative nine.",
        pt('stem', 'Our first method'), show(r9, 'Nine, and negative nine'), show(a0, 'So the inside'),
        pt('stem', 'x plus seven, is nine')),
      L("First case, x plus seven is nine. To get x alone, I take seven off both sides, and x is two.", show(a1, 'First case'), pt('a1', 'take seven off'),
        mk('circle', 'a1: two', 'x is two'), voice='calm'),
      L("Second case, x plus seven is negative nine. Take seven off again, and x is negative sixteen.",
        show(a2, 'Second case'), pt('a2', 'Take seven off again'), mk('circle', 'a2: m16', 'x is negative sixteen'), voice='calm'),
      L("[short pause] Now careful with the choices. Is two there? No. But negative two is there, and that's the trap. It "
        "looks like our two, but it's a different number.",
        pt('a1: two', 'Is two there'), pt('choice 2', 'negative two is there'), mk('cross', 'choice 2', "that's the trap")),
      L("Negative sixteen is there, it's number three. And look at the wording, could be. Two values work, two and negative "
        "sixteen, but they only offer one of them. So negative sixteen, number three is our answer.",
        pt('a2: m16', 'Negative sixteen is there'), pt('choice 3', "it's number three"), pt('stem', 'could be'),
        pt('a1: two', 'Two values work'), pt('a2: m16', 'and negative sixteen'), pt('choice 3', 'only offer one'), mk('tick', 'choice 3', 'number three is our answer'))),
    S('Method 2 · Number line',
      L("[pause] Our second method, the number line. What are we doing here? We read the bars as a distance. Remember, the "
        "absolute value of a number is its distance from zero. And the bars around a difference give the distance between "
        "two numbers. Five minus two is three, and from two to five is exactly three steps. Why? Five minus two tells me how "
        "far five is from two, and the sign only says which way. The bars drop the sign, so what's left is the distance. "
        "Now, x plus seven is x minus negative seven, because taking away negative seven is the same as adding seven. So "
        "x plus seven, in bars, is the distance between x and negative seven. And it's equal to nine, so x is exactly nine "
        "steps away from negative seven.",
        pt('stem', 'What are we doing here'), show(d9, 'Five minus two is three'), pt('d9', 'The bars drop the sign'),
        show(d0, 'x plus seven is x minus'), show(n1['line'], 'the distance between x'), pt('stem', 'exactly nine')),
      L("So how do I read the picture? I start at negative seven, and I walk nine steps each way. Nine steps to the right, "
        "negative seven plus nine is two. Nine steps to the left, negative seven minus nine is negative sixteen. Those are "
        "the only two points that are exactly nine steps away. Two isn't in the choices, but negative sixteen is, choice "
        "number three.", pt('n1_line', 'I start at negative seven'), show(n1['right'], 'Nine steps to the right'),
        mk('circle', 'fig: 2', 'plus nine is two'), show(n1['left'], 'Nine steps to the left'),
        mk('circle', 'fig: −16', 'is negative sixteen'), pt('choice 3', 'negative sixteen is,'), mk('tick', 'choice 3', 'is, choice number')),
      sb='Method 2 · Number line'),
    S('Method 3 · Plugging in the answers',
      L("[pause] And our third method, plugging in the answers. The choices are numbers, so let's just try them. Sixteen "
        "plus seven is twenty-three, and twenty-three isn't nine, so no. Negative two plus seven is five, and five "
        "isn't nine, so no again.",
        pt('choice 1', 'Sixteen'), show(b1, 'twenty-three'), mk('cross', 'choice 1', "twenty-three isn't nine"),
        pt('choice 2', 'Negative two plus seven'), mk('cross', 'choice 2', 'so no again'), voice=['base']),
      L("Negative sixteen plus seven is negative nine, and its absolute value is nine. It works. In the exam you'd circle it "
        "and move on.", show(b2, 'Negative sixteen plus seven'), mk('circle', 'b2: nine', 'absolute value is nine'),
        pt('choice 3', 'It works'), mk('tick', 'choice 3', 'circle it')),
      L("So which way is better? The two cases are the standard way, and you'll need them in the harder questions. But when "
        "the choices are numbers, plugging in is just as fast. Bars equal to a number? Two cases, two answers. "
        "[pause] Okay. I'll see you in the next question.",
        show(w1, 'The two cases are'), pt('w1', "you'll need them"), show(w2, 'plugging in is just as fast'), show(w3, 'Bars equal to'), mk('underline', 'w3', 'two answers'))),
])

# ------------------------------------------------------------------------------------------------ q-360 (Q3)
# REMINDER: small side = closed range (lesson), acting on all three parts (topic 12), distance picture.
r0 = I('r0', 'Small side: closed range', size=32, col=1)
r1 = I('r1', '$-7<\\text{inside}<7$', size=32, col=1, hand='−7 < inside < 7')
v1 = I('v1', 'Numbers in the choices: plug in', size=30)
v2 = I('v2', 'Closed range: make it automatic', size=30)
v3 = I('v3', '$|\\text{in}|<7$: $\\ -7<\\text{in}<7$', size=32, hand='|in| < 7 :   −7 < in < 7')
c1 = I('c1', '$-7<x+3<7$', hand='−7 < x+3 < 7')
c2 = I('c2', '$\\hl{lo}{-10}<x<\\hl{hi}{4}$', hand='\\hl{lo}{−10} < x < \\hl{hi}{4}')
n2 = DIST('n2', -13, 7, -3, 7, band='open')
d1 = I('d1', '$|5+3|=8$ $\\quad |-25+3|=22$', size=32, col=1, hand='|5+3| = 8    |−25+3| = 22')
d2 = I('d2', '$|3+3|=\\hl{six}{6}<7$', size=32, col=1, hand='|3+3|  =   \\hl{six}{6}   < 7')
video('solve-q-360', 'solution', qid='q-360', slides=[
    S('Method 1 · Closed range',
      L("Given: x plus three, in absolute value, is smaller than seven. Which of the following could be the value of x?",
        pt('stem', 'Given', 'hl', 9.0), voice='calm', pause=0.5),
      L("So now the bars are in an inequality, and they're on the small side. What did we say about the small side? It's a "
        "closed range. The inside is trapped between seven and negative seven. [short pause] We'll solve it three ways.",
        pt('stem', 'on the small side'), show(r0, "It's a closed range"), show(r1, 'trapped between')),
      L("[short pause] Our first method, the algebra. The inside is trapped, so I take the seven, and I put negative seven "
        "on the other side. So negative seven is smaller than x plus three, which is smaller than seven.",
        pt('stem', 'I take the seven'), pt('r1', 'negative seven on the other side'), show(c1, 'So negative seven is smaller'),
        pt('c1', 'which is smaller than seven')),
      L("How do I get x alone in the middle? I take three off all three parts. Negative seven minus three is negative ten, "
        "and seven minus three is four. So x is between negative ten and four.",
        pt('c1', 'all three parts'), show(c2, 'Negative seven minus three'), pt('c2: lo', 'is negative ten'),
        pt('c2: hi', 'seven minus three is four'), voice=None),
      L("Now the choices. Five and eleven are too big, they're above four. Negative twenty-five is too small, it's below "
        "negative ten. And three is inside the range. So three, number three is our answer.",
        pt('choice 1', 'Now the choices'), mk('cross', 'choice 1', 'Five and'), mk('cross', 'choice 4', 'eleven are too big'), mk('cross', 'choice 2', 'Negative twenty-five'), pt('c2: lo', 'below negative ten'),
        mk('tick', 'choice 3', 'number three is our answer'))),
    S('Method 2 · Number line',
      L("[pause] Our second method, the number line. x plus three is the distance from negative three. So x is less than "
        "seven steps away from negative three.", pt('stem', 'x plus three is the'), show(n2['line'], 'the distance from negative three'),
        pt('stem', 'less than seven steps')),
      L("Seven steps to the left, negative ten. Seven steps to the right, four. One band in the middle, from negative ten "
        "to four. Three is inside it. Five and eleven are past four, and negative twenty-five is way past negative ten, so "
        "they're outside. Three, number three.", show(n2['left'], 'Seven steps to the left'), show(n2['right'], 'Seven steps to the right'),
        show(n2['band'], 'One band in the middle'), pt('choice 3', 'Three is inside'), mk('cross', 'choice 1', 'Five and'),
        mk('cross', 'choice 4', 'eleven are past'), mk('cross', 'choice 2', 'negative twenty-five is way'), mk('tick', 'choice 3', 'Three, number three'))),
    S('Method 3 · Plugging in the answers',
      L("[pause] Our third method, plugging in the answers. Five plus three is eight, not smaller than seven. Negative "
        "twenty-five plus three is negative twenty-two, its absolute value is twenty-two. Too big.",
        show(d1, 'Five plus three'), mk('cross', 'choice 1', 'not smaller than seven'),
        pt('d1', 'Negative twenty-five plus'), pt('choice 2', 'its absolute value is twenty-two'), mk('cross', 'choice 2', 'Too big')),
      L("Three plus three is six, and six is smaller than seven. It works, so in the exam you circle it and move on.",
        show(d2, 'Three plus three'), mk('circle', 'd2: six', 'six is smaller'), pt('choice 3', 'It works'), mk('tick', 'choice 3', 'circle it')),
      L("Which way is better? With numbers in the choices, plugging in is the fastest here. But the closed range is the one "
        "to make automatic. An absolute value smaller than a number? Take that number, put its minus on the other side, and "
        "the inside is trapped between them. [pause] Okay. I'll see you in the next question.",
        pt('d2', 'Which way is better'), show(v1, 'plugging in is the fastest'), show(v2, 'But the closed range'), pt('stem', 'An absolute value smaller'),
        show(v3, 'Take that number'), mk('underline', 'v3', 'trapped between them'))),
])

# ------------------------------------------------------------------------------------------------ q-361 (Q4)
# NEW: the sign flips on the negative side; "cannot" = the one that fails.  REMINDER: big side = open range.
r1 = I('r1', 'Big side: open range', size=32, col=1)
e1 = I('e1', '$x+1>8$, so $\\hl{r}{x>7}$', hand='x+1 > 8,  so  \\hl{r}{x > 7}')
e2 = I('e2', '$x+1<-8$, so $\\hl{l}{x<-9}$', hand='x+1 < −8,  so  \\hl{l}{x < −9}')
n3 = NL('n3', fig(-13, 11, [(-9, '−9'), (-1, '−1'), (2, '2'), (7, '7')], [(None, -9, False, False), (7, None, False, False)],
                  center=(-1, 8), title='|x + 1| > 8: more than 8 from −1, x < −9 or x > 7'))
f1 = I('f1', '$|9+1|=10>8$', size=32, col=1)
f2 = I('f2', '$|2+1|=\\hl{three}{3}$, not $>8$', size=32, col=1, hand='|2+1| = \\hl{three}{3}')
video('solve-q-361', 'solution', qid='q-361', slides=[
    S('Method 1 · Open range',
      L("Given: eight is smaller than x plus one, in absolute value. Which of the following cannot be the value of x?",
        pt('stem', 'Given', 'hl', 4.0), voice='calm', pause=0.5),
      L("Let's read it the other way round. Eight is smaller than the bars, so the bars are bigger than eight. They're on the "
        "big side. And look at the word cannot. We're looking for the one number that doesn't work. [short pause] We'll do "
        "it three ways.", pt('stem', 'the other way round'), show(r1, "They're on the"), pt('stem', 'the word cannot')),
      L("[short pause] Our first method, two cases. Big side means an open range, one part going to the right and one going "
        "to the left. So one option, the inside is bigger than eight. Take one off both sides, and x is bigger than seven.",
        pt('r1', 'Big side means'), show(e1, 'one option, the inside is bigger')),
      L("Or, the other option, the inside is smaller than negative eight. Now careful, the sign flips too, because now we're on the negative "
        "side. x plus one is smaller than negative eight, so x is smaller than negative nine.",
        show(e2, 'the inside is smaller than negative eight'), pt('e2: l', 'so x is smaller')),
      L("So what does that leave? x can be above seven, or below negative nine, but not in between.", pt('e1: r', 'above seven'),
        pt('e2: l', 'below negative nine')),
      L("Nine and eleven are bigger than seven, so they can be x. Negative ten is smaller than negative nine, so it can be x "
        "too. And two? It's not above seven, and it's not below negative nine. It's stuck in the middle, so x cannot be two. "
        "Number two is our answer.",
        pt('choice 1', 'Nine and'), pt('choice 4', 'eleven are bigger'), pt('e1: r', 'bigger than seven'), pt('choice 3', 'Negative ten'),
        pt('choice 2', 'And two'), mk('tick', 'choice 2', 'Number two is our answer'))),
    S('Method 2 · Number line',
      L("[pause] Our second method, the number line. x plus one is the distance from negative one. More than eight steps from "
        "negative one means past seven on the right, or past negative nine on the left.",
        show(n3, 'the distance from negative one'), pt('n3', 'past seven')),
      L("Two rays going outward, and a gap in the middle. Two is only three steps from negative one, and three isn't more "
        "than eight. So two sits in the gap, and it cannot be x. Number two.",
        pt('n3', 'a gap in the middle'), pt('choice 2', 'Two is only'), mk('tick', 'choice 2', 'it cannot be x'))),
    S('Method 3 · Plugging in the answers',
      L("[pause] Our third method, plugging in the answers. Nine plus one is ten, and ten is bigger than eight, so nine can "
        "be x.", show(f1, 'Nine plus one'), pt('choice 1', 'so nine can')),
      L("Two plus one is three, and three is not bigger than eight. So two doesn't work. And in a cannot question, the one "
        "that doesn't work is the answer. In the exam you'd circle it and move on.", show(f2, 'Two plus one'),
        mk('circle', 'f2: three', 'not bigger than eight'), mk('tick', 'choice 2', 'the one that')),
      L("So which way? Here plugging in is really fast, because the choices are numbers. But you'll need the open range when "
        "the choices are ranges. Big side, two rays going outward. Small side, one band in the middle. "
        "[pause] Okay. I'll see you in the next question.",
        pt('f2', 'plugging in is really fast'), pt('stem', 'Big side, two rays'))),
])

# ------------------------------------------------------------------------------------------------ q-362 (Q5)
# NEW: "minus x is not negative here"; an answer can't contain x if x cancels; R15 tie check (why -2, not -6).
# REMINDER: an expression means you may plug in (topic 51); |x| = -x for a negative x (lesson); x/|x| = 1 or -1 (topic 5).
g0 = I('g0', '$x=-2$', hand='x = −2')
g1 = I('g1', 'choices at $x=-2$: $\\ 14,\\ 6,\\ 2,\\ 12$', size=30, col=1)
g2 = I('g2', '$10+\\frac{4(-2)}{|-2|}=10+\\frac{-8}{2}=10-4=\\hl{six}{6}$', size=34, hand='10 + {4(−2)/|−2|} = 10 + {−8/2} = \\hl{six}{6}')
h1 = I('h1', '$x<0$, so $|x|=\\hl{mx}{-x}$', hand='x < 0,  so  |x| = \\hl{mx}{−x}')
h2 = I('h2', '$\\frac{4x}{-x}=\\hl{m4}{-4}$', hand='{4x/−x} = \\hl{m4}{−4}')
h3 = I('h3', '$10-4=6$', hand='10 − 4 = 6')
h4 = I('h4', '$\\frac{x}{|x|}=1$ $\;$ or $\;$ $-1$', size=34, col=1, hand='{x/|x|} = 1  or  −1')
h5 = I('h5', '$\\frac{-8}{8}=-1$', size=30, col=1)
video('solve-q-362', 'solution', qid='q-362', slides=[
    S('Method 1 · Plugging in numbers',
      L("Given: x is smaller than zero. What is ten plus four x over the absolute value of x?",
        pt('stem', 'Given', 'hl', 4.0), voice='calm', pause=0.5),
      L("So they're asking what an expression is equal to, and all we know is that x is negative. And what did we say about "
        "an expression with a letter? We're allowed to plug in a number. [short pause] So we'll start with plugging in, and "
        "then we'll do the algebra.", pt('stem', 'what an expression'), pt('stem', 'all we know')),
      L("[short pause] Our first method, plugging in numbers. x has to be negative, so I'll take negative two. Why negative "
        "two? Before I plug in, I glance at the choices. At negative two they give fourteen, six, two and twelve, all "
        "different. So one plug-in will be enough.",
        show(g0, "I'll take negative two"), pt('choice 1', 'I glance at the choices'), show(g1, 'At negative two they give')),
      L("Negative six would be a bad pick, by the way. Then minus x is six, and two choices would come out the same.",
        pt('choice 3', 'Then minus x is six'), pt('choice 2', 'two choices')),
      L("So four times negative two is negative eight. The absolute value of negative two is two. Negative eight over two "
        "is negative four, and ten minus four is six.",
        show(g2, 'four times negative two'), mk('circle', 'g2: six', 'ten minus four is six'), voice='calm'),
      L("Which choice gives six at negative two? Only number two. So six, number two is our answer.",
        pt('g1', 'Which choice gives six'), mk('tick', 'choice 2', 'Only number two'))),
    S('Method 2 · Algebra',
      L("[pause] Our second method, the algebra. x is negative, so what's its absolute value? To turn a negative number "
        "positive, I take minus x. So the absolute value of x is minus x.",
        pt('stem', 'x is negative'), show(h1, 'So the absolute value of x is minus x')),
      L("Now careful here. A lot of students see minus x and think it's negative. It isn't. x itself is negative, so minus x "
        "is positive.", pt('h1: mx', 'see minus x'), pt('h1: mx', 'so minus x')),
      L("So four x over minus x. The x's cancel, and four over minus one is negative four. Ten minus four is six.",
        show(h2, 'So four x over minus x'), pt('h2: m4', 'is negative four'), show(h3, 'Ten minus four'), voice='calm'),
      L("And remember this one from earlier in the course. x over its absolute value is always one or minus one. When x is "
        "negative, like negative eight over eight, it's minus one.", show(h4, 'always one or minus one'), show(h5, 'like negative eight')),
      L("So the answer doesn't depend on x at all. That's why numbers three and four, with an x in them, can't be right. "
        "So six again, number two.",
        mk('cross', 'choice 3', 'numbers three'), mk('cross', 'choice 4', 'and four'), mk('tick', 'choice 2', 'So six again')),
      L("Which way is better? Plugging in is the safety net, and it's quick. But once you know that x over its absolute value "
        "is one or minus one, the algebra takes seconds. [pause] Okay. I'll see you in the next question.",
        pt('h4', 'once you know'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t13-01 (Q6)
# NEW: a number in front of x breaks the "opposites" symmetry; "all the values" needs both cases.
# REMINDER (short): two cases.
k0 = I('k0', 'Inside $=7$ $\;$ or $\;$ inside $=-7$', size=32)
k1 = I('k1', '$2x-1=7$', hand='2x−1 = 7')
k2 = I('k2', '$2x=8$, so $x=\\hl{four}{4}$', hand='2x = 8,  so  x = \\hl{four}{4}')
k3 = I('k3', '$2x-1=-7$', hand='2x−1 = −7')
k4 = I('k4', '$2x=-6$, so $x=\\hl{m3}{-3}$', hand='2x = −6,  so  x = \\hl{m3}{−3}')
m0_ = I('m0_', '$x=4$: $\\ |2\\cdot4-1|=|7|=7$', size=32, col=1)
m1 = I('m1', '$x=-4$: $\\ |2(-4)-1|=|-9|=9$', size=32, col=1)
m2 = I('m2', '$x=-3$: $\\ |2(-3)-1|=|-7|=\\hl{seven}{7}$', size=32, col=1)
video('solve-q-r26-t13-01', 'solution', qid='q-r26-t13-01', slides=[
    S('Method 1 · Two cases',
      L("Given: two x minus one, in absolute value, is equal to seven. Which of the following gives all the possible values "
        "of x?", pt('stem', 'Given', 'hl', 4.5), voice='calm', pause=0.5),
      L("So this time there's a number in front of x. And they ask for all the values, so we'll need both cases. "
        "[short pause] Two ways, two cases first, and then plugging in the answers.",
        pt('stem', 'a number in front of x'), pt('stem', 'all the values')),
      L("[short pause] Our first method, two cases. Which numbers have an absolute value of seven? Seven and negative "
        "seven. So the inside is seven, or the inside is negative seven.",
        show(k0, 'the inside is seven')),
      L("First case. Two x minus one is seven. To get x alone, add one, and two x is eight. Divide by two, and x is four.",
        show(k1, 'Two x minus one is seven'), show(k2, 'two x is eight'), mk('circle', 'k2: four', 'x is four'), voice='calm'),
      L("x is four, so I can already cross out number four. It doesn't have a four in it.",
        pt('choice 4', 'cross out number four'), mk('cross', 'choice 4', "It doesn't have")),
      L("Now careful. A lot of students just flip the sign here and say negative four. But there's a minus one inside the "
        "bars, so let's really solve the second case.", pt('choice 2', 'just flip the sign'), pt('k1', 'a minus one inside')),
      L("Two x minus one is negative seven. Add one, and two x is negative six. Divide by two, and x is negative three.",
        show(k3, 'Two x minus one is negative seven'), show(k4, 'two x is negative six'), mk('circle', 'k4: m3', 'x is negative three'),
        voice='calm'),
      L("So four or negative three, number three is our answer. Number one forgets the second case, and number two is the "
        "flipped sign.", mk('tick', 'choice 3', 'number three is our answer'), mk('cross', 'choice 1', 'Number one forgets'),
        mk('cross', 'choice 2', 'the flipped sign'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Our second method, plugging in the answers. Three of the choices have four in them, so let's test four "
        "first. Two times four is eight, minus one, seven. Its absolute value is seven, so four works.",
        pt('choice 1', 'Three of the choices'), show(m0_, 'Two times four')),
      L("And what does that tell us? Number four is three or negative four, so it leaves out four, a value that works. "
        "Number four is out.", pt('choice 4', 'Number four is three'), mk('cross', 'choice 4', 'Number four is out')),
      L("Now the other numbers. Negative four. Two times negative four is negative eight, minus one, negative nine. Its "
        "absolute value is nine, not seven. So number two is out.",
        show(m1, 'Two times negative four'), mk('cross', 'choice 2', 'number two is out')),
      L("Negative three. Two times negative three is negative six, minus one, negative seven. Its absolute value is seven, "
        "so it works too. So number one, four only, misses negative three. It's four or negative three, number three.",
        show(m2, 'Two times negative three'), mk('circle', 'm2: seven', 'Its absolute value is seven'),
        mk('cross', 'choice 1', 'misses negative three'), mk('tick', 'choice 3', 'number three')),
      L("So two cases, two answers, and don't assume they're opposites. When there's a number in front of x, or a number "
        "added inside, solve the second case all the way. [pause] Okay. I'll see you in the next question.",
        pt('m2', "don't assume"))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t13-02 (Q7)
# NEW (full): a negative or zero right side - bars < negative: never; bars > negative: always; bars = 0: one solution;
# bars = negative: no solution.  REMINDER: absolute value is never negative.
s1 = I('s1', '$|\\text{anything}|\\ge 0$', size=34, col=1)
s2 = I('s2', '(1) $\\ x-3=0$, so $x=3$', size=32, hand='(1)  x−3 = 0,  so  x = 3')
s3 = I('s3', '(2) $\\ $never', size=32, hand='(2)  never')
s4 = I('s4', '(3) $\\ $every $x$', size=32, hand='(3)  every x')
s5 = I('s5', '(4) $\\ x=0$ works', size=32, hand='(4)  x = 0 works')
s6 = I('s6', 'Bars $<$ negative: never', size=30, col=1)
s7 = I('s7', 'Bars $>$ negative: always', size=30, col=1)
s8 = I('s8', 'Bars $=$ negative: no solution', size=30, col=1)
video('solve-q-r26-t13-02', 'solution', qid='q-r26-t13-02', slides=[
    S('Method 1 · Look at the right side',
      L("Which of the following has no solution?", pt('stem', 'Which', 'hl', 2.5), voice='calm', pause=0.5),
      L("So we're looking for the one that no number can satisfy. And before any algebra, look at the right sides. Two of "
        "them are negative, and one is zero. That's our hint.",
        pt('choice 2', 'Two of'), pt('choice 3', 'them are negative'), pt('choice 1', 'one is zero')),
      L("Remember, an absolute value is never negative. It can be zero, it can be positive, but it can never go below "
        "zero.", show(s1, 'never negative')),
      L("Number one. The bars are equal to zero. Can that happen? Yes, when the inside is zero. x minus three is zero, so x "
        "is three. It has a solution, so it's out.",
        pt('choice 1', 'Number one'), show(s2, 'x minus three is zero'), mk('cross', 'choice 1', "so it's out")),
      L("Number two. The bars are smaller than negative one. But the bars are never negative, so they can never be below "
        "negative one. No number works.", pt('choice 2', 'Number two'), pt('s1', 'never negative, so'), show(s3, 'No number works')),
      L("Number three looks almost the same, but the sign goes the other way. The bars are bigger than negative one. And "
        "that's always true, because the bars are zero or more. Every x works, so it's out.",
        pt('choice 3', 'Number three looks'), show(s4, 'Every x works'), mk('cross', 'choice 3', "so it's out")),
      L("Number four. The absolute value of x is at most one. Zero works, because zero is at most one. So it has a solution, "
        "and it's out.",
        pt('choice 4', 'Number four'), show(s5, 'Zero works'), mk('cross', 'choice 4', "and it's out")),
      L("So x plus two, in absolute value, smaller than negative one has no solution. Number two is our answer.",
        mk('tick', 'choice 2', 'Number two is our answer'))),
    S('The rule',
      L("[short pause] Now look at numbers two and three again. The same numbers, and a different sign. One is never true, "
        "and the other one is always true.",
        pt('choice 2', 'numbers two'), pt('choice 3', 'and three again'), show(s6, 'never true'), show(s7, 'always true')),
      L("And it works the same way for equations. Bars equal to a negative number, like bars equal to negative five, have no "
        "solution at all.", show(s8, 'Bars equal to a negative number')),
      L("Is there a second way? Sure, try to find one solution for each choice. Number one, try three. Three minus three is "
        "zero, so three works.", pt('choice 1', 'Number one, try three')),
      L("Number three, try zero. Zero plus two is two, and two is bigger than negative one, so zero works. Number four, zero "
        "again, and zero is at most one. Works.", pt('choice 3', 'Number three, try zero'), pt('choice 4', 'Number four, zero')),
      L("Number two, whatever x I try, x plus two in bars comes out zero or more. Try zero, it's two. Try negative two, it's "
        "zero. It never gets below negative one. So no solution, number two.",
        pt('choice 2', 'Number two, whatever'), mk('tick', 'choice 2', 'So no solution')),
      L("So always look at the right side first. A negative number or a zero there is a gift. "
        "[pause] Okay. I'll see you in the next question.", pt('s6', 'look at the right side')),
      sb='Method 1 · Look at the right side'),
])

# ------------------------------------------------------------------------------------------------ r26-t13-tools (lesson)
# NEW: |x|^2 = x^2 (why), |a-b| = |b-a|, reading |x - 3| < 4 as a distance.  REMINDER: sqrt(x^2) = |x| (topic 9),
# |x - a| = distance (lesson), a plus inside = distance from a negative number.
t1 = I('t1', '$|x|^2=x^2$', size=50, hand='|x|^2 = x^2')
t2 = I('t2', '$|-6|^2=36 \\qquad (-6)^2=36$', size=34)
t3 = I('t3', '$\\sqrt{x^2}=|x|$', size=44, col=1)
t4 = I('t4', '$|a-b|=|b-a|$', size=50, hand='|a−b| = |b−a|')
t5 = I('t5', '$|2-9|=7=|9-2|$', size=40, hand='|2−9| = 7 = |9−2|')
u1 = I('u1', '$|x-a|$ = the distance between $x$ and $a$', size=40)
u2 = I('u2', '$|x-3|<4$', size=40, col=1, hand='|x−3| < 4')
n4 = NL('n4', fig(-3, 9, [(-1, '−1'), (0, '0'), (3, '3'), (7, '7')], [(-1, 7, False, False)], center=(3, 4),
                  title='|x − 3| < 4: within 4 of 3, between −1 and 7'))
u3 = I('u3', '$-1<x<7$', size=40, col=1, hand='−1 < x < 7')
u4 = I('u4', '$|x+5|$ = the distance from $-5$', size=36, col=1)
video('r26-t13-tools', 'lesson', slides=[
    S('Absolute Value — Exam Tools',
      L("Welcome back. Before the harder absolute-value questions, I want to give you two tools. You'll meet them again and "
        "again in the next questions.")),
    S('Squares and bars',
      L("First, a square and the bars do the same thing to the sign. They both remove it. So the absolute value of x, "
        "squared, is just x squared.", show(t1, 'So the absolute value of x')),
      L("Let's see it in numbers. Take negative six. Bars first, the absolute value of negative six is six, and six squared "
        "is thirty-six. Without the bars, negative six squared is also thirty-six.",
        show(t2, 'Take negative six'), pt('t2', 'Without the bars')),
      L("Why does this work? Squaring kills the sign, and so do the bars. So once you square, it doesn't matter if the bars "
        "are there or not.", pt('t1', 'Squaring kills the sign')),
      L("And you saw the other direction with roots. The square root of x squared is the absolute value of x, not x. The "
        "root of negative six squared is the root of thirty-six, and that's six.", show(t3, 'The square root of x squared')),
      L("[short pause] Second, the order inside the bars doesn't matter. a minus b and b minus a are always opposites. "
        "Opposites attract, so together they cancel out to zero. But each one alone is the same distance from zero.",
        show(t4, 'the order inside the bars'), pt('t4', 'always opposites')),
      L("Two minus nine is negative seven, and its absolute value is seven. Nine minus two is seven. The same.",
        show(t5, 'Two minus nine'), voice='calm'),
      L("So inside the bars, I can switch the order. a minus b, or b minus a, it's the same thing.",
        mk('underline', 't4', 'I can switch the order')),
      sb='Squares and bars'),
    S('Distance',
      L("[short pause] Now the distance. Remember from the lesson, the absolute value of x minus a number is the distance "
        "between x and that number. Nine minus two in bars is seven, and from two to nine is exactly seven steps.",
        show(u1, 'the absolute value of x minus a number'), pt('u1', 'Nine minus two')),
      L("So how do I read the absolute value of x minus three, smaller than four? x is less than four steps away from "
        "three.", show(u2, 'So how do I read'), show(n4, 'less than four steps')),
      L("Start at three. Four steps to the left is negative one, and four steps to the right is seven. So x is anywhere "
        "between negative one and seven, not including them.", pt('n4', 'Start at three'), show(u3, 'So x is anywhere')),
      L("And careful with a plus inside. x plus five is x minus negative five, so it's the distance from negative five.",
        show(u4, 'a plus inside')),
      L("So two tools. Squares and bars both remove the sign, and the order inside the bars doesn't matter. And bars around "
        "x minus a number mean distance. [pause] Okay. I'll see you in the next video.",
        pt('u1', 'And bars around'))),
])

# ------------------------------------------------------------------------------------------------ q-363 (Q8)
# NEW: "m can't be 0" (a zero would break n != m); dividing a positive by 4 stays positive; a bad plug gets changed.
# REMINDER: absolute value is never negative.
v1 = I('v1', '$|n|=m \\qquad n\\ne m$', hand='|n| = m      n ≠ m')
v2 = I('v2', 'So $\\hl{m}{m>0}$', hand='So \\hl{m}{m > 0}')
v3 = I('v3', '$\\hl{n}{n=-m}$, $\\ n<0$', hand='\\hl{n}{n = −m},  n < 0')
v4 = I('v4', '$k=\\frac{m}{4}$: $\\ \\hl{k}{0<k<m}$', hand='k = {m/4} :  \\hl{k}{0 < k < m}')
n5 = NL('n5', fig(-6, 6, [(-4, 'n'), (0, '0'), (1, 'k'), (4, 'm')], [], title='n, then 0, then k, then m'))
w1 = I('w1', '$m=4$', hand='m = 4')
w2 = I('w2', '$n=4$?', hand='n = 4 ?')
w3 = I('w3', '$n=-4$', hand='n = −4')
w4 = I('w4', '$4k=4$, so $k=1$', hand='4k = 4,  so  k = 1')
w5 = I('w5', '$-4<1<4$: $\\ n<k<m$', size=34, col=1)
video('solve-q-363', 'solution', qid='q-363', slides=[
    S('Method 1 · Understanding',
      L("Given: the absolute value of n is equal to m, n is not equal to m, and four k is equal to m. Which of the following "
        "is necessarily true?", pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("So three letters, three givens, and every choice puts the letters in order. Most absolute-value questions on the "
        "exam are understanding questions, and this is one of them. [short pause] We'll solve it two ways, understanding "
        "first, and then plugging in numbers.", pt('choice 1', 'every choice puts'), pt('choice 2', 'the letters in order')),
      L("[short pause] Our first method. The absolute value of n is m, so n and m are the same distance from zero. But "
        "they're not equal. So what does that tell me?", show(v1, 'The absolute value of n is m')),
      L("m is an absolute value, so m can't be negative. It's zero or positive. Could m be zero? Then n is zero too, and "
        "they'd be equal. Not allowed. So m is positive.", pt('v1', 'm is an absolute value'), show(v2, 'So m is positive')),
      L("And n is the same distance from zero, but it's a different number. So n is the negative one, n is minus m.",
        show(v3, 'So n is the negative one')),
      L("Now, four k is equal to m. So to get from m to k, I divide by four. And dividing a positive number by four, or by a "
        "thousand, or by a million, gets closer and closer to zero, but it never goes negative. So k is positive, and "
        "smaller than m.", pt('stem', 'four k is equal to m'), show(v4, 'I divide by four'), pt('v4: k', 'So k is positive')),
      L("On the number line, n is on the left, then zero, then k, and m is as far from zero as n.",
        show(n5, 'On the number line')),
      L("So n is the smallest, k is in the middle, and m is the biggest. n, k, m, that's number two.",
        pt('n5', 'n is the smallest'), mk('tick', 'choice 2', "that's number two"))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Our second method, plugging in numbers. I need numbers that obey all three givens. Let's start with m. m is "
        "equal to an absolute value, so it can't be negative. Why four for m? Because four k is m, so I'll divide m by four, "
        "and four divides easily.",
        pt('stem', 'obey all three givens'), show(w1, 'Why four for m')),
      L("Now n. Let's try n is four. The absolute value of four is four, that's m. But n has to be different from m, so "
        "this pick is bad. Let's change it.", show(w2, "try n is four"), mk('cross', 'w2', 'this pick is bad')),
      L("n is negative four. Its absolute value is four, so it's equal to m, and it's different from m. Now both givens "
        "work.", show(w3, 'n is negative four')),
      L("And k? Four k is m, and m is four. So four k is four, and k is one.", show(w4, 'four k is four'), voice='calm'),
      L("Negative four, one, four. So n, then k, then m, that's number two. And the others break with these numbers. Number "
        "one says four is smaller than one, no. Number three also puts four below one, no. Number four says one is smaller "
        "than negative four, no.", show(w5, 'Negative four, one, four'), mk('tick', 'choice 2', "that's number two"),
        mk('cross', 'choice 1', 'Number one says'), mk('cross', 'choice 3', 'Number three also'), mk('cross', 'choice 4', 'Number four says')),
      L("Which way is better? I prefer understanding here, it's quick. But plugging in is an excellent backup. And when your "
        "first pick breaks a given, don't give up, just change the pick. [pause] Okay. I'll see you in the next question.",
        pt('w5', 'I prefer understanding'), pt('w3', 'just change the pick'))),
])

# ------------------------------------------------------------------------------------------------ q-364 (Q9)
# NEW: same side of zero - you can compare distances; different sides - you can't; the "two extreme pictures" plug-in.
n6 = NL('n6', fig(-5, 5, [(-4, 'p'), (-2, 'q'), (0, '0'), (2, 'r'), (4, 's')], [], title='p < q < 0 < r < s'))
x1 = I('x1', 'Same side: we know who is further', size=30, col=1)
x2 = I('x2', 'Different sides: we don\'t know', size=30, col=1)
y1 = I('y1', '$p=-50,\\ \\ q=-40,\\ \\ r=1,\\ \\ s=3$', size=34, hand='p = −50,  q = −40,  r = 1,  s = 3')
y2 = I('y2', '$p=-3,\\ \\ q=-1,\\ \\ r=40,\\ \\ s=50$', size=34, hand='p = −3,  q = −1,  r = 40,  s = 50')
video('solve-q-364', 'solution', qid='q-364', slides=[
    S('Method 1 · Number line',
      L("Given: p is smaller than q, which is smaller than zero, which is smaller than r, which is smaller than s. Which of "
        "the following is necessarily true?", pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("So we know the order of four numbers. And look at the answers, every one of them uses absolute value. And what's "
        "absolute value? Distance from zero. So the question is really, who is further from zero? [short pause] Two ways, "
        "the number line, and then plugging in numbers.",
        pt('choice 1', 'look at the answers'), pt('choice 4', 'every one of them')),
      L("[short pause] Our first method. Let's put them on the number line. p and q are negative, and p is further to the "
        "left. r and s are positive, and s is further to the right.", show(n6, 'on the number line')),
      L("There are two things we can promise. s is always further from zero than r, both on the right. And p is always "
        "further from zero than q, both on the left. We don't know by how much, but always.",
        show(x1, 'two things we can promise'), pt('n6', 'both on the right')),
      L("But a negative against a positive? The negatives could be negative one and negative three, and the positives a "
        "thousand and seven thousand. Or the other way around. We only know the order, not the numbers.",
        show(x2, 'a negative against a positive')),
      L("So number one compares r and p, a positive and a negative. Not necessarily, out. Number three, p and s, different "
        "sides again, out. Number four, q and s, different sides, out.",
        mk('cross', 'choice 1', 'Not necessarily, out'), mk('cross', 'choice 3', 'sides again, out'), mk('cross', 'choice 4', 'different sides, out')),
      L("Three are out, so in the exam you'd circle number two and move on. Here, let's see why it's right. q and p are "
        "both negative, and p is further from zero. So the absolute value of q is smaller than the absolute value of p. "
        "Number two is our answer.", pt('choice 2', 'circle number two'), pt('x1', 'both negative'),
        mk('tick', 'choice 2', 'Number two is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Our second method, plugging in numbers. The givens only fix the order, not the sizes. So the trick is to "
        "try two extreme pictures. First, the negatives far from zero and the positives close to it. p is negative fifty, q "
        "negative forty, r one and s three. They're in order, so they obey the given.",
        show(y1, 'p is negative fifty')),
      L("Number one, one smaller than fifty? Yes, it stays. Number two, forty smaller than fifty? Yes, it stays. Number "
        "three, fifty smaller than three? No, out. Number four, forty smaller than three? No, out.",
        pt('choice 1', 'Number one, one'), pt('choice 2', 'Number two, forty'),
        mk('cross', 'choice 3', 'No, out'), mk('cross', 'choice 4', 'forty smaller than three'), voice='calm'),
      L("Now the opposite picture, the negatives close to zero and the positives far. p is negative three, q negative one, "
        "r forty and s fifty.", show(y2, 'p is negative three')),
      L("Number one, forty smaller than three? No, out. Number two, one smaller than three? Yes, and it worked in the first "
        "picture too. So number two survives both pictures. Number two.", mk('cross', 'choice 1', 'No, out'), mk('tick', 'choice 2', 'survives both'), voice='calm'),
      L("So when the letters sit on both sides of zero, try one picture with the negatives far away, and one with the "
        "positives far away. Same side, you can compare. Different sides, you can't. [pause] Okay. I'll see you in the next "
        "question.", pt('y1', 'the negatives far away'), pt('y2', 'the positives far away'))),
])

# ------------------------------------------------------------------------------------------------ q-365 (Q10)
# NEW: "only a negative number changes under the bars" (y jumps above x); x lives in the band between y and -y, zero too;
# a "not necessarily" answer is proved by ONE allowed example; plugging in finds the signs by trying (all positive fails) -
# R30.  REMINDER: same side of zero = compare distances (q-364).
z1 = I('z1', '$y<x$ $\;$ but $\;$ $|y|>|x|$', hand='y < x   but   |y| > |x|')
z2 = I('z2', 'So $\\hl{y}{y<0}$', hand='So  \\hl{y}{y < 0}')
z3 = I('z3', '$z<y<0$, so $z<0$', hand='z < y < 0,  so  z < 0')
n7 = NL('n7', fig(-6, 6, [(-5, 'z'), (-4, 'y'), (0, '0'), (4, '−y')], [(-4, 4, False, False)],
                  title='x is somewhere between y and −y'))
q0 = I('q0', '$z=1,\\ y=2,\\ x=3$: $\\ |3|<|2|$? ✗', size=30, hand='z = 1,  y = 2,  x = 3 :   |3| < |2| ?  ✗')
q1 = I('q1', '$y=-4,\\ \\ z=-5$', size=32, hand='y = −4,  z = −5')
q1x = I('q1x', '$x=2$', size=32, hand='x = 2')
q2 = I('q2', '$-5<-4<2 \\qquad |2|<|-4|$', size=34)
q3 = I('q3', '$x=2=|2|$', hand='x = 2 = |2|')
q4 = I('q4', '(1) $4<5$ $\\quad$ (2) $-5\\ne5$ $\\quad$ (4) $2<5$', size=28, col=1)
video('solve-q-365', 'solution', qid='q-365', slides=[
    S('Method 1 · Understanding',
      L("Given: z is smaller than y, which is smaller than x, and the absolute value of x is smaller than the absolute "
        "value of y. Which of the following is not necessarily true?", pt('stem', 'Given', 'hl', 6.0), voice='calm', pause=0.5),
      L("This one is a hard analysis question, so let's take it slowly. And look at the wording, not necessarily true. So "
        "three choices are always true, and we're looking for the one that can fail. [short pause] Two ways, understanding "
        "first, and then plugging in numbers.", pt('stem', 'not necessarily true')),
      L("[short pause] Our first method. The first given puts them in order, but we don't know any signs yet. They could all "
        "be positive, all negative, or a mix.", pt('stem', 'The first given')),
      L("Now the second given. Without the bars, x is bigger than y. With the bars, y suddenly jumps above x. So what does "
        "that mean? Only a negative number changes when you put bars on it. So y must be negative.",
        show(z1, 'Without the bars'), show(z2, 'So y must be negative')),
      L("Why? If y were zero or positive, x would be even bigger, and further from zero, so the bars would keep the same "
        "order.", pt('z1', 'If y were zero or positive')),
      L("z is even smaller than y, so z is negative too, and further from zero.", show(z3, 'z is even smaller')),
      L("And x? x has to be closer to zero than y. So x lives in the band between y and minus y. It could be on the left of "
        "zero, it could be on the right, and it could even be zero.", show(n7, 'x lives in the band'), pt('n7', 'it could even be zero')),
      L("Now number three says x is not equal to its absolute value. That claims x must be negative. But x could be two, or "
        "zero, and then x is equal to its absolute value. So it's not necessarily true. Number three is our answer.",
        pt('choice 3', 'Now number three says'), mk('tick', 'choice 3', 'Number three is our answer')),
      L("In the exam you'd circle it and move on. Here, let's quickly see why the others are always true. z and y are both "
        "negative, and z is further left, so z is further from zero. Number one, always true.",
        pt('z3', 'z and y are both'), mk('cross', 'choice 1', 'Number one, always true')),
      L("z is negative, so it's not equal to its absolute value. Number two, always true. And z is further from zero than y, "
        "and y is further than x. So z is further than x. Number four, always true.",
        mk('cross', 'choice 2', 'Number two, always true'), mk('cross', 'choice 4', 'Number four, always true'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Our second method, plugging in numbers. In a not necessarily question, one allowed example that breaks a "
        "choice is enough. So I need numbers that obey both givens, and I'll find them by trying."),
      L("Why start with positive numbers? Because they're the most natural guess. z is one, y is two, x is three. They're in "
        "order. But is the absolute value of three smaller than the absolute value of two? No. So that try fails.",
        show(q0, 'z is one'), mk('cross', 'q0', 'So that try fails')),
      L("What went wrong? x has to be bigger than y, but closer to zero. If y is zero or positive, a bigger x is always "
        "further from zero. So y has to be negative, and far from zero. y is negative four, and z is even smaller, negative "
        "five.", pt('q0', 'What went wrong'), show(q1, 'y is negative four')),
      L("Now x. It has to be bigger than negative four, but closer to zero than four. Which one do I pick? Number three is "
        "about the sign of x, so a positive x is where something might break. x is two.",
        pt('choice 3', 'Number three is'), show(q1x, 'x is two')),
      L("Check the givens. Negative five, negative four, two, they're in order. And the absolute value of two is smaller "
        "than four. Both work.", show(q2, 'Check the givens'), voice='calm'),
      L("Number three says x is not equal to its absolute value. But two is equal to the absolute value of two. It breaks, "
        "so number three.", show(q3, 'But two is equal'), mk('tick', 'choice 3', 'so number three')),
      L("And the others hold with these numbers. Number one, four smaller than five, true. Number two, negative five isn't "
        "five, true. Number four, two smaller than five, true.", show(q4, 'Number one, four'), voice='calm'),
      L("So when the bars change the order, think negative, because only a negative number changes under the bars. "
        "[pause] Okay. I'll see you in the next question.", pt('q3', 'think negative'))),
])

# ------------------------------------------------------------------------------------------------ q-366 (Q11)
# NEW: decoding "possible but not necessarily"; bars and even powers act alike; a common factor comes out of the bars.
# REMINDER: |xy| = |x||y| and |a+b| <= |a|+|b| (lesson rules 2 and 3); squaring both sides when both are positive.
w0 = I('w0', 'Never true: out', size=30, col=1)
w9 = I('w9', 'Always true: out', size=30, col=1)
a1_ = I('a1_', '$|x+y|>3$, so $|x+y|^2>9$', size=34)
a2_ = I('a2_', '$|x+y|^2=(x+y)^2$', size=34, hand='|x+y|^2 = (x+y)^2')
ev = I('ev', 'Bars and even powers act alike', size=30, col=1)
a3_ = I('a3_', '$|x\\cdot y|=|x|\\cdot|y|$', size=34, hand='|x·y| = |x|·|y|')
a4_ = I('a4_', '$|5x+5y|=5\\,|x+y|$', size=34, hand='|5x+5y| = 5|x+y|')
a5_ = I('a5_', '$|x+y|\\le|x|+|y|$', size=34)
b1_ = I('b1_', '$x=4,\\ \\ y=1$: $\\ |5|>3$', size=34, hand='x = 4,  y = 1')
b2_ = I('b2_', '(1) $25>9$ $\\quad$ (2) $5<5$? $\\quad$ (3) $4<4$? $\\quad$ (4) $5<25$', size=30)
b3_ = I('b3_', '$x=6,\\ \\ y=-2$: $\\ |4|>3$', size=34, hand='x = 6,  y = −2')
b4_ = I('b4_', '(1) $16>9$ $\\quad$ (2) $\\hl{two}{4<8}$ $\\quad$ (3) $12<12$? $\\quad$ (4) $4<20$', size=30)
video('solve-q-366', 'solution', qid='q-366', slides=[
    S('Method 1 · The rules',
      L("x and y are integers. Given: three is smaller than x plus y, in absolute value. Which of the following is possible "
        "but not necessarily true?", pt('stem', 'x and y', 'hl', 6.0), voice='calm', pause=0.5),
      L("Unlike the last few questions, this is a technique question. And before we start, let's understand the wording. "
        "Possible, but not necessarily true.", pt('stem', 'the wording')),
      L("So anything that's never true is not possible, and it's out. And anything that's always true is necessarily true, "
        "so it's out too. We want the one that's sometimes true and sometimes not. [short pause] Two ways, the rules first, "
        "and then plugging in numbers.", show(w0, 'never true'), show(w9, 'always true')),
      L("[short pause] Our first method. Choice number one looks like the given, with brackets instead of bars, and a "
        "square. Both sides of the given are positive, so I'm allowed to square them. Why? Remember, with positive "
        "numbers, the bigger number also has the bigger square. Three squared, three times three, is nine.",
        pt('choice 1', 'Number one looks'), show(a1_, 'square them')),
      L("And x plus y in absolute value, squared, is the same as x plus y, squared. A square doesn't care about the sign. "
        "So choice number one is always true, and it's out.", show(a2_, 'is the same as'), mk('cross', 'choice 1', "and it's out")),
      L("And there's a much simpler way to see it. Bars and an even power behave the same way. What's true with bars is "
        "true with a square.", show(ev, 'Bars and an even power')),
      L("Choice number two, let's leave it for the end.", pt('choice 2', 'Number two')),
      L("Choice number three. The absolute value of x y, against the absolute value of x times the absolute value of y. "
        "Remember, you can split the bars over multiplication. So these two are always equal, never smaller. Never true, "
        "so it's out.",
        pt('choice 3', 'Number three'), show(a3_, 'you can split the bars'), mk('cross', 'choice 3', "Never true, so it's out")),
      L("Choice number four. Inside the bars I have five x plus five y. Take out the common factor five, and it's five "
        "times x plus y. Then split the bars. That's five times the absolute value of x plus y.", pt('choice 4', 'Number four'), show(a4_, 'Take out the common factor')),
      L("So it says something is smaller than five times itself. That's true for every positive number. Could it fail? Only "
        "if x plus y were zero, but the given says it's more than three in absolute value. So it's always true, out.",
        pt('a4_', 'smaller than five times itself'), pt('stem', 'the given says'), mk('cross', 'choice 4', "always true, out")),
      L("Three are out, so in the exam you'd circle choice number two. Here, let's see why it's right. The rule from the "
        "lesson says the absolute value of a sum is smaller than or equal to the sum of the absolute values. They're "
        "equal when x and y have the same sign, and it's smaller when the signs are opposite. So sometimes true, "
        "sometimes not. Choice number two is our answer.", pt('choice 2', 'circle choice number two'), show(a5_, 'The rule from the lesson'),
        mk('tick', 'choice 2', 'Number two is our answer'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Our second method, plugging in numbers. I'll try one pair with the same sign and one with opposite signs, "
        "because signs are what the bars care about. First, x four and y one, small and easy. Four plus one is five, and "
        "five is bigger than three, so they fit the given.",
        show(b1_, 'First, x four')),
      L("Choice number one, five squared is twenty-five, and twenty-five is bigger than nine, true. Choice number two, "
        "the absolute value of four plus one is five, and four plus one is also five. Five smaller than five? No. Choice "
        "number three, four times one is four, in bars four, and four times one is four. Four smaller than four? No. "
        "Choice number four, five times five is twenty-five, and five is smaller than twenty-five, true.", show(b2_, 'five squared is twenty-five'),
        voice='calm'),
      L("Now opposite signs. Why x six and y negative two? Because with opposite signs they cancel, so I need one of them "
        "much bigger, to keep the sum above three. Six plus negative two is four, and four is bigger than three, so they "
        "fit.",
        show(b3_, 'Why x six')),
      L("Choice number one, four squared is sixteen, bigger than nine, true. Choice number two, the absolute value of six "
        "is six, and of negative two it's two, so six plus two is eight. Four smaller than eight? True this time. Choice "
        "number three, six times negative two is negative twelve, in bars twelve, and six times two is twelve. Twelve "
        "smaller than twelve? No again. Choice number four, five times four is twenty, and four is smaller than twenty, "
        "true.",
        show(b4_, 'four squared is sixteen'), pt('b4_: two', 'True this'), voice='calm'),
      L("So choice number two was false once and true once. That's exactly possible but not necessarily. Choice number "
        "three was never true, and choice numbers one and four were true both times. Choice number two.", mk('tick', 'choice 2', 'Number two.')),
      L("Which way is better? If you know the rules, you can mark this one in seconds. If not, two pairs, same sign and "
        "opposite signs, will get you there. [pause] Okay. I'll see you in the next question.",
        pt('b1_', 'same sign and'), pt('b3_', 'opposite signs, will'))),
])

# ------------------------------------------------------------------------------------------------ q-r26-t13-13 (Q12)
# NEW: flipping one sign made it bigger -> they were cancelling -> opposite signs; other wordings of the same idea.
# REMINDER: same signs add, opposite signs cancel (lesson rule 3, q-366).
e1_ = I('e1_', 'same signs: $\\ 7+3=10$', size=34)
e2_ = I('e2_', 'opposite signs: $\\ 7-3=4$', size=34)
e3_ = I('e3_', '$|a+b|<|a-b|$: $\\ $opposite signs', size=34)
e4_ = I('e4_', '$|a+b|=7-3=\\hl{four}{4}$', size=34, hand='|a+b| = 7 − 3 = \\hl{four}{4}')
o1 = I('o1', '$|x+y|=|x|-|y|$: $\\ $opposite signs, $|x|\\ge|y|$', size=34)
o2 = I('o2', '$|a+b|<|a|$: $\\ $opposite signs', size=34)
o3 = I('o3', '$a=5,\\ b=-2$: $\\ |3|<|5|$', size=32)
d1_ = I('d1_', '$7,\\ 3$: $\\ |10|<|4|$? no', size=32)
d2_ = I('d2_', '$-7,\\ -3$: $\\ |-10|<|-4|$? no', size=32)
d3_ = I('d3_', '$7,\\ -3$: $\\ |\\hl{f1}{4}|<|10|$ yes', size=32)
d4_ = I('d4_', '$-7,\\ 3$: $\\ |\\hl{f2}{-4}|<|-10|$ yes', size=32)
video('solve-q-r26-t13-13', 'solution', qid='q-r26-t13-13', slides=[
    S('Method 1 · Understanding',
      L("Given: the absolute value of a is seven, the absolute value of b is three, and a plus b, in absolute value, is "
        "smaller than a minus b, in absolute value. What is the absolute value of a plus b?",
        pt('stem', 'Given', 'hl', 7.0), voice='calm', pause=0.5),
      L("So three givens. The first two give sizes, and the third one hides the signs. [short pause] We'll solve it two "
        "ways, understanding, and then trying all the sign options.", pt('stem', 'The first two'), pt('stem', 'the third one')),
      L("[short pause] Our first method. a is seven away from zero, and b is three away. Their signs, we don't know yet. "
        "So what can a plus b be? Same signs add up, seven plus three is ten. Opposite signs cancel, seven minus three is "
        "four.",
        show(e1_, 'Same signs add up'), show(e2_, 'Opposite signs cancel')),
      L("Now the third given. a minus b is just a plus b with the sign of b flipped. So flipping one sign made it bigger. "
        "What does that mean? Before the flip, they were cancelling. So a and b have opposite signs.",
        pt('stem', 'Now the third given'), show(e3_, 'So a and b have opposite signs')),
      L("Now careful, a lot of people think this means b is negative. It doesn't. It only means b has the opposite sign of a. "
        "a could be negative seven, and b three.", pt('e3_', 'a lot of people')),
      L("So it's the cancelling case. The bigger size minus the smaller one, seven minus three, four.",
        pt('e2_', 'the cancelling case'), show(e4_, 'seven minus three'), voice='calm'),
      L("So four, choice number four is our answer. Ten is the same-signs case, and the third given throws it out. "
        "Negative four can't be, because the bars are never negative. And cannot be determined is the trap for anyone who "
        "skips the third given.", mk('tick', 'choice 4', 'number four is our answer'), mk('cross', 'choice 2', 'Ten is the same-signs'),
        mk('cross', 'choice 3', 'Negative four'), mk('cross', 'choice 1', 'cannot be determined'))),
    S('Other wordings',
      L("[pause] The exam can say the same idea in other words, so let's see two of them."),
      L("The absolute value of x plus y, equals the absolute value of x, minus the absolute value of y. The sizes subtract. "
        "That's cancelling, so x and y have opposite signs, and x is the bigger one in size.",
        show(o1, 'The sizes subtract')),
      L("And if a plus b, in absolute value, is smaller than the absolute value of a, then adding b made it smaller. So "
        "again they cancelled, opposite signs. For example, a five and b negative two. Five plus negative two is three, "
        "and three is smaller than five.",
        show(o2, 'adding b made it smaller'), show(o3, 'For example'))),
    S('Method 2 · Plugging in numbers',
      L("[pause] Our second method, trying the signs. Not sure about the reasoning? a is seven or negative seven, and b is "
        "three or negative three. So there are only four sign options, and let's try them all."),
      L("Both positive, seven and three. Seven plus three is ten, and seven minus three is four. Ten is not smaller than "
        "four, so it's out. Both negative, negative seven and negative three. Negative seven plus negative three is "
        "negative ten, and negative seven minus negative three is negative four. In bars that's ten against four again. "
        "Out.",
        show(d1_, 'Both positive'), show(d2_, 'Both negative'), voice='calm'),
      L("Seven and negative three. Seven plus negative three is four, and seven minus negative three is ten. Four is "
        "smaller than ten, so it works. Negative seven and three. Negative seven plus three is negative four, and "
        "negative seven minus three is negative ten. In bars, four against ten. It works too.", show(d3_, 'Seven and negative three'), show(d4_, 'Negative seven and three'),
        voice='calm'),
      L("In both cases that work, the absolute value of a plus b is four. Choice number four. [short pause] So when you "
        "test signs, check same signs and opposite signs, because that's where the bars change things. [pause] Okay. I'll "
        "see you in the next question.", pt('d3_: f1', 'In both cases'), pt('d4_: f2', 'that work'), mk('tick', 'choice 4', 'Number four'))),
])

# r26-t13-mirror (lesson) and q-r26-t13-15 were REMOVED 2026-10-11 (teacher decision: the mirror test is not in her
# Hebrew course and not simple; plugging in numbers covers the same questions). See t13.py remove_mirror().

# ------------------------------------------------------------------------------------------------ q-r26-t13-03 (Q13)
# NEW (full): a letter on the right side - check every answer (why: x on both sides); the right side must be >= 0.
# REMINDER: two cases.
k5_ = I('k5_', '$x+4=3x$', hand='x+4 = 3x')
k6_ = I('k6_', '$4=2x$, so $x=2$', hand='4 = 2x,  so  x = 2')
k7_ = I('k7_', '$x+4=-3x$', hand='x+4 = −3x')
k8_ = I('k8_', '$4x=-4$, so $x=-1$', hand='4x = −4,  so  x = −1')
k9_ = I('k9_', '$x=2$: $\\ |6|=6=3\\cdot2$', size=34, col=1)
k10 = I('k10', '$x=-1$: $\\ |3|=3$, but $3\\cdot(-1)=\\hl{fake}{-3}$', size=32, col=1)
j1_ = I('j1_', '$3x\\ge0$, so $x\\ge0$', size=38)
j2_ = I('j2_', '$x+4>0$: $\\ x+4=3x$, so $x=2$', size=34, hand='x+4 > 0 :   x+4 = 3x,  so  x = 2')
video('solve-q-r26-t13-03', 'solution', qid='q-r26-t13-03', slides=[
    S('Method 1 · Two cases and a check',
      L("Given: x plus four, in absolute value, is equal to three x. Which of the following gives all the possible values of "
        "x?", pt('stem', 'Given', 'hl', 4.5), voice='calm', pause=0.5),
      L("Now there's a letter on the right side too. This is the first time we meet it, and it changes one thing. We'll have "
        "to check every answer we get. [short pause] Two ways, two cases with a check, and then a shortcut.",
        pt('stem', 'a letter on the right side')),
      L("[short pause] Our first method. Two cases, as usual. Case one, x plus four is three x. Take x off both sides, "
        "and four is two x. Four divided by two is two, so x is two.", show(k5_, 'Case one'), show(k6_, 'four is two x')),
      L("Case two, x plus four is minus three x. Add three x to both sides, x plus three x is four x, so four x plus four "
        "is zero. Take four off, and four x is minus four. Minus four divided by four is minus one, so x is minus one.", show(k7_, 'Case two'), show(k8_, 'Four x is minus four'), voice='calm'),
      L("Now the check. Why do we need it here? Because there's an x on both sides. When the other side is a plain number, "
        "you don't need to check. When it's a letter, you must.", pt('stem', 'an x on both sides')),
      L("x is two. Two plus four is six, in bars six. And three times two is six. It works.", show(k9_, 'x is two'), voice='calm'),
      L("x is minus one. Minus one plus four is three, in bars three. But three times minus one is minus three. Three isn't "
        "minus three, so minus one is fake.", show(k10, 'x is minus one'), mk('cross', 'k10: fake', 'so minus one is fake'), voice='calm'),
      L("Now careful, choice number three keeps the fake answer, and that's the trap. A lot of students stop right after "
        "the two cases. So only two, choice number one is our answer.", mk('cross', 'choice 3', "that's the trap"),
        mk('tick', 'choice 1', 'number one is our answer'))),
    S('Method 2 · Understanding',
      L("[pause] Our second method, a shortcut that starts from the right side. The bars are never negative, so the right "
        "side can't be negative. Three x is zero or positive, so x is zero or positive.", show(j1_, 'Three x is zero or positive')),
      L("And what does that mean for the bars? If x is zero or positive, x plus four is positive, so the bars do nothing. "
        "I can just drop them. x plus four is three x, so four is two x, and four divided by two is two. x is two.",
        pt('stem', 'the bars do nothing'), show(j2_, 'I can just drop them')),
      L("So two is the only value. Choice numbers two and three have minus one in them, and x can't be negative here, so "
        "they're out. Choice number four says there's no such number, but two is one, so it's out too. Two only, choice "
        "number one.",
        mk('cross', 'choice 2', 'Numbers two'), mk('cross', 'choice 3', 'and three have'), mk('cross', 'choice 4', 'Number four says'),
        mk('tick', 'choice 1', 'Two only, choice number one')),
      L("So a letter on the right side? The right side must be zero or positive, and check every answer in the original "
        "equation. [pause] Okay. I'll see you in the next question.", pt('j1_', 'The right side must be'))),
])

# ------------------------------------------------------------------------------------------------ q-367 (Q14)
# NEW: subtract equations to drop |y|; "bars alone on one side"; any positive x fails |x| = 10 + x.
# REMINDER: two options for an absolute-value equation; a letter on the right means check (q-r26-t13-03).
p1_ = I('p1_', '$|x|+3|y|=11$', hand='|x| + 3|y| = 11')
p2_ = I('p2_', '$|x|-x=11-1=10$', hand='|x| − x = 11 − 1 = 10')
p3_ = I('p3_', '$|x|=10+x$', hand='|x| = 10 + x')
p4_ = I('p4_', '$x=10+x$: $\\ 0=10$, false', size=34)
p5_ = I('p5_', '$x=-(10+x)$, so $2x=-10$, $\\ x=\\hl{m5}{-5}$', size=34, hand='x = −(10+x),  2x = −10,  x = \\hl{m5}{−5}')
q1_ = I('q1_', '$|x|=10+x$', hand='|x| = 10 + x')
q2_ = I('q2_', '$-2$: $\\ 2$ and $8$, no', size=34)
q3_ = I('q3_', '$-5$: $\\ 5=5$, yes', size=34)
r1_ = I('r1_', '$x=-2$: $\\ -2+3|y|=1$, so $|y|=1$', size=34)
r2_ = I('r2_', '$4\\cdot2+12\\cdot1=20$, not $44$', size=34)
r3_ = I('r3_', '$x=-5$: $\\ -5+3|y|=1$, so $|y|=2$', size=34)
r4_ = I('r4_', '$4\\cdot5+12\\cdot2=\\hl{ok}{44}$', size=34, hand='4·5 + 12·2 = \\hl{ok}{44}')
video('solve-q-367', 'solution', qid='q-367', slides=[
    S('Method 1 · Algebra',
      L("Given: four times the absolute value of x, plus twelve times the absolute value of y, is forty-four. And x plus "
        "three times the absolute value of y is one. What is x?", pt('stem', 'Given', 'hl', 7.0), voice='calm', pause=0.5),
      L("Two equations, two unknowns, and absolute values. It looks scary, but it's really not. [short pause] We'll solve it "
        "three ways. The full algebra, a shorter algebra that ends with the answers, and plugging in the answers right "
        "away.", pt('stem', 'Two equations')),
      L("[short pause] Our first method, the algebra. Four, twelve and forty-four can all be divided by four. Four over "
        "four is one, twelve over four is three, and forty-four over four is eleven. So the first equation becomes the "
        "absolute value of x, plus three times the absolute value of y, is eleven.",
        pt('stem', 'can all be divided by four'), show(p1_, 'So the first equation becomes')),
      L("They ask for x, so I want to get rid of y. How do I do that? I subtract the second equation from the first. "
        "Three times the absolute value of y cancels, and eleven minus one is ten. So the absolute value of x, minus x, "
        "is ten.", show(p2_, 'I subtract the second')),
      L("With absolute values, I want the bars alone on one side and everything else on the other. Why? Because then I "
        "can open the bars into two options, just like bars equal to a number. So I add x to both sides, and the absolute "
        "value of x is ten plus x.", show(p3_, 'the absolute value of x is ten plus x')),
      L("Now two options, the sides are equal, or one is the opposite of the other. Option one, x is ten plus x. Take x "
        "off both sides, x minus x is zero, so zero is ten. That's false, so no solution here.", show(p4_, 'Option one'), voice='calm'),
      L("Option two, x is minus ten minus x. Add x to both sides, x plus x is two x, so two x is minus ten. Minus ten "
        "divided by two is minus five, so x is minus five.",
        show(p5_, 'Option two'), mk('circle', 'p5_: m5', 'x is minus five'), voice='calm'),
      L("A letter on the right side, so let's check. Ten plus minus five is five, and the absolute value of minus five is "
        "five. It works. Minus five, choice number two is our answer.", pt('p3_', "so let's check"),
        mk('tick', 'choice 2', 'number two is our answer'))),
    S('Method 2 · Algebra, then the answers',
      L("[pause] Our second method. The same algebra, until we get to the absolute value of x is ten plus x. And then, "
        "instead of solving it, I plug in the answers. They're all numbers.", show(q1_, 'until we get to'),
        pt('choice 1', 'I plug in the answers')),
      L("Minus two. Its absolute value is two, and ten plus minus two is eight. Two isn't eight, out. Minus five. Its "
        "absolute value is five, and ten plus minus five is five. Yes.", show(q2_, 'Minus two'), mk('cross', 'choice 1', 'out.'),
        show(q3_, 'Minus five'), mk('tick', 'choice 2', 'Yes'), voice='calm'),
      L("And choice numbers three and four, three and five? For a positive x the bars do nothing, so the absolute value "
        "of x is just x. Then x is ten plus x, and that's impossible. So choice numbers three and four are out too.",
        mk('cross', 'choice 3', 'So choice numbers three'), mk('cross', 'choice 4', 'and four are out'))),
    S('Method 3 · Plugging in the answers',
      L("[pause] Our third method, plugging in the answers from the very start. Choice number one, x is minus two. Into "
        "the second equation, minus two plus three times the absolute value of y is one. Add two to both sides, one plus "
        "two is three, so three times the absolute value of y is three. Three divided by three is one, so the absolute "
        "value of y is one.",
        pt('choice 1', 'Number one'), show(r1_, 'Into the second')),
      L("Now the first equation. Four times two is eight, twelve times one is twelve, and eight plus twelve is twenty. Not "
        "forty-four, out.", show(r2_, 'Four times two'), mk('cross', 'choice 1', 'forty-four, out'), voice='calm'),
      L("Choice number two, x is minus five. Minus five plus three times the absolute value of y is one. Add five to both "
        "sides, one plus five is six, so three times the absolute value of y is six. Six divided by three is two, so the "
        "absolute value of y is two.", show(r3_, 'Number two')),
      L("First equation. Four times five is twenty, twelve times two is twenty-four, and twenty plus twenty-four is "
        "forty-four. It works.", show(r4_, 'Four times five'), mk('circle', 'r4_: ok', 'It works'),
        mk('tick', 'choice 2', 'It works'), voice='calm'),
      L("In the exam you'd circle it and move on. Here, let's quickly see three and five. x is three. Three plus three "
        "times the absolute value of y is one, so take three off, one minus three is negative two. But an absolute value "
        "can't be negative, so it's out. x is five, one minus five is negative four, negative again. Out.", mk('cross', 'choice 3', "so it's out"), mk('cross', 'choice 4', 'negative again. Out')),
      L("Which way would I pick? The shorter algebra that ends with the answers, or plugging in the answers right away. The "
        "full algebra is great to know, but here it's the longest. [pause] Okay. I'll see you in the next question.",
        pt('r4_', 'plugging in the answers right away'))),
])

# ------------------------------------------------------------------------------------------------ q-368 (Q15)
# NEW: equal bars = equal or opposite insides; squaring both sides of an equation with bars; the "smart plug" that
# separates two surviving choices; the given doesn't care which letter is x and which is y.  REMINDER: shortcut formula
# (topic 4), bars ~ even powers (q-366).
c1_ = I('c1_', '$x+4y=4x+y$', hand='x+4y = 4x+y')
c2_ = I('c2_', '$3y=3x$, so $\\hl{e}{y=x}$', hand='3y = 3x,  so  \\hl{e}{y = x}')
c3_ = I('c3_', '$x+4y=-4x-y$', hand='x+4y = −4x−y')
c4_ = I('c4_', '$5x=-5y$, so $\\hl{o}{x=-y}$', hand='5x = −5y,  so  \\hl{o}{x = −y}')
s1q = I('s1q', '$(x+4y)^2=(4x+y)^2$', hand='(x+4y)^2 = (4x+y)^2')
s2q = I('s2q', '$x^2+\\hl{l}{8xy}+16y^2=16x^2+\\hl{r}{8xy}+y^2$', size=34)
s3q = I('s3q', '$15y^2=15x^2$, so $y^2=x^2$', hand='15y^2 = 15x^2,  so  y^2 = x^2')
s4q = I('s4q', '$|y|=|x|$', hand='|y| = |x|')
t1q = I('t1q', '$x=y=2$: $\\ |10|=|10|$', hand='x = y = 2 :  |10| = |10|')
t2q = I('t2q', '$x=2,\\ y=-2$: $\\ |-6|=|6|$', hand='x = 2,  y = −2 :  |−6| = |6|')
video('solve-q-368', 'solution', qid='q-368', slides=[
    S('Method 1 · Two cases',
      L("Given: x plus four y, in absolute value, is equal to four x plus y, in absolute value. Which of the following is "
        "necessarily true?", pt('stem', 'Given', 'hl', 5.0), voice='calm', pause=0.5),
      L("One equation, two unknowns, and bars on both sides. [short pause] We'll solve it three ways, two cases, squaring "
        "both sides, and plugging in numbers.", pt('stem', 'bars on both sides')),
      L("[short pause] Our first method, two cases. Two absolute values are equal when the insides are equal, or when one "
        "is the opposite of the other. Why? Equal absolute values mean the same distance from zero. So the insides are "
        "the same number, like five and five, or opposites, like five and negative five.", pt('stem', 'Two absolute values are equal')),
      L("Option one, they're equal. x plus four y is four x plus y. Take x and y off both sides. Four y minus y is three "
        "y, and four x minus x is three x. So three y is three x, and dividing both by three, y is x.", show(c1_, 'Option one'), show(c2_, 'Three y is three x'), voice='calm'),
      L("Option two, they're opposites. x plus four y is minus, open bracket, four x plus y. That's minus four x minus y.",
        show(c3_, "That's minus four x")),
      L("Move everything to the left. x plus four x is five x, and four y plus y is five y. So five x plus five y is "
        "zero. Divide by five, x plus y is zero, so x is minus y.", show(c4_, 'five x plus five y'),
        voice='calm'),
      L("So x is y, or x is minus y. Choice number two, x is y, is only half the story, because x could be minus y. But "
        "choice number three, the absolute value of x equals the absolute value of y. Equal or opposite, it's the same "
        "size in both cases. Always true. Choice number three is our answer.", pt('c2_: e', 'So x is y'), pt('c4_: o', 'or x is minus y'),
        mk('cross', 'choice 2', 'only half the story'), mk('tick', 'choice 3', 'Number three is our answer')),
      L("And choice numbers one and four? When x is y, x isn't smaller than y, and y isn't smaller than x. Out.",
        mk('cross', 'choice 1', 'numbers one'), mk('cross', 'choice 4', 'and four'))),
    S('Method 2 · Square both sides',
      L("[pause] Our second method, squaring both sides. Bars on both sides, and both sides are zero or positive. So I'm "
        "allowed to square them, and after squaring, the bars are gone.", show(s1q, 'allowed to square them')),
      L("Open both with the shortcut formula. On the left, x squared plus eight x y plus sixteen y squared. On the right, "
        "sixteen x squared plus eight x y plus y squared.", show(s2q, 'Open both'), voice='calm'),
      L("Eight x y is on both sides, so it cancels. Now move the terms. Sixteen y squared minus y squared is fifteen y "
        "squared, and sixteen x squared minus x squared is fifteen x squared. So fifteen y squared is fifteen x squared. "
        "Divide by fifteen, and y squared is x squared.", mk('cross', 's2q: l', 'Eight x y'), mk('cross', 's2q: r', 'so it cancels'),
        show(s3q, 'fifteen y squared'), voice='calm'),
      L("And remember, bars and even powers act alike. If the squares are equal, the absolute values are equal. Choice "
        "number three.", show(s4q, 'the absolute values are equal'), mk('tick', 'choice 3', 'Number three'))),
    S('Method 3 · Plugging in numbers',
      L("[pause] Our third method, plugging in numbers. It's not so obvious here, but it's the shortest. Look at the "
        "given. If x and y are equal, both sides are the same. So x two and y two. Two plus four times two is two plus "
        "eight, ten. And four times two plus two is ten too. Ten on both sides, it works.",
        show(t1q, 'So x two and y two')),
      L("With equal numbers, y smaller than x is false, and x smaller than y is false. Choice numbers one and four are "
        "out.",
        mk('cross', 'choice 1', 'y smaller than x is false'), mk('cross', 'choice 4', 'x smaller than y is false')),
      L("Choice numbers two and three both survive, and the answers give us a hint. Equal, or equal in absolute value. So "
        "the tie-breaker is opposite numbers. x two and y minus two. Four times minus two is minus eight, and two minus "
        "eight is minus six. Four times two is eight, and eight minus two is six. Six and six in bars, it works.", pt('choice 2', 'Two and'), pt('choice 3', 'three both survive'), show(t2q, 'x two and y minus two')),
      L("So they don't have to be equal, and choice number two is out. Choice number three.",
        mk('cross', 'choice 2', "don't have to be equal"), mk('tick', 'choice 3', 'Number three.')),
      L("And notice, the given doesn't care which one is x and which is y. So y smaller than x can't be necessarily true, "
        "and the same goes for x smaller than y. Just swap them.", pt('stem', "the given doesn't care"),
        pt('choice 1', 'So y smaller than x'), pt('choice 4', 'the same goes for')),
      L("Three approaches. The third is the hardest to spot, but it's the shortest. Pick what feels comfortable for you. "
        "[pause] Okay. I'll see you in the next question.", pt('t2q', 'The third is'))),
])

# ------------------------------------------------------------------------------------------------ q-369 (Q16)
# NEW: a double inequality with bars = two bands; minus nine goes on the left; the split method (both overlaps); where the
# bait comes from.  REMINDER: acting on all three parts (topic 12), small / big side.
b1q = I('b1q', '$7<2x-1<9$', size=32, hand='7 < 2x−1 < 9')
b2q = I('b2q', '$-9<2x-1<-7$', size=32, hand='−9 < 2x−1 < −7')
b3q = I('b3q', '$8<2x<10$, so $4<x<5$', size=32, hand='8 < 2x < 10,  so  4 < x < 5')
b5q = I('b5q', '$-8<2x<-6$, so $\\hl{ans}{-4<x<-3}$', size=32, hand='−8 < 2x < −6,  so  \\hl{ans}{−4 < x < −3}')
bait = I('bait', 'Take off $1$: $\\ 3<x<4$, the bait', size=30, col=1)
n8 = NL('n8', fig(-6, 6, [(-4, '−4'), (-3, '−3'), (0, '0'), (4, '4'), (5, '5')], [(-4, -3, False, False), (4, 5, False, False)],
                  title='7 < |2x − 1| < 9: −4 < x < −3 or 4 < x < 5'), w=480)
sp1 = I('sp1', '$|2x-1|<9$: $\\ -4<x<5$', size=34, hand='|2x−1| < 9 :  −4 < x < 5')
sp2 = I('sp2', '$|2x-1|>7$: $\\ x>4$ $\;$ or $\;$ $x<-3$', size=34, hand='|2x−1| > 7 :  x > 4  or  x < −3')
sp3 = I('sp3', 'Both: $\\ 4<x<5$ $\;$ or $\;$ $-4<x<-3$', size=34)
d1q = I('d1q', '(1) $\\ 3.5$: $\\ |6|=6$, no', size=32)
d2q = I('d2q', '(2) $\\ 5.5$: $\\ |10|=10$, no', size=32)
d3q = I('d3q', '(3) $\\ -3.5$: $\\ |-8|=\\hl{eight}{8}$, yes', size=32)
d4q = I('d4q', '(4) $\\ -4.5$: $\\ |-10|=10$, no', size=32)
video('solve-q-369', 'solution', qid='q-369', slides=[
    S('Method 1 · Two bands',
      L("Given: seven is smaller than two x minus one, in absolute value, which is smaller than nine. Which of the following "
        "ranges is possible for x?", pt('stem', 'Given', 'hl', 5.0), voice='calm', pause=0.5),
      L("A double inequality with bars, and ranges in the choices. We'll solve it three ways, two bands, splitting it in two, "
        "and plugging in the answers. [short pause] And there's a bait in the choices, so I'll show you where it comes from.",
        pt('stem', 'A double inequality'), pt('choice 1', 'ranges in the choices')),
      L("[short pause] Our first method, two bands. Two x minus one, in bars, is between seven and nine. So the inside is "
        "between seven and nine, or, on the negative side, between minus nine and minus seven.",
        show(b1q, 'So the inside is'), show(b2q, 'on the negative side')),
      L("Careful with the negative band. Minus nine is the smaller one, so it goes on the left. Minus nine is smaller than two "
        "x minus one, which is smaller than minus seven.", pt('b2q', 'Minus nine is the smaller')),
      L("The positive band first. Add one to all three parts. Seven plus one is eight, and nine plus one is ten, so "
        "eight, two x, ten. Divide all three by two. Eight over two is four, and ten over two is five. So x is between "
        "four and five.", pt('b1q', 'The positive band'), show(b3q, 'Add one to all three'), voice='calm'),
      L("Now a lot of students take one off instead of adding it. Seven minus one is six, nine minus one is eight, and "
        "over two that's three to four. That's choice number one, the bait. And choice number four is the same mistake on "
        "the negative side.", show(bait, 'take one off'), pt('choice 1', "That's choice number one"),
        mk('cross', 'choice 1', 'the bait'), mk('cross', 'choice 4', 'number four is the same')),
      L("Four to five isn't in the choices, so on to the negative band. Add one to all three parts. Minus nine plus one "
        "is minus eight, and minus seven plus one is minus six. Divide by two. Minus eight over two is minus four, and "
        "minus six over two is minus three. So x is between minus four and minus three.",
        pt('b3q', "isn't in the choices"), show(b5q, 'Add one to all three'), voice=None),
      L("Aaand that's exactly choice number three. On the number line, two small bands, one on each side. Minus four to "
        "minus three, and four to five.", mk('tick', 'choice 3', "that's exactly choice number three"), show(n8, 'On the number line'))),
    S('Method 2 · Split it',
      L("[pause] Our second method, splitting it in two. The bars smaller than nine means the inside is trapped between "
        "minus nine and nine. Add one, minus eight and ten. Divide by two, minus four and five. So x is between minus "
        "four and five.", show(sp1, 'The bars smaller than nine')),
      L("The bars bigger than seven means the inside is above seven, or below minus seven. Seven plus one is eight, over "
        "two is four. Minus seven plus one is minus six, over two is minus three. So x is above four, or below minus "
        "three.", show(sp2, 'The bars bigger than seven')),
      L("Both have to hold. Between minus four and five, and above four, gives four to five. Between minus four and five, "
        "and below minus three, gives minus four to minus three. And minus four to minus three is choice number three.", show(sp3, 'Both have to hold'),
        mk('tick', 'choice 3', 'is choice number three')),
      L("It's longer here, but this split is super useful in other absolute-value questions.", pt('sp1', "It's longer"))),
    S('Method 3 · Plugging in the answers',
      L("[pause] Our third method, plugging in the answers. If a range is possible, every number in it has to work. So I "
        "pick an easy number inside each range, and if it breaks the given, the range is out. Choice number one, three "
        "and a half. Two times it is seven, minus one, six. Six isn't bigger than seven, out.", show(d1q, 'three and a half'), mk('cross', 'choice 1', 'seven, out')),
      L("Choice number two, five and a half. Two times it is eleven, minus one, ten. Ten isn't smaller than nine, out.",
        show(d2q, 'five and a half'), mk('cross', 'choice 2', 'nine, out'), voice='calm'),
      L("Choice number three, minus three and a half. Two times it is minus seven, minus one, minus eight. In bars, "
        "eight. Between seven and nine, it works.", show(d3q, 'minus three and a half'), mk('circle', 'd3q: eight', 'In bars, eight'),
        mk('tick', 'choice 3', 'it works'), voice='calm'),
      L("And choice number four, minus four and a half. Times two is minus nine, minus one, minus ten. In bars, ten. Out.",
        show(d4q, 'minus four and a half'), mk('cross', 'choice 4', 'In bars, ten'), voice='calm'),
      L("Plugging in was much shorter here. We need to let go of the instinct to solve everything. These shortcuts aren't "
        "cheats, they're the proper way on this exam. But know the two bands too, because the choices won't always be "
        "ranges. [pause] Okay. I'll see you in the next question.", pt('d3q', 'Plugging in was much shorter'))),
])

# ------------------------------------------------------------------------------------------------ q-370 (Q17)
# The known struggle spot: case 2 is written out exactly (|x| = -x, so x + |x| = 0 < 12, always true).
# NEW: split at zero when x and |x| are added; "most precise"; zero kills two choices; the smart plug below -6.
k1r = I('k1r', '$x\\ge0$: $\\ \\ x+x<12$', size=36)
k2r = I('k2r', '$2x<12$, so $x<6$', hand='2x < 12,  so  x < 6')
k3r = I('k3r', '$x<0$: $\\ \\ x+(-x)=\\hl{zero}{0}$', size=36)
k4r = I('k4r', '$-4+4=0 \\qquad -9+9=0$', size=34, hand='−4+4 = 0      −9+9 = 0')
k5r = I('k5r', '$0<12$: every negative works', size=34)
n9 = NL('n9', fig(-9, 9, [(-6, '−6'), (0, '0'), (6, '6')], [(None, 6, False, False)], title='x + |x| < 12: x < 6'))
m1r = I('m1r', '$x=0$: $\\ 0+0=0<12$', hand='x = 0 :  0 + 0 = 0 < 12')
m2r = I('m2r', '$x=-8$: $\\ -8+8=0<12$', hand='x = −8 :  −8 + 8 = 0 < 12')
video('solve-q-370', 'solution', qid='q-370', slides=[
    S('Method 1 · Two cases',
      L("Given: x plus the absolute value of x is smaller than twelve. What is the most precise domain for x?",
        pt('stem', 'Given', 'hl', 4.0), voice='calm', pause=0.5),
      L("So first, what does most precise mean? The domain has to hold exactly the numbers that work, no more and no less. "
        "[short pause] We'll solve it two ways, two cases, and plugging in the answers.", pt('stem', 'most precise')),
      L("[short pause] Our first method, two cases. The bars act differently on each side of zero, so that's where we "
        "split."),
      L("Case one, x is zero or positive. Then the bars do nothing, the absolute value of x is just x. So x plus x is "
        "smaller than twelve. Two x is smaller than twelve, and twelve divided by two is six, so x is smaller than six.",
        show(k1r, 'Case one'), show(k2r, 'Two x is smaller')),
      L("Now case two, and careful here, because this is the case people lose. x is negative. Then the bars turn x into its "
        "opposite, so the absolute value of x is minus x. And x plus minus x? Opposites attract, so they cancel out to zero.",
        show(k3r, 'x is negative'), mk('circle', 'k3r: zero', 'cancel out to zero')),
      L("Let's see it in numbers. Minus four plus four is zero. Minus nine plus nine is zero. Always zero.",
        show(k4r, 'Minus four plus four'), voice='calm'),
      L("And is zero smaller than twelve? Yes, every time. So every negative number works.", show(k5r, 'every negative number')),
      L("Put the two cases together. Every negative number, and the positives below six. That's every number below six. On "
        "the number line, one ray going left from six, an open circle at six, and no stop at minus six.",
        pt('k2r', 'the positives below six'), show(n9, 'On the number line')),
      L("So x smaller than six, choice number three is our answer.", mk('tick', 'choice 3', 'number three is our answer'))),
    S('Method 2 · Plugging in the answers',
      L("[pause] Our second method, plugging in the answers. One number that breaks a choice crosses it out. Let's try zero "
        "first. Why zero? Because the choices disagree about zero, two of them include it and two leave it out. Zero plus zero is zero, smaller than twelve, so zero works.", show(m1r, "Let's try zero")),
      L("But choice number two says x is smaller than zero, and choice number four says x is bigger than zero. Both leave "
        "zero out. So one number kills two choices.", mk('cross', 'choice 2', 'number two says'), mk('cross', 'choice 4', 'number four says')),
      L("Choice numbers one and three both stop at six on top. The difference is the bottom, minus six, or no limit at "
        "all. So I test a number below minus six, minus eight.", pt('choice 1', 'Numbers one'), pt('choice 3', 'and three both stop'),
        show(m2r, 'minus eight')),
      L("Minus eight plus its absolute value, eight, is zero. Zero is smaller than twelve, so it works. So x can go below "
        "minus six, and choice number one misses those numbers. Choice number three.", mk('cross', 'choice 1', 'number one misses'),
        mk('tick', 'choice 3', 'Number three.'), voice='calm'),
      L("Both approaches are excellent, pick what's comfortable for you. And when x and its absolute value are added, split at "
        "zero. On the negative side, they cancel to zero. [pause] Okay. I'll see you in the next question.",
        pt('m2r', 'On the negative side'))),
])

# ------------------------------------------------------------------------------------------------ r26-t13-summary
# REMINDERS only (every rule of the topic, said the way it was taught), in the order of the sidebar.
y1s = I('y1s', '$|x|$ = the distance from $0$: never negative', size=40)
y2s = I('y2s', '$|3|=3 \\qquad |-10|=10 \\qquad |0|=0$', size=44)
y3s = I('y3s', 'Letters: if $x=-7$, then $|x|=7=-x$', size=40)
y4s = I('y4s', 'An expression inside: the whole inside first', size=36)
r1s = I('r1s', '$|a\\cdot b|=|a|\\cdot|b| \\qquad \\left|\\frac{a}{b}\\right|=\\frac{|a|}{|b|}$', size=44)
r2s = I('r2s', '$|a+b|\\le|a|+|b|$', size=44)
r3s = I('r3s', '$|x|^2=x^2 \\qquad \\sqrt{x^2}=|x| \\qquad |a-b|=|b-a|$', size=40)
c1s = I('c1s', '$|x|>x$: negative $\\qquad |x|=x$: $\\ x\\ge0$', size=40)
c2s = I('c2s', '$|x|=-x$: $\\ x\\le0 \\qquad x>|x|$: impossible', size=40)
c3s = I('c3s', '$a\\cdot b>0$: same signs $\\qquad \\frac{x}{|x|}=1$ or $-1$', size=40)
e1s = I('e1s', '$|x+2|=10$: $\\ x+2=10$ or $x+2=-10$', size=40)
e2s = I('e2s', '$x=8$ or $x=-12$', size=40)
e3s = I('e3s', 'Letter on the right: check every answer', size=38)
e4s = I('e4s', 'Bars on both sides: square both sides', size=38)
i1s = I('i1s', '$|x-5|<3$: $\\ 2<x<8$ (between)', size=40)
i2s = I('i2s', '$|x-5|>3$: $\\ x>8$ or $x<2$ (outside)', size=40)
i3s = NL('i3s', SNL.two(dict(lo=0, hi=10, ticks=[(2, '2'), (5, '5'), (8, '8')], segs=[(2, 8, False, False)]),
                        dict(lo=0, hi=10, ticks=[(2, '2'), (5, '5'), (8, '8')], segs=[(None, 2, False, False), (8, None, False, False)]),
                        title='small side: one band; big side: two rays'), w=600)
g1s = I('g1s', '$|x-4|<-2$: $\\ $no solution', size=42)
g2s = I('g2s', '$|x-4|>-2$: $\\ $every $x$', size=42)
g3s = I('g3s', '$|x-4|\\le0$: $\\ x=4$', size=42)
h1s = I('h1s', '$|x-a|$ = the distance between $x$ and $a$', size=40)
h2s = I('h2s', '$|x+6|$ = the distance from $-6$', size=40)
j1s = I('j1s', 'An expression $=$ ? $\\ $ Plug in a number that fits', size=38)
j2s = I('j2s', 'Check the choices come out different. Two survive? Plug in again', size=32)
z1s = I('z1s', 'Is the letter positive, negative, or zero?', size=38)
z2s = I('z2s', 'Did I keep both cases?', size=38)
z3s = I('z3s', 'Is the right side negative or zero?', size=38)
z4s = I('z4s', 'Letter on the right: did I check every answer?', size=38)
z5s = I('z5s', 'Must, could, cannot, or not necessarily?', size=38)
video('r26-t13-summary', 'lesson', slides=[
    S('Summary',
      L("Before you practice, here's a quick summary of absolute value. Everything important, in a few minutes.")),
    S('Distance from zero',
      L("Absolute value is the distance from zero. So it's zero or positive, never negative. The absolute value of three is "
        "three, of negative ten it's ten, and of zero it's zero.", show(y1s, 'the distance from zero'), show(y2s, 'The absolute value of three')),
      L("With a plain number, the minus just drops off. But a letter hides its sign. If x is negative seven, its absolute "
        "value is seven, and that's minus x.", show(y3s, 'a letter hides its sign')),
      L("And with an expression inside, calculate the whole inside first, and only then the bars.", show(y4s, 'calculate the whole inside'))),
    S('The rules',
      L("A product, or a fraction? The bars can go on each part.", show(r1s, 'A product')),
      L("A sum is different. Same signs, the sizes add. Opposite signs, they cancel, so the result is smaller. And read it "
        "backwards, if the sizes cancelled, the signs were opposite.", show(r2s, 'A sum is different')),
      L("A square and the bars both remove the sign. The square root of x squared is the absolute value of x, not x. And the "
        "order inside the bars doesn't matter.", show(r3s, 'A square and the bars'))),
    S('Sign clues',
      L("Compare a number with its absolute value, and you know its sign. A bigger absolute value means the number is "
        "negative. Equal means zero or positive. Equal to minus the number means zero or negative.",
        show(c1s, 'Compare a number'), show(c2s, 'Equal to minus the number')),
      L("Don't forget the zero, it's the favorite trap.", pt('c1s', "Don't forget the zero")),
      L("A positive product means same signs, and a negative product means opposite signs. And x over its absolute value is "
        "one, or minus one.", show(c3s, 'A positive product'))),
    S('Equations',
      L("Bars equal to a number? Two cases, plus and minus. x plus two, in bars, is ten. So x plus two is ten, and ten "
        "minus two is eight. Or x plus two is minus ten, and minus ten minus two is minus twelve. Keep both.", show(e1s, 'Two cases'), show(e2s, 'ten minus two is eight')),
      L("A letter on the right side? The right side must be zero or positive, and check every answer in the original "
        "equation.", show(e3s, 'A letter on the right side')),
      L("Bars on both sides? Both sides are zero or positive, so you're allowed to square them.", show(e4s, 'Bars on both sides'))),
    S('Inequalities',
      L("Bars on the small side, the inside is trapped in the middle. One band.", show(i1s, 'Bars on the small side')),
      L("Bars on the big side, two rays going outward.", show(i2s, 'Bars on the big side'), show(i3s, 'two rays'))),
    S('Negative right side',
      L("Look at the right side before any algebra. Bars smaller than a negative number? Never, no solution.",
        show(g1s, 'Bars smaller than')),
      L("Bars bigger than a negative number? Always, every x works.", show(g2s, 'Bars bigger than')),
      L("And bars at most zero? The inside must be zero, so there's one solution.", show(g3s, 'bars at most zero'))),
    S('Distance',
      L("The absolute value of x minus a is the distance between x and a.", show(h1s, 'the distance between')),
      L("And careful with a plus inside. x plus six is the distance from negative six.", show(h2s, 'a plus inside'))),
    S('Plug in',
      L("Asked what an expression equals? Plug in a number that fits the conditions, and check that the choices come out "
        "different. Two survive? Plug in again.", show(j1s, 'Plug in a number'), show(j2s, 'check that the choices'))),
    S('Before you practice',
      L("Before each question, ask yourself. Is the letter positive, negative, or zero? Did I keep both cases? Is the right "
        "side negative or zero?", show(z1s, 'Is the letter'), show(z2s, 'Did I keep'), show(z3s, 'Is the right side')),
      L("Did I check every answer when there's a letter on the right? And what exactly are they asking, must, could, "
        "cannot, or not necessarily?", show(z4s, 'Did I check'), show(z5s, 'what exactly')),
      L("The common traps are forgetting the zero, losing the second case, and keeping a fake answer. [pause] That's it. Now "
        "go practice, and I'll see you in the next video.", mk('underline', 'z1s', 'forgetting the zero'),
        mk('underline', 'z2s', 'losing the second case'), mk('underline', 'z4s', 'keeping a fake answer'))),
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
        if '[' in ph: return None
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
                if ph: add.append((k, pt(last, ph)))
            if add:
                allc = sorted(have + add, key=lambda x: x[0])
                ln['cues'] = [c for p, c in allc]
            for p, c in have:
                if c[0] == 'show': last = c[1]['_name']


# Method headers (2026-10-11, teacher: "make it easy to follow" - a method change must be clear on the board): a solution
# slide titled "Method N · X" gets a small header line "Method N: X" at the top of its work area, shown when the voice
# names the method in the slide's first line ("Our second method", "first by understanding", ...).
_ORD = r"(?:first|second|third|fourth)"


def _method_headers(vid):
    V = VIDEOS[vid]
    if V['kind'] != 'solution': return
    for si, sl in enumerate(V['slides']):
        m = re.match(r'Method (\d) · (.+)$', sl['title'])
        if not m: continue
        lines = sl['lines'][1:3] if si == 0 else sl['lines'][:1]       # slide 1: the lines after the question reading
        for ln in lines:
            say = ln['say']; h = re.search(r"\b(?:our %s method|%s by|%s,)" % (_ORD, _ORD, _ORD), say, re.I)
            if not h: continue
            ph = _unique(say, h.start(), 2)
            if not ph: continue
            left = sum(1 for l2 in sl['lines'] for c in l2['cues'] if c[0] == 'show' and c[1]['_col'] == 0 and not c[1].get('over'))
            if left >= 4: break        # a full left column keeps its room (the sidebar still names the method)
            it = I('hdr%d' % si, 'Method %s: %s' % (m.group(1), m.group(2)), size=28)
            have = [(_phrase_pos(say, c), c) for c in ln['cues']]
            ln['cues'] = [c for p, c in sorted(have + [(h.start() - .5, show(it, ph))], key=lambda x: x[0])]
            break


for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v)


if __name__ == '__main__':
    for _v in sys.argv[1:] or ORDER:
        _p = check(_v)
        if _p: print('PROBLEMS', _v, _p)
        print('ai script written:', write_json(_v), stats(_v))
