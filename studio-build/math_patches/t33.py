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
    _american(M)
    _sync_canvas(M)


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
    # Equal chords: a figure, no SSS proof (not taught in T31)
    M.set_slide('geo-075', 8, script=[
        "One more fact that we'll use later.",
        A('Two equal chords AB and CD with the radii to their ends appear', VIS(fig_equal_chords(), w=1000, h=520)),
        "Two equal chords in the same circle. Join the ends of each chord to the center O.",
        D('Mark the equal central angles at O'),
        "Equal chords make equal central angles — and cut off equal arcs.",
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
            A('Around a circle: AB + CD = BC + AD',
              T('Quadrilateral around a circle: $AB+CD=BC+AD$', size=34, x=1110, y=560, w=420)),
            "The same idea works for a quadrilateral around a circle: the two pairs of opposite sides have the same sum.",
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
    # Q2: no cultural reference
    M.set_slide('solve-geo33-g078', 2, title='Automatic: draw the radii')
    _say(M, 'solve-geo33-g078', 2, "Always, automatically. It should be Pavlov — anyone who doesn't know who Pavlov is, look him up.",
         "Always, automatically — every time.")
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
        ['Quadrilateral around a circle', '\\(AB+CD=BC+AD\\)'],
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
    # near-duplicates: "tangents -> quadrilateral 360°" (Q2, p09, p13) and "ring = big - small" (Q10, p25, adv-p08)
    for q in ['geo33-foundation-p09', 'geo33-foundation-p13', 'geo33-foundation-p25', 'geo33-advanced-p08']:
        M.unplace(q)

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
    P[7] = (ADVP, 'Quadrilateral ABCD is drawn around a circle: all four sides are tangent to the circle. Given:\n'
                  '$\\begin{cases} AB=7\\text{ cm} \\\\ BC=9\\text{ cm} \\\\ CD=12\\text{ cm} \\end{cases}$\nWhat is AD (in cm)?',
            ['$14$', '$10$', '$16$', '$4$'], 2, [
                'Tangent pieces from each vertex are equal. Call them a, b, c and d (from A, B, C and D).',
                '$AB+CD=(a+b)+(c+d)$ and $BC+AD=(b+c)+(d+a)$ — both are $a+b+c+d$.',
                '$7+12=9+AD$, so $AD=10$.'], None)
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
    P[12] = (ADVP, 'Two circles with radii 3 cm and 5 cm meet at exactly two points. Which of the following cannot be '
                   'the distance between their centers (in cm)?',
             ['$3$', '$5$', '$7$', '$8$'], 4, [
                 'At $5+3=8$ the circles touch from outside at one point only. Farther apart, they do not meet at all.',
                 'At $5-3=2$ the small circle touches the big one from inside. Closer, they do not meet.',
                 'Two points: the distance is between 2 and 8. 3, 5 and 7 are possible; 8 is not.'], None)
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
        f(1), f(10), f(12), f(2), g[5], f(24), f(6), f(14), f(26), f(7), f(21), f(19), f(20), f(18), f(17), f(23),
        f(27), g[6], f(22), f(5), f(4), f(3), f(8), f(11), f(16), f(15)])
    M.practice_order(ADVP, [
        a(1), a(7), a(9), a(22), a(2), a(12), a(13), a(3), a(10), a(14), a(25), g[7], a(26), a(16), a(4), a(5), a(6),
        a(11), a(17), a(18), a(21), g[10], g[11], g[12], g[13], a(24), g[9], a(19), a(15), g[8], a(20), a(23), a(27)])
