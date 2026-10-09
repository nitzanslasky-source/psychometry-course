"""Topic 31 - Triangles. Course review 2026-09 fixes.
See t31_CHANGES.md for the plain-language list."""
import math, re
import math_api
from dsl import T, H, A, D, Q
from math_api import VIS

TOPIC = 31
L1, L2 = 'geo31-learn-1', 'geo31-learn-2'
FOUND, ADV = 'geo31-foundation-practice', 'geo31-advanced-practice'
V_TRI, V_SPEC, V_AREA, V_EQ, V_MED = 'geo-009', 'geo-013', 'geo-016', 'geo-017-after', 'geo-018-after'
V_PYT, V_TRIP, V_3060, V_4545 = 'geo-019', 'geo-024', 'geo-026', 'geo-027-after'
N = ['q-r26-t31-%02d' % k for k in range(1, 13)]
C = r'\text{ cm}'

# ---------------------------------------------------------------------------------------------
# SVG helpers - same style as the course figures (ink #203344, teal #087f83, DejaVu Sans 20/18)
# ---------------------------------------------------------------------------------------------
INK, TEAL, FONT = '#203344', '#087f83', 'DejaVu Sans,Arial,sans-serif'


def _f(v): return '%.3f' % v


def _svg(vb, title, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, title, title, ''.join(body)))


def _poly(*pts):
    return ('<polygon points="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>'
            % (' '.join('%s,%s' % (_f(x), _f(y)) for x, y in pts), INK))


def _ln(p, q, color=INK, w=2.5, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>' % (
        _f(p[0]), _f(p[1]), _f(q[0]), _f(q[1]), color, w, d)


def _tx(p, s, color=INK, size=20):
    return ('<text x="%s" y="%s" text-anchor="middle" dominant-baseline="middle" fill="%s" font-family="%s" '
            'font-size="%d">%s</text>' % (_f(p[0]), _f(p[1]), color, FONT, size, s))


def _pt(c, r, a):
    return (c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))


def _ang(c, p): return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))


def _arc(c, r, a1, a2, color=TEAL):
    """arc around c from angle a1 to a2 (degrees, SVG y-down), the short way given by the sign of a2-a1."""
    p, q = _pt(c, r, a1), _pt(c, r, a2)
    return '<path d="M %s %s A %s %s 0 %d %d %s %s" fill="none" stroke="%s" stroke-width="2"/>' % (
        _f(p[0]), _f(p[1]), _f(r), _f(r), 1 if abs(a2 - a1) > 180 else 0, 1 if a2 > a1 else 0, _f(q[0]), _f(q[1]), color)


def _arc_tick(c, r, a, L=5):
    return _ln(_pt(c, r - L, a), _pt(c, r + L, a), TEAL, 1.8)


def _right(c, a1, a2, s=12):
    p, q = _pt(c, s, a1), _pt(c, s, a2)
    m = (p[0] + q[0] - c[0], p[1] + q[1] - c[1])
    return _ln(p, m, TEAL, 1.7) + _ln(m, q, TEAL, 1.7)


def _unit(p, q):
    d = math.hypot(q[0] - p[0], q[1] - p[1]); return ((q[0] - p[0]) / d, (q[1] - p[1]) / d)


# ---------------------------------------------------------------------------------------------
# text helpers
# ---------------------------------------------------------------------------------------------
def _script(M, vid, n):
    """The current script of a slide, in DSL form (so it can be edited and passed to set_slide)."""
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _say(M, vid, n, old, new):
    """Replace a spoken line that contains `old` (new=None deletes it, a list inserts several lines)."""
    hit = []

    def fn(lines):
        out = []
        for l in lines:
            if 'say' in l and old in l['say']:
                hit.append(1)
                if new is None: continue
                for s in ([new] if isinstance(new, str) else new): out.append({'say': s})
                continue
            out.append(l)
        return out
    M.edit_lines(vid, n, fn)
    assert hit, (vid, n, old)


def _draw(M, vid, n, old, new):
    hit = []

    def fn(lines):
        for l in lines:
            if 'draw' in l and old in l['draw']:
                l['draw'] = l['draw'].replace(old, new); hit.append(1)
        return lines
    M.edit_lines(vid, n, fn)
    assert hit, (vid, n, old)


def _add_lines(M, vid, n, new, after=None):
    """Append spoken/draw lines (str = say, ('D', x) = draw) at the end, or after the line containing `after`."""
    conv = [{'say': x} if isinstance(x, str) else {'draw': x[1]} for x in new]

    def fn(lines):
        if after is None: return lines + conv
        for k, l in enumerate(lines):
            if after in (l.get('say') or l.get('draw') or ''):
                return lines[:k + 1] + conv + lines[k + 1:]
        raise KeyError(after)
    M.edit_lines(vid, n, fn)


def _vis_item(M, vid, n):
    return next(it for it in M.slide(vid, n)['items'] if it.get('k') == 'vis')


def _edit_q_svg(M, qid, fn):
    """Apply fn(svg) to a question's figure and to every copy of it on the slides."""
    q = M.q(qid)
    M.set_q(qid, figure=fn(q['questionVisual']['svg']))
    for v in M.D['videos'].values():
        for b in v.get('beats', []):
            for it in b.get('items', []):
                if it.get('k') == 'q' and it.get('qid') == qid and isinstance(it.get('fig'), dict):
                    it['fig'] = dict(it['fig'], svg=fn(it['fig']['svg'])); M.touched_videos.add(v['id'])


def _drop(svg, *needles, texts=()):
    """Remove every <line>/<path> element that contains one of the needles, and the <text> labels in `texts`."""
    for nd in needles:
        svg = re.sub(r'<(line|path)[^>]*%s[^>]*/>' % re.escape(nd), '', svg)
    for t in texts:
        svg = re.sub(r'<text[^>]*>%s</text>' % re.escape(t), '', svg)
    return svg


def _lesson_actives(M, vid):
    k = 0
    for b in M.video(vid)['beats']:
        if b['mode'] == 'concept':
            b['active'] = k; k += 1


def _solution(M, qid, group, num, intro, slides, fig=True):
    """Guided-question solution video in the style of the topic's solve-geo31-* videos (placed after its question)."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=0, title=title,
                          pre=[Q(qid, figw=0.56, figalign='left') if fig else Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, group, ['Question %d' % n], beats, M.section_of(qid), kind='solution', qid=qid)
    v['beats'][0]['title'] = group
    v['hybrid']['num'] = num
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _fix_sidebars(M):
    """Solution videos between two lessons form a group: each lists the group's questions (renumbered later)."""
    for sec in (L1, L2):
        groups, cur = [], []
        for f in M.D['flow']:
            if f['section'] != sec or f['type'] != 'video': continue
            v = M.video(f['ref'])
            if v.get('kind') == 'solution': cur.append(f['ref'])
            elif cur: groups.append(cur); cur = []
        if cur: groups.append(cur)
        for g in groups:
            labels = [M.video(v)['beats'][0]['bigTitle'] for v in g]
            for k, vid in enumerate(g):
                M.set_sidebar(vid, labels)
                for b in M.video(vid)['beats']:
                    if b['mode'] != 'title': b['active'] = k


_BRIT = [('memorising', 'memorizing'), ('memorise', 'memorize'), ('centimetres', 'centimeters'), ('Centimetres', 'Centimeters'),
         ('kilometres', 'kilometers'), ('metres', 'meters'), ('practise', 'practice'), ('Practise', 'Practice'),
         ('colours', 'colors'), ('colour', 'color'), ('recognise', 'recognize')]


def _us(t):
    for a, b in _BRIT: t = t.replace(a, b)
    return t


def _cleanup(M):
    vids = [f['ref'] for f in M.D['flow'] if f['topic'] == TOPIC and f['type'] == 'video']
    for vid in vids:
        v = M.video(vid)
        for b in v['beats']:
            for l in b['lines']:
                for k in ('say', 'draw', 'label'):
                    if k in l: l[k] = _us(l[k])
            for it in b['items']:
                if it.get('t'): it['t'] = _us(it['t'])
        v['hybrid']['sidebar'] = [_us(x) for x in v['hybrid'].get('sidebar', [])]
        M.touched_videos.add(vid)
        if v.get('kind') == 'solution' and v.get('questionId') in M.D['questions']:
            v['title'] = v['navLabel'] = M.q(v['questionId'])['stem']


# ---------------------------------------------------------------------------------------------
# figures
# ---------------------------------------------------------------------------------------------
# the lesson triangle of "Triangles" (geo-009)
TA, TB, TC = (189.459, 278.531), (450.541, 278.531), (366.894, 81.469)


def fig_exterior():
    u = _unit(TA, TC)                                  # direction A -> C, continued past C
    E = (TC[0] + 85 * u[0], TC[1] + 85 * u[1])
    aU, aCB, aCA = _ang(TC, E), _ang(TC, TB), _ang(TC, TA)
    return _svg('139.5 0 395.8 321.6', 'Triangle ABC with an exterior angle at C', [
        _poly(TA, TB, TC), _ln(TC, E),
        _tx((171.459, 295.531), 'A'), _tx((468.541, 295.531), 'B'), _tx((346.0, 66.0), 'C'),
        '<path d="M 215.567 278.531 A 26.108 26.108 0 0 0 206.929 259.128" fill="none" stroke="%s" stroke-width="2"/>' % TEAL,
        _tx((231.524, 259.802), 'α', TEAL, 18),
        '<path d="M 440.340 254.498 A 26.108 26.108 0 0 0 424.433 278.531" fill="none" stroke="%s" stroke-width="2"/>' % TEAL,
        _tx((412.144, 253.116), 'β', TEAL, 18),
        _arc(TC, 26, aCB, aCA), _tx(_pt(TC, 46, (aCB + aCA) / 2), 'γ', TEAL, 18),
        _arc(TC, 26, aU, aCB), _tx(_pt(TC, 46, (aU + aCB) / 2), 'δ', TEAL, 18),
    ])


def fig_bisector():
    ca, cb = math.hypot(TA[0] - TC[0], TA[1] - TC[1]), math.hypot(TB[0] - TC[0], TB[1] - TC[1])
    Dx = TA[0] + (TB[0] - TA[0]) * ca / (ca + cb); Dp = (Dx, TA[1])
    aA, aB, aD = _ang(TC, TA), _ang(TC, TB), _ang(TC, Dp)
    return _svg('139.5 35.5 361.1 288.1', 'Triangle ABC with the angle bisector from C', [
        _poly(TA, TB, TC),
        _tx((171.459, 295.531), 'A'), _tx((468.541, 295.531), 'B'), _tx((366.894, 61.469), 'C'),
        _ln(TC, Dp, TEAL), _tx((Dx, 298.531), 'D'),
        _arc(TC, 34, aD, aA), _arc(TC, 34, aB, aD),
        _arc_tick(TC, 34, (aD + aA) / 2), _arc_tick(TC, 34, (aB + aD) / 2),
    ])


def _alt_hyp(labels, title, h=None):
    """Right triangle (right angle at C, on top) with the altitude CD to the hypotenuse AB (3-4-5 shape)."""
    A_, B_, D_, C_ = (170, 290), (470, 290), (278, 290), (278, 146)
    body = [_poly(A_, B_, C_), _ln(C_, D_, TEAL),
            _right(C_, _ang(C_, A_), _ang(C_, B_), 18), _right(D_, -90, 0),
            _tx((152, 302), 'A'), _tx((488, 302), 'B'), _tx((278, 126), 'C'), _tx((278, 312), 'D'),
            _tx((208, 206), labels[0]), _tx((390, 206), labels[1]), _tx((392, 312), labels[2])]
    if h: body.append(_tx((292, 222), h))
    return _svg('120 100 400 230', title, body)


def fig_area_two_ways(): return _alt_hyp(('6', '8', '10'), 'Area of a right triangle in two ways', 'h')


def fig_q01(): return _alt_hyp(('15', '20', '25'), 'Altitude to the hypotenuse')


def fig_max_area():
    P, Qp, V = (170, 280), (410, 280), (170, 100)
    S = _pt(P, 180, -50); F = (S[0], 280)
    return _svg('120 70 320 250', 'Two sides with a changing angle between them', [
        _poly(P, Qp, V), _right(P, -90, 0),
        _ln(P, S, INK, 2.5, '7 5'), _ln(S, Qp, INK, 2.5, '7 5'), _ln(S, F, TEAL, 2.5, '7 5'), _right(F, -90, 180, 10),
        _tx((290, 300), '8'), _tx((154, 190), '6'), _tx((214, 199), '6'), _tx((298, 225), 'h'),
    ])


def fig_p20():
    B_, C_, A_ = (190, 190), (390, 190), (260, 60)
    E = (490, 290); E2 = (515, 315)
    aAB, aAC = _ang(A_, B_), _ang(A_, C_)
    aBA = _ang(B_, A_)
    return _svg('0 0 640 360', 'A triangle, a line parallel to its base and three angles', [
        _poly(A_, B_, C_), _ln((110, 190), (470, 190)), _ln((110, 290), (570, 290)), _ln(C_, E2),
        _tx((260, 40), 'A'), _tx((194, 210), 'B'), _tx((372, 210), 'C'), _tx((474, 308), 'E'), _tx((586, 290), 'ℓ', INK, 22),
        _arc(A_, 24, aAC, aAB), _tx(_pt(A_, 40, (aAB + aAC) / 2), 'p', TEAL, 18),
        _arc(B_, 24, aBA, -180), _tx(_pt(B_, 40, (aBA - 180) / 2), 'q', TEAL, 18),
        _arc(E, 24, 0, -135), _tx(_pt(E, 40, -67.5), 'r', TEAL, 18),
    ])


# ---------------------------------------------------------------------------------------------
def apply(M):
    S = M.set_q

    # =========================================================================================
    # 1. Lesson "Triangles" (geo-009): angle bisector, exterior angle as a core rule, clean figure
    # =========================================================================================
    M.set_slide(V_TRI, 7, script=[
        A('Triangle ABC with α, β, γ and the extension of AC appears', VIS(fig_exterior(), w=1000, h=520)),
        "An exterior angle of a triangle equals the sum of the two interior angles that are not next to it.",
        "First of all — what is an exterior angle?",
        D('Trace the extension of AC past C, and the angle δ between it and CB'),
        "Extend side AC past C. The angle between the extension and side CB — that's an exterior angle. Let's call it delta.",
        "It's outside the triangle — so it's exterior. Gamma, inside, is next to it.",
        A("'Exterior angle δ = α + β' appears",
          T(r'Exterior angle: $\delta=\alpha+\beta$ (the two interior angles not next to it)', size=38, x=410, y=650)),
        "The rule says: delta equals alpha plus beta. Let's prove it.",
        D('Write γ + δ = 180°'),
        "Gamma and delta are adjacent angles on a straight line. Together: 180.",
        D('Write α + β + γ = 180°'),
        "And by the angle sum: alpha plus beta plus gamma is also 180.",
        D('Cover γ in both lines; write α + β = δ'),
        "Both lines have gamma, and both give 180. So what's left must be equal: alpha plus beta equals delta.",
    ])
    _say(M, V_TRI, 8, "Honestly — we don't use this rule a lot on the exam.",
         "This rule shows up a lot on the exam. It's a core rule — learn it.")
    _say(M, V_TRI, 8, "And we don't really need it",
         "You can always go the long way too: find the angle next to the exterior angle, and use the angle sum.")
    _say(M, V_TRI, 8, "But if we know it — it can save us time",
         "But the rule saves a step — and on the exam, a step is time. Look.")
    M.set_slide(V_TRI, 12, script=[
        "Let's see an extension of this rule.",
        A("'c < a + b' appears", T('$c<a+b$', size=52)),
        "c is less than a plus b — two sides together are greater than the third.",
        A("'c + b > a' appears", T('$c+b>a$', size=52)),
        "But c and b are also two sides — so together they're greater than a.",
        D('Move b across: write c > a − b'),
        "Move b to the other side — and we get c is greater than a minus b.",
        A("'big − small < c < sum' appears", T(r'big $-$ small $<c<$ sum', size=56)),
        "Put them together: a side of a triangle is less than the sum of the other two sides — and greater than their difference.",
        "The difference is always big minus small. For 7 and 12 it's 12 minus 7 — not 7 minus 12.",
        D("Circle the two '<' signs"),
        "And both signs are strict — it can't be equal to either end.",
        "For sides 7 and 12: more than 5 and less than 19.",
        A("'Whole numbers? 2 × shorter − 1 lengths' appears",
          T(r'Whole-number lengths: $2\times$ shorter side $-\,1$', size=44)),
        "How many whole-number lengths can the third side have? 6, 7, and so on up to 18. That's 13 lengths.",
        D('Write 2 × 7 − 1 = 13'),
        "Quick count: twice the shorter side, minus 1. Twice 7 is 14, minus 1 — 13.",
        "We'll use all of this in a moment.",
    ])
    M.set_slide(V_TRI, 13, script=[
        A("'Median · Altitude · Bisector' appears",
          T(r'Median: midpoint · Altitude: $90°$ (maybe outside) · Bisector: two equal angles', size=36)),
        A("'Angle sum' appears", T(r'Angle sum: $\alpha+\beta+\gamma=180°$', size=42)),
        A("'Exterior angle' appears", T(r'Exterior angle $=$ sum of the two interior angles not next to it', size=38)),
        A("'Larger side opposite larger angle' appears", T('Larger side opposite larger angle', size=42)),
        A("'big − small < side < sum' appears", T(r'big $-$ small $<$ side $<$ sum', size=42)),
        D('Underline the angle-sum line and the exterior-angle line'),
        "Those are the rules. The angle sum and the exterior angle are the ones you'll use most.",
        "Let's see some sample questions.",
    ])
    M.insert_slides(V_TRI, 5, [dict(mode='concept', title='Angle bisector', script=[
        A('Triangle ABC with the bisector CD appears', VIS(fig_bisector(), w=1000, h=520)),
        "The third special line: the angle bisector.",
        "We met it in the angles topic. It splits an angle into two equal angles.",
        D('Mark the two equal angles at C'),
        "Here it starts at C, splits the angle at C in half, and goes down to the side opposite it.",
        A("'Angle bisector: two equal angles' appears", T('Angle bisector: two equal angles', size=44, x=410, y=650)),
        "That's all it promises: two equal angles.",
        "No equal pieces of the side, and no right angle. Look: AD and DB are not equal here.",
        "Median — equal pieces. Altitude — a right angle. Bisector — equal angles. Three different lines.",
        "In a moment, in the isosceles triangle, we'll see all three become one line.",
    ])])
    M.set_sidebar(V_TRI, ['Median', 'Three medians', 'Altitude', 'Altitude outside', 'Angle bisector', 'Angle sum 180°',
                          'Exterior angle', 'Two routes', 'Side vs. angle', 'Two sides > third', 'The shortest path',
                          'Between diff and sum', 'Recap'])
    _lesson_actives(M, V_TRI)

    c = M.card('mem-triangle-rules')
    c['intro'] = 'The general triangle rules. The angle sum and the exterior angle are the ones you will use most.'
    rows = c['tables'][0]['rows']
    rows.insert(2, ['Angle bisector', 'splits the angle at a vertex into two equal angles', 'no equal pieces, no right angle promised'])
    for r in rows:
        if r[0] == 'Exterior angle': r[2] = 'core rule — used again and again'
        if r[0] == 'Range of a side':
            r[1] = '\\(\\text{big}-\\text{small}<c<a+b\\)'; r[2] = 'strict — never equal to either end'
    rows.append(['Whole-number third side', 'count \\(=2\\times\\) shorter side \\(-\\,1\\)', 'sides 7 and 12: \\(2\\cdot7-1=13\\) lengths'])

    # Q3 video: the exterior angle is not optional
    _say(M, 'solve-geo31-g012', 3, "If you already remember that — take the exterior angle too",
         "And the exterior angle: it equals the two interior angles not next to it. It comes up again and again — learn it too.")
    _say(M, 'solve-geo31-g012', 3, "You can solve without it", "You can always go the long way, but the rule saves time.")

    # =========================================================================================
    # 2. Lesson "Special Triangles" (geo-013): plain figures, the converse, softer "rare"
    # =========================================================================================
    it = _vis_item(M, V_SPEC, 2)   # plain isosceles triangle: no symmetry line, no right angle, no base ticks yet
    it['v'] = dict(it['v'], svg=_drop(it['v']['svg'], 'stroke-dasharray', 'stroke-width="1.7"', 'y1="271.493"'))
    sc = _script(M, V_SPEC, 2)
    sc = [x for x in sc if not (isinstance(x, tuple) and x[0] == 'A' and x[2].get('t', '').startswith('Vertex'))]
    k = next(i for i, x in enumerate(sc) if isinstance(x, str) and x.startswith('If the vertex angle is 44'))
    sc[k:k] = [A("'Vertex 44° → base angles 68°' appears",
                 T(r'Vertex $44°$ → base angles $\dfrac{180°-44°}{2}=68°$', size=44, x=410, y=650))]
    sc += [
        "And it works backwards too.",
        A("'Base angles equal ⇔ legs equal' appears", T(r'Base angles equal $\Leftrightarrow$ legs equal', size=40, x=410, y=760)),
        "If two angles of a triangle are equal, the sides opposite them are equal. Two equal angles? The triangle is isosceles.",
    ]
    M.set_slide(V_SPEC, 2, script=sc)
    sc = _script(M, V_SPEC, 5)
    sc = [A(x[1], T(r'$180°\div3=60°$', size=x[2]['size'], **{k: x[2][k] for k in ('x', 'y') if k in x[2]}))
          if isinstance(x, tuple) and x[0] == 'A' and x[2].get('t', '').startswith('$180') else x for x in sc]
    M.set_slide(V_SPEC, 5, script=sc)
    it = _vis_item(M, V_SPEC, 6)   # plain right triangle: no median yet
    it['v'] = dict(it['v'], svg=_drop(it['v']['svg'], 'stroke-dasharray', 'stroke-width="1.8"', texts=('M',)))
    it['v']['svg'] = it['v']['svg'].replace('aria-label="A right triangle and the median to its hypotenuse"',
                                            'aria-label="A right triangle"').replace(
        '<title>A right triangle and the median to its hypotenuse</title>', '<title>A right triangle</title>')
    _say(M, V_SPEC, 7, "It's very rare.", "It's less common on the exam — but it comes back with circles. So learn it.")
    _say(M, V_SPEC, 7, "Like I said — very rare on the exam.", "Remember it: we'll meet it again in circles.")
    sc = _script(M, V_SPEC, 8)
    new = []
    for x in sc:
        if isinstance(x, tuple) and x[0] == 'A':
            t = x[2]['t']
            if t.startswith('Isosceles'):
                x = A(x[1], dict(x[2], t=r'Isosceles: symmetric — base angles equal $\Leftrightarrow$ legs equal; '
                                      r'median $=$ altitude $=$ bisector', size=38))
            if 'Median to the hypotenuse' in t:
                x = A(x[1], dict(x[2], t=r'Right triangle: median to the hypotenuse $=$ half the hypotenuse'))
        new.append(x)
    M.set_slide(V_SPEC, 8, script=new)
    c = M.card('mem-special-triangles')
    for r in c['tables'][0]['rows']:
        if r[0] == 'Isosceles': r[2] = 'base angles equal \\(\\Leftrightarrow\\) legs equal'
        if r[0].startswith('Right: median'): r[3] = 'comes back in circles'
    c['tips'][0] = 'Isosceles vertex angle \\(v\\): each base angle is \\(\\dfrac{180°-v}{2}\\).'
    c['tips'].append('Two equal angles? Then the sides opposite them are equal — the triangle is isosceles.')

    # =========================================================================================
    # 3. Lesson "Area of Triangles" (geo-016): area two ways, largest possible area
    # =========================================================================================
    M.set_slide(V_AREA, 8, script=[
        A("'Rectangle' appears", T(r'Rectangle: width $\times$ length', size=38)),
        A("'Right triangle' appears", T(r'Right triangle: $\dfrac{\text{leg}\times\text{leg}}{2}$', size=38)),
        A("'Any triangle' appears", T(r'Any triangle: $\dfrac{\text{side}\times\text{height to that side}}{2}$', size=38)),
        A("'Altitude outside' appears", T('Altitude outside? Still only the side itself', size=38)),
        A("'Area two ways' appears", T(r'Right triangle: leg $\times$ leg $=$ hypotenuse $\times$ altitude', size=38)),
        A("'Largest area' appears", T(r'Sides $a,\ b$: area $\le\dfrac{ab}{2}$', size=38)),
        "Let's see an example.",
    ])
    M.insert_slides(V_AREA, 7, [dict(mode='concept', title='Largest possible area', script=[
        A('Base 8 with a side 6 standing up and leaning appears', VIS(fig_max_area(), w=1000, h=520)),
        "One more trap. Two sides are 6 and 8 — but the angle between them is not given.",
        "Put the 8 on the floor. The height is how high the side 6 reaches.",
        D('Trace the leaning side 6 and its dashed height h'),
        "When the 6 leans over, the height is less than 6. The height is a leg, and the 6 is the hypotenuse — the longest side.",
        D('Trace the side 6 standing straight up'),
        "The highest it can reach: 6 itself, when it stands straight up. That's a right angle.",
        A("'Sides a, b: area ≤ ab/2' appears", T(r'Sides $a,\ b$: area $\le\dfrac{ab}{2}$ (equal only at $90°$)', size=42, x=410, y=650)),
        "So the area is at most 8 times 6 over 2: 24. It's exactly 24 only with a right angle between them.",
        "Any area up to 24 is possible. 30? Impossible. And 48 forgot to divide by 2.",
    ])])
    M.insert_slides(V_AREA, 6, [dict(mode='concept', title='Area two ways', script=[
        A('Right triangle 6-8-10 with the altitude h to the hypotenuse appears', VIS(fig_area_two_ways(), w=1000, h=520)),
        "Here's a strong move: find the same area in two ways.",
        "A right triangle: legs 6 and 8, hypotenuse 10. What is h, the altitude to the hypotenuse?",
        D('Write S = 6 · 8 ÷ 2 = 24'),
        "Way one: the legs are a side and its height. 6 times 8, over 2 — 24.",
        D('Write S = 10 · h ÷ 2 = 5h'),
        "Way two: the hypotenuse is a side too, and h is the height to it. 10 times h, over 2 — 5h.",
        D('Write 5h = 24 → h = 4.8'),
        "Same triangle, same area. 5h equals 24 — h is 4.8.",
        A("'leg × leg = hypotenuse × altitude' appears",
          T(r'Right triangle: leg $\times$ leg $=$ hypotenuse $\times$ altitude', size=40, x=410, y=650)),
        "In a right triangle this gives a short rule: leg times leg equals hypotenuse times the altitude to it. 6 times 8 is 48 — and 10 times 4.8 is 48.",
        "It works in any triangle: every side with its own height gives the same area.",
    ])])
    M.set_sidebar(V_AREA, ['Length vs. area', 'Rectangle', 'Right triangle', 'Any triangle', 'Any side as base',
                           'Area two ways', 'Outside altitude', 'Largest possible area', 'Recap'])
    _lesson_actives(M, V_AREA)

    # "A Median Halves the Area": name the rule "same base, same height"
    _add_lines(M, V_MED, 3, [
        "The same rule works when the top vertex moves along a line parallel to the base.",
        D('Draw a line through the top vertex parallel to the base, and a second triangle with its vertex on it'),
        "Same base, and the height is the distance between the parallel lines — it doesn't change. So the area doesn't change.",
    ], after="Careful: same area does NOT mean")

    c = M.card('mem-triangle-area')
    c['intro'] = 'Area is a side times the height to that side, over 2 — any side, with its own height.'
    rows = [r for r in c['tables'][0]['rows'] if not r[0].startswith('Equilateral')]
    rows[-1:-1] = [
        ['Area two ways', 'leg \\(\\times\\) leg \\(=\\) hypotenuse \\(\\times\\) altitude', 'same area from two sides — solve for the height'],
        ['Largest area', 'sides \\(a,\\ b\\): area \\(\\le\\dfrac{ab}{2}\\)', 'equal only with a right angle between them'],
    ]
    rows.append(['Same base, same height', 'same area', 'vertex moves along a parallel line — the area does not change'])
    c['tables'][0]['rows'] = rows
    c['tips'] = ['Triangles between parallel lines have the same height — the area ratio is the base ratio.',
                 'Two sides and no angle? The area can be anything up to half their product.']

    # --- new guided question A: area two ways (after Q6) --------------------------------------
    M.new_q(N[0], TOPIC, 'Triangle ABC is right at C, and CD is the altitude to AB.\nGiven:\n'
            r'$\begin{cases} AC=15' + C + r' \\ BC=20' + C + r' \\ AB=25' + C + r' \end{cases}$' + '\nWhat is CD (in cm)?',
            ['$6$', '$12$', '$12.5$', '$15$'], 2, [
                'Area with the legs: $S=\\frac{15\\cdot20}{2}=150$.',
                'Area with the side AB and its altitude CD: $S=\\frac{25\\cdot CD}{2}$.',
                'Same area: $\\frac{25\\cdot CD}{2}=150$, therefore $25\\cdot CD=300$ and $CD=12$.',
                'Traps: $6=150\\div25$ forgets to double the area; $12.5$ is half the hypotenuse (the median, not the altitude).'],
            figure=fig_q01())
    M.place_q(N[0], L1, after='solve-geo31-g017')
    _solution(M, N[0], 'Triangle Area Question', 10, ["Let's see a sample question."], [
        ('Area two ways', [
            "Triangle ABC is right at C. The sides are 15, 20 and 25. CD is the altitude to AB. What is CD?",
            "CD is a height. Heights live in area — so let's find the area in two ways.",
            D('Write S = 15 · 20 ÷ 2 = 150'),
            "Way one: the legs. AC and BC are perpendicular — a side and its height. 15 times 20, over 2: 150.",
            D('Write S = 25 · CD ÷ 2'),
            "Way two: the side AB, 25, and the height to it — that's CD.",
            D('Write 25 · CD ÷ 2 = 150 → 25 · CD = 300 → CD = 12'),
            "Same triangle, same area. 25 times CD is 300. CD is 12.",
            D('Circle choice 2'),
            "Choice two.",
        ]),
        ('The traps', [
            D('Next to choice 1 write 150 ÷ 25 — forgot × 2'),
            "6? Someone divided 150 by 25 and forgot to double the area first.",
            D('Next to choice 3 write 25 ÷ 2 = median'),
            "12.5? That's half the hypotenuse — the median to the hypotenuse, not the altitude. The altitude is shorter.",
            "The short rule for right triangles: leg times leg equals hypotenuse times altitude.",
            D('Write 15 · 20 = 25 · CD → CD = 300 ÷ 25 = 12'),
            "15 times 20 is 300. Divide by 25 — 12. One line.",
        ]),
    ])

    # --- new guided question B: largest possible area (after A) -------------------------------
    M.new_q(N[1], TOPIC, 'In triangle ABC:\n' r'$\begin{cases} AB=6' + C + r' \\ BC=8' + C + r' \end{cases}$'
            '\nWhich of the following could be the area of the triangle (in cm²)?',
            ['$25$', '$48$', '$20$', '$28$'], 3, [
                'Take BC $=8$ as the base. The height from A is a leg of a right triangle whose hypotenuse is AB $=6$, '
                'therefore the height is at most $6$.',
                'Area $\\le\\frac{8\\cdot6}{2}=24$ (exactly $24$ only when $\\angle B=90°$).',
                '$25$, $28$ and $48$ are more than $24$ — impossible. $20$ is possible.',
                'Trap: $48=6\\cdot8$ forgets to divide by $2$.'])
    M.place_q(N[1], L1, after='solve-' + N[0])
    _solution(M, N[1], 'Triangle Area Question', 10, ["Let's see one more."], [
        ('The height is at most 6', [
            "Two sides, 6 and 8. The angle between them is not given. Which could be the area?",
            "The area isn't fixed — it depends on the angle at B. So let's find the largest possible area.",
            D('Sketch BC = 8 on the floor, and AB = 6 leaning up from B'),
            "Put BC, 8, on the floor. The height is the distance from A down to the floor.",
            "That height is a leg of a right triangle, and AB is its hypotenuse. A leg is shorter than the hypotenuse.",
            "So the height is at most 6 — when AB stands straight up.",
            D('Write S ≤ 8 · 6 ÷ 2 = 24'),
            "The largest area: 8 times 6 over 2 — 24. Only with a right angle at B.",
            D('Cross out 25, 28 and 48'),
            "25, 28 and 48 are all above 24. Impossible.",
            D('Circle choice 3'),
            "20 is below 24 — possible. Choice three.",
        ]),
        ('The trap', [
            "48 is 6 times 8 — someone forgot to divide by 2.",
            "And the big trap: many students compute 24 and stop. But nobody said the angle is 90.",
            "Two sides and no angle? The area can be anything up to half their product.",
        ]),
    ], fig=False)

    # =========================================================================================
    # 4. Order fix: "Equilateral Triangle Area" + Q7 move after the 30°-60°-90° lesson (and Q12)
    # =========================================================================================
    M.move(V_EQ, L1, after='solve-geo31-g027')
    M.move('geo31-g018', L1, after=V_EQ)
    M.move('solve-geo31-g018', L1, after='geo31-g018')
    M.set_slide(V_EQ, 1, script=[
        "Let's see how we find the area of an equilateral triangle.",
        "Now that we know the golden triangle, it's quick.",
    ])
    M.set_slide(V_EQ, 2, title='Two golden halves', script=[
        A('Equilateral triangle ABC with the altitude CH appears', _vis_item(M, V_EQ, 2)),
        "We need a side times a height — so we drop an altitude.",
        D('Write a on the two slanted sides'),
        "Every side is a.",
        "In an equilateral triangle the altitude is also a median and an angle bisector. It cuts the triangle into two halves.",
        D('Write a/2 on AH, 60° at A and 30° at C'),
        "Each half has angles 30, 60 and 90 — a golden triangle.",
        "Its hypotenuse is a. The short leg, opposite the 30, is half of it: a over 2.",
        D('Write h = (a/2) · √3 on CH'),
        "The height is the long leg: the short leg times root 3.",
        A("'h = a√3/2' appears", T(r'$h=\dfrac a2\cdot\sqrt3=\dfrac{a\sqrt3}{2}$', size=50, x=410, y=650)),
        "a over 2, times root 3: a root 3 over 2.",
    ])
    M.set_slide(V_EQ, 3, title='Check with Pythagoras', script=[
        "Prefer Pythagoras? The same half-triangle: hypotenuse a, one leg a over 2.",
        A("'h² = a² − (a/2)²' appears", T(r'$h^2=a^2-\left(\dfrac{a}{2}\right)^2=a^2-\dfrac{a^2}{4}$', size=50)),
        "Hypotenuse squared minus leg squared. a over 2, squared, is a squared over 4 — the top and the bottom are both squared.",
        A("'h² = 3a²/4' appears", T(r'$h^2=\dfrac{3a^2}{4}$', size=50)),
        "a squared minus a quarter of a squared: three quarters of a squared.",
        A("'h = a√3/2' appears", T(r'$h=\dfrac{a\sqrt3}{2}$', size=56)),
        "Take the root: a root 3 over 2. The same height — the golden triangle just gets there faster.",
        D('Box the h'),
        "So far we've only found the height.",
    ])
    _draw(M, V_EQ, 4, 'Write : 2 : 2 = · ½ · ½ = : 4', 'Write ÷ 2 ÷ 2 = ÷ 4')
    _say(M, V_EQ, 4, "We have divide by 2 and divide by 2", "We divide by 2, and then by 2 again — that's dividing by 4.")
    _say(M, V_EQ, 4, "And we don't want to do the whole Pythagoras process every time",
         "And we don't want to find the height every time, and then the area. Remember the formula.")
    sc = _script(M, V_EQ, 5)
    sc = [A(x[1], dict(x[2], t=r'Side $8$: $\ \dfrac{8^2\sqrt3}{4}=\dfrac{64\sqrt3}{4}=16\sqrt3$'))
          if isinstance(x, tuple) and x[0] == 'A' and x[2]['t'].startswith('$a=8') else x for x in sc]
    sc += ["And the 30-30-120 triangle with legs a from the last lesson? The same area: a squared root 3 over 4."]
    M.set_slide(V_EQ, 5, script=sc)
    M.set_sidebar(V_EQ, ['Two golden halves', 'Check with Pythagoras', 'Area formula', 'a-two-three-four'])
    _say(M, V_3060, 10, "Look familiar? Same as an equilateral triangle with side a!",
         "Keep this formula in mind. In the next lesson you'll see it again — it's also the area of an equilateral triangle with side a.")
    _draw(M, V_3060, 7, 'write 9 : 3 = 3', 'write 9 ÷ 3 = 3')
    _draw(M, V_4545, 4, 'Write 16 : 2 = 8', 'Write 16 ÷ 2 = 8')
    c = M.card('mem-special-right')
    c['tables'][0]['rows'].append(['Equilateral (side \\(a\\))', 'height \\(\\dfrac{a\\sqrt3}{2}\\) · area \\(\\dfrac{a^2\\sqrt3}{4}\\)',
                                   'two golden halves · a-two-three-four'])
    c['tips'].append('Subtracting equilateral areas? Keep the denominator 4 until the end.')

    # =========================================================================================
    # 5. Pythagoras (geo-019): acute / right / obtuse from the sides + guided question
    # =========================================================================================
    M.insert_slides(V_PYT, 3, [dict(mode='concept', title='Acute or obtuse?', script=[
        "But first — one more use of the squares, even when there's no right-angle mark.",
        A("'c = the longest side' appears", T('$c$ = the longest side', size=46)),
        "Take the longest side, c. Compare c squared with a squared plus b squared.",
        A("'c² = a² + b² → right' appears", T(r'$c^2=a^2+b^2$ → right', size=46)),
        "Equal? A right triangle.",
        A("'c² > a² + b² → obtuse' appears", T(r'$c^2>a^2+b^2$ → obtuse', size=46)),
        "c squared bigger? The angle opposite c opens wider than 90 — obtuse.",
        A("'c² < a² + b² → acute' appears", T(r'$c^2<a^2+b^2$ → acute', size=46)),
        "Smaller? The angle opposite c is less than 90 — and so are the others. Acute.",
        D('Write 5, 5, 8: 8² = 64 > 5² + 5² = 50 → obtuse'),
        "Sides 5, 5 and 8: 8 squared is 64. 25 plus 25 is 50. 64 is bigger — obtuse.",
        "Think of a door: open the angle wider, and the side opposite it grows.",
        "Now the sample questions: the hypotenuse, a leg — and then this test.",
    ])])
    M.set_sidebar(V_PYT, ['The theorem', 'Right triangles only', 'Acute or obtuse?'])
    _lesson_actives(M, V_PYT)
    M.card('mem-pythagoras')['tables'][0]['rows'].append(
        ['Right, acute or obtuse?', 'compare the longest side squared with the other two squares',
         '\\(c^2=a^2+b^2\\) right · \\(>\\) obtuse · \\(<\\) acute'])
    _say(M, 'solve-geo31-g022', 3, "The next lesson is actually a proof of the theorem.",
         "Soon there's a lesson with a proof of the theorem. You don't have to watch it — but I warmly recommend it. It's beautiful.")

    M.new_q(N[2], TOPIC, 'In triangle ABC:\n' r'$\begin{cases} AB=6' + C + r' \\ BC=7' + C + r' \\ AC=10' + C + r' \end{cases}$'
            '\nWhich of the following is true?',
            ['The triangle is acute.', 'The triangle is right, with the right angle at B.',
             'The triangle is obtuse, with the obtuse angle at B.', 'The triangle is obtuse, with the obtuse angle at C.'], 3, [
                'The longest side is $AC=10$: $10^2=100$.',
                'The other two sides: $6^2+7^2=36+49=85$.',
                '$100>85$, therefore the angle opposite AC is obtuse. The angle opposite AC is the angle at B.'])
    M.place_q(N[2], L1, after='solve-geo31-g022')
    _solution(M, N[2], 'Pythagoras Questions', 15, ["Let's see one more question."], [
        ('Compare the squares', [
            "The sides are 6, 7 and 10. Acute, right or obtuse?",
            "No figure and no angles. Only sides. So we use the squares.",
            D('Circle 10 — the longest side'),
            "Step one: the longest side. 10 — that's AC.",
            D('Write 10² = 100 and 6² + 7² = 36 + 49 = 85'),
            "10 squared is 100. The other two: 36 plus 49 — 85.",
            D('Write 100 > 85 → obtuse'),
            "100 is bigger than 85. The longest side is too long for a right angle — the angle opposite it is obtuse.",
            "A right angle would need exactly 100.",
        ]),
        ('Which angle?', [
            "Which angle is obtuse? The one opposite the longest side.",
            D('Draw an arrow from AC across to B'),
            "AC doesn't touch B. So B is the angle opposite AC.",
            D('Circle choice 3'),
            "The obtuse angle is at B. Choice three.",
            "Choice four is the trap: C is an end of AC — it's next to the longest side, not opposite it.",
        ]),
    ], fig=False)

    # =========================================================================================
    # 6. Triples (geo-024): 8-15-17 is not "very, very rare" (Q8 uses it)
    # =========================================================================================
    M.set_slide(V_TRIP, 6, title='8-15-17: less common')
    _say(M, V_TRIP, 6, "Honestly — there's no real need for it.",
         "It's less common than the first two — but it does appear. Our first Pythagoras question was exactly 8, 15, 17.")
    _say(M, V_TRIP, 8, "8, 15, 17 — you really don't need to memorise.",
         "8, 15, 17 — good to recognize too. A trick: 8 times 2 is 16 — minus 1 is 15, plus 1 is 17.")
    _say(M, V_TRIP, 8, "But don't bother yourself with it.", None)
    _say(M, V_TRIP, 8, "Just remember 3, 4, 5",
         "Know 3, 4, 5 and hamsa, bat mitzvah, bar mitzvah by heart. And recognize 8, 15, 17 when you see it.")
    sb = M.video(V_TRIP)['hybrid']['sidebar']
    M.set_sidebar(V_TRIP, ['8-15-17: less common' if x.startswith('8-15-17') else x for x in sb])
    for r in M.card('mem-triples')['tables'][0]['rows']:
        if r[0].startswith('\\(8:15:17\\)'): r[0] = '\\(8:15:17\\) (less common)'

    # =========================================================================================
    # 7. Draw notes with ":" for division, Q17 ending
    # =========================================================================================
    _draw(M, 'solve-geo31-g015', 2, 'Write (180° − 24°) : 2 = 78°', 'Write (180° − 24°) ÷ 2 = 78°')
    _draw(M, 'solve-geo31-g025', 2, '24 (5:12:13 × 2)', '24 (5-12-13 × 2)')
    _draw(M, 'solve-geo31-g025', 2, '30 (3:4:5 × 6)', '30 (3-4-5 × 6)')
    _draw(M, 'solve-geo31-g028', 2, 'Write 14 : 2 = 7', 'Write 14 ÷ 2 = 7')
    _draw(M, 'solve-geo31-g038', 3, 'Write 1 : 3 → 8 and 24', 'Write area ratio 1 : 3 → 8 and 24')
    _say(M, 'solve-geo31-g034', 3, "Honestly, it's not very clear what to do with these numbers.",
         "It's not clear yet what to do with these numbers. So skip it — go to the next answer and hope to eliminate that one.")
    _add_lines(M, 'solve-geo31-g034', 3, [
        ('D', 'Sketch a side of 4 with its midpoint, and a slanted segment of 6 from the midpoint to a third vertex'),
        "Here's a quick sketch. A side of 4, and its midpoint. From the midpoint, a segment of 6 — leaning to the side.",
        "Its top is the third vertex. Join it to both ends: one side comes out short, the other long.",
        "A median of 6 to a side of 4 — and not isosceles. That's why it's the answer.",
    ])

    # =========================================================================================
    # 8. Question text: TeX, stacked givens, full solutions (every question of the topic)
    # =========================================================================================
    S('geo31-g010', stem='In triangle ABC, the marked angle outside the triangle is vertically opposite the interior angle '
      'at A. Based on this information and the information in the figure, what is the value of $x$?', expl=[
        'The marked angle $2x$ is vertically opposite the interior angle at A, therefore $\\angle A=2x$.',
        'Angle sum: $2x+3x+4x=180°$, that is $9x=180°$. Therefore $x=20°$.'])
    S('geo31-g011', expl=[
        'Call each of the equal angles at A and C $u$.',
        '$p$ is adjacent to the angle at A: $p=180°-u$.',
        '$q$ is an exterior angle at B. It equals the two interior angles not next to it: $q=u+u=2u$.',
        '$p+\\frac{q}{2}=(180°-u)+\\frac{2u}{2}=180°-u+u=180°$.'])
    S('geo31-g012', stem='In triangle ABC:\n' r'$\begin{cases} AC=7' + C + r' \\ BC=12' + C + r' \end{cases}$'
      '\nWhich of the following could be the length of AB (in cm)?', expl=[
        'A side is between the difference and the sum of the other two sides: $12-7<AB<12+7$, that is $5<AB<19$.',
        'Both signs are strict: $5$ and $19$ are not allowed, and $21$ is too long. Only $10$ fits.'])
    S('geo31-g014', stem='ABC is an equilateral triangle. Point D lies on BC.\nGiven:\n'
      r'$\begin{cases} \angle DAC=30° \\ DC=6' + C + r' \end{cases}$' '\nWhat is AB (in cm)?', expl=[
        'ABC is equilateral, therefore $\\angle BAC=60°$ and $\\angle BAD=60°-30°=30°$: AD bisects angle A.',
        'In an equilateral triangle the angle bisector is also a median: $BD=DC=6$.',
        '$AB=BC=6+6=12$.'])
    S('geo31-g015', stem='In triangle ABC, point D lies on AB.\nGiven:\n'
      r'$\begin{cases} AB=AC \\ \angle BAC=24° \\ BC=CD \end{cases}$' '\nWhat is $\\angle ACD$?', expl=[
        'ABC is isosceles: $\\angle B=\\angle ACB=\\frac{180°-24°}{2}=78°$.',
        'BCD is isosceles ($BC=CD$): $\\angle BDC=\\angle B=78°$, therefore $\\angle BCD=180°-78°-78°=24°$.',
        '$\\angle ACD=78°-24°=54°$.'])
    S('geo31-g017', expl=[
        'The lines are parallel, therefore both triangles have the same height $h$.',
        'Let $CD=x$. Then $DE=4x$.',
        '$\\dfrac{S_{BDE}}{S_{ACD}}=\\dfrac{\\frac{4x\\cdot h}{2}}{\\frac{x\\cdot h}{2}}=4$.',
        'Without calculating: same height, therefore the area ratio is the base ratio, $4$.'])
    S('geo31-g018', expl=[
        'Each side of ABC is $18\\div3=6$, therefore $BD=BE=3$.',
        'DBE has two sides of $3$ with a $60°$ angle between them. It is isosceles with a $60°$ vertex angle, therefore '
        'its base angles are $\\frac{180°-60°}{2}=60°$ too: it is equilateral with side $3$.',
        '$S_{ABC}=\\frac{6^2\\sqrt3}{4}=\\frac{36\\sqrt3}{4}$ and $S_{DBE}=\\frac{3^2\\sqrt3}{4}=\\frac{9\\sqrt3}{4}$.',
        '$S_{ADEC}=\\frac{36\\sqrt3}{4}-\\frac{9\\sqrt3}{4}=\\frac{27\\sqrt3}{4}$.'])
    S('geo31-g020', stem='Triangle ABC is a right triangle.\nGiven:\n'
      r'$\begin{cases} \angle ABC=90° \\ AB=8' + C + r' \\ BC=15' + C + r' \end{cases}$' '\nWhat is AC (in cm)?', expl=[
        'The right angle is at B, therefore AC is the hypotenuse — the longest side. $8$ and $15$ are out.',
        '$AC^2=8^2+15^2=64+225=289$, therefore $AC=\\sqrt{289}=17$.',
        'The trap $23=8+15$ breaks the triangle rule: a side is less than the sum of the other two.'])
    S('geo31-g021', stem='Triangle ABC is a right triangle.\nGiven:\n'
      r'$\begin{cases} \angle ABC=90° \\ AB=4' + C + r' \\ BC=7' + C + r' \end{cases}$' '\nWhat is AC (in cm)?', expl=[
        'AC is the hypotenuse: $AC^2=4^2+7^2=16+49=65$, therefore $AC=\\sqrt{65}$.',
        'Traps: $11=4+7$ adds the lengths, and $65$ forgets the root.'])
    S('geo31-g022', stem='Triangle ABC is a right triangle.\nGiven:\n'
      r'$\begin{cases} \angle ABC=90° \\ AB=8' + C + r' \\ AC=11' + C + r' \end{cases}$' '\nWhat is BC (in cm)?', expl=[
        'The right angle is at B, therefore $AC=11$ is the hypotenuse and BC is a leg.',
        '$BC^2=11^2-8^2=121-64=57$, therefore $BC=\\sqrt{57}$.',
        'Trap: $3=11-8$ subtracts the lengths, not the squares.'])
    S('geo31-g025', expl=[
        'ABC: $10=2\\cdot5$ and $26=2\\cdot13$, the triple 5-12-13 times $2$. Therefore $AC=2\\cdot12=24$.',
        'ACE: legs $18=6\\cdot3$ and $24=6\\cdot4$, the triple 3-4-5 times $6$. Therefore $CE=6\\cdot5=30$.',
        'CED: two legs of $30$. $CD^2=30^2+30^2=2\\cdot30^2$, therefore $CD=30\\sqrt2$.'])
    S('geo31-g027', stem='Triangle ABC is a right triangle.\nGiven:\n'
      r'$\begin{cases} \angle ABC=90° \\ \angle ACB=30° \\ AB=6' + C + r' \end{cases}$'
      '\nWhat is the perimeter of the triangle (in cm)?', expl=[
        '$\\angle C=30°$, therefore AB, opposite it, is the short leg: $a=6$.',
        'The hypotenuse: $AC=2a=12$. The long leg: $BC=a\\sqrt3=6\\sqrt3$.',
        'Perimeter $=6+12+6\\sqrt3=18+6\\sqrt3$.'])
    S('geo31-g028', stem='Triangle ABC is a right triangle.\nGiven:\n'
      r'$\begin{cases} \angle ABC=90° \\ \angle ACB=45° \\ AC=14' + C + r' \end{cases}$'
      '\nWhat is its perimeter (in cm)?', expl=[
        '$\\angle C=45°$, therefore $\\angle A=45°$ too: a 45°-45°-90° triangle with hypotenuse $AC=14$.',
        'Each leg: $\\frac{14}{\\sqrt2}=7\\sqrt2$.',
        'Perimeter $=7\\sqrt2+7\\sqrt2+14=14+14\\sqrt2$.'])
    # --- further guided examples
    S('geo31-g031', expl=[
        'Triangle ABE: $\\angle B=60°$ (equilateral), $\\angle BAE=q$ (vertically opposite), $\\angle AEB=180°-p$ (adjacent).',
        'Angle sum: $60°+q+(180°-p)=180°$, therefore $q=p-60°$.',
        'Faster: $p$ is an exterior angle of ABE, therefore $p=60°+q$.',
        'Plug in: $p=100°$ gives $q=40°$. Only $p-60°$ gives $40°$.'])
    S('geo31-g032', expl=[
        '$\\alpha+\\beta=180°-40°=140°$. Since $\\alpha>\\beta$: $\\alpha>70°$ and $\\beta<70°$.',
        'Therefore $\\alpha$ is the largest angle: larger than $\\beta$ and larger than $40°$.',
        'The longest side is opposite the largest angle: BC.'])
    S('geo31-g033', expl=[
        'Minimum: $AC+BC>AB=6$, therefore the perimeter is more than $6+6=12$.',
        'Maximum: $\\angle C>90°$ is the largest angle, therefore AB is the longest side: $AC<6$ and $BC<6$. '
        'The perimeter is less than $6+6+6=18$.',
        'Only $13.5$ is between $12$ and $18$.',
        'Example: sides $3.75,\\ 3.75,\\ 6$. The obtuse test: $6^2=36>3.75^2+3.75^2=28.125$, therefore the angle opposite AB is obtuse.'])
    S('geo31-g034', expl=[
        'Choice 2: the third angle is $180°-76°-52°=52°$. Two equal angles, therefore two equal sides: isosceles.',
        'Choice 3: an altitude that also bisects its angle is a symmetry line: isosceles.',
        'Choice 4: a median that is perpendicular to its side is a symmetry line: isosceles.',
        'Choice 1: a median of $6$ to a side of $4$ can lean to one side. Then the other two sides are different: '
        'not necessarily isosceles.'])
    S('geo31-g035', stem='In the accompanying figure, triangles ABC and ACD are right triangles. The marked lengths are in '
      'cm. What is the area of quadrilateral ABCD (in cm²)?', expl=[
        'ABC: legs $6$ and $8$, the triple 3-4-5 times $2$. Therefore $AC=10$.',
        'ACD: leg $10$ and hypotenuse $26$, the triple 5-12-13 times $2$. Therefore $CD=24$.',
        'Area $=\\frac{6\\cdot8}{2}+\\frac{10\\cdot24}{2}=24+120=144$.'])
    S('geo31-g036', expl=[
        'ABD: $\\angle A=30°$ and $\\angle B=90°$, hypotenuse $AD=12$. Short leg $BD=\\frac{12}{2}=6$, long leg $AB=6\\sqrt3$.',
        'BCD: a 45°-45°-90° triangle with hypotenuse $BD=6$. Each leg: $BC=CD=\\frac{6}{\\sqrt2}=3\\sqrt2$.',
        'Perimeter (outside sides only): $12+6\\sqrt3+3\\sqrt2+3\\sqrt2=12+6\\sqrt3+6\\sqrt2$.'])
    S('geo31-g037', stem='In triangle ABC, AE is the altitude to BC. Point D lies on AE, and DBC is an equilateral '
      'triangle.\nGiven:\n' r'$\begin{cases} BE=3' + C + r' \\ AD=2\sqrt3' + C + r' \end{cases}$'
      '\nWhat is the shaded area (in cm²)?', expl=[
        'DE is the altitude of the equilateral triangle DBC, therefore it is also a median: $EC=BE=3$ and $BC=6$.',
        'DEC is a 30°-60°-90° triangle with short leg $EC=3$: $DE=3\\sqrt3$. Therefore $AE=3\\sqrt3+2\\sqrt3=5\\sqrt3$.',
        '$S_{ABC}=\\frac{6\\cdot5\\sqrt3}{2}=15\\sqrt3$ and $S_{DBC}=\\frac{6\\cdot3\\sqrt3}{2}=9\\sqrt3$.',
        'Shaded area $=15\\sqrt3-9\\sqrt3=6\\sqrt3$.'])
    S('geo31-g038', expl=[
        'ABD and ADC have the same height from A. Therefore their areas are in the ratio of their bases, 1 to 3.',
        'Four equal parts: $32\\div4=8$. $S_{ABD}=8$ and $S_{ADC}=3\\cdot8=24$.',
        'Difference: $24-8=16$.'])
    S('geo31-g039', expl=[
        'AE is made of two diagonals of small squares: $AE=3\\sqrt2+3\\sqrt2=6\\sqrt2$. $AG=3+3=6$.',
        'AF is in both triangles, and $EF=FG=3$. These cancel in the difference.',
        '$P_{AEF}-P_{AFG}=AE-AG=6\\sqrt2-6$.',
        'Full calculation: $AF=\\sqrt{6^2+3^2}=\\sqrt{45}=3\\sqrt5$, $P_{AEF}=6\\sqrt2+3+3\\sqrt5$, $P_{AFG}=6+3+3\\sqrt5$.'])
    S('geo31-g040', expl=[
        'The bold line: $b+b+(b-a)=3b-a$.',
        'Twice the small perimeter: $2\\cdot3a=6a$.',
        '$3b-a=6a$, therefore $3b=7a$ and $\\frac ab=\\frac37$.',
        'Check: $a=3$, $b=7$: $21-3=18=2\\cdot9$ ✓.'])

    # --- foundation practice
    S('geo31-foundation-p01', stem='ABC is isosceles, with $AC=BC$. Based on this information and the information in the '
      'figure, what is the value of $x$?', expl=[
        'The interior angle at A is adjacent to $146°$: $\\angle A=180°-146°=34°$.',
        '$AC=BC$, therefore the angles opposite them are equal: $\\angle B=\\angle A=34°$.',
        '$x=180°-34°-34°=112°$.'])
    S('geo31-foundation-p02', stem='The marked lengths in triangle ABC are in cm. Which of the following is necessarily true?',
      expl=['The sides opposite $\\beta$, $\\alpha$ and $\\gamma$ are $8$, $10$ and $13$.',
            'The longer the side, the larger the angle opposite it: $\\beta<\\alpha<\\gamma$.'])
    S('geo31-foundation-p03', stem='Triangle ADC is equilateral, and B, D and C lie on one line in that order.\nGiven:\n'
      r'$\begin{cases} BD=7' + C + r' \\ \angle BAD=30° \end{cases}$' '\nWhat is DC (in cm)?', expl=[
        '$\\angle ADC=60°$ (equilateral). It is an exterior angle of ABD: $60°=30°+\\angle ABD$, therefore $\\angle ABD=30°$.',
        'Two equal angles ($30°$ at A and at B), therefore the sides opposite them are equal: $AD=BD=7$.',
        'ADC is equilateral, therefore $DC=AD=7$.'])
    S('geo31-foundation-p04', expl=[
        'The third side is between the difference and the sum: $11-8<x<11+8$, that is $3<x<19$.',
        '$3$ is not allowed (strict sign). $7$, $12$ and $18$ are all inside.'])
    S('geo31-foundation-p05', expl=[
        '$AB=BC$, therefore $\\angle A=\\angle C=\\frac{180°-42°}{2}=69°$.',
        'Alternate angles between the parallel lines: $y=\\angle C=69°$.'])
    S('geo31-foundation-p06', stem='Triangle ABC is right at B.\nGiven:\n'
      r'$\begin{cases} AC=25' + C + r' \\ BC=20' + C + r' \end{cases}$' '\nWhat is its area (in cm²)?', expl=[
        '$20=5\\cdot4$ and $25=5\\cdot5$: the triple 3-4-5 times $5$. Therefore $AB=5\\cdot3=15$.',
        'Area $=\\frac{15\\cdot20}{2}=150$.',
        'Check: $AB^2=25^2-20^2=625-400=225$, $AB=15$ ✓.'])
    S('geo31-foundation-p07', stem='In triangle ABC:\n'
      r'$\begin{cases} \angle A=35° \\ \angle B=85° \\ AB=12' + C + r' \end{cases}$'
      '\nWhich of the following is necessarily true?', expl=[
        '$\\angle C=180°-35°-85°=60°$ (not $70°$).',
        'Order the angles: $\\angle A<\\angle C<\\angle B$. The sides opposite them: $BC<AB<AC$.',
        '$AB=12$, therefore $AC>12$.'])
    S('geo31-foundation-p08', stem='In triangle ABC, CD bisects angle C and meets AB at D.\nGiven:\n'
      r'$\begin{cases} AC=BC=10' + C + r' \\ \angle A=60° \end{cases}$' '\nWhat is DB (in cm)?', expl=[
        '$AC=BC$, therefore $\\angle B=\\angle A=60°$ and $\\angle C=180°-60°-60°=60°$. The triangle is equilateral: $AB=10$.',
        'The angle bisector CD is also a median: $DB=\\frac{10}{2}=5$.'])
    S('geo31-foundation-p09', stem='In the accompanying figure, $AD\\perp BC$.\nGiven:\n'
      r'$\begin{cases} AB=13' + C + r' \\ BD=5' + C + r' \\ AC=\sqrt{313}' + C + r' \end{cases}$'
      '\nWhat is DC (in cm)?', expl=[
        'ABD is right at D, with $BD=5$ and $AB=13$: the triple 5-12-13. Therefore $AD=12$.',
        'ADC: $DC^2=AC^2-AD^2=313-144=169$, therefore $DC=13$.'])
    S('geo31-foundation-p10', expl=['A median splits a triangle into two triangles of equal area: $S_{ACD}=\\frac{30}{2}=15$.'])
    S('geo31-foundation-p11', expl=[
        'The angles next to the two marked $120°$ angles are $180°-120°=60°$: $\\angle BDE=60°$ and $\\angle ACB=60°$.',
        '$DE\\parallel AC$, therefore $\\angle DEB=\\angle ACB=60°$ (corresponding angles). BDE has two $60°$ angles, '
        'therefore it is equilateral with side $6$.',
        'Area $=\\frac{6^2\\sqrt3}{4}=\\frac{36\\sqrt3}{4}=9\\sqrt3$.'])
    S('geo31-foundation-p12', stem='In triangle ABC:\n'
      r'$\begin{cases} AB=26' + C + r' \\ AC=19' + C + r' \end{cases}$' '\nWhich of the following is necessarily true?', expl=[
        'The third side is between the difference and the sum: $26-19<BC<26+19$, that is $7<BC<45$.',
        'Therefore $BC>7$ is always true.',
        'BC can be less than $19$ or more than $26$, therefore choices 1 and 2 are not necessarily true. Angle A is opposite '
        'BC, and BC need not be the longest side.'])
    S('geo31-foundation-p13', expl=[
        'In ABD: $\\angle BAD=180°-90°-52°=38°$.',
        'AC bisects it: $\\angle BAC=\\frac{38°}{2}=19°$.',
        'In ABC: $\\beta=180°-90°-19°=71°$.'])
    S('geo31-foundation-p14', expl=[
        'The angles of the triangle: $90°$, $2\\alpha$ and the other acute angle.',
        'The exterior angle next to the other acute angle equals the two interior angles not next to it: $90°+2\\alpha$.'])
    S('geo31-foundation-p15', expl=[
        'The two acute angles of a right triangle add up to $90°$. Together they are $1+5=6$ angles of $x$.',
        '$6x=90°$, therefore $x=15°$.'])
    S('geo31-foundation-p16', expl=[
        '$\\angle P=180°-u$ and $\\angle Q=180°-v$. Since $u>v$: $\\angle P<\\angle Q$.',
        'The side opposite P is QR, and the side opposite Q is PR. The smaller angle is opposite the shorter side: $QR<PR$.'])
    S('geo31-foundation-p17', stem='In the accompanying figure:\n'
      r'$\begin{cases} AB=AC \\ AD\perp BC \\ AE=EC \\ \angle BAD=24° \end{cases}$' '\nWhat is x?', expl=[
        'AD is the altitude to the base of the isosceles triangle ABC, therefore it also bisects angle A: $\\angle EAC=24°$.',
        '$AE=EC$, therefore $\\angle ECA=\\angle EAC=24°$.',
        '$x$ is an exterior angle of triangle AEC: $x=24°+24°=48°$.'])
    S('geo31-foundation-p18', expl=[
        'The two angles at O are vertically opposite, therefore equal. Call each one $\\theta$.',
        'Angle sums: $\\begin{cases} \\alpha+48°+\\theta=180° \\\\ \\beta+76°+\\theta=180° \\end{cases}$ '
        'Therefore $\\alpha+48°=\\beta+76°$.',
        '$\\beta=\\alpha+48°-76°=\\alpha-28°$.'])
    S('geo31-foundation-p19', expl=[
        'The $136°$ angle moves to the left parallel line as a corresponding angle. There it is an exterior angle of the triangle.',
        'The exterior angle equals the two interior angles not next to it: $\\alpha+24°=136°$, therefore $\\alpha=112°$.'])
    S('geo31-foundation-p20', stem='In the accompanying figure, line $\\ell$ is parallel to BC. The extension of side AC '
      'meets $\\ell$ at E. Which expression equals $r$?', expl=[
        'The interior angle at B is adjacent to $q$: $\\angle B=180°-q$.',
        'The exterior angle at C equals the two interior angles not next to it: $p+(180°-q)$.',
        '$\\ell\\parallel BC$, therefore $r$ equals this exterior angle (corresponding angles): $r=180°-q+p$.',
        'Check with numbers: $p=70°$ and $q=120°$ give $\\angle B=60°$ and $\\angle C=50°$. The exterior angle at C is '
        '$130°=180°-120°+70°$ ✓.'], figure=fig_p20())
    S('geo31-foundation-p21', expl=[
        'Let each equal side be $x$. The base is $x-6$.',
        '$x+x+(x-6)=38$, therefore $3x=44$ and $x=\\frac{44}{3}$.',
        'Base $=\\frac{44}{3}-6=\\frac{44-18}{3}=\\frac{26}{3}$.'])
    S('geo31-foundation-p22', expl=[
        '$14-9<x<14+9$, that is $5<x<23$.',
        'Whole numbers from $6$ to $22$: $22-6+1=17$.',
        'Shortcut: twice the shorter side, minus 1: $2\\cdot9-1=17$.'])
    S('geo31-foundation-p23', expl=['$\\frac{15h}{2}=45$, therefore $15h=90$ and $h=6$.'])
    S('geo31-foundation-p24', expl=[
        'The hypotenuse is $29$. The other leg: $b^2=29^2-20^2=841-400=441$, therefore $b=21$.',
        'Area $=\\frac{20\\cdot21}{2}=210$.'])
    S('geo31-foundation-p25', expl=[
        '$\\frac{a^2\\sqrt3}{4}=25\\sqrt3$, therefore $a^2=100$ and $a=10$.',
        'Perimeter $=3\\cdot10=30$.'])
    S('geo31-foundation-p27', expl=[
        'Each leg is $t$ and the hypotenuse is $t\\sqrt2$: $P=2t+t\\sqrt2=t(2+\\sqrt2)$.',
        '$16+8\\sqrt2=8(2+\\sqrt2)$, therefore $t=8$.',
        'Area $=\\frac{8\\cdot8}{2}=32$.'])

    # --- advanced practice
    S('geo31-advanced-p01', choices=[
        'A triangle in which an altitude also bisects the angle at its starting vertex', 'A triangle with two angles of $60°$',
        'An isosceles triangle with one angle of $60°$', 'An isosceles triangle whose base is twice half of an equal side'],
      correct=1, expl=[
        'An altitude that also bisects its starting angle makes the triangle isosceles. It does not force the base to equal the '
        'other two sides.',
        'Example: a triangle with sides $5,\\ 5,\\ 6$ has this symmetry line, but it is not equilateral.'])
    M.new_q(N[11], TOPIC, 'Which of the following triangles is not necessarily equilateral?',
            ['A triangle with two angles of $60°$', 'A triangle in which one median is also an altitude',
             'An isosceles triangle with one angle of $60°$', 'A triangle in which two different medians are also altitudes'], 2, [
        'Choice 1: the third angle is $180°-60°-60°=60°$: equilateral.',
        'Choice 3: a $60°$ vertex angle gives base angles of $\\frac{180°-60°}{2}=60°$; $60°$ base angles give a third angle of $60°$: equilateral.',
        'Choice 4: each such median is a symmetry line, therefore two pairs of sides are equal: all three sides are equal.',
        'Choice 2: one symmetry line makes the triangle only isosceles. Example: sides $5,\\ 5,\\ 6$ — not equilateral.'])
    M.place_q(N[11], ADV)
    S('geo31-advanced-p02', expl=[
        'ABC: legs $4$ and $4$, therefore $AC=4\\sqrt2$.',
        'ACD is equilateral: $AD=CD=AC=4\\sqrt2$.',
        'Perimeter (outside sides only): $4+4+4\\sqrt2+4\\sqrt2=8+8\\sqrt2$. AC is inside and is not counted.'])
    S('geo31-advanced-p03', expl=[
        'Let the base be $1$. Each equal side is $4$, and the perimeter is $1+4+4=9$.',
        '$\\frac{\\text{perimeter}}{\\text{equal side}}=\\frac94$.'])
    S('geo31-advanced-p04', stem='Triangles ABC and ACD are right at B and at C, respectively, and they have equal areas.'
      '\nGiven:\n' r'$\begin{cases} AB=9' + C + r' \\ BC=12' + C + r' \end{cases}$' '\nWhat is CD (in cm)?', expl=[
        'ABC: $9=3\\cdot3$ and $12=3\\cdot4$, the triple 3-4-5 times $3$. Therefore $AC=15$.',
        '$S_{ABC}=\\frac{9\\cdot12}{2}=54$.',
        'ACD is right at C, with legs AC and CD: $\\frac{15\\cdot CD}{2}=54$, therefore $CD=\\frac{108}{15}=\\frac{36}{5}$.'])
    S('geo31-advanced-p05', stem='At each vertex of a triangle, take the reflex angle outside the triangle (the reflex angle '
      '$=360°$ minus the interior angle). What is the average of these three reflex angles?', expl=[
        'Sum: $(360°-\\alpha)+(360°-\\beta)+(360°-\\gamma)=1080°-180°=900°$.',
        'Average: $\\frac{900°}{3}=300°$.',
        'Plug in: an equilateral triangle gives $360°-60°=300°$ at each vertex.'])
    S('geo31-advanced-p06', expl=[
        '$7$ is the longest side, therefore $x<7$.',
        'Triangle rule: $2+x>7$, therefore $x>5$.',
        'Only $6.5$ is between $5$ and $7$.'])
    S('geo31-advanced-p07', stem='In triangle ABC, BD bisects angle B and meets AC at D.\nGiven:\n'
      r'$\begin{cases} AB=AC \\ AD=DB \end{cases}$' '\nWhat is angle B?', expl=[
        'Let each half of angle B be $x$: $\\angle ABD=\\angle DBC=x$.',
        '$AD=DB$, therefore $\\angle A=\\angle ABD=x$.',
        '$AB=AC$, therefore $\\angle C=\\angle B=2x$.',
        'Angle sum: $x+2x+2x=180°$, therefore $x=36°$ and $\\angle B=72°$.'])
    S('geo31-advanced-p08', stem='AD is an altitude in triangle ABC, with D on BC. Given: $BD=\\frac34BC$. The area of ADC '
      'is 14 cm². What is the area of ABD (in cm²)?', expl=[
        '$BD=\\frac34BC$, therefore $DC=\\frac14BC$ and $BD=3\\cdot DC$.',
        'ABD and ADC have the same height AD. Therefore $S_{ABD}=3\\cdot S_{ADC}=3\\cdot14=42$.'])
    S('geo31-advanced-p09', expl=[
        'Angle ACD is an exterior angle of the triangle: $\\angle ACD=\\angle A+35°$.',
        '$\\angle A>45°$, therefore $\\angle ACD>80°$. $75°$ is impossible.',
        'The other choices work: $95°$, $115°$ and $135°$ give $\\angle A=60°$, $80°$ and $100°$.'])
    S('geo31-advanced-p10', stem='Triangle ABC is right at C, and D is the midpoint of BC.\nGiven:\n'
      r'$\begin{cases} AC=12' + C + r' \\ BC=16' + C + r' \end{cases}$'
      '\nWhich statement compares triangles ADC and ADB correctly?', expl=[
        'AD is a median, therefore $S_{ADC}=S_{ADB}$.',
        'Perimeters: both have AD, and $DC=DB=8$. Only AC and AB are different.',
        '$AB=20$ (the triple 3-4-5 times $4$) and $AC=12$. Therefore ADC has the smaller perimeter.'])
    S('geo31-advanced-p11', expl=[
        '$2x+4x+6x=180°$, therefore $x=15°$: the angles are $30°$, $60°$ and $90°$.',
        'A 30°-60°-90° triangle has sides $a,\\ a\\sqrt3,\\ 2a$. With $a=5$: $5,\\ 5\\sqrt3,\\ 10$.'])
    S('geo31-advanced-p12', stem='A, E and B lie on one line in that order; D, E and C lie on another. The marked angles '
      'at A and C are right angles.\nGiven:\n' r'$\begin{cases} BC=2 \\ CE=2\sqrt3 \\ AD=4\sqrt3 \end{cases}$'
      '\nWhat is AB?', expl=[
        'EBC is right at C, with legs $BC=2$ and $CE=2\\sqrt3$: the ratio $a,\\ a\\sqrt3$ with $a=2$. It is a 30°-60°-90° '
        'triangle: $EB=2\\cdot2=4$, and $\\angle BEC=30°$ (opposite the short leg BC).',
        'Vertically opposite angles: $\\angle AED=30°$.',
        'AED is right at A. $AD=4\\sqrt3$ is opposite the $30°$ angle, therefore it is the short leg. '
        'The long leg: $AE=4\\sqrt3\\cdot\\sqrt3=12$.',
        '$AB=AE+EB=12+4=16$.'])
    S('geo31-advanced-p13', stem='In the accompanying figure, $AD\\perp BC$.\nGiven:\n'
      r'$\begin{cases} AB=13 \\ BD=12 \\ AC=\sqrt{61} \end{cases}$' '\nWhat is BC?', expl=[
        'ABD: $AB=13$ and $BD=12$, the triple 5-12-13. Therefore $AD=5$.',
        'ADC: $DC^2=61-25=36$, therefore $DC=6$.',
        '$BC=BD+DC=12+6=18$.'])
    S('geo31-advanced-p14', expl=[
        'The altitude to the base makes two right triangles. In each one, an equal side is the hypotenuse and the altitude '
        'is a leg. The hypotenuse is the longest side, therefore the altitude is shorter than an equal side.',
        'The others are not always true. Sides $5,\\ 5,\\ 8$: the equal sides are shorter than the base, and the triangle '
        'is obtuse ($8^2=64>5^2+5^2=50$). Only the altitude to the base is also a bisector.'])
    S('geo31-advanced-p15', expl=[
        '$\\angle ACD+\\angle DCB=180°$. Their halves: $\\angle ECD+\\angle DCF=90°$, therefore $\\angle ECF=90°$.',
        'Triangle ECF: $\\angle EFC=180°-90°-2t=90°-2t$.'])
    S('geo31-advanced-p16', stem='Two angles of a triangle are $\\alpha$ and $\\beta$. At the third vertex, the reflex angle '
      'outside the triangle (the reflex angle $=360°$ minus the interior angle) is divided into three equal angles, each '
      'measuring $\\delta$. Which expression equals $\\delta$?', expl=[
        'The third angle: $180°-\\alpha-\\beta$.',
        'The reflex angle: $360°-(180°-\\alpha-\\beta)=180°+\\alpha+\\beta$.',
        '$\\delta=\\frac{180°+\\alpha+\\beta}{3}=60°+\\frac{\\alpha+\\beta}{3}$.'])
    S('geo31-advanced-p17', stem='Triangle ABC is right at A, and AD is the altitude to BC.\nGiven:\n'
      r'$\begin{cases} AB=8' + C + r' \\ AC=15' + C + r' \end{cases}$' '\nWhat is AD (in cm)?', expl=[
        '$BC=17$: the triple 8-15-17, or $\\sqrt{64+225}=\\sqrt{289}$.',
        'Area two ways: $\\frac{8\\cdot15}{2}=\\frac{17\\cdot AD}{2}$, therefore $17\\cdot AD=120$ and $AD=\\frac{120}{17}$.'])
    S('geo31-advanced-p18', expl=[
        'Triangle rule: the other two sides together are more than $8$.',
        'The obtuse angle is the largest angle, therefore $8$ is the longest side. Each other side is less than $8$, '
        'and their sum is less than $16$.',
        'Only $10$ is between $8$ and $16$. Example: $5,\\ 5,\\ 8$. The obtuse test: $8^2=64>5^2+5^2=50$ ✓.'])
    S('geo31-advanced-p19', expl=[
        'Angle sums: $\\begin{cases} 2p+q+42°=180° \\\\ p+2q+66°=180° \\end{cases}$, that is '
        '$\\begin{cases} 2p+q=138° \\\\ p+2q=114° \\end{cases}$',
        'Add the two equations: $3p+3q=252°$, therefore $p+q=84°$.'])
    S('geo31-advanced-p20', stem='In the accompanying figure, AD bisects angle BAC.\nGiven:\n'
      r'$\begin{cases} AC=BC \\ AB\parallel CD \\ \angle ACB=2t \end{cases}$' '\nWhich expression equals x?', expl=[
        '$AC=BC$, therefore $\\angle BAC=\\angle ABC=\\frac{180°-2t}{2}=90°-t$.',
        'AD bisects angle A: $\\angle BAD=\\frac{90°-t}{2}=45°-\\frac t2$.',
        'Alternate angles ($AB\\parallel CD$): $x=\\angle BAD=45°-\\frac t2$.'])
    S('geo31-advanced-p21', expl=[
        'The legs: $a+b=60-26=34$ and $a^2+b^2=26^2=676$.',
        'Fast way — spot the triple: $26=2\\cdot13$. Try 5-12-13 times $2$: $10,\\ 24,\\ 26$. Indeed $10+24=34$ ✓. '
        'Area $=\\frac{10\\cdot24}{2}=120$.',
        'Algebra: $(a+b)^2=a^2+2ab+b^2$: $34^2=1156=676+2ab$, therefore $2ab=480$ and the area is $\\frac{ab}{2}=120$.'])
    S('geo31-advanced-p22', expl=[
        'The common perimeter: $3\\cdot8=24$. With leg $x$, the hypotenuse is $x\\sqrt2$: $x(2+\\sqrt2)=24$.',
        'Work back from the choices: $12(2-\\sqrt2)\\cdot(2+\\sqrt2)=12(4-2)=24$ ✓.',
        'Algebra: $x=\\frac{24}{2+\\sqrt2}=\\frac{24(2-\\sqrt2)}{(2+\\sqrt2)(2-\\sqrt2)}=\\frac{24(2-\\sqrt2)}{2}=12(2-\\sqrt2)$.'])
    S('geo31-advanced-p23', stem='In triangle ABC, D lies on BC, and the ratio $BD:DC$ is $2:5$. E is the midpoint of AD. '
      'What is the ratio of the area of EBD to the area of ABC?', expl=[
        'ABD and ABC have the same height from A: $\\frac{S_{ABD}}{S_{ABC}}=\\frac{BD}{BC}=\\frac27$.',
        'E is the midpoint of AD, therefore E is half as high above BC as A: '
        '$S_{EBD}=\\frac12S_{ABD}=\\frac12\\cdot\\frac27S_{ABC}=\\frac17S_{ABC}$.'])
    S('geo31-advanced-p24', expl=[
        'Triangle rule: $10-6<x<10+6$, that is $4<x<16$.',
        '$10$ must be the only longest side: $x<10$.',
        'Whole numbers: $5, 6, 7, 8, 9$ — five values.'])
    S('geo31-advanced-p25', expl=[
        'The altitude to the base is also a median: it cuts the base $12$ into $6$ and $6$.',
        'Each half is a right triangle with hypotenuse $10$ and leg $6$ (the triple 3-4-5 times $2$), therefore the altitude is $8$.',
        'Area $=\\frac{12\\cdot8}{2}=48$.'])
    S('geo31-advanced-p26', expl=[
        'Sides $a,\\ a\\sqrt3,\\ 2a$. The hypotenuse minus the short leg: $2a-a=a$, therefore $a=7$.',
        'Legs $7$ and $7\\sqrt3$. Area $=\\frac{7\\cdot7\\sqrt3}{2}=\\frac{49\\sqrt3}{2}$.'])
    S('geo31-advanced-p27', expl=[
        'The triangles are on opposite sides of the base, therefore they do not overlap.',
        'Areas: $\\frac{14\\cdot5}{2}+\\frac{14\\cdot9}{2}=35+63=98$.',
        'Or at once: $\\frac{14\\cdot(5+9)}{2}=98$.'])

    # =========================================================================================
    # 9. Figures
    # =========================================================================================
    def p11(svg):   # "120°" sat on the letter D ("12D"): D to the right of the point, the angle label further left
        svg = svg.replace('<text x="240.600" y="183.915"', '<text x="283.000" y="188.000"')
        return svg.replace('<text x="231.037" y="185.915"', '<text x="218.000" y="186.000"')
    _edit_q_svg(M, 'geo31-foundation-p11', p11)

    def p10(svg):   # equal ticks on CD and DB: bolder and longer
        for x in ('393.000', '247.000'):
            svg = svg.replace('<line x1="%s" y1="291.690" x2="%s" y2="287.310" stroke="#087f83" stroke-width="1.8"/>' % (x, x),
                              '<line x1="%s" y1="297.500" x2="%s" y2="281.500" stroke="#087f83" stroke-width="2.6"/>' % (x, x))
        return svg
    _edit_q_svg(M, 'geo31-advanced-p10', p10)

    def g036(svg):  # "30°" and "45°" sat on the lines: bigger arcs, labels inside the angles
        svg = svg.replace('<path d="M 268.471 85.662 A 24.047 24.047 0 0 0 280.494 82.440"',
                          '<path d="M 268.471 106.615 A 45 45 0 0 0 290.971 100.586"')
        svg = svg.replace('<text x="276.562" y="91.811"', '<text x="286.000" y="126.000"')
        svg = svg.replace('<path d="M 280.616 252.263 A 17.176 17.176 0 0 0 285.647 240.118"',
                          '<path d="M 284.027 255.674 A 22 22 0 0 0 290.471 240.118"')
        return svg.replace('<text x="291.005" y="249.452"', '<text x="314.000" y="253.000"')
    _edit_q_svg(M, 'geo31-g036', g036)

    # =========================================================================================
    # 10. Practice: new questions, one duplicate out, easy -> hard
    # =========================================================================================
    # Pass 2: geo31-foundation-p26 stays (original question) - text clean-up only
    S('geo31-foundation-p26', expl=[
        'The median bisects the base, and the two small triangles share the same height, therefore their areas are equal.',
        'The original triangle: $19+19=38$.'])

    # acute test (foundation)
    M.new_q(N[3], TOPIC, 'Which of the following could be the side lengths of an acute triangle (in cm)?',
            ['$3,\\ 4,\\ 6$', '$5,\\ 12,\\ 13$', '$6,\\ 7,\\ 9$', '$2,\\ 3,\\ 6$'], 3, [
                'Compare the longest side squared with the sum of the other two squares.',
                '$3, 4, 6$: $36>9+16=25$ — obtuse. $5, 12, 13$: $169=25+144$ — right.',
                '$6, 7, 9$: $81<36+49=85$ — acute ✓.',
                '$2, 3, 6$: $2+3<6$ — not a triangle at all.'])
    M.place_q(N[3], FOUND)
    # largest area (foundation) - replaces the removed median question
    M.new_q(N[4], TOPIC, 'Two sides of a triangle are 10 cm and 7 cm long. What is the largest possible area of the '
            'triangle (in cm²)?', ['$70$', '$17.5$', '$35$', '$24.5$'], 3, [
                'Put the side $10$ on the floor. The height is at most $7$ (the side $7$ standing straight up).',
                'Largest area $=\\frac{10\\cdot7}{2}=35$, with a right angle between the two sides.',
                'Trap: $70=10\\cdot7$ forgets to divide by $2$.'])
    M.place_q(N[4], FOUND)
    # 30-30-120 (foundation)
    M.new_q(N[5], TOPIC, 'In triangle ABC:\n' r'$\begin{cases} AB=AC=10' + C + r' \\ \angle BAC=120° \end{cases}$'
            '\nWhat is the area of the triangle (in cm²)?', ['$50$', '$25\\sqrt3$', '$50\\sqrt3$', '$25$'], 2, [
                'The base angles: $\\frac{180°-120°}{2}=30°$. The altitude from A cuts the triangle into two 30°-60°-90° '
                'triangles with hypotenuse $10$.',
                'Height (opposite $30°$) $=\\frac{10}{2}=5$. Half the base $=5\\sqrt3$, therefore $BC=10\\sqrt3$.',
                'Area $=\\frac{10\\sqrt3\\cdot5}{2}=25\\sqrt3$ — the same as $\\frac{a^2\\sqrt3}{4}$ with $a=10$.'])
    M.place_q(N[5], FOUND)
    # obtuse range (advanced)
    M.new_q(N[6], TOPIC, 'In triangle ABC, angle B is obtuse.\nGiven:\n'
            r'$\begin{cases} AB=8' + C + r' \\ BC=15' + C + r' \end{cases}$' '\nWhich of the following could be AC (in cm)?',
            ['$16$', '$17$', '$20$', '$23$'], 3, [
                'Angle B is obtuse, therefore AC (opposite B) satisfies $AC^2>8^2+15^2=289$, that is $AC>17$.',
                'Triangle rule: $AC<8+15=23$.',
                'Only $20$ is between $17$ and $23$. ($17$ gives a right angle at B.)'])
    M.place_q(N[6], ADV)
    # area forces a right angle (advanced)
    M.new_q(N[7], TOPIC, 'In triangle ABC:\n' r'$\begin{cases} AB=5' + C + r' \\ AC=8' + C + r' \end{cases}$'
            '\nThe area of the triangle is 20 cm². What is angle A?', ['$30°$', '$45°$', '$60°$', '$90°$'], 4, [
                'The largest possible area with sides $5$ and $8$ is $\\frac{5\\cdot8}{2}=20$.',
                'The area is exactly $20$, the largest possible. This happens only when the two sides are perpendicular: '
                '$\\angle A=90°$.'])
    M.place_q(N[7], ADV)
    # smallest side from the area (advanced)
    M.new_q(N[8], TOPIC, 'The area of triangle ABC is 18 cm², and $AB=4$ cm. Which of the following could be the length '
            'of BC (in cm)?', ['$5$', '$7$', '$8.5$', '$10$'], 4, [
                'Take AB as the base. The height from C is at most BC.',
                'Therefore $18\\le\\frac{4\\cdot BC}{2}=2\\cdot BC$, that is $BC\\ge9$.',
                'Only $10$ is at least $9$.'])
    M.place_q(N[8], ADV)
    # area two ways, any triangle (advanced)
    M.new_q(N[9], TOPIC, 'Two sides of a triangle are 12 cm and 9 cm long. The altitude to the 12 cm side is 6 cm. What '
            'is the altitude to the 9 cm side (in cm)?', ['$4.5$', '$6$', '$8$', '$12$'], 3, [
                'Area with the side $12$: $\\frac{12\\cdot6}{2}=36$.',
                'Area with the side $9$ and its altitude $h$: $\\frac{9h}{2}=36$, therefore $9h=72$ and $h=8$.',
                'Sense check: the shorter side has the longer altitude. Trap: $4.5=\\frac{9\\cdot6}{12}$ turns the ratio upside down.'])
    M.place_q(N[9], ADV)
    # obtuse count (advanced, exam-hard)
    M.new_q(N[10], TOPIC, 'Two sides of a triangle are 8 cm and 13 cm long. The third side has a whole-number length, and '
            'the triangle is obtuse. How many different lengths are possible for the third side?',
            ['$5$', '$8$', '$10$', '$15$'], 3, [
                'Triangle rule: $13-8<x<13+8$, that is $5<x<21$: the whole numbers $6$ to $20$.',
                'If $x$ is the longest side: $x^2>8^2+13^2=233$. $15^2=225$ is too small and $16^2=256$ works: $x=16$ to $20$, '
                'five lengths.',
                'If $13$ is the longest side: $13^2=169>64+x^2$, that is $x^2<105$: $x=6$ to $10$, five lengths.',
                'Total: $5+5=10$. ($x=11$ to $15$ give acute triangles.)'])
    M.place_q(N[10], ADV)

    M.practice_order(FOUND, [
        'geo31-foundation-p04', 'geo31-foundation-p10', 'geo31-foundation-p26', 'geo31-foundation-p23', 'geo31-foundation-p15', 'geo31-foundation-p14',
        'geo31-foundation-p01', 'geo31-foundation-p02', 'geo31-foundation-p07', 'geo31-foundation-p12', 'geo31-foundation-p16',
        'geo31-foundation-p22', N[4], 'geo31-foundation-p05', 'geo31-foundation-p08', 'geo31-foundation-p13',
        'geo31-foundation-p17', 'geo31-foundation-p18', 'geo31-foundation-p19', 'geo31-foundation-p20', 'geo31-foundation-p03',
        'geo31-foundation-p21', 'geo31-foundation-p06', 'geo31-foundation-p24', 'geo31-foundation-p09', N[3],
        'geo31-foundation-p25', 'geo31-foundation-p11', N[5], 'geo31-foundation-p27'])
    M.practice_order(ADV, [
        'geo31-advanced-p03', 'geo31-advanced-p06', 'geo31-advanced-p27', 'geo31-advanced-p09', 'geo31-advanced-p14',
        'geo31-advanced-p01', 'geo31-advanced-p19', 'geo31-advanced-p15', 'geo31-advanced-p02', 'geo31-advanced-p11', N[11],
        'geo31-advanced-p25', 'geo31-advanced-p08', 'geo31-advanced-p10', 'geo31-advanced-p13', 'geo31-advanced-p04',
        N[9], 'geo31-advanced-p17', 'geo31-advanced-p07', 'geo31-advanced-p05', 'geo31-advanced-p16', 'geo31-advanced-p20',
        'geo31-advanced-p12', 'geo31-advanced-p26', 'geo31-advanced-p18', N[6], N[8], N[7], 'geo31-advanced-p24', N[10],
        'geo31-advanced-p23', 'geo31-advanced-p21', 'geo31-advanced-p22'])

    # lesson order changed: fix "next lesson" / "last lesson" references
    _say(M, 'solve-geo31-g025', 2, "we'll learn it next lesson", "There's actually something for this — we'll learn it soon. For now, Pythagoras.")
    _say(M, 'solve-geo31-g025', 3, "And next lesson: a right triangle with two equal legs",
         "And soon: a right triangle with two equal legs — ratio 30, 30, 30 root 2. We'd solve it without calculating at all.")
    _say(M, V_4545, 4, "Remember the method from last lesson", "Remember the method from the 30-60-90 lesson: pretend there's no root.")

    # =========================================================================================
    # 11. Whole-topic pass: US spelling, solution-video titles, sidebars
    # =========================================================================================
    _cleanup(M)
    _fix_sidebars(M)
    _summaries(M)
    cut_repeats(M)   # 2026-10-05: runs last


# =============================================================================================
# Pass 2: summary lessons - one right before each practice section
# =============================================================================================
def _b(label, tex, size=40):
    """A board line that pops in (label = what the teacher sees in the script)."""
    return A("'%s' appears" % label, T(tex, size=size))


def _summary_video(M, vid, section, intro, slides):
    last = [f['ref'] for f in M.D['flow'] if f['section'] == section][-1]
    sb = [s[0] for s in slides]
    beats = [dict(mode='title', title='Summary', script=intro)]
    beats += [dict(mode='concept', title=t, active=k, script=sc) for k, (t, sc) in enumerate(slides)]
    M.new_video(vid, TOPIC, 'Summary', sb, beats, section, after=last)


def _summaries(M):
    # ---- before the foundation practice: everything taught in "Learn and try" ----
    _summary_video(M, 'r26-t31-summary', L1, [
        'A quick summary before the practice.',
        'Everything important about triangles — in about three minutes.'], [
        ('Three lines', [
            _b('Median → midpoint', 'Median $\\to$ the midpoint of the opposite side'),
            'Three lines from a vertex. The median goes to the midpoint of the opposite side.',
            _b('Altitude → 90°', 'Altitude $\\to$ $90°$ to the opposite side (maybe outside)'),
            'The altitude meets the opposite side at 90 degrees. In an obtuse triangle it can fall outside.',
            _b('Bisector → two equal angles', 'Angle bisector $\\to$ two equal angles'),
            'The angle bisector splits the angle into two equal angles. Nothing more is promised.']),
        ('Angles', [
            _b('α + β + γ = 180°', '$\\alpha+\\beta+\\gamma=180°$'),
            'The angles of a triangle add up to 180. Always.',
            _b('Exterior angle = the two interior angles not next to it', 'Exterior angle $=$ the two interior angles not next to it'),
            'An exterior angle equals the two interior angles not next to it. 52 and 73? The exterior angle is 125.',
            _b('Larger angle ↔ longer side', 'Larger angle $\\leftrightarrow$ longer side opposite it'),
            'And the larger angle sits opposite the longer side.']),
        ('Sides', [
            _b('big − small < c < big + small', '$\\text{big}-\\text{small}<c<\\text{big}+\\text{small}$'),
            'Any two sides together are longer than the third.',
            'So the third side is between the difference and the sum — never equal to either end.',
            _b('Sides 6 and 10: 4 < c < 16 → 2 · 6 − 1 = 11 lengths', 'Sides $6$ and $10$: $4<c<16$ $\\Rightarrow$ $2\\cdot6-1=11$ whole lengths', size=38),
            'Whole-number lengths? Twice the shorter side, minus one. Sides 6 and 10 — 11 lengths.']),
        ('Special triangles', [
            _b('Isosceles: base angle = (180° − v)/2', 'Isosceles: each base angle $=\\dfrac{180°-v}{2}$'),
            'Isosceles: equal legs, equal base angles — and the other way around.',
            'Vertex angle 36? Each base angle is 180 minus 36, over 2 — 72.',
            _b('To the base: median = altitude = bisector', 'To the base: median $=$ altitude $=$ bisector'),
            'The line to the base is a median, an altitude and a bisector at once.',
            _b('Equilateral: 60° · median to the hypotenuse = half', 'Equilateral: all $60°$ · Right: median to the hypotenuse $=\\frac12$ hypotenuse', size=36),
            'Equilateral: every angle is 60. And in a right triangle, the median to the hypotenuse is half the hypotenuse.']),
        ('Area', [
            _b('Area = side × height to that side / 2', 'Area $=\\dfrac{\\text{side}\\times\\text{height to that side}}{2}$'),
            'A side times the height to THAT side, over 2. Any side can be the base.',
            'The height falls outside? Still use only the side itself.',
            _b('leg × leg = hypotenuse × altitude', 'Right triangle: leg $\\times$ leg $=$ hypotenuse $\\times$ altitude'),
            'In a right triangle, count the area twice. Legs 30 and 40, hypotenuse 50: the altitude is 1200 over 50 — 24.',
            _b('area ≤ ab/2 · a median halves the area', 'Sides $a,\\ b$: area $\\le\\dfrac{ab}{2}$ · a median halves the area', size=38),
            'Two sides a and b: the area is at most a times b over 2 — only with a right angle between them.',
            'And a median splits a triangle into two equal areas: same base, same height.']),
        ('Pythagoras', [
            _b('a² + b² = c² — right triangles only', '$a^2+b^2=c^2$ — right triangles only'),
            'Pythagoras works only in a right triangle. Find the right angle first — the hypotenuse is opposite it.',
            _b('Hypotenuse: add · Leg: subtract', 'Hypotenuse: add the squares · Leg: subtract'),
            'Looking for the hypotenuse? Add the squares. A leg? Subtract.',
            _b('c² > a² + b² → obtuse · < → acute', '$c^2>a^2+b^2$ → obtuse · $c^2<a^2+b^2$ → acute', size=38),
            'No right angle? Take the longest side, c. c squared bigger than the other two squares — obtuse. Smaller — acute. Equal — right.']),
        ('Triples', [
            _b('3:4:5 · 5:12:13 · 8:15:17', '$3:4:5$ · $5:12:13$ · $8:15:17$'),
            'Before you calculate, look for a triple.',
            _b('6:8:10 · 15:20:25 · 10:24:26', 'Multiples: $6:8:10$ · $15:20:25$ · $10:24:26$'),
            'Any multiple works too: 6, 8, 10 or 15, 20, 25.',
            _b('The largest number = the hypotenuse', 'The largest number $=$ the hypotenuse'),
            'Match the positions. Hypotenuse 12 and a leg 9? That is not 9, 12, 15.']),
        ('Special right triangles', [
            _b('30°-60°-90°: a, a√3, 2a', '$30°$-$60°$-$90°$: $a,\\ a\\sqrt3,\\ 2a$'),
            'The golden triangle: the short leg, a, is opposite the 30. Double it for the hypotenuse, times root 3 for the long leg.',
            _b('45°-45°-90°: a, a, a√2', '$45°$-$45°$-$90°$: $a,\\ a,\\ a\\sqrt2$'),
            'The silver triangle: legs a and a, hypotenuse a root 2.',
            _b('30°-30°-120°: a, a, a√3 · equilateral: a²√3/4', '$30°$-$30°$-$120°$: $a,\\ a,\\ a\\sqrt3$ · equilateral: $S=\\dfrac{a^2\\sqrt3}{4}$', size=36),
            'The 30-30-120: legs a, base a root 3. And the equilateral triangle: a squared root 3, over 4.',
            _b('12/√3 = 4√3', '$\\dfrac{12}{\\sqrt3}=4\\sqrt3$'),
            'Dividing by a root? Ignore the root, divide, attach it back: 12 over root 3 is 4 root 3.']),
        ('Before you practice', [
            'Before you practice, ask yourself:',
            _b('Where is the right angle? Which side is the hypotenuse?', 'Where is the right angle? Which side is the hypotenuse?', size=36),
            _b('Is this height perpendicular to my base?', 'Is this height perpendicular to my base?', size=36),
            _b('A special angle or a triple hiding?', 'A special angle ($30°$, $45°$, $60°$, $120°$) or a triple hiding?', size=36),
            _b('An angle outside? The exterior angle.', 'An angle outside? Use the exterior angle.', size=36),
            'The traps: doubling the long leg instead of the short one, forgetting to divide the area by 2, '
            'using a sloping side as the height, and a side equal to the sum or the difference.',
            'Good luck.']),
    ])

    # ---- before the advanced practice: the methods of the further guided examples ----
    _summary_video(M, 'r26-t31-summary-2', L2, [
        'A quick summary before the advanced practice.',
        'The methods from the last examples — in about three minutes.'], [
        ('Letters in the answers', [
            _b('Plug in: p = 120 → q = 50 → check every choice', 'Plug in: $p=120$ $\\Rightarrow$ $q=50$ · check every choice', size=38),
            'Letters in the answers? Plug in a comfortable number that fits the figure.',
            'An obtuse p? Try 120. Find q: 50. Put 120 into every answer, and keep only the one that gives 50.',
            _b('Exterior angle: p = q + 70°', 'Exterior angle: $p=q+70°$'),
            'And look for an exterior angle — it cuts the angle-sum equation short.']),
        ('The longest side', [
            _b('Opposite the largest angle: the longest side', 'Opposite the largest angle $\\to$ the longest side'),
            'No lengths at all? Order the angles. The longest side is opposite the largest angle.',
            'You don\'t always need the full order — only the largest angle.',
            _b('Obtuse angle → the side opposite it is the longest', 'Obtuse angle $\\to$ the side opposite it is the longest', size=38),
            'An obtuse angle is always the largest. The side opposite it is the longest.']),
        ('Trap it: min and max', [
            'Can\'t calculate it exactly? Trap it between a minimum and a maximum.',
            _b('Minimum: two sides > the third', 'Minimum: two sides together $>$ the third'),
            'AB is 8. The two other sides together are more than 8 — so the perimeter is more than 16.',
            _b('Obtuse at C: AC, BC < AB = 8 → P < 24', 'Obtuse at C: $AC,\\ BC<AB=8$ $\\Rightarrow$ $16<P<24$', size=38),
            'Obtuse at C? AB is the longest side. The other two are each less than 8 — the perimeter is less than 24.',
            'Answers in order? If a bigger answer fit, every answer between it and the minimum would fit too. Only the smallest one above the minimum can be right.']),
        ('Not necessarily', [
            _b('Two of median, altitude, bisector → isosceles', 'Two of median $\\cdot$ altitude $\\cdot$ bisector $\\to$ isosceles', size=38),
            '"Not necessarily" questions: go through the answers — the quick ones first.',
            'A line that is two of the three — median, altitude, bisector — is a symmetry line. The triangle is isosceles.',
            _b('A median alone → not necessarily', 'A median alone $\\to$ not necessarily'),
            'A median alone can lean to one side. Sketch it: the two sides come out different.',
            'Not sure? Sketch a counterexample.']),
        ('Shaded areas', [
            _b('Shaded = big − white', '$S_{\\text{shaded}}=S_{\\text{big}}-S_{\\text{white}}$'),
            'Shaded area? The main way: a shape you know, minus the white.',
            'Complete the data first — in an equilateral triangle, the altitude is also a median.',
            _b('Or: split into triangles you can calculate', 'Or: split it into triangles you can calculate'),
            'Or split the shaded part into triangles with a known base and height. An altitude outside still counts.']),
        ('Same height', [
            _b('Same height: area ratio = base ratio', 'Same height: area ratio $=$ base ratio'),
            'Two triangles with the same height? The area ratio is the base ratio.',
            _b('DC = 4BD, area 45 → 9 and 36', '$DC=4BD$, area $45$ $\\Rightarrow$ $9$ and $36$'),
            'DC is 4 times BD — so the areas are 1 to 4. 45 is 5 parts of 9: 9 and 36.']),
        ('Faster ways', [
            _b('Shared sides cancel in a difference', 'Shared and equal sides cancel in a difference'),
            'A difference of two perimeters? Shared sides and equal sides cancel — you don\'t need their lengths.',
            _b('√2 ≈ 1.4 · √3 ≈ 1.7', '$\\sqrt2\\approx1.4$ · $\\sqrt3\\approx1.7$'),
            'Out of time? Estimate: root 2 is about 1.4, root 3 about 1.7. A negative length? Eliminate it.',
            _b('a < b → a/b < 1', '$a<b$ $\\Rightarrow$ $\\dfrac ab<1$'),
            'A ratio? Check which way it goes: a is smaller than b, so a over b is less than 1.',
            'And you can always work back from the answers.']),
        ('Before you practice', [
            'Before you practice, ask yourself:',
            _b('Letters in the answers? Plug in numbers.', 'Letters in the answers? Plug in numbers.', size=36),
            _b('Can I calculate it — or only trap it?', 'Can I calculate it — or only trap it between a min and a max?', size=36),
            _b('Which angle is the largest?', 'Which angle is the largest? Which side is opposite it?', size=36),
            _b('A shape I know, minus the white?', 'A shape I know, minus the white?', size=36),
            'The traps: a ratio upside down, a perimeter equal to the minimum, and mixing "could be" with "necessarily".',
            'Good luck.']),
    ])


# =============================================================================================
# 2026-10-05 cut repeats: a lesson slide that the next question video teaches again is cut
# =============================================================================================
def _slide_no(M, vid, title):
    for n, b in enumerate(M.video(vid)['beats'], 1):
        if b.get('title') == title: return n
    raise KeyError('%s: no slide %r' % (vid, title))


def _cut_slides(M, vid, titles):
    """Remove the slides with these titles, drop their sidebar labels, re-point every slide's 'active'."""
    v = M.video(vid)
    M.remove_slides(vid, [_slide_no(M, vid, t) for t in titles])
    sb = [x for x in v['hybrid']['sidebar'] if x not in titles]
    M.set_sidebar(vid, sb)
    for b in v['beats']:
        if b.get('mode') != 'title': b['active'] = sb.index(b['title'])


def _drop_items(M, vid, n, texts):
    """Remove board items whose text starts with one of `texts`, with their appear lines."""
    b = M.slide(vid, n)
    gone = [k for k, it in enumerate(b['items']) if any(it.get('t', '').startswith(x) for x in texts)]
    assert len(gone) == len(texts), (vid, n, gone)
    new_idx, lines = {}, []
    for k in range(len(b['items'])):
        if k not in gone: new_idx[k] = len(new_idx)
    for l in b['lines']:
        if 'appear' in l:
            if l['appear'] in gone: continue
            l = dict(l, appear=new_idx[l['appear']])
        lines.append(l)
    b['items'] = [it for k, it in enumerate(b['items']) if k not in gone]
    b['lines'] = lines
    M.touched_videos.add(vid)


def cut_repeats(M):
    # --- teacher's rule: the lesson example must not use the numbers of the next question (g012: 7 and 12)
    n = _slide_no(M, V_TRI, 'Between diff and sum')
    swap = {
        "The difference is always big minus small. For 7 and 12 it's 12 minus 7 — not 7 minus 12.":
            "The difference is always big minus small. For 5 and 9 it's 9 minus 5 — not 5 minus 9.",
        'For sides 7 and 12: more than 5 and less than 19.': 'For sides 5 and 9: more than 4 and less than 14.',
        "How many whole-number lengths can the third side have? 6, 7, and so on up to 18. That's 13 lengths.":
            "How many whole-number lengths can the third side have? 5, 6, and so on up to 13. That's 9 lengths.",
        'Quick count: twice the shorter side, minus 1. Twice 7 is 14, minus 1 — 13.':
            'Quick count: twice the shorter side, minus 1. Twice 5 is 10, minus 1 — 9.',
        'Write 2 × 7 − 1 = 13': 'Write 2 × 5 − 1 = 9',
    }
    hit = []
    for l in M.slide(V_TRI, n)['lines']:
        for k in ('say', 'draw'):
            if l.get(k) in swap: l[k] = swap[l[k]]; hit.append(1)
    assert len(hit) == len(swap), hit
    M.touched_videos.add(V_TRI)

    # --- geo-016 "Area of Triangles": two September slides are taught again, in full, by the next questions
    #     "Area two ways"         -> solve-q-r26-t31-01 (legs 15, 20, hypotenuse 25: area two ways + leg x leg = hyp x alt)
    #     "Largest possible area" -> solve-q-r26-t31-02 (sides 6 and 8: height at most 6, area at most 24)
    _cut_slides(M, V_AREA, ['Area two ways', 'Largest possible area'])
    _drop_items(M, V_AREA, _slide_no(M, V_AREA, 'Recap'), ['Right triangle: leg $\\times$ leg', 'Sides $a,'])

    # --- geo-019 "The Pythagorean Theorem": "Acute or obtuse?" is taught again by solve-q-r26-t31-03.
    #     That video only showed the obtuse case, so the full rule moves there as one line + one board item.
    _cut_slides(M, 'geo-019', ['Acute or obtuse?'])
    vid = 'solve-q-r26-t31-03'
    b = M.slide(vid, 2)
    b['items'].append(T('Longest side $c$:\n$c^2=a^2+b^2$ → right\n$c^2>a^2+b^2$ → obtuse\n$c^2<a^2+b^2$ → acute',
                        size=32, x=410, y=320, w=900))
    k = next(i for i, l in enumerate(b['lines']) if l.get('say', '').startswith('No figure and no angles'))
    b['lines'][k + 1:k + 1] = [
        {'appear': len(b['items']) - 1, 'label': "'c² = a² + b² right · > obtuse · < acute' appears"},
        {'say': 'The rule: square the longest side. Compare it with the other two squares, added.'},
        {'say': 'Equal — a right angle. Bigger — obtuse. Smaller — acute.'}]
    M.touched_videos.add(vid)


# ======================================================================================================
# 2026-10-06 renumber pass (runs LAST). The English course must not look like the Hebrew one: every Hebrew-derived
# question (guided geo31-g010 ... g040, practice geo31-foundation-p01 ... p20 and geo31-advanced-p01 ... p20) gets new
# numbers (and new letters / settings where it helps); idea, trap, level and methods stay. Every guided solution video
# and every changed figure is rewritten to match. Nothing in topic 31 is recorded (checked ~/Documents/Course.recordings
# 2026-10-06).
# ======================================================================================================
import copy
RN_RECORDED = set()


def _rn_q(M, qid, stem=None, choices=None, correct=None, expl=None, figure=Ellipsis):
    """Rewrite a question (and the figure copies on its slides). Recorded questions are never touched."""
    if qid in RN_RECORDED: return
    kw = {k: v for k, v in dict(stem=stem, choices=choices, correct=correct, expl=expl).items() if v is not None}
    M.set_q(qid, **kw)
    if figure is not Ellipsis: _rn_fig(M, qid, lambda s: figure)


def _rn_fig(M, qid, fn):
    """Apply fn(svg) to a question's figure and to every copy of it on the slides."""
    if qid in RN_RECORDED: return
    _edit_q_svg(M, qid, fn)


def _rn_svg_sub(pairs):
    """fn(svg) that replaces exact substrings (each must hit)."""
    def fn(svg):
        for old, new in pairs:
            assert old in svg, ('svg', old)
            svg = svg.replace(old, new)
        return svg
    return fn


def _rn_label(old, new):
    """Replace the text of an SVG <text> label: '>old</text>' -> '>new</text>'."""
    return ('>%s</text>' % old, '>%s</text>' % new)


def _rn_sub(M, vid, n, pairs):
    """Exact substring replacements in one slide's spoken / drawn lines, labels and board items (each must hit)."""
    if vid in RN_RECORDED: return
    b = M.slide(vid, n)
    for old, new in pairs:
        hit = False
        for l in b['lines']:
            for key in ('say', 'draw', 'label'):
                if key in l and old in l[key]: l[key] = l[key].replace(old, new); hit = True
        for it in b['items']:
            if it.get('t') and old in it['t']: it['t'] = it['t'].replace(old, new); hit = True
        assert hit, (vid, n, old)
    M.touched_videos.add(vid)


def _rn_video(M, qid, slides, titles=None):
    """Rewrite the question slides (2, 3, ...) of a guided question's solution video. The pre-loaded question stays."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    assert len(v['beats']) == len(slides) + 1, (vid, len(v['beats']))
    for n, script in enumerate(slides, 2):
        if script is None: continue
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, script=script, title=(titles or {}).get(n))


def _rn_slide_no(M, vid, title):
    return next(i for i, b in enumerate(M.video(vid)['beats'], 1) if b['title'] == title)


def _rn_titles(M):
    """Solution-video titles follow the (new) question stems."""
    for f in M.D['flow']:
        if f['topic'] != TOPIC or f['type'] != 'video': continue
        v = M.video(f['ref'])
        if v.get('kind') == 'solution' and v.get('questionId') in M.D['questions']:
            v['title'] = v['navLabel'] = M.q(v['questionId'])['stem']


# ====================================================================================================
# ---- renumber pass, part g1: guided g010 ... g028 (+ figures) --------------------------------------------------


def _g1_ticks(p, q, n=1, L=8, gap=6):
    """n short tick marks across the middle of segment pq."""
    ux, uy = _unit(p, q); nx, ny = -uy, ux
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    out = []
    for k in range(n):
        o = (k - (n - 1) / 2) * gap
        cx, cy = mx + ux * o, my + uy * o
        out.append(_ln((cx - nx * L, cy - ny * L), (cx + nx * L, cy + ny * L), TEAL, 1.8))
    return ''.join(out)


def _g1_apex(A, B, angA, angB):
    """A left, B right on one horizontal line (y-down): the third vertex above, with angles angA at A and angB at B."""
    ta, tb = math.tan(math.radians(angA)), math.tan(math.radians(angB))
    L = B[0] - A[0]; dx = L * tb / (ta + tb)
    return (A[0] + dx, A[1] - dx * ta)


def _g1_off(p, q, d, inside):
    """Label point: the midpoint of pq pushed d px away from the point `inside`."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    ux, uy = _unit(p, q); nx, ny = -uy, ux
    if (inside[0] - mx) * nx + (inside[1] - my) * ny > 0: nx, ny = -nx, -ny
    return (mx + nx * d, my + ny * d)


def _g1_arc_between(c, p, q, r):
    """Arc at c between rays c->p and c->q (the angle < 180)."""
    a1, a2 = _ang(c, p), _ang(c, q)
    d = (a2 - a1 + 540) % 360 - 180
    return _arc(c, r, a1, a1 + d), _pt(c, r + 18, a1 + d / 2)


def fig_g010():
    A, B = (165.0, 270.0), (485.0, 270.0)
    Cc = _g1_apex(A, B, 45, 60)
    uA = _unit(Cc, A)
    P1, P2 = (A[0] - 62, A[1]), (A[0] + 62 * uA[0], A[1] + 62 * uA[1])
    arcB, lB = _g1_arc_between(B, A, Cc, 32)
    arcC, lC = _g1_arc_between(Cc, A, B, 30)
    arcV, lV = _g1_arc_between(A, P1, P2, 34)
    return _svg('0 0 640 360', 'Triangle ABC', [
        _poly(A, B, Cc), _ln(P1, A), _ln(P2, A),
        _tx((A[0] + 16, A[1] + 18), 'A'), _tx((B[0] + 18, B[1] + 16), 'B'), _tx((Cc[0], Cc[1] - 20), 'C'),
        arcB, _tx(lB, '4x', TEAL, 18),
        arcC, _tx(lC, '5x', TEAL, 18),
        arcV, _tx(lV, '3x', TEAL, 18),
    ])


def fig_g012():
    s = 30.0
    A = (165.0, 290.0); B = (A[0] + 11 * s, A[1])
    cosA = (6 ** 2 + 11 ** 2 - 13 ** 2) / (2 * 6 * 11); aA = math.degrees(math.acos(cosA))
    Cc = (A[0] + 6 * s * math.cos(math.radians(aA)), A[1] - 6 * s * math.sin(math.radians(aA)))
    G = ((A[0] + B[0] + Cc[0]) / 3, (A[1] + B[1] + Cc[1]) / 3)
    return _svg('0 0 640 360', 'Triangle ABC', [
        _poly(A, B, Cc),
        _tx((A[0] - 18, A[1] + 16), 'A'), _tx((B[0] + 18, B[1] + 16), 'B'), _tx((Cc[0], Cc[1] - 20), 'C'),
        _tx(_g1_off(A, B, 22, G), 'x'), _tx(_g1_off(B, Cc, 22, G), '13'), _tx(_g1_off(A, Cc, 20, G), '6'),
    ])


def fig_g015():
    A = (130.0, 262.0); L = 380.0; B = (A[0] + L, A[1])
    Cc = (A[0] + L * math.cos(math.radians(28)), A[1] - L * math.sin(math.radians(28)))
    BC = math.hypot(B[0] - Cc[0], B[1] - Cc[1]); BD = 2 * BC * math.cos(math.radians(76))
    Dp = (B[0] - BD, A[1])
    arcA, lA = _g1_arc_between(A, B, Cc, 70)
    arcC, lC = _g1_arc_between(Cc, A, Dp, 46)
    return _svg('0 0 640 360', 'Triangle ABC', [
        _poly(A, B, Cc), _ln(Cc, Dp, TEAL),
        _tx((A[0] - 18, A[1] + 16), 'A'), _tx((B[0] + 18, B[1] + 16), 'B'), _tx((Cc[0], Cc[1] - 20), 'C'),
        _tx((Dp[0], Dp[1] + 20), 'D'),
        _g1_ticks(A, B, 1), _g1_ticks(A, Cc, 1), _g1_ticks(B, Cc, 2), _g1_ticks(Dp, Cc, 2),
        arcA, _tx(_pt(A, 96, _ang(A, Cc) / 2), '28°', TEAL, 18),
        arcC, _tx(_pt(Cc, 66, (_ang(Cc, A) + _ang(Cc, Dp)) / 2), 'x', TEAL, 18),
    ])


def fig_g017():
    y1, y2 = 96.0, 264.0
    Cc, Dp, E = (96.0, y2), (166.0, y2), (516.0, y2)
    A, B = (140.0, y1), (400.0, y1)
    return _svg('0 0 640 360', 'Triangles between parallel lines have the same height', [
        _ln((56.8, y1), (583.2, y1)), _ln((56.8, y2), (583.2, y2)),
        '<polygon points="%s,%s %s,%s %s,%s" fill="#e8edf8" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>'
        % (_f(A[0]), _f(A[1]), _f(Cc[0]), _f(Cc[1]), _f(Dp[0]), _f(Dp[1]), INK),
        '<polygon points="%s,%s %s,%s %s,%s" fill="#d9efed" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>'
        % (_f(B[0]), _f(B[1]), _f(Dp[0]), _f(Dp[1]), _f(E[0]), _f(E[1]), INK),
        _tx((A[0], A[1] - 20), 'A'), _tx((B[0], B[1] - 20), 'B'), _tx((Cc[0] - 7, Cc[1] + 21), 'C'),
        _tx((Dp[0], Dp[1] + 21), 'D'), _tx((E[0] + 7, E[1] + 21), 'E'),
    ])


def _g1_right(ab, bc, lab_ab, lab_bc, lab_ac):
    """Right triangle ABC (right angle at B, bottom-left), AB vertical, BC horizontal, drawn to scale."""
    s = min(233.6 / ab, 438.0 / bc)
    hb, wb = ab * s, bc * s
    B = (320 - wb / 2, 296.8); A = (B[0], B[1] - hb); Cc = (B[0] + wb, B[1])
    G = ((A[0] + B[0] + Cc[0]) / 3, (A[1] + B[1] + Cc[1]) / 3)
    return _svg('0 0 640 360', 'Right triangle ABC, with right angle at B', [
        _poly(A, B, Cc), _right(B, -90, 0, 18),
        _tx((A[0] - 14, A[1] - 14), 'A'), _tx((B[0] - 18, B[1] + 14), 'B'), _tx((Cc[0] + 18, Cc[1] + 14), 'C'),
        _tx((B[0] - 22, (A[1] + B[1]) / 2), lab_ab), _tx(((B[0] + Cc[0]) / 2, B[1] + 22), lab_bc),
        _tx(_g1_off(A, Cc, 20, G), lab_ac),
    ])


def fig_g025():
    s = 5.5
    A = (190.0, 80.0)
    B = (A[0] - 16 * s, A[1]); Cc = (A[0], A[1] + 30 * s); E = (A[0] + 40 * s, A[1])
    D = (E[0] + 50 * s * 0.6, E[1] + 50 * s * 0.8)
    def rmark(c, p, q, k=12):
        u, v = _unit(c, p), _unit(c, q)
        a, b = (c[0] + u[0] * k, c[1] + u[1] * k), (c[0] + v[0] * k, c[1] + v[1] * k)
        m = (a[0] + v[0] * k, a[1] + v[1] * k)
        return _ln(a, m, TEAL, 1.7) + _ln(m, b, TEAL, 1.7)
    G1 = ((A[0] + B[0] + Cc[0]) / 3, (A[1] + B[1] + Cc[1]) / 3)
    G3 = ((E[0] + D[0] + Cc[0]) / 3, (E[1] + D[1] + Cc[1]) / 3)
    return _svg('0 0 640 360', 'A chain of three right triangles', [
        _poly(A, B, Cc), _poly(A, E, Cc), _poly(E, D, Cc),
        rmark(A, B, Cc), rmark(A, E, Cc), rmark(E, Cc, D),
        _tx((A[0] - 6, A[1] - 20), 'A'), _tx((B[0] - 16, B[1] - 10), 'B'), _tx((Cc[0] - 12, Cc[1] + 20), 'C'),
        _tx((E[0], E[1] - 20), 'E'), _tx((D[0] + 16, D[1] + 8), 'D'),
        _tx(((A[0] + B[0]) / 2, A[1] - 17), '16'), _tx(_g1_off(B, Cc, 20, G1), '34'),
        _tx(((A[0] + E[0]) / 2, A[1] - 17), '40'), _tx(_g1_off(E, D, 20, G3), '50'),
        _tx(_g1_off(Cc, D, 20, G3), 'x'),
    ])


def rn_g1(M):
    # ---------- g010: vertical angle 2x, 3x, 4x -> 20  ==>  3x (vertical), 4x, 5x -> 15 (Hebrew: α, 3α, 2α -> 30)
    g = 'geo31-g010'
    _rn_q(M, g, choices=['$45°$', '$15°$', '$12°$', '$20°$'], correct=2, expl=[
        'The marked angle $3x$ and the interior angle at A are vertical angles, therefore $\\angle A=3x$.',
        'Angle sum: $3x+4x+5x=180°$, that is $12x=180°$. Therefore $x=15°$.',
        'Trap: $45°$ is $3x$, the angle at A, not $x$.'], figure=fig_g010())
    _rn_sub(M, 'solve-' + g, 2, [
        ('Write 2x in the interior angle at A', 'Write 3x in the interior angle at A'),
        ('This 2x is vertical to the angle at A — so the angle inside is also 2x.',
         'This 3x is vertical to the angle at A — so the angle inside is also 3x.'),
        ('Write 2x + 3x + 4x = 180°', 'Write 3x + 4x + 5x = 180°'),
        ('So 2x plus 3x plus 4x together have to give 180.', 'So 3x plus 4x plus 5x together have to give 180.'),
        ('Write 9x = 180°, x = 20°', 'Write 12x = 180°, x = 15°'),
        ("That's 9x equals 180. Divide by 9 — x is 20.", "That's 12x equals 180. Divide by 12 — x is 15."),
        ('Circle choice 4', 'Circle choice 2'), ('Choice four.', 'Choice two. Not 45 — that is 3x, the angle at A.')])

    # ---------- g011: letters u, p, q -> k, m, n (expression p + q/2 -> m + n/2 = 180°)
    g = 'geo31-g011'
    _rn_q(M, g, stem='In the accompanying figure, the angles at A and C are equal. What is the value of $m+\\frac{n}{2}$?',
          choices=['$90°$', '$360°$', '$180°$', '$270°$'], correct=3, expl=[
        'Call each of the equal angles at A and C $k$.',
        '$m$ is adjacent to the angle at A: $m=180°-k$.',
        '$n$ is an exterior angle at B. It equals the two interior angles not next to it: $n=k+k=2k$.',
        '$m+\\frac{n}{2}=(180°-k)+\\frac{2k}{2}=180°-k+k=180°$.'])
    _rn_fig(M, g, _rn_svg_sub([_rn_label('u', 'k'), _rn_label('p', 'm'), _rn_label('q', 'n')]))
    _rn_video(M, g, [[
        "In the figure, the angles at A and C are equal.",
        "What is the value of m plus n over 2?",
        "We have an expression to calculate. And notice — the figure has k, m and n.",
        "To calculate the expression, I have to end up with ONE unknown. Not stuck with k, m and n.",
        "So let's use the exterior-angle rule. Why? Because m and n are both outside the triangle.",
        D('Write m = 180° − k'),
        "m is adjacent to the angle at A — so m is 180 minus k.",
        D('Write n = k + k = 2k'),
        "n is an exterior angle. It equals the two interior angles not next to it: k plus k. 2k.",
        "Now I can calculate the expression.",
        A('m + n/2 = (180° − k) + 2k/2 appears',
          T('$m+\\frac{n}{2}=(180°-k)+\\frac{2k}{2}$', size=32, x=1060, y=250, w=470)),
        "m is 180 minus k. And n over 2 is 2k over 2 — just k.",
        D('Cross out −k and +k; write = 180°'),
        "Minus k and plus k cancel. We're left with 180.",
        D('Circle choice 3'),
        "Choice three.",
    ]])

    # ---------- g012: AC = 7, BC = 12 -> 10  ==>  AC = 6, BC = 13 -> 11 (Hebrew: 5 and 9 -> 9)
    g = 'geo31-g012'
    _rn_q(M, g, stem='In triangle ABC:\n' r'$\begin{cases} AC=6' + C + r' \\ BC=13' + C + r' \end{cases}$'
          '\nWhich of the following could be the length of AB (in cm)?',
          choices=['$7$', '$21$', '$11$', '$19$'], correct=3, expl=[
        'A side is between the difference and the sum of the other two sides: $13-6<AB<13+6$, that is $7<AB<19$.',
        'Both signs are strict: $7$ and $19$ are not allowed, and $21$ is too long. Only $11$ fits.'], figure=fig_g012())
    _rn_sub(M, 'solve-' + g, 2, [
        ('In triangle ABC, AC is 7 and BC is 12.', 'In triangle ABC, AC is 6 and BC is 13.'),
        ('Write 12 − 7 < x < 12 + 7', 'Write 13 − 6 < x < 13 + 6'),
        ('So x is less than 12 plus 7, and greater than 12 minus 7.', 'So x is less than 13 plus 6, and greater than 13 minus 6.'),
        ('Write 5 < x < 19', 'Write 7 < x < 19'), ('x is between 5 and 19.', 'x is between 7 and 19.'),
        ('Cross out 21', 'Cross out 21'),
        ("From the choices, I'm looking for something between 5 and 19. 21 is too big.",
         "From the choices, I'm looking for something between 7 and 19. 21 is too big."),
        ('Cross out 5 and 19', 'Cross out 7 and 19'),
        ("5? x can't equal 5 — it has to be greater than 5. And the same for 19 — it can't be equal.",
         "7? x can't equal 7 — it has to be greater than 7. And the same for 19 — it can't be equal."),
        ('Circle choice 2', 'Circle choice 3'), ('10 is the only one inside. Choice two.', '11 is the only one inside. Choice three.')])

    # ---------- g014: DC = 6 -> AB = 12  ==>  DC = 7 -> 14 (Hebrew: 5 -> 10)
    g = 'geo31-g014'
    _rn_q(M, g, stem='ABC is an equilateral triangle. Point D lies on BC.\nGiven:\n'
          r'$\begin{cases} \angle DAC=30° \\ DC=7' + C + r' \end{cases}$' '\nWhat is AB (in cm)?',
          choices=['$7$', '$14$', '$21$', '$28$'], correct=2, expl=[
        'ABC is equilateral, therefore $\\angle BAC=60°$ and $\\angle BAD=60°-30°=30°$: AD bisects angle A.',
        'In an equilateral triangle the angle bisector is also a median: $BD=DC=7$.',
        '$AB=BC=7+7=14$.'])
    _rn_fig(M, g, _rn_svg_sub([_rn_label('6', '7')]))
    _rn_sub(M, 'solve-' + g, 2, [
        ("We're given: DC is 6, and angle DAC is 30 degrees. What is AB?",
         "We're given: DC is 7, and angle DAC is 30 degrees. What is AB?"),
        ('Mark equal ticks on BD and DC; write 6 on BD', 'Mark equal ticks on BD and DC; write 7 on BD'),
        ('If it\'s a median — DB equals DC. Each one is 6.', 'If it\'s a median — DB equals DC. Each one is 7.'),
        ('Write BC = 6 + 6 = 12, AB = 12', 'Write BC = 7 + 7 = 14, AB = 14'),
        ("Together: 12. That's the side of the triangle. And AB is a side — so AB is 12.",
         "Together: 14. That's the side of the triangle. And AB is a side — so AB is 14."),
        ('Circle choice 3', 'Circle choice 2'), ('Choice three.', 'Choice two. Not 7 — that is only half the side.')])

    # ---------- g015: vertex 24° -> 78, 24, 54  ==>  vertex 28° -> 76, 28, 48 (Hebrew: 30 -> 75, 30, 45)
    g = 'geo31-g015'
    _rn_q(M, g, stem='In triangle ABC, point D lies on AB.\nGiven:\n'
          r'$\begin{cases} AB=AC \\ \angle BAC=28° \\ BC=CD \end{cases}$' '\nWhat is $\\angle ACD$?',
          choices=['$28°$', '$62°$', '$48°$', '$76°$'], correct=3, expl=[
        'ABC is isosceles: $\\angle B=\\angle ACB=\\frac{180°-28°}{2}=76°$.',
        'BCD is isosceles ($BC=CD$): $\\angle BDC=\\angle B=76°$, therefore $\\angle BCD=180°-76°-76°=28°$.',
        '$\\angle ACD=76°-28°=48°$.'], figure=fig_g015())
    _rn_sub(M, 'solve-' + g, 2, [
        ('Given: angle BAC is 24 degrees.', 'Given: angle BAC is 28 degrees.'),
        ('Write (180° − 24°) ÷ 2 = 78° at B and at C', 'Write (180° − 28°) ÷ 2 = 76° at B and at C'),
        ('How much? Subtract the 24 — 156 — and split it in 2. 78 and 78.',
         'How much? Subtract the 28 — 152 — and split it in 2. 76 and 76.'),
        ("So the whole angle at C is 78. That already lets us eliminate the 78 choice — only PART of that angle can't be 78 too.",
         "So the whole angle at C is 76. That already lets us eliminate the 76 choice — only PART of that angle can't be 76 too."),
        ('Cross out 78°', 'Cross out 76°'), ('Write 78° at angle BDC', 'Write 76° at angle BDC'),
        ('Angle BDC is also 78. Mark it.', 'Angle BDC is also 76. Mark it.'),
        ('Write angle BCD = 180° − 78° − 78° = 24°', 'Write angle BCD = 180° − 76° − 76° = 28°'),
        ('78 and 78 — by the angle sum, the angle here at the bottom of C, angle DCB, is 24.',
         '76 and 76 — by the angle sum, the angle here at the bottom of C, angle DCB, is 28.'),
        ('Write x = 78° − 24° = 54°', 'Write x = 76° − 28° = 48°'),
        ('And now we can find the marked angle: 78 minus 24 — 54.', 'And now we can find the marked angle: 76 minus 28 — 48.'),
        ('Circle choice 1', 'Circle choice 3'), ('Choice one.', 'Choice three.')])

    # ---------- g017: DE = 4CD -> 4  ==>  DE = 5CD -> 5 (Hebrew: 3CD -> 3)
    g = 'geo31-g017'
    _rn_q(M, g, stem='Points A and B lie on one line, and C, D and E lie on a parallel line. Given: $DE=5CD$. '
                     'What is $\\frac{\\text{area of }BDE}{\\text{area of }ACD}$?',
          choices=['$5$', '$\\frac15$', '$25$', '$\\frac52$'], correct=1, expl=[
        'The lines are parallel, therefore both triangles have the same height $h$.',
        'Let $CD=x$. Then $DE=5x$.',
        '$\\dfrac{S_{BDE}}{S_{ACD}}=\\dfrac{\\frac{5x\\cdot h}{2}}{\\frac{x\\cdot h}{2}}=5$.',
        'Without calculating: same height, therefore the area ratio is the base ratio, $5$.'], figure=fig_g017())
    _rn_sub(M, 'solve-' + g, 2, [
        ('Given: DE is 4 times CD.', 'Given: DE is 5 times CD.'),
        ('Write x under CD and 4x under DE', 'Write x under CD and 5x under DE'),
        ('DE is 4 times CD. So CD is x, and DE is 4x.', 'DE is 5 times CD. So CD is x, and DE is 5x.'),
        ('Area of BDE: its base, 4x,', 'Area of BDE: its base, 5x,'),
        ('(4x·h/2)', '(5x·h/2)'), ('\\frac{4x\\cdot h}{2}', '\\frac{5x\\cdot h}{2}'),
        ('Write = 4xh/2 · 2/xh', 'Write = 5xh/2 · 2/xh'),
        ('Cross out xh and 2; write = 4', 'Cross out xh and 2; write = 5'),
        ('Cancel the xh, cancel the 2 — we get 4.', 'Cancel the xh, cancel the 2 — we get 5.'),
        ('Circle choice 4', 'Circle choice 1'), ('Choice four.', 'Choice one.')])
    _rn_sub(M, 'solve-' + g, 3, [
        ('Split DE into four equal parts x, x, x, x and connect each point to B',
         'Split DE into five equal parts x, x, x, x, x and connect each point to B'),
        ('If DE is 4x, we can split it into x, x, x, x — four triangles, each with a base of x.',
         'If DE is 5x, we can split it into x, x, x, x, x — five triangles, each with a base of x.'),
        ('Number the five triangles 1 to 5', 'Number the six triangles 1 to 6'),
        ('So now we have five triangles — ACD and the four small ones.', 'So now we have six triangles — ACD and the five small ones.'),
        ('So all five have the same area.', 'So all six have the same area.'),
        ('Write S(BDE) = 4 · S(ACD)', 'Write S(BDE) = 5 · S(ACD)'),
        ('BDE is made of 4 of them. ACD is 1 of them. So the ratio is 4.', 'BDE is made of 5 of them. ACD is 1 of them. So the ratio is 5.'),
        ('Choice four.', 'Choice one.')])

    # ---------- g020: legs 8, 15 -> 17  ==>  legs 20, 21 -> 29 (Hebrew: 3, 4 -> 5)
    g = 'geo31-g020'
    _rn_q(M, g, stem='Triangle ABC is a right triangle.\nGiven:\n'
          r'$\begin{cases} \angle ABC=90° \\ AB=20' + C + r' \\ BC=21' + C + r' \end{cases}$' '\nWhat is AC (in cm)?',
          choices=['$41$', '$29$', '$21$', '$20$'], correct=2, expl=[
        'The right angle is at B, therefore AC is the hypotenuse — the longest side. $20$ and $21$ are out.',
        '$AC^2=20^2+21^2=400+441=841$, therefore $AC=\\sqrt{841}=29$.',
        'The trap $41=20+21$ breaks the triangle rule: a side is less than the sum of the other two.'],
          figure=_g1_right(20, 21, '20', '21', 'x'))
    _rn_sub(M, 'solve-' + g, 2, [
        ('AB is 8, BC is 15. What is AC?', 'AB is 20, BC is 21. What is AC?'),
        ('We have 15 and 8 there.', 'We have 21 and 20 there.'),
        ('So it has to be more than 8 and more than 15. It could be 15.01 — but it must be more than 15.',
         'So it has to be more than 20 and more than 21. It could be 21.01 — but it must be more than 21.'),
        ('Cross out 15 and 8', 'Cross out 21 and 20'), ('So 15 and 8 are out.', 'So 21 and 20 are out.'),
        ("And 23? That's 8 plus 15.", "And 41? That's 20 plus 21."), ('Cross out 23', 'Cross out 41'),
        ('Only 17 is left', 'Only 29 is left')])
    _rn_sub(M, 'solve-' + g, 3, [
        ('Write 8² + 15² = AC²', 'Write 20² + 21² = AC²'),
        ('AB is 8, BC is 15. AC stays.', 'AB is 20, BC is 21. AC stays.'),
        ('Write 64 + 225 = 289 = AC²', 'Write 400 + 441 = 841 = AC²'),
        ('64 plus 225 is 289.', '400 plus 441 is 841.'),
        ('Write AC = √289 = 17', 'Write AC = √841 = 29'),
        ('To find AC, take the root. 17 squared is 289. So AC is 17.',
         'To find AC, take the root. 30 squared is 900 — a bit too much. 29 squared is 841. So AC is 29.'),
        ('Circle choice 4', 'Circle choice 2'), ('Choice four.', 'Choice two.')])

    # ---------- g021: legs 4, 7 -> √65  ==>  legs 5, 7 -> √74 (Hebrew: 2, 3 -> √13)
    g = 'geo31-g021'
    _rn_q(M, g, stem='Triangle ABC is a right triangle.\nGiven:\n'
          r'$\begin{cases} \angle ABC=90° \\ AB=5' + C + r' \\ BC=7' + C + r' \end{cases}$' '\nWhat is AC (in cm)?',
          choices=['$\\sqrt{74}$', '$12$', '$\\sqrt{24}$', '$74$'], correct=1, expl=[
        'AC is the hypotenuse: $AC^2=5^2+7^2=25+49=74$, therefore $AC=\\sqrt{74}$.',
        'Traps: $12=5+7$ adds the lengths, $74$ forgets the root, and $\\sqrt{24}$ subtracts the squares.'],
          figure=_g1_right(5, 7, '5', '7', 'x'))
    _rn_sub(M, 'solve-' + g, 2, [
        ('AB is 4, BC is 7. What is AC?', 'AB is 5, BC is 7. What is AC?'),
        ('Write 4² + 7² = AC²', 'Write 5² + 7² = AC²'),
        ('Write 16 + 49 = 65 = AC²', 'Write 25 + 49 = 74 = AC²'), ('16 plus 49 is 65.', '25 plus 49 is 74.'),
        ('Write AC = √65', 'Write AC = √74'), ("and we're left with root 65.", "and we're left with root 74."),
        ('Quick sense check: 8 squared is 64, so root 65 is a bit over 8 — longer than the leg 7, shorter than 4 plus 7.',
         'Quick sense check: 8 squared is 64 and 9 squared is 81, so root 74 is between 8 and 9 — longer than the leg 7, '
         'shorter than 5 plus 7.'),
        ('Cross out 11 and 65', 'Cross out 12 and 74'),
        ('11 just adds the lengths. 65 forgot the root.', '12 just adds the lengths. 74 forgot the root.'),
        ('Circle choice 3', 'Circle choice 1'), ('Choice three.', 'Choice one.')])

    # ---------- g022: leg 8, hypotenuse 11 -> √57  ==>  leg 7, hypotenuse 10 -> √51 (Hebrew: 5, 6 -> √11)
    g = 'geo31-g022'
    _rn_q(M, g, stem='Triangle ABC is a right triangle.\nGiven:\n'
          r'$\begin{cases} \angle ABC=90° \\ AB=7' + C + r' \\ AC=10' + C + r' \end{cases}$' '\nWhat is BC (in cm)?',
          choices=['$3$', '$\\sqrt{149}$', '$\\sqrt{17}$', '$\\sqrt{51}$'], correct=4, expl=[
        'The right angle is at B, therefore $AC=10$ is the hypotenuse and BC is a leg.',
        '$BC^2=10^2-7^2=100-49=51$, therefore $BC=\\sqrt{51}$.',
        'Traps: $3=10-7$ subtracts the lengths, not the squares; $\\sqrt{149}$ adds the squares as if BC were the hypotenuse.'],
          figure=_g1_right(7, math.sqrt(51), '7', 'x', '10'))
    _rn_sub(M, 'solve-' + g, 2, [
        ('Mark AC = 11 as the hypotenuse', 'Mark AC = 10 as the hypotenuse'),
        ('AB is 8, and AC — opposite the right angle — is 11. We need BC.',
         'AB is 7, and AC — opposite the right angle — is 10. We need BC.'),
        ('Write BC² = 121 − 64 = 57', 'Write BC² = 100 − 49 = 51'),
        ('Put in the numbers: 11 squared is 121. 8 squared is 64. 121 minus 64 is 57.',
         'Put in the numbers: 10 squared is 100. 7 squared is 49. 100 minus 49 is 51.'),
        ('Write BC = √57', 'Write BC = √51'), ('BC is root 57.', 'BC is root 51.'),
        ('Not 11 minus 8.', 'Not 10 minus 7.'), ('Circle choice 2', 'Circle choice 4'), ('Choice two.', 'Choice four.')])

    # ---------- g025: 10, 26 -> 24 (5-12-13 ×2); 18, 24 -> 30 (3-4-5 ×6); 30√2
    #           ==>  16, 34 -> 30 (8-15-17 ×2); 30, 40 -> 50 (3-4-5 ×10); 50√2  (Hebrew: 5-12-13; 9, 12, 15; 15√2)
    g = 'geo31-g025'
    _rn_q(M, g, choices=['$50$', '$100$', '$50\\sqrt2$', '$30\\sqrt2$'], correct=3, expl=[
        'ABC: $16=2\\cdot8$ and $34=2\\cdot17$, the triple 8-15-17 times $2$. Therefore $AC=2\\cdot15=30$.',
        'ACE: legs $30=10\\cdot3$ and $40=10\\cdot4$, the triple 3-4-5 times $10$. Therefore $CE=10\\cdot5=50$.',
        'CED: two legs of $50$. $CD^2=50^2+50^2=2\\cdot50^2$, therefore $CD=50\\sqrt2$.'], figure=fig_g025())
    vid = 'solve-' + g
    _rn_sub(M, vid, 2, [
        ('26 squared minus 10 squared', '34 squared minus 16 squared'),
        ('Next to AC write 24 (5-12-13 × 2)', 'Next to AC write 30 (8-15-17 × 2)'),
        ("10 and 26 are 5 and 13 times 2. It's 5, 12, 13 — so AC is 12 times 2: 24.",
         "16 and 34 are 8 and 17 times 2. It's 8, 15, 17 — so AC is 15 times 2: 30."),
        ('with legs 18 and 24.', 'with legs 30 and 40.'),
        ('After some practice, 18 and 24 should jump out as familiar: 3 times 6, 4 times 6.',
         'After some practice, 30 and 40 should jump out as familiar: 3 times 10, 4 times 10.'),
        ('Next to CE write 30 (3-4-5 × 6)', 'Next to CE write 50 (3-4-5 × 10)'),
        ("So CE is 5 times 6: 30. It's the 3, 4, 5 triple, scaled by 6.",
         "So CE is 5 times 10: 50. It's the 3, 4, 5 triple, scaled by 10."),
        ('No triple here — the legs are 30 and 30.', 'No triple here — the legs are 50 and 50.'),
        ('Write CD² = 30² + 30² = 2 · 30²', 'Write CD² = 50² + 50² = 2 · 50²'),
        ('30 squared plus 30 squared. Instead of adding to 1800, I write 2 times 30 squared',
         '50 squared plus 50 squared. Instead of adding to 5000, I write 2 times 50 squared'),
        ('Write CD = 30√2', 'Write CD = 50√2'),
        ('Take the root: root 2, and the root of 30 squared is 30. So CD is 30 root 2.',
         'Take the root: root 2, and the root of 50 squared is 50. So CD is 50 root 2.'),
        ('Circle choice 1', 'Circle choice 3'), ('Choice one.', 'Choice three.')])
    _rn_sub(M, vid, 3, [
        ('CD² = (26² − 10²) + 18² + 30²', 'CD² = (34² − 16²) + 40² + 50²'),
        ('$CD^2=(26^2-10^2)+18^2+30^2$', '$CD^2=(34^2-16^2)+40^2+50^2$'),
        ('AC squared is 26 squared minus 10 squared. Add 18 squared for CE squared. Add 30 squared for CD squared.',
         'AC squared is 34 squared minus 16 squared. Add 40 squared for CE squared. Add 50 squared for CD squared.'),
        ('576 plus 324 plus 900 — 1800. The root: 30 root 2.', '900 plus 1600 plus 2500 — 5000. The root: 50 root 2.'),
        ('ratio 30, 30, 30 root 2', 'ratio 50, 50, 50 root 2')])

    # ---------- g027: AB = 6 opposite 30° -> 18 + 6√3  ==>  AB = 5 -> 15 + 5√3 (Hebrew: 4 -> 12 + 4√3)
    g = 'geo31-g027'
    _rn_q(M, g, stem='Triangle ABC is a right triangle.\nGiven:\n'
          r'$\begin{cases} \angle ABC=90° \\ \angle ACB=30° \\ AB=5' + C + r' \end{cases}$'
          '\nWhat is the perimeter of the triangle (in cm)?',
          choices=['$15+5\\sqrt3$', '$10+5\\sqrt3$', '$5+10\\sqrt3$', '$20$'], correct=1, expl=[
        '$\\angle C=30°$, therefore AB, opposite it, is the short leg: $a=5$.',
        'The hypotenuse: $AC=2a=10$. The long leg: $BC=a\\sqrt3=5\\sqrt3$.',
        'Perimeter $=5+10+5\\sqrt3=15+5\\sqrt3$.'])
    _rn_fig(M, g, _rn_svg_sub([_rn_label('6', '5')]))
    vid = 'solve-' + g
    _rn_sub(M, vid, 2, [
        ('and AB is 6. What is the perimeter?', 'and AB is 5. What is the perimeter?'),
        ("it's the short leg. So a is 6.", "it's the short leg. So a is 5."),
        ('Write 12 on AC', 'Write 10 on AC'), ('The hypotenuse, of course, is 12.', 'The hypotenuse, of course, is 10.'),
        ('Write 6√3 on BC', 'Write 5√3 on BC'), ('And the long leg: 6 root 3.', 'And the long leg: 5 root 3.'),
        ("If it's still hard: a is 6, so a root 3 is 6 root 3, and 2a is twice 6 — 12.",
         "If it's still hard: a is 5, so a root 3 is 5 root 3, and 2a is twice 5 — 10."),
        ('Write P = 6 + 6√3 + 12 = 18 + 6√3', 'Write P = 5 + 5√3 + 10 = 15 + 5√3'),
        ('The perimeter: just add the sides. 6 plus 12 is 18 — and the 6 root 3 stays separate.',
         'The perimeter: just add the sides. 5 plus 10 is 15 — and the 5 root 3 stays separate.'),
        ('18 plus 6 root 3. Not 24 root 3 — only one term has the root.',
         '15 plus 5 root 3. Not 20 root 3 — only one term has the root.'),
        ('Circle choice 4', 'Circle choice 1'), ('Choice four.', 'Choice one.')])
    _rn_sub(M, vid, 3, [
        ('BC² = 12² − 6² = 108', 'BC² = 10² − 5² = 75'), ('$BC^2=12^2-6^2=108$', '$BC^2=10^2-5^2=75$'),
        ('to get the hypotenuse, 12.', 'to get the hypotenuse, 10.'),
        ('144 minus 36 is 108. The root of 108 is 6 root 3.', '100 minus 25 is 75. The root of 75 is 5 root 3.')])

    # ---------- g018: perimeter 18 (side 6, halves 3) -> 27√3/4  ==>  perimeter 30 (side 10, halves 5) -> 75√3/4
    #           (Hebrew: perimeter 6, side 2 -> 3√3/4)
    g = 'geo31-g018'
    _rn_q(M, g, stem='ABC is an equilateral triangle with perimeter 30 cm. Points D and E are the midpoints of AB and BC, '
                     'respectively. What is the area of quadrilateral ADEC (in cm²)?',
          choices=['$\\frac{25\\sqrt3}{4}$', '$\\frac{75\\sqrt3}{4}$', '$25\\sqrt3$', '$\\frac{25\\sqrt3}{2}$'], correct=2, expl=[
        'Each side of ABC is $30\\div3=10$, therefore $BD=BE=5$.',
        'DBE has two sides of $5$ with a $60°$ angle between them. It is isosceles with a $60°$ vertex angle, therefore '
        'its base angles are $\\frac{180°-60°}{2}=60°$ too: it is equilateral with side $5$.',
        '$S_{ABC}=\\frac{10^2\\sqrt3}{4}=\\frac{100\\sqrt3}{4}$ and $S_{DBE}=\\frac{5^2\\sqrt3}{4}=\\frac{25\\sqrt3}{4}$.',
        '$S_{ADEC}=\\frac{100\\sqrt3}{4}-\\frac{25\\sqrt3}{4}=\\frac{75\\sqrt3}{4}$.'])
    vid = 'solve-' + g
    _rn_sub(M, vid, 2, [
        ('S(ABC) = 6²√3/4 = 36√3/4', 'S(ABC) = 10²√3/4 = 100√3/4'),
        ('$S_{ABC}=\\dfrac{6^2\\sqrt3}{4}=\\dfrac{36\\sqrt3}{4}$', '$S_{ABC}=\\dfrac{10^2\\sqrt3}{4}=\\dfrac{100\\sqrt3}{4}$'),
        ('S(DBE) = 3²√3/4 = 9√3/4', 'S(DBE) = 5²√3/4 = 25√3/4'),
        ('$S_{DBE}=\\dfrac{3^2\\sqrt3}{4}=\\dfrac{9\\sqrt3}{4}$', '$S_{DBE}=\\dfrac{5^2\\sqrt3}{4}=\\dfrac{25\\sqrt3}{4}$'),
        ('S(ADEC) = 36√3/4 − 9√3/4 = 27√3/4', 'S(ADEC) = 100√3/4 − 25√3/4 = 75√3/4'),
        ('$S_{ADEC}=\\dfrac{36\\sqrt3}{4}-\\dfrac{9\\sqrt3}{4}=\\dfrac{27\\sqrt3}{4}$',
         '$S_{ADEC}=\\dfrac{100\\sqrt3}{4}-\\dfrac{25\\sqrt3}{4}=\\dfrac{75\\sqrt3}{4}$'),
        ('ABC is an equilateral triangle with perimeter 18.', 'ABC is an equilateral triangle with perimeter 30.'),
        ('Write 6 on each side of the big triangle', 'Write 10 on each side of the big triangle'),
        ('First: the perimeter is 18, so each side is 6. 6, 6 and 6 — 18 together.',
         'First: the perimeter is 30, so each side is 10. 10, 10 and 10 — 30 together.'),
        ('Write 3 and 3 on the halves of AB and of BC', 'Write 5 and 5 on the halves of AB and of BC'),
        ('If AB is 6, here we have 3 and 3. Same on BC.', 'If AB is 10, here we have 5 and 5. Same on BC.'),
        ('BD is 3, BE is 3 — isosceles —', 'BD is 5, BE is 5 — isosceles —'),
        ('The side is 6: 36 root 3 over 4.', 'The side is 10: 100 root 3 over 4.'),
        ('Area of DBE: the side is 3. 9 root 3 over 4.', 'Area of DBE: the side is 5. 25 root 3 over 4.'),
        ('36 minus 9: 27 root 3 over 4.', '100 minus 25: 75 root 3 over 4.'),
        ('Circle choice 1', 'Circle choice 2'), ('Choice one.', 'Choice two.')])
    _rn_sub(M, vid, 3, [
        ('Three quarters of 36 root 3 over 4 — 27 root 3 over 4. Same answer.',
         'Three quarters of 100 root 3 over 4 — 75 root 3 over 4. Same answer.'),
        ('Choice one.', 'Choice two.')])

    # ---------- g028: hypotenuse 14 -> 14 + 14√2  ==>  hypotenuse 18 -> 18 + 18√2 (Hebrew: 10 -> 10 + 10√2)
    g = 'geo31-g028'
    _rn_q(M, g, stem='Triangle ABC is a right triangle.\nGiven:\n'
          r'$\begin{cases} \angle ABC=90° \\ \angle ACB=45° \\ AC=18' + C + r' \end{cases}$'
          '\nWhat is its perimeter (in cm)?',
          choices=['$18+18\\sqrt2$', '$36$', '$36\\sqrt2$', '$18+9\\sqrt2$'], correct=1, expl=[
        '$\\angle C=45°$, therefore $\\angle A=45°$ too: a 45°-45°-90° triangle with hypotenuse $AC=18$.',
        'Each leg: $\\frac{18}{\\sqrt2}=9\\sqrt2$.',
        'Perimeter $=9\\sqrt2+9\\sqrt2+18=18+18\\sqrt2$.'])
    _rn_fig(M, g, _rn_svg_sub([_rn_label('14', '18')]))
    vid = 'solve-' + g
    _rn_sub(M, vid, 2, [
        ('the hypotenuse AC is 14.', 'the hypotenuse AC is 18.'),
        ('Just do 14 over root 2', 'Just do 18 over root 2'),
        ("For now, let's write it. 14 is the hypotenuse", "For now, let's write it. 18 is the hypotenuse"),
        ('Write 14 ÷ 2 = 7 → 7√2 on AB and on BC', 'Write 18 ÷ 2 = 9 → 9√2 on AB and on BC'),
        ("Pretend there's no root: 14 divided by 2 is 7 — attach the root 2. 7 root 2.",
         "Pretend there's no root: 18 divided by 2 is 9 — attach the root 2. 9 root 2."),
        ('Write a√2 = 14 → a = 14/√2 = 7√2', 'Write a√2 = 18 → a = 18/√2 = 9√2'),
        ('a root 2 equals 14. To find a, divide by root 2: 14 over root 2 — and as we know, 7 root 2.',
         'a root 2 equals 18. To find a, divide by root 2: 18 over root 2 — and as we know, 9 root 2.'),
        ('Not half of 14', 'Not half of 18'),
        ('Write P = 7√2 + 7√2 + 14 = 14 + 14√2', 'Write P = 9√2 + 9√2 + 18 = 18 + 18√2'),
        ('So the legs are 7 root 2 and 7 root 2. The perimeter: 7 root 2 plus 7 root 2 plus 14 —',
         'So the legs are 9 root 2 and 9 root 2. The perimeter: 9 root 2 plus 9 root 2 plus 18 —'),
        ('— 14 plus 14 root 2.', '— 18 plus 18 root 2.'),
        ('Circle choice 3', 'Circle choice 1'), ('Choice three.', 'Choice one.')])
    _rn_sub(M, vid, 3, [
        ('2t squared equals 196, t squared is 98, t is 7 root 2.', '2t squared equals 324, t squared is 162, t is 9 root 2.'),
        ('5, 5 root 2, 10, and so on.', '6, 6 root 2, 12 — and so on.')])

    rn_g1_lessons(M)


def rn_g1_lessons(M):
    # ---- "Triangles": 5 and 9 were the Hebrew guided question's numbers -> 4 and 9
    n = _rn_slide_no(M, V_TRI, 'Between diff and sum')
    _rn_sub(M, V_TRI, n, [
        ("For 5 and 9 it's 9 minus 5 — not 5 minus 9.", "For 4 and 9 it's 9 minus 4 — not 4 minus 9."),
        ('For sides 5 and 9: more than 4 and less than 14.', 'For sides 4 and 9: more than 5 and less than 13.'),
        ("How many whole-number lengths can the third side have? 5, 6, and so on up to 13. That's 9 lengths.",
         "How many whole-number lengths can the third side have? 6, 7, and so on up to 12. That's 7 lengths."),
        ('Write 2 × 5 − 1 = 9', 'Write 2 × 4 − 1 = 7'),
        ('Quick count: twice the shorter side, minus 1. Twice 5 is 10, minus 1 — 9.',
         'Quick count: twice the shorter side, minus 1. Twice 4 is 8, minus 1 — 7.')])
    for r in M.card('mem-triangle-rules')['tables'][0]['rows']:
        if r[0] == 'Whole-number third side': r[2] = 'sides 4 and 9: \\(2\\cdot4-1=7\\) lengths'

    # ---- "The 30°-60°-90° Triangle": 3 -> 6 and 5 -> 5√3 were the Hebrew lesson's; long leg 2 was the Hebrew's 1 -> 2/√3
    _rn_sub(M, V_3060, 4, [
        ("Say it's 3 — I know right away the hypotenuse is 6.", "Say it's 11 — I know right away the hypotenuse is 22."),
        ('5 becomes 5 root 3.', '10 becomes 10 root 3.')])
    _rn_sub(M, V_3060, 6, [
        ('Long leg 2 (opposite 60°) appears', 'Long leg 5 (opposite 60°) appears'),
        ('Long leg $2$ — opposite $60°$', 'Long leg $5$ — opposite $60°$'),
        ("Now I got a 2 — but this 2 is opposite 60.", "Now I got a 5 — but this 5 is opposite 60."),
        ("So I can't say the hypotenuse is 4, or the long leg is 2 root 3.",
         "So I can't say the hypotenuse is 10, or the long leg is 5 root 3."),
        ('Short leg 2/√3 appears', 'Short leg 5/√3 appears'), ('Short leg $\\frac{2}{\\sqrt3}$', 'Short leg $\\frac{5}{\\sqrt3}$'),
        ('So the short leg is 2 over root 3.', 'So the short leg is 5 over root 3.'),
        ('Hypotenuse 4/√3 appears', 'Hypotenuse 10/√3 appears'), ('Hypotenuse $\\frac{4}{\\sqrt3}$', 'Hypotenuse $\\frac{10}{\\sqrt3}$'),
        ('Instead of 2 over root 3 — 4 over root 3.', 'Instead of 5 over root 3 — 10 over root 3.')])

    # ---- "Area of Triangles": side 8 / altitude 5 / area 20 were the numbers of the practice question q-r26-t31-08
    _rn_sub(M, V_AREA, _rn_slide_no(M, V_AREA, 'Any side as base'), [
        ('Side 8, height to it 5 → 8 × 5 : 2 = 20 appears', 'Side 9, height to it 6 → 9 × 6 ÷ 2 = 27 appears'),
        ('Side $8$, height to it $5$: $\\ \\frac{8\\times5}{2}=20$', 'Side $9$, height to it $6$: $\\ \\frac{9\\times6}{2}=27$'),
        ('Side 8, the height to that side 5 — area 20.', 'Side 9, the height to that side 6 — area 27.')])

    # ---- "Pythagorean Triples": the first question is no longer 8-15-17; 15-20-25 is the guided altitude question
    _rn_sub(M, V_TRIP, _rn_slide_no(M, V_TRIP, '8-15-17: less common'), [
        ("It's less common than the first two — but it does appear. Our first Pythagoras question was exactly 8, 15, 17.",
         "It's less common than the first two — but it does appear. You'll meet it, doubled, in the next question.")])
    _rn_sub(M, V_TRIP, _rn_slide_no(M, V_TRIP, 'Match the positions'), [
        ('One trap. You see 15 and 20 in a right triangle.', 'One trap. You see 27 and 36 in a right triangle.'),
        ('Legs 15 and 20 → hypotenuse 25 appears', 'Legs 27 and 36 → hypotenuse 45 appears'),
        ('Legs $15,\\ 20$ $\\rightarrow$ hypotenuse $25$', 'Legs $27,\\ 36$ $\\rightarrow$ hypotenuse $45$'),
        ("If both are legs — that's 3 and 4 times 5. The hypotenuse is 25.",
         "If both are legs — that's 3 and 4 times 9. The hypotenuse is 45."),
        ('Hypotenuse 20? Not 3-4-5 appears', 'Hypotenuse 36? Not 3-4-5 appears'),
        ('Hypotenuse $20$? Then it is not $3:4:5$', 'Hypotenuse $36$? Then it is not $3:4:5$'),
        ("But if 20 is the hypotenuse", "But if 36 is the hypotenuse")])

    # ---- summary: 6-8-10 and 9-12-15 were the Hebrew lesson's multiples
    vid = 'r26-t31-summary'
    _rn_sub(M, vid, _rn_slide_no(M, vid, 'Triples'), [
        ("'6:8:10 · 15:20:25 · 10:24:26' appears", "'27:36:45 · 25:60:65 · 24:45:51' appears"),
        ('Multiples: $6:8:10$ · $15:20:25$ · $10:24:26$', 'Multiples: $27:36:45$ · $25:60:65$ · $24:45:51$'),
        ('Any multiple works too: 6, 8, 10 or 15, 20, 25.', 'Any multiple works too: 27, 36, 45 or 25, 60, 65.'),
        ('Hypotenuse 12 and a leg 9? That is not 9, 12, 15.', 'Hypotenuse 36 and a leg 27? That is not 27, 36, 45.')])

    _rn_sub(M, vid, _rn_slide_no(M, vid, 'Area'), [
        ('Legs 30 and 40, hypotenuse 50: the altitude is 1200 over 50 — 24.',
         'Legs 45 and 60, hypotenuse 75: the altitude is 2700 over 75 — 36.')])

    # ---- memory cards: examples that were the old question numbers
    c = M.card('mem-special-right')
    c['tips'] = [t.replace('\\frac{14}{\\sqrt2}=7\\sqrt2', '\\frac{22}{\\sqrt2}=11\\sqrt2') for t in c['tips']]
    assert any('11\\sqrt2' in t for t in c['tips'])
    c = M.card('mem-pythagoras')
    c['tips'] = [t.replace('$\\sqrt{65}$', '$\\sqrt{53}$') for t in c['tips']]
    assert any('sqrt{53}' in t for t in c['tips'])


# ====================================================================================================
# ---- renumber pass, part g2: the further guided examples geo31-g031 ... g040 ----
_G2_BOX = dict(x=1060, y=250, w=470)


def _g2_tri_fig(title, A_, B_, angA, angB, labels, arcs):
    """Triangle with base AB on the floor; angA / angB = interior angles at A / B (degrees).
    arcs: dict vertex -> label text (teal), drawn inside the angle."""
    import math as _m
    ab = B_[0] - A_[0]
    angC = 180 - angA - angB
    ac = ab * _m.sin(_m.radians(angB)) / _m.sin(_m.radians(angC))
    C_ = (A_[0] + ac * _m.cos(_m.radians(angA)), A_[1] - ac * _m.sin(_m.radians(angA)))
    body = [_poly(A_, B_, C_),
            _tx((A_[0] - 18, A_[1] + 17), labels[0]), _tx((B_[0] + 18, B_[1] + 17), labels[1]), _tx((C_[0], C_[1] - 20), labels[2])]
    P = {'A': A_, 'B': B_, 'C': C_}
    other = {'A': ('B', 'C'), 'B': ('C', 'A'), 'C': ('A', 'B')}
    for v, txt in arcs.items():
        c = P[v]; a1, a2 = _ang(c, P[other[v][0]]), _ang(c, P[other[v][1]])
        while a2 - a1 > 180: a2 -= 360
        while a2 - a1 < -180: a2 += 360
        r = 26
        body.append(_arc(c, r, a1, a2))
        body.append(_tx(_pt(c, r + (24 if len(txt) > 1 else 16), (a1 + a2) / 2), txt, TEAL, 18))
    return _svg('0 0 640 360', title, body)


def rn_g2(M):
    # =============================== g031: letters p, q -> x, y; plug-in 110 -> 50 (Hebrew 100 -> 40)
    g = 'geo31-g031'
    _rn_q(M, g, stem='ABC is an equilateral triangle. D, A and E lie on one line, E lies on BC, and F lies on the extension '
                     'of BA beyond A. Based on this information and the information in the figure, which expression equals $y$?',
          choices=['$180°-x$', '$x-60°$', '$2x-140°$', '$140°-x$'], correct=2, expl=[
              'Triangle ABE: $\\angle B=60°$ (equilateral), $\\angle BAE=y$ (vertically opposite), $\\angle AEB=180°-x$ (adjacent).',
              'Angle sum: $60°+y+(180°-x)=180°$, therefore $y=x-60°$.',
              'Faster: $x$ is an exterior angle of ABE, therefore $x=60°+y$.',
              'Plug in: $x=110°$ gives $y=50°$. The choices give $70°$, $50°$, $80°$ and $30°$: only $x-60°$ gives $50°$.'])
    _rn_fig(M, g, _rn_svg_sub([_rn_label('p', 'x'), _rn_label('q', 'y')]))
    _rn_video(M, g, [[
        "ABC is an equilateral triangle. The line DE passes through vertex A, and F is on the extension of side BA.",
        "Two angles are marked: x and y. We need to express y using x.",
        "There are several ways to solve this. First way: the angle sum in a triangle.",
        D('Highlight triangle ABE'),
        "Look at the highlighted triangle ABE, and let's express its angles using the givens.",
        "First given: ABC is equilateral. All sides are equal, all angles are equal — and each one is 60 degrees.",
        D('Write 60° at B'),
        "So angle B is 60.",
        D('Write y in angle BAE'),
        "Next, angle BAE. It's vertical to y — and vertical angles are equal. So it's y too.",
        D('Write 180° − x in angle AEB'),
        "Last angle: AEB. It completes x to 180 — so it's 180 minus x.",
        "Now: the angles in a triangle add up to 180. Write it as an equation.",
        A('60° + y + (180° − x) = 180° appears', T('$60°+y+(180°-x)=180°$', size=34, **_G2_BOX)),
        "A plus in front of the parentheses doesn't affect them — we can simply drop them.",
        D('Cross out 180° on both sides'),
        "180 cancels on both sides.",
        D('Write y = x − 60°'),
        "Move minus x across, move the 60 across — and y equals x minus 60.",
        D('Circle choice 2'),
        "Choice two.",
    ], [
        "Another way — with an exterior angle. It shortens the end a little.",
        D('Trace angle x, then the angles 60° and y inside triangle ABE'),
        "Some students notice that x is an exterior angle of the highlighted triangle.",
        "And an exterior angle equals the sum of the two interior angles not next to it: y plus 60.",
        A('x = y + 60° appears', T('$x=y+60°$', size=44, **_G2_BOX)),
        D('Write y = x − 60°'),
        "Move the 60 across and isolate y: y equals x minus 60.",
        D('Circle choice 2'),
        "Choice two again — and we really cut the end short.",
        "Instead of completing x to 180 and writing an angle-sum equation, we used the exterior-angle rule.",
    ], [
        "One more way — psychometric thinking: plugging in numbers.",
        "As we learned in geometry questions with unknowns: plug numbers in for the unknowns, and the question gets easier.",
        "Which unknown? The one that appears in the answers — here, x.",
        "In the figure, x is an obtuse angle. So choose a comfortable obtuse angle: 110.",
        D('Write x = 110° next to the figure'),
        "x equals 110. Now find y.",
        D('Write 60° + y = 110° → y = 50°'),
        "The exterior-angle way again: 60 plus what gives 110? 50.",
        "You could also go through the big triangle — lots of ways. Either way, y is 50.",
        "Now plug 110 in for x in every answer. Anything that isn't 50 — eliminate.",
        D('Next to choice 1 write 70 and cross it out'),
        "Choice one: 180 minus 110 — 70. Eliminated.",
        D('Next to choice 2 write 50 ✓'),
        "Choice two: 110 minus 60 — 50. Keep it.",
        D('Next to choice 3 write 80 and cross it out'),
        "Choice three: twice 110 is 220, minus 140 — 80. Eliminated.",
        D('Next to choice 4 write 30 and cross it out'),
        "Choice four: 140 minus 110 — 30. Eliminated.",
        D('Circle choice 2'),
        "Three answers out — choice two.",
    ]])

    # =============================== g032: angle B 40 -> 50 (Hebrew 60); alpha + beta = 130
    g = 'geo31-g032'
    fig = _g2_tri_fig('Triangle ABC', (195, 290), (445, 290), 82, 50, ('A', 'B', 'C'), {'A': 'α', 'B': '50°', 'C': 'β'})
    _rn_q(M, g, stem='In triangle ABC in the accompanying figure, $\\angle ABC=50°$ and $\\alpha>\\beta$. Which side is '
                     'necessarily the longest?',
          choices=['AB', 'AC', 'BC', 'It cannot be determined from the information given.'], correct=3, expl=[
              '$\\alpha+\\beta=180°-50°=130°$. Since $\\alpha>\\beta$: $\\alpha>65°$ and $\\beta<65°$.',
              'Therefore $\\alpha$ is the largest angle: larger than $\\beta$ and larger than $50°$.',
              'The longest side is opposite the largest angle: BC.'], figure=fig)
    _rn_video(M, g, [[
        "Given: alpha is bigger than beta, and angle B is 50 degrees.",
        "The angles in a triangle add up to 180. If B is 50, alpha and beta together are 130.",
        A('α + β = 130° appears', T('$\\alpha+\\beta=130°$', size=44, **_G2_BOX)),
        "That's our first conclusion from the givens.",
        "Next given: alpha is bigger than beta. What does that mean?",
        "If alpha were equal to beta, each would be 65.",
        D('Write α > 65°, β < 65°'),
        "But alpha is bigger — so alpha is more than 65, and beta is necessarily less than 65.",
        "So alpha is bigger than beta, and bigger than 50 too. Alpha is the biggest angle in the triangle.",
        "Careful: beta is below 65, but it could be above or below 50. So here we can't order all three angles.",
        "We don't need to. We only need the longest side.",
    ], [
        A('Opposite the largest angle — the longest side appears',
          T('Opposite the largest angle is the longest side — and vice versa.', size=32, **_G2_BOX)),
        "We learned: opposite the largest angle is the longest side — and vice versa.",
        D('Draw an arrow from α across to side BC'),
        "Alpha sits at A. Opposite it — side BC. That's the longest side.",
        "Now to the answers — let's see what's necessarily true.",
        D('Cross out choice 1'),
        "Choice one: AB. It's opposite beta, and beta is smaller than alpha — so AB is shorter than BC. Eliminated.",
        D('Cross out choice 2'),
        "Choice two: AC. It's opposite the 50-degree angle at B — also smaller than alpha. Eliminated.",
        D('Circle choice 3'),
        "Choice three: BC — the longest side. Mark it and move on. No need to check the last answer: we just determined it.",
    ]])

    # =============================== g033: AB 6 -> 10 (Hebrew 2); window 20 < P < 30
    g = 'geo31-g033'
    _rn_q(M, g, stem='ABC is an obtuse triangle, with $\\angle ACB>90°$ and $AB=10$ cm. Which of the following could be its '
                     'perimeter (in cm)?',
          choices=['$30$', '$20$', '$24$', '$35$'], correct=3, expl=[
              'Minimum: $AC+BC>AB=10$, therefore the perimeter is more than $10+10=20$.',
              'Maximum: $\\angle C>90°$ is the largest angle, therefore AB is the longest side: $AC<10$ and $BC<10$. '
              'The perimeter is less than $10+10+10=30$.',
              'Only $24$ is between $20$ and $30$.',
              'Example: sides $7,\\ 7,\\ 10$. The obtuse test: $10^2=100>7^2+7^2=98$, therefore the angle '
              'opposite AB is obtuse.'])
    _rn_fig(M, g, _rn_svg_sub([_rn_label('6', '10')]))
    _rn_video(M, g, [[
        "ABC is an obtuse triangle: angle C is more than 90 degrees. And AB is 10.",
        "Which of the answers could be the perimeter?",
        "It should be clear: there isn't enough information to calculate the perimeter exactly.",
        "So this is a minimum–maximum question in geometry.",
        "There's a minimum the perimeter has to be bigger than — and a maximum it has to be smaller than.",
        "Start with the minimum. One of the most basic triangle rules is about the range of the sides:",
        A('The sum of two sides is greater than the third appears',
          T('The sum of any two sides is always greater than the third side.', size=32, **_G2_BOX)),
        D('Write AC + BC > 10'),
        "So AC plus BC has to be more than 10.",
        D('Write P = 10 + AC + BC > 20'),
        "How does that affect the perimeter? The perimeter is 10 plus AC plus BC. 10 plus something bigger than 10 — more than 20.",
        "Any answer that is 20 or less — eliminated.",
        D('Cross out choice 2'),
        "30, 24 and 35 pass. 20 is too small — eliminated.",
    ], [
        "Now we just need the maximum… actually, not so fast.",
        "Some students already see the answer, with a min–max insight. How?",
        "Out of the answers, some are eliminated for being too small — and some for being too big.",
        D('Write the choices in order: 20, 24, 30, 35'),
        "Put them in order. 20 is already out — too small.",
        "So two of the three left must be too big. Which ones can be too big?",
        "Could 24 and 30 be too big, while 35 is the right answer? Impossible.",
        D('Draw a number line: lower limit 20, an open upper limit, and the choices on it'),
        "Picture it: a valid range. The lower limit — 20. An upper limit we haven't calculated yet.",
        "If 35 were inside the range, 24 — which is above 20 and below 35 — would be inside too. Two right answers.",
        "So necessarily the smallest answer above 20 is the right one. 30 and 35 go over the upper limit.",
        D('Circle choice 3'),
        "24 — choice three.",
    ], [
        "Let's see it with a full calculation too.",
        "We learned: opposite the biggest angle is the longest side.",
        D('Mark AB as the longest side'),
        "The triangle is obtuse — C is more than 90. So AB, opposite C, is the longest side in the triangle.",
        D('Write AC < 10, BC < 10'),
        "The other two angles are less than 90, so AC and BC must each be shorter than 10.",
        D('Write P < 10 + 10 + 10 = 30'),
        "So the perimeter is less than 30: 10 plus something under 10 plus something under 10.",
        D('Cross out choices 1 and 4'),
        "30 — too big; it can't even be equal. 35 — too big.",
        D('Circle choice 3'),
        "Only 24 fits. Choice three.",
    ]])

    # =============================== g034: angles 76, 52 -> 64, 58 (Hebrew 70, 55); median 6 to side 4 -> 7 to side 10
    g = 'geo31-g034'
    _rn_q(M, g, choices=['A triangle with angles 64° and 58°',
                         'A triangle in which a median is perpendicular to the side it meets',
                         'A triangle with a median of length 7 cm drawn to a side of length 10 cm',
                         'A triangle in which an altitude also bisects the angle at its starting vertex'], correct=3, expl=[
        'Choice 1: the third angle is $180°-64°-58°=58°$. Two equal angles, therefore two equal sides: isosceles.',
        'Choice 4: an altitude that also bisects its angle is a symmetry line: isosceles.',
        'Choice 2: a median that is perpendicular to its side is a symmetry line: isosceles.',
        'Choice 3: a median of $7$ to a side of $10$ can lean to one side. Then the other two sides are different: '
        'not necessarily isosceles.'])
    _rn_video(M, g, [None, [
        D('Next to choice 1 write 180 − 64 − 58 = 58'),
        "A triangle with angles 64 and 58. Find the third angle: 180 minus 64 is 116, minus 58 — 58.",
        "Two equal angles means two equal sides. It's necessarily isosceles — eliminate.",
        D('Cross out choice 1'),
        "Next: choice four — an altitude that also bisects the angle.",
        "If the altitude is also an angle bisector, it's a line of symmetry — so it's also a median, and the triangle is necessarily isosceles.",
        D('Cross out choice 4'),
        "Eliminated.",
        "Choice three: a median of 7 to a side of 10. It's a median — it splits the side in two. But it isn't given as an altitude or as a bisector.",
        "It's not clear yet what to do with these numbers. So skip it — go to the next answer and hope to eliminate that one.",
        "Choice two: a median that's perpendicular to the side it meets.",
        D('Write α + α = 180° → α = 90°'),
        "Sometimes the right angle is hidden: two equal angles alpha and alpha at the foot of the median. Two alphas make a straight angle, 180 — so alpha is 90.",
        "Either way, the median is also an altitude. That's a line of symmetry — the triangle is isosceles. Eliminate.",
        D('Cross out choice 2'),
        D('Circle choice 3'),
        "Three answers out — so we mark choice three, the one that wasn't clear.",
        "Why can it fail? A median reaches the midpoint, but it can lean to one side. Its length doesn't make it perpendicular — so the two sides can be different.",
        D('Sketch a side of 10 with its midpoint, and a slanted segment of 7 from the midpoint to a third vertex'),
        "Here's a quick sketch. A side of 10, and its midpoint. From the midpoint, a segment of 7 — leaning to the side.",
        "Its top is the third vertex. Join it to both ends: one side comes out short, the other long.",
        "A median of 7 to a side of 10 — and not isosceles. That's why it's the answer.",
    ]])

    # =============================== g035: legs 6, 8 + hyp 26 -> legs 12, 16 + hyp 52 (3-4-5 x4, 5-12-13 x4)
    g = 'geo31-g035'
    _rn_q(M, g, choices=['$288$', '$616$', '$576$', '$624$'], correct=3, expl=[
        'ABC: legs $12$ and $16$, the triple 3-4-5 times $4$. Therefore $AC=20$.',
        'ACD: leg $20$ and hypotenuse $52$, the triple 5-12-13 times $4$. Therefore $CD=48$.',
        'Area $=\\frac{12\\cdot16}{2}+\\frac{20\\cdot48}{2}=96+480=576$.'])
    _rn_fig(M, g, _rn_svg_sub([_rn_label('6', '12'), _rn_label('8', '16'), _rn_label('26', '52')]))
    _rn_video(M, g, [[
        "ABC and ACD are right triangles. What's the area of quadrilateral ABCD?",
        "In a right triangle, when two sides are given, we can always find the third with the Pythagorean theorem.",
        "But we also learned a shortcut: Pythagorean triples.",
        D('Highlight triangle ABC'),
        "Start with triangle ABC. One leg is 12, the other leg is 16.",
        D('Write AC = 20'),
        "That's 3, 4, 5 times four — so the hypotenuse AC is 20. No need for the full theorem.",
        D('Highlight triangle ACD'),
        "On to the second triangle. The leg AC is 20, and the hypotenuse is 52.",
        D('Write CD = 48'),
        "Another triple we learned: 5, 12, 13 — times four, that's 20, 48, 52. We have the leg 20 and the hypotenuse 52 — the missing one is 48. So CD is 48.",
        "Now, how do we find the area of ABCD? Notice: it's made of the two triangles together.",
        A('Area of a triangle = (side × altitude to it) ÷ 2 appears',
          T('$S=\\dfrac{\\text{side}\\times\\text{altitude}}{2}$', size=38, **_G2_BOX)),
        "The area of a triangle: a side times the altitude to it, divided by 2.",
        D('Write S(ABC) = 12·16/2 = 96'),
        "Triangle ABC: cancel first — 16 over 2 is 8, times 12 — 96.",
        D('Write S(ACD) = 20·48/2 = 480'),
        "Triangle ACD: 20 times 48 over 2. Cancel first — 48 over 2 is 24, times 20 — 480.",
        D('Write S(ABCD) = 96 + 480 = 576'),
        "So the quadrilateral's area is the sum of the two triangles: 96 plus 480 — 576.",
        D('Circle choice 3'),
        "Choice three.",
        "Careful with choice two: 52 is the hypotenuse, opposite the right angle at C — not a leg. Use it as a height, and you get 616.",
    ]])

    # =============================== g036: AD 12 -> 20 (Hebrew 8)
    g = 'geo31-g036'
    _rn_q(M, g, stem='In the accompanying figure, triangles ABD and BCD are right triangles. Given: $AD=20$ cm. What is the '
                     'perimeter of quadrilateral ABCD (in cm)?',
          choices=['$20+10\\sqrt3+5\\sqrt2$', '$30+10\\sqrt3+10\\sqrt2$', '$20+20\\sqrt3+10\\sqrt2$', '$20+10\\sqrt3+10\\sqrt2$'],
          correct=4, expl=[
              'ABD: $\\angle A=30°$ and $\\angle B=90°$, hypotenuse $AD=20$. Short leg $BD=\\frac{20}{2}=10$, long leg $AB=10\\sqrt3$.',
              'BCD: a 45°-45°-90° triangle with hypotenuse $BD=10$. Each leg: $BC=CD=\\frac{10}{\\sqrt2}=5\\sqrt2$.',
              'Perimeter (outside sides only): $20+10\\sqrt3+5\\sqrt2+5\\sqrt2=20+10\\sqrt3+10\\sqrt2$.'])
    _rn_fig(M, g, _rn_svg_sub([_rn_label('12', '20')]))
    _rn_video(M, g, [[
        "ABD and BCD are right triangles, and AD is 20. What's the perimeter of ABCD?",
        D('Highlight triangle ABD'),
        "Look at triangle ABD. Angle A is 30 degrees, angle B is 90 —",
        D('Write 60° at D in triangle ABD'),
        "— so the angle at D is 60. A golden triangle: 30, 60, 90.",
        A('Golden triangle 30-60-90: sides x, x√3, 2x appears',
          T('$30°\\!-\\!60°\\!-\\!90°:\\ \\ x,\\ x\\sqrt3,\\ 2x$', size=34, **_G2_BOX)),
        "The hypotenuse is 20. To go from the hypotenuse to the short leg in a golden triangle, divide by 2.",
        D('Write BD = 10'),
        "So BD, opposite the 30, is 10.",
        D('Write AB = 10√3'),
        "From the short leg, opposite 30, to the long leg, opposite 60 — multiply by root 3. So AB is 10 root 3.",
        D('Highlight triangle BCD'),
        "Now triangle BCD. It's a silver triangle: 45, 90, 45 — a right isosceles triangle.",
        A('Silver triangle 45-45-90: sides x, x, x√2 appears',
          T('$45°\\!-\\!45°\\!-\\!90°:\\ \\ x,\\ x,\\ x\\sqrt2$', size=34, x=1060, y=360, w=470)),
        "Careful: BD was a leg up there — here it's the hypotenuse, opposite the right angle at C.",
        "From the hypotenuse to a leg, divide by root 2. How much is 10 over root 2?",
        D('Write 10/√2 = 5√2'),
        "The method we learned: ignore the root — 10 over 2 is 5. Stick the root 2 back on: 5 root 2.",
        D('Write BC = CD = 5√2'),
        "So CD is 5 root 2, and BC is 5 root 2.",
        D('Write P = 20 + 10√3 + 5√2 + 5√2 = 20 + 10√3 + 10√2'),
        "Now the perimeter — the outside only, not BD: 20, plus 10 root 3, plus 5 root 2, plus 5 root 2.",
        "5 root 2 plus 5 root 2 is 10 root 2. So it's 20 plus 10 root 3 plus 10 root 2.",
        D('Circle choice 4'),
        "Choice four.",
    ]])

    # =============================== g037: BE 3, AD 2√3 -> BE 4, AD 3√3 (Hebrew 2, √3); shaded 12√3
    g = 'geo31-g037'
    _rn_q(M, g, stem='In triangle ABC, AE is the altitude to BC. Point D lies on AE, and DBC is an equilateral triangle.\n'
                     'Given:\n$\\begin{cases} BE=4' + C + ' \\\\ AD=3\\sqrt3' + C + ' \\end{cases}$\nWhat is the shaded area (in cm²)?',
          choices=['$28\\sqrt3$', '$12\\sqrt3$', '$6\\sqrt3$', '$16\\sqrt3$'], correct=2, expl=[
              'DE is the altitude of the equilateral triangle DBC, therefore it is also a median: $EC=BE=4$ and $BC=8$.',
              'DEC is a 30°-60°-90° triangle with short leg $EC=4$: $DE=4\\sqrt3$. Therefore $AE=4\\sqrt3+3\\sqrt3=7\\sqrt3$.',
              '$S_{ABC}=\\frac{8\\cdot7\\sqrt3}{2}=28\\sqrt3$ and $S_{DBC}=\\frac{8\\cdot4\\sqrt3}{2}=16\\sqrt3$.',
              'Shaded area $=28\\sqrt3-16\\sqrt3=12\\sqrt3$.',
              'Shorter: the shaded part is two triangles ADB and ADC, each with base $AD=3\\sqrt3$ and (outside) height $4$: '
              '$2\\cdot\\frac{3\\sqrt3\\cdot4}{2}=12\\sqrt3$.'])
    # A moves up so that AD : DE = 3 : 4 (was 2 : 3); labels 3 -> 4, 2√3 -> 3√3
    _rn_fig(M, g, _rn_svg_sub([('320.000,69.564', '320.000,58.071'), ('x1="320.000" y1="69.564"', 'x1="320.000" y1="58.071"'),
                               ('<text x="320.000" y="51.564"', '<text x="320.000" y="40.071"'),
                               ('<text x="350.000" y="115.542"', '<text x="364.000" y="109.796"'),
                               _rn_label('3', '4'), _rn_label('2√3', '3√3')]))
    _rn_video(M, g, [[
        "AE is the altitude to BC, D is on AE, and DBC is equilateral. BE is 4 and AD is 3 root 3. What's the shaded area?",
        "Shaded areas are pretty common on the exam. The main way to handle them: subtracting areas.",
        "We need to see what the shaded area is made of — or what minus what gives it.",
        A('Shaded = S(ABC) − S(DBC) appears', T('$S_{\\text{shaded}}=S_{ABC}-S_{DBC}$', size=34, **_G2_BOX)),
        "Take the big triangle ABC and subtract the white triangle DBC — that's exactly the shaded area.",
        "To calculate the areas, first complete the data.",
        D('Write EC = 4'),
        "If BE is 4, EC is 4 too. Why? DBC is equilateral, and an altitude in an equilateral triangle is also a median.",
        D('Write DE = 4√3'),
        "Now the altitude DE. It splits the equilateral triangle into two golden triangles, 30-60-90.",
        "The short leg, opposite the 30, is 4. Multiply by root 3 — DE is 4 root 3.",
        "Now we have everything: the big triangle minus the small one.",
        D('Write S(ABC) = 8 · 7√3 / 2 = 28√3'),
        "Big triangle: the base BC is 8. The height is 4 root 3 plus 3 root 3 — 7 root 3. 8 times 7 root 3 over 2 — cancel by 2 — 28 root 3.",
        D('Write S(DBC) = 8 · 4√3 / 2 = 16√3'),
        "The small white triangle: base 8, height 4 root 3. Over 2 — 16 root 3.",
        "Is there another way to get that area? Yes — it's equilateral, and there's a formula using only its side.",
        A('Equilateral area = a²√3 ⁄ 4 appears',
          T('$S=\\dfrac{a^2\\sqrt3}{4}=\\dfrac{64\\sqrt3}{4}=16\\sqrt3$', size=34, x=1060, y=380, w=470)),
        "a squared root 3 over 4. Put in 8: 64 root 3 over 4 — 16 root 3. Exactly the same.",
        D('Write 28√3 − 16√3 = 12√3'),
        "All that's left is to subtract: 28 root 3 minus 16 root 3 — 12 root 3.",
        D('Circle choice 2'),
        "Choice two. That's the standard way.",
    ], [
        "But this question has a flash-of-insight way — a shorter one.",
        D('Turn the figure so AD is horizontal (or tilt your head)'),
        "To see it, rotate the triangle. The shaded area is made of two triangles: ADC and ADB.",
        D('Highlight triangle ADC'),
        "For the area of ADC we need a base and its altitude. The base is given: AD, 3 root 3.",
        "Where's the altitude to AD from vertex C? The triangle is obtuse, so it's an outside altitude — extend the base and drop it.",
        D('Extend AD down to E and mark EC = 4 as the altitude'),
        "And we know it too: EC is 4 — the same as BE.",
        D('Write S(ADC) = 3√3 · 4 / 2 = 6√3'),
        "3 root 3 times 4 over 2 — 6 root 3. That's one shaded triangle.",
        D('Write S(ADB) = 6√3'),
        "The other triangle is completely symmetric to it — again 6 root 3.",
        D('Write 6√3 + 6√3 = 12√3'),
        "Twice 6 root 3 — 12 root 3.",
        D('Circle choice 2'),
        "Choice two — with almost no calculating. And choice three, 6 root 3, is only one of the two shaded triangles.",
    ]])

    # =============================== g038: area 32 -> 56, DC = 3BD (Hebrew 18, DC = 2BD); 14, 42, difference 28
    g = 'geo31-g038'
    _rn_q(M, g, stem='Triangle ABC has area 56 cm². Point D lies on BC, and $DC=3BD$. What is the difference between the '
                     'areas of ADC and ABD (in cm²)?',
          choices=['$14$', '$42$', '$28$', '$21$'], correct=3, expl=[
              'ABD and ADC have the same height from A. Therefore their areas are in the ratio of their bases, 1 to 3.',
              'Four equal parts: $56\\div4=14$. $S_{ABD}=14$ and $S_{ADC}=3\\cdot14=42$.',
              'Difference: $42-14=28$.'])
    _rn_video(M, g, [[
        "The area of ABC is 56, and DC is 3 times BD. What's the difference between the areas of ADC and ABD?",
        "Let's start with the math. The base isn't given and neither is the height — so define them with unknowns.",
        D('Write BD = x, DC = 3x'),
        "BD is x. DC is 3 times BD — so DC is 3x.",
        D('Drop the altitude h from A to BC'),
        "Drop an altitude h from vertex A to the base BC.",
        A('S(ABC) = 4x · h ⁄ 2 = 56 appears', T('$S_{ABC}=\\dfrac{4x\\cdot h}{2}=56$', size=36, **_G2_BOX)),
        "The area of ABC: the base BC is 4x, the height is h — 4x times h over 2. And it's given as 56.",
        D('Write 2xh = 56 → xh = 28'),
        "Solve: cancel by 2 — 2xh is 56. Divide by 2 — xh is 28. Keep that.",
        D('Write S(ADC) = 3x·h/2 = 3·28/2 = 42'),
        "Now ADC with x and h: base 3x, height h. 3xh over 2 — 3 times 28 over 2 — 42.",
        D('Write S(ABD) = x·h/2 = 14'),
        "Now ABD: base x, height h. It's obtuse, so the altitude falls outside — but it's the same altitude. xh over 2 — 28 over 2 — 14.",
        D('Write 42 − 14 = 28'),
        "The difference: 42 minus 14 — 28.",
        D('Circle choice 3'),
        "Choice three. That's the math way.",
    ], [
        "This question also has an insight way — through understanding area ratios.",
        A('Same height ⇒ area ratio = base ratio appears',
          T('Same height: the ratio of the areas equals the ratio of the bases.', size=32, **_G2_BOX)),
        "What's an area ratio? Two triangles with the same base and the same height have the same area.",
        "And if they have the same height but one base is 3 times bigger — its area is 3 times bigger too. Exactly like here.",
        "DC is 3 times BD, and the height is the same height, because it's the same triangle.",
        D('Write area ratio 1 : 3 → 14 and 42'),
        "So the areas are 1 to 3. Together 56 — four parts of 14. The left one is 14, the right one is 42.",
        D('Circle choice 3'),
        "The difference — 28. Choice three.",
        D('Split DC into three equal parts and join them to A'),
        "You can also see it another way: split DC into three pieces, each as long as BD, and join them to A.",
        "All four triangles have the same base and the same height — so the same area: 56 over 4, 14 each.",
        "ADC has three of them, ABD has one. The difference — two pieces: 28.",
    ]])

    # =============================== g039: squares of side 3 -> 5 (Hebrew 1); 10√2 − 10
    g = 'geo31-g039'
    _rn_q(M, g, stem='Four congruent squares, each with side 5 cm, are arranged as in the accompanying figure. What is the '
                     'perimeter of AEF minus the perimeter of AFG (in cm)?',
          choices=['$5\\sqrt3-5$', '$10-10\\sqrt2$', '$5-5\\sqrt3$', '$10\\sqrt2-10$'], correct=4, expl=[
              'AE is made of two diagonals of small squares: $AE=5\\sqrt2+5\\sqrt2=10\\sqrt2$. $AG=5+5=10$.',
              'AF is in both triangles, and $EF=FG=5$. These cancel in the difference.',
              '$P_{AEF}-P_{AFG}=AE-AG=10\\sqrt2-10$.',
              'Full calculation: $AF=\\sqrt{10^2+5^2}=\\sqrt{125}=5\\sqrt5$, $P_{AEF}=10\\sqrt2+5+5\\sqrt5$, $P_{AFG}=10+5+5\\sqrt5$.'])
    _rn_fig(M, g, _rn_svg_sub([_rn_label('3', '5')]))
    _rn_video(M, g, [[
        "Four squares with side 5 are joined as shown. What's the perimeter of AEF minus the perimeter of AFG?",
        "Full math first: find the perimeter of AEF, find the perimeter of AFG — and subtract.",
        D('Write 5 on the sides of the small squares'),
        "The four squares are identical, so every side is 5.",
        "Now the length AE. It's made of two diagonals of the small squares.",
        "A diagonal splits a square into two silver triangles. The legs are 5 and 5 — so the diagonal is 5 root 2.",
        D('Write AE = 5√2 + 5√2 = 10√2'),
        "And the second one is 5 root 2 too — so AE is 10 root 2.",
        D('Write AG² + GF² = AF²'),
        "Now AF. It's the hypotenuse of triangle AGF: one leg is 5, the other is 10. Pythagorean theorem.",
        D('Write 10² + 5² = 125 → AF = √125 = 5√5'),
        "100 plus 25 is 125. AF is root 125 — 5 root 5.",
        A('P(AEF) = 5√5 + 5 + 10√2 appears', T('$P_{AEF}=5\\sqrt5+5+10\\sqrt2$', size=32, **_G2_BOX)),
        "Perimeter of AEF: 5 root 5, plus 5, plus 10 root 2.",
        A('P(AFG) = 5√5 + 5 + 10 appears', T('$P_{AFG}=5\\sqrt5+5+10$', size=32, x=1060, y=330, w=470)),
        "Perimeter of AFG: 5 root 5, plus 5, plus 10.",
        D('Write difference = 10√2 − 10'),
        "Subtract: 5 root 5 minus 5 root 5 cancels. 5 minus 5 cancels. 10 root 2 minus 10.",
        D('Circle choice 4'),
        "Choice four. That's the full solution.",
    ], [
        "Could we shorten it? Yes — with a cancelling-sides insight.",
        D('Highlight AF in both triangles'),
        "Look at the two triangles: they share sides. AF is in both — so we don't need its length at all. Just ignore it.",
        D('Mark FG and EF as equal'),
        "Next: FG and EF are equal to each other. So we can ignore them too.",
        D('Write AE − AG = 10√2 − 10'),
        "All we need is AE — 10 root 2 — minus AG, which is 10. 10 root 2 minus 10.",
        D('Circle choice 4'),
        "Choice four — and no Pythagorean theorem at all.",
    ], [
        "One more nuance. Say you reach this question at the end of the exam, with 10 or 20 seconds left.",
        "Sometimes you can eliminate answers by estimating the size.",
        D('Write √2 ≈ 1.4, √3 ≈ 1.7'),
        "Root 3 is about 1.7. Root 2 is about 1.4.",
        D('Next to choice 1 write ≈ 8.5 − 5 > 0'),
        "Choice one: 5 root 3 is about 8.5, minus 5 — positive. Can't eliminate it.",
        D('Next to choice 2 write 10 − 14 < 0 and cross it out'),
        "Choice two: 10 root 2 is about 14. 10 minus 14 — negative. Eliminated.",
        D('Next to choice 3 write < 0 and cross it out'),
        "Choice three: 5 minus 8.5 — negative. Impossible: AE, the diagonal, is longer than AG.",
        "Two answers out already. Here the two left are close — about 3.5 and 4 — so the estimate alone won't finish it.",
        "But with no time left, you're down to a fifty-fifty guess. It's a trick that does show up on the exam.",
    ]])

    # =============================== g040: bold = twice the small perimeter (3/7) -> three times (3/10); Hebrew once (3/4)
    g = 'geo31-g040'
    import math as _m
    s = 0.3 * 262.8; xl, xr = 320 - s / 2, 320 + s / 2; ytop = 296.8 - s * _m.sqrt(3) / 2
    fig = _svg('0 0 640 360', 'Bold outer boundary beside a smaller equilateral triangle', [
        '<polygon points="320.000,69.209 188.600,296.800 451.400,296.800" fill="none" stroke="%s" stroke-width="2" '
        'stroke-linejoin="round"/>' % INK,
        '<polygon points="%s,296.800 %s,296.800 320.000,%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>'
        % (_f(xl), _f(xr), _f(ytop), TEAL),
        _ln((320, 69.209), (188.6, 296.8), INK, 6), _ln((320, 69.209), (451.4, 296.8), INK, 6),
        _ln((188.6, 296.8), (xl, 296.8), INK, 6), _ln((xr, 296.8), (451.4, 296.8), INK, 6),
        _tx((403.7, 183.004), 'b'), _tx(((xr + 320) / 2 + 18, (296.8 + ytop) / 2 - 2), 'a')])
    _rn_q(M, g, stem='The accompanying figure shows two equilateral triangles with side lengths a and b, where $a<b$. The total '
                     'length of the bold segments is three times the perimeter of the smaller triangle. What is $\\frac ab$?',
          choices=['$\\frac13$', '$1$', '$\\frac3{10}$', '$\\frac{10}3$'], correct=3, expl=[
              'The bold line: $b+b+(b-a)=3b-a$.',
              'Three times the small perimeter: $3\\cdot3a=9a$.',
              '$3b-a=9a$, therefore $3b=10a$ and $\\frac ab=\\frac3{10}$.',
              'Check: $a=3$, $b=10$: $30-3=27=3\\cdot9$ ✓.'], figure=fig)
    _rn_video(M, g, [[
        "Two equilateral triangles: the big one has side b, the small one has side a.",
        "The bold line is three times the perimeter of the small triangle. What's a over b?",
        "As usual, we start with the math.",
        D('Write a on all three sides of the small triangle'),
        "The small triangle is equilateral — if one side is a, all its sides are a.",
        D('Write b on all three sides of the big triangle'),
        "The big one too — all sides are b.",
        D('Write b − a on the bottom bold pieces'),
        "But how long is the bold line along the bottom? It's b minus a: the whole side of the big triangle minus the side of the small one.",
        A('b + b + (b − a) = 3 · 3a appears', T('$b+b+(b-a)=3\\cdot3a$', size=40, **_G2_BOX)),
        "Now the given: the bold line equals three times the perimeter of the small triangle — three times 3a, 9a.",
        D('Write 3b − a = 9a → 3b = 10a'),
        "A plus doesn't affect the parentheses. Move the minus a across — 3b equals 10a.",
        "And stop here. Most students get tangled at this point: how do I get from here to a over b? You don't really need to.",
        "It's clear the ratio is 3 to 10 or 10 to 3. On the psychometric exam, you usually won't find both orders as answers — but here you do!",
        D('Cross out choices 1 and 2'),
        "So the trick eliminates one third and 1 — but not 10 thirds.",
        D('Cross out choice 4'),
        "Then use the given a is smaller than b: a over b is less than 1. 10 thirds is out.",
        D('Write 3b = 10a  |÷ 10b → 3/10 = a/b'),
        "If you insist — not during the exam — divide everything by 10b. On the left, the b cancels: 3 tenths. On the right, the 10 cancels: a over b.",
        D('Circle choice 3'),
        "3 tenths — choice three.",
    ], [
        "Another way to solve this question: plugging in the answers.",
        D('Cross out choice 2'),
        "If the ratio is 1 — a equals b. Could a be 1 and b be 1? They defined a big triangle and a small one — the sides can't be equal. Eliminated.",
        D('Cross out choice 4'),
        "Next: 10 thirds means a is 10 and b is 3. Could a be 10 and b be 3? No — b is bigger than a. No point checking. Eliminated.",
        D('Next to choice 1 write a = 1, b = 3: 9 − 1 = 8 ≠ 9, and cross it out'),
        "One third: a is 1, b is 3. Looks fine — but we have to check the bold line. 3 plus 3 plus 3 is 9, minus 1 — 8. Three times the small perimeter: three times 3 — 9. 8 isn't 9. Eliminated.",
        D('Next to choice 3 write a = 3, b = 10: 30 − 3 = 27 = 3 · 9 ✓'),
        "3 tenths: a is 3, b is 10. Bold line: 30 minus 3 — 27. Three times the small perimeter: three times 9 — 27. It works.",
        D('Circle choice 3'),
        "Choice three.",
        "And one third? That's the trap of forgetting to take the small side off the bottom: 3b equals 9a.",
    ]])


# ====================================================================================================
# ---------------------------------------------------------------------------------------------
# Foundation practice geo31-foundation-p01 ... p20: new numbers / letters, figures redrawn to scale
# ---------------------------------------------------------------------------------------------
def _fp_arc(c, p, q, r, label=None, lr=None, size=18):
    """Arc of the angle p-c-q (the part smaller than 180), with an optional label on its bisector."""
    a1, a2 = _ang(c, p), _ang(c, q)
    d = (a2 - a1 + 180) % 360 - 180
    out = [_arc(c, r, a1, a1 + d)]
    if label: out.append(_tx(_pt(c, lr or r + 18, a1 + d / 2), label, TEAL, size))
    return ''.join(out)


def _fp_vlabel(p, centroid, s, d=20):
    u = _unit(centroid, p)
    return _tx((p[0] + d * u[0], p[1] + d * u[1]), s)


def _fp_side(p, q, s, inside, d=18):
    """Length label at the middle of pq, pushed away from the point `inside`."""
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    nx, ny = -(q[1] - p[1]), q[0] - p[0]
    L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
    if (inside[0] - m[0]) * nx + (inside[1] - m[1]) * ny > 0: nx, ny = -nx, -ny
    return _tx((m[0] + d * nx, m[1] + d * ny), s)


def _fp_tick(p, q, L=6):
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2); u = _unit(p, q)
    return _ln((m[0] - L * u[1], m[1] + L * u[0]), (m[0] + L * u[1], m[1] - L * u[0]), TEAL, 1.8)


def _fp_cen(*pts): return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def _fp_from(p, length, deg):
    """Point at distance `length` from p, at `deg` degrees above the horizontal (counter-clockwise, y up)."""
    return (p[0] + length * math.cos(math.radians(deg)), p[1] - length * math.sin(math.radians(deg)))


def fig_fp01():   # isosceles AC = BC, exterior angle 142 at A
    A, B = (114.667, 249.25), (525.333, 249.25)
    C = (320.0, 249.25 - 205.333 * math.tan(math.radians(38)))
    g = _fp_cen(A, B, C); E = (17.6, 249.25)
    return _svg('0 0 640 360', 'Triangle ABC', [
        _poly(A, B, C), _ln(E, A), _fp_vlabel(A, g, 'A'), _fp_vlabel(B, g, 'B'), _fp_vlabel(C, g, 'C'),
        _fp_arc(A, C, E, 40, '142°', 66), _fp_arc(C, A, B, 40, 'x', 62),
        _fp_tick(A, C), _fp_tick(B, C)])


def fig_fp02():   # AB = 11 (bottom), AC = 9, BC = 7
    k = 40.0; A, B = (100.0, 300.0), (100.0 + 11 * k, 300.0)
    cx = (81 - 49 + 121) / 22.0; cy = math.sqrt(81 - cx * cx)
    C = (100.0 + cx * k, 300.0 - cy * k); g = _fp_cen(A, B, C)
    return _svg('0 0 640 360', 'Triangle ABC', [
        _poly(A, B, C), _fp_vlabel(A, g, 'A'), _fp_vlabel(B, g, 'B'), _fp_vlabel(C, g, 'C'),
        _fp_arc(A, B, C, 24, 'α', 40), _fp_arc(B, A, C, 24, 'β', 40), _fp_arc(C, A, B, 24, 'γ', 40),
        _fp_side(A, B, '11', g, 20), _fp_side(A, C, '9', g), _fp_side(B, C, '7', g)])


def fig_fp05():   # parallel lines, AB = BC, angle B = 46
    B, C = (174.0, 289.5), (466.0, 289.5)
    A = _fp_from(B, 292.0, 46); R = (502.5, A[1])
    return _svg('0 0 640 360', 'An isosceles triangle between parallel lines', [
        _poly(A, B, C), _ln((137.5, 289.5), (502.5, 289.5)), _ln((137.5, A[1]), R),
        _fp_tick(A, B), _fp_tick(B, C),
        _tx((158.0, 305.5), 'B'), _tx((482.0, 305.5), 'C'), _tx((A[0], A[1] - 20), 'A'),
        _fp_arc(B, C, A, 36, '46°', 58), _fp_arc(A, C, R, 36, 'y', 58)])


def fig_fp06():   # right at B, AC = 40, BC = 32 (AB = 24)
    B = (190.0, 290.0); A = (190.0, 65.0); C = (490.0, 290.0); g = _fp_cen(A, B, C)
    return _svg('0 0 640 360', 'Right triangle with a missing leg', [
        _poly(A, B, C), _right(B, -90, 0, 14),
        _fp_vlabel(A, g, 'A'), _fp_vlabel(B, g, 'B'), _fp_vlabel(C, g, 'C'),
        _fp_side(A, C, '40', g, 20), _fp_side(B, C, '32', g, 20)])


def fig_fp07():   # angle A = 40, angle B = 75, AB = 14
    A, B = (177.342, 274.124), (462.658, 274.124)
    AC = (B[0] - A[0]) * math.sin(math.radians(75)) / math.sin(math.radians(65))
    C = _fp_from(A, AC, 40); g = _fp_cen(A, B, C)
    return _svg('0 0 640 360', 'Triangle ABC', [
        _poly(A, B, C), _fp_vlabel(A, g, 'A'), _fp_vlabel(B, g, 'B'), _fp_vlabel(C, g, 'C'),
        _fp_arc(A, B, C, 30, '40°', 52), _fp_arc(B, A, C, 30, '75°', 52), _fp_side(A, B, '14', g, 22)])


def fig_fp09():   # AD perpendicular to BC, AB = 17, BD = 8, AC = sqrt(421)
    k = 14.6; D = (260.0, 289.5); A = (260.0, 289.5 - 15 * k); B = (260.0 - 8 * k, 289.5); C = (260.0 + 14 * k, 289.5)
    g = _fp_cen(A, B, C)
    return _svg('0 0 640 360', 'Two right triangles share an altitude', [
        _poly(A, B, C), _ln(A, D, TEAL), _right(D, -90, 0, 13),
        _fp_vlabel(A, g, 'A'), _fp_vlabel(B, g, 'B'), _fp_vlabel(C, g, 'C'), _tx((D[0], D[1] + 21), 'D'),
        _fp_side(A, B, '17', D, 20), _fp_side(B, D, '8', A, 20), _fp_side(A, C, '√421', D, 26)])


def fig_fp13():   # right at B, angle ADB = 56, AC bisects angle A
    A, B = (194.857, 284.286), (445.143, 284.286); AB = B[0] - A[0]
    D = (B[0], B[1] - AB / math.tan(math.radians(56))); Cp = (B[0], B[1] - AB * math.tan(math.radians(17)))
    return _svg('0 0 640 360', 'An angle bisector inside a right triangle', [
        _poly(A, B, D), _ln(A, Cp, TEAL), _right(B, 180, -90, 12),
        _tx((A[0] - 17, A[1] + 12), 'A'), _tx((B[0] + 16, B[1] + 14), 'B'), _tx((Cp[0] + 20, Cp[1]), 'C'),
        _tx((D[0] + 15, D[1] - 13), 'D'),
        _fp_arc(A, B, Cp, 56, 'α', 72), _fp_arc(A, Cp, D, 80, 'α', 96),
        _fp_arc(D, A, B, 30, '56°', 50), _fp_arc(Cp, A, B, 24, 'β', 42)])


def fig_fp17():   # AB = AC, AD altitude, AE = EC, angle BAD = 22
    A, D = (320.0, 75.714), (320.0, 284.286); AD = D[1] - A[1]
    half = AD * math.tan(math.radians(22)); B, C = (320.0 - half, D[1]), (320.0 + half, D[1])
    AC = AD / math.cos(math.radians(22)); AE = AC * math.sin(math.radians(22)) / math.sin(math.radians(136))
    E = (320.0, A[1] + AE)
    return _svg('0 0 640 360', 'Two isosceles relationships with an altitude', [
        _poly(A, B, C), _ln(A, D, TEAL), _ln(E, C), _right(D, -90, 0, 12),
        _tx((320.0, 56.714), 'A'), _tx((B[0] - 18, 297.286), 'B'), _tx((C[0] + 18, 297.286), 'C'),
        _tx((320.0, 305.286), 'D'), _tx((337.0, E[1] - 12), 'E'),
        _fp_arc(A, B, D, 80, None), _tx((A[0] - 20, A[1] + 100), '22°', TEAL, 18), _fp_arc(E, D, C, 24, 'x', 42)])


def fig_fp18():   # vertically opposite angles at O; D = 52, C = 71
    O = (300.0, 195.0); th = 62.0
    aD = -88.0; aA = aD - th; aC = aD + 180; aB = aA + 180
    OD = 128.0; OA = OD * math.sin(math.radians(52)) / math.sin(math.radians(180 - 52 - th))
    OC = 90.0; OB = OC * math.sin(math.radians(71)) / math.sin(math.radians(180 - 71 - th))
    Dp, A_, Cp, B_ = _pt(O, OD, aD), _pt(O, OA, aA), _pt(O, OC, aC), _pt(O, OB, aB)
    return _svg('0 0 640 360', 'Two triangles with vertically opposite central angles', [
        _poly(A_, O, Dp), _poly(B_, O, Cp),
        _tx((O[0] - 16, O[1] + 16), 'O'), _fp_vlabel(A_, _fp_cen(A_, O, Dp), 'A'), _fp_vlabel(Dp, _fp_cen(A_, O, Dp), 'D'),
        _fp_vlabel(B_, _fp_cen(B_, O, Cp), 'B'), _fp_vlabel(Cp, _fp_cen(B_, O, Cp), 'C'),
        _fp_arc(A_, O, Dp, 22, 'α', 40), _fp_arc(Dp, A_, O, 22, '52°', 44),
        _fp_arc(Cp, O, B_, 22, '71°', 44), _fp_arc(B_, O, Cp, 22, 'β', 40)])


def _fp_meet(p, u, q, v):
    """Intersection of the lines p + s*u and q + t*v."""
    det = u[0] * (-v[1]) - u[1] * (-v[0])
    s = ((q[0] - p[0]) * (-v[1]) - (q[1] - p[1]) * (-v[0])) / det
    return (p[0] + s * u[0], p[1] + s * u[1])


def fig_fp19():   # two vertical parallel lines; 128 at the right line, 31 at the left line
    xl, xr = 271.333, 368.667
    L1 = (xl, 140.0); u1 = (math.cos(math.radians(38)), math.sin(math.radians(38)))     # down-right
    L2 = (xl, 268.0); u2 = (math.sin(math.radians(31)), -math.cos(math.radians(31)))   # up-right
    R = _fp_meet(L1, u1, (xr, 0), (0, 1)); X = _fp_meet(L1, u1, L2, u2)
    T1a = (L1[0] - 28 * u1[0], L1[1] - 28 * u1[1]); T1b = (R[0] + 32 * u1[0], R[1] + 32 * u1[1])
    T2a = (L2[0] - 10 * u2[0], L2[1] - 10 * u2[1]); T2b = (xr + 10, L2[1] + (xr + 10 - xl) / u2[0] * u2[1])
    return _svg('0 0 640 360', 'An exterior angle transferred between parallel lines', [
        _ln((xl, 330), (xl, 30)), _ln((xr, 330), (xr, 30)), _ln(T1a, T1b), _ln(T2a, T2b),
        _fp_arc(R, T1b, (xr, 30), 20, '128°', 42), _fp_arc(L2, (xl, 30), T2b, 30, '31°', 50),
        _fp_arc(X, L1, L2, 18, 'α', 34)])


def rn_fp(M):
    F = 'geo31-foundation-p%02d'

    # p01: exterior 146 -> 142 at A; base angles 38; x = 104
    _rn_q(M, F % 1, choices=['$76°$', '$38°$', '$104°$', '$142°$'], correct=3, expl=[
        'The interior angle at A is adjacent to $142°$: $\\angle A=180°-142°=38°$.',
        '$AC=BC$, therefore the angles opposite them are equal: $\\angle B=\\angle A=38°$.',
        '$x=180°-38°-38°=104°$.'], figure=fig_fp01())

    # p02: sides 8, 10, 13 -> AB = 11, AC = 9, BC = 7: alpha < beta < gamma
    _rn_q(M, F % 2, choices=['$\\beta<\\alpha<\\gamma$', '$\\gamma<\\beta<\\alpha$', '$\\alpha<\\beta<\\gamma$',
                             '$\\beta<\\gamma<\\alpha$'], correct=3, expl=[
        'The sides opposite $\\alpha$, $\\beta$ and $\\gamma$ are $BC=7$, $AC=9$ and $AB=11$.',
        'The longer the side, the larger the angle opposite it: $\\alpha<\\beta<\\gamma$.'], figure=fig_fp02())

    # p03: BD = 7 -> 9
    _rn_q(M, F % 3, stem='Triangle ADC is equilateral, and B, D and C lie on one line in that order.\nGiven:\n'
          r'$\begin{cases} BD=9' + C + r' \\ \angle BAD=30° \end{cases}$' '\nWhat is DC (in cm)?',
          choices=['$4.5$', '$9$', '$9\\sqrt3$', '$18$'], correct=2, expl=[
        '$\\angle ADC=60°$ (equilateral). It is an exterior angle of ABD: $60°=30°+\\angle ABD$, therefore $\\angle ABD=30°$.',
        'Two equal angles ($30°$ at A and at B), therefore the sides opposite them are equal: $AD=BD=9$.',
        'ADC is equilateral, therefore $DC=AD=9$.'])
    _rn_fig(M, F % 3, _rn_svg_sub([_rn_label('7', '9')]))

    # p04: 11 and 8 -> 14 and 5
    _rn_q(M, F % 4, stem='Two sides of a triangle are 14 cm and 5 cm long. Which of the following cannot be the length '
          'of the third side (in cm)?', choices=['$12$', '$18$', '$15$', '$9$'], correct=4, expl=[
        'The third side is between the difference and the sum: $14-5<x<14+5$, that is $9<x<19$.',
        '$9$ is not allowed (strict sign). $12$, $15$ and $18$ are all inside.'])

    # p05: angle B 42 -> 46; y = 67
    _rn_q(M, F % 5, choices=['$46°$', '$113°$', '$67°$', '$92°$'], correct=3, expl=[
        '$AB=BC$, therefore $\\angle A=\\angle C=\\frac{180°-46°}{2}=67°$.',
        'Alternate angles between the parallel lines: $y=\\angle C=67°$.'], figure=fig_fp05())

    # p06: 25, 20 (3-4-5 x 5) -> 40, 32 (3-4-5 x 8); area 384
    _rn_q(M, F % 6, stem='Triangle ABC is right at B.\nGiven:\n'
          r'$\begin{cases} AC=40' + C + r' \\ BC=32' + C + r' \end{cases}$' '\nWhat is its area (in cm²)?',
          choices=['$768$', '$384$', '$640$', '$512$'], correct=2, expl=[
        '$32=8\\cdot4$ and $40=8\\cdot5$: the triple 3-4-5 times $8$. Therefore $AB=8\\cdot3=24$.',
        'Area $=\\frac{24\\cdot32}{2}=384$.',
        'Check: $AB^2=40^2-32^2=1600-1024=576$, $AB=24$ ✓.',
        'Traps: $640=\\frac{40\\cdot32}{2}$ uses the hypotenuse as a height; $768$ forgets to divide by $2$.'],
          figure=fig_fp06())

    # p07: A 35, B 85, AB 12 -> A 40, B 75, AB 14 (C = 65)
    _rn_q(M, F % 7, stem='In triangle ABC:\n'
          r'$\begin{cases} \angle A=40° \\ \angle B=75° \\ AB=14' + C + r' \end{cases}$'
          '\nWhich of the following is necessarily true?',
          choices=['$\\angle C=55°$', '$BC>14$ cm', '$AC<BC$', '$AC>14$ cm'], correct=4, expl=[
        '$\\angle C=180°-40°-75°=65°$ (not $55°$).',
        'Order the angles: $\\angle A<\\angle C<\\angle B$. The sides opposite them: $BC<AB<AC$.',
        '$AB=14$, therefore $AC>14$.'], figure=fig_fp07())

    # p08: AC = BC = 10 -> 16
    _rn_q(M, F % 8, stem='In triangle ABC, CD bisects angle C and meets AB at D.\nGiven:\n'
          r'$\begin{cases} AC=BC=16' + C + r' \\ \angle A=60° \end{cases}$' '\nWhat is DB (in cm)?',
          choices=['$8\\sqrt3$', '$16$', '$8$', '$16\\sqrt3$'], correct=3, expl=[
        '$AC=BC$, therefore $\\angle B=\\angle A=60°$ and $\\angle C=180°-60°-60°=60°$. The triangle is equilateral: $AB=16$.',
        'The angle bisector CD is also a median: $DB=\\frac{16}{2}=8$.'])
    _rn_fig(M, F % 8, _rn_svg_sub([_rn_label('10', '16')]))

    # p09: 13, 5, sqrt313 (5-12-13) -> 17, 8, sqrt421 (8-15-17); DC = 14
    _rn_q(M, F % 9, stem='In the accompanying figure, $AD\\perp BC$.\nGiven:\n'
          r'$\begin{cases} AB=17' + C + r' \\ BD=8' + C + r' \\ AC=\sqrt{421}' + C + r' \end{cases}$'
          '\nWhat is DC (in cm)?', choices=['$14$', '$15$', '$22$', '$8$'], correct=1, expl=[
        'ABD is right at D, with $BD=8$ and $AB=17$: the triple 8-15-17. Therefore $AD=15$.',
        'ADC: $DC^2=AC^2-AD^2=421-225=196$, therefore $DC=14$.',
        'Traps: $15$ is AD, and $22=8+14$ is the whole side BC.'], figure=fig_fp09())

    # p10: area 30 -> 42
    _rn_q(M, F % 10, stem='CD is a median in triangle ABC. The area of ABC is 42 cm². What is the area of ACD (in cm²)?',
          choices=['$14$', '$21$', '$42$', '$28$'], correct=2, expl=[
        'A median splits a triangle into two triangles of equal area: $S_{ACD}=\\frac{42}{2}=21$.'])

    # p11: BD = 6 -> 10
    _rn_q(M, F % 11, stem='In the accompanying figure, $DE\\parallel AC$ and $BD=10$ cm. What is the area of triangle BDE '
          '(in cm²)?', choices=['$50$', '$10\\sqrt3$', '$50\\sqrt3$', '$25\\sqrt3$'], correct=4, expl=[
        'The angles next to the two marked $120°$ angles are $180°-120°=60°$: $\\angle BDE=60°$ and $\\angle ACB=60°$.',
        '$DE\\parallel AC$, therefore $\\angle DEB=\\angle ACB=60°$ (corresponding angles). BDE has two $60°$ angles, '
        'therefore it is equilateral with side $10$.',
        'Area $=\\frac{10^2\\sqrt3}{4}=\\frac{100\\sqrt3}{4}=25\\sqrt3$.'])
    _rn_fig(M, F % 11, _rn_svg_sub([_rn_label('6', '10')]))

    # p12: 26, 19 -> 31, 17
    _rn_q(M, F % 12, stem='In triangle ABC:\n'
          r'$\begin{cases} AB=31' + C + r' \\ AC=17' + C + r' \end{cases}$' '\nWhich of the following is necessarily true?',
          choices=['$BC>14$ cm', '$BC<17$ cm', 'Angle A is the largest angle', '$BC>31$ cm'], correct=1, expl=[
        'The third side is between the difference and the sum: $31-17<BC<31+17$, that is $14<BC<48$.',
        'Therefore $BC>14$ is always true.',
        'BC can be less than $17$ or more than $31$, therefore choices 2 and 4 are not necessarily true. Angle A is opposite '
        'BC, and BC need not be the longest side.'])

    # p13: angle ADB 52 -> 56; beta = 73
    _rn_q(M, F % 13, stem='Triangle ABD is right at B, and AC bisects angle A. Given: $\\angle ADB=56°$. What is the value '
          'of $\\beta$?', choices=['$17°$', '$68°$', '$73°$', '$34°$'], correct=3, expl=[
        'In ABD: $\\angle BAD=180°-90°-56°=34°$.',
        'AC bisects it: $\\angle BAC=\\frac{34°}{2}=17°$.',
        'In ABC: $\\beta=180°-90°-17°=73°$.'], figure=fig_fp13())

    # p14: 2 alpha -> 3 theta
    _rn_q(M, F % 14, stem='In a right triangle, one acute angle is $3\\theta$. What is the exterior angle adjacent to the '
          'other acute angle?', choices=['$180°-3\\theta$', '$3\\theta$', '$90°+3\\theta$', '$90°-3\\theta$'], correct=3, expl=[
        'The angles of the triangle: $90°$, $3\\theta$ and the other acute angle.',
        'The exterior angle next to the other acute angle equals the two interior angles not next to it: $90°+3\\theta$.'])

    # p15: five equal angles (x = 15) -> four equal angles (x = 18)
    _rn_q(M, F % 15, stem='In a right triangle, one acute angle is t. The other is divided into four equal angles, each '
          'measuring t. What is t?', choices=['$22.5°$', '$36°$', '$18°$', '$30°$'], correct=3, expl=[
        'The two acute angles of a right triangle add up to $90°$. Together they are $1+4=5$ angles of $t$.',
        '$5t=90°$, therefore $t=18°$.',
        'Traps: $22.5°=\\frac{90°}{4}$ forgets the angle $t$ itself; $36°=\\frac{180°}{5}$ forgets the right angle.'])

    # p16: P, Q, R and u > v -> K, L, M and s > t
    _rn_q(M, F % 16, stem='The exterior angles adjacent to the interior angles at K and L of triangle KLM are s and t, '
          'respectively. Given: $s>t$. Which of the following is necessarily true?',
          choices=['$KL>KM$', '$LM>KM$', '$KL<LM$', '$LM<KM$'], correct=4, expl=[
        '$\\angle K=180°-s$ and $\\angle L=180°-t$. Since $s>t$: $\\angle K<\\angle L$.',
        'The side opposite K is LM, and the side opposite L is KM. The smaller angle is opposite the shorter side: $LM<KM$.'])

    # p17: angle BAD 24 -> 22; x = 44
    _rn_q(M, F % 17, stem='In the accompanying figure:\n'
          r'$\begin{cases} AB=AC \\ AD\perp BC \\ AE=EC \\ \angle BAD=22° \end{cases}$' '\nWhat is x?',
          choices=['$22°$', '$136°$', '$44°$', '$68°$'], correct=3, expl=[
        'AD is the altitude to the base of the isosceles triangle ABC, therefore it also bisects angle A: $\\angle EAC=22°$.',
        '$AE=EC$, therefore $\\angle ECA=\\angle EAC=22°$.',
        '$x$ is an exterior angle of triangle AEC: $x=22°+22°=44°$.'], figure=fig_fp17())

    # p18: 48 and 76 -> 52 and 71; beta = alpha - 19
    _rn_q(M, F % 18, choices=['$\\alpha+19°$', '$\\alpha-19°$', '$180°-\\alpha$', '$\\alpha-24°$'], correct=2, expl=[
        'The two angles at O are vertically opposite, therefore equal. Call each one $\\theta$.',
        'Angle sums: $\\begin{cases} \\alpha+52°+\\theta=180° \\\\ \\beta+71°+\\theta=180° \\end{cases}$ '
        'Therefore $\\alpha+52°=\\beta+71°$.',
        '$\\beta=\\alpha+52°-71°=\\alpha-19°$.'], figure=fig_fp18())

    # p19: 136 and 24 -> 128 and 31; alpha = 97
    _rn_q(M, F % 19, choices=['$128°$', '$97°$', '$159°$', '$66°$'], correct=2, expl=[
        'The $128°$ angle moves to the left parallel line as a corresponding angle. There it is an exterior angle of the triangle.',
        'The exterior angle equals the two interior angles not next to it: $\\alpha+31°=128°$, therefore $\\alpha=97°$.'],
          figure=fig_fp19())

    # p20: letters p, q, r and E -> x, y, z and D
    _rn_q(M, F % 20, stem='In the accompanying figure, line $\\ell$ is parallel to BC. The extension of side AC meets '
          '$\\ell$ at D. Which expression equals $z$?',
          choices=['$y+x$', '$180°-y-x$', '$y-x$', '$180°-y+x$'], correct=4, expl=[
        'The interior angle at B is adjacent to $y$: $\\angle B=180°-y$.',
        'The exterior angle at C equals the two interior angles not next to it: $x+(180°-y)$.',
        '$\\ell\\parallel BC$, therefore $z$ equals this exterior angle (corresponding angles): $z=180°-y+x$.',
        'Check with numbers: $x=65°$ and $y=125°$ give $\\angle B=55°$ and $\\angle C=60°$. The exterior angle at C is '
        '$120°=180°-125°+65°$ ✓.'])
    _rn_fig(M, F % 20, _rn_svg_sub([_rn_label('p', 'x'), _rn_label('q', 'y'), _rn_label('r', 'z'), _rn_label('E', 'D')]))


# ====================================================================================================
# ---- 2026-10-06 renumber pass: advanced practice geo31-advanced-p01 ... p20 (Hebrew-derived) ----

def _ap_tick(p, q, n=1, L=8, gap=5):
    """n short ticks across the middle of segment pq."""
    ux, uy = _unit(p, q); m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2); out = ''
    for k in range(n):
        o = (k - (n - 1) / 2) * gap
        c = (m[0] + ux * o, m[1] + uy * o)
        out += _ln((c[0] - uy * L, c[1] + ux * L), (c[0] + uy * L, c[1] - ux * L), TEAL, 1.8)
    return out


def _ap_fig_p04():
    """ABC right at B (AB = 5, BC = 12), ACD right at C - drawn to scale."""
    B = (142.714, 284.286); u = 250 / 12.0
    C = (B[0] + 12 * u, B[1]); A = (B[0], B[1] - 5 * u)
    e = _unit(A, C); cd = 60 / 13.0 * u
    Dp = (C[0] + e[1] * cd, C[1] - e[0] * cd)          # perpendicular to AC at C, away from B
    return _svg('0 0 640 360', 'Two right triangles with equal areas', [
        _poly(A, B, C, Dp), _ln(A, C, TEAL),
        _right(B, -90, 0, 11.5), _right(C, _ang(C, A), _ang(C, Dp), 11.5),
        _tx((A[0] - 15, A[1] - 13), 'A'), _tx((B[0] - 16, B[1] + 14), 'B'), _tx((C[0] + 1, C[1] + 22), 'C'),
        _tx((Dp[0] + 20, Dp[1]), 'D'),
        _tx((B[0] - 23, (A[1] + B[1]) / 2), '5'), _tx(((B[0] + C[0]) / 2, B[1] + 23), '12')])


def _ap_fig_p07(old):
    """Triangle KLM, LN bisects angle L; equal ticks on KN and NL (KL = KM is given in the text)."""
    K, L, Mv, N = (161.497, 273.166), (478.503, 273.166), (417.960, 86.834), (320.000, 158.007)
    arcs = re.findall(r'<path d="M [^"]*" fill="none" stroke="#087f83" stroke-width="2"/>', old)
    xs = re.findall(r'<text [^>]*>x</text>', old)
    assert len(arcs) == 2 and len(xs) == 2
    return _svg('0 0 640 360', 'Triangle KLM', [
        _poly(K, L, Mv), _ln(L, N, TEAL), _ap_tick(K, N), _ap_tick(N, L),
        _tx((143.497, 290.166), 'K'), _tx((496.503, 290.166), 'L'), _tx((417.960, 66.834), 'M'), _tx((299.000, 146.007), 'N'),
        ] + arcs + xs)


def _ap_fig_p10():
    """Right at C: AC = 10, BC = 24, D the midpoint of BC (equal ticks)."""
    C_ = (174.0, 289.5); u = 292 / 24.0
    B_ = (C_[0] + 24 * u, C_[1]); A_ = (C_[0], C_[1] - 10 * u); D_ = ((C_[0] + B_[0]) / 2, C_[1])
    return _svg('0 0 640 360', 'A median in a right triangle', [
        _poly(A_, B_, C_), _ln(A_, D_, TEAL), _right(C_, -90, 0, 11),
        _ln((247, 297.5), (247, 281.5), TEAL, 2.6), _ln((393, 297.5), (393, 281.5), TEAL, 2.6),
        _tx((A_[0] - 15, A_[1] - 13), 'A'), _tx((B_[0] + 16, B_[1] + 14), 'B'), _tx((C_[0] - 15, C_[1] + 14), 'C'),
        _tx((D_[0], D_[1] + 22), 'D')])


def _ap_fig_p12():
    """EBC right at C (BC = 3, CE = 3√3, angle E = 30°); AED right at A (AD = 5√3, AE = 15). Drawn to scale."""
    E = (409.846, 123.846); u = (E[0] - 140.308) / 15.0
    A_ = (140.308, E[1]); D_ = (A_[0], E[1] + 5 * math.sqrt(3) * u)
    B_ = (E[0] + 6 * u, E[1]); C_ = _pt(E, 3 * math.sqrt(3) * u, -30)
    mbc = ((B_[0] + C_[0]) / 2, (B_[1] + C_[1]) / 2); mec = ((E[0] + C_[0]) / 2, (E[1] + C_[1]) / 2)
    return _svg('0 0 640 360', 'Two right triangles with a common angle', [
        _poly(E, B_, C_), _poly(E, A_, D_),
        _right(A_, 0, 90, 13.5), _right(C_, _ang(C_, E), _ang(C_, B_), 9),
        _tx((E[0], E[1] + 22), 'E'), _tx((B_[0] + 18, B_[1] + 6), 'B'), _tx((C_[0] + 8, C_[1] - 17), 'C'),
        _tx((A_[0] - 15, A_[1] + 15), 'A'), _tx((D_[0] - 18, D_[1] + 10), 'D'),
        _tx((mbc[0] + 18, mbc[1] - 4), '3'), _tx((mec[0] - 16, mec[1] - 18), '3√3'),
        _tx((A_[0] - 30, (A_[1] + D_[1]) / 2), '5√3')])


def _ap_fig_p13():
    """AD ⊥ BC: AB = 30, BD = 24, AD = 18, DC = 7, AC = √373. Drawn to scale."""
    B_ = (150.0, 250.0); u = 11.0
    D_ = (B_[0] + 24 * u, B_[1]); A_ = (D_[0], D_[1] - 18 * u); C_ = (D_[0] + 7 * u, D_[1])
    return _svg('0 0 640 360', 'Find a full base using a shared altitude', [
        _poly(A_, B_, C_), _ln(A_, D_, TEAL), _right(D_, -90, 0, 12.7),
        _tx((A_[0], A_[1] - 19), 'A'), _tx((B_[0] - 17, B_[1] + 13), 'B'), _tx((D_[0], D_[1] + 22), 'D'),
        _tx((C_[0] + 17, C_[1] + 13), 'C'),
        _tx(((A_[0] + B_[0]) / 2 - 14, (A_[1] + B_[1]) / 2 - 14), '30'), _tx(((B_[0] + D_[0]) / 2, B_[1] + 23), '24'),
        _tx(((A_[0] + C_[0]) / 2 + 26, (A_[1] + C_[1]) / 2 - 8), '√373')])


def _ap_fig_p17():
    """Right at A: AB = 33, AC = 44, BC = 55; AD the altitude to BC. Drawn to scale."""
    A_ = (258.526, 295.263); u = (295.263 - 64.737) / 44.0
    B_ = (A_[0] + 33 * u, A_[1]); C_ = (A_[0], A_[1] - 44 * u)
    e = _unit(B_, C_); t = (A_[0] - B_[0]) * e[0] + (A_[1] - B_[1]) * e[1]
    D_ = (B_[0] + e[0] * t, B_[1] + e[1] * t)
    n = _unit(A_, D_)
    return _svg('0 0 640 360', 'Altitude to the hypotenuse', [
        _poly(A_, B_, C_), _ln(A_, D_, TEAL), _right(A_, -90, 0, 7.7), _right(D_, _ang(D_, A_), _ang(D_, B_), 7),
        _tx((A_[0] - 16, A_[1] + 12), 'A'), _tx((B_[0] + 16, B_[1] + 12), 'B'), _tx((C_[0] - 13, C_[1] - 14), 'C'),
        _tx((D_[0] + n[0] * 20, D_[1] + n[1] * 20), 'D'),
        _tx(((A_[0] + B_[0]) / 2, A_[1] + 23), '33'), _tx((A_[0] - 25, (A_[1] + C_[1]) / 2), '44')])


def rn_ap(M):
    # ---------- p01 (letters / order only): the correct triangle is the "bisector that is also an altitude" one
    _rn_q(M, 'geo31-advanced-p01', 'Which of the following triangles is not necessarily equilateral?',
          ['An isosceles triangle in which one of the angles measures $60°$',
           'A triangle in which one angle bisector is also an altitude',
           'A triangle in which two of the angles measure $60°$',
           'An isosceles triangle whose base is equal to half of twice one of its legs'], 2, [
        'Choice 3: the third angle is $180°-60°-60°=60°$: equilateral.',
        'Choice 1: a $60°$ vertex angle gives base angles of $\\frac{180°-60°}{2}=60°$, and $60°$ base angles leave '
        '$60°$ for the vertex: equilateral either way.',
        'Choice 4: half of twice a leg is the leg itself, so the base equals the legs: equilateral.',
        'Choice 2: an angle bisector that is also an altitude makes the triangle isosceles. It does not force the base to '
        'equal the other two sides.',
        'Example: a triangle with sides $7,\\ 7,\\ 4$ has this symmetry line, but it is not equilateral.'])

    # ---------- p02: right isosceles AB = BC = 4 + equilateral ACD  ==>  AB = BC = 6
    _rn_q(M, 'geo31-advanced-p02',
          'In the accompanying figure, ABC is a right isosceles triangle with $AB=BC=6$ cm, and ACD is equilateral. '
          'What is the perimeter of quadrilateral ABCD (in cm)?',
          ['$12+6\\sqrt2$', '$12+12\\sqrt2$', '$18+6\\sqrt2$', '$12+18\\sqrt2$'], 2, [
        'ABC: legs $6$ and $6$, therefore $AC=6\\sqrt2$.',
        'ACD is equilateral: $AD=CD=AC=6\\sqrt2$.',
        'Perimeter (outside sides only): $6+6+6\\sqrt2+6\\sqrt2=12+12\\sqrt2$. AC is inside and is not counted.'])
    _rn_fig(M, 'geo31-advanced-p02', _rn_svg_sub([_rn_label('4', '6')]))

    # ---------- p03: each equal side 4 × the base -> 9/4  ==>  5 × the base -> 11/5
    _rn_q(M, 'geo31-advanced-p03', 'In an isosceles triangle, each equal side is five times as long as the base. What is '
          'the ratio of the perimeter to the length of an equal side?',
          ['$5$', '$\\frac{11}{5}$', '$\\frac{5}{11}$', '$\\frac95$'], 2, [
        'Let the base be $1$. Each equal side is $5$, and the perimeter is $1+5+5=11$.',
        '$\\frac{\\text{perimeter}}{\\text{equal side}}=\\frac{11}{5}$.',
        'Trap: $\\frac{5}{11}$ is the ratio upside down.'])

    # ---------- p04: AB = 9, BC = 12 (3-4-5 × 3) -> CD = 36/5  ==>  AB = 5, BC = 12 (5-12-13) -> CD = 60/13
    _rn_q(M, 'geo31-advanced-p04', 'Triangles ABC and ACD are right at B and at C, respectively, and they have equal areas.'
          '\nGiven:\n' r'$\begin{cases} AB=5' + C + r' \\ BC=12' + C + r' \end{cases}$' '\nWhat is CD (in cm)?',
          ['$\\frac{60}{13}$', '$5$', '$12$', '$\\frac{120}{13}$'], 1, [
        'ABC: legs $5$ and $12$, the triple 5-12-13. Therefore $AC=13$.',
        '$S_{ABC}=\\frac{5\\cdot12}{2}=30$.',
        'ACD is right at C, with legs AC and CD: $\\frac{13\\cdot CD}{2}=30$, therefore $CD=\\frac{60}{13}$.',
        'Trap: $\\frac{120}{13}$ forgets to divide by $2$.'],
          figure=_ap_fig_p04())

    # ---------- p05 (no numbers to change): average of the three reflex angles -> 300°; wording + choice order
    _rn_q(M, 'geo31-advanced-p05', 'At every vertex of a triangle, consider the reflex angle outside the triangle (the '
          'reflex angle $=360°$ minus the interior angle). What is the average of these three reflex angles?',
          ['$240°$', '$270°$', '$300°$', '$330°$'], 3, [
        'Sum: $(360°-\\alpha)+(360°-\\beta)+(360°-\\gamma)=1080°-180°=900°$.',
        'Average: $\\frac{900°}{3}=300°$.',
        'Plug in: an equilateral triangle gives $360°-60°=300°$ at each vertex.'])

    # ---------- p06: shortest 2, longest 7 -> 6.5  ==>  shortest 3, longest 9 -> 7.5
    _rn_q(M, 'geo31-advanced-p06', 'The shortest and longest sides of a triangle are 3 cm and 9 cm, respectively. Which of '
          'the following could be the length of its third side (in cm)?',
          ['$6$', '$7.5$', '$9.5$', '$5.5$'], 2, [
        '$9$ is the longest side, therefore $x<9$.',
        'Triangle rule: $3+x>9$, therefore $x>6$.',
        'Only $7.5$ is between $6$ and $9$. ($6$ is not allowed: the sign is strict.)'])

    # ---------- p07 (letters): AB = AC, BD bisects B, AD = DB -> 72°  ==>  triangle KLM
    old7 = M.q('geo31-advanced-p07')['questionVisual']['svg']
    _rn_q(M, 'geo31-advanced-p07', 'In triangle KLM, LN bisects angle L and meets KM at N.\nGiven:\n'
          r'$\begin{cases} KL=KM \\ KN=NL \end{cases}$' '\nWhat is angle L?',
          ['$36°$', '$72°$', '$108°$', '$60°$'], 2, [
        'Let each half of angle L be $x$: $\\angle KLN=\\angle NLM=x$.',
        '$KN=NL$, therefore $\\angle K=\\angle KLN=x$.',
        '$KL=KM$, therefore $\\angle M=\\angle L=2x$.',
        'Angle sum: $x+2x+2x=180°$, therefore $x=36°$ and $\\angle L=72°$.'], figure=_ap_fig_p07(old7))

    # ---------- p08: BD = 3/4 BC, ADC = 14 -> 42  ==>  BD = 4/5 BC, ADC = 11 -> 44
    _rn_q(M, 'geo31-advanced-p08', 'AD is an altitude in triangle ABC, with D on BC. Given: $BD=\\frac45BC$. The area of '
          'ADC is 11 cm². What is the area of ABD (in cm²)?',
          ['$22$', '$44$', '$\\frac{55}{4}$', '$55$'], 2, [
        '$BD=\\frac45BC$, therefore $DC=\\frac15BC$ and $BD=4\\cdot DC$.',
        'ABD and ADC have the same height AD. Therefore $S_{ABD}=4\\cdot S_{ADC}=4\\cdot11=44$.',
        'Trap: $55=5\\cdot11$ is the area of the whole triangle ABC.'])
    _rn_fig(M, 'geo31-advanced-p08', _rn_svg_sub([('368.667', '378.400'), ('382.293', '392.026')]))

    # ---------- p09: B = 35°, A > 45° -> 75° impossible  ==>  B = 25°, A > 60° -> 80° impossible
    _rn_q(M, 'geo31-advanced-p09', 'In triangle ABC, angle B is 25° and angle A is greater than 60°. BC is extended beyond '
          'C to D. Which of the following cannot be the measure of angle ACD?',
          ['$110°$', '$80°$', '$95°$', '$130°$'], 2, [
        'Angle ACD is an exterior angle of the triangle: $\\angle ACD=\\angle A+25°$.',
        '$\\angle A>60°$, therefore $\\angle ACD>85°$. $80°$ is impossible.',
        'The other choices work: $95°$, $110°$ and $130°$ give $\\angle A=70°$, $85°$ and $105°$.'])

    # ---------- p10: AC = 12, BC = 16 (3-4-5 × 4)  ==>  AC = 10, BC = 24 (5-12-13 × 2)
    _rn_q(M, 'geo31-advanced-p10', 'Triangle ABC is right at C, and D is the midpoint of BC.\nGiven:\n'
          r'$\begin{cases} AC=10' + C + r' \\ BC=24' + C + r' \end{cases}$'
          '\nWhich statement compares triangles ADC and ADB correctly?',
          ['Their areas are equal, and ADB has the smaller perimeter', 'ADC has the smaller area and the smaller perimeter',
           'Their areas are equal, and ADC has the smaller perimeter', 'Their areas and perimeters are equal'], 3, [
        'AD is a median, therefore $S_{ADC}=S_{ADB}$.',
        'Perimeters: both have AD, and $DC=DB=12$. Only AC and AB are different.',
        '$AB=26$ (the triple 5-12-13 times $2$) and $AC=10$. Therefore ADC has the smaller perimeter.'],
          figure=_ap_fig_p10())

    # ---------- p11: angles 2x, 4x, 6x, short leg 5  ==>  3x, 6x, 9x, short leg 9
    _rn_q(M, 'geo31-advanced-p11', 'The angles of a triangle are $3x$, $6x$ and $9x$. Which of the following could be its '
          'side lengths (in cm)?',
          ['$9,\\ 12,\\ 15$', '$9,\\ 9,\\ 9\\sqrt2$', '$9,\\ 18,\\ 18\\sqrt3$', '$9,\\ 9\\sqrt3,\\ 18$'], 4, [
        '$3x+6x+9x=180°$, therefore $x=10°$: the angles are $30°$, $60°$ and $90°$.',
        'A 30°-60°-90° triangle has sides $a,\\ a\\sqrt3,\\ 2a$. With $a=9$: $9,\\ 9\\sqrt3,\\ 18$.',
        'Trap: $9,\\ 12,\\ 15$ is a right triangle too, but not a 30°-60°-90° one.'])

    # ---------- p12: BC = 2, CE = 2√3, AD = 4√3 -> 16  ==>  BC = 3, CE = 3√3, AD = 5√3 -> 21
    _rn_q(M, 'geo31-advanced-p12', 'A, E and B lie on one line in that order; D, E and C lie on another. The marked angles '
          'at A and C are right angles.\nGiven:\n' r'$\begin{cases} BC=3 \\ CE=3\sqrt3 \\ AD=5\sqrt3 \end{cases}$'
          '\nWhat is AB?',
          ['$15$', '$21$', '$6+5\\sqrt3$', '$11$'], 2, [
        'EBC is right at C, with legs $BC=3$ and $CE=3\\sqrt3$: the ratio $a,\\ a\\sqrt3$ with $a=3$. It is a 30°-60°-90° '
        'triangle: $EB=2\\cdot3=6$, and $\\angle BEC=30°$ (opposite the short leg BC).',
        'Vertically opposite angles: $\\angle AED=30°$.',
        'AED is right at A. $AD=5\\sqrt3$ is opposite the $30°$ angle, therefore it is the short leg. '
        'The long leg: $AE=5\\sqrt3\\cdot\\sqrt3=15$.',
        '$AB=AE+EB=15+6=21$.'], figure=_ap_fig_p12())

    # ---------- p13: AB = 13, BD = 12 (5-12-13), AC = √61 -> 18  ==>  AB = 30, BD = 24 (3-4-5 × 6), AC = √373 -> 31
    _rn_q(M, 'geo31-advanced-p13', 'In the accompanying figure, $AD\\perp BC$.\nGiven:\n'
          r'$\begin{cases} AB=30 \\ BD=24 \\ AC=\sqrt{373} \end{cases}$' '\nWhat is BC?',
          ['$37$', '$31$', '$7$', '$30$'], 2, [
        'ABD: $AB=30=6\\cdot5$ and $BD=24=6\\cdot4$, the triple 3-4-5 times $6$. Therefore $AD=6\\cdot3=18$.',
        'ADC: $DC^2=373-324=49$, therefore $DC=7$.',
        '$BC=BD+DC=24+7=31$.'], figure=_ap_fig_p13())

    # ---------- p14 (no numbers): the altitude to the base is shorter than a leg; choice order + example 4, 4, 7
    _rn_q(M, 'geo31-advanced-p14', 'Which of the following is necessarily true for every isosceles triangle?',
          ['Every altitude is also an angle bisector', 'The altitude to the base is shorter than each equal side',
           'All three angles are acute', 'Each equal side is longer than the base'], 2, [
        'The altitude to the base makes two right triangles. In each one, an equal side is the hypotenuse and the altitude '
        'is a leg. The hypotenuse is the longest side, therefore the altitude is shorter than an equal side.',
        'The others are not always true. Sides $4,\\ 4,\\ 7$: the equal sides are shorter than the base, and the triangle '
        'is obtuse ($7^2=49>4^2+4^2=32$). Only the altitude to the base is also a bisector.'])

    # ---------- p15 (letters): A, C, B / E, F, D, angle 2t  ==>  K, M, L / P, R, N, angle 2k
    _rn_q(M, 'geo31-advanced-p15', 'K, M and L lie on one line. MP bisects angle KMN, and MR bisects angle NML. P and R lie '
          'on these bisectors. Given: angle MPR is $2k$. Which expression equals angle PRM?',
          ['$90°-k$', '$180°-2k$', '$90°-2k$', '$2k$'], 3, [
        '$\\angle KMN+\\angle NML=180°$. Their halves: $\\angle PMN+\\angle NMR=90°$, therefore $\\angle PMR=90°$.',
        'Triangle PMR: $\\angle PRM=180°-90°-2k=90°-2k$.'])
    _rn_fig(M, 'geo31-advanced-p15', _rn_svg_sub([_rn_label('A', 'K'), _rn_label('C', 'M'), _rn_label('B', 'L'),
                                                  _rn_label('D', 'N'), _rn_label('E', 'P'), _rn_label('F', 'R'),
                                                  _rn_label('2t', '2k')]))

    # ---------- p16: reflex angle split into three (δ = 60° + (α+β)/3)  ==>  split into four, angles β, γ, θ
    _rn_q(M, 'geo31-advanced-p16', 'Two angles of a triangle are $\\beta$ and $\\gamma$. At the third vertex, the reflex '
          'angle outside the triangle (the reflex angle $=360°$ minus the interior angle) is divided into four equal angles, '
          'each measuring $\\theta$. Which expression equals $\\theta$?',
          ['$90°-\\frac{\\beta+\\gamma}{4}$', '$\\frac{\\beta+\\gamma}{4}$', '$45°+\\frac{\\beta+\\gamma}{4}$',
           '$45°-\\frac{\\beta+\\gamma}{4}$'], 3, [
        'The third angle: $180°-\\beta-\\gamma$.',
        'The reflex angle: $360°-(180°-\\beta-\\gamma)=180°+\\beta+\\gamma$.',
        '$\\theta=\\frac{180°+\\beta+\\gamma}{4}=45°+\\frac{\\beta+\\gamma}{4}$.',
        'Plug in: an equilateral triangle ($\\beta=\\gamma=60°$) has reflex angle $300°$, so $\\theta=75°$. '
        'Only $45°+\\frac{120°}{4}=75°$ fits.'])

    # ---------- p17: AB = 8, AC = 15 (8-15-17) -> 120/17  ==>  AB = 33, AC = 44 (3-4-5 × 11) -> 132/5
    _rn_q(M, 'geo31-advanced-p17', 'Triangle ABC is right at A, and AD is the altitude to BC.\nGiven:\n'
          r'$\begin{cases} AB=33' + C + r' \\ AC=44' + C + r' \end{cases}$' '\nWhat is AD (in cm)?',
          ['$\\frac{66}{5}$', '$22$', '$\\frac{55}{2}$', '$\\frac{132}{5}$'], 4, [
        '$BC=55$: the triple 3-4-5 times $11$, or $\\sqrt{1089+1936}=\\sqrt{3025}$.',
        'Area two ways: $\\frac{33\\cdot44}{2}=\\frac{55\\cdot AD}{2}$, therefore $55\\cdot AD=1452$ and $AD=\\frac{1452}{55}=\\frac{132}{5}$.',
        'Traps: $\\frac{55}{2}$ is half the hypotenuse (the median, not the altitude), and $\\frac{66}{5}$ forgets to double the area.'],
          figure=_ap_fig_p17())

    # ---------- p18: side opposite the obtuse angle 8 -> sum 10  ==>  11 -> sum 15
    _rn_q(M, 'geo31-advanced-p18', 'The side opposite an obtuse angle of a triangle is 11 cm long. Which of the following '
          'could be the sum of the other two side lengths (in cm)?',
          ['$22$', '$11$', '$24$', '$15$'], 4, [
        'Triangle rule: the other two sides together are more than $11$.',
        'The obtuse angle is the largest angle, therefore $11$ is the longest side. Each other side is less than $11$, '
        'and their sum is less than $22$.',
        'Only $15$ is between $11$ and $22$. Example: $7,\\ 8,\\ 11$. The obtuse test: $11^2=121>7^2+8^2=113$ ✓.'])

    # ---------- p19: 2p + q + 42°, p + 2q + 66° -> 84°  ==>  2p + q + 46°, p + 2q + 50° -> 88°
    _rn_q(M, 'geo31-advanced-p19', 'One triangle has angles $2p$, $q$ and 46°. Another has angles $p$, $2q$ and 50°. '
          'What is $p+q$?',
          ['$92°$', '$76°$', '$88°$', '$100°$'], 3, [
        'Angle sums: $\\begin{cases} 2p+q+46°=180° \\\\ p+2q+50°=180° \\end{cases}$, that is '
        '$\\begin{cases} 2p+q=134° \\\\ p+2q=130° \\end{cases}$',
        'Add the two equations: $3p+3q=264°$, therefore $p+q=88°$.'])

    # ---------- p20 (letters): A, B, C, D, t  ==>  P, Q, R, S, k
    _rn_q(M, 'geo31-advanced-p20', 'In the accompanying figure, PS bisects angle QPR.\nGiven:\n'
          r'$\begin{cases} PR=QR \\ PQ\parallel RS \\ \angle PRQ=2k \end{cases}$' '\nWhich expression equals x?',
          ['$45°-\\frac k2$', '$90°-2k$', '$55°-k$', '$120°-\\frac k3$'], 1, [
        '$PR=QR$, therefore $\\angle QPR=\\angle PQR=\\frac{180°-2k}{2}=90°-k$.',
        'PS bisects angle P: $\\angle QPS=\\frac{90°-k}{2}=45°-\\frac k2$.',
        'Alternate angles ($PQ\\parallel RS$): $x=\\angle QPS=45°-\\frac k2$.'])
    _rn_fig(M, 'geo31-advanced-p20', _rn_svg_sub([_rn_label('A', 'P'), _rn_label('B', 'Q'), _rn_label('C', 'R'),
                                                  _rn_label('D', 'S'), _rn_label('2t', '2k')]))


# ====================================================================================================
# ---- renumber pass, practice clean-up (approved): copies, extra warm-ups beyond 3, September items the Hebrew covers


def rn_zz(M):
    out = ['q-r26-t31-12',            # copy of geo31-advanced-p01 (same stem: "not necessarily equilateral")
           'geo31-foundation-p26',    # copy of geo31-foundation-p10 (a median halves the area)
           # English extra warm-ups: keep 3 (foundation-p22, advanced-p23, advanced-p27)
           'geo31-foundation-p21', 'geo31-foundation-p23', 'geo31-foundation-p24', 'geo31-foundation-p25',
           'geo31-foundation-p27', 'geo31-advanced-p21', 'geo31-advanced-p22', 'geo31-advanced-p24',
           'geo31-advanced-p25', 'geo31-advanced-p26',
           # September items whose type the Hebrew practice already has
           'q-r26-t31-06',            # 30-30-120 / equilateral area: Hebrew foundation-p11, advanced-p11, p12
           'q-r26-t31-07',            # side opposite an obtuse angle: Hebrew advanced-p18
           'q-r26-t31-10']            # area two ways for an altitude: Hebrew advanced-p17 and p04
    for qid in out:
        assert M.section_of(qid) in (FOUND, ADV), qid
        M.unplace(qid)


def renumber_pass(M):
    rn_g1(M)    # guided g010 ... g028 + lesson / summary / card examples
    rn_g2(M)    # guided g031 ... g040
    rn_fp(M)    # foundation practice p01 ... p20
    rn_ap(M)    # advanced practice p01 ... p20
    rn_zz(M)    # practice clean-up (copies, extra warm-ups, September items) 63 -> 48
    _rn_titles(M)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


# ======================================================================================================
# 2026-10-07 methods spread (runs last). The 2026-10-06 methods (power count, compare by factors, mirror test, pick
# values that fit) are added where they really solve a question: a "Method N" line (a "Shortcut" line for pick values
# that fit, which is taught later, in topic 51) at the end of the written solution, and one extra slide in the
# clearest solution videos. Geometry is not recorded (checked ~/Documents/Course.recordings 2026-10-07).
# ======================================================================================================
def _sp_line(M, qid, line, drop=None):
    """Append one method line to a written solution (drop = a sentence the new line replaces)."""
    ex = list(M.q(qid).get('explanation') or [])
    if line in ex: return
    if drop:
        assert any(drop in e for e in ex), (qid, drop)
        ex = [e.replace(drop, '') for e in ex]
    M.set_q(qid, expl=ex + [line])


def _sp_slide(M, qid, after_n, title, script):
    """One extra method slide in a solution video; the question (with its figure) is pre-loaded as on slide 2."""
    vid = 'solve-' + qid
    assert M.video(vid)['questionId'] == qid, vid
    s2 = M.slide(vid, 2)
    M.insert_slides(vid, after_n, [dict(mode='question', active=s2['active'], title=title,
                                        pre=[dict(it) for it in s2['items'][:s2['pre']]], script=script)])


def _sp_say_after(M, vid, n, start, line):
    """Insert one spoken line after the spoken line that starts with `start` (slide n)."""
    def fn(ls):
        k = next(j for j, l in enumerate(ls) if (l.get('say') or '').startswith(start))
        return ls[:k + 1] + [{'say': line}] + ls[k + 1:]
    if any(l.get('say') == line for l in M.slide(vid, n)['lines']): return
    M.edit_lines(vid, n, fn)


def spread_methods(M):
    # Q2 (m + n/2, angles at A and C equal): the figure is free -> pick values that fit (topic 51, later) + slide
    _sp_line(M, 'geo31-g011', r'Shortcut · Pick values that fit: the figure does not fix $k$, and the question expects one number, so any $k$ that fits will do. Take $k=60°$ (an equilateral triangle): $m=180°-60°=120°$ and $n=60°+60°=120°$. $m+\frac n2=120°+60°=180°$.')
    _sp_slide(M, 'geo31-g011', 2, 'Shortcut · Pick values that fit', [
        "One more way. The figure doesn't fix k — and the question expects one number. So any k that fits gives the same answer.",
        A("'k = 60°: an equilateral triangle' appears", T(r'$k=60°$: an equilateral triangle', size=34, x=1060, y=250, w=470)),
        "Take the easiest: k is 60. Then all three angles are 60 — an equilateral triangle.",
        A("'m = 120°, n = 120°' appears", T(r'$m=180°-60°=120°$, $\ n=60°+60°=120°$', size=30, x=1060, y=330, w=470)),
        "m is next to the 60 at A — 120. n is the outside angle at B: 60 plus 60 — 120 too.",
        A("'m + n/2 = 120° + 60° = 180°' appears", T(r'$m+\frac n2=120°+60°=180°$', size=34, x=1060, y=410, w=470)),
        "120, plus half of 120 — 180.",
        D('Circle choice 3'),
        "Choice three. Same answer — and no letters at all."])
    # Q15 (ADEC in an equilateral triangle): DBE is ABC at half size -> compare by factors (area x 1/4)
    _sp_line(M, 'geo31-g018', r'Method 2 · Compare by factors: DBE is ABC with every side $\times\frac12$, so its area is $\times\left(\frac12\right)^2=\frac14$. ADEC is the other $\frac34$: $\frac34\cdot\frac{100\sqrt3}{4}=\frac{75\sqrt3}{4}$.')


_apply_before_spread = apply


def apply(M):
    _apply_before_spread(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last


# =====================================================================================
# 2026-10-07 study-plan order: students meet the topics in the STUDY PLAN order (src/lib/planData.ts ORDER), not
# by topic number. A named method used before the topic that teaches it (in the plan) becomes a self-contained
# "Shortcut · <name>: <why>" line; a "Shortcut" whose method the plan already taught becomes a normal
# "Method N · <name>" line. Unrecorded videos only. Runs LAST.
# =====================================================================================

def _po_line(M, qid, start, new):
    ex = list(M.q(qid)['explanation'])
    k = [i for i, l in enumerate(ex) if l.startswith(start)]
    assert len(k) == 1, (qid, start, k)
    ex[k[0]] = new
    M.set_q(qid, expl=ex)


def _po_relabel(M, qid, old, name):
    import re as _re
    ex = list(M.q(qid)['explanation'])
    k = [i for i, l in enumerate(ex) if l.startswith(old)]
    assert len(k) == 1, (qid, old, k)
    used = [int(n) for l in ex for n in _re.findall(r'^Method (\d+) ·', l)]
    rest = ex[k[0]][len(old):].lstrip()
    if _re.match(r'[A-Z][a-z]', rest): rest = rest[0].lower() + rest[1:]
    ex[k[0]] = 'Method %d · %s: %s' % (max(used) + 1 if used else 2, name, rest)
    M.set_q(qid, expl=ex)


def _po_say(M, vid, n, old, new):
    """Replace the spoken line `old` (exact) on slide n with `new` (a string, or a list of strings)."""
    b = M.slide(vid, n)
    k = [i for i, l in enumerate(b['lines']) if l.get('say') == old]
    assert len(k) == 1, (vid, n, old)
    M.edit_lines(vid, n, lambda ls: ls[:k[0]] + [{'say': s} for s in ([new] if isinstance(new, str) else new)] + ls[k[0] + 1:])


def plan_order_fix(M):
    # Topic 31 (days 1-5) comes before topic 26 (compare by factors, day 26) in the plan.
    _po_line(M, 'geo31-g018', 'Method 2 · Compare by factors:', "Shortcut · Compare by factors: an area is a length times a length, so when every side is multiplied by a number, the area is multiplied by that number squared. DBE is ABC with every side $\\times\\frac12$, so its area is $\\times\\left(\\frac12\\right)^2=\\frac14$. ADEC is the other $\\frac34$: $\\frac34\\cdot\\frac{100\\sqrt3}{4}=\\frac{75\\sqrt3}{4}$.")


_apply_before_plan_order_fix = apply


def apply(M):
    _apply_before_plan_order_fix(M)
    plan_order_fix(M)   # 2026-10-07 study-plan order: runs last


# =====================================================================================
# 2026-10-07 method names: the method slides of this topic's unrecorded videos ("Method N · X") and the written
# solutions' "Method N · / Shortcut ·" labels use ONE short vocabulary (thinking methods of topic 51 + named
# techniques). Data and rules: _method_names.py (a video recorded before its CUTOFF keeps its old titles).
def _mn_load():
    import importlib.util, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_method_names.py')
    spec = importlib.util.spec_from_file_location('_method_names', p); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m


_apply_before_method_names = apply


def apply(M):
    _apply_before_method_names(M)
    _mn_load().method_names(M, 31)   # 2026-10-07 method names: runs last


# =====================================================================================
# 2026-10-08 coverage fixes (teacher approved 2026-10-08 "go ahead"): the WEAK / MISSING points of the Hebrew-vs-English
# coverage check of this topic, plus the teacher's decisions, as 1-4 short spoken lines (or one short slide) in
# UNRECORDED videos. A video with a take recorded before CF_CUTOFF (UTC; the time this change was finished) is left
# exactly as recorded. Helpers (lines_of / set_slide / replace_line / add_lines) come from _hebrew_back.py.
import importlib.util as _ilu_cf, os as _os_cf, re as _re_cf, glob as _glob_cf
_s_cf = _ilu_cf.spec_from_file_location('_hebrew_back_cf', _os_cf.path.join(_os_cf.path.dirname(_os_cf.path.abspath(__file__)), '_hebrew_back.py'))
CF = _ilu_cf.module_from_spec(_s_cf); _s_cf.loader.exec_module(CF)
CF_CUTOFF = '2026-10-08T08-47-24'


def _cf_recorded(vid):
    """True = a take of vid was recorded before CF_CUTOFF: leave the video as recorded."""
    pat = _re_cf.compile(_re_cf.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _glob_cf.glob(_os_cf.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_os_cf.path.basename(f))
        if m and m.group(1) < CF_CUTOFF: return True
    return False


def _cf_add(M, vid, title, anchor, new, where='after'):
    """add script lines after/before the one line containing anchor (None = end of the slide)."""
    if _cf_recorded(vid): return False
    return CF.add_lines(M, vid, title, anchor, new, where)


def _cf_replace(M, vid, title, sub, new):
    """replace the one line containing sub by new (a line, a list of lines, or [] = drop it)."""
    if _cf_recorded(vid): return False
    CF.set_slide(M, vid, title, CF.replace_line(CF.lines_of(M, vid, title), sub, new))
    return True


def fig_g025_cf():
    """g025 rebuilt on 5-12-13 (teacher 2026-10-08): AB = 15, BC = 39 -> AC = 36; AE = 48 -> CE = 60; ED = 60."""
    s = 4.5
    A = (190.0, 80.0)
    B = (A[0] - 15 * s, A[1]); Cc = (A[0], A[1] + 36 * s); E = (A[0] + 48 * s, A[1])
    D = (E[0] + 60 * s * 0.6, E[1] + 60 * s * 0.8)
    def rmark(c, p, q, k=12):
        u, v = _unit(c, p), _unit(c, q)
        a, b = (c[0] + u[0] * k, c[1] + u[1] * k), (c[0] + v[0] * k, c[1] + v[1] * k)
        m = (a[0] + v[0] * k, a[1] + v[1] * k)
        return _ln(a, m, TEAL, 1.7) + _ln(m, b, TEAL, 1.7)
    G1 = ((A[0] + B[0] + Cc[0]) / 3, (A[1] + B[1] + Cc[1]) / 3)
    G3 = ((E[0] + D[0] + Cc[0]) / 3, (E[1] + D[1] + Cc[1]) / 3)
    return _svg('0 0 640 360', 'A chain of three right triangles', [
        _poly(A, B, Cc), _poly(A, E, Cc), _poly(E, D, Cc),
        rmark(A, B, Cc), rmark(A, E, Cc), rmark(E, Cc, D),
        _tx((A[0] - 6, A[1] - 20), 'A'), _tx((B[0] - 16, B[1] - 10), 'B'), _tx((Cc[0] - 12, Cc[1] + 20), 'C'),
        _tx((E[0], E[1] - 20), 'E'), _tx((D[0] + 16, D[1] + 8), 'D'),
        _tx(((A[0] + B[0]) / 2, A[1] - 17), '15'), _tx(_g1_off(B, Cc, 20, G1), '39'),
        _tx(((A[0] + E[0]) / 2, A[1] - 17), '48'), _tx(_g1_off(E, D, 20, G3), '60'),
        _tx(_g1_off(Cc, D, 20, G3), 'x'),
    ])


def coverage_fixes(M):
    # ---- (1) 8-15-17: the real exams use it ~2 times in 760 questions -> not taught as a triple to know.
    #      geo-024: slide "8-15-17: less common" removed; "How to remember" keeps ONE line about rarer triples.
    if not _cf_recorded(V_TRIP):
        CF._TR.drop_slide(M, V_TRIP, '8-15-17: less common')
        sc = CF.lines_of(M, V_TRIP, 'How to remember')
        sc = CF.replace_line(sc, '8, 15, 17 — good to recognize too', [])
        sc = CF.replace_line(sc, 'Know 3, 4, 5 and hamsa', [
            'Know 3, 4, 5 and hamsa, bat mitzvah, bar mitzvah by heart.',
            "There are other triples, much rarer — like 8, 15, 17. No need to learn them: if one comes up, the ordinary calculation works."])
        CF.set_slide(M, V_TRIP, 'How to remember', sc)
    card = M.card('mem-triples')
    card['tables'][0]['rows'] = [r for r in card['tables'][0]['rows'] if '8:15:17' not in r[0]]
    card['tips'] = card['tips'] + ['Other triples (like 8, 15, 17) are rare on the exam — no need to learn them; Pythagoras works.']
    if not _cf_recorded('r26-t31-summary'):
        sc = CF.lines_of(M, 'r26-t31-summary', 'Triples')
        sc = CF.replace_line(sc, '3:4:5 · 5:12:13 · 8:15:17', A("'3:4:5 · 5:12:13' appears", T('$3:4:5$ · $5:12:13$', size=40)))
        sc = CF.replace_line(sc, '27:36:45 · 25:60:65 · 24:45:51', A("'Multiples: 27:36:45 · 25:60:65' appears", T('Multiples: $27:36:45$ · $25:60:65$', size=40)))
        CF.set_slide(M, 'r26-t31-summary', 'Triples', sc)
    # practice p09 keeps its numbers (17, 8 -> 15), but the solution now calculates instead of naming the triple
    ex = [e for e in M.q('geo31-foundation-p09')['explanation']]
    ex[0] = 'ABD is right at D, with $BD=8$ and $AB=17$: $AD^2=17^2-8^2=289-64=225$, therefore $AD=15$.'
    M.set_q('geo31-foundation-p09', expl=ex)
    #      g025 rebuilt on 5-12-13 x 3 (15, 39 -> 36), then 3-4-5 x 12 (36, 48 -> 60), then 60 root 2. Same type, same method.
    g = 'geo31-g025'
    _rn_q(M, g, choices=['$60$', '$120$', '$60\\sqrt2$', '$36\\sqrt2$'], correct=3, expl=[
        'ABC: $15=3\\cdot5$ and $39=3\\cdot13$, the triple 5-12-13 times $3$. Therefore $AC=3\\cdot12=36$.',
        'ACE: legs $36=12\\cdot3$ and $48=12\\cdot4$, the triple 3-4-5 times $12$. Therefore $CE=12\\cdot5=60$.',
        'CED: two legs of $60$. $CD^2=60^2+60^2=2\\cdot60^2$, therefore $CD=60\\sqrt2$.'], figure=fig_g025_cf())
    vid = 'solve-' + g
    if not _cf_recorded(vid):
        _rn_sub(M, vid, 2, [
            ('34 squared minus 16 squared', '39 squared minus 15 squared'),
            ('Next to AC write 30 (8-15-17 × 2)', 'Next to AC write 36 (5-12-13 × 3)'),
            ("16 and 34 are 8 and 17 times 2. It's 8, 15, 17 — so AC is 15 times 2: 30.",
             "15 and 39 are 5 and 13 times 3. It's 5, 12, 13 — so AC is 12 times 3: 36."),
            ('with legs 30 and 40.', 'with legs 36 and 48.'),
            ('After some practice, 30 and 40 should jump out as familiar: 3 times 10, 4 times 10.',
             'After some practice, 36 and 48 should jump out as familiar: 3 times 12, 4 times 12.'),
            ('Next to CE write 50 (3-4-5 × 10)', 'Next to CE write 60 (3-4-5 × 12)'),
            ("So CE is 5 times 10: 50. It's the 3, 4, 5 triple, scaled by 10.",
             "So CE is 5 times 12: 60. It's the 3, 4, 5 triple, scaled by 12."),
            ('No triple here — the legs are 50 and 50.', 'No triple here — the legs are 60 and 60.'),
            ('Write CD² = 50² + 50² = 2 · 50²', 'Write CD² = 60² + 60² = 2 · 60²'),
            ('50 squared plus 50 squared. Instead of adding to 5000, I write 2 times 50 squared',
             '60 squared plus 60 squared. Instead of adding to 7200, I write 2 times 60 squared'),
            ('Write CD = 50√2', 'Write CD = 60√2'),
            ('Take the root: root 2, and the root of 50 squared is 50. So CD is 50 root 2.',
             'Take the root: root 2, and the root of 60 squared is 60. So CD is 60 root 2.')])
        _rn_sub(M, vid, 3, [
            ('CD² = (34² − 16²) + 40² + 50²', 'CD² = (39² − 15²) + 48² + 60²'),
            ('$CD^2=(34^2-16^2)+40^2+50^2$', '$CD^2=(39^2-15^2)+48^2+60^2$'),
            ('AC squared is 34 squared minus 16 squared. Add 40 squared for CE squared. Add 50 squared for CD squared.',
             'AC squared is 39 squared minus 15 squared. Add 48 squared for CE squared. Add 60 squared for CD squared.'),
            ('900 plus 1600 plus 2500 — 5000. The root: 50 root 2.', '1296 plus 2304 plus 3600 — 7200. The root: 60 root 2.'),
            ('ratio 50, 50, 50 root 2', 'ratio 60, 60, 60 root 2')])

    # ---- (2) g040: the real exams never offer a ratio AND its reverse (checked: 0). Choice 4 (10/3) -> 3/8, the trap
    #      of adding a instead of taking it off (3b + a = 9a). Key unchanged (3/10).
    g = 'geo31-g040'
    _rn_q(M, g, choices=['$\\frac13$', '$1$', '$\\frac3{10}$', '$\\frac38$'], correct=3)
    ex = list(M.q(g)['explanation']) + ['Traps: $\\frac13$ forgets to take $a$ off the bottom ($3b=9a$); $\\frac38$ adds it ($3b+a=9a$).']
    M.set_q(g, expl=ex)
    vid = 'solve-' + g
    if not _cf_recorded(vid):
        t2, t3 = M.slide(vid, 2)['title'], M.slide(vid, 3)['title']
        sc = CF.lines_of(M, vid, t2)
        sc = CF.replace_line(sc, "you usually won't find both orders", [
            "It's clear the ratio is 3 to 10 or 10 to 3. And on the psychometric exam, you won't find both orders among the answers."])
        sc = CF.replace_line(sc, 'Cross out choices 1 and 2', D('Cross out choices 1, 2 and 4'))
        sc = CF.replace_line(sc, 'So the trick eliminates one third and 1', [
            'Only one answer is 3 to 10 or 10 to 3: 3 tenths. One third, 1 and 3 eighths are out.'])
        sc = CF.drop_lines(sc, 'Cross out choice 4', 'Then use the given a is smaller than b')
        CF.set_slide(M, vid, t2, sc)
        sc = CF.lines_of(M, vid, t3)
        sc = CF.drop_lines(sc, 'Cross out choice 4', 'Next: 10 thirds means a is 10')
        sc = CF.replace_line(sc, 'Next to choice 3 write', [
            D('Next to choice 4 write a = 3, b = 8: 24 − 3 = 21 ≠ 27, and cross it out'),
            '3 eighths: a is 3, b is 8. Bold line: 24 minus 3 — 21. Three times the small perimeter: three times 9 — 27. Not equal. Eliminated.',
            D('Next to choice 3 write a = 3, b = 10: 30 − 3 = 27 = 3 · 9 ✓')])
        sc = CF.replace_line(sc, "And one third? That's the trap", [
            "And the traps? One third forgets to take the small side off the bottom: 3b equals 9a. 3 eighths adds it instead: 3b plus a."])
        CF.set_slide(M, vid, t3, sc)

    # ---- (3) exterior-angle rule: kept, but "shows up a lot / core rule" -> "useful, saves time when it fits"
    _cf_replace(M, V_TRI, 'Two routes', 'This rule shows up a lot on the exam', ["A useful rule — it saves time when it fits."])
    if not _cf_recorded(V_TRI):
        sc = CF.lines_of(M, V_TRI, 'Recap')
        sc = CF.replace_line(sc, 'Underline the angle-sum line and the exterior-angle line', D('Underline the angle-sum line'))
        sc = CF.replace_line(sc, "The angle sum and the exterior angle are the ones you'll use most", [
            "Those are the rules. The angle sum is the one you'll use most — and the exterior angle saves time when it fits."])
        CF.set_slide(M, V_TRI, 'Recap', sc)
    c = M.card('mem-triangle-rules')
    c['intro'] = 'The general triangle rules. The angle sum is the one you will use most.'
    for r in c['tables'][0]['rows']:
        if r[0] == 'Exterior angle': r[2] = 'useful — saves time when it fits'
    vid = 'solve-geo31-g012'
    if not _cf_recorded(vid):
        t3 = M.slide(vid, 3)['title']
        sc = CF.lines_of(M, vid, t3)
        sc = CF.replace_line(sc, 'It comes up again and again — learn it too', [
            'And the exterior angle equals the two interior angles not next to it. You can always go the long way — but when it fits, the rule saves time.'])
        sc = CF.drop_lines(sc, 'You can always go the long way, but the rule saves time.')
        CF.set_slide(M, vid, t3, sc)


_apply_before_coverage_fixes = apply


def apply(M):
    _apply_before_coverage_fixes(M)
    coverage_fixes(M)   # 2026-10-08 coverage fixes: runs LAST


# =====================================================================================================================
# 2026-10-09 spoken labels -> speech (teacher: "take off words like 'notice:' that seem like I'm reading"): spoken
# lines that open with "Careful:", "Notice:", "Step one:", "The trap:"... are rewritten by hand in her spoken style, in
# place (same line count, cues unchanged). Data and rules: _spoken_labels.py (a video recorded before its CUTOFF keeps
# its old lines). Runs LAST.
# =====================================================================================================================
def _sl_load():
    import importlib.util, os, sys
    if '_spoken_labels' in sys.modules: return sys.modules['_spoken_labels']   # one copy: its WARN / CHANGED add up
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_spoken_labels.py')
    spec = importlib.util.spec_from_file_location('_spoken_labels', p); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); sys.modules['_spoken_labels'] = m
    return m


_apply_before_spoken_labels = apply


def apply(M):
    _apply_before_spoken_labels(M)
    _sl_load().spoken_labels(M, 31)   # 2026-10-09 spoken labels: runs LAST
