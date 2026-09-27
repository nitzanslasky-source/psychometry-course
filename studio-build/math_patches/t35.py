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
            "A cone: radius, height and slant height. Radius 6, slant height 10 — the height is 8.",
            A("'Pyramid: height, half the diagonal, the edge' appears", T('Pyramid: height $\\cdot$ half the base diagonal $\\cdot$ the slanted edge', size=38, gap=30)),
            "A pyramid with equal edges: the apex is above the center. The height, half the diagonal and the edge.",
            A("'Height < slanted edge' appears", T('The height is shorter than any slanted edge', size=40)),
            "The height goes straight down. It's always shorter than a slanted edge."]),
        S(4, [
            A("'Cube: a√2 and a√3' appears", T('Cube: face diagonal $a\\sqrt2$ · body diagonal $a\\sqrt3$', size=42, gap=30)),
            "In a cube: the face diagonal is a root 2, the body diagonal a root 3.",
            A("'Box: √(a² + b² + c²)' appears", T('Box: body diagonal $=\\sqrt{a^2+b^2+c^2}$', size=42, gap=30)),
            "In a box: two right triangles, or the root of the three squares. 6, 8, 24 — 26.",
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
            "Three face areas at one corner? Multiply them and take the root. 6, 10, 15 — the volume is 30."]),
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
