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
            "x first, y second. Always. (4, 3) and (3, 4) are different points.",
            _b('On the x-axis: y = 0 · on the y-axis: x = 0', 'On the $x$-axis: $y=0$ · on the $y$-axis: $x=0$'),
            _b('I (+,+) · II (−,+) · III (−,−) · IV (+,−)', 'I $(+,+)$ · II $(-,+)$ · III $(-,-)$ · IV $(+,-)$'),
            "The four quadrants go counterclockwise from the top right. A point on an axis is in no quadrant."]),
        dict(title='Reflections', active=1, script=[
            _b('Across the x-axis: (x, −y) · across the y-axis: (−x, y)', 'Across the $x$-axis: $(x,\\ {-y})$ · across the $y$-axis: $(-x,\\ y)$'),
            "A reflection is a mirror. Across the x-axis, only y changes its sign. Across the y-axis, only x.",
            _b('Through the origin: (−x, −y)', 'Through the origin: $(-x,\\ {-y})$'),
            "Through the origin, both signs change. (4, 2) goes to (minus 4, minus 2)."]),
        dict(title='Along an axis', active=2, script=[
            _b('Same x → vertical · same y → horizontal', 'Same $x$ $\\rightarrow$ vertical · same $y$ $\\rightarrow$ horizontal'),
            "Same x? The segment is vertical — use the y values. Same y? It's horizontal — use the x values.",
            _b('Same side: subtract · opposite sides: add', 'Same side: subtract · opposite sides: add'),
            "Same side of the axis — subtract. Opposite sides — add the two parts.",
            _b('From x = −4 to x = 6: 4 + 6 = 10, not 6 − 4 = 2', 'From $x=-4$ to $x=6$: $4+6=10$, not $6-4=2$'),
            "6 minus 4 is the classic mistake."]),
        dict(title='Slanted segments', active=3, script=[
            _b('Slanted → right triangle → Pythagoras', 'Slanted $\\rightarrow$ right triangle $\\rightarrow$ Pythagoras'),
            "A slanted segment? Draw lines parallel to the axes and close a right triangle.",
            _b('Across 5, up 12 → 13', 'Across $5$, up $12$ $\\rightarrow$ $13$'),
            "Across 5, up 12. A triple — 13. No distance formula needed. It's just Pythagoras.",
            _b('Roots in the answers? Compare across² + up²', 'Roots in the answers? Compare across$^2+$ up$^2$'),
            "And if the answers are roots, don't take the root. Look for across squared plus up squared under the root."]),
        dict(title='Slanted triangles', active=4, script=[
            _b('A horizontal or vertical side → base × height ÷ 2', 'A horizontal or vertical side $\\rightarrow$ $\\frac{\\text{base}\\cdot\\text{height}}{2}$'),
            "The area of a triangle on the plane. Is one side horizontal or vertical? Use it as the base. The height is a straight drop.",
            _b('No such side → box it in, subtract the corners', 'No such side $\\rightarrow$ box it in, subtract the corners'),
            _b('36 − (6 + 6 + 8) = 16', 'Box $36$, corners $6+6+8$: $\\ 36-20=16$'),
            "Then subtract the three corner right triangles. Box 36, corners 20 — the triangle is 16."]),
        dict(title='Circles', active=5, script=[
            _b('Circle: find r first', 'Circle: find $r$ first'),
            "With a circle, find the radius first. Then the area, the circumference — whatever they ask.",
            _b('Center at O, point (5, 12) → r = 13', 'Center at $O$, point $(5,\\ 12)$ $\\rightarrow$ $r=13$'),
            "Center at the origin? Draw the radius to the point, close a right triangle, Pythagoras.",
            _b('Tangent to both axes: center (r, r) · center (6, 0) ≠ r = 6', 'Tangent to both axes: center $(r,\\ r)$ · center $(6,\\ 0)$ does not mean $r=6$', size=36),
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
            _b('(2, 3) → (4, 6) → (6, 9): both × the same number', '$(2,\\ 3)\\rightarrow(4,\\ 6)\\rightarrow(6,\\ 9)$: both $\\times$ the same number'),
            "A line through the origin: every point is one point with both values multiplied by the same number.",
            _b('Only for a line through the origin', 'Only for a line through the origin'),
            "This works only for a line through the origin. On other lines, compare the steps, not the points.",
            "Letters in the question? Plug in easy numbers, like a = 1 and b = 2."]),
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
            "The traps: 6 minus 4 instead of 4 plus 6. Adding the legs instead of Pythagoras.",
            "A center at (6, 0) is not a radius of 6. And across the x-axis, it's the y that changes.",
            "Good luck."]),
    ], LEARN, after=last)
