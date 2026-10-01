"""Topic 34 - Polygons. Course review 2026-09 fixes.
Adds exterior angles (sum 360, n = 360/(180 - angle)), the diagonal count (n - 3, n(n - 3)/2),
concave polygons, polygons meeting at a point / on a common side, hexagon diagonal facts; rewrites every written
solution in TeX, fixes figures and adds exam-level practice (pass 2: the plan of real_exam/PLAN_REMOVE_RESTORE.md is applied).
See t34_CHANGES.md for the plain-language list."""
import math
import re
from dsl import T, H, A, D, Q
from math_api import VIS

TOPIC = 34
LEARN, PRACTICE = 'geo34-learn-1', 'geo34-core-practice'
MAIN = 'geo-104'
MEET = 'r26-t34-meet'
G = ['q-r26-t34-%02d' % k for k in range(1, 12)]   # 01-03 guided, 04-11 practice

# ------------------------------------------------------------------------------------------------
# Figures - same style as the existing geometry figures (ink #203344, teal #087f83, fill #d5f1ed, DejaVu 20)
# ------------------------------------------------------------------------------------------------
INK, TEAL, FILL = '#203344', '#087f83', '#d5f1ed'


def _svg(label, body, vb='0 0 640 360'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, label, label, body))


def _t(x, y, s, size=20, color=INK):
    return ('<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="middle" fill="%s" '
            'font-family="DejaVu Sans,Arial,sans-serif" font-size="%d">%s</text>' % (x, y, color, size, s))


def _poly(pts, stroke=INK, fill='none'):
    p = ' '.join('%.1f,%.1f' % xy for xy in pts)
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (p, fill, stroke)


def _line(p, q, color=INK, w=2.5, dash=False):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (p[0], p[1], q[0], q[1], color, w, ' stroke-dasharray="7 5"' if dash else ''))


def _arc(c, p1, p2, r=26):
    """Small angle arc at c from the ray c->p1 to the ray c->p2."""
    def unit(p):
        dx, dy = p[0] - c[0], p[1] - c[1]; L = math.hypot(dx, dy); return dx / L, dy / L
    u, v = unit(p1), unit(p2)
    sweep = 1 if u[0] * v[1] - u[1] * v[0] > 0 else 0
    return ('<path d="M %.1f %.1f A %d %d 0 0 %d %.1f %.1f" fill="none" stroke="%s" stroke-width="2"/>'
            % (c[0] + r * u[0], c[1] + r * u[1], r, r, sweep, c[0] + r * v[0], c[1] + r * v[1], TEAL))


def _reg(cx, cy, R, n, start_deg):
    """Regular polygon vertices (screen coords), counterclockwise in math sense starting at start_deg."""
    return [(cx + R * math.cos(math.radians(start_deg + 360.0 * k / n)),
             cy - R * math.sin(math.radians(start_deg + 360.0 * k / n))) for k in range(n)]


def _bbox(svg):
    xs, ys = [], []
    for pts in re.findall(r'points="([^"]+)"', svg):
        for a, b in re.findall(r'(-?[\d.]+),(-?[\d.]+)', pts): xs.append(float(a)); ys.append(float(b))
    for tag in re.findall(r'<line [^>]*>', svg):
        g = {k: float(v) for k, v in re.findall(r'\b(x1|y1|x2|y2)="(-?[\d.]+)"', tag)}
        if len(g) == 4 and 'stroke="none"' not in tag: xs += [g['x1'], g['x2']]; ys += [g['y1'], g['y2']]
    for tag in re.findall(r'<circle [^>]*>', svg):
        g = {k: float(v) for k, v in re.findall(r'\b(cx|cy|r)="(-?[\d.]+)"', tag)}
        xs += [g['cx'] - g['r'], g['cx'] + g['r']]; ys += [g['cy'] - g['r'], g['cy'] + g['r']]
    for tag in re.findall(r'<text [^>]*>', svg):
        g = {k: float(v) for k, v in re.findall(r'\b(x|y)="(-?[\d.]+)"', tag)}
        xs += [g['x'] - 12, g['x'] + 12]; ys += [g['y'] - 12, g['y'] + 12]
    for d in re.findall(r' d="([^"]+)"', svg):
        nums = [float(x) for x in re.findall(r'-?[\d.]+', d)]
        if nums: xs += [nums[0], nums[-2]]; ys += [nums[1], nums[-1]]
    return min(xs), min(ys), max(xs), max(ys)


def _zoom(svg, pad=22):
    """Crop a 640x360 question figure to its drawing, keeping the 16:9 frame (bigger lines and labels on a phone)."""
    if 'viewBox="0 0 640 360"' not in svg: return svg
    x0, y0, x1, y1 = _bbox(svg)
    x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    w, h = x1 - x0, y1 - y0
    if w / h < 16 / 9.0: w = h * 16 / 9.0
    else: h = w * 9 / 16.0
    if w > 600: return svg
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return svg.replace('viewBox="0 0 640 360"', 'viewBox="%.1f %.1f %.1f %.1f"' % (cx - w / 2, cy - h / 2, w, h), 1)


def _crop_tight(svg, pad=30):
    x0, y0, x1, y1 = _bbox(svg)
    return re.sub(r'viewBox="[^"]*"', 'viewBox="%.1f %.1f %.1f %.1f"' % (x0 - pad, y0 - pad, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), svg, count=1)


# --- lesson: exterior angles of a convex pentagon (every side extended past its end vertex) ---
def _fig_exterior():
    P = [(250, 95), (420, 110), (470, 225), (335, 290), (200, 215)]
    b = _poly(P)
    for k in range(5):
        prev, cur, nxt = P[k - 1], P[k], P[(k + 1) % 5]
        dx, dy = cur[0] - prev[0], cur[1] - prev[1]; L = math.hypot(dx, dy)
        ext = (cur[0] + 62 * dx / L, cur[1] + 62 * dy / L)
        b += _line(cur, ext, TEAL, 2.2, dash=True) + _arc(cur, ext, nxt, 24)
    return _crop_tight(_svg('A pentagon with every side extended; the exterior angle at each vertex is marked', b))


# --- lesson: a regular hexagon with a square on its right side ---
HEX = _reg(250, 180, 100, 6, 90)            # top, upper-left, lower-left, bottom, lower-right, upper-right
P_SH = HEX[5]                               # shared top vertex of the right side
SQ = [HEX[5], (HEX[5][0] + 100, HEX[5][1]), (HEX[4][0] + 100, HEX[4][1]), HEX[4]]


def _fig_hex_square():
    b = _poly(HEX) + _poly(SQ, TEAL, FILL) + _arc(P_SH, SQ[1], HEX[0], 28)
    b += _t(P_SH[0] + 13, P_SH[1] - 44, 'x', 18, TEAL)
    return _crop_tight(_svg('A regular hexagon with a square on one side; x is the angle between them at a shared vertex', b))


# --- guided: square ABCD and regular pentagon ABEFG on opposite sides of AB ---
def _fig_sq_pent():
    Ap, Bp = (300, 110), (300, 210)
    Cp, Dp = (200, 210), (200, 110)
    ap = 50 / math.tan(math.radians(36)); R = 50 / math.sin(math.radians(36))
    pent = _reg(300 + ap, 160, R, 5, 144)    # A, B, E, F, G
    Ep, Fp, Gp = pent[2], pent[3], pent[4]
    b = _poly([Ap, Bp, Cp, Dp]) + _poly(pent) + _line(Dp, Gp, TEAL)
    b += (_t(287, 124, 'A') + _t(300, 228, 'B') + _t(186, 224, 'C') + _t(186, 98, 'D') + _t(Ep[0] + 8, Ep[1] + 17, 'E')
          + _t(Fp[0] + 18, Fp[1], 'F') + _t(Gp[0] + 8, Gp[1] - 16, 'G'))
    return _svg('A square and a regular pentagon on a common side AB, with segment DG', b)


# --- practice: regular pentagon ABCDE with equilateral triangle ABF inside ---
def _fig_pent_tri():
    ap = 50 / math.tan(math.radians(36)); R = 50 / math.sin(math.radians(36))
    V = _reg(320, 260 - ap, R, 5, 234)       # A, B, C, D, E
    Fp = (320, 260 - 100 * math.sqrt(3) / 2)
    b = _poly(V) + _line(V[0], Fp, TEAL) + _line(V[1], Fp, TEAL) + _line(V[4], Fp)
    b += (_t(V[0][0] - 12, V[0][1] + 14, 'A') + _t(V[1][0] + 12, V[1][1] + 14, 'B') + _t(V[2][0] + 17, V[2][1], 'C')
          + _t(V[3][0], V[3][1] - 16, 'D') + _t(V[4][0] - 17, V[4][1], 'E') + _t(Fp[0] + 16, Fp[1] - 13, 'F'))
    return _svg('A regular pentagon with an equilateral triangle on side AB, inside the pentagon', b)


# --- practice: regular octagon cut from a square ---
def _fig_oct_square():
    x0, y0, s = 200, 60, 240
    a = s / (1 + math.sqrt(2)); g = a / math.sqrt(2)
    octo = [(x0 + g, y0), (x0 + s - g, y0), (x0 + s, y0 + g), (x0 + s, y0 + s - g), (x0 + s - g, y0 + s), (x0 + g, y0 + s),
            (x0, y0 + s - g), (x0, y0 + g)]
    b = _poly(octo, TEAL, FILL) + _poly([(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s)])
    b += _t(x0 + s / 2, y0 + s + 22, '2+√2')
    return _svg('A square with its four corners cut off to leave a regular octagon', b)


# --- practice: regular hexagon ABCDEF with rectangle ACDF shaded ---
def _fig_hex_rect():
    V = _reg(320, 170, 100, 6, 90)          # A top, B, C, D bottom, E, F
    b = _poly([V[0], V[2], V[3], V[5]], TEAL, FILL) + _poly(V)
    for k, name in enumerate('ABCDEF'):
        dx, dy = V[k][0] - 320, V[k][1] - 170
        b += _t(V[k][0] + 0.2 * dx, V[k][1] + 0.2 * dy, name)
    return _svg('A regular hexagon ABCDEF with the quadrilateral ACDF shaded', b)


FIG_EXT = _fig_exterior()
FIG_HEXSQ = _fig_hex_square()


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


def _replace_say(M, vid, n, old, new):
    """Replace a spoken line; new=None deletes it, a list inserts several lines."""
    def fn(lines):
        out = []; hit = False
        for l in lines:
            if l.get('say') == old:
                hit = True
                if new is None: continue
                if isinstance(new, list):
                    out += [{'say': x} for x in new]; continue
                l = dict(l, say=new)
            out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def _insert_after_say(M, vid, n, anchor, new_lines):
    def fn(lines):
        out = []; hit = False
        for l in lines:
            out.append(l)
            if l.get('say') == anchor:
                hit = True; out += [{'say': x} for x in new_lines]
        assert hit, (vid, n, anchor)
        return out
    M.edit_lines(vid, n, fn)


def _set_item(M, vid, n, old, new, label=None):
    b = M.slide(vid, n)
    for k, it in enumerate(b['items']):
        if it.get('t') == old:
            it['t'] = new
            if label:
                for l in b['lines']:
                    if l.get('appear') == k: l['label'] = label
            M.touched_videos.add(vid); return
    raise KeyError((vid, n, old))


def _sync_stem_copies(M, qids):
    for qid in qids:
        q = M.q(qid)
        for v in M.D['videos'].values():
            if v['topic'] != TOPIC: continue
            for b in v['beats']:
                if (b.get('canvas') or '').startswith('Pre-loaded — question %s ' % qid):
                    b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])


US = [('centre', 'center'), ('Centre', 'Center'), ('practise', 'practice'), ('Practise', 'Practice')]
_DIV = re.compile(r'(\([^()$]*\)|[\d.]+°?)\s?:\s?([\d.]+°?)')


def _text_pass(M):
    """American spelling everywhere in the topic's videos; ':' as division -> fraction (board) or ÷ (labels, notes)."""
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        hit = False
        for b in v['beats']:
            for l in b['lines']:
                for k in ('say', 'draw', 'label'):
                    if k not in l: continue
                    s = l[k]
                    for a, c in US: s = s.replace(a, c)
                    if k != 'say': s = re.sub(r'(\d°?|\))\s?:\s?(\d)', r'\1 ÷ \2', s)
                    if s != l[k]: l[k] = s; hit = True
            for it in b['items']:
                if it.get('t'):
                    s = it['t']
                    for a, c in US: s = s.replace(a, c)
                    s = re.sub(r'\$[^$]*\$', lambda m: _DIV.sub(lambda d: '\\frac{%s}{%s}' % (d.group(1).strip('()'), d.group(2)), m.group(0)), s)
                    if s != it['t']: it['t'] = s; hit = True
        if hit: M.touched_videos.add(v['id'])


def _solution_video(M, qid, vid_title, group, sidebar, intro, slides, pre=None):
    n = M.next_question_number(TOPIC)
    act = sidebar.index('Question %d' % n)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for s in slides:
        beats.append(dict(mode='question', active=act, title=s[0], pre=[dict(x) for x in (pre or [Q(qid)])], script=s[1]))
    v = M.new_video('solve-' + qid, TOPIC, vid_title, sidebar, beats, M.section_of(qid), kind='solution', qid=qid)
    v['beats'][0]['title'] = group
    v['hybrid']['title'] = group
    v['hybrid']['num'] = 64
    return n


# ================================================================================================
def apply(M):
    _lesson_polygons(M)
    _other_videos(M)
    _cards(M)
    _existing_questions(M)
    _new_guided(M)
    _practice(M)
    _figures(M)
    _summary(M)
    _text_pass(M)            # new slides too


# ------------------------------------------------------------------------------------------------
# 1-2. The main lesson: diagonal count, concave polygons, exterior angles, n from an angle
# ------------------------------------------------------------------------------------------------
def _lesson_polygons(M):
    # slide 5 board: pass 2 - the original "5: 540° → 6: 720° → 7: 900° → 8: 1080°" is restored as it was; only the
    # label colons move out of the math (the ':' pass in _text_pass would read them as fractions)
    _set_item(M, MAIN, 5, '$5: 540°\\ \\rightarrow\\ 6: 720°\\ \\rightarrow\\ 7: 900°\\ \\rightarrow\\ 8: 1080°$',
              '5: $540°$ $\\rightarrow$ 6: $720°$ $\\rightarrow$ 7: $900°$ $\\rightarrow$ 8: $1080°$')
    # slide 6: concave polygons (one sentence the review asked for)
    _insert_after_say(M, MAIN, 6, "These two sides are exactly those two sides. But it's no longer a regular hexagon.", [
        "By the way — the folded shape is still a hexagon. Its angle sum is still 720.",
        "One of its angles now points inward, so it is bigger than 180. The formula 180 times n minus 2 still works."])

    # after slide 10 (Three to know): exterior angles + the reverse question
    ext = dict(title='Exterior angles', mode='concept', pre=[VIS(FIG_EXT, w=1000, h=520)], script=[
        "One more angle to know: the exterior angle.",
        "Here every side is extended past its vertex.",
        "The angle between the extension and the next side — that's the exterior angle.",
        "The polygon's angle and the exterior angle sit on one straight line. Together — 180.",
        A('Exterior angle = 180° − angle appears', T('Exterior angle $=180°-$ angle', size=36, x=410, y=650)),
        "Now the big fact. Take one exterior angle at every vertex and add them up. You always get 360.",
        "Why? Walk around the polygon. At every vertex you turn by the exterior angle.",
        "After one full walk you face the same way again. You turned one full circle — 360.",
        A('All exterior angles: 360° appears', T('All exterior angles together: $360°$', size=36, x=410, y=725)),
        "It doesn't matter how many sides. A triangle, a pentagon, twenty sides — always 360.",
        "In a regular polygon all the exterior angles are equal. So each one is 360 over n.",
        A('Regular: each exterior angle = 360°/n = central angle appears',
          T('Regular: each one $=\\frac{360°}{n}=$ central angle', size=36, x=410, y=805)),
        "Look — that's the central angle again. That's why the tip works: central angle plus the polygon's angle is 180.",
    ])
    rev = dict(title='Angle → sides', mode='concept', pre=[], script=[
        "Now the reverse question. Each angle of a regular polygon is 150. How many sides?",
        "You could solve 180 minus 360 over n equals 150. It works — but it's slow.",
        "The fast way: go to the exterior angle. 180 minus 150 — 30.",
        "Each exterior angle is 30, and together they make 360. 360 over 30 — 12 sides.",
        A('n = 360° / (180° − angle) appears', T('$n=\\frac{360°}{180°-\\text{angle}}$', size=48)),
        A('150°: 180 − 150 = 30, 360/30 = 12 sides appears',
          T('$150°$: $180-150=30$, $\\frac{360}{30}=12$ sides', size=40)),
    ])
    M.insert_slides(MAIN, 10, [ext, rev])

    # after slide 4 (Split into triangles): how many diagonals
    fig7 = M.slide(MAIN, 4)['items'][0]['v']['svg']
    diag = dict(title='How many diagonals', mode='concept', pre=[VIS(fig7, w=1000, h=520)], script=[
        "How many diagonals can we draw? Look at vertex A again.",
        "A diagonal joins two vertices that are not neighbors.",
        "From A, I can't draw to A itself. And I can't draw to its two neighbors, B and G — those are sides.",
        "So from one vertex: n minus 3 diagonals. Here 7 minus 3 — 4.",
        A('From one vertex: n − 3 diagonals → n − 2 triangles appears',
          T('From one vertex: $n-3$ diagonals $\\rightarrow$ $n-2$ triangles', size=34, x=410, y=650)),
        "And these 4 diagonals cut the heptagon into 5 triangles — n minus 2, just like before.",
        "Now all the diagonals of the polygon. Every vertex sends n minus 3. So n times n minus 3.",
        "But each diagonal has two ends — we counted it twice, once from each end. So divide by 2.",
        A('All diagonals: n(n − 3)/2 appears', T('All the diagonals: $\\frac{n(n-3)}{2}$', size=36, x=410, y=725)),
        "Heptagon: 7 times 4 is 28. Over 2 — 14 diagonals.",
        A('Heptagon: 7 · 4 / 2 = 14 appears', T('Heptagon: $\\frac{7\\cdot4}{2}=14$', size=36, x=410, y=805)),
    ])
    M.insert_slides(MAIN, 4, [diag])

    sb = ['Names', 'Angle sum', 'Split into triangles', 'How many diagonals', '+1 side = +180°', 'Regular', 'On a circle',
          'One angle', 'The formula sheet', 'Three to know', 'Exterior angles', 'Angle → sides', 'Diagonals: equal parts',
          'Isosceles triangles', 'The hexagon', 'Recap']
    M.set_sidebar(MAIN, sb)
    for b in M.video(MAIN)['beats']:
        if b['mode'] != 'title': b['active'] = sb.index(b['title'])

    # recap: add the two new rules
    n = len(M.video(MAIN)['beats'])
    assert M.slide(MAIN, n)['title'] == 'Recap'
    sc = _script_of(M, MAIN, n)
    k = sc.index("The regular hexagon is the special case: equilateral triangles, not just isosceles.") + 1
    sc[k:k] = [
        A('Diagonals: n − 3 from one vertex · n(n − 3)/2 in all appears',
          T('Diagonals: $n-3$ from one vertex · $\\frac{n(n-3)}{2}$ in all', size=36)),
        "Diagonals: n minus 3 from one vertex, n times n minus 3 over 2 in all.",
        A('Exterior angles: 360° · regular: n = 360°/(180° − angle) appears',
          T('Exterior angles: $360°$ in all · regular: $n=\\frac{360°}{180°-\\text{angle}}$', size=36)),
        "And the exterior angles always add up to 360. Know an angle of a regular polygon? 180 minus it, then 360 over that — the number of sides.",
    ]
    M.set_slide(MAIN, n, script=sc)


# ------------------------------------------------------------------------------------------------
# 3. Other existing videos
# ------------------------------------------------------------------------------------------------
def _other_videos(M):
    # Two Hexagon Partitions: explain "Haman's ear" for English learners
    # pass 2: the original line stays; one explaining line is added after it
    _insert_after_say(M, 'geo-112-after', 4,
                      "We call it the Haman's-ear partition: fold the three corners in, like the paper, and you get a hamantasch.",
                      ["A hamantasch — a Haman's ear — is a cookie with three corners. That's why we also call it the star partition."])

    # Q6: state the hexagon diagonal facts once
    _insert_after_say(M, 'solve-geo34-g112', 3, "Choice four. That's the math solution.", [
        "Remember this for later: in a regular hexagon, the short diagonal is the side times root 3. Here: 10 over root 3, times root 3 — 10.",
        "And the long diagonal, through the center, is twice the side."])

    # Q9: drop "measure with your fingers" - keep the real reason
    vid = 'solve-geo34-g114'
    M.set_slide(vid, 4, script=[
        "Way two: estimate — and know the octagon.",
        D('Mark AE and the bottom corner leg of BE'),
        "Lina compares 2AE with BE. One AE is the same as the bottom leg on BE — the silver-triangle legs are equal.",
        "Cancel them. What's left? One AE — against the square's side.",
        "Which is bigger? The square's side is an octagon side — the hypotenuse of a corner triangle. AE is only a leg.",
        A('Square side = hypotenuse > leg AE appears', T('Square side $=$ hypotenuse $>$ leg $AE$', size=34, x=1060, y=340, w=470)),
        "In a right triangle the hypotenuse is always the longest side. So BE is more than 2AE.",
        "Lina is right.",
        "Noam: here we just need to know which piece cancels which.",
        "CE is on both sides — cancel it. AE is the same as the leg on the left of CD. AC is an octagon side — the same as the middle of CD.",
        D('Circle choice 4'),
        "Everything cancels — Noam is right too. Choice four.",
    ])


# ------------------------------------------------------------------------------------------------
# memory cards
# ------------------------------------------------------------------------------------------------
def _cards(M):
    c = M.card('mem-polygons')
    rows = c['tables'][0]['rows']
    rows[3:3] = [['!Exterior angles', '$360°$ in all (any convex polygon)', 'regular: each $\\frac{360°}{n}$ = central angle'],
                 ['!Sides from one angle (regular)', '$n=\\frac{360°}{180°-\\text{angle}}$', '$150°$: $\\frac{360}{30}=12$ sides']]
    rows.insert(1, ['Diagonals', '$n-3$ from one vertex · $\\frac{n(n-3)}{2}$ in all', 'each diagonal has 2 ends'])
    c['tips'] += ['A concave polygon (one angle bigger than $180°$) still has the angle sum $180°(n-2)$.']

    h = M.card('mem-hexagon-partitions')
    h['tables'][1]['rows'][2][0] = "Haman's ear (star)"
    h['tables'].insert(1, {'title': 'Regular hexagon, side $a$', 'head': ['Length / area', 'Value'], 'rows': [
        ['Radius', '$a$'], ['!Short diagonal (e.g. $AC$)', '$a\\sqrt3$'], ['!Long diagonal (through the center)', '$2a$'],
        ['!Area', '$6\\cdot\\frac{a^2\\sqrt3}{4}=\\frac{3\\sqrt3}{2}a^2$'],
        ['Triangle $ACE$', '$\\frac12$ of the hexagon'], ['Rectangle $ACDF$', '$\\frac23$ of the hexagon']]})


# ------------------------------------------------------------------------------------------------
# 3. Existing questions: every written solution in TeX with the numbers; stems; p12 method
# ------------------------------------------------------------------------------------------------
EXPL = {
    'geo34-g106': ["Draw $AD$. Triangle $AED$ has a right angle at $E$ and legs $12$ and $5$. Its area is $\\frac{12\\cdot5}{2}=30$, and $AD=13$ (the 5-12-13 triple).",
                   "Drop the height $AH$ to $CD$. $ABCH$ is a square with side $12$. Its area is $12^2=144$.",
                   "Triangle $AHD$ has hypotenuse $AD=13$ and leg $AH=12$, so $DH=5$. Its area is $\\frac{12\\cdot5}{2}=30$.",
                   "Total: $144+30+30=204$."],
    'geo34-g107': ["The three long diagonals split the hexagon into 6 equilateral triangles with side $8$.",
                   "One triangle: $\\frac{8^2\\sqrt3}{4}=\\frac{64\\sqrt3}{4}=16\\sqrt3$.",
                   "Six triangles: $6\\cdot16\\sqrt3=96\\sqrt3$."],
    'geo34-g108': ["Split the octagon: a square in the middle, 4 rectangles and 4 corner right isosceles triangles.",
                   "Square: $5^2=25$.",
                   "Each corner triangle has hypotenuse $5$, so its legs are $\\frac{5}{\\sqrt2}$. Its area is $\\frac12\\cdot\\frac{5}{\\sqrt2}\\cdot\\frac{5}{\\sqrt2}=\\frac{25}{4}$. Four triangles: $25$.",
                   "Each rectangle: $5\\cdot\\frac{5}{\\sqrt2}=\\frac{25\\sqrt2}{2}$. Four rectangles: $50\\sqrt2$.",
                   "Total: $25+25+50\\sqrt2=50+50\\sqrt2$."],
    'geo34-g110': ["Each angle of a regular pentagon is $\\frac{540°}{5}=108°$.",
                   "Triangle $BCD$ is isosceles ($CB=CD$) with vertex angle $108°$, so $\\angle BDC=\\frac{180°-108°}{2}=36°$. In the same way, $\\angle EDA=36°$.",
                   "$x=\\angle ADB=108°-36°-36°=36°$."],
    'geo34-g111': ["Statement 3 is true: every central angle is $\\frac{360°}{8}=45°$.",
                   "Statement 4 is true: each arc is longer than its chord (the side), so the circumference is greater than the perimeter.",
                   "Statement 1 is true: triangles $OBC$ and $OCD$ have three pairs of equal sides, so they are congruent and $\\angle BCO=\\angle OCD$.",
                   "Statement 2 is false: triangle $OCD$ has the angles $45°$, $67.5°$ and $67.5°$. The side $CD$ faces $45°$ and a radius faces $67.5°$, so $CD<r$ and the perimeter is less than $8r$."],
    'geo34-g112': ["The three corner triangles are congruent, so triangle $ACE$ is equilateral: $AC=\\frac{30}{3}=10$.",
                   "Triangle $ABC$ is isosceles with vertex angle $120°$. The height from $B$ splits $AC$ into $5$ and $5$ and makes two 30-60-90 triangles.",
                   "In each one the long leg is $5$, so the short leg is $\\frac{5}{\\sqrt3}$ and the hypotenuse is $AB=\\frac{10}{\\sqrt3}$.",
                   "Perimeter: $6\\cdot\\frac{10}{\\sqrt3}=\\frac{60}{\\sqrt3}=20\\sqrt3$."],
    'geo34-g112-area': ["Each corner triangle ($ABC$, $CDE$, $EFA$) is $\\frac16$ of the hexagon: the same area as an equilateral triangle with side $6$, $\\frac{6^2\\sqrt3}{4}=9\\sqrt3$.",
                        "Three triangles: $3\\cdot9\\sqrt3=27\\sqrt3$ (half of the hexagon, $54\\sqrt3$)."],
    'geo34-g113': ["Plug in a number: side $=2$.",
                   "Maya: the four squares have perimeter $4\\cdot8=32$. The hexagon has perimeter $6\\cdot2=12$, and $3\\cdot12=36\\ne32$. Maya is wrong.",
                   "Daniel: the four squares have area $4\\cdot4=16$. The hexagon has area $6\\cdot\\frac{2^2\\sqrt3}{4}=6\\sqrt3<6\\cdot2=12<16$. Daniel is right.",
                   "Only Daniel is correct."],
    'geo34-g114': ["Let $AE=CE=1$. Triangle $ACE$ is right isosceles, so $AC=\\sqrt2$. All the octagon sides are $\\sqrt2$.",
                   "Lina: $BE=\\sqrt2+1\\approx2.4$ and $2AE=2$. $BE>2AE$, so Lina is correct.",
                   "Noam: the perimeter of $ACE$ is $1+1+\\sqrt2=2+\\sqrt2$, and $CD=1+\\sqrt2+1=2+\\sqrt2$. They are equal, so Noam is correct.",
                   "Both are correct."],
    'geo34-g115': ["Split the octagon the standard way: a middle square, 4 congruent rectangles and 4 corner triangles. The 4 triangles together equal the middle square.",
                   "White: the middle square $+$ 2 rectangles.",
                   "Shaded: 4 triangles $+$ 2 rectangles $=$ (the middle square) $+$ 2 rectangles.",
                   "The shaded area equals the white area: $8+8\\sqrt2$."],
    'geo34-g116': ["$180(n-2)=1620$. Divide by $180$: $n-2=9$, so $n=11$.",
                   "Or use an anchor: the octagon has $1080°$. Each extra side adds $180°$: $1260°$ (9 sides), $1440°$ (10 sides), $1620°$ (11 sides)."],
    'geo34-g117': ["$B-A=180(17-2)-180(12-2)=180(15-10)=5\\cdot180=900°$.",
                   "$180°(n-2)=900°$ gives $n-2=5$, so $n=7$: a heptagon.",
                   "Faster: 17 sides is 5 sides more than 12, and each side adds $180°$: $5\\cdot180°=900°$."],
    'geo34-core-p01': ["Each hexagon angle is $120°$, so the angle next to it on line $CD$ is $180°-120°=60°$.",
                       "Triangles $GBC$ and $HED$ have two $60°$ angles, so they are equilateral with side $3$.",
                       "$AG=3+3=6$, $FH=6$, $GH=3+3+3=9$ and $AF=3$.",
                       "Perimeter: $6+9+6+3=24$."],
    'geo34-core-p02': ["Along $AB$: the left hexagon gives a long diagonal, $2\\cdot2.4=4.8$. Then comes one side, $2.4$. Then the right hexagon gives another long diagonal, $4.8$.",
                       "$AB=4.8+2.4+4.8=12$."],
    'geo34-core-p04': ["Each octagon has 8 sides. It shares 1 side with the square opening and 1 side with each of its two neighbors, so 5 of its sides are on the outer boundary.",
                       "Outer boundary: $4\\cdot5=20$ sides. The four perimeters: $4\\cdot8=32$ sides.",
                       "The ratio is $\\frac{20}{32}=\\frac58$."],
    'geo34-core-p05': ["$BE=4$ is the hypotenuse of the right isosceles triangle $ABE$, so $AB=AE=\\frac{4}{\\sqrt2}=2\\sqrt2$.",
                       "The boundary has three square sides and two roof sides: $3\\cdot4+2\\cdot2\\sqrt2=12+4\\sqrt2$."],
    'geo34-core-p06': ["Each angle of a regular octagon is $180°-\\frac{360°}{8}=135°$.",
                       "Triangle $ABC$ is isosceles ($AB=BC$) with vertex angle $135°$, so $\\alpha=\\angle BAC=\\frac{180°-135°}{2}=22.5°$."],
    'geo34-core-p07': ["$C$ and $F$ are opposite vertices, so $CF$ is a long diagonal. It passes through the center.",
                       "The hexagon is made of 6 equilateral triangles, so the radius equals the side, $7$. $CF=2\\cdot7=14$."],
    'geo34-core-p08': ["Two heptagons have $2\\cdot7=14$ sides. The shared side is inside the shape, so it is counted in neither boundary: the outer boundary has $14-2=12$ equal sides.",
                       "Each side: $\\frac{84}{12}=7$ cm. One heptagon: $7\\cdot7=49$ cm."],
    'geo34-core-p09': ["$\\alpha$ is an angle of the octagon: $\\alpha=180°-\\frac{360°}{8}=135°$.",
                       "Quadrilateral $ABGH$ is an isosceles trapezoid: $AH\\parallel BG$ and the legs $AB$ and $HG$ are octagon sides. Its angles at $A$ and $H$ are octagon angles, $135°$.",
                       "So $\\beta=\\angle ABG=180°-135°=45°$.",
                       "$\\alpha-\\beta=135°-45°=90°$."],
    'geo34-core-p10': ["The octagon angle is $135°$, so at each vertex $\\frac{135}{360}=\\frac38$ of the disk is inside the octagon and $\\frac58$ is outside.",
                       "Each disk: $\\pi\\cdot2^2=4\\pi$. The part outside: $\\frac58\\cdot4\\pi=\\frac52\\pi$.",
                       "Eight disks: $8\\cdot\\frac52\\pi=20\\pi$."],
    'geo34-core-p11': ["A parallelogram has only 2 diagonals, and they cross at their common midpoint, inside the shape. So all its diagonals meet at one point.",
                       "A regular pentagon has $\\frac{5\\cdot2}{2}=5$ diagonals, and they do not all pass through one point. The same is true for the heptagon and the decagon (only the long diagonals of the decagon meet at the center)."],
    'geo34-core-p12': ["$\\angle TAF$ is next to the hexagon angle $\\angle BAF=120°$ on line $BT$, so $\\angle TAF=180°-120°=60°$.",
                       "Let $O$ be the center. A radius is perpendicular to the tangent: $\\angle OFT=90°$.",
                       "Triangle $OAF$ is equilateral (in a regular hexagon the side equals the radius), so $\\angle OFA=60°$ and $\\angle AFT=90°-60°=30°$.",
                       "In triangle $ATF$: $\\angle ATF=180°-60°-30°=90°$."],
    'geo34-core-p13': ["The 6 equal angles at the common vertex fill $360°$, so each is $\\frac{360°}{6}=60°$.",
                       "Each rhombus side is $\\frac{20}{4}=5$.",
                       "Each rhombus is made of two triangles with two sides $5$ and a $60°$ angle between them: equilateral triangles. So its short diagonal (a side of the inner hexagon) is $5$.",
                       "Perimeter: $6\\cdot5=30$."],
    'geo34-core-p15': ["The decagon angle is $180°-\\frac{360°}{10}=144°$.",
                       "Each central triangle has head angle $\\frac{360°}{10}=36°$ and base angles $\\frac{180°-36°}{2}=72°$. The attached triangle is congruent, so its angle at the marked vertex is $72°$.",
                       "Around the vertex: $\\alpha=360°-144°-72°=144°$."],
    'geo34-core-p16': ["Draw the height from $A$ to $BE$. It splits triangle $ABE$ into two 30-60-90 triangles with hypotenuse $4a$.",
                       "The height (short leg) is $2a$. Half of $BE$ (long leg) is $2a\\sqrt3$, so $BE=4a\\sqrt3$.",
                       "Triangle: $\\frac{4a\\sqrt3\\cdot2a}{2}=4\\sqrt3\\,a^2$. Rectangle: $4a\\sqrt3\\cdot a=4\\sqrt3\\,a^2$.",
                       "Total: $8\\sqrt3\\,a^2$."],
    'geo34-core-p17': ["Square: $3^2=9$.",
                       "Each rectangle has sides $3$ and $\\frac{3}{\\sqrt2}$, so its area is $\\frac{9}{\\sqrt2}=\\frac{9\\sqrt2}{2}$. Four rectangles: $18\\sqrt2$.",
                       "Shaded: $9+18\\sqrt2$."],
    'geo34-core-p18': ["$P$: $180°(n+1-2)=180°(n-1)$. $Q$: $180°(m+3-2)=180°(m+1)$.",
                       "Difference: $180°\\big((n-1)-(m+1)\\big)=180°(n-m-2)$.",
                       "Faster: $P$ has $(n+1)-(m+3)=n-m-2$ more sides, and each side adds $180°$."],
    'geo34-core-p19': ["Let the large radius be $R$. Take a short diagonal, like $BF$. Triangle $OBF$ is isosceles with $OB=OF=R$ and $\\angle BOF=2\\cdot60°=120°$.",
                       "The perpendicular from $O$ to $BF$ splits it into two 30-60-90 triangles with hypotenuse $R$. The small radius is the short leg: $\\frac{R}{2}$.",
                       "The radii are in the ratio $2:1$, so the areas are in the ratio $2^2:1^2=4:1$."],
    'geo34-core-p20': ["Each side cuts off one region between the side and the circle: $n$ regions. The inside of the polygon is one more region.",
                       "$n+1=10$, so $n=9$."],
    'geo34-core-p21': ["Exterior angle: $180°-150°=30°$.",
                       "The exterior angles add up to $360°$: $n=\\frac{360°}{30°}=12$."],
    'geo34-core-p22': ["Let the exterior angle be $x$. The interior angle is $4x$, and together they make $180°$: $5x=180°$, so $x=36°$.",
                       "$n=\\frac{360°}{36°}=10$."],
    'geo34-core-p23': ["From one vertex there are $n-3$ diagonals (not to the vertex itself and not to its two neighbors). $n-3=9$, so $n=12$.",
                       "Perimeter: $12\\cdot3=36$ cm."],
    'geo34-core-p24': ["A regular hexagon with side $s$ is 6 equilateral triangles: its area is $6\\cdot\\frac{s^2\\sqrt3}{4}$.",
                       "$6\\cdot\\frac{s^2\\sqrt3}{4}=150\\sqrt3$ gives $\\frac{s^2}{4}=25$, so $s^2=100$ and $s=10$.",
                       "Perimeter: $6\\cdot10=60$."],
    'geo34-core-p25': ["The four corner triangles together equal the middle square, and its side is the octagon side $s$. So $s^2=49$ and $s=7$.",
                       "Perimeter: $8\\cdot7=56$."],
    'geo34-core-p26': ["Dodecagon (12 sides): $180°-\\frac{360°}{12}=180°-30°=150°$.",
                       "Octagon: $180°-\\frac{360°}{8}=180°-45°=135°$.",
                       "Difference: $150°-135°=15°$. (Or with exterior angles: $45°-30°=15°$.)"],
    'geo34-core-p27': ["Each corner triangle is $\\frac16$ of the hexagon, so the three corner triangles together are $\\frac12$ of it.",
                       "The triangle in the middle is the other half: $\\frac{96}{2}=48$."],
}


def _existing_questions(M):
    for qid, ex in EXPL.items(): M.set_q(qid, expl=ex)
    M.set_q('geo34-g110', stem='ABCDE is a regular pentagon. What is the size of angle ADB (marked $x$ in the figure)?')
    M.set_q('geo34-core-p06', stem='ABCDEFGH is a regular octagon. What is the size of angle BAC (marked $\\alpha$ in the figure)?')
    M.set_q('geo34-core-p22', stem='Each interior angle of a regular polygon is 4 times its exterior angle. How many sides does the polygon have?')
    M.set_q('geo34-g117', stem='A is the sum of the interior angles of a 12-sided polygon, and B is the sum of the interior angles of a 17-sided polygon. The difference $B-A$ equals the sum of the interior angles of which polygon?')
    M.set_q('geo34-core-p18', stem='Polygon P has $n+1$ sides and polygon Q has $m+3$ sides. m and n are whole numbers, $m\\ge3$ and $n>m+2$. By how much is the interior-angle sum of P greater than that of Q?')
    M.set_q('geo34-g106', stem='In pentagon ABCDE, angles B, C and E are right angles, and AB is parallel to CD. Given:\n$\\begin{cases} AB=BC=AE=12 \\text{ cm} \\\\ DE=5 \\text{ cm} \\end{cases}$\nWhat is the area of the pentagon (in cm²)?')
    M.set_q('geo34-core-p09', stem='ABCDEFGH is a regular octagon. Given:\n$\\begin{cases} \\alpha=\\angle DEF \\\\ \\beta=\\angle ABG \\end{cases}$\nWhat is $\\alpha-\\beta$?')
    M.set_q('geo34-core-p16', stem='Pentagon ABCDE consists of rectangle BCDE and isosceles triangle ABE. Given:\n$\\begin{cases} AB=AE=4a \\\\ BC=a \\\\ \\angle BAE=120° \\end{cases}$\nWhat is the area of the pentagon?')
    _sync_stem_copies(M, ['geo34-g110', 'geo34-g117', 'geo34-g106'])


# ------------------------------------------------------------------------------------------------
# 2. New guided questions (Q13-Q15) and the "meeting at a point" lesson
# ------------------------------------------------------------------------------------------------
def _new_guided(M):
    GRP = 'Advanced Polygons III'
    SB = ['Question 13', 'Question 14']

    # Q13: from one angle to the number of sides
    q = G[0]
    M.new_q(q, TOPIC, 'Each interior angle of a regular polygon is $160°$. How many sides does the polygon have?',
            ['$9$', '$16$', '$18$', '$20$'], 3,
            ["Exterior angle: $180°-160°=20°$.",
             "The exterior angles add up to $360°$, so $n=\\frac{360°}{20°}=18$.",
             "Check: $180°-\\frac{360°}{18}=180°-20°=160°$."])
    M.place_q(q, LEARN, after='solve-geo34-g117')
    n13 = M.next_question_number(TOPIC)
    _solution_video(M, q, 'From one angle to the number of sides', GRP, ['Question %d' % n13, 'Question %d' % (n13 + 1)], [
        "A sample question — medium level.",
        "We know one angle — and we need the number of sides. Two ways."], [
        ('The formula way', [
            "Each interior angle of a regular polygon is 160. How many sides?",
            "The formula way: one angle is 180 minus 360 over n.",
            A('180° − 360°/n = 160° appears', T('$180°-\\frac{360°}{n}=160°$', size=34, x=410, y=300, w=1100)),
            "So 360 over n is 20.",
            A('360°/n = 20° → n = 18 appears', T('$\\frac{360°}{n}=20°\\ \\Rightarrow\\ n=18$', size=34, x=410, y=380, w=1100)),
            "n is 360 over 20 — 18.",
            D('Circle choice 3'),
            "Choice three."]),
        ('The fast way', [
            "Now the fast way — through the exterior angle.",
            "The angle and the exterior angle make 180. So the exterior angle is 180 minus 160 — 20.",
            A('180° − 160° = 20° appears', T('$180°-160°=20°$', size=34, x=410, y=300, w=1100)),
            "All the exterior angles together make 360. Each one is 20. How many fit? 360 over 20 — 18.",
            A('n = 360°/20° = 18 appears', T('$n=\\frac{360°}{20°}=18$', size=34, x=410, y=380, w=1100)),
            D('Cross out choice 1'),
            "9? That's 180 over 20 — someone used 180 instead of 360. The full turn is 360.",
            "Choice three. Two short lines — no equation."]),
    ])

    # Q14: counting diagonals
    q = G[1]
    M.new_q(q, TOPIC, 'From one vertex of a polygon, exactly 7 diagonals can be drawn. How many diagonals does the polygon have in all?',
            ['$28$', '$35$', '$45$', '$70$'], 2,
            ["From one vertex there are $n-3$ diagonals (not to the vertex itself and not to its two neighbors). $n-3=7$, so $n=10$.",
             "Each of the 10 vertices sends 7 diagonals: $10\\cdot7=70$. Each diagonal has two ends, so it was counted twice.",
             "In all: $\\frac{10\\cdot7}{2}=35$."])
    M.place_q(q, LEARN, after='solve-' + G[0])
    _solution_video(M, q, 'Counting the diagonals of a polygon', GRP, ['Question %d' % n13, 'Question %d' % (n13 + 1)], [
        "A sample question — medium level.",
        "Diagonals: count them without drawing them."], [
        ('Find n', [
            "From one vertex, 7 diagonals. How many diagonals in all?",
            "First — how many sides? From one vertex we draw n minus 3 diagonals: not to itself, not to its two neighbors.",
            A('n − 3 = 7 → n = 10 appears', T('$n-3=7\\ \\Rightarrow\\ n=10$', size=34, x=410, y=300, w=1100)),
            "n minus 3 is 7, so n is 10. A decagon."]),
        ('Count, then halve', [
            "Every vertex sends 7 diagonals. 10 vertices — 10 times 7, 70.",
            A('10 · 7 = 70 appears', T('$10\\cdot7=70$', size=34, x=410, y=300, w=1100)),
            D('Cross out choice 4'),
            "But 70 is a trap. Each diagonal has two ends — we counted it twice.",
            A('10 · 7 / 2 = 35 appears', T('$\\frac{10\\cdot7}{2}=35$', size=34, x=410, y=380, w=1100)),
            "70 over 2 — 35.",
            D('Circle choice 2'),
            "Choice two.",
            "And 45? That's 10 times 9 over 2 — it counts the 10 sides too. Sides are not diagonals."]),
    ])

    # lesson: polygons meeting at a point
    fig = VIS(FIG_HEXSQ, w=1000, h=520)
    msb = ['Around a point', 'Find the triangle', 'Recap']
    M.new_video(MEET, TOPIC, 'Polygons Meeting at a Point', msb, [
        dict(mode='title', title='Polygons Meeting at a Point', script=[
            "Polygons meeting at a point.",
            "Two regular polygons on a common side — the exam loves this picture."]),
        dict(mode='concept', active=0, title='Around a point', pre=[fig], script=[
            "Here's a regular hexagon, and a square built on one of its sides, outside.",
            "Look at the vertex they share. Three angles sit around it: the hexagon's angle, the square's angle, and the gap x.",
            "Around a point, the angles add up to 360.",
            D('Write 120° in the hexagon and 90° in the square at the shared vertex'),
            "The hexagon's angle — 120. The square's — 90.",
            A('x = 360° − 120° − 90° = 150° appears', T('$x=360°-120°-90°=150°$', size=40, x=410, y=650)),
            "So x is 360 minus 120 minus 90 — 150."]),
        dict(mode='concept', active=1, title='Find the triangle', pre=[fig], script=[
            "The exam usually goes one step further. Close the gap into a triangle.",
            D('Connect the two free ends with a dashed line'),
            "The two sides of angle x: one is a side of the square, one is a side of the hexagon.",
            "Both are equal to the common side. So the triangle is isosceles.",
            A('Both sides of x = the common side appears', T('Both sides of $x$ $=$ the common side', size=36, x=410, y=650)),
            "Its head angle is 150. The two base angles share what's left: 30. Each one — 15.",
            A('(180° − 150°)/2 = 15° appears', T('Base angles: $\\frac{180°-150°}{2}=15°$', size=36, x=410, y=730)),
            "That's the whole method: first 360 around the point — then look for the isosceles triangle."]),
        dict(mode='concept', active=2, title='Recap', pre=[], script=[
            "Let's sum up.",
            A('Around a point: 360° appears', T('Around a point: $360°$', size=40)),
            "All the angles around one point add up to 360.",
            A('Common side → equal sides → isosceles triangle appears',
              T('Regular polygons on a common side: all sides equal $\\rightarrow$ isosceles triangle', size=36)),
            "Two regular polygons on a common side: all their sides are equal. Look for an isosceles triangle.",
            A('Polygons filling a point: angles add up to 360° appears',
              T('Polygons that fill a point: their angles add up to $360°$', size=36)),
            "And when regular polygons fill the space around a point with no gaps, their angles add up to exactly 360.",
            "Three regular hexagons: 3 times 120 — 360. That's a honeycomb."]),
    ], LEARN, after='solve-' + G[1])
    M.video(MEET)['hybrid']['num'] = 64

    M.new_card('mem-r26-t34-meet', TOPIC, LEARN, {
        'title': 'Polygons meeting at a point', 'intro': 'Two steps: 360° around the point, then the isosceles triangle.',
        'tables': [{'title': '', 'head': ['Situation', 'Rule'], 'rows': [
            ['!Angles around a point', 'add up to $360°$'],
            ['!Two regular polygons on a common side', 'the gap $=360°-$ (the two polygon angles)'],
            ['Their free sides at the shared vertex', 'both equal the common side $\\rightarrow$ isosceles triangle'],
            ['Regular polygons filling a point', 'their angles add up to exactly $360°$']]}],
        'tips': ['Know the angles: triangle $60°$, square $90°$, pentagon $108°$, hexagon $120°$, octagon $135°$.',
                 'Square + pentagon on a common side: gap $360°-90°-108°=162°$.']}, after=MEET)

    # Q15: square + pentagon on a common side
    q = G[2]
    M.new_q(q, TOPIC, 'Square ABCD and regular pentagon ABEFG share the side AB. They lie on opposite sides of AB, as shown in the figure. What is the size of angle ADG?',
            ['$18°$', '$9°$', '$81°$', '$36°$'], 2,
            ["At $A$ three angles fill the full turn: the square's $90°$, the pentagon's $108°$ and $\\angle DAG$.",
             "$\\angle DAG=360°-90°-108°=162°$.",
             "$AD=AB$ (square) and $AG=AB$ (pentagon), so $AD=AG$: triangle $ADG$ is isosceles.",
             "$\\angle ADG=\\frac{180°-162°}{2}=9°$."], figure=_zoom(_fig_sq_pent()))
    M.place_q(q, LEARN, after='mem-r26-t34-meet')
    n15 = M.next_question_number(TOPIC)
    _solution_video(M, q, 'A square and a pentagon on a common side', GRP, ['Question %d' % n15], [
        "A sample question — medium-plus.",
        "A square and a pentagon on a common side — the picture from the lesson."], [
        ('Around point A', [
            "Square ABCD and regular pentagon ABEFG share side AB. What is angle ADG?",
            "Start at the shared vertex, A. Three angles sit around it.",
            D('Write 90° and 108° at A'),
            "The square's angle — 90. The pentagon's angle — 108. Know it by heart.",
            "Around a point: 360. So angle DAG is 360 minus 90 minus 108 — 162.",
            A('∠DAG = 360° − 90° − 108° = 162° appears', T('$\\angle DAG=360°-90°-108°=162°$', size=30, x=1060, y=250, w=470))]),
        ('The isosceles triangle', [
            "Now triangle ADG. AD is a side of the square. AG is a side of the pentagon.",
            "Both are equal to the common side AB. So AD equals AG — the triangle is isosceles.",
            D('Mark AD and AG as equal'),
            "The head angle is 162. What's left for the two base angles: 18. Each one — 9.",
            A('∠ADG = (180° − 162°)/2 = 9° appears', T('$\\angle ADG=\\frac{180°-162°}{2}=9°$', size=30, x=1060, y=250, w=470)),
            D('Circle choice 2'),
            "Choice two.",
            D('Cross out choice 1'),
            "18? That's both base angles together. Don't forget to divide by 2."]),
    ], pre=[Q(q, fig={'type': 'geometry', 'svg': _crop_tight(_fig_sq_pent())}, figw=0.56, figalign='left')])
    for qid in G[:3]:
        v = M.video('solve-' + qid); v['navLabel'] = v['title']


# ------------------------------------------------------------------------------------------------
# 5. Practice: remove duplicates, add new items, order easy -> hard
# ------------------------------------------------------------------------------------------------
def _practice(M):
    # pass 2: p03 and p14 are original questions - they stay (restored, solutions in TeX)
    M.set_q('geo34-core-p03', expl=['$180°(n-2)=900°$, so $n-2=\\frac{900}{180}=5$ and $n=7$: a heptagon.'])
    M.set_q('geo34-core-p14', expl=['$180°(n-2)=1{,}980°$, so $n-2=\\frac{1980}{180}=11$ and $n=13$.'])
    new = [
        (G[3], 'What is the size of each interior angle of a regular decagon (a 10-sided polygon)?',
         ['$108°$', '$144°$', '$150°$', '$162°$'], 2,
         ["Central angle (the same as the exterior angle): $\\frac{360°}{10}=36°$.",
          "One angle: $180°-36°=144°$.",
          "Or with the formula: $\\frac{180°(10-2)}{10}=\\frac{1440°}{10}=144°$."], None),
        (G[4], 'Each exterior angle of a regular polygon is $24°$. What is the sum of its interior angles?',
         ['$2160°$', '$2340°$', '$2520°$', '$2700°$'], 2,
         ["$n=\\frac{360°}{24°}=15$ sides.",
          "Angle sum: $180°(15-2)=180°\\cdot13=2340°$."], None),
        (G[6], 'A polygon has 20 diagonals. How many sides does it have?',
         ['$5$', '$7$', '$8$', '$10$'], 3,
         ["Number of diagonals: $\\frac{n(n-3)}{2}=20$, so $n(n-3)=40$.",
          "Work back from the answers: $n=8$ gives $8\\cdot5=40$. (The others: $n=5$ gives $5$ diagonals, $n=7$ gives $\\frac{7\\cdot4}{2}=14$, $n=10$ gives $\\frac{10\\cdot7}{2}=35$.)",
          "The polygon has 8 sides."], None),
        (G[7], 'A square, a regular hexagon and a third regular polygon meet at one point. Together they fill the whole angle around the point, with no gaps and no overlaps. How many sides does the third polygon have?',
         ['$8$', '$10$', '$12$', '$15$'], 3,
         ["Around a point: $360°$. The square gives $90°$ and the hexagon gives $120°$.",
          "The third angle: $360°-90°-120°=150°$.",
          "Exterior angle: $180°-150°=30°$, so $n=\\frac{360°}{30°}=12$."], None),
        (G[8], 'ABCDE is a regular pentagon. Triangle ABF is equilateral, and F is inside the pentagon, as shown in the figure. What is the size of angle AEF?',
         ['$48°$', '$66°$', '$72°$', '$84°$'], 2,
         ["$\\angle EAB=108°$ (pentagon) and $\\angle FAB=60°$ (equilateral triangle), so $\\angle EAF=108°-60°=48°$.",
          "$AF=AB$ (triangle) and $AE=AB$ (pentagon), so $AF=AE$: triangle $AEF$ is isosceles.",
          "$\\angle AEF=\\frac{180°-48°}{2}=66°$."], _fig_pent_tri()),
        (G[9], 'A regular octagon is made by cutting four congruent right isosceles triangles off the corners of a square with side $2+\\sqrt2$ cm, as shown in the figure. What is the area of the octagon (in cm²)?',
         ['$2+2\\sqrt2$', '$2+4\\sqrt2$', '$4+4\\sqrt2$', '$6+4\\sqrt2$'], 3,
         ["Let the octagon side be $a$. Each cut triangle has hypotenuse $a$ and legs $\\frac{a}{\\sqrt2}$.",
          "The square side is leg $+$ side $+$ leg: $\\frac{a}{\\sqrt2}+a+\\frac{a}{\\sqrt2}=a+a\\sqrt2=a(1+\\sqrt2)$.",
          "$a(1+\\sqrt2)=2+\\sqrt2=\\sqrt2(\\sqrt2+1)$, so $a=\\sqrt2$ and each leg is $\\frac{\\sqrt2}{\\sqrt2}=1$.",
          "Octagon $=$ square $-$ 4 triangles: $(2+\\sqrt2)^2-4\\cdot\\frac{1\\cdot1}{2}=(6+4\\sqrt2)-2=4+4\\sqrt2$.",
          "Check with the octagon pattern $2a^2+2a^2\\sqrt2$: $a^2=2$, so $4+4\\sqrt2$."], _fig_oct_square()),
        (G[10], 'ABCDEF is a regular hexagon with side 4 cm. What is the area of quadrilateral ACDF (in cm²)?',
         ['$8\\sqrt3$', '$16\\sqrt3$', '$24\\sqrt3$', '$32$'], 2,
         ["Each hexagon angle is $120°$ and $\\angle BCA=30°$ (triangle $ABC$ is isosceles), so $\\angle ACD=120°-30°=90°$. In the same way all four angles of $ACDF$ are right angles: it is a rectangle.",
          "$CD=4$ (a side), and $AC$ is a short diagonal: $AC=4\\sqrt3$.",
          "Area: $4\\sqrt3\\cdot4=16\\sqrt3$.",
          "Check: the hexagon is $6\\cdot\\frac{4^2\\sqrt3}{4}=24\\sqrt3$. $ACDF$ is the hexagon without the corner triangles $ABC$ and $DEF$, each $\\frac16$ of it: $24\\sqrt3-2\\cdot4\\sqrt3=16\\sqrt3$."], _fig_hex_rect()),
    ]
    for qid, stem, ch, cor, ex, fig in new:
        M.new_q(qid, TOPIC, stem, ch, cor, ex, figure=_zoom(fig) if fig else None)
        M.place_q(qid, PRACTICE)

    p = lambda k: 'geo34-core-p%02d' % k
    M.practice_order(PRACTICE, [
        p(3), G[3], p(14), p(26), p(21), p(8), p(7), p(6), p(23), G[6], p(22), G[4], p(11), p(24), p(25), p(27), p(5), p(2),
        p(1), p(18), p(20), p(17), G[7], p(9), G[8], p(13), G[10], p(12), p(16), p(19), p(15), p(4), p(10), G[9]])


# ------------------------------------------------------------------------------------------------
# 4. Figures
# ------------------------------------------------------------------------------------------------
_O_OLD = re.compile(r'<text x="33[23]\.000" y="19[56]\.000"([^>]*)>O</text>')
_O_NEW = r'<text x="348.000" y="191.000"\1>O</text>'


def _figures(M):
    # p09: remove the unused segment FC
    q = M.q('geo34-core-p09'); svg = q['questionVisual']['svg']
    fc = '<line x1="423.238" y1="137.238" x2="277.238" y2="283.238" stroke="#203344" stroke-width="2.5"/>'
    assert fc in svg; M.set_q('geo34-core-p09', figure=svg.replace(fc, ''))

    # g111 (and its slide copies) + slide 12 of the lesson: the "O" label sat on a radius
    q = M.q('geo34-g111'); svg = q['questionVisual']['svg']
    assert _O_OLD.search(svg); M.set_q('geo34-g111', figure=_O_OLD.sub(_O_NEW, svg))
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            for it in b['items']:
                f = it.get('fig') if it.get('k') == 'q' else it.get('v') if it.get('k') == 'vis' else None
                if f and f.get('svg') and _O_OLD.search(f['svg']):
                    f['svg'] = _O_OLD.sub(_O_NEW, f['svg']); M.touched_videos.add(v['id'])

    # v487: the figure had no description
    for it in M.slide(MAIN, 7)['items']:     # "Regular" is slide 7 after the new slide 4
        if it.get('k') == 'vis' and 'aria-label' not in it['v']['svg']:
            it['v']['svg'] = it['v']['svg'].replace('role="img"', 'role="img" aria-label="A regular hexagon and a folded hexagon with equal sides"', 1)

    # all question figures: crop to the drawing (they used about 250 px of the 640 px frame)
    for f in M.D['flow']:
        if f['topic'] == TOPIC and f['type'] == 'question':
            qq = M.q(f['ref']); vis = qq.get('questionVisual')
            if vis and vis.get('svg') and 'viewBox="0 0 640 360"' in vis['svg']:
                M.set_q(f['ref'], figure=_zoom(vis['svg']))


# ------------------------------------------------------------------------------------------------
# Pass 2: a summary lesson right before the practice
# ------------------------------------------------------------------------------------------------
def _summary(M):
    last = [f['ref'] for f in M.D['flow'] if f['section'] == LEARN][-1]
    sb = ['Angle sum', 'One angle', 'Exterior angles', 'Diagonals', 'Triangles inside', 'Areas',
          'Meeting at a point', 'Before you practice']
    M.new_video('r26-t34-summary', TOPIC, 'Polygons: Summary', sb, [
        dict(mode='title', title='Summary', script=[
            "Polygons — a quick summary before you practice.",
            "Everything important from these lessons, one idea at a time.",
        ]),
        dict(title='Angle sum', mode='concept', active=0, pre=[], script=[
            A('S = 180°(n − 2) appears', T('Angle sum: $180°(n-2)$', size=52, gap=40)),
            "The angle sum: 180 times n minus 2. Or split the polygon into n minus 2 triangles.",
            A('+1 side = +180° appears', T('5: $540°$ $\\rightarrow$ 6: $720°$ $\\rightarrow$ 7: $900°$ $\\rightarrow$ 8: $1080°$', size=42, gap=40)),
            "Every extra side adds 180.",
            D('Write "1800° ÷ 180° = 10 triangles → 12 sides"'),
            "Backwards: a sum of 1800 is 10 triangles — 12 sides.",
        ]),
        dict(title='One angle', mode='concept', active=1, pre=[], script=[
            A('one angle appears', T('Regular: one angle $=\\frac{180°(n-2)}{n}=180°-\\frac{360°}{n}$', size=42, gap=40)),
            "Regular means all the sides AND all the angles are equal. Then divide the sum by n.",
            A('three to know appears', T('Pentagon $108°$ $\\cdot$ hexagon $120°$ $\\cdot$ octagon $135°$', size=44, gap=40)),
            "Don't remember one? Find the central angle, 360 over n, and complete it to 180. Octagon: 45 — so 135.",
        ]),
        dict(title='Exterior angles', mode='concept', active=2, pre=[], script=[
            A('exterior angles: 360° appears', T('All the exterior angles together: $360°$', size=46, gap=40)),
            "The exterior angles always add up to 360 — any number of sides.",
            A('n = 360°/(180° − angle) appears', T('$n=\\frac{360°}{180°-\\text{angle}}$', size=52, gap=40)),
            "An angle of a regular polygon is given? 180 minus it — the exterior angle. Then 360 over that.",
            D('Write "140°: 180 − 140 = 40, 360 ÷ 40 = 9 sides"'),
            "140: the exterior angle is 40. 9 sides.",
        ]),
        dict(title='Diagonals', mode='concept', active=3, pre=[], script=[
            A('n − 3 and n(n − 3)/2 appears', T('Diagonals: $n-3$ from one vertex $\\cdot$ $\\frac{n(n-3)}{2}$ in all', size=42, gap=40)),
            "From one vertex: n minus 3. All of them: n times n minus 3, over 2 — each diagonal has two ends.",
            D('Write "hexagon: 6 · 3 ÷ 2 = 9"'),
            A('equal parts appears', T('Regular: the diagonals from a vertex split its angle equally', size=38)),
            "In a regular polygon, the diagonals from one vertex split its angle into equal parts. Hexagon: 120 over 4 — 30 each.",
        ]),
        dict(title='Triangles inside', mode='concept', active=4, pre=[], script=[
            A('n isosceles triangles appears', T('Radii $\\rightarrow$ $n$ congruent isosceles triangles', size=44, gap=40)),
            "Draw the radii of a regular polygon: n congruent isosceles triangles.",
            A('hexagon appears', T('Hexagon, side $a$: 6 equilateral triangles $\\cdot$ short diagonal $a\\sqrt3$ $\\cdot$ long diagonal $2a$', size=36)),
            "The hexagon is special: 6 equilateral triangles. The short diagonal is a root 3, the long one 2a.",
        ]),
        dict(title='Areas', mode='concept', active=5, pre=[], script=[
            A('no formula appears', T('No formula: split into shapes you know', size=46, gap=30)),
            "Polygons have no area formula. Split them into triangles, rectangles, trapezoids.",
            A('big shape minus corners appears', T('Or: a big shape minus the missing pieces', size=46, gap=30)),
            "Or surround them: an octagon is a square minus four corner triangles.",
            A('hexagon area appears', T('Regular hexagon: $6\\cdot\\frac{a^2\\sqrt3}{4}$', size=46)),
            "And in the hexagon, every corner triangle of the star partition is also a sixth of the hexagon.",
        ]),
        dict(title='Meeting at a point', mode='concept', active=6, pre=[], script=[
            A('360° around a point appears', T('Around a point: $360°$', size=50, gap=40)),
            "Polygons meeting at a point: their angles add up to 360.",
            D('Write "360° − 108° − 120° = 132°"'),
            "A pentagon and a hexagon: 360 minus 108 minus 120 — 132.",
            A('common side → isosceles appears', T('Regular polygons on a common side $\\rightarrow$ equal sides $\\rightarrow$ isosceles triangle', size=36)),
            "On a common side, all the sides are equal. Look for the isosceles triangle.",
        ]),
        dict(title='Before you practice', mode='concept', active=7, pre=[], script=[
            "Before each question, ask yourself:",
            A('check 1 appears', T('Is the polygon regular? Only then are all the angles equal.', size=34, gap=24)),
            A('check 2 appears', T('Which angle is it: the polygon’s angle, the exterior angle or the central angle?', size=34, gap=24)),
            A('check 3 appears', T('Which triangles hide here: isosceles from radii, equilateral in a hexagon?', size=34, gap=24)),
            A('check 4 appears', T('Around a point: do the angles add up to $360°$?', size=34, gap=24)),
            "The common traps: dividing the angle sum by n when the polygon is not regular, and counting every diagonal twice.",
            "And a polygon that fits in a circle is not necessarily regular.",
            "You know all of this. Now practice.",
        ]),
    ], LEARN, after=last)
