# Quantitative Reasoning · Topic 51 · Psychometric Thinking (the "super-methods").
# Backbone: the teacher's five Hebrew lessons (pt_src/seg1-seg5): intro, plugging in the answers, plugging in numbers,
# order-of-magnitude estimation, insight questions. Every example the teacher solves is a course-book question
# (book pp. 11-19, 23 questions, key on p. 20); all 23 are solved in guided videos, in the teacher's order.
import math
from dsl import *
from vbank import _q
from math_api import rich_html, rich_plain

T51 = 51


# =====================================================================================================================
# figures (same style as the geometry questions: ink #203344, accent #087f83, DejaVu Sans 20)
# =====================================================================================================================
INK, ACC, FILL = '#203344', '#087f83', '#d5f1ed'
FONT = 'font-family="DejaVu Sans,Arial,sans-serif"'


def _svg(vb, label, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, label, label, body))


def _t(x, y, s, size=20, color=INK, anchor='middle', italic=False):
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" dominant-baseline="middle" fill="%s" %s font-size="%d"%s>%s</text>'
            % (x, y, anchor, color, FONT, size, ' font-style="italic"' if italic else '', s))


def _l(p, q, color=INK, w=2.5, dash=None):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (p[0], p[1], q[0], q[1], color, w, ' stroke-dasharray="%s"' % dash if dash else ''))


def _poly(pts):
    return ' '.join('%.1f,%.1f' % p for p in pts)


def _unit(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]; n = math.hypot(dx, dy); return (dx / n, dy / n)


def _arc(c, p1, p2, r, color=ACC, w=2):
    """small angle arc at c between directions c->p1 and c->p2 (short way)."""
    u1, u2 = _unit(c, p1), _unit(c, p2)
    a = (c[0] + r * u1[0], c[1] + r * u1[1]); b = (c[0] + r * u2[0], c[1] + r * u2[1])
    cross = u1[0] * u2[1] - u1[1] * u2[0]
    return ('<path d="M %.1f %.1f A %.1f %.1f 0 0 %d %.1f %.1f" fill="none" stroke="%s" stroke-width="%s"/>'
            % (a[0], a[1], r, r, 1 if cross > 0 else 0, b[0], b[1], color, w))


def _mid_dir(c, p1, p2, d):
    u1, u2 = _unit(c, p1), _unit(c, p2); m = (u1[0] + u2[0], u1[1] + u2[1]); n = math.hypot(*m)
    return (c[0] + d * m[0] / n, c[1] + d * m[1] / n)


def _right(c, p1, p2, s=16):
    u1, u2 = _unit(c, p1), _unit(c, p2)
    a = (c[0] + s * u1[0], c[1] + s * u1[1]); b = (a[0] + s * u2[0], a[1] + s * u2[1]); d = (c[0] + s * u2[0], c[1] + s * u2[1])
    return '<polyline points="%s" fill="none" stroke="%s" stroke-width="1.8"/>' % (_poly([a, b, d]), ACC)


def fig_cube():
    """A cylinder inscribed in a cube with edge 3a (oblique drawing, like the book)."""
    s, dx, dy = 180, 70, -70
    TL, TR, BR, BL = (100, 120), (280, 120), (280, 300), (100, 300)
    b = lambda p: (p[0] + dx, p[1] + dy)
    out = []
    # hidden cube edges
    out += [_l(BL, b(BL), w=1.6, dash='6 5'), _l(b(BL), b(BR), w=1.6, dash='6 5'), _l(b(BL), b(TL), w=1.6, dash='6 5')]

    def ell(y0):
        pts = []
        for k in range(73):
            t = 2 * math.pi * k / 72; u = .5 + .5 * math.cos(t); v = .5 + .5 * math.sin(t)
            pts.append((TL[0] + u * s + v * dx, y0 + v * dy))
        return pts
    top, bot = ell(TL[1]), ell(BL[1])
    t0 = math.atan2(.5 * dx, .5 * s)       # extreme x of the ellipse
    ex = lambda y0, t: (TL[0] + (.5 + .5 * math.cos(t)) * s + (.5 + .5 * math.sin(t)) * dx, y0 + (.5 + .5 * math.sin(t)) * dy)
    out.append('<polygon points="%s" fill="%s" fill-opacity=".45" stroke="none"/>' % (_poly([ex(TL[1], t0), ex(BL[1], t0), ex(BL[1], t0 + math.pi), ex(TL[1], t0 + math.pi)]), FILL))
    out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.2"/>' % (_poly(bot), ACC))
    out.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="2.2"/>' % (_poly(top), FILL, ACC))
    out += [_l(ex(TL[1], t0), ex(BL[1], t0), ACC, 2.2), _l(ex(TL[1], t0 + math.pi), ex(BL[1], t0 + math.pi), ACC, 2.2)]
    # visible cube edges
    for p, q in [(TL, TR), (TR, BR), (BR, BL), (BL, TL), (TL, b(TL)), (TR, b(TR)), (b(TL), b(TR)), (b(TR), b(BR)), (BR, b(BR))]:
        out.append(_l(p, q))
    # edge label a
    x = b(TR)[0] + 22; y1, y2 = b(TR)[1], b(BR)[1]
    out.append(_l((x, y1 + 4), (x, y2 - 4), INK, 2))
    out.append('<path d="M %.1f %.1f l -6 12 l 12 0 Z M %.1f %.1f l -6 -12 l 12 0 Z" fill="%s"/>' % (x, y1, x, y2, INK))
    out.append(_t(x + 26, (y1 + y2) / 2, '3a', 24, italic=True))
    return _svg('70 30 355 290', 'A cylinder inscribed in a cube with edge 3a', ''.join(out))


def fig_triangles():
    """ABC right-angled at C, DBC isosceles (DB = DC), AB bisects angle DBC; alpha at A, beta where AB crosses DC."""
    al = math.radians(57)
    B, C = (110.0, 360.0), (410.0, 360.0)
    L = C[0] - B[0]
    A = (C[0], C[1] - L / math.tan(al))
    Dp = (B[0] + L / 2, C[1] - (L / 2) * math.tan(2 * (math.pi / 2 - al)))
    # intersection P of B->A and C->D
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = B, A, C, Dp
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    P = (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    out = ['<polygon points="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (_poly([B, C, Dp]), INK),
           _l(B, A), _l(A, C), _right(C, B, A, 16),
           _arc(A, B, C, 34), _t(*_mid_dir(A, B, C, 52), s='α', size=22, color=ACC),
           _arc(P, Dp, B, 28), _t(*_mid_dir(P, Dp, B, 48), s='β', size=22, color=ACC),
           _t(Dp[0], Dp[1] - 18, 'D'), _t(A[0] + 14, A[1] - 14, 'A'), _t(B[0] - 14, B[1] + 16, 'B'), _t(C[0] + 14, C[1] + 16, 'C')]
    return _svg('70 %.0f 380 %.0f' % (Dp[1] - 40, C[1] + 45 - (Dp[1] - 40)), 'Right triangle ABC and isosceles triangle DBC', ''.join(out))


def fig_sector():
    """Circle with center O, radius 2 cm; sector AOB of 45 degrees; AF perpendicular to OB; shaded = sector minus triangle."""
    O, R = (230.0, 250.0), 170.0
    pt = lambda deg, r=R: (O[0] + r * math.cos(math.radians(deg)), O[1] - r * math.sin(math.radians(deg)))
    B, A = pt(20), pt(65)
    F = pt(20, R * math.cos(math.radians(45)))
    shade = ('<path d="M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f Z" fill="%s" stroke="none"/>'
             % (F[0], F[1], B[0], B[1], R, R, A[0], A[1], FILL))
    lab = ((O[0] + A[0]) / 2 - 30, (O[1] + A[1]) / 2 + 4)
    out = [shade, '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="2.5"/>' % (O[0], O[1], R, INK),
           _l(O, A), _l(O, B), _l(A, F), _right(F, O, A, 14),
           _arc(O, B, A, 38), _t(*_mid_dir(O, B, A, 60), s='45°', size=18, color=ACC),
           '<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (O[0], O[1], INK),
           _t(O[0], O[1] + 22, 'O'), _t(A[0] - 6, A[1] - 18, 'A'), _t(B[0] + 18, B[1] + 4, 'B'), _t(lab[0], lab[1], '2 cm', 18)]
    return _svg('40 60 380 380', 'Sector AOB of a circle with radius 2 cm', ''.join(out))


def fig_rect():
    """Rectangle ABCD, height 4 cm, a quarter circle of radius 2 at each vertex, circle O tangent to all of them."""
    u = 90.0
    A = (110.0, 60.0); W = 2 * math.sqrt(3) * u; H = 2 * u
    D, B, C = (A[0] + W, A[1]), (A[0], A[1] + H), (A[0] + W, A[1] + H)
    O = (A[0] + W / 2, A[1] + H / 2)
    arcs = ['M %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f' % (A[0] + u, A[1], u, u, A[0], A[1] + u),
            'M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f' % (D[0] - u, D[1], u, u, D[0], D[1] + u),
            'M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f' % (B[0] + u, B[1], u, u, B[0], B[1] - u),
            'M %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f' % (C[0] - u, C[1], u, u, C[0], C[1] - u)]
    out = ['<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" stroke-width="2.5"/>' % (A[0], A[1], W, H, INK),
           '<path d="%s" fill="none" stroke="%s" stroke-width="2.2"/>' % (' '.join(arcs), ACC),
           '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="2.2"/>' % (O[0], O[1], u, ACC),
           '<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (O[0], O[1], INK), _t(O[0] + 4, O[1] + 20, 'O'),
           _t(A[0] - 14, A[1] - 14, 'A'), _t(D[0] + 14, D[1] - 14, 'D'), _t(B[0] - 14, B[1] + 16, 'B'), _t(C[0] + 14, C[1] + 16, 'C'),
           '<path d="M %.1f %.1f q -12 0 -12 12 L %.1f %.1f q 0 12 -12 12 q 12 0 12 12 L %.1f %.1f q 0 12 12 12" fill="none" stroke="%s" stroke-width="2"/>'
           % (A[0] - 10, A[1], A[0] - 22, O[1] - 12, A[0] - 22, B[1] - 12, INK),
           _t(A[0] - 58, O[1], '4 cm', 18)]
    return _svg('20 20 %.0f %.0f' % (W + 150, H + 80), 'Rectangle ABCD with quarter circles at its vertices and a circle O', ''.join(out))


def fig_square():
    """Square ABCD with side x cm; E on BC with EC = y cm; segment DE."""
    A, D, B, C = (110.0, 50.0), (330.0, 50.0), (110.0, 270.0), (330.0, 270.0)
    E = (C[0] - 72, B[1])
    out = ['<polygon points="%s" fill="none" stroke="%s" stroke-width="2.5"/>' % (_poly([A, D, C, B]), INK), _l(D, E),
           _t(A[0] - 12, A[1] - 14, 'A'), _t(D[0] + 12, D[1] - 14, 'D'), _t(B[0] - 14, B[1] + 16, 'B'), _t(C[0] + 14, C[1] + 16, 'C'),
           _t(E[0], E[1] + 18, 'E'),
           '<path d="M %.1f %.1f q -12 0 -12 12 L %.1f %.1f q 0 12 -12 12 q 12 0 12 12 L %.1f %.1f q 0 12 12 12" fill="none" stroke="%s" stroke-width="2"/>'
           % (A[0] - 10, A[1], A[0] - 22, 148, A[0] - 22, B[1] - 12, INK),
           _t(A[0] - 60, 160, 'x cm', 18),
           '<path d="M %.1f %.1f q 0 10 10 10 L %.1f %.1f q 8 0 8 10 q 0 -10 8 -10 L %.1f %.1f q 10 0 10 -10" fill="none" stroke="%s" stroke-width="2"/>'
           % (E[0] + 2, B[1] + 34, (E[0] + C[0]) / 2 - 8, B[1] + 44, C[0] - 12, B[1] + 44, INK),
           _t((E[0] + C[0]) / 2, B[1] + 72, 'y cm', 18)]
    return _svg('20 20 350 340', 'Square ABCD with a segment from D to E on side BC', ''.join(out))


# =====================================================================================================================
# questions (course book, chapter "Psychometric thinking", book pages 11-19; key on p. 20)
# =====================================================================================================================
QUESTIONS = {}


def mk(qid, page, n, stem, choices, key, steps, fig=None):
    q = _q(qid, T51, rich_plain(stem), [rich_plain(c) for c in choices], key, '',
           dict(subject='psychometric-thinking', trustRank=1, reviewFlag=False, source='Course book p.%d q%d (numbers changed)' % (page, n)))
    q.update(stem=rich_plain(stem), stemRich=stem, stemHtml=rich_html(stem),
             choices=[rich_plain(c) for c in choices], choicesRich=list(choices), choicesHtml=[rich_html(c) for c in choices],
             explanation=list(steps), answerHtml=''.join('<p>%s</p>' % rich_html(e) for e in steps),
             work=[], workText=[], methods=[dict(title='Worked solution', steps=list(steps), work=[], independent=False, board=[])],
             navLabel=rich_plain(stem.replace('\n', ' '))[:120])
    if fig: q['questionVisual'] = {'type': 'geometry', 'svg': fig}
    QUESTIONS[qid] = q


# ---- Introduction (book p. 11-12) ----
mk('pt-q01', 11, 1, r'$\sqrt{19{,}044}=?$', ['138', '156', '194', '212'], 1, [
    r'The square must end in 4. $156^2$ and $194^2$ end in 6 ($6\cdot6=36$, $4\cdot4=16$), so choices 2 and 3 are out.',
    r'$200^2=40{,}000$ is far more than 19,044, so 212 is too big.',
    r'Only 138 is left: $138^2=19{,}044$.'])
mk('pt-q02', 11, 2, r'Basket A contains 500 eggs, and basket B contains 600 eggs.' '\n'
    r'How many eggs must be moved from basket A to basket B so that basket A will contain $\frac{9}{13}$ of the number of eggs in basket B?',
   ['25', '50', '70', '85'], 2, [
    r'Move x eggs: basket A has $500-x$ eggs and basket B has $600+x$.',
    r'$500-x=\frac{9}{13}(600+x)$, so $6500-13x=5400+9x$, $22x=1100$ and $x=50$.',
    r'Or plug in the round answer 50: $\frac{450}{650}=\frac{9}{13}$.'])
mk('pt-q03', 11, 3, r'Given: $a\ne0$ and $b\ne0$.' '\n' r'$\frac{a^2+b^2+(a-b)^2}{2ab}+1=?$',
   [r'$\frac{a}{b}+\frac{b}{a}$', r'$\frac{a}{2b}+\frac{b}{2a}$', r'$\frac{(a+b)(a-b)}{ab}$', r'$2(a^2+b^2)$'], 1, [
    r'Open the brackets: $\frac{2a^2+2b^2-2ab}{2ab}+1=\frac{a}{b}+\frac{b}{a}-1+1=\frac{a}{b}+\frac{b}{a}$.',
    r'Or plug in $a=b=1$: the expression is $\frac{2}{2}+1=2$. Choices 2, 3 and 4 give 1, 0 and 4, so only choice 1 is left.'])
mk('pt-q04', 12, 4, r'A cylinder is inscribed in a cube whose edge is 3a (see figure).' '\n' r'What is the volume of the cylinder?',
   [r'$\frac{27\pi}{2}a^3$', r'$27\pi a^3$', r'$36\pi a^3$', r'$\frac{27\pi}{4}a^3$'], 4, [
    r'The diameter of the base equals the edge of the cube: $r=\frac{3a}{2}$, and the height is $h=3a$.',
    r'$V=\pi\left(\frac{3a}{2}\right)^2\cdot3a=\frac{27\pi a^3}{4}$.',
    r'Estimate: the cylinder is inside the cube, so its volume is less than $(3a)^3=27a^3$. With $\pi\approx3$, choices 1, 2 and 3 are all more than $27a^3$.'],
   fig_cube())
mk('pt-q05', 12, 5, r'Two fair dice, one blue and one red, are rolled.' '\n'
    r'What is the probability that the number obtained on the blue die will be at least as large as the number obtained on the red die?',
   [r'$\frac{37}{72}$', r'$\frac{1}{2}$', r'$\frac{2}{3}$', r'$\frac{7}{12}$'], 4, [
    r'There are 36 equally likely outcomes, and 6 of them are doubles (a tie).',
    r'By symmetry, the other 30 split equally: in 15 of them the blue die shows the greater number.',
    r'"At least as large" includes equal, so the 6 ties count too: $P=\frac{15+6}{36}=\frac{21}{36}=\frac{7}{12}$.'])

# ---- Plugging in the answers (book p. 13) ----
mk('pt-q06', 13, 1, 'x is an integer.\nGiven:\n' r'$\begin{cases} x^2<25 \\ 3x+6<0 \end{cases}$' '\n' r'$x=?$',
   ['1', '3', '$-4$', '$-7$'], 3, [
    r'Plug in the answers. $x=1$: $3\cdot1+6=9$, which is not less than 0. $x=3$ also gives a positive result.',
    r'$x=-4$: $(-4)^2=16<25$ and $3(-4)+6=-6<0$. Both hold. (For $x=-7$, $49$ is not less than 25.)'])
mk('pt-q07', 13, 2, r'Nadav and Amit have a total of 90 cards. Nadav has more cards than Amit. The difference between the numbers of cards the two of them have is equal to $\frac{1}{5}$ of the number of cards Nadav has.' '\n'
    'How many cards does Nadav have?', ['40', '43', '48', '50'], 4, [
    r'Nadav has more than half of 90, so 40 and 43 are out.',
    r'Plug in 50: Amit has 40, the difference is 10, and $\frac{1}{5}\cdot50=10$.'])
mk('pt-q08', 13, 3, 'Kobi bought a pair of pants at a 50% discount and a shirt at a 10% discount, and paid a total of 280 shekels instead of 500 shekels.\n'
    'What was the price of the shirt before the discount (in shekels)?', ['50', '75', '140', '150'], 2, [
    r'Shirt 50, pants 450: $225+45=270$. Shirt 150, pants 350: $175+135=310$. Shirt 140, pants 360: $180+126=306$. None is 280.',
    r'Shirt 75, pants 425: $212.5+67.5=280$.'])
mk('pt-q09', 13, 4, 'If Ron gives Miri 4 stamps, the number of stamps she has will be 2 times the number of stamps he will have. '
    'If it is known that the two of them now have the same number of stamps, how many stamps does Miri have now?',
   ['12', '8', '4', '16'], 1, [
    r'Plug in 12: both have 12. After Ron gives 4, Miri has 16 and Ron has 8, and $16=2\cdot8$.'])

# ---- Plugging in numbers (book p. 14-15) ----
mk('pt-q10', 14, 1, r'Given: $x\ge4$' '\n' r'$\sqrt{x+2-\sqrt{x^2-8x+16}}=?$', ['1', r'$\sqrt2$', r'$2\sqrt3$', r'$\sqrt6$'], 4, [
    r'For $x\ge4$: $\sqrt{x^2-8x+16}=\sqrt{(x-4)^2}=x-4$, so the expression is $\sqrt{x+2-(x-4)}=\sqrt6$.',
    r'Or plug in $x=4$: $\sqrt{6-\sqrt0}=\sqrt6$.'])
mk('pt-q11', 14, 2, r'In the accompanying figure, ABC is a right triangle, and DBC is an isosceles triangle ($DB=DC$).' '\n'
    'Given: AB bisects angle DBC.\n' r'Based on this information and the information in the figure, $\beta=?$',
   [r'$60°+\alpha$', r'$90°+\frac{\alpha}{2}$', r'$4\alpha-180°$', r'$270°-3\alpha$'], 4, [
    r'In triangle ABC: $\angle ABC=90°-\alpha$. AB bisects angle DBC, so $\angle DBC=180°-2\alpha$, and $\angle DCB$ is the same (base angles).',
    r'$\angle D=180°-2(180°-2\alpha)=4\alpha-180°$.',
    r'In the triangle formed by D, B and the vertex of $\beta$: $\beta=180°-(4\alpha-180°)-(90°-\alpha)=270°-3\alpha$.',
    r'Or plug in $\alpha=50°$: $\beta=120°$, while choices 1, 2 and 3 give $110°$, $115°$ and $20°$ (that is angle D, not $\beta$).'], fig_triangles())
mk('pt-q12', 14, 3, 'a is a positive integer.\n' r'$a!\cdot(a+2)!=?$',
   [r'$(2a+2)!$', r'$(a^2+2a)!$', r'$(a!)^2\cdot(a+2)$', r'$(a!)^2\cdot(a+1)(a+2)$'], 4, [
    r'$(a+2)!=(a+2)(a+1)\cdot a!$, so $a!\cdot(a+2)!=(a!)^2\cdot(a+1)(a+2)$.',
    r'Or plug in: $a=1$ gives 6 (choices 1 and 3 give 24 and 3); $a=2$ gives 48 (choice 2 gives $8!$).'])
mk('pt-q13', 15, 4, 'One pen contains x cm³ of ink. To write one word, y cm³ of ink are needed. '
    r"Hagai's supply of pens was enough for him to write $x^3y$ words." '\nHow many pens did Hagai have?',
   [r'$x^2y^2$', r'$x^3y$', r'$\frac{1}{x^2y^2}$', r'$\frac{1}{x^3y}$'], 1, [
    r'Each pen writes $\frac{x}{y}$ words, so the number of pens is $\frac{x^3y}{\frac{x}{y}}=x^2y^2$.',
    r'Or plug in $x=2$, $y=1$: 8 words, 2 words per pen, so 4 pens. Only choice 1 gives 4.'])
mk('pt-q14', 15, 5, 'Dana bought a dress at a discount of 40 shekels. The price of the dress after the discount was x shekels. '
    'What was the discount on the dress, in percent?',
   [r'$\frac{40\cdot100}{x+40}$', r'$\frac{40x}{100}$', r'$\frac{x+40}{100}$', r'$\frac{(x+40)\cdot100}{40}$'], 1, [
    r'The price before the discount was $x+40$, so the discount in percent is $\frac{40}{x+40}\cdot100=\frac{40\cdot100}{x+40}$.',
    r'Or put 100 at the whole: before 100, after $x=60$, a 40% discount. Only choice 1 gives 40.'])
mk('pt-q15', 15, 6, r'Orit and Batya decided to go on a trip and to share the expenses. Each of them undertook to pay $\frac{1}{2}$ of the total. '
    r'In the end, Orit paid only $\frac{1}{3}$ of the amount she had undertaken to pay, and Batya paid all the rest of the expenses.' '\n'
    'What is the ratio between the amount of money Batya actually paid and the amount of money she undertook to pay?',
   ['5 : 3', '2 : 1', '3 : 1', '5 : 1'], 1, [
    r'Say each of them undertook to pay 3 (6 in all). Orit paid $\frac{1}{3}\cdot3=1$, so Batya paid 5.',
    r'What Batya paid to what she undertook to pay: 5 : 3.'])
# ---- Picking values that fit (added 2026-10-06; original question, not from the book) ----
mk('pt-q24', 15, 7, r'Given: $x\ne-5$' '\n' r'$xy+5y=2x+10$' '\n' r'$y=?$',
   [r'$-5$', r'$-2$', '2', 'It cannot be determined from the given information'], 3, [
    r'One equation with two letters, and they ask for one value, so the answer is the same for every legal x. Pick $x=0$ (allowed, since $x\ne-5$): $5y=10$, so $y=2$.',
    r'Check with $x=1$: $y+5y=2+10$, $6y=12$, $y=2$ again, so y does not depend on x and "cannot be determined" is out.',
    r'Algebra: $xy+5y-2x-10=y(x+5)-2(x+5)=(x+5)(y-2)=0$. Since $x\ne-5$, $y-2=0$ and $y=2$.'])
QUESTIONS['pt-q24']['source'] = 'Original question (method: picking values that fit)'

# ---- Order-of-magnitude estimation (book p. 16-17) ----
mk('pt-q16', 16, 1, 'AOB is a sector of a circle with center O and a radius of 2 cm.\n'
    'Based on this information and the information in the figure, what is the area of the shaded region (in cm²)?',
   [r'$4-\pi$', r'$\frac{1}{2}\left(\frac{\pi}{2}-2\right)$', r'$\frac{\pi}{\sqrt2}$', r'$\frac{\pi}{2}-1$'], 4, [
    r'The circle has area $\pi\cdot2^2=4\pi$. The sector is $\frac{45}{360}=\frac18$ of it, so its area is $\frac{4\pi}{8}=\frac{\pi}{2}$.',
    r'The right triangle has legs $\sqrt2$ and $\sqrt2$, so its area is $\frac12\cdot\sqrt2\cdot\sqrt2=1$.',
    r'Shaded area: $\frac{\pi}{2}-1$.',
    r'Estimate: we need $\pi$ minus a number (choices 1 and 3 are out), and choice 2 is negative.'], fig_sector())
mk('pt-q17', 16, 2, r'$\frac{\sqrt2}{2+\sqrt2}=?$', [r'$(\sqrt2-1)^2$', r'$2\sqrt2$', r'$\sqrt2+1$', r'$\sqrt2-1$'], 4, [
    r'Multiply by $\frac{2-\sqrt2}{2-\sqrt2}$: $\frac{\sqrt2(2-\sqrt2)}{4-2}=\frac{2\sqrt2-2}{2}=\sqrt2-1$.',
    r'Or estimate with $\sqrt2\approx1.4$: $\frac{1.4}{3.4}\approx0.4$, and $1.4-1=0.4$.'])
mk('pt-q18', 16, 3, 'In the accompanying figure, each of the vertices of rectangle ABCD is the center of a circle with a radius of 2 cm. '
    'Point O is the center of a circle that is tangent to the four quarter circles and to sides AD and BC of the rectangle.\n'
    'What is the area of rectangle ABCD (in cm²)?', [r'$16\sqrt3$', r'$16\sqrt2$', '32', '40'], 1, [
    r'Circle O is tangent to AD and BC, so its radius is 2. It is tangent to the quarter circle at A, so $OA=2+2=4$.',
    r'O is 2 below AD, so its horizontal distance from A is $\sqrt{4^2-2^2}=\sqrt{12}=2\sqrt3$, and $AD=4\sqrt3$.',
    r'Area: $4\cdot4\sqrt3=16\sqrt3\approx27.2$.',
    r'Estimate: the width is between 6 and 8, so the area is between 24 and 32. Only $16\sqrt3\approx27.2$ fits.'], fig_rect())
mk('pt-q19', 17, 4, 'Bottle A contains 3.2 liters of a solution with an alcohol concentration of 20%. '
    'Bottle B contains 2 liters of a solution with an alcohol concentration of 3%.\n'
    'How many liters of alcohol are there in the two bottles together?', ['0.7', '0.95', '1.24', '3.1'], 1, [
    r'20% of 3.2 is 0.64. 3% of 2 is only 0.06, so the total is a little more than 0.64.',
    r'$0.64+0.06=0.7$.'])

# ---- Insights (book p. 18-19) ----
mk('pt-q20', 18, 1, r'$\frac{\frac{1}{5}+\frac{1}{6}}{\frac{2}{5}+\frac{2}{6}}=?$', [r'$\frac{1}{2}$', '2', r'$\frac{1}{30}$', r'$\frac{1}{15}$'], 1, [
    r'Each term in the denominator is twice the matching term in the numerator, so the fraction is $\frac12$.',
    r'Check: $\frac{11}{30}\div\frac{22}{30}=\frac{11}{22}=\frac12$.'])
mk('pt-q21', 18, 2, 'Roni has 60,000 shekels. He invests half of the money in a savings plan that yields a profit of 8% per year. '
    'He invests the rest of the money in a mutual fund that yields a profit ranging from 4% to 16% per year.\n'
    "Roni's profit in the coming year will be at least ____ of the total amount he invested, and at most ____ of the total amount he invested.",
   ['12% ; 24%', '8% ; 20%', '6% ; 12%', '12% ; 20%'], 3, [
    r'Half of the money at 8% earns 4% of the total.',
    r'Half of the money at 4% to 16% earns 2% to 8% of the total.',
    r'In all: at least $4+2=6$% and at most $4+8=12$%.'])
mk('pt-q22', 18, 3, 'In the accompanying figure, ABCD is a square.\n'
    'Based on this information and the information in the figure, what is the difference between the perimeter of quadrilateral ABED '
    'and the perimeter of triangle ECD (in cm)?', [r'$\frac{x}{2}$', r'$2(x-y)$', r'$\sqrt{x^2-y^2}$', r'$\sqrt{x^2+y^2}$'], 2, [
    r'DE is in both perimeters, and $AB=DC=x$, so they cancel.',
    r'What is left: $(BE+AD)-EC=(x-y)+x-y=2(x-y)$.'], fig_square())
mk('pt-q23', 19, 4, 'In a certain season, a basketball team won 30% of its first 40 games. From the 41st game on, the team won all of its games '
    'until the end of the season, and as a result, its overall winning percentage rose to 50%.\n'
    'How many games in total did the team win in this season?', ['12', '16', '20', '28'], 4, [
    r'First 40 games: 12 wins and 28 losses.',
    r'After that there are no more losses. 50% means wins = losses, so the team won 28 games in all.'])


# =====================================================================================================================
# slide helpers
# =====================================================================================================================
def R(t, size=None):
    """pop-in in the right-hand column of a figure question (the figure sits on the left)."""
    return T(t, size=size or (38 if '$' in t else 30), x=1000, y=120, w=540)


_P = P
def P(t, size=None, **k):
    """pop-in under the question; math renders smaller than text, so TeX pop-ins get a larger size."""
    return _P(t, size=size or (40 if '$' in t else 34), **k)


def G(i, qid, group, intro, slides, fig=False):
    pre = [Q(qid, figw=.5, figalign='left')] if fig else [Q(qid)]
    sb = ['Question %d' % (k + 1) for k in range(SBN[group])]
    return guided(i, qid, group, sb, intro, [(t, s, {'pre': pre}) for t, s in slides], T51)


GI, GA, GN, GE, GH = 'First Examples', 'Plugging In Answers', 'Plugging In Numbers', 'Estimation', 'Insight Questions'
SBN = {GI: 5, GA: 4, GN: 7, GE: 4, GH: 4}


# =====================================================================================================================
MODULES = [
# ------------------------------------------------------------------ lesson: intro (seg1, opening)
lesson('pt51-intro', 'Psychometric Thinking',
 ['The key lessons', 'What the exam is for', 'Special questions', 'The shortcut', 'Like a gifted test',
  'The super-methods', 'How to practice'], [
 dict(mode='title', title='Psychometric Thinking', script=[
  "Introduction to psychometric thinking.",
  "We're starting a run of the most important lessons in quantitative reasoning.",
 ]),
 dict(mode='concept', active=0, title='The key lessons', script=[
  "In these lessons we'll understand the essence of the psychometric exam — what stands behind the questions.",
  A("What stands behind the questions appears", T('What stands behind the questions?', size=46)),
  "This understanding will help you approach the questions in a more correct way — and an easier one.",
  A("Right way, easier way appears", T('Understand it → approach the questions the right way — and more easily', size=38)),
 ]),
 dict(mode='concept', active=1, title='What the exam is for', script=[
  "What's the goal of the psychometric exam?",
  A("Predict success appears", T('The goal: to predict success in academic studies', size=42)),
  "To predict success in academic studies.",
  A("A sorting exam appears", T('A sorting exam → it ranks the candidates', size=42)),
  "It's a sorting exam. It's supposed to rank the candidates.",
  "How does it do that? The questions on the exam are special questions.",
 ]),
 dict(mode='concept', active=2, title='Special questions', script=[
  "What does that mean?",
  "Usually, when we come to solve a question, we try to solve it in some way we know from school.",
  A("The school way appears", T('The school way: plug into a formula, build an equation…', size=40)),
  "Plugging into a formula, building an equation, and so on.",
  A("Often a shortcut appears", T('On the exam, in a large part of the questions: a shortcut', size=40)),
  "On the psychometric exam, in a large part of the questions, there's some shortcut.",
  "Some creative thinking that helps me get to the solution faster and more easily.",
 ]),
 dict(mode='concept', active=3, title='The shortcut', script=[
  A("Psychometric thinking = the shortcut appears", T('Psychometric thinking = creative thinking that finds the shortcut', size=40)),
  "That's psychometric thinking. That's what the exam tests.",
  A("Advantage appears", T('The exam looks for students who think this way — and gives them an advantage', size=38)),
  "It looks for the students who think this way — and gives them an advantage on the exam.",
 ]),
 dict(mode='concept', active=4, title='Like a gifted test', script=[
  "It's like the tests for gifted children. They look for the creative kids — the ones who think in a less obvious way.",
  A("Same principle appears", T('Tests for gifted children look for creative thinkers — the exam works the same way', size=38)),
  "The psychometric questions work on a similar principle.",
  A("A few methods appears", T('Most of us are not gifted — but a few methods let us solve as if we were', size=38)),
  "True, most of us aren't gifted. But luckily, there's a small number of methods that will help us solve the exam questions as if we were.",
 ]),
 dict(mode='concept', active=5, title='The super-methods', script=[
  "In this lesson we'll meet these methods for the first time, through sample questions. Later, each method gets a lesson of its own.",
  "We'll call them our super-methods.",
  A("1 appears", T('1 · Plugging in the answers', size=42)),
  A("2 appears", T('2 · Plugging in numbers', size=42)),
  A("3 appears", T('3 · Order-of-magnitude estimation', size=42)),
  A("Insights appears", T('+ Insight questions: an idea unique to one question', size=38)),
  "Three methods — and, here and there, insight questions. You'll see all of them in the examples.",
 ]),
 dict(mode='concept', active=6, title='How to practice', script=[
  "It's important to go through all of these psychometric-thinking lessons before you start studying the other topics.",
  A("These lessons first appears", T('Practice these lessons first', size=44)),
  "So that when you do your homework, you solve both the mathematical way and the psychometric way.",
  A("Both ways appears", T('Homework: solve every question both ways — the math way and the psychometric way', size=38)),
  "That's the right way to learn and to practice.",
  "Let's start with a sample question.",
 ]),
], T51),

# ------------------------------------------------------------------ intro examples (seg1)
G(0, 'pt-q01', GI,
 ["A sample question — number 17, toward the end of the section. A fairly high level of difficulty.",
  "The square root of 19,044."],
 [('No calculator', [
   "The square root of 19,044. To calculate this, I'd need a calculator — and on the exam there's no calculator.",
   "No calculator — but I do have answers.",
   "What is the square root of 19,044? Which number, times itself, gives me the number under the root?",
   "I have four answers, and I can check. I could multiply each answer by itself and see which one gives the number in the question.",
   "But that would be the calculating way. Here's where the shortcut we talked about comes in.",
  ]),
  ('The last digit', [
   A("Units digit appears", P('The number under the root ends in 4 → look at the units digit only')),
   "Take 156, for example, and multiply it by itself. Only the last digits: 6 times 6 — 36. That's it.",
   D('Write: 6 × 6 = 36 → ends in 6'),
   "My units digit is 6. It isn't 4 — it doesn't fit, and I don't need to keep calculating. Cross out choice two.",
   D('Cross out choice 2'),
   "The same way — take 194, and look only at the units digit. 4 times 4 is 16. Again a units digit of 6.",
   "It doesn't fit either. Cross out choice three.",
   D('Cross out choice 3'),
   "8 times 8 is 64 — the 4 is fine. 2 times 2 is 4 — that fits too.",
   "So with psychometric thinking — with the last digit — I eliminated two answers. Two are still left.",
  ]),
  ('Estimate the size', [
   "Now I could calculate: take one of them and multiply. If it works — fine. If not — the one that's left is correct.",
   "But here there's another shortcut. How much is 200 times 200?",
   A("200 × 200 appears", P(r'$200\cdot200=40{,}000$ — far more than 19,044')),
   "2 times 2 is 4 — so 200 times 200 is 40,000. That's much too much. 212 will be even more.",
   D('Cross out choice 4'),
   "So I can eliminate this answer too — and the one that's left, 138, is correct.",
   D('Circle choice 1'),
   "Choice one.",
   "Psychometric thinking led me to another shortcut — order-of-magnitude estimation. It helped me solve this without calculating at all.",
  ]),
  ('What we learned', [
   "So what did we learn from this question?",
   A("Answers appears", P('1 · On the exam, the answers are an essential part of the question')),
   "First: on the exam, the answers are an essential part of the question.",
   "When I showed you the question at the start, I showed it without the answers. That's a math question — I need a calculator to solve it, or some very, very long way.",
   "On the exam I have answers. And not only that — in many cases the answers also help me solve the question.",
   A("Thinking vs calculating appears", P('2 · Thinking vs calculating: often there is a shortcut')),
   "Second: thinking versus calculating. You can calculate the trivial way, what we know from school.",
   "But often there's a shortcut — some creative thinking, psychometric thinking — that gets me to the solution faster.",
   "Let's see another example.",
  ])]),

G(1, 'pt-q02', GI,
 ["A sample question — number 15, medium-plus difficulty.", "Two baskets of eggs."],
 [('Read the question', [
   "Basket A has 500 eggs. Basket B has 600 eggs.",
   "How many eggs must be moved from basket A to basket B, so that basket A will have nine-thirteenths of the eggs in basket B?",
   "Let's start by putting the data in order — we'll draw a table: basket A and basket B, before and after.",
   A("Table appears", P('Before: A = 500, B = 600 · Move x eggs → A = 500 − x, B = 600 + x')),
   "Right now, before, basket A has 500 eggs and basket B has 600.",
   "They ask how many eggs to move. I don't know — so I'll call it x.",
   "I move x eggs, so basket A is left with 500 minus x — I moved x eggs to basket B. And basket B has 600 plus the x eggs I moved.",
  ]),
  ('Build an equation', [
   "Now, what do they ask for? Basket A should have nine-thirteenths of the eggs in basket B.",
   "That's basket A after I moved eggs out of it, and basket B after it received them.",
   A("Equation appears", P(r'$500-x=\frac{9}{13}(600+x)$')),
   "Let's solve the equation. Multiply by 13: 13 times 500 minus x equals 9 times 600 plus x.",
   A("Open brackets appears", P(r'$6500-13x=5400+9x \;\Rightarrow\; 1100=22x$')),
   "Open the brackets: 6,500 minus 13x equals 5,400 plus 9x. Move the terms across: 1,100 equals 22x.",
   "Instead of dividing by 22, a middle step: divide by 11.",
   A("x = 50 appears", P(r'$100=2x \;\Rightarrow\; x=50$')),
   "100 equals 2x. Now it's clearer: x equals 50. Choice two is correct — and we solved it by building an equation.",
  ]),
  ('Plug in the answers', [
   "Now another way — psychometric thinking. One of our super-methods is plugging in the answers.",
   A("One must be right appears", P('Plugging in the answers: one of the four choices must be the answer')),
   "What does that mean? They ask how many eggs to move — and they already give me four options. One of them must be the answer. So let's check.",
   "If we move 25: 475 are left here, and here 625. Now I need to check whether that ratio equals nine-thirteenths.",
   "I could reduce — divide by 25, or by 5, and slowly get there. But that can be a fairly long calculation.",
   "But I don't have to start from the first answer. I don't have to check the answers in order.",
   A("Start convenient appears", P('A very important rule: start from the most convenient answer — usually a round one')),
   "A very, very important rule in plugging in answers: start from the answer that's most convenient for you. Usually, the rounder answers.",
  ]),
  ('Start with 50', [
   "The most convenient answer here is choice two, 50. Let's check it.",
   "500 and 600. If I move 50 from basket A to basket B, 450 are left here, and here there are 650.",
   A("Check appears", P(r'$\frac{450}{650}=\frac{45}{65}=\frac{9}{13}$ ✓')),
   "Drop the zero. 45 and 65 both divide by 5 — we get 9 and 13. Exactly the ratio they asked for in the question.",
   D('Circle choice 2'),
   "Choice two.",
   "We saw we can solve it algebraically, by building an equation — or we can plug in answers, faster, with a much easier calculation.",
   A("Round answer appears", P('In many questions, the first round answer you try is the correct one')),
   "By the way — in a large part of the questions where we plug in answers, the correct answer really is that first round answer we try.",
   "Why? Because they're giving us a shortcut. They're saying: whoever already uses this thinking — we'll give them an advantage.",
   "Again, not in every question — but in quite a few. Let's see another question.",
  ])]),

G(2, 'pt-q03', GI,
 ["A sample question — number 20, the last in the section. High difficulty.", "An algebraic expression — what does it equal?"],
 [('The algebra way', [
   "We're given an algebraic expression, and they ask what it equals. What does 'what it equals' mean?",
   "It means that one of the answers has an expression equivalent to this one. How do we find it?",
   "We take this expression and simplify it, reduce it, until we reach one of the expressions in the answers.",
   "Here's our expression, and we see a short multiplication formula — let's open it. a squared minus 2ab plus b squared.",
   A("Open appears", P(r'$\frac{a^2+b^2+a^2-2ab+b^2}{2ab}+1=\frac{2a^2+2b^2-2ab}{2ab}+1$')),
   "Collect like terms: 2a squared, 2b squared, and the minus 2ab.",
   "Many students take out a common factor of 2 here, reduce with the denominator — and honestly get a bit tangled.",
   "We'll do a small algebraic manipulation: split this fraction into three fractions.",
   A("Three fractions appears", P(r'$\frac{2a^2}{2ab}+\frac{2b^2}{2ab}-\frac{2ab}{2ab}+1=\frac{a}{b}+\frac{b}{a}$')),
   "If you put these three fractions back together, you get exactly what we had: the denominator is the same, so we just combine the numerators.",
   "Why did we do it? Because the right fraction, 2ab over 2ab, is 1. Now we have minus 1 and plus 1 — they cancel each other.",
   "Reduce the other two: a over b, and b over a. We got choice one. That was the algebraic way.",
  ]),
  ('Plug in numbers', [
   "Now the psychometric way. Our second super-method is called plugging in numbers — one of the most important methods for the exam.",
   A("Same values appears", P('Equivalent expressions → the same values give the same result')),
   "What does that mean? We have an expression with two unknowns, a and b. And the equivalent expression also has the same two unknowns.",
   "Instead of a and b, I can plug in any two values I want — as long as I don't break the condition written here.",
   "If I plug a pair of values into this expression, and the same pair into the equivalent expression — I must get the same result.",
   "Let's choose convenient numbers. For a — 1. And for b? I could take 2, 3, any number. But I can also take 1.",
   "It's the most convenient — the smallest number, the easiest to calculate with. And there's no restriction: nobody said they must be different.",
   A("a = b = 1 appears", P(r'$a=b=1$: $\frac{1+1+0^2}{2}+1=1+1=2$')),
   "1 squared is 1, plus 1, plus 0 squared — 0. Over 2. We have 2 over 2 — 1. Plus 1 — 2. So the original expression gives 2.",
  ]),
  ('Eliminate three', [
   "Now I go over the answers, and there too I plug in a and b equal to 1.",
   "If I get 2, the expression could be the equivalent one. But if I get some other number — it's certainly not, because the same values must give the same result.",
   "Choice one: 1 plus 1 — that's 2. Fine, but I have to keep checking.",
   "Choice two: a half plus a half — 1. It can't be the equivalent expression. Cross it out.",
   D('Cross out choice 2'),
   "Choice three: 1 minus 1 is 0. A 0 in the numerator makes the whole fraction 0. Cross it out too.",
   D('Cross out choice 3'),
   "Choice four: 1 plus 1, times 2 — 4. A different result again. Cross it out.",
   D('Cross out choice 4'),
   "After we eliminated three answers, we can mark choice one.",
   D('Circle choice 1'),
   A("Eliminate 3 appears", P('Plugging in numbers: you do not look for the right answer — you must eliminate 3')),
   "A very, very important point: when we work with plugging in numbers, we're not looking for the correct answer. We must eliminate three answers.",
   "We check which expression is not equivalent to the one in the question — and cross it out. Let's go on to the next question.",
  ])]),

G(3, 'pt-q04', GI,
 ["A sample question — again number 20, the last in the section. High difficulty.", "A cylinder inside a cube."],
 [('The formula way', [
   "A cylinder is inscribed in a cube with edge 3a — see the figure. Here's the cube, the cylinder is inside it, and the edge of the cube is 3a.",
   "What do they ask? The volume of the cylinder.",
   "For that we need the formula for the volume of a cylinder. Most students know it by heart — and if not, it's on the formula sheet.",
   A("Formula appears", R(r'$V=\pi r^2\cdot h$')),
   "Pi r squared, times h. Pi r squared is the area of the base of the cylinder, and h is its height.",
   "We need the radius of the base. The edge of the cube is 3a — that's given.",
   "If we slide it inward, we can see that the diameter of the base equals the edge of the cube.",
   D('Mark the diameter of the base = 3a'),
   A("r and h appears", R(r'$d=3a \Rightarrow r=\frac{3a}{2}$, $h=3a$')),
   "The diameter equals 3a — so the radius is exactly half of 3a. A diameter is 2 radii, so our radius is 3a over 2. And the height? The height is 3a.",
  ]),
  ('The bracket trap', [
   A("Volume appears", R(r'$\pi\left(\frac{3a}{2}\right)^2\cdot3a=\frac{27\pi a^3}{4}$')),
   "Plug it into the formula: squared, times h.",
   "Careful — many students write 3a over 2 here without brackets. They forget the brackets.",
   "What happens is that they square the 3a, but not the 2. Then they get 27 pi a cubed over 2 — which appears in choice one. They mark it, and they're wrong.",
   A("Brackets appears", R('A fraction for the radius → brackets → square the top and the bottom', size=28)),
   "If your radius is a fraction, put it in brackets — and square both the numerator and the denominator.",
   "Pi times 9a squared, over 2 squared — that's 4 — times 3a. 27 pi a cubed over 4. We got choice four. That was the algebraic way.",
  ]),
  ('Estimate', [
   "The psychometric way — our third super-method: order-of-magnitude estimation.",
   "If you remember, we used it in the question with the root: 200 squared was 40,000. How do we estimate in geometry?",
   A("Cube appears", R(r'Cube: $(3a)^3=27a^3$ → the cylinder is inside → a little less than $27a^3$', size=28)),
   "The volume of a cube is the edge cubed — 3a cubed is 27 a cubed. Again, something almost every student remembers. At most — the formula sheet.",
   "And the cylinder? It's inside the cube, so its volume will be a bit less. How much less? We don't know — right now we're only estimating.",
   "All the answers have a cubed, with some coefficient in front. And there's a π — it will be much easier to plug in a number.",
   A("π ≈ 3 appears", R(r'$\pi\approx3$')),
   "π is about 3.14 — but for estimating, π equals 3. That's enough.",
   "Choice one: 27 times 3, over 2 — about 40 a cubed. That's 1.5 times the cube. Could the cylinder be more than the cube? Not logical. Cross it out.",
   D('Cross out choice 1'),
   "Choice two: 27 times 3 — 81 a cubed. Three times the volume of the cube. It can't be. Cross it out.",
   D('Cross out choice 2'),
   "Choice three: 36 times 3 — 108 a cubed. Four times the cube. Also impossible.",
   D('Cross out choice 3'),
   "We eliminated three answers that make no sense, so we can mark the fourth.",
   D('Circle choice 4'),
   "Choice four.",
  ]),
  ('Why these answers?', [
   A("¾ appears", R(r'Choice 4: $\frac{81}{4}a^3\approx20a^3$ — about $\frac34$ of $27a^3$', size=28)),
   "By the way — plug in 3 there and you get 81 over 4, about 20 a cubed. That's about three-quarters of 27. That makes sense: the cylinder is about three-quarters of the cube.",
   "Notice: they didn't give us three-quarters, two-thirds, four-fifths. They gave three answers that are each more than the cube — not possible at all. Why?",
   A("Advantage appears", R('The answers are built to help whoever thinks', size=28)),
   "That's the exam's way of giving an advantage to whoever thinks.",
   "What they're saying is: if you use the trivial ways, what you learned in school — calculate. It'll take you time, maybe you'll make a mistake on the way.",
   "But if you think creatively and use one of the methods — you estimate — we'll help you. We'll give you answers that let you use that thinking. And that's what they did here.",
  ])], fig=True),

G(4, 'pt-q05', GI,
 ["A sample question — again number 20, the last in the section. High difficulty — and this one is especially hard.", "Two dice."],
 [('A table of cases', [
   "Two fair dice are rolled — a blue one and a red one. 'Fair dice' is the usual exam wording for regular dice.",
   "What's the probability that the number on the blue die will be at least as large as the number on the red die?",
   "At least as large — that means greater, or equal. A tie counts too.",
   "How do we start calculating this? The blue number I need depends on what I got on the red.",
   "If I get 1 on the red, every blue number is good for me. But if I get 6 on the red — only a 6 on the blue is good.",
   "How do I put order in all of this? We'll draw a table and list the options.",
   A("Red 1 appears", P(r'Red 1 → blue 1, 2, 3, 4, 5 or 6: $\frac16\cdot\frac66=\frac{6}{36}$')),
   "If we get 1 on the red, the blue can be 1, 2, 3, 4, 5 or 6. Every one of those is good — even 1, because equal is allowed.",
   "The probability of 1 on the red is one-sixth. The probability of one of those on the blue — six-sixths.",
   "And the probability that both happen — 1 on the red and one of those on the blue — is the product: six thirty-sixths.",
   A("Other cases appears", P(r'Red 2 → $\frac{5}{36}$ · red 3 → $\frac{4}{36}$ · … · red 6 → $\frac{1}{36}$')),
   "That's one case. We might get 2 on the red — then the blue must be 2, 3, 4, 5 or 6. One-sixth times five-sixths: five thirty-sixths.",
   "And so on: red 3 — four thirty-sixths. Red 4 — three. Red 5 — two. And the last option, 6 on the red — only a 6 on the blue. One thirty-sixth.",
  ]),
  ('Add the cases', [
   "Between these cases the link is 'or': this case happens, or this one, or this one.",
   A("Add appears", P(r'"Or" → add: $\frac{6+5+4+3+2+1}{36}=\frac{21}{36}=\frac{7}{12}$')),
   "To find the total probability we add — a link of 'or' means we add probabilities.",
   "Adding all of them gives twenty-one thirty-sixths. Reduce by 3 — seven-twelfths.",
   D('Circle choice 4'),
   "Choice four.",
   "That was the mathematical way. Long — we listed all the options. And not trivial: most students don't even get there.",
  ]),
  ('The insight', [
   "So far we've met super-methods. In this specific question there's an insight that helps us solve.",
   A("Insight appears", P('Insight = an idea unique to one question — not a method you can learn')),
   "What's an insight? Besides the questions these methods help us solve quickly and easily, here and there there's a question with some insight unique to it.",
   "Not a method we can learn — something specific to this question. In another question it'll be something completely different.",
   "So it's a bit harder to learn, except by practicing and opening your mind. But because it's on the exam — we'll learn it. Don't worry: these are rarer questions.",
   A("36 − 6 appears", P('36 outcomes − 6 doubles = 30 → split equally: 15 and 15')),
   "Two dice: 36 options in all. What's in them? Either the red is higher, or the blue is higher, or it's a tie — a double, the same number.",
   "Let's put the doubles aside. Two dice have 6 doubles: 1-1, 2-2, 3-3, 4-4, 5-5 and 6-6. Without them — 30 options are left.",
   "Those 30 must split equally between the red and the blue. The blue die isn't better or more special than the red — they're just different colors.",
   "So it's symmetric: in 15 of them the red gets the higher number, and in 15 the blue.",
   A("Ties count appears", P('Ties count too: "at least as large" includes equal → 15 + 6 = 21')),
   "Now — ties count too, because 'at least as large' includes equal. So we add the 6 doubles back: 15 plus 6 — 21.",
   A("21/36 appears", P(r'$\frac{15+6}{36}=\frac{21}{36}=\frac{7}{12}$')),
   "We found that in 21 out of 36 options the blue is at least as large as the red. The probability is twenty-one thirty-sixths — and we saw that after reducing, it's seven-twelfths.",
   "And a warning: whoever forgets the ties and just says 'symmetric, so a half' marks choice two — and is wrong.",
   "That was the insight specific to this question.",
  ])]),

# ------------------------------------------------------------------ lesson: intro wrap-up (seg1, closing)
lesson('pt51-intro-wrap', 'Thinking vs Calculating',
 ['Two ways to solve', 'Three super-methods', 'Insight questions', 'Solve both ways'], [
 dict(mode='title', title='Thinking vs Calculating', script=[
  "Let's sum up what we learned.",
 ]),
 dict(mode='concept', active=0, title='Two ways to solve', script=[
  "We saw that on the exam there are questions we can solve by calculating.",
  A("School way appears", T('The trivial way from school: calculations, math, algebra', size=40)),
  "There's the trivial way we know from school: calculations, math and algebra.",
  A("Shortcut appears", T('But the questions are special: often a shortcut — creative thinking that solves faster', size=38)),
  "But the questions are special questions. Often there's some shortcut — some creative thinking that helps us solve faster.",
 ]),
 dict(mode='concept', active=1, title='Three super-methods', script=[
  "We learned three super-methods that work in very many of the cases, and help us solve in this creative way.",
  A("Answers appears", T('Plugging in the answers — the eggs', size=42)),
  A("Numbers appears", T('Plugging in numbers — the expression with a and b', size=42)),
  A("Estimation appears", T('Order-of-magnitude estimation — the root, the cylinder', size=42)),
  "Plugging in the answers, plugging in numbers, and order-of-magnitude estimation.",
 ]),
 dict(mode='concept', active=2, title='Insight questions', script=[
  A("Insights appears", T('Insight questions: something unique to each question', size=42)),
  "And here and there, there are also insight questions — something unique to each question.",
  A("Rarer appears", T('Rarer — but they exist', size=42)),
  "They're rarer questions, but they exist too.",
  "So here we got a first look at the super-methods — and at what psychometric thinking is in general.",
 ]),
 dict(mode='concept', active=3, title='Solve both ways', script=[
  "From here there are separate lessons for each one of these methods — these techniques. It's very important to watch them,",
  A("Practice first appears", T('Watch and practice each method before you really start practicing for the exam', size=38)),
  "and to practice as much as you can before you really start practicing for the exam.",
  A("Both ways appears", T('At home: solve every question the math way AND the psychometric way', size=40)),
  "Remember: when you solve at home — solve the mathematical way, and also the psychometric way.",
  A("Options appears", T('On the exam: use whatever is more convenient, whatever comes to mind first', size=38)),
  "That will open the most options for you on the exam. You'll be able to solve both mathematically and psychometrically — whatever is more convenient, whatever jumps into your head at that moment.",
  "See you in the next lessons.",
 ]),
], T51),

# ------------------------------------------------------------------ lesson: plugging in the answers (seg2)
lesson('pt51-plug-answers', 'Plugging In the Answers',
 ['Go deeper', 'The answers help', 'Start convenient', 'Found one? Mark it', 'Three out → mark', 'Estimate first'], [
 dict(mode='title', title='Plugging In the Answers', script=[
  "Psychometric thinking — plugging in the answers.",
 ]),
 dict(mode='concept', active=0, title='Go deeper', script=[
  "In the intro lesson we got a first look at our super-methods.",
  A("Go deeper appears", T('This lesson: we go deeper into plugging in the answers', size=42)),
  "In this lesson we'll go deeper into the method of plugging in the answers. First, the rules — and then sample questions.",
 ]),
 dict(mode='concept', active=1, title='The answers help', script=[
  A("One must be right appears", T('One of the four choices must be the answer', size=44)),
  "On the exam we have answers — and the answers help us. We can use them.",
  A("Plug a choice in appears", T('Plug a choice into the question → does it satisfy all the data?', size=40)),
  "Instead of building equations, we look for an answer that, if we plug it in, satisfies the data of the question.",
 ]),
 dict(mode='concept', active=2, title='Start convenient', script=[
  A("Convenient appears", T('Start from the convenient, round answers — not in order', size=42)),
  "It's always worth starting from the convenient, round answers. You don't have to check them in order.",
  A("Usually right appears", T('In most cases, the round answer is also the correct one', size=40)),
  "In most cases, that will also be the correct answer. Not always — but in most.",
  "NITE builds the questions in a way that gives an advantage to whoever works with psychometric thinking — and not with calculation.",
 ]),
 dict(mode='concept', active=3, title='Found one? Mark it', script=[
  A("Mark it appears", T('A choice works → mark it and move on', size=44)),
  "The moment we find a correct answer, we can mark it.",
  A("No need appears", T('No need to eliminate 3 answers', size=42)),
  "We don't need to go on checking and eliminate three answers.",
 ]),
 dict(mode='concept', active=4, title='Three out → mark', script=[
  A("Three out appears", T('Eliminated 3 answers → mark the 4th without checking', size=42)),
  "And if we eliminated three answers, we don't need to check the fourth. We can mark it without checking.",
  "We know the three don't fit — so the one that's left must be correct.",
 ]),
 dict(mode='concept', active=5, title='Estimate first', script=[
  A("Estimate appears", T('Estimation: some answers are not logical → eliminate them without calculating', size=40)),
  "Order-of-magnitude estimation helps here too. There are answers where we can understand they're not logical —",
  "so we can use that, and eliminate them even without calculating.",
  "Let's start with a sample question.",
 ]),
], T51),

G(0, 'pt-q06', GA,
 ["A sample question — number 2, the beginning of the section. An easy question.", "x is an integer — and two inequalities."],
 [('Why is it here?', [
   "x is an integer. Given: x squared is less than 25, and 3x plus 6 is less than 0.",
   "Wait — number 2 is supposed to be an easy question. And we have two inequalities here, one of them a quadratic inequality, where I need to deal with the negative side and the positive side.",
   "This really isn't a question that fits number 2. It doesn't fit the beginning of the section. So why is it here?",
   "Because on the exam we also have answers — and we remember that the answers help us.",
   "Let's work with the answers, and see how easily this question is solved.",
  ]),
  ('Plug in the answers', [
   "They ask what x equals. Let's plug in the first answer: suppose x equals 1.",
   A("x = 1 appears", P(r'$x=1$: $1^2<25$ ✓ · $3\cdot1+6=9<0$ ✗')),
   "1 squared less than 25? Yes. 3 times 1 is 3, plus 6 — 9. Is that less than 0? No. So we can eliminate choice one.",
   D('Cross out choice 1'),
   "Choice two — 3. But wait: we already plugged in 1, a positive number, and here we got a positive number.",
   "Plug a positive number in here, and you can't get a negative one. So 3 also gives a positive number — it doesn't fit. We can eliminate choice two as well.",
   D('Cross out choice 2'),
   A("x = −4 appears", P(r'$x=-4$: $(-4)^2=16<25$ ✓ · $3(-4)+6=-6<0$ ✓')),
   "Let's continue — plug in choice three, minus 4. Minus 4 squared is 16. Less than 25? Yes.",
   "3 times minus 4 is minus 12. Plus 6 — minus 6. Less than 0? Yes. This answer fits.",
   "Can I mark it? In plugging in answers, the moment I find a correct answer I can mark it. I don't need to keep checking and eliminate three answers.",
   D('Circle choice 3'),
   "So yes — choice three.",
  ]),
  ('A test of thinking', [
   A("Test appears", P('A hard-looking question early in the section: stop and think — what is the best way?')),
   "By the way, it's no accident that we have a question that's mathematically hard, solved easily by plugging in answers — at the beginning of the section.",
   "NITE puts in such seemingly hard questions from time to time, to see who will try to solve them mathematically,",
   "and who stops for a moment and thinks: wait, what's the best way to solve this?",
   "Do I need to go with the methods I learned — solve the inequalities and combine them? Or can I use plugging in, or some other psychometric technique?",
   "That's what the exam does — to give an advantage to whoever stops and thinks. Let's go on to another example.",
  ])]),

G(1, 'pt-q07', GA,
 ["A sample question — number 13, a bit after the middle of the section. Medium difficulty.", "Nadav and Amit have cards."],
 [('Estimate first', [
   "Nadav and Amit have a total of 90 cards. Nadav has more cards than Amit.",
   "The difference between the numbers of cards the two of them have equals a fifth of the number of cards Nadav has. How many cards does Nadav have?",
   "Now, I could build an equation. Nadav — n, Amit — 90 minus n, and then build the equation from the data: a fifth of Nadav's cards, and so on.",
   "But why? On the exam we have answers. Let's start with an order-of-magnitude estimate.",
   A("More than half appears", P('Nadav has more than Amit → more than half of 90 → not 40, not 43')),
   "We're told that Nadav has more cards than Amit. So I can already eliminate 40 and 43 — that's less than half, and Nadav must have more than half.",
   D('Cross out choice 1'),
   D('Cross out choice 2'),
   "We eliminated two answers.",
  ]),
  ('Plug in the round one', [
   "Two answers are left. Which should I plug in? The more convenient, rounder answer — in this case, 50.",
   A("50 appears", P(r'Nadav 50 → Amit 40 → difference 10 = $\frac15\cdot50$ ✓')),
   "Let's check. Nadav has 50 cards, together they have 90 — so Amit has 40 cards. What's the difference between them? 10.",
   "Is 10 a fifth of 50? Yes. We found the correct answer.",
   D('Circle choice 4'),
   "Choice four.",
   A("Round first appears", P('Starting from convenient answers is very important — the round ones are often correct')),
   "Notice: this principle of starting from convenient answers is very, very important.",
   "Both because it helps us, and because in a large part of the exam questions, the round answers — the first ones we'd want to plug in — are where the correct answer will be.",
   "NITE builds the questions so they give an advantage to whoever works with psychometric thinking, not with calculation. Let's see another example.",
  ])]),

G(2, 'pt-q08', GA,
 ["A sample question — number 18, toward the end of the section. A relatively hard question.", "Kobi buys pants and a shirt on sale."],
 [('Round answers first', [
   "Kobi bought pants at a 50% discount and a shirt at a 10% discount, and paid 280 shekels in total instead of 500. What was the price of the shirt before the discount?",
   "If we try to solve this mathematically, we'll build two equations with two unknowns and calculate. Few students really manage to solve it that way.",
   "But we have answers — answers that help us. What we need is an answer that, if we plug it in, satisfies the data of the question.",
   "So we start plugging in — from the convenient answers. Let's start with choice one.",
   A("50 appears", P('Shirt 50, pants 450 → 225 + 45 = 270 ✗')),
   "If the shirt cost 50 shekels, the pants cost 450 — because he was supposed to pay 500. Those are the prices before the discount.",
   "On the pants he got 50% off — that's 225. On the shirt, 10% off — that's 45. Together, 270. It doesn't fit — we didn't reach 280.",
   D('Cross out choice 1'),
   "I'm a little disappointed that I plugged in a round answer and it didn't work. But there's nothing to do — we continue.",
   A("150 appears", P('Shirt 150, pants 350 → 175 + 135 = 310 ✗')),
   "The next round answer. If he was supposed to pay 150 for the shirt, he was supposed to pay 350 for the pants, to reach 500.",
   "50% off — 175. 10% off — 135. Together, 310. It doesn't fit either. We can eliminate this one too.",
   D('Cross out choice 4'),
  ]),
  ('When round fails', [
   "What's happening here? We said that usually the correct answer will be among the round, convenient answers — and here's a case where it isn't.",
   "Right: usually doesn't mean always. This question is here exactly so we learn what to do when it doesn't work out.",
   "So what do we do? We just continue as usual.",
   A("140 appears", P('Shirt 140, pants 360 → 180 + 126 = 306 ✗')),
   "We eliminated two answers, and two are left. We choose the rounder one and check it. Which is rounder? 140.",
   "If the shirt's price was 140 before the discount, the pants were 360. 50% off — 180. 10% off — 126. That won't come to 280 — we can eliminate it.",
   D('Cross out choice 3'),
   "OK — we're left with choice two. What now? Can I mark it? Yes, I can.",
   "When we plug in answers and eliminate three, we know they don't fit — the answer that's left must be correct. Eliminated three, mark the fourth without checking.",
   D('Circle choice 2'),
   "Choice two.",
  ]),
  ('A shortcut by estimate', [
   "Let's go back to where we had eliminated the two round answers. We could already have shortened the way there, with estimation.",
   A("270 vs 310 appears", P('50 → 270 · 150 → 310 · we need 280: much closer to 270')),
   "Here we got 270 when we plugged in 50, and when we plugged in 150 we got 310. We were supposed to reach 280.",
   "Look: 280 is much closer to 270 than to 310.",
   A("75 appears", P('75 is close to 50, 140 is close to 150 → the answer is 75')),
   "And of the two answers left, 75 is close to 50, and 140 is close to 150. So the answer will be 75.",
   "That's another way of estimating. Whoever saw it earlier — nice. Whoever didn't — no big deal: we plugged in another answer and eliminated it.",
   "Let's see another example.",
  ])]),

G(3, 'pt-q09', GA,
 ["A sample question — number 18, toward the end of the section. Quite a hard question.", "Ron, Miri and their stamps."],
 [('No round answer', [
   "If Ron gives Miri 4 stamps, the number of stamps she has will be 2 times the number he will have.",
   "If it's known that right now they both have the same number of stamps — how many stamps does Miri have now?",
   "We can work mathematically: build an equation, set Ron, move stamps to Miri, and so on.",
   "But let's work the way we did this whole lesson — plug in the answers. We have answers here; let's use them.",
   "When I look at these answers, there's no round or convenient answer. So I'll simply start from the first answer.",
  ]),
  ('Plug in 12', [
   "They ask how many stamps Miri has now. If she has 12 stamps now — how many does Ron have?",
   "We know that right now they both have the same number of stamps — so Ron has 12 stamps.",
   A("12 appears", P(r'Miri 12, Ron 12 → Ron gives 4 → Miri 16, Ron 8 → $16=2\cdot8$ ✓')),
   "If Ron gives Miri 4 stamps — she'll have 16, and he'll be left with only 8.",
   "Will her number be 2 times his? 16 is twice 8. That's it — that's the correct answer.",
   D('Circle choice 1'),
   "Choice one.",
   "Look — number 18, the end of the section, supposed to be a very hard question. The moment we plugged in answers, it was really, really simple. Amazing.",
  ]),
  ('What we learned', [
   A("Answers help appears", P('The answers help us · found one that works → mark it')),
   "So let's sum up. We saw that the answers help us — we can use them. And the moment we found a correct answer, we can mark it; we don't need to eliminate three.",
   A("Estimation appears", P('Estimation: answers that are not logical → out without calculating')),
   "Order-of-magnitude estimation: some answers we can understand aren't logical, and eliminate them even without calculating.",
   A("Round first appears", P('Start from the convenient, round answers · eliminated 3 → mark the 4th')),
   "It's always worth starting from the convenient, round answers — in most cases that will also be the correct answer. Not always, but in most.",
   "And if we eliminated three answers, we don't need to check the fourth — we can mark it without checking.",
   "That's our super-method of plugging in the answers. From here we go on to the next lesson — it's waiting for you there.",
  ])]),

# ------------------------------------------------------------------ lesson: plugging in numbers (seg3)
lesson('pt51-plug-numbers', 'Plugging In Numbers',
 ['The #1 technique', 'When: an expression', 'Expression ≠ equation', 'When: unknown choices', 'When: ratios',
  'Case 4: pick values', 'Pick values: watch out', 'Eliminate 3', 'Distinct results', 'Convenient numbers',
  'Nothing-changes value', 'Keep the conditions', 'It flattens the exam'], [
 dict(mode='title', title='Plugging In Numbers', script=[
  "Psychometric thinking — plugging in numbers.",
  "The most common technique of all our super-methods.",
 ]),
 dict(mode='concept', active=0, title='The #1 technique', script=[
  A("Most important appears", T('The most important technique on the psychometric exam', size=42)),
  "Plugging in numbers is the most important technique on the psychometric exam. Practice it as much as you can — it will help you a lot on the exam.",
  A("Magic appears", T('It takes hard questions and turns them into beginning-of-section questions', size=38)),
  "It works like magic: it takes hard questions and crumbles them — turns them into beginning-of-section questions.",
  A("Double advantage appears", T('A double advantage: the difficulty of the question and the solving time', size=38)),
  "That gives us a double advantage: in the difficulty of the question, and in the time it takes to solve.",
 ]),
 dict(mode='concept', active=1, title='When: an expression', script=[
  "When are we allowed to use it? There are four cases.",
  A("Case 1 appears", T('Case 1: an expression with an unknown — and numerical answers', size=40)),
  "The first case: an expression with an unknown. x can be any number, as long as it meets the conditions of the question.",
  "And if the answers are numbers, then whatever value I plug in for x, I'll always get the same answer.",
  A("Particular case appears", T('→ check a particular case: choose a number, plug it in, calculate', size=38)),
  "So we check a particular case: we choose a certain number, plug it in for x, and calculate.",
 ]),
 dict(mode='concept', active=2, title='Expression ≠ equation', script=[
  A("Expression appears", T('Expression: something = ?  → you may plug in', size=42)),
  "Just notice: an expression means I have something equals question mark.",
  A("Equation appears", T('An equation with ONE unknown → do not invent its value — plug in the answer choices instead', size=38)),
  "An equation is something equals something. If it has only one unknown — like 3x plus 5 equals 20 — then x has one specific value. I can't choose it.",
  "So there I don't invent a value for x. If the answers are numbers, I plug in the answer choices instead — that's the method from the last lesson.",
  "But careful — that's only when the equation has one unknown. When it has more letters than equations, the story changes. That's case four, in a minute.",
 ]),
 dict(mode='concept', active=3, title='When: unknown choices', script=[
  A("Case 2 appears", T('Case 2: an unknown in the answers', size=42)),
  "The second case: when there's an unknown in the answers.",
  "We don't know its value — and for each value of the unknown there's a matching value of the answer. So again, we can check a particular case.",
 ]),
 dict(mode='concept', active=4, title='When: ratios', script=[
  A("Case 3 appears", T('Case 3: ratio problems', size=42)),
  "The third case: ratio problems.",
  A("Same ratio appears", T('1 to 2 = 2 to 4 = 10 to 20 → the numbers do not matter', size=42)),
  "Why? Because in a ratio the numbers don't matter. The ratio 1 to 2, 2 to 4, 10 to 20 — it's the same ratio.",
  "And if the numbers don't matter, we can choose numbers that are convenient to work with, instead of working with unknowns.",
 ]),
 dict(mode='concept', active=5, title='Case 4: pick values', script=[
  A("Case 4 appears", T('Case 4: more letters than equations — and they ask for ONE value', size=40)),
  "The fourth case — and it's a very common one on the exam. We call it picking values that fit.",
  "The cue: you get an equation — something equals something — but it has more letters than equations. Say one equation with x and y. And they ask for one number.",
  "Think about what that means. One equation with two letters has many, many solutions. x equals this and y equals that, or x equals something else and y equals something else.",
  "But the question says the answer is one number. So the answer must come out the same for every one of those solutions. It can't depend on which solution I take.",
  "So I'm allowed to take the easiest solution there is. I give one letter a value I like, I solve the equation for the other letter, and I calculate what they ask.",
  A("Example appears", T(r'$4x+6y=18$.  $6x+9y=?$', size=46)),
  "Example. 4x plus 6y equals 18. What is 6x plus 9y?",
  A("y = 0 appears", T(r'$y=0$:  $4x=18$ → $x=4.5$', size=42)),
  "Which value do I pick? The best one is 0 — because 0 kills a whole term. Let y equal 0. Then 4x equals 18, so x is 4.5.",
  A("Answer appears", T(r'$6x+9y=6\cdot4.5+0=27$', size=42)),
  "Now what they ask: 6 times 4.5, plus 9 times 0. That's 27.",
  A("Why appears", T(r'Why: $6x+9y=1.5\,(4x+6y)=1.5\cdot18=27$', size=40)),
  "Why does it work? Because 6x plus 9y is exactly one and a half times 4x plus 6y. So it's one and a half times 18 — 27 — for every x and y. The algebra hides that; picking a value finds it without seeing it.",
  A("Order appears", T('Pick: 0 first (it kills terms) · then 1 or 2 · solve for the other letter · check the choices', size=36)),
  "So the order: try 0 first, because it kills terms. If 0 isn't allowed, or it makes a mess, try 1 or 2. Solve for the other letter. Then go to the answer choices.",
 ]),
 dict(mode='concept', active=6, title='Pick values: watch out', script=[
  A("Conditions appears", T(r'Your values must obey EVERY condition ($y\ne-2$, positive, integer…) — and the equation', size=36)),
  "Three things to watch out for. First: the values you pick must obey every condition in the question — y is not minus 2, x is positive, an integer — and of course the equation itself.",
  "That's why we pick one letter and SOLVE for the other. We don't pick both — then the equation probably won't hold.",
  A("Tie appears", T('1 often makes two choices give the same number → pick a second set of values', size=38)),
  "Second: when you go to the choices, 1 often makes two of them tie. Then pick a second set of values and check only the choices that are left.",
  A("Changes appears", T('The answer changes when your value changes → it cannot be determined', size=38)),
  "Third: if you pick two different values and the thing they ask comes out different — then it really does depend on your choice. That means the answer is 'cannot be determined from the information'.",
  A("Rule appears", T('More letters than equations, one value asked → give a letter an easy value, solve the rest', size=36)),
  "The rule to remember: more letters than equations, and they ask for one value — give one letter an easy value, solve for the rest, and check.",
 ]),
 dict(mode='concept', active=7, title='Eliminate 3', script=[
  "What are our rules?",
  A("Eliminate appears", T('We do not look for the right answer — we must eliminate 3', size=40)),
  "We must eliminate three answers. We're not looking for the correct answer — we eliminate the ones that aren't correct.",
  A("Mark the 4th appears", T('Eliminated 3 → mark the 4th without checking', size=42)),
  "If we eliminated three answers, we can mark the fourth without checking.",
  A("Plug again appears", T('Could not eliminate 3 → do another plug-in', size=42)),
  "If we didn't eliminate three answers, we need to do another plug-in — check another particular case.",
  A("Do not recheck appears", T('Answers already eliminated → do not check them again', size=40)),
  "And the answers we already eliminated — we don't need to check them again. We've already proven they're not the correct answer.",
 ]),
 dict(mode='concept', active=8, title='Distinct results', script=[
  A("Distinct appears", T('Choose values that give distinct results', size=42)),
  "When we plug in, we try to choose values that will give distinct answers.",
  A("1 appears", T('1 is convenient — but in powers, products and quotients it changes nothing', size=38)),
  "We like small numbers, often 1. But with powers, multiplication and division, 1 has no effect — and every answer may come out the same.",
  A("0 appears", T('0 is fine too — when it kills terms or makes the answer obvious. Two choices left? Plug a second number', size=36)),
  "And 0? 0 is fine when it kills terms, or when it makes the answer obvious. If it leaves two choices, just plug in a second number.",
 ]),
 dict(mode='concept', active=9, title='Convenient numbers', script=[
  A("Convenient appears", T('Choose a number that is convenient to calculate with', size=42)),
  "We try to plug in a number that's convenient for the calculation.",
  A("100 appears", T('Percent questions: plug in 100 — at the whole', size=42)),
  "In percent questions, we usually plug in 100 — and we put it at the whole, so the calculations are easy.",
  A("Change it appears", T('You chose the number → you may change it', size=42)),
  "And if along the way we see that it isn't convenient — we can change the plug-in. We chose it.",
 ]),
 dict(mode='concept', active=10, title='Nothing-changes value', script=[
  A("Nothing changes appears", T('The best value is often the one where NOTHING changes', size=42)),
  "One more trick for choosing the number. In a story with letters, look for the value where nothing happens — where the answer is obvious without any formula.",
  A("Bus appears", T('n friends rent a boat for P shekels; k more join. How much less does each pay?', size=36)),
  "Example. n friends rent a boat for P shekels and split the cost. Then k more friends join, and they split it again. By how much less does each one pay?",
  A("k = 0 appears", T('k = 0: nobody joins → each pays 0 less → every choice that is not 0 at k = 0 is out', size=36)),
  "Plug in k equals 0. Nobody joined, so nobody pays less — the answer must be 0. Now go to the choices with k equals 0: every choice that doesn't give 0 is out. No calculation at all.",
  A("Average appears", T('Averages: a new value EQUAL to the average → the average does not change', size=38)),
  "The same in averages: if the new person's grade is exactly the average, the average doesn't change. That's often the fastest value to plug in.",
  A("Second appears", T('Two choices left? Plug in a second, ordinary number (k = 1, n = 2)', size=38)),
  "The limit: the nothing-changes value often leaves two choices. Then plug in a second, ordinary number — k equals 1, n equals 2 — and check only those two.",
 ]),
 dict(mode='concept', active=11, title='Keep the conditions', script=[
  A("Conditions appears", T('Never break a condition of the question (x ≥ 4, a positive integer, …)', size=38)),
  "Whatever we plug in must not break the conditions written in the question.",
  A("Figure appears", T('In a figure: choose a value that looks logical in the drawing', size=40)),
  "And in a figure, we plug in a number that looks logical from the drawing — not something that contradicts it.",
 ]),
 dict(mode='concept', active=12, title='It flattens the exam', script=[
  A("Letters to numbers appears", T('The same question with numbers instead of letters = an easy question', size=40)),
  "Plugging in numbers lowers the difficulty of the question. If the question came with numbers instead of letters, it would be an easy one, somewhere at the beginning of the section.",
  A("Flattens appears", T('Plugging in numbers flattens the difficulty of the exam', size=42)),
  "So plugging in numbers flattens the difficulty of the exam. Let's see it in sample questions.",
 ]),
], T51),

G(0, 'pt-q10', GN,
 ["A sample question — number 17. Relatively high difficulty.", "An algebraic expression — what does it equal?"],
 [('The long way', [
   "Given: x is greater than or equal to 4. And an algebraic expression — they ask what it equals.",
   "If we tried to solve it the trivial way, the school way, we'd calculate it algebraically.",
   "We'd need to spot the short multiplication formula here, put it in brackets, take the root and calculate, until we got to the result.",
   "But that takes time. On the exam we have a shortcut. Let's see.",
  ]),
  ('Plug in x = 4', [
   "We have an expression with the unknown x. We don't know what x equals — x can be any number, as long as it meets the conditions of the question.",
   "And we have four numerical answers. That means whatever value I plug in for x, I'll always get the same answer.",
   A("Case appears", P('An expression with an unknown + numerical answers → plug in a number')),
   "If so, let's check a particular case: choose a certain number, plug it in for x, calculate the value of the expression, and see what we get.",
   "What do we plug in? x can be 4, or more. Let's plug in x equals 4 — the smallest, most convenient number.",
   A("x = 4 appears", P(r'$x=4$: $\sqrt{4+2-\sqrt{16-32+16}}=\sqrt{6-0}=\sqrt6$')),
   "4, 4, 4. 16 minus 32, plus 16 — that gives us 0. So inside the root, 0 — and we're left with root 6.",
   D('Circle choice 4'),
   "Choice four.",
   "Look — number 17, the end of the section. We solved it by plugging in a number, and it took 10 seconds.",
  ]),
  ('Expression, not equation', [
   "So what did we have here? An algebraic expression — and we decided to solve it by plugging in numbers. How did we know we could?",
   A("Case 1 appears", P('Case 1: we are given an expression with an unknown')),
   "The first case where we're allowed to: when we're given an expression with an unknown. Here we have an expression with an unknown inside.",
   A("Not an equation appears", P('Expression: something = ? → plug in · An equation with ONE unknown → plug in the answers instead')),
   "Just notice: an expression means I have something equals question mark. An equation is something equals something. If it has only one unknown, x has one specific value — I may not invent it. There I plug in the answer choices instead.",
   "And when an equation has more letters than equations? Then I may pick values again — we'll see that as case four.",
   "An expression — something equals question mark: I can plug in a number instead of the unknown, and solve much more easily. Let's see another example.",
  ])]),

G(1, 'pt-q11', GN,
 ["A sample question — number 20, the last in the section. High difficulty.", "Two triangles and an angle bisector."],
 [('The long way', [
   "In the figure, ABC is a right triangle — 90 degrees. DBC is an isosceles triangle: side DB equals side DC.",
   "We're given that AB bisects angle DBC — so these two angles are equal. They ask: what does beta equal?",
   "If we solve it the regular way, we calculate with angle sums, and run.",
   A("Run appears", R(r'At B: $90°-\alpha$ and $90°-\alpha$')),
   "Alpha, 90 — so this angle is 90 minus alpha. These angles are equal, so this one is also 90 minus alpha.",
   "Here we have base angles in an isosceles triangle — so this one equals twice 90 minus alpha.",
   "To find D we need 180 minus both of these, and then to find beta — again 180, minus this and minus that.",
   "A long calculation — and we might make a mistake along the way. But on the exam we have a shortcut. Let's see.",
  ]),
  ('Plug in α = 50°', [
   "Alpha appears in all the answers. Alpha is an unknown — we don't know its value. For every value of alpha there's a matching value of beta.",
   A("Case 2 appears", R('Case 2: an unknown in the answers → plug in')),
   "If so, like before, let's check a particular case: choose a certain alpha, plug it in, calculate beta and see what we get.",
   "That's the second case where we can plug in numbers: when there's an unknown in the answers.",
   "What do we plug in for alpha? A number that looks logical to us from the figure. We won't plug in alpha equals 120. Let's choose alpha equals 50.",
   D('Write 50° at A'),
   A("Angles appears", R(r'$\alpha=50°$: $40°$, $40°$ → $80°$, $80°$')),
   "50, 90 — 40. This one is also 40. The base angles are equal: 80 and 80.",
   A("D appears", R(r'$D=180°-160°=20°$')),
   "80 plus 80 is 160 — so D is 20.",
   A("β appears", R(r'$\beta=180°-20°-40°=120°$')),
   "And in the top triangle, beta is 180 minus 20 minus 40 — beta is 120.",
  ]),
  ('Eliminate three', [
   "We found it. Now we need to find beta in the answers — which answer gives us 120? Actually, not exactly.",
   "When we solve by plugging in numbers, we don't look for the correct answer. We need to find which answers are wrong and eliminate them — three answers.",
   "Choice one: plug in alpha equals 50 — 110. We can eliminate it.",
   D('Cross out choice 1'),
   "Choice two: plug in 50. I don't even need to calculate — half of 50 is 25, so it ends in 5. It isn't round, it doesn't end in 0. I can eliminate it.",
   D('Cross out choice 2'),
   "Choice three: plug in 50 — 4 times 50 is 200, minus 180, that's 20. That's angle D, not beta. Eliminate it.",
   D('Cross out choice 3'),
   "And do I need to check the last answer? No. If we eliminated three answers, we can mark the one that's left.",
   "Why? Because we've already shown those are wrong — and there must be one correct answer. So it's the one left.",
   D('Circle choice 4'),
   "Choice four.",
  ]),
  ('It lowers the difficulty', [
   "What did we have here? Number 20, the last question in the section — and we solved it easily, by plugging in numbers. In fact, we lowered the difficulty of the question.",
   A("Letters to numbers appears", R('The same question with 50 instead of α → an easy question')),
   "Look: if instead of the unknowns — alpha, and the unknowns in the answers — the question gave numbers: 50 instead of alpha, and in the answers the numbers we calculated before.",
   "That's a psychometric question too — it could appear on the exam. But not as number 20. It would be somewhere at the beginning of the section.",
   "So by plugging in numbers, we took number 20, a hard question, and lowered its difficulty. We flattened the difficulty level of the exam.",
   "That's what psychometric thinking does. It gives us an advantage: we lower the difficulty of the questions — and a question like this, with numbers, we also solve much faster.",
  ])], fig=True),

G(2, 'pt-q12', GN,
 ["A sample question — number 19, the end of the section. High difficulty.", "a is a positive integer — and factorials."],
 [('What is a factorial?', [
   "a is a positive integer. We're given an expression and asked to calculate what it equals.",
   "Inside the expression we have this exclamation mark. It's called a factorial, and it means the product of all the integers from the number down to 1.",
   A("Factorial appears", P(r'$5!=5\cdot4\cdot3\cdot2\cdot1$,  $4!=4\cdot3\cdot2\cdot1$,  $3!=3\cdot2\cdot1$')),
   "Let's see an example to understand. 5 factorial is 5 times 4 times 3 times 2 times 1. 4 factorial — 4 times 3 times 2 times 1. 3 factorial — 3 times 2 times 1. And so on.",
   "Back to the expression: a factorial, times a plus 2, factorial. The factorial of a certain number, a, times the factorial of the number two steps above it.",
   "Honestly, few students manage to solve this question in a mathematical, understanding way. So what do we do?",
   "We're given an expression with an unknown — we can plug in numbers.",
  ]),
  ('Plug in a = 1', [
   "a is a positive integer. Which really small positive integer do we know? 1. Let's plug in 1.",
   A("a = 1 appears", P(r'$a=1$: $1!\cdot3!=1\cdot6=6$')),
   "1 and 1 plus 2 — what do we have? 1 factorial times 3 factorial. 1 factorial is simply 1. And 3 factorial? 3 times 2 times 1 — 6. 1 times 6 — 6.",
   "Let's check the answers. Remember, we're looking for answers that give a number other than 6, so we can eliminate them — we need to eliminate three.",
   "Choice one: plug in 1 — 2 times 1 plus 2. That's 4 factorial. 4 times 3 times 2 times 1 — 24. It doesn't fit — we can eliminate it.",
   D('Cross out choice 1'),
   "Choice two: 1 squared is 1, plus 2 — 3. 3 factorial is 3 times 2 times 1 — 6. It fits; we don't eliminate it. We keep checking.",
   "Choice three: plug in 1. 1 factorial squared is 1, times 3 — 3. It doesn't fit — eliminate it.",
   D('Cross out choice 3'),
   "And if we eliminate this one too — we're done. Choice four: 1 factorial squared is 1, times 2, times 3 — that's also 6.",
  ]),
  ('Plug in again', [
   "What happened here? We checked a particular case — we plugged in a equals 1 — and we managed to eliminate only two answers.",
   "We need to eliminate three. Two answers are left that could fit, and we don't know which one is correct. So what do we do?",
   A("Plug again appears", P('Could not eliminate 3 → plug in another number')),
   "When we can't eliminate three answers, we simply do another plug-in — we check another, different particular case.",
   "Notice: the two answers we already eliminated — we don't need to check them again. We already proved they're not the correct answer.",
   A("a = 2 appears", P(r'$a=2$: $2!\cdot4!=2\cdot24=48$')),
   "Before, we plugged in 1; now let's plug in 2. 2 factorial is 2, 4 factorial is 24. 2 times 24 — 48.",
   "Choice two: plug in 2 — 2 squared is 4, plus 2 times 2 — 8. 8 factorial — how much is that? 8 times 7 times 6 times 5... wait.",
   "8 times 7 is 56 — that's already more than 48, and we haven't finished. This can't be the correct answer; I don't need to keep calculating. We can eliminate it.",
   D('Cross out choice 2'),
   "And now we can already mark choice four — the moment we eliminated three answers, we can mark the fourth.",
   D('Circle choice 4'),
  ])]),

G(3, 'pt-q13', GN,
 ["A sample question — number 20, the last in the section. High difficulty — and this one is especially hard.", "Pens, ink and words."],
 [('Can we understand it?', [
   "One pen holds x cubic centimeters of ink. To write one word you need y cubic centimeters of ink.",
   "Hagai's supply of pens was enough for him to write x cubed times y words. How many pens did Hagai have?",
   "Wow. Let's try for a moment to understand what's going on.",
   "One pen has x cubic centimeters, and one word needs y — so each pen writes x over y words. And these are the words he managed to write, so times...",
   "This isn't a simple question. Honestly, it confuses quite a few students, who get tangled up in it. But we don't need to get tangled.",
   "Look at the answers: x and y. When there are unknowns in the answers — we can plug in numbers and make the question easier.",
  ]),
  ('Plug in 1 and 1', [
   A("1 and 1 appears", P(r'$x=1,\ y=1$: 1 pen writes 1 word · $1^3\cdot1=1$ word → 1 pen')),
   "Let's plug in 1 for x and for y. One pen has 1 cubic centimeter of ink, and one word needs 1. So each pen writes exactly one word.",
   "Hagai's supply was enough for 1 cubed times 1 — that's 1. One word.",
   "One pen writes one word — so if he wrote one word, he had one pen.",
   "Now we need to check the answers — and see where we don't get 1, so we can eliminate.",
   "Choice one: 1 squared times 1 squared is 1. It fits — we continue. Choice two: 1 cubed times 1 — also 1.",
   "OK — it's happened to us before that a plug-in fit more than one answer. Let's keep checking.",
   "Choice three: 1 over 1 squared times 1 squared — also 1. And choice four — also 1.",
   "What happened? We said we plug in small numbers — we often plug in 1. In this case we plugged in 1 and couldn't eliminate a single answer. Why?",
  ]),
  ('Distinct results', [
   A("Distinct appears", P('Choose values that give distinct results — 1 changes nothing in powers, products and quotients')),
   "When we plug in, we do want small, convenient numbers — but it's important to choose plug-ins that give distinct answers.",
   "In this question, if we look at the answers, we have a power, multiplication and division here — and 1 has no effect in those cases.",
   "That's what happened to us: we got the same result in every answer — 1. So let's change the plug-in. If we didn't eliminate three answers — we do another plug-in.",
   A("2 and 1 appears", P(r'$x=2,\ y=1$: 1 pen writes 2 words · $2^3\cdot1=8$ words → 4 pens')),
   "Plug in 2: one pen has 2 cubic centimeters of ink, and one word needs 1. The supply was enough for 2 cubed times 1 — that's 8 words.",
   "So one pen writes 2 words, and he wrote 8 words in all — so he had 4 pens.",
   "Now the answers. Choice one: 2 squared times 1 squared — 4. It fits; let's keep checking. Choice two: 2 cubed times 1 — 8. It doesn't fit — eliminate it.",
   D('Cross out choice 2'),
   "In choices three and four we actually get fractions — 1 over something. So we can eliminate both of them.",
   D('Cross out choice 3'),
   D('Cross out choice 4'),
   "We're left with choice one — and we can mark it.",
   D('Circle choice 1'),
  ]),
  ('From 20 to 2', [
   "Look what we did. We took number 20, the hardest question in the section — and this one is even very hard. The moment we plugged in numbers, we made it light.",
   A("20 to 2 appears", P('2 cm³ in a pen, 1 cm³ per word: 1 pen → 2 words · 8 words → 4 pens')),
   "We took number 20 and turned it into number 2. Two cubic centimeters in a pen, one to write a word — that's easy to understand. One pen, 2 words; 8 words, 4 pens. We found it easily.",
   "Again — the beauty of psychometric thinking: it knows how to take the hardest questions and make them really, really easy. Let's see another example.",
  ])]),

G(4, 'pt-q14', GN,
 ["A sample question — number 20. High difficulty.", "Dana buys a dress on sale."],
 [('Unknown in the answers', [
   "Dana bought a dress at a discount of 40 shekels. The price of the dress after the discount was x shekels. What was the discount on the dress, in percent?",
   "Honestly, at first glance this question doesn't look so complicated. But from its position, we can assume it's probably less simple than we think.",
   "Anyway, that doesn't really interest us. We're not in this game of difficulty levels at all. We don't intend to solve the question mathematically — we work with psychometric thinking.",
   A("Unknown appears", P('An unknown in the answers → plug in numbers')),
   "When there's an unknown in the answers, we can plug in numbers. So let's start.",
  ]),
  ('Put 100 at the whole', [
   "We have the price of the dress before the discount, and after the discount. We know the price after the discount is x.",
   A("100 appears", P('Percent questions: plug in 100 — at the whole')),
   "In percent questions we usually plug in 100, so the calculations are easy. Where do we put the 100?",
   "Some students choose to put the 100 here, at x. Then the price before the discount is 140, because the discount was 40 shekels.",
   A("Inconvenient appears", P(r'At x: before 140 → $\frac{40}{140}$ — an inconvenient calculation')),
   "They ask what the discount on the dress was, in percent. So we'd need to calculate how much 40 is out of 140 — a slightly inconvenient calculation.",
   "It would be much easier if we had to calculate how much 40 is out of 100. So let's do that: put 100 at the original price — at the whole.",
   A("At the whole appears", P(r'Before: 100 → after: $x=60$ → $\frac{40}{100}=40\%$')),
   "That's the reason we put 100 at the whole — so the calculations are convenient. After the discount the price is 60.",
   "Now I need to calculate how much 40 is out of 100 — that's already simple. A 40% discount.",
   "Our next rule: we choose to plug in a convenient number. We could have calculated with 100 and 140 — but the calculation would just come out more complicated.",
  ]),
  ('Check the answers', [
   "Now check the answers — where we get 40, or rather where we don't get 40, so we can eliminate.",
   "Choice one: plug in 60. We have 100 over 100 here — reduce it, and we're left with 40. That's fine — we don't eliminate; we keep checking.",
   A("Check appears", P(r'$x=60$: (1) 40 ✓ · (2) 24 ✗ · (3) 1 ✗ · (4) 250 ✗')),
   "Choice two: plug in 60, cancel the zeros — 4 times 6 is 24. We eliminate it.",
   D('Cross out choice 2'),
   "Choice three: plug in 60 — 100 over 100, that's 1. We can eliminate it.",
   D('Cross out choice 3'),
   "Choice four: again plug in 60 — we have 100 here. 100 over 40 is 2.5, and 2.5 times 100 — 250. We can eliminate this one too.",
   D('Cross out choice 4'),
   "And mark the first answer.",
   D('Circle choice 1'),
   "Choice one. Again we see the magic of plugging in numbers. Let's solve one last question for this lesson.",
  ])]),

G(5, 'pt-q15', GN,
 ["A sample question — number 12. Medium difficulty.", "Orit and Batya share the cost of a trip."],
 [('A ratio → plug in', [
   "Orit and Batya decided to go on a trip and share the expenses. Each of them committed to pay half of the total.",
   "In the end, Orit paid only a third of the amount she had committed to, and Batya paid all the rest of the expenses.",
   "What's the ratio between the amount Batya actually paid and the amount she committed to pay?",
   "Wait — what's this question doing here? We don't have an expression with an unknown, and we don't have unknowns in the answers. But we do have a ratio.",
   A("Case 3 appears", P('Case 3: ratio problems — the numbers do not matter')),
   "And that's the third case where we can plug in numbers. Why? Because in a ratio, the numbers don't matter.",
   "The ratio 1 to 2, 2 to 4, 10 to 20 — it's the same ratio. And if the numbers don't matter, we can choose numbers that are convenient to work with, instead of working with unknowns.",
  ]),
  ('You can change it', [
   "Let's start. We'll draw a table: Orit, Batya — the amount they committed to, and the amount they actually paid.",
   "They decided to share the expenses; each was supposed to pay half. So let's plug in a small number — 1. Suppose this trip cost 1 shekel each. A cheap trip.",
   "In the end Orit paid only a third of the amount — so Orit pays a third. But a third is a fraction.",
   "That's an inconvenient number. I don't feel like working with fractions — I want convenient numbers, round numbers.",
   "Wait — who chose this 1? I did. So I can change it.",
   A("Change it appears", P('You chose the number → you may change it')),
   "If I see along the way that my calculations are leading me to inconvenient numbers, I can change the plug-in — I'm the one who plugged it in.",
   "So let's choose another number that's easy to take a third of. For example — 3.",
   A("Table appears", P('Committed: Orit 3, Batya 3 · Paid: Orit 1, Batya 5')),
   "How much is a third of 3? 1. And Batya paid all the rest: together they were supposed to pay 6. Orit paid 1, so Batya paid 5.",
  ]),
  ('The ratio', [
   "What do they ask? The ratio between the amount Batya actually paid — this — and the amount she committed to pay — this.",
   A("5 : 3 appears", P('Batya actually paid 5 and committed to 3 → the ratio is 5 to 3')),
   "5 to 3.",
   D('Circle choice 1'),
   "Choice one.",
  ]),
  ('What we learned', [
   "So let's sum up. First, we saw that plugging in numbers works like magic. It takes hard questions and crumbles them — turns them into beginning-of-section questions.",
   "That gives us a double advantage: in the difficulty of the question, and in the solving time.",
   A("When appears", P('When: an expression with an unknown · unknowns in the answers · ratio problems · more letters than equations')),
   "When are we allowed to use it? When we have an expression with an unknown, when we have an unknown in the answers, in ratio problems — and when an equation has more letters than equations and they ask for one value.",
   A("Rules appears", P('Eliminate 3 · 3 out → mark the 4th · not 3 → plug in again')),
   "What are our rules? We must eliminate three answers — we're not looking for the correct answer, we eliminate the ones that aren't correct. If we eliminated three, we mark the fourth without checking.",
   "If we didn't eliminate three, we need to do another plug-in.",
   A("Choose well appears", P('Distinct results · convenient numbers · you may change your number')),
   "When we plug in, we try to choose plug-ins that give distinct answers, and a number that's convenient to calculate with. And if along the way we see it isn't convenient — we can change the plug-in.",
   "One last thing: plugging in numbers is the most important technique on the psychometric exam. Practice it as much as you can — it will help you a lot on the exam.",
  ])]),

G(6, 'pt-q24', GN,
 ["One more question — case four: picking values that fit.", "One equation, two letters — and they ask for one value."],
 [('Read the question', [
   "Given: x is not equal to minus 5. And an equation: x y plus 5y equals 2x plus 10. They ask: what does y equal?",
   "Look at what we have. One equation — and two letters, x and y. But they ask for one number.",
   "The school way: move everything to one side, group the terms and factor. It works — but most students don't see the grouping, and get stuck.",
   "Some students say: one equation, two unknowns — it can't be solved. And they mark 'cannot be determined'. That's the trap.",
  ]),
  ('Case 4: pick x = 0', [
   A("Case 4 appears", P('More letters than equations, one value asked → pick a value for one letter, solve for the other')),
   "This is case four. More letters than equations, and they ask for one value.",
   "If y really has one value, it must be the same for every x that's allowed. So I may choose x myself — any x that obeys the conditions.",
   "Which x? 0 — because 0 kills every term that has x in it. Is 0 allowed? The only condition is x is not minus 5. So yes.",
   A("x = 0 appears", P(r'$x=0$:  $0+5y=0+10$ → $5y=10$ → $y=2$')),
   "x equals 0: x y is 0, 2x is 0. We're left with 5y equals 10. So y is 2.",
   "Notice what I did: I picked only x — and I solved for y from the equation. I didn't pick y too. If I picked both, the equation would probably not hold.",
   "Choices one and two give minus 5 and minus 2 — not 2. Cross them out.",
   D('Cross out choice 1'),
   D('Cross out choice 2'),
  ]),
  ('Check with x = 1', [
   "Two choices are left: 2, and 'cannot be determined'. How do I decide between them?",
   "If y depended on x, then a different x would give a different y. So let's pick a second value and see.",
   A("x = 1 appears", P(r'$x=1$:  $y+5y=2+10$ → $6y=12$ → $y=2$')),
   "x equals 1: y plus 5y is 6y. 2 plus 10 is 12. 6y equals 12 — y is 2 again.",
   "Same answer. y doesn't change when x changes — so it can be determined, and it's 2. Cross out choice four.",
   D('Cross out choice 4'),
   D('Circle choice 3'),
   "Choice three. Two small plug-ins — maybe 20 seconds.",
  ]),
  ('Why it works', [
   "Let's see why — so you trust it. Move everything to one side and group.",
   A("Factor appears", P(r'$xy+5y-2x-10=y(x+5)-2(x+5)=(x+5)(y-2)=0$')),
   "x y plus 5y is y times x plus 5. Minus 2x minus 10 is minus 2 times x plus 5. So we get x plus 5, times y minus 2, equals 0.",
   A("Condition appears", P(r'$x\ne-5$ → $x+5\ne0$ → $y-2=0$ → $y=2$')),
   "A product is 0 only when one of the factors is 0. x plus 5 can't be 0 — they told us x is not minus 5. So y minus 2 is 0, and y is 2, for every allowed x.",
   "And now you see why they gave the condition. If x were minus 5, the equation would become 0 equals 0, and y could be anything. A condition like 'x is not minus 5' is a hint that the answer doesn't depend on x.",
  ]),
  ('What we learned', [
   A("Rule appears", P('More letters than equations, one value asked → easy value (0 first), solve the rest, check the choices')),
   "So the rule: more letters than equations, and they ask for one value — give one letter an easy value, 0 first, solve for the rest, and check the choices.",
   A("Watch appears", P('Obey every condition · two choices left → a second value · the answer changes → cannot be determined')),
   "Watch out: your value must obey every condition. If two choices are left, pick a second value. And if the answer changes when your value changes — that's when the answer is 'cannot be determined'.",
  ])]),

# ------------------------------------------------------------------ lesson: order-of-magnitude estimation (seg4)
lesson('pt51-estimation', 'Estimation',
 ['Less known, works well', 'Eliminate, not search', 'Where is the π?', 'No negative areas', 'Numbers to know',
  'Round the numbers', 'Partial calculation', 'Negligible parts', 'Can I trust figures?'], [
 dict(mode='title', title='Order-of-Magnitude Estimation', script=[
  "Psychometric thinking — order-of-magnitude estimation.",
  "This technique is a little less known — but it works great.",
 ]),
 dict(mode='concept', active=0, title='Less known, works well', script=[
  A("Estimate appears", T('Estimate roughly how big the answer must be — instead of calculating it exactly', size=38)),
  "We don't calculate exactly — we estimate roughly how big the answer must be.",
  A("Saves time appears", T('It saves time — and it gets you out when you are stuck', size=40)),
  "There are places where we know how to calculate, and we can — but estimation can save us a lot of time.",
  "And there are questions where we get stuck: suddenly a geometry question where we didn't think of the auxiliary construction, or an expression where we don't know where to start. Estimation helps us solve those.",
 ]),
 dict(mode='concept', active=1, title='Eliminate, not search', script=[
  A("Eliminate appears", T('We do not look for the right answer — we eliminate 3', size=42)),
  "When we work with estimation, we don't look for the correct answer.",
  "We eliminate three answers — we eliminate whatever doesn't fit the value we found.",
 ]),
 dict(mode='concept', active=2, title='Where is the π?', script=[
  A("Pattern appears", T('Areas and volumes: check the pattern of the calculation — where is the π?', size=38)),
  "In geometry, when we need to find an area or a volume, the first way we can eliminate answers is by the pattern of the calculation. Where is the π?",
  A("Sector minus triangle appears", T('Sector − triangle → π − a number', size=42)),
  "For example: if we need a sector minus a triangle, the π is in the sector — so we look for the pattern π minus a number.",
  "There are questions where the π is always on the correct side, and we can't eliminate any answer.",
  "And there are questions where the π is in the right place in only one answer — so we can eliminate three answers in seconds.",
 ]),
 dict(mode='concept', active=3, title='No negative areas', script=[
  A("Negative appears", T('An area or a volume cannot be negative → eliminate negative answers', size=40)),
  "The second way: an area or a volume can't be negative. If we have a negative answer, we can eliminate it.",
  A("Hidden appears", T('The exam will not write −5 — it hides the minus with π', size=40)),
  "By the way, on the exam it won't say minus 5 — they hide it with π. But once we plug in a number, it's easy to see the answer is negative.",
 ]),
 dict(mode='concept', active=4, title='Numbers to know', script=[
  "There are a few numbers we need to know.",
  A("Numbers appears", T(r'$\pi\approx3$ · $\sqrt2\approx1.4$ · $\sqrt3\approx1.7$', size=52)),
  "π is about 3 — it's 3.14, but 3 is enough for us. Root 2 — 1.4. And root 3 — 1.7.",
  "These are the three numbers you can replace with these values, and then calculate approximately — an order-of-magnitude estimate.",
 ]),
 dict(mode='concept', active=5, title='Round the numbers', script=[
  A("Approximately appears", T(r'An approximate calculation: $\frac{14}{34}\approx\frac{14}{35}$', size=44)),
  "In an approximate calculation we don't need to be exact. If a fraction doesn't reduce nicely, we look for a close fraction that reduces better — we're calculating approximately anyway.",
  A("Far apart appears", T('The answers are far enough apart to find the correct one', size=40)),
  "The answers are far enough apart for us to find the correct one.",
 ]),
 dict(mode='concept', active=6, title='Partial calculation', script=[
  A("Partial appears", T('Partial calculation: calculate only part of it — then peek at the answers', size=40)),
  "Even when we do want to calculate, there's sometimes still a shortcut. We don't always need to calculate the whole expression — sometimes only part of it.",
  "Calculate part — and then peek at the answers.",
 ]),
 dict(mode='concept', active=7, title='Negligible parts', script=[
  A("Negligible appears", T('A tiny part is negligible: "0.64 and a little more" is enough', size=40)),
  "And sometimes part of the calculation is negligible — so small that we don't need to calculate it at all.",
  "The question is built that way on purpose — to give an advantage to whoever thinks: wait, this is negligible, I don't need to waste time on it.",
 ]),
 dict(mode='concept', active=8, title='Can I trust figures?', script=[
  A("Not to scale appears", T('Figures are not necessarily drawn to scale — but most of them are accurate', size=40)),
  "Wait — on the exam, figures don't have to be accurate. How can I estimate if the figure isn't accurate at all?",
  "In most cases we can know. One: most of the figures on the exam are accurate.",
  A("Regular shapes appears", T('Rule of thumb: regular shapes are accurate — square, circle, equilateral triangle, cube', size=38)),
  "Two, a rule of thumb: when it comes to regular shapes — a square, a circle, an equilateral triangle, a cube — the figures are accurate.",
  "Why? With a regular shape you can't draw it any other way. When I enlarge the figure, and when I shrink it, the ratios between the different parts are kept.",
  "There's a whole lesson later that explains how to know when figures are accurate and when less so. Let's start with a sample question.",
 ]),
], T51),

G(0, 'pt-q16', GE,
 ["A sample question — number 19. Relatively high difficulty.", "A sector of a circle, and a shaded region."],
 [('The plan', [
   "AOB is a sector of a circle with center O and a radius of 2 centimeters. Based on this and the figure — what's the area of the shaded region?",
   "To find the shaded area, we need to calculate the area of the sector, and subtract the area of the triangle.",
   A("Scheme appears", R('Shaded = sector − triangle')),
   "Sector minus triangle. The trivial way is to do it with the area formulas: sector area minus triangle area.",
   "Let's learn another way — with order-of-magnitude estimation.",
   "When we work with estimation, we don't look for the correct answer. We eliminate three answers — whatever doesn't fit the value we found.",
  ]),
  ('Where is the π?', [
   "In geometry, when we need an area or a volume, the first way we can eliminate answers is by the pattern of the calculation. Where is the π?",
   A("Pattern appears", R(r'Sector − triangle → $\pi$ − a number')),
   "We know our pattern: sector minus triangle. The π will be in the sector — on the left side — because it's inside the formula for the area of a sector.",
   "So we look for the pattern π minus a number — that's what should express the shaded area. Let's check the answers.",
   "Choice one: a number minus π. It doesn't fit — it's exactly the opposite. We need π minus a number. Eliminate it.",
   D('Cross out choice 1'),
   "Choice two: π minus a number — that's fine. Choice three: π divided by a number — that doesn't fit the pattern we're looking for either. Eliminate it.",
   D('Cross out choice 3'),
   "Choice four: π minus a number — it fits. We eliminated two answers just by understanding where the π is.",
   "By the way, in some questions the π is always on the correct side, and we can't eliminate any answer. And in some, it's in the right place in only one answer — then three are out in seconds.",
  ]),
  ('Negative? Out', [
   "How do we continue? Two answers are left. We know π equals 3.14 — for estimation, more or less 3.",
   A("Negative appears", R(r'(2): $\frac12\left(\frac32-2\right)<0$')),
   "Let's check what choice two is worth. Plug in 3: three-halves minus 2 — that's negative.",
   A("No negative area appears", R('An area cannot be negative → eliminate')),
   "It's a negative answer — and that's the second way we can eliminate: we can't get an area or a volume that's negative. If there's a negative answer, we can eliminate it.",
   "By the way, on the exam it won't say minus 5 — they hide it with π. But the moment we plug in a number, it's easy to see this answer is negative.",
   D('Cross out choice 2'),
   D('Circle choice 4'),
   "We're left with choice four — solved.",
   "And look — amazing: number 19, one before the last in the section, a hard question. By the π we eliminated two answers in seconds, this one is negative — choice four is correct. In seconds.",
  ]),
  ('Partial calculation', [
   "Let's see another way to solve this question, for whoever still wants to calculate. You can — but you don't have to calculate everything. Here too you can shorten it a bit.",
   "To calculate the area of the sector, we first need to understand what part of the circle it is.",
   "I always look at it like a pizza, and a slice of pizza. How many slices like this are there in the pizza?",
   A("Pizza appears", R(r'4 slices → $90°$ each · 8 slices → $45°$ each → $\frac18$ of the circle', size=28)),
   "Let's count. When we cut a pizza into 4 parts, each one has an angle of 90 degrees — a quarter. And if we cut it into 8, the angle is 45 degrees.",
   "So this sector is exactly an eighth of the circle — there are 8 pizza slices like this in the pizza.",
   A("π/2 appears", R(r'Circle: $\pi\cdot2^2=4\pi$ → sector: $\frac{4\pi}{8}=\frac{\pi}{2}$')),
   "The area of a circle is πr squared, and our radius is 2 — so the area of this circle is 4π, and the sector is an eighth of it: π over 2.",
   "Now, instead of calculating the area of the triangle, let's peek at the answers. The only place with π over 2 is choice four.",
   "In choice two we have π over 2 times a half — that's π over 4. It doesn't fit.",
   A("Partial appears", R('Partial calculation: calculate part — then peek at the answers', size=28)),
   "What we just did is a partial calculation. Even when we want to calculate, sometimes there's still a shortcut — we don't always need to calculate the whole expression. Only part of it.",
   "Let's see another example.",
  ])], fig=True),

G(1, 'pt-q17', GE,
 ["A sample question — number 20. High difficulty — and this one is especially hard.", "Root 2 over 2 plus root 2. It looks like an innocent expression."],
 [('The 5-unit trick', [
   "We have a fraction here, and they ask what it equals. And in the answers there are no fractions.",
   "So I need to simplify this fraction and get rid of the denominator. When I look at this expression, I don't really know where to start.",
   "Honestly, to know how to continue from here, there's a trick that only students of 5-unit math know how to do — and not all of them.",
   "What's the trick? We're going to multiply this fraction by 1. We multiply it by a fraction whose numerator and denominator are identical — so the fraction we multiplied by is 1. It doesn't change the value of our expression.",
   A("Times 1 appears", P(r'$\frac{\sqrt2}{2+\sqrt2}\cdot\frac{2-\sqrt2}{2-\sqrt2}$')),
   "Why did we do it? Because when we multiply the denominators, we get 2 plus root 2, times 2 minus root 2.",
   A("Formula appears", P(r'$(2+\sqrt2)(2-\sqrt2)=2^2-(\sqrt2)^2=4-2=2$')),
   "That's a short multiplication formula: a plus b, times a minus b — we can close it to a squared minus b squared.",
   "2 squared is 4, root 2 squared is 2. 4 minus 2 — 2. From here, continuing is simple.",
   A("Finish appears", P(r'$\frac{\sqrt2(2-\sqrt2)}{2}=\frac{2\sqrt2-2}{2}=\sqrt2-1$')),
  ]),
  ('Estimate: √2 ≈ 1.4', [
   "But what happens if I'm not one of those chosen few who know how to do this manipulation? How do I deal with an exercise like this?",
   "What we'll do is an approximate calculation. We don't need to be exact.",
   "Instead of root 2, we can plug in 1.4 — root 2 is about 1.4. Now we calculate the expression with numbers, and that's much simpler.",
   A("1.4 appears", P(r'$\frac{1.4}{3.4}=\frac{14}{34}\approx\frac{14}{35}=\frac25=0.4$')),
   "1.4 over 3.4. Multiply by 10 to get rid of the decimal point: 14 over 34.",
   "This fraction doesn't reduce so nicely. Let's look for another, close fraction that reduces more nicely: 14 over 35.",
   "Very, very close — and I'm allowed, because we're calculating approximately anyway. Reduce by 7: two-fifths, which is 0.4.",
   A("Answers appears", P(r'(1) $0.4^2=0.16$ · (2) $2.8$ · (3) $2.4$ · (4) $1.4-1=0.4$')),
   "Let's check the answers. Choice one: 1.4 minus 1 is 0.4. Squared — 0.16. Too small — we can eliminate it.",
   D('Cross out choice 1'),
   "Choice two: 2 times 1.4 — 2.8. Big — eliminate it.",
   D('Cross out choice 2'),
   "Choice three: 1.4 plus 1 — 2.4. Eliminate it.",
   D('Cross out choice 3'),
   "And choice four: 1.4 minus 1 — 0.4. Exactly what we got — we can mark it.",
   D('Circle choice 4'),
  ]),
  ('Numbers to know', [
   "Look at this. Number 20 — and I'm telling you, it's a hard question. Very few students know how to do that manipulation.",
   "And we solved it quickly and easily, the moment we plugged in numbers. We only put 1.4 in place of root 2.",
   "We made an order-of-magnitude estimate of this expression — we estimated roughly what it's worth. The answers are far enough apart for us to find the correct one.",
   A("Numbers appears", P(r'$\pi\approx3$ · $\sqrt2\approx1.4$ · $\sqrt3\approx1.7$')),
   "There are a few numbers we need to know. π is about 3 — 3.14, but 3 is enough for us. Root 2 — 1.4. And root 3 — 1.7.",
   "These are the three numbers you can replace with these values, and calculate approximately — an order-of-magnitude estimate. Let's see another question.",
  ])]),

G(2, 'pt-q18', GE,
 ["A sample question — number 20. High difficulty.", "A rectangle, quarter circles and a circle."],
 [('The width is the problem', [
   "In the figure, each vertex of rectangle ABCD is the center of a circle with a radius of 2 centimeters.",
   "Point O is the center of a circle tangent to the four quarter circles and to the sides AD and BC. What's the area of rectangle ABCD?",
   "To calculate the area of a rectangle, we need the length and the width. The height of the rectangle is already given here — 4 centimeters.",
   "Our problem is to find BC. We know this part is a radius — it's 2. And this one is also a radius — 2.",
   D('Mark 2 and 2 at the two ends of BC'),
   "And this segment in the middle — we don't know how to calculate it. To calculate it you need some auxiliary construction, a calculation, Pythagoras and so on.",
   "But what happens if we don't think of that auxiliary construction? How can we deal with the exercise? We solve with order-of-magnitude estimation.",
  ]),
  ('Is the figure accurate?', [
   "Wait — on the exam, the figures don't have to be accurate. How can I make an estimate if the figure isn't accurate at all? How do I know if it's accurate or not?",
   "Well, in most cases we can know. One: most of the figures on the exam are accurate.",
   A("Regular appears", R('Regular shapes → the figure is accurate: square, circle, equilateral triangle, cube', size=28)),
   "Two, a rule of thumb: when it comes to regular shapes — a square, a circle, an equilateral triangle, a cube — the figures are accurate.",
   "Why? Because with a regular shape — and here you can see we have circles; this circle is bounded by quarter circles — you can't draw it any other way.",
   "When I enlarge the figure, and when I shrink it, the ratios between the different parts are kept. So here we can make an estimate.",
   "As for accurate figures — there's a whole lesson that explains how to know when they're accurate and when less so. You'll see it later.",
  ]),
  ('Estimate the width', [
   "Let's start. We know this is 2 and this is 2, and we don't know what this segment equals.",
   A("Middle appears", R('Middle segment: more than 2, less than 4')),
   "We can see it's more than 2 — yes, we can estimate that. And we can also see it's less than 4: it's less than the diameter.",
   "If you can't see exactly what its size is, you can even use your eraser on the exam: take the eraser, mark a certain length, and check. You'll see it's more than 2 and less than the diameter.",
   A("Width appears", R('Width: between 6 and 8 → area: between 24 and 32')),
   "So the area of the rectangle is 4 times its width. If this were 2, the width would be 6; if it were 4, the width would be 8. It's neither — so the width is more than 6 and less than 8.",
   "That means the area will be between 4 times 6 and 4 times 8 — between 24 and 32. It can't equal either of them — it's somewhere in the middle.",
  ]),
  ('Check the answers', [
   A("Check appears", R(r'(1) $16\cdot1.7=27.2$ ✓')),
   "Let's look at the answers. Plug in root 3 as we learned: 1.7 times 16 — 27.2. It fits — it's in the range.",
   A("22.4 appears", R(r'(2) $16\cdot1.4=22.4$ ✗')),
   "Here plug in 1.4 — that's 22.4. It's less than 24; it doesn't fit — eliminate it.",
   D('Cross out choice 2'),
   "32 doesn't fit either. The area can't be 32 — it must be less, because this segment is less than 4. We can eliminate it.",
   D('Cross out choice 3'),
   "And 40, of course, we eliminate.",
   D('Cross out choice 4'),
   D('Circle choice 1'),
   "Look — we marked the first answer. We solved number 20, a very hard question, not easy to solve. But the moment we made an order-of-magnitude estimate — in seconds, really, really easily.",
  ])], fig=True),

G(3, 'pt-q19', GE,
 ["A sample question — number 13. Medium-plus difficulty.", "Two bottles of alcohol solution."],
 [('20% of 3.2', [
   "Bottle A has 3.2 liters of a solution with an alcohol concentration of 20%. Bottle B has 2 liters of a solution with an alcohol concentration of 3%.",
   "How many liters of alcohol are there in the two bottles together?",
   "What do we need to do? Calculate how much 20% of 3.2 is, calculate how much 3% of 2 liters is — and add.",
   A("20% appears", P('10% of 3.2 = 0.32 → 20% = 0.64')),
   "Let's start. 10% of 3.2 is 0.32 — I just divide by 10, move the decimal point one place to the left. That means 20% is 0.64.",
   D('Write 0.64'),
  ]),
  ('Negligible', [
   "Now we need to calculate how much 3% of 2 liters is. Actually — not really.",
   A("Negligible appears", P('3% of 2 liters = 0.0-something → negligible → 0.64 and a little more')),
   "What's 3% of 2 liters? It's nothing — 0.0-something. For us it's negligible. I don't need to calculate it.",
   "What I need to check in the answers is where I have 0.64 — and a bit more.",
   "0.7 — that's fine: 0.64 and a bit more. 0.95 is too big, 1.24 is big, 3.1 is big.",
   D('Cross out choices 2, 3 and 4'),
   D('Circle choice 1'),
   "We mark the first answer — 0.7. We found the correct answer fast, without getting tangled in the calculation.",
  ]),
  ('Built on purpose', [
   "It's important to note: most students manage to calculate 20% of 3.2 — it's an easy calculation.",
   "3% of 2 — some get tangled. And even if they don't get tangled and they manage, it still takes them more time. And what did we see? It isn't needed at all.",
   A("On purpose appears", P('The question is built on purpose — it rewards whoever sees what is negligible')),
   "And that's no accident. The question is built this way on purpose — to give an advantage to whoever thinks and says: wait, this is negligible, I don't need to waste time on it at all.",
   "I can look for something a bit more than 0.64, mark it, and move on to the next question.",
  ]),
  ('What we learned', [
   A("Summary appears", P('Estimation works amazingly — even on hard questions')),
   "So let's sum up our lesson. We learned a new super-method — order-of-magnitude estimation — and we saw that it works amazingly, even on hard questions.",
   "True, there are places where we know how to calculate, and we can. But it can save us a lot of time.",
   A("Stuck appears", P('Stuck? No auxiliary construction, no idea where to start → estimate, plug in numbers')),
   "Also, there are questions where we get stuck. Suddenly a geometry question where we didn't think of the auxiliary construction — or like the algebraic expression with root 2, where we didn't know where to start.",
   "Order-of-magnitude estimation and plugging in numbers help us solve those questions. From here we go on to the next lesson — it's waiting for you there.",
  ])]),

# ------------------------------------------------------------------ lesson: insight questions (seg5)
lesson('pt51-insights', 'Insight Questions',
 ['Special questions', 'What is an insight?', 'Rarer, but real', 'How to prepare'], [
 dict(mode='title', title='Insight Questions', script=[
  "Psychometric thinking — insight questions.",
 ]),
 dict(mode='concept', active=0, title='Special questions', script=[
  "By now we already understand that the questions on the psychometric exam are special questions.",
  A("Advantage appears", T('The questions give an advantage to students who think more creatively', size=40)),
  "They give an advantage to students who think in a more creative way.",
  A("Three methods appears", T('3 super-methods: plugging in answers · plugging in numbers · estimation', size=38)),
  "In the previous lessons we learned three super-methods that help us solve the questions faster and more easily — and they work in quite a large part of the exam questions.",
 ]),
 dict(mode='concept', active=1, title='What is an insight?', script=[
  "Here and there, there are also questions we call insight questions.",
  A("Insight appears", T('Insight question: the creative idea is specific to that one question', size=40)),
  "Questions where the creative thinking needed to solve them isn't something that repeats itself — it's something specific to that question.",
  A("Not twice appears", T('What works in one question will not work in another', size=42)),
  "What works in one question doesn't work in another.",
 ]),
 dict(mode='concept', active=2, title='Rarer, but real', script=[
  A("Rarer appears", T('Rarer questions — but they are on the exam', size=42)),
  "Don't worry — these are rarer questions. Most questions fall into the categories of our super-methods.",
  "But because they exist on the exam — we'll learn them.",
 ]),
 dict(mode='concept', active=3, title='How to prepare', script=[
  A("Practice appears", T('To prepare: practice as many as you can — to open your mind', size=40)),
  "The way to prepare for these questions is simply to practice them as much as you can — to open your mind.",
  "That will help you deal with them on the exam. Let's see a few sample questions like this.",
 ]),
], T51),

G(0, 'pt-q20', GH,
 ["A sample question — number 6. An easy question.", "A fraction of fractions."],
 [('Calculate', [
   "One-fifth plus one-sixth, divided by two-fifths plus two-sixths. Let's calculate.",
   "In the numerator we have fractions to add. Common denominator: 5 and 6 — a common denominator of 30. We get 6 plus 5, over 30.",
   A("Numerator appears", P(r'Numerator: $\frac{6+5}{30}=\frac{11}{30}$ · Denominator: $\frac{12+10}{30}=\frac{22}{30}$')),
   "In the denominator we again have 2 fractions — common denominator 30. We get 12 plus 10, over 30.",
   A("Divide appears", P(r'$\frac{11}{30}\div\frac{22}{30}=\frac{11}{30}\cdot\frac{30}{22}=\frac{11}{22}=\frac12$')),
   "Add: eleven-thirtieths divided by twenty-two-thirtieths. We need to divide fractions — multiply by the reciprocal, or any way that's convenient for you.",
   "Reduce the 30s, and we're left with 11 over 22 — that's a half.",
   D('Circle choice 1'),
   "Choice one.",
  ]),
  ('The insight', [
   "Now let's see the insight. Some students look at this expression and immediately see it's a half. How?",
   A("Double appears", P(r'The denominator is exactly twice the numerator: $\frac25=2\cdot\frac15$ and $\frac26=2\cdot\frac16$')),
   "What's in the denominator is exactly twice what's in the numerator. Here we have two-fifths, and here one-fifth. Here two-sixths, and here one-sixth.",
   A("Bananas appears", P('(a banana + an apple) over (2 bananas + 2 apples) = a half')),
   "Maybe it's easier to see it like this: it's as if we have a banana and 2 bananas, an apple and 2 apples. That's exactly a half.",
   "By the way — notice that NITE wrote two-sixths here, and not a third. They want us to see that it's exactly double the numerator.",
   "Honestly, I love this question. It shows that even in simple calculation questions — easy questions — NITE still gives an advantage to whoever thinks creatively. Let's see another example like this.",
  ])]),

G(1, 'pt-q21', GH,
 ["A sample question — number 19. High difficulty.", "Roni invests 60,000 shekels."],
 [('A simpler example', [
   "Roni has 60,000 shekels. He invests half of the money in a savings plan that yields a profit of 8% a year.",
   "He invests the rest of the money in a mutual fund that yields a profit ranging between 4% and 16% a year.",
   "Roni's profit in the coming year will be at least blank of the total he invested, and at most blank of the total he invested.",
   "You can solve this question in seconds, without calculating at all. But before we understand the idea behind the question, let's first take a simpler example.",
   A("100 shekels appears", P('100 shekels, a plan that yields 10%: invest all → 10% · invest half → 5%')),
   "Suppose I have 100 shekels, and I want to invest in a plan that yields a profit of 10%. If I invest all 100 shekels, I'll earn 10%.",
   "But if I invest only half, I'll earn only 5%. I invested half — I'll earn only half.",
   A("Check appears", P('50 shekels at 10% → 5 shekels = 5% of the 100')),
   "Let's check that it works. Suppose I invest 50 shekels; the plan is 10%. I earn 5 shekels.",
   "How much are those 5 shekels out of the 100? 5%. I invested half of the amount I had — and earned only half, in percent.",
  ]),
  ('Half the money, half the percent', [
   "Back to the question. He invests half of the money in a plan that yields 8% a year. So wait:",
   A("8% appears", P('Half of the money at 8% → 4% of the total')),
   "if he invested all the money, he would earn 8%. But he invested only half of the money — so he earned only 4%. Half of 8.",
   A("4–16% appears", P('Half of the money at 4%–16% → 2%–8% of the total')),
   "And here we have the rest of the money — that's also half of the money. If he invested all of it, he'd earn between 4 and 16%.",
   "But he invested only half — so he'll earn only half: between 2% and 8%.",
   A("6–12% appears", P('At least 4 + 2 = 6% · at most 4 + 8 = 12%')),
   "So how many percent at the minimum? 4 plus 2. At the maximum? 4 plus 8. Between 6% and 12%.",
   D('Circle choice 3'),
   "Choice three. We solved this question just from understanding — without calculating anything.",
  ]),
  ('If you calculate', [
   "By the way — whoever still chose to calculate, there's a shortcut here too.",
   A("Ratios appears", P('Work with ratios: 4% is half of 8% · 16% is twice 8%')),
   "Suppose you already calculated how much 8% of 30,000 is. You don't need to calculate 4% and 16% — you can work with ratios.",
   "4% is exactly half of 8. 16% is exactly twice 8.",
   A("Stop appears", P('Found the minimum (6%)? Stop — only one answer fits')),
   "And if we go on, there's another shortcut. Suppose you calculated the minimum and got 6%. Stop — check the answers.",
   "Only one answer fits; you don't need to calculate the maximum. And if you calculated the maximum first — again, only one answer fits.",
   "Remember? The answers help us. Let's see another example.",
  ])]),

G(2, 'pt-q22', GH,
 ["A sample question — number 16. Medium-plus difficulty.", "A square and a segment inside it."],
 [('The long way', [
   "In the figure, ABCD is a square. Based on this and the figure: what's the difference between the perimeter of quadrilateral ABED and the perimeter of triangle ECD?",
   "We need the difference between the perimeters of the two shapes.",
   "One option is to calculate the perimeter of the quadrilateral — by the way, it's a trapezoid. We have x, and x, and x minus y here — and then calculate this side with Pythagoras.",
   "And after that, the perimeter of the triangle. Here we have y, and x — and Pythagoras again; we calculated it before — and subtract.",
   "That's the long way. Let's solve it faster.",
  ]),
  ('Cancel what is shared', [
   A("Scheme appears", R('Difference = quadrilateral − triangle')),
   "To find the difference, we need quadrilateral minus triangle. But wait — we have shared sides. Look at DE.",
   D('Mark DE in both shapes'),
   "It's a shared side — it's in both of them. We can cancel it out, not deal with it at all.",
   A("Cancel appears", R('DE is shared → cancel · AB = DC = x → cancel')),
   "The sides AB and DC too — they're equal, both are x, both are sides of the square. We can cancel them as well.",
   A("Left appears", R(r'Left: $(x-y)+x-y$')),
   "Now we're left with x minus y and x here — minus y.",
   "And we can shorten this even more. Notice: if I draw a line here parallel to side AB, it cuts off a piece of AD that equals EC — y. These two cancel as well.",
   D('Draw a line from E parallel to AB; mark the two equal segments'),
   A("2(x − y) appears", R(r'$(x-y)+(x-y)=2(x-y)$')),
   "And what are we left with? x minus y, twice — 2 times x minus y.",
   D('Circle choice 2'),
   "Choice two. Simple. Let's see another example.",
  ])], fig=True),

G(3, 'pt-q23', GH,
 ["A sample question — number 20. High difficulty.", "A basketball season."],
 [('The first 40 games', [
   "In a certain season, a basketball team won 30% of its first 40 games.",
   "From the 41st game on, the team won all its games until the end of the season — and because of that, its overall winning percentage rose to 50%.",
   "At first it was 30%, and it rose to 50%. How many games in total did the team win in this season?",
   A("First 40 appears", P('First 40 games: 30% → 12 wins · the rest → 28 losses')),
   "Let's see. At first — the first 40 games — it won 30% of them. 10% is 4 games; 30% is 12 games.",
   "All the rest it lost — that means 28 games.",
  ]),
  ('Win until it is even', [
   "From game 41, the team only wins. No more losses — from now on, only wins. Until when?",
   A("50% appears", P('50% = wins equal losses → 28 wins')),
   "Until the number of wins equals the number of losses — because in the end it reached 50% wins. That means exactly fifty-fifty.",
   "So it wins the next game, and the game after that, and after that — it wins and wins, until the number of wins equals the number of losses.",
   "How many wins did it have in total? 28.",
   D('Circle choice 4'),
   "Choice four.",
   "Amazing — number 20, the end of the section, and it's solved in seconds, without any calculation. Only from an insight, an understanding:",
   "if it won 12 games and lost 28, it needs to reach 28 wins. That's all.",
  ]),
  ('Keep practicing', [
   A("Different appears", P('Each insight question had something different')),
   "So in this lesson we saw insights — a few examples of such questions. And in every question there was something different.",
   "On the psychometric exam there's creative thinking that helps us reach the solution faster, and the exam gives an advantage to students who think this way.",
   "We have our super-methods, which help in a large part of the cases — and here and there, there are also insight questions.",
   A("Practice appears", P('To prepare well: solve as many as you can — to open your mind')),
   "To prepare well, you need to solve as many of these as you can — to open your mind, as I said at the start. And that will help you prepare better for the exam.",
  ])]),

# ------------------------------------------------------------------ summary (before practice)
lesson('pt51-summary', 'Summary: The Super-Methods',
 ["Think, don't just calc", 'Plug in the answers', 'Plug in numbers: when', 'Plug in numbers: rules', 'Estimation',
  'Figures', 'Insights', 'Before you practice'], [
 dict(mode='title', title='Summary: The Super-Methods', script=[
  "Before you practice — let's put everything together.",
 ]),
 dict(mode='concept', active=0, title="Think, don't just calc", script=[
  A("Rewards thinking appears", T('The exam rewards thinking more than calculating', size=44)),
  "The exam gives an advantage to whoever stops and thinks before calculating.",
  A("Answers appears", T('The answers are part of the question — use them', size=42)),
  "The answers are part of the question. Use them.",
  A("Position appears", T('Too hard for its position in the section? → there is a shortcut', size=40)),
  "And when a question looks too hard for its place in the section — that's a sign there's a shortcut.",
 ]),
 dict(mode='concept', active=1, title='Plug in the answers', script=[
  A("When appears", T('When: numerical answers to a question you would solve with an equation', size=38)),
  "Plugging in the answers — when? When the answers are numbers, and the regular way would be to build an equation or solve an inequality.",
  A("How appears", T('How: start from the most convenient, round answer → does it satisfy all the data?', size=38)),
  "How? Start from the most convenient, round answer — not in order — and check it against all the data. A choice works? Mark it and move on.",
  A("Traps appears", T('Traps: round answer fails → keep going · 3 out → mark the 4th', size=38)),
  "The traps: the round answer is usually right — not always. If it fails, just keep going. And after three are out, don't check the fourth.",
 ]),
 dict(mode='concept', active=2, title='Plug in numbers: when', script=[
  A("Case 1 appears", T('1 · An expression with an unknown and numerical answers (an equation with ONE unknown → plug in the answers instead)', size=36)),
  "Plugging in numbers — when? One: an expression with an unknown — something equals question mark — and numerical answers. An equation with one unknown is different: x has one value, so don't invent it — plug in the answer choices instead.",
  A("Case 2 appears", T('2 · Unknowns in the answers', size=42)),
  "Two: unknowns in the answers.",
  A("Case 3 appears", T('3 · Ratio problems', size=42)),
  "Three: ratio problems — in a ratio the numbers don't matter.",
  A("Case 4 appears", T('4 · More letters than equations, one value asked → pick values that fit (0 first), solve the rest', size=36)),
  "Four: more letters than equations, and they ask for one value. The answer can't depend on your choice — so give one letter an easy value, 0 first, solve for the rest. Keep the conditions; if the answer changes with your choice, it cannot be determined.",
 ]),
 dict(mode='concept', active=3, title='Plug in numbers: rules', script=[
  A("Eliminate appears", T('Do not look for the right answer — eliminate 3 · 3 out → mark the 4th', size=38)),
  "The rules: we don't look for the correct answer — we eliminate three. Three out — mark the fourth.",
  A("Again appears", T('Two left → plug in again (do not recheck the eliminated ones)', size=38)),
  "Two left? Plug in another number — and don't recheck what you already eliminated.",
  A("Choose appears", T('Distinct results (1 fails with powers and products) · 100 at the whole in percents · keep the conditions', size=36)),
  "Choose numbers that give distinct results — 1 often fails with powers and products. In percents, put 100 at the whole. Keep the conditions of the question.",
  A("Nothing appears", T('0 or the nothing-changes value (k = 0, a value equal to the average) is fine — two left → a second number', size=36)),
  "0 is fine too — and so is the value where nothing changes: nobody joins, or the new value equals the average. If two choices survive, plug in a second number.",
  A("Change appears", T('You chose it → you can change it', size=42)),
  "And the trap: you're stuck with an ugly number. You aren't — you chose it, you can change it.",
 ]),
 dict(mode='concept', active=4, title='Estimation', script=[
  A("When appears", T('When: areas, volumes, roots, π — answers that are far apart', size=40)),
  "Estimation — when? Areas, volumes, roots, π — when the answers are far enough apart.",
  A("How appears", T(r'How: $\pi\approx3$, $\sqrt2\approx1.4$, $\sqrt3\approx1.7$ · where is the π? · negative area → out', size=36)),
  "How? π about 3, root 2 about 1.4, root 3 about 1.7. Check where the π should be. A negative area — out.",
  A("More appears", T('Partial calculation · negligible parts · a range: "between 15 and 20"', size=38)),
  "Calculate only part and peek at the answers. Drop what's negligible. Find a range the answer must be in.",
  A("Trap appears", T('Trap: estimation eliminates — make sure only one answer is left in the range', size=38)),
  "The trap: estimation is for eliminating. Make sure only one answer is left in your range.",
 ]),
 dict(mode='concept', active=5, title='Figures', script=[
  A("Not to scale appears", T('Figures are not necessarily drawn to scale — but most are accurate', size=40)),
  "Figures are not necessarily drawn to scale — but most of them are accurate.",
  A("Regular appears", T('Regular shapes (square, circle, equilateral triangle, cube) → accurate · measure with your eraser', size=36)),
  "With regular shapes — a square, a circle, an equilateral triangle, a cube — you can rely on the figure. Measure with your eraser.",
  A("Plug appears", T('Plugging in an angle? Choose one that looks logical in the figure', size=38)),
  "And when you plug a number into a figure, choose one that looks logical in the drawing.",
 ]),
 dict(mode='concept', active=6, title='Insights', script=[
  A("Insight appears", T('Insight questions: an idea unique to the question — rarer', size=40)),
  "Insight questions: an idea unique to the question. They're rarer.",
  A("Examples appears", T('We saw: symmetry (dice) · the denominator is double · cancel shared sides · half the money = half the percent · wins = losses', size=34)),
  "We saw symmetry in the dice, a denominator that's exactly double, shared sides that cancel, half the money earning half the percent, and wins that must equal losses.",
  A("Prepare appears", T('Prepare: practice many — to open your mind', size=42)),
  "The only way to prepare: practice many of them, to open your mind.",
 ]),
 dict(mode='concept', active=7, title='Before you practice', script=[
  "Before every question, always ask yourself:",
  A("Q1 appears", T('1 · Where is it in the section — does it look too hard for its place?', size=38)),
  A("Q2 appears", T('2 · Can I plug in the answers — starting from the round one?', size=38)),
  A("Q3 appears", T('3 · Is there a letter I can replace with a number — even in an equation with more letters?', size=36)),
  A("Q4 appears", T('4 · How big must the answer be? Which answers are impossible?', size=38)),
  A("Q5 appears", T('5 · Is part of it negligible, shared, or symmetric?', size=38)),
  "Where is it in the section? Can I plug in the answers? Is there a letter I can replace with a number? How big must the answer be? Is part of it negligible, shared or symmetric?",
  "And at home — solve every question both ways: the math way and the psychometric way. Good luck.",
 ]),
], T51),
]

PRACTICE = {51: [q for q in sorted(QUESTIONS)
                 if q not in {m['qid'] for m in MODULES if m.get('guided')}]}   # every book question is solved in a video

MEMORY = [
 dict(id='mem-pt-super-methods', after='pt51-summary', title='The four super-methods',
  intro='Psychometric thinking: before you calculate, look for the shortcut. The answers are part of the question.',
  tables=[dict(head=['Method', 'When', 'How', 'Trap'], rows=[
   ['!Plugging in the answers', 'Numerical answers; a question you would solve with an equation',
    'Start from the most convenient, round answer; check it against all the data; it works → mark it',
    'Round answer fails → just keep going; 3 out → mark the 4th without checking'],
   ['!Plugging in numbers', 'An expression with an unknown; unknowns in the answers; ratio problems (an equation with ONE unknown → plug in the answers instead)',
    'Choose small, convenient numbers (100 at the whole in percents; 0 or the nothing-changes value when it makes the answer obvious); eliminate 3 answers',
    '1 gives the same result everywhere (powers, products) → plug in again; keep the conditions'],
   ['!Plugging in numbers, case 4: picking values that fit', 'More letters than equations, and they ask for ONE value (e.g. 4x + 6y = 18, 6x + 9y = ?)',
    'Give one letter an easy value (0 first, then 1 or 2), solve the equation for the rest, check the choices (y = 0 → x = 4.5 → 27)',
    'Obey every condition (x ≠ −5, positive, integer); two choices tie → a second set; the answer changes with your choice → cannot be determined'],
   ['!Order-of-magnitude estimation', 'Areas, volumes, roots, π; answers far apart',
    'π ≈ 3, √2 ≈ 1.4, √3 ≈ 1.7; where is the π; negative area → out; partial calculation; drop negligible parts',
    'Only eliminates; figures: most are accurate, regular shapes always'],
   ['!Insight questions', 'Rarer; an idea unique to the question',
    'Look for symmetry, shared parts that cancel, a simpler version of the same question',
    'No fixed recipe — practice many to open your mind'],
  ])],
  tips=['Too hard for its position in the section? There is a shortcut.',
        'Plugging in numbers: you do not look for the right answer — you eliminate 3.',
        'You chose the number, so you can change it.',
        'More letters than equations and one value asked? The answer cannot depend on your choice: pick an easy value and solve the rest.',
        'At home, solve every question both ways: math and psychometric.']),
]
