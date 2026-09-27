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
N = ['q-r26-t31-%02d' % k for k in range(1, 12)]
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
    _say(M, V_PYT, 3, "Let's see sample questions", None)
    M.insert_slides(V_PYT, 3, [dict(mode='concept', title='Acute or obtuse?', script=[
        "One more use of the squares — even when there's no right-angle mark.",
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
        "Let's see sample questions — first finding the hypotenuse, then a leg, then this test.",
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
    S('geo31-advanced-p01', choices=['A triangle with two angles of $60°$', 'A triangle in which one median is also an altitude',
                                     'An isosceles triangle with one angle of $60°$',
                                     'A triangle in which two different medians are also altitudes'], correct=2, expl=[
        'Choice 1: the third angle is $180°-60°-60°=60°$: equilateral.',
        'Choice 3: a $60°$ vertex angle gives base angles of $\\frac{180°-60°}{2}=60°$; $60°$ base angles give a third angle of $60°$: equilateral.',
        'Choice 4: each such median is a symmetry line, therefore two pairs of sides are equal: all three sides are equal.',
        'Choice 2: one symmetry line makes the triangle only isosceles. Example: sides $5,\\ 5,\\ 6$ — not equilateral.'])
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
    M.unplace('geo31-foundation-p26')      # third "median halves the area" question (p10 and adv-p08 stay)

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
        'geo31-foundation-p04', 'geo31-foundation-p10', 'geo31-foundation-p23', 'geo31-foundation-p15', 'geo31-foundation-p14',
        'geo31-foundation-p01', 'geo31-foundation-p02', 'geo31-foundation-p07', 'geo31-foundation-p12', 'geo31-foundation-p16',
        'geo31-foundation-p22', N[4], 'geo31-foundation-p05', 'geo31-foundation-p08', 'geo31-foundation-p13',
        'geo31-foundation-p17', 'geo31-foundation-p18', 'geo31-foundation-p19', 'geo31-foundation-p20', 'geo31-foundation-p03',
        'geo31-foundation-p21', 'geo31-foundation-p06', 'geo31-foundation-p24', 'geo31-foundation-p09', N[3],
        'geo31-foundation-p25', 'geo31-foundation-p11', N[5], 'geo31-foundation-p27'])
    M.practice_order(ADV, [
        'geo31-advanced-p03', 'geo31-advanced-p06', 'geo31-advanced-p27', 'geo31-advanced-p09', 'geo31-advanced-p14',
        'geo31-advanced-p01', 'geo31-advanced-p19', 'geo31-advanced-p15', 'geo31-advanced-p02', 'geo31-advanced-p11',
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
