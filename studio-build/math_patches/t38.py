"""Topic 38 - Geometric reasoning. Course review 2026-09 fixes.
See t38_CHANGES.md for the plain-language list."""
import math, re
import math_api
from math_api import VIS
from dsl import T, H, A, D, Q

TOPIC = 38
SHAPE, MINMAX, DIAG = 'geo-172', 'geo-175', 'geo-177'
LEARN, PRACT = 'geo38-learn-1', 'geo38-core-practice'
CARD = 'mem-geo-reasoning'

# ------------------------------------------------------------------ SVG helpers (same style as the course figures)
INK, TEAL, ORANGE, GRAY = '#203344', '#087f83', '#bb6821', '#9aa8c0'
FILL, FILL2, TFILL = '#e8eefb', '#eef4fb', '#d5f1ed'
FONT = 'DejaVu Sans,Arial,sans-serif'


def _svg(vb, label, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, label, label, ''.join(body)))


def _t(x, y, s, fill=INK, size=20, weight=None, anchor='middle'):
    w = ' font-weight="%s"' % weight if weight else ''
    return ('<text x="%.3f" y="%.3f" text-anchor="%s" dominant-baseline="middle" fill="%s" font-family="%s" '
            'font-size="%s"%s>%s</text>' % (x, y, anchor, fill, FONT, size, w, s))


def _ln(x1, y1, x2, y2, stroke=INK, w=2.5, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="%s"%s/>' % (x1, y1, x2, y2, stroke, w, d)


def _poly(pts, fill=FILL, stroke=INK, w=2.5):
    return ('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>'
            % (' '.join('%.3f,%.3f' % p for p in pts), fill, stroke, w))


def _dot(x, y, r=3.2, fill=INK):
    return '<circle cx="%.3f" cy="%.3f" r="%s" fill="%s"/>' % (x, y, r, fill)


def _right(cx, cy, ux, uy, vx, vy, s=14, stroke=TEAL):
    """Right-angle mark at (cx, cy) between unit directions u and v."""
    p1 = (cx + s * ux, cy + s * uy); p2 = (p1[0] + s * vx, p1[1] + s * vy); p3 = (cx + s * vx, cy + s * vy)
    return _ln(*p1, *p2, stroke=stroke, w=1.7) + _ln(*p2, *p3, stroke=stroke, w=1.7)


# ---------- Q4: trapezoid PQRS, ST perpendicular to QR
def _trap(P, S, Q_, R, vb):
    T_ = (S[0], Q_[1])
    body = [_poly([P, Q_, T_, S], FILL, INK), _poly([T_, R, S], TFILL, TEAL),
            _right(T_[0], T_[1], 0, -1, 1, 0),
            _t(P[0] - 12, P[1] - 20, 'P'), _t(Q_[0] - 16, Q_[1] + 16, 'Q'), _t(R[0] + 16, R[1] + 16, 'R'),
            _t(S[0] + 12, S[1] - 20, 'S'), _t(T_[0], T_[1] + 23, 'T')]
    return _svg(vb, 'A trapezoid split by a perpendicular from an upper vertex', body)


# near-isosceles: the "first glance" drawing (the trapezoid is clearly bigger)
FIG_Q4 = _trap((190, 110), (350, 110), (130, 250), (410, 250), '70 64 400 235')
# the exaggerated drawing: QR stretched far to the right (the triangle is clearly bigger)
FIG_Q4_STRETCH = _trap((130, 110), (230, 110), (100, 250), (590, 250), '48 64 580 235')


# ---------- Q5: diameter AB and chord CD perpendicular to it
def _disk(cx_chord, vb='152.2 26.5 335.6 307.9'):
    ox, oy, r = 320.0, 180.0, 116.8
    h = math.sqrt(r * r - (cx_chord - ox) ** 2); top, bot = oy - h, oy + h
    a0 = math.pi; a1 = math.atan2(-(top - oy), cx_chord - ox)   # math angles (y up)
    arc = [(ox + r * math.cos(a0 + (a1 - a0) * k / 60), oy - r * math.sin(a0 + (a1 - a0) * k / 60)) for k in range(61)]
    left, right = (203.2 + cx_chord) / 2, (cx_chord + 436.8) / 2
    small = cx_chord > 380
    body = ['<circle cx="320.000" cy="180.000" r="116.800" fill="%s" stroke="%s" stroke-width="2.5"/>' % (FILL, INK),
            _poly([(cx_chord, oy)] + arc + [(cx_chord, top)], TFILL, 'none'),
            _ln(203.2, oy, 436.8, oy), _ln(cx_chord, top, cx_chord, bot),
            _right(cx_chord, oy, 1, 0, 0, -1, s=8.76),
            _t(184.2, oy, 'A'), _t(455.8, oy, 'B'), _t(cx_chord + 15, top - 17, 'C'), _t(cx_chord + 15, bot + 18, 'D'),
            _t(left, 136.2, 'I', size=21), _t(left, 223.8, 'II', size=21),
            _t(right, 204 if small else 209.2, 'III', size=19 if small else 21),
            _t(right, 156 if small else 150.8, 'IV', size=19 if small else 21)]
    return _svg(vb, 'A horizontal diameter and a perpendicular chord divide a disk into four regions', body)


FIG_Q5 = _disk(327.0)           # CD almost through the center: "all four look like quarters"
FIG_Q5_EXAG = _disk(392.0)      # CD pushed toward B


# ---------- the rods picture: two fixed sides, the angle between them opens
def _rods():
    B = (260.0, 330.0); C = (580.0, 330.0); L = 200.0
    pts = {a: (B[0] + L * math.cos(math.radians(a)), B[1] - L * math.sin(math.radians(a))) for a in (50, 90, 130)}
    col = {50: TEAL, 90: ORANGE, 130: INK}
    body = [_ln(90, pts[50][1], 420, pts[50][1], GRAY, 1.6, '6 5'), _t(430, pts[50][1] - 2, 'same height', GRAY, 19, anchor='start')]
    for a in (130, 90, 50):
        X = pts[a]
        body += [_ln(X[0], X[1], C[0], C[1], col[a], 1.8, '7 5'), _ln(B[0], B[1], X[0], X[1], col[a], 3), _dot(X[0], X[1], 4.5, col[a])]
    body += [_ln(B[0], B[1], C[0], C[1], INK, 3), _dot(*B, r=4), _dot(*C, r=4),
             _t(pts[50][0] + 26, pts[50][1] - 18, '50°', TEAL, 20, '700'),
             _t(pts[90][0] + 30, pts[90][1] - 6, '90°', ORANGE, 20, '700'),
             _t(pts[130][0] - 30, pts[130][1] - 18, '130°', INK, 20, '700'),
             _t(B[0] - 12, B[1] + 20, 'B', size=22), _t(C[0] + 12, C[1] + 20, 'C', size=22),
             _t(420, B[1] + 22, '8', ORANGE, 20, '700'), _t(238, 225, '5', ORANGE, 20, '700')]
    return _svg('60 100 620 262', 'Two fixed sides joined at B with the angle between them opening', body)


# ---------- slide the apex: same base, apex on a parallel line
def _apex():
    k, m = 120.0, 300.0; A_, B_ = (230.0, m), (390.0, m)
    body = [_ln(90, k, 620, k, INK, 2), _ln(90, m, 620, m, INK, 2), _t(74, k, 'k', size=21), _t(74, m, 'm', size=21)]
    for x, c, fl in ((150, TEAL, 'none'), (310, ORANGE, 'none'), (540, INK, 'none')):
        body.append(_poly([A_, B_, (x, k)], fl, c, 2.4))
    body += [_ln(310, k, 310, m, GRAY, 1.6, '6 5'), _right(310, m, 0, -1, 1, 0, s=12),
             _t(322, 210, 'h', ORANGE, 21, '700', 'start'),
             _dot(150, k, 4.5, TEAL), _dot(310, k, 4.5, ORANGE), _dot(540, k, 4.5, INK),
             _t(150, k - 22, 'P₁', TEAL, 22, '700'), _t(310, k - 22, 'P₂', ORANGE, 22, '700'), _t(540, k - 22, 'P₃', INK, 22, '700'),
             _t(A_[0] - 6, m + 22, 'A', size=22), _t(B_[0] + 6, m + 22, 'B', size=22)]
    return _svg('50 80 600 255', 'Triangles with the same base AB and apexes on a line parallel to AB', body)


# ---------- guided "slide the apex" question: trapezoid with its diagonals
def _trap_diag(shade=False):
    A_, D_, B_, C_ = (230.0, 100.0), (410.0, 100.0), (130.0, 280.0), (540.0, 280.0)
    t = 180.0 / 590.0; E = (A_[0] + t * 310, A_[1] + t * 180)
    body = [_poly([A_, D_, C_, B_], FILL, INK)]
    if shade:
        body += [_poly([A_, B_, E], TFILL, TEAL, 1.5), _poly([D_, C_, E], '#f6e3d2', ORANGE, 1.5)]
    body += [_ln(*A_, *C_, INK, 2), _ln(*B_, *D_, INK, 2), _poly([A_, D_, C_, B_], 'none', INK), _dot(*E),
             _t(A_[0] - 10, A_[1] - 18, 'A'), _t(D_[0] + 10, D_[1] - 18, 'D'),
             _t(B_[0] - 14, B_[1] + 16, 'B'), _t(C_[0] + 14, C_[1] + 16, 'C'), _t(E[0], E[1] - 22, 'E')]
    return _svg('100 66 470 240', 'A trapezoid with its two diagonals meeting at E', body)


# ---------- practice: P moves along a line parallel to AB
def _moving_p():
    k, m = 110.0, 270.0; A_, B_, P = (230.0, m), (390.0, m), (480.0, k)
    body = [_ln(90, k, 610, k, INK, 2), _ln(90, m, 610, m, INK, 2), _t(74, k, 'k', size=21), _t(74, m, 'm', size=21),
            _poly([A_, B_, P], FILL, TEAL, 2.4), _ln(P[0], k, P[0], m, GRAY, 1.6, '6 5'), _right(P[0], m, 0, -1, -1, 0, s=12),
            _dot(*P, r=4.5, fill=TEAL), _t(P[0], k - 20, 'P'), _t(A_[0] - 6, m + 20, 'A'), _t(B_[0] + 4, m + 20, 'B'),
            _t(310, m + 22, '6', ORANGE, 20, '700'), _t(P[0] + 14, 190, '4', ORANGE, 20, '700', 'start')]
    return _svg('50 72 580 230', 'Base AB on line m and a point P moving along the parallel line k', body)


# ---------- 2026-10-01: "farthest apart" slide: rectangle, circle, cylinder
def _farthest():
    body = []
    # rectangle: opposite corners
    R0 = (60.0, 110.0); R1 = (250.0, 230.0)
    body += [_poly([R0, (R1[0], R0[1]), R1, (R0[0], R1[1])], FILL, INK),
             _ln(R0[0], R1[1], R1[0], R0[1], ORANGE, 3), _dot(R0[0], R1[1], 4.5, ORANGE), _dot(R1[0], R0[1], 4.5, ORANGE),
             _t(155, 280, 'corner to corner', INK, 19)]
    # circle: the diameter, through the center
    cx, cy, r = 400.0, 170.0, 70.0
    body += ['<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s" stroke="%s" stroke-width="2.5"/>' % (cx, cy, r, FILL, INK),
             _ln(cx - r * 0.8, cy + r * 0.6, cx + r * 0.8, cy - r * 0.6, ORANGE, 3), _dot(cx, cy, 3.5),
             _dot(cx - r * 0.8, cy + r * 0.6, 4.5, ORANGE), _dot(cx + r * 0.8, cy - r * 0.6, 4.5, ORANGE),
             _t(cx, 280, 'through the center', INK, 19)]
    # cylinder: height and diameter make a right triangle
    x0, x1, top, bot, ry = 560.0, 680.0, 70.0, 230.0, 16.0
    xm = (x0 + x1) / 2
    body += ['<path d="M %.3f %.3f L %.3f %.3f A %.3f %.3f 0 0 0 %.3f %.3f L %.3f %.3f" fill="%s" stroke="%s" stroke-width="2.5"/>'
             % (x0, top, x0, bot, (x1 - x0) / 2, ry, x1, bot, x1, top, FILL, INK),
             '<ellipse cx="%.3f" cy="%.3f" rx="%.3f" ry="%.3f" fill="%s" stroke="%s" stroke-width="2.5"/>' % (xm, top, (x1 - x0) / 2, ry, FILL2, INK),
             '<path d="M %.3f %.3f A %.3f %.3f 0 0 1 %.3f %.3f" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="6 5"/>'
             % (x0, bot, (x1 - x0) / 2, ry, x1, bot, GRAY),
             _ln(x0, bot, x1, bot, TEAL, 2.2, '7 5'), _ln(x1, bot, x1, top, TEAL, 2.2),
             _right(x1, bot, -1, 0, 0, -1, s=12),
             _ln(x0, bot, x1, top, ORANGE, 3), _dot(x0, bot, 4.5, ORANGE), _dot(x1, top, 4.5, ORANGE),
             _t(x1 + 14, (top + bot) / 2, 'h', TEAL, 21, '700', 'start'), _t(xm, bot + 30, '2r', TEAL, 21, '700'),
             _t(xm, 280, 'h and 2r: Pythagoras', INK, 19)]
    return _svg('30 40 700 260', 'The greatest distance: corner to corner, through the center, and across a cylinder', body)


# ---------- 2026-10-01: practice, farthest point of a rectangle from E
def _rect_e():
    A_, B_, C_, D_ = (150.0, 110.0), (150.0, 250.0), (500.0, 250.0), (500.0, 110.0)
    E = (220.0, 250.0)
    body = [_poly([A_, B_, C_, D_], FILL, INK), _dot(*E, r=4.5),
            _t(A_[0] - 14, A_[1] - 16, 'A'), _t(B_[0] - 14, B_[1] + 18, 'B'), _t(C_[0] + 14, C_[1] + 18, 'C'),
            _t(D_[0] + 14, D_[1] - 16, 'D'), _t(E[0], E[1] + 22, 'E')]
    return _svg('110 76 430 210', 'Rectangle ABCD with point E on side BC', body)


# ---------- 2026-10-01: reworked figures (p02, p10, p16)
def _two_squares():
    """p02: squares ABCD and DEFG; triangle CFG shaded (C slides on line DC, parallel to GF)."""
    A_, B_, C_, D_ = (174.0, 75.714), (174.0, 284.286), (382.571, 284.286), (382.571, 75.714)
    E, F, G = (382.571, 159.143), (466.0, 159.143), (466.0, 75.714)
    body = [_poly([A_, B_, C_, D_], 'none', INK), _poly([C_, F, G], TFILL, TEAL, 2.2), _poly([D_, E, F, G], 'none', INK),
            _t(162, 57.714, 'A'), _t(160, 301.286, 'B'), _t(382.571, 306.286, 'C'), _t(369.571, 57.714, 'D'),
            _t(367.571, 170.143, 'E'), _t(484, 159.143, 'F'), _t(481, 57.714, 'G'), _t(501, 117.429, '2 cm')]
    return _svg('0 0 640 360', 'Two squares aligned along their top edges, with triangle CFG shaded', body)


def _par_squares():
    """p10: the same parallelogram; triangles ABE and HCD shaded."""
    A_, B_, C_, D_ = (215.0, 127.5), (75.0, 232.5), (425.0, 232.5), (565.0, 127.5)
    E, F, G, H = (215.0, 232.5), (320.0, 232.5), (320.0, 127.5), (425.0, 127.5)
    body = [_poly([A_, B_, C_, D_], 'none', INK),
            _poly([A_, E, F, G], FILL, INK), _poly([G, F, C_, H], FILL, INK),
            _poly([A_, B_, E], TFILL, TEAL), _poly([H, C_, D_], TFILL, TEAL),
            _t(203, 107.5, 'A'), _t(215, 255.5, 'E'), _t(320, 255.5, 'F'), _t(320, 105.5, 'G'), _t(425, 105.5, 'H'),
            _t(430, 254.5, 'C'), _t(580, 112.5, 'D'), _t(60, 248.5, 'B')]
    return _svg('0 0 640 360', 'A parallelogram containing two adjacent congruent squares, with two corner triangles shaded', body)


def _par_tri():
    """p16: B(0,0) C(5,0) A(6,6) D(11,6) E(0,6); u = 26 px."""
    u, ox, oy = 26.0, 150.0, 290.0
    P = lambda x, y: (ox + u * x, oy - u * y)
    A_, B_, C_, D_, E = P(6, 6), P(0, 0), P(5, 0), P(11, 6), P(0, 6)
    tick = lambda p, q, dx, dy: _ln((p[0] + q[0]) / 2 - dx, (p[1] + q[1]) / 2 - dy, (p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, TEAL, 1.8)
    body = [_poly([E, A_, B_], FILL, INK), _poly([B_, C_, D_, A_], 'none', INK),
            _right(E[0], E[1], 1, 0, 0, 1, s=13), _right(B_[0], B_[1], 1, 0, 0, -1, s=13),
            tick(E, A_, 0, 7), tick(E, B_, 7, 0),
            _t(A_[0], A_[1] - 20, 'A'), _t(B_[0] - 14, B_[1] + 16, 'B'), _t(C_[0] + 12, C_[1] + 18, 'C'),
            _t(D_[0] + 14, D_[1] - 14, 'D'), _t(E[0] - 18, E[1] - 12, 'E'), _t((B_[0] + C_[0]) / 2, B_[1] + 24, '5 cm')]
    return _svg('110 100 440 230', 'A parallelogram with a right isosceles triangle attached to side AB', body)


# ------------------------------------------------------------------ small helpers
_BRIT = [('practise', 'practice'), ('Practise', 'Practice'), ('metre', 'meter'), ('centre', 'center'), ('colour', 'color')]


def _us(t):
    for a, b in _BRIT: t = t.replace(a, b)
    return t


def _so(t):
    """'..., so x' / '... — so x' (so = therefore) -> '... . So, x'."""
    return re.sub(r'(,| —) so (?!that\b|often\b|much\b|many\b|far\b|on\b)(\w)', lambda mo: '. So, ' + mo.group(2), t)


def _script(M, vid, n):
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _replace_say(M, vid, n, old, new):
    """Replace the spoken line containing `old` by the line(s) `new` (str or list). new=None deletes it."""
    def fn(lines):
        out = []; hit = False
        for l in lines:
            if 'say' in l and old in l['say'] and not hit:
                hit = True
                for s in ([] if new is None else [new] if isinstance(new, str) else new): out.append({'say': s})
            else: out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def _set_fig(M, vid, n, svg):
    for it in M.slide(vid, n)['items']:
        if it.get('k') == 'q' and 'fig' in it: it['fig'] = {'type': 'geometry', 'svg': svg}
    M.touched_videos.add(vid)


def _lesson_actives(M, vid):
    k = 0
    for b in M.video(vid)['beats']:
        if b['mode'] == 'concept': b['active'] = k; k += 1


def _solution(M, qid, group_title, intro, slides, fig=False):
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=['Question %s.' % math_api._word(n)] + intro)]
    for s in slides:
        pre = [Q(qid, figw=0.56, figalign='left', **({'fig': {'type': 'geometry', 'svg': s[2]}} if len(s) > 2 else {}))] \
            if fig else [Q(qid)]
        beats.append(dict(mode='question', active=0, title=s[0], pre=pre, script=s[1]))
    v = M.new_video('solve-' + qid, TOPIC, group_title, ['Question %d' % n], beats, M.section_of(qid),
                    kind='solution', qid=qid)
    v['beats'][0]['title'] = group_title
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def R(x, y, t, size=34):
    """Board text in the right-hand column of a question slide that shows a figure."""
    return T(t, size=size, x=1060, y=y, w=470)


def W(y, t, size=36):
    """Board text under a question without a figure."""
    return T(t, size=size, x=410, y=y, w=1100)


# ==================================================================================== apply
def apply(M):
    S = M.set_q

    # ================================================================================
    # 1. WRONG RULES / MISLEADING WORDS
    # ================================================================================
    # --- Q9 (geo38-g183), slide 2: "60 degrees -> equilateral" is false for sides 3 and 6
    _replace_say(M, 'solve-geo38-g183', 2, 'A 60 degree angle would send us straight',
                 ["There's another way we learned: an anchor. Try 60 degrees.",
                  "Careful: sides 3 and 6 with 60 degrees between them are NOT an equilateral triangle. The sides aren't equal.",
                  "6 is twice 3. It's the 30-60-90 triangle: the right angle is at A, and AC is 3 root 3 — about 5.2."])
    _replace_say(M, 'solve-geo38-g183', 2, 'Here the angle is 75',
                 ["Our angle is 75 — wider than 60. The angle opened, and AC got even longer than 5.2.",
                  "Either way, AC is much longer than AB."])

    def q9s2(lines):
        # the anchor line gets its own board item
        k = next(i for i, l in enumerate(lines) if 'say' in l and "It's the 30-60-90" in l['say'])
        b = M.slide('solve-geo38-g183', 2)
        b['items'].append(R(0, 370, r'$60°$ with sides $3, 6$: a $30°$-$60°$-$90°$ triangle, $AC=3\sqrt3\approx5.2$', 30))
        lines.insert(k, {'appear': len(b['items']) - 1, 'label': "'60° with sides 3, 6: 30-60-90' appears"})
        return lines
    M.edit_lines('solve-geo38-g183', 2, q9s2)
    # slide 3: name the rods rule
    _replace_say(M, 'solve-geo38-g183', 3, "That's the angle-opening principle",
                 "That's the rods rule: two fixed sides — a wider angle between them makes a longer third side.")
    # slide 4: the height grows only up to 90 degrees
    _replace_say(M, 'solve-geo38-g183', 4, 'By the angle — exactly like before',
                 ["By the angle. The side of 3 leans at 75 in the first one, at 45 in the second.",
                  "Up to 90 degrees, the wider the angle, the taller the height. Both angles here are below 90."])
    _replace_say(M, 'solve-geo38-g183', 5, 'As it approaches 0, the height shrinks',
                 ["As it approaches 0, the height shrinks and shrinks — the area is just a hair above 0.",
                  "And past 90? The height shrinks again. 105 degrees gives the same height as 75 — the same area."])
    S('geo38-g183', figure=M.slide('solve-geo38-g183', 2)['items'][0]['fig']['svg'],   # H was cut off
      expl=['Take the 6-cm sides as bases. Then the area is $6\\cdot h$, where $h$ is the height from A (or from E).',
            'The side of 3 leans at $75°$ in ABCD and at $45°$ in EFGH. Up to $90°$, a wider angle gives a taller height. '
            'With $45°$, the height is $\\frac{3}{\\sqrt2}\\approx2.1$. With $75°$, it is more than that (and less than 3).',
            'Same base, taller height: ABCD has the greater area. Equal areas cannot be true: choice 1.',
            'The other claims are true: $AC>3=AB$ (triangle inequality), $AC>EG$ (a wider angle between the same sides), '
            'and both perimeters are $2(3+6)=18$.'])

    # --- Q3 (geo38-g176) video: rods rule instead of the wrong back-reference; one goodbye only (at the end)
    _replace_say(M, 'solve-geo38-g176', 3, 'Remember the start of the lesson',
                 'Remember the rods rule: two sides stay the same — the wider the angle between them, the longer the third side.')
    _replace_say(M, 'solve-geo38-g176', 4, "That's it for minimum–maximum — and that's the last",
                 "That's it for this anchor. One more question on the rods rule.")
    _replace_say(M, 'solve-geo38-g176', 4, 'What can I wish you', None)
    _replace_say(M, 'solve-geo38-g176', 4, 'So — go up and succeed', None)
    S('geo38-g176', expl=['Anchor: if $\\alpha$ were $90°$, the side opposite it would be 15, because $9, 12, 15$ is the triple $3, 4, 5$ times 3.',
                          'The side is 16, longer than 15. Two fixed sides (9 and 12) with a longer third side: the angle between them opened. So, $\\alpha>90°$.',
                          'Check: $16^2=256>9^2+12^2=225$.'])

    # --- "Move the vertex away": only when the vertex moves straight away
    sc = _script(M, MINMAX, 3)
    j = next(i for i, x in enumerate(sc) if isinstance(x, tuple) and x[0] == 'A' and x[2].get('k') == 't')
    sc[j] = A(sc[j][1], dict(sc[j][2], t='The vertex moves straight away from the segment $\\rightarrow$ the angle gets smaller'))
    k = next(i for i, x in enumerate(sc) if isinstance(x, str) and x.startswith('If I move the vertex away'))
    sc[k] = 'If I move the vertex straight away, along the dashed line — and away again — the angle gets smaller and smaller. It closes.'
    sc.insert(k + 1, "Careful: 'straight away' matters. A point that is farther, but off to the side, is a different story.")
    M.set_slide(MINMAX, 3, script=sc)

    # --- Q4 (geo38-g178): the first drawing is near-isosceles, the exaggerated one is stretched
    S('geo38-g178', figure=FIG_Q4,
      expl=['Both regions have height ST. Trapezoid PQTS: $\\frac{(PS+QT)\\cdot ST}{2}$. Triangle STR: $\\frac{TR\\cdot ST}{2}$.',
            'Compare $TR$ with $PS+QT$. The givens do not fix TR (QR can be stretched to the right).',
            'Example: $PS=3$, $QT=4$, $ST=3$: the trapezoid is 10.5. $TR=2$ gives a triangle of 3, $TR=7$ gives 10.5, '
            '$TR=10$ gives 15. All three cases happen, so none of the claims must be true: choice 4.'])
    _set_fig(M, 'solve-geo38-g178', 2, FIG_Q4)
    for n in (3, 4, 5): _set_fig(M, 'solve-geo38-g178', n, FIG_Q4_STRETCH)
    _replace_say(M, 'solve-geo38-g178', 3, 'Look at the legs PQ and SR',
                 "In the first drawing, the legs PQ and SR looked about equal — but nobody said the trapezoid is isosceles.")

    def q4s3(lines):
        for l in lines:
            if 'draw' in l and 'Extend QR' in l['draw']: l['draw'] = 'Point at the stretched base QR and the long leg SR'
        return lines
    M.edit_lines('solve-geo38-g178', 3, q4s3)
    _replace_say(M, 'solve-geo38-g178', 3, 'For example: stretch the base QR',
                 "For example: stretch the base QR — really stretch it to the right, like here. The leg SR gets much longer.")

    # --- Q5 (geo38-g179): the question figure really looks like four quarters; slides 3-4 show the exaggerated one
    S('geo38-g179', figure=FIG_Q5,
      expl=['AB is a diameter, and a diameter is a line of symmetry. Reflect across AB: I goes onto II, and IV goes onto III. So, I = II and III = IV (Ava is right).',
            'I + IV is half the disk (above AB). Since IV = III, I + III is also half the disk, and so is II + IV. Mia is right.',
            'CD is only a chord. Push it toward B: III becomes tiny while II stays large. II = III need not be true. Answer: Ava and Mia only, choice 3.'])
    _set_fig(M, 'solve-geo38-g179', 2, FIG_Q5)
    for n in (3, 4): _set_fig(M, 'solve-geo38-g179', n, FIG_Q5_EXAG)
    _replace_say(M, 'solve-geo38-g179', 3, 'Look at the exaggerated picture',
                 "Look at the exaggerated picture: CD is close to B. Two is big, three is tiny. Before, they only looked equal.")

    # --- Q12 (box cut): "edges" means box edges here -> "extremes"
    b = M.slide('solve-geo38-g186', 3)
    for it in b['items']:
        if it.get('t') and 'edges' in it['t']: it['t'] = 'Answers $10, 11, 12, 15$ · the extremes: $10$ and $15$'
    for n in (3, 4, 5):
        def ext(lines):
            for l in lines:
                for key in ('say', 'label'):
                    if key in l:
                        l[key] = (l[key].replace('Here the edges are', 'Here the extremes are').replace('at the edges', 'at the extremes')
                                  .replace("there's our edge", "there's our extreme").replace('edges: 10 and 15', 'extremes: 10 and 15'))
            return lines
        M.edit_lines('solve-geo38-g186', n, ext)

    # ================================================================================
    # 2. MISSING METHODS
    # ================================================================================
    # --- (a) rods rule + greatest area, in the Minimum and Maximum lesson (after "Stretch the segment")
    M.insert_slides(MINMAX, 4, [
        dict(mode='concept', title='Two rods', script=[
            "Now a situation the exam loves: two sides that don't change, and the angle between them changes.",
            A('Rods figure appears', VIS(_rods(), w=1000, h=520)),
            "Picture two rods joined at B: one of length 5, one of length 8. I open the angle between them.",
            "50 degrees, 90 degrees, 130 degrees. Look at the dashed lines — the third side.",
            A("'Wider angle → longer third side' appears",
              T('Same two sides, wider angle $\\rightarrow$ longer third side', size=36, x=410, y=640)),
            "The wider the angle, the longer the third side. Always.",
            "The height is different. It grows only up to 90 degrees. At 90, the rod of 5 stands straight up — that's the tallest.",
            "Past 90, the rod leans the other way, and the height shrinks again.",
            A("'50° and 130°: the same height' appears",
              T('Height and area: greatest at $90°$ · $\\theta$ and $180°-\\theta$ give the same area', size=36, x=410, y=710)),
            "Look at 50 and 130: they reach the same dashed line. Same height, same area.",
            "Here's the trap: a wider angle does NOT always mean a bigger area. Only up to 90.",
        ]),
        dict(mode='concept', title='Greatest area', script=[
            "So what is the greatest possible area with two given sides?",
            A("'Sides 5 and 8: greatest area?' appears", T('Two sides $5$ and $8$. Greatest possible area?', size=44)),
            "Make the angle 90. Then one side is the base, and the other is the height.",
            A("'At 90°: 5·8/2 = 20' appears", T('At $90°$: $\\dfrac{5\\cdot8}{2}=20$', size=46)),
            "5 times 8 over 2: 20. Every other angle gives less than 20.",
            A("'Parallelogram with sides 5 and 8: at most 40' appears",
              T('Parallelogram with sides $5$ and $8$: at most $5\\cdot8=40$ (a rectangle)', size=40)),
            "A parallelogram with sides 5 and 8? At most 40 — when it's a rectangle.",
            "And the area can be as small as you like: close the angle, and the area goes down toward 0.",
        ])])
    # slides now: 1 title, 2 min-max, 3 vertex away, 4 stretch, 5 rods, 6 greatest area, 7 arc, 8 diameter, 9 anchor
    M.insert_slides(MINMAX, 9, [dict(mode='concept', title='Acute or obtuse?', script=[
        "The anchor you'll use most: the right angle. You can check it with the sides alone.",
        A("'Longest side c, the other sides a and b' appears", T('Longest side $c$, the other two sides $a$ and $b$:', size=40)),
        A("'c² = a² + b²: right' appears", T('$c^2=a^2+b^2$ $\\rightarrow$ a right angle', size=42)),
        "If c squared equals a squared plus b squared — Pythagoras — the angle opposite c is exactly 90.",
        A("'c² > a² + b²: obtuse' appears", T('$c^2>a^2+b^2$ $\\rightarrow$ an obtuse angle', size=42)),
        "If c is longer than that, the rods opened wider: the angle is obtuse.",
        A("'c² < a² + b²: acute' appears", T('$c^2<a^2+b^2$ $\\rightarrow$ all three angles are acute', size=42)),
        "If c is shorter, the angle closed: it's acute. And since it's the biggest angle, all three are acute.",
        A("'7, 8, 10' appears", T('$7, 8, 10$: $\\ 10^2=100<49+64=113$ $\\rightarrow$ acute', size=40)),
        "For example 7, 8 and 10. 100 is less than 113. All the angles are acute.",
        "Always use the LONGEST side as c.",
    ])])
    # 2026-10-01 elite comparison: the greatest DISTANCE (real exams: square, rectangle, polygon, cylinder)
    M.insert_slides(MINMAX, 6, [dict(mode='concept', title='Farthest apart', script=[
        "One more 'greatest': the greatest distance.",
        A('Farthest-apart figure appears', VIS(_farthest(), w=1000, h=420)),
        "Two points on a square or a rectangle. How far apart can they be? Push them to the ends: opposite corners. The diagonal.",
        "And from any point you choose, the farthest point of a square, a rectangle or any polygon is always a corner. Check the corners.",
        "In a circle, the farthest two points are the ends of a diameter. The line goes through the center.",
        A("'Polygon: a corner · circle: the diameter' appears",
          T('Polygon: the farthest point is a corner · circle: the diameter', size=36, x=410, y=590)),
        "A cylinder: go from the edge of the bottom to the opposite edge of the top. The height and the diameter make a right triangle.",
        A("'Cylinder: h = 9, r = 4' appears",
          T('Cylinder $h=9$, $r=4$: $\\sqrt{9^2+8^2}=\\sqrt{145}\\approx12.04$', size=36, x=410, y=660)),
        "Height 9, radius 4 — so the diameter is 8. 81 plus 64 is 145. The square root is just over 12.",
        "The trap: use the diameter, not the radius.",
        "And if the length must be a whole number? The longest is 12. 13 is already too long.",
    ])])
    M.set_sidebar(MINMAX, ['Min–max in geometry', 'Move the vertex away', 'Stretch the segment', 'Two rods', 'Greatest area',
                           'Farthest apart', 'Angles on an arc', 'Angle on a diameter', 'Min–max with an anchor', 'Acute or obtuse?'])
    _lesson_actives(M, MINMAX)

    # guided question: greatest area with two fixed sides (after Question 3)
    g1 = 'q-r26-t38-01'
    M.new_q(g1, TOPIC, 'Two sides of a triangle are 6 cm and 10 cm long. The angle between them can change. '
                       'What is the greatest possible area of the triangle?',
            ['$24$ cm²', '$30$ cm²', '$60$ cm²', '$15$ cm²'], 2,
            ['Take the side of 10 as the base. The area is $\\frac{10\\cdot h}{2}$, and the height $h$ is at most 6.',
             'The height is 6 exactly when the angle is $90°$. Then the area is $\\frac{10\\cdot6}{2}=30$.',
             'Trap: 24 is the area of the 6-8-10 right triangle. There, 10 is the hypotenuse, and the angle between 6 and 10 is not $90°$.'])
    M.place_q(g1, LEARN, after='solve-geo38-g176')
    _solution(M, g1, 'Minimum and Maximum Question', ['Two sides, and the angle is free.'], [
        ('Fix the base', [
            'Two sides of a triangle are 6 and 10. The angle between them can change. What is the greatest possible area?',
            'Two fixed sides, a free angle. That\'s the rods rule.',
            "Take 10 as the base. It doesn't change.",
            A("'Area = 10·h/2' appears", W(250, 'Area $=\\dfrac{10\\cdot h}{2}$', 40)),
            'So the area depends only on the height: the distance from the end of the 6 down to the base.',
        ]),
        ('Open the rod', [
            'Open the angle. At 90 degrees, the side of 6 stands straight up. The height is the whole 6.',
            'At any other angle, the side leans, and the height is less than 6.',
            A("'Greatest at 90°: h = 6' appears", W(330, 'Greatest at $90°$: $h=6$', 40)),
            A("'10·6/2 = 30' appears", W(410, '$\\dfrac{10\\cdot6}{2}=30$', 40)),
            '10 times 6 over 2: 30.',
            D('Circle choice 2'),
            'Choice two.',
        ]),
        ('The trap', [
            'The trap is 24. Students see 6 and 10 and think of the 6, 8, 10 triangle.',
            'But there, 10 is the hypotenuse. The angle between the 6 and the 10 is not 90.',
            A("'6, 8, 10: area 24 — not the greatest' appears", W(250, '$6, 8, 10$: area $24$ — not the greatest', 38)),
            'Here we choose the angle freely. So we make it 90 — and get 30.',
            "That's it for minimum and maximum. Next: diagrams that can change.",
        ])])

    # --- (b) Diagrams That Can Change: slide the apex + push to the extremes
    M.insert_slides(DIAG, 3, [
        dict(mode='concept', title='Slide the apex', script=[
            "One classic flexible diagram: the apex slides, and the area doesn't change.",
            A('Apex figure appears', VIS(_apex(), w=1000, h=520)),
            "Lines k and m are parallel. The base AB sits on m. The apex P can be anywhere on k.",
            "P one, P two, P three. Three very different triangles.",
            "But the height is always the distance between the parallel lines — h.",
            A("'Same base, apex on a parallel line → same area' appears",
              T('Same base, apex on a parallel line $\\rightarrow$ same height $\\rightarrow$ same area', size=36, x=410, y=640)),
            "Same base, same height — the same area. All three.",
            A("'The perimeter does change' appears", T('The perimeter DOES change', size=36, x=410, y=710)),
            "Careful: the perimeter does change. Slide P far away, and the sides get very long.",
            "You'll see this in a trapezoid too: the two top corners are on a line parallel to the base.",
        ]),
        dict(mode='concept', title='Push to the extremes', script=[
            "How do we exaggerate? Three moves to try.",
            A("'1 · Push the free point to the end' appears", T('1 · Push the free point to the end (the shape almost goes flat)', size=38)),
            "One: push the free point all the way to the end. The shape almost goes flat.",
            A("'2 · Put it in the middle' appears", T('2 · Put it in the middle (a symmetric shape)', size=38)),
            "Two: put it exactly in the middle. The shape becomes symmetric.",
            A("'3 · Find what is free' appears", T('3 · Find what is free: an angle, a side, a split', size=38)),
            "Three: find what the givens don't fix. An angle? A side? Where a segment is split?",
            "And if a claim survives all the extremes, it's usually a 'must'. Then look for the reason.",
        ]),
        # 2026-10-01 elite comparison: "cannot be determined" is almost never the answer in real geometry questions
        dict(mode='concept', title='Cannot be determined?', script=[
            "One choice you'll see a lot: 'It cannot be determined from the information given.'",
            A("''It cannot be determined': in geometry, almost never the answer' appears",
              T("'It cannot be determined' — in geometry, almost never the answer", size=38)),
            "In geometry, it's usually a trap. On real exams, it's almost never the right answer.",
            A("'Two legal figures, two different answers' appears",
              T('Before you choose it: draw TWO figures that keep every given and give TWO different answers', size=36)),
            "So before you choose it, test it. Draw two figures. Both must keep every given.",
            "If they give two different answers — then, and only then, it cannot be determined.",
            A("'Can't build them → the answer is fixed' appears",
              T("Can't build them? The answer is fixed. Find the reason: a height, a parallel line, a symmetry", size=36)),
            "Can't build two such figures? Then the answer is fixed. Look for the reason.",
            "Remember the apex that slides: three very different triangles — and always the same area. The height didn't change.",
            "The reason is usually like that: a height that doesn't change, a parallel line, or a symmetry.",
        ])])
    M.set_sidebar(DIAG, ['Must or could?', 'How to test a claim', 'Slide the apex', 'Push to the extremes', 'Cannot be determined?'])
    _lesson_actives(M, DIAG)

    # guided question: slide the apex in a trapezoid (before Question 4)
    g2 = 'q-r26-t38-02'
    M.new_q(g2, TOPIC, 'ABCD is a trapezoid with AD ∥ BC. Its diagonals AC and BD meet at E. '
                       'Which of the following statements is necessarily true?',
            ['The area of triangle ABE is greater than the area of triangle DCE.', '$AE=EC$',
             'The area of triangle ABE equals the area of triangle DCE.',
             'The area of triangle ABE equals the area of triangle AED.'], 3,
            ['Triangles ABC and DBC have the same base BC. A and D lie on AD, which is parallel to BC, so both triangles have the same height. Their areas are equal.',
             'Both triangles contain triangle EBC. Take it away from each: $S_{ABE}=S_{ABC}-S_{EBC}=S_{DBC}-S_{EBC}=S_{DCE}$. Choice 3.',
             'AE = EC only in a parallelogram. ABE = AED fails when AD is very short: AED almost disappears, and ABE does not.'],
            figure=_trap_diag())
    M.place_q(g2, LEARN, after=DIAG)
    _solution(M, g2, 'Reasoning Questions', ['A trapezoid and its diagonals.'], [
        ('Same base, same height', [
            'ABCD is a trapezoid, AD parallel to BC. The diagonals meet at E. Which statement must be true?',
            'Look for triangles with the same base and an apex on a parallel line.',
            D('Shade triangle ABC, then triangle DBC'),
            'Triangle ABC and triangle DBC. The same base: BC.',
            'A and D are both on line AD — parallel to BC. So the two apexes are at the same height.',
            A("'S(ABC) = S(DBC)' appears", R(0, 250, '$S_{ABC}=S_{DBC}$', 40)),
            'Same base, same height — the same area.',
        ]),
        ('Take away the shared part', [
            'Both triangles contain the same piece: triangle EBC.',
            A("'S(ABE) = S(ABC) − S(EBC)' appears", R(0, 250, '$S_{ABE}=S_{ABC}-S_{EBC}$', 36)),
            A("'S(DCE) = S(DBC) − S(EBC)' appears", R(0, 330, '$S_{DCE}=S_{DBC}-S_{EBC}$', 36)),
            'Equal areas, minus the same piece. What is left is equal: ABE equals DCE.',
            A("'S(ABE) = S(DCE)' appears", R(0, 420, '$S_{ABE}=S_{DCE}$', 42)),
            D('Circle choice 3'),
            'Choice three.',
        ], _trap_diag(shade=True)),
        ('Check the others', [
            'Choice one says ABE is bigger. We just saw they are always equal. Out.',
            'AE equals EC? That happens only when the diagonals cut each other in half — a parallelogram. Here AD is shorter than BC. Out.',
            'ABE equals AED? Exaggerate: make AD tiny. Triangle AED almost disappears, but ABE does not. Out.',
            A("'Short AD → AED almost disappears' appears", R(0, 250, 'Short $AD$ $\\rightarrow$ $S_{AED}\\approx0$', 36)),
            'Remember this picture: same base, apex on a parallel line.',
        ], _trap_diag(shade=True))], fig=True)
    _replace_say(M, 'solve-geo38-g178', 4, "Here we don't have enough givens",
                 ["Here we don't have enough givens to decide.",
                  "Notice: TR is free. Nothing in the givens fixes it. That's the 'find what is free' check."])

    # --- (c) Pass 2: the angle-bisector shortcut is removed (approved plan); the solution keeps its fixed text
    S('geo38-g184', expl=['Drop NE perpendicular to KM. Right triangles MNE and MNL have equal angles at M and the same hypotenuse MN. They are congruent, therefore NE = NL.',
                          'In right triangle KNE, KN is the hypotenuse, therefore KN > NE = NL. Choice 3.'])

    # --- (d) goodbye only at the very end (Question 13 video)
    _replace_say(M, 'solve-geo38-g187', 3, "That's it — we've finished geometric understanding",
                 ["That's it — we've finished geometric understanding, and in fact we've finished geometry altogether.",
                  "What can I wish you? That you do as well in the other topics as you do in geometry — and I'm waiting for you there too."])

    # --- (e) memory card: after the last guided question, covering the whole topic
    M.move(CARD, LEARN, after='solve-geo38-g187')
    c = M.card(CARD)
    rows = c['tables'][0]['rows']
    k = next(i for i, r in enumerate(rows) if r[0].startswith('Vertex moves away from the segment'))
    rows[k] = ['Vertex moves straight away from the segment', 'the angle gets smaller (nearer $\\rightarrow$ opens toward $180°$)']
    k = next(i for i, r in enumerate(rows) if 'Anchor' in r[0])
    rows[k + 1:k + 1] = [
        ['!Two fixed sides, the angle opens', 'the third side gets longer · the height and area grow up to $90°$, then shrink · $\\theta$ and $180°-\\theta$ give the same area'],
        ['Greatest area with sides $a$, $b$', 'at $90°$: triangle $\\frac{ab}{2}$, parallelogram $ab$'],
        ['!Greatest distance', 'polygon: a corner (square, rectangle: the diagonal) · circle: the diameter · cylinder: $\\sqrt{h^2+(2r)^2}$'],
        ['Acute, right or obtuse?', 'longest side $c$: $c^2=a^2+b^2$ right · $c^2>a^2+b^2$ obtuse · $c^2<a^2+b^2$ acute'],
        ['!Must / could / cannot', 'must = in every allowed case · could = in at least one · cannot = in none'],
        ['!Flexible drawing', 'exaggerate the drawing, but keep every given'],
        ['Extreme cases', '1 · push the free point to the end · 2 · put it in the middle · 3 · find what is free'],
        ['!Cannot be determined?', 'only if two figures that keep every given give two different answers · in geometry it is almost never the answer'],
        ['!Slide the apex', 'same base, apex on a parallel line $\\rightarrow$ the same area (the perimeter changes)'],
    ]
    c['tips'] = c['tips'] + ['Before you trust a drawing: which lengths and angles are really given?',
                             'The choices have a smallest and a largest value? Check the extremes first.']

    # ================================================================================
    # 3. TEXT
    # ================================================================================
    S('geo38-core-p03', expl=[
        'Try one example with coordinates: $A(0, 7)$, $C(0, 3)$, $E(0, 0)$, $B(4, 7)$, $D(2, 3)$, $F(8, 0)$. AB, CD and EF are all horizontal, so they are perpendicular to k.',
        'Check the right angle with Pythagoras: $BD^2=2^2+4^2=20$, $DF^2=6^2+3^2=45$, $BF^2=4^2+7^2=65=20+45$. So, ∠BDF = 90°.',
        'But $AB=4\\ne8=EF$, $AC=4\\ne3=CE$, and $BD=\\sqrt{20}\\ne\\sqrt{45}=DF$. None of the claims must be true: choice 4.'])
    S('geo38-core-p19', expl=[
        'Perimeter 28: every side is $\\frac{28}{4}=7$.',
        'Area = side × height: $h=\\frac{35}{7}=5$. A side of 7 that rises exactly 5 fixes how the rhombus leans. Leaning the other way gives a mirror image — the same rhombus.',
        'So there is exactly one rhombus: choice 1.'])
    S('geo38-core-p22', expl=['For a fixed perimeter, the rectangle closest to a square has the greatest area.',
                              'Each side of the square is $\\frac{36}{4}=9$. The greatest area is $9\\cdot9=81$ m².'])
    S('geo38-g174', expl=['Both plots are hexagons with the same area. The regular hexagon is more like a circle, so it needs less perimeter.',
                          'The nonregular hexagon has the greater perimeter: choice 3.'])
    S('geo38-g182', expl=['The center is 5 cm from A and from B. Cut P is $6-5=1$ cm from the center. Cut Q is $8-5=3$ cm from the center.',
                          'Each cut keeps the whole sphere surface and adds two flat disks. Closer to the center means a bigger disk: '
                          '$\\rho^2=25-1=24$ for P, $\\rho^2=25-9=16$ for Q.',
                          'Cut P gives the greater total: choice 2.'])

    # ================================================================================
    # 4. FIGURES
    # ================================================================================
    # v788: labels were cut off at the right edge and crossed by a line
    b = M.slide(MINMAX, 3)
    for it in b['items']:
        if it.get('k') == 'vis':
            s = it['v']['svg']
            s = s.replace('viewBox="141.4 4.0 409.5 370.0"', 'viewBox="141.4 4.0 580 370.0"')
            s = s.replace('x="380.0" y="252.0"', 'x="478.0" y="252.0"').replace('x="380.0" y="152.0"', 'x="478.0" y="152.0"')
            s = s.replace('x="380.0" y="37.0"', 'x="478.0" y="37.0"')
            s = s.replace('farther still: narrower', 'farthest: narrowest')
            it['v']['svg'] = s
    # p04: O label at the vertex
    q = M.q('geo38-core-p04'); s = q['questionVisual']['svg']
    S('geo38-core-p04', figure=s.replace('</svg>', _t(303, 220, 'O') + '</svg>'))
    # p06: the answer (the semicircle) was drawn
    s = M.q('geo38-core-p06')['questionVisual']['svg']
    S('geo38-core-p06', figure=re.sub(r'<path d="M 514\.667[^>]*/>', '', s))
    # p20: unexplained orange segment through O and E
    s = M.q('geo38-core-p20')['questionVisual']['svg']
    S('geo38-core-p20', figure=re.sub(r'<line x1="267\.440"[^>]*/>', '', s).replace('x="305.000" y="197.000"', 'x="320.000" y="200.000"')
      .replace('</svg>', _dot(360.091, 150.8) + '</svg>'))
    # p21: separate chords with their own distance lines; letters at the chord ends
    ox, oy, r, u = 320.0, 180.0, 121.667, 24.333
    ha, hc = math.sqrt(r * r - u * u), math.sqrt(r * r - 9 * u * u)
    S('geo38-core-p21', figure=_svg('0 0 640 360', 'Two chords at different distances from the center', [
        '<circle cx="320.000" cy="180.000" r="121.667" fill="none" stroke="%s" stroke-width="2.5"/>' % INK,
        _ln(ox - ha, oy - u, ox + ha, oy - u, TEAL), _ln(ox - hc, oy + 3 * u, ox + hc, oy + 3 * u, TEAL),
        _ln(ox, oy, ox, oy - u, ORANGE, 2.5, '7 5'), _ln(ox, oy, ox, oy + 3 * u, ORANGE, 2.5, '7 5'),
        _dot(ox, oy), _t(ox - 17, oy + 2, 'O'),
        _t(ox + 14, oy - u / 2, '1', ORANGE, 20, '700', 'start'), _t(ox + 14, oy + 1.5 * u, '3', ORANGE, 20, '700', 'start'),
        _t(ox - ha - 16, oy - u - 4, 'A'), _t(ox + ha + 16, oy - u - 4, 'B'),
        _t(ox - hc - 14, oy + 3 * u + 10, 'C'), _t(ox + hc + 14, oy + 3 * u + 10, 'D')]))

    # ================================================================================
    # 5. PRACTICE: remove repeats, add exam-level questions, order easy -> hard
    # ================================================================================
    # Pass 2: geo38-core-p18 and geo38-core-p26 are restored (text clean-up only); q-r26-t38-08 is removed.
    S('geo38-core-p18', stem='A square and a rectangle that is not a square both have perimeter 32 cm. Which of the following statements is necessarily true?',
      expl=['The square has side $\\frac{32}{4}=8$ and area $8\\cdot8=64$ cm².',
            'For a fixed perimeter, the square has the greatest area of all rectangles. The other rectangle is not a square, so its area is less than 64 (for example, $10\\cdot6=60$).',
            'The square has the greater area: choice 4.'])
    S('geo38-core-p26', expl=['Each of the 4 vertical lines meets each of the 3 horizontal lines exactly once: $4\\cdot3=12$ points.',
                              'Two vertical lines are parallel, and two horizontal lines are parallel, so they add no more points. The answer is 12: choice 1.'])
    NEW = [
        ('q-r26-t38-03', 'A parallelogram has sides 4 cm and 9 cm. Its angles can change. What is its greatest possible area?',
         ['$18$ cm²', '$26$ cm²', '$13$ cm²', '$36$ cm²'], 4,
         ['Take the side of 9 as the base. Area = $9\\cdot h$, and the height is at most the other side, 4.',
          'The height is 4 when the angle is $90°$ (a rectangle): $9\\cdot4=36$ cm².'], None),
        ('q-r26-t38-04', 'AB is a diameter of a circle. Point P is not on line AB, and ∠APB = 100°. Where is P?',
         ['On the circle', 'Inside the circle', 'Outside the circle', 'It cannot be determined from the information given.'], 2,
         ['On the circle, an angle on a diameter is exactly $90°$.',
          'Closer to AB (inside the circle), the angle opens: more than $90°$. Farther (outside), it closes: less than $90°$.',
          '$100°>90°$, therefore P is inside the circle.'], None),
        ('q-r26-t38-05', 'A triangle has side lengths 5 cm, 12 cm and $x$ cm, where $x$ is the longest side and $13<x<17$. '
                         'Which of the following is necessarily true about the angle opposite the side of length $x$?',
         ['It is obtuse.', 'It is a right angle.', 'It is acute.', 'It cannot be determined from the information given.'], 1,
         ['Anchor: $5, 12, 13$ is a right triangle ($25+144=169=13^2$).',
          'Here $x>13$, therefore $x^2>169=5^2+12^2$. The side opposite the angle is longer than in the right triangle, so the angle is obtuse.'], None),
        ('q-r26-t38-06', 'Lines k and m are parallel, and the distance between them is 4 cm. A and B lie on m, and AB = 6 cm. '
                         'Point P moves along line k. Which of the following is necessarily true about triangle ABP?',
         ['Its area and its perimeter do not change.', 'Its area is always 12 cm², and its perimeter changes.',
          'Its area changes, and its perimeter does not change.', 'Its area and its perimeter both change.'], 2,
         ['The base AB = 6 is fixed, and the height is always the distance between the lines, 4. Area: $\\frac{6\\cdot4}{2}=12$ cm², wherever P is.',
          'Slide P far along k: AP and BP get very long. The perimeter changes. Choice 2.'], _moving_p()),
        ('q-r26-t38-07', 'A cube is cut by one flat plane. Which of the following cannot be the shape of the cut face?',
         ['A triangle', 'A rectangle that is not a square', 'A regular hexagon', 'A shape with 7 sides'], 4,
         ['Each side of the cut face lies on one face of the cube, and the plane meets each face at most once. The cube has 6 faces, so the cut face has at most 6 sides.',
          'A triangle: cut off a corner. A rectangle that is not a square: cut through two opposite edges. A regular hexagon: cut through the center, straight across a long diagonal of the cube.',
          'A shape with 7 sides is impossible: choice 4.'], None),
        ('q-r26-t38-09', 'Triangle 1 has two sides of 5 cm and 8 cm with a 50° angle between them. '
                         'Triangle 2 has two sides of 5 cm and 8 cm with a 130° angle between them. Which of the following is true?',
         ['The areas are equal, and the third sides are equal.', 'The areas are equal, and triangle 2 has the longer third side.',
          'Triangle 2 has the greater area.', 'Triangle 1 has the greater area, and triangle 2 has the longer third side.'], 2,
         ['Take the side of 8 as the base. At $50°$ and at $130°$, the side of 5 leans by the same amount (to different sides), so it reaches the same height. Same base, same height: the areas are equal.',
          'The third side: the same two sides with a wider angle give a longer third side. $130°>50°$, therefore triangle 2 has the longer third side. Choice 2.'], None),
        ('q-r26-t38-10', 'Two sides of a triangle are 6 cm and 8 cm long. Which of the following cannot be the area of the triangle?',
         ['$12$ cm²', '$24$ cm²', '$25$ cm²', '$20$ cm²'], 3,
         ['The greatest area is at $90°$: $\\frac{6\\cdot8}{2}=24$.',
          'Closing the angle makes the area as small as we like, so every area between 0 and 24 is possible (12, 20 and 24 too).',
          '25 is more than 24: impossible. Choice 3.'], None),
        ('q-r26-t38-11', "A circle and a square have the same perimeter. What is the ratio of the circle's area to the square's area?",
         ['$\\pi:4$', '$1:1$', '$4:\\pi$', '$2:\\pi$'], 3,
         ['Plug in a convenient perimeter: $4\\pi$.',
          'Square: side $\\pi$, area $\\pi^2$. Circle: $2\\pi r=4\\pi$, so $r=2$ and the area is $4\\pi$.',
          'The ratio is $4\\pi:\\pi^2=4:\\pi$. Since $\\pi<4$, the circle is bigger, as shape efficiency says.'], None),
    ]
    for qid, stem, ch, cor, ex, fig in NEW:
        M.new_q(qid, TOPIC, stem, ch, cor, ex, figure=fig)
        M.place_q(qid, PRACT)

    # ================================================================================
    # 2026-10-01 elite comparison
    # (a) "cannot be determined": in real geometry questions it was offered 18 times and correct 0 times.
    #     p02, p10, p16 now have a real answer ("cannot be determined" stays as the tempting distractor);
    #     p08 is kept as the honest exception and shows the two-figures test.
    # ================================================================================
    CBD = 'It cannot be determined from the information given.'
    S('geo38-core-p02',
      stem='ABCD and DEFG are squares. E lies on DC, and their top sides AD and DG lie on one straight line. '
           'Given: FG = 2 cm. What is the area of triangle CFG (in cm²)?',
      choices=['$1$', '$2$', '$4$', CBD], correct=2, figure=_two_squares(),
      expl=['The big square is not given — but test before you choose "cannot be determined". Take GF as the base of triangle CFG: $GF=2$.',
            'The height is the distance from C to line GF. C lies on line DC. DE is the side of the small square opposite GF, so line DC is parallel to GF. '
            'The distance between them is $DG=2$, whatever the size of the big square.',
            'Area $=\\frac{2\\cdot2}{2}=2$ cm². Choice 2.',
            'Two figures check: big side 5 or big side 8 — C slides along line DC, and the area is 2 both times. The answer is fixed.'])
    S('geo38-core-p10',
      stem='ABCD is a parallelogram containing adjacent squares AEFG and GFCH, each with side 3 cm, as shown in the accompanying figure. '
           'How does the area of triangle HCD compare with the area of triangle ABE?',
      choices=['It is necessarily smaller.', 'It is necessarily equal.', 'It is necessarily greater.', CBD], correct=2,
      figure=_par_squares(),
      expl=['BE and HD are not given — but test before you choose "cannot be determined".',
            'In a parallelogram, $AD=BC$: $6+HD=BE+6$. Therefore, $HD=BE$.',
            'Both triangles are right triangles with legs 3 and the same second leg: $S_{ABE}=\\frac{3\\cdot BE}{2}=\\frac{3\\cdot HD}{2}=S_{HCD}$.',
            'Two figures check: $BE=1$ gives 1.5 and 1.5, $BE=5$ gives 7.5 and 7.5. The areas change, but they are always equal: choice 2.'])
    S('geo38-core-p16',
      stem='ABCD is a parallelogram with BC = 5 cm. A right isosceles triangle AEB is constructed externally on AB, '
           'with right angle E and area 18 cm². Given: EB ⟂ BC. What is the area of the parallelogram (in cm²)?',
      choices=['$30$', '$36$', '$30\\sqrt2$', CBD], correct=1, figure=_par_tri(),
      expl=['The triangle: $\\frac{EB\\cdot EA}{2}=18$ and $EB=EA$. So, $EB^2=36$ and $EB=EA=6$.',
            'AE and BC are both perpendicular to EB. Two lines perpendicular to the same line are parallel: $AE\\parallel BC$. '
            'So, A is exactly as far from BC as E is: the height of the parallelogram is $EB=6$.',
            'Area $=BC\\cdot h=5\\cdot6=30$ cm². Choice 1.',
            'Traps: $30\\sqrt2=5\\cdot AB$ is true only for a rectangle. And the angle is not free here — $EB\\perp BC$ fixes it ($\\angle ABC=45°$).'])
    S('geo38-core-p08',
      choices=['$24$ cm', '$32$ cm', '$36$ cm', CBD], correct=4,
      expl=['AC is the axis of symmetry, so it cuts BD in half at a right angle: each half is 3. But nothing says where AC is cut.',
            'This is the rare case where the answer really cannot be determined. The two-figures test proves it.',
            'Figure 1: AC is cut into $5+5$. All four sides are $\\sqrt{5^2+3^2}=\\sqrt{34}$. Perimeter $4\\sqrt{34}\\approx23.3$.',
            'Figure 2: AC is cut into $1+9$. The sides are $\\sqrt{1^2+3^2}=\\sqrt{10}$ and $\\sqrt{9^2+3^2}=3\\sqrt{10}$. Perimeter $8\\sqrt{10}\\approx25.3$.',
            'Both figures keep every given, and the perimeters are different. It cannot be determined: choice 4.'])

    # (b) the greatest distance: a corner, the diameter, the cylinder triangle
    M.new_q('q-r26-t38-12', TOPIC,
            'ABCD is a rectangle with AB = 4 cm and BC = 10 cm. E lies on BC, and BE = 2 cm. '
            'Point P moves along the sides of the rectangle. What is the greatest possible length of EP (in cm)?',
            ['$2\\sqrt5$', '$8$', '$4\\sqrt5$', '$2\\sqrt{29}$'], 3,
            ['The farthest point of a rectangle from E is one of its corners. Check all four.',
             '$EB=2$ and $EC=10-2=8$. $EA=\\sqrt{2^2+4^2}=\\sqrt{20}=2\\sqrt5$. $ED=\\sqrt{8^2+4^2}=\\sqrt{80}=4\\sqrt5\\approx8.9$.',
             'The greatest is $ED=4\\sqrt5$: choice 3.',
             'Trap: $2\\sqrt{29}$ is the diagonal AC. It joins two corners, but E is not a corner.'], figure=_rect_e())
    M.place_q('q-r26-t38-12', PRACT)
    M.new_q('q-r26-t38-13', TOPIC,
            'A closed can has the shape of a cylinder. Its height is 8 cm, and the radius of its base is 3 cm. '
            'What is the length of the longest straight stick that fits completely inside the can (in cm)?',
            ['$8$', '$\\sqrt{73}$', '$10$', '$14$'], 3,
            ['The longest stick goes from the edge of the bottom base, through the middle, to the opposite edge of the top base.',
             'It is the hypotenuse of a right triangle. The legs are the height, 8, and the diameter, $2\\cdot3=6$.',
             '$\\sqrt{8^2+6^2}=\\sqrt{100}=10$. Choice 3.',
             'Trap: $\\sqrt{73}=\\sqrt{8^2+3^2}$ uses the radius instead of the diameter.'])
    M.place_q('q-r26-t38-13', PRACT)
    P = lambda n: 'geo38-core-p%02d' % n
    M.practice_order(PRACT, [
        P(26), P(22), P(18), P(23), P(24), P(21), P(1), P(4), 'q-r26-t38-04', 'q-r26-t38-03', 'q-r26-t38-13', P(5), P(25),
        'q-r26-t38-05', 'q-r26-t38-12', P(20), P(13), P(14), 'q-r26-t38-06', P(9), P(6), P(7), 'q-r26-t38-07', P(2), P(10), P(16), P(8),
        'q-r26-t38-09', 'q-r26-t38-10', 'q-r26-t38-11', P(12), P(11), P(19), P(3), P(15), P(17)])

    summary(M)   # Pass 2: summary lesson right before the practice

    # ================================================================================
    # 6. CLEAN-UP: American spelling, "so" = therefore, hyphens in words on pre-loaded canvases
    # ================================================================================
    for f in [f for f in M.D['flow'] if f['topic'] == TOPIC]:
        if f['type'] == 'question':
            q = M.q(f['ref']); ex = q.get('explanation') or []
            new = [_so(e) for e in ex]
            if new != ex: S(f['ref'], expl=new)
        if f['type'] != 'video': continue
        v = M.video(f['ref']); ch = False
        for b in v['beats']:
            for key in ('canvas', 'loads'):
                if b.get(key):
                    nb = re.sub(r'(?<=\d)−(?=[a-z])', '-', b[key])
                    if nb != b[key]: b[key] = nb; ch = True
            for l in b['lines']:
                if 'say' in l:
                    ns = _so(_us(l['say']))
                    if ns != l['say']: l['say'] = ns; ch = True
        if ch: M.touched_videos.add(f['ref'])

    cut_repeats(M)   # 2026-10-05: always last



def _b(label, tex, size=40):
    """A board line that pops in (label = what the teacher sees in the script)."""
    return A("'%s' appears" % label, T(tex, size=size))


def summary(M):
    """Pass 2: a short summary lesson at the end of the learn section (after the memory card), right before the practice."""
    last = [f['ref'] for f in M.D['flow'] if f['section'] == LEARN][-1]
    sb = ['Shape efficiency', 'Moving the vertex', 'Angle on a diameter', 'Two fixed sides', 'Acute or obtuse?',
          'Must, could, cannot', 'Test a claim', 'Slide the apex', 'Before you practice']
    M.new_video('r26-t38-summary', TOPIC, 'Summary', sb, [
        dict(mode='title', title='Summary', script=[
            "A quick summary before you practice.",
            "The big ideas of geometric understanding — with almost no calculation."]),
        dict(title='Shape efficiency', active=0, script=[
            _b('Same perimeter → the more circle-like shape has more area', 'Same perimeter $\\rightarrow$ the more circle-like shape has MORE area', size=38),
            _b('Same area → the more circle-like shape has less perimeter', 'Same area $\\rightarrow$ the more circle-like shape has LESS perimeter', size=38),
            "The circle is the most efficient shape. The country rule: most land, least border.",
            "So read what is fixed — the perimeter or the area.",
            _b('P = 20: 1 · 9 = 9, 3 · 7 = 21, 5 · 5 = 25', '$P=20$: $\\ 1\\cdot9=9$, $\\ 3\\cdot7=21$, $\\ 5\\cdot5=25$'),
            "Rectangles: the closer to a square, the more area. Regular polygons: the more sides, the more like a circle."]),
        dict(title='Moving the vertex', active=1, script=[
            _b('Vertex moves straight away → the angle gets smaller', 'Vertex moves straight away $\\rightarrow$ the angle gets smaller'),
            "Move the vertex straight away from the segment, and the angle closes. Bring it closer, and it opens toward 180.",
            _b('Vertex fixed, segment longer → the angle gets bigger', 'Vertex fixed, segment longer $\\rightarrow$ the angle gets bigger'),
            "Keep the vertex and stretch the segment: the old angle sits inside the new one. Bigger.",
            "And the farther the vertex from an arc, the smaller the angle."]),
        dict(title='Angle on a diameter', active=2, script=[
            _b('On the circle: 90° · inside: > 90° · outside: < 90°', 'On the circle: $90°$ · inside: $>90°$ · outside: $<90°$'),
            "An angle resting on a diameter. With the vertex on the circle, it's exactly 90.",
            "Inside the circle, the vertex is closer: the angle opens, more than 90.",
            "Outside, it's farther: the angle closes, less than 90."]),
        dict(title='Two fixed sides', active=3, script=[
            _b('Wider angle → longer third side', 'Wider angle $\\rightarrow$ longer third side'),
            "Two rods that don't change, and the angle between them opens. The third side always gets longer.",
            _b('Greatest area at 90°: 6 · 9 ÷ 2 = 27', 'Greatest area at $90°$: $\\ \\frac{6\\cdot9}{2}=27$ · parallelogram $6\\cdot9=54$'),
            "The area is different. It grows only up to 90 degrees. At 90 it's the greatest.",
            _b('θ and 180° − θ: the same area', '$\\theta$ and $180°-\\theta$: the same area'),
            "Here's the trap: 40 and 140 degrees give the same height — the same area."]),
        dict(title='Acute or obtuse?', active=4, script=[
            _b('c² = a² + b² → right · c² > a² + b² → obtuse · c² < a² + b² → acute', '$c^2=a^2+b^2$ right · $c^2>a^2+b^2$ obtuse · $c^2<a^2+b^2$ acute', size=36),
            "The anchor you'll use most: the right angle. Compare with Pythagoras.",
            _b('6, 7, 9: 81 < 36 + 49 = 85 → acute', '$6,\\ 7,\\ 9$: $\\ 81<36+49=85$ $\\rightarrow$ acute'),
            "The longest side is longer than in the right triangle? Obtuse. Shorter? Acute.",
            "Always use the longest side as c."]),
        dict(title='Must, could, cannot', active=5, script=[
            _b('Must: in every allowed case', 'Must be true: in EVERY case the givens allow'),
            _b('Could: in at least one', 'Could be true: in at least ONE allowed case'),
            _b('Cannot: in none', 'Cannot be true: in NO allowed case'),
            "Read which one they're asking before you look at the choices.",
            "One allowed case where a claim fails — and 'must be true' is out."]),
        dict(title='Test a claim', active=6, script=[
            _b('Change the shape — keep every given', 'Change the shape — keep every given'),
            "The figure isn't necessarily drawn to scale. Trust the givens, not the picture.",
            _b('The end · the middle · what is free?', 'Push to the end · put it in the middle · find what is free'),
            "Exaggerate: push the free point to the end, then put it in the middle.",
            _b('Cannot be determined? Two legal figures, two answers', "'Cannot be determined'? Only with two legal figures and two different answers", size=36),
            "'It cannot be determined'? Only if you can draw two figures that keep every given and give two different answers.",
            "In geometry, it's almost never the answer. Can't build the two figures? Find the reason the answer is fixed."]),
        dict(title='Slide the apex', active=7, script=[
            _b('Same base, apex on a parallel line → same area', 'Same base, apex on a parallel line $\\rightarrow$ same height $\\rightarrow$ same area', size=38),
            "The apex slides along a line parallel to the base. The height stays the same — so the area stays the same.",
            _b('The perimeter does change', 'The perimeter DOES change'),
            "But the perimeter changes. You'll see this in a trapezoid too."]),
        dict(title='Before you practice', active=8, script=[
            "Before you practice, ask yourself these questions.",
            _b('What is fixed: the perimeter or the area?', 'What is fixed: the perimeter or the area?'),
            _b('Must, could or cannot?', 'Must, could or cannot?'),
            _b('What is really given, and what is free?', 'What is really given, and what is free?'),
            _b('What happens at the extremes?', 'What happens at the extremes? Compare with $90°$.'),
            "The traps: trusting the drawing, and thinking a wider angle always means a bigger area.",
            "Good luck."]),
    ], LEARN, after=last)


# ==================================================================================== 2026-10-05 cut repeats
def _slide_no(M, vid, title):
    return next(n for n, b in enumerate(M.video(vid)['beats'], 1) if b.get('title') == title)


def _add_after(M, vid, n, after, new_items):
    """Insert DSL items (spoken lines / A(...) board items) right after the spoken line containing `after`."""
    sc = _script(M, vid, n)
    k = next(i for i, x in enumerate(sc) if isinstance(x, str) and after in x)
    sc[k + 1:k + 1] = new_items
    M.set_slide(vid, n, script=sc)


def cut_repeats(M):
    """Lessons back to the Hebrew length: cut lesson slides whose idea a question video right after teaches again.
    Where a cut slide had something the question video did not say, ONE short line + board item moves there."""

    # ---- Shape Efficiency (geo-172): Hebrew = slides 1-6. Cut 'Rectangles, P = 24' and 'Fixed P or fixed S?'.
    closing = [l['say'] for l in M.slide(SHAPE, _slide_no(M, SHAPE, 'Fixed P or fixed S?'))['lines']
               if 'say' in l and not l['say'].startswith(('Before you answer', 'Same perimeter —', 'And regular polygons'))]
    assert len(closing) == 4, closing
    M.remove_slides(SHAPE, [_slide_no(M, SHAPE, 'Rectangles, P = 24'), _slide_no(M, SHAPE, 'Fixed P or fixed S?')])
    n6 = _slide_no(M, SHAPE, 'Long and thin')
    M.edit_lines(SHAPE, n6, lambda lines: lines + [{'say': s} for s in closing])
    M.set_sidebar(SHAPE, ['No calculation', 'The circle wins', 'The country rule', 'Closer to a circle', 'Long and thin'])
    _lesson_actives(M, SHAPE)
    # the fixed-perimeter rectangles (24 of edging) move into Question 2's rectangle check
    q2 = 'solve-geo38-g174'; n = _slide_no(M, q2, 'Same idea with rectangles')
    _replace_say(M, q2, n, 'A familiar check from the course', "Let's check it with rectangles. Both of these have area 36.")
    _add_after(M, q2, n, 'Same area, more stretched', [
        A("'Same P = 24: 1 × 11 → 11, 6 × 6 → 36' appears", R(0, 470, 'Same $P=24$: $1\\times11\\rightarrow11$, $6\\times6\\rightarrow36$', 30)),
        "And the other way: 24 of edging. 1 by 11 gives area 11. 6 by 6 gives 36."])

    # ---- Minimum and Maximum (geo-175): cut 'Two rods', 'Greatest area', 'Acute or obtuse?'.
    #      Rods rule: taught in Question 3 (g176) and q-r26-t38-01; greatest area / parallelogram / area toward 0 /
    #      past 90 the height shrinks: q-r26-t38-01 and Question 9 (g183). c² vs a² + b²: Question 3, slide 4.
    #      'Farthest apart' stays: no question video teaches it (only practice uses it).
    M.remove_slides(MINMAX, [_slide_no(M, MINMAX, t) for t in ('Two rods', 'Greatest area', 'Acute or obtuse?')])
    _replace_say(M, MINMAX, _slide_no(M, MINMAX, 'Farthest apart'), "One more 'greatest'",
                 "Now a 'greatest' you'll see in practice: the greatest distance.")
    M.set_sidebar(MINMAX, ['Min–max in geometry', 'Move the vertex away', 'Stretch the segment', 'Farthest apart',
                           'Angles on an arc', 'Angle on a diameter', 'Min–max with an anchor'])
    _lesson_actives(M, MINMAX)
    q3 = 'solve-geo38-g176'
    _replace_say(M, q3, _slide_no(M, q3, 'The side grew — the angle opened'), 'Remember the rods rule',
                 "Here's the rods rule: two sides stay the same — the wider the angle between them, the longer the third side.")
    n = _slide_no(M, q3, 'Check with the squares')
    _replace_say(M, q3, n, 'A check from the course', 'A check with the squares: 16 squared is 256. 9 squared plus 12 squared is 225.')
    _add_after(M, q3, n, "The opposite side's square is bigger", [
        A("'c² < a² + b² → acute (c = the longest side)' appears",
          R(0, 400, '$c^2<a^2+b^2$ $\\rightarrow$ all acute ($c$ = the longest side)', 30)),
        "And if the longest side's square is smaller than the sum — all three angles are acute."])

    # ---- Diagrams That Can Change (geo-177): back to the Hebrew short intro.
    #      Must / could / cannot: topic 1 (and algebra topic 20); the questions here use it.
    #      Test a claim, push to the extremes: Questions 4-5 (g178, g179), edges: Question 6 (g180), counterexample with
    #      numbers: Question 10 (g184). Slide the apex: q-r26-t38-02. Cannot be determined: Question 4 (g178).
    M.remove_slides(DIAG, list(range(2, len(M.video(DIAG)['beats']) + 1)))
    M.set_slide(DIAG, 1, script=[
        'In the last lessons we met this topic and its main ideas.',
        "Now we practice exam questions at a high level. Along the way, we'll learn more fine points."])
    M.insert_slides(DIAG, 1, [dict(mode='concept', title='Diagrams that can change', active=0, pre=[], script=[
        A("'A drawing can suggest — not prove' appears", T('A drawing can suggest something — not prove it', 42)),
        'In these questions the drawing can suggest something — without proving it.',
        A("'Must, could or cannot?' appears", T('Must be true? Could be true? Cannot be true?', 42)),
        "And read what they ask: must be true, could be true, or cannot be true.",
        "Each question that follows teaches a tool for this. Let's start with a sample question."])])
    M.set_sidebar(DIAG, ['Diagrams that can change'])
    # q-r26-t38-02 (first question after it): say it is a tool, and keep the perimeter warning from 'Slide the apex'
    g2 = 'solve-q-r26-t38-02'; n = _slide_no(M, g2, 'Same base, same height')
    _replace_say(M, g2, n, 'Look for triangles with the same base',
                 'A tool for areas: look for triangles with the same base and an apex on a parallel line.')
    _add_after(M, g2, n, 'Same base, same height — the same area', [
        A("'Apex slides on a parallel line: same area, not same perimeter' appears",
          R(0, 330, 'Apex slides on a parallel line: same area — but not the same perimeter', 30)),
        'Careful: only the area stays. Slide the apex along the line, and the sides — the perimeter — change.'])
    # g178 (Question 4): 'what is free' + the end / the middle; and the test for 'cannot be determined'
    q4 = 'solve-geo38-g178'
    _replace_say(M, q4, _slide_no(M, q4, 'What does it depend on?'), "That's the 'find what is free' check",
                 'Notice: TR is free. Nothing in the givens fixes it. So always ask: what is free? Push it to the end — or to the middle.')
    n = _slide_no(M, q4, 'All three can happen')
    _add_after(M, q4, n, 'TR 2 — the triangle is 3', [
        A("'Cannot be determined? Two legal figures, two answers' appears",
          R(0, 470, "'Cannot be determined'? Two legal figures, two answers", 30)),
        "That's the only test for 'none must be true' or 'cannot be determined': two figures that keep every given, and two different answers.",
        "In geometry it's rare — so test it before you choose it."])


# ======================================================================================================
# 2026-10-06 renumber pass (runs LAST, after cut_repeats). The English course must not look like the Hebrew one:
# every Hebrew-derived question (guided geo38-g173 ... g187, practice geo38-core-p01 ... p20) gets new numbers
# (letter-only questions: new letters, names and choice order; stories a bit changed). Idea, trap, level and methods stay.
# Every changed figure is redrawn / relabelled, every guided solution video is rewritten to match.
# Practice clean-up (approved): copy p26, extras beyond 3, September items whose type the Hebrew practice covers.
# Nothing in topic 38 is recorded (checked ~/Documents/Course.recordings 2026-10-06).
# ======================================================================================================
RN_RECORDED = set()
CBD38 = 'It cannot be determined from the information given.'


def _rn_letters(t, mp):
    """Rename point letters: every all-capital token made only of letters in mp (not 'A' used as an article,
    not the area sign S_)."""
    def r(mo):
        tok = mo.group(1)
        if not all(ch in mp for ch in tok): return tok
        if tok == 'A' and re.match(r' [a-z]', t[mo.end():mo.end() + 2]): return tok
        return ''.join(mp[ch] for ch in tok)
    return re.sub(r'(?<![A-Za-z\\])([A-Z]+)(?![A-Za-z_])', r, t)


def _rn_video_text(M, vid, fn):
    """Apply fn to every text of a video: slide titles, spoken / drawn lines, labels, board items."""
    if vid in RN_RECORDED: return
    for b in M.video(vid)['beats']:
        if b.get('title'): b['title'] = fn(b['title'])
        for l in b['lines']:
            for key in ('say', 'draw', 'label'):
                if key in l: l[key] = fn(l[key])
        for it in b['items']:
            if it.get('t'): it['t'] = fn(it['t'])
    M.touched_videos.add(vid)


def _rn_sub(M, vid, n, pairs):
    """Exact substring replacements in one slide (title, lines, labels, board items); each must hit."""
    if vid in RN_RECORDED: return
    b = M.slide(vid, n)
    for old, new in pairs:
        hit = False
        if old in b.get('title', ''): b['title'] = b['title'].replace(old, new); hit = True
        for l in b['lines']:
            for key in ('say', 'draw', 'label'):
                if key in l and old in l[key]: l[key] = l[key].replace(old, new); hit = True
        for it in b['items']:
            if it.get('t') and old in it['t']: it['t'] = it['t'].replace(old, new); hit = True
        assert hit, (vid, n, old)
    M.touched_videos.add(vid)


def _rn_lines(M, vid, n, lines):
    """Replace all lines of a slide (items stay; 'appear' lines must point at the same items)."""
    if vid in RN_RECORDED: return
    old = [l['appear'] for l in M.slide(vid, n)['lines'] if 'appear' in l]
    assert old == [l['appear'] for l in lines if 'appear' in l], (vid, n)
    M.edit_lines(vid, n, lambda ls: lines)


def _rn_q(M, qid, **kw):
    if qid in RN_RECORDED: return
    old = (M.q(qid).get('questionVisual') or {}).get('svg')
    M.set_q(qid, **kw)
    return old


def _rn_slide_figs(M, vid, fn):
    """fn(svg) -> new svg for every figure shown on the slides of a video (question copies and VIS items)."""
    if vid in RN_RECORDED: return
    for b in M.video(vid)['beats']:
        for it in b['items']:
            if it.get('fig'): it['fig'] = dict(it['fig'], svg=fn(it['fig']['svg']))
            if it.get('k') == 'vis': it['v'] = dict(it['v'], svg=fn(it['v']['svg']))
    M.touched_videos.add(vid)


def _relabel(svg, mp):
    """Change the text of figure labels (exact <text> contents, each must exist)."""
    for old in mp: assert ('>%s</text>' % old) in svg, old
    return re.sub(r'>([^<]+)</text>', lambda mo: '>%s</text>' % mp.get(mo.group(1), mo.group(1)), svg)


def _rn_same(old, new):
    """Figure map for solution slides: the copy of the old question figure becomes the new one."""
    vb = lambda x: re.search(r'viewBox="([^"]+)"', x).group(1)

    def f(s):
        assert s.replace(vb(s), '') == old.replace(vb(old), ''), 'unexpected figure on a solution slide'
        return new.replace('viewBox="%s"' % vb(new), 'viewBox="%s"' % vb(s))   # keep the slide's crop
    return f


# ---------------------------------------------------------------- redrawn figures (same style and frames)
def _rn_reg(cx, base_y, n, side, rot0=None):
    """Regular n-gon with one side horizontal at the bottom (y = base_y), centered on x = cx."""
    R = side / (2 * math.sin(math.pi / n)); a = R * math.cos(math.pi / n)
    cy = base_y - a
    pts = [(cx + R * math.cos(math.radians(90 + 180.0 / n + 360.0 * k / n)), cy + R * math.sin(math.radians(90 + 180.0 / n + 360.0 * k / n)))
           for k in range(n)]
    return pts, (cx, cy, R)


def rn_fig_g173():
    """Perimeter 30 each (drawn with equal perimeters): triangle, square, pentagon, octagon (circle around it)."""
    P = 320.0; y = 250.0; body = []
    for cx, n, name in ((73.3, 3, 'triangle'), (216.7, 4, 'square'), (360.0, 5, 'pentagon'), (511.6, 8, 'octagon')):
        pts, (ox, oy, R) = _rn_reg(cx, y, n, P / n)
        if n == 8:
            body.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#c8691c" stroke-width="2" stroke-dasharray="6 5"/>' % (ox, oy, R + 1.5))
            body.append(_poly(pts, TFILL, TEAL))
        else: body.append(_poly(pts, 'none', INK))
        body.append(_t(cx, 276.0, name, size=18))
    return _svg('-6.0 123.4 595.9 178.6', 'Perimeter 30 each', body)


def rn_fig_g176():
    """Triangle ABC: AB = 8, BC = 15, AC = 18 (alpha at B, about 98 degrees)."""
    u = 16.5; al = math.degrees(math.acos((8 ** 2 + 15 ** 2 - 18 ** 2) / (2 * 8 * 15)))
    B = (400.0, 310.0); A_ = (B[0] - 8 * u, B[1]); d = math.radians(180 - al)
    C_ = (B[0] + 15 * u * math.cos(d), B[1] - 15 * u * math.sin(d))
    r = 23.0; a0 = math.pi; a1 = d
    p0 = (B[0] + r * math.cos(a1), B[1] - r * math.sin(a1)); p1 = (B[0] - r, B[1])
    body = [_poly([A_, B, C_], 'none', INK),
            _t(A_[0] - 18, A_[1] + 16, 'A'), _t(B[0] + 18, B[1] + 16, 'B'), _t(C_[0], C_[1] - 20, 'C'),
            '<path d="M %.3f %.3f A %.3f %.3f 0 0 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="2"/>' % (p0[0], p0[1], r, r, p1[0], p1[1], TEAL),
            _t(B[0] - 22, B[1] - 26, 'α', TEAL, 18),
            _t((A_[0] + B[0]) / 2, B[1] + 28, '8'), _t((B[0] + C_[0]) / 2 + 24, (B[1] + C_[1]) / 2, '15'),
            _t((A_[0] + C_[0]) / 2 - 22, (A_[1] + C_[1]) / 2 - 8, '18')]
    return _svg('0 0 640 360', 'Triangle ABC', body)


def _rn_trap(P, S, Q_, R, vb):
    """The trapezoid of Question 'trapezoid' with the new letters K L M N and F."""
    T_ = (S[0], Q_[1])
    body = [_poly([P, Q_, T_, S], FILL, INK), _poly([T_, R, S], TFILL, TEAL),
            _right(T_[0], T_[1], 0, -1, 1, 0),
            _t(P[0] - 12, P[1] - 20, 'K'), _t(Q_[0] - 16, Q_[1] + 16, 'L'), _t(R[0] + 16, R[1] + 16, 'M'),
            _t(S[0] + 12, S[1] - 20, 'N'), _t(T_[0], T_[1] + 23, 'F')]
    return _svg(vb, 'A trapezoid split by a perpendicular from an upper vertex', body)


RN_FIG_Q4 = _rn_trap((190, 110), (350, 110), (130, 250), (410, 250), '70 64 400 235')
RN_FIG_Q4_STRETCH = _rn_trap((130, 110), (230, 110), (100, 250), (590, 250), '48 64 580 235')


def rn_fig_g182():
    """Sphere of radius 6 (20 px per cm): cut P 9 cm from A, cut Q 7 cm from B."""
    def ball(cx, cut_x, title, dim_from, dim_to, dim):
        h = math.sqrt(120 ** 2 - (cut_x - cx) ** 2)
        return ['<circle cx="%d" cy="150" r="120" fill="%s" stroke="%s" stroke-width="2.5"/>' % (cx, FILL2, INK),
                '<ellipse cx="%d" cy="150" rx="120" ry="26" fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="5 5"/>' % (cx, GRAY),
                _ln(cx - 120, 150, cx + 120, 150, INK, 2.2), _dot(cx, 150, 4), _dot(cx - 120, 150, 4), _dot(cx + 120, 150, 4),
                _ln(cut_x, 150 - h, cut_x, 150 + h, TEAL, 3.4), _dot(cut_x, 150, 4, TEAL),
                _t(cx - 136, 150, 'A', size=21), _t(cx + 136, 150, 'B', size=21), _t(cx + (10 if cut_x < cx else -12), 170, 'O', size=19),
                _ln(cut_x, 150 + h + 4, cut_x, 304, GRAY, 1.2, '3 3'),
                _ln(dim_from if dim_from != cut_x else dim_to, 154, dim_from if dim_from != cut_x else dim_to, 304, GRAY, 1.2, '3 3'),
                _ln(dim_from, 296, dim_to, 296, ORANGE, 2.4), _t((dim_from + dim_to) / 2, 314, dim, ORANGE, 19, '700'),
                _t(cx, 10, title, TEAL, 20, '700')]
    body = ball(160, 40 + 9 * 20, 'Cut P: 9 cm from A', 40, 220, '9 cm') + \
        ball(480, 600 - 7 * 20, 'Cut Q: 7 cm from B', 460, 600, '7 cm')
    return _svg('10 0 620 330', 'Two cuts of a sphere of radius 6 cm', body)


def rn_fig_g183():
    """Parallelograms ABCD (4, 8, 70 degrees) and EFGH (4, 8, 30 degrees), 30 px per cm."""
    def par(B, ang, L, lab):
        u = 30.0; a = math.radians(ang)
        C_ = (B[0] + 8 * u, B[1]); A_ = (B[0] + 4 * u * math.cos(a), B[1] - 4 * u * math.sin(a)); D_ = (A_[0] + 8 * u, A_[1])
        r = 30.0; p1 = (B[0] + r * math.cos(a), B[1] - r * math.sin(a))
        return [_poly([B, C_, D_, A_], FILL2, INK, 2.6),
                '<path d="M %.1f %.1f A 30.0 30.0 0 0 0 %.1f %.1f" fill="none" stroke="%s" stroke-width="2.4"/>' % (B[0] + r, B[1], p1[0], p1[1], TEAL),
                _t(B[0] + 46 + (4 if ang < 45 else 0), B[1] - 16 + (4 if ang < 45 else 0), '%d°' % ang, TEAL, 18, '700', 'start'),
                _t(A_[0] - 8, A_[1] - 14, L[0]), _t(B[0] - 12, B[1] + 18, L[1]), _t(C_[0] + 12, C_[1] + 18, L[2]), _t(D_[0] + 12, D_[1] - 12, L[3]),
                _t((A_[0] + B[0]) / 2 - 14, (A_[1] + B[1]) / 2 - 4, '4', ORANGE, 20, '700'),
                _t((B[0] + C_[0]) / 2, B[1] + 22, '8', ORANGE, 20, '700')]
    body = par((30.0, 200.0), 70, 'ABCD', None) + par((350.0, 200.0), 30, 'EFGH', None)
    return _svg('-14.0 44.1 736.0 203.9', 'Parallelograms ABCD and EFGH', body)


def rn_fig_g185():
    """An equilateral triangle and a regular hexagon inscribed in the same circle."""
    ox, oy, r = 320.0, 180.0, 116.8
    hexa = [(ox + r * math.cos(math.radians(90 + 60 * k)), oy - r * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
    tri = hexa[0::2]
    body = ['<circle cx="%.3f" cy="%.3f" r="%.3f" fill="none" stroke="%s" stroke-width="2.5"/>' % (ox, oy, r, INK),
            _poly(hexa, TFILL, TEAL), _poly(tri, FILL, INK)]
    return _svg('177.2 37.2 285.6 285.6', 'An equilateral triangle and a regular hexagon inscribed in the same circle', body)


def rn_fig_g187():
    """Three rows of three congruent circles, tightly in a rectangle."""
    r = 45.0; x0, y0 = 320 - 3 * r, 180 - 3 * r
    body = [_poly([(x0, y0 + 6 * r), (x0 + 6 * r, y0 + 6 * r), (x0 + 6 * r, y0), (x0, y0)], 'none', INK)]
    for i in range(3):
        for j in range(3):
            body.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s" stroke="%s" stroke-width="2.5"/>'
                        % (x0 + r + 2 * r * i, y0 + r + 2 * r * j, r, FILL, TEAL))
    return _svg('0 0 640 360', 'Three rows of congruent tangent circles in a tight rectangle', body)


def rn_fig_p01():
    """Circles of radius 5 (center O) and 3, 3 (centers P, Q), externally tangent."""
    u = 23.36; O = (226.0, 180.0); d = 8 * u; h = 3 * u
    P = (O[0] + math.sqrt(d * d - h * h), O[1] - h); Q_ = (P[0], O[1] + h)
    body = ['<circle cx="%.3f" cy="%.3f" r="%.3f" fill="none" stroke="%s" stroke-width="2.5"/>' % (O[0], O[1], 5 * u, INK),
            '<circle cx="%.3f" cy="%.3f" r="%.3f" fill="none" stroke="%s" stroke-width="2.5"/>' % (P[0], P[1], 3 * u, INK),
            '<circle cx="%.3f" cy="%.3f" r="%.3f" fill="none" stroke="%s" stroke-width="2.5"/>' % (Q_[0], Q_[1], 3 * u, INK),
            _poly([O, P, Q_], 'none', TEAL), _t(O[0] - 15, O[1], 'O'), _t(P[0] + 18, P[1], 'P'), _t(Q_[0] + 18, Q_[1], 'Q')]
    return _svg('0 0 640 360', 'Three externally tangent circles, two of equal radius', body)


def rn_fig_p06():
    """Right isosceles triangle: K fixed on the line, L to the right of K, M above K (rotates counterclockwise)."""
    K = (320.0, 277.333); L = (514.667, 277.333); Mx = (320.0, 82.667)
    body = [_poly([L, K, Mx], FILL, INK), _right(K[0], K[1], 1, 0, 0, -1, s=14.6),
            _t(K[0], K[1] + 22, 'K'), _t(L[0] + 17, L[1], 'L'), _t(Mx[0], Mx[1] - 22, 'M')]
    return _svg('0 0 640 360', 'A right isosceles triangle rotating counterclockwise about its right-angle vertex', body)


def rn_fig_p13():
    """Rhombus KLMN with a 50-degree angle at L, and square PQRS with the same side."""
    B = (125.333, 277.333); s = 194.667; a = math.radians(50)
    A_ = (B[0] + s * math.cos(a), B[1] - s * math.sin(a)); C_ = (B[0] + s, B[1]); D_ = (A_[0] + s, A_[1])
    rr = 38.933; p1 = (B[0] + rr * math.cos(a), B[1] - rr * math.sin(a))
    rh = ['<g transform="translate(0 0) scale(.5)"><title>A rhombus with a fifty-degree angle</title>',
          _poly([A_, B, C_, D_], 'none', INK), _ln(A_[0], A_[1], C_[0], C_[1], TEAL), _ln(B[0], B[1], D_[0], D_[1], ORANGE),
          '<path d="M %.3f %.3f A %.3f %.3f 0 0 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="2"/>' % (B[0] + rr, B[1], rr, rr, p1[0], p1[1], TEAL),
          _t(B[0] + 58, B[1] - 16, '50°', TEAL, 18),
          _t(A_[0] - 10, A_[1] - 18, 'K'), _t(B[0] - 15, B[1] + 15, 'L'), _t(C_[0], C_[1] + 22, 'M'), _t(D_[0] + 15, D_[1] - 15, 'N'), '</g>',
          '<text x="160" y="197" text-anchor="middle" font-family="DejaVu Sans,Arial" font-size="15" fill="#203344">Rhombus</text>']
    E, F, G, H = (222.667, 82.667), (222.667, 277.333), (417.333, 277.333), (417.333, 82.667)
    sq = ['<g transform="translate(320 0) scale(.5)"><title>A square with the same side length as the rhombus</title>',
          _poly([E, F, G, H], 'none', INK), _ln(E[0], E[1], G[0], G[1], TEAL),
          _t(E[0] - 15, E[1] - 15, 'P'), _t(F[0] - 15, F[1] + 15, 'Q'), _t(G[0] + 15, G[1] + 15, 'R'), _t(H[0] + 15, H[1] - 15, 'S'), '</g>',
          '<text x="480" y="197" text-anchor="middle" font-family="DejaVu Sans,Arial" font-size="15" fill="#203344">Square</text>']
    return _svg('0 0 640 205', 'Compare the figures', rh + sq)


def rn_fig_p15():
    """Four horizontal and nine vertical segments at their maximum number of crossings."""
    body = []
    xs = [150.0 + 40.0 * k for k in range(9)]; ys = [120.0 + 40.0 * k for k in range(4)]
    for y in ys: body.append(_ln(128.0, y, 492.0, y, TEAL))
    for x in xs: body.append(_ln(x, 98.0, x, 262.0, ORANGE))
    return _svg('0 0 640 360', 'Four horizontal and nine vertical segments at their maximum number of crossings', body)


def rn_fig_p16():
    """p16: B(0,0) C(7,0) A(4,4) D(11,4) E(0,4); u = 30 px."""
    u, ox, oy = 30.0, 150.0, 280.0
    P = lambda x, y: (ox + u * x, oy - u * y)
    A_, B_, C_, D_, E = P(4, 4), P(0, 0), P(7, 0), P(11, 4), P(0, 4)
    tick = lambda p, q, dx, dy: _ln((p[0] + q[0]) / 2 - dx, (p[1] + q[1]) / 2 - dy, (p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, TEAL, 1.8)
    body = [_poly([E, A_, B_], FILL, INK), _poly([B_, C_, D_, A_], 'none', INK),
            _right(E[0], E[1], 1, 0, 0, 1, s=13), _right(B_[0], B_[1], 1, 0, 0, -1, s=13),
            tick(E, A_, 0, 7), tick(E, B_, 7, 0),
            _t(A_[0], A_[1] - 20, 'A'), _t(B_[0] - 14, B_[1] + 16, 'B'), _t(C_[0] + 12, C_[1] + 18, 'C'),
            _t(D_[0] + 14, D_[1] - 14, 'D'), _t(E[0] - 18, E[1] - 12, 'E'), _t((B_[0] + C_[0]) / 2, B_[1] + 24, '7 cm')]
    return _svg('110 120 420 210', 'A parallelogram with a right isosceles triangle attached to side AB', body)


# ---------------------------------------------------------------- guided questions and their solution videos
def rn_guided(M):
    # --- Question 1 (g173): perimeter 24, triangle / square / hexagon / octagon -> perimeter 30, triangle / square / pentagon / octagon
    q, v = 'geo38-g173', 'solve-geo38-g173'
    _rn_q(M, q, stem='An equilateral triangle, a square, a regular pentagon and a regular octagon each have perimeter 30 cm. Which has the greatest area?',
          choices=['The regular pentagon', 'The square', 'The equilateral triangle', 'The regular octagon'], correct=4,
          expl=['All four shapes are regular and have the same perimeter. Among regular polygons with equal perimeters, the one with the most sides is the most like a circle. So, it has the greatest area: the octagon.',
                'Choice 4.'])
    _rn_slide_figs(M, v, lambda s: rn_fig_g173())
    _rn_sub(M, v, 2, [('a regular hexagon and a regular octagon. All have perimeter 24.', 'a regular pentagon and a regular octagon. All have perimeter 30.'),
                      ('Triangle, square, hexagon, octagon', 'Triangle, square, pentagon, octagon'),
                      ('Circle choice 3', 'Circle choice 4'), ('Choice three.', 'Choice four.')])
    _rn_sub(M, v, 3, [('the whole boundary is still $24$', 'the whole boundary is still $30$'),
                      ('the boundary is the same 24', 'the boundary is the same 30'), ('the whole boundary is the same 24.', 'the whole boundary is the same 30.')])

    # --- Question 2 (g174): hexagonal plots, 90 m^2 -> octagonal flower beds, 60 m^2; rectangles area 36 -> area 100
    q, v = 'geo38-g174', 'solve-geo38-g174'
    _rn_q(M, q, stem=' Two convex octagonal flower beds have the same area, 60 m². One is regular and the other is not regular. Which statement is correct? ',
          choices=['The nonregular octagon has the greater perimeter.', 'The regular octagon has the greater perimeter.', 'The perimeters are equal.', CBD38],
          correct=1, expl=['Both beds are octagons with the same area. The regular octagon is more like a circle. So, it needs less perimeter.',
                           'The nonregular octagon has the greater perimeter: choice 1.'])
    M.video(v)['title'] = M.video(v)['navLabel'] = 'Equal areas: which bed needs more edging?'

    def rect(s):
        for a, b in (('>12</text>', '>20</text>'), ('>6</text>', '>10</text>'), ('>3</text>', '>5</text>'),
                     ('Area 36; perimeter 24', 'Area 100; perimeter 40'), ('Area 36; perimeter 30', 'Area 100; perimeter 50')):
            assert a in s, a; s = s.replace(a, b)
        return s
    _rn_slide_figs(M, v, rect)
    _rn_lines(M, v, 2, [
        {'say': "Two octagonal flower beds with the same area, 60 square meters. One is regular, the other isn't. Which statement is correct?"},
        {'say': "First of all — area and perimeter. So it's shape efficiency."},
        {'appear': 1, 'label': 'Who is more like a circle? The regular octagon appears'},
        {'say': 'Who is more like a circle? The regular octagon, of course.'},
        {'say': 'A more efficient shape always has more area and less perimeter.'},
        {'appear': 2, 'label': 'Same area → regular: less perimeter appears'},
        {'say': 'Both have the same area. So, the regular octagon has less perimeter.'},
        {'say': 'They asked who has the greater perimeter: the non-regular one. It has more border.'},
        {'draw': 'Circle choice 1'},
        {'say': 'Choice one.'}])
    _rn_sub(M, v, 2, [('The regular hexagon.', 'The regular octagon.')])
    _rn_lines(M, v, 3, [
        {'appear': 1, 'label': 'A 10 × 10 square and a 5 × 20 rectangle appear'},
        {'say': "Let's check it with rectangles. Both of these have area 100."},
        {'appear': 2, 'label': 'Square: perimeter 40 appears'},
        {'appear': 3, 'label': 'Rectangle: perimeter 50 appears'},
        {'say': 'The square — the more circle-like one — needs perimeter 40. The stretched rectangle needs 50.'},
        {'say': 'Same area, more stretched — more edging.'},
        {'appear': 4, 'label': "'Same P = 40: 2 × 18 → 36, 10 × 10 → 100' appears"},
        {'say': 'And the other way: 40 of edging. 2 by 18 gives area 36. 10 by 10 gives 100.'},
        {'say': 'One condition: this works because both are octagons, one regular, one not. Same number of sides.'}])
    _rn_sub(M, v, 3, [('Square: $P=24$', 'Square: $P=40$'), ('Rectangle: $P=30$', 'Rectangle: $P=50$'),
                      ('Same $P=24$: $1\\times11\\rightarrow11$, $6\\times6\\rightarrow36$', 'Same $P=40$: $2\\times18\\rightarrow36$, $10\\times10\\rightarrow100$')])

    # --- Question 3 (g176): 9, 12, 16 (anchor 9-12-15) -> 8, 15, 18 (anchor 8-15-17)
    q, v = 'geo38-g176', 'solve-geo38-g176'
    old = _rn_q(M, q, stem=' A triangle has side lengths 8 cm, 15 cm and 18 cm. Angle α is opposite the 18-cm side. Which of the following statements is necessarily true? ',
                choices=['$\\alpha<90°$', '$\\alpha=90°$', '$\\alpha>90°$', CBD38], correct=3,
                expl=['Anchor: if $\\alpha$ were $90°$, the side opposite it would be 17, because $8, 15, 17$ is a Pythagorean triple ($64+225=289=17^2$).',
                      'The side is 18, longer than 17. Two fixed sides (8 and 15) with a longer third side: the angle between them opened. So, $\\alpha>90°$: choice 3.',
                      'Check: $18^2=324>8^2+15^2=289$.'], figure=rn_fig_g176())
    _rn_slide_figs(M, v, _rn_same(old, rn_fig_g176()))
    _rn_sub(M, v, 2, [('A triangle with sides 9, 12 and 16. Angle α is opposite the 16.', 'A triangle with sides 8, 15 and 18. Angle α is opposite the 18.'),
                      ("what's given: α, 9, 12, 16.", "what's given: α, 8, 15, 18."),
                      ("9, 12, 15 — that's a right triangle! 3, 4, 5.", "8, 15, 17 — that's a right triangle! A Pythagorean triple."),
                      ("But it's not 15 — it's 16.", "But it's not 17 — it's 18."),
                      ('$\\alpha=90°\\ \\rightarrow\\ 9,\\ 12,\\ 15$ $(3,4,5)\\times3$', '$\\alpha=90°\\ \\rightarrow\\ 8,\\ 15,\\ 17$ (a Pythagorean triple)'),
                      ('α = 90° → 9, 12, 15 (3, 4, 5 × 3) appears', 'α = 90° → 8, 15, 17 (a Pythagorean triple) appears'),
                      ("it's a right triangle: 9, 12, 15. The triple 3, 4, 5 — times 3.", "it's a right triangle: 8, 15, 17. 8 squared plus 15 squared is 289 — that's 17 squared.")])
    _rn_sub(M, v, 3, [('$15\\rightarrow16$', '$17\\rightarrow18$'), ('15 → 16: the side', '17 → 18: the side'),
                      ("isn't 15. It's 16", "isn't 17. It's 18"), ('Think of the 9 and the 12', 'Think of the 8 and the 15'),
                      ('from 15 apart to 16 apart', 'from 17 apart to 18 apart'), ('Circle choice 2', 'Circle choice 3'), ('Choice two.', 'Choice three.')])
    _rn_sub(M, v, 4, [('$16^2=256$', '$18^2=324$'), ('$9^2+12^2=81+144=225$', '$8^2+15^2=64+225=289$'),
                      ('16² = 256, 9² + 12² = 225 appears', '18² = 324, 8² + 15² = 289 appears'), ('81 + 144 = 225 < 256 appears', '64 + 225 = 289 < 324 appears'),
                      ('16 squared is 256. 9 squared plus 12 squared is 225.', '18 squared is 324. 8 squared plus 15 squared is 289.'),
                      ("'16 is the longest side'", "'18 is the longest side'")])

    # --- Question 6 (g178): letters PQRS / T -> KLMN / F; numbers of the example 3, 4, 3 / 2, 7, 10 -> 2, 5, 4 / 3, 7, 12
    q, v = 'geo38-g178', 'solve-geo38-g178'
    mp = dict(P='K', Q='L', R='M', S='N', T='F')
    _rn_q(M, q, stem=' KLMN is a trapezoid with KN ∥ LM. F lies on LM, and NF ⟂ LM. Which of the following statements is necessarily true? ',
          choices=['The area of triangle NFM is less than the area of trapezoid KLFN.', 'The area of triangle NFM is greater than the area of trapezoid KLFN.',
                   'The area of triangle NFM equals the area of trapezoid KLFN.', 'None of the above is necessarily true.'], correct=4,
          expl=['Both regions have height NF. Trapezoid KLFN: $\\frac{(KN+LF)\\cdot NF}{2}$. Triangle NFM: $\\frac{FM\\cdot NF}{2}$.',
                'Compare $FM$ with $KN+LF$. The givens do not fix FM (LM can be stretched to the right).',
                'Example: $KN=2$, $LF=5$, $NF=4$: the trapezoid is 14. $FM=3$ gives a triangle of 6, $FM=7$ gives 14, $FM=12$ gives 24. '
                'All three cases happen. So, none of the claims must be true: choice 4.'], figure=RN_FIG_Q4)
    _rn_slide_figs(M, v, lambda s: RN_FIG_Q4 if s == FIG_Q4 else RN_FIG_Q4_STRETCH if s == FIG_Q4_STRETCH else 1 / 0)
    _rn_video_text(M, v, lambda t: _rn_letters(t, mp))
    _rn_sub(M, v, 5, [('Take KN 3, LF 4 and height 3. The trapezoid is 10.5.', 'Take KN 2, LF 5 and height 4. The trapezoid is 14.'),
                      ('$FM=2$: triangle $3$', '$FM=3$: triangle $6$'), ('$FM=7$: triangle $10.5$', '$FM=7$: triangle $14$'),
                      ('$FM=10$: triangle $15$', '$FM=12$: triangle $24$'),
                      ('FM = 2 → triangle 3 appears', 'FM = 3 → triangle 6 appears'), ('FM = 7 → triangle 10.5 appears', 'FM = 7 → triangle 14 appears'),
                      ('FM = 10 → triangle 15 appears', 'FM = 12 → triangle 24 appears'),
                      ('FM 2 — the triangle is 3, smaller. FM 7 — 10.5, equal. FM 10 — 15, bigger.', 'FM 3 — the triangle is 6, smaller. FM 7 — 14, equal. FM 12 — 24, bigger.')])

    # --- Question 7 (g179): diameter AB, chord CD, Ava / Noah / Mia -> diameter KL, chord MN, Lily / Ethan / Grace; new choice order
    q, v = 'geo38-g179', 'solve-geo38-g179'
    mp = dict(A='K', B='L', C='M', D='N')
    names = lambda t: t.replace('Ava', 'Lily').replace('Noah', 'Ethan').replace('Mia', 'Grace')
    _rn_q(M, q, stem=' KL is a diameter of a circle, and chord MN is perpendicular to KL. The four regions are labeled I, II, III and IV, as shown in the accompanying figure. '
                     'Lily claims I = II in area. Ethan claims II = III. Grace claims I + III = II + IV. Which of the claims are necessarily true? ',
          choices=['Lily’s only', 'Lily’s and Grace’s only', 'All three', 'Ethan’s and Grace’s only'], correct=2,
          expl=['KL is a diameter, and a diameter is a line of symmetry. Reflect across KL: I goes onto II, and IV goes onto III. So, I = II and III = IV (Lily is right).',
                'I + IV is half the circle (above KL). Since IV = III, I + III is also half the circle, and so is II + IV. Grace is right.',
                'MN is only a chord. Push it toward L: III becomes tiny while II stays large. II = III need not be true. Answer: Lily and Grace only, choice 2.'],
          figure=_relabel(FIG_Q5, mp))
    _rn_slide_figs(M, v, lambda s: _relabel(s, mp))
    _rn_video_text(M, v, lambda t: names(_rn_letters(t, mp)))
    _rn_sub(M, v, 4, [('Circle choice 3', 'Circle choice 2'), ("Lily's and Grace's only — choice three.", "Lily's and Grace's only — choice two.")])

    # --- Question 8 (g180): 45 degrees and beta < 80 -> 50 degrees and beta < 70 (range 60 .. 130)
    q, v = 'geo38-g180', 'solve-geo38-g180'
    old = _rn_q(M, q, stem='ABCD is a parallelogram, and AC is a diagonal. Given: ∠BAC = 50° and 0° < ∠ABC = β < 70°. Let α = ∠CAD. What is the exact range of α?',
                choices=['$50°<\\alpha<90°$', '$60°\\leq\\alpha\\leq130°$', '$0°<\\alpha<130°$', '$60°<\\alpha<130°$'], correct=4,
                expl=['At A, the whole angle is α + 50°. Adjacent angles of a parallelogram add up to 180°. So, α + 50° + β = 180° and α = 130° − β.',
                      'Since 0° < β < 70°, the exact range is 60° < α < 130°: choice 4.'])
    new = _relabel(old, {'45°': '50°'}); M.set_q(q, figure=new)
    _rn_slide_figs(M, v, _rn_same(old, new))
    _rn_sub(M, v, 2, [('Angle BAC is 45. Beta — angle ABC — is between 0 and 80.', 'Angle BAC is 50. Beta — angle ABC — is between 0 and 70.'),
                      ('$\\beta+45°+\\alpha=180°$', '$\\beta+50°+\\alpha=180°$'), ('β + 45° + α = 180° appears', 'β + 50° + α = 180° appears'),
                      ('$\\alpha=135°-\\beta$', '$\\alpha=130°-\\beta$'), ('α = 135° − β appears', 'α = 130° − β appears')])
    _rn_sub(M, v, 3, [('less than 80 — and obviously', 'less than 70 — and obviously'), ('as beta approaches 80?', 'as beta approaches 70?'),
                      ('plug in 79.999 forever — we plug in 80.', 'plug in 69.999 forever — we plug in 70.'),
                      ('$\\beta=80°:\\ \\alpha=135°-80°=55°$', '$\\beta=70°:\\ \\alpha=130°-70°=60°$'), ('β = 80° → α = 55° appears', 'β = 70° → α = 60° appears'),
                      ('80 plus 45 is 125. So alpha is 55.', '70 plus 50 is 120. So alpha is 60.'), ("can't actually be 80", "can't actually be 70"),
                      ('alpha must be MORE than 55.', 'alpha must be MORE than 60.'), ('$\\alpha>55°$', '$\\alpha>60°$'), ('α > 55° appears', 'α > 60° appears'),
                      ('push beta up toward 80 — alpha shrinks toward 55', 'push beta up toward 70 — alpha shrinks toward 60'),
                      ('let alpha go below 55', 'let alpha go below 60'), ('start at 55', 'start at 60')])
    _rn_sub(M, v, 4, [('$\\beta=0°:\\ \\alpha=135°$', '$\\beta=0°:\\ \\alpha=130°$'), ('β = 0° → α = 135° appears', 'β = 0° → α = 130° appears'),
                      ('0 plus 45 plus something is 180. That something is 135.', '0 plus 50 plus something is 180. That something is 130.'),
                      ('a little less than 135.', 'a little less than 130.'), ('alpha grows toward 135.', 'alpha grows toward 130.'),
                      ('$55°<\\alpha<135°$', '$60°<\\alpha<130°$'), ('55° < α < 135° appears', '60° < α < 130° appears'),
                      ('could equal 55 or 135. That would need beta to be exactly 80 or 0', 'could equal 60 or 130. That would need beta to be exactly 70 or 0')])

    # --- Question 9 (g181): lines a, b; YZ, WX, UV; VX -> lines c, d; KL, MN, PQ; NQ
    q, v = 'geo38-g181', 'solve-geo38-g181'
    mp = dict(Y='K', Z='L', W='M', X='N', U='P', V='Q')
    _rn_q(M, q, stem='Lines c and d are parallel. Segments KL, MN and PQ join them, making acute angles α, β and γ with line c, respectively. '
                     'Given: α < β < γ < 90°. Which statement cannot be true?',
          choices=['$MN<KL$', '$NQ>MN$', '$PQ>MN$', '$PQ<KL$'], correct=3,
          expl=['All three segments cross the same distance between the parallel lines. A smaller acute angle with the parallel line needs a longer segment. '
                'Thus KL > MN > PQ. The statement PQ > MN is impossible: choice 3.',
                'NQ lies along d, and its length depends on how far apart the segments are.'],
          figure=_relabel(M.q(q)['questionVisual']['svg'], dict(mp, a='c', b='d')))
    _rn_slide_figs(M, v, lambda s: _relabel(s, dict(mp, a='c', b='d')))
    _rn_sub(M, v, 2, [('Lines a and b are parallel.', 'Lines c and d are parallel.'), ('gamma with line a.', 'gamma with line c.'),
                      ('between line a and line b.', 'between line c and line d.')])
    _rn_video_text(M, v, lambda t: _rn_letters(t, mp).replace('QN', 'NQ'))

    # --- Question 10 (g182): radius 5, P 6 from B, Q 8 from A -> radius 6, P 9 from A, Q 7 from B (now Q is closer)
    q, v = 'geo38-g182', 'solve-geo38-g182'
    old = _rn_q(M, q, stem=' A solid sphere has radius 6 cm and diameter AB. Cut P is perpendicular to AB at a point 9 cm from A. Cut Q is perpendicular to AB at a point 7 cm from B. '
                           'Each cut is considered separately. Which produces the greater total surface area of the two resulting pieces? ',
                choices=['Cut P', 'The totals are equal.', 'Cut Q', CBD38], correct=3,
                expl=['The center is 6 cm from A and from B. Cut P is $9-6=3$ cm from the center. Cut Q is $7-6=1$ cm from the center.',
                      'Each cut keeps the whole sphere surface and adds two flat disks. Closer to the center means a bigger disk: '
                      '$\\rho^2=36-9=27$ for P, $\\rho^2=36-1=35$ for Q.',
                      'Cut Q gives the greater total: choice 3.'], figure=rn_fig_g182())
    _rn_slide_figs(M, v, _rn_same(old, rn_fig_g182()))
    _rn_sub(M, v, 2, [('A solid sphere, radius 5, diameter AB. Cut P is perpendicular to AB, 6 from B. Cut Q is perpendicular to AB, 8 from A.',
                       'A solid sphere, radius 6, diameter AB. Cut P is perpendicular to AB, 9 from A. Cut Q is perpendicular to AB, 7 from B.')])
    _rn_sub(M, v, 3, [('P: $6-5=1$ from O', 'P: $9-6=3$ from O'), ('Q: $8-5=3$ from O', 'Q: $7-6=1$ from O'),
                      ('P: 6 − 5 = 1 from O appears', 'P: 9 − 6 = 3 from O appears'), ('Q: 8 − 5 = 3 from O appears', 'Q: 7 − 6 = 1 from O appears'),
                      ('Radius 5. Cut P is 6 from B — 1 past the center. Cut Q is 8 from A — 3 past the center.',
                       'Radius 6. Cut P is 9 from A — 3 past the center. Cut Q is 7 from B — 1 past the center.'),
                      ('Cut P is closer to the center', 'Cut Q is closer to the center'), ('Circle choice 2', 'Circle choice 3'), ('Cut P — choice two.', 'Cut Q — choice three.')])
    _rn_sub(M, v, 4, [('$\\rho^2+d^2=5^2$', '$\\rho^2+d^2=6^2$'), ('ρ² + d² = 25 → P: 24, Q: 16 appears', 'ρ² + d² = 36 → P: 27, Q: 35 appears'),
                      ('P: $\\rho^2=24$ · Q: $\\rho^2=16$', 'P: $\\rho^2=27$ · Q: $\\rho^2=35$'), ('P: ρ² = 24 · Q: ρ² = 16 appears', 'P: ρ² = 27 · Q: ρ² = 35 appears'),
                      ("P: 25 minus 1 — 24. Q: 25 minus 9 — 16. P's faces are bigger.", "P: 36 minus 9 — 27. Q: 36 minus 1 — 35. Q's faces are bigger.")])

    # --- Question 11 (g183): 3, 6, 75 and 45 degrees -> 4, 8, 70 and 30 degrees (side 2 : 1 kept for the triangle-inequality method)
    q, v = 'geo38-g183', 'solve-geo38-g183'
    old = _rn_q(M, q, stem='ABCD and EFGH are parallelograms. Given: AB = EF = 4 cm, BC = FG = 8 cm, ∠ABC = 70°, and ∠EFG = 30°. Which statement cannot be true?',
                expl=['Take the 8-cm sides as bases. Then the area is $8\\cdot h$, where $h$ is the height from A (or from E).',
                      'The side of 4 leans at $70°$ in ABCD and at $30°$ in EFGH. Up to $90°$, a wider angle gives a taller height. '
                      'With $30°$, the height is half of 4: $h=2$. With $70°$, it is more than that (and less than 4).',
                      'Same base, taller height: ABCD has the greater area. Equal areas cannot be true: choice 1.',
                      'The other claims are true: $AC>8-4=4=AB$ (triangle inequality), $AC>EG$ (a wider angle between the same sides), '
                      'and both perimeters are $2(4+8)=24$.'], figure=rn_fig_g183())
    _rn_slide_figs(M, v, _rn_same(old, rn_fig_g183()))
    _rn_sub(M, v, 2, [('AB and EF are 3, BC and FG are 6. Angle ABC is 75, angle EFG is 45.', 'AB and EF are 4, BC and FG are 8. Angle ABC is 70, angle EFG is 30.'),
                      ('$6-3<AC<6+3$', '$8-4<AC<8+4$'), ('6 − 3 < AC < 6 + 3 appears', '8 − 4 < AC < 8 + 4 appears'),
                      ('Less than the sum — 9. More than the difference — 3. So AC is between 3 and 9.', 'Less than the sum — 12. More than the difference — 4. So AC is between 4 and 12.'),
                      ("It can't be 3 — it's definitely more than 3. And AB is 3.", "It can't be 4 — it's definitely more than 4. And AB is 4."),
                      ('sides 3 and 6 with 60 degrees', 'sides 4 and 8 with 60 degrees'),
                      ('$60°$ with sides $3, 6$: a $30°$-$60°$-$90°$ triangle, $AC=3\\sqrt3\\approx5.2$', '$60°$ with sides $4, 8$: a $30°$-$60°$-$90°$ triangle, $AC=4\\sqrt3\\approx6.9$'),
                      ("'60° with sides 3, 6: 30-60-90' appears", "'60° with sides 4, 8: 30-60-90' appears"),
                      ("6 is twice 3. It's the 30-60-90 triangle: the right angle is at A, and AC is 3 root 3 — about 5.2.",
                       "8 is twice 4. It's the 30-60-90 triangle: the right angle is at A, and AC is 4 root 3 — about 6.9."),
                      ('Our angle is 75 — wider than 60. The angle opened, and AC got even longer than 5.2.', 'Our angle is 70 — wider than 60. The angle opened, and AC got even longer than 6.9.')])
    _rn_sub(M, v, 3, [('AB equals EF — 3. BC equals FG — 6.', 'AB equals EF — 4. BC equals FG — 8.'), ('the angle: 75 against 45.', 'the angle: 70 against 30.')])
    _rn_sub(M, v, 4, [('Both have base 6.', 'Both have base 8.'), ('The side of 3 leans at 75 in the first one, at 45 in the second.', 'The side of 4 leans at 70 in the first one, at 30 in the second.'),
                      ('Same base $6$, taller height', 'Same base $8$, taller height'), ('Same base 6, taller height', 'Same base 8, taller height')])
    _rn_sub(M, v, 5, [('Push 75 up to 80 — close to 90. Pull 45 down to 30.', 'Push 70 up to 85 — close to 90. Pull 30 down to 15.'),
                      ('max area $6\\cdot3=18$', 'max area $8\\cdot4=32$'), ('max area 6 · 3 = 18 appears', 'max area 8 · 4 = 32 appears'),
                      ('the maximum area: 6 times 3, 18.', 'the maximum area: 8 times 4, 32.'), ('105 degrees gives the same height as 75', '110 degrees gives the same height as 70')])
    _rn_sub(M, v, 6, [('$P=2(3+6)=18$ for both', '$P=2(4+8)=24$ for both'), ('P = 2(3 + 6) = 18 for both appears', 'P = 2(4 + 8) = 24 for both appears')])

    # --- Question 12 (g184): letters KLM, N, E -> RST, P, H; plug-in angles 80 / 10 -> 70 / 20
    q, v = 'geo38-g184', 'solve-geo38-g184'
    mp = dict(K='R', L='S', M='T', N='P', E='H')
    Q0 = M.q(q)
    old = _rn_q(M, q, stem=_rn_letters(Q0['stemRich'], mp), choices=[_rn_letters(c, mp) for c in Q0['choicesRich']],
                expl=[_rn_letters(e, mp) for e in Q0['explanation']])
    new = _relabel(old, dict(K='R', L='S', M='T', N='P')).replace('bisector from M', 'bisector from T'); M.set_q(q, figure=new)
    _rn_slide_figs(M, v, _rn_same(old, new))
    _rn_video_text(M, v, lambda t: _rn_letters(t, mp))
    _rn_sub(M, v, 4, [('Say alpha is 80.', 'Say alpha is 70.'),
                      ('$\\alpha=80°\\Rightarrow\\angle T=10°\\Rightarrow x=5°$', '$\\alpha=70°\\Rightarrow\\angle T=20°\\Rightarrow x=10°$'),
                      ('α = 80° → x = 5° appears', 'α = 70° → x = 10° appears'), ('80, 90 — angle T is 10. So, x is 5.', '70, 90 — angle T is 20. So, x is 10.'),
                      ('But alpha could be 10 — a sharper angle.', 'But alpha could be 20 — a sharper angle.'),
                      ('$\\alpha=10°\\Rightarrow\\angle T=80°\\Rightarrow x=40°$', '$\\alpha=20°\\Rightarrow\\angle T=70°\\Rightarrow x=35°$'),
                      ('α = 10° → x = 40° appears', 'α = 20° → x = 35° appears'), ('10, 90 — angle T is 80. So, x is 40.', '20, 90 — angle T is 70. So, x is 35.')])

    # --- Question 13 (g185): square and regular octagon -> equilateral triangle and regular hexagon; new choice order
    q, v = 'geo38-g185', 'solve-geo38-g185'
    _rn_q(M, q, stem='An equilateral triangle and a regular hexagon are compared under each of the conditions below. Which statement is false?',
          choices=['If their areas are equal, the triangle has the greater perimeter.', 'If both are inscribed in the same circle, the hexagon has the greater area.',
                   'If their perimeters are equal, the hexagon has the greater area.', 'If both are inscribed in the same circle, the triangle has the greater perimeter.'],
          correct=4, expl=['For equal perimeters, a regular hexagon encloses more area than an equilateral triangle. For equal areas, it needs less perimeter.',
                           'In the same circle, the hexagon has both the greater area and the greater perimeter. So, the claim that the inscribed triangle has the greater perimeter is false: choice 4.'])
    _rn_slide_figs(M, v, lambda s: rn_fig_g185())
    _rn_video_text(M, v, lambda t: t.replace('A square and a regular octagon', 'An equilateral triangle and a regular hexagon')
                   .replace('square', 'triangle').replace('octagon', 'hexagon'))
    _rn_sub(M, v, 3, [('Cross out choice 4', 'Cross out choice 1')])
    _rn_sub(M, v, 4, [('Cross out choice 1', 'Cross out choice 2'), ('Circle choice 2', 'Circle choice 4'), ('Choice two.', 'Choice four.')])

    # --- Question 14 (g186): block, answers 10, 11, 12, 15 -> block of cheese, answers 10, 12, 16, 11
    q, v = 'geo38-g186', 'solve-geo38-g186'
    _rn_q(M, q, stem='A solid rectangular block of cheese is cut into two pieces by one straight cut (one plane through its interior). '
                     'Which of the following cannot be the total number of faces of the two pieces?',
          choices=['$10$', '$12$', '$16$', '$11$'], correct=3,
          expl=['Each of the six original faces ends up in at most two pieces, so it gives at most two faces. The cut adds exactly two new faces.',
                'The total is at most $6\\cdot2+2=14$. So, 16 is impossible: choice 3. (10, 11 and 12 are all possible.)'])
    _rn_sub(M, v, 2, [('A solid block is cut into two pieces', 'A block of cheese is cut into two pieces'), ('Cross out choice 1', 'Cross out choice 2')])
    _rn_sub(M, v, 3, [('Answers $10, 11, 12, 15$ · the extremes: $10$ and $15$', 'Answers $10, 11, 12, 16$ · the extremes: $10$ and $16$'),
                      ('Answers 10, 11, 12, 15 → edges 10 and 15 appears', 'Answers 10, 11, 12, 16 → extremes 10 and 16 appears'),
                      ('Here the extremes are 10 and 15.', 'Here the extremes are 10 and 16.')])
    _rn_sub(M, v, 4, [('Cross out choice 3', 'Cross out choice 1'), ('So, the insight points to 15.', 'So, the insight points to 16.'),
                      ('Circle choice 2', 'Circle choice 3'), ('15 — choice two.', '16 — choice three.')])
    _rn_sub(M, v, 5, [('Why not 15', 'Why not 16'), ('14 at most. 15 is impossible.', '14 at most. 16 is impossible.')])

    # --- Question 15 (g187): two rows (2n + 4, n = 3 -> 10) -> three rows (2n + 6, n = 3 -> 12)
    q, v = 'geo38-g187', 'solve-geo38-g187'
    old = _rn_q(M, q, stem=' A rectangle tightly contains three rows of n congruent circles of radius r, where n ≥ 2. The circles are arranged in aligned columns and are tangent to their neighbors, '
                           'as shown in the accompanying figure. How many points of tangency are there between the circles and the sides of the rectangle? ',
                choices=['$2n+4$', '$5n$', '$2n+6$', '$n^2+4$'], correct=3,
                expl=['The top side touches the n circles of the top row, and the bottom side touches the n circles of the bottom row. The middle row touches neither.',
                      'The left side touches 3 circles (one in each row), and the right side touches 3 circles. Total: $n+n+3+3=2n+6$: choice 3.',
                      'Contacts between circles are not counted.'], figure=rn_fig_g187())
    _rn_slide_figs(M, v, _rn_same(old, rn_fig_g187()))
    _rn_lines(M, v, 2, [
        {'say': 'A rectangle tightly holds three rows of n equal circles, radius r, each tangent to its neighbors.'},
        {'say': 'How many tangency points are there between the circles and the sides of the rectangle?'},
        {'say': 'Start with understanding. The rectangle has 4 sides: the bottom, the top, the left side and the right side.'},
        {'say': 'Check how many tangency points each side has with the circles. Start with the bottom.'},
        {'say': 'Each circle in the bottom row touches the bottom once. n circles — n tangency points.'},
        {'appear': 1, 'label': 'Bottom: n · top: n appears'},
        {'say': 'And by symmetry the same for the top: the top row — n points. The middle row touches neither.'},
        {'say': "Now the right side. Here the number doesn't depend on n: one circle from each row touches it — 3 points. The left side too — 3."},
        {'appear': 2, 'label': 'Left: 3 · right: 3 appears'},
        {'appear': 3, 'label': 'Total: 2n + 6 appears'},
        {'say': 'Altogether: 2n plus 6. Careful — with two rows it would be 2n plus 4. Here there are three rows.'},
        {'draw': 'Circle choice 3'},
        {'say': 'Choice three. That was the understanding approach.'}])
    _rn_sub(M, v, 2, [('Left: $2$ · right: $2$', 'Left: $3$ · right: $3$'), ('Total: $2n+4$', 'Total: $2n+6$')])
    _rn_lines(M, v, 3, [
        {'say': "Now let's solve it by plugging in. You can plug in any number for n — usually small ones."},
        {'say': 'But in questions like this, plugging in 1 or 2 usually gives two or more matching answers.'},
        {'appear': 1, 'label': 'n = 2: 5n = 10 and 2n + 6 = 10 appears'},
        {'say': 'Look — n equals 2 gives 10 for two different answers.'},
        {'say': 'So plug in 3: small enough to count easily — and usually only one answer fits.'},
        {'draw': 'Sketch three rows of 3 circles in a rectangle and mark the tangency points'},
        {'say': 'Count: 3 on the top, 3 at the bottom, 3 on each side — 12.'},
        {'appear': 2, 'label': 'n = 3: count = 12 appears'},
        {'say': "Plug 3 into the answers. Anything that isn't 12 — out."},
        {'appear': 3, 'label': '10, 15, 12, 13 appears'},
        {'say': '2n plus 4 — 10, out. 5n — 15, out. n squared plus 4 — 13, out. 2n plus 6 — 12.'},
        {'draw': 'Circle choice 3'},
        {'say': 'Choice three.'},
        {'say': "That's it — we've finished geometric understanding, and in fact we've finished geometry altogether."},
        {'say': "What can I wish you? That you do as well in the other topics as you do in geometry — and I'm waiting for you there too."},
        {'say': "Let's go to the summary of this topic."}])
    _rn_sub(M, v, 3, [('$n=2$: $4n=8$ and $2n+4=8$', '$n=2$: $5n=10$ and $2n+6=10$'), ('$n=3$: count $=10$', '$n=3$: count $=12$'),
                      ('$8,\\ 12,\\ 11,\\ 10$', '$10,\\ 15,\\ 12,\\ 13$')])


# ---------------------------------------------------------------- practice: the 20 Hebrew-derived questions
def rn_practice_questions(M):
    P_ = lambda n: 'geo38-core-p%02d' % n
    fig = lambda n: M.q(P_(n))['questionVisual']['svg']
    _rn_q(M, P_(1), stem='Three circles are externally tangent to one another. Two have radius 3 cm and the third has radius 5 cm. What type of triangle is formed by joining their centers?',
          choices=['A right triangle', 'An isosceles triangle', 'An obtuse triangle', 'A scalene triangle'], correct=2,
          expl=['The distance between the centers of two externally tangent circles is the sum of their radii. The sides are $5+3=8$, $5+3=8$ and $3+3=6$.',
                'Exactly two sides are equal: the triangle is isosceles. It is not right or obtuse: the longest side is 8, and $8^2=64<8^2+6^2=100$. Choice 2.'],
          figure=rn_fig_p01())
    _rn_q(M, P_(2), stem='ABCD and DEFG are squares. E lies on DC, and their top sides AD and DG lie on one straight line. Given: FG = 3 cm. What is the area of triangle CFG (in cm²)?',
          choices=['$3$', '$4.5$', '$9$', CBD38], correct=2,
          expl=['The big square is not given — but test before you choose "cannot be determined". Take GF as the base of triangle CFG: $GF=3$.',
                'The height is the distance from C to line GF. C lies on line DC. DE is the side of the small square opposite GF. So, line DC is parallel to GF. '
                'The distance between them is $DG=3$, whatever the size of the big square.',
                'Area $=\\frac{3\\cdot3}{2}=4.5$ cm². Choice 2.',
                'Two figures check: big side 6 or big side 10 — C slides along line DC, and the area is 4.5 both times. The answer is fixed.'],
          figure=_relabel(fig(2), {'2 cm': '3 cm'}))
    _rn_q(M, P_(3), stem=' K, M and P lie on line s. KL, MN and PQ are perpendicular to s, and ∠LNQ = 90°. Which of the following statements is necessarily true? ',
          choices=['$KM=MP$', '$LN=NQ$', '$KL=PQ$', 'None of the above is necessarily true.'], correct=4,
          expl=['Try one example with coordinates: $K(0, 9)$, $M(0, 5)$, $P(0, 0)$, $L(3, 9)$, $N(1, 5)$, $Q(11, 0)$. KL, MN and PQ are all horizontal. So, they are perpendicular to s.',
                'Check the right angle with Pythagoras: $LN^2=2^2+4^2=20$, $NQ^2=10^2+5^2=125$, $LQ^2=8^2+9^2=145=20+125$. So, ∠LNQ = 90°.',
                'But $KL=3\\ne11=PQ$, $KM=4\\ne5=MP$, and $LN=\\sqrt{20}\\ne\\sqrt{125}=NQ$. None of the claims must be true: choice 4.'],
          figure=_relabel(fig(3), dict(A='K', B='L', C='M', D='N', E='P', F='Q')))
    _rn_q(M, P_(4), stem=' P, O and Q lie on one straight line. Given: ∠TOQ = ∠SOR = 90°, with the rays ordered as shown in the accompanying figure. Let α = ∠TOS and β = ∠ROQ. Which of the following is necessarily true? ',
          choices=['$\\alpha<\\beta$', '$\\alpha=\\beta$', '$\\alpha>\\beta$', CBD38], correct=2,
          expl=['Let θ = ∠SOQ. Then α + θ = 90° and β + θ = 90°. Subtracting θ gives α = β: choice 2.'],
          figure=_relabel(fig(4), dict(A='P', B='Q', C='R', D='S', E='T')))
    _rn_q(M, P_(5), stem=' In acute triangle PQR, S is the point on QR closest to P. Which of the following statements is necessarily true? ',
          choices=['$PS\\perp QR$', '$PQ=PR$', '$QS=SR$', '$\\angle QPS=\\angle SPR$'], correct=1,
          expl=['The shortest distance from a point to a line is measured along a perpendicular. The triangle is acute. So, the foot of the perpendicular lies inside QR, and PS ⟂ QR: choice 1.'],
          figure=_relabel(fig(5), dict(A='P', B='Q', C='R', D='S')))
    _rn_q(M, P_(6), stem='A right isosceles triangle has its right-angle vertex K fixed on a horizontal line. At first, L lies to the right of K on the line, and M lies directly above K. '
                         'The triangle rotates counterclockwise through 90°, until M lies to the left of K on the line. What is the combined path traced by L and M?',
          choices=['A quarter circle', 'Two straight segments', 'A semicircle', 'A full circle'], correct=3,
          expl=['KL = KM. L traces the upper-right quarter circle, and M traces the upper-left quarter circle. Both have center K and the same radius.',
                'Together they form the upper semicircle: choice 3.'], figure=rn_fig_p06())
    _rn_q(M, P_(7), stem='A square napkin with side 15 cm is cut into two pieces by one straight cut. Which pair of shapes cannot be obtained?',
          choices=['Two rectangles', 'Two non-square rhombi', 'Two triangles', 'Two trapezoids, each with exactly one pair of parallel sides'], correct=2,
          expl=['A diagonal gives two triangles. A slanted cut joining opposite sides gives two trapezoids. A cut parallel to a side gives two rectangles.',
                'For two quadrilaterals, the cut must join opposite sides, and each piece keeps two right-angle corners. A rhombus with a right angle is a square. '
                'So, neither piece can be a non-square rhombus: choice 2.'])
    _rn_q(M, P_(8), stem='PQRS is a convex kite with PQ = PS and RQ = RS. Its diagonals have lengths PR = 12 cm and QS = 8 cm. What is its perimeter?',
          choices=['$40$ cm', '$20$ cm', '$32$ cm', CBD38], correct=4,
          expl=['PR is the axis of symmetry. So, it cuts QS in half at a right angle: each half is 4. But nothing says where PR is cut.',
                'This is the rare case where the answer really cannot be determined. The two-figures test proves it.',
                'Figure 1: PR is cut into $6+6$. All four sides are $\\sqrt{6^2+4^2}=\\sqrt{52}$. Perimeter $4\\sqrt{52}\\approx28.8$.',
                'Figure 2: PR is cut into $2+10$. The sides are $\\sqrt{2^2+4^2}=\\sqrt{20}$ and $\\sqrt{10^2+4^2}=\\sqrt{116}$. Perimeter $2\\sqrt{20}+2\\sqrt{116}\\approx30.5$.',
                'Both figures keep every given, and the perimeters are different. It cannot be determined: choice 4.'],
          figure=_relabel(fig(8), dict(A='P', B='Q', C='R', D='S')))
    _rn_q(M, P_(9), stem=' KLM is right-angled at L. KN bisects ∠LKM, with N on LM. P lies on KM and NP ⟂ KM. Which of the following statements is necessarily true? ',
          choices=['$KL=KP$ and $LN<NM$', '$KL<KP$ and $LN<NM$', '$KL=KP$ and $LN=NM$', '$KL>KP$ and $LN>NM$'], correct=1,
          expl=['Right triangles KLN and KPN share the hypotenuse KN and have equal angles at K. So, they are congruent. Thus KL = KP and LN = NP.',
                'In right triangle NPM, NM is the hypotenuse, and it is longer than NP. So, LN < NM: choice 1.'],
          figure=_relabel(fig(9), dict(A='K', B='L', C='M', D='N', E='P')))
    _rn_q(M, P_(10), stem='ABCD is a parallelogram containing adjacent squares AEFG and GFCH, each with side 4 cm, as shown in the accompanying figure. '
                          'How does the area of triangle HCD compare with the area of triangle ABE?',
          expl=['BE and HD are not given — but test before you choose "cannot be determined".',
                'In a parallelogram, $AD=BC$: $8+HD=BE+8$. Therefore, $HD=BE$.',
                'Both triangles are right triangles with legs 4 and the same second leg: $S_{ABE}=\\frac{4\\cdot BE}{2}=\\frac{4\\cdot HD}{2}=S_{HCD}$.',
                'Two figures check: $BE=1$ gives 2 and 2, $BE=3$ gives 6 and 6. The areas change, but they are always equal: choice 2.'])
    _rn_q(M, P_(11), stem=' Two perpendicular chords divide a circle into the four regions shown in the accompanying figure. The center O lies strictly inside region III. Which of the following is necessarily true? ',
          choices=['Area I > area II', 'Area I = area II', CBD38, 'Area I < area II'], correct=4,
          expl=['The vertical chord lies to the left of the center. Reflect region I across the vertical diameter through O. Its image lies entirely inside region II, '
                'and region II also has more area. Hence I < II: choice 4.'],
          figure=_relabel(fig(11), {'I': 'II', 'II': 'I', 'III': 'IV', 'IV': 'III'}))
    _rn_q(M, P_(12), stem=' Chords KM and LN of a circle intersect at right angles at P, and KP = PM. Region I is the part of the circle above LN and to the right of KM. '
                          'Region II is below LN and to the left of KM. Which of the following statements is necessarily true? ',
          choices=['Area I = area II', 'Area I > area II', 'Area I < area II', 'None of the other statements is necessarily true.'], correct=4,
          expl=['LN is the perpendicular bisector of KM. So, it passes through the center. But P need not be the center.',
                'If KM lies to the right of the center, I is smaller than II. If it lies to the left, I is larger. If both chords are diameters, the areas are equal. '
                'None of them must be true: choice 4.'],
          figure=_relabel(fig(12), dict(A='K', B='L', C='M', D='N', E='P')))
    _rn_q(M, P_(13), stem=' KLMN is a rhombus with ∠KLM = 50°. PQRS is a square, and KL = PQ = 6 cm. Which of the following statements is necessarily true? ',
          choices=['$KM>KL$', '$LN<PR$', 'The square has greater area than the rhombus.', 'The square has greater perimeter than the rhombus.'], correct=3,
          expl=['The square has base 6 and height 6. The rhombus also has base 6, but its side of 6 leans at $50°$. So, its height is less than 6, and its area is less than 36.',
                'The square has the greater area: choice 3.'], figure=rn_fig_p13())
    _rn_q(M, P_(14), stem=' DG is a median of triangle DEF, and H lies strictly between D and G. Let α = ∠EHG and β = ∠EDH. Which of the following is necessarily true? ',
          choices=['$\\alpha=\\beta$', '$\\alpha<\\beta$', '$\\alpha>\\beta$', CBD38], correct=3,
          expl=['HG continues DH beyond H. So, α is an exterior angle of triangle DEH, and α = β + ∠DEH. The added angle is positive. So, α > β: choice 3.'],
          figure=_relabel(fig(14), dict(K='D', L='E', M='F', N='G', P='H')))
    _rn_q(M, P_(15), stem='A drawing contains 4 horizontal segments on distinct lines and 9 vertical segments on distinct lines. The segments may be placed and given lengths freely. '
                          'Which describes all possible numbers of intersection points?',
          choices=['Every integer from 0 to 36, inclusive', 'Only multiples of 4 from 0 to 36', 'Only 36', 'Every integer from 0 to 13, inclusive'], correct=1,
          expl=['Each of the 4 horizontal segments can meet at most 9 vertical segments. So, the maximum is $4\\cdot9=36$. Separating the groups gives 0.',
                'For any count $9q+r$ with $0\\le r<9$, let q horizontal segments cross all 9 vertical ones, let one more cross exactly r of them, and let the rest cross none. '
                'The case 36 uses all 4 full rows. Every integer from 0 to 36 is possible: choice 1.'], figure=rn_fig_p15())
    _rn_q(M, P_(16), stem='ABCD is a parallelogram with BC = 7 cm. A right isosceles triangle AEB is constructed externally on AB, with right angle E and area 8 cm². '
                          'Given: EB ⟂ BC. What is the area of the parallelogram (in cm²)?',
          choices=['$16$', '$28\\sqrt2$', '$28$', CBD38], correct=3,
          expl=['The triangle: $\\frac{EB\\cdot EA}{2}=8$ and $EB=EA$. So, $EB^2=16$ and $EB=EA=4$.',
                'AE and BC are both perpendicular to EB. Two lines perpendicular to the same line are parallel: $AE\\parallel BC$. '
                'So, A is exactly as far from BC as E is: the height of the parallelogram is $EB=4$.',
                'Area $=BC\\cdot h=7\\cdot4=28$ cm². Choice 3.',
                'Traps: $28\\sqrt2=7\\cdot AB$ is true only for a rectangle, and 16 is just twice the triangle. The angle is not free here — $EB\\perp BC$ fixes it ($\\angle ABC=45°$).'],
          figure=rn_fig_p16())
    _rn_q(M, P_(17), stem=' A, B, C and D lie on one circle. The minor arc CD is 4 times the minor arc AB. P and Q may be any points strictly inside the circle, and need not be distinct. '
                          'Let α = ∠APB and β = ∠CQD. Which of the following is necessarily true? ',
          choices=['$\\beta=4\\alpha$', '$\\beta<4\\alpha$', 'None of the other relationships is necessarily true.', '$\\beta>4\\alpha$'], correct=3,
          expl=['Choose arcs AB = 20° and CD = 80°. With both vertices at the center, α = 20° and β = 80°. So, equality can hold.',
                'Keep Q at the center and move P close to the midpoint of chord AB: α approaches 180°, and β < 4α.',
                'Keep P at the center and move Q close to chord CD: β approaches 180°, more than 4α = 80°. All the vertices stay strictly inside the circle. '
                'None of the relationships must hold: choice 3.'])
    _rn_q(M, P_(18), stem='A square and a rectangle that is not a square both have perimeter 44 cm. Which of the following statements is necessarily true?',
          choices=['The square has the greater area.', CBD38, 'Their areas are equal.', 'The rectangle has the greater area.'], correct=1,
          expl=['The square has side $\\frac{44}{4}=11$ and area $11\\cdot11=121$ cm².',
                'For a fixed perimeter, the square has the greatest area of all rectangles. The other rectangle is not a square. So, its area is less than 121 (for example, $13\\cdot9=117$).',
                'The square has the greater area: choice 1.'])
    _rn_q(M, P_(19), stem='How many mutually noncongruent rhombi have perimeter 36 cm and area 63 cm²?',
          choices=['$0$', '$2$', '$1$', 'Infinitely many'], correct=3,
          expl=['Perimeter 36: every side is $\\frac{36}{4}=9$.',
                'Area = side × height: $h=\\frac{63}{9}=7$. A side of 9 that rises exactly 7 fixes how the rhombus leans. Leaning the other way gives a mirror image — the same rhombus.',
                'So there is exactly one rhombus: choice 3.'])
    _rn_q(M, P_(20), stem=' A circle has radius 5 cm. Chord AB does not pass through the center. E lies strictly between A and B, with AE = x cm and EB = 3.5 cm. Which of the following statements is necessarily true? ',
          choices=['$x<3.5$', '$x>6.5$', '$x<6.5$', '$x=6.5$'], correct=3,
          expl=['The diameter is 10 cm, and it is the longest chord. AB is not a diameter. So, AB < 10.', 'Thus $x+3.5<10$ and $x<6.5$: choice 3.'],
          figure=_relabel(fig(20), {'2.5': '3.5'}))


# ---------------------------------------------------------------- practice clean-up + order, card, canvases
def rn_practice(M):
    # copy: p26 (an easier copy of the lines-crossing type, p15). English warm-ups: keep p21 (chords and the center),
    # p24 (angles on the same arc), p25 (acute / obtuse with the squares). September items: keep q-04 (angle on a diameter),
    # q-12 and q-13 (the greatest distance - the lesson's 'Farthest apart' sends students to practice); the others repeat
    # a type the Hebrew practice already has (03, 09, 10: two fixed sides -> p13; 05: acute / obtuse -> p25; 06: slide the
    # apex -> p02, p10; 07: one plane cut -> p07; 11: shape efficiency -> p18).
    for qid in ['geo38-core-p26', 'geo38-core-p22', 'geo38-core-p23', 'geo38-core-p27',
                'q-r26-t38-03', 'q-r26-t38-05', 'q-r26-t38-06', 'q-r26-t38-07', 'q-r26-t38-09', 'q-r26-t38-10', 'q-r26-t38-11']:
        M.unplace(qid)
    P_ = lambda n: 'geo38-core-p%02d' % n
    M.practice_order(PRACT, [P_(18), P_(24), P_(21), P_(1), P_(4), 'q-r26-t38-04', 'q-r26-t38-13', P_(5), P_(25), 'q-r26-t38-12',
                             P_(20), P_(13), P_(14), P_(9), P_(6), P_(7), P_(2), P_(10), P_(16), P_(8), P_(12), P_(11), P_(19), P_(3), P_(15), P_(17)])


def rn_cards(M):
    rows = M.card(CARD)['tables'][0]['rows']
    k = next(i for i, r in enumerate(rows) if r[0] == '!Anchor')
    assert '9,12,15' in rows[k][1], rows[k]
    rows[k] = [rows[k][0], rows[k][1].replace('$9,12,15$', '$8,15,17$')]


def _rn_sync(M):
    """'Pre-loaded' notes follow the changed stems."""
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC or v['id'] in RN_RECORDED: continue
        for b in v['beats']:
            pre = b['items'][:b['pre']]
            if len(pre) == 1 and pre[0].get('k') == 'q' and b.get('canvas', '').startswith('Pre-loaded — question'):
                qid = pre[0]['qid']
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, M.q(qid)['stem'])
                M.touched_videos.add(v['id'])


def renumber_pass(M):
    rn_guided(M)
    rn_practice_questions(M)
    rn_practice(M)
    rn_cards(M)
    _rn_sync(M)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


# ===================================================================================================================
# 2026-10-07 no decimal estimates. Teacher: a student can't estimate roots or π to one decimal place. Estimates use
# whole-number benchmarks only (perfect squares, squaring, a factor into the root, 3 < π < 3.5) or another method.
# Recorded videos are never changed (any take in ~/Documents/Course.recordings).
import glob as _nd_glob, os as _nd_os, re as _nd_re


def _nd_recorded(vid):
    # only takes recorded BEFORE this change was first built (2026-10-07 12:40Z) keep the old video; takes recorded
    # later were made with the rewritten slides, so the rewrite must stay
    pat = _nd_re.compile(_nd_re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _nd_glob.glob(_nd_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_nd_os.path.basename(f))
        if m and m.group(1) < '2026-10-07T12-40-00': return True
    return False


def _nd_n(M, vid, title):
    ns = [i for i, b in enumerate(M.video(vid)['beats'], 1) if b['title'] == title]
    assert len(ns) == 1, (vid, title, ns)
    return ns[0]


def _nd_lines(M, vid, title, subs):
    """subs: [(kind, old, new)], kind 'say' or 'draw'; new is a str or a list of str of the same kind."""
    n = _nd_n(M, vid, title)

    def fn(ls):
        ls = list(ls)
        for kind, old, new in subs:
            k = [i for i, l in enumerate(ls) if l.get(kind) == old]
            assert len(k) == 1, (vid, title, old)
            ls[k[0]:k[0] + 1] = [{kind: x} for x in ([new] if isinstance(new, str) else new)]
        return ls
    M.edit_lines(vid, n, fn)


def _nd_item(M, vid, title, old_t, new_t, label=None):
    n = _nd_n(M, vid, title); b = M.slide(vid, n)
    k = [i for i, it in enumerate(b['items']) if it.get('t') == old_t]
    assert len(k) == 1, (vid, title, old_t)
    b['items'][k[0]]['t'] = new_t
    if label is not None:
        for l in b['lines']:
            if l.get('appear') == k[0]: l['label'] = label
    M.touched_videos.add(vid)


def _nd_expl(M, qid, subs):
    """subs: [(index, old_start, new)]; new None drops the paragraph."""
    ex = list(M.q(qid)['explanation'])
    for i, start, new in sorted(subs, key=lambda x: -x[0]):
        assert ex[i].startswith(start), (qid, i, ex[i][:70])
        if new is None: ex.pop(i)
        else: ex[i] = new
    M.set_q(qid, expl=ex)


def no_decimal_estimates(M):
    # solve-geo38-g183 · the 60° anchor: AC = 4√3 = √48 (no 6.9)
    v = 'solve-geo38-g183'
    if not _nd_recorded(v):
        _nd_item(M, v, 'AC against AB', r'$60°$ with sides $4, 8$: a $30°$-$60°$-$90°$ triangle, $AC=4\sqrt3\approx6.9$',
                 r'$60°$ with sides $4, 8$: a $30°$-$60°$-$90°$ triangle, $AC=4\sqrt3=\sqrt{48}$')
        _nd_lines(M, v, 'AC against AB', [
            ('say', "8 is twice 4. It's the 30-60-90 triangle: the right angle is at A, and AC is 4 root 3 — about 6.9.",
             "8 is twice 4. It's the 30-60-90 triangle: the right angle is at A, and AC is 4 root 3 — root 48. Almost root 49, which is 7."),
            ('say', "Our angle is 70 — wider than 60. The angle opened, and AC got even longer than 6.9.",
             "Our angle is 70 — wider than 60. The angle opened, and AC got even longer than root 48.")])
    # geo-175 · Farthest apart: √145 is just over √144 = 12 (board had 12.04)
    v = 'geo-175'
    if not _nd_recorded(v):
        _nd_item(M, v, 'Farthest apart', r'Cylinder $h=9$, $r=4$: $\sqrt{9^2+8^2}=\sqrt{145}\approx12.04$',
                 r'Cylinder $h=9$, $r=4$: $\sqrt{9^2+8^2}=\sqrt{145}>\sqrt{144}=12$')
    _nd_expl(M, 'q-r26-t38-12', [(1, '$EB=2$',
             '$EB=2$ and $EC=10-2=8$. $EA=\\sqrt{2^2+4^2}=\\sqrt{20}=2\\sqrt5$. $ED=\\sqrt{8^2+4^2}=\\sqrt{80}=4\\sqrt5$, more than $\\sqrt{64}=8$.')])
    _nd_expl(M, 'geo38-core-p08', [
        (2, 'Figure 1:', 'Figure 1: PR is cut into $6+6$. All four sides are $\\sqrt{6^2+4^2}=\\sqrt{52}$. '
                         'Perimeter $4\\sqrt{52}=\\sqrt{16\\cdot52}=\\sqrt{832}$, less than $\\sqrt{900}=30$.'),
        (3, 'Figure 2:', 'Figure 2: PR is cut into $1+11$. The sides are $\\sqrt{1^2+4^2}=\\sqrt{17}$ and $\\sqrt{11^2+4^2}=\\sqrt{137}$. '
                         'Perimeter $2\\sqrt{17}+2\\sqrt{137}$, more than $2\\sqrt{16}+2\\sqrt{121}=8+22=30$.')])


_apply_before_no_decimal_estimates = apply


def apply(M):
    _apply_before_no_decimal_estimates(M)
    no_decimal_estimates(M)   # 2026-10-07 no decimal estimates: runs last
