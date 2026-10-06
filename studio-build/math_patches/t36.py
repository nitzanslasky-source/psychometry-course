"""Topic 36 - Similarity and scale. Course review 2026-09 fixes.
New: parallel-line part-to-part rule, "same height - don't square", trapezoid diagonals, altitude shortcuts,
half-height cone, percent change in area/volume, and a map-scale lesson. See t36_CHANGES.md."""
import re
from dsl import T, H, A, D, Q, P
from math_api import VIS, _word

TOPIC = 36
LEARN, PRACTICE = 'geo36-learn-1', 'geo36-core-practice'
G = ['q-r26-t36-%02d' % k for k in range(1, 19)]      # 01-05 guided, 06-18 practice
MAP = 'r26-t36-map-scale'

# ------------------------------------------------------------------------------------------------
# Figures - same style as the topic's geometry figures (ink #203344, teal #087f83, shade #d5f1ed,
# blue #e8eefb, orange #bb6821, DejaVu 20, viewBox 0 0 640 360)
# ------------------------------------------------------------------------------------------------
INK, TEAL, FILL, BLUE, ORANGE, GREY = '#203344', '#087f83', '#d5f1ed', '#e8eefb', '#bb6821', '#71818d'


def _svg(label, body, vb='0 0 640 360'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, label, label, body))


def _t(x, y, s, size=20, color=INK, italic=False):
    return ('<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="middle" fill="%s" '
            'font-family="DejaVu Sans,Arial,sans-serif" font-size="%d"%s>%s</text>'
            % (x, y, color, size, ' font-style="italic"' if italic else '', s))


def _poly(pts, fill='none', stroke=INK, w=2.5):
    return ('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>'
            % (' '.join('%.1f,%.1f' % p for p in pts), fill, stroke, w))


def _line(p, q, color=INK, w=2.5, dash=False):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (p[0], p[1], q[0], q[1], color, w, ' stroke-dasharray="7 5"' if dash else ''))


def _dot(p):
    return '<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (p[0], p[1], INK)


def _ell(cx, cy, rx, ry, fill='none', stroke=INK, w=2.5):
    return '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"/>' % (cx, cy, rx, ry, fill, stroke, w)


def _right(p, a, b, s=12):
    """right-angle marker at p between directions to a and b"""
    import math
    ua = ((a[0] - p[0]), (a[1] - p[1])); la = math.hypot(*ua); ua = (ua[0] / la * s, ua[1] / la * s)
    ub = ((b[0] - p[0]), (b[1] - p[1])); lb = math.hypot(*ub); ub = (ub[0] / lb * s, ub[1] / lb * s)
    q1 = (p[0] + ua[0], p[1] + ua[1]); q2 = (q1[0] + ub[0], q1[1] + ub[1]); q3 = (p[0] + ub[0], p[1] + ub[1])
    return _line(q1, q2, TEAL, 1.7) + _line(q2, q3, TEAL, 1.7)


def _lerp(p, q, t): return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _crop(svg, vb): return re.sub(r'viewBox="[^"]*"', 'viewBox="%s"' % vb, svg, count=1)


def _qfig(svg, vb): return {'type': 'geometry', 'svg': _crop(svg, vb)}


# --- two separate cubes (Q5: no grid, so nothing can be counted) ---
def _cube(x, y, a):
    dx, dy = 0.55 * a, -0.35 * a
    front = [(x, y), (x + a, y), (x + a, y + a), (x, y + a)]
    top = [(x, y), (x + a, y), (x + a + dx, y + dy), (x + dx, y + dy)]
    side = [(x + a, y), (x + a + dx, y + dy), (x + a + dx, y + a + dy), (x + a, y + a)]
    return _poly(top, BLUE) + _poly(side, '#f8fbfd') + _poly(front, FILL, TEAL)


FIG_Q5 = _svg('A small cube and a large cube, each with one face shaded',
              _cube(130, 230, 62) + _cube(300, 120, 165) + _t(161, 318, 'small') + _t(382, 312, 'large'))

# --- triangle with DE parallel to BC ---
TA, TB, TC = (320, 50), (130, 300), (510, 300)


def _tri_de(t, labels, extra='', label='In triangle ABC, a segment DE is parallel to BC'):
    Dp, Ep = _lerp(TA, TB, t), _lerp(TA, TC, t)
    b = _poly([TA, Dp, Ep], FILL, TEAL) + _poly([TA, TB, TC]) + _line(Dp, Ep, TEAL) + extra
    b += _t(320, 30, 'A') + _t(112, 314, 'B') + _t(528, 314, 'C') + _t(Dp[0] - 18, Dp[1], 'D') + _t(Ep[0] + 18, Ep[1], 'E')
    for (x, y, s) in labels: b += _t(x, y, s)
    return _svg(label, b)


def _side_lab(p, q, out=-1, d=18):
    """label position at the middle of pq, pushed to the outside (left side for AB: out=-1, right for AC: +1)"""
    import math
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2); vx, vy = q[0] - p[0], q[1] - p[1]; L = math.hypot(vx, vy)
    nx, ny = -vy / L, vx / L
    if (nx < 0) != (out < 0): nx, ny = -nx, -ny
    return (m[0] + nx * d, m[1] + ny * d)


def _parts_fig(t, ad, db, ae=None, ec=None, de=None, label='In triangle ABC, a segment DE is parallel to BC'):
    Dp, Ep = _lerp(TA, TB, t), _lerp(TA, TC, t)
    labs = []
    for (p, q, s, o) in [(TA, Dp, ad, -1), (Dp, TB, db, -1), (TA, Ep, ae, 1), (Ep, TC, ec, 1)]:
        if s: x, y = _side_lab(p, q, o); labs.append((x, y, s))
    if de: labs.append((320, Dp[1] - 16, de))
    return _tri_de(t, labs, label=label)


FIG_PARTS = _parts_fig(0.6, '3', '2', '6', '4', label='DE is parallel to BC: AD = 3, DB = 2, AE = 6, EC = 4')
FIG_P_PARTS = _parts_fig(0.4, '4', '6', '6', None)
FIG_P_WHOLE = _parts_fig(0.4, '2', '3', None, None, de='4')


def _ade_dbe():
    t = 1 / 3.
    Dp, Ep = _lerp(TA, TB, t), _lerp(TA, TC, t)
    b = _poly([TA, Dp, Ep], FILL, TEAL) + _poly([Dp, TB, Ep], BLUE, INK, 1.8) + _poly([TA, TB, TC]) + _line(Dp, Ep, TEAL)
    b += _t(320, 30, 'A') + _t(112, 314, 'B') + _t(528, 314, 'C') + _t(Dp[0] - 18, Dp[1], 'D') + _t(Ep[0] + 18, Ep[1], 'E')
    return _svg('In triangle ABC, DE is parallel to BC; triangles ADE and DBE are shaded', b)


FIG_P_ADE = _ade_dbe()


# --- same height: D on BC, dashed height from A ---
def _same_height(frac, foot_x, labels_on_base, areas=None, label='Triangle ABC with a point D on BC and the height from A'):
    A_, B_, C_ = (foot_x, 60), (110, 300), (530, 300)
    Dp = _lerp(B_, C_, frac); F = (foot_x, 300)
    b = _poly([A_, B_, Dp], FILL, TEAL) + _poly([A_, B_, C_]) + _line(A_, Dp, TEAL)
    b += _line(A_, F, ORANGE, 2.2, dash=True) + _right(F, A_, C_, 11)
    b += _t(A_[0], 40, 'A') + _t(92, 314, 'B') + _t(548, 314, 'C') + _t(Dp[0] + 14, 286, 'D')
    if labels_on_base:
        b += _t((110 + Dp[0]) / 2, 322, labels_on_base[0]) + _t((Dp[0] + 530) / 2, 322, labels_on_base[1])
    if areas:
        b += _t((A_[0] + 110 + Dp[0]) / 3 + 8, 235, areas[0], color=TEAL) + _t((A_[0] + Dp[0] + 530) / 3, 235, areas[1])
    return _svg(label, b)


FIG_SAMEH = _same_height(3 / 8., 175, ('3', '5'), label='Triangle ABC with D on BC: BD = 3, DC = 5, and the same height from A')
FIG_Q_SAMEH = _same_height(2 / 5., 180, None)
FIG_P_SAMEH = _same_height(2 / 5., 180, None, areas=('12', '18'))


# --- trapezoid with its diagonals ---
def _trap(a, b, unit, areas=None, base_labels=None, label='Trapezoid ABCD with its diagonals meeting at O'):
    y1, y2, cx = 110, 300, 320
    A_, B_ = (cx - a * unit / 2 - 10, y1), (cx + a * unit / 2 - 10, y1)
    D_, C_ = (cx - b * unit / 2, y2), (cx + b * unit / 2, y2)
    k = a / float(a + b); O = _lerp(A_, C_, k)
    body = _poly([A_, B_, O], FILL, TEAL, 1.8) + _poly([D_, C_, O], FILL, TEAL, 1.8)
    body += _poly([A_, B_, C_, D_]) + _line(A_, C_, INK, 2) + _line(B_, D_, INK, 2)
    body += _t(A_[0] - 14, y1 - 14, 'A') + _t(B_[0] + 14, y1 - 14, 'B') + _t(C_[0] + 16, y2 + 14, 'C') + _t(D_[0] - 16, y2 + 14, 'D')
    body += _t(O[0] + 22, O[1] + 2, 'O')
    if base_labels:
        body += _t(cx - 10, y1 - 18, base_labels[0]) + _t(cx, y2 + 22, base_labels[1])
    if areas:
        c = lambda *ps: (sum(p[0] for p in ps) / 3, sum(p[1] for p in ps) / 3)
        for (p, s) in [(c(A_, B_, O), areas[0]), (c(A_, D_, O), areas[1]), (c(B_, C_, O), areas[2]), (c(D_, C_, O), areas[3])]:
            body += _t(p[0], p[1] + 2, s, size=22, color=TEAL if s in (areas[0], areas[3]) else INK)
    return _svg(label, body)


FIG_TRAP = _trap(2, 3, 100, areas=('4', '6', '6', '9'), base_labels=('2', '3'),
                 label='Trapezoid with bases 2 and 3; its diagonals cut it into triangles of areas 4, 6, 6 and 9')
FIG_Q_TRAP = _trap(4, 6, 50, base_labels=('4', '6'))
FIG_P_TRAP = _trap(2, 5, 64)


# --- cone standing on its vertex, partly filled ---
def _glass(f, label):
    V, top, R, ry = (320, 310), 80, 120, 24
    h = V[1] - top
    wy, wr = V[1] - f * h, f * R
    b = _poly([V, (320 - wr, wy), (320 + wr, wy)], FILL, 'none', 0)
    b += _ell(320, wy, wr, wr * ry / R, FILL, TEAL, 2)
    b += _line(V, (320 - R, top)) + _line(V, (320 + R, top)) + _ell(320, top, R, ry, 'none')
    b += _line((320 - wr, wy), V, TEAL, 2) + _line((320 + wr, wy), V, TEAL, 2)
    return _svg(label, b)


FIG_HALF = _glass(0.5, 'A cone-shaped glass on its vertex, filled with water to half its height')
FIG_P_GLASS = _glass(2 / 3., 'A cone-shaped glass on its vertex, partly filled with water')


# --- right triangle with the altitude to the hypotenuse (practice: BD = 4, BC = 25) ---
def _alt_fig():
    B_, C_ = (100, 300), (540, 300)
    u = 440 / 25.
    Dp = (100 + 4 * u, 300); A_ = (Dp[0], 300 - (4 * 21) ** 0.5 * u)
    b = _poly([A_, B_, C_]) + _line(A_, Dp, TEAL) + _right(Dp, A_, C_, 10) + _right(A_, B_, C_, 12)
    b += _t(A_[0], A_[1] - 18, 'A') + _t(84, 314, 'B') + _t(556, 314, 'C') + _t(Dp[0], 322, 'D')
    b += _t((100 + Dp[0]) / 2, 322, '4')
    return _svg('A right triangle ABC with the altitude AD to the hypotenuse BC', b)


FIG_P_ALT = _alt_fig()


# ------------------------------------------------------------------------------------------------
# fixes to existing figures (edit the SVG strings, keep the style)
# ------------------------------------------------------------------------------------------------
def _move_text(svg, content, x, y):
    rx = r'<text x="[\d.]+" y="[\d.]+"( [^>]*>%s</text>)' % re.escape(content)
    new, n = re.subn(rx, lambda m: '<text x="%.3f" y="%.3f"%s' % (x, y, m.group(1)), svg)
    assert n, content
    return new


def _fix_g147(svg): return _move_text(svg, '1.4r', 372.0, 164.0)


def _fix_g150(svg): return _move_text(svg, 'Small', 367.45, 163.0)


def _fix_v631(svg):
    svg = re.sub(r'<text x="([\d.]+)" y="180.000"( [^>]*>3 units</text>)', r'<text x="\1" y="150.000"\2', svg)
    return svg


def _fix_v632(svg):
    lab = 'A small equilateral triangle with side a, and a big one with side 3a cut into nine small triangles'
    return svg.replace('role="img">', 'role="img" aria-label="%s">' % lab, 1).replace(
        '<title>Equilateral triangles, side ratio 1:3</title>', '<title>%s</title>' % lab)


def _fix_v648(svg):
    lab = '<text x="%.3f" y="%.3f" text-anchor="middle" dominant-baseline="middle" fill="#203344" font-family="DejaVu Sans,Arial,sans-serif" font-size="20">%s</text>'
    return svg.replace('</svg>', lab % (320, 316, '6') + lab % (214, 180, '8') + lab % (332, 166, '10') + '</svg>')


def _fix_v656(svg):
    # radii drawn on the top faces, labels next to them (the old labels under the bases looked like widths)
    svg = re.sub(r'<text x="240.364" y="323.455"[^>]*>2</text>', '', svg)
    svg = re.sub(r'<text x="452.727" y="323.455"[^>]*>4</text>', '', svg)
    add = (_line((213.8, 193.3), (266.9, 193.3), TEAL, 2.5) + _dot((213.8, 193.3)) + _t(240.4, 181.0, '2') +
           _line((399.6, 87.1), (505.8, 87.1), TEAL, 2.5) + _dot((399.6, 87.1)) + _t(452.7, 73.0, '4'))
    return svg.replace('</svg>', add + '</svg>')


def _v646():
    """the big triangle of v644 turned upside down (rotated 180 degrees) - same side colors and labels"""
    Dp, Ep, Fp = (579.259, 86.667), (579.259, 273.333), (330.370, 86.667)
    A_, B_, C_ = (60.741, 273.333), (185.185, 273.333), (60.741, 107.407)
    b = _poly([A_, B_, C_]) + _poly([Dp, Ep, Fp])
    b += _right(A_, B_, C_, 12.4) + _right(Dp, Ep, Fp, 12.4)
    b += _line(A_, B_, TEAL, 4) + _line(Dp, Ep, TEAL, 4) + _line(A_, C_, ORANGE, 4) + _line(Dp, Fp, ORANGE, 4)
    b += _t(44.7, 288.3, 'A') + _t(201.2, 288.3, 'B') + _t(48.7, 90.4, 'C')
    b += _t(595.3, 72.0, 'D') + _t(595.3, 288.3, 'E') + _t(314.4, 72.0, 'F')
    b += _t(123.0, 297.3, '6') + _t(40.7, 190.4, '8') + _t(138.0, 184.4, '10')
    b += _t(454.8, 66.0, '12') + _t(599.3, 180.0, '9') + _t(440.0, 196.0, '15')
    return _svg('Similar right triangles; the big one is turned upside down', b, vb='8.7 43.7 618.5 279.7')


# ------------------------------------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------------------------------------
def _replace_say(M, vid, n, old, new):
    def fn(lines):
        out, hit = [], False
        for l in lines:
            if l.get('say') == old:
                hit = True
                if new is None: continue
                l = dict(l, say=new)
            out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def _replace_draw(M, vid, n, old, new):
    def fn(lines):
        out, hit = [], False
        for l in lines:
            if l.get('draw') == old:
                hit = True
                l = dict(l, draw=new)
            out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def _script_of(M, vid, n):
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _set_vis(M, vid, n, fn):
    for it in M.slide(vid, n)['items']:
        if it.get('k') == 'vis': it['v']['svg'] = fn(it['v']['svg'])
    M.touched_videos.add(vid)


def _qfig_all(M, qid, fn):
    """apply fn to the question figure and to every copy of it on slides"""
    q = M.q(qid)
    M.set_q(qid, figure=fn(q['questionVisual']['svg']))
    for vid, v in M.D['videos'].items():
        for b in v.get('beats', []):
            for it in b.get('items', []):
                if it.get('k') == 'q' and it.get('qid') == qid and isinstance(it.get('fig'), dict):
                    it['fig']['svg'] = fn(it['fig']['svg']); M.touched_videos.add(vid)


def _active_by_title(M, vid, sidebar):
    for b in M.video(vid)['beats']:
        if b['mode'] != 'title' and b['title'] in sidebar: b['active'] = sidebar.index(b['title'])


# ================================================================================================
def apply(M):
    _figures(M)
    _lesson_similarity(M)
    _lesson_triangles(M)
    _lesson_solids(M)
    _solution_videos(M)
    _existing_questions(M)
    _new_guided(M)
    _map_block(M)
    _new_practice(M)
    _cards(M)
    _practice(M)
    _wording(M)
    _sync_stem_copies(M)
    summary(M)
    for k, t in enumerate(['Same height: area ratio without squaring', 'A trapezoid and its diagonals: four triangles',
                           'A cube grows by 20%: the volume in percent', 'Map scale: a real distance',
                           'Map scale: a real area']):
        v = M.video('solve-' + G[k]); v['title'] = v['navLabel'] = t


# ------------------------------------------------------------------------------------------------
# 4. figures
# ------------------------------------------------------------------------------------------------
def _figures(M):
    _qfig_all(M, 'geo36-g147', _fix_g147)
    _qfig_all(M, 'geo36-g150', _fix_g150)
    # Q5: two separate cubes instead of a 4 x 4 x 4 block that can be counted
    M.set_q('geo36-g142', figure=FIG_Q5)
    for n in (2, 3):
        for it in M.slide('solve-geo36-g142', n)['items']:
            if it.get('k') == 'q': it['fig'] = _qfig(FIG_Q5, '110 20 470 320')
    _set_vis(M, 'geo-134', 12, _fix_v631)
    _set_vis(M, 'geo-135', 3, _fix_v632)
    _set_vis(M, 'geo-139', 8, _fix_v648)
    _set_vis(M, 'geo-141', 5, _fix_v656)
    M.slide('geo-139', 5)['items'][0]['v']['svg'] = _v646()


# ------------------------------------------------------------------------------------------------
# 1-2. lesson videos
# ------------------------------------------------------------------------------------------------
def _lesson_similarity(M):
    # geo-135 slide 2: regular shapes are always similar - other shapes are NOT automatically similar
    M.set_slide('geo-135', 2, script=_script_of(M, 'geo-135', 2) + [
        "But careful: other shapes are NOT automatically similar.",
        A("'Not always similar' appears",
          T('NOT always similar: rectangles $\\cdot$ rhombuses $\\cdot$ isosceles triangles $\\cdot$ right triangles', size=36)),
        "Two rectangles can be long and thin, or almost square. Two right triangles can have different acute angles.",
        "For these shapes, check the angles — or check that every length changes by the same factor.",
    ])


def _lesson_triangles(M):
    V = 'geo-139'
    # --- recap (slide 12) ---
    M.set_slide(V, 12, script=[
        A('Two equal angles → similar appears', T('Two equal angles $\\rightarrow$ similar triangles', size=38, y=250)),
        "Two equal angles — similar.",
        A('Match sides opposite equal angles — small–big table appears',
          T('Match sides opposite equal angles — make a small–big table', size=36, y=330)),
        "Match by the angles — and make the table.",
        A('Parallel to the base · altitude to hypotenuse · hourglass appears',
          T('On the exam: parallel to the base $\\cdot$ altitude to the hypotenuse $\\cdot$ hourglass', size=34, y=410)),
        "The three exam pictures.",
        A('Parallel line: part to part, the segment to the whole side appears',
          T('Parallel line: part to part ✓ $\\cdot$ the segment itself $\\leftrightarrow$ the WHOLE side', size=34, y=490)),
        "With a parallel line: part to part is fine. The parallel segment itself — always against the whole side.",
        A('Same height, not similar → area ratio = base ratio appears',
          T('Same height, not similar $\\rightarrow$ area ratio $=$ base ratio (no squaring)', size=34, y=570)),
        "Same height but not similar — the areas follow the bases. No squaring.",
        A('Rectangles: both dimensions, one factor appears', T('Rectangles: both dimensions use one factor', size=34, y=650)),
        A('Also similar: 3 proportional sides, or 2 + the angle between appears',
          T('Also similar: 3 proportional side pairs — or 2 pairs and the angle between them', size=30, y=730)),
        "Rectangles: both dimensions, one factor.",
        "Two more ways to prove similarity — you will rarely need them on the exam: all three sides in the same ratio, or two sides in the same ratio and the angle between them equal.",
    ])
    # --- rectangle on the diagonal (slide 11): a worked example with numbers ---
    fig = M.slide(V, 11)['items'][0]
    M.set_slide(V, 11, script=[
        "On the exam, rectangle-similarity questions usually look like this —",
        A('A small rectangle on the diagonal of a big rectangle appears', dict(fig)),
        "A rectangle, a diagonal through it — and on the diagonal, the corner of another rectangle.",
        "Then the two rectangles are similar. We won't prove it here — let's use it.",
        D('Write 12 on AB, 8 on AD and 9 on AP'),
        "Example: the big rectangle is 12 by 8. The small one has length AP equal to 9. What is its width AR?",
        A("'AR = 6' appears", T('$\\frac{AR}{AP}=\\frac{AD}{AB}$: $\\frac{AR}{9}=\\frac{8}{12}\\Rightarrow AR=6$', size=38, x=410, y=640)),
        "Width to length is the same in both: 8 over 12 — two thirds. Two thirds of 9 — 6.",
        D('Write 6 on AR, 2 on RD and 3 on PB'),
        "Now the leftover pieces: the top part RD is 8 minus 6 — 2. The right part PB is 12 minus 9 — 3.",
        A("'Leftovers: 2/6 = 3/9' appears", T('Leftovers: $\\frac{RD}{AR}=\\frac26=\\frac13$ and $\\frac{PB}{AP}=\\frac39=\\frac13$', size=38, x=410, y=730)),
        "Top part to bottom part: 2 to 6. Right part to left part: 3 to 9. Both one third — the same ratio.",
        "So when you see a rectangle inside a rectangle with its corner on the big one's diagonal — they're similar.",
    ])
    # --- altitude to the hypotenuse (slide 8): numbers on the figure + the two shortcuts ---
    M.set_slide(V, 8, script=_script_of(M, V, 8) + [
        "Two shortcuts come from this picture. Remember them — they save a lot of time.",
        A("'h² = p · q · leg² = its part · hypotenuse' appears",
          T('Shortcuts: $h^2=p\\cdot q$ $\\cdot$ $\\text{leg}^2=\\text{its part}\\cdot\\text{hypotenuse}$', size=36, x=410, y=740)),
        "The altitude squared equals the two parts of the hypotenuse multiplied: 4.8 squared is 23.04, and 3.6 times 6.4 is also 23.04.",
        "And a leg squared equals its own part times the whole hypotenuse: AB is 6 — 36. And 3.6 times 10 — 36.",
    ])
    # --- turn it around (slide 5): the figure now really shows a turned triangle ---
    M.set_slide(V, 5, script=_script_of(M, V, 5) + [
        D('Mark α at C and at F, β at B and at E'),
        "Here I turned the big triangle upside down. 9 is still opposite α, and 12 is still opposite β.",
    ])
    # --- parallel to the base (slide 7): lead-in to the part-to-part rule ---
    M.edit_lines(V, 7, lambda ls: ls + [{'say': "And what about the parts AD and DB? There IS a rule for parts. Next slide."}])

    # --- new slides after the hourglass (slide 9): same height, trapezoid diagonals ---
    M.insert_slides(V, 9, [
        dict(mode='concept', title='Same height', script=[
            "Now the most common WRONG use of similarity.",
            A('Triangle ABC with D on BC and the height from A appears', VIS(FIG_SAMEH, w=1000, h=520)),
            "D is on BC. BD is 3, DC is 5. What is the ratio of the areas of triangles ABD and ADC?",
            "The reflex: 3 to 5 — square it, 9 to 25. Stop! Are these triangles similar?",
            "No. Their angles are different. So there is nothing to square.",
            D('Trace the dashed height from A'),
            "But they share the same height — the distance from A down to BC.",
            "Area is base times height over 2. Same height — so the areas are in the ratio of the bases: 3 to 5.",
            A("'Same height → area ratio = base ratio' appears",
              T('Same height $\\rightarrow$ area ratio $=$ base ratio: $3:5$, NOT $9:25$', size=38, x=410, y=650)),
            "Square only when the shapes are similar — when EVERY length grows by the same factor. Here only the base changed.",
        ]),
        dict(mode='concept', title='Trapezoid diagonals', script=[
            "A favorite on the exam: a trapezoid with its two diagonals.",
            A('A trapezoid with bases 2 and 3 and its diagonals appears', VIS(FIG_TRAP, w=1000, h=520)),
            "The diagonals cut it into four triangles. The top and the bottom ones — that's an hourglass.",
            "Bases 2 and 3. The hourglass triangles are similar, ratio 2 to 3 — areas 4 to 9.",
            D('Point to the left triangle and the top triangle'),
            "The side triangles? The left one and the top one have the same height — from A down to the diagonal BD.",
            "Their bases on that diagonal are 3 parts and 2 parts. Same height — no squaring: the side triangle is 6.",
            "The right one — also 6. The two side triangles are always equal.",
            A("'Bases a and b: a², ab, ab, b²' appears",
              T('Bases $a$ and $b$: areas $a^2,\\ ab,\\ ab,\\ b^2$', size=40, x=410, y=650)),
            "In general: a squared, a times b, a times b, b squared.",
            A("'2 and 3: 4, 6, 6, 9 — trapezoid = 25' appears",
              T('Bases $2$ and $3$: $4+6+6+9=25$ units', size=38, x=410, y=730)),
            "Here: 4, 6, 6, 9. The whole trapezoid — 25 units.",
        ]),
    ])
    # --- new slide after slide 7: part to part ---
    M.insert_slides(V, 7, [dict(mode='concept', title='Part to part', script=[
        "One more rule with a line parallel to the base. Look only at the two sides AB and AC.",
        A('Triangle ABC with DE parallel to BC and the four parts appears', VIS(FIG_PARTS, w=1000, h=520)),
        "The parallel line cuts both sides in the same ratio. AD to DB equals AE to EC. Part to part.",
        A("'AD/DB = AE/EC ✓' appears", T('Part to part: $\\frac{AD}{DB}=\\frac{AE}{EC}$: $\\frac32=\\frac64$ ✓', size=40, x=410, y=650)),
        "Here AD is 3 and DB is 2. AE is 6 — so EC is 4. 3 to 2 on both sides.",
        "So why did I say that AE doesn't match EC? Because DE is different.",
        A("'DE/BC = AD/AB — the WHOLE side' appears",
          T('But $\\frac{DE}{BC}=\\frac{AD}{AB}=\\frac35$ — the WHOLE side', size=40, x=410, y=740)),
        "DE is not a part of a side. It matches the WHOLE BC. So DE to BC is 3 to 5 — AD to the whole AB. Not 3 to 2.",
        "The rule: parts of the two sides — part to part is fine. The parallel segment itself — always against the whole side.",
    ])])
    sb = ['Two angles are enough', 'Opposite equal angles', 'Small–big table', 'Turn it around', 'Ratios inside',
          'Parallel to the base', 'Part to part', 'Altitude to hypotenuse', 'Hourglass', 'Same height',
          'Trapezoid diagonals', 'Rectangles', 'Rectangle on diagonal', 'Recap']
    M.set_sidebar(V, sb)
    _active_by_title(M, V, sb)


def _lesson_solids(M):
    # geo-141 slide 3: spheres
    M.set_slide('geo-141', 3, script=_script_of(M, 'geo-141', 3) + [
        A("'Spheres: always similar' appears", T('Spheres: ALWAYS similar — like circles', size=40, y=480)),
        "And spheres? Like circles — every sphere is the same shape. All spheres are similar.",
    ])
    _replace_draw(M, 'geo-141', 5, 'Write 2 : 4 by the radii and 4 : 8 by the heights',
                  'Write the ratio 2 : 4 by the radii and the ratio 4 : 8 by the heights')
    # geo-141 new slide 6: the half-height cone
    M.insert_slides('geo-141', 5, [dict(mode='concept', active=4, title='Half-height cone', script=[
        "One more trap — a famous one.",
        A('A cone-shaped glass filled to half its height appears', VIS(FIG_HALF, w=1000, h=520)),
        "A cone-shaped glass, standing on its point. I fill it with water up to HALF of its height.",
        "Is the glass half full? It looks like it. But no!",
        "The water is a small cone — similar to the glass. Its height is half, and its radius is half too.",
        A("'Half the height → (1/2)³ = 1/8' appears",
          T('Water to half the height $\\rightarrow$ $\\left(\\frac12\\right)^3=\\frac18$ of the glass', size=42, x=410, y=650)),
        "Volume: one half cubed — one eighth. Only one eighth of the glass is full.",
        "The wide part at the top holds almost all the water.",
    ])])
    M.set_sidebar('geo-141', ['Volume: cubed', 'Similar solids', 'Cubes: count them', 'Cylinders: check both', 'Half-height cone'])

    # geo-143: wording, percent-change slide, recap
    M.insert_slides('geo-143', 7, [dict(mode='concept', active=6, title='Percent change', script=[
        "Percent questions with similar shapes. Every side grows by 10 percent.",
        "First, turn the percent into a factor: plus 10 percent is times 1.1.",
        A("'Sides +10% → × 1.1' appears", T('Sides $+10\\%$ $\\rightarrow$ $\\times1.1$', size=44)),
        "Area — square the factor. 1.1 squared is 1.21. Back to percent: plus 21 percent — not 20.",
        A("'Area × 1.21 → +21%' appears", T('Area: $\\times1.1^2=\\times1.21$ $\\rightarrow$ $+21\\%$', size=44)),
        "Volume — cube it. 1.1 cubed is 1.331. Plus 33.1 percent — not 30.",
        A("'Volume × 1.331 → +33.1%' appears", T('Volume: $\\times1.1^3=\\times1.331$ $\\rightarrow$ $+33.1\\%$', size=44)),
        "And backwards: the area grew by 44 percent — times 1.44. The square root is 1.2 — the sides grew by 20 percent.",
        A("'Percent → factor → power → back to percent' appears",
          T('Percent $\\rightarrow$ factor $\\rightarrow$ power $\\rightarrow$ back to percent', size=40)),
        "Always the same four steps.",
    ])])
    M.set_slide('geo-143', 9, active=7, script=_script_of(M, 'geo-143', 9) + [
        A("'Percent: factor first, then the power' appears", T('Percent: turn it into a factor first, then the power', size=40, y=490)),
        "And with percents: a factor first, then the power, then back to percent.",
    ])
    M.set_sidebar('geo-143', ['Cube edge × 4', 'Height only', 'Radius only', 'Cone: same rules', 'Both change',
                              'Factor vs percent', 'Percent change', 'Recap'])


# ------------------------------------------------------------------------------------------------
# 1 + 3. existing solution videos
# ------------------------------------------------------------------------------------------------
def _solution_videos(M):
    # Q3: trap answers can be there at any level
    V = 'solve-geo36-g138'
    _replace_say(M, V, 3, "In a harder question, the common mistake usually won't even be in the choices. It's a hint: read the question again.",
                 "A trap answer can be there at any level — in easy questions and in hard ones.")
    _replace_say(M, V, 3, "But in a very easy question — the common-mistake answer CAN be there. Like here: 1 to 9 is choice 2. Don't fall for it.",
                 "Like here: 1 to 9 is choice 2. Found the answer you expected? Read the question again before you circle it.")
    # Q5: 256 is the area ratio squared (not "16 as the edge")
    _replace_say(M, 'solve-geo36-g142', 3, "16 is the area ratio — not the volume. 256 is sixteen squared — the mistake of using 16 as the edge.",
                 "16 is the area ratio — not the volume. 256 is sixteen squared — someone squared the area ratio instead of going back to the edge.")
    # Q6: corresponding angles; part-to-part rule instead of the 1.25 factor
    V = 'solve-geo36-g144'
    _replace_say(M, V, 2, "Call angle A alpha. ED is parallel to AB — so angle E is also alpha. Parallel lines, equal acute angles.",
                 "Call angle A alpha. ED is parallel to AB — so angle E is also alpha. Corresponding angles between parallel lines are equal.")
    b = M.slide(V, 5)
    M.set_slide(V, 5, script=[
        "Now the psychometric way — the part-to-part rule from the lesson.",
        "ED is parallel to AB. A line parallel to one side cuts the other two sides in the same ratio.",
        D('Write "ratio 1 : 2" between BD and DC'),
        "On side CB: BD is 4 and DC is 8 — the ratio 1 to 2.",
        D('Write "ratio 1 : 2" between AE and EC'),
        "So on side CA, AE to EC is also 1 to 2. Part to part — that's allowed.",
        A(b['lines'][5]['label'], b['items'][1]),
        "AE is 5 — so EC is 10, and all of AC is 15. Much, much shorter.",
        "Only the parallel segment itself, ED, must be compared with a WHOLE side.",
        "Which way is better? Here, clearly — the psychometric one. Significantly shorter.",
        D('Circle choice 1'),
        "Choice one.",
    ])
    # Q8: the shortcut
    V = 'solve-geo36-g146'
    M.set_slide(V, 3, script=_script_of(M, V, 3) + [
        "Next time, use the shortcut from the lesson: the altitude squared equals the two parts multiplied.",
        A("'h² = p · q = 9 · 16' appears", T('Shortcut: $h^2=p\\cdot q=9\\cdot16=144$', size=34, x=1060, y=560, w=470)),
        "9 times 16 is 144. The altitude is 12 — in one line.",
    ])
    # Q10: no colon for division on the board
    for it in M.slide('solve-geo36-g148', 5)['items']:
        if it.get('t') == 'Trapezoid $=3$ triangles: $15:3=5$': it['t'] = 'Trapezoid $=3$ triangles: $15\\div3=5$'


# ------------------------------------------------------------------------------------------------
# 3. existing questions: TeX, stacked givens, solutions with numbers
# ------------------------------------------------------------------------------------------------
def _existing_questions(M):
    S = M.set_q
    S('geo36-g136', expl=['A regular octagon with side $s$ has perimeter $P=8s$.',
                          'With side $4s$: $P=8\\cdot4s=32s$, and $\\frac{32s}{8s}=4$.',
                          'A perimeter is a length, so it changes like the side: $\\times4$. ($16$ would be the area factor.)'])
    S('geo36-g137', stem='AB is a diameter of a circle with radius $7$ cm. Four congruent smaller circles have their centers on AB. Their diameters cover AB from end to end, as shown in the figure. What is the sum of the circumferences of the four smaller circles (in cm)?',
      expl=['Each small diameter is $\\frac14$ of AB, so the ratio of the lengths is $1:4$. A circumference is a length, so each small circumference is $\\frac14$ of the large one.',
            'Four small circumferences add up to the large circumference: $2\\pi\\cdot7=14\\pi$.',
            'Check: $AB=14$, the small radius is $\\frac{14}{8}=\\frac74$, and $4\\cdot2\\pi\\cdot\\frac74=14\\pi$.'])
    S('geo36-g138', stem='AB is a diameter of a circle. Point C lies on AB, and $AC=\\frac13AB$. A smaller circle has diameter AC. What is the ratio of the area of the smaller disk to the area inside the larger circle but outside the smaller circle?',
      expl=['The ratio of the diameters is $AC:AB=1:3$, so the ratio of the disk areas is $1^2:3^2=1:9$.',
            'Say the small disk is $1$ unit. Then the whole large disk is $9$ units, and the region outside the small disk is $9-1=8$ units.',
            'The requested ratio is $1:8$. ($1:9$ is the trap — it compares the small disk with the whole large disk.)'])
    S('geo36-g140', stem='In triangle ABC, point D lies on AB and point E lies on AC, and $DE\\parallel BC$.\nGiven:\n$\\begin{cases} AD=3\\text{ cm} \\\\ DB=2\\text{ cm} \\end{cases}$\nWhat is the ratio of the area of triangle ADE to the area of trapezoid DBCE?',
      expl=['$DE\\parallel BC$, so triangles ADE and ABC are similar. AD matches the WHOLE side AB: $AB=3+2=5$.',
            'The ratio of the lengths is $3:5$, so the ratio of the areas is $3^2:5^2=9:25$.',
            'The trapezoid is the whole triangle minus the small one: $25-9=16$ units. The requested ratio is $9:16$.'])
    S('geo36-g142', expl=['Cubes are similar. The ratio of the face areas is $1:16$, so the ratio of the edges is $1:\\sqrt{16}=1:4$.',
                          'The ratio of the volumes is $1^3:4^3=1:64$. So $64$ small cubes fill the large cube.',
                          '($16$ is the area ratio, and $256=16^2$ squares the area ratio.)'])
    S('geo36-g144', stem='In triangle ABC, point D lies on BC and point E lies on AC, and $ED\\parallel AB$.\nGiven:\n$\\begin{cases} BD=4\\text{ cm} \\\\ DC=8\\text{ cm} \\\\ AE=5\\text{ cm} \\end{cases}$\nWhat is the length of AC (in cm)?',
      expl=['$ED\\parallel AB$, so triangles EDC and ABC are similar (corresponding angles, and the angle at C is shared).',
            'DC matches the whole side BC: $BC=4+8=12$. The ratio of the lengths is $\\frac{DC}{BC}=\\frac8{12}=\\frac23$.',
            'EC matches the whole side AC. Let $EC=x$: $\\frac{x}{x+5}=\\frac23$, so $3x=2x+10$ and $x=10$. Then $AC=10+5=15$.',
            'Faster (part to part): the parallel line cuts both sides in the same ratio. $BD:DC=4:8=1:2$, so $AE:EC=1:2$ too: $EC=2\\cdot5=10$ and $AC=15$.'])
    S('geo36-g145', stem='ABC is a right triangle with the right angle at C. DECF is a square: D lies on AB, E lies on BC, and F lies on AC. $AF=3$ cm, and the side of the square is $x$ cm. What is the length of BE (in cm)?',
      expl=['$DF\\parallel BC$ and $DE\\parallel AC$, so triangles AFD and DEB have the same angles: they are similar.',
            'Sides opposite equal angles match: AF matches DE, and FD matches EB. $\\frac{AF}{DE}=\\frac{FD}{EB}$: $\\frac3x=\\frac{x}{BE}$.',
            '$BE=\\frac{x\\cdot x}{3}=\\frac{x^2}{3}$.',
            'Check by plugging in $x=3$: both small triangles are isosceles right triangles, so $BE=3$. Only $\\frac{x^2}3=\\frac93=3$ fits.'])
    S('geo36-g146', stem='ABC is a right triangle with the right angle at A. AD is perpendicular to BC.\nGiven:\n$\\begin{cases} BD=9\\text{ cm} \\\\ DC=16\\text{ cm} \\end{cases}$\nWhat is the length of AD (in cm)?',
      expl=['Triangles ABD and CAD are similar: both have a right angle at D, and the angle BAD equals the angle C (each is $90°$ minus the angle B).',
            'Matching legs: $\\frac{AD}{BD}=\\frac{DC}{AD}$, so $AD^2=9\\cdot16=144$ and $AD=12$.',
            'Shortcut: the altitude to the hypotenuse squared equals the product of the two parts: $h^2=p\\cdot q$.'])
    S('geo36-g147', stem='Two concentric circles have radii $r$ and $1.4r$. Liam claims that the outer circumference is $1.4$ times the inner circumference. Maya claims that the area of the ring between the circles is greater than the area of the inner disk. Who is correct?',
      expl=['Circles are similar. The ratio of the radii is $1:1.4=5:7$.',
            'A circumference is a length, so the ratio of the circumferences is also $5:7$: the outer one is $1.4$ times the inner one. Liam is correct.',
            'The ratio of the areas is $5^2:7^2=25:49$. The ring is $49-25=24$ units, and the inner disk is $25$ units. $24<25$, so Maya is incorrect.',
            'Answer: Liam only.'])
    S('geo36-g148', stem='D and F are the midpoints of sides AB and AC of triangle ABC. The area of trapezoid DBCF is $15$ cm². What is the area of triangle ADF (in cm²)?',
      expl=['A segment that joins two midpoints is parallel to the third side, so triangle ADF is similar to triangle ABC. The ratio of the lengths is $AD:AB=1:2$.',
            'The ratio of the areas is $1^2:2^2=1:4$. Small triangle: $1$ unit. Whole triangle: $4$ units. Trapezoid: $4-1=3$ units.',
            '$3$ units $=15$, so $1$ unit $=15\\div3=5$. The area of triangle ADF is $5$.'])
    S('geo36-g149', expl=['Regular hexagons are similar. The ratio of the areas is $72\\sqrt3:24\\sqrt3=3:1$.',
                          'Go back from areas to lengths with a square root: the ratio of the sides is $\\sqrt3:1$.',
                          'A perimeter is a length, so the ratio of the perimeters is also $\\sqrt3:1$.'])
    S('geo36-g150', expl=['Spheres are similar. Let the large radius be $R$. The small diameter is $\\frac23R$, so the small radius is $\\frac13R$. The ratio of the radii is $1:3$.',
                          'The ratio of the volumes is $1^3:3^3=1:27$. Small ball: $1$ unit. Large sphere: $27$ units.',
                          'Difference: $27-1=26$ units. The requested ratio is $26:1$. ($27:1$ forgets to subtract.)'])
    S('geo36-g151', stem='A cone-shaped tank with base radius $r$ and height $h$ is filled with water using a cone-shaped measuring cup. The cup\'s radius is $\\frac r3$, and its height is $\\frac h4$. How many full cups are needed to fill the tank? (Assume that no water is lost.)',
      expl=['The cones are not similar (the radius and the height change by different factors), so multiply the separate factors.',
            'From the cup to the tank, the radius is multiplied by $3$, so the volume is multiplied by $3^2=9$. The height is multiplied by $4$, so the volume is multiplied by $4$.',
            'Together: $9\\cdot4=36$. So $36$ cups fill the tank.'])

    # ---- practice ----
    S('geo36-core-p01', stem='The two right triangles in the figure stand on the same straight line. The marked angle between their neighboring legs is $90°$. The ratio $a:b=2:3$. What is the ratio $c:d$?',
      expl=['Let the angle at the shared point inside the small triangle be $\\theta$. The marked angle is $90°$, so the angle at the shared point inside the large triangle is $180°-90°-\\theta=90°-\\theta$.',
            'The large triangle has a right angle, so its third angle is $\\theta$. The two triangles have the same angles: they are similar.',
            'a is opposite $\\theta$ in the small triangle, and c is opposite $\\theta$ in the large one. So a matches c, and b matches d.',
            'Therefore the ratio $c:d=a:b=2:3$.'])
    S('geo36-core-p02', stem='Points A, B, C, D and E lie on one straight line, and $AB=BC=CD=DE$. Points F and G lie on a ray from A. EF and CG are perpendicular to AE. What is the ratio $CG:EF$?',
      expl=['Triangles ACG and AEF share the angle at A, and each has a right angle (at C and at E). So they are similar.',
            'AC is $2$ equal parts and AE is $4$ equal parts, so the ratio of the lengths is $2:4=1:2$.',
            'CG matches EF, so the ratio $CG:EF=1:2$.'])
    S('geo36-core-p03', stem='ABCD is a rectangle. E lies on the extension of BA beyond A, F lies on the extension of BC beyond C, and E, D and F lie on one straight line.\nGiven:\n$\\begin{cases} AE=3\\text{ cm} \\\\ CF=5\\text{ cm} \\end{cases}$\nWhat is the area of ABCD (in cm²)?',
      expl=['Triangles EAD and DCF each have a right angle (at A and at C). $AD\\parallel CF$, so the angle at D in triangle EAD equals the angle at F in triangle DCF (corresponding angles). The triangles are similar.',
            'Matching legs: $\\frac{AE}{DC}=\\frac{AD}{CF}$, so $AD\\cdot DC=AE\\cdot CF=3\\cdot5=15$.',
            '$AD\\cdot DC$ is exactly the area of the rectangle: $15$.'])
    S('geo36-core-p04', stem='A, B, C and D lie on a circle. Chords AC and BD meet at E. The ratio $AE:DE$ is $3:5$, and $AB=6$ cm. What is the length of DC (in cm)?',
      expl=['The angles ABD and ACD are inscribed angles on the same arc AD, so they are equal (see the circles topic). The angles AEB and DEC are vertical angles.',
            'So triangles AEB and DEC are similar. AE matches DE, and AB matches DC.',
            '$\\frac{AE}{DE}=\\frac{AB}{DC}$: $\\frac35=\\frac6{DC}$, so $DC=10$.'])
    S('geo36-core-p05', expl=['All squares are similar, and a perimeter is a length.',
                              'So the ratio of the sides equals the ratio of the perimeters: $\\sqrt5:1$.'])
    S('geo36-core-p06', stem='D, E and F are the midpoints of the sides of triangle ABC. The perimeter of triangle DEF is $18$ cm. What is the perimeter of triangle ABC (in cm)?',
      expl=['Each side of DEF joins two midpoints, so it is half of a side of ABC.',
            'So the perimeter of DEF is half the perimeter of ABC, and the perimeter of ABC is $2\\cdot18=36$.'])
    S('geo36-core-p07', stem='A smaller circle is internally tangent at A to a circle with center O. AB is a diameter of the smaller circle, O lies on AB, and $OA=4\\cdot OB$. What is the ratio of the smaller disk\'s area to the larger disk\'s area?',
      expl=['Let $OB=x$. Then $OA=4x$, and the small diameter is $AB=4x+x=5x$.',
            'The large radius is $OA=4x$, so the large diameter is $8x$. The ratio of the diameters is $5:8$.',
            'The ratio of the areas is $5^2:8^2=25:64$, so the answer is $\\frac{25}{64}$.'])
    S('geo36-core-p08', expl=['Sectors with equal central angles are similar. The arc lengths give the ratio of the lengths: $1.5:1=3:2$.',
                              'The ratio of the areas is $3^2:2^2=9:4$.'])
    S('geo36-core-p09', stem='$AB\\parallel CD$, and segments AC and BD meet at E.\nGiven:\n$\\begin{cases} AB=3\\text{ cm} \\\\ CD=5\\text{ cm} \\\\ AE=(x-2)\\text{ cm} \\\\ EC=(x+4)\\text{ cm} \\end{cases}$\nWhat is the value of $x$?',
      expl=['Triangles ABE and CDE are similar (an hourglass: Z angles and vertical angles). AE matches EC, and AB matches CD.',
            '$\\frac{EC}{AE}=\\frac{CD}{AB}$: $\\frac{x+4}{x-2}=\\frac53$.',
            '$3(x+4)=5(x-2)$, so $3x+12=5x-10$, $2x=22$ and $x=11$.',
            'Check: $AE=9$ and $EC=15$, and $\\frac{15}9=\\frac53$ ✓.'])
    S('geo36-core-p11', stem='$AB\\parallel DE$, and segments AE and BD meet at C. The areas of triangles ABC and EDC are $5$ cm² and $20$ cm². What is the ratio $CD:CB$?',
      expl=['The hourglass triangles ABC and EDC are similar. CB (in the small triangle) matches CD (in the large triangle).',
            'The ratio of the areas is $20:5=4:1$, so the ratio of the lengths is $\\sqrt4:1=2:1$.',
            'So the ratio $CD:CB=2:1$.'])
    S('geo36-core-p12', stem='A cone has volume V. Its radius is multiplied by $4$, and its height is halved. The new cone has volume U. What is the ratio $U:V$?',
      expl=['The radius is multiplied by $4$, so the volume is multiplied by $4^2=16$.',
            'The height is halved, so the volume is multiplied by $\\frac12$.',
            'Together: $16\\cdot\\frac12=8$. The ratio $U:V=8:1$.'])
    S('geo36-core-p13', stem='The area of a disk is multiplied by $9x$, where $x>0$. By what factor is its circumference multiplied?', expl=['The area is multiplied by $9x$, so every length is multiplied by $\\sqrt{9x}=3\\sqrt x$.',
                              'The circumference is a length, so it is multiplied by $3\\sqrt x$.'])
    S('geo36-core-p14', stem='E, B and D lie on one straight line. Angles EAB, ABC and BCD are right angles.\nGiven:\n$\\begin{cases} AB=10\\text{ cm} \\\\ BC=12\\text{ cm} \\\\ CD=8\\text{ cm} \\end{cases}$\nWhat is the length of AE (in cm)?',
      expl=['AE and BC are both perpendicular to AB, so $AE\\parallel BC$. AB and CD are both perpendicular to BC, so $AB\\parallel CD$.',
            'So triangles EAB and BCD have the same angles (right angles at A and at C, and corresponding angles at E and at B). They are similar.',
            'AE matches BC, and AB matches CD: $\\frac{AE}{12}=\\frac{10}8$, so $AE=\\frac{120}8=15$.'])
    S('geo36-core-p16', expl=['The cut is parallel to the base, so the small cone is similar to the whole cone. The ratio of the heights is $2:3$.',
                              'The ratio of the volumes is $2^3:3^3=8:27$. Small cone: $8$ units. Whole cone: $27$ units.',
                              'Below the cut: $27-8=19$ units. The requested ratio is $19:8$.'])
    S('geo36-core-p17', stem='Two rectangles share a corner A, and their sides lie on the same two lines. Their opposite corners B and C lie on the same ray from A, with B between A and C. The ratio $AB:BC=3:2$. The larger rectangle has area S. What is the area of the smaller rectangle?',
      expl=['The corner B of the small rectangle is on the diagonal AC of the large one, so the rectangles are similar (a rectangle on the diagonal).',
            'AB matches the WHOLE diagonal AC: $AC=3+2=5$ parts. The ratio of the lengths is $3:5$.',
            'The ratio of the areas is $3^2:5^2=9:25$, so the smaller area is $\\frac9{25}S$.'])
    S('geo36-core-p18', stem='ABC is a right triangle with the right angle at B. A circle with radius r is tangent to AB at D and to BC at E, and its center O lies on AC. $AD=4$ cm. What is the length of BC (in cm)?',
      expl=['A radius is perpendicular to a tangent, so $OD\\perp AB$ and $OE\\perp BC$. ODBE is a square with side r, so $AB=4+r$.',
            '$OD\\parallel BC$, so triangles ADO and ABC are similar: $\\frac{AD}{AB}=\\frac{OD}{BC}$.',
            '$\\frac4{4+r}=\\frac r{BC}$, so $BC=\\frac{r(4+r)}4=r+\\frac{r^2}4$.'])
    S('geo36-core-p19', stem='ACF is a right triangle with the right angle at F. AGHJ and CDEF are squares. G lies on AF, B lies on AC, and $BG\\parallel CF$.\nGiven:\n$\\begin{cases} AJ=5\\text{ cm} \\\\ AB=10\\text{ cm} \\\\ BC=4\\text{ cm} \\end{cases}$\nWhat is the area of square CDEF (in cm²)?',
      expl=['AGHJ is a square, so $AG=AJ=5$.',
            '$BG\\parallel CF$, so triangles ABG and ACF are similar. In triangle ABG, $AG=5$ is half of $AB=10$.',
            'So in triangle ACF, AF is half of AC. $AC=10+4=14$, so $AF=7$.',
            'Pythagoras: $CF^2=14^2-7^2=196-49=147$. The area of the square is $CF^2=147$ (no square root needed).'])
    S('geo36-core-p20', stem='The area of a square increases by $125\\%$. By what percent does its side length increase?',
      expl=['Area $+125\\%$ means an area factor of $2.25$.',
            'The side is a length: $\\sqrt{2.25}=1.5$, so the side increases by $50\\%$.',
            'Check with numbers: side $10$, area $100$. New area $225$, new side $15$. That is $5$ more out of $10$: $50\\%$.'])
    S('geo36-core-p21', stem='The ratio of the perimeters of two similar triangles is $3:5$. The area of the smaller triangle is $54$ cm². What is the area of the larger triangle (in cm²)?',
      expl=['A perimeter is a length, so the ratio of the areas is $3^2:5^2=9:25$.',
            '$9$ units $=54$, so $1$ unit $=54\\div9=6$.',
            'The larger area is $25\\cdot6=150$.'])
    S('geo36-core-p22', stem='At the same time, a vertical pole and a vertical measuring rod $1.8$ m tall cast shadows on level ground. The rod\'s shadow is $2.4$ m long, and the pole\'s shadow is $12$ m long. What is the height of the pole (in m)?',
      expl=['At the same moment, the sun\'s rays make the same angle with the ground. So the pole with its shadow and the rod with its shadow form similar right triangles.',
            'The pole\'s shadow is $12\\div2.4=5$ times the rod\'s shadow.',
            'So the pole is $5$ times as tall as the rod: $5\\cdot1.8=9$ m.'])
    S('geo36-core-p23', stem='A map has a scale of $1:25{,}000$. A park covers $3.2$ cm² on the map. What is the real area of the park (in km²)?',
      expl=['$1$ cm on the map is $25{,}000$ cm $=250$ m $=0.25$ km in reality.',
            'Areas use the square of the scale: $1$ cm² on the map is $0.25^2=0.0625$ km² in reality.',
            '$3.2\\cdot0.0625=0.2$ km².'])
    S('geo36-core-p24', stem='The ratio of the total surface areas of two similar cylinders is $16:25$. The volume of the smaller cylinder is $128\\pi$ cm³. What is the volume of the larger cylinder (in cm³)?',
      expl=['The ratio of the lengths is $\\sqrt{16}:\\sqrt{25}=4:5$.',
            'The ratio of the volumes is $4^3:5^3=64:125$.',
            '$64$ units $=128\\pi$, so $1$ unit $=2\\pi$. The larger volume is $125\\cdot2\\pi=250\\pi$.'])
    S('geo36-core-p25', stem='In triangle ABC, D lies on AB, E lies on AC, and $DE\\parallel BC$. The area of triangle ADE is $64\\%$ of the area of triangle ABC. What fraction of AB is DB?',
      expl=['The area factor is $0.64$, so the length factor is $\\sqrt{0.64}=0.8$.',
            '$AD=0.8\\cdot AB=\\frac45AB$, so $DB=AB-\\frac45AB=\\frac15AB$.'])
    S('geo36-core-p26', expl=['The ratio of the sides is $6:10=3:5$.',
                              'Check the ratio in each choice: $12:15=4:5$, $8:12=2:3$, $10:12=5:6$ and $9:15=3:5$.',
                              'Only the $9$ cm × $15$ cm rectangle has the same ratio.'])
    S('geo36-core-p27', stem='The ratio of the volumes of two similar cones is $27:125$. Their heights differ by $8$ cm. What is the height of the smaller cone (in cm)?',
      expl=['The ratio of the heights is $\\sqrt[3]{27}:\\sqrt[3]{125}=3:5$.',
            'The difference is $5-3=2$ units $=8$ cm, so $1$ unit $=4$ cm.',
            'The smaller height is $3\\cdot4=12$ cm.'])


# ------------------------------------------------------------------------------------------------
# 2. new guided questions with solution videos
# ------------------------------------------------------------------------------------------------
def _solution(M, qid, group_title, sidebar, num, intro, slides, fig=None):
    n = M.next_question_number(TOPIC)
    label = 'Question %d' % n
    act = sidebar.index(label)
    beats = [dict(mode='title', title=label, script=intro)]
    for title, script in slides:
        pre = [Q(qid, fig=fig, figw=0.56, figalign='left')] if fig else [Q(qid)]
        beats.append(dict(mode='question', active=act, title=title, pre=pre, script=script))
    v = M.new_video('solve-' + qid, TOPIC, group_title, sidebar, beats, M.section_of(qid), kind='solution', qid=qid)
    v['beats'][0]['title'] = group_title
    v['hybrid']['num'] = num
    v['title'] = v['navLabel'] = M.q(qid)['stem'].split('Given:')[0].strip()
    return n


def _R(t, y, size=36): return T(t, size=size, x=1060, y=y, w=470)


def _new_guided(M):
    # the Q4 group becomes "Similar Triangles Questions": Q4, same height, trapezoid
    TRI_SB = ['Question 4', 'Question 14', 'Question 15']
    M.set_sidebar('solve-geo36-g140', TRI_SB)
    M.slide('solve-geo36-g140', 1)['title'] = 'Similar Triangles Questions'
    M.video('solve-geo36-g140')['hybrid']['title'] = 'Similar Triangles Questions'

    # ---- same height ----
    g = G[0]
    M.new_q(g, TOPIC, 'In triangle ABC, point D lies on BC. The ratio $BD:DC=2:3$. The area of triangle ABC is $40$ cm². What is the area of triangle ABD (in cm²)?',
            ['$16$', '$6.4$', '$24$', '$20$'], 1,
            ['Triangles ABD and ADC are NOT similar, so do not square. They have the same height: the distance from A to BC.',
             'Area $=\\frac{\\text{base}\\cdot\\text{height}}2$, and the height is the same, so the ratio of the areas is the ratio of the bases: $2:3$.',
             'The whole triangle is $2+3=5$ units $=40$, so $1$ unit $=8$. Triangle ABD: $2\\cdot8=16$.',
             '($6.4=\\frac4{25}\\cdot40$ is the trap: it squares the ratio. $24$ is the area of triangle ADC.)'],
            figure=FIG_Q_SAMEH)
    M.place_q(g, LEARN, after='solve-geo36-g140')
    fig = _qfig(FIG_Q_SAMEH, '70 20 500 320')
    _solution(M, g, 'Similar Triangles Questions', TRI_SB, 73, ["A triangle cut into two pieces. Do we square or not?"], [
        ('Similar? No', [
            "D is on BC, and the ratio BD to DC is 2 to 3. The whole triangle is 40. What is the area of ABD?",
            "The reflex after this topic: 2 to 3 — square it, 4 to 9. Stop!",
            "Are ABD and ADC similar? Look at the angles: the angle at B and the angle at C are different. Not similar.",
            D('Trace the dashed height from A to BC'),
            "But they share something: the height. The same distance from A down to BC.",
            A("'Same height → area ratio = base ratio' appears", _R('Same height $\\rightarrow$ area ratio $=$ base ratio', 280, 34)),
            "Area is base times height over 2. Same height — so the areas are in the ratio of the bases: 2 to 3.",
        ]),
        ('Units', [
            A("'2 + 3 = 5 units = 40' appears", _R('$2+3=5$ units $=40$', 280)),
            "The whole triangle: 2 plus 3 — 5 units. 5 units are 40, so one unit is 8.",
            A("'ABD = 2 · 8 = 16' appears", _R('$S_{ABD}=2\\cdot8=16$', 370)),
            "Triangle ABD is 2 units: 16.",
            D('Circle choice 1'),
            "Choice one.",
            D('Next to choice 2 write "squared ✗"'),
            "6.4 is the trap — someone squared the ratio. And 24 is the other triangle, ADC.",
        ]),
    ], fig)

    # ---- trapezoid diagonals ----
    g = G[1]
    M.new_q(g, TOPIC, 'ABCD is a trapezoid with $AB\\parallel DC$. Its diagonals meet at O.\nGiven:\n$\\begin{cases} AB=4\\text{ cm} \\\\ DC=6\\text{ cm} \\end{cases}$\nThe area of triangle AOB is $8$ cm². What is the area of the trapezoid (in cm²)?',
            ['$26$', '$42$', '$50$', '$72$'], 3,
            ['Triangles AOB and COD form an hourglass: they are similar, with the ratio $AB:DC=4:6=2:3$. The ratio of their areas is $2^2:3^2=4:9$.',
             'Triangle AOD has the same height as triangle AOB (from A to the diagonal BD), and its base OD is $3$ parts while OB is $2$ parts. So its area is $2\\cdot3=6$ units. Triangle BOC is also $6$ units.',
             'In all: $4+6+6+9=25$ units. Triangle AOB is $4$ units $=8$, so $1$ unit $=2$.',
             'The trapezoid is $25\\cdot2=50$. ($26$ forgets the two side triangles.)'],
            figure=FIG_Q_TRAP)
    M.place_q(g, LEARN, after='solve-' + G[0])
    fig = _qfig(FIG_Q_TRAP, '120 70 400 260')
    _solution(M, g, 'Similar Triangles Questions', TRI_SB, 73, ["A trapezoid with its diagonals — four triangles."], [
        ('The hourglass', [
            "ABCD is a trapezoid, AB parallel to DC. AB is 4, DC is 6. The diagonals meet at O. Triangle AOB is 8. What is the whole trapezoid?",
            "Inside every trapezoid with its diagonals — an hourglass: the top triangle and the bottom triangle.",
            D('Point to the shaded triangles AOB and COD'),
            "They're similar. The ratio of the bases: 4 to 6 — 2 to 3.",
            A("'Top and bottom: 4 and 9' appears", _R('Top, bottom: $2^2=4$ and $3^2=9$', 280)),
            "The areas — square it: 4 and 9 units.",
        ]),
        ('The side triangles', [
            "Now the side triangles. Triangle AOD and triangle AOB have the same height — from A down to the diagonal BD.",
            "Their bases on BD are OD and OB — 3 parts and 2 parts. Same height, so no squaring.",
            A("'Sides: 2 · 3 = 6 each' appears", _R('Sides: $2\\cdot3=6$ each', 280)),
            "The top is 4 units, so the side triangle is 6 units. The other side triangle — also 6. Always a times b.",
            A("'4 + 6 + 6 + 9 = 25 units' appears", _R('$4+6+6+9=25$ units', 370)),
            "4, 6, 6, 9 — 25 units in all.",
        ]),
        ('Units to cm²', [
            A("'4 units = 8 → 1 unit = 2' appears", _R('$4$ units $=8\\Rightarrow1$ unit $=2$', 280)),
            "The top triangle is 4 units, and it is 8. So one unit is 2.",
            A("'25 · 2 = 50' appears", _R('Trapezoid: $25\\cdot2=50$', 370)),
            "The trapezoid: 25 units, times 2 — 50.",
            D('Circle choice 3'),
            "Choice three.",
            "26 forgot the side triangles. 42 thought the side triangles were equal to the top one.",
        ]),
    ], fig)

    # ---- percent change in volume (after the "Volume Changes" lesson) ----
    g = G[2]
    M.new_q(g, TOPIC, 'Each edge of a cube is increased by $20\\%$. By what percent does the volume of the cube increase?',
            ['$60\\%$', '$44\\%$', '$72.8\\%$', '$20\\%$'], 3,
            ['Turn the percent into a factor: $+20\\%$ means $\\times1.2$.',
             'Volume: cube the factor. $1.2^3=1.44\\cdot1.2=1.728$.',
             '$\\times1.728$ is an increase of $72.8\\%$.',
             'Check with numbers: edge $10$, volume $1000$. Edge $12$, volume $1728$. The increase is $728$ out of $1000$: $72.8\\%$. ($60\\%=3\\cdot20\\%$ is the trap, and $44\\%$ is the increase of the area of a face.)'])
    M.place_q(g, LEARN, after='geo-143')
    _solution(M, g, 'Volume Changes Question', ['Question 16'], 76, ["Percent and volume — a classic trap."], [
        ('Percent → factor', [
            "Each edge of a cube grows by 20 percent. By what percent does the volume grow?",
            "The trap: 3 times 20 — 60 percent. Percents don't work like that.",
            "First, turn the percent into a factor. Plus 20 percent — times 1.2.",
            A("'+20% → × 1.2' appears", P('$+20\\%\\ \\rightarrow\\ \\times1.2$', size=38)),
            "The cube stays a cube — a similar solid. Volume: cube the factor.",
            A("'1.2³ = 1.728' appears", P('$1.2^3=1.44\\cdot1.2=1.728$', size=38)),
            "1.2 squared is 1.44. Times 1.2 again — 1.728.",
            A("'× 1.728 → +72.8%' appears", P('$\\times1.728\\ \\rightarrow\\ +72.8\\%$', size=38)),
            "Times 1.728 — back to percent: plus 72.8 percent.",
            D('Circle choice 3'),
            "Choice three.",
        ]),
        ('Check · plug in 10', [
            "Don't trust the decimals? Plug in an easy edge: 10.",
            A("'10³ = 1000 · 12³ = 1728' appears", P('$10^3=1000\\qquad12^3=1728$', size=38)),
            "Volume 1000. Plus 20 percent — the edge is 12. 12 cubed is 1728.",
            "The volume grew by 728 out of 1000 — 72.8 percent. The same answer.",
            "44 percent is the AREA of a face: 1.2 squared. Read what they ask.",
        ]),
    ])


# ------------------------------------------------------------------------------------------------
# 2. map scale: lesson + 2 guided questions + card
# ------------------------------------------------------------------------------------------------
def _map_block(M):
    sb = ['Scale 1 : n', 'Units ladder', 'Length example', 'Area example', 'Recap']
    v = M.new_video(MAP, TOPIC, 'Map Scale', sb, [
        dict(mode='title', title='Map Scale', script=[
            "The last part of the topic: scale.",
            "A map is a similar copy of the real world — just much smaller.",
            "So everything we learned about similarity works on maps.",
        ]),
        dict(mode='concept', active=0, title='Scale 1 : n', script=[
            "The scale is a ratio: a length on the map to the real length.",
            A("'Scale 1 : 25,000' appears", T('Scale $1:25{,}000$: $1$ cm on the map $=25{,}000$ cm in reality', size=40)),
            "Scale 1 to 25,000: every centimeter on the map is 25,000 centimeters in reality.",
            "The map and the land are similar shapes. The scale is the linear ratio.",
            A("'Lengths × n · areas × n²' appears", T('Lengths $\\times n$ $\\cdot$ areas $\\times n^2$', size=46)),
            "So real lengths are n times the map lengths. And real areas — n squared times the map areas.",
        ]),
        dict(mode='concept', active=1, title='Units ladder', script=[
            "The map gives centimeters. The question asks for meters or kilometers. So we need the units ladder.",
            A("'km → m → cm' appears", T('$1$ km $=1000$ m $\\qquad 1$ m $=100$ cm', size=44)),
            "One kilometer is 1000 meters. One meter is 100 centimeters.",
            A("'1 km = 100,000 cm' appears", T('$1$ km $=100{,}000$ cm', size=44)),
            "So one kilometer is 100,000 centimeters. From centimeters to kilometers: divide by 100, then by 1000.",
            A("'1 km² = 10¹⁰ cm²' appears", T('Areas: $1$ km$^2=100{,}000^2$ cm$^2=10^{10}$ cm$^2$', size=40)),
            "Careful with areas: the conversion is squared too! One square kilometer is 100,000 squared square centimeters.",
            "That's why I convert lengths first — and square only at the end.",
        ]),
        dict(mode='concept', active=2, title='Length example', script=[
            "A length example.",
            A("'Scale 1 : 50,000, map distance 6 cm' appears", T('Scale $1:50{,}000$, map distance $6$ cm', size=44)),
            "The scale is 1 to 50,000. Two villages are 6 centimeters apart on the map. How far apart are they?",
            A("'6 · 50,000 = 300,000 cm' appears", T('$6\\cdot50{,}000=300{,}000$ cm', size=44)),
            "6 times 50,000 — 300,000 centimeters.",
            A("'= 3,000 m = 3 km' appears", T('$=3{,}000$ m $=3$ km', size=44)),
            "Divide by 100 — 3,000 meters. Divide by 1000 — 3 kilometers.",
        ]),
        dict(mode='concept', active=3, title='Area example', script=[
            "Now an area. This is where most students fall.",
            A("'Scale 1 : 50,000, map area 8 cm²' appears", T('Scale $1:50{,}000$, map area $8$ cm$^2$', size=44)),
            "The same map. A forest covers 8 square centimeters on the map. What is its real area in square kilometers?",
            "My trick: first change ONE map centimeter into the real unit.",
            A("'1 cm → 0.5 km' appears", T('$1$ cm $\\rightarrow50{,}000$ cm $=0.5$ km', size=44)),
            "One centimeter — 50,000 centimeters — 500 meters — half a kilometer.",
            A("'1 cm² → 0.25 km²' appears", T('$1$ cm$^2\\rightarrow0.5^2=0.25$ km$^2$', size=44)),
            "Now square it: one square centimeter on the map is 0.25 square kilometers.",
            A("'8 · 0.25 = 2 km²' appears", T('$8\\cdot0.25=2$ km$^2$ (not $8\\cdot0.5=4$)', size=44)),
            "8 times 0.25 — 2 square kilometers. The trap is 4: someone forgot to square.",
        ]),
        dict(mode='concept', active=4, title='Recap', script=[
            A("'Scale 1 : n: lengths × n, areas × n²' appears", T('Scale $1:n$: lengths $\\times n$, areas $\\times n^2$', size=44)),
            "Scale 1 to n: lengths times n, areas times n squared.",
            A("'Convert 1 map cm first, then square' appears", T('Convert $1$ map cm to the real unit first — then square for areas', size=38)),
            "Change one map centimeter into the unit they want. For areas — square it.",
            A("'Ladder: cm ÷ 100 → m ÷ 1000 → km' appears", T('Ladder: cm $\\div100\\rightarrow$ m $\\div1000\\rightarrow$ km', size=40)),
            "And climb the ladder carefully: divide by 100, then by 1000.",
        ]),
    ], LEARN, after='solve-geo36-g151')
    v['hybrid']['num'] = 78

    MSB = ['Question 17', 'Question 18']
    g = G[3]
    M.new_q(g, TOPIC, 'A map has a scale of $1:20{,}000$. On the map, the distance between two towns is $7.5$ cm. What is the real distance between the towns (in km)?',
            ['$15$', '$1.5$', '$150$', '$0.15$'], 2,
            ['Scale $1:20{,}000$: every real length is $20{,}000$ times the length on the map.',
             '$7.5\\cdot20{,}000=150{,}000$ cm.',
             'From cm to m, divide by $100$: $1{,}500$ m. From m to km, divide by $1000$: $1.5$ km.'])
    M.place_q(g, LEARN, after=MAP)
    _solution(M, g, 'Map Scale Questions', MSB, 79, ["A map question — lengths."], [
        ('Map to reality', [
            "The scale is 1 to 20,000. The towns are 7.5 centimeters apart on the map. How far apart are they in reality, in kilometers?",
            "Scale 1 to 20,000: every real length is 20,000 times the map length.",
            A("'7.5 · 20,000 = 150,000 cm' appears", P('$7.5\\cdot20{,}000=150{,}000$ cm', size=38)),
            "7.5 times 20,000 — 150,000 centimeters.",
        ]),
        ('Units ladder', [
            "Now the units. They asked for kilometers.",
            A("'150,000 cm ÷ 100 = 1,500 m' appears", P('$150{,}000$ cm $\\div100=1{,}500$ m', size=38)),
            "Centimeters to meters: divide by 100. 1,500 meters.",
            A("'1,500 m ÷ 1000 = 1.5 km' appears", P('$1{,}500$ m $\\div1000=1.5$ km', size=38)),
            "Meters to kilometers: divide by 1000. 1.5 kilometers.",
            D('Circle choice 2'),
            "Choice two.",
            "The other choices are unit mistakes. Climb the ladder step by step.",
        ]),
    ])
    g = G[4]
    M.new_q(g, TOPIC, 'A map has a scale of $1:40{,}000$. A lake covers $5$ cm² on the map. What is the real area of the lake (in km²)?',
            ['$2$', '$0.08$', '$0.8$', '$8$'], 3,
            ['First change one map centimeter to kilometers: $1$ cm $\\rightarrow40{,}000$ cm $=400$ m $=0.4$ km.',
             'Areas use the square of the scale: $1$ cm² on the map is $0.4^2=0.16$ km² in reality.',
             '$5\\cdot0.16=0.8$ km². ($5\\cdot0.4=2$ is the trap: the scale was not squared.)'])
    M.place_q(g, LEARN, after='solve-' + G[3])
    _solution(M, g, 'Map Scale Questions', MSB, 79, ["A map question — areas. Here's the classic trap."], [
        ('One cm first', [
            "Scale 1 to 40,000. A lake covers 5 square centimeters on the map. What is its real area in square kilometers?",
            "My trick: first change ONE map centimeter into the real unit they want.",
            A("'1 cm → 0.4 km' appears", P('$1$ cm $\\rightarrow40{,}000$ cm $=400$ m $=0.4$ km', size=38)),
            "40,000 centimeters — 400 meters — 0.4 kilometers.",
        ]),
        ('Then square', [
            "Now the area. The map and the lake are similar — areas use the square.",
            A("'1 cm² → 0.16 km²' appears", P('$1$ cm$^2\\rightarrow0.4^2=0.16$ km$^2$', size=38)),
            "One square centimeter on the map is 0.4 squared — 0.16 square kilometers.",
            A("'5 · 0.16 = 0.8 km²' appears", P('$5\\cdot0.16=0.8$ km$^2$', size=38)),
            "Five of them: 0.8.",
            D('Circle choice 3'),
            "Choice three.",
            "2 is the trap: 5 times 0.4 — someone forgot to square.",
        ]),
    ])


# ------------------------------------------------------------------------------------------------
# 2 + 5. new practice questions
# ------------------------------------------------------------------------------------------------
NEW_PRACTICE = [
    # 06 part to part
    ('In triangle ABC, point D lies on AB and point E lies on AC, and $DE\\parallel BC$.\nGiven:\n$\\begin{cases} AD=4\\text{ cm} \\\\ DB=6\\text{ cm} \\\\ AE=6\\text{ cm} \\end{cases}$\nWhat is the length of EC (in cm)?',
     ['$4$', '$9$', '$15$', '$10$'], 2,
     ['A line parallel to BC cuts the other two sides in the same ratio (part to part): $\\frac{AD}{DB}=\\frac{AE}{EC}$.',
      '$\\frac46=\\frac6{EC}$, so $4\\cdot EC=36$ and $EC=9$.',
      'Check with the whole sides: $\\frac{AD}{AB}=\\frac4{10}$ and $\\frac{AE}{AC}=\\frac6{15}=\\frac4{10}$ ✓.'], FIG_P_PARTS),
    # 07 the segment against the whole side
    ('In triangle ABC, point D lies on AB and point E lies on AC, and $DE\\parallel BC$.\nGiven:\n$\\begin{cases} AD=2\\text{ cm} \\\\ DB=3\\text{ cm} \\\\ DE=4\\text{ cm} \\end{cases}$\nWhat is the length of BC (in cm)?',
     ['$6$', '$8$', '$10$', '$12$'], 3,
     ['Triangles ADE and ABC are similar. DE is not a part of a side, so it matches the WHOLE side BC, and AD matches the WHOLE side AB.',
      '$AB=2+3=5$. $\\frac{DE}{BC}=\\frac{AD}{AB}$: $\\frac4{BC}=\\frac25$, so $BC=10$.',
      '($6=4\\cdot\\frac32$ is the trap: it uses the part DB instead of the whole side AB.)'], FIG_P_WHOLE),
    # 08 same height
    ('In triangle ABC, point D lies on BC. The area of triangle ABD is $12$ cm², the area of triangle ADC is $18$ cm², and $BC=20$ cm. What is the length of BD (in cm)?',
     ['$6$', '$8$', '$10$', '$12$'], 2,
     ['Triangles ABD and ADC have the same height (from A to BC). So the ratio of their areas is the ratio of their bases: $BD:DC=12:18=2:3$.',
      '$BC$ is $2+3=5$ parts $=20$, so $1$ part $=4$.',
      '$BD=2\\cdot4=8$.'], FIG_P_SAMEH),
    # 09 same height inside a "similar" picture
    ('In triangle ABC, point D lies on AB and point E lies on AC, and $DE\\parallel BC$. The ratio $AD:DB=1:2$. What is the ratio of the area of triangle ADE to the area of triangle DBE?',
     ['$1:4$', '$1:2$', '$1:8$', '$1:3$'], 2,
     ['Triangles ADE and DBE are not similar. They have the same height: the distance from E to the line AB.',
      'So the ratio of their areas is the ratio of their bases: $AD:DB=1:2$.',
      '($1:4$ squares a ratio of shapes that are not similar. $1:8$ compares ADE with the trapezoid DBCE.)'], FIG_P_ADE),
    # 10 trapezoid: areas 4 and 25
    ('ABCD is a trapezoid with $AB\\parallel DC$. Its diagonals meet at O. The area of triangle AOB is $4$ cm², and the area of triangle COD is $25$ cm². What is the area of triangle BOC (in cm²)?',
     ['$10$', '$12.5$', '$14.5$', '$21$'], 1,
     ['The ratio of the areas of the hourglass triangles is $4:25=2^2:5^2$, so the ratio of the bases is $AB:DC=2:5$.',
      'With bases in the ratio $a:b$, the four triangles are $a^2$, $ab$, $ab$ and $b^2$: here $4$, $10$, $10$ and $25$.',
      'Triangle BOC is $ab=2\\cdot5=10$.'], FIG_P_TRAP),
    # 11 trapezoid: fraction
    ('ABCD is a trapezoid with $AB\\parallel DC$, and its diagonals meet at O.\nGiven:\n$\\begin{cases} AB=3\\text{ cm} \\\\ DC=9\\text{ cm} \\end{cases}$\nWhat fraction of the area of the trapezoid is the area of triangle COD?',
     ['$\\frac34$', '$\\frac9{16}$', '$\\frac9{10}$', '$\\frac12$'], 2,
     ['The ratio of the bases is $3:9=1:3$. The four triangles are $1^2$, $1\\cdot3$, $1\\cdot3$ and $3^2$ units: $1$, $3$, $3$ and $9$.',
      'The trapezoid is $1+3+3+9=16$ units, and triangle COD is $9$ units.',
      'So COD is $\\frac9{16}$ of the trapezoid. ($\\frac9{10}$ forgets the two side triangles.)'], None),
    # 12 leg squared
    ('ABC is a right triangle with the right angle at A. AD is perpendicular to BC.\nGiven:\n$\\begin{cases} BD=4\\text{ cm} \\\\ BC=25\\text{ cm} \\end{cases}$\nWhat is the length of AB (in cm)?',
     ['$10$', '$2\\sqrt{21}$', '$5$', '$20$'], 1,
     ['Triangles ABD and CBA are similar (right angles at D and at A, and the shared angle B). The hypotenuse AB of the small triangle matches the hypotenuse CB of the large one, and BD matches BA.',
      '$\\frac{BD}{AB}=\\frac{AB}{BC}$, so $AB^2=BD\\cdot BC=4\\cdot25=100$ and $AB=10$.',
      'Shortcut: $\\text{leg}^2=\\text{its part}\\cdot\\text{hypotenuse}$. ($2\\sqrt{21}$ is AD: $AD^2=4\\cdot21=84$.)'], FIG_P_ALT),
    # 13 cone glass 2/3 height
    ('A cone-shaped glass stands on its vertex. When it is full, it holds $216$ cm³ of water. Water is poured into the empty glass until the water reaches $\\frac23$ of the glass\'s height. How much water is in the glass (in cm³)?',
     ['$144$', '$96$', '$64$', '$72$'], 3,
     ['The water forms a small cone that is similar to the glass: its height AND its radius are $\\frac23$ of the glass\'s.',
      'Volume: $\\left(\\frac23\\right)^3=\\frac8{27}$ of the glass.',
      '$\\frac8{27}\\cdot216=8\\cdot8=64$. ($144=\\frac23\\cdot216$ forgets to cube, and $96=\\frac49\\cdot216$ squares instead of cubing.)'], FIG_P_GLASS),
    # 14 sphere surface -10%
    ('The radius of a sphere is decreased by $10\\%$. By what percent does the surface area of the sphere decrease?',
     ['$10\\%$', '$20\\%$', '$19\\%$', '$27.1\\%$'], 3,
     ['$-10\\%$ means a factor of $0.9$. The surface is an area, so square the factor: $0.9^2=0.81$.',
      '$\\times0.81$ is a decrease of $19\\%$. ($27.1\\%$ is the decrease of the volume: $1-0.9^3=0.271$.)'], None),
    # 15 circle area +69%
    ('The area of a circle increases by $69\\%$. By what percent does its radius increase?',
     ['$13\\%$', '$30\\%$', '$34.5\\%$', '$69\\%$'], 2,
     ['Area $+69\\%$ means an area factor of $1.69$.',
      'The radius is a length: take the square root. $\\sqrt{1.69}=1.3$, an increase of $30\\%$.',
      'Check: radius $10$, area $100\\pi$. Radius $13$, area $169\\pi$, which is $69\\%$ more ✓.'], None),
    # 16 find the scale
    ('Two cities are $36$ km apart. On a map, they are $12$ cm apart. What is the scale of the map?',
     ['$1:3{,}000$', '$1:30{,}000$', '$1:300{,}000$', '$1:3{,}000{,}000$'], 3,
     ['Change the real distance to centimeters: $36$ km $=36{,}000$ m $=3{,}600{,}000$ cm.',
      'Every map centimeter stands for $3{,}600{,}000\\div12=300{,}000$ cm.',
      'The scale is $1:300{,}000$.'], None),
    # 17 two maps
    ('Two maps show the same region. Map A has a scale of $1:10{,}000$, and map B has a scale of $1:30{,}000$. A park covers $18$ cm² on map A. How many cm² does it cover on map B?',
     ['$6$', '$2$', '$54$', '$3$'], 2,
     ['The same real length is $3$ times shorter on map B ($30{,}000$ is $3$ times $10{,}000$). The ratio of the lengths (B to A) is $1:3$.',
      'The ratio of the areas is $1^2:3^2=1:9$.',
      '$18\\div9=2$ cm². ($6$ forgets to square.)'], None),
    # 18 field in m²
    ('A map has a scale of $1:5{,}000$. On the map, a rectangular field measures $4$ cm by $3$ cm. What is the real area of the field (in m²)?',
     ['$600$', '$3{,}000$', '$30{,}000$', '$300{,}000$'], 3,
     ['$1$ cm on the map $\\rightarrow5{,}000$ cm $=50$ m in reality.',
      'The real sides: $4\\cdot50=200$ m and $3\\cdot50=150$ m.',
      'Area: $200\\cdot150=30{,}000$ m². ($600=12\\cdot50$ forgets to square the scale.)'], None),
]


def _new_practice(M):
    for k, (stem, ch, c, ex, fig) in enumerate(NEW_PRACTICE):
        g = G[5 + k]
        M.new_q(g, TOPIC, stem, ch, c, ex, figure=fig)
        M.place_q(g, PRACTICE)
    # pass 2: p10 and p15 are originals and stay (restored)
    M.set_q('geo36-core-p10', stem='A disk is inscribed in a semicircle of radius $6$ cm. It is tangent to the diameter at its midpoint O and tangent internally to the semicircular arc. What fraction of the semicircle\u2019s area lies outside the disk?',
            expl=['The disk touches the diameter at O, so its center lies directly above O, at a distance equal to its radius $r$.',
                  'It also touches the arc from the inside, so the distance from O to its center is $6-r$. Therefore $r=6-r$, and $r=3$.',
                  'The semicircle: $\\frac{\\pi\\cdot6^2}{2}=18\\pi$. The disk: $\\pi\\cdot3^2=9\\pi$. Outside the disk: $18\\pi-9\\pi=9\\pi$.',
                  'The fraction is $\\frac{9\\pi}{18\\pi}=\\frac12$.'])
    M.set_q('geo36-core-p15', stem='A regular heptagon with side $2$ cm has area $a$ cm². What is the area of a regular heptagon with side $5$ cm (in cm²)?',
            expl=['Regular heptagons are similar. The ratio of the sides is $5:2$, so every length is multiplied by $\\frac52$.',
                  'Areas use the square: $\\left(\\frac52\\right)^2=\\frac{25}{4}$.',
                  'The new area is $\\frac{25}{4}\\cdot a=\\frac{25a}{4}$ cm².'])


def _practice(M):
    p = lambda n: 'geo36-core-p%02d' % n
    order = [p(5), p(26), p(6), p(13), p(8), p(15), p(21), p(12), G[5], p(2), p(22), G[15], p(20), G[14], p(11),
             G[7], p(23), G[17], G[6], p(25), p(7), p(16), p(4), p(1), p(9), p(10), p(14), G[13], G[11], G[9],
             G[10], G[8], G[16], p(24), p(27), G[12], p(17), p(3), p(18), p(19)]
    if 'geo35-core-p27' in M.D['questions'] and M.section_of('geo35-core-p27') == PRACTICE:   # moved here by t35
        order.insert(order.index(G[8]) + 1, 'geo35-core-p27')
    M.practice_order(PRACTICE, order)


# ------------------------------------------------------------------------------------------------
# memory cards
# ------------------------------------------------------------------------------------------------
def _cards(M):
    c = M.card('mem-similarity')
    c['tips'] = [t for t in c['tips'] if not t.startswith('Man with glasses')] + [
        'Man with glasses: two equal circles on the diameter of a big circle — the top leftover \\(=\\) one small circle.',
        'NOT always similar: rectangles, rhombuses, isosceles triangles, right triangles — check the angles or both dimensions.']

    c = M.card('mem-similar-triangles')
    c['tables'].append({'title': 'Shortcuts', 'head': ['Picture', 'Rule'], 'rows': [
        ['!Parallel line — parts of the sides', 'part to part: \\(\\frac{AD}{DB}=\\frac{AE}{EC}\\) — but \\(DE\\leftrightarrow BC\\) (the WHOLE side)'],
        ['!Same height, NOT similar', 'area ratio \\(=\\) base ratio — do NOT square'],
        ['Altitude to the hypotenuse', '\\(h^2=p\\cdot q\\) · \\(\\text{leg}^2=\\text{its part}\\cdot\\text{hypotenuse}\\)'],
        ['!Trapezoid with its diagonals (bases \\(a\\), \\(b\\))', 'four triangles: \\(a^2,\\ ab,\\ ab,\\ b^2\\) — the side triangles are equal'],
    ]})
    c['tips'] = c['tips'] + ['Stuck? Plug in: an easy angle (\\(20°\\)) to see what matches what, or an easy number (\\(x=3\\)) and test the choices.']

    c = M.card('mem-similar-solids')
    c['tables'][0]['rows'] += [
        ['!Sides \\(+10\\%\\) (factor \\(1.1\\))', '\\(\\times1.21\\) (\\(+21\\%\\))', '\\(\\times1.331\\) (\\(+33.1\\%\\))'],
        ['Cone filled to half its height', '', 'water \\(=\\left(\\frac12\\right)^3=\\frac18\\) of the cone'],
    ]
    c['tips'] = c['tips'] + ['Spheres are always similar, like circles and cubes.',
                             'Percent \\(\\rightarrow\\) factor \\(\\rightarrow\\) power \\(\\rightarrow\\) back to percent.']

    M.new_card('mem-r26-t36-map-scale', TOPIC, LEARN, {
        'title': 'Map scale',
        'intro': 'A map is similar to the real land. The scale \\(1:n\\) is the linear ratio.',
        'tables': [{'title': '', 'head': ['What', 'Rule', 'Example (scale \\(1:50{,}000\\))'], 'rows': [
            ['!Lengths', '\\(\\times n\\)', '\\(6\\) cm \\(\\rightarrow300{,}000\\) cm \\(=3\\) km'],
            ['!Areas', '\\(\\times n^2\\)', '\\(1\\) cm \\(\\rightarrow0.5\\) km, so \\(8\\) cm² \\(\\rightarrow8\\cdot0.25=2\\) km²'],
            ['Units', '\\(1\\) km \\(=1000\\) m, \\(1\\) m \\(=100\\) cm', '\\(1\\) km \\(=100{,}000\\) cm'],
        ]}],
        'tips': ['Change ONE map centimeter into the unit they ask for first — then square it for areas.',
                 'Area trap: multiplying by the scale without squaring.'],
    }, after='solve-' + G[4])


# ------------------------------------------------------------------------------------------------
# wording in all topic-36 videos: American spelling, "the psychometric" as a noun
# ------------------------------------------------------------------------------------------------
REPL = [('centimetres', 'centimeters'), ('centimetre', 'centimeter'), ('On the psychometric, ', 'On the exam, '),
        ('on the psychometric that', 'on the exam that'), ('On the psychometric exam', 'On the exam')]


def _wording(M):
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        hit = False
        for b in v['beats']:
            for l in b['lines']:
                for k in ('say', 'draw', 'label'):
                    if k in l:
                        s = l[k]
                        for a, c in REPL: s = s.replace(a, c)
                        if s != l[k]: l[k] = s; hit = True
        if hit: M.touched_videos.add(v['id'])


def _sync_stem_copies(M):
    """solution videos: keep the pre-loaded description in step with the (rewritten) stem"""
    for v in M.D['videos'].values():
        qid = v.get('questionId')
        if v['topic'] != TOPIC or not qid or qid not in M.D['questions']: continue
        q = M.q(qid)
        for b in v['beats']:
            if (b.get('canvas') or '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])


# ------------------------------------------------------------------------------------------------
# Pass 2: summary lesson right before the practice
# ------------------------------------------------------------------------------------------------
def summary(M):
    sb = ['Length, area, volume', 'Always similar?', 'Similar triangles', 'The exam pictures', 'Same height',
          'Parts and leftovers', 'Similar solids', 'Percent change', 'Map scale', 'Before you practice']
    S = lambda k, script: dict(title=sb[k], mode='concept', active=k, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of similarity.",
            "Everything important, one idea at a time."]),
        S(0, [
            A("'Length k · area k² · volume k³' appears", T('Length $k$ $\\cdot$ area $k^2$ $\\cdot$ volume $k^3$', size=48, gap=30)),
            "Similar shapes: every matching line has the same ratio — sides, heights, diagonals, perimeters, circumferences.",
            "Areas — square it. Volumes — cube it.",
            A("'3 : 4 → 9 : 16 → 27 : 64' appears", T('Linear $3:4$ $\\rightarrow$ area $9:16$ $\\rightarrow$ volume $27:64$', size=42, gap=30)),
            A("'Area 36 : 49 → linear 6 : 7' appears", T('Back: area $36:49$ $\\rightarrow$ linear $6:7$ (square root)', size=40)),
            "Going back from areas to lengths? Take the square root."]),
        S(1, [
            A("'Always similar' appears", T('Always similar: circles · squares · equilateral triangles · regular polygons (same number of sides) · cubes · spheres', size=34, gap=30)),
            "Some shapes are always similar: circles, squares, equilateral triangles, regular polygons with the same number of sides. Cubes and spheres too.",
            A("'NOT always' appears", T('NOT always: rectangles · rhombuses · isosceles triangles · right triangles', size=36, gap=30)),
            "Others are not. A rectangle needs both dimensions to grow by one factor.",
            A("'Man with glasses' appears", T('Man with glasses: top leftover $=$ one small circle', size=40)),
            "And the man with glasses: the top leftover is exactly one small circle."]),
        S(2, [
            A("'Two equal angles → similar' appears", T('Two equal angles $\\rightarrow$ similar triangles', size=44, gap=30)),
            "Two equal angles are enough. The third completes to 180.",
            A("'Match sides opposite equal angles' appears", T('Match sides opposite equal angles — make a small–big table', size=38, gap=30)),
            "Match the sides by the angles, not by left and right. Then make the small–big table.",
            "Stuck on what matches what? Plug in an easy angle, like 20 degrees, and follow it."]),
        S(3, [
            A("'Parallel to the base' appears", T('Parallel line: part to part ✓ · the segment $\\leftrightarrow$ the WHOLE side', size=36, gap=30)),
            "A line parallel to the base: part to part is fine. The parallel segment itself — always against the whole side.",
            A("'Hourglass' appears", T('Hourglass: parallel lines, two similar triangles', size=40, gap=30)),
            A("'Altitude to the hypotenuse' appears", T('Altitude to the hypotenuse: $h^2=p\\cdot q$ · $\\text{leg}^2=\\text{its part}\\cdot\\text{hypotenuse}$', size=36)),
            "The altitude to the hypotenuse: parts 4 and 25 — the altitude squared is 100. It's 10."]),
        S(4, [
            A("'Same height → area ratio = base ratio' appears", T('Same height, NOT similar $\\rightarrow$ area ratio $=$ base ratio', size=40, gap=30)),
            "Not similar, but the same height? The areas follow the bases. No squaring! 3 to 7 stays 3 to 7.",
            A("'Trapezoid: a², ab, ab, b²' appears", T('Trapezoid with its diagonals, bases $a$, $b$: $a^2,\\ ab,\\ ab,\\ b^2$', size=38)),
            "A trapezoid with its diagonals: the hourglass triangles are a squared and b squared. The side triangles — a times b each."]),
        S(5, [
            A("'Leftover = whole − part' appears", T('Leftover $=$ whole $-$ part: $1:25$ $\\rightarrow$ $1:24$', size=42, gap=30)),
            "Read what they compare. The small circle to the whole big circle — 1 to 25. To what's left — 1 to 24.",
            A("'Work in units' appears", T('Small $4$ units, whole $49$ $\\rightarrow$ trapezoid $49-4=45$', size=40)),
            "Work in units: square the ratio, subtract, and then find what one unit is worth."]),
        S(6, [
            A("'Similar solids: the radius AND the height' appears", T('Similar solids: every edge — the radius AND the height', size=40, gap=30)),
            A("'Only one changes: multiply the factors' appears", T('Radius $\\times n\\rightarrow$ volume $\\times n^2$ · height $\\times n\\rightarrow$ volume $\\times n$', size=38, gap=30)),
            "Only one dimension changes? It's not similar. Multiply the separate factors: radius times 3, height times 2 — volume times 18.",
            A("'A third of the height → 1/27' appears", T('Cone filled to a third of its height $\\rightarrow\\left(\\frac13\\right)^3=\\frac1{27}$', size=40)),
            "A cone filled to a third of its height holds only one twenty-seventh."]),
        S(7, [
            A("'Percent → factor → power → percent' appears", T('Percent $\\rightarrow$ factor $\\rightarrow$ power $\\rightarrow$ back to percent', size=40, gap=30)),
            "Percents: turn them into a factor first.",
            A("'−50%: area −75%, volume −87.5%' appears", T('Sides $-50\\%$: area $\\times0.25$ ($-75\\%$) · volume $\\times0.125$ ($-87.5\\%$)', size=38, gap=30)),
            A("'× 3 = +200%' appears", T('Volume $\\times3$ $=$ an increase of $200\\%$', size=40)),
            "And a factor is not a percent: times 3 is an increase of 200 percent."]),
        S(8, [
            A("'Scale 1 : n' appears", T('Scale $1:n$: lengths $\\times n$ · areas $\\times n^2$', size=44, gap=30)),
            "A map is a similar copy. Lengths times n, areas times n squared.",
            A("'One map cm first' appears", T('Change ONE map cm into the real unit first — then square for areas', size=38, gap=30)),
            A("'cm ÷ 100 → m ÷ 1000 → km' appears", T('cm $\\div100\\rightarrow$ m $\\div1000\\rightarrow$ km', size=42)),
            "Scale 1 to 30,000: one centimeter is 0.3 kilometers. One square centimeter — 0.09 square kilometers."]),
        S(9, [
            "Before you start, always ask yourself:",
            A('Check 1 appears', T('Similar or not? (same angles — or every length, one factor)', size=36, gap=24)),
            A('Check 2 appears', T('Length, area or volume? $k$, $k^2$ or $k^3$', size=36, gap=24)),
            A('Check 3 appears', T('What matches what? Opposite equal angles — the WHOLE side', size=36, gap=24)),
            A('Check 4 appears', T('Part or leftover — what exactly do they compare?', size=36, gap=24)),
            A('Check 5 appears', T('Percent or scale? Turn it into a factor first', size=36)),
            "And the traps: squaring shapes that aren't similar, the parallel segment against a part, and 20 percent times 3.",
            "Now it's your turn. Good luck!"]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == LEARN][-1]
    M.new_video('r26-t36-summary', TOPIC, 'Summary: Similarity', sb, slides, LEARN, after=last)


# ================================================================================================
# 2026-10-05 cut repeats: a lesson slide that the next question video teaches again is cut
# (see the CHANGES file). Runs LAST: the original apply() is wrapped below.
# ================================================================================================
def _cr_cut(M, vid, ns):
    """Remove slides ns (1-based) and keep the sidebar and every slide's 'active' consistent."""
    v = M.video(vid); sb = list(v.get('hybrid', {}).get('sidebar', [])); beats = v['beats']
    gone = {beats[n - 1].get('active', -1) for n in ns} - {-1}
    used = {b.get('active', -1) for k, b in enumerate(beats, 1) if k not in ns}
    gone -= used
    idx, new = {}, []
    for i, l in enumerate(sb):
        if i in gone: continue
        idx[i] = len(new); new.append(l)
    M.remove_slides(vid, ns)
    for b in v['beats']:
        if b.get('active', -1) >= 0: b['active'] = idx[b['active']]
    M.set_sidebar(vid, new)


def _cr_find(M, vid, n, part):
    ls = M.slide(vid, n)['lines']
    k = [i for i, l in enumerate(ls) if part in (l.get('say') or '')]
    assert len(k) == 1, (vid, n, part, k)
    return ls, k[0]


def _cr_say(M, vid, n, old, new):
    ls, k = _cr_find(M, vid, n, old)
    ls[k]['say'] = ls[k]['say'].replace(old, new); M.touched_videos.add(vid)


def _cr_drop_say(M, vid, n, part):
    ls, k = _cr_find(M, vid, n, part)
    ls.pop(k); M.touched_videos.add(vid)


def _cr_drop_item(M, vid, n, k):
    """Remove board item k of a slide, its 'appears' cue, and renumber the later cues."""
    b = M.slide(vid, n); b['items'].pop(k)
    b['lines'] = [l for l in b['lines'] if l.get('appear') != k]
    for l in b['lines']:
        if l.get('appear') is not None and l['appear'] > k: l['appear'] -= 1
    M.touched_videos.add(vid)


def _cr_add(M, vid, n, part, say, item, label, before=False, at=None):
    """Add one spoken line with its board item, right after (or before) the line containing `part`.
    at = position of the item in the slide's item list (default: last)."""
    b = M.slide(vid, n)
    at = len(b['items']) if at is None else at
    for l in b['lines']:
        if l.get('appear') is not None and l['appear'] >= at: l['appear'] += 1
    b['items'].insert(at, item)
    ls, k = _cr_find(M, vid, n, part)
    k = k if before else k + 1
    ls[k:k] = [{'appear': at, 'label': label}, {'say': say}]
    M.touched_videos.add(vid)


def cut_repeats(M):
    # --- "Similar Triangles and Rectangles": slide 11 (same height: no squaring) is taught again in
    #     solve-q-r26-t36-01, slide 12 (trapezoid diagonals: a², ab, ab, b²) in solve-q-r26-t36-02.
    #     Neither is in the Hebrew lesson. The recap line about "same height" goes with them.
    L = 'geo-139'
    _cr_cut(M, L, [11, 12])
    rec = len(M.video(L)['beats'])
    _cr_drop_item(M, L, rec, 4)
    _cr_drop_say(M, L, rec, 'Same height but not similar')
    for it, y in zip(M.slide(L, rec)['items'][4:], (570, 650)): it['y'] = y

    # --- "Volume Changes": slide 8 (percent change: factor, power, back to percent) is taught again in
    #     solve-q-r26-t36-03. Its "backwards" step (area +44% -> sides +20%) moves into that video.
    V = 'geo-143'
    _cr_cut(M, V, [8])
    rec = len(M.video(V)['beats'])
    _cr_drop_item(M, V, rec, 3)
    _cr_drop_say(M, V, rec, 'And with percents: a factor first')
    _cr_add(M, 'solve-q-r26-t36-03', 3, '44 percent is the AREA of a face',
            "And backwards: the area grew by 44 percent? That's times 1.44. The square root is 1.2 — so the sides grew by 20 percent.",
            T(r'Backwards: area $\times1.44$ $\rightarrow$ sides $\times\sqrt{1.44}=1.2$', size=34, x=410, y=190, w=1140),
            "'Backwards: area × 1.44 → sides × 1.2' appears")

    # --- "Map Scale": slides 3-5 (units ladder, a length example, an area example) are taught again, step by
    #     step, in solve-q-r26-t36-04 (length, the ladder) and solve-q-r26-t36-05 (area: one map cm first, then
    #     square). The recap goes too. Kept: the short intro and what a scale 1 : n means.
    S = 'r26-t36-map-scale'
    _cr_cut(M, S, [3, 4, 5, 6])
    _cr_say(M, S, 2, 'And real areas — n squared times the map areas.',
            "And real areas — n squared times the map areas. Let's see it in the questions.")


_apply_before_cut = apply


def apply(M):
    _apply_before_cut(M)
    cut_repeats(M)


# ================================================================================================
# 2026-10-06 renumber pass (runs LAST). The English course must not look like the Hebrew one: every Hebrew-derived
# question (guided geo36-g136 ... g151, practice geo36-core-p01 ... p20) gets new numbers (and a slightly changed
# story where there is one). Idea, trap, level and methods stay. Every changed figure is redrawn, every guided solution
# video is rewritten to match. Lesson examples that used the Hebrew lesson's own numbers get new numbers.
# Practice clean-up 41 -> 27. Nothing in topic 36 is recorded (checked ~/Documents/Course.recordings 2026-10-06).
# ================================================================================================
import math as _m
RN_RECORDED = set()


def _rn_sub(M, vid, n, pairs):
    """Exact substring replacements in one slide's spoken / drawn lines, cue labels and board items (each must hit)."""
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


def _rn_q(M, qid, stem=None, choices=None, correct=None, expl=None, figure=None, vb=None):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)
    if figure is not None: _rn_fig(M, qid, figure, vb)


def _rn_fig(M, qid, svg, vb=None):
    """New question figure; its copies on solution slides get the same drawing (cropped to vb or to their old crop)."""
    M.set_q(qid, figure=svg)
    for vid, v in M.D['videos'].items():
        for b in v.get('beats', []):
            for it in b.get('items', []):
                if it.get('k') == 'q' and it.get('qid') == qid and isinstance(it.get('fig'), dict):
                    old = re.search(r'viewBox="([^"]*)"', it['fig']['svg']).group(1)
                    it['fig']['svg'] = _crop(svg, vb or old); M.touched_videos.add(vid)


def _relabel(svg, mp):
    """Change the text of figure labels (exact <text> contents, all at once)."""
    for old in mp:
        assert re.search('>%s</text>' % re.escape(old), svg), old
    return re.sub(r'>([^<]+)</text>', lambda mo: '>%s</text>' % mp.get(mo.group(1), mo.group(1)), svg)


def _circ(c, r, fill='none', stroke=INK, w=2.5):
    return '<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s" stroke="%s" stroke-width="%s"/>' % (c[0], c[1], r, fill, stroke, w)


# --- redrawn figures ---------------------------------------------------------------------------------
def rn_regular(n, label):
    R, L = 107.353, 123.456
    pts, labs = [], ''
    for k in range(n):
        th = _m.radians(-90 - 360. * k / n)
        pts.append((320 + R * _m.cos(th), 180 + R * _m.sin(th)))
        labs += _t(320 + L * _m.cos(th), 180 + L * _m.sin(th), 'ABCDEFGHIJ'[k])
    return _svg(label, _poly(pts) + labs)


def rn_fig_g137():
    R, n = 127.75, 6; r = R / n
    b = _circ((320, 180), R) + _line((320 - R, 180), (320 + R, 180), ORANGE, 2.5, dash=True)
    for k in range(n): b += _circ((320 - R + r + 2 * r * k, 180), r, 'none', TEAL, 4)
    b += _t(320 - R - 18, 180, 'A') + _t(320 + R + 18, 180, 'B')
    return _svg('Six equal small circles whose diameters cover the diameter AB of a larger circle', b)


def rn_fig_g138():
    R = 109.5; r = R / 4
    b = _circ((320, 180), R) + _circ((320 - R + r, 180), r, FILL, TEAL) + _line((320 - R, 180), (320 + R, 180), ORANGE, 2.5, dash=True)
    b += _t(320 - R - 18, 180, 'A') + _t(320 + R + 18, 180, 'B') + _t(320 - R + 2 * r + 10, 198, 'C')
    return _svg('A small disk whose diameter AC is one quarter of the larger diameter AB', b)


def rn_fig_g142():
    return _svg('A large cube-shaped box and a small cubic block, each with one face shaded',
                # 2026-10-06 review: block edge = box edge / 6 (165 / 6 = 27.5), matching the 1 : 6 edge ratio
                _cube(150, 257.5, 27.5) + _cube(300, 120, 165) + _t(164, 312, 'block') + _t(382, 312, 'box'))


def rn_fig_g144():
    A_, B_, C_ = (267.535, 51.488), (424.929, 308.512), (215.071, 308.512)
    Dp, Ep = _lerp(C_, B_, 0.6), _lerp(C_, A_, 0.6)
    b = _poly([A_, B_, C_]) + _line(Ep, Dp, TEAL, 3)
    b += _t(A_[0], A_[1] - 20, 'A') + _t(B_[0] + 18, B_[1] + 17, 'B') + _t(C_[0] - 18, C_[1] + 17, 'C')
    b += _t(Dp[0], Dp[1] + 20, 'D') + _t(Ep[0] - 20, Ep[1], 'E')
    m = _lerp(A_, Ep, 0.5); b += _t(m[0] - 22, m[1], '4')
    b += _t((C_[0] + Dp[0]) / 2, 343.5, '15') + _t((Dp[0] + B_[0]) / 2, 343.5, '10')
    return _svg('A segment ED parallel to AB inside triangle ABC', b)


def rn_fig_g146():
    B_, C_ = (91.875, 289.5), (548.125, 289.5)
    u = (C_[0] - B_[0]) / 30.
    Dp = (B_[0] + 3 * u, 289.5); A_ = (Dp[0], 289.5 - 9 * u)
    b = _poly([A_, B_, C_]) + _line(A_, Dp, TEAL) + _right(Dp, A_, C_, 11) + _right(A_, B_, C_, 12)
    b += _t(A_[0], A_[1] - 20, 'A') + _t(B_[0] - 18, 305.5, 'B') + _t(C_[0] + 18, 305.5, 'C') + _t(Dp[0] + 4, 309.5, 'D')
    b += _t((B_[0] + Dp[0]) / 2 - 6, 326, '3') + _t((Dp[0] + C_[0]) / 2, 324.5, '27')
    return _svg('An altitude divides the hypotenuse of a right triangle into lengths 3 and 27', b)


def rn_fig_g147():
    R = 127.75; r = R / 1.3
    b = _circ((320, 180), R, FILL) + _circ((320, 180), r, 'white')
    b += _line((320, 180), (320, 180 + r), TEAL) + _line((320, 180), (320 + R, 180), ORANGE) + _dot((320, 180))
    b += _t(304, 180 + r / 2, 'r') + _t(320 + R / 2 + 8, 164, '1.3r')
    return _svg('Concentric circles with radii r and 1.3r', b)


def rn_fig_g150():
    R = 109.5; r = R / 4
    b = _circ((320, 180), R, BLUE) + _circ((372, 180), r, FILL, TEAL) + _line((320 - R, 180), (320 + R, 180), ORANGE, 2.5, dash=True)
    b += _t(320, 99.7, 'Glass globe') + _t(372, 140, 'Ball', size=16)
    return _svg('A small ball inside a larger glass globe, shown in cross section', b)


def rn_fig_p02():
    A_, F_ = (174.0, 70.5), (466.0, 70.5); G_ = (466.0, 289.5)
    Dp = _lerp(A_, F_, 0.6); H_ = _lerp(A_, G_, 0.6)
    b = _poly([A_, F_, G_]) + _line(Dp, H_, TEAL) + _right(Dp, A_, H_, 11) + _right(F_, A_, G_, 11)
    b += _t(160, 54.5, 'A')
    for k, s in enumerate('BCDE', 1): b += _t(174 + 292 * k / 5., 52.5, s)
    b += _t(482, 54.5, 'F') + _t(482, 304.5, 'G') + _t(Dp[0] - 15, H_[1] + 12, 'H')
    return _svg('Equal gaps on one line and two perpendicular segments to a ray from A', b)


def rn_fig_p07():
    R = 116.8; r = 0.6 * R; A_ = (320, 180 + R); Oc = (320, 180 + R - r); B_ = (320, 180 + R - 2 * r)
    b = _circ((320, 180), R) + _circ(Oc, r, FILL, TEAL) + _line(A_, B_, ORANGE) + _dot((320, 180))
    b += _t(338, 180, 'O') + _t(320, A_[1] + 22, 'A') + _t(320, B_[1] - 20, 'B')
    return _svg('An internally tangent circle whose diameter AB passes through the center O of the larger circle', b)


def _sector(apex, R, th, fill):
    p = (apex[0] + R, apex[1]); q = (apex[0] + R * _m.cos(_m.radians(th)), apex[1] - R * _m.sin(_m.radians(th)))
    s = '<path d="M %.3f %.3f L %.3f %.3f A %.3f %.3f 0 0 0 %.3f %.3f Z" fill="%s" stroke="%s" stroke-width="2.2"/>' % (
        apex[0], apex[1], p[0], p[1], R, R, q[0], q[1], fill, TEAL)
    a = 0.2 * R if R > 100 else 0.42 * R
    a = max(a, 22)
    p2 = (apex[0] + a, apex[1]); q2 = (apex[0] + a * _m.cos(_m.radians(th)), apex[1] - a * _m.sin(_m.radians(th)))
    s += '<path d="M %.3f %.3f A %.3f %.3f 0 0 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="2"/>' % (p2[0], p2[1], a, a, q2[0], q2[1], TEAL)
    lab = (apex[0] + (a + 14) * _m.cos(_m.radians(th / 2)), apex[1] - (a + 14) * _m.sin(_m.radians(th / 2)))
    return s + _t(lab[0], lab[1], 'θ', size=18, color=TEAL)


def rn_fig_p08():
    return _svg('Two circular sectors with the same central angle and different radii',
                _sector((150, 277.333), 165, 110, FILL) + _sector((450, 277.333), 66, 110, BLUE))


def rn_fig_p09():
    u, H = 28.0, 269.244 / 5     # bases 2u and 3u, heights 2H and 3H
    top, E_ = 45.378, 45.378 + 2 * H; bot = E_ + 3 * H
    A_, B_ = (320 - u, top), (320 + u, top); D_, C_ = (320 - 1.5 * u, bot), (320 + 1.5 * u, bot)
    b = _poly([A_, B_, (320, E_)], FILL, TEAL) + _poly([C_, D_, (320, E_)])
    b += _t(A_[0] - 17, top - 15, 'A') + _t(B_[0] + 17, top - 15, 'B') + _t(338, E_, 'E')
    b += _t(C_[0] + 17, bot + 16, 'C') + _t(D_[0] - 17, bot + 16, 'D') + _t(320, top - 28, '2') + _t(320, bot + 29, '3')
    b += _t(268, (top + E_) / 2, 'x − 1') + _t(374, (E_ + bot) / 2, 'x + 3')
    return _svg('An hourglass arrangement with bases 2 and 3', b)


def rn_fig_p11():
    C_ = (320, 125.5)
    b = _poly([(270, 75.5), (370, 75.5), C_], FILL, TEAL) + _poly([C_, (170, 275.5), (470, 275.5)])
    b += _t(254, 60.5, 'A') + _t(386, 60.5, 'B') + _t(337, 125.5, 'C') + _t(154, 291.5, 'D') + _t(486, 291.5, 'E')
    return _svg('Similar hourglass triangles ABC and EDC', b)


def rn_fig_p14():
    s = 7.2
    A_ = (250.0, 40 + 20 * s); E_ = (250.0, 40.0); B_ = (250 + 8 * s, A_[1]); C_ = (B_[0], A_[1] + 15 * s); D_ = (C_[0] + 6 * s, C_[1])
    b = _poly([E_, A_, B_]) + _poly([B_, C_, D_]) + _right(A_, E_, B_, 9.4) + _right(B_, A_, C_, 9.4) + _right(C_, B_, D_, 9.4)
    b += _t(A_[0] - 16, A_[1] + 16, 'A') + _t(B_[0] + 16, B_[1] - 12, 'B') + _t(C_[0] - 15, C_[1] + 17, 'C')
    b += _t(D_[0] + 16, D_[1] + 16, 'D') + _t(E_[0] - 14, E_[1] - 12, 'E')
    b += _t((A_[0] + B_[0]) / 2, A_[1] + 22, '8') + _t(B_[0] - 18, (B_[1] + C_[1]) / 2, '15') + _t((C_[0] + D_[0]) / 2, C_[1] + 26, '6')
    return _svg('Two right triangles along one straight line through E, B and D', b)


def rn_fig_p16():
    Vy, by, R, ry = 60.545, 299.455, 79.636, 22.298
    f = 0.75; cy = Vy + f * (by - Vy)
    b = _poly([(240.364, by), (399.636, by), (320, Vy)], FILL, 'none', 0)
    b += '<path d="M 240.364 %.3f A %.3f %.3f 0 0 1 399.636 %.3f" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 5"/>' % (by, R, ry, by, GREY)
    b += '<path d="M 240.364 %.3f A %.3f %.3f 0 0 0 399.636 %.3f" fill="none" stroke="%s" stroke-width="2.5"/>' % (by, R, ry, by, INK)
    b += _line((240.364, by), (320, Vy)) + _line((320, Vy), (399.636, by)) + _ell(320, cy, f * R, f * ry, FILL, TEAL, 2)
    return _svg('A cone cut by a plane parallel to its base', b)


def rn_fig_p19():
    s = 12.0; CF = _m.sqrt(288) * s
    F_ = (380.0, 42 + 6 * s); A_ = (380.0, 42.0); G_ = (380.0, 42 + 4 * s); C_ = (F_[0] - CF, F_[1])
    B_ = (F_[0] - CF * 2 / 3., G_[1])
    b = _poly([C_, (C_[0], C_[1] + CF), (F_[0], F_[1] + CF), F_], FILL, TEAL)
    b += _poly([A_, G_, (G_[0] + 4 * s, G_[1]), (A_[0] + 4 * s, A_[1])]) + _poly([A_, F_, C_])
    b += _line(B_, G_, ORANGE) + _right(F_, A_, C_, 8.3)
    b += _t(A_[0] - 15, A_[1] - 14, 'A') + _t(F_[0] + 16, F_[1] - 12, 'F') + _t(C_[0] - 16, C_[1] + 4, 'C')
    b += _t(C_[0] - 15, C_[1] + CF + 15, 'D') + _t(F_[0] + 15, F_[1] + CF + 15, 'E') + _t(G_[0] - 16, G_[1] - 13, 'G')
    b += _t(G_[0] + 4 * s + 16, G_[1] + 6, 'H') + _t(A_[0] + 4 * s + 16, A_[1] - 6, 'J') + _t(B_[0] - 14, B_[1] - 14, 'B')
    b += _t(A_[0] + 2 * s, A_[1] - 16, '4')
    m1 = _lerp(A_, B_, 0.5); m2 = _lerp(B_, C_, 0.5)
    b += _t(m1[0] - 12, m1[1] - 14, '12') + _t(m2[0] - 14, m2[1] - 12, '6')
    return _svg('Squares AGHJ and CDEF in a right triangle ACF, with BG parallel to CF', b)


def rn_cubes(n):
    x0, yb, S, DX, DY = 195.431, 288.495, 160.734, 88.404, -56.256
    c, dx, dy = S / n, DX / n, DY / n; yt = yb - S
    b = ''
    for k in range(n):
        for i in range(n):
            p = (x0 + i * c + k * dx, yt + k * dy)
            b += _poly([p, (p[0] + c, p[1]), (p[0] + c + dx, p[1] + dy), (p[0] + dx, p[1] + dy)], BLUE, INK, 1.7)
    for k in range(n):
        for j in range(n):
            p = (x0 + S + k * dx, yb - j * c + k * dy)
            b += _poly([p, (p[0] + dx, p[1] + dy), (p[0] + dx, p[1] + dy - c), (p[0], p[1] - c)], FILL, INK, 1.7)
    for i in range(n):
        for j in range(n):
            p = (x0 + i * c, yb - j * c)
            b += _poly([p, (p[0] + c, p[1]), (p[0] + c, p[1] - c), (p[0], p[1] - c)], '#f8fbfd', INK, 1.7)
    return _svg('Four small cube edges in each direction give sixty-four equal cubes', b, vb='169.4 45.5 301.1 269.0')


def rn_guided(M):
    S = lambda g: 'solve-' + g
    # ---------- g136: octagon, side x4 -> 4 (Hebrew: pentagon x3)  ==>  decagon, side x5 -> 5
    g = 'geo36-g136'
    _rn_q(M, g, stem='The side length of a regular decagon is multiplied by $5$. By what factor is its perimeter multiplied?',
          choices=['$25$', '$5$', '$50$', '$10$'], correct=2, expl=[
              'A regular decagon with side $s$ has perimeter $P=10s$.',
              'With side $5s$: $P=10\\cdot5s=50s$, and $\\frac{50s}{10s}=5$.',
              'A perimeter is a length, so it changes like the side: $\\times5$. ($25$ would be the area factor.)'],
          figure=rn_regular(10, 'Regular 10-sided polygon'))
    _rn_sub(M, S(g), 2, [
        ('The side of a regular octagon is multiplied by 4.', 'The side of a regular decagon is multiplied by 5.'),
        ('Write s on a side of the octagon', 'Write s on a side of the decagon'),
        ("Let's picture a regular octagon with side s — and a second one whose side is 4 times bigger: 4s.",
         "Let's picture a regular decagon with side s — and a second one whose side is 5 times bigger: 5s."),
        ('The perimeter here: 8 sides — 8s.', 'The perimeter here: 10 sides — 10s.'),
        ('And there: 4s plus 4s plus … eight times — 32s.', 'And there: 5s plus 5s plus … ten times — 50s.'),
        ('32s against 8s — the perimeter is 4 times bigger.', '50s against 10s — the perimeter is 5 times bigger.'),
        ('$P=8s$', '$P=10s$'), ('P = 8s', 'P = 10s'),
        ('$P=8\\cdot4s=32s$', '$P=10\\cdot5s=50s$'), ('P = 8 · 4s = 32s', 'P = 10 · 5s = 50s')])
    _rn_sub(M, S(g), 3, [
        ('the side grew 4 times.', 'the side grew 5 times.'),
        ('so it grew 4 times as well. Linear ratio 1 to 4, the perimeter stays 1 to 4.',
         'so it grew 5 times as well. Linear ratio 1 to 5, the perimeter stays 1 to 5.'),
        ('16 would be the AREA', '25 would be the AREA'),
        ('Side $\\times4$ $\\rightarrow$ perimeter $\\times4$', 'Side $\\times5$ $\\rightarrow$ perimeter $\\times5$'),
        ('Side ×4 → perimeter ×4', 'Side ×5 → perimeter ×5'),
        ('Circle choice 3', 'Circle choice 2'), ('The answer, of course: 4. Choice three.', 'The answer, of course: 5. Choice two.')])

    # ---------- g137: radius 7, four circles -> 14pi (Hebrew: radius 5, three circles -> 10pi)  ==>  radius 9, six circles -> 18pi
    g = 'geo36-g137'
    _rn_q(M, g, stem='AB is a diameter of a circle with radius $9$ cm. Six congruent smaller circles have their centers on AB. Their diameters cover AB from end to end, as shown in the figure. What is the sum of the circumferences of the six smaller circles (in cm)?',
          choices=['$36\\pi$', '$108\\pi$', '$9\\pi$', '$18\\pi$'], correct=4, expl=[
              'Each small diameter is $\\frac16$ of AB, so the ratio of the lengths is $1:6$. A circumference is a length, so each small circumference is $\\frac16$ of the large one.',
              'Six small circumferences add up to the large circumference: $2\\pi\\cdot9=18\\pi$.',
              'Check: $AB=18$, the small radius is $\\frac{18}{12}=\\frac32$, and $6\\cdot2\\pi\\cdot\\frac32=18\\pi$.'],
          figure=rn_fig_g137())
    _rn_sub(M, S(g), 2, [
        ('AB is a diameter of a circle with radius 7. Four identical small circles sit on AB',
         'AB is a diameter of a circle with radius 9. Six identical small circles sit on AB'),
        ("What's the sum of the circumferences of the four small circles?", "What's the sum of the circumferences of the six small circles?"),
        ('Honestly, it bugs me that the radius is 7.', 'Honestly, it bugs me that the radius is 9.'),
        ("From A to B is 14. For one small circle's radius — 14 over 8, 7 quarters.",
         "From A to B is 18. For one small circle's radius — 18 over 12, 3 halves."),
        ('with r equals 7 quarters', 'with r equals 3 halves'),
        ('Small radius $=\\frac{14}{8}=\\frac74$', 'Small radius $=\\frac{18}{12}=\\frac32$'),
        ('Small radius = 14 : 8 = 7/4', 'Small radius = 18/12 = 3/2')])
    _rn_sub(M, S(g), 3, [
        ('Write r on a small radius and 4r on the big radius', 'Write r on a small radius and 6r on the big radius'),
        ('Small radius r. The big radius — four small diameters — 4r.', 'Small radius r. The big radius — three small diameters — 6r.'),
        ('Linear ratio 1 to 4. Circumference is a line — so the circumferences are 1 to 4 too.',
         'Linear ratio 1 to 6. Circumference is a line — so the circumferences are 1 to 6 too.'),
        ('exactly a quarter of the big one.', 'exactly a sixth of the big one.'),
        ('And four of them together?', 'And six of them together?'),
        ('Linear $1:4$ $\\rightarrow$ circumference $1:4$', 'Linear $1:6$ $\\rightarrow$ circumference $1:6$'),
        ('Linear ratio 1 : 4 → circumference 1 : 4', 'Linear ratio 1 : 6 → circumference 1 : 6'),
        ('4 small circumferences', '6 small circumferences')])
    _rn_sub(M, S(g), 4, [
        ('2π r: 2π times 7 — 14π.', '2π r: 2π times 9 — 18π.'),
        ('Choice three. See how easy that was with similarity — instead of radius 7 quarters',
         'Choice four. See how easy that was with similarity — instead of radius 3 halves'),
        ('The four small disks together cover just a quarter of the big AREA.',
         'The six small disks together cover just a sixth of the big AREA.'),
        ('$C=2\\pi\\cdot7=14\\pi$', '$C=2\\pi\\cdot9=18\\pi$'), ('C = 2π · 7 = 14π', 'C = 2π · 9 = 18π'),
        ('Circle choice 3', 'Circle choice 4')])

    # ---------- g138: AC = AB/3 -> 1:8 (Hebrew: 1:2 -> 1:3)  ==>  AC = AB/4 -> 1:15
    g = 'geo36-g138'
    _rn_q(M, g, stem='AB is a diameter of a circle. Point C lies on AB, and $AC=\\frac14AB$. A smaller circle has diameter AC. What is the ratio of the area of the smaller disk to the area inside the larger circle but outside the smaller circle?',
          choices=['$1:16$', '$1:15$', '$1:4$', '$4:15$'], correct=2, expl=[
              'The ratio of the diameters is $AC:AB=1:4$, so the ratio of the disk areas is $1^2:4^2=1:16$.',
              'Say the small disk is $1$ unit. Then the whole large disk is $16$ units, and the region outside the small disk is $16-1=15$ units.',
              'The requested ratio is $1:15$. ($1:16$ is the trap — it compares the small disk with the whole large disk.)'],
          figure=rn_fig_g138())
    _rn_sub(M, S(g), 2, [
        ('with AC a third of AB.', 'with AC a quarter of AB.'),
        ('the small diameter AC is a third of the big diameter AB.', 'the small diameter AC is a quarter of the big diameter AB.'),
        ('Linear ratio 1 to 3. The area ratio — squared — 1 to 9.', 'Linear ratio 1 to 4. The area ratio — squared — 1 to 16.'),
        ('Linear $1:3$ $\\rightarrow$ area $1:9$', 'Linear $1:4$ $\\rightarrow$ area $1:16$'),
        ('Linear 1 : 3 → area 1 : 9', 'Linear 1 : 4 → area 1 : 16')])
    _rn_sub(M, S(g), 3, [
        ('Like here: 1 to 9 is choice 2.', 'Like here: 1 to 16 is choice 1.'),
        ('Write 1 in the small disk and 9 next to the big circle', 'Write 1 in the small disk and 16 next to the big circle'),
        ('The big disk is 9.', 'The big disk is 16.'), ('9 minus 1 — 8.', '16 minus 1 — 15.'),
        ('Small disk to leftover: 1 to 8.', 'Small disk to leftover: 1 to 15.'),
        ('Leftover $=9-1=8$', 'Leftover $=16-1=15$'), ('Leftover = 9 − 1 = 8', 'Leftover = 16 − 1 = 15'),
        ('$1:8$', '$1:15$'), ('1 : 8', '1 : 15'),
        ('Circle choice 4', 'Circle choice 2'), ('Choice four.', 'Choice two.')])
    _rn_sub(M, S(g), 4, [
        ('Small radius 1, big radius 3. Areas π and 9π. Leftover 8π. π to 8π — 1 to 8.',
         'Small radius 1, big radius 4. Areas π and 16π. Leftover 15π. π to 15π — 1 to 15.'),
        ('$r=1,\\ R=3$: $\\pi:(9\\pi-\\pi)=1:8$', '$r=1,\\ R=4$: $\\pi:(16\\pi-\\pi)=1:15$'),
        ('r = 1, R = 3: π : (9π − π) = 1 : 8', 'r = 1, R = 4: π : (16π − π) = 1 : 15')])

    # ---------- g140: AD 3, DB 2 -> 9:16 (Hebrew: 2, 1 -> 4:5)  ==>  AD 4, DB 3 -> 16:33
    g = 'geo36-g140'
    _rn_q(M, g, stem='In triangle ABC, point D lies on AB and point E lies on AC, and $DE\\parallel BC$.\nGiven:\n$\\begin{cases} AD=4\\text{ cm} \\\\ DB=3\\text{ cm} \\end{cases}$\nWhat is the ratio of the area of triangle ADE to the area of trapezoid DBCE?',
          choices=['$16:49$', '$4:3$', '$16:33$', '$4:7$'], correct=3, expl=[
              '$DE\\parallel BC$, so triangles ADE and ABC are similar. AD matches the WHOLE side AB: $AB=4+3=7$.',
              'The ratio of the lengths is $4:7$, so the ratio of the areas is $4^2:7^2=16:49$.',
              'The trapezoid is the whole triangle minus the small one: $49-16=33$ units. The requested ratio is $16:33$.'],
          figure=_parts_fig(4 / 7., '4', '3', label='In triangle ABC, a segment DE is parallel to BC: AD = 4, DB = 3'),
          vb='70 10 500 330')
    _rn_sub(M, S(g), 2, [
        ('AD is 3, DB is 2.', 'AD is 4, DB is 3.'), ('the length ratio is NOT 3 to 2.', 'the length ratio is NOT 4 to 3.'),
        ('That 2, DB,', 'That 3, DB,'), ('Cross out choice 1', 'Cross out choice 2'),
        ('AD is 3. AB is 3 plus 2 — 5.', 'AD is 4. AB is 4 plus 3 — 7.'),
        ('is 3 to 5 — to the WHOLE AB.', 'is 4 to 7 — to the WHOLE AB.'),
        ('$AB=3+2=5$', '$AB=4+3=7$'), ('AB = 3 + 2 = 5', 'AB = 4 + 3 = 7'),
        ('Length ratio $3:5$', 'Length ratio $4:7$'), ('Length ratio 3 : 5', 'Length ratio 4 : 7')])
    _rn_sub(M, S(g), 3, [
        ('Length ratio 3 to 5 — area ratio squared: 9 to 25.', 'Length ratio 4 to 7 — area ratio squared: 16 to 49.'),
        ('Write 9 in the small triangle and 25 beside the whole triangle', 'Write 16 in the small triangle and 49 beside the whole triangle'),
        ('Say the small triangle is 9. The whole big triangle is 25.', 'Say the small triangle is 16. The whole big triangle is 49.'),
        ("What's left is the trapezoid: 25 minus 9.", "What's left is the trapezoid: 49 minus 16."),
        ('16 — so that the big triangle really is 25.', '33 — so that the big triangle really is 49.'),
        ('Small triangle to trapezoid: 9 to 16.', 'Small triangle to trapezoid: 16 to 33.'),
        ('9 to 25 is a trap: that\'s small against the whole, not against the trapezoid. And 3 to 5 forgot to square.',
         '16 to 49 is a trap: that\'s small against the whole, not against the trapezoid. And 4 to 7 forgot to square.'),
        ('Area ratio $3^2:5^2=9:25$', 'Area ratio $4^2:7^2=16:49$'), ('Area ratio 9 : 25', 'Area ratio 16 : 49'),
        ('Trapezoid $=25-9=16$', 'Trapezoid $=49-16=33$'), ('Trapezoid = 25 − 9 = 16', 'Trapezoid = 49 − 16 = 33'),
        ('$9:16$', '$16:33$'), ('9 : 16', '16 : 33'),
        ('Circle choice 4', 'Circle choice 3'), ('Choice four.', 'Choice three.')])

    # ---------- g142: face area x16 -> 64 cubes (Hebrew: x9 -> 27)  ==>  box and blocks, x36 -> 216
    g = 'geo36-g142'
    _rn_q(M, g, stem='A large cube-shaped box is filled completely with small cubic blocks. The area of one face of the box is $36$ times the area of one face of a block. How many blocks fill the box?',
          choices=['$36$', '$216$', '$1296$', '$72$'], correct=2, expl=[
              'Cubes are similar. The ratio of the face areas is $1:36$, so the ratio of the edges is $1:\\sqrt{36}=1:6$.',
              'The ratio of the volumes is $1^3:6^3=1:216$. So $216$ blocks fill the box.',
              '($36$ is the area ratio, and $1296=36^2$ squares the area ratio.)'],
          figure=rn_fig_g142(), vb='110 20 470 320')
    _rn_sub(M, S(g), 2, [
        ('The area of one face of a big cube is 16 times the area of one face of a small cube.',
         'The area of one face of the box is 36 times the area of one face of a block.'),
        ('How many small cubes fill the big cube?', 'How many blocks fill the box?'),
        ('First: cubes are similar shapes.', 'First: the box and the blocks are cubes — similar shapes.'),
        ('The area ratio is 1 to 16.', 'The area ratio is 1 to 36.'),
        ('The edges: 1 to 4.', 'The edges: 1 to 6.'),
        ('Areas $1:16$', 'Areas $1:36$'), ('Areas 1 : 16', 'Areas 1 : 36'),
        ('Edges $1:\\sqrt{16}=1:4$', 'Edges $1:\\sqrt{36}=1:6$'), ('Edges 1 : 4 (square root)', 'Edges 1 : 6 (square root)')])
    _rn_sub(M, S(g), 3, [
        ('Now that I have the length ratio, 1 to 4', 'Now that I have the length ratio, 1 to 6'),
        ('1 to 4 cubed: 1 to 64.', '1 to 6 cubed: 1 to 216.'),
        ('Sketch 4 × 4 in one layer, × 4 layers', 'Sketch 6 × 6 in one layer, × 6 layers'),
        ('You can see it: a layer of 4 by 4 — 16 — and 4 layers. 64.', 'You can see it: a layer of 6 by 6 — 36 — and 6 layers. 216.'),
        ("So if the small cube's volume is 1, the big cube's volume is 64. 64 small cubes fit in.",
         "So if a block's volume is 1, the box's volume is 216. 216 blocks fit in."),
        ('16 is the area ratio — not the volume. 256 is sixteen squared — someone squared the area ratio instead of going back to the edge.',
         '36 is the area ratio — not the volume. 1296 is thirty-six squared — someone squared the area ratio instead of going back to the edge.'),
        ('Volumes $1^3:4^3=1:64$', 'Volumes $1^3:6^3=1:216$'), ('Volumes 1 : 64', 'Volumes 1 : 216'),
        ('Circle choice 3', 'Circle choice 2'), ('Choice three.', 'Choice two.')])

    # ---------- g144: BD 4, DC 8, AE 5 -> 15 (Hebrew: BD 2, DC 6, AE 3 -> 12)  ==>  BD 10, DC 15, AE 4 -> 10
    g = 'geo36-g144'
    _rn_q(M, g, stem='In triangle ABC, point D lies on BC and point E lies on AC, and $ED\\parallel AB$.\nGiven:\n$\\begin{cases} BD=10\\text{ cm} \\\\ DC=15\\text{ cm} \\\\ AE=4\\text{ cm} \\end{cases}$\nWhat is the length of AC (in cm)?',
          choices=['$6$', '$25$', '$10$', '$\\frac{20}3$'], correct=3, expl=[
              '$ED\\parallel AB$, so triangles EDC and ABC are similar (corresponding angles, and the angle at C is shared).',
              'DC matches the whole side BC: $BC=10+15=25$. The ratio of the lengths is $\\frac{DC}{BC}=\\frac{15}{25}=\\frac35$.',
              'EC matches the whole side AC. Let $EC=x$: $\\frac{x}{x+4}=\\frac35$, so $5x=3x+12$ and $x=6$. Then $AC=6+4=10$.',
              'Faster (part to part): the parallel line cuts both sides in the same ratio. $BD:DC=10:15=2:3$, so $AE:EC=2:3$ too: $EC=\\frac32\\cdot4=6$ and $AC=10$.'],
          figure=rn_fig_g144())
    _rn_sub(M, S(g), 2, [('BD is 4, DC is 8, AE is 5.', 'BD is 10, DC is 15, AE is 4.')])
    _rn_sub(M, S(g), 3, [
        ('Write 12 under BC', 'Write 25 under BC'),
        ('Opposite alpha in the small triangle: DC — 8. Opposite alpha in the big one: the whole side BC — 4 plus 8, 12.',
         'Opposite alpha in the small triangle: DC — 15. Opposite alpha in the big one: the whole side BC — 10 plus 15, 25.'),
        ("That's x plus 5.", "That's x plus 4."),
        ('8 over 12 equals x over x plus 5.', '15 over 25 equals x over x plus 4.'),
        ('Cross-multiply. 12x equals 8x plus 40.', 'Cross-multiply. 25x equals 15x plus 60.'),
        ('4x is 40, x is 10.', '10x is 60, x is 6.'),
        ('They asked for AC: 10 plus 5 — 15.', 'They asked for AC: 6 plus 4 — 10.'),
        ('$\\frac{8}{12}=\\frac{x}{x+5}$', '$\\frac{15}{25}=\\frac{x}{x+4}$'), ('8/12 = x/(x+5) appears', '15/25 = x/(x+4) appears'),
        ('$12x=8x+40$', '$25x=15x+60$'), ('12x = 8x + 40 → x = 10 appears', '25x = 15x + 60 → x = 6 appears'),
        ('$x=10\\ \\Rightarrow\\ AC=15$', '$x=6\\ \\Rightarrow\\ AC=10$'), ('x = 10 → AC = 15 appears', 'x = 6 → AC = 10 appears'),
        ('Circle choice 1', 'Circle choice 3'), ('Choice one.', 'Choice three.')])
    _rn_sub(M, S(g), 4, [
        ('the ratio between the sides is 8 to x. In the big one: 12 to x plus 5.',
         'the ratio between the sides is 15 to x. In the big one: 25 to x plus 4.'),
        ('swap the x and the 12 in the first equation', 'swap the x and the 25 in the first equation'),
        ('the same x equals 10.', 'the same x equals 6.'),
        ('$\\frac{8}{x}=\\frac{12}{x+5}$', '$\\frac{15}{x}=\\frac{25}{x+4}$'), ('8/x = 12/(x+5) appears', '15/x = 25/(x+4) appears')])
    _rn_sub(M, S(g), 5, [
        ('Write "ratio 1 : 2" between BD and DC', 'Write "ratio 2 : 3" between BD and DC'),
        ('Write "ratio 1 : 2" between AE and EC', 'Write "ratio 2 : 3" between AE and EC'),
        ('On side CB: BD is 4 and DC is 8 — the ratio 1 to 2.', 'On side CB: BD is 10 and DC is 15 — the ratio 2 to 3.'),
        ('AE to EC is also 1 to 2.', 'AE to EC is also 2 to 3.'),
        ('AE is 5 — so EC is 10, and all of AC is 15.', 'AE is 4 — 2 parts, so one part is 2. EC is 3 parts — 6, and all of AC is 10.'),
        ('$AE=5\\Rightarrow EC=10\\Rightarrow AC=15$', '$AE=4\\Rightarrow EC=6\\Rightarrow AC=10$'),
        ('AE = 5 → EC = 10 → AC = 15 appears', 'AE = 4 → EC = 6 → AC = 10 appears'),
        ('Circle choice 1', 'Circle choice 3'), ('Choice one.', 'Choice three.')])

    # ---------- g145: AF = 3 -> x^2/3, plug in 3 (Hebrew: AF = 2, plug in 2)  ==>  AF = 5 -> x^2/5, plug in 5
    g = 'geo36-g145'
    q = M.q(g)
    _rn_q(M, g, stem=q['stemRich'].replace('$AF=3$', '$AF=5$'),
          choices=['$5x$', '$x^2$', '$\\frac{x^2}{5}$', '$\\frac x5$'], correct=3, expl=[
              '$DF\\parallel BC$ and $DE\\parallel AC$, so triangles AFD and DEB have the same angles: they are similar.',
              'Sides opposite equal angles match: AF matches DE, and FD matches EB. $\\frac{AF}{DE}=\\frac{FD}{EB}$: $\\frac5x=\\frac{x}{BE}$.',
              '$BE=\\frac{x\\cdot x}{5}=\\frac{x^2}{5}$.',
              'Check by plugging in $x=5$: both small triangles are isosceles right triangles, so $BE=5$. Only $\\frac{x^2}5=\\frac{25}5=5$ fits.'],
          figure=_relabel(q['questionVisual']['svg'], {'3': '5'}))
    assert '$AF=5$' in M.q(g)['stemRich']
    _rn_sub(M, S(g), 2, [('AF is 3,', 'AF is 5,')])
    _rn_sub(M, S(g), 3, [
        ('AF — 3.', 'AF — 5.'), ('Plug in: 3 over x equals x over BE.', 'Plug in: 5 over x equals x over BE.'),
        ('x times x — x squared — divided by 3.', 'x times x — x squared — divided by 5.'),
        ('$\\frac{3}{x}=\\frac{x}{BE}$', '$\\frac{5}{x}=\\frac{x}{BE}$'), ('3/x = x/BE appears', '5/x = x/BE appears'),
        ('$BE=\\frac{x\\cdot x}{3}=\\frac{x^2}{3}$', '$BE=\\frac{x\\cdot x}{5}=\\frac{x^2}{5}$'), ('BE = x²/3 appears', 'BE = x²/5 appears'),
        ('Circle choice 1', 'Circle choice 3'), ('Choice one.', 'Choice three.')])
    _rn_sub(M, S(g), 4, [
        ('the legs of the top triangle are 3 and 1', 'the legs of the top triangle are 5 and 1'),
        ('Simplest: plug in 3 —', 'Simplest: plug in 5 —'),
        ("x equals 3: now the top triangle's legs are 3 and 3.", "x equals 5: now the top triangle's legs are 5 and 5."),
        ('Write 3 on all four sides of the square', 'Write 5 on all four sides of the square'),
        ('Write 3 on BE', 'Write 5 on BE'), ('So BE is 3 as well.', 'So BE is 5 as well.'),
        ('Now plug 3 into the answers. Which gives 3?', 'Now plug 5 into the answers. Which gives 5?'),
        ('x squared over 3 — 9 over 3, really 3. Stays. x over 3 — 1, out. 3x — 9, out. x squared — 9, out.',
         '5x — 25, out. x squared — 25, out. x squared over 5 — 25 over 5, really 5. Stays. x over 5 — 1, out.'),
        ('Cross out choices 2, 3 and 4', 'Cross out choices 1, 2 and 4'),
        ('$x=3\\ \\Rightarrow\\ BE=3$', '$x=5\\ \\Rightarrow\\ BE=5$'), ('x = 3 → BE = 3 appears', 'x = 5 → BE = 5 appears'),
        ("I'd plug in 3.", "I'd plug in 5."),
        ('Circle choice 1', 'Circle choice 3'), ('Choice one.', 'Choice three.')])

    # ---------- g146: BD 9, DC 16 -> 12 (Hebrew: 4, 9 -> 6)  ==>  BD 3, DC 27 -> 9
    g = 'geo36-g146'
    _rn_q(M, g, stem='ABC is a right triangle with the right angle at A. AD is perpendicular to BC.\nGiven:\n$\\begin{cases} BD=3\\text{ cm} \\\\ DC=27\\text{ cm} \\end{cases}$\nWhat is the length of AD (in cm)?',
          choices=['$15$', '$9$', '$3\\sqrt{10}$', '$6$'], correct=2, expl=[
              'Triangles ABD and CAD are similar: both have a right angle at D, and the angle BAD equals the angle C (each is $90°$ minus the angle B).',
              'Matching legs: $\\frac{AD}{BD}=\\frac{DC}{AD}$, so $AD^2=3\\cdot27=81$ and $AD=9$.',
              'Shortcut: the altitude to the hypotenuse squared equals the product of the two parts: $h^2=p\\cdot q$. ($3\\sqrt{10}$ is the leg AB: $AB^2=3\\cdot30=90$.)'],
          figure=rn_fig_g146())
    _rn_sub(M, S(g), 2, [
        ("BD is 9, DC is 16. What's AD?", "BD is 3, DC is 27. What's AD?"),
        ('BD is 9, so AD is 9… and so is DC?', 'BD is 3, so AD is 3… and so is DC?')])
    _rn_sub(M, S(g), 3, [
        ('We have two numbers: 9 and 16.', 'We have two numbers: 3 and 27.'),
        ('the long leg, DC, 16.', 'the long leg, DC, 27.'),
        ('Cross-multiply: AD squared is 144. Take the root: 12.', 'Cross-multiply: AD squared is 81. Take the root: 9.'),
        ('9 times 16 is 144. The altitude is 12 — in one line.', '3 times 27 is 81. The altitude is 9 — in one line.'),
        ('$\\frac{AD}{9}=\\frac{16}{AD}$', '$\\frac{AD}{3}=\\frac{27}{AD}$'), ('AD/9 = 16/AD appears', 'AD/3 = 27/AD appears'),
        ('$AD^2=144\\ \\Rightarrow\\ AD=12$', '$AD^2=81\\ \\Rightarrow\\ AD=9$'), ('AD² = 144 → AD = 12 appears', 'AD² = 81 → AD = 9 appears'),
        ('$h^2=p\\cdot q=9\\cdot16=144$', '$h^2=p\\cdot q=3\\cdot27=81$'), ("'h² = p · q = 9 · 16' appears", "'h² = p · q = 3 · 27' appears"),
        ('Circle choice 3', 'Circle choice 2'), ('Choice three.', 'Choice two.')])
    _rn_sub(M, S(g), 4, [
        ('they add up to 25 squared — 625.', 'they add up to 30 squared — 900.'),
        ('2h squared is 288 — h squared 144 — h is 12.', '2h squared is 162 — h squared 81 — h is 9.'),
        ('$AB^2=h^2+81$', '$AB^2=h^2+9$'), ('$AC^2=h^2+256$', '$AC^2=h^2+729$'),
        ('$2h^2+337=625$', '$2h^2+738=900$'), ('$h^2=144\\ \\Rightarrow\\ h=12$', '$h^2=81\\ \\Rightarrow\\ h=9$'),
        ('AB² = h² + 81, AC² = h² + 256 appears', 'AB² = h² + 9, AC² = h² + 729 appears'),
        ('sum = 25² appears', 'sum = 30² appears'), ('h = 12 appears', 'h = 9 appears'),
        ('Circle choice 3', 'Circle choice 2'), ('Choice three.', 'Choice two.')])

    # ---------- g147: 1.4r, Liam / Maya (Hebrew: 1.5r)  ==>  1.3r, Noah / Emma (still: the first one only)
    g = 'geo36-g147'
    _rn_q(M, g, stem='Two concentric circles have radii $r$ and $1.3r$. Noah claims that the outer circumference is $1.3$ times the inner circumference. Emma claims that the area of the ring between the circles is greater than the area of the inner disk. Who is correct?',
          choices=['Both Noah and Emma', 'Noah only', 'Neither Noah nor Emma', 'Emma only'], correct=2, expl=[
              'Circles are similar. The ratio of the radii is $1:1.3=10:13$.',
              'A circumference is a length, so the ratio of the circumferences is also $10:13$: the outer one is $1.3$ times the inner one. Noah is correct.',
              'The ratio of the areas is $10^2:13^2=100:169$. The ring is $169-100=69$ units, and the inner disk is $100$ units. $69<100$, so Emma is incorrect.',
              'Answer: Noah only.'],
          figure=rn_fig_g147())
    _rn_sub(M, S(g), 2, [
        ('Two concentric circles, radii r and 1.4r. Liam: the outer circumference is 1.4 times the inner. Maya: the ring is bigger than the inner disk.',
         'Two concentric circles, radii r and 1.3r. Noah: the outer circumference is 1.3 times the inner. Emma: the ring is bigger than the inner disk.'),
        ('We need to decide: Liam, Maya, both, or neither.', 'We need to decide: Noah, Emma, both, or neither.'),
        ('Outer radius 1.4r — times 2 pi: 2.8 pi r.', 'Outer radius 1.3r — times 2 pi: 2.6 pi r.'),
        ('2.8 is really 1.4 times 2. Liam is right.', '2.6 is really 1.3 times 2. Noah is right.'),
        ("'neither' and 'Maya only'", "'neither' and 'Emma only'"),
        ("Now it's either Liam only, or both of them.", "Now it's either Noah only, or both of them."),
        ('Cross out choices 2 and 4', 'Cross out choices 3 and 4'),
        ('$C_{\\text{out}}=2\\pi\\cdot1.4r=2.8\\pi r$', '$C_{\\text{out}}=2\\pi\\cdot1.3r=2.6\\pi r$'),
        ('C = 2π · 1.4r = 2.8πr appears', 'C = 2π · 1.3r = 2.6πr appears')])
    _rn_sub(M, S(g), 3, [
        ('Maya: the ring is bigger than the white disk.', 'Emma: the ring is bigger than the white disk.'),
        ('Big circle: pi times 1.4r squared.', 'Big circle: pi times 1.3r squared.'),
        ('1.4 squared is 1.96. Minus 1 — the ring is 0.96 pi r squared.', '1.3 squared is 1.69. Minus 1 — the ring is 0.69 pi r squared.'),
        ('So 0.96 is LESS than 1.', 'So 0.69 is LESS than 1.'),
        ("Careful — this is close! With 1.5 the ring would be bigger. With 1.4, it isn't. Maya is wrong.",
         "Careful — in the figure the ring looks big. With 1.6 the ring would be bigger. With 1.3, it isn't. Emma is wrong."),
        ('$\\pi(1.4r)^2-\\pi r^2$', '$\\pi(1.3r)^2-\\pi r^2$'), ('π(1.4r)² − πr² appears', 'π(1.3r)² − πr² appears'),
        ('$=1.96\\pi r^2-\\pi r^2=0.96\\pi r^2$', '$=1.69\\pi r^2-\\pi r^2=0.69\\pi r^2$'),
        ('= 1.96πr² − πr² = 0.96πr² appears', '= 1.69πr² − πr² = 0.69πr² appears'),
        ('With $1.5r$ the ring would win: $2.25-1=1.25$', 'With $1.6r$ the ring would win: $2.56-1=1.56$'),
        ('Hebrew note appears', "'With 1.6r the ring would win' appears"),
        ('Circle choice 3', 'Circle choice 2'), ('Choice three.', 'Choice two.')])
    _rn_sub(M, S(g), 4, [
        ('Liam: in similar shapes the length ratio is kept. Radius times 1.4 — circumference times 1.4. Nothing to calculate. Liam is right.',
         'Noah: in similar shapes the length ratio is kept. Radius times 1.3 — circumference times 1.3. Nothing to calculate. Noah is right.'),
        ('Maya: from a length ratio to an area ratio — square it.', 'Emma: from a length ratio to an area ratio — square it.'),
        ("1 to 1.4 isn't comfortable — we don't like decimals. Expand it: 5 to 7. Same ratio.",
         "1 to 1.3 isn't comfortable — we don't like decimals. Expand it: 10 to 13. Same ratio."),
        ('Square it: 25 to 49. The small disk — 25 units. The big one — 49 units.',
         'Square it: 100 to 169. The small disk — 100 units. The big one — 169 units.'),
        ('The ring: 49 minus 25 — 24 units. Less than 25. Maya is wrong.', 'The ring: 169 minus 100 — 69 units. Less than 100. Emma is wrong.'),
        ('$1:1.4=5:7$', '$1:1.3=10:13$'), ('1 : 1.4 = 5 : 7 appears', '1 : 1.3 = 10 : 13 appears'),
        ('$25:49$', '$100:169$'), ('25 : 49 appears', '100 : 169 appears'),
        ('Ring $=49-25=24<25$', 'Ring $=169-100=69<100$'), ('Ring = 49 − 25 = 24 < 25 appears', 'Ring = 169 − 100 = 69 < 100 appears'),
        ('Circle choice 3', 'Circle choice 2'), ('Choice three.', 'Choice two.')])

    # ---------- g148: trapezoid 15 -> 5 (Hebrew: 6 -> 2)  ==>  trapezoid 21 -> 7
    g = 'geo36-g148'
    _rn_q(M, g, stem='D and F are the midpoints of sides AB and AC of triangle ABC. The area of trapezoid DBCF is $21$ cm². What is the area of triangle ADF (in cm²)?',
          choices=['$10.5$', '$5.25$', '$14$', '$7$'], correct=4, expl=[
              'A segment that joins two midpoints is parallel to the third side, so triangle ADF is similar to triangle ABC. The ratio of the lengths is $AD:AB=1:2$.',
              'The ratio of the areas is $1^2:2^2=1:4$. Small triangle: $1$ unit. Whole triangle: $4$ units. Trapezoid: $4-1=3$ units.',
              '$3$ units $=21$, so $1$ unit $=21\\div3=7$. The area of triangle ADF is $7$. ($10.5$ halves the trapezoid, and $5.25$ takes a quarter of it.)'])
    _rn_sub(M, S(g), 2, [('The trapezoid DBCF has area 15.', 'The trapezoid DBCF has area 21.')])
    _rn_sub(M, S(g), 3, [
        ('equals 15.', 'equals 21.'),
        ('Times 2: 3yh is 30. Divide by 3: yh is 10.', 'Times 2: 3yh is 42. Divide by 3: yh is 14.'),
        ('10 over 2 is 5.', '14 over 2 is 7.'),
        ('$\\frac{(y+2y)h}{2}=15$', '$\\frac{(y+2y)h}{2}=21$'), ('(y + 2y)h/2 = 15 appears', '(y + 2y)h/2 = 21 appears'),
        ('$3yh=30\\Rightarrow yh=10$', '$3yh=42\\Rightarrow yh=14$'), ('3yh = 30 → yh = 10 appears', '3yh = 42 → yh = 14 appears'),
        ('$S_{ADF}=\\frac{yh}{2}=\\frac{10}{2}=5$', '$S_{ADF}=\\frac{yh}{2}=\\frac{14}{2}=7$'), ('S = yh/2 = 5 appears', 'S = yh/2 = 7 appears'),
        ('Circle choice 2', 'Circle choice 4'), ('Choice two.', 'Choice four.')])
    _rn_sub(M, S(g), 4, [
        ("3 units. And it's 15.", "3 units. And it's 21."),
        ('So one unit is 5 — and the small triangle is one unit. 5.', 'So one unit is 7 — and the small triangle is one unit. 7.'),
        ('Trapezoid $=4-1=3$ units $=15$', 'Trapezoid $=4-1=3$ units $=21$'),
        ('Trapezoid = 4 − 1 = 3 units = 15 appears', 'Trapezoid = 4 − 1 = 3 units = 21 appears'),
        ('$1$ unit $=5$', '$1$ unit $=7$'), ('1 unit = 5 appears', '1 unit = 7 appears'),
        ('Circle choice 2', 'Circle choice 4'), ('Choice two. Much shorter', 'Choice four. Much shorter')])
    _rn_sub(M, S(g), 5, [
        ('So each is 5 — and the top one too.', 'So each is 7 — and the top one too.'),
        ('Trapezoid $=3$ triangles: $15\\div3=5$', 'Trapezoid $=3$ triangles: $21\\div3=7$'),
        ('Trapezoid = 3 triangles → 15 : 3 = 5 appears', 'Trapezoid = 3 triangles → 21 ÷ 3 = 7 appears'),
        ('Circle choice 2', 'Circle choice 4'), ('Choice two.', 'Choice four.')])

    # ---------- g149: 72√3 and 24√3 -> √3:1 (Hebrew: 12√3 and 6√3 -> √2:1)  ==>  150√3 and 30√3 -> √5:1
    g = 'geo36-g149'
    _rn_q(M, g, stem='Two regular hexagons have areas $150\\sqrt3$ cm² and $30\\sqrt3$ cm². What is the ratio of the perimeter of the first hexagon to the perimeter of the second?',
          choices=['$\\sqrt5:1$', '$25:1$', '$5:1$', '$\\sqrt{10}:1$'], correct=1, expl=[
              'Regular hexagons are similar. The ratio of the areas is $150\\sqrt3:30\\sqrt3=5:1$.',
              'Go back from areas to lengths with a square root: the ratio of the sides is $\\sqrt5:1$.',
              'A perimeter is a length, so the ratio of the perimeters is also $\\sqrt5:1$. (Check: the sides are $10$ and $2\\sqrt5$, and $\\frac{10}{2\\sqrt5}=\\sqrt5$.)'])
    _rn_sub(M, S(g), 2, [
        ('areas 72 root 3 and 24 root 3.', 'areas 150 root 3 and 30 root 3.'),
        ('times 6, equals 72 root 3.', 'times 6, equals 150 root 3.'),
        ('a squared over 4 is 12 — a squared is 48. a is root 48 — 4 root 3.', 'a squared over 4 is 25 — a squared is 100. a is 10.'),
        ('b squared over 4 is 4, b squared is 16, b is 4.', 'b squared over 4 is 5, b squared is 20, b is root 20 — 2 root 5.'),
        ('$6\\cdot\\frac{a^2\\sqrt3}{4}=72\\sqrt3$', '$6\\cdot\\frac{a^2\\sqrt3}{4}=150\\sqrt3$'),
        ('6 · a²√3/4 = 72√3 appears', '6 · a²√3/4 = 150√3 appears'),
        ('$a^2=48\\Rightarrow a=4\\sqrt3$', '$a^2=100\\Rightarrow a=10$'), ('a² = 48 → a = 4√3 appears', 'a² = 100 → a = 10 appears'),
        ('$6\\cdot\\frac{b^2\\sqrt3}{4}=24\\sqrt3\\Rightarrow b=4$', '$6\\cdot\\frac{b^2\\sqrt3}{4}=30\\sqrt3\\Rightarrow b=2\\sqrt5$'),
        ('b² = 16 → b = 4 appears', 'b² = 20 → b = 2√5 appears')])
    _rn_sub(M, S(g), 3, [
        ('First perimeter: 6 times 4 root 3. Second: 6 times 4.', 'First perimeter: 6 times 10. Second: 6 times 2 root 5.'),
        ('The 6s cancel, the 4s cancel — root 3 to 1.',
         'The 6s cancel: 10 to 2 root 5. Divide by 2: 5 to root 5. And 5 is root 5 times root 5 — so root 5 to 1.'),
        ('$6\\cdot4\\sqrt3\\ :\\ 6\\cdot4$', '$6\\cdot10\\ :\\ 6\\cdot2\\sqrt5$'), ('6 · 4√3 : 6 · 4 appears', '6 · 10 : 6 · 2√5 appears'),
        ('$=\\sqrt3:1$', '$=5:\\sqrt5=\\sqrt5:1$'), ('= √3 : 1 appears', '= √5 : 1 appears'),
        ('Circle choice 4', 'Circle choice 1'), ('Choice four.', 'Choice one.')])
    _rn_sub(M, S(g), 4, [
        ('72 root 3 is three times 24 root 3. Area ratio 3 to 1.', '150 root 3 is five times 30 root 3. Area ratio 5 to 1.'),
        ('Root 3 to root 1 — root 3 to 1.', 'Root 5 to root 1 — root 5 to 1.'),
        ('$72\\sqrt3:24\\sqrt3=3:1$', '$150\\sqrt3:30\\sqrt3=5:1$'), ('72√3 : 24√3 = 3 : 1 appears', '150√3 : 30√3 = 5 : 1 appears'),
        ('$\\sqrt3:\\sqrt1=\\sqrt3:1$', '$\\sqrt5:\\sqrt1=\\sqrt5:1$'), ('√3 : 1 appears', '√5 : 1 appears'),
        ('Circle choice 4', 'Circle choice 1'), ('Choice four. Much, much shorter', 'Choice one. Much, much shorter')])

    # ---------- g150: small diameter = 2/3 R -> 26:1 (Hebrew: = R -> 7:1)  ==>  glass globe, diameter = R/2 -> 63:1
    g = 'geo36-g150'
    _rn_q(M, g, stem='A hollow glass globe contains a small solid ball. The small ball\u2019s diameter is $\\frac12$ of the globe\u2019s radius. What is the ratio of the difference between their volumes to the small ball\u2019s volume?',
          choices=['$64:1$', '$15:1$', '$16:1$', '$63:1$'], correct=4, expl=[
              'Spheres are similar. Let the globe\u2019s radius be $R$. The small diameter is $\\frac12R$, so the small radius is $\\frac14R$. The ratio of the radii is $1:4$.',
              'The ratio of the volumes is $1^3:4^3=1:64$. Small ball: $1$ unit. Globe: $64$ units.',
              'Difference: $64-1=63$ units. The requested ratio is $63:1$. ($64:1$ forgets to subtract.)'],
          figure=rn_fig_g150())
    _rn_sub(M, S(g), 2, [
        ("A sphere contains a smaller ball. The small ball's diameter is two thirds of the big sphere's radius.",
         "A glass globe contains a small ball. The small ball's diameter is half of the globe's radius."),
        ('The small diameter is two thirds of the big radius.', 'The small diameter is half of the big radius.'),
        ('so the small radius is one third of the big radius. Ratio 1 to 3.', 'so the small radius is one quarter of the big radius. Ratio 1 to 4.'),
        ('$2r=\\frac23R\\ \\Rightarrow\\ r=\\frac13R$', '$2r=\\frac12R\\ \\Rightarrow\\ r=\\frac14R$'), ('r = ⅓R appears', 'r = ¼R appears')])
    _rn_sub(M, S(g), 3, [
        ('1 cubed is 1, 3 cubed is 27.', '1 cubed is 1, 4 cubed is 64.'),
        ('Small ball — 1 unit. Big sphere — 27 units.', 'Small ball — 1 unit. Globe — 64 units.'),
        ('The difference: 27 minus 1 — 26 units. Difference over the small ball: 26 to 1.',
         'The difference: 64 minus 1 — 63 units. Difference over the small ball: 63 to 1.'),
        ("Watch out for 27 to 1 — that's the whole sphere, before subtracting.", "Watch out for 64 to 1 — that's the whole globe, before subtracting."),
        ('$1:3\\ \\rightarrow\\ 1:27$', '$1:4\\ \\rightarrow\\ 1:64$'), ('1 : 3 → 1 : 27 appears', '1 : 4 → 1 : 64 appears'),
        ('$27-1=26\\ \\Rightarrow\\ 26:1$', '$64-1=63\\ \\Rightarrow\\ 63:1$'), ('27 − 1 = 26 → 26 : 1 appears', '64 − 1 = 63 → 63 : 1 appears'),
        ('Circle choice 3', 'Circle choice 4'), ('Choice three.', 'Choice four.')])

    # ---------- g151: cup r/3, h/4 -> 36 (Hebrew: r/5, h/3 -> 75)  ==>  sand scoop r/2, h/6 -> 24
    g = 'geo36-g151'
    _rn_q(M, g, stem='A cone-shaped container with base radius $r$ and height $h$ is filled with sand using a cone-shaped scoop. The scoop\'s radius is $\\frac r2$, and its height is $\\frac h6$. How many full scoops are needed to fill the container? (Assume that no sand is spilled.)',
          choices=['$12$', '$72$', '$24$', '$8$'], correct=3, expl=[
              'The cones are not similar (the radius and the height change by different factors), so multiply the separate factors.',
              'From the scoop to the container, the radius is multiplied by $2$, so the volume is multiplied by $2^2=4$. The height is multiplied by $6$, so the volume is multiplied by $6$.',
              'Together: $4\\cdot6=24$. So $24$ scoops fill the container. ($12$ forgets to square the radius factor, and $8=2^3$ treats the cones as similar.)'])
    _rn_sub(M, S(g), 2, [
        ('A cone tank, radius r, height h. A cone cup: radius r over 3, height h over 4. How many cups fill the tank?',
         'A cone container, radius r, height h. A cone scoop: radius r over 2, height h over 6. How many scoops fill the container?'),
        ('The cup: pi times r over 3 squared — r squared over 9 — times h over 4. Over 3.',
         'The scoop: pi times r over 2 squared — r squared over 4 — times h over 6. Over 3.'),
        ('pi r squared h — and pi r squared h over 36. The tank is 36 times bigger.',
         'pi r squared h — and pi r squared h over 24. The container is 24 times bigger.'),
        ('$V_{\\text{tank}}=\\frac{\\pi r^2h}{3}$', '$V_{\\text{container}}=\\frac{\\pi r^2h}{3}$'), ('V_tank = πr²h/3 appears', 'V_container = πr²h/3 appears'),
        ('$V_{\\text{cup}}=\\frac{\\pi(\\frac r3)^2\\cdot\\frac h4}{3}=\\frac{\\pi r^2h/36}{3}$', '$V_{\\text{scoop}}=\\frac{\\pi(\\frac r2)^2\\cdot\\frac h6}{3}=\\frac{\\pi r^2h/24}{3}$'),
        ('V_cup appears', 'V_scoop appears'),
        ('Circle choice 1', 'Circle choice 3'), ('Choice one.', 'Choice three.')])
    _rn_sub(M, S(g), 3, [
        ('the height was divided by 4, the radius by 3.', 'the height was divided by 6, the radius by 2.'),
        ('height 4 times bigger, volume 4 times bigger.', 'height 6 times bigger, volume 6 times bigger.'),
        ('The radius is 3 times bigger. Circles are similar — area ratio is the square: 9.',
         'The radius is 2 times bigger. Circles are similar — area ratio is the square: 4.'),
        ('Total: times 4, times 9 — times 36.', 'Total: times 6, times 4 — times 24.'),
        ('Height $\\times4\\ \\rightarrow$ volume $\\times4$', 'Height $\\times6\\ \\rightarrow$ volume $\\times6$'),
        ('Height × 4 → volume × 4 appears', 'Height × 6 → volume × 6 appears'),
        ('Radius $\\times3\\ \\rightarrow$ base $\\times9$', 'Radius $\\times2\\ \\rightarrow$ base $\\times4$'),
        ('Radius × 3 → base × 9 → volume × 9 appears', 'Radius × 2 → base × 4 → volume × 4 appears'),
        ('$4\\times9=36$', '$6\\times4=24$'), ('4 × 9 = 36 appears', '6 × 4 = 24 appears'),
        ('Circle choice 1', 'Circle choice 3'), ('Choice one.', 'Choice three.')])


def rn_practice_questions(M):
    P = lambda k: 'geo36-core-p%02d' % k
    Q = M.q
    _rn_q(M, P(1), stem='The two right triangles in the figure stand on the same straight line. The marked angle between their neighboring legs is $90°$. The ratio $a:b=3:5$. What is the ratio $c:d$?',
          choices=['$5:3$', '$3:5$', '$9:25$', '$\\sqrt3:\\sqrt5$'], correct=2, expl=[
              'Let the angle at the shared point inside the small triangle be $\\theta$. The marked angle is $90°$, so the angle at the shared point inside the large triangle is $180°-90°-\\theta=90°-\\theta$.',
              'The large triangle has a right angle, so its third angle is $\\theta$. The two triangles have the same angles: they are similar.',
              'a is opposite $\\theta$ in the small triangle, and c is opposite $\\theta$ in the large one. So a matches c, and b matches d.',
              'Therefore the ratio $c:d=a:b=3:5$.'])
    _rn_q(M, P(2), stem='Points A, B, C, D, E and F lie on one straight line, and $AB=BC=CD=DE=EF$. Points G and H lie on a ray from A. FG and DH are perpendicular to AF. What is the ratio $DH:FG$?',
          choices=['$1:5$', '$2:5$', '$3:2$', '$3:5$'], correct=4, expl=[
              'Triangles ADH and AFG share the angle at A, and each has a right angle (at D and at F). So they are similar.',
              'AD is $3$ equal parts and AF is $5$ equal parts, so the ratio of the lengths is $3:5$.',
              'DH matches FG, so the ratio $DH:FG=3:5$.'], figure=rn_fig_p02())
    _rn_q(M, P(3), stem='ABCD is a rectangle. E lies on the extension of BA beyond A, F lies on the extension of BC beyond C, and E, D and F lie on one straight line.\nGiven:\n$\\begin{cases} AE=4\\text{ cm} \\\\ CF=6\\text{ cm} \\end{cases}$\nWhat is the area of ABCD (in cm²)?',
          choices=['$10$', '$30$', '$24$', '$20$'], correct=3, expl=[
              'Triangles EAD and DCF each have a right angle (at A and at C). $AD\\parallel CF$, so the angle at D in triangle EAD equals the angle at F in triangle DCF (corresponding angles). The triangles are similar.',
              'Matching legs: $\\frac{AE}{DC}=\\frac{AD}{CF}$, so $AD\\cdot DC=AE\\cdot CF=4\\cdot6=24$.',
              '$AD\\cdot DC$ is exactly the area of the rectangle: $24$.'],
          figure=_relabel(Q(P(3))['questionVisual']['svg'], {'3': '4', '5': '6'}))
    _rn_q(M, P(4), stem='A, B, C and D lie on a circle. Chords AC and BD meet at E. The ratio $AE:DE$ is $2:3$, and $AB=8$ cm. What is the length of DC (in cm)?',
          choices=['$16$', '$12$', '$\\frac{16}3$', '$10$'], correct=2, expl=[
              'The angles ABD and ACD are inscribed angles on the same arc AD, so they are equal (see the circles topic). The angles AEB and DEC are vertical angles.',
              'So triangles AEB and DEC are similar. AE matches DE, and AB matches DC.',
              '$\\frac{AE}{DE}=\\frac{AB}{DC}$: $\\frac23=\\frac8{DC}$, so $DC=12$. ($\\frac{16}3$ turns the ratio upside down.)'],
          figure=_relabel(Q(P(4))['questionVisual']['svg'], {'6': '8'}))
    _rn_q(M, P(5), stem='The ratio of the perimeter of square A to the perimeter of square B is $\\sqrt7:1$. What is the ratio of their side lengths, A to B?',
          choices=['$7:1$', '$\\frac{\\sqrt7}{4}:1$', '$\\sqrt7:1$', '$2\\sqrt7:1$'], correct=3, expl=[
              'All squares are similar, and a perimeter is a length.',
              'So the ratio of the sides equals the ratio of the perimeters: $\\sqrt7:1$.'])
    _rn_q(M, P(6), stem='D, E and F are the midpoints of the sides of triangle ABC. The perimeter of triangle DEF is $19$ cm. What is the perimeter of triangle ABC (in cm)?',
          choices=['$38$', '$57$', '$28.5$', '$76$'], correct=1, expl=[
              'Each side of DEF joins two midpoints, so it is half of a side of ABC.',
              'So the perimeter of DEF is half the perimeter of ABC, and the perimeter of ABC is $2\\cdot19=38$. ($76$ uses the area factor $4$.)'])
    _rn_q(M, P(7), stem='A smaller circle is internally tangent at A to a circle with center O. AB is a diameter of the smaller circle, O lies on AB, and $OA=5\\cdot OB$. What is the ratio of the smaller disk\'s area to the larger disk\'s area?',
          choices=['$\\frac{9}{25}$', '$\\frac35$', '$\\frac1{25}$', '$\\frac{25}{36}$'], correct=1, expl=[
              'Let $OB=x$. Then $OA=5x$, and the small diameter is $AB=5x+x=6x$.',
              'The large radius is $OA=5x$, so the large diameter is $10x$. The ratio of the diameters is $6:10=3:5$.',
              'The ratio of the areas is $3^2:5^2=9:25$, so the answer is $\\frac9{25}$.'], figure=rn_fig_p07())
    _rn_q(M, P(8), stem='Two circular sectors have equal central angles. The arc length of the larger sector is $2.5$ times that of the smaller. What is the ratio of the larger sector\u2019s area to the smaller sector\u2019s area?',
          choices=['$5:2$', '$25:4$', '$4:25$', '$2:5$'], correct=2, expl=[
              'Sectors with equal central angles are similar. The arc lengths give the ratio of the lengths: $2.5:1=5:2$.',
              'The ratio of the areas is $5^2:2^2=25:4$.'], figure=rn_fig_p08())
    _rn_q(M, P(9), stem='$AB\\parallel CD$, and segments AC and BD meet at E.\nGiven:\n$\\begin{cases} AB=2\\text{ cm} \\\\ CD=3\\text{ cm} \\\\ AE=(x-1)\\text{ cm} \\\\ EC=(x+3)\\text{ cm} \\end{cases}$\nWhat is the value of $x$?',
          choices=['$9$', '$6$', '$12$', '$7$'], correct=1, expl=[
              'Triangles ABE and CDE are similar (an hourglass: Z angles and vertical angles). AE matches EC, and AB matches CD.',
              '$\\frac{EC}{AE}=\\frac{CD}{AB}$: $\\frac{x+3}{x-1}=\\frac32$.',
              '$2(x+3)=3(x-1)$, so $2x+6=3x-3$ and $x=9$.',
              'Check: $AE=8$ and $EC=12$, and $\\frac{12}8=\\frac32$ ✓.'], figure=rn_fig_p09())
    _rn_q(M, P(10), stem='A disk is inscribed in a semicircle of radius $8$ cm. It is tangent to the diameter at its midpoint O and tangent internally to the semicircular arc. What fraction of the semicircle\u2019s area lies outside the disk?',
          choices=['$\\frac12$', '$\\frac14$', '$\\frac34$', '$\\frac13$'], correct=1, expl=[
              'The disk touches the diameter at O, so its center lies directly above O, at a distance equal to its radius $r$.',
              'It also touches the arc from the inside, so the distance from O to its center is $8-r$. Therefore $r=8-r$, and $r=4$.',
              'The semicircle: $\\frac{\\pi\\cdot8^2}{2}=32\\pi$. The disk: $\\pi\\cdot4^2=16\\pi$. Outside the disk: $32\\pi-16\\pi=16\\pi$.',
              'The fraction is $\\frac{16\\pi}{32\\pi}=\\frac12$. (With similarity: the disk\'s radius is half the semicircle\'s, so the disk is $\\frac14$ of the full circle, which is $\\frac12$ of the semicircle.)'])
    _rn_q(M, P(11), stem='$AB\\parallel DE$, and segments AE and BD meet at C. The areas of triangles ABC and EDC are $7$ cm² and $63$ cm². What is the ratio $CD:CB$?',
          choices=['$9:1$', '$1:3$', '$3:1$', '$\\sqrt3:1$'], correct=3, expl=[
              'The hourglass triangles ABC and EDC are similar. CB (in the small triangle) matches CD (in the large triangle).',
              'The ratio of the areas is $63:7=9:1$, so the ratio of the lengths is $\\sqrt9:1=3:1$.',
              'So the ratio $CD:CB=3:1$.'], figure=rn_fig_p11())
    _rn_q(M, P(12), stem='A cone has volume V. Its radius is multiplied by $3$, and its height is divided by $3$. The new cone has volume U. What is the ratio $U:V$?',
          choices=['$9:1$', '$1:1$', '$27:1$', '$3:1$'], correct=4, expl=[
              'The radius is multiplied by $3$, so the volume is multiplied by $3^2=9$.',
              'The height is divided by $3$, so the volume is multiplied by $\\frac13$.',
              'Together: $9\\cdot\\frac13=3$. The ratio $U:V=3:1$. ($1:1$ forgets to square the radius factor.)'])
    _rn_q(M, P(13), stem='The area of a disk is multiplied by $16x$, where $x>0$. By what factor is its circumference multiplied?',
          choices=['$16x$', '$4x$', '$4\\sqrt x$', '$16\\sqrt x$'], correct=3, expl=[
              'The area is multiplied by $16x$, so every length is multiplied by $\\sqrt{16x}=4\\sqrt x$.',
              'The circumference is a length, so it is multiplied by $4\\sqrt x$.'])
    _rn_q(M, P(14), stem='E, B and D lie on one straight line. Angles EAB, ABC and BCD are right angles.\nGiven:\n$\\begin{cases} AB=8\\text{ cm} \\\\ BC=15\\text{ cm} \\\\ CD=6\\text{ cm} \\end{cases}$\nWhat is the length of AE (in cm)?',
          choices=['$11.25$', '$20$', '$16$', '$24$'], correct=2, expl=[
              'AE and BC are both perpendicular to AB, so $AE\\parallel BC$. AB and CD are both perpendicular to BC, so $AB\\parallel CD$.',
              'So triangles EAB and BCD have the same angles (right angles at A and at C, and corresponding angles at E and at B). They are similar.',
              'AE matches BC, and AB matches CD: $\\frac{AE}{15}=\\frac86$, so $AE=\\frac{120}6=20$. ($11.25$ matches the sides the wrong way round.)'],
          figure=rn_fig_p14())
    _rn_q(M, P(15), stem='A regular octagon with side $3$ cm has area $a$ cm². What is the area of a regular octagon with side $7$ cm (in cm²)?',
          choices=['$7a$', '$\\frac{7a}{3}$', '$49a$', '$\\frac{49a}{9}$'], correct=4, expl=[
              'Regular octagons are similar. The ratio of the sides is $7:3$, so every length is multiplied by $\\frac73$.',
              'Areas use the square: $\\left(\\frac73\\right)^2=\\frac{49}{9}$.',
              'The new area is $\\frac{49}{9}\\cdot a=\\frac{49a}{9}$ cm². ($\\frac{7a}3$ forgets to square.)'],
          figure=rn_regular(8, 'Regular 8-sided polygon'))
    _rn_q(M, P(16), stem='A cone is cut by a plane parallel to its base. The smaller cone above the cut has height $\\frac34$ of the original height. What is the ratio of the volume below the cut to the volume of the smaller cone?',
          choices=['$64:27$', '$37:27$', '$4:3$', '$16:9$'], correct=2, expl=[
              'The cut is parallel to the base, so the small cone is similar to the whole cone. The ratio of the heights is $3:4$.',
              'The ratio of the volumes is $3^3:4^3=27:64$. Small cone: $27$ units. Whole cone: $64$ units.',
              'Below the cut: $64-27=37$ units. The requested ratio is $37:27$. ($64:27$ forgets to subtract.)'], figure=rn_fig_p16())
    _rn_q(M, P(17), stem='Two rectangles share a corner A, and their sides lie on the same two lines. Their opposite corners B and C lie on the same ray from A, with B between A and C. The ratio $AB:BC=4:3$. The larger rectangle has area S. What is the area of the smaller rectangle?',
          choices=['$\\frac47S$', '$\\frac{16}{49}S$', '$\\frac{9}{49}S$', '$\\frac{16}{9}S$'], correct=2, expl=[
              'The corner B of the small rectangle is on the diagonal AC of the large one, so the rectangles are similar (a rectangle on the diagonal).',
              'AB matches the WHOLE diagonal AC: $AC=4+3=7$ parts. The ratio of the lengths is $4:7$.',
              'The ratio of the areas is $4^2:7^2=16:49$, so the smaller area is $\\frac{16}{49}S$. ($\\frac{16}9S$ uses the part BC instead of the whole AC.)'])
    _rn_q(M, P(18), stem='ABC is a right triangle with the right angle at B. A circle with radius r is tangent to AB at D and to BC at E, and its center O lies on AC. $AD=6$ cm. What is the length of BC (in cm)?',
          choices=['$\\frac{7r}{6}$', '$\\frac{r^2}{6}-r$', '$r+\\frac{r^2}{6}$', '$\\frac{3r}{2}$'], correct=3, expl=[
              'A radius is perpendicular to a tangent, so $OD\\perp AB$ and $OE\\perp BC$. ODBE is a square with side r, so $AB=6+r$.',
              '$OD\\parallel BC$, so triangles ADO and ABC are similar: $\\frac{AD}{AB}=\\frac{OD}{BC}$.',
              '$\\frac6{6+r}=\\frac r{BC}$, so $BC=\\frac{r(6+r)}6=r+\\frac{r^2}6$.'],
          figure=_relabel(Q(P(18))['questionVisual']['svg'], {'4': '6'}))
    _rn_q(M, P(19), stem='ACF is a right triangle with the right angle at F. AGHJ and CDEF are squares. G lies on AF, B lies on AC, and $BG\\parallel CF$.\nGiven:\n$\\begin{cases} AJ=4\\text{ cm} \\\\ AB=12\\text{ cm} \\\\ BC=6\\text{ cm} \\end{cases}$\nWhat is the area of square CDEF (in cm²)?',
          choices=['$36$', '$288$', '$324$', '$144$'], correct=2, expl=[
              'AGHJ is a square, so $AG=AJ=4$.',
              '$BG\\parallel CF$, so triangles ABG and ACF are similar. In triangle ABG, $AG=4$ is a third of $AB=12$.',
              'So in triangle ACF, AF is a third of AC. $AC=12+6=18$, so $AF=6$.',
              'Pythagoras: $CF^2=18^2-6^2=324-36=288$. The area of the square is $CF^2=288$ (no square root needed).'],
          figure=rn_fig_p19())
    _rn_q(M, P(20), stem='The area of a square increases by $96\\%$. By what percent does its side length increase?',
          choices=['$96\\%$', '$40\\%$', '$48\\%$', '$14\\%$'], correct=2, expl=[
              'Area $+96\\%$ means an area factor of $1.96$.',
              'The side is a length: $\\sqrt{1.96}=1.4$, so the side increases by $40\\%$.',
              'Check with numbers: side $10$, area $100$. New area $196$, new side $14$. That is $4$ more out of $10$: $40\\%$. ($48\\%$ just halves the percent.)'])


def rn_practice(M):
    """Approved clean-up (41 -> 27). Copies: q-r26-t36-06 (= lesson part-to-part), -15 (= the backwards percent step),
    -18 (= the map-area guided type). September items whose type the Hebrew practice (or a kept item) already drills:
    -07 (segment vs the whole side: Hebrew p02 / guided), -09 (same height: -08 stays), -11 (trapezoid: -10 stays),
    -13 (cone glass: Hebrew p16), -14 (percent and area: Hebrew p20). English extras: keep p26 (warm-up) and p22 (shadow);
    remove p21, p23, p24, p25, p27 and the box item geo35-core-p27 (types in Hebrew p05/p06, p20, p16, guided)."""
    out = ['q-r26-t36-06', 'q-r26-t36-15', 'q-r26-t36-18', 'q-r26-t36-07', 'q-r26-t36-09', 'q-r26-t36-11',
           'q-r26-t36-13', 'q-r26-t36-14', 'geo36-core-p21', 'geo36-core-p23', 'geo36-core-p24', 'geo36-core-p25',
           'geo36-core-p27']
    if 'geo35-core-p27' in M.D['questions'] and M.section_of('geo35-core-p27') == PRACTICE: out.append('geo35-core-p27')
    for qid in out:
        assert M.section_of(qid) == PRACTICE, qid
        M.unplace(qid)
    p = lambda n: 'geo36-core-p%02d' % n
    M.practice_order(PRACTICE, [p(5), p(26), p(6), p(13), p(15), p(8), p(20), p(12), p(22), p(2), p(1), 'q-r26-t36-16',
                                'q-r26-t36-17', p(11), 'q-r26-t36-08', p(7), p(16), p(4), p(9), p(10), p(14),
                                'q-r26-t36-10', 'q-r26-t36-12', p(17), p(3), p(18), p(19)])


def rn_lessons_cards(M):
    """Lesson examples that used the Hebrew lesson's own numbers get new ones."""
    # Similarity: square diagonal x2 (Hebrew) -> x3; linear 2:3 -> 4:9 (Hebrew) -> 4:5 -> 16:25
    _rn_sub(M, 'geo-134', 6, [
        ('Square: diagonal $\\times2$ $\\rightarrow$ side $\\times2$', 'Square: diagonal $\\times3$ $\\rightarrow$ side $\\times3$'),
        ('Square diagonal ×2 → square side ×2', 'Square diagonal ×3 → square side ×3'),
        ("If the big square's diagonal is twice the small one's — then its side is twice as long too.",
         "If the big square's diagonal is three times the small one's — then its side is three times as long too.")])
    _rn_sub(M, 'geo-134', 10, [
        ('Linear $2:3$ $\\rightarrow$ area $4:9$', 'Linear $4:5$ $\\rightarrow$ area $16:25$'),
        ('Linear 2 : 3 → area 4 : 9', 'Linear 4 : 5 → area 16 : 25'),
        ('Linear 2 to 3 — square both parts — areas 4 to 9.', 'Linear 4 to 5 — square both parts — areas 16 to 25.')])
    # Regular shapes: hexagons 3:5 -> 9:25 (the Hebrew squares example) -> 5:6 -> 25:36
    _rn_sub(M, 'geo-135', 5, [
        ('Side $3:5$', 'Side $5:6$'), ('Side 3 : 5', 'Side 5 : 6'), ('Area $9:25$', 'Area $25:36$'), ('Area 9 : 25', 'Area 25 : 36'),
        ('Linear ratio 3 to 5.', 'Linear ratio 5 to 6.'), ('9 to 25. 3 squared is 9, 5 squared is 25.', '25 to 36. 5 squared is 25, 6 squared is 36.')])
    # Similar triangles: the 6-8-10 triangles (Hebrew 3-4-5 / 6-8-10) -> 12-16-20 and 18-24-30 (same shape, relabeled)
    V = 'geo-139'
    mp = {'6': '12', '8': '16', '10': '20', '9': '18', '12': '24', '15': '30'}
    for n in (3, 4, 5):
        for it in M.slide(V, n)['items']:
            if it.get('k') == 'vis': it['v']['svg'] = _relabel(it['v']['svg'], mp)
    _rn_sub(M, V, 4, [
        ('Write 6 → 9, 8 → 12, 10 → 15 in the table', 'Write 12 → 18, 16 → 24, 20 → 30 in the table'),
        ("6 is opposite α here — what's opposite α in the other triangle? 9. So 6 goes with 9.",
         "12 is opposite α here — what's opposite α in the other triangle? 18. So 12 goes with 18."),
        ('8 is opposite β — opposite β over there: 12. And the hypotenuse, 10, goes with the hypotenuse, 15.',
         '16 is opposite β — opposite β over there: 24. And the hypotenuse, 20, goes with the hypotenuse, 30.')])
    _rn_sub(M, V, 5, [('9 is still opposite α, and 12 is still opposite β.', '18 is still opposite α, and 24 is still opposite β.')])
    _rn_sub(M, V, 6, [
        ('$\\frac68=\\frac9{12}=\\frac34$', '$\\frac{12}{16}=\\frac{18}{24}=\\frac34$'), ('6/8 = 9/12 = 3/4 appears', '12/16 = 18/24 = 3/4 appears'),
        ('$\\frac8{10}=\\frac{12}{15}=\\frac45$', '$\\frac{16}{20}=\\frac{24}{30}=\\frac45$'), ('8/10 = 12/15 = 4/5 appears', '16/20 = 24/30 = 4/5 appears'),
        ('A fraction is just a ratio: $4:5=8:10$', 'A fraction is just a ratio: $4:5=16:20$'),
        ('A fraction is a ratio: 4 : 5 = 8 : 10 appears', 'A fraction is a ratio: 4 : 5 = 16 : 20 appears'),
        ('6 over 8 — three quarters. 9 over 12 — also three quarters.', '12 over 16 — three quarters. 18 over 24 — also three quarters.'),
        ('8 over 10 — four fifths. 12 over 15 — four fifths.', '16 over 20 — four fifths. 24 over 30 — four fifths.')])
    for it in M.slide(V, 9)['items']:
        if it.get('k') == 'vis': it['v']['svg'] = _relabel(it['v']['svg'], {'6': '15', '8': '20', '10': '25'})
    _rn_sub(M, V, 9, [
        ('With 6, 8, 10: the factor is 6 to 10, three fifths — so BD is 3.6 and AD is 4.8.',
         'With 15, 20, 25: the factor is 15 to 25, three fifths — so BD is 9 and AD is 12.'),
        ('4.8 squared is 23.04, and 3.6 times 6.4 is also 23.04.', '12 squared is 144, and 9 times 16 is also 144.'),
        ('AB is 6 — 36. And 3.6 times 10 — 36.', 'AB is 15 — 225. And 9 times 25 — 225.')])
    # Similar solids: the 3 x 3 x 3 cube (= the Hebrew volume lesson) -> 4 x 4 x 4 (redrawn)
    V = 'geo-141'
    for it in M.slide(V, 4)['items']:
        if it.get('k') == 'vis': it['v']['svg'] = rn_cubes(4)
    _rn_sub(M, V, 4, [
        ('A big cube built from 3 × 3 × 3 small cubes appears', 'A big cube built from 4 × 4 × 4 small cubes appears'),
        ('a big cube whose edge is 3 times longer. Length ratio 1 to 3.', 'a big cube whose edge is 4 times longer. Length ratio 1 to 4.'),
        ('Count the bottom layer: 9', 'Count the bottom layer: 16'), ('One layer — 3 by 3 — 9 cubes.', 'One layer — 4 by 4 — 16 cubes.'),
        ('Write × 3 layers = 27', 'Write × 4 layers = 64'), ('And three layers. 27.', 'And four layers. 64.'),
        ('Length $1:3$ $\\rightarrow$ area $1:9$ $\\rightarrow$ volume $1:27$', 'Length $1:4$ $\\rightarrow$ area $1:16$ $\\rightarrow$ volume $1:64$'),
        ('1 : 3 → 1 : 9 → 1 : 27 appears', '1 : 4 → 1 : 16 → 1 : 64 appears'),
        ('Length 1 to 3. Area — squared — 1 to 9. Volume — cubed — 1 to 27.', 'Length 1 to 4. Area — squared — 1 to 16. Volume — cubed — 1 to 64.')])
    # Volume changes: edge x4 -> x5 (so it does not repeat the cube above); radius x3 -> x9 (Hebrew) -> x5 -> x25
    V = 'geo-143'
    k = next(i for i, b in enumerate(M.video(V)['beats'], 1) if b['title'] == 'Cube edge × 4')
    M.slide(V, k)['title'] = 'Cube edge × 5'
    sb = M.video(V)['hybrid']['sidebar']; sb[sb.index('Cube edge × 4')] = 'Cube edge × 5'
    _rn_sub(M, V, k, [
        ('One layer: $4\\times4=16$ $\\quad$ 4 layers: $64$', 'One layer: $5\\times5=25$ $\\quad$ 5 layers: $125$'),
        ('One layer: 4 × 4 = 16 · four layers = 64 appears', 'One layer: 5 × 5 = 25 · five layers = 125 appears'),
        ('$V=a^3\\quad\\rightarrow\\quad(4a)^3=4^3a^3=64a^3$', '$V=a^3\\quad\\rightarrow\\quad(5a)^3=5^3a^3=125a^3$'),
        ('V = a³ → (4a)³ = 64a³ appears', 'V = a³ → (5a)³ = 125a³ appears'),
        ('The edge of a cube is made 4 times longer.', 'The edge of a cube is made 5 times longer.'),
        ('each is now like 4 cubes.', 'each is now like 5 cubes.'),
        ('One layer: 4 by 4, 16 cubes. And 4 layers — 64 cubes.', 'One layer: 5 by 5, 25 cubes. And 5 layers — 125 cubes.'),
        ('Make the edge 4a.', 'Make the edge 5a.'), ('the 4 is cubed — 64.', 'the 5 is cubed — 125.'),
        ('So the original volume grew 64 times. The 4 itself went to the power of three.',
         'So the original volume grew 125 times. The 5 itself went to the power of three.')])
    k = next(i for i, b in enumerate(M.video(V)['beats'], 1) if b['title'] == 'Radius only')
    _rn_sub(M, V, k, [('Radius times 3 — volume times 9.', 'Radius times 5 — volume times 25.')])
    # memory cards: the linear 2:3 example and the 1:9 -> 1:8 leftover (old guided numbers)
    c = M.card('mem-similarity')
    t = c['tables'][0]
    assert t['head'][2] == 'Example (linear $2:3$)', t['head']
    t['head'][2] = 'Example (linear $4:5$)'
    for r in t['rows']:
        r[2] = {'$2:3$': '$4:5$', '$4:9$': '$16:25$'}.get(r[2], r[2])
    old = 'Part vs. leftover: whole $-$ part first, then the ratio ($1:9$ whole $\\rightarrow$ $1:8$ leftover).'
    assert old in c['tips']
    c['tips'] = [('Part vs. leftover: whole $-$ part first, then the ratio ($1:25$ whole $\\rightarrow$ $1:24$ leftover).' if x == old else x)
                 for x in c['tips']]
    c = M.card('mem-similar-triangles')
    old = [x for x in c['tips'] if 'an easy number (\\(x=3\\))' in x]
    assert len(old) == 1
    c['tips'] = [x.replace('an easy number (\\(x=3\\))', 'an easy number that makes a special case') for x in c['tips']]


def renumber_pass(M):
    rn_guided(M)
    rn_practice_questions(M)
    rn_practice(M)
    rn_lessons_cards(M)
    _sync_stem_copies(M)
    review_fixes(M)


def review_fixes(M):
    """2026-10-06 review: the slide title still had the old plug-in number (the video now plugs in 5)."""
    if 'solve-geo36-g145' in RN_RECORDED: return
    b = M.slide('solve-geo36-g145', 4)
    assert b.get('title') == 'Psychometric · plug in x = 3', b.get('title')
    b['title'] = 'Psychometric · plug in x = 5'; M.touched_videos.add('solve-geo36-g145')


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last
