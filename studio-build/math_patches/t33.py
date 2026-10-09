"""Topic 33 - Circles. Course review 2026-09 fixes.
See t33_CHANGES.md for the plain-language list."""
import math, re
from dsl import T, H, A, D, Q
from math_api import VIS, _word

TOPIC = 33
LEARN1, FOUND, LEARN2, ADVP = 'geo33-learn-1', 'geo33-foundation-practice', 'geo33-learn-2', 'geo33-advanced-practice'
GID = ['q-r26-t33-%02d' % k for k in range(1, 21)]
TOOLS = 'r26-t33-more-tools'

# ================================================================================================
# SVG toolkit - the same style as the existing geometry figures
# (ink #203344, teal #087f83, shade #d5f1ed, DejaVu Sans 20 / angle labels 18, circle r = 109.5 at (320, 180))
# ================================================================================================
INK, TEAL, FILL = '#203344', '#087f83', '#d5f1ed'
CX, CY, R = 320.0, 180.0, 109.5
FONT = 'font-family="DejaVu Sans,Arial,sans-serif"'


def _svg(label, body, vb='0 0 640 360'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, label, label, body))


def _t(x, y, s, size=20, color=INK, italic=False):
    return ('<text x="%.3f" y="%.3f" text-anchor="middle" dominant-baseline="middle" fill="%s" %s font-size="%d"%s>%s</text>'
            % (x, y, color, FONT, size, ' font-style="italic"' if italic else '', s))


def _c(cx, cy, r, fill='none', stroke=INK, w=2.5):
    return '<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s" stroke="%s" stroke-width="%s"/>' % (cx, cy, r, fill, stroke, w)


def _dot(p):
    return '<circle cx="%.3f" cy="%.3f" r="3.2" fill="%s"/>' % (p[0], p[1], INK)


def _l(p, q, color=INK, w=2.5, dash=False):
    return ('<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="%s"%s/>'
            % (p[0], p[1], q[0], q[1], color, w, ' stroke-dasharray="6 5"' if dash else ''))


def _poly(pts, fill='none', stroke=INK, w=2.5):
    return ('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>'
            % (' '.join('%.3f,%.3f' % p for p in pts), fill, stroke, w))


def _P(deg, r=R, c=(CX, CY)):
    """point on a circle; deg in the usual math sense (counterclockwise, 0 = right)."""
    a = math.radians(deg)
    return (c[0] + r * math.cos(a), c[1] - r * math.sin(a))


def _lab(deg, s, r=R, c=(CX, CY), off=19):
    return _t(*_P(deg, r + off, c), s=s)


def _dir(p, q):
    return math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0]))


def _angle(v, p1, p2, rad=26, label=None, lr=None, size=18, color=TEAL):
    """angle mark at vertex v between rays v->p1 and v->p2 (the smaller angle) + optional label on the bisector."""
    a1, a2 = _dir(v, p1), _dir(v, p2)
    d = (a2 - a1) % 360
    if d > 180: a1, a2, d = a2, a1, 360 - d
    s, e = _P(a1, rad, v), _P(a2, rad, v)
    out = ('<path d="M %.3f %.3f A %.3f %.3f 0 0 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="2"/>'
           % (s[0], s[1], rad, rad, e[0], e[1], color))
    if label:
        out += _t(*_P(a1 + d / 2, lr or rad + 16, v), s=label, size=size, color=color)
    return out


def _right(v, p1, p2, k=9):
    a1, a2 = _dir(v, p1), _dir(v, p2)
    u, w = _P(a1, k, v), _P(a2, k, v)
    m = (u[0] + w[0] - v[0], u[1] + w[1] - v[1])
    return _l(u, m, TEAL, 1.7) + _l(m, w, TEAL, 1.7)


def _sector(a1, a2, r=R, c=(CX, CY), fill=FILL, stroke=TEAL):
    s, e = _P(a1, r, c), _P(a2, r, c)
    big = 1 if (a2 - a1) % 360 > 180 else 0
    return ('<path d="M %.3f %.3f L %.3f %.3f A %.3f %.3f 0 %d 0 %.3f %.3f Z" fill="%s" stroke="%s" stroke-width="2.2"/>'
            % (c[0], c[1], s[0], s[1], r, r, big, e[0], e[1], fill, stroke))


def _segment(a1, a2, r=R, c=(CX, CY), fill=FILL, stroke=TEAL):
    """region between the chord and the arc from a1 to a2 (counterclockwise)."""
    s, e = _P(a1, r, c), _P(a2, r, c)
    big = 1 if (a2 - a1) % 360 > 180 else 0
    return ('<path d="M %.3f %.3f A %.3f %.3f 0 %d 0 %.3f %.3f Z" fill="%s" stroke="%s" stroke-width="2.2"/>'
            % (s[0], s[1], r, r, big, e[0], e[1], fill, stroke))


def _tick(p, q, n=1):
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    a = math.atan2(q[1] - p[1], q[0] - p[0]); nx, ny = -math.sin(a), math.cos(a)
    out = ''
    for k in range(n):
        o = (k - (n - 1) / 2) * 6
        cx, cy = mx + o * math.cos(a), my + o * math.sin(a)
        out += _l((cx - 7 * nx, cy - 7 * ny), (cx + 7 * nx, cy + 7 * ny), INK, 1.8)
    return out


def _mid_label(p, q, s, off=16, side=1, size=20, color=INK, italic=False):
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    return _t(mx - side * off * math.sin(a), my + side * off * math.cos(a), s, size=size, color=color, italic=italic)


def _crop(svg, vb):
    return re.sub(r'viewBox="[^"]*"', 'viewBox="%s"' % vb, svg, count=1)


def _drop(svg, *snippets):
    """remove the elements that contain the given text snippets (each must match exactly one element)."""
    for sn in snippets:
        els = re.findall(r'<(?:text|path|circle|line|polygon)[^>]*>(?:[^<]*</text>)?', svg)
        hit = [e for e in els if sn in e]
        assert len(hit) == 1, (sn, len(hit))
        svg = svg.replace(hit[0], '', 1)
    return svg


def _relabel(svg, old_xy, new_xy=None, new_text=None):
    """move / rename the <text> element that sits at old_xy = 'x="..." y="..."'."""
    m = re.search(r'<text %s[^>]*>([^<]*)</text>' % re.escape(old_xy), svg)
    assert m, old_xy
    el = m.group(0)
    new = el
    if new_xy: new = new.replace(old_xy, 'x="%.3f" y="%.3f"' % new_xy, 1)
    if new_text is not None: new = new.replace('>%s</text>' % m.group(1), '>%s</text>' % new_text)
    return svg.replace(el, new, 1)


# ================================================================================================
# Figures: fixes of existing figures
# ================================================================================================
def _q_to_mark(svg, greek):
    """a Greek letter that the question never mentions -> '?'"""
    assert svg.count('>%s</text>' % greek) == 1, greek
    return svg.replace('>%s</text>' % greek, '>?</text>')


def fig_p03(svg):
    # the stem never names α (it asks for angle BAD) -> "?"; "140°" sat on chord CD -> smaller arc, label above CD
    svg = _q_to_mark(svg, 'α')
    svg = svg.replace('M 294.276 189.363 A 27.375 27.375 0 0 0 345.724 189.363',
                      'M 304.965 185.472 A 16.000 16.000 0 0 0 335.035 185.472')
    svg = _relabel(svg, 'x="320.000" y="222.705"', (320.0, 205.0))
    return _relabel(svg, 'x="305.000" y="195.000"', (318.0, 162.0))


def fig_g085(svg):
    # "12" sat right under O ("O12", read as OB = 12). Draw a dimension line under the diameter AB instead.
    svg = _drop(svg, 'y="206.000"')
    y = 304.0
    dim = (_l((210.5, y), (429.5, y), INK, 1.5) + _l((210.5, y - 7), (210.5, y + 7), INK, 1.5) +
           _l((429.5, y - 7), (429.5, y + 7), INK, 1.5) + _l((210.5, 186), (210.5, y - 9), INK, 1, dash=True) +
           _l((429.5, 186), (429.5, y - 9), INK, 1, dash=True) + _t(320, y + 17, '12'))
    return svg.replace('</svg>', dim + '</svg>')


def fig_p05(svg):
    # the stem never mentions the center: no O (it showed that AC passes through the center), "8" away from O
    svg = _drop(svg, 'r="3.2"', '>O</text>')
    return _relabel(svg, 'x="335.000" y="184.000"', (366.0, 164.0))


def fig_p15(svg):
    # the stem never mentions the center; the marked O showed at once that AC is a diameter
    return _drop(svg, 'r="3.2"', '>O</text>')


def fig_p20(svg):
    return _drop(svg, 'x="305.000" y="195.000"')          # "O" was printed twice


def fig_g083(svg):
    return _drop(svg, 'x="305.000" y="195.000"')          # "O" was printed twice


def fig_g091(svg):
    # the 12 angle marks at radius 74.8 joined up into an unexplained inner circle - remove them (labels stay)
    for p in re.findall(r'<path d="M [^"]*A 74\.825 74\.825[^>]*>', svg):
        svg = svg.replace(p, '', 1)
    return svg


def fig_g095(svg):
    # radius OD was already drawn (the teal edge of the shaded triangle ODC) - it is the helper line of the video.
    # Shade the region D-C-E-arc instead: no line from O to D.
    O, Dp, C, E = (277.059, 211.490), (320.0, 137.114), (448.824, 211.490), (362.941, 211.490)
    svg = _drop(svg, 'L 362.941 211.490 A')              # the white sector that covered the triangle
    old = re.search(r'<polygon points="277\.059,211\.490 320\.000,137\.114 448\.824,211\.490"[^>]*>', svg).group(0)
    svg = svg.replace(old, '<path d="M %.3f %.3f L %.3f %.3f L %.3f %.3f A 85.882 85.882 0 0 0 %.3f %.3f Z" fill="%s" '
                           'stroke="%s" stroke-width="2.2"/>' % (Dp + C + E + Dp + (FILL, TEAL)), 1)
    return svg


def fig_g098():
    # B moved from 225° to 200°: chord BF no longer runs (almost) through O and looks like a diameter
    ang = dict(A=0, G=25, F=52, E=115, D=150, B=200, C=285)
    P = {k: _P(v) for k, v in ang.items()}
    b = _c(CX, CY, R)
    for k, v in ang.items(): b += _lab(v, k)
    b += _dot((CX, CY)) + _t(305, 195, 'O')
    b += _l(P['B'], P['A']) + _l(P['B'], P['F']) + _l(P['C'], P['F']) + _l(P['C'], P['D'])
    b += _l((CX, CY), P['G']) + _l((CX, CY), P['E']) + _right((CX, CY), P['G'], P['E'], 12)
    b += _angle(P['B'], P['A'], P['F'], 34, '26°', 56) + _angle(P['C'], P['F'], P['D'], 29.2, '49°', 50)
    b += ('<path d="M %.3f %.3f A %.1f %.1f 0 0 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="6"/>'
          % (P['A'] + (R, R) + P['G'] + (TEAL,)))
    b += ('<path d="M %.3f %.3f A %.1f %.1f 0 0 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="6"/>'
          % (P['E'] + (R, R) + P['D'] + (TEAL,)))
    return _svg('Two highlighted arcs determined by inscribed angles', b)


def fig_p11():
    # "144°" did not fit inside the thin angle BOC and ran over the chord: the angle is given in the stem, so the
    # figure no longer labels it. The asked angle is marked "?" (the stem has no α).
    r, O = 75.0, (320.0, 262.0)
    B, C = _P(162, r, O), _P(18, r, O)
    Ap = (320.0, O[1] - r / math.cos(math.radians(72)))
    b = _c(O[0], O[1], r) + _poly([Ap, B, C]) + _l(O, B) + _l(O, C) + _dot(O)
    b += _t(O[0], O[1] + 20, 'O') + _t(Ap[0], Ap[1] - 16, 'A') + _t(B[0] - 20, B[1], 'B') + _t(C[0] + 20, C[1], 'C')
    b += _angle(B, Ap, C, 22, '?', 36)
    return _svg('Tangents and a chord from a common external point', b)


def fig_p19(svg):
    return _relabel(svg, 'x="305.000" y="195.000"', (339.0, 172.0))


def fig_adv_p04(svg):
    svg = _relabel(svg, 'x="332.167" y="162.000"', (332.0, 170.0))
    return _relabel(svg, 'x="248.109" y="212.676"', (227.0, 211.0))


def fig_adv_p11(svg):
    return _relabel(svg, 'x="356.312" y="230.317"', (381.0, 226.0))


def fig_g101(svg):
    return _relabel(svg, 'x="295.667" y="200.000"', (309.0, 197.0))


def fig_adv_p15():
    # sides 6, 10, 14, 10 and radii 2, 4, 6, 8 as before - but now B and D (and A and C) do not touch
    u = {'B': (0.0, 0.0), 'D': (14.0, 0.0)}
    ax = (36 - 100 + 196) / 28.0; u['A'] = (ax, -math.sqrt(36 - ax * ax))
    cx = (100 - 196 + 196) / 28.0; u['C'] = (cx, math.sqrt(100 - cx * cx))
    rad = dict(A=2, B=4, C=6, D=8)
    k = 12.6
    X = lambda p: (320 + k * (p[0] - 9), 180 + k * (p[1] - 3.67))
    b = ''
    for n in 'ABCD': b += _c(*X(u[n]), r=k * rad[n]) + _dot(X(u[n]))
    b += _poly([X(u[n]) for n in 'ABCD'], stroke=TEAL)
    off = dict(A=(0, -13), B=(-17, 0), C=(-4, 18), D=(17, 0))
    for n in 'ABCD':
        x, y = X(u[n]); b += _t(x + off[n][0], y + off[n][1], n)
    return _svg('Four circles tangent to their neighbors', b)


def fig_adv_p26():
    # right triangle with legs 6 and 8 and its inscribed circle (no figure before)
    k = 26.0
    C0 = (250.0, 300.0)                       # right angle
    Bp, Ap = (C0[0] + 8 * k, C0[1]), (C0[0], C0[1] - 6 * k)
    I = (C0[0] + 2 * k, C0[1] - 2 * k)
    b = _poly([Ap, C0, Bp]) + _c(I[0], I[1], 2 * k) + _right(C0, Ap, Bp, 12)
    b += _t(C0[0] - 18, (C0[1] + Ap[1]) / 2, '6') + _t((C0[0] + Bp[0]) / 2, C0[1] + 20, '8')
    return _svg('A circle inscribed in a right triangle', b)


def fig_quad(svg_label, with_o):
    # inscribed quadrilateral that is clearly not a rectangle: angle A = 70°, angle C = 110°
    ang = dict(A=110, B=190, C=260, D=330)
    P = {k: _P(v) for k, v in ang.items()}
    b = _c(CX, CY, R)
    for k, v in ang.items(): b += _lab(v, k)
    b += _poly([P['A'], P['B'], P['C'], P['D']])
    b += _angle(P['A'], P['B'], P['D'], 22, 'α', 40) + _angle(P['C'], P['D'], P['B'], 22, 'β', 40)
    if with_o: b += _dot((CX, CY)) + _t(CX + 4, CY - 17, 'O')
    return _svg(svg_label, b, '171.5 42.7 301.2 272.8')


def fig_quarters():
    # the circle in quarters (the teacher draws the line that makes the eighth)
    b = _sector(90, 180) + _sector(180, 270, fill='#fff8eb', stroke='#d6b88f') + \
        _sector(270, 360, fill='#fff8eb', stroke='#d6b88f') + _sector(0, 90, fill='#fff8eb', stroke='#d6b88f')
    return _svg('A circle in quarters, one quarter shaded', b + _dot((CX, CY)), '184.5 44.5 271.0 271.0')


def fig_nested_tri(svg):
    # the inner triangle upside down: its vertices are the midpoints of the outer sides - 4 equal triangles
    return svg.replace('points="320.000,121.600 269.424,209.200 370.576,209.200"',
                       'points="320.000,238.400 269.424,150.800 370.576,150.800"')


# ================================================================================================
# Figures: new lesson / question figures
# ================================================================================================
def fig_equal_chords():
    ang = dict(A=160, B=95, C=300, D=235)
    P = {k: _P(v) for k, v in ang.items()}
    O = (CX, CY)
    b = _c(CX, CY, R) + _l(P['A'], P['B']) + _l(P['C'], P['D'])
    for k in 'ABCD': b += _l(O, P[k], INK, 1.8, dash=True)
    b += _tick(P['A'], P['B']) + _tick(P['C'], P['D'])
    b += _angle(O, P['A'], P['B'], 24) + _angle(O, P['C'], P['D'], 24)
    for k, v in ang.items(): b += _lab(v, k)
    b += _dot(O) + _t(CX + 20, CY + 2, 'O')
    return _svg('Two equal chords and their equal central angles', b, '180 40 280 285')


def fig_chord_perp(labels=True):
    O = (CX, CY)
    Ap, Bp = _P(215), _P(325)
    M = ((Ap[0] + Bp[0]) / 2, Ap[1])
    b = _c(CX, CY, R) + _l(Ap, Bp) + _l(O, M, TEAL) + _l(O, Bp, TEAL) + _right(M, O, Bp, 10)
    b += _tick(Ap, M) + _tick(M, Bp)
    b += _lab(215, 'A') + _lab(325, 'B') + _t(M[0], M[1] + 19, 'M') + _dot(O) + _t(CX - 16, CY - 8, 'O')
    if labels:
        b += _mid_label(O, M, 'd', 12, -1, italic=True) + _mid_label(O, Bp, 'r', 14, 1, italic=True)
    return _svg('The perpendicular from the center cuts the chord in half', b, '180 40 280 285')


def fig_chord_q():
    # guided question: chord AB = 16, distance 6 (the helper line OM is NOT drawn)
    O = (CX, CY)
    Ap, Bp = _P(217), _P(323)
    b = _c(CX, CY, R) + _l(Ap, Bp) + _lab(217, 'A') + _lab(323, 'B') + _dot(O) + _t(CX, CY - 18, 'O')
    b += _t(CX, Ap[1] + 20, '16')
    return _svg('A chord AB of a circle with center O', b)


def _incircle(Ap, Bp, Cp):
    a = math.dist(Bp, Cp); bb = math.dist(Ap, Cp); c = math.dist(Ap, Bp)
    p = a + bb + c
    I = ((a * Ap[0] + bb * Bp[0] + c * Cp[0]) / p, (a * Ap[1] + bb * Bp[1] + c * Cp[1]) / p)
    s = p / 2
    area = abs((Bp[0] - Ap[0]) * (Cp[1] - Ap[1]) - (Cp[0] - Ap[0]) * (Bp[1] - Ap[1])) / 2
    r = area / s

    def foot(P1, P2):
        dx, dy = P2[0] - P1[0], P2[1] - P1[1]
        t = ((I[0] - P1[0]) * dx + (I[1] - P1[1]) * dy) / (dx * dx + dy * dy)
        return (P1[0] + t * dx, P1[1] + t * dy)
    return I, r, foot(Ap, Bp), foot(Bp, Cp), foot(Cp, Ap)


def fig_incircle():
    Ap, Bp, Cp = (262.0, 42.0), (150.0, 300.0), (490.0, 300.0)
    I, r, F_ab, F_bc, F_ca = _incircle(Ap, Bp, Cp)
    b = _poly([Ap, Bp, Cp]) + _c(I[0], I[1], r)
    for f in (F_ab, F_bc, F_ca): b += '<circle cx="%.3f" cy="%.3f" r="3" fill="%s"/>' % (f[0], f[1], TEAL)
    b += _t(Ap[0], Ap[1] - 16, 'A') + _t(Bp[0] - 16, Bp[1] + 8, 'B') + _t(Cp[0] + 16, Cp[1] + 8, 'C')
    b += _mid_label(Ap, F_ab, 'x', 14, 1, color=TEAL, italic=True) + _mid_label(F_ca, Ap, 'x', 14, 1, color=TEAL, italic=True)
    b += _mid_label(F_ab, Bp, 'y', 14, 1, color=TEAL, italic=True) + _mid_label(Bp, F_bc, 'y', 16, -1, color=TEAL, italic=True)
    b += _mid_label(F_bc, Cp, 'z', 16, -1, color=TEAL, italic=True) + _mid_label(Cp, F_ca, 'z', 14, 1, color=TEAL, italic=True)
    return _svg('A circle inside a triangle: equal tangent pieces x, y and z', b, '120 20 400 310')


def fig_incircle_q():
    # guided question: right triangle with legs 8 and 15 and its inscribed circle
    k = 15.0
    C0 = (210.0, 290.0)
    Bp, Ap = (C0[0] + 15 * k, C0[1]), (C0[0], C0[1] - 8 * k)
    b = _poly([Ap, C0, Bp]) + _c(C0[0] + 3 * k, C0[1] - 3 * k, 3 * k) + _right(C0, Ap, Bp, 12)
    b += _t(C0[0] - 18, (C0[1] + Ap[1]) / 2, '8') + _t((C0[0] + Bp[0]) / 2, C0[1] + 20, '15')
    return _svg('A circle inscribed in a right triangle with legs 8 and 15', b)


def fig_two_distances():
    # externally tangent (left) and internally tangent (right) circles, with the distance between the centers
    b = ''
    O1, O2 = (130.0, 190.0), (130.0 + 70 + 45, 190.0)
    b += _c(O1[0], O1[1], 70) + _c(O2[0], O2[1], 45) + _l(O1, O2, TEAL) + _dot(O1) + _dot(O2)
    b += _t((O1[0] + O2[0]) / 2, 292, 'd = R + r', size=20, color=TEAL)
    b += _t(O1[0] - 40, O1[1] + 30, 'R', italic=True) + _t(O2[0] + 22, O2[1] + 26, 'r', italic=True)
    Q1 = (470.0, 190.0); Q2 = (Q1[0] + 90 - 45, 190.0)
    b += _c(Q1[0], Q1[1], 90) + _c(Q2[0], Q2[1], 45) + _l(Q1, Q2, TEAL) + _dot(Q1) + _dot(Q2)
    b += _t(Q1[0], 300, 'd = R − r', size=20, color=TEAL)
    b += _t(Q1[0] - 50, Q1[1] + 44, 'R', italic=True) + _t(Q2[0] + 8, Q2[1] + 30, 'r', italic=True)
    b += _t(160, 40, 'outside each other', size=18) + _t(470, 40, 'one inside the other', size=18)
    return _svg('Tangent circles: the distance between the centers', b, '40 20 580 300')


def fig_segment():
    O = (CX, CY)
    Ap, Bp = _P(135), _P(45)
    b = _sector(45, 135, fill='none') + _segment(45, 135) + _c(CX, CY, R) + _l(O, Ap) + _l(O, Bp) + _l(Ap, Bp)
    b += _lab(135, 'A') + _lab(45, 'B') + _dot(O) + _t(CX, CY + 20, 'O') + _right(O, Ap, Bp, 12)
    b += _mid_label(O, Ap, '6', 14, 1) + _mid_label(O, Bp, '6', 14, -1)
    return _svg('A segment: the region between a chord and its arc', b, '180 40 280 285')


def fig_lens():
    r = 90.0
    O, Pp = (275.0, 180.0), (365.0, 180.0)
    h = r * math.sqrt(3) / 2
    Ai, Bi = (320.0, 180 - h), (320.0, 180 + h)
    lens = ('<path d="M %.3f %.3f A %.1f %.1f 0 0 1 %.3f %.3f A %.1f %.1f 0 0 1 %.3f %.3f Z" fill="%s" stroke="%s" '
            'stroke-width="2.2"/>' % (Ai + (r, r) + Bi + (r, r) + Ai + (FILL, TEAL)))
    b = lens + _c(O[0], O[1], r) + _c(Pp[0], Pp[1], r)
    b += _poly([O, Ai, Pp, Bi], stroke=TEAL, w=1.8) + _l(O, Pp, TEAL, 1.8)
    b += _dot(O) + _dot(Pp) + _t(O[0] - 18, O[1], 'O') + _t(Pp[0] + 18, Pp[1], 'P')
    b += _t(Ai[0], Ai[1] - 16, 'A') + _t(Bi[0], Bi[1] + 18, 'B')
    b += _angle(O, Ai, Bi, 22) + _t(O[0] + 42, O[1] - 13, '120°', size=16, color=TEAL)
    return _svg('Two equal circles, each through the center of the other', b, '160 45 320 270')


def fig_common_tangent(R1=80.0, r1=20.0, with_help=True, labels=('8', '2'), x0=250.0, y0=300.0):
    """circles tangent to each other and to a horizontal line. with_help=False: the question figure (no radii,
    no line between the centers - those are the helper lines of the solution)."""
    dx = 2 * math.sqrt(R1 * r1)
    A0, B0 = (x0, y0 - R1), (x0 + dx, y0 - r1)
    Dp, Cp = (A0[0], y0), (B0[0], y0)
    b = _c(A0[0], A0[1], R1) + _c(B0[0], B0[1], r1) + _l((x0 - R1 - 20, y0), (B0[0] + r1 + 70, y0))
    b += _dot(A0) + _dot(B0) + _dot(Dp) + _dot(Cp)
    b += _t(A0[0] - 16, A0[1] - 8, 'A') + _t(B0[0] + r1 * 0.8 + 10, B0[1] - r1 * 0.8 - 10, 'B')
    b += _t(Dp[0], y0 + 18, 'D') + _t(Cp[0], y0 + 18, 'C')
    if with_help:
        E = (A0[0], B0[1])
        b += _l(A0, Dp, TEAL) + _l(B0, Cp, TEAL) + _l(A0, B0, TEAL)
        b += _right(Dp, A0, Cp, 10) + _right(Cp, B0, Dp, 8)
        b += _mid_label(A0, Dp, labels[0], 12, 1) + _t(B0[0] + r1 + 14, B0[1] + r1 / 2, labels[1])
        b += _l(B0, E, INK, 1.8, dash=True) + _right(E, A0, B0, 8)
        b += _t(E[0] - 14, E[1], 'E', size=18)
    return _svg('Two tangent circles and a common tangent line', b, '140 60 310 280')


def fig_common_tangent_q():
    return _crop(fig_common_tangent(128.0, 32.0, False, x0=250.0, y0=320.0), '0 0 640 360').replace(
        'Two tangent circles and a common tangent line', 'Two tangent circles and a common tangent DC')


def fig_ring_chord():
    O = (CX, CY)
    r1 = 60.0
    Tp = (CX, CY + r1)
    hx = math.sqrt(R * R - r1 * r1)
    Ap, Bp = (CX - hx, Tp[1]), (CX + hx, Tp[1])
    b = _c(CX, CY, R, fill=FILL, stroke=TEAL) + _c(CX, CY, r1, fill='white') + _l(Ap, Bp)
    b += _l(O, Tp, TEAL) + _l(O, Bp, TEAL) + _right(Tp, O, Bp, 9) + _dot(O)
    b += _t(CX - 16, CY - 8, 'O') + _t(Ap[0] - 14, Ap[1] + 10, 'A') + _t(Bp[0] + 14, Bp[1] + 10, 'B')
    b += _mid_label(O, Tp, 'r', 12, -1, italic=True)
    b += _t(O[0] + 0.62 * (Bp[0] - O[0]) + 8, O[1] + 0.62 * (Bp[1] - O[1]) - 14, 'R', italic=True)
    b += _mid_label(Tp, Bp, 'h', 14, 1, italic=True)
    return _svg('A chord of the large circle that touches the small circle', b, '180 40 280 285')


def fig_segment_q():
    O = (CX, CY)
    Ap, Bp = _P(120), _P(60)
    b = _segment(60, 120) + _c(CX, CY, R) + _l(Ap, Bp) + _l(O, Ap) + _l(O, Bp)
    b += _lab(120, 'A') + _lab(60, 'B') + _dot(O) + _t(CX, CY + 20, 'O') + _angle(O, Bp, Ap, 26, '60°', 44)
    return _svg('The region between chord AB and arc AB is shaded', b)


def fig_internal():
    Ac, Bc = (300.0, 180.0), (361.0, 180.0)
    b = _c(Ac[0], Ac[1], 110) + _c(Bc[0], Bc[1], 49) + _dot(Ac) + _dot(Bc)
    b += _t(Ac[0] - 4, Ac[1] - 18, 'A') + _t(Bc[0] + 4, Bc[1] - 18, 'B')
    return _svg('A small circle inside a large circle, touching it at one point', b)


def fig_incircle_bd():
    k = 26.0
    Bp, Cp = (164.0, 300.0), (164.0 + 12 * k, 300.0)
    Ap = (164.0 + 7.5 * k, 300.0 - math.sqrt(100 - 56.25) * k)
    I, r, F_ab, F_bc, F_ca = _incircle(Ap, Bp, Cp)
    b = _poly([Ap, Bp, Cp]) + _c(I[0], I[1], r) + _dot(F_ab)
    b += _t(Ap[0], Ap[1] - 16, 'A') + _t(Bp[0] - 16, Bp[1] + 8, 'B') + _t(Cp[0] + 16, Cp[1] + 8, 'C')
    b += _t(F_ab[0] - 16, F_ab[1] - 8, 'D')
    return _svg('A circle inscribed in triangle ABC touches AB at D', b)


def fig_ring_q():
    r1 = 60.0
    y = CY + r1
    hx = math.sqrt(R * R - r1 * r1)
    b = _c(CX, CY, R, fill=FILL, stroke=TEAL) + _c(CX, CY, r1, fill='white') + _l((CX - hx, y), (CX + hx, y)) + _dot((CX, CY))
    b += _t(CX, y + 18, '16')
    return _svg('Two circles with the same center and a chord of the large circle that touches the small circle', b)


# ================================================================================================
# helpers for videos
# ================================================================================================
def _set_fig(M, qid, svg, vb=None):
    """set a question figure and every copy of it on the solution slides (keep their crop unless vb is given)."""
    M.set_q(qid, figure=svg)
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            for it in b['items']:
                if it.get('k') == 'q' and it.get('qid') == qid and it.get('fig'):
                    old = re.search(r'viewBox="([^"]*)"', it['fig']['svg']).group(1)
                    it['fig'] = {'type': 'geometry', 'svg': _crop(svg, vb or old)}
                    M.touched_videos.add(v['id'])


def _set_vis(M, vid, n, svg, keep_crop=True):
    b = M.slide(vid, n)
    its = [it for it in b['items'] if it.get('k') == 'vis']
    assert len(its) == 1, (vid, n)
    if keep_crop:
        svg = _crop(svg, re.search(r'viewBox="([^"]*)"', its[0]['v']['svg']).group(1))
    its[0]['v'] = {'type': 'geometry', 'svg': svg}
    M.touched_videos.add(vid)


def _script_of(M, vid, n):
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _say(M, vid, n, old, new):
    """replace (part of) a spoken line; new=None deletes the line."""
    def fn(lines):
        out, hit = [], False
        for l in lines:
            if 'say' in l and old in l['say']:
                hit = True
                if new is None: continue
                l = dict(l, say=l['say'].replace(old, new))
            out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def _draw(M, vid, n, old, new):
    def fn(lines):
        out, hit = [], False
        for l in lines:
            if 'draw' in l and old in l['draw']:
                hit = True
                if new is None: continue
                l = dict(l, draw=l['draw'].replace(old, new))
            out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def _item(M, vid, n, old, new, label=None):
    """replace a board item's text (exact) and, optionally, its 'appears' label."""
    b = M.slide(vid, n); hit = None
    for k, it in enumerate(b['items']):
        if it.get('t') == old: it['t'] = new; hit = k
    assert hit is not None, (vid, n, old)
    if label:
        for l in b['lines']:
            if l.get('appear') == hit: l['label'] = label
    M.touched_videos.add(vid)


US = [('CENTRE', 'CENTER'), ('centres', 'centers'), ('centre', 'center'), ('Centre', 'Center'), ('centimetres', 'centimeters'),
      ('metres', 'meters'), ('practised', 'practiced'), ('practise', 'practice'), ('Recognise', 'Recognize'),
      ('recognise', 'recognize'), ('colour', 'color')]


def _american(M):
    def fix(s):
        for a, c in US: s = s.replace(a, c)
        return s
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        hit = False
        for k in ('title', 'navLabel'):
            if v.get(k) and fix(v[k]) != v[k]: v[k] = fix(v[k]); hit = True
        for b in v['beats']:
            for k in ('title', 'bigTitle'):
                if b.get(k) and fix(b[k]) != b[k]: b[k] = fix(b[k]); hit = True
            for l in b['lines']:
                for k in ('say', 'draw', 'label'):
                    if k in l and fix(l[k]) != l[k]: l[k] = fix(l[k]); hit = True
            for it in b['items']:
                if it.get('t') and fix(it['t']) != it['t']: it['t'] = fix(it['t']); hit = True
        if hit: M.touched_videos.add(v['id'])


def _sync_canvas(M):
    """the 'Pre-loaded — question ...' descriptions keep an old copy of each stem: refresh them."""
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            c = b.get('canvas') or ''
            m = re.match(r'Pre-loaded — question (\S+) with its four answer choices', c)
            if m and m.group(1) in M.D['questions']:
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (
                    m.group(1), M.q(m.group(1))['stem'])
                M.touched_videos.add(v['id'])


def _qfig(qid, svg, vb):
    return Q(qid, fig={'type': 'geometry', 'svg': _crop(svg, vb)}, figw=0.56, figalign='left')


def _bt(t, k, size=38):
    """board item next to a question with a figure (right column)."""
    return T(t, size=size, x=1060, y=250 + 80 * k, w=470)


def _bw(t, k, size=46):
    """board item under a question without a figure (full width)."""
    return T(t, size=size, x=410, y=300 + 80 * k, w=1100)


def _solution(M, qid, group, sb_title, intro, slides, num, after=None):
    """guided-question solution video in the style of the existing solve-geo33-* videos."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script, pre in slides:
        beats.append(dict(mode='question', active=0, title=title, pre=pre, script=script))
    v = M.new_video('solve-' + qid, TOPIC, group, ['Question %d' % n], beats, M.section_of(qid),
                    kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = sb_title
    v['hybrid']['num'] = num
    v['hybrid']['title'] = sb_title
    v['title'] = v['navLabel'] = group
    return n


# ================================================================================================
def apply(M):
    _figures(M)
    _questions(M)
    _lesson_videos(M)
    _solution_videos(M)
    _new_guided_learn1(M)
    _tools_block(M)
    _cards(M)
    _practice(M)
    _summaries(M)
    _american(M)
    _sync_canvas(M)
    cut_repeats(M)          # 2026-10-05: last
    renumber_pass(M)        # 2026-10-06 renumber pass: runs last


# ------------------------------------------------------------------------------------------------
# 1. Figures of existing questions and lesson slides
# ------------------------------------------------------------------------------------------------
def _figures(M):
    F = lambda q: M.q(q)['questionVisual']['svg']
    _set_fig(M, 'geo33-g085', fig_g085(F('geo33-g085')), '159.5 42.7 321.0 294.0')
    _set_fig(M, 'geo33-g083', fig_g083(F('geo33-g083')))
    _set_fig(M, 'geo33-g091', fig_g091(F('geo33-g091')))
    _set_fig(M, 'geo33-g095', fig_g095(F('geo33-g095')))
    _set_fig(M, 'geo33-g098', fig_g098())
    _set_fig(M, 'geo33-g101', fig_g101(F('geo33-g101')))
    _set_fig(M, 'geo33-foundation-p03', fig_p03(F('geo33-foundation-p03')))
    _set_fig(M, 'geo33-foundation-p05', fig_p05(F('geo33-foundation-p05')))
    _set_fig(M, 'geo33-foundation-p11', fig_p11())
    _set_fig(M, 'geo33-foundation-p15', fig_p15(F('geo33-foundation-p15')))
    _set_fig(M, 'geo33-foundation-p19', fig_p19(F('geo33-foundation-p19')))
    _set_fig(M, 'geo33-foundation-p20', fig_p20(F('geo33-foundation-p20')))
    _set_fig(M, 'geo33-advanced-p04', fig_adv_p04(F('geo33-advanced-p04')))
    _set_fig(M, 'geo33-advanced-p06', _q_to_mark(F('geo33-advanced-p06'), 'γ'))
    _set_fig(M, 'geo33-advanced-p11', fig_adv_p11(F('geo33-advanced-p11')))
    _set_fig(M, 'geo33-advanced-p15', fig_adv_p15())
    _set_fig(M, 'geo33-advanced-p26', fig_adv_p26())
    # lesson figures
    _set_vis(M, 'geo-074', 2, _drop(M.slide('geo-074', 2)['items'][0]['v']['svg'], '>A</text>'))   # stray "A"
    _set_vis(M, 'geo-075', 5, fig_quad('A quadrilateral inscribed in a circle', False))
    _set_vis(M, 'geo-075', 6, fig_quad('A quadrilateral inscribed in a circle with center O', True))
    _set_vis(M, 'geo-081', 5, fig_quarters())
    _set_vis(M, 'geo-097-after', 4, fig_nested_tri(M.slide('geo-097-after', 4)['items'][0]['v']['svg']))


# ------------------------------------------------------------------------------------------------
# 2. Existing questions: TeX in every solution, numbers shown, no ":" for division, stacked givens
# ------------------------------------------------------------------------------------------------
def _questions(M):
    S = M.set_q
    for qid, q in M.D['questions'].items():            # stray spaces around stems
        if q['topic'] == TOPIC and q['stemRich'] != q['stemRich'].strip():
            S(qid, stem=q['stemRich'].strip())

    # ---------------- guided: Learn and try ----------------
    S('geo33-g076', expl=[
        'B is on the minor arc AC. Stand at B between BA and BC: you see the major arc AC. Angle ABC rests on it.',
        'The central angle on the major arc: $360°-112°=248°$.',
        'The inscribed angle is half of it: $\\angle ABC=\\frac{248°}{2}=124°$.',
        'Check: a point D on the major arc makes ABCD an inscribed quadrilateral. $\\angle ADC=\\frac{112°}{2}=56°$, '
        'and $\\angle ABC=180°-56°=124°$. ($180°-112°=68°$ is the trap: AOCB is not an inscribed quadrilateral.)'])
    S('geo33-g078', expl=[
        'Draw the radii OD and OE. A radius to a point of tangency is perpendicular to the tangent: '
        '$\\angle ODP=\\angle OEP=90°$.',
        'The angles of quadrilateral ODPE add up to $360°$: $\\angle DOE=360°-90°-90°-52°=128°$.',
        'Angle DAE is an inscribed angle on the same minor arc DE: $\\angle DAE=\\frac{128°}{2}=64°$.'])
    S('geo33-g080', expl=[
        'Area $=3\\times$ circumference: $\\pi r^2=3\\cdot2\\pi r$.',
        'Divide by $\\pi$: $r^2=6r$. Divide by $r$ (a radius is not 0): $r=6$.',
        'Check: $S=\\pi\\cdot6^2=36\\pi$ and $C=2\\pi\\cdot6=12\\pi$, and $36\\pi=3\\cdot12\\pi$.'])
    S('geo33-g082', expl=[
        'The whole circumference: $2\\pi\\cdot6=12\\pi$.',
        'The arc is $\\frac{3\\pi}{12\\pi}=\\frac14$ of the circle.',
        'So its central angle is $\\frac14$ of $360°$: $\\alpha=90°$.'])
    S('geo33-g083', expl=[
        '$60°$ is $\\frac16$ of the circle and $90°$ is $\\frac14$: $\\frac16+\\frac14=\\frac2{12}+\\frac3{12}=\\frac5{12}$.',
        'The area of the circle: $\\pi\\cdot6^2=36\\pi$.',
        'Shaded: $\\frac5{12}\\cdot36\\pi=15\\pi$. (Or separately: $6\\pi+9\\pi=15\\pi$.)'])
    S('geo33-g085', expl=[
        'AB is a straight line: $\\angle BOC=180°-120°=60°$.',
        '$OB=OC$ (radii), so the base angles are equal: $\\frac{180°-60°}{2}=60°$ each. Triangle OBC is equilateral.',
        'Its side is a radius: $\\frac{12}{2}=6$.',
        'Area of an equilateral triangle: $\\frac{6^2\\sqrt3}{4}=\\frac{36\\sqrt3}{4}=9\\sqrt3$.'])
    S('geo33-g086', expl=[
        'The central angle on arc BC: $\\angle BOC=2\\cdot40°=80°$.',
        'Triangle BOC is isosceles ($OB=OC$): $\\angle OBC=\\frac{180°-80°}{2}=50°$.',
        'Triangle ABC is isosceles ($AB=AC$): $\\angle ABC=\\frac{180°-40°}{2}=70°$.',
        '$\\angle ABO=70°-50°=20°$.',
        'Faster: the radius OA splits angle A in half, $\\frac{40°}{2}=20°$. Triangle AOB is isosceles ($OA=OB$), '
        'so $\\angle ABO=\\angle BAO=20°$.'])
    S('geo33-g087',
      stem='AE is a diameter of a circle with center O. B, C and D lie on the same semicircle, in that order. Given:\n'
           '$\\begin{cases} AB=BC=CD=DE \\\\ AO=3\\text{ cm} \\end{cases}$\n'
           'Which of the following statements is not true?',
      expl=['Angles DAE and CAD are inscribed angles on the equal chords DE and CD, so they are equal. Statement 1 is true.',
            'The four equal chords cut off four equal central angles. Together they make the straight angle AOE: '
            '$4x=180°$, so $x=45°$. Statement 2 is true.',
            'Angle ADE is an inscribed angle on the diameter AE: $90°$. Statement 3 is true.',
            'Triangle AOC: $AO=OC=3$ and $\\angle AOC=45°+45°=90°$. A 45°-45°-90° triangle: $AC=3\\sqrt2\\neq3\\sqrt3$. '
            'Statement 4 is not true.'])
    S('geo33-g088', expl=[
        'Radius to the point of tangency: $OA\\perp MA$ and $OB\\perp MB$.',
        'The circles are tangent, so the distance between the centers is the sum of the radii: $OM=4+4=8$.',
        'Right triangle OAM: the leg $OA=4$ is half of the hypotenuse $OM=8$. It is a 30°-60°-90° triangle: '
        '$\\angle AMO=30°$ and $\\angle AOM=60°$.',
        'By symmetry, $\\angle BOM=60°$ too: $\\angle AOB=60°+60°=120°$.'])
    S('geo33-g089', expl=[
        'Small circle: $2\\pi r=8\\pi$, so $r=4$. Its area: $\\pi\\cdot4^2=16\\pi$.',
        'Large circle: $16\\pi+65\\pi=81\\pi$, so $R^2=81$ and $R=9$.',
        'Circumference: $2\\pi\\cdot9=18\\pi\\approx18\\cdot3.14=56.52$ — between 56 and 57.'])
    S('geo33-g090', expl=[
        '$7^2+24^2=49+576=625=25^2$, so the triangle is a right triangle. The right angle is opposite the side 25.',
        'An inscribed right angle rests on a diameter. So the hypotenuse is a diameter of the circle: $d=25$.',
        '$C=\\pi d=25\\pi$.'])
    S('geo33-g091',
      stem='A circle has radius $\\sqrt{30}$ cm. Its central angles are $\\alpha$ and $\\beta$ in turn, six of each, as in '
           'the figure. One sector with angle $\\alpha$ and one sector with angle $\\beta$ are shaded. What is their total '
           'area (in cm²)?',
      expl=['The twelve angles make a full turn: $6\\alpha+6\\beta=360°$, so $\\alpha+\\beta=60°$.',
            'The two shaded sectors are $\\frac{60°}{360°}=\\frac16$ of the circle.',
            'The area of the circle: $\\pi(\\sqrt{30})^2=30\\pi$. Shaded: $\\frac16\\cdot30\\pi=5\\pi$.'])
    S('geo33-g092', expl=[
        'For tangent circles, the distance between the centers is the sum of the radii: '
        '$AB=2+4=6$, $AC=2+6=8$ and $BC=4+6=10$.',
        '$6^2+8^2=100=10^2$, so the angle at A is $90°$.',
        'The arc inside that angle is $\\frac14$ of circle A. The highlighted arc is the other $\\frac34$.',
        'Circumference of circle A: $2\\pi\\cdot2=4\\pi$. Highlighted arc: $\\frac34\\cdot4\\pi=3\\pi$.'])

    # ---------------- guided: Further guided examples ----------------
    S('geo33-g094', expl=[
        'Draw the radius OC to the point of tangency: $OC\\perp AB$ and $OC=4$.',
        'Triangle AOB is right and isosceles, so its height OC is also a median. Triangles AOC and BOC are 45°-45°-90° '
        'triangles: $AC=CB=OC=4$, and $AB=8$.',
        'Triangle: $\\frac{8\\cdot4}{2}=16$. Sector ($90°$ is a quarter): $\\frac14\\cdot\\pi\\cdot4^2=4\\pi$.',
        'Shaded: $16-4\\pi$.'])
    S('geo33-g095', expl=[
        'OE is a radius: $OD=OE=12$, and $OC=12+12=24$.',
        'Draw the radius OD to the point of tangency: $OD\\perp AC$, so triangle ODC is a right triangle.',
        'The hypotenuse OC is twice the leg OD: a 30°-60°-90° triangle. $\\angle DOC=60°$ and $DC=12\\sqrt3$.',
        'Triangle ODC: $\\frac{12\\cdot12\\sqrt3}{2}=72\\sqrt3$. Sector DOE ($60°$ is a sixth): $\\frac16\\cdot\\pi\\cdot12^2=24\\pi$.',
        'Shaded: $72\\sqrt3-24\\pi$.'])
    S('geo33-g096', expl=[
        '$OA=OB=r$, so the base angles of triangle AOB are equal: both are $60°$. The triangle is equilateral, and its '
        'perimeter is $3r$.',
        'The perimeter of the semicircle is half the circumference plus the diameter: $\\pi r+2r=(\\pi+2)r$.',
        'Ratio: $\\frac{(\\pi+2)r}{3r}=\\frac{\\pi+2}{3}$.',
        'Check with $r=2$: $\\frac{2\\pi+4}{6}=\\frac{\\pi+2}{3}$. A ratio of two perimeters cannot contain r.'])
    S('geo33-g097', expl=[
        'Let the radius be r. The side of ABCD is a diameter, $2r$, so its area is $(2r)^2=4r^2$.',
        'The diagonal of EFGH is a diameter, $2r$. Area of a square from its diagonal: $\\frac{(2r)^2}{2}=2r^2$.',
        '$\\frac{2r^2}{4r^2}=\\frac12$.'])
    S('geo33-g098',
      stem='A circle with center O has radius 9 cm. A, G, F, E and D lie on the same arc, in that order. B and C lie on '
           'the arc AD that does not contain F. Given:\n'
           '$\\begin{cases} \\angle ABF=26° \\\\ \\angle FCD=49° \\\\ \\angle GOE=90° \\end{cases}$\n'
           'What is the sum of the lengths of the highlighted arcs AG and ED (in cm)?',
      expl=['Angle ABF is an inscribed angle on arc AF. The central angle is twice as big: $\\angle AOF=2\\cdot26°=52°$.',
            'Angle FCD is an inscribed angle on arc FD: $\\angle FOD=2\\cdot49°=98°$.',
            '$\\angle AOD=52°+98°=150°$. Take away the middle part: $\\angle AOG+\\angle EOD=150°-90°=60°$.',
            'The two arcs together are $\\frac{60°}{360°}=\\frac16$ of the circumference $2\\pi\\cdot9=18\\pi$: '
            '$\\frac16\\cdot18\\pi=3\\pi$.'])
    S('geo33-g099', expl=[
        'A minor arc that is a quarter of the circle has a central angle of $90°$: $\\angle AOB=\\angle APB=90°$.',
        '$OA=AP=PB=BO=4$, and the angles are $90°$: OAPB is a square with area $4^2=16$.',
        'Outside the square, each disk leaves a sector of $360°-90°=270°$, which is $\\frac34$ of the disk: '
        '$\\frac34\\cdot\\pi\\cdot4^2=12\\pi$.',
        'Union: $12\\pi+16+12\\pi=24\\pi+16$.'])
    S('geo33-g100', expl=[
        'The tangents AD and BC are parallel, so the distance between them is a diameter: $AB=2\\cdot3=6$.',
        'The area of the circle: $\\pi\\cdot3^2=9\\pi$.',
        '$6\\cdot BC=9\\pi$, so $BC=\\frac{9\\pi}{6}=\\frac{3\\pi}{2}$.',
        'Size check: the circle is smaller than the square around it ($6\\cdot6=36$). So $6\\cdot BC<36$ and $BC<6$. '
        'Only $\\frac{3\\pi}{2}\\approx4.7$ fits.'])
    S('geo33-g101', expl=[
        'Let the small radius be r. Then $AC=2r$, and the large diameter is $AB=2r+6$. So $R=\\frac{2r+6}{2}=r+3$.',
        'Shaded: $\\pi(r+3)^2-\\pi r^2=21\\pi$.',
        'Divide by $\\pi$ and expand: $r^2+6r+9-r^2=21$, so $6r+9=21$ and $r=2$.',
        'Check: $R=5$, and $25\\pi-4\\pi=21\\pi$.'])
    S('geo33-g102',
      stem='ABC is an isosceles triangle. Given:\n'
           '$\\begin{cases} AB=AC \\\\ \\angle BAC=2\\alpha\\text{ degrees, where }0<\\alpha<90 \\end{cases}$\n'
           'B lies on a circle with center O and radius r. AB and BC meet the circle again at D and E, respectively. What is the '
           'length of the arc DE that does not contain B?',
      expl=['The base angles are equal: $\\angle ABC=\\frac{180°-2\\alpha}{2}=90°-\\alpha$.',
            'Angle DBE is the same angle, and it is an inscribed angle on arc DE. The central angle is twice as big: '
            '$180°-2\\alpha$.',
            'Arc: $\\frac{180-2\\alpha}{360}\\cdot2\\pi r=\\frac{180-2\\alpha}{180}\\cdot\\pi r=\\pi r\\left(1-\\frac{\\alpha}{90}\\right)$.',
            'Check with $\\alpha=30$ and $r=1$: the central angle is $120°$, and the arc is $\\frac13\\cdot2\\pi=\\frac{2\\pi}{3}$. '
            'Only $\\pi\\left(1-\\frac{30}{90}\\right)=\\frac{2\\pi}{3}$ fits.'])

    # ---------------- Foundation practice ----------------
    S('geo33-foundation-p01', expl=['The wire becomes the whole circumference: $2\\pi r=10$.',
                                    '$r=\\frac{10}{2\\pi}=\\frac5\\pi$.'])
    S('geo33-foundation-p02', expl=['The large radius is 6, and the small radius is $\\frac62=3$.',
                                    'Areas: $\\pi\\cdot6^2=36\\pi$ and $\\pi\\cdot3^2=9\\pi$.',
                                    '$36\\pi-9\\pi=27\\pi$.'])
    S('geo33-foundation-p03', expl=['$OC=OD$ (radii), so $\\angle ODC=\\frac{180°-140°}{2}=20°$.',
                                    '$AB\\parallel CD$, and AD crosses both. Alternate angles are equal: $\\angle BAD=\\angle ADC=20°$.'])
    S('geo33-foundation-p04', expl=['Equal inscribed angles rest on equal arcs: arc BC $=$ arc CD.',
                                    'Equal arcs have equal chords: $BC=CD$.',
                                    'The other statements depend on where C and D are, so they are not necessarily true.'])
    S('geo33-foundation-p05', expl=['$\\pi r^2=16\\pi$, so $r=4$ and the diameter is 8.',
                                    'No chord is longer than the diameter. A chord of length 8 is a diameter: AC is a diameter.',
                                    'An inscribed angle on a diameter is $90°$: $\\angle ABC=90°$.'])
    S('geo33-foundation-p06', expl=['COB and BOD make the straight angle COD: $5\\alpha+\\alpha=180°$, so $\\alpha=30°$.',
                                    'BOD and DOA make the straight angle BOA: $30°+\\beta=180°$, so $\\beta=150°$.'])
    S('geo33-foundation-p07', expl=['The minor arc BC has the central angle $2\\cdot36°=72°$. That is $\\frac{72}{360}=\\frac15$ of the circle.',
                                    'The major arc BC is the rest: $1-\\frac15=\\frac45$.'])
    S('geo33-foundation-p08', expl=['Angle BAD rests on arc BCD. The central angle is twice as big: $\\angle BOD=2\\cdot2\\alpha=4\\alpha$.',
                                    '$\\angle BOD=\\angle BOC+\\angle COD$, so $\\angle BOC=4\\alpha-3\\beta$.'])
    S('geo33-foundation-p10', expl=['Small circle: $\\pi d=6\\pi$, so its diameter OB is 6.',
                                    'OB is a radius of the large circle: $R=6$.',
                                    'Large circumference: $2\\pi\\cdot6=12\\pi$.'])
    S('geo33-foundation-p11', expl=['Triangle BOC is isosceles ($OB=OC$): $\\angle OBC=\\frac{180°-144°}{2}=18°$.',
                                    'The radius OB is perpendicular to the tangent BA: $\\angle OBA=90°$.',
                                    '$\\angle ABC=90°-18°=72°$.'])
    S('geo33-foundation-p12', expl=['Each disk: $\\frac{50\\pi}{2}=25\\pi$, so $r^2=25$ and $r=5$.',
                                    'For tangent circles, the distance between the centers is the sum of the radii: $AB=5+5=10$.'])
    S('geo33-foundation-p14', expl=['On the same arc, the central angle is twice the inscribed angle: $\\alpha=2\\beta$.',
                                    '$3\\beta-\\alpha=3\\beta-2\\beta=\\beta$.'])
    S('geo33-foundation-p15', expl=[
        'Write the angles at A and C as $2\\alpha$ and $2\\beta$. Opposite angles of an inscribed quadrilateral: '
        '$2\\alpha+2\\beta=180°$, so $\\alpha+\\beta=90°$.',
        'In triangle ABC: $\\angle B=180°-\\alpha-\\beta=90°$. An inscribed right angle rests on a diameter: AC is a diameter.',
        '$\\pi r^2=25\\pi$, so $r=5$ and $AC=2\\cdot5=10$.'])
    S('geo33-foundation-p16',
      choices=['A kite whose two unequal opposite angles are 90° and 72°',
               'An isosceles trapezoid with upper base angles of 104°',
               'A rectangle with sides 3 cm and 40 cm', 'A regular polygon with 11 sides'],
      expl=['A quadrilateral can be inscribed in a circle only if its opposite angles add up to $180°$.',
            'The kite: $90°+72°=162°\\neq180°$. It cannot be inscribed.',
            'The trapezoid ($104°+76°=180°$), the rectangle and a regular polygon can all be inscribed.'])
    S('geo33-foundation-p17', expl=['OT is a radius to the point of tangency: $OT\\perp AB$. So OT is the height of triangle AOB: 5.',
                                    '$\\frac{AB\\cdot5}{2}=35$, so $AB=14$.'])
    S('geo33-foundation-p18', expl=['Side of the square: $\\frac{28}{4}=7$. AD and BC are sides, so each diameter is 7.',
                                    'Each circumference: $\\pi\\cdot7=7\\pi$. Sum: $7\\pi+7\\pi=14\\pi$.'])
    S('geo33-foundation-p19', expl=['The third angle: $360°-135°-90°=135°$. That is $\\frac{135}{360}=\\frac38$ of the circle.',
                                    'Circumference: $2\\pi\\cdot8=16\\pi$. Arc: $\\frac38\\cdot16\\pi=6\\pi$.'])
    S('geo33-foundation-p20', expl=['$\\angle COB=180°-36°=144°$. That is $\\frac{144}{360}=\\frac25$ of the circle.',
                                    'Sector: $\\frac25\\cdot25\\pi=10\\pi$.'])
    S('geo33-foundation-p21', expl=['$72°$ is $\\frac15$ of the circle. Circumference: $2\\pi\\cdot10=20\\pi$, so the arc is $\\frac15\\cdot20\\pi=4\\pi$.',
                                    'Perimeter of the sector: arc $+$ two radii $=4\\pi+20$.'])
    S('geo33-foundation-p22', expl=['The perpendicular from the center to a chord cuts it in half.',
                                    'Right triangle: radius 13 (hypotenuse), distance 5, half chord: $\\sqrt{13^2-5^2}=\\sqrt{144}=12$.',
                                    'The chord: $2\\cdot12=24$.'])
    S('geo33-foundation-p23',
      stem='PT is tangent at T to a circle with center O. Given:\n'
           '$\\begin{cases} OP=17\\text{ cm} \\\\ OT=8\\text{ cm} \\end{cases}$\nWhat is PT (in cm)?',
      expl=['$OT\\perp PT$ (radius to the point of tangency), so triangle OTP is a right triangle with hypotenuse OP.',
            '$PT^2=17^2-8^2=289-64=225$, so $PT=15$.'])
    S('geo33-foundation-p24', expl=['The new radius is $1.2r$. Area: $\\pi(1.2r)^2=1.44\\pi r^2$.',
                                    'The area is multiplied by 1.44: an increase of $44\\%$ (not $20\\%$ — area grows like $r^2$).'])
    S('geo33-foundation-p26', expl=['Opposite angles of an inscribed quadrilateral add up to $180°$: $3x+(2x+20)=180$.',
                                    '$5x=160$, so $x=32$.'])
    S('geo33-foundation-p27', expl=['$OA\\perp PA$ (radius to the point of tangency).',
                                    '$OP^2=5^2+12^2=169$, so $OP=13$.'])

    # ---------------- Advanced practice ----------------
    S('geo33-advanced-p01', expl=['The four equal arcs are $\\frac25$ of the circle, so one arc is $\\frac25\\div4=\\frac1{10}$ of the circle.',
                                  'Its central angle: $\\frac1{10}\\cdot360°=36°$.'])
    S('geo33-advanced-p02', expl=['Five equal arcs on a semicircle: $\\frac{180°}{5}=36°$ each.',
                                  'E is the midpoint of arc AB, so arc AE is $\\frac{36°}{2}=18°$.',
                                  'Angle ADE is an inscribed angle on arc AE: $\\frac{18°}{2}=9°$.'])
    S('geo33-advanced-p03', expl=['OC is a radius (6), and it is also the diagonal of the square OACD.',
                                  'Side of a square from its diagonal: $OA=\\frac{6}{\\sqrt2}=3\\sqrt2$.',
                                  '$OB=6$, so $AB=OB-OA=6-3\\sqrt2$.'])
    S('geo33-advanced-p04', expl=['The smallest disk: $\\pi a^2$.',
                                  'The outer ring: $\\pi(3c)^2-\\pi(2b)^2=9\\pi c^2-4\\pi b^2$.',
                                  'Total: $\\pi(9c^2-4b^2+a^2)$.'])
    S('geo33-advanced-p05', expl=['Angles ABD and ACD rest on the same arc AD, so $\\angle ACD=\\angle ABD=\\alpha$. Also $\\angle ADB=\\alpha$.',
                                  '$\\angle ADC=\\angle ADB+\\angle BDC=\\alpha+24°$.',
                                  'Triangle ACD: $44°+\\alpha+(\\alpha+24°)=180°$, so $2\\alpha=112°$ and $\\alpha=56°$.'])
    S('geo33-advanced-p06', expl=['Angle ACE is an inscribed angle on arc AE, so the arc is $2\\cdot2p=4p$.',
                                  'Arc ED has the central angle EOD: $3q$.',
                                  'Arc AD: $4p+3q$. Angle ABD is an inscribed angle on it: $\\frac{4p+3q}{2}=2p+\\frac{3q}{2}$.'])
    S('geo33-advanced-p07', expl=['A semicircular arc with radius r has length $\\frac{2\\pi r}{2}=\\pi r$.',
                                  'The four radii add up to $4m$ (their average is m). So the four arcs add up to $\\pi\\cdot4m=4\\pi m$.'])
    S('geo33-advanced-p09', expl=['Let f be the fraction of the circle: $f=\\frac{150}{360}$.',
                                  'Sector area $=f\\cdot\\pi r^2$ and arc $=f\\cdot2\\pi r$: $f\\pi r^2=3\\cdot f\\cdot2\\pi r$.',
                                  'Divide by $f\\pi r$: $r=6$. (The angle does not matter.)'])
    S('geo33-advanced-p10', expl=['Square: $6^2=36$. Semicircle with radius 3: $\\frac{\\pi\\cdot3^2}{2}=\\frac{9\\pi}{2}=4.5\\pi$.',
                                  '$36-4.5\\pi\\approx36-14.14=21.86$: between 21 and 22.'])
    S('geo33-advanced-p11', expl=['Angle ECA is an inscribed angle on arc EA, so the arc is $2\\cdot3t=6t$. Arc AB is equal: $6t$.',
                                  'Central angle EOB: $6t+6t=12t$. The vertical angle DOC is also $12t$.',
                                  'Angle DAC is an inscribed angle on arc DC: $\\frac{12t}{2}=6t$.'])
    S('geo33-advanced-p12', expl=['The central angle on arc BC: $\\angle BOC=2\\cdot45°=90°$.',
                                  'Triangle BOC is right and isosceles with legs r: $BC=r\\sqrt2$.'])
    S('geo33-advanced-p13', expl=['Arc CB is twice arc AC, and together they make the semicircle: arc AC $=60°$ and arc CB $=120°$.',
                                  'Inscribed angles: $\\angle ABC=30°$, $\\angle BAC=60°$, and $\\angle ACB=90°$ (on the diameter).',
                                  'A 30°-60°-90° triangle with hypotenuse $AB=10$: $AC=5$ and $BC=5\\sqrt3$.'])
    S('geo33-advanced-p14', expl=['The three sector angles are the angles of the triangle: together $180°$.',
                                  'With the same radius 3, the three sectors make half a disk: $\\frac12\\cdot\\pi\\cdot3^2=\\frac{9\\pi}{2}$.'])
    S('geo33-advanced-p15',
      stem='Four circles have centers A, B, C and D. Each circle is externally tangent to its two neighbors, in the order '
           'A, B, C, D, A. Given:\n'
           '$\\begin{cases} AB=6\\text{ cm} \\\\ BC=10\\text{ cm} \\\\ CD=14\\text{ cm} \\end{cases}$\nWhat is AD (in cm)?',
      expl=['Call the radii a, b, c and d. For tangent circles, the distance between the centers is the sum of the radii.',
            '$AB+CD=(a+b)+(c+d)$ and $BC+AD=(b+c)+(a+d)$: both are the sum of all four radii.',
            '$6+14=10+AD$, so $AD=10$.'])
    S('geo33-advanced-p16', expl=['Each side of triangle ABC is 6, the radius: the triangle is equilateral, and each angle is $60°$.',
                                  'The common region is bounded by three $60°$ arcs. Each is $\\frac16$ of the circumference $2\\pi\\cdot6=12\\pi$: $2\\pi$.',
                                  'Perimeter: $3\\cdot2\\pi=6\\pi$.'])
    S('geo33-advanced-p17', expl=['Diameter: $\\frac{12\\pi}{\\pi}=12$. It is the diagonal of ABCD: area $\\frac{12^2}{2}=72$.',
                                  'The square of the midpoints has half the area: $\\frac{72}{2}=36$.'])
    S('geo33-advanced-p18', expl=['The $45°$ sector is $\\frac18$ of the disk: $\\frac18\\cdot\\pi\\cdot4^2=2\\pi$.',
                                  'Triangle AOB is right and isosceles, with hypotenuse $OA=4$: legs $\\frac4{\\sqrt2}=2\\sqrt2$, '
                                  'area $\\frac{2\\sqrt2\\cdot2\\sqrt2}{2}=4$.',
                                  'Sector outside the triangle: $2\\pi-4$.'])
    S('geo33-advanced-p19', expl=['$AD\\parallel BC$, so the two angles on the leg CD add up to $180°$: $\\angle BCD=180°-60°=120°$.',
                                  'Radii to the points of tangency: $OE\\perp CD$ and $OF\\perp BC$. In quadrilateral OECF: '
                                  '$\\angle EOF=360°-90°-90°-120°=60°$.',
                                  'Sector: $\\frac16\\cdot\\pi\\cdot6^2=6\\pi$.'])
    S('geo33-advanced-p20', expl=['Tangent circles: $AB=9+4=13$. The radii AD and BC are perpendicular to the tangent DC, so ABCD is a right trapezoid.',
                                  'Draw BE parallel to DC (E on AD): $AE=9-4=5$ and $BE=DC$.',
                                  'Right triangle ABE: $DC=\\sqrt{13^2-5^2}=\\sqrt{144}=12$.',
                                  'Perimeter: $13+4+12+9=38$.'])
    S('geo33-advanced-p21', expl=['The chord touches the small circle. The small radius to that point is perpendicular to the chord, so the distance from the center to the chord is 5.',
                                  'This perpendicular cuts the chord in half: $\\sqrt{13^2-5^2}=\\sqrt{144}=12$.',
                                  'The chord: $2\\cdot12=24$.'])
    S('geo33-advanced-p22', expl=['Same units first: $3.6\\pi$ m $=360\\pi$ cm.',
                                  'One turn covers one circumference: $2\\pi\\cdot12=24\\pi$ cm.',
                                  'Turns: $\\frac{360\\pi}{24\\pi}=15$.'])
    S('geo33-advanced-p23', expl=['The centers form an equilateral triangle with side $2+2=4$: area $\\frac{4^2\\sqrt3}{4}=4\\sqrt3$.',
                                  'Inside the triangle, each circle has a $60°$ sector. Three of them make $180°$ — half of a disk with radius 2: '
                                  '$\\frac12\\cdot\\pi\\cdot2^2=2\\pi$.',
                                  'The gap: $4\\sqrt3-2\\pi$.'])
    S('geo33-advanced-p24', expl=['Ring: $\\pi R^2-\\pi r^2=45\\pi$, so $R^2-r^2=45$.',
                                  'Difference of squares: $(R-r)(R+r)=45$. With $R-r=3$: $R+r=15$.',
                                  '$\\begin{cases} R+r=15 \\\\ R-r=3 \\end{cases}$ Subtract: $2r=12$, so $r=6$.'])
    S('geo33-advanced-p25', expl=['Each angle of the rectangle is $90°$, so its diagonal is a diameter of the circle around it.',
                                  'Diagonal: $\\sqrt{10^2+24^2}=\\sqrt{676}=26$, so $r=13$.',
                                  'Area: $\\pi\\cdot13^2=169\\pi$.'])
    S('geo33-advanced-p26', expl=['Hypotenuse: $\\sqrt{6^2+8^2}=10$.',
                                  'Tangent pieces from one vertex are equal. At the right angle both pieces are r, so the pieces on the '
                                  'hypotenuse are $6-r$ and $8-r$: $(6-r)+(8-r)=10$, and $r=2$.',
                                  'Shortcut for a right triangle: $r=\\frac{a+b-c}{2}=\\frac{6+8-10}{2}=2$.'])
    S('geo33-advanced-p27', expl=['Each center lies on the other circle: $OA=OP=PA=4$ and $OB=OP=PB=4$. Two equilateral triangles, so $\\angle AOB=120°$.',
                                  'AB is twice the height of an equilateral triangle: $AB=2\\cdot2\\sqrt3=4\\sqrt3$. The distance from O to AB is $\\frac42=2$. '
                                  'Triangle AOB: $\\frac{4\\sqrt3\\cdot2}{2}=4\\sqrt3$.',
                                  'One segment $=$ sector $-$ triangle: $\\frac13\\cdot16\\pi-4\\sqrt3=\\frac{16\\pi}{3}-4\\sqrt3$.',
                                  'The common region is two segments: $\\frac{32\\pi}{3}-8\\sqrt3$.'])


# ------------------------------------------------------------------------------------------------
# 3. Lesson videos
# ------------------------------------------------------------------------------------------------
def _lesson_videos(M):
    # ---- geo-075 Angles in a Circle ----
    _item(M, 'geo-075', 4, 'On a diameter: $180°:2=90°$', 'On a diameter: $\\frac{180°}{2}=90°$',
          'On a diameter: 180° ÷ 2 = 90°')
    M.edit_lines('geo-075', 4, lambda ls: ls + [
        {'say': "It works backwards too: a right angle with its vertex on the circle always rests on a diameter."},
        {'draw': 'Write "right triangle in a circle → hypotenuse = diameter · rectangle → diagonal = diameter"'},
        {'say': "So a right triangle inside a circle: its hypotenuse is a diameter. A rectangle inside a circle: its diagonal is a diameter."},
    ])
    M.slide('geo-075', 4)['items'].append(
        T('Backwards: right angle on the circle $\\rightarrow$ hypotenuse $=$ diameter', size=36, x=410, y=730))
    M.slide('geo-075', 4)['lines'].insert(len(M.slide('geo-075', 4)['lines']) - 2,
        {'appear': len(M.slide('geo-075', 4)['items']) - 1, 'label': "'Backwards: right angle on the circle → hypotenuse = diameter' appears"})
    _draw(M, 'geo-075', 6, 'Write 2α at O on the side facing A', 'Write 2α at O, on the side of C (angle BOD that rests on arc BCD)')
    _draw(M, 'geo-075', 6, 'Write 2β for the other central angle', 'Write 2β for the other central angle BOD, on the side of A')
    # Equal chords: a figure + the original SSS proof (pass 2: the proof is restored)
    M.set_slide('geo-075', 8, script=[
        "One more fact from the course that we'll use later.",
        A('Two equal chords AB and CD with the radii to their ends appear', VIS(fig_equal_chords(), w=1000, h=520)),
        "In the same circle, equal chords cut off equal arcs — and equal central angles.",
        "Join each chord's ends to the center: two triangles, radius, radius, equal chord — identical triangles. "
        "So the central angles are equal.",
        D('Mark the equal central angles at O'),
        A('Equal chords → equal central angles → equal arcs',
          T('Equal chords $\\rightarrow$ equal central angles $\\rightarrow$ equal arcs', size=40, x=410, y=650)),
        "And it works backwards too: equal arcs — equal chords.",
    ])
    M.insert_slides('geo-075', 8, [dict(mode='concept', active=7, title='Chord and center', script=[
        "One more chord rule — and it's on the exam all the time.",
        A('A chord AB with the perpendicular OM from the center appears', VIS(fig_chord_perp(), w=1000, h=520)),
        "Draw a perpendicular from the center O to a chord. Call its foot M.",
        D('Mark AM and MB with equal ticks'),
        "It cuts the chord exactly in half: AM equals MB.",
        "Why? Triangles OMA and OMB have the same hypotenuse — a radius — and the same leg OM. So, by Pythagoras, the other legs are equal too.",
        A('d² + (half chord)² = r²',
          T('$d^2+\\left(\\frac{\\text{chord}}{2}\\right)^2=r^2$', size=44, x=410, y=650)),
        "Now we have a right triangle: the distance d, half the chord, and the radius r as the hypotenuse.",
        D('Write "r = 13, d = 5 → half chord = 12 → chord = 24"'),
        "Radius 13, distance 5: half the chord is 12 — a 5-12-13 triangle. The whole chord: 24.",
        "The distance from the center to a chord? Always draw the perpendicular.",
        "Now let's solve a sample question.",
    ])])
    M.set_sidebar('geo-075', ['Central = 2×inscribed', 'Same arc, same angle', 'Angle on a diameter', 'Inscribed quad',
                              'Why: 2α + 2β = 360°', 'One rule behind it all', 'Equal chords', 'Chord and center'])

    # ---- geo-077 Tangents: circle inside a triangle, tangent circles ----
    _say(M, 'geo-077', 4, "Let's solve a sample question.", None)
    M.insert_slides('geo-077', 4, [
        dict(mode='concept', active=3, title='Circle inside a triangle', script=[
            "Now a circle inside a triangle. It touches all three sides.",
            A('A triangle with its inscribed circle and the tangent pieces x, y, z appears',
              VIS(fig_incircle(), w=760, h=600, x=330, y=40)),
            "Each vertex sends two tangents to the circle. And two tangents from one point are equal.",
            D('Mark x, x at A · y, y at B · z, z at C'),
            "From A — x and x. From B — y and y. From C — z and z.",
            A('AB = x + y · BC = y + z · CA = z + x',
              T('$\\begin{cases} AB=x+y \\\\ BC=y+z \\\\ CA=z+x \\end{cases}$', size=38, x=1110, y=120, w=420)),
            "Each side is made of two pieces. Add the three sides: two x plus two y plus two z — the perimeter.",
            A('Right triangle: r = (a + b − c)/2',
              T('Right triangle: $r=\\frac{a+b-c}{2}$', size=38, x=1110, y=420, w=420)),
            "A right triangle has a shortcut. At the right angle, the two tangent pieces are r and r — they make a little square with the radii.",
            D('Write "legs 6, 8, hypotenuse 10 → r = (6 + 8 − 10) ÷ 2 = 2"'),
            "Legs 6 and 8, hypotenuse 10. 6 plus 8 minus 10 is 4. Half of it — the radius is 2.",
        ]),
        dict(mode='concept', active=4, title='Tangent circles', script=[
            "Two circles that touch at one point. Join the centers.",
            A('Two pairs of tangent circles appear: outside each other and one inside the other',
              VIS(fig_two_distances(), w=1000, h=500)),
            "Outside each other: the line between the centers is one radius plus the other. R plus r.",
            "One inside the other: the big radius covers the small one. R minus r.",
            A('Touching: outside d = R + r · inside d = R − r',
              T('Touching from outside: $d=R+r$ $\\cdot$ from inside: $d=R-r$', size=40, x=410, y=650)),
            D('Write "R = 9, r = 4: outside 13 · inside 5"'),
            "Radii 9 and 4: from outside, the centers are 13 apart. From inside — 5.",
            "Tangent circles in a question? Join the centers — another automatic helper line.",
            "Let's solve a sample question.",
        ]),
    ])
    M.set_sidebar('geo-077', ['Touches at one point', 'Radius ⊥ tangent', 'Two tangents: a kite', 'Circle inside a triangle',
                              'Tangent circles'])

    # ---- geo-079 Area and Circumference: scaling and wheels ----
    _say(M, 'geo-079', 7, "Let's see a psychometric question.", None)
    M.insert_slides('geo-079', 7, [
        dict(mode='concept', active=6, title='Scale the radius', script=[
            "What happens to the circle when the radius grows?",
            D('Write "r = 3: C = 6π, S = 9π"'),
            D('Write "r = 6: C = 12π, S = 36π"'),
            "Double the radius: 3 becomes 6. The circumference: 6π becomes 12π — times 2. The area: 9π becomes 36π — times 4!",
            A('r × k → C × k, S × k²', T('$r\\times k\\ \\Rightarrow\\ C\\times k,\\ \\ S\\times k^2$', size=54)),
            "Lengths grow like the radius. Areas grow like the radius squared.",
            A('Radius + 20% → × 1.2 → area × 1.44 (+44%)',
              T('Radius $+20\\%$: $\\times1.2\\ \\Rightarrow$ area $\\times1.2^2=1.44$ $\\ (+44\\%)$', size=40)),
            "Radius up 20 percent: times 1.2. The area: 1.2 squared — 1.44. That's 44 percent more, not 20.",
            A('Area × 9 → radius × 3', T('Backwards: area $\\times9\\ \\Rightarrow$ radius $\\times3$', size=40)),
            "It works backwards too: the area is 9 times bigger — the radius is 3 times bigger. So is the circumference.",
        ]),
        dict(mode='concept', active=7, title='Wheels', script=[
            "Wheels. In one full turn, a wheel rolls exactly one circumference.",
            A('Turns = distance ÷ circumference',
              T('Turns $=\\frac{\\text{distance}}{\\text{circumference}}$', size=54)),
            "A wheel with radius 10 cm: one turn is 2π times 10 — 20π centimeters.",
            A('Same units first!', T('Same units first!', size=44)),
            D('Write "10π m = 1,000π cm"'),
            "The road is 10π meters. Change it to centimeters first: 1,000π.",
            D('Write "1,000π ÷ 20π = 50 turns"'),
            "1,000π divided by 20π: 50 turns.",
            "Let's see a psychometric question.",
        ]),
    ])
    M.set_sidebar('geo-079', ['The two formulas', 'What is π?', 'π is a number', 'From the radius', 'Back from C',
                              'Back from the area', 'Scale the radius', 'Wheels'])

    # ---- geo-081 Sectors and Arcs ----
    M.slide('geo-081', 5)['lines'][0]['label'] = 'A circle cut into four quarters, one shaded, appears'
    _item(M, 'geo-081', 6, 'Circle $25\\pi\\ \\rightarrow$ sector $25\\pi:5=5\\pi$',
          'Circle $25\\pi\\ \\rightarrow$ sector $\\frac{25\\pi}{5}=5\\pi$', 'Circle 25π → sector 25π ÷ 5 = 5π')

    # ---- geo-097-after: why the triangle case is 4 times ----
    _say(M, 'geo-097-after', 4, "We didn't prove it — you can sit down and prove it. The key: in an equilateral triangle, "
                                "the center is twice as far from a vertex as from a side.",
         "Why? Look at the inner triangle — it's upside down. Its corners touch the outer sides exactly at their midpoints.")
    M.edit_lines('geo-097-after', 4, lambda ls: ls[:-1] + [
        {'draw': 'Shade the three corner triangles of the outer triangle'},
        {'say': "So the outer triangle is cut into four equal triangles — and the inner one is one of them. Four times the area."},
        ls[-1]])


# ------------------------------------------------------------------------------------------------
# 4. Existing solution videos
# ------------------------------------------------------------------------------------------------
def _solution_videos(M):
    # Q1: fractions, and Method 3 step by step
    _item(M, 'solve-geo33-g076', 3, '$\\angle ADC=112°:2=56°$', '$\\angle ADC=\\frac{112°}{2}=56°$', '∠ADC = 112° ÷ 2 = 56° appears')
    _item(M, 'solve-geo33-g076', 4, '$\\angle ABC=248°:2=124°$', '$\\angle ABC=\\frac{248°}{2}=124°$', '∠ABC = 248° ÷ 2 = 124° appears')
    M.set_slide('solve-geo33-g076', 5, script=[
        "One more route, step by step — just so you've seen it.",
        D('Draw OB'),
        "Draw OB. OA, OB and OC are all radii — so we get two isosceles triangles.",
        A('∠OAB = ∠OBA = x · ∠OBC = ∠OCB = y appears',
          _bt('$\\angle OBA=\\angle OAB=x$, $\\ \\angle OBC=\\angle OCB=y$', 0, 30)),
        "Triangle AOB: its base angles are equal — call them x. Triangle BOC: call them y. Angle ABC is x plus y.",
        A('∠AOB + ∠BOC = 112° appears', _bt('$\\angle AOB+\\angle BOC=112°$', 1, 34)),
        "The two angles at O make up the 112.",
        A('(180° − 2x) + (180° − 2y) = 112° appears', _bt('$(180°-2x)+(180°-2y)=112°$', 2, 34)),
        "Each of them is 180 minus twice its base angle.",
        A('2(x + y) = 248° → x + y = 124° appears', _bt('$2(x+y)=248°\\ \\Rightarrow\\ x+y=124°$', 3, 34)),
        "So twice x plus y is 360 minus 112 — 248. And x plus y — that's angle ABC — is 124.",
        "Again 124. But the two methods before are the ones to remember.",
    ])
    # Q2
    M.set_slide('solve-geo33-g078', 2, title='Automatic: draw the radii')
    # pass 2: the original "Pavlov" line stays (restored)
    _item(M, 'solve-geo33-g078', 3, '$\\angle DAE=128°:2=64°$', '$\\angle DAE=\\frac{128°}{2}=64°$', '∠DAE = 128° ÷ 2 = 64°')
    # Q7
    _item(M, 'solve-geo33-g086', 2, '$\\angle OBC=(180°-80°):2=50°$', '$\\angle OBC=\\frac{180°-80°}{2}=50°$', '(180° − 80°) ÷ 2 = 50° appears')
    _item(M, 'solve-geo33-g086', 3, '$\\angle ABC=(180°-40°):2=70°$', '$\\angle ABC=\\frac{180°-40°}{2}=70°$', '∠ABC = (180° − 40°) ÷ 2 = 70° appears')
    _item(M, 'solve-geo33-g086', 4, '$\\angle BAO=40°:2=20°$', '$\\angle BAO=\\frac{40°}{2}=20°$', '40° ÷ 2 = 20° appears')
    # Q9: remind the golden triangle ratios on first use
    M.edit_lines('solve-geo33-g088', 4, lambda ls: ls[:3] + [
        {'appear': len(M.slide('solve-geo33-g088', 4)['items']), 'label': "'30°-60°-90°: x, x√3, 2x' appears"},
        {'say': "A reminder: in the golden triangle the sides are x, x root 3 and 2x. The short leg is half the hypotenuse."},
    ] + ls[3:])
    M.slide('solve-geo33-g088', 4)['items'].append(_bt('$30°$-$60°$-$90°$: $\\ x,\\ x\\sqrt3,\\ 2x$', 1, 36))
    # Q8: remind the silver triangle (already on the board) - say the ratio
    # Q16 Method 3: "1+" on three arcs was only true for three 60° pieces
    b = M.slide('solve-geo33-g096', 4)
    M.edit_lines('solve-geo33-g096', 4, lambda ls: [
        l for l in ls if l.get('draw') != 'Write 1+ on each of the three arcs'
        and not l.get('say', '').startswith('Same for the other two arcs')])
    _say(M, 'solve-geo33-g096', 4,
         "The arc from A to B is longer than the chord AB — the shortest path between two points is the straight line. So it's 1-plus.",
         "The curved part is half a circle: π times 1 — a bit more than 3. Add the diameter, 2: the semicircle is 5-plus.")
    # Q20 estimate: a clear reason
    _say(M, 'solve-geo33-g100', 3,
         "The diameter is 6. And BC is shorter than the diameter — the rectangle has the circle's area, but it's shorter than the square around the circle.",
         "The circle fits inside a 6 by 6 square, so its area is less than 36. The rectangle has the same area: 6 times BC is less than 36.")
    _item(M, 'solve-geo33-g100', 3, '$BC<6$', '$6\\cdot BC<36\\ \\Rightarrow\\ BC<6$', '6 · BC < 36 → BC < 6 appears')
    # Q21 / Q22: no colon inside the math
    _item(M, 'solve-geo33-g101', 3, '$r=3:\\ R=6,\\ 36\\pi-9\\pi=27\\pi$', '$r=3$: $\\ R=6,\\ 36\\pi-9\\pi=27\\pi$')
    _item(M, 'solve-geo33-g101', 3, '$r=2:\\ R=5,\\ 25\\pi-4\\pi=21\\pi$', '$r=2$: $\\ R=5,\\ 25\\pi-4\\pi=21\\pi$')
    _item(M, 'solve-geo33-g102', 4, '$\\alpha=30,\\ r=1:\\ L=\\frac{120}{360}\\cdot2\\pi=\\frac{2\\pi}{3}$',
          '$\\alpha=30,\\ r=1$: $\\ L=\\frac{120}{360}\\cdot2\\pi=\\frac{2\\pi}{3}$')
    _say(M, 'solve-geo33-g102', 4, "That's it for circles. On to the summary.",
         "Next: a few more tools for the hardest circle questions.")


# ------------------------------------------------------------------------------------------------
# 5. New guided questions in "Learn and try": chord, circle inside a triangle, scaling
# ------------------------------------------------------------------------------------------------
VB_CHORD, VB_INC = '180 45 280 275', '175 150 300 180'


def _new_guided_learn1(M):
    # ---- chord + distance -> radius ----
    g = GID[0]
    M.new_q(g, TOPIC, 'Chord AB of a circle with center O is 16 cm long. The distance from O to AB is 6 cm. '
                      'What is the circumference of the circle (in cm)?',
            ['$16\\pi$', '$10\\pi$', '$20\\pi$', '$100\\pi$'], 3, [
                'Draw the perpendicular OM from O to AB. It cuts the chord in half: $AM=MB=\\frac{16}{2}=8$.',
                'Right triangle OMB: $OB^2=6^2+8^2=100$, so the radius is $OB=10$.',
                'Circumference: $2\\pi\\cdot10=20\\pi$. ($100\\pi$ is the area, and $10\\pi$ takes 10 as the diameter.)'],
            figure=fig_chord_q())
    M.place_q(g, LEARN1, after='solve-geo33-g076')
    pre = lambda: [_qfig(g, fig_chord_q(), VB_CHORD)]
    _solution(M, g, 'A chord, its distance and the radius', 'Circle Chord Question',
              ["Let's solve a sample question.", "A chord and its distance from the center — one helper line does it."], [
        ('Draw the distance', [
            "Chord AB is 16. Its distance from the center is 6. What is the circumference?",
            "The distance from a point to a line is a perpendicular.",
            D('Draw OM ⊥ AB and mark the right angle at M'),
            "Draw it from O to the chord, and call its foot M.",
            A('AM = MB = 16 ÷ 2 = 8 appears', _bt('$AM=MB=\\frac{16}{2}=8$', 0)),
            "The perpendicular from the center cuts the chord in half: 8 and 8.",
            D('Draw the radius OB'),
            "Now draw the radius to the end of the chord: OB.",
        ], pre()),
        ('Pythagoras, then C', [
            "Right triangle OMB: the legs are 6 and 8.",
            A('r² = 6² + 8² = 100 → r = 10 appears', _bt('$r^2=6^2+8^2=100\\ \\Rightarrow\\ r=10$', 0)),
            "6, 8, 10 — a Pythagorean triple. The radius is 10.",
            A('C = 2π · 10 = 20π appears', _bt('$C=2\\pi\\cdot10=20\\pi$', 1)),
            "Circumference: 2π times 10 — 20π.",
            D('Circle choice 3'),
            "Choice three.",
            D('Cross out 100π and 10π'),
            "100π is the area. 10π — someone who took 10 as the diameter.",
        ], pre()),
    ], 45)

    # ---- circle inside a right triangle ----
    g = GID[1]
    M.new_q(g, TOPIC, 'A circle is inscribed in a right triangle whose legs are 8 cm and 15 cm. '
                      'What is the radius of the circle (in cm)?',
            ['$6$', '$8.5$', '$3$', '$1.5$'], 3, [
                'Hypotenuse: $\\sqrt{8^2+15^2}=\\sqrt{289}=17$.',
                'Tangent pieces from one vertex are equal. At the right angle both pieces are r, so the pieces on the '
                'hypotenuse are $8-r$ and $15-r$: $(8-r)+(15-r)=17$, so $23-2r=17$ and $r=3$.',
                'Shortcut for a right triangle: $r=\\frac{a+b-c}{2}=\\frac{8+15-17}{2}=3$. '
                '($8.5$ is half the hypotenuse: the radius of the circle around the triangle.)'],
            figure=fig_incircle_q())
    M.place_q(g, LEARN1, after='solve-geo33-g078')
    pre = lambda: [_qfig(g, fig_incircle_q(), VB_INC)]
    _solution(M, g, 'A circle inside a right triangle', 'Tangents Question',
              ["Let's solve a sample question.", "A circle inside a triangle — equal tangent pieces."], [
        ('Tangent pieces', [
            "Legs 8 and 15. A circle inside touches all three sides. What is its radius?",
            A('c = √(8² + 15²) = 17 appears', _bt('$c=\\sqrt{8^2+15^2}=\\sqrt{289}=17$', 0, 34)),
            "First the hypotenuse: 64 plus 225 is 289. The root: 17.",
            D('Draw the radii to the two legs: a small square r by r at the right angle'),
            "At the right angle, the radii to the legs make a little square. So the tangent pieces there are r and r.",
            D('Write 8 − r and 15 − r on the rest of the legs'),
            "The rest of the legs: 8 minus r, and 15 minus r.",
        ], pre()),
        ('Equal tangents', [
            "Two tangents from one vertex are equal. So the same pieces sit on the hypotenuse.",
            A('(8 − r) + (15 − r) = 17 appears', _bt('$(8-r)+(15-r)=17$', 0)),
            A('23 − 2r = 17 → r = 3 appears', _bt('$23-2r=17\\ \\Rightarrow\\ r=3$', 1)),
            "23 minus 2r is 17. So 2r is 6 — r is 3.",
            D('Circle choice 3'),
            "Choice three.",
        ], pre()),
        ('Shortcut and trap', [
            A('r = (a + b − c)/2 = (8 + 15 − 17)/2 = 3 appears', _bt('$r=\\frac{a+b-c}{2}=\\frac{8+15-17}{2}=3$', 0, 34)),
            "The shortcut for a right triangle: leg plus leg minus hypotenuse, over 2.",
            "8 plus 15 minus 17 is 6. Half of it — 3.",
            D('Cross out 8.5'),
            "8.5 is half the hypotenuse. That is the radius of the circle AROUND a right triangle — not inside it.",
        ], pre()),
    ], 47)

    # ---- scaling ----
    g = GID[2]
    M.new_q(g, TOPIC, 'The circumference of a circle increases by 50%. By what percent does its area increase?',
            ['$50\\%$', '$100\\%$', '$225\\%$', '$125\\%$'], 4, [
                'The circumference grows like the radius: the radius is multiplied by 1.5.',
                'The area grows like the radius squared: $1.5^2=2.25$.',
                'The new area is $225\\%$ of the old one: an increase of $225\\%-100\\%=125\\%$.',
                'Check with numbers: $r=2\\to3$. The area goes from $4\\pi$ to $9\\pi$: up $5\\pi$, and $\\frac{5\\pi}{4\\pi}=1.25=125\\%$.'])
    M.place_q(g, LEARN1, after='solve-geo33-g080')
    _solution(M, g, 'Scaling a circle: lengths and areas', 'Area and Circumference Question',
              ["Let's solve a sample question.", "The radius grows — how much does the area grow?"], [
        ('Length × 1.5, area × 1.5²', [
            "The circumference goes up 50 percent. By what percent does the area go up?",
            "The circumference is 2π r — it grows exactly like the radius. So the radius is multiplied by 1.5.",
            A('r × 1.5 → S × 1.5² = 2.25 appears', _bw('$r\\times1.5\\ \\Rightarrow\\ S\\times1.5^2=2.25$', 0)),
            "The area grows like r squared: 1.5 squared — 2.25.",
            A('225% − 100% = 125% appears', _bw('$225\\%-100\\%=125\\%$', 1)),
            "Times 2.25 means 225 percent of the old area. The increase: 125 percent.",
            D('Circle choice 4'),
            "Choice four.",
            D('Cross out 225% and 50%'),
            "225 is the new area, not the increase. And 50 — someone who forgot the square.",
        ], [Q(g)]),
        ('Check with numbers', [
            "Not sure? Plug in numbers. Radius 2 becomes 3 — that's 50 percent more.",
            A('r = 2 → 3: 4π → 9π appears', _bw('$r=2\\to3$: $\\ S=4\\pi\\to9\\pi$', 0)),
            "The area: 4π becomes 9π. It went up by 5π.",
            A('5π ÷ 4π = 1.25 = 125% appears', _bw('$\\frac{5\\pi}{4\\pi}=1.25=125\\%$', 1)),
            "5π out of 4π: 1.25 — 125 percent. The same answer.",
        ], [Q(g)]),
    ], 49)


# ------------------------------------------------------------------------------------------------
# 6. "Further guided examples": a short lesson with four tools + two guided questions + a card
# ------------------------------------------------------------------------------------------------
VB_SEG, VB_CT = '184.5 40 271 275', '100 50 420 300'


def _tools_block(M):
    sb = ['Segment', 'Two equal circles', 'Common tangent', 'Chord of a ring']
    v = M.new_video(TOOLS, TOPIC, 'More Circle Tools', sb, [
        dict(mode='title', title='More Circle Tools', script=[
            "Four more tools for the hardest circle questions.",
            "Each one shows up near the end of the section.",
        ]),
        dict(mode='concept', active=0, title='Segment = sector − triangle', script=[
            A('A circle with a chord AB and the region between the chord and the arc appears',
              VIS(fig_segment(), w=1000, h=520)),
            "A chord cuts off a piece of the circle: the region between the chord and the arc. It's called a segment.",
            A('Segment = sector − triangle', T('Segment $=$ sector $-$ triangle', size=46, x=410, y=650)),
            "Its area: the sector, minus the triangle.",
            "Here the radius is 6, and the angle at O is 90.",
            D('Write "sector: ¼ · 36π = 9π"'),
            "The sector: 90 is a quarter. A quarter of 36π — 9π.",
            D('Write "triangle: 6 · 6 ÷ 2 = 18"'),
            "The triangle: a right triangle with legs 6 and 6 — 18.",
            D('Write "segment: 9π − 18"'),
            "The segment: 9π minus 18.",
        ]),
        dict(mode='concept', active=1, title='Two equal circles', script=[
            "Two equal circles — and each one passes through the center of the other.",
            A('Two equal circles with centers O and P, crossing at A and B, appear', VIS(fig_lens(), w=1000, h=520)),
            "Join the centers and the two crossing points. Every one of these lines is a radius.",
            A('All sides = r → two equilateral triangles',
              T('All sides $=r\\ \\Rightarrow$ two equilateral triangles $\\Rightarrow\\ \\angle AOB=120°$', size=38, x=410, y=650)),
            "So both triangles are equilateral — 60 degrees everywhere. The angle at O: 60 plus 60 — 120. A third of the circle.",
            A('Common region = 2 segments', T('Common region $=2$ segments', size=38, x=410, y=730)),
            "The shaded region is two equal segments. Each one: a 120-degree sector minus the triangle AOB.",
        ]),
        dict(mode='concept', active=2, title='Common tangent', script=[
            "Two circles touch, and a line touches both of them. How far apart are the touching points?",
            A('Two tangent circles with radii 8 and 2 on a common tangent line appear',
              VIS(fig_common_tangent(), w=1000, h=520)),
            "Radii to the touching points: both are perpendicular to the line.",
            "Join the centers: 8 plus 2 — 10.",
            "From B, draw a line parallel to the tangent. It cuts off a right triangle.",
            A('DC² + (R − r)² = (R + r)²',
              T('$DC^2+(R-r)^2=(R+r)^2$', size=42, x=410, y=650)),
            "Its legs: DC, and 8 minus 2 — 6. The hypotenuse: 10.",
            D('Write "DC = √(10² − 6²) = 8"'),
            "So DC is 8.",
            A('Touching circles: DC = 2√(Rr)', T('Touching circles: $DC=2\\sqrt{Rr}$', size=42, x=410, y=740)),
            "A shortcut when the circles touch: 2 root of R times r. 2 root 16 — 8 again.",
        ]),
        dict(mode='concept', active=3, title='Chord of a ring', script=[
            "Two circles with the same center. A chord of the big circle just touches the small one.",
            A('Two circles with the same center and a chord AB that touches the small circle appear',
              VIS(fig_ring_chord(), w=1000, h=520)),
            "The small radius to the touching point is perpendicular to the chord — and cuts it in half. Call each half h.",
            A('R² − r² = h²  ·  ring = πh²',
              T('$R^2-r^2=h^2\\ \\Rightarrow$ ring $=\\pi R^2-\\pi r^2=\\pi h^2$', size=40, x=410, y=650)),
            "Pythagoras: R squared minus r squared is h squared. And the ring is π R squared minus π r squared — that's π h squared.",
            D('Write "chord 10 → h = 5 → ring = 25π"'),
            "A chord of 10? h is 5, and the ring is 25π — without knowing either radius.",
            "Now let's solve two questions.",
        ]),
    ], LEARN2, after='solve-geo33-g102')
    v['hybrid']['num'] = 58

    # ---- guided: segment ----
    g = GID[3]
    M.new_q(g, TOPIC, 'In a circle with center O and radius 6 cm, angle AOB is 60°. What is the area of the shaded '
                      'region between chord AB and arc AB (in cm²)?',
            ['$6\\pi-18$', '$12\\pi-9\\sqrt3$', '$6\\pi-9\\sqrt3$', '$3\\pi-9\\sqrt3$'], 3, [
                'Segment $=$ sector $-$ triangle.',
                'Sector: $60°$ is $\\frac16$ of the circle: $\\frac16\\cdot\\pi\\cdot6^2=6\\pi$.',
                'Triangle AOB: $OA=OB=6$ and $\\angle AOB=60°$, so it is equilateral with side 6: $\\frac{6^2\\sqrt3}{4}=9\\sqrt3$.',
                'Segment: $6\\pi-9\\sqrt3$. ($3\\pi-9\\sqrt3$ is negative: $3\\pi\\approx9.4$ and $9\\sqrt3\\approx15.6$.)'],
            figure=fig_segment_q())
    M.place_q(g, LEARN2, after=TOOLS)
    pre = lambda: [_qfig(g, fig_segment_q(), VB_SEG)]
    _solution(M, g, 'A segment: sector minus triangle', 'Advanced Circles III',
              ["Let's solve a sample question.", "A segment — sector minus triangle."], [
        ('Sector minus triangle', [
            "Radius 6, and angle AOB is 60. What is the area between the chord and the arc?",
            A('Segment = sector − triangle appears', _bt('Segment $=$ sector $-$ triangle', 0, 34)),
            "This region is a segment. The scheme: the sector, minus the triangle.",
            A('Sector: 1/6 · 36π = 6π appears', _bt('Sector: $\\frac16\\cdot36\\pi=6\\pi$', 1)),
            "The sector: 60 is a sixth. The circle is 36π — a sixth of it is 6π.",
        ], pre()),
        ('The triangle', [
            "Triangle AOB: two radii and 60 degrees between them. The base angles are equal — 60 each. It's equilateral, with side 6.",
            A('Triangle: 6²√3 / 4 = 9√3 appears', _bt('$\\triangle AOB=\\frac{6^2\\sqrt3}{4}=9\\sqrt3$', 0)),
            "Area: a squared root 3 over 4 — 36 root 3 over 4 — 9 root 3.",
            A('6π − 9√3 appears', _bt('$6\\pi-9\\sqrt3$', 1)),
            "The segment: 6π minus 9 root 3.",
            D('Circle choice 3'),
            "Choice three.",
        ], pre()),
        ('The traps', [
            D('Next to choice 4 write "3π ≈ 9.4 < 9√3 ≈ 15.6"'),
            "3π minus 9 root 3 is negative. An area can't be negative.",
            D('Next to choice 1 write "6 · 6 ÷ 2 ✗"'),
            "6π minus 18: that treats the triangle as a right triangle. It isn't — the angle is 60.",
            "12π minus 9 root 3: a third of the circle instead of a sixth.",
        ], pre()),
    ], 59)

    # ---- guided: common tangent ----
    g = GID[4]
    M.new_q(g, TOPIC, 'Two circles with centers A and B touch each other from the outside. Their radii are 8 cm and 2 cm. '
                      'A line touches the two circles at D and C, as in the figure. What is the length of DC (in cm)?',
            ['$10$', '$8$', '$6$', '$2\\sqrt{34}$'], 2, [
                'Draw the radii AD and BC. Both are perpendicular to the line DC, so ABCD is a right trapezoid. '
                'The centers: $AB=8+2=10$.',
                'Draw BE parallel to DC, with E on AD: $AE=8-2=6$ and $BE=DC$.',
                'Right triangle ABE: $DC=BE=\\sqrt{10^2-6^2}=\\sqrt{64}=8$.',
                'Shortcut for circles that touch: $DC=2\\sqrt{Rr}=2\\sqrt{8\\cdot2}=8$.'],
            figure=fig_common_tangent_q())
    M.place_q(g, LEARN2, after='solve-' + GID[3])
    pre = lambda: [_qfig(g, fig_common_tangent_q(), VB_CT)]
    _solution(M, g, 'The common tangent of two touching circles', 'Advanced Circles III',
              ["Let's solve a sample question.", "Two touching circles and a common tangent — build a right triangle."], [
        ('Radii and the centers', [
            "Two circles touch. The radii are 8 and 2. A line touches them at D and C. How long is DC?",
            "Tangent points — automatic helper lines: the radii.",
            D('Draw AD and BC with right angles at D and C'),
            "Both radii are perpendicular to the same line, so they are parallel.",
            D('Draw AB and write 8 + 2 = 10'),
            A('AB = 8 + 2 = 10 appears', _bt('$AB=8+2=10$', 0)),
            "Touching circles — join the centers: 8 plus 2, 10. We get a right trapezoid ABCD.",
        ], pre()),
        ('Cut off a right triangle', [
            D('Draw BE ∥ DC, with E on AD'),
            "From B, draw a line parallel to DC, to the point E on AD.",
            A('AE = 8 − 2 = 6 appears', _bt('$AE=8-2=6$', 0)),
            "ED equals BC, which is 2 — so AE is 8 minus 2: 6.",
            A('DC = BE = √(10² − 6²) = 8 appears', _bt('$DC=BE=\\sqrt{10^2-6^2}=8$', 1)),
            "Right triangle ABE: hypotenuse 10, leg 6. The other leg is 8 — a 6-8-10 triangle. And BE equals DC.",
            D('Circle choice 2'),
            "DC is 8. Choice two.",
        ], pre()),
        ('Traps and a shortcut', [
            "10 is AB — the distance between the centers, not the tangent. 6 is only the difference of the radii.",
            "2 root 34: someone added the squares instead of subtracting. But 10 is the hypotenuse — the longest side.",
            A('Touching circles: DC = 2√(Rr) appears', _bt('Touching circles: $DC=2\\sqrt{Rr}=2\\sqrt{16}=8$', 0, 32)),
            "For circles that touch, a shortcut: 2 root of R times r. 2 root 16 — 8.",
        ], pre()),
    ], 59)

    M.new_card('mem-r26-t33-more-tools', TOPIC, LEARN2, {
        'title': 'Circles — more tools',
        'intro': 'Four tools for the hardest circle questions.',
        'tables': [{'title': '', 'head': ['Tool', 'What it says', 'Example'], 'rows': [
            ['!Segment', 'segment \\(=\\) sector \\(-\\) triangle', 'radius 6, \\(60°\\): \\(6\\pi-9\\sqrt3\\)'],
            ['Two equal circles, each through the other\'s center', 'two equilateral triangles, \\(\\angle AOB=120°\\); common region \\(=2\\) segments',
             'radius 4: \\(\\frac{32\\pi}{3}-8\\sqrt3\\)'],
            ['!Common tangent', 'radii \\(\\perp\\) tangent; right triangle with legs DC and \\(R-r\\), hypotenuse \\(R+r\\)',
             'touching circles: \\(DC=2\\sqrt{Rr}\\)'],
            ['Chord of a ring (touches the small circle)', 'half chord \\(h\\): ring \\(=\\pi h^2\\)', 'chord 10: ring \\(25\\pi\\)'],
        ]}],
        'tips': ['Shaded region with a curved edge and a straight edge? Sector minus triangle.',
                 'Tangent line to two circles: draw both radii to it, join the centers, and cut off a right triangle.'],
    }, after='solve-' + GID[4])


# ------------------------------------------------------------------------------------------------
# 7. Memory cards
# ------------------------------------------------------------------------------------------------
def _cards(M):
    c = M.card('mem-circle-rules')
    c['tables'][0]['rows'] += [
        ['Right angle on the circle', 'rests on a diameter: a right triangle\'s hypotenuse (a rectangle\'s diagonal) is a diameter'],
        ['!Chord and center', 'the perpendicular from the center cuts a chord in half: '
                              '\\(d^2+\\left(\\frac{\\text{chord}}{2}\\right)^2=r^2\\)'],
        ['Circle inside a triangle', 'tangent pieces from each vertex are equal; right triangle: \\(r=\\frac{a+b-c}{2}\\)'],
        ['Tangent circles', 'distance between the centers: \\(R+r\\) (from outside) or \\(R-r\\) (from inside)'],
    ]
    c['tips'] = c['tips'] + ['Distance from the center to a chord? Draw the perpendicular — it halves the chord.']
    c = M.card('mem-circle-formulas')
    c['tables'][0]['rows'] += [
        ['!Scaling', 'radius \\(\\times k\\): \\(C\\times k\\), \\(S\\times k^2\\)', 'radius \\(+20\\%\\) \\(\\rightarrow\\) area \\(+44\\%\\)'],
        ['Wheel turns', '\\(\\frac{\\text{distance}}{\\text{circumference}}\\)', 'same units first (m \\(\\rightarrow\\) cm)'],
    ]
    c['tips'] = c['tips'] + ['A regular hexagon in a circle: its side equals the radius (six equilateral triangles).']


# ------------------------------------------------------------------------------------------------
# 8. Practice: remove near-duplicates, add chord / tangent / scaling / "which statement" questions, order easy -> hard
# ------------------------------------------------------------------------------------------------
def _practice(M):
    # pass 2: p09, p13, p25 and adv-p08 are original questions - they stay (restored, text cleaned up)
    F = lambda q: M.q(q)['questionVisual']['svg']
    M.set_q('geo33-foundation-p09', stem='Circles with centers K and M intersect at A and B. MA is tangent to the circle with '
            'center K at A, and KB is tangent to the circle with center M at B. Given: $\\angle AMB=72°$. What is angle AKB?',
            figure=_q_to_mark(F('geo33-foundation-p09'), 'α'), expl=[
                'Radius to the point of tangency: $KA\\perp MA$ and $MB\\perp KB$, so $\\angle KAM=\\angle KBM=90°$.',
                'The angles of quadrilateral KAMB add up to $360°$: $\\angle AKB=360°-90°-90°-72°=108°$.'])
    M.set_q('geo33-foundation-p13', stem='ABC is an isosceles triangle. Given:\n'
            '$\\begin{cases} AB=AC \\\\ \\angle BCA=56° \\end{cases}$\n'
            'A circle with center O is tangent to AB and AC at D and E. What is the smaller angle DOE?',
            figure=_q_to_mark(F('geo33-foundation-p13'), 'α'), expl=[
                '$AB=AC$, so the base angles are equal: $\\angle A=180°-2\\cdot56°=68°$.',
                'Radii to the points of tangency: $\\angle ADO=\\angle AEO=90°$.',
                'The angles of quadrilateral ADOE add up to $360°$: $\\angle DOE=360°-90°-90°-68°=112°$.'])
    M.set_q('geo33-foundation-p25', expl=[
        'The area between the circles: $\\pi\\cdot3^2-\\pi\\cdot2^2=9\\pi-4\\pi=5\\pi$.',
        'The smaller disk: $\\pi\\cdot2^2=4\\pi$.',
        'The ratio: $5\\pi:4\\pi=5:4$.'])
    M.set_q('geo33-advanced-p08', expl=[
        'Same units first: the inner radius is $600$ m $=0.6$ km, and the outer radius is $600+100=700$ m $=0.7$ km.',
        'Path $=$ big disk $-$ small disk: $\\pi\\cdot0.7^2-\\pi\\cdot0.6^2=\\pi(0.49-0.36)=0.13\\pi$ km².'])

    P = {}
    P[5] = (FOUND, 'The area of a circle is multiplied by 9. By what number is its circumference multiplied?',
            ['$9$', '$3$', '$4.5$', '$81$'], 2, [
                'Area $\\times9=\\times3^2$, so the radius is multiplied by 3.',
                'The circumference grows like the radius: $\\times3$.',
                'Check: $r=1\\to3$. $C=2\\pi\\to6\\pi$ ($\\times3$) and $S=\\pi\\to9\\pi$ ($\\times9$).'], None)
    P[6] = (FOUND, 'A circle with center B and radius 4 cm lies inside a circle with center A and radius 9 cm. The two '
                   'circles touch at one point. What is AB (in cm)?',
            ['$13$', '$4$', '$5$', '$9$'], 3, [
                'One circle inside the other, touching: the distance between the centers is the difference of the radii.',
                '$AB=9-4=5$. (13 is the distance for circles that touch from outside.)'], fig_internal())
    P[8] = (ADVP, 'A circle is inscribed in triangle ABC and touches side AB at D. Given:\n'
                  '$\\begin{cases} AB=10\\text{ cm} \\\\ BC=12\\text{ cm} \\\\ CA=8\\text{ cm} \\end{cases}$\nWhat is BD (in cm)?',
            ['$5$', '$6$', '$7$', '$3$'], 3, [
                'Tangent pieces from one vertex are equal: x from A, y from B and z from C. '
                '$\\begin{cases} x+y=10 \\\\ y+z=12 \\\\ z+x=8 \\end{cases}$',
                'Add the three equations: $2(x+y+z)=30$, so $x+y+z=15$.',
                '$BD=y=15-(z+x)=15-8=7$.'], fig_incircle_bd())
    P[9] = (ADVP, 'Two circles have the same center. A chord of the larger circle is 16 cm long and touches the smaller '
                  'circle. What is the area between the two circles (in cm²)?',
            ['$16\\pi$', '$256\\pi$', '$64\\pi$', '$32\\pi$'], 3, [
                'The small radius to the touching point is perpendicular to the chord and cuts it in half: $h=8$.',
                'Right triangle: $R^2=r^2+8^2$, so $R^2-r^2=64$.',
                'Ring: $\\pi R^2-\\pi r^2=\\pi(R^2-r^2)=64\\pi$ — we never needed R or r.'], fig_ring_q())
    P[10] = (ADVP, 'In a circle with radius 5 cm, two parallel chords are 6 cm and 8 cm long. The center of the circle '
                   'is between the two chords. What is the distance between the chords (in cm)?',
             ['$1$', '$7$', '$5$', '$14$'], 2, [
                 'Chord 8: half of it is 4, and its distance from the center is $\\sqrt{5^2-4^2}=3$.',
                 'Chord 6: half of it is 3, and its distance from the center is $\\sqrt{5^2-3^2}=4$.',
                 'The center is between the chords: $3+4=7$. (1 is the distance when both chords are on the same side.)'], None)
    P[11] = (ADVP, 'In a circle with center O and radius 5 cm, chord AB is 8 cm long. Which of the following statements is true?',
             ['$\\angle AOB=90°$', 'The distance from O to AB is 4 cm', 'The area of triangle AOB is 12 cm²',
              '$\\angle OAB=45°$'], 3, [
                 'The perpendicular from O cuts AB in half: 4 and 4. The distance: $\\sqrt{5^2-4^2}=3$, not 4.',
                 'Triangle AOB: $\\frac{8\\cdot3}{2}=12$ — true.',
                 'If $\\angle AOB$ were $90°$, AB would be $5\\sqrt2\\approx7.07$, not 8. And $\\angle OAB=45°$ would need '
                 'the distance (3) to equal the half chord (4).'], None)
    P[13] = (ADVP, 'The radius of a circle decreases by 10%. By what percent does its area decrease?',
             ['$10\\%$', '$20\\%$', '$19\\%$', '$81\\%$'], 3, [
                 'The radius is multiplied by 0.9, so the area is multiplied by $0.9^2=0.81$.',
                 'The area is $81\\%$ of what it was: a decrease of $100\\%-81\\%=19\\%$.'], None)
    for k, (sec, stem, ch, cor, ex, fig) in P.items():
        M.new_q(GID[k], TOPIC, stem, ch, cor, ex, figure=fig)
        M.place_q(GID[k], sec)

    f = lambda n: 'geo33-foundation-p%02d' % n
    a = lambda n: 'geo33-advanced-p%02d' % n
    g = GID
    M.practice_order(FOUND, [
        f(1), f(10), f(12), f(2), f(25), 'wp26-p10', g[5], f(24), f(6), f(14), f(26), f(7), 'wp27-p10', f(21), f(19),
        f(20), f(18), f(17), f(23), f(27), g[6], f(22), f(5), f(4), f(3), f(8), f(9), f(11), f(13), f(16), f(15)])
    M.practice_order(ADVP, [
        a(1), a(7), a(9), a(22), a(8), a(2), a(12), a(13), a(3), a(10), a(14), a(25), a(26), a(16), a(4), a(5), a(6),
        a(11), a(17), a(18), a(21), g[10], g[11], g[13], a(24), g[9], a(19), a(15), g[8], a(20), a(23), a(27)])


# ------------------------------------------------------------------------------------------------
# 9. Pass 2: summary lessons right before each practice section
# ------------------------------------------------------------------------------------------------
def _summaries(M):
    last = lambda sec: [f['ref'] for f in M.D['flow'] if f['section'] == sec][-1]

    # ---- 1. before the foundation practice: everything taught in "Learn and try" ----
    sb = ['Radii', 'Central and inscribed', 'Diameter, quad', 'Chords', 'Tangents',
          'Circle in a triangle', 'Area and circumference', 'Sectors and arcs', 'Before you practice']
    M.new_video('r26-t33-summary', TOPIC, 'Circles: Summary', sb, [
        dict(mode='title', title='Summary', script=[
            "Circles — a quick summary before you practice.",
            "Everything important from these lessons, one idea at a time.",
        ]),
        dict(title='Radii', mode='concept', active=0, pre=[], script=[
            A('All radii are equal appears', T('All radii of one circle are equal $\\rightarrow$ isosceles triangles', size=40, gap=40)),
            "Rule number one: every radius is equal.",
            "Two radii and a chord? An isosceles triangle. They hide everywhere inside a circle.",
            A('d = 2r appears', T('Diameter $d=2r$ — the longest chord', size=44)),
            "The diameter is two radii. Diameter 30? The radius is 15. Switch to r before any formula.",
        ]),
        dict(title='Central and inscribed', mode='concept', active=1, pre=[], script=[
            A('central = 2 × inscribed appears', T('Central $=2\\times$ inscribed (same arc)', size=48, gap=40)),
            "The one big rule: the central angle is twice the inscribed angle on the same arc.",
            D('Write "central 100° → inscribed 50°"'),
            "Central 100? The inscribed angle is 50.",
            A('same arc → equal inscribed angles appears', T('Same arc $\\rightarrow$ equal inscribed angles', size=44)),
            "And all the inscribed angles on the same arc are equal.",
            "First ask: which arc does the angle rest on? Stand at the vertex — the arc you see is the one.",
        ]),
        dict(title='Diameter, quad', mode='concept', active=2, pre=[], script=[
            A('On a diameter: 90° appears', T('On a diameter: $\\frac{180°}{2}=90°$', size=48, gap=40)),
            "An inscribed angle on a diameter is 90.",
            "And backwards: a right triangle in a circle — its hypotenuse is a diameter. A rectangle — its diagonal.",
            A('Inscribed quadrilateral: α + β = 180° appears', T('Inscribed quadrilateral: opposite angles $\\alpha+\\beta=180°$', size=40)),
            "All four vertices on the circle? Opposite angles add up to 180. 65 here — 115 across.",
        ]),
        dict(title='Chords', mode='concept', active=3, pre=[], script=[
            A('Equal chords → equal central angles → equal arcs appears',
              T('Equal chords $\\rightarrow$ equal central angles $\\rightarrow$ equal arcs', size=38, gap=40)),
            "Equal chords cut off equal arcs and equal central angles. And backwards too.",
            A('d² + (chord/2)² = r² appears', T('$d^2+\\left(\\frac{\\text{chord}}{2}\\right)^2=r^2$', size=50, gap=30)),
            "The distance from the center to a chord? Draw the perpendicular. It cuts the chord in half.",
            D('Write "r = 5, d = 3 → half chord 4 → chord 8"'),
            "Radius 5, distance 3: half the chord is 4. The whole chord — 8.",
        ]),
        dict(title='Tangents', mode='concept', active=4, pre=[], script=[
            A('Radius ⊥ tangent appears', T('Radius to the point of tangency $\\perp$ tangent', size=42, gap=40)),
            "See a tangent? Draw the radius to the point of tangency. Automatically. 90 degrees.",
            A('Two tangents from one point are equal appears', T('Two tangents from one point are equal $\\rightarrow$ a kite', size=40)),
            "Two tangents from one point are equal. With the radii, they make a kite.",
            "The kite has two right angles, so the other two angles add up to 180.",
        ]),
        dict(title='Circle in a triangle', mode='concept', active=5, pre=[], script=[
            A('Equal tangent pieces appears', T('Circle inside a triangle: equal tangent pieces from each vertex', size=38, gap=30)),
            "A circle inside a triangle: from each vertex, two equal tangent pieces.",
            A('Right triangle: r = (a + b − c)/2 appears', T('Right triangle: $r=\\frac{a+b-c}{2}$', size=46, gap=40)),
            "Right triangle? Leg plus leg minus hypotenuse, over 2. Legs 12 and 16, hypotenuse 20 — r is 4.",
            A('Tangent circles: R + r or R − r appears', T('Tangent circles: $d=R+r$ (outside) $\\cdot$ $d=R-r$ (inside)', size=38)),
            "Two circles touch? Join the centers. Outside each other — R plus r. One inside the other — R minus r.",
        ]),
        dict(title='Area and circumference', mode='concept', active=6, pre=[], script=[
            A('S = πr², C = 2πr appears', T('$S=\\pi r^2\\qquad C=2\\pi r$', size=56, gap=40)),
            "Area: π r squared. Circumference: 2π r. Given the area or the circumference? Go back to r first.",
            "π is a bit more than 3. If the answers have π — keep the π.",
            A('r × k → C × k, S × k² appears', T('$r\\times k\\ \\Rightarrow\\ C\\times k,\\ \\ S\\times k^2$', size=46, gap=30)),
            "Lengths grow like the radius, areas like the radius squared. Radius plus 30 percent — area plus 69.",
            A('Turns = distance ÷ circumference appears', T('Wheel: turns $=\\frac{\\text{distance}}{\\text{circumference}}$ — same units!', size=38)),
            "And a wheel: one turn is one circumference. Change the units first.",
        ]),
        dict(title='Sectors and arcs', mode='concept', active=7, pre=[], script=[
            A('Which fraction of the circle? appears', T('Which fraction of the circle is it?', size=48, gap=40)),
            "Sectors and arcs: skip the formula. Ask which part of the circle it is.",
            A('angles to know appears', T('$90°=\\frac14\\quad60°=\\frac16\\quad72°=\\frac15\\quad45°=\\frac18\\quad120°=\\frac13$', size=44, gap=40)),
            "90 is a quarter, 60 a sixth, 72 a fifth, 45 an eighth, 120 a third.",
            D('Write "r = 4, 45°: sector 16π ÷ 8 = 2π · arc 8π ÷ 8 = π"'),
            "A sector — part of the area. An arc — part of the circumference.",
            A('Sector perimeter = arc + 2r appears', T('Sector perimeter $=$ arc $+\\,2r$', size=44)),
            "And the perimeter of a sector is the arc plus two radii.",
        ]),
        dict(title='Before you practice', mode='concept', active=8, pre=[], script=[
            "Before each question, ask yourself:",
            A('check 1 appears', T('Did I draw the helper lines? Radii, the radius to a tangent point, the line between the centers.', size=34, gap=24)),
            A('check 2 appears', T('Which arc does the angle rest on — the minor or the major one?', size=34, gap=24)),
            A('check 3 appears', T('Radius or diameter? Area or circumference? Arc or perimeter?', size=34, gap=24)),
            A('check 4 appears', T('Is it really an inscribed quadrilateral — are all four vertices on the circle?', size=34, gap=24)),
            "The common traps: 180 minus a central angle when the center is not on the circle, forgetting that area grows like r squared, and mixing up the radius and the diameter.",
            "You know all of this. Now practice.",
        ]),
    ], LEARN1, after=last(LEARN1))

    # ---- 2. before the advanced practice: everything taught in "Further guided examples" ----
    sb = ['Shaded areas', 'Segments', 'Nested shapes', 'Special triangles', 'Tangent and ring',
          'The whole, not the parts', 'Numbers and estimates', 'Before you practice']
    M.new_video('r26-t33-summary-2', TOPIC, 'Advanced Circles: Summary', sb, [
        dict(mode='title', title='Summary', script=[
            "Advanced circles — a quick summary before you practice.",
            "The tools for the hardest circle questions, one at a time.",
        ]),
        dict(title='Shaded areas', mode='concept', active=0, pre=[], script=[
            A('Shaded = what minus what? appears', T('Shaded area: what minus what?', size=50, gap=40)),
            "A shaded region? Don't calculate it directly. Build a scheme: which shape minus which shape.",
            D('Write "square 64 − quarter circle 16π = 64 − 16π"'),
            "A square with area 64, minus a quarter circle of 16π: the shaded part is 64 minus 16π.",
            "Overlapping circles? Split the region into pieces you know — or add both and take away the overlap.",
        ]),
        dict(title='Segments', mode='concept', active=1, pre=[], script=[
            A('Segment = sector − triangle appears', T('Segment $=$ sector $-$ triangle', size=50, gap=40)),
            "The region between a chord and its arc: the sector, minus the triangle.",
            D('Write "r = 4, 60°: 8π/3 − 4√3"'),
            "Radius 4, angle 60: the sector is 8π over 3. The triangle is equilateral — 4 root 3.",
            A('Two equal circles through each other’s centers appears',
              T('Two equal circles, each through the other’s center: $120°$, common region $=2$ segments', size=36)),
            "Two equal circles through each other's centers: two equilateral triangles, 120 degrees, and two segments.",
        ]),
        dict(title='Nested shapes', mode='concept', active=2, pre=[], script=[
            A('square · circle · square appears', T('Square $\\cdot$ circle $\\cdot$ square: area $\\times2$', size=44, gap=30)),
            A('circle · square · circle appears', T('Circle $\\cdot$ square $\\cdot$ circle: area $\\times2$', size=44, gap=30)),
            A('triangle · circle · triangle appears', T('Triangle $\\cdot$ circle $\\cdot$ triangle: area $\\times4$', size=44, gap=40)),
            "Three nested objects to know by heart. Square in a circle in a square — twice. Circle, square, circle — twice. Equilateral triangles — four times.",
            "Anything else inside a circle? Write every length with r.",
            "And careful: a length factor is not an area factor. Root 2 for lengths is 2 for areas.",
        ]),
        dict(title='Special triangles', mode='concept', active=3, pre=[], script=[
            A('30°-60°-90° appears', T('$30°$-$60°$-$90°$: $\\ x,\\ x\\sqrt3,\\ 2x$', size=48, gap=30)),
            A('45°-45°-90° appears', T('$45°$-$45°$-$90°$: $\\ x,\\ x,\\ x\\sqrt2$', size=48, gap=40)),
            "Radii and tangents make right triangles all the time.",
            "A leg that is half of the hypotenuse? That's the 30-60-90 triangle. Two equal legs? 45-45-90.",
            "Two radii and a 60-degree angle? An equilateral triangle.",
        ]),
        dict(title='Tangent and ring', mode='concept', active=4, pre=[], script=[
            A('DC² + (R − r)² = (R + r)² appears', T('Common tangent: $DC^2+(R-r)^2=(R+r)^2$', size=42, gap=30)),
            "A line touches two touching circles: radii to the line, join the centers, cut off a right triangle.",
            A('Touching: DC = 2√(Rr) appears', T('Touching circles: $DC=2\\sqrt{Rr}$', size=44, gap=40)),
            "Radii 18 and 2: 2 root 36 — 12.",
            A('Ring = πh² appears', T('Chord of a ring: ring $=\\pi h^2$ ($h=$ half the chord)', size=40)),
            "A chord of the big circle that touches the small one? The ring is π times half the chord, squared.",
        ]),
        dict(title='The whole, not the parts', mode='concept', active=5, pre=[], script=[
            A('Find the total directly appears', T('They ask for a total? Find the total directly.', size=44, gap=40)),
            "Two arcs together, two sectors together — you often can't find each one. You don't need to.",
            D('Write "4α + 4β = 360° → α + β = 90°"'),
            "Four α and four β make a full turn: α plus β is 90. That's all we need.",
        ]),
        dict(title='Numbers and estimates', mode='concept', active=6, pre=[], script=[
            A('Plug in numbers appears', T('Letters in the answers? Plug in numbers: $r=2$, $\\alpha=30$', size=40, gap=30)),
            "Letters in the question? Choose easy numbers, solve, and test the choices.",
            A('Estimate appears', T('Estimate: $\\pi\\approx3.14$, a circle $<$ the square around it', size=40, gap=30)),
            "Estimate sizes to cross out choices. An area can't be negative. A circle is smaller than the square around it.",
            "And a ratio of two lengths can't contain r.",
        ]),
        dict(title='Before you practice', mode='concept', active=7, pre=[], script=[
            "Before each question, ask yourself:",
            A('check 1 appears', T('What minus what? Write the scheme before you calculate.', size=34, gap=24)),
            A('check 2 appears', T('Which helper lines? Radii, the line between the centers, a perpendicular.', size=34, gap=24)),
            A('check 3 appears', T('Is a special triangle hiding here: equilateral, 30-60-90 or 45-45-90?', size=34, gap=24)),
            A('check 4 appears', T('Can I plug in numbers or estimate to cross out choices?', size=34, gap=24)),
            "The common traps: treating a triangle as a right triangle when it isn't, taking the wrong fraction of the circle, and a length factor used for an area.",
            "You know all of this. Now practice.",
        ]),
    ], LEARN2, after=last(LEARN2))


# ================================================================================================
# 2026-10-05 cut repeats: a lesson slide that the next question video teaches again is removed
# (the teacher: the Hebrew course has a short intro, and each question video teaches its own idea).
# ================================================================================================
def _cr_cut(M, vid, ns):
    """remove slides ns (1-based) and drop their sidebar labels; the other slides' 'active' indexes follow."""
    v = M.video(vid)
    gone = {v['beats'][n - 1].get('active') for n in ns}
    M.remove_slides(vid, ns)
    side = v.get('hybrid', {}).get('sidebar')
    if side is None: return
    used = {b.get('active') for b in v['beats']}
    drop = sorted(a for a in gone if a is not None and a >= 0 and a not in used)
    for b in v['beats']:
        a = b.get('active')
        if a is not None and a >= 0: b['active'] = a - sum(1 for d in drop if d < a)
    M.set_sidebar(vid, [l for k, l in enumerate(side) if k not in drop])


def _cr_say(M, vid, n, old, new):
    """replace a spoken line (by its start); new=None deletes it."""
    def fn(lines):
        k = next(i for i, l in enumerate(lines) if l.get('say', '').startswith(old))
        if new is None: lines.pop(k)
        else: lines[k] = dict(lines[k], say=new)
        return lines
    M.edit_lines(vid, n, fn)


def _cr_add(M, vid, n, after, says, item=None, label=None):
    """add spoken lines (and optionally one board item that appears before them) after the line starting with `after`
    (after=None: at the end of the slide)."""
    b = M.slide(vid, n)
    new = []
    if item is not None:
        b['items'].append(item)
        new.append({'appear': len(b['items']) - 1, 'label': label})
    new += [{'say': s} for s in says]
    def fn(lines):
        k = len(lines) if after is None else next(i for i, l in enumerate(lines) if l.get('say', '').startswith(after)) + 1
        return lines[:k] + new + lines[k:]
    M.edit_lines(vid, n, fn)


def cut_repeats(M):
    # --- Angles in a Circle (geo-075): slide 9 "Chord and center" is taught again by the next question video,
    #     solve-q-r26-t33-01 (perpendicular from the center halves the chord; radius as hypotenuse; Pythagoras).
    _cr_cut(M, 'geo-075', [9])
    _cr_add(M, 'geo-075', 8, None, ["Now let's solve a sample question."])

    # --- Tangents (geo-077): slide 5 "Circle inside a triangle" = solve-q-r26-t33-02 (equal tangent pieces, the little
    #     square at the right angle, leg + leg − hypotenuse over 2). Slide 6 "Tangent circles": joining the centers and
    #     R + r are taught in solve-geo33-g088 (OM = 4 + 4) and solve-geo33-g092; R − r moves there as one line.
    _cr_cut(M, 'geo-077', [5, 6])
    _cr_add(M, 'geo-077', 4, None, ["Let's solve a sample question."])
    _cr_add(M, 'solve-geo33-g088', 3, 'The first part is a radius of circle O.',
            ["Two circles touch? Join the centers. Outside each other — R plus r. One inside the other — R minus r."],
            T('Touching circles: outside $R+r$ · inside $R-r$', size=30, x=1060, y=420, w=470),
            "'Touching circles: outside R + r · inside R − r' appears")

    # --- Area and Circumference (geo-079): slide 8 "Scale the radius" = solve-q-r26-t33-03 (lengths grow like r,
    #     areas like r squared). Its "backwards" line moves there.
    _cr_cut(M, 'geo-079', [8])
    _cr_add(M, 'solve-q-r26-t33-03', 2, 'The area grows like r squared',
            ["It works backwards too: the area 9 times bigger — the radius only 3 times bigger."],
            T(r'Backwards: $S\times9\ \Rightarrow\ r\times3$', size=40, x=410, y=460, w=1100),
            "'Backwards: S × 9 → r × 3' appears")

    # --- More Circle Tools (r26-t33-more-tools): slide 2 "Segment" = solve-q-r26-t33-04 (sector minus triangle);
    #     slide 4 "Common tangent" = solve-q-r26-t33-05 (same numbers, 8 and 2, same steps, same shortcut).
    _cr_cut(M, 'r26-t33-more-tools', [2, 4])
    _cr_say(M, 'r26-t33-more-tools', 1, 'Four more tools', 'Two more tools for the hardest circle questions.')
    _cr_say(M, 'r26-t33-more-tools', 1, 'Each one shows up', 'Two more come in the questions after this lesson.')
    _cr_say(M, 'r26-t33-more-tools', 2, 'The shaded region is two equal segments',
            'The shaded region is two equal pieces. Each one: a 120-degree sector minus the triangle AOB.')
    b = M.slide('r26-t33-more-tools', 2)
    b['items'][2]['t'] = r'Common region $=2\times$(sector $-$ triangle)'
    M.edit_lines('r26-t33-more-tools', 2, lambda L: [dict(l, label='Common region = 2 × (sector − triangle)')
                                                    if l.get('label') == 'Common region = 2 segments' else l for l in L])


# ================================================================================================================
# 2026-10-06 renumber pass (runs LAST, after cut_repeats). The English course must not look like the Hebrew one:
# every Hebrew-derived question (guided geo33-g076 ... g102, practice geo33-foundation-p01 ... p20,
# geo33-advanced-p01 ... p20, and wp26-p10 / wp27-p10 that live in this topic's practice) gets new numbers (and a
# changed story / new letters where there is one); idea, trap, level and methods stay. Every guided solution video is
# rewritten to match, figures are redrawn. Hebrew-derived lesson examples (70/110, a circle of 25π in fifths) and
# summary / card examples that copied the Hebrew or a question get new numbers. Practice clean-up 63 -> 49.
# Nothing in topic 33 is recorded (checked ~/Documents/Course.recordings 2026-10-06).
# ================================================================================================================
RN_RECORDED = set()
_RN_CW = {'one': 1, 'two': 2, 'three': 3, 'four': 4}
_RN_WC = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}
_RN_CHOICE = re.compile(r'\b([Cc]hoices? )((?:[1-4]|one|two|three|four)(?:(?:, | and | or )(?:[1-4]|one|two|three|four))*)\b')


def _rn_rx(old):
    e = re.escape(old)
    if old[0].isdigit(): e = r'(?:(?<![\d.A-Za-z/])|(?<=\\cdot)|(?<=\\times))' + e
    if old[-1].isdigit(): e = e + r'(?!\d)'
    return e


def _rn_text(s, pairs, perm, hits):
    """one pass: choice references are permuted (old position -> new position), then all pairs are replaced at once
    (no chained replacements)."""
    keep = []

    def prot(m):
        toks = re.split(r'(, | and | or )', m.group(2))
        nums = [t for k, t in enumerate(toks) if k % 2 == 0]
        if perm:
            new = []
            for t in nums:
                if t.isdigit(): new.append(str(perm[int(t)]))
                else:
                    w = _RN_WC[perm[_RN_CW[t.lower()]]]
                    new.append(w.capitalize() if t[0].isupper() else w)
            if len(new) > 1:
                key = lambda x: int(x) if x.isdigit() else _RN_CW[x.lower()]
                new = sorted(new, key=key)
                if not new[0].isdigit() and toks[0][0].isupper(): new = [w.lower() for w in new]; new[0] = new[0].capitalize()
            toks = [new[k // 2] if k % 2 == 0 else t for k, t in enumerate(toks)]
        keep.append(m.group(1) + ''.join(toks))
        return '\x00' + ''.join('abcdefghij'[int(c)] for c in str(len(keep) - 1)) + '\x00'
    s = _RN_CHOICE.sub(prot, s)
    if pairs:
        d = dict(pairs)
        rx = re.compile('|'.join(_rn_rx(o) for o in sorted(d, key=len, reverse=True)))

        def rep(m):
            hits.add(m.group(0)); return d[m.group(0)]
        s = rx.sub(rep, s)
    return re.sub('\x00([a-j]+)\x00', lambda m: keep[int(''.join(str('abcdefghij'.index(c)) for c in m.group(1)))], s)


def _rn_video(M, vid, pairs=(), perm=None, slides=None):
    """Whole-video rewrite: number / word pairs and choice permutation in every title, spoken line, draw cue, label
    and board item (the title slide's big 'Question N' stays). slides={n: (title or None, script)} rewrites slides."""
    if vid in RN_RECORDED: return
    v = M.video(vid)
    for n, (title, script) in (slides or {}).items():
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, title=title, script=script)
    hits = set()
    for b in v['beats']:
        if b['mode'] != 'title': b['title'] = _rn_text(b['title'], pairs, perm, hits)
        for l in b['lines']:
            for k in ('say', 'draw', 'label'):
                if k in l: l[k] = _rn_text(l[k], pairs, perm, hits)
        for it in b['items']:
            if it.get('t'): it['t'] = _rn_text(it['t'], pairs, perm, hits)
    miss = [o for o, _ in pairs if o not in hits]
    assert not miss, (vid, miss)
    M.touched_videos.add(vid)


def _rn_q(M, qid, stem, choices, correct, expl, figure=Ellipsis, vb=None):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)
    if figure is not Ellipsis: _set_fig(M, qid, figure, vb)


def _rn_lbl(svg, mp, count=None):
    """rename <text> labels at once (each old label must exist)."""
    keep = {}
    for k, (o, n) in enumerate(mp.items()):
        tag = '>%s</text>' % o
        assert tag in svg, o
        svg = svg.replace(tag, '>\x00%d\x00</text>' % k); keep[k] = n
    return re.sub('\x00(\\d+)\x00', lambda m: keep[int(m.group(1))], svg)


def _rn_fig(M, qid):
    return M.q(qid)['questionVisual']['svg']


# ---------------------------------------------------------------- figures (same style as the existing ones)
def rn_fig_g082():
    Pa, Pb = _P(10), _P(82)
    b = _c(CX, CY, R) + _lab(10, 'A') + _lab(82, 'B') + _dot((CX, CY)) + _t(305, 195, 'O')
    b += _l((CX, CY), Pa, TEAL) + _l((CX, CY), Pb, TEAL)
    b += ('<path d="M %.3f %.3f A 109.500 109.500 0 0 0 %.3f %.3f" fill="none" stroke="#bb6821" stroke-width="6"/>'
          % (Pa + Pb))
    b += _angle((CX, CY), Pa, Pb, 29.2, 'α', 46)
    b += _lab(46, '4π', off=28)
    return _svg('A given arc length determines its central angle', b)


def rn_fig_g083():
    O = (CX, CY)
    b = _c(CX, CY, R) + _sector(0, 120) + _sector(200, 240)
    b += _angle(O, _P(0), _P(120), 32.85, '120°', 54) + _angle(O, _P(200), _P(240), 32.85, '40°', 56)
    b += _dot(O) + _t(338, 200, 'O')
    return _svg('Two separated sectors of a circle', b)


def rn_fig_g090():
    A0, B0, C0 = (280.0, 300.0), (364.0, 300.0), (280.0, 55.0)
    b = _poly([A0, B0, C0])
    b += _t(264, 314, 'A') + _t(380, 314, 'B') + _t(268, 39, 'C')
    b += _t(322, 322, '12') + _t(260, 178, '35') + _t(340, 176, '37')
    return _svg('A triangle with sides 12, 35 and 37', b)


def rn_fig_g091():
    O = (CX, CY)
    edges, a = [], 90.0
    for k in range(10):
        edges.append(a); a += 30.0 if k % 2 == 0 else 42.0
    b = _sector(edges[0], edges[2]) + _c(CX, CY, R)
    for e in edges: b += _l(O, _P(e), TEAL, 2)
    for k, e in enumerate(edges):
        w = 30.0 if k % 2 == 0 else 42.0
        b += _t(*_P(e + w / 2, 0.72 * R), s='α' if k % 2 == 0 else 'β', size=18, color=TEAL)
    b += _dot(O)
    return _svg('Five repeated pairs of central angles', b)


def rn_fig_g092():
    k, x0, y0 = 6.4, 259.2, 250.4
    A0, B0, C0 = (x0, y0), (x0 + 20 * k, y0), (x0, y0 - 21 * k)
    ra, rb, rc = 6 * k, 14 * k, 15 * k
    b = _c(A0[0], A0[1], ra) + _c(B0[0], B0[1], rb) + _c(C0[0], C0[1], rc) + _dot(A0) + _dot(B0) + _dot(C0)
    b += _t(A0[0] - 14, A0[1] + 14, 'A') + _t(B0[0] + 15, B0[1] + 15, 'B') + _t(C0[0] + 15, C0[1] - 15, 'C')
    b += ('<path d="M %.3f %.3f A %.3f %.3f 0 1 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="7"/>'
          % (A0[0], A0[1] - ra, ra, ra, A0[0] + ra, A0[1], TEAL))
    return _svg('Three mutually tangent circles', b)


def rn_fig_g098():
    ang = dict(A=0, G=20, F=56, E=100, D=170, B=215, C=290)
    P = {k: _P(v) for k, v in ang.items()}
    b = _c(CX, CY, R)
    for k, v in ang.items(): b += _lab(v, k)
    b += _dot((CX, CY)) + _t(305, 195, 'O')
    b += _l(P['B'], P['A']) + _l(P['B'], P['F']) + _l(P['C'], P['F']) + _l(P['C'], P['D'])
    b += _l((CX, CY), P['G']) + _l((CX, CY), P['E']) + _angle((CX, CY), P['G'], P['E'], 16, '80°', 32, size=16)
    b += _angle(P['B'], P['A'], P['F'], 34, '28°', 56) + _angle(P['C'], P['F'], P['D'], 29.2, '57°', 50)
    for u, w in (('A', 'G'), ('E', 'D')):
        b += ('<path d="M %.3f %.3f A %.1f %.1f 0 0 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="6"/>'
              % (P[u] + (R, R) + P[w] + (TEAL,)))
    return _svg('Two highlighted arcs determined by inscribed angles', b)


def rn_fig_p11():
    r, O = 75.0, (320.0, 262.0)
    B, C = _P(158, r, O), _P(22, r, O)
    Ap = (320.0, O[1] - r / math.cos(math.radians(68)))
    b = _c(O[0], O[1], r) + _poly([Ap, B, C]) + _l(O, B) + _l(O, C) + _dot(O)
    b += _t(O[0], O[1] + 20, 'O') + _t(Ap[0], Ap[1] - 16, 'A') + _t(B[0] - 20, B[1], 'B') + _t(C[0] + 20, C[1], 'C')
    b += _angle(B, Ap, C, 22, '?', 36)
    return _svg('Tangents and a chord from a common external point', b)


def rn_fig_p19():
    O = (CX, CY)
    b = _c(CX, CY, R) + _lab(90, 'A') + _lab(240, 'B') + _lab(330, 'C') + _dot(O) + _t(339, 172, 'O')
    b += _l(O, _P(90)) + _l(O, _P(240)) + _l(O, _P(330))
    b += _angle(O, _P(90), _P(240), 31, '150°', 54) + _right(O, _P(240), _P(330), 13)
    b += ('<path d="M %.3f %.3f A 109.500 109.500 0 0 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="6"/>'
          % (_P(330) + _P(90) + (TEAL,)))
    return _svg('The remaining arc after two central angles', b)


def rn_fig_p20():
    O = (CX, CY)
    b = _c(CX, CY, R) + _sector(270, 30) + _l(_P(90), _P(270)) + _l(O, _P(30)) + _dot(O)
    b += _lab(90, 'A') + _lab(270, 'B') + _lab(30, 'C') + _t(304, 180, 'O')
    b += _angle(O, _P(90), _P(30), 34, '60°', 56)
    return _svg('A shaded sector within a semicircle', b)


def rn_fig_adv_p07():
    b, x, y, u = '', 50.0, 250.0, 18.0
    for k in range(1, 6):
        r = k * u
        b += ('<path d="M %.3f %.3f A %.3f %.3f 0 0 1 %.3f %.3f" fill="none" stroke="%s" stroke-width="4"/>'
              % (x, y, r, r, x + 2 * r, y, TEAL)) + _l((x, y), (x + 2 * r, y))
        x += 2 * r
    return _svg('Five semicircular arcs placed end to end', b)


def rn_fig_adv_p09():
    O = (CX, CY)
    b = _sector(216, 324) + _angle(O, _P(216), _P(324), 32.85, '108°', 50)
    return _svg('A 108-degree sector', b)


def rn_fig_adv_p02():
    O = (CX, CY)
    b = _c(CX, CY, R) + _l(_P(180), _P(0)) + _l(_P(0), _P(210)) + _dot(O) + _t(320, 163, 'O')
    for k, a in dict(A=180, B=240, C=300, D=0, E=210).items(): b += _lab(a, k)
    return _svg('A semicircle divided into three equal arcs', b)


def rn_fig_adv_p12():
    O = (CX, CY)
    K0, L0, M0 = _P(180), _P(315), _P(45)
    b = _c(CX, CY, R) + _poly([K0, L0, M0]) + _dot(O) + _t(305, 195, 'O')
    b += _lab(180, 'K') + _lab(315, 'L') + _lab(45, 'M') + _angle(K0, L0, M0, 30, '45°', 50)
    return _svg('A chord cut off by a 45-degree inscribed angle', b)


def rn_fig_adv_p19():
    r, O = 70.0, (320.0, 225.0)
    s = math.sqrt(0.5)
    E = (O[0] + r * s, O[1] - r * s); F = (O[0] + r, O[1])
    xa, xb = O[0] - r, O[0] + r
    Dp = (xa, E[1] + (xa - E[0])); Cp = (xb, E[1] + (xb - E[0]))
    Ap, Bp = (xa, O[1] + r), (xb, O[1] + r)
    b = _sector(0, 45, r, O) + _c(O[0], O[1], r) + _poly([Ap, Bp, Cp, Dp]) + _l(O, E) + _l(O, F) + _dot(O)
    b += _t(Ap[0] - 16, Ap[1] + 15, 'A') + _t(Bp[0] + 16, Bp[1] + 15, 'B') + _t(Cp[0] + 17, Cp[1] - 4, 'C')
    b += _t(Dp[0] - 16, Dp[1] - 12, 'D') + _t(O[0] - 16, O[1] + 2, 'O') + _t(E[0] + 10, E[1] - 16, 'E')
    b += _t(F[0] + 16, F[1] + 2, 'F') + _angle(Dp, Ap, Cp, 24, '45°', 42)
    return _svg('A sector between the radii to two sides of a tangential trapezoid', b)


def rn_fig_adv_p15():
    # radii 2, 5, 6, 9: AB = 7, BC = 11, CD = 15, DA = 11, and B, D (and A, C) do not touch
    u = {'B': (0.0, 0.0), 'D': (16.0, 0.0)}
    ax = (49 - 121 + 256) / 32.0; u['A'] = (ax, -math.sqrt(49 - ax * ax))
    cx = (121 - 225 + 256) / 32.0; u['C'] = (cx, math.sqrt(121 - cx * cx))
    rad = dict(A=2, B=5, C=6, D=9)
    k = 11.5
    X = lambda p: (320 + k * (p[0] - 10), 180 + k * (p[1] - 3.45))
    b = ''
    for n in 'ABCD': b += _c(*X(u[n]), r=k * rad[n]) + _dot(X(u[n]))
    b += _poly([X(u[n]) for n in 'ABCD'], stroke=TEAL)
    off = dict(A=(0, -13), B=(-17, 0), C=(-4, 18), D=(17, 0))
    for n in 'ABCD':
        x, y = X(u[n]); b += _t(x + off[n][0], y + off[n][1], n)
    return _svg('Four circles tangent to their neighbors', b)


def rn_fig_adv_p20():
    kk, y0 = 8.2, 311.4
    Rr, rr = 16 * kk, 9 * kk
    A0 = (268.9, y0 - Rr); B0 = (A0[0] + 2 * math.sqrt(Rr * rr), y0 - rr)
    b = _c(A0[0], A0[1], Rr) + _c(B0[0], B0[1], rr) + _l((137.5, y0), (B0[0] + rr + 20, y0))
    b += _poly([A0, B0, (B0[0], y0), (A0[0], y0)], stroke=TEAL)
    b += _t(A0[0], A0[1] - 18, 'A') + _t(B0[0], B0[1] - 18, 'B') + _t(A0[0], y0 + 20, 'D') + _t(B0[0], y0 + 20, 'C')
    b += _t(A0[0] - 20, (A0[1] + y0) / 2, '16') + _t(B0[0] + 16, (B0[1] + y0) / 2, '9')
    return _svg('Two externally tangent circles sharing a horizontal tangent', b)


def _rn_stem(M, qid, *pairs):
    s = M.q(qid)['stemRich']
    for o, n in pairs:
        assert o in s, (qid, o)
        s = s.replace(o, n)
    return s


def rn_guided(M):
    F = lambda q: _rn_fig(M, q)

    # ---------- g076: AOC 112° -> 124°  ==>  AOC 104° -> 128° (trap 180 − 104 = 76; half the wrong arc 52)
    g = 'geo33-g076'
    _rn_q(M, g, _rn_stem(M, g, ('112°', '104°')), ['$52°$', '$128°$', '$76°$', '$104°$'], 2, [
        'B is on the minor arc AC. Stand at B between BA and BC: you see the major arc AC. Angle ABC rests on it.',
        'The central angle on the major arc: $360°-104°=256°$.',
        'The inscribed angle is half of it: $\\angle ABC=\\frac{256°}{2}=128°$.',
        'Check: a point D on the major arc makes ABCD an inscribed quadrilateral. $\\angle ADC=\\frac{104°}{2}=52°$, '
        'and $\\angle ABC=180°-52°=128°$. ($180°-104°=76°$ is the trap: AOCB is not an inscribed quadrilateral.)'],
        _rn_lbl(F(g), {'112°': '104°'}))
    _rn_video(M, 'solve-' + g, [('112', '104'), ('248', '256'), ('124', '128'), ('68', '76'), ('56', '52')],
              {1: 3, 2: 4, 3: 2, 4: 1})

    # ---------- g078: DPE 52° -> 64°  ==>  DPE 68° -> central 112° -> 56°
    g = 'geo33-g078'
    _rn_q(M, g, _rn_stem(M, g, ('52°', '68°')), ['$112°$', '$34°$', '$68°$', '$56°$'], 4, [
        'Draw the radii OD and OE. A radius to a point of tangency is perpendicular to the tangent: $\\angle ODP=\\angle OEP=90°$.',
        'The angles of quadrilateral ODPE add up to $360°$: $\\angle DOE=360°-90°-90°-68°=112°$.',
        'Angle DAE is an inscribed angle on the same minor arc DE: $\\angle DAE=\\frac{112°}{2}=56°$.'],
        _rn_lbl(F(g), {'52°': '68°'}))
    _rn_video(M, 'solve-' + g, [('52', '68'), ('128', '112'), ('64', '56'), ('26', '34')], {1: 3, 2: 1, 3: 4, 4: 2})

    # ---------- g080: area = 3 × circumference -> r = 6  ==>  4 × -> r = 8
    g = 'geo33-g080'
    _rn_q(M, g, _rn_stem(M, g, ('3 times', '4 times')), ['$8$', '$4$', '$16$', '$12$'], 1, [
        'Area $=4\\times$ circumference: $\\pi r^2=4\\cdot2\\pi r$.',
        'Divide by $\\pi$: $r^2=8r$. Divide by $r$ (a radius is not 0): $r=8$.',
        'Check: $S=\\pi\\cdot8^2=64\\pi$ and $C=2\\pi\\cdot8=16\\pi$, and $64\\pi=4\\cdot16\\pi$.'])
    _rn_video(M, 'solve-' + g, [('three times', 'four times'), ('3', '4'), ('6', '8'), ('36', '64'), ('12', '16')],
              {1: 4, 2: 3, 3: 1, 4: 2})

    # ---------- g082: r 6, arc 3π -> 90°  ==>  r 10, arc 4π -> 1/5 -> 72° (trap 144°: 4π out of πr = 10π)
    g = 'geo33-g082'
    _rn_q(M, g, _rn_stem(M, g, ('radius 6 cm', 'radius 10 cm'), ('$3\\pi$', '$4\\pi$')),
          ['$36°$', '$144°$', '$72°$', '$90°$'], 3, [
        'The whole circumference: $2\\pi\\cdot10=20\\pi$.',
        'The arc is $\\frac{4\\pi}{20\\pi}=\\frac15$ of the circle.',
        'So its central angle is $\\frac15$ of $360°$: $\\alpha=72°$.'], rn_fig_g082())
    _rn_video(M, 'solve-' + g, [('6', '10'), ('12', '20'), ('3', '4'), ('1/4', '1/5'), ('\\frac14', '\\frac15'),
                                ('a quarter', 'a fifth'), ('A quarter', 'A fifth'), ('90', '72')], {1: 1, 2: 2, 3: 4, 4: 3})

    # ---------- g083: r 6, 60° + 90° -> 15π  ==>  r 3, 40° + 120° -> 4/9 of 9π = 4π
    g = 'geo33-g083'
    _rn_q(M, g, _rn_stem(M, g, ('radius 6 cm', 'radius 3 cm'), ('60° and 90°', '40° and 120°')),
          ['$9\\pi$', '$\\frac{8\\pi}{3}$', '$4\\pi$', '$3\\pi$'], 3, [
        '$40°$ is $\\frac19$ of the circle and $120°$ is $\\frac13$: $\\frac19+\\frac13=\\frac19+\\frac39=\\frac49$.',
        'The area of the circle: $\\pi\\cdot3^2=9\\pi$.',
        'Shaded: $\\frac49\\cdot9\\pi=4\\pi$. (Or separately: $\\pi+3\\pi=4\\pi$.)'], rn_fig_g083())
    _rn_video(M, 'solve-' + g, slides={
        2: (None, [
            'A circle with center O, radius 3. Two shaded sectors: 40 degrees and 120 degrees. What is their total area?',
            "Here too I could plug into the formula. I'll save myself that — I have a 40 and a 120.",
            D('Write 1/3 in the 120° sector'),
            "120 degrees — we know that's a third.",
            D('Write 1/9 in the 40° sector'),
            '40 degrees — a ninth.',
            A('1/3 + 1/9 = 3/9 + 1/9 = 4/9 appears', _bt('$\\frac13+\\frac19=\\frac39+\\frac19=\\frac49$', 0)),
            'Together: a third plus a ninth. In ninths: 3 ninths plus 1 ninth — 4 ninths.',
            "So the shaded part is 4/9 of the circle's area."]),
        3: (None, [
            "Let's find the area of the circle.",
            A('πr² = π · 3² = 9π appears', _bt('$\\pi r^2=\\pi\\cdot3^2=9\\pi$', 0)),
            'π r squared — π times 3 squared, the radius is 3 — 9π.',
            "I don't need the whole circle. Only 4/9 of it.",
            A('4/9 · 9π = 4π appears', _bt('$\\frac49\\cdot9\\pi=4\\pi$', 1)),
            '9 divided by 9 is 1, times 4 — 4π.',
            D('Circle choice 3'),
            'Choice three.',
            'Or separately: a ninth of 9π is π, a third is 3π — 4π. Same thing.',
            'So once again: no formulas for arcs and sectors. Just see which part of the circle it is — it solves much faster.'])})

    # ---------- g085: AB = 12 -> 9√3  ==>  AB = 20 -> side 10 -> 25√3
    g = 'geo33-g085'
    _rn_q(M, g, _rn_stem(M, g, ('$AB=12$', '$AB=20$')), ['$10\\sqrt3$', '$50\\sqrt3$', '$25\\pi$', '$25\\sqrt3$'], 4, [
        'AB is a straight line: $\\angle BOC=180°-120°=60°$.',
        '$OB=OC$ (radii), so the base angles are equal: $\\frac{180°-60°}{2}=60°$ each. Triangle OBC is equilateral.',
        'Its side is a radius: $\\frac{20}{2}=10$.',
        'Area of an equilateral triangle: $\\frac{10^2\\sqrt3}{4}=\\frac{100\\sqrt3}{4}=25\\sqrt3$.'],
        _rn_lbl(F(g), {'12': '20'}))
    _rn_video(M, 'solve-' + g, [('12', '20'), ('6', '10'), ('36', '100'), ('9', '25')], {1: 4, 2: 1, 3: 2, 4: 3})

    # ---------- g086: A = 40° -> ABO 20°  ==>  A = 56° -> BOC 112°, OBC 34°, ABC 62°, ABO 28°
    g = 'geo33-g086'
    _rn_q(M, g, _rn_stem(M, g, ('40°', '56°')), ['$28°$', '$34°$', '$62°$', '$56°$'], 1, [
        'The central angle on arc BC: $\\angle BOC=2\\cdot56°=112°$.',
        'Triangle BOC is isosceles ($OB=OC$): $\\angle OBC=\\frac{180°-112°}{2}=34°$.',
        'Triangle ABC is isosceles ($AB=AC$): $\\angle ABC=\\frac{180°-56°}{2}=62°$.',
        '$\\angle ABO=62°-34°=28°$.',
        'Faster: the radius OA splits angle A in half, $\\frac{56°}{2}=28°$. Triangle AOB is isosceles ($OA=OB$), so '
        '$\\angle ABO=\\angle BAO=28°$.'], _rn_lbl(F(g), {'40°': '56°'}))
    _rn_video(M, 'solve-' + g, [('40', '56'), ('80', '112'), ('50', '34'), ('140', '124'), ('70', '62'), ('20', '28')],
              {1: 3, 2: 1, 3: 4, 4: 2})

    # ---------- g087: AO = 3 -> AC = 3√2 (not 3√3)  ==>  AO = 5 -> AC = 5√2 (not 5√3); same statement order
    g = 'geo33-g087'
    q = M.q(g)
    _rn_q(M, g, _rn_stem(M, g, ('AO=3\\text{ cm}', 'AO=5\\text{ cm}')),
          q['choicesRich'][:3] + ['$AC=5\\sqrt3$ cm'], 4, [
        'Angles DAE and CAD are inscribed angles on the equal chords DE and CD, so they are equal. Statement 1 is true.',
        'The four equal chords cut off four equal central angles. Together they make the straight angle AOE: $4x=180°$, '
        'so $x=45°$. Statement 2 is true.',
        'Angle ADE is an inscribed angle on the diameter AE: $90°$. Statement 3 is true.',
        'Triangle AOC: $AO=OC=5$ and $\\angle AOC=45°+45°=90°$. A 45°-45°-90° triangle: $AC=5\\sqrt2\\neq5\\sqrt3$. '
        'Statement 4 is not true.'], _rn_lbl(F(g), {'3': '5'}))
    assert q['choicesRich'][3] == '$AC=5\\sqrt3$ cm'
    _rn_video(M, 'solve-' + g, [('AO is 3.', 'AO is 5.'), ('OC = 3', 'OC = 5'), ('radius — 3', 'radius — 5'),
                                ('3 root', '5 root'), ('3\\sqrt', '5\\sqrt'), ('\\neq3', '\\neq5'), ('3√', '5√')])

    # ---------- g088: radius 4 (OM = 8)  ==>  radius 7 (OM = 14); still 120°, the key moves
    g = 'geo33-g088'
    _rn_q(M, g, _rn_stem(M, g, ('radius 4 cm', 'radius 7 cm')), ['$60°$', '$150°$', '$120°$', '$30°$'], 3, [
        'Radius to the point of tangency: $OA\\perp MA$ and $OB\\perp MB$.',
        'The circles are tangent, so the distance between the centers is the sum of the radii: $OM=7+7=14$.',
        'Right triangle OAM: the leg $OA=7$ is half of the hypotenuse $OM=14$. It is a 30°-60°-90° triangle: '
        '$\\angle AMO=30°$ and $\\angle AOM=60°$.',
        'By symmetry, $\\angle BOM=60°$ too: $\\angle AOB=60°+60°=120°$.'])
    _rn_video(M, 'solve-' + g, [('4', '7'), ('8', '14')], {1: 3, 2: 4, 3: 1, 4: 2})

    # ---------- g089: small C 8π, ring 65π -> 18π ≈ 56.5  ==>  small C 10π, ring 39π -> R 8 -> 16π ≈ 50.3
    g = 'geo33-g089'
    _rn_q(M, g, _rn_stem(M, g, ('$8\\pi$', '$10\\pi$'), ('$65\\pi$', '$39\\pi$')),
          ['48 and 49', '25 and 26', '64 and 65', '50 and 51'], 4, [
        'Small circle: $2\\pi r=10\\pi$, so $r=5$. Its area: $\\pi\\cdot5^2=25\\pi$.',
        'Large circle: $25\\pi+39\\pi=64\\pi$, so $R^2=64$ and $R=8$.',
        'Circumference: $2\\pi\\cdot8=16\\pi\\approx16\\cdot3.14=50.24$ — between 50 and 51. '
        '(48 and 49 comes from $\\pi\\approx3$: too rough here.)'])
    _rn_video(M, 'solve-' + g, [('8', '10'), ('4', '5'), ('16', '25'), ('65', '39'), ('81', '64'), ('9', '8'),
                                ('18', '16'), ('54', '48'), ('2.5', '2.2'), ('56.52', '50.24'),
                                ('56 and a half', '50 and a quarter'), ('56 and 57', '50 and 51')], {1: 3, 2: 4, 3: 1, 4: 2})

    # ---------- g090: sides 7, 24, 25 -> 25π  ==>  sides 12, 35, 37 -> 37π
    g = 'geo33-g090'
    _rn_q(M, g, _rn_stem(M, g, ('7 cm, 24 cm and 25 cm', '12 cm, 35 cm and 37 cm')),
          ['$74\\pi$', '$37\\pi$', '$18.5\\pi$', '$144\\pi$'], 2, [
        '$12^2+35^2=144+1225=1369=37^2$, so the triangle is a right triangle. The right angle is opposite the side 37.',
        'An inscribed right angle rests on a diameter. So the hypotenuse is a diameter of the circle: $d=37$.',
        '$C=\\pi d=37\\pi$.'], rn_fig_g090(), '200 20 230 330')
    _rn_video(M, 'solve-' + g, [('7', '12'), ('24', '35'), ('25', '37'), ('49', '144'), ('576', '1225'),
                                ('625', '1369'), ('12.5', '18.5')], {1: 4, 2: 1, 3: 2, 4: 3})

    # ---------- g091: radius √30, six of each -> 60° -> 5π  ==>  radius √35, five of each -> 72° -> 7π
    g = 'geo33-g091'
    _rn_q(M, g, _rn_stem(M, g, ('\\sqrt{30}', '\\sqrt{35}'), ('six of each', 'five of each')),
          ['$\\frac{7\\pi}{2}$', '$7\\pi$', '$14\\pi$', '$\\frac{35\\pi}{6}$'], 2, [
        'The ten angles make a full turn: $5\\alpha+5\\beta=360°$, so $\\alpha+\\beta=72°$.',
        'The two shaded sectors are $\\frac{72°}{360°}=\\frac15$ of the circle.',
        'The area of the circle: $\\pi(\\sqrt{35})^2=35\\pi$. Shaded: $\\frac15\\cdot35\\pi=7\\pi$.'], rn_fig_g091())
    _rn_video(M, 'solve-' + g, [('30', '35'), ('sixth', 'fifth'), ('six', 'five'), ('6', '5'), ('60', '72'),
                                ('5', '7'), ('20 and 40, could be 10 and 50', '30 and 42, could be 12 and 60')],
              {1: 4, 2: 1, 3: 2, 4: 3})

    # ---------- g092: radii 2, 4, 6 (6-8-10) -> 3π  ==>  radii 6, 14, 15 (20-21-29) -> ¾ of 12π = 9π
    g = 'geo33-g092'
    _rn_q(M, g, _rn_stem(M, g, ('2 cm, 4 cm and 6 cm', '6 cm, 14 cm and 15 cm')),
          ['$12\\pi$', '$8\\pi$', '$9\\pi$', '$6\\pi$'], 3, [
        'For tangent circles, the distance between the centers is the sum of the radii: $AB=6+14=20$, $AC=6+15=21$ '
        'and $BC=14+15=29$.',
        '$20^2+21^2=400+441=841=29^2$, so the angle at A is $90°$.',
        'The arc inside that angle is $\\frac14$ of circle A. The highlighted arc is the other $\\frac34$.',
        'Circumference of circle A: $2\\pi\\cdot6=12\\pi$. Highlighted arc: $\\frac34\\cdot12\\pi=9\\pi$.'],
        rn_fig_g092(), '150 10 340 340')
    _rn_video(M, 'solve-' + g, slides={
        2: (None, [
            'Three circles, centers A, B and C, all touching. Radii 6, 14 and 15. How long is the highlighted arc of circle A?',
            'An arc is a part of the circumference: the angle out of 360, times 2 pi r.',
            A('C_A = 2π · 6 = 12π appears', _bt('$C_A=2\\pi\\cdot6=12\\pi$', 1, 40)),
            "Circle A's radius is 6, so the whole circle is 12 pi."]),
        3: (None, [
            'Peek at the answers.',
            D('Cross out choice 1'),
            '12 pi — the whole circle. The arc must be less. Out.',
            D('Cross out choice 4'),
            "Sharp-eyed students cross out 6 pi too. That's exactly half — it needs an angle of 180 at A. But that angle "
            "is part of a triangle — less than 180.",
            'Choices two and three — no quick way to split them. We have to solve.',
            'Out of time? Guess one of them: a 50 percent chance instead of 25.']),
        4: ('A 20-21-29 triangle', [
            D("Write 6, 6 on circle A's radii; 14, 14 on B's; 15, 15 on C's"),
            'Put in the radii. Tangent circles — the distance between centers is the two radii together.',
            A('AB = 20 · AC = 21 · BC = 29 appears', _bt('$AB=6+14=20$, $AC=6+15=21$, $BC=14+15=29$', 1, 34)),
            '6 plus 14 — 20. 6 plus 15 — 21. 14 plus 15 — 29.',
            '20, 21, 29 — check Pythagoras: 400 plus 441 is 841. And 29 squared is 841. A Pythagorean triple.',
            D('Mark the right angle at A'),
            '29 is the hypotenuse — so the angle at A, opposite it, is 90.']),
        5: (None, [
            "The angle at A — the part we don't need — is 90. A quarter of the circle.",
            'So the highlighted arc is three quarters of the circumference.',
            A('L = ¾ × 12π = 9π appears', _bt('$L=\\frac34\\times12\\pi=9\\pi$', 1, 40)),
            'Three quarters of 12 pi — 9 pi.',
            D('Circle choice 3'),
            "Choice three. That's the end of the basic circle questions."])})

    # ---------- g094: radius 4 -> 16 − 4π  ==>  radius 6 -> AB 12, triangle 36, quarter circle 9π -> 36 − 9π
    g = 'geo33-g094'
    _rn_q(M, g, _rn_stem(M, g, ('radius 4 cm', 'radius 6 cm')),
          ['$18-9\\pi$', '$36-9\\pi$', '$18\\pi-18$', '$72-9\\pi$'], 2, [
        'Draw the radius OC to the point of tangency: $OC\\perp AB$ and $OC=6$.',
        'Triangle AOB is right and isosceles, so its height OC is also a median. Triangles AOC and BOC are '
        '45°-45°-90° triangles: $AC=CB=OC=6$, and $AB=12$.',
        'Triangle: $\\frac{12\\cdot6}{2}=36$. Sector ($90°$ is a quarter): $\\frac14\\cdot\\pi\\cdot6^2=9\\pi$.',
        'Shaded: $36-9\\pi$.'])
    _rn_video(M, 'solve-' + g, slides={
        2: (None, [
            "AB is tangent to a circle with center O, radius 6. OA equals OB, and angle AOB is 90. What's the shaded area?",
            'Shaded areas — we met them in quadrilaterals. The most common way to solve them: subtract areas.',
            "And it's one of the principles that keeps coming back in edge circle questions.",
            'So first — a scheme. What minus what gives the shaded part?',
            A('S shaded = S triangle AOB − S sector appears', _bt('$S_{\\text{shaded}}=S_{\\triangle AOB}-S_{\\text{sector}}$', 0, 34)),
            "If we know the area of triangle AOB, and the area of the sector inside it — subtract them. That's our scheme.",
            'Now the givens. OA equals OB, and the angle at O is 90.',
            D('Write 45° at A and at B'),
            "So AOB isn't just a right triangle — it's right AND isosceles. A silver triangle. The base angles: 45 each.",
            'AB is tangent. We learned an automatic construction: a point of tangency — draw a radius to it.',
            D('Draw OC to the point of tangency and mark the right angle at C'),
            'Call the point C. The radius is perpendicular to the tangent.',
            "AOB is isosceles, and OC is the altitude to its base — so it's also an angle bisector and a median.",
            D('Write 6 on OC, 6 on AC and 6 on CB'),
            'The radius is 6, so OC is 6. And OCB is a silver triangle too — so CB is 6, and AC is 6.']),
        3: (None, [
            'We have everything. Start with the triangle.',
            'The best way: base AB times the height, over 2.',
            'Plenty of students say: I have a hypotenuse in a silver triangle — find the legs, multiply, divide by 2.',
            "I ask — why? You already have a base and a height. Don't work for nothing — there's no time on the psychometric.",
            A('S triangle = 12 · 6 ÷ 2 = 36 appears', _bt('$S_{\\triangle}=\\frac{12\\cdot6}{2}=36$', 0)),
            'Base 12 times height 6, over 2 — 36.',
            'But wait. We can stop here and look at the answers. They often help.',
            'The shaded area must be 36 minus some sector — something with pi.',
            D('Cross out choice 3'),
            "18 pi minus 18? The pi is in the wrong place — that's circle minus triangle. Out, for sure.",
            D('Cross out choice 1'),
            '18 minus 9 pi — pi is in the right place, but the triangle is 36, not 18. Out.',
            D('Cross out choice 4'),
            '72 minus 9 pi — same argument. We need 36 minus something. Out.',
            D('Circle choice 2'),
            'Only 36 minus 9 pi is left. Choice two.',
            'We started with math and switched halfway to psychometric thinking. On the exam — mark it and move on.']),
        4: (None, [
            "We're in a lesson, so let's also calculate the sector.",
            A('Circle = π · 6² = 36π appears', _bt('$S_{\\circ}=\\pi\\cdot6^2=36\\pi$', 0)),
            'The whole circle: pi r squared — 36 pi.',
            'The sector is part of it — the part is set by the central angle. 90 degrees.',
            A('Sector = 90/360 · 36π = 9π appears', _bt('$S_{\\text{sector}}=\\frac{90}{360}\\cdot36\\pi=9\\pi$', 1)),
            'Some know by heart that 90 is a quarter — wonderful. If not: 90 over 360 — a quarter. A quarter of 36 pi — 9 pi.',
            A('36 − 9π appears', _bt('$36-9\\pi$', 2)),
            '36 minus 9 pi. The answer we found is really right.',
            D('Circle choice 2'),
            'Choice two.']),
        5: (None, [
            'One more approach — fully psychometric: estimating sizes.',
            "Maybe you plug in the givens and don't know how to go on. Maybe you run out of time — it's one of the last questions.",
            A('0 < shaded < 36 appears', _bt('$0<S_{\\text{shaded}}<36$', 0)),
            'What do we know? The triangle is 36. The shaded part is inside it — so less than 36.',
            'And by eye — even less than half. Now the answers.',
            D('Next to choice 1 write < 0'),
            '18 minus 9 pi — 9 pi is about 28, so this is negative. They do that a lot: hide a negative answer behind '
            "letters. An area can't be negative. Out.",
            D('Next to choice 3 write ≈ 38.5'),
            '18 pi — pi is 3.14, so 18 pi is about 56.5. Minus 18 — about 38.5. More than the whole triangle? Impossible. Out.',
            D('Next to choice 4 write ≈ 43.7'),
            '72 minus 9 pi — about 72 minus 28.3 — about 43.7. Too big. Out.',
            D('Next to choice 2 write ≈ 7.7'),
            "36 minus 9 pi — about 7.7. The only one possible — and by eye it's about a fifth of the triangle.",
            D('Circle choice 2'),
            'Choice two.',
            "Which approach? Up to you. Me — math, then shorten with partial calculation. It's safer.",
            'The problem with estimating: sometimes it rules out only one or two answers. But when there\'s no choice — '
            'a great card up your sleeve.'])})

    # ---------- g095: OE = EC = 12 -> 72√3 − 24π  ==>  OE = EC = 4 -> DC 4√3, triangle 8√3, sector 8π/3
    g = 'geo33-g095'
    _rn_q(M, g, _rn_stem(M, g, ('$OE=EC=12$', '$OE=EC=4$')),
          ['$8\\sqrt3-\\frac{4\\pi}{3}$', '$16\\sqrt3-\\frac{8\\pi}{3}$', '$8\\sqrt3-\\frac{8\\pi}{3}$',
           '$4\\sqrt3-\\frac{4\\pi}{3}$'], 3, [
        'OE is a radius: $OD=OE=4$, and $OC=4+4=8$.',
        'Draw the radius OD to the point of tangency: $OD\\perp AC$, so triangle ODC is a right triangle.',
        'The hypotenuse OC is twice the leg OD: a 30°-60°-90° triangle. $\\angle DOC=60°$ and $DC=4\\sqrt3$.',
        'Triangle ODC: $\\frac{4\\cdot4\\sqrt3}{2}=8\\sqrt3$. Sector DOE ($60°$ is a sixth): '
        '$\\frac16\\cdot\\pi\\cdot4^2=\\frac{16\\pi}{6}=\\frac{8\\pi}{3}$.',
        'Shaded: $8\\sqrt3-\\frac{8\\pi}{3}$.'], _rn_lbl(F(g).replace('>12</text>', '>4</text>', 1), {'12': '4'}))
    _rn_video(M, 'solve-' + g, slides={
        2: (None, [
            "ABC is a right triangle, tangent to the circle at B and D. OE and EC are both 4. What's the shaded area?",
            'Again shaded areas. We need a scheme: what minus what.',
            "The problem — here the scheme isn't trivial. The big triangle minus something? Triangle BDC minus something? Not clear.",
            'What do we do in these cases? Work with the givens, plug them in — and hope the solution shows itself.',
            "B is a point of tangency, and it's already marked 90 — the radius is perpendicular to the tangent.",
            "D is a point of tangency too. But careful: BD is NOT a radius, so there's no 90 there.",
            D('Draw the radius OD and mark the right angle at D'),
            'Draw a radius to the point of tangency and mark 90. The most basic construction there is.',
            D('Write 4 on OD'),
            'The radius is 4 — OE is a radius, so OD is 4 too.',
            A('S shaded = S triangle ODC − S sector appears', _bt('$S_{\\text{shaded}}=S_{\\triangle ODC}-S_{\\text{sector}}$', 0, 34)),
            "And now it's clear: the shaded area is triangle ODC minus the sector. Like the last question."]),
        3: (None, [
            'Triangle ODC: right angle at D. One leg, OD, is 4. The hypotenuse OC is 4 plus 4 — 8.',
            "We need the other leg, DC. Pythagoras? Probably... but there's no need.",
            'Spot the special triangle: the hypotenuse is exactly twice a leg. That only happens in a golden triangle.',
            D('Write 30° at C and 60° at O'),
            'Opposite the short leg — 30. Opposite DC — 60.',
            A('DC = 4√3 appears', _bt('$DC=4\\sqrt3$', 0)),
            'The long leg is root 3 times the short one: 4 root 3.',
            A('Triangle = 4 · 4√3 ÷ 2 = 8√3 appears', _bt('$S_{\\triangle}=\\frac{4\\cdot4\\sqrt3}{2}=8\\sqrt3$', 1)),
            'Leg times leg over 2: 8 root 3.',
            'Calculate the sector? We saw we can shorten — look for 8 root 3 minus something.',
            D('Cross out choices 2 and 4'),
            "Choices 2 and 4 don't have 8 root 3 — out.",
            "But here the trick doesn't finish the job: two answers start with 8 root 3.",
            "Some students start from the sector instead. Let's use both."]),
        4: (None, [
            'The sector: part of the circle. The whole circle — pi times 4 squared — 16 pi.',
            A('Sector = 60/360 · 16π = 8π/3 appears', _bt('$S_{\\text{sector}}=\\frac{60}{360}\\cdot16\\pi=\\frac{8\\pi}{3}$', 0)),
            'Which part? The angle at O is 60 — 60 out of 360 is a sixth. A sixth of 16 pi — 16 pi over 6. That is 8 pi over 3.',
            D('Cross out choice 1'),
            '8 root 3 minus 4 pi over 3 — that sector is only a twelfth of the circle. Wrong sector. Out.',
            A('8√3 − 8π/3 appears', _bt('$8\\sqrt3-\\frac{8\\pi}{3}$', 1)),
            'Only 8 root 3 minus 8 pi over 3 has both parts right.',
            D('Circle choice 3'),
            'Choice three.',
            'By the way — starting from the sector alone, 8 pi over 3 leaves two answers too. Together they settle it.'])})

    # ---------- g096: letters only (O, A, B -> K, M, N) and a new choice order; the answer stays (π + 2)/3
    g = 'geo33-g096'
    _rn_q(M, g, 'A semicircle has center K and radius r. M and N lie on its curved boundary, and angle KMN is 60°. '
                'What is the ratio of the perimeter of the semicircle to the perimeter of triangle KMN?',
          ['$\\frac{\\pi}{3}$', '$\\frac{\\pi+2}{3r}$', '$\\frac{\\pi+2}{3}$', '$\\frac{r(\\pi+2)}{3}$'], 3, [
        '$KM=KN=r$, so the base angles of triangle KMN are equal: both are $60°$. The triangle is equilateral, and its '
        'perimeter is $3r$.',
        'The perimeter of the semicircle is half the circumference plus the diameter: $\\pi r+2r=(\\pi+2)r$.',
        'Ratio: $\\frac{(\\pi+2)r}{3r}=\\frac{\\pi+2}{3}$.',
        'Check with $r=2$: $\\frac{2\\pi+4}{6}=\\frac{\\pi+2}{3}$. A ratio of two perimeters cannot contain r.'],
        _rn_lbl(F(g), {'O': 'K', 'A': 'M', 'B': 'N'}))
    _rn_video(M, 'solve-' + g, [('center O', 'center K'), ('Angle OAB', 'Angle KMN'), ('triangle AOB', 'triangle KMN'),
                                ('r on OA and on OB', 'r on KM and on KN'), ('OA and OB are radii', 'KM and KN are radii'),
                                ('at B and at O', 'at N and at K'), ('Angle A is 60, so B is 60', 'Angle M is 60, so N is 60'),
                                ('AB is r too', 'MN is r too')], {1: 3, 2: 1, 3: 4, 4: 2})

    # ---------- g097: letters only (ABCD -> KLMN, EFGH -> PQRS) and a new choice order; the answer stays 1/2
    g = 'geo33-g097'
    _rn_q(M, g, 'Square KLMN is circumscribed about a circle, and square PQRS is inscribed in the circle. '
                'What is the ratio of the area of PQRS to the area of KLMN?',
          ['$\\frac14$', '$\\frac12$', '$\\frac2\\pi$', '$\\frac1{\\sqrt2}$'], 2, [
        'Let the radius be r. The side of KLMN is a diameter, $2r$, so its area is $(2r)^2=4r^2$.',
        'The diagonal of PQRS is a diameter, $2r$. Area of a square from its diagonal: $\\frac{(2r)^2}{2}=2r^2$.',
        '$\\frac{2r^2}{4r^2}=\\frac12$.'],
        _rn_lbl(F(g), dict(zip('ABCDEFGH', 'KLMNPQRS'))))
    _rn_video(M, 'solve-' + g, [('ABCD', 'KLMN'), ('EFGH', 'PQRS'), ('— BC —', '— LM —')], {1: 4, 2: 3, 3: 2, 4: 1})

    # ---------- g098: r 9, 26°, 49°, GOE 90° -> 60° -> 3π  ==>  r 8, 28°, 57°, GOE 80° -> 170° − 80° = 90° -> 4π
    g = 'geo33-g098'
    _rn_q(M, g, _rn_stem(M, g, ('radius 9 cm', 'radius 8 cm'), ('26°', '28°'), ('49°', '57°'), ('GOE=90°', 'GOE=80°')),
          ['$8\\pi$', '$2\\pi$', '$4\\pi$', '$6\\pi$'], 3, [
        'Angle ABF is an inscribed angle on arc AF. The central angle is twice as big: $\\angle AOF=2\\cdot28°=56°$.',
        'Angle FCD is an inscribed angle on arc FD: $\\angle FOD=2\\cdot57°=114°$.',
        '$\\angle AOD=56°+114°=170°$. Take away the middle part: $\\angle AOG+\\angle EOD=170°-80°=90°$.',
        'The two arcs together are $\\frac{90°}{360°}=\\frac14$ of the circumference $2\\pi\\cdot8=16\\pi$: '
        '$\\frac14\\cdot16\\pi=4\\pi$.'], rn_fig_g098())
    _rn_video(M, 'solve-' + g, [('9', '8'), ('26', '28'), ('49', '57'), ('52', '56'), ('98', '114'), ('150', '170'),
                                ('90', '80'), ('60', '90'), ('18', '16'), ('3', '4'),
                                ('Maybe 30 and 30, maybe 20 and 40', 'Maybe 45 and 45, maybe 30 and 60'),
                                ('a sixth', 'a quarter'), ('A sixth', 'A quarter')], {1: 1, 2: 3, 3: 4, 4: 2})

    # ---------- g099: radius 4 -> 24π + 16  ==>  radius 6 -> square 36, sectors 27π each -> 54π + 36
    g = 'geo33-g099'
    _rn_q(M, g, _rn_stem(M, g, ('radius 4 cm', 'radius 6 cm')),
          ['$27\\pi+18$', '$54\\pi+18$', '$54\\pi+36$', '$27\\pi+36$'], 3, [
        'A minor arc that is a quarter of the circle has a central angle of $90°$: $\\angle AOB=\\angle APB=90°$.',
        '$OA=AP=PB=BO=6$, and the angles are $90°$: OAPB is a square with area $6^2=36$.',
        'Outside the square, each circle leaves a sector of $360°-90°=270°$, which is $\\frac34$ of the circle: '
        '$\\frac34\\cdot\\pi\\cdot6^2=27\\pi$.',
        'Union: $27\\pi+36+27\\pi=54\\pi+36$.'])
    _rn_video(M, 'solve-' + g, [('4 equal sides', '4 equal sides'), ('4', '6'), ('16', '36'), ('12', '27'), ('24', '54'),
                                ('8', '18')], {1: 3, 2: 2, 3: 1, 4: 4})

    # ---------- g100: radius 3 -> BC = 3π/2  ==>  radius 4 -> 8 · BC = 16π -> BC = 2π (< 8)
    g = 'geo33-g100'
    _rn_q(M, g, _rn_stem(M, g, ('radius 3 cm', 'radius 4 cm')), ['$3\\pi$', '$2\\pi$', '$8\\pi$', '$4\\pi$'], 2, [
        'The tangents AD and BC are parallel, so the distance between them is a diameter: $AB=2\\cdot4=8$.',
        'The area of the circle: $\\pi\\cdot4^2=16\\pi$.',
        '$8\\cdot BC=16\\pi$, so $BC=\\frac{16\\pi}{8}=2\\pi$.',
        'Size check: the circle is smaller than the square around it ($8\\cdot8=64$). So $8\\cdot BC<64$ and $BC<8$. '
        'Only $2\\pi\\approx6.3$ fits.'])
    _rn_video(M, 'solve-' + g, slides={
        2: (None, [
            "Radius 4. AD and BC are tangent to the circle at E and F. The rectangle's area equals the circle's area. What's BC?",
            D('Draw EF through O'),
            'The rectangle is tangent to the circle at E and F — so EF is a diameter.',
            D('Write 8 on AB'),
            "Radius 4, diameter 8. And the diameter equals the rectangle's height, AB.",
            A('8 · BC = π · 4² = 16π appears', _bt('$8\\cdot BC=\\pi\\cdot4^2=16\\pi$', 0)),
            'Rectangle area: AB times BC — 8 BC. It equals the circle: pi r squared — 16 pi.',
            A('BC = 16π ÷ 8 = 2π appears', _bt('$BC=\\frac{16\\pi}{8}=2\\pi$', 1)),
            'Isolate BC: divide by 8 — 2 pi.',
            D('Circle choice 2'),
            'Choice two. The math solution — honestly, not bad.']),
        3: (None, [
            'Now the psychometric way — estimating sizes.',
            A('8 · BC < 64 → BC < 8 appears', _bt('$8\\cdot BC<64\\ \\Rightarrow\\ BC<8$', 0)),
            'The circle fits inside an 8 by 8 square, so its area is less than 64. The rectangle has the same area: '
            '8 times BC is less than 64.',
            'So BC is less than 8. Now the answers.',
            D('Cross out choice 4'),
            '4 pi — 4 times 3-plus — 12-plus. Too big.',
            D('Cross out choice 3'),
            '8 pi — 24-plus. Way too big.',
            D('Cross out choice 1'),
            '3 pi — 9-plus. Just too big as well.',
            D('Circle choice 2'),
            'Three answers out — mark the fourth with certainty. No need to even calculate it: 2 pi is about 6.3. Choice two.'])})

    # ---------- g101: CB 6, ring 21π -> r = 2  ==>  CB 10, ring 65π -> R = r + 5, 10r + 25 = 65 -> r = 4
    g = 'geo33-g101'
    _rn_q(M, g, _rn_stem(M, g, ('$CB=6$', '$CB=10$'), ('$21\\pi$', '$65\\pi$')), ['$5$', '$4$', '$2$', '$3$'], 2, [
        'Let the small radius be r. Then $AC=2r$, and the large diameter is $AB=2r+10$. So $R=\\frac{2r+10}{2}=r+5$.',
        'Shaded: $\\pi(r+5)^2-\\pi r^2=65\\pi$.',
        'Divide by $\\pi$ and expand: $r^2+10r+25-r^2=65$, so $10r+25=65$ and $r=4$.',
        'Check: $R=9$, and $81\\pi-16\\pi=65\\pi$.'], _rn_lbl(F(g), {'6': '10'}))
    _rn_video(M, 'solve-' + g, slides={
        2: (None, [
            'A small circle inside a big one, tangent at A. AB and AC are diameters, CB is 10. The shaded area is 65 pi. '
            'The small radius?',
            'How do we calculate the shaded area? Big circle minus small circle.',
            A('πR² − πr² = 65π appears', _bt('$\\pi R^2-\\pi r^2=65\\pi$', 0)),
            'No radius is given. Call the big one R, the small one r.',
            'We need one unknown — write R with r. Easier than the other way round: adding is easier than subtracting.',
            D('Write r and r on AC, and 10 on CB'),
            'The big diameter AB is 2r plus 10.',
            A('R = (2r + 10) ÷ 2 = r + 5 appears', _bt('$R=\\frac{2r+10}{2}=r+5$', 1)),
            'The radius is half of that: r plus 5.',
            A('(r + 5)² − r² = 65 → 10r + 25 = 65 → r = 4 appears',
              _bt('$(r+5)^2-r^2=65$ $\\Rightarrow 10r+25=65 \\Rightarrow r=4$', 2, 32)),
            'Pi multiplies everything — divide it out. Open the brackets: r squared plus 10r plus 25, minus r squared. '
            'The squares cancel. 10r is 40 — r is 4.',
            D('Circle choice 2'),
            'Choice two.']),
        3: (None, [
            "Now the psychometric way: plugging in answers. They're all round numbers — easy to plug in.",
            'Where to start? From the middle.',
            "Why? Start from the smallest and it fails — every answer is bigger, you learned nothing. Start in the middle: "
            "if it's too big, go down; too small, go up. Two tries are always enough.",
            "Here the answers aren't in order: 5, 4, 2, 3. Order the values — 2, 3, 4, 5 — the middle values are 3 and 4.",
            A('r = 3: R = 8, 64π − 9π = 55π appears', _bt('$r=3$: $\\ R=8,\\ 64\\pi-9\\pi=55\\pi$', 0)),
            'Try 3. Small diameter 6, big diameter 6 plus 10 — 16, big radius 8. 64 pi minus 9 pi — 55 pi.',
            D('Cross out choices 3 and 4'),
            'Not 65 pi — too small. So 3 is out, and 2 is out too: we need a bigger radius.',
            A('r = 4: R = 9, 81π − 16π = 65π appears', _bt('$r=4$: $\\ R=9,\\ 81\\pi-16\\pi=65\\pi$', 1)),
            'Try 4. Small diameter 8, big diameter 18, big radius 9. 81 pi minus 16 pi — 65 pi. It fits!',
            D('Circle choice 2'),
            'Choice two. Solved two ways — pick the one that suits you.'])})

    # ---------- g102: angle A = 2α -> πr(1 − α/90)  ==>  angle A = 4θ (0 < θ < 45) -> πr(1 − θ/45); plug θ = 15
    g = 'geo33-g102'
    _rn_q(M, g, _rn_stem(M, g, ('2\\alpha', '4\\theta'), ('0<\\alpha<90', '0<\\theta<45')),
          ['$\\pi r\\left(1-\\frac{\\theta}{15}\\right)$', '$\\pi r\\left(1-\\frac{\\theta}{30}\\right)$',
           '$\\pi r\\left(1-\\frac{\\theta}{90}\\right)$', '$\\pi r\\left(1-\\frac{\\theta}{45}\\right)$'], 4, [
        'The base angles are equal: $\\angle ABC=\\frac{180°-4\\theta}{2}=90°-2\\theta$.',
        'Angle DBE is the same angle, and it is an inscribed angle on arc DE. The central angle is twice as big: '
        '$180°-4\\theta$.',
        'Arc: $\\frac{180-4\\theta}{360}\\cdot2\\pi r=\\frac{180-4\\theta}{180}\\cdot\\pi r=\\pi r\\left(1-\\frac{\\theta}{45}\\right)$.',
        'Check with $\\theta=15$ and $r=1$: the central angle is $120°$, and the arc is $\\frac13\\cdot2\\pi=\\frac{2\\pi}{3}$. '
        'Only $\\pi\\left(1-\\frac{15}{45}\\right)=\\frac{2\\pi}{3}$ fits.'], _rn_lbl(F(g), {'2α': '4θ'}))
    _rn_video(M, 'solve-' + g, slides={
        2: (None, [
            'ABC is isosceles, AB equals AC, the angle at A is 4 theta. B is on the circle, radius r. The length of the bold arc DE?',
            'An arc length — so first a central angle.',
            A('∠B = ∠C = (180° − 4θ) ÷ 2 = 90° − 2θ appears',
              _bt('$\\angle B=\\angle C=\\frac{180°-4\\theta}{2}=90°-2\\theta$', 0, 34)),
            "AB equals AC, so angle B equals angle C. Together they're 180 minus 4 theta.",
            'Each one is half of that: 90 minus 2 theta.',
            'Notice — angle B is an inscribed angle, resting on the bold arc. The central angle is twice as big.',
            A('central = 180° − 4θ appears', _bt('$\\text{central}=180°-4\\theta$', 1)),
            '180 minus 4 theta.',
            'Did you notice we divided by 2, then multiplied by 2? Spot that early, and you write 180 minus 4 theta straight away.']),
        3: (None, [
            'An arc is the part of the circumference set by the central angle, out of 360.',
            A('L = (180 − 4θ)/360 · 2πr appears', _bt('$L=\\frac{180-4\\theta}{360}\\cdot2\\pi r$', 0)),
            '180 minus 4 theta over 360, times 2 pi r.',
            'Lots of letters. Glance at the answers and continue smartly: they all have pi r in front — so shape ours like that.',
            A('= (180 − 4θ)/180 · πr appears', _bt('$=\\frac{180-4\\theta}{180}\\cdot\\pi r$', 1)),
            'Cancel the 2 against 360: 180 below.',
            'Every answer has a 1 in the bracket. Split the fraction: 180 over 180, minus 4 theta over 180.',
            A('= πr(1 − θ/45) appears', _bt('$=\\pi r\\left(1-\\frac{\\theta}{45}\\right)$', 2)),
            "4 over 180 is 1 over 45. That's 1 minus theta over 45.",
            D('Circle choice 4'),
            'Choice four. The math solution — it got tangled at the end with not-simple algebra.']),
        4: (None, [
            'Whenever there are unknowns, we can plug in a number — and turn it into a simpler question.',
            "Which value? A convenient special case. What's more convenient than 60 degrees?",
            D('Write 60° at A, B and C'),
            'Make the triangle equilateral: angle A is 60, so 4 theta is 60 — theta is 15. Each base angle is 60.',
            "The central angle is then 120. And r isn't given either — plug in 1.",
            A('θ = 15, r = 1: L = 120/360 · 2π = 2π/3 appears',
              _bt('$\\theta=15,\\ r=1$: $\\ L=\\frac{120}{360}\\cdot2\\pi=\\frac{2\\pi}{3}$', 0, 34)),
            'Circumference 2 pi. A third of it: 2 pi over 3.',
            "Now put theta 15 and r 1 into every answer — and rule out anything that isn't 2 pi over 3.",
            D('Cross out choice 1 (1 − 1 = 0)'),
            '15 over 15 is 1. 1 minus 1 — 0. Out.',
            D('Cross out choice 2 (π/2)'),
            '15 over 30 — a half. Pi over 2. Out.',
            D('Cross out choice 3 (5π/6)'),
            '15 over 90 — a sixth. 1 minus a sixth — 5 sixths pi. Out.',
            D('Circle choice 4'),
            '15 over 45 — a third. 1 minus a third — 2 thirds pi. It fits — and all three others are out. Choice four.',
            'Two solutions: full math — or psychometric, plugging in numbers.',
            'Next: a few more tools for the hardest circle questions.'])})


def rn_practice_questions(M):
    f = lambda n: 'geo33-foundation-p%02d' % n
    a = lambda n: 'geo33-advanced-p%02d' % n
    F = lambda q: _rn_fig(M, q)
    Q = _rn_q

    # ------------------------------------------------------------ foundation practice
    Q(M, f(1), 'A piece of string 18 cm long is laid out to form a circle, with no overlap. What is the radius of the '
               'circle (in cm)?', ['$9\\pi$', '$\\frac{18}\\pi$', '$\\frac9\\pi$', '$\\frac3\\pi$'], 3, [
        'The string becomes the whole circumference: $2\\pi r=18$.',
        '$r=\\frac{18}{2\\pi}=\\frac9\\pi$.'], _rn_lbl(F(f(1)), {'10 cm': '18 cm'}))
    Q(M, f(10), 'CD is a diameter of a circle with center O. OD is a diameter of a smaller circle whose circumference is '
                '$10\\pi$ cm. What is the circumference of the larger circle (in cm)?',
      ['$20\\pi$', '$40\\pi$', '$10\\pi$', '$30\\pi$'], 1, [
        'Small circle: $\\pi d=10\\pi$, so its diameter OD is 10.',
        'OD is a radius of the large circle: $R=10$.',
        'Large circumference: $2\\pi\\cdot10=20\\pi$.'], _rn_lbl(F(f(10)), {'A': 'C', 'B': 'D'}))
    Q(M, f(12), 'Two congruent circles with centers P and Q are externally tangent. The sum of their areas is $72\\pi$ cm². '
                'What is PQ (in cm)?', ['$6$', '$9$', '$12$', '$24$'], 3, [
        'Each circle: $\\frac{72\\pi}{2}=36\\pi$, so $r^2=36$ and $r=6$.',
        'For tangent circles, the distance between the centers is the sum of the radii: $PQ=6+6=12$.'],
      _rn_lbl(F(f(12)), {'A': 'P', 'B': 'Q'}))
    Q(M, f(2), 'The diameter of a smaller circle equals the radius of a larger circle and is 10 cm. The smaller circle lies '
               'entirely inside the larger circle. What is the area inside the larger circle but outside the smaller one '
               '(in cm²)?', ['$75\\pi$', '$50\\pi$', '$100\\pi$', '$25\\pi$'], 1, [
        'The large radius is 10, and the small radius is $\\frac{10}2=5$.',
        'Areas: $\\pi\\cdot10^2=100\\pi$ and $\\pi\\cdot5^2=25\\pi$.',
        '$100\\pi-25\\pi=75\\pi$.'])
    Q(M, 'wp26-p10', 'A robot cleans 480 m² per hour on a hard floor. On carpet its rate is halved. How many hours does it '
                     'need to clean a circular carpet of radius 12 meters?',
      ['$\\frac{3\\pi}{10}$', '$\\frac{5\\pi}{3}$', '$\\frac{3\\pi}{5}$', '$\\frac{\\pi}{5}$'], 3, [
        'On carpet the rate is $480\\div2=240$ m² per hour.',
        'The carpet area is $\\pi\\cdot12^2=144\\pi$ m². Time $=$ work $\\div$ rate $=\\frac{144\\pi}{240}=\\frac{3\\pi}{5}$ hours.'])
    Q(M, f(6), 'AB and CD are diameters of a circle with center O. Given: angle COB is $4\\alpha$, angle BOD is $\\alpha$, '
               'and angle DOA is $\\beta$. What is $\\beta$?', ['$108°$', '$135°$', '$154°$', '$144°$'], 4, [
        'COB and BOD make the straight angle COD: $4\\alpha+\\alpha=180°$, so $\\alpha=36°$.',
        'BOD and DOA make the straight angle BOA: $36°+\\beta=180°$, so $\\beta=144°$.'],
      _rn_lbl(F(f(6)), {'5α': '4α'}))
    Q(M, f(14), 'In the accompanying figure, $\\varphi$ is a central angle and $\\theta$ is an inscribed angle intercepting '
                'the same arc. What is $5\\theta-2\\varphi$?', ['$\\theta$', '$0$', '$\\varphi$', '$3\\theta$'], 1, [
        'On the same arc, the central angle is twice the inscribed angle: $\\varphi=2\\theta$.',
        '$5\\theta-2\\varphi=5\\theta-4\\theta=\\theta$.'], _rn_lbl(F(f(14)), {'α': 'φ', 'β': 'θ'}))
    Q(M, f(7), 'Triangle ABC is inscribed in a circle, and angle BAC is 40°. What fraction of the circumference is the '
               'major arc BC, which contains A?', ['$\\frac19$', '$\\frac29$', '$\\frac79$', '$\\frac89$'], 3, [
        'The minor arc BC has the central angle $2\\cdot40°=80°$. That is $\\frac{80}{360}=\\frac29$ of the circle.',
        'The major arc BC is the rest: $1-\\frac29=\\frac79$.'], _rn_lbl(F(f(7)), {'36°': '40°'}))
    Q(M, 'wp27-p10', 'A cyclist and a walker leave the same point on a circular path at the same time, in opposite '
                     'directions. The cyclist is eight times as fast as the walker. At their first meeting, what central '
                     'angle corresponds to the arc traveled by the walker?', ['45°', '36°', '40°', '80°'], 3, [
        'At their first meeting, together they have covered one full circle.',
        'Equal times: their distances are in the same ratio as their speeds, $1:8$. The circle is $1+8=9$ parts, and '
        'the walker covers $1$ part: $\\frac19$ of the circle.',
        'Central angle: $\\frac{360°}{9}=40°$.'])
    Q(M, f(19), 'A circle with center O has radius 6 cm. Three radii divide it into sectors of 150°, 90°, and a third '
                'angle. What is the length of the arc belonging to the third sector (in cm)?',
      ['$5\\pi$', '$4\\pi$', '$12\\pi$', '$2\\pi$'], 2, [
        'The third angle: $360°-150°-90°=120°$. That is $\\frac{120}{360}=\\frac13$ of the circle.',
        'Circumference: $2\\pi\\cdot6=12\\pi$. Arc: $\\frac13\\cdot12\\pi=4\\pi$.'], rn_fig_p19())
    Q(M, f(20), 'A circle with center O has area $36\\pi$ cm². AB is a diameter and angle AOC is 60°. What is the area of '
                'sector COB contained in the same semicircle as C (in cm²)?',
      ['$6\\pi$', '$18\\pi$', '$12\\pi$', '$24\\pi$'], 3, [
        '$\\angle COB=180°-60°=120°$. That is $\\frac{120}{360}=\\frac13$ of the circle.',
        'Sector: $\\frac13\\cdot36\\pi=12\\pi$.'], rn_fig_p20())
    Q(M, f(18), 'AD and BC are diameters of two externally tangent circles. ABCD is a square with perimeter 36 cm. What is '
                'the sum of the circumferences of the circles (in cm)?', ['$18\\pi$', '$36\\pi$', '$81\\pi$', '$9\\pi$'], 1, [
        'Side of the square: $\\frac{36}{4}=9$. AD and BC are sides, so each diameter is 9.',
        'Each circumference: $\\pi\\cdot9=9\\pi$. Sum: $9\\pi+9\\pi=18\\pi$.'])
    Q(M, f(17), 'AB is tangent at T to a circle with center O and radius 6 cm. The area of triangle AOB is 54 cm². What is '
                'AB (in cm)?', ['$9$', '$12$', '$18$', '$27$'], 3, [
        'OT is a radius to the point of tangency: $OT\\perp AB$. So OT is the height of triangle AOB: 6.',
        '$\\frac{AB\\cdot6}{2}=54$, so $AB=18$.'])
    Q(M, f(5), 'Triangle ABC is inscribed in a circle of area $49\\pi$ cm². Given: $AC=14$ cm. What is angle ABC?',
      ['$60°$', '$90°$', '$45°$', '$75°$'], 2, [
        '$\\pi r^2=49\\pi$, so $r=7$ and the diameter is 14.',
        'No chord is longer than the diameter. A chord of length 14 is a diameter: AC is a diameter.',
        'An inscribed angle on a diameter is $90°$: $\\angle ABC=90°$.'], _rn_lbl(F(f(5)), {'8': '14'}))
    Q(M, f(4), 'KL is a diameter of a circle with center O. M and N lie on the same semicircle in the order L, M, N, K. '
               'Given: angle LKM equals angle MKN. Which of the following statements is necessarily true?',
      ['$KM=KN$', '$\\angle KML=45°$', '$LM=MN$', '$\\angle LOM=2\\angle MON$'], 3, [
        'Equal inscribed angles intercept equal arcs: arc LM $=$ arc MN.',
        'Equal arcs have equal chords: $LM=MN$.',
        'The other statements depend on where M and N are, so they are not necessarily true.'],
      _rn_lbl(F(f(4)), {'A': 'K', 'B': 'L', 'C': 'M', 'D': 'N'}))
    Q(M, f(3), 'In the accompanying figure, AD is a diameter of a circle with center O, $AB\\parallel CD$, and angle COD is '
               '128°. What is angle BAD?', ['$52°$', '$26°$', '$13°$', '$38°$'], 2, [
        '$OC=OD$ (radii), so $\\angle ODC=\\frac{180°-128°}{2}=26°$.',
        '$AB\\parallel CD$, and AD crosses both. Alternate angles are equal: $\\angle BAD=\\angle ADC=26°$.'],
      _rn_lbl(F(f(3)), {'140°': '128°'}))
    Q(M, f(8), 'A, B, C and D lie on a circle with center O. C is on the arc BD that does not contain A. Given: angle BAD '
               'is $3\\alpha$ and angle COD is $2\\beta$. What is angle BOC?',
      ['$3\\alpha-2\\beta$', '$6\\alpha-2\\beta$', '$6\\alpha+2\\beta$', '$2\\beta-3\\alpha$'], 2, [
        'Angle BAD intercepts arc BCD. The central angle is twice as big: $\\angle BOD=2\\cdot3\\alpha=6\\alpha$.',
        '$\\angle BOD=\\angle BOC+\\angle COD$, so $\\angle BOC=6\\alpha-2\\beta$.'],
      _rn_lbl(F(f(8)), {'2α': '3α', '3β': '2β'}))
    Q(M, f(9), 'Circles with centers K and M intersect at A and B. MA is tangent to the circle with center K at A, and KB '
               'is tangent to the circle with center M at B. Given: $\\angle AMB=64°$. What is angle AKB?',
      ['$116°$', '$64°$', '$90°$', '$128°$'], 1, [
        'Radius to the point of tangency: $KA\\perp MA$ and $MB\\perp KB$, so $\\angle KAM=\\angle KBM=90°$.',
        'The angles of quadrilateral KAMB add up to $360°$: $\\angle AKB=360°-90°-90°-64°=116°$.'],
      _rn_lbl(F(f(9)), {'72°': '64°'}))
    Q(M, f(11), 'AB and AC are tangent to a circle with center O at B and C. The smaller central angle BOC is 136°. What is '
                'angle ABC?', ['$22°$', '$44°$', '$68°$', '$34°$'], 3, [
        'Triangle BOC is isosceles ($OB=OC$): $\\angle OBC=\\frac{180°-136°}{2}=22°$.',
        'The radius OB is perpendicular to the tangent BA: $\\angle OBA=90°$.',
        '$\\angle ABC=90°-22°=68°$.'], rn_fig_p11())
    Q(M, f(13), 'ABC is an isosceles triangle. Given:\n$\\begin{cases} AB=AC \\\\ \\angle BCA=64° \\end{cases}$\n'
                'A circle with center O is tangent to AB and AC at D and E. What is the smaller angle DOE?',
      ['$52°$', '$116°$', '$128°$', '$64°$'], 3, [
        '$AB=AC$, so the base angles are equal: $\\angle A=180°-2\\cdot64°=52°$.',
        'Radii to the points of tangency: $\\angle ADO=\\angle AEO=90°$.',
        'The angles of quadrilateral ADOE add up to $360°$: $\\angle DOE=360°-90°-90°-52°=128°$.'],
      _rn_lbl(F(f(13)), {'56°': '64°'}))
    Q(M, f(16), M.q(f(16))['stemRich'],
      ['An isosceles trapezoid with upper base angles of 112°', 'A rectangle with sides 5 cm and 36 cm',
       'A deltoid whose two unequal opposite angles are 90° and 84°', 'A regular polygon with 13 sides'], 3, [
        'A quadrilateral can be inscribed in a circle only if its opposite angles add up to $180°$.',
        'The deltoid: $90°+84°=174°\\neq180°$. It cannot be inscribed.',
        'The trapezoid ($112°+68°=180°$), the rectangle and a regular polygon can all be inscribed.'])
    Q(M, f(15), 'Quadrilateral ABCD is inscribed in a circle of area $64\\pi$ cm². Diagonal AC bisects both angle A and '
                'angle C. What is AC (in cm)?', ['$8\\sqrt2$', '$8$', '$16$', '$12$'], 3, [
        'Write the angles at A and C as $2\\alpha$ and $2\\beta$. Opposite angles of an inscribed quadrilateral: '
        '$2\\alpha+2\\beta=180°$, so $\\alpha+\\beta=90°$.',
        'In triangle ABC: $\\angle B=180°-\\alpha-\\beta=90°$. An inscribed right angle rests on a diameter: AC is a diameter.',
        '$\\pi r^2=64\\pi$, so $r=8$ and $AC=2\\cdot8=16$.'])

    # ------------------------------------------------------------ advanced practice
    Q(M, a(1), 'Four equal arcs of a circle have a combined length equal to $\\frac49$ of its circumference. What is the '
               'central angle subtending one of these arcs?', ['$45°$', '$80°$', '$40°$', '$160°$'], 3, [
        'The four equal arcs are $\\frac49$ of the circle, so one arc is $\\frac49\\div4=\\frac19$ of the circle.',
        'Its central angle: $\\frac19\\cdot360°=40°$.'])
    Q(M, a(7), 'Five semicircular arcs have radii whose average is k. What is the sum of the lengths of the five curved arcs?',
      ['$10\\pi k$', '$5\\pi k^2$', '$5\\pi k$', '$2.5\\pi k$'], 3, [
        'A semicircular arc with radius r has length $\\frac{2\\pi r}{2}=\\pi r$.',
        'The five radii add up to $5k$ (their average is k). So the five arcs add up to $\\pi\\cdot5k=5\\pi k$.'],
      rn_fig_adv_p07())
    Q(M, a(9), 'A sector has central angle 108°. Its area, measured in cm², is numerically 5 times as much as its arc '
               'length, measured in cm. What is the radius of its circle (in cm)?', ['$5$', '$20$', '$10$', '$2.5$'], 3, [
        'Let f be the fraction of the circle: $f=\\frac{108}{360}$.',
        'Sector area $=f\\cdot\\pi r^2$ and arc $=f\\cdot2\\pi r$: $f\\pi r^2=5\\cdot f\\cdot2\\pi r$.',
        'Divide by $f\\pi r$: $r=10$. (The angle does not matter.)'], rn_fig_adv_p09())
    Q(M, a(8), 'A circular lake has radius 400 m. A walkway 100 m wide is built around its entire shore. What is the area '
               'of the walkway (in km²)?', ['$0.25\\pi$', '$0.09\\pi$', '$0.01\\pi$', '$0.16\\pi$'], 2, [
        'Same units first: the inner radius is $400$ m $=0.4$ km, and the outer radius is $400+100=500$ m $=0.5$ km.',
        'Walkway $=$ big circle $-$ small circle: $\\pi\\cdot0.5^2-\\pi\\cdot0.4^2=\\pi(0.25-0.16)=0.09\\pi$ km².'])
    Q(M, a(2), 'AD is a diameter of a circle with center O. B and C divide one semicircular arc AD into three equal arcs, '
               'and E is the midpoint of arc AB. What is angle ADE?', ['$30°$', '$7.5°$', '$15°$', '$60°$'], 3, [
        'Three equal arcs on a semicircle: $\\frac{180°}{3}=60°$ each.',
        'E is the midpoint of arc AB, so arc AE is $\\frac{60°}{2}=30°$.',
        'Angle ADE is an inscribed angle intercepting arc AE: $\\frac{30°}{2}=15°$.'], rn_fig_adv_p02())
    Q(M, a(12), 'Triangle KLM is inscribed in a circle with center O and radius r. Given: angle LKM is 45°. What is LM?',
      ['$r$', '$2r$', '$r\\sqrt2$', '$\\frac{r\\sqrt3}{2}$'], 3, [
        'The central angle on arc LM: $\\angle LOM=2\\cdot45°=90°$.',
        'Triangle LOM is right and isosceles with legs $OL=OM=r$: $LM=r\\sqrt2$.'], rn_fig_adv_p12())
    Q(M, a(13), 'AB is a diameter of a circle with radius 8 cm. C lies on one semicircular arc AB. Arc CB is twice as long '
                'as arc AC. What is BC (in cm)?', ['$8$', '$8\\sqrt3$', '$8\\sqrt2$', '$16$'], 2, [
        'Arc CB is twice arc AC, and together they make the semicircle: arc AC $=60°$ and arc CB $=120°$.',
        'Inscribed angles: $\\angle ABC=30°$, $\\angle BAC=60°$, and $\\angle ACB=90°$ (on the diameter).',
        'A 30°-60°-90° triangle with hypotenuse $AB=16$: $AC=8$ and $BC=8\\sqrt3$.'])
    Q(M, a(3), 'A circle with center O has radius 8 cm. OACD is a square, C lies on the circle, and ray OA meets the '
               'circle at B. What is AB (in cm)?', ['$8-4\\sqrt3$', '$4$', '$8-4\\sqrt2$', '$8-\\sqrt2$'], 3, [
        'OC is a radius (8), and it is also the diagonal of the square OACD.',
        'Side of a square from its diagonal: $OA=\\frac{8}{\\sqrt2}=4\\sqrt2$.',
        '$OB=8$, so $AB=OB-OA=8-4\\sqrt2$.'])
    Q(M, a(10), 'A semicircle is drawn inside a square of side 8 cm, with one side of the square as its diameter. Between '
                'which two values is the area inside the square but outside the semicircle (in cm²)?',
      ['25 and 26', '39 and 40', '38 and 39', '13 and 14'], 3, [
        'Square: $8^2=64$. Semicircle with radius 4: $\\frac{\\pi\\cdot4^2}{2}=8\\pi$.',
        '$64-8\\pi\\approx64-25.13=38.87$: between 38 and 39.'])
    Q(M, a(14), 'Each side of triangle ABC is longer than 8 cm. A sector of radius 4 cm is drawn at each vertex, bounded by '
                'the two sides meeting there. The three sectors lie entirely inside the triangle and do not overlap. What is '
                'the sum of the areas of the three sectors (in cm²)?',
      ['$4\\pi$', '$8\\pi$', '$16\\pi$', '$\\frac{16\\pi}{3}$'], 2, [
        'The three sector angles are the angles of the triangle: together $180°$.',
        'With the same radius 4, the three sectors make half a circle: $\\frac12\\cdot\\pi\\cdot4^2=8\\pi$.'])
    Q(M, a(16), 'Three circles of radius 9 cm have centers A, B and C, with $AB=BC=CA=9$ cm. What is the perimeter of their '
                'common region (in cm)?', ['$27\\pi$', '$18\\pi$', '$9\\pi$', '$3\\pi$'], 3, [
        'Each side of triangle ABC is 9, the radius: the triangle is equilateral, and each angle is $60°$.',
        'The common region is bounded by three $60°$ arcs. Each is $\\frac16$ of the circumference $2\\pi\\cdot9=18\\pi$: $3\\pi$.',
        'Perimeter: $3\\cdot3\\pi=9\\pi$.'])
    Q(M, a(4), 'Three concentric circles have radii $x$, $3y$ and $4z$, where $0<x<3y<4z$. The smallest circle and the '
               'region outside the middle circle but inside the largest circle are shaded. What is the total shaded area?',
      ['$\\pi(16z^2-9y^2+x^2)$', '$\\pi(4z-3y+x)^2$', '$\\pi(16z^2+9y^2-x^2)$', '$\\pi(16z^2-9y^2-x^2)$'], 1, [
        'The smallest circle: $\\pi x^2$.',
        'The outer ring: $\\pi(4z)^2-\\pi(3y)^2=16\\pi z^2-9\\pi y^2$.',
        'Total: $\\pi(16z^2-9y^2+x^2)$.'], _rn_lbl(F(a(4)), {'a': 'x', '2b': '3y', '3c': '4z'}))
    Q(M, a(5), 'A, B, C and D lie on a circle. Given: angle CAD is 46°, angle CDB is 20°, and angle ADB equals angle ABD. '
               'What is angle ABD?', ['$47°$', '$57°$', '$46°$', '$67°$'], 2, [
        'Angles ABD and ACD intercept the same arc AD, so $\\angle ACD=\\angle ABD=\\alpha$. Also $\\angle ADB=\\alpha$.',
        '$\\angle ADC=\\angle ADB+\\angle BDC=\\alpha+20°$.',
        'Triangle ACD: $46°+\\alpha+(\\alpha+20°)=180°$, so $2\\alpha=114°$ and $\\alpha=57°$.'],
      _rn_lbl(F(a(5)), {'44°': '46°', '24°': '20°'}))
    Q(M, a(6), 'BD and CE are diameters of a circle with center O. Given: angle ACE is $3m$ and angle EOD is $2n$. A and E '
               'lie on the arc AD that does not contain B, in the order A, E, D. What is angle ABD?',
      ['$180°-3m-2n$', '$3m+2n$', '$3m+n$', '$\\frac{3m}{2}+n$'], 3, [
        'Angle ACE is an inscribed angle intercepting arc AE, so the arc is $2\\cdot3m=6m$.',
        'Arc ED has the central angle EOD: $2n$.',
        'Arc AD: $6m+2n$. Angle ABD is an inscribed angle on it: $\\frac{6m+2n}{2}=3m+n$.'],
      _rn_lbl(F(a(6)), {'2p': '3m', '3q': '2n'}))
    Q(M, a(11), 'BD and EC are diameters of a circle with center O. A lies on the minor arc EB, and arcs EA and AB are equal. '
                'Given: angle ECA is $2k$. What is angle DAC?', ['$2k$', '$4k$', '$90°-2k$', '$180°-4k$'], 2, [
        'Angle ECA is an inscribed angle intercepting arc EA, so the arc is $2\\cdot2k=4k$. Arc AB is equal: $4k$.',
        'Central angle EOB: $4k+4k=8k$. The vertical angle DOC is also $8k$.',
        'Angle DAC is an inscribed angle intercepting arc DC: $\\frac{8k}{2}=4k$.'], _rn_lbl(F(a(11)), {'3t': '2k'}))
    Q(M, a(17), 'Square ABCD is inscribed in a circle with circumference $20\\pi$ cm. E, F, G and H are the midpoints of its '
                'sides. What is the area of square EFGH (in cm²)?', ['$50$', '$100\\sqrt2$', '$100$', '$200$'], 3, [
        'Diameter: $\\frac{20\\pi}{\\pi}=20$. It is the diagonal of ABCD: area $\\frac{20^2}{2}=200$.',
        'The square of the midpoints has half the area: $\\frac{200}{2}=100$.'])
    Q(M, a(18), 'A circle with center O has radius 10 cm. A and E lie on the circle, angle AOE is 45°, and B is the foot of '
                'the perpendicular from A to OE. What is the area of sector AOE outside triangle AOB (in cm²)?',
      ['$25\\pi-50$', '$\\frac{25\\pi}{2}-25$', '$\\frac{25\\pi}{2}-50$', '$25-\\frac{25\\pi}{2}$'], 2, [
        'The $45°$ sector is $\\frac18$ of the circle: $\\frac18\\cdot\\pi\\cdot10^2=\\frac{100\\pi}{8}=\\frac{25\\pi}{2}$.',
        'Triangle AOB is right and isosceles, with hypotenuse $OA=10$: legs $\\frac{10}{\\sqrt2}=5\\sqrt2$, area '
        '$\\frac{5\\sqrt2\\cdot5\\sqrt2}{2}=25$.',
        'Sector outside the triangle: $\\frac{25\\pi}{2}-25$.'])
    Q(M, a(19), 'ABCD is a trapezoid with $AD\\parallel BC$, circumscribed about a circle with center O and radius 8 cm. The '
                'circle is tangent to CD at E and to BC at F. Given: angle ADC is 45°. What is the area of the minor sector '
                'EOF (in cm²)?', ['$16\\pi$', '$8\\pi$', '$24\\pi$', '$32\\pi$'], 2, [
        '$AD\\parallel BC$, so the two angles on the leg CD add up to $180°$: $\\angle BCD=180°-45°=135°$.',
        'Radii to the points of tangency: $OE\\perp CD$ and $OF\\perp BC$. In quadrilateral OECF: '
        '$\\angle EOF=360°-90°-90°-135°=45°$.',
        'Sector: $\\frac18\\cdot\\pi\\cdot8^2=8\\pi$.'], rn_fig_adv_p19())
    Q(M, a(15), 'Four circles have centers A, B, C and D. Each circle is externally tangent to its two neighbors, in the '
                'order A, B, C, D, A. Given:\n$\\begin{cases} AB=7\\text{ cm} \\\\ BC=11\\text{ cm} \\\\ CD=15\\text{ cm} '
                '\\end{cases}$\nWhat is AD (in cm)?', ['$11$', '$9$', '$13$', '$15$'], 1, [
        'Call the radii a, b, c and d. For tangent circles, the distance between the centers is the sum of the radii.',
        '$AB+CD=(a+b)+(c+d)$ and $BC+AD=(b+c)+(a+d)$: both are the sum of all four radii.',
        '$7+15=11+AD$, so $AD=11$.'], rn_fig_adv_p15())
    Q(M, a(20), 'Two externally tangent circles with centers A and B have radii 16 cm and 9 cm. A common tangent touches them '
                'at D and C, respectively. What is the perimeter of quadrilateral ABCD (in cm)?',
      ['$56$', '$74$', '$75$', '$49$'], 2, [
        'Tangent circles: $AB=16+9=25$. The radii AD and BC are perpendicular to the tangent DC, so ABCD is a right trapezoid.',
        'Draw BE parallel to DC (E on AD): $AE=16-9=7$ and $BE=DC$.',
        'Right triangle ABE: $DC=\\sqrt{25^2-7^2}=\\sqrt{576}=24$.',
        'Perimeter: $25+9+24+16=74$.'], rn_fig_adv_p20())


def rn_practice(M):
    """Approved clean-up (63 -> 49): the three copies, the English extras beyond three warm-ups, and the September items
    whose type is already practised (or that copy a video board)."""
    out = ['geo33-foundation-p25',   # copy: ring between concentric circles (= p02 / guided g089 type)
           'q-r26-t33-14',           # copy: radius −10% -> area (= p24 / guided q-r26-t33-03)
           'geo33-advanced-p26',     # copy: circle in a right triangle 6-8-10 (= guided q-r26-t33-02)
           'q-r26-t33-06',           # area ×9 -> circumference ×3: the board line "Backwards: S×9 ⇒ r×3" of q-03's video
           'q-r26-t33-12',           # chord 8 in radius 5: same type as q-11 and guided q-01
           'geo33-foundation-p24',   # extra: scaling (guided q-03)
           'geo33-foundation-p26',   # extra: inscribed quadrilateral algebra (p15, p16 practise the rule)
           'geo33-foundation-p23',   # extra: tangent + Pythagoras (p17, adv-p20)
           'geo33-foundation-p27',   # extra: same as p23
           'geo33-foundation-p22',   # extra: chord at a distance (q-11, guided q-01)
           'geo33-advanced-p25',     # extra: rectangle in a circle (guided g090, p15)
           'geo33-advanced-p21',     # extra: chord of a ring (q-10)
           'geo33-advanced-p24',     # extra: ring and difference of squares (q-10, p02)
           'geo33-advanced-p23']     # extra: gap between three circles (adv-p16)
    for qid in out:
        assert M.section_of(qid) in (FOUND, ADVP), qid
        M.unplace(qid)


def rn_lessons_cards(M):
    # ---- Angles in a Circle: the Hebrew lesson example 70° / 110°
    _rn_video(M, 'geo-075', [('70', '75'), ('110', '105')])
    # ---- Sectors and Arcs, "Fifths": the Hebrew example (a circle of 25π -> 5π)
    _rn_video(M, 'geo-081', [('25π', '40π'), ('25\\pi', '40\\pi'), ('5π', '8π'), ('=5\\pi', '=8\\pi')])
    # ---- summaries: the Hebrew "4α + 4β" (= the old g091) and "radius 5, distance 3" (= q-r26-t33-12 / q-11)
    _rn_video(M, 'r26-t33-summary', [('r = 5, d = 3 → half chord 4 → chord 8', 'r = 17, d = 8 → half chord 15 → chord 30'),
                                     ('Radius 5, distance 3: half the chord is 4. The whole chord — 8.',
                                      'Radius 17, distance 8: half the chord is 15. The whole chord — 30.')])
    _rn_video(M, 'r26-t33-summary-2', [('4α + 4β = 360° → α + β = 90°', '3α + 3β = 360° → α + β = 120°'),
                                       ('Four α and four β make a full turn: α plus β is 90.',
                                        'Three α and three β make a full turn: α plus β is 120.')])
    # ---- card: two examples were questions (guided q-r26-t33-04 and practice adv-p27)
    c = M.card('mem-r26-t33-more-tools')
    rows = c['tables'][0]['rows']
    new = {'!Segment': 'radius 12, \\(60°\\): \\(24\\pi-36\\sqrt3\\)',
           "Two equal circles, each through the other's center": 'radius 6: \\(24\\pi-18\\sqrt3\\)'}
    for r in rows:
        if r[0] in new: r[2] = new.pop(r[0])
    assert not new, new


def renumber_pass(M):
    rn_guided(M)
    rn_practice_questions(M)
    rn_practice(M)
    rn_lessons_cards(M)
    _sync_canvas(M)


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
    # Q19 (semicircle perimeter : triangle perimeter): power count (topic 5) cuts the two choices with r
    _sp_line(M, 'geo33-g096', r'Method 2 · Power count: a perimeter has power 1, so perimeter $\div$ perimeter has power $1-1=0$. Choice 2, $\frac{\pi+2}{3r}$, has power $-1$, and choice 4, $\frac{r(\pi+2)}{3}$, has power $1$: both are out. Choice 1 leaves out the diameter $2r$ of the semicircle: choice 3.',
             drop=' A ratio of two perimeters cannot contain r.')
    _sp_say_after(M, 'solve-geo33-g096', 4, 'But if we enlarge or shrink the whole figure',
                  "That's the power count from algebra: a perimeter has power 1, so perimeter over perimeter has power 1 minus 1 — zero. No r can stay.")
    # advanced practice (five semicircular arcs, average radius k): all radii k -> pick values that fit; tie -> powers
    _sp_line(M, 'geo33-advanced-p07', r'Shortcut · Pick values that fit: only the average is given, so take all five radii equal to $k$. Each arc is $\pi k$, and five arcs are $5\pi k$. Tie? Check the powers (power count): with $k=1$, $5\pi k^2$ is $5\pi$ too, but a length has power 1, and $5\pi k^2$ has power 2 — out.')
    # advanced practice (ring between concentric circles, tangent chord 16): radii free -> pick values that fit
    _sp_line(M, 'q-r26-t33-10', r'Shortcut · Pick values that fit: the radii are not given, and the question expects one answer, so any pair that fits will do. Take the small radius $6$: half the chord is $8$, so $R=10$ ($6, 8, 10$). Ring: $100\pi-36\pi=64\pi$.')
    # advanced practice (four tangent circles): one radius free -> pick values that fit
    _sp_line(M, 'geo33-advanced-p15', r'Shortcut · Pick values that fit: only the distances are given, so choose one radius and the rest follow. $a=1$: $b=7-1=6$, $c=11-6=5$, $d=15-5=10$. $AD=a+d=1+10=11$.')
    # foundation practice (equal inscribed angles at K): one figure that fits knocks out three choices
    _sp_line(M, 'geo33-foundation-p04', r'Shortcut · Pick values that fit: draw one figure that fits — arcs $LM=MN=30°$, so arc $NK=120°$. Then $\angle LOM=30°$ but $2\angle MON=60°$ (choice 4 out), chord KM (on an arc of $150°$) is longer than KN (on $120°$) (choice 1 out), and $\angle KML=90°$, an angle on the diameter (choice 2 out). Choice 3 is left.')


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
    # Topic 33 (days 1-5) comes before topic 5 (power count, day 13) in the plan.
    _po_line(M, 'geo33-g096', 'Method 2 · Power count:', "Shortcut · Power count: count the lengths multiplied in each expression — $r$ is one length (power $1$), a plain number has power $0$, and dividing subtracts. Enlarging the whole figure cannot change a ratio of two perimeters, so the answer has power $1-1=0$: no $r$ can stay. Choice 2, $\\frac{\\pi+2}{3r}$, has power $-1$, and choice 4, $\\frac{r(\\pi+2)}{3}$, has power $1$: both are out. Choice 1 leaves out the diameter $2r$ of the semicircle: choice 3.")
    _po_line(M, 'geo33-advanced-p07', 'Shortcut · Pick values that fit:', "Shortcut · Pick values that fit: only the average is given, so take all five radii equal to $k$. Each arc is $\\pi k$, and five arcs are $5\\pi k$. Tie? Count the lengths multiplied: with $k=1$, $5\\pi k^2$ is $5\\pi$ too, but $k^2$ is a length times a length (an area), and a total arc length is one length — out.")
    v = 'solve-geo33-g096'   # not recorded
    _po_say(M, v, 4, "That's the power count from algebra: a perimeter has power 1, so perimeter over perimeter has power 1 minus 1 — zero. No r can stay.",
            "Count the lengths: a perimeter is one length, so perimeter over perimeter is one length over one length — they cancel. No r can stay.")


_apply_before_plan_order_fix = apply


def apply(M):
    _apply_before_plan_order_fix(M)
    plan_order_fix(M)   # 2026-10-07 study-plan order: runs last


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
    # solve-geo33-g094 · Estimate the size: 3 < π < 4 instead of 56.5 / 43.7 / 7.7
    v = 'solve-geo33-g094'
    if not _nd_recorded(v):
        _nd_lines(M, v, 'Estimate the size', [
            ('draw', 'Next to choice 1 write < 0', 'Next to choice 1 write "9π > 27 → < 0"'),
            ('say', "18 minus 9 pi — 9 pi is about 28, so this is negative. They do that a lot: hide a negative answer behind letters. An area can't be negative. Out.",
             "18 minus 9 pi — pi is more than 3, so 9 pi is more than 27. This is negative. They do that a lot: hide a negative answer behind letters. An area can't be negative. Out."),
            ('draw', 'Next to choice 3 write ≈ 38.5', 'Next to choice 3 write "18π > 54 → > 36"'),
            ('say', "18 pi — pi is 3.14, so 18 pi is about 56.5. Minus 18 — about 38.5. More than the whole triangle? Impossible. Out.",
             "18 pi minus 18 — 18 pi is more than 54. Minus 18 — still more than 36. More than the whole triangle? Impossible. Out."),
            ('draw', 'Next to choice 4 write ≈ 43.7', 'Next to choice 4 write "9π < 36 → > 36"'),
            ('say', "72 minus 9 pi — about 72 minus 28.3 — about 43.7. Too big. Out.",
             "72 minus 9 pi — pi is less than 4, so 9 pi is less than 36. 72 minus less than 36 — more than 36. Too big. Out."),
            ('draw', 'Next to choice 2 write ≈ 7.7', 'Next to choice 2 write "27 < 9π < 36 → between 0 and 9"'),
            ('say', "36 minus 9 pi — about 7.7. The only one possible — and by eye it's about a fifth of the triangle.",
             "36 minus 9 pi — 9 pi is between 27 and 36, so this is between 0 and 9. The only one possible — and by eye it's a small piece of the triangle."),
        ])
    # solve-geo33-g096 · Method 3: the board no longer shows 5.14 / 3 ≈ 1.7 (the spoken lines already say "5-plus over 3")
    v = 'solve-geo33-g096'
    if not _nd_recorded(v):
        _nd_item(M, v, 'Method 3 · Estimate', r'$\frac{\pi+2}{3}\approx\frac{5.14}{3}\approx1.7$',
                 r'$\pi>3\;\Rightarrow\;\frac{\pi+2}{3}>\frac{5}{3}$', label='π > 3 → (π+2)/3 > 5/3 appears')
    # solve-geo33-g100 · Method 2: "2π is about 6.3" -> 6-plus, under 8
    v = 'solve-geo33-g100'
    if not _nd_recorded(v):
        _nd_lines(M, v, 'Method 2 · Estimate', [
            ('say', "Three answers out — mark the fourth with certainty. No need to even calculate it: 2 pi is about 6.3. Choice two.",
             "Three answers out — mark the fourth with certainty. No need to even calculate it: 2 pi is 6-plus — under 8. Choice two.")])
    _nd_expl(M, 'geo33-g100', [(3, 'Size check:',
             'Size check: the circle is smaller than the square around it ($8\\cdot8=64$). So $8\\cdot BC<64$ and $BC<8$. '
             '$3\\pi$, $4\\pi$ and $8\\pi$ are all more than $9$. Only $2\\pi$ (less than $2\\cdot3.5=7$) fits.')])
    # q-r26-t33-04 · the negative trap: 3π < 12 < √243 = 9√3 instead of 9.4 and 15.6
    v = 'solve-q-r26-t33-04'
    if not _nd_recorded(v):
        _nd_lines(M, v, 'The traps', [
            ('draw', 'Next to choice 4 write "3π ≈ 9.4 < 9√3 ≈ 15.6"', 'Next to choice 4 write "3π < 12 < √243 = 9√3"'),
            ('say', "3π minus 9 root 3 is negative. An area can't be negative.",
             ["3π is less than 12. And 9 root 3 is root 243 — more than root 144, which is 12.",
              "So 3π minus 9 root 3 is negative. An area can't be negative."])])
    _nd_expl(M, 'q-r26-t33-04', [(3, 'Segment:',
             'Segment: $6\\pi-9\\sqrt3$. ($3\\pi-9\\sqrt3$ is negative: $3\\pi<3\\cdot4=12$, and $9\\sqrt3=\\sqrt{81\\cdot3}=\\sqrt{243}>\\sqrt{144}=12$.)')])
    # r26-t33-summary-2 · Numbers and estimates: π between 3 and 3.5, not 3.14
    v = 'r26-t33-summary-2'
    if not _nd_recorded(v):
        _nd_item(M, v, 'Numbers and estimates', r'Estimate: $\pi\approx3.14$, a circle $<$ the square around it',
                 r'Estimate: $3<\pi<3.5$, a circle $<$ the square around it')
    # geo-079 · π is a number: the exam fact is 3 < π < 3.5
    v = 'geo-079'
    if not _nd_recorded(v):
        _nd_lines(M, v, 'π is a number', [
            ('say', "All we need to know about π: it's a bit more than 3.",
             "All we need to know about π: it's more than 3 and less than three and a half.")])


_apply_before_no_decimal_estimates = apply


def apply(M):
    _apply_before_no_decimal_estimates(M)
    no_decimal_estimates(M)   # 2026-10-07 no decimal estimates: runs last


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
    _mn_load().method_names(M, 33)   # 2026-10-07 method names: runs last


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


def coverage_fixes(M):
    # #127: with plugged-in numbers, one fitting answer is not enough - say WHY all four are checked
    vid = 'solve-geo33-g102'
    _cf_add(M, vid, M.slide(vid, 4)['title'], 'into every answer — and rule out anything', [
        "Even if one fits early — don't mark it yet. A special case can fit more than one answer, so we check all four."])


_apply_before_coverage_fixes = apply


def apply(M):
    _apply_before_coverage_fixes(M)
    coverage_fixes(M)   # 2026-10-08 coverage fixes: runs LAST


# =====================================================================================
# 2026-10-09 AI auto-narrate pilot (studio_autonarrate.py): POINT cues — the AI video points at / highlights what the
# voice talks about (the shaded sectors, the α / β labels, the left side of the equation, the fraction). The TeX parts
# are marked with \hl{name}{...} (renders exactly as before). A video with a take recorded before AI_CUTOFF (UTC) is
# left exactly as recorded.
AI_CUTOFF = '2026-10-09T07-10-00'


def _ai_recorded(vid):
    pat = _re_cf.compile(_re_cf.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _glob_cf.glob(_os_cf.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_os_cf.path.basename(f))
        if m and m.group(1) < AI_CUTOFF: return True
    return False


def ai_pointers(M):
    from dsl import PT
    vid = 'solve-geo33-g091'
    if _ai_recorded(vid): return

    def slide(title):
        return M.video(vid)['beats'][CF.n_of(M, vid, title) - 1]

    def item(b, k, old, new):
        assert b['items'][k]['t'] == old, (vid, b['title'], b['items'][k]['t'])
        b['items'][k]['t'] = new

    def before(b, start, *cues):
        k = [i for i, l in enumerate(b['lines']) if (l.get('say') or '').startswith(start)]
        assert len(k) == 1, (vid, b['title'], start, k)
        b['lines'][k[0]:k[0]] = [dict(c[1]) for c in cues]

    b = slide('The whole circle')
    # pilot v2 (teacher: "'Here is a sample question' should be taken off", "you didn't read out the question")
    # (it sits on the 'Question N' title slide here; the build's no_question_numbers moves it to the first slide)
    k = [(x, i) for x in M.video(vid)['beats'] for i, l in enumerate(x['lines']) if l.get('say') == 'A sample question — medium-plus.']
    assert len(k) == 1, (vid, 'sample-question line', k)
    k[0][0]['lines'][k[0][1]] = {'say': 'Read the question aloud: radius root 35, central angles α, β in turn, five of each. '
                               'One α sector and one β sector are shaded — their total area?'}
    before(b, 'Radius root 35.', PT('fig: shaded', 'the two shaded sectors', at=0.58))
    b = slide('The sum α + β')
    item(b, 1, '$5\\alpha+5\\beta=360°$', '$\\hl{left}{5\\alpha+5\\beta}=360°$')
    before(b, 'Count them:', PT('fig: α', 'the five alphas', at=0.15), PT('fig: β', 'the five betas', at=0.5))
    before(b, 'One equation, two unknowns', PT('item 1: left', 'the left side: 5α + 5β', at=0.0, style='both'))
    b = slide('A fifth of the circle')
    item(b, 1, '$\\frac{72°}{360°}\\times35\\pi=7\\pi$', '$\\hl{frac}{\\frac{72°}{360°}}\\times35\\pi=7\\pi$')
    before(b, 'Together the two sectors', PT('item 1: frac', '72 out of 360', at=0.38))
    M.touched_videos.add(vid)


_apply_before_ai_pointers = apply


def apply(M):
    _apply_before_ai_pointers(M)
    ai_pointers(M)   # 2026-10-09 AI auto-narrate pilot: runs LAST


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
    _sl_load().spoken_labels(M, 33)   # 2026-10-09 spoken labels: runs LAST
