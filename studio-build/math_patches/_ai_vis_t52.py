"""Topic 52 (Charts & Tables) - the scripts for the teacher's own-voice reading (2026-10-21), written from the first draft
to the Codex review standard, the clarity style, W1-W21, R37 (core methods taught in the lessons), the method vocabulary
and the method visuals. The DSL and the visual passes are copied from topic 25 (math_patches/_ai_vis_t25.py), so the
topics stay independent.

Topic 52 is NOT a math_patches/tNN.py topic: modulesV52a.py (the lessons) and modulesV52b.py (the three guided chart
sets) build its videos inside build_verbal.py. Like topic 51, build_verbal.py then calls
math_patches/_t52_reading.py ai_redo_t52(MATH), which rebuilds every video listed here from its ONE spec:
  - the script      ai_scripts/<vid>.json  (python3 math_patches/_ai_vis_t52.py [vid ...] writes it);
  - the visual plan VIS[vid] in the _ai_visual.py format (_ai_visual.py merges every _ai_vis_t*.py into its own VIS);
  - the studio video: the slides from studio_slides(vid) (spoken lines only), then _ai_visual.apply() adds the cues and
                    the click items around them.
The camera lesson 'ch52-intro' is read on camera in three parts (math_patches/_camera_parts.py). The long lessons are
split into parts (not on camera). The summary video 'ch52-summary' is not read: summary_pages/t52.json replaces it.

Charts. Every chart on the board is the course's OWN rendering (modulesV52a.py / modulesV52b.py / charts_assets.py, the
same function calls). The teaching marks - a highlighted bar, a reading line, a boundary line, a ring on a point, a
bracket - are built step by step at her words as transparent LAYERS over the chart: each layer is the difference between
the chart drawn with the mark and the chart drawn without it (OVL below), so it sits exactly on the chart. The chart is a
pre-loaded item with a figure id ('fig'), each layer an over item with 'of' = that id (studio_handwrite: a layer is drawn
at its own figure's place and scale, even when written lines come in between). The question figures stay as they are
(they become black and white centrally); our marks are amber, like the course's own highlights.

Spec DSL (as in topic 25): video / S(title, *lines, sb=None, pre=None) / L / I / IH / show / pt / mk; pre = the slide's
pre-loaded items (charts and quoted text, with their own x / y); solution slides pre-load the question (its text, the
chart, the four choices, modulesV52b.QC) unless pre is given. Board items: col 0 = under the chart (or the left column
when there is no chart), col 1 = the column right of the chart. Targets: 'stem' (= the question text), 'choice N',
'<item name>', '<item name>: <hl part>'.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(HERE) != 'math_patches':      # a test copy elsewhere still reads and writes the real studio files
    HERE = '/Users/nitzanslasky/psychometry-course/studio-build/math_patches'
SB = os.path.dirname(HERE)
if SB not in sys.path: sys.path.insert(0, SB)
from dsl import T, Q
import studio_handwrite as HWR
import charts_assets as CA
import modulesV52a as MA
import modulesV52b as MB

VIDEOS = {}
ORDER = []          # topic-52 flow order of the scripts
TAG = re.compile(r'\[(short pause|pause|long pause)\]')
CHOICE_N = re.compile(r'(?<![Cc]hoice )(?<![Tt]he )\b[Nn]umbers? (one|two|three|four)\b')   # = ai_check.py (R34)
VERDICT = re.compile(r'which (way|method|one of them) is (better|best|faster)|\bso which way\b', re.I)
AMBER = CA.AMBER


# ------------------------------------------------------------------------------------------------------------- DSL
def I(name, tex, size=34, col=0, hand=None):
    return {'_name': name, '_col': col, '_hand': hand, 'k': 't', 't': tex, 'size': size, 'gap': 16}


def NL(name, svg, w=560, col=0):
    vb = [float(t) for t in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    return {'_name': name, '_col': col, '_hand': None, 'k': 'vis', 'v': {'type': 'geometry', 'svg': svg}, 'w': w,
            'h': int(round(w * vb[3] / vb[2])), 'gap': 16}


def show(item, phrase): return ('show', item, phrase)
def pt(target, phrase, style=None, dur=None): return ('point', target, phrase, style, dur)
def mk(kind, target, phrase): return ('mark', kind, target, phrase)


def L(say, *cues, voice=None, pause=None):
    return {'say': say, 'cues': list(cues), 'voice': voice, 'pause': pause}


def S(title, *lines, sb=None, pre=None):
    return {'title': title, 'sb': sb or title, 'lines': list(lines), 'pre': pre}


def video(vid, kind, slides, qid=None, title=None):
    VIDEOS[vid] = {'kind': kind, 'slides': slides, 'qid': qid, 'title': title}
    ORDER.append(vid)


# ------------------------------------------------------------------------------------------------------ the charts
# A chart is a pre-loaded figure (fig id = its item name); its teaching marks are layers (over, of = the chart).
_EL = re.compile(r'<(\w+)\b[^>]*?/>|<(\w+)\b[^>]*>.*?</\2>', re.S)
_HI = ('#FDEBC8', '#E6F4F1')          # soft fills of a highlight: made see-through in a layer


def _parts(svg):
    head = svg[:svg.index('>') + 1]
    body = svg[svg.index('</title>') + 8:svg.rindex('</svg>')] if '</title>' in svg else svg[len(head):svg.rindex('</svg>')]
    defs = ''
    m = re.match(r'\s*<defs>.*?</defs>', body, re.S)
    if m: defs = m.group(0); body = body[m.end():]
    els = [m.group(0) for m in _EL.finditer(body)]
    if els and els[0].startswith('<rect') and 'fill="#fff' in els[0] and 'x=' not in els[0]: els = els[1:]   # the white page
    return head, defs, els


def OVL(base, marked, title='Mark'):
    """the transparent layer that turns the chart `base` into the chart `marked`: every element of `marked` that is not
    in `base` (in order), soft highlight fills made see-through, so the chart under it stays readable."""
    hb, _, eb = _parts(base); hm, defs, em = _parts(marked)
    left = {}
    for e in eb: left[e] = left.get(e, 0) + 1
    out = []
    for e in em:
        if left.get(e): left[e] -= 1; continue
        for f in _HI:
            if 'fill="%s"' % f in e and 'fill-opacity' not in e:
                e = e.replace('fill="%s"' % f, 'fill="%s" fill-opacity="0.5"' % f, 1)
        out.append(e)
    vb = re.search(r'viewBox="([^"]+)"', hm).group(1)
    ff = re.search(r'font-family="([^"]+)"', hm)
    body = ''.join(out)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"%s><title>%s</title>%s%s</svg>'
            % (vb, title, ' font-family="%s"' % ff.group(1) if ff else '', title, defs if 'url(#' in body else '', body))


def CH(name, svg, x, y, w, layers=()):
    """a chart placed at (x, y), w wide, as a pre-loaded item + its layers: layers = [(key, svg of the chart WITH the mark
    (and every earlier layer's mark))]; each layer draws only what it adds; a key '!name' = the whole new chart, drawn over
    the old one (the chart turns into another one, e.g. the points are joined into lines). -> {'base': item, key: ...}"""
    vb = [float(t) for t in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    h = round(w * vb[3] / vb[2], 1)
    base = {'_name': name, '_col': 0, '_hand': None, 'k': 'vis', 'v': {'type': 'geometry', 'svg': svg}, 'x': x, 'y': y,
            'w': w, 'h': h, 'fig': name, 'gap': 16, '_chart': True}
    out = {'base': base}; prev = svg
    for key, msvg in layers:
        full = key.startswith('!'); key = key.lstrip('!')      # '!key' = the whole new chart over the old one (a redraw)
        it = {'_name': '%s_%s' % (name, key), '_col': 0, '_hand': None, 'k': 'vis',
              'v': {'type': 'geometry', 'svg': msvg if full else OVL(prev, msvg, '%s: %s' % (name, key))}, 'w': w, 'h': h,
              'over': 1, 'of': name, 'gap': 0}
        LAYER_BASE[it['_name']] = name
        out[key] = it; prev = msvg
    return out


def QT(name, text, x, y, w, size=24):
    """a quoted line of a chart page (the explanation, the example, a note), pre-loaded (it sits in the quote panel)"""
    return {'_name': name, '_col': 0, '_hand': None, 'k': 't', 't': text, 'size': size, 'x': x, 'y': y, 'w': w}


LAYER_BASE = {}     # a figure layer's item name -> its base item's name (a POINT on a layer lights nothing visible)


# ----------------------------------------------------------------------------------------------- pre-loaded question
def QPRE(qid, name, layers=(), stem=None, choices=None):
    """the question slide of a chart set (the course's own layout, modulesV52b.QC): the question text on top, the chart
    under it as large as the space allows, the four choices at the bottom. -> (pre items, chart dict from CH)"""
    o = MB.QC(qid, stem=stem)
    pre, chart = [], None
    for k, it in enumerate(o['pre']):
        d = dict(it)
        if d['k'] == 'vis':
            chart = CH(name, d['v']['svg'], d['x'], d['y'], d['w'], layers)
            pre.append(chart['base']); continue
        d.update(_name='%s_p%d' % (name, k), _col=0, _hand=None)
        if d['k'] == 't' and not any(p.get('_stem') for p in pre): d['_stem'] = True
        if d['k'] == 'q' and choices: d['choices'] = choices
        pre.append(d)
    return pre, chart


def RPRE(n, paras, name, layers=(), size=23):
    """the 'read the chart' slide of set n (modulesV52b.RD): the explanation / example lines on top, the chart under them"""
    o = MB.RD(n, paras, size=size)
    pre, chart = [], None
    for k, it in enumerate(o['pre']):
        d = dict(it)
        if d['k'] == 'vis':
            chart = CH(name, d['v']['svg'], d['x'], d['y'], d['w'], layers)
            pre.append(chart['base']); continue
        d.update(_name='%s_p%d' % (name, k), _col=0, _hand=None)
        pre.append(d)
    return pre, chart


# ------------------------------------------------------------------------------------------------------- resolving
def _plain(say): return re.sub(r'\s+', ' ', TAG.sub(' ', say)).strip()


CAM_BASE = 'ch52-intro'
CAM_Y = 280          # camera lesson (V4.8): nothing above y 262 may reach the face bubble (x >= 1344)


def _h(it, d):
    if d['k'] == 'vis': return d['h']
    z = d.get('size', 34)
    return int(z * 1.55 * ((1.9 if '/' in it['_hand'] else 1.4) if it.get('_hand') else 1)) + 8


def _layout(vid):
    """item dicts per slide (placed), name -> (slide index, item index); raises on a bad spec."""
    V = VIDEOS[vid]; names = {}; per = []
    cam = bool(re.fullmatch(re.escape(CAM_BASE) + r'(-\d+)?', vid))
    for si, sl in enumerate(V['slides']):
        lesson_title = V['kind'] == 'lesson' and si == 0
        pre = list(sl.get('pre') or [])
        assert not (lesson_title and pre), (vid, 'no board items on the title slide')
        assert V['kind'] == 'lesson' or pre, (vid, si, 'a question slide needs its pre-loaded question (QPRE / RPRE)')
        items = []
        for k, it in enumerate(pre):
            assert it['_name'] not in names, (vid, 'item name used twice', it['_name'])
            names[it['_name']] = (si, k)
        for ln in sl['lines']:
            for c in ln['cues']:
                if c[0] == 'show':
                    it = c[1]
                    assert not lesson_title, (vid, 'no board items on the title slide')
                    assert it['_name'] not in names, (vid, 'item name used twice', it['_name'])
                    names[it['_name']] = (si, len(pre) + len(items)); items.append(it)
        anchor = next((p for p in pre if p.get('_chart')), None) or next((it for it in items if it.get('_chart')), None)
        sol = V['kind'] == 'solution'
        out = []
        if anchor:
            ax, ay, aw, ah = anchor['x'], anchor['y'], anchor['w'], anchor['h']
            rx = int(ax + aw + 24); rw = (1545 if sol else 1585) - rx
            ry = ay if not sol else max(ay, 110)
            if cam and rx + rw > 1335: ry = max(ry, CAM_Y)
            by = ay + ah + 16; bx = ax if not sol else 410
        else:
            rx, rw, ry = 1010, 540, (100 if sol else 78)
        for it in items:
            d = {k: v for k, v in it.items() if not k.startswith('_')}
            if d.get('over') or it.get('_chart'):
                pass
            elif it.get('_x') is not None or it.get('_y') is not None:
                if it.get('_x') is not None: d['x'] = it['_x']
                if it.get('_y') is not None: d['y'] = it['_y']
            elif it['_col'] == 1:
                if d['k'] == 'vis':
                    s = min(1.0, rw / float(d['w'])); d['w'] = round(d['w'] * s); d['h'] = round(d['h'] * s)
                d.update(x=rx, y=int(ry), w=d['w'] if d['k'] == 'vis' else rw)
                ry += _h(it, d) + 10
            elif anchor:
                d.update(x=bx, y=int(by))
                if d['k'] != 'vis': d['w'] = (1130 if not sol else 1130)
                by += _h(it, d) + 10
            elif any(i2['_col'] == 1 for i2 in items) and d['k'] == 't':
                d['w'] = 560
            if cam and d['k'] in ('t', 'hw') and d.get('y') is None and (d.get('w') or 1130) > 920:
                d['w'] = 920                    # V4.8: a flowing line ends left of the bubble
            out.append((it, d))
        per.append((pre, out))
    return names, per


def _target(vid, names, si, t):
    if t == 'stem':
        pre = VIDEOS[vid]['slides'][si].get('pre') or []
        k = next((k for k, p in enumerate(pre) if p.get('_stem')), None)
        assert k is not None, (vid, si, 'POINT on the question, but this slide has no question text')
        return 'item %d' % k
    if re.fullmatch(r'choice \d', t) or t.startswith('fig:'): return t
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
    placed = {id(it): d for pre, sl in per for it, d in sl}
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
            'style': "the teacher reads it herself (Reading Studio), topic-52 scripts (2026-10-21): math_patches/_ai_vis_t52.py is "
                     "the source - edit there and re-run it. Rules: real_exam/TEACHING_STYLE_GUIDE.md R1-R37, W1-W21 (no 'which way is "
                     "better' verdict) + NITZAN_RHYTHM_DELIVERY.md P1-P13. Calm preset on the question reading and plain calculations.",
            'slides': slides}


def write_json(vid):
    p = os.path.join(SB, 'ai_scripts', vid + '.json')
    json.dump(ai_json(vid), open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    return p


def _clean(it):
    return {k: v for k, v in it.items() if not k.startswith('_')}


def studio_slides(vid):
    """beat specs for math_api.MathCourse._beat (spoken lines only; cues + items come from _ai_visual.apply) + sidebar.
    The pre-loaded items (the question, the chart, quoted lines of the chart page) are the slide's own."""
    V = VIDEOS[vid]; lesson = V['kind'] == 'lesson'
    body = V['slides'][1:] if lesson else V['slides']
    sb = list(dict.fromkeys(sl['sb'] for sl in body))
    out = []
    for si, sl in enumerate(V['slides']):
        script = [_plain(ln['say']) for ln in sl['lines']]
        pre = [_clean(p) for p in (sl.get('pre') or [])]
        if lesson and si == 0:
            out.append({'title': sl['title'], 'mode': 'title', 'active': -1, 'pre': [], 'script': script})
        else:
            out.append({'title': sl['title'], 'mode': 'concept' if lesson else 'question', 'active': sb.index(sl['sb']),
                        'pre': pre, 'script': script})
    return out, sb


def rebuild(M, vid):
    """replace the studio video's slides by the spec (spoken lines only); _ai_visual.apply adds cues + items."""
    v = M.video(vid); beats, sb = studio_slides(vid)
    v['beats'] = [M._beat(v, b) for b in beats]
    hy = v.setdefault('hybrid', {}); hy['sidebar'] = sb; hy['subject'] = 'QUANTITATIVE'
    words = sum(len(l['say'].split()) for b in v['beats'] for l in b['lines'] if 'say' in l)
    v['wordCount'] = words; v['minutes'] = round(words / 157.0, 1)
    M.touched_videos.add(vid)


def stats(vid):
    flat = [ln for sl in VIDEOS[vid]['slides'] for ln in sl['lines']]
    words = sum(len(_plain(ln['say']).split()) for ln in flat)
    chars = sum(len(_plain(ln['say'])) for ln in flat)
    cues = sum(len(ln['cues']) for ln in flat)
    return {'words': words, 'chars': chars, 'minutes': round(words / 157.0, 1), 'cues': cues, 'lines': len(flat)}


# ------------------------------------------------------------------------------------------- figures (V1)
def _layers(name, out, w, col):
    items = {}
    base = '%s_%s' % (name, out[0][0])
    for k, sv in out:
        it = NL('%s_%s' % (name, k), sv, w=w, col=col)
        if k != 'line': it['over'] = 1; it['gap'] = 0; LAYER_BASE[it['_name']] = base
        items[k] = it
    return items


_mv_spec = importlib.util.spec_from_file_location('_method_visuals', os.path.join(HERE, '_method_visuals.py'))
MV = importlib.util.module_from_spec(_mv_spec); _mv_spec.loader.exec_module(MV)


def _hand(tex):
    """the hand-written twin of a typed line (studio_handwrite syntax), or None if it has a glyph the pen lacks"""
    t = tex.replace('{,}', ',')                # 2026-10-21 topic 52: a thousands comma (not a pen fraction)
    for a, b in [('\\blacklozenge', '◆'), ('\\times', '×'), ('\\cdot', '·'), ('\\ne', '≠'), ('\\le', '≤'), ('\\ge', '≥'), ('\\to', '→'),
                 ('\\quad', '    '), ('\\qquad', '      '), ('\\ ', ' '), ('\\,', ''), ('\\star', '⋆'), ('\\div', '÷'),
                 ('\\left', ''), ('\\right', ''), ('\\%', '%')]:
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



ORANGE = '#c8641e'
_INK, _TEAL, _LIGHT = MV.INK, MV.TEAL, MV.LIGHT


def _tx(x, y, t, size=28, col=None, anchor='middle'):
    return MV._text(x, y, t, size, col or _INK, anchor)


def TBL(name, head, rowlab, layers, colw=200, labw=190, rowh=74, headh=56, col=0, w=None, side=0, size=34,
        title='Table'):
    """a table: head = the column names, rowlab = the row names ('' = no name column); layers = [(key, [mark, ...])]:
      ('c', r, c, text[, colour])      a cell value (r, c from 0; c counts the value columns only)
      ('q', r, c)                      a teal question mark
      ('cover', r, c, text)            the value found, over the question mark (teal)
      ('across', r, label)             an arrow across row r, from column 0 to column 1, with its label (x 7)
      ('down', c, r1, r2, label)       an arrow down beside column c (the first or the last), from row r1 to r2
      ('diag', (r1, c1), (r2, c2))     the diagonal of the triangle value
      ('box', r, c)                    a teal frame around a cell
    side = an empty margin left and right (for the down arrows)"""
    nr = len(rowlab); haslab = any(rowlab); lw = labw if haslab else 0
    x0 = 10 + side; y0 = 10
    xs = [x0 + lw + k * colw for k in range(len(head) + 1)]
    W = xs[-1] + 10 + side; H = y0 + headh + rowh * nr + 12
    top = lambda r: y0 + headh + rowh * r
    cy = lambda r: top(r) + rowh * .64
    cx = lambda c: (xs[c] + xs[c + 1]) / 2.0
    body = '<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (xs[0], y0, xs[-1] - xs[0], headh, _LIGHT)
    body += ''.join(_tx(cx(k), y0 + headh * .68, h, max(27, size - 2)) for k, h in enumerate(head))   # topic 25: the data sit in the head row
    left = x0 if haslab else xs[0]
    body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4"/>' % (xs[0], y0, xs[-1], y0, _INK)
    for r in range(nr + 1):
        y = top(r)
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s"/>' % (left if r else xs[0], y, xs[-1], y, _INK, 2.4 if r == 0 else 1.6)
    for x in xs:
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>' % (x, y0, x, top(nr), _INK)
    if haslab:
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>' % (x0, top(0), x0, top(nr), _INK)
        body += ''.join(_tx(x0 + lw / 2.0, cy(r), lab, max(26, size - 6)) for r, lab in enumerate(rowlab))
    out = [('line', MV._svg(W, H, body, title + ': ' + ', '.join(head)))]
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'c':
                b += _tx(cx(m[2]), cy(m[1]), m[3], size, m[4] if len(m) > 4 else _INK)
            elif k == 'q':
                b += _tx(cx(m[2]), cy(m[1]), '?', size + 2, _TEAL)
            elif k == 'cover':
                r, c = m[1], m[2]
                b += '<rect x="%.1f" y="%.1f" width="76" height="%.1f" fill="#ffffff"/>' % (cx(c) - 38, top(r) + 6, rowh - 12)
                b += _tx(cx(c), cy(r), m[3], size, _TEAL)
            elif k == 'across':
                r = m[1]; y = top(r) + rowh * .5
                xm = (cx(0) + cx(1)) / 2.0
                b += MV._arrow(cx(0) + 46, y + 6, cx(1) - 46, y + 6)
                b += '<rect x="%.1f" y="%.1f" width="66" height="27" rx="5" fill="#ffffff"/>' % (xm - 33, y - 25)
                b += _tx(xm, y - 3, m[2], 28, _TEAL)
            elif k == 'down':
                c, r1, r2 = m[1], m[2], m[3]
                y1, y2 = top(r1) + rowh * .32, top(r2) + rowh * .68
                if c == 0:
                    x = xs[0] - 20 - (lw if haslab else 0)
                    b += MV._arrow(x, y1, x, y2) + _tx(x - 10, (y1 + y2) / 2.0 + 10, m[4], 30, _TEAL, 'end')
                else:
                    x = xs[-1] + 20
                    b += MV._arrow(x, y1, x, y2) + _tx(x + 10, (y1 + y2) / 2.0 + 10, m[4], 30, _TEAL, 'start')
            elif k == 'diag':
                (r1, c1), (r2, c2) = m[1], m[2]
                x1, ya, x2, yb = cx(c1), top(r1) + rowh * .5, cx(c2), top(r2) + rowh * .5
                b += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3.2" stroke-linecap="round"/>'
                      % (x1 + (x2 - x1) * .22, ya + (yb - ya) * .22, x1 + (x2 - x1) * .78, ya + (yb - ya) * .78, _TEAL))
            elif k == 'box':
                r, c = m[1], m[2]
                b += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="none" stroke="%s" stroke-width="3"/>'
                      % (xs[c] + 5, top(r) + 5, colw - 10, rowh - 10, _TEAL))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)



def _ml(x, y, t, size=22, col=None, anchor='middle'):
    """text with '\\n' = a second line (each line its own <text>)"""
    parts = t.split('\n'); out = ''
    for k, p in enumerate(parts):
        out += _tx(x, y + (k - (len(parts) - 1) / 2.0) * size * 1.08, p, size, col, anchor)
    return out



def STRIP(name, lb, la, layers, col=0, w=None, title='The squares method'):
    """the squares method: boxes 0..3 = neither | lb only | both | la only (left to right).
      lb = the group whose bracket is drawn OVER boxes 1-2, la = the group whose bracket is UNDER boxes 2-3.
    layers = [(key, [mark, ...])]:
      ('B', text)               the bracket over boxes 1-2 (lb's group), with its value
      ('A', text)               the bracket under boxes 2-3 (la's group), with its value
      ('T', text)               the total: a long bracket under all four boxes
      ('top', i0, i1, text)     a second bracket above, over boxes i0..i1-1 (e.g. "not morning")
      ('v', i, text)            a value in box i
      ('q', i)                  a teal question mark in box i
      ('hl', i0, i1)            a thick teal frame around boxes i0..i1-1 (what we look at)"""
    W, H = 620, 330; x0, bw = 10, 150; yh, ybx, bh = 100, 146, 76
    X = lambda i: x0 + i * bw
    names = ['neither', lb + '\nonly', 'both', la + '\nonly']
    body = ''.join('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="2.4"/>'
                   % (X(i), yh, bw, ybx - yh, LIGHTH if i == 2 else '#ffffff', _INK) for i in range(4))
    body += ''.join('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="2.4"/>'
                    % (X(i), ybx, bw, bh, _INK) for i in range(4))
    body += ''.join(_ml(X(i) + bw / 2.0, (yh + ybx) / 2.0 + 7, t.replace('\nonly', ' only') if len(t) < 11 else t, 23 if len(t) < 11 else 21)
                    for i, t in enumerate(names))
    out = [('line', MV._svg(W, H, body, '%s: neither, %s only, both, %s only' % (title, lb, la)))]

    def br(i0, i1, y, up, lab, colr):
        xa, xb = X(i0) + 8, X(i1) - 8; dd = -12 if up else 12
        return ('<path d="M %d %d L %d %d L %d %d L %d %d" fill="none" stroke="%s" stroke-width="2.8"/>'
                % (xa, y - dd, xa, y, xb, y, xb, y - dd, colr) + _tx((xa + xb) / 2.0, y - 9 if up else y + 29, lab, 27, colr))
    for key, marks in layers:
        b = ''
        for m in marks:
            k = m[0]
            if k == 'B': b += br(1, 3, yh - 18, True, m[1], _TEAL)
            elif k == 'A': b += br(2, 4, ybx + bh + 14, False, m[1], _BLUE)
            elif k == 'T': b += br(0, 4, ybx + bh + 66, False, m[1], _INK)
            elif k == 'top':
                b += br(m[1], m[2], yh - 58, True, m[3], ORANGE)
            elif k == 'v':
                b += _tx(X(m[1]) + bw / 2.0, ybx + bh * .68, m[2], 40 if len(m[2]) < 5 else 32, _TEAL)
            elif k == 'q':
                b += _tx(X(m[1]) + bw / 2.0, ybx + bh * .68, '?', 40, _TEAL)
            elif k == 'hl':
                b += ('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="none" stroke="%s" stroke-width="5"/>'
                      % (X(m[1]) + 3, yh + 3, (m[2] - m[1]) * bw - 6, ybx + bh - yh - 6, ORANGE))
        out.append((key, MV._svg(W, H, b, '%s: %s' % (title, key))))
    return MV.items(_layers, name, out, w=w, col=col, own=True)


LIGHTH = MV.LIGHT


CARRY52 = {}      # vid -> carry-over ("So far") boxes, _method_visuals.carry format
SPLITS = []       # lessons split into parts (not on camera)
PAGE = MA.set_page()
LX, LY, LW = 345, 92, 740        # a chart on the left of a lesson slide


def PAGE_CH(name, hl):
    return CH(name, PAGE, LX, LY, LW, [('hl', MA.set_page(hl))])


# =================================================================================================================
# ch52-intro (camera lesson, three parts)
# Hebrew (charts seg01, all of it): a chart or a table, then 4-5 questions; 5-6 minutes, a minute or a minute and a half
# on the chart first; the skill tested; "any chart can come" is wrong, very specific types, ~95%; the instructions say
# nothing; the explanation, the example at its end (almost always) - the most important line: check it in the chart; not
# clear -> read again slowly, still not -> leave the set and come back; titles, units (thousands, hundreds, percent),
# notes; the questions easy -> hard, the first pulls one value; table vs chart (rows x columns; Excel's "insert chart");
# the set's place = its difficulty, "always skip the chart" is a mistake (80% vs 85%); charts are accurate (unlike
# geometry): solve by eye; a table holds a lot of data (ages: siblings 2.3 / 2.8 / 3.6, children, friends, salary,
# rooms), a chart shows the trend at a glance; the simulation curves (big at first then flat; flat then steep from the
# 4th-5th; flat until 7-9) and the real one. ADDED for the camera lesson (2-3 examples per idea): the example checked on
# a real bar chart (2010 -> 60, a second sentence for 2013 -> 100), the units with two cases (90 thousand, 40 percent),
# a first question answered like the example (2011 -> 80 thousand), the row-and-column cross (31-40 siblings -> 2.8,
# 21-30 salary -> 6,200), the trend read from the table (salary up, friends down). NEW (all). The chart data are the
# course's own renderings (modulesV52a.py, the same data as the Hebrew lesson).
# =================================================================================================================
i_p1 = PAGE_CH('i_p1', 'qs')
i_n1 = I('i_n1', 'A chart or a table, then $4$ or $5$ questions', size=28, col=1)
i_n2 = I('i_n2', 'About $5$ to $6$ minutes for the set', size=28, col=1)
i_n3 = I('i_n3', 'First $1$ to $1\\frac{1}{2}$ minutes: understand the chart', size=28, col=1)
i_n4 = I('i_n4', 'The skill: understand data and draw conclusions', size=28, col=1)
i_m0 = CH('i_m0', MA.chart_menu(), 345, 92, 830)
i_m1 = I('i_m1', 'A few very specific types of charts', size=30)
i_m2 = I('i_m2', 'About $95\\%$ of the sets: the types in these lessons', size=30)
i_p2 = PAGE_CH('i_p2', 'instr')
i_n5 = I('i_n5', 'No special instructions: read the chart, answer the questions', size=28, col=1)
i_p3 = CH('i_p3', PAGE, LX, LY, LW, [('ex', MA.set_page('expl')), ('ex2', MA.set_page('example'))])
i_n6 = I('i_n6', 'The explanation: what the chart describes', size=28, col=1)
i_n7 = I('i_n7', 'At its end: an example (almost always)', size=28, col=1)
BAR1 = MA.car_bar(n=1)
i_b1 = CH('i_b1', BAR1, LX, LY, LW, [('g60', MA.car_bar(n=1, marks=[('guide', 0, 60, '60')])),
                                     ('g100', MA.car_bar(n=1, marks=[('guide', 0, 60, '60'), ('guide', 3, 100, '100')]))])
i_e1 = I('i_e1', '"For example: in 2010, 60 thousand vehicles were sold."', size=26, col=1)
i_e2 = I('i_e2', '$2010$: $\\ 60$ on a thousands axis $= 60{,}000$', size=28, col=1)
i_e3 = I('i_e3', 'It matches: we understand the chart', size=28, col=1)
i_e4 = I('i_e4', 'Our own check: $\\ 2013$, $\\ 100$ thousand', size=28, col=1)
i_p4 = PAGE_CH('i_p4', 'example')
i_c1 = I('i_c1', "The example doesn't match? Stop", size=28, col=1)
i_c2 = I('i_c2', 'Read the explanation again, slowly, line by line', size=28, col=1)
i_c3 = I('i_c3', 'Still not clear? Leave the set and come back at the end', size=28, col=1)
i_p5 = PAGE_CH('i_p5', 'units')
i_u1 = I('i_u1', '$90$ on a thousands axis $= 90{,}000$', size=28, col=1)
i_u2 = I('i_u2', '$40$ on a percent axis $= 40\\%$', size=28, col=1)
i_u3 = I('i_u3', 'Read every note: it is there for a reason', size=28, col=1)
i_p6 = PAGE_CH('i_p6', 'qs')
i_q1 = I('i_q1', 'From easy to hard: the last one is the hardest', size=28, col=1)
i_q2 = I('i_q2', 'The first question: usually pull out one value', size=28, col=1)
i_q3 = I('i_q3', 'Later questions: a calculation, or deeper understanding', size=28, col=1)
i_p7 = PAGE_CH('i_p7', 'chart')
i_d1 = I('i_d1', 'At the start of the section: easy. $\\ $At the end: hard', size=28, col=1)
i_d2 = I('i_d2', 'Other first questions: $80\\%$ right. $\\ $The chart: about $85\\%$', size=28, col=1)
i_d3 = I('i_d3', 'An early chart: solve it when you reach it', size=28, col=1)
i_d4 = I('i_d4', 'A chart at the end: you reach it last anyway', size=28, col=1)
i_t0 = CH('i_t0', MA.sib_table(2), LX, LY, 520, [('c', MA.sib_table(2, highlight=[(1, 1)]))])
i_t1 = I('i_t1', 'A table: rows and columns', size=28, col=1)
i_t2 = I('i_t2', 'Row $31$–$40$, column siblings: $\\ 2.8$', size=28, col=1)
i_t3 = I('i_t3', 'A chart: the same data as a picture', size=28, col=1)
i_m3 = CH('i_m3', MA.chart_menu(), 345, 92, 830)
i_m4 = I('i_m4', 'We choose the chart that shows our data best', size=30)
SIM_A = MA.sim_chart(MA.SIM_A)
i_s0 = CH('i_s0', SIM_A, LX, LY, LW, [('a', MA.sim_chart(MA.SIM_A, marks=[('col', 1, 5)])),
                                      ('b', MA.sim_chart(MA.SIM_A, marks=[('col', 1, 5), ('col', 8, 15)]))])
i_a1 = I('i_a1', 'Charts: use the scale, units and any axis break', size=28, col=1)
i_a2 = I('i_a2', 'Same axes and time interval: steeper means a bigger change', size=28, col=1)
i_a3 = I('i_a3', 'Tests $1$ to $5$: steep, a big improvement', size=28, col=1)
i_a4 = I('i_a4', 'From test $8$: almost flat', size=28, col=1)
SIB6 = MA.sib_table(6)
i_t4 = CH('i_t4', SIB6, 345, 92, 1000, [('sal', MA.sib_table(6, highlight=[(0, 4)]))])
i_t5 = I('i_t5', 'A table can hold a lot of data. $\\ $We read only what we need.', size=30)
i_t6 = I('i_t6', 'So much data in a chart: too many lines, a mess', size=30)
i_t7 = CH('i_t7', SIB6, 345, 92, 1000, [('sal', MA.sib_table(6, hl_cols=[4])), ('fr', MA.sib_table(6, hl_cols=[4, 3]))])
i_t8 = I('i_t8', 'Salary: $\\ 6{,}200,\\ 8{,}300,\\ 10{,}100$, $\\ $up', size=30)
i_t9 = I('i_t9', 'Friends: $\\ 12,\\ 9,\\ 7$, $\\ $down', size=30)
i_t10 = I('i_t10', 'A chart shows a trend in one look', size=30)
SIM_B = MA.sim_chart(MA.SIM_B, extra=MA.SIM_C)
i_s1 = CH('i_s1', SIM_B, LX, LY, LW, [('a', MA.sim_chart(MA.SIM_B, extra=MA.SIM_C, marks=[('col', 5, 8)])),
                                      ('b', MA.sim_chart(MA.SIM_B, extra=MA.SIM_C, marks=[('col', 5, 8), ('col', 10, 15)]))])
i_b2 = I('i_b2', 'Tests $5$ to $8$: steep, a big improvement', size=28, col=1)
i_b3 = I('i_b3', 'From test $10$: flat again', size=28, col=1)
i_b4 = I('i_b4', 'Dashed: almost nothing until test $9$, then a sharp rise', size=28, col=1)
i_b5 = I('i_b5', 'Most students: the big jump comes from about the $4$th or $5$th test', size=28, col=1)

video('ch52-intro', 'lesson', slides=[
    S('Charts & Tables',
      L("Welcome back, and now a new topic, charts and tables."),
      L("Every quantitative section has one chart or one table, with a few questions about it. Once we know how to read "
        "the page, these questions can be quick points.")),
    S('The chart set',
      L("Here's what a chart set looks like on the exam. First comes a chart or a table. After it come four or five "
        "questions about it.", show(i_p1['hl'], 'After it come four or five'), show(i_n1, 'four or five questions')),
      L("How much time should we give the set? About five to six minutes. That's a bit more than a minute for each "
        "question.", show(i_n2, 'About five to six minutes')),
      L("And here's the important part. We start with the chart, not with the questions. We spend a minute, or a minute "
        "and a half, just understanding the chart.", show(i_n3, 'We spend a minute')),
      L("Why? Because every question uses the same chart. Once we understand it, every question gets easier."),
      L("What do these questions test? One skill. Can we understand data, and draw conclusions from it?",
        show(i_n4, 'Can we understand data')),
      L("The data can come in a table, or in a few kinds of charts."), pre=[i_p1['base']]),
    S('Specific types',
      L("Many students think that any kind of chart can show up. So they feel there's no way to prepare."),
      L("That's not true. The exam uses a few very specific types of charts.", show(i_m1, 'a few very specific types')),
      L("We'll go through all of them in the next lessons. A table, points, lines, bars, and a few more."),
      L("Once in a few years, a really different chart shows up. But that's very rare."),
      L("In about ninety-five percent of the sets, the chart is one of the types we learn here.",
        show(i_m2, 'In about ninety-five percent')), pre=[i_m0['base']]),
    S('The instructions',
      L("Now let's go over the page itself, from the top. At the top there's one line of instructions.",
        show(i_p2['hl'], 'one line of instructions')),
      L("It says, study the chart below, then answer the questions that follow."),
      L("So really, there are no special instructions. We read the chart, and we answer the questions.",
        show(i_n5, 'there are no special instructions')), pre=[i_p2['base']]),
    S('The explanation',
      L("Under it there's a short explanation. It tells us what the chart describes.", show(i_p3['ex'], 'a short explanation'),
        show(i_n6, 'It tells us what the chart describes')),
      L("For example, the chart describes the vehicles sold in the years two thousand ten to two thousand thirteen."),
      L("At the end of the explanation there's almost always an example.", show(i_p3['ex2'], 'almost always an example'),
        show(i_n7, 'almost always an example')),
      L("Sometimes there's no example, but that's rare. And when there is one, it's the most important line on the page."),
      pre=[i_p3['base']]),
    S('The example',
      L("Why is the example so important? Because it lets us check ourselves."),
      L("We read the example. Then we find the same thing in the chart. If we see exactly what the example says, we "
        "understand the chart."),
      L("Let's try it on this bar chart. The example says, in two thousand ten, sixty thousand vehicles were sold.",
        show(i_e1, 'The example says')),
      L("So we go to two thousand ten, at the bottom. We go up to the top of its bar, and across to the axis. We get to sixty.",
        show(i_b1['g60'], 'We go up to the top')),
      L("And the axis says thousands, at the top. So sixty means sixty thousand.", pt('fig: Thousands', 'the axis says thousands'),
        show(i_e2, 'So sixty means sixty thousand')),
      L("It matches the example, so we understand the chart.", show(i_e3, 'It matches the example')),
      L("Let's check one more sentence, of our own. In two thousand thirteen, a hundred thousand vehicles were sold.",
        show(i_e4, 'of our own')),
      L("We go to two thousand thirteen, up to its bar, and across. We get to a hundred, so a hundred thousand. It matches again.",
        show(i_b1['g100'], 'up to its bar, and across')),
      L("And if it didn't match? Then our reading is wrong somewhere. Maybe we read the wrong axis, or we missed the units."),
      pre=[i_b1['base']]),
    S('If it is not clear',
      L("So what do we do when the example doesn't match what we see?", show(i_p4['hl'], "the example doesn't match")),
      L("We stop. We don't go on to the questions yet, because if we don't understand the example, we don't understand "
        "the chart.", show(i_c1, 'We stop')),
      L("We read the explanation again, slowly, line by line. Then we check the example again.",
        show(i_c2, 'We read the explanation again')),
      L("Now it's clear? Excellent, we go to the questions."),
      L("Still not clear? Then we leave the set for now. We solve the rest of the section, and we come back to the chart at "
        "the end.", show(i_c3, 'Still not clear')),
      L("That way we don't waste time on questions about a chart we don't understand."), pre=[i_p4['base']]),
    S('Titles, units, notes',
      L("Now the chart itself. We look at its title, and at the units on the axes.", show(i_p5['hl'], 'the units on the axes')),
      L("Is the number in thousands, in hundreds, or in percent? For example, ninety on a thousands axis means ninety "
        "thousand.", show(i_u1, 'ninety on a thousands axis')),
      L("And forty on a percent axis means forty percent. It's not forty people.", show(i_u2, 'forty on a percent axis')),
      L("Then we read every note under the chart. A note is there for a reason. Without it, something won't add up.",
        show(i_u3, 'A note is there for a reason')), pre=[i_p5['base']]),
    S('The questions',
      L("After the chart come the questions. They go from easy to hard.", show(i_p6['hl'], 'After the chart come the questions')),
      L("So the first question is the easiest, and the last is the hardest. The last one can be harder, or just longer to "
        "calculate.", show(i_q1, 'the last is the hardest')),
      L("The first question usually checks one thing. Do we understand the chart? It asks us to pull out one value.",
        show(i_q2, 'pull out one value')),
      L("For example, how many vehicles were sold in two thousand eleven? We read eighty thousand, and that's it."),
      L("The later questions go further. Some need a calculation, and some need a deeper understanding of the chart.",
        show(i_q3, 'The later questions go further')), pre=[i_p6['base']]),
    S('Its place in the section',
      L("The chart set has a place in the section too. And its place tells us how hard it is.",
        show(i_p7['hl'], 'its place tells us')),
      L("A set at the start of the section is easy. A set at the end is hard.", show(i_d1, 'A set at the start')),
      L("You may hear this advice, always skip the chart, and come back to it at the end. That's a mistake."),
      L("Here's why. A chart at the start is not only easy. It's usually easier than the other questions around it."),
      L("Let's say students answer eighty percent of the first questions right. Then they answer about eighty-five percent "
        "of the chart questions right.", show(i_d2, 'Let\'s say students answer')),
      L("So a chart at the start, or in the middle, we solve when we get to it.", show(i_d3, 'or in the middle')),
      L("A chart at the end, we reach at the end anyway. So there's nothing to skip.", show(i_d4, 'A chart at the end')),
      L("If charts are really hard for you, you may choose to skip them. But for most students, an early chart is worth "
        "solving."), pre=[i_p7['base']]),
    S('Table or chart?',
      L("What's the difference between a table and a chart? A table puts related data together, in rows and columns.",
        show(i_t1, 'in rows and columns')),
      L("We find a value where a row and a column cross. Let's take the row thirty-one to forty, and the siblings column.",
        pt('i_t0', 'the row thirty-one to forty')),
      L("They cross at two point eight. So people aged thirty-one to forty have two point eight siblings, on average.",
        show(i_t0['c'], 'They cross at two point eight'), show(i_t2, 'two point eight siblings')),
      L("A chart shows the same kind of data as a picture.", show(i_t3, 'as a picture')), pre=[i_t0['base']]),
    S('Insert chart',
      L("Think of Excel. We type the data into a table, and we click insert chart."),
      L("Excel asks which kind of chart we want. Columns, a line, a pie, and more."),
      L("We choose the chart that shows our data best. Different charts help us see different things. We'll see that in "
        "the next lessons.", show(i_m4, 'We choose the chart')), pre=[i_m3['base']]),
    S('Charts are accurate',
      L("Here's an important difference from geometry. In geometry, a figure is not necessarily drawn to scale."),
      L("In charts, we can read values from the drawing. But first, check the scale, the units, and any break in the axis.",
        show(i_a1, 'check the scale')),
      L("Often the fastest way is just to look. On the same axes, over the same time interval, a steeper line means a bigger change.",
        show(i_a2, 'a steeper line means')),
      L("Let's see it on this chart. It shows a score, by the number of full practice tests a student did."),
      L("At the start the line is very steep. From the first test to the fifth, the score jumps a lot.",
        show(i_s0['a'], 'From the first test to the fifth'), show(i_a3, 'the score jumps a lot')),
      L("From about the eighth test, the line is almost flat. So the score hardly goes up any more.",
        show(i_s0['b'], 'From about the eighth test'), show(i_a4, 'the line is almost flat')),
      L("We saw all of this in one look, with no calculation."), pre=[i_s0['base']]),
    S('Table: a lot of data',
      L("So when is a table better? A table can hold a lot of data about the same groups."),
      L("Here are the same three age groups. Now we also have children, friends, salary, and rooms at home."),
      L("If a question needs one value, we just find it. At ages twenty-one to thirty, the salary is six thousand two "
        "hundred shekels.", show(i_t4['sal'], 'the salary is six thousand')),
      L("The other columns don't bother us. We just ignore them.", show(i_t5, "The other columns don't bother us")),
      L("In a chart, so much data would be a mess. Too many lines or bars, and we can't see anything.",
        show(i_t6, 'would be a mess')), pre=[i_t4['base']]),
    S('Chart: the trend',
      L("But a table has a weak point. To see a trend, we must read every number."),
      L("Look at the salary. Six thousand two hundred, then eight thousand three hundred, then ten thousand one hundred. "
        "It goes up with age.", show(i_t7['sal'], 'Look at the salary'), show(i_t8, 'It goes up with age')),
      L("And the friends go down. Twelve, nine, seven.", show(i_t7['fr'], 'And the friends go down'),
        show(i_t9, 'Twelve, nine, seven')),
      L("We had to read six numbers to see that. In a chart, we'd see one line going up and one going down, right away.",
        show(i_t10, 'right away')), pre=[i_t7['base']]),
    S('Another student',
      L("Now back to the practice tests. Here's another student. At the start the line is almost flat, so there's almost "
        "no improvement."),
      L("From the fifth test the line gets steep. From five to six, six to seven, seven to eight, the score goes up a lot.",
        show(i_s1['a'], 'From the fifth test'), show(i_b2, 'the score goes up a lot')),
      L("Steeper means a bigger improvement. And from about the tenth test, it's flat again.",
        show(i_s1['b'], 'from about the tenth test'), show(i_b3, "it's flat again")),
      L("The dashed line is a third student. Almost nothing until the ninth test, and only then a sharp rise.",
        show(i_b4, 'The dashed line')),
      L("By the way, the second student is the real picture for most of us. If your first practice tests don't improve, "
        "don't worry."),
      L("The big jump usually comes from about the fourth or fifth test. Then the score levels off.",
        show(i_b5, 'The big jump usually comes')),
      L("That's it for the introduction. In the next lessons we'll go through each type of chart. I'll see you in the next "
        "video."), pre=[i_s1['base']]),
])
CAMERA_SPLIT = ('ch52-intro', 'Charts & Tables', [
    (1, None),
    (6, "Let's continue with the chart page."),
    (10, "Let's continue with tables and charts.")])


# =================================================================================================================
# ch52-tables (lesson, two parts, not on camera)
# Hebrew (seg02, all of it): the car table (year, vehicles sold; example 2010 -> 60 thousand), more columns: private cars
# ("of them" = of all the vehicles sold: 45 of the 60), privately owned (a private person or a company), commercial vehicles
# that are privately owned; chart and table questions bring in every problem type; the average (60 + 80 + 80 + 100) / 4 =
# 80 and the symmetric shortcut (gaps 20, 0, 20); the percent question (after "of" comes the whole: 40/60 = 2/3, 50/80 =
# 5/8 = 62.5%, the eighths, 65/100); the overlap question in squares (45, 40, 4 -> 36 -> 9 thousand). The Hebrew says
# "learn this topic after all the other problem types": in our plan charts come after percents (23), overlap (24) and
# averages (25), so they are REMINDERS here (short), said "like in the averages lesson"; work and motion come later, so
# they are not named. ADDED: why "of them" is a part, the steps of each calculation said aloud, the four squares as a
# table (her "this square belongs to commercial and private ownership"). The chart data are the course's own.
# =================================================================================================================
CT2, CT3, CT5 = MA.car_table(2), MA.car_table(3), MA.car_table(5)
t_c2 = CH('t_c2', CT2, 345, 92, 600, [('a', MA.car_table(2, highlight=[(0, 1)]))])
t_n1 = I('t_n1', '$2010$ row, vehicles sold column: $\\ 60$', size=30, col=1)
t_n2 = I('t_n2', '$60$ thousand: it matches the example', size=30, col=1)
t_c3 = CH('t_c3', CT3, 345, 92, 760, [('a', MA.car_table(3, highlight=[(0, 1), (0, 2)]))])
t_n3 = I('t_n3', 'Of them $=$ of all the vehicles sold', size=30, col=1)
t_n4 = I('t_n4', '$45$ is a part of the $60$', size=30, col=1)
t_c5 = CH('t_c5', CT5, 345, 92, 1000, [('a', MA.car_table(5, highlight=[(0, 3)])), ('b', MA.car_table(5, highlight=[(0, 3), (0, 4)]))])
t_n5 = I('t_n5', 'Privately owned: a private person owns it', size=30)
t_n6 = I('t_n6', 'Commercial, privately owned: a van that a private person owns', size=30)
t_c6 = CH('t_c6', CT5, 345, 92, 1000)
t_n7 = I('t_n7', 'Inside a table: percents, averages, overlap, and more', size=30)
t_n8 = I('t_n8', 'We use the tools we already know', size=30)
t_c7 = CH('t_c7', CT5, 345, 92, 760, [('a', MA.car_table(5, hl_cols=[1]))])
t_q1 = I('t_q1', 'What is the average number of vehicles sold per year?', size=30)
t_a1 = IH('t_a1', '$60+80=140$', size=30, col=1)
t_a2 = IH('t_a2', '$140+80=220$', size=30, col=1)
t_a3 = IH('t_a3', '$220+100=320$', size=30, col=1)
t_a4 = IH('t_a4', '$320\\div4=80$', size=30, col=1)
t_c8 = CH('t_c8', CT5, 345, 92, 760, [('a', MA.car_table(5, hl_cols=[1]))])
t_s1 = IH('t_s1', '$60$ to $80$: $\\ 20$', size=30, col=1)
t_s2 = IH('t_s2', '$80$ to $80$: $\\ 0$', size=30, col=1)
t_s3 = IH('t_s3', '$80$ to $100$: $\\ 20$', size=30, col=1)
t_s4 = I('t_s4', 'Symmetric numbers: $\\ $the average is the middle, $80$', size=30)
# part 2
t_c9 = CH('t_c9', CT5, 345, 92, 760, [('a', MA.car_table(5, hl_cols=[1, 3]))])
t_q2 = I('t_q2', 'What percent of the vehicles sold were privately owned?', size=30)
t_w1 = I('t_w1', 'Of the vehicles sold: $\\ $they are the whole, $100\\%$', size=30)
t_p1 = IH('t_p1', '$2010$: $\\ \\frac{40}{60}=\\frac{2}{3}$', size=30, col=1)
t_p2 = IH('t_p2', '$\\frac{2}{3}=66\\frac{2}{3}\\%$', size=30, col=1)
t_p3 = IH('t_p3', '$2011$: $\\ \\frac{50}{80}=\\frac{5}{8}$', size=30, col=1)
t_c10 = CH('t_c10', CT5, 345, 92, 760, [('a', MA.car_table(5, hl_cols=[1, 3]))])
t_e1 = IH('t_e1', '$\\frac{1}{4}=25\\%$', size=30, col=1)
t_e2 = IH('t_e2', '$\\frac{1}{8}=12.5\\%$', size=30, col=1)
t_e3 = IH('t_e3', '$5\\cdot12.5=62.5$', size=30, col=1)
t_e4 = IH('t_e4', '$2012$: $\\ 62.5\\%$', size=30, col=1)
t_e5 = IH('t_e5', '$2013$: $\\ \\frac{65}{100}=65\\%$', size=30, col=1)
t_c11 = CH('t_c11', CT5, 345, 92, 820, [('a', MA.car_table(5, highlight=[(0, 1), (0, 2), (0, 3), (0, 4)]))])
t_q3 = I('t_q3', 'In $2010$, how many private cars were owned by a company?', size=28, col=1)
t_sq = TBL('t_sq', ['Privately owned', 'Company owned', 'Total'], ['Private car', 'Commercial', 'Total'], [
    ('r', [('c', 0, 2, '45')]), ('k', [('c', 2, 0, '40')]), ('t', [('c', 2, 2, '60')]), ('f', [('c', 1, 0, '4')]),
    ('x', [('c', 0, 0, '36', _TEAL)]), ('y', [('c', 0, 1, '9', _TEAL)])],
    colw=250, labw=210, rowh=64, size=30, w=700, title='The four squares, 2010 (thousands)')
for _k, _it in t_sq.items():
    if _k == 'line': _it.update(_x=345, _y=420)
t_o1 = IH('t_o1', '$40-4=36$', size=30, col=1)
t_o2 = IH('t_o2', '$45-36=9$', size=30, col=1)
t_o3 = I('t_o3', '$9{,}000$ private cars owned by a company', size=28, col=1)
video('ch52-tables', 'lesson', slides=[
    S('Tables',
      L("Welcome back. Let's start with the first type, the table."),
      L("A table is the simplest type. We find a value where a row and a column cross.")),
    S('The car table',
      L("Here's an example. The table describes the new vehicles sold in Israel, in the years two thousand ten to two thousand "
        "thirteen."),
      L("Here's the year, and here's the number of vehicles sold. And the title says thousands."),
      L("The example says, in two thousand ten, sixty thousand new vehicles were sold. Let's check it."),
      L("We take the two thousand ten row, and the vehicles sold column. They cross at sixty.", show(t_c2['a'], 'They cross at sixty'),
        show(t_n1, 'They cross at sixty')),
      L("The title says thousands, so it's sixty thousand. It matches the example.", show(t_n2, 'It matches the example')),
      pre=[t_c2['base']]),
    S('Of them',
      L("Now we add a column, private cars. How many of the vehicles sold were private cars?"),
      L("What does of them mean? It means of all the vehicles sold.", show(t_n3, 'of all the vehicles sold')),
      L("In two thousand ten, sixty thousand vehicles were sold. Of them, forty-five thousand were private cars.",
        show(t_c3['a'], 'Of them, forty-five thousand')),
      L("So the forty-five is a part of the sixty. They are not more vehicles on top of the sixty.",
        show(t_n4, 'a part of the sixty')), pre=[t_c3['base']]),
    S('Who owns it?',
      L("Now two more columns. They are about the owner. A vehicle can be owned by a private person, or by a company."),
      L("Privately owned means a private person owns it. In two thousand ten, forty thousand vehicles were privately owned.",
        show(t_c5['a'], 'forty thousand vehicles'), show(t_n5, 'Privately owned means')),
      L("The last column is commercial vehicles that a private person owns. A van, for example. In two thousand ten, there were "
        "four thousand.", show(t_c5['b'], 'there were four thousand'), show(t_n6, 'A van, for example')),
      L("So now the table has five columns. A question usually asks about one or two of them."), pre=[t_c5['base']]),
    S('Other topics inside',
      L("Table and chart questions can bring in other topics. Percents, averages, overlap, and more.",
        show(t_n7, 'Percents, averages, overlap')),
      L("The good news is that we already know these topics. So inside a table, we use the same tools.",
        show(t_n8, 'we use the same tools')),
      L("Let's see three examples on this table."), pre=[t_c6['base']]),
    S('An average',
      L("The first one. What is the average number of vehicles sold per year?", show(t_q1, 'What is the average number')),
      L("The vehicles sold column has four years. Sixty, eighty, eighty and a hundred.", show(t_c7['a'], 'The vehicles sold column')),
      L("Remember, the average is the sum divided by how many numbers there are. So first the sum."),
      L("Sixty plus eighty is a hundred forty.", show(t_a1, 'Sixty plus eighty')),
      L("A hundred forty plus eighty is two hundred twenty.", show(t_a2, 'A hundred forty plus eighty')),
      L("And two hundred twenty plus a hundred is three hundred twenty.", show(t_a3, 'two hundred twenty plus a hundred')),
      L("There are four years, so we divide by four. Three hundred twenty divided by four is eighty.",
        show(t_a4, 'Three hundred twenty divided by four')),
      L("So the average is eighty thousand vehicles a year."), pre=[t_c7['base']]),
    S('The symmetric shortcut',
      L("Did we need that calculation? Not really. Remember from averages, when numbers are symmetric, the average is the "
        "middle.", show(t_c8['a'], 'when numbers are symmetric')),
      L("Let's check the steps. From sixty to eighty is twenty.", show(t_s1, 'From sixty to eighty')),
      L("From eighty to eighty is zero.", show(t_s2, 'From eighty to eighty')),
      L("And from eighty to a hundred is twenty again.", show(t_s3, 'from eighty to a hundred')),
      L("The steps from both ends are the same, so the numbers are symmetric around eighty. The average is the middle, "
        "eighty, with no calculation.", show(t_s4, 'The average is the middle')), pre=[t_c8['base']]),
    S('A percent question',
      L("Now a percent question. What percent of the vehicles sold were privately owned?", show(t_q2, 'What percent of the')),
      L("First, who is the whole? Remember, what comes after of is the whole. Here it's of the vehicles sold.",
        show(t_c9['a'], "Here it's of the vehicles sold")),
      L("So the vehicles sold are a hundred percent. The privately owned vehicles are the part.",
        show(t_w1, 'the vehicles sold are a hundred percent')),
      L("Two thousand ten. Forty thousand were privately owned, out of sixty thousand. Forty over sixty is two thirds.",
        show(t_p1, 'Forty over sixty')),
      L("And two thirds is sixty-six and two thirds percent.", show(t_p2, 'sixty-six and two thirds percent')),
      L("Two thousand eleven. Fifty out of eighty. We divide the top and the bottom by ten, and we get five eighths.",
        show(t_p3, 'we get five eighths')), pre=[t_c9['base']]),
    S('The eighths',
      L("How much is five eighths in percent? Remember, a quarter is twenty-five percent.", show(t_c10['a'], 'Remember, a quarter'),
        show(t_e1, 'a quarter is twenty-five')),
      L("An eighth is half of a quarter. Half of twenty-five is twelve and a half. So an eighth is twelve and a half "
        "percent.", show(t_e2, 'So an eighth is twelve')),
      L("Five eighths is five times twelve and a half. Five times twelve is sixty, and five halves are two and a half. So "
        "it's sixty-two and a half percent.", show(t_e3, 'Five eighths is five times')),
      L("Two thousand twelve is the same, fifty out of eighty. Sixty-two and a half percent again.", show(t_e4, 'Two thousand twelve is the same')),
      L("And two thousand thirteen is sixty-five out of a hundred. That's simply sixty-five percent.",
        show(t_e5, 'sixty-five out of a hundred')), pre=[t_c10['base']]),
    S('An overlap question',
      L("Now overlap. In two thousand ten, how many private cars were owned by a company?", show(t_q3, 'how many private cars')),
      L("We can split the vehicles in two ways. By the type, a private car or a commercial vehicle. And by the owner, a "
        "private person or a company.", show(t_c11['a'], 'We can split the vehicles')),
      L("So every vehicle sits in one of four squares, like in the squares method.", show(t_sq['line'], 'one of four squares')),
      L("Let's fill in the squares from the table. Private cars, forty-five thousand. That's the whole private car row.",
        show(t_sq['r'], 'Private cars, forty-five')),
      L("Privately owned, forty thousand. That's the whole privately owned column.", show(t_sq['k'], 'Privately owned, forty')),
      L("And all the vehicles together, sixty thousand.", show(t_sq['t'], 'all the vehicles together')),
      L("Commercial vehicles that are privately owned, four thousand. That's one square, commercial and privately owned.",
        show(t_sq['f'], "That's one square")),
      L("Now we use the column total. The privately owned column is forty, and four of them are commercial. Forty minus four is "
        "thirty-six.", show(t_o1, 'Forty minus four'), show(t_sq['x'], 'is thirty-six')),
      L("So thirty-six thousand private cars are privately owned."),
      L("The private car row is forty-five. Forty-five minus thirty-six is nine.", show(t_o2, 'Forty-five minus thirty-six'),
        show(t_sq['y'], 'is nine')),
      L("So nine thousand private cars were owned by a company. That's what the question asked.",
        show(t_o3, 'So nine thousand private cars')), pre=[t_c11['base']]),
    S('What we saw',
      L("So a table question can be a percent question, an average question, or an overlap question. We use the tools we "
        "already know."),
      L("Not every question is like that. Sometimes we only read the table. But it's good to be ready for both."),
      L("Next, the first type of chart, points on axes. I'll see you in the next video.")),
])
# (5.6 minutes: one video)


# =================================================================================================================
# ch52-scatter (lesson)
# Hebrew (seg03, all of it): points on axes = the most important type, the base of the others; the car table turned into
# points: x = the years, y = thousands (90 = 90,000), the key first (a black star = sold), 2010 up to 60 and a star,
# 80, 80, 100, the points sit exactly at the value; the other series (a dot, a white star, an x): the chart = the table;
# the advantage: we SEE up / same / up; numbers as markers (the number of dealers): which year had the biggest average
# per dealer? 60/5 = 12, 80/8 = 10, 80/10 = 8, 100/15 < 10 without calculating -> 2010; negative values (-10 = 10,000
# returned); the scale is exact (every line = 10,000); the Z on the axis (starts at 50: that part is not to scale,
# nothing below it). ADDED under R37 (a core method of the topic, used in solve-ch-q01 and solve-ch-q05, and in the real
# exam's "in how many of ..." questions): COUNTING WITH A LINE - a line at the value, count what is past it, "more than"
# leaves out a point that sits on the line; two examples (privately owned above 50: only 2013, the 50s sit on the line;
# sold above 70: 3 years); the line can also be vertical. NEW (all).
# =================================================================================================================
SC0 = MA.car_scatter(1, only=0)
p_c0 = CH('p_c0', MA.car_scatter(1, only=0), 345, 92, 740, [
    ('h90', MA.car_scatter(1, only=0, marks=[('hline', 90, '90 = 90,000')]))])
p_n1 = I('p_n1', 'Across: $\\ $the years', size=28, col=1)
p_n2 = I('p_n2', 'Up: $\\ $the amount, in thousands', size=28, col=1)
p_n3 = I('p_n3', '$90$ on the axis $= 90{,}000$', size=28, col=1)
p_c1 = CH('p_c1', SC0, 345, 92, 740, [
    ('s1', MA.car_scatter(1, only=1, marks=[('guide', 0, 60)])), ('s2', MA.car_scatter(1, only=2, marks=[('guide', 0, 60)])),
    ('s3', MA.car_scatter(1, only=3, marks=[('guide', 0, 60)])), ('s4', MA.car_scatter(1, only=4, marks=[('guide', 0, 60)]))])
p_n4 = I('p_n4', 'The key: $\\ $a black star $=$ vehicles sold', size=28, col=1)
p_n5 = I('p_n5', '$2010$: $\\ $up to $60$, a star', size=28, col=1)
p_n6 = I('p_n6', 'Each point sits exactly at its value', size=28, col=1)
SC4 = MA.car_scatter(4)
p_c2 = CH('p_c2', MA.car_scatter(1), 345, 92, 740, [('all', SC4)])
p_n7 = I('p_n7', 'The other three columns: $\\ $a dot, a white star, an x', size=28, col=1)
p_n8 = I('p_n8', 'Every number of the table is a point', size=28, col=1)
p_c3 = CH('p_c3', SC4, 345, 92, 740, [('up', MA.car_scatter(4, highlight=[(0, 1), (0, 2)]))])
p_n9 = I('p_n9', 'Sold: $\\ $up, the same, up', size=28, col=1)
p_n10 = I('p_n10', 'In a table we read every number. $\\ $Here we see it.', size=28, col=1)
p_c4 = CH('p_c4', SC4, 345, 92, 740, [
    ('l50', MA.car_scatter(4, marks=[('hline', 50, '50')])),
    ('r50', MA.car_scatter(4, marks=[('hline', 50, '50'), ('pt', 3, 65)]))])
p_q1 = I('p_q1', 'In how many years were more than $50$ thousand vehicles privately owned?', size=28, col=1)
p_k1 = I('p_k1', 'A line at $50$: $\\ $count the white stars above it', size=28, col=1)
p_k2 = I('p_k2', 'On the line ($50$) is not more than $50$', size=28, col=1)
p_k3 = I('p_k3', 'Above it: $\\ $only $2013$. $\\ $One year.', size=28, col=1)
p_c5 = CH('p_c5', SC4, 345, 92, 740, [
    ('l70', MA.car_scatter(4, marks=[('hline', 70, '70')])),
    ('r70', MA.car_scatter(4, marks=[('hline', 70, '70'), ('pt', 1, 80), ('pt', 2, 80), ('pt', 3, 100)]))])
p_q2 = I('p_q2', 'In how many years were more than $70$ thousand vehicles sold?', size=28, col=1)
p_k4 = I('p_k4', 'Black stars above the line: $\\ 2011,\\ 2012,\\ 2013$', size=28, col=1)
p_k5 = I('p_k5', 'Three years', size=28, col=1)
p_k6 = I('p_k6', 'More than a value? $\\ $A line at the value, count past it', size=28, col=1)
NUM = MA.car_scatter_num()
p_c6 = CH('p_c6', NUM, 345, 92, 740, [('h', MA.car_scatter_num(hl=[(0, 1)]))])
p_n11 = I('p_n11', 'The number at a point $=$ the number of car dealers', size=28, col=1)
p_n12 = I('p_n12', '$2011$: $\\ 80$ thousand vehicles, $8$ dealers', size=28, col=1)
p_c7 = CH('p_c7', NUM, 345, 92, 740)
p_q3 = I('p_q3', 'In which year was the average number of vehicles sold per dealer the greatest?', size=28, col=1)
p_q3c = I('p_q3c', '$(1)\\ 2010\\quad (2)\\ 2011\\quad (3)\\ 2012\\quad (4)\\ 2013$', size=28, col=1)
p_v1 = IH('p_v1', '$2010$: $\\ 60\\div5=12$', size=30, col=1)
p_v2 = IH('p_v2', '$2011$: $\\ 80\\div8=10$', size=30, col=1)
p_v3 = IH('p_v3', '$2012$: $\\ 80\\div10=8$', size=30, col=1)
p_v4 = IH('p_v4', '$2013$: $\\ 100\\div15$, less than $10$', size=30, col=1)
NEG = CA.scatter(MA.YEARS, [dict(name='Vehicles sold', values=[-10, 80, 80, 100], marker='star')], ymin=-20, ymax=110, ystep=10,
                 ylabel='Thousands', title='Vehicles sold (imagine: 2010 = −10)', legend=None)
p_c8 = CH('p_c8', NEG, 345, 92, 740, [('h', CA.scatter(MA.YEARS, [dict(name='Vehicles sold', values=[-10, 80, 80, 100], marker='star')],
                                                       ymin=-20, ymax=110, ystep=10, ylabel='Thousands', legend=None,
                                                       title='Vehicles sold (imagine: 2010 = −10)', highlight=[(0, 0)]))])
p_n13 = I('p_n13', 'Below zero: $\\ -10 =$ $10{,}000$ cars returned', size=28, col=1)
p_c9 = CH('p_c9', SC4, 345, 92, 740, [('b', MA.car_scatter(4, marks=[('brace', 3.3, 10, 20, '10,000'), ('brace', 3.3, 30, 40, '10,000')]))])
p_n14 = I('p_n14', 'Every line on the axis: $\\ $the same step, $10{,}000$', size=28, col=1)
ZSC = MA.car_scatter(3, ymin=50, ymax=110, ystep=10)
p_c10 = CH('p_c10', ZSC, 345, 92, 740)
p_n15 = I('p_n15', 'The axis starts at $50$', size=28, col=1)
p_n16 = I('p_n16', 'The Z: $\\ $from $0$ to $50$ is not to scale', size=28, col=1)
p_n17 = I('p_n17', 'Nothing under $50$ is shown', size=28, col=1)
video('ch52-scatter', 'lesson', slides=[
    S('Points on Axes',
      L("Welcome back, and now the first type of chart, points on axes."),
      L("It's the most important type, because all the other charts grow out of it.")),
    S('From a table to points',
      L("Let's take the car table from the last lesson, and turn it into points on axes."),
      L("Across the bottom we have the years, two thousand ten to two thousand thirteen.", show(p_n1, 'Across the bottom')),
      L("Going up we have the amount, in thousands.", show(p_n2, 'Going up we have the amount')),
      L("So when the axis says ninety, it's not really ninety. It's ninety thousand.", show(p_c0['h90'], "it's not really ninety"),
        show(p_n3, "It's ninety thousand")), pre=[p_c0['base']]),
    S('Plotting the points',
      L("First we need a key. It tells us which mark stands for which column. A black star is the vehicles sold.",
        show(p_n4, 'A black star is the vehicles sold')),
      L("In two thousand ten, sixty thousand vehicles were sold. So we go to two thousand ten, we go up to sixty, and we put a star "
        "there.", show(p_c1['s1'], 'we put a star there'), show(p_n5, 'we go up to sixty')),
      L("In two thousand eleven, eighty thousand. A star at eighty.", show(p_c1['s2'], 'A star at eighty')),
      L("Two thousand twelve, also eighty.", show(p_c1['s3'], 'Two thousand twelve, also eighty')),
      L("And two thousand thirteen, a hundred thousand. A star at a hundred.", show(p_c1['s4'], 'A star at a hundred')),
      L("Each point sits exactly at its value. So if we read two thousand twelve, we get eighty, just like in the table.",
        show(p_n6, 'Each point sits exactly')), pre=[p_c1['base']]),
    S('All four columns',
      L("We mark the other columns the same way. Each one gets its own mark in the key."),
      L("Private cars get a dot. Privately owned vehicles get a white star. And privately owned commercial vehicles get an x.",
        show(p_c2['all'], 'Private cars get a dot'), show(p_n7, 'privately owned commercial vehicles get an x')),
      L("Now every number of the table is a point on the chart. It's the same data, as a picture.",
        show(p_n8, 'every number of the table')), pre=[p_c2['base']]),
    S('Easy to see',
      L("Why is this better than the table? Because we can see the changes."),
      L("Look at the black stars. From two thousand ten to two thousand eleven they go up. Then they stay the same. Then they go up "
        "again.", show(p_c3['up'], 'Then they stay the same'), show(p_n9, 'Then they go up again')),
      L("In the table we had to read every number to see that. Here we see it in one look.", show(p_n10, 'In the table we had')),
      pre=[p_c3['base']]),
    S('Counting with a line',
      L("Now a tool we'll use a lot. Here's a question. In how many years were more than fifty thousand vehicles privately "
        "owned?", show(p_q1, 'In how many years')),
      L("Privately owned are the white stars. We need the ones above fifty. So we draw a line at fifty.",
        show(p_c4['l50'], 'So we draw a line at fifty'), show(p_k1, 'we draw a line at fifty')),
      L("Now we only count the white stars above the line.", pt('p_c4', 'count the white stars')),
      L("Careful with two thousand eleven and two thousand twelve. Their white stars sit right on the line. That's fifty, and fifty is "
        "not more than fifty. So they don't count.", show(p_k2, 'fifty is not more than fifty')),
      L("Above the line there's only two thousand thirteen, at sixty-five. So the answer is one year.",
        show(p_c4['r50'], 'at sixty-five'), show(p_k3, 'So the answer is one year')), pre=[p_c4['base']]),
    S('One more line',
      L("Let's try another one. In how many years were more than seventy thousand vehicles sold?", show(p_q2, 'In how many years')),
      L("Vehicles sold are the black stars. So we draw a line at seventy.", show(p_c5['l70'], 'we draw a line at seventy')),
      L("Which black stars are above it? Two thousand eleven, two thousand twelve and two thousand thirteen.",
        show(p_c5['r70'], 'Which black stars are above it'), show(p_k4, 'Two thousand eleven, two thousand twelve')),
      L("So it's three years. Two thousand ten is at sixty, below the line.", show(p_k5, "So it's three years")),
      L("So when a question asks how many are more than some value, we draw a line at that value. Then we count what's "
        "past the line. The line can also stand up, when the value is on the bottom axis.", show(p_k6, 'we draw a line at that value')),
      pre=[p_c5['base']]),
    S('Numbers as marks',
      L("Sometimes the points aren't stars or dots. They can be numbers. Then each number adds one more piece of data."),
      L("Here the number at each point is the number of car dealers that sold the vehicles that year.",
        show(p_n11, 'the number of car dealers')),
      L("So in two thousand eleven, eighty thousand vehicles were sold, by eight dealers.", show(p_c6['h'], 'by eight dealers'),
        show(p_n12, 'by eight dealers')), pre=[p_c6['base']]),
    S('An average per dealer',
      L("Here's a question on it. In which year was the average number of vehicles sold per dealer the greatest?",
        show(p_q3, 'In which year was'), show(p_q3c, 'the greatest')),
      L("The average per dealer is the vehicles divided by the dealers. Two thousand ten. Sixty thousand vehicles, five dealers. "
        "Sixty divided by five is twelve.", show(p_v1, 'Sixty divided by five')),
      L("Two thousand eleven. Eighty divided by eight is ten.", show(p_v2, 'Eighty divided by eight')),
      L("Two thousand twelve. Eighty divided by ten is eight.", show(p_v3, 'Eighty divided by ten')),
      L("Two thousand thirteen. A hundred divided by fifteen. Do we need the exact number? No. A hundred divided by ten is ten, "
        "and fifteen dealers is more than ten. So the average is less than ten thousand per dealer.", show(p_v4, 'A hundred divided by fifteen')),
      L("Twelve is the greatest. So the answer is two thousand ten, choice number one."), pre=[p_c7['base']]),
    S('Below zero',
      L("A few more things about axes. An axis can go below zero."),
      L("Imagine that in two thousand ten, no cars were sold. And on top of that, ten thousand cars were returned. Then the point "
        "is at minus ten.", show(p_c8['h'], 'Then the point is at minus ten'), show(p_n13, 'ten thousand cars were returned')),
      L("In other charts, below zero can mean other things, like a loss. The chart's explanation tells us."),
      pre=[p_c8['base']]),
    S('The scale is exact',
      L("Look at the lines on the axis. Ten, twenty, thirty, forty. Every line is the same step, ten thousand.",
        show(p_c9['b'], 'Every line is the same step'), show(p_n14, 'the same step, ten thousand')),
      L("The chart is drawn exactly to scale. So we can trust what we see."), pre=[p_c9['base']]),
    S('The Z on the axis',
      L("Now look at this axis. It doesn't start at zero. It starts at fifty.", show(p_n15, 'It starts at fifty')),
      L("But we said the chart is exact. And the distance from zero to fifty here is much shorter than five steps."),
      L("So the axis has a zigzag at the bottom, like a Z. The Z tells us that this part is not to scale.",
        pt('p_c10', 'like a Z'), show(p_n16, 'this part is not to scale')),
      L("And nothing under fifty is shown. So the x's are gone, and so are the two points of two thousand ten that were under "
        "fifty.", show(p_n17, 'nothing under fifty is shown')),
      L("That's it for points on axes. Next, we'll join the points with a line. I'll see you in the next video."),
      pre=[p_c10['base']]),
])


# =================================================================================================================
# ch52-line (lesson)
# Hebrew (seg04, all of it): a line graph = the points on axes joined by a line, so we see things more clearly; the car
# data joined line by line, the points can go, four lines look the same -> a style per line (bold, dashed, dash-dot) and
# the key; the line itself has no value between the points (no "2010 and a half" with 70,000); its only meaning is the
# trend (flat = no change, up = a rise), the angle = how big the rise; points vs lines (hide the lines: hard to see which
# rise is bigger). ADDED (R37, "compare by eye" is used in many questions): the steeper part with numbers (privately owned
# +10 vs +15) and a second case with the same steepness (sold +20 and +20). NEW (all).
# =================================================================================================================
LK = dict(ymin=0, ymax=110, ystep=10, ylabel='Thousands', title='Vehicles sold, 2010–2013')


def car_lines(n=4, styles=True, points=True, marks=()):
    ser = [dict(name=s['name'], values=s['values'], style=MA.STYLES[i] if styles else 'solid', marker=s['marker'])
           for i, s in enumerate(MA.CAR_S[:n])]
    return CA.line(MA.YEARS, ser, points=points, legend='right' if styles else None, marks=marks, **LK)


l_c1 = CH('l_c1', MA.car_scatter(1), 345, 92, 740, [('!join', car_lines(1, styles=False))])
l_n1 = I('l_n1', 'A line graph $=$ points on axes, joined by a line', size=28, col=1)
l_c2 = CH('l_c2', car_lines(4, styles=False), 345, 92, 740, [('!nopts', car_lines(4, styles=False, points=False))])
l_n2 = I('l_n2', 'The points can go: $\\ $the line is enough', size=28, col=1)
l_n3 = I('l_n3', 'But four lines that look the same: $\\ $which is which?', size=28, col=1)
l_c3 = CH('l_c3', car_lines(4, styles=False, points=False), 345, 92, 740, [('!st', car_lines(4, points=False))])
l_n4 = I('l_n4', 'A style for each line: $\\ $bold, plain, dashed, dash-dot', size=28, col=1)
l_n5 = I('l_n5', 'The key shows which style is which', size=28, col=1)
LS = car_lines(4, points=False)
l_c4 = CH('l_c4', LS, 345, 92, 740, [
    ('x', car_lines(4, points=False, marks=[('cross', 0.5, 70)])),
    ('p', car_lines(4, points=False, marks=[('cross', 0.5, 70), ('pt', 0, 60), ('pt', 1, 80), ('pt', 2, 80), ('pt', 3, 100)]))])
l_n6 = I('l_n6', 'Each value is a full-year total', size=28, col=1)
l_n7 = I('l_n7', 'In this yearly chart: values only at the marked years', size=28, col=1)
l_c5 = CH('l_c5', LS, 345, 92, 740, [
    ('f', car_lines(4, points=False, marks=[('seg', 1, 80, 2, 80)])),
    ('u', car_lines(4, points=False, marks=[('seg', 1, 80, 2, 80), ('seg', 2, 80, 3, 100)]))])
l_n8 = I('l_n8', 'The line shows the trend', size=28, col=1)
l_n9 = I('l_n9', 'Flat: $\\ $no change. $\\ $Up: $\\ $a rise.', size=28, col=1)
l_c6 = CH('l_c6', LS, 345, 92, 740, [
    ('a', car_lines(4, points=False, marks=[('seg', 0, 40, 1, 50)])),
    ('b', car_lines(4, points=False, marks=[('seg', 0, 40, 1, 50), ('seg', 2, 50, 3, 65)]))])
l_r1 = IH('l_r1', '$50-40=10$', size=30, col=1)
l_r2 = IH('l_r2', '$65-50=15$', size=30, col=1)
l_n10 = I('l_n10', 'Same one-year interval: $\\ $steeper means a bigger rise', size=28, col=1)
l_c7 = CH('l_c7', LS, 345, 92, 740, [
    ('a', car_lines(4, points=False, marks=[('seg', 0, 60, 1, 80)])),
    ('b', car_lines(4, points=False, marks=[('seg', 0, 60, 1, 80), ('seg', 2, 80, 3, 100)]))])
l_r3 = IH('l_r3', '$80-60=20$', size=30, col=1)
l_r4 = IH('l_r4', '$100-80=20$', size=30, col=1)
l_n11 = I('l_n11', 'Just as steep: $\\ $the same rise', size=28, col=1)
l_c8 = CH('l_c8', MA.car_scatter(4, legend=None), 345, 92, 600)
l_c9 = CH('l_c9', car_lines(4, styles=True, points=False), 965, 92, 600)
l_c9['base'].pop('_chart')
l_n12 = I('l_n12', 'Points: $\\ $hard to see which rise is bigger', size=30)
l_n13 = I('l_n13', 'Lines: $\\ $the steeper line shows it right away', size=30)

video('ch52-line', 'lesson', slides=[
    S('Line Graph',
      L("Welcome back, and now the line graph."),
      L("A line graph is the same chart as points on axes. We just join the points with a line.")),
    S('Join the points',
      L("Here are the vehicles sold again. Sixty, eighty, eighty, and a hundred thousand.", pt('l_c1', 'Sixty, eighty, eighty')),
      L("Now we join them with a line, from one point to the next.", show(l_c1['join'], 'we join them with a line'),
        show(l_n1, 'from one point to the next')),
      L("Why do we do that? We'll see in a moment. The line helps us see the changes more clearly."), pre=[l_c1['base']]),
    S('Four lines',
      L("We do the same for the other three columns. Each one gets its own line."),
      L("Once the points are joined, we can even take the points away. The line is enough.",
        show(l_c2['nopts'], 'take the points away'), show(l_n2, 'The line is enough')),
      L("But now there's a problem. All four lines look the same. Which line is which?", show(l_n3, 'Which line is which')),
      pre=[l_c2['base']]),
    S('A style for each line',
      L("So we draw each line in its own style. A bold line, a plain line, a dashed line, and a dash-dot line.",
        show(l_c3['st'], 'in its own style'), show(l_n4, 'A bold line, a plain line')),
      L("And the key shows which style belongs to which column.", show(l_n5, 'the key shows')),
      L("So it's really the points from before, joined by lines."), pre=[l_c3['base']]),
    S('Only the points count',
      L("Now something very important. The line has values only at the marked years."),
      L("Look halfway between two thousand ten and two thousand eleven. The bold line passes seventy there.",
        show(l_c4['x'], 'The bold line passes seventy')),
      L("Does that give us another sales figure? No. Each value here is a full-year total. The line doesn't give us a "
        "separate total halfway between the years.", show(l_n6, 'Each value here is a full-year total')),
      L("The values are only at the points. Two thousand ten, two thousand eleven, two thousand twelve and two thousand thirteen.",
        show(l_c4['p'], 'The values are only at the points'), show(l_n7, 'only at the points')), pre=[l_c4['base']]),
    S('The line shows the trend',
      L("So what is the line for? It shows the trend.", show(l_n8, 'It shows the trend')),
      L("What does trend mean? Where the line is flat, there's no change. Like the bold line from two thousand eleven to two thousand "
        "twelve.", show(l_c5['f'], 'Where the line is flat'), show(l_n9, 'there\'s no change')),
      L("Where the line goes up, there's a rise. Like the bold line from two thousand twelve to two thousand thirteen.",
        show(l_c5['u'], 'Where the line goes up')), pre=[l_c5['base']]),
    S('Steeper means more',
      L("Each step here is one year, on the same axes. So a steeper line means a bigger rise in that year. Let's see it in numbers."),
      L("Look at privately owned, the dashed line. From two thousand ten to two thousand eleven it goes from forty to fifty.",
        show(l_c6['a'], 'From two thousand ten to two thousand eleven')),
      L("Fifty minus forty is ten. So that's a rise of ten thousand.", show(l_r1, 'Fifty minus forty')),
      L("From two thousand twelve to two thousand thirteen it goes from fifty to sixty-five.", show(l_c6['b'], 'From two thousand twelve to two thousand thirteen')),
      L("Sixty-five minus fifty is fifteen. A rise of fifteen thousand.", show(l_r2, 'Sixty-five minus fifty')),
      L("Fifteen is more than ten. And on the chart, the second part is steeper. So the steeper part is the bigger rise.",
        show(l_n10, 'the steeper part is the bigger rise')), pre=[l_c6['base']]),
    S('Just as steep',
      L("And when two parts are just as steep, the rise is the same. Look at the bold line, the vehicles sold."),
      L("From two thousand ten to two thousand eleven, it goes from sixty to eighty. Eighty minus sixty is twenty.",
        show(l_c7['a'], 'it goes from sixty to eighty'), show(l_r3, 'Eighty minus sixty')),
      L("From two thousand twelve to two thousand thirteen, from eighty to a hundred. A hundred minus eighty is twenty again.",
        show(l_c7['b'], 'from eighty to a hundred'), show(l_r4, 'A hundred minus eighty')),
      L("The same rise, and on the chart the two parts are just as steep.", show(l_n11, 'just as steep')),
      pre=[l_c7['base']]),
    S('Points or lines?',
      L("Let's compare the two charts. On the left, the points alone. On the right, the same data with lines."),
      L("With the points alone, it's hard to see which rise is bigger.", show(l_n12, "it's hard to see")),
      L("With the lines, the steeper line shows it right away. That's the advantage of a line graph.",
        show(l_n13, 'the steeper line shows it')), pre=[l_c8['base'], l_c9['base']]),
    S('Line graph: in short',
      L("So a line graph helps us see the trend, and how steep each part is."),
      L("But remember, in this yearly chart, only the marked years have given sales totals. The connecting line doesn't give us extra totals."),
      L("Next, the same data as bars. I'll see you in the next video."),
      pre=[CH('l_recap', car_lines(), 345, 92, 740)['base']]),
])


# =================================================================================================================
# ch52-bar (lesson, two parts, not on camera)
# Hebrew (seg05, all of it): bars = the same data as the table / points / lines; the lines on the left, bars on the
# right, line by line: a bar from the bottom up to the point, the key now shows a white bar; the next series moved a bit
# to the right; 2010 privately owned: the bar's height 40 = the point; a bar inside a bar (60 sold, 45 private inside;
# 40 privately owned, about 4 of them commercial); the overlap in bars (80 / 60 / 50: all 50 inside -> 50 are both, pushed
# to the top -> only 30); stacked bars (private, commercial, motorcycles can't overlap): the top = the total (2012
# almost 120), a part = the gap (commercial 60 to 110 = 50, not 110); a chart fits its user (table / bars / stacked for
# the manager); horizontal bars ("Carob" English 75, "Zucchini" 80; turn the notebook 90 degrees); "is it stacked? is one
# inside the other?". ADDED: each reading said with its numbers; the stacked-bar part with two examples (commercial 2012,
# private cars 2013 = 70 from 0); the overlap range said as "from 30 to 50" (overlap: topic 24, a REMINDER). NEW.
# =================================================================================================================
BK = dict(ymin=0, ymax=110, ystep=10, ylabel='Thousands', title='Vehicles sold, 2010–2013')
b_ln = CH('b_ln', car_lines(4, points=False), 345, 92, 600)
B_EMPTY = CA.bar(MA.YEARS, [dict(name='Vehicles sold', values=[None] * 4)], legend=None, **BK)
b_br = CH('b_br', B_EMPTY, 965, 92, 600, [('!b1', MA.car_bar(1)), ('!b2', MA.car_bar(2)), ('!b4', MA.car_bar(4))])
b_br['base'].pop('_chart')
b_n1 = I('b_n1', 'Bars: $\\ $the same data again', size=30)
b_n2 = I('b_n2', 'Each bar goes up to the point: $\\ 60,\\ 80,\\ 80,\\ 100$', size=30)
b_n3 = I('b_n3', 'The key: $\\ $a white bar $=$ vehicles sold', size=30)
b_n4 = I('b_n4', 'The next column: $\\ $its bars stand next to them', size=30)
B4 = MA.car_bar(4)
b_c2 = CH('b_c2', B4, 345, 92, 740, [('h', MA.car_bar(4, highlight=[(2, 0)], marks=[('hline', 40, '40')]))])
b_n5 = I('b_n5', '$2010$, privately owned: $\\ $the bar reaches $40$', size=28, col=1)
b_n6 = I('b_n6', '$40$ thousand, $\\ $the same as the point and the table', size=28, col=1)
BIN = lambda **k: CA.bar(MA.YEARS, [dict(name='Vehicles sold', values=MA.SOLD, fill='#fff'), dict(name='Private cars', values=MA.PRIV, fill=CA.INK)],
                         mode='overlap', ymax=110, ystep=10, ylabel='Thousands', title='Bar inside a bar', **k)
b_c3 = CH('b_c3', BIN(), 345, 92, 740, [('h', BIN(highlight=[(0, 0), (1, 0)]))])
b_n7 = I('b_n7', 'The white bar: $\\ $all the vehicles sold, $60$', size=28, col=1)
b_n8 = I('b_n8', 'The black bar inside: $\\ $the private cars, $45$', size=28, col=1)
b_n9 = I('b_n9', 'The black bar is a part of the white bar', size=28, col=1)
b_o1 = CH('b_o1', MA.overlap_fig(1), 345, 92, 740)
b_o2 = CH('b_o2', MA.overlap_fig(2).replace('both: 30', 'both: ?'), 345, 92, 740,
          [('!value', MA.overlap_fig(2))])
b_n10 = I('b_n10', '$2011$: $\\ 80$ sold, $\\ 60$ private cars, $\\ 50$ privately owned', size=28, col=1)
b_n11 = I('b_n11', 'Both? $\\ $All $50$ inside the $60$: $\\ 50$', size=28, col=1)
b_n12 = IH('b_n12', '$60+50=110$', size=30, col=1)
b_n13 = IH('b_n13', '$110-80=30$', size=30, col=1)
b_n14 = I('b_n14', 'Both: $\\ $anywhere from $30$ to $50$ thousand', size=28, col=1)
ST = MA.stack_chart()
b_c5 = CH('b_c5', ST, 345, 92, 740, [('t', MA.stack_chart(marks=[('hline', 118, 'about 118')])),
                                     ('g', MA.stack_chart(marks=[('hline', 118, 'about 118'), ('brace', 2.35, 60, 110, '50')]))])
b_n15 = I('b_n15', 'Different kinds: $\\ $a vehicle is only one of them', size=28, col=1)
b_n16 = I('b_n16', 'Stacked: $\\ $the top of the stack $=$ the total', size=28, col=1)
b_n17 = IH('b_n17', '$110-60=50$', size=30, col=1)
b_n18 = I('b_n18', 'A part $=$ the gap, $\\ $not the top', size=28, col=1)
b_c6 = CH('b_c6', ST, 345, 92, 740, [('p', MA.stack_chart(marks=[('brace', 3.35, 0, 70, '70')]))])
b_n19 = I('b_n19', 'The bottom part starts at $0$: $\\ $private cars $2013$, $70$', size=28, col=1)
b_n20 = I('b_n20', 'The same data: $\\ $a table, bars, or a stack. $\\ $Each fits another user.', size=28, col=1)
SCH = MA.school_chart()
b_c7 = CH('b_c7', SCH, 345, 92, 800, [('h', MA.school_chart(highlight=[(0, 1), (1, 1)]))])
b_n21 = I('b_n21', 'Horizontal bars: $\\ $the values go across', size=28, col=1)
b_n22 = I('b_n22', '"For example: the average grade in English at the Carob school was 75, and at the Zucchini school, 80."', size=24, col=1)
b_n23 = I('b_n23', 'Turn the page: $\\ $an ordinary bar chart', size=28, col=1)

video('ch52-bar', 'lesson', slides=[
    S('Bar Chart',
      L("Welcome back, and now the bar chart. It's one of the most common charts on the exam."),
      L("A bar chart shows the same data as before, the table, the points and the lines. This time we use bars.")),
    S('From lines to bars',
      L("On the left are the lines from the last lesson. On the right we'll build bars from the same data.",
        show(b_n1, 'the same data')),
      L("Let's start with the vehicles sold. Instead of the line, each year gets a bar from the bottom up to the point.",
        show(b_br['b1'], 'each year gets a bar')),
      L("Two thousand ten up to sixty, two thousand eleven up to eighty, two thousand twelve also eighty, and two thousand thirteen up to a hundred.",
        show(b_n2, 'Two thousand ten up to sixty')),
      L("The key changes too. A white bar now means the vehicles sold.", show(b_n3, 'A white bar now means')),
      L("Next, the private cars. Their bars would fall inside the same place, so we move them a bit to the right.",
        show(b_br['b2'], 'we move them a bit'), show(b_n4, 'we move them')),
      L("We do the same with the other two columns. Now the bars of each year stand next to each other.",
        show(b_br['b4'], 'the bars of each year')), pre=[b_ln['base'], b_br['base']]),
    S('Reading a bar',
      L("So a bar's height is its value. Let's check one. Two thousand ten, privately owned, the grey bar."),
      L("It reaches forty. So forty thousand vehicles were privately owned.", show(b_c2['h'], 'It reaches forty'),
        show(b_n5, 'It reaches forty')),
      L("That's the same forty as the point in the line graph, and the same as in the table. The same data, three "
        "pictures.", show(b_n6, 'the same as in the table')), pre=[b_c2['base']]),
    S('A bar inside a bar',
      L("Sometimes a bar stands inside another bar."),
      L("Here, the white bar is all the vehicles sold. In two thousand ten, it reaches sixty.", show(b_c3['h'], 'it reaches sixty'),
        show(b_n7, 'the white bar is all')),
      L("Inside it stands a black bar, the private cars. It reaches forty-five.", show(b_n8, 'Inside it stands a black bar')),
      L("Why inside? Because the private cars are a part of the vehicles sold. Forty-five of the sixty.",
        show(b_n9, 'Why inside')), pre=[b_c3['base']]),
    S('Both groups in one bar',
      L("A bar inside a bar can also hide an overlap question. Look at two thousand eleven.", show(b_n10, 'Look at two thousand eleven')),
      L("Eighty thousand vehicles were sold. Of them, sixty thousand were private cars, and fifty thousand were privately "
        "owned."),
      L("How many were both, private cars and privately owned? It could be that all fifty are inside the sixty.",
        show(b_o1['base'], 'all fifty are inside the sixty')),
      L("Then all fifty are both.", show(b_n11, 'Then all fifty are both')), pre=[]),
    S('The smallest overlap',
      L("Or we can push the fifty up, as high as it goes, to the top of the eighty.", show(b_o2['base'], 'push the fifty up')),
      L("Now only part of it is inside the sixty. How much? Sixty plus fifty is a hundred ten.", show(b_n12, 'Sixty plus fifty')),
      L("But there are only eighty thousand vehicles. A hundred ten minus eighty is thirty. So at least thirty thousand are both.",
        show(b_n13, 'A hundred ten minus eighty'), show(b_o2['value'], 'is thirty')),
      L("So both can be anywhere from thirty to fifty thousand. It's the same as in overlap questions.",
        show(b_n14, 'anywhere from thirty to fifty')), pre=[]),
    S('Stacked bars',
      L("Now another kind of bar chart. Here there are three kinds of vehicles. Private cars, commercial vehicles, and "
        "motorcycles."),
      L("A vehicle can be only one of them. It's a van or a car, not both.", show(b_n15, 'A vehicle can be only one')),
      L("So we can put the bars one on top of the other. That's called stacked bars.", show(b_n16, 'one on top of the other')),
      L("Why would we want that? Say I own the dealer group. Most of all, I want the total."),
      L("The top of the stack is the total. In two thousand twelve it's almost a hundred twenty. About a hundred eighteen thousand.",
        show(b_c5['t'], 'The top of the stack is the total')),
      L("And how many commercial vehicles were sold in two thousand twelve? The grey part goes from sixty up to a hundred ten.",
        show(b_c5['g'], 'The grey part goes from sixty')),
      L("So it's a hundred ten minus sixty, fifty thousand.", show(b_n17, 'a hundred ten minus sixty')),
      L("Careful, a lot of students say a hundred ten, because that's where the grey part ends. But a part is the gap, "
        "from its bottom to its top.", show(b_n18, 'a part is the gap')), pre=[b_c5['base']]),
    S('The bottom part',
      L("Only the bottom part starts at zero. So we can read it straight from the axis."),
      L("Private cars in two thousand thirteen, the black part, go from zero to seventy. So seventy thousand.",
        show(b_c6['p'], 'go from zero to seventy'), show(b_n19, 'seventy thousand')),
      L("The same data can be shown in many ways. One worker likes a table, another likes bars. The manager wants the "
        "total, so he gets a stack.", show(b_n20, 'The same data can be shown')), pre=[b_c6['base']]),
    S('Horizontal bars',
      L("One more kind, and it comes up quite often. Horizontal bars. They're ordinary bars, lying on their side.",
        show(b_n21, 'lying on their side')),
      L("This chart shows the average grades at the end of tenth grade, in two schools, Carob and Zucchini."),
      L("The example says, the average grade in English at Carob was seventy-five, and at Zucchini, eighty.",
        show(b_n22, 'The example says')),
      L("Now the values go across, on the bottom axis. The English bar at Carob reaches seventy-five. At Zucchini, it "
        "reaches eighty. It matches.", show(b_c7['h'], 'The English bar at Carob')),
      L("If it confuses you, turn the page in your mind. Then it's an ordinary bar chart.", show(b_n23, 'turn the page')),
      L("So in a bar chart, always ask two things. Is it stacked? Is one bar inside another? Then you won't read a hundred "
        "ten where the answer is fifty."),
      L("I'll see you in the next video."), pre=[b_c7['base']]),
])
# (4.7 minutes: one video)


# =================================================================================================================
# ch52-continuous (lesson)
# Hebrew (seg06, all of it): start from a bar chart (the "Psycho" website, 24 hours; the strips under the chart = where
# most visitors are; the example 16:00 -> 390, 16:00-17:00 forum); a bar every 4 hours, every hour, every quarter hour ...
# so many bars that we see one area -> a continuous line; unlike the line graph, EVERY point of it is a measurement;
# used for things measured all the time (temperature), not for a yearly total (cars); the question: the biggest relative
# increase vs the hour before (relative = how many times; 8:00 80 -> 9:00 300, almost x4; 15 -> 16, 20 -> 21, 22 -> 23
# small); mark the slope before each point, the sharpest wins; with similar numbers of visitors the steeper slope is the
# bigger change -> 9:00. ADDED: relative increase with two number examples (100 -> 150 vs 400 -> 450), the "lower start"
# rule said in words, each check said with its numbers. NEW (all). Percent change: topic 23, a REMINDER.
# =================================================================================================================
s_c1 = CH('s_c1', MA.site_bars(4), 345, 92, 740, [('h', MA.site_bars(4, hl=(16,)))])
s_n1 = I('s_n1', 'Across: $\\ $the hours. $\\ $Up: $\\ $the visitors.', size=28, col=1)
s_n2 = I('s_n2', 'The strips: $\\ $where most visitors are in that hour', size=28, col=1)
s_n3 = I('s_n3', '"For example: at 16:00 there were 390 visitors on the site. Between 16:00 and 17:00, most of them were in the forum."', size=24, col=1)
s_c2 = CH('s_c2', MA.site_bars(4), 345, 92, 740, [('!h1', MA.site_bars(1)), ('!q', MA.site_bars(0)), ('!c', MA.site_curve())])
s_n4 = I('s_n4', 'A bar every $4$ hours', size=28, col=1)
s_n5 = I('s_n5', 'A bar every hour', size=28, col=1)
s_n6 = I('s_n6', 'A bar every quarter hour: $\\ $one big area', size=28, col=1)
s_n7 = I('s_n7', 'So: $\\ $one continuous line', size=28, col=1)
CV = MA.site_curve()
s_c3 = CH('s_c3', CV, 345, 92, 740, [('g', MA.site_curve(marks=[('guide', 12.5, 322)]))])
s_n8 = I('s_n8', 'Every point of the line is a measurement', size=28, col=1)
s_n9 = I('s_n9', 'The line graph of the cars: $\\ $values only at the years', size=28, col=1)
s_n10 = I('s_n10', 'Measured all the time: $\\ $visitors, temperature', size=28, col=1)
s_n11 = I('s_n11', 'One total a year: $\\ $points or a line graph', size=28, col=1)
s_c4 = CH('s_c4', CV, 345, 92, 740)
s_q1 = I('s_q1', 'At which hour was the relative increase in the number of visitors, compared with the hour before it, the greatest?', size=24, col=1)
s_q1c = I('s_q1c', '$(1)\\ $9:00 $\\quad(2)\\ $16:00 $\\quad(3)\\ $21:00 $\\quad(4)\\ $23:00', size=26, col=1)
s_r1 = IH('s_r1', '$100$ to $150$: $\\ $half more', size=30, col=1)
s_r2 = IH('s_r2', '$400$ to $450$: $\\ $an eighth more', size=30, col=1)
s_r3 = I('s_r3', 'Relative $=$ compared with where we started', size=28, col=1)
s_c5 = CH('s_c5', CV, 345, 92, 740, [
    ('a', MA.site_curve(marks=[('seg', 8, 80, 9, 300)])),
    ('b', MA.site_curve(marks=[('seg', 8, 80, 9, 300), ('seg', 15, 350, 16, 390), ('seg', 20, 430, 21, 480), ('seg', 22, 400, 23, 420)]))])
s_r4 = IH('s_r4', '$8$:00 to $9$:00: $\\ $about $80$ to $300$', size=28, col=1)
s_r5 = IH('s_r5', '$80\\times4=320$: $\\ $almost $\\times4$', size=28, col=1)
s_r6 = I('s_r6', 'The others: $\\ $a small rise from a high start', size=28, col=1)
s_r7 = I('s_r7', 'The steepest rise, from the lowest start: $\\ $9:00', size=28, col=1)

video('ch52-continuous', 'lesson', slides=[
    S('Continuous Line Graph',
      L("Welcome back, and now the continuous line graph."),
      L("To see why we need it, let's start with a bar chart.")),
    S('The website',
      L("This chart shows the visitors on the Psycho website, over twenty-four hours in a row."),
      L("Across the bottom we have the hours. Going up, the number of visitors.", show(s_n1, 'Across the bottom')),
      L("And the strips under the chart show where most of the visitors are in each hour. In the explanations, the "
        "practice, the forum, or somewhere else.", show(s_n2, 'And the strips under the chart')),
      L("The example says, at four in the afternoon there were three hundred ninety visitors. And between four and five, "
        "most of them were in the forum.", show(s_n3, 'The example says')),
      L("Let's check. Four in the afternoon is sixteen on the axis. Its bar reaches a bit under four hundred. That's three "
        "hundred ninety.", show(s_c1['h'], 'Its bar reaches a bit under')),
      L("And the strip between sixteen and seventeen is dark grey. In the key, dark grey is the forum. It matches."),
      pre=[s_c1['base']]),
    S('More and more bars',
      L("Here we have a bar every four hours. That's not much.", show(s_n4, 'a bar every four hours')),
      L("We can measure more often, say every hour. Then we get a bar for every hour.", show(s_c2['h1'], 'a bar for every hour'),
        show(s_n5, 'a bar for every hour')),
      L("And more often still, every quarter of an hour. Now the bars are so close that we just see one big area.",
        show(s_c2['q'], 'every quarter of an hour'), show(s_n6, 'one big area')),
      L("If we measure every minute, there's no point in bars. We draw one continuous line instead.",
        show(s_c2['c'], 'We draw one continuous line'), show(s_n7, 'one continuous line')), pre=[s_c2['base']]),
    S('Every point counts',
      L("Here's the big difference from the line graph of the cars. There, the line had values only at the years.",
        show(s_n9, 'only at the years')),
      L("Here every point of the line is a measurement. We measured all the time.", show(s_n8, 'every point of the line')),
      L("So we can read any time we like. For example, at half past twelve, the line is a bit above three hundred.",
        show(s_c3['g'], 'at half past twelve')),
      L("When is this chart used? For things that are measured all the time, like visitors on a site, or the temperature.",
        show(s_n10, 'measured all the time')),
      L("The cars were different. We had one total for each year, not a value for every day. So points or a line graph "
        "were right there.", show(s_n11, 'one total for each year')), pre=[s_c3['base']]),
    S('A relative increase',
      L("Here's a sample question. At which hour was the relative increase in visitors, compared with the hour before, "
        "the greatest?", show(s_q1, 'At which hour'), show(s_q1c, 'the greatest')),
      L("What does relative increase mean? It's the increase compared with where we started. What fraction of the starting "
        "amount was added?", show(s_r3, 'compared with where we started')),
      L("Let's see it in numbers. From a hundred to a hundred fifty is fifty more. That's half of a hundred, so half "
        "more.", show(s_r1, 'From a hundred to a hundred fifty')),
      L("From four hundred to four hundred fifty is also fifty more. But fifty is only an eighth of four hundred.",
        show(s_r2, 'From four hundred to four hundred fifty')),
      L("The same fifty, but the first one is a much bigger relative increase. Because it started lower."),
      pre=[s_c4['base']]),
    S('Use the slope',
      L("Now the question. Let's look at the line just before each of the four hours."),
      L("Nine o'clock. At eight there were about eighty visitors, and at nine about three hundred.",
        show(s_c5['a'], 'At eight there were about eighty'), show(s_r4, 'about three hundred')),
      L("Eighty times four is three hundred twenty. So the final number is a little less than four times the starting number.", show(s_r5, 'Eighty times four')),
      L("Now the other three hours. Before sixteen, twenty-one and twenty-three, the line rises only a little, and it "
        "starts high, at three hundred fifty or more.", show(s_c5['b'], 'the line rises only a little'),
        show(s_r6, 'it starts high')),
      L("Do we need to calculate them? No. A small rise from a high start is a small relative increase. Nine o'clock has "
        "the steepest rise, from the lowest start.", show(s_r7, 'the steepest rise')),
      L("So the answer is nine o'clock, choice number one. We saw it with our eyes, by the slope, almost with no "
        "calculation."),
      L("One warning. Compare the same time interval, and check the starting value too. A steeper line alone doesn't tell us the relative rise. Here nine "
        "o'clock wins both ways, steeper and lower."),
      L("I'll see you in the next video."), pre=[s_c5['base']]),
])


# =================================================================================================================
# ch52-range (lesson, two parts, not on camera) and ch52-regions (lesson)
# Hebrew (seg07, all of it): NITE loves minimum-maximum, a range of values; the Tel Aviv rents by rooms, the Z (0 to 2 is
# not to scale); the bottom of a bar = the lowest rent, the top = the highest, the bold line = the mean; the example 6
# rooms 4,500 / 8,000 / 6,500; the mean isn't always in the middle (expensive flats pull it up; one flat at 2,500, the
# rest 4 to 4.5); Ella (rents 2 rooms, rents out 5) and Daniel (rents 1, rents out 4): "rent" vs "rent out"; Ella at most
# 7,500 - 2,500 = 5,000, at least 4,500 - 4,500 = 0; Daniel 7,000 - 2,000 = 5,000 and 4,000 - 4,000 = 0; so the difference
# can be 0, 2,500, 5,000 but not 5,500; the same data as a table with three numbers in a cell (position = meaning), easy
# to add cities to a table, easier to compare cities in a chart. Regions (the same seg): the health insurance by height and
# weight, the numbers inside = thousands a year (4 to 12), the example 100 kg and 174 cm -> 6,000. ADDED: "to get the
# most, take the biggest income and the smallest cost" said as a rule with the why; a second reading of the table;
# a second insured person (80 kg, 190 cm). The extremes (min-max): topic 21, a REMINDER; the mean: topic 25, a REMINDER.
# =================================================================================================================
RC = MA.rent_chart()
r_c1 = CH('r_c1', RC, 345, 92, 740)
r_n1 = I('r_n1', 'Across: $\\ $rooms. $\\ $Up: $\\ $thousands of shekels', size=28, col=1)
r_n2 = I('r_n2', 'The Z: $\\ $from $0$ to $2$ is not to scale', size=28, col=1)
r_c2 = CH('r_c2', RC, 345, 92, 740, [('lo', MA.rent_chart(hl=[(5, 'min')])), ('hi', MA.rent_chart(hl=[(5, 'min'), (5, 'max')])),
                                     ('mn', MA.rent_chart(hl=[(5, 'min'), (5, 'max'), (5, 'mean')]))])
r_n3 = I('r_n3', 'Bottom of a bar: $\\ $the lowest rent', size=28, col=1)
r_n4 = I('r_n4', 'Top: $\\ $the highest rent', size=28, col=1)
r_n5 = I('r_n5', 'The bold line: $\\ $the mean rent', size=28, col=1)
r_n6 = I('r_n6', '$6$ rooms: $\\ 4{,}500$ to $8{,}000$, $\\ $mean $6{,}500$', size=28, col=1)
r_c3 = CH('r_c3', RC, 345, 92, 740, [('b', MA.rent_chart(hl=[(1, 'bar')]))])
r_n7 = I('r_n7', '$2$ rooms: $\\ 2{,}500$ to $4{,}500$, $\\ $the middle is $3{,}500$', size=28, col=1)
r_n8 = I('r_n8', 'The mean is $4{,}000$: $\\ $above the middle', size=28, col=1)
r_n9 = I('r_n9', 'One cheap flat, many expensive ones: $\\ $the mean goes up', size=28, col=1)
r_c4 = CH('r_c4', RC, 345, 92, 700, [('e1', MA.rent_chart(hl=[(4, 'max'), (1, 'min')])),
                                     ('e2', MA.rent_chart(hl=[(4, 'max'), (1, 'min'), (4, 'min'), (1, 'max')]))])
r_q1 = I('r_q1', 'Ella rents a $2$-room flat and rents out a $5$-room flat.', size=24, col=1)
r_q2 = I('r_q2', 'Daniel rents a $1$-room flat and rents out a $4$-room flat.', size=24, col=1)
r_q3 = I('r_q3', 'Each one saves the difference every month. Which cannot be the difference between their savings?', size=24, col=1)
r_q4 = I('r_q4', '$(1)\\ 0\\quad(2)\\ 2{,}500\\quad(3)\\ 5{,}000\\quad(4)\\ 5{,}500$', size=26, col=1)
r_e1 = I('r_e1', 'Rent out: $\\ $she gets the money. $\\ $Rent: $\\ $she pays.', size=26)
r_e2 = IH('r_e2', 'Ella, most: $\\ 7{,}500-2{,}500=5{,}000$', size=28)
r_e3 = IH('r_e3', 'Ella, least: $\\ 4{,}500-4{,}500=0$', size=28)
r_c5 = CH('r_c5', RC, 345, 92, 700, [('d1', MA.rent_chart(hl=[(3, 'max'), (0, 'min')])),
                                     ('d2', MA.rent_chart(hl=[(3, 'max'), (0, 'min'), (3, 'min'), (0, 'max')]))])
r_d1 = IH('r_d1', 'Daniel, most: $\\ 7{,}000-2{,}000=5{,}000$', size=28)
r_d2 = IH('r_d2', 'Daniel, least: $\\ 4{,}000-4{,}000=0$', size=28)
r_d3 = I('r_d3', 'Each one saves from $0$ to $5{,}000$', size=28, col=1)
r_d4 = I('r_d4', 'The biggest difference: $\\ 5{,}000-0=5{,}000$', size=28, col=1)
r_d5 = I('r_d5', '$5{,}500$ is impossible', size=28, col=1)
RT = MA.rent_table()
r_c6 = CH('r_c6', RT, 345, 92, 1000, [('c', MA.rent_table(hl=[(0, 1)]))])
r_t1 = I('r_t1', 'Three numbers in a cell: $\\ $the place tells the meaning', size=30)
r_t2 = I('r_t2', '$1$ room: $\\ $lowest $2$, $\\ $mean $3$, $\\ $highest $4$ (thousands)', size=30)
r_t3 = I('r_t3', '$4$ rooms: $\\ $lowest $4$, $\\ $mean $5.5$, $\\ $highest $7$', size=30)
RT3 = MA.rent_table(cities=(MA.RENT, MA.RENT_J, MA.RENT_E))
r_c7 = CH('r_c7', RT3, 345, 92, 860)
r_t4 = I('r_t4', 'A table: $\\ $easy to add more cities', size=28, col=1)
RC3 = MA.rent_chart(series=[MA.RENT, MA.RENT_J, MA.RENT_E], legend='top', title='Monthly rent, 2012')
r_c8 = CH('r_c8', RC3, 345, 92, 740)
r_t5 = I('r_t5', 'A chart with three cities: $\\ $busier', size=28, col=1)
r_t6 = I('r_t6', 'But it is easy to compare: $\\ $higher or lower bars', size=28, col=1)

video('ch52-range', 'lesson', slides=[
    S('Range Chart',
      L("Welcome back, and now the range chart. A range is everything from the smallest value to the biggest one."),
      L("The exam loves the smallest and the biggest possible values, in every topic. In charts too.")),
    S('Rents in Tel Aviv',
      L("This chart shows a survey of the monthly rent of flats in Tel Aviv in two thousand twelve, by the number of rooms."),
      L("Across the bottom, the number of rooms. Going up, the rent, in thousands of shekels.", show(r_n1, 'Across the bottom')),
      L("Look at the bottom of the axis. There's a Z. Remember, it tells us that from zero to two is not to scale.",
        show(r_n2, "There's a Z")), pre=[r_c1['base']]),
    S('Bottom, top, mean',
      L("Each bar here is a range. The bottom of a bar is the lowest rent for that number of rooms.",
        show(r_c2['lo'], 'The bottom of a bar'), show(r_n3, 'the lowest rent')),
      L("The top of the bar is the highest rent.", show(r_c2['hi'], 'The top of the bar'), show(r_n4, 'the highest rent')),
      L("And the bold line inside the bar is the mean rent, the average.", show(r_c2['mn'], 'the bold line inside'),
        show(r_n5, 'the mean rent')),
      L("The example says, in six-room flats the lowest rent was four thousand five hundred. The highest was eight "
        "thousand, and the mean was six thousand five hundred.", show(r_n6, 'in six-room flats')),
      L("And on the chart, the six-room bar goes from four and a half to eight, with the bold line at six and a half. It "
        "matches."), pre=[r_c2['base']]),
    S('The mean is not the middle',
      L("Is the mean always in the middle of the bar? No. Look at two rooms.", show(r_c3['b'], 'Look at two rooms')),
      L("It goes from two thousand five hundred to four thousand five hundred. The middle of that is three thousand five "
        "hundred.", show(r_n7, 'The middle of that')),
      L("But the mean is four thousand, higher than the middle. Why?", show(r_n8, 'But the mean is four thousand')),
      L("Say there's just one cheap flat, at two thousand five hundred. All the other flats cost four thousand or more. "
        "The many expensive flats pull the mean up.", show(r_n9, 'pull the mean up')),
      L("So the bar shows where the rents start and end. The bold line shows the average. They're different things."),
      pre=[r_c3['base']]),
    S('Ella and Daniel',
      L("Here's a sample question. Ella rents a two-room flat, and she rents out a five-room flat.", show(r_q1, 'Ella rents')),
      L("Daniel rents a one-room flat, and he rents out a four-room flat.", show(r_q2, 'Daniel rents')),
      L("Each one saves the difference between the two rents every month. Which of these cannot be the difference between "
        "their savings?", show(r_q3, 'Each one saves'), show(r_q4, 'cannot be the difference')),
      L("First, what's the difference between rent and rent out? Ella owns the five-room flat. She rents it out, so she "
        "gets the money."),
      L("And she lives in the two-room flat. She rents it, so she pays. So her saving is what she gets, minus what she "
        "pays.", show(r_e1, 'So her saving is')),
      L("What's the most Ella can save? She gets the most, and she pays the least. The most for five rooms is seven "
        "thousand five hundred.", show(r_c4['e1'], 'The most for five rooms')),
      L("The least for two rooms is two thousand five hundred. Seven thousand five hundred minus two thousand five hundred "
        "is five thousand.", show(r_e2, 'Seven thousand five hundred minus')),
      L("And the least she can save? She gets the least, four thousand five hundred. And she pays the most, also four "
        "thousand five hundred.", show(r_c4['e2'], 'She gets the least')),
      L("Four thousand five hundred minus four thousand five hundred is zero. So Ella saves anywhere from zero to five "
        "thousand.", show(r_e3, 'minus four thousand five hundred is zero')), pre=[r_c4['base']]),
    S("Daniel's savings",
      L("Now Daniel, the same way. The most he can save: he gets the most for four rooms, seven thousand. He pays the "
        "least for one room, two thousand.", show(r_c5['d1'], 'he gets the most for four rooms')),
      L("Seven thousand minus two thousand is five thousand.", show(r_d1, 'Seven thousand minus two thousand')),
      L("The least: he gets four thousand, and he pays the most for one room, also four thousand. That's zero.",
        show(r_c5['d2'], 'he gets four thousand'), show(r_d2, "That's zero")),
      L("So each one saves something from zero to five thousand.", show(r_d3, 'from zero to five thousand')),
      L("Now the question. Can the difference between them be zero? Yes, if they both save the same amount."),
      L("Two thousand five hundred? Yes, for example five thousand and two thousand five hundred. Five thousand? Yes, if "
        "one saves five thousand and the other saves zero."),
      L("And five thousand five hundred? The biggest difference is when one saves the most and the other saves the least. "
        "Five thousand minus zero is only five thousand.", show(r_d4, 'The biggest difference')),
      L("So five thousand five hundred is impossible. That's choice number four.", show(r_d5, 'is impossible')),
      pre=[r_c5['base']]),
    S('The same data in a table',
      L("The same data can also come as a table. Then each cell has three numbers, and the place of each number tells its "
        "meaning.", show(r_t1, 'each cell has three numbers')),
      L("The note says, top left is the lowest rent, the centre is the mean, and bottom right is the highest."),
      L("So one room: the lowest is two, the mean is three, and the highest is four, in thousands. Just like the bar.",
        show(r_c6['c'], 'So one room'), show(r_t2, 'the lowest is two')),
      L("Four rooms: the lowest is four, the mean is five and a half, and the highest is seven.", show(r_t3, 'Four rooms')),
      L("Tables like this, with two or three numbers in a cell, are common on the exam. So always read the note."),
      pre=[r_c6['base']]),
    S('Table or chart?',
      L("Which is better? In a table, it's easy to add more cities. Each city is one more row.", show(r_t4, 'easy to add more cities')),
      pre=[r_c7['base']]),
    S('Three cities',
      L("In a chart, three cities make three bars for each number of rooms. It gets busy.", show(r_t5, 'It gets busy')),
      L("But it's easy to compare. We see right away which city has higher bars.", show(r_t6, "it's easy to compare")),
      L("I'll see you in the next video."), pre=[r_c8['base']]),
])
# (5.1 minutes: one video)


# ------------------------------------------------------------------------------------------------ ch52-regions (lesson)
INS = MA.ins_chart()
g_c1 = CH('g_c1', INS, 345, 92, 740, [
    ('w', MA.ins_chart(marks=[('hline', 100, '100 kg')])),
    ('h', MA.ins_chart(marks=[('hline', 100, '100 kg'), ('guide', 174, 100)]))])
g_c0 = CH('g_c0', INS, 345, 92, 740)
g_n1 = I('g_n1', 'Across: $\\ $height. $\\ $Up: $\\ $weight.', size=28, col=1)
g_n2 = I('g_n2', 'The number in an area: $\\ $the yearly cost, in thousands', size=28, col=1)
g_n3 = I('g_n3', 'From $4{,}000$ to $12{,}000$ shekels a year', size=28, col=1)
g_n4 = I('g_n4', '"For example: an insured person who weighs 100 kg and is 174 cm tall pays 6,000 shekels a year."', size=24, col=1)
g_n5 = I('g_n5', 'The point falls in the striped area: $\\ 6$, $\\ $so $6{,}000$', size=28, col=1)
g_c2 = CH('g_c2', INS, 345, 92, 740, [('p', MA.ins_chart(marks=[('guide', 190, 80)]))])
g_n6 = I('g_n6', '$80$ kg, $\\ 190$ cm: $\\ $the area $4$, $\\ $so $4{,}000$', size=28, col=1)
g_n7 = I('g_n7', 'Height and weight, $\\ $the point, $\\ $its area, $\\ $the price', size=28, col=1)

video('ch52-regions', 'lesson', slides=[
    S('Regions Chart',
      L("Welcome back. Here's another kind of range chart. This time the ranges are areas on the axes."),
      L("It's not points and not bars. Each area of the chart stands for a range.")),
    S('Health insurance',
      L("This chart shows the cost of health insurance, by the height and the weight of the insured person."),
      L("Across the bottom we have the height, in centimetres. Going up, the weight, in kilograms.", show(g_n1, 'Across the bottom')),
      L("The numbers inside the areas are the yearly cost, in thousands of shekels. So four is not four shekels. It's four "
        "thousand.", show(g_n2, 'The numbers inside the areas')),
      L("The prices go from four thousand to twelve thousand shekels a year.", show(g_n3, 'from four thousand to twelve')),
      pre=[g_c0['base']]),
    S('Check the example',
      L("The example always helps us check our reading. It says, a person who weighs a hundred kilograms, and is a hundred "
        "seventy-four centimetres tall, pays six thousand shekels a year.", show(g_n4, 'It says')),
      L("A hundred kilograms is somewhere on this line, across the chart.", show(g_c1['w'], 'on this line')),
      L("A hundred seventy-four centimetres is somewhere on this line, going up. Where they cross is our person.",
        show(g_c1['h'], 'Where they cross')),
      L("The point falls in the striped area, with the six. So six thousand shekels. It matches the example.",
        show(g_n5, 'The point falls in the striped area')), pre=[g_c1['base']]),
    S('Any insured person',
      L("Let's read one more person. Eighty kilograms, and a hundred ninety centimetres tall."),
      L("We go up from a hundred ninety, and across from eighty. The point falls in the area with the four. So this person "
        "pays four thousand shekels.", show(g_c2['p'], 'The point falls in the area'), show(g_n6, 'pays four thousand')),
      L("So for anyone, we find the point of the height and the weight. The area it falls in gives the price.",
        show(g_n7, 'we find the point')),
      L("That's it for range charts. I'll see you in the next video."), pre=[g_c2['base']]),
])


# =================================================================================================================
# ch52-circle (lesson)
# Hebrew (seg08, all of it): a common chart, different from the others; the same website story; the hours round the
# circle, the visitors = the circles (500, 400, 300 ...), the dark areas = where most visitors are that hour (the strips
# of the continuous chart); the example 9:00 -> 300, 9-10 forum; it's a coordinate system bent round (points, bars, a
# line); the two charts are the same (12:00 a bit above 300 in both; 12-16 explanations, the outer ring); the question:
# the latest hour with visitors in the practice area: the arc ends at 20:00, but a dark area = where MOST visitors are,
# not all of them -> it can't be known; cut it open and unfold it -> the same chart on axes. ADDED: "most" with numbers
# (more than half: 300 visitors, 160 in the forum, the other 140 can be anywhere); the trap said at the step. NEW.
# =================================================================================================================
CIRC = MA.site_circle()
c_c1 = CH('c_c1', CIRC, 345, 85, 700, [('h9', MA.site_circle(guide_hours=[9], highlight_spans=[(2, 9, 10)]))])
c_c0 = CH('c_c0', CIRC, 345, 85, 700)
c_n1 = I('c_n1', 'The hours go round the circle', size=28, col=1)
c_n2 = I('c_n2', 'The circles: $\\ 100,\\ 200,\\ \\ldots,\\ 500$ visitors', size=28, col=1)
c_n3 = I('c_n3', 'The dark rings: $\\ $where most visitors are', size=28, col=1)
c_n4 = I('c_n4', '"For example: at 9:00 there were 300 visitors on the site. Between 9:00 and 10:00, most of them were in the forum."', size=24, col=1)
c_n5 = I('c_n5', '9:00: $\\ $the line is on the $300$ circle', size=28, col=1)
c_p = CH('c_p', MA.site_circle(style='points', show_band_names=False, bands=()), 345, 92, 390)
c_b = CH('c_b', MA.site_circle(style='bars', show_band_names=False, bands=()), 765, 92, 390)
c_l = CH('c_l', MA.site_circle(style='curve', show_band_names=False, bands=()), 1185, 92, 390)
for _x in (c_b, c_l): _x['base'].pop('_chart')
c_n6 = I('c_n6', 'Points, bars, a line: $\\ $all of them in a circle', size=30)
c_n7 = I('c_n7', 'A circle chart $=$ axes bent into a circle', size=30)
c_k1 = CH('c_k1', MA.site_curve(), 345, 110, 640, [('g', MA.site_curve(marks=[('guide', 12, 320)])), ('s', MA.site_curve(marks=[('guide', 12, 320), ('col', 12, 16)]))])
c_k2 = CH('c_k2', MA.site_circle(show_band_names=False), 1030, 85, 500, [('g', MA.site_circle(show_band_names=False, guide_hours=[12])),
                                                                          ('s', MA.site_circle(show_band_names=False, guide_hours=[12], highlight_spans=[(0, 12, 16)]))])
c_k2['base'].pop('_chart')
c_n8 = I('c_n8', '12:00: $\\ $a bit above $300$, $\\ $in both charts', size=28)
c_n9 = I('c_n9', '12:00 to 16:00: $\\ $explanations, $\\ $in both charts', size=28)
c_c3 = CH('c_c3', CIRC, 345, 85, 700, [('pr', MA.site_circle(highlight_spans=[(1, 10, 12), (1, 18, 20)]))])
c_q1 = I('c_q1', 'What is the latest hour at which there are visitors in the practice area of the site?', size=26, col=1)
c_n10 = I('c_n10', 'The practice ring ends at 20:00. $\\ $Is that the answer?', size=28, col=1)
c_n11 = I('c_n11', 'Dark $=$ where MOST visitors are, $\\ $not all of them', size=28, col=1)
c_n12 = IH('c_n12', '$300$ visitors, $\\ 160$ in the forum', size=28, col=1)
c_n13 = I('c_n13', 'So the latest hour cannot be known', size=28, col=1)
c_c4 = CH('c_c4', CIRC, 345, 85, 700)
c_n14 = I('c_n14', 'Cut the circle open and unfold it: $\\ $a chart on axes', size=28, col=1)

video('ch52-circle', 'lesson', slides=[
    S('Circle Chart',
      L("Welcome back, and now the circle chart. It comes up quite a lot on the exam."),
      L("It looks different from everything we've seen. But we'll see that it's an old friend.")),
    S('The website again',
      L("We know the story already. It's the visitors on the Psycho website, over twenty-four hours."),
      L("The hours go round the circle, like a clock. Zero at the top.", show(c_n1, 'The hours go round the circle')),
      L("The number of visitors is shown by the circles. A hundred, two hundred, up to five hundred on the big circle.",
        show(c_n2, 'shown by the circles')),
      L("The dark rings outside show where most of the visitors are in each hour. They're the strips from the last "
        "chart, bent round the circle.", show(c_n3, 'The dark rings outside')),
      L("From the outside in, the rings are explanations, practice, forum, and other."), pre=[c_c0['base']]),
    S('Check the example',
      L("The example says, at nine o'clock there were three hundred visitors. And between nine and ten, most of them were "
        "in the forum.", show(c_n4, 'The example says')),
      L("Let's find nine o'clock on the clock. We go in along that line, to the teal curve. It's on the circle of three "
        "hundred.", show(c_c1['h9'], 'We go in along that line'), show(c_n5, 'on the circle of three')),
      L("And between nine and ten, the dark part is in the third ring. The third ring is the forum. It matches."),
      pre=[c_c1['base']]),
    S('Axes in a circle',
      L("Notice, every chart we've seen so far, except the table, was on axes. Here the axes are just bent into a circle.",
        show(c_n7, 'bent into a circle')),
      L("So the circle chart can have points, like points on axes. Or bars, each bar going out to its value.",
        pt('c_p', 'can have points')),
      L("Or one continuous line, like here.", show(c_n6, 'one continuous line')), pre=[c_p['base'], c_b['base'], c_l['base']]),
    S('Two identical charts',
      L("Here's the continuous chart from the last lesson, next to the circle chart. They show exactly the same data."),
      L("At twelve o'clock, the continuous line is a bit above three hundred. About three hundred twenty.",
        show(c_k1['g'], 'a bit above three hundred')),
      L("In the circle, at twelve, the curve is also just past the three hundred circle.", show(c_n8, 'the curve is also'),
        show(c_k2['g'], 'just past the three hundred')),
      L("And from twelve to sixteen, most visitors were in the explanations. Below the chart it's the explanations strip. "
        "In the circle it's the outer ring.", show(c_k1['s'], 'from twelve to sixteen'), show(c_k2['s'], 'In the circle it'),
        show(c_n9, "it's the outer ring")), pre=[c_k1['base'], c_k2['base']]),
    S('The latest hour?',
      L("Now a sample question. What is the latest hour at which there are visitors in the practice area?",
        show(c_q1, 'What is the latest hour')),
      L("The practice ring is the second one. Going round, its last dark part ends at twenty o'clock.",
        show(c_c3['pr'], 'its last dark part ends'), show(c_n10, 'ends at twenty')),
      L("So is the answer twenty o'clock? A lot of students mark it. But let's read what the dark areas mean."),
      L("They show where most of the visitors are in that hour. Most, not all.", show(c_n11, 'Most, not all')),
      L("Say there are three hundred visitors, and a hundred sixty are in the forum. That's more than half, but it still "
        "doesn't mean everyone.", show(c_n12, 'three hundred visitors')),
      L("The other hundred forty can be anywhere, also in the practice area. So after twenty o'clock, some people may "
        "still practise. Or maybe nobody does."),
      L("The chart can't tell us. So the latest hour cannot be known.", show(c_n13, 'cannot be known')),
      pre=[c_c3['base']]),
    S('Unfold it',
      L("So the circle chart is just a chart on axes. The circles are the lines of the value axis, bent round.",
        pt('c_c4', 'The circles are the lines')),
      L("We could cut the circle open at the top and unfold it. Then we'd get the same chart on straight axes.",
        show(c_n14, 'We could cut the circle open')),
      L("I'll see you in the next video."), pre=[c_c4['base']]),
])


# =================================================================================================================
# ch52-cumulative (lesson) and ch52-change (lesson)
# Hebrew (seg09): a cumulative graph = each point is the sum of everything up to it; one month = this point minus the one
# before; Pixeltech's cumulative income, Jan-Jun 2013, thousands; the example May = 20,000 but the graph shows 70 (= Jan
# to May together; April 50 = up to April); the bank account you only deposit into (10, 20, 50, 50, 70); May 70 - 50 =
# 20; the question "no income at all" = the flat part -> April; the total = the last point, 80,000 (up to June, not in
# June); not very common, better met here. ADDED: one more month read (March 50 - 20 = 30), the trap said at the step.
# Hebrew (seg10): very rare but hard; the values are CHANGES compared with the week before; ignore the line, look only
# at the points; "Green Light" volunteers, 10 weeks; week 2: +10 (100 -> 110); week 3 the line goes down but +5 is a
# rise; the question "no change" = 0 -> weeks 5, 9, 10 (the line falls into 5 and rises into 9: ignore it); from 75 at
# week 2: +5 -> 80, +5 -> 85, 0 -> 85, -10 -> 75; "watch it again if you need to". ADDED: the running count written row
# by row. NEW (both).
# =================================================================================================================
PIX = MA.pix_chart()
u_c1 = CH('u_c1', PIX, 345, 92, 740, [('may', MA.pix_chart(marks=[('guide', 4, 70, '70')]))])
u_n1 = I('u_n1', 'Each point: $\\ $the sum of everything up to it', size=28, col=1)
u_n2 = I('u_n2', '"For example: the income of Pixeltech in May was 20,000 shekels."', size=24, col=1)
u_n3 = I('u_n3', 'But at May the graph shows $70$', size=28, col=1)
u_c2 = CH('u_c2', PIX, 345, 92, 740, [('a', MA.pix_chart(marks=[('guide', 3, 50, '50'), ('guide', 4, 70, '70')])),
                                      ('b', MA.pix_chart(marks=[('guide', 3, 50, '50'), ('guide', 4, 70, '70'), ('brace', 4.2, 50, 70, '20')]))])
u_n4 = I('u_n4', '$70 =$ January to May together', size=28, col=1)
u_n5 = I('u_n5', '$50 =$ everything up to April', size=28, col=1)
u_n6 = IH('u_n6', 'May: $\\ 70-50=20$', size=30, col=1)
u_n7 = IH('u_n7', 'March: $\\ 50-20=30$', size=30, col=1)
u_n8 = I('u_n8', 'One month $=$ this point minus the one before', size=28, col=1)
u_t = TBL('u_t', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], ['in', 'balance'], [
    ('a', [('c', 1, 0, '10'), ('c', 0, 0, '+10')]), ('b', [('c', 1, 1, '20'), ('c', 0, 1, '+10')]), ('c', [('c', 1, 2, '50'), ('c', 0, 2, '+30')]),
    ('d', [('c', 1, 3, '50'), ('c', 0, 3, '+0')]), ('e', [('c', 1, 4, '70'), ('c', 0, 4, '+20')])],
    colw=110, labw=150, rowh=60, size=28, w=760, title='A bank account (thousands)')
for _k, _it in u_t.items():
    if _k == 'line': _it.update(_x=345, _y=455)
u_c3 = CH('u_c3', PIX, 345, 92, 600)
u_c4 = CH('u_c4', PIX, 345, 92, 740, [('f', MA.pix_chart(marks=[('seg', 2, 50, 3, 50)]))])
u_q1 = I('u_q1', 'In which of the months did Pixeltech have no income at all?', size=26, col=1)
u_n9 = I('u_n9', 'Flat: $\\ $nothing was added', size=28, col=1)
u_n10 = IH('u_n10', 'April: $\\ 50-50=0$', size=30, col=1)
u_c5 = CH('u_c5', PIX, 345, 92, 740, [('t', MA.pix_chart(marks=[('guide', 5, 80, '80')]))])
u_q2 = I('u_q2', "What was Pixeltech's total income in all the months described?", size=26, col=1)
u_n11 = I('u_n11', 'The last point is the total: $\\ 80{,}000$', size=28, col=1)
u_n12 = I('u_n12', '$80$ at June $=$ up to June, $\\ $not in June', size=28, col=1)

video('ch52-cumulative', 'lesson', slides=[
    S('Cumulative Graph',
      L("Welcome back, and now the cumulative graph. Cumulative means adding up."),
      L("In this graph, each point is not its own value. It's the sum of everything up to it.")),
    S('Pixeltech',
      L("This graph shows the cumulative income of a company, Pixeltech, in the first half of two thousand thirteen."),
      L("Across the bottom, the months. Going up, the cumulative income, in thousands of shekels. So eighty means eighty "
        "thousand shekels."),
      L("The example says, Pixeltech's income in May was twenty thousand shekels.", show(u_n2, 'The example says')),
      L("Let's check. We go to May, and up to the line. We get to seventy. Seventy, not twenty. Why?",
        show(u_c1['may'], 'We go to May'), show(u_n3, 'Seventy, not twenty')),
      L("Because it's cumulative. Each point is the sum of everything up to it.", show(u_n1, 'Each point is the sum')),
      pre=[u_c1['base']]),
    S('One month alone',
      L("So the seventy at May is all the income from January to May together.", show(u_c2['a'], 'all the income from January'),
        show(u_n4, 'from January to May together')),
      L("And the fifty at April is all the income up to April.", show(u_n5, 'up to April')),
      L("How much came in May alone? What was added from April to May. Seventy minus fifty is twenty. That's the twenty of "
        "the example.", show(u_c2['b'], 'Seventy minus fifty'), show(u_n6, 'Seventy minus fifty')),
      L("Let's try March. At March it's fifty, and at February it's twenty. Fifty minus twenty is thirty. So thirty "
        "thousand came in March.", show(u_n7, 'Fifty minus twenty')),
      L("So one month is this point, minus the point before it.", show(u_n8, 'this point, minus')), pre=[u_c2['base']]),
    S('Like a bank account',
      L("Think of a bank account that we only put money into. It started at zero."),
      L("In January we put in ten thousand. The balance is ten.", show(u_t['line'], 'In January'), show(u_t['a'], 'The balance is ten')),
      L("In February we put in ten more. The balance is twenty.", show(u_t['b'], 'The balance is twenty')),
      L("In March, thirty more. The balance is fifty.", show(u_t['c'], 'The balance is fifty')),
      L("In April we put in nothing. The balance stays fifty.", show(u_t['d'], 'The balance stays fifty')),
      L("And in May, twenty more. The balance is seventy. The graph shows the balance, not what we put in each month.",
        show(u_t['e'], 'The balance is seventy')), pre=[u_c3['base']]),
    S('No income?',
      L("Here's a sample question. In which month did Pixeltech have no income at all?", show(u_q1, 'In which month')),
      L("We can see it straight away. From March to April the line is flat.", show(u_c4['f'], 'the line is flat')),
      L("Flat means nothing was added. Up to March, fifty. Up to April, also fifty. Fifty minus fifty is zero.",
        show(u_n9, 'nothing was added'), show(u_n10, 'Fifty minus fifty')),
      L("So in April there was no income. The answer is April."), pre=[u_c4['base']]),
    S('The total',
      L("One more question. What was the total income in all the months?", show(u_q2, 'What was the total income')),
      L("Do we add January, February, March, and so on? No. The graph already adds them up."),
      L("The last point is the total. At June it's eighty, so eighty thousand shekels.", show(u_c5['t'], 'At June'),
        show(u_n11, 'The last point is the total')),
      L("Careful, eighty is not the income in June. It's everything up to June.", show(u_n12, 'up to June')),
      L("The cumulative graph is not very common. But it's better to meet it here than for the first time on the exam."),
      L("I'll see you in the next video."), pre=[u_c5['base']]),
])

# ------------------------------------------------------------------------------------------------ ch52-change
VOLC = MA.vol_chart()
VOLN = MA.vol_chart(show_line=False)
h_c1 = CH('h_c1', VOLC, 345, 92, 740, [('w2', MA.vol_chart(hl=[1]))])
h_n1 = I('h_n1', 'Each point: $\\ $the change from the week before', size=28, col=1)
h_n2 = I('h_n2', 'Above $0$: $\\ $volunteers joined. $\\ $Below $0$: $\\ $they left.', size=28, col=1)
h_n3 = I('h_n3', '"For example: at the end of the second week there were 10 more volunteers than at the end of the first week."', size=24, col=1)
h_n4 = IH('h_n4', 'week $1$: $\\ 100$, $\\ $week $2$: $\\ 110$', size=28, col=1)
h_c2 = CH('h_c2', VOLC, 345, 92, 740, [('w3', MA.vol_chart(hl=[2]))])
h_n5 = I('h_n5', 'Week $3$: $\\ $the line goes down, $\\ $but $+5$', size=28, col=1)
h_n6 = IH('h_n6', '$110+5=115$: $\\ $a rise', size=28, col=1)
h_n7 = I('h_n7', 'Ignore the line. $\\ $Look only at the points.', size=28, col=1)
h_c3 = CH('h_c3', VOLC, 345, 92, 740, [('!nl', VOLN), ('z', MA.vol_chart(show_line=False, hl=[4, 8, 9]))])
h_q1 = I('h_q1', 'In how many of the weeks was there no change in the number of volunteers?', size=26, col=1)
h_n8 = I('h_n8', 'No change: $\\ $the point is at $0$', size=28, col=1)
h_n9 = I('h_n9', 'Weeks $5,\\ 9,\\ 10$: $\\ $three weeks', size=28, col=1)
h_c4 = CH('h_c4', VOLC, 345, 92, 740, [('z', MA.vol_chart(hl=[4, 8]))])
h_n10 = I('h_n10', 'Into week $5$ the line falls, $\\ $but the change is $0$', size=28, col=1)
h_n11 = I('h_n11', 'Into week $9$ the line rises, $\\ $but the change is $0$', size=28, col=1)
h_c5 = CH('h_c5', VOLN, 345, 92, 700, [('a', MA.vol_chart(show_line=False, hl=[2])), ('b', MA.vol_chart(show_line=False, hl=[2, 3])),
                                       ('c', MA.vol_chart(show_line=False, hl=[2, 3, 4])), ('d', MA.vol_chart(show_line=False, hl=[2, 3, 4, 5]))])
h_q2 = I('h_q2', 'At the end of week $2$ there were $75$ volunteers. How many were there at the end of week $6$?', size=26, col=1)
h_r1 = IH('h_r1', 'week $3$: $\\ 75+5=80$', size=28, col=1)
h_r2 = IH('h_r2', 'week $4$: $\\ 80+5=85$', size=28, col=1)
h_r3 = IH('h_r3', 'week $5$: $\\ 85+0=85$', size=28, col=1)
h_r4 = IH('h_r4', 'week $6$: $\\ 85-10=75$', size=28, col=1)

video('ch52-change', 'lesson', slides=[
    S('Change Graph',
      L("Welcome back, and now the change graph. It's very rare on the exam. But it's hard and confusing, so it's good to "
        "know its trick before we meet it."),
      L("In a change graph, the values are not amounts. Each value is a change.")),
    S('Values are changes',
      L("This graph shows the volunteers in an organization called Green Light, over ten weeks. Each point is the change at "
        "the end of a week, compared with the end of the week before.", show(h_n1, 'compared with the end of the week before')),
      L("Above zero, volunteers joined. Below zero, volunteers left.", show(h_n2, 'Above zero')),
      L("The example says, at the end of the second week there were ten more volunteers than at the end of the first week.",
        show(h_n3, 'The example says')),
      L("And the point of week two is at plus ten. Ten more than the week before. It matches.", show(h_c1['w2'], 'the point of week two')),
      L("Let's say there were a hundred volunteers at the end of week one. Then at the end of week two there were a hundred "
        "ten.", show(h_n4, 'a hundred volunteers')), pre=[h_c1['base']]),
    S('Down, but up',
      L("Here's the confusing part. Look at week three. The line goes down into it. So it feels like volunteers left.",
        show(h_c2['w3'], 'Look at week three')),
      L("But the point of week three says plus five. Plus five means five more volunteers than the week before.",
        show(h_n5, 'plus five')),
      L("So it's a rise. A hundred ten plus five is a hundred fifteen.", show(h_n6, 'A hundred ten plus five')),
      L("That's why we ignore the line. We look only at the points.", show(h_n7, 'we ignore the line')), pre=[h_c2['base']]),
    S('No change?',
      L("Here's a sample question. In how many of the weeks was there no change in the number of volunteers?",
        show(h_q1, 'In how many of the weeks')),
      L("What does no change mean? The change was zero. So we look for points at zero.", show(h_n8, 'The change was zero')),
      L("Let's take the line away, so it doesn't confuse us.", show(h_c3['nl'], 'take the line away')),
      L("The points at zero are weeks five, nine and ten. That's three weeks.", show(h_c3['z'], 'weeks five, nine and ten'),
        show(h_n9, "That's three weeks")), pre=[h_c3['base']]),
    S('The line fools us',
      L("Now let's bring the line back, to see how it fools us."),
      L("Into week five, the line falls. It looks like a drop. But the point of week five is zero, so nothing changed. Week "
        "five ended with the same number as week four.", show(h_c4['z'], 'Into week five'), show(h_n10, 'the line falls')),
      L("Into week nine, the line rises. But the point is zero again. No change.", show(h_n11, 'Into week nine')),
      L("So the answer is three weeks."), pre=[h_c4['base']]),
    S('Week by week',
      L("One more question. At the end of week two there were seventy-five volunteers. How many were there at the end of "
        "week six?", show(h_q2, 'At the end of week two')),
      L("We start from seventy-five, and we add the changes one week at a time. Only the points, no line."),
      L("Week three is plus five. Seventy-five plus five is eighty.", show(h_c5['a'], 'Week three is plus five'),
        show(h_r1, 'Seventy-five plus five')),
      L("Week four is plus five again. Eighty plus five is eighty-five.", show(h_c5['b'], 'Week four is plus five'),
        show(h_r2, 'Eighty plus five')),
      L("Week five is zero. So it stays eighty-five.", show(h_c5['c'], 'Week five is zero'), show(h_r3, 'it stays eighty-five')),
      L("Week six is minus ten. Eighty-five minus ten is seventy-five.", show(h_c5['d'], 'Week six is minus ten'),
        show(h_r4, 'Eighty-five minus ten')),
      L("So at the end of week six there were seventy-five volunteers."),
      L("This graph is confusing, so watch this video again if you need to. And remember the one rule. Ignore the line, "
        "and look only at the points."),
      L("That's the last type of chart. Next, we'll solve full chart sets. I'll see you in the next video."),
      pre=[h_c5['base']]),
])


# =================================================================================================================
# the three chart sets (modulesV52b.py): our marks, drawn in each chart's own viewBox coordinates and appended to the
# chart (so OVL turns them into a see-through layer that sits exactly on the question's figure)
# =================================================================================================================
S1, S2, S3 = MB.S1, MB.S2, MB.S3
AM = CA.AMBER
TF = 'font-family="Helvetica Neue, Helvetica, Arial, sans-serif"'


def plus(svg, *extras):
    return svg[:svg.rindex('</svg>')] + ''.join(extras) + '</svg>'


def _ln(x1, y1, x2, y2, w=4, dash=None, col=AM):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" stroke-linecap="round"%s/>'
            % (x1, y1, x2, y2, col, w, ' stroke-dasharray="%s"' % dash if dash else ''))


def _ring(x, y, r=17, col=AM, w=3.5):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (x, y, r, col, w)


def _box(x, y, w, h, col=AM, sw=4, fill='none', op=None):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="%s"%s stroke="%s" stroke-width="%s"/>'
            % (x, y, w, h, fill, ' fill-opacity="%s"' % op if op else '', col, sw))


def _lab(x, y, t, size=20, anchor='middle'):
    w = len(t) * size * .56 + 16
    x0 = x - w / 2 if anchor == 'middle' else (x if anchor == 'start' else x - w)
    return (_box(x0, y - size * .95, w, size * 1.4, AM, 2, '#FFF7E6') +
            '<text x="%.1f" y="%.1f" text-anchor="middle" fill="#8A5A00" %s font-size="%d" font-weight="700">%s</text>'
            % (x0 + w / 2, y + size * .2, TF, size, t))


# chart 1 (soil samples): carbon across (c1x), hydrogen up (c1y)
c1x, c1y = MB.c1x, MB.c1y


def V1(c, lab=None):
    """a boundary line at carbon c% (standing up)"""
    return _ln(c1x(c), MB.C1_YT, c1x(c), MB.C1_YB, 4, '10 6') + (_lab(c1x(c), MB.C1_YT - 8, lab) if lab else '')


def H1(h, lab=None):
    """a boundary line at hydrogen h% (across)"""
    return _ln(MB.C1_X0, c1y(h), MB.C1_X1, c1y(h), 4, '10 6') + (_lab(MB.C1_X1 - 40, c1y(h) - 14, lab) if lab else '')


def R1(c, h, r=17): return _ring(c1x(c), c1y(h), r)


def SPAN1(planet, dy=0):
    """the carbon range of a planet: a thick line from its leftmost to its rightmost sample, at the samples' middle height"""
    pts = MB.C1[planet]; lo = min(pts); hi = max(pts)
    y = c1y(sum(h for c, h in pts) / len(pts)) + dy
    return _ln(c1x(lo[0]), y, c1x(hi[0]), y, 7) + _ring(c1x(lo[0]), c1y(lo[1]), 15) + _ring(c1x(hi[0]), c1y(hi[1]), 15)


def TREND1(planet):
    pts = sorted(MB.C1[planet])
    return ('<polyline points="%s" fill="none" stroke="%s" stroke-width="5" stroke-linejoin="round" stroke-opacity="0.8"/>'
            % (' '.join('%.1f,%.1f' % (c1x(c), c1y(h)) for c, h in pts), AM))


def SEG1(p1, p2):
    return _ln(c1x(p1[0]), c1y(p1[1]), c1x(p2[0]), c1y(p2[1]), 7)


# chart 2 (car races): the team rows and the year columns of the left table, the prize table on the right
def ROW2(team):
    y = MB.C2_TY + MB.C2_HH + MB.C2_RH * MB.TEAMS.index(team)
    return _box(MB.C2_TX + 2, y + 3, MB.C2_TW + 6 * MB.C2_YW - 4, MB.C2_RH - 6)


def CELL2(team, year):
    y = MB.C2_TY + MB.C2_HH + MB.C2_RH * MB.TEAMS.index(team); k = MB.YEARS.index(year)
    return _ring(MB.C2_TX + MB.C2_TW + MB.C2_YW * (k + .5), y + MB.C2_RH / 2, 22)


def COL2(year):
    k = MB.YEARS.index(year); x = MB.C2_TX + MB.C2_TW + MB.C2_YW * k
    return _box(x + 3, MB.C2_TY + 3, MB.C2_YW - 6, MB.C2_HH + 7 * MB.C2_RH - 6)


def PRIZE2(place):
    y = MB.C2_TY + MB.C2_HH + MB.C2_RH * (place - 1)
    return _box(MB.C2_PX + 3, y + 3, 92 + 136 - 6, MB.C2_RH - 6)


def PRIZES2(p1, p2):
    y1 = MB.C2_TY + MB.C2_HH + MB.C2_RH * (p1 - 1); y2 = MB.C2_TY + MB.C2_HH + MB.C2_RH * p2
    return _box(MB.C2_PX + 3, y1 + 3, 92 + 136 - 6, y2 - y1 - 6)


# chart 3 (weddings): the bars (c3x, c3y) and the pies above them (centre y 128, radius 56)
def BAR3(day, lab=None):
    k = MB.DAYS.index(day); x = MB.c3x(k); n = MB.GUESTS[day]
    return (_box(x - 44, MB.c3y(n) - 6, 88, MB.C3_YB - MB.c3y(n) + 6) + _ln(MB.C3_X0, MB.c3y(n), x - 44, MB.c3y(n), 3, '8 6') +
            (_lab(x, MB.c3y(n) - 18, lab) if lab else ''))


def PIE3(day): return _ring(MB.c3x(MB.DAYS.index(day)), 128, 62, AM, 5)


def SLICE3(day, part):
    """ring the label of one slice (0 groom only, 1 bride only, 2 shared) of a day's pie"""
    import math
    parts = MB.SPLIT[day]; a = -90.0
    for i, p in enumerate(parts):
        b = a + 360.0 * p / 100
        if i == part:
            m = math.radians((a + b) / 2); cx = MB.c3x(MB.DAYS.index(day))
            return _ring(cx + 56 * .58 * math.cos(m), 128 + 56 * .58 * math.sin(m), 17, AM, 4)
        a = b
    return ''


# ------------------------------------------------------------------------------------------------ ch52-practice-intro
# The course's own short lesson before the three guided sets (no Hebrew lesson; the Hebrew solution videos say these
# habits inside the questions). Everything here is a REMINDER of the intro lesson, except "each question stands alone"
# (the sets' own note) and "the answer is not among the choices -> stop and check" (her Hebrew, chart 1 question 1).
k_c1 = CH('k_c1', S1, 345, 92, 700)
k_n1 = I('k_n1', 'First $1$ to $1\\frac{1}{2}$ minutes: $\\ $the page and the chart', size=28, col=1)
k_n2 = I('k_n2', 'The axes, the units, the key, every note', size=28, col=1)
k_n3 = I('k_n3', 'Each question stands alone', size=28, col=1)
k_n4 = I('k_n4', 'Circle the key word of the question', size=28, col=1)
k_n5 = I('k_n5', "Your answer isn't a choice? $\\ $Stop and check", size=28, col=1)
k_n6 = I('k_n6', 'Most questions: $\\ $by eye. $\\ $Calculate only when you must.', size=28, col=1)

video('ch52-practice-intro', 'lesson', slides=[
    S('Solving a Chart Set',
      L("Welcome back. Now we'll solve three full chart sets, with all their questions."),
      L("Before we start, let's remember how we attack a set.")),
    S('How we attack a set',
      L("First, a minute or a minute and a half on the page itself, before any question.", show(k_n1, 'before any question')),
      L("We read the explanation, and we check the example in the chart. Then the axes, the units, the key, and every "
        "note.", show(k_n2, 'the axes, the units')),
      L("Here's the first chart we'll solve. Two axes, five planets in the key, and a note at the top.",
        pt('k_c1', 'Here\'s the first chart')),
      L("Then the questions. Each question stands alone. What one question tells us doesn't carry over to the next one.",
        show(k_n3, 'Each question stands alone')),
      L("In each question, circle the key word. Is it carbon, or hydrogen? Then we check exactly what they asked.",
        show(k_n4, 'circle the key word')),
      L("And if our answer isn't one of the choices, we don't panic. We stop, and we check the axis, the key and the "
        "question again.", show(k_n5, "isn't one of the choices")),
      L("Most chart questions are solved by eye. A line, a corner, a length, a slope. We calculate only when we must.",
        show(k_n6, 'solved by eye')),
      L("Let's start with the first chart."), pre=[k_c1['base']]),
])


# =================================================================================================================
# Chart set 1 (soil samples, scatter): solve-ch-q01 .. q05
# Hebrew (seg11, chart 1): q1 the boundary line at 60% carbon, count to the right; the pressure trap (the 60% of the
# hydrogen axis -> 1 sample, not a choice -> stop and check); q2 high carbon = the right side, low hydrogen = the bottom,
# by eye, the corner; q3 the range = the leftmost and the rightmost sample, a line for each planet, compare by eye ("one of
# the main ways we solve chart questions"); q4 "necessarily true": look at all four choices (the same idea: a direct or an
# inverse relation), one planet jumps out as a line, then each planet in detail; q5 circle "hydrogen", the mini-graphs
# come from the big chart, don't check graph by graph - rule out where they differ, start at the edges (below 10%: 3
# samples there in the Hebrew data; then the other edge). Course numbers (modulesV52b.py): 6 samples (the 59% ring on the
# line), Neptune's corner, Saturn's range, Mercury's line, graph (2). ch-q01's choices are put in the real-exam order in
# _t52_reading.py REORDER (3 in its own place): 7, 6, 3, 10 -> the answer 6 is choice number two.
# REMINDERS: counting with a line (ch52-scatter), the example check and the notes (ch52-intro), must / necessarily (topic
# 1, "one exception is enough"). NEW: the corner (q02), the range of a cloud of points (q03), the mini-graph method (q05).
# =================================================================================================================
q1r_pre, q1r = RPRE(1, MB._intro(MB.C1_INTRO, 1, 2), 'q1r', [('k', plus(S1, _ring(c1x(74), c1y(3), 18)))])
q1n1 = I('q1n1', 'Carbon: $\\ $across', size=26, col=1)
q1n2 = I('q1n2', 'Hydrogen: $\\ $up', size=26, col=1)
q1n3 = I('q1n3', 'A shape counts at its centre', size=26, col=1)
q1_pre, q1c = QPRE('ch-q01', 'q1c', [
    ('v', plus(S1, V1(60, '60%'))),
    ('m', plus(S1, V1(60, '60%'), R1(62, 42), R1(66, 48), R1(71, 57))),
    ('n', plus(S1, V1(60, '60%'), R1(62, 42), R1(66, 48), R1(71, 57), R1(64, 8), R1(68, 7), R1(74, 3))),
    ('o', plus(S1, V1(60, '60%'), R1(62, 42), R1(66, 48), R1(71, 57), R1(64, 8), R1(68, 7), R1(74, 3),
               _ln(c1x(59) - 13, c1y(12) - 13, c1x(59) + 13, c1y(12) + 13, 5), _ln(c1x(59) - 13, c1y(12) + 13, c1x(59) + 13, c1y(12) - 13, 5)))])
q1a = IH('q1a', 'Mercury: $\\ 3$', size=26, col=1)
q1b = IH('q1b', 'Neptune: $\\ 3$', size=26, col=1)
q1d = IH('q1d', 'the $59\\%$ ring: $\\ $out', size=26, col=1)
q1e = IH('q1e', '$3+3=6$', size=26, col=1)
q1w_pre, q1w = QPRE('ch-q01', 'q1w', [('h', plus(S1, H1(60, '60%'))), ('r', plus(S1, H1(60, '60%'), R1(19, 64)))])
q1f = I('q1f', 'The wrong axis: $\\ $only $1$', size=26, col=1)
q1g = I('q1g', 'Not a choice? $\\ $Stop and check', size=26, col=1)

video('solve-ch-q01', 'solution', qid='ch-q01', slides=[
    S('Read the chart',
      L("Here's our first chart set. Before the questions, let's read the page."),
      L("The graph shows the percent of carbon and the percent of hydrogen in soil samples from five planets. Each shape "
        "is one sample, and the key tells us its planet."),
      L("Carbon is on the bottom axis, going across. Hydrogen is on the side axis, going up.", show(q1n1, 'Carbon is on the bottom'),
        show(q1n2, 'Hydrogen is on the side')),
      L("And there's a note. The exact place of each shape is its centre. Let's remember it, because we'll need it soon.",
        show(q1n3, 'its centre')),
      L("There's no example on this page. So let's check ourselves with one shape. The ring at the bottom right is a "
        "Neptune sample.", show(q1r['k'], 'The ring at the bottom right')),
      L("We go down from it to the carbon axis, a bit under seventy-five. And across to the hydrogen axis, about three. So "
        "about seventy-four percent carbon, and three percent hydrogen."), pre=q1r_pre),
    S('A line at 60%',
      L("Now the first question. In how many of the samples is the percent of carbon greater than sixty percent?",
        pt('stem', 'In how many of the samples'), voice='calm', pause=0.5),
      L("So they ask for a count. And it's about carbon, the bottom axis.", pt('stem', 'So they ask for a count')),
      L("Like in the lesson, to count what's more than a value, we draw a line at that value. Carbon goes across, so this "
        "time the line stands up, at sixty percent.", show(q1c['v'], 'the line stands up')),
      L("Now we count only the shapes to the right of the line. First the Mercury dots. One, two, three.",
        show(q1c['m'], 'First the Mercury dots'), show(q1a, 'One, two, three')),
      L("Then the Neptune rings. Four, five, six.", show(q1c['n'], 'Then the Neptune rings'), show(q1b, 'Four, five, six')),
      L("What about the ring that touches the line? Its edge reaches the line. But the note says a shape is at its centre. "
        "And its centre is at fifty-nine percent, left of the line. So it doesn't count.", show(q1c['o'], 'its centre is at fifty-nine'),
        show(q1d, "it doesn't count")),
      L("If we counted it, we'd get seven. That's choice number one, the trap.", mk('cross', 'choice 1', "That's choice number one")),
      L("So three Mercury samples and three Neptune samples. Three plus three is six. That's choice number two.",
        show(q1e, 'Three plus three')), pre=q1_pre),
    S('The wrong axis',
      L("One more thing that happens under pressure. Instead of sixty percent carbon, we check sixty percent hydrogen.",
        show(q1w['h'], 'we check sixty percent hydrogen')),
      L("Above sixty percent hydrogen there's only one sample. And one is not among the choices.",
        show(q1w['r'], "there's only one sample"), show(q1f, 'only one')),
      L("So if our answer isn't one of the choices, we don't panic. We stop, and we check the key, the axis, and exactly "
        "what they asked.", show(q1g, "we don't panic")),
      L("Choice number two is our answer, and I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer')),
      pre=q1w_pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q02
q2_pre, q2c = QPRE('ch-q02', 'q2c', [
    ('r', plus(S1, _box(c1x(60), MB.C1_YT + 4, MB.C1_X1 - c1x(60) - 4, MB.C1_YB - MB.C1_YT - 8, AM, 3, '#FDEBC8', .35))),
    ('b', plus(S1, _box(c1x(60), MB.C1_YT + 4, MB.C1_X1 - c1x(60) - 4, MB.C1_YB - MB.C1_YT - 8, AM, 3, '#FDEBC8', .35),
               _box(MB.C1_X0 + 4, c1y(15), MB.C1_X1 - MB.C1_X0 - 8, MB.C1_YB - c1y(15) - 4, AM, 3, '#FDEBC8', .35))),
    ('k', plus(S1, _box(c1x(60), MB.C1_YT + 4, MB.C1_X1 - c1x(60) - 4, MB.C1_YB - MB.C1_YT - 8, AM, 3, '#FDEBC8', .35),
               _box(MB.C1_X0 + 4, c1y(15), MB.C1_X1 - MB.C1_X0 - 8, MB.C1_YB - c1y(15) - 4, AM, 3, '#FDEBC8', .35), R1(74, 3, 20))),
    ('m', plus(S1, _box(c1x(60), MB.C1_YT + 4, MB.C1_X1 - c1x(60) - 4, MB.C1_YB - MB.C1_YT - 8, AM, 3, '#FDEBC8', .35),
               _box(MB.C1_X0 + 4, c1y(15), MB.C1_X1 - MB.C1_X0 - 8, MB.C1_YB - c1y(15) - 4, AM, 3, '#FDEBC8', .35), R1(74, 3, 20),
               R1(71, 57)))])
q2a = I('q2a', 'More carbon: $\\ $the right side', size=26, col=1)
q2b = I('q2b', 'Less hydrogen: $\\ $the bottom', size=26, col=1)
q2d = I('q2d', 'The bottom right corner: $\\ $Neptune', size=26, col=1)
q2e = I('q2e', 'Mercury: $\\ $right, but high up', size=26, col=1)

video('solve-ch-q02', 'solution', qid='ch-q02', slides=[
    S('The corner',
      L("It is known that a region suits people better the higher the percent of carbon in its soil, and the lower the "
        "percent of hydrogen. On which planet is the region that suits people best?", pt('stem', 'It is known that'),
        voice='calm', pause=0.5),
      L("So the question gives us a rule. More carbon is better, and less hydrogen is better. We want the sample with "
        "both.", pt('stem', 'So the question gives us a rule')),
      L("Do we check the exact numbers of every sample? No. We solve it by understanding, with our eyes."),
      L("More carbon means further to the right, because carbon goes across.", show(q2c['r'], 'further to the right'),
        show(q2a, 'further to the right')),
      L("Less hydrogen means lower down, because hydrogen goes up.", show(q2c['b'], 'lower down'), show(q2b, 'lower down')),
      L("So we want a sample that is both on the right and at the bottom. That's the bottom right corner."),
      L("Who's in the corner? The ring at about seventy-four percent carbon and three percent hydrogen. It has more carbon "
        "than every other sample, and less hydrogen than all of them.", show(q2c['k'], "Who's in the corner"),
        show(q2d, 'It has more carbon')),
      L("The key says a ring is Neptune."),
      L("What about Mercury? It has samples far to the right too. But look how high they are. They have a lot of "
        "hydrogen, so they don't suit people.", show(q2c['m'], 'look how high they are'), show(q2e, 'look how high')),
      L("Choice number two is our answer, and I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer')),
      pre=q2_pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q03
q3_pre, q3c = QPRE('ch-q03', 'q3c', [
    ('ve', plus(S1, SPAN1('Venus'))), ('sa', plus(S1, SPAN1('Venus'), SPAN1('Saturn'))),
    ('ma', plus(S1, SPAN1('Venus'), SPAN1('Saturn'), SPAN1('Mars', 6))),
    ('ne', plus(S1, SPAN1('Venus'), SPAN1('Saturn'), SPAN1('Mars', 6), SPAN1('Neptune')))])
q3a = I('q3a', 'Range: $\\ $the leftmost to the rightmost sample', size=26, col=1)
q3b = I('q3b', 'Venus: $\\ $a short line', size=26, col=1)
q3d = I('q3d', 'Saturn: $\\ $a long line', size=26, col=1)
q3e = I('q3e', 'Mars, Neptune: $\\ $shorter than Saturn', size=26, col=1)

video('solve-ch-q03', 'solution', qid='ch-q03', slides=[
    S('Compare the lengths',
      L("The largest range of carbon percents is found in the samples from which planet?", pt('stem', 'The largest range'),
        voice='calm', pause=0.5),
      L("What's a range? It's everything from the smallest value to the biggest one. Here it's carbon, so we look across.",
        show(q3a, "What's a range")),
      L("So for each planet, we take its leftmost sample and its rightmost sample. The range is the distance between them."),
      L("Do we read each number and subtract? No. We draw a line from the leftmost to the rightmost sample, and we compare "
        "the lengths by eye."),
      L("Venus, the squares. From about ten to about thirty. A short line.", show(q3c['ve'], 'Venus, the squares'), show(q3b, 'A short line')),
      L("Saturn, the triangles. From about eight all the way to fifty-five. Much longer than Venus. So Venus is out.",
        show(q3c['sa'], 'Saturn, the triangles'), show(q3d, 'Much longer'), mk('cross', 'choice 3', 'So Venus is out')),
      L("Mars, the diamonds. From twenty to fifty. Shorter than Saturn's line. Out.", show(q3c['ma'], 'Mars, the diamonds'),
        mk('cross', 'choice 2', "Shorter than Saturn's line")),
      L("Neptune, the rings. From forty to seventy-four. Also shorter than Saturn's line. Out.", show(q3c['ne'], 'Neptune, the rings'),
        show(q3e, 'Also shorter'), mk('cross', 'choice 4', "Also shorter than Saturn's line")),
      L("So Saturn has the largest range. We didn't calculate anything. We just compared lengths. That's one of the main "
        "ways we solve chart questions."),
      L("Choice number one is our answer, and I'll see you in the next question.", mk('tick', 'choice 1', 'Choice number one is our answer')),
      pre=q3_pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q04
q4_pre, q4c = QPRE('ch-q04', 'q4c', [('me', plus(S1, TREND1('Mercury')))])
q4a = I('q4a', 'Every choice: $\\ $one planet, $\\ $more carbon, more or less hydrogen', size=24, col=1)
q4b = I('q4b', 'Mercury: $\\ $the dots form a line going up', size=24, col=1)
q4d_pre, q4d = QPRE('ch-q04', 'q4d', [
    ('ve', plus(S1, SEG1((10, 44), (13, 57)), SEG1((13, 57), (16, 36)))),
    ('ne', plus(S1, SEG1((10, 44), (13, 57)), SEG1((13, 57), (16, 36)), SEG1((46, 12), (52, 16)))),
    ('sa', plus(S1, SEG1((10, 44), (13, 57)), SEG1((13, 57), (16, 36)), SEG1((46, 12), (52, 16)), SEG1((8, 26), (17, 33)))),
    ('me', plus(S1, SEG1((10, 44), (13, 57)), SEG1((13, 57), (16, 36)), SEG1((46, 12), (52, 16)), SEG1((8, 26), (17, 33)), TREND1('Mercury')))])
q4e = I('q4e', 'Venus: $\\ $up, then down', size=24, col=1)
q4f = IH('q4f', 'Neptune: $\\ 12\\%$ up to $16\\%$', size=26, col=1)
q4g = I('q4g', 'Necessarily: $\\ $one exception is enough', size=24, col=1)
q4h = I('q4h', 'Saturn: $\\ $less carbon, but less hydrogen too', size=24, col=1)
q4i = I('q4i', 'Mercury: $\\ $every step right is a step up', size=24, col=1)

video('solve-ch-q04', 'solution', qid='ch-q04', slides=[
    S('Method 1 · Insight: look at all four',
      L("Which of the following statements is necessarily true?", pt('stem', 'Which of the following'), voice='calm', pause=0.5),
      L("Necessarily true means true with no exception. Every sample has to follow it.", pt('stem', 'Necessarily true means')),
      L("Usually we'd read the first choice and go to the chart. But first, let's read all four choices together. We'll "
        "solve it in two different ways. First with an insight, and then by checking each planet."),
      L("Choice number one says, on Venus, the higher the carbon, the higher the hydrogen. Choice number two says, on "
        "Neptune, the higher the carbon, the lower the hydrogen.", pt('choice 1', 'Choice number one says'), pt('choice 2', 'Choice number two says')),
      L("Choice number three says the same as choice number one, on Mercury. And choice number four says, on Saturn, the "
        "lower the carbon, the higher the hydrogen.", pt('choice 3', 'Choice number three says'), pt('choice 4', 'And choice number four')),
      L("So it's the same idea every time. One planet, and a steady link between carbon and hydrogen.", show(q4a, 'the same idea every time')),
      L("For more carbon and more hydrogen, every move right must also go up. For more carbon and less hydrogen, it must "
        "go down. The points don't have to form a straight line. Let's look at the whole chart."),
      L("One planet jumps out. The Mercury dots form a straight line going up. More carbon, and more hydrogen too.",
        show(q4c['me'], 'One planet jumps out'), show(q4b, 'form a straight line')),
      L("So choice number three looks right. But a quick look is not enough to prove necessarily true. Now let's check "
        "it properly."), pre=q4_pre),
    S('Method 2 · Understanding: each planet',
      L("Now we check each planet, from the givens. Choice number one, Venus, the squares. Is it true that more carbon "
        "means more hydrogen?", pt('choice 1', 'Choice number one, Venus')),
      L("From ten to thirteen percent carbon, the hydrogen goes up. But from thirteen to sixteen, it goes down. So it's "
        "not steady. Out.", show(q4d['ve'], 'From ten to thirteen'), show(q4e, 'it goes down'), mk('cross', 'choice 1', 'So it\'s not steady')),
      L("Choice number two, Neptune, the rings. More carbon, less hydrogen? Almost all the way, yes. But careful.",
        pt('choice 2', 'Choice number two, Neptune')),
      L("From forty-six to fifty-two percent carbon, the hydrogen goes up, from twelve to sixteen percent.",
        show(q4d['ne'], 'From forty-six to fifty-two'), show(q4f, 'the hydrogen goes up')),
      L("Necessarily means no exception. One exception is enough, so it's out.", show(q4g, 'One exception is enough'),
        mk('cross', 'choice 2', "so it's out")),
      L("Choice number four, Saturn, the triangles. Less carbon, more hydrogen? From seventeen down to eight percent "
        "carbon, the hydrogen goes down too, from thirty-three to twenty-six. Out.", pt('choice 4', 'Choice number four, Saturn'),
        show(q4d['sa'], 'From seventeen down to eight'), show(q4h, 'the hydrogen goes down too'), mk('cross', 'choice 4', 'twenty-six. Out')),
      L("And Mercury, choice number three. Every step to the right is also a step up. No exception.",
        show(q4d['me'], 'Every step to the right'), show(q4i, 'Every step to the right')),
      L("Choice number three is our answer, and I'll see you in the next question.", mk('tick', 'choice 3', 'Choice number three is our answer')),
      pre=q4d_pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q05
_o5 = MB.L5both(None)
_y5 = round(_o5['y'], 1)
q5h = MB.chart1_options_svg()
def _q5pre(tag, slayers, glayers):
    pre = []
    for _k, _it in enumerate(_o5['pre']):
        _d = dict(_it); _d.update(_name='%s_p%d' % (tag, _k), _col=0, _hand=None)
        if _d['k'] == 't': _d['_stem'] = True
        if _d['k'] == 'vis': continue
        pre.append(_d)
    sc = CH(tag + 's', S1, 410, _y5, 560, slayers)
    gr = CH(tag + 'g', q5h, 1000, _y5, 540, glayers); gr['base'].pop('_chart')
    return pre + [sc['base'], gr['base']], sc, gr


q5_pre, q5s0, q5g = _q5pre('q5', [], [('a', MB.chart1_options_svg(0))])
q52_pre, q5s, q5g2 = _q5pre('q52', [('l', plus(S1, H1(10, '10%'))),
                                    ('r', plus(S1, H1(10, '10%'), R1(36, 6), R1(64, 8), R1(68, 7), R1(74, 3))),
                                    ('t', plus(S1, H1(10, '10%'), R1(36, 6), R1(64, 8), R1(68, 7), R1(74, 3), H1(60, '60%'), R1(19, 64)))],
                            [('b', MB.chart1_options_svg(6))])
q5a = I('q5a', 'Hydrogen: $\\ $the side axis of the big chart', size=26)
q5b = I('q5b', 'Check only where the graphs differ: $\\ $the edges first', size=26)
q5d = I('q5d', 'Below $10\\%$: $\\ 4$ samples. $\\ $Graphs $(1)$ and $(3)$ out.', size=26)
q5e = I('q5e', '$60\\%$ to $70\\%$: $\\ 1$ sample. $\\ $Graph $(4)$ out.', size=26)
q5f = I('q5f', 'Graph $(1)$: $\\ $carbon instead of hydrogen', size=26)

video('solve-ch-q05', 'solution', qid='ch-q05', slides=[
    S('Where they differ',
      L("Which of the following graphs describes the number of samples collected on all five planets together, in each "
        "range of hydrogen percents?", pt('stem', 'Which of the following graphs'), voice='calm', pause=0.5),
      L("So the choices are small graphs. Each one counts the samples in ranges of ten percent of hydrogen. Only one of "
        "them is right.", pt('q5g', 'So the choices are small graphs')),
      L("First, let's circle the word hydrogen. Then we remember to count up the side axis, and not across.",
        show(q5a, 'circle the word hydrogen')),
      L("Do we check graph one bar by bar, and then graph two? No, that takes too long. We only check where the graphs are "
        "different. And the easiest places are the edges.", show(q5b, 'where the graphs are different')),
      L("The left edge is below ten percent. There, the four graphs show one, four, five and four.", show(q5g['a'], 'The left edge')),
      L("So whatever the real count is, it rules out at least two graphs."), pre=q5_pre),
    S('The two edges',
      L("Let's count. We draw a line at ten percent hydrogen, and count the shapes under it.", show(q5s['l'], 'We draw a line at ten')),
      L("One, the Mercury dot at six percent. Two, three, four, the Neptune rings. Remember, each one counts at its centre. "
        "So four samples.", show(q5s['r'], 'the Mercury dot at six')),
      L("Graph one shows one, and graph three shows five. Both are out. We're left with graphs two and four.",
        show(q5d, 'Both are out'), mk('cross', 'choice 1', 'Graph one shows one'), mk('cross', 'choice 3', 'graph three shows five')),
      L("To tell two and four apart, we could check the middle. But between thirty and forty we'd need two lines and a "
        "careful count. The other edge is easier."),
      L("The right edge is sixty to seventy percent. Graph two says one sample, and graph four says three.",
        show(q5g2['b'], 'The right edge')),
      L("We draw a line at sixty percent. Above it there's just one square, the Venus sample at sixty-four. So graph four "
        "is out.", show(q5s['t'], 'Above it there'), show(q5e, 'just one square'), mk('cross', 'choice 4', 'graph four is out')),
      L("And graph one? It's what we get if we count carbon instead of hydrogen. That's why we circled the word.",
        show(q5f, 'count carbon instead')),
      L("So when the choices are small graphs, we don't check each one to the end. We find where they differ, and we start "
        "at the edges."),
      L("Choice number two is our answer, and I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer')),
      pre=q52_pre),
])


# =================================================================================================================
# Chart set 2 (car races, two tables): solve-ch-q06 .. q10. No Hebrew solution videos for this set (seg11: "and then
# the other charts the same way"); the course book's questions, the course's numbers (modulesV52b.py). The habits of
# set 1 carry over (read the page, the example, the key word). REMINDERS: the average (topic 25: the sum, and the
# balance - differences add up to zero), counting years 2017-2022 (last - first + 1, topic 15), percents (23).
# NEW: translate money into a place (q06); a change "of three or more" counted row by row (q07); skip the zeros (q09);
# the same total -> the same average (q10, an insight; the math way first).
# =================================================================================================================
q6r_pre, q6r = RPRE(2, MB._intro(MB.C2_INTRO, 1, 3), 'q6r', [('e', plus(S2, CELL2('Night Owls', 2019), PRIZE2(2)))])
q6n1 = I('q6n1', 'Left: $\\ $the place of each team, each year', size=24, col=1)
q6n2 = I('q6n2', 'Right: $\\ $the prize for each place', size=24, col=1)
q6n3 = I('q6n3', 'Night Owls, $2019$: $\\ 2$nd, $\\ 80{,}000$', size=24, col=1)
q6n4 = I('q6n4', 'Places $6$ and $7$: $\\ 0$', size=24, col=1)
q6_pre, q6c = QPRE('ch-q06', 'q6c', [('p', plus(S2, PRIZE2(1))),
    ('f', plus(S2, PRIZE2(1), CELL2('Desert Foxes', 2017), CELL2('Red Arrows', 2018), CELL2('Silver Wolves', 2019),
               CELL2('Road Runners', 2020), CELL2('Desert Foxes', 2021), CELL2('Blue Comets', 2022)))])
q6a = I('q6a', '$120{,}000$: $\\ $first place', size=24, col=1)
q6b = I('q6b', 'Find the $1$s, $\\ $one in each year', size=24, col=1)
q6d = I('q6d', 'Desert Foxes: $\\ 2017$ and $2021$', size=24, col=1)

video('solve-ch-q06', 'solution', qid='ch-q06', slides=[
    S('Read the tables',
      L("Here's our second chart set. Two tables of car races. Let's read the page first."),
      L("The races were held from two thousand seventeen to two thousand twenty-two, with seven teams. The left table shows the place "
        "each team reached in each year's race.", show(q6n1, 'The left table shows')),
      L("The right table shows the prize, in shekels, for each place.", show(q6n2, 'The right table shows')),
      L("Now the example. In two thousand nineteen, Night Owls came second, and won eighty thousand shekels. Let's check it."),
      L("The Night Owls row, the two thousand nineteen column. It says two. And in the prize table, second place gets eighty "
        "thousand. It matches.", show(q6r['e'], 'It says two'), show(q6n3, 'It matches')),
      L("Notice one more thing. Places six and seven win nothing. Their prize is zero.", show(q6n4, 'Places six and seven')),
      pre=q6r_pre),
    S('Find the 1s',
      L("Which team won a hundred twenty thousand shekels twice, in the years two thousand seventeen to two thousand twenty-two?",
        pt('stem', 'Which team won'), voice='calm', pause=0.5),
      L("First, we turn the money into a place. In the prize table, a hundred twenty thousand is first place. So we look "
        "for the ones.", show(q6c['p'], 'a hundred twenty thousand is first place'), show(q6a, 'is first place')),
      L("Each year has exactly one team in first place. So each column has exactly one one. Let's go year by year.",
        show(q6b, 'exactly one one')),
      L("Two thousand seventeen, Desert Foxes. Two thousand eighteen, Red Arrows. Two thousand nineteen, Silver Wolves.",
        show(q6c['f'], 'Two thousand seventeen, Desert Foxes')),
      L("Two thousand twenty, Road Runners. Two thousand twenty-one, Desert Foxes again. And two thousand twenty-two, Blue Comets."),
      L("Only Desert Foxes came first twice.", show(q6d, 'Only Desert Foxes')),
      L("Choice number two is our answer, and I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer')),
      pre=q6_pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q07
q7_pre, q7c = QPRE('ch-q07', 'q7c', [('no', plus(S2, ROW2('Night Owls'), ROW2('Iron Eagles')))])
q7a = I('q7a', 'Three or more: $\\ $exactly $3$ counts too', size=24, col=1)
q7b = I('q7b', 'Night Owls, Iron Eagles: $\\ $no change of $3$', size=24, col=1)
q7_2pre, q7d = QPRE('ch-q07', 'q7d', [('rr', plus(S2, ROW2('Road Runners'))), ('df', plus(S2, ROW2('Road Runners'), ROW2('Desert Foxes'))),
    ('bc', plus(S2, ROW2('Road Runners'), ROW2('Desert Foxes'), ROW2('Blue Comets'), ROW2('Red Arrows'))),
    ('sw', plus(S2, ROW2('Road Runners'), ROW2('Desert Foxes'), ROW2('Blue Comets'), ROW2('Red Arrows'), ROW2('Silver Wolves')))])
q7e = IH('q7e', 'Road Runners: $\\ 2$', size=26, col=1)
q7f = IH('q7f', 'Desert Foxes: $\\ 3$', size=26, col=1)
q7g = IH('q7g', 'Blue Comets $1$, $\\ $Red Arrows $1$', size=26, col=1)
q7h = IH('q7h', 'Silver Wolves: $\\ 2$', size=26, col=1)
q7i = IH('q7i', '$2+3+1+1+2=9$', size=26, col=1)

video('solve-ch-q07', 'solution', qid='ch-q07', slides=[
    S('A dramatic change',
      L("A dramatic change is a change of three places or more in a team's place, between two races in a row. How many "
        "dramatic changes were there, in the years two thousand seventeen to two thousand twenty-two?", pt('stem', 'A dramatic change is'),
        voice='calm', pause=0.5),
      L("So the question gives us a new word, and asks us to count. This question doesn't need a trick. It needs a "
        "careful count, in order.", pt('stem', 'So the question gives us')),
      L("Let's circle three or more. A change of exactly three counts too.", show(q7a, 'A change of exactly three')),
      L("We go row by row. For each team, we compare each year with the next year."),
      L("Some rows are quick. Night Owls are two, three, two, three, two, four. The biggest change is two. Iron Eagles are "
        "seven, five, six, seven, five, seven. Again at most two. So no dramatic changes there.",
        show(q7c['no'], 'Some rows are quick'), show(q7b, 'So no dramatic changes')), pre=q7_pre),
    S('Count',
      L("Now Road Runners. Four to two is a change of two, no. Two to five is three, yes. Five to one is four, yes. Then "
        "one to three, and three to three, no. So two.", show(q7d['rr'], 'Now Road Runners'), show(q7e, 'So two')),
      L("Desert Foxes. One to six is five, yes. Six to three is three, yes. Three to four, no. Four to one is three, yes. "
        "One to two, no. So three.", show(q7d['df'], 'Desert Foxes'), show(q7f, 'So three')),
      L("Blue Comets are six, seven, seven, five, four, one. Only four to one is three. So one. Red Arrows have only one "
        "to four. So one.",
        show(q7d['bc'], 'Blue Comets'), show(q7g, 'Red Arrows have only one')),
      L("Silver Wolves. Four to one is three, yes. Two to six is four, yes. So two.", show(q7d['sw'], 'Silver Wolves'),
        show(q7h, 'So two')),
      L("Now we add them up. Two plus three is five. Five plus one is six, and six plus one is seven. Seven plus two is "
        "nine.", show(q7i, 'Now we add them up')),
      L("Careful, if we count only changes of more than three, we get three, choice number three. But three or more "
        "includes exactly three.", mk('cross', 'choice 3', 'choice number three')),
      L("Choice number one is our answer, and I'll see you in the next question.", mk('tick', 'choice 1', 'Choice number one is our answer')),
      pre=q7_2pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q08
q8_pre, q8c = QPRE('ch-q08', 'q8c', [('r', plus(S2, ROW2('Night Owls'))), ('p', plus(S2, ROW2('Night Owls'), PRIZES2(2, 4)))])
q8a = IH('q8a', 'places: $\\ 2, 3, 2, 3, 2, 4$', size=26, col=1)
q8b = IH('q8b', '$3\\cdot80{,}000=240{,}000$', size=26, col=1)
q8d = IH('q8d', '$2\\cdot50{,}000=100{,}000$', size=26, col=1)
q8e = IH('q8e', '$1\\cdot20{,}000=20{,}000$', size=26, col=1)
q8f = IH('q8f', 'sum: $\\ 360{,}000$', size=26, col=1)
q8g = IH('q8g', '$2022-2017+1=6$ years', size=26, col=1)
q8h = IH('q8h', '$360{,}000\\div6=60{,}000$', size=26, col=1)
q8_2pre, q8k = QPRE('ch-q08', 'q8k', [('r', plus(S2, ROW2('Night Owls')))])
q8i = IH('q8i', 'vs. $60{,}000$: $\\ +20,\\ -10,\\ +20$', size=26, col=1)
q8j = IH('q8j', '$-10,\\ +20,\\ -40$', size=26, col=1)
q8l = IH('q8l', '$+60-60=0$', size=26, col=1)

video('solve-ch-q08', 'solution', qid='ch-q08', slides=[
    S('Method 1 · The math way',
      L("What is the average amount, in shekels, that Night Owls won per year, in the years two thousand seventeen to two thousand "
        "twenty-two?", pt('stem', 'What is the average amount'), voice='calm', pause=0.5),
      L("So we need the average prize of one team. First we turn its places into prizes. We'll solve it in two different "
        "ways, the math way, and then by plugging in the answers.", pt('stem', 'So we need the average prize')),
      L("Let's start with the math way. The Night Owls row says two, three, two, three, two, four.",
        show(q8c['r'], 'The Night Owls row'), show(q8a, 'two, three, two')),
      L("Second place three times. Each one is eighty thousand. Three times eighty thousand is two hundred forty thousand.",
        show(q8c['p'], 'Second place three times'), show(q8b, 'Three times eighty thousand')),
      L("Third place twice. Two times fifty thousand is a hundred thousand.", show(q8d, 'Two times fifty thousand')),
      L("Fourth place once, twenty thousand.", show(q8e, 'Fourth place once')),
      L("Now the sum. Two hundred forty thousand plus a hundred thousand is three hundred forty thousand. Plus twenty "
        "thousand is three hundred sixty thousand.", show(q8f, 'Plus twenty thousand is three')),
      L("And how many years? From two thousand seventeen to two thousand twenty-two. Twenty-two minus seventeen is five, plus one, "
        "because we count both ends. Six years.", show(q8g, 'Six years')),
      L("The average is the sum divided by six. Three hundred sixty thousand divided by six is sixty thousand.",
        show(q8h, 'divided by six is sixty')),
      L("Careful, if we divide by five instead of six, we get seventy-two thousand. That's choice number four, the trap.",
        mk('cross', 'choice 4', "That's choice number four")),
      L("So the average is sixty thousand, choice number three."), pre=q8_pre),
    S('Method 2 · Plugging in the answers',
      L("[pause] Now let's plug in the answers, with the balance from averages. We start again from the Night Owls row.",
        show(q8k['r'], 'from the Night Owls row')),
      L("Remember, the differences from the average add up to zero. Let's try choice number three, sixty thousand. It's "
        "a round number in the middle of the choices.", pt('choice 3', "Let's try choice number three")),
      L("Each prize, compared with sixty thousand. Eighty gives plus twenty. Fifty gives minus ten. Eighty gives plus twenty again.",
        show(q8i, 'Eighty gives plus twenty')),
      L("Then fifty gives minus ten, eighty gives plus twenty, and twenty gives minus forty.", show(q8j, 'twenty gives minus forty')),
      L("The plus side is twenty, twenty and twenty, sixty. The minus side is ten, ten and forty, also sixty. Sixty minus "
        "sixty is zero. So sixty thousand is the average.", show(q8l, 'Sixty minus sixty is zero')),
      L("Choice number three is our answer, and I'll see you in the next question.", mk('tick', 'choice 3', 'Choice number three is our answer')),
      pre=q8_2pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q09
q9_pre, q9c = QPRE('ch-q09', 'q9c', [('z', plus(S2, PRIZES2(6, 7))), ('b', plus(S2, PRIZES2(6, 7), ROW2('Blue Comets'))),
                                     ('i', plus(S2, PRIZES2(6, 7), ROW2('Blue Comets'), ROW2('Iron Eagles')))])
q9a = I('q9a', 'Places $6$ and $7$: $\\ 0$, $\\ $skip them', size=24, col=1)
q9b = IH('q9b', '$10{,}000+20{,}000=30{,}000$', size=24, col=1)
q9d = IH('q9d', '$30{,}000+120{,}000=150{,}000$', size=24, col=1)
q9e = IH('q9e', '$2\\cdot10{,}000=20{,}000$', size=24, col=1)
q9f = IH('q9f', '$150{,}000-20{,}000=130{,}000$', size=24, col=1)
q9g = I('q9g', 'Blue Comets earned more', size=24, col=1)

video('solve-ch-q09', 'solution', qid='ch-q09', slides=[
    S('Skip the zeros',
      L("Over the races in the years two thousand seventeen to two thousand twenty-two, the team Blue Comets earned blank shekels, "
        "blank than the team Iron Eagles.", pt('stem', 'Over the races'), voice='calm', pause=0.5),
      L("So there are two blanks. A number of shekels, and the direction, more or less. Both must be right.",
        pt('stem', 'So there are two blanks')),
      L("Here's a shortcut. Places six and seven win nothing. So in each row we skip the sixes and the sevens.",
        show(q9c['z'], 'Places six and seven win nothing'), show(q9a, 'we skip the sixes')),
      L("Blue Comets are six, seven, seven, five, four, one. The six and the two sevens give nothing.", show(q9c['b'], 'Blue Comets are six')),
      L("Fifth place is ten thousand, and fourth place is twenty thousand. Ten thousand plus twenty thousand is thirty "
        "thousand.", show(q9b, 'Ten thousand plus twenty thousand')),
      L("First place is a hundred twenty thousand. Thirty thousand plus a hundred twenty thousand is a hundred fifty "
        "thousand.", show(q9d, 'Thirty thousand plus a hundred twenty')),
      L("Iron Eagles are seven, five, six, seven, five, seven. Only the two fifth places count. Two times ten thousand is "
        "twenty thousand.", show(q9c['i'], 'Iron Eagles are seven'), show(q9e, 'Two times ten thousand')),
      L("The difference is a hundred fifty thousand minus twenty thousand, a hundred thirty thousand.", show(q9f, 'The difference is')),
      L("And Blue Comets earned more, because a hundred fifty thousand is more than twenty thousand. So a hundred thirty "
        "thousand, more.", show(q9g, 'Blue Comets earned more')),
      L("Careful, a hundred fifty thousand is Blue Comets' total. It's the trap if we forget to subtract.",
        mk('cross', 'choice 4', "the trap if we forget")),
      L("Choice number three is our answer, and I'll see you in the next question.", mk('tick', 'choice 3', 'Choice number three is our answer')),
      pre=q9_pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q10
q10_pre, q10c = QPRE('ch-q10', 'q10c', [('p', plus(S2, PRIZES2(1, 7)))])
q10a = IH('q10a', '$2017$: $\\ 120+80=200$', size=24, col=1)
q10b = IH('q10b', '$200+50+20+10=280$', size=24, col=1)
q10d = IH('q10d', '$280\\div7=40$', size=24, col=1)
q10e = IH('q10e', '$2016$: $\\ 200\\div2=100$ each', size=24, col=1)
q10f = IH('q10f', '$100+100+80=280$', size=24, col=1)
q10g = I('q10g', 'Thousands. $\\ $The same $280$, $\\ $the same $7$ teams.', size=22, col=1)
q10_2pre, q10k = QPRE('ch-q10', 'q10k')
q10h = I('q10h', 'The same total money', size=24, col=1)
q10i = I('q10i', 'The same seven teams', size=24, col=1)
q10j = I('q10j', 'So the same average', size=24, col=1)

video('solve-ch-q10', 'solution', qid='ch-q10', slides=[
    S('Method 1 · The math way',
      L("In two thousand sixteen, all seven teams raced. Night Owls and Red Arrows came first together. The prizes for first and "
        "second place were added, and split equally between them. The prizes for places three to seven didn't change.",
        pt('stem', 'In two thousand sixteen'), voice='calm', pause=0.5),
      L("The average prize per team in two thousand sixteen was blank the average prize per team in two thousand seventeen.",
        pt('stem', 'The average prize per team'), voice='calm'),
      L("So we compare two averages. This is the last question of the set, so let's look for the idea. But first, let's "
        "solve it the math way. Then we'll see the insight."),
      L("Let's start with the math way, in thousands. In two thousand seventeen, the prizes are the prize table. A hundred "
        "twenty plus eighty is two hundred.", show(q10c['p'], 'the prizes are the prize table'), show(q10a, 'A hundred twenty plus eighty')),
      L("Plus fifty, twenty and ten is two hundred eighty. Places six and seven add zero.", show(q10b, 'Plus fifty, twenty and ten')),
      L("Seven teams, so the average is two hundred eighty divided by seven. That's forty thousand.", show(q10d, 'divided by seven')),
      L("Now two thousand sixteen. The two winners share a hundred twenty plus eighty, two hundred. Two hundred divided by two "
        "is a hundred each.", show(q10e, 'Two hundred divided by two')),
      L("The other five teams get places three to seven, the same prizes as before. Fifty, twenty, ten, zero and zero, "
        "that's eighty."),
      L("So the total is a hundred plus a hundred, two hundred. Plus eighty is two hundred eighty again. Divided by the same "
        "seven teams, forty thousand.", show(q10f, 'So the total is'), show(q10g, 'Divided by the same')),
      L("The two averages are equal. That's choice number one."), pre=q10_pre),
    S('Method 2 · Insight: the same total',
      L("[pause] Now the insight, from the givens again. What did two thousand sixteen change? Only how the money was split.",
        pt('stem', 'What did two thousand sixteen change')),
      L("The two winners got the first and second prizes together, the same money as always. Places three to seven didn't "
        "change. So the total money is the same.", show(q10h, 'the total money is the same')),
      L("And the same seven teams share it.", show(q10i, 'the same seven teams')),
      L("The average is the total divided by the number of teams. The same total, divided by the same seven, gives the "
        "same average. No calculation needed.", show(q10j, 'gives the same average')),
      L("So in the last questions of a set, look for the idea first. Here the whole question was one fact. Sharing money "
        "differently doesn't change the average."),
      L("Choice number one is our answer, and I'll see you in the next question.", mk('tick', 'choice 1', 'Choice number one is our answer')),
      pre=q10_2pre),
])


# =================================================================================================================
# Chart set 3 (weddings: bars + a pie above each bar): solve-ch-q11 .. q15. No Hebrew solution videos (as set 2); the
# course book's questions with the course's numbers. REMINDERS: overlap (topic 24: the shared guests belong to both
# sides), the whole of a percent and a percent of a number (topic 23), the weighted average (topic 25, the seesaw:
# the average sits nearer the heavier group). NEW: compare slices of the same pie without numbers (q11); "and not from"
# = only (q12); whole people (q13, an insight); both numbers matter (q14).
# =================================================================================================================
q11r_pre, q11r = RPRE(3, MB._intro(MB.C3_INTRO, 1, 2), 'q11r', [('b', plus(S3, BAR3('Sunday', '300'))),
                                                              ('p', plus(S3, BAR3('Sunday', '300'), SLICE3('Sunday', 0)))])
q11n1 = I('q11n1', 'A bar: $\\ $the number of guests', size=24, col=1)
q11n2 = I('q11n2', "A pie: $\\ $groom's side only, bride's side only, shared", size=24, col=1)
q11n3 = I('q11n3', "Sunday: $\\ 300$, $\\ 60\\%$ groom's side only", size=24, col=1)
q11_pre, q11c = QPRE('ch-q11', 'q11c', [('w', plus(S3, SLICE3('Monday', 0), SLICE3('Monday', 1), SLICE3('Tuesday', 0), SLICE3('Tuesday', 1),
                                                  SLICE3('Wednesday', 0), SLICE3('Wednesday', 1), SLICE3('Thursday', 0), SLICE3('Thursday', 1)))])
q11a = I('q11a', 'Shared guests: $\\ $on both sides', size=24, col=1)
q11b = I('q11b', "Compare groom's only with bride's only", size=24, col=1)
q11d = IH('q11d', 'Mon $50$, $25$. $\\ $Tue $25$, $50$', size=24, col=1)
q11e = IH('q11e', 'Wed $35$, $35$. $\\ $Thu $30$, $50$', size=24, col=1)

video('solve-ch-q11', 'solution', qid='ch-q11', slides=[
    S('Read the chart',
      L("Here's our third chart set, weddings in an event hall. Let's read the page first."),
      L("There's a wedding every day. Each bar shows the number of guests at that day's wedding.", show(q11n1, 'Each bar shows')),
      L("Above each bar there's a pie. It splits the guests into three groups. The groom's side only, the bride's side "
        "only, and guests shared by both.", show(q11n2, 'It splits the guests')),
      L("The example says, on Sunday there were three hundred guests, and sixty percent were from the groom's side only."),
      L("Let's check. The Sunday bar reaches three hundred.", show(q11r['b'], 'The Sunday bar reaches')),
      L("And in Sunday's pie, the slice for the groom's side only says sixty. It matches.", show(q11r['p'], 'says sixty'),
        show(q11n3, 'It matches')), pre=q11r_pre),
    S('A happy wedding',
      L("A happy wedding is a wedding with an equal number of guests from the groom's side and from the bride's side. On "
        "which day was there a happy wedding?", pt('stem', 'A happy wedding is'), voice='calm', pause=0.5),
      L("Careful with the shared guests. They belong to both sides. So they add the same number to the groom's side and "
        "to the bride's side.", show(q11a, 'They belong to both sides')),
      L("So we only need to compare the groom's side only with the bride's side only.", show(q11b, 'So we only need to compare')),
      L("And it's the same wedding, the same total. So we can compare the percents. We don't need the number of guests."),
      L("Monday, fifty and twenty-five. Tuesday, twenty-five and fifty.", show(q11c['w'], 'Monday, fifty'), show(q11d, 'Tuesday, twenty-five')),
      L("Wednesday, thirty-five and thirty-five. Thursday, thirty and fifty.", show(q11e, 'Wednesday, thirty-five')),
      L("Only Wednesday is equal. That's the happy wedding."),
      L("Careful with Tuesday. The groom's side only plus the shared is twenty-five plus twenty-five, fifty. That's equal to "
        "the bride's side only, fifty. But then we gave the shared guests to one side only.", mk('cross', 'choice 2', 'Careful with Tuesday')),
      L("Choice number three is our answer, and I'll see you in the next question.", mk('tick', 'choice 3', 'Choice number three is our answer')),
      pre=q11_pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q12
q12_pre, q12c = QPRE('ch-q12', 'q12c', [('b', plus(S3, BAR3('Tuesday', '500'))), ('s', plus(S3, BAR3('Tuesday', '500'), SLICE3('Tuesday', 1)))])
q12a = I('q12a', "The bride's side and not the groom's: $\\ $the bride's side only", size=24, col=1)
q12b = IH('q12b', '$50\\%$ of $500$', size=26, col=1)
q12d = IH('q12d', '$500\\div2=250$', size=26, col=1)

video('solve-ch-q12', 'solution', qid='ch-q12', slides=[
    S('One slice',
      L("How many of the guests at Tuesday's wedding were from the bride's side, and not from the groom's side?",
        pt('stem', "How many of the guests"), voice='calm', pause=0.5),
      L("What does and not from the groom's side mean? It means not the shared guests. So only the bride's side only.",
        show(q12a, "It means not the shared guests")),
      L("Tuesday's bar reaches five hundred. So five hundred guests.", show(q12c['b'], "Tuesday's bar reaches")),
      L("In Tuesday's pie, the bride's side only is fifty percent.", show(q12c['s'], "the bride's side only is fifty")),
      L("So it's fifty percent of five hundred. Fifty percent is a half, and half of five hundred is two hundred fifty.",
        show(q12b, "it's fifty percent of five hundred"), show(q12d, 'half of five hundred')),
      L("Careful, three hundred seventy-five adds the shared guests. That's seventy-five percent, and the question left "
        "them out.", mk('cross', 'choice 4', 'three hundred seventy-five')),
      L("Choice number three is our answer, and I'll see you in the next question.", mk('tick', 'choice 3', 'Choice number three is our answer')),
      pre=q12_pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q13
q13_pre, q13c = QPRE('ch-q13', 'q13c', [('t', plus(S3, BAR3('Thursday', '350')))])
q13a = I('q13a', '$1\\%$ of the guests: $\\ $a whole number of people', size=24, col=1)
q13b = IH('q13b', 'Sun $3$, $\\ $Mon $4$, $\\ $Tue $5$', size=26, col=1)
q13d = IH('q13d', 'Thu: $\\ 350\\div100=3.5$', size=26, col=1)
q13e = I('q13e', 'Half a person? $\\ $Impossible', size=24, col=1)

video('solve-ch-q13', 'solution', qid='ch-q13', slides=[
    S('Whole people',
      L("Daniel the photographer worked in the hall on one day last week. He photographed exactly one percent of the "
        "wedding guests. Which of these cannot be the day he worked?", pt('stem', 'Daniel the photographer'), voice='calm', pause=0.5),
      L("So they ask which day is impossible. Let's look for what could break."),
      L("Daniel photographed people. People come whole, so one percent of the guests must be a whole number.",
        show(q13a, 'one percent of the guests must be')),
      L("One percent is the number divided by a hundred. Sunday has three hundred guests, so one percent is three people. "
        "Monday, four hundred, four people. Tuesday, five hundred, five people.", show(q13b, 'Sunday has three hundred')),
      L("Thursday's bar stops halfway between three hundred and four hundred. So three hundred fifty guests.",
        show(q13c['t'], "Thursday's bar stops halfway")),
      L("Three hundred fifty divided by a hundred is three and a half. Half a person? That's impossible.",
        show(q13d, 'Three hundred fifty divided by'), show(q13e, 'Half a person')),
      L("So Thursday cannot be the day."),
      L("Choice number four is our answer, and I'll see you in the next question.", mk('tick', 'choice 4', 'Choice number four is our answer')),
      pre=q13_pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q14
q14_pre, q14c = QPRE('ch-q14', 'q14c', [('s', plus(S3, SLICE3('Sunday', 0), SLICE3('Sunday', 2)))])
q14a = I('q14a', "Groom's side $=$ groom's only $+$ shared", size=24, col=1)
q14b = IH('q14b', 'Sun: $\\ 60+20=80\\%$', size=24, col=1)
q14d = IH('q14d', '$10\\%$ of $300=30$', size=24, col=1)
q14e = IH('q14e', '$80\\%$: $\\ 8\\cdot30=240$', size=24, col=1)
q14_2pre, q14k = QPRE('ch-q14', 'q14k')
q14f = IH('q14f', 'Mon: $\\ 75\\%$ of $400$', size=24, col=1)
q14g = IH('q14g', '$400\\div4=100$, $\\ 3\\cdot100=300$', size=24, col=1)
q14h = IH('q14h', 'Tue: $\\ 50\\%$ of $500=250$', size=24, col=1)
q14i = IH('q14i', 'Thu: $\\ 50\\%$ of $350=175$', size=24, col=1)
q14j = I('q14j', 'Not the tallest bar, $\\ $not the biggest percent', size=24, col=1)

video('solve-ch-q14', 'solution', qid='ch-q14', slides=[
    S("The groom's side",
      L("On which day was the number of guests from the groom's side, only or shared, the greatest?", pt('stem', 'On which day was'),
        voice='calm', pause=0.5),
      L("So the groom's side here is two slices. The groom's side only, plus the shared guests.", show(q14a, "the groom's side here is two slices")),
      L("And they ask for a number of guests. So we need both the percent and the bar. Percent times the number of guests."),
      L("Sunday. Sixty percent plus twenty percent is eighty percent.", show(q14c['s'], 'Sixty percent plus twenty'),
        show(q14b, 'Sixty percent plus twenty')),
      L("Eighty percent of three hundred. Ten percent of three hundred is thirty. So eighty percent is eight times thirty, "
        "two hundred forty.", show(q14d, 'Ten percent of three hundred'), show(q14e, 'eight times thirty')), pre=q14_pre),
    S('The other days',
      L("Monday. Fifty plus twenty-five is seventy-five percent, of four hundred guests.", show(q14f, 'Fifty plus twenty-five')),
      L("Seventy-five percent is three quarters. A quarter of four hundred is a hundred, so three quarters is three "
        "hundred.", show(q14g, 'A quarter of four hundred')),
      L("Tuesday. Twenty-five plus twenty-five is fifty percent, of five hundred. That's half, two hundred fifty.",
        show(q14h, 'Twenty-five plus twenty-five')),
      L("Thursday. Thirty plus twenty is fifty percent, of three hundred fifty. Half of three hundred fifty is a hundred "
        "seventy-five.", show(q14i, 'Thirty plus twenty')),
      L("The greatest is Monday, three hundred."),
      L("Look at the two traps. The tallest bar is Tuesday. The biggest percent is Sunday. But neither one wins, because we "
        "need both numbers together.", show(q14j, 'Look at the two traps')),
      L("Choice number two is our answer, and I'll see you in the next question.", mk('tick', 'choice 2', 'Choice number two is our answer')),
      pre=q14_2pre),
])

# ------------------------------------------------------------------------------------------------ solve-ch-q15
q15_pre, q15c = QPRE('ch-q15', 'q15c', [('m', plus(S3, BAR3('Monday', '400'), PIE3('Monday')))])
q15a = IH('q15a', '$50\\%$ of $400=200$; mean gift $150$', size=24, col=1)
q15b = IH('q15b', '$25\\%$ of $400=100$; mean gift $250$', size=24, col=1)
q15d = IH('q15d', '$100$ guests; mean gift $350$', size=24, col=1)
q15e = IH('q15e', '$200\\cdot150=30{,}000$', size=24, col=1)
q15f = IH('q15f', '$100\\cdot250=25{,}000$', size=24, col=1)
q15g = IH('q15g', '$100\\cdot350=35{,}000$', size=24, col=1)
q15_2pre, q15k = QPRE('ch-q15', 'q15k', [('m', plus(S3, PIE3('Monday')))])
q15h = IH('q15h', 'total: $\\ 90{,}000$', size=24, col=1)
q15i = IH('q15i', '$90{,}000\\div400=900\\div4=225$', size=24, col=1)
q15_3pre, q15m = QPRE('ch-q15', 'q15m', [('m', plus(S3, PIE3('Monday')))])
q15j = I('q15j', '$250$: $\\ $exactly between $150$ and $350$', size=24, col=1)
q15l = I('q15l', 'More guests in the low-average group: $\\ $the overall average is below $250$', size=24, col=1)

video('solve-ch-q15', 'solution', qid='ch-q15', slides=[
    S('Method 1 · The math way',
      L("At the wedding on Monday, the guests from the groom's side only gave a gift of a hundred fifty shekels on "
        "average. The bride's side only gave two hundred fifty on average. And the shared guests gave three hundred fifty "
        "on average.", pt('stem', 'At the wedding on Monday'), voice='calm', pause=0.5),
      L("What can be said about the average gift of a guest at Monday's wedding?", pt('stem', 'What can be said'), voice='calm'),
      L("A lot of students say two hundred fifty. It's the middle of a hundred fifty, two hundred fifty and three hundred "
        "fifty. But we can't just average the three amounts without checking the group sizes."),
      L("We'll solve it in two different ways. The math way, and then by understanding, with the seesaw from averages."),
      L("Let's start with the math way. Monday's bar is four hundred guests. And the pie says fifty, twenty-five and "
        "twenty-five percent.", show(q15c['m'], "Monday's bar is four hundred")),
      L("Fifty percent of four hundred is two hundred guests. Their average gift was a hundred fifty.", show(q15a, 'Fifty percent of four hundred')),
      L("Twenty-five percent of four hundred is a hundred guests. Their average gift was two hundred fifty.", show(q15b, 'Twenty-five percent of four hundred')),
      L("And the other hundred guests, the shared ones, gave three hundred fifty on average.", show(q15d, 'the other hundred guests')),
      L("Now the total money from each group is its number of guests times its average gift. Two hundred times a hundred fifty is thirty thousand.", show(q15e, 'Two hundred times a hundred fifty')),
      L("A hundred times two hundred fifty is twenty-five thousand.", show(q15f, 'A hundred times two hundred fifty')),
      L("And a hundred times three hundred fifty is thirty-five thousand.", show(q15g, 'a hundred times three hundred fifty')),
      pre=q15_pre),
    S('The average gift',
      L("Thirty thousand plus twenty-five thousand is fifty-five thousand. Plus thirty-five thousand is ninety thousand "
        "shekels.", show(q15h, 'Plus thirty-five thousand')),
      L("The average is the total divided by the four hundred guests. Ninety thousand divided by four hundred is nine "
        "hundred divided by four. That's two hundred twenty-five.", show(q15i, 'nine hundred divided by four')),
      L("Two hundred twenty-five is less than two hundred fifty. That's choice number one."), pre=q15_2pre),
    S('Method 2 · Understanding: the weights',
      L("[pause] Now by understanding, from the givens again. Remember the seesaw. The average sits nearer the heavier "
        "group."),
      L("Two hundred fifty is exactly in the middle between a hundred fifty and three hundred fifty.", show(q15j, 'exactly in the middle')),
      L("The pie says half of the guests are on the groom's side only. Their average gift was a hundred fifty, the lowest group average. The "
        "three hundred fifty group is only a quarter.", show(q15m['m'], 'The pie says half')),
      L("So the low side is heavier, and it pulls the average down, below two hundred fifty.", show(q15l, 'pulls the average down')),
      L("Choice number one is our answer, and I'll see you in the next question.", mk('tick', 'choice 1', 'Choice number one is our answer')),
      pre=q15_3pre),
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



# =================================================================================================================
# topic 52: the passes, adapted to charts
# =================================================================================================================
_method_headers_plain = _method_headers


def _method_headers(vid):
    """the small "Method N: X" header line - not on a slide with a chart (it would go under the chart; the sidebar and
    the slide title name the method)"""
    V = VIDEOS[vid]
    keep = [sl for sl in V['slides'] if any(p.get('_chart') for p in (sl.get('pre') or []))]
    saved = [(sl, sl['title']) for sl in keep]
    for sl in keep: sl['title'] = '_' + sl['title']
    try: _method_headers_plain(vid)
    finally:
        for sl, t in saved: sl['title'] = t


def _no_stem(vid):
    """a POINT on 'stem' on a slide with no question text (a lesson, the chart page): on the slide's chart instead, or
    dropped"""
    V = VIDEOS[vid]
    for sl in V['slides']:
        pre = sl.get('pre') or []
        if any(p.get('_stem') for p in pre): continue
        ch = next((p['_name'] for p in pre if p.get('_chart')), None)
        for ln in sl['lines']:
            new = []
            for c in ln['cues']:
                if c[0] == 'point' and c[1] == 'stem':
                    if not ch: continue
                    c = ('point', ch) + tuple(c[2:])
                new.append(c)
            ln['cues'] = new


# 21 Oct, direct review L: derived rows wait for their spoken result, not merely
# the question or the first input. Chart data themselves remain visible as givens.
def _result_at(vid, name, phrase):
    found = []
    for sl in VIDEOS[vid]['slides']:
        for ln in sl['lines']:
            for j, c in enumerate(ln['cues']):
                if c[0] == 'show' and c[1]['_name'] == name:
                    assert phrase.lower() in ln['say'].lower(), (vid, name, phrase)
                    ln['cues'][j] = show(c[1], phrase)
                    ln['cues'].sort(key=lambda q: _phrase_pos(ln['say'], q))
                    found.append(name)
    assert len(found) == 1, (vid, name, found)

_RESULTS52 = {
 'ch52-tables': {
  't_a1':'is a hundred forty', 't_a2':'is two hundred twenty', 't_a3':'is three hundred twenty',
  't_a4':'is eighty', 't_s1':'is twenty', 't_s2':'is zero', 't_s3':'is twenty again',
  't_p1':'is two thirds', 't_e3':"it's sixty-two and a half percent", 't_e4':'Sixty-two and a half percent again',
  't_e5':"That's simply sixty-five percent", 't_o1':'is thirty-six', 't_o2':'is nine'},
 'ch52-scatter': {'p_v1':'is twelve', 'p_v2':'is ten', 'p_v3':'is eight',
                  'p_v4':'the average is less than ten thousand per dealer'},
 'ch52-line': {'l_r1':'is ten', 'l_r2':'is fifteen', 'l_r3':'is twenty', 'l_r4':'is twenty again'},
 'ch52-bar': {'b_n10':'Look at two thousand eleven', 'b_n12':'is a hundred ten',
              'b_n13':'is thirty', 'b_n17':'fifty thousand'},
 'ch52-continuous': {'s_r1':'so half more', 's_r2':'an eighth of four hundred',
                     's_r5':'less than four times the starting number'},
 'ch52-range': {'r_n7':'is three thousand five hundred', 'r_e2':'is five thousand',
                'r_d1':'is five thousand', 'r_d4':'is only five thousand'},
 'ch52-circle': {'c_n12':'a hundred sixty are in the forum'},
 'ch52-cumulative': {'u_n6':'is twenty', 'u_n7':'is thirty', 'u_n10':'is zero',
                     'u_n11':'so eighty thousand shekels'},
 'ch52-change': {'h_n4':'a hundred ten', 'h_n6':'is a hundred fifteen',
                 'h_r1':'is eighty', 'h_r2':'is eighty-five', 'h_r4':'is seventy-five'},
 'solve-ch-q01': {'q1a':'three', 'q1b':'six', 'q1e':'is six'},
 'solve-ch-q04': {'q4f':'from twelve to sixteen percent'},
 'solve-ch-q07': {'q7i':'is nine'},
 'solve-ch-q08': {'q8b':'is two hundred forty thousand', 'q8d':'is a hundred thousand',
                  'q8e':'twenty thousand', 'q8f':'is three hundred sixty thousand',
                  'q8i':'Eighty gives plus twenty again'},
 'solve-ch-q09': {'q9b':'is thirty thousand', 'q9d':'is a hundred fifty thousand',
                  'q9e':'is twenty thousand', 'q9f':'a hundred thirty thousand'},
 'solve-ch-q10': {'q10a':'is two hundred', 'q10b':'is two hundred eighty',
                  'q10d':"That's forty thousand", 'q10e':'is a hundred each',
                  'q10f':'Plus eighty is two hundred eighty again'},
 'solve-ch-q11': {'q11e':'Thursday, thirty and fifty'},
 'solve-ch-q12': {'q12d':'is two hundred fifty'},
 'solve-ch-q13': {'q13b':'five people', 'q13d':'is three and a half'},
 'solve-ch-q14': {'q14b':'is eighty percent', 'q14d':'is thirty', 'q14e':'two hundred forty',
                  'q14f':'of four hundred guests', 'q14g':'so three quarters is three hundred',
                  'q14h':'two hundred fifty', 'q14i':'is a hundred seventy-five'},
 'solve-ch-q15': {'q15a':'two hundred guests', 'q15b':'a hundred guests',
                  'q15d':'three hundred fifty on average', 'q15e':'is thirty thousand',
                  'q15f':'is twenty-five thousand', 'q15g':'is thirty-five thousand',
                  'q15h':'is ninety thousand shekels', 'q15i':"That's two hundred twenty-five"},
}
for _vid, _rows in _RESULTS52.items():
    for _name, _phrase in _rows.items(): _result_at(_vid, _name, _phrase)

# The stacked-bar bracket contains the derived 50; move it to the calculation.
_sl52 = next(sl for sl in VIDEOS['ch52-bar']['slides']
             if any(c[0]=='show' and c[1]['_name']=='b_c5_g' for ln in sl['lines'] for c in ln['cues']))
_g52 = [(ln,c) for ln in _sl52['lines'] for c in ln['cues'] if c[0]=='show' and c[1]['_name']=='b_c5_g']
assert len(_g52)==1, ('stacked-bar bracket',len(_g52))
_old52,_cue52 = _g52[0]
_old52['cues'].remove(_cue52)
_to52 = next(ln for ln in _sl52['lines'] if 'minus sixty, fifty thousand' in ln['say'])
_to52['cues'].append(show(_cue52[1], 'fifty thousand'))
_to52['cues'].sort(key=lambda q:_phrase_pos(_to52['say'],q))

# the camera lesson in parts of about 3-4 minutes (math_patches/_camera_parts.py), the long lessons in parts (not on
# camera), before the visual passes
_cp_spec = importlib.util.spec_from_file_location('_camera_parts', os.path.join(HERE, '_camera_parts.py'))
CP = importlib.util.module_from_spec(_cp_spec); _cp_spec.loader.exec_module(CP)
CP.split(globals(), *CAMERA_SPLIT)
for _sp in SPLITS: CP.split(globals(), *_sp)

for _v in ORDER: _method_headers(_v); _densify(_v); _follow(_v); _fill(_v); _no_stem(_v); _write_gap(_v)

# carry-over boxes (V2) and the layer-order check (V1), steady highlights, like topic 25
import types as _types
MV.carry(_types.SimpleNamespace(**globals()), CARRY52)
for _v in CARRY52:
    for _sl in VIDEOS[_v]['slides']:
        for _ln in _sl['lines']:
            for _c in _ln['cues']:
                if _c[0] == 'show' and _c[1].get('keep'): _c[1]['size'] = 28
MV.calm(_types.SimpleNamespace(**globals()), ORDER)
_lp = [(v, p) for v in ORDER for p in MV.check_layers(VIDEOS[v])]
assert not _lp, ('figure layers out of order', _lp)

# one vocabulary for method names (math_patches/_method_names.py CORE)
_mn_spec = importlib.util.spec_from_file_location('_method_names_vocab', os.path.join(HERE, '_method_names.py'))
_mn = importlib.util.module_from_spec(_mn_spec); _mn_spec.loader.exec_module(_mn)
_mn.check_vocab(VIDEOS)


if __name__ == '__main__':
    _bad = 0
    for _v in sys.argv[1:] or ORDER:
        _p = check(_v)
        if _p: print('PROBLEMS', _v, _p); _bad += 1
        print('script written:', write_json(_v), stats(_v))
    for x in WRITE_LATE: print('mark dropped (its item is still being written):', x)
    print('total: %d videos, %.1f minutes' % (len(ORDER), sum(stats(v)['minutes'] for v in ORDER)))
    sys.exit(1 if _bad else 0)
