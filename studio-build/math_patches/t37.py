"""Topic 37 - The coordinate system. Course review 2026-09 fixes.
See t37_CHANGES.md for the plain-language list."""
import re
from dsl import T, H, A, D, Q

TOPIC = 37
LEARN = 'geo37-learn-1'
PRACTICE = 'geo37-core-practice'

# ------------------------------------------------------------------------------------------------
# SVG helpers (same style as the existing coordinate-plane figures)
# ------------------------------------------------------------------------------------------------
INK, AXIS, TEAL, ORANGE, FILL, GRID = '#203344', '#71818d', '#087f83', '#bb6821', '#d5f1ed', '#e8eef3'
FONT = 'DejaVu Sans,Arial,sans-serif'
HALO = ' stroke="white" stroke-width="4" stroke-linejoin="round" paint-order="stroke"'


def VIS(svg, w=1000, h=520):
    return dict(k='vis', v={'type': 'geometry', 'svg': svg}, w=w, h=h)


def _text(x, y, s, size=18, anchor='middle', color=INK, halo=False):
    return ('<text x="%.3f" y="%.3f" text-anchor="%s" dominant-baseline="middle" fill="%s" font-family="%s" '
            'font-size="%s"%s>%s</text>' % (x, y, anchor, color, FONT, size, HALO if halo else '', s))


def _line(x1, y1, x2, y2, color=TEAL, w=2.5, dash=False):
    return '<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="%s"%s/>' % (
        x1, y1, x2, y2, color, w, ' stroke-dasharray="7 5"' if dash else '')


def _dot(x, y, color=TEAL):
    return '<circle cx="%.3f" cy="%.3f" r="3.2" fill="%s"/>' % (x, y, color)


def _poly(pts, fill=FILL, stroke=TEAL, w=2.5):
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (
        ' '.join('%.3f,%.3f' % p for p in pts), fill, stroke, w)


class Plane:
    """A coordinate plane drawn like the course figures (axes with arrows, x / y / O labels, optional grid)."""

    def __init__(self, xmin, xmax, ymin, ymax, grid=False, ticks=False, skip_y=()):
        self.u = min(292.0 / (ymax - ymin), 420.0 / (xmax - xmin))
        self.ox = 320 - self.u * (xmin + xmax) / 2.0
        self.oy = 34 + self.u * ymax
        self.r = (xmin, xmax, ymin, ymax)
        self.body = []
        self.grid, self.ticks, self.skip_y = grid, ticks, set(skip_y)

    def P(self, x, y): return (self.ox + self.u * x, self.oy - self.u * y)

    def add(self, *els): self.body.extend(els)

    def label(self, x, y, s, dx=0, dy=0, anchor='middle', size=18, color=INK):
        px, py = self.P(x, y); self.body.append(_text(px + dx, py + dy, s, size, anchor, color, halo=True))

    def point(self, x, y, color=TEAL): self.body.append(_dot(*self.P(x, y), color=color))

    def seg(self, a, b, color=TEAL, w=2.5, dash=False):
        self.body.append(_line(*(self.P(*a) + self.P(*b)), color=color, w=w, dash=dash))

    def poly(self, pts, fill=FILL, stroke=TEAL, w=2.5):
        self.body.append(_poly([self.P(*p) for p in pts], fill, stroke, w))

    def svg(self, title='Coordinate plane', full=False):
        xmin, xmax, ymin, ymax = self.r
        out = []
        if self.grid:
            for x in range(int(xmin), int(xmax) + 1):
                if x: out.append(_line(self.P(x, ymin)[0], self.P(0, ymin)[1], self.P(x, ymax)[0], self.P(0, ymax)[1], GRID, 1))
            for y in range(int(ymin), int(ymax) + 1):
                if y: out.append(_line(self.P(xmin, 0)[0], self.P(0, y)[1], self.P(xmax, 0)[0], self.P(0, y)[1], GRID, 1))
        x0, y0 = self.P(xmin, 0); x1, _ = self.P(xmax, 0)
        _, ya = self.P(0, ymin); _, yb = self.P(0, ymax)
        out.append(_line(x0 - 12, y0, x1 + 12, y0, AXIS, 1.8))
        out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f" fill="none" stroke="%s" stroke-width="1.8"/>' % (
            x1 + 5, y0 - 4, x1 + 12, y0, x1 + 5, y0 + 4, AXIS))
        out.append(_text(x1 + 26, y0 - 14, 'x'))
        out.append(_line(self.ox, ya + 12, self.ox, yb - 12, AXIS, 1.8))
        out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f" fill="none" stroke="%s" stroke-width="1.8"/>' % (
            self.ox - 4, yb - 5, self.ox, yb - 12, self.ox + 4, yb - 5, AXIS))
        out.append(_text(self.ox - 14, yb - 26, 'y'))
        if self.ticks:
            for x in range(int(xmin), int(xmax) + 1):
                if x:
                    px = self.P(x, 0)[0]
                    out.append(_line(px, y0 - 3, px, y0 + 3, AXIS, 1))
                    out.append(_text(px, y0 + 17, str(x).replace('-', '−'), 13))
            for y in range(int(ymin), int(ymax) + 1):
                if y and y not in self.skip_y:
                    py = self.P(0, y)[1]
                    out.append(_line(self.ox - 3, py, self.ox + 3, py, AXIS, 1))
                    out.append(_text(self.ox - 16, py, str(y).replace('-', '−'), 13))
        out.append(_text(self.ox - 13, self.oy + 17, 'O', 15))
        vx0 = min(x0 - 12, self.ox - 40) - 50; vx1 = x1 + 70
        if full:
            return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="%s">'
                    '<title>%s</title>%s</svg>') % (title, title, ''.join(out + self.body))
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.1f -6.0 %.1f 358.0" role="img" aria-label="%s">'
                '<title>%s</title>%s</svg>') % (vx0, vx1 - vx0, title, title, ''.join(out + self.body))


# ---- editing existing SVG strings ----------------------------------------------------------------
_TX = r'<text x="([\d.]+)" y="([\d.]+)" text-anchor="(\w+)"([^>]*)>%s</text>'


def _move(svg, label, x=None, y=None, anchor=None, dx=0, dy=0, halo=True):
    """Move the text element whose content is `label` (absolute x/y or relative dx/dy)."""
    rx = re.compile(_TX % re.escape(label))
    m = rx.search(svg)
    assert m, 'label not found: ' + label
    nx = float(m.group(1)) + dx if x is None else x
    ny = float(m.group(2)) + dy if y is None else y
    rest = m.group(4)
    if halo and 'paint-order' not in rest: rest += HALO
    new = '<text x="%.3f" y="%.3f" text-anchor="%s"%s>%s</text>' % (nx, ny, anchor or m.group(3), rest, label)
    return svg[:m.start()] + new + svg[m.end():]


def _backdrop(svg, label):
    """White box behind a label (start-anchored, font 18) so dashed lines do not run through it."""
    m = re.search(_TX % re.escape(label), svg)
    x, y = float(m.group(1)), float(m.group(2))
    rect = '<rect x="%.1f" y="%.1f" width="%.1f" height="22" fill="white"/>' % (x - 3, y - 11, len(label) * 10.2 + 6)
    return svg[:m.start()] + rect + svg[m.start():]


def _has(svg, label): return re.search(_TX % re.escape(label), svg) is not None


def _drop(svg, pattern):
    """Remove every element (line/circle/text/...) matching the regex pattern."""
    return re.sub(pattern, '', svg)


def _axes(svg):
    """(x of the y-axis, y of the x-axis) of a course plane figure."""
    xs = re.search(r'<line x1="([\d.]+)" y1="[\d.]+" x2="\1" y2="[\d.]+" stroke="#71818d" stroke-width="1.8"/>', svg)
    ys = re.search(r'<line x1="[\d.]+" y1="([\d.]+)" x2="[\d.]+" y2="\1" stroke="#71818d" stroke-width="1.8"/>', svg)
    return float(xs.group(1)), float(ys.group(1))


def _o_label(svg, where):
    """Put the origin label O in a free corner: 'ur' up-right, 'ul' up-left, 'dr' down-right of the origin."""
    ax, ay = _axes(svg)
    pos = {'ul': (ax - 11, ay - 12), 'dr': (ax + 13, ay + 17), 'ur': (ax + 13, ay - 13)}[where]
    return _move(svg, 'O', x=pos[0], y=pos[1], anchor='middle')


def _append(svg, *els): return svg.replace('</svg>', ''.join(els) + '</svg>')


def _fix_svg(svg):
    """All figure fixes of the topic. Each fix recognizes its figure by its labels."""
    o = svg
    grid = GRID in svg
    # 1. crowded "O" next to the "-1" labels on the grid planes (video 1 and the Lengths video)
    if grid and _has(svg, 'O') and _has(svg, '−1') and not _has(svg, 'U (−1, 0)'):
        svg = _o_label(svg, 'ul')
    # 2. v722: "O" sat next to U(-1, 0), so U looked like the origin
    if _has(svg, 'U (−1, 0)'):
        svg = _o_label(svg, 'dr')
    # 3. Slope video, points on a line through the origin (P, Q, R, S): labels were on the line
    if _has(svg, 'P (2, 3)') and _has(svg, 'S (−2, −3)'):
        for lab, dx, dy in (('P (2, 3)', -23, 22), ('Q (4, 6)', -23, 22), ('R (6, 9)', -23, 22)):
            svg = _move(svg, lab, dx=dx, dy=dy, anchor='start')
            svg = _backdrop(svg, lab)
        svg = _move(svg, 'S (−2, −3)', x=235, y=299.5, anchor='end')
        svg = _o_label(svg, 'dr')
        vb = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', svg)
        if vb and float(vb.group(1)) > 120:
            x0 = float(vb.group(1)); w = float(vb.group(3))
            svg = svg.replace(vb.group(0), 'viewBox="120.0 %s %.1f %s"' % (vb.group(2), w + x0 - 120, vb.group(4)), 1)
    # 4. Q3 (line through O and A(-2a, -2b)): O and A labels were on the line
    if _has(svg, 'A (−2a, −2b)'):
        svg = _move(svg, 'A (−2a, −2b)', x=233, y=293.5, anchor='end')
        svg = _move(svg, 'B (x, y)', x=386.75, y=103.875, anchor='start')
        svg = _o_label(svg, 'dr')
    # 5. Q4 trapezoid: the origin label E was on the line AB
    if _has(svg, 'A (3, 4)') and _has(svg, 'E'):
        svg = _o_label_named(svg, 'E')
    # 6. Q5 rectangle: the label (-2, 1) ran into the x-axis
    if _has(svg, '(−2, 1)') and _has(svg, '(3, 9)'):
        svg = _move(svg, '(−2, 1)', x=240, y=266, anchor='end')
    # 7. Q8 lines m and n: "A (5, 7)" sat on line m, "n" ran into "C (10, 4)"
    if _has(svg, 'C (10, 4)') and _has(svg, 'A (5, 7)'):
        svg = _move(svg, 'A (5, 7)', x=312, y=88, anchor='end')
        svg = _move(svg, 'C (10, 4)', x=432, y=162, anchor='end')
    # 8. practice p02: B label on the line
    if _has(svg, 'B (0, −2)') and _has(svg, 'A (6, 0)'):
        svg = _move(svg, 'B (0, −2)', x=330, y=216, anchor='start')
    # 9. practice p04: the 60° mark touched OB
    if _has(svg, '60°') and _has(svg, 'B') and not _has(svg, 'D'):
        svg = _move(svg, '60°', x=362, y=168, halo=False)
    # 10. practice p05: B is the origin, so the extra O label overlapped "B (0, 0)"
    if _has(svg, 'B (0, 0)'):
        svg = _drop(svg, r'<text [^>]*font-size="15">O</text>')
    # 11. practice p09: the circle ran through the O label
    if _has(svg, 'A (12, 0)') and _has(svg, '(0, y)'):
        svg = _o_label(svg, 'dr')
    # 12. practice p10: the answer (the x-axis) was drawn as a thick teal line
    if re.search(r'<circle cx="320.000" cy="191.231" r="89.846"', svg):
        svg = _drop(svg, r'<line x1="185.231" y1="281.077" x2="454.769" y2="281.077" stroke="#087f83" stroke-width="3"/>')
    # 13. practice p15: the x-axis arrow ran through "C (6, 2)"
    if _has(svg, 'C (6, 2)') and _has(svg, 'B (−2, 2)'):
        svg = _move(svg, 'B (−2, 2)', x=234, y=267.6, anchor='end')
        svg = _move(svg, 'C (6, 2)', x=406, y=267.6, anchor='start')
    # 14. practice p20: A and B labels on the line
    if _has(svg, 'A (n, 6)'):
        svg = _move(svg, 'A (n, 6)', x=405, y=80, anchor='end')
        svg = _move(svg, 'B (−1, −2)', x=210, y=270, anchor='end')
    # 15. practice p25: the intercepts 4 and 6 (the whole question) were written on the axes
    if re.search(r'<polygon points="174.000,284.286 424.286,284.286 174.000,117.429"', svg):
        svg = _drop(svg, r'<text [^>]*font-size="20">[46]</text>')
    return svg


def _o_label_named(svg, name):
    ax, ay = _axes(svg)
    return _move(svg, name, x=ax + 13, y=ay + 17, anchor='middle')


def _split_points(svg, keep):
    """Video 1 slides 5-7: the figure showed A, B and C at once. Keep only one point (with its dashed lines)."""
    pts = {'A': ('426.182', '113.636'), 'B': ('187.273', '140.182'), 'C': ('240.364', '272.909')}
    for name, (cx, cy) in pts.items():
        if name == keep: continue
        svg = _drop(svg, r'<line x1="%s" y1="%s" [^>]*/>' % (cx, cy))
        svg = _drop(svg, r'<circle cx="%s" cy="%s" [^>]*/>' % (cx, cy))
        svg = _drop(svg, r'<text [^>]*font-size="18">%s</text>' % name)
    return svg


# ------------------------------------------------------------------------------------------------
# small editing helpers
# ------------------------------------------------------------------------------------------------
def _say(M, vid, n, old, new):
    hit = []

    def fn(lines):
        for l in lines:
            if 'say' in l and old in l['say']:
                l['say'] = l['say'].replace(old, new); hit.append(1)
        return lines
    M.edit_lines(vid, n, fn)
    assert hit, (vid, n, old)


def _item(M, vid, n, old_t, new_t, new_label=None):
    b = M.slide(vid, n)
    k = [i for i, it in enumerate(b['items']) if it.get('t') == old_t]
    assert k, (vid, n, old_t)
    b['items'][k[0]]['t'] = new_t
    if new_label:
        for l in b['lines']:
            if l.get('appear') == k[0]: l['label'] = new_label
    M.touched_videos.add(vid)


def _spelling(M):
    rep = [('centred', 'centered'), ('centre', 'center'), ('Centre', 'Center'), ('neighbouring', 'neighboring'),
           ('practise', 'practice')]

    def fix(s):
        for a, b in rep: s = s.replace(a, b)
        return s
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            b['title'] = fix(b['title'])
            for l in b['lines']:
                for key in ('say', 'draw', 'label'):
                    if key in l: l[key] = fix(l[key])
            for it in b['items']:
                if it.get('t'): it['t'] = fix(it['t'])
        v['hybrid']['sidebar'] = [fix(x) for x in v['hybrid'].get('sidebar', [])]
        M.touched_videos.add(v['id'])
    c = M.card('mem-coordinates')
    for tb in c['tables']:
        tb['rows'] = [[fix(x) for x in r] for r in tb['rows']]
    c['tips'] = [fix(x) for x in c['tips']]


def _all_figures(M):
    """Apply _fix_svg to every figure of the topic: question figures, slide figures and figures inside question items."""
    for q in M.D['questions'].values():
        if q['topic'] == TOPIC and q.get('questionVisual') and q['questionVisual'].get('svg'):
            new = _fix_svg(q['questionVisual']['svg'])
            if new != q['questionVisual']['svg']: M.set_q(q['id'], figure=new)
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            for it in b['items']:
                if it.get('k') == 'vis' and it.get('v', {}).get('svg'):
                    new = _fix_svg(it['v']['svg'])
                    if new != it['v']['svg']: it['v']['svg'] = new; M.touched_videos.add(v['id'])
                if it.get('k') == 'q' and it.get('fig', {}).get('svg'):
                    new = _fix_svg(it['fig']['svg'])
                    if new != it['fig']['svg']: it['fig']['svg'] = new; M.touched_videos.add(v['id'])


def _solution(M, qid, title, intro, slides, after=None, before=None):
    """Guided question solution video (own sidebar, like the topic's first three guided questions)."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for sl in slides:
        pre = sl[2] if len(sl) > 2 else [Q(qid)]
        beats.append(dict(mode='question', active=0, title=sl[0], pre=pre, script=sl[1]))
    v = M.new_video('solve-' + qid, TOPIC, title, ['Question %d' % n], beats, M.section_of(qid), kind='solution', qid=qid)
    v['beats'][0]['title'] = 'Coordinate Question'
    v['hybrid']['title'] = 'Coordinate Question'
    v['hybrid']['num'] = M.video('solve-geo37-g156')['hybrid'].get('num', 0)
    return n


def _renumber_active(M, vid):
    for k, b in enumerate(M.video(vid)['beats'][1:]):
        b['active'] = k
    M.touched_videos.add(vid)


# ------------------------------------------------------------------------------------------------
# Question texts: every stem, choice list and worked solution of the topic (TeX, numbers shown)
# ------------------------------------------------------------------------------------------------
QTEXT = {
    'geo37-g156': dict(
        stem='The vertices of triangle $ABC$ are $A(4,\\ 7)$, $B(-8,\\ -5)$ and $C(13,\\ -5)$. What is its perimeter?',
        expl=['$B$ and $C$ have the same $y$ ($-5$), so $BC$ is horizontal: $BC=8+13=21$.',
              'Drop the altitude from $A$ to $BC$. Its foot is $H(4,\\ -5)$, and $AH=7+5=12$.',
              'Left: $BH=8+4=12$ and $AH=12$. This is a 45-45-90 triangle, so $AB=12\\sqrt2$.',
              'Right: $HC=13-4=9$ and $AH=12$. This is the triple 9-12-15, so $AC=15$.',
              'Perimeter: $21+15+12\\sqrt2=36+12\\sqrt2$.']),
    'geo37-g158': dict(
        stem='A circle with radius $10$ is centered at the origin $O$. The point $A$ lies on the circle in the first quadrant, and its $y$-coordinate is $5$. What is the angle between $OA$ and the positive $x$-axis?',
        expl=['Drop $AH$ perpendicular to the $x$-axis. $AH=5$ (the $y$ of $A$) and $OA=10$ (a radius).',
              'In a right triangle, a leg that is half the hypotenuse faces a $30°$ angle (the 30-60-90 triangle).',
              'So $\\angle AOH=30°$.']),
    'geo37-g160': dict(
        stem='A straight line passes through the origin and through $A(-2a,\\ -2b)$, where $a>0$, $b>0$ and $a\\ne b$. The point $B$ lies on this line in the first quadrant. Which of the following cannot be the coordinates of $B$?',
        expl=['The line passes through the origin, so every point on it has the same ratio $\\frac xy$. For $A$: $\\frac{-2a}{-2b}=\\frac ab$.',
              'Check the choices: $\\frac{3a}{3b}=\\frac ab$, $\\ \\frac1b\\div\\frac1a=\\frac ab$ and $\\frac{a/2}{b/2}=\\frac ab$. These three can be on the line.',
              '$\\frac{a^3}{b^3}=\\frac ab$ only if $a^2=b^2$, that is $a=b$ (both are positive). But $a\\ne b$, so $(a^3,\\ b^3)$ cannot be on the line.',
              'Quick check with numbers: $a=1$, $b=2$. The line goes through $(1,\\ 2)$, so $y$ is always twice $x$. $(1,\\ 8)$ is not on it; $(3,\\ 6)$ and $(\\frac12,\\ 1)$ are.']),
    'geo37-g162': dict(
        stem='$ABCD$ is a right trapezoid with $AD\\parallel BC$. Side $DC$ is parallel to the $y$-axis, and $AB$ passes through the origin $E$. Given: $A(3,\\ 4)$, $D(8,\\ 4)$ and $AE=EB$. What is the area of the trapezoid?',
        expl=['$E$ is the origin and the midpoint of $AB$. From $E$ to $A$: 3 right and 4 up. So from $E$ to $B$: 3 left and 4 down. $B=(-3,\\ -4)$.',
              '$AD=8-3=5$. $C$ is below $D$, at the height of $B$: $C=(8,\\ -4)$. So $BC=3+8=11$.',
              'The height is $DC=4+4=8$.',
              'Area: $\\frac{(5+11)\\cdot8}{2}=64$.']),
    'geo37-g163': dict(
        stem='A rectangle has sides parallel to the coordinate axes. Two opposite vertices of the rectangle are $(-2,\\ 1)$ and $(3,\\ 9)$. The rectangle makes a full turn around its right-hand vertical side. What is the volume of the solid formed?',
        expl=['The width is $3-(-2)=5$ and the height is $9-1=8$.',
              'A full turn around the right side gives a cylinder. Its radius is the width, $r=5$, and its height is $h=8$.',
              '$V=\\pi r^2h=\\pi\\cdot25\\cdot8=200\\pi$.']),
    'geo37-g164': dict(
        stem='A circle is centered at the origin $O$ and passes through $A(6,\\ 6)$. $B$ is the point where the circle meets the negative $y$-axis. The two shaded regions together are the right half of the circle without triangle $OAB$. What is their total area?',
        expl=['Radius: from $O$ to $A(6,\\ 6)$ is 6 right and 6 up, a 45-45-90 triangle. So $r=6\\sqrt2$ and $r^2=72$.',
              'The right half of the circle: $\\frac{72\\pi}{2}=36\\pi$.',
              'Triangle $OAB$: the base $OB=6\\sqrt2$ is a radius on the $y$-axis. The height to it is the distance from $A$ to the $y$-axis, 6. Area: $\\frac{6\\sqrt2\\cdot6}{2}=18\\sqrt2$.',
              'Shaded area: $36\\pi-18\\sqrt2$.']),
    'geo37-g165': dict(
        stem='$ABCDEF$ is a regular hexagon. Side $CD$ lies on the positive $x$-axis, $B$ lies on the positive $y$-axis, and $C=(3,\\ 0)$. The whole hexagon is shaded except triangle $AFE$. What is the shaded area?',
        expl=['Each angle of a regular hexagon is $120°$, so $\\angle BCO=180°-120°=60°$.',
              'Triangle $BOC$ is a 30-60-90 triangle with short leg $OC=3$. So the side of the hexagon is $BC=2\\cdot3=6$.',
              'The hexagon is 6 equilateral triangles with side 6. Each has area $\\frac{6^2\\sqrt3}{4}=9\\sqrt3$. Triangle $AFE$ has the same area as one of them.',
              'Shaded area: $5\\cdot9\\sqrt3=45\\sqrt3$.']),
    'geo37-g166': dict(
        stem='Line $n$ passes through the origin and through $C(10,\\ 4)$. Line $m$ is parallel to $n$ and passes through $A(5,\\ 7)$ and $B(0,\\ b)$. What are the coordinates of $B$?',
        expl=['Line $n$: from $O$ to $C(10,\\ 4)$ is 10 right and 4 up.',
              'Line $m$ is parallel to $n$, so it has the same steps: 5 right goes with $\\frac{4}{10}\\cdot5=2$ up.',
              'From $B$ (on the $y$-axis) to $A(5,\\ 7)$ is 5 right, so 2 up. Then $b=7-2=5$ and $B=(0,\\ 5)$.']),
    'geo37-g167': dict(
        stem='A straight line and the $y$-axis have some number of points in common. Which of the following cannot be that number?',
        expl=['A line parallel to the $y$-axis (and not on it) never meets it: 0 points.',
              'A slanted line or a horizontal line meets the $y$-axis once: 1 point.',
              'The $y$-axis itself: infinitely many points.',
              'A straight line can never meet the $y$-axis in exactly 3 points.']),
    'geo37-g168': dict(
        stem='Straight line $a$ does not intersect the $y$-axis, and straight line $b$ does not intersect the $x$-axis. Which of the following is necessarily true?',
        choices=['If $(4,\\ -3)$ lies on $a$, then $(4,\\ 7)$ also lies on $a$.',
                 'If $(4,\\ -3)$ lies on $a$, then $(-4,\\ -3)$ also lies on $a$.',
                 'If $(-2,\\ 5)$ lies on $b$, then $(6,\\ -5)$ also lies on $b$.',
                 'If $(-2,\\ 5)$ lies on $b$, then $(-2,\\ -5)$ also lies on $b$.'],
        expl=['Line $a$ never meets the $y$-axis, so it is parallel to it (vertical). Every point on $a$ has the same $x$.',
              'If $(4,\\ -3)$ is on $a$, then every point on $a$ has $x=4$. So $(4,\\ 7)$ is on $a$: choice 1 is true.',
              'Choice 2 changes $x$, so it is false.',
              'Line $b$ is horizontal. If $(-2,\\ 5)$ is on $b$, every point on $b$ has $y=5$. Choices 3 and 4 change $y$, so they are false.']),
    'geo37-g169': dict(
        stem='A straight line passes through $(-2,\\ 4)$. It is not perpendicular to either of the coordinate axes. Which of the following points cannot lie on the line?',
        expl=['The line is not perpendicular to the $x$-axis, so it is not vertical. It is not perpendicular to the $y$-axis, so it is not horizontal.',
              '$(-2,\\ 9)$ has the same $x$ as $(-2,\\ 4)$. The line through both points is vertical, which is not allowed.',
              'Each other point has a different $x$ and a different $y$ from $(-2,\\ 4)$. The line through it is slanted, so it is possible.']),
    'geo37-core-p01': dict(
        stem='The diagonals of rhombus $ABCD$ lie on the coordinate axes. Given: $A(0,\\ 4)$ and $D(5,\\ 0)$. What is the area of the rhombus?',
        expl=['The diagonals of a rhombus bisect each other, and here they meet at the origin. So $C=(0,\\ -4)$ and $B=(-5,\\ 0)$.',
              '$AC=4+4=8$ and $BD=5+5=10$.',
              'Area $=\\frac{8\\cdot10}{2}=40$.']),
    'geo37-core-p02': dict(
        stem='The points $A(6,\\ 0)$, $B(0,\\ -2)$ and $C$ lie on one straight line, and $B$ is between $A$ and $C$. Given: $AB=BC$. What are the coordinates of $C$?',
        expl=['From $A(6,\\ 0)$ to $B(0,\\ -2)$: 6 left and 2 down.',
              '$AB=BC$ on the same line, so repeat the same move from $B$: $C=(0-6,\\ -2-2)=(-6,\\ -4)$.']),
    'geo37-core-p03': dict(
        stem='For which pair of points does the straight line through them pass through the origin?',
        choices=['$(-6,\\ -5)$ and $(-6,\\ 10)$', '$(-6,\\ 5)$ and $(12,\\ 5)$', '$(-6,\\ -5)$ and $(12,\\ 10)$', '$(-6,\\ -5)$ and $(12,\\ -5)$'],
        expl=['On a line through the origin, you get from one point to another by multiplying both coordinates by the same number.',
              '$(-6,\\ -5)\\cdot(-2)=(12,\\ 10)$. Both coordinates are multiplied by $-2$, so the line through these points passes through the origin.',
              'The other pairs share a coordinate: choice 1 is the vertical line $x=-6$, and choices 2 and 4 are the horizontal lines $y=5$ and $y=-5$. None of them passes through the origin.']),
    'geo37-core-p04': dict(
        stem='A circle centered at the origin $O$ has radius $6$. The point $B$ lies on the circle in the first quadrant, and $BA$ is perpendicular to the positive $x$-axis at $A$. Given: $\\angle BOA=60°$. What are the coordinates of $A$?',
        expl=['$OB=6$ is a radius. Triangle $OAB$ has a right angle at $A$ and $\\angle BOA=60°$, so $\\angle B=30°$.',
              '$OA$ faces the $30°$ angle, so it is half the hypotenuse: $OA=\\frac62=3$.',
              '$A$ is on the positive $x$-axis: $A=(3,\\ 0)$.']),
    'geo37-core-p05': dict(
        stem='The vertices of triangle $ABC$ are $A(5,\\ 12)$, $B(0,\\ 0)$ and $C(10,\\ 0)$. What is its perimeter?',
        expl=['$BC=10-0=10$. The altitude from $A$ meets $BC$ at $(5,\\ 0)$, and its length is 12.',
              'Each half of the base is 5, so $AB=AC=13$ (the triple 5-12-13).',
              'Perimeter $=13+13+10=36$.']),
    'geo37-core-p06': dict(
        stem='$ABC$ is a right triangle with the right angle at $C$. Given: $B(-1,\\ 3)$ and $C(5,\\ 3)$. $A$ lies above $C$, and the area of the triangle is $18$. What are the coordinates of $A$?',
        expl=['$BC$ is horizontal: $BC=5-(-1)=6$. $AC$ is vertical, so it is the height.',
              '$\\frac{6\\cdot AC}{2}=18$, so $AC=6$.',
              '$A$ is 6 above $C(5,\\ 3)$: $A=(5,\\ 9)$.']),
    'geo37-core-p07': dict(
        stem='A straight line intersects the $y$-axis at exactly one point, and that point is not the origin. The line is not perpendicular to the $y$-axis. Which of the following is necessarily true?',
        expl=['The line meets the $y$-axis at one point, so it is not vertical. It is not perpendicular to the $y$-axis, so it is not horizontal. A slanted line meets the $x$-axis too, exactly once.',
              'The line does not pass through the origin, so it meets the two axes at two different points, both away from the origin.',
              'The line and the two axes close a right triangle (the right angle is at the origin).',
              'Choices 1 and 4 are not necessarily true: the line can meet the positive or the negative $x$-axis.']),
    'geo37-core-p08': dict(
        stem='Which pair of points lies on a line parallel to the $y$-axis?',
        choices=['$(-3,\\ 2)$ and $(3,\\ -2)$', '$(2,\\ -3)$ and $(-5,\\ 3)$', '$(-3,\\ 2)$ and $(-3,\\ -5)$', '$(-3,\\ 2)$ and $(4,\\ 2)$'],
        expl=['A line parallel to the $y$-axis is vertical: all its points have the same $x$.',
              'Only $(-3,\\ 2)$ and $(-3,\\ -5)$ have the same $x$, $-3$.']),
    'geo37-core-p09': dict(
        stem='A circle has center $A(12,\\ 0)$ and radius $13$. It intersects the positive $y$-axis at $(0,\\ y)$. What is $y$?',
        expl=['Join the center $A(12,\\ 0)$ to the point $(0,\\ y)$. With the origin, they make a right triangle.',
              'The horizontal leg is 12, and the hypotenuse is a radius, 13. So the other leg is 5 (the triple 5-12-13).',
              'The point is on the positive $y$-axis, so $y=5$.']),
    'geo37-core-p10': dict(
        stem='A circle has its center on the $y$-axis and passes through the origin. Which line is tangent to the circle at the origin?',
        choices=['The $y$-axis', 'The line through $(0,\\ 0)$ and $(1,\\ 1)$', 'The line through $(0,\\ 0)$ and $(1,\\ -1)$', 'The $x$-axis'],
        expl=['The center is on the $y$-axis, so the radius to the origin lies on the $y$-axis.',
              'A tangent is perpendicular to the radius at the point where it touches the circle. The line through the origin that is perpendicular to the $y$-axis is the $x$-axis.']),
    'geo37-core-p11': dict(
        stem='$ABCDEF$ is a regular hexagon. $AB$ lies on the positive $x$-axis, $F$ lies on the positive $y$-axis, and $B=(6,\\ 0)$. A circle passes through all six vertices of the hexagon. What is the radius of the circle?',
        expl=['Let $OA=x$. Each angle of a regular hexagon is $120°$, so $\\angle FAO=180°-120°=60°$.',
              'Triangle $FOA$ is a 30-60-90 triangle with short leg $OA=x$, so the side is $AF=2x$.',
              '$AB=AF=2x$, so $OB=x+2x=3x=6$. Then $x=2$ and the side is 4.',
              'A regular hexagon is 6 equilateral triangles, so the radius of the circle through its vertices equals the side: 4.']),
    'geo37-core-p12': dict(
        stem='Straight lines $a$ and $b$ are parallel, and they are not the same line. Line $a$ passes through the origin, and line $b$ passes through $(0,\\ 3)$. Which point cannot lie on $a$?',
        expl=['If $a$ passed through $(0,\\ -2)$ and the origin, $a$ would be the $y$-axis.',
              'Then $a$ would also pass through $(0,\\ 3)$, which is on $b$. Two different parallel lines have no point in common, so this is impossible.',
              'Each of the other points gives a slanted line through the origin, and $b$ can be the parallel line through $(0,\\ 3)$.']),
    'geo37-core-p13': dict(
        stem='A straight line passes through the origin and through $(a,\\ c)$, where $a>0$, $c>0$ and $a\\ne c$. Which of the following points necessarily lies on the line?',
        expl=['On a line through the origin, both coordinates are multiplied by the same number.',
              '$(a,\\ c)\\cdot(-2)=(-2a,\\ -2c)$, so this point is on the line.',
              'Check the others with the ratio $\\frac xy$. The line has $\\frac ac$. $(3c,\\ 3a)$ and $(\\frac1a,\\ \\frac1c)$ both give $\\frac ca$, which is not $\\frac ac$ because $a\\ne c$. $(-a,\\ c)$ gives a negative ratio.']),
    'geo37-core-p14': dict(
        stem='$ABCD$ is a square. Two neighboring vertices are $A(0,\\ 3)$ and $B(2,\\ 0)$. What is the area of the square?',
        expl=['From $A(0,\\ 3)$ to $B(2,\\ 0)$: 2 across and 3 down. $AB^2=2^2+3^2=13$.',
              'The area of a square is its side squared: $AB^2=13$. No square root is needed.']),
    'geo37-core-p15': dict(
        stem='$ABC$ is an isosceles triangle with $AB=AC$. Given: $B(-2,\\ 2)$ and $C(6,\\ 2)$. $A$ lies above $BC$, and the area of the triangle is $40$. What are the coordinates of $A$?',
        expl=['$BC$ is horizontal: $BC=6-(-2)=8$. Its midpoint is $\\left(\\frac{-2+6}{2},\\ 2\\right)=(2,\\ 2)$.',
              'In an isosceles triangle, the altitude from $A$ goes to the midpoint of $BC$. So $A$ has $x=2$.',
              '$\\frac{8\\cdot h}{2}=40$, so $h=10$. $A$ is 10 above $(2,\\ 2)$: $A=(2,\\ 12)$.']),
    'geo37-core-p16': dict(  # Pass 2: restored original, text clean-up only
        stem='A straight line passes through $(-4,\\ 6)$ and does not intersect the $y$-axis. Which of the following statements is necessarily true?',
        choices=['The point $(6,\\ -4)$ lies on the line.', 'The line is perpendicular to the $x$-axis.',
                 'The point $(4,\\ 6)$ lies on the line.', 'The line passes through the origin.'],
        expl=['A whole straight line that never meets the $y$-axis must be parallel to it. Therefore it is vertical: every point on it has $x=-4$.',
              'A vertical line is perpendicular to the $x$-axis: choice 2.',
              'The other choices: $(6,\\ -4)$, $(4,\\ 6)$ and the origin $(0,\\ 0)$ do not have $x=-4$, so they are not on the line.']),
    'geo37-core-p17': dict(
        stem='$AOBC$ is a square in the first quadrant. $O$ is the origin, and the sides $OA$ and $OB$ lie on the axes. The side of the square is $3$. A circle centered at $O$ passes through $C$. What is the area of the part of the circle in the first quadrant that is outside the square?',
        expl=['$C=(3,\\ 3)$, so $r=OC=3\\sqrt2$ (a 45-45-90 triangle) and $r^2=18$.',
              'The quarter of the circle in the first quadrant: $\\frac{18\\pi}{4}=\\frac{9\\pi}{2}$.',
              'Subtract the square, $3^2=9$: $\\frac{9\\pi}{2}-9$.']),
    'geo37-core-p18': dict(
        stem='$ABCD$ is a trapezoid with $AD\\parallel BC$. $BC$ lies on the $x$-axis. The vertices $A(0,\\ t)$ and $C(2t,\\ 0)$ are given, where $t>0$. $D$ lies to the right of $C$, and $\\angle ADC=60°$. What are the coordinates of $D$?',
        expl=['$AD\\parallel BC$ and $BC$ is on the $x$-axis, so $AD$ is horizontal. $D$ has the same $y$ as $A$: $D=(x,\\ t)$.',
              'Drop $DE$ to the $x$-axis: $DE=t$. $\\angle DCE=\\angle ADC=60°$, because they are alternate angles between the parallel lines $AD$ and $BC$.',
              'Triangle $CED$ is a 30-60-90 triangle. The leg $DE=t$ faces the $60°$ angle, so the short leg is $CE=\\frac{t}{\\sqrt3}$.',
              '$D=\\left(2t+\\frac{t}{\\sqrt3},\\ t\\right)$.']),
    'geo37-core-p19': dict(
        stem='Given: $A(0,\\ 5)$ and $B(6,\\ -1)$. What is the length of $AB$?',
        expl=['Across: $6-0=6$. Down: $5-(-1)=6$.',
              '$AB^2=6^2+6^2=72$, so $AB=\\sqrt{72}$.',
              'Shortcut: the answers are roots, so compare $AB^2=72$ with the numbers under the roots. There is no need to take the root.']),
    'geo37-core-p20': dict(
        stem='The points $A(n,\\ 6)$, $B(-1,\\ -2)$ and $C(1,\\ 0)$ lie on one straight line. What is $n$?',
        expl=['From $B(-1,\\ -2)$ to $C(1,\\ 0)$: 2 right and 2 up. So every 1 right goes 1 up.',
              'From $C$ (height 0) to $A$ (height 6) is 6 up, so it is 6 right: $n=1+6=7$.']),
    'geo37-core-p21': dict(
        stem='The point $P(-7,\\ 3)$ is reflected across the $y$-axis to $Q$. What are the coordinates of $Q$?',
        expl=['A reflection across the $y$-axis changes the sign of $x$ and keeps $y$: $(x,\\ y)\\rightarrow(-x,\\ y)$.',
              '$P(-7,\\ 3)\\rightarrow Q(7,\\ 3)$.']),
    'geo37-core-p22': dict(
        stem='$M(-1,\\ 4)$ is the midpoint of segment $AB$. Given: $A(3,\\ -2)$. What are the coordinates of $B$?',
        expl=['From $A(3,\\ -2)$ to $M(-1,\\ 4)$: 4 left and 6 up.',
              '$M$ is the middle, so repeat the move from $M$: $B=(-1-4,\\ 4+6)=(-5,\\ 10)$.',
              'Check with the averages: $\\frac{3+(-5)}{2}=-1$ and $\\frac{-2+10}{2}=4$. That is $M$.']),
    'geo37-core-p23': dict(
        stem='A circle has center $(3,\\ -4)$ and is tangent to the $x$-axis. What is the area of the circle?',
        expl=['The circle is tangent to the $x$-axis, so the radius to the point of tangency is vertical. Its length is the distance from the center to the $x$-axis: 4 (the $y$ of the center without the sign).',
              'Area $=\\pi\\cdot4^2=16\\pi$.']),
    'geo37-core-p24': dict(
        stem='A square has center $(-2,\\ 1)$ and side $6$, and its sides are parallel to the coordinate axes. What are the coordinates of its upper-right vertex?',
        expl=['Half the side is 3. The upper-right vertex is 3 right and 3 up from the center.',
              '$(-2+3,\\ 1+3)=(1,\\ 4)$.']),
    'geo37-core-p25': dict(
        stem='The line $2x+3y=12$ and the two coordinate axes form a triangle. What is the area of the triangle?',
        expl=['Where the line cuts the $y$-axis, $x=0$: $3y=12$, so $y=4$. Where it cuts the $x$-axis, $y=0$: $2x=12$, so $x=6$.',
              'The triangle has legs 6 and 4 on the axes, so its area is $\\frac{6\\cdot4}{2}=12$.']),
    'geo37-core-p26': dict(
        stem='What is the shortest distance from the point $P(-3,\\ 7)$ to the line $y=-2$?',
        expl=['$y=-2$ is a horizontal line. The shortest way from $P$ to it is straight down (vertical).',
              'Distance $=7-(-2)=9$.']),
    'geo37-core-p27': dict(
        stem='Line $a$ passes through $(-2,\\ -1)$ and $(4,\\ 3)$. Line $b$ is parallel to $a$ and passes through $(3,\\ 8)$. At what point does $b$ intersect the $y$-axis?',
        expl=['Line $a$: from $(-2,\\ -1)$ to $(4,\\ 3)$ is 6 right and 4 up. So 3 right goes with 2 up.',
              'Line $b$ is parallel, so it has the same steps. From $(3,\\ 8)$ to the $y$-axis is 3 left, so 2 down: $(0,\\ 6)$.']),
}

NEWQ = {
    # --- reflections ---
    'q-r26-t37-03': dict(
        stem='The point $P(4,\\ -3)$ is reflected across the $x$-axis to $Q$. Then $Q$ is reflected across the $y$-axis to $R$. What is the length of $PR$?',
        choices=['$14$', '$8$', '$10$', '$6$'], correct=3,
        expl=['Across the $x$-axis: $(x,\\ y)\\rightarrow(x,\\ -y)$, so $Q=(4,\\ 3)$.',
              'Across the $y$-axis: $(x,\\ y)\\rightarrow(-x,\\ y)$, so $R=(-4,\\ 3)$. (Two reflections, one across each axis, are the same as a reflection through the origin.)',
              'From $P(4,\\ -3)$ to $R(-4,\\ 3)$: 8 across and 6 up. $PR^2=8^2+6^2=100$, so $PR=10$ (the triple 6-8-10).',
              'Trap: $14=8+6$ adds the legs.']),
    # --- midpoint ---
    'q-r26-t37-05': dict(  # guided
        stem='$M(2,\\ -1)$ is the midpoint of segment $AB$. Given: $A(-4,\\ 3)$. What are the coordinates of $B$?',
        choices=['$(-1,\\ 1)$', '$(8,\\ -5)$', '$(-10,\\ 7)$', '$(6,\\ -4)$'], correct=2,
        expl=['From $A(-4,\\ 3)$ to $M(2,\\ -1)$: 6 right and 4 down.',
              '$M$ is the middle, so $B$ is the same move again from $M$: $B=(2+6,\\ -1-4)=(8,\\ -5)$.',
              'Check with the averages: $\\frac{-4+8}{2}=2$ and $\\frac{3+(-5)}{2}=-1$. That is $M$.']),
    'q-r26-t37-06': dict(
        stem='Given: $A(-3,\\ 5)$ and $B(7,\\ -1)$. $M$ is the midpoint of $AB$. What is the distance from $M$ to the origin?',
        choices=['$\\sqrt{34}$', '$2$', '$4$', '$2\\sqrt2$'], correct=4,
        expl=['The midpoint: the average of the $x$ values and the average of the $y$ values.',
              '$M=\\left(\\frac{-3+7}{2},\\ \\frac{5+(-1)}{2}\\right)=(2,\\ 2)$.',
              'From $O$ to $M$: 2 right and 2 up, a 45-45-90 triangle. So $OM=2\\sqrt2$.',
              'Trap: $\\frac{7-(-3)}{2}=5$ and $\\frac{-1-5}{2}=-3$ are half of the moves, not the midpoint. They give $\\sqrt{34}$.']),
    # --- the line equation ---
    'q-r26-t37-07': dict(  # guided
        stem='The line $4x+3y=24$ intersects the $x$-axis at $A$ and the $y$-axis at $B$. What is the length of $AB$?',
        choices=['$14$', '$2\\sqrt7$', '$10$', '$24$'], correct=3,
        expl=['On the $x$-axis, $y=0$: $4x=24$, so $x=6$ and $A=(6,\\ 0)$.',
              'On the $y$-axis, $x=0$: $3y=24$, so $y=8$ and $B=(0,\\ 8)$.',
              '$OA=6$ and $OB=8$ are the legs of a right triangle with the right angle at $O$. $AB$ is the hypotenuse: 6-8-10, so $AB=10$.',
              'Traps: $14=6+8$ adds the legs, and $24=\\frac{6\\cdot8}{2}$ is the area.']),
    'q-r26-t37-09': dict(
        stem='The line $y=-2x+b$ passes through the point $(3,\\ 1)$. At what point does the line intersect the $x$-axis?',
        choices=['$(0,\\ 7)$', '$(-3.5,\\ 0)$', '$(7,\\ 0)$', '$(3.5,\\ 0)$'], correct=4,
        expl=['Put the point into the equation: $1=-2\\cdot3+b$, so $b=7$. The line is $y=-2x+7$.',
              'On the $x$-axis, $y=0$: $0=-2x+7$, so $x=3.5$.',
              'The point is $(3.5,\\ 0)$. Trap: $(0,\\ 7)$ is where the line cuts the $y$-axis.']),
    # --- area of a slanted triangle: the box method ---
    'q-r26-t37-10': dict(  # guided
        stem='The vertices of triangle $ABC$ are $A(-2,\\ 1)$, $B(4,\\ -1)$ and $C(2,\\ 5)$. What is the area of the triangle?',
        choices=['$18$', '$20$', '$36$', '$16$'], correct=4,
        expl=['No side is horizontal or vertical, so draw a box around the triangle with sides parallel to the axes.',
              'The box goes from $x=-2$ to $x=4$ (width 6) and from $y=-1$ to $y=5$ (height 6). Its area is $6\\cdot6=36$.',
              'Three right triangles fill the corners of the box outside $ABC$. $A$ to $B$: 6 across and 2 down, $\\frac{6\\cdot2}{2}=6$. $B$ to $C$: 2 across and 6 up, $\\frac{2\\cdot6}{2}=6$. $C$ to $A$: 4 across and 4 down, $\\frac{4\\cdot4}{2}=8$.',
              'Area of $ABC$: $36-(6+6+8)=16$.']),
    'q-r26-t37-11': dict(
        stem='The vertices of triangle $OBC$ are $O(0,\\ 0)$, $B(6,\\ 2)$ and $C(2,\\ 4)$. What is the area of the triangle?',
        choices=['$10$', '$12$', '$14$', '$24$'], correct=1,
        expl=['Box: from $x=0$ to $x=6$ and from $y=0$ to $y=4$. Its area is $6\\cdot4=24$.',
              'The corner triangles: $O$ to $B$: $\\frac{6\\cdot2}{2}=6$. $B$ to $C$: 4 across and 2 up, $\\frac{4\\cdot2}{2}=4$. $C$ to $O$: $\\frac{2\\cdot4}{2}=4$.',
              'Area: $24-(6+4+4)=10$.']),
    'q-r26-t37-12': dict(
        stem='The vertices of quadrilateral $ABCD$ are $A(0,\\ 2)$, $B(5,\\ 0)$, $C(6,\\ 4)$ and $D(2,\\ 6)$. What is the area of the quadrilateral?',
        choices=['$15$', '$18$', '$21$', '$24$'], correct=3,
        expl=['Box: from $x=0$ to $x=6$ and from $y=0$ to $y=6$. Its area is $6\\cdot6=36$. Each vertex lies on a side of the box.',
              'The four corner triangles: $A$ to $B$: $\\frac{5\\cdot2}{2}=5$. $B$ to $C$: $\\frac{1\\cdot4}{2}=2$. $C$ to $D$: $\\frac{4\\cdot2}{2}=4$. $D$ to $A$: $\\frac{2\\cdot4}{2}=4$.',
              'Area: $36-(5+2+4+4)=21$.']),
}


def _fig_q10(box=False):
    p = Plane(-3, 5, -2, 6)
    if box:
        for a, b in (((-2, -1), (4, -1)), ((4, -1), (4, 5)), ((4, 5), (-2, 5)), ((-2, 5), (-2, -1))):
            p.seg(a, b, ORANGE, 2, dash=True)
    p.poly([(-2, 1), (4, -1), (2, 5)])
    for (x, y) in ((-2, 1), (4, -1), (2, 5)): p.point(x, y)
    p.label(-2, 1, 'A (−2, 1)', dx=-10, dy=-4, anchor='end')
    p.label(4, -1, 'B (4, −1)', dx=10, dy=12, anchor='start')
    p.label(2, 5, 'C (2, 5)', dx=10, dy=-14, anchor='start')
    return p.svg(full=not box)


def _fig_box(step):
    p = Plane(-1, 8, -1, 7, grid=True, ticks=True)
    tri = [(1, 1), (7, 3), (3, 6)]
    if step == 2:
        p.poly([(1, 1), (7, 1), (7, 3)], '#fbe7d6', ORANGE, 1.5)
        p.poly([(7, 3), (7, 6), (3, 6)], '#fbe7d6', ORANGE, 1.5)
        p.poly([(3, 6), (1, 6), (1, 1)], '#fbe7d6', ORANGE, 1.5)
        p.label(5.6, 1.7, '6', size=20, color=ORANGE)
        p.label(6.0, 5.0, '6', size=20, color=ORANGE)
        p.label(1.7, 4.6, '5', size=20, color=ORANGE)
    for a, b in (((1, 1), (7, 1)), ((7, 1), (7, 6)), ((7, 6), (1, 6)), ((1, 6), (1, 1))):
        p.seg(a, b, ORANGE, 2.2, dash=True)
    p.poly(tri)
    for (x, y) in tri: p.point(x, y)
    p.label(1, 1, 'A (1, 1)', dx=8, dy=16, anchor='start')
    p.label(7, 3, 'B (7, 3)', dx=10, dy=0, anchor='start')
    p.label(3, 6, 'C (3, 6)', dx=0, dy=-18)
    return p.svg()


def _fig_cut():
    p = Plane(-1, 7, -1, 5, grid=True, ticks=True)
    p.seg((-1, 3.6), (6.5, -0.9), TEAL, 3)
    p.point(0, 3); p.point(5, 0)
    p.label(0, 3, '(0, 3)', dx=12, dy=-14, anchor='start')
    p.label(5, 0, '(5, 0)', dx=10, dy=-16, anchor='start')
    return p.svg()


def _quad_figs(base):
    """Quadrants and reflections, drawn on the grid plane of video 1 (origin (320, 193.273), unit 26.545)."""
    u, ox, oy = 26.545454, 320.0, 193.272727
    P = lambda x, y: (ox + u * x, oy - u * y)
    q = []
    for x, y, s in ((3.4, 4.2, 'I'), (-3.4, 4.2, 'II'), (-3.4, -2.2, 'III'), (3.4, -2.2, 'IV')):
        q.append(_text(P(x, y)[0], P(x, y)[1], s, 26, color=TEAL, halo=True))
    for x, y, s in ((3.4, 3.2, '(+, +)'), (-3.4, 3.2, '(−, +)'), (-3.4, -3.2, '(−, −)'), (3.4, -3.2, '(+, −)')):
        q.append(_text(P(x, y)[0], P(x, y)[1], s, 20, halo=True))
    quad = _append(base, *q)
    r = [_line(*(P(4, 2) + P(4, -2)), color=ORANGE, w=1.6, dash=True),
         _line(*(P(4, 2) + P(-4, 2)), color=ORANGE, w=1.6, dash=True),
         _line(*(P(4, 2) + P(-4, -2)), color=ORANGE, w=1.6, dash=True)]
    for x, y in ((4, 2), (4, -2), (-4, 2), (-4, -2)): r.append(_dot(*P(x, y)))
    r += [_text(P(4, 2)[0] + 10, P(4, 2)[1] - 12, 'P (4, 2)', 18, 'start', halo=True),
          _text(P(4, -2)[0] + 10, P(4, -2)[1] + 12, '(4, −2)', 18, 'start', halo=True),
          _text(P(-4, 2)[0] - 10, P(-4, 2)[1] - 12, '(−4, 2)', 18, 'end', halo=True),
          _text(P(-4, -2)[0] - 10, P(-4, -2)[1] + 12, '(−4, −2)', 18, 'end', halo=True)]
    refl = _append(base, *r)
    return quad, refl


def _extend(M, vid, n, extra):
    """Rebuild a slide with its current script plus extra script items."""
    b = M.slide(vid, n); script = []
    for l in b['lines']:
        if 'say' in l: script.append(l['say'])
        elif 'appear' in l: script.append(A(l['label'], b['items'][l['appear']]))
        else: script.append(D(l['draw']))
    M.set_slide(vid, n, script=script + extra)


# ================================================================================================
def apply(M):
    # ---------------------------------------------------------------------------------------------
    # 0. Figures: labels, giveaways (p10, p25), overlaps (Q3, Q4, Q5, Q8, v722, slope video, p02...)
    # ---------------------------------------------------------------------------------------------
    _all_figures(M)
    V1 = 'geo-154'
    for n, keep in ((5, 'A'), (6, 'B'), (7, 'C')):
        b = M.slide(V1, n)
        b['items'][0]['v']['svg'] = _split_points(b['items'][0]['v']['svg'], keep)
        for l in b['lines']:
            if l.get('appear') == 0: l['label'] = 'The plane with point %s appears' % keep
    M.touched_videos.add(V1)

    # ---------------------------------------------------------------------------------------------
    # 1. Video 1 "The Coordinate Plane": quadrants and reflections (new slides 8 and 9)
    # ---------------------------------------------------------------------------------------------
    base = M.slide(V1, 2)['items'][0]['v']['svg']
    fig_quad, fig_refl = _quad_figs(base)
    M.insert_slides(V1, 7, [
        dict(mode='concept', title='Four quadrants', script=[
            A('The four quadrants appear', VIS(fig_quad)),
            "The two axes cut the plane into four parts. They're called quadrants.",
            "We number them counterclockwise, starting at the top right.",
            D('Point to each quadrant and say its signs'),
            "The first quadrant, top right: x positive, y positive. Plus, plus.",
            "The second, top left: minus, plus. The third, bottom left: minus, minus. The fourth, bottom right: plus, minus.",
            A("'I (+,+) · II (−,+) · III (−,−) · IV (+,−)' appears",
              T('I $(+,+)$ · II $(-,+)$ · III $(-,-)$ · IV $(+,-)$', size=44, x=410, y=650)),
            "Our A was in the first quadrant, B in the second, C in the third.",
            "And a point on an axis is in no quadrant at all.",
        ]),
        dict(mode='concept', title='Reflections', script=[
            A('P (4, 2) and its three reflections appear', VIS(fig_refl)),
            "Questions also flip a point across an axis. That's a reflection — like a mirror.",
            "Take P, (4, 2). Across the x-axis it goes down to (4, minus 2). Only y changes its sign.",
            A("'Across the x-axis: (x, −y) · across the y-axis: (−x, y)' appears",
              T('Across the $x$-axis: $(x,\\ -y)$ · across the $y$-axis: $(-x,\\ y)$', size=38, x=410, y=650, w=1100)),
            "Across the y-axis it goes to (minus 4, 2). Only x changes its sign.",
            A("'Through the origin: (−x, −y)' appears", T('Through the origin: $(-x,\\ -y)$', size=38, x=410, y=730, w=1100)),
            "Through the origin both signs change: (minus 4, minus 2).",
            "Here's the trap. Across the x-axis, it's the y that changes. The mirror is the x-axis — the point jumps over it, up or down.",
        ]),
    ])
    M.set_sidebar(V1, ['The two axes', 'The origin', '(x, y): x first', 'Reading a point', 'A negative x', 'Both negative',
                       'Four quadrants', 'Reflections', 'On an axis'])
    _renumber_active(M, V1)

    # Pass 2: the guided "which quadrant" question q-r26-t37-01 (+ its video) is removed (approved plan).
    NQ = NEWQ
    def mk(qid, figure=None):
        d = NQ[qid]
        M.new_q(qid, TOPIC, d['stem'], d['choices'], d['correct'], d['expl'], figure=figure)

    # ---------------------------------------------------------------------------------------------
    # 2. "Lengths on the Plane": roots in the answers (strong-student shortcut)
    # ---------------------------------------------------------------------------------------------
    _extend(M, 'geo-155', 8, [
        A("'Roots in the answers? Compare across² + up²' appears",
          T('Roots in the answers? Compare across$^2+$ up$^2$ with the number under the root', size=36)),
        "One more shortcut. Sometimes the answers are roots, like root 72.",
        "Then don't take the root at all. Across squared plus up squared — and look for that number under the root.",
    ])

    # ---------------------------------------------------------------------------------------------
    # 3. New short lesson after Question 1: area of a slanted triangle (box method) + guided question
    # ---------------------------------------------------------------------------------------------
    box = M.new_video('r26-t37-box', TOPIC, 'Area of a Slanted Triangle', ['Box it in', 'Subtract the corners', 'When to use it'], [
        dict(mode='title', title='Area of a Slanted Triangle', script=[
            "One more tool for triangles on the plane.",
            "In Question 1, one side was horizontal. That made the base and the height easy. What if no side is?",
        ]),
        dict(mode='concept', active=0, title='Box it in', script=[
            A('Triangle ABC in its box appears', VIS(_fig_box(1))),
            "Here's triangle ABC: A is (1, 1), B is (7, 3), C is (3, 6).",
            "No side is horizontal, and no side is vertical. The height is hard to find.",
            "So we put the triangle in a box — a rectangle with sides parallel to the axes.",
            D('Trace the box through A, B and C'),
            "Width: from x = 1 to x = 7 — 6. Height: from y = 1 to y = 6 — 5.",
            A("'Box: 6 · 5 = 30' appears", T('Box: $6\\cdot5=30$', size=46, x=410, y=650)),
        ]),
        dict(mode='concept', active=1, title='Subtract the corners', script=[
            A('The three corner triangles appear', VIS(_fig_box(2))),
            "The box is bigger than the triangle. What's extra? Three right triangles in the corners.",
            "Their legs lie on the box — so their areas are easy.",
            "A to B: 6 across, 2 up. 6 times 2, over 2 — 6.",
            "B to C: 4 across, 3 up — 6. C to A: 2 across, 5 down — 5.",
            A("'Corners: 6 + 6 + 5 = 17' appears", T('Corners: $6+6+5=17$', size=44, x=410, y=650)),
            A("'Triangle: 30 − 17 = 13' appears", T('Triangle: $30-17=13$', size=44, x=410, y=730)),
            "The triangle: 30 minus 17 — 13.",
        ]),
        dict(mode='concept', active=2, title='When to use it', script=[
            A("'A side on a grid line → base × height ÷ 2' appears",
              T('A horizontal or vertical side $\\rightarrow$ base $\\times$ height $\\div 2$', size=40)),
            "If one side is horizontal or vertical — like in Question 1 — use it as the base. The height is a straight drop.",
            A("'No such side → box it, subtract the corners' appears", T('No such side $\\rightarrow$ box it in, subtract the corners', size=40)),
            "No such side? Box it in and subtract the corners.",
            A("'Works for any polygon whose vertices touch the box' appears",
              T('Works for any polygon whose vertices all touch the box', size=36)),
            "It works for a quadrilateral too — as long as every vertex touches the box.",
        ]),
    ], LEARN, after='solve-geo37-g156')
    box['hybrid']['num'] = M.video('solve-geo37-g156')['hybrid'].get('num', 0)
    mk('q-r26-t37-10', figure=_fig_q10())
    M.place_q('q-r26-t37-10', LEARN, after='r26-t37-box')
    FQ10 = dict(type='geometry', svg=_fig_q10(box=True))
    _solution(M, 'q-r26-t37-10', 'The area of a slanted triangle: the box method', [
        "A triangle with no horizontal side. Box it in.",
    ], [
        ('Box it in', [
            "Triangle ABC. No side is horizontal or vertical, so there's no easy base and height.",
            "Use the box: a rectangle around the triangle, with sides parallel to the axes.",
            D('Trace the dashed box through A, B and C'),
            "Its width: from x = minus 2 to x = 4 — 6. Its height: from y = minus 1 to y = 5 — 6.",
            A("'Box: 6 · 6 = 36' appears", T('Box: $6\\cdot6=36$', size=34, x=1060, y=250, w=470)),
        ], [Q('q-r26-t37-10', fig=FQ10, figw=0.56, figalign='left')]),
        ('Subtract the corners', [
            "Around the triangle, three right triangles fill the corners of the box.",
            "A to B: 6 across, 2 down. 6 times 2, over 2 — 6.",
            A("'6 · 2 ÷ 2 = 6' appears", T('$A\\to B$: $\\frac{6\\cdot2}{2}=6$', size=34, x=1060, y=250, w=470)),
            "B to C: 2 across, 6 up — 6.",
            A("'2 · 6 ÷ 2 = 6' appears", T('$B\\to C$: $\\frac{2\\cdot6}{2}=6$', size=34, x=1060, y=320, w=470)),
            "C to A: 4 across, 4 down — 8.",
            A("'4 · 4 ÷ 2 = 8' appears", T('$C\\to A$: $\\frac{4\\cdot4}{2}=8$', size=34, x=1060, y=390, w=470)),
            A("'36 − 20 = 16' appears", T('$36-(6+6+8)=16$', size=34, x=1060, y=460, w=470)),
            "36 minus 20 — 16.",
            D('Circle choice 4'),
            "Choice four. The traps: 20 is the corners, and 36 is the whole box.",
        ], [Q('q-r26-t37-10', fig=FQ10, figw=0.56, figalign='left')]),
    ])

    # ---------------------------------------------------------------------------------------------
    # 4. Circles video + Question 2 video: small wording fixes
    # ---------------------------------------------------------------------------------------------
    _say(M, 'geo-157', 3, 'if the circle is tangent to both x and y, the centre must have the same x and y.',
         'in the first quadrant, a circle tangent to both axes has a center with the same x and y.')
    _say(M, 'solve-geo37-g158', 4, "30 out of 360 is a twelfth. 90 holds three 30s — three, three, three, three — 12. Or just 360 divided by 30.",
         "30 out of 360 is a twelfth: 360 divided by 30 is 12.")

    # ---------------------------------------------------------------------------------------------
    # 5. Slope video: midpoint, stairs going down, the line equation, cutting the axes
    # ---------------------------------------------------------------------------------------------
    SV = 'geo-159'
    stair_vis = dict(M.slide(SV, 4)['items'][0])
    M.insert_slides(SV, 4, [dict(mode='concept', title='Midpoint', pre=[stair_vis], script=[
        "These stairs give us one more thing: the midpoint.",
        "B is exactly halfway between A and C — one step from each.",
        A("'Midpoint = average of the x values, average of the y values' appears",
          T('Midpoint: the average of the $x$ values, the average of the $y$ values', size=38, x=410, y=650, w=1100)),
        "The rule: the midpoint is the average of the x values and the average of the y values.",
        D('Write "(−8 + 0) ÷ 2 = −4 and (0 + 6) ÷ 2 = 3"'),
        "Minus 8 plus 0, over 2 — minus 4. 0 plus 6, over 2 — 3. B is (minus 4, 3). Same as the stairs.",
        A("'One end and the midpoint → repeat the move' appears",
          T('One end and the midpoint known? Repeat the move', size=38, x=410, y=730, w=1100)),
        "And the other way around: you know A and the midpoint B? Just repeat the move.",
        "A to B is 4 right and 3 up. Do it again from B — and you're at C.",
    ])])
    # Pass 2: the "Stairs going down" slide (negative slope) is removed (approved plan).
    n_end = len(M.video(SV)['beats'])
    M.insert_slides(SV, n_end, [
        dict(mode='concept', title='The line equation', script=[
            "Some questions give the line as an equation. You need only two ideas.",
            A("'y = mx + b' appears", T('$y=mx+b$', size=56)),
            A("'m = the slope' appears", T('$m$ = the slope: up $\\div$ across, with its sign', size=40)),
            "m is the slope — the step: up divided by across.",
            A("'b = where the line cuts the y-axis' appears", T('$b$ = where the line cuts the $y$-axis: the point $(0,\\ b)$', size=40)),
            "b is where the line cuts the y-axis. At x = 0, y is b.",
            A("'y = −2: horizontal · x = 4: vertical' appears", T('$y=-2$: horizontal $\\cdot$ $x=4$: vertical', size=40)),
            "Two special lines: y = minus 2 is horizontal — every point on it has y = minus 2. And x = 4 is vertical.",
        ]),
        dict(mode='concept', title='Cutting the axes', script=[
            A('The line 3x + 5y = 15 appears', VIS(_fig_cut())),
            "The most common line question: where does the line cut the axes?",
            A("'x-axis: put y = 0 · y-axis: put x = 0' appears",
              T('On the $x$-axis: put $y=0$ · on the $y$-axis: put $x=0$', size=38, x=410, y=650, w=1100)),
            "On the x-axis, y is 0. On the y-axis, x is 0. Put them into the equation.",
            D('Write "3x + 5y = 15: y = 0 → x = 5; x = 0 → y = 3"'),
            "Take 3x plus 5y equals 15. Put y = 0: 3x = 15, and x = 5. The point (5, 0).",
            "Put x = 0: 5y = 15, and y = 3. The point (0, 3).",
            A("'Legs 5 and 3 → area 7.5' appears", T('Legs $5$ and $3$ $\\rightarrow$ area $\\frac{5\\cdot3}{2}=7.5$', size=38, x=410, y=740, w=1100)),
            "Now it's ordinary geometry: a right triangle with legs 5 and 3. Its area is 7.5. Its long side — Pythagoras.",
        ]),
    ])
    M.set_sidebar(SV, ['Slope is constant', 'Equal steps', 'Step size', 'Midpoint', 'The length AD', 'Slope is a ratio',
                       'Through the origin', 'Same multiplier', 'Negative side too', 'Other lines',
                       'The line equation', 'Cutting the axes'])
    _renumber_active(M, SV)

    # ---------------------------------------------------------------------------------------------
    # 6. Question 3 video: logic of the signs, plug-in shortcut first, clearer reason
    # ---------------------------------------------------------------------------------------------
    S3 = 'solve-geo37-g160'
    _say(M, S3, 2, "A is (−2a, −2b) — so a and b are positive, because A is in the negative region.",
         "A is (−2a, −2b). We are given that a and b are positive — so A is in the third quadrant, bottom left.")
    _say(M, S3, 3, "If a ≠ b, once I raise them to a power I can't cancel down to a over b.",
         "Cubing does not keep the ratio when a ≠ b. We'll see exactly why at the end.")
    _item(M, S3, 5, '$a=2,\\ b=3$: $\\ 2:3$ vs $8:27$', '$a=2,\\ b=3$: $\\ \\frac23$ vs $\\frac{8}{27}$',
          'a = 2, b = 3: 2/3 vs 8/27')
    M.insert_slides(S3, 2, [dict(mode='question', active=0, title='Plug in numbers',
                                 pre=[Q('geo37-g160', figw=0.56, figalign='left')], script=[
        "Before the algebra — the fast way for strong students: plug in numbers.",
        "Take a = 1 and b = 2. They're positive, and they're different.",
        A("'a = 1, b = 2: A(−2, −4)' appears", T('$a=1,\\ b=2$: $\\ A(-2,\\ -4)$', size=34, x=1060, y=250, w=470)),
        "Then A is (minus 2, minus 4). On this line, y is always twice x.",
        A("'(1, 8) ✗' appears", T('$(1,\\ 8)$ ✗', size=34, x=1060, y=320, w=470)),
        "Choice 1: (1, 8). 8 is not twice 1. Off the line.",
        A("'(3, 6) ✓ (1/2, 1) ✓ (1/2, 1) ✓' appears", T('$(3,\\ 6)$ ✓ $\\ (\\frac12,\\ 1)$ ✓ $\\ (\\frac12,\\ 1)$ ✓', size=34, x=1060, y=390, w=470)),
        "Choice 2: (3, 6). Choices 3 and 4 both give (one half, 1). All three are on the line.",
        "Only choice 1 is off the line. Ten seconds. Now let's see why, with the letters.",
    ])])

    # ---------------------------------------------------------------------------------------------
    # 7. Guided questions after Question 3: midpoint, and a line equation with a negative slope
    # ---------------------------------------------------------------------------------------------
    mk('q-r26-t37-05')
    M.place_q('q-r26-t37-05', LEARN, after=S3)
    _solution(M, 'q-r26-t37-05', 'From one end and the midpoint to the other end', [
        "A midpoint question. Repeat the move.",
    ], [
        ('Repeat the move', [
            "M is the midpoint of AB. We know A and M. Where is B?",
            "Think of stairs. From A to M is one move. From M to B is the same move again.",
            "From A to M: x goes from minus 4 to 2 — 6 right. y goes from 3 to minus 1 — 4 down.",
            A("'A → M: 6 right, 4 down' appears", T('$A\\to M$: 6 right, 4 down', size=36, x=410, y=260, w=1100)),
            "The same move from M: 2 plus 6 is 8. Minus 1 minus 4 is minus 5.",
            A("'B = (2 + 6, −1 − 4) = (8, −5)' appears", T('$B=(2+6,\\ -1-4)=(8,\\ -5)$', size=36, x=410, y=330, w=1100)),
            D('Circle choice 2'),
            "B is (8, minus 5). Choice two.",
        ]),
        ('Check with the averages', [
            "Let's check with the midpoint rule: the average of the x values, and the average of the y values.",
            A("'(−4 + 8) ÷ 2 = 2 ✓ · (3 − 5) ÷ 2 = −1 ✓' appears",
              T('$\\frac{-4+8}{2}=2$ ✓ $\\cdot$ $\\frac{3+(-5)}{2}=-1$ ✓', size=36, x=410, y=260, w=1100)),
            "Minus 4 plus 8, over 2 — 2. 3 plus minus 5, over 2 — minus 1. That's M.",
            "The traps: (minus 1, 1) is the midpoint of A and M, not B. (6, minus 4) is only the move. And (minus 10, 7) goes the wrong way.",
        ]),
    ])
    mk('q-r26-t37-07')
    M.place_q('q-r26-t37-07', LEARN, after='solve-q-r26-t37-05')
    _solution(M, 'q-r26-t37-07', 'Where a line cuts the axes', [
        "A line given as an equation. Where does it cut the axes?",
    ], [
        ('Put 0 for x, then for y', [
            "The line 4x plus 3y equals 24. A is on the x-axis, B is on the y-axis. How long is AB?",
            "On the x-axis, y is 0. Put y = 0: 4x = 24, and x = 6.",
            A("'y = 0: 4x = 24 → A(6, 0)' appears", T('$y=0$: $4x=24$ $\\rightarrow$ $A(6,\\ 0)$', size=36, x=410, y=260, w=1100)),
            "On the y-axis, x is 0. Put x = 0: 3y = 24, and y = 8.",
            A("'x = 0: 3y = 24 → B(0, 8)' appears", T('$x=0$: $3y=24$ $\\rightarrow$ $B(0,\\ 8)$', size=36, x=410, y=330, w=1100)),
        ]),
        ('A right triangle', [
            "Now sketch it. A, B and the origin make a right triangle, with the right angle at the origin.",
            D('Sketch the axes, mark A at 6 and B at 8, and join them'),
            "The legs are 6 and 8. AB is the hypotenuse.",
            A("'6, 8 → AB = 10' appears", T('Legs $6,\\ 8$ $\\rightarrow$ $AB=10$', size=36, x=410, y=260, w=1100)),
            "6, 8, 10 — the triple 3, 4, 5 times 2. AB is 10.",
            D('Circle choice 3'),
            "Choice three.",
            "The traps: 14 adds the legs. 24 is the area. And 2 root 7 subtracts the squares instead of adding them.",
        ]),
    ])

    # ---------------------------------------------------------------------------------------------
    # 8. Question 6 video: remove the "Hebrew version" remark
    # ---------------------------------------------------------------------------------------------
    _say(M, 'solve-geo37-g164', 5,
         "In the Hebrew version we compared the top dark piece with a square. Here that's not reliable: the top piece is an eighth of the circle — 9 pi, about 28 — smaller than the 6-by-6 square.",
         "You may want to compare the top shaded piece with the 6-by-6 square. That's not reliable here: the top piece is an eighth of the circle — 9 pi, about 28 — smaller than the square, 36.")

    # ---------------------------------------------------------------------------------------------
    # 9. Question 8 video: fractions instead of ":", the equation remark now uses the taught y = mx + b
    # ---------------------------------------------------------------------------------------------
    S8 = 'solve-geo37-g166'
    # Pass 2: the original board and the original "If you prefer an equation" line are restored (clean-up only).
    _item(M, S8, 3, '$10:4=5:\\ ?$', '$\\frac{10}{4}=\\frac{5}{?}$', '10/4 = 5/? appears')
    _say(M, S8, 3, "If you prefer an equation: y equals two fifths x plus b; plug in A: 7 equals 2 plus b, so b is 5. Same answer.",
         "If you prefer an equation: y equals two fifths x plus b. Plug in A: 7 equals 2 plus b. So, b is 5. Same answer.")

    # ---------------------------------------------------------------------------------------------
    # 10. Question 9 video: the first board line was wrong ("they never meet")
    # ---------------------------------------------------------------------------------------------
    _item(M, 'solve-geo37-g167', 3,
          '1. Parallel to one axis $\\rightarrow$ perpendicular to the other — they never meet',
          '1. Parallel to an axis $\\rightarrow$ never meets that axis · perpendicular to the other axis',
          'Parallel to an axis → never meets it · perpendicular to the other appears')
    _say(M, 'solve-geo37-g167', 3, "A line parallel to one axis is necessarily perpendicular to the other.",
         "A line parallel to one axis never meets that axis — unless it lies on it. And it is necessarily perpendicular to the other axis.")

    # ---------------------------------------------------------------------------------------------
    # 11. Memory card
    # ---------------------------------------------------------------------------------------------
    c = M.card('mem-coordinates')
    rows = c['tables'][0]['rows']

    def after(label, new_rows):
        k = [i for i, r in enumerate(rows) if r[0] == label][0]
        rows[k + 1:k + 1] = new_rows
    after('!A point', [
        ['!Quadrants', 'I $(+,+)$ · II $(-,+)$ · III $(-,-)$ · IV $(+,-)$ · a point on an axis is in no quadrant'],
        ['Reflection', 'across the $x$-axis $(x,\\ -y)$ · across the $y$-axis $(-x,\\ y)$ · through the origin $(-x,\\ -y)$']])
    after('!Slanted segment', [
        ['!Midpoint', 'the average of the $x$ values, the average of the $y$ values · or repeat the move from one end'],
        ['Slanted triangle area', 'box it in (sides parallel to the axes), subtract the corner right triangles']])
    after('Straight line', [
        ['!Parallel lines', 'the same slope: the same step across and the same step up'],
        ['Line equation', '$y=mx+b$: $m$ = slope, $b$ = where it cuts the $y$-axis · $x$-axis: put $y=0$ · $y$-axis: put $x=0$']])
    c['tips'] += ['Answers given as roots? Compare across$^2+$ up$^2$ with the number under the root. No need to take the root.',
                  'Letters in the question? Plug in easy numbers (for example $a=1$, $b=2$) and check each choice.']

    # ---------------------------------------------------------------------------------------------
    # 12. Question texts: TeX, stacked data, full worked solutions with numbers
    # ---------------------------------------------------------------------------------------------
    for qid, d in QTEXT.items():
        M.set_q(qid, stem=d.get('stem'), choices=d.get('choices'), expl=d.get('expl'))

    # ---------------------------------------------------------------------------------------------
    # 13. Practice: drop the near-duplicate p16, add new questions, order easy -> hard
    # ---------------------------------------------------------------------------------------------
    # Pass 2: geo37-core-p16 is restored; q-r26-t37-02, -04 (which quadrant) and -08 (negative slope) are removed.
    for qid in ('q-r26-t37-03', 'q-r26-t37-06', 'q-r26-t37-09', 'q-r26-t37-11', 'q-r26-t37-12'):
        mk(qid)
        M.place_q(qid, PRACTICE)
    P = lambda n: 'geo37-core-p%02d' % n
    R = lambda n: 'q-r26-t37-%02d' % n
    M.practice_order(PRACTICE, [
        P(8), P(21), P(24), P(23), P(1), P(19), P(5), P(6), P(22), P(2), P(26), P(3), P(10), P(9), P(14),
        P(20), P(27), P(25), P(4), R(6), R(11), P(16), P(7), P(12), P(13), R(3), R(9), P(11), P(17), P(15), P(18),
        R(12)])

    # ---------------------------------------------------------------------------------------------
    # Pass 2: summary lesson right before the practice
    # ---------------------------------------------------------------------------------------------
    summary(M)

    # ---------------------------------------------------------------------------------------------
    # 14. American spelling everywhere in the topic's videos and card
    # ---------------------------------------------------------------------------------------------
    _spelling(M)

    # ---------------------------------------------------------------------------------------------
    # 15. "(b,\\ -a)" rendered the minus as a binary operator ("(b, − a)"): make it a sign
    # ---------------------------------------------------------------------------------------------
    # and 16. no "so" meaning "therefore" in the middle of a sentence (solutions and spoken lines)
    fx = lambda t: t.replace(',\\ -', ',\\ {-}')
    so = lambda t: re.sub(r'(,| —) so (?!far|on\b)', '. So, ', t)
    for q in list(M.D['questions'].values()):
        if q['topic'] != TOPIC: continue
        st, ch, ex = q['stemRich'], q['choicesRich'], q.get('explanation') or []
        if fx(st) != st or any(fx(c) != c for c in ch) or any(so(fx(e)) != e for e in ex):
            M.set_q(q['id'], stem=fx(st), choices=[fx(c) for c in ch], expl=[so(fx(e)) for e in ex])
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            for l in b['lines']:
                if 'say' in l and so(l['say']) != l['say']:
                    l['say'] = so(l['say']); M.touched_videos.add(v['id'])
            for it in b['items']:
                if it.get('t') and fx(it['t']) != it['t']:
                    it['t'] = fx(it['t']); M.touched_videos.add(v['id'])


def _b(label, tex, size=40):
    """A board line that pops in (label = what the teacher sees in the script)."""
    return A("'%s' appears" % label, T(tex, size=size))


def summary(M):
    """Pass 2: a short summary lesson at the end of the learn section, right before the practice."""
    last = [f['ref'] for f in M.D['flow'] if f['section'] == LEARN][-1]
    sb = ['Points', 'Reflections', 'Along an axis', 'Slanted segments', 'Slanted triangles', 'Circles', 'Slope and midpoint',
          'Through the origin', 'Lines and axes', 'Before you practice']
    M.new_video('r26-t37-summary', TOPIC, 'Summary', sb, [
        dict(mode='title', title='Summary', script=[
            "A quick summary before you practice.",
            "Everything important about the coordinate plane."]),
        dict(title='Points', active=0, script=[
            _b('A(x, y): x first, y second', '$A(x,\\ y)$: $x$ first, $y$ second'),
            "x first, y second. Always. (7, 1) and (1, 7) are different points.",
            _b('On the x-axis: y = 0 · on the y-axis: x = 0', 'On the $x$-axis: $y=0$ · on the $y$-axis: $x=0$'),
            _b('I (+,+) · II (−,+) · III (−,−) · IV (+,−)', 'I $(+,+)$ · II $(-,+)$ · III $(-,-)$ · IV $(+,-)$'),
            "The four quadrants go counterclockwise from the top right. A point on an axis is in no quadrant."]),
        dict(title='Reflections', active=1, script=[
            _b('Across the x-axis: (x, −y) · across the y-axis: (−x, y)', 'Across the $x$-axis: $(x,\\ {-y})$ · across the $y$-axis: $(-x,\\ y)$'),
            "A reflection is a mirror. Across the x-axis, only y changes its sign. Across the y-axis, only x.",
            _b('Through the origin: (−x, −y)', 'Through the origin: $(-x,\\ {-y})$'),
            "Through the origin, both signs change. (3, 5) goes to (minus 3, minus 5)."]),
        dict(title='Along an axis', active=2, script=[
            _b('Same x → vertical · same y → horizontal', 'Same $x$ $\\rightarrow$ vertical · same $y$ $\\rightarrow$ horizontal'),
            "Same x? The segment is vertical — use the y values. Same y? It's horizontal — use the x values.",
            _b('Same side: subtract · opposite sides: add', 'Same side: subtract · opposite sides: add'),
            "Same side of the axis — subtract. Opposite sides — add the two parts.",
            _b('From x = −3 to x = 5: 3 + 5 = 8, not 5 − 3 = 2', 'From $x=-3$ to $x=5$: $3+5=8$, not $5-3=2$'),
            "5 minus 3 is the classic mistake."]),
        dict(title='Slanted segments', active=3, script=[
            _b('Slanted → right triangle → Pythagoras', 'Slanted $\\rightarrow$ right triangle $\\rightarrow$ Pythagoras'),
            "A slanted segment? Draw lines parallel to the axes and close a right triangle.",
            _b('Across 8, up 15 → 17', 'Across $8$, up $15$ $\\rightarrow$ $17$'),
            "Across 8, up 15. A triple — 17. No distance formula needed. It's just Pythagoras.",
            _b('Roots in the answers? Compare across² + up²', 'Roots in the answers? Compare across$^2+$ up$^2$'),
            "And if the answers are roots, don't take the root. Look for across squared plus up squared under the root."]),
        dict(title='Slanted triangles', active=4, script=[
            _b('A horizontal or vertical side → base × height ÷ 2', 'A horizontal or vertical side $\\rightarrow$ $\\frac{\\text{base}\\cdot\\text{height}}{2}$'),
            "The area of a triangle on the plane. Is one side horizontal or vertical? Use it as the base. The height is a straight drop.",
            _b('No such side → box it in, subtract the corners', 'No such side $\\rightarrow$ box it in, subtract the corners'),
            _b('24 − (6 + 4 + 4) = 10', 'Box $24$, corners $6+4+4$: $\\ 24-14=10$'),
            "Then subtract the three corner right triangles. Box 24, corners 14 — the triangle is 10."]),
        dict(title='Circles', active=5, script=[
            _b('Circle: find r first', 'Circle: find $r$ first'),
            "With a circle, find the radius first. Then the area, the circumference — whatever they ask.",
            _b('Center at O, point (6, 8) → r = 10', 'Center at $O$, point $(6,\\ 8)$ $\\rightarrow$ $r=10$'),
            "Center at the origin? Draw the radius to the point, close a right triangle, Pythagoras.",
            _b('Tangent to both axes: center (r, r) · center (8, 0) ≠ r = 8', 'Tangent to both axes: center $(r,\\ r)$ · center $(8,\\ 0)$ does not mean $r=8$', size=36),
            "Tangent to both axes: the distances to the axes, without the signs, both equal r.",
            "And a leg that is half the hypotenuse? A 30-60-90 triangle."]),
        dict(title='Slope and midpoint', active=6, script=[
            _b('Straight line: identical steps', 'Straight line: identical steps — the same across, the same up'),
            "A straight line has a constant slope. Cut it into equal pieces, and every step is the same.",
            _b('Slope = up ÷ across', 'Slope $=$ up $\\div$ across — a ratio, not a length'),
            "The slope is up divided by across. Parallel lines have the same step.",
            _b('Midpoint: the averages, or repeat the move', 'Midpoint: $\\left(\\frac{x_1+x_2}{2},\\ \\frac{y_1+y_2}{2}\\right)$ · or repeat the move'),
            "The midpoint: the average of the x values and the average of the y values.",
            "Or repeat the move from the midpoint."]),
        dict(title='Through the origin', active=7, script=[
            _b('(3, 1) → (6, 2) → (9, 3): both × the same number', '$(3,\\ 1)\\rightarrow(6,\\ 2)\\rightarrow(9,\\ 3)$: both $\\times$ the same number'),
            "A line through the origin: every point is one point with both values multiplied by the same number.",
            _b('Only for a line through the origin', 'Only for a line through the origin'),
            "This works only for a line through the origin. On other lines, compare the steps, not the points.",
            "Letters in the question? Plug in easy numbers, like a = 3 and b = 5."]),
        dict(title='Lines and axes', active=8, script=[
            _b('Never cuts an axis → parallel to it', 'Never cuts an axis $\\rightarrow$ parallel to it'),
            "A whole line that never cuts an axis is parallel to it. A line parallel to neither axis cuts each axis once.",
            _b('y = mx + b: b = where it cuts the y-axis', '$y=mx+b$: $m$ = slope, $b$ = where it cuts the $y$-axis'),
            "Some questions give a line as an equation: y = mx + b.",
            _b('x-axis: put y = 0 · y-axis: put x = 0', '$x$-axis: put $y=0$ · $y$-axis: put $x=0$'),
            "Where does it cut the axes? Put y = 0, then x = 0.",
            "Then it's ordinary geometry."]),
        dict(title='Before you practice', active=9, script=[
            "Before you practice, ask yourself these questions.",
            _b('x first? Which sign changes?', 'Did I read $x$ first? In a reflection, which sign changes?'),
            _b('Parallel to an axis? Same side or opposite sides?', 'Is the segment parallel to an axis? Same side or opposite sides?', size=36),
            _b('Slanted? Close a right triangle.', 'Slanted? Close a right triangle.'),
            _b('A circle? Find r first.', 'A circle? Find $r$ first.'),
            "The traps: 5 minus 3 instead of 3 plus 5. Adding the legs instead of Pythagoras.",
            "A center at (8, 0) is not a radius of 8. And across the x-axis, it's the y that changes.",
            "Good luck."]),
    ], LEARN, after=last)


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
    # --- "Area of a Slanted Triangle" (r26-t37-box, a lesson the Hebrew course does not have): every slide
    #     (box it in, subtract the corners, when to use it) is taught again by the very next video,
    #     solve-q-r26-t37-10. The lesson leaves the flow; its one extra fact moves into that video.
    M.unplace('r26-t37-box')
    _cr_add(M, 'solve-q-r26-t37-10', 3, 'Choice four. The traps',
            'The box works for a quadrilateral too — as long as every corner touches the box.',
            T('Works for a quadrilateral too', size=34, x=1060, y=530, w=470),
            "'Works for a quadrilateral too' appears")

    # --- "Slope": slide 5 (midpoint: repeat the move / the averages) is taught again in solve-q-r26-t37-05,
    #     slide 13 (where a line cuts the axes) in solve-q-r26-t37-07. Neither is in the Hebrew lesson.
    _cr_cut(M, 'geo-159', [5, 13])


_apply_before_cut = apply


def apply(M):
    _apply_before_cut(M)
    cut_repeats(M)


# ================================================================================================
# 2026-10-06 renumber pass (runs LAST, after cut_repeats). The English course must not look like the Hebrew one:
# every Hebrew-derived question (guided geo37-g156 ... g169, practice geo37-core-p01 ... p20) and every Hebrew-derived
# lesson example (videos geo-154, geo-155, geo-157, geo-159) gets new numbers (letter-only questions: new letters /
# axis / choice order). Idea, trap, level and methods stay. Every coordinate figure of a changed question or example is
# redrawn to the new points (true positions). Solution videos rewritten to match. Practice clean-up 32 -> 26.
# Nothing in topic 37 is recorded (checked ~/Documents/Course.recordings 2026-10-06), so RN_RECORDED is empty.
# ================================================================================================
import math
RN_RECORDED = set()
S3_ = math.sqrt(3)


class RPlane(Plane):
    """Plane + circles, arcs, right-angle marks; question figures use the full 640 x 360 frame."""

    def __init__(self, *a, no_o=False, **k):
        Plane.__init__(self, *a, **k); self.no_o = no_o

    def circle(self, x, y, r, color=INK, w=2.5, fill='none'):
        px, py = self.P(x, y)
        self.body.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s" stroke="%s" stroke-width="%s"/>' % (px, py, r * self.u, fill, color, w))

    def cdot(self, x, y, color=INK): self.body.append(_dot(*self.P(x, y), color=color))

    def arc(self, x, y, a1, a2, rpx=24, label=None, lr=None, color=TEAL):
        """Angle mark at (x, y) from direction a1 to a2 (degrees, counterclockwise, math convention)."""
        cx, cy = self.P(x, y)
        p1 = (cx + rpx * math.cos(math.radians(a1)), cy - rpx * math.sin(math.radians(a1)))
        p2 = (cx + rpx * math.cos(math.radians(a2)), cy - rpx * math.sin(math.radians(a2)))
        self.body.append('<path d="M %.3f %.3f A %.3f %.3f 0 0 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="2"/>' % (
            p1[0], p1[1], rpx, rpx, p2[0], p2[1], color))
        if label:
            m = math.radians((a1 + a2) / 2.0); lr = lr or rpx + 16
            self.body.append(_text(cx + lr * math.cos(m), cy - lr * math.sin(m), label, 18, color=color, halo=True))

    def right(self, x, y, d1, d2, s=11, color=TEAL):
        """Right-angle mark at (x, y) between unit directions d1, d2 (math coordinates)."""
        cx, cy = self.P(x, y)
        a = (cx + s * d1[0], cy - s * d1[1]); b = (a[0] + s * d2[0], a[1] - s * d2[1]); c = (cx + s * d2[0], cy - s * d2[1])
        self.body.append('<path d="M %.3f %.3f L %.3f %.3f L %.3f %.3f" fill="none" stroke="%s" stroke-width="1.6"/>' % (
            a[0], a[1], b[0], b[1], c[0], c[1], color))

    def svg(self, title='Coordinate plane', full=True):
        out = Plane.svg(self, title, full)
        if self.no_o: out = re.sub(r'<text [^>]*font-size="15">O</text>', '', out, count=1)
        return out


def _lab(p, x, y, s, dx=0, dy=0, anchor='middle', size=18, color=INK): p.label(x, y, s, dx, dy, anchor, size, color)


# ---- lesson figures ---------------------------------------------------------------------------------------
def rn_fig_point(base, x, y, name):
    """Video 1 grid plane (origin (320, 193.27), unit 26.545): one point with dashed lines to both axes."""
    u, ox, oy = 26.545454, 320.0, 193.272727
    P = lambda a, b: (ox + u * a, oy - u * b)
    px, py = P(x, y); dx = 10 if x > 0 else -10
    return _append(base, _line(px, py, px, oy, TEAL, 1.6, True), _line(px, py, ox, py, TEAL, 1.6, True), _dot(px, py),
                   _text(px + dx, py - 16 if y > 0 else py + 16, name, 18, 'start' if x > 0 else 'end', halo=True))


def rn_fig_pq():
    p = RPlane(-1, 6, -6, 5, grid=True, ticks=True)
    p.seg((4, 3), (4, -5), TEAL, 3); p.point(4, 3); p.point(4, -5)
    _lab(p, 4, 3, 'P (4, 3)', 10, -12, 'start'); _lab(p, 4, -5, 'Q (4, −5)', 10, 10, 'start')
    return _o_label(p.svg(full=False), 'ul')


def rn_fig_rs():
    p = RPlane(-1, 9, -1, 6, grid=True, ticks=True)
    p.seg((1, 4), (7, 4), TEAL, 3); p.point(1, 4); p.point(7, 4)
    _lab(p, 1, 4, 'R (1, 4)', 0, -18); _lab(p, 7, 4, 'S (7, 4)', 0, -18)
    return p.svg(full=False)


def rn_fig_uv():
    p = RPlane(-3, 8, -4, 13, grid=True)
    p.seg((-2, -3), (6, -3), ORANGE, 2, dash=True); p.seg((6, -3), (6, 12), ORANGE, 2, dash=True)
    p.right(6, -3, (-1, 0), (0, 1), 9, ORANGE)
    p.seg((-2, -3), (6, 12), TEAL, 3); p.point(-2, -3); p.point(6, 12)
    _lab(p, -2, -3, 'U (−2, −3)', -10, 4, 'end'); _lab(p, 6, 12, 'V (6, 12)', 10, 0, 'start')
    return _o_label(p.svg(full=False), 'dr')


def rn_fig_center_axis():
    p = RPlane(-1, 11, -5, 5)
    p.circle(5, 0, 4); p.cdot(5, 0); p.point(9, 0)
    _lab(p, 5, 0, 'C (5, 0)', 0, -16); _lab(p, 9, 0, 'P (9, 0)', 10, 16, 'start')
    return p.svg(full=False)


def rn_fig_origin_circle():
    p = RPlane(-27, 27, -27, 27)
    p.circle(0, 0, 26)
    p.seg((10, 24), (10, 0), TEAL, 1.6, dash=True); p.seg((10, 24), (0, 24), TEAL, 1.6, dash=True)
    p.seg((0, 0), (10, 24), TEAL, 2.5); p.point(10, 24)
    _lab(p, 10, 24, 'A (10, 24)', 10, -12, 'start')
    return p.svg(full=False)


def rn_fig_stairs():
    p = RPlane(-28, 16, -3, 19)
    p.seg((-26.4, -1), (14.4, 16), TEAL, 2.5)
    for a, b in (((-24, 0), (-12, 0)), ((-12, 0), (-12, 5)), ((-12, 5), (0, 5)), ((0, 5), (0, 10)),
                 ((0, 10), (12, 10)), ((12, 10), (12, 15))):
        p.seg(a, b, ORANGE, 1.8, dash=True)
    for x, y in ((-24, 0), (-12, 5), (0, 10), (12, 15)): p.point(x, y)
    _lab(p, -24, 0, 'A (−24, 0)', -6, -16, 'end'); _lab(p, -12, 5, 'B', -6, -16, 'end')
    _lab(p, 0, 10, 'C (0, 10)', -8, -16, 'end'); _lab(p, 12, 15, 'D', -8, -16, 'end')
    return p.svg(full=False)


def rn_fig_origin_line():
    p = RPlane(-5, 11, -4, 8)
    p.seg((-4.5, -3), (10.5, 7), TEAL, 2.5)
    for x, y, s in ((3, 2, 'P (3, 2)'), (6, 4, 'Q (6, 4)'), (9, 6, 'R (9, 6)'), (-3, -2, 'S (−3, −2)')):
        p.seg((x, y), (x, 0), TEAL, 1.4, dash=True); p.seg((x, y), (0, y), TEAL, 1.4, dash=True); p.point(x, y)
        if x > 0: _lab(p, x, y, s, 8, -14, 'end')
        else: _lab(p, x, y, s, -10, 4, 'end')
    return _o_label(p.svg(full=False), 'dr')


# ---- guided question figures -------------------------------------------------------------------------------
def rn_fig_g156():
    p = RPlane(-21, 14, -10, 18)
    p.poly([(5, 16), (-19, -8), (12, -8)], 'none', TEAL)
    for x, y in ((5, 16), (-19, -8), (12, -8)): p.point(x, y)
    _lab(p, 5, 16, 'A (5, 16)', 10, -6, 'start', 20); _lab(p, -19, -8, 'B (−19, −8)', 0, 18, 'middle', 20)
    _lab(p, 12, -8, 'C (12, −8)', 0, 18, 'middle', 20)
    return p.svg()


def rn_fig_g158():
    p = RPlane(-9, 9, -9, 9)
    p.circle(0, 0, 8); ax, ay = 4 * S3_, 4
    p.seg((0, 0), (8, 0), TEAL, 2.5); p.seg((0, 0), (ax, ay), TEAL, 2.5); p.point(ax, ay)
    p.arc(0, 0, 0, 30, 30, 'α', 44)
    _lab(p, 4, 0, '8', 0, 18, 'middle', 20); _lab(p, ax, ay, 'A (x, 4)', 12, -10, 'start', 20)
    return p.svg()


def rn_fig_g160():
    p = RPlane(-4, 3, -7, 5)
    p.seg((-3.4, -6.8), (2.4, 4.8), TEAL, 2.5)
    for x, y in ((-3, -6), (1.5, 3)):
        p.seg((x, y), (x, 0), TEAL, 1.4, dash=True); p.seg((x, y), (0, y), TEAL, 1.4, dash=True); p.point(x, y)
    _lab(p, -3, -6, 'A (−3p, −3q)', -10, 0, 'end', 20); _lab(p, 1.5, 3, 'B (x, y)', 10, 4, 'start', 20)
    s = p.svg(); return _o_label(s, 'dr')


def rn_fig_g162():
    p = RPlane(-6, 12, -5, 5, no_o=True)
    p.poly([(4, 3), (10, 3), (10, -3), (-4, -3)], 'none', INK)
    p.right(10, 3, (-1, 0), (0, -1)); p.right(10, -3, (-1, 0), (0, 1))
    for x, y in ((4, 3), (10, 3), (10, -3), (-4, -3)): p.point(x, y)
    _lab(p, 4, 3, 'A (4, 3)', -4, -16, 'middle', 20); _lab(p, 10, 3, 'D (10, 3)', 8, -16, 'middle', 20)
    _lab(p, 10, -3, 'C', 10, 16, 'start', 20); _lab(p, -4, -3, 'B', -10, 16, 'end', 20)
    _lab(p, 0, 0, 'E', 14, 14, 'middle', 16)
    return p.svg()


def rn_fig_g163():
    p = RPlane(-6, 5, -1, 10)
    p.poly([(-4, 2), (2, 2), (2, 9), (-4, 9)], FILL, TEAL)
    p.seg((2, 2), (2, 9), ORANGE, 3)
    _lab(p, -4, 2, '(−4, 2)', -8, 0, 'end', 20); _lab(p, 2, 9, '(2, 9)', 8, -12, 'start', 20)
    _lab(p, 3, 5.5, '↻', 0, 0, 'middle', 26)
    return p.svg()


def rn_fig_g164():
    R = 8 * math.sqrt(2)
    p = RPlane(-12.5, 12.5, -12.5, 12.5)
    t = p.P(0, R); b = p.P(0, -R); r = R * p.u
    p.body.append('<path d="M %.3f %.3f A %.3f %.3f 0 0 1 %.3f %.3f Z" fill="%s" stroke="none"/>' % (t[0], t[1], r, r, b[0], b[1], FILL))
    p.poly([(0, 0), (8, 8), (0, -R)], 'white', TEAL)
    p.seg((0, 0), (0, R), TEAL, 2.5)
    p.circle(0, 0, R); p.point(8, 8); p.point(0, -R)
    _lab(p, 8, 8, 'A (8, 8)', 10, -12, 'start', 20); _lab(p, 0, -R, 'B', -12, 14, 'end', 20)
    s = p.svg(); return _o_label(s, 'ul')


def rn_fig_g165():
    h = 4 * S3_
    V = {'C': (4, 0), 'D': (12, 0), 'E': (16, h), 'F': (12, 2 * h), 'A': (4, 2 * h), 'B': (0, h)}
    p = RPlane(-3, 19, -2, 15)
    p.poly([V[k] for k in 'CDEFAB'], FILL, TEAL)
    p.poly([V['A'], V['F'], V['E']], 'white', TEAL)
    off = {'A': (-6, -14, 'end'), 'F': (6, -14, 'start'), 'E': (10, 0, 'start'), 'D': (6, 16, 'start'), 'B': (-10, 0, 'end')}
    for k, (dx, dy, an) in off.items(): _lab(p, V[k][0], V[k][1], k, dx, dy, an, 20)
    _lab(p, 4, 0, 'C (4, 0)', -2, 18, 'middle', 20)
    s = p.svg(); return _o_label(s, 'ul')


def rn_fig_g166():
    p = RPlane(-1, 10, -1, 12)
    p.seg((-0.6, -0.45), (9.6, 7.2), TEAL, 2.5); p.seg((-0.6, 6.55), (6.4, 11.8), ORANGE, 2.5)
    for x, y in ((4, 10), (8, 6)):
        p.seg((x, y), (x, 0), TEAL, 1.4, dash=True); p.seg((x, y), (0, y), TEAL, 1.4, dash=True); p.point(x, y)
    p.point(0, 7)
    _lab(p, 4, 10, 'A (4, 10)', 8, -14, 'end', 20); _lab(p, 8, 6, 'C (8, 6)', 4, -16, 'end', 20)
    _lab(p, 0, 7, 'B (0, b)', -10, 0, 'end', 20)
    _lab(p, 6.4, 11.8, 'm', 14, 0, 'start', 20, ORANGE); _lab(p, 9.6, 7.2, 'n', 14, 0, 'start', 20, TEAL)
    return _o_label(p.svg(), 'dr')


# ---- practice figures --------------------------------------------------------------------------------------
def rn_fig_p01():
    p = RPlane(-8, 8, -7, 7, no_o=True)
    p.poly([(0, 6), (7, 0), (0, -6), (-7, 0)], FILL, TEAL)
    p.seg((0, 6), (0, -6), INK, 2); p.seg((-7, 0), (7, 0), INK, 2)
    _lab(p, 0, 6, 'A (0, 6)', 8, -14, 'start', 20); _lab(p, 7, 0, 'D (7, 0)', 8, 16, 'start', 20)
    _lab(p, -7, 0, 'B', -10, 14, 'end', 20); _lab(p, 0, -6, 'C', -12, 12, 'end', 20)
    return p.svg()


def rn_fig_p02():
    p = RPlane(-6, 6, -1, 7)
    p.seg((-5.3, -1), (5.3, 7), TEAL, 2.5)
    for x, y in ((-4, 0), (0, 3), (4, 6)): p.point(x, y)
    _lab(p, -4, 0, 'A (−4, 0)', -6, -16, 'end', 20); _lab(p, 0, 3, 'B (0, 3)', 10, 12, 'start', 20)
    _lab(p, 4, 6, 'C', 12, 8, 'start', 20)
    return p.svg()


def rn_fig_p04():
    p = RPlane(-15, 15, -15, 15)
    bx, by = 7, 7 * S3_
    p.circle(0, 0, 14); p.seg((0, 0), (bx, by), TEAL); p.seg((bx, by), (bx, 0), TEAL); p.seg((0, 0), (bx, 0), TEAL)
    p.right(bx, 0, (-1, 0), (0, 1)); p.arc(0, 0, 0, 60, 22, '60°', 42)
    _lab(p, bx, by, 'B', 10, -10, 'start', 20); _lab(p, bx, 0, 'A', 4, 18, 'middle', 20)
    return p.svg()


def rn_fig_p05():
    p = RPlane(-2, 20, -1, 14, no_o=True)
    p.poly([(9, 12), (0, 0), (18, 0)], 'none', TEAL)
    _lab(p, 9, 12, 'A (9, 12)', 0, -16, 'middle', 20); _lab(p, 0, 0, 'B (0, 0)', -6, 18, 'end', 20)
    _lab(p, 18, 0, 'C (18, 0)', 0, 18, 'middle', 20)
    return p.svg()


def rn_fig_p06():
    p = RPlane(-3, 8, -2, 6)
    p.poly([(-2, -1), (6, -1), (6, 4)], 'none', INK); p.right(6, -1, (-1, 0), (0, 1))
    _lab(p, -2, -1, 'B (−2, −1)', -4, 18, 'middle', 20); _lab(p, 6, -1, 'C (6, −1)', 6, 18, 'start', 20)
    _lab(p, 6, 4, 'A', 10, -8, 'start', 20)
    s = p.svg(); ax, ay = _axes(s); return _move(s, 'O', x=ax - 26, y=ay - 16, anchor='middle')


def rn_fig_p09():
    p = RPlane(-3, 33, -18, 18)
    p.circle(15, 0, 17); p.cdot(15, 0); p.seg((15, 0), (0, 8), TEAL)
    _lab(p, 15, 0, 'A (15, 0)', 0, 18, 'middle', 20); _lab(p, 0, 8, '(0, y)', -10, -12, 'end', 20)
    s = p.svg(); return _o_label(s, 'dr')


def rn_fig_p10():
    p = RPlane(-2, 10, -5, 5)
    p.circle(4, 0, 4); p.cdot(4, 0)
    s = p.svg(); return _o_label(s, 'ul')


def rn_fig_p11():
    h = 3 * S3_
    V = {'A': (3, 0), 'B': (9, 0), 'C': (12, h), 'D': (9, 2 * h), 'E': (3, 2 * h), 'F': (0, h)}
    p = RPlane(-2, 14, -1, 11)
    p.poly([V[k] for k in 'ABCDEF'], 'none', INK)
    off = {'A': (0, 18, 'middle'), 'C': (10, 0, 'start'), 'D': (6, -14, 'start'), 'E': (-6, -14, 'end'), 'F': (-10, 0, 'end')}
    for k, (dx, dy, an) in off.items(): _lab(p, V[k][0], V[k][1], k, dx, dy, an, 20)
    _lab(p, 9, 0, 'B (9, 0)', 6, 18, 'start', 20)
    return p.svg()


def rn_fig_p14():
    p = RPlane(-1, 9, -1, 9)
    p.poly([(0, 5), (3, 0), (8, 3), (5, 8)], FILL, TEAL)
    _lab(p, 0, 5, 'A (0, 5)', -10, 0, 'end', 20); _lab(p, 3, 0, 'B (3, 0)', 6, 18, 'start', 20)
    _lab(p, 8, 3, 'C', 12, 0, 'start', 20); _lab(p, 5, 8, 'D', 0, -16, 'middle', 20)
    return p.svg()


def rn_fig_p15():
    p = RPlane(-4, 6, -2, 6)
    p.poly([(-3, -1), (5, -1), (1, 5)], 'none', INK)
    _lab(p, -3, -1, 'B (−3, −1)', -2, 18, 'middle', 20); _lab(p, 5, -1, 'C (5, −1)', 2, 18, 'middle', 20)
    _lab(p, 1, 5, 'A', 0, -16, 'middle', 20)
    s = p.svg(); return _o_label(s, 'ul')


def rn_fig_p17():
    R = 4 * math.sqrt(2)
    p = RPlane(-1, 7, -1, 7)
    a, b, r = p.P(0, R), p.P(R, 0), R * p.u; o = p.P(0, 0)
    p.body.append('<path d="M %.3f %.3f L %.3f %.3f A %.3f %.3f 0 0 1 %.3f %.3f Z" fill="%s" stroke="%s" stroke-width="2"/>' % (
        o[0], o[1], a[0], a[1], r, r, b[0], b[1], FILL, TEAL))
    p.poly([(0, 0), (0, 4), (4, 4), (4, 0)], 'white', TEAL)
    _lab(p, 0, 4, 'A (0, 4)', -10, 0, 'end', 20); _lab(p, 4, 0, 'B (4, 0)', 0, 18, 'middle', 20)
    _lab(p, 4, 4, 'C', 10, -12, 'start', 20)
    return p.svg()


def rn_fig_p18():
    k = 1.0; d = 3 + 1 / S3_
    p = RPlane(-0.6, 4.6, -0.5, 1.7)
    p.poly([(0, k), (d, k), (3, 0), (0.8, 0)], 'none', INK)
    p.arc(d, k, 180, 240, 24, '60°', 44)
    _lab(p, 0, k, 'A (0, k)', -8, -14, 'end', 20); _lab(p, d, k, 'D', 8, -14, 'start', 20)
    _lab(p, 3, 0, 'C (3k, 0)', 0, 18, 'middle', 20); _lab(p, 0.8, 0, 'B', 0, 18, 'middle', 20)
    return p.svg()


def rn_fig_p19():
    p = RPlane(-2, 7, -5, 6)
    p.seg((0, -3), (5, 4), TEAL, 2.5); p.point(0, -3); p.point(5, 4)
    _lab(p, 0, -3, 'A (0, −3)', -10, 4, 'end', 20); _lab(p, 5, 4, 'B (5, 4)', 10, -8, 'start', 20)
    s = p.svg(); return _o_label(s, 'ul')


def rn_fig_p20():
    p = RPlane(-4, 6, -7, 9)
    p.seg((-2.9, -6.8), (4.6, 8.2), TEAL, 2.5)
    for x, y in ((-2, -5), (0, -1), (4, 7)): p.point(x, y)
    _lab(p, -2, -5, 'B (−2, −5)', -10, 0, 'end', 20); _lab(p, 0, -1, 'C (0, −1)', 12, 4, 'start', 20)
    _lab(p, 4, 7, 'A (n, 7)', 10, 4, 'start', 20)
    s = p.svg(); return _o_label(s, 'ul')


# ---- new question texts (stem, choices, key, worked solution) ---------------------------------------------
RNQ = {
    # ---------------- guided ----------------
    'geo37-g156': dict(  # was A(4, 7), B(-8, -5), C(13, -5): 12-12 silver + 9-12-15 (Hebrew: 8-8 silver + 6-8-10)
        stem='The vertices of triangle $ABC$ are $A(5,\\ 16)$, $B(-19,\\ {-}8)$ and $C(12,\\ {-}8)$. What is its perimeter?',
        choices=['$31+24\\sqrt2$', '$80$', '$56+24\\sqrt2$', '$55+24\\sqrt2$'], correct=3,
        expl=['$B$ and $C$ have the same $y$ ($-8$). So, $BC$ is horizontal: $BC=19+12=31$.',
              'Drop the altitude from $A$ to $BC$. Its foot is $H(5,\\ {-}8)$, and $AH=16+8=24$.',
              'Left: $BH=19+5=24$ and $AH=24$. This is a 45-45-90 triangle. So, $AB=24\\sqrt2$.',
              'Right: $HC=12-5=7$ and $AH=24$. This is the triple 7-24-25. So, $AC=25$.',
              'Perimeter: $31+25+24\\sqrt2=56+24\\sqrt2$.',
              'Traps: $55+24\\sqrt2$ uses the altitude (24) instead of $AC$, and $80$ takes $AB$ as 24.']),
    'geo37-g158': dict(  # was radius 10, y = 5 (Hebrew: radius 6, y = 3)
        stem='A circle with radius $8$ is centered at the origin $O$. The point $A$ lies on the circle in the first quadrant, and its $y$-coordinate is $4$. What is the angle between $OA$ and the positive $x$-axis?',
        choices=['$60°$', '$45°$', '$30°$', '$75°$'], correct=3,
        expl=['Drop $AH$ perpendicular to the $x$-axis. $AH=4$ (the $y$ of $A$) and $OA=8$ (a radius).',
              'In a right triangle, a leg that is half the hypotenuse faces a $30°$ angle (the 30-60-90 triangle).',
              'So $\\angle AOH=30°$.']),
    'geo37-g160': dict(  # letters a, b -> p, q; A(-2a, -2b) -> A(-3p, -3q); key 1 -> 3
        stem='A straight line passes through the origin and through $A(-3p,\\ {-}3q)$, where $p>0$, $q>0$ and $p\\ne q$. The point $B$ lies on this line in the first quadrant. Which of the following cannot be the coordinates of $B$?',
        choices=['$(2p,\\ 2q)$', '$(\\frac1q,\\ \\frac1p)$', '$(p^3,\\ q^3)$', '$(\\frac p3,\\ \\frac q3)$'], correct=3,
        expl=['The line passes through the origin. So, every point on it has the same ratio $\\frac xy$. For $A$: $\\frac{-3p}{-3q}=\\frac pq$.',
              'Check the choices: $\\frac{2p}{2q}=\\frac pq$, $\\ \\frac1q\\div\\frac1p=\\frac pq$ and $\\frac{p/3}{q/3}=\\frac pq$. These three can be on the line.',
              '$\\frac{p^3}{q^3}=\\frac pq$ only if $p^2=q^2$, that is $p=q$ (both are positive). But $p\\ne q$. So, $(p^3,\\ q^3)$ cannot be on the line.',
              'Quick check with numbers: $p=1$, $q=2$. The line goes through $(1,\\ 2)$. So, $y$ is always twice $x$. $(1,\\ 8)$ is not on it; $(2,\\ 4)$, $(\\frac12,\\ 1)$ and $(\\frac13,\\ \\frac23)$ are.']),
    'geo37-g162': dict(  # was A(3, 4), D(8, 4): 64 (Hebrew A(2, 2), D(5, 2): 20)
        stem='$ABCD$ is a right trapezoid with $AD\\parallel BC$. Side $DC$ is parallel to the $y$-axis, and $AB$ passes through the origin $E$. Given: $A(4,\\ 3)$, $D(10,\\ 3)$ and $AE=EB$. What is the area of the trapezoid?',
        choices=['$36$', '$60$', '$120$', '$48$'], correct=2,
        expl=['$E$ is the origin and the midpoint of $AB$. From $E$ to $A$: 4 right and 3 up. So from $E$ to $B$: 4 left and 3 down. $B=(-4,\\ {-}3)$.',
              '$AD=10-4=6$. $C$ is below $D$, at the height of $B$: $C=(10,\\ {-}3)$. So $BC=4+10=14$.',
              'The height is $DC=3+3=6$.',
              'Area: $\\frac{(6+14)\\cdot6}{2}=60$.',
              'Traps: $36$ is only the $6\\times6$ rectangle, $48$ takes $BC$ as 10, and $120$ forgets to divide by 2.']),
    'geo37-g163': dict(  # was (-2, 1), (3, 9): 200 pi (Hebrew (5, 2), (9, 12): 160 pi)
        stem='A rectangle has sides parallel to the coordinate axes. Two opposite vertices of the rectangle are $(-4,\\ 2)$ and $(2,\\ 9)$. The rectangle makes a full turn around its right-hand vertical side. What is the volume of the solid formed?',
        choices=['$42\\pi$', '$252\\pi$', '$63\\pi$', '$294\\pi$'], correct=2,
        expl=['The width is $2-(-4)=6$ and the height is $9-2=7$.',
              'A full turn around the right side gives a cylinder. Its radius is the width, $r=6$, and its height is $h=7$.',
              '$V=\\pi r^2h=\\pi\\cdot36\\cdot7=252\\pi$.',
              'Traps: $63\\pi$ takes half the width as the radius, and $294\\pi$ swaps the radius and the height.']),
    'geo37-g164': dict(  # was A(6, 6) (Hebrew A(4, 4))
        stem='A circle is centered at the origin $O$ and passes through $A(8,\\ 8)$. $B$ is the point where the circle meets the negative $y$-axis. The two shaded regions together are the right half of the circle without triangle $OAB$. What is their total area?',
        choices=['$8\\sqrt2-4\\pi$', '$32\\pi-8$', '$64\\sqrt2-8\\pi$', '$64\\pi-32\\sqrt2$'], correct=4,
        expl=['Radius: from $O$ to $A(8,\\ 8)$ is 8 right and 8 up, a 45-45-90 triangle. So $r=8\\sqrt2$ and $r^2=128$.',
              'The right half of the circle: $\\frac{128\\pi}{2}=64\\pi$.',
              'Triangle $OAB$: the base $OB=8\\sqrt2$ is a radius on the $y$-axis. The altitude to it is the distance from $A$ to the $y$-axis, 8. Area: $\\frac{8\\sqrt2\\cdot8}{2}=32\\sqrt2$.',
              'Shaded area: $64\\pi-32\\sqrt2$.']),
    'geo37-g165': dict(  # was C(3, 0): 45 root 3 (Hebrew C(2, 0): 20 root 3)
        stem='$ABCDEF$ is a regular hexagon. Side $CD$ lies on the positive $x$-axis, $B$ lies on the positive $y$-axis, and $C=(4,\\ 0)$. The whole hexagon is shaded except triangle $AFE$. What is the shaded area?',
        choices=['$96\\sqrt3$', '$80\\sqrt3$', '$64\\sqrt3$', '$48\\sqrt3$'], correct=2,
        expl=['Each angle of a regular hexagon is $120°$. So, $\\angle BCO=180°-120°=60°$.',
              'Triangle $BOC$ is a 30-60-90 triangle with short leg $OC=4$. So the side of the hexagon is $BC=2\\cdot4=8$.',
              'The hexagon is 6 equilateral triangles with side 8. Each has area $\\frac{8^2\\sqrt3}{4}=16\\sqrt3$. Triangle $AFE$ has the same area as one of them.',
              'Shaded area: $5\\cdot16\\sqrt3=80\\sqrt3$.']),
    'geo37-g166': dict(  # was C(10, 4), A(5, 7): B(0, 5) (Hebrew C(6, 3), A(4, 4): B(0, 2))
        stem='Line $n$ passes through the origin and through $C(8,\\ 6)$. Line $m$ is parallel to $n$ and passes through $A(4,\\ 10)$ and $B(0,\\ b)$. What are the coordinates of $B$?',
        choices=['$(0,\\ 13)$', '$(0,\\ 4)$', '$(0,\\ 6)$', '$(0,\\ 7)$'], correct=4,
        expl=['Line $n$: from $O$ to $C(8,\\ 6)$ is 8 right and 6 up.',
              'Line $m$ is parallel to $n$. So, it has the same steps: 4 right goes with $\\frac{6}{8}\\cdot4=3$ up.',
              'From $B$ (on the $y$-axis) to $A(4,\\ 10)$ is 4 right. So, 3 up. Then $b=10-3=7$ and $B=(0,\\ 7)$.']),
    'geo37-g167': dict(  # y-axis -> x-axis, new choice order (key 2 -> 4)
        stem='A straight line and the $x$-axis have some number of points in common. Which of the following cannot be that number?',
        choices=['$1$', 'Infinitely many', '$0$', '$3$'], correct=4,
        expl=['A slanted line or a vertical line meets the $x$-axis once: 1 point.',
              'The $x$-axis itself: infinitely many points.',
              'A line parallel to the $x$-axis (and not on it) never meets it: 0 points.',
              'A straight line can never meet the $x$-axis in exactly 3 points.']),
    'geo37-g168': dict(  # was (4, -3) / (-2, 5), key 1 -> 2
        stem='Straight line $a$ does not intersect the $y$-axis, and straight line $b$ does not intersect the $x$-axis. Which of the following is necessarily true?',
        choices=['If $(-6,\\ 1)$ lies on $a$, then $(6,\\ 1)$ also lies on $a$.',
                 'If $(-6,\\ 1)$ lies on $a$, then $(-6,\\ {-}7)$ also lies on $a$.',
                 'If $(2,\\ {-}3)$ lies on $b$, then $(-2,\\ 3)$ also lies on $b$.',
                 'If $(2,\\ {-}3)$ lies on $b$, then $(2,\\ 3)$ also lies on $b$.'], correct=2,
        expl=['Line $a$ never meets the $y$-axis. So, it is parallel to it (vertical). Every point on $a$ has the same $x$.',
              'If $(-6,\\ 1)$ is on $a$, then every point on $a$ has $x=-6$. So $(-6,\\ {-}7)$ is on $a$: choice 2 is true.',
              'Choice 1 changes $x$. So, it is false.',
              'Line $b$ is horizontal. If $(2,\\ {-}3)$ is on $b$, every point on $b$ has $y=-3$. Choices 3 and 4 change $y$. So, they are false.']),
    'geo37-g169': dict(  # was through (-2, 4), key (-2, 9) [same x]; now through (3, -5), key (-1, -5) [same y]
        stem='A straight line passes through $(3,\\ {-}5)$. It is not perpendicular to either of the coordinate axes. Which of the following points cannot lie on the line?',
        choices=['$(6,\\ 1)$', '$(-1,\\ {-}5)$', '$(0,\\ 2)$', '$(-4,\\ 3)$'], correct=2,
        expl=['The line is not perpendicular to the $x$-axis. So, it is not vertical. It is not perpendicular to the $y$-axis. So, it is not horizontal.',
              '$(-1,\\ {-}5)$ has the same $y$ as $(3,\\ {-}5)$. The line through both points is horizontal, which is not allowed.',
              'Each other point has a different $x$ and a different $y$ from $(3,\\ {-}5)$. The line through it is slanted. So, it is possible.']),
    # ---------------- practice (Hebrew study-guide questions) ----------------
    'geo37-core-p01': dict(
        stem='The diagonals of rhombus $ABCD$ lie on the coordinate axes. Given: $A(0,\\ 6)$ and $D(7,\\ 0)$. What is the area of the rhombus?',
        choices=['$42$', '$84$', '$168$', '$63$'], correct=2,
        expl=['The diagonals of a rhombus bisect each other, and here they meet at the origin. So $C=(0,\\ {-}6)$ and $B=(-7,\\ 0)$.',
              '$AC=6+6=12$ and $BD=7+7=14$.',
              'Area $=\\frac{12\\cdot14}{2}=84$. Traps: $42=6\\cdot7$ uses half-diagonals, and $168$ forgets to divide by 2.']),
    'geo37-core-p02': dict(
        stem='The points $A(-4,\\ 0)$, $B(0,\\ 3)$ and $C$ lie on one straight line, and $B$ is between $A$ and $C$. Given: $AB=BC$. What are the coordinates of $C$?',
        choices=['$(4,\\ 3)$', '$(6,\\ 4)$', '$(4,\\ 6)$', '$(2,\\ 6)$'], correct=3,
        expl=['From $A(-4,\\ 0)$ to $B(0,\\ 3)$: 4 right and 3 up.',
              '$AB=BC$ on the same line. So, repeat the same move from $B$: $C=(0+4,\\ 3+3)=(4,\\ 6)$.']),
    'geo37-core-p03': dict(
        stem='For which pair of points does the straight line through them pass through the origin?',
        choices=['$(4,\\ {-}6)$ and $(4,\\ 9)$', '$(4,\\ {-}6)$ and $(-6,\\ 9)$', '$(-6,\\ 9)$ and $(4,\\ 9)$', '$(4,\\ {-}6)$ and $(-6,\\ {-}6)$'], correct=2,
        expl=['On a line through the origin, you get from one point to another by multiplying both coordinates by the same number.',
              '$(4,\\ {-}6)\\cdot(-1.5)=(-6,\\ 9)$. Both coordinates are multiplied by $-1.5$. So, the line through these points passes through the origin.',
              'The other pairs share a coordinate: choice 1 is the vertical line $x=4$, and choices 3 and 4 are the horizontal lines $y=9$ and $y=-6$. None of them passes through the origin.']),
    'geo37-core-p04': dict(
        stem='A circle centered at the origin $O$ has radius $14$. The point $B$ lies on the circle in the first quadrant, and $BA$ is perpendicular to the positive $x$-axis at $A$. Given: $\\angle BOA=60°$. What are the coordinates of $A$?',
        choices=['$(7\\sqrt3,\\ 0)$', '$(14,\\ 0)$', '$(0,\\ 7)$', '$(7,\\ 0)$'], correct=4,
        expl=['$OB=14$ is a radius. Triangle $OAB$ has a right angle at $A$ and $\\angle BOA=60°$. So, $\\angle B=30°$.',
              '$OA$ faces the $30°$ angle. So, it is half the hypotenuse: $OA=\\frac{14}{2}=7$.',
              '$A$ is on the positive $x$-axis: $A=(7,\\ 0)$.']),
    'geo37-core-p05': dict(
        stem='The vertices of triangle $ABC$ are $A(9,\\ 12)$, $B(0,\\ 0)$ and $C(18,\\ 0)$. What is its perimeter?',
        choices=['$42$', '$36$', '$48$', '$33$'], correct=3,
        expl=['$BC=18-0=18$. The altitude from $A$ meets $BC$ at $(9,\\ 0)$, and its length is 12.',
              'Each half of the base is 9. So, $AB=AC=15$ (the triple 9-12-15).',
              'Perimeter $=15+15+18=48$. Trap: $42=12+12+18$ uses the altitude instead of the sides.']),
    'geo37-core-p06': dict(
        stem='$ABC$ is a right triangle with the right angle at $C$. Given: $B(-2,\\ {-}1)$ and $C(6,\\ {-}1)$. $A$ lies above $C$, and the area of the triangle is $20$. What are the coordinates of $A$?',
        choices=['$(2,\\ 4)$', '$(6,\\ 9)$', '$(6,\\ 4)$', '$(6,\\ {-}6)$'], correct=3,
        expl=['$BC$ is horizontal: $BC=6-(-2)=8$. $AC$ is vertical. So, it is the height.',
              '$\\frac{8\\cdot AC}{2}=20$. So, $AC=5$.',
              '$A$ is 5 above $C(6,\\ {-}1)$: $A=(6,\\ 4)$. Trap: $(6,\\ 9)$ forgets to divide by 2.']),
    'geo37-core-p07': dict(  # y-axis <-> x-axis
        stem='A straight line intersects the $x$-axis at exactly one point, and that point is not the origin. The line is not perpendicular to the $x$-axis. Which of the following is necessarily true?',
        choices=['The line meets the positive $y$-axis.', 'The line and the coordinate axes bound a rectangle.',
                 'The line meets the negative $y$-axis.', 'The line and the coordinate axes bound a right triangle.'], correct=4,
        expl=['The line meets the $x$-axis at one point. So, it is not horizontal. It is not perpendicular to the $x$-axis. So, it is not vertical. A slanted line meets the $y$-axis too, exactly once.',
              'The line does not pass through the origin. So, it meets the two axes at two different points, both away from the origin.',
              'The line and the two axes close a right triangle (the right angle is at the origin).',
              'Choices 1 and 3 are not necessarily true: the line can meet the positive or the negative $y$-axis.']),
    'geo37-core-p08': dict(
        stem='Which pair of points lies on a line parallel to the $y$-axis?',
        choices=['$(4,\\ {-}1)$ and $(4,\\ 6)$', '$(4,\\ {-}1)$ and $(-1,\\ 4)$', '$(4,\\ {-}1)$ and $(7,\\ {-}1)$', '$(-1,\\ 6)$ and $(6,\\ {-}1)$'], correct=1,
        expl=['A line parallel to the $y$-axis is vertical: all its points have the same $x$.',
              'Only $(4,\\ {-}1)$ and $(4,\\ 6)$ have the same $x$, 4. Trap: choice 3 has the same $y$, so it is parallel to the $x$-axis.']),
    'geo37-core-p09': dict(
        stem='A circle has center $A(15,\\ 0)$ and radius $17$. It intersects the positive $y$-axis at $(0,\\ y)$. What is $y$?',
        choices=['$15$', '$8$', '$17$', '$2$'], correct=2,
        expl=['Join the center $A(15,\\ 0)$ to the point $(0,\\ y)$. With the origin, they make a right triangle.',
              'The horizontal leg is 15, and the hypotenuse is a radius, 17. So the other leg is 8 (the triple 8-15-17).',
              'The point is on the positive $y$-axis. So, $y=8$.']),
    'geo37-core-p10': dict(  # center on the y-axis -> on the x-axis
        stem='A circle has its center on the $x$-axis and passes through the origin. Which line is tangent to the circle at the origin?',
        choices=['The $x$-axis', 'The $y$-axis', 'The line through $(0,\\ 0)$ and $(1,\\ 1)$', 'The line through $(0,\\ 0)$ and $(-1,\\ 1)$'], correct=2,
        expl=['The center is on the $x$-axis. So, the radius to the origin lies on the $x$-axis.',
              'A tangent is perpendicular to the radius at the point where it touches the circle. The line through the origin that is perpendicular to the $x$-axis is the $y$-axis.']),
    'geo37-core-p11': dict(
        stem='$ABCDEF$ is a regular hexagon. $AB$ lies on the positive $x$-axis, $F$ lies on the positive $y$-axis, and $B=(9,\\ 0)$. A circle passes through all six vertices of the hexagon. What is the radius of the circle?',
        choices=['$3$', '$4.5$', '$9$', '$6$'], correct=4,
        expl=['Let $OA=x$. Each angle of a regular hexagon is $120°$. So, $\\angle FAO=180°-120°=60°$.',
              'Triangle $FOA$ is a 30-60-90 triangle with short leg $OA=x$. So, the side is $AF=2x$.',
              '$AB=AF=2x$. So, $OB=x+2x=3x=9$. Then $x=3$ and the side is 6.',
              'A regular hexagon is 6 equilateral triangles. So, the radius of the circle through its vertices equals the side: 6.']),
    'geo37-core-p12': dict(  # b through (0, 3) -> through (4, 0)
        stem='Straight lines $a$ and $b$ are parallel, and they are not the same line. Line $a$ passes through the origin, and line $b$ passes through $(4,\\ 0)$. Which point cannot lie on $a$?',
        choices=['$(1,\\ 2)$', '$(-3,\\ 1)$', '$(-5,\\ 0)$', '$(2,\\ {-}5)$'], correct=3,
        expl=['If $a$ passed through $(-5,\\ 0)$ and the origin, $a$ would be the $x$-axis.',
              'Then $a$ would also pass through $(4,\\ 0)$, which is on $b$. Two different parallel lines have no point in common. So, this is impossible.',
              'Each of the other points gives a slanted line through the origin, and $b$ can be the parallel line through $(4,\\ 0)$.']),
    'geo37-core-p13': dict(  # letters a, c -> m, n
        stem='A straight line passes through the origin and through $(m,\\ n)$, where $m>0$, $n>0$ and $m\\ne n$. Which of the following points necessarily lies on the line?',
        choices=['$\\left(\\frac1m,\\ \\frac1n\\right)$', '$(-3m,\\ {-}3n)$', '$(2n,\\ 2m)$', '$(m,\\ {-}n)$'], correct=2,
        expl=['On a line through the origin, both coordinates are multiplied by the same number.',
              '$(m,\\ n)\\cdot(-3)=(-3m,\\ {-}3n)$. So, this point is on the line.',
              'Check the others with the ratio $\\frac xy$. The line has $\\frac mn$. $(2n,\\ 2m)$ and $(\\frac1m,\\ \\frac1n)$ both give $\\frac nm$, which is not $\\frac mn$ because $m\\ne n$. $(m,\\ {-}n)$ gives a negative ratio.']),
    'geo37-core-p14': dict(
        stem='$ABCD$ is a square. Two neighboring vertices are $A(0,\\ 5)$ and $B(3,\\ 0)$. What is the area of the square?',
        choices=['$15$', '$64$', '$34$', '$8$'], correct=3,
        expl=['From $A(0,\\ 5)$ to $B(3,\\ 0)$: 3 across and 5 down. $AB^2=3^2+5^2=34$.',
              'The area of a square is its side squared: $AB^2=34$. No square root is needed. Trap: $64=(3+5)^2$ adds the legs first.']),
    'geo37-core-p15': dict(
        stem='$ABC$ is an isosceles triangle with $AB=AC$. Given: $B(-3,\\ {-}1)$ and $C(5,\\ {-}1)$. $A$ lies above $BC$, and the area of the triangle is $24$. What are the coordinates of $A$?',
        choices=['$(1,\\ 6)$', '$(1,\\ 5)$', '$(4,\\ 5)$', '$(1,\\ {-}7)$'], correct=2,
        expl=['$BC$ is horizontal: $BC=5-(-3)=8$. Its midpoint is $\\left(\\frac{-3+5}{2},\\ {-}1\\right)=(1,\\ {-}1)$.',
              'In an isosceles triangle, the altitude from $A$ goes to the midpoint of $BC$. So $A$ has $x=1$.',
              '$\\frac{8\\cdot h}{2}=24$. So, $h=6$. $A$ is 6 above $(1,\\ {-}1)$: $A=(1,\\ 5)$. Trap: $(1,\\ 6)$ uses the height as the $y$.']),
    'geo37-core-p16': dict(  # through (-4, 6), misses the y-axis -> through (5, -3), misses the x-axis
        stem='A straight line passes through $(5,\\ {-}3)$ and does not intersect the $x$-axis. Which of the following statements is necessarily true?',
        choices=['The point $(-3,\\ 5)$ lies on the line.', 'The line passes through the origin.',
                 'The line is perpendicular to the $y$-axis.', 'The point $(5,\\ 3)$ lies on the line.'], correct=3,
        expl=['A whole straight line that never meets the $x$-axis must be parallel to it. Therefore it is horizontal: every point on it has $y=-3$.',
              'A horizontal line is perpendicular to the $y$-axis: choice 3.',
              'The other choices: $(-3,\\ 5)$, $(5,\\ 3)$ and the origin $(0,\\ 0)$ do not have $y=-3$. So, they are not on the line.']),
    'geo37-core-p17': dict(
        stem='$AOBC$ is a square in the first quadrant. $O$ is the origin, and the sides $OA$ and $OB$ lie on the axes. The side of the square is $4$. A circle centered at $O$ passes through $C$. What is the area of the part of the circle in the first quadrant that is outside the square?',
        choices=['$8\\pi-16$', '$4\\pi-16$', '$16\\pi-16$', '$16-8\\pi$'], correct=1,
        expl=['$C=(4,\\ 4)$. So, $r=OC=4\\sqrt2$ (a 45-45-90 triangle) and $r^2=32$.',
              'The quarter of the circle in the first quadrant: $\\frac{32\\pi}{4}=8\\pi$.',
              'Subtract the square, $4^2=16$: $8\\pi-16$.']),
    'geo37-core-p18': dict(  # A(0, t), C(2t, 0) -> A(0, k), C(3k, 0)
        stem='$ABCD$ is a trapezoid with $AD\\parallel BC$. $BC$ lies on the $x$-axis. The vertices $A(0,\\ k)$ and $C(3k,\\ 0)$ are given, where $k>0$. $D$ lies to the right of $C$, and $\\angle ADC=60°$. What are the coordinates of $D$?',
        choices=['$\\left(3k+\\frac{k}{\\sqrt3},\\ k\\right)$', '$\\left(3k-\\frac{k}{\\sqrt3},\\ k\\right)$', '$(4k,\\ k)$', '$(3k+\\sqrt3k,\\ k)$'], correct=1,
        expl=['$AD\\parallel BC$ and $BC$ is on the $x$-axis. So, $AD$ is horizontal. $D$ has the same $y$ as $A$: $D=(x,\\ k)$.',
              'Drop $DE$ to the $x$-axis: $DE=k$. $\\angle DCE=\\angle ADC=60°$, because they are alternate angles between the parallel lines $AD$ and $BC$.',
              'Triangle $CED$ is a 30-60-90 triangle. The leg $DE=k$ faces the $60°$ angle. So, the short leg is $CE=\\frac{k}{\\sqrt3}$.',
              '$D=\\left(3k+\\frac{k}{\\sqrt3},\\ k\\right)$. Trap: $(4k,\\ k)$ treats the angle as $45°$.']),
    'geo37-core-p19': dict(
        stem='Given: $A(0,\\ {-}3)$ and $B(5,\\ 4)$. What is the length of $AB$?',
        choices=['$\\sqrt{24}$', '$\\sqrt{12}$', '$\\sqrt{74}$', '$\\sqrt{35}$'], correct=3,
        expl=['Across: $5-0=5$. Up: $4-(-3)=7$.',
              '$AB^2=5^2+7^2=74$. So, $AB=\\sqrt{74}$.',
              'Shortcut: the answers are roots. So, compare $AB^2=74$ with the numbers under the roots. There is no need to take the root.']),
    'geo37-core-p20': dict(
        stem='The points $A(n,\\ 7)$, $B(-2,\\ {-}5)$ and $C(0,\\ {-}1)$ lie on one straight line. What is $n$?',
        choices=['$6$', '$8$', '$4$', '$3$'], correct=3,
        expl=['From $B(-2,\\ {-}5)$ to $C(0,\\ {-}1)$: 2 right and 4 up. So every 1 right goes 2 up.',
              'From $C$ (height $-1$) to $A$ (height 7) is 8 up. So, it is 4 right: $n=0+4=4$.',
              'Trap: $8$ takes one step right for each step up.']),
}

RNFIG = {'geo37-g156': rn_fig_g156, 'geo37-g158': rn_fig_g158, 'geo37-g160': rn_fig_g160, 'geo37-g162': rn_fig_g162,
         'geo37-g163': rn_fig_g163, 'geo37-g164': rn_fig_g164, 'geo37-g165': rn_fig_g165, 'geo37-g166': rn_fig_g166,
         'geo37-core-p01': rn_fig_p01, 'geo37-core-p02': rn_fig_p02, 'geo37-core-p04': rn_fig_p04, 'geo37-core-p05': rn_fig_p05,
         'geo37-core-p06': rn_fig_p06, 'geo37-core-p09': rn_fig_p09, 'geo37-core-p10': rn_fig_p10, 'geo37-core-p11': rn_fig_p11,
         'geo37-core-p14': rn_fig_p14, 'geo37-core-p15': rn_fig_p15, 'geo37-core-p17': rn_fig_p17, 'geo37-core-p18': rn_fig_p18,
         'geo37-core-p19': rn_fig_p19, 'geo37-core-p20': rn_fig_p20}


# ---- slide rewriting -----------------------------------------------------------------------------------------
def AP(k, label): return ('AP', k, label)


def _rn_slide(M, vid, n, lines, items=None, fig=None, vis=None):
    """Rewrite one slide in place: board item texts (by index), the question figure / slide figure, and all lines.
    lines: str = spoken · D(text) = draw cue · AP(k, label) = item k pops in. Every item that popped in before must
    still pop in (same indexes), so the layout of the slide stays the same."""
    if vid in RN_RECORDED: return
    b = M.slide(vid, n)
    for k, t in (items or {}).items():
        assert b['items'][k].get('k') == 't', (vid, n, k); b['items'][k]['t'] = t
    for it in b['items']:
        if fig is not None and it.get('k') == 'q' and 'fig' in it: it['fig'] = {'type': 'geometry', 'svg': fig}
        if vis is not None and it.get('k') == 'vis': it['v']['svg'] = vis
    new = []
    for x in lines:
        if isinstance(x, str): new.append({'say': x})
        elif x[0] == 'D': new.append({'draw': x[1]})
        else: new.append({'appear': x[1], 'label': x[2]})
    old = sorted(l['appear'] for l in b['lines'] if 'appear' in l)
    assert old == sorted(l['appear'] for l in new if 'appear' in l), (vid, n, old)
    b['lines'] = new; M.touched_videos.add(vid)


def _rn_n(M, vid, title):
    ns = [i for i, b in enumerate(M.video(vid)['beats'], 1) if b['title'] == title]
    assert len(ns) == 1, (vid, title, ns); return ns[0]


def rn_videos(M, F):
    """F = new question figures by question id."""
    # ---------------- Question: triangle perimeter (geo37-g156) ----------------
    V = 'solve-geo37-g156'; f = F['geo37-g156']
    _rn_slide(M, V, 2, fig=f, items={1: '$BC=19+12=31$'}, lines=[
        "Triangle ABC on the coordinate plane. We already have the values of the points on the drawing. What's the perimeter?",
        "For the perimeter I need the length of each of the three sides. Let's start.",
        "BC — the simplest. B and C have the same y, minus 8. So, BC is parallel to the x-axis.",
        D('Split BC at the y-axis; write 19 on the left part and 12 on the right'),
        "I'll split it into two parts: from B to the y-axis, and from the y-axis to C.",
        "B is at minus 19. So, that part is 19. C is at 12. So, that part is 12.",
        AP(1, 'BC = 19 + 12 = 31'), "19 plus 12 — 31."])
    _rn_slide(M, V, 3, fig=f, items={1: '$AH=16+8=24$'}, lines=[
        "The other two sides are slanted. For a slanted line I need a right triangle. How do I make one?",
        D('Draw a perpendicular from A down to BC; call its foot H'),
        "From A, I drop a line perpendicular to the base — to BC. It's parallel to the y-axis.",
        "Now I have right triangles on both sides — right and left — and I can use Pythagoras.",
        D('Write 16 above the x-axis and 8 below it'),
        "The altitude: from the x-axis up to A is 16. From the x-axis down to the base — the height of the base line is minus 8. So, that's 8.",
        AP(1, 'AH = 16 + 8 = 24'), "16 and 8 — the whole altitude is 24."])
    _rn_slide(M, V, 4, fig=f, items={1: 'Left: $24,\\ 24$ $\\rightarrow$ silver $\\rightarrow$ $AB=24\\sqrt2$',
                                     2: 'Right: $7,\\ 24$ $\\rightarrow$ $7$-$24$-$25$ $\\rightarrow$ $AC=25$'}, lines=[
        "Now how long are the two parts of the base?",
        D('Write 24 on BH and 7 on HC'),
        "The x of A is 5. So, H is also at 5. From B at minus 19 to H at 5 — 19 plus 5, 24. And from H to C — 12 minus 5, 7.",
        AP(1, 'Left: 24, 24 → silver → AB = 24√2'),
        "On the left: 24 and 24 — a right isosceles triangle. The silver triangle: a, a, a root 2. So AB is 24 root 2.",
        AP(2, 'Right: 7, 24 → 7-24-25 → AC = 25'),
        "On the right: 7 and 24. That's the triple 7, 24, 25. So, AC is 25."])
    _rn_slide(M, V, 5, fig=f, items={1: '$P=31+25+24\\sqrt2$ $=56+24\\sqrt2$'}, lines=[
        AP(1, 'P = 31 + 25 + 24√2 = 56 + 24√2'),
        "Perimeter: 31 plus 25 plus 24 root 2 — 56 plus 24 root 2.",
        "Don't add the altitude — it's a helper line inside, not part of the boundary.",
        D('Circle choice 3'), "Choice three.",
        "The traps: 55 plus 24 root 2 takes the altitude, 24, instead of AC. And 80 takes AB as 24.",
        "So what did we have here? Supposedly analytic geometry — a coordinate plane.",
        "But really, the solution is Pythagoras. I need the triples, and the silver and golden triangles.",
        "Whoever isn't solid on those — really go back to Pythagoras and the special triangles."])

    # ---------------- Question: angle from a coordinate on a circle (geo37-g158) ----------------
    V = 'solve-geo37-g158'; f = F['geo37-g158']
    _rn_slide(M, V, 2, fig=f, items={1: '$AH=4$ $\\cdot$ $OA=8$'}, lines=[
        "A circle centered at the origin, radius 8. A is a point on the circle whose y value is 4. What is alpha?",
        D('Write 4 next to the y of A'),
        "The y of A is 4. So, the height of A is 4.",
        "Its x? Not given. But I don't really need it.",
        D('Drop a perpendicular from A to the x-axis; call its foot H'),
        "What do I do with a circle? As usual — first I drop a perpendicular and close a right triangle.",
        AP(1, 'AH = 4 · OA = 8'),
        "What do I know about this triangle? This leg — the height of A — is 4. And the hypotenuse is the radius, 8."])
    _rn_slide(M, V, 3, fig=f, lines=[
        "Now I have a right triangle with a leg and a hypotenuse. I could do Pythagoras and find the other leg.",
        "But I don't really need Pythagoras. Why?",
        AP(1, 'Leg = ½ hypotenuse → golden triangle'),
        "A right triangle where a leg is half the hypotenuse. When does that happen?",
        "Only in the golden triangle — 30, 60, 90.",
        "And the short leg sits opposite the 30.",
        AP(2, 'α = 30°'), "So our alpha is 30.",
        D('Circle choice 3'), "Choice three."])
    _rn_slide(M, V, 4, fig=f, items={1: '$S_{\\circ}=\\pi\\cdot8^2=64\\pi$',
                                     2: '$30°=\\frac1{12}$ $\\rightarrow$ $\\frac{64\\pi}{12}=\\frac{16\\pi}{3}$'}, lines=[
        "So what did we have? A circle on the coordinate plane. Here the radius was given — but it's the same move: close a right triangle and calculate what you need.",
        "By the way, they could have made it harder. What's the area of this sector?",
        D('Shade the sector between OA and the x-axis'),
        AP(1, 'S = π · 8² = 64π'), "First the whole circle: 64 pi.",
        AP(2, '30° = 1/12 of the circle → 64π/12 = 16π/3'),
        "30 out of 360 is a twelfth: 360 divided by 30 is 12.",
        "So the sector is 64 pi over 12 — 16 pi over 3.",
        "A circle on the coordinate plane isn't very complicated. Just remember — always close a Pythagoras triangle."])

    # ---------------- Question: which point cannot be on an origin line (geo37-g160) ----------------
    V = 'solve-geo37-g160'; f = F['geo37-g160']
    _rn_slide(M, V, 2, fig=f, items={1: '$\\frac xy=\\frac{3p}{3q}=\\frac pq$'}, lines=[
        "Line AB passes through the origin. A is (−3p, −3q). We are given that p and q are positive. So, A is in the third quadrant, bottom left.",
        "Which of these cannot be the coordinates of point B?",
        "B is somewhere on this line — we don't know exactly where. And notice, everything here is in letters, in unknowns.",
        "Some of you will see right away: the ratio is constant. But let's build a helper drawing.",
        D('Close a right triangle under A; write 3p and 3q on its legs'),
        "I close a triangle for A. Its legs: 3p and 3q — from the values of A.",
        D('Close a right triangle under B; write x and y on its legs'),
        "And a triangle for B. x and y — I don't know them. That's what they're asking.",
        "Two similar triangles: a 90 degree angle, and because the lines are parallel, these angles are equal.",
        AP(1, 'x/y = 3p/3q = p/q'),
        "Similar. So, x over y equals 3p over 3q. That's p over q.",
        "So I plug each answer in for x and y and check: is it equal to p over q? If not — that's the one we're looking for."])
    _rn_slide(M, V, 3, items={1: '$p=1,\\ q=2$: $\\ A(-3,\\ {-}6)$', 2: '$(2,\\ 4)$ ✓ $\\ (\\frac12,\\ 1)$ ✓',
                              3: '$(1,\\ 8)$ ✗ $\\ (\\frac13,\\ \\frac23)$ ✓'}, lines=[
        "Before the algebra — the fast way for strong students: plug in numbers.",
        "Take p = 1 and q = 2. They're positive, and they're different.",
        AP(1, "'p = 1, q = 2: A(−3, −6)' appears"),
        "Then A is (minus 3, minus 6). On this line, y is always twice x.",
        AP(2, "'(2, 4) ✓ (1/2, 1) ✓' appears"),
        "Choice 1: (2, 4). Choice 2: (one half, 1). In both, y is twice x. On the line.",
        AP(3, "'(1, 8) ✗ (1/3, 2/3) ✓' appears"),
        "Choice 3: (1, 8). 8 is not twice 1. Off the line. Choice 4: (one third, two thirds) — on the line.",
        "Only choice 3 is off the line. Ten seconds. Now let's see why, with the letters."])
    _rn_slide(M, V, 4, fig=f, items={1: '$\\frac{p^3}{q^3}\\stackrel{?}{=}\\frac pq$'}, lines=[
        AP(1, 'p³/q³ = p/q ?'),
        "Choice 3: p cubed over q cubed. Is it equal to p over q?",
        "Not only don't I know — I can say it's NOT equal. It's given that p is not equal to q.",
        "Cubing does not keep the ratio when p ≠ q. We'll see exactly why at the end.",
        D('Circle choice 3'),
        "So that's the answer — the one that can't be the coordinates of B. Choice three."])
    _rn_slide(M, V, 5, fig=f, items={1: '$\\frac{2p}{2q}=\\frac pq\\ \\checkmark$',
                                     2: '$\\frac1q\\div\\frac1p=\\frac1q\\cdot p=\\frac pq\\ \\checkmark$',
                                     3: '$\\frac{p/3}{q/3}=\\frac pq\\ \\checkmark$'}, lines=[
        "But let's check the other answers too — suppose this one had been the last choice, and we checked it last.",
        AP(1, '2p/2q = p/q ✓'), "2p over 2q: cancel the 2 — p over q. Equal. Cross it out.", D('Cross out choice 1'),
        AP(2, '(1/q) ÷ (1/p) = (1/q) · p = p/q ✓'),
        "1 over q divided by 1 over p — a fraction divided by a fraction: multiply by the reciprocal. p over q. Also possible.",
        D('Cross out choice 2'),
        AP(3, '(p/3)/(q/3) = p/q ✓'), "p over 3, q over 3 — the thirds cancel. p over q. Cross it out.", D('Cross out choice 4')])
    _rn_slide(M, V, 6, fig=f, items={1: '$p\\rightarrow p^3$: $\\times p^2$ $\\cdot$ $q\\rightarrow q^3$: $\\times q^2$',
                                     2: '$p=1,\\ q=2$: $\\ \\frac12$ vs $\\frac18$'}, lines=[
        "So what's important to understand? A line through the origin — its points make similar triangles, one inside the other.",
        "So the ratio of x to y must be the same at every point. Build that equation, and check the choices.",
        AP(1, 'p → p³: × p² · q → q³: × q²'),
        "The course puts it one more way: cubing multiplies p by p squared, and q by q squared — two different multipliers. Off the line.",
        AP(2, 'p = 1, q = 2: 1/2 vs 1/8'),
        "With numbers: p = 1, q = 2. The line is 1 to 2. The cubes — 1 to 8. Not the same.",
        "Not an easy question. Whoever needs to — rewind and watch it again, slowly.",
        "An edge question, like we sometimes get at the end of the section. And we're strong students — we can handle it."])

    # ---------------- Question: right trapezoid (geo37-g162) ----------------
    V = 'solve-geo37-g162'; f = F['geo37-g162']
    _rn_slide(M, V, 2, fig=f, items={2: '$AD=10-4=6$'}, lines=[
        "E is the origin. ABCD is a right trapezoid. AE equals EB. What's the area of the trapezoid?",
        "We need the area of a trapezoid. It's really a quadrilaterals question, presented on a coordinate system.",
        AP(1, 'Area = (a + b) · h / 2 appears'),
        "The area of a trapezoid: sum of the bases, times the height, over 2.",
        "What we need to do: pull the data out of the system.",
        "Start with AD — the top base. We have points A and D.",
        "The y of A is 3, and the y of D is 3. So AD is parallel to the x-axis.",
        AP(2, 'AD = 10 − 4 = 6 appears'),
        "So its length is simply the difference between the x's: 10 minus 4 — 6.",
        D('Write 6 on AD'), "Top base — done."])
    _rn_slide(M, V, 3, fig=f, items={1: '$B=(-4,\\ {-}3)$'}, lines=[
        "The bottom base is harder. We have nothing about B or C.",
        "But there's one more given: EB equals AE.",
        D('Mark AE = EB with equal ticks'),
        "We learned: once there's a slanted line on the axes — draw right triangles on it.",
        D('Draw a right triangle under AE (legs to the axes) and one on EB'),
        "Same line, same slope. So, the triangles are at least similar.",
        "Here they're more than similar: the hypotenuses are equal. So, they're congruent.",
        "The top triangle: E is the origin, zero-zero. A is at 4, 3. So we moved 4 to the right, and climbed 3 floors.",
        D('Write 4 and 3 on the legs of both triangles'),
        "So the bottom triangle is 4 and 3 as well.",
        AP(1, 'B(−4, −3) appears'),
        "B is 4 to the left and 3 down: minus 4, minus 3."])
    _rn_slide(M, V, 4, fig=f, items={1: '$BC=4+4+6=14$', 2: '$h=DC=3+3=6$', 3: '$\\frac{(6+14)\\cdot6}{2}=60$'}, lines=[
        "Almost done. Let's collect the data.",
        AP(1, 'BC = 4 + 4 + 6 = 14 appears'), "BC: 4, plus 4, plus 6 under AD — 14.",
        AP(2, 'DC = 3 + 3 = 6 appears'), "The height DC: 3 up plus 3 down — 6.",
        AP(3, '(6 + 14) · 6 / 2 = 60 appears'),
        "Into the formula: 6 plus 14 is 20. Times 6, over 2 — cancel the 2: 20 times 3 — 60.",
        D('Circle choice 2'), "Choice two.",
        "By the way — 36 is a trap. That's only the 6-by-6 rectangle, without the triangle on the left. And 48 forgets the part of BC to the left of the y-axis."])

    # ---------------- Question: rectangle turned into a cylinder (geo37-g163) ----------------
    V = 'solve-geo37-g163'; f = F['geo37-g163']
    _rn_slide(M, V, 2, fig=f, lines=[
        "A rectangle with sides parallel to the axes. We rotate it a full turn around its right-hand vertical side.",
        "What's the volume of the solid formed?",
        "A 3D solid is formed here. Let's understand it.",
        D('Draw the rectangle sweeping around its right side'),
        "We take the rectangle and turn it a full turn — and we get a cylinder.",
        "So we need the volume of a cylinder. A 3D question, on the axes.",
        AP(1, 'V = πr² · h appears'),
        "The volume of a cylinder — a straight solid: base area times height. Pi r squared, times h.",
        "How do we find the radius and the height? From the rectangle."])
    _rn_slide(M, V, 3, fig=f, items={1: '$r=2-(-4)=6$', 2: '$h=9-2=7$'}, lines=[
        "The sides are parallel to the axes, and we're given two opposite corners.",
        "In this case it's always easy to find the rectangle's dimensions.",
        "The bottom side is parallel to the x-axis. So, y is fixed along it. The right side is parallel to the y-axis. So, x is fixed along it.",
        D('Write (2, 2) at the bottom-right corner'),
        "So the bottom-right corner is 2, 2.",
        AP(1, 'r = 2 − (−4) = 6 appears'),
        "The x-difference: from minus 4 to 2 — 6. That's the width — and it's the radius, because we turn around the side itself.",
        AP(2, 'h = 9 − 2 = 7 appears'),
        "The y-difference: from floor 2 to floor 9 — we climbed 7. That's the height."])
    _rn_slide(M, V, 4, fig=f, items={1: '$\\pi\\cdot6^2\\cdot7=252\\pi$'}, lines=[
        "We have the radius, and we have the height. Plug in.",
        AP(1, 'π · 6² · 7 = 252π appears'),
        "Pi times 6 squared — 36 pi. Times 7 — 252 pi.",
        D('Circle choice 2'), "Choice two.",
        "What did we have here? A 3D question presented on the coordinate system.",
        "Two traps: 63 pi — taking half the width as the radius. And 294 pi — swapping the radius and the height."])

    # ---------------- Question: semicircle minus a triangle (geo37-g164) ----------------
    V = 'solve-geo37-g164'; f = F['geo37-g164']
    _rn_slide(M, V, 2, fig=f, items={2: '$r=8\\sqrt2$'}, lines=[
        "A is on a circle centered at the origin. B is on the negative y-axis. What's the total shaded area?",
        "The sum of the shaded areas — a shaded-area question. How do we handle those? Build a scheme.",
        AP(1, 'Shaded = semicircle − triangle appears'),
        "Here: half a circle, minus the triangle.",
        "For the semicircle we need the radius. The radius is OA.",
        "We learned: to find a slanted segment on the axes — build a right triangle with it as the hypotenuse.",
        D('Drop a perpendicular from A to the x-axis and draw the right triangle'),
        "O is zero-zero, A is 8, 8. We moved 8 right and climbed 8.",
        "Legs 8 and 8 — a silver triangle.",
        AP(2, 'r = 8√2 appears'),
        "So the hypotenuse — the radius — is 8 root 2."])
    _rn_slide(M, V, 3, fig=f, items={1: '$\\pi(8\\sqrt2)^2=128\\pi$', 2: 'Semicircle $=64\\pi$'}, lines=[
        AP(1, 'πr² = π(8√2)² = 128π appears'),
        "The whole circle: pi r squared. Careful — square the 8 AND the root 2: 64 times 2 — 128 pi.",
        AP(2, 'Semicircle = 64π appears'),
        "Half a circle — 64 pi.",
        "Now — don't rush to the triangle. We can think psychometrically: partial calculation.",
        "The answer must be 64 pi minus something. Any other answer is out.",
        D('Cross out choice 1'),
        "8 root 2 minus 4 pi — no 64 pi. Out.",
        D('Cross out choices 2 and 3'),
        "32 pi minus 8 — the wrong number in front of pi. 64 root 2 minus 8 pi — pi in the wrong place. Both out.",
        D('Circle choice 4'),
        "64 pi minus something — that's only choice four. Partial calculation really shortens the solution.",
        "On the exam: mark it and move on. This is probably the last question — go back over the section if you have time."])
    _rn_slide(M, V, 4, fig=f, items={1: '$S_\\triangle=\\frac{8\\sqrt2\\cdot8}{2}=32\\sqrt2$', 2: '$64\\pi-32\\sqrt2$'}, lines=[
        "In the lesson we finish — the triangle's area.",
        "We need a base and the altitude to it. Take OB as the base.",
        D('Write 8√2 on OB'),
        "OB is a radius — 8 root 2.",
        "The height: the triangle is obtuse. So, it's an outside height — the distance from A to the y-axis.",
        D('Draw the horizontal distance from A to the y-axis and write 8'),
        "And that distance is exactly how far we moved right in x — 8.",
        AP(1, 'Triangle = 8√2 · 8 / 2 = 32√2 appears'),
        "8 root 2 times 8, over 2 — 32 root 2.",
        AP(2, '64π − 32√2 appears'),
        "64 pi minus 32 root 2 — choice four.",
        "And if you found the triangle first? Then it's something with pi, minus 32 root 2 — partial calculation works from that side too. Only choice four."])
    _rn_slide(M, V, 5, fig=f, items={1: '$8\\sqrt2-4\\pi\\approx11.3-12.6<0$', 2: 'Semicircle $64\\pi>192$',
                                     3: '$\\triangle<\\frac{12\\cdot8}{2}=48\\ \\Rightarrow$ shaded $>144$'}, lines=[
        "Now by estimating sizes. Honestly — here it's a bit weak. Better to calculate with partial calculation.",
        "But some students get here with no time, or can't even find the radius. So we work with what we can.",
        "First — check the answers. Are they far enough apart to rule some out?",
        AP(1, '8√2 − 4π ≈ 11.3 − 12.6 < 0 appears'),
        "Choice one: 8 root 2 is a bit over 11. 4 pi is a bit over 12.5. So it's negative! An area can't be negative — out, with no calculating.",
        "You may want to compare the top shaded piece with the 8-by-8 square. That's not reliable here: the top piece is an eighth of the circle — 16 pi, about 50 — smaller than the square, 64.",
        "So use two quick bounds instead.",
        AP(2, 'Semicircle 64π > 192 appears'),
        "The semicircle: 64 pi is more than 64 times 3 — 192.",
        AP(3, 'Triangle < 12 · 8 / 2 = 48 appears'),
        "The triangle: base 8 root 2 is less than 12, height 8 — less than 48. So the shaded area is more than 144.",
        D('Cross out choices 2 and 3'),
        "32 pi minus 8 is about 92. 64 root 2 minus 8 pi is about 65. Both too small. Choice four.",
        "Two approaches: full math with the partial-calculation shortcut, or estimating. The recommended one: math with partial calculation."])

    # ---------------- Question: regular hexagon on the axes (geo37-g165) ----------------
    V = 'solve-geo37-g165'; f = F['geo37-g165']
    for it in M.slide(V, 2)['items']:   # slide 2 has no numbers: only the figure changes
        if it.get('k') == 'q' and 'fig' in it: it['fig'] = {'type': 'geometry', 'svg': f}
    M.touched_videos.add(V)
    _rn_slide(M, V, 3, fig=f, items={1: '$BC=2\\cdot4=8$'}, lines=[
        "Now find the side. C is at 4, 0. Work with triangle BOC.",
        "In a regular hexagon every angle is 120.",
        D('Write 120° at C inside the hexagon and 60° at C in triangle BOC'),
        "The angle next to it is 60. And at O — 90, the axes. A right triangle.",
        "90, 60, 30 — a golden triangle.",
        "The short leg, opposite the 30, is OC — the distance from the origin to C: 4.",
        AP(1, 'BC = 2 · 4 = 8 appears'),
        "The hypotenuse BC is twice the short leg — 8. That's the hexagon's side."])
    _rn_slide(M, V, 4, fig=f, items={1: '$5\\cdot\\frac{8^2\\sqrt3}{4}=5\\cdot16\\sqrt3$', 2: '$=80\\sqrt3$'}, lines=[
        "Now we plug in a equals 8.",
        AP(1, '5 · 8²√3/4 = 5 · 16√3 appears'),
        "8 squared is 64. Over 4 — 16. 16 root 3, times 5 —",
        AP(2, '= 80√3 appears'),
        "— 80 root 3.",
        D('Circle choice 2'), "Choice two."])

    # ---------------- Question: parallel lines, find B (geo37-g166) ----------------
    V = 'solve-geo37-g166'; f = F['geo37-g166']
    _rn_slide(M, V, 2, fig=f, lines=[
        "Line n passes through the origin and C at 8, 6. Line m passes through A at 4, 10 and B at zero, b. m is parallel to n. What's B?",
        "When it's not clear what to do — go given by given, and see what information each one gives.",
        "First given: n passes through C and the origin.",
        "We learned: a line through two points — build a right triangle.",
        D('Drop a perpendicular from C to the x-axis; write 8 on the x-leg and 6 on the y-leg'),
        "Drop a height from C to the x-axis. The x-leg is 8, the y-leg is 6.",
        "Next given: m passes through A and B. Build a right triangle again.",
        D('Draw the right triangle from B to A; write 4 on the x-leg and ? on the y-leg'),
        "This time x goes from 0 to 4 — we moved 4. The height — we don't know. That's the question mark."])
    _rn_slide(M, V, 3, fig=f, items={1: '$\\frac{8}{6}=\\frac{4}{?}$', 2: '$10-3=7\\ \\Rightarrow\\ B(0,\\ 7)$'}, lines=[
        "The lines are parallel. What does that tell us?",
        "Their slope is equal. And if the slope is equal — the triangles are similar.",
        "So this is really a similarity question on the coordinate system.",
        AP(1, '8/6 = 4/? appears'),
        "The ratio of the legs: 6 is three quarters of 8. So here too, the y-leg is three quarters of 4 — 3.",
        "Or simply: the x-leg was halved, 8 to 4. So, the y-leg is halved too, 6 to 3.",
        AP(2, '10 − 3 = 7 → B(0, 7) appears'),
        "Almost done. From floor 10 I go down 3 floors — floor 7.",
        D('Circle choice 4'),
        "B is zero, 7. Choice four. A similarity question on the axes.",
        "If you prefer an equation: y equals three quarters x plus b. Plug in A: 10 equals 3 plus b. So, b is 7. Same answer."])

    # ---------------- Question: a line and the x-axis (geo37-g167) ----------------
    V = 'solve-geo37-g167'
    _rn_slide(M, V, 2, lines=[
        "Which of the following cannot be the number of points a straight line shares with the x-axis?",
        "To solve it — sketch a coordinate system.",
        "Go through the answers. An answer that's impossible — mark it. Any answer that's possible — cross it out.",
        D('Sketch a slanted line crossing the x-axis once'),
        "One point: a standard slanted line. One shared point with the x-axis. Possible —",
        D('Cross out choice 1'), "— out.",
        "Infinitely many: only in one situation — when the line lies right on top of the x-axis. Then every point is shared.",
        D('Cross out choice 2'), "Possible — out.",
        D('Sketch a horizontal line above the x-axis'),
        "Zero points: a line parallel to the x-axis. A line is endless — if its distance from the axis is always the same, they never meet.",
        D('Cross out choice 3'), "Parallel lines never meet. Zero is possible — out.",
        D('Circle choice 4'),
        "And 3 is impossible. Choice four. To cross an axis more than once you need a parabola, or some other curve — not a straight line."])
    _rn_slide(M, V, 3, lines=[
        "To solve these questions, understand three situations.",
        AP(1, 'Parallel to an axis → never meets it · perpendicular to the other appears'),
        "One: parallel–perpendicular. A line parallel to one axis never meets that axis — unless it lies on it. And it is necessarily perpendicular to the other axis.",
        AP(2, "Doesn't cross an axis → parallel to it appears"),
        "Two: crossing or not. If a line doesn't cross the x-axis — it must be parallel to it, and perpendicular to the y-axis.",
        "But a line that does cross an axis doesn't have to be perpendicular to it — it can be slanted, and then it crosses both axes.",
        AP(3, 'Lying on an axis → infinitely many points appears'),
        "Three: coinciding lines. A line can lie right on an axis — infinitely many shared points."])

    # ---------------- Question: which coordinate stays fixed (geo37-g168) ----------------
    V = 'solve-geo37-g168'
    _rn_slide(M, V, 2, items={1: 'On $a$: every point with $x=-6$ — $(-6,\\ {-}7),\\ (-6,\\ 0),\\ (-6,\\ 100)$'}, lines=[
        "Line a doesn't meet the y-axis. Line b doesn't meet the x-axis. Which must be true?",
        "Go through the claims. Start with choice one.",
        D('Sketch axes and mark (−6, 1)'),
        "If minus 6, 1 is on a — then 6, 1 is on a too?",
        "a has no shared point with the y-axis. What do we learn? It must be parallel to it.",
        D('Draw a vertical line through (−6, 1)'),
        "So draw a vertical line through minus 6, 1.",
        AP(1, 'a: every point with x = −6 appears'),
        "Every point on it has x equal to minus 6: minus 6, minus 7 — minus 6, zero — minus 6, a hundred. 6, 1 has x equal to 6 — off the line. Choice one is wrong.",
        "Notice: choices one and two start the same, three and four start the same. If a claim fails, its twin with the same start is the next one to check.",
        "Choice two: minus 6, minus 7. Its x is minus 6 — it's on the line.",
        D('Circle choice 2'),
        "That's the right answer. On the exam — mark it and move on."])
    _rn_slide(M, V, 3, items={1: 'On $b$: every point with $y=-3$'}, lines=[
        "In the lesson we check the rest.",
        "Now b. It has no shared point with the x-axis — it can't be slanted. It must be parallel to the x-axis.",
        D('Draw a horizontal line through (2, −3)'),
        AP(1, 'b: every point with y = −3 appears'),
        "Every point on it has y equal to minus 3.",
        "Choice three: minus 2, 3 — the y changed. Wrong. Choice four: 2, 3 — the y changed again. Wrong.",
        "Keeping a coordinate isn't enough — keep the right one: x on a vertical line, y on a horizontal line."])
    _rn_slide(M, V, 4, lines=[
        "We solved it by understanding. Some students solve it by trial and error.",
        "They draw the point minus 6, 1, then the point minus 6, minus 7, join them with a line — and check whether that line misses the y-axis.",
        D('Plot (−6, 1) and (−6, −7) and join them'),
        "That works too. But the understanding way is better."])

    # ---------------- Question: a forbidden point (geo37-g169) ----------------
    V = 'solve-geo37-g169'
    _rn_slide(M, V, 2, lines=[
        "A line passes through 3, minus 5. It's perpendicular to neither axis. Which point cannot be on it?",
        "To understand it — sketch a coordinate system.",
        D('Sketch axes and mark (3, −5)'),
        "The line passes through 3, minus 5. It's not perpendicular to the x-axis. So, a vertical line is impossible.",
        "And it's not perpendicular to the y-axis. So, a horizontal line is impossible too.",
        "Go through the answers. Which point can't be on the line?",
        "6, 1 — join it: a slanted line, neither vertical nor horizontal. Possible.",
        D('Mark (−1, −5) and join it to (3, −5)'),
        "Minus 1, minus 5. Same y — notice! If we join the points, the line is horizontal — perpendicular to the y-axis. Not allowed.",
        D('Circle choice 2'),
        "So this point is impossible — choice two. On the exam: mark and move on.",
        "In the lesson, the others: 0, 2 and minus 4, 3 — slanted lines again. Possible."])
    _rn_slide(M, V, 3, items={1: "The point can't have $x=3$ or $y=-5$"}, lines=[
        "How do we solve it psychometrically? You can draw — or understand.",
        AP(1, 'x ≠ 3 and y ≠ −5 appears'),
        "Some students see it right away: if the line is perpendicular to neither axis, the point can't have x equal to 3 — or y equal to minus 5.",
        AP(2, 'Same x → vertical · same y → horizontal appears'),
        "Any point with y equal to minus 5 — the line would be perpendicular to the y-axis. Any point with x equal to 3 — perpendicular to the x-axis.",
        "Only minus 1, minus 5 has that pattern. Choice two.",
        "That's it for the coordinate system."])


def rn_lessons(M):
    # ---------------- "The Coordinate Plane" (geo-154): A(4, 3), B(-5, 2), C(-3, -3) -> A(6, 2), B(-4, 3), C(-2, -4) ----
    V = 'geo-154'
    base = M.slide(V, 2)['items'][0]['v']['svg']
    _rn_slide(M, V, 3, lines=[
        AP(0, 'The coordinate plane appears'),
        "The two axes are perpendicular to each other, and they meet at one point.",
        D('Circle O and write (0, 0)'),
        "That point is called the origin. Its x is 0 and its y is 0.",
        "Every point has an x value and a y value — and they decide where the point is.",
        D('Mark 3 and 6 on the x-axis, and −1 and −4 on the y-axis'),
        "A point can sit right on an axis — say 3 or 6 on x, or −1, −4 on y.",
        "But once we have both axes, we can move across AND up. So, a point can be anywhere in the plane.",
        AP(1, 'Origin O = (0, 0)')])
    _rn_slide(M, V, 4, lines=[
        "How do we write where a point is?",
        AP(0, 'A(x, y) appears'),
        "The value of A is made of its x value and its y value, inside brackets.",
        AP(1, 'x always first · y always second'),
        "x always comes first, y always second. Always.",
        "So (6, 2) and (2, 6) are two different points."])
    _rn_slide(M, V, 5, vis=rn_fig_point(base, 6, 2, 'A'), items={1: '$A=(6,\\ 2)$'}, lines=[
        AP(0, 'The plane with point A appears'),
        "Here's A. We don't have its values — we need to find them.",
        "How? From A, I drop a perpendicular to each axis.",
        D('Draw a dashed line from A down to the x-axis and write 6'),
        "Down to the x-axis: it cuts the x-axis at 6. So the x of A is 6.",
        D('Draw a dashed line from A across to the y-axis and write 2'),
        "Across to the y-axis: it cuts it at 2. So the y of A is 2.",
        AP(1, 'A = (6, 2)'),
        "Notice — I wrote the 6 first and the 2 second. x first, y second. A is (6, 2)."])
    _rn_slide(M, V, 6, vis=rn_fig_point(base, -4, 3, 'B'), items={1: '$B=(-4,\\ 3)$'}, lines=[
        AP(0, 'The plane with point B appears'),
        "Another one — B.",
        D('Drop a dashed line from B to the x-axis and write −4'),
        "First a perpendicular to the x-axis — it cuts at minus 4.",
        D('Draw a dashed line from B to the y-axis and write 3'),
        "Then a perpendicular to the y-axis — it cuts at 3.",
        AP(1, 'B = (−4, 3)'),
        "B is (−4, 3). The minus belongs to the x only — B is to the left, but still above the x-axis."])
    _rn_slide(M, V, 7, vis=rn_fig_point(base, -2, -4, 'C'), items={1: '$C=(-2,\\ {-}4)$'}, lines=[
        AP(0, 'The plane with point C appears'),
        "And one more point — C.",
        D('Drop dashed lines from C to both axes and write −2 and −4'),
        "Perpendicular to the x-axis — minus 2. Perpendicular to the y-axis — minus 4.",
        AP(1, 'C = (−2, −4)'),
        "C is (−2, −4). Left and down.",
        "So let's sum up: every point has two values, an x and a y. We find them where the perpendiculars cut the x-axis and the y-axis.",
        "And the notation is always A(x, y) — x on the left, y on the right."])

    # ---------------- "Lengths on the Plane" (geo-155) ----------------
    V = 'geo-155'; fpq = rn_fig_pq()
    _rn_slide(M, V, 2, vis=fpq, lines=[
        AP(0, 'Points P and Q on one vertical line appear'),
        "If a segment is parallel to one of the axes, we find its length from the distance between its two ends — on the axis it's parallel to.",
        "When is a segment parallel to the y-axis? When the x values of its two points are the same.",
        "Look: the x of P is 4, and the x of Q is also 4. Both go 4 units to the right.",
        D('Complete a rectangle between PQ and the y-axis'),
        "Imagine closing a rectangle here — PQ is parallel to the y-axis. It's perpendicular to the x-axis.",
        AP(1, 'Same x → parallel to the y-axis')])
    _rn_slide(M, V, 3, vis=fpq, items={1: '$PQ=3+5=8$', 2: 'or $3-(-5)=8$'}, lines=[
        AP(0, 'P and Q on the vertical line appear'),
        "So how long is it?",
        D('Write 3 above the x-axis and 5 below it'),
        "I check its height above the x-axis — 3. And its depth below the x-axis — 5. That's just the y of Q without the minus.",
        AP(1, 'PQ = 3 + 5 = 8'), "Together — 8.",
        "In practice I can also subtract the y values: 3 minus minus 5 — 8.",
        AP(2, 'or 3 − (−5) = 8'),
        "But when the two points are on opposite sides of the axis, it's easier to see by eye: up to the axis, plus down from the axis."])
    _rn_slide(M, V, 4, vis=rn_fig_rs(), items={1: '$RS=7-1=6$'}, lines=[
        AP(0, 'Points R and S on one horizontal line appear'),
        "A segment parallel to the x-axis — that happens when the y values of the two points are the same.",
        "Here both are 4. And here I subtract the x values.",
        "These two points are on the same side of the axis — no minus here.",
        D('Mark 1 and 7 on the x-axis'),
        "From the y-axis to S is 7. From the y-axis to R is 1. What's left between them — 6.",
        AP(1, 'RS = 7 − 1 = 6'),
        "Same side — subtract. Opposite sides — add."])
    _rn_slide(M, V, 5, items={0: 'From $x=-2$ to $x=7$: $\\ 2+7=9$', 1: 'Not $7-2=5$!'}, lines=[
        "A quick check with the x values.",
        AP(0, 'From x = −2 to x = 7: 2 + 7 = 9'),
        "From minus 2 to 7: 2 units up to the y-axis, 7 more after it. 9.",
        AP(1, 'Not 7 − 2 = 5!'),
        "The classic mistake is 7 minus 2 — 5. The ends are on opposite sides of zero. A quick sketch prevents it.",
        "Most students have no problem with these — once you do it once, you get it."])
    _rn_slide(M, V, 7, vis=rn_fig_uv(), items={1: '$8,\\ 15$ $\\rightarrow$ $UV=17$'}, lines=[
        AP(0, 'The slanted segment UV appears'),
        "To find the length of a slanted segment — one that isn't parallel to either axis —",
        D('Draw a horizontal line from U and a vertical line from V; mark the right angle'),
        "we draw lines parallel to the axes and close a right triangle.",
        D('Write 8 on the horizontal leg'),
        "The horizontal leg: from x = −2 to x = 6 — 8.",
        D('Write 15 on the vertical leg'),
        "The vertical leg: from y = −3 up to 12 — 15.",
        AP(1, '8, 15 → UV = 17'),
        "And now I don't even need to calculate Pythagoras — a triple, 8, 15, 17."])
    _say(M, V, 8, 'like root 72.', 'like root 74.')

    # ---------------- "Circles on the Plane" (geo-157) ----------------
    V = 'geo-157'
    M.edit_lines(V, 3, lambda ls: [dict(l, draw='Write (5, 5) next to C') if l.get('draw') == 'Write (4, 4) next to C' else l for l in ls])
    _say(M, V, 3, "say (4, 4) — I know right away the radius is 4.", "say (5, 5) — I know right away the radius is 5.")
    _rn_slide(M, V, 4, items={0: 'Center $(-6,\\ 6)$, tangent to both axes $\\rightarrow$ $r=6$'}, lines=[
        "The course adds one line about the other quadrants.",
        AP(0, 'Center (−6, 6), tangent to both axes → r = 6'),
        "A circle with center (−6, 6) is tangent to both axes too. The values aren't equal — but without the signs, they are.",
        AP(1, 'The distances to the axes, without the signs, both equal r')])
    _rn_slide(M, V, 5, vis=rn_fig_center_axis(), items={1: '$r=9-5=4$'}, lines=[
        AP(0, 'A circle with center C on the x-axis and a point P appears'),
        "Another circle — its center is on one of the axes, here the x-axis.",
        "Sometimes the circle sits a bit further along the x-axis.",
        "Then say I have the value of the center, and the value of this point on the circle, where it cuts the x-axis.",
        D('Write 9 − 5 = 4 on CP'),
        "To find the radius, I subtract the x of the center from the x of the point.",
        AP(1, 'r = 9 − 5 = 4'),
        "9 minus 5 — the radius is 4. Not 5! 5 is where the center is, not the radius."])
    fo = rn_fig_origin_circle()
    _rn_slide(M, V, 6, vis=fo, items={1: '$10,\\ 24$ $\\rightarrow$ $r=26$'}, lines=[
        AP(0, 'A circle centered at the origin with a point A appears'),
        "The truth is, the most common circle questions on the coordinate plane — are when the center is at the origin.",
        "Most likely I'll be given a point on the circle, and asked for an area, a circumference, something like that.",
        "For that I need the radius. How do I find it?",
        D('Draw the radius OA'),
        "I draw a radius to the point. Now it's a slanted line — and we already know how to find the length of a slanted line.",
        D('Drop a perpendicular from A to the x-axis; write 10 and 24'),
        "Close a triangle: the x of the point is 10. So, this leg is 10. The height of the point is 24.",
        AP(1, '10, 24 → r = 26'),
        "10, 24 — that's 5, 12, 13 times 2. The radius is 26."])
    _rn_slide(M, V, 7, vis=fo, items={1: '$C=2\\pi\\cdot26=52\\pi$', 2: '$S=\\pi\\cdot26^2=676\\pi$'}, lines=[
        AP(0, 'The circle centered at the origin appears'),
        "And now the circumference and the area — this we already know.",
        AP(1, 'C = 2π · 26 = 52π'), AP(2, 'S = π · 26² = 676π'),
        "Circumference 52 pi. Area 676 pi.",
        "But look what I did: I drew a radius, closed a right triangle, found the radius — and from there, whatever they ask."])
    c = M.card('mem-coordinates')
    c['tips'] = [t.replace('A center at $(6,\\ 0)$ does not mean $r=6$', 'A center at $(5,\\ 0)$ does not mean $r=5$') for t in c['tips']]
    assert any('$(5,\\ 0)$' in t for t in c['tips'])

    # ---------------- "Slope" (geo-159): stairs A(-8, 0), C(0, 6), step 4-3 -> A(-24, 0), C(0, 10), step 12-5;
    #                  origin line (2, 3), (4, 6), (6, 9) -> (3, 2), (6, 4), (9, 6) ----------------
    V = 'geo-159'; fs, fl = rn_fig_stairs(), rn_fig_origin_line()
    n = _rn_n(M, V, 'Equal steps')
    for it in M.slide(V, n)['items']:
        if it.get('k') == 'vis': it['v']['svg'] = fs
    _rn_slide(M, V, _rn_n(M, V, 'Step size'), vis=fs, items={1: 'One step: $12$ across, $5$ up'}, lines=[
        AP(0, 'The line with A, B, C and D appears'),
        "Since the values of A and C are given, I can find the size of every step.",
        "From A to C is two steps.",
        D('Write 24 under the two steps, then 12 under each'),
        "Across: from minus 24 to 0 — 24. Two steps. So, each step is 12 wide.",
        D('Write 10 beside the two steps, then 5 beside each'),
        "Up: from 0 to 10 — 10. Two steps. So, each step is 5 high.",
        AP(1, 'One step: 12 across, 5 up'),
        D('Write B = (−12, 5) and D = (12, 15)'),
        "And now I get the other points for free: B is (−12, 5). One more step — D is (12, 15)."])
    _rn_slide(M, V, _rn_n(M, V, 'The length AD'), vis=fs, items={
            1: '$AD^2=36^2+15^2=1521$ $\\rightarrow$ $AD=39$', 2: 'One step: $5,\\ 12,\\ 13$ $\\rightarrow$ $13\\times3=39$'}, lines=[
        AP(0, 'The line with A, B, C and D appears'),
        "To find AD — a slanted line — what do we do? Close a right triangle.",
        D('Drop a vertical line from D and draw a horizontal line from A'),
        "The height: three steps, 5 each — 15. The width: three steps, 12 each — 36.",
        AP(1, 'AD² = 36² + 15² = 1521 → AD = 39'),
        "36 squared plus 15 squared — 1,521. Its root is 39. Heavy numbers.",
        "Much easier: Pythagoras on one step, and multiply by 3.",
        AP(2, 'One step: 5, 12, 13 → 13 × 3 = 39'),
        "One step is 5, 12, 13 — 13. Times 3 — 39. Exactly the same."])
    _rn_slide(M, V, _rn_n(M, V, 'Slope is a ratio'), items={
            0: 'Slope $=$ up $\\div$ across $=\\frac{5}{12}$', 1: 'Not the length $13$ $\\cdot$ $24$ across, $10$ up $\\rightarrow$ also $\\frac{5}{12}$'}, lines=[
        "A short word on the word 'slope' itself.",
        AP(0, 'Slope = up ÷ across = 5/12'),
        "The slope is the ratio: up divided by across. Here 5 over 12.",
        AP(1, 'Not the length 13 · 24 across, 10 up → also 5/12'),
        "It's not the length of the step, 13. A bigger step — 24 across and 10 up — has the same slope. Direction: the ratio. Length: Pythagoras."])
    _rn_slide(M, V, _rn_n(M, V, 'Through the origin'), vis=fl, lines=[
        "Now the more complicated part of the lesson — a line that passes through the origin.",
        "It's not really complicated — it can even be an easy question. But very often the questions here are not simple.",
        AP(0, 'A line through the origin with several points appears'),
        AP(1, 'Through the origin: x : y is the same for every point'),
        "When a line passes through the origin, the ratio between the x and the y of all its points is always constant.",
        D('Draw the stairs from O: 3 across, 2 up, three times'),
        "Go right 3 and up 2 — I reach a point on the line. Again right 3, up 2 — another. The same stairs we saw before.",
        "(3, 2), (6, 4), (9, 6) — the ratio between x and y stays the same every time."])
    _rn_slide(M, V, _rn_n(M, V, 'Same multiplier'), vis=fl, items={1: '$(3,2)\\rightarrow(6,4)\\rightarrow(9,6)$: both $\\times$ the same number'}, lines=[
        AP(0, 'The line through the origin appears'),
        AP(1, '(3, 2) → (6, 4) → (9, 6): both × the same number'),
        "Every point here is (3, 2) with BOTH values multiplied by the same number. Times 2, times 3.",
        "Double only the x and keep the y? You've left the line."])
    _rn_slide(M, V, _rn_n(M, V, 'Negative side too'), vis=fl, items={1: '$(-3,\\ {-}2)$: the same ratio $3:2$'}, lines=[
        AP(0, 'The line through the origin appears'),
        D('Point to S and write (−3, −2)'),
        "Through the origin to the other side: (−3, −2). Both signs changed together — the ratio is still 3 to 2.",
        AP(1, '(−3, −2): the same ratio 3 : 2')])


RN_REMOVE = ['geo37-core-p22', 'q-r26-t37-11',                       # copies (of guided q-r26-t37-05 and -10)
             'geo37-core-p24', 'geo37-core-p25', 'geo37-core-p27',    # extra-bank items beyond 3 warm-ups
             'q-r26-t37-06']                                          # September item, midpoint type the Hebrew p02 covers
RN_ORDER = ['geo37-core-p08', 'geo37-core-p21', 'geo37-core-p26', 'geo37-core-p23', 'geo37-core-p01', 'geo37-core-p19',
            'geo37-core-p05', 'geo37-core-p06', 'geo37-core-p02', 'geo37-core-p03', 'geo37-core-p10', 'geo37-core-p09',
            'geo37-core-p14', 'geo37-core-p20', 'geo37-core-p04', 'geo37-core-p16', 'geo37-core-p07', 'geo37-core-p12',
            'geo37-core-p13', 'q-r26-t37-03', 'q-r26-t37-09', 'geo37-core-p11', 'geo37-core-p17', 'geo37-core-p15',
            'geo37-core-p18', 'q-r26-t37-12']


def renumber_pass(M):
    fx = lambda t: t.replace(',\\ -', ',\\ {-}')
    F = {}
    for qid, d in RNQ.items():
        if qid in RN_RECORDED: continue
        fig = RNFIG[qid]() if qid in RNFIG else None
        F[qid] = fig
        kw = dict(stem=fx(d['stem']), choices=[fx(c) for c in d['choices']], correct=d['correct'], expl=[fx(e) for e in d['expl']])
        if fig is not None: kw['figure'] = fig
        M.set_q(qid, **kw)
    rn_videos(M, F)
    rn_lessons(M)
    # practice clean-up and order (easy -> hard)
    for qid in RN_REMOVE: M.unplace(qid)
    M.practice_order(PRACTICE, RN_ORDER)
    # guided order: the two easy English questions (midpoint, line equation) before the hard letters question;
    # the cylinder (medium) before the trapezoid (medium-plus). All of them come after the lessons they use.
    for qid in ('q-r26-t37-05', 'q-r26-t37-07'):
        M.move(qid, LEARN, before='geo37-g160'); M.move('solve-' + qid, LEARN, after=qid)
    M.move('geo37-g163', LEARN, before='geo37-g162'); M.move('solve-geo37-g163', LEARN, after='geo37-g163')
    review_fixes(M)


def review_fixes(M):
    """2026-10-06 review: the slide title still named the old key position (the cubes are choice 3 now)."""
    if 'solve-geo37-g160' in RN_RECORDED: return
    b = M.slide('solve-geo37-g160', 4)
    assert b.get('title') == 'Plug in choice 1', b.get('title')
    b['title'] = 'Plug in choice 3'; M.touched_videos.add('solve-geo37-g160')


_apply_before_rn = apply


def apply(M):
    _apply_before_rn(M)
    renumber_pass(M)


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
    # core practice (line through the origin and (m, n)): pick values that fit (topic 51, later)
    _sp_line(M, 'geo37-core-p13', r'Shortcut · Pick values that fit: any $m\ne n$ that are positive will do. Take $m=1$, $n=2$: the line goes through $(1,\ 2)$, so $y=2x$. Only $(-3,\ {-}6)$ fits: $-6=2\cdot(-3)$. $\left(1,\ \frac12\right)$, $(4,\ 2)$ and $(1,\ {-}2)$ do not.')


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
    # "Pick values that fit" is taught in topic 51 (day 6), before topic 37: a normal method line.
    _po_relabel(M, 'geo37-core-p13', 'Shortcut · Pick values that fit:', 'Pick values that fit')


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
    # solve-geo37-g164 · Estimating sizes: √128 < 12 < 4π, and upper bounds with π < 4, √2 < 1.5 (no 11.3 / 12.6 / 92 / 65)
    v = 'solve-geo37-g164'
    if not _nd_recorded(v):
        _nd_item(M, v, 'Estimating sizes', r'$8\sqrt2-4\pi\approx11.3-12.6<0$',
                 r'$8\sqrt2=\sqrt{128}<12<4\pi$', label='8√2 = √128 < 12 < 4π appears')
        _nd_lines(M, v, 'Estimating sizes', [
            ('say', "Choice one: 8 root 2 is a bit over 11. 4 pi is a bit over 12.5. So it's negative! An area can't be negative — out, with no calculating.",
             ["Choice one: bring the 8 into the root — 8 root 2 is root 128. Less than root 144, which is 12. And 4 pi is more than 12.",
              "So it's negative! An area can't be negative — out, with no calculating."]),
            ('say', "You may want to compare the top shaded piece with the 8-by-8 square. That's not reliable here: the top piece is an eighth of the circle — 16 pi, about 50 — smaller than the square, 64.",
             "You may want to compare the top shaded piece with the 8-by-8 square. That's not reliable here: the top piece is an eighth of the circle — 16 pi, less than 16 times three and a half, 56 — smaller than the square, 64."),
            ('say', "32 pi minus 8 is about 92. 64 root 2 minus 8 pi is about 65. Both too small. Choice four.",
             ["32 pi is less than 32 times 4 — 128. And 64 root 2 is less than 64 times one and a half — 96.",
              "Both are under 144 — too small. Choice four."])])


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
    _mn_load().method_names(M, 37)   # 2026-10-07 method names: runs last


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
    # #37: center on the x-axis and the circle touches the y-axis -> the center's x IS the radius
    _cf_add(M, 'geo-157', 'Center on an axis', '9 minus 5 — the radius is 4.', [
        'Unless the circle touches the y-axis: then the x of the center IS the radius. Center at 5, touching the y-axis — r is 5.'])
    # #40: center at the origin - tangents where the circle cuts the axes make a square around it
    _cf_add(M, 'geo-157', 'Center at the origin', "10, 24 — that's 5, 12, 13 times 2.", [
        D('Draw the tangents where the circle cuts the axes'),
        'And one more picture: tangents where the circle cuts the axes make a square around it. Its side is 2r — here 52.'])
    # #52: the answer may show a simplified root (3 root 13 = root 117)
    _cf_add(M, 'geo-159', 'The length AD', 'One step is 5, 12, 13 — 13. Times 3 — 39.', [
        "And if one step's length is a root? Say root 13 — three steps are 3 root 13. The answers may show it as root 117: the same number, 117 is 9 times 13."])


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
    _sl_load().spoken_labels(M, 37)   # 2026-10-09 spoken labels: runs LAST
