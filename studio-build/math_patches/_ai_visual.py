"""2026-10-09 AI pilots, extra visual guidance (teacher: "extra visual so it will be very easy to follow what you are
saying"). For the three AI-narrated pilot videos, almost every moment of the voice has something on screen: POINT
highlights on the part of the question / figure / board line / choice being named, every calculation step APPEARS when
it is said (one step per item, no arrow chains), marks (circle a key number, tick the answer, cross out eliminated
choices, underline the key-idea line) and a few-word key-idea line when the idea is said. No hand-writing.

ONE spec per video (VIS below) drives both sides, so they cannot drift apart:
  - the video (called from each topic patch's time-gated ai_pilot / ai_pointers - a take recorded before that
    patch's AI_CUTOFF keeps its video): apply(M, vid) rebuilds the cue lines and click items of the video's slides
    around its spoken lines (spoken lines are never changed, so the AI audio still lines up);
  - the AI script: `python3 math_patches/_ai_visual.py` writes each cue's "at" phrase into ai_scripts/<vid>.json (the
    spoken text is left exactly as it is, so the audio needs no new credits: ai_narrate.py <vid> --remap re-times).

A cue belongs to spoken line N (1-based, whole video) and fires when the voice reaches its phrase; "<phrase" = a phrase
of line N-1 (the question reading sits on the title slide while patching, so its cues hang on line 2 with "<").
Cue tuples:
  ('show', item, phrase)                         click item APPEARS (item = a dsl.T(...) dict; label = its text)
  ('point', target, phrase[, style[, dur]])      POINT: 'stem' · 'choice N' · 'fig: α' · 'fig: shaded' · 'item K[: part]'
  ('mark', kind, target, phrase)                 pen mark: kind circle | cross | tick | underline; target as POINT
  ('write', item, phrase, text)                  2026-10-10 HANDWRITING TEST: like 'show', but in a handwriting video the
                                                 item is hand-written (studio_handwrite.py `text` syntax, e.g. '{n/2}',
                                                 '\\hl{name}{..}') and drawn stroke by stroke from the phrase; elsewhere
                                                 it is the typed `item` (APPEAR), exactly as before
Handwriting videos = HANDWRITE (env AI_HANDWRITE="vid,vid" or "all"; default none, so the studio keeps the approved
typed pilots until the teacher picks handwriting). In them 'write' items are hand-written and every mark is drawn as an
imperfect hand stroke ('hand': 1); mark kind 'arrow' (an arrow pointing at the target) is also available there.
Items are numbered on their slide: the question is item 0, then the 'show' items in order (K below).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.dirname(HERE)
sys.path.insert(0, SB)
from dsl import T
import studio_handwrite as HWR

HANDWRITE = {x.strip() for x in os.environ.get('AI_HANDWRITE', '').split(',') if x.strip()}


def _hw(vid):
    return vid in HANDWRITE or 'all' in HANDWRITE


def HW(item, text):
    """the hand-written twin of a typed item: same place and width; a bit larger (pen writing has no heavy strokes,
    so at the typed size it reads smaller)"""
    return HWR.item(text, size=round(item.get('size', 46) * 1.2), **{k: item[k] for k in ('x', 'y', 'w') if k in item})


def R(t, y, x=1060, w=470, size=38):        # geometry: right of the figure
    return T(t, size=size, x=x, y=y, w=w)


def L(t, y, x=410, w=560, size=38):         # left column under the stem
    return T(t, size=size, x=x, y=y, w=w)


def RC(t, y, x=1010, w=540, size=38):       # right column under the stem
    return T(t, size=size, x=x, y=y, w=w)


VIS = {}

# ------------------------------------------------------------------------------------------------ geometry (topic 33)
G1 = R('$\\text{shaded}=\\hl{part}{\\text{part}}\\times\\hl{whole}{\\text{whole circle}}$', 320, size=32)
G2 = R('$S=\\pi r^2$', 400)
G3 = R('$r^2=(\\sqrt{35})^2=35$', 470)
G4 = R('$S=\\enspace\\hl{area}{35\\pi}$', 540)
G5 = R('$\\hl{left}{5\\alpha+5\\beta}=\\hl{full}{360°}$', 320)
G6 = R('$\\alpha+\\beta=\\enspace\\hl{sum}{72°}$', 400)
G7 = R('$30+42=72$', 480, size=32)
G8 = R('$12+60=72$', 540, size=32)
G9 = R('Sector $=\\frac{\\text{angle}}{360°}$ of the circle', 320, size=30)
G10 = R('$\\hl{frac}{\\frac{72°}{360°}}=\\hl{fifth}{\\frac{1}{5}}$', 400)
G11 = R('$\\frac{1}{5}\\times35\\pi=\\enspace\\hl{ans}{7\\pi}$', 490)
G12 = R("Can't find each? Find the sum.", 590, size=30)
VIS['solve-geo33-g091'] = {
    # line 1 (question reading) - cues hang on line 2 with "<"
    2: [('point', 'stem', '<A circle has a radius', 'hl', 4.5), ('point', 'fig: α', '<alpha, then'), ('point', 'fig: β', '<then beta'),
        ('point', 'fig: shaded', '<One sector of each kind is shaded', 'hl', 2.2), ('point', 'stem', "<What's their total area"),
        ('point', 'fig: α', 'the two angles'), ('point', 'fig: β', 'separately')],
    3: [('point', 'fig: shaded', 'shaded part', 'hl', 3.0)],
    4: [('point', 'fig: shaded', 'The shaded part is just'), ('show', G1, 'So I need two things'), ('point', 'item 1: whole', 'The area of the whole circle'),
        ('point', 'item 1: part', 'how much of it is shaded')],
    5: [('show', G2, 'pi r squared'), ('point', 'stem', 'Here r is root'), ('show', G3, 'Squaring cancels'),
        ('show', G4, 'The whole circle is'), ('mark', 'circle', 'item 4: area', 'thirty-five pi.')],
    6: [('point', 'fig: shaded', 'how much of it is shaded'), ('point', 'fig: α', 'I need the angles'),
        ('point', 'fig: β', "they don't give me")],
    7: [('point', 'fig: α', 'five alphas', 'hl', 2.0), ('point', 'fig: β', 'five betas', 'hl', 2.0),
        ('show', G5, 'five alpha plus five beta'), ('point', 'item 1: full', 'three sixty degrees')],
    8: [('point', 'item 1: left', 'this side', 'both'), ('point', 'item 1', 'two unknowns'),
        ('point', 'item 1: left', 'their sum')],
    9: [('point', 'item 1', 'Divide both sides'), ('show', G6, 'alpha plus beta is equal'),
        ('mark', 'circle', 'item 2: sum', 'seventy-two degrees')],
    10: [('show', G7, 'thirty and forty-two'), ('show', G8, 'Twelve and sixty'),
         ('point', 'item 2', 'all I need is their sum', 'both')],
    11: [('show', G9, 'A sector takes'), ('point', 'fig: shaded', 'the two shaded sectors'),
         ('show', G10, 'seventy-two out of three sixty'), ('point', 'item 2: fifth', 'is one fifth')],
    12: [('show', G11, 'one fifth of thirty-five pi'), ('mark', 'circle', 'item 3: ans', "that's seven pi")],
    13: [('mark', 'tick', 'choice 2', 'number two'), ('point', 'fig: shaded', 'We never even found'),
         ('show', G12, "So when you can't find"), ('mark', 'underline', 'item 4', 'looking for their sum')],
}

# ------------------------------------------------------------------------------------------------ algebra (topic 19)
A1 = L('Operation $=$ a rule', 250)
A2x = RC('$\\div 2$, then $+5$', 250)
A2 = RC('$\\hl{in}{2x}$ in, $\\;\\hl{out}{x+5}$ out', 320)
A3 = RC('$\\blacklozenge(n)=\\hl{half}{\\frac{n}{2}}+5$', 400)
A4 = L('$\\hl{two}{2x}=14$', 340)
A5 = L('$x=7$', 410)
A6 = L('$\\blacklozenge(14)=\\hl{rule}{x+5}$', 480)
A7 = L('$7+5=\\enspace\\hl{tw}{12}$', 550)
# 2026-10-10 handwriting test: every calculation / key-idea line is a 'write' (typed exactly as before unless the video
# is in HANDWRITE); the hand-written text keeps the same \hl parts the POINT / circle cues use
VIS['solve-q-544'] = {
    2: [('point', 'stem', '<The operation diamond is defined', 'hl', 5.0), ('point', 'stem', "<And they're asking"),
        ('write', A1, 'is JUST a rule', 'Operation = a rule'),
        ('mark', 'underline', 'item 1', "That's it."), ('point', 'stem', 'The diamond works on two x', 'hl', 2.2),
        ('point', 'stem', 'What does this operation'), ('write', A2x, 'divides it by two', '÷2, then +5'),
        ('write', A2, 'Two x goes in', '\\hl{in}{2x} in, \\hl{out}{x+5} out'), ('point', 'item 3: out', 'x plus five comes out'),
        ('write', A3, 'half of the number', '◆(n) = \\hl{half}{{n/2}} + 5'), ('point', 'item 4: half', 'Pretty simple')],
    3: [('point', 'item 3: in', 'Fourteen is the two x'), ('point', 'item 3: out', 'straight into x plus five'),
        ('point', 'choice 2', 'They get nineteen', 'both'), ('mark', 'cross', 'choice 2', "That's the trap")],
    4: [('write', A4, 'Two x is equal to fourteen', '\\hl{two}{2x} = 14'), ('write', A5, 'x is equal to seven', 'x = 7')],
    5: [('write', A6, 'Now the rule says', '◆(14) = \\hl{rule}{x+5}'), ('write', A7, 'Seven plus five', '7+5 =  \\hl{tw}{12}'),
        ('mark', 'circle', 'item 8: tw', 'is twelve'),
        ('point', 'item 4', 'half of fourteen', 'both')],
    6: [('mark', 'tick', 'choice 1', 'number one')],
    7: [('point', 'item 1', 'an operation like this'), ('point', 'item 4', 'what it really does', 'hl', 2.0),
        ('point', 'item 7: rule', 'use the rule', 'hl', 2.0)],
}

# ------------------------------------------------------------------------------------------- word problem (topic 22)
W1 = L('Ratio table: both go up ↑ ↑', 290, w=1100)
WN = L('2 notebooks: twice the price', 355, w=1100, size=30)
W2 = L('Here: workers ↑ days ↓', 420, w=1100)
W3 = L('Fewer workers: more than 10 days', 490, w=1100)
W4 = L('Whole job $=$ worker-days', 290)
W5 = L('1 worker-day $=$ 1 worker for 1 day', 360, size=30)
W6 = RC('$6\\times10=\\enspace\\hl{sixty}{60}\\enspace$ worker-days', 290)
W7 = RC('$4\\times d=60$', 360)
W8 = RC('$d=\\frac{60}{4}=\\enspace\\hl{ans}{15}$', 430)
W9 = L('One up, one down: the product stays the same', 520, w=1100, size=32)
W10 = L('workers $\\times$ days $\\quad$ speed $\\times$ time', 590, w=1100, size=32)
VIS['solve-q-r26-t22-02'] = {
    2: [('point', 'stem', '<Six workers paint a hall', 'hl', 4.5), ('point', 'stem', '<How many days would four workers'),
        ('show', W1, 'both numbers grow together'), ('show', WN, 'Two notebooks cost'), ('point', 'item 1', "it's the opposite"),
        ('show', W2, 'the number of days goes down'), ('point', 'item 3', 'More workers, fewer days'),
        ('mark', 'cross', 'item 1', "just won't work")],
    3: [('point', 'item 3', 'More days, or fewer'), ('point', 'stem', 'fewer workers now'),
        ('show', W3, 'it has to be more than ten days'), ('mark', 'underline', 'item 4', 'See?')],
    4: [('point', 'choice 1', 'Six and two thirds'), ('point', 'choice 4', 'and eight.'),
        ('mark', 'cross', 'choice 1', 'number one and'), ('mark', 'cross', 'choice 4', 'number four are out')],
    5: [('show', W4, 'measure the whole job'), ('show', W5, 'So one worker-day')],
    6: [('point', 'stem', 'Six workers work for ten days'), ('show', W6, 'Six times ten'),
        ('mark', 'circle', 'item 3: sixty', 'the job is sixty'), ('point', 'stem', "it's the same hall"),
        ('point', 'item 3: sixty', 'no matter how many workers', 'both')],
    7: [('point', 'item 3: sixty', 'split those sixty'), ('show', W7, 'Four times d'),
        ('show', W8, 'd is equal to sixty over four'), ('mark', 'circle', 'item 5: ans', "That's fifteen days")],
    8: [('mark', 'tick', 'choice 3', 'number three')],
    9: [('point', 'choice 1', 'Six and two thirds is what', 'both'), ('point', 'choice 2', 'twelve just adds', 'both'),
        ('mark', 'cross', 'choice 1', 'They'), ('mark', 'cross', 'choice 2', "both wrong")],
    10: [('show', W9, 'When one number goes up'), ('mark', 'underline', 'item 6', 'stays the SAME'),
         ('show', W10, 'Workers and days, or speed')],
}


def _label(t):
    return re.sub(r'\s+', ' ', re.sub(r'\\hl\{[^{}]*\}', '', t.replace('$', ''))).strip()


def _draw(kind, target):
    m = re.match(r'choice (\d)$', target)
    if m: return {'Circle': 'Circle', 'cross': 'Cross out', 'tick': 'Tick', 'underline': 'Underline', 'circle': 'Circle'}[kind] + ' choice ' + m.group(1)
    return None


def cues_of(vid):
    """-> {line: [(cue line dict or ('item', dict, label)), ...]}, {line: [phrase, ...]}"""
    lines, ats = {}, {}
    hw = _hw(vid)
    for n, cs in VIS[vid].items():
        for c in cs:
            if c[0] == 'write' and hw:
                lines.setdefault(n, []).append(('item', HW(c[1], c[3]), "'%s' is written" % re.sub(r'[{}]', '', _label(c[3])), True)); ats.setdefault(n, []).append(c[2])
            elif c[0] in ('show', 'write'):
                lines.setdefault(n, []).append(('item', c[1], "'%s' appears" % _label(c[1]['t']))); ats.setdefault(n, []).append(c[2])
            elif c[0] == 'point':
                d = {'point': c[1], 'label': c[1]}
                if len(c) > 3: d['style'] = c[3]
                if len(c) > 4: d['dur'] = c[4]
                lines.setdefault(n, []).append(d); ats.setdefault(n, []).append(c[2])
            else:
                kind, target, ph = c[1], c[2], c[3]
                d = {'draw': _draw(kind, target)} if _draw(kind, target) else {'draw': '%s %s' % (kind.capitalize(), target), 'mark': kind, 'target': target}
                if hw: d['hand'] = 1
                lines.setdefault(n, []).append(d); ats.setdefault(n, []).append(ph)
    return lines, ats


def _merge_title(v):
    """the build (no_question_numbers.py) later moves the spoken lines of a 'Question N' title slide onto the first real
    slide and DROPS the title slide's cue lines. Cues of those lines must live on the real slide, so do that move now,
    the same way (the build then finds no title slide and leaves the video alone)."""
    import no_question_numbers as NQ
    beats = v.get('beats') or []
    if v.get('kind') == 'solution' and len(beats) > 1 and beats[0].get('mode') == 'title' \
            and re.fullmatch(r'Question \d+', beats[0].get('bigTitle') or ''):
        intro = [x for x in (NQ._opener(l['say']) for l in beats[0].get('lines') or [] if l.get('say')) if x]
        beats = v['beats'] = beats[1:]
        beats[0]['lines'] = [{'say': x} for x in intro] + (beats[0].get('lines') or [])
        if v.get('hybrid') is not None: v['hybrid']['sidebar'] = [b.get('title') or 'Solution' for b in beats]
        for i, b in enumerate(beats): b['active'] = i; b['number'] = i + 1


def apply(M, vid):
    """rebuild the cue lines + click items of every slide of `vid` around its spoken lines (see the module doc)."""
    v = M.video(vid); cues, _ = cues_of(vid)
    _merge_title(v)
    for b in v['beats']:                                   # keep the pre-loaded items and the spoken lines only
        b['items'] = b['items'][:b['pre']]; b['lines'] = [l for l in b['lines'] if 'say' in l]
        b.pop('arw', None)
    pos = [(b, i) for b in v['beats'] for i, l in enumerate(b['lines'])]
    # count from the END: while patching, the title slide can still hold an intro line that the build drops later
    o = json.load(open(os.path.join(SB, 'ai_scripts', vid + '.json'), encoding='utf-8')); total = sum(len(x) for x in o['slides'])
    assert len(pos) >= total, (vid, len(pos), total)
    pos = pos[len(pos) - total:]
    for n in sorted(cues, reverse=True):                   # from the end, so earlier positions stay valid
        b, i = pos[n - 1]; new = []
        for c in cues[n]:
            if isinstance(c, tuple):
                b['items'].append(dict(c[1])); new.append({'appear': len(b['items']) - 1, 'label': c[2]})
                if len(c) > 3 and c[3]: new[-1]['write'] = 1
            else: new.append(dict(c))
        b['lines'][i:i] = new
    # items were appended from the last line backwards: renumber so items appear in order on each slide
    for b in v['beats']:
        ap = [l for l in b['lines'] if 'appear' in l]
        if not ap: continue
        old = [l['appear'] for l in ap]; items = b['items'][:b['pre']] + [b['items'][k] for k in old]
        for j, l in enumerate(ap): l['appear'] = b['pre'] + j
        b['items'] = items
    M.touched_videos.add(vid)


def write_at(vid):
    """write the cue phrases into ai_scripts/<vid>.json (spoken text untouched)."""
    p = os.path.join(SB, 'ai_scripts', vid + '.json'); o = json.load(open(p, encoding='utf-8'))
    _, ats = cues_of(vid); n = 0
    for sl in o['slides']:
        for i, x in enumerate(sl):
            n += 1; d = x if isinstance(x, dict) else {'say': x}
            d.pop('at', None)
            if n in ats: d['at'] = ats[n]
            d = {k: d[k] for k in ('say', 'voice', 'at', 'pause') if k in d}
            sl[i] = d if len(d) > 1 else d['say']
    json.dump(o, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('at phrases written:', vid, sum(len(a) for a in ats.values()))


if __name__ == '__main__':
    for vid in sys.argv[1:] or list(VIS):
        write_at(vid)
