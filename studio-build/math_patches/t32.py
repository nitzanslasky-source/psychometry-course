"""Topic 32 - Quadrilaterals. Course review 2026-09 fixes.
See t32_CHANGES.md for the plain-language list."""
import math, re
from dsl import T, H, A, D, Q
from math_api import VIS, _word

TOPIC = 32
LEARN1, FOUND, LEARN2, ADVP = 'geo32-learn-1', 'geo32-foundation-practice', 'geo32-learn-2', 'geo32-advanced-practice'
GID = ['q-r26-t32-%02d' % k for k in range(1, 8)]      # guided questions
PID = ['q-r26-t32-%02d' % k for k in range(8, 22)]     # practice questions

# ------------------------------------------------------------------------------------------------
# Figures - same style as the existing geometry figures (ink #203344, teal #087f83, fill #d5f1ed,
# orange #bb6821, DejaVu Sans 20, labels 20 / angle labels 18)
# ------------------------------------------------------------------------------------------------
INK, TEAL, FILL, ORANGE, OFILL = '#203344', '#087f83', '#d5f1ed', '#bb6821', '#ffefdc'


def _svg(label, body, vb='0 0 640 360'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, label, label, body))


def _t(x, y, s, size=20, color=INK, italic=False, bold=False):
    return ('<text x="%.3f" y="%.3f" text-anchor="middle" dominant-baseline="middle" fill="%s" '
            'font-family="DejaVu Sans,Arial,sans-serif" font-size="%d"%s%s>%s</text>'
            % (x, y, color, size, ' font-style="italic"' if italic else '', ' font-weight="bold"' if bold else '', s))


def _poly(pts, fill='none', stroke=INK, w=2.5):
    p = ' '.join('%.3f,%.3f' % xy for xy in pts)
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (p, fill, stroke, w)


def _line(p, q, color=INK, w=2.5, dash=False):
    return ('<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="%s"%s/>'
            % (p[0], p[1], q[0], q[1], color, w, ' stroke-dasharray="7 5"' if dash else ''))


def _path(pts, color=INK, w=2.5):
    d = 'M ' + ' L '.join('%.3f %.3f' % xy for xy in pts)
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (d, color, w)


def _dir(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def _pt(c, r, a):
    return (c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))


def _arc(c, r, a1, a2, color=TEAL):
    """Arc around c from screen angle a1 to a2 (degrees, a2 > a1, clockwise on screen)."""
    p, q = _pt(c, r, a1), _pt(c, r, a2)
    return ('<path d="M %.3f %.3f A %.3f %.3f 0 %d 1 %.3f %.3f" fill="none" stroke="%s" stroke-width="2"/>'
            % (p[0], p[1], r, r, 1 if a2 - a1 > 180 else 0, q[0], q[1], color))


def _angle(c, p, q, text, r=28, dist=None, color=TEAL, size=18):
    """Mark the (smaller, < 180 degrees) angle at c between rays c->p and c->q."""
    a1, a2 = _dir(c, p), _dir(c, q)
    while a2 <= a1: a2 += 360
    if a2 - a1 > 180: a1, a2 = a2 - 360, a1
    m = (a1 + a2) / 2
    lx, ly = _pt(c, dist or r + 20, m)
    return _arc(c, r, a1, a2, color) + (_t(lx, ly, text, size=size, color=color) if text else '')


def _right(c, p, q, s=13, color=INK):
    """Right-angle mark at c between rays c->p and c->q."""
    def u(a, b):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); return ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
    u1, u2 = u(c, p), u(c, q)
    a = (c[0] + s * u1[0], c[1] + s * u1[1]); b = (a[0] + s * u2[0], a[1] + s * u2[1]); d = (c[0] + s * u2[0], c[1] + s * u2[1])
    return _path([a, b, d], color, 1.7)


def _lab(p, dx, dy, s, **k):
    return _t(p[0] + dx, p[1] + dy, s, **k)


def _mid(p, q, t=0.5):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _cross(p1, p2, p3, p4):
    """Intersection of line p1p2 with line p3p4."""
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    a = x1 * y2 - y1 * x2; b = x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / d, (a * (y3 - y4) - (y1 - y2) * b) / d)


def _abcd(A_, B_, C_, D_, off):
    """Vertex labels A, B, C, D with offsets off = [(dx, dy)] * 4."""
    return ''.join(_lab(p, o[0], o[1], n) for p, o, n in zip((A_, B_, C_, D_), off, 'ABCD'))


# --- general quadrilateral (lesson slides 2 and 4): irregular, no parallel or equal sides ---
_QA, _QB, _QC, _QD = (212, 88), (128, 236), (446, 290), (470, 108)
FIG_QUAD = _svg('A general quadrilateral ABCD', _poly([_QA, _QB, _QC, _QD]) +
                _abcd(_QA, _QB, _QC, _QD, [(-12, -16), (-16, 10), (8, 18), (16, -10)]), vb='100.2 54.1 398.6 257.8')

# --- concave quadrilateral (lesson slide 3): same as before, B label moved off the side ---
_KA, _KB, _KC, _KD = (191.176, 94.118), (191.176, 265.882), (448.824, 265.882), (285.647, 192.882)
FIG_CONCAVE = _svg('A concave quadrilateral', _poly([_KA, _KB, _KC, _KD]) +
                   _lab(_KA, 0, -17, 'A') + _lab(_KB, -16, 12, 'B') + _lab(_KC, 16, 12, 'C') + _lab(_KD, 4, -20, 'D'),
                   vb='159.2 51.1 321.6 240.8')

# --- the arrow rule (lesson): angles a, b, c inside, x in the notch at D ---
FIG_ARROW = _svg('A concave quadrilateral with the angle x in the notch at D',
                 _poly([_KA, _KB, _KC, _KD]) +
                 _angle(_KA, _KD, _KB, 'a', r=30) + _right(_KB, _KC, _KA, color=TEAL) + _t(_KB[0] + 30, _KB[1] - 30, 'b', size=18, color=TEAL) +
                 _angle(_KC, _KB, _KD, 'c', r=48, dist=76) + _angle(_KD, _KC, _KA, 'x', r=24, dist=44, color=ORANGE, size=20) +
                 _lab(_KA, 0, -17, 'A') + _lab(_KB, -16, 12, 'B') + _lab(_KC, 16, 12, 'C') + _lab(_KD, -2, 24, 'D'),
                 vb='150 55 330 240')


# --- family tree (lesson) ---
def _box(x, y, s, w):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="40" rx="10" fill="%s" stroke="%s" stroke-width="2"/>'
            % (x - w / 2, y - 20, w, FILL, TEAL) + _t(x, y, s, size=19))


def _arrow(p, q, color=INK):
    a = math.atan2(q[1] - p[1], q[0] - p[0]); L = 11
    h1 = (q[0] - L * math.cos(a - 0.4), q[1] - L * math.sin(a - 0.4))
    h2 = (q[0] - L * math.cos(a + 0.4), q[1] - L * math.sin(a + 0.4))
    return _line(p, q, color, 2) + '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>' % (q[0], q[1], h1[0], h1[1], h2[0], h2[1], color)


_N = {'Quadrilateral': (320, 30, 170), 'Trapezoid': (100, 115, 130), 'Parallelogram': (320, 115, 160), 'Kite': (545, 115, 90),
      'Rectangle': (215, 205, 130), 'Rhombus': (430, 205, 120), 'Square': (320, 295, 110)}
_E = [('Quadrilateral', 'Trapezoid'), ('Quadrilateral', 'Parallelogram'), ('Quadrilateral', 'Kite'),
      ('Parallelogram', 'Rectangle'), ('Parallelogram', 'Rhombus'), ('Kite', 'Rhombus'),
      ('Rectangle', 'Square'), ('Rhombus', 'Square')]


def _tree():
    b = ''
    for s, e in _E:
        (x1, y1, _), (x2, y2, _) = _N[s], _N[e]
        f = 20 / abs(y2 - y1)
        b += _arrow((x1 + (x2 - x1) * f, y1 + 20), (x2 - (x2 - x1) * f, y2 - 21))
    for k, (x, y, w) in _N.items():
        b += _box(x, y, k, w)
    return _svg('The quadrilateral family: each arrow points to a special kind', b, vb='20 0 600 320')


FIG_TREE = _tree()


# --- scaling: side x2 -> area x4 (lesson) ---
def _scale():
    b = ''
    x0, y0, u = 110, 250, 26
    b += _poly([(x0, y0), (x0 + 3 * u, y0), (x0 + 3 * u, y0 - 3 * u), (x0, y0 - 3 * u)], FILL, TEAL)
    X0 = 330
    b += _poly([(X0, y0), (X0 + 6 * u, y0), (X0 + 6 * u, y0 - 6 * u), (X0, y0 - 6 * u)], FILL, TEAL)
    for k in range(1, 6):
        if k < 3:
            b += _line((x0 + k * u, y0), (x0 + k * u, y0 - 3 * u), TEAL, 1) + _line((x0, y0 - k * u), (x0 + 3 * u, y0 - k * u), TEAL, 1)
        b += _line((X0 + k * u, y0), (X0 + k * u, y0 - 6 * u), TEAL, 1) + _line((X0, y0 - k * u), (X0 + 6 * u, y0 - k * u), TEAL, 1)
    b += _t(x0 + 1.5 * u, y0 + 22, '3') + _t(X0 + 3 * u, y0 + 22, '6')
    b += _t(x0 + 1.5 * u, y0 - 3 * u - 22, 'area 9', size=19) + _t(X0 + 3 * u, y0 - 6 * u - 22, 'area 36', size=19)
    b += _arrow((x0 + 3 * u + 18, y0 - 60), (X0 - 18, y0 - 60), TEAL) + _t((x0 + 3 * u + X0) / 2, y0 - 80, '×2', size=19, color=TEAL)
    return _svg('Side 3 becomes side 6: the area 9 becomes 36', b, vb='80 50 450 240')


FIG_SCALE = _scale()


# --- parallelogram with a 30 degree angle (lesson) ---
def _par30():
    u = 34; B_ = (120, 270); C_ = (120 + 8 * u, 270)
    A_ = _pt(B_, 6 * u, -30); D_ = (A_[0] + 8 * u, A_[1]); H_ = (A_[0], 270)
    b = _poly([A_, B_, C_, D_]) + _line(A_, H_, TEAL, 2, dash=True) + _right(H_, A_, C_, color=TEAL)
    b += _angle(B_, A_, C_, '30°', r=40, dist=66) + _t(A_[0] + 14, (A_[1] + 270) / 2, 'h', italic=True, color=TEAL)
    b += _t((B_[0] + C_[0]) / 2 + 30, 294, '8') + _t((A_[0] + B_[0]) / 2 - 16, (A_[1] + B_[1]) / 2 - 14, '6')
    b += _abcd(A_, B_, C_, D_, [(-8, -18), (-16, 12), (14, 12), (14, -14)])
    return _svg('Parallelogram ABCD with sides 8 and 6 and a 30° angle at B', b, vb='80 120 530 200')


FIG_PAR30 = _par30()


# --- guided question: parallelogram with a 150 degree angle ---
def _g1():
    s = 22; B_ = (270, 250); C_ = (270 + 14 * s, 250)
    A_ = _pt(B_, 10 * s, -150); D_ = (A_[0] + 14 * s, A_[1])
    b = _poly([A_, B_, C_, D_]) + _angle(B_, A_, C_, '150°', r=26, dist=52)
    b += _t((B_[0] + C_[0]) / 2, 274, '14') + _t((A_[0] + B_[0]) / 2 - 8, (A_[1] + B_[1]) / 2 + 22, '10')
    b += _abcd(A_, B_, C_, D_, [(-10, -16), (-4, 22), (14, 14), (14, -14)])
    return _svg('Parallelogram ABCD with an obtuse angle of 150° at B', b, vb='40 100 580 200')


FIG_G1 = _g1()

# --- trapezoids ---
_TA, _TB, _TC, _TD = (182.667, 82.667), (125.333, 277.333), (514.667, 277.333), (382.667, 82.667)
_TOFF = [(-14, -16), (-14, 16), (14, 16), (14, -16)]
FIG_TRAP = _svg('Trapezoid ABCD', _poly([_TA, _TB, _TC, _TD]) + _abcd(_TA, _TB, _TC, _TD, _TOFF), vb='79.3 40.7 481.3 278.7')


def _midseg(label, extra='', mn_text=''):
    M_, N_ = _mid(_TA, _TB), _mid(_TD, _TC)
    b = _poly([_TA, _TB, _TC, _TD]) + _line(M_, N_, TEAL, 2.5)
    for p in (M_, N_): b += '<circle cx="%.3f" cy="%.3f" r="4" fill="%s"/>' % (p[0], p[1], TEAL)
    b += _lab(M_, -18, 0, 'M') + _lab(N_, 18, 0, 'N') + _abcd(_TA, _TB, _TC, _TD, _TOFF)
    if mn_text: b += _t((M_[0] + N_[0]) / 2, M_[1] - 16, mn_text, color=TEAL)
    return _svg(label, b + extra, vb='79.3 40.7 481.3 278.7')


FIG_MID = _midseg('Trapezoid ABCD with its midsegment MN',
                  _t((_TA[0] + _TD[0]) / 2, _TA[1] - 16, 'b', italic=True) + _t((_TB[0] + _TC[0]) / 2, _TB[1] + 20, 'a', italic=True))
FIG_G3 = _midseg('Trapezoid ABCD with midsegment MN of length 11', mn_text='11')

# right trapezoid (lesson slide)
_RA, _RB, _RC, _RD = (125.333, 82.667), (125.333, 277.333), (514.667, 277.333), (372.667, 82.667)
FIG_RIGHT = _svg('Right trapezoid ABCD', _poly([_RA, _RB, _RC, _RD]) + _abcd(_RA, _RB, _RC, _RD, _TOFF), vb='79.3 40.7 481.3 278.7')


def _rtrap(label, u, ad, bc, h, labels, extra=''):
    B_ = (150, 290); C_ = (150 + bc * u, 290); A_ = (150, 290 - h * u); D_ = (150 + ad * u, 290 - h * u)
    b = _poly([A_, B_, C_, D_]) + _right(B_, A_, C_) + _right(A_, B_, D_)
    b += _abcd(A_, B_, C_, D_, [(-14, -14), (-14, 14), (14, 14), (14, -14)])
    lab = {'AD': ((A_[0] + D_[0]) / 2, A_[1] - 16), 'BC': ((B_[0] + C_[0]) / 2, 312), 'AB': (132, (A_[1] + B_[1]) / 2),
           'CD': ((C_[0] + D_[0]) / 2 + 16, (C_[1] + D_[1]) / 2 - 8)}
    for k, s in labels.items(): b += _t(lab[k][0], lab[k][1], s)
    if callable(extra): b += extra(A_, B_, C_, D_)
    return _svg(label, b, vb='100 %d 460 %d' % (290 - h * u - 40, h * u + 70))


FIG_G2 = _rtrap('Right trapezoid ABCD with bases 9 and 15 and slanted leg 10', 20, 9, 15, 8, {'AD': '9', 'BC': '15', 'CD': '10'})
FIG_Q08 = _rtrap('Right trapezoid ABCD with bases 5 and 11 and height 8', 24, 5, 11, 8, {'AD': '5', 'BC': '11', 'AB': '8'})
FIG_Q20 = _rtrap('Right trapezoid ABCD with bases 4 and 10 and a 45° angle at C', 30, 4, 10, 6, {'AD': '4', 'BC': '10'},
                 extra=lambda A_, B_, C_, D_: _angle(C_, D_, B_, '45°', r=34, dist=56))


# --- trapezoid with both diagonals ("butterfly") ---
def _bfly(label, shade=True, nums=None):
    A_, B_, C_, D_ = (230, 80), (110, 290), (530, 290), (400, 80)
    O_ = _cross(A_, C_, B_, D_)
    b = ''
    if shade:
        b += _poly([A_, B_, O_], FILL, TEAL, 0) + _poly([D_, C_, O_], FILL, TEAL, 0)
    b += _poly([A_, B_, C_, D_]) + _line(A_, C_, TEAL) + _line(B_, D_, TEAL)
    b += _abcd(A_, B_, C_, D_, [(-12, -14), (-14, 12), (14, 12), (12, -14)])
    b += _lab(O_, 24, 2, 'O') if nums else _lab(O_, 0, -20, 'O')
    if nums:
        top, bottom, left, right = nums
        if top: b += _t(O_[0], A_[1] + 0.45 * (O_[1] - A_[1]), top, size=18)
        if bottom: b += _t(O_[0], (O_[1] + 290) / 2 + 6, bottom, size=18)
        if left: b += _t((A_[0] + B_[0] + O_[0]) / 3, (A_[1] + B_[1] + O_[1]) / 3, left, size=18)
        if right: b += _t((D_[0] + C_[0] + O_[0]) / 3, (D_[1] + C_[1] + O_[1]) / 3, right, size=18)
    return _svg(label, b, vb='70 45 500 275')


FIG_BFLY = _bfly('Trapezoid ABCD with both diagonals; the two side triangles are shaded')
FIG_G4 = _bfly('Trapezoid ABCD with diagonals meeting at O and three triangle areas', shade=False, nums=('8', '18', '12', None))
FIG_BF_P = _bfly('Trapezoid ABCD with diagonals meeting at O', shade=False)


# --- concave quadrilaterals for questions ---
def _concave_q():
    B_, C_ = (170, 300), (430, 300)
    A_ = _pt(B_, 260, -70)
    dA = _dir(A_, B_) - 25                          # interior angle at A = 25
    D_ = _cross(A_, _pt(A_, 100, dA), C_, _pt(C_, 100, 180 + 35))   # interior angle at C = 35
    b = _poly([A_, B_, C_, D_])
    b += _angle(A_, D_, B_, '25°', r=52, dist=84) + _angle(B_, A_, C_, '70°', r=34, dist=58) + _angle(C_, B_, D_, '35°', r=56, dist=84)
    b += _angle(D_, C_, A_, 'x', r=26, dist=48, color=ORANGE, size=20)
    b += _abcd(A_, B_, C_, D_, [(0, -18), (-14, 12), (14, 12), (4, 24)])
    return _svg('A concave quadrilateral ABCD with the angle x in the notch at D', b, vb='120 20 400 310')


FIG_G5 = _concave_q()
FIG_Q11 = _svg('A concave quadrilateral ABCD with the angle x in the notch at D',
               _poly([_KA, _KB, _KC, _KD]) + _angle(_KA, _KD, _KB, '45°', r=30, dist=54) + _right(_KB, _KC, _KA) +
               _angle(_KC, _KB, _KD, '25°', r=48, dist=78) + _angle(_KD, _KC, _KA, 'x', r=24, dist=44, color=ORANGE, size=20) +
               _lab(_KA, 0, -17, 'A') + _lab(_KB, -16, 12, 'B') + _lab(_KC, 16, 12, 'C') + _lab(_KD, -2, 24, 'D'),
               vb='150 55 330 240')


def _dart():
    A_, B_, C_, D_ = (170, 80), (320, 300), (470, 80), (320, 170)
    b = _poly([A_, B_, C_, D_])
    b += _angle(A_, B_, D_, 'α', r=44, dist=70) + _angle(C_, D_, B_, 'α', r=44, dist=70)
    b += _angle(B_, C_, A_, '50°', r=30, dist=54) + _angle(D_, A_, C_, '110°', r=26, dist=52, color=ORANGE)
    b += _abcd(A_, B_, C_, D_, [(-14, -12), (0, 20), (14, -12), (0, 26)])
    return _svg('A concave quadrilateral ABCD shaped like an arrowhead', b, vb='120 20 400 310')


FIG_Q19 = _dart()


# --- perimeter tricks ---
def _cut():
    b = _poly([(140, 90), (140, 270), (500, 270), (500, 90)]) + _line((300, 90), (300, 270), ORANGE, 3)
    b += _t(220, 180, 'I', size=24, color=TEAL) + _t(400, 180, 'II', size=24, color=TEAL) + _t(318, 180, 'cut', size=18, color=ORANGE)
    return _svg('A rectangle cut into two smaller rectangles', b, vb='110 60 420 240')


def _stair(label, w=12, h=8, labels=True):
    u = 30; x0, y0 = 130, 300
    P = [(x0, y0), (x0 + w * u, y0), (x0 + w * u, y0 - 3 * u), (x0 + 9 * u, y0 - 3 * u), (x0 + 9 * u, y0 - 5 * u),
         (x0 + 6 * u, y0 - 5 * u), (x0 + 6 * u, y0 - 7 * u), (x0 + 3 * u, y0 - 7 * u), (x0 + 3 * u, y0 - h * u), (x0, y0 - h * u)]
    b = _poly(P)
    if labels:
        b += _t(x0 + w * u / 2, y0 + 22, str(w)) + _t(x0 - 20, y0 - h * u / 2, str(h))
    else:
        b += _poly([(x0, y0), (x0 + w * u, y0), (x0 + w * u, y0 - h * u), (x0, y0 - h * u)], 'none', TEAL, 1.5).replace('/>', ' stroke-dasharray="7 5"/>')
    return _svg(label, b, vb='90 30 470 305')


def _notch(label, labels=True):
    u = 34; x0, y0 = 150, 300
    P = [(x0, y0), (x0 + 10 * u, y0), (x0 + 10 * u, y0 - 7 * u), (x0 + 6 * u, y0 - 7 * u), (x0 + 6 * u, y0 - 4 * u),
         (x0 + 3.5 * u, y0 - 4 * u), (x0 + 3.5 * u, y0 - 7 * u), (x0, y0 - 7 * u)]
    b = _poly(P)
    if labels:
        b += _t(x0 + 5 * u, y0 + 22, '10') + _t(x0 - 20, y0 - 3.5 * u, '7') + _t(x0 + 6 * u + 16, y0 - 5.5 * u, '3')
    else:
        b += _line((x0 + 3.5 * u, y0 - 7 * u), (x0 + 3.5 * u, y0 - 4 * u), ORANGE, 3.5) + _line((x0 + 6 * u, y0 - 7 * u), (x0 + 6 * u, y0 - 4 * u), ORANGE, 3.5)
    return _svg(label, b, vb='110 40 430 290')


FIG_CUT = _cut()
FIG_STAIR = _stair('A staircase outline inside its rectangle', labels=False)
FIG_G6 = _stair('A staircase figure 12 wide and 8 tall, all angles right angles')
FIG_NOTCH = _notch('A rectangle with a rectangular notch; the two walls of the notch are marked', labels=False)
FIG_Q17 = _notch('A 10 by 7 rectangle with a notch 3 deep cut into its top side')

FIG_G7 = _svg('Rectangle ABCD with diagonal AC of length 13',
              _poly([(150, 90), (150, 270), (490, 270), (490, 90)]) + _line((150, 90), (490, 270), TEAL) +
              _t(330, 162, '13', color=TEAL) + _abcd((150, 90), (150, 270), (490, 270), (490, 90), [(-14, -14), (-14, 14), (14, 14), (14, -14)]),
              vb='110 60 420 240')


# ------------------------------------------------------------------------------------------------
# small label fixes inside existing figures: (text that identifies the figure, [(old, new), ...])
# ------------------------------------------------------------------------------------------------
def _arc_path(c, r, a1, a2):
    return _arc(c, r, a1, a2)


_P12_X = 119.773 + (143.5 - 70.5) * (484.25 - 119.773) / 219.0          # where the teal line crosses AD
_P12_A = math.degrees(math.atan2(219.0, 484.25 - 119.773))
FIX = [
    # Q13 kite: "12" under BO, not inside triangle ABO next to AB
    ('A kite with three given lengths', [('x="240.364" y="93.636"', 'x="240.364" y="132.000"')]),
    # adv-p18: 12 with a dimension line over the whole of AD (F cuts AD)
    ('A square inside a parallelogram', [(
        _t(421.818, 87.091, '12'),
        _line((269.091, 76), (574.545, 76), INK, 1.5) + _line((269.091, 68), (269.091, 84), INK, 1.5) +
        _line((574.545, 68), (574.545, 84), INK, 1.5) + _t(421.818, 60, '12'))]),
    # adv-p12: the top alpha moves to the vertical angle inside the rectangle (away from the label A)
    ('Two rays meet at a rectangle corner', [
        ('<path d="M 216.236 128.461 A 29.200 29.200 0 0 0 212.065 143.500" fill="none" stroke="#087f83" stroke-width="2"/>',
         _arc((_P12_X, 143.5), 29.2, 0, _P12_A)),
        (_t(198.355, 131.6, 'α', size=18, color=TEAL), _t(*_pt((_P12_X, 143.5), 50, _P12_A / 2), 'α', size=18, color=TEAL))]),
    # adv-p20: the 45 degree mark between the vertical side and the tilted side, clear of both lines
    ('The overlap of two rectangles at a forty-five-degree angle', [
        ('<path d="M 298.417 265.602 A 16.504 16.504 0 0 0 293.583 253.932" fill="none" stroke="#087f83" stroke-width="2"/>',
         _arc((281.913, 265.602), 26, -90, -45)),
        (_t(302.087, 257.246, '45°', size=18, color=TEAL), _t(*_pt((281.913, 265.602), 52, -67.5), '45°', size=17, color=TEAL))]),
    # adv-p06: 15 degree label outside the thin wedge; C label off the line BF
    ('A rectangle attached to a square diagonal', [
        ('<path d="M 248.107 165.743 A 38.933 38.933 0 0 0 249.433 155.667" fill="none" stroke="#087f83" stroke-width="2"/>',
         _arc((210.5, 155.667), 60, 0, 15)),
        (_t(259.233, 162.082, '15°', size=18, color=TEAL), _t(*_pt((210.5, 155.667), 92, 7.5), '15°', size=16, color=TEAL)),
        (_t(292.5, 173.667, 'C'), _t(297, 142, 'C'))]),
    # Q18 trapezoid: "14 cm²" inside the shaded triangle, off side AB
    ('Area ratio across a trapezoid diagonal', [(_t(238.889, 147.556, '14 cm²', size=17), _t(272, 112, '14 cm²', size=17))]),
    # adv-p02: AE : ED drawn 12 : 7, as the areas say
    ('Find a corner area from the central triangle', [('344.333', '377.632')]),
]




# ------------------------------------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------------------------------------
def _script_of(M, vid, n):
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _edit(M, vid, n, key, old, new):
    """Replace one whole say/draw line (new=None deletes it; new may be a list of line dicts to put in its place)."""
    def fn(lines):
        out = []; hit = False
        for l in lines:
            if l.get(key) == old:
                hit = True
                if new is None: continue
                if isinstance(new, list): out.extend(new); continue
                l = dict(l, **{key: new})
            out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def _say(M, vid, n, old, new): _edit(M, vid, n, 'say', old, new)
def _draw(M, vid, n, old, new): _edit(M, vid, n, 'draw', old, new)


def _after(M, vid, n, old, new_lines):
    """Insert line dicts right after the spoken line old."""
    _say(M, vid, n, old, [{'say': old}] + new_lines)


def _item_text(M, vid, n, old, new):
    b = M.slide(vid, n)
    for it in b['items']:
        if it.get('t') == old:
            it['t'] = new; M.touched_videos.add(vid); return
    raise AssertionError((vid, n, old))


def _vis(M, vid, n, svg, k=0):
    its = [it for it in M.slide(vid, n)['items'] if it.get('k') == 'vis']
    its[k]['v']['svg'] = svg; M.touched_videos.add(vid)


def _set_group(M, vids, labels):
    """Solution videos of one group: same sidebar; each slide highlights its own question."""
    for vid in vids:
        v = M.video(vid); M.set_sidebar(vid, labels)
        own = 'Question %s' % re.match(r'Question (\d+)', v['beats'][0].get('bigTitle') or '').group(1)
        for b in v['beats']:
            if b['mode'] != 'title': b['active'] = labels.index(own)


def _sync_stem_copies(M, qids):
    for qid in qids:
        q = M.q(qid)
        for v in M.D['videos'].values():
            if v.get('questionId') != qid: continue
            for b in v['beats']:
                if (b.get('canvas') or '').startswith('Pre-loaded — question'):
                    b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])


def _qfig(qid, svg):
    return [Q(qid, fig={'type': 'geometry', 'svg': svg}, figw=0.56, figalign='left')]


def _R(t, row, size=40):
    """Board line next to the question figure."""
    return T(t, size=size, x=1060, y=250 + 90 * row, w=470)


def _solution(M, qid, vid, title, group_title, num, intro, slides, fig):
    """Worked-solution video in the style of the existing solve-geo32-* videos. Returns its question number."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for st, script in slides:
        beats.append(dict(mode='question', active=0, title=st, pre=_qfig(qid, fig), script=script))
    v = M.new_video(vid, TOPIC, title, ['Question %d' % n], beats, M.section_of(qid), kind='solution', qid=qid)
    v['beats'][0]['title'] = group_title
    v['hybrid']['num'] = num
    return n


US = [('centimetres', 'centimeters'), ('centimetre', 'centimeter'), ('memorise', 'memorize'), ('Memorise', 'Memorize'),
      ('practise', 'practice'), ('colour', 'color'), ('realise', 'realize'), ('recognise', 'recognize'), ('metres', 'meters')]


def _american(M):
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        hit = False
        for b in v['beats']:
            for l in b['lines']:
                for k in ('say', 'draw', 'label'):
                    if k in l:
                        s = l[k]
                        for a, c in US: s = s.replace(a, c)
                        if s != l[k]: l[k] = s; hit = True
            for it in b['items']:
                if it.get('t'):
                    s = it['t']
                    for a, c in US: s = s.replace(a, c)
                    if s != it['t']: it['t'] = s; hit = True
        if hit: M.touched_videos.add(v['id'])


# ================================================================================================
def apply(M):
    _figures(M)
    _lesson_videos(M)
    _existing_solution_videos(M)
    _existing_questions(M)
    _new_guided(M)
    _cards(M)
    _practice(M)
    _american(M)
    _summaries(M)
    cut_repeats(M)          # 2026-10-05: last


def _all_svgs(M):
    """Yield (container, key, video id) for every figure svg in topic 32 (question figures, slide figures, question copies)."""
    for q in M.D['questions'].values():
        if q.get('topic') == TOPIC and q.get('questionVisual'):
            yield q['questionVisual'], 'svg', None
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            for it in b['items']:
                if it.get('k') == 'vis': yield it['v'], 'svg', v['id']
                if it.get('k') == 'q' and it.get('fig'): yield it['fig'], 'svg', v['id']


def _figures(M):
    for c, k, vid in list(_all_svgs(M)):
        s = c[k]
        for key, reps in FIX:
            if 'aria-label="%s"' % key in s:
                for old, new in reps:
                    assert old in s, (key, old[:60])
                    s = s.replace(old, new)
        if s != c[k]:
            c[k] = s
            if vid: M.touched_videos.add(vid)
    # lesson figures that showed the wrong shape
    _vis(M, 'geo-042', 2, FIG_QUAD); _vis(M, 'geo-042', 4, FIG_QUAD)      # "general" quadrilateral was a parallelogram
    _vis(M, 'geo-042', 3, FIG_CONCAVE)                                     # B label sat on side AB
    for n in (2, 3, 4): _vis(M, 'geo-054', n, FIG_TRAP)                    # a general trapezoid, not an isosceles one
    _vis(M, 'geo-054', 7, FIG_RIGHT)                                       # the right trapezoid was drawn isosceles


# ------------------------------------------------------------------------------------------------
# 1. Lesson videos: "not necessarily", definitions, family tree, new rules
# ------------------------------------------------------------------------------------------------
def _lesson_videos(M):
    # ---- geo-042 Quadrilaterals: family tree ----
    _say(M, 'geo-042', 5, 'From here: a lesson on each one. We start with the square — the easiest to understand, because we all know what a square is.',
         "These arrows show how we changed one shape into another. But which shape is ALSO which? Let's draw it as a family tree.")
    M.insert_slides('geo-042', 5, [dict(mode='concept', active=4, title='Who is also who?', script=[
        A('The family tree appears', VIS(FIG_TREE, w=1000, h=520)),
        "Now the same family as a tree. Read every arrow as \"a special kind of\".",
        "A trapezoid, a parallelogram and a kite are special kinds of quadrilateral.",
        "A rectangle is a special parallelogram: a parallelogram with right angles.",
        "A rhombus is a special parallelogram — and also a special kite. All four sides are equal.",
        "At the bottom: the square. It's a rectangle AND a rhombus.",
        D('Trace the path from Square up to Quadrilateral'),
        "Going down the tree, a shape only gains properties. A square has every property of every shape above it.",
        A("'Down the tree: all the properties above' appears", T('Down the tree: all the properties of the shapes above', size=38, x=410, y=650)),
        "Going up — careful. Every square is a rectangle. But a rectangle is not necessarily a square.",
        A("'Up the tree: only \"not necessarily\"' appears", T('Up the tree: \"not necessarily\"', size=38, x=410, y=730)),
        "That's why we say \"not necessarily\". A rectangle's diagonals are not necessarily perpendicular — but in a square they are.",
        "From here: a lesson on each one. We start with the square — the easiest to understand, because we all know what a square is.",
    ])])
    M.set_sidebar('geo-042', ['What it is', 'It can bend inward', 'Angle sum 360°', 'The family', 'Who is also who?'])

    # ---- geo-043 The Square: scaling rule + colon in a draw note ----
    _draw(M, 'geo-043', 6, 'Write 6 × 6 : 2 = 18 inside that triangle', 'Write 6 × 6 ÷ 2 = 18 inside that triangle')
    M.insert_slides('geo-043', 6, [dict(mode='concept', active=5, title='Scale it up', script=[
        A('Two squares, side 3 and side 6, appear', VIS(FIG_SCALE, w=1000, h=520)),
        "One more thing about area — and it's true for every shape.",
        "Double the side of a square: 3 becomes 6.",
        "The area? Not double. 9 becomes 36 — four times as much.",
        "Count the little squares: every row is twice as long, and there are twice as many rows. 2 times 2 — 4.",
        A("'every length × k → area × k²' appears", T('Every length $\\times k$ $\\Rightarrow$ area $\\times k^2$', size=46, x=410, y=650)),
        "Every length times k — the area times k squared.",
        A("'diagonal +50% → area ×2.25' appears", T('Diagonal $+50\\%$: $\\times1.5$ $\\Rightarrow$ area $\\times2.25$, up $125\\%$', size=38, x=410, y=740)),
        "The diagonal grows by 50 percent? That's times 1.5. The area grows times 1.5 squared — 2.25. That's up 125 percent.",
        "Careful: this is only when ALL the lengths grow. Only the base grows and the height stays? Then the area grows by the same factor as the base.",
    ])])
    M.video('geo-043')['beats'][7]['active'] = 6
    M.set_sidebar('geo-043', ['Sides and angles', 'The diagonals', 'Silver triangles', 'Area: side squared', 'Area from a diagonal',
                              'Scale it up', 'Square: all yes'])

    # ---- geo-045 The Rectangle: "not necessarily" ----
    _item_text(M, 'geo-045', 3, "NOT perpendicular · DON'T bisect the angles",
               "Not necessarily $\\perp$ · not necessarily angle bisectors")
    _say(M, 'geo-045', 3, 'The diagonals are NOT perpendicular. You can actually see it here.',
         'Are they perpendicular? Not necessarily. You can see it here — these are not.')
    _say(M, 'geo-045', 3, "And they don't bisect the rectangle's angles — unlike the square.",
         "Do they bisect the rectangle's angles? Not necessarily either.")
    _say(M, 'geo-045', 3, 'In the square they were perpendicular and bisected the angles. Here — neither.',
         "In a square they always do both — and a square is a special rectangle. But in a general rectangle, don't assume it.")

    # ---- geo-047 The Parallelogram: "not necessarily", height from A, special angles ----
    _say(M, 'geo-047', 5, "They're NOT equal. You can see it here — a longer diagonal and a shorter one.",
         'Are they equal? Not necessarily. Here there is a longer diagonal and a shorter one.')
    _say(M, 'geo-047', 5, "They also don't bisect the parallelogram's angles, even though sometimes it looks like it.",
         "Do they bisect the parallelogram's angles? Not necessarily — even though sometimes it looks like it.")
    _say(M, 'geo-047', 5, "And they're not perpendicular.", [
        {'say': 'Perpendicular? Not necessarily either.'},
        {'say': 'Equal diagonals? Then it is a rectangle. Perpendicular diagonals? Then it is a rhombus. A general parallelogram promises only one thing: they bisect each other.'}])
    _draw(M, 'geo-047', 6, 'Draw the height from D down to BC with a right-angle mark; write h',
          'Draw the height from A down to BC with a right-angle mark; write h')
    _after(M, 'geo-047', 6, 'a times h. The HEIGHT — perpendicular to the base. Not the sloping side.', [
        {'say': 'Careful where you drop it. From A, the foot lands on BC. From D, it would land outside BC — then you extend BC first.'}])
    M.insert_slides('geo-047', 7, [dict(mode='concept', active=6, title='Special angles', script=[
        A('Parallelogram ABCD with sides 8 and 6 and a 30° angle appears', VIS(FIG_PAR30, w=1000, h=520)),
        "Exam questions love a parallelogram with a special angle: 30, 45 or 60.",
        "Sides 8 and 6, and a 30-degree angle at B. What is the area?",
        D('Drop the height from A to BC; mark the right angle'),
        "Drop the height from A. A right triangle forms — with a 30. A golden triangle.",
        "The height is opposite the 30 — the short leg. It's half the hypotenuse: half of 6 is 3.",
        A("'30°: h = 3, S = 24' appears", T('$30°$: $h=\\frac62=3$ $\\Rightarrow$ $S=8\\cdot3=24$', size=44, x=410, y=650)),
        "Area: 8 times 3 — 24. The trap: 8 times 6. The sloping side is not the height.",
        A("'45° and 60°' appears", T('$45°$: $h=\\frac{\\text{side}}{\\sqrt2}$ $\\cdot$ $60°$: $h=\\frac{\\text{side}}{2}\\cdot\\sqrt3$', size=40, x=410, y=740)),
        "With 45: a silver triangle — the height is the side over root 2. With 60: half the side, times root 3.",
        "And an obtuse angle, like 150? Look at the angle next to it: 30. Same rule.",
    ])])
    M.set_sidebar('geo-047', ['Squash a rectangle', 'Angles', 'Why: parallel lines', 'The diagonals', 'Area: base × height',
                              'Why: cut and move', 'Special angles'])

    # ---- geo-050 The Rhombus ----
    _item_text(M, 'geo-050', 3, 'Perpendicular · bisect each other · bisect the angles — NOT equal',
               'Perpendicular · bisect each other · bisect the angles — not necessarily equal')
    _say(M, 'geo-050', 3, "They're NOT equal — there's a long diagonal and a short one.",
         "Are they equal? Not necessarily — usually there's a long diagonal and a short one. If they are equal, the rhombus is a square.")

    # ---- geo-052 The Kite ----
    _say(M, 'geo-052', 3, "The diagonals of the kite. They're not equal.", "The diagonals of the kite. They're not necessarily equal.")
    _say(M, 'geo-052', 3, "The main one is the kite's line of symmetry. It joins the two head angles.",
         "The main one is the kite's line of symmetry. It joins the two angles between the equal sides — here, A and C.")
    _say(M, 'geo-052', 4, 'So the main diagonal also bisects the head angles.', 'So the main diagonal also bisects the angles at A and C.')
    _say(M, 'geo-052', 4, "The secondary diagonal doesn't bisect its angles — this angle isn't equal to this one.",
         "The secondary diagonal doesn't necessarily bisect its angles — here this angle isn't equal to this one.")

    # ---- geo-054 The Trapezoid ----
    _say(M, 'geo-054', 2, "So the definition of a trapezoid: the legs aren't parallel.",
         'So the definition of a trapezoid: exactly one pair of parallel sides — the bases.')
    _after(M, 'geo-054', 6, '— and they cut each other into matching pieces: the top parts are equal, and the bottom parts are equal.', [
        {'appear': 2, 'label': "'Opposite angles: α + β = 180°' appears"},
        {'say': 'One more: alpha plus beta is 180 — they sit on the same leg.'},
        {'say': 'So opposite angles, like A and C, also add up to 180. Remember it for angle questions.'}])
    M.slide('geo-054', 6)['items'].append(T('Opposite angles: $\\alpha+\\beta=180°$', size=36, x=410, y=730))
    _draw(M, 'geo-054', 7, 'Draw a leg perpendicular to the bases, with right-angle marks top and bottom', 'Draw right-angle marks at A and at B')
    _say(M, 'geo-054', 7, 'Nothing else special about it.',
         'In questions: drop the height from D. You get a rectangle and a right triangle — and Pythagoras does the rest.')
    # (Pass 2: the arrow rule, the midsegment and the trapezoid "butterfly" slides were removed - teacher's plan)


# ------------------------------------------------------------------------------------------------
# 2. Existing solution videos
# ------------------------------------------------------------------------------------------------
def _existing_solution_videos(M):
    # division written with ":" in teacher notes / board
    _draw(M, 'solve-geo32-g044', 2, 'Write 144 : 2 = 72', 'Write 144 ÷ 2 = 72')
    _draw(M, 'solve-geo32-g068', 2, 'Write 2 : 1 on AD and on BC', 'Write the ratio 2 : 1 on AD and on BC')
    _draw(M, 'solve-geo32-g069', 3, 'Write 4 : 12 = 1 : 3', 'Write the ratio 4 : 12 = 1 : 3')
    _item_text(M, 'solve-geo32-g046', 2, '$(180°-120°):2=30°$', '$\\frac{180°-120°}{2}=30°$')
    _say(M, 'solve-geo32-g046', 5, "Look at it. Are the diagonals perpendicular? Do they bisect the angles? You'll see it right away — no.",
         "Look at it. Are the diagonals perpendicular? Do they bisect the angles? You'll see it right away: not necessarily.")
    # Q9: name the pattern
    _after(M, 'solve-geo32-g058', 4, 'Equal angles — so the sides opposite them are equal. The triangle is isosceles.', [
        {'say': 'Remember this pattern: an angle bisector in a parallelogram cuts off an isosceles triangle. Bisector plus parallel sides — isosceles.'}])
    # Q15: the kite's shared base is the secondary diagonal
    _say(M, 'solve-geo32-g066', 2, "What's a kite? Two isosceles triangles on a shared base — the short diagonal.",
         "What's a kite? Two isosceles triangles on a shared base — the secondary diagonal.")

    # Q10: three ways, all taught (original framing and order - Pass 2); only clean-ups here
    vid = 'solve-geo32-g059'
    _say(M, vid, 5, 'By the way — that\'s true across the whole parallelogram family: rectangle, rhombus, square.',
         "By the way — that's true in every parallelogram, and so also in a rectangle, a rhombus and a square.")
    _say(M, vid, 5, 'So one triangle is the rectangle divided by 4: 5 times 12 is 60, over 4 — 15. Choice three.', [
        {'say': 'So one triangle is the rectangle divided by 4: 5 times 12 is 60, over 4 — 15.'}, {'draw': 'Circle choice 3'}, {'say': 'Choice three.'}])

    # Q11: original framing and order (Pass 2). Slide 6 keeps its fix: AB = AD, so angle ADB (not "the angle opposite AD") is 60.
    vid = 'solve-geo32-g060'
    b6 = M.slide(vid, 6)
    M.set_slide(vid, 6, script=[
        "One more way. Well done if you spotted this one.",
        "Some notice the 60 degrees and say: wait — that's a hint.",
        D('Mark AB and AD as equal'),
        "In a rhombus all the sides are equal. AB equals AD — so triangle ABD is isosceles, and angle ADB is 60 too.",
        D('Write 60° at D and at A in triangle ABD'),
        "Two 60s make 120 — so the top angle is 60 as well. The triangle is equilateral.",
        "Worth remembering: an isosceles triangle with a 60-degree angle is always equilateral.",
        D('Write 6 on AB, AD, BC and CD'),
        "BD is 6 — so AB and AD are 6. And all the sides of a rhombus are equal: DC and BC are 6 too.",
        "So what do we have? Two equilateral triangles.",
        A(b6['lines'][[l.get('appear') for l in b6['lines']].index(1)]['label'], b6['items'][1]),
        "Area of one equilateral triangle: side squared times root 3 over 4. Twice: 2 times 36 root 3 over 4 — 18 root 3.",
        D('Circle choice 4'),
        "That's the shorter, psychometric way. Choice four.",
    ])

    # Q19: the "Completions" slide stays (restored in Pass 2 - it is correct)

    # Q21: work back from the answers
    vid = 'solve-geo32-g072'
    pre = [dict(M.slide(vid, 2)['items'][0])]
    M.insert_slides(vid, 2, [dict(mode='question', active=4, title='Check from the answers', pre=pre, script=[
        "One more way — work back from the answers.",
        "The area is 4x times 6x — 24 x squared. And the perimeter, 20x, must be 50.",
        A("'S = 24x²' appears", _R('$S=4x\\cdot6x=24x^2$', 0)),
        "Try choice one, 150. 150 divided by 24 is 6.25 — that's 2.5 squared. So x is 2.5.",
        A("'150 ÷ 24 = 6.25 = 2.5²' appears", _R('$150\\div24=6.25=2.5^2$', 1, size=36)),
        "Check the one number we were given, the perimeter: 20 times 2.5 — 50. It fits.",
        A("'20 · 2.5 = 50' appears", _R('$20\\cdot2.5=50$', 2)),
        "Try 100, 125 or 200: divided by 24, none of them gives a perimeter of 50.",
        "Short on time? Plug an answer back into the figure and check the number you were given.",
    ])])


# ------------------------------------------------------------------------------------------------
# 3. Existing questions: stacked givens, TeX solutions with numbers, spacing after commas
# ------------------------------------------------------------------------------------------------
def _cases(*rows):
    return '$\\begin{cases} ' + ' \\\\ '.join(rows) + ' \\end{cases}$'


CM = '\\text{ cm}'
STEMS = {
    'geo32-g046': 'The diagonals of rectangle ABCD intersect at E. Given:\n' + _cases('CD=3' + CM, '\\angle BEC=120°') +
                  '\nWhat is the area of the rectangle (in cm²)?',
    'geo32-g049': 'ABCD is a parallelogram, and $AE\\perp BC$. Given:\n' + _cases('AD=17' + CM, 'CD=13' + CM, 'EC=12' + CM) +
                  '\nWhat is the area of the parallelogram (in cm²)?',
    'geo32-g053': 'ABCD is a kite. Given:\n' + _cases('AB=AD', 'CB=CD=6' + CM, '\\angle ABD=45°', '\\angle DBC=60°') +
                  '\nWhat is the perimeter of the kite (in cm)?',
    'geo32-g058': 'ABCD is a parallelogram, and E lies on AD. Given:\n' + _cases('AB=7' + CM, 'AE=3' + CM, '\\angle ABC=64°', '\\angle BCE=58°') +
                  '\nWhat is the perimeter of the parallelogram (in cm)?',
    'geo32-g060': 'ABCD is a rhombus. Given:\n' + _cases('BD=6' + CM, '\\angle ABD=60°') + '\nWhat is the area of the rhombus (in cm²)?',
    'geo32-g062': 'ABCD is a kite, and its diagonals meet at O. Given:\n' + _cases('AB=AD=13' + CM, 'CB=CD', 'BO=12' + CM, 'OC=15' + CM) +
                  '\nWhat is the area of the kite (in cm²)?',
    'geo32-g063': 'ABCD is an isosceles trapezoid with $AD\\parallel BC$. Given:\n' + _cases('AB=AD=5' + CM, '\\angle ABD=30°') +
                  '\nWhat is its perimeter (in cm)?',
    'geo32-g068': 'ABCD is a rectangle. E lies on AD, G lies on BC, and F lies on AB. Given:\n' + _cases('AE=2ED', 'BG=2GC') +
                  '\nTriangles FEG and EGC are shaded. Which of the following additional data is sufficient to determine the total shaded area?',
    'geo32-g069': 'ABCD is an isosceles trapezoid. Given:\n' + _cases('AD\\parallel BC', 'AD=4' + CM, 'BC=12' + CM) +
                  '\nThe shaded triangle ABD has area 14 cm². What is the area of the trapezoid (in cm²)?',
    'geo32-foundation-p02': 'ABCD is an isosceles trapezoid with $AD\\parallel BC$. Given: $y=x+32°$. What is x?',
    'geo32-foundation-p03': 'ABCD is an isosceles trapezoid with $AD\\parallel BC$. Angle ABC is $2t$. Which expression equals β?',
    'geo32-advanced-p03': 'ABCD is an isosceles trapezoid with $AD\\parallel BC$. Given:\n' + _cases('AB=9' + CM, 'BC=18' + CM, '\\angle BAC=90°') +
                          '\nWhat is α?',
    'geo32-advanced-p05': 'ABCD is an isosceles trapezoid with $AD\\parallel BC$. Given:\n' + _cases('AB=AD=CD', '\\angle DAC=2t') +
                          '\nWhich expression equals β?',
    'geo32-advanced-p07': 'ABCD is a kite. Given:\n' + _cases('AB=AD', 'CB=CD', '\\angle A=3t', '\\angle C=t') +
                          '\nWhich expression equals angle ADC?',
    'geo32-advanced-p13': 'ABCD is a square. Isosceles triangles AFB and AED are constructed outside it. Given:\n' +
                          _cases('FA=FB', 'EA=ED', '\\angle AFB=2p', '\\angle AED=2q') + '\nWhich expression equals the marked angle FAE?',
    'geo32-advanced-p14': 'ABCD is a rectangle with perimeter 34 cm. E lies on AB, and F lies on CD. Given:\n' + _cases('BE=DF', 'EF=7' + CM) +
                          '\nWhat is the perimeter of quadrilateral AEFD (in cm)?',
    'geo32-advanced-p17': 'ABCD is a trapezoid, and $a>0$. Given:\n' + _cases('AD\\parallel BC', 'AD=3a', 'BC=5a') +
                          '\nE and F lie on BC. The area of trapezoid AEFD equals the combined areas of the two shaded triangles. What is EF?',
    'geo32-advanced-p08': 'In rectangle ABCD, E lies on CD, and $DE=3EC$. The areas of triangles AED, AEC and ABC are x, y and z, '
                          'respectively. What is the ratio $x:y:z$?',
}

EXPL = {
    'geo32-g044': ['The area of a square from its diagonal: $S=\\frac{d^2}{2}$.', '$S=\\frac{12^2}{2}=\\frac{144}{2}=72$.'],
    'geo32-g046': ['The diagonals of a rectangle are equal and bisect each other, so $EB=EC$. Triangle BEC is isosceles, and its base angles are $\\frac{180°-120°}{2}=30°$.',
                   'In right triangle BCD, $\\angle DBC=30°$. CD is opposite the $30°$ angle: it is the short leg, 3. The long leg is $BC=3\\sqrt3$ (the sides are in the ratio $1 : \\sqrt3 : 2$).',
                   '$S=3\\cdot3\\sqrt3=9\\sqrt3$.'],
    'geo32-g048': ['Angle B is $3\\alpha+\\alpha=4\\alpha$, and angle C is $4\\beta$. Adjacent angles of a parallelogram add up to $180°$: $4\\alpha+4\\beta=180°$. Therefore $\\alpha+\\beta=45°$.',
                   'In triangle BCE: $x=180°-3\\alpha-3\\beta=180°-3(\\alpha+\\beta)=180°-135°=45°$.'],
    'geo32-g049': ['Opposite sides are equal: $BC=AD=17$ and $AB=CD=13$.',
                   '$BE=17-12=5$. In right triangle ABE, the sides are $5, 12, 13$ (a Pythagorean triple). The height is $AE=12$.',
                   '$S=BC\\cdot AE=17\\cdot12=204$.'],
    'geo32-g051': ['Call the diagonals $a>b$. Then:\n$\\begin{cases} a+b=34 \\\\ a-b=14 \\end{cases}$',
                   'Add the equations: $2a=48$. Therefore $a=24$ and $b=10$.',
                   'The diagonals are perpendicular and bisect each other: the half-diagonals 12 and 5 are the legs of a right triangle. Its hypotenuse, the side, is 13 ($5, 12, 13$).',
                   '$P=4\\cdot13=52$.'],
    'geo32-g053': ['Triangle BCD: $CB=CD=6$ and $\\angle DBC=60°$. An isosceles triangle with a $60°$ angle is equilateral, so $BD=6$.',
                   'Triangle ABD: $AB=AD$, so $\\angle ADB=\\angle ABD=45°$ and $\\angle A=90°$. It is a 45-45-90 triangle with hypotenuse $BD=6$.',
                   'Each leg: $AB=AD=\\frac{6}{\\sqrt2}=3\\sqrt2$.', '$P=6+6+3\\sqrt2+3\\sqrt2=12+6\\sqrt2$.'],
    'geo32-g055': ['Triangle DEC: $\\frac{6\\cdot EC}{2}=6$, so $EC=2$.',
                   'Drop the height AF too. The trapezoid is isosceles, so triangle ABF also has area 6.',
                   'The middle rectangle AFED has area $54-6-6=42$ and height 6: $AD=\\frac{42}{6}=7$.'],
    'geo32-g057': ['Call the fourth angle β. The angles of a quadrilateral add up to $360°$: $\\alpha+\\beta=360°-112°-104°=144°$.',
                   'Both angles are positive, so $\\alpha<144°$. If $\\alpha=144°$, then $\\beta=0°$ — impossible.',
                   'The other choices are possible: $16°+128°$, $64°+80°$ and $128°+16°$ all give $144°$.'],
    'geo32-g058': ['Opposite angles are equal: $\\angle D=\\angle B=64°$. Adjacent angles: $\\angle C=180°-64°=116°$, so $\\angle ECD=116°-58°=58°$.',
                   'Triangle EDC: $\\angle CED=180°-64°-58°=58°$. Two equal angles, so $ED=CD=AB=7$. (An angle bisector in a parallelogram cuts off an isosceles triangle.)',
                   '$AD=3+7=10$ and $P=2(7+10)=34$.'],
    'geo32-g059': ['The diagonals of a rectangle are equal and bisect each other: $EB=EC$. $EB+EC=25-12=13$, so each is $6.5$ and $AC=13$.',
                   'Right triangle ABC: hypotenuse 13 and leg 12, so $AB=5$ ($5, 12, 13$). The rectangle is $5\\cdot12=60$.',
                   'The diagonals of any parallelogram (a rectangle too) split it into four triangles of equal area: $S_{ABE}=\\frac{60}{4}=15$.'],
    'geo32-g060': ['$AB=AD$ (all the sides of a rhombus are equal), so triangle ABD is isosceles with a $60°$ angle. It is equilateral: $AB=AD=BD=6$.',
                   'All the sides are 6, so triangle BCD is equilateral too.',
                   '$S=2\\cdot\\frac{6^2\\sqrt3}{4}=2\\cdot9\\sqrt3=18\\sqrt3$.'],
    'geo32-g061': ['$AO=AD=AB$ (the sides of the equilateral triangle and of the square).',
                   '$\\angle BAO=90°-60°=30°$. Triangle ABO is isosceles: $\\angle ABO=\\frac{180°-30°}{2}=75°$.',
                   '$\\angle OBC=90°-75°=15°$. (75° is a trap: it is angle ABO.)'],
    'geo32-g062': ['The main diagonal AC bisects BD: $OD=BO=12$, so $BD=24$.',
                   'Right triangle AOD: hypotenuse 13 and leg 12, so $AO=5$ ($5, 12, 13$). $AC=5+15=20$.',
                   '$S=\\frac{AC\\cdot BD}{2}=\\frac{20\\cdot24}{2}=240$.'],
    'geo32-g063': ['$AB=AD$, so $\\angle ADB=\\angle ABD=30°$ and $\\angle A=180°-30°-30°=120°$.',
                   'Angles on the same leg add up to $180°$: $\\angle B=60°$, so $\\angle DBC=60°-30°=30°$. The trapezoid is isosceles: $\\angle C=\\angle B=60°$.',
                   'Triangle BCD has angles $30°$, $60°$ and $90°$. The short leg is $CD=AB=5$, so the hypotenuse is $BC=2\\cdot5=10$.',
                   '$P=5+5+5+10=25$.'],
    'geo32-foundation-p01': ['The four triangles have a total perimeter of $4\\cdot38=152$.',
                             'Their bases are the sides of the square, $40$ in total. They are inside the figure, so they are not part of its perimeter.',
                             '$P=152-40=112$.'],
    'geo32-foundation-p02': ['In an isosceles trapezoid, opposite angles add up to $180°$ (angles on the same leg add up to $180°$, and the base angles are equal).',
                             '$x+y=180°$: $x+x+32°=180°$, $2x=148°$ and $x=74°$.'],
    'geo32-foundation-p03': ['Isosceles trapezoid: the base angles are equal, $\\angle BCD=\\angle ABC=2t$.',
                             'β and angle C sit on the same leg CD: $\\beta=180°-2t$.'],
    'geo32-foundation-p04': ['$\\angle ABC=180°-124°=56°$, and BE bisects it: $\\angle EBC=\\frac{56°}{2}=28°$.',
                             '$AD\\parallel BC$, so $\\angle AEB=\\angle EBC=28°$ (Z-angles).'],
    'geo32-foundation-p06': ['The two added lines are parallel, and $AB\\parallel DC$. By the parallel-line angles, the angle between CB and the line through C equals α.',
                             'So the whole angle at C is $\\alpha+\\gamma$, and angle B is β.',
                             'Adjacent angles of a parallelogram add up to $180°$: $\\alpha+\\beta+\\gamma=180°$.'],
    'geo32-foundation-p07': ['Each side is $\\frac{36}{4}=9$.',
                             'A diagonal and two sides make a triangle, so the diagonal is shorter than $9+9=18$. 19 is impossible.',
                             'The longer diagonal is at least the diagonal of a square with side 9: $9\\sqrt2\\approx12.7$. So 13, 15 and 17 are all possible.'],
    'geo32-foundation-p09': ['Complete the figure to a $14\\times14$ square, and take away the missing $9\\times9$ square.',
                             '$S=14^2-9^2=196-81=115$.'],
    'geo32-foundation-p10': ['Each white kite has perpendicular diagonals 4 and 2: $S=\\frac{4\\cdot2}{2}=4$. The two kites: $8$.',
                             'The rectangle is 30, so the shaded area is $30-8=22$.'],
    'geo32-foundation-p11': ['All four outside sides equal AC, so ABCD is a rhombus.',
                             'α is an angle of the equilateral triangle ACD: $\\alpha=60°$.',
                             'The diagonal BD bisects the $60°$ angle at D: $\\beta=30°$. $\\alpha+\\beta=90°$.'],
    'geo32-foundation-p13': ['The other side: $\\frac{11-2\\cdot4}{2}=\\frac32=1.5$.', '$S=4\\cdot1.5=6$.'],
    'geo32-foundation-p14': ['Square, rhombus and kite: the diagonals are always perpendicular.',
                             'Rectangle: the diagonals are equal and bisect each other, but they are not necessarily perpendicular. Example: an $8\\times3$ rectangle.'],
    'geo32-foundation-p15': ['Look at the quadrilateral formed by AB, the two long lines and the perpendicular. Three of its angles are $101°$, $67°$ and $90°$.',
                             'Its angle at A: $360°-101°-67°-90°=102°$.',
                             '$AB\\parallel CD$, so α is the corresponding angle: $\\alpha=102°$.'],
    'geo32-foundation-p16': ['Each corner triangle is right-angled: hypotenuse 13 and one leg 5. The other leg is 12 ($5, 12, 13$).',
                             'The rectangle is $2\\cdot5=10$ by $2\\cdot12=24$.', '$P=2(10+24)=68$.'],
    'geo32-foundation-p17': ['12 equal angles meet at the center: each is $\\frac{360°}{12}=30°$.',
                             'Opposite angles of a rhombus are equal: $\\alpha=30°$.'],
    'geo32-foundation-p18': ['The side of the square is $\\frac{40}{4}=10$.',
                             'Each small rectangle is $\\frac{10}{5}=2$ wide and $\\frac{10}{4}=2.5$ tall.', '$P=2(2+2.5)=9$.'],
    'geo32-foundation-p20': ['Square: the perimeter gives the side, and the side gives the area. Leah is correct.',
                             'Rhombus: the perimeter gives the side, but the angles can change. A rhombus with side 5 can be a square (area 25) or very flat (area close to 0). Daniel is incorrect.'],
    'geo32-foundation-p21': ['Call the sides $x$ and $x+5$: $x(x+5)=84$.',
                             'Try factor pairs of 84: $7\\cdot12=84$, and $12-7=5$. The sides are 7 and 12.', '$P=2(7+12)=38$.'],
    'geo32-foundation-p23': ['Drop both heights. The difference of the bases, $20-8=12$, splits into two equal ends of 6.',
                             'Each end triangle: hypotenuse 10 and leg 6, so the height is 8 ($6, 8, 10$).', '$S=\\frac{(8+20)\\cdot8}{2}=112$.'],
    'geo32-foundation-p24': ['The height stays the same, so the area grows by the same percent as the base.',
                             '$90\\cdot1.2=108$. Check: the height is $\\frac{90}{15}=6$, the new base is $18$, and $18\\cdot6=108$.'],
    'geo32-foundation-p25': ['Every length times $k$ means the area times $k^2$.',
                             'The diagonal is multiplied by $1.5$, so the area is multiplied by $1.5^2=2.25$.',
                             'That is an increase of $2.25-1=1.25$, or $125\\%$. Check: diagonal 2 gives area $\\frac{2^2}{2}=2$; diagonal 3 gives $\\frac{3^2}{2}=4.5$.'],
    'geo32-foundation-p26': ['The kite: $S=\\frac{9\\cdot16}{2}=72$.', 'The rectangle: $12\\cdot x=72$, so $x=6$.'],
    'geo32-foundation-p27': ['The diagonals of a parallelogram bisect each other, so they split it into four triangles of equal area.',
                             '$S=4\\cdot11=44$.'],
    'geo32-g066': ['Every rectangle is a parallelogram, every rhombus is a kite, and every square is a rectangle — all three are true.',
                   'A parallelogram does not necessarily have perpendicular diagonals. Example: an $8\\times3$ rectangle is a parallelogram, and its diagonals are not perpendicular.'],
    'geo32-g067': ['Drop EF perpendicular to BC. ABFE and EFCD are rectangles.',
                   'A diagonal splits a rectangle into two equal triangles: $S_{EBF}=S_{ABE}=5$ and $S_{EFC}=S_{ECD}=13$.',
                   '$S_{EBC}=5+13=18$.'],
    'geo32-g068': ['E and G split AD and BC in the same ratio, $2 : 1$. So EG is parallel to AB, and it splits the rectangle into a left part and a right part in the ratio $2 : 1$.',
                   'Let $S_{ECD}=s$. Then $S_{EGC}=s$ (a diagonal halves the right rectangle), the right rectangle is $2s$, and the left rectangle is $4s$.',
                   'FEG stands on the full side EG of the left rectangle, with its tip on AB: $S_{FEG}=2s$. The shaded area is $s+2s=3s$, so the area of ECD is enough.',
                   'The area of AFE or of FBG is not enough: F can be anywhere on AB.'],
    'geo32-g069': ['Triangles ABD and BCD have the same height (the height of the trapezoid). The ratio of their areas equals the ratio of their bases: $4 : 12=1 : 3$.',
                   '$S_{BCD}=3\\cdot14=42$, and the trapezoid is $14+42=56$.',
                   'Or: $\\frac{4h}{2}=14$ gives $h=7$, and $S=\\frac{(4+12)\\cdot7}{2}=56$.'],
    'geo32-g070': ['The rectangle is $7\\cdot5=35$.',
                   'The four white corner triangles have legs 1 and 2, 6 and 2, 2 and 3, and 2 and 3. Their areas are $\\frac{1\\cdot2}{2}=1$, $\\frac{6\\cdot2}{2}=6$, $\\frac{2\\cdot3}{2}=3$ and $3$. Together: $13$.',
                   '$S=35-13=22$.'],
    'geo32-g071': ['Angle sum: $\\angle D=360°-110°-\\alpha-\\beta=250°-\\alpha-\\beta$.',
                   'DE bisects it: $\\angle ADE=125°-\\frac\\alpha2-\\frac\\beta2$.',
                   'Triangle AED: $\\angle AED=180°-\\alpha-\\left(125°-\\frac\\alpha2-\\frac\\beta2\\right)=55°-\\frac\\alpha2+\\frac\\beta2$.',
                   'Check with numbers: $\\alpha=100°$ and $\\beta=70°$ give $\\angle D=80°$, $\\angle ADE=40°$ and $\\angle AED=40°$. Only choice 2 gives $55°-50°+35°=40°$.'],
    'geo32-g072': ['Call the short side of a small rectangle $x$. Four short sides stack up to one long side, so the long side is $4x$.',
                   'The big rectangle is $4x$ by $x+4x+x=6x$. $P=2(4x+6x)=20x=50$, so $x=2.5$.',
                   '$S=4x\\cdot6x=10\\cdot15=150$.'],
    'geo32-advanced-p01': ['Call the longer side $L$. The upper row is $L+2+L$ wide, and the lower row is $4+L+4$ wide.',
                           '$2L+2=L+8$, so $L=6$.'],
    'geo32-advanced-p02': ['EBC stands on the full base BC, with its tip on AD. It is half the rectangle.',
                           'The two corner triangles make the other half: $S_{ABE}+S_{ECD}=19$.', '$S_{ABE}=19-7=12$.'],
    'geo32-advanced-p03': ['In right triangle ABC, $BC=18=2\\cdot AB$. The hypotenuse is twice a leg, so it is a 30-60-90 triangle: $\\angle ACB=30°$ and $\\angle ABC=60°$.',
                           'The angles on leg AB add up to $180°$, and the trapezoid is isosceles: each top angle is $180°-60°=120°$. $\\alpha=120°$.'],
    'geo32-advanced-p04': ['The height of an equilateral triangle with side 8 is $\\frac{8\\sqrt3}{2}=4\\sqrt3$. So $AF=4\\sqrt3$.',
                           'By symmetry, E is above the middle of AD: $FE=\\frac82=4$.', '$S=\\frac{4\\cdot4\\sqrt3}{2}=8\\sqrt3$.'],
    'geo32-advanced-p05': ['$AD=CD$, so triangle ADC is isosceles: $\\angle ACD=\\angle DAC=2t$.',
                           '$AD\\parallel BC$ (Z-angles): $\\angle ACB=\\angle DAC=2t$.',
                           '$\\angle C=2t+2t=4t$, and the base angles are equal: $\\beta=4t$.'],
    'geo32-advanced-p06': ['$BD=3\\sqrt2$ (the diagonal of the square), and it makes a $45°$ angle with BC.',
                           '$\\angle DBF=45°+15°=60°$. BEFD is a rectangle, so $\\angle BDF=90°$.',
                           'Triangle BDF is a 30-60-90 triangle. BD is opposite the $30°$ angle, so $BF=2\\cdot BD=6\\sqrt2$.'],
    'geo32-advanced-p07': ['The kite is symmetric about AC, so $\\angle B=\\angle D$.',
                           '$2\\angle D=360°-3t-t=360°-4t$, so $\\angle ADC=180°-2t$.'],
    'geo32-advanced-p08': ['AED and AEC have the same height from A, and their bases are in the ratio $DE : EC=3 : 1$. So $x : y=3 : 1$.',
                           'The diagonal AC halves the rectangle: $z=x+y$.', 'With $x=3$ and $y=1$: $z=4$. The ratio is $3 : 1 : 4$.'],
    'geo32-advanced-p09': ['The four congruent regions: $49-5\\cdot1=44$.', 'Two of them: $\\frac{44}{2}=22$.'],
    'geo32-advanced-p10': ['Each rectangle is $s$ by $\\frac s2$. Its perimeter: $2\\left(s+\\frac s2\\right)=3s=96$, so $s=32$.', '$P=4\\cdot32=128$.'],
    'geo32-advanced-p11': ['A parallelogram has equal opposite sides. A kite has two pairs of equal adjacent sides.',
                           'Together, all four sides are equal: it is a rhombus. Each side is $\\frac{40}{4}=10$.',
                           'The other statements are true only for a square.'],
    'geo32-advanced-p12': ['$AD\\parallel BC$: the angle between the shallow line and AD equals the angle between that line and CB at C (Z-angles). That angle at C is α.',
                           'The right angle at C is made of α, $28°$ and α: $2\\alpha+28°=90°$, so $\\alpha=31°$.'],
    'geo32-advanced-p13': ['Triangle AFB: $\\angle FAB=\\frac{180°-2p}{2}=90°-p$. Triangle AED: $\\angle EAD=90°-q$.',
                           'The angles around A add up to $360°$: $x+(90°-p)+90°+(90°-q)=360°$.', '$x=90°+p+q$.'],
    'geo32-advanced-p14': ['$BE=DF$, so $AE+FD=AE+EB=AB$.', '$AE+FD+AD=AB+AD=\\frac{34}{2}=17$.', 'Add the cut: $P=17+7=24$.'],
    'geo32-advanced-p15': ['The two small perimeters contain every outer side once and the cut EF twice: $2\\cdot EF=10$, so $EF=5$.',
                           'EF is the height from E to CD: $S=\\frac{14\\cdot5}{2}=35$.'],
    'geo32-advanced-p16': ['The square: $\\frac{30\\cdot10}{3}=100$, so its side is 10.',
                           'Triangle AEC has height $AB=10$ to the base EC: $\\frac{10\\cdot EC}{2}=30$, so $EC=6$.', '$BE=10-6=4$.'],
    'geo32-advanced-p17': ['The inner trapezoid is half of the whole area, with the same height. So the sum of its bases is half of $3a+5a=8a$: it is $4a$.',
                           '$3a+EF=4a$, so $EF=a$.'],
    'geo32-advanced-p18': ['Call $AE=x$. It is the side of the square and also the height of the parallelogram to BC, and $BC=AD=12$.',
                           '$12x=3x^2$. Divide by $3x$ (it is not 0): $x=4$.'],
    'geo32-advanced-p19': ['The four squares have a total perimeter of $4(p+q+r+s)$.',
                           'The shared edges ($r$, $q$ and $2p$ in total) are inside the figure, and each was counted twice. Take away $2(r+q+2p)$.',
                           '$4p+4q+4r+4s-2r-2q-4p=2q+2r+4s$.'],
    'geo32-advanced-p20': ['The tilted side inside the vertical strip is the hypotenuse of a 45-45-90 triangle with leg $4\\sqrt2$. Its length is $4\\sqrt2\\cdot\\sqrt2=8$.',
                           'The height to that side is the width of the tilted rectangle: 6.', '$S=8\\cdot6=48$.'],
    'geo32-advanced-p21': ['Call the sides $a$ and $b$:\n$\\begin{cases} a+b=26 \\\\ a^2+b^2=20^2=400 \\end{cases}$',
                           'Use the identity $(a+b)^2=a^2+2ab+b^2$: $676=400+2ab$, so $2ab=276$.', '$S=ab=138$.'],
    'geo32-advanced-p22': ['Each cut takes $2+2=4$ away from the square\'s perimeter and adds a hypotenuse of $2\\sqrt2$.',
                           '$P=48-4\\cdot4+4\\cdot2\\sqrt2=32+8\\sqrt2$.'],
    'geo32-advanced-p23': ['$\\frac{10\\cdot d}{2}=120$, so the other diagonal is $d=24$.',
                           'The half-diagonals 5 and 12 are the legs of a right triangle: the side is 13 ($5, 12, 13$).', '$P=4\\cdot13=52$.'],
    'geo32-advanced-p24': ['Each outer side is counted once in the four small perimeters, and each cut is counted twice.',
                           '$46+2\\cdot3\\cdot7=46+42=88$.'],
    'geo32-advanced-p25': ['Drop both heights: the difference of the bases, $22-10=12$, splits into two ends of 6.',
                           'Each leg is the hypotenuse of a right triangle with legs 6 and 8: it is 10 ($6, 8, 10$).', '$P=10+22+10+10=52$.'],
    'geo32-advanced-p26': ['The width: $3+8=11$. The height: $2+5=7$.', '$S=11\\cdot7=77$.'],
    'geo32-advanced-p27': ['For any quadrilateral with perpendicular diagonals, $S=\\frac{d_1\\cdot d_2}{2}$ — even when the diagonals do not bisect each other.',
                           '$S=\\frac{14\\cdot9}{2}=63$.'],
}


def _therefore(lines):
    return [re.sub(r', so (?=[$A-Za-z0-9(])', ', therefore ', x) if ', so ' in x else x for x in lines]


def _existing_questions(M):
    for qid, q in M.D['questions'].items():               # stray spaces around stems
        if q.get('topic') == TOPIC and q['stemRich'] != q['stemRich'].strip():
            M.set_q(qid, stem=q['stemRich'].strip())
    for qid, st in STEMS.items():
        M.set_q(qid, stem=st)
    for qid, ex in EXPL.items():
        M.set_q(qid, expl=_therefore(ex))
    _sync_stem_copies(M, list(STEMS))


# ------------------------------------------------------------------------------------------------
# 4. New guided questions (each with a worked-solution video) and the perimeter-tricks lesson
# ------------------------------------------------------------------------------------------------
def _new_guided(M):
    G = GID
    # ---- G1: parallelogram with a special (obtuse) angle ----
    M.new_q(G[0], TOPIC, 'ABCD is a parallelogram. Given:\n' + _cases('AB=10' + CM, 'BC=14' + CM, '\\angle ABC=150°') +
            '\nWhat is the area of the parallelogram (in cm²)?',
            ['$140$', '$70\\sqrt3$', '$70$', '$35$'], 3,
            ['The base is $BC=14$. Drop the height from A. Angle B is obtuse, so the foot H falls on the extension of CB, beyond B.',
             '$\\angle ABH=180°-150°=30°$. In right triangle ABH, the height AH is opposite the $30°$ angle, so it is half the hypotenuse: $AH=\\frac{10}{2}=5$.',
             '$S=BC\\cdot AH=14\\cdot5=70$.'], figure=FIG_G1)
    M.place_q(G[0], LEARN1, after='solve-geo32-g049')
    n1 = _solution(M, G[0], 'solve-' + G[0], 'A parallelogram with a 150° angle', 'Parallelogram Questions', 30,
                   ['A sample question — medium level.', 'An obtuse angle. Where does the height fall?'], [
        ('Extend the base', [
            "ABCD is a parallelogram. AB is 10, BC is 14, and angle B is 150. What is the area?",
            "Area of a parallelogram: base times height. The base BC is 14. We need the height to BC.",
            "Drop it from A. But angle B is obtuse — so the foot falls outside, to the left of B.",
            D('Extend CB beyond B; drop the height from A to H on the extension; mark the right angle'),
            "Extend CB beyond B, and drop the height AH.",
            A("'∠ABH = 180° − 150° = 30°' appears", _R('$\\angle ABH=180°-150°=30°$', 0)),
            "Angle ABH and angle ABC sit on one straight line. 180 minus 150 — 30.",
        ]),
        ('Half the hypotenuse', [
            "Triangle ABH: a right angle and a 30. A golden triangle — 30, 60, 90.",
            "AB is the hypotenuse: 10. The height AH is opposite the 30 — the short leg.",
            A("'AH = 10/2 = 5' appears", _R('$AH=\\frac{10}{2}=5$', 0)),
            "The short leg is half the hypotenuse: 5.",
            A("'S = 14 · 5 = 70' appears", _R('$S=14\\cdot5=70$', 1)),
            "Area: 14 times 5 — 70.",
            D('Circle choice 3'),
            "Choice three.",
        ]),
        ('The traps', [
            A("'30° or 150° → height = half the side' appears", _R('$30°$ or $150°$ $\\Rightarrow$ height $=\\frac12$ side', 0, size=34)),
            "Remember: an angle of 30 — or 150 next to it — and the height is half the sloping side.",
            D('Cross out choice 1'),
            "140? That's 14 times 10 — the sloping side, not the height.",
            D('Cross out choice 2'),
            "70 root 3? That uses the long leg. The height is opposite the 30 — the short leg.",
            D('Cross out choice 4'),
            "35? Someone divided by 2 — that's the triangle formula, not the parallelogram.",
        ]),
    ], FIG_G1)

    # ---- G2: right trapezoid ----
    M.new_q(G[1], TOPIC, 'ABCD is a right trapezoid with $AD\\parallel BC$ and $\\angle ABC=90°$. Given:\n' +
            _cases('AD=9' + CM, 'BC=15' + CM, 'CD=10' + CM) + '\nWhat is the area of the trapezoid (in cm²)?',
            ['$120$', '$96$', '$192$', '$72$'], 2,
            ['Drop the height DE to BC. ABED is a rectangle: $BE=AD=9$, so $EC=15-9=6$.',
             'Right triangle DEC: hypotenuse 10 and leg 6, so the height is $DE=8$ ($6, 8, 10$).',
             '$S=\\frac{(9+15)\\cdot8}{2}=96$.'], figure=FIG_G2)
    M.place_q(G[1], LEARN1, after='solve-geo32-g055')
    n2 = _solution(M, G[1], 'solve-' + G[1], 'A right trapezoid: one height, one triple', 'Trapezoid Questions', 36,
                   ['A sample question — easy-plus.', 'A right trapezoid. Drop one height.'], [
        ('Drop the height', [
            "ABCD is a right trapezoid. AD is 9, BC is 15 and CD is 10. What is its area?",
            "For the area we need the height. AB is a height — but we don't know it.",
            D('Drop the height from D to E on BC; mark the right angle'),
            "Drop a height from D. Now we have a rectangle, ABED, and a right triangle, DEC.",
            A("'BE = AD = 9 → EC = 6' appears", _R('$BE=AD=9\\ \\Rightarrow\\ EC=15-9=6$', 0, size=34)),
            "In the rectangle, BE equals AD: 9. So EC is 15 minus 9 — 6.",
        ]),
        ('A triple, then the area', [
            A("'6 - 8 - 10' appears", _R('$6\\ -\\ 8\\ -\\ 10$', 0, size=44)),
            "Triangle DEC: hypotenuse 10, leg 6. The triple 6, 8, 10 — the height DE is 8.",
            A("'S = (9 + 15) · 8 / 2 = 96' appears", _R('$S=\\frac{(9+15)\\cdot8}{2}=96$', 1)),
            "Area: 9 plus 15 is 24. Times 8, over 2. 12 times 8 — 96.",
            D('Circle choice 2'),
            "Choice two.",
            "The trap: 120 uses CD, 10, as the height. The sloping leg is not the height.",
        ]),
    ], FIG_G2)

    # (Pass 2: G3 midsegment, G4 arrow rule and G5 trapezoid butterfly - q-r26-t32-03/04/05 - removed)

    # ---- perimeter tricks lesson ----
    PER = 'r26-t32-perimeter'
    M.new_video(PER, TOPIC, 'Perimeter Tricks', ['A cut counts twice', 'The staircase', 'A notch adds'], [
        dict(mode='title', title='Perimeter Tricks', script=[
            "Perimeter tricks.", "Three quick rules that turn long perimeter questions into one line."]),
        dict(mode='concept', active=0, title='A cut counts twice', script=[
            A('A rectangle cut into two rectangles appears', VIS(FIG_CUT, w=1000, h=520)),
            "A rectangle, cut into two smaller rectangles.",
            "Add the two small perimeters. Every outside side is counted once —",
            D('Trace the cut twice'),
            "— but the cut belongs to both pieces. It's counted twice.",
            A("'pieces = original + 2 × cut' appears", T('Sum of the pieces $=$ original $+\\ 2\\times$ cut', size=46, x=410, y=650)),
            "So the sum of the pieces is the original perimeter plus two times the cut.",
            "Three cuts? Add two times each cut.",
        ]),
        dict(mode='concept', active=1, title='The staircase', script=[
            A('A staircase outline and its rectangle appear', VIS(FIG_STAIR, w=1000, h=520)),
            "A staircase: all the angles are right angles, and the steps go only one way.",
            D('Push the horizontal steps up and the vertical steps to the right'),
            "Push every horizontal step up to the top line. Push every vertical step out to the side.",
            "Nothing gets longer or shorter — and we get the full rectangle.",
            A("'staircase: P = 2(width + height)' appears", T('Staircase: $P=2(\\text{width}+\\text{height})$', size=46, x=410, y=650)),
            "So the perimeter is the same as the rectangle around it: 2 times, width plus height.",
            "You don't need the length of a single step.",
        ]),
        dict(mode='concept', active=2, title='A notch adds', script=[
            A('A rectangle with a notch appears', VIS(FIG_NOTCH, w=1000, h=520)),
            "Careful — a notch is different.",
            "Push the bottom of the notch back up, and the width is still covered.",
            D('Mark the two walls of the notch'),
            "But the two walls of the notch have nowhere to go. They are extra.",
            A("'notch: + 2 × depth' appears", T('Notch: $P=2(\\text{width}+\\text{height})+2\\times\\text{depth}$', size=40, x=410, y=650)),
            "So a notch adds two times its depth.",
            "Let's try one.",
        ]),
    ], LEARN2, after='solve-geo32-g072')
    M.video(PER)['hybrid']['num'] = 43

    # ---- G6: staircase perimeter ----
    M.new_q(G[5], TOPIC, 'All the angles in the accompanying figure are right angles. The figure is 12 cm wide and 8 cm tall, as marked. '
            'What is its perimeter (in cm)?',
            ['$20$', '$40$', '$96$', 'It cannot be determined from the information given.'], 2,
            ['Push the horizontal steps up to the top line and the vertical steps out to the side. No length changes.',
             'The outline becomes the full $12\\times8$ rectangle: $P=2(12+8)=40$.',
             'The lengths of the single steps are not needed.'], figure=FIG_G6)
    M.place_q(G[5], LEARN2, after=PER)
    n6 = _solution(M, G[5], 'solve-' + G[5], 'A staircase has the perimeter of its rectangle', 'Perimeter Questions', 44,
                   ['A sample question — easy-plus.', 'A staircase. No step lengths needed.'], [
        ('Push the steps out', [
            "All the angles are right angles. The figure is 12 wide and 8 tall. What's the perimeter?",
            "We don't know a single step. Many students stop here and choose \"cannot be determined\".",
            "But it's a staircase.",
            D('Push the horizontal steps up and the vertical steps to the right'),
            "Push every horizontal step up — together they cover the top: 12. Push every vertical step to the right — together they cover the side: 8.",
            A("'P = 2(12 + 8) = 40' appears", _R('$P=2(12+8)=40$', 0)),
            "The perimeter is the full rectangle's: 2 times, 12 plus 8 — 40.",
            D('Circle choice 2'),
            "Choice two.",
            "96 is 12 times 8 — that's an area, not a perimeter.",
        ]),
    ], FIG_G6)

    # ---- G7: perimeter + diagonal -> area (identity; work back from the answers) ----
    M.new_q(G[6], TOPIC, 'A rectangle has a perimeter of 34 cm, and its diagonal is 13 cm long. What is its area (in cm²)?',
            ['$60$', '$65$', '$120$', '$30$'], 1,
            ['Call the sides $a$ and $b$:\n$\\begin{cases} a+b=17 \\\\ a^2+b^2=13^2=169 \\end{cases}$',
             'Use the identity $(a+b)^2=a^2+2ab+b^2$: $289=169+2ab$, so $2ab=120$ and $ab=60$.',
             'Faster: 13 suggests the triple $5, 12, 13$. Sides 5 and 12 give $P=2(5+12)=34$. It fits, and $S=5\\cdot12=60$.'],
            figure=FIG_G7)
    M.place_q(G[6], LEARN2, after='solve-' + G[5])
    n7 = _solution(M, G[6], 'solve-' + G[6], 'Perimeter and diagonal give the area', 'Perimeter Questions', 44,
                   ['A sample question — medium-plus.', 'Perimeter and diagonal — the area without the sides.'], [
        ('Method 1 · The identity', [
            "A rectangle: perimeter 34, diagonal 13. What's the area?",
            "Call the sides a and b.",
            A("'a + b = 17, a² + b² = 169' appears", _R('$\\begin{cases} a+b=17 \\\\ a^2+b^2=169 \\end{cases}$', 0, size=36)),
            "Half the perimeter: a plus b is 17. Pythagoras on the diagonal: a squared plus b squared is 169.",
            "We want a times b. Remember the identity: a plus b, squared, is a squared plus 2ab plus b squared.",
            A("'17² = 169 + 2ab' appears", _R('$17^2=169+2ab$', 1)),
            "17 squared is 289. So 289 equals 169 plus 2ab.",
            A("'2ab = 120 → ab = 60' appears", _R('$2ab=120\\ \\Rightarrow\\ ab=60$', 2)),
            "2ab is 120. The area, ab, is 60.",
            D('Circle choice 1'),
            "Choice one.",
        ]),
        ('Method 2 · Work back from the answers', [
            "The psychometric way. A diagonal of 13 — that smells like a triple: 5, 12, 13.",
            A("'5, 12 → P = 2(5 + 12) = 34' appears", _R('$5,\\ 12\\ \\Rightarrow\\ P=2(5+12)=34$', 0, size=36)),
            "Try sides 5 and 12. The perimeter: 2 times 17 — 34. It matches!",
            "So the area is 5 times 12 — 60.",
            "The traps: 120 is 2ab — you forgot to divide by 2. 30 is only half the rectangle. 65 uses the diagonal as a side.",
        ]),
    ], FIG_G7)

    # ---- sidebars of the groups the new questions joined ----
    Qn = lambda *ns: ['Question %d' % k for k in ns]
    _set_group(M, ['solve-geo32-g048', 'solve-geo32-g049', 'solve-' + G[0]], Qn(3, 4, n1))
    _set_group(M, ['solve-geo32-g055', 'solve-' + G[1]], Qn(7, n2))
    M.video('solve-geo32-g055')['beats'][0]['title'] = 'Trapezoid Questions'
    _set_group(M, ['solve-' + G[5], 'solve-' + G[6]], Qn(n6, n7))


# ------------------------------------------------------------------------------------------------
# 5. Memory cards
# ------------------------------------------------------------------------------------------------
def _cards(M):
    c = M.card('mem-quad-area')
    rows = c['tables'][0]['rows']
    for r in rows:
        if r[0] == 'Parallelogram': r[2] = 'the height, not the sloping side · angle $30°$: $h=\\frac12$ side'
    rows.append(['Any quadrilateral with $\\perp$ diagonals', '$\\frac{d_1\\cdot d_2}{2}$', 'even if the diagonals do not bisect each other'])
    c['tips'] = ['Trapezoid: drop both heights — a rectangle in the middle, triangles at the ends. Right trapezoid: one height is enough.',
                 'Dropped a height? Look for Pythagoras, a triple, or a $30°$/$45°$/$60°$ triangle.',
                 'Every length $\\times k$ $\\Rightarrow$ area $\\times k^2$ (diagonal $+50\\%$ $\\Rightarrow$ area $\\times2.25$). Only the base grows? Area $\\times$ the same factor.',
                 'Rectangle with the perimeter and the diagonal: $(a+b)^2=a^2+b^2+2ab$ gives $ab$ — or try a triple.']

    c = M.card('mem-quad-family')
    rows = c['tables'][0]['rows']
    for r in rows:
        if r[0] == 'Rectangle': r[3] = 'equal · bisect each other — not necessarily $\\perp$, not necessarily angle bisectors'
        if r[0] == 'Parallelogram': r[3] = 'bisect each other — that\'s all (not necessarily equal or $\\perp$)'
        if r[0] == 'Rhombus': r[3] = '$\\perp$ · bisect each other · bisect the angles — not necessarily equal'
        if r[0] == 'Kite': r[2] = 'the main diagonal bisects the angles between the equal sides'
        if r[0] == 'Trapezoid': r[1] = 'exactly one pair of parallel sides (the bases)'
        if r[0] == 'Isosceles trapezoid': r[2] = 'base angles equal · opposite angles sum $180°$'
    c['tips'] = ['Who is also who: a square is a rectangle AND a rhombus; a rectangle and a rhombus are parallelograms; a rhombus is also a kite. Down the family tree a shape only gains properties.',
                 '"Not necessarily": a property of a special shape (a square) is not a property of the general one (a rectangle).',
                 'Not sure about a property? Sketch an extreme version — very wide and very low — and look.',
                 'Rhombus: symmetric right–left AND top–bottom. Kite: right–left only.',
                 'An angle bisector in a parallelogram cuts off an isosceles triangle.',
                 'Midpoints of the sides: of a rectangle — a rhombus; of a square — a square with half the area.',
                 'Right trapezoid: always two right angles.']

    M.new_card('mem-r26-t32-perimeter', TOPIC, LEARN2, {
        'title': 'Perimeter tricks',
        'intro': 'Perimeter questions with many small pieces usually need only one of these rules.',
        'tables': [{'title': '', 'head': ['Situation', 'Perimeter'], 'rows': [
            ['A shape cut into pieces', 'sum of the pieces $=$ original $+\\ 2\\times$ each cut'],
            ['!Staircase (all right angles, steps one way)', '$2(\\text{width}+\\text{height})$ — like its rectangle'],
            ['Rectangular notch cut into a side', '$2(\\text{width}+\\text{height})+2\\times\\text{depth}$'],
            ['Shapes glued along an edge', 'sum of the perimeters $-\\ 2\\times$ each shared edge']]}],
        'tips': ['Area and perimeter are different questions: $12\\times8$ is an area, $2(12+8)$ is a perimeter.']},
        after='solve-' + GID[6])


# ------------------------------------------------------------------------------------------------
# 6. Practice: remove fillers and repeats, add the new rules and exam-hard items, order easy -> hard
# ------------------------------------------------------------------------------------------------
NEW_PRACTICE = [
    # (section, stem, choices, correct, solution, figure)
    (FOUND, 'ABCD is a right trapezoid with $AD\\parallel BC$ and $AB\\perp BC$. Given:\n' + _cases('AD=5' + CM, 'BC=11' + CM, 'AB=8' + CM) +
     '\nWhat is the perimeter of the trapezoid (in cm)?', ['$30$', '$32$', '$34$', '$36$'], 3,
     ['Drop the height DE to BC. ABED is a rectangle: $DE=AB=8$ and $BE=AD=5$, so $EC=11-5=6$.',
      'Right triangle DEC: legs 6 and 8, so $CD=10$ ($6, 8, 10$).', '$P=5+11+8+10=34$.'], FIG_Q08),
    (FOUND, 'ABCD is a parallelogram. Given:\n' + _cases('AB=7' + CM, 'BC=10' + CM, '\\angle ABC=30°') +
     '\nWhat is the area of the parallelogram (in cm²)?', ['$70$', '$35$', '$35\\sqrt3$', '$17.5$'], 2,
     ['Drop the height from A to BC. It is opposite the $30°$ angle in a right triangle with hypotenuse $AB=7$, so it is half of it: $h=3.5$.',
      '$S=BC\\cdot h=10\\cdot3.5=35$.'], None),
    (FOUND, 'The midsegment of a trapezoid (the segment that joins the midpoints of its legs) is 9 cm long. One base is 4 cm longer than the other. '
     'What is the length of the longer base (in cm)?', ['$13$', '$11$', '$7$', '$9$'], 2,
     ['The midsegment is the average of the bases: $\\frac{b+(b+4)}{2}=9$.', '$2b+4=18$, so $b=7$, and the longer base is $7+4=11$.',
      'Check: $\\frac{7+11}{2}=9$.'], None),
    (FOUND, 'ABCD is a concave quadrilateral. Based on the information in the accompanying figure, what is x?',
     ['$200°$', '$160°$', '$20°$', '$135°$'], 2,
     ['The angle in the notch equals the sum of the other three angles: $x=45°+90°+25°=160°$.',
      'Why: the inside angle at D is $360°-x$, and $45°+90°+25°+(360°-x)=360°$. Therefore $x=160°$.'], FIG_Q11),
    (FOUND, 'The length and the width of a rectangle are each increased by 10%. By what percent does its area increase?',
     ['$20\\%$', '$21\\%$', '$10\\%$', '$121\\%$'], 2,
     ['Every length times $1.1$ means the area times $1.1^2=1.21$: an increase of $21\\%$.',
      'Check with numbers: a $10\\times20$ rectangle (area 200) becomes $11\\times22$ (area 242). $\\frac{42}{200}=21\\%$.'], None),
    (FOUND, 'The midpoints of the sides of a square with side 10 cm are joined, forming a new quadrilateral. What is the area of the new quadrilateral (in cm²)?',
     ['$25$', '$50$', '$75$', '$100$'], 2,
     ['The new quadrilateral is a square. Its diagonals join the midpoints of opposite sides, so each diagonal is 10.',
      '$S=\\frac{10\\cdot10}{2}=50$ — half of the big square.',
      'Or: the four corner triangles are $4\\cdot\\frac{5\\cdot5}{2}=50$, and $100-50=50$.'], None),
    (FOUND, 'In trapezoid ABCD, $AD\\parallel BC$, and the diagonals meet at O. The area of triangle ABC is 30 cm², and the area of triangle BOC is 18 cm². '
     'What is the area of triangle COD (in cm²)?', ['$18$', '$12$', '$30$', '$6$'], 2,
     ['$S_{AOB}=S_{ABC}-S_{BOC}=30-18=12$.',
      'Triangles ABC and DBC have the same base BC and the same height, so their areas are equal. Take away BOC from both: $S_{COD}=S_{AOB}=12$.'], FIG_BF_P),
    (ADVP, 'In trapezoid ABCD, $AD\\parallel BC$, and the diagonals meet at O. The area of triangle AOD is 4 cm², and the area of triangle BOC is 25 cm². '
     'What is the area of the trapezoid (in cm²)?', ['$29$', '$39$', '$49$', '$58$'], 3,
     ['The two side triangles have equal areas: $S_{AOB}=S_{COD}=s$.',
      'AOD and AOB have the same height from A (their bases OD and OB are on BD): $\\frac{s}{4}=\\frac{OB}{OD}$. BOC and COD have the same height from C: $\\frac{25}{s}=\\frac{OB}{OD}$.',
      '$\\frac s4=\\frac{25}{s}$, so $s^2=100$ and $s=10$.', '$S=4+25+10+10=49$.'], FIG_BF_P),
    (ADVP, 'ABCD is a trapezoid with $AD\\parallel BC$. Which of the following data is sufficient to determine its area?',
     ['The lengths of its two legs and its height', 'The length of its midsegment and its height', 'The lengths of its two diagonals',
      'The lengths of its two bases'], 2,
     ['$S=\\frac{AD+BC}{2}\\cdot h=\\text{midsegment}\\cdot h$. The midsegment and the height give the area directly.',
      'The legs and the height do not fix the bases (the whole trapezoid can be wider or narrower). The diagonals alone or the bases alone do not give the height.'], None),
    (ADVP, 'The accompanying figure was made by cutting a rectangular notch, 3 cm deep, out of the top side of a 10 cm by 7 cm rectangle. '
     'All the angles are right angles. What is the perimeter of the figure (in cm)?', ['$34$', '$37$', '$40$', '$46$'], 3,
     ['Push the bottom of the notch back up: the horizontal pieces still cover the width twice, and the outer sides cover the height twice. That is $2(10+7)=34$.',
      'The two walls of the notch are extra: $3+3=6$.', '$P=34+6=40$.'], FIG_Q17),
    (ADVP, 'ABCD is a parallelogram. Given:\n' + _cases('AB=6' + CM, 'BC=10' + CM, '\\angle ABC=60°') +
     '\nWhat is the area of the parallelogram (in cm²)?', ['$30$', '$60$', '$30\\sqrt3$', '$15\\sqrt3$'], 3,
     ['Drop the height from A to BC: a 30-60-90 triangle with hypotenuse $AB=6$. The leg opposite $30°$ is 3, and the height, opposite $60°$, is $3\\sqrt3$.',
      '$S=10\\cdot3\\sqrt3=30\\sqrt3$.'], None),
    (ADVP, 'ABCD is a concave quadrilateral, as in the accompanying figure. Angles A and C are both α, angle B is 50°, and the angle ADC marked in the notch is 110°. '
     'What is α?', ['$30°$', '$60°$', '$20°$', '$35°$'], 1,
     ['The angle in the notch equals the sum of the other three angles: $\\alpha+50°+\\alpha=110°$.', '$2\\alpha=60°$, so $\\alpha=30°$.'], FIG_Q19),
    (ADVP, 'ABCD is a right trapezoid with $AD\\parallel BC$ and $\\angle A=\\angle B=90°$. Given:\n' + _cases('AD=4' + CM, 'BC=10' + CM, '\\angle C=45°') +
     '\nWhat is the area of the trapezoid (in cm²)?', ['$84$', '$42$', '$56$', '$30$'], 2,
     ['Drop the height DE to BC. ABED is a rectangle: $BE=AD=4$, so $EC=10-4=6$.',
      'Triangle DEC has a right angle and a $45°$ angle, so it is isosceles: $DE=EC=6$.', '$S=\\frac{(4+10)\\cdot6}{2}=42$.'], FIG_Q20),
    (ADVP, 'The midpoints of the sides of a rectangle with sides 6 cm and 8 cm are joined, forming a quadrilateral. What is the perimeter of this quadrilateral (in cm)?',
     ['$14$', '$20$', '$24$', '$28$'], 2,
     ['The new quadrilateral is a rhombus. Each side is the hypotenuse of a corner triangle with legs $\\frac62=3$ and $\\frac82=4$.',
      'Each side is 5 ($3, 4, 5$), so $P=4\\cdot5=20$.'], None),
]


# Pass 2: these added practice items are removed (arrow rule, midsegment, butterfly) - teacher's plan
REMOVED_PRACTICE = {'q-r26-t32-10', 'q-r26-t32-11', 'q-r26-t32-14', 'q-r26-t32-15', 'q-r26-t32-16', 'q-r26-t32-19'}

# Pass 2: original foundation questions restored, with the text clean-up only
RESTORED = {
    'geo32-foundation-p05': dict(expl=[
        'The side of the triangle is $\\frac{216}{3}=72$.',
        'This is the perimeter of the square, therefore each side of the square is $\\frac{72}{4}=18$.']),
    'geo32-foundation-p08': dict(expl=[
        'A diagonal is the hypotenuse of a right triangle whose legs are sides of the square, therefore it is longer than a side '
        '($d=s\\sqrt2$).',
        'Each route has four segments. Replacing a side-length segment with a diagonal-length segment makes the route longer, '
        'therefore four sides is the shortest route.']),
    'geo32-foundation-p12': dict(expl=[
        'Both horizontal lines are perpendicular to the right vertical line, therefore they are parallel.',
        'The downward sloping line makes $32°$ with either horizontal line.',
        'Its perpendicular therefore makes $90°-32°=58°$ with the horizontal line: $\\alpha=58°$.']),
    'geo32-foundation-p19': dict(
        stem='ABCD is a kite, and its diagonals intersect at O. Given:\n' +
             _cases('AB=AD=17' + CM, 'CB=CD', 'BO=8' + CM, 'OC=9' + CM) + '\nWhat is its area (in cm²)?',
        expl=['$OD=BO=8$, therefore $BD=8+8=16$.',
              'Right triangle ABO: $8, 15, 17$, therefore $AO=15$ and $AC=15+9=24$.',
              '$S=\\frac{16\\cdot24}{2}=192$.']),
    'geo32-foundation-p22': dict(expl=[
        'The half-diagonals are $\\frac{16}{2}=8$ and $\\frac{30}{2}=15$, and they are perpendicular.',
        'They form a right triangle whose hypotenuse is a side of the rhombus: $8, 15, 17$, therefore the side is $17$.',
        '$P=4\\cdot17=68$.']),
}


def _practice(M):
    for qid, kw in RESTORED.items():
        M.set_q(qid, **kw)
    for qid, (sec, stem, ch, cor, ex, fig) in zip(PID, NEW_PRACTICE):
        if qid in REMOVED_PRACTICE: continue
        M.new_q(qid, TOPIC, stem, ch, cor, _therefore(ex), figure=fig)
        M.place_q(qid, sec)
    f = lambda *k: ['geo32-foundation-p%02d' % x for x in k]
    a = lambda *k: ['geo32-advanced-p%02d' % x for x in k]
    p = lambda *k: ['q-r26-t32-%02d' % x for x in k]
    M.practice_order(FOUND, f(13, 14, 5, 8, 26, 27, 18) + f(9, 4, 12, 3, 2, 17, 11) + p(13, 9) + f(22, 24) + p(12) +
                     f(25, 21, 23, 19) + p(8) + f(16) + f(6, 15, 10, 7, 20, 1))
    M.practice_order(ADVP, a(26, 9, 23, 16, 25, 2, 7, 11) + a(3, 5) + p(20, 21) + a(12) + p(18) + a(13, 4, 6, 10, 1, 24, 15, 14) +
                     p(17) + a(19, 22, 8, 17, 18, 20, 21, 27))


# ------------------------------------------------------------------------------------------------
# 7. Pass 2: summary lessons - one right before each practice section
# ------------------------------------------------------------------------------------------------
def _b(label, tex, size=40):
    """A board line that pops in (label = what the teacher sees in the script)."""
    return A("'%s' appears" % label, T(tex, size=size))


def _summary_video(M, vid, section, intro, slides):
    last = [f['ref'] for f in M.D['flow'] if f['section'] == section][-1]
    beats = [dict(mode='title', title='Summary', script=intro)]
    beats += [dict(mode='concept', title=t, active=k, script=sc) for k, (t, sc) in enumerate(slides)]
    M.new_video(vid, TOPIC, 'Summary', [s[0] for s in slides], beats, section, after=last)


def _summaries(M):
    # ---- before the foundation practice: everything taught in "Learn and try" ----
    _summary_video(M, 'r26-t32-summary', LEARN1, [
        'A quick summary before the practice.',
        'Everything important about quadrilaterals — in about three minutes.'], [
        ('The family', [
            _b('Angle sum 360°', 'Any quadrilateral: the angles add up to $360°$'),
            'Every quadrilateral — even one that bends inward — has angles that add up to 360.',
            _b('Down the tree: all the properties above', 'Down the tree: all the properties of the shapes above'),
            'A square is a rectangle AND a rhombus. A rectangle and a rhombus are parallelograms. A rhombus is also a kite.',
            _b('Up the tree: not necessarily', 'Up the tree: "not necessarily"'),
            'Going down, a shape only gains properties. Going up — careful: a rectangle is not necessarily a square.']),
        ('The diagonals', [
            _b('Square: all yes', 'Square: equal · bisect each other · $\\perp$ · bisect the angles'),
            'A square: every diagonal property — yes.',
            _b('Rectangle: equal · Parallelogram: bisect each other', 'Rectangle: equal, bisect each other · Parallelogram: bisect each other — that\'s all', size=36),
            'A rectangle: equal, and they bisect each other. A parallelogram: they only bisect each other.',
            _b('Rhombus: ⊥, bisect the angles · Kite: main diagonal = symmetry line', 'Rhombus: $\\perp$, bisect the angles · Kite: main diagonal $=$ symmetry line', size=36),
            'A rhombus: perpendicular, and they bisect the angles. A kite: the main diagonal is its line of symmetry.']),
        ('Angles', [
            _b('Parallelogram: opposite equal, adjacent 180°', 'Parallelogram: opposite angles equal · adjacent sum $180°$'),
            'In a parallelogram, opposite angles are equal, and two neighbors add up to 180.',
            _b('Trapezoid: angles on one leg 180°', 'Trapezoid: the angles on one leg sum $180°$'),
            'In a trapezoid, the two angles on the same leg add up to 180. Isosceles trapezoid: the base angles are equal.',
            _b('Bisector in a parallelogram → isosceles triangle', 'Bisector in a parallelogram $\\to$ an isosceles triangle'),
            'And an angle bisector in a parallelogram cuts off an isosceles triangle.']),
        ('Area formulas', [
            _b('Square a² or d²/2 · Rectangle ab', 'Square: $a^2$ or $\\dfrac{d^2}{2}$ · Rectangle: $a\\cdot b$'),
            'Square: side squared — or the diagonal squared, over 2. Diagonal 8? 64 over 2 — 32.',
            _b('Parallelogram a · h', 'Parallelogram: $a\\cdot h$'),
            'Parallelogram: base times height.',
            _b('Rhombus, kite: d₁ · d₂ / 2', 'Rhombus, kite ($\\perp$ diagonals): $\\dfrac{d_1\\cdot d_2}{2}$'),
            'Rhombus and kite: the diagonals multiplied, over 2. Diagonals 16 and 5 — 40.',
            _b('Trapezoid (a + b) · h / 2', 'Trapezoid: $\\dfrac{(a+b)\\cdot h}{2}$'),
            'Trapezoid: the sum of the bases, times the height, over 2.']),
        ('The height', [
            _b('The height, not the sloping side', 'The height — not the sloping side'),
            'The height is perpendicular to the base. The sloping side is not the height.',
            _b('30°: h = half the side', '$30°$: $h=\\frac{\\text{side}}{2}$ · sides $9,\\ 8$: $S=9\\cdot4=36$'),
            'A 30-degree angle? The height is half the sloping side. Sides 9 and 8: the height is 4, the area 36.',
            _b('45°: side/√2 · 60°: side/2 · √3', '$45°$: $h=\\frac{\\text{side}}{\\sqrt2}$ · $60°$: $h=\\frac{\\text{side}}{2}\\cdot\\sqrt3$'),
            'With 45: the side over root 2. With 60: half the side, times root 3. An angle of 150? Look at the 30 next to it.']),
        ('Drop a height', [
            _b('Trapezoid: a rectangle + triangles', 'Trapezoid: a rectangle in the middle, triangles at the ends', size=38),
            'A trapezoid? Drop the heights: a rectangle in the middle, right triangles at the ends.',
            _b('Then: Pythagoras, a triple, or 30°/45°/60°', 'Then: Pythagoras, a triple, or a $30°$/$45°$/$60°$ triangle', size=38),
            'Then look for Pythagoras, a triple, or a special triangle.',
            'Bases 6 and 18, and a sloping leg 15: the piece at the end is 12, so the height is 9. The area: 24 times 9, over 2 — 108.']),
        ('Scale it up', [
            _b('Every length × k → area × k²', 'Every length $\\times k$ $\\Rightarrow$ area $\\times k^2$'),
            'Every length times k? The area times k squared.',
            _b('Diagonal +20% → area × 1.44', 'Diagonal $+20\\%$: $1.2^2=1.44$ $\\Rightarrow$ area up $44\\%$'),
            'The diagonal of a square grows by 20 percent? The area grows times 1.44 — up 44 percent.',
            'Only the base grows, and the height stays? Then the area grows by the same factor as the base.']),
        ('In questions', [
            _b('The name → its properties', 'The shape\'s name $\\to$ its properties'),
            'In a question, the name of the shape gives you its properties. Write them on the figure.',
            _b('Look for a useful triangle', 'Look for a useful triangle — or equal areas'),
            'Then look for a useful triangle: a silver triangle in a square, an equilateral triangle in a rhombus with a 60.',
            'The diagonals of a parallelogram split it into four triangles of equal area.',
            'Several ways to the answer? Learn them all — on the exam, take the first one you see.']),
        ('Before you practice', [
            'Before you practice, ask yourself:',
            _b('What does the name promise — and what not?', 'What does the name promise — and what is only "not necessarily"?', size=36),
            _b('Is this the height, or a sloping side?', 'Is this the height — or a sloping side?', size=36),
            _b('Can I drop a height and get a special triangle?', 'Can I drop a height and get a triple or a special triangle?', size=36),
            _b('Did all the lengths grow, or only one?', 'Did all the lengths grow — or only one?', size=36),
            'The traps: a sloping side used as the height, forgetting to divide by 2 in the diagonal formula, and a property of a square given to a rectangle.',
            'Good luck.']),
    ])

    # ---- before the advanced practice: the methods of "Further guided examples" ----
    _summary_video(M, 'r26-t32-summary-2', LEARN2, [
        'A quick summary before the advanced practice.',
        'The ideas from the last examples — in about three minutes.'], [
        ('Not necessarily', [
            _b('Check each statement against the definition', 'Check each statement against the definition'),
            '"Not necessarily true" questions: check every statement against the definitions.',
            _b('Not sure? Sketch an extreme version', 'Not sure? Sketch an extreme version — very wide and very low', size=38),
            'Not sure? Sketch an extreme version of the shape — very wide and very low — and look.']),
        ('Equal halves', [
            _b('A diagonal: two equal halves', 'A diagonal splits a parallelogram into two equal halves', size=38),
            'A diagonal splits a parallelogram — a rectangle, a rhombus, a square — into two equal halves.',
            _b('Triangle on the full base, tip on the opposite side = 1/2', 'Triangle on the full base, tip on the opposite side $=\\frac12$', size=38),
            'A triangle on the full base, with its tip on the opposite side, is half the shape. The white parts are the other half.',
            _b('On 1/3 of the base: 1/3 × 1/2 = 1/6', 'On $\\frac13$ of the base: $\\frac13\\times\\frac12=\\frac16$'),
            'On a third of the base? A third of a half — one sixth.']),
        ('Area ratios', [
            _b('Same height: area ratio = base ratio', 'Same height: area ratio $=$ base ratio'),
            'Two triangles with the same height? The area ratio is the base ratio.',
            _b('Bases 3 and 12: 7 and 28 → 35', 'Bases $3$ and $12$: $7$ and $4\\cdot7=28$ $\\Rightarrow$ $35$'),
            'A trapezoid with bases 3 and 12, cut by a diagonal. The top triangle is 7 — the bottom one is 4 times as much, 28. Together: 35.']),
        ('Shaded areas', [
            _b('Subtract: known shape − white', 'Subtract: a shape you know $-$ the white'),
            'Shaded area? Approach one: take a shape you know, and subtract the white. 60 minus 24 — 36.',
            _b('Or: break it into familiar pieces', 'Or: break it into familiar pieces'),
            'Approach two: break the shaded area into familiar pieces — by completions or by symmetry.',
            'Completions: pair only pieces that truly complete each other. A guess by eye is not a method.']),
        ('Letters and hidden ratios', [
            _b('Angles with letters? Plug in numbers', 'Angles with letters? Plug in numbers'),
            'Angles with letters in the answers? Solve it — or plug in numbers and check every choice.',
            _b('Congruent rectangles: find the hidden ratio', 'Congruent rectangles: find the hidden ratio first'),
            'Congruent rectangles? Read the hidden ratio off the figure. Then one unknown, x, is enough.',
            'And check from the answers: plug one back into the figure and test the number you were given.']),
        ('Perimeter tricks', [
            _b('A cut counts twice', 'Sum of the pieces $=$ original $+\\ 2\\times$ cut'),
            'Cut a shape into pieces? The cut belongs to both pieces — it counts twice.',
            _b('Staircase: P = 2(width + height)', 'Staircase: $P=2(\\text{width}+\\text{height})$ · $2(9+6)=30$'),
            'A staircase has the perimeter of its rectangle: 9 wide and 6 tall — 30.',
            _b('Notch: + 2 × depth', 'Notch: $+\\ 2\\times\\text{depth}$'),
            'A notch is different: its two walls are extra — add two times its depth.']),
        ('Perimeter and diagonal', [
            _b('(a + b)² = a² + b² + 2ab', '$(a+b)^2=a^2+b^2+2ab$'),
            'A rectangle with the perimeter and the diagonal? You don\'t need the sides.',
            _b('14² = 100 + 2ab → ab = 48', '$14^2=100+2ab$ $\\Rightarrow$ $ab=48$'),
            'Perimeter 28: a plus b is 14. Diagonal 10: a squared plus b squared is 100. 196 is 100 plus 2ab — the area is 48.',
            'Or try a triple: 6, 8, 10. The perimeter is 28 — it fits.']),
        ('Before you practice', [
            'Before you practice, ask yourself:',
            _b('Same base or same height anywhere?', 'Same base or same height anywhere? Then equal areas or a ratio.', size=36),
            _b('Subtract the white, or break it up?', 'Subtract the white — or break the shape into pieces?', size=36),
            _b('Letters in the answers? Plug in numbers.', 'Letters in the answers? Plug in numbers.', size=36),
            _b('Perimeter or area?', 'Is it a perimeter or an area?', size=36),
            'The traps: pairing pieces by eye, "same area" taken as "congruent", and an area answer to a perimeter question.',
            'Good luck.']),
    ])


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
    # --- Perimeter Tricks (r26-t32-perimeter): slide 3 "The staircase" is taught again by the next question video,
    #     solve-q-r26-t32-06 (push the steps out; P = 2 × (width + height); no step length needed).
    #     "A cut counts twice" and "A notch adds" stay: no question video teaches them.
    _cr_cut(M, 'r26-t32-perimeter', [3])
    _cr_say(M, 'r26-t32-perimeter', 1, 'Three quick rules',
            'Quick rules that turn long perimeter questions into one line. Two here — and one more in the question.')
    _cr_say(M, 'r26-t32-perimeter', 3, 'Careful — a notch is different.', 'A notch: the border goes in, and comes back out.')
    _cr_say(M, 'r26-t32-perimeter', 3, "Let's try one.", "Now a question.")


# ======================================================================================================
# 2026-10-06 renumber pass (runs LAST). The English course must not look like the Hebrew one: every Hebrew-derived
# question (guided geo32-g044 ... g072, practice geo32-foundation-p01 ... p20 and geo32-advanced-p01 ... p20) gets new
# numbers (letter-only items: new letters / names and a new choice order). Idea, trap, level and methods stay.
# Every guided solution video is rewritten to match (speech, draw cues, board items, the question figure copies).
# Figures whose shape depends on the numbers are redrawn; the others get new labels. Practice clean-up 62 -> 48.
# Nothing in topic 32 is recorded (checked ~/Documents/Course.recordings 2026-10-06).
# ======================================================================================================
import copy as _copy

RN_RECORDED = set()
_RN_W = {'one': 1, 'two': 2, 'three': 3, 'four': 4}
_RN_N = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}


def _rn_relabel(svg, mp, aria=None):
    """Change the text of figure labels (whole text nodes, all at once - no chained replacements)."""
    out = re.sub(r'(<text[^>]*>)([^<]*)(</text>)', lambda m: m.group(1) + mp.get(m.group(2), m.group(2)) + m.group(3), svg)
    for a, b in (aria or []):
        assert a in out, a
        out = out.replace(a, b)
    return out


def _rn_vb(svg):
    return re.search(r'viewBox="([^"]*)"', svg).group(1)


def _rn_fig(M, qid, mp=None, aria=None, svg=None):
    """New question figure: relabel (mp) or replace (svg). The copies on the solution-video slides follow
    (a replaced figure keeps the copy's own crop, since all figures share the 640 x 360 coordinates)."""
    q = M.q(qid)
    old = q['questionVisual']['svg']
    new = svg if svg is not None else _rn_relabel(old, mp, aria)
    if svg is not None and mp: new = _rn_relabel(new, mp)
    M.set_q(qid, figure=new)
    for v in M.D['videos'].values():
        for b in v.get('beats', []):
            for it in b.get('items', []):
                if it.get('k') == 'q' and it.get('qid') == qid and isinstance(it.get('fig'), dict):
                    s = it['fig']['svg']
                    if svg is not None:
                        s2 = re.sub(r'viewBox="[^"]*"', 'viewBox="%s"' % _rn_vb(s), new, count=1)
                    else:
                        s2 = _rn_relabel(s, mp, aria)
                    it['fig']['svg'] = s2; M.touched_videos.add(v['id'])


def _rn_q(M, qid, stem=None, choices=None, correct=None, expl=None):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_choices(M, vid, perm):
    """Old choice number -> new choice number in every 'choice N' / 'Choice four' / 'choices 1 and 4' of a video."""
    def tok(m):
        t = m.group(0)
        if t.isdigit(): return str(perm[int(t)])
        w = _RN_N[perm[_RN_W[t.lower()]]]
        return w.capitalize() if t[0].isupper() else w
    def fix(s):
        return re.sub(r'\b([Cc]hoices?)((?:\s*(?:,|and)?\s*\b(?:[1-4]|one|two|three|four|One|Two|Three|Four)\b)+)',
                      lambda m: m.group(1) + re.sub(r'\b([1-4]|one|two|three|four|One|Two|Three|Four)\b', tok, m.group(2)), s)
    for b in M.video(vid)['beats']:
        for l in b['lines']:
            for k in ('say', 'draw'):
                if k in l: l[k] = fix(l[k])
    M.touched_videos.add(vid)


def _rn_sub(M, vid, pairs):
    """Exact substring replacements in a video's spoken / drawn lines, labels and board items (each must hit)."""
    v = M.video(vid)
    for old, new in pairs:
        hit = False
        for b in v['beats']:
            for l in b['lines']:
                for key in ('say', 'draw', 'label'):
                    if key in l and old in l[key]: l[key] = l[key].replace(old, new); hit = True
            for it in b['items']:
                if it.get('t') and old in it['t']: it['t'] = it['t'].replace(old, new); hit = True
        assert hit, (vid, old)
    M.touched_videos.add(vid)


def _rn_guided(M, qid, stem, choices, correct, expl, perm, pairs, fig=None, svg=None, aria=None):
    if qid in RN_RECORDED: return
    _rn_q(M, qid, stem, choices, correct, expl)
    if fig is not None or svg is not None: _rn_fig(M, qid, fig, aria, svg)
    vid = 'solve-' + qid
    if perm: _rn_choices(M, vid, perm)
    _rn_sub(M, vid, pairs)
    _sync_stem_copies(M, [qid])


# ---------------- redrawn figures (same style as the base figures: 640 x 360, ink / teal / fill) ----------------
def _rn_txt(x, y, s, size=20):
    return _t(x, y, s, size=size)


def _rn_g048():
    """review 2026-10-06: drawn to the new split (B = 5α = 70°, so 3α = 42°; C = 5β = 110°, so 3β = 66°; x = 72°)."""
    A_, B_, C_, D_ = (291.283, 58.333), (202.717, 301.667), (348.717, 301.667), (437.283, 58.333)
    E_ = _cross(B_, _pt(B_, 100, -42), C_, _pt(C_, 100, -114))
    b = _poly([A_, B_, C_, D_]) + _abcd(A_, B_, C_, D_, [(-14, -16), (-14, 16), (14, 16), (14, -16)])
    b += _line(B_, E_, TEAL) + _line(C_, E_, TEAL) + _lab(E_, 4, -20, 'E')
    b += _angle(B_, E_, C_, '3α', r=26, dist=50) + _angle(B_, A_, E_, '2α', r=44, dist=64)
    b += _angle(C_, B_, E_, '3β', r=26, dist=50) + _angle(C_, E_, D_, '2β', r=44, dist=64)
    b += _angle(E_, B_, C_, 'x', r=20, dist=36)
    return _svg('Two adjacent parallelogram angles split in a fixed ratio', b)


def _rn_g068():
    A_, B_, C_, D_ = (155.75, 70.5), (155.75, 289.5), (484.25, 289.5), (484.25, 70.5)
    ex = 155.75 + 0.75 * 328.5          # AE = 3 ED, BG = 3 GC
    E_, G_, F_ = (ex, 70.5), (ex, 289.5), (155.75, 216.5)
    b = _poly([A_, B_, C_, D_]) + _abcd(A_, B_, C_, D_, [(-14, -16), (-14, 16), (14, 16), (14, -16)])
    b += _poly([F_, E_, G_], FILL, TEAL) + _poly([E_, G_, C_], FILL, TEAL) + _line(E_, G_, TEAL)
    b += _lab(E_, 0, -22, 'E') + _lab(G_, 0, 22, 'G') + _lab(F_, -22, 0, 'F')
    return _svg('Which extra area would determine all the shading?', b)


def _rn_g069():
    B_, C_ = (125.333, 293.556), (514.667, 293.556)
    w = (C_[0] - B_[0]) / 4                 # AD : BC = 5 : 20
    A_, D_ = (320 - w / 2, 66.444), (320 + w / 2, 66.444)
    b = _poly([A_, B_, C_, D_]) + _abcd(A_, B_, C_, D_, [(-14, -16), (-14, 16), (14, 16), (14, -16)])
    b += _poly([A_, B_, D_], FILL, TEAL)
    b += _t(320, 43.444, '5') + _t(320, 316.556, '20') + _t(286, 104, '15 cm²', size=17)
    return _svg('Area ratio across a trapezoid diagonal', b)


def _rn_grid(x0, y0, u, nx, ny, color='#c6d4dd'):
    b = ''
    for k in range(1, nx): b += _line((x0 + k * u, y0 + ny * u), (x0 + k * u, y0), color, 1)
    for k in range(1, ny): b += _line((x0, y0 + k * u), (x0 + nx * u, y0 + k * u), color, 1)
    return b


def _rn_g070():
    u, nx, ny = 36.5, 8, 5
    x0, y0 = 320 - nx * u / 2, 180 - ny * u / 2 - 10
    P = lambda x, y: (x0 + x * u, y0 + (ny - y) * u)     # grid point, y up
    b = _poly([P(0, 0), P(8, 0), P(8, 5), P(0, 5)]) + _rn_grid(x0, y0, u, nx, ny)
    b += _poly([P(3, 5), P(8, 3), P(6, 0), P(2, 0), P(0, 3)], FILL, TEAL)
    b += _t(320, y0 + ny * u + 25, 'Each grid square: 1 cm × 1 cm', size=17)
    return _svg('A shaded pentagon on a one-centimeter grid', b)


def _rn_p09():
    x0, y0, s = 192.25, 52.25, 255.5
    c = s * 7 / 13                          # 13 by 13 with a 7 by 7 square missing
    P = [(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0 + c, y0 + s), (x0 + c, y0 + s - c), (x0, y0 + s - c)]
    b = _poly(P, FILL, TEAL)
    b += _t(x0 + s / 2, y0 - 22, '13') + _t(x0 + s + 25, y0 + s / 2 - 7.75, '13')
    b += _t(x0 + c / 2, y0 + s - c + 23, '7') + _t(x0 + c - 20, y0 + s - c / 2, '7')
    return _svg('An L-shaped region with right-angle corners', b)


def _rn_p10():
    u, nx, ny = 41.714, 7, 5
    x0, y0 = 320 - nx * u / 2, 180 - ny * u / 2
    P = lambda x, y: (x0 + x * u, y0 + (ny - y) * u)
    b = _poly([P(0, 0), P(7, 0), P(7, 5), P(0, 5)], FILL, TEAL)
    b += _poly([P(2, 5), P(0, 4), P(2, 3), P(4, 4)], 'white', TEAL) + _poly([P(5, 2), P(3, 1), P(5, 0), P(7, 1)], 'white', TEAL)
    b += _rn_grid(x0, y0, u, nx, ny, '#b0c4ce')
    return _svg('Two unshaded kites on a grid', b)


def _rn_p16():
    W, H = 400, 300                          # rectangle 24 by 18 (half-sides 12 and 9), rhombus side 15
    A_, B_, C_, D_ = (320 - W / 2, 180 - H / 2), (320 - W / 2, 180 + H / 2), (320 + W / 2, 180 + H / 2), (320 + W / 2, 180 - H / 2)
    b = _poly([A_, B_, C_, D_]) + _abcd(A_, B_, C_, D_, [(-14, -16), (-14, 16), (14, 16), (14, -16)])
    b += _poly([(320, A_[1]), (D_[0], 180), (320, B_[1]), (A_[0], 180)], FILL, TEAL)
    b += _t(A_[0] - 20, (A_[1] + 180) / 2, '9') + _t((320 + D_[0]) / 2 + 16, (A_[1] + 180) / 2 - 12, '15')
    return _svg('A rhombus joining the side midpoints of a rectangle', b)


def _rn_p17():
    n, R, c = 10, 125.356, (320.0, 180.0)
    ang = 360.0 / n
    b = ''
    for k in range(n):
        a = -90 + k * ang
        tip = _pt(c, R, a)
        s = R / 2 / math.cos(math.radians(ang / 2))
        p1, p2 = _pt(c, s, a - ang / 2), _pt(c, s, a + ang / 2)
        b += _poly([c, p1, tip, p2], '#e7f4f3', TEAL)
        if k == 0:
            b += _angle(tip, p1, p2, '', r=19.5) + _t(tip[0], tip[1] + 36, 'α', size=18, color=TEAL)
    return _svg('Ten congruent rhombuses around a point', b)


def _rn_p18():
    x0, y0, s = 198.333, 58.333, 243.333     # 3 rows and 4 columns
    A_, B_, C_, D_ = (x0, y0), (x0, y0 + s), (x0 + s, y0 + s), (x0 + s, y0)
    b = _poly([A_, B_, C_, D_]) + _abcd(A_, B_, C_, D_, [(-14, -16), (-14, 16), (14, 16), (14, -16)])
    for k in range(1, 4): b += _line((x0 + k * s / 4, y0 + s), (x0 + k * s / 4, y0), TEAL)
    for k in range(1, 3): b += _line((x0, y0 + k * s / 3), (x0 + s, y0 + k * s / 3), TEAL)
    return _svg('A square divided into a three-by-four array of rectangles', b)


def _rn_p19():
    k = 14.0                                  # BO 5, AO 12, OC 8
    O_ = (320.0, 45.231 + 12 * k)
    A_, C_, B_, D_ = (320.0, 45.231), (320.0, O_[1] + 8 * k), (320.0 - 5 * k, O_[1]), (320.0 + 5 * k, O_[1])
    b = _poly([A_, B_, C_, D_]) + _line(A_, C_, TEAL) + _line(B_, D_, TEAL)
    b += _lab(A_, 0, -20, 'A') + _lab(B_, -21, 0, 'B') + _lab(C_, 0, 20, 'C') + _lab(D_, 21, 0, 'D') + _lab(O_, 15, -15, 'O')
    b += _t((A_[0] + B_[0]) / 2 - 22, (A_[1] + B_[1]) / 2 - 6, '13') + _t((B_[0] + O_[0]) / 2, O_[1] + 18, '5') + _t(306, (O_[1] + C_[1]) / 2, '8')
    return _svg('A kite with an unknown upper diagonal piece', b, vb='0 0 640 360')


def _rn_a02():
    A_, B_, C_, D_ = (101, 82.667), (101, 277.333), (539, 277.333), (539, 82.667)
    E_ = (101 + 438 * 14 / 23, 82.667)       # AE : ED = 14 : 9, as the areas say
    b = _poly([A_, B_, C_, D_]) + _abcd(A_, B_, C_, D_, [(-14, -16), (-14, 16), (14, 16), (14, -16)])
    b += _poly([A_, B_, E_], FILL, TEAL) + _line(E_, C_, TEAL) + _lab(E_, 0, -22, 'E')
    return _svg('Find a corner area from the central triangle', b)


def _rn_a08():
    A_, B_, C_, D_ = (232.4, 63.2), (232.4, 296.8), (407.6, 296.8), (407.6, 63.2)
    E_ = (407.6, 63.2 + 233.6 * 4 / 5)       # DE = 4 EC
    b = _poly([A_, B_, C_, D_]) + _abcd(A_, B_, C_, D_, [(-14, -16), (-14, 16), (14, 16), (14, -16)])
    b += _line(A_, C_, TEAL) + _line(A_, E_, TEAL) + _lab(E_, 22, 0, 'E')
    b += _t(352, 118, 'x') + _t(352, 214, 'y') + _t(284.96, 223.8, 'z')
    return _svg('Three triangle areas in a rectangle', b)


def _rn_a17():
    B_, C_ = (86.667, 273.333), (553.333, 273.333)
    a = (C_[0] - B_[0]) / 7                   # AD = 3a, BC = 7a, EF = 2a
    A_, D_ = (320 - 1.5 * a, 86.667), (320 + 1.5 * a, 86.667)
    E_, F_ = (320 - a, 273.333), (320 + a, 273.333)
    b = _poly([A_, B_, C_, D_]) + _abcd(A_, B_, C_, D_, [(-14, -16), (-14, 16), (14, 16), (14, -16)])
    b += _poly([A_, B_, E_], FILL, TEAL) + _poly([D_, F_, C_], FILL, TEAL)
    b += _lab(E_, 0, 22, 'E') + _lab(F_, 0, 22, 'F') + _t(320, 64.667, '3a') + _t(320, 315.333, '7a')
    return _svg('A smaller trapezoid covers half the total area', b)


def rn_guided(M):
    # ---------- g044: square, diagonal 12 -> 72  ==>  diagonal 14 -> 98 (lesson example stays 12 -> 72; Hebrew 10 -> 50)
    _rn_guided(M, 'geo32-g044', 'The diagonal of a square is 14 cm long. What is the area of the square (in cm²)?',
               ['$49$', '$98$', '$196$', '$392$'], 2,
               ['The area of a square from its diagonal: $S=\\frac{d^2}{2}$.', '$S=\\frac{14^2}{2}=\\frac{196}{2}=98$.'],
               {1: 1, 2: 3, 3: 4, 4: 2}, [
        ('The diagonal of a square is 12 centimeters.', 'The diagonal of a square is 14 centimeters.'),
        ('put 12 on the diagonal', 'put 14 on the diagonal'),
        ('\\frac{12\\cdot12}{2}=72', '\\frac{14\\cdot14}{2}=98'), ('12 · 12 / 2 = 72', '14 · 14 / 2 = 98'),
        ('12 times 12 over 2.', '14 times 14 over 2.'),
        ('Write 144 ÷ 2 = 72', 'Write 196 ÷ 2 = 98'), ('144 over 2 — 72.', '196 over 2 — 98.'),
        ('s^2+s^2=12^2\\ \\Rightarrow\\ s^2=72', 's^2+s^2=14^2\\ \\Rightarrow\\ s^2=98'),
        ('s² + s² = 12² → s² = 72', 's² + s² = 14² → s² = 98'),
        ('s squared plus s squared is 144. So s squared is 72.', 's squared plus s squared is 196. So s squared is 98.'),
        ("144? That's the diagonal squared", "196? That's the diagonal squared"),
        ("36? That's half the diagonal squared.", "49? That's half the diagonal squared."),
        ('72. Choice two.', '98. Choice two.')],
        fig={'12': '14'}, aria=[('diagonal 12 cm', 'diagonal 14 cm')])

    # ---------- g046: rectangle, CD 3, angle BEC 120 -> 9√3  ==>  CD 5 -> 25√3 (Hebrew CD 2)
    _rn_guided(M, 'geo32-g046', 'The diagonals of rectangle ABCD intersect at E. Given:\n' + _cases('CD=5' + CM, '\\angle BEC=120°') +
               '\nWhat is the area of the rectangle (in cm²)?',
               ['$25$', '$50$', '$25\\sqrt3$', '$50\\sqrt3$'], 3,
               ['The diagonals of a rectangle are equal and bisect each other, therefore $EB=EC$. Triangle BEC is isosceles, and its base angles are $\\frac{180°-120°}{2}=30°$.',
                'In right triangle BCD, $\\angle DBC=30°$. CD is opposite the $30°$ angle: it is the short leg, 5. The long leg is $BC=5\\sqrt3$ (the sides are in the ratio $1 : \\sqrt3 : 2$).',
                '$S=5\\cdot5\\sqrt3=25\\sqrt3$.'],
               {1: 2, 2: 3, 3: 1, 4: 4}, [
        ('CD is 3 centimeters.', 'CD is 5 centimeters.'), ('write a = 3', 'write a = 5'), ('So a is 3.', 'So a is 5.'),
        ('Write BC = 3√3', 'Write BC = 5√3'), ('BC is 3 root 3.', 'BC is 5 root 3.'),
        ('S=3\\cdot3\\sqrt3=9\\sqrt3', 'S=5\\cdot5\\sqrt3=25\\sqrt3'), ('S = 3 · 3√3 = 9√3', 'S = 5 · 5√3 = 25√3'),
        ('3 root 3 times 3 — 9 root 3.', '5 root 3 times 5 — 25 root 3.')],
        fig={'3': '5'})

    # ---------- g048: parallelogram, parts 3α + α and 3β + β -> 45  ==>  3α + 2α and 3β + 2β -> 72 (Hebrew 60)
    _rn_guided(M, 'geo32-g048', 'In parallelogram ABCD, the marked parts of angle B are $3\\alpha$ and $2\\alpha$, and the marked parts of angle C are '
               '$3\\beta$ and $2\\beta$. The segments BE and CE meet as in the accompanying figure. What is x?',
               ['$36°$', '$72°$', '$90°$', '$108°$'], 2,
               ['Angle B is $3\\alpha+2\\alpha=5\\alpha$, and angle C is $5\\beta$. Adjacent angles of a parallelogram add up to $180°$: $5\\alpha+5\\beta=180°$. Therefore $\\alpha+\\beta=36°$.',
                'In triangle BCE: $x=180°-3\\alpha-3\\beta=180°-3(\\alpha+\\beta)=180°-108°=72°$.'],
               {1: 4, 2: 2, 3: 1, 4: 3}, [
        ('Angle B is split into 3 alpha and alpha. Angle C — into 3 beta and beta.',
         'Angle B is split into 3 alpha and 2 alpha. Angle C — into 3 beta and 2 beta.'),
        ('4\\alpha+4\\beta=180°', '5\\alpha+5\\beta=180°'), ('4α + 4β = 180°', '5α + 5β = 180°'),
        ('4 alpha plus 4 beta equals 180.', '5 alpha plus 5 beta equals 180.'),
        ('\\alpha+\\beta=45°', '\\alpha+\\beta=36°'), ('α + β = 45°', 'α + β = 36°'),
        ('Divide by 4: alpha plus beta is 45.', 'Divide by 5: alpha plus beta is 36.'),
        ('We already know alpha plus beta is 45 — so 3 alpha plus 3 beta is 135.', 'We already know alpha plus beta is 36 — so 3 alpha plus 3 beta is 108.'),
        ('180°-135°=45°', '180°-108°=72°'), ('180° − 135° = 45°', '180° − 108° = 72°'),
        ('180 minus 135. 45.', '180 minus 108. 72.'), ("But the angle x — that's 45.", "But the angle x — that's 72.")],
        svg=_rn_g048())   # review: redrawn to 42° / 66° / 72° (was the old 52.5° / 82.5° / 45° drawing relabeled)

    # ---------- g049: parallelogram, 17 / 13 / EC 12 (5-12-13) -> 204  ==>  AD 24, CD 17, EC 16 (8-15-17) -> 360 (Hebrew 3-4-5)
    _rn_guided(M, 'geo32-g049', 'ABCD is a parallelogram, and $AE\\perp BC$. Given:\n' + _cases('AD=24' + CM, 'CD=17' + CM, 'EC=16' + CM) +
               '\nWhat is the area of the parallelogram (in cm²)?',
               ['$180$', '$255$', '$360$', '$408$'], 3,
               ['Opposite sides are equal: $BC=AD=24$ and $AB=CD=17$.',
                '$BE=24-16=8$. In right triangle ABE, the sides are $8, 15, 17$ (a Pythagorean triple). The height is $AE=15$.',
                '$S=BC\\cdot AE=24\\cdot15=360$.'],
               {1: 4, 2: 1, 3: 3, 4: 2}, [
        ('AD is 17, CD is 13, EC is 12.', 'AD is 24, CD is 17, EC is 16.'),
        ('Write 13 on AB', 'Write 17 on AB'), ('If DC is 13 — AB is also 13.', 'If DC is 17 — AB is also 17.'),
        ('Write 17 under the whole of BC', 'Write 24 under the whole of BC'), ('If AD is 17 — then all of BC is 17.', 'If AD is 24 — then all of BC is 24.'),
        ('Write BE = 17 − 12 = 5', 'Write BE = 24 − 16 = 8'), ("And if BC is 17 — what's left, BE, has to be 5.", "And if BC is 24 — what's left, BE, has to be 8."),
        ('Here I see a right triangle: 5, something, and 13.', 'Here I see a right triangle: 8, something, and 17.'),
        ('5\\ -\\ 12\\ -\\ 13', '8\\ -\\ 15\\ -\\ 17'), ('5 - 12 - 13', '8 - 15 - 17'),
        ('5, 12, 13 — a Pythagorean triple!', '8, 15, 17 — a Pythagorean triple!'),
        ('Write AE = 12', 'Write AE = 15'), ('So the height AE is 12.', 'So the height AE is 15.'),
        ('S=17\\cdot12=204', 'S=24\\cdot15=360'), ('S = 17 · 12 = 204', 'S = 24 · 15 = 360'), ('17 times 12 — 204.', '24 times 15 — 360.'),
        ('13 times 17 is 221', '17 times 24 is 408'), ('The base is all of BC, 17.', 'The base is all of BC, 24.')],
        fig={'17': '24', '13': '17', '12': '16'})

    # ---------- g051: rhombus, diagonals sum 34 / difference 14 -> 52  ==>  sum 46 / difference 14 -> 30, 16 -> side 17 -> 68 (Hebrew 14 / 2)
    _rn_guided(M, 'geo32-g051', 'The sum of the lengths of the diagonals of a rhombus is 46 cm. The absolute difference between their lengths is 14 cm. '
               'What is its perimeter (in cm)?',
               ['$34$', '$68$', '$92$', '$240$'], 2,
               ['Call the diagonals $a>b$. Then:\n$\\begin{cases} a+b=46 \\\\ a-b=14 \\end{cases}$',
                'Add the equations: $2a=60$. Therefore $a=30$ and $b=16$.',
                'The diagonals are perpendicular and bisect each other: the half-diagonals 15 and 8 are the legs of a right triangle. Its hypotenuse, the side, is 17 ($8, 15, 17$).',
                '$P=4\\cdot17=68$.'],
               {1: 2, 2: 1, 3: 3, 4: 4}, [
        ('The sum of the diagonals of a rhombus is 34.', 'The sum of the diagonals of a rhombus is 46.'),
        ('a+b=34', 'a+b=46'), ('a + b = 34', 'a + b = 46'), ('a plus b is 34.', 'a plus b is 46.'),
        ('write 2a = 48, a = 24', 'write 2a = 60, a = 30'), ('2a is 48, so a is 24.', '2a is 60, so a is 30.'),
        ('Write b = 10', 'Write b = 16'), ('And b: 24 minus what gives 14? Minus 10. b is 10.', 'And b: 30 minus what gives 14? Minus 16. b is 16.'),
        ('Write 12 and 12 on the halves of the long diagonal', 'Write 15 and 15 on the halves of the long diagonal'),
        ('So I split 24 into 12 and 12.', 'So I split 30 into 15 and 15.'),
        ('Write 5 and 5 on the halves of the short diagonal', 'Write 8 and 8 on the halves of the short diagonal'),
        ('And 10 into 5 and 5.', 'And 16 into 8 and 8.'),
        ('Again — a right triangle here. 5, 12 —', 'Again — a right triangle here. 8, 15 —'),
        ('5\\ -\\ 12\\ -\\ 13', '8\\ -\\ 15\\ -\\ 17'), ('5 - 12 - 13', '8 - 15 - 17'), ('— 13. A Pythagorean triple.', '— 17. A Pythagorean triple.'),
        ('Write 13 on each side', 'Write 17 on each side'), ('all the others are 13 too.', 'all the others are 17 too.'),
        ('P=4\\cdot13=52', 'P=4\\cdot17=68'), ('P = 4 · 13 = 52', 'P = 4 · 17 = 68'), ('4 sides together — 52.', '4 sides together — 68.')])

    # ---------- g053: kite, CB = CD = 6 -> 12 + 6√2  ==>  10 -> 20 + 10√2 (Hebrew 4)
    _rn_guided(M, 'geo32-g053', 'ABCD is a kite. Given:\n' + _cases('AB=AD', 'CB=CD=10' + CM, '\\angle ABD=45°', '\\angle DBC=60°') +
               '\nWhat is the perimeter of the kite (in cm)?',
               ['$20+10\\sqrt3$', '$10+10\\sqrt2$', '$20+10\\sqrt2$', '$10+10\\sqrt3$'], 3,
               ['Triangle BCD: $CB=CD=10$ and $\\angle DBC=60°$. An isosceles triangle with a $60°$ angle is equilateral, therefore $BD=10$.',
                'Triangle ABD: $AB=AD$, therefore $\\angle ADB=\\angle ABD=45°$ and $\\angle A=90°$. It is a 45-45-90 triangle with hypotenuse $BD=10$.',
                'Each leg: $AB=AD=\\frac{10}{\\sqrt2}=5\\sqrt2$.', '$P=10+10+5\\sqrt2+5\\sqrt2=20+10\\sqrt2$.'],
               {1: 2, 2: 4, 3: 1, 4: 3}, [
        ('And DC is 6.', 'And DC is 10.'), ('Write 6 on CB', 'Write 10 on CB'), ('This is 6, and this is 6.', 'This is 10, and this is 10.'),
        ('Write BD = 6', 'Write BD = 10'), ('so BD is 6 as well.', 'so BD is 10 as well.'),
        ('\\frac{6}{\\sqrt2}=3\\sqrt2', '\\frac{10}{\\sqrt2}=5\\sqrt2'), ('6 ÷ √2 = 3√2', '10 ÷ √2 = 5√2'),
        ('Ignore the root: 6 divided by 2 is 3. Attach the root: 3 root 2.', 'Ignore the root: 10 divided by 2 is 5. Attach the root: 5 root 2.'),
        ('Write 3√2 on AB and on AD', 'Write 5√2 on AB and on AD'),
        ('P=6+6+3\\sqrt2+3\\sqrt2=12+6\\sqrt2', 'P=10+10+5\\sqrt2+5\\sqrt2=20+10\\sqrt2'),
        ('Write P = 6 + 6 + …', 'Write P = 10 + 10 + …'), ('Now the perimeter: 6 plus 6 is 12.', 'Now the perimeter: 10 plus 10 is 20.'),
        ('Only two choices start with 12.', 'Only two choices start with 20.'), ('P = 12 + 6√2', 'P = 20 + 10√2'),
        ('12 plus 6 root 2.', '20 plus 10 root 2.')],
        fig={'6': '10'})

    # ---------- g055: isosceles trapezoid 54 / DE 6 / triangle 6 -> AD 7  ==>  65 / DE 5 / triangle 10 -> EC 4, AD 9 (Hebrew 30 / 3 / 3 -> 8)
    _rn_guided(M, 'geo32-g055', 'The area of isosceles trapezoid ABCD is 65 cm². DE is an altitude, $DE=5$ cm, and the area of triangle DEC is 10 cm². '
               'What is AD (in cm)?',
               ['$5$', '$9$', '$13$', '$17$'], 2,
               ['Triangle DEC: $\\frac{5\\cdot EC}{2}=10$, therefore $EC=4$.',
                'Drop the height AF too. The trapezoid is isosceles, therefore triangle ABF also has area 10.',
                'The middle rectangle AFED has area $65-10-10=45$ and height 5: $AD=\\frac{45}{5}=9$.'],
               {1: 4, 2: 2, 3: 1, 4: 3}, [
        ('ABCD is an isosceles trapezoid with area 54.', 'ABCD is an isosceles trapezoid with area 65.'),
        ('has area 6. The height DE is 6.', 'has area 10. The height DE is 5.'),
        ('Triangle DEC has area 6. So', 'Triangle DEC has area 10. So'),
        ('\\frac{6\\cdot EC}{2}=6\\ \\Rightarrow\\ EC=2', '\\frac{5\\cdot EC}{2}=10\\ \\Rightarrow\\ EC=4'),
        ('6 · EC / 2 = 6 → EC = 2', '5 · EC / 2 = 10 → EC = 4'),
        ('6 times EC over 2 equals 6. EC is 2.', '5 times EC over 2 equals 10. EC is 4.'),
        ('Write BF = 2', 'Write BF = 4'), ('So BF is also 2.', 'So BF is also 4.'),
        ("x doesn't equal 6.", "x doesn't equal 5."), ('Write 6 in the left triangle', 'Write 10 in the left triangle'),
        ('has area 6 — so the one on the left also has area 6.', 'has area 10 — so the one on the left also has area 10.'),
        ('54-6-6=42', '65-10-10=45'), ('54 − 6 − 6 = 42', '65 − 10 − 10 = 45'),
        ('The whole trapezoid is 54.', 'The whole trapezoid is 65.'), ('the rectangle — is 42.', 'the rectangle — is 45.'),
        ('6x=42\\ \\Rightarrow\\ x=7', '5x=45\\ \\Rightarrow\\ x=9'), ('6x = 42 → x = 7', '5x = 45 → x = 9'),
        ('6x equals 42. x is 7.', '5x equals 45. x is 9.'),
        ('Forget the 6, 42, 6 for a moment.', 'Forget the 10, 45, 10 for a moment.'),
        ('\\frac{(x+x+4)\\cdot6}{2}=54', '\\frac{(x+x+8)\\cdot5}{2}=65'), ('(x + x + 4) · 6 / 2 = 54', '(x + x + 8) · 5 / 2 = 65'),
        ('x plus x plus 4. Times 6, the height. Over 2. Equals 54.', 'x plus x plus 8. Times 5, the height. Over 2. Equals 65.'),
        ('6x+12=54\\ \\Rightarrow\\ x=7', '5x+20=65\\ \\Rightarrow\\ x=9'),
        ('3(2x + 4) = 54 → 6x + 12 = 54 → x = 7', '5(2x + 8) / 2 = 65 → 5x + 20 = 65 → x = 9'),
        ("That's 6x plus 12 equals 54. 6x is 42. x is 7.", "That's 5x plus 20 equals 65. 5x is 45. x is 9."),
        ("if this is 6, that's 6 too — the middle has to be 42.", "if this is 10, that's 10 too — the middle has to be 45.")],
        fig={'6': '5', '6 cm²': '10 cm²'})

    # ---------- g057: angles 112 + 104 -> α < 144  ==>  118 + 96 -> α < 146 (Hebrew 120 + 100 -> 140)
    _rn_guided(M, 'geo32-g057', 'The accompanying figure shows quadrilateral ABCD. Given: angle A is 118° and angle B is 96°. '
               'Which of the following cannot be the value of α?',
               ['$26°$', '$70°$', '$124°$', '$146°$'], 4,
               ['Call the fourth angle β. The angles of a quadrilateral add up to $360°$: $\\alpha+\\beta=360°-118°-96°=146°$.',
                'Both angles are positive, therefore $\\alpha<146°$. If $\\alpha=146°$, then $\\beta=0°$ — impossible.',
                'The other choices are possible: $26°+120°$, $70°+76°$ and $124°+22°$ all give $146°$.'],
               {1: 4, 2: 1, 3: 2, 4: 3}, [
        ('Angle A is 112, angle B is 104.', 'Angle A is 118, angle B is 96.'),
        ('\\alpha+\\beta+112°+104°=360°', '\\alpha+\\beta+118°+96°=360°'), ('α + β + 112° + 104° = 360°', 'α + β + 118° + 96° = 360°'),
        ('112 plus 104 is 216. 360 minus 216 — 144.', '118 plus 96 is 214. 360 minus 214 — 146.'),
        ('\\alpha+\\beta=144°', '\\alpha+\\beta=146°'), ('α + β = 144°', 'α + β = 146°'),
        ('So alpha plus beta together — 144.', 'So alpha plus beta together — 146.'),
        ('Together the two angles are 144.', 'Together the two angles are 146.'),
        ('Could be 72 and 72. Could be 100 and 44.', 'Could be 73 and 73. Could be 100 and 46.'),
        ('But neither one can be 144 — or more than 144.', 'But neither one can be 146 — or more than 146.'),
        ('\\alpha=144°\\ \\Rightarrow', '\\alpha=146°\\ \\Rightarrow'), ('α = 144° → β = 0°', 'α = 146° → β = 0°'),
        ('If alpha is 144, beta is zero. Beta has to be a real angle — so 144 is impossible.',
         'If alpha is 146, beta is zero. Beta has to be a real angle — so 146 is impossible.'),
        ('\\alpha=16°\\ \\rightarrow\\ \\beta=128°', '\\alpha=26°\\ \\rightarrow\\ \\beta=120°'), ('α = 16° → β = 128°', 'α = 26° → β = 120°'),
        ('\\alpha=64°\\ \\rightarrow\\ \\beta=80°', '\\alpha=70°\\ \\rightarrow\\ \\beta=76°'), ('α = 64° → β = 80°', 'α = 70° → β = 76°'),
        ('\\alpha=128°\\ \\rightarrow\\ \\beta=16°', '\\alpha=124°\\ \\rightarrow\\ \\beta=22°'), ('α = 128° → β = 16°', 'α = 124° → β = 22°'),
        ('Alpha 16: beta is 128. Together 144 — possible.', 'Alpha 26: beta is 120. Together 146 — possible.'),
        ('Alpha 64: beta 80 — fine.', 'Alpha 70: beta 76 — fine.'),
        ("Alpha 128 — some students think: wait, the angle looks acute. It can't be 128.",
         "Alpha 124 — some students think: wait, the angle looks acute. It can't be 124."),
        ('Alpha 128, beta 16 — also possible.', 'Alpha 124, beta 22 — also possible.'),
        ('The only impossible value: 144.', 'The only impossible value: 146.')],
        fig={'112°': '118°', '104°': '96°'})

    # ---------- g058: parallelogram 7 / 3 / 64° / 58° -> 34  ==>  9 / 4 / 72° / 54° -> 44 (Hebrew 5 / 2 / 70° / 55°)
    _rn_guided(M, 'geo32-g058', 'ABCD is a parallelogram, and E lies on AD. Given:\n' + _cases('AB=9' + CM, 'AE=4' + CM, '\\angle ABC=72°', '\\angle BCE=54°') +
               '\nWhat is the perimeter of the parallelogram (in cm)?',
               ['$26$', '$36$', '$44$', '$50$'], 3,
               ['Opposite angles are equal: $\\angle D=\\angle B=72°$. Adjacent angles: $\\angle C=180°-72°=108°$, therefore $\\angle ECD=108°-54°=54°$.',
                'Triangle EDC: $\\angle CED=180°-72°-54°=54°$. Two equal angles, therefore $ED=CD=AB=9$. (An angle bisector in a parallelogram cuts off an isosceles triangle.)',
                '$AD=4+9=13$ and $P=2(9+13)=44$.'],
               {1: 2, 2: 4, 3: 1, 4: 3}, [
        ('Write 7 on CD', 'Write 9 on CD'), ('AB is 7 — so CD is 7 too.', 'AB is 9 — so CD is 9 too.'),
        ('AE is 3.', 'AE is 4.'), ('Angle B is 64.', 'Angle B is 72.'), ('Write 64° at D', 'Write 72° at D'),
        ('so angle D is 64 too.', 'so angle D is 72 too.'),
        ('\\angle A=180°-64°=116°', '\\angle A=180°-72°=108°'), ('∠A = 180° − 64° = 116°', '∠A = 180° − 72° = 108°'),
        ('So angle A is 180 minus 64 — 116.', 'So angle A is 180 minus 72 — 108.'), ('Write 116° at C', 'Write 108° at C'),
        ('Either way — 116.', 'Either way — 108.'),
        ('\\angle ECD=116°-58°=58°', '\\angle ECD=108°-54°=54°'), ('∠ECD = 116° − 58° = 58°', '∠ECD = 108° − 54° = 54°'),
        ('Angle ECD: 116 minus 58 — 58.', 'Angle ECD: 108 minus 54 — 54.'),
        ('\\angle CED=180°-64°-58°=58°', '\\angle CED=180°-72°-54°=54°'), ('180° − 64° − 58° = 58°', '180° − 72° − 54° = 54°'),
        ('64 plus 58 is 122. 180 minus 122 — 58.', '72 plus 54 is 126. 180 minus 126 — 54.'),
        ('angle CED is 58 right away.', 'angle CED is 54 right away.'), ('Either way — angle E is 58.', 'Either way — angle E is 54.'),
        ('Write 7 on ED', 'Write 9 on ED'), ('CD is 7 — so ED is 7 too.', 'CD is 9 — so ED is 9 too.'),
        ('AD=3+7=10', 'AD=4+9=13'), ('AD = 3 + 7 = 10', 'AD = 4 + 9 = 13'), ('All of AD: 3 plus 7 — 10.', 'All of AD: 4 plus 9 — 13.'),
        ('Write 10 on BC', 'Write 13 on BC'), ('BC is 10 too', 'BC is 13 too'),
        ('P=7+10+7+10=34', 'P=9+13+9+13=44'), ('P = 7 + 10 + 7 + 10 = 34', 'P = 9 + 13 + 9 + 13 = 44'),
        ('The perimeter: 7 plus 10 plus 7 plus 10. 14 and 20 — 34.', 'The perimeter: 9 plus 13 plus 9 plus 13. 18 and 26 — 44.')],
        fig={'7': '9', '3': '4', '64°': '72°', '58°': '54°'})

    # ---------- g059: rectangle, BC 12, perimeter EBC 25 -> 15  ==>  BC 24, perimeter 50 -> AC 26, AB 10 -> 60 (Hebrew 4 / 9)
    _rn_guided(M, 'geo32-g059', 'The diagonals of rectangle ABCD intersect at E. Given: $BC=24$ cm, and the perimeter of triangle EBC is 50 cm. '
               'What is the area of triangle ABE (in cm²)?',
               ['$30$', '$60$', '$120$', '$240$'], 2,
               ['The diagonals of a rectangle are equal and bisect each other: $EB=EC$. $EB+EC=50-24=26$, therefore each is $13$ and $AC=26$.',
                'Right triangle ABC: hypotenuse 26 and leg 24, therefore $AB=10$ ($10, 24, 26$ — the triple $5, 12, 13$ doubled). The rectangle is $10\\cdot24=240$.',
                'The diagonals of any parallelogram (a rectangle too) split it into four triangles of equal area: $S_{ABE}=\\frac{240}{4}=60$.'],
               {1: 4, 2: 1, 3: 2, 4: 3}, [
        ('The perimeter of triangle EBC is 25.', 'The perimeter of triangle EBC is 50.'),
        ('EB+12+EC=25', 'EB+24+EC=50'), ('EB + 12 + EC = 25', 'EB + 24 + EC = 50'),
        ('The perimeter of EBC is 25: EB plus 12 plus EC.', 'The perimeter of EBC is 50: EB plus 24 plus EC.'),
        ("So EB and EC together are 13. They're equal — 6.5 each.", "So EB and EC together are 26. They're equal — 13 each."),
        ('Write 6.5 on EB and on EC', 'Write 13 on EB and on EC'),
        ('AC=6.5+6.5=13', 'AC=13+13=26'), ('AC = 6.5 + 6.5 = 13', 'AC = 13 + 13 = 26'),
        ('If each piece is 6.5, then AE and ED are 6.5 too — so the diagonal AC is 13.', 'If each piece is 13, then AE and ED are 13 too — so the diagonal AC is 26.'),
        ('13,\\ 12\\ \\rightarrow\\ AB=5', '26,\\ 24\\ \\rightarrow\\ AB=10'), ('13, 12 → AB = 5', '26, 24 → AB = 10'),
        ('Hypotenuse 13, leg 12 — the triple 5, 12, 13. AB is 5.', 'Hypotenuse 26, leg 24 — the triple 5, 12, 13, doubled: 10, 24, 26. AB is 10.'),
        ('Write 5 on AB', 'Write 10 on AB'),
        ('\\frac{5\\cdot12}{2}=30\\ \\Rightarrow\\ S_{ABE}=15', '\\frac{10\\cdot24}{2}=120\\ \\Rightarrow\\ S_{ABE}=60'),
        ('S(ABC) = 30 → S(ABE) = 15', 'S(ABC) = 120 → S(ABE) = 60'),
        ('Triangle ABC is easy: 5 times 12 over 2 — 30. ABE is half of it: 15.', 'Triangle ABC is easy: 10 times 24 over 2 — 120. ABE is half of it: 60.'),
        ('S_{ABE}=\\frac{5\\cdot12}{4}=15', 'S_{ABE}=\\frac{10\\cdot24}{4}=60'), ('S(ABE) = 60 ÷ 4 = 15', 'S(ABE) = 240 ÷ 4 = 60'),
        ('5 times 12 is 60, over 4 — 15.', '10 times 24 is 240, over 4 — 60.'),
        ('S_{ABE}=\\frac{5\\cdot6}{2}=15', 'S_{ABE}=\\frac{10\\cdot12}{2}=60'), ('S(ABE) = 5·6/2 = 15', 'S(ABE) = 10·12/2 = 60'),
        ("So one triangle's height is half of 12 — 6.", "So one triangle's height is half of 24 — 12."),
        ('5 times 6 over 2 — 15.', '10 times 12 over 2 — 60.')],
        fig={'12': '24'})

    # ---------- g060: rhombus, BD 6, angle 60 -> 18√3  ==>  BD 10 -> 50√3 (Hebrew 4)
    _rn_guided(M, 'geo32-g060', 'ABCD is a rhombus. Given:\n' + _cases('BD=10' + CM, '\\angle ABD=60°') + '\nWhat is the area of the rhombus (in cm²)?',
               ['$25\\sqrt3$', '$50\\sqrt3$', '$100$', '$100\\sqrt3$'], 2,
               ['$AB=AD$ (all the sides of a rhombus are equal), therefore triangle ABD is isosceles with a $60°$ angle. It is equilateral: $AB=AD=BD=10$.',
                'All the sides are 10, therefore triangle BCD is equilateral too.',
                '$S=2\\cdot\\frac{10^2\\sqrt3}{4}=2\\cdot25\\sqrt3=50\\sqrt3$.'],
               {1: 1, 2: 4, 3: 3, 4: 2}, [
        ('The diagonal BD is 6, and angle ABD is 60.', 'The diagonal BD is 10, and angle ABD is 60.'),
        ('Write 3 on BO and 3 on OD', 'Write 5 on BO and 5 on OD'), ('— it cuts BD into 3 and 3.', '— it cuts BD into 5 and 5.'),
        ("3 is opposite the 30 — it's the short leg.", "5 is opposite the 30 — it's the short leg."),
        ('Write 3√3 on AO', 'Write 5√3 on AO'), ('AO is 3 root 3.', 'AO is 5 root 3.'),
        ('Write 3√3 on OC', 'Write 5√3 on OC'), ('so the bottom part is 3 root 3 too.', 'so the bottom part is 5 root 3 too.'),
        ('S=\\frac{6\\cdot6\\sqrt3}{2}=18\\sqrt3', 'S=\\frac{10\\cdot10\\sqrt3}{2}=50\\sqrt3'), ('S = 6 · 6√3 / 2 = 18√3', 'S = 10 · 10√3 / 2 = 50√3'),
        ('BD is 6. AC is 3 root 3 plus 3 root 3 — 6 root 3.', 'BD is 10. AC is 5 root 3 plus 5 root 3 — 10 root 3.'),
        ('6 times 6 root 3 over 2. Cancel the 6 with the 2 — 3. 3 times 6 root 3 — 18 root 3.',
         '10 times 10 root 3 over 2. Cancel the 10 with the 2 — 5. 5 times 10 root 3 — 50 root 3.'),
        ('4\\cdot\\frac{3\\cdot3\\sqrt3}{2}=18\\sqrt3', '4\\cdot\\frac{5\\cdot5\\sqrt3}{2}=50\\sqrt3'),
        ('2\\cdot\\frac{6\\cdot3\\sqrt3}{2}=18\\sqrt3', '2\\cdot\\frac{10\\cdot5\\sqrt3}{2}=50\\sqrt3'),
        ('2\\cdot\\frac{6\\sqrt3\\cdot3}{2}=18\\sqrt3', '2\\cdot\\frac{10\\sqrt3\\cdot5}{2}=50\\sqrt3'),
        ('base 3, height 3 root 3', 'base 5, height 5 root 3'), ('base 6, height 3 root 3', 'base 10, height 5 root 3'),
        ('base 6 root 3, height 3', 'base 10 root 3, height 5'),
        ('Write 6 on AB, AD, BC and CD', 'Write 10 on AB, AD, BC and CD'),
        ('BD is 6 — so AB and AD are 6. And all the sides of a rhombus are equal: DC and BC are 6 too.',
         'BD is 10 — so AB and AD are 10. And all the sides of a rhombus are equal: DC and BC are 10 too.'),
        ('S=2\\cdot\\frac{6^2\\sqrt3}{4}=18\\sqrt3', 'S=2\\cdot\\frac{10^2\\sqrt3}{4}=50\\sqrt3'), ('S = 2 · 6²√3 / 4 = 18√3', 'S = 2 · 10²√3 / 4 = 50√3'),
        ('Twice: 2 times 36 root 3 over 4 — 18 root 3.', 'Twice: 2 times 100 root 3 over 4 — 50 root 3.'),
        ('AC=6\\sqrt3', 'AC=10\\sqrt3'), ('AC = 6√3', 'AC = 10√3'),
        ('Triangle ABC has sides 6 and 6 with 120 between them — so AC is 6 root 3 straight away.',
         'Triangle ABC has sides 10 and 10 with 120 between them — so AC is 10 root 3 straight away.')],
        fig={'6': '10'})

    # ---------- g061 (letters only): equilateral AOD in square, angle OBC  ==>  equilateral BPC, angle PAD (same figure, new labels)
    _rn_guided(M, 'geo32-g061', 'ABCD is a square, and P is a point inside it such that triangle BPC is equilateral. What is angle PAD?',
               ['$15°$', '$30°$', '$60°$', '$75°$'], 1,
               ['$BP=BC=AB$ (the sides of the equilateral triangle and of the square).',
                '$\\angle ABP=90°-60°=30°$. Triangle ABP is isosceles: $\\angle BAP=\\frac{180°-30°}{2}=75°$.',
                '$\\angle PAD=90°-75°=15°$. (75° is a trap: it is angle BAP.)'],
               {1: 3, 2: 4, 3: 1, 4: 2}, [
        ('O is a point inside it, and triangle AOD is equilateral. What is angle OBC?',
         'P is a point inside it, and triangle BPC is equilateral. What is angle PAD?'),
        ('O is inside — but', 'P is inside — but'), ('Write 90° at A and at B', 'Write 90° at B and at A'),
        ('next to the angle we want — A and B.', 'next to the angle we want — B and A.'),
        ('Next given: AOD is equilateral.', 'Next given: BPC is equilateral.'),
        ('Mark AO and DO with the same tick', 'Mark BP and CP with the same tick'),
        ('In an equilateral triangle all sides are equal: DA, OD, AO. AD already has a tick — so DO and AO get the same tick.',
         'In an equilateral triangle all sides are equal: CB, PC, BP. BC already has a tick — so CP and BP get the same tick.'),
        ('Write 60° at A inside triangle AOD', 'Write 60° at B inside triangle BPC'),
        ('Highlight triangle ABO', 'Highlight triangle ABP'),
        ('Now look at the triangle that holds the angle at B: ABO.', 'Now look at the triangle that holds the angle at A: ABP.'),
        ('ABO is isosceles: AB equals AO.', 'ABP is isosceles: BA equals BP.'),
        ('Write α at B and at O inside triangle ABO', 'Write α at A and at P inside triangle ABP'),
        ('Angle ABO and angle AOB — call both alpha.', 'Angle BAP and angle BPA — call both alpha.'),
        ('\\angle BAO=90°-60°=30°', '\\angle ABP=90°-60°=30°'), ('∠BAO = 90° − 60° = 30°', '∠ABP = 90° − 60° = 30°'),
        ('The top angle: 90 minus 60 — 30.', 'The angle at B: 90 minus 60 — 30.'),
        ('75 is angle ABO', '75 is angle BAP'), ('the question asks for angle OBC.', 'the question asks for angle PAD.'),
        ('\\angle OBC=90°-75°=15°', '\\angle PAD=90°-75°=15°'), ('∠OBC = 90° − 75° = 15°', '∠PAD = 90° − 75° = 15°'),
        ("Together they fill the square's corner at B — 90.", "Together they fill the square's corner at A — 90.")],
        fig={'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C', 'O': 'P'})
    for b in M.video('solve-geo32-g061')['beats']:
        b['title'] = b['title'].replace('Solve triangle ABO', 'Solve triangle ABP')

    # ---------- g062: kite 13 / 12 / 15 (5-12-13) -> 240  ==>  AB = AD = 17, BO 15, OC 12 (8-15-17) -> 300 (Hebrew 5 / 4 / 9)
    _rn_guided(M, 'geo32-g062', 'ABCD is a kite, and its diagonals meet at O. Given:\n' + _cases('AB=AD=17' + CM, 'CB=CD', 'BO=15' + CM, 'OC=12' + CM) +
               '\nWhat is the area of the kite (in cm²)?',
               ['$150$', '$180$', '$300$', '$600$'], 3,
               ['The main diagonal AC bisects BD: $OD=BO=15$, therefore $BD=30$.',
                'Right triangle AOD: hypotenuse 17 and leg 15, therefore $AO=8$ ($8, 15, 17$). $AC=8+12=20$.',
                '$S=\\frac{AC\\cdot BD}{2}=\\frac{20\\cdot30}{2}=300$.'],
               {1: 3, 2: 1, 3: 2, 4: 4}, [
        ('Write 12 on OD', 'Write 15 on OD'), ('BO is 12 — so OD is 12.', 'BO is 15 — so OD is 15.'),
        ('13,\\ 12\\ \\rightarrow\\ AO=5', '17,\\ 15\\ \\rightarrow\\ AO=8'), ('13, 12 → AO = 5', '17, 15 → AO = 8'),
        ('We know the hypotenuse, 13, and a leg, 12. The Pythagorean triple 5, 12, 13 — the other leg is 5.',
         'We know the hypotenuse, 17, and a leg, 15. The Pythagorean triple 8, 15, 17 — the other leg is 8.'),
        ('Write 5 on AO', 'Write 8 on AO'),
        ('S=\\frac{(5+15)(12+12)}{2}=\\frac{20\\cdot24}{2}', 'S=\\frac{(8+12)(15+15)}{2}=\\frac{20\\cdot30}{2}'),
        ('S = (5 + 15)(12 + 12) / 2', 'S = (8 + 12)(15 + 15) / 2'),
        ('AC is 5 plus 15 — 20. BD is 12 plus 12 — 24. Over 2.', 'AC is 8 plus 12 — 20. BD is 15 plus 15 — 30. Over 2.'),
        ('=20\\cdot12=240', '=20\\cdot15=300'), ('= 20 · 12 = 240', '= 20 · 15 = 300'),
        ('You could do 20 times 24 first — better to cancel first: 24 over 2 is 12. 20 times 12 — 240.',
         'You could do 20 times 30 first — better to cancel first: 30 over 2 is 15. 20 times 15 — 300.'),
        ('\\frac{24\\cdot5}{2}+\\frac{24\\cdot15}{2}=60+180', '\\frac{30\\cdot8}{2}+\\frac{30\\cdot12}{2}=120+180'),
        ('2\\cdot\\frac{12\\cdot5}{2}+2\\cdot\\frac{12\\cdot15}{2}', '2\\cdot\\frac{15\\cdot8}{2}+2\\cdot\\frac{15\\cdot12}{2}'),
        ('60 + 180 appears', '120 + 180 appears'),
        ('base 24, height 5 — and triangle CBD — base 24, height 15 —', 'base 30, height 8 — and triangle CBD — base 30, height 12 —'),
        ('two small ones, 12 by 5 over 2, twice. Two big ones, 12 by 15 over 2, twice.', 'two small ones, 15 by 8 over 2, twice. Two big ones, 15 by 12 over 2, twice.'),
        ('Lots of ways — all 240.', 'Lots of ways — all 300.')],
        fig={'13': '17', '12': '15', '15': '12'})

    # ---------- g063: isosceles trapezoid AB = AD = 5, 30° -> 25  ==>  7 -> BC 14 -> 35 (Hebrew 2 -> 10)
    _rn_guided(M, 'geo32-g063', 'ABCD is an isosceles trapezoid with $AD\\parallel BC$. Given:\n' + _cases('AB=AD=7' + CM, '\\angle ABD=30°') +
               '\nWhat is its perimeter (in cm)?',
               ['$28$', '$35$', '$42$', '$21+7\\sqrt3$'], 2,
               ['$AB=AD$, therefore $\\angle ADB=\\angle ABD=30°$ and $\\angle A=180°-30°-30°=120°$.',
                'Angles on the same leg add up to $180°$: $\\angle B=60°$, therefore $\\angle DBC=60°-30°=30°$. The trapezoid is isosceles: $\\angle C=\\angle B=60°$.',
                'Triangle BCD has angles $30°$, $60°$ and $90°$. The short leg is $CD=AB=7$, therefore the hypotenuse is $BC=2\\cdot7=14$.',
                '$P=7+7+7+14=35$.'],
               {1: 1, 2: 3, 3: 4, 4: 2}, [
        ('AB and AD are 5', 'AB and AD are 7'), ('Write 5 on CD', 'Write 7 on CD'), ('so CD equals AB: 5.', 'so CD equals AB: 7.'),
        ('BC=2\\cdot5=10', 'BC=2\\cdot7=14'), ('BC = 2 · 5 = 10', 'BC = 2 · 7 = 14'), ('BC is 10.', 'BC is 14.'),
        ('P=5+5+5+10=25', 'P=7+7+7+14=35'), ('P = 5 + 5 + 5 + 10 = 25', 'P = 7 + 7 + 7 + 14 = 35'),
        ('The perimeter: 5 plus 5 plus 5 plus 10 — 25.', 'The perimeter: 7 plus 7 plus 7 plus 14 — 35.'),
        ('BD=5\\sqrt3', 'BD=7\\sqrt3'), ('BD = 5√3', 'BD = 7√3'), ('so BD is 5 root 3.', 'so BD is 7 root 3.'),
        ('times root 3 — 5 root 3.', 'times root 3 — 7 root 3.')],
        fig={'5': '7'})

    # ---------- g066 (statements only): new choice order; the false statement stays last
    q = 'geo32-g066'; vid = 'solve-' + q
    _rn_q(M, q, None, ['Every rhombus is a kite', 'Every square is a rectangle', 'Every rectangle is a parallelogram',
                       'Every parallelogram has perpendicular diagonals'], 4,
          ['Every rhombus is a kite, every square is a rectangle, and every rectangle is a parallelogram — all three are true.',
           'A parallelogram does not necessarily have perpendicular diagonals. Example: a $9\\times4$ rectangle is a parallelogram, and its diagonals are not perpendicular.'])
    L = M.slide(vid, 2)['lines']
    says = [l.get('say') or l.get('draw') for l in L]
    i1, i2, i3 = (says.index(s) for s in ('Statement one: every rectangle is a parallelogram.', 'Statement two: every rhombus is a kite.',
                                          'Statement three: every square is a rectangle.'))
    i4 = says.index('Circle choice 4')
    head, rect, rhom, sq, tail = L[:i1], L[i1:i2], L[i2:i3], L[i3:i4], L[i4:]
    def ren(block, word, num):
        out = []
        for l in block:
            l = dict(l)
            if 'say' in l: l['say'] = re.sub(r'^Statement \w+:', 'Statement %s:' % word, l['say'])
            if 'draw' in l: l['draw'] = re.sub(r'^Cross out choice \d', 'Cross out choice %d' % num, l['draw'])
            out.append(l)
        return out
    M.slide(vid, 2)['lines'] = head + ren(rhom, 'one', 1) + ren(sq, 'two', 2) + ren(rect, 'three', 3) + tail
    _rn_sub(M, vid, [('take a rectangle 8 by 3', 'take a rectangle 9 by 4')])

    # ---------- g067: rectangle, corner areas 5 and 13 -> 18  ==>  6 and 15 -> 21 (Hebrew 3 and 9)
    _rn_guided(M, 'geo32-g067', 'ABCD is a rectangle, and E lies on AD. The areas of triangles ABE and ECD are 6 cm² and 15 cm², respectively. '
               'What is the area of the shaded triangle EBC (in cm²)?',
               ['$9$', '$21$', '$30$', '$42$'], 2,
               ['Drop EF perpendicular to BC. ABFE and EFCD are rectangles.',
                'A diagonal splits a rectangle into two equal triangles: $S_{EBF}=S_{ABE}=6$ and $S_{EFC}=S_{ECD}=15$.',
                '$S_{EBC}=6+15=21$.'],
               {1: 4, 2: 2, 3: 1, 4: 3}, [
        ('Triangle ABE has area 5, triangle ECD has area 13.', 'Triangle ABE has area 6, triangle ECD has area 15.'),
        ('\\frac{xh}{2}=5\\ \\Rightarrow\\ xh=10', '\\frac{xh}{2}=6\\ \\Rightarrow\\ xh=12'), ('xh/2 = 5 → xh = 10', 'xh/2 = 6 → xh = 12'),
        ('x times h over 2 is 5. Multiply by 2: xh is 10.', 'x times h over 2 is 6. Multiply by 2: xh is 12.'),
        ('\\frac{yh}{2}=13\\ \\Rightarrow\\ yh=26', '\\frac{yh}{2}=15\\ \\Rightarrow\\ yh=30'), ('yh/2 = 13 → yh = 26', 'yh/2 = 15 → yh = 30'),
        ('yh over 2 is 13, so yh is 26.', 'yh over 2 is 15, so yh is 30.'),
        ('\\frac{10+26}{2}=18', '\\frac{12+30}{2}=21'), ('(10+26)/2 = 18', '(12+30)/2 = 21'),
        ("That's 10 plus 26 over 2 — 36 over 2 — 18.", "That's 12 plus 30 over 2 — 42 over 2 — 21."),
        ('Triangle ABE is 5.', 'Triangle ABE is 6.'), ('Write 5 in the left shaded part', 'Write 6 in the left shaded part'),
        ('So this shaded piece is 5 too.', 'So this shaded piece is 6 too.'),
        ('Write 13 in the right shaded part', 'Write 15 in the right shaded part'),
        ('The right rectangle: ECD is 13. Again a rectangle, again a diagonal — the shaded piece is 13.',
         'The right rectangle: ECD is 15. Again a rectangle, again a diagonal — the shaded piece is 15.'),
        ('Write 5 + 13 = 18', 'Write 6 + 15 = 21'), ('5 plus 13 — 18.', '6 plus 15 — 21.')],
        fig={'5 cm²': '6 cm²', '13 cm²': '15 cm²'})

    # ---------- g068: E, G split 2 : 1 -> ECD is enough  ==>  3 : 1 (Hebrew: midpoints); choices reordered
    _rn_guided(M, 'geo32-g068', 'ABCD is a rectangle. E lies on AD, G lies on BC, and F lies on AB. Given:\n' + _cases('AE=3ED', 'BG=3GC') +
               '\nTriangles FEG and EGC are shaded. Which of the following additional data is sufficient to determine the total shaded area?',
               ['The area of triangle ECD', 'The area of triangle AFE', 'The area of triangle FBG', 'None of these data is sufficient'], 1,
               ['E and G split AD and BC in the same ratio, $3 : 1$. So EG is parallel to AB, and it splits the rectangle into a left part and a right part in the ratio $3 : 1$.',
                'Let $S_{ECD}=s$. Then $S_{EGC}=s$ (a diagonal halves the right rectangle), the right rectangle is $2s$, and the left rectangle is $6s$.',
                'FEG stands on the full side EG of the left rectangle, with its tip on AB: $S_{FEG}=3s$. The shaded area is $s+3s=4s$, therefore the area of ECD is enough.',
                'The area of AFE or of FBG is not enough: F can be anywhere on AB.'],
               {1: 2, 2: 3, 3: 4, 4: 1}, [
        ('AE is twice ED, and BG is twice GC.', 'AE is three times ED, and BG is three times GC.'),
        ('Write the ratio 2 : 1 on AD and on BC', 'Write the ratio 3 : 1 on AD and on BC'),
        ('E splits AD, 2 to 1. G splits BC the same way, 2 to 1.', 'E splits AD, 3 to 1. G splits BC the same way, 3 to 1.'),
        ('$=2\\cdot2s=4s$', '$=3\\cdot2s=6s$'), ('Left rectangle = 2 × 2s = 4s', 'Left rectangle = 3 × 2s = 6s'),
        ("The left rectangle: same height, twice the base — 2 to 1. So it's twice as big: 4s.",
         "The left rectangle: same height, three times the base — 3 to 1. So it's three times as big: 6s."),
        ('Write 2s in triangle FEG', 'Write 3s in triangle FEG'), ('half the left rectangle — 2s.', 'half the left rectangle — 3s.'),
        ('$=s+2s=3s$', '$=s+3s=4s$'), ('Shaded = s + 2s = 3s', 'Shaded = s + 3s = 4s'),
        ('Total shaded: s plus 2s — 3s.', 'Total shaded: s plus 3s — 4s.'),
        ('the rectangle is 6s, the shaded part is half of it — and ECD is a sixth.', 'the rectangle is 8s, the shaded part is half of it — and ECD is an eighth.')],
        svg=_rn_g068())

    # ---------- g069: isosceles trapezoid 4 / 12 / 14 -> 56  ==>  5 / 20 / 15 -> 75 (Hebrew 3 / 6 / 10 -> 30)
    _rn_guided(M, 'geo32-g069', 'ABCD is an isosceles trapezoid. Given:\n' + _cases('AD\\parallel BC', 'AD=5' + CM, 'BC=20' + CM) +
               '\nThe shaded triangle ABD has area 15 cm². What is the area of the trapezoid (in cm²)?',
               ['$30$', '$60$', '$75$', '$150$'], 3,
               ['Triangles ABD and BCD have the same height (the height of the trapezoid). The ratio of their areas equals the ratio of their bases: $5 : 20=1 : 4$.',
                '$S_{BCD}=4\\cdot15=60$, and the trapezoid is $15+60=75$.',
                'Or: $\\frac{5h}{2}=15$ gives $h=6$, and $S=\\frac{(5+20)\\cdot6}{2}=75$.'],
               {1: 2, 2: 4, 3: 3, 4: 1}, [
        ('AD is 4, BC is 12, and the shaded triangle ABD has area 14.', 'AD is 5, BC is 20, and the shaded triangle ABD has area 15.'),
        ('The only base we have is AD — 4.', 'The only base we have is AD — 5.'),
        ('\\frac{4h}{2}=14\\ \\Rightarrow\\ h=7', '\\frac{5h}{2}=15\\ \\Rightarrow\\ h=6'), ('4h/2 = 14 → h = 7', '5h/2 = 15 → h = 6'),
        ('4h over 2 is 14 — so h is 7.', '5h over 2 is 15 — so h is 6.'),
        ('S=\\frac{(4+12)\\cdot7}{2}=56', 'S=\\frac{(5+20)\\cdot6}{2}=75'), ('S = (4+12)·7/2 = 56', 'S = (5+20)·6/2 = 75'),
        ('4 plus 12 is 16, times 7 over 2 — 8 times 7 — 56.', '5 plus 20 is 25, times 6 over 2 — 25 times 3 — 75.'),
        ('Shaded base: 4. White base: 12. Three times bigger — so the area is three times bigger: 42.',
         'Shaded base: 5. White base: 20. Four times bigger — so the area is four times bigger: 60.'),
        ('Write the ratio 4 : 12 = 1 : 3', 'Write the ratio 5 : 20 = 1 : 4'),
        ('Split BC into 4, 4, 4 and join the points to D', 'Split BC into 5, 5, 5, 5 and join the points to D'),
        ('Split BC into three pieces of 4. Now every triangle here has the same base — 4 —', 'Split BC into four pieces of 5. Now every triangle here has the same base — 5 —'),
        ('Write 14 in each of the four triangles', 'Write 15 in each of the five triangles'),
        ('So they all have the same area: 14, 14, 14, and the shaded 14.', 'So they all have the same area: 15, 15, 15, 15, and the shaded 15.'),
        ('S=14+42=4\\times14=56', 'S=15+60=5\\times15=75'), ('S = 4 × 14 = 56', 'S = 5 × 15 = 75'),
        ('The whole trapezoid: 14 plus 42 — 56. Careful: 42 alone', 'The whole trapezoid: 15 plus 60 — 75. Careful: 60 alone'),
        ('Base three times bigger, area three times bigger.', 'Base four times bigger, area four times bigger.')],
        svg=_rn_g069())

    # ---------- g070: 7 x 5 grid -> 22  ==>  8 x 5 grid, new pentagon -> 26 (Hebrew 20 squares -> 12)
    _rn_guided(M, 'geo32-g070', 'The rectangle in the accompanying figure consists of 40 congruent squares, each with side length 1 cm. '
               'What is the shaded area (in cm²)?',
               ['$14$', '$20$', '$26$', '$28$'], 3,
               ['The rectangle is $8\\cdot5=40$.',
                'The four white corner triangles have legs 3 and 2, 5 and 2, 2 and 3, and 2 and 3. Their areas are $\\frac{3\\cdot2}{2}=3$, $\\frac{5\\cdot2}{2}=5$, $\\frac{2\\cdot3}{2}=3$ and $3$. Together: $14$.',
                '$S=40-14=26$.'],
               {1: 3, 2: 1, 3: 2, 4: 4}, [
        ('A rectangle made of 35 congruent squares', 'A rectangle made of 40 congruent squares'),
        ('Rectangle: $7\\times5=35$', 'Rectangle: $8\\times5=40$'), ('Rectangle: 7 × 5 = 35', 'Rectangle: 8 × 5 = 40'),
        ('The rectangle: 35 squares — area 35.', 'The rectangle: 40 squares — area 40.'),
        ('Write 1 in the upper-left triangle', 'Write 3 in the upper-left triangle'),
        ('Upper left: legs 1 and 2. 1 times 2 over 2 — 1.', 'Upper left: legs 3 and 2. 3 times 2 over 2 — 3.'),
        ('Write 6 in the upper-right triangle', 'Write 5 in the upper-right triangle'),
        ('Upper right: legs 6 and 2 — 6.', 'Upper right: legs 5 and 2 — 5.'),
        ('35-(1+6+3+3)=22', '40-(3+5+3+3)=26'), ('35 − (1+6+3+3) = 22', '40 − (3+5+3+3) = 26'),
        ('All the white together: 13. 35 minus 13 — 22.', 'All the white together: 14. 40 minus 14 — 26.'),
        ('middle 3-by-3 block', 'middle 4-by-3 block'), ('is 9 whole squares', 'is 12 whole squares'),
        ('7+9+3+3=22', '8+12+3+3=26'), ('7 + 9 + 3 + 3 = 22', '8 + 12 + 3 + 3 = 26'),
        ('Write 7 in the top triangle', 'Write 8 in the top triangle'),
        ('a triangle on the full 7-by-2 rectangle — a triangle on the full base is half. Half of 14 — 7.',
         'a triangle on the full 8-by-2 rectangle — a triangle on the full base is half. Half of 16 — 8.'),
        ('Write 9 in the middle 3-by-3 square', 'Write 12 in the middle 4-by-3 rectangle'),
        ('Below: the middle square, 3 by 3 — 9.', 'Below: the middle rectangle, 4 by 3 — 12.'),
        ('Add up: 7 plus 9 plus 3 plus 3 — 22.', 'Add up: 8 plus 12 plus 3 plus 3 — 26.')],
        svg=_rn_g070())

    # ---------- g071: angle B 110, plug 100 / 70  ==>  angle B 130, plug 110 / 60 (Hebrew: B 90, plug 100 / 70); choices reordered
    q = 'geo32-g071'; vid = 'solve-' + q
    _rn_guided(M, q, 'In quadrilateral ABCD, angle A is α, angle B is 130° and angle C is β. E lies on AB, and DE bisects angle ADC. '
               'Which expression equals angle AED?',
               ['$65°+\\frac\\alpha2-\\frac\\beta2$', '$130°+\\frac\\alpha2-\\frac\\beta2$', '$65°-\\frac\\alpha2+\\frac\\beta2$', '$130°-\\frac\\alpha2+\\frac\\beta2$'], 3,
               ['Angle sum: $\\angle D=360°-130°-\\alpha-\\beta=230°-\\alpha-\\beta$.',
                'DE bisects it: $\\angle ADE=115°-\\frac\\alpha2-\\frac\\beta2$.',
                'Triangle AED: $\\angle AED=180°-\\alpha-\\left(115°-\\frac\\alpha2-\\frac\\beta2\\right)=65°-\\frac\\alpha2+\\frac\\beta2$.',
                'Check with numbers: $\\alpha=110°$ and $\\beta=60°$ give $\\angle D=60°$, $\\angle ADE=30°$ and $\\angle AED=40°$. Only choice 3 gives $65°-55°+30°=40°$.'],
               {1: 2, 2: 3, 3: 1, 4: 4}, [
        ('angle B is 110, angle C is beta.', 'angle B is 130, angle C is beta.'),
        ('360°-110°-\\alpha-\\beta$ $=250°', '360°-130°-\\alpha-\\beta$ $=230°'), ('360° − 110° − α − β = 250° − α − β', '360° − 130° − α − β = 230° − α − β'),
        ('Isolate D: 360 minus 110 is 250. D equals 250 minus alpha minus beta.', 'Isolate D: 360 minus 130 is 230. D equals 230 minus alpha minus beta.'),
        ('\\angle ADE=125°', '\\angle ADE=115°'), ('Half: 125° − α/2 − β/2', 'Half: 115° − α/2 − β/2'),
        ('Half of 250 is 125', 'Half of 230 is 115'), ('Write 125 − α/2 − β/2', 'Write 115 − α/2 − β/2'),
        ('\\left(125°', '\\left(115°'), ('x = 180° − α − (125° − α/2 − β/2)', 'x = 180° − α − (115° − α/2 − β/2)'),
        ('Write 180 − 125 = 55', 'Write 180 − 115 = 65'),
        ('180 minus 125 — 55. Notice: already choices two and four are out — the number must be 55, not 110.',
         '180 minus 115 — 65. Notice: already choices two and four are out — the number must be 65, not 130.'),
        ('55 minus alpha over 2 plus beta over 2.', '65 minus alpha over 2 plus beta over 2.')],
        fig={'110°': '130°'})
    b3 = M.slide(vid, 3)
    item = dict(b3['items'][b3['lines'][[l.get('appear') for l in b3['lines']].index(1)]['appear']])
    item['t'] = '$\\frac\\alpha2=55,\\ \\ \\frac\\beta2=30$'
    M.set_slide(vid, 3, script=[
        "The psychometric solution: plug in numbers.",
        "Pick some alpha, some beta. Plug them into the drawing AND into the answers. Find the answer that matches.",
        "That turns a complex question into a simple one — numbers are much easier to work with.",
        D('Write α = 110°, β = 60°'),
        "Alpha looks obtuse — I'll take 110. Beta — 60. You can pick others, as long as the drawing still works.",
        D('Write ∠D = 360 − 130 − 110 − 60 = 60 → 30, 30'),
        "Angle D: 110 plus 60 plus 130 is 300. 360 minus 300 — 60. Bisected — 30 and 30.",
        D('Write x = 180 − 110 − 30 = 40'),
        "Now the question mark is a joke: 110 plus 30 is 140. To 180 — 40 degrees.",
        "Now plug alpha 110 and beta 60 into every answer — and eliminate anything that isn't 40.",
        "The drawback of plugging in: to be sure, we have to eliminate the other answers.",
        A('α/2 = 55, β/2 = 30 appears', item),
        D('Next to the choices write 90, 155, 40, 105'),
        "Choice one: 65 plus 55 minus 30 — 90. Out. Choice two: 130 plus 55 minus 30 — 155. Out.",
        "Choice three: 65 minus 55 plus 30 — 40. It fits!",
        "Still — don't mark it yet. If you're out of time, it's a very reasonable guess.",
        "Choice four: 130 minus 55 plus 30 — 105. Out.",
        D('Cross out choices 1, 2 and 4'),
        D('Circle choice 3'),
        "Choice three.",
        "Two approaches. If you're strong in algebra and do it in under a minute — great, solve it fully.",
        "For most students the full algebra is hard — especially at the end of a section under time pressure. Plugging in is a wonderful solution for that.",
    ])

    # ---------- g072: six congruent rectangles, perimeter 50 -> 150  ==>  perimeter 40 -> x 2 -> 96 (Hebrew five, 32 -> 60)
    _rn_guided(M, 'geo32-g072', 'Rectangle ABCD consists of six congruent rectangles, arranged as in the accompanying figure. The perimeter of ABCD is 40 cm. '
               'What is its area (in cm²)?',
               ['$64$', '$80$', '$96$', '$128$'], 3,
               ['Call the short side of a small rectangle $x$. Four short sides stack up to one long side, therefore the long side is $4x$.',
                'The big rectangle is $4x$ by $x+4x+x=6x$. $P=2(4x+6x)=20x=40$, therefore $x=2$.',
                '$S=4x\\cdot6x=8\\cdot12=96$.'],
               {1: 3, 2: 2, 3: 1, 4: 4}, [
        ('Its perimeter is 50.', 'Its perimeter is 40.'),
        ('20x=50$ $\\Rightarrow\\ x=2.5', '20x=40$ $\\Rightarrow\\ x=2'), ('20x = 50 → x = 2.5', '20x = 40 → x = 2'),
        ("It's 50, so x is 2.5.", "It's 40, so x is 2."),
        ('10\\times15=150', '8\\times12=96'), ('S = 10 × 15 = 150', 'S = 8 × 12 = 96'),
        ('4x is 10, 6x is 15. 10 times 15 — 150.', '4x is 8, 6x is 12. 8 times 12 — 96.'),
        ('Half the perimeter is 25 — five parts, so one part is 5: sides 15 and 10. Same 150.',
         'Half the perimeter is 20 — five parts, so one part is 4: sides 12 and 8. Same 96.'),
        ('20x, must be 50.', '20x, must be 40.'),
        ('150\\div24=6.25=2.5^2', '96\\div24=4=2^2'), ('150 ÷ 24 = 6.25 = 2.5²', '96 ÷ 24 = 4 = 2²'),
        ("Try choice three, 150. 150 divided by 24 is 6.25 — that's 2.5 squared. So x is 2.5.",
         "Try choice three, 96. 96 divided by 24 is 4 — that's 2 squared. So x is 2."),
        ('20\\cdot2.5=50', '20\\cdot2=40'), ('20 · 2.5 = 50', '20 · 2 = 40'),
        ('the perimeter: 20 times 2.5 — 50.', 'the perimeter: 20 times 2 — 40.'),
        ('Try 100, 125 or 200: divided by 24, none of them gives a perimeter of 50.',
         'Try 64, 80 or 128: divided by 24, none of them gives a perimeter of 40.')])


def _rn_p(M, qid, stem, choices, correct, expl, fig=None, svg=None, aria=None):
    if qid in RN_RECORDED: return
    _rn_q(M, qid, stem, choices, correct, expl)
    if fig is not None or svg is not None: _rn_fig(M, qid, fig, aria, svg)


def rn_practice_questions(M):
    F = lambda k: 'geo32-foundation-p%02d' % k
    Ad = lambda k: 'geo32-advanced-p%02d' % k
    # ---------------- foundation ----------------
    _rn_p(M, F(1), 'A congruent isosceles triangle is constructed externally on each side of square ABCD. The square has perimeter 48 cm, '
          'and each triangle has perimeter 34 cm. What is the perimeter of the resulting figure (in cm)?',
          ['$88$', '$112$', '$136$', '$184$'], 1,
          ['The four triangles have a total perimeter of $4\\cdot34=136$.',
           'Their bases are the sides of the square, $48$ in total. They are inside the figure, therefore they are not part of its perimeter.',
           '$P=136-48=88$.'])
    _rn_p(M, F(2), 'ABCD is an isosceles trapezoid with $AD\\parallel BC$. Given: $y=x+46°$. What is x?',
          ['$44°$', '$67°$', '$90°$', '$113°$'], 2,
          ['In an isosceles trapezoid, opposite angles add up to $180°$ (angles on the same leg add up to $180°$, and the base angles are equal).',
           '$x+y=180°$: $x+x+46°=180°$, $2x=134°$ and $x=67°$.'])
    _rn_p(M, F(3), 'ABCD is an isosceles trapezoid with $AD\\parallel BC$. Angle ABC is $3k$. Which expression equals β?',
          ['$90°-3k$', '$180°-k$', '$180°-3k$', '$90°+3k$'], 3,
          ['Isosceles trapezoid: the base angles are equal, $\\angle BCD=\\angle ABC=3k$.',
           'β and angle C sit on the same leg CD: $\\beta=180°-3k$.'], fig={'2t': '3k'})
    _rn_p(M, F(4), 'ABCD is a parallelogram. BE bisects angle ABC and meets AD at E. Given: angle BCD is 136°. What is angle AEB?',
          ['$22°$', '$44°$', '$68°$', '$112°$'], 1,
          ['$\\angle ABC=180°-136°=44°$, and BE bisects it: $\\angle EBC=\\frac{44°}{2}=22°$.',
           '$AD\\parallel BC$, therefore $\\angle AEB=\\angle EBC=22°$ (Z-angles).'], fig={'124°': '136°'})
    _rn_p(M, F(5), 'The side length of an equilateral triangle equals the perimeter of a square. The triangle’s perimeter is 252 cm. '
          'What is the side length of the square (in cm)?',
          ['$21$', '$28$', '$63$', '$84$'], 1,
          ['The side of the triangle is $\\frac{252}{3}=84$.',
           'This is the perimeter of the square, therefore each side of the square is $\\frac{84}{4}=21$.'])
    _rn_p(M, F(6), 'ABCD is a parallelogram. The two additional lines through A and C are parallel. Based on this information and the information '
          'in the figure, what is $x+y+z$?',
          ['$120°$', '$180°$', '$270°$', '$360°$'], 2,
          ['The two added lines are parallel, and $AB\\parallel DC$. By the parallel-line angles, the angle between CB and the line through C equals x.',
           'So the whole angle at C is $x+z$, and angle B is y.',
           'Adjacent angles of a parallelogram add up to $180°$: $x+y+z=180°$.'], fig={'α': 'x', 'β': 'y', 'γ': 'z'})
    _rn_p(M, F(7), 'A rhombus has perimeter 44 cm. Which of the following lengths cannot be the length of its longer diagonal (in cm)?',
          ['$16$', '$18$', '$21$', '$23$'], 4,
          ['Each side is $\\frac{44}{4}=11$.',
           'A diagonal and two sides make a triangle, therefore the diagonal is shorter than $11+11=22$. 23 is impossible.',
           'The longer diagonal is at least the diagonal of a square with side 11: $11\\sqrt2\\approx15.6$. So 16, 18 and 21 are all possible.'])
    _rn_p(M, F(8), None, ['Two side-length segments and two diagonal-length segments', 'Four side-length segments',
                          'Three side-length segments and one diagonal-length segment', 'One side-length segment and three diagonal-length segments'], 2, None)
    _rn_p(M, F(9), None, ['$49$', '$120$', '$156$', '$169$'], 2,
          ['Complete the figure to a $13\\times13$ square, and take away the missing $7\\times7$ square.',
           '$S=13^2-7^2=169-49=120$.'], svg=_rn_p09())
    _rn_p(M, F(10), 'The rectangle consists of 35 congruent unit squares. What is the shaded area?',
          ['$8$', '$19$', '$27$', '$31$'], 3,
          ['Each white kite has perpendicular diagonals 4 and 2: $S=\\frac{4\\cdot2}{2}=4$. The two kites: $8$.',
           'The rectangle is 35, therefore the shaded area is $35-8=27$.'], svg=_rn_p10())
    _rn_p(M, F(11), None, ['$30°$', '$60°$', '$90°$', '$120°$'], 3, None)
    _rn_p(M, F(12), None, ['$26°$', '$52°$', '$64°$', '$74°$'], 3,
          ['Both horizontal lines are perpendicular to the right vertical line, therefore they are parallel.',
           'The downward sloping line makes $26°$ with either horizontal line.',
           'Its perpendicular therefore makes $90°-26°=64°$ with the horizontal line: $\\alpha=64°$.'], fig={'32°': '26°'})
    _rn_p(M, F(13), 'The perimeter of a rectangle is 17 cm, and one side is 6 cm long. What is its area (in cm²)?',
          ['$5$', '$15$', '$30$', '$34$'], 2,
          ['The other side: $\\frac{17-2\\cdot6}{2}=\\frac52=2.5$.', '$S=6\\cdot2.5=15$.'])
    _rn_p(M, F(14), None, ['A square', 'A rhombus', 'A rectangle', 'A kite'], 3,
          ['Square, rhombus and kite: the diagonals are always perpendicular.',
           'Rectangle: the diagonals are equal and bisect each other, but they are not necessarily perpendicular. Example: a $6\\times2$ rectangle.'])
    _rn_p(M, F(15), None, ['$85°$', '$95°$', '$109°$', '$119°$'], 2,
          ['Look at the quadrilateral formed by AB, the two long lines and the perpendicular. Three of its angles are $104°$, $71°$ and $90°$.',
           'Its angle at A: $360°-104°-71°-90°=95°$.',
           '$AB\\parallel CD$, so α is the corresponding angle: $\\alpha=95°$.'], fig={'101°': '104°', '67°': '71°'})
    _rn_p(M, F(16), 'The vertices of the inscribed rhombus are the midpoints of the rectangle’s sides. A half-side of the rectangle is 9 cm and a side '
          'of the rhombus is 15 cm, as marked. What is the perimeter of the rectangle (in cm)?',
          ['$42$', '$60$', '$66$', '$84$'], 4,
          ['Each corner triangle is right-angled: hypotenuse 15 and one leg 9. The other leg is 12 ($9, 12, 15$).',
           'The rectangle is $2\\cdot9=18$ by $2\\cdot12=24$.', '$P=2(18+24)=84$.'], svg=_rn_p16())
    _rn_p(M, F(17), 'Ten congruent rhombuses meet at a common vertex with no gaps or overlaps, as in the accompanying figure. What is α?',
          ['$30°$', '$36°$', '$40°$', '$144°$'], 2,
          ['10 equal angles meet at the center: each is $\\frac{360°}{10}=36°$.',
           'Opposite angles of a rhombus are equal: $\\alpha=36°$.'], svg=_rn_p17())
    _rn_p(M, F(18), 'A square with perimeter 48 cm is divided into 12 congruent rectangles in three rows and four columns. '
          'What is the perimeter of each small rectangle (in cm)?',
          ['$7$', '$12$', '$14$', '$16$'], 3,
          ['The side of the square is $\\frac{48}{4}=12$.',
           'Each small rectangle is $\\frac{12}{4}=3$ wide and $\\frac{12}{3}=4$ tall.', '$P=2(3+4)=14$.'], svg=_rn_p18())
    _rn_p(M, F(19), 'ABCD is a kite, and its diagonals intersect at O. Given:\n' +
          _cases('AB=AD=13' + CM, 'CB=CD', 'BO=5' + CM, 'OC=8' + CM) + '\nWhat is its area (in cm²)?',
          ['$50$', '$100$', '$130$', '$200$'], 2,
          ['$OD=BO=5$, therefore $BD=5+5=10$.',
           'Right triangle ABO: $5, 12, 13$, therefore $AO=12$ and $AC=12+8=20$.',
           '$S=\\frac{10\\cdot20}{2}=100$.'], svg=_rn_p19())
    _rn_p(M, F(20), 'Maya says: “Knowing a rhombus’s perimeter is enough to determine its area.” Ethan says: “Knowing a square’s perimeter is '
          'enough to determine its area.” Which statement is correct?',
          ['Both are correct', 'Maya is correct and Ethan is incorrect', 'Ethan is correct and Maya is incorrect', 'Both are incorrect'], 3,
          ['Square: the perimeter gives the side, and the side gives the area. Ethan is correct.',
           'Rhombus: the perimeter gives the side, but the angles can change. A rhombus with side 6 can be a square (area 36) or very flat '
           '(area close to 0). Maya is incorrect.'])

    # ---------------- advanced ----------------
    _rn_p(M, Ad(1), 'All the rectangles in the accompanying figure are congruent. The shorter side of each rectangle is 3 cm. '
          'What is its longer side (in cm)?',
          ['$8$', '$9$', '$10$', '$12$'], 2,
          ['Call the longer side $L$. The upper row is $L+3+L$ wide, and the lower row is $6+L+6$ wide.',
           '$2L+3=L+12$, therefore $L=9$.'], fig={'2': '3'})
    _rn_p(M, Ad(2), 'ABCD is a rectangle and E lies on AD. Triangle EBC has area 23 cm², and triangle ECD has area 9 cm². '
          'What is the shaded area of triangle ABE (in cm²)?',
          ['$9$', '$14$', '$23$', '$32$'], 2,
          ['EBC stands on the full base BC, with its tip on AD. It is half the rectangle.',
           'The two corner triangles make the other half: $S_{ABE}+S_{ECD}=23$.', '$S_{ABE}=23-9=14$.'], svg=_rn_a02())
    _rn_p(M, Ad(3), 'ABCD is an isosceles trapezoid with $AD\\parallel BC$. Given:\n' + _cases('AB=13' + CM, 'BC=26' + CM, '\\angle BAC=90°') +
          '\nWhat is α?',
          ['$60°$', '$120°$', '$135°$', '$150°$'], 2,
          ['In right triangle ABC, $BC=26=2\\cdot AB$. The hypotenuse is twice a leg, therefore it is a 30-60-90 triangle: $\\angle ACB=30°$ and $\\angle ABC=60°$.',
           'The angles on leg AB add up to $180°$, and the trapezoid is isosceles: each top angle is $180°-60°=120°$. $\\alpha=120°$.'],
          fig={'9': '13', '18': '26'})   # review: 11/22 = the t31 lesson example (geo-026) -> 13/26
    _rn_p(M, Ad(4), 'ABCD is a square with side length 12 cm. Triangle AED is equilateral and lies inside the square. F lies on AB, with '
          '$EF\\parallel AD$. What is the area of the shaded triangle AFE (in cm²)?',
          ['$18\\sqrt3$', '$9\\sqrt3$', '$36\\sqrt3$', '$18\\sqrt2$'], 1,
          ['The height of an equilateral triangle with side 12 is $\\frac{12\\sqrt3}{2}=6\\sqrt3$. So $AF=6\\sqrt3$.',
           'By symmetry, E is above the middle of AD: $FE=\\frac{12}{2}=6$.', '$S=\\frac{6\\cdot6\\sqrt3}{2}=18\\sqrt3$.'], fig={'8': '12'})
    _rn_p(M, Ad(5), 'ABCD is an isosceles trapezoid with $AD\\parallel BC$. Given:\n' + _cases('AB=AD=CD', '\\angle DAC=2m') +
          '\nWhich expression equals β?',
          ['$4m$', '$180°-4m$', '$2m+45°$', '$2m+60°$'], 1,
          ['$AD=CD$, therefore triangle ADC is isosceles: $\\angle ACD=\\angle DAC=2m$.',
           '$AD\\parallel BC$ (Z-angles): $\\angle ACB=\\angle DAC=2m$.',
           '$\\angle C=2m+2m=4m$, and the base angles are equal: $\\beta=4m$.'], fig={'2t': '2m'})
    _rn_p(M, Ad(6), 'ABCD is a square with side length 5 cm, and BEFD is a rectangle. Given: angle CBF is 15°. What is BF (in cm)?',
          ['$5\\sqrt2$', '$10$', '$10\\sqrt2$', '$10\\sqrt3$'], 3,
          ['$BD=5\\sqrt2$ (the diagonal of the square), and it makes a $45°$ angle with BC.',
           '$\\angle DBF=45°+15°=60°$. BEFD is a rectangle, therefore $\\angle BDF=90°$.',
           'Triangle BDF is a 30-60-90 triangle. BD is opposite the $30°$ angle, therefore $BF=2\\cdot BD=10\\sqrt2$.'], fig={'3': '5'})
    _rn_p(M, Ad(7), 'ABCD is a kite. Given:\n' + _cases('AB=AD', 'CB=CD', '\\angle A=3n', '\\angle C=n') + '\nWhich expression equals angle ADC?',
          ['$180°-2n$', '$90°-2n$', '$360°-2n$', '$180°-4n$'], 1,
          ['The kite is symmetric about AC, therefore $\\angle B=\\angle D$.',
           '$2\\angle D=360°-3n-n=360°-4n$, therefore $\\angle ADC=180°-2n$.'], fig={'3t': '3n', 't': 'n'})
    _rn_p(M, Ad(8), 'In rectangle ABCD, E lies on CD, and $DE=4EC$. The areas of triangles AED, AEC and ABC are x, y and z, respectively. '
          'What is the ratio $x:y:z$?',
          ['$1:4:5$', '$4:1:4$', '$4:1:5$', '$4:5:1$'], 3,
          ['AED and AEC have the same height from A, and their bases are in the ratio $DE : EC=4 : 1$. So $x : y=4 : 1$.',
           'The diagonal AC halves the rectangle: $z=x+y$.', 'With $x=4$ and $y=1$: $z=5$. The ratio is $4 : 1 : 5$.'], svg=_rn_a08())
    _rn_p(M, Ad(9), 'A square of side length 14 cm contains five congruent squares of side length 2 cm, at its corners and center as in the '
          'accompanying figure. The four remaining regions are congruent under quarter-turns. What is the total area of the two shaded regions (in cm²)?',
          ['$44$', '$88$', '$98$', '$176$'], 2,
          ['The four congruent regions: $14^2-5\\cdot2^2=196-20=176$.', 'Two of them: $\\frac{176}{2}=88$.'])
    _rn_p(M, Ad(10), 'Two congruent rectangles are placed together to form a square, as in the accompanying figure. Each rectangle has perimeter 84 cm. '
          'What is the square’s perimeter (in cm)?',
          ['$84$', '$112$', '$126$', '$168$'], 2,
          ['Each rectangle is $s$ by $\\frac s2$. Its perimeter: $2\\left(s+\\frac s2\\right)=3s=84$, therefore $s=28$.', '$P=4\\cdot28=112$.'])
    _rn_p(M, Ad(11), 'A quadrilateral is both a parallelogram and a kite. Its perimeter is 52 cm. Which of the following is necessarily true?',
          ['Each side is 13 cm long', 'Its diagonals have equal lengths', 'Every angle is 90°', 'Its area is 169 cm²'], 1,
          ['A parallelogram has equal opposite sides. A kite has two pairs of equal adjacent sides.',
           'Together, all four sides are equal: it is a rhombus. Each side is $\\frac{52}{4}=13$.',
           'The other statements are true only for a square.'])
    _rn_p(M, Ad(12), 'ABCD is a rectangle. The two sloping lines meet at C and form an angle of 36°. The two angles marked α are equal. What is α?',
          ['$27°$', '$36°$', '$54°$', '$63°$'], 1,
          ['$AD\\parallel BC$: the angle between the shallow line and AD equals the angle between that line and CB at C (Z-angles). That angle at C is α.',
           'The right angle at C is made of α, $36°$ and α: $2\\alpha+36°=90°$, therefore $\\alpha=27°$.'], fig={'28°': '36°'})
    _rn_p(M, Ad(13), 'ABCD is a square. Isosceles triangles AFB and AED are constructed outside it. Given:\n' +
          _cases('FA=FB', 'EA=ED', '\\angle AFB=2m', '\\angle AED=2n') + '\nWhich expression equals the marked angle FAE?',
          ['$90°+m+n$', '$180°-m-n$', '$90°-m-n$', '$180°+m+n$'], 1,
          ['Triangle AFB: $\\angle FAB=\\frac{180°-2m}{2}=90°-m$. Triangle AED: $\\angle EAD=90°-n$.',
           'The angles around A add up to $360°$: $x+(90°-m)+90°+(90°-n)=360°$.', '$x=90°+m+n$.'], fig={'2p': '2m', '2q': '2n'})
    _rn_p(M, Ad(14), 'ABCD is a rectangle with perimeter 46 cm. E lies on AB, and F lies on CD. Given:\n' + _cases('BE=DF', 'EF=11' + CM) +
          '\nWhat is the perimeter of quadrilateral AEFD (in cm)?',
          ['$23$', '$28$', '$34$', '$35$'], 3,
          ['$BE=DF$, therefore $AE+FD=AE+EB=AB$.', '$AE+FD+AD=AB+AD=\\frac{46}{2}=23$.', 'Add the cut: $P=23+11=34$.'], fig={'7': '11'})
    _rn_p(M, Ad(15), 'EF divides rectangle ABCD into two smaller rectangles. The sum of their perimeters is 16 cm greater than the perimeter of ABCD. '
          'Given: $CD=13$ cm. What is the area of the shaded triangle EDC (in cm²)?',
          ['$26$', '$52$', '$104$', '$208$'], 2,
          ['The two small perimeters contain every outer side once and the cut EF twice: $2\\cdot EF=16$, therefore $EF=8$.',
           'EF is the height from E to CD: $S=\\frac{13\\cdot8}{2}=52$.'], fig={'14': '13'})
    _rn_p(M, Ad(16), 'ABCD is a square. E lies on BC. The shaded triangle AEC has area 42 cm², which is $\\frac7{24}$ of the square’s area. '
          'What is BE (in cm)?',
          ['$4$', '$5$', '$6$', '$7$'], 2,
          ['The square: $\\frac{42\\cdot24}{7}=144$, therefore its side is 12.',
           'Triangle AEC has height $AB=12$ to the base EC: $\\frac{12\\cdot EC}{2}=42$, therefore $EC=7$.', '$BE=12-7=5$.'])
    _rn_p(M, Ad(17), 'ABCD is a trapezoid, and $a>0$. Given:\n' + _cases('AD\\parallel BC', 'AD=3a', 'BC=7a') +
          '\nE and F lie on BC. The area of trapezoid AEFD equals the combined areas of the two shaded triangles. What is EF?',
          ['$a$', '$2a$', '$3a$', '$4a$'], 2,
          ['The inner trapezoid is half of the whole area, with the same height. So the sum of its bases is half of $3a+7a=10a$: it is $5a$.',
           '$3a+EF=5a$, therefore $EF=2a$.'], svg=_rn_a17())
    _rn_p(M, Ad(18), 'ABCD is a parallelogram, and AECF is a square. Given: $AD=15$ cm. The parallelogram’s area is 3 times as much as the square’s area. '
          'What is AE (in cm)?',
          ['$3$', '$5$', '$6$', '$10$'], 2,
          ['Call $AE=x$. It is the side of the square and also the height of the parallelogram to BC, and $BC=AD=15$.',
           '$15x=3x^2$. Divide by $3x$ (it is not 0): $x=5$.'], fig={'12': '15'})
    _rn_p(M, Ad(19), 'Four squares with areas $a^2$, $b^2$, $c^2$ and $d^2$ are arranged as in the accompanying figure, where $0<a<b<c<d$. '
          'What is the perimeter of the resulting figure?',
          ['$2a+2b+2c+2d$', '$2b+2c+4d$', '$4a+4b+c+d$', '$3a+2c+3d$'], 2,
          ['The four squares have a total perimeter of $4(a+b+c+d)$.',
           'The shared edges ($c$, $b$ and $2a$ in total) are inside the figure, and each was counted twice. Take away $2(c+b+2a)$.',
           '$4a+4b+4c+4d-2c-2b-4a=2b+2c+4d$.'], fig={'s²': 'd²', 'r²': 'c²', 'q²': 'b²', 'p²': 'a²'})
    _rn_p(M, Ad(20), 'Two rectangles overlap at an angle of 45°, forming the shaded parallelogram. Their widths are 5 cm and $3\\sqrt2$ cm, as marked. '
          'What is the shaded area (in cm²)?',
          ['$15$', '$15\\sqrt2$', '$30$', '$60$'], 3,
          ['The tilted side inside the vertical strip is the hypotenuse of a 45-45-90 triangle with leg $3\\sqrt2$. Its length is $3\\sqrt2\\cdot\\sqrt2=6$.',
           'The height to that side is the width of the tilted rectangle: 5.', '$S=6\\cdot5=30$.'], fig={'4√2': '3√2', '6': '5'})


def rn_practice(M):
    """Approved clean-up (62 -> 48): copies, 8 of the 12 English extras (keep 4), 3 September items whose type the Hebrew practice has."""
    out = ['q-r26-t32-18',          # copy of q-r26-t32-09 (parallelogram with a special angle)
           'geo32-advanced-p21',    # copy of guided q-r26-t32-07 (perimeter + diagonal -> area)
           'geo32-foundation-p22',  # copy: rhombus from its diagonals (guided g051 type, adv-p23)
           'geo32-foundation-p25',  # = the lesson example (diagonal +50% -> area up 125%)
           'geo32-foundation-p26', 'geo32-foundation-p27', 'geo32-foundation-p21',
           'geo32-advanced-p26', 'geo32-advanced-p23', 'geo32-advanced-p25', 'geo32-advanced-p24',
           'q-r26-t32-13',          # midpoint quadrilateral: Hebrew foundation p16
           'q-r26-t32-21',          # rhombus from rectangle midpoints, a triple: Hebrew foundation p16
           'q-r26-t32-20']          # trapezoid + special triangle: Hebrew advanced p03 (and = q-08 drop-a-height)
    for qid in out:
        assert M.section_of(qid) in (FOUND, ADVP), qid
        M.unplace(qid)
    f = lambda *k: ['geo32-foundation-p%02d' % x for x in k]
    a = lambda *k: ['geo32-advanced-p%02d' % x for x in k]
    p = lambda *k: ['q-r26-t32-%02d' % x for x in k]
    M.practice_order(FOUND, f(13, 14, 5, 8, 18, 9, 4, 12, 3, 2, 17, 11) + p(9) + f(24) + p(12) + f(23, 19) + p(8) + f(16, 6, 15, 10, 7, 20, 1))
    M.practice_order(ADVP, a(9, 27, 16, 2, 7, 11, 3, 5, 12, 13, 4, 6, 10, 1, 15, 14) + p(17) + a(19, 22, 8, 17, 18, 20))


def rn_lessons_cards(M):
    # summary 2: "a third of the base -> a sixth" was the Hebrew lesson example -> a fifth -> a tenth
    vid = 'r26-t32-summary-2'
    _rn_sub(M, vid, [('On $\\frac13$ of the base: $\\frac13\\times\\frac12=\\frac16$', 'On $\\frac15$ of the base: $\\frac15\\times\\frac12=\\frac1{10}$'),
                     ('On a third of the base? A third of a half — one sixth.', 'On a fifth of the base? A fifth of a half — one tenth.')])
    # the perimeter card copied the staircase question (12 wide, 8 tall)
    c = M.card('mem-r26-t32-perimeter')
    c['tips'] = ['Area and perimeter are different questions: $9\\times5$ is an area, $2(9+5)$ is a perimeter.']


def renumber_pass(M):
    rn_guided(M)
    rn_practice_questions(M)
    rn_practice(M)
    rn_lessons_cards(M)


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
    # Q3 (parallelogram, 3α/2α and 3β/2β): only α + β is fixed -> pick values that fit (topic 51, later) + slide
    _sp_line(M, 'geo32-g048', r'Shortcut · Pick values that fit: only $\alpha+\beta=36°$ is fixed, and the question expects one x, so any pair that fits will do. Take $\alpha=\beta=18°$: angles B and C are $5\cdot18°=90°$ (a rectangle — still a parallelogram), and $x=180°-54°-54°=72°$.')
    _sp_slide(M, 'geo32-g048', 3, 'Shortcut · Pick values that fit', [
        "A faster way. Only alpha plus beta is fixed — 36. The question expects one x, so any alpha and beta that fit will do.",
        A("'α = β = 18°' appears", T(r'$\alpha=\beta=18°$', size=40, x=1060, y=250, w=470)),
        "Take them equal: 18 and 18.",
        A("'B = C = 5 · 18° = 90°' appears", T(r'$\angle B=\angle C=5\cdot18°=90°$', size=34, x=1060, y=330, w=470)),
        "Then angles B and C are 90 each. The parallelogram is a rectangle — that's allowed, a rectangle is a parallelogram.",
        A("'x = 180° − 54° − 54° = 72°' appears", T(r'$x=180°-54°-54°=72°$', size=34, x=1060, y=410, w=470)),
        "In triangle BCE: 3 alpha is 54, and 3 beta is 54. x is 180 minus 108 — 72.",
        D('Circle choice 2'),
        "Choice two."])
    # advanced practice (isosceles trapezoid, three equal sides): half a regular hexagon fits -> pick values that fit
    _sp_line(M, 'geo32-advanced-p05', r'Shortcut · Pick values that fit: half of a regular hexagon fits every given (three equal sides, the long base parallel to the short one). There $\angle D=120°$, so $\angle DAC=\frac{180°-120°}{2}=30°$ and $m=15°$, and $\beta=60°$. The choices give $60°$, $120°$, $75°$ and $90°$: only $4m$ fits.')
    # advanced practice (square with two isosceles triangles): both equilateral fits -> pick values that fit
    _sp_line(M, 'geo32-advanced-p13', r'Shortcut · Pick values that fit: take both triangles equilateral, $m=n=30°$. Then $\angle FAB=\angle EAD=60°$ and $x=360°-60°-90°-60°=150°$. The choices give $150°$, $120°$, $30°$ and $240°$: only choice 1.')


_apply_before_spread = apply


def apply(M):
    _apply_before_spread(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last
