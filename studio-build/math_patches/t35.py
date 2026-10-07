"""Topic 35 - Three-dimensional geometry. Course review 2026-09 fixes.
See t35_CHANGES.md for the plain-language list."""
import re
from dsl import T, H, A, D, Q

TOPIC = 35
LEARN = 'geo35-learn-1'
PRACT = 'geo35-core-practice'

# =========================================================================================
# Figure helpers - same style as the existing geometry figures (colors, stroke widths, font)
# =========================================================================================
INK, DASH, TEAL, ORANGE = '#203344', '#71818d', '#087f83', '#bb6821'
FILL, FRONT, TOP, HL, SQ = '#d5f1ed', '#f8fbfd', '#e8eefb', '#efc58b', '#edf3f7'
FONT = 'DejaVu Sans,Arial,sans-serif'


class Fig:
    def __init__(self, title):
        self.title = title; self.parts = []; self.xs = []; self.ys = []

    def _pts(self, pts):
        for x, y in pts: self.xs.append(x); self.ys.append(y)

    def poly(self, pts, fill=FRONT, stroke=INK, sw=2.5):
        self._pts(pts)
        self.parts.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (
            ' '.join('%.3f,%.3f' % p for p in pts), fill, stroke, sw))

    def line(self, p, q, stroke=INK, sw=2.5, dash=False):
        self._pts([p, q])
        self.parts.append('<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="%s"%s/>' % (
            p[0], p[1], q[0], q[1], stroke, sw, ' stroke-dasharray="7 5"' if dash else ''))

    def text(self, x, y, s, size=20, color=INK, bold=False):
        w = 0.62 * size * len(s) / 2
        self._pts([(x - w, y - size * 0.6), (x + w, y + size * 0.6)])
        self.parts.append('<text x="%.3f" y="%.3f" text-anchor="middle" dominant-baseline="middle" fill="%s" font-family="%s" font-size="%s"%s>%s</text>' % (
            x, y, color, FONT, size, ' font-weight="700"' if bold else '', s))

    def ellipse(self, cx, cy, rx, ry, fill='white', stroke=INK, sw=2.5):
        self._pts([(cx - rx, cy - ry), (cx + rx, cy + ry)])
        self.parts.append('<ellipse cx="%.3f" cy="%.3f" rx="%.3f" ry="%.3f" fill="%s" stroke="%s" stroke-width="%s"/>' % (cx, cy, rx, ry, fill, stroke, sw))

    def half_ellipse(self, cx, cy, rx, ry, front=True):
        """front=True: the visible lower arc (solid); False: the hidden upper arc (dashed)."""
        self._pts([(cx - rx, cy - ry), (cx + rx, cy + ry)])
        if front:
            self.parts.append('<path d="M %.3f %.3f A %.3f %.3f 0 0 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="2.5"/>' % (cx - rx, cy, rx, ry, cx + rx, cy, INK))
        else:
            self.parts.append('<path d="M %.3f %.3f A %.3f %.3f 0 0 1 %.3f %.3f" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 5"/>' % (cx - rx, cy, rx, ry, cx + rx, cy, DASH))

    def raw(self, s, bbox=None):
        if bbox: self._pts(bbox)
        self.parts.append(s)

    def svg(self, tight=False, pad=24):
        if tight:
            x0, y0 = min(self.xs) - pad, min(self.ys) - pad
            vb = '%.1f %.1f %.1f %.1f' % (x0, y0, max(self.xs) + pad - x0, max(self.ys) + pad - y0)
        else:
            vb = '0 0 640 360'
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
                % (vb, self.title, self.title, ''.join(self.parts)))


def box_fig(title, x0, y0, w, h, d, labels=(), water=None, hidden=True, extra=None):
    """Oblique box. Front face: (x0, y0) bottom-left, width w, height h. Depth d drawn at 30 degrees.
    labels: list of (x, y, text) in figure coordinates. water: height (px) of a water layer."""
    f = Fig(title)
    dx, dy = d * 0.8, -d * 0.5
    A_, B_ = (x0, y0), (x0 + w, y0)
    C_, D_ = (x0 + w + dx, y0 + dy), (x0 + dx, y0 + dy)
    E_, F_ = (x0, y0 - h), (x0 + w, y0 - h)
    G_, H_ = (x0 + w + dx, y0 - h + dy), (x0 + dx, y0 - h + dy)
    f.poly([A_, B_, F_, E_], fill=FRONT)
    f.poly([B_, C_, G_, F_], fill=FILL if water is None else FRONT)
    f.poly([E_, F_, G_, H_], fill=TOP)
    if water is not None:
        wy = water
        f.poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 - wy), (x0, y0 - wy)], fill=FILL, stroke=TEAL, sw=1.7)
        f.poly([(x0 + w, y0), C_, (C_[0], C_[1] - wy), (x0 + w, y0 - wy)], fill=FILL, stroke=TEAL, sw=1.7)
        f.poly([(x0, y0 - wy), (x0 + w, y0 - wy), (C_[0], C_[1] - wy), (D_[0], D_[1] - wy)], fill='#bfe6e0', stroke=TEAL, sw=1.7)
        # redraw the box outline on top of the water
        for p, q in [(A_, B_), (B_, F_), (F_, E_), (E_, A_), (B_, C_), (C_, G_), (G_, F_), (G_, H_), (H_, E_)]:
            f.line(p, q)
    if hidden:
        f.line(A_, D_, DASH, dash=True); f.line(D_, C_, DASH, dash=True); f.line(D_, H_, DASH, dash=True)
    if extra: extra(f, dict(A=A_, B=B_, C=C_, D=D_, E=E_, F=F_, G=G_, H=H_))
    for x, y, s in labels: f.text(x, y, s)
    return f


def cube_grid(f, n, x0, y0, s, marks=None):
    """n x n x n cube of small cubes. Front face bottom-left at (x0, y0), small edge s (px).
    marks: {(col, row, 'front'|'top'|'right'): fill} with col from the left, row from the top (front face),
    for the top face row = depth (0 = front), for the right face col = depth."""
    marks = marks or {}
    ddx, ddy = s * 0.55, -s * 0.35
    for r in range(n):          # top face, back rows first
        k = n - 1 - r
        for c in range(n):
            bx, by = x0 + c * s + k * ddx, y0 - n * s + k * ddy
            f.poly([(bx, by), (bx + s, by), (bx + s + ddx, by + ddy), (bx + ddx, by + ddy)],
                   fill=marks.get((c, k, 'top'), TOP), sw=1.7)
    for k in range(n - 1, -1, -1):  # right face
        for r in range(n):
            bx, by = x0 + n * s + k * ddx, y0 - (n - 1 - r) * s + k * ddy
            f.poly([(bx, by), (bx + ddx, by + ddy), (bx + ddx, by + ddy - s), (bx, by - s)],
                   fill=marks.get((k, r, 'right'), FILL), sw=1.7)
    for r in range(n):          # front face
        for c in range(n):
            bx, by = x0 + c * s, y0 - (n - 1 - r) * s
            f.poly([(bx, by), (bx + s, by), (bx + s, by - s), (bx, by - s)], fill=marks.get((c, r, 'front'), FRONT), sw=1.7)


def fig_upright_prism():
    f = Fig('An upright triangular prism: triangle ABC at the bottom, triangle DEF straight above it')
    A_, B_, C_ = (180, 300), (340, 300), (410, 215)
    up = 165
    D_, E_, F_ = (A_[0], A_[1] - up), (B_[0], B_[1] - up), (C_[0], C_[1] - up)
    f.poly([A_, B_, E_, D_], fill=FRONT)
    f.poly([B_, C_, F_, E_], fill=FILL)
    f.poly([D_, E_, F_], fill=TOP)
    f.line(A_, C_, DASH, dash=True)
    for (x, y), s in [((164, 312), 'A'), ((352, 316), 'B'), ((428, 222), 'C'), ((164, 128), 'D'), ((346, 118), 'E'), ((426, 40), 'F')]:
        f.text(x, y, s)
    return f


def fig_cone_cyl():
    f = Fig('A cylinder with height h and a cone with height H, side by side, with equal bases')
    # cylinder (left)
    cx, cy, rx, ry, hh = 215, 285, 62, 17, 120
    f.poly([(cx - rx, cy), (cx + rx, cy), (cx + rx, cy - hh), (cx - rx, cy - hh)], fill=FILL, stroke='none', sw=0)
    f.ellipse(cx, cy, rx, ry, fill=FILL, stroke='none', sw=0)
    f.half_ellipse(cx, cy, rx, ry, front=False); f.half_ellipse(cx, cy, rx, ry, front=True)
    f.line((cx - rx, cy), (cx - rx, cy - hh)); f.line((cx + rx, cy), (cx + rx, cy - hh))
    f.ellipse(cx, cy - hh, rx, ry)
    f.line((cx + rx + 18, cy), (cx + rx + 18, cy - hh), TEAL, 2, dash=True)
    f.text(cx + rx + 34, cy - hh / 2, 'h')
    # cone (right)
    kx, H_ = 430, 190
    f.poly([(kx - rx, cy), (kx + rx, cy), (kx, cy - H_)], fill=FILL, stroke='none', sw=0)
    f.ellipse(kx, cy, rx, ry, fill=FILL, stroke='none', sw=0)
    f.half_ellipse(kx, cy, rx, ry, front=False); f.half_ellipse(kx, cy, rx, ry, front=True)
    f.line((kx - rx, cy), (kx, cy - H_)); f.line((kx + rx, cy), (kx, cy - H_))
    f.line((kx, cy - H_), (kx, cy), TEAL, 2.5, dash=True)
    f.text(kx + 16, cy - H_ / 2, 'H')
    return f


def fig_cone_slant(r_lab='r', h_lab='h', l_lab='ℓ', title='A cone: radius, height and slant height form a right triangle'):
    f = Fig(title)
    cx, cy, rx, ry, hh = 320, 280, 105, 28, 200
    f.poly([(cx - rx, cy), (cx + rx, cy), (cx, cy - hh)], fill=FILL, stroke='none', sw=0)
    f.half_ellipse(cx, cy, rx, ry, front=False); f.half_ellipse(cx, cy, rx, ry, front=True)
    f.line((cx - rx, cy), (cx, cy - hh)); f.line((cx, cy - hh), (cx + rx, cy), TEAL, 3.5)
    if h_lab is not None:
        f.line((cx, cy - hh), (cx, cy), ORANGE, 2.5, dash=True)
        f.line((cx, cy - 10), (cx + 10, cy - 10), TEAL, 1.7); f.line((cx + 10, cy - 10), (cx + 10, cy), TEAL, 1.7)
        if h_lab: f.text(cx - 16, cy - hh / 2 + 10, h_lab)
    f.line((cx, cy), (cx + rx, cy), TEAL, 2.5)
    f.text(cx + rx / 2, cy + 42, r_lab)
    f.text(cx + rx / 2 + 22, cy - hh / 2 - 6, l_lab)
    return f


def fig_three_positions():
    f = Fig('Three 3 by 3 by 3 cubes: a corner cube, an edge cube and a face-center cube removed from the front')
    s = 30
    specs = [(40, 'corner', {(2, 0, 'front'): HL, (2, 0, 'top'): HL, (0, 0, 'right'): HL}),
             (250, 'edge', {(1, 0, 'front'): HL, (1, 0, 'top'): HL}),
             (460, 'face center', {(1, 1, 'front'): HL})]
    for x0, lab, mk in specs:
        cube_grid(f, 3, x0, 250, s, mk)
        f.text(x0 + 1.5 * s + 10, 285, lab, size=22)
    return f


def fig_box_diag(a='6', b='8', c='24'):
    f = Fig('A tall box 6 by 8 by 24 with the base diagonal and the body diagonal')
    def ex(f, P):
        f.line(P['A'], P['C'], TEAL, 2.5, dash=True)
        f.line(P['A'], P['G'], TEAL, 3)
    return box_fig(f.title, 250, 320, 95, 250, 105, labels=[(297, 342, a), (402, 308, b), (226, 195, c)], extra=ex)


def fig_pour():
    f = Fig('Water in a box with base 10 by 8 reaches height 9; an empty cube with edge 12')
    left = box_fig('', 60, 300, 150, 190, 90, water=120, labels=[(135, 322, '10'), (242, 296, '8'), (40, 240, '9')])
    right = box_fig('', 350, 300, 190, 190, 110, labels=[(445, 322, '12')])
    f.parts = left.parts + right.parts; f.xs = left.xs + right.xs; f.ys = left.ys + right.ys
    return f


def fig_turn():
    f = Fig('A right triangle turns about one leg and makes a cone')
    # triangle on the left with the axis
    f.poly([(120, 290), (220, 290), (120, 110)], fill=FILL)
    f.line((120, 320), (120, 80), TEAL, 2.5, dash=True)
    f.text(98, 200, '6'); f.text(170, 312, '3'); f.text(96, 95, '↻', size=30)
    f.line((120, 280), (130, 280), TEAL, 1.7); f.line((130, 280), (130, 290), TEAL, 1.7)
    f.text(300, 200, '→', size=36)
    # cone on the right
    cx, cy, rx, ry, hh = 470, 290, 100, 26, 180
    f.poly([(cx - rx, cy), (cx + rx, cy), (cx, cy - hh)], fill=FILL, stroke='none', sw=0)
    f.half_ellipse(cx, cy, rx, ry, front=False); f.half_ellipse(cx, cy, rx, ry, front=True)
    f.line((cx - rx, cy), (cx, cy - hh)); f.line((cx, cy - hh), (cx + rx, cy))
    f.line((cx, cy - hh), (cx, cy), TEAL, 2.5, dash=True)
    f.line((cx, cy), (cx + rx, cy), TEAL, 2.5)
    f.text(cx - 14, cy - hh / 2, '6'); f.text(cx + rx / 2, cy + 40, '3')
    return f


def fig_painted(n=3):
    f = Fig('A painted 3 by 3 by 3 cube: corner cubes have 3 painted faces, edge cubes 2, face-center cubes 1')
    mk = {}
    for c in range(3):
        for r in range(3):
            kind = (c in (0, 2)) + (r in (0, 2))
            col = {2: HL, 1: '#bfe6e0', 0: FRONT}[kind]
            mk[(c, r, 'front')] = col
    cube_grid(f, 3, 200, 300, 70, mk)
    return f


def fig_cube5():
    f = Fig('A painted cube cut into 5 small cubes along each edge')
    cube_grid(f, 5, 210, 320, 44)
    return f


def fig_p13():
    f = Fig('The square base of the cube with a few circular bases in one corner')
    f.poly([(194.857, 305.143), (445.143, 305.143), (445.143, 54.857), (194.857, 54.857)], fill='none')
    for cx, cy in [(215.714, 284.286), (257.429, 284.286), (215.714, 242.571)]:
        f.raw('<circle cx="%.3f" cy="%.3f" r="20.857" fill="#d5f1ed" stroke="#203344" stroke-width="1.3"/>' % (cx, cy))
    f.text(300, 284, '…', size=26); f.text(216, 200, '⋮', size=26)
    f.text(320, 328, '12'); f.text(470, 180, '12')
    return f


# =========================================================================================
# Editing helpers
# =========================================================================================
def VIS(svg, **k): return dict(k='vis', v={'type': 'geometry', 'svg': svg}, **k)
def RT(t, y, size=34): return T(t, size=size, x=1060, y=y, w=470)   # right-column board item on a question slide


def _script(M, vid, n):
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _fix(M, vid, n, key, old, new):
    b = M.slide(vid, n); hit = 0
    for l in b['lines']:
        if key in l and old in l[key]: l[key] = l[key].replace(old, new); hit += 1
    assert hit, (vid, n, old)
    M.touched_videos.add(vid)


def _fix_item(M, vid, n, old, new):
    b = M.slide(vid, n); hit = 0
    for it in b['items']:
        if it.get('t') == old: it['t'] = new; hit += 1
    assert hit, (vid, n, old)
    M.touched_videos.add(vid)


def _insert_say_after(M, vid, n, after_text, new_lines):
    b = M.slide(vid, n)
    k = next(i for i, l in enumerate(b['lines']) if after_text in (l.get('say') or l.get('draw') or ''))
    for j, s in enumerate(new_lines): b['lines'].insert(k + 1 + j, {'say': s} if isinstance(s, str) else {'draw': s[1]})
    M.touched_videos.add(vid)


def _set_q_figs(M, qid, fn):
    """Apply fn(svg) to the question figure and to every slide copy of it."""
    q = M.q(qid)
    M.set_q(qid, figure=fn(q['questionVisual']['svg']))
    for v in M.D['videos'].values():
        for b in v.get('beats', []):
            for it in b.get('items', []):
                if it.get('k') == 'q' and it.get('qid') == qid and it.get('fig'):
                    it['fig'] = dict(it['fig'], svg=fn(it['fig']['svg'])); M.touched_videos.add(v['id'])


def _set_q_fig_new(M, qid, fig):
    """New figure (Fig object): full 640x360 view for the question, tight view on the slides."""
    M.set_q(qid, figure=fig.svg())
    for v in M.D['videos'].values():
        for b in v.get('beats', []):
            for it in b.get('items', []):
                if it.get('k') == 'q' and it.get('qid') == qid and it.get('fig'):
                    it['fig'] = {'type': 'geometry', 'svg': fig.svg(tight=True)}; M.touched_videos.add(v['id'])


def _move_text(svg, label, x, y):
    new, n = re.subn(r'<text x="[\d.]+" y="[\d.]+"([^>]*)>%s</text>' % re.escape(label),
                     lambda m: '<text x="%.3f" y="%.3f"%s>%s</text>' % (x, y, m.group(1), label), svg)
    assert n == 1, label
    return new


def _drop_text(svg, label):
    new, n = re.subn(r'<text [^>]*>%s</text>' % re.escape(label), '', svg)
    assert n == 1, label
    return new


def _solution(M, qid, sidebar, group_title, num, intro, slides):
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for sl in slides:
        title, script = sl[0], sl[1]
        pre = sl[2] if len(sl) > 2 else [Q(qid, figw=0.56, figalign='left')]
        beats.append(dict(mode='question', active=sidebar.index('Question %d' % n), title=title, pre=pre, script=script))
    v = M.new_video('solve-' + qid, TOPIC, group_title, sidebar, beats, M.section_of(qid), kind='solution', qid=qid)
    v['beats'][0]['title'] = group_title
    v['hybrid']['num'] = num
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _lesson(M, vid, title, sidebar, slides, after, num):
    beats = [dict(mode='title', title=title, script=slides[0])]
    for k, sl in enumerate(slides[1:]):
        beats.append(dict(mode='concept', active=sidebar.index(sl[0]), title=sl[0], pre=[], script=sl[1]))
    v = M.new_video(vid, TOPIC, title, sidebar, beats, LEARN, after=after)
    v['hybrid']['num'] = num
    return v


def _american(t):
    for a, b in (('metre', 'meter'), ('litre', 'liter'), ('centre', 'center'), ('colour', 'color'),
                 ('practis', 'practic'), ('memoris', 'memoriz'), ('Centre', 'Center')):
        t = t.replace(a, b)
    return t


# Solution-video sidebars use the OLD question numbers; renumber_guided() maps them to the final order.
# New guided questions: 13 (water, group I), 14 (cone slant height, group II), 15 (painted cube, group II).
SB1 = ['Question %d' % n for n in (1, 2, 3, 4, 13)]
SB2 = ['Question %d' % n for n in (5, 6, 7, 8, 9, 10, 11, 12, 14, 15)]


def apply(M):
    S = M.set_q
    L1, L2 = 'geo-119', 'geo-120'

    # =====================================================================================
    # 1. Lesson "Solids: Surface and Volume" (geo-119)
    # =====================================================================================
    lying_prism = M.slide(L1, 3)['items'][0]['v']['svg']
    _fix(M, L1, 2, 'draw', 'Trace one edge in colour', 'Trace one edge in color')
    _fix(M, L1, 2, 'say', 'And the bottom face and the top face — we also call them bases.',
         'And the bottom face and the top face — we call them bases. In a box, any two opposite faces can be the bases.')
    # slide 3: an upright prism (the narration says "lift it straight up")
    M.slide(L1, 3)['items'][0]['v'] = {'type': 'geometry', 'svg': fig_upright_prism().svg(tight=True)}
    # new slide 4: the same prism lying on its side (as in Q4 and in practice)
    M.insert_slides(L1, 3, [dict(mode='concept', active=2, title='Lying down', script=[
        A('The same prism, lying on its side, appears', VIS(lying_prism, w=1000, h=520)),
        "Now the same prism — turned over. It lies on its side.",
        "Where are the bases now? Not at the bottom!",
        D('Shade triangles ABC and DEF'),
        "The bases are the two identical faces — the triangles ABC and DEF. Here they stand up, front and back.",
        A("'Bases = the two identical faces · height = the distance between them' appears",
          T('Bases $=$ the two identical faces · height $=$ the distance between them', size=34, x=410, y=650)),
        D('Trace the edge BE'),
        "The height is the distance between the bases. Here it's the edge BE — it lies flat.",
        "So don't look for the height going up. Find the two identical faces first. The height joins them.",
    ])])
    # old slide 10 (now 11): link ml to cm³
    _fix(M, L1, 11, 'say', "It always says on the can: 330 millilitres. That's a volume unit.",
         "It always says on the can: 330 milliliters. That's a volume unit.")
    _insert_say_after(M, L1, 11, 'A tiny cube, every edge one', [
        "And one milliliter is exactly one cubic centimeter. That can holds 330 cubic centimeters."])
    # formula page slide before the recap (old 14 -> now 15)
    M.insert_slides(L1, 14, [dict(mode='concept', active=13, title='On the formula page', script=[
        "Good news: at the start of every quantitative section there's a formula page.",
        A("'On the page' appears", T('On the page: box and cube (volume, surface area) · cylinder (lateral, total, volume) · cone volume · pyramid volume', size=34)),
        "These are on it: the volume and surface area of a box and a cube. The cylinder — lateral area, total surface area and volume. The volume of a cone and of a pyramid.",
        "So you don't have to panic about those formulas. Know where to find them.",
        A("'NOT on the page' appears", T('NOT on the page: perimeter $\\times$ height · base area $\\times$ height for any prism · cube diagonals · units', size=34)),
        "What's NOT on it: the general rules for any prism, the diagonals of a cube and a box, the angles in a cube, and the units.",
        "Those you need to know by heart. We'll collect them for you as we go.",
    ])])
    b = M.slide(L1, 16)   # recap: one more line
    M.set_slide(L1, 16, script=_script(M, L1, 16)[:-1] + [
        A("'Formula page' appears", T('Box, cylinder, cone, pyramid: on the formula page', size=38)),
        "And the basic formulas are on the formula page. Know them — but you can check them there.",
        "That's it for 3D definitions and formulas. From here — psychometric questions."])
    sb = ['Edge, face, base', 'Prism', 'Lying down', 'Cylinder', 'Lateral: unroll it', 'Box and cube lateral',
          'Perimeter × height', 'Total surface area', 'Box and cylinder', 'Volume', 'Base area × height',
          'Pointed: the cone', 'Pointed: the pyramid', 'On the formula page', 'Recap']
    M.set_sidebar(L1, sb)
    for b in M.video(L1)['beats']:
        if b['mode'] != 'title': b['active'] = sb.index(b['title'])

    # "Solids in Questions" (geo-120): what's ahead
    M.set_slide(L2, 2, script=[
        A('Volume and capacity appears', T('Volume and capacity — straight solid or pointed?', size=40)),
        'Volumes and capacity — the most important thing: is it a straight solid or a pointed one?',
        A('Water level appears', T('Water level · units · the cone’s slant height', size=40)),
        'Water poured from one container to another, liters and cubic centimeters, and the slant height of a cone.',
        A('Lateral and total surface area appears', T('Lateral area and total surface area', size=40)),
        'Lateral areas and total surface areas.',
        A('Cube facts appears', T('Volume ratios $\\cdot$ cube and box facts $\\cdot$ shortcuts', size=40)),
        'And the shortcuts — volume ratios, symmetry, and the facts about cubes and boxes. Try each question yourself first, then watch the solution.',
    ])

    # =====================================================================================
    # 2. Guided questions 1-12: solutions, wording, figures, wrong rule
    # =====================================================================================
    S('geo35-g121', expl=[
        'The cone holds $\\frac{\\pi(\\sqrt7)^2\\cdot9}{3}=21\\pi$ cm³ of water.',
        'Check each container. The box (choice 1): $7\\times3\\times3=63$, too small. The pyramid (choice 2): $\\frac{6^2\\times6}{3}=72$, big enough. '
        'The cube (choice 3): $4^3=64$, too small. The cylinder (choice 4): $\\pi(\\sqrt5)^2\\times4=20\\pi$, less than $21\\pi$.',
        'Since $65.1<21\\pi<66$, only the pyramid (72 cm³) can hold all the water.'])

    S('geo35-g122', expl=[
        'Let the common base area be B and the cone height be H. The cone volume is $\\frac{BH}{3}$ and the cylinder volume is $Bh$.',
        '$\\frac{BH}{3}=2Bh$. Divide by B and multiply by 3: $H=6h$.',
        'Trap: $3h$ gives equal volumes, not twice the volume.'])
    _set_q_fig_new(M, 'geo35-g122', fig_cone_cyl())   # side by side, no true proportions (the old one showed H = 6h)

    S('geo35-g123', stem='The volume of rectangular box ABCDEFGH is 216 cm³. M lies on AB so that the ratio AM : MB is 1 : 2, and N lies directly above M on EF. What is the volume of triangular prism AMD–ENH (in cm³)?',
      expl=['AM is $\\frac13$ of AB. The rectangle with sides AM and AD is $\\frac13$ of the base, and triangle AMD is half of that rectangle.',
            'So the triangle is $\\frac12\\cdot\\frac13=\\frac16$ of the base. The prism and the box have the same height. Therefore the prism is $\\frac16$ of the box: $216\\div6=36$ cm³.'])
    _fix_item(M, 'solve-geo35-g123', 3, '$216:6=36$', '$216\\div6=36$')
    _fix(M, 'solve-geo35-g123', 3, 'label', '216 : 6 = 36', '216 ÷ 6 = 36')

    S('geo35-g124', expl=[
        'The prism lies on its side. Its bases are the two right triangles, and its height is the edge between them, 4.',
        'The missing leg is 12, since $5^2+12^2=13^2$. The base perimeter is $5+12+13=30$.',
        'Lateral surface area $=30\\times4=120$ cm². (Adding the two triangles, $2\\times30=60$, gives the total surface area, 180.)'])
    _set_q_figs(M, 'geo35-g124', lambda s: _move_text(s, '13', 287, 200))   # 13 on the hypotenuse BC, not on the side face
    _insert_say_after(M, 'solve-geo35-g124', 2, 'A right prism whose base is a right triangle', [
        "Careful — this prism lies on its side. The bases are the two triangles, front and back.",
        "The height is the distance between them: the edge BE, 4. It lies flat — but it's the height."])

    S('geo35-g125', expl=[
        'For dimensions a, b, c the total surface area is $2(ab+ac+bc)$.',
        'Choice 1, $1\\times3\\times4$: $2(3+4+12)=38$. Choice 2, $2\\times2\\times3$: $2(4+6+6)=32$. Choice 3, $1\\times1\\times12$: $2(1+12+12)=50$. Choice 4, $1\\times2\\times6$: $2(2+6+12)=40$.',
        'The smallest is 32: the block closest to a cube.'])

    S('geo35-g126', expl=[
        'The box volume is $(2a)^2\\cdot3a=12a^3$.',
        'The circle is inscribed in the square with side 2a. Therefore its diameter is 2a and its radius is a. The cylinder volume is $\\pi a^2\\cdot3a=3\\pi a^3$.',
        'The part outside the cylinder: $\\frac{12a^3-3\\pi a^3}{12a^3}=1-\\frac{\\pi}{4}$.'])
    _set_q_figs(M, 'geo35-g126', lambda s: _drop_text(s, 'a'))   # the radius label was the key step
    _fix(M, 'solve-geo35-g126', 3, 'draw', 'Write (96 − 24π) : 96 = 1 − π/4', 'Write (96 − 24π)/96 = 1 − π/4')

    S('geo35-g127', expl=[
        'The pyramid has the same base and the same height as the cube. Therefore it is $\\frac13$ of the cube, and the part left is $\\frac23$.',
        'In ratio units, pyramid : left : cube = 1 : 2 : 3. Two units are 54, so one unit is $54\\div2=27$ cm³.'])
    _fix_item(M, 'solve-geo35-g127', 3, '$1$ unit $=54:2=27$', '$1$ unit $=54\\div2=27$')
    _fix(M, 'solve-geo35-g127', 3, 'label', '1 unit = 54 : 2 = 27', '1 unit = 54 ÷ 2 = 27')

    S('geo35-g128', expl=[
        'All lateral edges are equal. Therefore the apex P is above the center O of the square.',
        'The base diagonal is $2\\sqrt2\\cdot\\sqrt2=4$ (silver triangle: hypotenuse = leg $\\times\\sqrt2$). Half of it: $OB=2$.',
        'Triangle POB is right-angled at O: $h^2+2^2=5^2$, $h^2=21$, $h=\\sqrt{21}$.',
        'Check: the height must be less than the slanted edge, 5. Only $\\sqrt{21}$ is less than $\\sqrt{25}=5$.'])
    _set_q_figs(M, 'geo35-g128', lambda s: _move_text(s, '5', 348, 199))   # 5 on edge PB, not in the middle of face PBC
    sc = _script(M, 'solve-geo35-g128', 3)
    k = sc.index('The diagonals cut the square into 4 silver triangles — right and isosceles.')
    sc[k + 1:k + 1] = [A("'Silver: hypotenuse = leg × √2' appears", RT('Silver (45°-45°-90°): hypotenuse $=$ leg $\\times\\sqrt2$', 200, 30)),
                       "Remember the silver triangle: angles 45, 45, 90. The hypotenuse is the leg times root 2."]
    M.set_slide('solve-geo35-g128', 3, script=sc)

    S('geo35-g129', expl=[
        'BD, DG and GB are diagonals of equal square faces. Therefore all three are equal: $3\\sqrt2\\cdot\\sqrt2=6$.',
        'Triangle BDG is equilateral with side 6. Its area is $\\frac{6^2\\sqrt3}{4}=9\\sqrt3$ cm².'])
    # wrong rule: "edge and a diagonal of ANOTHER face -> 90°" (edge AB and diagonal EG make 45°)
    V9 = 'solve-geo35-g129'
    _fix_item(M, V9, 5, 'Edge and a diagonal of another face $\\rightarrow90°$',
              'Edge $+$ diagonal of the face it stands on (same corner) $\\rightarrow90°$')
    _fix(M, V9, 5, 'label', 'Edge ⊥ a diagonal of another face → 90°', 'Edge + diagonal of the face it stands on → 90°')
    _fix_item(M, V9, 5, 'Two diagonals of different faces $\\rightarrow60°$', 'Two face diagonals from the same corner $\\rightarrow60°$')
    _fix(M, V9, 5, 'say', 'One: an edge and a diagonal on the face it stands on. The edge is perpendicular to the base — 90 degrees.',
         'One: an edge that stands on a face, and a diagonal of THAT face, from the same corner. The edge is perpendicular to the whole face — 90 degrees.')
    _insert_say_after(M, V9, 5, 'The edge is perpendicular to the whole face', [
        "Careful: not just any edge and any diagonal. They must meet at one corner, and the edge must stand on that face. Otherwise the angle can be 45, or something else."])

    V10 = 'solve-geo35-g130'
    _fix(M, V10, 2, 'say', 'And angle AEG is 90 — we just learned it: an edge and a diagonal of another face.',
         'And angle AEG is 90 — we just learned it: edge AE stands on the top face, and EG is a diagonal of that face, from the same corner E.')
    _fix_item(M, V10, 3, 'Diagonal $18\\rightarrow$ edge $\\frac{18}{\\sqrt3}=6\\sqrt3$',
              'Diagonal $18\\rightarrow$ edge $\\frac{18}{\\sqrt3}=\\frac{18\\sqrt3}{3}=6\\sqrt3$')
    _insert_say_after(M, V10, 3, 'The other way round? Diagonal 18', [
        "Why does it work? Multiply the top and the bottom by root 3: 18 root 3 over 3. And 18 over 3 is 6.",
        "Same with root 2: 18 over root 2 is 18 root 2 over 2 — 9 root 2. Divide by the number under the root, keep the root."])
    # slide 4: the original slide (question with its edge-2 cube stays on the left) + the one-step box diagonal
    M.set_slide(V10, 4, script=[
        'What about a box?',
        "Unlike a cube, the edges aren't all equal. There's no fixed ratio.",
        'What we do: build two right triangles, like we did in this question.',
        A('Box 6 × 8 × 24 appears', RT('Box $6\\times8\\times24$', 280, 36)),
        'A box: 6 by 8, height 24. How long is the inner diagonal?',
        A('Base: 6, 8 → 10 appears', RT('Base: $6,\\ 8\\rightarrow10$', 350, 36)),
        'First the diagonal of the base: 6, 8 — the right angle there — a 3-4-5 triple times 2. 10.',
        A('10, 24 → 26 appears', RT('$10,\\ 24\\rightarrow26$', 420, 36)),
        'Now with the height, another right triangle: 10 and 24. 5-12-13 times 2 — hamsa, bat mitzvah, bar mitzvah. 26.',
        A('One step appears', RT('One step: $\\sqrt{6^2+8^2+24^2}=\\sqrt{676}=26$', 500, 30)),
        'Or in one step: the root of 6 squared plus 8 squared plus 24 squared. Root 676 — 26.',
        'In a cube — a fixed ratio. In a box — two right triangles, or the root of the three squares.',
    ])

    S('geo35-g131', expl=[
        'Solid cubes are not water: count each direction and drop the remainder.',
        'Length: $10\\div3=3$ cubes (remainder 1). Width: $7\\div3=2$ (remainder 1). Height: $8\\div3=2$ (remainder 2).',
        '$3\\times2\\times2=12$. Trap: dividing volumes, $560\\div27\\approx20.7$, treats the cubes like water.'])
    for old, new, lo, ln in [('$10:3=3$ (remainder 1)', '$10\\div3=3$ (remainder 1)', '10 : 3 = 3 (+1)', '10 ÷ 3 = 3 (+1)'),
                             ('$7:3=2$ (remainder 1)', '$7\\div3=2$ (remainder 1)', '7 : 3 = 2 (+1)', '7 ÷ 3 = 2 (+1)'),
                             ('$8:3=2$ (remainder 2)', '$8\\div3=2$ (remainder 2)', '8 : 3 = 2 (+2)', '8 ÷ 3 = 2 (+2)')]:
        _fix_item(M, 'solve-geo35-g131', 3, old, new); _fix(M, 'solve-geo35-g131', 3, 'label', lo, ln)

    S('geo35-g132', expl=[
        'The removed cube has volume $2^3=8$ cm³. The volume goes down by 8.',
        'The corner cube showed 3 faces, each $2\\times2=4$ cm². Removing it loses those 3 faces, but 3 faces of its neighbors appear.',
        'Lose 3, gain 3: the surface area does not change.'])
    # slide 3: picture the three positions (the old slide showed only the corner)
    sc = _script(M, 'solve-geo35-g132', 3)
    M.set_slide('solve-geo35-g132', 3, mode='concept', pre=[], script=[sc[0],
        A('Three cubes appear: corner, edge, face center', VIS(fig_three_positions().svg(tight=True), w=620, h=260, x=390, y=250))] + sc[1:])

    # existing solution videos: sidebars with the new question numbers
    for v in M.D['videos'].values():
        if v['topic'] == TOPIC and v.get('kind') == 'solution':
            M.set_sidebar(v['id'], SB1 if v['hybrid'].get('num') == 67 else SB2)
            for b in v['beats']:
                if b['mode'] != 'title':
                    b['active'] = (SB1 if v['hybrid'].get('num') == 67 else SB2).index(v['beats'][0]['bigTitle'])

    # =====================================================================================
    # 3. New lesson: Water Level (after Question 1) + guided question
    # =====================================================================================
    WV = 'r26-t35-water'
    _lesson(M, WV, 'Water Level', ['Height = volume ÷ base', 'Pouring', 'Liters and cm³', 'Recap'], [
        ["Water in containers.", "It's just the volume formula, turned around."],
        ('Height = volume ÷ base', [
            A("'V = base area × height' appears", T('$V=$ base area $\\times$ height', size=46)),
            "We know: volume equals base area times height.",
            "Water in a straight container takes its shape. The water itself is a box — or a cylinder.",
            A("'Water height = V ÷ base area' appears", T('Water height $=\\frac{V}{\\text{base area}}$', size=46)),
            "Turn it around: the height of the water is the volume divided by the base area.",
            D('Write "720 cm³ in a box with base 12 × 10: 720 ÷ 120 = 6 cm"'),
            "720 cubic centimeters of water, in a box with a base of 12 by 10. The base area is 120.",
            "720 over 120 — the water is 6 centimeters high.",
        ]),
        ('Pouring', [
            A("'Pouring: the volume stays the same' appears", T('Pouring: the VOLUME stays the same — not the height', size=42)),
            "Water is poured from one container into another. What stays the same? The volume. Not the height!",
            A("'Step 1' appears", T('Step 1: the volume in the first container', size=40)),
            D('Write "cylinder r = 2, water 9 high: V = π · 2² · 9 = 36π"'),
            "A cylinder with radius 2, water 9 high. The volume: pi times 4 times 9 — 36 pi.",
            A("'Step 2' appears", T('Step 2: volume $\\div$ the new base area', size=40)),
            D('Write "into a cylinder with r = 3: 36π ÷ 9π = 4 cm"'),
            "Pour it into a cylinder with radius 3. Its base is 9 pi. 36 pi over 9 pi — 4 centimeters.",
            "A wider container — lower water. It makes sense.",
        ]),
        ('Liters and cm³', [
            "Units. Often the water is in liters and the container is in centimeters.",
            A("'1 ml = 1 cm³' appears", T('$1$ ml $=1\\text{ cm}^3$', size=46)),
            "One milliliter is exactly one cubic centimeter.",
            A("'1 liter = 1000 cm³' appears", T('$1$ liter $=1000\\text{ cm}^3$ (a cube $10\\times10\\times10$)', size=42)),
            "One liter is a thousand cubic centimeters — a cube, 10 by 10 by 10.",
            A("'1 m³ = 1,000,000 cm³' appears", T('$1\\text{ m}^3=100\\cdot100\\cdot100=1{,}000{,}000\\text{ cm}^3$', size=40)),
            "And a cubic meter: 100 by 100 by 100 — a million cubic centimeters.",
            D('Write "2 liters into a box with base 20 × 10: 2000 ÷ 200 = 10 cm"'),
            "2 liters into a box with a base of 20 by 10. 2000 over 200 — 10 centimeters.",
            "First the same units. Then compare or divide.",
        ]),
        ('Recap', [
            A("'Height' appears", T('Water height $=$ volume $\\div$ base area', size=40)),
            A("'Pouring' appears", T('Pouring: same volume, new base', size=40)),
            A("'Units' appears", T('$1$ liter $=1000\\text{ cm}^3$ · $1$ ml $=1\\text{ cm}^3$', size=40)),
            "Height is volume over base area. Pouring keeps the volume.",
            "And check the units first. Now try a question.",
        ]),
    ], after='solve-geo35-g121', num=66)

    g1 = 'q-r26-t35-01'
    M.new_q(g1, TOPIC,
            'Water in a box-shaped container with a base of 10 cm × 8 cm reaches a height of 9 cm. All the water is poured into an empty cube-shaped container with an internal edge of 12 cm. How high is the water in the cube (in cm)?',
            ['$9$', '$6$', '$5$', '$7.5$'], 3,
            ['The volume of the water: $10\\times8\\times9=720$ cm³. It does not change when we pour.',
             'The base of the cube: $12\\times12=144$ cm². The new height: $720\\div144=5$ cm.',
             'Trap: 9 cm. The height does not stay the same; the volume does.'],
            figure=fig_pour().svg())
    M.place_q(g1, LEARN, after=WV)
    _solution(M, g1, SB1, '3D Questions I', 67, ["Water poured from a box into a cube.", "One idea: the volume does not change."], [
        ('The volume stays', [
            "Water in a box, 10 by 8, 9 high. It's poured into a cube with edge 12. How high is it now?",
            "Step one: how much water? A box — multiply.",
            A("'V = 720' appears", RT('$V=10\\cdot8\\cdot9=720$', 280, 36)),
            "10 times 8 is 80, times 9 — 720 cubic centimeters.",
            "Step two: the new base. The cube's base is 12 by 12 — 144.",
            A("'h = 720 ÷ 144 = 5' appears", RT('$h=720\\div144=5$', 360, 36)),
            "720 over 144 — 5 centimeters.",
            D('Circle choice 3'),
            "Choice three.",
        ]),
        ('Check it', [
            "Does it make sense? The new base, 144, is bigger than the old one, 80. More floor — lower water. 5 is less than 9. Good.",
            A("'Trap: 9' appears", RT('Trap: 9 — the height does not carry over', 280, 32)),
            "Choice one, 9, is the trap. The height doesn't carry over. The volume does.",
            A("'Shortcut' appears", RT('Shortcut: $9\\times\\frac{80}{144}=5$', 360, 34)),
            "A shortcut: the base got bigger by 144 over 80. So the height gets smaller by the same fraction: 9 times 80 over 144 — 5.",
            D('Circle choice 3'),
        ]),
    ])

    # =====================================================================================
    # 4. New lesson: cones - slant height and solids made by turning (after Question 8)
    # =====================================================================================
    CV = 'r26-t35-cones'
    _lesson(M, CV, 'Cones: Slant Height and Turning', ['Slant height', 'Turn a rectangle', 'Turn a right triangle', 'Recap'], [
        ["Two more cone ideas from the exam.", "The slant height — and solids you make by turning a flat shape."],
        ('Slant height', [
            A('A cone with r, h and ℓ appears', VIS(fig_cone_slant().svg(tight=True), w=620, h=420)),
            "Look at a cone from the side. The height h goes straight down inside it, from the tip to the center of the base.",
            "The slant height, ℓ, runs along the outside — from the tip to the edge of the base.",
            A("'r² + h² = ℓ²' appears", T('$r^2+h^2=\\ell^2$ — the slant height is the longest', size=42)),
            "The radius, the height and the slant height make a right triangle. The slant height is the hypotenuse — the longest side.",
            D('Write "r = 3, ℓ = 5 → h = 4"'),
            "Radius 3, slant height 5: a 3-4-5 triangle. The height is 4.",
            "The same idea as the pyramid in the last question: find the right triangle inside the solid.",
        ]),
        ('Turn a rectangle', [
            "Take a rectangle and turn it one full turn around one of its sides. What do you get? A cylinder.",
            A("'Rectangle about a side → cylinder' appears", T('Rectangle turns about a side $\\rightarrow$ cylinder', size=42)),
            "The side on the axis stays where it is — it's the height. The other side sweeps a circle — it's the radius.",
            A("'Side on the axis = height · other side = radius' appears", T('Side on the axis $=$ height · the other side $=$ radius', size=40)),
            D('Write "4 × 2, about the 4 side: r = 2, h = 4 → V = π · 2² · 4 = 16π"'),
            "A 4 by 2 rectangle, turned about the side of 4: radius 2, height 4. 16 pi.",
        ]),
        ('Turn a right triangle', [
            A('A right triangle turning into a cone appears', VIS(fig_turn().svg(tight=True), w=820, h=380)),
            "A right triangle turned around one of its legs makes a cone.",
            A("'Right triangle about a leg → cone' appears", T('Right triangle about a leg $\\rightarrow$ cone', size=40)),
            "Again: the leg on the axis is the height. The other leg is the radius. The hypotenuse becomes the slant height.",
            D('Write "about the 6 leg: r = 3, h = 6 → V = π · 9 · 6 ÷ 3 = 18π"'),
            "Legs 3 and 6, about the leg of 6: radius 3, height 6. 18 pi.",
            D('Write "about the 3 leg: r = 6, h = 3 → V = π · 36 · 3 ÷ 3 = 36π"'),
            "About the leg of 3: radius 6, height 3. 36 pi — twice as much!",
            "So which side is on the axis matters. The radius is squared — it counts more.",
        ]),
        ('Recap', [
            A("'Slant' appears", T('Cone: $r^2+h^2=\\ell^2$ — the slant height is not the height', size=38)),
            A("'Rectangle' appears", T('Rectangle about a side $\\rightarrow$ cylinder', size=38)),
            A("'Triangle' appears", T('Right triangle about a leg $\\rightarrow$ cone', size=38)),
            A("'Axis' appears", T('The side on the axis $=$ the height', size=38)),
            "Slant height: the hypotenuse of the inner triangle. Turning: the side on the axis is the height.",
            "Now a question.",
        ]),
    ], after='solve-geo35-g128', num=66)

    g2 = 'q-r26-t35-02'
    M.new_q(g2, TOPIC, 'A cone has a base radius of 6 cm and a slant height of 10 cm. What is its volume (in cm³)?',
            ['$120\\pi$', '$96\\pi$', '$288\\pi$', '$360\\pi$'], 2,
            ['The radius, the height and the slant height form a right triangle. The slant height, 10, is the hypotenuse.',
             '$h^2+6^2=10^2$, $h^2=64$, $h=8$ (the 3-4-5 triangle times 2).',
             'Volume: $\\frac{\\pi\\cdot6^2\\cdot8}{3}=\\frac{288\\pi}{3}=96\\pi$ cm³.',
             'Traps: $120\\pi$ uses 10 as the height; $288\\pi$ forgets to divide by 3.'],
            figure=fig_cone_slant(r_lab='6', h_lab='', l_lab='10', title='A cone with base radius 6 and slant height 10').svg())
    M.place_q(g2, LEARN, after=CV)
    _solution(M, g2, SB2, '3D Questions II', 68, ["A cone and its slant height.", "The trap: the slant height is not the height."], [
        ('Find the height', [
            "Radius 6, slant height 10. What's the volume?",
            "The volume of a cone: pi r squared h, over 3. We have r. We need h.",
            "10 is the slant height — along the outside. It is not the height!",
            D('Highlight the right triangle: height, radius, slant height'),
            "The height, the radius and the slant height make a right triangle. The slant height is the hypotenuse.",
            A("'6, ?, 10 → h = 8' appears", RT('$6,\\ h,\\ 10$: 3-4-5 times 2 $\\rightarrow h=8$', 280, 34)),
            "6 and 10 — that's 3, 4, 5 times 2. The height is 8.",
        ]),
        ('The volume', [
            A("'V = 96π' appears", RT('$V=\\frac{\\pi\\cdot36\\cdot8}{3}=96\\pi$', 280, 36)),
            "Pi times 36 times 8, over 3. 36 over 3 is 12. 12 times 8 — 96 pi.",
            D('Circle choice 2'),
            "Choice two.",
            A("'Traps' appears", RT('$120\\pi$: 10 used as the height · $288\\pi$: no $\\div3$', 380, 30)),
            "Choice one, 120 pi, is for whoever used 10 as the height. Choice three forgot to divide by 3.",
        ]),
    ])

    # =====================================================================================
    # 5. New lesson: Cube and Box Facts (after Question 12) + guided painted-cube question
    # =====================================================================================
    FV = 'r26-t35-cubefacts'
    fsb = ['Diagonals', 'Angles in a cube', 'Faces, edges, vertices', 'Painted cube', 'Three faces → volume', 'Quick checks']
    _lesson(M, FV, 'Cube and Box Facts', fsb, [
        ["All the cube and box facts in one place.", "Some you met in the questions. Some are new. None of them are on the formula page."],
        ('Diagonals', [
            A("'a√2 and a√3' appears", T('Cube: face diagonal $=a\\sqrt2$ · body diagonal $=a\\sqrt3$', size=40)),
            "In a cube with edge a: the diagonal of a face is a root 2. The diagonal through the inside is a root 3.",
            A("'Box: d = √(a² + b² + c²)' appears", T('Box: body diagonal $=\\sqrt{a^2+b^2+c^2}$', size=40)),
            "In a box: the root of a squared plus b squared plus c squared. It's the two right triangles in one step.",
            D('Write "3 × 4 × 12: √(9 + 16 + 144) = √169 = 13"'),
            "3 by 4 by 12: 9 plus 16 plus 144 — 169. The diagonal is 13.",
            "It's also the longest rod that fits inside the box.",
        ]),
        ('Angles in a cube', [
            A("'90°' appears", T('Edge $+$ diagonal of the face it stands on, same corner $\\rightarrow90°$', size=36)),
            "An edge that stands on a face, and a diagonal of that face from the same corner: 90 degrees.",
            A("'45°' appears", T('Edge $+$ diagonal of the same face $\\rightarrow45°$', size=36)),
            "An edge and a diagonal of the same face: 45.",
            A("'60°' appears", T('Two face diagonals from the same corner $\\rightarrow60°$', size=36)),
            "Two diagonals of different faces, from the same corner: 60 — the third diagonal closes an equilateral triangle.",
            "They must meet at the same corner. Otherwise, check with a picture.",
        ]),
        ('Faces, edges, vertices', [
            "Counting questions. Take a prism whose base has n sides.",
            A("'Prism' appears", T('Prism, base with $n$ sides: $n+2$ faces · $3n$ edges · $2n$ vertices', size=36)),
            "Faces: n side walls, plus 2 bases — n plus 2. Edges: n at the bottom, n at the top, n going up — 3n. Vertices: n at the bottom, n at the top — 2n.",
            D('Write "cube: n = 4 → 6 faces, 12 edges, 8 vertices ✓"'),
            "Check on a cube: n is 4. 6 faces, 12 edges, 8 vertices. Right.",
            A("'Pyramid' appears", T('Pyramid, base with $n$ sides: $n+1$ faces · $2n$ edges · $n+1$ vertices', size=36)),
            "A pyramid: n walls plus the base — n plus 1 faces. n edges around the base, n up to the tip — 2n. n corners plus the tip — n plus 1 vertices.",
        ]),
        ('Painted cube', [
            A('A painted 3 by 3 by 3 cube appears', VIS(fig_painted().svg(tight=True), w=520, h=380)),
            "A big cube is painted on the outside. Then it's cut into n by n by n small cubes. How many small cubes have paint on 3 faces? On 2? On 1?",
            A("'3 faces: 8' appears", T('3 painted faces: $8$ (the corners)', size=36)),
            "3 painted faces — only the corners. Always 8.",
            A("'2 faces' appears", T('2 faces: $12(n-2)$ (on the edges)', size=36)),
            "2 painted faces — on the edges, without the corners. Each of the 12 edges has n minus 2 of them.",
            A("'1 face, 0 faces' appears", T('1 face: $6(n-2)^2$ · no paint: $(n-2)^3$', size=36)),
            "1 painted face — the middle of each face: n minus 2, squared, times 6 faces. No paint — the inside: n minus 2, cubed.",
            D('Write "n = 3: 8 + 12 + 6 + 1 = 27 ✓"'),
            "Check with n = 3: 8 plus 12 plus 6 plus 1 — 27. All of them.",
        ]),
        ('Three faces → volume', [
            "Sometimes they give the areas of three faces that meet at a corner — not the edges.",
            A("'V = √(ab · bc · ca)' appears", T('Face areas $ab,\\ bc,\\ ca$ $\\rightarrow V=\\sqrt{ab\\cdot bc\\cdot ca}$', size=40)),
            "Multiply the three areas: a b times b c times c a. Each edge appears twice. That's a b c, squared — the volume squared.",
            D('Write "6, 10, 15 → √(6 · 10 · 15) = √900 = 30"'),
            "Areas 6, 10 and 15: the product is 900. The volume is 30.",
        ]),
        ('Quick checks', [
            "Before you calculate — cross out what's impossible.",
            A("'Size checks' appears", T('Height $<$ slant edge · a part $<$ the whole · a fraction of a volume is between 0 and 1', size=34)),
            "The height is shorter than any slanted edge. A part of a solid is smaller than the whole.",
            A("'Solids are not water' appears", T('Solids in a box: count each direction — try each position', size=36)),
            "Solids in a box aren't water. Count each direction. Bricks that aren't cubes? Try each way of turning them — the count can change.",
            A("'Units' appears", T('Same units first: $1$ liter $=1000\\text{ cm}^3$', size=36)),
            "And compare only in the same units. Now a question.",
        ]),
    ], after='solve-geo35-g132', num=66)

    g3 = 'q-r26-t35-03'
    M.new_q(g3, TOPIC,
            'A wooden cube is painted on all six faces. Then it is cut into 125 identical small cubes, 5 along each edge. How many small cubes have paint on exactly one face?',
            ['$36$', '$54$', '$27$', '$150$'], 2,
            ['A small cube with exactly one painted face lies in the middle part of a big face — not on an edge and not on a corner.',
             'Each big face has a $3\\times3$ middle ($5-2=3$): 9 cubes. Six faces: $6\\times9=54$.',
             'Check: $8+12\\times3+54+3^3=8+36+54+27=125$. Traps: 36 have two painted faces; 27 have no paint.'],
            figure=fig_cube5().svg())
    M.place_q(g3, LEARN, after=FV)
    _solution(M, g3, SB2, '3D Questions II', 68, ["A painted cube.", "Count by position: corner, edge, or the middle of a face."], [
        ('Where are they?', [
            "125 small cubes, 5 along each edge. How many have exactly one painted face?",
            "Where is such a cube? Not on a corner — that has 3. Not on an edge — that has 2. In the middle of a face.",
            D('On the front face, mark the 3 × 3 middle'),
            "On each face, take off the border. 5 minus 2 is 3. A 3 by 3 middle — 9 cubes.",
            A("'6 × 3² = 54' appears", RT('$6\\times3^2=6\\times9=54$', 280, 36)),
            "6 faces, 9 on each — 54.",
            D('Circle choice 2'),
            "Choice two.",
        ]),
        ('Check the whole cube', [
            A("'8 + 36 + 54 + 27 = 125' appears", RT('$8+36+54+27=125$ ✓', 280, 36)),
            "Check: 8 corners. 12 edges with 3 each — 36. 54 on the faces. And the inside, 3 cubed — 27. Together 125. Everything fits.",
            "And the traps: 36 is the number with two painted faces. 27 is the number with no paint at all.",
            D('Circle choice 2'),
        ]),
    ])

    # =====================================================================================
    # 6. Memory cards
    # =====================================================================================
    c = M.card('mem-solids')
    c['tables'].append({'title': 'Water and units', 'head': ['Question', 'Rule'], 'rows': [
        ['Water height', 'volume \\(\\div\\) base area'],
        ['Pouring into another container', 'the volume stays the same — find it, then \\(\\div\\) the new base area'],
        ['!Units', '\\(1\\) ml \\(=1\\text{ cm}^3\\) · \\(1\\) liter \\(=1000\\text{ cm}^3\\) · \\(1\\text{ m}^3=1{,}000{,}000\\text{ cm}^3\\)']]})
    c['tables'].append({'title': 'Cones', 'head': ['Idea', 'Rule'], 'rows': [
        ['!Slant height \\(\\ell\\)', '\\(r^2+h^2=\\ell^2\\) — the slant height is not the height'],
        ['Rectangle turns about a side', 'cylinder: side on the axis \\(=h\\), other side \\(=r\\)'],
        ['Right triangle turns about a leg', 'cone: leg on the axis \\(=h\\), other leg \\(=r\\)']]})
    c['tips'] = c['tips'] + [
        'Bases = the two identical faces; height = the distance between them, even when the solid lies on its side.',
        'On the formula page: box, cube, cylinder, cone and pyramid formulas. Not on it: the general prism rules, diagonals, units.']

    c = M.card('mem-cube-facts')
    c['intro'] = 'Diagonals, angles, counting and the cube-removing situations. None of these are on the formula page.'
    for t in c['tables']:
        if t['title'].startswith('Segments'):
            t['rows'][2] = ['Box body diagonal', '\\(\\sqrt{a^2+b^2+c^2}\\) (or two right triangles)']
        if t['title'] == 'Angles in a cube':
            t['rows'] = [['An edge and a diagonal of the face it stands on, from the same corner', '\\(90°\\)'],
                         ['An edge and a diagonal of the same face', '\\(45°\\)'],
                         ['!Two face diagonals from the same corner', '\\(60°\\)']]
        for r in t['rows']:
            r[0] = _american(r[0])
    c['tables'] += [
        {'title': 'Counting (base with \\(n\\) sides)', 'head': ['Solid', 'Faces', 'Edges', 'Vertices'], 'rows': [
            ['Prism', '\\(n+2\\)', '\\(3n\\)', '\\(2n\\)'], ['Pyramid', '\\(n+1\\)', '\\(2n\\)', '\\(n+1\\)']]},
        {'title': 'Painted cube, cut \\(n\\times n\\times n\\)', 'head': ['Painted faces', 'How many'], 'rows': [
            ['3 (corners)', '\\(8\\)'], ['2 (edges)', '\\(12(n-2)\\)'], ['1 (middle of a face)', '\\(6(n-2)^2\\)'], ['0 (inside)', '\\((n-2)^3\\)']]}]
    c['tips'] = [_american(t) for t in c['tips']] + [
        'Three face areas \\(ab,\\ bc,\\ ca\\) → volume \\(=\\sqrt{ab\\cdot bc\\cdot ca}\\).',
        'Bricks in a box: try every position — the count can change.']

    # =====================================================================================
    # 7. Practice: text, figures, removals, new items, order
    # =====================================================================================
    S('geo35-core-p01', expl=[
        'A rectangle turned about a side makes a cylinder. The side on the axis, 5, is the height. The other side, 3, is the radius.',
        'Volume: $\\pi\\cdot3^2\\cdot5=45\\pi$ cm³. Trap: $75\\pi$ swaps the radius and the height.'])
    S('geo35-core-p03', expl=[
        'The two square faces are opposite each other. The edges are 4, 4 and h: $16h=112$, $h=7$.',
        'Each rectangular face: $4\\times7=28$ cm².'])
    S('geo35-core-p04', expl=[
        'The cone is $\\frac13$ of the cylinder. The part left is $\\frac23$.',
        'The ratio of the remaining volume to the removed volume is $\\frac23:\\frac13=2:1$. (The numbers 4 and 6 are not needed.)'])
    S('geo35-core-p06', expl=[
        '$DN=DC-NC=8-3=5$. The base AMND is a trapezoid with parallel sides $AM=3$ and $DN=5$ and height $AD=4$.',
        'Its area: $\\frac{(3+5)\\cdot4}{2}=16$. The volume: $16\\times5=80$ cm³.'])
    S('geo35-core-p07', expl=[
        'Solid A: 5 edges around the shared pentagon, 5 up to the top apex and 5 down to the bottom apex — 15 edges. A cube has 12 edges.',
        'The ratio is $\\frac{15}{12}=\\frac54$.'])
    S('geo35-core-p08',
      stem='The base of a rectangular box is square ABCD. M lies on AB and N lies on DC. Given:\n$\\begin{cases} AM=\\frac13AB \\\\ DN=\\frac23DC \\end{cases}$\nVertical planes through AN and MC divide the box into a middle prism with base AMCN and two outer prisms. What is the ratio of the combined outer volumes to the middle volume?',
      expl=['$NC=DC-DN=\\frac13$ of the side, and $AM=\\frac13$ of the side. AMCN is a parallelogram with base AM and height AD.',
            'Its area is $\\frac13$ of the square. The two outer parts make $\\frac23$.',
            'All three prisms have the same height. Therefore the ratio of the volumes is $\\frac23:\\frac13=2:1$.'])
    S('geo35-core-p09', expl=[   # restored original (pass 2)
        'Edge EA is perpendicular to the top face EFGH. So it is perpendicular to every line in that face that passes through E, including the diagonal EG.',
        'Therefore angle AEG $=90°$.'])
    S('geo35-core-p10',
      stem='Twelve cubes, each with edge 3 cm, form the stepped solid shown in the accompanying figure. The highlighted cube is removed. What is the change in the total surface area (in cm²)?',
      expl=['The highlighted cube shows 3 faces: front, top and bottom. It touches 3 cubes: left, right and behind.',
            'Removing it loses its 3 faces and uncovers 3 faces of its neighbors. Each face is $3\\times3=9$ cm²: $-27+27=0$.'])
    S('geo35-core-p12', expl=[
        'Let the common edge be a and the other edges b and c. The two faces are ab and ac: $(ab)(ac)=a^2bc=350$.',
        'The volume is $abc=140$. Divide: $\\frac{a^2bc}{abc}=a=\\frac{350}{140}=\\frac52$.'])
    S('geo35-core-p13', expl=[
        'Each diameter is 2 cm. Along each 12 cm side: $12\\div2=6$ cylinders. One layer: $6\\times6=36$.',
        'Height: $12\\div4=3$ layers. Total: $36\\times3=108$.'])
    _set_q_fig_new(M, 'geo35-core-p13', fig_p13())   # the old figure drew the full 6 x 6 layer
    S('geo35-core-p15', expl=[
        'The volume: $3\\times2\\times\\frac32=9$ cm³. The block lasts longest when only $\\frac38$ cm³ is used each day.',
        '$9\\div\\frac38=9\\times\\frac83=24$ days.'])
    S('geo35-core-p16', expl=[
        'The full cylinder: $\\pi\\cdot3^2\\cdot8=72\\pi$.',
        'A 150° sector is $\\frac{150}{360}=\\frac5{12}$ of the circle (as in the circles topic). The solid is the same fraction of the cylinder: $\\frac5{12}\\times72\\pi=30\\pi$ cm³.'])
    S('geo35-core-p17', expl=[
        'The square is inscribed in the circle. Its diagonal is the diameter, 10. Its area: $\\frac{10^2}{2}=50$. The circle area: $25\\pi$.',
        'Both solids have the same height. Therefore the volume ratio equals the ratio of the base areas: $\\frac{25\\pi-50}{50}=\\frac{\\pi}{2}-1$.'])
    S('geo35-core-p18', expl=[
        'Each diameter is 6. The base of the box is $12\\times6$ and its height is 7.',
        'Volume: $12\\times6\\times7=504$ cm³.'])
    S('geo35-core-p22', expl=[
        'Lateral area: $2\\pi\\cdot4\\cdot h=48\\pi$. Therefore $8h=48$ and $h=6$.',
        'Volume: $\\pi\\cdot4^2\\cdot6=96\\pi$ cm³.'])
    S('geo35-core-p23', expl=[
        'With edges a, b, c the three faces are ab, bc and ca: $(ab)(bc)(ca)=(abc)^2$.',
        'Therefore $V=\\sqrt{12\\times18\\times24}=\\sqrt{5184}=72$ cm³.'])
    _set_q_figs(M, 'geo35-core-p25', lambda s: re.sub(r'<line x1="185.564" y1="297.089" x2="454.436" y2="62.911"[^>]*/>', '', s))  # no body diagonal drawn
    # p27 (each dimension x 3/4 -> volume x 27/64) needs the k³ rule of topic 36: move it there
    M.move('geo35-core-p27', 'geo36-core-practice')

    new = [
        ('q-r26-t35-04', 'A box-shaped tank has internal dimensions 50 cm × 40 cm × 30 cm. How many liters of water does it hold when it is full?',
         ['$600$', '$6$', '$6{,}000$', '$60$'], 4,
         ['Volume: $50\\times40\\times30=60{,}000$ cm³.', '1 liter = 1000 cm³: $60{,}000\\div1000=60$ liters.']),
        ('q-r26-t35-05', 'A cylinder with radius 3 cm contains water to a height of 8 cm. All the water is poured into an empty cylinder with radius 6 cm. How high is the water now (in cm)?',
         ['$1$', '$4$', '$16$', '$2$'], 4,
         ['Water volume: $\\pi\\cdot3^2\\cdot8=72\\pi$ cm³. New base: $\\pi\\cdot6^2=36\\pi$ cm².',
          'Height: $72\\pi\\div36\\pi=2$ cm. Trap: 4. The radius doubles, so the base area is 4 times larger, not 2 times.']),
        ('q-r26-t35-08', 'A cone-shaped cup with base radius 6 cm and height 10 cm is full of water. All the water is poured into an empty cylinder with base radius 6 cm. How high is the water in the cylinder (in cm)?',
         ['$10$', '$30$', '$\\frac{10}{3}$', '$5$'], 3,
         ['Water: $\\frac{\\pi\\cdot6^2\\cdot10}{3}=120\\pi$ cm³. The cylinder base: $36\\pi$ cm².',
          'Height: $120\\pi\\div36\\pi=\\frac{10}{3}$ cm. Faster: the same base, and a cone is $\\frac13$ of the cylinder, so the water is $\\frac13$ of 10. Trap: 10.']),
        ('q-r26-t35-09', 'A cone has a base radius of 5 cm and a slant height of 13 cm. What is its volume (in cm³)?',
         ['$\\frac{325\\pi}{3}$', '$300\\pi$', '$100\\pi$', '$65\\pi$'], 3,
         ['Radius, height and slant height form a right triangle: $h^2+5^2=13^2$, $h=12$ (5-12-13).',
          'Volume: $\\frac{\\pi\\cdot5^2\\cdot12}{3}=100\\pi$ cm³. Trap: $\\frac{325\\pi}{3}$ uses 13 as the height.']),
        ('q-r26-t35-10', 'Identical bricks measure 2 cm × 3 cm × 5 cm. They are packed into a box with internal dimensions 7 cm × 10 cm × 9 cm. All the bricks are placed in the same position, with their edges parallel to the box edges. What is the greatest number of bricks that fit?',
         ['$21$', '$16$', '$9$', '$18$'], 4,
         ['Bricks are solids: count each direction, and try each way of turning the brick.',
          'Best: 2 cm along the 7 (3 bricks), 5 cm along the 10 (2 bricks), 3 cm along the 9 (3 bricks): $3\\times2\\times3=18$.',
          'Another position, e.g. 2 along 7, 3 along 10, 5 along 9, gives only $3\\times3\\times1=9$. Trap: $630\\div30=21$ divides the volumes, as if the bricks were water.']),
        ('q-r26-t35-12', 'Solid I is a cube with edge 3 cm. Solid II is a cylinder with radius 2 cm and height 2 cm. Solid III is a cone with radius 3 cm and height 3 cm. Which list orders the solids from the smallest volume to the largest?',
         ['I, II, III', 'II, I, III', 'III, II, I', 'II, III, I'], 2,
         ['I: $3^3=27$. II: $\\pi\\cdot2^2\\cdot2=8\\pi\\approx25.1$. III: $\\frac{\\pi\\cdot3^2\\cdot3}{3}=9\\pi\\approx28.3$.',
          'So II < I < III. Use 3.14 for π: with π = 3, III would be 27, the same as I.']),
        ('q-r26-t35-13', 'An empty box-shaped aquarium has internal length 60 cm, width 30 cm and height 40 cm. Water flows in at 2 liters per minute. After how many minutes does the water reach a height of 30 cm?',
         ['$27$', '$36$', '$270$', '$2.7$'], 1,
         ['Water needed: $60\\times30\\times30=54{,}000$ cm³ = 54 liters.',
          '$54\\div2=27$ minutes. Trap: 36 minutes fills the whole aquarium (72 liters).']),
        ('q-r26-t35-14', 'A cube is painted on all six faces and then cut into 216 identical small cubes, 6 along each edge. How many small cubes have no paint at all?',
         ['$64$', '$96$', '$48$', '$125$'], 1,
         ['The unpainted cubes form the inside cube: $6-2=4$ along each edge.',
          '$4^3=64$. Traps: 96 have one painted face ($6\\times4^2$), 48 have two ($12\\times4$).']),
        ('q-r26-t35-15', 'A prism has 18 edges. How many faces does it have?',
         ['$12$', '$20$', '$8$', '$6$'], 3,
         ['A prism whose base has n sides has 3n edges: $3n=18$, $n=6$.',
          'Faces: $n+2=8$ (6 side walls and 2 bases). Trap: 12 is the number of vertices.']),
        ('q-r26-t35-16', 'A right triangle has legs of 2 cm and 5 cm. Solid A is formed by turning the triangle one full turn about its 2 cm leg. Solid B is formed by turning it about its 5 cm leg. What is the ratio of the volume of A to the volume of B?',
         ['$5:2$', '$2:5$', '$1:1$', '$25:4$'], 1,
         ['A: the axis leg, 2, is the height and 5 is the radius: $\\frac{\\pi\\cdot5^2\\cdot2}{3}=\\frac{50\\pi}{3}$.',
          'B: height 5, radius 2: $\\frac{\\pi\\cdot2^2\\cdot5}{3}=\\frac{20\\pi}{3}$. The ratio is $50:20=5:2$.']),
    ]
    for qid, stem, ch, cor, ex in new:
        M.new_q(qid, TOPIC, stem, ch, cor, ex)
        M.place_q(qid, PRACT)

    M.practice_order(PRACT, [
        # easy
        'geo35-core-p02', 'geo35-core-p03', 'geo35-core-p22', 'geo35-core-p21', 'q-r26-t35-04', 'geo35-core-p01',
        'geo35-core-p04', 'q-r26-t35-15', 'geo35-core-p26', 'geo35-core-p18', 'geo35-core-p14', 'geo35-core-p19', 'geo35-core-p09',
        # medium
        'geo35-core-p06', 'geo35-core-p05', 'q-r26-t35-05', 'geo35-core-p16', 'q-r26-t35-09',
        'geo35-core-p13', 'q-r26-t35-12', 'geo35-core-p20', 'q-r26-t35-16', 'geo35-core-p24', 'geo35-core-p07', 'geo35-core-p25',
        'q-r26-t35-14', 'geo35-core-p10',
        # exam-hard
        'geo35-core-p11', 'geo35-core-p15', 'geo35-core-p12', 'geo35-core-p23', 'geo35-core-p08', 'geo35-core-p17',
        'q-r26-t35-13', 'q-r26-t35-08', 'q-r26-t35-10',
    ])

    # =====================================================================================
    # 8. Cleanup: American spelling, "so" mid-sentence, titles and on-screen notes in sync
    # =====================================================================================
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            b['title'] = _american(b['title'])
            for l in b['lines']:
                for key in ('say', 'draw', 'label'):
                    if key in l:
                        t = _american(l[key])
                        if key == 'say': t = re.sub(r', so (?=[a-z])', '. So ', t)
                        if t != l[key]: l[key] = t; M.touched_videos.add(v['id'])
            for it in b['items']:
                if it.get('t'): it['t'] = _american(it['t'])
    for f in list(M.D['flow']):
        if f['topic'] == TOPIC and f['type'] == 'question':
            q = M.q(f['ref'])
            if q['stemRich'] != q['stemRich'].strip(): S(f['ref'], stem=q['stemRich'].strip())
    for v in M.D['videos'].values():
        if v['topic'] == TOPIC and v.get('kind') == 'solution' and v.get('questionId') in M.D['questions']:
            v['title'] = v['navLabel'] = M.q(v['questionId'])['stem']
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            pre = b['items'][:b['pre']]
            if len(pre) == 1 and pre[0].get('k') == 'q' and b.get('canvas', '').startswith('Pre-loaded — question'):
                qid = pre[0]['qid']
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, M.q(qid)['stem'])
    summary(M)


# =========================================================================================
# 9. Pass 2: summary lesson right before the practice
# =========================================================================================
def summary(M):
    sb = ['Straight or pointed', 'Surface area', 'Water and units', 'Right triangles inside', 'Cube and box facts',
          'Turning a shape', 'Cubes in a box', 'Counting and face areas', 'Before you practice']
    S = lambda k, script: dict(title=sb[k], mode='concept', active=k, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of solid geometry.",
            "Everything important, one idea at a time."]),
        S(0, [
            A("'Straight: V = base area × height' appears", T('Straight (prism, box, cylinder): $V=$ base area $\\times$ height', size=40, gap=30)),
            "First question: is the solid straight or pointed? A straight solid: base area times height.",
            A("'Pointed: ÷ 3' appears", T('Pointed (cone, pyramid): $V=\\frac{\\text{base area}\\times\\text{height}}{3}$', size=40, gap=30)),
            "A pointed solid: the same, divided by 3. One third of the straight solid with the same base and height.",
            A("'pyramid : left : cube = 1 : 2 : 3' appears", T('Pyramid in a cube: pyramid : left : cube $=1:2:3$', size=38)),
            "Box, cylinder, cone and pyramid are on the formula page. The general rules — know them by heart."]),
        S(1, [
            A("'Lateral = perimeter of the base × height' appears", T('Lateral $=$ perimeter of the base $\\times$ height', size=42, gap=30)),
            "Lateral area is what wraps around: the perimeter of the base times the height.",
            A("'Total = lateral + 2 bases' appears", T('Total $=$ lateral $+$ the two bases', size=42, gap=30)),
            "Total surface area: add the two bases.",
            A("'Bases = the two identical faces' appears", T('Bases $=$ the two identical faces — even lying down', size=40)),
            "A prism lying on its side? Find the two identical faces first. The height joins them."]),
        S(2, [
            A("'Water height = volume ÷ base area' appears", T('Water height $=$ volume $\\div$ base area', size=42, gap=30)),
            "Water takes the shape of the container. Its height is the volume over the base area.",
            A("'Pouring: the volume stays' appears", T('Pouring: the VOLUME stays — not the height', size=42, gap=30)),
            "Pouring into another container? The volume stays, and the height changes. A wider base — lower water.",
            A("'1 ml = 1 cm³ · 1 liter = 1000 cm³' appears", T('$1$ ml $=1\\text{ cm}^3$ · $1$ liter $=1000\\text{ cm}^3$', size=42)),
            "And the same units first: a liter is a thousand cubic centimeters."]),
        S(3, [
            A("'Cone: r² + h² = ℓ²' appears", T('Cone: $r^2+h^2=\\ell^2$ — the slant height is not the height', size=40, gap=30)),
            "Many questions hide a right triangle inside the solid. Find it.",
            "A cone: radius, height and slant height. Radius 9, slant height 15 — the height is 12.",
            A("'Pyramid: height, half the diagonal, the edge' appears", T('Pyramid: height $\\cdot$ half the base diagonal $\\cdot$ the slanted edge', size=38, gap=30)),
            "A pyramid with equal edges: the apex is above the center. The height, half the diagonal and the edge.",
            A("'Height < slanted edge' appears", T('The height is shorter than any slanted edge', size=40)),
            "The height goes straight down. It's always shorter than a slanted edge."]),
        S(4, [
            A("'Cube: a√2 and a√3' appears", T('Cube: face diagonal $a\\sqrt2$ · body diagonal $a\\sqrt3$', size=42, gap=30)),
            "In a cube: the face diagonal is a root 2, the body diagonal a root 3.",
            A("'Box: √(a² + b² + c²)' appears", T('Box: body diagonal $=\\sqrt{a^2+b^2+c^2}$', size=42, gap=30)),
            "In a box: two right triangles, or the root of the three squares. 2, 3, 6 — 7.",
            A("'90°' appears", T('Edge $+$ diagonal of the face it stands on (same corner): $90°$', size=36, gap=20)),
            A("'45° · 60°' appears", T('Edge $+$ diagonal of the same face: $45°$ · two face diagonals, same corner: $60°$', size=36)),
            "And the angles in a cube — only when the lines meet at the same corner."]),
        S(5, [
            A("'Rectangle about a side → cylinder' appears", T('Rectangle about a side $\\rightarrow$ cylinder', size=42, gap=30)),
            A("'Right triangle about a leg → cone' appears", T('Right triangle about a leg $\\rightarrow$ cone', size=42, gap=30)),
            "Turn a flat shape one full turn: a rectangle makes a cylinder, a right triangle makes a cone.",
            A("'The side on the axis = the height' appears", T('The side on the axis $=$ the height · the other side $=$ the radius', size=38)),
            "The side on the axis is the height. The other side is the radius — and the radius is squared, so it counts more."]),
        S(6, [
            A("'Count each direction, drop the remainder' appears", T('Solids in a box: divide each direction, drop the remainder, multiply', size=36, gap=30)),
            "Solids in a box aren't water. Divide each direction, drop the remainder, then multiply. Never divide the volumes.",
            "Bricks that aren't cubes? Try each position — the count can change.",
            A("'Remove a corner cube: lose 3, gain 3' appears", T('Remove a corner cube: lose $3$ faces, gain $3$ — no change', size=38, gap=30)),
            "Remove a corner cube: the volume goes down, the surface area stays the same.",
            A("'Painted cube' appears", T('Painted $n\\times n\\times n$: $8$ · $12(n-2)$ · $6(n-2)^2$ · $(n-2)^3$', size=38)),
            "A painted cube: 3 faces — the 8 corners. 2 faces — the edges. 1 face — the middle of each face. None — the inside."]),
        S(7, [
            A("'Prism: n + 2 faces · 3n edges · 2n vertices' appears", T('Prism, base with $n$ sides: $n+2$ faces · $3n$ edges · $2n$ vertices', size=36, gap=30)),
            A("'Pyramid: n + 1 · 2n · n + 1' appears", T('Pyramid: $n+1$ faces · $2n$ edges · $n+1$ vertices', size=36, gap=30)),
            "Counting: check the rule on a cube — n is 4: 6 faces, 12 edges, 8 vertices.",
            A("'V = √(ab · bc · ca)' appears", T('Three face areas $\\rightarrow V=\\sqrt{ab\\cdot bc\\cdot ca}$', size=40)),
            "Three face areas at one corner? Multiply them and take the root. 12, 15, 20 — the volume is 60."]),
        S(8, [
            "Before you start, always ask yourself:",
            A('Check 1 appears', T('Straight or pointed? (pointed: $\\div3$)', size=38, gap=24)),
            A('Check 2 appears', T('Where are the bases — and the height?', size=38, gap=24)),
            A('Check 3 appears', T('What stays the same? (pouring: the volume)', size=38, gap=24)),
            A('Check 4 appears', T('Is there a right triangle inside?', size=38, gap=24)),
            A('Check 5 appears', T('Same units?', size=38)),
            "And the traps: the slant height is not the height, a pointed solid needs the divide by 3, and solids in a box are not water.",
            "Now it's your turn. Good luck!"]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == LEARN][-1]
    M.new_video('r26-t35-summary', TOPIC, 'Summary: Solid Geometry', sb, slides, LEARN, after=last)


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
    # --- "Water Level": slides 2 (height = volume / base) and 3 (pouring) are taught again in Q (solve-q-r26-t35-01);
    #     the recap goes with them. Kept: the units slide (no question teaches liters / cm³).
    W = 'r26-t35-water'
    _cr_cut(M, W, [2, 3, 5])
    _cr_say(M, W, 2, 'First the same units. Then compare or divide.',
            'First the same units. Then compare or divide. Now try a question.')
    # the rule moves into the question video as one line + board item
    _cr_add(M, 'solve-q-r26-t35-01', 2, 'Water in a box, 10 by 8, 9 high.',
            "The rule: the water's height is the volume divided by the base area.",
            T(r'Height $=$ volume $\div$ base', size=34, x=1060, y=200, w=470),
            "'Height = volume ÷ base' appears", at=1)

    # --- "Cones": slide 2 (slant height) is taught again in solve-q-r26-t35-02. Kept: turning a shape (no question).
    C = 'r26-t35-cones'
    _cr_cut(M, C, [2])
    _cr_say(M, C, 1, 'The slant height — and solids you make by turning a flat shape.',
            'Solids you make by turning a flat shape. And then a question on the slant height.')
    _cr_drop_item(M, C, 4, 0)
    _cr_say(M, C, 4, 'Slant height: the hypotenuse of the inner triangle. Turning: the side on the axis is the height.',
            'Turning: the side on the axis is the height.')
    _cr_say(M, C, 4, 'Now a question.', 'Now a question on the slant height.')

    # --- "Cube and Box Facts": slide 5 (painted cube) is taught again in solve-q-r26-t35-03.
    _cr_cut(M, 'r26-t35-cubefacts', [5])


_apply_before_cut = apply


def apply(M):
    _apply_before_cut(M)
    cut_repeats(M)


# ================================================================================================
# 2026-10-06 renumber pass (runs LAST, after cut_repeats). The English course must not look like the Hebrew one:
# every Hebrew-derived question (guided geo35-g121 ... g132, practice geo35-core-p01 ... p20) gets new numbers
# (letter-only questions: new letters and choice order), its solution video is rewritten to match, and every changed
# figure is redrawn. Hebrew-derived lesson examples get new numbers too. Practice clean-up 36 -> 26.
# Nothing in topic 35 is recorded (checked ~/Documents/Course.recordings 2026-10-06: only Algebra topics 1-8).
# Topic 35 has no practice_methods / add_methods / pen_or_click.
# ================================================================================================
import math
RN_RECORDED = set()


# --- figures ----------------------------------------------------------------------------------
def _rn_cone(title, r_px, h_px, h_lab, r_lab, cy=299.455):
    f = Fig(title)
    cx, ry = 320.0, r_px * 0.28
    top = cy - h_px
    f.poly([(cx - r_px, cy), (cx + r_px, cy), (cx, top)], fill=FILL, stroke='none', sw=2.5)
    f.half_ellipse(cx, cy, r_px, ry, front=False); f.half_ellipse(cx, cy, r_px, ry, front=True)
    f.line((cx - r_px, cy), (cx, top)); f.line((cx, top), (cx + r_px, cy))
    f.line((cx, cy), (cx, top), TEAL, 2.5, dash=True)
    f.line((cx, cy), (cx + r_px, cy), TEAL, 2.5)
    f.text(cx - min(20, r_px / 2) - (14 if r_px < 60 else 0) - (r_px / 2 if r_px < 60 else 0), cy - h_px / 2, h_lab)
    f.text(cx + r_px / 2, cy + ry + 6 if ry > 14 else cy + 20, r_lab)
    return f


def rn_fig_g121():   # radius sqrt6, height 12 (to scale: 12 / 2.449)
    return _rn_cone('Right circular cone', 239.0 * math.sqrt(6) / 12, 239.0, '12', '√6')


def rn_fig_p02():    # radius 3a, height 4a
    return _rn_cone('Right circular cone', 150.0, 200.0, '4a', '3a', cy=280.0)


def rn_fig_g123(svg):
    """AM : MB = 1 : 3 (was 1 : 2): M and N move to a quarter of AB."""
    xa, xb = 135.388, 424.975
    xm = xa + (xb - xa) / 4
    svg = svg.replace('231.917', '%.3f' % xm)
    svg = _move_text(svg, 'x', (xa + xm) / 2, 314.736)
    svg = re.sub(r'(<text x=")[\d.]+(" y="[\d.]+"[^>]*>)2x</text>', lambda m: '%s%.3f%s3x</text>' % (m.group(1), (xm + xb) / 2, m.group(2)), svg)
    return svg


def rn_fig_g124():
    """Right prism lying on its side: right-triangle bases (legs 9 and 12, hypotenuse 15), height 5."""
    f = Fig('A right triangular prism with congruent triangular bases')
    k = 19.0
    A_ = (240.0, 307.0); B_ = (A_[0] + 9 * k, A_[1]); C_ = (A_[0], A_[1] - 12 * k)
    dv = (5 * 10.4, -5 * 6.6)
    D_, E_, F_ = [(p[0] + dv[0], p[1] + dv[1]) for p in (A_, B_, C_)]
    f.poly([B_, E_, F_, C_], fill=FILL)
    f.poly([A_, B_, C_], fill=FRONT)
    f.line(A_, D_, DASH, dash=True); f.line(D_, E_, DASH, dash=True); f.line(D_, F_, DASH, dash=True)
    f.line(C_, F_); f.line(E_, F_)
    m = 10
    f.line((A_[0] + m, A_[1]), (A_[0] + m, A_[1] - m), TEAL, 1.7); f.line((A_[0] + m, A_[1] - m), (A_[0], A_[1] - m), TEAL, 1.7)
    for (x, y), s in [((A_[0] - 15, A_[1] + 12), 'A'), ((B_[0] + 4, B_[1] + 18), 'B'), ((C_[0] - 15, C_[1] - 15), 'C'),
                      ((D_[0] - 13, D_[1] - 7), 'D'), ((E_[0] + 18, E_[1] + 8), 'E'), ((F_[0] + 8, F_[1] - 19), 'F')]:
        f.text(x, y, s)
    f.text((A_[0] + B_[0]) / 2, A_[1] + 21, '9')
    f.text(B_[0] + 0.3 * (C_[0] - B_[0]) - 16, B_[1] + 0.3 * (C_[1] - B_[1]) + 2, '15')
    f.text((B_[0] + E_[0]) / 2 + 12, (B_[1] + E_[1]) / 2 + 14, '5')
    return f


def _rn_block(f, w, d, h, x0, y0, s):
    """A w (across) x d (deep) x h (up) block of unit cubes; front face bottom-left at (x0, y0), small edge s."""
    ddx, ddy = s * 0.55, -s * 0.35
    for k in range(d - 1, -1, -1):          # top face, back rows first
        for c in range(w):
            bx, by = x0 + c * s + k * ddx, y0 - h * s + k * ddy
            f.poly([(bx, by), (bx + s, by), (bx + s + ddx, by + ddy), (bx + ddx, by + ddy)], fill=TOP, sw=1.2)
    for k in range(d - 1, -1, -1):          # right face
        for r in range(h):
            bx, by = x0 + w * s + k * ddx, y0 - r * s + k * ddy
            f.poly([(bx, by), (bx + ddx, by + ddy), (bx + ddx, by + ddy - s), (bx, by - s)], fill=FILL, sw=1.2)
    for r in range(h):                      # front face
        for c in range(w):
            bx, by = x0 + c * s, y0 - r * s
            f.poly([(bx, by), (bx + s, by), (bx + s, by - s), (bx, by - s)], fill=FRONT, sw=1.2)


def rn_fig_g125():
    f = Fig('Four rectangular blocks, each made from eighteen unit cubes')
    s = 11.0
    for cx, (w, d, h), lab in [(170, (1, 1, 18), '1 × 1 × 18'), (270, (2, 1, 9), '1 × 2 × 9'),
                               (370, (3, 1, 6), '1 × 3 × 6'), (470, (3, 2, 3), '2 × 3 × 3')]:
        x0 = cx - (w * s + d * s * 0.55) / 2
        _rn_block(f, w, d, h, x0, 300, s)
        f.text(cx, 328, lab, size=16)
    return f


def rn_fig_g128():
    """Square pyramid: base side 4*sqrt2, lateral edge 7, height sqrt33 (to scale)."""
    f = Fig('Square pyramid and its perpendicular height')
    k = 33.0
    sd = 4 * math.sqrt(2) * k; h = math.sqrt(33) * k
    dx, dy = sd * 0.55, -sd * 0.35
    O = (320.0, 268.0)
    A_ = (O[0] - sd / 2 - dx / 2, O[1] - dy / 2); B_ = (A_[0] + sd, A_[1])
    C_ = (B_[0] + dx, B_[1] + dy); D_ = (A_[0] + dx, A_[1] + dy); P = (O[0], O[1] - h)
    f.poly([A_, B_, P], fill=FRONT)
    f.poly([B_, C_, P], fill=FILL)
    f.line(A_, D_, DASH, dash=True); f.line(D_, C_, DASH, dash=True); f.line(D_, P, DASH, dash=True)
    f.line(P, O, ORANGE, 2.5, dash=True)
    f.raw('<circle cx="%.3f" cy="%.3f" r="3.2" fill="#203344"/>' % O, [O])
    for (x, y), t in [((A_[0] - 14, A_[1] + 16), 'A'), ((B_[0] + 6, B_[1] + 20), 'B'), ((C_[0] + 18, C_[1] + 6), 'C'),
                      ((D_[0] - 12, D_[1] - 10), 'D'), ((P[0], P[1] - 20), 'P'), ((O[0] - 20, O[1]), 'O')]:
        f.text(x, y, t)
    f.text((A_[0] + B_[0]) / 2, A_[1] + 24, '4√2')
    f.text((B_[0] + P[0]) / 2 + 16, (B_[1] + P[1]) / 2, '7')
    return f


def rn_fig_g131():
    """Box 18 x 9 x 11 (length x width x height)."""
    k = 16.5
    w, h, d = 18 * k, 11 * k, 9 * k * 0.65 / 0.943
    x0, y0 = 320 - (w + d * 0.8) / 2, 312
    return box_fig('Rectangular box with hidden edges shown dashed', x0, y0, w, h, d,
                   labels=[(x0 + w / 2, y0 + 22, '18'), (x0 + w + d * 0.4 + 14, y0 - d * 0.25 + 14, '9'),
                           (x0 + w + d * 0.4 + 2, y0 - h / 2 - d * 0.25, '11')])


def rn_fig_p01():
    """Rectangle 7 x 4 turned about one of its 7 cm sides (25 px per cm, as before)."""
    f = Fig('A rectangle rotated about one of its seven-centimeter sides')
    x0, y0, w, h = 270.0, 267.5, 100.0, 175.0
    f.poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 - h), (x0, y0 - h)], fill=FILL)
    f.line((x0, y0 + 21), (x0, y0 - h - 21), TEAL, 2.5, dash=True)
    f.text(x0 - 22, y0 - h / 2, '7'); f.text(x0 + w / 2, y0 + 22, '4')
    f.text(x0 - 42, y0 - h / 2 - 21, '↻', size=35)
    return f


def rn_fig_p03():
    """Box with two opposite square faces 5 x 5 (front and back) and length 6."""
    s = 130.0
    d = s * 1.1
    return box_fig('Rectangular box with hidden edges shown dashed', 320 - (s + d * 0.8) / 2, 292, s, s, d)


def rn_fig_p06():
    """Box AB = 10, AD = 3, height 8; AM = NC = 4; prism with trapezoid base AMND."""
    k = 26.0
    w, h, d = 10 * k, 8 * k, 3 * k * 0.9
    x0, y0 = 320 - (w + d * 0.8) / 2, 312
    def ex(f, P):
        M_ = (P['A'][0] + 0.4 * w, P['A'][1]); N_ = (P['D'][0] + 0.6 * w, P['D'][1])
        Mt, Nt = (M_[0], M_[1] - h), (N_[0], N_[1] - h)
        f.poly([P['A'], M_, N_, P['D']], fill=FILL, stroke=TEAL)
        f.poly([P['E'], Mt, Nt, P['H']], fill=FILL, stroke=TEAL)
        f.line(M_, Mt, TEAL, 2.5); f.line(N_, Nt, TEAL, 2.5, dash=True)
        f.text(M_[0], M_[1] + 20, 'M'); f.text(N_[0] + 13, N_[1] - 14, 'N')
        for key, (ox, oy) in dict(A=(-15, 13), B=(10, 18), C=(18, 7), D=(-16, -3), E=(-15, -15), F=(10, -15), G=(16, -13), H=(-12, -18)).items():
            f.text(P[key][0] + ox, P[key][1] + oy, key)
    return box_fig('Rectangular box with hidden edges shown dashed', x0, y0, w, h, d, extra=ex)


def rn_fig_p07():
    """Two hexagonal pyramids joined along their common base."""
    f = Fig('Two hexagonal pyramids joined along their common base')
    cx, cy, rx, ry = 320.0, 180.0, 82.0, 26.0
    top, bot = (cx, 70.5), (cx, 289.5)
    V = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in (10, 70, 130, 190, 250, 310)]
    back = lambda p: p[1] < cy - 1
    for i, p in enumerate(V):
        q = V[(i + 1) % 6]
        b = back(p) or back(q)
        f.line(p, q, DASH if b else INK, 2.5, dash=b)
    for p in V:
        for apex in (top, bot):
            f.line(p, apex, TEAL, 2.5, dash=back(p))
    return f


def rn_fig_p08(svg):
    """AM = AB/4 and DN = 3DC/4 (was 1/3 and 2/3)."""
    xa, xb, xd, xc = 152.370, 368.667, 271.333, 487.630
    xm, xn = xa + (xb - xa) / 4, xd + 3 * (xc - xd) / 4
    return svg.replace('224.469', '%.3f' % xm).replace('415.531', '%.3f' % xn)


def rn_fig_p09(svg):
    """Highlight edge BF (orange) and the top-face diagonal FH (teal), instead of AE and EG."""
    old_t = '<line x1="197.676" y1="128.703" x2="442.324" y2="73.459" stroke="#087f83" stroke-width="4"/>'
    old_o = '<line x1="197.676" y1="128.703" x2="197.676" y2="286.541" stroke="#bb6821" stroke-width="4"/>'
    assert old_t in svg and old_o in svg
    svg = svg.replace(old_t, '<line x1="355.514" y1="128.703" x2="284.486" y2="73.459" stroke="#087f83" stroke-width="4"/>')
    return svg.replace(old_o, '<line x1="355.514" y1="128.703" x2="355.514" y2="286.541" stroke="#bb6821" stroke-width="4"/>')


def rn_fig_p13():
    """Cube edge 10 seen from above, a few circular bases of radius 1 in one corner."""
    f = Fig('The square base of the cube with a few circular bases in one corner')
    x0, y0, side = 194.857, 305.143, 250.286
    f.poly([(x0, y0), (x0 + side, y0), (x0 + side, y0 - side), (x0, y0 - side)], fill='none')
    r = side / 10
    for i, j in [(0, 0), (1, 0), (0, 1)]:
        f.raw('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="#d5f1ed" stroke="#203344" stroke-width="1.3"/>' % (x0 + r + 2 * r * i, y0 - r - 2 * r * j, r))
    f.text(x0 + 4 * r + 30, y0 - r, '…', size=26); f.text(x0 + r, y0 - 4 * r - 22, '⋮', size=26)
    f.text(x0 + side / 2, y0 + 23, '10'); f.text(x0 + side + 25, y0 - side / 2, '10')
    return f


def rn_fig_p16(svg):
    """Sector 135 degrees (was 150), radius label 4 (was 3)."""
    R, c, r = 109.5, (320.0, 180.0), 29.2
    e = (c[0] + R * math.cos(math.radians(135)), c[1] - R * math.sin(math.radians(135)))
    ei = (c[0] + r * math.cos(math.radians(135)), c[1] - r * math.sin(math.radians(135)))
    svg, n1 = re.subn(r'A 109\.500 109\.500 0 0 0 225\.170 125\.250 Z', 'A 109.500 109.500 0 0 0 %.3f %.3f Z' % e, svg)
    svg, n2 = re.subn(r'A 29\.200 29\.200 0 0 0 294\.712 165\.400', 'A 29.200 29.200 0 0 0 %.3f %.3f' % ei, svg)
    assert n1 == n2 == 1
    lx, ly = c[0] + 44.5 * math.cos(math.radians(67.5)), c[1] - 44.5 * math.sin(math.radians(67.5))
    svg = re.sub(r'<text x="[\d.]+" y="[\d.]+"([^>]*)>150°</text>', lambda m: '<text x="%.3f" y="%.3f"%s>135°</text>' % (lx, ly, m.group(1)), svg)
    return _relabel_t(svg, {'3': '4'})


def _relabel_t(svg, mp):
    """Change the text of figure labels (exact <text> contents, each must occur once)."""
    for old in mp:
        n = len(re.findall('>%s</text>' % re.escape(old), svg))
        assert n == 1, (old, n)
    return re.sub(r'>([^<]+)</text>', lambda mo: '>%s</text>' % mp.get(mo.group(1), mo.group(1)), svg)


# --- editing helpers --------------------------------------------------------------------------
def _rn_q(M, qid, stem=None, choices=None, correct=None, expl=None):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


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


def _rn_items(M, vid, n, texts):
    """Board items by index -> new text (the item must be a text item)."""
    if vid in RN_RECORDED: return
    b = M.slide(vid, n)
    for k, t in texts.items():
        assert b['items'][k].get('k') == 't', (vid, n, k)
        b['items'][k]['t'] = t
    M.touched_videos.add(vid)


def _rn_lines(M, vid, n, lines):
    """Replace all lines of a slide. lines: str = spoken · ('d', text) = draw · (k, label) = item k appears."""
    if vid in RN_RECORDED: return
    out = []
    for l in lines:
        if isinstance(l, str): out.append({'say': l})
        elif l[0] == 'd': out.append({'draw': l[1]})
        else: out.append({'appear': l[0], 'label': l[1]})
    old = [l['appear'] for l in M.slide(vid, n)['lines'] if 'appear' in l]
    assert old == [l['appear'] for l in out if 'appear' in l], (vid, n)
    M.edit_lines(vid, n, lambda ls: out)


def _rn_fig(M, qid, fig):
    """New figure: a Fig (full view for the question, tight crop on slides) or a function svg -> svg."""
    if qid in RN_RECORDED: return
    if isinstance(fig, Fig): _set_q_fig_new(M, qid, fig)
    else: _set_q_figs(M, qid, fig)


# --- guided questions + their solution videos ---------------------------------------------------
def rn_guided(M):
    # ---------- g121: cone r = sqrt7, h = 9 -> 21pi (Hebrew sqrt5, 6 -> 10pi)  ==>  r = sqrt6, h = 12 -> 24pi ~ 75.4
    g = 'geo35-g121'; V = 'solve-' + g
    _rn_q(M, g, stem='A cone-shaped container with base radius $\\sqrt6$ cm and height 12 cm is full of water. Which of the following empty containers can hold all the water? The dimensions given are internal dimensions.',
          choices=['A cube with edge 4 cm', 'A square pyramid with base edge 6 cm and height 7 cm',
                   'A box measuring 6 cm × 4 cm × 3 cm', 'A cylinder with base radius $\\sqrt2$ cm and height 10 cm'], correct=2, expl=[
        'The cone holds $\\frac{\\pi(\\sqrt6)^2\\cdot12}{3}=24\\pi$ cm³ of water, about $24\\times3.14\\approx75.4$.',
        'Check each container. The cube (choice 1): $4^3=64$, too small. The pyramid (choice 2): $\\frac{6^2\\times7}{3}=84$, big enough. '
        'The box (choice 3): $6\\times4\\times3=72$, too small. The cylinder (choice 4): $\\pi(\\sqrt2)^2\\times10=20\\pi$, less than $24\\pi$.',
        'Only the pyramid (84 cm³) can hold all the water. Careful with π: with π = 3 the water would be 72, and the box would look big enough.'])
    _rn_fig(M, g, rn_fig_g121())
    _rn_items(M, V, 2, {2: '$\\frac{\\pi\\cdot(\\sqrt6)^2\\cdot12}{3}=24\\pi$', 3: '$24\\pi\\approx24\\times3.14\\approx75.4$'})
    _rn_sub(M, V, 2, [
        ('radius root 7, height 9', 'radius root 6, height 12'),
        ('π · 7 · 9 / 3 = 21π appears', 'π · 6 · 12 / 3 = 24π appears'),
        ('Root 7 squared is 7. 9 and 3 cancel to 3. 7 times 3 — 21π.', 'Root 6 squared is 6. 12 and 3 cancel to 4. 6 times 4 — 24π.'),
        ('21π ≈ 21 × 3.14 ≈ 65.9 appears', '24π ≈ 24 × 3.14 ≈ 75.4 appears'),
        ('21 times 3.14 — 63 plus 2.94. About 65.9.', '24 times 3.14 — 72 plus 3.36. About 75.4.')])
    _rn_items(M, V, 3, {1: 'Cube: $4^3=64<75.4$', 2: 'Pyramid: $\\frac{6^2\\cdot7}{3}=84$'})
    _rn_lines(M, V, 3, [
        'Now the choices. Bigger or equal — we mark it. Smaller — we eliminate and move on.',
        'The most important thing: straight solid or pointed? Straight — base area times height. Pointed — the same, over 3.',
        'Choice one: a cube with edge 4. A straight solid. For a cube — just the edge cubed.',
        (1, 'Cube: 4³ = 64 appears'),
        '4 cubed — 64. Less than the water.',
        ('d', 'Cross out choice 1'),
        'Choice two: a square pyramid — a pyramid whose base is a square. Base edge 6, height 7. Pointed.',
        (2, 'Pyramid: 6² · 7 / 3 = 84 appears'),
        'Base area 6 squared, 36. Over 3 — 12. Times the height 7 — 84.',
        '84 is more than 75.4. This pyramid can hold all the water.',
        ('d', 'Circle choice 2'),
        'Choice two. On the exam — we mark and move on.'])
    _rn_items(M, V, 4, {1: 'Box: $6\\cdot4\\cdot3=72<75.4$', 2: 'Cylinder: $\\pi\\cdot(\\sqrt2)^2\\cdot10=20\\pi<24\\pi$'})
    _rn_lines(M, V, 4, [
        "In the lesson, let's check the other two as well.",
        (1, 'Box: 6 · 4 · 3 = 72 appears'),
        'The box: a straight solid — just multiply all the dimensions. 6 times 4 times 3 — 72. Just below the water. Eliminated.',
        "Careful — that one's close. If you round π to 3, the water is 72 and the box suddenly looks big enough. Use 3.14.",
        (2, 'Cylinder: π · 2 · 10 = 20π appears'),
        'The cylinder: a straight solid. Root 2 squared is 2, times the height 10 — 20π. Less than 24π. Eliminated.',
        'So: straight or pointed — those are the two most important principles of volume on the exam.',
        'Only the pyramid holds all the water. Choice two.'])

    # ---------- g122: cone = 2 x cylinder -> H = 6h (Hebrew: equal volumes -> 3h)  ==>  4 x cylinder -> H = 12h
    g = 'geo35-g122'; V = 'solve-' + g
    _rn_q(M, g, stem='A cone and a cylinder have equal base areas. The volume of the cone is four times the volume of the cylinder. If the cylinder’s height is h, what is the cone’s height?',
          choices=['$4h$', '$3h$', '$\\frac{4h}{3}$', '$12h$'], correct=4, expl=[
        'Let the common base area be B and the cone height be H. The cone volume is $\\frac{BH}{3}$ and the cylinder volume is $Bh$.',
        '$\\frac{BH}{3}=4Bh$. Divide by B and multiply by 3: $H=12h$.',
        'Traps: $3h$ gives equal volumes, not four times the volume; $4h$ forgets that a cone is a third.'])
    _rn_items(M, V, 2, {1: '$\\frac{\\pi r^2H}{3}=4\\cdot\\pi r^2h$', 2: '$\\frac{H}{3}=4h\\ \\Rightarrow\\ H=12h$'})
    _rn_sub(M, V, 2, [
        ("The cone's volume is twice the cylinder's.", "The cone's volume is four times the cylinder's."),
        ('πr²H / 3 = 2 · πr²h appears', 'πr²H / 3 = 4 · πr²h appears'),
        ("The cone's volume equals twice the cylinder's volume.", "The cone's volume equals four times the cylinder's volume."),
        ('H / 3 = 2h → H = 6h appears', 'H / 3 = 4h → H = 12h appears'),
        ('Multiply by 3: H is 6h.', 'Multiply by 3: H is 12h.'),
        ('Circle choice 2', 'Circle choice 4'), ('Choice two. Not complicated at all.', 'Choice four. Not complicated at all.')])
    _rn_sub(M, V, 3, [
        ('But we want TWICE the cylinder — so double that again: 6h.', 'But we want FOUR TIMES the cylinder — so multiply that by 4: 12h.'),
        ('Choice two. This principle', 'Choice four. This principle')])

    # ---------- g123: V = 216, AM : MB = 1 : 2 -> 1/6 -> 36 (Hebrew 120, x and x -> 1/4 -> 30)  ==>  320, 1 : 3 -> 1/8 -> 40
    g = 'geo35-g123'; V = 'solve-' + g
    _rn_q(M, g, stem='The volume of rectangular box ABCDEFGH is 320 cm³. M lies on AB so that the ratio AM : MB is 1 : 3, and N lies directly above M on EF. What is the volume of triangular prism AMD–ENH (in cm³)?',
          choices=['$80$', '$160$', '$40$', '$120$'], correct=3, expl=[
        'AM is $\\frac14$ of AB. The rectangle with sides AM and AD is $\\frac14$ of the base, and triangle AMD is half of that rectangle.',
        'So the triangle is $\\frac12\\cdot\\frac14=\\frac18$ of the base. The prism and the box have the same height. Therefore the prism is $\\frac18$ of the box: $320\\div8=40$ cm³.'])
    _rn_fig(M, g, rn_fig_g123)
    _rn_items(M, V, 2, {1: '$4x\\cdot y\\cdot z=320$', 3: '$xyz=80\\ \\Rightarrow\\ V=40$'})
    _rn_sub(M, V, 2, [
        ('A box with volume 216. AM to MB is 1 to 2.', 'A box with volume 320. AM to MB is 1 to 3.'),
        ("The box's volume is 216", "The box's volume is 320"),
        ('Write x on AM and 2x on MB', 'Write x on AM and 3x on MB'),
        ("So AM is x and MB is 2x — the box's length is 3x.", "So AM is x and MB is 3x — the box's length is 4x."),
        ('3x · y · z = 216 appears', '4x · y · z = 320 appears'),
        ('xyz = 72 → V = 36 appears', 'xyz = 80 → V = 40 appears'),
        ('3xyz is 216. So xyz is 72. Half of 72 — 36.', '4xyz is 320. So xyz is 80. Half of 80 — 40.')])
    _rn_items(M, V, 3, {1: 'Strip $AM$: $\\frac14$ of the base', 2: 'Triangle $=\\frac12\\cdot\\frac14=\\frac18$', 3: '$320\\div8=40$'})
    _rn_sub(M, V, 3, [
        ('Strip = ⅓ of the rectangle appears', 'Strip = ¼ of the rectangle appears'),
        ('cuts the rectangle into x and 2x — three equal parts. The left strip is one third.',
         'cuts the rectangle into x and 3x — four equal parts. The left strip is one quarter.'),
        ('Triangle = ½ of the strip → ⅙ appears', 'Triangle = ½ of the strip → ⅛ appears'),
        ('So the shaded part is half of a third — one sixth.', 'So the shaded part is half of a quarter — one eighth.'),
        ('216 ÷ 6 = 36 appears', '320 ÷ 8 = 40 appears'),
        ('One sixth of 216 — 36. Choice three.', 'One eighth of 320 — 40. Choice three.')])

    # ---------- g124: leg 5, hyp 13, h 4 -> 120 (Hebrew 3, 5, h 2 -> 24)  ==>  leg 9, hyp 15, h 5 -> 36 x 5 = 180
    g = 'geo35-g124'; V = 'solve-' + g
    _rn_q(M, g, stem='The bases of a right triangular prism are right triangles. Each base has a leg of 9 cm and a hypotenuse of 15 cm. The height of the prism is 5 cm. What is its lateral surface area (in cm²)?',
          choices=['$180$', '$108$', '$120$', '$288$'], correct=1, expl=[
        'The prism lies on its side. Its bases are the two right triangles, and its height is the edge between them, 5.',
        'The missing leg is 12, since $9^2+12^2=15^2$. The base perimeter is $9+12+15=36$.',
        'Lateral surface area $=36\\times5=180$ cm². (Adding the two triangles, $2\\times54=108$, gives the total surface area, 288.)'])
    _rn_fig(M, g, rn_fig_g124())
    _rn_items(M, V, 2, {1: '$9,\\ 12,\\ 15$', 2: '$P=9+12+15=36$', 3: '$S_{\\text{lateral}}=36\\times5=180$'})
    _rn_sub(M, V, 2, [
        ('a leg of 5, a hypotenuse of 13, height 4.', 'a leg of 9, a hypotenuse of 15, height 5.'),
        ('the edge BE, 4.', 'the edge BE, 5.'),
        ('one side 5, the hypotenuse 13.', 'one side 9, the hypotenuse 15.'),
        ('5, 12, 13 appears', '9, 12, 15 appears'),
        ('A right triangle, hypotenuse 13, leg 5 — the other leg is 12. The Pythagorean triple 5, 12, 13.',
         'A right triangle, hypotenuse 15, leg 9 — the other leg is 12. The Pythagorean triple 3, 4, 5 — times 3: 9, 12, 15.'),
        ('P = 5 + 12 + 13 = 30 appears', 'P = 9 + 12 + 15 = 36 appears'),
        ("5 plus 12 plus 13 — 30. Or: the average of the three sides is 10. So it's 3 times 10.",
         "9 plus 12 plus 15 — 36. Or: the average of the three sides is 12. So it's 3 times 12."),
        ('30 × 4 = 120 appears', '36 × 5 = 180 appears'),
        ('The height is given — 4. 30 times 4 — 120.', 'The height is given — 5. 36 times 5 — 180.')])
    _rn_items(M, V, 3, {1: '$9\\cdot5=45$', 2: '$12\\cdot5=60$', 3: '$15\\cdot5=75$', 4: '$45+60+75=180$'})
    _rn_sub(M, V, 3, [
        ('5 · 4 = 20 appears', '9 · 5 = 45 appears'), ('The first face — 5 times the height 4. 20.', 'The first face — 9 times the height 5. 45.'),
        ('12 · 4 = 48 appears', '12 · 5 = 60 appears'), ('The next one — 12 times 4. 48.', 'The next one — 12 times 5. 60.'),
        ('13 · 4 = 52 appears', '15 · 5 = 75 appears'), ('The last one — 13 times 4. 52.', 'The last one — 15 times 5. 75.'),
        ('20 + 48 + 52 = 120 appears', '45 + 60 + 75 = 180 appears'),
        ('Add it all up: 48 and 52 make 100, plus 20 — 120.', 'Add it all up: 45 and 75 make 120, plus 60 — 180.'),
        ('adding the two triangle bases gives 180', 'adding the two triangle bases gives 288')])

    # ---------- g125: 12 cubes -> 2 x 2 x 3 = 32 (Hebrew 8 cubes -> 2 x 2 x 2 = 24)  ==>  18 cubes -> 2 x 3 x 3 = 42
    g = 'geo35-g125'; V = 'solve-' + g
    _rn_q(M, g, stem='Eighteen identical cubes, each with edge 1 cm, are joined face to face to form a rectangular block. Which of the following block dimensions gives the smallest total surface area?',
          choices=['1 cm × 2 cm × 9 cm', '2 cm × 3 cm × 3 cm', '1 cm × 1 cm × 18 cm', '1 cm × 3 cm × 6 cm'], correct=2, expl=[
        'For dimensions a, b, c the total surface area is $2(ab+ac+bc)$.',
        'Choice 1, $1\\times2\\times9$: $2(2+9+18)=58$. Choice 2, $2\\times3\\times3$: $2(6+6+9)=42$. Choice 3, $1\\times1\\times18$: $2(1+18+18)=74$. Choice 4, $1\\times3\\times6$: $2(3+6+18)=54$.',
        'The smallest is 42: the block closest to a cube.'])
    _rn_fig(M, g, rn_fig_g125())
    _rn_sub(M, V, 2, [
        ('Twelve identical cubes, edge 1,', 'Eighteen identical cubes, edge 1,'),
        ('Next to choice 1 write 2(12 + 4 + 3) = 38', 'Next to choice 1 write 2(18 + 2 + 9) = 58'),
        ('Choice one, 1 by 3 by 4: front 12, top 4, side 3. 19, times 2 — 38. Remember it.',
         'Choice one, 1 by 2 by 9: front 18, top 2, side 9. 29, times 2 — 58. Remember it.'),
        ('Next to choice 2 write 2(6 + 6 + 4) = 32', 'Next to choice 2 write 2(9 + 6 + 6) = 42'),
        ('Choice two, 2 by 2 by 3: 6, 6 and 4 — 16, times 2 — 32.', 'Choice two, 2 by 3 by 3: 9, 6 and 6 — 21, times 2 — 42.'),
        ('Already smaller than 38.', 'Already smaller than 58.'),
        ('Next to choice 3 write 2(12 + 12 + 1) = 50 and cross it out', 'Next to choice 3 write 2(18 + 18 + 1) = 74 and cross it out'),
        ('Choice three, the long stick 1 by 1 by 12: 12, 12 and 1 — 25, times 2 — 50. Bigger. Out.',
         'Choice three, the long stick 1 by 1 by 18: 18, 18 and 1 — 37, times 2 — 74. Bigger. Out.'),
        ('Next to choice 4 write 2(12 + 6 + 2) = 40 and cross it out', 'Next to choice 4 write 2(18 + 6 + 3) = 54 and cross it out'),
        ('Choice four, 1 by 2 by 6: 12, 6 and 2 — 20, times 2 — 40. Also out.', 'Choice four, 1 by 3 by 6: 18, 6 and 3 — 27, times 2 — 54. Also out.'),
        ('choice two, 32. Not hard.', 'choice two, 42. Not hard.')])
    _rn_items(M, V, 3, {1: 'Separate: $18\\times6=108$ faces'})
    _rn_sub(M, V, 3, [
        ('Separate: 12 × 6 = 72 faces appears', 'Separate: 18 × 6 = 108 faces appears'),
        ('Twelve cubes lying apart — 72 faces.', 'Eighteen cubes lying apart — 108 faces.'),
        ('2 by 2 by 3. Choice two', '2 by 3 by 3. Choice two')])

    # ---------- g126 (letters): side 2a, height 3a; choice 3 (Hebrew: side a, height 2a, cylinder part)
    #            ==>  side 2k, height 5k; choice 4; plug in k = 2 (box 4 x 4 x 10)
    g = 'geo35-g126'; V = 'solve-' + g
    _rn_q(M, g, stem='A cylinder is inscribed in a box whose square base has side 2k and whose height is 5k. The cylinder has the same height as the box, and its circular bases are inscribed in the square bases. What fraction of the box’s volume lies outside the cylinder?',
          choices=['$1-\\frac{\\pi k}{4}$', '$1-\\frac{\\pi}{2}$', '$1-\\frac{\\pi}{4k}$', '$1-\\frac{\\pi}{4}$'], correct=4, expl=[
        'The box volume is $(2k)^2\\cdot5k=20k^3$.',
        'The circle is inscribed in the square with side 2k. Therefore its diameter is 2k and its radius is k. The cylinder volume is $\\pi k^2\\cdot5k=5\\pi k^3$.',
        'The part outside the cylinder: $\\frac{20k^3-5\\pi k^3}{20k^3}=1-\\frac{\\pi}{4}$.'])
    _rn_fig(M, g, lambda s: _relabel_t(s, {'2a': '2k'}))
    _rn_items(M, V, 2, {1: '$V_{\\text{cyl}}=\\pi k^2\\cdot5k=5\\pi k^3$', 2: '$V_{\\text{box}}=2k\\cdot2k\\cdot5k=20k^3$',
                        3: '$\\frac{20k^3-5\\pi k^3}{20k^3}=1-\\frac{\\pi}{4}$'})
    _rn_lines(M, V, 2, [
        'A cylinder is inscribed in a box. The square base has side 2k, the height is 5k. What fraction of the box is outside the cylinder?',
        'Cylinder volume: base area times height. A straight solid.',
        'We want everything in terms of k — no r. So look at the base.',
        ('d', 'On the top view, mark the diameter along the side 2k'),
        'The circle sits inside the square: the side of the square is the diameter. So 2r = 2k — the radius is k.',
        (1, 'V_cyl = πk² · 5k = 5πk³ appears'),
        'Pi k squared, times the height 5k: 5 pi k cubed.',
        (2, 'V_box = 2k · 2k · 5k = 20k³ appears'),
        'The box — multiply the dimensions: 20k cubed.',
        (3, 'Outside ÷ box appears'),
        'Outside is box minus cylinder. Divide by the box — k cubed cancels. 1 minus pi over 4.',
        ('d', 'Circle choice 4'),
        "Choice four. That's the full solution — and it's long."])
    _rn_items(M, V, 3, {1: '$k=1$: choices 1, 3, 4 all become $1-\\frac{\\pi}{4}$',
                        2: '$k=2$: box $4\\cdot4\\cdot10=160$, cylinder $\\pi\\cdot2^2\\cdot10=40\\pi$'})
    _rn_lines(M, V, 3, [
        "We learned it in circles: inscribed–circumscribed? Plug in numbers — don't fight with letters.",
        "Usually we'd think 1 is the easiest number.",
        (1, 'k = 1: choices 1, 3 and 4 all become 1 − π/4 appears'),
        "But look at the answers: with k = 1, choices one, three and four all turn into 1 minus pi over 4. It can't separate them.",
        "So pick a convenient number that isn't 1. k = 2.",
        (2, 'k = 2: box 4·4·10 = 160, cylinder π·2²·10 = 40π appears'),
        'Box: 4 by 4 by 10 — 160. Cylinder: radius 2, height 10 — 40 pi.',
        ('d', 'Write (160 − 40π)/160 = 1 − π/4'),
        'Outside over the box: 1 minus pi over 4.',
        ('d', 'Cross out choice 1 (1 − π/2) and choice 3 (1 − π/8)'),
        'Now put k = 2 in the answers. Choice one — 1 minus pi over 2. Out. Choice three — 1 minus pi over 8. Out.',
        ('d', 'Cross out choice 2 and circle choice 4'),
        'Choice two has no k — 1 minus pi over 2. Not ours. Choice four. The recommended approach — the safest.'])
    _rn_items(M, V, 4, {1: 'Volume $\\div$ volume: $k$ must cancel'})
    _rn_lines(M, V, 4, [
        'Third approach — psychometric thinking, estimating sizes.',
        'Remember the rule from circles: make the shape bigger or smaller — the ratio stays the same.',
        (1, 'Volume ÷ volume: k must cancel appears'),
        "Volume over volume — the k's cancel and we get a fixed number. Same for area over area, perimeter over perimeter.",
        ('d', 'Cross out choices 1 and 3'),
        'So any answer with a k in it is a distractor. Choices one and three — out.',
        (2, '1 − π/2 ≈ 1 − 1.57 < 0 appears'),
        "Choice two: pi over 2 is about 1.57. 1 minus 1.57 — negative. A part of the box can't be a negative fraction.",
        ('d', 'Cross out choice 2 and circle choice 4'),
        'Choice four. And it makes sense: pi over 4 is about three quarters — the cylinder is about three quarters of the box. A quarter is outside.',
        'Three approaches: full math — not recommended. Plugging in — the safest. Estimating — depends on the answers.',
        'Here the estimate knocked out all three. Sometimes it only knocks out some.'])

    # ---------- g127: 54 left -> pyramid 27 (Hebrew 18 left -> 9)  ==>  60 left -> pyramid 30 (a³ = 90, a not whole)
    g = 'geo35-g127'; V = 'solve-' + g
    _rn_q(M, g, stem='A pyramid is removed from a cube. The pyramid’s base is the entire bottom face of the cube, and its apex lies on the top face. The remaining solid has volume 60 cm³. What was the volume of the pyramid (in cm³)?',
          choices=['$40$', '$20$', '$30$', '$90$'], correct=3, expl=[
        'The pyramid has the same base and the same height as the cube. Therefore it is $\\frac13$ of the cube, and the part left is $\\frac23$.',
        'In ratio units, pyramid : left : cube = 1 : 2 : 3. Two units are 60, so one unit is $60\\div2=30$ cm³.'])
    _rn_items(M, V, 2, {1: '$V_{\\text{cube}}-V_{\\text{pyramid}}=60$', 2: '$a^3-\\frac{a^3}{3}=60\\ \\Rightarrow\\ \\frac{2a^3}{3}=60$',
                        3: '$a^3=90\\ \\Rightarrow\\ \\frac{a^3}{3}=30$'})
    _rn_sub(M, V, 2, [
        ('54 is left.', '60 is left.'), ('Cube − pyramid = 54 appears', 'Cube − pyramid = 60 appears'),
        ('a³ − a³/3 = 54 appears', 'a³ − a³/3 = 60 appears'), ('two thirds of a cubed is 54.', 'two thirds of a cubed is 60.'),
        ('a³ = 81 appears', 'a³ = 90 appears'),
        ("a cubed is 81. And here — a isn't even a whole number. But we don't need a! The pyramid is a cubed over 3: 27.",
         "a cubed is 90. And here — a isn't even a whole number. But we don't need a! The pyramid is a cubed over 3: 30."),
        ('Circle choice 1', 'Circle choice 3'), ('Choice one.', 'Choice three.')])
    _rn_items(M, V, 3, {2: '$1$ unit $=60\\div2=30$'})
    _rn_sub(M, V, 3, [
        ('Write 2 units = 54', 'Write 2 units = 60'), ("What's left is 54. So two units are 54.", "What's left is 60. So two units are 60."),
        ('1 unit = 54 ÷ 2 = 27 appears', '1 unit = 60 ÷ 2 = 30 appears'), ('One unit — divide by 2. 27. Done.', 'One unit — divide by 2. 30. Done.'),
        ('Circle choice 1', 'Circle choice 3'), ('Choice one. Simple and easy.', 'Choice three. Simple and easy.')])

    # ---------- g128: side 2sqrt2, edge 5 -> sqrt21 (Hebrew sqrt2, 4 -> sqrt15)  ==>  side 4sqrt2, edge 7 -> OB = 4, h = sqrt33
    g = 'geo35-g128'; V = 'solve-' + g
    _rn_q(M, g, stem='A pyramid has a square base with side $4\\sqrt2$ cm. Each lateral edge is 7 cm. What is the height of the pyramid (in cm)?',
          choices=['$7\\sqrt2$', '$\\sqrt{33}$', '$\\sqrt{65}$', '$5\\sqrt2$'], correct=2, expl=[
        'All lateral edges are equal. Therefore the apex P is above the center O of the square.',
        'The base diagonal is $4\\sqrt2\\cdot\\sqrt2=8$ (silver triangle: hypotenuse = leg $\\times\\sqrt2$). Half of it: $OB=4$.',
        'Triangle POB is right-angled at O: $h^2+4^2=7^2$, $h^2=33$, $h=\\sqrt{33}$.',
        'Check: the height must be less than the slanted edge, 7. Only $\\sqrt{33}$ is less than $\\sqrt{49}=7$ ($5\\sqrt2=\\sqrt{50}$ is just above it).'])
    _rn_fig(M, g, rn_fig_g128())
    _rn_sub(M, V, 2, [
        ('side 2 root 2. Each lateral edge is 5.', 'side 4 root 2. Each lateral edge is 7.'),
        ("What's given? The lateral edge, 5.", "What's given? The lateral edge, 7."),
        ('We have the hypotenuse, 5.', 'We have the hypotenuse, 7.')])
    _rn_items(M, V, 3, {2: '$4\\sqrt2\\div\\sqrt2=4\\ \\Rightarrow\\ OB=4$', 3: '$h^2+4^2=7^2\\ \\Rightarrow\\ h^2=33$', 4: '$h=\\sqrt{33}$'})
    _rn_sub(M, V, 3, [
        ('The base is a square with side 2 root 2.', 'The base is a square with side 4 root 2.'),
        ('2 root 2 over root 2 — 2. So OB is 2.', '4 root 2 over root 2 — 4. So OB is 4.'),
        ('Write 2 on OB', 'Write 4 on OB'),
        ('Leg 2, hypotenuse 5.', 'Leg 4, hypotenuse 7.'),
        ('h² + 2² = 5² appears', 'h² + 4² = 7² appears'),
        ('h squared plus 4 is 25. h squared is 21.', 'h squared plus 16 is 49. h squared is 33.'),
        ('h = √21 appears', 'h = √33 appears'),
        ('21 has no whole root: h is root 21.', '33 has no whole root: h is root 33.')])
    _rn_items(M, V, 4, {1: '$h<7=\\sqrt{49}$'})
    _rn_lines(M, V, 4, [
        'Now the psychometric solution — estimating sizes.',
        'Look at the height. If the lateral edge is 7 — must the height be less than 7?',
        'The height is the SHORTEST distance from the apex to the base. The edge is slanted — longer.',
        (1, 'h < 7 = √49 appears'),
        'So the height is less than 7. Our anchor: root 49 is exactly 7.',
        ('d', 'Cross out choice 1 (7√2 ≈ 9.8)'),
        '7 root 2 — root 2 is about 1.4. About 9.8. Too big. Out.',
        ('d', 'Next to choice 2 write √33 < √49 ✓'),
        "Root 33 — less than root 49. Possible. Not certain yet — but possible. Don't cross it out.",
        ('d', 'Cross out choice 3 (√65 > √49)'),
        'Root 65 — more than root 49. More than 7. Out.',
        ('d', 'Cross out choice 4 (5√2 = √50 > √49)'),
        "5 root 2 — that's root 50. Just above 7. Out.",
        ('d', 'Circle choice 2'),
        'Three out — mark the fourth. Choice two.',
        'Two ways: full math — and here the psychometric solution was much shorter.'])

    # ---------- g129: edge 3sqrt2 -> side 6 -> 9sqrt3 (Hebrew sqrt2 -> 2 -> sqrt3)  ==>  edge 4sqrt2 -> side 8 -> 16sqrt3
    g = 'geo35-g129'; V = 'solve-' + g
    _rn_q(M, g, stem='The edge of cube ABCDEFGH is $4\\sqrt2$ cm. What is the area of triangle BDG (in cm²)?',
          choices=['$32\\sqrt3$', '$48$', '$16\\sqrt3$', '$16$'], correct=3, expl=[
        'BD, DG and GB are diagonals of equal square faces. Therefore all three are equal: $4\\sqrt2\\cdot\\sqrt2=8$.',
        'Triangle BDG is equilateral with side 8. Its area is $\\frac{8^2\\sqrt3}{4}=16\\sqrt3$ cm².'])
    _rn_fig(M, g, lambda s: _relabel_t(s, {'3√2': '4√2'}))
    _rn_items(M, V, 2, {1: '$BD=4\\sqrt2\\cdot\\sqrt2=8$', 2: '$GM^2=4^2+(4\\sqrt2)^2=16+32=48$', 3: '$GM=4\\sqrt3$'})
    _rn_sub(M, V, 2, [
        ('The edge of the cube is 3 root 2.', 'The edge of the cube is 4 root 2.'),
        ('BD = 3√2 · √2 = 6 appears', 'BD = 4√2 · √2 = 8 appears'),
        ('3 root 2 times root 2 — 6.', '4 root 2 times root 2 — 8.'),
        ('The edge CG — 3 root 2 — stands straight up.', 'The edge CG — 4 root 2 — stands straight up.'),
        ('CM is half of 6 — 3.', 'CM is half of 8 — 4.'),
        ('GM² = 3² + (3√2)² = 27 appears', 'GM² = 4² + (4√2)² = 48 appears'),
        ('Leg 3, leg 3 root 2. Not golden, not silver, not a triple — full Pythagoras. 9 plus 18 — 27.',
         'Leg 4, leg 4 root 2. Not golden, not silver, not a triple — full Pythagoras. 16 plus 32 — 48.'),
        ('GM = 3√3 appears', 'GM = 4√3 appears'), ('The height is 3 root 3.', 'The height is 4 root 3.')])
    _rn_items(M, V, 3, {1: '$S=\\frac{8\\cdot4\\sqrt3}{2}=16\\sqrt3$'})
    _rn_sub(M, V, 3, [
        ('S = 6 · 3√3 / 2 = 9√3 appears', 'S = 8 · 4√3 / 2 = 16√3 appears'),
        ('Base 6, height 3 root 3, over 2: 9 root 3.', 'Base 8, height 4 root 3, over 2: 16 root 3.')])
    _rn_items(M, V, 4, {1: '$S=\\frac{a^2\\sqrt3}{4}=\\frac{64\\sqrt3}{4}=16\\sqrt3$'})
    _rn_sub(M, V, 4, [
        ('BD — a diagonal on the bottom face. 6.', 'BD — a diagonal on the bottom face. 8.'),
        ('All three sides are 6.', 'All three sides are 8.'),
        ('S = a²√3/4 = 36√3/4 = 9√3 appears', 'S = a²√3/4 = 64√3/4 = 16√3 appears'),
        ('36 over 4 — 9 root 3.', '64 over 4 — 16 root 3.')])

    # ---------- g130: edge 2 (Hebrew 1); lesson examples edge 5 / diagonal 18 / box 6 x 8 x 24 (Hebrew 5, 12, 3 x 4 x 12)
    #            ==>  edge 3 -> 3 + 3sqrt2 + 3sqrt3; edge 8 -> 8sqrt3; diagonal 27 -> 9sqrt3; 14/sqrt2 = 7sqrt2; box 9 x 12 x 8 -> 17
    g = 'geo35-g130'; V = 'solve-' + g
    _rn_q(M, g, stem='The edge of cube ABCDEFGH is 3 cm. What is the perimeter of triangle AEG (in cm)?',
          choices=['$3+6\\sqrt2$', '$9\\sqrt2$', '$3+3\\sqrt3$', '$3+3\\sqrt2+3\\sqrt3$'], correct=4, expl=[
        'AE = 3. The top-face diagonal is $EG=\\sqrt{3^2+3^2}=3\\sqrt2$. Since AE is perpendicular to the top face, triangle AEG is right at E. '
        'Thus $AG=\\sqrt{3^2+(3\\sqrt2)^2}=\\sqrt{27}=3\\sqrt3$. Add the three sides: $3+3\\sqrt2+3\\sqrt3$.'])
    _rn_fig(M, g, lambda s: _relabel_t(s, {'2': '3'}))
    _rn_items(M, V, 2, {1: '$EG=3\\cdot\\sqrt2=3\\sqrt2$', 2: '$AG^2=3^2+(3\\sqrt2)^2=9+18=27$', 3: '$AG=\\sqrt{27}=3\\sqrt3$', 4: '$P=3+3\\sqrt2+3\\sqrt3$'})
    _rn_sub(M, V, 2, [
        ('The edge of the cube is 2.', 'The edge of the cube is 3.'),
        ('Write 2 on AE', 'Write 3 on AE'), ('The edge is 2.', 'The edge is 3.'),
        ('EG = 2√2 appears', 'EG = 3√2 appears'),
        ('EG — a diagonal on a square with side 2. Two silver triangles: leg to hypotenuse, times root 2. 2 root 2.',
         'EG — a diagonal on a square with side 3. Two silver triangles: leg to hypotenuse, times root 2. 3 root 2.'),
        ('AG² = 2² + (2√2)² = 12 appears', 'AG² = 3² + (3√2)² = 27 appears'),
        ('Two legs — Pythagoras: 4 plus 8 — 12.', 'Two legs — Pythagoras: 9 plus 18 — 27.'),
        ('AG = 2√3 appears', 'AG = 3√3 appears'), ('Root 12 — 2 root 3.', 'Root 27 — 3 root 3.'),
        ('P = 2 + 2√2 + 2√3 appears', 'P = 3 + 3√2 + 3√3 appears'),
        ('Perimeter: 2 plus 2 root 2 plus 2 root 3.', 'Perimeter: 3 plus 3 root 2 plus 3 root 3.')])
    _rn_items(M, V, 3, {2: 'Edge $8\\rightarrow$ diagonal $8\\sqrt3$', 3: 'Diagonal $27\\rightarrow$ edge $\\frac{27}{\\sqrt3}=\\frac{27\\sqrt3}{3}=9\\sqrt3$'})
    _rn_sub(M, V, 3, [
        ('Edge 5 → body diagonal 5√3 appears', 'Edge 8 → body diagonal 8√3 appears'),
        ("edge 5, what's the diagonal? 5 root 3. Instantly.", "edge 8, what's the diagonal? 8 root 3. Instantly."),
        ('Diagonal 18 → edge 18/√3 = 6√3 appears', 'Diagonal 27 → edge 27/√3 = 9√3 appears'),
        ('The other way round? Diagonal 18 — divide by root 3. Our method: ignore the root, 18 over 3 is 6, attach the root — 6 root 3.',
         'The other way round? Diagonal 27 — divide by root 3. Our method: ignore the root, 27 over 3 is 9, attach the root — 9 root 3.'),
        ('Multiply the top and the bottom by root 3: 18 root 3 over 3. And 18 over 3 is 6.',
         'Multiply the top and the bottom by root 3: 27 root 3 over 3. And 27 over 3 is 9.'),
        ('Same with root 2: 18 over root 2 is 18 root 2 over 2 — 9 root 2.', 'Same with root 2: 14 over root 2 is 14 root 2 over 2 — 7 root 2.')])
    _rn_items(M, V, 4, {1: 'Box $9\\times12\\times8$', 2: 'Base: $9,\\ 12\\rightarrow15$', 3: '$15,\\ 8\\rightarrow17$',
                        4: 'One step: $\\sqrt{9^2+12^2+8^2}=\\sqrt{289}=17$'})
    _rn_sub(M, V, 4, [
        ('Box 6 × 8 × 24 appears', 'Box 9 × 12 × 8 appears'),
        ('A box: 6 by 8, height 24.', 'A box: 9 by 12, height 8.'),
        ('Base: 6, 8 → 10 appears', 'Base: 9, 12 → 15 appears'),
        ('First the diagonal of the base: 6, 8 — the right angle there — a 3-4-5 triple times 2. 10.',
         'First the diagonal of the base: 9, 12 — the right angle there — a 3-4-5 triple times 3. 15.'),
        ('10, 24 → 26 appears', '15, 8 → 17 appears'),
        ('Now with the height, another right triangle: 10 and 24. 5-12-13 times 2 — hamsa, bat mitzvah, bar mitzvah. 26.',
         'Now with the height, another right triangle: 15 and 8. The triple 8, 15, 17 — 17.'),
        ('Or in one step: the root of 6 squared plus 8 squared plus 24 squared. Root 676 — 26.',
         'Or in one step: the root of 9 squared plus 12 squared plus 8 squared. 81 plus 144 plus 64 — root 289. 17.')])

    # ---------- g131: edge 3 into 10 x 7 x 8 -> 12 (Hebrew 2 into 6 x 4 x 5 -> 12)  ==>  edge 4 into 18 x 9 x 11 -> 16
    g = 'geo35-g131'; V = 'solve-' + g
    _rn_q(M, g, stem='Identical cubes with edge 4 cm are placed in a box with internal dimensions 18 cm × 9 cm × 11 cm. The cube edges must be parallel to the box edges. What is the greatest number of cubes that can fit entirely inside the box?',
          choices=['$24$', '$16$', '$20$', '$27$'], correct=2, expl=[
        'Solid cubes are not water: count each direction and drop the remainder.',
        'Length: $18\\div4=4$ cubes (remainder 2). Width: $9\\div4=2$ (remainder 1). Height: $11\\div4=2$ (remainder 3).',
        '$4\\times2\\times2=16$. Trap: dividing volumes, $1782\\div64\\approx27.8$, treats the cubes like water.'])
    _rn_fig(M, g, rn_fig_g131())
    _rn_sub(M, V, 2, [('Cubes with edge 3 go into a box 10 by 7 by 8.', 'Cubes with edge 4 go into a box 18 by 9 by 11.')])
    _rn_items(M, V, 3, {1: '$18\\div4=4$ (remainder 2)', 2: '$9\\div4=2$ (remainder 1)', 3: '$11\\div4=2$ (remainder 3)', 4: '$4\\cdot2\\cdot2=16$'})
    _rn_sub(M, V, 3, [
        ('10 ÷ 3 = 3 (+1) appears', '18 ÷ 4 = 4 (+2) appears'), ('3 into 10 — 3 full times.', '4 into 18 — 4 full times.'),
        ('7 ÷ 3 = 2 (+1) appears', '9 ÷ 4 = 2 (+1) appears'), ('3 into 7 — twice.', '4 into 9 — twice.'),
        ('8 ÷ 3 = 2 (+2) appears', '11 ÷ 4 = 2 (+3) appears'), ('3 into 8 — twice, with 2 left.', '4 into 11 — twice, with 3 left.'),
        ('3 · 2 · 2 = 12 appears', '4 · 2 · 2 = 16 appears'), ('Multiply: 3 times 2 times 2 — 12.', 'Multiply: 4 times 2 times 2 — 16.'),
        ('dividing volumes — 560 over 27 — about 20.7. Choice four, 20, is waiting',
         'dividing volumes — 1782 over 64 — about 27.8. Choice four, 27, is waiting')])

    # ---------- g132: 27 cubes, edge 2 -> volume -8, faces 4 cm² (Hebrew 8 cubes, edge 1)  ==>  27 cubes, edge 4 -> -64, faces 16 cm²
    g = 'geo35-g132'; V = 'solve-' + g
    _rn_q(M, g, stem='Twenty-seven identical cubes, each with edge 4 cm, form a larger cube. One corner cube is removed, as shown in the accompanying figure. How do the volume and total surface area of the remaining solid change?',
          choices=['The volume is unchanged, and the surface area is unchanged.',
                   'The volume decreases by 64 cm³, and the surface area is unchanged.',
                   'The volume decreases by 64 cm³, and the surface area decreases by 48 cm².',
                   'The volume decreases by 64 cm³, and the surface area increases by 48 cm².'], correct=2, expl=[
        'The removed cube has volume $4^3=64$ cm³. The volume goes down by 64.',
        'The corner cube showed 3 faces, each $4\\times4=16$ cm². Removing it loses those 3 faces, but 3 faces of its neighbors appear.',
        'Lose 3, gain 3: the surface area does not change.'])
    _rn_sub(M, V, 2, [('27 cubes with edge 2 form a big cube.', '27 cubes with edge 4 form a big cube.'),
                      ('The others all say it drops by 8, one small cube.', 'The others all say it drops by 64, one small cube.')])


# --- practice: new numbers ---------------------------------------------------------------------
def rn_practice_questions(M):
    P = lambda k: 'geo35-core-p%02d' % k
    # p01: rectangle 5 x 3 about the 5 side -> 45pi  ==>  7 x 4 about the 7 side -> r 4, h 7 -> 112pi
    _rn_q(M, P(1), stem='A rectangle measuring 7 cm × 4 cm is rotated through one full turn about one of its 7 cm sides. What is the volume of the solid formed (in cm³)?',
          choices=['$224\\pi$', '$112\\pi$', '$28\\pi$', '$196\\pi$'], correct=2, expl=[
        'A rectangle turned about a side makes a cylinder. The side on the axis, 7, is the height. The other side, 4, is the radius.',
        'Volume: $\\pi\\cdot4^2\\cdot7=112\\pi$ cm³. Trap: $196\\pi$ swaps the radius and the height.'])
    _rn_fig(M, P(1), rn_fig_p01())
    # p02: cone r 2a, h 6a -> 8pi a³  ==>  r 3a, h 4a -> 12pi a³
    _rn_q(M, P(2), stem='A cone has base radius 3a and height 4a, where a > 0. What is its volume?',
          choices=['$36\\pi a^3$', '$12\\pi a^2$', '$12\\pi a^3$', '$4\\pi a^3$'], correct=3, expl=[
        '$V=\\frac{\\pi(3a)^2(4a)}3=\\frac{36\\pi a^3}3=12\\pi a^3$. Square both the 3 and the a in the radius.',
        'Traps: $36\\pi a^3$ forgets to divide by 3; $4\\pi a^3$ squares only the a.'])
    _rn_fig(M, P(2), rn_fig_p02())
    # p03: V 112, square faces 4 -> h 7 -> 28  ==>  V 150, square faces 5 -> h 6 -> 30
    _rn_q(M, P(3), stem='A box has volume 150 cm³. Two of its faces are squares with side 5 cm, and its other four faces are rectangles that are not squares. What is the area of each rectangular face (in cm²)?',
          choices=['$25$', '$60$', '$30$', '$36$'], correct=3, expl=[
        'The two square faces are opposite each other. The edges are 5, 5 and h: $25h=150$, $h=6$.',
        'Each rectangular face: $5\\times6=30$ cm².'])
    _rn_fig(M, P(3), rn_fig_p03())
    # p04: cylinder r 4, h 6 (numbers not needed) -> 2 : 1  ==>  r 5, h 9, new choice order
    _rn_q(M, P(4), stem='A cone is removed from a cylinder with radius 5 cm and height 9 cm. The cone has the same base and height as the cylinder. What is the ratio of the remaining volume to the removed volume?',
          choices=['$1:2$', '$3:1$', '$2:3$', '$2:1$'], correct=4, expl=[
        'The cone is $\\frac13$ of the cylinder. The part left is $\\frac23$.',
        'The ratio of the remaining volume to the removed volume is $\\frac23:\\frac13=2:1$. (The numbers 5 and 9 are not needed.)'])
    # p05: cube edge 2 -> 12 + 4sqrt2  ==>  edge 3 -> 27 + 9sqrt2
    _rn_q(M, P(5), stem='A cube with edge 3 cm is cut into two congruent triangular prisms by a plane through diagonals of two opposite faces. What is the total surface area of one prism (in cm²)?',
          choices=['$54+9\\sqrt2$', '$27+9\\sqrt2$', '$27+3\\sqrt2$', '$18+9\\sqrt2$'], correct=2, expl=[
        'The two triangular bases together make one $3\\times3$ square, area 9. Two lateral faces are $3\\times3$ squares, total area 18. '
        'The cut face is a rectangle with sides 3 and $3\\sqrt2$, area $9\\sqrt2$. Total: $27+9\\sqrt2$.'])
    # p06: AB 8, AD 4, h 5, AM = NC = 3 -> 80  ==>  AB 10, AD 3, h 8, AM = NC = 4 -> trapezoid (4 + 6) x 3 / 2 = 15 -> 120
    _rn_q(M, P(6), stem='A box has base ABCD, with AB = 10 cm, AD = 3 cm, and height 8 cm. M lies on AB and N lies on DC, with AM = NC = 4 cm. A prism has base AMND and the same height as the box. What is its volume (in cm³)?',
          choices=['$240$', '$120$', '$96$', '$144$'], correct=2, expl=[
        '$DN=DC-NC=10-4=6$. The base AMND is a trapezoid with parallel sides $AM=4$ and $DN=6$ and height $AD=3$.',
        'Its area: $\\frac{(4+6)\\cdot3}{2}=15$. The volume: $15\\times8=120$ cm³. (Since AM = NC, the prism is exactly half of the box, 240.)'])
    _rn_fig(M, P(6), rn_fig_p06())
    # p07: two pentagonal pyramids : cube = 15 : 12  ==>  two hexagonal pyramids : cube = 18 : 12 = 3/2
    _rn_q(M, P(7), stem='Solid A is formed by joining two hexagonal pyramids along their entire bases. Solid B is a cube. What is the ratio of the number of edges of A to the number of edges of B?',
          choices=['$1$', '$2$', '$\\frac23$', '$\\frac32$'], correct=4, expl=[
        'Solid A: 6 edges around the shared hexagon, 6 up to the top apex and 6 down to the bottom apex — 18 edges. A cube has 12 edges.',
        'The ratio is $\\frac{18}{12}=\\frac32$. Traps: 1 compares the vertices (8 and 8); 2 compares the faces (12 and 6).'])
    _rn_fig(M, P(7), rn_fig_p07())
    # p08: AM = AB/3, DN = 2DC/3 -> 2 : 1  ==>  AM = AB/4, DN = 3DC/4 -> 3 : 1
    _rn_q(M, P(8), stem='The base of a box is square ABCD. M lies on AB and N lies on DC. Given:\n$\\begin{cases} AM=\\frac14AB \\\\ DN=\\frac34DC \\end{cases}$\nVertical planes through AN and MC divide the box into a middle prism with base AMCN and two outer prisms. What is the ratio of the combined outer volumes to the middle volume?',
          choices=['$1:3$', '$3:1$', '$1:1$', '$4:3$'], correct=2, expl=[
        '$NC=DC-DN=\\frac14$ of the side, and $AM=\\frac14$ of the side. AMCN is a parallelogram with base AM and height AD.',
        'Its area is $\\frac14$ of the square. The two outer parts make $\\frac34$.',
        'All three prisms have the same height. Therefore the ratio of the volumes is $\\frac34:\\frac14=3:1$.'])
    _rn_fig(M, P(8), rn_fig_p08)
    # p09 (letters): angle AEG, choice 2  ==>  angle BFH, choice 4
    _rn_q(M, P(9), stem='In cube ABCDEFGH, FH is a diagonal of the top face EFGH. What is angle BFH?',
          choices=['$60°$', '$45°$', '$75°$', '$90°$'], correct=4, expl=[
        'Edge FB is perpendicular to the top face EFGH. So it is perpendicular to every line in that face that passes through F, including the diagonal FH.',
        'Therefore angle BFH $=90°$.'])
    _rn_fig(M, P(9), rn_fig_p09)
    # p10: stepped solid, edge 3 -> 0  ==>  edge 4 -> 0 (faces 16 cm²)
    _rn_q(M, P(10), stem='Twelve cubes, each with edge 4 cm, form the stepped solid shown in the accompanying figure. The highlighted cube is removed. What is the change in the total surface area (in cm²)?',
          choices=['$16$', '$32$', '$0$', '$48$'], correct=3, expl=[
        'The highlighted cube shows 3 faces: front, top and bottom. It touches 3 cubes: left, right and behind.',
        'Removing it loses its 3 faces and uncovers 3 faces of its neighbors. Each face is $4\\times4=16$ cm²: $-48+48=0$.'])
    # p11: 9 x 7 x 5 -> 245  ==>  10 x 8 x 6 -> 8 x 8 x 6 = 384
    _rn_q(M, P(11), stem='A rectangular block measures 10 cm × 8 cm × 6 cm. One straight cut parallel to a face leaves a smaller rectangular block with at least one square face. What is the greatest possible volume of the smaller block (in cm³)?',
          choices=['$360$', '$288$', '$480$', '$384$'], correct=4, expl=[
        'Reducing 10 to 8 gives dimensions 8, 8, 6 and volume 384. Reducing 8 to 6 gives 10, 6, 6 and volume 360. Reducing 10 to 6 gives 6, 8, 6 and volume 288. '
        'Any further reduction gives no larger valid block. The maximum is 384. (480 is the whole block, which is not cut.)'])
    # p12: product 350, volume 140 -> 5/2  ==>  product 378, volume 108 -> 7/2
    _rn_q(M, P(12), stem='The product of the numerical areas of two adjacent faces of a box is 378. The volume of the box is 108 cm³. The face areas are measured in cm². What is the length of their common edge (in cm)?',
          choices=['$3$', '$\\frac72$', '$6$', '$7$'], correct=2, expl=[
        'Let the common edge be a and the other edges b and c. The two faces are ab and ac: $(ab)(ac)=a^2bc=378$.',
        'The volume is $abc=108$. Divide: $\\frac{a^2bc}{abc}=a=\\frac{378}{108}=\\frac72$.'])
    # p13: r 1, h 4 in a cube of 12 -> 6 x 6 x 3 = 108  ==>  r 1, h 5 in a cube of 10 -> 5 x 5 x 2 = 50
    _rn_q(M, P(13), stem='Cylinders with radius 1 cm and height 5 cm are packed upright in a cube with internal edge 10 cm. In each layer, their bases are arranged in straight rows and columns parallel to the cube’s edges. What is the greatest number of cylinders that can fit?',
          choices=['$200$', '$25$', '$50$', '$63$'], correct=3, expl=[
        'Each diameter is 2 cm. Along each 10 cm side: $10\\div2=5$ cylinders. One layer: $5\\times5=25$.',
        'Height: $10\\div5=2$ layers. Total: $25\\times2=50$. Traps: 200 uses the radius instead of the diameter; 63 divides the volumes ($1000\\div5\\pi\\approx63.7$).'])
    _rn_fig(M, P(13), rn_fig_p13())
    # p14: h 12, base 9pi, two cuts -> 4 x 9pi = 36pi  ==>  h 15, base 16pi -> 64pi
    _rn_q(M, P(14), stem='A cylinder has height 15 cm and base area 16π cm². Two cuts parallel to its bases divide it into three cylinders of equal height. By how much does the sum of their total surface areas exceed the original surface area (in cm²)?',
          choices=['$96\\pi$', '$64\\pi$', '$32\\pi$', '$48\\pi$'], correct=2, expl=[
        'The curved lateral surface is divided, but its total area is unchanged. Each of the two cuts creates two new circular faces, giving four new bases.',
        'The increase is $4\\times16\\pi=64\\pi$.'])
    # p15: chalk 3 x 2 x 1½ = 9, 3/8 a day -> 24  ==>  4 x 2 x 2½ = 20, 5/8 a day -> 32
    _rn_q(M, P(15), stem='A rectangular block of drawing chalk measures 4 cm × 2 cm × $2\\frac12$ cm. Each complete day of use removes at least $\\frac58$ cm³ of chalk. For how many complete days, at most, can the block last?',
          choices=['$25$', '$40$', '$12$', '$32$'], correct=4, expl=[
        'The volume: $4\\times2\\times\\frac52=20$ cm³. The block lasts longest when only $\\frac58$ cm³ is used each day.',
        '$20\\div\\frac58=20\\times\\frac85=32$ days.'])
    # p16: r 3, h 8, 150° sector -> 30pi  ==>  r 4, h 6, 135° sector -> 3/8 of 96pi = 36pi
    _rn_q(M, P(16), stem='A right cylinder has radius 4 cm and height 6 cm. A solid is formed by extending a 135° sector of its base through the full height. What is the volume of this solid (in cm³)?',
          choices=['$32\\pi$', '$48\\pi$', '$36\\pi$', '$24\\pi$'], correct=3, expl=[
        'The full cylinder: $\\pi\\cdot4^2\\cdot6=96\\pi$.',
        'A 135° sector is $\\frac{135}{360}=\\frac38$ of the circle (as in the circles topic). The solid is the same fraction of the cylinder: $\\frac38\\times96\\pi=36\\pi$ cm³.'])
    _rn_fig(M, P(16), rn_fig_p16)
    # p17: cube in a cylinder of radius 5 -> pi/2 - 1  ==>  radius 3 (the ratio does not depend on it), new choice order
    _rn_q(M, P(17), stem='A cube is inscribed in a cylinder of radius 3 cm. The top and bottom faces of the cube are inscribed in the circular bases of the cylinder. What is the ratio of the volume outside the cube but inside the cylinder to the volume of the cube?',
          choices=['$\\frac2\\pi$', '$\\frac{\\pi}{2}-1$', '$1-\\frac2\\pi$', '$\\frac{\\pi}{4}-1$'], correct=2, expl=[
        'The square is inscribed in the circle. Its diagonal is the diameter, 6. Its area: $\\frac{6^2}{2}=18$. The circle area: $9\\pi$.',
        'Both solids have the same height. Therefore the volume ratio equals the ratio of the base areas: $\\frac{9\\pi-18}{18}=\\frac{\\pi}{2}-1$.'])
    _rn_fig(M, P(17), lambda s: _relabel_t(s, {'10': '6'}))
    # p18: two cylinders r 3, h 7 -> 12 x 6 x 7 = 504  ==>  r 4, h 5 -> 16 x 8 x 5 = 640
    _rn_q(M, P(18), stem='Two cylinders, each of radius 4 cm and height 5 cm, stand side by side, as shown in the accompanying figure. Their bases are tangent, and the box fits tightly around this arrangement. What is the volume of the box (in cm³)?',
          choices=['$480$', '$1280$', '$640$', '$320$'], correct=3, expl=[
        'Each diameter is 8. The base of the box is $16\\times8$ and its height is 5.',
        'Volume: $16\\times8\\times5=640$ cm³.'])
    _rn_fig(M, P(18), lambda s: _relabel_t(s, {'3': '4'}))
    # p19: volume = 2/9 edge -> face 2/9  ==>  volume = 3/16 edge -> face 3/16
    _rn_q(M, P(19), stem='The numerical value of a cube’s volume in cm³ is $\\frac3{16}$ times the numerical value of its edge length in cm. What is the area of one face (in cm²)?',
          choices=['$\\frac38$', '$\\frac3{16}$', '$\\frac{\\sqrt3}{4}$', '$\\frac34$'], correct=2, expl=[
        'Let the edge length be a. The numerical relation is $a^3=\\frac3{16}a$. Since a > 0, divide by a to obtain $a^2=\\frac3{16}$. This is already the area of a face.',
        'Trap: $\\frac{\\sqrt3}{4}$ is the edge, not the face.'])
    # p20: edge 2x -> E-ABD = 4x³/3  ==>  edge 3y -> 9y³/2
    _rn_q(M, P(20), stem='The edge of cube ABCDEFGH is 3y cm, where y > 0. What is the volume of triangular pyramid E–ABD (in cm³)?',
          choices=['$\\frac{27y^3}{2}$', '$9y^3$', '$\\frac{9y^3}{2}$', '$\\frac{9y^3}{4}$'], correct=3, expl=[
        'Triangle ABD has area $\\frac12(3y)(3y)=\\frac{9y^2}{2}$. The perpendicular height from E is EA = 3y.',
        'The pyramid volume is $\\frac13\\cdot\\frac{9y^2}{2}\\cdot3y=\\frac{9y^3}{2}$. Trap: $\\frac{27y^3}{2}$ forgets to divide by 3.'])
    _rn_fig(M, P(20), lambda s: _relabel_t(s, {'2x': '3y'}))


def rn_practice(M):
    """Approved clean-up (36 -> 26): the copies q-09 (= guided q-02, slant height) and q-14 (= guided q-03, painted
    cube); 3 of the 6 English extras (keep p23 three face areas, p24 painted cube, p25 body diagonal); the September
    items whose type the Hebrew practice already has or that another kept item drills (q-04 liters: q-13 drills it;
    q-08 cone -> cylinder pouring: q-05 + p04; q-12 compare volumes: p02 / p04; q-15 prism edges: p07; q-16 turning: p01)."""
    out = ['q-r26-t35-09', 'q-r26-t35-14',                          # copies
           'geo35-core-p21', 'geo35-core-p22', 'geo35-core-p26',    # extras: open box (p03 / p05 types), lateral -> volume (p14), cone vs cylinder (p04)
           'q-r26-t35-04', 'q-r26-t35-08', 'q-r26-t35-12', 'q-r26-t35-15', 'q-r26-t35-16']
    for qid in out:
        assert M.section_of(qid) == PRACT, qid
        M.unplace(qid)


def rn_lessons_cards(M):
    # Lesson "Solids: Surface and Volume": the Hebrew lesson's 330 ml cola can -> a 500 ml bottle of water
    L1 = 'geo-119'
    n = next(i for i, b in enumerate(M.video(L1)['beats'], 1) if b['title'] == 'Volume')
    _rn_sub(M, L1, n, [
        ('Imagine a can of cola.', 'Imagine a bottle of water.'),
        ('It always says on the can: 330 milliliters.', 'It always says on the bottle: 500 milliliters.'),
        ('That can holds 330 cubic centimeters.', 'That bottle holds 500 cubic centimeters.')])
    # "Cube and Box Facts": the Hebrew box 3 x 4 x 12 -> 13  ==>  2 x 6 x 9 -> 11
    FV = 'r26-t35-cubefacts'
    n = next(i for i, b in enumerate(M.video(FV)['beats'], 1) if b['title'] == 'Diagonals')
    _rn_sub(M, FV, n, [
        ('Write "3 × 4 × 12: √(9 + 16 + 144) = √169 = 13"', 'Write "2 × 6 × 9: √(4 + 36 + 81) = √121 = 11"'),
        ('3 by 4 by 12: 9 plus 16 plus 144 — 169. The diagonal is 13.', '2 by 6 by 9: 4 plus 36 plus 81 — 121. The diagonal is 11.')])


def _rn_sync(M):
    """Solution-video titles and 'Pre-loaded' notes follow the (changed) stems."""
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC or v.get('kind') != 'solution' or v.get('questionId') not in M.D['questions']: continue
        v['title'] = v['navLabel'] = M.q(v['questionId'])['stem']
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
    rn_lessons_cards(M)
    _rn_sync(M)


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
    # Q3 (cone 4 times a cylinder with the same base): compare by factors (topic 26)
    _sp_line(M, 'geo35-g122', r'Method 2 · Compare by factors: the base is the same, so only the height matters. With the same height a cone is $\frac13$ of the cylinder, so to hold as much it needs $\times3$ the height, and four times as much needs $\times4$ more: $h\cdot3\cdot4=12h$.')
    # Q7 (fraction of the box outside the cylinder): power count (topic 5) cuts the two mixed choices
    _sp_line(M, 'geo35-g126', r'Method 2 · Power count: a fraction of the box is volume $\div$ volume, power $3-3=0$ — a plain number. Choices 1 and 3 are mixed ($1$ has power 0, $\frac{\pi k}{4}$ power 1, $\frac{\pi}{4k}$ power $-1$): out. Choice 2 is negative ($\frac{\pi}{2}>1$): choice 4.')
    _sp_say_after(M, 'solve-geo35-g126', 4, 'Volume over volume',
                  "It's the power count from algebra: volume over volume is power 3 minus 3 — zero. And 1 minus pi k over 4 mixes power 0 with power 1.")
    # core practice (cone 3a, 4a): power count cuts the a² choice
    _sp_line(M, 'geo35-core-p02', r'Method 2 · Power count: a volume has power 3 ($3a\cdot3a\cdot4a$). Choice 2, $12\pi a^2$, has power 2 — out at once.')
    # core practice (water into a cylinder with twice the radius): compare by factors
    _sp_line(M, 'q-r26-t35-05', r'Method 2 · Compare by factors: the volume stays the same. The radius is $\times2$, so the base is $\times2^2=4$, and the height must be $\div4$: $\frac84=2$ cm.')


_apply_before_spread = apply


def apply(M):
    _apply_before_spread(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last


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
    # solve-geo35-g121 · the water: 3 < π < 3.5 gives 72 < 24π < 84, which decides every choice (no 24 × 3.14 ≈ 75.4)
    v = 'solve-geo35-g121'
    if not _nd_recorded(v):
        _nd_item(M, v, 'The water in the cone', r'$24\pi\approx24\times3.14\approx75.4$',
                 r'$3<\pi<3.5\;\Rightarrow\;72<24\pi<84$', label='72 < 24π < 84 appears')
        _nd_lines(M, v, 'The water in the cone', [
            ('say', "How much is that roughly? 24 times 3.14 — 72 plus 3.36. About 75.4. Remember that number — it's the water.",
             ["How much is that? Pi is more than 3 and less than three and a half.",
              "24 times 3 is 72. 24 times three and a half is 84. So the water is more than 72 and less than 84. Remember those two numbers."])])
        _nd_item(M, v, 'Go through the choices', r'Cube: $4^3=64<75.4$', r'Cube: $4^3=64<72$')
        _nd_item(M, v, 'Go through the choices', r'Pyramid: $\frac{6^2\cdot7}{3}=84$', r'Pyramid: $\frac{6^2\cdot7}{3}=84>24\pi$')
        _nd_lines(M, v, 'Go through the choices', [
            ('say', "4 cubed — 64. Less than the water.", "4 cubed — 64. Less than 72 — less than the water."),
            ('say', "84 is more than 75.4. This pyramid can hold all the water.",
             "84. And the water is less than 84. This pyramid can hold all of it.")])
        _nd_item(M, v, 'In the lesson: the rest', r'Box: $6\cdot4\cdot3=72<75.4$', r'Box: $6\cdot4\cdot3=72<24\pi$')
        _nd_lines(M, v, 'In the lesson: the rest', [
            ('say', "Careful — that one's close. If you round π to 3, the water is 72 and the box suddenly looks big enough. Use 3.14.",
             "Careful — that one's close. Pi is MORE than 3, not equal to 3. So the water is a bit more than 72 — the box is just too small.")])
    _nd_expl(M, 'geo35-g121', [
        (0, 'The cone holds', 'The cone holds $\\frac{\\pi(\\sqrt6)^2\\cdot12}{3}=24\\pi$ cm³ of water. Since $3<\\pi<3.5$: '
                              '$24\\cdot3<24\\pi<24\\cdot3.5$, so the water is more than $72$ and less than $84$.'),
        (1, 'Check each container.', 'Check each container. The cube (choice 1): $4^3=64$, too small. The pyramid (choice 2): '
                                     '$\\frac{6^2\\times7}{3}=84$, more than $24\\pi$: big enough. The box (choice 3): $6\\times4\\times3=72$, '
                                     'less than $24\\pi$: too small. The cylinder (choice 4): $\\pi(\\sqrt2)^2\\times10=20\\pi$, less than $24\\pi$.'),
        (2, 'Only the pyramid', 'Only the pyramid (84 cm³) can hold all the water. Careful with π: it is more than 3, so the water is '
                                'more than 72, and the box (72) is just too small.')])
    # solve-geo35-g126 · Estimate: π > 3 so π/2 > 3/2 > 1 (no 1.57)
    v = 'solve-geo35-g126'
    if not _nd_recorded(v):
        _nd_item(M, v, 'Approach 3 · Estimate', r'$1-\frac{\pi}{2}\approx1-1.57<0$',
                 r'$\frac{\pi}{2}>\frac{3}{2}>1\;\Rightarrow\;1-\frac{\pi}{2}<0$', label='π/2 > 3/2 > 1 → 1 − π/2 < 0 appears')
        _nd_lines(M, v, 'Approach 3 · Estimate', [
            ('say', "Choice two: pi over 2 is about 1.57. 1 minus 1.57 — negative. A part of the box can't be a negative fraction.",
             "Choice two: pi is more than 3, so pi over 2 is more than one and a half. 1 minus that — negative. A part of the box can't be a negative fraction.")])
    # solve-geo35-g128 · Estimate: 7√2 is more than 7 (no 9.8)
    v = 'solve-geo35-g128'
    if not _nd_recorded(v):
        _nd_lines(M, v, 'Approach 2 · Estimate', [
            ('draw', 'Cross out choice 1 (7√2 ≈ 9.8)', 'Cross out choice 1 (7√2 > 7)'),
            ('say', "7 root 2 — root 2 is about 1.4. About 9.8. Too big. Out.",
             "7 root 2 — root 2 is more than 1, so this is more than 7. Too big. Out.")])


_apply_before_no_decimal_estimates = apply


def apply(M):
    _apply_before_no_decimal_estimates(M)
    no_decimal_estimates(M)   # 2026-10-07 no decimal estimates: runs last
